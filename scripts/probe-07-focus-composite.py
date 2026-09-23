#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe-07-focus-composite.py — D-18 的**反事实证据**,不是门。

它不进四条守卫命令契约(`check-01`…`check-04`),不被任何门禁 / CI 调用,
`scripts/check-05-ui-uat.py` 也不引用它。存在的唯一目的:证明
`/* PAIR --color-focus ON --color-surface NON-TEXT@0.75 */`(`frontend/style.css` 的
PAIR 清单)这条算术断言**真的会失败/成立**,而不是静默空转。

为什么需要这条证明:D-18 已核实,**五个状态样本(`scripts/ui-states/` 的 p1 / p12 /
p3 / checking / archive)的 `#round-doc` 内 `a[href]` 计数为 0** —— 归档半场的
**运行时**断言今天没有服务对象。常驻算术门(`check-02` 的 `@0.75` 条目)因此是唯一的
承担者,而一条没有服务对象的断言很容易悄悄变成空转。本探针把两件事变成可复跑的证据:
「那个服务对象可以被造出来」,以及「造出来之后算术仍然成立」。

做法:起本地应用 → 进入 `archive` 样本 → 在浏览器侧用 `page.evaluate` 向 `#round-doc`
内**合成**一个 `<a href="#">`(**不是**改磁盘文件),然后:

  - 断言注入**真的发生了**(注入前 `#round-doc` 内 `a[href]` 计数 == 0、注入后 == 1)
    —— 空转的注入会让整条证明失去意义(照 `probe-05-resolve-color.py` 的
    「变异必须真的发生」防线);
  - 断言 `#rounds-placeholder.archive-mode` 这个态**真的生效**:类名在位、`#round-doc`
    的计算 `opacity` 恰为 0.75。两者不等即说明被测态与 PAIR 条目所建模的态不是同一个;
  - 用 `page.keyboard.press("Tab")` 把焦点驱动到注入的链接上(程序化聚焦在 Chrome 下
    不保证匹配 `:focus-visible`),读它的计算 `outline-color`,与运行时解析的
    `--color-focus` 对比;
  - 用**运行时实测**的三个输入(环色 / 地面 / 合成因子)复算 `check-02` 的合成算术
    (`composite` + `contrast_ratio`,直接导入它自己的实现,不另写一份),断言比值 >= 3:1。
    这是「归档合成下的环色读数成立」的实证。

不用 `sed`:本机是 darwin,BSD `sed` 的 `0,/re/` 地址会**静默不替换**,那会让注入变成
空转、整条证明失去意义(plan 02 已实测并写成纪律)。注入只走 `page.evaluate`;磁盘上的
`frontend/style.css` 与五个样本**逐字节不变**。

运行方式
    .venv/bin/python scripts/probe-07-focus-composite.py
退出码
    0 = 全部断言成立;1 = 任一条不成立(哪一条写到 stderr)
"""
from __future__ import annotations

import importlib.util
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HARNESS_PATH = ROOT / "scripts" / "check-05-ui-uat.py"
CONTRAST_GATE_PATH = ROOT / "scripts" / "check-02-contrast.py"

# 归档态的合成因子(`frontend/style.css`:
# `#rounds-placeholder.archive-mode #round-doc { opacity: 0.75; }`)。
# 它不是被采信的常量,而是**断言的对象** —— 探针从运行时读 `#round-doc` 的计算
# opacity 与这个期望值比对,不等即说明被测态与 PAIR 条目所建模的态不是同一个。
ARCHIVE_OPACITY = "0.75"
# 注入链接的 id:既是 DOM 句柄,也是 Tab 循环的终止判据。
PROBE_LINK_ID = "idi07-probe-link"
# SC 1.4.11 的非文字阈值,与 check-02 的 NON_TEXT_MIN 同值。
NON_TEXT_MIN = 3.0
# Tab 上限:注入的链接在 `#round-doc` 内,而 `#round-doc` 在文档靠后的位置。
# 40 次远大于实测需要(实测第 2 次即命中),余量用于吸收「click 后第一次 Tab 被吞」。
TAB_LIMIT = 40


def load_harness():
    """按路径导入 harness(文件名带连字符,不能走普通 import)。

    该文件末尾是 `if __name__ == "__main__": sys.exit(main())`,导入无副作用。
    复用它的 helper 而不是复制实现 —— 否则探针测的就不是真实 helper。
    """
    spec = importlib.util.spec_from_file_location("check05_ui_uat", HARNESS_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_contrast_gate():
    """按路径导入 `check-02`(PAIR 清单算术的权威实现),同样复用而不复制。

    `composite()` 只住在 `check-02` 里 —— 本探针要证明的正是**它**那条算术,
    所以必须用它的实现算,不能自己写一份「差不多的」。
    """
    spec = importlib.util.spec_from_file_location("check02_contrast", CONTRAST_GATE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def require(cond, msg):
    if not cond:
        print(f"PROBE FAILED: {msg}", file=sys.stderr, flush=True)
        raise SystemExit(1)


# ---------------------------------------------------------------------------
# 页面侧的三段脚本
# ---------------------------------------------------------------------------
# 态的前提检查:archive-mode 类名在位、`#round-doc` 可见且其计算 opacity 就是合成因子。
_STATE_JS = """() => {
  const rp = document.querySelector('#rounds-placeholder');
  const rd = document.querySelector('#round-doc');
  if (!rp || !rd) return null;
  return {
    archiveModeClass: rp.classList.contains('archive-mode'),
    placeholderClasses: [...rp.classList],
    docVisible: rd.getClientRects().length > 0,
    docOpacity: getComputedStyle(rd).opacity,
  };
}"""

# 注入前/后的计数普查 —— 这是「变异必须真的发生」的防线。
_COUNT_LINKS_JS = """() => {
  const rd = document.querySelector('#round-doc');
  if (!rd) return null;
  return rd.querySelectorAll('a[href]').length;
}"""

# 注入:在 `#round-doc` 内**合成**一个 `<a href>`。只活在页面里,不落盘。
_INJECT_JS = """(id) => {
  const rd = document.querySelector('#round-doc');
  if (!rd) return null;
  const a = document.createElement('a');
  a.href = '#';
  a.id = id;
  a.textContent = '归档合成探针链接';
  rd.appendChild(a);
  return rd.querySelectorAll('a[href]').length;
}"""

# 焦点读数:当前 `document.activeElement` 的那一瞬。
_FOCUS_READ_JS = """() => {
  const el = document.activeElement;
  if (!(el instanceof HTMLElement)) return null;
  return {
    tag: el.tagName.toLowerCase(),
    id: el.id,
    focusVisible: el.matches(':focus-visible'),
  };
}"""


def main():
    h5 = load_harness()
    c2 = load_contrast_gate()
    server = h5.ensure_server()
    tmp_root = Path(tempfile.mkdtemp(prefix="idi-07-probe-"))
    pw = browser = None
    failures = []
    try:
        from playwright.sync_api import sync_playwright

        pw = sync_playwright().start()
        # 与 harness 默认的 --browser bundled 一致,不引入新的浏览器选择逻辑。
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.set_default_timeout(20000)

        proj = h5.make_fixture("archive", tmp_root)
        h5.enter_project(page, proj)

        # ---- 1. 态的前提检查 -------------------------------------------------
        state = page.evaluate(_STATE_JS)
        require(state is not None,
                "#rounds-placeholder / #round-doc 读不到 —— 被测态造不出")
        require(state["archiveModeClass"],
                "#rounds-placeholder 不在 archive-mode(实测类名 "
                f"{state['placeholderClasses']})")
        require(state["docVisible"], "#round-doc 不可见 —— 环无从渲染")
        require(state["docOpacity"] == ARCHIVE_OPACITY,
                f"#round-doc 的计算 opacity 是 {state['docOpacity']},期望 "
                f"{ARCHIVE_OPACITY} —— 被测态与 PAIR 条目所建模的 0.75 合成不是同一个")
        print(f"PROBE archive-state opacity={state['docOpacity']} "
              f"visible={state['docVisible']}", flush=True)

        # ---- 2. 注入前:运行时断言今天确实没有服务对象 -----------------------
        before = page.evaluate(_COUNT_LINKS_JS)
        require(before is not None, "#round-doc 读不到,计数失败")
        require(before == 0,
                f"注入前 #round-doc 内 a[href] 计数为 {before},期望 0 —— "
                "D-18 的前提(归档半场无服务对象)不成立")
        print("PROBE links-before=0", flush=True)

        # ---- 3. 注入(只走浏览器侧,磁盘逐字节不变)--------------------------
        after = page.evaluate(_INJECT_JS, PROBE_LINK_ID)
        require(after is not None, "#round-doc 读不到,注入失败")
        require(after == 1,
                f"注入后 #round-doc 内 a[href] 计数为 {after},期望 1 —— "
                "注入空转,整条证明失去意义")
        print("PROBE links-after=1 (mutation-applied=yes)", flush=True)

        # ---- 4. Tab 驱动焦点到注入的链接(程序化聚焦不保证 :focus-visible)----
        focused = None
        for _ in range(TAB_LIMIT):
            page.keyboard.press("Tab")
            cur = page.evaluate(_FOCUS_READ_JS)
            if cur and cur["id"] == PROBE_LINK_ID:
                focused = cur
                break
        require(focused is not None,
                "Tab 未把焦点驱动到注入的链接上 —— 读不到环,本探针无法成立")
        require(focused["focusVisible"],
                "注入的链接成为 activeElement 但 :focus-visible 为假 —— "
                "环规则不适用,读数无意义")
        print(f"PROBE focus={focused}", flush=True)

        # ---- 5. 环色读数 vs 运行时解析的令牌 ---------------------------------
        ring_css = h5.read_style(page, f"#{PROBE_LINK_ID}", "outline-color")
        ring_width = h5.read_style(page, f"#{PROBE_LINK_ID}", "outline-width")
        expected = h5.resolve_color(page, "--color-focus")
        require(expected is not None, "--color-focus 解析不出 —— 令牌未声明")
        require(h5.norm(ring_css) == h5.norm(expected),
                f"注入链接的 outline-color {ring_css} != 运行时解析的 "
                f"--color-focus {expected}")
        require(ring_width == "2px",
                f"注入链接的 outline-width 是 {ring_width},期望 2px")
        print(f"PROBE ring outline-color={ring_css} outline-width={ring_width}", flush=True)

        # ---- 6. 归档合成下的算术(三个输入全部来自运行时实测)----------------
        ground_css = h5.effective_bg(page, f"#{PROBE_LINK_ID}")
        ring_rgb = h5.parse_rgb(ring_css)
        ground_rgb = h5.parse_rgb(ground_css)
        require(ring_rgb is not None, f"环色解析不出 rgb:{ring_css}")
        require(ground_rgb is not None, f"地面解析不出 rgb:{ground_css}")
        alpha = float(state["docOpacity"])
        composited = c2.composite(ring_rgb, ground_rgb, alpha)
        ratio = c2.contrast_ratio(composited, ground_rgb)
        require(ratio >= NON_TEXT_MIN,
                f"归档合成下环色对地面 {ground_css} 的对比度 {ratio:.2f} < "
                f"{NON_TEXT_MIN}:1(环 {ring_rgb} 以 alpha {alpha} 合成到 {composited})")
        print(f"PROBE composite ring={ring_rgb} ground={ground_css} alpha={alpha} "
              f"composited={composited} ratio={ratio:.2f} (>= {NON_TEXT_MIN})",
              flush=True)

        ctx.close()
    except SystemExit as e:
        # **非 `require` 的失败也必须写到 stderr。** 上面那段 docstring 承诺
        # 「哪一条写到 stderr」,而 `require()` 是唯一自己打印的抛出点:本块里其余
        # `SystemExit`(最典型的是 `h5.make_fixture()` 对缺失样本抛的
        # `ERROR: 状态样本不存在: …`)原先只被 append 进 `failures`,`str(e)` 从不打印
        # ⇒ 退出码 1 配一个**空的 stderr**,操作者分不清「断言失败」与「样本没到位」。
        print(f"PROBE FAILED: {e}", file=sys.stderr, flush=True)
        failures.append(str(e))
    finally:
        if browser is not None:
            browser.close()
        if pw is not None:
            pw.stop()
        if server is not None:
            server.terminate()
            try:
                server.wait(timeout=10)
            except Exception:
                server.kill()
        shutil.rmtree(tmp_root, ignore_errors=True)

    if failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

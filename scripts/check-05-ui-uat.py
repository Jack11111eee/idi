#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check-05-ui-uat.py — idi-04 UAT 6 项的浏览器实检 harness(Playwright + 系统 Chrome)。

用途
    `.planning/phases/idi-04-tokens-contract/idi-04-UAT.md` 的 6 项此前全部以
    「本环境无法自动化」为由挂在 `pending`。本脚本把那条路径固化下来:启动本地应用 →
    系统 Chrome → 经 `#enter-path-input` 进入一个磁盘状态样本 → 用
    `getComputedStyle` 读真实 computed style → 逐条断言并打印 expected vs actual。

前置条件
    - 项目 `.venv` 已装 `requirements-dev.txt`(即 `.venv/bin/pip install -r requirements-dev.txt`)。
    - 浏览器:**不需要**执行 `playwright install`,零下载。默认走 Playwright 自带的
      chromium(`--browser bundled`):playwright 1.63.0 对应的 revision 1243 已在本机
      `~/Library/Caches/ms-playwright/` 中,且是 arm64 原生。
    - `scripts/ui-states/` 下 5 个磁盘状态样本在位(p1 / p12 / p3 / checking / archive)。

浏览器选择(实测结论,不是偏好)
    **默认 `--browser bundled`**。计划原写「必须用系统 Chrome(channel="chrome")」,
    其两条理由在本机都已失效,实测如下:
      1. 「捆绑版 chromium 报 Executable doesn't exist at .../chromium-1243」——
         **已失效**。本 venv 装的 playwright 1.63.0 正好对应 revision 1243,该目录
         已在缓存里(chrome-mac-arm64),`launch()` 0.5s 成功,零下载。
      2. 「channel='chrome' 无需 playwright install」——**仍成立但不可用于无头**。
         本 venv 的 Python 是 x86_64(Rosetta),spawn 出来的系统 Chrome 会跑 x86_64 切片;
         `channel="chrome"` + `headless=True` 在本机 **CDP 永不连上,180s 超时挂死**
         (Chrome 自己打印 "The use of Rosetta to run the x64 version of Chromium on Arm
         is neither tested nor maintained")。同一台机器上 `headless=False` 则 6.6s 成功。
    故:`--browser chrome` 仍保留,但它强制有头(headless=False),不能无人值守。

运行方式
    .venv/bin/python scripts/check-05-ui-uat.py                 # 跑 UAT 第 1..6 项
    .venv/bin/python scripts/check-05-ui-uat.py --item smoke    # 只跑 harness 自检切片
    .venv/bin/python scripts/check-05-ui-uat.py --item 1 --item 2
    .venv/bin/python scripts/check-05-ui-uat.py --ai-smoke      # 额外真跑两次 AI 交互冒烟
    .venv/bin/python scripts/check-05-ui-uat.py --keep          # 保留临时工作目录供排查
    .venv/bin/python scripts/check-05-ui-uat.py --browser chrome  # 改用系统 Chrome(有头)

退出码语义
    0 = 所选项全部 pass
    1 = 至少一项含 FAIL 断言
    2 = 无 FAIL,但至少一项含 BLOCKED 断言(状态造不出 / 元素不可见 / 选择器不存在)

设计要点
    - **fixture 隔离**:每次进入一个样本都复制到 `tempfile.mkdtemp()` 下的新副本,
      应用只碰副本;仓库样本永远只读。故 harness 幂等,可重复运行且结论一致。
    - **服务生命周期**:先探测 `127.0.0.1:8765`;已在服务则复用,结束时不动它;
      未服务才自己 `Popen` uvicorn,结束时只关掉自己起的那个进程。
    - **导航**:`wait_until="domcontentloaded"` + 显式 `wait_for_timeout`。
      应用常驻 `/api/events` SSE 长连接,`networkidle` 永不返回,禁止使用。
    - **绝不静默判过**:读不到的记 BLOCKED 并写明原因,失败就是 FAIL。

已知限制(不试图绕过)
    **键盘文本选区无法自动化**:`keyboard.press("Shift+ArrowRight")` 与
    `down("Shift")+press()` 两种写法,在普通 `<p>`、`tabindex` 容器、甚至
    `contenteditable` 里都选不中任何文字(`window.getSelection()` 恒为空),
    `--enable-caret-browsing` 也无效。故任何依赖 Shift+方向键选字的验收项无法自动验证。
    本 UAT 的 6 项里没有这类项,但这条限制真实存在,记录在此供后续验收参考。
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATES_SRC = ROOT / "scripts" / "ui-states"
VENV_UVICORN = ROOT / ".venv" / "bin" / "uvicorn"
HOST, PORT = "127.0.0.1", 8765
BASE_URL = f"http://{HOST}:{PORT}"

# ---------------------------------------------------------------------------
# 断言记录器:每条恒打印 PASS/FAIL/BLOCKED + expected vs actual
# ---------------------------------------------------------------------------
ROWS: list[dict] = []


def _emit(item, verdict, label, expected, actual, note=""):
    ROWS.append(
        {
            "item": item,
            "verdict": verdict,
            "label": label,
            "expected": expected,
            "actual": actual,
            "note": note,
        }
    )
    line = f"{verdict} {label}: expected={expected} actual={actual}"
    if note:
        line += f"  # {note}"
    print(line, flush=True)


def ok(item, label, expected, actual, note=""):
    """等值断言;actual 为 None 表示元素/选择器不存在 → BLOCKED,绝不记 pass。

    比较前对 rgb()/rgba() 内部空白做归一:UAT 里写 `rgb(106,106,106)`,
    Chrome 序列化成 `rgb(106, 106, 106)` —— 这是序列化差异,不是产品差异。
    打印的仍是原始 actual,失败可独立诊断。
    """
    if actual is None:
        _emit(item, "BLOCKED", label, expected, "<MISSING>", "元素/选择器不存在")
    elif norm(actual) == norm(expected):
        _emit(item, "PASS", label, expected, actual, note)
    else:
        _emit(item, "FAIL", label, expected, actual, note)


def norm(value):
    """把 rgb()/rgba() 内部的空白抹平,使 UAT 的紧凑写法与 Chrome 的序列化可比。"""
    if not isinstance(value, str):
        return value
    return re.sub(r"(rgba?\([^)]*\))", lambda m: re.sub(r"\s+", "", m.group(1)), value)


def ok_true(item, label, cond, expected, actual, note=""):
    _emit(item, "PASS" if cond else "FAIL", label, expected, actual, note)


def ok_contains(item, label, needle, actual, note=""):
    if actual is None:
        _emit(item, "BLOCKED", label, f"contains {needle}", "<MISSING>", "元素/选择器不存在")
        return
    _emit(
        item,
        "PASS" if norm(needle) in norm(actual) else "FAIL",
        label,
        f"contains {needle}",
        actual,
        note,
    )


def blocked(item, label, expected, actual, reason):
    _emit(item, "BLOCKED", label, expected, actual, reason)


def info(label, text):
    """诊断行——不参与判定,只为让失败可独立诊断。"""
    print(f"INFO {label}: {text}", flush=True)


def item_verdict(item):
    vs = [r["verdict"] for r in ROWS if r["item"] == item]
    if not vs:
        return "blocked"
    if "FAIL" in vs:
        return "fail"
    if "BLOCKED" in vs:
        return "blocked"
    return "pass"


# ---------------------------------------------------------------------------
# WCAG 相对亮度 / 对比度(与 scripts/check-02-contrast.py 同款公式)
# ---------------------------------------------------------------------------
def channel_luminance(channel):
    c = channel / 255.0
    if c <= 0.03928:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb):
    r, g, b = rgb[:3]
    return (
        0.2126 * channel_luminance(r)
        + 0.7152 * channel_luminance(g)
        + 0.0722 * channel_luminance(b)
    )


def contrast_ratio(fg, bg):
    lf, lb = relative_luminance(fg), relative_luminance(bg)
    light, dark = max(lf, lb), min(lf, lb)
    return (light + 0.05) / (dark + 0.05)


_RGB_RE = re.compile(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)")


def parse_rgb(css_color):
    """'rgb(1, 2, 3)' / 'rgba(1, 2, 3, 1)' → (1, 2, 3);解析不出返回 None。"""
    if not css_color:
        return None
    m = _RGB_RE.match(css_color)
    return tuple(int(x) for x in m.groups()) if m else None


# ---------------------------------------------------------------------------
# 服务生命周期
# ---------------------------------------------------------------------------
def port_open(host, port):
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


def ensure_server():
    """返回自己起的 Popen;若端口已在服务则返回 None(复用,不关)。"""
    if port_open(HOST, PORT):
        info("server", f"{HOST}:{PORT} 已在服务 —— 复用,不新起、结束时也不关闭")
        return None
    if not VENV_UVICORN.exists():
        raise SystemExit(f"ERROR: 找不到 {VENV_UVICORN}")
    info("server", f"{HOST}:{PORT} 未服务 —— 自行启动 uvicorn")
    proc = subprocess.Popen(
        [str(VENV_UVICORN), "backend.main:app", "--port", str(PORT)],
        cwd=str(ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(120):
        if port_open(HOST, PORT):
            return proc
        time.sleep(0.5)
    proc.terminate()
    raise SystemExit("ERROR: uvicorn 启动超时(60s)")


# ---------------------------------------------------------------------------
# 页面读取器
# ---------------------------------------------------------------------------
_READ_JS = """([sel, prop]) => {
  const el = document.querySelector(sel);
  if (!el) return null;
  return getComputedStyle(el)[prop];
}"""


def read_style(page, selector, prop):
    return page.evaluate(_READ_JS, [selector, prop])


def read_classlist(page, selector):
    return page.evaluate(
        "(sel) => { const el = document.querySelector(sel); return el ? [...el.classList] : null; }",
        selector,
    )


def resolve_color(page, token):
    """把令牌解析成归一化的 computed rgb —— 挂一个探针元素读它的 color。"""
    return page.evaluate(
        """(t) => {
            const p = document.createElement('div');
            p.style.color = `var(${t})`;
            document.body.appendChild(p);
            const c = getComputedStyle(p).color;
            p.remove();
            return c;
        }""",
        token,
    )


def effective_bg(page, selector):
    """沿祖先链找到第一个非透明 background-color(元素自身优先)。"""
    return page.evaluate(
        """(sel) => {
            let el = document.querySelector(sel);
            while (el) {
                const bg = getComputedStyle(el).backgroundColor;
                if (bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') return bg;
                el = el.parentElement;
            }
            return getComputedStyle(document.documentElement).backgroundColor;
        }""",
        selector,
    )


# ---------------------------------------------------------------------------
# fixture 隔离
# ---------------------------------------------------------------------------
def make_fixture(name, tmp_root):
    """把 scripts/ui-states/<name> 复制到临时目录的新副本,返回其绝对路径。"""
    src = STATES_SRC / name
    if not src.is_dir():
        raise SystemExit(f"ERROR: 状态样本不存在:{src}")
    dest = Path(tempfile.mkdtemp(dir=str(tmp_root), prefix=f"{name}-"))
    dest = dest / name
    shutil.copytree(src, dest)
    return dest


def write_annotations(project_path, round_n, items):
    docs = project_path / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    payload = {"round": round_n, "items": items}
    (docs / f"discuss-round-{round_n}.annotations.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def enter_project(page, project_path):
    """导航 + 进入项目。SSE 常驻 ⇒ 禁止 networkidle,用显式等待。"""
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(1200)
    page.fill("#enter-path-input", str(project_path))
    page.click("#btn-enter")
    page.wait_for_timeout(2500)


def reload_project(page):
    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(2500)


# ---------------------------------------------------------------------------
# UAT 第 1 项 — SC4 浏览器实检
# ---------------------------------------------------------------------------
# 元素 × 状态 期望矩阵:由 frontend/app.js 的状态分支逐条读出,不靠运行期猜。
#   hidden  = app.js 在该状态给该元素**自身**加了 .hidden(故 display 必须为 none)
#   visible = app.js 在该状态没有给该元素自身加 .hidden
# 注意:visible 只断言「自身 .hidden 未生效」;元素是否被祖先藏住另由 offsetParent 诊断行体现。
HIDDEN_MATRIX = {
    "#draft-empty": {
        "p1": "visible",  # renderDraft(null) → remove('hidden')
        "p12": "hidden",  # draft 有内容 → add('hidden')
        "p3": "visible",
        "checking": "visible",
        "archive": "visible",
    },
    "#rounds-hint": {
        "p1": "visible",  # applySessionGates 未触碰
        "p12": "visible",
        "p3": "hidden",  # loadRoundsView: roundsHint.add('hidden')
        "checking": "hidden",  # applyPhase5View
        "archive": "hidden",  # applyArchiveView
    },
    "#btn-process-round": {
        "p1": "visible",  # applySessionGates 复位 remove('hidden')
        "p12": "visible",
        "p3": "visible",
        "checking": "visible",
        "archive": "hidden",  # applyArchiveView: 只读防线
    },
    "#round-switcher": {
        "p1": "visible",
        "p12": "visible",
        "p3": "visible",
        "checking": "hidden",  # applyPhase5View
        "archive": "visible",  # applyArchiveView: remove('hidden')
    },
    "#writing-hint": {
        # app.js 只对 writingHint 调 remove('hidden')(applyWritingView),从不 add;
        # 它在样本状态里是被祖先 #writing-view 藏住的。故 5 个样本的自身 display 均非 none。
        "p1": "visible",
        "p12": "visible",
        "p3": "visible",
        "checking": "visible",
        "archive": "visible",
    },
    "#session-panel": {
        # 主区承载「操作对象」:阶段 1-2 会话流 / 阶段 3+ 批注流——是切换不是叠加
        # (§4.1 说明 1、§4.2 第 4 条,D-P2-2)。app.js 在 applySessionGates 单点 toggle。
        "p1": "visible",
        "p12": "visible",
        "p3": "hidden",
        "checking": "hidden",
        "archive": "hidden",
    },
}

# 三个 1-0-0 竞争者:#selection-menu / #annotations-panel / #checks-panel
# 以 ID 特异性声明 display:flex,压过 .hidden(0-1-0)——CHECK-03 只证明规则文本唯一,
# 不证明它仍赢得层叠。这里的强制加类断言才是那一步。
COMPETITORS = ["#selection-menu", "#annotations-panel", "#checks-panel"]
STATES = ["p1", "p12", "p3", "checking", "archive"]


def item1(page, tmp_root):
    item = "1"
    # 注:#session-panel 同时是 1-0-0 的 display:flex 竞争者(style.css:566),
    # 但它不进 COMPETITORS —— 那个列表的既有语义专指 CHECK-03 的三元素。
    # 其「强制加类 → 隐藏」的层叠证据由下方 list(HIDDEN_MATRIX) + COMPETITORS 循环覆盖。
    print("\n=== UAT 1: SC4 browser 实检 — six .hidden-only elements ===", flush=True)
    for state in STATES:
        proj = make_fixture(state, tmp_root)
        enter_project(page, proj)
        for sel, expect_map in HIDDEN_MATRIX.items():
            disp = read_style(page, sel, "display")
            own_visible = disp is not None and disp != "none"
            offset_parent = page.evaluate(
                "(sel) => { const el = document.querySelector(sel); return el ? el.offsetParent === null : null; }",
                sel,
            )
            info(
                f"[{state}] {sel}",
                f"display={disp} offsetParent_is_null={offset_parent}",
            )
            if expect_map[state] == "hidden":
                ok(item, f"[{state}] {sel} 自身 .hidden 生效", "none", disp)
            else:
                ok_true(
                    item,
                    f"[{state}] {sel} 自身未被 .hidden 藏",
                    own_visible,
                    "display!=none",
                    disp,
                )
    # 强制施加强制类:证明 .hidden 对每个元素自身都赢得层叠(1-0-0 竞争者亦然)
    proj = make_fixture("p3", tmp_root)
    enter_project(page, proj)
    for sel in list(HIDDEN_MATRIX) + COMPETITORS:
        added = page.evaluate(
            "(sel) => { const el = document.querySelector(sel); if (!el) return null; el.classList.add('hidden'); return true; }",
            sel,
        )
        disp = read_style(page, sel, "display") if added else None
        ok(item, f"[p3] {sel} 强制 .hidden → 隐藏", "none", disp)
    # 「仅由 .hidden 决定」的反向证据:摘掉 .hidden 后自身必须重新可见
    for sel in HIDDEN_MATRIX:
        removed = page.evaluate(
            "(sel) => { const el = document.querySelector(sel); if (!el) return null; el.classList.remove('hidden'); return true; }",
            sel,
        )
        disp = read_style(page, sel, "display") if removed else None
        ok_true(
            item,
            f"[p3] {sel} 摘掉 .hidden → 自身可见",
            disp is not None and disp != "none",
            "display!=none",
            disp,
        )
    note = (
        "#writing-hint 在 5 个样本状态中没有任何一格是「app.js 给自身加 .hidden」——"
        "它只被祖先 #writing-view 藏住;其自身 .hidden 由上面的强制加类断言覆盖"
    )
    info("item1 覆盖说明", note)


# ---------------------------------------------------------------------------
# 冻结轮读取器(第 2 项与第 4 项共用)
# ---------------------------------------------------------------------------
FROZEN_AMBER = "rgb(138, 101, 8)"


def parse_box_shadow(raw):
    """解析 computed box-shadow。Chrome 序列化为 'color x y blur spread[ inset]'。"""
    if not raw or raw == "none":
        return None
    inset = "inset" in raw
    s = raw.replace("inset", " ").strip()
    m = re.search(r"rgba?\([^)]*\)|#\w+", s)
    color = m.group(0) if m else None
    rest = re.sub(r"rgba?\([^)]*\)|#\w+", " ", s).split()
    if len(rest) != 4:
        return None
    return {"inset": inset, "color": color, "x": rest[0], "y": rest[1], "blur": rest[2], "spread": rest[3]}


def goto_frozen_round(page, item):
    """在 p3 样本上把 #round-switcher 切到第 1 轮(历史轮),返回 page。"""
    page.select_option("#round-switcher", value="1")
    page.wait_for_timeout(2000)


def check_frozen_marker(page, item, label_prefix):
    classes = read_classlist(page, "#round-doc")
    ok_true(
        item,
        f"{label_prefix} #round-doc 带 round-frozen",
        classes is not None and "round-frozen" in classes,
        "round-frozen in classList",
        classes,
    )
    raw = read_style(page, "#round-doc", "box-shadow")
    info(f"{label_prefix} box-shadow 原始值", repr(raw))
    parsed = parse_box_shadow(raw) if raw else None
    if parsed is None:
        blocked(
            item,
            f"{label_prefix} 冻结轮 box-shadow 语义",
            "inset 3px 0 0 rgb(138, 101, 8)",
            raw,
            "box-shadow 缺失或无法解析",
        )
    else:
        semantic_ok = (
            parsed["inset"]
            and parsed["x"] == "3px"
            and parsed["y"] == "0px"
            and parsed["blur"] == "0px"
            and parsed["spread"] == "0px"
            and parsed["color"] == FROZEN_AMBER
        )
        ok_true(
            item,
            f"{label_prefix} 冻结轮 box-shadow 语义(inset/3px/0/0/0/amber)",
            semantic_ok,
            "inset 3px 0 0 rgb(138, 101, 8)",
            raw,
            "Chrome 序列化为 'color x y blur spread inset',故用语义解析而非子串全等",
        )
        info(
            f"{label_prefix} UAT 字面子串",
            f"'inset 3px 0 0 rgb(138, 101, 8)' present={('inset 3px 0 0 rgb(138, 101, 8)' in (raw or ''))}"
            " —— Chrome 把颜色放在最前、inset 放在最后,该字面序不存在(harness 规格修正,非产品缺陷)",
        )
    ok(item, f"{label_prefix} 冻结轮 opacity", "1", read_style(page, "#round-doc", "opacity"))
    ok(item, f"{label_prefix} 冻结轮 filter", "saturate(0.6)", read_style(page, "#round-doc", "filter"))


def item2(page, tmp_root):
    item = "2"
    print("\n=== UAT 2: 冻结轮 backstop ===", flush=True)
    proj = make_fixture("p3", tmp_root)
    enter_project(page, proj)
    goto_frozen_round(page, item)
    check_frozen_marker(page, item, "[p3→round1]")
    # 正文对比度 ≥ 4.5:1 —— 取 #round-doc 内首个**正文** <p>(即不在 blockquote 内的)
    # 的 color 与其实际背景。blockquote 是刻意弱化的引用块(--color-text-muted),
    # 不属 UAT 所称「正文」;其比值另作 INFO 记录。
    colors = page.evaluate("""() => {
        const ps = [...document.querySelectorAll('#round-doc p')];
        const body = ps.find((p) => !p.closest('blockquote'));
        const quoted = ps.find((p) => p.closest('blockquote'));
        return {
            body: body ? getComputedStyle(body).color : null,
            quoted: quoted ? getComputedStyle(quoted).color : null,
        };
    }""")
    fg = colors["body"]
    bg = effective_bg(page, "#round-doc")
    fg_rgb, bg_rgb = parse_rgb(fg), parse_rgb(bg)
    if fg_rgb is None or bg_rgb is None:
        blocked(item, "[p3→round1] 正文对比度", ">=4.5:1", f"color={fg} bg={bg}", "取色失败")
    else:
        ratio = contrast_ratio(fg_rgb, bg_rgb)
        ok_true(
            item,
            "[p3→round1] 正文对比度",
            ratio >= 4.5,
            ">=4.5:1",
            f"ratio={ratio:.2f} (color={fg} on bg={bg})",
        )
    # 诊断:引用块(--color-text-muted)的比值。UAT 未把它算作「正文」,故只记录不判定。
    q_rgb = parse_rgb(colors["quoted"])
    if q_rgb is not None and bg_rgb is not None:
        qr = contrast_ratio(q_rgb, bg_rgb)
        info("[p3→round1] blockquote 比值(诊断,非正文)",
             f"ratio={qr:.2f} (color={colors['quoted']} on bg={bg})"
             " —— --color-text-muted 在 260918-qrq 换肤后由 #6a6a6a 变为 #8f8f8f,低于 AA 4.5:1")


# ---------------------------------------------------------------------------
# UAT 第 3 项 — Plan 01 的 13 项 computed-style 抽查
# ---------------------------------------------------------------------------
def item3(page, tmp_root):
    item = "3"
    print("\n=== UAT 3: DevTools computed-style 抽查 — Plan 01(13 项)===", flush=True)

    # --- p1:.hint(说明文字,文档面板内)---
    proj = make_fixture("p1", tmp_root)
    enter_project(page, proj)
    ok(item, "[p1] .hint color", "rgb(106,106,106)", read_style(page, ".hint", "color"))
    ok(item, "[p1] #ai-route-select border-top-color", "rgb(138,138,138)",
       read_style(page, "#ai-route-select", "border-top-color"))
    ok(item, "[p1] #selection-menu border-top-color", "rgb(138,138,138)",
       read_style(page, "#selection-menu", "border-top-color"))
    ok(item, "[p1] #stream-banner border-top-color", "rgb(138,101,8)",
       read_style(page, "#stream-banner", "border-top-color"))
    ok_contains(item, "[p1] .overlay-card box-shadow 含 rgba(0,0,0,0.2)",
                "rgba(0, 0, 0, 0.2)", read_style(page, ".overlay-card", "box-shadow"))
    # .kind-write / .kind-done 事件行:用应用自身的 renderEvent 渲染(不触发 AI 调用)
    page.evaluate("""() => {
        renderEvent({ kind: 'write', content: 'harness: kind-write 探针', raw: null });
        renderEvent({ kind: 'done', content: 'harness: kind-done 探针', raw: null });
    }""")
    ok(item, "[p1] .kind-write .event-kind background", "rgb(38,117,74)",
       read_style(page, ".kind-write .event-kind", "background-color"))
    ok(item, "[p1] .kind-done .event-kind background", "rgb(0,0,0)",
       read_style(page, ".kind-done .event-kind", "background-color"))
    # .chat-user:用应用自身的 appendChatMessage 渲染(不触发 AI 调用)
    page.evaluate("() => { appendChatMessage('user', 'harness: .chat-user 探针'); }")
    ok(item, "[p1] .chat-user background", "rgb(31,99,189)",
       read_style(page, ".chat-user", "background-color"))
    info("item3 构造说明",
         ".kind-write/.kind-done/.chat-user 三处用应用自身的 renderEvent/appendChatMessage 渲染探针节点"
         "(真实代码路径,零 AI 调用、零网络)")

    # --- p3:#btn-authorize / #btn-process-round / #state-badge / .badge-answered ---
    proj = make_fixture("p3", tmp_root)
    write_annotations(proj, 2, [
        {
            "id": "harness-1",
            "quote": "建议进入授权环节",
            "before": "",
            "type": "comment",
            "note": "harness 探针批注(已回应)",
            "status": "answered",
            "answer": "harness 探针回应",
            "created_at": "2026-09-19T00:00:00+00:00",
        }
    ])
    enter_project(page, proj)
    ok(item, "[p3] #btn-authorize color", "rgb(38,117,74)", read_style(page, "#btn-authorize", "color"))
    ok(item, "[p3] #btn-authorize border-color", "rgb(38,117,74)",
       read_style(page, "#btn-authorize", "border-top-color"))
    ok(item, "[p3] #btn-authorize background-color", "rgb(233,247,239)",
       read_style(page, "#btn-authorize", "background-color"))
    proc_color = read_style(page, "#btn-process-round", "color")
    proc_border = read_style(page, "#btn-process-round", "border-top-color")
    proc_bg = read_style(page, "#btn-process-round", "background-color")
    auth_color = read_style(page, "#btn-authorize", "color")
    auth_border = read_style(page, "#btn-authorize", "border-top-color")
    auth_bg = read_style(page, "#btn-authorize", "background-color")
    ok_true(
        item,
        "[p3] #btn-process-round 与 #btn-authorize 三属性逐字节相同",
        (proc_color, proc_border, proc_bg) == (auth_color, auth_border, auth_bg),
        f"({auth_color}, {auth_border}, {auth_bg})",
        f"({proc_color}, {proc_border}, {proc_bg})",
    )
    ok(item, "[p3] #state-badge color", "rgb(31,99,189)", read_style(page, "#state-badge", "color"))
    ok(item, "[p3] #state-badge background-color", "rgb(238,244,255)",
       read_style(page, "#state-badge", "background-color"))
    ok(item, "[p3] .badge-answered color", "rgb(106,106,106)",
       read_style(page, ".badge-answered", "color"))


# ---------------------------------------------------------------------------
# UAT 第 4 项 — Plan 02 的 16 项
# ---------------------------------------------------------------------------
def item4(page, tmp_root):
    item = "4"
    print("\n=== UAT 4: DevTools computed-style 抽查 — Plan 02(16 项)===", flush=True)
    proj = make_fixture("p1", tmp_root)
    enter_project(page, proj)

    ok(item, "[p1] .panel-header padding-top", "10px", read_style(page, ".panel-header", "padding-top"))
    ok(item, "[p1] .panel-header padding-left", "16px", read_style(page, ".panel-header", "padding-left"))
    # #doc-pane 在 index.html 里不存在(实际 id 是 #doc-panel / #doc-panel-body)
    doc_pane = read_style(page, "#doc-pane", "padding")
    blocked(
        item,
        "[p1] #doc-pane padding",
        "32px 40px",
        "<MISSING>",
        "选择器 #doc-pane 不存在(index.html 里实际为 #doc-panel-body)——"
        f"诊断:#doc-panel-body padding={read_style(page, '#doc-panel-body', 'padding')}",
    )
    info("item4 #doc-pane", f"raw read={doc_pane}")
    # 探针说明:`button` 指的是**通用 button 规则**(D-16 账本里的 6px/10px)。
    # 用 #btn-enter —— 它没有更具体的选择器覆盖 padding/color;而 document.querySelector('button')
    # 落在 #btn-send 上(#chat-input-row button,0-1-1,8px/16px + 主色前景),不是通用规则的探针。
    ok(item, "[p1] button padding-top(通用规则,探针 #btn-enter)", "6px",
       read_style(page, "#btn-enter", "padding-top"))
    ok(item, "[p1] button padding-left(通用规则,探针 #btn-enter)", "10px",
       read_style(page, "#btn-enter", "padding-left"))
    ok(item, "[p1] .overlay-card padding-top", "24px", read_style(page, ".overlay-card", "padding-top"))
    info("item4 .overlay-card", f"padding={read_style(page, '.overlay-card', 'padding')}")
    # #brainstorm-view 的「24px」:该元素上唯一的 24px 是 margin-top(--space-6);
    # 其 padding 是 D-16 映射的 --space-3/--space-3-5(12px/14px)。按 margin-top 判读。
    ok(item, "[p1] #brainstorm-view margin-top", "24px", read_style(page, "#brainstorm-view", "margin-top"))
    info("item4 #brainstorm-view",
         f"padding={read_style(page, '#brainstorm-view', 'padding')}(D-16 映射值,非 24px)")

    ok(item, "[p1] #brainstorm-view h2 font-size", "14px", read_style(page, "#brainstorm-view h2", "font-size"))
    ok(item, "[p1] #brainstorm-view h2 color", "rgb(138,101,8)",
       read_style(page, "#brainstorm-view h2", "color"))
    ok(item, "[p1] #draft-view h2 font-size", "15px", read_style(page, "#draft-view h2", "font-size"))
    ok(item, "[p1] .panel-header h2 font-size", "14px", read_style(page, ".panel-header h2", "font-size"))
    ok(item, "[p1] .overlay-card h3 font-size", "16px", read_style(page, ".overlay-card h3", "font-size"))
    # `.markdown-body` 的规范消费者是 #draft-content(文档区正文渲染区)。
    # document.querySelector('.markdown-body') 会落到 #latest-check(它也带该类且自带
    # font-size 覆盖),那不是 `.markdown-body` 规则本身的探针。
    ok(item, "[p1] .markdown-body font-size(探针 #draft-content)", "14px",
       read_style(page, "#draft-content", "font-size"))
    # `.markdown-body code` 需要真实 <code> 元素:用应用自身的 renderMarkdown 渲染一个代码跨度
    # (真实渲染路径,零网络、零 AI 调用)。
    page.evaluate("""() => {
        const host = document.querySelector('#draft-content');
        host.innerHTML = '';
        host.appendChild(renderMarkdown('harness `probe` 探针'));
    }""")
    ok(item, "[p1] .markdown-body code font-size", "13px",
       read_style(page, "#draft-content code", "font-size"))

    ok(item, "[p1] #selection-menu z-index", "200", read_style(page, "#selection-menu", "z-index"))
    ok(item, "[p1] #state-badge z-index", "10", read_style(page, "#state-badge", "z-index"))
    ok(item, "[p1] #stream-banner z-index", "20", read_style(page, "#stream-banner", "z-index"))

    # 冻结轮(与第 2 项共用读取器)
    proj = make_fixture("p3", tmp_root)
    enter_project(page, proj)
    goto_frozen_round(page, item)
    check_frozen_marker(page, item, "[p3→round1]")

    # 归档态灰化
    proj = make_fixture("archive", tmp_root)
    enter_project(page, proj)
    ok(item, "[archive] #rounds-placeholder.archive-mode #round-doc opacity", "0.75",
       read_style(page, "#rounds-placeholder.archive-mode #round-doc", "opacity"))

    # 任意 button color(通用规则,探针同上)
    ok(item, "[archive] button color(通用规则,探针 #btn-enter)", "rgb(26,26,26)",
       read_style(page, "#btn-enter", "color"))

    # S-2 依赖:14px 必须作为一级字号档存活
    base = page.evaluate(
        "() => getComputedStyle(document.documentElement).getPropertyValue('--text-base').trim()"
    )
    ok_true(
        item,
        "S-2 DEPENDENCY --text-base 存活为 14px",
        base == "14px",
        "14px",
        base,
        "Phase 5 SC5 / Phase 6 SC5 的下游门依赖此档",
    )


# ---------------------------------------------------------------------------
# UAT 第 5 项 — Plan 03 的 10 项
# ---------------------------------------------------------------------------
def item5(page, tmp_root, ai_smoke):
    item = "5"
    print("\n=== UAT 5: DevTools computed-style 抽查 — Plan 03(10 项)===", flush=True)
    proj = make_fixture("p1", tmp_root)
    enter_project(page, proj)

    ok(item, "[p1] #ai-route-select border-top-color", "rgb(138,138,138)",
       read_style(page, "#ai-route-select", "border-top-color"))
    ok(item, "[p1] #ai-route-select background-color", "rgb(255,255,255)",
       read_style(page, "#ai-route-select", "background-color"))
    ok(item, "[p1] .hint color", "rgb(106,106,106)", read_style(page, ".hint", "color"))
    hint_bg = effective_bg(page, ".hint")
    ok(item, "[p1] .hint 实际背景", "rgb(250,250,250)", hint_bg,
       note=".hint 自身无背景,沿祖先链取到的实际底色")
    ok(item, "[p1] #stream-banner border-top-color", "rgb(138,101,8)",
       read_style(page, "#stream-banner", "border-top-color"))

    # ORDER 0.311 的可观察形态:.markdown-body 必须明显比 .hint 更深
    body_color = read_style(page, ".markdown-body", "color")
    hint_color = read_style(page, ".hint", "color")
    ok(item, "[p1] .markdown-body color", "rgb(26,26,26)", body_color)
    body_rgb, hint_rgb = parse_rgb(body_color), parse_rgb(hint_color)
    if body_rgb is None or hint_rgb is None:
        blocked(item, "[p1] .markdown-body 亮度显著低于 .hint", "<", "取色失败", "取色失败")
    else:
        lb, lh = relative_luminance(body_rgb), relative_luminance(hint_rgb)
        ok_true(
            item,
            "[p1] .markdown-body 亮度显著低于 .hint",
            lb < lh,
            "<",
            f"lum(.markdown-body)={lb:.4f} lum(.hint)={lh:.4f}",
            "ORDER 0.311 的可观察形态",
        )

    # 交互冒烟:「处理本轮批注」与「发送」
    if not ai_smoke:
        blocked(item, "[p3] 交互冒烟「处理本轮批注」", "无错误完成", "<未执行>",
                "需要真实 AI 调用,默认不执行;加 --ai-smoke 重跑")
        blocked(item, "[p3] 交互冒烟「发送」", "无错误完成", "<未执行>",
                "需要真实 AI 调用,默认不执行;加 --ai-smoke 重跑")
        return
    run_ai_smoke(page, item, tmp_root)


def run_ai_smoke(page, item, tmp_root):
    """真实 AI 调用冒烟(仅在临时副本上;有界超时 90s)。"""
    errors = []
    page.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
    page.on("response", lambda r: errors.append(f"http {r.status}: {r.url}") if r.status >= 400 else None)

    proj = make_fixture("p3", tmp_root)
    write_annotations(proj, 2, [
        {
            "id": "smoke-1",
            "quote": "建议进入授权环节",
            "before": "",
            "type": "comment",
            "note": "冒烟批注:请简短回应",
            "status": "pending",
            "answer": None,
            "created_at": "2026-09-19T00:00:00+00:00",
        }
    ])
    enter_project(page, proj)

    def wait_done(selector, deadline_s=90):
        deadline = time.time() + deadline_s
        while time.time() < deadline:
            disabled = page.evaluate(
                "(sel) => { const el = document.querySelector(sel); return el ? el.disabled : null; }",
                selector,
            )
            if disabled is False:
                return True
            time.sleep(1.0)
        return False

    # 1) 处理本轮批注
    errors.clear()
    if not page.evaluate("() => !!document.querySelector('#btn-process-round:not([disabled])')"):
        blocked(item, "[p3] 交互冒烟「处理本轮批注」", "无错误完成", "按钮不可点",
                "按钮在该样本状态下未点亮,无法发起")
    else:
        try:
            page.click("#btn-process-round", timeout=15000)
            done = wait_done("#btn-process-round")
            if not done:
                blocked(item, "[p3] 交互冒烟「处理本轮批注」", "无错误完成", "超时(90s)",
                        "claude CLI 不可用或超时")
            else:
                ok_true(item, "[p3] 交互冒烟「处理本轮批注」", not errors, "无 console/http 错误",
                        errors or "无错误", "; ".join(errors[:3]))
        except Exception as exc:
            blocked(item, "[p3] 交互冒烟「处理本轮批注」", "无错误完成", f"{type(exc).__name__}",
                    f"点击未能完成:{str(exc).splitlines()[0]}")

    # 诊断:阶段 3 的 #btn-send 在 AI 流之后是否仍可点(主区在阶段 3 切给批注流)
    clickable = page.evaluate("""() => {
        const el = document.querySelector('#btn-send');
        if (!el) return null;
        const r = el.getBoundingClientRect();
        const top = document.elementFromPoint(r.left + r.width/2, r.top + r.height/2);
        return { top: top ? (top.id || top.className || top.tagName) : null,
                 is_send: top === el || (top && el.contains(top)) };
    }""")
    info("[p3] #btn-send 可点性诊断(处理批注之后)",
         f"{clickable} —— 阶段 3 主区由批注流占据,会话流发送键被挤到不可点的位置;"
         "故「发送」冒烟改在 p12(会话流的自然活动面)执行")

    # 2) 发送 —— 会话流的自然活动面是阶段 1-2(阶段 3 主区切给批注流,见下方 INFO)
    errors.clear()
    proj2 = make_fixture("p12", tmp_root)
    enter_project(page, proj2)
    page.fill("#message-input", "冒烟:请用一句话确认你在线")
    try:
        page.click("#btn-send", timeout=15000)
        done = wait_done("#btn-send")
        if not done:
            blocked(item, "[p12] 交互冒烟「发送」", "无错误完成", "超时(90s)",
                    "claude CLI 不可用或超时")
        else:
            ok_true(item, "[p12] 交互冒烟「发送」", not errors, "无 console/http 错误",
                    errors or "无错误", "; ".join(errors[:3]))
    except Exception as exc:
        blocked(item, "[p12] 交互冒烟「发送」", "无错误完成", f"{type(exc).__name__}",
                f"点击未能完成:{str(exc).splitlines()[0]}")


# ---------------------------------------------------------------------------
# UAT 第 6 项 — CR-06 渲染结果
# ---------------------------------------------------------------------------
def item6(page, tmp_root):
    item = "6"
    print("\n=== UAT 6: CR-06 渲染结果 ===", flush=True)
    proj = make_fixture("p3", tmp_root)
    write_annotations(proj, 2, [
        {
            "id": "cr06-1",
            "quote": "建议进入授权环节",
            "before": "",
            "type": "comment",
            "note": "CR-06 探针:用户批注正文",
            "status": "answered",
            "answer": "CR-06 探针:AI 回应正文",
            "created_at": "2026-09-19T00:00:00+00:00",
        }
    ])
    enter_project(page, proj)

    present = page.evaluate("() => !!document.querySelector('#annotation-list .annotation-item')")
    if not present:
        blocked(item, "CR-06 批注条目渲染", "条目出现在 #annotations-panel", "<未渲染>",
                "批注条目未渲染(locate_quote 或列表渲染环节卡住)")
        return
    # 展开 <details>(点 summary)
    opened = page.evaluate("""() => {
        const d = document.querySelector('#annotation-list .annotation-answer');
        if (!d) return false;
        const s = d.querySelector('summary');
        if (s) s.click();
        return d.open;
    }""")
    page.wait_for_timeout(300)
    info("item6 details", f"opened={opened}")

    muted = resolve_color(page, "--color-text-muted")
    info("item6 --color-text-muted 解析值", muted)
    note_color = read_style(page, ".annotation-note", "color")
    body_color = read_style(page, ".annotation-answer-body", "color")
    if muted is None or note_color is None or body_color is None:
        blocked(item, "CR-06 用户批注以 --color-text-muted 渲染", muted, note_color,
                "元素缺失或令牌解析失败")
        blocked(item, "CR-06 AI 回应正文以 --color-text-muted 渲染", muted, body_color,
                "元素缺失或令牌解析失败")
        return
    ok(item, "CR-06 用户批注 .annotation-note color", muted, note_color)
    ok(item, "CR-06 AI 回应正文 .annotation-answer-body color", muted, body_color)


# ---------------------------------------------------------------------------
# harness 自检切片(--item smoke)
# ---------------------------------------------------------------------------
def item_smoke(page, tmp_root):
    item = "smoke"
    print("\n=== SMOKE: 端到端薄切片(样本 → 应用 → 系统 Chrome → computed style)===", flush=True)
    proj = make_fixture("p3", tmp_root)
    enter_project(page, proj)
    info("smoke 样本", f"p3 → {proj}")
    ok_true(item, "smoke #state-badge 可见", read_style(page, "#state-badge", "display") != "none",
            "display!=none", read_style(page, "#state-badge", "display"))
    # 切片证据:消费者 → 令牌的接线(读到的 computed 值必须等于令牌解析值)
    color_token = resolve_color(page, "--color-text-info")
    bg_token = resolve_color(page, "--color-surface-info")
    info("smoke 令牌解析", f"--color-text-info={color_token} --color-surface-info={bg_token}")
    ok(item, "smoke #state-badge color == var(--color-text-info)",
       color_token, read_style(page, "#state-badge", "color"))
    ok(item, "smoke #state-badge background == var(--color-surface-info)",
       bg_token, read_style(page, "#state-badge", "background-color"))
    # 透明记录:UAT/PLAN 里写的字面值 rgb(31,99,189) 是 260918-qrq 换肤前的 --blue-700;
    # 该字面值由 UAT 第 3 项逐字断言,故此处只作 INFO,不参与本切片的判定。
    info("smoke UAT 字面值对照",
         "#state-badge color 的 UAT 字面期望 rgb(31,99,189) 实测="
         f"{read_style(page, '#state-badge', 'color')} —— 差异由 260918-qrq 令牌值换肤引入,"
         "该字面断言在第 3 项逐字执行")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def parse_args():
    ap = argparse.ArgumentParser(add_help=True, description="idi-04 UAT browser harness")
    ap.add_argument("--item", action="append", default=None,
                    help="只跑指定项:smoke / 1 / 2 / 3 / 4 / 5 / 6(可重复,或逗号分隔)")
    ap.add_argument("--ai-smoke", action="store_true",
                    help="第 5 项额外真跑两次 AI 交互冒烟(会产生真实 AI 调用与计费)")
    ap.add_argument("--keep", action="store_true", help="保留临时工作目录供排查")
    ap.add_argument("--headed", action="store_true", help="有头模式(默认无头;--browser chrome 恒有头)")
    ap.add_argument("--browser", choices=["bundled", "chrome"], default="bundled",
                    help="bundled=Playwright 自带 chromium(revision 1243,已缓存,arm64 原生,零下载,可无头);"
                         "chrome=系统 Google Chrome(本机 x86_64 venv 下无头会挂死,故强制有头)")
    return ap.parse_args()


def normalize_items(raw):
    if not raw:
        return ["1", "2", "3", "4", "5", "6"]
    out = []
    for chunk in raw:
        for piece in chunk.split(","):
            piece = piece.strip()
            if piece:
                out.append(piece)
    return out


def main():
    args = parse_args()
    items = normalize_items(args.item)
    known = {"smoke", "1", "2", "3", "4", "5", "6"}
    bad = [i for i in items if i not in known]
    if bad:
        raise SystemExit(f"ERROR: 未知项 {bad}(可用:{sorted(known)})")

    server = ensure_server()
    tmp_root = Path(tempfile.mkdtemp(prefix="idi-05-uat-"))
    info("tmp", f"临时工作目录 {tmp_root}(--keep 可保留)")
    pw = browser = None
    try:
        from playwright.sync_api import sync_playwright

        pw = sync_playwright().start()
        if args.browser == "chrome":
            # 系统 Chrome 在本机(x86_64 venv → Rosetta)无头会挂死,故强制有头
            info("browser", "channel='chrome'(系统 Google Chrome,有头)")
            browser = pw.chromium.launch(channel="chrome", headless=False)
        else:
            info("browser", "Playwright 自带 chromium(revision 1243,已缓存,零下载)")
            browser = pw.chromium.launch(headless=not args.headed)
        info("browser.version", browser.version)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.set_default_timeout(20000)

        if "smoke" in items:
            item_smoke(page, tmp_root)
        if "1" in items:
            item1(page, tmp_root)
        if "2" in items:
            item2(page, tmp_root)
        if "3" in items:
            item3(page, tmp_root)
        if "4" in items:
            item4(page, tmp_root)
        if "5" in items:
            item5(page, tmp_root, args.ai_smoke)
        if "6" in items:
            item6(page, tmp_root)
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
            info("server", "已关闭本次自起的 uvicorn")
        if not args.keep:
            shutil.rmtree(tmp_root, ignore_errors=True)
        else:
            info("tmp", f"保留:{tmp_root}")

    # ---- 汇总 ----
    print("\n=== 逐项结论 ===", flush=True)
    verdicts = {}
    for i in items:
        v = item_verdict(i)
        verdicts[i] = v
        n = len([r for r in ROWS if r["item"] == i])
        fails = len([r for r in ROWS if r["item"] == i and r["verdict"] == "FAIL"])
        blocks = len([r for r in ROWS if r["item"] == i and r["verdict"] == "BLOCKED"])
        print(f"item {i}: {v.upper()}  ({n} 条断言,{fails} FAIL,{blocks} BLOCKED)", flush=True)

    any_fail = any(v == "fail" for v in verdicts.values())
    any_blocked = any(v == "blocked" for v in verdicts.values())
    code = 1 if any_fail else (2 if any_blocked else 0)
    print(f"\nexit={code}  (0=全 pass,1=有 fail,2=有 blocked)", flush=True)
    return code


if __name__ == "__main__":
    sys.exit(main())
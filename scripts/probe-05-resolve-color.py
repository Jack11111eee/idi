#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe-05-resolve-color.py — CR-01 的**变异证明**,不是门。

它不进四条守卫命令契约(`check-01`…`check-04`),不被任何门禁 / CI 调用,
`scripts/check-05-ui-uat.py` 也不引用它。存在的唯一目的:把「修复前 PASS /
修复后 BLOCKED」这一对照变成可复跑的证据 —— 变异测试是唯一能证明守卫真的
会失败的手段。

做法:起本地应用 → 在浏览器侧拦截 `/style.css` 的响应,**只删掉
`--color-text-muted:` 那一行声明**(`route.fetch()` → 逐行过滤 →
`route.fulfill(response=resp, body=mutated)`)。变异只活在被拦截的那份响应里,
`frontend/style.css` 在磁盘上逐字节不变。

同一份被变异的副本上跑同一条断言两次:
  - **修复前形态**(`PREFIX_PROBE_JS`,引自 `68309d0`):探针 div 的
    `color: var(--t)` 在 computed-value 阶段失效 → 继承 `body` 的 color;
    真实消费者 `.hint` 用的是同一个 `var(--t)`,两侧退化成同一个继承值
    → 断言**恒真**,记 PASS。**这就是缺陷的实证。**
  - **修复后形态**(harness 的 `resolve_color`):先确认令牌确有声明,未声明
    即返回 `None` → `ok()` 记 BLOCKED。**这就是修复的实证。**

未变异的对照(PASS B)断言同一条断言仍记 PASS —— 没有它,一个永远返回
`None` 的 `resolve_color` 也会让本探针通过。

不用 `sed`:本机是 darwin,BSD `sed` 的 `0,/re/` 地址会**静默不替换**,那会让
变异变成空转、整条证明失去意义(plan 02 已实测并写成纪律)。

运行方式
    .venv/bin/python scripts/probe-05-resolve-color.py
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

# ---------------------------------------------------------------------------
# 反事实常量:修复前(68309d0)resolve_color 的探针体
# ---------------------------------------------------------------------------
# 它为什么存在:它是「没有前置分支时会算出什么」的反事实。没有它就没有对照 ——
# 也就无法证明「修复前会记 PASS」,整条变异证明退化成自陈。
PREFIX_PROBE_JS = """(t) => {
    const p = document.createElement('div');
    p.style.color = `var(${t})`;
    document.body.appendChild(p);
    const c = getComputedStyle(p).color;
    p.remove();
    return c;
}"""

TOKEN = "--color-text-muted"
CONSUMER_SELECTOR = ".hint"


def load_harness():
    """按路径导入 harness(文件名带连字符,不能走普通 import)。

    该文件末尾是 `if __name__ == "__main__": sys.exit(main())`,导入无副作用。
    复用它的 helper 而不是复制实现 —— 否则探针测的就不是真实 helper。
    """
    spec = importlib.util.spec_from_file_location("check05_ui_uat", HARNESS_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def require(cond, msg):
    if not cond:
        print(f"PROBE FAILED: {msg}", file=sys.stderr, flush=True)
        raise SystemExit(1)


def make_mutated_handler(h5, seen):
    """返回一个 `/style.css` 路由 handler:删掉 TOKEN 的声明行后放行。

    变异**不落盘** —— 只构造一份被拦截响应的 body。故真实样式表逐字节不变。
    """

    def handler(route):
        resp = route.fetch()
        original = resp.body().decode("utf-8")
        lines = original.splitlines(keepends=True)
        mutated = "".join(ln for ln in lines if f"{TOKEN}:" not in ln)
        # 空转变异的防线:变异必须真的发生。
        seen["original"] = original
        seen["mutated"] = mutated
        route.fulfill(response=resp, body=mutated)

    return handler


def main():
    h5 = load_harness()
    seen = {}
    server = h5.ensure_server()
    tmp_root = Path(tempfile.mkdtemp(prefix="idi-05-probe-"))
    pw = browser = None
    failures = []
    try:
        from playwright.sync_api import sync_playwright

        pw = sync_playwright().start()
        # 与 harness 默认的 --browser bundled 一致,不引入新的浏览器选择逻辑。
        browser = pw.chromium.launch(headless=True)

        # ---------------- PASS A:变异副本 ----------------
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.set_default_timeout(20000)
        page.route("**/style.css", make_mutated_handler(h5, seen))
        proj = h5.make_fixture("p1", tmp_root)
        h5.enter_project(page, proj)

        # 变异真的发生了吗?(否则整条证明是空转)
        mutation_applied = bool(seen.get("mutated")) and seen["mutated"] != seen.get(
            "original"
        )
        require(mutation_applied, "变异未发生:mutated 与原始 body 相等")
        require(
            f"{TOKEN}:" not in seen["mutated"],
            f"变异未发生:mutated 仍含 {TOKEN}: 声明",
        )
        print("PROBE mutation-applied=yes", flush=True)

        # 1. 真实消费者的 computed 值
        hint_computed = h5.read_style(page, CONSUMER_SELECTOR, "color")

        # 2. 修复前形态:探针继承 body 的 color
        pre_fix_expected = page.evaluate(PREFIX_PROBE_JS, TOKEN)
        require(
            pre_fix_expected is not None,
            "修复前探针返回 None —— 反事实不成立",
        )
        require(
            h5.norm(pre_fix_expected) == h5.norm(hint_computed),
            f"修复前探针 {pre_fix_expected} 与消费者 {hint_computed} 不相等 —— "
            "两侧未退化成同一个继承值,缺陷机制未被复现",
        )

        # 3. 缺陷的实证:这条断言在修复前记 PASS
        h5.ok(
            "probe",
            f"[mutated] {CONSUMER_SELECTOR} color == var({TOKEN}) (pre-fix)",
            pre_fix_expected,
            hint_computed,
        )
        prefix_verdict = h5.ROWS[-1]["verdict"]
        require(
            prefix_verdict == "PASS",
            f"修复前判定为 {prefix_verdict},期望 PASS —— 缺陷未被实证",
        )
        print("PROBE mutated-prefix-verdict=PASS", flush=True)

        # 4. 修复后形态:未声明令牌返回 None
        post_fix_expected = h5.resolve_color(page, TOKEN)
        require(
            post_fix_expected is None,
            f"修复后 resolve_color 返回 {post_fix_expected!r},期望 None —— "
            "未声明分支缺失",
        )

        # 5. 修复的实证:这条断言在修复后记 BLOCKED
        h5.ok(
            "probe",
            f"[mutated] {CONSUMER_SELECTOR} color == var({TOKEN}) (post-fix)",
            post_fix_expected,
            hint_computed,
        )
        postfix_verdict = h5.ROWS[-1]["verdict"]
        require(
            postfix_verdict == "BLOCKED",
            f"修复后判定为 {postfix_verdict},期望 BLOCKED —— 修复未被实证",
        )
        print("PROBE mutated-postfix-verdict=BLOCKED", flush=True)

        # 四值对照表(供 SUMMARY 逐字抄录)
        print(
            "PROBE contrast-table: "
            f"pre_fix_expected={pre_fix_expected} | "
            f"hint_computed={hint_computed} | "
            f"pre-fix verdict={prefix_verdict} | "
            f"post-fix verdict={postfix_verdict}",
            flush=True,
        )
        ctx.close()

        # ---------------- PASS B:未变异的对照 ----------------
        ctx2 = browser.new_context(viewport={"width": 1440, "height": 900})
        page2 = ctx2.new_page()
        page2.set_default_timeout(20000)
        proj2 = h5.make_fixture("p1", tmp_root)
        h5.enter_project(page2, proj2)

        control_expected = h5.resolve_color(page2, TOKEN)
        control_actual = h5.read_style(page2, CONSUMER_SELECTOR, "color")
        require(
            control_expected is not None,
            "对照支:未变异的世界里 resolve_color 返回 None —— 修复把断言变成恒 BLOCKED",
        )
        require(
            h5.norm(control_expected) == h5.norm(control_actual),
            f"对照支:resolve_color {control_expected} != 消费者 {control_actual}",
        )
        h5.ok(
            "probe",
            f"[control] {CONSUMER_SELECTOR} color == var({TOKEN})",
            control_expected,
            control_actual,
        )
        control_verdict = h5.ROWS[-1]["verdict"]
        require(
            control_verdict == "PASS",
            f"对照支判定为 {control_verdict},期望 PASS —— 修复可能把断言变成恒 BLOCKED",
        )
        print("PROBE control-verdict=PASS", flush=True)
        ctx2.close()
    except SystemExit as e:
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
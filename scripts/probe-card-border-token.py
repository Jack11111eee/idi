#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一次性探针:卡片容器的边界色是 `--color-border`(gray-7)还是 `--color-border-subtle`(gray-6)。

为什么需要它 —— 本仓库既有的六条门**没有一条**读卡片容器的 `border-*-color`:
  - check-01  只数围栏外的裸 hex 与 tier-1 原语引用
  - check-02  只算 PAIR 清单上的对比度比值(两个 border 令牌都不在清单里)
  - check-03  只数 `.hidden {` 规则条数
  - check-04  只数 `!important;` 声明条数
  - check-05  断言既有 UAT 项(令牌接线 / 几何 / 焦点环),对边界色恒真
  - check-09  对卡片容器读的是 background-color / border-*-radius / border-*-width /
              border-*-style / box-shadow —— **没有任何一条读 border-*-color**
故「边界色换到哪个令牌」这条缝在本探针之前零运行时覆盖。本探针补的正是这条缝。

这是一次性探针,**不是门**:不进任何 check 的调用链、不被 CI 调用、不被任何计划或
门引用。仓库对此有现成先例 —— `scripts/probe-menu-modal-reachability.py` 是同形的
一次性探针。它被否决的替代方案是「往 check-09 的 c1 里加一条边界色断言」:那是改门
语义,而本次的裁定是纯值级修正(零处门改动)。

判别控制 —— **改动前的状态本身就是本探针的失败方向**。改动前五条卡片规则的
`border-top-color` 实测是 `rgb(217, 217, 217)`(= `--color-border-subtle`),正是
本探针的 FAIL 方向;故 RED 输出即是「它区分得开「改了」与「没改」」的实证。
另有一条防恒真的前置判据(① 令牌可区分):若两个令牌恰好取同一个值,②③ 两条会在
两侧相等时静默恒绿 —— 那正是本仓库反复付过代价的假绿形态。

不写盘:fixture 落在临时目录,浏览器在 finally 内关闭,仓库树零改动。
"""
import importlib.util
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "check05_ui_uat", ROOT / "scripts" / "check-05-ui-uat.py")
c05 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c05)

# 五个卡片容器:左栏四个 section + 右栏文档面板(check-09 c1/c2 用的同一批)。
CARD_SELECTORS = ["#session-panel", "#annotations-panel", "#checks-panel",
                  "#ai-panel", "#doc-panel"]

# 四个非卡片消费者(改动面严格是两处,不是六处)。
NON_CARD_SELECTORS = [".event-list", "#latest-check", ".annotation-item",
                      ".badge-answered"]

# 对照元素的可读下限:少于 2 个即证明力不足,记 BLOCKED 而非静默跳过。
MIN_NON_CARD_READABLE = 2


def main():
    server = c05.ensure_server()
    tmp_root = Path(tempfile.mkdtemp(prefix="probe-card-border-"))
    pw = browser = None
    try:
        from playwright.sync_api import sync_playwright

        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.set_default_timeout(20000)

        # p1 是 check-09 c1/c2 用的同一样本(四个左栏 section 与 #doc-panel 都在)。
        # 浏览器固定走 Playwright 自带 chromium + 无头(与 check-09 同款):
        # 本机 channel="chrome" + headless 会 CDP 挂死,是既有实测结论。
        proj = c05.make_fixture("p1", tmp_root)
        c05.enter_project(page, proj)
        page.wait_for_timeout(400)

        fails = 0
        blocked = False

        # ---- ① 令牌解析 + 可区分性(防恒真)------------------------------
        border = c05.resolve_color(page, "--color-border")
        subtle = c05.resolve_color(page, "--color-border-subtle")
        print(f"INFO 令牌解析: --color-border={border} "
              f"--color-border-subtle={subtle}")
        if border is None or subtle is None:
            print(f"FAIL 令牌可区分: 令牌未声明或解析失败"
                  f"(--color-border={border} --color-border-subtle={subtle})")
            fails += 1
        elif c05.norm(border) == c05.norm(subtle):
            print(f"FAIL 令牌可区分: --color-border == --color-border-subtle"
                  f"({border})(两侧相等 ⇒ 下一条判据恒真)")
            fails += 1
        else:
            print(f"PASS 令牌可区分: --color-border != --color-border-subtle"
                  f"({border} != {subtle})")

        # ---- ② 卡片边界(主判据)------------------------------------------
        for sel in CARD_SELECTORS:
            actual = c05.read_style(page, sel, "border-top-color")
            if actual is None:
                print(f"FAIL 卡片边界 {sel}: 元素不存在")
                blocked = True
                continue
            if c05.norm(actual) == c05.norm(border):
                print(f"PASS 卡片边界 {sel}: expected={border} actual={actual}")
            else:
                print(f"FAIL 卡片边界 {sel}: expected={border} actual={actual}")
                fails += 1

        # ---- ③ 非卡片对照(证明改动面严格是两处)--------------------------
        readable = 0
        for sel in NON_CARD_SELECTORS:
            actual = c05.read_style(page, sel, "border-top-color")
            if actual is None:
                print(f"INFO 非卡片边界对照 {sel}: p1 样本里不存在 —— 不计入")
                continue
            readable += 1
            if c05.norm(actual) == c05.norm(subtle):
                print(f"PASS 非卡片边界对照 {sel}: expected={subtle} actual={actual}")
            else:
                print(f"FAIL 非卡片边界对照 {sel}: expected={subtle} actual={actual}")
                fails += 1
        if readable < MIN_NON_CARD_READABLE:
            print(f"FAIL 非卡片边界对照: p1 样本里只有 {readable} 个可读,"
                  f"对照不足以证明改动面")
            blocked = True

        # ---- ④ 结果行 ----------------------------------------------------
        print()
        if blocked:
            print("PROBE RESULT: BLOCKED(exit=2)")
            return 2
        if fails:
            print("PROBE RESULT: FAIL(exit=1)")
            return 1
        print("PROBE RESULT: PASS(exit=0)")
        return 0
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


if __name__ == "__main__":
    sys.exit(main())

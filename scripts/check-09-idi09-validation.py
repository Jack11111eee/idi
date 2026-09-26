#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check-09-idi09-validation.py — Phase 9「卡片容器化与页面底色下沉」的运行时门。

为什么另开一个文件
    既有五条门里**没有任何一条**断言五个容器的 `background` / `border` /
    `border-radius` / `box-shadow`:
      - `check-01-token-conformance.sh`  只数围栏外的裸 hex 与 tier-1 原语引用
      - `check-02-contrast.py`           只算 PAIR 清单上的对比度比值
      - `check-03-hidden-uniqueness.sh`  只数 `.hidden {` 规则条数
      - `check-04-important-count.sh`    只数 `!important;` 声明条数
      - `check-05-ui-uat.py`             断言的是既有 UAT 项(令牌接线 / 几何 / 焦点环),
                                         对「容器是不是卡片」恒真
    需求 CARD-01 / CARD-02 / CARD-03 的渲染判据在本文件之前**零自动化覆盖** ——
    本文件补的正是这条缝。全部断言是真实浏览器里的 `getComputedStyle` 读数,
    不是源码文本匹配:卡片是**画出来**的,文本里写着 `background` 不等于它真的生效。

与 check-05 的关系
    复用 check-05 的模块级设施(服务生命周期 `ensure_server` / fixture 隔离
    `make_fixture` / `enter_project` / 断言记录器 `ok` / `ok_true` / `blocked` /
    `info` / 令牌解析 `resolve_color` / `resolve_token` / 读数器 `read_style` /
    样本清单 `STATES`),不重复实现,也不改动 check-05 一行(本阶段对 check-05 的
    唯一改动是 `.hint` 断言的期望侧重新登记,与本文件的设施无关)。

运行方式
    .venv/bin/python scripts/check-09-idi09-validation.py --item c1
    .venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2
    .venv/bin/python scripts/check-09-idi09-validation.py --screenshot .planning/phases/idi-09-card-containers/screenshots
    .venv/bin/python scripts/check-09-idi09-validation.py --keep

退出码语义(与 check-05 一致)
    0 = 全 pass;1 = 至少一条 FAIL;2 = 无 FAIL 但至少一条 BLOCKED

断言与需求的映射
    c1 → VIS-01 / VIS-02 / CARD-01   左栏 4 个 section 的卡片语言(令牌 + 计算读数)
    c2 → CARD-02 / REG-01            #doc-panel 的卡片语言 + #doc-panel-header 对照组
    c4 → CARD-03                    密度几何(D-9-2):#main-pane gap 12px / .panel-body
                                     padding 16px,外加 #doc-panel-body 与 .panel-header
                                     两条对照组(证明改动没有漏出裁定范围)
    shot                             逐样本整窗截图,供用户评审(不参与卡片判据)

浏览器路线(实测结论,不是偏好)
    固定走 Playwright 自带 chromium + 无头(与 check-06 同款)。本机 `channel="chrome"`
    + headless 会 CDP 挂死(见 check-05 文件头的实测记录),故本文件不提供 `--browser`。
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import shutil
import struct
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK05 = ROOT / "scripts" / "check-05-ui-uat.py"


def load_check05():
    """把 check-05 当模块加载(文件名含连字符,不能用 import)。"""
    spec = importlib.util.spec_from_file_location("check05_ui_uat", CHECK05)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


c05 = load_check05()
ok = c05.ok
ok_true = c05.ok_true
blocked = c05.blocked
info = c05.info
read_style = c05.read_style
resolve_color = c05.resolve_color
resolve_token = c05.resolve_token

# 左栏 4 个 section(index.html 的 main#main-pane 的 4 个直接子 section)。
LEFT_SECTIONS = ["#session-panel", "#annotations-panel", "#checks-panel", "#ai-panel"]

# 用户裁定值(D-9-3)。字面量写在这里,是因为本断言的用途正是「运行时读到的值
# 等于用户裁定的那个值」—— 若两侧都从同一个令牌解析,改坏令牌值也照样 PASS。
SHADOW_CARD_LITERAL = "0 1px 2px rgba(0, 0, 0, 0.04)"
SHADOW_CARD_COLOR = "rgba(0, 0, 0, 0.04)"
CARD_WHITE = "rgb(255, 255, 255)"

_SHADOW_COLOR_RE = re.compile(r"rgba?\([^)]*\)")


def shadow_lengths(raw):
    """把 computed box-shadow 去掉颜色后拆成分量;none / 取不到返回 None。

    Chrome 的 computed 序列化把颜色写在最前(如
    `rgba(0, 0, 0, 0.04) 0px 1px 2px 0px`),故去掉颜色子串后剩下的就是
    `[offset-x, offset-y, blur, spread]`。offset-x 是零位移判据的读数。
    """
    if not raw or not isinstance(raw, str) or raw.strip() == "none":
        return None
    parts = _SHADOW_COLOR_RE.sub(" ", raw).split()
    return parts or None


def png_size(path):
    """读 PNG 的 IHDR 取 (width, height);不是 PNG 或读不到返回 (None, None)。"""
    try:
        with open(path, "rb") as handle:
            head = handle.read(24)
    except OSError:
        return (None, None)
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        return (None, None)
    return struct.unpack(">II", head[16:24])


# ---------------------------------------------------------------------------
# c1 — 左栏 4 个 section 的卡片语言(VIS-01 / VIS-02 / CARD-01)
# ---------------------------------------------------------------------------
# 样本 p1:4 个 section 在 p1 下全部存在于 DOM 中。`getComputedStyle` 对
# `display: none` 的元素同样返回解析值,故无需为每个面板切样本 —— 与 check-05
# item 9 读 `#annotation-list` 同一依据。
def c1(page, tmp_root):
    item = "c1"
    print("\n=== c1: 左栏 4 个 section 的卡片语言(VIS-01 / VIS-02 / CARD-01)===", flush=True)
    proj = c05.make_fixture("p1", tmp_root)
    c05.enter_project(page, proj)

    card = resolve_color(page, "--color-surface-card")
    radius = resolve_token(page, "--radius-md")
    shadow_token = resolve_token(page, "--shadow-card")
    info("c1 令牌解析",
         f"--color-surface-card={card} --radius-md={radius} --shadow-card={shadow_token}")
    ok(item, "c1 [令牌] --color-surface-card 解析为白", CARD_WHITE, card,
       note="令牌级断言:两侧都写死,防止「令牌被改坏而消费者仍接线」时假绿")
    ok(item, "c1 [令牌] --shadow-card == 用户裁定值(D-9-3)", SHADOW_CARD_LITERAL,
       shadow_token, note="令牌级断言:期望侧是字面量,不是同一个令牌")

    for sel in LEFT_SECTIONS:
        bg = read_style(page, sel, "background-color")
        tl_radius = read_style(page, sel, "border-top-left-radius")
        bw = read_style(page, sel, "border-top-width")
        bs = read_style(page, sel, "border-top-style")
        shadow = read_style(page, sel, "box-shadow")
        info(f"c1 {sel} 原始读数",
             f"background-color={bg} border-top-left-radius={tl_radius} "
             f"border-top={bw} {bs} box-shadow={shadow}")
        if None in (bg, tl_radius, bw, bs, shadow):
            blocked(item, f"[p1] {sel} 五个读数可读", "5 个非 None 读数",
                    f"{bg} / {tl_radius} / {bw} / {bs} / {shadow}", "元素/选择器不存在")
            continue
        ok(item, f"[p1] {sel} 计算底色 == var(--color-surface-card)", card, bg,
           note="HEAD 上是完全透明(rgba(0, 0, 0, 0)),卡片化后必须是白")
        ok(item, f"[p1] {sel} 计算 border-top-left-radius == var(--radius-md)",
           radius, tl_radius, note="证明圆角取自既有刻度,零新增圆角值(VIS-02)")
        ok(item, f"[p1] {sel} 计算 border-top-width == 1px", "1px", bw)
        ok(item, f"[p1] {sel} 计算 border-top-style == solid", "solid", bs)
        ok_true(item, f"[p1] {sel} box-shadow 非 none 且含卡片阴影",
                shadow != "none" and c05.norm(SHADOW_CARD_COLOR) in c05.norm(shadow),
                f"非 none 且含 {SHADOW_CARD_COLOR}", str(shadow))
        lengths = shadow_lengths(shadow)
        ok_true(item, f"[p1] {sel} box-shadow 水平偏移为 0px(零位移)",
                bool(lengths) and lengths[0] == "0px", "offset-x == 0px",
                f"分量={lengths}")


# ---------------------------------------------------------------------------
# c2 — #doc-panel 的卡片语言 + #doc-panel-header 对照组(CARD-02 / REG-01)
# ---------------------------------------------------------------------------
# 同族判据:右栏与左栏用**同一组**令牌(底色 / 边界 / 圆角 / 阴影),故期望侧一律取
# 运行时解析的令牌值 —— 与 c1 的对照正是「两栏取同一批令牌」这件事本身。
def c2(page, tmp_root):
    item = "c2"
    print("\n=== c2: #doc-panel 卡片语言 + #doc-panel-header 对照组(CARD-02 / REG-01)===",
          flush=True)
    proj = c05.make_fixture("p1", tmp_root)
    c05.enter_project(page, proj)

    card = resolve_color(page, "--color-surface-card")
    radius = resolve_token(page, "--radius-md")
    info("c2 令牌解析", f"--color-surface-card={card} --radius-md={radius}")

    sides = ("top", "right", "bottom", "left")
    bg = read_style(page, "#doc-panel", "background-color")
    radius_tl = read_style(page, "#doc-panel", "border-top-left-radius")
    shadow = read_style(page, "#doc-panel", "box-shadow")
    overflow_y = read_style(page, "#doc-panel", "overflow-y")
    widths = {s: read_style(page, "#doc-panel", f"border-{s}-width") for s in sides}
    styles = {s: read_style(page, "#doc-panel", f"border-{s}-style") for s in sides}
    info("c2 #doc-panel 原始读数",
         f"background-color={bg} border-top-left-radius={radius_tl} "
         f"box-shadow={shadow} overflow-y={overflow_y}")
    info("c2 #doc-panel 四条边框宽度原始读数",
         " / ".join(f"{s}={widths[s]}" for s in sides))
    info("c2 #doc-panel 四条边框样式原始读数",
         " / ".join(f"{s}={styles[s]}" for s in sides))

    if None in (bg, radius_tl, shadow, overflow_y) or None in widths.values():
        blocked(item, "[p1] #doc-panel 的读数可读", "非 None 的读数",
                f"{bg} / {radius_tl} / {shadow} / {overflow_y}", "元素/选择器不存在")
    else:
        ok(item, "[p1] #doc-panel 计算底色 == var(--color-surface-card)", card, bg,
           note="HEAD 上是 gray-2(比页面更暗,读作凹陷),卡片化后是白卡片")
        ok(item, "[p1] #doc-panel 计算 border-top-left-radius == var(--radius-md)",
           radius, radius_tl, note="与左栏同族,圆角取自同一既有刻度")
        for s in sides:
            ok(item, f"[p1] #doc-panel 计算 border-{s}-width == 1px", "1px", widths[s],
               note="四边同族边界,取代原 border-left 的单边凹陷读感")
            ok(item, f"[p1] #doc-panel 计算 border-{s}-style == solid", "solid",
               styles[s])
        ok_true(item, "[p1] #doc-panel box-shadow 非 none 且含卡片阴影",
                shadow != "none" and c05.norm(SHADOW_CARD_COLOR) in c05.norm(shadow),
                f"非 none 且含 {SHADOW_CARD_COLOR}", str(shadow))
        # 承重事实,必须正面断言:它是右列的滚动者,L-1 的 sticky 表头依赖它仍是最近的
        # 可滚祖先。删掉它不会让任何颜色断言变红,所以这里不靠颜色门兜底。
        ok(item, "[p1] #doc-panel 计算 overflow-y == auto(承重的滚动契约)", "auto",
           overflow_y, note="L-1 的 sticky 表头依赖 #doc-panel 仍是最近的可滚祖先")

    header_shadow = read_style(page, "#doc-panel-header", "box-shadow")
    info("c2 #doc-panel-header 原始读数", f"box-shadow={header_shadow}")
    # 对照组:阴影属于卡片容器,不属于 sticky 表头 —— 与 check-06 g6 的既有对照组同口径
    # (那里断言 #ai-panel-header / #doc-panel-header 的 box-shadow 恒 none)。
    ok(item, "[p1] #doc-panel-header 计算 box-shadow == none(对照组)", "none",
       header_shadow, note="阴影画在卡片上,不在表头上")


# ---------------------------------------------------------------------------
# c4 — 密度几何(D-9-2):卡片间距 12px / 左栏面板内边距 16px
# ---------------------------------------------------------------------------
# 判据是**计算几何读数**,不是源码文本匹配 —— 与 check-05 的 padding 断言同口径,
# 期望侧一律写字面量 px 字符串(不是令牌名:两侧都从同一个令牌解析会让「令牌改坏
# 但声明仍接线」假绿)。
#
# 两条对照组是**回归护栏**,不是重复劳动:
#   · #doc-panel-body —— 证明密度改动没有漏到右栏。它的 padding 由 check-05 item 4
#     独立断言(`32px 40px`);这里重列一遍是为了让「有人把 .panel-body 的选择器扩成
#     同时命中 #doc-panel-body」这件事在本文件里也能当场变红,而不必等 check-05。
#   · .panel-header padding-top —— 表头是 36px 固定高的 chrome 条,它的内边距**不在**
#     D-9-2 的裁定范围内,故刻意未随卡片内边距一起改。
def c4(page, tmp_root):
    item = "c4"
    print("\n=== c4: 密度几何(D-9-2)—— 间距 12px / 面板内边距 16px ===", flush=True)
    proj = c05.make_fixture("p1", tmp_root)
    c05.enter_project(page, proj)

    # 文档序第一个 .panel-body 是 #session-panel 内的那一个(p1 下它在 DOM 里;
    # getComputedStyle 对 display:none 的元素同样返回解析值)。
    readings = [
        ("#main-pane", "gap", "12px", "卡片间距(D-9-2 紧凑档;HEAD 是 6px)"),
        (".panel-body", "padding", "16px", "左栏 4 个面板的正文内边距(D-9-2 紧凑档;HEAD 是 10px)"),
        ("#doc-panel-body", "padding", "32px 40px", "对照组:右栏阅读列内边距未受影响"),
        (".panel-header", "padding-top", "6px", "对照组:表头 chrome 条的内边距未随卡片内边距改动"),
    ]
    for sel, prop, expected, note in readings:
        actual = read_style(page, sel, prop)
        info(f"c4 {sel} {prop} 原始读数", f"{actual}")
        if actual is None:
            blocked(item, f"[p1] {sel} 计算 {prop} == {expected}", expected,
                    "<MISSING>", "元素/选择器不存在")
            continue
        ok(item, f"[p1] {sel} 计算 {prop} == {expected}", expected, actual, note=note)


# ---------------------------------------------------------------------------
# shot — 逐样本整窗截图(供用户评审;不参与卡片判据)
# ---------------------------------------------------------------------------
def run_screenshots(page, out_dir, tmp_root):
    item = "shot"
    print("\n=== shot: 逐样本整窗截图(1440x900)===", flush=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    made = []
    for state in c05.STATES:
        proj = c05.make_fixture(state, tmp_root)
        c05.enter_project(page, proj)
        path = out_dir / f"{state}.png"
        page.screenshot(path=str(path))
        width, height = png_size(path)
        made.append(state)
        info(f"shot {state}", f"{path} {width}x{height}")
        ok_true(item, f"shot [{state}] 截图落盘且为 1440x900",
                width == 1440 and height == 900, "1440x900", f"{width}x{height}")
    ok(item, "shot 样本清单逐项一一对应(无缺项、无多余样本)",
       list(c05.STATES), made, note=f"来源 check-05 的 STATES={c05.STATES}")
    pngs = sorted(p.name for p in out_dir.glob("*.png"))
    ok(item, "shot 输出目录恰含 5 个 PNG",
       sorted(f"{s}.png" for s in c05.STATES), pngs)


ITEMS = {"c1": c1, "c2": c2, "c4": c4}


def parse_args():
    ap = argparse.ArgumentParser(add_help=True, description="Phase 9 卡片语言的运行时门")
    ap.add_argument("--item", action="append", default=None,
                    help="只跑指定项:c1 / c2 / c4(可重复,或逗号分隔)")
    ap.add_argument("--screenshot", default=None, metavar="DIR",
                    help="遍历 check-05 的 5 个样本,每个样本出一张 1440x900 整窗截图到 DIR")
    ap.add_argument("--keep", action="store_true", help="保留临时工作目录供排查")
    return ap.parse_args()


def main():
    args = parse_args()
    items = []
    for chunk in (args.item or []):
        items.extend(p.strip() for p in chunk.split(",") if p.strip())
    if not items:
        items = list(ITEMS)
    bad = [i for i in items if i not in ITEMS]
    if bad:
        raise SystemExit(f"ERROR: 未知项 {bad}(可用:{sorted(ITEMS)})")

    server = c05.ensure_server()
    tmp_root = Path(tempfile.mkdtemp(prefix="idi-09-gate-"))
    info("tmp", f"临时工作目录 {tmp_root}(--keep 可保留)")
    pw = browser = None
    try:
        from playwright.sync_api import sync_playwright

        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=True)
        info("browser.version", browser.version)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.set_default_timeout(20000)
        for name in items:
            ITEMS[name](page, tmp_root)
        if args.screenshot:
            run_screenshots(page, Path(args.screenshot), tmp_root)
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

    summary = list(items) + (["shot"] if args.screenshot else [])
    print("\n=== 逐项结论 ===", flush=True)
    verdicts = {}
    for i in summary:
        v = c05.item_verdict(i)
        verdicts[i] = v
        rows = [r for r in c05.ROWS if r["item"] == i]
        fails = len([r for r in rows if r["verdict"] == "FAIL"])
        blocks = len([r for r in rows if r["verdict"] == "BLOCKED"])
        print(f"item {i}: {v.upper()}  ({len(rows)} 条断言,{fails} FAIL,{blocks} BLOCKED)",
              flush=True)
    any_fail = any(v == "fail" for v in verdicts.values())
    any_blocked = any(v == "blocked" for v in verdicts.values())
    code = 1 if any_fail else (2 if any_blocked else 0)
    print(f"\nexit={code}  (0=全 pass,1=有 fail,2=有 blocked)", flush=True)
    return code


if __name__ == "__main__":
    sys.exit(main())

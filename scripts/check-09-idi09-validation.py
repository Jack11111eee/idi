#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check-09-idi09-validation.py — Phase 9「卡片容器化与页面底色下沉」的运行时门,
Phase 11「去卡片化与发丝分隔线」把它**改写**为断言去卡片后的新契约。

为什么另开一个文件(Phase 9 的原始论证,Phase 11 后仍逐字成立)
    既有五条门里**没有任何一条**断言五个容器的 `background` / `border` /
    `border-radius` / `box-shadow`:
      - `check-01-token-conformance.sh`  只数围栏外的裸 hex 与 tier-1 原语引用
      - `check-02-contrast.py`           只算 PAIR 清单上的对比度比值
      - `check-03-hidden-uniqueness.sh`  只数 `.hidden {` 规则条数
      - `check-04-important-count.sh`    只数 `!important;` 声明条数
      - `check-05-ui-uat.py`             断言的是既有 UAT 项(令牌接线 / 几何 / 焦点环),
                                         对「容器是不是卡片」恒真
    Phase 9 补的是这条缝;Phase 11 反转了它断言的那套卡片语言,故本文件**被改写而不是
    被删除** —— 旧契约(四边 border + 卡片底色 + 卡片阴影 + gray-3 页面档 + 12px 灰缝)
    反转后**必然全红**,那正是门在正确工作的证据(ROADMAP Phase 11 Rationale 的逐字表述)。
    改写后的判据断言新契约:连续面(五个容器不再绘制边界)+ 统一面(面板与页面同色、
    内陷面仍更暗)+ 灰缝归零 + 两条发丝线。全部断言仍是真实浏览器里的
    `getComputedStyle` **计算读数**,不是源码文本匹配:容器边界是**画出来**的,文本里
    写着 `border: none` 不等于它真的生效。令牌解析降为 `info()` 诊断 —— 见下条。
    唯一的源码文本级断言是两条**专用**残留断言(见 c1),它读的是围栏全文(含注释)。

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

断言与需求的映射(Phase 11 改写后)
    c1 → REG-01 / SURF-01 / SURF-02   左栏 4 个 section 的**连续面**:box-shadow == none、
                                     四个物理角长手 == 0px、计算底色 == 统一面、边界宽度按
                                     **异形**形状断言(第一个 section 四边全 0px,其余三个
                                     各带一条 1px 上边线);外加交互控件对照组(证明
                                     「移除边界」严格限于五个容器)、活动标记的正面断言、
                                     两条**专用**残留断言与两条「被删令牌已不可解析」探测器
    c2 → REG-01 / DIV-01              #doc-panel 的**单边竖线**:box-shadow == none、四角 0px、
                                     四条边中**仅** border-left-width == 1px、border-left 的
                                     颜色双断言(令牌 + gray-6 字面量)、overflow-y == auto
                                     (承重的滚动契约),外加 #doc-panel-header 的 sticky /
                                     top / 背景三条断言(背景已随统一面改归属)
    c3 → REG-01 / SURF-02             **两级**刻度:body 计算底色 == 统一面令牌解析值 **且**
                                     == 写死字面量白 **且** != 旧的 gray-3 页面档;
                                     内陷面令牌解析值的相对亮度**严格低于**统一面
                                     (判据取令牌级读数,不取 effective_bg)
    c4 → REG-01 / SURF-03 / DIV-01..03 灰缝归零(#main-pane gap == 0px)+ 两条发丝线的宽度与
                                     颜色**双断言**(令牌 + gray-6 字面量)+ 第一个面板顶部
                                     不画线 + 竖线宿主跨满视口的真实几何,外加三条对照组
    c5 → REG-02                      滚动契约保持:#doc-panel / #chat-messages 的
                                     overflow-y == auto,sticky 表头在**已证明可滚**的
                                     前提下滚到底仍可见
    shot                             逐样本整窗截图,供用户评审(不参与卡片判据)

断言写法纪律(Phase 11 / D-11-12 的机器形态)
    `ok()` 在**期望侧为 None 时降级成 BLOCKED**(exit 2,本项目把 2 当作良性码),文案还
    指向 DOM。令牌一旦被删,旧式「断言解析值」不会变红,而是静默变成「良性阻塞」。
    故本文件里**每一处令牌解析断言都走 `ok_true` 并显式处理 `None`**。

浏览器路线(实测结论,不是偏好)
    固定走 Playwright 自带 chromium + 无头(与 check-06 同款)。本机 `channel="chrome"`
    + headless 会 CDP 挂死(见 check-05 文件头的实测记录),故本文件不提供 `--browser`。
"""
from __future__ import annotations

import argparse
import importlib.util
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

# 横线的宿主:只有后三个。`#session-panel` 是 DOM 第一个 section,
# `#main-pane > section + section` 永不匹配它 ⇒ 第一个面板顶部不画线(D-11-10)。
HAIRLINE_SECTIONS = ["#annotations-panel", "#checks-panel", "#ai-panel"]

# 四个**物理角长手**。为什么不读简写 `border-radius`:简写在多值规则体上会被 Chrome
# 序列化成三值,`== "0px"` 这种断言不可满足。长手读法在任何规则体上都成立。
RADIUS_CORNER_PROPS = (
    "border-top-left-radius",
    "border-top-right-radius",
    "border-bottom-left-radius",
    "border-bottom-right-radius",
)
BORDER_SIDES = ("top", "right", "bottom", "left")

# 围栏标记与 style.css 路径 —— 供源码文本级的**专用残留断言**读围栏全文。
# 两个标记字符串与 scripts/check-10-idi10-validation.py 逐字相同。
STYLE_CSS = ROOT / "frontend" / "style.css"
FENCE_START = "===== DESIGN TOKENS: START ====="
FENCE_END = "===== DESIGN TOKENS: END ====="

# 三档字面量:断言**两侧都写死**。若两侧都从同一个令牌解析,令牌被改坏(而消费者仍接着
# 线)也照样 PASS —— 那条接线的价值就消失了。三档分别对应
# --color-surface-page(统一面,白)/ --color-surface(内陷面,gray-2)/
# --color-border-subtle(发丝线,gray-6)。
SURFACE_PAGE_LITERAL = "rgb(255, 255, 255)"
SURFACE_SUNKEN_LITERAL = "rgb(249, 249, 249)"
HAIRLINE_LITERAL = "rgb(217, 217, 217)"

# Phase 11 反转自己孤立掉、随后删掉的两个卡片令牌名。它们在本文件里只以**字面量**出现:
# 判据正是「style.css 的围栏全文里还有没有这个名字」。
RETIRED_CARD_TOKENS = ("--color-surface-card", "--shadow-card")

# 交互控件对照组(SC1 明文要求的反向证据):没有它,「移除边界」可能是把整站边界一起抹掉。
# 五个选择器在 frontend/index.html 里都存在;`#ai-route-select` / `#check-switcher` 之所以
# 被选为 `select` 族的代表,是因为它们在样式表里**各有一条显式声明** ⇒ 判据确定,不依赖
# UA 默认样式。
# ⚠ `.panel-header` **不得**进这个序列:它有合法的 `border-radius: 0`(D-11-7)与合法的
#   `inset 3px 0 0` 活动标记阴影,断言「圆角非零」会把它误判为缺陷。
# 第三列 = 该控件是否承载 resting border。四个表单控件各有一条
# `border: 1px solid var(--color-border-strong)`;`.overlay-card` **从未声明过 border**
# (它只有 `border-radius: var(--radius-md)` + `box-shadow: var(--shadow-overlay)`)⇒
# 它的计算 `border-top-width` 恒为 `0px`(改动前后都一样),故它的反向证据是
# 「圆角 + elevation 仍在」,不是「边框仍在」。
CONTROL_GROUP = (
    ("button", "全局按钮族", True),
    ("#project-path-input", "AI 面板的路径输入框", True),
    ("#check-switcher", "核查报告切换 select", True),
    ("#ai-route-select", "AICaller 路线 select", True),
    (".overlay-card", "弹窗卡片(无 resting border,靠圆角 + elevation 取证)", False),
)


def fence_text():
    """返回两行 `===== DESIGN TOKENS: START/END` 之间的文本(含标记行自身)。

    逐字照抄 scripts/check-10-idi10-validation.py 的同名函数:本文件原先没有它,
    Phase 11 的两条专用残留断言需要读围栏全文(含注释)。
    """
    text = STYLE_CSS.read_text(encoding="utf-8")
    start = text.index(FENCE_START)
    end = text.index(FENCE_END)
    return text[start:end]


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
# c1 — 左栏 4 个 section 的连续面 + 交互控件对照组(REG-01 / SURF-01 / SURF-02)
# ---------------------------------------------------------------------------
# 样本 p1:4 个 section 在 p1 下全部存在于 DOM 中。`getComputedStyle` 对
# `display: none` 的元素同样返回解析值,故无需为每个面板切样本 —— 与 check-05
# item 9 读 `#annotation-list` 同一依据(#annotations-panel / #checks-panel 在 p1 下
# 带 `.hidden`,读数照常返回)。
def c1(page, tmp_root):
    item = "c1"
    print("\n=== c1: 左栏 4 个 section 的连续面(REG-01 / SURF-01 / SURF-02)===", flush=True)

    # ---- (a) 源码文本级:两条**专用**残留断言(浏览器之前就能判,不需要 fixture)----
    # 判据是**围栏内的子串计数,扫含注释的围栏全文** —— 只删声明行不够:一条点名该令牌的
    # 注释会让计数非零。依据是围栏抬头与 Hard Rule 5 / D-04「只声明被消费的令牌」;先例是
    # Phase 10 删掉未并入刻度的圆角档位时给它加的那条专用残留断言(check-10 的 r1)。
    # ⚠ 这**不是**通用的围栏消费断言(「每个声明的令牌都被消费」)—— 通用断言属 G2,
    #   用户 2026-09-28 明确排除在 v1.16 范围外。本阶段只处置本次反转自己孤立掉的两个
    #   令牌,每个令牌一条**专用**断言;不得把它扩写成通用形态。
    fenced = fence_text()
    for token in RETIRED_CARD_TOKENS:
        count = fenced.count(token)
        ok_true(item, f"c1 [源码] 围栏内 {token} 残留计数 == 0(含注释)",
                count == 0, "== 0", str(count),
                note="读 DESIGN TOKENS 围栏内的**全文含注释**(子串计数):只删声明行不够,"
                     "点名它的注释也会让计数非零(D-04 / Hard Rule 5;Phase 10 的 --radius-lg"
                     " 先例)。这不是通用围栏消费断言 —— 通用断言属 G2,不在 v1.16 范围")

    proj = c05.make_fixture("p1", tmp_root)
    c05.enter_project(page, proj)

    # ---- (b) 运行时:被删令牌的探测器(硬 FAIL,不得降级为 BLOCKED)----
    # ⚠ 走 ok_true 而**不是** ok():ok() 在期望侧 / actual 为 None 时记 BLOCKED
    # (exit 2,本项目把 2 当作良性码),而「令牌被删」正是本项要抓的回归 —— 令牌未声明
    # 必须是硬 FAIL,否则删掉这两个令牌这条回归在本门里无人拦。
    for token in RETIRED_CARD_TOKENS:
        gone = resolve_token(page, token)
        ok_true(item, f"c1 [令牌] 被删令牌 {token} 已不可解析(解析值 None)",
                gone is None, "None", str(gone),
                note="被删令牌的探测器:它若还能解析出值,说明删漏了或消费者没搬完。"
                     "令牌未声明按 FAIL 计,不得降级为 BLOCKED")

    # ---- (c) 运行时:四个 section 的连续面 ----
    # 底色判据取**同一份读数里**的 body 计算底色(body 是统一面的实际绘制者),并另与
    # 写死字面量比对 —— 两侧都写死,防止「令牌被改坏而消费者仍接线」时假绿。
    body_bg = read_style(page, "body", "background-color")
    info("c1 body 计算 background-color 原始读数(统一面的实际绘制值)", f"{body_bg}")

    for sel in LEFT_SECTIONS:
        bg = read_style(page, sel, "background-color")
        corners = {p: read_style(page, sel, p) for p in RADIUS_CORNER_PROPS}
        widths = {s: read_style(page, sel, f"border-{s}-width") for s in BORDER_SIDES}
        shadow = read_style(page, sel, "box-shadow")
        info(f"c1 {sel} 原始读数",
             f"background-color={bg} box-shadow={shadow} "
             f"corner-radii={[corners[p] for p in RADIUS_CORNER_PROPS]} "
             f"border-widths={[widths[s] for s in BORDER_SIDES]}")
        if bg is None or shadow is None or None in corners.values() or None in widths.values():
            blocked(item, f"[p1] {sel} 的读数可读", "非 None 的计算读数",
                    f"{bg} / {shadow} / {corners} / {widths}", "元素/选择器不存在")
            continue
        ok(item, f"[p1] {sel} 计算 box-shadow == none(不绘制阴影)", "none", shadow,
           note="Phase 9 的卡片阴影随去卡片化整段作废")
        for prop in RADIUS_CORNER_PROPS:
            ok(item, f"[p1] {sel} 计算 {prop} == 0px(不绘制圆角)", "0px", corners[prop],
               note="读**长手**不读简写:简写在多值规则体上会被 Chrome 序列化成三值,不可断言")
        ok(item, f"[p1] {sel} 计算底色 == body 计算底色(同一份读数)", body_bg, bg,
           note="连续面:面板与页面同色,屏幕上不再有可辨的灰底与 elevation 差(SURF-02)")
        ok(item, f"[p1] {sel} 计算底色 == rgb(255, 255, 255)(写死字面量)",
           SURFACE_PAGE_LITERAL, bg,
           note="与上一条互补:只跟 body 比会跟着令牌一起变;这一条把统一面钉死在白")
        # 边界宽度是**异形**的,不是一条统一循环:#session-panel 是 DOM 第一个 section,
        # `#main-pane > section + section` 永不匹配它 ⇒ 它的四条边全 0px;其余三个各带
        # 一条上边线(横线),另三条边 0px。把四个 section 塞进一条统一循环会写错第一个。
        if sel == "#session-panel":
            for side in BORDER_SIDES:
                ok(item, f"[p1] {sel} 计算 border-{side}-width == 0px(DOM 第一个 section 无横线)",
                   "0px", widths[side],
                   note="相邻兄弟选择器按 **DOM 相邻**判定,第一个 section 顶部不画线")
        else:
            ok(item, f"[p1] {sel} 计算 border-top-width == 1px(横线)", "1px",
               widths["top"])
            for side in ("right", "bottom", "left"):
                ok(item, f"[p1] {sel} 计算 border-{side}-width == 0px(横线只落上边)",
                   "0px", widths[side])

    # ---- (d) 交互控件对照组(SC1 明文要求的反向证据)----
    # 没有它,「移除边界」可能是把整站边界一起抹掉 —— 这条反向证据与上面的正向断言
    # 在同一份运行时读数里给出。
    for sel, label, has_border in CONTROL_GROUP:
        radius = read_style(page, sel, "border-top-left-radius")
        top_width = read_style(page, sel, "border-top-width")
        shadow = read_style(page, sel, "box-shadow")
        info(f"c1 对照组 {sel} 原始读数",
             f"border-top-left-radius={radius} border-top-width={top_width} box-shadow={shadow}")
        if radius is None or top_width is None or shadow is None:
            blocked(item, f"[p1] 对照组 {sel} 的读数可读", "非 None 的计算读数",
                    f"{radius} / {top_width} / {shadow}", "元素/选择器不存在")
            continue
        ok_true(item, f"[p1] 对照组 {sel}({label})计算 border-top-left-radius != 0px",
                radius != "0px", "!= 0px", str(radius),
                note="去卡片化严格限于五个容器:表单控件与弹窗卡片仍有各自的圆角")
        if has_border:
            ok_true(item, f"[p1] 对照组 {sel}({label})计算 border-top-width != 0px",
                    top_width != "0px", "!= 0px", str(top_width),
                    note="该控件承载一条 resting border:1px solid var(--color-border-strong)")
        else:
            ok_true(item, f"[p1] 对照组 {sel}({label})计算 box-shadow != none",
                    shadow != "none", "!= none", str(shadow),
                    note="它**从未声明过 border**(计算 border-top-width 恒为 0px,改动前后都"
                         "一样),故它的反向证据是 elevation 仍在:--shadow-overlay")

    # ---- (e) 活动面板标记的正面断言(去卡片后仅存的活动态视觉线索)----
    # ⚠ `.panel-header` 既不进对照组、也不进「box-shadow === none」的判定集:它合法地携带
    # `inset 3px 0 0 var(--color-marker-active)`(三条 ID 选择器,#session-panel 在 p1 下
    # 未隐藏)。任何「所有面板后代 box-shadow === none」的写法都会把它误判为缺陷。
    marker = read_style(page, "#session-panel .panel-header", "box-shadow")
    info("c1 #session-panel .panel-header 活动标记原始读数", f"{marker}")
    ok_true(item, "[p1] #session-panel .panel-header 活动标记存活(inset 3px 0px 竖条)",
            marker is not None and "inset" in marker and "3px 0px" in marker,
            "含 inset 与 3px 0px", str(marker),
            note="去卡片化后仅存的活动态视觉线索,不得被本次改动波及;.panel-header 的圆角已"
                 "在 D-11-7 归零,故它不进交互控件对照组")


# ---------------------------------------------------------------------------
# c2 — #doc-panel 的单边竖线 + sticky 表头(REG-01 / DIV-01)
# ---------------------------------------------------------------------------
# Phase 9 的判据是「右栏与左栏取**同一组**令牌(底色 / 边界 / 圆角 / 阴影)」;Phase 11
# 反转了那条同族叙事:四边边界收成**单边竖线**,底色改归统一面。故本项的期望侧不再取
# 卡片令牌,而是「仅左边一条 1px、其余三条边 0px」这个**形状**。
def c2(page, tmp_root):
    item = "c2"
    print("\n=== c2: #doc-panel 的单边竖线 + sticky 表头(REG-01 / DIV-01)===", flush=True)
    proj = c05.make_fixture("p1", tmp_root)
    c05.enter_project(page, proj)

    subtle = resolve_color(page, "--color-border-subtle")
    info("c2 令牌解析", f"--color-border-subtle={subtle}")

    bg = read_style(page, "#doc-panel", "background-color")
    corners = {p: read_style(page, "#doc-panel", p) for p in RADIUS_CORNER_PROPS}
    shadow = read_style(page, "#doc-panel", "box-shadow")
    overflow_y = read_style(page, "#doc-panel", "overflow-y")
    widths = {s: read_style(page, "#doc-panel", f"border-{s}-width") for s in BORDER_SIDES}
    left_style = read_style(page, "#doc-panel", "border-left-style")
    left_color = read_style(page, "#doc-panel", "border-left-color")
    info("c2 #doc-panel 原始读数",
         f"background-color={bg} box-shadow={shadow} overflow-y={overflow_y} "
         f"corner-radii={[corners[p] for p in RADIUS_CORNER_PROPS]}")
    info("c2 #doc-panel 四条边框宽度原始读数",
         " / ".join(f"{s}={widths[s]}" for s in BORDER_SIDES))
    info("c2 #doc-panel border-left 原始读数", f"{widths['left']} {left_style} {left_color}")

    if (None in (bg, shadow, overflow_y, left_style, left_color)
            or None in corners.values() or None in widths.values()):
        blocked(item, "[p1] #doc-panel 的读数可读", "非 None 的计算读数",
                f"{bg} / {shadow} / {overflow_y} / {widths} / {corners}",
                "元素/选择器不存在")
    else:
        ok(item, "[p1] #doc-panel 计算 box-shadow == none(不绘制阴影)", "none", shadow,
           note="Phase 9 的四边卡片阴影随去卡片化整段作废")
        for prop in RADIUS_CORNER_PROPS:
            ok(item, f"[p1] #doc-panel 计算 {prop} == 0px(不绘制圆角)", "0px", corners[prop],
               note="读长手不读简写(简写在多值规则体上会被 Chrome 序列化成三值)")
        # 四条边里**仅**左边一条是线 —— 这正是「四边卡片收成单边竖线」的机器读数。
        ok(item, "[p1] #doc-panel 计算 border-left-width == 1px(竖线)", "1px",
           widths["left"])
        for side in ("top", "right", "bottom"):
            ok(item, f"[p1] #doc-panel 计算 border-{side}-width == 0px(单边,非四边)",
               "0px", widths[side],
               note="四边边界收成单边竖线(D-11-9);残留的顶侧边框会顶破 check-05 --item 8"
                    " 的 sticky 容差")
        ok(item, "[p1] #doc-panel 计算 border-left-style == solid", "solid", left_style)
        ok(item, "[p1] #doc-panel 计算 border-left-color == var(--color-border-subtle)",
           subtle, left_color,
           note="线取既有的语义令牌 gray-6 ⇒ 零新增令牌、零新增颜色值(D-11-8)")
        ok(item, "[p1] #doc-panel 计算 border-left-color == gray-6 字面量",
           HAIRLINE_LITERAL, left_color,
           note="与上一条互补:只跟令牌比是**自指**的 —— 把该令牌换成 --color-border"
                "(gray-7)会让两侧一起变、恒过,而那正是 D-11-8 显式否决的备选。这一条把"
                "「线是浅档」钉死在 gray-6,使那个备选对本门可见")
        # 承重事实,必须正面断言:它是右列的滚动者,L-1 的 sticky 表头依赖它仍是最近的
        # 可滚祖先。删掉它不会让任何颜色断言变红,所以这里不靠颜色门兜底。
        # ⚠ 保留它的理由**只有** L-1:磁盘实测 check-05 的滚动者普查是 3 个成员,且
        #   #doc-panel 根本不在它的遍历范围内(它是 #main-pane 的兄弟)。
        ok(item, "[p1] #doc-panel 计算 overflow-y == auto(承重的滚动契约)", "auto",
           overflow_y, note="L-1 的 sticky 表头依赖 #doc-panel 仍是最近的可滚祖先")

    # #doc-panel-header:sticky 与背景仍成立。背景声明本身不得删除(不加背景则滚动正文
    # 从标题行底下穿过);Phase 11 只改它的**归属令牌**:表头底色与统一面同值。
    position = read_style(page, "#doc-panel-header", "position")
    top = read_style(page, "#doc-panel-header", "top")
    header_bg = read_style(page, "#doc-panel-header", "background-color")
    body_bg = read_style(page, "body", "background-color")
    info("c2 #doc-panel-header 原始读数",
         f"position={position} top={top} background-color={header_bg}")
    ok(item, "[p1] #doc-panel-header 计算 position == sticky", "sticky", position)
    ok(item, "[p1] #doc-panel-header 计算 top == 0px", "0px", top)
    ok_true(item, "[p1] #doc-panel-header 计算 background-color 非透明(sticky 遮挡前提)",
            header_bg is not None and header_bg not in ("rgba(0, 0, 0, 0)", "transparent"),
            "非 rgba(0, 0, 0, 0)", str(header_bg),
            note="不加背景则滚动正文从标题行底下穿过 —— 背景声明是必需的,不是可选")
    ok(item, "[p1] #doc-panel-header 计算 background-color == body 计算底色(归属统一面)",
       body_bg, header_bg,
       note="Phase 11 只改它的归属令牌:表头底色与统一面同值,不再取卡片令牌")


# ---------------------------------------------------------------------------
# c4 — 灰缝归零 + 两条发丝线 + 竖线跨满几何(REG-01 / SURF-03 / DIV-01..03)
# ---------------------------------------------------------------------------
# 判据是**计算几何读数**,不是源码文本匹配 —— 与 check-05 的 padding 断言同口径,
# 期望侧一律写字面量 px 字符串(不是令牌名:两侧都从同一个令牌解析会让「令牌改坏
# 但声明仍接线」假绿)。
#
# 三条对照组是**回归护栏**,不是重复劳动:
#   · .panel-body padding —— D-11-6:去卡片化删的是「容器边界」,不是「内容呼吸」。
#   · #doc-panel-body padding —— 证明改动没有漏到右栏(它另有 check-05 item 4 的活断言
#     `32px 40px`);重列一遍是为了让「有人把 .panel-body 的选择器扩成同时命中
#     #doc-panel-body」这件事在本文件里也能当场变红,而不必等 check-05。
#   · .panel-header padding-top —— 表头是 36px 固定高的 chrome 条,它的内边距不在裁定
#     范围内,故刻意未随卡片内边距一起改。
def c4(page, tmp_root):
    item = "c4"
    print("\n=== c4: 灰缝归零 + 两条发丝线 + 竖线跨满几何 ===", flush=True)
    proj = c05.make_fixture("p1", tmp_root)
    c05.enter_project(page, proj)

    subtle = resolve_color(page, "--color-border-subtle")
    info("c4 令牌解析", f"--color-border-subtle={subtle}")

    gap = read_style(page, "#main-pane", "gap")
    info("c4 #main-pane gap 原始读数", f"{gap}")
    ok(item, "[p1] #main-pane 计算 gap == 0px(灰缝归零)", "0px", gap,
       note="Phase 9 把间隙当作卡片层次的载体(间隙里透出页面底色);Phase 11 里面板与页面"
            "同色,间隙不再承载任何东西,分区改由发丝线承担(SURF-03)")

    # ---- 竖线:#doc-panel 的 border-left ----
    left_w = read_style(page, "#doc-panel", "border-left-width")
    left_color = read_style(page, "#doc-panel", "border-left-color")
    info("c4 竖线 #doc-panel border-left 原始读数", f"{left_w} {left_color}")
    ok(item, "[p1] 竖线 #doc-panel 计算 border-left-width == 1px", "1px", left_w)
    ok(item, "[p1] 竖线 #doc-panel 计算 border-left-color == var(--color-border-subtle)",
       subtle, left_color)
    ok(item, "[p1] 竖线 #doc-panel 计算 border-left-color == gray-6 字面量",
       HAIRLINE_LITERAL, left_color,
       note="与上一条互补:只跟令牌比是**自指的** —— 令牌被改成 gray-7 时两侧一起变、恒过;"
            "这一条把「线是浅档」钉死在 gray-6。**没有它,D-11-8 显式否决的那个备选"
            "(gray-7)对门是不可见的。**")

    # ---- 横线:#main-pane > section + section 的 border-top(恰 3 条)----
    for sel in HAIRLINE_SECTIONS:
        w = read_style(page, sel, "border-top-width")
        c = read_style(page, sel, "border-top-color")
        info(f"c4 横线 {sel} border-top 原始读数", f"{w} {c}")
        ok(item, f"[p1] 横线 {sel} 计算 border-top-width == 1px", "1px", w)
        ok(item, f"[p1] 横线 {sel} 计算 border-top-color == var(--color-border-subtle)",
           subtle, c)
        ok(item, f"[p1] 横线 {sel} 计算 border-top-color == gray-6 字面量",
           HAIRLINE_LITERAL, c,
           note="字面量半条是承重的:使 D-11-8 否决的 gray-7 备选对本门可见")
    ok(item, "[p1] 横线 #session-panel 计算 border-top-width == 0px(第一个面板顶部不画线)",
       "0px", read_style(page, "#session-panel", "border-top-width"),
       note="#session-panel 是 DOM 第一个 section,相邻兄弟选择器永不匹配它 ⇒ 恰 3 条线;"
            "顶部是窗口边缘,画了会读成多一条(D-11-10)")

    # ---- 竖线跨满:#doc-panel 的 rect 覆盖整个视口高 ----
    # 这一条是**承重的**:没有它,「跨满面板可视高度」就退化成一条恒真的
    # 「有一条 1px 边框」断言。
    rect = page.evaluate(
        "() => { const el = document.querySelector('#doc-panel'); if (!el) return null;"
        " const r = el.getBoundingClientRect();"
        " return {top: r.top, bottom: r.bottom, height: r.height}; }")
    info("c4 竖线宿主 #doc-panel getBoundingClientRect", f"{rect}")
    if not isinstance(rect, dict):
        blocked(item, "[p1] 竖线宿主 #doc-panel 的 rect 可读", "非 None 的 rect", str(rect),
                "元素/选择器不存在")
    else:
        viewport_h = page.evaluate("() => window.innerHeight")
        info("c4 视口高 window.innerHeight", f"{viewport_h}")
        ok_true(item, "[p1] 竖线宿主 #doc-panel rect.top == 0(自视口顶起)",
                abs(rect["top"]) <= 0.5, "≈ 0", str(rect["top"]),
                note="0.5px 是浮点读数容差,不是几何放宽")
        ok_true(item, "[p1] 竖线宿主 #doc-panel rect.bottom == 视口高(跨满)",
                abs(rect["bottom"] - viewport_h) <= 0.5, f"≈ {viewport_h}",
                str(rect["bottom"]),
                note="#app 是 align-items: stretch 的 flex 行 ⇒ #doc-panel 天然跨满视口高;"
                     "这条几何读数使「跨满面板可视高度」可失败")
        ok_true(item, "[p1] 竖线宿主 #doc-panel rect.height == 视口高(跨满)",
                abs(rect["height"] - viewport_h) <= 0.5, f"≈ {viewport_h}",
                str(rect["height"]))

    # ---- 三条对照组(证明改动没有漏出裁定范围)----
    controls = [
        (".panel-body", "padding", "16px",
         "D-11-6:去卡片化删的是容器边界,不是内容呼吸"),
        ("#doc-panel-body", "padding", "32px 40px",
         "对照组:右栏阅读列内边距未受影响(check-05 item 4 锁死)"),
        (".panel-header", "padding-top", "6px",
         "对照组:表头 chrome 条的内边距未随卡片内边距改动"),
    ]
    for sel, prop, expected, note in controls:
        actual = read_style(page, sel, prop)
        info(f"c4 {sel} {prop} 原始读数", f"{actual}")
        if actual is None:
            blocked(item, f"[p1] {sel} 计算 {prop} == {expected}(对照组)", expected,
                    "<MISSING>", "元素/选择器不存在")
            continue
        ok(item, f"[p1] {sel} 计算 {prop} == {expected}(对照组)", expected, actual, note=note)


# ---------------------------------------------------------------------------
# c3 — 两级刻度(REG-01 / SURF-02):统一面 == body 底色,内陷面严格更暗
# ---------------------------------------------------------------------------
# 判据是**令牌级**读数,不是某个元素的「有效背景」:两级刻度里未被任何元素采用的那一档
# 会被 effective_bg 沿祖先链整个跳过,断言就在看不见的那一档上恒真(Phase 9 已为此付过
# 代价)。故用 resolve_color 分别解析两个令牌后比较。
#
# 亮度比较直接复用 check-05 的 relative_luminance / contrast_ratio(与 probe-07 的
# 纪律一致:直接导入它自己的实现,不另写一份)。
def c3(page, tmp_root):
    item = "c3"
    print("\n=== c3: 两级刻度 —— 统一面 == body 底色,内陷面严格更暗 ===", flush=True)
    proj = c05.make_fixture("p1", tmp_root)
    c05.enter_project(page, proj)

    body_bg = read_style(page, "body", "background-color")
    page_token = resolve_color(page, "--color-surface-page")
    sunken_token = resolve_color(page, "--color-surface")
    info("c3 body 计算 background-color 原始读数", f"{body_bg}")
    info("c3 统一面 --color-surface-page 解析值", f"{page_token}")
    info("c3 内陷面 --color-surface 解析值", f"{sunken_token}")

    # ⚠ 令牌解析断言一律走 ok_true 并显式处理 None:ok() 在期望侧为 None 时记 BLOCKED
    # (exit 2,本项目把 2 当作良性码),而「令牌被删」必须是 FAIL。
    ok_true(item, "[p1] --color-surface-page 已声明且可解析(堵住 ok() 的 None-期望侧降级)",
            page_token is not None, "非 None", str(page_token),
            note="ok() 在期望侧为 None 时记 BLOCKED(exit 2,本项目当良性码)—— 令牌缺失"
                 "必须是 FAIL,不是 BLOCKED")
    ok_true(item, "[p1] body 计算底色 == --color-surface-page 解析值(底色来自令牌)",
            page_token is not None and c05.norm(body_bg) == c05.norm(page_token),
            f"== {page_token}", str(body_bg),
            note="等值复核:证明底色来自令牌而不是硬编码的 rgb()。少了这条,把 body 写成"
                 "字面量再删掉令牌声明也能全绿")
    ok(item, "[p1] body 计算底色 == rgb(255, 255, 255)(统一面写死字面量)",
       SURFACE_PAGE_LITERAL, body_bg,
       note="与上一条互补:两侧都写死,防止「令牌被改坏而消费者仍接线」时假绿")
    ok_true(item, "[p1] body 计算底色 != rgb(240, 240, 240)(Phase 9 的 gray-3 页面档已退场)",
            c05.norm(body_bg) != c05.norm("rgb(240, 240, 240)"),
            "!= rgb(240, 240, 240)", str(body_bg),
            note="Phase 11 把卡片档并回页面档:旧的三级刻度叙事(gray-3 页面 < gray-2 内陷"
                 " < 白卡片)改写成**两级**(统一面白 > 内陷面 gray-2)—— 「统一」是把卡片档"
                 "并回页面档,不是把所有层次压平")
    ok_true(item, "[p1] 内陷面 --color-surface 解析值 == rgb(249, 249, 249)(写死字面量)",
            sunken_token is not None
            and c05.norm(sunken_token) == c05.norm(SURFACE_SUNKEN_LITERAL),
            f"== {SURFACE_SUNKEN_LITERAL}", str(sunken_token),
            note="与统一面同理:两侧都写死。少了这条,把内陷面令牌换成更暗的一档(例如旧"
                 "gray-3)也能全绿 —— 亮度序的严格小于拦不住「更暗」")

    parsed_page = c05.parse_rgb(page_token) if page_token else None
    parsed_sunken = c05.parse_rgb(sunken_token) if sunken_token else None
    if parsed_page is None or parsed_sunken is None:
        blocked(item, "[p1] 统一面与内陷面两个令牌均解析为 rgb(...)", "2 个可解析读数",
                f"page={page_token} sunken={sunken_token}",
                "令牌未声明或解析失败 ⇒ 亮度序不可判,不记 PASS")
        return

    lum_page = c05.relative_luminance(parsed_page)
    lum_sunken = c05.relative_luminance(parsed_sunken)
    info("c3 统一面相对亮度", f"{lum_page:.6f}")
    info("c3 内陷面相对亮度", f"{lum_sunken:.6f}")
    # 两档比值是**只读诊断**(不判定):给截图评审一个「ΔL 到底有多大」的锚点。
    info("c3 统一面 vs 内陷面 对比度比值(只读诊断,不判定)",
         f"{c05.contrast_ratio(parsed_page, parsed_sunken):.4f}")

    ok_true(item, "[p1] 内陷面相对亮度严格低于统一面(两级刻度未塌成一档)",
            lum_sunken < lum_page,
            "lum(内陷面) < lum(统一面)",
            f"内陷面={lum_sunken:.6f} 统一面={lum_page:.6f}",
            note="严格小于(不是 <=):两档若相等,内陷面这一档就没有画出来")


# ---------------------------------------------------------------------------
# c5 — 滚动契约保持
# ---------------------------------------------------------------------------
# 本项**不重复** check-05 item 9 的滚动者集合普查(那一条更严,口径是「恰好」)。
# 这里只断言本阶段改动的两个具体滚动者,外加 sticky 表头的可滚前提。
#
# 关于 sticky 的断言纪律:先在运行时**证明可滚前提成立**(scrollHeight >
# clientHeight),再断言「滚到底时表头仍在面板可视区内」。在不可滚的容器上断言
# 「滚到底后表头仍可见」是空转 —— 它恒真,因为根本滚不动。
_C5_SCROLL_JS = """() => {
  const panel = document.querySelector('#doc-panel');
  const header = document.querySelector('#doc-panel-header');
  if (!panel || !header) return {error: '#doc-panel 或 #doc-panel-header 不存在'};

  const measured = () => {
    const pr = panel.getBoundingClientRect();
    const hr = header.getBoundingClientRect();
    return {
      scrollHeight: panel.scrollHeight, clientHeight: panel.clientHeight,
      scrollTop: panel.scrollTop,
      panel: {top: pr.top, bottom: pr.bottom, height: pr.height},
      header: {top: hr.top, bottom: hr.bottom, height: hr.height},
    };
  };

  const before = measured();
  let host = null, hostLabel = null, extended = false;
  if (before.scrollHeight <= before.clientHeight) {
    // 前提不足 ⇒ 走应用自身的渲染路径把文档内容加长(renderMarkdown 是 app.js 渲染
    // 文档区的那个函数),再复查。不直接改 innerHTML:那会绕过被断言的那条渲染路径,
    // 证明的是别的应用。
    //
    // 落点必须取**当前可见**的那个 markdown 宿主:五个 .doc-subview 里只有一个不带
    // .hidden,把内容追加进被 display:none 藏住的子树不会改变任何布局读数(首跑就是
    // 这样:追加进了 p1 下隐藏的 #round-doc,scrollHeight 纹丝不动)。
    const subview = document.querySelector('#doc-panel-body .doc-subview:not(.hidden)');
    host = subview ? subview.querySelector('.markdown-body') : null;
    if (!host) host = document.querySelector('#doc-panel-body');
    if (typeof renderMarkdown !== 'function' || !host) {
      return {premise: 'unavailable', before: before,
              error: 'renderMarkdown 或可见的文档宿主不可用'};
    }
    hostLabel = host.id ? '#' + host.id
      : host.tagName.toLowerCase()
        + ((typeof host.className === 'string' && host.className.trim())
           ? '.' + host.className.trim().split(/\\s+/).join('.') : '');
    const filler = Array.from({length: 60},
      (_, i) => '第 ' + (i + 1) + ' 段滚动前提探针:把右栏文档区撑到可滚。').join('\\n\\n');
    host.appendChild(renderMarkdown(filler));
    extended = true;
  }

  const premise = measured();
  if (premise.scrollHeight <= premise.clientHeight) {
    return {premise: 'not-scrollable', before: before, premiseReading: premise,
            host: hostLabel, extended: extended};
  }

  panel.scrollTop = panel.scrollHeight;
  const after = measured();
  return {premise: 'ok', before: before, premiseReading: premise, after: after,
          host: hostLabel, extended: extended};
}"""


def c5(page, tmp_root):
    item = "c5"
    print("\n=== c5: 滚动契约保持 —— #doc-panel / #chat-messages / sticky 表头 ===",
          flush=True)
    proj = c05.make_fixture("p1", tmp_root)
    c05.enter_project(page, proj)

    ok(item, "[p1] #doc-panel 计算 overflow-y == auto(承重的滚动契约)", "auto",
       read_style(page, "#doc-panel", "overflow-y"),
       note="L-1 的 sticky 表头依赖它仍是最近的可滚祖先;删它会同时打破 L-1 与计数门")
    ok(item, "[p1] #chat-messages 计算 overflow-y == auto(输入行钉底依赖它)", "auto",
       read_style(page, "#chat-messages", "overflow-y"))
    ok(item, "[p1] #doc-panel-header 计算 position == sticky", "sticky",
       read_style(page, "#doc-panel-header", "position"))
    ok(item, "[p1] #doc-panel-header 计算 top == 0px", "0px",
       read_style(page, "#doc-panel-header", "top"))

    label = "[p1] #doc-panel 可滚前提下,滚到底时 #doc-panel-header 仍在面板可视区内"
    expected = "scrollHeight > clientHeight ∧ header ⊆ panel(滚到底后)"
    result = page.evaluate(_C5_SCROLL_JS)
    if not isinstance(result, dict) or "error" in result:
        blocked(item, label, expected,
                (result or {}).get("error") if isinstance(result, dict) else result,
                "探针跑不起来 ⇒ 不记 PASS")
        return
    if result.get("premise") != "ok":
        blocked(item, label, expected,
                f"scrollHeight={result.get('premiseReading', {}).get('scrollHeight')} "
                f"clientHeight={result.get('premiseReading', {}).get('clientHeight')} "
                f"host={result.get('host')} extended={result.get('extended')}",
                "可滚前提不成立 ⇒ 在不可滚的容器上断言「滚到底表头仍可见」是空转,"
                "绝不记 PASS")
        return

    before, after = result["before"], result["after"]
    info("c5 滚动前 rect",
         f"panel.top={before['panel']['top']} panel.bottom={before['panel']['bottom']} "
         f"header.top={before['header']['top']} header.bottom={before['header']['bottom']}")
    info("c5 滚动后 rect",
         f"panel.top={after['panel']['top']} panel.bottom={after['panel']['bottom']} "
         f"header.top={after['header']['top']} header.bottom={after['header']['bottom']}")
    info("c5 可滚前提读数",
         f"scrollHeight={after['scrollHeight']} clientHeight={after['clientHeight']} "
         f"scrollTop={after['scrollTop']}")
    inside = (after["header"]["top"] >= after["panel"]["top"] - 0.5
              and after["header"]["bottom"] <= after["panel"]["bottom"] + 0.5)
    ok_true(item, label, inside, expected,
            f"header=[{after['header']['top']:.2f}, {after['header']['bottom']:.2f}] "
            f"panel=[{after['panel']['top']:.2f}, {after['panel']['bottom']:.2f}]",
            note="0.5px 容差是浮点读数容差,不是几何放宽 —— 表头必须整体落在面板可视带内")


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


ITEMS = {"c1": c1, "c2": c2, "c3": c3, "c4": c4, "c5": c5}


def parse_args():
    ap = argparse.ArgumentParser(add_help=True, description="Phase 9 卡片语言的运行时门")
    ap.add_argument("--item", action="append", default=None,
                    help="只跑指定项:c1 / c2 / c3 / c4 / c5(可重复,或逗号分隔)")
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

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
    c3 → CARD-03                     body 计算底色 gray-3 + 三档亮度严格递增
                                     (页面 < 内陷面 < 卡片),含令牌级等值复核
    c4 → CARD-03                    密度几何(D-9-2):#main-pane gap 12px / .panel-body
                                     padding 16px,外加 #doc-panel-body 与 .panel-header
                                     两条对照组(证明改动没有漏出裁定范围)
    c5 → REG-02                     滚动契约保持:#doc-panel / #chat-messages 的
                                     overflow-y == auto,sticky 表头在**已证明可滚**的
                                     前提下滚到底仍可见
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
# c3 — 三层刻度(CARD-03):body 底色 + 页面 < 内陷面 < 卡片的亮度序
# ---------------------------------------------------------------------------
# 判据是**令牌级**读数,不是某个元素的「有效背景」:三档本身就是三个令牌,故用
# resolve_color 分别解析后比较 —— effective_bg 沿祖先链找第一个非透明底色,会把
# 三档里未被任何元素采用的中间档整个跳过。
#
# 亮度比较直接复用 check-05 的 relative_luminance / contrast_ratio(与 probe-07 的
# 纪律一致:直接导入它自己的实现,不另写一份)。
GRAY3_BODY = "rgb(240, 240, 240)"
TIER_TOKENS = [
    ("页面", "--color-surface-page"),
    ("内陷面", "--color-surface"),
    ("卡片", "--color-surface-card"),
]


def c3(page, tmp_root):
    item = "c3"
    print("\n=== c3: 三层刻度(CARD-03)—— body 底色 + 亮度序 ===", flush=True)
    proj = c05.make_fixture("p1", tmp_root)
    c05.enter_project(page, proj)

    body_bg = read_style(page, "body", "background-color")
    info("c3 body 计算 background-color 原始读数", f"{body_bg}")
    ok(item, "[p1] body 计算 background-color == rgb(240, 240, 240)(gray-3)",
       GRAY3_BODY, body_bg,
       note="页面不再是全场最亮的东西(CARD-03 / D-9-1)")

    page_token = resolve_color(page, "--color-surface-page")
    info("c3 --color-surface-page 令牌解析值", f"{page_token}")
    # 等值复核:证明底色来自令牌而不是硬编码的 rgb()。少了这条,把 body 写成
    # `background: rgb(240, 240, 240)` 再删掉令牌声明也能全绿。
    ok(item, "[p1] --color-surface-page 解析值 == body 计算底色(底色来自令牌)",
       body_bg, page_token,
       note="与上一条互为对照:硬编码字面量会在这里 FAIL")

    resolved = [(label, token, resolve_color(page, token)) for label, token in TIER_TOKENS]
    for label, token, rgb_str in resolved:
        info(f"c3 {label} {token} 解析值", f"{rgb_str}")

    parsed = [(label, c05.parse_rgb(rgb_str)) for label, _token, rgb_str in resolved]
    if any(rgb is None for _label, rgb in parsed):
        blocked(item, "[p1] 三档令牌均解析为 rgb(...)", "3 个可解析读数",
                str(resolved), "令牌未声明或解析失败 ⇒ 亮度序不可判,不记 PASS")
        return

    lums = [(label, c05.relative_luminance(rgb)) for label, rgb in parsed]
    for label, lum in lums:
        info(f"c3 {label} 相对亮度", f"{lum:.6f}")
    # 两两比值是**只读诊断**(不判定):它是给用户看「ΔL 到底有多小」的锚点,
    # 截图评审时会用到 —— 层次主要靠边框与这点的底色差,不是靠阴影。
    for i in range(len(parsed)):
        for j in range(i + 1, len(parsed)):
            ratio = c05.contrast_ratio(parsed[i][1], parsed[j][1])
            info(f"c3 {parsed[i][0]} vs {parsed[j][0]} 对比度比值(只读诊断,不判定)",
                 f"{ratio:.4f}")

    ok_true(item, "[p1] 三档亮度严格递增:页面 < 内陷面 < 卡片",
            lums[0][1] < lums[1][1] < lums[2][1],
            "lum(页面) < lum(内陷面) < lum(卡片)",
            " < ".join(f"{label}={lum:.6f}" for label, lum in lums),
            note="严格递增(不是 <=):三档若有两档相等,层次就没有画出来")


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

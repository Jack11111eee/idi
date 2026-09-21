#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check-06-idi05-validation.py — idi-05 的 Nyquist 验证缺口补齐(6 条**行为**断言)。

为什么另开一个文件
    `scripts/check-05-ui-uat.py` 覆盖的是「令牌接线」与「computed 值等值」两类证据,
    它对以下六件事**恒真**:期望侧由 `resolve_token()` 在运行时解析 ⇒ 只要消费者仍写着
    `var(--t)`,把 `--t` 的值改坏(例如让 --text-2xl > --text-3xl)断言照样 PASS;
    它读 `box-shadow` 的语义但不看几何;它从不**执行**折叠点击。
    本文件的六条断言补的正是这些「接线对但行为坏」的缝。全部是真实浏览器里的
    **行为/几何**读数,不是源码文本匹配。

与 check-05 的关系
    复用 check-05 的模块级设施(服务生命周期 / fixture 隔离 / enter_project / ok /
    resolve_token / read_style / read_pseudo_style),不重复实现,也不改动 check-05 一行。

运行方式
    .venv/bin/python scripts/check-06-idi05-validation.py
    .venv/bin/python scripts/check-06-idi05-validation.py --item g3,g5
    .venv/bin/python scripts/check-06-idi05-validation.py --keep

退出码语义(与 check-05 一致)
    0 = 全 pass;1 = 至少一条 FAIL;2 = 无 FAIL 但至少一条 BLOCKED

六条断言与需求的映射
    g1 → TYPE-01           三档标题字号在四个宿主上严格降序(值改了也抓得到)
    g2 → VISUAL-03 / SC3   全屏最大字号的文字是文档自己的 h1,不是容器标签
    g3 → VISUAL-04 / E4-E5 活动面板竖条不被不透明子元素遮挡、标题贴左缘、长标题不溢出
    g4 → VISUAL-05 / E6-E7 掩码字形不撑高行盒(差分测量)
    g5 → VISUAL-01 / E3    最窄面板 340px 下 #btn-authorize 单行、不裁切
    g6 → VISUAL-04          #ai-panel 折叠点击穿透:行为与改动前一致

未覆盖(如实记录,不伪装成已覆盖)
    E8「层级读起来是否分明」与 E4/E5 的「竖条在圆角处是否视觉断裂」是**渲染判读**,
    computed style 还原不出;g3 只把可机械核的几何(遮挡 / 贴边 / 溢出 / 圆角半径)
    读出来并打印,判定仍归人工(UAT 第 1/3 项已人工判过)。
    VISUAL-04 的口径收窄(D-16)是**裁决**,不是可测行为,无自动化断言。
"""
from __future__ import annotations

import argparse
import importlib.util
import shutil
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
resolve_token = c05.resolve_token
MARKDOWN_HOSTS = c05.MARKDOWN_HOSTS

GLYPH_MD = (
    "# 一级标题\n\n## 二级标题\n\n### 三级标题\n\n"
    "| 表头 A | 表头 B |\n| --- | --- |\n| 单元格 | 单元格 |\n\n"
    "> 引用块探针\n\nharness `probe` 探针"
)


def px(value):
    """'28px' → 28.0;取不到返回 None。"""
    if not value or not isinstance(value, str) or not value.endswith("px"):
        return None
    try:
        return float(value[:-2])
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# g1 — TYPE-01:三档标题字号在四个宿主上**严格降序**
# ---------------------------------------------------------------------------
# check-05 断言的是「每个宿主的三档各等于其令牌的运行时值」。那条断言对
# 「令牌之间的大小关系」是**盲的**:把 --text-2xl 改成 30px,四条宿主 × 三档的
# 令牌接线断言全部照样 PASS,而「三级标题层级分明、不互相淹没」当场破掉。
# 本断言补的正是这个序关系。
def g1(page, tmp_root):
    item = "g1"
    print("\n=== g1: TYPE-01 三档标题字号严格降序(四宿主)===", flush=True)
    proj = c05.make_fixture("p1", tmp_root)
    c05.enter_project(page, proj)
    page.evaluate("""(args) => {
        const [hosts, md] = args;
        for (const sel of hosts) {
            const host = document.querySelector(sel);
            if (!host) continue;
            host.innerHTML = '';
            host.appendChild(renderMarkdown(md));
        }
    }""", [list(MARKDOWN_HOSTS), GLYPH_MD])

    t3 = px(resolve_token(page, "--text-3xl"))
    t2 = px(resolve_token(page, "--text-2xl"))
    tl = px(resolve_token(page, "--text-lg"))
    info("g1 令牌解析", f"--text-3xl={t3} --text-2xl={t2} --text-lg={tl}")
    if t3 is None or t2 is None or tl is None:
        blocked(item, "g1 三档令牌可解析", "三个 px 值", f"{t3}/{t2}/{tl}", "令牌未声明")
    else:
        ok_true(item, "g1 令牌序 --text-3xl > --text-2xl > --text-lg",
                t3 > t2 > tl, "h1>h2>h3", f"{t3} > {t2} > {tl}")

    for host in MARKDOWN_HOSTS:
        sizes = [px(read_style(page, f"{host} {tag}", "font-size")) for tag in ("h1", "h2", "h3")]
        label = f"[p1] {host} 三档严格降序 h1>h2>h3"
        if any(s is None for s in sizes):
            blocked(item, label, "三个可解析 px 值", str(sizes), "标题未渲染出来")
            continue
        ok_true(item, label, sizes[0] > sizes[1] > sizes[2],
                "h1>h2>h3", " > ".join(f"{s:g}px" for s in sizes))
        # 与 chrome 侧标题不得同档(「不互相淹没」的可机械核半边)
        chrome = px(read_style(page, ".panel-header h2", "font-size"))
        ok_true(item, f"[p1] {host} h3 > chrome 标题(.panel-header h2)",
                sizes[2] > chrome, f">{chrome}px", f"{sizes[2]:g}px")


# ---------------------------------------------------------------------------
# g2 — VISUAL-03 / SC3:全屏最大字号的文字是文档自己的 h1
# ---------------------------------------------------------------------------
# check-05 的层级链只比较**四个被点名的元素**(文档 h1 / 模态 h3 / 文档 h2 /
# 容器标签)。任何第五个元素被改成 30px 都溜得过去。本断言把扫描面提到整页:
# 可见元素里不存在比文档 h1 更大的字号。
# 注意:不断言「最重」—— HEAD 上 `#draft-view > h2`(chrome 标题)是 700,
# 文档 h1 是 600。需求原文针对的是容器标签「文档区」(14px/500),不是全局最重。
def g2(page, tmp_root):
    item = "g2"
    print("\n=== g2: VISUAL-03 文档 h1 是全屏最大字号 ===", flush=True)
    proj = c05.make_fixture("p1", tmp_root)
    c05.enter_project(page, proj)
    page.evaluate("""(args) => {
        const [hosts, md] = args;
        for (const sel of hosts) {
            const host = document.querySelector(sel);
            if (!host) continue;
            host.innerHTML = '';
            host.appendChild(renderMarkdown(md));
        }
    }""", [list(MARKDOWN_HOSTS), GLYPH_MD])

    doc_h1 = px(read_style(page, "#draft-content h1", "font-size"))
    if doc_h1 is None:
        blocked(item, "g2 文档 h1 已渲染", "px 值", None, "renderMarkdown 未产出 #draft-content h1")
        return
    scan = page.evaluate("""() => {
        const out = [];
        for (const el of document.querySelectorAll('body *')) {
            const cs = getComputedStyle(el);
            if (cs.display === 'none' || cs.visibility === 'hidden') continue;
            if (el.getClientRects().length === 0) continue;
            out.push({
                sel: el.tagName + (el.id ? '#' + el.id : '') + (el.className ? '.' + el.className : ''),
                size: parseFloat(cs.fontSize),
                isDocH1: el.matches('#draft-content h1'),
            });
        }
        return out;
    }""")
    info("g2 文档 h1 字号", f"{doc_h1}px")
    others = [r for r in scan if not r["isDocH1"]]
    if not others:
        blocked(item, "g2 页面存在其它可见元素", ">0", 0, "扫描面为空,断言会空过")
        return
    others.sort(key=lambda r: -r["size"])
    info("g2 可见元素字号 Top3", str([(r["sel"], r["size"]) for r in others[:3]]))
    worst = others[0]
    ok_true(item, "g2 全屏最大字号是文档 h1(无可见元素 >= 它)",
            doc_h1 > worst["size"], f"<{doc_h1}px",
            f"max_other={worst['size']}px @ {worst['sel']}")
    # 容器标签「文档区」必须严格小于文档 h1
    label = px(read_style(page, "#doc-panel-header h1", "font-size"))
    ok_true(item, "g2 容器标签 #doc-panel-header h1 严格小于文档 h1",
            label is not None and doc_h1 > label, f"<{doc_h1}px", f"{label}px")


# ---------------------------------------------------------------------------
# g3 — VISUAL-04 / E4-E5:竖条几何(遮挡 / 贴边 / 溢出)
# ---------------------------------------------------------------------------
# check-05 读的是 `.panel-header` 的 box-shadow 语义。inset 阴影画在元素**自身**
# 背景之上、内容/子元素之下 —— 一个带不透明背景的子元素压在左缘 3px 带上就会
# 把竖条吃掉,而 box-shadow 的 computed 值**一字不变**。D-17 把竖条从 `<section>`
# 挪到 `.panel-header` 正是为了躲这件事(三个 section 的子元素都带背景色)。
# 本断言把那条设计理由变成可失败的几何检查。
def _marker_geometry(page, panel_selector, long_title=False):
    return page.evaluate("""(args) => {
        const [panel, longTitle] = args;
        const header = document.querySelector(panel + ' .panel-header');
        if (!header) return {err: 'no .panel-header'};
        const h2 = header.querySelector('h2');
        if (longTitle && h2) h2.textContent = '超长标题'.repeat(40);
        const hr = header.getBoundingClientRect();
        const band = {l: hr.left, r: hr.left + 3, t: hr.top, b: hr.bottom};
        const occluders = [];
        for (const el of header.querySelectorAll('*')) {
            const cs = getComputedStyle(el);
            const bg = cs.backgroundColor;
            if (!bg || bg === 'rgba(0, 0, 0, 0)' || bg === 'transparent') continue;
            if (cs.display === 'none' || cs.visibility === 'hidden') continue;
            const r = el.getBoundingClientRect();
            if (r.right > band.l && r.left < band.r && r.bottom > band.t && r.top < band.b) {
                occluders.push({
                    sel: el.tagName + '.' + el.className, bg: bg,
                    left: r.left, width: r.width,
                });
            }
        }
        const h2r = h2 ? h2.getBoundingClientRect() : null;
        return {
            headerLeft: hr.left, headerWidth: hr.width,
            radiusTL: getComputedStyle(header).borderTopLeftRadius,
            h2Delta: h2r ? h2r.left - hr.left : null,
            scrollW: header.scrollWidth, clientW: header.clientWidth,
            shadow: getComputedStyle(header).boxShadow,
            occluders,
        };
    }""", [panel_selector, long_title])


def g3(page, tmp_root):
    item = "g3"
    print("\n=== g3: VISUAL-04 活动面板竖条几何(三态)===", flush=True)
    for state, panel in (("p1", "#session-panel"),
                         ("p3", "#annotations-panel"),
                         ("checking", "#checks-panel")):
        proj = c05.make_fixture(state, tmp_root)
        c05.enter_project(page, proj)
        geo = _marker_geometry(page, panel)
        if geo.get("err"):
            blocked(item, f"[{state}] {panel} 几何可读", "header 存在", geo["err"], "面板未渲染")
            continue
        info(f"g3 [{state}] {panel} 几何",
             f"radiusTL={geo['radiusTL']} h2Delta={geo['h2Delta']} "
             f"scrollW={geo['scrollW']} clientW={geo['clientW']}")
        ok_true(item, f"[{state}] {panel} 竖条 3px 带无被不透明子元素遮挡",
                len(geo["occluders"]) == 0, "0 个遮挡者", str(geo["occluders"]))
        ok_true(item, f"[{state}] {panel} 标题贴左缘且越过竖条(h2Delta >= 3)",
                geo["h2Delta"] is not None and geo["h2Delta"] >= 3,
                ">=3px", f"{geo['h2Delta']}px")
        ok_true(item, f"[{state}] {panel} 标题行不横向溢出",
                geo["scrollW"] <= geo["clientW"], "scrollW<=clientW",
                f"{geo['scrollW']}<={geo['clientW']}")

    # 长标题鲁棒性:标题变长不得把竖条挤掉、不得溢出
    proj = c05.make_fixture("p1", tmp_root)
    c05.enter_project(page, proj)
    base = _marker_geometry(page, "#session-panel")
    long = _marker_geometry(page, "#session-panel", long_title=True)
    if base.get("err") or long.get("err"):
        blocked(item, "[p1] 长标题几何可读", "header 存在", str(long.get("err")), "面板未渲染")
    else:
        ok_true(item, "[p1] 长标题下竖条声明未变",
                long["shadow"] == base["shadow"], base["shadow"], long["shadow"])
        ok_true(item, "[p1] 长标题下标题仍贴左缘(h2Delta >= 3)",
                long["h2Delta"] >= 3, ">=3px", f"{long['h2Delta']}px")
        ok_true(item, "[p1] 长标题下标题行不横向溢出",
                long["scrollW"] <= long["clientW"], "scrollW<=clientW",
                f"{long['scrollW']}<={long['clientW']}")
    # 透明记录:竖条与圆角的关系(见文件头「未覆盖」段)
    info("g3 圆角观察", f"border-top-left-radius={base.get('radiusTL')} —— inset 阴影沿圆角裁切,"
                        "竖条顶端在圆角过渡区收窄;是否「视觉断裂」属 E4/E5 人工判读项")


# ---------------------------------------------------------------------------
# g4 — VISUAL-05 / E6-E7:掩码字形不撑高行盒
# ---------------------------------------------------------------------------
# 差分测量:同一元素在 ::before 可见 / 被 display:none 抑制两种情形下的
# 布局高度。相等 ⇒ 12px 字形没有把行盒撑高。这是**行为**证据,不是「12px < 行高」
# 的算术推断。
def _linebox_delta(page, selector, glyph):
    return page.evaluate("""(args) => {
        const [sel, glyphSel] = args;
        const el = document.querySelector(sel);
        if (!el) return {err: 'no element'};
        const before = getComputedStyle(el, '::before');
        const withGlyph = el.getBoundingClientRect().height;
        if (withGlyph === 0) return {err: 'zero-height (宿主不可见)'};
        const st = document.createElement('style');
        st.textContent = glyphSel + '::before{display:none !important}';
        document.head.appendChild(st);
        const without = el.getBoundingClientRect().height;
        st.remove();
        const restored = el.getBoundingClientRect().height;
        return {
            withGlyph, without, restored,
            glyphH: before.height, glyphW: before.width,
            glyphVA: before.verticalAlign, glyphDisplay: before.display,
            lineHeight: getComputedStyle(el).lineHeight,
        };
    }""", [selector, glyph])


def g4(page, tmp_root):
    item = "g4"
    print("\n=== g4: VISUAL-05 掩码字形不撑高行盒 ===", flush=True)
    # .annotation-quote —— p3 + 写一条批注(真实渲染路径)
    proj = c05.make_fixture("p3", tmp_root)
    c05.write_annotations(proj, 2, [{
        "id": "g4-1", "quote": "建议进入授权环节", "before": "", "type": "comment",
        "note": "g4 探针批注正文", "status": "answered", "answer": "g4 探针回应",
        "created_at": "2026-09-19T00:00:00+00:00"}])
    c05.enter_project(page, proj)
    d = _linebox_delta(page, ".annotation-quote", ".annotation-quote")
    if d.get("err"):
        blocked(item, "g4 .annotation-quote 可测", "高度 > 0", d["err"], "批注引用行未渲染")
    else:
        info("g4 .annotation-quote", str(d))
        ok_true(item, "g4 .annotation-quote 字形不撑高行盒(差分高度相等)",
                d["withGlyph"] == d["without"], f"{d['withGlyph']}px",
                f"with={d['withGlyph']} without={d['without']}")
        ok_true(item, "g4 .annotation-quote 摘掉抑制样式后高度复原",
                d["restored"] == d["withGlyph"], f"{d['withGlyph']}px", f"{d['restored']}px")
        ok_true(item, "g4 .annotation-quote 字形为盒模型(display:inline-block,12×12)",
                d["glyphDisplay"] == "inline-block" and d["glyphH"] == "12px" and d["glyphW"] == "12px",
                "inline-block 12px/12px", f"{d['glyphDisplay']} {d['glyphW']}x{d['glyphH']}")

    # .verdict-location —— checking 样本下 #verdict-cards 可见
    proj = c05.make_fixture("checking", tmp_root)
    c05.enter_project(page, proj)
    rendered = page.evaluate("""() => {
        const host = document.querySelector('#verdict-cards');
        if (!host || typeof renderVerdictCard !== 'function') return false;
        host.innerHTML = '';
        host.appendChild(renderVerdictCard(
            {number: 1, location: 'g4 探针位置', issue: 'i', suggestion: 's'}, 'p2'));
        return !!host.querySelector('.verdict-location');
    }""")
    if not rendered:
        blocked(item, "g4 .verdict-location 可测", "裁决卡渲染出 .verdict-location", "<未渲染>",
                "renderVerdictCard(..., 'p2') 未产出目标元素")
    else:
        d2 = _linebox_delta(page, ".verdict-location", ".verdict-location")
        if d2.get("err"):
            blocked(item, "g4 .verdict-location 可测", "高度 > 0", d2["err"],
                    "#verdict-cards 在 checking 样本下应可见")
        else:
            info("g4 .verdict-location", str(d2))
            ok_true(item, "g4 .verdict-location 字形不撑高行盒(差分高度相等)",
                    d2["withGlyph"] == d2["without"], f"{d2['withGlyph']}px",
                    f"with={d2['withGlyph']} without={d2['without']}")
            ok_true(item, "g4 .verdict-location 字形为盒模型(display:inline-block,12×12)",
                    d2["glyphDisplay"] == "inline-block" and d2["glyphH"] == "12px",
                    "inline-block 12px/12px", f"{d2['glyphDisplay']} {d2['glyphW']}x{d2['glyphH']}")


# ---------------------------------------------------------------------------
# g5 — VISUAL-01 / E3:最窄面板 340px 下授权按钮单行不裁切
# ---------------------------------------------------------------------------
# 计划给的是一条**算术**(144px 标签 + 32px padding < 260px 内容宽),而 check-05
# 不把面板压到 340px 实测。本断言真的把 #doc-panel 压到 340px,再用 Range 数
# 文本行的 line box 数 —— 换行会产生第 2 个 rect。
def g5(page, tmp_root):
    item = "g5"
    print("\n=== g5: VISUAL-01/E3 最窄面板 340px 下 #btn-authorize 不换行不裁切 ===", flush=True)
    proj = c05.make_fixture("p3", tmp_root)
    c05.enter_project(page, proj)
    res = page.evaluate("""() => {
        const panel = document.querySelector('#doc-panel');
        const btn = document.querySelector('#btn-authorize');
        const row = document.querySelector('#authorize-row');
        if (!panel || !btn || !row) return {err: 'missing element'};
        if (row.classList.contains('hidden')) return {err: '#authorize-row 在 p3 被藏'};
        panel.style.flexBasis = '340px';
        panel.style.width = '340px';
        const pr = panel.getBoundingClientRect();
        const body = document.querySelector('#doc-panel-body');
        const br = btn.getBoundingClientRect();
        const range = document.createRange();
        range.selectNodeContents(btn);
        const rects = [...range.getClientRects()].map(r => ({w: r.width, h: r.height}));
        return {
            panelWidth: pr.width,
            bodyClientW: body.clientWidth,
            fontSize: getComputedStyle(btn).fontSize,
            btnWidth: br.width, btnHeight: br.height,
            scrollW: btn.scrollWidth, clientW: btn.clientWidth,
            lineBoxes: rects.length, rects,
        };
    }""")
    if res.get("err"):
        blocked(item, "g5 #btn-authorize 可测", "#authorize-row 可见", res["err"], "样本状态不满足")
        return
    info("g5 实测", str(res))
    ok_true(item, "g5 面板确已压到最窄值 340px",
            abs(res["panelWidth"] - 340) < 1, "340px", f"{res['panelWidth']}px")
    ok(item, "g5 #btn-authorize 字号为 var(--text-md) 的解析值(16px)",
       "16px", res["fontSize"])
    ok_true(item, "g5 文本单行(仅 1 个 line box)",
            res["lineBoxes"] == 1, "1", str(res["lineBoxes"]))
    ok_true(item, "g5 不横向裁切(scrollWidth <= clientWidth)",
            res["scrollW"] <= res["clientW"], "scrollW<=clientW",
            f"{res['scrollW']}<={res['clientW']}")
    ok_true(item, "g5 按钮宽度不超出面板内容宽",
            res["btnWidth"] <= res["bodyClientW"], f"<={res['bodyClientW']}px",
            f"{res['btnWidth']}px")


# ---------------------------------------------------------------------------
# g6 — VISUAL-04:#ai-panel 折叠点击穿透(行为不变)
# ---------------------------------------------------------------------------
# VERIFICATION 的 human_verification #6 原文:「没有任何测试**执行**这次切换」。
# 本断言就是那次执行:点折叠指示器 → .collapsed 切换 / 面板体 display:none /
# 字形 ▾↔▸ / 标题行 box-shadow 恒为 none(新增的两条标记规则不匹配 #ai-panel)。
def _collapse_roundtrip(page, header_sel, body_sel, target_sel):
    """点标题行 → 观察 .collapsed 落在**哪一个**元素上、面板体显隐、字形、竖条。

    target_sel 必须显式给出:`#ai-panel-header` 的处理器把 `.collapsed` 加在
    `#ai-panel-body` 上,而 `#doc-panel-header` 的处理器加在 `#doc-panel`(aside)上 ——
    两者不同形,猜错目标会让断言假 FAIL(本 harness 首跑即踩过)。"""
    return page.evaluate("""(args) => {
        const [hsel, bsel, tsel] = args;
        const hdr = document.querySelector(hsel);
        if (!hdr) return {err: 'no header'};
        const body = document.querySelector(bsel);
        const target = document.querySelector(tsel);
        if (!target) return {err: 'no toggle target: ' + tsel};
        const ind = hdr.querySelector('.collapse-indicator');
        const snap = () => ({
            toggled: target.classList.contains('collapsed'),
            display: body ? getComputedStyle(body).display : null,
            indicator: ind ? ind.textContent : null,
            headerShadow: getComputedStyle(hdr).boxShadow,
        });
        const before = snap();
        (ind || hdr).click();
        const afterFirst = snap();
        (ind || hdr).click();
        const afterSecond = snap();
        return {before, afterFirst, afterSecond};
    }""", [header_sel, body_sel, target_sel])


def g6(page, tmp_root):
    item = "g6"
    print("\n=== g6: VISUAL-04 #ai-panel 折叠点击穿透 ===", flush=True)
    proj = c05.make_fixture("p1", tmp_root)
    c05.enter_project(page, proj)
    r = _collapse_roundtrip(page, "#ai-panel-header", "#ai-panel-body", "#ai-panel-body")
    if r.get("err"):
        blocked(item, "g6 #ai-panel-header 存在", "header", r["err"], "面板未渲染")
    else:
        info("g6 #ai-panel", str(r))
        ok_true(item, "g6 初始态未折叠且面板体可见",
                r["before"]["toggled"] is False and r["before"]["display"] != "none",
                "collapsed=False display!=none", str(r["before"]))
        ok_true(item, "g6 首次点击 → .collapsed 生效、面板体 display:none",
                r["afterFirst"]["toggled"] is True and r["afterFirst"]["display"] == "none",
                "collapsed=True display=none", str(r["afterFirst"]))
        ok_true(item, "g6 首次点击 → 指示器字形切到 ▸",
                r["afterFirst"]["indicator"] == "▸", "▸", str(r["afterFirst"]["indicator"]))
        ok_true(item, "g6 二次点击 → 复原(折叠态解除、面板体可见、字形 ▾)",
                r["afterSecond"]["toggled"] is False
                and r["afterSecond"]["display"] != "none"
                and r["afterSecond"]["indicator"] == "▾",
                "collapsed=False display!=none ▾", str(r["afterSecond"]))
        ok_true(item, "g6 折叠/展开全程标题行无竖条(box-shadow 恒 none)",
                r["before"]["headerShadow"] == "none"
                and r["afterFirst"]["headerShadow"] == "none"
                and r["afterSecond"]["headerShadow"] == "none",
                "none ×3", f"{r['before']['headerShadow']} / {r['afterFirst']['headerShadow']} / {r['afterSecond']['headerShadow']}")

    # 同形消费者:#doc-panel-header(.collapsed 加在 #doc-panel 自身)
    r2 = _collapse_roundtrip(page, "#doc-panel-header", "#doc-panel-body", "#doc-panel")
    if r2.get("err"):
        blocked(item, "g6 #doc-panel-header 存在", "header", r2["err"], "面板未渲染")
    else:
        ok_true(item, "g6 文档面板折叠往返一致(#doc-panel.collapsed 切换、正文隐藏)",
                r2["afterFirst"]["toggled"] is True
                and r2["afterFirst"]["display"] == "none"
                and r2["afterSecond"]["toggled"] is False
                and r2["afterSecond"]["display"] != "none",
                "True/none → False/可见", str(r2["afterFirst"]) + " → " + str(r2["afterSecond"]))
        ok_true(item, "g6 文档面板标题行无竖条(box-shadow 恒 none)",
                r2["before"]["headerShadow"] == "none" and r2["afterFirst"]["headerShadow"] == "none",
                "none", r2["afterFirst"]["headerShadow"])


ITEMS = {"g1": g1, "g2": g2, "g3": g3, "g4": g4, "g5": g5, "g6": g6}


def parse_args():
    ap = argparse.ArgumentParser(add_help=True, description="idi-05 Nyquist 缺口补齐 harness")
    ap.add_argument("--item", action="append", default=None,
                    help="只跑指定项:g1 / g2 / g3 / g4 / g5 / g6(可重复,或逗号分隔)")
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
    tmp_root = Path(tempfile.mkdtemp(prefix="idi05-gap-"))
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

    print("\n=== 逐项结论 ===", flush=True)
    verdicts = {}
    for i in items:
        v = c05.item_verdict(i)
        verdicts[i] = v
        rows = [r for r in c05.ROWS if r["item"] == i]
        fails = len([r for r in rows if r["verdict"] == "FAIL"])
        blocks = len([r for r in rows if r["verdict"] == "BLOCKED"])
        print(f"item {i}: {v.upper()}  ({len(rows)} 条断言,{fails} FAIL,{blocks} BLOCKED)", flush=True)
    any_fail = any(v == "fail" for v in verdicts.values())
    any_blocked = any(v == "blocked" for v in verdicts.values())
    code = 1 if any_fail else (2 if any_blocked else 0)
    print(f"\nexit={code}  (0=全 pass,1=有 fail,2=有 blocked)", flush=True)
    return code


if __name__ == "__main__":
    sys.exit(main())
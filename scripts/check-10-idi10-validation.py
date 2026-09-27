#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check-10-idi10-validation.py — Phase 10「表格重做」的运行时门(骨架 + t1 / t2)。

为什么另开一个文件
    规划期 grep 了全部 7 个门脚本 + 2 个探针,**没有任何一条**断言文档区表格的
    边框 / 底色 / 布局:
      - `check-01-token-conformance.sh`  只数围栏外的裸 hex 与 tier-1 原语引用
      - `check-02-contrast.py`           只算 PAIR 清单上的对比度比值
      - `check-03-hidden-uniqueness.sh`  只数 `.hidden {` 规则条数
      - `check-04-important-count.sh`    只数 `!important;` 声明条数
      - `check-05-ui-uat.py`             唯一的接触点是 `[p1] .markdown-body td font-size`
                                         那一条 —— 它断言的**不是**本阶段改的属性
                                         (border / background),且期望侧由
                                         `resolve_token` 运行时解析 ⇒ 值层不改就恒过
      - `check-06` / `check-07` / `check-09` 与两个 probe 对本阶段改动的属性零断言
    ⇒ TABLE-01 / TABLE-02 的渲染判据在本文件之前**零自动化覆盖**。全部断言是真实
    浏览器里的 `getComputedStyle` 读数,不是源码文本匹配:表格是**画出来**的,
    文本里写着 `background` 不等于浏览器里真的生效。

与 check-05 的关系
    复用 check-05 的模块级设施(服务生命周期 `ensure_server` / fixture 隔离
    `make_fixture` / `enter_project` / 断言记录器 `ok` / `ok_true` / `blocked` /
    `info` / 令牌解析 `resolve_color` / `resolve_token` / 读数器 `read_style` /
    归一化 `norm` / 样本清单 `STATES`),不重复实现,**也不改动 check-05 一行** ——
    它在 `idi-08` 的 `covered_files` 里,改它会把连带指纹的重验面从 1 份变成 2 份。

运行方式
    .venv/bin/python scripts/check-10-idi10-validation.py --item t1
    .venv/bin/python scripts/check-10-idi10-validation.py --item t1,t2
    .venv/bin/python scripts/check-10-idi10-validation.py --item t1 --item t2 --json
    .venv/bin/python scripts/check-10-idi10-validation.py --screenshot <DIR>
    .venv/bin/python scripts/check-10-idi10-validation.py --keep

退出码语义(与 check-05 一致)
    0 = 全 pass;1 = 至少一条 FAIL;2 = 无 FAIL 但至少一条 BLOCKED

断言与需求的映射
    t1 → TABLE-01 / TABLE-02   `.markdown-body th`:计算底色 == --color-surface
                                (gray-2),下边线 1px solid == --color-border-subtle,
                                left / right / top 三条边 0px,外加 padding 与
                                font-size 两条对照组
    t2 → TABLE-01 / TABLE-02   `.markdown-body td`:left / right / top 三条边 0px
                               (ROADMAP SC1 对「不再有竖线与外框」的逐字操作定义),
                               下边线 1px solid == --color-border-subtle,外加
                               font-size(被 check-05 锁死的属性)与 padding 两条对照组
    shot                          逐样本整窗截图(供用户评审;计划 03 直接消费)

「造出容器再断言」+ 两个独立读数(本文件的核心纪律)
    每个 (样本, 宿主) 对在读数前都用**应用自身的 `renderMarkdown`** 把一段含表头与
    数据格的最小 markdown 注入该宿主(与 `check-05-ui-uat.py` 的 item4 同款手法:
    真实渲染路径、零网络、零 AI 调用)。规划期逐样本实测:`scripts/ui-states/p1/`
    只有 `.gitkeep`,p12 / checking / archive 的文档表格行数**全部为 0**,故靠
    「哪个宿主本来就有表」选点会把门退化成**单点门** —— 本项目已登记过这条漏检教训。

    注入只保证**元素存在**;**是否被渲染**是另一个独立事实,必须在同一次
    `page.evaluate` 里沿宿主自身的祖先链判 `display` 采集。隐藏子树上的读数照常返回
    **解析值**(计算样式与 `display` 无关),故「注入成功」完全推不出「被渲染」——
    这正是 `idi-06` 已登记的同型陷阱(被祖先藏住的元素 `getBoundingClientRect()`
    全零,而基于存在性的断言照常 PASS)。两类证据分开陈述:
      · 渲染证据    —— 宿主处于被渲染子树中(rendered 为真)
      · 层叠解析证据 —— 宿主被祖先 display:none 藏住(rendered 为假)
    两个断言集各自含一条聚合断言「至少 1 个对处于被渲染子树」,使「零渲染证据」
    可失败,而不是只写在散文里。

浏览器路线(实测结论,不是偏好)
    固定走 Playwright 自带 chromium + 无头。本机 `channel="chrome"` + headless 会
    CDP 挂死(见 check-05 / check-09 文件头的实测记录),故本文件不提供 `--browser`。
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import struct
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK05 = ROOT / "scripts" / "check-05-ui-uat.py"
STYLE_CSS = ROOT / "frontend" / "style.css"

FENCE_START = "===== DESIGN TOKENS: START ====="
FENCE_END = "===== DESIGN TOKENS: END ====="

# gray-2 的字面量:表头新绘制面上的断言**两侧都写死**。若两侧都从同一个令牌解析,
# 令牌被改坏(而消费者仍接着线)也照样 PASS —— 那条接线的价值就消失了。
TH_BG_LITERAL = "rgb(249, 249, 249)"

# 每个 (样本, 宿主) 对。覆盖 check-05 的 MARKDOWN_HOSTS **全部四个** doc 宿主
# (p1 下四个都在 DOM),外加一对自然渲染样本 (p3, #round-doc) —— 该样本渲染
# `scripts/ui-states/p3/docs/discuss-round-2.md`,含 SC1 点名的机器可解析表。
#
# 这 5 个对**不是等价证据**:四个 doc 宿主在 p1 下多数处于隐藏子树(例如
# #brainstorm-content 的祖先 #brainstorm-view 初始即带 .hidden,#latest-check 的祖先
# #checks-panel 在阶段 1-2 也是 .hidden),它们承载的是**层叠解析**覆盖;只有处于
# 被渲染子树中的对,其读数才构成**渲染证据**。哪些属于后者由运行时显示性读数当场
# 决定,不预先写死。对数是 5,不因证据分类而减。
TABLE_PROBES = (
    ("p1", "#draft-content"),
    ("p1", "#brainstorm-content"),
    ("p1", "#round-doc"),
    ("p1", "#latest-check"),
    ("p3", "#round-doc"),
)

# 含表头 + 至少一行数据格的最小 markdown。走 marked ⇒ <thead><tr><th> + <tbody><tr><td>。
TABLE_PROBE_MD = (
    "| 探针表头甲 | 探针表头乙 | 探针表头丙 |\n"
    "| --- | --- | --- |\n"
    "| 探针数据一 | 探针数据二 | 探针数据三 |\n"
    "| 探针数据四 | 探针数据五 | 探针数据六 |\n"
)

# 表格规则的 padding 是 `var(--space-1) var(--space-2-5)`,Chrome 序列化为 4px 10px。
TH_TD_PADDING = "4px 10px"


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
norm = c05.norm


def fence_text():
    """返回两行 `===== DESIGN TOKENS: START/END` 之间的文本(含标记行自身)。"""
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
# 探针:注入 + 两个独立读数(注入成功 / 是否被渲染)
# ---------------------------------------------------------------------------
# 一次 page.evaluate 里做完三件事,使「元素存在」与「被渲染」两个事实各自可见:
#   1. 注入 —— 清空宿主,append 应用自身 renderMarkdown(探针 markdown)的产物
#   2. 注入成功读数 —— 注入后宿主内的 th / td 计数
#   3. 显示性读数 —— 沿宿主自身的祖先链(含宿主)找首个 display:none 的祖先
# `hidden_by` 报出那个祖先的 id / class / 标签名,便于在隐藏子树的情形下定位。
_PROBE_JS = """([sel, md]) => {
  const host = document.querySelector(sel);
  if (!host) return {error: 'host-not-found'};
  if (typeof renderMarkdown !== 'function') return {error: 'renderMarkdown-unavailable'};
  host.innerHTML = '';
  host.appendChild(renderMarkdown(md));
  const th = host.querySelectorAll('th').length;
  const td = host.querySelectorAll('td').length;
  let el = host, hiddenBy = null;
  while (el) {
    if (getComputedStyle(el).display === 'none') {
      hiddenBy = el.id ? '#' + el.id
        : ((typeof el.className === 'string' && el.className.trim())
           ? '.' + el.className.trim().split(/\\s+/).join('.')
           : el.tagName.toLowerCase());
      break;
    }
    el = el.parentElement;
  }
  return {th: th, td: td, rendered: hiddenBy === null, hidden_by: hiddenBy};
}"""


def run_probe_pairs(page, tmp_root, item, assert_pair, on_entered=None):
    """遍历 `TABLE_PROBES`:按样本分组,注入探针表后**就地**跑该对的两条读数与断言。

    为什么必须就地(不是先收集、再断言):`enter_project` 会 `page.goto` 重新导航,
    上一个 fixture 里注入的 DOM 会被整体丢掉。滞后读会读到已清空的宿主 —— 那是
    **探针缺陷**,不是产品缺陷,但它会让整份读数静默退化成 `<MISSING>`,把一次
    真实的 PASS 变成满屏 BLOCKED(首跑实测过这条)。

    `on_entered(page)` 在**第一次**进入 fixture 之后、任何读数之前调用一次 ——
    令牌解析必须落在这个时点:页面还在 `about:blank` 时 `documentElement` 上
    没有任何 CSS 自定义属性,`resolve_color` / `resolve_token` 一律返回 `None`。

    返回 `(rendered, hidden)`:两个列表各含 `(sample, host, hidden_by)`。
    """
    rendered, hidden = [], []
    first = True
    for sample in dict.fromkeys(s for s, _h in TABLE_PROBES):
        proj = c05.make_fixture(sample, tmp_root)
        c05.enter_project(page, proj)
        if first:
            first = False
            if on_entered is not None:
                on_entered(page)
        for probe_sample, host in TABLE_PROBES:
            if probe_sample != sample:
                continue
            pair = f"[{sample}] {host}"
            reading = page.evaluate(_PROBE_JS, [host, TABLE_PROBE_MD])
            if not isinstance(reading, dict) or reading.get("error"):
                reason = reading.get("error") if isinstance(reading, dict) else str(reading)
                blocked(item, f"{pair} 探针注入与读数可读", "注入成功且读数可读",
                        str(reading), f"注入失败:{reason} ⇒ 探针跑不起来,绝不记 PASS")
                continue
            # 两个事实必须各自可见,不合并成一句「已注入」。
            info(f"{item} {pair} 注入与显示读数",
                 f"注入后 th={reading['th']} td={reading['td']} / "
                 f"处于被渲染子树={reading['rendered']} / 藏住它的祖先={reading['hidden_by']}")
            ok_true(item, f"{pair} 注入成功:注入后 td 计数 > 0", reading["td"] > 0,
                    "td 计数 > 0", f"th={reading['th']} td={reading['td']}",
                    note="每个对都在读数前用应用自身的 renderMarkdown 注入过探针表 —— "
                         "造出容器再断言,不依赖 fixture 自然渲染")
            if reading["rendered"]:
                rendered.append((sample, host, reading["hidden_by"]))
            else:
                hidden.append((sample, host, reading["hidden_by"]))
            assert_pair(pair, host)
    return rendered, hidden


def render_evidence_assertion(item, rendered, hidden):
    """聚合断言:至少 1 个对处于被渲染子树(渲染证据存在)。

    使「零渲染证据」可失败 —— 否则隐藏子树上的层叠读数会被读成渲染证据,
    那正是本项要修的失真。
    """
    detail = "rendered=" + (", ".join(f"({s}, {h})" for s, h, _b in rendered) or "无")
    detail += " / hidden=" + (", ".join(f"({s}, {h})<-{b}" for s, h, b in hidden) or "无")
    info(f"{item} 证据分类",
         f"渲染证据 {len(rendered)} 个对 / 层叠解析证据 {len(hidden)} 个对 —— {detail}")
    ok_true(item, f"{item} [聚合] 至少 1 个 (样本, 宿主) 对处于被渲染子树",
            len(rendered) >= 1, ">= 1 个 rendered=True",
            f"rendered {len(rendered)}/{len(TABLE_PROBES)} 个对;{detail}",
            note="为真 ⇒ 其上的读数构成渲染证据;其余对(被祖先 display:none 藏住)上的"
                 "读数只能陈述为层叠解析证据,不得当作渲染证据")


# ---------------------------------------------------------------------------
# t1 — .markdown-body th:表头浅底 + 1px 下边线(TABLE-01)
# ---------------------------------------------------------------------------
def t1(page, tmp_root):
    item = "t1"
    print("\n=== t1: .markdown-body th — 表头浅底 + 1px 下边线(TABLE-01)===", flush=True)
    tokens = {}

    def on_entered(page):
        tokens["surface"] = resolve_color(page, "--color-surface")
        tokens["subtle"] = resolve_color(page, "--color-border-subtle")
        tokens["base_size"] = resolve_token(page, "--text-base")
        info("t1 令牌解析",
             f"--color-surface={tokens['surface']} "
             f"--color-border-subtle={tokens['subtle']} "
             f"--text-base={tokens['base_size']}")
        ok(item, "t1 [令牌] --color-surface 解析值 == gray-2 字面量", TH_BG_LITERAL,
           tokens["surface"],
           note="令牌级断言:两侧都写死,防止「令牌被改坏而消费者仍接线」时假绿")
        ok_true(item, "t1 [令牌] --color-border-subtle 解析值 != --color-surface(两档不塌)",
                tokens["subtle"] != tokens["surface"] and tokens["subtle"] is not None,
                f"!= {tokens['surface']}", str(tokens["subtle"]),
                note="行间线必须比表头绘制面深一档,否则分隔线消失")

    def assert_pair(pair, host):
        ok(item, f"{pair} .markdown-body th 计算 background-color == var(--color-surface)",
           tokens["surface"], read_style(page, f"{host} th", "background-color"),
           note="表头浅底落三级刻度的「内陷面」档(D-10-1);HEAD 上 th 无自身底色(透明)")
        ok(item, f"{pair} .markdown-body th 计算 border-bottom-width == 1px", "1px",
           read_style(page, f"{host} th", "border-bottom-width"))
        ok(item, f"{pair} .markdown-body th 计算 border-bottom-style == solid", "solid",
           read_style(page, f"{host} th", "border-bottom-style"))
        ok(item, f"{pair} .markdown-body th 计算 border-bottom-color == var(--color-border-subtle)",
           tokens["subtle"], read_style(page, f"{host} th", "border-bottom-color"),
           note="表头下边线与行间分隔线同档,不再是原 --color-border(gray-7)的深线")
        for side in ("left", "right", "top"):
            ok(item, f"{pair} .markdown-body th 计算 border-{side}-width == 0px", "0px",
               read_style(page, f"{host} th", f"border-{side}-width"),
               note="去掉竖线与外框(ROADMAP SC1)")
        # 对照组:证明没顺手改别的属性。
        ok(item, f"{pair} .markdown-body th 计算 padding == {TH_TD_PADDING}(对照组)",
           TH_TD_PADDING, read_style(page, f"{host} th", "padding"))
        ok(item, f"{pair} .markdown-body th 计算 font-size == var(--text-base)(对照组)",
           tokens["base_size"], read_style(page, f"{host} th", "font-size"))

    rendered, hidden = run_probe_pairs(page, tmp_root, item, assert_pair, on_entered)
    render_evidence_assertion(item, rendered, hidden)


# ---------------------------------------------------------------------------
# t2 — .markdown-body td:三条边 0px + 行间浅线(TABLE-01 / TABLE-02)
# ---------------------------------------------------------------------------
def t2(page, tmp_root):
    item = "t2"
    print("\n=== t2: .markdown-body td — 三条边 0px + 行间浅线(TABLE-01)===", flush=True)
    tokens = {}

    def on_entered(page):
        tokens["subtle"] = resolve_color(page, "--color-border-subtle")
        tokens["base_size"] = resolve_token(page, "--text-base")
        info("t2 令牌解析",
             f"--color-border-subtle={tokens['subtle']} --text-base={tokens['base_size']}")

    def assert_pair(pair, host):
        for side in ("left", "right", "top"):
            ok(item, f"{pair} .markdown-body td 计算 border-{side}-width == 0px", "0px",
               read_style(page, f"{host} td", f"border-{side}-width"),
               note="HEAD 上是 1px —— 这是 ROADMAP SC1 对「不再有竖线与外框」的逐字操作定义")
        ok(item, f"{pair} .markdown-body td 计算 border-bottom-width == 1px", "1px",
           read_style(page, f"{host} td", "border-bottom-width"))
        ok(item, f"{pair} .markdown-body td 计算 border-bottom-style == solid", "solid",
           read_style(page, f"{host} td", "border-bottom-style"))
        ok(item, f"{pair} .markdown-body td 计算 border-bottom-color == var(--color-border-subtle)",
           tokens["subtle"], read_style(page, f"{host} td", "border-bottom-color"),
           note="行间极浅分隔线(gray-6);border-collapse 把它与上一行折成一条,不出现双线")
        # 对照组:font-size 是 check-05-ui-uat.py 活断言锁死的属性,本阶段一字不动。
        ok(item, f"{pair} .markdown-body td font-size == var(--text-base)(对照组,check-05 锁死)",
           tokens["base_size"], read_style(page, f"{host} td", "font-size"),
           note="check-05-ui-uat.py 的 [p1] .markdown-body td font-size 活断言;改它就红")
        ok(item, f"{pair} .markdown-body td 计算 padding == {TH_TD_PADDING}(对照组)",
           TH_TD_PADDING, read_style(page, f"{host} td", "padding"))

    rendered, hidden = run_probe_pairs(page, tmp_root, item, assert_pair, on_entered)
    render_evidence_assertion(item, rendered, hidden)


# ---------------------------------------------------------------------------
# shot — 逐样本整窗截图(供用户评审;不参与表格判据)
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


ITEMS = {"t1": t1, "t2": t2}


def parse_args():
    ap = argparse.ArgumentParser(add_help=True, description="Phase 10 表格重做的运行时门")
    ap.add_argument("--item", action="append", default=None,
                    help="只跑指定项:t1 / t2(可重复,或逗号分隔)")
    ap.add_argument("--screenshot", default=None, metavar="DIR",
                    help="遍历 check-05 的 5 个样本,每个样本出一张 1440x900 整窗截图到 DIR")
    ap.add_argument("--json", action="store_true",
                    help="把断言记录(c05.ROWS)全量序列化为 JSON 打到 stdout,供机器消费")
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

    # --json 时把人类可读输出改道 stderr,使 stdout 是一份可被 json.loads 解析的纯 JSON。
    real_stdout = sys.stdout
    if args.json:
        sys.stdout = sys.stderr

    server = c05.ensure_server()
    tmp_root = Path(tempfile.mkdtemp(prefix="idi-10-gate-"))
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

    if args.json:
        sys.stdout = real_stdout
        print(json.dumps(c05.ROWS, ensure_ascii=False, indent=2), flush=True)
    return code


if __name__ == "__main__":
    sys.exit(main())

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
    .venv/bin/python scripts/check-05-ui-uat.py                 # 跑 UAT 第 1..9 项
    .venv/bin/python scripts/check-05-ui-uat.py --item smoke    # 只跑 harness 自检切片
    .venv/bin/python scripts/check-05-ui-uat.py --item 7        # 只跑渲染目标的标题刻度
    .venv/bin/python scripts/check-05-ui-uat.py --item 8        # 只跑 sticky 表头 / 流内 badge
    .venv/bin/python scripts/check-05-ui-uat.py --item 9        # 只跑面板区滚动容器收敛
    .venv/bin/python scripts/check-05-ui-uat.py --item 1 --item 2
    .venv/bin/python scripts/check-05-ui-uat.py --ai-smoke      # 额外真跑两次 AI 交互冒烟
    .venv/bin/python scripts/check-05-ui-uat.py --keep          # 保留临时工作目录供排查
    .venv/bin/python scripts/check-05-ui-uat.py --browser chrome  # 改用系统 Chrome(有头)

第 9 项(L-4 / D-14)
    面板区的滚动容器从「3 个嵌套 + 1 个外层」收敛为「1 个外层(`#main-pane`)+ 1 个被
    保留的内层(`#latest-check`)+ 1 个 SC#3 明文豁免的会话流滚动者(`#chat-messages`)」。
    三项断言:滚动者集合按 **DOM 遍历**普查恰为三者(排除豁免后恰为两者)、
    `#main-pane` 与 `#latest-check` 滚到底后末条内容可达、`#ai-events` 与
    `#annotation-list` 的计算 `max-height` 为 `none`。另含两条**保留项护栏**:
    `#chat-messages` 的 `overflow-y == auto`(计算样式)、`#latest-check` 的
    `max-height: 30vh;` 按**源码文本计数 == 1**(计算样式对 `vh` 返回 px 用值,
    断言 `== "30vh"` 会恒 FAIL)。可达性断言各带**前提检查**(容器可见且 rect 高 > 0),
    前提不成立记 BLOCKED 而非 PASS。

第 8 项(L-1 / D-06)
    文档面板标题行从「随面板内容滚走」改为「钉在面板顶部」(`#doc-panel-header` 新增
    `position: sticky`)。三项断言:badge 仍是流内元素(computed position == static)、
    768 / 1024 / 1280 三处 badge × banner 的 rect 不相交、滚动 `#doc-panel` 到底后表头仍可见。
    两条几何断言各带**前提检查**(元素可见且 rect 非全零 / 容器真的可滚),前提不成立记
    BLOCKED 而非 PASS —— 与第 7 项 `all(w != "700")` 对 None 恒真是同型陷阱。
    本项还产出三项**只读诊断**(三宽度文档级 scrollWidth / L-5 clearance 普查 /
    L-6 命中区普查),经 `info()` 输出、不参与判定 —— 它们是后续计划决策的原始输入。
    本项是 harness 里**第一次**变更 viewport,结束前必须复位到 1440×900。

第 7 项(G-idi-05-1)
    `renderMarkdown()` 的返回值被注入**五个不是 `.markdown-body`** 的容器
    (`.event-content` / `.chat-bubble` / `.say-chunk` / `.annotation-note` /
    `.annotation-answer-body`),而标题尺寸规则此前只存在于 `.markdown-body` 作用域内,
    故这些容器里的 h1/h2/h3 全部回落 UA 默认值(`.chat-bubble` 上下文 32px、
    `.event-content` 上下文 28px,字重一律 700)。第 7 项用应用自身的四个渲染函数
    **造出这五个容器再断言**(容器造不出记 BLOCKED,绝不记 PASS),并含一条**静态普查守卫**:
    `frontend/app.js` 的 `renderMarkdown(` 计数一变即 FAIL,强制 `MARKDOWN_TARGETS` 跟上。
    枚举纪律是**按调用点,不按类名** —— 只枚举四个 `.markdown-body` 宿主正是该缺陷存活的直接原因。

退出码语义
    0 = 所选项全部 pass
    1 = 至少一项含 FAIL 断言
    2 = 无 FAIL,但至少一项含 BLOCKED 断言(状态造不出 / 元素不可见 / 选择器不存在 / 期望值解析不出)

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

    expected 为 None 表示**期望值解析不出**(如令牌未声明)→ 同样记 BLOCKED。
    不加这一支它会落进下面的比较分支:norm(actual) == norm(None) 恒为假,于是
    记 FAIL —— FAIL 也不是假 PASS,但「期望值本身不可得」与「值不相等」是两种
    状态,混为一谈会让诊断指向错误的方向。两类 BLOCKED 的区别:actual 侧是读不到
    (元素/选择器不存在),expected 侧是解析不出(令牌未声明或解析失败)。

    比较前对 rgb()/rgba() 内部空白做归一:UAT 里写 `rgb(106,106,106)`,
    Chrome 序列化成 `rgb(106, 106, 106)` —— 这是序列化差异,不是产品差异。
    打印的仍是原始 actual,失败可独立诊断。
    """
    if expected is None:
        _emit(item, "BLOCKED", label, "<UNRESOLVED>", actual, "令牌未声明或期望值解析失败")
    elif actual is None:
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


_PSEUDO_READ_JS = """([sel, pseudo, prop]) => {
  const el = document.querySelector(sel);
  if (!el) return null;
  const v = getComputedStyle(el, pseudo)[prop];
  return (v === undefined || v === null) ? null : v;
}"""


def read_pseudo_style(page, selector, pseudo, prop):
    """读伪元素的 computed style。

    既有的 read_style 只接受 (selector, prop),拿不到伪元素,故另开一个读取器。
    元素本身不存在时返回 None → 调用方记 BLOCKED,绝不记 PASS。"""
    return page.evaluate(_PSEUDO_READ_JS, [selector, pseudo, prop])


def check_mask_glyph(page, item, label_prefix, selector, icon_token):
    """两处内联掩码字形(VISUAL-05 / D-20 / D-21 / D-22)的四条运行时断言。

    机制是 mask-image + background-color(不是 content: url(...)),故产物是一个
    **盒模型**:尺寸 12×12、底色跟随 --color-text-secondary 令牌、mask-image 接上围栏
    内的 data-URI 令牌。伪元素未渲染时四条一起记 BLOCKED,绝不记 PASS。
    """
    pseudo = "::before"
    width = read_pseudo_style(page, selector, pseudo, "width")
    height = read_pseudo_style(page, selector, pseudo, "height")
    bg = read_pseudo_style(page, selector, pseudo, "background-color")
    mask = read_pseudo_style(page, selector, pseudo, "mask-image")
    if width is None or height is None or bg is None or mask is None:
        blocked(
            item,
            f"{label_prefix} {selector}{pseudo} mask 盒模型",
            "12px / 12px / <--color-text-secondary> / mask-image != none",
            f"width={width} height={height} background-color={bg} mask-image={mask}",
            "伪元素未渲染(元素不存在或 ::before 未生成)",
        )
        return
    ok(item, f"{label_prefix} {selector}{pseudo} width", "12px", width)
    ok(item, f"{label_prefix} {selector}{pseudo} height", "12px", height)
    ok(
        item,
        f"{label_prefix} {selector}{pseudo} background-color == var(--color-text-secondary)",
        resolve_color(page, "--color-text-secondary"),
        bg,
    )
    info(f"{label_prefix} {selector}{pseudo} mask-image 原始值", repr(mask))
    ok_true(
        item,
        f"{label_prefix} {selector}{pseudo} mask-image 接上 var({icon_token})",
        mask != "none",
        "!=none",
        mask,
    )


# --- 三段坡道(D-04 的反转形态,Plan 02)------------------------------------
# 六只动作按钮按「不可逆程度」分三档。档内三属性必须逐字节相同(它能抓到「改错了一只」),
# 三档之间必须两两不同(它守卫的是核心价值红线:授权绝不与例行混同)。
# 六只按钮全部常驻 DOM;getComputedStyle 对 display:none 的元素仍返回解析后的
# color / border-color / background-color(它们不依赖布局),故一个 p3 样本就够。
ROUTINE = ("#btn-process-round", "#btn-continue-check", "#btn-continue-repair")
COMMIT = ("#btn-approve-draft", "#btn-start-writing")
IRREVERSIBLE = ("#btn-authorize",)


def trio(page, selector):
    """一只按钮的三属性读数:(color, border-top-color, background-color)。

    与 parse_box_shadow / check_frozen_marker 同构 —— 比较的是解析后的语义值,
    不是选择器文本或子串全等。"""
    return (
        read_style(page, selector, "color"),
        read_style(page, selector, "border-top-color"),
        read_style(page, selector, "background-color"),
    )


def read_classlist(page, selector):
    return page.evaluate(
        "(sel) => { const el = document.querySelector(sel); return el ? [...el.classList] : null; }",
        selector,
    )


def resolve_color(page, token):
    """把令牌解析成归一化的 computed rgb —— 挂一个探针元素读它的 color。

    令牌**未声明**时返回 `None`(与 resolve_token 同形),不再返回探针继承到的
    正文色。故先确认 `documentElement` 上该令牌确有声明:为空即直接返回,不进
    探针。否则 `var(--t)` 在 computed-value 阶段失效,探针与真实消费者(用同一个
    `var(--t)`)会一起退化成同一个继承值 —— 断言在令牌改名/删除下恒真。
    """
    return page.evaluate(
        """(t) => {
            const declared = getComputedStyle(document.documentElement).getPropertyValue(t);
            if (!declared || !declared.trim()) return null;
            const p = document.createElement('div');
            p.style.color = `var(${t})`;
            document.body.appendChild(p);
            const c = getComputedStyle(p).color;
            p.remove();
            return c;
        }""",
        token,
    )


def resolve_token(page, name):
    """把任意令牌解析成它的运行时值(字符串)——
    与 resolve_color 并列:后者只能解析颜色,而 --z-badge 是数字、--shadow-*
    是多段阴影,探针 color 读不出它们。"""
    return page.evaluate(
        """(t) => {
            const v = getComputedStyle(document.documentElement).getPropertyValue(t);
            return v ? v.trim() : null;
        }""",
        name,
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
# D-14:冻结轮的琥珀色不再硬编码 —— 期望侧由 resolve_color(page, "--color-action-warning")
# 在运行时解析。原先那个模块常量(及其三处字面串)已整体删除:
# 它是「值层一改就产生假 FAIL」这条单条根因在 check_frozen_marker 里的那一份。


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
    # D-14:期望侧来自运行时解析的令牌(值层的仲裁者是 check-02-contrast.py,不是本 harness)
    frozen_amber = resolve_color(page, "--color-action-warning")
    info(f"{label_prefix} 令牌解析 --color-action-warning", frozen_amber)
    expected_shadow = f"inset 3px 0 0 {frozen_amber}"
    parsed = parse_box_shadow(raw) if raw else None
    if parsed is None or frozen_amber is None:
        blocked(
            item,
            f"{label_prefix} 冻结轮 box-shadow 语义",
            expected_shadow,
            raw,
            "box-shadow 缺失或无法解析,或 --color-action-warning 解析失败",
        )
    else:
        semantic_ok = (
            parsed["inset"]
            and parsed["x"] == "3px"
            and parsed["y"] == "0px"
            and parsed["blur"] == "0px"
            and parsed["spread"] == "0px"
            and norm(parsed["color"]) == norm(frozen_amber)
        )
        ok_true(
            item,
            f"{label_prefix} 冻结轮 box-shadow 语义(inset/3px/0/0/0/amber)",
            semantic_ok,
            expected_shadow,
            raw,
            "Chrome 序列化为 'color x y blur spread inset',故用语义解析而非子串全等",
        )
        info(
            f"{label_prefix} UAT 字面子串",
            f"'{expected_shadow}' present={expected_shadow in (raw or '')}"
            " —— Chrome 把颜色放在最前、inset 放在最后,该字面序不存在(harness 规格修正,非产品缺陷)",
        )
    ok(item, f"{label_prefix} 冻结轮 opacity", "1", read_style(page, "#round-doc", "opacity"))
    ok(item, f"{label_prefix} 冻结轮 filter", "saturate(0.6)", read_style(page, "#round-doc", "filter"))


def check_active_marker(page, item, label_prefix, panel_selector):
    """活动面板标记(VISUAL-04 / D-17)的语义断言。

    与 check_frozen_marker 同构:读 `.panel-header` 的 computed box-shadow,期望侧由
    resolve_color(page, "--color-marker-active") 在**运行时**解析 —— 值层的仲裁者是
    check-02-contrast.py,不是本 harness(故值层再改也不产生假 FAIL)。
    解析失败 / 令牌未声明 / 元素不存在一律记 blocked,绝不记 PASS。
    """
    marker = resolve_color(page, "--color-marker-active")
    info(f"{label_prefix} 令牌解析 --color-marker-active", marker)
    header = f"{panel_selector} .panel-header"
    raw = read_style(page, header, "box-shadow")
    info(f"{label_prefix} {header} box-shadow 原始值", repr(raw))
    expected = f"inset 3px 0 0 {marker}"
    parsed = parse_box_shadow(raw) if raw else None
    if parsed is None or marker is None:
        blocked(
            item,
            f"{label_prefix} 活动面板竖条 box-shadow 语义",
            expected,
            raw,
            "box-shadow 缺失或无法解析,或 --color-marker-active 解析失败",
        )
    else:
        semantic_ok = (
            parsed["inset"]
            and parsed["x"] == "3px"
            and parsed["y"] == "0px"
            and parsed["blur"] == "0px"
            and parsed["spread"] == "0px"
            and norm(parsed["color"]) == norm(marker)
        )
        ok_true(
            item,
            f"{label_prefix} 活动面板竖条 box-shadow 语义(inset/3px/0/0/0/marker)",
            semantic_ok,
            expected,
            raw,
            "Chrome 序列化为 'color x y blur spread inset',故用语义解析而非子串全等",
        )
    ok(
        item,
        f"{label_prefix} 活动面板标题 color == var(--color-marker-active)",
        marker,
        read_style(page, f"{header} h2", "color"),
    )


def check_marker_control(page, item, label_prefix):
    """活动面板标记的对照组(D-16)。

    `#ai-panel` **从不**被 `.hidden`(app.js 里 grep `aiPanel` 零命中),它的可辨状态是
    既有的折叠指示器,故不参与「三选一活动态」的 :not(.hidden) 推导,不得被标记。
    `#doc-panel-header` 虽是 `.panel-header`,但不被三条 ID 选择器匹配 —— 无意外覆盖。
    """
    ok(item, f"{label_prefix} 对照组 #ai-panel .panel-header box-shadow == none", "none",
       read_style(page, "#ai-panel .panel-header", "box-shadow"))
    ok(item, f"{label_prefix} 对照组 #doc-panel-header box-shadow == none", "none",
       read_style(page, "#doc-panel-header", "box-shadow"))


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
    # D-14:期望侧一律来自运行时解析出的令牌,不再硬编码 rgb。
    # 每条断言旁的 info() 打印解析值 —— 这是「接线对但值错」留下的人工核对痕迹;
    # 值本身的仲裁者是 scripts/check-02-contrast.py,不是本 harness。
    muted = resolve_color(page, "--color-text-muted")
    border_strong = resolve_color(page, "--color-border-strong")
    warning = resolve_color(page, "--color-action-warning")
    kind_write = resolve_color(page, "--color-kind-write")
    kind_done = resolve_color(page, "--color-kind-done")
    surface_user = resolve_color(page, "--color-surface-user")
    info("item3 令牌解析(p1)",
         f"--color-text-muted={muted} --color-border-strong={border_strong} "
         f"--color-action-warning={warning}")
    info("item3 令牌解析(p1)",
         f"--color-kind-write={kind_write} --color-kind-done={kind_done} "
         f"--color-surface-user={surface_user}")
    ok(item, "[p1] .hint color == var(--color-text-muted)", muted,
       read_style(page, ".hint", "color"))
    ok(item, "[p1] #ai-route-select border-top-color == var(--color-border-strong)", border_strong,
       read_style(page, "#ai-route-select", "border-top-color"))
    ok(item, "[p1] #selection-menu border-top-color == var(--color-border-strong)", border_strong,
       read_style(page, "#selection-menu", "border-top-color"))
    ok(item, "[p1] #stream-banner border-top-color == var(--color-action-warning)", warning,
       read_style(page, "#stream-banner", "border-top-color"))
    # box-shadow 不是颜色令牌:该 needle 由 R-2 的令牌形状(--shadow-overlay 的 0.2 alpha)
    # 固定,是本文件里唯一保留的颜色字面(D-14 的例外条款)。
    ok_contains(item, "[p1] .overlay-card box-shadow 含 rgba(0,0,0,0.2)",
                "rgba(0, 0, 0, 0.2)", read_style(page, ".overlay-card", "box-shadow"))
    # .kind-write / .kind-done 事件行:用应用自身的 renderEvent 渲染(不触发 AI 调用)
    page.evaluate("""() => {
        renderEvent({ kind: 'write', content: 'harness: kind-write 探针', raw: null });
        renderEvent({ kind: 'done', content: 'harness: kind-done 探针', raw: null });
    }""")
    ok(item, "[p1] .kind-write .event-kind background == var(--color-kind-write)", kind_write,
       read_style(page, ".kind-write .event-kind", "background-color"))
    ok(item, "[p1] .kind-done .event-kind background == var(--color-kind-done)", kind_done,
       read_style(page, ".kind-done .event-kind", "background-color"))
    # .chat-user:用应用自身的 appendChatMessage 渲染(不触发 AI 调用)
    page.evaluate("() => { appendChatMessage('user', 'harness: .chat-user 探针'); }")
    ok(item, "[p1] .chat-user background == var(--color-surface-user)", surface_user,
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
    irreversible = resolve_color(page, "--color-action-irreversible")
    irreversible_fg = resolve_color(page, "--color-action-irreversible-fg")
    irreversible_surface = resolve_color(page, "--color-action-irreversible-surface")
    text_info = resolve_color(page, "--color-text-info")
    surface_info = resolve_color(page, "--color-surface-info")
    muted_p3 = resolve_color(page, "--color-text-muted")
    info("item3 令牌解析(p3)",
         f"--color-action-irreversible={irreversible} "
         f"--color-action-irreversible-fg={irreversible_fg} "
         f"--color-action-irreversible-surface={irreversible_surface}")
    info("item3 令牌解析(p3)",
         f"--color-text-info={text_info} --color-surface-info={surface_info} "
         f"--color-text-muted={muted_p3}")
    # 接线按 style.css:928-934 的三条声明逐条对位:
    #   color → --color-action-irreversible-fg(green-12)
    #   border-color → --color-action-irreversible(green-11)
    #   background → --color-action-irreversible-surface(green-3)
    ok(item, "[p3] #btn-authorize color == var(--color-action-irreversible-fg)", irreversible_fg,
       read_style(page, "#btn-authorize", "color"))
    ok(item, "[p3] #btn-authorize border-color == var(--color-action-irreversible)", irreversible,
       read_style(page, "#btn-authorize", "border-top-color"))
    ok(item, "[p3] #btn-authorize background-color == var(--color-action-irreversible-surface)",
       irreversible_surface, read_style(page, "#btn-authorize", "background-color"))
    # D-04 反转(Plan 02):原来那条「#btn-process-round 与 #btn-authorize 三属性逐字节
    # 相同」在本阶段之后必然 FAIL —— 那正是本阶段要做的事(三段坡道)。反转成「档内相同 +
    # 三档两两不同」,一个断言同时覆盖 VISUAL-01 与 VISUAL-02。注意反转的是断言而不是现实。
    # 档内相同那一半同样承重:它能抓到「改错了一只」。
    routine_trios = {trio(page, s) for s in ROUTINE}
    commit_trios = {trio(page, s) for s in COMMIT}
    tier_trios = {trio(page, ROUTINE[0]), trio(page, COMMIT[0]), trio(page, IRREVERSIBLE[0])}
    info("item3 三档读数",
         f"routine={trio(page, ROUTINE[0])} commit={trio(page, COMMIT[0])} "
         f"irreversible={trio(page, IRREVERSIBLE[0])}")
    ok_true(
        item,
        "[p3] routine 三只三属性逐字节相同",
        len({trio(page, s) for s in ROUTINE}) == 1,
        "1",
        len(routine_trios),
        "档内相同是承重的:它能抓到「改错了一只」",
    )
    ok_true(
        item,
        "[p3] commit 两只三属性逐字节相同",
        len({trio(page, s) for s in COMMIT}) == 1,
        "1",
        len(commit_trios),
    )
    ok_true(
        item,
        "[p3] routine / commit / irreversible 三档两两不同",
        len({trio(page, ROUTINE[0]), trio(page, COMMIT[0]), trio(page, IRREVERSIBLE[0])}) == 3,
        "3",
        len(tier_trios),
        "核心价值红线:授权绝不与例行/承诺按钮在计算样式上混同",
    )
    ok(item, "[p3] #state-badge color == var(--color-text-info)", text_info,
       read_style(page, "#state-badge", "color"))
    ok(item, "[p3] #state-badge background-color == var(--color-surface-info)", surface_info,
       read_style(page, "#state-badge", "background-color"))
    ok(item, "[p3] .badge-answered color == var(--color-text-muted)", muted_p3,
       read_style(page, ".badge-answered", "color"))


# ---------------------------------------------------------------------------
# 渲染目标枚举 —— 单一事实源(G-idi-05-1 的修法)
# ---------------------------------------------------------------------------
# **枚举纪律:按 `renderMarkdown()` 的调用点,不按类名。**
#
# 这里此前只有 `MARKDOWN_HOSTS`(4 个 `.markdown-body` 宿主),而 `renderMarkdown()`
# 实际有 10 个调用点、9 个不同注入目标 —— 另外 5 个(`.event-content` / `.chat-bubble` /
# `.say-chunk` / `.annotation-note` / `.annotation-answer-body`)**不是** `.markdown-body`,
# 因此拿不到 `.markdown-body h1/h2/h3` 的字号规则,标题全部回落 UA 默认值
# (`.chat-bubble` 上下文 32px、`.event-content` 上下文 28px,字重一律 700)。
# **只枚举四个 `.markdown-body` 宿主正是 `G-idi-05-1` 存活到验证后的直接原因** ——
# 与本阶段 plan 01 已登记的教训同型(当时是只探一个宿主)。
#
# 每项 = (选择器, 注入它的 app.js 函数名, 刻度族)。刻度族取 "doc" 或 "embedded"。
# 「函数名」一栏是**给人核对的锚点**(它比行号稳 —— Phase 8 改 app.js 时行号会漂),
# 不参与断言。
MARKDOWN_TARGETS = (
    ("#draft-content", "renderDraft", "doc"),
    ("#brainstorm-content", "renderBrainstorm", "doc"),
    ("#round-doc", "loadArchiveView", "doc"),          # 两个调用点:loadArchiveView 与冻结轮路径
    ("#latest-check", "applyPhase5View", "doc"),
    (".event-content", "renderEvent", "embedded"),
    (".chat-bubble", "appendChatMessage", "embedded"),
    (".say-chunk", "appendSayToChat", "embedded"),
    (".annotation-note", "renderAnnotations", "embedded"),
    (".annotation-answer-body", "renderAnnotations", "embedded"),
)

# 派生视图(不再是手写清单)。MARKDOWN_HOSTS 的顺序与拆分前逐字相同,item4 的既有循环
# 与 check-06 的 `c05.MARKDOWN_HOSTS` 继续原样消费它。
MARKDOWN_HOSTS = tuple(sel for sel, _fn, fam in MARKDOWN_TARGETS if fam == "doc")
RENDER_TARGETS = tuple(sel for sel, _fn, fam in MARKDOWN_TARGETS if fam == "embedded")

APP_JS = ROOT / "frontend" / "app.js"
# 1 处定义(app.js:112)+ 10 个调用点。九个目标里 `#round-doc` 有两个调用点
# (`loadArchiveView` 与冻结轮路径),故调用点数比目标数多 1。
RENDER_MARKDOWN_CALL_SITES = 11


def check_render_markdown_call_sites(item):
    """调用点普查守卫(静态):让枚举无法悄悄过期。

    新增一个渲染目标而不更新 `MARKDOWN_TARGETS`,本断言立刻 FAIL 并给出可执行的动作。
    判据由脚本自己从 `frontend/app.js` 的文本算出(不用 shell 管道),且比的是
    「调用点数 vs 枚举条数」两个独立量 —— 不是自比。
    """
    count = APP_JS.read_text(encoding="utf-8").count("renderMarkdown(")
    ok_true(
        item,
        "app.js 的 renderMarkdown( 计数 == 11(1 定义 + 10 调用点)",
        count == RENDER_MARKDOWN_CALL_SITES,
        RENDER_MARKDOWN_CALL_SITES,
        count,
        "调用点数变了 ⇒ 按调用点更新 MARKDOWN_TARGETS,再跑本项",
    )
    ok_true(
        item,
        "MARKDOWN_TARGETS 条数 == 9(与调用点枚举一一对应)",
        len(MARKDOWN_TARGETS) == 9,
        9,
        len(MARKDOWN_TARGETS),
        "渲染目标数变了 ⇒ 按调用点更新 MARKDOWN_TARGETS,再跑本项",
    )


# ---------------------------------------------------------------------------
# UAT 第 4 项 — Plan 02 的 16 项
# ---------------------------------------------------------------------------
# `.markdown-body` 的四个宿主(UI-SPEC §字号刻度的范围栅栏点名的影响面)。四个都要探:
# 本阶段修掉的层叠缺陷(`#draft-view h2` 等 1-0-1 后代选择器压掉 `.markdown-body h2`)
# 只在其中三个上出现,`#latest-check` 一直是对的 —— 只探一个宿主正是它存活到执行期的原因。


def item4(page, tmp_root):
    item = "4"
    print("\n=== UAT 4: DevTools computed-style 抽查 — Plan 02(16 项)===", flush=True)
    proj = make_fixture("p1", tmp_root)
    enter_project(page, proj)
    # D-14:期望侧来自运行时解析的令牌,不再硬编码 rgb(值的仲裁者是 check-02-contrast.py)。
    brainstorm_warning = resolve_color(page, "--color-action-warning")
    info("item4 令牌解析", f"--color-action-warning={brainstorm_warning}")

    # D-12:该值在 HEAD 上是刻度内的合法档(6px = --space-1-5、10px = --space-2-5),
    # 04.1 明令不改 S-1/S-2,故更新期望值而非改 CSS。
    ok(item, "[p1] .panel-header padding-top", "6px", read_style(page, ".panel-header", "padding-top"))
    ok(item, "[p1] .panel-header padding-left", "10px", read_style(page, ".panel-header", "padding-left"))
    # D-13:原期望串写错了名字 —— index.html 里从来没有 #doc-pane 这个 id,实际是
    # #doc-panel-body。实测其 padding 一直是 32px/40px,与期望值一致,只是名对不上。
    # 改的是 UAT 的期望字符串,不是 id(硬规则 5:约 70 个 getElementById id 一字未动)。
    ok(item, "[p1] #doc-panel-body padding", "32px 40px",
       read_style(page, "#doc-panel-body", "padding"))
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

    # D-12:以下四条字号是「更新期望值接受 HEAD 现状」(18px = --text-lg、
    # 24px = --text-xl 都是 S-2 刻度内的合法档),frontend/style.css 一字未动。
    # D-02:该断言守卫的 14px 已由 quick 260918-qrq 推翻(HEAD 实况 16px = --text-md),
    # 继续硬编码只会继续假 FAIL。按 D-03 第一类改为令牌接线表述。
    ok(item, "[p1] #brainstorm-view h2 font-size == var(--text-md)",
       resolve_token(page, "--text-md"), read_style(page, "#brainstorm-view h2", "font-size"))
    ok(item, "[p1] #brainstorm-view h2 color == var(--color-action-warning)",
       brainstorm_warning, read_style(page, "#brainstorm-view h2", "color"))
    ok(item, "[p1] #draft-view h2 font-size", "18px", read_style(page, "#draft-view h2", "font-size"))
    ok(item, "[p1] .panel-header h2 font-size", "14px", read_style(page, ".panel-header h2", "font-size"))
    ok(item, "[p1] .overlay-card h3 font-size", "24px", read_style(page, ".overlay-card h3", "font-size"))
    # `.markdown-body` 的规范消费者是 #draft-content(文档区正文渲染区)。
    # document.querySelector('.markdown-body') 会落到 #latest-check(它也带该类且自带
    # font-size 覆盖),那不是 `.markdown-body` 规则本身的探针。
    ok(item, "[p1] .markdown-body font-size(探针 #draft-content)", "16px",
       read_style(page, "#draft-content", "font-size"))
    # `.markdown-body` 内的标题、行内 code、表格单元格与引用块都需要真实元素:用应用自身的
    # renderMarkdown 渲染一段含三级标题、代码跨度、表格与引用块的 markdown
    # (真实渲染路径,零网络、零 AI 调用)。
    page.evaluate("""(hosts) => {
        const md = '# 一级标题\\n\\n## 二级标题\\n\\n### 三级标题\\n\\n'
                 + '| 表头 A | 表头 B |\\n| --- | --- |\\n| 单元格 | 单元格 |\\n\\n'
                 + '> 引用块探针\\n\\nharness `probe` 探针';
        for (const sel of hosts) {
            const host = document.querySelector(sel);
            host.innerHTML = '';
            host.appendChild(renderMarkdown(md));
        }
    }""", list(MARKDOWN_HOSTS))
    # D-03 第一类:本阶段改动的字号走令牌接线,期望侧由 resolve_token 在运行时解析,
    # 值层再改也不产生假 FAIL。info() 打印解析值,给「接线对但值错」留下人工核对痕迹。
    h1_size = resolve_token(page, "--text-3xl")
    h2_size = resolve_token(page, "--text-2xl")
    h3_size = resolve_token(page, "--text-lg")
    info("item4 令牌解析(文档标题字号)",
         f"--text-3xl={h1_size} --text-2xl={h2_size} --text-lg={h3_size}")
    # 四个宿主逐个断言。只探 #draft-content 时,`#brainstorm-content`(16px)与 `#round-doc`(18px)
    # 的同类压制会整片溜过去 —— 那是本阶段执行期真实发生的漏检,不是假设。
    for host in MARKDOWN_HOSTS:
        ok(item, f"[p1] {host} h1 font-size == var(--text-3xl)", h1_size,
           read_style(page, f"{host} h1", "font-size"))
        ok(item, f"[p1] {host} h2 font-size == var(--text-2xl)", h2_size,
           read_style(page, f"{host} h2", "font-size"))
        ok(item, f"[p1] {host} h3 font-size == var(--text-lg)", h3_size,
           read_style(page, f"{host} h3", "font-size"))
    ok(item, "[p1] .markdown-body code font-size", "14px",
       read_style(page, "#draft-content code", "font-size"))

    # TYPE-02 复证(D-08,零 CSS 改动):三处「已由 quick 260918-qrq 归入刻度与令牌」的对象
    # 里,表格单元格与引用块在此补出**运行时**证据(第三处 code 由上面那条字面守卫覆盖)。
    # 本任务只出证据、不改这三处的任何值 —— 为「有交付物」而重写会把一个已经正确的状态改坏。
    # 探针宿主沿用 #draft-content(与上面 code 的探针一致),元素未渲染出来时 read_style
    # 返回 None,ok() 记 BLOCKED,绝不记 PASS。
    base_size = resolve_token(page, "--text-base")
    muted_color = resolve_color(page, "--color-text-muted")
    info("item4 令牌解析(TYPE-02 复证)",
         f"--text-base={base_size} --color-text-muted={muted_color}")
    ok(item, "[p1] .markdown-body td font-size == var(--text-base)", base_size,
       read_style(page, "#draft-content td", "font-size"))
    ok(item, "[p1] .markdown-body blockquote color == var(--color-text-muted)", muted_color,
       read_style(page, "#draft-content blockquote", "color"))

    # TYPE-03(D-09 / D-12):五只动作按钮的字重由 600 降到 500 —— 与 chrome 标题同档,
    # 分工是「内容标题 600 / chrome 标题与按钮 500」。#btn-authorize 按 D-12 保持 600,
    # 这是 D-09 的**唯一已登记例外**(授权绝不与例行混同,四个强调通道此处用满)。
    # 六只按钮全部常驻 DOM;getComputedStyle 对 display:none 的元素仍返回解析后的
    # font-weight(它不依赖布局),故此处无需检查可见性 —— 与上面读 #state-badge 的
    # z-index 是同一个事实。期望侧写字面档值 500 / 600:Chrome 把 font-weight 序列化为
    # 无单位的数字串,与 resolve_token 读到的自定义属性值同形(info() 里记录解析值以便核对)。
    fw_medium = resolve_token(page, "--fw-medium")
    fw_semibold = resolve_token(page, "--fw-semibold")
    info("item4 令牌解析(字重档)", f"--fw-medium={fw_medium} --fw-semibold={fw_semibold}")
    for sel in ("#btn-approve-draft", "#btn-process-round", "#btn-start-writing",
                "#btn-continue-check", "#btn-continue-repair"):
        ok(item, f"[p1] {sel} font-weight == 500(--fw-medium)", "500",
           read_style(page, sel, "font-weight"))
    ok(item, "[p1] #btn-authorize font-weight == 600(--fw-semibold,D-12 唯一例外)", "600",
       read_style(page, "#btn-authorize", "font-weight"))
    # D-13(Plan 02):#btn-authorize 的第四个强调通道 —— 字号步进到 16px(--text-md,
    # 现有档,零新增令牌)。**不加 padding 步进**:16px 下「授权撰写总设计文档」约 144px +
    # padding-x 32px ≈ 176px,而 --doc-panel-w 最窄 340px 减 #doc-panel-body 的
    # padding(32/40)= 内容宽 260px > 176px,故不换行 —— 这条算术正是 D-13 的验收条件。
    text_md_size = resolve_token(page, "--text-md")
    info("item4 令牌解析(D-13 字号步进)", f"--text-md={text_md_size}")
    ok(item, "[p1] #btn-authorize font-size == var(--text-md)(D-13)", text_md_size,
       read_style(page, "#btn-authorize", "font-size"))

    # ---- VISUAL-03 复证 + 页面级层级链(SC3)------------------------------------
    # D-19:VISUAL-03 已由 quick 260918-qrq 实现,本任务**零 CSS 改动**,产物是门与记录。
    # 契约文本(ROADMAP / 04-UI-SPEC)引用的是 `#doc-pane > h1`,该选择器在 HEAD 上
    # **从来不存在**;实际承担「安静的容器标签,不是全屏最大最重的文字」职责的是
    # `#doc-panel-header h1`。下面两条把这次漂移登记成机械可核的事实。
    # 字面值而非令牌接线 —— D-03 第二类:它们守卫的是一个**不该变**的值,改成令牌
    # 接线会退化为同义反复。**不得**为让契约文本成立而新建 `#doc-pane` 元素或规则。
    ok(item, "[p1] #doc-panel-header h1 font-size", "14px",
       read_style(page, "#doc-panel-header h1", "font-size"))
    ok(item, "[p1] #doc-panel-header h1 font-weight", "500",
       read_style(page, "#doc-panel-header h1", "font-weight"))
    has_doc_pane = page.evaluate("() => document.querySelector('#doc-pane') !== null")
    ok_true(item, "[p1] #doc-pane 选择器不存在(契约漂移登记,D-01)",
            has_doc_pane is False, "false", has_doc_pane,
            "契约文本引用的 #doc-pane > h1 从来不是 HEAD 上的选择器")

    # SC3 的页面级层级链:全屏最大最重的文字不再是容器标签「文档区」。
    # 用应用自身的 renderMarkdown 重新渲染一个含 h1/h2 的探针串(真实渲染路径,零网络、
    # 零 AI 调用),再把四档字号**解析成整数**逐对比较 —— 字符串比较会踩 "14px" < "9px"
    # 的序陷阱。此处的重新渲染是安全的:依赖 #draft-content 内容的断言(code / td /
    # blockquote)都已在上方跑完,此后不再读它的旧内容。
    page.evaluate("""() => {
        const host = document.querySelector('#draft-content');
        host.innerHTML = '';
        host.appendChild(renderMarkdown('# 一级标题\\n\\n## 二级标题'));
    }""")
    chain_raw = [
        ("文档 h1", read_style(page, "#draft-content h1", "font-size")),
        (".overlay-card h3(模态)", read_style(page, ".overlay-card h3", "font-size")),
        ("文档 h2", read_style(page, "#draft-content h2", "font-size")),
        ("#doc-panel-header h1(容器标签)", read_style(page, "#doc-panel-header h1", "font-size")),
    ]
    info("item4 页面级层级链(SC3)", " > ".join(f"{k}={v}" for k, v in chain_raw))
    chain_px = [int(v[:-2]) if isinstance(v, str) and v.endswith("px") else None
                for _, v in chain_raw]
    if None in chain_px:
        blocked(item, "[p1] 页面级层级链 文档h1 > 模态h3 > 文档h2 > 容器标签h1(严格降序)",
                "28 > 24 > 22 > 14", chain_px, "四档字号中有读不到的值(元素/选择器不存在)")
    else:
        ok_true(item, "[p1] 页面级层级链 文档h1 > 模态h3 > 文档h2 > 容器标签h1(严格降序)",
                all(a > b for a, b in zip(chain_px, chain_px[1:])),
                "28 > 24 > 22 > 14", " > ".join(str(v) for v in chain_px),
                "SC3:全屏最大最重的文字是文档自己的 h1,不是容器标签")

    # TOKEN-07 / R-1 的渲染层证据:三条 z-index 走令牌接线,值层再改也不产生假 FAIL。
    # #state-badge 的 z-index 由 R-1 恢复后 --z-badge 才重新有消费者,
    # 围栏断言的 `badge < banner` 承重序关系两端都在真实 DOM 上被读到。
    z_menu = resolve_token(page, "--z-selection-menu")
    z_badge = resolve_token(page, "--z-badge")
    z_banner = resolve_token(page, "--z-banner")
    info("item4 令牌解析(z-index)", f"--z-selection-menu={z_menu} --z-badge={z_badge} "
         f"--z-banner={z_banner}")
    ok(item, "[p1] #selection-menu z-index == var(--z-selection-menu)", z_menu,
       read_style(page, "#selection-menu", "z-index"))
    ok(item, "[p1] #state-badge z-index == var(--z-badge)", z_badge,
       read_style(page, "#state-badge", "z-index"))
    ok(item, "[p1] #stream-banner z-index == var(--z-banner)", z_banner,
       read_style(page, "#stream-banner", "z-index"))

    # ---- VISUAL-04:活动面板标记的三态实读 + 对照组(D-16 / D-17)----------------
    # 三个互斥面板在任一状态里恰有一个可见,那一个就是「活动态」。三态各读一次:
    # p1 → #session-panel、p3 → #annotations-panel、checking → #checks-panel。
    # 每个样本同时跑对照组:活动面板之外的两个 `.panel-header` 必须保持 box-shadow: none。
    check_active_marker(page, item, "[p1]", "#session-panel")
    check_marker_control(page, item, "[p1]")

    # ---- VISUAL-05:裁决位置行的掩码字形(D-20 / D-21 / D-22)-------------------
    # 用应用自身的 renderVerdictCard 渲染一张裁决卡 —— 'p2' 模式才会创建
    # .verdict-location(真实渲染路径,零网络、零 AI 调用)。
    verdict_rendered = page.evaluate("""() => {
        const host = document.querySelector('#verdict-cards');
        if (!host || typeof renderVerdictCard !== 'function') return false;
        host.innerHTML = '';
        host.appendChild(renderVerdictCard(
            { number: 1, location: 'harness 探针位置', issue: 'i', suggestion: 's' }, 'p2'));
        return !!host.querySelector('.verdict-location');
    }""")
    if not verdict_rendered:
        blocked(
            item,
            "[p1] .verdict-location::before mask 盒模型",
            "裁决卡渲染出 .verdict-location",
            "<未渲染>",
            "renderVerdictCard(..., 'p2') 未产出 .verdict-location",
        )
    else:
        check_mask_glyph(page, item, "[p1]", ".verdict-location", "--icon-location")

    # 冻结轮(与第 2 项共用读取器)
    proj = make_fixture("p3", tmp_root)
    enter_project(page, proj)
    goto_frozen_round(page, item)
    check_frozen_marker(page, item, "[p3→round1]")
    check_active_marker(page, item, "[p3]", "#annotations-panel")
    check_marker_control(page, item, "[p3]")

    # checking 样本:p3 的批注流让位给自检报告面板(#checks-panel 变活动态)。
    proj = make_fixture("checking", tmp_root)
    enter_project(page, proj)
    check_active_marker(page, item, "[checking]", "#checks-panel")
    check_marker_control(page, item, "[checking]")

    # 归档态灰化
    proj = make_fixture("archive", tmp_root)
    enter_project(page, proj)
    ok(item, "[archive] #rounds-placeholder.archive-mode #round-doc opacity", "0.75",
       read_style(page, "#rounds-placeholder.archive-mode #round-doc", "opacity"))

    # 任意 button color(通用规则,探针同上)。D-14:期望侧来自 --color-text 的运行时解析。
    text_token = resolve_color(page, "--color-text")
    info("item4 令牌解析", f"--color-text={text_token}")
    ok(item, "[archive] button color(通用规则,探针 #btn-enter) == var(--color-text)",
       text_token, read_style(page, "#btn-enter", "color"))

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
    # D-14:六条颜色断言的期望侧全部来自运行时解析的令牌,不再硬编码 rgb。
    ok(item, "[p1] #ai-route-select border-top-color == var(--color-border-strong)",
       resolve_color(page, "--color-border-strong"),
       read_style(page, "#ai-route-select", "border-top-color"))
    ok(item, "[p1] #ai-route-select background-color == var(--color-surface)",
       resolve_color(page, "--color-surface"),
       read_style(page, "#ai-route-select", "background-color"))
    ok(item, "[p1] .hint color == var(--color-text-muted)",
       resolve_color(page, "--color-text-muted"), read_style(page, ".hint", "color"))
    # .hint 自身无背景,沿祖先链取到的实际底色。实测:命中的是 index.html 里
    # #doc-panel-body → #doc-panel 内的那条,而 #doc-panel { background: var(--color-surface) }
    # —— 故是 --color-surface,不是 --color-surface-page(两者在 04.1 之后是 #f9f9f9 / #fcfcfc)。
    ok(item, "[p1] .hint 实际背景 == var(--color-surface)",
       resolve_color(page, "--color-surface"), effective_bg(page, ".hint"),
       note=".hint 自身无背景,沿祖先链取到的实际底色")
    ok(item, "[p1] #stream-banner border-top-color == var(--color-action-warning)",
       resolve_color(page, "--color-action-warning"),
       read_style(page, "#stream-banner", "border-top-color"))

    # ORDER 0.363 的可观察形态:.markdown-body 必须明显比 .hint 更深
    # (该比值由 0.311 放宽到 0.363 是刻度强制的,见 UI-SPEC 04.1-N-1,不是判断失误)。
    body_color = read_style(page, ".markdown-body", "color")
    hint_color = read_style(page, ".hint", "color")
    ok(item, "[p1] .markdown-body color == var(--color-text)",
       resolve_color(page, "--color-text"), body_color)
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
            "ORDER 0.363 的可观察形态",
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

    # VISUAL-05 / D-20…D-22:引用行前缀从写死的 emoji 换成跟随令牌的掩码字形。
    # item6 已经写出批注并渲染出 .annotation-quote,是这条断言的天然落点。
    check_mask_glyph(page, item, "[p3]", ".annotation-quote", "--icon-pin")


# ---------------------------------------------------------------------------
# UAT 第 7 项 — G-idi-05-1:五个非 .markdown-body 渲染目标的标题刻度
# ---------------------------------------------------------------------------
# 这五项断言是**造出容器再断言**,不靠「fixture 里本来就有 .chat-bubble」。
# 容器造不出时记 BLOCKED,绝不记 PASS(与 check-06 的 g4 / g5 同约定)。
# 取值规则(契约 P-20):嵌入档 = 文档档沿数值阶梯下移一档 —— 28 → 24(--text-xl)、
# 22 → 18(--text-lg)、18 → 16(--text-md),字重取内容标题档 --fw-semibold(600)。
PROBE_MD = "# 探针一级\n\n## 探针二级\n\n### 探针三级"


def px_of(value):
    """'28px' → 28.0;取不到返回 None。比较必须用整数 —— 字符串比较会踩 "14px" < "9px"。"""
    if not value or not isinstance(value, str) or not value.endswith("px"):
        return None
    try:
        return float(value[:-2])
    except ValueError:
        return None


def item7(page, tmp_root):
    item = "7"
    print("\n=== UAT 7: 五个嵌入渲染目标的标题刻度(G-idi-05-1 / SC3)===", flush=True)
    proj = make_fixture("p1", tmp_root)
    enter_project(page, proj)
    info("item7 渲染目标枚举",
         f"doc={list(MARKDOWN_HOSTS)} embedded={list(RENDER_TARGETS)}")

    # 用应用自身的四个渲染函数把带三级标题的探针 markdown 注入五个容器 ——
    # 真实渲染路径,零网络、零 AI 调用(`appendChatMessage` / `appendSayToChat` 就是
    # 应用自己的注入路径,不需要真实 AI 轮次)。
    # renderAnnotations 的入参是**对象** `{items: [...]}`,不是数组;条目用 type:'plain'
    # 使 details.open = true,两个容器都真实渲染。
    created = page.evaluate("""(md) => {
        const sels = ['.event-content', '.chat-bubble', '.say-chunk',
                      '.annotation-note', '.annotation-answer-body'];
        try {
            if (typeof renderEvent === 'function') renderEvent({ kind: 'say', content: md });
            if (typeof appendChatMessage === 'function') appendChatMessage('ai', md);
            if (typeof appendSayToChat === 'function') appendSayToChat(md);
            if (typeof renderAnnotations === 'function') {
                renderAnnotations({ items: [{
                    id: 'probe-7', type: 'plain', status: 'answered',
                    quote: '探针摘录', note: md, answer: md,
                }] }, true);
            }
            const doc = document.querySelector('#draft-content');
            if (doc) { doc.innerHTML = ''; doc.appendChild(renderMarkdown(md)); }
        } catch (e) {
            return { error: String(e) };
        }
        const out = {};
        for (const s of sels) out[s] = document.querySelector(s) !== null;
        return { created: out };
    }""", PROBE_MD)
    info("item7 容器创建", str(created))
    if created.get("error"):
        blocked(item, "item7 五个容器已渲染", "四个渲染函数产出五个容器",
                "<ERROR>", created["error"])
    hit = created.get("created") or {}

    t_xl = resolve_token(page, "--text-xl")
    t_lg = resolve_token(page, "--text-lg")
    t_md = resolve_token(page, "--text-md")
    fw_semibold = resolve_token(page, "--fw-semibold")
    info("item7 令牌解析",
         f"--text-xl={t_xl} --text-lg={t_lg} --text-md={t_md} --fw-semibold={fw_semibold}")

    # 5 目标 × 3 档 × 2 属性 = 30 条。期望侧由 resolve_token 在运行时解析
    # (D-03 第一类),值层再改也不产生假 FAIL。
    scale = (("h1", t_xl, "--text-xl"), ("h2", t_lg, "--text-lg"), ("h3", t_md, "--text-md"))
    weights = []
    for sel in RENDER_TARGETS:
        if not hit.get(sel):
            blocked(item, f"[p1] {sel} 容器已渲染", "<容器存在>", "<MISSING>",
                    "渲染函数未产出该容器")
            continue
        for tag, token, token_name in scale:
            ok(item, f"[p1] {sel} {tag} font-size == var({token_name})", token,
               read_style(page, f"{sel} {tag}", "font-size"))
            weight = read_style(page, f"{sel} {tag}", "font-weight")
            weights.append(weight)
            ok(item, f"[p1] {sel} {tag} font-weight == var(--fw-semibold)", fw_semibold, weight)

    # SC3 的机械形态:文档 h1 **严格大于**每个目标自己的 h1(先造容器再断言)。
    # 注意 check-06 的 g2 只把探针注入四个 MARKDOWN_HOSTS,对下面五个容器状态盲
    # (见 UI-SPEC 05-N-7),故它不是这条约束的依据 —— 依据就是下面这 5 条。
    doc_h1 = px_of(read_style(page, "#draft-content h1", "font-size"))
    info("item7 文档 h1", f"#draft-content h1 = {doc_h1}px")
    if doc_h1 is None:
        blocked(item, "[p1] 文档 h1 已渲染(#draft-content h1)", "px 值", "<MISSING>",
                "renderMarkdown 未产出 #draft-content h1")
    for sel in RENDER_TARGETS:
        label = f"[p1] 文档 h1 严格大于 {sel} h1(SC3)"
        if doc_h1 is None:
            continue
        if not hit.get(sel):
            blocked(item, label, f">{doc_h1:g}px", "<MISSING>", "容器未渲染出来")
            continue
        target_h1 = px_of(read_style(page, f"{sel} h1", "font-size"))
        if target_h1 is None:
            blocked(item, label, f">{doc_h1:g}px", "<MISSING>", f"{sel} h1 未渲染出来")
            continue
        ok_true(item, label, doc_h1 > target_h1, f">{target_h1:g}px", f"{doc_h1:g}px",
                "SC3:全屏最大最重的文字是文档自己的 h1")

    # 第四字重档:五个目标的 h1/h2/h3 里不得有任何 700(契约只声明 400 / 500 / 600)。
    # 读不到的字重是 None,`all(w != "700")` 对 None 恒真 —— 不加 None 支这条断言会在
    # 「标题根本没渲染出来」时静默 PASS。故 None 与缺失同处置:记 BLOCKED。
    if not weights or any(w is None for w in weights):
        blocked(item, "[p1] 五个渲染目标无第四字重档 700(契约只声明 400/500/600)",
                "15 个可读字重", ",".join(str(w) for w in weights) or "<MISSING>",
                "五个容器有一个造不出,或标题未渲染出来")
    else:
        ok_true(item, "[p1] 五个渲染目标无第四字重档 700(契约只声明 400/500/600)",
                all(w != "700" for w in weights), "无 700", ",".join(weights))

    check_render_markdown_call_sites(item)


# ---------------------------------------------------------------------------
# UAT 第 8 项 — L-1 徽标收口:流内 badge + sticky 表头(D-06)
# ---------------------------------------------------------------------------
# 三条断言(L-1 的门):
#   (a) #state-badge 是流内元素(computed position == static,right 无声明);
#   (b) 768 / 1024 / 1280 三处 #state-badge 与 #stream-banner 的 rect 不相交;
#   (c) 滚动 #doc-panel 到底后 #doc-panel-header 仍可见(sticky 生效)。
# 两条几何断言各带**前提检查**(元素可见且 rect 非全零 / 容器真的可滚),前提不成立记
# blocked(...) 而非 ok_true(...) —— 与 item7 已登记的 `all(w != "700")` 对 None 恒真
# 是同型陷阱(空转断言),也是本阶段威胁表 T-idi-06-04 的落点。
# 另含三项诊断(三宽度文档级溢出 / L-5 clearance 普查 / L-6 命中区普查):波次 1 一律经
# info() 输出、不升为断言(判据要等 L-3 / L-4 落地后才成立);波次 3 把其中两项升为断言
# (三宽度文档级溢出 → L-2 的硬断言 + `#doc-panel` 实测宽的判别性探针;L-5 / L-6 两条普查
# → item 9 的断言)。**原始数值**始终逐行落盘,不给结论替代证据(UI-SPEC §L-2 明文)。
BADGE_BANNER_WIDTHS = (768, 1024, 1280)
# harness 里**第一次** viewport 变更(item 8);任何一次 set_viewport_size 之后都必须
# 复位到这个值,否则污染其后所有项(item 9 与任何依赖 1440 宽度的既有断言)。
VIEWPORT_RESTORE = {"width": 1440, "height": 900}
# L-1 的碰撞实检用的就是这个字符串(UI-SPEC §Copywriting Contract 的冻结表)。
BANNER_TEXT = "事件流已断开,正在自动重连……"
# 把 #doc-panel 撑到可滚所需的正文(经应用自身的 renderMarkdown 注入,真实渲染路径)。
LONG_DOC_MD = "\n\n".join(
    f"第 {i} 段探针正文:用于把文档面板撑到可滚,使 sticky 断言不是空转。" for i in range(1, 81)
)
# 三宽度溢出诊断的输入:一张宽 markdown 表 + 一个不可断长 token。
# #doc-panel { overflow-y: auto } 会把 overflow-x 的 used value 一并算成 auto,
# 故宽表只在**面板内部**产生横向滚动条 —— 那是可达内容,不是文档级溢出(L-2 明文)。
WIDE_MD = (
    "| " + " | ".join(f"列{c}" for c in range(1, 13)) + " |\n"
    + "| " + " | ".join("---" for _ in range(12)) + " |\n"
    + "| " + " | ".join("单元格内容" for _ in range(12)) + " |\n\n"
    + "不可断长 token:" + ("a" * 240) + "\n"
)

# L-2 的三宽度判据读数:文档级 scrollWidth / clientWidth + `#doc-panel` 的**实测宽**。
# `#doc-panel` 的实测宽是本阶段 LAYOUT-02 的**判别性探针**,不是补充读数:文档级
# `scrollWidth` 对「flex 项被长不可断内容顶破」这一失效模式是**结构性失明**的 ——
# `#doc-panel { overflow-y: auto }` 会把 `overflow-x` 的 used value 一并算成 `auto`,
# 且滚动容器的自动最小尺寸(`min-width: auto`)解析为 0,故宽内容只在**面板内部**产生
# 横向滚动条,永远推不高文档级 `scrollWidth`。面板自身的实测宽则直接测「它有没有被顶得
# 比它自己声明的 `clamp(340px, 30vw, 480px)` 还宽」—— 那正是 L-3 的 `min-width: 0` 的
# 保护对象。(波次 1 / 2 的三宽度读数在波次 1 就已经是 0px,该读数无法区分「修好了」与
# 「本来就没破」;本节的两个读数一起才构成判据。)
_IDI06_OVERFLOW_JS = """() => {
  const p = document.querySelector('#doc-panel');
  return {
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
    panelWidth: p ? p.getBoundingClientRect().width : null,
  };
}"""

# `--doc-panel-w: clamp(340px, 30vw, 480px)`(frontend/style.css:228)的三个参数。
# 面板宽的**声明上界**就是这条 clamp 在当前视口宽下的解析值。
DOC_PANEL_W_MIN_PX = 340.0
DOC_PANEL_W_VW = 0.30
DOC_PANEL_W_MAX_PX = 480.0


def _doc_panel_declared_width(viewport_width):
    """`clamp(340px, 30vw, 480px)` 在给定视口宽下的解析值(= 面板宽的声明上界)。"""
    return min(DOC_PANEL_W_MAX_PX, max(DOC_PANEL_W_MIN_PX, DOC_PANEL_W_VW * viewport_width))


# L-2 的决策(本阶段实测结论,见 `idi-06-03-SUMMARY.md` 的「测量决策记录(最终态)」):
# 1440 / 1024 / 768 三处在波次 2 之后的树上均无破版 ⇒ 按 UI-SPEC §L-2 的决策规则第一支,
# 守卫**不写**,该交付物登记为「被实测推翻」。故期望的 `@media` 出现次数是 **0**。
# 若日后实测证成并写出守卫,把这里改成 1 并同步更新 SUMMARY 的决策记录与 UI-SPEC §L-2。
MEDIA_QUERY_DECL = "@media"
EXPECTED_MEDIA_QUERIES = 0


def _l2_guard_shape(item):
    """L-2 守卫形态(静态):`frontend/style.css` 里 `@media` 出现次数与本次决策一致。

    读的是**文件文本**而非渲染结果 —— 与几何断言互补:它抓「守卫被悄悄删掉 / 悄悄多写
    一条」。读法与 `check_render_markdown_call_sites` 同族:脚本自己从文件文本算,不依赖
    shell 管道;比的是「实测计数 vs 决策」两个独立量,不是自比。
    """
    try:
        text = STYLE_CSS.read_text(encoding="utf-8")
    except OSError as exc:
        blocked(item, "[static] frontend/style.css 的 @media 出现次数 == 决策",
                EXPECTED_MEDIA_QUERIES, "<MISSING>", f"{STYLE_CSS} 读不到:{exc}")
        return
    count = text.count(MEDIA_QUERY_DECL)
    lines = [i for i, ln in enumerate(text.splitlines(), 1) if MEDIA_QUERY_DECL in ln]
    info("item8 [static] L-2 守卫形态",
         f"frontend/style.css 里 '{MEDIA_QUERY_DECL}' 计数={count} 命中行={lines};"
         f"本次决策=「被实测推翻」(三宽度均无破版)⇒ 期望 {EXPECTED_MEDIA_QUERIES}")
    ok_true(item,
            "[static] frontend/style.css 的 @media 出现次数 == 决策(被实测推翻 ⇒ 0)",
            count == EXPECTED_MEDIA_QUERIES, EXPECTED_MEDIA_QUERIES, count,
            "该断言读文件文本而非渲染结果,与几何断言互补。若实测证成并写出守卫,"
            "须同步改本常量与 idi-06-03-SUMMARY.md 的决策记录")

_IDI06_BADGE_BANNER_JS = """() => {
  const b = document.querySelector('#state-badge');
  const n = document.querySelector('#stream-banner');
  if (!b || !n) return null;
  const rb = b.getBoundingClientRect();
  const rn = n.getBoundingClientRect();
  return {
    badge: {left: rb.left, right: rb.right, top: rb.top, bottom: rb.bottom,
            width: rb.width, height: rb.height},
    banner: {left: rn.left, right: rn.right, top: rn.top, bottom: rn.bottom,
             width: rn.width, height: rn.height},
    badgeDisplay: getComputedStyle(b).display,
    bannerDisplay: getComputedStyle(n).display,
  };
}"""

_IDI06_SCROLL_JS = """() => {
  const p = document.querySelector('#doc-panel');
  const h = document.querySelector('#doc-panel-header');
  if (!p || !h) return null;
  p.scrollTop = p.scrollHeight;
  const rp = p.getBoundingClientRect();
  const rh = h.getBoundingClientRect();
  return {
    scrollTop: p.scrollTop, scrollHeight: p.scrollHeight, clientHeight: p.clientHeight,
    panel: {top: rp.top, bottom: rp.bottom, left: rp.left, right: rp.right},
    header: {top: rh.top, bottom: rh.bottom, left: rh.left, right: rh.right},
  };
}"""

# L-5 / L-6 的普查。**按元素枚举,不按容器名** —— 按点名枚举会漏掉没被点名的那个
# (Phase 5 的 G-idi-05-1 与本阶段 A11Y-07 是同构教训)。
# clearance = 可聚焦元素 rect 到其**最近裁剪祖先**的 padding 边的距离,取四边最小值。
# `visible` 一栏是承重的:被祖先藏住的元素 rect 全零,不得把它读成「命中区不足 24×24」。
_IDI06_CENSUS_JS = r"""() => {
  const px = (v) => parseFloat(v) || 0;
  const isClipping = (el) => {
    const s = getComputedStyle(el);
    return s.overflowX !== 'visible' || s.overflowY !== 'visible';
  };
  const labelOf = (el) => {
    if (el.id) return '#' + el.id;
    const cls = (typeof el.className === 'string' && el.className.trim())
      ? '.' + el.className.trim().split(/\s+/).join('.') : '';
    return el.tagName.toLowerCase() + cls;
  };
  const rectOf = (el) => {
    const r = el.getBoundingClientRect();
    return {left: r.left, top: r.top, right: r.right, bottom: r.bottom,
            width: r.width, height: r.height};
  };

  const clearance = [];
  document.querySelectorAll(
    'button, input, select, textarea, a[href], summary, [tabindex]'
  ).forEach((el) => {
    let anc = el.parentElement;
    let nearest = null;
    while (anc) {
      if (isClipping(anc)) { nearest = anc; break; }
      anc = anc.parentElement;
    }
    if (!nearest) return;
    const r = el.getBoundingClientRect();
    const ar = nearest.getBoundingClientRect();
    const s = getComputedStyle(nearest);
    const padLeft = ar.left + px(s.borderLeftWidth);
    const padTop = ar.top + px(s.borderTopWidth);
    const padRight = ar.right - px(s.borderRightWidth);
    const padBottom = ar.bottom - px(s.borderBottomWidth);
    const gap = Math.min(r.left - padLeft, padRight - r.right,
                         r.top - padTop, padBottom - r.bottom);
    // `intersects` 是承重的:元素若与容器的 padding 盒**完全不相交**,说明它被滚动到
    // 视口之外 —— 当前不渲染,焦点环无被裁风险,它的 clearance 是负的噪声(p3 下
    // `#btn-authorize × #doc-panel = -122.6px` 就是这一类,应读作「需滚动才能到达」
    // 而非「被裁切」,见 idi-06-01-SUMMARY.md 的判读)。反之,元素与 padding 盒**相交
    // 却越界**才是真正的裁切,其 clearance 为负,必须被断言抓到。
    const intersects = r.right > padLeft && r.left < padRight
                    && r.bottom > padTop && r.top < padBottom;
    clearance.push({el: labelOf(el), container: labelOf(nearest), clearance: gap,
                    visible: r.width > 0 && r.height > 0, intersects: intersects,
                    rect: rectOf(el)});
  });

  const hits = [];
  document.querySelectorAll(
    'button, input, select, textarea, summary, a[href], [role=button], [onclick]'
  ).forEach((el) => {
    const r = el.getBoundingClientRect();
    const visible = r.width > 0 && r.height > 0;
    hits.push({el: labelOf(el), w: r.width, h: r.height, visible: visible,
               below24: visible ? (r.width < 24 || r.height < 24) : null});
  });

  return {clearance: clearance, hits: hits};
}"""


def _rects_intersect(a, b):
    """两个 rect 是否相交(判据与 L-1 的门逐字一致)。"""
    return not (
        a["right"] <= b["left"]
        or b["right"] <= a["left"]
        or a["bottom"] <= b["top"]
        or b["bottom"] <= a["top"]
    )


def _idi06_census(page, state):
    """L-5 / L-6 的普查读数。

    波次 1 / 2 里调用方一律 info()、不判定(判据属计划 03);波次 3 起 item 9 消费同一份
    返回值做断言(`clearance` / `hits` 两个数组)。返回 `None` 表示普查脚本无返回。
    """
    data = page.evaluate(_IDI06_CENSUS_JS)
    if data is None:
        info(f"item8 [{state}] 普查", "<SKIPPED> 普查脚本无返回")
        return None
    info(f"item8 [{state}] L-5 clearance 普查(可聚焦元素 × 最近裁剪祖先 × 实测 clearance;阈值 4px)",
         f"{len(data['clearance'])} 对")
    for row in data["clearance"]:
        info(f"item8 [{state}] L-5 clearance",
             f"{row['el']} × {row['container']} = {row['clearance']:.1f}px "
             f"visible={row['visible']} intersects={row['intersects']} rect={row['rect']}")
    info(f"item8 [{state}] L-6 命中区普查(可交互元素 rect;阈值 24×24)",
         f"{len(data['hits'])} 个")
    for row in data["hits"]:
        info(f"item8 [{state}] L-6 命中区",
             f"{row['el']} w={row['w']:.1f} h={row['h']:.1f} "
             f"visible={row['visible']} below24={row['below24']}")
    return data


def item8(page, tmp_root):
    item = "8"
    print("\n=== UAT 8: L-1 徽标收口 —— 流内 badge + sticky 表头(D-06)===", flush=True)
    proj = make_fixture("p1", tmp_root)
    enter_project(page, proj)
    info("item8 样本", f"p1(会话流活动态,#state-badge 可见)→ {proj}")

    # ---- (a) badge 是流内元素(运行时 computed style,不读源码)-----------------
    # 元素读不到时 read_style 返回 None ⇒ ok() 自动记 BLOCKED,绝不记 PASS。
    # `right` 在未声明时的 computed 值是 `auto`。
    ok(item, "[p1] #state-badge position == static", "static",
       read_style(page, "#state-badge", "position"),
       "L-1 承重约束 1:流内机制一字不动")
    ok(item, "[p1] #state-badge right 无声明", "auto",
       read_style(page, "#state-badge", "right"),
       "L-1 承重约束 1:不得给它加 right(加回浮层会复活 LAYOUT-03 的遮挡)")

    # ---- (b) 三宽度下 badge × banner 不相交 -----------------------------------
    # 768 是承诺的窄窗口下限,必须补上(路线图 Success Criterion #2 原本只在 1024/1280 实检)。
    # try/finally:viewport 复位必须执行 —— 这是 harness 里**第一次**变更 viewport,
    # 不复位会污染其后所有项。
    try:
        for width in BADGE_BANNER_WIDTHS:
            page.set_viewport_size({"width": width, "height": 900})
            page.wait_for_timeout(250)
            # 用应用自身的 showStreamBanner(...) 让横幅可见 —— 不得手工
            # classList.remove('hidden') 拼 DOM,那是伪造被测状态(威胁面「应用 JS → harness」)。
            shown = page.evaluate(
                """(text) => {
                    if (typeof showStreamBanner !== 'function') return false;
                    showStreamBanner(text, false);
                    return true;
                }""",
                BANNER_TEXT,
            )
            if not shown:
                blocked(item, f"[p1 @{width}px] 横幅可见态已构造",
                        "showStreamBanner(text, false) 可调用", "<MISSING>",
                        "应用未导出 showStreamBanner,被测状态造不出")
                continue
            geo = page.evaluate(_IDI06_BADGE_BANNER_JS)
            if geo is None:
                blocked(item, f"[p1 @{width}px] badge × banner 几何读数",
                        "#state-badge 与 #stream-banner 都存在", "<MISSING>",
                        "元素不存在,getBoundingClientRect 读不出")
                continue
            badge, banner = geo["badge"], geo["banner"]
            info(f"item8 [{width}px] badge × banner 原始 rect",
                 f"badge={badge} display={geo['badgeDisplay']} | "
                 f"banner={banner} display={geo['bannerDisplay']}")
            # 前提检查:两个元素都真的被渲染出来(可见 + rect 非全零)。
            # 任一前提不成立 ⇒ blocked,绝不把「两个零矩形不相交」记成 PASS。
            if (
                geo["badgeDisplay"] == "none"
                or geo["bannerDisplay"] == "none"
                or badge["width"] <= 0
                or badge["height"] <= 0
                or banner["width"] <= 0
                or banner["height"] <= 0
            ):
                blocked(
                    item,
                    f"[p1 @{width}px] #state-badge 与 #stream-banner 不相交",
                    "两个元素均可见且 rect 宽高 > 0",
                    f"badge display={geo['badgeDisplay']} rect={badge} / "
                    f"banner display={geo['bannerDisplay']} rect={banner}",
                    "前提不成立(元素被隐藏或 rect 全零)⇒ 不相交判定是空转,不记 PASS",
                )
                continue
            ok_true(
                item,
                f"[p1 @{width}px] #state-badge 与 #stream-banner 不相交",
                not _rects_intersect(badge, banner),
                "不相交",
                f"badge={badge} banner={banner}",
                "L-1 的门断言几何不相交,不是「横幅不存在」",
            )
    finally:
        page.set_viewport_size(VIEWPORT_RESTORE)

    # ---- (c) 滚动 #doc-panel 到底后 #doc-panel-header 仍可见(sticky 生效)-------
    # 先把内容加长(经应用自身的 renderMarkdown,真实渲染路径),否则 p1 下
    # #doc-panel 内容可能不足一屏 ⇒「滚到底后仍可见」是空转断言。
    grown = page.evaluate(
        """(md) => {
            const doc = document.querySelector('#draft-content');
            if (!doc || typeof renderMarkdown !== 'function') return null;
            doc.innerHTML = '';
            doc.appendChild(renderMarkdown(md));
            const p = document.querySelector('#doc-panel');
            return p ? {scrollHeight: p.scrollHeight, clientHeight: p.clientHeight} : null;
        }""",
        LONG_DOC_MD,
    )
    if grown is None:
        blocked(item, "[p1] 滚动 #doc-panel 到底后 #doc-panel-header 仍可见(sticky)",
                "#draft-content 可注入长内容", "<MISSING>",
                "#draft-content 或 renderMarkdown 不可用")
    elif grown["scrollHeight"] <= grown["clientHeight"]:
        blocked(
            item,
            "[p1] 滚动 #doc-panel 到底后 #doc-panel-header 仍可见(sticky)",
            "scrollHeight > clientHeight(容器真的可滚)",
            f"scrollHeight={grown['scrollHeight']} clientHeight={grown['clientHeight']}",
            "#doc-panel 内容不足一屏,不可滚 ⇒「滚到底后仍可见」是空转断言,不记 PASS",
        )
    else:
        scrolled = page.evaluate(_IDI06_SCROLL_JS)
        if scrolled is None:
            blocked(item, "[p1] 滚动 #doc-panel 到底后 #doc-panel-header 仍可见(sticky)",
                    "#doc-panel 与 #doc-panel-header 都存在", "<MISSING>", "元素不存在")
        else:
            hp, pp = scrolled["header"], scrolled["panel"]
            info("item8 sticky 原始数值",
                 f"scrollTop={scrolled['scrollTop']} scrollHeight={scrolled['scrollHeight']} "
                 f"clientHeight={scrolled['clientHeight']} header={hp} panel={pp}")
            ok_true(
                item,
                "[p1] 滚动到底后 #doc-panel-header 仍落在 #doc-panel 可视区内",
                hp["bottom"] > pp["top"] and hp["top"] < pp["bottom"],
                "header.bottom > panel.top 且 header.top < panel.bottom",
                f"header={hp} panel={pp}",
                "sticky 生效:标题行钉在面板顶部而非随正文滚走",
            )
            ok_true(
                item,
                "[p1] sticky 把 #doc-panel-header 钉在 #doc-panel 顶部(<=1px)",
                abs(hp["top"] - pp["top"]) <= 1.0,
                "|header.top - panel.top| <= 1px",
                f"{abs(hp['top'] - pp['top']):.3f}px",
            )

    # ---- 三项只读诊断(计划 03 的输入契约;本计划一律 info(),不判定)------------
    injected = page.evaluate(
        """(md) => {
            const body = document.querySelector('#doc-panel-body');
            if (!body || typeof renderMarkdown !== 'function') return null;
            const d = document.createElement('div');
            d.id = 'idi06-overflow-probe';
            d.appendChild(renderMarkdown(md));
            body.appendChild(d);
            return true;
        }""",
        WIDE_MD,
    )
    if not injected:
        info("item8 L-2 三宽度溢出诊断", "<SKIPPED> #doc-panel-body 或 renderMarkdown 不可用")
        blocked(item, "[L-2] 三宽度溢出读数",
                "#doc-panel-body 与 renderMarkdown 均可用", "<MISSING>",
                "探针内容注入失败 ⇒ 三宽度判据读不出,不记 PASS")
    else:
        try:
            for width in (1440, 1024, 768):
                page.set_viewport_size({"width": width, "height": 900})
                page.wait_for_timeout(250)
                m = page.evaluate(_IDI06_OVERFLOW_JS)
                if m is None:
                    blocked(item, f"[@{width}px] L-2 文档级溢出读数",
                            "documentElement 与 #doc-panel 均可读", "<MISSING>",
                            "读数返回 null ⇒ 不记 PASS")
                    continue
                info(
                    f"item8 L-2 文档级溢出 @{width}px(波次 2 之后:L-3 / L-4 已落地;"
                    "面板内部横向滚动条不计入)",
                    f"scrollWidth={m['scrollWidth']} clientWidth={m['clientWidth']} "
                    f"overflow={m['scrollWidth'] - m['clientWidth']}px "
                    f"docPanelWidth={m['panelWidth']}",
                )
                # LAYOUT-02 的字面承诺「≥1024px 无横向溢出」—— 1440 与 1024 两处升为硬断言。
                # 768 处保持只读诊断:它在 LAYOUT-02 里的承诺是「无内容遮挡」,已由本项前面的
                # badge × banner 不相交断言覆盖(UI-SPEC §L-2 的判据表)。
                if width >= 1024:
                    ok_true(
                        item,
                        f"[@{width}px] 文档级 scrollWidth <= clientWidth",
                        m["scrollWidth"] <= m["clientWidth"],
                        "scrollWidth <= clientWidth",
                        f"{m['scrollWidth']} <= {m['clientWidth']}",
                        "LAYOUT-02 的字面承诺:≥1024px 无横向溢出",
                    )
                else:
                    info(f"item8 L-2 @{width}px",
                         "保持只读诊断(768px 处的承诺是「无内容遮挡」,"
                         "已由 badge × banner 不相交断言覆盖)")
                # L-2 的**判别性探针**(理由见 _IDI06_OVERFLOW_JS 的注释):面板实测宽不得
                # 超过它自己声明的 clamp 上界。这是「flex 项被长不可断内容顶破」这一失效模式
                # 的直接读数 —— 文档级 scrollWidth 对该模式结构性失明。
                if m["panelWidth"] is None:
                    blocked(item, f"[@{width}px] #doc-panel 实测宽 <= clamp() 上界",
                            f"<= {_doc_panel_declared_width(width):.1f}px", "<MISSING>",
                            "#doc-panel 不存在 ⇒ 不记 PASS")
                else:
                    expected_w = _doc_panel_declared_width(width)
                    ok_true(
                        item,
                        f"[@{width}px] #doc-panel 实测宽 <= clamp(340px, 30vw, 480px) 上界",
                        m["panelWidth"] <= expected_w + 1.0,
                        f"<= {expected_w:.1f}px",
                        f"{m['panelWidth']:.1f}px",
                        "L-2 的判别性探针:长不可断内容不得把面板顶得比它声明的宽还宽"
                        "(文档级 scrollWidth 对该失效模式结构性失明)",
                    )
        finally:
            page.set_viewport_size(VIEWPORT_RESTORE)

    # L-2 的守卫形态断言(静态,读 style.css 文件文本;不依赖 viewport)。
    _l2_guard_shape(item)

    # L-5 / L-6 普查跑两个样本:p1 让 #session-panel / #chat-messages 可见,
    # p3(补渲染一条批注)让 #annotations-panel / #annotation-list 与其中的
    # `<summary>` 可见 —— 被祖先藏住的元素 rect 全零,普查会失真。
    for state, with_annotations in (("p1", False), ("p3", True)):
        proj_c = make_fixture(state, tmp_root)
        enter_project(page, proj_c)
        if with_annotations:
            page.evaluate(
                """() => {
                    if (typeof renderAnnotations !== 'function') return false;
                    renderAnnotations({items: [{
                        id: 'idi06-census', type: 'plain', status: 'answered',
                        quote: '普查探针摘录', note: '普查探针正文', answer: '普查探针回答',
                    }]}, true);
                    return true;
                }"""
            )
        _idi06_census(page, state)


# ---------------------------------------------------------------------------
# UAT 第 9 项 — L-4 滚动容器收敛(D-14 / LAYOUT-04)
# ---------------------------------------------------------------------------
# 三件事(UI-SPEC §L-4 的门):
#   (a) 面板区(`#main-pane` 及其**全部后代**)内计算 `overflow-y` 为 `auto` / `scroll`
#       的元素集合恰为 `{#main-pane, #chat-messages, #latest-check}`;排除 SC#3 明文豁免的
#       `#chat-messages` 之后恰为 `{#main-pane, #latest-check}`;
#   (b) `#main-pane` 与 `#latest-check` 滚到底后末条内容可达;
#   (c) `#ai-events` / `#annotation-list` 的计算 `max-height` 为 `none`。
# 另含两条**保留项护栏**(D-11 的保留理由是承重约束,不是风格偏好,故必须机器化):
#   `#chat-messages` 的 `overflow-y` 按**计算样式**断言为 `auto` —— `auto` 是关键字值,
#   `getComputedStyle` 逐字返回它,读法成立;
#   `#latest-check` 的限高按**源码文本计数**断言为 1 —— `getComputedStyle` 对 `vh` 返回的
#   是解析后的**用值(px)**(1440×900 下 `30vh` → `270px`),断言 `== "30vh"` 是一条
#   **恒 FAIL** 的断言,会让本项永远无法转绿。两条护栏互补:前者抓「保留项被改值」,
#   后者抓「保留项被悄悄删掉」。
#
# 波次 3(D-13 / D-17)另加两条**普查断言**,均按 DOM 遍历算出、不硬编码选择器列表:
#   (f) L-5:每个裁剪容器 × 其每个可聚焦后代的实测 clearance >= 4px;
#   (g) L-6:每个可交互元素的计算盒宽与高均 >= 24px(主要对象 `.annotation-answer summary`
#       须先经应用自身的 renderAnnotations 造出并断言存在,否则断言失去证明力)。
# 两条在三样本(p1 / checking / p3)上跑,以覆盖全部裁剪容器 —— 被祖先藏住的元素 rect
# 全零,单样本会把「藏住」静默读成「不达标」(T-idi-06-01 的假 PASS 落点)。
#
# 普查的**状态无关性**:七个 `overflow` 声明所在的元素全部是 `index.html` 的静态元素
# (`#main-pane` / `#doc-panel` / `#ai-events` / `#chat-messages` / `#annotation-list` /
# `#latest-check`),与磁盘状态样本无关,故普查在 `p1` 下得到的结论对五个样本同样成立 ——
# 这是本断言比「按状态样本逐格探」更强的地方(也正是不必逐样本重跑的原因)。
#
# 两个样本各出一半**可达性**证据:`#main-pane` 要 `#ai-events` 可见(仅 p1),
# `#latest-check` 要 `#checks-panel` 可见(仅 checking)。在错误的样本上读到的 rect 全零,
# 那正是本阶段威胁表 T-idi-06-10(假 PASS)的落点,故两条都带显式前提检查。
PANEL_SCROLLERS = ("#chat-messages", "#latest-check", "#main-pane")
# SC#3 明文豁免的会话流滚动者(D-14 第 1 条:排除它之后「恰好两个」)。
PANEL_SCROLLERS_EXEMPT = ("#chat-messages",)
STYLE_CSS = ROOT / "frontend" / "style.css"
# ---- L-5 / L-6 两条普查断言的阈值(波次 3 落地)-------------------------------
# L-5:裁剪容器的每个可聚焦后代距其 padding 边 >= 4px(= Phase 7 的
# `outline: 2px solid` + `outline-offset: 2px` 的环外伸量)。本阶段只为它**解裁切**,
# 不写任何焦点规则。
CLEARANCE_MIN_PX = 4.0
# L-6:每个可交互元素的计算盒宽与高均 >= 24px(WCAG 2.5.8 目标尺寸,AA;按字面走尺寸,
# 不走 2.5.8 的间距例外 —— A11Y-07 明文要求「达到 24×24」)。
TARGET_MIN_PX = 24.0
# `.annotation-answer summary` 在普查里的标签(无 id、无 class 的 `<summary>` 即此形态)。
SUMMARY_TAG = "summary"
# 保留项护栏读的源码文本(D-11:去掉限高会把裁决按钮推出视口)。
LATEST_CHECK_MAX_HEIGHT_DECL = "max-height: 30vh;"
# `#latest-check` 的可达性探针正文(经应用自身的 renderMarkdown 渲染 60 次)。
LATEST_CHECK_PROBE_MD = (
    "## 探针核查段落\n\n"
    "这是一段足够长的自检报告探针正文,用于把 `#latest-check` 撑到可滚,"
    "使末条可达性断言不是空转。\n"
)

# 滚动者普查:遍历 `#main-pane` **及其全部后代**,读每个元素的计算 `overflow-y`。
# 按 **DOM 遍历**算出,不硬编码选择器列表(PATTERNS.md E-5 第 1 条纪律)。
_IDI06_SCROLLERS_JS = """() => {
  const root = document.querySelector('#main-pane');
  if (!root) return null;
  const labelOf = (el) => {
    if (el.id) return '#' + el.id;
    const cls = (typeof el.className === 'string' && el.className.trim())
      ? '.' + el.className.trim().split(/\\s+/).join('.') : '';
    return el.tagName.toLowerCase() + cls;
  };
  const out = [];
  [root, ...root.querySelectorAll('*')].forEach((el) => {
    const oy = getComputedStyle(el).overflowY;
    if (oy === 'auto' || oy === 'scroll') out.push(labelOf(el));
  });
  return out;
}"""

# 末条可达性:读 scrollHeight / clientHeight → 滚到底 → 读容器与末条子元素的 rect。
# 元素不存在返回 null ⇒ 调用方记 blocked(),绝不记假 PASS。
_IDI06_REACH_JS = """(sel) => {
  const c = document.querySelector(sel);
  if (!c) return null;
  const scrollHeight = c.scrollHeight;
  const clientHeight = c.clientHeight;
  c.scrollTop = scrollHeight;
  const rc = c.getBoundingClientRect();
  const last = c.lastElementChild;
  const rl = last ? last.getBoundingClientRect() : null;
  const label = last
    ? (last.id ? '#' + last.id
       : last.tagName.toLowerCase() + ((typeof last.className === 'string' && last.className.trim())
         ? '.' + last.className.trim().split(/\\s+/).join('.') : ''))
    : null;
  return {
    scrollHeight: scrollHeight, clientHeight: clientHeight, scrollTop: c.scrollTop,
    display: getComputedStyle(c).display,
    container: {top: rc.top, bottom: rc.bottom, left: rc.left, right: rc.right,
                width: rc.width, height: rc.height},
    last: rl ? {top: rl.top, bottom: rl.bottom, left: rl.left, right: rl.right,
                width: rl.width, height: rl.height} : null,
    lastLabel: label,
  };
}"""


def _latest_check_max_height_guard(item):
    """D-11 保留项护栏(静态):`#latest-check` 的 `max-height: 30vh;` 仍在。

    按**源码文本**计数,不读计算样式 —— 理由见本节头注释。读法与
    `check_render_markdown_call_sites` 同族:脚本自己从文件文本算,不依赖 shell 管道。
    """
    try:
        text = STYLE_CSS.read_text(encoding="utf-8")
    except OSError as exc:
        blocked(item, "[static] frontend/style.css 的 max-height: 30vh 声明计数 == 1",
                "1", "<MISSING>", f"{STYLE_CSS} 读不到:{exc}")
        return
    count = text.count(LATEST_CHECK_MAX_HEIGHT_DECL)
    lines = [i for i, ln in enumerate(text.splitlines(), 1)
             if LATEST_CHECK_MAX_HEIGHT_DECL in ln]
    info("item9 [static] #latest-check 保留项护栏",
         f"frontend/style.css 里 '{LATEST_CHECK_MAX_HEIGHT_DECL}' 计数={count} 命中行={lines}")
    ok_true(item, "[static] frontend/style.css 的 max-height: 30vh 声明计数 == 1",
            count == 1, 1, count,
            "删掉它会去掉 #latest-check 的内部滚动、把裁决按钮推出视口 ⇒ "
            "若要改口径,先更新本断言与 UI-SPEC §L-4 的保留理由")


def _idi06_reach(page, item, sel, sample, injected, inject_error):
    """末条可达性(D-14 第 2 条)。

    前提链:内容已注入 → 容器存在 → 容器**可见且 rect 高 > 0**。任一前提不成立记
    `blocked(...)` —— 被祖先藏住的容器 rect 全零,「末条落在容器内」会平凡成立,
    那是一条空转 PASS(威胁表 T-idi-06-10),与 item7 已登记的 `all(w != "700")`
    对 `None` 恒真是同型陷阱。
    """
    label = f"[{sample}] {sel} 末条内容可达"
    if injected is None:
        blocked(item, label, "内容经应用自身的渲染路径注入", "<MISSING>", inject_error)
        return
    geo = page.evaluate(_IDI06_REACH_JS, sel)
    if geo is None:
        blocked(item, label, f"{sel} 存在", "<MISSING>", "元素不存在")
        return
    if geo["display"] == "none" or geo["container"]["height"] <= 0:
        blocked(item, label, "容器可见且 rect 高 > 0",
                f"display={geo['display']} rect={geo['container']}",
                "容器被祖先藏住 ⇒ 几何读数全零,可达性判定是空转,不记 PASS")
        return
    info(f"item9 {label} 原始数值",
         f"scrollHeight={geo['scrollHeight']} clientHeight={geo['clientHeight']} "
         f"scrollTop={geo['scrollTop']} last={geo['lastLabel']} lastRect={geo['last']} "
         f"container={geo['container']}")
    if geo["scrollHeight"] <= geo["clientHeight"]:
        info(f"item9 {label}",
             "容器无需滚动,可达性平凡成立(不记断言,避免空转 PASS)")
    else:
        ok_true(item, f"[{sample}] {sel} 滚到底(scrollTop + clientHeight >= scrollHeight - 1)",
                geo["scrollTop"] + geo["clientHeight"] >= geo["scrollHeight"] - 1,
                f">= {geo['scrollHeight'] - 1}",
                f"{geo['scrollTop'] + geo['clientHeight']}")
    if geo["last"] is None:
        blocked(item, f"[{sample}] {sel} 末条子元素落在容器可视区内",
                "容器有子元素", "<MISSING>",
                "末条读不到 ⇒ 可达性判定是空转,不记 PASS")
        return
    # 承重判据:末条元素的**下边缘**落在容器可视带内(上界 +1px 容差吸收子像素),
    # 且不低于容器上边缘(内容末端没被滚过头)。
    # 为何不写成 `last.top >= container.top - 1`:当末条子元素本身**高于**容器
    # (p1 下 `#main-pane` 的末条 `#ai-panel` 实测高 2434px > 容器 900px)时,该式
    # 恒不成立 —— 那是一条恒 FAIL 的断言,与 `max-height == "30vh"` 同类。真正的
    # 主张是「内容末端可达」,即下边缘落在可视带内;上边缘属于被滚动遮住的部分,
    # 不影响末端可达性。
    ok_true(item, f"[{sample}] {sel} 末条子元素落在容器可视区内",
            geo["last"]["bottom"] <= geo["container"]["bottom"] + 1
            and geo["last"]["bottom"] >= geo["container"]["top"],
            "container.top <= last.bottom <= container.bottom + 1",
            f"last.bottom={geo['last']['bottom']} "
            f"container=[{geo['container']['top']}, {geo['container']['bottom']}]",
            "内容末端可达:末条不被限高截断到可视区之外")


def _idi06_clearance_assert(page, item, state):
    """L-5 的 clearance 普查断言(D-13):每个裁剪容器 × 其可聚焦后代的实测 clearance >= 4px。

    按 **DOM 遍历**算出,不硬编码选择器列表。只判定**当前落在容器可视滚动区内**的行:
    与 padding 盒完全不相交的元素被滚动到视口之外,当前不渲染,其负 clearance 是噪声
    (见 `_IDI06_CENSUS_JS` 里 `intersects` 的注释);相交却越界才是真裁切,clearance 为负。
    """
    data = page.evaluate(_IDI06_CENSUS_JS)
    if data is None:
        blocked(item, f"[{state}] L-5 每个裁剪容器 × 可聚焦后代的 clearance >= {CLEARANCE_MIN_PX:.0f}px",
                "普查脚本返回数据", "<MISSING>", "普查无返回 ⇒ 不记 PASS")
        return
    rows = data["clearance"]
    info(f"item9 [{state}] L-5 clearance 普查(全部原始行)",
         f"{len(rows)} 对:"
         f"{[(r['el'], r['container'], round(r['clearance'], 1), r['visible'], r['intersects']) for r in rows]}")
    judged = [r for r in rows if r["visible"] and r["intersects"]]
    if not judged:
        info(f"item9 [{state}] L-5 clearance",
             "无「裁剪容器 × 可聚焦后代」组合落在可视滚动区内 ⇒ 本样本无判定"
             "(不记断言,避免空转 PASS)")
        return
    bad = [r for r in judged if r["clearance"] < CLEARANCE_MIN_PX]
    ok_true(item,
            f"[{state}] L-5 每个裁剪容器 × 可聚焦后代的 clearance >= {CLEARANCE_MIN_PX:.0f}px",
            not bad, f"全部 >= {CLEARANCE_MIN_PX:.0f}px",
            f"共 {len(judged)} 行,未达标 "
            f"{[(r['el'], r['container'], round(r['clearance'], 1)) for r in bad]}",
            "4px = Phase 7 的 outline: 2px + outline-offset: 2px 的环外伸量。"
            "实测未达标时**只改那一个容器**的 padding 为 var(--space-1),"
            "禁止「为确定性四个全抬」(UI-SPEC §L-5 的决策规则)")


def _idi06_hit_assert(page, item, state, require_summary):
    """L-6 的命中区普查断言(D-17):每个可交互元素的计算盒宽与高均 >= 24px。

    `require_summary=True` 时先断言 `.annotation-answer summary` 存在且可见 —— 它是本
    断言的**主要对象**(全文件唯一实测不达标的可交互元素)。元素读不到时
    `getBoundingClientRect()` 返回全零矩形,断言会退化成一条空转 PASS;复刻 item7 已登记的
    `all(w != "700")` 对 `None` 恒真的陷阱,故不成立即 blocked(...)。
    """
    data = page.evaluate(_IDI06_CENSUS_JS)
    if data is None:
        blocked(item, f"[{state}] 每个可交互元素的计算盒宽高均 >= {TARGET_MIN_PX:.0f}px",
                "普查脚本返回数据", "<MISSING>", "普查无返回 ⇒ 不记 PASS")
        return
    rows = [r for r in data["hits"] if r["visible"]]
    info(f"item9 [{state}] L-6 命中区普查(可见行;阈值 24×24)",
         f"{len(rows)} 个:"
         f"{[(r['el'], r['w'], r['h']) for r in rows]}")
    if require_summary:
        summary_rows = [r for r in rows if r["el"].split(".")[0] == SUMMARY_TAG]
        if not summary_rows:
            blocked(item,
                    f"[{state}] .annotation-answer summary 已由 renderAnnotations 造出且可见",
                    ">= 1 个可见的 <summary>", "<MISSING>",
                    "本断言的主要对象不存在 ⇒ 命中区断言失去证明力,不记 PASS")
            return
        info(f"item9 [{state}] 命中区断言的主要对象",
             f"<summary> 实测 {[(r['el'], r['w'], r['h']) for r in summary_rows]}")
    bad = [r for r in rows if r["w"] < TARGET_MIN_PX or r["h"] < TARGET_MIN_PX]
    ok_true(item,
            f"[{state}] 每个可交互元素的计算盒宽高均 >= {TARGET_MIN_PX:.0f}px",
            not bad, f"全部 >= {TARGET_MIN_PX:.0f}px",
            f"共 {len(rows)} 行,未达标 {[(r['el'], r['w'], r['h']) for r in bad]}",
            "WCAG 2.5.8 按字面走尺寸,不走间距例外。未达标者只补 min-height / min-width "
            "两条声明(机制锁定,见 UI-SPEC §L-6),不动 padding、不用 ::after 撑开")


def item9(page, tmp_root):
    item = "9"
    print("\n=== UAT 9: L-4 面板区滚动容器收敛(D-14)===", flush=True)

    # ---- (a) 滚动者 DOM 普查 + (c) 两处限高消失 + (d) 保留项护栏 ---------------
    proj = make_fixture("p1", tmp_root)
    enter_project(page, proj)
    info("item9 样本", f"p1(会话流活动态,#session-panel / #ai-events 可见)→ {proj}")

    scrollers = page.evaluate(_IDI06_SCROLLERS_JS)
    expected_all = sorted(PANEL_SCROLLERS)
    if scrollers is None:
        blocked(item, "[p1] 面板区滚动者集合(#main-pane 及其全部后代)",
                expected_all, "<MISSING>",
                "#main-pane 不存在,普查无法跑 ⇒ 不记 PASS")
    else:
        info("item9 [p1] 面板区滚动者普查(实测数组)",
             f"{len(scrollers)} 个:{scrollers}")
        if "#main-pane" not in scrollers:
            blocked(item, "[p1] 面板区滚动者集合(#main-pane 及其全部后代)",
                    expected_all, scrollers,
                    "实测结果里没有 #main-pane ⇒ 探针跑错了范围,不记 PASS")
        else:
            actual = sorted(scrollers)
            ok_true(item,
                    "[p1] 面板区滚动者集合 == {#main-pane, #chat-messages, #latest-check}",
                    actual == expected_all, expected_all, actual,
                    "口径取「恰好」而非「至多」:意外新增第四个滚动者会在这里 FAIL")
            exempted = sorted(s for s in scrollers if s not in PANEL_SCROLLERS_EXEMPT)
            expected_exempted = sorted(
                s for s in PANEL_SCROLLERS if s not in PANEL_SCROLLERS_EXEMPT)
            ok_true(item,
                    "[p1] 排除 #chat-messages(SC#3 明文豁免)后 == {#main-pane, #latest-check}",
                    exempted == expected_exempted, expected_exempted, exempted,
                    "D-14 第 1 条的字面读法:面板区内恰好两个滚动容器")

    # 读计算样式即可 —— `getComputedStyle` 对 `display: none` 的元素同样返回解析后的值
    # (computed style 不依赖布局),故 `#annotation-list` 在 p1 下(被祖先藏住)这两条
    # 依然有效,无需为它切样本。
    ok(item, "[p1] #ai-events 计算 max-height == none", "none",
       read_style(page, "#ai-events", "max-height"),
       "L-4:套娃第一层(55vh 限高 + 内滚动)已原地删除")
    ok(item, "[p1] #annotation-list 计算 max-height == none", "none",
       read_style(page, "#annotation-list", "max-height"),
       "L-4:套娃第二层(32vh 限高 + 内滚动)已原地删除")

    ok(item, "[p1] #chat-messages overflow-y == auto", "auto",
       read_style(page, "#chat-messages", "overflow-y"),
       "D-12:输入行必须钉底,会话流滚动者按保留项对待")
    _latest_check_max_height_guard(item)

    # ---- (b) 末条可达性(D-14 第 2 条)---------------------------------------
    # `#main-pane`:经应用自身的 renderEvent 注入足量条目到 #ai-events(不手工拼 DOM)。
    grown = page.evaluate("""() => {
        const list = document.querySelector('#ai-events');
        if (!list || typeof renderEvent !== 'function') return null;
        for (let i = 0; i < 40; i++) {
          renderEvent({kind: 'say', content: '第 ' + i + ' 条可达性探针:把面板撑到可滚。'});
        }
        return document.querySelectorAll('#ai-events .event-item').length;
    }""")
    _idi06_reach(page, item, "#main-pane", "p1", grown,
                 "#ai-events 或 renderEvent 不可用")

    # `#latest-check`:`#checks-panel` 只在 checking 样本可见 —— p1 下它的 rect 全零,
    # 前提检查会记 BLOCKED 而不是记一条假 PASS。
    proj_c = make_fixture("checking", tmp_root)
    enter_project(page, proj_c)
    info("item9 样本",
         f"checking(自检报告态,#checks-panel / #latest-check 可见)→ {proj_c}")
    grown_lc = page.evaluate("""(md) => {
        const c = document.querySelector('#latest-check');
        if (!c || typeof renderMarkdown !== 'function') return null;
        c.innerHTML = '';
        for (let i = 0; i < 60; i++) c.appendChild(renderMarkdown(md));
        return c.childElementCount;
    }""", LATEST_CHECK_PROBE_MD)
    _idi06_reach(page, item, "#latest-check", "checking", grown_lc,
                 "#latest-check 或 renderMarkdown 不可用")

    # ---- (f) L-5 clearance 普查断言 + L-6 命中区普查断言(D-13 / D-17)-----------
    # 两条都按 **DOM 遍历**算出,不硬编码选择器列表。三样本合起来才覆盖全部
    # 「裁剪容器 × 可聚焦后代」组合:p1 覆盖 #main-pane / #doc-panel / #chat-messages,
    # checking 覆盖 #latest-check,p3 覆盖批注面板里的 `<summary>`(它只在批注面板可见时
    # 才有非零 rect —— 被祖先藏住的元素 rect 全零,单样本会把「藏住」读成「不达标」)。
    for state in ("p1", "checking"):
        proj_c = make_fixture(state, tmp_root)
        enter_project(page, proj_c)
        _idi06_clearance_assert(page, item, state)
        _idi06_hit_assert(page, item, state, require_summary=False)

    # p3(补渲染一条批注):L-6 的主要对象 `.annotation-answer summary` 经应用自身的
    # renderAnnotations 造出 —— 不手工拼 DOM,那是伪造被测状态。
    proj_p3 = make_fixture("p3", tmp_root)
    enter_project(page, proj_p3)
    info("item9 样本",
         f"p3(批注面板可见态,#annotations-panel / #annotation-list 可见)→ {proj_p3}")
    built = page.evaluate(
        """() => {
            if (typeof renderAnnotations !== 'function') return false;
            renderAnnotations({items: [{
                id: 'idi06-a11y-probe', type: 'plain', status: 'answered',
                quote: '命中区普查探针摘录', note: '命中区普查探针正文',
                answer: '命中区普查探针回答',
            }]}, true);
            return true;
        }"""
    )
    if not built:
        blocked(item, "[p3] .annotation-answer summary 已由 renderAnnotations 造出且可见",
                "renderAnnotations(items, true) 可调用", "<MISSING>",
                "应用未导出 renderAnnotations ⇒ 被测状态造不出,不记 PASS")
    _idi06_clearance_assert(page, item, "p3")
    _idi06_hit_assert(page, item, "p3", require_summary=True)

    # ---- (e) viewport 纪律 ---------------------------------------------------
    # 本项不变更 viewport;此处是兜底复位(若调试期用过 set_viewport_size),
    # 与 item 8 同一纪律:VIEWPORT_RESTORE 是 harness 的基准视口,不复位会污染其后各项。
    page.set_viewport_size(VIEWPORT_RESTORE)


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
    # 令牌接线(R-1 / R-2 / R-3):围栏外三处声明必须真的接上围栏内的令牌。
    # 判据取「消费者 computed 值 == 令牌运行时值」,值层再改也不产生假 FAIL。
    z_token = resolve_token(page, "--z-badge")
    info("smoke 令牌解析", f"--z-badge={z_token}")
    ok(item, "smoke #state-badge z-index == var(--z-badge)",
       z_token, read_style(page, "#state-badge", "z-index"))
    shadow = read_style(page, ".overlay-card", "box-shadow")
    ok_contains(item, "smoke .overlay-card box-shadow 接上 var(--shadow-overlay)",
                "0.2", shadow, "needle 只用短串 0.2,不复用 item3 的完整 rgba 字面")
    ok(item, "smoke .tier-desc opacity == 1(R-3 已删除 opacity: 0.9)",
       "1", read_style(page, ".tier-desc", "opacity"))
    # VISUAL-04 快速切片:p3 样本下活动面板是 #annotations-panel(3px 竖条 + 标题变色)。
    check_active_marker(page, item, "[smoke p3]", "#annotations-panel")
    # 透明记录:UAT/PLAN 里写的字面值 rgb(31,99,189) 是 260918-qrq 换肤前的 --blue-700;
    # 该字面值由 UAT 第 3 项逐字断言,故此处只作 INFO,不参与本切片的判定。
    info("smoke UAT 字面值对照",
         "#state-badge color 的 UAT 字面期望 rgb(31,99,189) 实测="
         f"{read_style(page, '#state-badge', 'color')} —— 差异由 260918-qrq 令牌值换肤引入,"
         "该字面断言在第 3 项逐字执行")
    # G-idi-05-1 的快速切片:用应用自身的 appendChatMessage 造一个 .chat-bubble,
    # 其中的 h1 必须取嵌入刻度最高档 --text-xl(24px),不再是 UA 默认的 32px。
    bubble_ok = page.evaluate("""(md) => {
        if (typeof appendChatMessage !== 'function') return false;
        appendChatMessage('ai', md);
        return !!document.querySelector('.chat-bubble h1');
    }""", "# 探针")
    if not bubble_ok:
        blocked(item, "smoke .chat-bubble h1 已渲染", "appendChatMessage('ai', ...) 产出 .chat-bubble h1",
                "<未渲染>", "appendChatMessage 未产出 .chat-bubble h1")
    else:
        ok(item, "smoke .chat-bubble h1 font-size == var(--text-xl)",
           resolve_token(page, "--text-xl"), read_style(page, ".chat-bubble h1", "font-size"))


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def parse_args():
    ap = argparse.ArgumentParser(add_help=True, description="idi-04 UAT browser harness")
    ap.add_argument("--item", action="append", default=None,
                    help="只跑指定项:smoke / 1 / 2 / 3 / 4 / 5 / 6 / 7 / 8 / 9(可重复,或逗号分隔)")
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
        return ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
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
    known = {"smoke", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
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
        if "7" in items:
            item7(page, tmp_root)
        if "8" in items:
            item8(page, tmp_root)
        if "9" in items:
            item9(page, tmp_root)
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
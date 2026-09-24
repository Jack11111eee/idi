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
    .venv/bin/python scripts/check-05-ui-uat.py                 # 跑 UAT 第 1..10 项
    .venv/bin/python scripts/check-05-ui-uat.py --item smoke    # 只跑 harness 自检切片
    .venv/bin/python scripts/check-05-ui-uat.py --item 7        # 只跑渲染目标的标题刻度
    .venv/bin/python scripts/check-05-ui-uat.py --item 8        # 只跑 sticky 表头 / 流内 badge
    .venv/bin/python scripts/check-05-ui-uat.py --item 9        # 只跑面板区滚动容器收敛
    .venv/bin/python scripts/check-05-ui-uat.py --item 10       # 只跑焦点环覆盖与交互态
    .venv/bin/python scripts/check-05-ui-uat.py --item 1 --item 2
    .venv/bin/python scripts/check-05-ui-uat.py --ai-smoke      # 额外真跑两次 AI 交互冒烟
    .venv/bin/python scripts/check-05-ui-uat.py --keep          # 保留临时工作目录供排查
    .venv/bin/python scripts/check-05-ui-uat.py --browser chrome  # 改用系统 Chrome(有头)

第 10 项(A11Y-01 / INTERACT-01 / INTERACT-02)
    全站焦点环的**元素普查** + SC1 / SC2 / SC4 三条运行时探针。断言分两段:
    「静态契约计数」(令牌声明与消费的计数)与「运行时元素普查」(真实 Chrome 里的
    环读数)。普查口径**不是**「规则被写下了」,而是「**判定集(可见 ∧ 可聚焦,即
    Tab 可达)里未被环覆盖的元素数为 0,且判定集非空**」—— 按选择器计数只证明规则
    存在,而「枚举会漏项」正是焦点规则选择枚举路线的已知代价,门必须正面回答它。
    判定集有两条过滤(`visible` / `focusable`)。`focusable` 排除禁用控件与
    `tabindex="-1"`:它们 rect 非零、确实渲染在树里,却不在顺序焦点序里,**永远无法
    被 Tab 覆盖** —— 拿它们去要求「被环覆盖」会造出一条永远无法满足的判据。
    `#btn-approve-draft` / `#btn-authorize` 是这类真实实例(标记里带 `disabled`)。
    本判据是 **Reachable**,不是 Exists。

    已显式登记的事实:**五个状态样本(`scripts/ui-states/` 的 p1 / p12 / p3 /
    checking / archive)的 `#round-doc` 内 `a[href]` 计数为 0** ⇒ 归档半场
    (`.archive-mode` 的 0.75 合成)的**运行时**断言今天没有服务对象。它由常驻算术门
    (`check-02` 的 `--color-focus ON --color-surface NON-TEXT@0.75` 条目)+ 一次性
    反事实探针(`scripts/probe-07-focus-composite.py`,不进守卫契约)共同承担。
    不登记这个事实,读者会把「没有断言」误读成「没有风险」。

第 10 项的交互态半场(INTERACT-01 / D-08 / D-09 / D-10,计划 02 追加)
    SC5 / SC5-朴素按下 / SC5′ 三条运行时探针 + 输入控件的 hover 边界断言。
    - **SC5**(p1):`#btn-send` hover 时 `background-color` **不变**、`box-shadow` 出现
      `inset 0 0 0 999px <--color-overlay-hover>`,按住不放时叠层换成
      `--color-overlay-active`(alpha 0.06 → 0.12);`#message-input` hover 时
      `border-color` 加深到 `--color-border-hover`。
    - **SC5-朴素按下**(checking):用应用自身的 `renderVerdictCard()` 造一张裁决卡,对它
      的首个按钮读三次 `background-color` —— 静默 `--color-surface` → 悬停
      `--color-surface-hover` → 按住不放 `--color-surface-active`,并断言**③ != ②**。
      最后那半条是 D-09 的判据本体:没有 L587 的 `:where(:not(:active))` 让位时,③ 会读到
      ② 的值,而「③ == surface-active」那条断言仍然成立 ⇒ 只断言相等时失效的实现不变红。
    - **SC5′**(checking,复用同一张卡):把两个裁决按钮的 `.disabled` 置真
      (app.js:718-719 的真实状态切换),断言 hover 时 `background-color` 与静默**相同**
      (D-07 的 gate 生效证明),且计算 `opacity` 仍为 `0.5`(未被软化)。
    - 三条探针读值前**都必须先断言目标存在、可见且未被禁用**:一个渲染出来的禁用按钮照样
      有非零 rect,却永远不匹配 `:not(:disabled)` 的选择器 —— 「可见」不等于「可交互」,
      拿它做断言会 FAIL 而非 BLOCKED(本计划最初的探针目标正是这样写错的)。
      读完后**先把指针移开再抬手**(`page.mouse.move(0, 0)` 之后才 `page.mouse.up()`):
      在裁决按钮或 `#btn-send` 上原地上抬会触发 click,真的发请求并改动样本状态。

第 10 项的过渡与减弱动效半场(INTERACT-02 / D-11 / D-12 / D-13 / D-14,计划 03 追加)
    两段,与上面那些探针互补:**静态契约计数**先跑(不依赖任何运行时状态),**运行时
    过渡读数**在 p1 跑。
    - **静态契约计数**(`_idi07_focus_contract_guards`)四条:①`:focus-visible` 计数
      `>= EXPECTED_FOCUS_VISIBLE_MIN`(判据是 `>=`,不是 `==`;**只数代码** —— 注释
      提及不计,否则整条规则删光后计数仍 >= 1,断言会与它守的东西脱钩);②**没有任何含
      `:focus-visible` 的规则块设置 `border` / `padding`** —— 这条必须做**块提取**
      (逐行跟踪注释状态,从选择器行切到第一个 `}`),全文件 grep 会数到满地的
      `border` / `padding`,回答不了「焦点规则自己设了没有」;③`prefers-reduced-motion`
      与新增过渡**同时存在**;④五个交互态令牌**围栏内声明恰好一次 ∧ 围栏外被消费**
      (硬规则 5 的机械形态,用与 check-01 同一对围栏标记切分)。
    - ⚠ **第 ③ 条不证明「同提交」。** 「同提交」是 **git 维度**的事实,文件文本断言在
      结构上无法证明它 —— 该断言只退化为「两者同时存在」,局限在 `info()` 里逐字声明。
      同提交只能落成计划 / 评审义务(见 `idi-07-03-PLAN.md` Task 1 的 `<verify>`/`<done>`)。
    - **运行时过渡读数**(`_idi07_transition_motion_assert`,p1):button / input / select
      的 `transition-property` 含 `background-color` 与 `border-color`、时长 0.12s;
      `.event-list` 是 `background-color` 与 **0.3s**(D-11 的具名例外在运行时可见)。
      随后 `page.emulate_media(reduced_motion="reduce")` 重读四个元素的
      `transition-duration`,断言**全为 0s**;读毕**立即复位** `reduced_motion=
      "no-preference"`(与 `VIEWPORT_RESTORE` 同级纪律,否则污染其后各项)。
    - 时长判据先把 `transition-duration` 拆成列表再逐项比,**不用子串包含**:
      两个属性序列化成 `"0.12s, 0.12s"`,而 `"0s"` 是它的子串 —— 子串判据会让
      「reduce 下必须全为 0s」在**未生效**时假绿。

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


# L-2 的决策(Phase 6 实测结论,见 `idi-06-03-SUMMARY.md` 的「测量决策记录(最终态)」):
# 1440 / 1024 / 768 三处在波次 2 之后的树上均无破版 ⇒ 按 UI-SPEC §L-2 的决策规则第一支,
# **L-2 的窄窗口守卫不写**,该交付物登记为「被实测推翻」。
#
# ⚠ 计数**现在是 1**,但它与上面那件事**不是同一件事**:Phase 7 落地了
# `@media (prefers-reduced-motion: reduce)`(减弱动效偏好),那是本阶段 INTERACT-02 /
# D-13 的交付物。**L-2 的窄窗口守卫仍未写出**(三宽度仍无破版,该结论未变)。把两者混为
# 一谈会让后来者把「计数 == 1」读成「L-2 的守卫被写了」。
#
# 耦合(D-13 / T-idi-07-13):本常量与 frontend/style.css 里那个减弱动效媒体块的计数是
# 一对同步量。**若日后有人删掉该媒体块,必须同时把这里改回 0**,否则本项静态守卫会误报。
MEDIA_QUERY_DECL = "@media"
EXPECTED_MEDIA_QUERIES = 1


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
         f"Phase 7 的减弱动效媒体块 ⇒ 期望 {EXPECTED_MEDIA_QUERIES}"
         f"(L-2 的窄窗口守卫仍走「被实测推翻」支、仍未写出 —— 两者不是同一件事)")
    ok_true(item,
            "[static] frontend/style.css 的 @media 出现次数 == 决策"
            "(Phase 7 的 prefers-reduced-motion 块 ⇒ 1;L-2 的窄窗口守卫仍未写出)",
            count == EXPECTED_MEDIA_QUERIES, EXPECTED_MEDIA_QUERIES, count,
            "该断言读文件文本而非渲染结果,与几何断言互补。删掉那个减弱动效媒体块"
            "必须把本常量改回 0;L-2 的窄窗口守卫若日后实测证成并写出,须同步改本常量"
            "与 idi-06-03-SUMMARY.md 的决策记录")

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

# 焦点规则的枚举集(D-05)。**逐字**等于 `frontend/style.css` 文件末尾那条
# `:focus-visible` 规则的选择器列表(顺序亦同)。两侧必须同时改:新增一类可聚焦元素要
# 改两处(CSS 那一处 + 本常量),只改一处会让「规则覆盖了谁」与「门检查了谁」重新分叉,
# 而那正是 G-idi-05-1 的成因。
#
# **本文件这一侧只有这一处。** 下面两份普查脚本(item 9 的 `_IDI06_CENSUS_JS` 与第 10
# 项的 `_IDI07_FOCUS_CENSUS_JS`)的 `document.querySelectorAll(...)` 参数都经
# `_focusable_census_js()` 用本常量生成 —— 故改本常量就真的改了普查枚举到什么。
# **不这么做的话本常量是「声明了却没人用」的第二说法**:照注释改它不会改变任何行为,
# 门仍按旧集合普查,而维护者会以为两侧已同步。CSS 那一处只能是字面量(CSS 消费不了
# Python 常量),那一侧的同步靠注释承诺承担。
#
# 本常量定义在两份脚本之前(而不是与其它第 10 项常量放在一起):两份脚本都要消费它,
# 而脚本是在 import 期构造的。
FOCUSABLE_SELECTOR = "button, input, select, textarea, a[href], summary, [tabindex]"


def _focusable_census_js(js):
    """把普查脚本里的 `__FOCUSABLE_SELECTOR__` 占位符填成 `FOCUSABLE_SELECTOR`。

    用 `json.dumps` 而不是裸引号拼接:选择器里将来若出现引号(如
    `input[type='text']`),它会转义成合法 JS 字面量,而不是把脚本拼成语法错误 ——
    那种错误在 `page.evaluate` 侧表现为返回 `null`,会被读成「普查无返回」而不是
    「脚本拼坏了」,诊断方向就错了。
    """
    return js.replace("__FOCUSABLE_SELECTOR__", json.dumps(FOCUSABLE_SELECTOR))


# L-5 / L-6 的普查。**按元素枚举,不按容器名** —— 按点名枚举会漏掉没被点名的那个
# (Phase 5 的 G-idi-05-1 与本阶段 A11Y-07 是同构教训)。
# clearance = 可聚焦元素 rect 到其**最近裁剪祖先**的 padding 边的距离,取四边最小值。
# `visible` 一栏是承重的:被祖先藏住的元素 rect 全零,不得把它读成「命中区不足 24×24」。
_IDI06_CENSUS_JS = _focusable_census_js(r"""() => {
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
    __FOCUSABLE_SELECTOR__
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
                    // elH / padBoxH 供 L-5 的**声明集**判据用(见 L5_CONTENT_REGION_MIN_RATIO):
                    // 高度占容器 padding 盒一半以上的可聚焦元素是「内容区」而非控件。
                    elH: r.height, padBoxH: padBottom - padTop,
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
}""")


# ---- UAT 第 10 项(A11Y-01 / D-05 / D-16 / D-17)的常量 ----------------------
# 焦点规则的枚举集 `FOCUSABLE_SELECTOR` **不在这里**,在 `_IDI06_CENSUS_JS` 之上:
# 它同时被 item 9 的普查(`_IDI06_CENSUS_JS`)与第 10 项的普查
# (`_IDI07_FOCUS_CENSUS_JS`)消费,故必须定义在那两份脚本之前 —— 那是「本文件这一侧
# 只有这一处」的前提。
# 环的几何。外伸量 = 2px + 2px = 4px,正是 `CLEARANCE_MIN_PX = 4.0` ——
# 改几何即改那个门的阈值,两者不是两件事。
FOCUS_RING_WIDTH_PX = 2.0
FOCUS_RING_OFFSET_PX = 2.0
# 浏览器把 2px 序列化成 "2px";判据比的是这个字符串,不是浮点数。
FOCUS_RING_WIDTH_CSS = "2px"
# 单次 Tab 驱动的上限。Tab 序列里 `document.body` 也是一站(焦点走到最后一个可聚焦
# 元素后落回 BODY),故上限要留余量;12 远大于「一轮 Tab 序列里落到第一个控件」所需。
_IDI07_TAB_LIMIT = 12

# ---- SC5 / SC5′(INTERACT-01 / D-08 / D-09)的常量 ---------------------------
# 叠层的「整面铺满」分量。`box-shadow: inset 0 0 0 999px <c>` 里的 999px 大于任何按钮的
# 盒宽,故等价于整面覆盖;浏览器把它序列化成 `<c> 0px 0px 0px 999px inset` —— 判据因此取
# 「含 inset 分量 + 含这个铺满分量 + 含该令牌解析出的颜色」的**合取**,而不是逐字比对整串:
# 逐字比对会把 CSSOM 的序列化格式当成契约的一部分(那条契约是 CSS 的,不是 CSSOM 的)。
_IDI07_OVERLAY_SPREAD = "999px"
# 禁用态的 opacity。`.verdict-buttons button:disabled` 用的是 0.5(不是 0.55)—— 它只设
# opacity / cursor、**不钉 background**,这正是 D-07 要修的缺陷现场。
_IDI07_DISABLED_OPACITY = "0.5"
# SC5-朴素按下 与 SC5′ 共用的那张探针裁决卡的 id(打在 `renderVerdictCard()` 的产物上,
# 使后续选择器唯一命中它,而不是命中样本里可能已存在的其它裁决卡)。
_IDI07_VERDICT_PROBE_ID = "idi07-verdict-probe"

# ---- D-15 中段:契约计数的**静态**守卫(INTERACT-02 / D-11…D-14)的常量 ----------
# `:focus-visible` 的出现次数下限。判据是 `>=` 而**不是** `==`:七选择器枚举天然大于 1,
# 且日后按枚举纪律新增一类可聚焦元素会让它继续变大 —— 硬编码一个相等值会把「按纪律扩展」
# 误判成回归。ROADMAP Phase 7 的 gate 原文就是「`:focus-visible` 计数 > 0」。
EXPECTED_FOCUS_VISIBLE_MIN = 1
# 围栏标记(与 check-01 / check-02 逐字同一对)。用它把 style.css 切成围栏内 / 围栏外
# 两段,供「令牌在围栏内声明、在围栏外被消费」这条硬规则 5 的机械形态使用。
FENCE_START_MARKER = "===== DESIGN TOKENS: START"
FENCE_END_MARKER = "===== DESIGN TOKENS: END"
# 硬规则 5「与消费者同提交」的机械形态:每个令牌在围栏内**声明恰好一次**,且在围栏外
# **被消费至少一次**。声明侧抓「改名残留 / 声明了两次」,消费侧抓「死令牌」(声明了却
# 没人用)。前一个抓的是假绿,后一个抓的是假绿的反面 —— 两条都要有。
_IDI07_DECLARED_AND_CONSUMED = (
    "--color-focus",
    "--color-surface-active",
    "--color-border-hover",
    "--color-overlay-hover",
    "--color-overlay-active",
)
# D-13 的运行时探针目标:button / input / select 各一个真实实例 + `.event-list`。
# `.event-list` 是 `#ai-events`(frontend/index.html:76)的类,静态存在于每个样本;
# 枚举含它是**刻意**的 —— 否则减弱动效用户仍会看到流式状态的 0.3s 背景淡入。
_IDI07_MOTION_TARGETS = (
    ("#btn-process-round", "button"),
    ("#message-input", "input"),
    ("#ai-route-select", "select"),
    (".event-list", ".event-list"),
)
# D-12 的时长与 D-11 保留的既有例外。Chrome 把 120ms 序列化成 "0.12s",把两个属性的
# 时长序列化成 "0.12s, 0.12s" —— 故判据先把该串拆成列表再逐项比,**不用子串包含**
# (子串包含会让 "0.12s, 0.12s" 在「必须全为 0s」的断言里假绿:"0s" 是它的子串)。
_IDI07_TRANSITION_DURATION = "0.12s"
_IDI07_EVENT_LIST_DURATION = "0.3s"
_IDI07_REDUCED_DURATION = "0s"

# 交互态探针的共用前提检查(D-17 / T-idi-07-10)。**读值前必须先断言目标存在、可见、未被
# 禁用**,否则 `getComputedStyle` 对不存在的元素返回 null、对不可见元素照样返回解析值,
# 断言会退化成**空转 PASS** —— 这正是本文件 docstring 点名的同型陷阱(第 7 项
# `all(w != "700")` 对 None 恒真)。
#
# ⚠ **「可见」不等于「可交互」。** 一个渲染出来的**禁用**按钮照样有非零 rect,却永远不会
# 匹配 `:not(:disabled)` 的选择器 —— 拿它去断言「hover 有反馈」会 **FAIL 而非 BLOCKED**。
# 故本检查把 `disabled` 一并返回,由调用方按自己的断言对象决定要不要它。
_IDI07_INTERACTIVE_JS = r"""([sel]) => {
  const el = document.querySelector(sel);
  if (!el) return {ok: false, why: 'not found'};
  const r = el.getBoundingClientRect();
  if (!(r.width > 0 && r.height > 0)) {
    return {ok: false, why: 'rect is zero (hidden or not laid out)'};
  }
  return {ok: true, disabled: !!el.disabled, tag: el.tagName.toLowerCase(),
          rect: [Math.round(r.width), Math.round(r.height)]};
}"""

# SC5-朴素按下 与 SC5′ 共用**同一张**裁决卡:由应用自身的 `renderVerdictCard()` 造出
# (不手工拼 DOM —— 那是伪造被测状态;照 item9 用 renderEvent / renderAnnotations 的先例),
# 挂到 `#verdict-cards` 下并打上探针 id。
_IDI07_BUILD_VERDICT_CARD_JS = r"""() => {
  const host = document.querySelector('#verdict-cards');
  if (!host || typeof renderVerdictCard !== 'function') return null;
  const card = renderVerdictCard(
    {number: 9001, location: '(SC5 探针)', issue: 'SC5 交互态探针',
     suggestion: '(无)'}, 'p2');
  card.id = '__PROBE_ID__';
  host.appendChild(card);
  return {buttons: card.querySelectorAll('.verdict-buttons button').length,
          notes: card.querySelectorAll('.verdict-note-input').length};
}""".replace("__PROBE_ID__", _IDI07_VERDICT_PROBE_ID)

# SC5′ 的 `.disabled` 切换。这是 app.js 在 `submit` 里做的**真实**状态切换
# (frontend/app.js:718-719),不是伪造 DOM。
_IDI07_DISABLE_VERDICT_BUTTONS_JS = r"""([sel]) => {
  const card = document.querySelector(sel);
  if (!card) return null;
  const btns = [...card.querySelectorAll('.verdict-buttons button')];
  btns.forEach((b) => { b.disabled = true; });
  return btns.map((b) => b.disabled);
}"""

# 第 10 项的普查:按 **DOM 遍历**枚举 `FOCUSABLE_SELECTOR` 的**全部实例**,对每个实例
# 返回清单项 `{tag, id, cls, label, visible, focusable}` —— **只出清单,不出环读数**。
#
# 清单项里**不得放 DOM 节点本身**:`page.evaluate` 跨边界序列化时节点会塌成字面串
# `ref: <Node>`(实测),放进去既读不出信息、又与本项「只出清单,不出第二种说法」的
# 纪律相悖。采样表的键由 `tag` / `id` / `cls` 拼出(`labelOf`),照 `_IDI06_CENSUS_JS`
# 里 `labelOf` 的形态 —— 两个脚本必须用**同一个** labelOf,否则采样表与判定集对不上。
#
# `visible` 取 `el.getClientRects().length > 0`:被祖先藏住的元素 rect 全零,不得把它
# 读成「未覆盖」。
#
# `focusable` 取 `!el.matches(':disabled') && el.getAttribute('tabindex') !== '-1'`。
# 用 `:disabled` 而不是 `[disabled]`:前者覆盖「实际被禁用」的全部形态(含被外层
# `<fieldset disabled>` 包裹的控件),后者只认写在元素自己身上的那个属性。
#
# **排除面是有意的,不是漏项。** 禁用控件与 `tabindex="-1"` 的元素 **rect 非零、确实
# 渲染在树里,却不在顺序焦点序里** —— 拿它们去要求「被环覆盖」会造出一条**永远无法
# 满足**的判据(禁用控件被浏览器移出顺序焦点序,永远不会成为 `document.activeElement`)。
# 本仓库真实存在的实例(逐个点名 + 可复跑取证):
#   - `frontend/index.html:126` 的 `#btn-approve-draft[disabled]`:p1 样本里 `#draft-view`
#     被 `frontend/app.js` 取消隐藏,而该样本无 `docs/draft.md` ⇒ `app.js` 让它保持禁用;
#   - `frontend/index.html:143` 的 `#btn-authorize[disabled]`:p3 样本里 `#authorize-row`
#     被 `app.js` 取消隐藏;`_IDI06_CENSUS_JS` 的注释已实测记录它 clearance `-122.6px`,
#     即确实渲染在树里。它的点亮与否由 `app.js` 消费的 `g3_available` 决定 —— 若某样本里
#     它被点亮,`focusable` 自动为真、它自动回到判定集并被 Tab 覆盖,登记面无需改动;
#   - 计划 02 在 `checking` 样本里新增的两个 `.verdict-buttons button:disabled`。
# 结论:它们**有意**落在判定集之外 —— 禁用控件不参与顺序焦点序,不得用环去覆盖它们。
# 本判据是 **Reachable**,不是 Exists。
#
# 已登记的两条边界(照 `_IDI06_CENSUS_JS` 里 `intersects` 那条「登记而非静默」的先例):
#   ① Tab 序不覆盖被祖先藏住的元素 —— 那正是 `visible` 过滤存在的理由;
#   ② Tab 序也不覆盖不可聚焦的实例 —— 那正是 `focusable` 过滤存在的理由。
# 两条过滤之后剩下的集合必须逐个被 Tab 覆盖。
_IDI07_FOCUS_CENSUS_JS = _focusable_census_js(r"""() => {
  const labelOf = (el) => {
    if (el.id) return '#' + el.id;
    const cls = (typeof el.className === 'string' && el.className.trim())
      ? '.' + el.className.trim().split(/\s+/).join('.') : '';
    return el.tagName.toLowerCase() + cls;
  };
  const out = [];
  document.querySelectorAll(
    __FOCUSABLE_SELECTOR__
  ).forEach((el) => {
    out.push({
      tag: el.tagName.toLowerCase(),
      id: el.id,
      cls: (typeof el.className === 'string') ? el.className.trim() : '',
      label: labelOf(el),
      visible: el.getClientRects().length > 0,
      // 禁用控件与 tabindex="-1" 渲染在树里却不在顺序焦点序里 —— 见上方注释。
      focusable: !el.matches(':disabled') && el.getAttribute('tabindex') !== '-1',
    });
  });
  return out;
}""")

# 第 10 项的环读数**唯一来源**:读**当前焦点元素的那一瞬读数**。
# 它返回 `{label, tag, outlineWidth, outlineColor, outlineOffset, focusVisible}`;
# `document.activeElement` 不是 `HTMLElement` 时返回 `null`。它与上面的清单常量**分开
# 命名**:清单只出「有哪些元素」,环读数只出「此刻焦点元素读到什么」,两者不互相携带
# 第二种说法。labelOf 与上面那份逐字相同。
#
# `outlineOffset` 与 `outlineWidth` 是**同一件事的两半**:环的外伸量 = 两者之和,而
# `CLEARANCE_MIN_PX` 编码的正是这个和。两半都在这里读,故 SC1 能同时断言它们 —— 只读
# 宽度时,把 `outline-offset` 从 2px 改成 0 不会让任何一条断言变红(外伸量真值从 4px
# 变成 2px,而门仍按 4px 判),「几何双向绑定」那条注释就没有机械守卫。
_IDI07_TAB_READ_JS = r"""() => {
  const el = document.activeElement;
  if (!(el instanceof HTMLElement)) return null;
  const labelOf = (e) => {
    if (e.id) return '#' + e.id;
    const cls = (typeof e.className === 'string' && e.className.trim())
      ? '.' + e.className.trim().split(/\s+/).join('.') : '';
    return e.tagName.toLowerCase() + cls;
  };
  const s = getComputedStyle(el);
  return {
    label: labelOf(el),
    tag: el.tagName.toLowerCase(),
    outlineWidth: s.outlineWidth,
    outlineColor: s.outlineColor,
    outlineOffset: s.outlineOffset,
    focusVisible: el.matches(':focus-visible'),
  };
}"""

# SC4 的 clearance 读数:对**当前焦点元素**套用 item 9 的 L-5 口径 —— 到最近裁剪祖先
# padding 边的最小距离,取四边最小值。算法与 `_IDI06_CENSUS_JS` 逐字相同,只是取样对象
# 换成 `document.activeElement`(item 9 是按选择器全量枚举,结构上读不到「此刻焦点在哪」)。
# 没有裁剪祖先时 `clearance` 为 `null`(无定义,不是 0)。
_IDI07_TAB_CLEARANCE_JS = r"""() => {
  const px = (v) => parseFloat(v) || 0;
  const labelOf = (el) => {
    if (el.id) return '#' + el.id;
    const cls = (typeof el.className === 'string' && el.className.trim())
      ? '.' + el.className.trim().split(/\s+/).join('.') : '';
    return el.tagName.toLowerCase() + cls;
  };
  const isClipping = (el) => {
    const s = getComputedStyle(el);
    return s.overflowX !== 'visible' || s.overflowY !== 'visible';
  };
  const el = document.activeElement;
  if (!(el instanceof HTMLElement)) return null;
  const r = el.getBoundingClientRect();
  const visible = r.width > 0 && r.height > 0;
  let anc = el.parentElement;
  let nearest = null;
  while (anc) {
    if (isClipping(anc)) { nearest = anc; break; }
    anc = anc.parentElement;
  }
  if (!nearest) {
    return {label: labelOf(el), container: null, clearance: null, visible: visible};
  }
  const ar = nearest.getBoundingClientRect();
  const s = getComputedStyle(nearest);
  const padLeft = ar.left + px(s.borderLeftWidth);
  const padTop = ar.top + px(s.borderTopWidth);
  const padRight = ar.right - px(s.borderRightWidth);
  const padBottom = ar.bottom - px(s.borderBottomWidth);
  const gap = Math.min(r.left - padLeft, padRight - r.right,
                       r.top - padTop, padBottom - r.bottom);
  return {label: labelOf(el), container: labelOf(nearest), clearance: gap,
          visible: visible};
}"""

# SC4 的前提:让**裁剪容器真的可滚**,否则「滚到底」是 no-op、本断言退化成普通
# clearance 检查(WR-01)。p1 下三个容器实测都是 `scrollHeight == clientHeight`:
# `#main-pane` 900/900、`#chat-messages` 8/8(空态,`:has(:empty)` 把它钉成
# `flex: 0 0 auto`)、`#doc-panel` 900/900 —— 于是「侧栏滚到底再 Tab」里的「滚到底」
# 从未发生,而这条断言恰恰是为此命名的。
#
# 撑高走**应用自己的渲染路径**,不手搓 DOM(与 item8 撑 `#doc-panel` 同一形态):
#   · `#doc-panel`:`renderMarkdown()` 渲染进 `#draft-content` —— 逐字照 item8 的做法;
#   · `#main-pane`:应用自己的 `renderEvent()`(它内部对 `kind: 'say'` 走
#     `renderMarkdown()`)。`.event-list` 的限高与内滚动在 item 9 被刻意删除,故
#     `#ai-events` 会随条目长高、把外层 `#main-pane` 顶到可滚 —— 这正是 item 9 的
#     设计意图(「条目随外层 #main-pane 滚动」),本探针只是把它撑到能观测。
# 两处都**只加不删**:不写死页面的既有内容,`#draft-content` 的清空是 item8 已确立的
# 做法(该区域是 markdown 渲染区,内容由应用覆盖式写入)。
#
# `kind` 必须取 `'say'`:`renderEvent` 对 `done` / `error` 会解除「发起」按钮的禁用,
# 那是**状态变更**,会污染本项后续探针(SC5 / hover / SC2)。
#
# 实测(1440×900,p1):`renderEvent` × 40 让 `#main-pane` 900/900 → 2640/900,
# `#doc-panel` 经上面那条 → 5248/900;两者的可聚焦元素普查计数(28)**不变** ——
# 撑高只加非可聚焦的正文节点,不改判定集、不改 Tab 序。
#
# ⚠ 正文**不得含链接**:`renderMarkdown` 会把 `[x](y)` 渲染成 `a[href]`,那是**新增
# 可聚焦元素**,会改判定集与 Tab 序 —— 撑高必须对这两者零影响。
_IDI07_SC4_GROW_MD = "\n\n".join(
    f"第 {i} 段探针正文:用于把容器撑到可滚,使「滚到底后环不被裁切」不是空转断言。"
    for i in range(1, 81)
)
# 每条事件的正文。**逐条编号**,重复文本会被 markdown 渲染成同一段,长高幅度不可控。
_IDI07_SC4_EVENT_MD = "事件条目 {i}:用于把 #ai-events 撑高,进而把外层 #main-pane 顶到可滚。"
_IDI07_SC4_EVENT_COUNT = 40
_IDI07_SC4_GROW_JS = """([md, eventMd, count]) => {
  const out = {};
  const events = document.querySelector('#ai-events');
  if (events && typeof renderEvent === 'function') {
    for (let i = 1; i <= count; i++) {
      renderEvent({kind: 'say', content: eventMd.replace('{i}', String(i))});
    }
    out['#ai-events'] = events.childElementCount;
  }
  const doc = document.querySelector('#draft-content');
  if (doc && typeof renderMarkdown === 'function') {
    doc.innerHTML = '';
    doc.appendChild(renderMarkdown(md));
    out['#draft-content'] = doc.childElementCount;
  }
  return out;
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
                # 768 处保持只读诊断:它在 LAYOUT-02 里的承诺是「无内容遮挡」,
                # 而**该承诺未被覆盖** —— 本项前面的 badge × banner 断言(:1834)只测 #state-badge
                # 那一对;768px 下真正发生遮挡的那一对(banner × #doc-panel-header 的 h1)
                # 不在覆盖范围内,这里是显式「未覆盖」。
                # 实测证伪:h1 = 439.0–481.0 × 8–28,banner = 285.3–482.7 × 12–39,
                # 重叠 42×16px,相交带 768–855px。这是**已知缺口**,不是 PASS;
                # 收窄已登记在 idi-06-UI-SPEC.md §L-2(A-10 行)。
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
                         "该承诺未被覆盖:badge × banner 断言只测 badge 那一对,"
                         "banner × #doc-panel-header 的 h1 不在覆盖范围内 —— 显式「未覆盖」。"
                         "实测:h1 = 439.0–481.0 × 8–28 vs banner = 285.3–482.7 × 12–39,"
                         "重叠 42×16px,相交带 768–855px。这是已知缺口(既未满足、也未断言),"
                         "收窄已登记在 idi-06-UI-SPEC.md §L-2(A-10 行))")
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
# L-5 的**声明集**(用户裁定,2026-09-24;取代 08-UI-SPEC D-21 的「check-05 零改动」)。
# 为什么需要:Phase 8 给 `#round-doc` 加了 `tabindex="0"`,于是它经 `FOCUSABLE_SELECTOR`
# 的 `[tabindex]` 一臂**首次**进入 L-5 的判定集 —— 而它是**内容区**(当前轮文档的渲染容器),
# 不是控件。实测(p3 样本,1440×900):元素高 778.64px、容器 padding 盒 900px、元素在盒内
# 顶部偏移 188px ⇒ 默认滚动位(scrollTop 0)下其下边缘越界 66.64px;浏览器把元素滚入视野后
# (scrollTop 67)下边缘恰好贴边(clearance 0.36px)。**L-5 的 4px 因此恒差约 4px**。
# 三条承重理由:①L-5 的规定修法(抬该容器的 padding)对这类元素**只会更糟** —— padding 落在
# 元素上方,把它推得更低;②元素高度**由文档内容决定、无上界**,故任何布局改动都无法稳健满足;
# ③本阶段 D-02 已就**同一几何**裁定过「环可辨」(5.57:1,底边被裁 3.64px,正是上面那个 0.36px)。
# 判据是**客观比例**而不是元素名清单:高度 >= 容器 padding 盒一半的可聚焦元素 = 内容区。
# 命中者逐行 `info()` 报出,**不从视野里消失** —— 声明不是静默跳过。
L5_CONTENT_REGION_MIN_RATIO = 0.5
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

    **判定集再分两半**(用户裁定,2026-09-24):高度 >= 容器 padding 盒一半的可聚焦元素是
    **内容区**(见 `L5_CONTENT_REGION_MIN_RATIO` 的注释),对它**声明**而不断言 —— 逐行
    `info()` 报出,断言只落在其余(控件)行上。声明集与断言集都为空时走 `blocked(...)`,
    防止「判定集被声明集吃光」退化成一条空转 PASS。
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
    # 内容区(声明集):高度占容器 padding 盒一半以上。缺 elH / padBoxH 的行不误伤 —— 判据
    # 取不到就当控件处理(进断言集),宁可多判也不静默放行。
    def _is_content_region(r):
        elh, padbox = r.get("elH"), r.get("padBoxH")
        if not elh or not padbox:
            return False
        return elh >= padbox * L5_CONTENT_REGION_MIN_RATIO

    declared = [r for r in judged if _is_content_region(r)]
    asserted = [r for r in judged if not _is_content_region(r)]
    if declared:
        info(f"item9 [{state}] L-5 声明集(内容区,不断言)",
             f"{[(r['el'], r['container'], round(r['elH'], 1), round(r['padBoxH'], 1),
                  round(r['clearance'], 1)) for r in declared]}"
             f" —— 高度 >= 容器 padding 盒的 {L5_CONTENT_REGION_MIN_RATIO:.0%} 即可聚焦内容区:"
             "环在浏览器滚入视野后必然贴边(见 L5_CONTENT_REGION_MIN_RATIO 的注释)")
    if not asserted:
        blocked(item,
                f"[{state}] L-5 每个裁剪容器 × 可聚焦后代的 clearance >= {CLEARANCE_MIN_PX:.0f}px",
                f">= {CLEARANCE_MIN_PX:.0f}px(控件行)",
                f"断言集为空:共 {len(judged)} 行判定行全部落进声明集(内容区)",
                "判定集被声明集吃光 ⇒ 本样本对控件无判定,不记 PASS。走到这里说明声明集的"
                "比例判据过宽(把控件也当成内容区了),不是「样本恰好只有内容区」")
        return
    bad = [r for r in asserted if r["clearance"] < CLEARANCE_MIN_PX]
    ok_true(item,
            f"[{state}] L-5 每个裁剪容器 × 可聚焦后代的 clearance >= {CLEARANCE_MIN_PX:.0f}px",
            not bad, f"全部 >= {CLEARANCE_MIN_PX:.0f}px",
            f"共 {len(asserted)} 行(另有 {len(declared)} 行内容区声明),未达标 "
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
# UAT 第 10 项 — A11Y-01 焦点环(令牌 → 规则 → 算术门 → 浏览器里读到的环)
# ---------------------------------------------------------------------------
def _idi07_blur_reset(page):
    """清空焦点复位:blur 把焦点交还 `document.body`,Tab 序列随即从头开始。

    **这不是「聚焦某个元素」** —— 本文件对程序化聚焦调用的计数仍为 0(第 10 项的验收
    判据)。不得改用显式聚焦调用:那在 Chrome 下不保证匹配 `:focus-visible`,用它替代
    Tab 会让「键盘 Tab 到控件出环」这条断言失去意义。
    """
    page.evaluate(
        "() => { const el = document.activeElement;"
        " if (el instanceof HTMLElement) el.blur(); }"
    )


def _idi07_tab_drive(page, limit):
    """Tab 驱动焦点,逐次读当前 `document.activeElement` 的环读数。

    返回 `(order, samples)`:`order` 是每次 Tab 后的**全部原始载荷**(含落回 `body` 的
    那些),`samples` 是「稳定标签 -> 最后一次采样到的读数」。

    **环读数只在「该元素成为 `document.activeElement` 的那一刻」采**,唯一来源是
    `_IDI07_TAB_READ_JS`。本项**不存在**「未聚焦时的 outline 读数」这个概念:未聚焦
    元素在 `:focus-visible` 下计算 `outline-width` 为 `0px`、`outline-color` 回落到 UA
    值,拿静态读数去判定会把**每一个**元素都判成 bad。
    """
    _idi07_blur_reset(page)
    order, samples = [], {}
    for _ in range(limit):
        page.keyboard.press("Tab")
        payload = page.evaluate(_IDI07_TAB_READ_JS)
        order.append(payload)
        if payload:
            samples[payload["label"]] = payload
    return order, samples


def _idi07_focus_census_assert(page, item, state, focus_color):
    """D-16 的焦点环元素普查断言:判定集非空,且其中「未被环覆盖的元素数」为 0。

    **判定集** = `_IDI07_FOCUS_CENSUS_JS` 返回的实例中同时满足 `visible` 与 `focusable`
    的那些(两个字段都由普查逐元素返回),即 Tab 可达的可聚焦元素。**`bad`** = 判定集里
    「在其成为 `document.activeElement` 的时刻**从未读到过环**」的元素 —— 即采样表里没有
    它的条目,或它采样到的读数不等于 `("2px", focus_color)`。

    五条形态纪律(照 `_idi06_clearance_assert`):
      1. `data is None` ⇒ `blocked(...)`,**绝不记 PASS**;
      2. 先 `info()` 落**全部原始行**(每个元素的 tag/id/class + visible + focusable +
         采样到的环读数,没采样到就写 None),再判定;
      3. **判定集为空集 ⇒ `blocked(...)`,不是 `info()` + `return`** —— 这是对 item9
         第 3 条的**有意收紧**。item9 的样本可能真的没有「落在可视滚动区内」的组合,而
         本项三个样本各自都有**必然存在**的「可见 ∧ 可聚焦(即 Tab 可达)」实例
         (p1:`#message-input` / `#btn-send` / `#ai-route-select` / `#project-path-input`;
         checking:`#check-switcher` / `#btn-continue-check` / `#ai-route-select` /
         `#project-path-input`;p3:`summary` / `#round-switcher` / `#ai-route-select` /
         `#btn-enter`),已由执行前基线的 `check-05 --item 9` 普查 INFO 行逐样本实测为
         `visible=True`。故**空集只可能是过滤式写错或样本没到位**,不是「样本恰好没有
         可聚焦元素」。⚠ 判据的锚必须是「可见 ∧ 可聚焦」这个**合取**,不是「可见」单独
         一项:`#btn-process-round` 在 p1 的标记里带 `disabled`(`frontend/index.html:73`),
         `visible=True` 却被 `focusable` 排除在判定集之外,拿 item9 的可见性表当
         「可聚焦」的证据正是同型混淆。空集若退化成 `info()` + `return`,整条普查会以
         「0 条断言」静默通过 —— 这正是「假 PASS」的形态(`item_verdict` 只读行级裁决,
         没有任何机制把「一行都没断言」读成非 PASS)。`len(judged) > 0` 必须是**真实
         守卫**,不是散文承诺;
      4. 判据是 `not bad` —— 即「判定集里未被环覆盖的元素数 == 0」;
      5. 失败行的 note 给出**可执行的修复动作**。
    """
    data = page.evaluate(_IDI07_FOCUS_CENSUS_JS)
    if data is None:
        blocked(item,
                f"[{state}] 焦点环覆盖全部 Tab 可达的可聚焦元素(判定集非空且未覆盖数为 0)",
                "普查脚本返回数据", "<MISSING>", "普查无返回 ⇒ 不记 PASS")
        return
    order, samples = _idi07_tab_drive(page, len(data) + 8)
    judged = [r for r in data if r["visible"] and r["focusable"]]
    info(f"item10 [{state}] 焦点环普查(全部原始行:标签 / visible / focusable / "
         f"采样到的 outline-width / outline-color)",
         f"{len(data)} 个元素:"
         f"{[(r['label'], r['visible'], r['focusable'],
             (samples.get(r['label']) or {}).get('outlineWidth'),
             (samples.get(r['label']) or {}).get('outlineColor')) for r in data]}")
    info(f"item10 [{state}] Tab 序列(全部原始载荷)", f"{order}")
    if not judged:
        blocked(item,
                f"[{state}] 焦点环覆盖全部 Tab 可达的可聚焦元素(判定集非空且未覆盖数为 0)",
                "判定集(可见 ∧ 可聚焦)非空", f"共 {len(data)} 个实例,判定集为空",
                "本项三个样本各自都有必然存在的可见 ∧ 可聚焦实例 ⇒ 空集只可能是过滤式"
                "写错或样本没到位。空集不得退化成 info() + return —— item_verdict 只读"
                "行级裁决,空转会以 PASS 现身,那正是假 PASS 的形态")
        return
    bad = [
        r for r in judged
        if r["label"] not in samples
        or (
            samples[r["label"]]["outlineWidth"],
            norm(samples[r["label"]]["outlineColor"]),
        ) != (FOCUS_RING_WIDTH_CSS, norm(focus_color))
    ]
    ok_true(item,
            f"[{state}] 焦点环覆盖全部 Tab 可达的可聚焦元素(判定集非空且未覆盖数为 0)",
            not bad, "未覆盖数 == 0",
            f"判定集 {len(judged)} 个元素,未覆盖 "
            f"{[(r['label'], r['tag'], r['id'], r['cls']) for r in bad]}",
            "未覆盖者若确实是可聚焦元素 ⇒ 它不在 :focus-visible 的七选择器枚举里,"
            "到 frontend/style.css 文件末尾补它的选择器,并同步本文件的 "
            "FOCUSABLE_SELECTOR;若它其实是**不可聚焦**的(说明 focusable 漏了一类,"
            "例如被 <fieldset disabled> 包裹的控件),则改 focusable 的判定式,"
            "**不要**改 CSS")


def _idi07_sc1_assert(page, item, state, focus_color):
    """SC1(D-17):键盘 Tab 到控件后环可见 —— 读**当前焦点元素**的计算 outline。

    载荷本身就是 `_IDI07_TAB_READ_JS` 返回的「当前 `document.activeElement` 的那一瞬
    读数」,取其中的 `outlineWidth` / `outlineColor` / `outlineOffset`。**不得写成
    `read_style(page, sel, prop)`**:那个 helper 走 `document.querySelector(sel)`、按
    选择器取值,结构上读不到「当前焦点元素」,本项的焦点读数只走 `_IDI07_TAB_READ_JS`。
    宽度与偏移量在这里**成对**断言:两者之和才是环的外伸量,而 `CLEARANCE_MIN_PX`
    编码的就是那个和(见 `_IDI07_TAB_READ_JS` 上的注释)。

    为什么 Tab 若干次而不是恰好一次:`document.body` 是 Tab 循环里的一站(实测:焦点走到
    最后一个可聚焦元素后,下一次 Tab 落回 BODY,那里 `:focus-visible` 为假、`outline-width`
    是 UA 的 3px)。BODY 不是「控件」,故循环到第一个落在控件上的载荷为止;全部原始载荷
    都经 `info()` 落盘,不隐藏任何一跳。载荷为 `null`(焦点不在元素上)或始终没落到控件上
    ⇒ `blocked`。
    """
    _idi07_blur_reset(page)
    order, hit = [], None
    for _ in range(_IDI07_TAB_LIMIT):
        page.keyboard.press("Tab")
        payload = page.evaluate(_IDI07_TAB_READ_JS)
        order.append(payload)
        if payload and payload["tag"] not in ("body", "html"):
            hit = payload
            break
    info(f"item10 [{state}] SC1 Tab 序列(全部原始载荷)", f"{order}")
    if hit is None:
        blocked(item, f"[{state}] SC1 键盘 Tab 到控件后环可见",
                f'outline-width == "{FOCUS_RING_WIDTH_CSS}" 且 '
                "outline-color == var(--color-focus)",
                f"{order}",
                "Tab 未落到任何控件上(或焦点不在元素上)⇒ 读不到环,不记 PASS")
        return
    ok(item,
       f"[{state}] SC1 Tab 到 {hit['label']} 的 outline-width == {FOCUS_RING_WIDTH_CSS}",
       FOCUS_RING_WIDTH_CSS, hit["outlineWidth"],
       f"焦点伪类匹配={hit['focusVisible']};几何 {FOCUS_RING_WIDTH_PX:.0f}px + "
       f"outline-offset {FOCUS_RING_OFFSET_PX:.0f}px 的外伸量 = CLEARANCE_MIN_PX "
       f"= {CLEARANCE_MIN_PX:.0f}px")
    # 外伸量的**另一半**。只断言宽度时,把 `outline-offset` 从 2px 改成 0 不会让本项
    # 任何一条断言变红:宽度读数不变,SC4 实测的 clearance 是 40 / 130,2px 的真值变化
    # 挪不动它 —— 于是环的真实外伸量变成 2px,而 CLEARANCE_MIN_PX 仍编码 4px,
    # 「几何是双向绑定的」那条注释就没有机械守卫(它的反向变异「加宽环」由上面那条抓)。
    # 期望侧由 FOCUS_RING_OFFSET_PX 算出(与宽度同源),不硬编码 "2px"。
    ok(item,
       f"[{state}] SC1 Tab 到 {hit['label']} 的 outline-offset == "
       f"{FOCUS_RING_OFFSET_PX:.0f}px(= CLEARANCE_MIN_PX - 环宽)",
       f"{FOCUS_RING_OFFSET_PX:.0f}px", hit["outlineOffset"],
       "外伸量 = 上面那条的宽度 + 这一条,合起来才是 CLEARANCE_MIN_PX;"
       "改几何即改那个门的阈值 —— 两者不是两件事")
    ok(item,
       f"[{state}] SC1 Tab 到 {hit['label']} 的 outline-color == var(--color-focus)",
       focus_color, hit["outlineColor"],
       "期望侧来自运行时解析的令牌,不硬编码 rgb")


def _idi07_sc2_assert(page, item, state, focus_color):
    """SC2(D-17,样本固定 p1):鼠标点击控件后**不**出现焦点环。

    四步,缺一步这条断言就会空转:
      1. **先断言目标元素存在、可见、且未被禁用**(`getBoundingClientRect()` 非全零
         **且** `!el.disabled`);
      2. `page.keyboard.press("Tab")` 让环先出现 —— 证明 `:focus-visible` 规则此刻是活的;
      3. `page.click(sel)`,**并断言点击后 `document.activeElement` 就是这个元素** ——
         少了它,「读到的 `outline-color` 不等于 `--color-focus`」在「环规则压根不存在」
         时同样成立,而这一步把读数锁在「鼠标确实把焦点给了它」的那一瞬;
      4. 读它的 `outline-color`,断言**不等于** `resolve_color(page, "--color-focus")`。
         这直接证明「鼠标点击不出现环」,比断言 UA 基线字符串稳。`outline-style` /
         `outline-width` 作为 `info()` 诊断落盘,不参与判定。

    目标取 `#btn-send`(`frontend/index.html:23`,在 `#chat-input-row` 内、由
    `#chat-input-row button` 以 1-0-1 填充):它在 p1 里**可见、可聚焦、未禁用** ——
    `applySessionGates()` 显式 `sendBtn.disabled = false`,全局唯一把它置真的是
    `applyArchiveView()`(`mission_complete` 归档路径,p1 不走);且 p1 的 `#message-input`
    为空,`sendBtn` 的 click 处理器在 `if (!text) return;` 处**整体空转**,不产生 DOM
    变更、不改状态。

    **不得用 `#btn-process-round`**:它在标记里带 `disabled`(`frontend/index.html:73`),
    p1 里对它 `page.click()` 会因 Playwright 的 actionability「enabled」检查抛
    `TimeoutError`;而强行 `force=True` 的「弄绿」写法是假 PASS:禁用控件不在顺序焦点序
    里、永远不会成为 `document.activeElement`,`outline-color != --color-focus` 无论 CSS
    怎么写都成立。
    """
    sel = "#btn-send"
    pre = page.evaluate(
        """(sel) => {
            const el = document.querySelector(sel);
            if (!el) return null;
            const r = el.getBoundingClientRect();
            return {w: r.width, h: r.height, disabled: !!el.disabled,
                    visible: el.getClientRects().length > 0};
        }""",
        sel,
    )
    if pre is None or not pre["visible"] or pre["w"] <= 0 or pre["h"] <= 0:
        blocked(item, f"[{state}] SC2 {sel} 存在、可见、未被禁用",
                "rect 非全零且 visible", f"{pre}",
                "目标元素读不到/不可见 ⇒ 本断言失去证明力,不记 PASS")
        return
    if pre["disabled"]:
        blocked(item, f"[{state}] SC2 {sel} 存在、可见、未被禁用",
                "disabled == false", f"{pre}",
                "目标被禁用:禁用控件不在顺序焦点序里,永远不会成为 document.activeElement,"
                "「点击后不出环」无论 CSS 怎么写都成立 ⇒ 假 PASS 的形态,不记 PASS")
        return
    info(f"item10 [{state}] SC2 目标前提",
         f"{sel} rect={pre['w']}x{pre['h']} disabled=False visible=True")

    # 2. 先让环出现,证明 :focus-visible 规则此刻是活的。
    page.keyboard.press("Tab")
    info(f"item10 [{state}] SC2 点击前的环(证明规则此刻是活的)",
         f"{page.evaluate(_IDI07_TAB_READ_JS)}")

    # 3. 点击,并断言焦点真的落到目标上。
    page.click(sel)
    after = page.evaluate(
        """(sel) => {
            const el = document.activeElement;
            if (!(el instanceof HTMLElement)) return null;
            const s = getComputedStyle(el);
            return {
              matchesTarget: el === document.querySelector(sel),
              label: el.id ? '#' + el.id : el.tagName.toLowerCase(),
              outlineStyle: s.outlineStyle,
              outlineWidth: s.outlineWidth,
              outlineColor: s.outlineColor,
              focusVisible: el.matches(':focus-visible'),
            };
        }""",
        sel,
    )
    if after is None or not after["matchesTarget"]:
        blocked(item, f"[{state}] SC2 点击后 document.activeElement 就是 {sel}",
                f"activeElement == {sel}", f"{after}",
                "鼠标没有把焦点交给目标 ⇒ 读数不在「点击」这一瞬,断言空转,不记 PASS")
        return
    info(f"item10 [{state}] SC2 点击后的诊断(outline-style / outline-width,不参与判定)",
         f"style={after['outlineStyle']} width={after['outlineWidth']} "
         f"focusVisible={after['focusVisible']}")
    ok_true(item,
            f"[{state}] SC2 鼠标点击 {sel} 后 outline-color != var(--color-focus)",
            norm(after["outlineColor"]) != norm(focus_color),
            f"!= {focus_color}", after["outlineColor"],
            "点击后焦点伪类不匹配 ⇒ 不出环。这比断言 UA 基线字符串稳")


def _idi07_sc4_assert(page, item, state, focus_color):
    """SC4(D-17):侧栏滚到底再 Tab,环不被裁切 —— 复用 item 9 的 L-5 clearance 口径。

    几何 `2px` + `outline-offset: 2px` 是本探针的**前提**:环的外伸量恰为 4px,故判据取
    `CLEARANCE_MIN_PX`(= 4.0)。**改几何即改本判据** —— 宽度与偏移量两半都由 SC1 在
    运行时断言(`_IDI07_TAB_READ_JS` 的 `outlineWidth` / `outlineOffset`),不是只写在
    注释里。

    **「滚到底」本身也是前提,必须先把它变成真的(WR-01)。** 三个裁剪容器
    (`#main-pane` / `#chat-messages` / `#doc-panel`)在 p1 下默认都不可滚
    (`scrollHeight == clientHeight`),那时 `scrollTop = scrollHeight` 是 no-op,本断言
    就退化成一条普通 clearance 检查 —— 它再也回答不了它被命名来回答的问题(滚到底之后
    环是否被裁),因为「滚到底」这一态从未到达。故本探针**先走应用自己的渲染路径撑高**
    (`renderEvent` / `renderMarkdown`,见 `_IDI07_SC4_GROW_JS`),再回读三元组:

      · 有容器真的可滚 ⇒ 继续判定(正常路径);
      · 撑高之后仍无容器可滚 ⇒ **`blocked(...)`,不是 PASS** —— fail-closed 兜底,与
        item8 对 sticky 表头用的判据同源。该分支在正常路径下不可达,留着是为了让
        「撑高失效」以 BLOCKED 现身,而不是退化成一条绿的空转断言。

    `#doc-panel` 必须在滚动列表里:它是 4 条判定行(`#enter-path-input` ×2、
    `#btn-enter`、`#btn-divergence`)的最近裁剪祖先,不滚它等于「侧栏滚到底」对那几条
    从未发生。

    撑高对**本项其余探针**必须是零影响(它们在同一样本内排在 SC4 之后):正文不含链接
    (链接会成为新的可聚焦元素,改判定集与 Tab 序),事件 `kind` 取 `'say'`(取
    `done` / `error` 会解除「发起」按钮的禁用,是状态变更)。撑高前后 item 10 的断言集
    已逐条比对,差异只在 SC4 那几条。

    判据 = 滚到底之后**每个新 Tab 聚焦到的可见元素**的 clearance >= `CLEARANCE_MIN_PX`。
    判定集为空(滚到底后没有任何新 Tab 聚焦到的可见元素)或元素不可见 ⇒ **`blocked(...)`,
    不是 `info()` 声明「本样本无判定」、更不得记 PASS** —— 理由与上面普查第 3 条同源,在
    这里更硬:`item_verdict` 只看**行级裁决**,一个「其余行全 PASS」的项会返回 `pass`,所以
    一条未判定的探针会**以 `item 10: PASS (N 条断言,0 FAIL,0 BLOCKED)` 的形态现身**,这
    正是本项要消灭的空转 PASS;而 SC4 的判定集比普查更窄(只限「滚到底之后新 Tab 覆盖到」
    的那些元素),它的空集更不可能是「样本恰好没有裁切风险」,只可能是探针写错或样本没到位。
    **确实没有裁剪祖先的元素**:clearance 无定义,写进 `info()` 的原始行记为 `None` 并从
    判定集里剔除(剔除后判定集为空则仍走 `blocked`)。
    """
    # ---- 前提:先让裁剪容器真的可滚 -----------------------------------------
    # p1 下三个容器默认都不可滚(见 `_IDI07_SC4_GROW_JS` 上的实测),「滚到底」会是
    # no-op。走应用自己的渲染路径撑高(`renderEvent` / `renderMarkdown`),再回读三个
    # 容器的三元组。
    grown = page.evaluate(
        _IDI07_SC4_GROW_JS,
        [_IDI07_SC4_GROW_MD, _IDI07_SC4_EVENT_MD, _IDI07_SC4_EVENT_COUNT],
    )
    info(f"item10 [{state}] SC4 撑高裁剪容器(走应用自己的渲染路径)",
         f"{grown}(#ai-events / #draft-content 的子节点数)")

    scrolled = page.evaluate(
        """() => {
            const out = {};
            for (const sel of ['#main-pane', '#chat-messages', '#doc-panel']) {
              const el = document.querySelector(sel);
              if (!el) continue;
              el.scrollTop = el.scrollHeight;
              out[sel] = [el.scrollTop, el.scrollHeight, el.clientHeight];
            }
            return out;
        }"""
    )
    scrollable = [s for s, (_top, sh, ch) in scrolled.items() if sh > ch]
    info(f"item10 [{state}] SC4 滚到底",
         f"{scrolled}([scrollTop, scrollHeight, clientHeight]);"
         f"真的可滚的容器={scrollable}")
    if not scrollable:
        blocked(item,
                f"[{state}] SC4 滚到底后每个新 Tab 聚焦元素的 clearance >= "
                f"{CLEARANCE_MIN_PX:.0f}px",
                "至少一个裁剪容器真的可滚(scrollHeight > clientHeight)",
                f"{scrolled}",
                "撑高之后仍没有容器可滚 ⇒「滚到底」是 no-op,本断言退化成普通 clearance "
                "检查,不记 PASS(item8 对 sticky 表头用的是同一条判据)。本条是 fail-closed "
                "兜底:正常路径下撑高必然让 #main-pane / #doc-panel 可滚,走到这里说明"
                "撑高失效(应用的渲染函数改名 / 样本结构变了),不是「样本恰好不可滚」")
        return

    _idi07_blur_reset(page)
    rows = []
    for _ in range(_IDI07_TAB_LIMIT):
        page.keyboard.press("Tab")
        row = page.evaluate(_IDI07_TAB_CLEARANCE_JS)
        if row is not None:
            rows.append(row)
    info(f"item10 [{state}] SC4 clearance 普查(全部原始行)",
         f"{len(rows)} 行:"
         f"{[(r['label'], r['container'], r['clearance'], r['visible']) for r in rows]}")
    judged = [r for r in rows if r["visible"] and r["clearance"] is not None]
    if not judged:
        blocked(item,
                f"[{state}] SC4 滚到底后每个新 Tab 聚焦元素的 clearance >= "
                f"{CLEARANCE_MIN_PX:.0f}px",
                f">= {CLEARANCE_MIN_PX:.0f}px",
                f"判定集为空(共 {len(rows)} 行原始读数)",
                "滚到底后没有任何新 Tab 聚焦到的可见元素(或它们全部没有裁剪祖先)⇒ 本样本"
                "无判定,不记 PASS。item_verdict 只读行级裁决,未判定的探针会以 PASS 现身")
        return
    bad = [r for r in judged if r["clearance"] < CLEARANCE_MIN_PX]
    ok_true(item,
            f"[{state}] SC4 滚到底后每个新 Tab 聚焦元素的 clearance >= "
            f"{CLEARANCE_MIN_PX:.0f}px",
            not bad, f"全部 >= {CLEARANCE_MIN_PX:.0f}px",
            f"共 {len(judged)} 行,未达标 "
            f"{[(r['label'], r['container'], round(r['clearance'], 1)) for r in bad]}",
            f"{CLEARANCE_MIN_PX:.0f}px = 环的 outline {FOCUS_RING_WIDTH_PX:.0f}px + "
            f"outline-offset {FOCUS_RING_OFFSET_PX:.0f}px 的外伸量。实测未达标时**只改"
            "那一个容器**的 padding 为 var(--space-1),禁止「为确定性四个全抬」")


# 过渡落地后,「交互后立刻读」不再等于「读到终态」。计划 03 的 Task 1 给 button / input /
# select 挂了 120ms 的 background-color / border-color 过渡(D-12),于是 hover 或 mouse.down
# 之后的一次性读数会读到**过渡中间值** —— 实测 #message-input 读到 rgb(112, 112, 112),
# 而终态是 rgb(100, 100, 100);裁决按钮的悬停/按下读数同理。这不是 CSS 写错,是「读数时刻」
# 早于「终态时刻」。本读取器先等两帧(确保过渡已被注册)再 `await` 该元素上所有动画
# `finished`,然后才读数 —— 判据要的是**终态**,不是动画的任意一帧。
_IDI07_SETTLED_READ_JS = r"""async ([sel, prop]) => {
  const el = document.querySelector(sel);
  if (!el) return null;
  await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
  const anims = el.getAnimations();
  await Promise.all(anims.map((a) => a.finished.catch(() => {})));
  return getComputedStyle(el)[prop];
}"""


def read_settled_style(page, selector, prop):
    """读**过渡终态**的 computed style。

    只用于「交互触发了过渡 ⇒ 立刻读会读到中间值」的那几处探针。其余探针仍用
    `read_style`:它们读的量要么不参与过渡(`box-shadow` / `outline`),要么未被交互
    改变,给它们加等待只会拖慢 harness 而不改变结论。
    """
    return page.evaluate(_IDI07_SETTLED_READ_JS, [selector, prop])


def _idi07_hover_border_assert(page, item, state, sel, label):
    """输入控件的 hover 边界断言(D-10):静默读 border-color → hover → 再读,断言变为令牌值。

    期望侧来自 `resolve_color(page, "--color-border-hover")`,**不硬编码 rgb**(这是本文件
    立下的纪律:值的仲裁者是 `scripts/check-02-contrast.py`)。

    两条断言缺一不可:①hover 后 == 令牌值;②hover 后 != 静默值。只留 ① 时,若 hover 规则
    完全没生效、而静默值恰好等于期望值,断言会静默通过 —— ② 是它的对照半场。

    前提不成立(元素不存在 / rect 全零 / 被禁用)⇒ `blocked(...)`,**绝不记 PASS**。
    """
    pre = page.evaluate(_IDI07_INTERACTIVE_JS, [sel])
    if pre is None or not pre.get("ok"):
        blocked(item, f"[{state}] {label} hover 后 border-color == var(--color-border-hover)",
                "元素存在、可见且未被禁用",
                "<MISSING>" if pre is None else f"ok=False why={pre.get('why')}",
                "目标不可交互 ⇒ 本断言失去证明力,不记 PASS")
        return
    expected = resolve_color(page, "--color-border-hover")
    if expected is None:
        blocked(item, f"[{state}] {label} hover 后 border-color == var(--color-border-hover)",
                "非 None 的 computed rgb", "<MISSING>",
                "令牌未声明 ⇒ 期望侧解析不出,本断言不记 PASS")
        return
    page.mouse.move(0, 0)
    before = read_settled_style(page, sel, "border-color")
    page.hover(sel)
    after = read_settled_style(page, sel, "border-color")
    info(f"item10 [{state}] {label} hover 边界读数",
         f"sel={sel} 静默={before} hover={after} 期望={expected}")
    ok_true(item,
            f"[{state}] {label} hover 后 border-color == var(--color-border-hover)",
            norm(after) == norm(expected), expected, after,
            "D-10:静默是 --color-border-strong(gray-9),hover 加深一步到 "
            "--color-border-hover(gray-11)。期望侧来自运行时解析的令牌,不硬编码 rgb")
    ok_true(item,
            f"[{state}] {label} hover 后 border-color != 静默值",
            norm(after) != norm(before), f"!= {before}", after,
            "对照半场:只断言「等于令牌值」时,若 hover 规则没生效而静默值恰好等于期望值,"
            "那条断言会静默通过")


def _idi07_sc5_filled_assert(page, item, state, sel, label):
    """SC5 的填充半场(D-08):hover 时 `background-color` **不变**、`box-shadow` 出现 inset 叠层;
    按住不放时叠层的 alpha 从 hover 的令牌值提到 active 的令牌值。

    期望侧的 alpha 由 `resolve_color(page, "--color-overlay-hover" / "--color-overlay-active")`
    解析,**不硬编码 rgba 字面量**。浏览器把 `inset 0 0 0 999px <c>` 序列化成
    `<c> 0px 0px 0px 999px inset`,故判据是三者的合取(见 `_IDI07_OVERLAY_SPREAD` 的注释)。

    前提检查里 `disabled` 是**承重的**:本探针的目标必须真的可交互 —— 一个渲染出来的禁用
    按钮照样有非零 rect,却永远不匹配 `:not(:disabled)` 的选择器,断言会 FAIL 而不是
    BLOCKED(这正是本任务最初的探针目标写错的地方)。

    按下读完**先把指针移开再抬手**:`#btn-send` 的 click 会真的发一条消息,在按钮上原地
    上抬会污染样本状态。
    """
    pre = page.evaluate(_IDI07_INTERACTIVE_JS, [sel])
    if pre is None or not pre.get("ok"):
        blocked(item, f"[{state}] SC5 {label} hover 出现 inset 叠层",
                "元素存在、可见且未被禁用",
                "<MISSING>" if pre is None else f"ok=False why={pre.get('why')}",
                "目标不可交互 ⇒ 本断言失去证明力,不记 PASS")
        return
    if pre.get("disabled"):
        blocked(item, f"[{state}] SC5 {label} hover 出现 inset 叠层",
                "未被禁用(即 :not(:disabled) 的选择器能匹配到它)",
                f"disabled=True rect={pre.get('rect')}",
                "「可见」不等于「可交互」:禁用按钮的 rect 非零,却永远不匹配 "
                ":not(:disabled) 的选择器,拿它做本断言会 FAIL 而非 BLOCKED。换一个样本内"
                "真正可用的填充按钮")
        return
    hover_color = resolve_color(page, "--color-overlay-hover")
    active_color = resolve_color(page, "--color-overlay-active")
    if hover_color is None or active_color is None:
        blocked(item, f"[{state}] SC5 {label} hover 出现 inset 叠层",
                "两个叠层令牌都能被运行时解析", f"{hover_color} / {active_color}",
                "令牌未声明 ⇒ 期望侧解析不出,本探针不记 PASS")
        return

    page.mouse.move(0, 0)
    bg_before = read_style(page, sel, "background-color")
    shadow_before = read_style(page, sel, "box-shadow")
    page.hover(sel)
    bg_after = read_style(page, sel, "background-color")
    shadow_after = read_style(page, sel, "box-shadow")

    page.mouse.down()
    shadow_pressed = read_style(page, sel, "box-shadow")
    # 先移开再抬手:原地上抬会触发 click 并发出一条消息。
    page.mouse.move(0, 0)
    page.mouse.up()

    info(f"item10 [{state}] SC5 {label} 填充按钮读数",
         f"sel={sel} rect={pre.get('rect')} "
         f"bg[静默={bg_before} hover={bg_after}] "
         f"shadow[静默={shadow_before} hover={shadow_after} 按下={shadow_pressed}] "
         f"期望 hover={hover_color} active={active_color}")

    ok_true(item,
            f"[{state}] SC5 {label} hover 时 background-color 不变",
            norm(bg_after) == norm(bg_before), bg_before, bg_after,
            "D-08:叠层走 box-shadow 的 inset,填充色本身不动。改填充色(或加 opacity)会把"
            "白字一起压暗,三个色族会跌破 AA 4.5:1")
    ok_true(item,
            f"[{state}] SC5 {label} hover 出现 inset 叠层(含 {_IDI07_OVERLAY_SPREAD} 铺满分量)",
            "inset" in (shadow_after or "") and _IDI07_OVERLAY_SPREAD in (shadow_after or ""),
            f"含 'inset' 与 '{_IDI07_OVERLAY_SPREAD}'",
            f"静默={shadow_before} hover={shadow_after}",
            "D-08:本文件既有的 box-shadow: inset 只有 3px 竖条形态;999px 大于任何按钮的"
            "盒宽 ⇒ 等价于整面覆盖。box-shadow 不参与布局 ⇒ 零位移")
    ok_true(item,
            f"[{state}] SC5 {label} hover 叠层的颜色 == var(--color-overlay-hover)",
            norm(hover_color) in norm(shadow_after or ""), f"含 {hover_color}",
            shadow_after,
            "期望侧来自运行时解析的令牌,不硬编码 rgba 字面量")
    ok_true(item,
            f"[{state}] SC5 {label} 按住不放时叠层的颜色 == var(--color-overlay-active)",
            norm(active_color) in norm(shadow_pressed or ""), f"含 {active_color}",
            shadow_pressed,
            "D-09:alpha 从 0.06 提到 0.12。这一条与上一条合起来证明按下态真的换了一份叠层,"
            "而不是 hover 读数的回声")
    ok_true(item,
            f"[{state}] SC5 {label} 按住不放时的叠层 != hover 时的叠层",
            norm(shadow_pressed) != norm(shadow_after), f"!= {shadow_after}", shadow_pressed,
            "对照半场:若 active 组没有落地(或 alpha 与 hover 相同),按下读数就是 hover 读数,"
            "上面那条「含 active 颜色」的断言在有 active 组时必然成立、无 active 组时不会变红")


def _idi07_sc5_naive_press_assert(page, item, state):
    """SC5-朴素按下(D-09):朴素无底色按钮「静默 → 悬停 → 按住不放」三次读数递进,
    且**按住不放的读数与悬停的读数不相等**。

    为什么必须显式断言「不相等」:若 L587 的让位(`:where(:not(:active))`)没生效,第三次
    读到的就是第二次的值 —— 而「③ == --color-surface-active」这条断言**仍然成立**(它只要求
    等于期望值,不要求不等于 hover)。故「③ != ②」这半条是 D-09 的判据本体,不是补强。

    目标取本探针用 `renderVerdictCard()` 造出的裁决卡的首个按钮 —— 它是本仓库里**在样本中
    稳定可达的朴素无底色按钮**(`.modal-buttons button` / `.tier-buttons button` 虽然也叫
    「模态按钮」,但它们都在 `.overlay-card` 内,已被 `.overlay-card button`(0-1-1)填成主色,
    不是朴素族)。

    读完**先把指针移开再抬手**:裁决按钮的 click 会触发 app.js 的 `submit('修')` 并发一次
    `POST /api/checks/verdict`,在按钮上原地上抬会真的发请求并改动样本状态。
    """
    built = page.evaluate(_IDI07_BUILD_VERDICT_CARD_JS)
    info(f"item10 [{state}] SC5-朴素按下 裁决卡构造",
         f"renderVerdictCard(...) → {built}")
    if built is None or built.get("buttons", 0) < 1:
        blocked(item, f"[{state}] SC5-朴素按下 静默 → 悬停 → 按住不放 的三次读数递进",
                "renderVerdictCard(...) 造出的卡里 >= 1 个 .verdict-buttons button",
                "<MISSING>",
                "造不出裁决卡 ⇒ 被测状态不存在,不记 PASS。绝不用「都不可用」换一条 PASS")
        return
    sel = f"#{_IDI07_VERDICT_PROBE_ID} .verdict-buttons button"
    pre = page.evaluate(_IDI07_INTERACTIVE_JS, [sel])
    if pre is None or not pre.get("ok") or pre.get("disabled"):
        blocked(item, f"[{state}] SC5-朴素按下 静默 → 悬停 → 按住不放 的三次读数递进",
                "该按钮存在、可见且未被禁用",
                "<MISSING>" if pre is None else f"ok={pre.get('ok')} "
                f"disabled={pre.get('disabled')} why={pre.get('why')}",
                "裁决按钮造出来了却不可交互 ⇒ 本断言失去证明力,不记 PASS")
        return
    surface = resolve_color(page, "--color-surface")
    hover = resolve_color(page, "--color-surface-hover")
    active = resolve_color(page, "--color-surface-active")
    if surface is None or hover is None or active is None:
        blocked(item, f"[{state}] SC5-朴素按下 静默 → 悬停 → 按住不放 的三次读数递进",
                "三个 surface 令牌都能被运行时解析", f"{surface} / {hover} / {active}",
                "令牌未声明 ⇒ 期望侧解析不出,本探针不记 PASS")
        return

    page.mouse.move(0, 0)
    silent = read_settled_style(page, sel, "background-color")
    page.hover(sel)
    hovered = read_settled_style(page, sel, "background-color")
    page.mouse.down()
    pressed = read_settled_style(page, sel, "background-color")
    # 先移开再抬手 —— 见 docstring。
    page.mouse.move(0, 0)
    page.mouse.up()
    info(f"item10 [{state}] SC5-朴素按下 读数",
         f"sel={sel} rect={pre.get('rect')} "
         f"① 静默={silent} ② 悬停={hovered} ③ 按住不放={pressed} "
         f"期望 {surface} / {hover} / {active}")

    ok_true(item,
            f"[{state}] SC5-朴素按下 ① 静默 background-color == var(--color-surface)",
            norm(silent) == norm(surface), surface, silent,
            "朴素按钮的底色来自 button 基础规则(0-0-1)的 --color-surface")
    ok_true(item,
            f"[{state}] SC5-朴素按下 ② 悬停 background-color == var(--color-surface-hover)",
            norm(hovered) == norm(hover), hover, hovered,
            "L587 的 hover 对朴素按钮仍然生效 —— D-07 的 gate 只排除禁用按钮,不排除朴素按钮")
    ok_true(item,
            f"[{state}] SC5-朴素按下 ③ 按住不放 background-color == var(--color-surface-active)",
            norm(pressed) == norm(active), active, pressed,
            "朴素 active 停在 0-1-0,高于 button 基础规则(0-0-1)⇒ 按下反馈成立")
    ok_true(item,
            f"[{state}] SC5-朴素按下 ③ 按住不放读数 != ② 悬停读数",
            norm(pressed) != norm(hovered), f"!= {hovered}", pressed,
            "**D-09 的判据本体。** 若 L587 的让位(:where(:not(:active)))没生效,③ 会读到 ② 的值,"
            "而上面那条「③ == surface-active」**仍然成立**(它只要求等于期望值)⇒ 只断言相等时"
            "让位失效的实现不会变红。实测相等 ⇒ 到 frontend/style.css 检查 L587 那条规则的选择器"
            "是否还带着让位")


def _idi07_sc5prime_disabled_assert(page, item, state):
    """SC5′(D-07 的 gate 生效证明):禁用按钮 hover 时 `background-color` 与静默**相同**,
    且计算 `opacity` 未被软化(仍为 0.5)。

    **复用 SC5-朴素按下 已经造好的那张卡**,不重复造第二张。`.disabled` 由 `page.evaluate`
    置真 —— 这正是 `frontend/app.js:718-719` 在 `submit` 里做的真实状态切换,不是伪造 DOM。

    本条今天会 FAIL:未 gate 的 `button:hover`(0-1-1)会给 `.verdict-buttons button:disabled`
    (它只设 opacity / cursor、不钉 background)上 --color-surface-hover。
    """
    sel = f"#{_IDI07_VERDICT_PROBE_ID} .verdict-buttons button"
    pre = page.evaluate(_IDI07_INTERACTIVE_JS, [sel])
    if pre is None or not pre.get("ok"):
        blocked(item, f"[{state}] SC5′ 禁用按钮 hover 时 background-color == 静默值",
                "SC5-朴素按下 造出的那张探针裁决卡仍在 DOM 里且按钮可见",
                "<MISSING>" if pre is None else f"ok=False why={pre.get('why')}",
                "探针卡不存在或不可见 ⇒ 本断言失去证明力,不记 PASS")
        return
    flipped = page.evaluate(_IDI07_DISABLE_VERDICT_BUTTONS_JS,
                            [f"#{_IDI07_VERDICT_PROBE_ID}"])
    if not flipped or not all(flipped):
        blocked(item, f"[{state}] SC5′ 禁用按钮 hover 时 background-color == 静默值",
                "两个裁决按钮的 .disabled 均为 True", f"{flipped}",
                "禁用态切换失败 ⇒ 被测状态不存在,不记 PASS")
        return

    page.mouse.move(0, 0)
    silent = read_style(page, sel, "background-color")
    opacity = read_style(page, sel, "opacity")
    page.hover(sel)
    hovered = read_style(page, sel, "background-color")
    page.mouse.move(0, 0)
    info(f"item10 [{state}] SC5′ 禁用按钮读数",
         f"sel={sel} 静默={silent} hover={hovered} opacity={opacity}")

    ok_true(item,
            f"[{state}] SC5′ 禁用按钮 hover 时 background-color == 静默值",
            norm(hovered) == norm(silent), silent, hovered,
            "D-07 的 gate 证明:L587 的选择器带 :where(:not(:disabled)),禁用按钮不再匹配它。"
            "实测不等 ⇒ 到 frontend/style.css 检查那条 hover 规则的选择器是否还带着 gate")
    ok_true(item,
            f"[{state}] SC5′ 禁用按钮的计算 opacity 仍为 {_IDI07_DISABLED_OPACITY}(未被软化)",
            opacity == _IDI07_DISABLED_OPACITY, _IDI07_DISABLED_OPACITY, opacity,
            "禁用态是 G3 前提条件唯一的视觉信号,不得软化;.verdict-buttons button:disabled "
            "用的是 0.5,不是 0.55")


# ---------------------------------------------------------------------------
# 第 10 项的**静态**契约计数守卫(D-15 中段,计划 03 追加)
# ---------------------------------------------------------------------------
def _idi07_code_only(line, in_comment):
    """返回 (该行注释之外的代码片段, 行末是否仍在注释内)。

    CSS 里没有嵌套注释,本文件也没有把 `/*` 写进字符串的先例(data-URI 是
    `url("…")`,其中的 SVG 不含这两个字符序列),故逐字符扫描足够。
    不做这一步,规则上方那段「为什么枚举而不是裸 `:focus-visible`」的论证散文会被
    当成一条规则块,块内计数随即失去意义。
    """
    out, i = [], 0
    while i < len(line):
        if in_comment:
            end = line.find("*/", i)
            if end == -1:
                i = len(line)
            else:
                in_comment = False
                i = end + 2
        else:
            start = line.find("/*", i)
            if start == -1:
                out.append(line[i:])
                i = len(line)
            else:
                out.append(line[i:start])
                in_comment = True
                i = start + 2
    return "".join(out), in_comment


def _idi07_focus_rule_blocks(text):
    """切出所有含 `:focus-visible` 的**规则块**:[(起始行号, [(行号, 代码片段), …]), …]。

    从选择器行到**第一个 `}`** —— 这正是「规则块」的形态。注释里的 `:focus-visible`
    提及不算规则块(见 `_idi07_code_only`)。
    """
    lines = text.splitlines()
    blocks, in_comment, i = [], False, 0
    while i < len(lines):
        code, in_comment = _idi07_code_only(lines[i], in_comment)
        if ":focus-visible" in code:
            start, buf = i, []
            while i < len(lines):
                code_i, in_comment = _idi07_code_only(lines[i], in_comment)
                buf.append((i + 1, code_i))
                if "}" in code_i:
                    break
                i += 1
            blocks.append((start + 1, buf))
        i += 1
    return blocks


_DECL_PROP_RE = re.compile(r"(?:^|[;{])\s*([-a-zA-Z]+)\s*:")


def _idi07_block_declarations(buf):
    """块内的 (行号, 声明属性名) 列表 —— 只看 `{` 之后的部分(选择器行不是声明)。"""
    out, seen_brace = [], False
    for lineno, code in buf:
        if not seen_brace:
            if "{" not in code:
                continue
            seen_brace = True
            code = code.split("{", 1)[1]
        out.extend((lineno, m.group(1)) for m in _DECL_PROP_RE.finditer(code))
    return out


def _idi07_fence_split(text):
    """把 style.css 切成 (围栏内, 围栏外) 两段 —— awk 状态机(照 check-01 L27)。

    围栏标记各出现一次是前提(围栏标记行自身不计入任何一段)。标记不成对时返回
    `(None, None)`,由调用方记 BLOCKED —— 切分不可信时任何计数都不可信。
    """
    if text.count(FENCE_START_MARKER) != 1 or text.count(FENCE_END_MARKER) != 1:
        return None, None
    inside, outside, fenced = [], [], False
    for line in text.splitlines():
        if FENCE_START_MARKER in line:
            fenced = True
            continue
        if FENCE_END_MARKER in line:
            fenced = False
            continue
        (inside if fenced else outside).append(line)
    return "\n".join(inside), "\n".join(outside)


def _idi07_durations(raw):
    """把 computed `transition-duration` 拆成规范化列表(Chrome 用 `, ` 连接多个值)。

    **必须拆开再逐项比**,不能对整串做子串包含:两个属性的时长序列化成
    `"0.12s, 0.12s"`,而 `"0s"` 是它的子串 —— 子串判据会让「reduce 下必须全为 0s」
    这条断言在**未生效**时假绿。这正是本文件 docstring 点名的同型陷阱。
    """
    if raw is None:
        return None
    return [p.strip() for p in raw.split(",") if p.strip()]


def _idi07_focus_contract_guards(item):
    """D-15 中段的四条**契约计数静态断言**(INTERACT-02 / D-11…D-14)。

    照 `_l2_guard_shape` 的三条共同纪律写:**`OSError` ⇒ `blocked()`**、
    **打印命中行号**、**比的是「实测计数 vs 独立决策常量」不是自比**。读的是
    **文件文本**而非渲染结果 —— 与 item10 的运行时普查互补:它抓「规则被悄悄删掉 /
    悄悄多写一条」,运行时普查抓「规则实际覆盖了谁」。

    第 ① 条**只数代码**:`text.count(":focus-visible")` 会把注释里的散文提及一并计入,
    而本文件的注释大量讨论 `:focus-visible` —— 那种计数在规则被整条删掉之后仍然
    >= 1,断言就与它守的东西脱钩了。用 `_idi07_focus_rule_blocks` 切出的**规则块数**
    作计数(它逐行跟踪注释状态,注释里的提及不算规则块),与第 ② 条同源、同一次切分。
    """
    try:
        text = STYLE_CSS.read_text(encoding="utf-8")
    except OSError as exc:
        blocked(item, "[static] frontend/style.css 可读", "读得到文件文本", "<MISSING>",
                f"{STYLE_CSS} 读不到:{exc}")
        return

    # ---- 断言 1:`:focus-visible` 计数 > 0(ROADMAP Phase 7 的 gate 原文)--------
    # **只数代码,不数注释提及。** 直接 `text.count(":focus-visible")` 会把文件里的
    # 散文提及一并计入 —— 实测本文件的 9 处命中里有 2 处是注释(L239 / L1482,两者都
    # 在本文件里讨论这条规则),于是**整条规则被删掉之后计数仍是 2 >= 1,断言照样
    # PASS**。这不是「阈值取宽」,是断言与它要守的东西脱钩。`_idi07_focus_rule_blocks`
    # 已经把注释剔掉了(它逐行跟踪注释状态),用它计数即得「规则块数」(实测 1 块,
    # 起始行 L1508),与下面断言 2 同源、同一次切分。
    fv_blocks = _idi07_focus_rule_blocks(text)
    fv_count = len(fv_blocks)
    fv_lines = [ln for ln, _ in fv_blocks]
    info("item10 [static] :focus-visible 计数",
         f"计数={fv_count}(只数代码,注释提及不计;规则块起始行={fv_lines});"
         f"期望 >= {EXPECTED_FOCUS_VISIBLE_MIN}")
    ok_true(item,
            f"[static] frontend/style.css 的 :focus-visible 计数 >= {EXPECTED_FOCUS_VISIBLE_MIN}",
            fv_count >= EXPECTED_FOCUS_VISIBLE_MIN,
            f">= {EXPECTED_FOCUS_VISIBLE_MIN}", fv_count,
            "判据是 `>=` 而不是 `==`:七选择器枚举天然大于 1,日后按枚举纪律新增一类"
            "可聚焦元素会让它继续变大 —— 相等判据会把「按纪律扩展」误判成回归。"
            "计的是**规则块数**(注释剔除后),不是全文件子串数:后者会把散文提及算进来,"
            "规则删光也仍然 PASS")

    # ---- 断言 2:没有任何焦点规则设置 border 或 padding(块提取,非全文件 grep)----
    blocks = _idi07_focus_rule_blocks(text)
    if not blocks:
        blocked(item, "[static] 没有任何含 :focus-visible 的规则块设置 border / padding",
                ">= 1 个含 :focus-visible 的规则块", "<MISSING>",
                "一条规则块都切不出来 ⇒ 本断言无判定对象,不记空转 PASS")
        return
    all_decls = [(n, p) for _, buf in blocks for n, p in _idi07_block_declarations(buf)]
    bad_decls = [(n, p) for n, p in all_decls
                 if p in ("border", "padding")
                 or p.startswith("border-") or p.startswith("padding-")]
    info("item10 [static] 焦点规则块",
         f"块起始行={[b[0] for b in blocks]};块内全部声明={all_decls}")
    ok_true(item,
            "[static] 没有任何含 :focus-visible 的规则块设置 border / padding",
            not bad_decls, "0 条 border / padding 声明",
            f"{len(bad_decls)} 条:{bad_decls}",
            "D-05:焦点规则只能用不参与布局的 outline —— border / padding 会 reflow "
            "#probe-controls 并位移。必须用**块提取**而不是全文件 grep:全文件里 "
            "border / padding 到处都是,只有块内计数能回答「焦点规则自己设了没有」。"
            "失败时按上面行号定位到具体规则与属性")

    # ---- 断言 3:减弱动效偏好与新增过渡同时存在(并逐字声明其局限)---------------
    prm_count = text.count("prefers-reduced-motion")
    tr_count = text.count("transition: background-color 120ms")
    info("item10 [static] 减弱动效 × 新增过渡",
         f"prefers-reduced-motion 计数={prm_count};"
         f"transition: background-color 120ms 计数={tr_count};"
         "**本断言不证明「同提交」** —— 「同提交」是 git 维度的事实,文件文本断言在结构上"
         "无法证明它。本断言只退化为「两者同时存在」。同提交只能落成计划 / 评审义务:"
         "本计划的 Task 1 已把它写进 <verify> 与 <done>,并由那一次提交的 diff 承载")
    ok_true(item,
            "[static] prefers-reduced-motion 与新增过渡同时存在",
            prm_count >= 1 and tr_count >= 1, ">= 1 且 >= 1",
            f"{prm_count} / {tr_count}",
            "⚠ 本断言**不证明同提交**(见上面 INFO 行):它只证明两者同时存在。"
            "「同提交」是 git 维度的事实,只能由计划 / 评审义务承担")

    # ---- 断言 4:五个令牌「围栏内声明恰好一次 ∧ 围栏外被消费」(硬规则 5)-------
    inside, outside = _idi07_fence_split(text)
    if inside is None:
        blocked(item, "[static] 每个交互态令牌「围栏内声明一次 ∧ 围栏外被消费」",
                f"围栏标记各出现一次({FENCE_START_MARKER} / {FENCE_END_MARKER})",
                f"start={text.count(FENCE_START_MARKER)} "
                f"end={text.count(FENCE_END_MARKER)}",
                "围栏标记不成对 ⇒ 切分不可信,本断言不记 PASS"
                "(check-01 对同一对标记有独立断言)")
        return
    for token in _IDI07_DECLARED_AND_CONSUMED:
        decl = inside.count(f"{token}:")
        cons = outside.count(f"var({token})")
        info("item10 [static] 令牌声明 / 消费",
             f"{token}: 围栏内声明={decl} 围栏外消费={cons}")
        ok_true(item,
                f"[static] {token} 围栏内声明 == 1 且围栏外被消费 > 0",
                decl == 1 and cons > 0, "声明 1 且消费 > 0", f"声明 {decl} / 消费 {cons}",
                "硬规则 5「与消费者同提交」的机械形态:声明侧抓改名残留(声明了两次),"
                "消费侧抓死令牌(声明了却没人用)。围栏外只认 var() 形态 —— "
                "裸令牌名不是消费")


def _idi07_transition_motion_assert(page, item, state):
    """过渡与减弱动效的**运行时**探针(D-12 / D-13 / D-11;硬规则 7)。

    两段:
    (a) 静默态:button / input / select 的 `transition-property` 含 `background-color`
        与 `border-color`,`transition-duration` 为 0.12s;`.event-list` 是
        `background-color` 与 0.3s —— **D-11 的具名例外在运行时可见**,不是一句只写在
        注释里的说法。
    (b) `page.emulate_media(reduced_motion="reduce")` 下重读四个元素的
        `transition-duration`,断言**全部**为 0s(含 `.event-list`)。

    ⚠ 读完**立即**复位 `reduced_motion="no-preference"`,与 `VIEWPORT_RESTORE` 同级纪律:
    媒体模拟是页面级的,不复位会污染其后各项 UAT。
    ⚠ 元素读不到 ⇒ `blocked(...)`,**绝不记 PASS**。
    """
    readings, missing = [], []
    for sel, label in _IDI07_MOTION_TARGETS:
        prop = read_style(page, sel, "transition-property")
        dur = read_style(page, sel, "transition-duration")
        if prop is None or dur is None:
            missing.append((sel, label))
            continue
        readings.append({"sel": sel, "label": label, "prop": prop, "dur": dur})
    if missing:
        blocked(item, f"[{state}] 过渡挂载规则的四个目标元素都读得到 computed transition",
                "button / input / select / .event-list 四个目标均可读", f"读不到:{missing}",
                "元素不存在 ⇒ getComputedStyle 读不出值;本探针不记 PASS")
        return

    info(f"item10 [{state}] 过渡读数(全部原始值)",
         f"{[(r['label'], r['prop'], r['dur']) for r in readings]}")
    controls = [r for r in readings if r["label"] != ".event-list"]
    bad_prop = [(r["label"], r["prop"]) for r in controls
                if "background-color" not in r["prop"] or "border-color" not in r["prop"]]
    bad_dur = [(r["label"], r["dur"]) for r in controls
               if _idi07_durations(r["dur"]) != [_IDI07_TRANSITION_DURATION] * 2]
    ok_true(item,
            f"[{state}] button / input / select 的 transition-property 含 "
            "background-color 与 border-color",
            not bad_prop, "三个控件都含这两个属性", f"不符:{bad_prop}",
            "D-12 的挂载规则只声明这两个属性;opacity 与 outline-* 刻意不在列表内(D-14)")
    ok_true(item,
            f"[{state}] button / input / select 的 transition-duration 两项均为 "
            f"{_IDI07_TRANSITION_DURATION}",
            not bad_dur, f"[{_IDI07_TRANSITION_DURATION}] * 2", f"不符:{bad_dur}",
            "Chrome 把 120ms 序列化成 '0.12s',两个属性序列化成 '0.12s, 0.12s' —— "
            "判据先拆成列表再逐项比,不用子串包含")

    el_row = next(r for r in readings if r["label"] == ".event-list")
    ok_true(item,
            f"[{state}] .event-list 的 transition-duration == {_IDI07_EVENT_LIST_DURATION}"
            "(D-11 的具名例外在运行时可见)",
            _idi07_durations(el_row["dur"]) == [_IDI07_EVENT_LIST_DURATION]
            and "background-color" in el_row["prop"],
            f"background-color 且时长 {_IDI07_EVENT_LIST_DURATION}",
            f"prop={el_row['prop']} dur={el_row['dur']}",
            "D-11:300ms 那个时长**不是控件态**,它服务 .streaming / .aborted 两个流式状态"
            "指示类。把「例外仍在」变成可观测事实,而不是只写在注释里")

    page.emulate_media(reduced_motion="reduce")
    try:
        reduced = [(label, read_style(page, sel, "transition-duration"))
                   for sel, label in _IDI07_MOTION_TARGETS]
    finally:
        # ⚠ 复位与 VIEWPORT_RESTORE 同级纪律:媒体模拟是页面级的,不复位会污染其后各项。
        page.emulate_media(reduced_motion="no-preference")
    info(f"item10 [{state}] reduce 下的 transition-duration(全部原始值)", f"{reduced}")
    bad_reduced = [(lbl, raw) for lbl, raw in reduced
                   if _idi07_durations(raw) != [_IDI07_REDUCED_DURATION]]
    ok_true(item,
            f"[{state}] reduced_motion='reduce' 下 button / input / select / .event-list 的 "
            f"transition-duration 全为 {_IDI07_REDUCED_DURATION}",
            not bad_reduced, f"四个目标全为 {_IDI07_REDUCED_DURATION}",
            f"不符:{bad_reduced}",
            "D-13:按选择器重写为 none,而不是把时长压到「几乎为零」。读完后已复位 "
            "reduced_motion='no-preference',否则会污染其后各项")


def item10(page, tmp_root):
    item = "10"
    print("\n=== UAT 10: A11Y-01 焦点环(D-05 / D-16 / D-17)===", flush=True)

    # ---- (a) 静态契约计数守卫(D-15 中段)先跑,不依赖任何运行时状态 -------------
    _idi07_focus_contract_guards(item)

    # 环色的期望侧来自**运行时解析的令牌**(resolve_color),**不得硬编码**
    # rgb(31, 99, 189) —— 这是本文件立下的纪律:期望侧来自运行时解析的令牌,
    # 值的仲裁者是 scripts/check-02-contrast.py。
    #
    # **单个样本内的探针执行顺序是承重的,必须写死:Tab 驱动的探针
    # (普查 → SC1 → SC4)先全部跑完,`page.click()` 驱动的 SC2 最后跑。** 理由是实测的
    # 浏览器行为:一次 `page.click()` 之后,紧随其后的 Tab 落点会变(实测 click 后第一次
    # Tab 可能落回 BODY,那里 `:focus-visible` 为假、`outline-width` 是 UA 的 3px)。
    # 故 SC2 若排在 SC1 之前,SC1 的读数会读到 BODY 的 UA 默认值而 FAIL —— 那不是探针
    # 写错,是顺序写错。
    proj = make_fixture("p1", tmp_root)
    enter_project(page, proj)
    info("item10 样本", f"p1(会话流活动态)→ {proj}")

    focus_color = resolve_color(page, "--color-focus")
    if focus_color is None:
        blocked(item, "[p1] --color-focus 已声明且可被运行时解析",
                "非 None 的 computed rgb", "<MISSING>",
                "令牌未声明 ⇒ 期望侧解析不出,本项全部探针不记 PASS")
        page.set_viewport_size(VIEWPORT_RESTORE)
        return
    info("item10 令牌解析", f"--color-focus={focus_color}")

    # ---- p1:普查 → SC1 → SC4 → SC5 → SC2(鼠标驱动的那条 click 必须最后)------
    _idi07_focus_census_assert(page, item, "p1", focus_color)
    _idi07_sc1_assert(page, item, "p1", focus_color)
    _idi07_sc4_assert(page, item, "p1", focus_color)
    # 过渡与减弱动效(D-12 / D-13 / D-11)的运行时探针。排在 Tab 驱动的三条之后、SC5 之前:
    # 它只读 computed transition 并短暂模拟媒体偏好(读毕立即复位),不改焦点、不改滚动,
    # 故不干扰 Tab 序列;排在 `page.click()` 驱动的 SC2 之前,符合「click 必须最后」那条顺序约束。
    _idi07_transition_motion_assert(page, item, "p1")
    # SC5 的填充半场取 `#btn-send`,**不用** `#btn-process-round`:后者在 p1 的标记里带
    # `disabled`(frontend/index.html:73),而 `#btn-process-round:not(:disabled):hover`
    # 根本不匹配它 —— 断言会 **FAIL 而非 BLOCKED**(`applySessionGates()` 只
    # `classList.remove('hidden')`、从不清 `disabled`;放开它的是阶段 3 路径上的
    # `updateFrozenPresentation()`)。`#btn-send` 在 p1 可用:`applySessionGates()`
    # 显式 `sendBtn.disabled = false`,全局唯一把它置真的是归档路径的
    # `applyArchiveView()`(p1 不走)。
    _idi07_sc5_filled_assert(page, item, "p1", "#btn-send", "#btn-send")
    _idi07_hover_border_assert(page, item, "p1", "#message-input", "#message-input")
    _idi07_sc2_assert(page, item, "p1", focus_color)

    # ---- checking / p3:各跑一遍普查与 SC1 -----------------------------------
    # 三样本合起来才覆盖全部 Tab 可达的可聚焦元素组合(照 item9 的教训:单样本会把
    # 「藏住」读成「不达标」)。`#checks-panel` 只在 checking 可见,批注面板只在 p3 可见。
    for state in ("checking", "p3"):
        proj = make_fixture(state, tmp_root)
        enter_project(page, proj)
        info("item10 样本", f"{state} → {proj}")
        _idi07_focus_census_assert(page, item, state, focus_color)
        _idi07_sc1_assert(page, item, state, focus_color)
        # SC5-朴素按下 / SC5′ / 动态输入框的 hover 边界**只在 checking 跑**:裁决卡挂在
        # `#verdict-cards` 下,而 `#checks-panel` 只在 checking 可见 —— p1 / p3 里造出来的卡
        # rect 全零,前提检查会记 BLOCKED(而不是记一条假 PASS)。
        #
        # 顺序是承重的:两个探针**共用同一张卡**,而 SC5′ 会把两个按钮的 `.disabled` 置真 ——
        # 故 SC5-朴素按下必须**先跑**(那时按钮还没被禁用)。
        if state == "checking":
            _idi07_sc5_naive_press_assert(page, item, state)
            # 第八条输入规则的唯一服务对象是 app.js 在裁决卡里**动态**建的那个输入框;
            # 静态样本里它不存在,不在这里断言就等于该选择器没有服务对象的证据。
            _idi07_hover_border_assert(
                page, item, state,
                f"#{_IDI07_VERDICT_PROBE_ID} .verdict-note-input",
                "动态 .verdict-note-input")
            _idi07_sc5prime_disabled_assert(page, item, state)

    # ---- viewport 纪律 ------------------------------------------------------
    # 本项用 page.click() 可能改变滚动位置;此处兜底复位(与 item 8 / item 9 同一纪律:
    # VIEWPORT_RESTORE 是 harness 的基准视口,不复位会污染其后各项)。
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
                    help="只跑指定项:smoke / 1 / 2 / 3 / 4 / 5 / 6 / 7 / 8 / 9 / 10(可重复,或逗号分隔)")
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
        return ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
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
    known = {"smoke", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"}
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
        if "10" in items:
            item10(page, tmp_root)
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
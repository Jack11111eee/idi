---
phase: 260918-qrq-frontend-chatgpt
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - frontend/index.html
  - frontend/style.css
  - frontend/app.js
  - DESIGN.md
  - .claude/CLAUDE.md
autonomous: true
requirements:
  - TOKEN-04
  - TOKEN-06
  - TOKEN-08
  - VISUAL-03
  - VISUAL-04
  - TYPE-01
  - TYPE-03
  - LAYOUT-01
  - LAYOUT-03
user_setup: []

estimate:
  tokens: 70000
  raw_tokens: 70000
  tasks: 4
  confidence: low

must_haves:
  truths:
    - "页面左侧是主区(会话流 / 本轮批注流 / 自检报告 / AI 工作面板),右侧是可折叠文档面板(进入表单 / 草稿 / 轮次文档)——旧版是文档区在左、会话流在右,本次为整体对调。"
    - "点文档面板标题 → 面板收成 48px 竖条(只留折叠指示符);再点 → 展开回原宽度。折叠态不落盘、刷新即展开。"
    - "主区内容列 768px 居中;文档面板宽度由单一令牌 `--doc-panel-w` 控制,收起态由 `--doc-panel-w-collapsed` 控制——改宽度只需改一个值。"
    - "状态徽标不再是 position:fixed 浮层:它落在文档面板标题行内,随面板滚动/收起,不遮挡任何滚动内容,`right: 448px` 魔法数从文件里消失(LAYOUT-01 / LAYOUT-03 同时闭合)。"
    - "划词批注在搬动后仍然成立:`#round-doc` 随文档面板移动,`#selection-menu` 只绑它——在文档面板里划词仍弹出菜单,批注仍落入主区的批注流。"
    - "助手消息不再有背景色、内边距、圆角与宽度上限——全宽裸排的正文;用户消息仍是浅灰(#ececec)圆角气泡、深色文字。两者仍靠同特异性的 .chat-ai 覆盖 .chat-bubble,源码顺序承重。"
    - "全站文字色阶收敛为三档:主文字 #0d0d0d、次要文字 #8f8f8f、白底;字号阶梯收敛为 12/14/16/18/24 五档;圆角 4 值;全页只剩一条影子令牌(输入框,三层叠加)。"
    - "四门结果:check-01 / check-03 / check-04 PASS;check-02 FAIL,且输出全部是「对比度低于阈值」行——不得出现 unknown token / malformed / coverage below floor,失败条目数与每条数值逐条抄进 SUMMARY 作为有意保留的偏差证据。"
    - "fence 内的 PAIR/ORDER 清单注释块一字未改(34 条 PAIR + 1 条 ORDER);scripts/check-01..04 四个脚本一字未改。"
    - ".annotation-answered 规则块仍在 .annotation-plain .annotation-note 规则之后(实测改动前 plain=669 / answered=852,改后须仍满足 answered > plain),位置未移动。"
    - "DESIGN.md §4.1/§4.2 与代码同批交付:§4.1 的布局图与职责描述已按新信息架构改写,§4.2 中「侧栏」措辞已改为「主区 / 文档面板」,版本号已随之推进——代码与权威文档之间不留漂移。"
  artifacts:
    - "frontend/index.html:两个容器对调——`<main id=\"main-pane\">` 承载原 #sidebar 的四个 section;`<aside id=\"doc-panel\">` 承载原 #doc-pane 的全部内容 + 新的面板标题行(含 #state-badge 与折叠指示符)"
    - "frontend/style.css:token fence 内 tier-1 值改写(--gray-900/700/600/500/100/50/25、--blue-700)、新增 tier-1 --gray-200;新增 tier-2 --color-surface-user / --shadow-composer / --fw-medium / --radius-lg / --lh-snug;布局令牌 --sidebar-w 改名 --doc-panel-w 并新增 --doc-panel-w-collapsed;删除 --text-sm 与 --shadow-overlay / --shadow-menu"
    - "frontend/style.css:#main-pane / #doc-panel / #doc-panel.collapsed / #doc-panel-header h1 / #doc-panel-body 五组新规则;.chat-ai 去气泡;.panel-header / .panel-body / #chat-input-row / .markdown-body / #state-badge 的几何与描边改写"
    - "frontend/app.js:文档面板折叠处理器(与既有 #ai-panel 折叠处理器同形,约 8 行)"
    - "DESIGN.md:§4.1 布局段与 §4.2 划词批注交互段的修订 + 版本行推进"
    - ".planning/quick/260918-qrq-frontend-chatgpt/260918-qrq-SUMMARY.md:含 check-02 偏差证据表(失败条目数 + 每条 ratio 与阈值 + 该 pair 是否对应真实渲染)与人工验收清单"
  key_links:
    - "#round-doc 随 #doc-panel 搬动 → #selection-menu 的 mouseup/keyup 绑定只挂在 #round-doc 元素本身(app.js:1340-1341)→ 搬动不断绑定;selectionInRoundDoc 用 roundDoc.contains(el) 判断,与容器层级无关"
    - "index.html 的容器对调 → app.js 全部元素句柄走 getElementById(不依赖 DOM 层级)→ 搬动不断 JS;两个被改名的容器 id(#sidebar / #doc-pane)在 app.js 里零引用(已 grep 证实)"
    - "fence 内 --gray-200 → 同提交声明 --color-surface-user → .chat-user 的 background(唯一消费者,Hard Rule 5)"
    - "新增 --shadow-composer → #chat-input-row input 的 box-shadow(唯一消费者);删除 --shadow-overlay / --shadow-menu → .overlay-card 与 #selection-menu 两处 box-shadow 行必须同时移除,否则悬空引用"
    - "删除 --text-sm → 6 个消费者(style.css:332/417/433/614/677/778)必须同批改引 --text-xs,否则 var(--text-sm) 解析为空、字号静默回落到继承值,而四条门禁一条都不会报"
    - "tier-2 语义动作色系(--color-action-danger/warning/routine/commit/irreversible)承担「授权撰写总设计文档」这一不可逆动作的安全信号 → 本次换肤只改底层 --blue-700,五族语义名与绿色族值一律不动"
    - "`#round-doc.round-frozen` 的 inset 3px 0 0 var(--color-action-warning) 是冻结轮的结构标记(S-4),不是影子 → 影子收敛任务必须绕过它"
---

<objective>
把界面信息架构整体对调并照搬 ChatGPT 视觉语言:主区承载会话流(阶段 3+ 为批注流),右侧改为可折叠的文档面板;配色、字号阶梯、圆角、阴影与消息气泡形态换成实测自 chatgpt.com 真实渲染 DOM 的目标规格;DESIGN.md §4.1/§4.2 同批修订。

Purpose: 现状有三处结构性毛病。(1) 信息架构反了——**文档是长文阅读对象,却占了主区;会话流是操作对象,却挤在 420px 侧栏里**。讨论场景下用户的高频动作是"说话 / 处理批注 / 看 AI 在干什么",低频动作是"读文档",而现状把低频动作放在主区、高频动作塞进侧栏。(2) `.chat-bubble` 同时作用于用户与助手消息,助手的长文回答(列表 / 代码 / 多级标题)被塞进带背景的窄盒子——助手回答才是主体内容,非对称内容应当非对称呈现。(3) 令牌层虽已收口成 25 primitive + 50 语义名,但**值**仍是上一轮审计修修补补的产物(6 档字号、三种行高倍数、8 个圆角值、两条影子令牌、17 处描边),没有一套统一的视觉语言。本次是**值层与结构层**的重做,令牌的**名**与三层分类学(除布局令牌改名)一字不动。

Output: 三个前端文件 + 权威文档修订。零后端改动、零新增依赖、零构建步骤。附带一份有意保留的偏差证据:`check-02` 预期 FAIL,其失败清单是用户知情接受的 AA 对比度倒退的机器可查形态。

**用户已拍板的四项决策(锁定,执行期不得重新讨论):**
1. 完整照搬 ChatGPT 视觉语言,**接受 AA 对比度倒退**(次要文字 5.41:1 → 约 3.23:1,低于 WCAG AA 4.5:1)
2. **会话流移到主区**(原侧栏内容整体搬到主区)
3. **文档区变为可折叠的右侧面板**
4. **授权修改 DESIGN.md §4.1 / §4.2**

**绝对禁令(违反即失败):**
- 不得修改 `scripts/check-01..04` 任何门禁脚本
- 不得修改 style.css 中「Contrast pair manifest」注释块里的任何 `/* PAIR ... */` / `/* ORDER ... */` 行——它们存在的意义就是让偏差可见
- `check-02` 必须红着交出去。不得用任何手段让它变绿(包括但不限于:改阈值、删 pair 行、删令牌名让脚本提前 exit、把 rgba 当背景令牌洗掉失败)
- 不得让 `check-02` 以「unknown token」「malformed manifest」「coverage below floor」的方式失败——那会毁掉偏差证据表,失败必须逐条是「对比度低于阈值」
- 不得引入任何依赖、构建步骤、CDN、CSS 框架或图标库

**为什么两个「透明度描边」用不透明等价色而非字面 rgba(必须遵守,不要"改回"规格原文):**
规格给的是 `rgba(0,0,0,.15)`(组件描边)与 `rgba(0,0,0,.05)`(分割线)。但 `check-02` 只对**前景**做 alpha 合成(见 `scripts/check-02-contrast.py` 的 `fg_alpha` 分支),背景令牌的 alpha 会被当成完全不透明的 `rgb(0,0,0)`。若 `--gray-100` 是 `rgba(0,0,0,.05)`,`PAIR --color-text-muted ON --gray-100` 会算出 **6.49 PASS**,而真实合成值是 **2.89 FAIL**——门会把一条本该红的偏差洗白,用户要求保留的偏差信号就没了。改用白底上的不透明等价色:0.85×255+0.15×0 = 216.75 → `#d9d9d9`;0.95×255 = 242.25 → `#f2f2f2`。**在白底上像素完全相同**,而门诚实地红。这是刻意的偏差,记录在 SUMMARY 里。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/STATE.md
@.planning/REQUIREMENTS.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/CLAUDE.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/CLAUDE.md
@DESIGN.md
@frontend/index.html
@frontend/style.css
@frontend/app.js
@scripts/check-01-token-conformance.sh
@scripts/check-02-contrast.py
@scripts/check-03-hidden-uniqueness.sh
@scripts/check-04-important-count.sh

**改动前基线(已实测于 2026-09-18,执行期先复跑确认再动手):**

```
bash scripts/check-01-token-conformance.sh        # PASS
./.venv/bin/python scripts/check-02-contrast.py   # PASS: 0 failures(34 PAIR + 1 ORDER)
bash scripts/check-03-hidden-uniqueness.sh        # PASS
bash scripts/check-04-important-count.sh          # PASS
grep -c 'var(--sidebar-w)'   frontend/style.css   # 1  (仅 #sidebar 的 flex-basis,现 242 行)
grep -c 'right: 448px'       frontend/style.css   # 1  (现 412 行,魔法数)
grep -c 'var(--text-sm)'     frontend/style.css   # 6  (332/417/433/614/677/778)
grep -cE '^\s*box-shadow:'   frontend/style.css   # 3  (376 卡片 / 701 划词菜单 / 725 冻结轮 inset)
grep -c 'max-width: 720px'   frontend/style.css   # 1
grep -c 'var(--doc-panel'    frontend/style.css   # 0
grep -c 'id="main-pane"\|id="doc-panel"' frontend/index.html   # 0
grep -c '/\* PAIR'           frontend/style.css   # 34
grep -c '/\* ORDER'          frontend/style.css   # 1
grep -o '!important;' frontend/style.css | wc -l  # 1
grep -cE '^[[:space:]]*\.hidden[[:space:]]*\{' frontend/style.css  # 1
grep -n '^\.annotation-plain \.annotation-note'   frontend/style.css   # 669
grep -n '^\.annotation-answered \.annotation-note' frontend/style.css  # 852
node --check frontend/app.js                       # 通过
```

**令牌引用完整性门(改动前后都应返回 0;这是"删了 --text-sm 却漏改消费者"的唯一机械防线):**

```bash
awk '/DESIGN TOKENS: START/{f=1;next} /DESIGN TOKENS: END/{f=0} f' frontend/style.css \
  | grep -oE 'var\(--[a-z0-9-]+\)' | sed -E 's/var\(--(.*)\)/\1/' | sort -u > /tmp/u.txt
awk '/DESIGN TOKENS: START/{f=1;next} /DESIGN TOKENS: END/{f=0} f' frontend/style.css \
  | grep -oE '^\s*--[a-z0-9-]+' | sed -E 's/.*--//' | sort -u > /tmp/d.txt
comm -23 /tmp/u.txt /tmp/d.txt | wc -l     # 必须为 0
```

**check-02 的两个非显然事实(决定了本计划的多条约束):**
1. `resolve()` 只对 **manifest 里按名引用的令牌**调用。因此新增的布局令牌 `--doc-panel-w: clamp(360px, 38vw, 620px)` 不会被解析,`clamp()` 不会触发 "unparsable value"。
2. `raw_pairs = fence.count("/* PAIR")` 必须等于正则解析出的条数。因此 fence 内**一条 PAIR/ORDER 都不许增删改**。

**约束(项目 CLAUDE.md §2 简单优先 / §3 外科手术式改动):** 每一行改动都必须能追溯到上面的目标规格之一。不重排格式、不"顺手改进"相邻代码、不删除既存死代码(唯一的例外是本计划显式点名的 `--text-sm` / `--shadow-overlay` / `--shadow-menu` / `--sidebar-w`)、不引入构建步骤、不引入任何依赖。

**必须保持原样的既有结构(五条硬约束):**
1. `/* ===== DESIGN TOKENS: START ===== */` … `/* ===== DESIGN TOKENS: END ===== */` 围栏必须仍**恰好一对**;裸 `#hex` 只能出现在围栏内;tier-1 primitive 名(`--white/--black/--gray-*/--green-*/--blue-*/--amber-*/--red-*/--purple-*`)只能在围栏内被 `var()` 引用,围栏外只准引用 tier-2 名。新配色值必须作为 tier-1 primitive 进围栏,再经 tier-2 语义名暴露给选择器。
2. `.hidden { display: none !important; }` 必须仍**恰好 1 条**;`!important;` 声明必须仍**恰好 1 个**。因此本次新增的任何注释散文里不得出现带分号的 `!important;` 字面量。**折叠态一律用 `#doc-panel.collapsed` 类名,不得复用 `.hidden`。**
3. `--z-badge(10) < --z-banner(20) < --z-overlay(100) < --z-selection-menu(200)` 四条令牌与断言不得改动。注意:徽标改为流内元素后 `--z-badge` 不再有消费者,但**声明必须保留**(四条令牌是一个被注释断言的序关系整体)。
4. 文件末尾的 `.annotation-answered` 规则组(注释写明「绝不插入、绝不重排(Global Hard Rule 3)」)必须保持在 `.annotation-plain .annotation-note` 之后,不得移动、不得插入任何规则到它与其前驱之间。
5. `--color-text-inverse` 与 `--color-surface-info-strong` 两条声明**必须保留**:`.chat-user` 改引 `--color-surface-user` 后它们不再被任何选择器消费,但 check-02 的清单里有 `PAIR --color-text-inverse ON --color-surface-info-strong TEXT` 一条**按名引用**它们——删掉声明会让脚本以 "unknown token" 提前 exit,偏差证据表就没了。两条声明原样保留,并在其上方补一行注释说明"保留是为 CHECK-02 清单的按名引用"(注释里不得出现带分号的 `!important;`)。

**语义动作色系的安全职责(不得被换肤吞掉):** `--color-action-danger/warning/routine/commit/irreversible` 五族的语义名必须全部保留;它们的底层值本次一律不动(green-700 / amber-800 / red-600 原样)。`#btn-authorize`(「授权撰写总设计文档」)是不可逆操作,它的颜色是安全信号——本次唯一被改动的动作色是 `--color-action-primary`(经 `--blue-700` 变成品牌蓝),它服务的是「发送」「同意」「放行」这类可逆操作。

**REQUIREMENTS 与本次用户决策的已知张力(必须如实记录,不得静默):** `TOKEN-08` 写的字号刻度是 `11 / 12 / 13 / 15 / 18 / 22`。用户决策 1 锁定「完整照搬 ChatGPT 视觉语言」,其阶梯是 `12 / 14 / 16 / 18 / 24`。**用户决策优先**;TOKEN-08 的**意图**(把 7 个字号收敛成少量档位、消灭 12.5px 这类分数值)仍然满足(5 档、零分数值)。SUMMARY 里记录这一条为「需求字面值被用户决策覆盖」。

<!-- 本计划的验收断言会反向 grep 下面这些字面量(它们必须从文件里消失或必须出现固定次数),
     而这些字面量本身又必须出现在 <action> 里才说得清要删什么/改什么。按 planner 的
     注释文本纪律,逐条登记为允许出现: -->
<!-- planner-discipline-allow: id="sidebar" -->
<!-- planner-discipline-allow: id="doc-pane" -->
<!-- planner-discipline-allow: var(--sidebar-w) -->
<!-- planner-discipline-allow: right: 448px -->
<!-- planner-discipline-allow: max-width: 720px -->
<!-- planner-discipline-allow: classList.toggle('collapsed') -->
<!-- planner-discipline-allow: 侧栏 -->
</context>

<tasks>

<task type="tracer">
  <name>Task 1: 信息架构对调 —— 会话流入主区、文档区变可折叠右栏(一条端到端切片)</name>
  <files>frontend/index.html, frontend/style.css, frontend/app.js</files>
  <action>
这是本计划的纵向切片:从 HTML 容器结构 → 布局令牌 → CSS 定位 → JS 折叠交互,一路穿到屏幕上"点标题能把文档面板收起来"这条真实可操作路径,证明新信息架构端到端成立。后续 Task 2/3 只在这条已跑通的架构上换视觉的值。

**A. index.html:两个容器整体对调(内部内容逐字搬运,不得顺手改任何子元素的属性或文案)**

把现有的
`<main id="doc-pane"> … </main>` 与 `<aside id="sidebar"> … </aside>`
两个块替换为下面的结构。**四个 section(`#session-panel` / `#annotations-panel` / `#checks-panel` / `#ai-panel`)的内部标记一行都不许改,只换外层容器。** `#enter-form` / `#stream-banner` / `#draft-view` / `#rounds-placeholder` 同理。

新结构:

- `<main id="main-pane">` —— 主区,依次包含四个 section,保持原相对顺序:`#session-panel`、`#annotations-panel`、`#checks-panel`、`#ai-panel`。
- `<aside id="doc-panel">` —— 右侧可折叠文档面板,包含:
  - 面板标题行:`<header class="panel-header" id="doc-panel-header">`,内含 `<h1>文档区</h1>` 与一个右侧容器 `.panel-header-right`,后者含 `<span id="state-badge" class="hidden"></span>` 与 `<span class="collapse-indicator">▾</span>`。
  - `<div id="doc-panel-body">`,依次包含 `#enter-form`、`#stream-banner`、`#draft-view`、`#rounds-placeholder`(原顺序)。
- `#state-badge` **从 `#doc-pane` 的直接子元素移入面板标题行**(这是它从浮层变成流内元素的结构前提,见 D-2)。
- 顶部两行 HTML 注释(现 11 行「左:文档区」、80 行「右:侧栏」)改写为新信息架构的说明;注释里不得出现带分号的 `!important;`。
- **不得触碰**:四个模态(`#permission-modal` / `#confirmation-modal` / `#tier-modal` / `#mission-complete-modal`)、`#selection-menu`、`#cli-check-overlay`、两个 `<script>` 标签及其上方注释(现 214-219 行)。

**B. style.css:布局令牌改名 + 新增收起宽度**

- fence 内 `--sidebar-w: 420px;`(现 114 行)整行改为 `--doc-panel-w: clamp(360px, 38vw, 620px);`,并新增一行 `--doc-panel-w-collapsed: 48px;`。两行上方的注释(现 113 行)改为陈述新用途。
- **理由(必须写进注释)**:`clamp()` 让"主区阅读列够不够宽"退化成**一个令牌**的取值问题——窄屏下面板收窄、主区保住阅读列,宽屏下面板最多 620px。用户已明确这条张力交由用户裁决,执行器不得自行改动这个值(见 `<verification>` 的张力段)。
- 令牌引用完整性:改名后围栏外不得残留任何 `var(--sidebar-w)`。

**C. style.css:两栏布局改写**

- 删除现有 `#doc-pane { … }` 规则(现 233-238 行)与 `#sidebar { … }` 规则(现 241-247 行),替换为:
  - `#main-pane`:占满剩余宽度(`flex: 1 1 auto`),纵向排列、可滚动(`display: flex; flex-direction: column; overflow-y: auto;`),内容列居中(`align-items: center;`)。
  - `#main-pane > section`:内容列宽(`width: 100%; max-width: 768px;`)——这就是用户规格里的「主区内容列 768px」,四块面板同宽同列。
  - `#doc-panel`:固定基准宽(`flex: 0 0 var(--doc-panel-w);`),纵向排列、可滚动,左边一条分隔线(`border-left: 1px solid var(--color-border-subtle);`),白底(`background: var(--color-surface);`)。
  - `#doc-panel.collapsed`:`flex-basis: var(--doc-panel-w-collapsed); overflow: hidden;`(48px 竖条,不出滚动条)。
  - `#doc-panel.collapsed #doc-panel-body`、`#doc-panel.collapsed #doc-panel-header h1`、`#doc-panel.collapsed #state-badge`:三者 `display: none`。
  - `#doc-panel.collapsed #doc-panel-header`:居中(`justify-content: center; padding-inline: 0;`),让折叠指示符落在 48px 竖条正中。
- 新增 `#doc-panel-header h1`:把 `<h1>文档区</h1>` 降级为安静的容器标签(`margin: 0; font-size: var(--text-base); font-weight: var(--fw-semibold); color: var(--color-text-secondary);`)。**必须用 `#doc-panel-header h1` 限定,不得写全局 `h1` 规则**(VISUAL-03)。`--fw-semibold` 是现存的令牌;Task 3 会把它改成 `--fw-medium`。
- 新增 `#doc-panel-body { padding: var(--space-8) var(--space-10); }`——**沿用原 `#doc-pane` 的内边距**,文档面板的呼吸空间不得缩水。注意不要给这个 div 加 `.panel-body` 类(那会套上 12/16px 的紧凑内边距)。

**D. style.css:`#state-badge` 由浮层改为流内元素**

现规则(现 409-420 行)含 `position: fixed; top: 12px; right: 448px;` 与 `z-index: var(--z-badge);`。

- **删除** `position: fixed`、`top`、`right`、`z-index` 四条声明,以及 `right` 那行的魔法数注释。
- **保留** 其余(胶囊圆角、`background: var(--color-surface-info)`、`color: var(--color-text-info)`、字号、字重)。
- **理由(必须写进注释)**:徽标是「当前推导状态」的说明,它属于文档面板的 chrome。改为流内元素一次性闭合两条既有需求——LAYOUT-01(`right: 448px` 魔法数消失,且不再需要 `calc()` 重新制造一个耦合)与 LAYOUT-03(它不再是不透明浮层,不再遮挡从底下穿过的正文)。**不要**改用 `right: calc(var(--doc-panel-w) + …)`:那只是把一个魔法数换成另一个耦合,并且面板收起时该算术立刻失真。

**E. app.js:文档面板折叠处理器**

在现有「面板折叠(点击标题切换)」段落(现 1544-1553 行区段)之后追加一个同形的处理器:

- 新增两个句柄:`#doc-panel` 与 `#doc-panel-header`(沿用文件既有的 `document.getElementById` 写法,句柄声明放在文件顶部句柄区)。
- 点击标题 → `classList.toggle('collapsed')` → 把标题行内 `.collapse-indicator` 的文本在 `'▾'`(展开)与 `'▸'`(收起)之间切换。
- **不要**给 `#ai-panel` 的既有处理器做任何改动(不动它的变量名、不抽公共函数)。重复 5 行好过为一个消费者造一个抽象(项目 CLAUDE.md §2)。
- **为什么加在 app.js 而不是独立脚本(理由必须写进 SUMMARY)**:①既有折叠交互就在 app.js,同形处理器放一起才可审;②新增一个 `<script>` 标签会引入第二个 DOM-ready 时序面,而 index.html 现 215-217 行的注释已经记录了"脚本顺序错一次就让尾部代码全不执行"的既有事故(G-idi01-8);③本仓库零构建步骤,没有打包器把两个文件合成一个。代价是 app.js 增加约 8 行。

**F. 不得触碰**:fence 内的 Contrast pair manifest(34 PAIR + 1 ORDER);`scripts/check-01..04`;`.hidden` 规则;四条 `--z-*` 令牌;`.annotation-answered` 规则组;`#round-doc.round-frozen` 的 inset 标记。
  </action>
  <verify>
    <automated>cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && node --check frontend/app.js && bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh && test "$(grep -c 'id="sidebar"' frontend/index.html)" = 0 && test "$(grep -c 'id="doc-pane"' frontend/index.html)" = 0 && test "$(grep -c 'id="main-pane"' frontend/index.html)" = 1 && test "$(grep -c 'id="doc-panel"' frontend/index.html)" = 1 && test "$(awk '/<main id="main-pane">/{f=1} /<\/main>/{f=0} f' frontend/index.html | grep -cE 'id="(session-panel|annotations-panel|checks-panel|ai-panel)"')" -ge 4 && test "$(awk '/<aside id="doc-panel">/{f=1} /<\/aside>/{f=0} f' frontend/index.html | grep -cE 'id="(enter-form|stream-banner|draft-view|rounds-placeholder|state-badge|round-doc)"')" -ge 6 && test "$(awk '/<aside id="doc-panel">/{f=1} /<\/aside>/{f=0} f' frontend/index.html | grep -c 'id="round-doc"')" = 1 && test "$(grep -n 'id="main-pane"' frontend/index.html | cut -d: -f1)" -lt "$(grep -n 'id="doc-panel"' frontend/index.html | cut -d: -f1)" && test "$(grep -c 'var(--sidebar-w)' frontend/style.css)" = 0 && test "$(grep -c 'var(--doc-panel-w' frontend/style.css)" -ge 2 && test "$(grep -c 'right: 448px' frontend/style.css)" = 0 && test "$(awk '/^#state-badge \{/,/^\}/' frontend/style.css | grep -cE 'position:|z-index:')" = 0 && test "$(grep -c 'doc-panel-header h1' frontend/style.css)" -ge 1 && test "$(grep -c "getElementById('doc-panel" frontend/app.js)" -ge 2 && test "$(grep -c "classList.toggle('collapsed')" frontend/app.js)" -ge 2 && git diff -U0 -- frontend/style.css > /tmp/plan-diff.txt && test "$(grep -cE '^[+-].*/\* (PAIR|ORDER)' /tmp/plan-diff.txt)" = 0 && test "$(awk '/DESIGN TOKENS: START/{f=1;next} /DESIGN TOKENS: END/{f=0} f' frontend/style.css | grep -oE 'var\(--[a-z0-9-]+\)' | sed -E 's/var\(--(.*)\)/\1/' | sort -u > /tmp/u.txt; awk '/DESIGN TOKENS: START/{f=1;next} /DESIGN TOKENS: END/{f=0} f' frontend/style.css | grep -oE '^\s*--[a-z0-9-]+' | sed -E 's/.*--//' | sort -u > /tmp/d.txt; comm -23 /tmp/u.txt /tmp/d.txt | wc -l | tr -d ' ')" = 0 && test "$(git diff --name-only -- frontend scripts)" = "frontend/app.js
frontend/index.html
frontend/style.css" && echo TASK1-STRUCTURE-OK; ./.venv/bin/python scripts/check-02-contrast.py | tail -3; echo "check-02 exit=${PIPESTATUS[0]} (本任务预期仍为 0:配色未动)"</automated>
  </verify>
  <done>
    `node --check frontend/app.js` 通过;check-01 / check-03 / check-04 PASS;`id="sidebar"` 与 `id="doc-pane"` 在 index.html 里归零,`id="main-pane"` / `id="doc-panel"` 各恰 1 个;四个 section 全在 `<main id="main-pane">` 内,`#enter-form` / `#stream-banner` / `#draft-view` / `#rounds-placeholder` / `#state-badge` / `#round-doc` 六个 id 全在 `<aside id="doc-panel">` 内;`#main-pane` 在 `#doc-panel` 之前;`var(--sidebar-w)` 归零、`var(--doc-panel-w` 前缀至少 2 处消费(`--doc-panel-w` 与 `--doc-panel-w-collapsed` 各一);`right: 448px` 归零、`#state-badge` 规则体内无 `position:` / `z-index:`;`#doc-panel-header h1` 规则存在;app.js 有 2 处 `getElementById('doc-panel…')` 与 2 处 `classList.toggle('collapsed')`(既有 AI 面板 + 新文档面板);fence 内 PAIR/ORDER 一行未改;令牌引用完整性门返回 0;`git diff --name-only -- frontend scripts` 恰为三个前端文件;check-02 仍为 0 退出(本任务未改任何颜色值)。
  </done>
</task>

<task type="auto">
  <name>Task 2: 令牌值层换血 —— 配色 + 字号阶梯 + 行高配对 + 字重档 + 圆角刻度 + 影子收敛到一条 + 助手消息去气泡</name>
  <files>frontend/style.css</files>
  <action>
**A. 在 token fence 内改写 tier-1 primitive 的值**(只改值,不改名,不增删既有 tier-1 名):

| tier-1 | 现值 | 目标值 | 依据 |
|---|---|---|---|
| `--gray-900` | `#1a1a1a` | `#0d0d0d` | 主文字 |
| `--gray-700` | `#555555` | `#8f8f8f` | 次要文字 |
| `--gray-600` | `#6a6a6a` | `#8f8f8f` | 次要文字(规格只给一档 #8f8f8f;两个语义角色各自保留,值相同) |
| `--gray-500` | `#8a8a8a` | `#d9d9d9` | 组件描边 rgba(0,0,0,.15) 的白底不透明等价 |
| `--gray-100` | `#eeeeee` | `#f2f2f2` | 分割线 rgba(0,0,0,.05) 的白底不透明等价 |
| `--gray-50` | `#f5f5f5` | `#f3f3f3` | 次级表面 |
| `--gray-25` | `#fafafa` | `#ffffff` | 表面 |
| `--blue-700` | `#1f63bd` | `#3a83f7` | 品牌蓝 |

其余 tier-1(`--white`、`--black`、`--gray-300`、`--blue-100`、`--blue-50`、`--green-*`、`--amber-*`、`--red-*`、`--purple-600`)**一律不动**。`--gray-600` 行上原有的「AA-safe muted grey」注释已不成立(它现在是知情接受的 AA 倒退),改为陈述新事实的注释。

**B. 新增一个 tier-1 primitive**,插在灰阶阶梯的正确位置上(`--gray-300` 与 `--gray-100` 之间,保持"数字越小越浅"的单调性):

| 新增 tier-1 | 值 | 依据 |
|---|---|---|
| `--gray-200` | `#ececec` | 用户气泡 |

**C. 新增一个 tier-2 语义名**(与唯一消费者同提交,Hard Rule 5):

| 新增 tier-2 | 值 |
|---|---|
| `--color-surface-user` | `var(--gray-200)` |

**D. 保留两条"失去消费者"的令牌声明**:`--color-surface-info-strong` 与 `--color-text-inverse` 在 `.chat-user` 改引新令牌后不再被任何选择器消费,但 check-02 的清单**按名引用**它们(见 `<context>` 硬约束 5)。两条声明原样保留,并在它们上方补一行注释说明保留原因。

**E. 字号阶梯:6 档收敛为 5 档(改值 + 删一个名 + 同步 6 个消费者)**

| tier-2 | 现值 | 目标值 | 规格档位 |
|---|---|---|---|
| `--text-xs` | 11px | 12px | 12px/16px 页脚、辅助 |
| `--text-sm` | 12px | **删除** | —(消费者改引 `--text-xs`,值不变,零视觉 delta) |
| `--text-base` | 13px | 14px | 14px/20px 界面 chrome、按钮 |
| `--text-md` | 14px | 16px | 16px/26px 消息正文 |
| `--text-lg` | 15px | 18px | 18px/28px 章节标题 |
| `--text-xl` | 16px | 24px | 24px/32px 大标题 |

删除 `--text-sm` 的声明行,并把 6 个消费者(style.css 现 332 / 417 / 433 / 614 / 677 / 778 行)对该令牌的引用逐处改为 `--text-xs`。**这 6 处必须同批完成**——漏一处,那条已删令牌的引用解析为空、字号静默回落到继承值,而四条门禁一条都不会报。改完后围栏外不得残留任何指向已删令牌的引用(令牌引用完整性门是唯一防线)。

**F. 行高:三种倍数改为四种,与字号配对**

| tier-2 | 现值 | 目标值 | 配对 |
|---|---|---|---|
| `--lh-tight` | 1.35 | 1.3333 | 24/32 与 12/16 |
| `--lh-snug` | (新增) | 1.4286 | 14/20 |
| `--lh-compact` | 1.6 | 1.5556 | 18/28 |
| `--lh-reading` | 1.75 | 1.625 | 16/26 |

**G. 字重:新增 500 档**

| tier-2 | 值 |
|---|---|
| `--fw-medium` | 500 |

(`--fw-regular` 400 / `--fw-semibold` 600 不动。v1.14 Phase 4 曾按 Q4 刻意不声明 500 档,理由是"没有消费者";本次目标阶梯明确要求 chrome 用 w400/500/600,该理由不再成立,故声明。原有那行「the 500 rank is deliberately NOT declared (Q4)」注释必须同批改写,否则注释与本文件互相矛盾。)

**H. 圆角:3 值扩为 4 值**

| tier-2 | 现值 | 目标值 | 用途 |
|---|---|---|---|
| `--radius-sm` | 4px | 8px | 小按钮、chip、行内 code |
| `--radius-md` | 8px | 10px | 导航项、卡片、菜单、批注条目 |
| `--radius-lg` | (新增) | 28px | 输入框(composer);用户气泡 |
| `--radius-pill` | 999px | 999px | 徽标、胶囊按钮 |

**I. 影子收敛为全页唯一一条**

- 删除 tier-2 `--shadow-overlay` 与 `--shadow-menu` 两条声明。
- 同时删除它们的两处消费者(style.css 现 376 行 `.overlay-card`、现 701 行 `#selection-menu`,各有一条指向影子令牌的 box-shadow 声明)——留着就是悬空引用。
- 新增 tier-2 `--shadow-composer`,值恰为三层叠加:`rgba(0, 0, 0, 0.04) 0 0 0 1px, rgba(0, 0, 0, 0.04) 0 2px 8px 0, rgba(0, 0, 0, 0.024) 0 4px 80px 8px`。
- **不得触碰** `#round-doc.round-frozen` 的 `box-shadow: inset 3px 0 0 var(--color-action-warning);`(现 725 行)——它是冻结轮的结构标记(S-4),不是影子,它的存在是为了在不用 opacity 的前提下表达只读。它的上一行注释(现 722 行)同样保留。

**J. 消息气泡非对称化(style.css 现 530-552 行区段)**

- `.chat-user`:背景改引 `var(--color-surface-user)`,前景由 `var(--color-text-inverse)`(白字)改引 `var(--color-text)`(深字);`align-self: flex-end` 与右下角小圆角保持不变。
- `.chat-ai`:规则体只保留 `align-self: flex-start;` 一条声明。`.chat-bubble` 保留的 `padding` / `border-radius` / `max-width` 仍服务用户侧气泡,因此助手侧必须在 `.chat-ai` 里显式给出 `background: none`、`padding: 0`、`border-radius: 0`、`max-width: 100%`——四者缺一都会让助手消息继续带着盒子。`.chat-ai` 必须留在 `.chat-bubble` **之后**(同特异性 0-1-0,靠源码顺序取胜;不得把 `.chat-ai` 移到 `.chat-bubble` 之前)。
- `.chat-ai.streaming-ai` 的左侧流式竖线(3px `--color-border-streaming`)保留不动——它是"正在流式"的状态信号,不是气泡语义。
- `.chat-ai p` / `.say-chunk p` 的段间距保留。

**K. 新增令牌的消费者在 Task 3 落地(不得因此删声明)**

`--fw-medium`、`--radius-lg`、`--lh-snug`、`--shadow-composer` 四条在本任务声明,消费者全部在 Task 3(同一计划的下一个任务)落地。**不得**因为"暂时没有消费者"而把任何一条删掉或推迟声明——令牌值层一次性收口,消费端在同批交付内跟上。令牌引用完整性门只校验"围栏外引用的都声明了",不会因为暂时无人引用而失败,因此本任务的门禁结果无法替这条把关:**执行期必须确认 Task 3 已把这四条各自接上一个真实消费者**(`--lh-snug` → `.hint` 的 `line-height`,见 Task 3 A 段)。

**L. 不得触碰**:fence 内的 PAIR/ORDER 注释块;`scripts/check-01..04`;`.hidden`;四条 `--z-*`;`.annotation-answered` 规则组;`#round-doc.round-frozen` 的 inset 标记;Task 1 建立的容器与布局规则。
  </action>
  <verify>
    <automated>cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh && test "$(grep -c 'var(--text-sm)' frontend/style.css)" = 0 && test "$(grep -cE '^\s*--text-sm:' frontend/style.css)" = 0 && test "$(grep -c 'var(--shadow-overlay)\|var(--shadow-menu)' frontend/style.css)" = 0 && test "$(grep -cE '^\s*--shadow-(overlay|menu):' frontend/style.css)" = 0 && test "$(grep -cE '^\s*box-shadow:' frontend/style.css)" = 1 && test "$(grep -c 'inset 3px 0 0 var(--color-action-warning)' frontend/style.css)" = 1 && test "$(grep -c 'var(--text-xs)' frontend/style.css)" -ge 7 && test "$(grep -c 'var(--gray-200)' frontend/style.css)" -ge 1 && test "$(grep -c 'var(--color-surface-user)' frontend/style.css)" -ge 1 && test "$(grep -cE '^\s*--fw-medium:' frontend/style.css)" = 1 && test "$(grep -cE '^\s*--radius-lg:' frontend/style.css)" = 1 && test "$(grep -cE '^\s*--lh-snug:' frontend/style.css)" = 1 && test "$(grep -cE '^\s*--shadow-composer:' frontend/style.css)" = 1 && test "$(awk '/^\.chat-ai \{/,/^\}/' frontend/style.css | grep -oE '(background|padding|max-width|border-radius):' | wc -l | tr -d ' ')" -ge 4 && test "$(awk '/^\.chat-ai \{/,/^\}/' frontend/style.css | grep -c 'align-self: flex-start')" = 1 && test "$(grep -n '^\.chat-bubble {' frontend/style.css | cut -d: -f1)" -lt "$(grep -n '^\.chat-ai {' frontend/style.css | cut -d: -f1)" && git diff -U0 -- frontend/style.css > /tmp/plan-diff.txt && test "$(grep -cE '^[+-].*/\* (PAIR|ORDER)' /tmp/plan-diff.txt)" = 0 && test "$(awk '/DESIGN TOKENS: START/{f=1;next} /DESIGN TOKENS: END/{f=0} f' frontend/style.css | grep -oE 'var\(--[a-z0-9-]+\)' | sed -E 's/var\(--(.*)\)/\1/' | sort -u > /tmp/u.txt; awk '/DESIGN TOKENS: START/{f=1;next} /DESIGN TOKENS: END/{f=0} f' frontend/style.css | grep -oE '^\s*--[a-z0-9-]+' | sed -E 's/.*--//' | sort -u > /tmp/d.txt; comm -23 /tmp/u.txt /tmp/d.txt | wc -l | tr -d ' ')" = 0 && test "$(git diff --name-only -- frontend scripts)" = "frontend/style.css" && echo TASK2-STRUCTURE-OK; ./.venv/bin/python scripts/check-02-contrast.py > /tmp/check02-after.txt 2>&1; echo "check-02 exit=$? (本任务起预期非 0)"; grep -c '^FAIL ' /tmp/check02-after.txt; grep -cE 'unknown token|malformed|coverage below floor|unparsable' /tmp/check02-after.txt</automated>
  </verify>
  <done>
    check-01 / check-03 / check-04 PASS;`--text-sm` 的声明与 6 处引用全部消失,`--text-xs` 引用数 ≥7(6 处迁移 + 原 `.annotation-badge`);`--shadow-overlay` / `--shadow-menu` 的声明与两处消费者全部消失,`box-shadow:` 声明全文件恰 1 条(只剩冻结轮的 inset 结构标记——输入框那条影子在 Task 3 接上);冻结轮 inset 标记 1 条未动;`--fw-medium` / `--radius-lg` / `--lh-snug` / `--shadow-composer` 各恰 1 条声明;`.chat-ai` 规则体含 ≥4 条覆盖声明且 `align-self: flex-start` 恰 1 条,`.chat-ai` 在 `.chat-bubble` 之后;fence 内 34 条 PAIR 未改;令牌引用完整性门返回 0;`git diff --name-only -- frontend scripts` 只有 `frontend/style.css`;check-02 非 0 退出,`/tmp/check02-after.txt` 里 `unknown token|malformed|coverage below floor|unparsable` 命中数为 0。
  </done>
</task>

<task type="auto">
  <name>Task 3: 消费端落位 —— 排版作用域 + 导航项/输入框几何 + 减描边 + 内容列 768</name>
  <files>frontend/style.css</files>
  <action>
**A. 排版作用域(TYPE-01 / VISUAL-03)**

- `.markdown-body h1 / h2 / h3` 获得**显式**字号且**作用域限定在 `.markdown-body` 内**:h1 → `--text-xl`(24px)、h2 → `--text-lg`(18px)、h3 → `--text-md`(16px),三级一律 `--fw-semibold`。**不得**写成全局 `h1, h2, h3` 规则——那会与四处 chrome 覆盖碰撞(`.panel-header h2`、`#draft-view h2`、`#brainstorm-view h2`、`.overlay-card h3`)。
- `#doc-panel-header h1` 的字重由 `--fw-semibold` 改 `--fw-medium`(Task 1 建立的那条规则;导航项 14px w500)。
- `.panel-header h2` 改 `--text-base` + `--fw-medium`(覆盖 `--text-md` 变成 16px 的连带效应)。
- `.overlay-card h3` 用 `--text-xl`(24px),`.overlay-card p` 用 `--text-md`(16px)+ `--lh-compact`。
- `.chat-bubble` 的字号由 `--text-base` 改引 `--text-md`(16px),行高改引 `--lh-reading`(1.625)——即规格的 16/26 消息正文。
- `button` 基础规则补 `font-weight: var(--fw-medium)`。
- `.hint` 补 `line-height: var(--lh-snug)`(14/20)——这是 Task 2 新增的 `--lh-snug` 的**唯一消费者**;`.hint` 是多行散文,正是这一档行高服务的对象。漏掉它,`--lh-snug` 就是一条声明了却无人使用的令牌(令牌引用完整性门只查反方向,不会报)。
- `.markdown-body` 的正文行高已是 `--lh-reading`(值经 Task 2 变为 1.625,无需改动);`.markdown-body code` 与 `th/td` 继续用 `--text-base`(14px),在正文 16px 之下形成"正文 > 表格/代码"的既定层级(TYPE-02 的刻度归位)。
- `.annotation-badge` 保持 `--text-xs`(12px);`.tier-desc` 由 `--text-sm` 改 `--text-xs` 后值不变(仍 12px),其 `opacity: 0.9` **不得改动**(它是 Phase 4 刚修过 AA 的敏感点,不在本次范围)。
- 用户气泡的圆角改为 `--radius-lg`(28px):在 `.chat-user` 规则里、`border-bottom-right-radius: var(--radius-sm)` **之前**加一行 `border-radius: var(--radius-lg);`——右下角仍保留 `--radius-sm` 的小圆角作为"尾巴"(长手写法必须在简写之后才生效)。

**B. 导航项几何(四个 `.panel-header` + 文档面板标题行共用同一条规则)**

- `height: 36px`;`padding: var(--space-1-5) var(--space-2-5)`(6px 10px);`border-radius: var(--radius-md)`(10px)。
- **删除**下边界那条 1px hairline 与 sunken 背景色(减描边的核心动作:面板不再靠分隔线与色块区分,改靠 36px 的行高节奏与主区的段间距)。
- `.collapse-indicator { font-size: 20px; line-height: 1; }`(现无任何规则,图标因此以正文字号呈现)。
- 各 `.panel-header` 的 `cursor` 声明保持原样(`#ai-panel-header` 与 `#doc-panel-header` 可折叠故为 pointer,其余为 default)。
- **不加 hover 态**——三个不可点的面板头若有 hover 会给出错误的可点暗示(INTERACT-01 不在本计划范围)。

**C. 主区段间距替代被删的分隔线**

- `#main-pane` 加 `gap: var(--space-1-5)`(6px)——这是被删掉的三条 hairline 的替代物。
- 删除 `#annotations-panel` 与 `#checks-panel` 的上边界 1px hairline(它们与 `#session-panel` 的分隔已由 `#main-pane` 的 6px gap 承担)。
- `.panel-body { padding: var(--space-2-5); }`(10px,与导航项的水平内缩对齐)。

**D. 输入框(composer):28px 圆角 + 52px 高 + 全页唯一的影子**

- `#chat-input-row input`:新增 `min-height: 52px;`、`border-radius: var(--radius-lg);`、`box-shadow: var(--shadow-composer);`;内边距改 `var(--space-1-5) var(--space-2-5)`;字号 `--text-md`(16px,与消息正文同级)。
- `#chat-input-row button`:圆角改 `--radius-pill`(999px 胶囊),字号 `--text-base`,字重 `--fw-medium`。
- **规格里"输入框 768×52"的 768 现在成立,理由必须写进 SUMMARY**:768 是主区内容列宽度(`#main-pane > section` 的 `max-width`),composer 落在这一列内、输入框以 `flex: 1` 吃掉按钮与间隙之外的余量,高度 52 / 圆角 28 / 三层影子被照搬。内边距规格给的是 7px,本计划用 `--space-1-5`(6px)——间距刻度是 4px 基准,写 7px 会引入刻度外的裸字面量;这 1px 是刻意的刻度吸附。

**E. 内容列 768px**

- `.markdown-body` 的 `max-width: 720px;`(现 446 行)→ `max-width: 768px;`。**保持左对齐,不要 `margin-inline: auto`**——同一容器里的其它子元素(进入表单、认可按钮行、发散产物区)不在 `.markdown-body` 内,只给 markdown 列居中会让同一窗格里的内容左右不齐。
- 说明:在文档面板内该 `max-width` 通常不生效(面板比它窄,元素自然取 100%);它真正生效的地方是主区里那些同为 `.markdown-body` 的块(`#latest-check`、`#brainstorm-content`)。这是"一个阅读尺度令牌、两处自然生效",不是死规则。

**F. 减描边(其余站点)**

- `.event-list`、`#latest-check`、`.annotation-item`、`.verdict-card`、`#brainstorm-view`、`#selection-menu` 的描边保留(它们是内容容器,不是分段线);其值经 Task 2 后自动变为新的 hairline / 组件描边值,无需逐条改。
- `.overlay-card` 的阴影已在 Task 2 删除;它的 `border-radius` 经 `--radius-md` 自动变为 10px。模态卡片在深色遮罩(`--color-overlay-backdrop`)上仍有边界,不必补边框。

**G. 不得触碰**:fence 内的 PAIR/ORDER 注释块;`scripts/check-01..04`;`.hidden`;四条 `--z-*`;`.annotation-answered` 规则组;`#round-doc.round-frozen` 的 inset 标记;Task 1 的容器结构与折叠规则;Task 2 的令牌值。
  </action>
  <verify>
    <automated>cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && node --check frontend/app.js && bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh && test "$(grep -c 'max-width: 768px' frontend/style.css)" = 1 && test "$(grep -c 'max-width: 720px' frontend/style.css)" = 0 && test "$(awk '/^\.panel-header \{/,/^\}/' frontend/style.css | grep -c 'height: 36px')" = 1 && test "$(awk '/^\.panel-header \{/,/^\}/' frontend/style.css | grep -cE '^\s*(border-bottom|background):')" = 0 && test "$(grep -c 'border-top: 1px solid var(--color-border-subtle)' frontend/style.css)" = 0 && test "$(grep -cE '^\s*box-shadow: var\(--shadow-composer\)' frontend/style.css)" = 1 && test "$(grep -c 'min-height: 52px' frontend/style.css)" = 1 && test "$(grep -c 'line-height: var(--lh-snug)' frontend/style.css)" = 1 && test "$(grep -c 'var(--fw-medium)' frontend/style.css)" -ge 3 && test "$(grep -c 'border-radius: var(--radius-lg)' frontend/style.css)" -ge 2 && test "$(awk '/^\.chat-user \{/,/^\}/' frontend/style.css | grep -c 'border-radius: var(--radius-lg)')" = 1 && test "$(awk '/^\.markdown-body h1, \.markdown-body h2, \.markdown-body h3/,/^\}/' frontend/style.css | grep -c 'font-size:')" -ge 3 && test "$(grep -cE '^\s*h1, h2, h3' frontend/style.css)" = 0 && test "$(grep -c 'gap: var(--space-1-5)' frontend/style.css)" -ge 1 && test "$(grep -n '^\.chat-bubble {' frontend/style.css | cut -d: -f1)" -lt "$(grep -n '^\.chat-ai {' frontend/style.css | cut -d: -f1)" && test "$(grep -n '^\.annotation-plain \.annotation-note' frontend/style.css | cut -d: -f1)" -lt "$(grep -n '^\.annotation-answered \.annotation-note' frontend/style.css | cut -d: -f1)" && git diff -U0 -- frontend/style.css > /tmp/plan-diff.txt && test "$(grep -cE '^[+-].*/\* (PAIR|ORDER)' /tmp/plan-diff.txt)" = 0 && test "$(awk '/DESIGN TOKENS: START/{f=1;next} /DESIGN TOKENS: END/{f=0} f' frontend/style.css | grep -oE 'var\(--[a-z0-9-]+\)' | sed -E 's/var\(--(.*)\)/\1/' | sort -u > /tmp/u.txt; awk '/DESIGN TOKENS: START/{f=1;next} /DESIGN TOKENS: END/{f=0} f' frontend/style.css | grep -oE '^\s*--[a-z0-9-]+' | sed -E 's/.*--//' | sort -u > /tmp/d.txt; comm -23 /tmp/u.txt /tmp/d.txt | wc -l | tr -d ' ')" = 0 && test "$(git diff --name-only -- frontend scripts)" = "frontend/style.css" && echo TASK3-STRUCTURE-OK; ./.venv/bin/python scripts/check-02-contrast.py > /tmp/check02-after.txt 2>&1; echo "check-02 exit=$? (预期非 0)"; echo "FAIL 行数: $(grep -c '^FAIL ' /tmp/check02-after.txt)"; echo "提前退出形态命中: $(grep -cE 'unknown token|malformed|coverage below floor|unparsable' /tmp/check02-after.txt)"</automated>
  </verify>
  <done>
    check-01 / check-03 / check-04 PASS;`max-width: 768px` 恰 1 处、`720px` 归零;`.panel-header` 规则体含 `height: 36px` 且无 `border-bottom` / `background`;`border-top: 1px solid var(--color-border-subtle)` 归零;`box-shadow: var(--shadow-composer)` 恰 1 处、`min-height: 52px` 恰 1 处;`line-height: var(--lh-snug)` 恰 1 处(`--lh-snug` 的唯一消费者);`var(--fw-medium)` ≥3 处消费(`--fw-medium` / `--radius-lg` / `--lh-snug` / `--shadow-composer` 四条 Task 2 新增令牌在本任务全部接上消费者);`border-radius: var(--radius-lg)` ≥2 处且 `.chat-user` 内恰 1 处;`.markdown-body h1/h2/h3` 组含 3 条 font-size 且无全局 `h1, h2, h3` 规则;`.chat-bubble` 仍在 `.chat-ai` 之前;`.annotation-plain .annotation-note` 的行号仍小于 `.annotation-answered .annotation-note`;fence 内 34 条 PAIR 未改;令牌引用完整性门返回 0;`git diff --name-only -- frontend scripts` 只有 `frontend/style.css`;check-02 非 0 退出,`/tmp/check02-after.txt` 里提前退出形态命中数为 0。
  </done>
</task>

<task type="auto">
  <name>Task 4: DESIGN.md §4.1/§4.2 修订(与代码同批)+ 全量门禁取证 + SUMMARY</name>
  <files>DESIGN.md, .claude/CLAUDE.md, .planning/quick/260918-qrq-frontend-chatgpt/260918-qrq-SUMMARY.md</files>
  <action>
**A. DESIGN.md §4.1 布局段改写(现 102-116 行)**

保留 `### 4.1 布局` 标题与其末尾的决策追溯行 `(D-08, D-10, D-11;划词批注为必开发功能 D-02,排期独立于为本项目自举服务)`。把代码块里的 ASCII 图换成新信息架构,并在图后补三条行为说明:

- 新图:左 = 主区(自适应宽度,内容列 768px 居中),右 = 文档面板(可折叠)。主区内标注「会话流 / 本轮批注流 + 自检报告 / AI 工作面板(直播)」;文档面板内标注「正文 · 划词→弹菜单 · 高亮 = 有批注」「draft.md / discuss-round-N.md」,标题行标注折叠控件。
- 说明 1(职责与阶段映射):主区承载**操作对象**(阶段 1-2 = 会话流;阶段 3+ = 批注流 + 自检报告;AI 工作面板全程在主区);文档面板承载**阅读对象**(阶段 1-2 = 草稿 `draft.md`;阶段 3+ = 轮次文档)。
- 说明 2(折叠行为):点文档面板标题收起为 48px 竖条,再点展开;折叠态只存在于当前页面会话,不落盘。
- 说明 3(状态徽标):当前推导状态徽标随文档面板同排,不是浮层——因此不遮挡正文,也不依赖面板宽度的算术。

**措辞要求**:DESIGN.md 是行为层设计文档,不要写 CSS 类名、令牌名或选择器;用「主区」「文档面板」这两个词统一指代(不得再用「侧栏」指代任何一侧)。

**B. DESIGN.md §4.2 划词批注交互段改写(现 118-123 行)**

- 第 1、2 条(划词 → 小菜单 →「批注」/「用大白话讲这段」;批注与被选原文绑定存档、已解决批注变灰但不删除)**不改**——交互本身没变,变的只是它所在的容器位置。
- 第 3 条:`每轮侧栏显式"本轮批注未处理数"` → `每轮在主区批注流标题处显式"本轮批注未处理数"`。其余(全部被回应后本轮随下一轮文档产生自动冻结、无单独"标记结束"操作、指回 §4.4)不动。
- 第 4 条:`阶段 1-2 时,文档区显示会话产出的草稿(draft.md)、侧栏为对话流` → `阶段 1-2 时,主区为对话流,文档面板显示会话产出的草稿(draft.md)`;`进入轮次后切换为轮次文档 + 批注流` → `进入轮次后切换为主区批注流 + 文档面板的轮次文档`。括号内关于 `docs/transcript.md` 的恢复依据说明逐字保留。
- 检查 §4.2 全段:`侧栏` 一词必须归零。

**C. DESIGN.md 版本行推进(现第 4 行)**

`> 版本:v1.13(收口版)。…` → `> 版本:v1.14(界面信息架构改版)。…`,并在句末追加一段变更说明:`v1.14 按用户裁决修订 §4.1/§4.2:会话流移入主区、文档区改为可折叠的右侧面板;同时照搬 ChatGPT 视觉语言,次要文字对比度由 5.41:1 降至约 3.23:1(低于 WCAG AA 4.5:1)——这是用户在看过实测数字后知情接受的倒退,偏差由 `scripts/check-02-contrast.py` 机器留证。`

**D. `.claude/CLAUDE.md` 的版本引用同步(一行)**

该文件的 Project 段落写着「唯一权威设计文档为项目根 `DESIGN.md`(v1.13 收口版)」。把 `v1.13 收口版` 改为 `v1.14 界面信息架构改版`,其余一字不动。

**若该写入被权限系统拒绝**:不要跳过、也不要改写该文件的其他内容——在 SUMMARY 的「待用户处理」段落记下这一条未完成的同步(文件路径 + 需要改的那一行原文与新文),然后继续。静默跳过是禁止的。

**E. 全量门禁与偏差取证(本任务的核心交付物)**

依次跑四条门禁并**原样抄录** check-02 的完整输出:

1. `bash scripts/check-01-token-conformance.sh` → 必须 PASS
2. `bash scripts/check-03-hidden-uniqueness.sh` → 必须 PASS
3. `bash scripts/check-04-important-count.sh` → 必须 PASS
4. `./.venv/bin/python scripts/check-02-contrast.py` → **必须 FAIL**。用 `./.venv/bin/python`(项目 venv),**不得**用 bash 调用它、也不得用环境 `python3`(环境 python3 是 miniconda,会给出与项目 venv 不同的结果)。把完整输出重定向到 `/tmp/check02-final.txt` 留档。

再跑一遍令牌引用完整性门(见 `<context>`)确认返回 0;跑 `./.venv/bin/python -m pytest backend/tests -q` 确认后端回归基线不变(REG-03;前端三文件不影响后端,这条是"没碰坏别处"的证据)。

**F. SUMMARY.md 必须包含的五块内容**

1. **改动清单**:五个文件的改动摘要(前端三文件 + DESIGN.md + .claude/CLAUDE.md),以及 `git diff --name-only -- frontend DESIGN.md .claude/CLAUDE.md` 的输出。
2. **check-02 偏差证据表**:逐条列出每个 FAIL 行(令牌对名、实测 ratio、阈值),并标注**哪些对应真实渲染、哪些是清单陈旧**。预期形态(执行器必须用 `/tmp/check02-final.txt` 的**实际输出**替换这张预测,不得直接抄):次要文字四对(muted ON gray-25 / white / gray-50 / gray-100)与 secondary 两对(ON gray-25 / amber-25)、结果 chip 与说话 chip 的前景(`--color-kind-fg` ON `--color-kind-default` / `--color-kind-say`)、品牌蓝前景两对(`--color-action-primary-fg` ON `--color-action-primary` 及其 @0.9)、`--color-text-info` ON `--color-surface-info`、组件描边两对(`--color-border-strong` ON `--white` / `--gray-50`)——这些都对应真实渲染。**`PAIR --color-text-inverse ON --color-surface-info-strong` 是清单陈旧项**:它的消费者 `.chat-user` 已改引 `--color-surface-user` 与 `--color-text`,这一条 FAIL 不对应任何屏上像素,它之所以还在清单里是因为清单按名引用令牌(见 `<context>` 硬约束 5)。同时记录失败条目总数与 check-02 退出码。
3. **三条刻意偏差**:① 两个"透明度描边"用白底不透明等价色(理由:check-02 不对背景令牌做 alpha 合成,字面 rgba 会造出 6.49 的假 PASS);② 输入框内边距 7px 吸附为 `--space-1-5`(6px);③ `--gray-600` 与 `--gray-700` 同值 #8f8f8f(规格只给一档次要文字色,两个语义角色各自保留)。另记 `TOKEN-08` 的字面刻度被用户决策 1 覆盖。
4. **人工验收清单**(见 `<verification>`,12 条)写入 SUMMARY 并**逐条标注 `pending`**——前端无自动化覆盖(Nyquist 缺口),未逐条跑过之前不得声称任何视觉结论成立。
5. **已知设计张力**(原文照录,交由用户裁决):主区宽度 = 视口宽度 − 文档面板宽度,而助手消息去气泡后的可用宽度就是主区宽度。本次把这条张力收敛到**一个令牌** `--doc-panel-w: clamp(360px, 38vw, 620px)`;在 1440px 视口下面板约 547px、主区约 893px,768px 阅读列有富余;在 1152px 视口下面板约 438px、主区约 714px,阅读列开始被压。若人工验收判定阅读列不可接受,**唯一的一值回退就是改这个令牌**(例如改成固定 `420px` 或把 clamp 上限降到 480px),不需要任何结构性返工。执行器不得自行改宽度。

**G. 不得触碰**:`scripts/check-01..04`;`.planning/ROADMAP.md`(本次不动路线图;ROADMAP Phase 6/7 计划里引用 `#sidebar` / `#doc-pane` 的旧选择器已因本次信息架构对调而失效,这一条只在 SUMMARY 的「待用户处理」段落记录,不在本计划修复)。
  </action>
  <verify>
    <automated>cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && node --check frontend/app.js && bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh && test "$(grep -c '侧栏' DESIGN.md)" = 0 && test "$(grep -c 'v1.14' DESIGN.md)" -ge 1 && test "$(grep -c '文档面板' DESIGN.md)" -ge 3 && test "$(grep -c '主区' DESIGN.md)" -ge 3 && test "$(grep -c 'v1.14' .claude/CLAUDE.md)" = 1 && test -f .planning/quick/260918-qrq-frontend-chatgpt/260918-qrq-SUMMARY.md && test "$(grep -c 'pending' .planning/quick/260918-qrq-frontend-chatgpt/260918-qrq-SUMMARY.md)" -ge 10 && test "$(awk '/DESIGN TOKENS: START/{f=1;next} /DESIGN TOKENS: END/{f=0} f' frontend/style.css | grep -oE 'var\(--[a-z0-9-]+\)' | sed -E 's/var\(--(.*)\)/\1/' | sort -u > /tmp/u.txt; awk '/DESIGN TOKENS: START/{f=1;next} /DESIGN TOKENS: END/{f=0} f' frontend/style.css | grep -oE '^\s*--[a-z0-9-]+' | sed -E 's/.*--//' | sort -u > /tmp/d.txt; comm -23 /tmp/u.txt /tmp/d.txt | wc -l | tr -d ' ')" = 0 && FILES=$(git diff --name-only -- frontend DESIGN.md .claude/CLAUDE.md) && test "$FILES" = "$(printf '.claude/CLAUDE.md\nDESIGN.md\nfrontend/app.js\nfrontend/index.html\nfrontend/style.css')" && echo TASK4-STRUCTURE-OK; ./.venv/bin/python scripts/check-02-contrast.py > /tmp/check02-final.txt 2>&1; echo "check-02 exit=$? (预期非 0)"; echo "FAIL 行数: $(grep -c '^FAIL ' /tmp/check02-final.txt)"; echo "提前退出形态命中: $(grep -cE 'unknown token|malformed|coverage below floor|unparsable' /tmp/check02-final.txt)"; echo "--- check-02 原样输出 ---"; cat /tmp/check02-final.txt; echo "--- pytest 回归 ---"; ./.venv/bin/python -m pytest backend/tests -q 2>&1 | tail -5</automated>
  </verify>
  <done>
    check-01 / check-03 / check-04 PASS;`node --check frontend/app.js` 通过;DESIGN.md 中 `侧栏` 归零、`主区` 与 `文档面板` 各 ≥3 处、版本行含 v1.14;`.claude/CLAUDE.md` 版本引用为 v1.14(或被权限拒绝时已在 SUMMARY 记录待办);SUMMARY.md 存在且人工验收清单 ≥10 条 `pending` 标注;令牌引用完整性门返回 0;`git diff --name-only -- frontend DESIGN.md .claude/CLAUDE.md` 恰为五个预期文件(注意不能用裸 `git diff --name-only`——工作树里另有 `.claude/settings.local.json` 与 `.planning/state.json` 的既存改动);check-02 非 0 退出,`/tmp/check02-final.txt` 里的 FAIL 行全部是「对比度低于阈值」形态,提前退出形态命中数为 0,完整输出与失败条目数已原样抄进 SUMMARY;pytest 回归与改动前基线一致(219 passed / 6 skipped)。
  </done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 无(网络 / 用户输入) | 本计划是静态标记与样式改写 + 一个本地折叠交互:无网络请求、无新增端点、无新增依赖、无用户输入进入样式层。所有新增值都是围栏内的字面量常量。 |
| 语义色 → 用户对"不可逆操作"的判断 | `--color-action-irreversible` 是「授权撰写总设计文档」这一不可逆动作的安全信号;换肤若把它做成与可逆动作同色,等于移除一道人工防线。 |
| 容器 id 改名 → JS 的 DOM 契约 | `#sidebar` / `#doc-pane` 改名 + 内容整体搬动,是本次唯一可能"页面看起来正常但 JS 静默失效"的改动面(所有句柄走 `getElementById`,失败形态是 `null` 而不是布局错乱)。 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-260918-01 | Tampering | `--color-action-irreversible*` / `#btn-authorize`(style.css 现 734-741 行) | medium | mitigate | 五族语义动作名(`danger`/`warning`/`routine`/`commit`/`irreversible`)全部保留且底层值一律不动;本次唯一改动的动作色是 `--color-action-primary`(经 `--blue-700`),它只服务可逆操作。人工验收清单第 9 条专门回归此点。 |
| T-260918-02 | Tampering | `--color-text-muted` / `--color-text-secondary`(次要文字) | low | accept | 次要文字对比度由约 5.41:1 降到约 3.23:1,低于 WCAG AA 4.5:1。这是**用户知情决策**:实测数字已呈上,用户选择完整照搬 ChatGPT 视觉语言。偏差由 check-02 的 FAIL 输出机器化留证,不静默。 |
| T-260918-03 | Denial of service | 容器对调后 JS 句柄失效(app.js 顶层 `getElementById`) | medium | mitigate | ①两个被改名的容器 id 在 app.js 里**零引用**(已 grep 证实),搬动的是容器而非句柄目标;②Task 1 的 automated 断言逐条核对"六个 id 落在正确的容器内"与"`#round-doc` 在文档面板内";③`node --check` 只保证语法,因此人工验收清单第 5 条把「在文档面板里划词仍弹出批注菜单」列为本次搬动最关键的回归点,并要求在本地起服务后用真实浏览器确认。 |
| T-260918-04 | Tampering | `#round-doc.round-frozen` 的 inset 结构标记(S-4) | low | mitigate | 影子收敛任务(Task 2)显式点名它是结构标记不是影子;每个任务的 automated 断言都含 `grep -c 'inset 3px 0 0 var(--color-action-warning)' = 1`;人工验收清单第 10 条回归。 |
| T-260918-05 | Information disclosure | 本次 diff 全为前端标记/样式/一行设计文档措辞 | low | accept | 无凭据、无端点、无用户数据进入样式层;无新增网络面。 |
| T-260918-SC | Tampering | 依赖安装(npm / pip / cargo) | high | mitigate | **本计划不安装任何依赖**:零新增包、零构建步骤、零 CDN、零图标库。若执行期出现"顺手引入一个 CSS 框架/图标库"的念头,即为违反本计划,立即停止。 |
</threat_model>

<verification>
**每个任务结束时必须提交(不是可选)**:本计划三条 `git diff --name-only -- frontend scripts` 断言都读的是"工作树 vs HEAD"的差异,只有 Task 1-3 各自提交一次,Task 3 的断言才会是 `frontend/style.css` 单文件。提交信息按 `fix(260918-qrq): <任务摘要>` 的形式(项目仓库 CLAUDE.md 第 5 条纪律)。

**四门(逐任务跑,Task 4 为最终收口):**

```bash
bash scripts/check-01-token-conformance.sh         # PASS —— 围栏外零裸 hex、零 tier-1 泄漏
bash scripts/check-03-hidden-uniqueness.sh         # PASS —— .hidden 规则恰 1 条
bash scripts/check-04-important-count.sh           # PASS —— !important; 声明恰 1 个
./.venv/bin/python scripts/check-02-contrast.py    # FAIL(预期)—— 必须用项目 venv 解释器
```

**check-02 的失败方向必须被"证明"而不是被"假设":** 失败行全部是 `FAIL  <ratio>  <pair>  (need >= <threshold>)` 形态;`unknown token` / `malformed manifest entry` / `coverage ... below floor` / `unparsable value` 四种提前退出形态命中数必须为 0。若出现后四种,说明令牌名被删、清单被改、或 fence 内出现了 check-02 无法解析的值,偏差证据表已失效,必须回退到"只改值、不删被清单按名引用的令牌名"。

**结构性断言(见各 task 的 `<automated>`):**

- 围栏恰一对 START/END;`/* PAIR` = 34、`/* ORDER` = 1(与改动前逐字一致)
- 令牌引用完整性:围栏外引用的每个 `var(--x)` 都在围栏内有 `--x:` 声明(返回 0)
- `--text-sm` 的声明与引用全文件为 0;`--text-xs` 引用 ≥7
- `box-shadow:` 声明全文件恰 2 条(输入框影子 + 冻结轮 inset);冻结轮 `inset 3px 0 0 var(--color-action-warning)` 恰 1 条
- `id="sidebar"` / `id="doc-pane"` 归零;`id="main-pane"` / `id="doc-panel"` 各恰 1 个;`#main-pane` 在 `#doc-panel` 之前;六个内容 id 落在正确容器内
- `var(--sidebar-w)` 归零;`var(--doc-panel-w)` ≥2 处;`right: 448px` 归零;`#state-badge` 规则体内无 `position:` / `z-index:`
- `max-width: 768px` 恰 1 处、`720px` 归零;`min-height: 52px` 恰 1 处
- `.annotation-answered .annotation-note` 的行号 > `.annotation-plain .annotation-note` 的行号(源码顺序承重,改动前 852 > 669);`.chat-bubble` 的行号 < `.chat-ai` 的行号
- `git diff --name-only -- frontend scripts` 在 Task 1-3 输出恰为当前任务涉及的前端文件;Task 4 用 `git diff --name-only -- frontend DESIGN.md .claude/CLAUDE.md` 输出恰为五个文件(注意不能用裸 `git diff --name-only`——工作树里另有 `.claude/settings.local.json` 与 `.planning/state.json` 的既存改动,裸命令会污染这条断言)

**门算术陷阱(不得简化):** `grep -c 'box-shadow' frontend/style.css` 会命中一行**注释散文**(现 722 行),基线返回 4 而真实声明是 3。一律用 `grep -cE '^\s*box-shadow:'`(基线 3 → 目标 2:输入框 + 冻结轮 inset)。同理 `grep -c '!important'` 返回 3(两行注释散文),声明门必须用带分号的 `grep -o '!important;' | wc -l`。

**人工验收清单(前端无自动化覆盖,Nyquist 缺口的显式补偿;写入 SUMMARY 并逐条标注 `pending`——未逐条跑过之前不得声称任何视觉结论成立):**

1. 页面左侧主区显示会话流(阶段 1-2)/ 批注流 + 自检报告(阶段 3+);右侧文档面板显示进入表单 / 草稿 / 轮次文档。**左右与旧版相反**,这是本次改版的判据本身。
2. 点文档面板标题 → 收成 48px 竖条(只剩折叠指示符);再点 → 展开。收起/展开过程中主区宽度随之变化,无横向溢出、无内容被裁切。
3. 状态徽标落在文档面板标题行内;滚动任何区域时它都不遮挡正文;`right: 448px` 魔法数已从文件中消失。
4. 主区内容列 768px 居中;AI 工作面板的 5 个探针控件(路线下拉 / 路径输入 / 发起 / 处理本轮批注 / 中止)在 768px 列内单行排下,无横向溢出。
5. **本次搬动最关键的回归点**——划词批注:在文档面板的轮次文档里划词 → 小菜单出现 → 点「批注」→ 条目出现在**主区**的批注流;点「用大白话讲这段」→ 灰斜体条目出现在主区批注流。`#selection-menu` 只绑 `#round-doc`,该元素随面板搬动后绑定必须仍然成立。
6. 助手长回答(含列表 / 代码块 / 多级标题)无背景、无内边距、无圆角、占满 768px 列;用户消息为右侧浅灰(#ececec)气泡、深色文字。两者交替出现时视觉上不对称。
7. 输入框 52px 高、28px 圆角、全页唯一的影子;模态卡片与划词菜单无影子仍可辨(模态靠深色遮罩边界,菜单靠描边)。
8. 「文档区」标题是文档面板标题行里的安静小标签,不再是全屏最大最重的文字;模态标题(24px)是全页最大的文字。
9. **安全信号回归**:`#btn-authorize`(授权撰写总设计文档)仍是绿色系、与品牌蓝按钮(发送 / 同意 / 放行)以及中性例行按钮可区分——本次换肤不得把不可逆动作的安全信号吞掉。
10. 冻结轮仍是"去饱和 + 左侧琥珀 inset 竖线",且该 inset 标记未被误当成影子删掉。
11. 已回应批注条目仍是弱化的灰字(源码顺序未被破坏)。
12. 键盘可达性(仅鼠标路径可自动化,此项为人工):Tab 能到达主区与文档面板内的交互控件;文档面板标题可用鼠标点击折叠(键盘路径不在本计划范围,A11Y-01/A11Y-03 是独立需求)。

**已知设计张力(交付时必须如实记录,不得静默):** 主区宽度 = 视口宽度 − 文档面板宽度,而助手消息去气泡后的可用宽度就是主区宽度。本次把这条张力收敛到**一个令牌** `--doc-panel-w: clamp(360px, 38vw, 620px)`(1440px 视口:面板约 547px / 主区约 893px;1152px 视口:面板约 438px / 主区约 714px)。若人工验收判定阅读列不可接受,**唯一的一值回退就是改这个令牌**,不需要任何结构性返工。这条张力交由用户裁决,**执行器不得自行改宽度**。
</verification>

<success_criteria>
- 四项用户锁定决策逐项落地:① ChatGPT 视觉语言照搬(配色 8 值 + 描边 2 等价色 + 用户气泡 + 品牌蓝;字号 5 档;行高 4 倍率;字重 3 档;圆角 4 值;影子 1 条三层叠加;助手去气泡);② 会话流在主区;③ 文档区是可折叠右面板;④ DESIGN.md §4.1/§4.2 同批修订。
- 信息架构对调完整:四个面板在主区,文档面板在右;主区内容列 768px;文档面板宽度由单一令牌控制、可收起为 48px 竖条。
- 令牌分类学零破坏:围栏恰一对、围栏外零裸 hex、零 tier-1 引用、围栏外引用的每个令牌名都在围栏内声明。
- 四条硬约束零破坏:`.hidden` 恰 1 条、`!important;` 恰 1 个、四条 `--z-*` 与断言未动、`.annotation-answered` 规则组仍在其前驱规则之后且未移动。
- 五族语义动作色名全部保留且底层值未动;`#btn-authorize` 的安全信号在人工验收第 9 条被显式回归。
- 划词批注绑定在搬动后仍成立(`#round-doc` 在文档面板内,`#selection-menu` 绑定未断)——由 Task 1 的结构断言 + 人工验收第 5 条双重覆盖。
- 改动严格限于五个文件:`git diff --name-only -- frontend DESIGN.md .claude/CLAUDE.md` 无第六个文件;`scripts/check-01..04` 与后端零改动。
- check-01 / check-03 / check-04 PASS;check-02 红着交出,失败条目数与每条数值逐条抄进 SUMMARY,并标注哪些对应真实渲染、哪些是清单陈旧项。
- 三条刻意偏差被显式记录而非静默(不透明等价描边色 / 输入框内边距 6px 吸附 / `--gray-600` 与 `--gray-700` 同值),外加 `TOKEN-08` 字面刻度被用户决策覆盖这一条。
- 人工验收 12 条清单写入 SUMMARY 且逐条标注 `pending`;主区阅读列宽度张力如实记录并交由用户裁决。
- 零新增依赖、零构建步骤、零 CDN、零图标库、零新增门禁脚本。
</success_criteria>

<output>
Create `.planning/quick/260918-qrq-frontend-chatgpt/260918-qrq-SUMMARY.md` when done
</output>
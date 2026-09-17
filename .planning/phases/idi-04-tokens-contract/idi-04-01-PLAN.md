---
phase: idi-04
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - frontend/style.css
  - scripts/check-01-token-conformance.sh
  - scripts/check-03-hidden-uniqueness.sh
  - scripts/check-04-important-count.sh
autonomous: true
requirements:
  - TOKEN-01
  - TOKEN-02
  - TOKEN-03
  - TOKEN-04
  - A11Y-04
  - CHECK-01
  - CHECK-03
  - CHECK-04

estimate:
  tokens: 95000
  raw_tokens: 95000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "frontend/style.css 顶部存在**唯一**一个 `:root` 块,由 `/* ===== DESIGN TOKENS: START ===== */` 与 `/* ===== DESIGN TOKENS: END ===== */` 两行围栏注释界定,插入位置在 `* { box-sizing: border-box; }` 之后、`html, body {` 之前 ← TOKEN-01 / UI-SPEC `## Global Hard Rules` 7(提交序第 1 步)"
    - "围栏之外 `style.css` 含零裸 `#hex`:`bash scripts/check-01-token-conformance.sh` 打印 `PASS`(计数 0)。基线为 117 匹配行 / 120 次出现 / 34 个不同值 ← TOKEN-04 / CHECK-01 / ROADMAP Phase 4 SC1"
    - "tier-1 primitive 名绝不出现在围栏之外(硬不变量,机械可查):`grep -nE '^\\s*(background|color|border|border-color|border-left|border-right|border-top|border-bottom|box-shadow)\\s*:.*--(white|black|gray|green|blue|amber|red|purple)-' frontend/style.css` 在 `:root` 块外无命中 ← TOKEN-02"
    - "`--color-text-muted: var(--gray-600)` 且 `--gray-600: #6a6a6a` —— **不是** `#767676` / `#737373` / `#6e6e6e`(三者在本文件实际出现的背景上均不达 4.5:1)。.hint 的比值 2.73:1 → 5.18:1 ← A11Y-04 第 1 项 / UI-SPEC note N-1"
    - "AA 阈值边界(显式):`--color-text-muted` 在 `#fafafa` 5.18:1、`#fff` 5.41:1、`#f5f5f5` 4.96:1、`#f0f0f0` 4.75:1 —— 四处**全部** ≥ 4.5:1;而 `#767676` 在 `#fafafa` 只有 4.35:1、在 `#f5f5f5` 4.35:1,`#737373` 在 `#f0f0f0` 4.16:1 —— 即「再浅一档即失败」的一步之隔由 CHECK-02 逐对判定(阈值判定为**闭区间**:比值 ≥ 4.5 通过)← A11Y-04 edge-probe boundary 行"
    - "对比度计算的精度契约(显式):CHECK-02 按 WCAG 2.x 相对亮度定义 `L = 0.2126R + 0.7152G + 0.0722B`(通道先做 sRGB 反伽马:`c/255 <= 0.03928 ? c/255/12.92 : ((c/255+0.055)/1.055)^2.4`),比值 `(L_light + 0.05)/(L_dark + 0.05)`,报告保留 2 位小数;**不做四舍五入到阈值** —— 4.496 判失败,4.504 判通过 ← A11Y-04 precision 行 / UI-SPEC `## Contrast Verification` 的「逐对重算」要求"
    - "`.annotation-answered` 的 `opacity: 0.65` 声明被**删除**;其内部文字改为 `var(--color-text-muted)`,1.88:1 → 5.41:1。灰色**色相**保留(「已回应…变灰不删除」仍成立),只去掉乘数 ← A11Y-04b / D-11 / UI-SPEC UI-Considerations 行 `partial` E5"
    - "`.tier-desc { opacity: 0.8 }` **保持不变**(12.63:1,已通过)—— 覆盖 ≠ 失败,该站点被裁定并保留 ← UI-SPEC UI-Considerations 行 `partial` E6"
    - "`#confirm-error` 保留 **ID 选择器**(1-0-0)且带 `var(--color-action-danger)` 声明 —— 特异性高于 `.hint`(0-1-0),G3 确认失败信息不会退化为灰色提示 ← Pitfall M6 / UI-SPEC UI-Considerations 行 `error` E12"
    - "`grep -c '^\\.hidden {' frontend/style.css` == 1 且 `grep -c '!important;' frontend/style.css` == 1 —— 全站唯一一条 `!important` 仍是 `.hidden { display: none !important }` ← CHECK-03 / CHECK-04 / ROADMAP Phase 4 SC4"
    - "围栏外零裸 hex 的**唯一**合法例外只有围栏内部的 primitive 字面量与两个 `--icon-*` data-URI(L-3,Phase 5 才声明);本计划不引入任何新例外 ← UI-SPEC `## Literal exceptions`"
    - statement: "在运行中的应用里打开一个历史(冻结)轮次,确认:①左侧有琥珀色 inset 竖线;②轮次切换器显示历史轮次;③正文可读(计算样式对比度 ≥ 4.5:1)。本环境截图不可用、headless 渲染被挡,此检查只能人工执行 —— 无法确认时按 `human_needed`(insufficient_spec)上报,绝不静默判过。渲染面在 Phase 5 收口 ← UI-SPEC UI-Considerations 行 `long-text` E8(backstop)"
      verification: backstop
  artifacts:
    - path: "frontend/style.css"
      provides: "单一围栏 `:root` 令牌块(25 个 tier-1 颜色 primitive + 50 个 tier-2 颜色语义令牌)+ 全部颜色字面量替换为 var()"
      contains: "/* ===== DESIGN TOKENS: START ===== */"
    - path: "scripts/check-01-token-conformance.sh"
      provides: "CHECK-01 令牌合规校验:围栏外裸 #hex 计数,打印 PASS/FAIL"
      contains: "DESIGN TOKENS: START"
    - path: "scripts/check-03-hidden-uniqueness.sh"
      provides: "CHECK-03 `.hidden` 全局规则唯一性守卫,打印 PASS/FAIL"
      contains: ".hidden {"
    - path: "scripts/check-04-important-count.sh"
      provides: "CHECK-04 `!important` **声明**计数守卫(按 `!important;` 计数,不按命中行)"
      contains: "!important;"
  key_links:
    - from: "frontend/style.css 围栏外声明"
      to: "frontend/style.css :root 块"
      via: "每个 `var(--x)` 必须解析到块内已声明的 `--x`(Gate 2,`comm -23` 输出为空)"
      pattern: "var\\(--color-"
    - from: "scripts/check-01-token-conformance.sh"
      to: "frontend/style.css 的两行围栏注释"
      via: "awk 状态机 `/DESIGN TOKENS: START/{f=1} /DESIGN TOKENS: END/{f=0} !f` 精确排除块内字面量"
      pattern: "DESIGN TOKENS: (START|END)"
    - from: "#confirm-error"
      to: "--color-action-danger"
      via: "ID 选择器 1-0-0 压过 .hint 0-1-0,与源码顺序无关(Pitfall M6 的机制)"
      pattern: "#confirm-error"
  prohibitions:
    - "不得新增任何 `!important` 声明,也不得把 `display` 令牌化 —— 两者都会重新打开 `.hidden` 的特异性竞速(CHECK-04 会失败,且 5 个只靠它隐藏的元素会常显)← TOKEN/CHECK-04 / UI-SPEC Global Hard Rules 1·2·4"
    - "不得对 `.hidden` 使用 `:where()` 降特异性,不得移动、改写或令牌化 `style.css:13-17` 的注释与规则(该注释的理由刚于 quick 260917-fqh 修正,现为准确)← UI-SPEC Do-Not-Touch List"
    - "不得引入 `@layer` / `@property` / `var(--x, #fallback)` —— 前三者重开 `.hidden` 竞速,第四种重建第二事实源且对 CHECK-01 隐形(hex 藏在 var() 里)← UI-SPEC Global Hard Rules 4 / Gate 2 说明"
    - "不得**重排**任何既有规则 —— 只追加。`#draft-view h2`(L232)与 `#brainstorm-view h2`(L298)同为 1-0-1 且都命中同一标题,L298 因靠后而胜出(14px / `#8a6508`);上移 L232 会让它静默渲染成 15px / `#555`,而源码 diff 看起来完全无辜 ← UI-SPEC Global Hard Rules 3 / Pitfall 9"
    - "不得改动 `frontend/app.js` 与 `frontend/index.html` 的任何一个字节 —— `app.js:4-75` 约 67 个顶层 `getElementById` 句柄,任何 id 改名/删除会在解析期静默杀死其下全部处理器(G-idi01-8);本阶段零改动是**已验证可行**的(app.js 不写颜色/间距/字号值,index.html 零内联 style=)← UI-SPEC Do-Not-Touch List / ROADMAP Phase 4 Gates"
    - "不得把 `#confirm-error` 由 ID 改成 class —— 改后它与 `.hint` 同为 0-1-0,胜者取决于源码顺序,后续任何 `.hint` 移动都会把 G3 失败信息变回灰色 ← Pitfall M6"
    - "不得软化 8 处 `:disabled` 的 `opacity: 0.55 / 0.5` —— SC 1.4.3 豁免非活动组件,而 `:disabled` 是 G3 前提条件唯一的视觉信号(软化 = 死按钮看起来可点)← A11Y-04b 例外条款 / Pitfall M5"
    - "不得把 `#stream-banner.fatal` 折叠进共享 danger 令牌 —— 它必须保持为独立选择器,否则「无法自动恢复,请刷新页面」会与「正在自动重连」视觉合一 ← UI-SPEC Do-Not-Touch List"
    - "不得为 `.hint` / `.badge-answered` 等取「更安全的」更深灰以回避边界 —— `#6a6a6a` 是**每个背景上都通过的最浅值**,取深会毁掉 hint/正文的层级关系(Pitfall 4a)← UI-SPEC `## Hierarchy preserved, not just ratios`"
    - "不得声明任何在同一提交中不被消费的令牌(唯一有界例外是 `--green-800`,见 N-2);也不得为已令牌化的值留下字面量 —— 半迁移的调色板比不迁移更糟 ← Pitfall 1 / UI-SPEC Global Hard Rules 5·6"
    - "不得触碰 `renderAnnotations` / `renderVerdictCard`(已验收的批注/裁决渲染路径),不得替换两处 `window.prompt` 调用点,不得移除或重定位 `#probe-controls` ← UI-SPEC Do-Not-Touch List / `## Not in v1.14`"
    - "不得引入任何新增运行时依赖、构建步骤或 lint 工具链(D-06);四条校验命令必须是零依赖的 grep/awk/python3 ← ROADMAP 全局硬规则 6 / CHECK-01·02"
---

<objective>
落地 `frontend/style.css` 的**单一围栏 `:root` 令牌块**与**全部颜色字面量**的 `var()` 替换,AA 达标值在**声明处**选定;并交付 CHECK-01 / CHECK-03 / CHECK-04 三条零依赖守卫命令。

Purpose: Phase 4 是本里程碑的硬前置 —— 后续四个阶段全部消费这层令牌,且它是唯一一个成功判据为**纯重构**的阶段,因而是发现"迁移方法本身错了"最便宜的地方。颜色是四个值族中最大、最危险的一族(34 个 hex / 120 次出现,且承载全部 A11Y-04 对比度修复),所以它带 tracer 先行。

Output: 带围栏令牌块的 `frontend/style.css`(颜色部分完成迁移,CHECK-01 归零)、`scripts/check-01-token-conformance.sh`、`scripts/check-03-hidden-uniqueness.sh`、`scripts/check-04-important-count.sh`。

**用户签核记录(2026-09-17,已批准,不得重新讨论):** UI-SPEC 的四个 Sign-Off Items 用户已**全部照原文批准**。该批准有两处**持久记录**可核:①`04-UI-SPEC.md` 的 `## Sign-Off Items`(契约原文);②`.planning/STATE.md` 的 `### Blockers/Concerns` `[v1.14 P4]` 条目与 `## Operator Next Steps` 的 `S-1…S-4` 逐项清单(✅ 批准 2026-09-17,规划期,并记明四项的一行式替代方案**均不执行**)。签核不在本计划内自证 —— 本计划只**消费**该已决事项。本计划执行其中两项:

- **S-3 已批准** —— 控件边框 `#ccc` → `#8a8a8a`(10 处,`--color-border-strong`)。这是本阶段最大的刻意视觉变更,**已接受**。理由:SC 1.4.11 —— 边框是识别文本输入框边界的唯一事物。**不执行**"保留 `#cccccc` 并豁免 1.4.11"的一行替代方案。
- **S-2 已批准** —— `14px` 保留为一等字号档(7 档,非字面 6 档)。TOKEN-08 的"删除 14px"**不执行**(执行会同时打破 ROADMAP Phase 5 SC5 与 Phase 6 SC5)。本计划的颜色工作不涉及字号,该签核由 Plan 02 落地。

S-1(间距 12 档,含 5 个半步)与 S-4(`#round-doc.round-frozen` 结构性标记)由 Plan 02 落地。

**无 `checkpoint:decision` 就位,这是刻意的:** 四个签核项已由用户在规划前批准(REVERSIBILITY_GATES 要求"为单向门决策放置 checkpoint";此处决策**已经**由用户做出,再问一次即重新审理已决事项)。令牌命名分类学评为 `costly` 而非 `one-way`(改名是机械替换,只是会波及四个下游阶段),故只记录不设卡。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/REQUIREMENTS.md
@.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md
@frontend/style.css
</context>

<tasks>

<task type="tracer">
  <name>Task 1 (tracer): 围栏令牌块 + 文本色族端到端迁移 + 三条守卫命令</name>
  <files>frontend/style.css, scripts/check-01-token-conformance.sh, scripts/check-03-hidden-uniqueness.sh, scripts/check-04-important-count.sh</files>
  <read_first>
    - frontend/style.css(正在修改的文件;先看当前状态,不要凭假设改)
    - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md —— 读 `## Color` 的 Tier 1 primitives 表、Tier 2 语义表(Text/surface/border 段)、`### Meaning inventory`、`### RULING: #round-doc.round-frozen` 之外的 `opacity` rulings 段、`## The Four Contract-Check Commands`、`## Global Hard Rules`
    - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md 的 `## Sign-Off Items`(S-1…S-4 已由用户批准,照原文执行)
  </read_first>
  <action>
    这是本阶段的 tracer:用**一条最薄的端到端切片**同时打通本阶段要改的两层 —— 新增的 `scripts/` 校验层与 `style.css` 的令牌层 —— 并让它携带一条真实可跑的验证。

    1) **落地围栏与颜色 primitive。** 在 `* { box-sizing: border-box; }` 之后、`html, body {` 之前插入唯一一个 `:root` 块,用 `/* ===== DESIGN TOKENS: START ===== */` 与 `/* ===== DESIGN TOKENS: END ===== */` 两行围栏注释界定。块内先放 tier-1 颜色 primitive(共 25 个,全部字面量只允许出现在这里):`--white #ffffff`、`--black #000000`、`--gray-900 #1a1a1a`、`--gray-700 #555555`、`--gray-600 #6a6a6a`、`--gray-500 #8a8a8a`、`--gray-300 #dddddd`、`--gray-100 #eeeeee`、`--gray-50 #f5f5f5`、`--gray-25 #fafafa`、`--green-800 #1f5c3a`、`--green-700 #26754a`、`--green-100 #e9f7ef`、`--blue-700 #1f63bd`、`--blue-100 #eef4ff`、`--blue-50 #f0f7ff`、`--amber-800 #8a6508`、`--amber-300 #d9c58a`、`--amber-100 #fff3c4`、`--amber-50 #fdf6ec`、`--amber-25 #fffdf5`、`--red-600 #c0392b`、`--red-200 #e8b4ae`、`--red-50 #fdecea`、`--purple-600 #6f42c1`。`--gray-600` / `--gray-500` / `--green-800` 是三个新值;其余由现有 34 个 hex 折叠而来(13 个被折叠消除)。

    2) **块内再放本任务消费的 tier-2 文本族令牌**(绝不声明本任务不消费的令牌 —— UI-SPEC Global Hard Rule 5):`--color-text: var(--gray-900)`、`--color-text-secondary: var(--gray-700)`、`--color-text-muted: var(--gray-600)`、`--color-surface-page: var(--gray-25)`、`--color-surface-sunken: var(--gray-50)`、`--color-kind-default: var(--gray-600)`、`--color-kind-result: var(--gray-700)`、`--color-action-danger: var(--red-600)`。**共 8 个,每个都在本任务第 3 步被消费。**

    **本任务不声明的三个令牌(由 Task 3 与它们的消费者同提交声明,避免违反 Hard Rule 5):** `--color-text-inverse`(Task 3 的 `.chat-user` 消费)、`--color-kind-fg`(Task 3 的 `.event-kind` 消费)、`--color-border-danger-subtle`(Task 3 的 `#stream-banner.fatal` 消费)。本任务的 acceptance 只断言本任务实际声明的 8 个。

    **两处计划期裁定(UI-SPEC 的残留缺口,在此显式补上,不是疏漏):**
    - `--color-border-danger-subtle: var(--red-200)` 是**新令牌**。UI-SPEC 的 Tier-2 表把 `#fdecea` 命名为 `--color-surface-danger` 却漏了 `#e8b4ae`(`#stream-banner.fatal` 的 `border-color`)—— 它属于 meaning-inventory 行 19–23 同一类"有值无合法名"的缺口。不加它,`.fatal` 的边框在围栏外就没有合法名可写。**它的声明与消费都在 Task 3**(Task 3 替换 `#stream-banner.fatal` 的 `border-color`),本任务不声明它 —— 见上一条。
    - `--color-surface-success` **不声明**。UI-SPEC 的 Tier-2 表列了它,但其含义清单说的消费者是"三个绿色按钮族",而那三族各自持有 `-surface` 令牌(`--color-action-*-surface`),Phase 5 还要把 commit/irreversible 两族的 surface 改成实心填充 —— 一个共享的"success surface"名会立刻变成假抽象,且违反 Global Hard Rule 5(不得声明未消费的令牌)。三个绿色 surface 直接从 `--green-100` 取值。

    3) **迁移文本色族的字面量**(逐条替换,只改值,不改选择器、不重排、不增删其它声明)。**恰好这 19 行,替换后 CHECK-01 的围栏外匹配行数应为 98**(基线 117 − 19):`html, body` 的 `background: #fafafa` → `var(--color-surface-page)`、`color: #1a1a1a` → `var(--color-text)`;`.hint` 的 `color: #999` → `var(--color-text-muted)`;`.event-kind` 的 `background: #999` → `var(--color-kind-default)`;`.kind-result .event-kind` 的 `background: #555` → `var(--color-kind-result)`;`#draft-view h2` 的 `color: #555` → `var(--color-text-secondary)`;`.markdown-body blockquote` 的 `color: #666` → `var(--color-text-muted)`;`.annotation-quote` 的 `color: #555` → `var(--color-text-secondary)`;`.annotation-note` 的 `color: #1a1a1a` → `var(--color-text)`;`.badge-answered` 的 `color: #999` → `var(--color-text-muted)`、`background: #f5f5f5` → `var(--color-surface-sunken)`;`.annotation-plain .annotation-note, .annotation-plain .annotation-answer-body` 的 `color: #999` → `var(--color-text-muted)`;`.annotation-answer summary` 的 `color: #999` → `var(--color-text-muted)`;`.overlay-card p` 的 `color: #444` → `var(--color-text-secondary)`;`.verdict-location` 的 `color: #555` → `var(--color-text-secondary)`;`.verdict-issue` 的 `color: #1a1a1a` → `var(--color-text)`;`.verdict-suggestion` 的 `color: #666` → `var(--color-text-muted)`。同时给 `#confirm-error` 的 `color: #c0392b` → `var(--color-action-danger)`(**保留 ID 选择器不动**,Pitfall M6)。`.kind-error .event-content` 的 `color: #c0392b` 也一并改 `var(--color-action-danger)`(同一值,同族)。

    **19 行 = 上面枚举的 17 行 + `#confirm-error`(`style.css:552`)+ `.kind-error .event-content`(`style.css:150`)。** 这 19 行**全部**是 hex 承载行,替换后 `grep -c` 从 117 落到 98。此处以行数(而非出现次数)计:CHECK-01 用 `grep -c`,数的是匹配**行**。

    4) **A11Y-04b:`#annotation-list` 的已回应灰化(D-11)。** 删除 `.annotation-answered { opacity: 0.65 }` 这条声明(整条规则体已空,连同该规则一并移除,其上方注释改为说明新机制),并在文件**末尾追加**(绝不插入、绝不重排)一条新规则:`.annotation-answered .annotation-note, .annotation-answered .annotation-quote, .annotation-answered .annotation-answer summary { color: var(--color-text-muted); }`。

    **为什么必须是 0-2-0 的后代选择器(准确的理由,勿改成"父级压不过子级"的简化说法):** 真正的竞争者不是裸 `.annotation-note`(0-1-0)—— 那条在同等特异性下由**源码顺序**决定,追加在末尾的父级规则本可赢过它。真正的竞争者是 `.annotation-plain .annotation-note`(0-2-0,`style.css:460-463`);两个 class 可以同时出现在一个条目上(`app.js:1120-1121` 确认)。0-1-0 的父级规则**压不过** 0-2-0 的它,所以必须用同为 0-2-0 的后代选择器,并靠追加在文件末尾的源码顺序取胜。(该 0-2-0 竞争者在**本任务**同样被赋 `--color-text-muted`,故二者值一致、不会冲突 —— 但选择器形态仍须是 0-2-0 才能对未来的值分歧保持稳健。)灰色色相保留,只去掉那个 1.88:1 的乘数。

    5) **新建三条零依赖守卫命令**(`scripts/` 目录,新建;不在 `frontend/` 下,以避开"frontend/ 仅三个已知文件"的门):
    - `scripts/check-01-token-conformance.sh`:`#!/usr/bin/env bash` + `set -euo pipefail`;用 awk 状态机 `/===== DESIGN TOKENS: START/{f=1} /===== DESIGN TOKENS: END/{f=0} !f` 过滤掉围栏块,再 `grep -c '#[0-9a-fA-F]\{3,6\}'`。计数为 0 打印 `PASS` 并 `exit 0`;否则打印 `FAIL: <n> bare hex outside the token block` 并 `exit 1`。**注意 `grep -c` 在计数为 0 时退出码为 1**,所以判定必须读 stdout 数值,不能靠 grep 的退出码。
    - `scripts/check-03-hidden-uniqueness.sh`:取 `grep -c '^\.hidden {' frontend/style.css`,等于 1 打印 `PASS` 并 `exit 0`,否则打印 `FAIL` 并 `exit 1`。
    - `scripts/check-04-important-count.sh`:取 `grep -c '!important;' frontend/style.css`(**按声明计数,不是按命中行** —— `grep -c '!important'` 会返回 3,其中 2 行是 L13-16 的注释散文),等于 1 打印 `PASS` 并 `exit 0`,否则打印 `FAIL` 并 `exit 1`。
    三个脚本各自 `chmod +x`,各自可独立运行。

    **不要做:** 不要在本任务里迁移 action / surface / border 族的字面量(那是 Task 2/3);不要声明本任务不消费的令牌;不要碰 `#state-badge { right: 448px }`(L-5,LAYOUT-01 是 Phase 6);不要 tokenize `display`;不要重排任何规则。
  </action>
  <verify>
    <automated>bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh</automated>
    <fails_when>任一命令退出码非 0,或 stdout 中出现 `FAIL` 字样</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>退出码为 0,或 stdout 不含 `FAIL: 98 bare hex outside the token block` —— **此刻 CHECK-01 必须正确地报错**:本任务只迁移了文本色族,围栏外仍有 98 行裸 hex。这条"预期失败"正是 tracer 对校验层端到端可用性的证明(awk 围栏状态机真的排除了块内字面量、计数口径正确、失败方向可观察)。CHECK-01 转为 PASS 是 Task 3 的判据。</fails_when>
    <automated>awk '/===== DESIGN TOKENS: START/{f=1} /===== DESIGN TOKENS: END/{f=0} !f' frontend/style.css | grep -c '#[0-9a-fA-F]\{3,6\}'</automated>
    <fails_when>stdout 不是十进制整数 98(基线 117 减去本任务迁移的 19 行)</fails_when>
    <automated>comm -23 <(grep -o 'var(--[a-z0-9-]*' frontend/style.css | sed 's/var(//' | sort -u) <(grep -o '\-\-[a-z0-9-]*:' frontend/style.css | sed 's/:$//' | sort -u)</automated>
    <fails_when>stdout 非空 —— 打印出的任一 `--x` 表示存在未声明的 var() 消费(Gate 2:var() 静默失败,拼错即整条声明回退 unset)</fails_when>
    <automated>grep -c '^\.hidden {' frontend/style.css && grep -c '!important;' frontend/style.css && grep -c '!important' frontend/style.css</automated>
    <fails_when>三行输出不是依次为 1、1、3(第三行是已知的注释散文算术陷阱,用于证明 CHECK-04 数的是声明而不是命中行)</fails_when>
    <human-check>启动应用(`./run.sh`,http://127.0.0.1:8765),在 DevTools Elements 面板选中一处闸门说明文字(`.hint`,例如「进入」表单下方或 `#approve-row` 下方),读 Computed → color,应为 `rgb(106, 106, 106)`;再选 `.badge-answered`,color 亦为 `rgb(106, 106, 106)`。打开一个历史(冻结)轮次,确认左侧出现琥珀色 inset 竖线且正文可读(backstop 真值)。**本环境截图不可用、headless 渲染被挡 —— 不得改用视觉 diff。**</human-check>
  </verify>
  <acceptance_criteria>
    - `bash scripts/check-01-token-conformance.sh` 退出 1 且 stdout 含 `FAIL: 98 bare hex outside the token block`(tracer 阶段的**预期失败** —— 校验层可用且失败方向可观察;转为 PASS/0 是 Task 3 的判据)
    - `awk '/===== DESIGN TOKENS: START/{f=1} /===== DESIGN TOKENS: END/{f=0} !f' frontend/style.css | grep -c '#[0-9a-fA-F]\{3,6\}'` 输出 `98`
    - `grep -c '^\.hidden {' frontend/style.css` 输出 `1`;`grep -c '!important;' frontend/style.css` 输出 `1`
    - `frontend/style.css` 含 `/* ===== DESIGN TOKENS: START ===== */` 与 `/* ===== DESIGN TOKENS: END ===== */` 各恰好 1 次;START 行号 > `* { box-sizing` 的行号,且 < `html, body {` 的行号
    - `frontend/style.css` 含 `--color-text-muted: var(--gray-600);` 与 `--gray-600: #6a6a6a;`
    - `frontend/style.css` **不含** `#767676`、`#737373`、`#6e6e6e`
    - `grep -n 'opacity: 0.65' frontend/style.css` 无命中(`.annotation-answered` 的乘数已删除);`grep -n 'opacity: 0.8' frontend/style.css` 仍有 1 处命中(`.tier-desc` 保留)
    - `frontend/style.css` 含 `.annotation-answered .annotation-note` 且其声明为 `color: var(--color-text-muted)`
    - `frontend/style.css` 含 `#confirm-error { color: var(--color-action-danger); }`(ID 选择器保留)
    - `frontend/style.css` **不含** `--color-surface-success`
    - `frontend/style.css` **不含** `--color-text-inverse`、`--color-kind-fg`、`--color-border-danger-subtle`(三者由 Task 3 与各自的消费者同提交声明 —— 本任务不得声明不消费的令牌,Hard Rule 5)
    - `comm -23 <(grep -o 'var(--[a-z0-9-]*' frontend/style.css | sed 's/var(//' | sort -u) <(grep -o '\-\-[a-z0-9-]*:' frontend/style.css | sed 's/:$//' | sort -u)` 输出为空
    - `node --check frontend/app.js` 退出 0;`git diff --name-only HEAD -- frontend/app.js frontend/index.html` 输出为空
    - `ls frontend/vendor/` 只含 `marked.min.js`
    - 三个脚本文件均存在且可执行(`test -x` 通过)
  </acceptance_criteria>
  <done>围栏令牌块就位且位置正确;文本色族 19 行字面量全部替换;CHECK-01 围栏外计数恰为 98;CHECK-03/04 均打印 PASS;`.annotation-answered` 的 opacity 已删、其文字改走 `--color-text-muted`;三条守卫命令独立可跑且各有明确 PASS/FAIL;Gate 2 为空;app.js/index.html 零改动。</done>
</task>

<task type="auto">
  <name>Task 2: 动作族颜色迁移 —— 六绿按钮、kind 芯片、danger</name>
  <files>frontend/style.css</files>
  <read_first>
    - frontend/style.css(读 Task 1 之后的当前状态)
    - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md 的 `### Q1 — Token naming, and the positive / gate / irreversible split`(含"两个非动作绿色消费者"表)与 `### Tier 2 — semantic` 的 Actions / Event kinds 两段
  </read_first>
  <action>
    在 `:root` 块内**追加**本任务消费的 tier-2 动作与 kind 令牌(不声明不消费的):`--color-action-primary: var(--blue-700)`、`--color-action-primary-fg: var(--white)`、`--color-action-danger-fg: var(--white)`、`--color-action-warning: var(--amber-800)`、`--color-action-warning-surface: var(--amber-50)`、`--color-action-routine: var(--green-700)`、`--color-action-routine-surface: var(--green-100)`、`--color-action-routine-fg: var(--green-700)`、`--color-action-commit: var(--green-700)`、`--color-action-commit-surface: var(--green-100)`、`--color-action-commit-fg: var(--green-700)`、`--color-action-irreversible: var(--green-700)`、`--color-action-irreversible-surface: var(--green-100)`、`--color-action-irreversible-fg: var(--green-700)`、`--color-kind-say: var(--blue-700)`、`--color-kind-read: var(--purple-600)`、`--color-kind-write: var(--green-700)`、`--color-kind-command: var(--amber-800)`、`--color-kind-error: var(--red-600)`、`--color-kind-done: var(--black)`、`--color-border-success: var(--green-700)`。

    **`--color-border-success` 必须在本任务的追加清单里**(不是只在 acceptance 里出现):它是第 12 个 `#2e8b57` 站点(`#mission-complete-modal .overlay-card` 的 `border: 2px solid`)的消费目标。缺了它,Gate 2(`comm -23` 消费集减声明集)在本任务结束时不可能为空,`check-02-contrast.py` 也会对未知令牌大声失败 —— 而「声明与消费同提交」正是 Hard Rule 5 的要求。**共 21 个令牌,每个都在本任务被消费。**

    **Phase 4 值规则(刻意,不是遗漏):** 三个绿色族在 Phase 4 **共用同一对值**(`--green-700` / `--green-100`)。令牌**名**在此落地,视觉差异化是 Phase 5 的事 —— 届时每一族只需改一行值,而不是重写选择器。`--color-action-irreversible*` 在本阶段**只被 `#btn-authorize` 消费,且永远只被它消费**。

    然后逐条替换字面量(只改值,不改选择器、不重排、不增删其它声明):
    - 六个绿色按钮:`.kind-write .event-kind` 的 `background: #2e8b57` → `var(--color-kind-write)`;`#btn-approve-draft` 的 `border-color: #2e8b57` → `var(--color-action-commit)`、`color: #2e8b57` → `var(--color-action-commit-fg)`、`background: #e9f7ef` → `var(--color-action-commit-surface)`;`#btn-process-round` 的 `border-color: #2e8b57` → `var(--color-action-routine)`、`color: #2e8b57` → `var(--color-action-routine-fg)`、`background: #e9f7ef` → `var(--color-action-routine-surface)`;`#btn-authorize` 的 `border-color: #2e8b57` → `var(--color-action-irreversible)`、`color: #2e8b57` → `var(--color-action-irreversible-fg)`、`background: #e9f7ef` → `var(--color-action-irreversible-surface)`;`#btn-start-writing` 同 `#btn-approve-draft` 用 commit 族;`#btn-continue-check, #btn-continue-repair` 用 routine 族。
    - 第 12 个 `#2e8b57` 站点(不是按钮):`#mission-complete-modal .overlay-card` 的 `border: 2px solid #2e8b57` → `var(--color-border-success)`(它框住的是"已完成"状态,属 border 族,不属任何动作族)。
    - `#btn-divergence`:`border-color: #b8860b` → `var(--color-action-warning)`、`color: #8a6508` → `var(--color-action-warning)`、`background: #fdf6ec` → `var(--color-action-warning-surface)`。
    - `.kind-command .event-kind` 的 `background: #b8860b` → `var(--color-kind-command)`;`#pending-count` 与 `.badge-pending` 的 `color: #b8860b` → `var(--color-action-warning)`。
    - 蓝色族:`button.primary`、`.overlay-card button`、`#chat-input-row button` 的 `background` / `border-color: #2c7be5` → `var(--color-action-primary)`,`color: #fff` → `var(--color-action-primary-fg)`;`.kind-say .event-kind` 的 `background: #2c7be5` → `var(--color-kind-say)`。
    - 红/紫/黑:`button.danger` 与 `.overlay-card button.danger` 的 `#c0392b` → `var(--color-action-danger)`,其 `color: #fff` → `var(--color-action-danger-fg)`;`.kind-error .event-kind` 的 `background: #c0392b` → `var(--color-kind-error)`;`.kind-read .event-kind` 的 `background: #6f42c1` → `var(--color-kind-read)`;`.kind-done .event-kind` 的 `background: #000` → `var(--color-kind-done)`。
    - `#stream-banner` 的 `color: #8a6508` → `var(--color-action-warning)`。

    **不要做:** 不要动 `.event-kind` 的 `color: #fff`(它属 kind-fg,`--color-kind-fg` 由 **Task 3** 与它的消费者 `.event-kind` 同提交声明 —— 本任务声明它就会违反 Hard Rule 5);不要改任何 `padding` / `font-size` / `border-radius`(Plan 02);不要重排规则;不要引入新令牌。
  </action>
  <verify>
    <automated>awk '/===== DESIGN TOKENS: START/{f=1} /===== DESIGN TOKENS: END/{f=0} !f' frontend/style.css | grep -c '#[0-9a-fA-F]\{3,6\}'</automated>
    <fails_when>stdout 不是十进制整数,或该整数不小于 98(本任务必须把围栏外计数严格压到 Task 1 结束时的 98 以下;CHECK-01 此刻仍应打印 `FAIL`,转 PASS 是 Task 3 的判据)</fails_when>
    <automated>comm -23 <(grep -o 'var(--[a-z0-9-]*' frontend/style.css | sed 's/var(//' | sort -u) <(grep -o '\-\-[a-z0-9-]*:' frontend/style.css | sed 's/:$//' | sort -u)</automated>
    <fails_when>stdout 非空(存在未声明的 var() 消费)</fails_when>
    <automated>bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh && node --check frontend/app.js</automated>
    <fails_when>任一命令退出码非 0,或 stdout 出现 `FAIL` 字样</fails_when>
    <human-check>在 DevTools Computed 面板读:`#btn-authorize` 的 `color` == `rgb(38, 117, 74)`、`border-color` == `rgb(38, 117, 74)`、`background-color` == `rgb(233, 247, 239)`;`#btn-process-round` 三者与 `#btn-authorize` **逐字节相同**(这是 Phase 4 的刻意状态 —— 差异化是 Phase 5 的活);`.kind-write .event-kind` 的 `background-color` == `rgb(38, 117, 74)`;`.kind-done .event-kind` 的 `background-color` == `rgb(0, 0, 0)`。</human-check>
  </verify>
  <acceptance_criteria>
    - 围栏外 CHECK-01 计数严格小于 98(Task 1 结束时的值)
    - `frontend/style.css` 含 `--color-action-irreversible: var(--green-700);`、`--color-action-irreversible-surface: var(--green-100);`、`--color-action-irreversible-fg: var(--green-700);`
    - `grep -c 'var(--color-action-irreversible' frontend/style.css` 的全部命中都出现在 `#btn-authorize` 规则体内(无第二消费者)
    - `frontend/style.css` 含 `#mission-complete-modal .overlay-card { border: 2px solid var(--color-border-success); }`
    - `frontend/style.css` 含 `--color-border-success: var(--green-700);`
    - `frontend/style.css` 围栏外 `grep -c '#2e8b57'` 输出 **0**(本任务覆盖它的全部 12 个站点)
    - `frontend/style.css` 围栏外 `grep -c '#2c7be5'` 输出 **2** —— 且这两处必须是 `.chat-user` 的 `background`(`style.css:332`)与 `.chat-ai.streaming-ai` 的 `border-left`(`style.css:341`)。二者是 **Task 3** 的站点(`--color-surface-info-strong` / `--color-border-streaming`),本任务不得触碰;本任务只清除它自己的 7 个 `#2c7be5` 站点(kind-say、`.overlay-card button`、`#chat-input-row button`、`button.primary`)
    - `frontend/style.css` 仍含 `#stream-banner.fatal { background: #fdecea; color: #c0392b; border-color: #e8b4ae; }` 的**独立选择器**(未被折叠进共享 danger 令牌)
    - `comm -23 <(...var(...)...) <(...--...:...)>` 输出为空
    - `node --check frontend/app.js` 退出 0;`git diff --name-only HEAD -- frontend/app.js frontend/index.html` 输出为空
  </acceptance_criteria>
  <done>动作族与 kind 族的颜色字面量全部替换;`--color-action-irreversible*` 只被 `#btn-authorize` 消费;第 12 个 `#2e8b57` 站点(使命完成模态边框)归入 `--color-border-success`;围栏外计数严格下降;`.fatal` 保持独立选择器。</done>
</task>

<task type="auto">
  <name>Task 3: 表面/边框族收尾 —— CHECK-01 归零与 D-9 边框对比度修复</name>
  <files>frontend/style.css</files>
  <read_first>
    - frontend/style.css(读 Task 2 之后的当前状态)
    - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md 的 `### Tier 2 — semantic`(Text/surface/border 段)、`### Non-text contrast (SC 1.4.11, ≥3:1)`、`## Deliberate Delta Ledger`(D-9 / D-10 / D-10b / D-14 / D-15)
    - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md 的 `## Sign-Off Items` 中 **S-3**(已由用户批准)
  </read_first>
  <action>
    1) 在 `:root` 块内**追加**本任务消费的 tier-2 表面/边框/遮罩令牌:`--color-surface: var(--white)`、`--color-surface-hover: var(--gray-100)`、`--color-surface-info: var(--blue-100)`、`--color-surface-warning: var(--amber-50)`、`--color-surface-warning-subtle: var(--amber-25)`、`--color-surface-mark: var(--amber-100)`、`--color-surface-danger: var(--red-50)`、`--color-surface-streaming: var(--blue-50)`、`--color-border-strong: var(--gray-500)`、`--color-border: var(--gray-300)`、`--color-border-subtle: var(--gray-100)`、`--color-border-warning-subtle: var(--amber-300)`、`--color-border-streaming: var(--blue-700)`、`--color-surface-info-strong: var(--blue-700)`、`--color-text-info: var(--blue-700)`、`--color-overlay-backdrop: rgba(0, 0, 0, 0.45)`、`--shadow-overlay: 0 8px 30px rgba(0, 0, 0, 0.2)`、`--shadow-menu: 0 4px 14px rgba(0, 0, 0, 0.18)`、**以及三个由本任务与消费者同提交声明的令牌** `--color-text-inverse: var(--white)`、`--color-kind-fg: var(--white)`、`--color-border-danger-subtle: var(--red-200)`。

    **那三个令牌为何在此而非 Task 1:** 它们的唯一消费者全在本任务(本任务第 2 步的 `.chat-user` → `--color-text-inverse`、`.event-kind` → `--color-kind-fg`;`.fatal` 的 `border-color` → `--color-border-danger-subtle`)。把它们放在消费者同一次提交里,是 UI-SPEC Global Hard Rule 5(不得声明同一提交中不被消费的令牌)的直接落地。**共 21 个令牌,每个都在本任务被消费。**

    2) 替换剩余全部颜色字面量(只改值,不改选择器、不重排、不增删其它声明):
    - **D-9(S-3 已批准,本阶段最大刻意视觉变更):** `#ai-route-select`、`#project-path-input`、`button`、`#enter-form input[type="text"]`、`#chat-input-row input`、`#round-switcher`、`#selection-menu`、`#confirmation-modal input[type="text"]`、`#check-switcher`、`.verdict-note-input` 共 **10 处** `1px solid #ccc` 的 `border`/`border-color` → `var(--color-border-strong)`。**不执行**"保留 `#cccccc`"的退出口 —— 用户已批准 `#8a8a8a`。
    - `.markdown-body blockquote` 的 `border-left: 3px solid #ccc`(**第 11 处 `#ccc`,非控件**)→ `var(--color-border)`。
    - `#doc-pane` 的 `border-right: 1px solid #e0e0e0`、`.badge-answered` 的 `border: 1px solid #e0e0e0`、`.panel-header` / `#annotations-panel` / `#checks-panel` 的 `1px solid #eee`、`.annotation-item` 的 `1px solid #eee`、`.event-list` 与 `#latest-check` 的 `1px solid #f0f0f0` → `var(--color-border-subtle)`。
    - `.markdown-body th, .markdown-body td` 的 `1px solid #ddd` → `var(--color-border)`。
    - `#brainstorm-view` 的 `border: 1px dashed #d9c58a` → `var(--color-border-warning-subtle)`(值不变,1.68:1,装饰性,不在 1.4.11 范围)。
    - **D-10b:** `.verdict-card` 的 `border: 1px solid #e8d9a8` → `var(--color-border-warning-subtle)`(值 1.38 → 1.68,与 `#brainstorm-view` 共用同一档琥珀装饰)。
    - **D-10(状态指示器,SC 1.4.11 在范围内):** `#stream-banner` 的 `border: 1px solid #e8d9a8`、`#pending-count` 的 `border: 1px solid #e8d9a8`、`.badge-pending` 的 `border: 1px solid #e8d9a8`、`.annotation-pending-item` 的 `border-left: 3px solid #e8d9a8` 共 **4 处** → `var(--color-action-warning)`(1.26–1.38 → 4.78–5.23)。
    - `#stream-banner.fatal` 的 `border-color: #e8b4ae` → `var(--color-border-danger-subtle)`(**保持 `.fatal` 为独立选择器**,两态仍可区分)。
    - 表面:`#sidebar` 的 `background: #fff` → `var(--color-surface)`;`#selection-menu`、`.annotation-item`、`button`、`.overlay-card` 的 `background: #fff` → `var(--color-surface)`;`#ai-route-select` / `#round-switcher` / `#check-switcher` 的 `background: #fff` → `var(--color-surface)`;`.event-list` 与 `#latest-check` 的 `background: #fdfdfd` → `var(--color-surface)`;`.panel-header` 的 `background: #f5f5f5` → `var(--color-surface-sunken)`;`.chat-ai` 的 `background: #f1f3f5` → `var(--color-surface-sunken)`;`.markdown-body code` 的 `background: #f4f4f4` → `var(--color-surface-sunken)`;`button:hover` 的 `background: #f0f0f0` → `var(--color-surface-hover)`;`#state-badge` 的 `background: #eef4ff` → `var(--color-surface-info)`;`#selection-menu button:hover` 的 `background: #eef4ff` → `var(--color-surface-info)`;`.event-list.streaming` 的 `background: #f0f7ff` → `var(--color-surface-streaming)`;`.event-list.aborted` 与 `#stream-banner.fatal` 的 `background: #fdecea` → `var(--color-surface-danger)`;`#stream-banner` 与 `mark` 的 `background: #fff3c4` → `var(--color-surface-mark)`;`#brainstorm-view` 与 `.verdict-card` 的 `background: #fffdf5` → `var(--color-surface-warning-subtle)`;`#pending-count` 与 `.badge-pending` 的 `background: #fdf6ec` → `var(--color-surface-warning)`;`.chat-user` 的 `background: #2c7be5` → `var(--color-surface-info-strong)`;`.chat-ai.streaming-ai` 的 `border-left: 3px solid #2c7be5` → `var(--color-border-streaming)`;`#state-badge` 的 `color: #2c5fb8` → `var(--color-text-info)`;`.chat-user` 的 `color: #fff` → `var(--color-text-inverse)`;`.event-kind` 的 `color: #fff` → `var(--color-kind-fg)`。
    - 遮罩与阴影:`.overlay` 的 `background: rgba(0, 0, 0, 0.45)` → `var(--color-overlay-backdrop)`;`.overlay-card` 的 `box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2)` → `var(--shadow-overlay)`;`#selection-menu` 的 `box-shadow: 0 4px 14px rgba(0, 0, 0, 0.18)` → `var(--shadow-menu)`。
    - **两个必须点名的收尾站点(否则只有"替换剩余全部"这句兜底,令牌选择无指引):**
      - `style.css:44` `.inline-error { color: #c0392b; … }` → `var(--color-action-danger)`。它是 UI-SPEC 破坏性/错误行里点名的一处,与 `#confirm-error` / `.kind-error .event-content` 同族同值(本阶段三处共用 `--red-600`)。**不要**新建一个"错误文字"令牌。
      - `style.css:301` `#brainstorm-view h2 { … color: #8a6508 }` → `var(--color-action-warning)`。它是 `#brainstorm-view` 标题的琥珀色,与 `#stream-banner` / `#pending-count` / `.badge-pending` 同一琥珀档;它同时是 Phase 5/6 下游门断言的对象(`#brainstorm-view h2` 计算为 14px / `rgb(138, 101, 8)`),值必须保持 `#8a6508` 不变。

    3) 收尾自检:`bash scripts/check-01-token-conformance.sh` 必须打印 `PASS`(围栏外 0 裸 hex);Gate 2 必须为空。若仍有残留,定位并归入正确的语义令牌,**不要**新增 primitive 名到围栏之外。

    **不要做:** 不要 tokenize `top` / `right` / `max-width` / `min-width` / `min-height` / `max-height` / `flex` 的像素值(见下方"令牌化范围边界");不要碰 `#state-badge { right: 448px }`;不要给任何选择器增删声明(唯一例外是本阶段已在 ledger 记明的两处追加规则,且它们属 Plan 02 与本计划 Task 1);不要重排规则。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>退出码非 0,或 stdout 不含 `PASS`(即围栏外仍有裸 hex)</fails_when>
    <automated>awk '/===== DESIGN TOKENS: START/{f=1} /===== DESIGN TOKENS: END/{f=0} !f' frontend/style.css | grep -c '#[0-9a-fA-F]\{3,6\}'</automated>
    <fails_when>stdout 不是 0</fails_when>
    <automated>comm -23 <(grep -o 'var(--[a-z0-9-]*' frontend/style.css | sed 's/var(//' | sort -u) <(grep -o '\-\-[a-z0-9-]*:' frontend/style.css | sed 's/:$//' | sort -u)</automated>
    <fails_when>stdout 非空(存在未声明的 var() 消费)</fails_when>
    <automated>bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh && node --check frontend/app.js && .venv/bin/python -m pytest -q</automated>
    <fails_when>任一命令退出码非 0;或 pytest 摘要行的 passed 数少于 225(见下方基线说明);或 CHECK-03/04 stdout 出现 `FAIL`</fails_when>
    <automated>test -z "$(git diff --name-only HEAD -- frontend/app.js frontend/index.html)" && test -z "$(git ls-files --others --exclude-standard frontend/)" && test "$(ls frontend/vendor/)" = "marked.min.js"</automated>
    <fails_when>任一 `test` 返回非 0 —— 即 app.js/index.html 被改动、或 `frontend/` 下出现新文件、或 vendor 目录不是恰好 `marked.min.js`</fails_when>
    <human-check>在 DevTools Computed 面板读:`#ai-route-select` 的 `border-top-color` == `rgb(138, 138, 138)`(这是 D-9 的最大视觉变更,应肉眼可见输入框/按钮边框变深);`#selection-menu` 的 `border-top-color` 亦为 `rgb(138, 138, 138)`;`#stream-banner` 的 `border-top-color` == `rgb(138, 101, 8)`;`#state-badge` 的 `color` == `rgb(31, 99, 189)`、`background-color` == `rgb(238, 244, 255)`;`.chat-user` 的 `background-color` == `rgb(31, 99, 189)`;`.overlay-card` 的 `box-shadow` 含 `rgba(0, 0, 0, 0.2)`。</human-check>
  </verify>
  <acceptance_criteria>
    - `bash scripts/check-01-token-conformance.sh` 退出 0 且 stdout 含 `PASS`
    - `awk '/===== DESIGN TOKENS: START/{f=1} /===== DESIGN TOKENS: END/{f=0} !f' frontend/style.css | grep -c '#[0-9a-fA-F]\{3,6\}'` 输出 `0`
    - `frontend/style.css` 含 `--color-border-strong: var(--gray-500);` 且 `--gray-500: #8a8a8a;`
    - `frontend/style.css` 含本任务与消费者同提交声明的三个令牌:`--color-text-inverse: var(--white);`、`--color-kind-fg: var(--white);`、`--color-border-danger-subtle: var(--red-200);`(Task 1 的 acceptance 反向断言这三者**不**在 Task 1 结束时存在)
    - 围栏外 `1px solid var(--color-border-strong)` 恰出现 10 次;`border-left: 3px solid var(--color-border)` 恰出现 1 次(blockquote)
    - `frontend/style.css` 仍含 `#stream-banner.fatal { background: var(--color-surface-danger); color: var(--color-action-danger); border-color: var(--color-border-danger-subtle); }` 形式的**独立** `.fatal` 选择器
    - `frontend/style.css` 含 `--color-overlay-backdrop: rgba(0, 0, 0, 0.45);`、`--shadow-overlay: 0 8px 30px rgba(0, 0, 0, 0.2);`、`--shadow-menu: 0 4px 14px rgba(0, 0, 0, 0.18);`
    - `comm -23 <(...var(...)...) <(...--...:...)>` 输出为空
    - `node --check frontend/app.js` 退出 0;pytest 全绿且通过数 ≥ 225
    - `git diff --name-only HEAD -- frontend/app.js frontend/index.html` 输出为空;`git status --porcelain frontend/` 只有 `frontend/style.css`
    - `ls frontend/vendor/` 仅 `marked.min.js`
  </acceptance_criteria>
  <done>围栏外零裸 hex(CHECK-01 PASS);10 处控件边框改 `#8a8a8a`(S-3 已批准);4 处琥珀状态指示器边框改 `#8a6508`;`.verdict-card` 与 `#brainstorm-view` 共用 `--amber-300` 装饰档;遮罩与两处阴影令牌化;Gate 2 为空;app.js/index.html/vendor 零改动;pytest 基线不下降。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 开发者 shell → `scripts/check-0*.sh` | 脚本读取 `frontend/style.css` 的**内容**并计数;文件内容不得被当作可执行输入(不得 `eval`、不得把文件内容拼进命令行) |
| `scripts/check-0*.sh` → 仓库工作树 | 脚本是**只读**的:不得写入或修改 `frontend/style.css`,不得 `git checkout`/`git reset` |
| `frontend/style.css` → 浏览器渲染 | 纯样式,无用户输入、无网络、无脚本执行面 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi04-01 | Tampering | `frontend/style.css` 的 `.hidden { display: none !important }` 机制 | high | mitigate | 本计划的三条守卫命令在**每个**任务里都跑:`check-03`(`^\.hidden {` == 1)与 `check-04`(`!important;` == 1)。`.hidden` 是 5 路单点故障(`#draft-empty` / `#rounds-hint` / `#btn-process-round` / `#round-switcher` / `#writing-hint` 只靠它隐藏),且三个 1-0-0 竞争者(`#selection-menu` / `#annotations-panel` / `#checks-panel`)靠 ID 特异性取胜 —— 弱化它会让这些容器常显。另:prohibition 明令禁止新增 `!important`、令牌化 `display`、使用 `:where()`。 |
| T-idi04-02 | Tampering | `#stream-banner.fatal` 与非致命态的区分 | high | mitigate | 禁止把 `.fatal` 折叠进共享 danger 令牌;两态(4.78:1 / 4.76:1)必须继续可区分。若折叠,「无法自动恢复,请刷新页面」会与「正在自动重连」视觉合一 —— 用户会按错误的方式处置断流。Task 2 的 acceptance_criteria 显式断言 `.fatal` 仍是独立选择器。 |
| T-idi04-03 | Elevation of Privilege | `#confirm-error` 的 G3 失败信息降级为灰色提示 | high | mitigate | Pitfall M6:`#confirm-error` 保留 **ID 选择器**(1-0-0),高于 `.hint`(0-1-0),并显式带 `var(--color-action-danger)`。改 class 会让胜者取决于源码顺序,后续任何 `.hint` 移动都会让 G3 确认失败信息退化 —— 那是 Core Value 红线路径上的唯一错误提示。 |
| T-idi04-04 | Information Disclosure | `app.js:4-75` 约 67 个顶层 `getElementById` 句柄 | high | mitigate | `app.js` / `index.html` 本阶段**零改动**,由 `git diff --name-only HEAD -- frontend/app.js frontend/index.html` 输出为空作为机械门。任何 id 改名/删除会在解析期静默杀死其下全部处理器(G-idi01-8),而本阶段根本不触碰这两个文件。 |
| T-idi04-05 | Denial of Service | `scripts/check-01-token-conformance.sh` 的 awk/grep 管道 | low | accept | 输入是本仓库自有的 633 行样式表,非不可信输入;正则 `#[0-9a-fA-F]\{3,6\}` 无嵌套量词,无回溯爆炸面。接受。 |
| T-idi04-06 | Spoofing | 三条守卫命令的 PASS/FAIL 输出被伪造(误报通过) | medium | mitigate | 每条命令必须**同时**用退出码与 stdout 判定;`grep -c` 在计数为 0 时退出码为 1,所以 CHECK-01 明确要求读 stdout 数值而非 grep 退出码(UI-SPEC 的算术陷阱条款)。verification 里同时跑独立于脚本的裸 `awk … | grep -c` 作为交叉校验。 |
| T-idi04-07 | Repudiation | 「渲染未变」被断言而非证明 | medium | mitigate | 本环境截图不可用、headless 渲染被挡,故**不规划视觉 diff**;改为具名人工 DevTools Computed 检查(每个任务至少一条)+ 机械的"app.js/index.html 零 diff"门。backstop 真值在无法确认时按 `human_needed` 上报,不静默判过。 |
| T-idi04-SC | Tampering | npm / pip / cargo 安装(供应链) | high | mitigate | **本阶段零安装**:D-06 禁止新增运行时依赖与构建步骤,四条校验命令必须是零依赖的 `grep` / `awk` / `python3`(均已在本机)。任何需要安装的写法是计划偏差与停止条件。无包管理器安装任务 ⇒ 无 `[ASSUMED]`/`[SUS]` 包需要合法性检查点。 |
</threat_model>

<verification>
**自动化门(每条都可独立运行,均须给出明确 PASS/FAIL):**

1. `bash scripts/check-01-token-conformance.sh` → PASS,围栏外裸 hex = 0
2. `bash scripts/check-03-hidden-uniqueness.sh` → PASS,`^\.hidden {` = 1
3. `bash scripts/check-04-important-count.sh` → PASS,`!important;` 声明数 = 1
4. Gate 2:`comm -23 <(grep -o 'var(--[a-z0-9-]*' frontend/style.css | sed 's/var(//' | sort -u) <(grep -o '\-\-[a-z0-9-]*:' frontend/style.css | sed 's/:$//' | sort -u)` → 输出为空
5. `node --check frontend/app.js` → 退出 0
6. `.venv/bin/python -m pytest -q` → 全绿
7. `git diff --name-only HEAD -- frontend/app.js frontend/index.html` → 输出为空
8. `git status --porcelain frontend/` → 只有 `frontend/style.css`
9. `ls frontend/vendor/` → 仅 `marked.min.js`

**pytest 基线说明(必须照实记录,不要照抄陈旧数字):** ROADMAP 与 REQUIREMENTS 写的基线是 **219**,但规划时对工作树实测 `pytest --collect-only -q` 收集到 **225** 条(quick `260917-fqh` 之后新增了用例)。**门必须按"通过数 ≥ 执行本计划前实测的收集数"判定,并在 SUMMARY 里记录实际数字**;照抄 219 会造出一个必然失败的假门 —— 这正是本里程碑反复警告的 gate 算术错误。若通过数少于改动前实测值,那才是回归。

**运行时验证(Pitfall M1:静态计数是补充不是替代,本计划每个任务都带一条):**
- 本环境截图不可用(headless 渲染被挡,且常驻 `/api/events` SSE 流使采集处理器无法终止)—— **不得规划视觉 diff**。
- 改为在运行中的应用里用 DevTools Computed 面板读具名选择器的具名属性(见各任务 `<human-check>`):`.hint` / `.badge-answered` 的 `color`、`#btn-authorize` 的三属性、`.kind-*` 的 `background-color`、`#ai-route-select` 的 `border-top-color`、`#state-badge` 的 `color` 与 `background-color`。
- 冻结轮次的 backstop 真值(琥珀 inset 竖线 + 轮次切换器 + 正文可读)只能人工确认;无法确认时按 `human_needed`(reason `insufficient_spec`)上报。

**渲染不变性(ROADMAP Phase 4 SC2):** 除 Deliberate Delta Ledger 记明的项(D-2…D-11、D-14、D-15)外,没有任何既有选择器改变位置、改名或增删声明。本计划的唯一新增规则是 Task 1 末尾追加的 `.annotation-answered` 后代规则(D-11 的落地形态,属 A11Y-04b 的刻意修复)。
</verification>

<success_criteria>
1. `frontend/style.css` 顶部存在**单一**围栏 `:root` 块,位置在 `* { box-sizing }` 之后、`html, body` 之前
2. 围栏外零裸 `#hex` —— CHECK-01 一条命令即可证明
3. 全部颜色字面量替换为 `var()`,tier-1 primitive 名不出现在围栏之外(TOKEN-02 硬不变量)
4. A11Y-04 的文本对比度失败项全部修复;`.hint` 2.73:1 → 5.18:1 且取的是**每个背景上都通过的最浅值** `#6a6a6a`
5. A11Y-04b 的 `.annotation-answered` 1.88:1 已修复;`.tier-desc` 被裁定保留
6. `#confirm-error` 的 ID 与错误色都保留(Pitfall M6)
7. `.hidden` 仍是全站唯一一条 `!important` 声明;`^\.hidden {` 仍恰好 1 处
8. CHECK-01 / CHECK-03 / CHECK-04 三条命令可独立运行,各自给出明确的通过/失败结论
9. `app.js` / `index.html` 零改动;`frontend/vendor/` 仍只有 `marked.min.js`;pytest 基线不下降
</success_criteria>

## Artifacts this phase produces

**本阶段(Phase 4)新建的全部符号 —— 供 plan-review-convergence 的 source-grounding pass 排除"新符号漂移"误报。** 本计划产出其中带 ✅ 的部分;无标记者由 Plan 02 / Plan 03 产出。

**新增文件路径(4 个):**

| 路径 | 产出计划 | 说明 |
|---|---|---|
| ✅ `scripts/check-01-token-conformance.sh` | Plan 01 | CHECK-01,零依赖 bash |
| ✅ `scripts/check-03-hidden-uniqueness.sh` | Plan 01 | CHECK-03,零依赖 bash |
| ✅ `scripts/check-04-important-count.sh` | Plan 01 | CHECK-04,零依赖 bash |
| `scripts/check-02-contrast.py` | Plan 03 | CHECK-02,零依赖 python3 |

**新增 CLI 调用(4 条,均从仓库根目录运行):**

| 命令 | 产出计划 |
|---|---|
| ✅ `bash scripts/check-01-token-conformance.sh` | Plan 01 |
| ✅ `bash scripts/check-03-hidden-uniqueness.sh` | Plan 01 |
| ✅ `bash scripts/check-04-important-count.sh` | Plan 01 |
| `python3 scripts/check-02-contrast.py` | Plan 03 |

**`frontend/style.css` 围栏 `:root` 块内新增的 CSS 自定义属性 —— 颜色部分(本计划产出,共 75 个):**

tier-1 primitive(25):`--white` `--black` `--gray-900` `--gray-700` `--gray-600` `--gray-500` `--gray-300` `--gray-100` `--gray-50` `--gray-25` `--green-800` `--green-700` `--green-100` `--blue-700` `--blue-100` `--blue-50` `--amber-800` `--amber-300` `--amber-100` `--amber-50` `--amber-25` `--red-600` `--red-200` `--red-50` `--purple-600`

tier-2 文本/表面/边框(26):`--color-text` `--color-text-secondary` `--color-text-muted` `--color-text-inverse` `--color-surface` `--color-surface-page` `--color-surface-sunken` `--color-surface-hover` `--color-surface-info` `--color-surface-warning` `--color-surface-warning-subtle` `--color-surface-mark` `--color-surface-danger` `--color-surface-streaming` `--color-border-strong` `--color-border` `--color-border-subtle` `--color-border-warning-subtle` `--color-border-success` `--color-border-streaming` `--color-border-danger-subtle` `--color-surface-info-strong` `--color-text-info` `--color-overlay-backdrop` `--shadow-overlay` `--shadow-menu`

tier-2 动作(15):`--color-action-primary` `--color-action-primary-fg` `--color-action-danger` `--color-action-danger-fg` `--color-action-warning` `--color-action-warning-surface` `--color-action-routine` `--color-action-routine-surface` `--color-action-routine-fg` `--color-action-commit` `--color-action-commit-surface` `--color-action-commit-fg` `--color-action-irreversible` `--color-action-irreversible-surface` `--color-action-irreversible-fg`

tier-2 事件类别(9):`--color-kind-say` `--color-kind-read` `--color-kind-write` `--color-kind-command` `--color-kind-result` `--color-kind-error` `--color-kind-done` `--color-kind-default` `--color-kind-fg`

**`frontend/style.css` 新增的围栏注释行(2):** `/* ===== DESIGN TOKENS: START ===== */`、`/* ===== DESIGN TOKENS: END ===== */`

**新增/变更的选择器(仅 2 处,均在 ledger 记明):**

| 选择器 | 计划 | 性质 |
|---|---|---|
| ✅ `.annotation-answered .annotation-note, .annotation-answered .annotation-quote, .annotation-answered .annotation-answer summary` | Plan 01 | **新增规则**(D-11 的落地形态) |
| `button, input, select` | Plan 02 | **新增规则**(D-19 / note N-4,追加在文件末尾) |

**新增字面量例外(0 个):** 本计划不引入任何新例外。L-1(`@media` 断点)是 Phase 6;L-3(两个 `--icon-*` data-URI)是 Phase 5;L-4(`--sidebar-w: 420px`)在 Plan 02;L-5(`right: 448px`)保持不动。
</verification>

## Flagged Assumptions (spec-less probe fallback — 12 `unclassified` rows)

本阶段没有 SPEC.md,故 `EDGE_ABSENT=1` / `PROHIB_ABSENT=1`,确定性 edge probe 已对 14 个阶段需求 ID 跑过。**探针共 surfaced 16 项,16 项全部有归宿(no-silent-drop 等式成立):**

- **4 项**(A11Y-04 / A11Y-04b 各一条 `boundary` + 一条 `precision`)**已被显式解决**,写成 `must_haves.truths` 的**普通字符串**(不是 backstop 标记):
  - A11Y-04 `boundary` → Plan 01 真值「AA 阈值边界(显式)」
  - A11Y-04 `precision` → Plan 01 真值「对比度计算的精度契约(显式)」
  - A11Y-04b `boundary` → Plan 02 真值「A11Y-04b 阈值边界(显式)」
  - A11Y-04b `precision` → Plan 02 真值「A11Y-04b 精度契约(显式)」
  UI-SPEC 的 `## Contrast Verification` 段给了具体数字(精确比值、精确令牌对、精确阈值),故按规则优先取 `explicit` 而非 `backstop`。
- **12 项 `unclassified` 行保持 `unresolved`,在此逐条列为显式 flagged assumption**(规则:#1110 —— `unclassified` 行**绝不**自动解决,连 `backstop` 都不行;也绝不自动驳回)。这 12 行的探针理由一律是 "unclassified — review manually":探针无法把 TOKEN-* / CHECK-* 归入它已知的边界/精度/规模类别,因为它们是**契约类**需求(令牌化与静态校验),不是边界算术类需求。

| # | 需求 ID | 探针类别 | 状态 | 归宿(显式 flagged assumption) |
|---|---|---|---|---|
| 1 | TOKEN-01 | unclassified | unresolved | 令牌块**唯一性**由人工审阅保证 —— 机械门只能证明"围栏外零 hex"与"`var()` 全部可解析",证明不了"全文件只有一个 `:root` 块"。Plan 01 的 acceptance_criteria 断言两行围栏注释各恰好 1 次,这是最近似的机械替代,但**不等于**唯一性证明。 |
| 2 | TOKEN-02 | unclassified | unresolved | 硬不变量"tier-1 primitive 名不出现在围栏之外"由 Plan 01 的一条 grep 近似覆盖,但 grep 只覆盖已列出的属性名清单(background / color / border* / box-shadow),`filter` / `fill` / `outline` 等属性上的 primitive 名不会被它抓到。**近似,非证明。** |
| 3 | TOKEN-03 | unclassified | unresolved | "先产出含义清单再收敛强调色"是一个**顺序性/过程性**主张,无法由任何命令验证 —— UI-SPEC 的 `### Meaning inventory` 已产出该清单(30 行),本阶段消费它;但"清单先于令牌"这一时序无法机械复验。 |
| 4 | TOKEN-04 | unclassified | unresolved | 探针未把"零裸 hex"识别为边界项。CHECK-01 覆盖**围栏外**;`var(--x, #fallback)` 形式的回退 hex 在围栏外对 CHECK-01 **隐形** —— 该风险由 prohibition(禁止 fallback)与 Gate 2 兜住,不是探针类别内的边界。 |
| 5 | TOKEN-05 | unclassified | unresolved | 间距刻度的边界不是数值边界而是**覆盖完整性**:14 padding / 11 margin / 5 gap 是否真的全部迁移,机械计数只能给近似(≥ 34 处消费点),`padding: 0` / 简写展开等形态可能漏计。 |
| 6 | TOKEN-06 | unclassified | unresolved | 同 TOKEN-05:8 个圆角值 → 3 档的映射完整性靠人工审阅,`border-bottom-right-radius` / `border-bottom-left-radius` 这类长写形态是已知的漏计面(Plan 02 的 action 已显式列出这两处)。 |
| 7 | TOKEN-07 | unclassified | unresolved | 序关系断言是**注释文本**,不是可执行约束 —— 没有任何机制阻止未来改号。探针无法为"注释里的断言"构造边界用例。 |
| 8 | TOKEN-08 | unclassified | unresolved | 字号刻度的边界是"是否有未声明的字号档被使用" —— Plan 02 用 `grep -cE 'font-size: [0-9.]+px'` == 0 近似覆盖,但 `font: 13px/1.6 …` 简写形态会漏计(本文件当前无此形态)。 |
| 9 | CHECK-01 | unclassified | unresolved | 校验命令**自身**的正确性不在探针类别内:一条永远打印 PASS 的脚本也能让门变绿。Plan 03 Task 2 的失败方向实证是这一行的实际归宿,但它是对命令的实证,不是对需求的边界分析。 |
| 10 | CHECK-02 | unclassified | unresolved | 同 CHECK-01:对比度引擎的**实现正确性**(sRGB 反伽马、通道权重、α 合成顺序)由 Plan 03 的精度契约真值约束,并由"改回 `#767676` 即变红"的实测反证;探针未给出此类"实现正确性"类别。 |
| 11 | CHECK-03 | unclassified | unresolved | `.hidden` 唯一性的**充分性**未证:计数 1 不等于"该规则仍然赢下级联"。三个 1-0-0 竞争者与 5 个只靠它隐藏的元素必须在浏览器里实检(ROADMAP SC4 明说"实检,不靠读 CSS")。Plan 01/02 的 `<human-check>` 是最近似的替代,但本环境的 headless 渲染被挡,该实检只能人工完成。 |
| 12 | CHECK-04 | unclassified | unresolved | `!important` **声明数** == 1 的计数口径是已知陷阱(`grep -c '!important'` 返回 3,其中 2 行是 L13-16 注释散文)。Plan 01 的 verify 同时打印三个数字(1 / 1 / 3)以证明口径正确,但"声明数"与"命中行数"的区分在其它属性上仍是人工判断。 |

**这 12 条不阻塞本阶段** —— 它们是探针在无法分类时按规则必须显式浮出的审阅项,而不是未覆盖的需求:每一条在对应的计划里都有至少一项机械或人工的近似验证(见上表"归宿"列)。**没有一条被静默丢弃。**

---

## Multi-Source Coverage Audit

**源类型与来源(本阶段无 CONTEXT.md、无 RESEARCH.md、无 SPEC.md —— 规划上下文明确声明它们缺席,故这四类中只有 GOAL 与 REQ 有实体):**

| 源 | 是否存在 | 实体 |
|---|---|---|
| **GOAL**(ROADMAP phase goal) | ✅ | `.planning/ROADMAP.md` Phase 4 的 `**Goal**` 段 + 5 条 Success Criteria + `**Gates**` 段 |
| **REQ**(phase_req_ids) | ✅ | TOKEN-01…08、CHECK-01…04、A11Y-04、A11Y-04b(14 条,`REQUIREMENTS.md` 逐条有正文) |
| **RESEARCH** | ✖ 缺席 | `workflow.research=false`;规划上下文声明 RESEARCH.md 不存在 |
| **CONTEXT**(D-XX 决策) | ✖ 缺席 | 未跑 `/gsd-discuss-phase`;UI-SPEC 的 `## Design Decisions`(Q1–Q7)与 `## Sign-Off Items`(S-1–S-4)承载了 CONTEXT.md 通常会持有的设计决策 |

**REQ 覆盖(14/14,无 MISSING):**

| 需求 | 归属计划 | 覆盖方式 |
|---|---|---|
| TOKEN-01 | 01 | 围栏 `:root` 块落地(Plan 01 Task 1) |
| TOKEN-02 | 01 | 两层分类学 + primitive 名不出围栏(Plan 01,`must_haves.truths` + prohibition) |
| TOKEN-03 | 01 | 消费 UI-SPEC 的 `### Meaning inventory`(30 行)并把四套竞争强调色收敛为 routine / commit / irreversible / primary / warning / danger 六族 |
| TOKEN-04 | 01 | CHECK-01 围栏外零裸 hex(117 → 0) |
| TOKEN-05 | 02 | 间距 12 档 + 14 padding / 11 margin / 5 gap 全替换(S-1 已批准) |
| TOKEN-06 | 02 | 圆角 3 档 + 8 个圆角值全归入 |
| TOKEN-07 | 02 | `--z-*` 4 档 + 块内序关系断言注释 |
| TOKEN-08 | 02 | 字号 6 档 + 7 个字号值全替换,12.5px 折叠(S-2 已批准) |
| CHECK-01 | 01 | `scripts/check-01-token-conformance.sh` |
| CHECK-02 | 03 | `scripts/check-02-contrast.py` + 围栏内 PAIR 清单 |
| CHECK-03 | 01 | `scripts/check-03-hidden-uniqueness.sh` |
| CHECK-04 | 01 | `scripts/check-04-important-count.sh`(按 `!important;` 声明计数) |
| A11Y-04 | 01(+03 校验) | 20 条文本失败声明全部修复,AA 值在声明处选定;CHECK-02 逐对验证 |
| A11Y-04b | 01 + 02(+03 校验) | `.annotation-answered` 0.65 删除(Plan 01)、`#round-doc.round-frozen` 0.55 删除 + 结构性标记(Plan 02)、`.tier-desc` 与归档态裁定保留、8 处 `:disabled` 豁免;CHECK-02 覆盖两条 α 合成对 |

**GOAL 覆盖(ROADMAP Phase 4 的 5 条 Success Criteria):**

| SC | 判据 | 归属 | 覆盖方式 |
|---|---|---|---|
| SC1 | 单一 `:root` 令牌块,块外零裸 `#hex`,CHECK-01 一条命令即可证明 | 01 | Plan 01 Task 1 的 tracer verify + Task 3 的终局门 |
| SC2 | 除刻意对比度修复外渲染与迁移前一致(纯值替换) | 01 + 02 | 每个 `<action>` 的"只改值、不重排、不增删其它声明"条款 + Deliberate Delta Ledger 作为**封闭清单** + `git diff` 面积检查 + DevTools Computed 抽验 |
| SC3 | 闸门说明文字仍比主正文次要,且自身达 AA(层级与比值一起校验) | 01 | `--gray-600` 取**最浅的通过值**(0.311 的 hint/正文比);CHECK-02 的 `--color-text-muted` 四条背景对 |
| SC4 | `.hidden` 仍是全站唯一 `!important` 声明;五个只依赖它的元素仍正确隐藏(实检) | 01 + 02 | CHECK-03/04 在每个任务里跑;浏览器实检见 flagged assumption #11(本环境只能人工) |
| SC5 | CHECK-01/02/03/04 可独立运行,各自给出明确通过/失败结论 | 03 | Plan 03 Task 2 的四组失败方向实证 |

**RESEARCH / CONTEXT 源:** 缺席,故无未覆盖项。UI-SPEC 的 Q1–Q7 与 S-1–S-4 已按用户签核(四项全批)全部落入 Plan 01 / 02 的 `<action>` 与 `must_haves.truths`。

**Exclusions(非缺口,不计入未覆盖):** `## Not in v1.14` 表的全部条目(`#probe-controls` 移除、暗色模式、两处 `window.prompt`、响应式系统、完整 ARIA、焦点陷阱、其余弹窗的 `role`、组件令牌层、lint 流水线、图标库、骨架屏、动效系统、Storybook、markdown 标题层级、装饰性分隔线加深);UI-SPEC `## UI Considerations` 的 13 条 `overflow` 项(显式延后到 Phase 6);61 条 dismissed 项(纯值重构不引入新状态)。

**UI Considerations 提升(无静默丢弃):** 4 条 resolved(explicit)分别落入 Plan 01(E5 `#annotation-list`、E6 `#checks-panel`、E12 inline error)与 Plan 02(E8 `#doc-pane`/`#round-doc`)的 `must_haves.truths`;1 条 backstop(E8 `long-text`)写成结构化 flat-scalar 标记 `{ statement, verification: backstop }`,同时出现在 Plan 01 与 Plan 02 的 `must_haves.truths` 中;13 条 deferred **显式记为延后到 Phase 6**,不丢弃。

---

<output>
Create `.planning/phases/idi-04-tokens-contract/idi-04-01-SUMMARY.md` when done
</output>
---
phase: idi-04
plan: 02
type: execute
wave: 2
depends_on:
  - idi-04-01
files_modified:
  - frontend/style.css
autonomous: true
requirements:
  - TOKEN-05
  - TOKEN-06
  - TOKEN-07
  - TOKEN-08
  - A11Y-04b

estimate:
  tokens: 85000
  raw_tokens: 85000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "`--space-*` 刻度共 **12 档**全部声明且全部被消费:`--space-px` 1px、`--space-half` 2px、`--space-1` 4px、`--space-1-5` 6px、`--space-2` 8px、`--space-2-5` 10px、`--space-3` 12px、`--space-3-5` 14px、`--space-4` 16px、`--space-6` 24px、`--space-8` 32px、`--space-10` 40px。`--space-0` / `--space-5` / `--space-7` **不声明**。**S-1 已由用户批准:** 保留 5 个半步档(1/2/6/10/14),TOKEN-05 字面的七个 4 倍数档是**子集而非上限**;理由:Phase 4 SC2 禁止渲染变化,而 6/10/14px 今天物理存在。**不执行**「删除半步档并把 6→8 / 10→12 / 14→16 压平」的一行替代方案。← TOKEN-05"
    - "全部 14 个 padding / 11 个 margin / 5 个 gap 值落到已声明档位;仅 6 组吸附变更(其余是纯替换),最大 4px:`3px→--space-1`(`.verdict-card p` margin-y)、`5px→--space-1`(`.verdict-note-input` padding-y)、`18px→--space-4`(`#btn-approve-draft` / `#authorize-row` / `#writing-view` 的 `margin-top` 与 `.markdown-body h1,h2,h3` 的 `margin-top`)、`18px→--space-4`(`#btn-approve-draft` / `#btn-authorize` / `#btn-start-writing` 的 padding-x)、`28px→--space-6`(`.overlay-card` padding-y)、`22px→--space-6`(`#brainstorm-view` 的 `margin-top` 与 `.markdown-body ul, ol` 的 `padding-left`)← TOKEN-05 / ledger D-16"
    - "字号刻度 **6 档**全部整数、全部消费:`--text-xs` 11px、`--text-sm` 12px、`--text-base` 13px、`--text-md` 14px、`--text-lg` 15px、`--text-xl` 16px;`12.5px` 的 3 处(`.markdown-body code` / `.verdict-note-input` / `.verdict-buttons button`)全部折叠到 `--text-base`(13px);**`14px` 保留为一等档**(7 档而非字面 6 档)。**S-2 已由用户批准:** ROADMAP Phase 5 SC5 与 Phase 6 SC5 都断言 `#brainstorm-view h2` 计算为 14px,`.markdown-body` 正文也是 14px,删除会同时打破两个下游门。**不执行**「把 `.markdown-body` / `.overlay-card p` / `#confirmation-modal input` 改 15px、`.panel-header h2` 改 13px」的一行替代方案。← TOKEN-08"
    - "字重只有 **2 档**且都被消费:`--fw-regular: 400`、`--fw-semibold: 600`;**`--fw-medium: 500` 不声明**(基线 font-weight 只有 600 ×12 与 400 ×1,声明一个不消费的令牌就是换个好名字的第二个字面量)。行高 **3 档**全部消费:`--lh-tight: 1.35`、`--lh-compact: 1.6`、`--lh-reading: 1.75` ← TOKEN-08 / TYPE-03 / UI-SPEC Q4"
    - "圆角刻度 **3 值**,8 个既有圆角值全部归入:`--radius-sm: 4px`(控件)、`--radius-md: 8px`(卡片、菜单)、`--radius-pill: 999px`(徽标)。吸附:`2px` / `3px` → `--radius-sm`;`6px` ×4 → `--radius-md`(+2px);`9px` / `12px` ×2 / `10px`(`#pending-count`)→ `--radius-pill`;`10px`(`.chat-bubble`)→ `--radius-md`(−2px);`8px`(`.overlay-card`)与 `4px` ×12 不变 ← TOKEN-06 / ledger D-17"
    - "`z-index` 令牌化为 4 个 `--z-*`,且**序关系在块内注释中显式断言**:`--z-badge` 10 < `--z-banner` 20 < `--z-overlay` 100 < `--z-selection-menu` 200。`badge < banner` 这一关系对 b9664e0 FIX 2 承重(横幅必须压在状态徽标之上),未来任何反转它的改号必须被 review 拦下 ← TOKEN-07"
    - "`--sidebar-w: 420px` 声明且被 `#sidebar` 消费(`flex: 0 0 var(--sidebar-w)`);`#state-badge { right: 448px }` **保持不动**(它不是 hex 字面量,CHECK-01 是 hex 计数器;LAYOUT-01 是 Phase 6 的需求)← UI-SPEC Q5 / L-4 / L-5"
    - "`#round-doc.round-frozen` 的 `opacity: 0.55` 被**删除**,`filter: saturate(0.6)` 保留,并新增 `box-shadow: inset 3px 0 0 var(--color-action-warning)` 结构性只读标记。正文对比度 3.84:1 → **16.67:1**;标记本身 5.10:1 on `#fafafa`,过 3:1 非文本下限。**S-4 已由用户批准:** 删掉 `opacity` 才让 Phase 7 的焦点环在冻结轮内保持 **5.62:1**;路线 1(`opacity: 0.65`)会把环压到 **2.85:1**、低于 3:1 下限。**不执行**「设 `opacity: 0.65`、去掉结构性标记」的一行替代方案。`box-shadow` 不参与布局 ⇒ 零位移,纯重构判据成立。← A11Y-04b / ledger D-12"
    - "`#rounds-placeholder.archive-mode #round-doc { opacity: 0.75 }` **保持不变** —— 7.49:1 已过 AA,是终态只读视图,是应用内读已完成 DESIGN.md 的唯一途径,不得回归。**覆盖 ≠ 失败** ← UI-SPEC `opacity` rulings 表"
    - "**`opacity` 被禁用为文字弱化手段**:全站**不存在** `--opacity-deemphasized` 之类的统一乘数令牌 —— 一个 α 无法同时服务两个需求相反的状态(会把归档态从 0.75 往下压,并把未来每个弱化站点都挂到同一个乘数上)。文字弱化一律走 `--color-text-muted` ← A11Y-04b / UI-SPEC `### opacity rulings` 禁令条款"
    - "A11Y-04b 阈值边界(显式):合成是逐通道在 8 位 sRGB 空间做 `result = α·fg + (1−α)·bg` 并四舍五入到整数(`opacity` 的浏览器语义)。`#1a1a1a` 文字合成到 `#fafafa` 上:α=0.55 → `#7f7f7f` = **3.84:1 ✗**;α=0.60 → `#747474` = **4.48:1 ✗**;α=**0.61** → `#717171` = **4.68:1 ✓**(阈值恰在 0.61);α=0.65 → `#686868` = **5.34:1 ✓**;α=0.83 → `#404040` = 9.93:1。即「提高不透明度」在算术上**确实可行**;裁定改走路线 2 不是因为路线 1 不成立,而是因为路线 1 把 Phase 7 的焦点环压到 2.85:1。"
    - "A11Y-04b 精度契约(显式):冻结轮的裁定是**删除**而非调参 —— 因为 `opacity` 合成整棵子树(包括 Phase 7 的焦点环),任何 α 都要同时满足「文字 ≥4.5:1」与「环 ≥3:1」;实测 α=0.65 时环色 `#1f63bd` 合成到 `#6c98d2` = 2.85:1(失败),删除后环回到 5.62:1。归档态 α=0.75 下环为 3.44:1(通过)。三个存续情形全部过 3:1 非文本下限。"
    - statement: "在运行中的应用里打开一个历史(冻结)轮次,确认:①文档区左侧出现 3px 琥珀色 inset 竖线(Computed 的 `box-shadow` 含 `inset 3px 0 0 rgb(138, 101, 8)`);②轮次切换器显示该历史轮次;③正文计算样式可读(删除 opacity 后应为 16.67:1);④文档区没有任何横向位移(inset 阴影不参与布局)。本环境截图不可用、headless 渲染被挡,只能人工确认 —— 无法确认时按 `human_needed`(insufficient_spec)上报,绝不静默判过。渲染面在 Phase 5 收口 ← UI-SPEC UI-Considerations 行 `long-text` E8(backstop)"
      verification: backstop
  artifacts:
    - path: "frontend/style.css"
      provides: "间距/字号/字重/行高/圆角/z-index/布局 共 31 个新令牌 + 全部非颜色字面量替换 + 冻结轮结构性标记 + `button, input, select` 前景色规则"
      contains: "--space-1-5"
  key_links:
    - from: "frontend/style.css 的 padding / margin / gap 声明"
      to: ":root 块的 --space-* 刻度"
      via: "每个数值型间距值都落到一个已声明档位(纯替换 34 处 + 吸附 6 组)"
      pattern: "var\\(--space-"
    - from: "#round-doc.round-frozen 的 box-shadow"
      to: "--color-action-warning"
      via: "结构性只读标记复用「需要注意但不是错误」的琥珀语义(与 pending 徽标同色)"
      pattern: "inset 3px 0 0 var\\(--color-action-warning\\)"
    - from: "button, input, select 的前景色"
      to: "--color-text"
      via: "0-0-1 元素选择器,被 button.danger(0-1-1) / #btn-*(1-0-0) / .overlay-card button(0-1-1) 压制,只接管 UA 的 buttontext / fieldtext"
      pattern: "color: var\\(--color-text\\)"
  prohibitions:
    - "不得声明 `--text-2xl`(18px)与 `--text-3xl`(22px) —— 它们在 Phase 5 与 `.markdown-body h1/h2/h3` 的显式字号**同一次提交**落地;本阶段声明即违反「不得声明未消费的令牌」(Pitfall 1 推论)← UI-SPEC `## Typography` 末段"
    - "不得声明 `--icon-pin` / `--icon-location` —— 两个 data-URI SVG 令牌在 Phase 5 与其 `content:` 消费者同提交;本阶段声明即孤儿令牌 ← UI-SPEC Q7"
    - "不得声明 `--color-focus` —— 焦点环色在 Phase 7 与全局 `:focus-visible` 规则同提交 ← UI-SPEC `### Phase 7 consequence recorded now`"
    - "不得把 `--green-800` 接进任何选择器 —— 它是 Phase 5 对 `--color-action-irreversible` 的目的地,是 Pitfall 1 的唯一有界例外,本阶段对选择器不可见 ← note N-2"
    - "不得在媒体查询条件里用 `var()`(CSS 禁止,该规则会被静默丢弃);本阶段**不新增任何 `@media` 块** —— 唯一的 `@media` 守卫是 Phase 6 的 LAYOUT-02,其断点是唯一的合法字面量例外(L-1)← UI-SPEC Q5 / L-1"
    - "不得 tokenize 布局尺寸字面量(`top: 12px`、`right: 448px`、`max-width: 720px` / `420px` / `86%`、`min-width: 96px`、`min-height: 160px` / `320px`、`max-height: 40vh` / `55vh` / `32vh` / `30vh`、`flex: 0 0 48px`、`height: 100%` / `100vh`、`border-left: 3px`、`border: 2px solid`)—— TOKEN-05 的基线明确定义为 14 个 padding / 11 个 margin / 5 个 gap,布局尺寸属 LAYOUT-* 需求(Phase 6),本阶段纳入即范围蔓延 ← ROADMAP Phase 4 Deliverables / Pitfall 8"
    - "不得把冻结轮的只读信号退化为「只是变淡」 —— 删 `opacity` 的同时必须补上结构性标记,否则 D-P2-21 的「这轮只读」信号彻底消失 ← UI-SPEC S-4 裁定"
    - "不得静默回退冻结轮裁定(改回 `opacity: 0.65` 且不加标记)—— Phase 5 的 gate 必须复验冻结轮仍读得出「冻结」 ← UI-SPEC `### RULING` 末段"
    - "不得把任何内容排版写进全局 `h1,h2,h3` 规则 —— 会与四处 chrome 覆盖碰撞(`.panel-header h2` 14px、`#draft-view h2` 15px、`#brainstorm-view h2` 14px、`.overlay-card h3` 16px)。内容排版一律限定在 `.markdown-body` 下(本阶段只做字号值替换,不新增任何字号规则)← Pitfall M4 / TYPE-01"
    - "不得软化 8 处 `:disabled` 的 `opacity: 0.55` / `0.5` —— SC 1.4.3 豁免非活动组件,而 `:disabled` 是 G3 前提条件唯一的视觉信号 ← Pitfall M5"
---

<objective>
把 `frontend/style.css` 的**非颜色**字面量全部令牌化:间距(12 档)、字号(6 档)、字重(2 档)、行高(3 档)、圆角(3 档)、z-index(4 档)与侧栏宽度;落地 A11Y-04b 的冻结轮裁定与 note N-4 的前景色规则。

Purpose: 颜色是"看得见"的一半,间距 / 字号 / 圆角是另一半 —— 且它们是**后续阶段唯一的改动面**(Phase 5/6/7 的每个修复都是这些令牌的**值**改动)。没有这一层,Phase 5 的"不可逆动作独立处理"就得重写选择器而不是改一行值。

Output: 带 31 个新令牌的 `:root` 块;全部 padding / margin / gap / font-size / border-radius / z-index 替换为 `var()`;`#round-doc.round-frozen` 的结构性只读标记;文件末尾追加的 `button, input, select { color: var(--color-text) }`。

**用户签核记录(2026-09-17,已批准,不得重新讨论):** 本计划落地 **S-1**(间距 12 档,含 5 个半步)与 **S-4**(冻结轮改走结构性标记),两项均**照原文执行**,不执行其"一行替代方案";**S-2**(14px 保留为一等档)在本计划落地;**S-3**(控件边框)已由 Plan 01 落地。该批准的两处**持久记录**为:①`04-UI-SPEC.md` 的 `## Sign-Off Items`;②`.planning/STATE.md` 的 `### Blockers/Concerns` `[v1.14 P4]` 条目与 `## Operator Next Steps` 的 `S-1…S-4` 逐项清单(✅ 批准 2026-09-17,并记明四项的一行式替代方案**均不执行**)。签核不在本计划内自证 —— 本计划只**消费**该已决事项。

**无 `checkpoint:decision`:** S-1…S-4 已由用户在规划前批准,再设卡即重新审理已决事项。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md
@.planning/phases/idi-04-tokens-contract/idi-04-01-SUMMARY.md
@frontend/style.css
</context>

<tasks>

<task type="auto">
  <name>Task 1: 间距刻度 12 档 + 全部 padding / margin / gap 替换 + 侧栏宽度令牌</name>
  <files>frontend/style.css</files>
  <read_first>
    - frontend/style.css(读 Plan 01 之后的当前状态;围栏块与 `var(--` 已存在)
    - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md 的 `## Spacing Scale`(令牌表 + 命名规则 + 吸附 delta 表 + 两个 22px 站点说明)与 `## Sign-Off Items` 的 S-1
    - .planning/phases/idi-04-tokens-contract/idi-04-01-SUMMARY.md(Plan 01 实际落地的块内令牌清单与两处计划期裁定)
  </read_first>
  <action>
    1) 在 `:root` 块内**追加** 12 个间距令牌(全部在本任务被消费,零孤儿):`--space-px: 1px`、`--space-half: 2px`、`--space-1: 4px`、`--space-1-5: 6px`、`--space-2: 8px`、`--space-2-5: 10px`、`--space-3: 12px`、`--space-3-5: 14px`、`--space-4: 16px`、`--space-6: 24px`、`--space-8: 32px`、`--space-10: 40px`。命名规则:`--space-N` 的 N 是 px 值 ÷ 4。**不要声明** `--space-0`(`0` 是 reset,保留为字面量,例如 `margin: 0 0 var(--space-2)` 里的第一个 `0`)、`--space-5`(20px,无消费者)、`--space-7`(28px,无消费者)。

    2) 在块内**追加** `--sidebar-w: 420px`,并把 `#sidebar` 的 `flex: 0 0 420px` 改为 `flex: 0 0 var(--sidebar-w)`。**不要碰** `#state-badge { right: 448px }`(L-5;它不是 hex,CHECK-01 不管它;LAYOUT-01 是 Phase 6)。

    3) 替换全部间距字面量。**纯替换(值不变,只换成同名档位)**,逐条按值映射:32px 40px(`#doc-pane` padding)→ `--space-8` / `--space-10`;10px 16px(`.panel-header` padding)→ `--space-2-5` / `--space-4`;12px 16px(`.panel-body` padding)→ `--space-3` / `--space-4`;8px(gap 群:`#probe-controls` / `#enter-form` / `#chat-input-row` / `#check-controls` / `.verdict-buttons` / `.event-item` / `#latest-check` 的 gap 与 padding 等)→ `--space-2`;6px 6px(`#ai-route-select` padding)→ `--space-1-5`;6px 8px(`#project-path-input` / `#latest-check` padding)→ `--space-1-5` / `--space-2`;6px 10px(`button` padding)→ `--space-1-5` / `--space-2-5`;8px(`.event-list` padding)→ `--space-2`;6px(`.event-list` gap)→ `--space-1-5`;4px 6px(`.event-item` padding)→ `--space-1` / `--space-1-5`;1px 4px(`.event-kind` padding)→ `--space-px` / `--space-1`;8px 10px(输入框 padding 群)→ `--space-2` / `--space-2-5`;4px 12px(`#state-badge` / `#stream-banner` padding)→ `--space-1` / `--space-3`;8px 0(`.markdown-body p` margin)→ `--space-2`;2px 12px(`.markdown-body blockquote` padding)→ `--space-half` / `--space-3`;4px 10px(`.markdown-body th,td` padding)→ `--space-1` / `--space-2-5`;1px 4px(`.markdown-body code` padding)→ `--space-px` / `--space-1`;8px 12px(`.chat-bubble` padding)→ `--space-2` / `--space-3`;4px 2px(`#chat-messages` padding)→ `--space-1` / `--space-half`;10px(gap 群:`#chat-messages` / `#annotation-list` / `#verdict-cards`)→ `--space-2-5`;10px(`#chat-input-row` margin-top / `.overlay-card button` margin-top)→ `--space-2-5`;12px(gap 群:`.modal-buttons` / `.round-view-header`)→ `--space-3`;4px 8px(`#round-switcher` / `#check-switcher` padding)→ `--space-1` / `--space-2`;2px 10px(`#pending-count` padding)→ `--space-half` / `--space-2-5`;2px(`#annotation-list` padding)→ `--space-half`;8px 10px(`.annotation-item` padding)→ `--space-2` / `--space-2-5`;1px 8px(`.annotation-badge` padding)→ `--space-px` / `--space-2`;6px / 4px / 2px(`.annotation-*` 的 margin-top 群)→ `--space-1-5` / `--space-1` / `--space-half`;4px(`#selection-menu` padding)与 6px(其 gap)→ `--space-1` / `--space-1-5`;0 1px(`mark` padding)→ 保留 `0`,`1px` → `--space-px`;8px 16px(`#btn-divergence` / `#chat-input-row button` padding)→ `--space-2` / `--space-4`;8px 18px(三个 `#btn-*` 的 padding,18px 见下)→ `--space-2` / 吸附;10px 16px(`.tier-buttons button` padding)→ `--space-2-5` / `--space-4`;4px(`.tier-buttons button` gap)→ `--space-1`;10px 0 4px(`#confirmation-modal input` padding)→ `--space-2-5` / `0` / `--space-1`;4px 10px(`.verdict-buttons button` padding)→ `--space-1` / `--space-2-5`;8px 10px(`.verdict-card` padding)→ `--space-2` / `--space-2-5`;12px 14px(`#brainstorm-view` padding)→ `--space-3` / `--space-3-5`;6px 0 0(`.hint` margin-top 群)→ `--space-1-5` / `0` / `0`;14px(`#divergence-entry` margin-bottom)→ `--space-3-5`;16px(`#enter-form` margin-bottom / `#btn-*` margin-top)→ `--space-4`;0 0 8px(`#brainstorm-view h2` margin)→ `0` / `0` / `--space-2`;8px(`.markdown-body` 群 margin)→ `--space-2`。

    **吸附变更 6 组(值会变,全部在 ledger D-16 记明,最大 4px):** `3px → var(--space-1)`(`.verdict-card p` margin-y)、`5px → var(--space-1)`(`.verdict-note-input` padding-y)、`18px → var(--space-4)`(`#btn-approve-draft` / `#authorize-row` / `#writing-view` 的 `margin-top`,与 `.markdown-body h1,h2,h3` 的 `margin-top`)、`18px → var(--space-4)`(`#btn-approve-draft` / `#btn-authorize` / `#btn-start-writing` 的 padding-x)、`28px → var(--space-6)`(`.overlay-card` padding-y)、`22px → var(--space-6)`(`#brainstorm-view` 的 `margin-top` **与** `.markdown-body ul, .markdown-body ol` 的 `padding-left` —— 这两个站点此前**没有任何令牌目的地**,是本任务必须覆盖的)。

    **令牌化范围边界(必须遵守,否则范围蔓延):** TOKEN-05 的基线明确是 14 个 padding / 11 个 margin / 5 个 gap。`top: 12px`、`right: 448px`、`max-width: 720px` / `420px` / `86%`、`min-width: 96px`、`min-height: 160px` / `320px`、`max-height: 40vh` / `55vh` / `32vh` / `30vh`、`flex: 0 0 48px`、`height: 100%` / `100vh`、`border-left: 3px`、`border: 2px solid` 等**布局尺寸与边框宽度保持字面量** —— 它们是 LAYOUT-* 需求的领地(Phase 6),不属于本阶段的需求集合。

    **不要做:** 不要改任何颜色值(Plan 01 已完成);不要改任何 `font-size` / `border-radius` / `z-index`(Task 2);不要新增任何选择器;不要重排规则(只改值、只追加)。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh</automated>
    <fails_when>任一命令退出码非 0,或 stdout 出现 FAIL 字样(颜色迁移不得被本任务破坏)</fails_when>
    <automated>comm -23 <(grep -o 'var(--[a-z0-9-]*' frontend/style.css | sed 's/var(//' | sort -u) <(grep -o '\-\-[a-z0-9-]*:' frontend/style.css | sed 's/:$//' | sort -u)</automated>
    <fails_when>stdout 非空(存在未声明的 var() 消费 —— 新加的 --space-* / --sidebar-w 若拼错即在此暴露)</fails_when>
    <automated>grep -c 'var(--space-' frontend/style.css; grep -cE '\-\-space-(px|half|1|1-5|2|2-5|3|3-5|4|6|8|10):' frontend/style.css; grep -c 'var(--sidebar-w)' frontend/style.css</automated>
    <fails_when>第一行计数少于 34(间距消费点未铺开);第二行不是 12(间距档位不是 12 个);第三行不是 1(#sidebar 未消费 --sidebar-w)</fails_when>
    <automated>node --check frontend/app.js && git diff --name-only HEAD -- frontend/app.js frontend/index.html</automated>
    <fails_when>node 退出非 0,或第二条输出非空</fails_when>
    <human-check>在 DevTools Computed 面板读:`.panel-header` 的 `padding-top` == 10px、`padding-left` == 16px;`#doc-pane` 的 `padding-top` == 32px、`padding-left` == 40px;`button` 的 `padding-top` == 6px、`padding-left` == 10px;`.overlay-card` 的 `padding-top` == 24px(由 28px 吸附,本任务最大的位移);`#brainstorm-view` 的 `margin-top` == 24px。确认只有 D-16 记明的 6 组发生变化。</human-check>
  </verify>
  <acceptance_criteria>
    - `frontend/style.css` 含 12 个间距令牌声明,名称与值逐字为:`--space-px: 1px;` `--space-half: 2px;` `--space-1: 4px;` `--space-1-5: 6px;` `--space-2: 8px;` `--space-2-5: 10px;` `--space-3: 12px;` `--space-3-5: 14px;` `--space-4: 16px;` `--space-6: 24px;` `--space-8: 32px;` `--space-10: 40px;`
    - `frontend/style.css` 不含 `--space-0`、`--space-5`、`--space-7`
    - `frontend/style.css` 含 `--sidebar-w: 420px;`,且 `#sidebar` 规则体内为 `flex: 0 0 var(--sidebar-w);`
    - `grep -c 'var(--space-' frontend/style.css` 不小于 34
    - `frontend/style.css` 仍含 `right: 448px`(`#state-badge`,L-5,保持不动)
    - `frontend/style.css` 含 `padding-left: var(--space-6)` 于 `.markdown-body ul, .markdown-body ol` 规则内,且 `#brainstorm-view` 的 `margin-top` 为 `var(--space-6)`
    - `bash scripts/check-01-token-conformance.sh` 仍打印 PASS;Gate 2 输出为空
    - `node --check frontend/app.js` 退出 0;`git diff --name-only HEAD -- frontend/app.js frontend/index.html` 输出为空
  </acceptance_criteria>
  <done>12 个间距档位声明且全部被消费;`--sidebar-w` 被 `#sidebar` 消费;14 padding / 11 margin / 5 gap 全部落到档位;6 组吸附变更按 D-16 落地(含两个此前无令牌目的地的 22px 站点);布局尺寸字面量按范围边界保持不动;CHECK-01 仍为 PASS。</done>
</task>

<task type="auto">
  <name>Task 2: 字号 / 字重 / 行高 / 圆角 / z-index 刻度与全部替换</name>
  <files>frontend/style.css</files>
  <read_first>
    - frontend/style.css(读 Task 1 之后的当前状态)
    - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md 的 `## Typography`(角色表 + 权重/行高令牌 + 12.5px 折叠 + 作用域围栏)与 `## Sign-Off Items` 的 S-2
    - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md 的 `### Tier 2 — semantic` 的 radius 段与 "Radius deltas" 表、`--z-*` 段与 ordering assertion 段
  </read_first>
  <action>
    1) 在 `:root` 块内**追加**字号 6 档:`--text-xs: 11px`、`--text-sm: 12px`、`--text-base: 13px`、`--text-md: 14px`、`--text-lg: 15px`、`--text-xl: 16px`。**不要声明** `--text-2xl` / `--text-3xl`(Phase 5 与消费者同提交)。

    2) 追加字重 2 档:`--fw-regular: 400`、`--fw-semibold: 600`。**不要声明** `--fw-medium: 500`。

    3) 追加行高 3 档:`--lh-tight: 1.35`、`--lh-compact: 1.6`、`--lh-reading: 1.75`。

    4) 追加圆角 3 档:`--radius-sm: 4px`、`--radius-md: 8px`、`--radius-pill: 999px`。

    5) 追加 z-index 4 档:`--z-badge: 10`、`--z-banner: 20`、`--z-overlay: 100`、`--z-selection-menu: 200`,并在块内紧邻处写一行注释**显式断言序关系**:`--z-badge`(10) < `--z-banner`(20) < `--z-overlay`(100) < `--z-selection-menu`(200),并注明 `badge < banner` 对 b9664e0 FIX 2 承重(横幅必须压在状态徽标之上)。

    6) 替换全部字号字面量(**7 个不同值 → 6 档**):`font-size: 11px`(`.annotation-badge`)→ `var(--text-xs)`;`font-size: 12px` 共 6 处(`.event-kind` / `#state-badge` / `#stream-banner` / `#pending-count` / `.annotation-answer summary` / `.tier-desc`)→ `var(--text-sm)`;`font-size: 13px` 共 15 处(`.hint` / `.inline-error` / `#ai-route-select` / `#project-path-input` / `button` / `.event-item` / `#enter-form input` / `#chat-input-row input` / `#round-switcher` / `.annotation-item` / `.chat-bubble` / `#latest-check` / `#check-switcher` / `.markdown-body th,td` / `.verdict-card`)→ `var(--text-base)`;`font-size: 14px` 共 5 处(`.panel-header h2` / `.overlay-card p` / `.markdown-body` / `#confirmation-modal input` / `#brainstorm-view h2`)→ `var(--text-md)`(**S-2 已批准:14px 是一等档,不删除**);`font-size: 15px`(`#draft-view h2, #rounds-placeholder h2`)→ `var(--text-lg)`;`font-size: 16px`(`.overlay-card h3`)→ `var(--text-xl)`;**`font-size: 12.5px` 共 3 处**(`.markdown-body code` / `.verdict-note-input` / `.verdict-buttons button`)→ `var(--text-base)`(13px,本阶段唯一的字号值变更,D-1)。

    7) 替换全部字重与行高:`font-weight: 600`(12 处)→ `var(--fw-semibold)`;`font-weight: 400`(`.tier-desc`)→ `var(--fw-regular)`;`line-height: 1.75`(`.markdown-body`)→ `var(--lh-reading)`;`line-height: 1.6`(`.overlay-card p` / `.chat-bubble`)→ `var(--lh-compact)`;`line-height: 1.35`(`.markdown-body h1,h2,h3`)→ `var(--lh-tight)`。

    8) 替换全部圆角字面量(**8 个不同值 → 3 档**):`border-radius: 2px`(`mark` / `.chat-user` 的 `border-bottom-right-radius`)→ `var(--radius-sm)`;`border-radius: 3px`(`.event-kind` / `.markdown-body code`)→ `var(--radius-sm)`;`border-radius: 4px`(12 处)→ `var(--radius-sm)`;`border-radius: 6px`(4 处:`.annotation-item` / `#brainstorm-view` / `#selection-menu` / `.verdict-card`)→ `var(--radius-md)`;`border-radius: 8px`(`.overlay-card`)→ `var(--radius-md)`;`border-radius: 9px`(`.annotation-badge`)→ `var(--radius-pill)`;`border-radius: 10px`(`#pending-count`)→ `var(--radius-pill)`;`border-radius: 10px`(`.chat-bubble`)→ `var(--radius-md)`;`border-radius: 12px`(`#state-badge` / `#stream-banner`)→ `var(--radius-pill)`;`.chat-ai` 的 `border-bottom-left-radius: 2px` → `var(--radius-sm)`。

    9) 替换 4 个 z-index:`z-index: 100`(`.overlay`)→ `var(--z-overlay)`;`z-index: 10`(`#state-badge`)→ `var(--z-badge)`;`z-index: 20`(`#stream-banner`)→ `var(--z-banner)`;`z-index: 200`(`#selection-menu`)→ `var(--z-selection-menu)`。**不要改动 `#stream-banner` 上方那条注释里对 z-index 关系的说明**(它是对的)。

    **不要做:** 不要新增任何字号规则(尤其不要写全局 `h1,h2,h3` —— 会与四处 chrome 覆盖碰撞);不要改颜色或间距(Plan 01 / Task 1);不要声明 Phase 5 的 `--text-2xl` / `--text-3xl` / `--icon-*` 或 Phase 7 的 `--color-focus`;不要重排规则。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh</automated>
    <fails_when>任一命令退出码非 0,或 stdout 出现 FAIL 字样</fails_when>
    <automated>grep -cE 'font-size: [0-9.]+px' frontend/style.css; grep -c 'font-size: var(--text-' frontend/style.css; grep -cE 'border-radius: [0-9]+px' frontend/style.css; grep -c 'border-radius: var(--radius-' frontend/style.css; grep -cE 'radius: [0-9]+px' frontend/style.css; grep -cE 'radius: var\(--radius-' frontend/style.css; grep -cE 'z-index: [0-9]+' frontend/style.css; grep -c 'z-index: var(--z-' frontend/style.css</automated>
    <fails_when>第 1 / 3 / 5 / 7 行的裸字面量计数任一非 0(仍有未替换的字号 / 圆角 / z-index);或第 5 行(`grep -cE 'radius: [0-9]+px'`)非 0 —— **这一行是本任务唯一能看见两个长写圆角的探针**:`style.css:334` 的 `border-bottom-right-radius: 2px` 与 `style.css:339` 的 `border-bottom-left-radius: 2px` 不含子串 `border-radius:`,所以第 3 行的探针对它们**隐形**;或偶数行计数低于该族期望消费点(字号 30 处、`border-radius:` shorthand 25 处、圆角**全部形态** 27 处、z-index 4 处)</fails_when>
    <automated>comm -23 <(grep -o 'var(--[a-z0-9-]*' frontend/style.css | sed 's/var(//' | sort -u) <(grep -o '\-\-[a-z0-9-]*:' frontend/style.css | sed 's/:$//' | sort -u); node --check frontend/app.js</automated>
    <fails_when>第一条输出非空(存在未声明的 var() 消费),或 node 退出码非 0</fails_when>
    <human-check>在 DevTools Computed 面板读:`#brainstorm-view h2` 的 `font-size` == 14px、`color` == rgb(138, 101, 8)(这条是 ROADMAP Phase 5 SC5 / Phase 6 SC5 的下游门,必须在 Phase 4 结束时仍成立);`#draft-view h2` 的 `font-size` == 15px;`.panel-header h2` 的 `font-size` == 14px;`.overlay-card h3` 的 `font-size` == 16px;`.markdown-body` 的 `font-size` == 14px;`.markdown-body code` 的 `font-size` == 13px(由 12.5px 折叠);`#selection-menu` 的 `z-index` == 200、`#state-badge` == 10、`#stream-banner` == 20。</human-check>
  </verify>
  <acceptance_criteria>
    - `frontend/style.css` 含 `--text-xs: 11px;` `--text-sm: 12px;` `--text-base: 13px;` `--text-md: 14px;` `--text-lg: 15px;` `--text-xl: 16px;` 六个声明
    - `frontend/style.css` 含 `--fw-regular: 400;` 与 `--fw-semibold: 600;`,**不含** `--fw-medium`
    - `frontend/style.css` 含 `--lh-tight: 1.35;` `--lh-compact: 1.6;` `--lh-reading: 1.75;`
    - `frontend/style.css` 含 `--radius-sm: 4px;` `--radius-md: 8px;` `--radius-pill: 999px;`
    - `frontend/style.css` 含 `--z-badge: 10;` `--z-banner: 20;` `--z-overlay: 100;` `--z-selection-menu: 200;`,且块内有一行注释同时出现 10 / 20 / 100 / 200 与 badge / banner 字样(序关系断言)
    - `grep -cE 'font-size: [0-9.]+px' frontend/style.css` 输出 0;`grep -c 'font-size: var(--text-' frontend/style.css` 不小于 30
    - `grep -cE 'border-radius: [0-9]+px' frontend/style.css` 输出 0;`grep -c 'border-radius: var(--radius-' frontend/style.css` 输出 25;`grep -cE 'radius: [0-9]+px' frontend/style.css` 输出 0;`grep -cE 'radius: var\(--radius-' frontend/style.css` 输出 27
    - `grep -cE 'z-index: [0-9]+' frontend/style.css` 输出 0;`grep -c 'z-index: var(--z-' frontend/style.css` 输出 4
    - `frontend/style.css` 不含 `12.5px`
    - `frontend/style.css` 不含全局 `h1, h2, h3 {` 或 `h1,h2,h3 {` 规则(内容排版未越出 `.markdown-body`)
    - `frontend/style.css` 不含 `--text-2xl`、`--text-3xl`、`--icon-pin`、`--icon-location`、`--color-focus`
    - `frontend/style.css` 不含 `@media`
    - `comm -23 <(...var(...)...) <(...--...:...)>` 输出为空;`node --check frontend/app.js` 退出 0
  </acceptance_criteria>
  <done>6 档字号 / 2 档字重 / 3 档行高 / 3 档圆角 / 4 档 z-index 全部声明且全部被消费;7 个字号值、8 个圆角值、4 个 z-index 值全部替换(12.5px 折叠为 13px);序关系断言写入块内注释;`#brainstorm-view h2` 仍计算为 14px / rgb(138,101,8);Phase 5/6/7 的令牌未被提前声明。</done>
</task>

<task type="auto">
  <name>Task 3: 冻结轮结构性标记(S-4)、N-4 前景色规则与全文件收尾</name>
  <files>frontend/style.css</files>
  <read_first>
    - frontend/style.css(读 Task 2 之后的当前状态)
    - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md 的 `### RULING: #round-doc.round-frozen — the genuine design conflict`(全文,含 α 阈值表与路线 1 的代价)与 `## Sign-Off Items` 的 S-4
    - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md 的 `### Notes N-1 … N-4` 中的 N-4、`## Deliberate Delta Ledger`(D-11 / D-12 / D-19)
  </read_first>
  <action>
    1) **S-4 已批准 —— 冻结轮裁定落地。** 把 `#round-doc.round-frozen` 的规则体从 `{ opacity: 0.55; filter: saturate(0.6); }` 改为 `{ filter: saturate(0.6); box-shadow: inset 3px 0 0 var(--color-action-warning); }`。要点:
    - `opacity: 0.55` **删除**(不是调参)。正文对比度 3.84:1 → 16.67:1。
    - `filter: saturate(0.6)` **保留** —— 去饱和传达"不活跃"而不动亮度,因而文字对比度不受影响。
    - `box-shadow: inset` 是**零布局位移**的标记(`box-shadow` 不参与布局,没有选择器位移、没有宽度变化,"纯重构"判据因此成立)。**不要**用 `border-left` —— 那会加 3px 宽度并推移每个冻结轮的文字,已明确否决。
    - 标记色用 `--color-action-warning`(与 pending 徽标同一个"需要注意但不是错误"的琥珀)。非文本状态指示器,5.10:1 on `#fafafa`,过 SC 1.4.11 的 3:1 下限。
    - 更新该规则上方的注释:说明"只读"信号现在由去饱和 + 结构性琥珀竖线承载,并记下为什么删 `opacity`(它合成整棵子树,包括 Phase 7 的焦点环)。

    2) **`#rounds-placeholder.archive-mode #round-doc { opacity: 0.75 }` 保持原样** —— 7.49:1 已过 AA,是应用内读已完成 DESIGN.md 的唯一途径,不得回归。

    3) **N-4 已记明 —— 文件末尾追加**(绝不插入、绝不重排)一条规则:`button, input, select { color: var(--color-text); }`。理由:今天每个按钮与输入框的前景色来自 UA(`buttontext` / `fieldtext`,即 `#000`),这是令牌块**之外**的第二事实源 —— 正是本阶段要消除的东西,且是 Phase 7 的阻碍(对 UA 着色的控件做 `background-color` 过渡是不自洽的)。元素选择器特异性 0-0-1,所以 `button.danger`(0-1-1)、`#btn-*`(1-0-0)、`.overlay-card button`(0-1-1)全部仍然取胜。视觉 delta:`#000` → `#1a1a1a`,不可感知。

    4) **全文件收尾自检**(这是本阶段的终局状态):
    - `bash scripts/check-01-token-conformance.sh` → PASS(围栏外 0 裸 hex)
    - Gate 2(`comm -23 …`)→ 空(每个 `var(--x)` 都解析到已声明的 `--x`)
    - **孤儿令牌扫描**:块内每个 `--*` 声明都必须被至少一个 `var(--…)` 消费,唯一例外是 `--green-800`(note N-2 的有界例外,Phase 5 的目的地)。用 `grep -o '\-\-[a-z0-9-]*:' frontend/style.css` 与 `grep -o 'var(--[a-z0-9-]*' frontend/style.css` 做**反向**差集核对;若有其它孤儿,把它接进正确的消费者或删除该声明 —— **绝不留下未消费的令牌**。
    - `grep -c '^\.hidden {'` == 1;`grep -c '!important;'` == 1
    - `git diff --name-only HEAD -- frontend/app.js frontend/index.html` 为空;`git status --porcelain frontend/` 只有 `frontend/style.css`;`ls frontend/vendor/` 仅 `marked.min.js`
    - `node --check frontend/app.js` 退出 0;`.venv/bin/python -m pytest -q` 全绿

    **不要做:** 不要为冻结轮改用 `opacity: 0.65`(那是 S-4 的一行替代方案,已明确不执行);不要给归档态加任何标记或改任何值;不要新增第三条规则(本阶段新增的规则只有 Plan 01 的 `.annotation-answered` 后代规则与本次的 `button, input, select`,共 2 条);不要重排任何既有规则。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh</automated>
    <fails_when>任一命令退出码非 0,或 stdout 出现 FAIL 字样</fails_when>
    <automated>grep -n 'opacity' frontend/style.css</automated>
    <fails_when>输出中出现 `#round-doc.round-frozen` 规则体内的 opacity,或 `.annotation-answered` 的 opacity;期望只剩 8 处 :disabled 的 opacity、.tier-desc 的 0.8、以及归档态的 0.75</fails_when>
    <automated>grep -c 'opacity: 0.55' frontend/style.css; grep -c 'opacity: 0.5;' frontend/style.css; grep -c 'opacity: 0.8' frontend/style.css; grep -c 'opacity: 0.75' frontend/style.css</automated>
    <fails_when>四行输出不是依次 6、2、1、1(:disabled 的 8 处 opacity 必须原样保留 —— 软化它就是让死掉的 G3 按钮看起来可点)</fails_when>
    <automated>comm -23 <(grep -o '\-\-[a-z0-9-]*:' frontend/style.css | sed 's/:$//' | sort -u) <(grep -o 'var(--[a-z0-9-]*' frontend/style.css | sed 's/var(//' | sort -u)</automated>
    <fails_when>输出的孤儿令牌中除 `--green-800` 之外还有其它名字(未消费的令牌 = 换个好名字的第二个字面量,Pitfall 1)</fails_when>
    <automated>node --check frontend/app.js && .venv/bin/python -m pytest -q && git diff --name-only HEAD -- frontend/app.js frontend/index.html</automated>
    <fails_when>任一命令退出码非 0;pytest 摘要行 passed 数少于改动前实测的收集数(规划时实测 225);第三条输出非空</fails_when>
    <human-check>在运行中的应用里打开一个历史(冻结)轮次:DevTools 选中 `#round-doc`,确认 Computed 的 `box-shadow` 含 `inset 3px 0 0 rgb(138, 101, 8)`、`opacity` == 1、`filter` == `saturate(0.6)`;肉眼确认文档区左侧有一条 3px 琥珀竖线,且没有任何横向位移。再确认归档态(`#rounds-placeholder.archive-mode #round-doc`)的 `opacity` 仍为 0.75。最后选一个 `button`,确认 Computed 的 `color` == rgb(26, 26, 26)。</human-check>
  </verify>
  <acceptance_criteria>
    - `frontend/style.css` 含 `#round-doc.round-frozen` 规则,体内为 `filter: saturate(0.6);` 与 `box-shadow: inset 3px 0 0 var(--color-action-warning);`,**不含** `opacity`
    - `grep -c 'opacity: 0.55' frontend/style.css` 输出 6;`grep -c 'opacity: 0.5;' frontend/style.css` 输出 2;`grep -c 'opacity: 0.8' frontend/style.css` 输出 1;`grep -c 'opacity: 0.75' frontend/style.css` 输出 1
    - `frontend/style.css` 含 `#rounds-placeholder.archive-mode #round-doc { opacity: 0.75; }`(未改动)
    - `frontend/style.css` 含 `button, input, select { color: var(--color-text); }` 且该规则位于文件**末尾**的追加区
    - `frontend/style.css` 不含 `--opacity-deemphasized`
    - 反向孤儿扫描除 `--green-800` 外输出为空
    - `bash scripts/check-01-token-conformance.sh` 打印 PASS;Gate 2 输出为空;`grep -c '^\.hidden {'` 输出 1;`grep -c '!important;'` 输出 1
    - `node --check frontend/app.js` 退出 0;pytest 全绿且 passed 数不少于改动前实测收集数;`git diff --name-only HEAD -- frontend/app.js frontend/index.html` 输出为空
  </acceptance_criteria>
  <done>冻结轮的 opacity 已删、结构性琥珀 inset 标记已加、saturate(0.6) 保留;归档态 0.75 未动;N-4 的 `button, input, select` 规则追加在文件末尾;全文件 CHECK-01 = 0、Gate 2 为空、除 `--green-800` 外零孤儿令牌;app.js/index.html/vendor 零改动;pytest 基线不下降。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| `frontend/style.css` → 浏览器渲染 | 纯样式,无用户输入、无网络、无脚本执行面 |
| 令牌块 → 围栏外全部声明 | 单点解析边界:`var()` 失败**静默**(拼错不回退报错,而是整条声明在计算值阶段失效并回退 `unset`)—— 这是本阶段唯一的"静默失败"面 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi04-08 | Tampering | `var(--x)` 拼写错误导致整条声明静默失效 | high | mitigate | 每个任务的 verify 都跑 Gate 2(`comm -23` 消费集减去声明集),输出必须为空。**明令禁止**用 `var(--x, #fallback)` 防御 —— 回退值重建第二事实源,且对 CHECK-01 隐形(hex 藏在 `var()` 里)。 |
| T-idi04-09 | Tampering | `#round-doc.round-frozen` 的只读信号被弱化为"只是变淡" | high | mitigate | 删 `opacity` 的同时必须补 `box-shadow: inset 3px 0 0 var(--color-action-warning)`(结构性、零位移);prohibition 明令禁止静默回退到 `opacity: 0.65` 且不加标记。D-P2-21 的"这轮只读"是用户在冻结轮里唯一的安全信号。 |
| T-idi04-10 | Tampering | 8 处 `:disabled` 的 `opacity` 被"顺手"统一或软化 | high | mitigate | `.verdict-buttons button:disabled` / `.overlay-card .modal-buttons button:disabled` / 六个 `#btn-*:disabled` 的 `opacity: 0.55 / 0.5` 必须原样保留,由 verify 的四处精确计数断言(6 / 2 / 1 / 1)。`:disabled` 是 G3 前提条件唯一的视觉信号(Pitfall M5)。 |
| T-idi04-11 | Tampering | 全局 `h1,h2,h3` 规则被"顺手"写出 | high | mitigate | 会与四处 chrome 覆盖碰撞(`.panel-header h2` 14px、`#draft-view h2` 15px、`#brainstorm-view h2` 14px、`.overlay-card h3` 16px);acceptance_criteria 显式断言文件不含全局 `h1, h2, h3 {` 规则。本阶段只做字号**值**替换,不新增任何字号规则。 |
| T-idi04-12 | Tampering | `--z-badge` / `--z-banner` 序关系被反转 | medium | mitigate | 序关系断言写入块内注释(10 < 20 < 100 < 200),并注明 `badge < banner` 对 b9664e0 FIX 2 承重(横幅必须压在状态徽标之上)。反转会让断流横幅被状态徽标盖住。 |
| T-idi04-13 | Repudiation | "渲染未变"被断言而非证明 | medium | mitigate | 本环境截图不可用、headless 渲染被挡,**不规划视觉 diff**;改为具名人工 DevTools Computed 检查(每个任务至少一条)+ 机械门(`app.js` / `index.html` 零 diff)。冻结轮的 backstop 真值无法确认时按 `human_needed` 上报。 |
| T-idi04-14 | Elevation of Privilege | 焦点环在冻结轮内失效(为 Phase 7 埋雷) | medium | mitigate | 这是 S-4 裁定的核心:删 `opacity` 才让 Phase 7 的 `--color-focus` 在冻结轮内保持 5.62:1;路线 1 会留下 2.85:1。本计划用"冻结轮规则体内不得出现 opacity"作为机械门。 |
| T-idi04-SC | Tampering | npm / pip / cargo 安装(供应链) | high | mitigate | **本阶段零安装**:D-06 禁止新增运行时依赖与构建步骤。无包管理器安装任务 ⇒ 无 `[ASSUMED]` / `[SUS]` 包需要合法性检查点。 |
</threat_model>

<verification>
**自动化门(每条都可独立运行,均须给出明确 PASS/FAIL):**

1. `bash scripts/check-01-token-conformance.sh` → PASS,围栏外裸 hex = 0
2. `bash scripts/check-03-hidden-uniqueness.sh` → PASS,`^\.hidden {` = 1
3. `bash scripts/check-04-important-count.sh` → PASS,`!important;` 声明数 = 1
4. Gate 2:`comm -23 <(消费集) <(声明集)` → 输出为空
5. 反向孤儿扫描:`comm -23 <(声明集) <(消费集)` → 只允许 `--green-800`
6. `grep -cE 'font-size: [0-9.]+px' frontend/style.css` → 0;`border-radius: [0-9]+px` → 0;`radius: [0-9]+px` → 0(后者覆盖两个长写圆角);`z-index: [0-9]+` → 0
7. `node --check frontend/app.js` → 退出 0
8. `.venv/bin/python -m pytest -q` → 全绿
9. `git diff --name-only HEAD -- frontend/app.js frontend/index.html` → 输出为空
10. `git status --porcelain frontend/` → 只有 `frontend/style.css`;`ls frontend/vendor/` → 仅 `marked.min.js`

**pytest 基线说明(必须照实记录):** ROADMAP 与 REQUIREMENTS 写的基线是 **219**,但规划时对工作树实测 `pytest --collect-only -q` 收集到 **225** 条(quick `260917-fqh` 之后新增)。门按"passed 数 ≥ 执行本计划前实测的收集数"判定,并在 SUMMARY 里记录实际数字 —— 照抄 219 会造出一个必然失败的假门。

**运行时验证(Pitfall M1:静态计数是补充不是替代,本计划每个任务都带一条):**
- 本环境截图不可用(headless 渲染被挡,且常驻 `/api/events` SSE 流使采集处理器无法终止)—— **不得规划视觉 diff**。
- 改为 DevTools Computed 面板的具名属性检查:`.panel-header` / `#doc-pane` / `button` 的 padding、`.overlay-card` 的 padding-top、`#brainstorm-view` 的 margin-top、四处 chrome 标题的 font-size、`.markdown-body code` 的 font-size、三个 z-index、冻结轮的 `box-shadow` / `opacity` / `filter`。
- **下游门必须实检:** `#brainstorm-view h2` 计算为 14px / rgb(138, 101, 8) —— 这是 ROADMAP Phase 5 SC5 与 Phase 6 SC5 的断言,本阶段结束时必须仍然成立。
- 冻结轮 backstop(琥珀 inset 竖线 + 轮次切换器 + 正文可读 + 零横向位移)只能人工确认;无法确认时按 `human_needed`(reason `insufficient_spec`)上报。

**渲染不变性(ROADMAP Phase 4 SC2):** 除 Deliberate Delta Ledger 记明的项(D-1、D-16、D-17、D-19,以及 Plan 01 已落地的 D-2…D-11、D-14、D-15)外,没有任何既有选择器改变位置、改名或增删声明。
</verification>

<success_criteria>
1. 间距 / 字号 / 字重 / 行高 / 圆角 / z-index 六族刻度全部声明且全部被消费,零孤儿(`--green-800` 除外)
2. 全部非颜色字面量替换为 `var()`;仅 D-16 / D-17 记明的吸附变更改变像素
3. `12.5px` 分数档被消除;`14px` 保留为一等档
4. z-index 序关系在块内注释中显式断言
5. `#round-doc.round-frozen` 的只读信号改为结构性标记(零布局位移);归档态 0.75 未动;8 处 `:disabled` 的 opacity 未软化
6. 围栏外零裸 hex(CHECK-01 仍 PASS);Gate 2 为空
7. `app.js` / `index.html` 零改动;`frontend/vendor/` 仍只有 `marked.min.js`;pytest 基线不下降
8. `#brainstorm-view h2` 仍计算为 14px / rgb(138, 101, 8)
</success_criteria>

## Artifacts this phase produces (本计划产出的部分)

Plan 01 已列出本阶段的完整符号清单;本计划新增的部分如下。

**新增文件路径:** 无。

**新增 CLI 调用:** 无(本计划复用 Plan 01 的三条守卫命令)。

**`frontend/style.css` 围栏 `:root` 块内新增的 CSS 自定义属性(本计划产出,共 31 个):**

间距(12):`--space-px` `--space-half` `--space-1` `--space-1-5` `--space-2` `--space-2-5` `--space-3` `--space-3-5` `--space-4` `--space-6` `--space-8` `--space-10`

字号(6):`--text-xs` `--text-sm` `--text-base` `--text-md` `--text-lg` `--text-xl`

字重(2):`--fw-regular` `--fw-semibold`

行高(3):`--lh-tight` `--lh-compact` `--lh-reading`

圆角(3):`--radius-sm` `--radius-md` `--radius-pill`

z-index(4):`--z-badge` `--z-banner` `--z-overlay` `--z-selection-menu`

布局(1):`--sidebar-w`

**新增/变更的选择器(本计划 1 处,已在 ledger 记明):**

| 选择器 | 性质 |
|---|---|
| `button, input, select` | **新增规则**(D-19 / note N-4),追加在文件末尾 |

**变更的既有规则体(值替换,选择器未变):** `#sidebar`(`flex-basis` 改 `var(--sidebar-w)`)、`#round-doc.round-frozen`(删 `opacity`、加 `box-shadow`)。

**新增字面量例外(0 个):** 本计划不引入任何新例外。`--sidebar-w: 420px` 的 420px 是 L-4(令牌**内部**的字面量,围栏内本就合法)。
</verification>

<output>
Create `.planning/phases/idi-04-tokens-contract/idi-04-02-SUMMARY.md` when done
</output>
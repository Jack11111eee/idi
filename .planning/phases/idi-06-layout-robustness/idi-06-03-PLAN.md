---
phase: idi-06-layout-robustness
plan: 03
type: execute
wave: 3
depends_on:
  - idi-06-01
  - idi-06-02
files_modified:
  - frontend/style.css
  - scripts/check-05-ui-uat.py
autonomous: true
requirements:
  - LAYOUT-02
  - A11Y-07

estimate:
  tokens: 66000
  raw_tokens: 66000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- lifted from idi-06-UI-SPEC.md `## UI Considerations` — explicit tier (1 of 24; E8) ----
    - "E8 `.annotation-answer summary` `long-text`:`-answer summary` 加 `min-height: 24px; min-width: 24px;` 后命中区 ≥24×24,而标签文案(`AI 回应` / `大白话回答`)不折断、不溢出该命中区 ← UI-SPEC UI-Considerations E8 `long-text`(explicit)"
    # ---- lifted from idi-06-UI-SPEC.md `## UI Considerations` — backstop tier (2 of 19; E8) ----
    - statement: "E8 `.annotation-answer summary` `loading`:数据或内容仍在加载时显示什么(skeleton / spinner / 渐进呈现)?本阶段对该状态维度零改动 —— `<details>` 的展开控件语义与标签文案一字不动,只加两条尺寸下限声明。"
      verification: backstop
    - statement: "E8 `.annotation-answer summary` `error`:加载或提交失败时显示什么(消息 / 重试入口 / 部分回退)?本阶段对该状态维度零改动 —— AI 答复的失败态由 `app.js` 的渲染路径决定,本阶段不触碰。"
      verification: backstop
    # ---- phase-specific truths ----
    - "窄窗口守卫是**实测驱动**的条件交付物:在 L-3 / L-4 已落地的树上重测 1440 / 1024 / 768 三处的文档级 `scrollWidth` 与 `clientWidth`,按 UI-SPEC §L-2 的决策规则三选一 —— ≥768px 区间无破版 ⇒ **不写**守卫并登记「被实测推翻」;768–1023px 之间破版 ⇒ 写**恰好一条** `@media (max-width: 1023px)`;只在 <768px 破版 ⇒ 登记、不修(承诺下限是 768px)← L-2 / D-08"
    - "无论走哪一支,三个宽度的**原始数值**(各一行 `scrollWidth / clientWidth`)必须落盘 —— UI-SPEC L-2 明文「不能只给结论」← L-2"
    - "若写出守卫:它是全文件**唯一**的媒体查询,块首带 UI-SPEC §L-2 的逐字围栏注释(显式声明断点字面量例外 L-1:CSS 禁止在媒体查询条件中使用 `var()`,带 `var()` 的 `@media` 会被静默丢弃),块内**只放实测证成的声明**,取值全部来自已声明令牌或媒体作用域内 `:root` 的重赋 ← L-2 / D-10 / 硬规则 4"
    - "若写出守卫:块内**不得**出现 `#app { flex-direction: column }`、任何堆叠布局、第二条断点、断点阶梯、`!important`、新令牌或 `#hex` ← L-2 的「禁止」列 / Q5 / 硬规则 2 / 4 / 8"
    - "item 8 的三宽度文档级溢出读数由**只读诊断升为硬断言**:1440 与 1024 两处 `document.documentElement.scrollWidth <= document.documentElement.clientWidth` —— 这正是 LAYOUT-02 承诺的「≥1024px 无横向溢出」。768 处的读数保持诊断(它的承诺是「无内容遮挡」,已由 item 8 的 badge × banner 不相交断言覆盖)← L-2 / D-14"
    - "item 8 追加一条守卫形态断言:`@media` 块在全文件的出现次数与 `idi-06-03-SUMMARY.md` 记录的决策一致(写出守卫 ⇒ 恰 1;登记推翻 ⇒ 0)。**该断言读的是文件文本而非渲染结果**,与几何断言互补 ← L-2 / Anti-Pattern 3"
    - "A11Y-07 按**可交互元素普查**施加,不按点名:A11Y-07 点名了裁决按钮,而实测唯一确定不达标的是 `.annotation-answer summary`(`font-size: var(--text-xs)` = 12px、无 padding、无 min-height ⇒ ≈14–17px)。**只对实测 < 24×24 者施加,已达标者零改动** ← L-6 / D-15 / D-17"
    - "机制锁定为 `min-height: 24px` + `min-width: 24px`(原地加两行到该控件的既有规则体)。**不动现有 `padding`**(改 padding 改的是外观而非命中区);**不用 `::after` 撑开**(`.verdict-buttons { gap: var(--space-2) }` = 8px,扩展后的相邻命中区会互相重叠,反而可能违反 2.5.8 的「不与他者相交」)← L-6 / D-16"
    - "`24px` 是**裸字面量**(尺寸族,非间距族),刻意不写成 `var(--space-6)` —— 24 是 WCAG 2.5.8 的目标尺寸常数;挂在间距刻度上会让一次间距改动静默地把命中区压到下限之下(「名必须说实话」的同一条方法论)← L-6 / S-3"
    - "`.annotation-answer summary` 的既有四条声明(`cursor: pointer` / `color: var(--color-text-muted)` / `font-size: var(--text-xs)` / `margin-top: var(--space-1)`)逐字保留,只加两行尺寸声明 ← L-6 / Do-Not-Touch List"
    - "已登记的视觉变更:`-answer summary` 从 ≈14–17px 抬到 ≥24px **会改变 `-item` 的高度**(每个带 AI 回复的批注条目 +7…10px)。这是 D-17 明文要求显式登记的变更,必须进 SUMMARY ← L-6 / D6-3"
    - "`.collapse-indicator` 的 `font-size: 20px; line-height: 1` **不得触碰** —— 它是 backlog `999.1` 第 1 项,属硬规则 5 的不得触碰清单;其可点父级 `.panel-header` 为 36px,达标 ← 硬规则 5 / 05-CONTEXT D-23"
    - "L-5 的焦点环解裁切按**可聚焦元素普查**判定,不按容器名。判据:一个裁剪容器(计算 `overflow != visible`)必须让它的每一个可聚焦后代距离其 **padding 边**至少 **4px**(= Phase 7 的 `outline: 2px solid` + `outline-offset: 2px` 的环外伸量)← L-5 / D-13"
    - "L-5 的决策规则:实测与静态分析预期一致 ⇒ **不改任何 padding**,登记为「被实测推翻」并附普查原始数据;实测某容器 clearance < 4px ⇒ **只改那一个容器**,取值 `var(--space-1)`(4px),并在 SUMMARY 登记为视觉变更。**禁止「为确定性四个全抬」** ← L-5 / S-2 / Pitfall 8"
    - "item 9 追加两条普查断言:(a) 每个裁剪容器 × 其每个可聚焦后代的实测 clearance ≥ 4px;(b) 每个可交互元素的计算盒宽与高均 ≥ 24px。两条都按 DOM 普查算出,不硬编码选择器列表 ← L-5 / L-6 / D-13 / D-17"
    - "**本阶段不写任何 `:focus` / `:focus-visible` / `:hover` / `:active` / `transition` 规则** —— 本阶段只为 Phase 7 解裁切。`frontend/style.css` 内 `:focus-visible` 计数 == 0 ← L-5 / 硬规则 9"
    - "`frontend/style.css` 围栏 `:root` 内零改动(零新增令牌);硬规则 8 成立 ← 硬规则 8"
    - "`bash scripts/check-01-token-conformance.sh` 打印 `PASS` 且 exit 0(围栏外裸 `#hex` 仍为 0;断点是**非 hex** 字面量,不触发该门)← CHECK-01 / D-10 的门面事实"
    - "`python3 scripts/check-02-contrast.py` 仍打印 `PASS: 0 failures`,清单规模与 `ORDER` 行逐字不变(本计划零颜色改动)← CHECK-02"
    - "`bash scripts/check-03-hidden-uniqueness.sh` 打印 `PASS`(`^\\.hidden {` 计数 == 1)← CHECK-03 / 硬规则 1"
    - "`bash scripts/check-04-important-count.sh` 打印 `PASS`(`!important` **声明**数 == 1)← CHECK-04 / 硬规则 2"
    - "全量 harness 门在收口时复跑且全绿:`--item smoke` / `1` / `2` / `3` / `4` / `6` / `7` / `8` / `9` 九项(第 5 项含真实 AI 调用,其 `--ai-smoke` 半边沿用已记录的处置)← 硬规则 7 / D-20"
    - "D-19 的连带复验义务履行:`frontend/style.css` 与 `scripts/check-05-ui-uat.py` 都在 `idi-04.1-radix` 的 `covered_files` 内,故本阶段**必然**令其 `covered_digest` stale(成因是**内容真变**,走重新验证而非补指纹)。本计划以 HEAD 内容重算 04.1 的全部结论数值并把证据记入 SUMMARY,**`idi-04.1-VERIFICATION.md` 一字不改**(`git status --porcelain -- .planning/phases/idi-04.1-radix/` 为空),指纹写回留给编排器的 `/gsd-verify-work idi-04.1-radix` ← D-19 / Phase 5 `idi-05-03` 的先例"
    - "运行时:item 8 在 1440 与 1024 两处读到文档级 `scrollWidth <= clientWidth`;item 9 在真实浏览器里读到每个裁剪容器 × 可聚焦后代的 clearance ≥ 4px、每个可交互元素的盒宽高均 ≥ 24px ← 硬规则 7 / L-2 / L-5 / L-6"

  artifacts:
    - path: "frontend/style.css"
      provides: "条件交付物:`@media (max-width: 1023px)` 守卫块(仅在实测证成时落地);`.annotation-answer summary` 规则体内新增 `min-height: 24px;` 与 `min-width: 24px;`;条件交付物:某个裁剪容器的 `padding` 改为 `var(--space-1)`(仅在实测 clearance < 4px 时)"
      contains: ".annotation-answer summary"
    - path: "scripts/check-05-ui-uat.py"
      provides: "item 8 的三宽度文档级溢出断言(1440 / 1024)+ 守卫形态断言;item 9 的 L-5 clearance 普查断言与 A11Y-07 命中区普查断言"
      contains: "clearance"

  key_links:
    - from: "`@media (max-width: 1023px)` 守卫块(若落地)"
      to: "`--doc-panel-w: clamp(340px, 30vw, 480px)`"
      via: "媒体作用域内的 `:root` 重赋是唯一被允许的守卫体形态(例外 L-4:字面量在令牌声明内是合法的);或改用已声明令牌的消费者侧声明"
      pattern: "@media \\(max-width: 1023px\\)"
    - from: "`.annotation-answer summary` 的 `min-height: 24px` / `min-width: 24px`"
      to: "`scripts/check-05-ui-uat.py` item 9 的可交互元素命中区普查断言"
      via: "运行时 `getBoundingClientRect()` 逐元素读数,与 24×24 期望相比;元素读不到时记 BLOCKED"
      pattern: "min-height: 24px;"
    - from: "L-5 的 clearance 普查结论"
      to: "Phase 7 的 `:focus-visible { outline: 2px solid; outline-offset: 2px }`"
      via: "4px 阈值就是环的外伸量;本阶段只解裁切、不写环,故 Phase 7 落地时环不被任何裁剪祖先切掉"
      pattern: "clearance"
    - from: "`idi-04.1-radix` 的 `covered_digest`"
      to: "本阶段改写过的 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`"
      via: "两份文件都在 04.1 的 `covered_files` 内 ⇒ 指纹 stale(内容真变);本计划提供重算证据,写回由 `/gsd-verify-work idi-04.1-radix` 执行"
      pattern: "covered_files"

  prohibitions:
    - statement: "不得为命中区去重构侧栏。路线图 fence 的**前提两处都已失效**(420px 侧栏不存在,现为 `--doc-panel-w: clamp(340px, 30vw, 480px)`;裁决按钮已从 3 个变成 2 个),故 fence 不再构成本阶段的具体约束 —— 但它的**实质**(不为命中区去重构侧栏结构)保留为一般原则。命中区的修法只有两条尺寸声明,不得演变成布局改动"
      status: active
      verification: flagged
    - statement: "不得触碰 `.collapse-indicator`(含它的 `font-size: 20px` 与 `line-height: 1`)。它是 backlog `999.1` 第 1 项,属硬规则 5 的不得触碰清单;它在 24×24 判据上由可点父级 `.panel-header`(36px)满足,不得被当作「顺手达标」的对象"
      status: active
      verification: flagged
    - statement: "不得用抬 `padding`、`::after` 撑开、改 `font-size` 或任何改外观的方式达成 24×24。机制已锁定为 `min-height: 24px` + `min-width: 24px`(D-16):抬 padding 改的是外观而非命中区,且连锁影响行高与相邻间距观感;`::after` 撑开会让 `.verdict-buttons`(gap = 8px)的相邻命中区互相重叠,反而可能违反 WCAG 2.5.8 的「不与他者相交」要求"
      status: active
      verification: flagged
    - statement: "不得「为确定性」把四个裁剪容器的 padding 全抬一遍。`#main-pane` 的 padding 抬升会移动其居中布局下四个 section 的位置,并与 `#doc-panel-body { padding: 32px 40px }` 叠加 —— 那是两处计划外视觉位移,且会干扰 L-4 的滚动容器数统计。这类「顺手统一」正是 Pitfall 8 的范围蔓延(UI-SPEC S-2 的裁定)"
      status: active
      verification: flagged
    - statement: "不得声明任何 `:focus` / `:focus-visible` / `:hover` / `:active` / `transition` 规则 —— A11Y-01 / INTERACT-01 / INTERACT-02 全归 Phase 7。本阶段只为焦点环**解裁切**,不写环。同理不得新增任何令牌(硬规则 8:围栏 `:root` 内零改动)"
      status: active
      verification: flagged
    - statement: "不得写出第二条断点、断点阶梯或任何响应式系统;不得在媒体查询条件里使用 `var()`(该规则会被静默丢弃);不得在守卫体内使用 `!important` / 新令牌 / `#hex`;不得写 `#app { flex-direction: column }` 或任何堆叠布局(Q5 明文 Out of scope:它们改变 DESIGN.md §4.1 两栏契约的**含义**)。若实测无破版,守卫**不写**"
      status: active
      verification: flagged
    - statement: "不得触碰 `#selection-menu` 的定位数学(Pitfall 8:它在旗舰交互路径上且工作正常,不得「顺手改进」);不得为 DRY 让归档视图复用 `loadRoundView`(Pitfall 3 UI-6.3:`updateFrozenPresentation(true)` 会把 `applyArchiveView` 设的 `disabled = true` 复位);不得重构 header"
      status: active
      verification: flagged
    - statement: "不得改写 `idi-04.1-VERIFICATION.md` 的 frontmatter(含 `covered_digest`)—— D-19 的义务是**提供重算证据**,指纹写回是编排器 `/gsd-verify-work idi-04.1-radix` 的动作。本计划擅自写回会破坏「谁改了什么」的可追溯性(Phase 5 `idi-05-03` 已立此先例)"
      status: active
      verification: flagged

  assumptions:
    # ---- edge probe fallback ($COVERAGE): A11Y-07 row, ALL unresolved ----
    # The edge probe is an English-cue classifier and misclassified the Chinese requirement prose;
    # `unclassified` stays `unresolved` (never auto-resolved with backstop, never dismissed).
    - statement: "A11Y-07 的边缘面未经探针确认(probe 返回 `unclassified — review manually`):需求的**两处边界前提均已失效**(「实测约 21–22px 高」按 HEAD 的 `font-size` / `padding` / `border` / `line-height` 算应为 26–30px;「420px 侧栏内 3 个按钮」的前提不存在,现为 `clamp()` 面板与 2 个按钮),故判据只能走实测。本计划按 D-15 / D-16 / D-17 的可交互元素普查执行,并把该行记为 flagged assumption 而非已解决项。"
      status: unresolved
      verification: flagged
---

<objective>
在 L-3 / L-4 已落地的树上做三件收口工作:用实测决定窄窗口守卫是否存在(L-2)、按元素普查施加两处「解裁切 / 命中区」的尺寸下限(L-5 / L-6)、并履行 D-19 的连带复验义务。

Purpose: 前两个计划把布局结构改稳,本计划把三件**必须看到全部结构改动之后才能判定**的事做掉。**L-2 是唯一的顺序强制项**:D-08 的分析是「横向溢出的真因是 `min-width: auto` 缺失,而不是面板宽度占比」,所以在 L-3 / L-4 之前测三宽度会把一个即将被修好的状态判成破版、写出一条本不该存在的守卫。**L-5 / L-6 是同一口径的两处普查**:按容器名 / 点名枚举会漏掉没被点名的那个 —— A11Y-07 点名了裁决按钮(实测很可能本来就达标),而唯一确定不达标的是没被点名的 `.annotation-answer summary`(`<details>` 的展开控件)。这与 Phase 5 `G-idi-05-1` 是同构的教训。**D-19 是流程义务**:`frontend/style.css` 与 `scripts/check-05-ui-uat.py` 都在 `idi-04.1-radix` 的 `covered_files` 内,本阶段必然令其指纹 stale。

Output: `frontend/style.css` 的条件守卫(若实测证成)、`.annotation-answer summary` 的两条尺寸下限、条件性的某容器 padding 抬升;`scripts/check-05-ui-uat.py` 的 item 8 三宽度硬断言 + 守卫形态断言、item 9 的 clearance 与命中区两条普查断言;以及 04.1 的连带复验证据。

**基线口径(D-01):磁盘 HEAD 是唯一现实基线。** 本计划所有「现状」值以 `frontend/style.css` 与 `scripts/check-05-ui-uat.py` 在**波次 2 结束后的磁盘内容**为准 —— 不是 `06-CONTEXT.md` 的行号(已漂移),不是 `04-UI-SPEC.md` 的 Q5/Q6(其前提已被 HEAD 推翻),不是 `ROADMAP.md` Phase 6 的交付物清单(六项被推翻)。

**本计划消费的三个输入(缺一即无法执行):**

| 输入 | 出处 | 用途 |
|---|---|---|
| 波次 1 的三宽度基线数值 | `idi-06-01-SUMMARY.md` §`测量决策记录` | L-2 决策的对照(区分「L-3 / L-4 修好了」与「本来就没破」) |
| 波次 2 之后的三宽度新数值 | `idi-06-02-SUMMARY.md`(Task 1 第 3 步) | L-2 决策的**判据本身** |
| L-5 clearance 普查表 + L-6 命中区普查表 + < 24×24 清单 | `idi-06-01-SUMMARY.md` §`测量决策记录` | L-5 / L-6 的落点清单 |

**本计划关闭的需求:** LAYOUT-02(判据在 Task 1 落地)、A11Y-07(Task 2)。**本计划不触碰:** LAYOUT-01 / LAYOUT-03 / LAYOUT-04(计划 01 / 02 已关闭);`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` / `scripts/ui-states/` 零改动;`scripts/check-01…04` 与 `scripts/check-06-idi05-validation.py` 代码零改动;围栏 `:root` 内零改动(零新增令牌);任何 `:focus` / `:hover` / `:active` / `transition` 规则(Phase 7);`.collapse-indicator`(backlog `999.1`);`#selection-menu` 的定位数学;归档视图的 `loadRoundView` 复用路径;header 的重构。

**口径登记(不改文件,只登记):** SC#3 收窄为「面板区内恰好两个滚动者(`#main-pane` + `#latest-check`)」,外加 SC#3 明文豁免的 `#chat-messages`(A-5);SC#5 更正为令牌接线表述 `var(--text-md)` / `var(--color-action-warning)`(A-6);LAYOUT-04 基线从「4 个滚动容器」更正为「3 个嵌套 + 1 个外层」(A-8);`ROADMAP.md` Phase 7 段的「`#sidebar` 的 padding 为 0」更正为 `#main-pane` / `#doc-panel`(A-9)。**`ROADMAP.md` / `REQUIREMENTS.md` / `04-UI-SPEC.md` 正文一律不改** —— 改它们会作废已通过的验证指纹。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/REQUIREMENTS.md
@.planning/phases/idi-06-layout-robustness/06-CONTEXT.md
@.planning/phases/idi-06-layout-robustness/idi-06-PATTERNS.md
@.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md
@.planning/phases/idi-06-layout-robustness/idi-06-01-SUMMARY.md
@.planning/phases/idi-06-layout-robustness/idi-06-02-SUMMARY.md
@.planning/phases/idi-04.1-radix/idi-04.1-VERIFICATION.md
@.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-03-SUMMARY.md
@frontend/style.css
@frontend/index.html
@scripts/check-05-ui-uat.py
@scripts/check-02-contrast.py
</context>

## Artifacts this phase produces

> 本节的用途:**plan-review-convergence 的 source-grounding pass 读它,把本阶段新建的符号从漂移校验里排除**。
> 未列在此的符号即既有符号,其变动必须能追到某条已锁决策。

**本计划新建的符号:**

| 类别 | 符号 | 位置 | 条件性 |
|---|---|---|---|
| 新增 CSS 媒体查询 | `@media (max-width: 1023px)` 块 | `frontend/style.css` 文件末尾 | **条件交付物**:仅在实测证成 768–1023px 破版时落地 |
| 新增 CSS 声明 | `min-height: 24px;` / `min-width: 24px;` | `.annotation-answer summary` 规则体内 | 仅在实测该控件 < 24×24 时(UI-SPEC 判定「确定不达标」) |
| 改写 CSS 声明 | 某裁剪容器的 `padding` → `var(--space-1)` | 由 L-5 普查定 | **条件交付物**:仅在实测 clearance < 4px 时,且**只改那一个容器** |
| 新增断言标签 | item 8:1440 / 1024 两处文档级 `scrollWidth <= clientWidth` | `scripts/check-05-ui-uat.py` | 无条件 |
| 新增断言标签 | item 8:守卫形态(`@media` 出现次数与决策一致) | 同上 | 无条件 |
| 新增断言标签 | item 9:每个裁剪容器 × 可聚焦后代的 clearance ≥ 4px | 同上 | 无条件 |
| 新增断言标签 | item 9:每个可交互元素的计算盒 ≥ 24×24 | 同上 | 无条件 |

**本计划明确不产生的新符号:** 零新增令牌(围栏 `:root` 内零改动;守卫体内若重赋 `--doc-panel-w` 是**重赋既有令牌**,不是新令牌)、零新文件、零新依赖、零新构建步骤、零 `:focus` / `:focus-visible` / `:hover` / `:active` / `transition` 规则、`frontend/app.js` / `index.html` / `vendor/` 零字节改动。

<tasks>

<task type="auto">
  <name>Task 1: L-2 窄窗口守卫决策 —— 重测三宽度 + item 8 溢出硬断言 + 条件守卫</name>
  <files>frontend/style.css, scripts/check-05-ui-uat.py</files>
  <read_first>
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`### L-2 窄窗口守卫(条件交付物 —— 实测驱动)` —— **逐字照做**的两条判据公式、三宽度取值、「面板内部的横向滚动条不算破版,明确不计入」的明文、**决策规则三条**、若写出守卫时被锁死的**逐字注释头与块体形态**、允许的守卫体 / 禁止清单
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`## Deliberate Delta Ledger(本阶段)` 的 D6-9 —— 守卫体声明的登记要求(「实测无破版则本项不存在」)
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`## 契约修正登记` 的 A-1 / A-2 / A-3 —— 契约 Q6 整条撤销、Pitfall 8 的「不得移入正常流」撤销、L-5 例外行的豁免对象消失。**本任务不得复活任何一条被撤销的文本**
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`## Spacing Scale` 的例外清单 —— L-1(条件:断点字面量,仅在写出 `@media` 时于该段首的围栏注释里声明)/ L-2(unitless `0`)/ L-4(字面量在令牌声明内合法)
    - `.planning/phases/idi-06-layout-robustness/idi-06-01-SUMMARY.md` §`测量决策记录` 的三宽度**基线**数值(波次 1 之前)与 `.planning/phases/idi-06-layout-robustness/idi-06-02-SUMMARY.md` 的三宽度**新**数值(波次 2 之后)—— **判据取后者,前者是对照**
    - `frontend/style.css` 围栏内 `--doc-panel-w: clamp(340px, 30vw, 480px);`(HEAD `:228`)与 `--doc-panel-w-collapsed: 48px;`(`:229`)—— 守卫体内若重赋令牌,重赋的是这两个之一,且**不改围栏内的声明**(围栏内零改动)
    - `frontend/style.css` 文件末尾 —— 波次 2 追加的六选择器 `overflow-wrap` 规则;守卫块**追加在它之后**
    - `scripts/check-05-ui-uat.py` 本阶段 item 8 全文 —— 三宽度循环、`set_viewport_size`、viewport 复位、`showStreamBanner` 调用、以及**三项只读诊断**的实现位置(本任务把其中「文档级 `scrollWidth`」一项升为硬断言,另两项保持只读)
    - `scripts/check-05-ui-uat.py` L1411-1517(item7 的骨架)与 L880-945(`check_render_markdown_call_sites` 的两条纪律:比两个独立量、FAIL 消息给可执行动作)
    - `scripts/check-01-token-conformance.sh` —— 只统计裸 `#hex`;断点 `1023px` 是**非 hex 字面量**,不触发该门(已核实)。**只读不改**
    - `.planning/ROADMAP.md` §Phase 6 的 **Anti-Pattern 3** 与 §Phase 6 交付物第 2 条 —— 断点值是「该规则唯一的合法字面量例外」,须在 UI-SPEC 中显式声明为例外,否则会被读成疏漏;**只读不改**
  </read_first>
  <action>
    **第 1 步 —— 在波次 2 之后的树上重测三宽度(L-2 的判据)。** 实跑 `.venv/bin/python scripts/check-05-ui-uat.py --item 8`,从输出里取三项只读诊断中的**文档级溢出**那一项:1440 / 1024 / 768 三处各一行的 `document.documentElement.scrollWidth` 与 `clientWidth`。**判据一律取文档级 `scrollWidth`** —— `#doc-panel { overflow-y: auto }` 会把 `overflow-x` 的 used value 一并算成 `auto`,故一张宽 markdown 表会在**面板内部**产生横向滚动条;那是可达内容,不是文档级溢出,也不是遮挡。把三个宽度的**原始数值逐行抄进 SUMMARY**,并与 `idi-06-01-SUMMARY.md` 的基线值**并列**。

    **第 2 步 —— 按 UI-SPEC §L-2 的决策规则三选一(逐字照做,不得自创第四种)。**

    - **≥768px 区间内无破版** ⇒ **不写** `@media`;把路线图这条交付物登记为**「被实测推翻」**,并在 SUMMARY 里附三个宽度的原始数值作为证据,同时写明「L-3 / L-4 落地后已满足;基线值(波次 1)为 X,当前为 Y」。
    - **768–1023px 之间破版** ⇒ 写**恰好一条** `@media (max-width: 1023px)`。
    - **只在 <768px 破版** ⇒ 落在 LAYOUT-02 承诺之外,**登记,不修**(承诺下限是 768px)。

    **第 3 步 —— 若走「写出守卫」这一支,形态被锁死。** 块首必须带 UI-SPEC §L-2 的**逐字围栏注释**,它显式声明断点字面量例外(理由:CSS 禁止在媒体查询条件中使用 `var()`,带 `var()` 的 `@media` 会被静默丢弃;`1023px` 是 Q5 承诺边界「≥1024px 无横向溢出」的唯一合法字面量),并写明本块是全文件唯一的媒体查询、范围是「不破版」而非「适配」。块体**只放实测证成的声明**,取值来自两类:(a) 媒体作用域内 `:root { --doc-panel-w: <字面量> }`(命中例外 L-4:字面量在令牌声明内合法);(b) `#doc-panel` / `#doc-panel-body` 上使用**已声明令牌**的声明(如收窄 `#doc-panel-body` 的 `padding`)。**禁止**:`#app { flex-direction: column }` 或任何堆叠布局、第二条断点、断点阶梯、媒体查询条件里的 `var()`、任何 `!important`、任何新令牌、任何 `#hex`。

    守卫块**追加在文件末尾**(波次 2 的六选择器规则之后),不重排任何既有规则(硬规则 3)。围栏 `:root` 内**零改动** —— 媒体作用域内的 `:root` 是另一个块,不是围栏。

    **第 4 步 —— 把 item 8 的文档级溢出读数由只读诊断升为硬断言。** 对 1440 与 1024 两处各加一条 `ok_true`:`document.documentElement.scrollWidth <= document.documentElement.clientWidth`。**这正是 LAYOUT-02 承诺的「≥1024px 无横向溢出」**,而它是本任务之后才成立的 —— 故升级放在本任务而非波次 1(在波次 1 升它会得到一条必然失败的假红)。768 处的读数**保持只读诊断**:它在 LAYOUT-02 里的承诺是「无内容遮挡」,已由 item 8 的 badge × banner 不相交断言覆盖。每处断言旁用 `info()` 打印原始 `scrollWidth` / `clientWidth`。探针返回 `null` ⇒ `blocked(...)`。

    **第 5 步 —— item 8 追加一条守卫形态断言。** 加一条 `ok_true`:全文件 `@media` 出现次数与本次决策一致(走「写出守卫」⇒ 期望 1;走「登记推翻」⇒ 期望 0)。判据从 `frontend/style.css` 的文本算出(在 Python 侧 `read_text()` 后 `count("@media")`,与 `check_render_markdown_call_sites` 的算法同族),**不依赖 shell 管道**。这条断言读的是文件文本而非渲染结果,与几何断言互补:它抓的是「守卫被悄悄删掉 / 悄悄多写一条」。在 `info()` 里写明本次走的是哪一支与原始数值。

    **第 6 步 —— 运行时验证(硬规则 7)。** 实跑 `--item 8`(新断言)与 `--item smoke,1,4,7`(既有项无回归),并把逐项结论与三宽度原始数值抄进 SUMMARY。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 8</automated>
    <fails_when>exit code is not 0, or the `=== 逐项结论 ===` block reports anything other than `item 8: PASS`, or any assertion line reports `FAIL` or `BLOCKED`</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,4,7</automated>
    <fails_when>exit code is not 0, or the summary reports anything other than `item smoke: PASS`, `item 1: PASS`, `item 4: PASS`, `item 7: PASS`</fails_when>
    <automated>grep -c '@media' frontend/style.css; grep -c '^@media (max-width: 1023px) {' frontend/style.css</automated>
    <fails_when>the second count is greater than 1 (at most one media query is permitted), or the second count differs from the decision recorded in `idi-06-03-SUMMARY.md` (write-guard branch ⇒ 1; refuted branch ⇒ 0)</fails_when>
    <automated>grep -n -A 6 '^@media (max-width: 1023px) {' frontend/style.css | grep -c 'flex-direction: column'</automated>
    <fails_when>the count is not 0 (stacking layouts change the meaning of the DESIGN.md §4.1 two-column contract and are explicitly out of scope)</fails_when>
    <automated>grep -c 'var(--[a-z0-9-]*,' frontend/style.css</automated>
    <fails_when>the count is not 0 (Hard Rule 4 forbids `var(--x, fallback)` — it reopens a second source of truth)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>any of the three prints anything other than exactly `PASS`, or exits non-zero</fails_when>
    <automated>python3 scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>the last line is not exactly `PASS: 0 failures`</fails_when>
    <automated>grep -o 'scrollWidth' scripts/check-05-ui-uat.py | wc -l</automated>
    <fails_when>the count is less than 2 (the 1440 and 1024 overflow assertions plus the retained 768 diagnostic)</fails_when>
  </verify>
  <acceptance_criteria>
    - 三个宽度(1440 / 1024 / 768)的原始 `scrollWidth` 与 `clientWidth` 逐行记入 `idi-06-03-SUMMARY.md`,并与 `idi-06-01-SUMMARY.md` 的基线值并列对照
    - SUMMARY 明确写出走了 UI-SPEC §L-2 三条决策规则中的**哪一支**,并给出判据数值
    - 若走「写出守卫」:文件内 `@media (max-width: 1023px) {` 恰 1 处,块首含逐字围栏注释(声明断点字面量例外与「本块是全文件唯一的媒体查询」),块体内无 `flex-direction: column`、无第二条断点、无媒体条件内的 `var()`、无 `!important`、无新令牌、无 `#hex`
    - 若走「被实测推翻」:文件内 `@media` 计数 == 0,且 SUMMARY 含三个宽度的原始数值作为推翻证据
    - item 8 含 1440 与 1024 两处文档级溢出硬断言(`scrollWidth <= clientWidth`),768 处保持只读诊断
    - item 8 含守卫形态断言(读 `frontend/style.css` 文本算出 `@media` 计数并与决策比较)
    - 围栏 `:root` 内零改动:`git diff -- frontend/style.css` 的 hunk 中没有任何行落在围栏 START/END 之间
    - `frontend/style.css` 内 `var(--x,` 形式的 fallback 计数 == 0(硬规则 4)
    - `--item 8` 全 PASS(0 FAIL / 0 BLOCKED);`--item smoke` / `1` / `4` / `7` 四项仍全 PASS
    - `bash scripts/check-01-token-conformance.sh` / `check-03` / `check-04` 均 `PASS`;`check-02` 仍 `PASS: 0 failures`
  </acceptance_criteria>
  <done>三宽度在波次 2 之后的树上重测完毕,原始数值与波次 1 基线并列落盘;按 UI-SPEC §L-2 的决策规则走出唯一一支(写出恰好一条守卫 / 登记被实测推翻);item 8 的 1440 与 1024 两处文档级溢出升为硬断言、768 保持诊断、并追加守卫形态断言;四条既有守卫与 `--item 8` / `smoke,1,4,7` 全绿。</done>
</task>

<task type="auto">
  <name>Task 2: L-6 命中区 + L-5 解裁切 —— 按元素普查施加尺寸下限,并把两条普查写成门</name>
  <files>frontend/style.css, scripts/check-05-ui-uat.py</files>
  <read_first>
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`### L-6 紧凑控件命中区(A11Y-07)` —— 24×24 判据、**机制锁定**(`min-height` / `min-width`,不动 padding、不用 `::after`)、普查表(五类控件的盒高估算与 ✓/✗ 判定)、决策规则两条、**已登记的视觉变更**、`24px` 为何不是间距刻度违规的显式声明、fence 失效的登记(D-18)
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`### L-5 焦点环解裁切(普查口径 —— 本阶段不写任何 :focus 规则)` —— 裁剪容器判据(`overflow != visible`)、**4px 阈值的由来**、静态分析预期表(四个容器的 HEAD padding 与可聚焦后代)、决策规则三条、**禁止「为确定性四个全抬」**
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`## Spacing Scale` —— `--space-1` = 4px 是本阶段**唯一**被允许用于 L-5 抬升的取值;`--space-half` = 2px 是 `#annotation-list` 的现值
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`## Deliberate Delta Ledger(本阶段)` 的 D6-3 / D6-10 —— 两条必须进 SUMMARY 的视觉变更登记
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`## Sign-Off Items` 的 S-2 / S-3 —— 「接受零 padding 改动」与「`24px` 用裸字面量」两条**已由本文件的建议裁定**,执行器照做、不得重新讨论
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`## Do-Not-Touch List(继承 + 本阶段追加)` —— `.annotation-answer summary` 的既有四条声明(`font-size` / `color` / `cursor` / `margin-top`)不得改动;`.collapse-indicator` 不得触碰
    - `frontend/style.css` L991-996 —— `.annotation-answer summary` 规则体**现状逐字**(`cursor: pointer` / `color: var(--color-text-muted)` / `font-size: var(--text-xs)` / `margin-top: var(--space-1)`);两行尺寸声明加在其后
    - `frontend/style.css` L1174-1176 —— `.verdict-buttons { display: flex; gap: var(--space-2) }` 与 `.verdict-buttons button { font-size: var(--text-base); padding: var(--space-1) var(--space-2-5) }` —— D-16 拒绝 `::after` 撑开的依据(8px gap 下扩展命中区会互相重叠)
    - `frontend/style.css` L551-559 —— `button { padding: var(--space-1-5) var(--space-2-5); border: 1px solid …; font-size: var(--text-base) }`,普查表里「所有 `<button>` ≈ 30–34px ✓」的依据
    - `frontend/style.css` L509-518 / L522 —— `.panel-header { height: 36px }` 与 `.collapse-indicator { font-size: 20px; line-height: 1 }`(后者**不得触碰**)
    - `frontend/style.css` L919 —— `#annotation-list { … padding: var(--space-half); }`(2px,是 clearance 预期 13px 的第一段)
    - `frontend/style.css` L501(`#doc-panel-body { padding: var(--space-8) var(--space-10); }`)、L524(`.panel-body { padding: var(--space-2-5); }`)、L923-929(`.annotation-item { padding: var(--space-2) var(--space-2-5); border: 1px solid … }`)—— L-5 预期 clearance 链的三段依据
    - `frontend/app.js` L1150-1156 —— `renderAnnotations` 把 AI 答复渲染成 `<details>` + `<summary>`;`<summary>` 默认可聚焦。**这是 `#annotation-list` 确有可聚焦后代的证据**,也是 item 9 命中区普查必须能造出该元素的依据;**只读不改**
    - `frontend/app.js` L260-285 —— `appendSayToChat` / 流式气泡(气泡是 `div` 与 `p`,无 `button`、无 `details`/`summary`)—— `#chat-messages` **无可聚焦后代**的证据;**只读不改**
    - `scripts/check-05-ui-uat.py` 本阶段 item 9 全文 —— 滚动者普查 / 末条可达性 / `max-height` / 保留项护栏;本任务**追加**两条普查断言,不改既有四条
    - `scripts/check-05-ui-uat.py` L346-380 —— `resolve_color` / `resolve_token`;L258-262 —— `read_style`
  </read_first>
  <action>
    **第 1 步 —— L-6:先实测,再只对未达标者施加(机制锁定)。**

    实跑 `.venv/bin/python scripts/check-05-ui-uat.py --item 8`,取三项只读诊断中的**命中区普查**那一项,并对照 `idi-06-01-SUMMARY.md` 里已记的 < 24×24 清单。**只对实测宽或高 < 24px 的可交互元素施加**,已达标者**零改动**。

    机制逐字锁定:在该控件的**既有规则体内原地加两行** —— `min-height: 24px;` 与 `min-width: 24px;`。**不得动现有 `padding`**;**不得用 `::after` 撑开**;**不得改 `font-size`**。`24px` 是**裸字面量**(尺寸族,非间距族),刻意不写成 `var(--space-6)` —— 24 是 WCAG 2.5.8 的目标尺寸常数,挂在间距刻度上会让一次间距改动静默地把命中区压到下限之下。规则体上方加一段注释写明这两点(为什么是裸字面量、为什么不用 padding / `::after`)。

    按 UI-SPEC 的判定,预期落点是 **`.annotation-answer summary`**(`font-size: var(--text-xs)` = 12px、无 padding、无 min-height ⇒ ≈14–17px)。其既有四条声明(`cursor: pointer` / `color: var(--color-text-muted)` / `font-size: var(--text-xs)` / `margin-top: var(--space-1)`)**逐字保留**。若实测发现**其他**控件也不达标,同样按上款处理;若实测发现某控件**没有既有规则**(如 `#selection-menu button` 若有独立规则则就地改,否则追加一条新规则到文件末尾)—— 那种情况下必须在 SUMMARY 里登记为新增规则。**`.collapse-indicator` 不得进入待修清单** —— 它是 `<span>` 且属不得触碰,其可点父级 `.panel-header` 为 36px。

    **第 2 步 —— L-5:先普查,再只在实测 clearance < 4px 的容器上抬 padding。**

    取 `idi-06-01-SUMMARY.md` 的 **clearance 普查表**,并**重新实测确认**(item 8 的该项诊断每次跑都会重算,故取本次运行的读数)。判据逐字:一个**裁剪容器**(计算 `overflow != visible`)必须让它的每一个可聚焦后代距离其 **padding 边**至少 **4px**(= Phase 7 的 `outline: 2px solid` + `outline-offset: 2px` 的环外伸量)。

    - **实测与静态分析预期一致**(预期:`#annotation-list` 的 `<summary>` clearance ≈ 13px = 2px 列表 padding + 1px 卡片 border + 10px 卡片 padding;`#chat-messages` **无可聚焦后代** ⇒ 空动作;`#latest-check` 无;`#main-pane` ≥10px 由 `.panel-body` 的 10px 撑开;`#doc-panel` 由 `#doc-panel-body` 的 32/40px 撑开)⇒ **不改任何 padding**;把这条交付物登记为**「被实测推翻」**,并在 SUMMARY 附普查原始数据(元素 × 最近裁剪祖先 × 实测 clearance)。
    - **实测某容器 clearance < 4px** ⇒ **只改那一个容器**,取值 `var(--space-1)`(4px),并登记为**视觉变更**。
    - **禁止「为确定性四个全抬」** —— 那会移动 `#main-pane` 居中布局下四个 section 的位置,并与 `#doc-panel-body` 的 `padding: var(--space-8) var(--space-10)` 叠加。

    **第 3 步 —— item 9 追加两条普查断言(两条都按 DOM 普查算,不硬编码选择器列表)。**

    - **(a) clearance 断言:** 在 `page.evaluate` 里,对每个计算 `overflow != visible` 的容器,枚举其可聚焦后代(`button` / `input` / `select` / `textarea` / `a[href]` / `summary` / `[tabindex]`),算出每个后代到该容器 padding 边的最小距离,返回「容器 × 元素 × clearance」的扁平数组。Python 侧断言**所有** clearance ≥ 4px;`info()` 里打印完整数组。数组为空时用 `info()` 报告「无裁剪容器 × 可聚焦后代组合」,**不记断言**(避免空转 PASS);探针返回 `null` ⇒ `blocked(...)`。
    - **(b) 命中区断言:** 在 `page.evaluate` 里枚举每个可交互元素(`button` / `input` / `select` / `textarea` / `summary` / `[role=button]` / `[onclick]`),返回 `getBoundingClientRect()` 的宽与高。Python 侧断言**所有**宽 ≥ 24 且高 ≥ 24;`info()` 里打印完整数组与未达标清单。**必须先用应用自身的 `renderAnnotations` 造出 `.annotation-answer summary`** —— 它是本断言的主要对象,若它不存在则该断言失去证明力 ⇒ 先断言该元素存在,不存在则 `blocked(...)`。
    - 两条断言都**只追加**,不改 item 9 既有的四条(滚动者普查两条 / 末条可达性 / `max-height` 两条 / 保留项护栏两条)。

    **第 4 步 —— 运行时验证(硬规则 7)。** 实跑 `--item 9`(新断言)与 `--item smoke,1,4,7,8`(既有项无回归)。把两条 Delta(D6-3 `.annotation-answer summary` 从 ≈14–17px 抬到 ≥24px ⇒ `.annotation-item` 高度 +7…10px;D6-10 L-5 的条件 padding 抬升——若未发生则明确写「本项不存在」)登记进 SUMMARY。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 9</automated>
    <fails_when>exit code is not 0, or the `=== 逐项结论 ===` block reports anything other than `item 9: PASS`, or any assertion line reports `FAIL` or `BLOCKED`</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,4,7,8</automated>
    <fails_when>exit code is not 0, or the summary reports anything other than `item smoke: PASS`, `item 1: PASS`, `item 4: PASS`, `item 7: PASS`, `item 8: PASS`</fails_when>
    <automated>grep -o 'min-height: 24px;' frontend/style.css | wc -l; grep -o 'min-width: 24px;' frontend/style.css | wc -l</automated>
    <fails_when>the two counts are not equal, or either is less than 1 (the measured under-sized interactive controls each receive both declarations)</fails_when>
    <automated>grep -n -A 8 '^\.annotation-answer summary {' frontend/style.css | grep -o 'min-height: 24px;' | wc -l; grep -n -A 8 '^\.annotation-answer summary {' frontend/style.css | grep -o 'min-width: 24px;' | wc -l</automated>
    <fails_when>either count is not exactly 1</fails_when>
    <automated>grep -n -A 8 '^\.annotation-answer summary {' frontend/style.css | grep -oE '(font-size: var\(--text-xs\);|cursor: pointer;|color: var\(--color-text-muted\);|margin-top: var\(--space-1\);)' | wc -l</automated>
    <fails_when>the count is not exactly 4 (the four pre-existing declarations must survive verbatim — only two size declarations are added)</fails_when>
    <automated>grep -o 'font-size: 20px;' frontend/style.css | wc -l; grep -o 'line-height: 1;' frontend/style.css | wc -l</automated>
    <fails_when>either count is not exactly 1 (`.collapse-indicator` is on the do-not-touch list — backlog 999.1)</fails_when>
    <automated>grep -c ':focus-visible' frontend/style.css; grep -c ':focus ' frontend/style.css</automated>
    <fails_when>either count is not 0 (focus styling is A11Y-01 / Phase 7 — this phase only removes the clipping that would cut the ring)</fails_when>
    <automated>grep -o 'clearance' scripts/check-05-ui-uat.py | wc -l; grep -o 'getBoundingClientRect' scripts/check-05-ui-uat.py | wc -l</automated>
    <fails_when>the first count is less than 1, or the second count is less than 3 (item 9 gains a clearance census and a hit-area census on top of the reachability reads)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>any of the three prints anything other than exactly `PASS`, or exits non-zero</fails_when>
    <automated>python3 scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>the last line is not exactly `PASS: 0 failures`</fails_when>
    <automated>grep -o 'min-height: 24px;' frontend/style.css | wc -l; grep -o 'min-height: 160px;' frontend/style.css | wc -l; grep -o 'min-height: 200px;' frontend/style.css | wc -l; grep -o 'min-height: 52px;' frontend/style.css | wc -l</automated>
    <fails_when>the second, third or fourth count is not exactly 1 (the pre-existing un-tokenised size literals must survive — 24px belongs to that family and does not displace any of them)</fails_when>
  </verify>
  <acceptance_criteria>
    - `min-height: 24px;` 与 `min-width: 24px;` 的声明数相等且 ≥ 1;**只施加于实测 < 24×24 的可交互元素**
    - `.annotation-answer summary` 规则体内含 `min-height: 24px;` 与 `min-width: 24px;` 各 1 处,且其既有四条声明逐字保留(计数 == 4)
    - 若实测发现其他未达标控件,其落点与形态记入 SUMMARY(就地改 / 新增规则必须写明是哪种);已达标控件**零改动**
    - `.collapse-indicator` 的 `font-size: 20px;` 与 `line-height: 1;` 逐字保留(计数各 == 1),未被列入待修清单
    - `frontend/style.css` 内 `:focus-visible` 与 `:focus ` 计数均为 0(本阶段不写焦点规则)
    - L-5 的结论已登记:或「零 padding 改动 + 被实测推翻 + 普查原始数据」,或「只改那一个容器为 `var(--space-1)` + 视觉变更登记」;`#main-pane` / `#doc-panel` / `#chat-messages` / `#latest-check` 四者**未**被「为确定性全抬」
    - item 9 追加两条普查断言(clearance ≥ 4px;可交互元素宽高均 ≥ 24px),两条都按 DOM 遍历算出;`.annotation-answer summary` 在命中区断言前先被 `renderAnnotations` 造出并断言存在
    - item 9 既有的四条断言(滚动者普查两条 / 末条可达性 / `max-height` 两条 / 保留项护栏两条)未被改动
    - `idi-06-03-SUMMARY.md` 登记 D6-3(必然发生)与 D6-10(仅在 L-5 实改时发生;否则写明「本项不存在」)
    - 既有未令牌化尺寸字面量(`min-height: 160px;` / `200px;` / `52px;`)各仍为 1 处
    - `--item 9` 全 PASS(0 FAIL / 0 BLOCKED);`--item smoke` / `1` / `4` / `7` / `8` 五项仍全 PASS
    - `bash scripts/check-01-token-conformance.sh` / `check-03` / `check-04` 均 `PASS`;`check-02` 仍 `PASS: 0 failures`
  </acceptance_criteria>
  <done>A11Y-07 按可交互元素普查施加 —— 实测 < 24×24 的控件(预期为 `.annotation-answer summary`)各获 `min-height: 24px;` + `min-width: 24px;` 两条裸字面量声明,既有四条声明逐字保留,`.collapse-indicator` 未被触碰;L-5 的 clearance 普查按 4px 判据得出结论并只在该改的容器上改(或登记为被实测推翻并附原始数据);item 9 追加两条普查断言且全绿;两条 Delta(D6-3 / D6-10)登记进 SUMMARY。</done>
</task>

<task type="auto">
  <name>Task 3: D-19 连带复验(`idi-04.1-radix`)+ 全量门禁收口</name>
  <files>scripts/check-05-ui-uat.py</files>
  <read_first>
    - `.planning/phases/idi-04.1-radix/idi-04.1-VERIFICATION.md` frontmatter —— `covered_files` 十三条清单(含 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`)、`covered_digest: "v1:sha256:25d5f1fe…"`、`score: 37/38`、`behavior_unverified: 0`;**正文与 frontmatter 一律不改**
    - `.planning/phases/idi-04.1-radix/idi-04.1-VERIFICATION.md` L230-250 —— 该报告自己记录的指纹重算历史与「`REQUIREMENTS.md` 同时在 `idi-04` 与本报告的 `covered_files` 里」的结构性观察。**只读不改**
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-03-SUMMARY.md` §`D-05 复验记录` —— **本次的范本**:指纹的义务归属(写回由 `/gsd-verify-work idi-04.1-radix` 执行)、四条守卫的复跑结果、三项 `human_verification` 的照实记录、三处 04.1 结论 + 数量差值的逐条重算表。**照抄它的结构**
    - `.planning/STATE.md` §Operator Next Steps 第 2 条 —— `idi-04.1-radix` 的复验义务仍未收口(Phase 5 已把输入备齐但未写指纹),本阶段在其上**再叠一层**;判据取 HEAD 内容,不看 mtime
    - `scripts/check-02-contrast.py` —— 复验要重算的四条数值(47 对清单、`ORDER 0.363`、`--color-text-info ON --color-surface-info` 4.53、冻结轮 `opacity` / `filter` / `box-shadow`)的来源。**只读不改**
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`## 契约校验命令` —— 四条既有守卫 + 两条扩写门(item 8 / item 9)+ 必须保留的既有门(item 4 / item 7 / item 1)
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`## Registry Safety` —— `frontend/vendor/` 含**恰好一个文件**(`marked.min.js`),本阶段每个计划之后都必须仍是恰好一个文件
    - `.planning/phases/idi-06-layout-robustness/idi-06-01-SUMMARY.md` §`测量决策记录` 与 `.planning/phases/idi-06-layout-robustness/idi-06-02-SUMMARY.md` —— 全量收口时要复核的既有数值
  </read_first>
  <action>
    **第 1 步 —— 全量门禁复跑(收口门,必须在全部 CSS / harness 改动之后执行)。**

    实跑并逐条记录原始输出:`bash scripts/check-01-token-conformance.sh`、`python3 scripts/check-02-contrast.py`(记 `tail -1` 与配对数、`ORDER` 行)、`bash scripts/check-03-hidden-uniqueness.sh`、`bash scripts/check-04-important-count.sh`、`.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8,9`、`.venv/bin/python scripts/check-06-idi05-validation.py`。**第 5 项(item 5)的 `--ai-smoke` 半边需要真实 AI 调用与计费** —— 按已记录的处置单独跑 `.venv/bin/python scripts/check-05-ui-uat.py --item 5`(非 AI 半边)并在 SUMMARY 里注明其 AI 半边沿用已记录的证据,不重复计费。

    任何一条不绿即为停止条件:**先修根因,不得在本任务里绕过或降级断言**。把每一项的逐项结论(条数 / FAIL / BLOCKED)与执行前基线表并列记入 SUMMARY。

    **第 2 步 —— D-19 的连带复验证据(照 `idi-05-03` 的结构写)。**

    **义务归属先写清:** `idi-04.1-radix` 的 `covered_digest` 因 `frontend/style.css` 与 `scripts/check-05-ui-uat.py` 被本阶段改写而 **stale**;成因是**内容真变**,故走**重新验证**而非补指纹。**指纹的重新写回由编排器执行 `/gsd-verify-work idi-04.1-radix`** —— 本任务提供它的输入。**不得改写 `idi-04.1-VERIFICATION.md` 的 frontmatter 或正文**,以保住「谁改了什么」的可追溯性(验收用 `git status --porcelain -- .planning/phases/idi-04.1-radix/` 为空证明)。

    然后以 HEAD 内容重算并逐条记录:

    - **四条守卫:** CHECK-01 / 02 / 03 / 04 的结果(第 1 步已跑,直接引用)。
    - **04.1 的 `covered_files` 十三条的现状:** 逐条给出该文件相对 04.1 收口时是否变化(本阶段只改 `frontend/style.css` 与 `scripts/check-05-ui-uat.py` 两条;其余十一条应零变化)。若可逐字复现 04.1 声明的 sha256 方案,给出重算后的 `v1:sha256:<hex>`;若无法逐字复现该方案,**照实写明「本计划未能复现该指纹方案,只提供逐文件的 sha256 与变更清单,写回留给 `/gsd-verify-work idi-04.1-radix`」** —— 不得凭猜测填一个值。
    - **04.1 的三处结论 + 数量差值(逐条从 HEAD 重算):** 清单规模与 `ORDER` 行;`--color-text-info ON --color-surface-info` 的比值;冻结轮的 `opacity` / `filter` / `box-shadow` 三值。Phase 5 已记过一轮(`ORDER 0.363` / 4.53 / `1` + `saturate(0.6)` + `inset 3px 0 0` 琥珀);本阶段**零颜色改动**,故这些值必须**逐字不变** —— 若有一处变了,说明本阶段意外触碰了颜色层,那是停止条件。
    - **三项 `human_verification`:** 照实记录其状态,**不静默转绿**(Phase 5 已记录 TOKEN-07 的序关系半场仍是 manual-only,本阶段不得单方面翻转)。

    **第 3 步 —— 零外溢与范围锁复核。** 逐条确认:`git status --porcelain -- frontend/app.js frontend/index.html frontend/vendor/ scripts/ui-states/ scripts/check-01-token-conformance.sh scripts/check-02-contrast.py scripts/check-03-hidden-uniqueness.sh scripts/check-04-important-count.sh scripts/check-06-idi05-validation.py` 输出为空;`ls frontend/vendor/` 只有 `marked.min.js`;`.planning/phases/idi-04.1-radix/` 零改动;`ROADMAP.md` / `REQUIREMENTS.md` / `04-UI-SPEC.md` 正文零改动(口径登记只写在计划与 SUMMARY 里)。

    **第 4 步 —— 把「测量决策记录」的最终态写进 SUMMARY。** 本阶段的三个实测驱动决策(L-2 守卫是否落地、L-5 是否抬 padding、L-6 的落点清单)必须在本 SUMMARY 里有**最终裁定**,并各自附原始数值与依据 —— 这是后续 `/gsd-verify-work idi-06` 与本里程碑收口的唯一入口。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>any of the three prints anything other than exactly `PASS`, or exits non-zero</fails_when>
    <automated>python3 scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>the last line is not exactly `PASS: 0 failures`</fails_when>
    <automated>python3 scripts/check-02-contrast.py | grep '^ORDER 0.363  --color-text-muted before --color-text on --color-surface' | wc -l</automated>
    <fails_when>the count is not exactly 1 (this phase makes zero colour changes — the ordering line must be byte-identical to the pre-execution baseline)</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8,9</automated>
    <fails_when>exit code is not 0, or the summary reports any item other than PASS for smoke, 1, 2, 3, 4, 6, 7, 8, 9</fails_when>
    <automated>.venv/bin/python scripts/check-06-idi05-validation.py</automated>
    <fails_when>exit code is not 0, or the summary reports any item other than PASS</fails_when>
    <automated>git status --porcelain -- .planning/phases/idi-04.1-radix/</automated>
    <fails_when>the output is not empty (the fingerprint write-back belongs to `/gsd-verify-work idi-04.1-radix`; this plan only supplies evidence)</fails_when>
    <automated>git status --porcelain -- frontend/app.js frontend/index.html frontend/vendor/ scripts/ui-states/ scripts/check-01-token-conformance.sh scripts/check-02-contrast.py scripts/check-03-hidden-uniqueness.sh scripts/check-04-important-count.sh scripts/check-06-idi05-validation.py</automated>
    <fails_when>the output is not empty</fails_when>
    <automated>git status --porcelain -- .planning/ROADMAP.md .planning/REQUIREMENTS.md .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md</automated>
    <fails_when>the output is not empty (changing these would invalidate already-passed verification fingerprints; deviations are registered in plans and summaries only)</fails_when>
    <automated>ls frontend/vendor/ | wc -l</automated>
    <fails_when>the count is not exactly 1 (`frontend/vendor/` must keep containing exactly `marked.min.js`; no dependency was added or removed)</fails_when>
  </verify>
  <acceptance_criteria>
    - 四条既有守卫全绿:`check-01` / `check-03` / `check-04` 各打印 `PASS`;`check-02` 打印 `PASS: 0 failures`
    - `check-02` 的 `ORDER 0.363` 行逐字不变(本阶段零颜色改动)
    - `--item smoke,1,2,3,4,6,7,8,9` 九项全 PASS(0 FAIL / 0 BLOCKED);`check-06-idi05-validation.py` 全 PASS
    - item 5 的非 AI 半边已跑并记录;其 `--ai-smoke` 半边沿用已记录证据,SUMMARY 明确写出这一处置
    - SUMMARY 含 `idi-04.1-radix` 连带复验的证据块:义务归属(写回属 `/gsd-verify-work idi-04.1-radix`)、四条守卫结果、`covered_files` 十三条的变化清单(只有 `frontend/style.css` 与 `scripts/check-05-ui-uat.py` 两条变化)、三处 04.1 结论数值的重算结果、三项 `human_verification` 的照实状态(不静默转绿)
    - 若无法逐字复现 04.1 的 sha256 方案,SUMMARY 照实写明「未能复现」并只提供逐文件 sha256 与变更清单 —— **不得填入猜测的指纹值**
    - `git status --porcelain -- .planning/phases/idi-04.1-radix/` 输出为空(`idi-04.1-VERIFICATION.md` 一字未改)
    - `frontend/app.js` / `frontend/index.html` / `frontend/vendor/` / `scripts/ui-states/` / `check-01`…`check-04` / `check-06` 零改动(`git status --porcelain` 为空)
    - `ROADMAP.md` / `REQUIREMENTS.md` / `04-UI-SPEC.md` 正文零改动(口径登记只写在计划与 SUMMARY 里)
    - `frontend/vendor/` 仍恰好 1 个文件
    - SUMMARY 含「测量决策记录」的最终态:L-2 / L-5 / L-6 三个实测驱动决策各有最终裁定 + 原始数值 + 依据
  </acceptance_criteria>
  <done>四条既有守卫 + 九项 harness + `check-06` 全绿;`idi-04.1-radix` 的连带复验证据(四条守卫、`covered_files` 变化清单、三处结论数值、三项 `human_verification` 照实状态)记入 SUMMARY 且报告文件一字未改;零外溢复核通过;三个实测驱动决策的最终裁定与原始数值落盘。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 无网络边界 | 本阶段只改两份**本地静态文件**(`frontend/style.css` + `scripts/check-05-ui-uat.py`)。运行期唯一外部接口是 Playwright 驱动本机浏览器访问 `127.0.0.1` 上的本地服务;无入站、无出站、无凭据、无多用户。 |
| 构建/依赖边界 | 零新增依赖、零新增构建步骤。`frontend/vendor/` 维持恰好一个文件。 |
| 门禁可信边界 | 本阶段**同时改写被测物与被测物的一道门**(`check-05-ui-uat.py`),故「门通过」不等于「改动正确」—— 需要反向证据(见下)。 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi06-01 | Tampering | `scripts/check-05-ui-uat.py` item 8 / item 9 的新断言 | high | mitigate | 新断言**必须能失败**:item 9 的命中区断言在断言前先 `ok_true` 该元素(`.annotation-answer summary`)存在,不存在则 `blocked(...)` —— 复刻 item 7 已记录的 `all(w != "700")` 在 `None` 上恒真的陷阱。`getBoundingClientRect` 对缺失元素返回全零矩形,故每条几何断言都必须先确认元素可见且矩形非零,否则记 `blocked(...)` 而非 PASS。验收:反向验证 —— 临时注释掉 `.annotation-answer summary` 的两条尺寸声明后重跑 `--item 9`,该断言必须 FAIL;恢复后必须 PASS。 |
| T-idi06-02 | Repudiation | 「测量决策记录」的数值来源 | medium | mitigate | 三个实测驱动决策(L-2 / L-5 / L-6)的判据数值必须**逐行落盘**并与波次 1 基线并列;SUMMARY 必须写明走了哪一支。禁止只写结论(UI-SPEC L-2 明文)。 |
| T-idi06-03 | Tampering | 既有验证指纹 `idi-04.1-radix` | medium | mitigate | 本阶段必然令其 `covered_digest` stale(成因:内容真变)。处置:本计划只提供重算证据,`git status --porcelain -- .planning/phases/idi-04.1-radix/` 必须为空;指纹写回由 `/gsd-verify-work idi-04.1-radix` 执行。同时**不改** `ROADMAP.md` / `REQUIREMENTS.md` / `04-UI-SPEC.md` 正文(改它们会作废另外两个已通过的指纹)。 |
| T-idi06-04 | Information disclosure | 无 | low | accept | 无凭据、无 PII、无网络传输、无日志外发。本阶段新增的运行时读数只有元素尺寸与滚动几何,留在本地 SUMMARY 里。 |
| T-idi06-05 | Denial of service | `--item 5 --ai-smoke` 的真实 AI 调用 | low | accept | 该项需要本机 claude CLI 登录且会产生调用计费。处置:非 AI 半边照跑,AI 半边沿用已记录证据、不重复计费。这是成本约束而非安全风险。 |
| T-idi06-06 | Elevation of privilege | 无 | low | accept | 无认证、无授权、无会话、无服务端代码改动。工具为单机单人本地运行(D-03)。 |
| T-idi06-SC | Tampering | npm / pip / cargo 安装 | high | mitigate | **本阶段零新增依赖**:`frontend/vendor/` 维持恰好一个文件(`marked.min.js`,已在库);`scripts/check-05-ui-uat.py` 只用既有 Playwright 与标准库。故无需包合法性审计门,也**不得**在本阶段引入任何新包。验收:`ls frontend/vendor/ \| wc -l` == 1,且无 `package.json` / `requirements.txt` 改动。 |
</threat_model>

<verification>
**自动化门(全部必须在收口时绿):**

```bash
bash scripts/check-01-token-conformance.sh
python3 scripts/check-02-contrast.py | tail -1
bash scripts/check-03-hidden-uniqueness.sh
bash scripts/check-04-important-count.sh
.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8,9
.venv/bin/python scripts/check-06-idi05-validation.py
```

**条件交付物的判据(二选一,由 SUMMARY 记录的那一支决定):**

```bash
grep -c '^@media (max-width: 1023px) {' frontend/style.css   # 写出守卫 ⇒ 1;登记推翻 ⇒ 0
grep -c 'var(--[a-z0-9-]*,' frontend/style.css                # 恒为 0(硬规则 4)
```

**范围锁:**

```bash
git status --porcelain -- frontend/app.js frontend/index.html frontend/vendor/ scripts/ui-states/
git status --porcelain -- .planning/phases/idi-04.1-radix/
git status --porcelain -- .planning/ROADMAP.md .planning/REQUIREMENTS.md
```

**反向验证(T-idi06-01,证明新门真的会失败):** 临时注释掉 `.annotation-answer summary` 的两条尺寸声明 → 重跑 `--item 9` → 命中区断言必须 FAIL → 恢复 → 必须 PASS。临时删掉 `@media` 块(若存在)→ 重跑 `--item 8` → 守卫形态断言必须 FAIL → 恢复 → 必须 PASS。**这是唯一能证明守卫不是恒真的手段**;两组反向验证的原始输出记入 SUMMARY。
</verification>

<success_criteria>
- LAYOUT-02 关闭:三宽度在波次 2 之后的树上重测,原始数值落盘,并按 UI-SPEC §L-2 的决策规则走出唯一一支(写出恰好一条守卫 / 登记被实测推翻);item 8 的 1440 与 1024 两处文档级溢出升为硬断言
- A11Y-07 关闭:按可交互元素普查施加 `min-height: 24px` + `min-width: 24px`,只落在实测 < 24×24 者(预期仅 `.annotation-answer summary`);`.collapse-indicator` 未被触碰;既有四条声明逐字保留
- L-5 关闭:clearance 普查按 4px 判据得出结论并只在该改的容器上改(或登记被实测推翻 + 原始数据)
- item 9 追加两条普查断言(clearance / 命中区),且经反向验证证明会失败
- D-19 义务履行:04.1 的连带复验证据记入 SUMMARY,`idi-04.1-VERIFICATION.md` 一字未改,指纹写回明确留给 `/gsd-verify-work idi-04.1-radix`
- 全部既有门绿:check-01 / 02 / 03 / 04 / 06 + `--item smoke,1,2,3,4,6,7,8,9`
- 零外溢:`frontend/app.js` / `index.html` / `vendor/` / `scripts/ui-states/` / `check-01`…`check-04` / `check-06` 零改动;围栏 `:root` 内零改动;零新增令牌;零 `:focus` / `:hover` / `:active` / `transition` 规则;`ROADMAP.md` / `REQUIREMENTS.md` / `04-UI-SPEC.md` 正文零改动
- 三个实测驱动决策各有最终裁定 + 原始数值 + 依据,写在 `idi-06-03-SUMMARY.md`
</success_criteria>

<output>
Create `.planning/phases/idi-06-layout-robustness/idi-06-03-SUMMARY.md` when done

SUMMARY 必含以下小节(缺一即视为未完成):
1. `## 测量决策记录(最终态)` —— L-2 / L-5 / L-6 三个实测驱动决策各一行裁定 + 原始数值 + 依据
2. `## 三宽度对照` —— 波次 1 基线与波次 2 之后的新数值并列
3. `## 守卫形态` —— 走了哪一支(写出守卫 / 被实测推翻),及对应证据
4. `## 命中区普查` —— 可交互元素 × 实测宽高 × 是否施加尺寸下限
5. `## clearance 普查` —— 裁剪容器 × 可聚焦后代 × 实测 clearance × 是否抬 padding
6. `## Delta 登记` —— D6-3(必然)与 D6-10(仅在实改时)
7. `## D-19 连带复验记录` —— 照 `idi-05-03-SUMMARY.md` §`D-05 复验记录` 的结构:义务归属、四条守卫、`covered_files` 变化清单、三处结论数值重算、三项 `human_verification` 照实状态
8. `## 反向验证原始输出` —— 两组(命中区 / 守卫形态)的「注释掉 → FAIL → 恢复 → PASS」原始输出
9. `## 全量门禁逐项结论` —— 与执行前基线表并列
</output>
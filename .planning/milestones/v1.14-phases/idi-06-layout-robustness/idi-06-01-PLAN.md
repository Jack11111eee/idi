---
phase: idi-06-layout-robustness
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - frontend/style.css
  - scripts/check-05-ui-uat.py
autonomous: true
requirements:
  - LAYOUT-01
  - LAYOUT-03

estimate:
  tokens: 52000
  raw_tokens: 52000
  tasks: 2
  confidence: low

must_haves:
  truths:
    # ---- lifted from idi-06-UI-SPEC.md `## UI Considerations` — explicit tier (8 of 24; E1/E2/E3) ----
    - "E1 `#doc-panel-header`(sticky 表头)`overflow`:`#doc-panel` 是滚动容器、`#doc-panel-header` 是其直接 flex 子项,故 `position: sticky; top: 0` 生效:滚动面板正文时表头钉在面板顶部,正文首行不被遮住。门:`check-05 --item 8` ← UI-SPEC UI-Considerations E1 `overflow`(explicit)"
    - "E1 `#doc-panel-header`(sticky 表头)`long-text`:sticky 条在 `--doc-panel-w` 最小宽 340px 下仍单行 —— 最宽文案是 `#state-badge` 的 9 字 + `文档区` h1,不折断、不换行。门:768/1024/1280 三处实检(L-1 的门)← UI-SPEC UI-Considerations E1 `long-text`(explicit)"
    - "E2 `#state-badge` `overflow`:`#state-badge` 是流内元素(无 `position`、无 `right`,HEAD `style.css:671-679`),结构上不可能遮挡正文;本阶段不得把它改回 fixed。徽标随 sticky 条钉住,滚动时恒可见 ← UI-SPEC UI-Considerations E2 `overflow`(explicit)"
    - "E2 `#state-badge` `long-text`:最宽 badge 文案(阶段 1-12 / 自检档,9 字)在 340px 面板最小宽下不溢出、不换行,不把 `#doc-panel-header` 撑破。该文案是 L-1 碰撞实检的输入 ← UI-SPEC UI-Considerations E2 `long-text`(explicit)"
    - "E3 `#stream-banner` `loading`:重连中态由 `#stream-banner` 的非 `.fatal` 形态承载,对比度 4.78:1 保持 AA;本阶段零改动 ← UI-SPEC UI-Considerations E3 `loading`(explicit)"
    - "E3 `#stream-banner` `error`:致命态由 `.fatal` 修饰符承载,`.fatal` 必须保留为独立选择器,对比度 4.76:1 保持 AA;门:`check-02-contrast.py` 两态实测 ← UI-SPEC UI-Considerations E3 `error`(explicit)"
    - "E3 `#stream-banner` `overflow`:`#stream-banner` 与 `#state-badge` 的相交条件是视口 < 490px,低于本阶段 768px 下限 ⇒ 残余碰撞不存在;门:768 / 1024 / 1280 三处实检横幅不盖 badge(L-1 的门)← UI-SPEC UI-Considerations E3 `overflow`(explicit)"
    - "E3 `#stream-banner` `long-text`:横幅文案「事件流已断开,正在自动重连……」在 768px 下不折断、不换行溢出,且不因换行而增高到遮挡 badge ← UI-SPEC UI-Considerations E3 `long-text`(explicit)"
    # ---- lifted from idi-06-UI-SPEC.md `## UI Considerations` — backstop tier (2 of 19; E1) ----
    - statement: "E1 `#doc-panel-header`(sticky 表头)`loading`:数据或内容仍在加载时显示什么(skeleton / spinner / 渐进呈现)?本阶段对该状态维度零改动,文案与显隐机制一字不动(见 Copywriting Contract 冻结表)。"
      verification: backstop
    - statement: "E1 `#doc-panel-header`(sticky 表头)`error`:加载或提交失败时显示什么(消息 / 重试入口 / 部分回退)?本阶段对该状态维度零改动;断流态由 `#stream-banner` 承载,本阶段零改动。"
      verification: backstop
    # ---- phase-specific truths ----
    - "`frontend/style.css` 围栏外新增恰好一条 `#doc-panel-header` 规则,声明体为 `position: sticky` / `top: 0` / `background: var(--color-surface)` / `border-radius: 0`,插在既有规则块 `#doc-panel.collapsed #doc-panel-header { justify-content: center; padding-inline: 0; }` 之后 ← L-1 / D-03 / D-05"
    - "`#state-badge` 的流内机制一字不动:它仍无 `position` 声明、无 `right` 声明、仍是 `#doc-panel-header` 的子元素;其 `z-index: var(--z-badge)` 声明必须保留 ← L-1 承重约束 1 / D-03"
    - "新规则**不加** `z-index`:sticky 元素是 positioned,默认画在静态内容之上;若实测出现穿透再补,届时须连带登记 `--z-*` 的序关系(badge 10 < banner 20 < overlay 100 < selection-menu 200)← L-1 承重约束 2"
    - "折叠态零改动:`#doc-panel.collapsed` 的三条规则(含 `#state-badge { display: none }`)逐字不变,登记为**有意设计**而非缺口 ← L-1 承重约束 3 / D-04"
    - "`background: var(--color-surface)` 复用 `#doc-panel` 自身已消费的令牌(`style.css:474`)⇒ 本阶段零新增令牌,围栏 `:root` 内零改动 ← L-1 / 硬规则 8 / 硬规则 5"
    - "`scripts/check-05-ui-uat.py` 新增 item 8 并接入派发三处(`normalize_items` 默认列表 / `known` 集合 / `main()` 派发),`--item 8` 可单跑 ← D-06 / PATTERNS.md E-7"
    - "item 8 的 L-1 三条断言齐备:(a) `#state-badge` 计算 `position` 为 `static` 且 `right` 无声明;(b) 768 / 1024 / 1280 三处 `#state-badge` 与 `#stream-banner` 的 `getBoundingClientRect()` 不相交;(c) 滚动 `#doc-panel` 到底后 `#doc-panel-header` 仍可见 ← D-06"
    - "item 8 的三宽度断言在测量前先证明前提成立:badge 可见(计算 `display != none`)且 banner 被应用自身的 `showStreamBanner(...)` 置为可见;两者的 rect 均非全零,否则记 BLOCKED 而非 PASS ← PATTERNS.md E-2 / E-8 的「绝不记假 PASS」纪律"
    - "item 8 的 sticky 断言先证明 `#doc-panel` 真的可滚(`scrollHeight > clientHeight`),否则记 BLOCKED —— 不可滚的容器上「滚到底后表头仍可见」是空转断言 ← PATTERNS.md E-2"
    - "item 8 是 harness 里**第一次**变更 viewport(`page.set_viewport_size`),必须在返回前恢复 1440×900,否则污染后续项 ← PATTERNS.md E-3"
    - "`bash scripts/check-01-token-conformance.sh` 打印 `PASS` 且 exit 0(围栏外裸 `#hex` 仍为 0)← CHECK-01 / 硬规则 5"
    - "`python3 scripts/check-02-contrast.py` 仍打印 `PASS: 0 failures`,清单规模与 `ORDER` 行逐字不变(本计划零颜色改动)← CHECK-02"
    - "`bash scripts/check-03-hidden-uniqueness.sh` 打印 `PASS`(`^\\.hidden {` 计数 == 1)← CHECK-03 / 硬规则 1"
    - "`bash scripts/check-04-important-count.sh` 打印 `PASS`(`!important` **声明**数 == 1)← CHECK-04 / 硬规则 2"
    - "既有门无回归:`--item smoke` / `--item 1` / `--item 4` / `--item 7` 四项在改动后仍全 PASS(0 FAIL / 0 BLOCKED)← 硬规则 7 / D-20"
    - "运行时:item 8 在真实浏览器里读到 `#state-badge` 的 computed `position` 为 `static`,且 768 / 1024 / 1280 三处 badge × banner 的 rect 不相交;滚动 `#doc-panel` 到底后 `#doc-panel-header` 的 rect 仍落在 `#doc-panel` 的可视区内 ← 硬规则 7 / D-06"
    - "item 8 打印三项只读诊断的**原始数值**(供计划 03 消费):1440 / 1024 / 768 三处的文档级 `scrollWidth` 与 `clientWidth`;可聚焦元素 × 最近裁剪祖先 × 实测 clearance 的普查表;可交互元素的 `getBoundingClientRect()` 普查表。三者一律经 `info()` 输出,**本计划不把它们升为断言**(前两项的判据要等 L-3 / L-4 落地后才成立,第三项由计划 03 的 A11Y-07 承担)← L-2 / L-5 / L-6 的「实测驱动」+ PATTERNS.md E-6 的「给人核对的锚点」纪律"

  artifacts:
    - path: "frontend/style.css"
      provides: "围栏外新增一条 `#doc-panel-header` 规则(`position: sticky` / `top: 0` / `background: var(--color-surface)` / `border-radius: 0`)与其承重注释;`#state-badge` / `.panel-header` / `#doc-panel.collapsed` 三条规则族逐字不变"
      contains: "position: sticky;"
    - path: "scripts/check-05-ui-uat.py"
      provides: "新增 `def item8(page, tmp_root)`(L-1 三条断言 + 三宽度 / clearance / 命中区三项只读诊断);`normalize_items` 默认列表、`known` 集合、`main()` 派发三处接入 `\"8\"`;模块 docstring 与 `--item` help 同步"
      contains: "def item8"

  key_links:
    - from: "`frontend/style.css` 的 `#doc-panel-header` 规则(1-0-0)"
      to: "`#doc-panel`(`overflow-y: auto`)的滚动行为"
      via: "sticky 的滚动容器是最近的可滚祖先;`#doc-panel-header` 是 `#doc-panel` 的直接 flex 子项,故 `top: 0` 生效"
      pattern: "^#doc-panel-header \\{"
    - from: "`#doc-panel-header` 的 `background: var(--color-surface)`"
      to: "`#doc-panel` 自身的 `background: var(--color-surface)`(`style.css:474`)"
      via: "复用已消费令牌 ⇒ 零新增令牌(硬规则 5 / 硬规则 8)"
      pattern: "background: var\\(--color-surface\\);"
    - from: "`#state-badge` 的流内形态(无 `position` / 无 `right`)"
      to: "`scripts/check-05-ui-uat.py` item 8 的 `read_style(page, \"#state-badge\", \"position\")`"
      via: "运行时 computed style 读取,不靠读源码;元素缺失时 `ok()` 记 BLOCKED"
      pattern: "read_style\\(page, \"#state-badge\", \"position\"\\)"
    - from: "item 8 的三项只读诊断(三宽度 `scrollWidth` / clearance 普查 / 命中区普查)"
      to: "计划 03 的 L-2 决策与 A11Y-07 落点"
      via: "原始数值记入 `idi-06-01-SUMMARY.md`,由 `idi-06-03` 的 `<context>` 消费"
      pattern: "scrollWidth"

  prohibitions:
    - statement: "不得把 `#state-badge` 改回 `position: fixed`,也不得给它加 `position` / 加 `right` / 把它移出 `#doc-panel-header`。HEAD 的流内机制已一次性消掉 LAYOUT-01 的魔法数、LAYOUT-03 的遮挡与 Pitfall M2 碰撞的主因;把它改回浮层会同时复活这三者,并要重开一份已签核的 UI-SPEC 决策(D-03 撤销了契约 Q6 的 calc() 分支与 Pitfall 8 的「不得移入正常流」禁令)。契约侧被推翻的文本见 UI-SPEC §契约修正登记 A-1 / A-2"
      status: active
      verification: flagged
    - statement: "不得为了通过「不相交」「无遮挡」「无溢出」任何一条判据而隐藏、删除或弱化状态读数(`#state-badge`)—— 它是界面唯一的状态指示器,「让碰撞检测通过」不能以丢失状态读数为代价。同理不得移动 `#stream-banner`(含 `position: fixed` / `top: 12px` / `left: 50%`)或弱化它的对比度来通过 L-1 的门;该门断言的是**几何不相交**,不是「横幅不存在」"
      status: active
      verification: flagged
    - statement: "不得删除 `#state-badge` 的 `z-index: var(--z-badge)` 声明(`style.css:678`)。它在静态元素上是惰性的,但 `check-05` item4 有活断言(`#state-badge z-index == var(--z-badge)`),删掉即打破既有门"
      status: active
      verification: flagged
    - statement: "不得给 `#doc-panel-header` 加 `z-index`;不得顺手给 `.panel-header` 补任何声明。若实测出现正文穿透 sticky 条,补 `z-index` 时必须同时登记 `--z-*` 的序关系断言(badge 10 < banner 20 < overlay 100 < selection-menu 200),不得静默新增一个 `--z-*` 消费者"
      status: active
      verification: flagged
    - statement: "不得触碰折叠态:`#doc-panel.collapsed` 的三条规则(含 `#state-badge { display: none }`)逐字不变。折叠是用户**主动**让出空间(48px 竖条放不下 pill 形态),与「横幅盖住 badge」的非自愿丢失性质不同,已登记为有意设计(D-04)"
      status: active
      verification: flagged
    - statement: "不得改动任何用户可见文案,不得触碰 `frontend/app.js` / `frontend/index.html` / `frontend/vendor/`。本阶段唯一允许的浏览器侧调用是应用自身已导出的函数(`showStreamBanner`),不得在 harness 里手工拼 DOM 来伪造被测状态"
      status: active
      verification: flagged

  assumptions:
    # ---- edge probe fallback ($COVERAGE): LAYOUT-01 / LAYOUT-03 rows, ALL unresolved ----
    # The edge probe is an English-cue classifier and misclassified the Chinese requirement prose;
    # `unclassified` stays `unresolved` (never auto-resolved with backstop, never dismissed).
    - statement: "LAYOUT-01 的边缘面未经探针确认(probe 返回 `unclassified — review manually`):「魔法数消除 + 与侧栏宽度决策作为**一个工作单元**」在 HEAD 上的落点是「该魔法数根本不存在」——badge 已是 `#doc-panel-header` 内的流内元素。本计划按已锁决策(D-03 / D-02 第 1 项)只补「恒可见」,并把该行记为 flagged assumption 而非已解决项。"
      status: unresolved
      verification: flagged
    - statement: "LAYOUT-03 的边缘面未经探针确认(probe 返回 `unclassified — review manually`):「badge 不再遮挡滚动内容」的边界情形是**sticky 表头在滚动过程中覆盖经过其下的正文**——UI-SPEC L-1 已把它显式声明为「已接受的行为」(sticky 的定义,覆盖只在滚动中发生且滚到底后内容全部可达),与 LAYOUT-03 的「浮层永久压住正文」判据不同。本计划按该裁定执行,并把该行记为 flagged assumption。"
      status: unresolved
      verification: flagged
---

<objective>
把文档面板的标题行(含状态徽标与折叠指示符)从「随面板内容滚走」改为「钉在面板顶部」,并把这一条规则端到端接进验证 harness —— 一条 CSS 规则 → 浏览器运行时几何 → `scripts/check-05-ui-uat.py` 的 item 8 → 派发可单跑。

Purpose: LAYOUT-01 / LAYOUT-03 / Pitfall M2 三者在 HEAD 上**已由 quick `260918-qrq` 的流内机制一次性解决**(`#state-badge` 不再是 `position: fixed` 浮层,故结构上不可能遮挡正文,也不再需要与面板宽度做算术耦合)。本计划补的是 HEAD 因此引入的**非自愿丢失**:`#doc-panel { overflow-y: auto }` 且全文件 `position: sticky` 计数为 **0**,于是标题行会随面板内容滚走 —— 连折叠指示符一起,滚动时状态读数彻底消失。这正是 `04-UI-SPEC.md` Q6 反对 `position: absolute` 时给出的理由原话(「`#doc-pane` has `overflow-y: auto`, so the badge would scroll away — a behaviour change to a shipped element」),该理由对 HEAD 同样成立,故采纳它并用 `position: sticky` 补回恒可见。

Output: `frontend/style.css` 围栏外新增的一条 `#doc-panel-header` 规则(零新增令牌);`scripts/check-05-ui-uat.py` 的 item 8(L-1 三条断言 + 三宽度 / clearance / 命中区三项只读诊断)与三处派发接入。

**基线口径(D-01):磁盘 HEAD 是唯一现实基线。** 本计划每一个「现状」值都取自 `frontend/style.css` 的磁盘内容(1265 行)与 `scripts/check-05-ui-uat.py` 的断言(1672 行)。**行号锚点一律以选择器文本为准,不以 `06-CONTEXT.md` 的行号为准** —— 该文件的 `canonical_refs` 行号已漂移(例如 `.panel-header` 在磁盘上是 `:509-518`,CONTEXT 写 `:529-537`;`#chat-messages` 在磁盘上是 `:790-798`,CONTEXT 写 `:791-799`)。`idi-06-PATTERNS.md` 用的是磁盘值,与 `idi-06-UI-SPEC.md` 的引用一致。

**执行前基线(D-20,规划期已实测,执行器须复核):**

| 门 | 规划期在 HEAD 上的实测结果 |
|---|---|
| `scripts/check-01-token-conformance.sh` | `PASS` / exit 0 |
| `scripts/check-02-contrast.py` | `PASS: 0 failures`(47 对)+ `ORDER 0.363` |
| `scripts/check-03-hidden-uniqueness.sh` | `PASS` |
| `scripts/check-04-important-count.sh` | `PASS` |
| `check-05 --item smoke` | PASS(9 条断言,0 FAIL / 0 BLOCKED) |
| `check-05 --item 1` | PASS(45 条断言,0 FAIL / 0 BLOCKED) |
| `check-05 --item 4` | PASS(65 条断言,0 FAIL / 0 BLOCKED) |
| `check-05 --item 7` | PASS(38 条断言,0 FAIL / 0 BLOCKED) |

**本阶段会打破的既有断言(D-20 的登记结论:零项)。** 已逐条普查 `scripts/check-05-ui-uat.py` 与 `scripts/check-06-idi05-validation.py`:两者**没有任何**断言触及 `#ai-events` / `.event-list` / `#annotation-list` / `#latest-check` 的 `max-height` 或 `overflow`,也**没有**断言 `#session-panel` 的 `flex` / `min-height`。唯一涉及 `#session-panel` 的是 item1 的五态显隐矩阵(`p1`/`p12` = visible、`p3`/`checking`/`archive` = hidden),而 D-12 令 `#session-panel` 零改动,该断言存活。本计划新增的 `background` 不触及 `check-04` 断言的 `#doc-panel-header box-shadow == none` 对照组(`check-06` g3 的 `radiusTL` 是 `info()` 观察项而非硬断言,且其探针是 `#session-panel` 族而非 `#doc-panel-header`)。

**为什么三个计划串行而非并行(本阶段的结构约束,不是保守)。** 本阶段的改动面是**单一文件** `frontend/style.css` 加**单一测试文件** `scripts/check-05-ui-uat.py`;`execute-phase` 的同波次规则要求同波次计划的 `files_modified` 零重叠,故三个计划必须落在三个波次。这不是本阶段可以优化的地方 —— 它是「纯 CSS 阶段」的定义。

**波次与依赖形状(本阶段的真实约束,不是保守):**

| 波次 | 计划 | 落点 | 为什么必须在这个位置 |
|---|---|---|---|
| 1 | `idi-06-01`(本计划) | L-1 徽标收口 + item 8 + 三项只读诊断 | 唯一不依赖任何测量结论的交付物;同时**先产出原始数值**,供计划 03 消费 |
| 2 | `idi-06-02` | L-3 换行与 flex 最小尺寸 + L-4 滚动容器收敛 + item 9 | L-2 的窄窗口判据必须在 L-3 / L-4 落地**之后**测 —— D-08 的分析是「横向溢出的真因是 `min-width: auto` 缺失」,在 L-3 之前测会把一个即将被修好的状态判成破版 |
| 3 | `idi-06-03` | L-2 决策 + L-5 / L-6 普查落地 + D-19 连带复验 | 三件都必须看到波次 1/2 的全部改动:三宽度判据、clearance 判据、命中区判据、以及 `idi-04.1-radix` 的指纹面 |

**本计划关闭的需求:** LAYOUT-01、LAYOUT-03。**本计划不触碰:** LAYOUT-02 / LAYOUT-04 / A11Y-07(计划 02 / 03);`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` / `scripts/ui-states/` 零改动;`scripts/check-01…04` 与 `scripts/check-06-idi05-validation.py` 代码零改动;围栏 `:root` 内零改动(零新增令牌);任何 `:focus` / `:hover` / `:active` / `transition` 规则(Phase 7)。
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
@.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md
@frontend/style.css
@frontend/index.html
@scripts/check-05-ui-uat.py
</context>

## Artifacts this phase produces

> 本节的用途:**plan-review-convergence 的 source-grounding pass 读它,把本阶段新建的符号从漂移校验里排除**。
> 本阶段(全部三个计划)新建的符号逐条列出;未列在此的符号即既有符号,其变动必须能追到某条已锁决策。
> 本节列出**全阶段**的产出;每个计划的 SUMMARY 只登记自己那部分。

**新增 CSS 规则(全部为「追加,不重排」,硬规则 3):**

| # | 符号 | 位置 | 计划 | 备注 |
|---|---|---|---|---|
| 1 | `#doc-panel-header` 规则(4 条声明) | `frontend/style.css` 围栏外,紧随 `#doc-panel.collapsed #doc-panel-header` 之后 | 01 | 全文件**首条** `position: sticky` |
| 2 | 六目标 `overflow-wrap` 规则(1 条声明、6 个选择器) | `frontend/style.css` 文件末尾 | 02 | 全文件**首条** `overflow-wrap` |
| 3 | `@media (max-width: 1023px)` 块(**条件交付物**) | `frontend/style.css` 文件末尾 | 03 | 全文件**唯一**的媒体查询;实测无破版则**不存在** |

**原地修改的既有规则(删 / 加声明,规则块不移动):**

| # | 符号 | 位置(HEAD 行号) | 计划 | 动作 |
|---|---|---|---|---|
| 4 | `.event-list` 规则体 | `:564-575` | 02 | 删 `max-height: 55vh;` + `overflow-y: auto;` |
| 5 | `#annotation-list` 规则体 | `:913-920` | 02 | 删 `max-height: 32vh;` + `overflow-y: auto;` |
| 6 | `#main-pane` 规则体 | `:453-460` | 02 | 加 `min-width: 0;` |
| 7 | `#doc-panel` 规则体 | `:468-475` | 02 | 加 `min-width: 0;` |
| 8 | `.annotation-answer summary` 规则体 | `:991-996` | 03 | 加 `min-height: 24px;` + `min-width: 24px;` |
| 9 | 条件:某个裁剪容器的 `padding` | 由 L-5 普查定 | 03 | 仅在实测 clearance < 4px 时改为 `var(--space-1)` |

**`scripts/check-05-ui-uat.py` 新增符号:**

| 符号 | 计划 | 备注 |
|---|---|---|
| `def item8(page, tmp_root)` | 01 | L-1 三条断言 + 三项只读诊断 |
| `def item9(page, tmp_root)` | 02 | L-4 三条断言(滚动者普查 / 可滚到底 / `max-height == none`) |
| item 8 内的三宽度文档级溢出断言(≥1024px) | 03 | 由只读诊断升为硬断言 |
| item 9 内的可交互元素命中区普查断言(≥24×24) | 03 | A11Y-07 的门 |
| item 9 内的焦点环 clearance 普查断言(≥4px) | 03 | L-5 的门 |
| `normalize_items` 默认列表 / `known` 集合 / `main()` 派发三处的 `"8"` 与 `"9"` | 01 加 `"8"`;02 加 `"9"` | PATTERNS.md E-7 的三处协同编辑 |
| 模块 docstring 与 `--item` help 的项清单 | 01 / 02 | 同步到 8 / 9 |
| 运行时 `page.set_viewport_size` 调用(含 1440×900 复位) | 01 | harness 里**第一次** viewport 变更 |

**明确不产生的新符号:** 零新增令牌(围栏 `:root` 内零改动)、零新 CSS 自定义属性、零新文件、零新依赖、零新构建步骤、`frontend/app.js` / `index.html` / `vendor/` 零字节改动。

<tasks>

<task type="tracer">
  <name>Task 1 (tracer): sticky 表头端到端 —— 一条 CSS 规则 → 浏览器几何 → harness item 8 → 派发可单跑</name>
  <files>frontend/style.css, scripts/check-05-ui-uat.py</files>
  <reversibility rating="costly">D-03 / D-05:回退是删三条声明,但本计划把 L-1 的门写进了 `scripts/check-05-ui-uat.py` —— 回退要同时删 item 8 的断言、三处派发接入与 `--item` help 文本,并重算该脚本自身参与的 `idi-04.1-radix` 指纹(该脚本在 04.1 的 `covered_files` 内)。故评级 costly 而非 reversible。</reversibility>
  <read_first>
    - `frontend/style.css` §`#doc-panel` 与折叠态 —— `#doc-panel { flex: 0 0 var(--doc-panel-w); display: flex; flex-direction: column; overflow-y: auto; border-left: 1px solid var(--color-border-subtle); background: var(--color-surface); }`(`:468-475`)、`#doc-panel.collapsed { flex-basis: var(--doc-panel-w-collapsed); overflow: hidden; }`(`:477-480`)、`#doc-panel.collapsed #doc-panel-body, #doc-panel.collapsed #doc-panel-header h1, #doc-panel.collapsed #state-badge { display: none; }`(`:483-485`)、`#doc-panel.collapsed #doc-panel-header { justify-content: center; padding-inline: 0; }`(`:487-490`)—— **新增规则就插在 `:490` 这一块之后**
    - `frontend/style.css` §`#doc-panel-header h1`(`:493-498`)与 §`.panel-header`(`:509-518`)—— **后者体内没有任何 `background` 声明**(只有 `display` / `justify-content` / `align-items` / `height: 36px` / `padding` / `border-radius: var(--radius-md)` / `cursor` / `user-select`),这是新规则**必须**自带背景的原因;`#doc-panel-header` 是 1-0-0,`.panel-header` 是 0-1-0,ID 分量取胜,与源码顺序无关
    - `frontend/style.css` §`#state-badge`(`:671-679`)与它上方 `:668-669` 的 qrq 反驳注释 —— **逐字读,本任务一字不动**(含 `z-index: var(--z-badge)` 在 `:678`)
    - `frontend/style.css` §`#stream-banner`(`:682-696`)—— `position: fixed; top: 12px; left: 50%; transform: translateX(-50%)`;`.fatal` 是**独立选择器**(`:696`),不得合并
    - `frontend/index.html` L82-92 —— DOM 结构:`aside#doc-panel` > `header.panel-header#doc-panel-header`(`<h1>文档区</h1>` + `.panel-header-right` 内的 `span#state-badge.hidden` 与 `span.collapse-indicator`) + `div#doc-panel-body`;`#state-badge` **初始带 `class="hidden"`**,由 `app.js:346-347` 的 `stateBadge.classList.remove('hidden')` 置为可见
    - `frontend/index.html` L101 —— `div#stream-banner.hidden`,同样由 JS 控制显隐
    - `frontend/app.js` L144-152 —— `showStreamBanner(text, fatal)` / `hideStreamBanner()`;二者是**顶层函数声明**(经典脚本,不是 module)⇒ 可从 `page.evaluate` 直接调用,与 item7 直接调 `renderEvent(...)` 同一手法。**这是本任务唯一允许的浏览器侧状态构造方式**
    - `scripts/check-05-ui-uat.py` L86-175 —— 断言记录器全文:`_emit` / `ok`(expected 为 `None` ⇒ `<UNRESOLVED>` BLOCKED;actual 为 `None` ⇒ `<MISSING>` BLOCKED)/ `norm` / `ok_true` / `ok_contains` / `blocked` / `info` / `item_verdict`。**两处 BLOCKED 方向都是承重的,新增项必须用满**
    - `scripts/check-05-ui-uat.py` L256-262(`read_style`)、L346-380(`resolve_color` / `resolve_token`)、L401-435(`make_fixture` / `enter_project` / `reload_project`)、L480-506(`HIDDEN_MATRIX` 与 item1 的写法)
    - `scripts/check-05-ui-uat.py` L1305-1312 —— **全文件唯一的 `getBoundingClientRect()` 用法**(`#btn-send` 可点性诊断);item 8 的几何读数沿用这个 `page.evaluate` 形状:元素不存在时返回 `null`,调用方记 BLOCKED
    - `scripts/check-05-ui-uat.py` L1411-1517 —— item7 的**新项骨架**:`item = "7"` → `print("\n=== UAT 7: … ===")` → `make_fixture("p1", tmp_root)` → `enter_project(page, proj)` → `info(...)` → 断言 → 末尾接静态普查守卫
    - `scripts/check-05-ui-uat.py` L1490-1502 —— item7 的「`all(w != \"700\")` 对 `None` 恒真」陷阱注释。**本任务的三宽度断言与 sticky 断言各有一个同型陷阱**(见 action 第 3 步),该注释是范本
    - `scripts/check-05-ui-uat.py` L1567-1636 —— `parse_args` / `normalize_items` / `main()` 的派发;L1617 `ctx = browser.new_context(viewport={"width": 1440, "height": 900})` 是**唯一**的 viewport 设置点,全文件**没有** `set_viewport_size`
    - `scripts/check-05-ui-uat.py` L18-40 —— 头部注释里的运行方式块(模块 docstring);L1569-1570 的 `--item` help 字符串
    - `scripts/check-06-idi05-validation.py` L200-250 / L470-480 —— g3 的 `radiusTL` 是 `info()` 观察项、g6 的 `#doc-panel-header` 折叠往返。**只读不改**;确认本任务的新规则不会打破它们
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`### L-1 徽标收口:流内 badge + sticky 表头` —— 新规则的**逐字注释文本**、四条承重约束、已接受的行为声明、门的三条断言
    - `.planning/phases/idi-06-layout-robustness/idi-06-PATTERNS.md` §`B-1`(追加规则的位置与注释范本)、§`E-1`…§`E-8`(断言 API / rect 读数 / viewport 变更 / 新项骨架 / 枚举表 / 派发接入 / 环境约束)
  </read_first>
  <action>
    **第 1 步 —— 在 `frontend/style.css` 围栏外新增一条 `#doc-panel-header` 规则。**

    位置:紧接既有规则块 `#doc-panel.collapsed #doc-panel-header { justify-content: center; padding-inline: 0; }`(HEAD `:487-490`)**之后**插入。**不得移动、不得改写任何既有规则块** —— 硬规则 3 在本阶段的风险比 Phase 5 更高(本阶段是结构性 diff)。

    规则体四条声明,逐字:`position: sticky;` / `top: 0;` / `background: var(--color-surface);` / `border-radius: 0;`。选择器是 `#doc-panel-header`(1-0-0)。

    规则上方必须带 UI-SPEC §L-1 给出的**逐字注释**,它承载四条理由,缺一即会被读成任选:(1) 背景是**必需的,不是可选** —— `.panel-header` 规则体内没有任何 `background` 声明,sticky 之后面板正文会从标题行底下穿过去;(2) `--color-surface` 与 `#doc-panel` 自身背景同值且**已被消费**(`style.css:474`)⇒ 零新增令牌;(3) **不加层叠序声明**(该声明的属性名逐字见 UI-SPEC §L-1 的注释原文,本计划不在此复述) —— sticky 元素是 positioned,默认画在静态内容之上;实测若有穿透再补,届时须连带登记 `--z-*` 的序关系断言(badge 10 < banner 20 < overlay 100 < selection-menu 200);(4) `border-radius: 0` —— 半径在本元素上是加背景之后才**首次可见**的新视觉物,而 10px 圆角会让滚动正文从四角露出,全宽条带没有卡片边缘需要圆角。

    注释文本**不得**包含媒体查询 at-rule 关键字(本计划的验收项要求它在 `frontend/style.css` 内计数为 0,故此处不复述该字面量)、`!important`、`#hex`、`var(--x, #fallback)`、`@layer`、`@property` —— 它们会被本计划与后续计划的守卫命令在 `frontend/style.css` 上扫到(硬规则 2 / 4 / 8 与 CHECK-01)。`top: 0` 与 `border-radius: 0` 是无单位零,命中已登记的例外 L-2,不新增例外行。

    **第 2 步 —— `scripts/check-05-ui-uat.py` 新增 `def item8(page, tmp_root)` 的 L-1 三条断言。**

    骨架照抄 item7(`:1411-1517`):`item = "8"` → `print("\n=== UAT 8: … ===", flush=True)` → `proj = make_fixture("p1", tmp_root)` → `enter_project(page, proj)` → `info(...)` → 断言。样本用 `p1`(会话流活动态,`#state-badge` 可见)。

    **(a) badge 是流内元素。** `ok(item, "[p1] #state-badge position == static", "static", read_style(page, "#state-badge", "position"))` 与 `ok(item, "[p1] #state-badge right 无声明", "auto", read_style(page, "#state-badge", "right"))`。`right` 在未声明时的 computed 值是 `auto` —— 若实测不是 `auto`,以实跑输出为准,把期望值改成实测值并在 `info()` 里记录依据(**不得**把断言删掉了事)。元素读不到时 `read_style` 返回 `None` ⇒ `ok()` 自动记 BLOCKED,绝不记 PASS。

    **(b) 三宽度下 badge × banner 不相交(D-06 第 2 条,必须补上 768px)。** 对 `[768, 1024, 1280]` 三个宽度逐一:(i) `page.set_viewport_size({"width": w, "height": 900})`;(ii) 用 `page.evaluate` 调用应用自身的 `showStreamBanner('事件流已断开,正在自动重连……', false)` 让横幅可见 —— **不得**手工 `classList.remove('hidden')` 拼 DOM,那是伪造被测状态;(iii) 在一次 `page.evaluate` 里同时读两个元素的 `getBoundingClientRect()` 与 computed `display`,元素不存在时返回 `null`;(iv) 先证明**前提成立**:badge 与 banner 的 computed `display` 均非 `none`,且两者的 rect 宽高均 **> 0**。任一前提不成立(元素缺失、被隐藏、rect 全零)⇒ `blocked(item, …)` 并给出原因,**绝不**把「两个零矩形不相交」记成 PASS —— 这与 item7 的 `all(w != "700")` 对 `None` 恒真是**同一个陷阱**,只是换了测量对象;(v) 前提成立后再断言矩形不相交(判据:`a.right <= b.left || b.right <= a.left || a.bottom <= b.top || b.bottom <= a.top`),用 `ok_true` 记 PASS/FAIL,并在 `info()` 里打印两个 rect 的原始数值。三个宽度各自一条断言标签(标签里带宽度值,便于诊断)。

    **(c) 滚动 `#doc-panel` 到底后 `#doc-panel-header` 仍可见(sticky 生效)。** 先证明**可滚前提**:`#doc-panel` 的 `scrollHeight > clientHeight`。`p1` 样本下文档面板内容可能不足一屏 ⇒ 先经应用自身的渲染路径把内容加长(用 `renderMarkdown` 渲染一段长 markdown 到 `#draft-content`,与 item4 / item7 的探针同一手法),再复查 `scrollHeight > clientHeight`;仍不可滚 ⇒ `blocked(item, …)`,**绝不**在不可滚的容器上断言「滚到底后仍可见」(那是空转断言)。前提成立后:记下 `#doc-panel-header` 滚动前的 rect;`page.evaluate` 把 `#doc-panel.scrollTop` 设为其 `scrollHeight`;再读 `#doc-panel-header` 的 rect 与 `#doc-panel` 的 rect,断言表头仍落在面板可视区内(`header.bottom > panel.top && header.top < panel.bottom`),并额外断言 `header.top` 与 `panel.top` 的差在 1px 以内(sticky 把表头钉在顶部)。用 `ok_true`,并在 `info()` 里打印 `scrollTop` / `scrollHeight` / `clientHeight` 与两个 rect。

    **(d) viewport 复位(必须)。** 三项做完后把 viewport 设回 `{"width": 1440, "height": 900}`。这是 harness 里**第一次** viewport 变更;不复位会污染其后所有项(item 9 与任何依赖 1440 宽度的既有断言)。在代码里用注释写明这一点,并把复位放在一个 `finally` 或函数末尾的显式语句里,使其在断言失败时也执行。

    **第 3 步 —— item 8 的三项只读诊断(经 `info()` 输出,本计划不升为断言)。**

    这三项的原始数值是**计划 03 的输入**(L-2 的窄窗口决策、L-5 的 clearance 落点、L-6 的命中区落点),故必须在波次 1 就产出。**它们在本计划里一律只读、只打印,不判定** —— 因为它们的判据要等 L-3 / L-4 落地后才成立(L-2)、或由计划 03 承担(L-5 / L-6)。用 `info()` 而非 `ok*()`,使本计划的 `--item 8` 保持全绿而不产生假红。

    - **三宽度文档级溢出:** 对 `[1440, 1024, 768]` 各打印一行,含宽度、`document.documentElement.scrollWidth`、`document.documentElement.clientWidth`。**判据一律取文档级 `scrollWidth`** —— `#doc-panel { overflow-y: auto }` 会把 `overflow-x` 的 used value 一并算成 `auto`,故一张宽 markdown 表会在**面板内部**产生横向滚动条,那是可达内容、不是破版,不计入。诊断前先给 `#doc-panel-body` 注入一段含宽表格与长不可断 token 的 markdown(经 `renderMarkdown`,真实渲染路径),否则三宽度测的是空页面。测完复位 viewport。
    - **L-5 clearance 普查:** 对每个「裁剪容器」(computed `overflow != visible` 的祖先)枚举其可聚焦后代(`button` / `input` / `select` / `textarea` / `a[href]` / `summary` / `[tabindex]`),逐对打印「可聚焦元素 × 最近裁剪祖先 × 实测 clearance(元素 rect 到祖先 padding 边的距离)」。判据阈值是 **4px**(Phase 7 的 `outline: 2px solid` + `outline-offset: 2px` 的环外伸量)。**按元素普查,不按容器名** —— 这正是 Phase 5 `G-idi-05-1` 与本阶段 A11Y-07 的同构教训:按点名枚举会漏掉没被点名的那个。
    - **L-6 命中区普查:** 对每个**可交互元素**(`button` / `input` / `select` / `textarea` / `summary` / `[role=button]` / `[onclick]`)打印选择器或标签、`getBoundingClientRect()` 的宽与高、以及是否 < 24×24。遍历在 `page.evaluate` 里做,返回扁平数组,Python 侧逐条 `info()`。**注意 `.collapse-indicator` 是 `<span>` 且属不得触碰**,不得把它列进「待修」清单(它的可点父级 `.panel-header` 为 36px,达标)。

    **第 4 步 —— 派发接入(PATTERNS.md E-7 的三处协同编辑,缺一即 `--item 8` 不可达)。**

    `normalize_items` 的默认列表由 `["1", "2", "3", "4", "5", "6", "7"]` 改为 `[…, "7", "8"]`;`main()` 的 `known` 集合加 `"8"`;`main()` 的派发链末尾加 `if "8" in items: item8(page, tmp_root)`。同时更新模块 docstring 的运行方式块(加一行 `--item 8` 的说明)与 `parse_args` 的 `--item` help 字符串(项清单加 `8`)。**本计划只加 `8`,不加 `9`** —— item 9 是计划 02 的产出,现在加会在 `main()` 里引用一个不存在的函数。汇总块(`=== 逐项结论 ===`)按 `items` 迭代 `ROWS`,**自动适配,无需改动**。

    **第 5 步 —— 运行时验证(硬规则 7)。** 改完必须实跑并记录原始输出:`check-01` / `check-02` / `check-03` / `check-04`、`--item 8`(新项)、`--item smoke,1,4,7`(既有项无回归)。把三宽度 / clearance / 命中区三项诊断的**原始输出逐行抄进 `idi-06-01-SUMMARY.md`**(这是计划 03 的输入,不是可选的留痕)。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>non-zero exit, or the only stdout line is not exactly `PASS`</fails_when>
    <automated>python3 scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>the last line is not exactly `PASS: 0 failures`, or the command exits non-zero</fails_when>
    <automated>bash scripts/check-03-hidden-uniqueness.sh</automated>
    <fails_when>non-zero exit, or the only stdout line is not exactly `PASS`</fails_when>
    <automated>bash scripts/check-04-important-count.sh</automated>
    <fails_when>non-zero exit, or the only stdout line is not exactly `PASS`</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 8</automated>
    <fails_when>exit code is not 0, or the `=== 逐项结论 ===` block reports anything other than `item 8: PASS`, or any assertion line reports `FAIL` or `BLOCKED`</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,4,7</automated>
    <fails_when>exit code is not 0, or the summary reports anything other than `item smoke: PASS`, `item 1: PASS`, `item 4: PASS`, `item 7: PASS`</fails_when>
    <automated>grep -o 'position: sticky;' frontend/style.css | wc -l</automated>
    <fails_when>the count is not exactly 1</fails_when>
    <automated>grep -c '^#doc-panel-header {' frontend/style.css</automated>
    <fails_when>the count is not exactly 1</fails_when>
    <automated>grep -n -A 5 '^#doc-panel-header {' frontend/style.css | grep -o 'background: var(--color-surface);' | wc -l</automated>
    <fails_when>the count is not exactly 1 (the sticky header must carry its own background — `.panel-header` declares none, so the panel body would show through the header row)</fails_when>
    <automated>grep -n -A 5 '^#doc-panel-header {' frontend/style.css | grep -o 'border-radius: 0;' | wc -l</automated>
    <fails_when>the count is not exactly 1</fails_when>
    <automated>grep -c '^#state-badge {' frontend/style.css; grep -n -A 8 '^#state-badge {' frontend/style.css | grep -o 'z-index: var(--z-badge);' | wc -l; grep -n -A 8 '^#state-badge {' frontend/style.css | grep -oE '(position|right)[[:space:]]*:' | wc -l</automated>
    <fails_when>the first count is not 1, or the second count is not 1, or the third count is not 0 (the badge's in-flow mechanism and its z-index declaration must be untouched; adding a `position` or `right` declaration to it re-opens LAYOUT-03)</fails_when>
    <automated>grep -c '^#doc-panel.collapsed #state-badge { display: none; }' frontend/style.css; grep -c '^#doc-panel.collapsed #doc-panel-header {' frontend/style.css</automated>
    <fails_when>either count is not exactly 1 (the collapsed-state rules are registered as intentional design, not a gap)</fails_when>
    <automated>grep -n -A 9 '^\.panel-header {' frontend/style.css | grep -o 'border-radius: var(--radius-md);' | wc -l</automated>
    <fails_when>the count is not exactly 1 (`.panel-header` itself must be untouched — only the new ID-specific rule changes the header's radius)</fails_when>
    <automated>grep -c '^#stream-banner.fatal {' frontend/style.css</automated>
    <fails_when>the count is not exactly 1 (`.fatal` must remain an independent selector)</fails_when>
    <automated>grep -c 'def item8' scripts/check-05-ui-uat.py; grep -c 'if "8" in items' scripts/check-05-ui-uat.py; grep -o '"8"' scripts/check-05-ui-uat.py | wc -l</automated>
    <fails_when>the first count is not 1, or the second count is not 1, or the third count is less than 3 (normalize_items default list + known set + main() dispatch)</fails_when>
    <automated>grep -c 'def item9' scripts/check-05-ui-uat.py; grep -o '"9"' scripts/check-05-ui-uat.py | wc -l</automated>
    <fails_when>either count is not 0 (item 9 belongs to plan idi-06-02 — wiring it now would reference a function that does not exist)</fails_when>
    <automated>grep -o 'set_viewport_size' scripts/check-05-ui-uat.py | wc -l</automated>
    <fails_when>the count is less than 2 (at least one resize per measured width plus the mandatory restore to 1440x900)</fails_when>
    <automated>git status --porcelain -- frontend/app.js frontend/index.html frontend/vendor/ scripts/check-01-token-conformance.sh scripts/check-02-contrast.py scripts/check-03-hidden-uniqueness.sh scripts/check-04-important-count.sh scripts/check-06-idi05-validation.py scripts/ui-states/</automated>
    <fails_when>the output is not empty</fails_when>
  </verify>
  <acceptance_criteria>
    - `grep -o 'position: sticky;' frontend/style.css | wc -l` == 1(全文件首条 sticky),且 `grep -c '^#doc-panel-header {' frontend/style.css` == 1
    - 新规则的四条声明齐备:`position: sticky;` / `top: 0;` / `background: var(--color-surface);` / `border-radius: 0;` 各恰 1 处,且都在 `#doc-panel-header` 规则体内
    - 新规则的位置:`grep -n '^#doc-panel.collapsed #doc-panel-header {' frontend/style.css` 的行号 **小于** `grep -n '^#doc-panel-header {' frontend/style.css` 的行号(插在既有规则块之后)
    - 围栏 `:root` 内零改动:`git diff -- frontend/style.css` 的 hunk 里没有任何落在 `/* ===== DESIGN TOKENS: START ===== */` 与 `/* ===== DESIGN TOKENS: END ===== */` 之间的行(硬规则 8 / 零新增令牌)
    - `git diff -- frontend/style.css` 只新增了 `#doc-panel-header` 规则块(选择器行 + 注释 + 4 条声明);**没有任何既有规则块被移动或改写**(硬规则 3)
    - `#state-badge` 规则体逐字未变:仍无 `position`、无 `right`,仍含 `z-index: var(--z-badge);`(三条 grep 的计数为 1 / 1 / 0)
    - `#doc-panel.collapsed` 的三条规则与 `#doc-panel.collapsed #doc-panel-header` 逐字未变(两条 `grep -c '^…'` 各 == 1)
    - `.panel-header` 规则体的 `border-radius: var(--radius-md);` 仍在(`grep -n -A 9` 计数 == 1);`#stream-banner.fatal` 仍是独立选择器(计数 == 1)
    - `#doc-panel-header` 规则体内**不含** `z-index`(`grep -n -A 5 '^#doc-panel-header {' frontend/style.css | grep -c 'z-index'` == 0)
    - `frontend/style.css` 内 `@media` 计数仍为 0(`grep -c '@media' frontend/style.css` == 0 —— 窄窗口守卫是计划 03 的条件交付物)
    - `check-05-ui-uat.py` 内新增 `def item8(`;`if "8" in items` 恰 1 处;`"8"` 字面量 ≥3 处(默认列表 / `known` / 派发)
    - `check-05-ui-uat.py` 内 `"9"` 与 `def item9` 计数均为 0(item 9 归计划 02)
    - item 8 含三宽度循环:`768` / `1024` / `1280` 三个字面量各 ≥1 处;含 `showStreamBanner(` 调用;含 `set_viewport_size`
    - item 8 含 viewport 复位到 `1440`(与 768/1024/1280 并列的第四次 `set_viewport_size`,或等价的一次 `new_context` 重建)
    - item 8 的 badge × banner 断言在 rect 全零或元素隐藏时走 `blocked(...)` 而非 `ok_true(...)`(人工逐字核:断言前有 `display != none` 与 rect 宽高 > 0 的前提检查)
    - item 8 的 sticky 断言在 `#doc-panel` 不可滚时走 `blocked(...)` 而非 `ok_true(...)`(人工逐字核:断言前有 `scrollHeight > clientHeight` 的前提检查)
    - item 8 的三项诊断(L-2 三宽度 / L-5 clearance / L-6 命中区)一律经 `info(...)` 输出,**未**升为 `ok*()` 断言
    - `--item 8` 全 PASS(0 FAIL / 0 BLOCKED),且输出里含 3 行文档级 `scrollWidth` / `clientWidth` 数值(1440 / 1024 / 768)、clearance 普查表、命中区普查表
    - `--item smoke` / `--item 1` / `--item 4` / `--item 7` 四项仍全 PASS(0 FAIL / 0 BLOCKED),断言条数不低于执行前基线(9 / 45 / 65 / 38)
    - `idi-06-01-SUMMARY.md` 含三项诊断的**原始输出**(逐行抄录),含三宽度数值行
    - `bash scripts/check-01-token-conformance.sh` / `check-03` / `check-04` 均 `PASS`;`check-02` 仍 `PASS: 0 failures`
  </acceptance_criteria>
  <done>`frontend/style.css` 围栏外新增恰好一条 `#doc-panel-header` 规则(`position: sticky` / `top: 0` / `background: var(--color-surface)` / `border-radius: 0` + 承重注释),插在折叠态规则块之后,围栏内零改动、零新增令牌;`#state-badge` 的流内机制与 `z-index` 声明、折叠态三条规则、`.panel-header`、`#stream-banner.fatal` 全部逐字未变;`scripts/check-05-ui-uat.py` 的 item 8 落地并接入派发,三条 L-1 断言在 768 / 1024 / 1280 三处实检通过(前提不成立时记 BLOCKED),viewport 复位到 1440×900;三项只读诊断的原始数值记入 SUMMARY;四条既有守卫与 `--item smoke,1,4,7` 全部仍绿。</done>
</task>

<task type="auto">
  <name>Task 2: 执行前基线复核 + 三项诊断原始数值的落盘(零代码改动)</name>
  <files>scripts/check-05-ui-uat.py</files>
  <read_first>
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`### L-2 窄窗口守卫(条件交付物 —— 实测驱动)` —— 两条判据的**精确公式**、三宽度取值、「面板内部横向滚动条不计入」的明文、决策规则三条、若写出守卫时被锁死的形态
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`### L-5 焦点环解裁切(普查口径 —— 本阶段不写任何 :focus 规则)` —— 裁剪容器的判据(`overflow != visible`)、4px 阈值的由来、**静态分析的预期结论表**(四个容器的 HEAD padding 与可聚焦后代)、决策规则三条、**禁止「为确定性四个全抬」**
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`### L-6 紧凑控件命中区(A11Y-07)` —— 24×24 判据、机制锁定(`min-height` / `min-width`)、普查表(五类控件的盒高估算与判定)、决策规则、已登记的视觉变更
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`## Deliberate Delta Ledger(本阶段)` —— D6-1…D6-10 的完整清单(本任务的诊断数值是 D6-9 / D6-10 成立与否的唯一证据)
    - `scripts/check-05-ui-uat.py` 本计划 Task 1 新增的 item 8 全文 —— 三项诊断的实现,本任务只**跑**不**改**
    - `frontend/app.js` L1150-1156(`renderAnnotations` 把 AI 答复渲染成 `<details>` + `<summary>`)与 L676-717(`renderVerdictCard`,两个按钮)—— L-5 / L-6 普查依据;**只读不改**
    - `frontend/app.js` L260-285(`appendSayToChat` / 流式气泡)—— `#chat-messages` 无可聚焦后代的证据;**只读不改**
    - `scripts/ui-states/` —— 五个磁盘状态样本(p1 / p12 / p3 / checking / archive),诊断的运行时环境
  </read_first>
  <action>
    **本任务是证据任务,零代码改动。** 它存在的理由是三条硬约束同时成立:(1) 硬规则 7 要求每个 `style.css` 计划带运行时验证;(2) UI-SPEC L-2 明文要求「**必须产出可复核的原始数值**(三个宽度各一行 `scrollWidth / clientWidth`),不能只给结论」;(3) 计划 03 的 L-2 / L-5 / L-6 三个决策必须以**波次 1 的实测数值**为输入,而不是以静态分析或上游文档的论断为输入。

    **第 1 步 —— 复核执行前基线。** 依次实跑并在 SUMMARY 里逐条记录原始输出:`bash scripts/check-01-token-conformance.sh` / `python3 scripts/check-02-contrast.py | tail -1` / `bash scripts/check-03-hidden-uniqueness.sh` / `bash scripts/check-04-important-count.sh` / `.venv/bin/python scripts/check-05-ui-uat.py --item smoke` / `--item 1` / `--item 4` / `--item 7`。这八条的结果必须与本计划 objective 里的「执行前基线」表一致 —— 若某条不一致,说明 Task 1 引入了回归,**先修 Task 1,不得在本任务里绕过**。

    **第 2 步 —— 跑 item 8 并把三项诊断的原始输出逐行抄进 SUMMARY。** 命令:`.venv/bin/python scripts/check-05-ui-uat.py --item 8`。需要落盘的是:

    (a) **三宽度文档级溢出**(L-2 的判据):1440 / 1024 / 768 各一行的 `scrollWidth` 与 `clientWidth`。**明确标注**:这是**波次 1 的基线值**(L-3 / L-4 尚未落地),不是 L-2 的最终判据 —— L-2 的决策在计划 03 用**波次 2 之后**的同一读数做出。基线值的用途是让计划 03 能区分「L-3 / L-4 修好了」与「本来就没破」。若基线上三处都不溢出,照样记录(「本来就没破」也是结论)。

    (b) **L-5 clearance 普查表**(可聚焦元素 × 最近裁剪祖先 × 实测 clearance)。与 UI-SPEC 的**静态分析预期**逐条对照:预期是 `#annotation-list` 的 `<summary>` clearance ≈ 13px、`#chat-messages` **无可聚焦后代**(空动作)、`#latest-check` 无、`#main-pane` ≥10px、`#doc-panel` 由 `#doc-panel-body` 的 32/40px 撑开。**预期必须由实测确认或推翻,不得直接采信** —— 这正是 UI-SPEC S-2 要用户裁定的那一条。逐条写明「实测值 vs 预期值 vs 一致/不一致」。

    (c) **L-6 命中区普查表**(每个可交互元素的宽 × 高 × 是否 < 24×24)。与 UI-SPEC 的普查表逐条对照:预期 `button` ≈ 30–34px ✓、`#selection-menu button` ≈ 30px ✓、`.verdict-buttons button` ≈ 26–30px(待实测)、`.annotation-answer summary` ≈ 14–17px ✗ **确定不达标**、`.collapse-indicator` 属不得触碰(其可点父级 `.panel-header` 为 36px ✓)。**逐条写明实测值**,尤其:`#state-badge` 在 `p1` 下可见、`.annotation-answer summary` 需要先渲染出一个 `<details>` 才存在(用应用自身的 `renderAnnotations`,与 item7 同一手法)。

    **第 3 步 —— 写「测量决策记录」节进 `idi-06-01-SUMMARY.md`。** 这一节是计划 03 的**唯一输入契约**,必须含四块:(1) 上述八条门的基线结果;(2) 三宽度基线数值;(3) L-5 普查表 + 逐条「实测 vs 预期」判定;(4) L-6 普查表 + **明确列出实测 < 24×24 的控件清单**(这是计划 03 施加 `min-height` / `min-width` 的对象)。每一块都要带原始命令与原始输出,**不得只给结论**。

    **不得做的事:** 不得在本任务里改动 `frontend/style.css`(L-3 / L-4 / L-5 / L-6 都是后续计划的落点);不得在本任务里把 item 8 的诊断升为断言(判据尚未成立);不得为了「让数值好看」而在诊断前注入与真实场景不符的内容(注入的长 markdown 必须与 item4 / item7 探针同一量级,且经应用自身的 `renderMarkdown`)。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>any of the three prints anything other than exactly `PASS`, or exits non-zero</fails_when>
    <automated>python3 scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>the last line is not exactly `PASS: 0 failures`</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,4,7,8</automated>
    <fails_when>exit code is not 0, or the summary reports anything other than `item smoke: PASS`, `item 1: PASS`, `item 4: PASS`, `item 7: PASS`, `item 8: PASS`</fails_when>
    <automated>grep -c '测量决策记录' .planning/phases/idi-06-layout-robustness/idi-06-01-SUMMARY.md</automated>
    <fails_when>the count is not exactly 1</fails_when>
    <automated>grep -c 'scrollWidth' .planning/phases/idi-06-layout-robustness/idi-06-01-SUMMARY.md</automated>
    <fails_when>the count is less than 3 (one raw line per measured width: 1440 / 1024 / 768)</fails_when>
    <automated>grep -c 'clearance' .planning/phases/idi-06-layout-robustness/idi-06-01-SUMMARY.md</automated>
    <fails_when>the count is less than 4 (the L-5 census must name every clipping container it inspected, not just conclude)</fails_when>
    <automated>git status --porcelain -- frontend/style.css</automated>
    <fails_when>the output is not empty (this task makes zero CSS changes — L-3/L-4/L-5/L-6 belong to plans 02 and 03)</fails_when>
  </verify>
  <acceptance_criteria>
    - 八条既有门的基线结果逐条记入 SUMMARY,且与本计划 objective 的「执行前基线」表一致(`check-05 --item smoke` 9 条 / `--item 1` 45 条 / `--item 4` 65 条 / `--item 7` 38 条,均 0 FAIL / 0 BLOCKED)
    - SUMMARY 含 `测量决策记录` 节,且该节含四块:门基线 / 三宽度数值 / L-5 普查表 / L-6 普查表
    - 三宽度数值含 `scrollWidth` 与 `clientWidth` 两个量,1440 / 1024 / 768 各一行,并**显式标注这是波次 1 基线**(L-2 的最终判据在计划 03)
    - L-5 普查表逐条给出「可聚焦元素 × 最近裁剪祖先 × 实测 clearance」,并与 UI-SPEC 的静态分析预期逐条对照(一致 / 不一致各自写明);`#chat-messages` 的「无可聚焦后代」结论有实测依据(实测遍历结果为空,不是照抄预期)
    - L-6 普查表逐条给出可交互元素的宽 × 高,并**明确列出实测 < 24×24 的控件清单**;`.collapse-indicator` 未被列入待修清单
    - `git status --porcelain -- frontend/style.css` 为空(本任务零 CSS 改动)
    - `git diff -- scripts/check-05-ui-uat.py` 为空(本任务零 harness 改动 —— 诊断由 Task 1 实现,本任务只跑)
    - `--item smoke,1,4,7,8` 五项全 PASS(0 FAIL / 0 BLOCKED)
  </acceptance_criteria>
  <done>执行前八条门的基线结果、三宽度文档级 `scrollWidth / clientWidth` 基线数值、L-5 clearance 普查表(含逐条「实测 vs 预期」判定)、L-6 命中区普查表(含实测 < 24×24 的控件清单)全部以原始输出形式记入 `idi-06-01-SUMMARY.md` 的「测量决策记录」节;本任务零代码改动,五项 harness 门全绿。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 本阶段无新增信任边界 | 纯 `frontend/style.css` 的声明新增 + `scripts/check-05-ui-uat.py` 的断言新增。零新增网络面、零新增输入面、零新增持久化数据、零新增依赖、零新增文件(`frontend/app.js` / `index.html` / `vendor/` 零 diff) |
| 磁盘 → 浏览器 | `frontend/style.css` 是唯一被消费的样式来源;围栏 `:root` 是令牌的唯一事实源。本计划**零新增令牌**,故不产生第二个事实源 |
| 应用 JS → harness | item 8 用应用自身的 `showStreamBanner(...)` 构造「横幅可见」这一被测状态,而不是手工拼 DOM。越界会测到应用永远不会产生的状态,使断言失去证明力 |
| 人类 → 流程 | 状态徽标是界面**唯一**的状态读数(阶段 1-12 / 自检档)。本计划把它从「随面板滚走」改为「钉在顶部」,该读数在滚动中的可见性因此成为可被破坏的承诺 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-06-01 | Information Disclosure / Repudiation | `#state-badge`(界面唯一状态读数) | high | mitigate | 禁止把 badge 改回 `position: fixed`、加 `position` / `right`、或移出 `#doc-panel-header`(prohibition 1);禁止以隐藏 badge 的方式通过碰撞判据(prohibition 2);`z-index: var(--z-badge)` 声明不得删除(prohibition 3,item4 有活断言);折叠态的 `display: none` 保留并登记为有意设计(D-04) |
| T-idi-06-02 | Tampering | `frontend/style.css` 的四条守卫不变量 | high | mitigate | 每个任务复跑 CHECK-01 / 02 / 03 / 04;围栏标记 1/1;`^\.hidden {` == 1;`!important` **声明**数 == 1;新规则体内不得出现 `!important` / `#hex` / `@layer` / `@property` / `var(--x, #fallback)`(硬规则 2 / 4) |
| T-idi-06-03 | Tampering | 既有门被新断言污染 | medium | mitigate | item 8 的 viewport 变更必须复位到 1440×900(否则污染其后所有项);`--item smoke,1,4,7` 四项作为回归门复跑;断言条数不得低于执行前基线 |
| T-idi-06-04 | Denial of Service | 假 PASS(空转断言) | high | mitigate | badge × banner 断言与 sticky 断言各有**前提检查**(badge / banner 可见且 rect 非全零;`#doc-panel` 真的可滚),前提不成立记 `blocked(...)` 而非 `ok_true(...)`。这与 item7 已登记的 `all(w != "700")` 对 `None` 恒真是同型陷阱 |
| T-idi-06-05 | Information Disclosure | 本计划的改动内容 | low | accept | 改动只有四条布局声明,无用户数据、无网络请求、无外部资源;`frontend/vendor/` 仍只含 `marked.min.js` |
| T-idi-06-SC | Tampering | npm / pip / cargo 安装 | high | mitigate | 本阶段零安装(硬规则 6):不新增任何依赖、文件或构建步骤;`git status --porcelain -- frontend/vendor/` 为空。无 `[ASSUMED]` / `[SUS]` 包,故无需 package-legitimacy 人工签核门 |

**ASVS L1 口径:** 本阶段零新增输入面、零新增网络调用、零新增持久化,故 ASVS 的注入 / 认证 / 会话类威胁不适用。上表 `high` 两项(T-idi-06-01 / T-idi-06-04)是本阶段真实的失败模式:前者是产品承诺(状态读数不可静默丢失),后者是证据完整性(断言不可空转)。二者都由 `blocked(...)` 前提检查与 prohibition 1–3 收口。
</threat_model>

<verification>
- `bash scripts/check-01-token-conformance.sh` → `PASS` / exit 0
- `python3 scripts/check-02-contrast.py | tail -1` → `PASS: 0 failures`
- `bash scripts/check-03-hidden-uniqueness.sh` → `PASS`(`^\.hidden {` == 1)
- `bash scripts/check-04-important-count.sh` → `PASS`(`!important;` 声明数 == 1)
- `.venv/bin/python scripts/check-05-ui-uat.py --item 8` → `item 8: PASS`(0 FAIL / 0 BLOCKED)
- `.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,4,7` → 四项全 PASS,断言条数 ≥ 执行前基线(9 / 45 / 65 / 38)
- Gate A(围栏纯度):`git diff -- frontend/style.css` 的 hunk 中没有任何行落在围栏 START/END 之间(零新增令牌)
- Gate B(既有规则未动):`git diff -- frontend/style.css` 只新增 `#doc-panel-header` 规则块;`#state-badge` / `.panel-header` / `#doc-panel.collapsed` 族 / `#stream-banner` 四条规则族零改动
- Gate C(零外溢):`git status --porcelain -- frontend/app.js frontend/index.html frontend/vendor/ scripts/ui-states/ scripts/check-01-token-conformance.sh scripts/check-02-contrast.py scripts/check-03-hidden-uniqueness.sh scripts/check-04-important-count.sh scripts/check-06-idi05-validation.py` 输出为空
- Gate D(原始数值落盘):`idi-06-01-SUMMARY.md` 的「测量决策记录」节含三宽度 `scrollWidth` 数值行、L-5 clearance 普查表、L-6 命中区普查表与 < 24×24 清单
</verification>

<success_criteria>
- 文档面板标题行在滚动时钉在面板顶部:状态徽标与折叠指示符恒可见(非自愿丢失被修掉),且 badge 仍是流内元素、不回到浮层
- 新规则只带四条声明,围栏内零改动、零新增令牌、零新增文件、零新增依赖
- L-1 的三条门在 768 / 1024 / 1280 三处实检通过,且两条几何断言在前提不成立时记 BLOCKED 而非假 PASS
- 三项诊断(三宽度文档级溢出 / L-5 clearance / L-6 命中区)的原始数值落盘,成为计划 03 三个决策的唯一输入
- 四条既有守卫与 `--item smoke,1,4,7` 全绿,断言条数不低于执行前基线
- `frontend/app.js` / `frontend/index.html` / `frontend/vendor/` / `scripts/ui-states/` 零 diff
</success_criteria>

<output>
Create `.planning/phases/idi-06-layout-robustness/idi-06-01-SUMMARY.md` when done
</output>
---
phase: idi-06-layout-robustness
plan: 02
type: execute
wave: 2
depends_on:
  - idi-06-01
files_modified:
  - frontend/style.css
  - scripts/check-05-ui-uat.py
autonomous: true
requirements:
  - LAYOUT-02
  - LAYOUT-04

estimate:
  tokens: 62000
  raw_tokens: 62000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- lifted from idi-06-UI-SPEC.md `## UI Considerations` — explicit tier (15 of 24; E4/E5/E6/E7/E9/E10) ----
    - "E4 `#ai-events` / `.event-list` `overflow`:删掉 `.event-list` 的 `max-height: 55vh` 与 `overflow-y: auto` 后不再内部滚动,条目随外层容器滚动,滚到面板区底部时内容可达(L-4:面板区只剩两个滚动者)。门:`check-05 --item 9` ← UI-SPEC UI-Considerations E4 `overflow`(explicit)"
    - "E4 `#ai-events` / `.event-list` `zero-one-many`:0 / 1 / 多条目下高度随内容自然增长,无固定高度截断、无空白占位塌陷(本阶段删除了固定高度)← UI-SPEC UI-Considerations E4 `zero-one-many`(explicit)"
    - "E4 `#ai-events` / `.event-list` `long-text`:`.event-content` 在 L-3 的六目标 `overflow-wrap: anywhere` 之列,不可断长串换行而不撑破视口 ← UI-SPEC UI-Considerations E4 `long-text`(explicit)"
    - "E5 `#annotation-list` `overflow`:删掉 `#annotation-list` 的 `max-height: 32vh` 与 `overflow-y: auto` 后不再内部滚动,条目随外层容器滚动,滚到面板区底部时内容可达(L-4)。门:`check-05 --item 9` ← UI-SPEC UI-Considerations E5 `overflow`(explicit)"
    - "E5 `#annotation-list` `zero-one-many`:0 / 1 / 多条目下高度随内容自然增长;展开某条 `<details>` 后不把后续条目挤出不可达区域(不再内部滚动即达成)← UI-SPEC UI-Considerations E5 `zero-one-many`(explicit)"
    - "E5 `#annotation-list` `long-text`:`.annotation-note` 与 `.annotation-answer-body` 在 L-3 的六目标 `overflow-wrap: anywhere` 之列,引用摘录与批注正文的长串换行不撑破视口 ← UI-SPEC UI-Considerations E5 `long-text`(explicit)"
    - "E6 `#chat-messages` `overflow`:`#chat-messages` **保留**为面板区内唯一合理的第二滚动者(输入行必须钉底),本阶段不动其 `overflow`;门:`check-05 --item 9` 断言面板区滚动者集合恰为 `#main-pane` / `#chat-messages` / `#latest-check` 三者 ← UI-SPEC UI-Considerations E6 `overflow`(explicit)"
    - "E6 `#chat-messages` `zero-one-many`:0 / 1 / 多条消息下 `#chat-messages` 的滚动行为一致;流式追加时新内容进入既有滚动区,不改变输入行的钉底位置 ← UI-SPEC UI-Considerations E6 `zero-one-many`(explicit)"
    - "E6 `#chat-messages` `long-text`:`.chat-bubble` 与 `.say-chunk` 在 L-3 的六目标 `overflow-wrap: anywhere` 之列,长 markdown 与不可断长串换行不撑破视口 ← UI-SPEC UI-Considerations E6 `long-text`(explicit)"
    - "E7 `#latest-check` `overflow`:`#latest-check` **保留** 30vh 内部滚动(自检报告是本阶段唯一除 `#chat-messages` 外被显式允许保留的内部滚动者);L-4 只收敛 `.event-list` 与 `#annotation-list` ← UI-SPEC UI-Considerations E7 `overflow`(explicit)"
    - "E7 `#latest-check` `long-text`:报告 markdown 的不可断长串(路径、长 token)在 30vh 滚动区内换行,不产生横向滚动条 ← UI-SPEC UI-Considerations E7 `long-text`(explicit)"
    - "E9 `#doc-panel-body` `overflow`:`#doc-panel { min-width: 0 }` 生效,flex 项默认 `min-width: auto` 不再让面板被不可断长内容撑破视口;门:1440 → 1024 → 768 无横向溢出 ← UI-SPEC UI-Considerations E9 `overflow`(explicit)"
    - "E9 `#doc-panel-body` `long-text`:`.markdown-body` 在 L-3 的六目标 `overflow-wrap: anywhere` 之列,草稿 / 轮次文档 / 归档视图三态共用同一换行契约,长串换行不产生横向滚动 ← UI-SPEC UI-Considerations E9 `long-text`(explicit)"
    - "E10 `#main-pane` `overflow`:`#main-pane { min-width: 0 }` 生效,四个居中 section 的列不再被长内容撑破;门:1440 → 1024 → 768 三档无横向溢出(L-2 的判据:文档级 `scrollWidth`,面板内部横向滚动条不计)← UI-SPEC UI-Considerations E10 `overflow`(explicit)"
    - "E10 `#main-pane` `long-text`:主区内不可断长内容(代码块、长路径)换行或在其自身容器内滚动,不把 `#main-pane` 的 `scrollWidth` 推过视口宽 ← UI-SPEC UI-Considerations E10 `long-text`(explicit)"
    # ---- lifted from idi-06-UI-SPEC.md `## UI Considerations` — backstop tier (15 of 19; E4/E5/E6) ----
    - statement: "E4 `#ai-events` / `.event-list` `empty`:无数据(零条目 / 未填表单 / 缺媒体)时显示什么?本阶段对该状态维度零改动 —— `.event-list` 的 `display` / `flex-direction` / `gap` / `border` / `border-radius` / `padding` / `background` 与 `.streaming` / `.aborted` 两条全部逐字保留,只删限高与内滚动。"
      verification: backstop
    - statement: "E4 `#ai-events` / `.event-list` `loading`:数据仍在加载时显示什么?本阶段零改动;`.event-list.streaming` 的 `--color-surface-streaming` 背景逐字保留(INTERACT-02 归 Phase 7)。"
      verification: backstop
    - statement: "E4 `#ai-events` / `.event-list` `error`:加载或提交失败时显示什么?本阶段零改动;`.event-list.aborted` 的 `--color-surface-danger` 背景逐字保留 —— 它是已交付的 SSE 修复(REG-03 的复验对象)。"
      verification: backstop
    - statement: "E4 `#ai-events` / `.event-list` `populated`:正常填充态在典型内容量下是什么样?本阶段的行为变更正是这一维度 —— 条目不再被 55vh 截断,高度随内容自然增长,由 `#main-pane` 承担滚动。门:`check-05 --item 9` 的滚动者普查 + 末条可达性断言。"
      verification: backstop
    - statement: "E4 `#ai-events` / `.event-list` `partial`:部分数据(部分字段或行存在、其余缺失)时显示什么?本阶段零改动 —— 条目渲染路径在 `app.js`(`renderEvent`),本阶段不触碰。"
      verification: backstop
    - statement: "E5 `#annotation-list` `empty`:无数据时显示什么?本阶段零改动 —— 空态文案由 `app.js` 注入,`#annotation-list` 自身的 `display` / `flex-direction` / `gap` / `padding` 逐字保留。"
      verification: backstop
    - statement: "E5 `#annotation-list` `loading`:数据仍在加载时显示什么?本阶段零改动。"
      verification: backstop
    - statement: "E5 `#annotation-list` `error`:加载或提交失败时显示什么?本阶段零改动 —— 内联错误锚点是 `#probe-controls`,不在 `#annotation-list` 内(REG-02 已交付的结构性修复)。"
      verification: backstop
    - statement: "E5 `#annotation-list` `populated`:正常填充态在典型内容量下是什么样?本阶段的行为变更正是这一维度 —— 条目不再被 32vh 截断,由 `#main-pane` 承担滚动。门:`check-05 --item 9`。"
      verification: backstop
    - statement: "E5 `#annotation-list` `partial`:部分数据时显示什么?本阶段零改动 —— 批注条目渲染路径在 `app.js`(`renderAnnotations`),本阶段不触碰。"
      verification: backstop
    - statement: "E6 `#chat-messages` `empty`:无消息时显示什么?本阶段零改动 —— 居中问候语由 `#session-panel .panel-body:has(#chat-messages:empty)` 族承载,该族四条规则逐字保留(D-12 的零改动对象)。"
      verification: backstop
    - statement: "E6 `#chat-messages` `loading`:数据仍在加载时显示什么?本阶段零改动。"
      verification: backstop
    - statement: "E6 `#chat-messages` `error`:加载或提交失败时显示什么?本阶段零改动;断流态由 `#stream-banner` 承载。"
      verification: backstop
    - statement: "E6 `#chat-messages` `populated`:正常填充态在典型内容量下是什么样?本阶段零改动 —— `#chat-messages` 的 `flex: 1` / `min-height: 160px` / `overflow-y: auto` 三条声明逐字保留,输入行仍钉底。门:`check-05 --item 9` 的滚动者普查(它必须在集合内)。"
      verification: backstop
    - statement: "E6 `#chat-messages` `partial`:部分数据时显示什么?本阶段零改动 —— 流式追加路径在 `app.js`(`appendSayToChat`),本阶段不触碰。"
      verification: backstop
    # ---- phase-specific truths ----
    - "`frontend/style.css` 文件末尾新增恰好一条六选择器规则:`.markdown-body, .event-content, .chat-bubble, .say-chunk, .annotation-note, .annotation-answer-body { overflow-wrap: anywhere; }`,并带 UI-SPEC §L-3 的逐字注释(含「不写通配规则」与「必须用 anywhere 而非 break-word」两条理由)← L-3 / D-07"
    - "`overflow-wrap` 的声明数恰为 1;`.event-content` 的既有 `word-break: break-all` 与 `white-space: pre-wrap` 逐字保留、未被通配规则波及 ← L-3 / D-07"
    - "`#main-pane` 与 `#doc-panel` 两条**既有**规则体内各原地新增一行 `min-width: 0;`,各带一段注释写明「`anywhere` 落地后 min-content 会塌缩,本行看似冗余 —— 它不依赖六个目标长期全覆盖,将来新增一个未被 `overflow-wrap` 覆盖的渲染容器时仍能兜住,不得当作冗余代码删除」← L-3 / D-09"
    - "`min-width: 0;` 声明数恰为 2(两条都在既有规则体内原地新增,未新增规则块);两条规则的既有声明逐字未动 ← L-3 / 硬规则 3"
    - "`.event-list` 规则体内原地删掉 `max-height: 55vh;` 与 `overflow-y: auto;` 两行;其余八条声明(`display` / `flex-direction` / `gap` / `border` / `border-radius` / `padding` / `background` / `transition: background-color 0.3s`)与 `.streaming` / `.aborted` 两条**逐字不变**;规则块未移动 ← L-4 / D-11 / 硬规则 3"
    - "`#annotation-list` 规则体内原地删掉 `max-height: 32vh;` 与 `overflow-y: auto;` 两行;其余四条声明(`display` / `flex-direction` / `gap` / `padding: var(--space-half)`)逐字不变;规则块未移动 ← L-4 / D-11 / 硬规则 3"
    - "`#latest-check` 的 `max-height: 30vh;` 与 `overflow-y: auto;` **保留** —— 去掉它会把裁决按钮(`#verdict-cards` 的「修」/「接受现状」)推到视口之外,那是把交互面推到折叠线以下 ← L-4 保留理由 / D-11"
    - "`#chat-messages` 的 `overflow-y: auto;` 与 `#session-panel` 族的每一条声明**保留** —— 输入行必须钉底;执行路线图的「改 `flex: 0 0 auto`」会让 `#chat-messages` 随消息无限增高、输入行落到视口之外 ← D-12 / 硬规则 5"
    - "本阶段结束后面板区(`#main-pane` 及其后代)内计算 `overflow-y` 为 `auto` / `scroll` 的元素集合恰为 `{#main-pane, #chat-messages, #latest-check}` 三者;排除 SC#3 明文豁免的 `#chat-messages` 之后恰为 `{#main-pane, #latest-check}` 两者 ← D-14 第 1 条 / L-4 / SC#3 的偏离登记(A-5)"
    - "Success Criterion #3 的措辞偏离已登记:路线图写「侧栏内只剩一个滚动条(`#chat-messages` 除外)」,本阶段的实际目标状态是**面板区内 `#main-pane` + `#latest-check` 两个滚动者**(外加豁免的 `#chat-messages`)。**不改 `ROADMAP.md` / `REQUIREMENTS.md` 正文**(改会作废指纹),只在计划与验证记录里登记 ← UI-SPEC §契约修正登记 A-5"
    - "`scripts/check-05-ui-uat.py` 新增 item 9 并接入派发三处,`--item 9` 可单跑;item 9 的滚动者普查按 **DOM 遍历**算出,不硬编码选择器列表 ← D-14 / PATTERNS.md E-5"
    - "item 9 的断言齐备:(a) 面板区滚动者集合 == `{#main-pane, #chat-messages, #latest-check}` 且排除 `#chat-messages` 后 == `{#main-pane, #latest-check}`;(b) `#main-pane` 与 `#latest-check` 两者滚到底后末条内容可达;(c) `#ai-events` / `#annotation-list` 的计算 `max-height` 为 `none`;(d) 两条保留项护栏(`#latest-check` 的 `max-height` 仍为 `30vh`、`#chat-messages` 的 `overflow-y` 仍为 `auto`)← D-14 / D-11"
    - "item 9 的滚动者普查是**状态无关**的 —— 七个 `overflow` 声明所在的元素全部是 `index.html` 的静态元素,与磁盘状态样本无关,故普查在任何样本下都成立 ← 静态 DOM 事实"
    - "item 9 的可达性断言在注入足量内容后做出(经应用自身的 `renderEvent` / `renderMarkdown` 渲染,不手工拼 DOM);在「容器无需滚动」时用 `info()` 报告而非记一条空转 PASS;末条元素读不到时记 BLOCKED ← PATTERNS.md E-2 的「绝不记假 PASS」纪律"
    - "`bash scripts/check-01-token-conformance.sh` 打印 `PASS` 且 exit 0(围栏外裸 `#hex` 仍为 0)← CHECK-01"
    - "`python3 scripts/check-02-contrast.py` 仍打印 `PASS: 0 failures`,清单规模与 `ORDER` 行逐字不变(本计划零颜色改动)← CHECK-02"
    - "`bash scripts/check-03-hidden-uniqueness.sh` 打印 `PASS`(`^\\.hidden {` 计数 == 1)← CHECK-03 / 硬规则 1"
    - "`bash scripts/check-04-important-count.sh` 打印 `PASS`(`!important` **声明**数 == 1)← CHECK-04 / 硬规则 2"
    - "既有门无回归:`--item smoke` / `--item 1` / `--item 4` / `--item 7` / `--item 8` 五项在改动后仍全 PASS(0 FAIL / 0 BLOCKED)← 硬规则 7 / D-20"
    - "运行时:item 9 在真实浏览器里读到面板区滚动者集合恰为三者、排除豁免后恰为两者;`#main-pane` 与 `#latest-check` 滚到底后末条内容落在各自可视区内;`#ai-events` / `#annotation-list` 的计算 `max-height` 为 `none` ← 硬规则 7 / D-14"

  artifacts:
    - path: "frontend/style.css"
      provides: "文件末尾追加的六选择器 `overflow-wrap: anywhere` 规则 + `#main-pane` / `#doc-panel` 两条既有规则体内各新增一行 `min-width: 0;` + `.event-list` / `#annotation-list` 两条既有规则体内各删两行限高与内滚动声明"
      contains: "overflow-wrap: anywhere;"
    - path: "scripts/check-05-ui-uat.py"
      provides: "新增 `def item9(page, tmp_root)`(滚动者 DOM 普查两条 + 末条可达性 + `max-height == none` 两条 + 保留项护栏两条);`normalize_items` 默认列表、`known` 集合、`main()` 派发三处接入 `\"9\"`;模块 docstring 与 `--item` help 同步"
      contains: "def item9"

  key_links:
    - from: "六目标 `overflow-wrap: anywhere` 规则"
      to: "`#main-pane` / `#doc-panel` 的 `min-width: 0`"
      via: "按 CSS Text 3 只有 `anywhere` 参与 min-content 内在尺寸计算 ⇒ 六处落地后子树 min-content 塌缩,`min-width: auto` 自然失效;`min-width: 0` 是对「将来新增未被覆盖的渲染容器」的兜底,不是冗余"
      pattern: "overflow-wrap: anywhere;"
    - from: "`.event-list` / `#annotation-list` 删除的两条声明"
      to: "`#main-pane` 的 `overflow-y: auto`"
      via: "内层滚动者移除后,原本被 55vh / 32vh 截断的内容改由外层唯一滚动者承载 ⇒ 滚到面板区底部时内容可达"
      pattern: "^#main-pane \\{"
    - from: "item 9 的滚动者 DOM 普查"
      to: "面板区实际的计算 `overflow-y` 分布"
      via: "在 `page.evaluate` 里遍历 `#main-pane` 及其后代、读 computed `overflow-y`,与期望集合两个独立量相比(不是自比)"
      pattern: "overflow-y"
    - from: "`#latest-check` 保留的 `max-height: 30vh`"
      to: "`#check-controls` 里的裁决按钮可达性"
      via: "长自检报告被限高在 30vh 内滚动,故其下方的裁决按钮不被推出视口"
      pattern: "max-height: 30vh;"

  prohibitions:
    - statement: "不得重排 `frontend/style.css` 的任何规则或声明(硬规则 3「追加,不重排」)。删除 `max-height` / `overflow-y` 必须**原地改声明**,新增规则必须**追加在文件末尾**。至少一对等特异性规则由源码顺序决定(`#draft-view > h2` 与 `#brainstorm-view > h2`,同为 1-0-1);本阶段是结构性 diff,重排风险比 Phase 5 更高,而源码 diff 看起来完全无辜"
      status: active
      verification: flagged
    - statement: "不得用「隐藏溢出」的手段通过任何不破版判据:不得新增 `overflow: hidden`、不得裁切、不得让内容变得不可达。判据是「无横向溢出、无内容被遮挡」,**不是**「溢出看不见」。同理不得删除任何服务于可达性的滚动者(`#latest-check` 的 30vh 内滚动一旦删除,长自检报告会把裁决按钮推到折叠线以下)"
      status: active
      verification: flagged
    - statement: "不得删除 `#chat-messages` 的 `overflow-y: auto` / `flex: 1` / `min-height: 160px`,也不得触碰 `#session-panel` 族的任何声明(含 `flex: 1 1 auto` / `min-height: 200px` 与两条 `:has(:empty)` 空态规则)。执行路线图的「改 `flex: 0 0 auto`」会让输入行落到视口之外,与路线图自己的「输入行必须钉底」互相矛盾;`min-height: 200px` 不是死代码 —— 空态下它是居中问候语唯一的空间来源(D-12)"
      status: active
      verification: flagged
    - statement: "不得写通配 `overflow-wrap` 规则(如 `* { … }` 或对 `body` 的等价写法):那会波及已裁定的 `.event-content { word-break: break-all }`(`style.css:598-601`),并把「哪些容器受影响」重新变成不可枚举 —— 那正是 `G-idi-05-1` 的成因。同理不得把 `min-width: 0` 当冗余代码删掉(D-09 的双保险是刻意的)"
      status: active
      verification: flagged
    - statement: "不得引入任何媒体查询、断点阶梯、响应式系统或堆叠布局(`#app { flex-direction: column }`)。Q5 明文 Out of scope:它们改变 DESIGN.md §4.1 两栏契约的**含义**,是新设计决策而非 CSS 重构。窄窗口守卫是计划 03 的条件交付物,且最多一条"
      status: active
      verification: flagged
    - statement: "不得改动任何用户可见文案,不得触碰 `frontend/app.js` / `frontend/index.html` / `frontend/vendor/`。harness 注入内容一律经应用自身的渲染函数(`renderEvent` / `renderMarkdown`),不得手工拼 DOM 伪造被测状态"
      status: active
      verification: flagged

  assumptions:
    # ---- edge probe fallback ($COVERAGE): LAYOUT-02 / LAYOUT-04 rows, ALL unresolved ----
    # The edge probe is an English-cue classifier and misclassified the Chinese requirement prose;
    # `unclassified` stays `unresolved` (never auto-resolved with backstop, never dismissed).
    - statement: "LAYOUT-02 的边缘面未经探针确认(probe 返回 `unclassified — review manually`):「窄窗口不破版」在 768–1023px 之间的边界情形(视口恰好 768 / 恰好 1024)未经探针枚举。本计划只落 L-3 的换行与最小尺寸(该条的**判据**要等计划 03 在波次 2 之后的树上重测),并把该行记为 flagged assumption 而非已解决项。"
      status: unresolved
      verification: flagged
    - statement: "LAYOUT-04 的边缘面未经探针确认(probe 返回 `unclassified — review manually`):「滚动容器套娃收敛」的边界情形是**面板区滚动者数目的口径本身** —— 路线图 SC#3 写「只剩一个滚动条(`#chat-messages` 除外)」,而 `#main-pane` 自身也是滚动者,故本阶段的真实目标状态是「恰好两个 + 一个明文豁免」。本计划按 D-11 / D-14 / A-5 的口径执行并把该偏离显式登记,把该行记为 flagged assumption。"
      status: unresolved
      verification: flagged
---

<objective>
把不可断长内容导致的横向撑破从根上堵死(六目标 `overflow-wrap: anywhere` + `#app` 两个 flex 子项的 `min-width: 0`),并把面板区的滚动容器套娃从「3 个嵌套 + 1 个外层」收敛为「1 个外层 + 1 个被保留的内层」,同时把收敛结果写成可机械复核的门(item 9)。

Purpose: LAYOUT-02 与 LAYOUT-04 在 HEAD 上有同一个技术根因。`#app { display: flex }` 的两个子项 `#main-pane { flex: 1 1 auto }` 与 `#doc-panel { flex: 0 0 var(--doc-panel-w) }` 都是 `min-width: auto` —— **`flex-basis` 不是硬约束,`min-width: auto` 胜出**,所以长不可断内容能把 `#doc-panel` 顶得比它的 `clamp(340px, 30vw, 480px)` 还宽,不只是撑破主区。而按 CSS Text 3,只有 `overflow-wrap: anywhere` 参与 min-content 内在尺寸计算(`break-word` 不参与)—— 这是两条声明能成立的技术前提,注释里必须写明,否则会被读成任选其一。LAYOUT-04 是同一件事的容器侧:`.event-list`(55vh)与 `#annotation-list`(32vh)是套娃的前两层,删掉它们的内容改由 `#main-pane` 这一个外层滚动者承载。

Output: `frontend/style.css` 末尾新增的一条六选择器 `overflow-wrap` 规则;`#main-pane` / `#doc-panel` 两条既有规则体内各新增一行 `min-width: 0;`;`.event-list` / `#annotation-list` 两条既有规则体内各删两行;`scripts/check-05-ui-uat.py` 的 item 9(滚动者 DOM 普查 / 末条可达性 / `max-height == none` / 保留项护栏)与派发接入。

**基线口径(D-01):磁盘 HEAD 是唯一现实基线。** 本计划每一个「现状」值都取自 `frontend/style.css` 的磁盘内容(1265 行)。**行号锚点一律以选择器文本为准,不以 `06-CONTEXT.md` 的行号为准** —— 该文件的 `canonical_refs` 行号已漂移。`idi-06-PATTERNS.md` 用的是磁盘值。

**本阶段「打破既有断言」的登记结论(D-20):零项。** 已逐条普查 `scripts/check-05-ui-uat.py` 与 `scripts/check-06-idi05-validation.py`:**没有任何**既有断言触及 `#ai-events` / `.event-list` / `#annotation-list` / `#latest-check` 的 `max-height` 或 `overflow`,也**没有**断言 `#session-panel` 的 `flex` / `min-height`。本计划删除的四条声明因此**不打破任何既有门**。唯一需要登记的是**语义层**的措辞偏离:Success Criterion #3 写「侧栏内只剩一个滚动条(`#chat-messages` 除外)」,本阶段的实际目标状态是「面板区内 `#main-pane` + `#latest-check` 两个滚动者」(外加 SC#3 明文豁免的 `#chat-messages`)。**不改 `ROADMAP.md` / `REQUIREMENTS.md` 正文**(改会作废已通过的验证指纹),只在计划与验证记录里登记(UI-SPEC §契约修正登记 A-5)。

**`#main-pane` 自身也是滚动者,这是 SC#3 口径必须收窄的原因。** HEAD 的 `overflow` 声明共七处:`#main-pane`(:458)、`#doc-panel`(:472)、`#doc-panel.collapsed`(:479,`overflow: hidden`)、`.event-list`(:569)、`#chat-messages`(:793)、`#annotation-list`(:918)、`#latest-check`(:1116)。删除 L-4 的两处之后,面板区(`#main-pane` 及其后代)内计算 `overflow-y` 为 `auto` 的元素是 `#main-pane` / `#chat-messages` / `#latest-check` 三者 —— 不是路线图写的「一个」。D-14 的「恰好两个」是**排除 SC#3 明文豁免的 `#chat-messages`** 之后的口径。item 9 把两种读法都断言,故「意外新增第四个滚动者」这类回归仍会被抓到。

**本计划关闭的需求:** LAYOUT-02(其判据的最终测量在计划 03)、LAYOUT-04。**本计划不触碰:** LAYOUT-01 / LAYOUT-03(计划 01 已关闭);A11Y-07 与窄窗口守卫(计划 03);`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` / `scripts/ui-states/` 零改动;`scripts/check-01…04` 与 `scripts/check-06-idi05-validation.py` 代码零改动;围栏 `:root` 内零改动(零新增令牌);任何 `:focus` / `:hover` / `:active` / `transition` 规则(Phase 7)。
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
@frontend/style.css
@frontend/index.html
@scripts/check-05-ui-uat.py
</context>

## Artifacts this phase produces

> 本节的用途:**plan-review-convergence 的 source-grounding pass 读它,把本阶段新建的符号从漂移校验里排除**。
> 未列在此的符号即既有符号,其变动必须能追到某条已锁决策。

**本计划新建的符号:**

| 类别 | 符号 | 位置 | 备注 |
|---|---|---|---|
| 新增 CSS 规则 | 六选择器 `overflow-wrap: anywhere` 规则(1 条声明、6 个选择器) | `frontend/style.css` 文件末尾 | 全文件**首条** `overflow-wrap` |
| 新增 CSS 声明 | `min-width: 0;` × 2 | `#main-pane` / `#doc-panel` 两条既有规则体内 | 全文件**首条** `min-width` |
| 删除 CSS 声明 | `max-height: 55vh;` / `overflow-y: auto;` | `.event-list` 规则体内 | 原地删,规则块不移动 |
| 删除 CSS 声明 | `max-height: 32vh;` / `overflow-y: auto;` | `#annotation-list` 规则体内 | 原地删,规则块不移动 |
| 新增 Python 函数 | `def item9(page, tmp_root)` | `scripts/check-05-ui-uat.py` | 滚动者 DOM 普查 / 末条可达性 / `max-height == none` / 保留项护栏 |
| 新增派发字面量 | `"9"`(默认列表 / `known` / 派发三处) | 同上 | PATTERNS.md E-7 |
| 新增断言标签 | 滚动者集合断言 ×2(全集 == 三者;排除 `#chat-messages` 后 == 两者) | item 9 | 两个独立量的比较,不是自比 |
| 新增断言标签 | `#main-pane` / `#latest-check` 末条可达性 | item 9 | 需先注入足量内容 |
| 新增断言标签 | `#ai-events` / `#annotation-list` 计算 `max-height == none` | item 9 | 状态无关(元素常驻静态 DOM) |
| 新增断言标签 | 保留项护栏 ×2(`#latest-check` 的 `max-height == 30vh`;`#chat-messages` 的 `overflow-y == auto`) | item 9 | D-11 保留理由的机器化形态 |

**本计划明确不产生的新符号:** 零新增令牌、零新 CSS 自定义属性、零新文件、零新依赖、零新构建步骤;`.markdown-body` / `.event-content` / `.chat-bubble` / `.say-chunk` / `.annotation-note` / `.annotation-answer-body` 六个既有选择器**没有**新增任何规则块(只被新规则的选择器列表引用)。

<tasks>

<task type="auto">
  <name>Task 1: L-3 换行与 flex 最小尺寸 —— 六目标 `anywhere` + 两处 `min-width: 0`</name>
  <files>frontend/style.css</files>
  <read_first>
    - `frontend/style.css` L1263-1265 —— **文件末尾的三条嵌入标题刻度规则**(`.event-content h1, .chat-bubble h1, …` / `h2` / `h3`),新规则**追加在这三行之后**;L1229-1262 是 Phase 5 `idi-05-04` 的注入目标枚举注释,新规则的注释与它相邻
    - `frontend/style.css` L453-460 —— `#main-pane` 规则体**现状逐字**(`flex: 1 1 auto` / `display: flex` / `flex-direction: column` / `gap: var(--space-1-5)` / `overflow-y: auto` / `align-items: center`);`min-width: 0;` 加在 `align-items: center;` 之后
    - `frontend/style.css` L468-475 —— `#doc-panel` 规则体**现状逐字**(`flex: 0 0 var(--doc-panel-w)` / `display: flex` / `flex-direction: column` / `overflow-y: auto` / `border-left` / `background`);`min-width: 0;` 加在 `background: var(--color-surface);` 之后
    - `frontend/style.css` L447-450 —— `#app { display: flex; height: 100vh; }`,D-09 的语境(两个子项都是 `min-width: auto`)
    - `frontend/style.css` L564-577 —— `.event-list` 规则体与它下方的 `.streaming` / `.aborted` 两条(**本任务只读**,限高删除是 Task 2 的事)
    - `frontend/style.css` L598-602 —— `.event-content { flex: 1; word-break: break-all; white-space: pre-wrap; }`,**已裁定、不动**;新规则对它渲染零影响,但仍列入六目标以保证枚举与渲染目标一一对应
    - `frontend/style.css` L709-712 —— `.markdown-body { line-height: var(--lh-reading); font-size: var(--text-md); }`(六目标之一,现零换行保护)
    - `frontend/style.css` L812-819 —— `.chat-bubble`(现 `word-break: break-word`;注意 `break-word` **不**参与 min-content 计算,这正是本任务要改的那一处行为)
    - `frontend/style.css` L838(`.say-chunk { margin: var(--space-half) 0; }`)、L959(`.annotation-note { color: var(--color-text); }`)、L997(`.annotation-answer-body { margin-top: var(--space-half); }`)—— 另外三个零保护目标
    - `scripts/check-05-ui-uat.py` L880-935 —— `MARKDOWN_TARGETS`(九个渲染目标)与 `check_render_markdown_call_sites` 的调用点普查守卫。**本任务的六目标与它必须一致** —— 六目标 = `.markdown-body`(宿主 `#doc-panel-body` / `#latest-check`)+ 五个 `embedded` 家族成员;`#draft-content` / `#brainstorm-content` / `#round-doc` 三个 doc 家族宿主都带 `.markdown-body` 类,故被第一条选择器覆盖
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`### L-3 换行与 flex 最小尺寸` —— 新规则的**逐字注释文本**、六目标的 HEAD 换行保护现状表、声明组织方式的裁定(合并为一条六选择器列表)
    - `.planning/phases/idi-06-layout-robustness/idi-06-PATTERNS.md` §`B-2` 与 §`A-3` / §`A-4` —— 追加位置与两处原地新增的形态
    - `.planning/phases/idi-06-layout-robustness/idi-06-01-SUMMARY.md` §`测量决策记录` —— 波次 1 的三宽度基线数值(本任务落地后三宽度会变,计划 03 才重测)
  </read_first>
  <action>
    **第 1 步 —— 在 `frontend/style.css` 文件末尾追加一条六选择器规则。**

    位置:紧接文件末尾的三条嵌入标题刻度规则(`.event-content h1, …` / `h2` / `h3`)之后,**不重排任何既有规则**(硬规则 3)。

    选择器列表逐字、顺序逐字:`.markdown-body, .event-content, .chat-bubble, .say-chunk, .annotation-note, .annotation-answer-body`。声明体只有一条:`overflow-wrap: anywhere;`。

    规则上方必须带 UI-SPEC §L-3 给出的**逐字注释**,它承载三条理由,缺一即会被读成任选:(1) 六目标枚举与 `renderMarkdown()` 的调用点一一对应(Phase 5 `idi-05-04` 已建立该枚举,见 `MARKDOWN_TARGETS`);(2) **不写通配规则** —— 那会波及已裁定的 `.event-content` 的 `word-break: break-all`,并把「哪些容器受影响」重新变成不可枚举,那正是 `G-idi-05-1` 的成因;(3) **必须用 `anywhere` 而非 `break-word`** —— 按 CSS Text 3,只有 `anywhere` 参与 min-content 内在尺寸计算,`break-word` 不参与,这是 `min-width: 0` 能生效的前提。注释还须写明:`.event-content` 已在 `break-all` 之下(`break-all` 同样影响 min-content),故本处的 `anywhere` 对它渲染零影响 —— **仍列入六目标**,因为枚举必须与渲染目标一一对应(部分枚举正是缺陷存活的原因)。

    **第 2 步 —— `#main-pane` 与 `#doc-panel` 两条既有规则体内各原地新增一行 `min-width: 0;`。**

    `#main-pane`:加在 `align-items: center;` 之后。`#doc-panel`:加在 `background: var(--color-surface);` 之后。**两条规则块不移动,既有声明一字不动** —— 这是「原地改声明」而非「新增规则」。

    每处声明**正上方**加一段 2–3 行注释,写明 D-09 的理由(否则会被当成冗余代码删掉):`#app` 的两个 flex 子项都是 `min-width: auto` ⇒ `flex-basis` 不是硬约束、`min-width: auto` 胜出,长不可断内容能把 `#doc-panel` 顶得比它的 `clamp()` 还宽;上面的 `anywhere` 落地后 min-content 会塌缩,本行看似冗余 —— **它不依赖「六个目标长期全覆盖」**,将来新增一个未被 `overflow-wrap` 覆盖的渲染容器时仍能兜住,**不得当作冗余代码删除**。

    **注释文本的硬约束:** 两段注释**不得**把该声明连分号一起复写出来(即不得出现 `min-width: 0;` 这个带分号的串)。理由:验收用 `grep -o 'min-width: 0;' | wc -l` 计数,注释里的同形串会把计数从 2 抬到 4。注释里写 `min-width: 0`(不带分号)即可。同理六目标规则的注释**不得**复写 `overflow-wrap: anywhere;`(带分号),计数须保持 1。

    另:两段注释与规则注释都**不得**包含字符串 `@media`、`!important`、`#hex`、`@layer`、`@property`、`var(--x, #fallback)` —— 它们会被本阶段与后续阶段的守卫命令在 `frontend/style.css` 上扫到。

    **第 3 步 —— 运行时验证(硬规则 7)。** 改完必须实跑:`check-01` / `check-02` / `check-03` / `check-04`,以及 `--item smoke,1,4,7,8`(本计划不改 harness,这五项必须与波次 1 结束时逐条一致)。另外**重跑 `--item 8` 并抄录三项诊断的新数值**:本任务落地后三宽度文档级 `scrollWidth` 会变化,把新数值与 `idi-06-01-SUMMARY.md` 的基线值**并列**记入本计划的 SUMMARY —— 计划 03 的 L-2 决策读的是**本任务之后**的数值,基线值是它的对照。这一步不是可选的留痕:没有对照就无法区分「L-3 修好了」与「本来就没破」。
  </action>
  <verify>
    <automated>grep -o 'overflow-wrap: anywhere;' frontend/style.css | wc -l</automated>
    <fails_when>the count is not exactly 1</fails_when>
    <automated>grep -c '^\.markdown-body, \.event-content, \.chat-bubble, \.say-chunk, \.annotation-note, \.annotation-answer-body {' frontend/style.css</automated>
    <fails_when>the count is not exactly 1</fails_when>
    <automated>grep -o 'min-width: 0;' frontend/style.css | wc -l</automated>
    <fails_when>the count is not exactly 2</fails_when>
    <automated>grep -n -A 9 '^#main-pane {' frontend/style.css | grep -o 'min-width: 0;' | wc -l; grep -n -A 9 '^#doc-panel {' frontend/style.css | grep -o 'min-width: 0;' | wc -l</automated>
    <fails_when>either count is not exactly 1</fails_when>
    <automated>grep -o 'word-break: break-all;' frontend/style.css | wc -l; grep -o 'white-space: pre-wrap;' frontend/style.css | wc -l</automated>
    <fails_when>either count is not exactly 1 (the adjudicated `.event-content` protection must survive untouched)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>any of the three prints anything other than exactly `PASS`, or exits non-zero</fails_when>
    <automated>python3 scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>the last line is not exactly `PASS: 0 failures`</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,4,7,8</automated>
    <fails_when>exit code is not 0, or the summary reports anything other than `item smoke: PASS`, `item 1: PASS`, `item 4: PASS`, `item 7: PASS`, `item 8: PASS`</fails_when>
    <automated>grep -c '@media' frontend/style.css</automated>
    <fails_when>the count is not 0 (the narrow-window guard is plan idi-06-03's conditional deliverable — this task must not write it)</fails_when>
  </verify>
  <acceptance_criteria>
    - `overflow-wrap: anywhere;` 声明数 == 1,且其选择器行逐字为 `.markdown-body, .event-content, .chat-bubble, .say-chunk, .annotation-note, .annotation-answer-body {`
    - 该规则位于文件**末尾**(`grep -n '^\.markdown-body, \.event-content' frontend/style.css` 的行号大于三条嵌入标题刻度规则的行号),未插入到任何既有规则之间
    - `min-width: 0;` 声明数 == 2,且分别在 `#main-pane` 与 `#doc-panel` 的规则体内(`grep -n -A 9` 各命中 1 次)
    - `git diff -- frontend/style.css` 的 hunk 里 `#main-pane` 与 `#doc-panel` 两条规则**只有新增行**(注释 + `min-width: 0;`),既有声明一行未改
    - `.event-content` 的 `word-break: break-all;` 与 `white-space: pre-wrap;` 逐字保留(计数各 == 1)
    - 围栏 `:root` 内零改动:`git diff -- frontend/style.css` 的 hunk 中没有任何行落在围栏 START/END 之间(零新增令牌)
    - `frontend/style.css` 内 `@media` 计数 == 0
    - `--item smoke` / `--item 1` / `--item 4` / `--item 7` / `--item 8` 五项全 PASS(0 FAIL / 0 BLOCKED),断言条数不低于波次 1 结束时的值
    - `idi-06-02-SUMMARY.md` 含本任务之后的三宽度诊断新数值,并与 `idi-06-01-SUMMARY.md` 的基线值并列对照
    - `bash scripts/check-01-token-conformance.sh` / `check-03` / `check-04` 均 `PASS`;`check-02` 仍 `PASS: 0 failures`
  </acceptance_criteria>
  <done>六选择器 `overflow-wrap: anywhere` 规则追加在文件末尾(带三条理由的逐字注释),`#main-pane` 与 `#doc-panel` 两条既有规则体内各原地新增一行 `min-width: 0;`(带「不是冗余」的注释),两条规则块的既有声明零改动,`.event-content` 的既有裁定逐字保留;四条既有守卫全绿,`--item smoke,1,4,7,8` 五项全 PASS,三宽度诊断新数值已与基线并列记入 SUMMARY。</done>
</task>

<task type="auto">
  <name>Task 2: L-4 滚动容器收敛 —— `.event-list` 与 `#annotation-list` 各删两条声明</name>
  <files>frontend/style.css</files>
  <read_first>
    - `frontend/style.css` L564-577 —— `.event-list` 规则体**现状逐字**(`display: flex` / `flex-direction: column` / `gap: var(--space-1-5)` / `max-height: 55vh` / `overflow-y: auto` / `border` / `border-radius` / `padding` / `background` / `transition: background-color 0.3s`)与下方 `.streaming` / `.aborted` 两条。**要删的是 `max-height: 55vh;` 与 `overflow-y: auto;` 两行,其余逐字保留**
    - `frontend/style.css` L913-920 —— `#annotation-list` 规则体**现状逐字**(`display: flex` / `flex-direction: column` / `gap: var(--space-2-5)` / `max-height: 32vh` / `overflow-y: auto` / `padding: var(--space-half)`)。**要删的是 `max-height: 32vh;` 与 `overflow-y: auto;` 两行**;`padding: var(--space-half);` **必须保留** —— 它是 L-5 普查的输入(计划 03 要读它)
    - `frontend/style.css` L1114-1122 —— `#latest-check` 规则体(`max-height: 30vh` / `overflow-y: auto` / `padding` / `border` / `border-radius` / `background` / `font-size`)。**只读,一字不动** —— 去掉限高会把裁决按钮推出视口
    - `frontend/style.css` L783-811 —— `#session-panel` 族(`flex: 1 1 auto` / `min-height: 200px` / `.panel-body` / 两条 `:has(:empty)` 空态规则 / `#chat-messages` 的 `flex: 1` / `min-height: 160px` / `overflow-y: auto`)。**只读,一字不动**(D-12)
    - `frontend/style.css` L447-450 / L458 / L472 —— `#app { display: flex }`、`#main-pane { overflow-y: auto }`(唯一外层滚动者,保留)、`#doc-panel { overflow-y: auto }`(不在面板区普查范围内,保留)
    - `frontend/index.html` L20(`#chat-messages`)、L35(`#annotation-list`)、L47(`#latest-check`)、L76(`#ai-events` 带 `class="event-list"`)—— 四个滚动者所在的 DOM 位置:**`#main-pane` 及其后代**是面板区,`#doc-panel` 是另一列
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`### L-4 滚动容器收敛(LAYOUT-04)` —— 六个容器的 HEAD / 动作 / 理由表、保留 `#latest-check` 的理由、SC#3 的偏离登记、门的三条断言
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`## Deliberate Delta Ledger(本阶段)` 的 D6-4 / D6-5 —— 这两条是**行为变更而非纯视觉**,必须在本计划的 SUMMARY 里显式登记
    - `.planning/phases/idi-06-layout-robustness/idi-06-PATTERNS.md` §`A-1` / §`A-2` —— 原地删除的形态与「删声明、不移动规则块」的先例
  </read_first>
  <action>
    **第 1 步 —— `.event-list` 规则体内原地删两行。** 删掉 `max-height: 55vh;` 与 `overflow-y: auto;` 两行。**规则块位置不动,其余八条声明逐字不变**:`display: flex` / `flex-direction: column` / `gap: var(--space-1-5)` / `border: 1px solid var(--color-border-subtle)` / `border-radius: var(--radius-sm)` / `padding: var(--space-2)` / `background: var(--color-surface)` / `transition: background-color 0.3s`。下方 `.event-list.streaming { background: var(--color-surface-streaming); }` 与 `.event-list.aborted { background: var(--color-surface-danger); }` 两条**一字不动** —— `.aborted` 是已交付的 SSE 修复(REG-03 的复验对象),`transition` 归 Phase 7(INTERACT-02)。

    在规则体上方加一行注释,写明这次删除是 **L-4 的刻意收敛**(行为变更:AI 面板不再内部滚动,条目随 `#main-pane` 滚动),并点名门是 `check-05 --item 9`。注释**不得**包含 `@media` / `!important` / `#hex` / `@layer` / `@property`。

    **第 2 步 —— `#annotation-list` 规则体内原地删两行。** 删掉 `max-height: 32vh;` 与 `overflow-y: auto;` 两行。**`padding: var(--space-half);` 必须保留**(L-5 普查的输入),`display` / `flex-direction` / `gap: var(--space-2-5)` 逐字不变。同样加一行注释写明是 L-4 的刻意收敛(行为变更:批注面板不再内部滚动)。

    **第 3 步 —— 保留项复核(不改,只确认)。** 逐条确认并记录:`#latest-check` 的 `max-height: 30vh;` 与 `overflow-y: auto;` 仍在(去掉它会把 `#check-controls` 里的裁决按钮推出视口);`#chat-messages` 的 `overflow-y: auto;` 仍在;`#session-panel` 族的每一条声明仍在;`#main-pane` 的 `overflow-y: auto;` 仍在(唯一外层滚动者)。**这四项是「保留」而非「遗漏」,计划 03 的 item 9 会断言它们。**

    **第 4 步 —— 运行时验证(硬规则 7)。** 改完必须实跑:`check-01` / `check-02` / `check-03` / `check-04`,以及 `--item smoke,1,4,7,8`(五项必须与波次 1 结束时逐条一致 —— 本计划到此为止不改 harness)。**另外**把两条 Delta 显式登记进 SUMMARY:D6-4(`.event-list` 删限高 ⇒ AI 面板不再内部滚动,条目随 `#main-pane` 滚动)与 D6-5(`#annotation-list` 同上),二者都是**行为变更,不是纯视觉**。
  </action>
  <verify>
    <automated>grep -o 'max-height: 55vh;' frontend/style.css | wc -l; grep -o 'max-height: 32vh;' frontend/style.css | wc -l</automated>
    <fails_when>either count is not 0</fails_when>
    <automated>grep -o 'max-height: 30vh;' frontend/style.css | wc -l</automated>
    <fails_when>the count is not exactly 1 (`#latest-check` keeps its limit — removing it pushes the verdict buttons below the fold)</fails_when>
    <automated>grep -o 'overflow-y: auto;' frontend/style.css | wc -l</automated>
    <fails_when>the count is not exactly 3 (HEAD has 5; L-4 deletes 2 ⇒ `#main-pane` / `#chat-messages` / `#latest-check` remain)</fails_when>
    <automated>grep -n -A 9 '^\.event-list {' frontend/style.css | grep -o 'transition: background-color 0.3s;' | wc -l; grep -c '^\.event-list.streaming {' frontend/style.css; grep -c '^\.event-list.aborted {' frontend/style.css</automated>
    <fails_when>any count is not exactly 1 (the streaming/aborted states and the transition are Phase 7 / REG-03 material and must survive untouched)</fails_when>
    <automated>grep -n -A 6 '^#annotation-list {' frontend/style.css | grep -o 'padding: var(--space-half);' | wc -l</automated>
    <fails_when>the count is not exactly 1 (the list padding is the input to plan idi-06-03's L-5 clearance census)</fails_when>
    <automated>grep -o 'min-height: 160px;' frontend/style.css | wc -l; grep -o 'min-height: 200px;' frontend/style.css | wc -l; grep -c '^#session-panel {' frontend/style.css</automated>
    <fails_when>any count is not exactly 1 (`#chat-messages` keeps its floor and `#session-panel` keeps its flex/min-height — the input row must stay pinned to the bottom)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>any of the three prints anything other than exactly `PASS`, or exits non-zero</fails_when>
    <automated>python3 scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>the last line is not exactly `PASS: 0 failures`</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,4,7,8</automated>
    <fails_when>exit code is not 0, or the summary reports anything other than `item smoke: PASS`, `item 1: PASS`, `item 4: PASS`, `item 7: PASS`, `item 8: PASS`</fails_when>
  </verify>
  <acceptance_criteria>
    - `max-height: 55vh;` 与 `max-height: 32vh;` 计数均为 0;`max-height: 30vh;` 计数 == 1(`#latest-check` 保留)
    - `overflow-y: auto;` 计数 == 3(`#main-pane` / `#chat-messages` / `#latest-check`);HEAD 的 5 处中恰有 2 处被删
    - `git diff -- frontend/style.css` 的 hunk 里 `.event-list` 与 `#annotation-list` 两条规则**只有删除行**,其余声明与规则位置逐字不变(硬规则 3)
    - `.event-list` 的 `transition: background-color 0.3s;` 仍在;`.event-list.streaming {` 与 `.event-list.aborted {` 各仍为 1 处
    - `#annotation-list` 的 `padding: var(--space-half);` 仍在(计数 == 1)
    - `#chat-messages` 的 `min-height: 160px;`、`#session-panel {` 的 `min-height: 200px;` 与 `#session-panel {` 规则本身各仍在(计数各 == 1)
    - 围栏 `:root` 内零改动;`frontend/style.css` 内 `@media` 计数 == 0
    - `idi-06-02-SUMMARY.md` 显式登记 D6-4 与 D6-5 两条 **行为变更**(不是纯视觉)
    - `--item smoke` / `--item 1` / `--item 4` / `--item 7` / `--item 8` 五项全 PASS(0 FAIL / 0 BLOCKED)
    - `bash scripts/check-01-token-conformance.sh` / `check-03` / `check-04` 均 `PASS`;`check-02` 仍 `PASS: 0 failures`
  </acceptance_criteria>
  <done>`.event-list` 与 `#annotation-list` 两条既有规则体内各原地删掉两行限高与内滚动声明,规则块与其余声明逐字不变;`#latest-check` / `#chat-messages` / `#session-panel` 族 / `#main-pane` 四处保留项逐条复核通过;两条行为变更(D6-4 / D6-5)登记进 SUMMARY;四条既有守卫与五项 harness 门全绿。</done>
</task>

<task type="auto">
  <name>Task 3: item 9 —— 面板区滚动者 DOM 普查 + 末条可达性 + `max-height == none`</name>
  <files>scripts/check-05-ui-uat.py</files>
  <read_first>
    - `scripts/check-05-ui-uat.py` L86-175 —— 断言记录器全文(`ok` 的两处 BLOCKED 方向、`ok_true`、`blocked`、`info`)。**新增断言必须用满两处 BLOCKED 方向**
    - `scripts/check-05-ui-uat.py` L880-945 —— `MARKDOWN_TARGETS` / `MARKDOWN_HOSTS` / `RENDER_TARGETS` 与 `check_render_markdown_call_sites`。**本任务照抄它的两条纪律**:(1) 比的是「实际值 vs 期望值」两个独立量,不是自比;(2) FAIL 消息要给出**可执行的下一步动作**
    - `scripts/check-05-ui-uat.py` L1411-1517 —— item7 的新项骨架(样本 → `enter_project` → 经应用自身渲染函数注入内容 → 断言 → 末尾接静态守卫)。本任务的 item 9 沿用同一骨架
    - `scripts/check-05-ui-uat.py` 本阶段 Task 1 新增的 item 8 全文 —— viewport 复位、`page.evaluate` 返回 `null` 时记 BLOCKED、前提检查的写法。**item 9 沿用同一纪律**
    - `scripts/check-05-ui-uat.py` L1490-1502 —— item7 的「对 `None` 恒真」陷阱注释(本任务的可达性断言有同型风险)
    - `scripts/check-05-ui-uat.py` L1567-1636 —— `parse_args` / `normalize_items` / `main()` 的派发(本任务要把 `"9"` 接进三处);L18-40 的模块 docstring 运行方式块
    - `frontend/index.html` L20 / L35 / L47 / L76 —— 四个滚动者元素的**静态**存在性(`#chat-messages` / `#annotation-list` / `#latest-check` / `#ai-events`),它们全部常驻 DOM,与磁盘状态样本无关
    - `frontend/app.js` L237-285 —— `renderEvent` / `appendChatMessage` / `appendSayToChat`(item7 已在用它们注入内容);**只读不改**
    - `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §`### L-4 滚动容器收敛(LAYOUT-04)` 的门三件事 + §`## 契约校验命令`(item 9 的调用形式)
    - `.planning/phases/idi-06-layout-robustness/idi-06-PATTERNS.md` §`E-5`(DOM 普查守卫的两条纪律)、§`E-6`(枚举表范本)、§`E-7`(派发三处协同编辑)
  </read_first>
  <action>
    **第 1 步 —— 新增 `def item9(page, tmp_root)`。** 骨架照抄 item7 / item 8:`item = "9"` → `print("\n=== UAT 9: 面板区滚动容器收敛(LAYOUT-04)===", flush=True)` → `proj = make_fixture("p1", tmp_root)` → `enter_project(page, proj)` → `info(...)` → 断言。

    **(a) 滚动者 DOM 普查(两条断言,比的是两个独立量)。** 在 `page.evaluate` 里遍历 `#main-pane` **及其全部后代**,读每个元素的 computed `overflow-y`,把值为 `auto` 或 `scroll` 的元素收集为一个**扁平的选择器标识数组**(优先用 `id`,无 `id` 时用 `tagName + '.' + className`)。返回该数组。Python 侧先断言 `#main-pane` 自身在数组内(否则探针跑错了范围 ⇒ `blocked(...)`),然后:

    - 断言一(全集):数组排序后 == `["#chat-messages", "#latest-check", "#main-pane"]`。**这条抓的是「意外新增第四个滚动者」这类回归** —— 它是 D-14 口径取「恰好」而非「至多」的全部理由。
    - 断言二(排除豁免后):把 `#chat-messages` 从数组里滤掉,剩下的排序后 == `["#latest-check", "#main-pane"]`。**这条是 D-14 第 1 条的**字面**读法**(「面板区内恰好两个滚动容器」),而 SC#3 明文写「`#chat-messages` 除外」—— 两条断言同时成立,故两种读法都被机械覆盖。

    两条断言都用 `ok_true`,expected 侧写期望集合、actual 侧写实测集合,**并在 `info()` 里打印完整数组**(失败可独立诊断)。数组为空或探针返回 `null` ⇒ `blocked(...)`,**绝不**把「空集合 == 空集合」记成 PASS。

    **普查的状态无关性必须在注释里写明:** 这七个 `overflow` 声明所在的元素全部是 `index.html` 的静态元素,与磁盘状态样本无关,故普查在 `p1` 下得到的结论对五个样本同样成立 —— 这是本断言比「按状态样本逐格探」更强的地方。

    **(b) 末条可达性(D-14 第 2 条)。** 先**注入足量内容**(经应用自身的渲染路径,不手工拼 DOM):用 `renderEvent({ kind: 'say', content: … })` 反复注入足量事件条目到 `#ai-events`,并用 `renderMarkdown` 把一段长 markdown 渲染进 `#latest-check`(与 item4 / item7 的探针同一手法)。然后对 `#main-pane` 与 `#latest-check` 各做一次:
    - 读 `scrollHeight` / `clientHeight` / `scrollTop`。若 `scrollHeight <= clientHeight`(该容器无需滚动)⇒ 用 `info()` 报告「无需滚动,可达性平凡成立」,**不记断言**(避免空转 PASS);若 `scrollHeight > clientHeight` ⇒ 把 `scrollTop` 设为 `scrollHeight` 并断言 `scrollTop + clientHeight >= scrollHeight - 1`(滚到底)。
    - **无论是否需要滚动,都断言可达性不变量:** 滚到底之后,该容器的**最后一个子元素**的 `getBoundingClientRect()` 落在容器 rect 之内(`last.bottom <= container.bottom + 1 && last.top >= container.top - 1`)。这条是「内容可达」的真正主张 —— 它抓的是「条目被限高截断后看不见」这一原始缺陷,而不是「滚动条动没动」。
    - 最后一条子元素读不到(容器无子元素 / 探针返回 `null`)⇒ `blocked(...)`,**绝不**记 PASS。这与 item7 已登记的「对 `None` 恒真」陷阱同型。

    **(c) 两处限高确已消失(D-14 第 3 条)。** `ok(item, "[p1] #ai-events 计算 max-height == none", "none", read_style(page, "#ai-events", "max-height"))` 与 `ok(item, "[p1] #annotation-list 计算 max-height == none", "none", read_style(page, "#annotation-list", "max-height"))`。**注意:`read_style` 对 `display: none` 的元素同样返回解析后的 computed 值**(computed style 不依赖布局),故这两条在 `p1`(`#annotation-list` 可能被隐藏)下依然有效 —— 把这一点写进注释,否则后续维护者会以为需要切样本。元素读不到时 `read_style` 返回 `None` ⇒ `ok()` 自动记 BLOCKED。

    **(d) 保留项护栏两条。** `ok(item, "[p1] #latest-check 仍保留 max-height == 30vh", "30vh", read_style(page, "#latest-check", "max-height"))` 与 `ok(item, "[p1] #chat-messages overflow-y == auto", "auto", read_style(page, "#chat-messages", "overflow-y"))`。这两条是 D-11 保留理由的机器化形态,防止计划 03 或后续阶段顺手删掉它们。

    **(e) viewport 纪律。** item 9 不需要变更 viewport;若调试期用过 `set_viewport_size`,必须在返回前复位 1440×900(与 item 8 同一纪律)。

    **第 2 步 —— 派发接入(PATTERNS.md E-7 的三处协同编辑)。** `normalize_items` 的默认列表加 `"9"`;`main()` 的 `known` 集合加 `"9"`;`main()` 的派发链在 `if "8" in items:` 之后加 `if "9" in items: item9(page, tmp_root)`。同步更新模块 docstring 的运行方式块与 `parse_args` 的 `--item` help 字符串(项清单加 `9`)。汇总块按 `items` 迭代 `ROWS`,自动适配,无需改动。

    **第 3 步 —— 运行时验证(硬规则 7)。** 实跑 `--item 9`(新项)与 `--item smoke,1,4,7,8`(既有项无回归),并把两项的逐项结论抄进 SUMMARY。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 9</automated>
    <fails_when>exit code is not 0, or the `=== 逐项结论 ===` block reports anything other than `item 9: PASS`, or any assertion line reports `FAIL` or `BLOCKED`</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,4,7,8</automated>
    <fails_when>exit code is not 0, or the summary reports anything other than `item smoke: PASS`, `item 1: PASS`, `item 4: PASS`, `item 7: PASS`, `item 8: PASS`</fails_when>
    <automated>grep -c 'def item9' scripts/check-05-ui-uat.py; grep -c 'if "9" in items' scripts/check-05-ui-uat.py; grep -o '"9"' scripts/check-05-ui-uat.py | wc -l</automated>
    <fails_when>the first count is not 1, or the second count is not 1, or the third count is less than 3</fails_when>
    <automated>grep -o 'overflow-y' scripts/check-05-ui-uat.py | wc -l; grep -o 'max-height' scripts/check-05-ui-uat.py | wc -l</automated>
    <fails_when>either count is less than 2 (the census reads computed `overflow-y`; the assertions read computed `max-height` on both converged containers and both retained guards)</fails_when>
    <automated>grep -o 'scrollHeight' scripts/check-05-ui-uat.py | wc -l; grep -o 'getBoundingClientRect' scripts/check-05-ui-uat.py | wc -l</automated>
    <fails_when>either count is less than 2 (reachability requires reading scrollHeight/clientHeight and the last child's rect)</fails_when>
    <automated>grep -o 'renderEvent(' scripts/check-05-ui-uat.py | wc -l; grep -o 'renderMarkdown(' scripts/check-05-ui-uat.py | wc -l</automated>
    <fails_when>either count is less than 1 (content must be injected through the app's own render paths, never hand-built DOM)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>any of the three prints anything other than exactly `PASS`, or exits non-zero</fails_when>
    <automated>python3 scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>the last line is not exactly `PASS: 0 failures`</fails_when>
    <automated>git status --porcelain -- frontend/app.js frontend/index.html frontend/vendor/ scripts/check-01-token-conformance.sh scripts/check-02-contrast.py scripts/check-03-hidden-uniqueness.sh scripts/check-04-important-count.sh scripts/check-06-idi05-validation.py scripts/ui-states/</automated>
    <fails_when>the output is not empty</fails_when>
  </verify>
  <acceptance_criteria>
    - `check-05-ui-uat.py` 内新增 `def item9(`;`if "9" in items` 恰 1 处;`"9"` 字面量 ≥3 处(默认列表 / `known` / 派发)
    - item 9 的滚动者普查在 `page.evaluate` 内遍历 `#main-pane` 及其后代(不是硬编码选择器列表),且 Python 侧先断言 `#main-pane` 自身在结果内
    - item 9 含两条滚动者集合断言(全集 == 三者;排除 `#chat-messages` 后 == 两者),expected 与 actual 都是集合(两个独立量,不是自比)
    - item 9 的末条可达性断言先注入内容(经 `renderEvent` / `renderMarkdown`),并含 `scrollHeight` / `clientHeight` 与末条 `getBoundingClientRect()` 的读数;容器无需滚动时用 `info()` 报告而非记断言;末条读不到时记 `blocked(...)`
    - item 9 含 `#ai-events` 与 `#annotation-list` 两条计算 `max-height == none` 断言,以及 `#latest-check` 的 `30vh` 与 `#chat-messages` 的 `auto` 两条保留项护栏
    - `--item 9` 全 PASS(0 FAIL / 0 BLOCKED),输出里含实测滚动者数组
    - `--item smoke` / `--item 1` / `--item 4` / `--item 7` / `--item 8` 五项仍全 PASS(0 FAIL / 0 BLOCKED),断言条数不低于波次 1 结束时的值
    - `bash scripts/check-01-token-conformance.sh` / `check-03` / `check-04` 均 `PASS`;`check-02` 仍 `PASS: 0 failures`
    - `git status --porcelain -- frontend/app.js frontend/index.html frontend/vendor/ scripts/check-01…04 scripts/check-06-idi05-validation.py scripts/ui-states/` 输出为空
  </acceptance_criteria>
  <done>item 9 落地并接入派发三处,滚动者 DOM 普查两条断言在 `p1` 下实测集合恰为 `{#main-pane, #chat-messages, #latest-check}`(排除豁免后恰为两者);`#main-pane` 与 `#latest-check` 的末条可达性断言在注入足量内容后通过;两处 `max-height == none` 与两条保留项护栏齐备;`--item 9` 与 `--item smoke,1,4,7,8` 全部全绿。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 本阶段无新增信任边界 | 纯 `frontend/style.css` 的声明增删 + `scripts/check-05-ui-uat.py` 的断言新增。零新增网络面、零新增输入面、零新增持久化数据、零新增依赖、零新增文件(`frontend/app.js` / `index.html` / `vendor/` 零 diff) |
| 磁盘 → 浏览器 | `frontend/style.css` 是唯一被消费的样式来源;围栏 `:root` 是令牌的唯一事实源。本计划**零新增令牌**,故不产生第二个事实源 |
| 内容 → 可达性 | 本计划把两个内层滚动者移除,把可达性责任移交给 `#main-pane`。若移交不完整(内容既不被内层滚动承载、又不被外层承载),用户会看到**被截断且无法到达**的内容 —— 这是本计划唯一的新失败模式,由 item 9 的末条可达性断言收口 |
| 应用 JS → harness | item 9 用应用自身的 `renderEvent` / `renderMarkdown` 注入内容,而不是手工拼 DOM。越界会测到应用永远不会产生的状态,使断言失去证明力 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-06-06 | Denial of Service / Repudiation | 内容可达性(删除两个内层滚动者之后) | high | mitigate | item 9 的末条可达性断言:注入足量内容 → 滚到底 → 断言容器最后一个子元素落在容器 rect 之内。**这是「内容不可达」这一失败模式的唯一机器化形态**;容器无需滚动时用 `info()` 报告而非空转 PASS |
| T-idi-06-07 | Tampering | 交互面被推到折叠线以下 | high | mitigate | `#latest-check` 的 `max-height: 30vh` 保留(prohibition 2),并由 item 9 的保留项护栏断言为 `30vh`;`#chat-messages` 的 `overflow-y` 保留并断言为 `auto`;`#session-panel` 族零改动(D-12 / prohibition 3) |
| T-idi-06-08 | Tampering | `frontend/style.css` 的四条守卫不变量 | high | mitigate | 每个任务复跑 CHECK-01 / 02 / 03 / 04;围栏标记 1/1;`^\.hidden {` == 1;`!important` **声明**数 == 1;新增注释与规则体内不得出现 `!important` / `#hex` / `@layer` / `@property` / `var(--x, #fallback)`(硬规则 2 / 4) |
| T-idi-06-09 | Tampering | 源码顺序被重排(硬规则 3) | medium | mitigate | 删除一律原地改声明、新增一律追加在文件末尾;验收以 `git diff` 的 hunk 形态为准(`.event-list` / `#annotation-list` 两条规则只有删除行,`#main-pane` / `#doc-panel` 只有新增行) |
| T-idi-06-10 | Denial of Service | 假 PASS(空转断言) | high | mitigate | 滚动者普查在探针返回 `null` / 数组为空时记 `blocked(...)`;可达性断言在末条元素读不到时记 `blocked(...)`;容器无需滚动时记 `info()` 而非断言。与 item7 已登记的「对 `None` 恒真」陷阱同型 |
| T-idi-06-11 | Information Disclosure | 本计划的改动内容 | low | accept | 改动只有四条声明的新增/删除与一条换行规则,无用户数据、无网络请求、无外部资源;`frontend/vendor/` 仍只含 `marked.min.js` |
| T-idi-06-SC | Tampering | npm / pip / cargo 安装 | high | mitigate | 本阶段零安装(硬规则 6):不新增任何依赖、文件或构建步骤;`git status --porcelain -- frontend/vendor/` 为空。无 `[ASSUMED]` / `[SUS]` 包,故无需 package-legitimacy 人工签核门 |

**ASVS L1 口径:** 本阶段零新增输入面、零新增网络调用、零新增持久化,故 ASVS 的注入 / 认证 / 会话类威胁不适用。上表 `high` 四项(T-idi-06-06 / 07 / 08 / 10)是本阶段真实的失败模式:内容不可达、交互面被推出视口、守卫不变量被打破、断言空转。四者分别由 item 9 的三类断言、保留项护栏、四条守卫复跑与 `blocked(...)` 前提检查收口。
</threat_model>

<verification>
- `bash scripts/check-01-token-conformance.sh` → `PASS` / exit 0
- `python3 scripts/check-02-contrast.py | tail -1` → `PASS: 0 failures`
- `bash scripts/check-03-hidden-uniqueness.sh` → `PASS`(`^\.hidden {` == 1)
- `bash scripts/check-04-important-count.sh` → `PASS`(`!important;` 声明数 == 1)
- `.venv/bin/python scripts/check-05-ui-uat.py --item 9` → `item 9: PASS`(0 FAIL / 0 BLOCKED)
- `.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,4,7,8` → 五项全 PASS,断言条数不低于波次 1 结束时
- Gate A(围栏纯度):`git diff -- frontend/style.css` 的 hunk 中没有任何行落在围栏 START/END 之间(零新增令牌)
- Gate B(硬规则 3):`git diff -- frontend/style.css` 里 `.event-list` / `#annotation-list` 两条规则只有删除行,`#main-pane` / `#doc-panel` 两条规则只有新增行,无任何规则块位置变化
- Gate C(保留项):`grep -o 'overflow-y: auto;' frontend/style.css | wc -l` == 3 且 `grep -o 'max-height: 30vh;' frontend/style.css | wc -l` == 1
- Gate D(零外溢):`git status --porcelain -- frontend/app.js frontend/index.html frontend/vendor/ scripts/ui-states/ scripts/check-01-token-conformance.sh scripts/check-02-contrast.py scripts/check-03-hidden-uniqueness.sh scripts/check-04-important-count.sh scripts/check-06-idi05-validation.py` 输出为空
- Gate E(证据落盘):`idi-06-02-SUMMARY.md` 含三宽度诊断新数值(与波次 1 基线并列)、D6-4 / D6-5 两条行为变更登记、`--item 9` 的逐项结论
</verification>

<success_criteria>
- 六目标 `overflow-wrap: anywhere` 规则落地,`.event-content` 的既有裁定逐字保留、未被通配规则波及
- `#main-pane` 与 `#doc-panel` 各获 `min-width: 0`,`#doc-panel` 不再能被不可断长内容顶得比 `clamp()` 还宽
- 面板区滚动容器从「3 个嵌套 + 1 个外层」收敛为「1 个外层 + 1 个保留的内层 + 1 个明文豁免的会话流滚动者」,收敛结果由 item 9 的 DOM 普查机械复核
- `#latest-check` 的 30vh 内滚动保留,裁决按钮不被推出折叠线;`#chat-messages` 与 `#session-panel` 族零改动,输入行仍钉底
- Success Criterion #3 的口径偏离(A-5)在计划与 SUMMARY 里显式登记,`ROADMAP.md` / `REQUIREMENTS.md` 正文未被改动
- 四条既有守卫与五项 harness 门全绿;`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` / `scripts/ui-states/` 零 diff
</success_criteria>

<output>
Create `.planning/phases/idi-06-layout-robustness/idi-06-02-SUMMARY.md` when done
</output>
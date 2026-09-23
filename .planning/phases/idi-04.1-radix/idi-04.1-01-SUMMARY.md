---
phase: idi-04.1-radix
plan: 01
subsystem: ui
tags: [css-design-tokens, radix-colors, wcag-contrast, custom-properties, playwright, a11y]

# Dependency graph
requires:
  - phase: idi-04-tokens-contract
    provides: 围栏 `:root` 令牌块(单一事实源)、`/* PAIR */` 清单语法、四条守卫命令、CHECK-02 仲裁脚本
provides:
  - "围栏值层:25 个 tier-1 Radix primitive(24 个 `--radix-<family>-<step>` + `--white`)+ 47 个 `--color-*` 语义令牌"
  - "CHECK-02 清单重算:43 对(34 TEXT + 9 NON-TEXT)+ 1 条 ORDER,`PASS: 0 failures` / `ORDER 0.363`"
  - "围栏注释 V-12:名↔步映射表、12 步语义与四处越轨的算术、D-15 的三数差异、三处「不得好心改回」警告"
  - "围栏外三处声明 R-1(z-index)/ R-2(box-shadow)/ R-3(删 opacity),各带一条真实浏览器的运行时接线断言"
  - "`--shadow-overlay` 新令牌 + `resolve_token(page, name)` 新助手"
affects: [idi-04.1-02, idi-04.1-03, phase-5-visual, phase-6, phase-7-focus-ring]

actuals:
  tokens: 6173      # chars/4 over the realized diff (24691 chars) — same scale as the plan's estimate.tokens
  tasks: 3
  commits: 3        # MEASURED: git rev-list --count e530ead..HEAD
  plan_head_before: e530ead47e909c04b4d28083a33f09b9129a937e

tech-stack:
  added: []
  patterns:
    - "值层与结构层分离:重写只落在围栏内的值,围栏位置/标记/分层/守卫全部不动"
    - "令牌接线断言:消费者 computed 值 == 令牌运行时解析值,值层再改也不产生假 FAIL"

key-files:
  created: []
  modified:
    - frontend/style.css
    - scripts/check-05-ui-uat.py

key-decisions:
  - "D-16 核实成立:无 muted-text 类元素落在 <button> 内,该对不进清单,清单为 43 对(34 TEXT + 9 NON-TEXT)"
  - "R-3 只删 `.tier-desc` 的 `opacity: 0.9` 一条声明,`font-size` / `font-weight` 一字未动"
  - "R-1 只加 `z-index` 一条声明,不加 `position` —— `#state-badge` 刻意不是 `position: fixed` 浮层"
  - "`--shadow-overlay` 与 `.overlay-card` 的消费者同一次提交落地(Hard Rule 5),围栏外零裸 rgba()"
  - "item_smoke 的 R-2 断言用短 needle \"0.2\",不复用 item3 的完整字面 rgba(0, 0, 0, 0.2) —— 那个字面是 wave 3 的计数不变量"

patterns-established:
  - "围栏注释承载名↔步映射:上游 Radix 更新可机械同步(D-03 / V-12)"
  - "越轨记账:步带是工作假设,算术在本项目真实背景上推翻它时,越轨连同数字写进围栏"

requirements-completed: [TOKEN-01, TOKEN-02, TOKEN-04, TOKEN-07, CHECK-02, CHECK-03, CHECK-04, A11Y-04, A11Y-04b]

coverage:
  - id: D1
    description: "围栏值层换成 Radix 刻度:25 个 tier-1 primitive + 47 个 `--color-*`;CHECK-02 清单重算为 43 对 + 1 ORDER"
    requirement: "CHECK-02"
    verification:
      - kind: unit
        ref: "python3 scripts/check-02-contrast.py"
        status: pass
      - kind: unit
        ref: "bash scripts/check-01-token-conformance.sh"
        status: pass
    human_judgment: false
  - id: D2
    description: "`--color-text-muted` 的 AA 倒退(3.23:1)在声明处被刻度消解 —— muted = step 11、正文 = step 12 的同族相邻两步"
    requirement: "A11Y-04"
    verification:
      - kind: unit
        ref: "python3 scripts/check-02-contrast.py#--color-text-muted on --color-surface = 5.62"
        status: pass
    human_judgment: false
  - id: D3
    description: "`--color-border-strong` 恢复 SC 1.4.11 达标(#d9d9d9 1.41 → --radix-gray-9 3.24 / 3.15),S-3 签核意图以 Radix 步恢复"
    requirement: "A11Y-04"
    verification:
      - kind: unit
        ref: "python3 scripts/check-02-contrast.py#--color-border-strong NON-TEXT = 3.24 / 3.15"
        status: pass
    human_judgment: false
  - id: D4
    description: "围栏外三处声明 R-1 / R-2 / R-3 落地并各带一条真实浏览器的运行时接线断言"
    requirement: "TOKEN-07"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,6 (exit=0,三项结论列全 PASS)"
        status: pass
    human_judgment: false
  - id: D5
    description: "结构不变量保持:`.hidden {` 唯一、`!important;` 声明数 = 1、围栏外零裸 hex、围栏外零 tier-1 名引用"
    requirement: "CHECK-03"
    verification:
      - kind: unit
        ref: "bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh"
        status: pass
    human_judgment: false
  - id: D6
    description: "UI-SPEC 的 28 条 backstop(overflow / long-text 文本适配)在真实界面上的留出视觉确认"
    verification: []
    human_judgment: true
    rationale: "backstop 类考虑项按契约只能由显式留出/视觉证据确认,本环境无法自动化(E1 七芯片窄行、E5 面板与页面底色可分辨、E10 `.tier-desc` 满不透明度可读、E16 mark 跨行底色等)。本计划只交付了 D4 的三条令牌接线运行时断言;28 条 backstop 需在 verify-work 阶段人工/截图确认,绝不静默通过。"

# Metrics
duration: 22min
completed: 2026-09-19
status: complete
---

# Phase 04.1 Plan 01: 围栏值层 Radix 重写 + 围栏外三处声明恢复 Summary

**`frontend/style.css` 的颜色值层整体换成 Radix Colors 12 步刻度(tier-1 25 条 / tier-2 47 条),CHECK-02 清单重算为 43 对并实测 `PASS: 0 failures` + `ORDER 0.363`;同时恢复 `#state-badge` 的 `z-index` 与 `.overlay-card` 的 `box-shadow`、删除由算术强制的 `.tier-desc { opacity: 0.9 }`,三处各带一条真实浏览器的运行时接线断言。**

## Performance

- **Duration:** 22 min
- **Started:** 2026-09-19T12:37:34Z
- **Completed:** 2026-09-19T12:59:49Z
- **Tasks:** 3 / 3
- **Files modified:** 2

## Accomplishments

- **值层重写**:26 个 Tailwind 式 tier-1 primitive → 25 个(24 个 `--radix-<family>-<step>` + `--white`);49 个 `--color-*` → 47 个(名逐字冻结,只改右侧 `var()` 目标)。`--black` / `--green-800` / `--color-text-inverse` / `--color-surface-info-strong` 连同它们「对代码说谎」的注释一并删除。
- **仲裁者全绿**:`check-02-contrast.py` 输出 43 行 `PASS  ` / 0 行 `FAIL` / 末行 `PASS: 0 failures` / `ORDER 0.363`,逐条比值与 UI-SPEC `### The measured table` 完全一致(含 `--color-text-info` 的 4.53 与 `--color-border-strong` 的 3.24 / 3.15)。
- **三处结构性回归被吸收**:`--color-text-muted` 3.23:1 → 5.62(声明处消解,非手调);`--color-border-strong` 1.41 → 3.24 / 3.15(SC 1.4.11);`--color-action-primary` 3.64 → 4.77。
- **R-1 / R-2 / R-3 落地**:`--z-badge` 重新有消费者(TOKEN-07 的 `badge < banner` 序断言两端都被真实消费);`--shadow-overlay` 与 `.overlay-card` 消费者同一次提交落地,围栏外零裸 `rgba()`;`.tier-desc` 的 `opacity: 0.9` 删除后满不透明度 4.77 ✓。
- **运行时证据**:`item_smoke` 新增 `resolve_token` 助手与三条令牌接线断言,`--item smoke,1,6` 退出码 0、三项结论列全 `PASS`。
- **围栏自述性**:注释承载名↔步映射、12 步语义与四处越轨的算术、D-15 的三数差异(24 / 34 / 43)、三处「不得好心改回」的警告。

## Task Commits

Each task was committed atomically:

1. **Task 1 (tracer): 围栏值层与对比度清单的原子重写** - `c6b7735` (feat)
2. **Task 2: 围栏注释 V-12** - `d82ce87` (docs)
3. **Task 3: 围栏外三处声明 R-1/R-2/R-3 与运行时接线断言** - `00c6073` (feat)

**Plan metadata:** (docs: complete plan — 本 SUMMARY 的提交)

## Files Created/Modified

- `frontend/style.css` - 围栏值层整体换为 Radix 刻度;清单整块替换;注释 V-12;围栏外三处声明(R-1 / R-2 / R-3)+ 新增 `--shadow-overlay`(260 insertions / 115 deletions 合计跨三个任务)
- `scripts/check-05-ui-uat.py` - 新增 `resolve_token(page, name)` 助手;`item_smoke` 追加三条令牌接线断言(+24 行,零删除)

## Decisions Made

- **D-16 核实成立 → 该对不进清单。** 逐条证据见下节。清单为 43 对(34 TEXT + 9 NON-TEXT),与 UI-SPEC `### The manifest, verbatim` 和 `### The measured table` 一致。
- **R-3 只删一条声明。** `.tier-desc { font-size: var(--text-xs); font-weight: var(--fw-regular); }` —— `font-size` / `font-weight` 逐字保留(S-2 / C-1 领域)。
- **R-1 只加 `z-index`,不加 `position`。** `#state-badge` 被刻意设计为不是 `position: fixed` 浮层(style.css:579-581 的注释已写明理由);`z-index` 在非定位元素上是惰性的,它的价值在于让 `--z-badge` 重新有消费者。
- **`--shadow-overlay` 与消费者同一次提交落地**(Hard Rule 5)。Task 1 刻意不新增该令牌 —— 它必须与 `.overlay-card` 的 `box-shadow` 一起出现,否则围栏内会出现一个零消费者的声明。
- **R-2 断言的 needle 用短串 `"0.2"`。** 完整字面 `rgba(0, 0, 0, 0.2)` 在 `idi-04.1-03-PLAN.md` Task 1 里是「全文件唯一颜色字面」的计数不变量(计数 == 1);在 `item_smoke` 里再写一遍会让 wave 3 的那个门变红并把原因误诊为「漏改」。两条断言测的是同一个属性,共享的是属性而不是字面。
- **tier-1 区块按 UI-SPEC 表的族/步升序重写**(white → gray → blue → green → amber → red → violet)。这是任务明写的动作(「严格按 UI-SPEC `### Tier 1 — primitives` 表执行」);tier-1 名是一次全新集合,不存在可保留的旧位置。tier-2 与围栏外的改动则严格原位替换/追加/删除,零重排。

## D-16 前置核实(逐条 `文件:行号` 证据与结论)

**核实对象**:是否存在任何 muted-text 类元素落在 `<button>` 内部。

**A. `app.js` 中所有创建 `<button>` 的路径 —— 穷举:**

| 路径 | 行号 | 内容形态 |
|---|---|---|
| `renderVerdictCard` 的「修」按钮 | `frontend/app.js:709` | `document.createElement('button')` + `fixBtn.textContent = '修'`(711 行附近) |
| `renderVerdictCard` 的「接受现状」按钮 | `frontend/app.js:711` | `document.createElement('button')` + `keepBtn.textContent = '接受现状'` |
| `innerHTML` 含 `<button` | — | `grep -n '<button' frontend/app.js` **零命中** |

两个按钮都只写 `textContent`,**没有任何子元素**,因此不可能包含任何类元素。

**B. 五个 muted-text 类在 `app.js` / `index.html` 中的全部使用点:**

| 类 | 文件:行号 | 宿主元素 | 父容器 |
|---|---|---|---|
| `.verdict-suggestion` | `frontend/app.js:690` | `<p>`(687 行 `createElement('p')`) | `card`(677 行 `div.verdict-card`) |
| `.hint` | `frontend/app.js:1120` | `<p>`(1119 行 `createElement('p')`) | `annotationList` |
| `.annotation-note` | `frontend/app.js:1143` | `<div>`(1142 行 `createElement('div')`) | `li`(1128 行 `div.annotation-item`) |
| `.annotation-answer-body` | `frontend/app.js:1156` | `<div>`(1155 行 `createElement('div')`) | `ansEl`(1150 行 `details.annotation-answer`) |
| `.badge-answered` | `frontend/app.js:1165` | `<span>`(1164 行 `createElement('span')`) | `li`(1128 行) |
| `.hint`(静态) | `frontend/index.html:98,110,115,127,138,144,150,175` | 全部 `<p class="hint">` | 各种容器,**无一是 `<button>`** |
| `#abort-inline-hint` | `frontend/index.html:60` | `<span id="abort-inline-hint">` —— **无 class**,`hint` 只出现在 id 里 | `div.panel-header-right` |

补充机械核实:`grep -n 'className' frontend/app.js` 的 20 处赋值与 `grep -n 'classList' frontend/app.js` 的全部调用中,没有任何一处把上述 muted-text 类加到 `<button>` 上。

**结论:D-16 成立** —— 不存在任何 muted-text 类元素落在 `<button>` 内部,与 UI-SPEC `### Pairs deliberately NOT in the manifest` 第 1 行及 `## UI Considerations` 的记载一致。`PAIR --color-text-muted ON --color-surface-hover` **不进清单**,清单为 **43 对**(34 TEXT + 9 NON-TEXT)+ 1 ORDER;`--color-surface-hover` 继续与 `--color-sunken` 共享 `--radix-gray-3`(04.1-N-4)。

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] 更新 `--shadow-overlay` 紧邻的分节注释**

- **Found during:** Task 3(新增 `--shadow-overlay` 时)
- **Issue:** 该分节注释原文是「Tier 2 — overlay backdrop and the **single** shadow token (composer, three layers)」。Task 3 新增第二个 shadow 令牌后,`single` 变成假陈述 —— 正是 04.1-N-8 立的规矩(「一条对代码说谎的注释」不得留下)所要禁止的。Task 2 是注释任务的窗口,但 Task 2 执行时该令牌尚不存在,写「两个 shadow 令牌」会是一个**提前**的假陈述;该注释只有在 Task 3 落地后才需要改。
- **Fix:** 在 Task 3 内把该注释改为「the shadow tokens(composer: three layers; overlay: the modal card's elevation, restored by R-2 so that no bare rgba() appears outside the fence)」,与该声明在同一次提交内落地。
- **Files modified:** `frontend/style.css`
- **Verification:** 纯注释改动;Task 3 全部静态门与运行时门重跑后仍全绿;`grep -c '/\* PAIR '` 仍 43、`/\* ORDER '` 仍 1。
- **Committed in:** `00c6073` (Task 3 commit)

---

**Total deviations:** 1 auto-fixed (1 missing critical)
**Impact on plan:** 无范围蔓延。该修正是 Hard Rule 5 的注释面必然要求(令牌与注释同提交),不改变任何声明、不改变任何渲染。

## Issues Encountered

**1. `--item smoke,1,6` 首次运行 `item 6` 报 BLOCKED(测试假象,非缺陷)。**

首次运行时 `item 6` 在第一条断言就 BLOCKED:「批注条目未渲染(locate_quote 或列表渲染环节卡住)」,退出码 2。按「先怀疑自己的探针」逐项排查:

- 在 `e530ead`(本计划动手前的 pristine HEAD)建临时 worktree 复跑 → `item 6` **PASS**。
- 但该次基线复跑暴露了一个混淆源:端口 8765 上有一个**本会话之前**就存在的陈旧 uvicorn(PID 57542,11:58pm 起,根在主仓库),harness 按设计复用它,故静态资源实际由主仓库提供。
- 在主仓库原样重跑 `--item smoke,1,6` → **exit=0,item smoke / 1 / 6 三项结论列全 PASS**。

**判定:首次 BLOCKED 是 harness 的时序竞态(渲染完成前查询 DOM),不是本计划引入的回归。** 本计划只改 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`,而 `item 6` 的阻塞点是 `!!document.querySelector('#annotation-list .annotation-item')` 这个 **DOM 存在性**判据,发生在任何样式读取之前,不可能被值层改动影响。与既有记忆「键盘选区无法自动化,别把测试假象当缺陷」同源。

**2. 计划的工作树范围门列出三个 `.planning/*` 文件(动手前既有状态)。**

Task 3 的门 `git diff --name-only HEAD -- . ':!.claude/settings.local.json'` 除两个预期文件外还列出 `.planning/STATE.md` / `.planning/config.json` / `.planning/state.json`。核实:这三者在**本计划动手之前**就已是 `M`(会话起始 git status 已记录;其 diff 内容是编排器写入的 `current_phase_name: Radix 颜色族重写 (INSERTED)` / `last_activity_desc: Phase idi-04.1 execution started` / `state_head: e530ead`,时间戳 12:36:27,早于本执行器 12:37:34 的启动)。它们与计划刻意排除的 `.claude/settings.local.json` 属同一类「非本计划产出、不得由本计划提交」的既存工作树状态。

**本计划的实际改动面严格等于 `frontend/style.css` + `scripts/check-05-ui-uat.py`**(见 Task 3 commit `00c6073` 的 `--numstat`:`frontend/style.css` 与 `scripts/check-05-ui-uat.py` 两个文件)。未把任何 `.planning/*` 或 `.claude/*` 文件纳入本计划的任何一次提交。

## Verification Evidence

| 门 | 命令 | 结果 |
|---|---|---|
| 仲裁者 | `python3 scripts/check-02-contrast.py` | `PASS: 0 failures`;43 行 `PASS  ` / 0 行 `FAIL`;`ORDER 0.363` 恰 1 行 |
| CHECK-01 | `bash scripts/check-01-token-conformance.sh` | `PASS`(围栏外裸 hex 计数 0) |
| CHECK-03 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` |
| CHECK-04 | `bash scripts/check-04-important-count.sh` | `PASS` |
| 围栏结构 | `awk` 计数 | tier-1 = 25、`--color-*` = 47、`/* PAIR ` = 43、`/* ORDER ` = 1 |
| Gate 2(双向) | `comm -23`(两个方向) | 两向皆空:无未解析 `var()`,亦无零消费者声明 |
| 运行时 | `.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,6` | `exit=0`;`item smoke: PASS (6 条断言)` / `item 1: PASS (45 条)` / `item 6: PASS (2 条)` |
| 语法 | `node --check frontend/app.js` | OK |
| 回归 | `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped`(基线不变) |
| 零改动面 | `git diff --name-only HEAD -- frontend/app.js frontend/index.html` | 空 |
| vendor | `ls frontend/vendor/` | `marked.min.js`(唯一文件) |
| 未跟踪 | `git ls-files --others --exclude-standard frontend/` | 空 |

## User Setup Required

None - no external service configuration required.

## Known Stubs

None. 本计划不新增任何 UI 数据源或占位文案;它是单文件 CSS 值层重写加一个只读测试脚本的断言追加。

## Threat Flags

None. 未引入计划 `<threat_model>` 之外的任何新面 —— 无网络端点、无认证路径、无输入解析、无新文件、无新依赖。`--shadow-overlay` 与全部 Radix hex 只流向 `background` / `color` / `border-*` / `box-shadow`;本计划未新增任何 `url()` / `content:` 汇点。

## Next Phase Readiness

- **Plan 02(wave 2)就绪**:它依赖本计划以加固 `check-01-token-conformance.sh:37-39` 的 tier-1 名守卫 —— 该正则的交替式(`white|black|gray|green|blue|amber|red|purple`)在 `--radix-*` 改名后**不再匹配** `var(--radix-…`,TOKEN-02 的守卫目前静默空转而仍打印 `PASS`(T-idi041-03)。本计划已用「围栏外 `comm -23` 未解析 var() 为空」+ 逐条人工复核作为过渡证据,但守卫本身的加固与变异证明在 Plan 02。
- **Plan 03(wave 3)就绪**:`scripts/check-05-ui-uat.py` 的其余硬编码 rgb 断言(D-14)与完整携带项 #9 运行时清单(`.hint` / `#btn-authorize` / `#ai-route-select` / `#selection-menu` / `.kind-write .event-kind` 等)由它收口。本计划已把 `rgba(0, 0, 0, 0.2)` 的计数不变量守住(== 1),wave 3 的「全文件唯一颜色字面」门不会因本计划变红。
- **Phase 7 的注意项(沿自 UI-SPEC 携带项 #8)**:焦点环 `--color-focus: #1f63bd` 必须针对**新的**底色重测(`--color-surface` `#f9f9f9`、`--color-surface-page` `#fcfcfc`),不能再对着旧的 `#fafafa`。
- **留给 verify-work 的人工项**:UI-SPEC 的 28 条 backstop(overflow / long-text 文本适配)未由本计划验证 —— 见 coverage `D6`,已显式标为 `human_judgment: true`,不得静默通过。

## Self-Check: PASSED

---
*Phase: idi-04.1-radix*
*Completed: 2026-09-19*
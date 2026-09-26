---
phase: idi-04.1-radix
plan: 03
subsystem: ui
tags: [playwright, computed-style, design-tokens, token-wiring, wcag-contrast, uat, d14]

# Dependency graph
requires:
  - phase: idi-04.1-radix
    provides: 围栏值层 Radix 重写(47 个 `--color-*`)、R-1/R-2/R-3 三处围栏外声明、`resolve_token(page, name)` 助手、`item_smoke` 的三条令牌接线范本
  - phase: idi-04-tokens-contract
    provides: idi-04-UAT.md 的 6 项与 `## Gaps` 的单条根因、四条守卫命令、CHECK-02 仲裁脚本
provides:
  - "`scripts/check-05-ui-uat.py` 的颜色断言全部改为令牌接线形式(D-14):item2/item3/item4/item5 的期望侧来自运行时解析的 `--token`,`FROZEN_AMBER` 常量删除"
  - "携带项 #9 具名运行时清单的其余六组落到 item3 / item4 / item5(01 覆盖 `.overlay-card` box-shadow / `.tier-desc` opacity / `#state-badge` z-index 三条)"
  - "`#doc-pane` → `#doc-panel-body`(D-13),item 4 由 BLOCKED 转 PASS 且 0 BLOCKED"
  - "D-12 的七条间距/字号漂移以更新期望值的方式接受 HEAD 现状"
  - "`idi-04-UAT.md` 六项全 `pass`、三条 gap 标为已消解、AA 倒退记为已修复(5.62:1)"
  - "C-1 下游门引用复核留证:实测 16px / `#4f3422`,五个 ROADMAP 站点逐点枚举(内容锚,非行号锚)"
affects: [phase-5-visual, phase-6, phase-7-focus-ring, verify-work]

actuals:
  tokens: 13258     # chars/4 over the realized diff (53033 chars) — same scale as the plan's estimate.tokens
  tasks: 3
  commits: 3        # MEASURED: git rev-list --count a506ba6..HEAD
  plan_head_before: a506ba6387acbef833b35296592747c12ea85154

tech-stack:
  added: []
  patterns:
    - "令牌接线断言:期望侧 = 运行时解析出的 `--token`,消费者侧 = computed style;值层再改不产生假 FAIL"
    - "两个解析助手分工:`resolve_color` 挂探针元素读 `color`(颜色专用),`resolve_token` 读 `documentElement` 的 `getPropertyValue`(数字/多段值)"
    - "检测力损失的补偿:每条接线断言旁的 `info()` 打印解析值,值的仲裁交给独立的 check-02"

key-files:
  created: []
  modified:
    - scripts/check-05-ui-uat.py
    - .planning/phases/idi-04-tokens-contract/idi-04-UAT.md

key-decisions:
  - "`#btn-authorize` 的 `color` 接的是 `--color-action-irreversible-fg`(green-12),不是 `--color-action-irreversible`(green-11)—— 按 style.css:928-934 的三条声明逐条对位"
  - "`item3` 的 `.overlay-card` box-shadow 是全文件唯一保留的颜色字面(`rgba(0, 0, 0, 0.2)`,由 R-2 的令牌形状固定),计数不变量 == 1"
  - "`item5` 的 `.hint 实际背景` 接 `--color-surface`(不是 `--color-surface-page`)—— 探针落在 `#doc-panel` 内,其 `background` 是 `var(--color-surface)`"
  - "`item4` 的三条 z-index 走 `resolve_token`,使 `badge < banner` 的承重序关系在渲染层两端都被读到,而不只在围栏注释里被声明"
  - "`idi-04-UAT.md` 的 `## Current Test` 一并更新(原为「awaiting 修复决定」)—— 6 项全 pass 后保留该措辞会让文档自相矛盾"
  - "ROADMAP 的失真引用只复核、只留证,不单方面改写(未来阶段已签核的门,须用户裁决)"

patterns-established:
  - "结构性地移除假 FAIL 的根因:断言改为令牌接线,而非逐条重写字面期望值"
  - "枚举基准是内容不是行号:站点按「同一行同时含选择器与旧值」识别,行号只作复核当时的定位辅助"

requirements-completed: [A11Y-04, A11Y-04b, TOKEN-07, CHECK-02, CHECK-03, CHECK-04]

coverage:
  - id: D1
    description: "item2(item2 + check_frozen_marker)与 item3 的 15 条断言期望侧全部改为运行时令牌解析,模块常量 FROZEN_AMBER 与三处字面串删除"
    requirement: "A11Y-04"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 2,3 (exit=0;item 2 PASS 5/0/0,item 3 PASS 15/0/0)"
        status: pass
    human_judgment: false
  - id: D2
    description: "item4 / item5 的期望侧改为令牌接线,z-index 三条走 resolve_token(TOKEN-07 在渲染层的证据)"
    requirement: "TOKEN-07"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 4,5 (item 4 PASS 24/0/0;item 5 BLOCKED 9 条 0 FAIL 2 BLOCKED;exit=2 设计使然)"
        status: pass
    human_judgment: false
  - id: D3
    description: "D-13:`#doc-pane` 的 BLOCKED 块改为 `#doc-panel-body` 的 ok 断言(期望 32px 40px),item 4 转为 0 BLOCKED"
    requirement: "CHECK-03"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 4 (item 4: PASS,0 FAIL,0 BLOCKED)"
        status: pass
    human_judgment: false
  - id: D4
    description: "idi-04-UAT.md 六项全 pass、三条 gap 标为已消解、AA 倒退记为已修复(--color-text-muted #646464 在 #f9f9f9 上 5.62:1)"
    requirement: "A11Y-04b"
    verification:
      - kind: unit
        ref: "grep gates on .planning/phases/idi-04-tokens-contract/idi-04-UAT.md (result: [pass] = 6,[fail] = 0,expected:#doc-panel-body = 1,expected:#doc-pane = 0)"
        status: pass
      - kind: unit
        ref: "python3 scripts/check-02-contrast.py (末行 PASS: 0 failures,43 对 + ORDER 0.363)"
        status: pass
    human_judgment: false
  - id: D5
    description: "C-1 的下游门引用复核:实测 #brainstorm-view h2 = 16px / #4f3422,五个 ROADMAP 站点逐点留证(内容锚),一行式修正建议已给出"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 4 (#brainstorm-view h2 font-size=16px 与 color == --color-action-warning 两条断言 PASS)"
        status: pass
      - kind: unit
        ref: "grep -cE '#brainstorm-view h2.*8a6508' .planning/ROADMAP.md (= 5,内容锚未失效)"
        status: pass
    human_judgment: false
  - id: D6
    description: "携带项 #8(Phase 7 焦点环重测义务)与 D-15 的三数差异(24 / 34 / 43)在 ## Carry-Forward 留档"
    verification:
      - kind: unit
        ref: "grep -c 'Carry-Forward' idi-04-UAT.md (= 1,含 ①C-1 ②携带项 #8 ③D-15 ④收口证据)"
        status: pass
    human_judgment: false
  - id: D7
    description: "ROADMAP.md §Phase 6 SC5 等五处失真引用(14px / #8a6508)的**裁决** —— 改或不改"
    verification: []
    human_judgment: true
    rationale: "那是未来阶段已签核的门,改写它属于本阶段范围外(plan prohibition 明写「不得单方面改写 ROADMAP.md §Phase 6 SC5 的验收判据 —— 只记录、交用户裁决」)。本阶段只交付复核与留证(D5),修正与否必须由用户决定。一行式建议已备:14px → 16px;#8a6508 → #4f3422。"

# Metrics
duration: 41min
completed: 2026-09-19
status: complete
---

# Phase 04.1 Plan 03: UAT 断言令牌接线化 + UAT 文档消解 Summary

**`scripts/check-05-ui-uat.py` 的全部颜色断言改为令牌接线形式(D-14),`FROZEN_AMBER` 删除、`#doc-pane` → `#doc-panel-body`;全量 harness 由「20 条假 FAIL」变为 0 FAIL(item 1/2/3/4/6 全 PASS 0 BLOCKED,item 5 仅剩两条按设计记 BLOCKED 的交互冒烟,exit=2);`idi-04-UAT.md` 六项全 pass、三条 gap 消解、AA 倒退记为已修复,并补上 C-1 下游门复核与携带项 #8 的留档。**

## Performance

- **Duration:** 41 min
- **Started:** 2026-09-19T13:05:00Z
- **Completed:** 2026-09-19T13:46:00Z
- **Tasks:** 3 / 3
- **Files modified:** 2

## Accomplishments

- **根因被结构性移除。** 20 条假 FAIL 的单条根因是「UAT 期望值定稿于值层改动之前」;本计划把断言改成令牌接线,值层再改不产生假 FAIL —— 逐条重写字面值是治标。
- **`FROZEN_AMBER` 及三处字面串删除**,冻结轮琥珀色改由 `resolve_color(page, "--color-action-warning")` 在运行时解析;冻结轮的 `opacity: 1` / `filter: saturate(0.6)` 两条仍以字面断言(它们不是颜色令牌)。
- **携带项 #9 的具名运行时清单补齐。** 01 覆盖 `.overlay-card` box-shadow / `.tier-desc` opacity / `#state-badge` z-index 三条;本计划覆盖其余六组:`.hint` color、`.badge-answered` color、`#btn-authorize` color/border/background、`.kind-write .event-kind` background、`#ai-route-select` 与 `#selection-menu` border-top-color(外加 `.chat-user` background、`#state-badge` color/background)。
- **D-13 落地:** `#doc-pane` 那条 BLOCKED 改为 `#doc-panel-body` 的 `ok` 断言,期望 `32px 40px` 实测一致 → `item 4` 由「14 PASS / 9 FAIL / 1 BLOCKED」变为 **24 PASS / 0 FAIL / 0 BLOCKED**。改的是期望字符串,`app.js` 的约 70 个顶层 `getElementById` id 一字未动。
- **D-12 落地:** 七条间距/字号漂移以更新期望值接受 HEAD 现状(`frontend/style.css` 一字未动)。
- **TOKEN-07 获得渲染层证据:** 三条 z-index 走 `resolve_token`,`badge(10) < banner(20)` 的承重序关系两端都在真实 DOM 上被读到。
- **`idi-04-UAT.md` 收口:** 六项 `result: [pass]`、三条 gap 标为 `resolved`(原始 `observed`/`failing` 保留为历史对照)、AA 倒退改写为已修复(`#646464` 在 `#f9f9f9` 上 5.62:1)。
- **C-1 复核留证:** `#brainstorm-view h2` 实测 16px / `#4f3422`,与 ROADMAP 五处及 `04-UI-SPEC.md` 携带项 #7 所写的 `14px` / `#8a6508` 全部不符;五站点逐点留证(内容锚),一行式修正建议已给,但**不改写未来阶段已签核的门**。

## Task Commits

Each task was committed atomically:

1. **Task 1: item2/item3 断言改令牌接线,删除 FROZEN_AMBER 常量** - `e93c97f` (refactor)
2. **Task 2: item4/item5 令牌接线 + D-13 选择器改名 + D-12 期望值更新** - `68309d0` (refactor)
3. **Task 3: UAT 按 D-10/D-12/D-13 更新 + C-1 下游门复核 + 携带项 #8** - `a5e0b07` (docs)

**Plan metadata:** (docs: complete plan — 本 SUMMARY 的提交)

## Files Created/Modified

- `scripts/check-05-ui-uat.py` - item2/item3/item4/item5 的期望侧改为运行时令牌解析;`FROZEN_AMBER` 与三处字面串删除;`#doc-pane` → `#doc-panel-body`;七条期望值按 D-12 更新;三条 z-index 走 `resolve_token`;每条接线断言旁加 `info()`(+299 / −163 跨两次提交)
- `.planning/phases/idi-04-tokens-contract/idi-04-UAT.md` - 六项 evidence 更新为本阶段实跑输出;三条 gap 标为 resolved;AA 倒退改写为已修复;新增 `## Carry-Forward` 四节(C-1 复核 / 携带项 #8 / D-15 三数差异 / 收口证据表)

## Decisions Made

- **`#btn-authorize` 的 `color` 接 `--color-action-irreversible-fg`,不是 `--color-action-irreversible`。** 按 `frontend/style.css:928-934` 的三条声明逐条对位:`color` → `-fg`(green-12)、`border-color` → 无后缀(green-11)、`background` → `-surface`(green-3)。计划原文把 color 与 border-color 都写成同一个令牌,那会让该断言永远失败 —— 这是接线错误,不是产品缺陷(见 Deviations)。
- **box-shadow 的 needle 保持字面。** `rgba(0, 0, 0, 0.2)` 不是颜色令牌,它的形状由 R-2 的 `--shadow-overlay` 固定;`grep -c 'rgba(0, 0, 0, 0.2)'` == 1 是本计划守住的计数不变量(`item_smoke` 用的是短 needle `"0.2"`,不冲突)。
- **`.hint 实际背景` 接 `--color-surface`。** 探针命中的 `.hint` 落在 `#doc-panel` 内,而 `#doc-panel { background: var(--color-surface) }` —— 接成 `--color-surface-page` 会让该断言永远失败(两者在 04.1 之后是 `#f9f9f9` / `#fcfcfc`)。
- **`## Current Test` 一并更新。** 该节原写「awaiting:修复决定」;六项全 pass 后保留它会让文档与 `## Summary` 自相矛盾。改为 `number: 6` / `awaiting: 无`。
- **ROADMAP 的失真引用只复核、不改写。** 计划 prohibition 明写这是未来阶段已签核的门;修正建议以一行式给出,裁决权留给用户(见 coverage D7)。

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] `#btn-authorize` 的 `color` 接错了令牌**

- **Found during:** Task 1(`--item 2,3` 首次运行)
- **Issue:** 计划 Task 1 步骤 2 写「`[p3] #btn-authorize color` 与 `border-color` → `resolve_color(page, "--color-action-irreversible")`」。实测该断言 FAIL:`--color-action-irreversible` 解析为 `rgb(33, 131, 88)`(green-11),而 `#btn-authorize` 的 computed `color` 是 `rgb(25, 59, 45)`(green-12)。查 `frontend/style.css:928-934`:`color: var(--color-action-irreversible-fg)`,而 `--color-action-irreversible-fg: var(--radix-green-12)`。按计划原文接线,该断言**永远无法通过**。
- **Fix:** `color` 的期望侧改为 `resolve_color(page, "--color-action-irreversible-fg")`;`border-color` 保持 `--color-action-irreversible`。并在代码里加注释点明三条声明的逐条对位。
- **Files modified:** `scripts/check-05-ui-uat.py`
- **Verification:** `.venv/bin/python scripts/check-05-ui-uat.py --item 2,3` → `exit=0`,item 2 与 item 3 均 `PASS`(15 条断言 0 FAIL 0 BLOCKED)。该 token 对是 UI-SPEC 的 `PAIR --color-action-irreversible-fg ON --color-action-irreversible-surface TEXT`(11.00 ✓),产品侧无缺陷。
- **Committed in:** `e93c97f` (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** 无范围蔓延。修的是计划里的一处令牌对位错误 —— 若照抄,本计划的核心门(item 3 全 PASS)不可能通过,而执行器可能转而怀疑产品。`frontend/style.css` 一字未动。

## Issues Encountered

**1. 我自己的探针一度误报「计划的 `#doc-pane\b` 门不可满足」(探针故障,非计划缺陷)。**

计划 Task 2 的负向门是 `grep -cE 'read_style\(page, .#doc-pane\b'` == 0,而 `doc-pane` 是 `doc-panel-body` 的子串,我据此怀疑该门会把**正确**的那一行也算进去,与「`read_style(page, "#doc-panel-body")` 计数 ≥ 1」互斥。

第一次探针把两行(`#doc-panel-body` 与 `#doc-pane`)**同时**写进一个文件再计数,得到 1,我把它误读成「命中了正确的那一行」。**逐行隔离后结论相反**:本机 `grep` 是 ugrep 7.8.4,它把 `-` 当作词字符,故 `#doc-pane\b` **不**匹配 `#doc-panel-body`(该行计数 0),只匹配真正的 `#doc-pane`(计数 1)。计划的门是正确的、可满足的,无需修正。

**教训与既有记忆「先怀疑自己的探针」同源:报门失败之前,逐字复现那条门命令,并且一次只放一个变量。** 我差一点就把一个不存在的「计划缺陷」写进 SUMMARY。

**2. 计划的工作树范围门会列出既存的 `.planning/config.json`。**

`git diff --name-only HEAD -- . ':!.claude/settings.local.json'` 在 Task 1 / 2 的门里会列出 `.planning/config.json`。核实:该文件在**本计划动手之前**就已是 `M`(会话起始 git status 已记录,内容是编排器写入的配置变更)。它与计划刻意排除的 `.claude/settings.local.json` 属同一类「非本计划产出、不得由本计划提交」的既存工作树状态。

**本计划的实际改动面严格等于 `scripts/check-05-ui-uat.py` + `.planning/phases/idi-04-tokens-contract/idi-04-UAT.md` 两个文件**(见两次 refactor 提交与一次 docs 提交的 `--numstat`)。未把任何既存的 `.planning/*` 或 `.claude/*` 改动纳入本计划的任何一次提交。

## Verification Evidence

| 门 | 命令 | 结果 |
|---|---|---|
| 全量 harness | `.venv/bin/python scripts/check-05-ui-uat.py` | **0 FAIL**;`item 1`(45 条)/`2`(5)/`3`(15)/`4`(24)/`6`(2)全 `PASS` 且 0 BLOCKED;`item 5` 为 `BLOCKED`(9 条,0 FAIL,2 BLOCKED)且其 2 条 BLOCKED 恰为已记录的两条交互冒烟;退出码 **2**(不带 `--ai-smoke` 时 0 BLOCKED 不可达,`idi-04-UAT.md:262` 已逐字记明) |
| 切片(含 01 的三条) | `.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,6` | 退出码 **0**;`smoke`(6 条)/`1`(45 条)/`6`(2 条)三项结论列全 `PASS` |
| 值的仲裁者 | `python3 scripts/check-02-contrast.py` | 末行 `PASS: 0 failures`;43 对 + `ORDER 0.363` |
| CHECK-01 | `bash scripts/check-01-token-conformance.sh` | `PASS` |
| CHECK-03 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` |
| CHECK-04 | `bash scripts/check-04-important-count.sh` | `PASS` |
| 回归 | `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped`(基线不变) |
| 语法 | `node --check frontend/app.js` | OK |
| 零改动面 | `git status --porcelain -- frontend/ .planning/ROADMAP.md` | 空 |
| vendor | `ls frontend/vendor/` | `marked.min.js`(唯一文件) |
| D-14 不变量 | `grep -c 'FROZEN_AMBER'` / `grep -c 'rgba(0, 0, 0, 0.2)'` | `0` / `1`(后者是全文件唯一保留的颜色字面) |
| D-13 门 | `grep -cE 'read_style\(page, .#doc-pane\b'` / `...#doc-panel-body\b` | `0` / `1` |
| D-14 铺开度 | `item3` / `item4` / `item5` 的 `resolve_color` 计数 | `12` / `2` / `6`;`item4` 另有 `resolve_token` `3` |
| UAT 计数门 | `result: [pass]` / `[fail]` / `expected:.*#doc-panel-body` / `expected:.*#doc-pane\b` | `6` / `0` / `1` / `0` |
| C-1 内容锚 | `grep -cE '#brainstorm-view h2.*8a6508' .planning/ROADMAP.md` | `5`(枚举基准未失效) |

## User Setup Required

None - no external service configuration required.

## Known Stubs

None. 本计划不新增任何 UI 数据源或占位文案;它只改一个只读测试脚本的断言表述与一份 UAT 文档。

## Threat Flags

None. 未引入计划 `<threat_model>` 之外的任何新面 —— 无网络端点、无认证路径、无输入解析、无新文件、无新依赖。T-idi041-09(「运行时验证被断言而非执行」)的缓解已按计划落地:全量 harness 0 FAIL,`item 4` 的 `#doc-pane` 项由 BLOCKED 转 ok,剩余的 2 条 BLOCKED **恰为**已记录的两条交互冒烟,未被任何手段「变绿」。

## Next Phase Readiness

- **本阶段(idi-04.1-radix)三波全部完成。** wave 1 值层重写、wave 2 守卫加固、wave 3 断言接线与 UAT 消解。
- **交给 verify-work 的人工项:**
  - coverage **D7** —— ROADMAP 五处 + `04-UI-SPEC.md` 携带项 #7 的失真引用(`14px` / `#8a6508`)是否照一行式建议改为 `16px` / `#4f3422`。**这是用户的裁决,不是执行器的。**
  - **携带项 #8** —— Phase 7 必须在 `--color-surface` `#f9f9f9` 与 `--color-surface-page` `#fcfcfc` 上重测焦点环 `--color-focus: #1f63bd` ≥ 3:1。
- **本阶段遗留的真实限制:** 键盘文本选区在本机无法自动化(见 `scripts/check-05-ui-uat.py` 头部与 `idi-04-UAT.md`);UI-SPEC 的 28 条 backstop 仍未由自动化确认(沿自 wave 1 的 coverage D6)。
- **`--item 5 --ai-smoke`** 仍是补齐两条交互冒烟证据的唯一手段(会产生真实 AI 调用与计费)。

## Self-Check: PASSED

---
*Phase: idi-04.1-radix*
*Completed: 2026-09-19*
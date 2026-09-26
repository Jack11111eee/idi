---
phase: 260926-vaf-card-border-shadow-strength
plan: 01
subsystem: ui
tags: [css, design-tokens, card-language, box-shadow, border-color, computed-style, playwright, guard-first, value-level-change]

# Dependency graph
requires:
  - phase: idi-09-card-containers
    provides: 卡片语言(白底 + 四边 1px 边界 + --radius-md + 零位移 --shadow-card)与 check-09 的 c1/c2 运行时判据;本次是 Phase 9 自己 parked 的「强度刻度」决策的落地
provides:
  - 两条卡片规则(#main-pane > section / #doc-panel)的边界令牌由 --color-border-subtle(gray-6)换到 --color-border(gray-7)
  - --shadow-card 由单层 0 1px 2px rgba(0,0,0,0.04) 改为两层 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04)
  - scripts/probe-card-border-token.py —— 卡片容器 border-*-color 的运行时探针(既有六条门的零覆盖缝)
  - check-09 的两个阴影常量与 shadow_lengths docstring 重新登记到新裁定值
affects: [idi-09-VERIFICATION.md, 视觉构图后续候选]

# Actuals (#2632) — pairs with the plan's `estimate` (30000 tokens / 2 tasks) to calibrate future estimates.
# Same estimateTokens scale (chars/4 over files actually changed), never a harness token count.
actuals:
  tokens: 27956
  tasks: 2
  commits: 2
  plan_head_before: 6e2b16b5b212af90e8e0b54738a2955a1940699b

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "守卫先行(guard-first):先写运行时探针并看它 RED,再动值 —— 本项目口径「你没见它红过的守卫不是守卫」"
    - "期望侧取字面量而非同一令牌:改坏令牌值时断言仍能红(check-09 的 SHADOW_CARD_LITERAL)"
    - "计数门是 scope-blind 的:grep -c 数的是行,不是声明/断言,注释散文与汇总行都会把计数顶高"

key-files:
  created:
    - scripts/probe-card-border-token.py
  modified:
    - frontend/style.css
    - scripts/check-09-idi09-validation.py

key-decisions:
  - "边界换令牌而非改值:--color-border(gray-7)已是既有令牌,零新增令牌、零 tier-1 原语改动(禁改颜色值)"
  - "SHADOW_CARD_COLOR 取主层 0.08 而非次层 0.04:两条子串断言取主层才能让「主层确实加深了」被断言到;取次层旧色会被次层蒙过去(已由中间态 RED 实证:常量未更新时该条仍 PASS)"
  - "两层阴影不打破零位移判据:check-09 只比 lengths[0],实测 lengths=['0px','1px','3px','0px,','0px','1px','2px','0px'] ⇒ 首层 offset-x 仍 0px"
  - "新写探针而非往 check-09 加断言:后者是改门语义,而本次裁定是纯值级修正(本仓库把门改动当高代价事件)"
  - "四处非卡片消费者一字不动:用户裁定是「卡片边框与阴影加重一档」,不是「全站边界加深」"

patterns-established:
  - "值级改动的完整闭环:探针(新缝)+ 既有门(回归)+ 常量重新登记(期望侧)+ 散文同步(注释/docstring)"
  - "六处逐字相同的声明里只改两处的定位法:带上下文行的锚点,改完用计数核盘(六处总数不变)"

requirements-completed: [CARD-01, CARD-02, D-9-3]

# Coverage metadata (#1602) — drives deterministic UAT routing in verify-work.
coverage:
  - id: D1
    description: "两条卡片规则(#main-pane > section / #doc-panel)在真实浏览器里计算 border-top-color == rgb(206, 206, 206)(--color-border / gray-7)"
    requirement: "CARD-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/probe-card-border-token.py (exit=0, 5 行 PASS 卡片边界)"
        status: pass
    human_judgment: false
  - id: D2
    description: "卡片计算 box-shadow 首层为 rgba(0, 0, 0, 0.08) 且首层 offset-x 仍为 0px;check-09 c1/c2 零回归"
    requirement: "CARD-02"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2 (exit=0, 26+13 条断言, 0 FAIL, 0 BLOCKED)"
        status: pass
    human_judgment: false
  - id: D3
    description: "四处非卡片 --color-border-subtle 消费者(.event-list / .annotation-item / .badge-answered / #latest-check)仍计算为 gray-6 —— 改动面严格是两处"
    verification:
      - kind: automated_ui
        ref: "scripts/probe-card-border-token.py 的非卡片对照(2/4 在 p1 样本可读,均 PASS)+ grep 计数(--color-border-subtle 仍 4 处)"
        status: pass
    human_judgment: false
  - id: D4
    description: "新增守卫 scripts/probe-card-border-token.py 本身:改动前 RED、改动后 GREEN,证明它区分得开「改了」与「没改」"
    verification:
      - kind: automated_ui
        ref: "/tmp/vaf-probe-red.txt (exit=1, 5 行 FAIL 卡片边界 actual=rgb(217, 217, 217)) vs /tmp/vaf-probe-green.txt (exit=0)"
        status: pass
    human_judgment: false
  - id: D5
    description: "强度「稍微重一点」是否到位 —— 这是用户的感知裁定,自动化只能证明值按裁定落了地"
    requirement: "D-9-3"
    verification: []
    human_judgment: true
    rationale: "「太轻了,稍微重一点」是感知阈值判断,只有用户的眼能裁;自动化能证明的是新值被真实渲染(getComputedStyle)且零回归,不能证明「这一档恰好合适」。截图见 /tmp/vaf-screenshots/(p1/p12/p3/checking/archive,1440×900)"

# Metrics
duration: ~20min
completed: 2026-09-26
status: complete
---

# Quick 260926-vaf: 卡片边框与阴影强度加重一档 Summary

**两条卡片规则的边界令牌由 gray-6 换到 gray-7(--color-border),`--shadow-card` 由单层 `0 1px 2px rgba(0,0,0,0.04)` 改为两层 `0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04)` —— 四个值级改动,零新增令牌/规则/选择器,并补上一条此前零覆盖的运行时守卫。**

## Performance

- **Duration:** ~20 min
- **Started:** 2026-09-26T22:40 (plan 提交时刻,`6e2b16b`)
- **Completed:** 2026-09-26T22:58 (+08:00)
- **Tasks:** 2
- **Files modified:** 3 (2 modified + 1 created)

## Accomplishments

- **四处值改动全部落地且改动面可机械核盘**:`border: 1px solid var(--color-border);` 由 1 处变为 3 处(+2,`#main-pane > section` 与 `#doc-panel`);`border: 1px solid var(--color-border-subtle);` 由 6 处降为 4 处 —— 六处总数不变,四处非卡片消费者一字未动。
- **一条此前零覆盖的缝被补上**:既有六条门没有一条读卡片容器的 `border-*-color`(check-09 读的是 width / style / radius / background / box-shadow)。新探针在真实浏览器里读 `getComputedStyle(el)['border-top-color']`,并带一条防恒真的前置判据(两令牌必须可区分)。
- **两条守卫都在改动前真的红过**(本仓库口径:你没见它红过的守卫不是守卫):探针 `exit=1` / 5 行 `FAIL 卡片边界` 且 `actual=rgb(217, 217, 217)`;check-09 的字面量断言在「CSS 已改、常量未更新」的中间态 `exit=1` / 1 行 `FAIL c1 [令牌] --shadow-card`。
- **零回归**:四个静态门全绿(check-02 仍 `PASS: 0 failures`)、check-05/06/07 与 probe-05/07 零新增 FAIL、pytest 仍 `219 passed, 6 skipped`。
- **散文与代码重新一致**:卡片注释第 ① 条改写(删掉已被用户裁定推翻的「不得顺手换成别的令牌」),`shadow_lengths` 的 docstring 按两层值修正。

## Task Commits

Each task was committed atomically:

1. **Task 1: 先把边界色的运行时守卫写出来,并看它红** - `8faa4fe` (test)
2. **Task 2: 四处值改动落地(阴影 + 两条卡片边界 + 常量)并全绿** - `6ce0923` (fix)

**Plan metadata:** 未提交 —— 按派发说明,SUMMARY/STATE/PLAN 等 docs 产物由编排侧统一提交。

## Files Created/Modified

- `scripts/probe-card-border-token.py`(新建)- 一次性探针,复用 check-05 的 `ensure_server` / `make_fixture` / `enter_project` / `read_style` / `resolve_color` / `norm`;不写盘、不进任何 check 的调用链。四条判据:①令牌解析 + 可区分性(防恒真)②五个卡片容器边界色 == `--color-border` ③四个非卡片对照仍 == `--color-border-subtle`(要求至少 2 个可读)④结果行 PASS/FAIL/BLOCKED(exit 0/1/2)。
- `frontend/style.css`(改)- 围栏内 `--shadow-card`(围栏内唯一一处声明)改两层;`#main-pane > section` 与 `#doc-panel` 两条规则体内的边界令牌改 `--color-border`;卡片注释第 ① 条改写。零新增令牌、零新增 hex、零新增规则、零选择器改动。
  **锚点纪律(本仓库已记录的教训)**:以上一律按选择器文本定位,不按行号 —— 注释第 ① 条由 3 行扩为 5 行,其后所有行号**整体下移 2**。改动后的落点:`#main-pane > section` 的 border 在 `:747`、`#doc-panel` 的在 `:765`(改动前分别为 `:745` / `:763`)。
- `scripts/check-09-idi09-validation.py`(改)- `SHADOW_CARD_LITERAL` / `SHADOW_CARD_COLOR` 重新登记到新裁定值 + `shadow_lengths` docstring 两层措辞修正。numstat 10/7;**断言零删除**(`ok|ok_true|blocked` 调用点 33 处不变,`FAIL|assert` 计数 4 不变),阈值与标签一字未动。

## Decisions Made

- **边界换令牌而非改颜色值**:`--color-border` 已是既有令牌(`var(--radix-gray-7)` = `#cecece`),故本次零 tier-1 原语改动、零新增令牌 —— 符合「禁改颜色值」的硬约束。
- **`SHADOW_CARD_COLOR` 取主层 0.08,不取次层 0.04**:两条子串断言(`check-09:161-163` 与 `:214-216`)都在 computed 值上做包含比对。取主层才能让「主层确实加深了」被断言到。这一点由中间态 RED 独立实证 —— 常量未更新时,旧色 `rgba(0, 0, 0, 0.04)` 仍是新 computed 串的子串,那两条断言照样 PASS。
- **两层阴影不打破零位移判据(计划标为最高风险项,实测安全)**:check-09 只比 `lengths[0]`。实测 `lengths=['0px', '1px', '3px', '0px,', '0px', '1px', '2px', '0px']` ⇒ 首层 offset-x 仍 `0px`,五条断言全 PASS。
- **新写探针而非往 check-09 的 c1 加断言**:后者是改门语义(本仓库把门改动当高代价事件,上一阶段以「零处门改动」为交付亮点),而本次裁定是纯值级修正。仓库有现成先例 `scripts/probe-menu-modal-reachability.py`(同为一次性探针)。
- **四处非卡片消费者一字不动**:用户裁定是「卡片边框与阴影加重一档」,不是「全站边界加深」。

## Deviations from Plan

### 计划文本的两处不精确(均已按正确判据执行并留证,不是代码偏离)

**1. [Plan-verify 计数写错] 计划 `<verify>` 断言 `border: 1px solid var(--color-border);` 计数 == 2,实为 3**

- **Found during:** Task 2 核盘
- **Issue:** 该字符串在改动前**已有 1 处**消费者 —— `frontend/style.css:1083` 的 `.markdown-body th, .markdown-body td` 规则。计划只数了「本次要新增的 2 处」,漏了这处既有消费者。
- **Fix:** 按派发说明与 `must_haves` 的**正确判据**执行:**增量 +2**。实测 `1 → 3`(+2 ✓),`--color-border-subtle` `6 → 4`(六处总数不变 ✓)。未改任何代码,只按正确判据核对。
- **Files modified:** 无(纯核盘判据更正)
- **Verification:** `grep -c` 实测 3 / 4,且 `git diff -- frontend/style.css` 逐行确认只有两处 `--color-border-subtle` → `--color-border`(均在卡片规则体内),`:1083` 那处未动。

**2. [Plan-verify 计数写错] 计划 GREEN 预期 `grep -c 'FAIL'` == 0 / `grep -c 'BLOCKED'` == 0,实为 2 / 2**

- **Found during:** Task 2 GREEN 核盘
- **Issue:** 这是本仓库反复踩过的「计数门是 scope-blind 的」同型陷阱 —— `grep -c` 数**行**,而 `=== 逐项结论 ===` 的汇总行 `item c1: PASS (26 条断言,0 FAIL,0 BLOCKED)` 本身就含 `FAIL` 与 `BLOCKED` 子串,两个 item 各贡献 1 行。
- **Fix:** 判据改用 `grep -n 'FAIL' <file> | grep -v '0 FAIL'`(真 FAIL 行)与退出码。实测真 FAIL 行 **0** 行、真 BLOCKED 行 **0** 行、`exit=0`。未改任何代码。
- **Files modified:** 无(纯核盘判据更正)
- **Verification:** `tail -8 /tmp/vaf-c09.txt` 显示 `item c1: PASS (26 条断言,0 FAIL,0 BLOCKED)` / `item c2: PASS (13 条断言,0 FAIL,0 BLOCKED)` / `exit=0`。

### 执行顺序的一处说明(证据等价,非偏离)

计划的 Task 2 要求「在只改完 ①②③、还没动常量时」跑一次 check-09 取中间态 RED。本次的实际次序是:四条改动一并落地 → **把两个常量临时改回旧值** → 跑 check-09 取 RED → 再把常量改回新值。中间态的语义与计划要求的完全一致(CSS 已改、常量未更新),证据等价;取 RED 的临时回退不留痕(最终 `git diff` 只有常量与 docstring 两处)。

### 可选产出落点的一处说明

计划 `<verification>` 第 9 条(明确标注「不参与判据」)给的出图路径是仓库内 quick 目录。本次改出到 `/tmp/vaf-screenshots/`(5 张 1440×900 PNG),理由:截图是二进制产物,而本次派发说明只授权提交代码改动、docs 产物由编排侧统一提交 —— 落在 /tmp 可避免在仓库留下未跟踪的二进制。**逐字复现命令:** `.venv/bin/python scripts/check-09-idi09-validation.py --screenshot /tmp/vaf-screenshots`(若用户希望归档进仓库,改路径即可)。

---

**Total deviations:** 0 auto-fixed(无 Rule 1-4 触发);3 处说明(2 处计划文本计数不精确、1 处执行顺序等价说明、1 处可选产出落点)
**Impact on plan:** 零代码影响。两处计数不精确都是**判据写错而非结论写错** —— 按正确判据(增量 +2 / 真 FAIL 行数)实测全部满足计划意图。改动面、断言集、门语义均与计划逐条一致。

## Issues Encountered

- **服务进程复用**:`ensure_server()` 探测到 8765 已有 uvicorn 在服务,走「复用,不新起、结束时也不关闭」分支(返回 `None`,故探针 `finally` 里的 terminate 是 no-op)。已核实该服务对 `/style.css` 的响应与磁盘**逐字节一致**(改动后复核:卡片两处边界与 `--shadow-card` 的新值均已生效)。此为该端口既有遗留进程,非本次引入。
- **无其它阻塞。**

## Gate Evidence

| 门 | 命令 | 结果 |
|---|---|---|
| check-01 令牌合规 | `bash scripts/check-01-token-conformance.sh` | `PASS` / exit 0(零围栏外裸 hex、零 tier-1 原语引用) |
| check-02 对比度 | `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`(PAIR 清单零改动;两边界令牌都不在清单里) |
| check-03 `.hidden` 唯一性 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` / exit 0 |
| check-04 `!important` 声明数 | `bash scripts/check-04-important-count.sh` | `PASS` / exit 0(声明数 1) |
| check-09 c1/c2(卡片判据) | `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2` | exit 0,`26 + 13` 条断言,**0 FAIL / 0 BLOCKED** |
| check-09 全量(含 c3/c4/c5/shot) | `... --screenshot /tmp/vaf-screenshots` | exit 0,全部 item PASS,0 FAIL / 0 BLOCKED |
| **探针 RED(改动前)** | `.venv/bin/python scripts/probe-card-border-token.py` | **exit 1**,5 行 `FAIL 卡片边界` 全部 `actual=rgb(217, 217, 217)` |
| **check-09 RED(常量未更新的中间态)** | `... --item c1` | **exit 1**,1 行 `FAIL c1 [令牌] --shadow-card` |
| 探针 GREEN | 同 RED 命令 | exit 0,5 行 `PASS 卡片边界`,0 FAIL |
| check-05 全量浏览器 | `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` | exit 2,**0 FAIL**;仅 item 5 的 2 条 `--ai-smoke` 腿 BLOCKED(按设计,与 idi-09-03 基线逐字相同) |
| check-06 / check-07 | 各自直跑 | 各 exit 0,0 FAIL / 0 BLOCKED |
| probe-05 / probe-07 | 各自直跑 | 各 exit 0(probe-05 的 `BLOCKED [mutated] post-fix` 是变异证明的对照支;probe-07 地面仍为卡片白 3.54,与 idi-09 登记一致) |
| pytest 基线 | `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped` |

**零回归的两条重点读数**(阴影属于卡片容器,不该漏到表头):

- `check-05 --item 8`:sticky 断言 `|header.top - panel.top| = 1.000px` **PASS**(余量为零,与 STATE.md 登记的既有开放项逐字相同)。本次只改 `#doc-panel` 边界的**颜色**、未动宽度,故该读数不变 —— 与「任何 1px 级边框改动都会顶破它」的风险登记不冲突。
- `check-09 c2`:`#doc-panel-header` 计算 `box-shadow == none` **PASS**(对照组未受污染)。

## RED 证据原始计数(逐条抄录)

`/tmp/vaf-probe-red.txt`(改动前):

- `exit=1`
- `FAIL 卡片边界` = **5** 行,每行 `actual=rgb(217, 217, 217)`(= `--color-border-subtle`);5 个容器逐个为 `#session-panel` / `#annotations-panel` / `#checks-panel` / `#ai-panel` / `#doc-panel`
- `FAIL 非卡片边界对照` = **0** 行
- `INFO 令牌解析` = **1** 行:`--color-border=rgb(206, 206, 206) --color-border-subtle=rgb(217, 217, 217)`
- `PASS 令牌可区分` = **1** 行
- **非卡片对照命中数:4 个候选里 2 个可读、2 个不存在** ——
  - 可读并 PASS:`.event-list`、`#latest-check`(均 `actual=rgb(217, 217, 217)`)
  - `INFO … 不存在 —— 不计入`:**2** 行(`.annotation-item`、`.badge-answered`;二者由 app.js 在存在批注/已答时动态渲染,p1 样本里没有)

`/tmp/vaf-c09-red.txt`(CSS 已改、常量未更新的中间态):

- `exit=1`
- `FAIL c1 [令牌] --shadow-card` = **1** 行(期望侧旧字面量 `0 1px 2px rgba(0, 0, 0, 0.04)`,实际侧新两层值)
- 同一次运行里 `非 none 且含 rgba(0, 0, 0, 0.04)` 五条**仍 PASS** —— 这正是「`SHADOW_CARD_COLOR` 必须取主层」的实证:旧色仍是新串的子串。

## 两条必须逐条写明的登记

### 登记 1:裁定值变更的溯源(回答了 Phase 9 自己 parked 的问题)

用户 **2026-09-26** 的裁定(逐字):「目前只需要改 2. 边框与阴影强度,现在太轻了,稍微重一点。其他都不需要改。保持原样即可」。

本次把 **D-9-3 的阴影值**从 `0 1px 2px rgba(0, 0, 0, 0.04)` 改为两层值 `0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04)`,并把**卡片边界**从 `--color-border-subtle`(gray-6)改到 `--color-border`(gray-7)。

这条裁定回答的正是 Phase 9 自己刻意 parked 的设计问题 —— `idi-09-03-PLAN.md:301` 与 `idi-09-03-SUMMARY.md:340` 都逐字写着「卡片边界与阴影的**强度**:……是否要更强的边界 = 设计决策,本阶段不动」。本次就是那个决策的落地。

**变更的边界(用户明确排除,不得顺手做)**:`.overlay-card` 底色 / 页面级留白 / 输入框在白卡片上的 UA 白填充 —— 三条仍为开放项,本次零触碰。

### 登记 2:指纹义务与正确闭包

`frontend/style.css` 与 `scripts/check-09-idi09-validation.py` **都在 `.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md` 的 `covered_files` 里** ⇒ 该报告按**内容真变**判 stale(两个文件确实变了字节)。

- **正确闭包 = 重跑 `/gsd-verify-work idi-09`,不是重算 digest。** 重算会把 `covered_digest` 刷成当前值,从而断言「自该验证以来覆盖输入无变化」—— 而这两个文件确实变了,那是不实陈述。
- **不得用 `gsd-tools query verification status <phase>` 判定 stale**(本项目实测:这些相位目录一律返回 `missing`)。
- **重验证时会读到两处与新裁定值的差异,那是用户的裁定、不是回归**:该报告第 10 行的 must-have 与第 157 行的设计说明**逐字钉着旧值**(`--shadow-card` = `0 1px 2px rgba(0, 0, 0, 0.04)`;边界取既有 `--color-border-subtle`(#d9d9d9))。重验证必须按**新裁定值**记录,不得据此判回归。
- **`idi-09-01/02/03-PLAN.md` / `*-SUMMARY.md` / `idi-09-VERIFICATION.md` 零改动** —— 它们是「当时验证了什么」的历史记录,改写会让记录失真。登记写在本 SUMMARY 里。

## Known Stubs

None —— 本次是纯值级改动,无占位符、无硬编码空值、无未接线数据源。

## Threat Flags

None —— 未引入新的信任边界:零新增端点、零新增输入解析面、零新增依赖、零新增 DOM 属性写入、零新增令牌、零新增选择器。

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **本次交付是值级的,Phase 9 的收口状态不变**:不跑 `phase.complete`、不跑 `advance-plan`(本项目已登记:这两个动词会翻掉不归它管的需求并改写被覆盖文件,把刚过的门自己打破)。
- **待用户看效果裁定**:新增强度是否到位(D5,`human_judgment: true`)。截图在 `/tmp/vaf-screenshots/`(5 张 1440×900),或直接看 8765 上的运行实例。
- **待闭合的指纹**:`idi-09-VERIFICATION.md` 因本次改动 stale,正确闭包是重跑 `/gsd-verify-work idi-09`(见登记 2)。
- **本次未触碰的三条开放项仍在**:`.overlay-card` 底色 / 页面级留白 / 输入框 UA 白填充。

---

*Quick: 260926-vaf-card-border-shadow-strength*
*Completed: 2026-09-26*

## Self-Check: PASSED

- FOUND: `scripts/probe-card-border-token.py`
- FOUND: `frontend/style.css`
- FOUND: `scripts/check-09-idi09-validation.py`
- FOUND: `.planning/quick/260926-vaf-card-border-shadow-strength/260926-vaf-SUMMARY.md`
- FOUND: `8faa4fe`(Task 1)
- FOUND: `6ce0923`(Task 2)
- 工作树:代码改动全部已提交;唯一未跟踪文件是本 SUMMARY(按派发说明由编排侧统一提交)

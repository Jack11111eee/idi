---
phase: idi-04.1-radix
plan: 04
subsystem: scripts
tags: [guard-hardening, mutation-testing, ui-uat-harness, token-wiring, vacuous-guard, cr-01]

# Dependency graph
requires:
  - phase: idi-04.1-radix
    plan: 03
    provides: "D-14 落地:22 条硬编码 rgb(...) 断言改为 `resolve_color` 令牌接线 + item4/item5 令牌化 + D-13 选择器改名"
  - phase: idi-04.1-radix
    plan: 02
    provides: "同类空转守卫的修复先例与「修复必须配变异对照」的纪律(check-01 tier-1 交替式)"
provides:
  - "CR-01 关闭:`resolve_color` 区分「令牌已声明 / 未声明」,未声明返回 `None`;24 处颜色断言在令牌改名/删除下重新具备证伪能力"
  - "`ok()` 的 `expected is None` → BLOCKED 分支:期望值解析不出不再落进比较分支记 FAIL"
  - "`scripts/probe-05-resolve-color.py`:可复跑的变异证明 —— 同一份被删掉 `--color-text-muted` 声明的副本上,修复前记 PASS / 修复后记 BLOCKED,未变异对照仍记 PASS"
affects: [idi-04.1-verification, phase-5-visual, phase-6, phase-7-focus-ring]

actuals:
  tokens: 3222      # chars/4 over the realized diff (12890 chars) — same scale as the plan's estimate.tokens
  tasks: 3
  commits: 2        # f06b1d8 (fix) + ff0e95c (test);Task 3 产出 SUMMARY,无代码 delta
  plan_head_before: f5adfa4ab5cd5bd93b0f6067e7d6b406ea5a11a1

tech-stack:
  added: []
  patterns:
    - "变异只活在浏览器侧被拦截的响应里(`page.route` + `route.fetch()` → 字符串删行 → `route.fulfill(response=resp, body=mutated)`),被验证的仓库文件逐字节不变"
    - "反事实常量:把修复前的实现体原样留成探针里的常量,是「修复前会怎样」的唯一硬证据;没有它对照就退化成自陈"
    - "未变异的对照支(control)是任何「修复使其不再空转」证明的必要半场 —— 否则一个恒 None 的实现也能骗过变异支"

key-files:
  created:
    - scripts/probe-05-resolve-color.py
  modified:
    - scripts/check-05-ui-uat.py

key-decisions:
  - "只改 `resolve_color` 与 `ok()` 两个 helper + 模块 docstring 的退出码释义一处括号;24 处调用点、全部 `expected` 字面值、`resolve_token` / `read_style` / `effective_bg` / `norm` / `item_verdict` / `_emit` 一字未动"
  - "`ok()` 的 `expected is None` 分支必须存在:不加它会落进比较分支,`norm(actual) == norm(None)` 恒为假 → 记 FAIL。FAIL 同样不是假 PASS,但 binding scope 明写 BLOCKED,且「期望值不可得」与「值不相等」是两种状态"
  - "`resolve_color` 的 docstring 用散文说「先确认 documentElement 上该令牌确有声明」,不逐字抄写读取表达式 —— 门按 `grep -c 'getPropertyValue'` 计数,抄一遍会让计数从 3 变成 4(照 plan 02 Task 1 的同款纪律)"
  - "探针按路径 `importlib.util.spec_from_file_location` 导入 harness 并复用其 helper,不复制实现 —— 否则探针测的就不是真实 helper"
  - "变异禁用 `sed`:本机是 darwin,BSD `sed` 的 `0,/re/` 地址会静默不替换,那会让变异空转、整条证明失去意义(plan 02 已实测并写成纪律);改用 Python 逐行过滤"
  - "探针**不是门**:不进四条守卫命令契约,不被任何门禁 / CI 调用;顶部注释明写这一点(T-idi041-16)"

patterns-established:
  - "空转守卫的修复必须配「反事实常量 + 变异副本 + 未变异对照」三件套:反事实证明旧形态会静默通过,变异证明新形态真的会失败,对照证明修复没有把断言变成恒 BLOCKED"

requirements-completed: [CHECK-02, A11Y-04]

coverage:
  - id: D1
    description: "`resolve_color` 在令牌未声明时返回 `None`(不再返回探针继承到的正文色);`ok()` 把 `None` 期望值记 BLOCKED —— 24 处颜色断言在令牌改名/删除下重新具备证伪能力"
    requirement: "CHECK-02"
    verification:
      - kind: mutation
        ref: "scripts/probe-05-resolve-color.py → PROBE mutated-postfix-verdict=BLOCKED (exit 0)"
        status: pass
      - kind: integration
        ref: ".venv/bin/python scripts/check-05-ui-uat.py → 0 FAIL;item 1/2/3/4/6 PASS 且 0 BLOCKED;item 5 BLOCKED (9,0,2);exit=2 —— 与 VERIFICATION.md P3.7 基线逐项一致"
        status: pass
    human_judgment: false
  - id: D2
    description: "CR-01 的变异证明落地为可复跑脚本:拦截 `/style.css`、只删 `--color-text-muted` 声明,打印四行 `PROBE …` 对照"
    requirement: "CHECK-02"
    verification:
      - kind: mutation
        ref: ".venv/bin/python scripts/probe-05-resolve-color.py → mutation-applied=yes / mutated-prefix-verdict=PASS / mutated-postfix-verdict=BLOCKED / control-verdict=PASS (exit 0)"
        status: pass
      - kind: unit
        ref: "git diff --exit-code -- frontend/style.css → exit 0(变异未落盘)"
        status: pass
    human_judgment: false
  - id: D3
    description: "九条范围外项(W-2 / W-3 / W-4 / W-5 / W-6 / CR-02 / IN-01 / IN-02 / IN-03)与 12 行 unclassified 逐条登记为 deferred、既未修也未静默丢弃"
    verification:
      - kind: unit
        ref: "grep -oE 'W-2|W-3|W-4|W-5|W-6|CR-02|IN-01|IN-02|IN-03' <SUMMARY> | sort -u | wc -l → 9"
        status: pass
    human_judgment: true
    rationale: "登记是否忠实于 VERIFICATION.md 的逐条原文、是否真的「未静默扩范围」,是判断项 —— 机械门只证明九条各自出现过,不证明口径未被改写"
  - id: D4
    description: "范围外人工项 H-1(28 条 UI-SPEC backstop 陈述,约 21 条无自动化证据)被登记为未解决,本 run 不代其转绿(非本计划交付物,阶段级携带项)"
    verification: []
    human_judgment: true
    rationale: "VERIFICATION.md frontmatter `human_verification[0]`;裁切/换行/滚动归属/200% 缩放/菜单重定位这类渲染几何行为 `grep` 与 computed-style 都看不见,必须由人看"
  - id: D5
    description: "范围外人工项 H-2(E16 的 `--color-text ON --color-surface-mark` 比值归属)被登记为未裁决,本 run 不代其裁决(非本计划交付物,阶段级携带项)"
    verification: []
    human_judgment: true
    rationale: "VERIFICATION.md frontmatter `human_verification[1]`;该对不在 check-02 清单里,计划引用的 `15.88` 是另一个配对的数,是否补进清单并修正引用需人决定"

# Metrics
duration: 20min
completed: 2026-09-20
status: complete
---

# Phase 04.1 Plan 04: CR-01 关闭 —— `resolve_color` 区分令牌已声明/未声明 + 变异证明 Summary

**把 `check-05-ui-uat.py` 的颜色断言从「令牌改名/删除下恒真」修回「真的会失败」—— `resolve_color` 未声明即返回 `None`、`ok()` 把 `None` 期望值记 BLOCKED(两处 helper),并用一份只删掉 `--color-text-muted` 声明的浏览器侧副本证明:同一条断言修复前记 PASS(渲染已坏)、修复后记 BLOCKED,未变异对照仍记 PASS。**

## Performance

- **Duration:** 20 min
- **Started:** 2026-09-20T01:51:27Z
- **Completed:** 2026-09-20T02:11:30Z
- **Tasks:** 3 / 3
- **Files modified:** 2(`scripts/check-05-ui-uat.py`、新增 `scripts/probe-05-resolve-color.py`)

## Accomplishments

- **CR-01 关闭。** `resolve_color` 现在先读 `documentElement` 上该令牌的声明,为空即返回 `None`;`ok()` 新增 `expected is None` → BLOCKED 分支。24 处颜色断言在令牌改名/删除下重新具备证伪能力 —— 这正是 D-14 换掉 22 条硬编码 `rgb(...)` 时付出的代价(见下「成因链」)。
- **修复被证明,而非被断言。** `scripts/probe-05-resolve-color.py` 在浏览器侧拦截 `/style.css`、逐行删掉 `--color-text-muted:` 声明,同一份副本上跑同一条断言两次:修复前 `expected=rgb(32, 32, 32) actual=rgb(32, 32, 32)` → **PASS**(提示灰已变成正文黑,渲染明显是坏的,而 harness 记 PASS);修复后 `expected=<UNRESOLVED> actual=rgb(32, 32, 32)` → **BLOCKED**。这是缺陷与修复的双向实证。
- **修复没有引入另一种空转。** 未变异的对照支 `expected=rgb(100, 100, 100) actual=rgb(100, 100, 100)` → PASS;全量 harness 的逐项结论与 VERIFICATION.md P3.7 基线**逐项一致**(0 FAIL、item 1/2/3/4/6 PASS 且 0 BLOCKED、item 5 `BLOCKED (9,0,2)`、`exit=2`)。一个永远返回 `None` 的 `resolve_color` 会被这两道门同时抓住。
- **被验证对象未被污染。** 变异只活在 `page.route` 拦截到的那份响应里,不写任何磁盘文件;`git status --porcelain -- frontend/` 为空,`git diff --exit-code -- frontend/style.css` 退出码 0。
- **范围纪律。** 九条范围外项与两条人工项逐条登记为 deferred(见下),既未修也未静默丢弃;12 行 `unclassified` / `unresolved` 沿用 plans 01–03 的处置。
- **零依赖、零构建步骤。** 探针只用标准库 + `.venv` 里已装的 `playwright`(harness 早已依赖它);四条守卫命令契约与 `pytest` 基线不变。

## Task Commits

Each task was committed atomically:

1. **Task 1: `resolve_color` 区分「已声明 / 未声明」,`ok()` 把 `None` 期望值记 BLOCKED** - `f06b1d8` (fix)
2. **Task 2: 变异证明 —— 删掉 `--color-text-muted` 声明后该断言不再记 PASS** - `ff0e95c` (test)
3. **Task 3: 全量门禁收口 + 把变异对照与范围外登记写进 SUMMARY** - 无独立提交(本任务产出 SUMMARY 与一次全量复跑,代码 delta 为零,见下)

**Plan metadata:** (docs: complete plan — 本 SUMMARY 的提交)

## Files Created/Modified

- `scripts/check-05-ui-uat.py` — `resolve_color` 加「令牌未声明 → `None`」前置分支(+7/−1);`ok()` 加 `expected is None` → BLOCKED 分支(+8/−0,含 docstring 补述);模块 docstring L42 的退出码 `2` 释义补「期望值解析不出」(1 行内改写)。净 `+19/−3`。
- `scripts/probe-05-resolve-color.py` — **新增**(246 行)。CR-01 的变异证明:按路径导入 harness 复用其 helper,`PREFIX_PROBE_JS` 反事实常量引自 `68309d0`,浏览器侧路由变异,四条 `PROBE …` 输出契约 + 四值对照表,退出码 0/1。**不是门。**

## CR-01 对照证据(本 SUMMARY 的承重内容)

### 四值对照表(逐字抄自探针输出)

| 值 | 实测 | 含义 |
|---|---|---|
| `pre_fix_expected` | `rgb(32, 32, 32)` | 修复前的期望值 —— 探针 `color: var(--color-text-muted)` 在 computed-value 阶段失效,继承 `body` 的正文黑 |
| `hint_computed` | `rgb(32, 32, 32)` | 真实消费者 `.hint` 的 computed 值 —— 与期望值**退化成了同一个继承值**(提示灰已变成正文黑,渲染明显是坏的) |
| **修复前判定** | **PASS** | **这就是缺陷的实证**:渲染已坏,而 harness 记 PASS |
| **修复后判定** | **BLOCKED** | **这就是修复的实证**:期望值解析不出,不再记 PASS |

探针逐字输出:

```
PROBE mutation-applied=yes
PASS [mutated] .hint color == var(--color-text-muted) (pre-fix): expected=rgb(32, 32, 32) actual=rgb(32, 32, 32)
PROBE mutated-prefix-verdict=PASS
BLOCKED [mutated] .hint color == var(--color-text-muted) (post-fix): expected=<UNRESOLVED> actual=rgb(32, 32, 32)  # 令牌未声明或期望值解析失败
PROBE mutated-postfix-verdict=BLOCKED
PROBE contrast-table: pre_fix_expected=rgb(32, 32, 32) | hint_computed=rgb(32, 32, 32) | pre-fix verdict=PASS | post-fix verdict=BLOCKED
PASS [control] .hint color == var(--color-text-muted): expected=rgb(100, 100, 100) actual=rgb(100, 100, 100)
PROBE control-verdict=PASS
exit=0
```

### 两条修复的形状

1. **`resolve_color(page, token)` —— 签名不变,行为契约改变。** 在探针 `div` 被创建**之前**先读 `documentElement` 上该令牌的声明,`trim()` 后为空即返回 `None`。已声明令牌的探针路径(建 `div` → `p.style.color = var(--t)` → `appendChild` → 读 computed color → `remove` → 返回)逐字保留。未声明令牌此前返回探针继承到的正文色 —— 因为真实消费者用的是**同一个** `var(--t)`,两侧退化成同一个继承值,断言恒真。
2. **`ok(item, label, expected, actual, note="")` —— 签名不变,新增一条判定路径。** `expected is None` → `BLOCKED`(reason `令牌未声明或期望值解析失败`,expected 打印 `<UNRESOLVED>`),置于 `actual is None` 分支**之前**;其余三条路径与 `norm` 一字未动。**不加这一支会落进比较分支 —— `norm(actual) == norm(None)` 恒为 False —— 于是记 FAIL。FAIL 同样不是假 PASS(证伪能力已经恢复),但本次 `--gaps` 的 binding scope 明写「使 `ok()` 记 BLOCKED 而非假 PASS」,故必须补上这一支才能兑现该措辞。** 附带收益:走 `resolve_token` 的四条断言(item4 的三条 z-index 断言 + smoke 的 `--z-badge` 断言)本来就该有这个对称保护。

### 成因链

D-14 把 22 条硬编码 `rgb(...)` 断言换成 `resolve_color` 调用,移除了「值层改动产生假 FAIL」的根因 —— **同时**移除了「令牌接错线 / 被改名时响亮 FAIL」的能力。**这一损失并非未披露:** plan 03 把它登记为**已由 `check-02` 的 43 对实测比值与每条接线断言旁的 `info()` 解析值补偿**(见 `idi-04.1-03-PLAN.md:34`、该计划的威胁登记行 `T-idi041-10`、以及 `idi-04.1-03-SUMMARY.md:33`)。

CR-01 证明的是:**该补偿只覆盖了值轴**(值本身错了能看见),**接线轴**(令牌被改名/删除)仍然空转。这是比「未披露」更强的结论,也是本 SUMMARY 要写的准确口径。**不得写成「计划与 SUMMARY 只写了收益、未披露这一损失」**——该陈述与仓库矛盾。〔本句为**编排器代写**(`authored_by: orchestrator`):planner 修订连续两次在 600s 看门狗处卡死且盘上零改动,经用户明确授权代写;改动面仅此一句事实口径,由 plan-checker 独立复核。〕

VERIFICATION.md 的 B-1 已在真实 chromium-1243 上独立复现过同一机制(拦截 `/style.css` 删掉声明后 `.hint` computed 与 `resolve_color` 都变成 `rgb(32, 32, 32)`,而 harness 记 PASS);本 run 把那条一次性复现固化成可复跑的证据。

## Verification Evidence

### 全量门禁复跑(逐条记命令 + 逐字输出 + 退出码)

| # | 门 | 命令 | 逐字输出 | 退出码 |
|---|---|---|---|---|
| 1 | CHECK-01 | `bash scripts/check-01-token-conformance.sh` | `PASS` | **0** |
| 2 | CHECK-02 | `python3 scripts/check-02-contrast.py` | 末行 `PASS: 0 failures`;含 `ORDER 0.363  --color-text-muted before --color-text on --color-surface` | **0** |
| 3 | CHECK-03 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` | **0** |
| 4 | CHECK-04 | `bash scripts/check-04-important-count.sh` | `PASS` | **0** |
| 5 | 全量 harness | `.venv/bin/python scripts/check-05-ui-uat.py` | 见下表逐项;0 条 `^FAIL ` 行;末行 `exit=2  (0=全 pass,1=有 fail,2=有 blocked)` | **2** |
| 6 | 变异证明 | `.venv/bin/python scripts/probe-05-resolve-color.py` | 四行 `PROBE …` 齐备;`exit=0` | **0** |
| 7 | 回归 | `.venv/bin/python -m pytest -q 2>&1 \| grep -c '219 passed, 6 skipped'` | `1`(实测汇总行 `219 passed, 6 skipped, 1 warning in 6.01s`,故按子串判定而非整行) | — |

### 全量 harness 逐项与 VERIFICATION.md P3.7 基线对照

| 项 | 本 run 实测 | P3.7 基线 | 对照 |
|---|---|---|---|
| item 1 | `PASS  (45 条断言,0 FAIL,0 BLOCKED)` | `PASS (45,0,0)` | **一致** |
| item 2 | `PASS  (5 条断言,0 FAIL,0 BLOCKED)` | `PASS (5,0,0)` | **一致** |
| item 3 | `PASS  (15 条断言,0 FAIL,0 BLOCKED)` | `PASS (15,0,0)` | **一致** |
| item 4 | `PASS  (24 条断言,0 FAIL,0 BLOCKED)` | `PASS (24,0,0)` | **一致** |
| item 5 | `BLOCKED  (9 条断言,0 FAIL,2 BLOCKED)` | `BLOCKED (9,0,2)` | **一致** |
| item 6 | `PASS  (2 条断言,0 FAIL,0 BLOCKED)` | `PASS (2,0,0)` | **一致** |
| 汇总 | `exit=2` | `exit=2` | **一致** |

item 5 的两条 BLOCKED 逐字为 `[p3] 交互冒烟「处理本轮批注」` 与 `[p3] 交互冒烟「发送」`,与基线逐字相同。**0 条 `^FAIL ` 判定行。**

**这条对照就是 T-idi041-15 的处置证据:** `ok()` 的新分支只在 `expected is None` 时生效,而真实树上全部令牌都已声明、`resolve_color` / `resolve_token` 均返回非 None 值 —— 任何把真 FAIL 降级成 BLOCKED 的行为都会让逐项计数偏移而被抓住。逐项一致,故无降级。

### 静态门

| 门 | 命令 | 结果 |
|---|---|---|
| `getPropertyValue` 计数 | `grep -c 'getPropertyValue' scripts/check-05-ui-uat.py` | `3`(L268 `resolve_color` 新增 + L287 `resolve_token` 原有 + L798 item4 `--text-base` 原有) |
| `expected is None` 计数 | `grep -c 'expected is None' scripts/check-05-ui-uat.py` | `1` |
| 语法 | `.venv/bin/python -m py_compile scripts/check-05-ui-uat.py` / `scripts/probe-05-resolve-color.py` | 均 OK |
| 改动面 | `git diff --numstat f5adfa4..HEAD` | `19 3 scripts/check-05-ui-uat.py` + `246 0 scripts/probe-05-resolve-color.py`(两文件) |
| 删除文件 | `git diff --diff-filter=D --name-only f5adfa4..HEAD` | 空 |
| 探针零第三方依赖 | `ast` 扫 import 集合 | `['__future__', 'importlib', 'pathlib', 'playwright', 'shutil', 'sys', 'tempfile']` |
| 样式表逐字节未变 | `git diff --exit-code -- frontend/style.css` | exit 0 |
| 被验证对象零改动 | `git status --porcelain -- frontend/` | 空 |
| 探针临时目录自清 | `ls /tmp \| grep -c 'idi-05-probe'` | `0` |

### 工作树范围门(执行期观察,非偏离)

计划 Task 3 给出的范围门是 `git status --porcelain -- . ':!.claude/settings.local.json' ':!.planning/config.json'`。本次执行实测输出为:

```
 M .planning/STATE.md
 M .planning/state.json
```

**这两项不是本 run 的产出。** 本会话起始的 git status 快照即为 `M .claude/settings.local.json` / `M .planning/STATE.md` / `M .planning/config.json` / `M .planning/state.json` —— 四个条目在本 run 动手前就已 modified,是 GSD 编排器写入的流程状态,与本计划的两个脚本无因果关系(本 run 未对任何 `.planning/*` 或 `.claude/*` 文件执行过写操作,Task 1 / Task 2 的两次提交的 `--numstat` 各只含 `scripts/` 下的一个文件)。计划的排除清单只列了两项,未覆盖 `STATE.md` / `state.json`。

**门的意图成立:** 本 run 在 `scripts/` 之外零新增、零改动 —— 两个改动源文件(均已提交)与一份新脚本,加本 SUMMARY,再无其它。此观察与 plan 02 SUMMARY 记录的同类既有工作树状态同源(计划的工作树范围门与实际的起始快照不一致),记录以免被误读为缺陷。

## Decisions Made

- **只改两处 helper + 一处 docstring 括号。** 24 处 `resolve_color` 调用点、全部 `expected` 字面值、`resolve_token` / `read_style` / `effective_bg` / `norm` / `item_verdict` / `_emit` 一字未动;`item_smoke` 的 `!= "none"` 写法与 `wait_done` 的谓词也一字未动(两者都是范围外)。
- **`ok()` 的新分支是 binding scope 的要求,不是可选修饰。** 见上「两条修复的形状」第 2 条:不加它会记 FAIL —— FAIL 也不是假 PASS,但 scope 明写 BLOCKED。
- **docstring 不逐字抄写读取表达式。** 门 `grep -c 'getPropertyValue'` 必须等于 3;若 docstring 里再抄一遍完整表达式,计数会变成 4 而门变红。故用散文说「先确认 `documentElement` 上该令牌确有声明」。
- **探针复用 harness 而不另写一套。** 用 `importlib.util.spec_from_file_location` 按路径导入(文件名带连字符,不能走普通 `import`;该文件末尾是 `if __name__ == "__main__": sys.exit(main())`,导入无副作用),复用 `ensure_server` / `make_fixture` / `enter_project` / `resolve_color` / `read_style` / `ok` / `norm` / `ROWS` / `HOST, PORT` / `BASE_URL`。复制实现会让探针测的就不是真实 helper。
- **变异禁用 `sed`,并显式断言变异真的发生。** BSD `sed` 的 `0,/re/` 地址在本机(darwin)会静默不替换 —— 那会让整条证明空转。改用 Python 逐行过滤,并断言 `mutated != 原始 body` 且 `mutated` 不再含 `--color-text-muted:`;不成立即 exit 1,且 `PROBE mutation-applied=yes` 必须打印。
- **Task 3 无独立提交。** 它的 `<files>` 是 SUMMARY 本身,计划明写「本任务不产出代码改动」。全量复跑、对照证据抄录、范围登记即为验收(沿 `idi-04-02` Task 2 与 `idi-04-03` 的既有先例)。

## Deviations from Plan

None - plan executed exactly as written.

一条执行期观察(不是偏离,记录以免被误读为缺陷,详见上「工作树范围门」):计划 Task 3 的工作树范围门把排除项写为 `.claude/settings.local.json` 与 `.planning/config.json`,而本 run 起始快照里被改的是那两项**加上** `.planning/STATE.md` 与 `.planning/state.json`。后两项是 GSD 流程状态、动手前既有、本 run 未触碰;门的意图(本 run 在 `scripts/` 之外零新增零改动)成立。

## Issues Encountered

None. 唯一需要说明的是本机 `zsh` 的 `PIPESTATUS` 不可用(`bash` 语法),故涉及管道的退出码改用「重定向到临时文件后取 `$?`」的方式逐条取证 —— 这是取证方式的调整,不是缺陷。

## Threat Surface Scan

| Threat ID | Disposition | 处置结果 |
|---|---|---|
| T-idi041-11(篡改:变异证明污染真实 `frontend/style.css`) | mitigate | **已消解。** 变异只在 `page.route("**/style.css", …)` 拦截到的响应里构造,不写任何磁盘文件;`git diff --exit-code -- frontend/style.css` exit 0,`git status --porcelain -- frontend/` 为空 |
| T-idi041-12(篡改:空转变异) | mitigate | **已消解。** 禁用 `sed`,改用 Python 逐行过滤;探针显式断言 `mutated != 原始 body` 且不再含 `--color-text-muted:`,并打印 `PROBE mutation-applied=yes` |
| T-idi041-13(否认:修复被断言为「有效」而非被证明) | mitigate | **已消解。** 反事实常量 `PREFIX_PROBE_JS`(引自 `68309d0`)+ 同一份变异副本上修复前 PASS / 修复后 BLOCKED 的双向对照,逐字进本 SUMMARY |
| T-idi041-14(篡改:修复把断言变成恒 BLOCKED) | mitigate | **已消解。** PASS B 对照支断言未变异世界里同一条断言仍记 PASS;全量 harness 门要求 item 1/2/3/4/6 的 BLOCKED 计数为 0 —— 两道门同时成立 |
| T-idi041-15(篡改:`ok()` 新分支吞掉真实 FAIL) | mitigate | **已消解。** 该分支只在 `expected is None` 时生效;真实树上逐项结论与 P3.7 基线逐项一致(见上对照表),任何降级都会让计数偏移而被抓住 |
| T-idi041-16(否认:新探针被当成门禁而长期腐烂) | mitigate | **已消解。** 探针顶部注释明写「变异证明,不是门」;未加入四条守卫命令契约,无任何门禁依赖它 |
| T-idi041-SC(供应链) | accept | 未变:**本 run 未安装任何包**;探针 import 集合为纯标准库 + `.venv` 里已装的 `playwright`;四条守卫仍零依赖 |

**诚实结论:本 run 不存在 high 或 critical 级威胁。** 改动面是一个 helper 的前置检查、一个断言记录器的分支、以及一个只读的浏览器侧变异探针 —— 全部在本机、离线、无凭据。

## Deferred Scope Register(范围外项,本 run 未修,不得静默丢弃)

全部条目逐字来自 VERIFICATION.md `## Anti-Patterns Found` 与 frontmatter `human_verification`,照录本计划 `<deferred>` 表的口径,不改写、不省略。

| 编号 | 位置 | 性质 | 本 run 的处置 |
|---|---|---|---|
| **W-2** (WR-01) | `scripts/check-01-token-conformance.sh:41-43` | 交替式要求 `var(--` 无空格,CSS 允许 `var( --radix-gray-11 )` → TOKEN-02 的硬不变量仍有机械缺口 | deferred,不修 |
| **W-3** (WR-02) | `scripts/check-01-token-conformance.sh:17-27` | 成对断言只数 START/END 数量、不管位置;标记被搬移时 `$outside` 退化为空而打印 `PASS` | deferred,不修 |
| **W-4** (WR-03) | `frontend/style.css:279-341` 清单 + plan 01 的 E16 backstop | 清单缺 `--color-text ON --color-surface-mark`;引用的 `15.88` 实为 `--color-text ON --color-surface-page` 的数,该引用在 `check-02` 输出里不存在(实测 text-on-mark = 15.0:1) | deferred,不修;与人工项 H-2 同源 |
| **W-5** (WR-04) | `scripts/check-05-ui-uat.py:996-997` | `read_style(...) != "none"` 在元素缺席时返回 `None`,`None != "none"` 为真 → `smoke #state-badge 可见` 记 PASS | deferred,不修(同文件 item1 L404-405 的写法是对的,但改它属范围外) |
| **W-6** | `frontend/style.css:229-231` | z-index 序关系(`badge < banner`)只有散文注释,无任何脚本比较两个值;`--z-overlay` 无运行时断言 | deferred,不修 |
| **CR-02** | `scripts/check-05-ui-uat.py:873-883`(`wait_done`)、923-930(发送分支) | `wait_done("#btn-send")` 的谓词是 `el.disabled === false`,而 `app.js` 只在归档态 disable `#btn-send` → 90s 截止是死代码 | deferred,不修;**预先存在**于 `6f52602`,本阶段未触碰 `run_ai_smoke` |
| **IN-01** | `scripts/check-05-ui-uat.py:477-480` | `goto_frozen_round(page, item)` 的 `item` 参数从未使用 | deferred,不修 |
| **IN-02** | `scripts/check-05-ui-uat.py:845` vs `:926` | 同一验收项在两个运行模式下标签不同(`[p3]` / `[p12]`) | deferred,不修 |
| **IN-03** | `scripts/check-05-ui-uat.py:842-847` / `1124-1127` | 默认运行必然 `exit 2`(`code = 1 if any_fail else (2 if any_blocked else 0)`) | deferred,不修(文档已记明) |

### 两条人工判断项(本 run 不代其转绿、不代其裁决)

| 编号 | 来源 | 内容 | 本 run 的处置 |
|---|---|---|---|
| **H-1** | VERIFICATION.md frontmatter `human_verification[0]` | 28 条 UI-SPEC backstop 陈述(约 21 条无自动化证据;7 条的比值半边已由 check-02 实测覆盖) | **deferred 为人工判断项**;不代其转绿 |
| **H-2** | VERIFICATION.md frontmatter `human_verification[1]` | E16 的 `--color-text ON --color-surface-mark` 比值归属(该对不在清单里,计划引用的 `15.88` 是另一个配对的数;实测 15.0:1 通过) | **deferred 为人工判断项**;不代其裁决 |

### 12 行 unclassified / unresolved 边角项

`TOKEN-01` / `TOKEN-02` / `TOKEN-04` / `TOKEN-07` / `CHECK-01` / `CHECK-02` / `CHECK-03` / `CHECK-04`(以上 8 行 `unclassified`)+ `A11Y-04`(boundary、precision 各 1 行)+ `A11Y-04b`(boundary、precision 各 1 行)= **12 行**。本阶段无 `*-SPEC.md`,`EDGE_ABSENT` / `PROHIB_ABSENT`;边角覆盖报告 `coverage: {applicable:12, resolved:0, unresolved:12, byVerification:{explicit:0,backstop:0}}`,12 行全部 `unclassified` / `unresolved`。

**本 run 的处置:沿用已执行 plans 01–03 的处置,不重新推导。** 它们继续以 `unresolved` 存在,由 Phase 5/6/7 与最终验收自行面对。`CHECK-02` 在本 run 交付的是它的**验收仪器侧**;`A11Y-04` 的两条探针问句(min/max/阈值两侧各一步、精度损失/溢出/舍入与平局规则的确切契约)在值层由 `check-02` 的实测比值与 WCAG 公式回答,本 run 不动。

**CR-01 的关闭不依赖上述任何一条范围外项。** CR-01 的成因是 `resolve_color` 的退化分支,与 W-2 / W-3 / W-4 / W-5 / W-6 / CR-02 / IN-01 / IN-02 / IN-03 无因果关系;本 run 未借修复之名对任何一条顺手补刀,也未静默扩范围。两条人工项与 12 行 `unresolved` 同样保持原状。

## User Setup Required

None - no external service configuration required.

## Known Stubs

None. 本计划只改两处 helper + 一处 docstring 释义,并新增一个只读的浏览器侧变异探针;无 UI 数据源、无占位文案、无未接线代码。

## Threat Flags

None. 未引入计划 `<threat_model>` 之外的任何新面 —— 无网络端点、无认证路径、无新依赖、无写仓库文件行为。新增文件是一个只读探针。

## Next Phase Readiness

- **CR-01 关闭,`idi-04.1-VERIFICATION.md` 的唯一 BLOCKER 消解。** 该报告 `## Required Artifacts` 里 `scripts/check-05-ui-uat.py` 的 `⚠️ PARTIAL` 判定("`resolve_color` 的未声明分支缺失使其颜色断言在改名/删除下恒真")现在可以翻绿。`0 FAIL` 这条头条证据的验收仪器重新具备证伪能力。
- **`0 FAIL` 的语义未变。** 逐项结论与 P3.7 基线逐项一致;`exit=2` 仍由 item 5 的两条 AI 冒烟 BLOCKED 产生(IN-03 已登记,文档已记明 —— 退出码不能当默认运行的通过信号)。
- **同类风险已排查过一轮。** plan 02 修掉 `check-01` 的 tier-1 交替式空转,本计划修掉 `check-05` 的 `resolve_color` 空转 —— 两者是同一失败类(守卫静默空转)。已登记但未修的同类残余是 W-3(标记搬移)与 W-5(`!= "none"`),它们仍在 VERIFICATION.md 的 `## Anti-Patterns Found` 里可见。
- **留给 verify-work 的人工项未变。** 28 条 UI-SPEC backstop(约 21 条无自动化证据)与 E16 的比值归属仍为 `human_judgment: true`,不得静默通过。
- **Phase 7 的注意项(沿自 UI-SPEC 携带项 #8):** 焦点环 `--color-focus: #1f63bd` 必须针对新的底色(`--color-surface` `#f9f9f9`、`--color-surface-page` `#fcfcfc`)重测,不能再对着旧的 `#fafafa`。

## Self-Check: PASSED

- `scripts/check-05-ui-uat.py` 在盘上 ✓;`scripts/probe-05-resolve-color.py` 在盘上 ✓
- `git log --oneline --grep="idi-04.1-04"` 返回 ≥1 提交 ✓(`f06b1d8`、`ff0e95c`)
- Task 1 全部 `<acceptance_criteria>` 复跑通过:计数 3/1、py_compile、harness 逐项与基线一致、`frontend/` 为空 ✓
- Task 2 全部 `<acceptance_criteria>` 复跑通过:四行 `PROBE …`、exit 0、`frontend/style.css` exit 0、harness 零 diff、import 集合无第三方 ✓
- Task 3 全部门复跑通过:四条守卫 `PASS` / exit 0(含 `ORDER 0.363` 与 `PASS: 0 failures`)、harness 0 `^FAIL ` 行、探针 exit 0、`pytest` 子串计数 1、`frontend/` 为空 ✓
- 计划级 `<verification>` 七条逐条复跑,结果见上「Verification Evidence」✓

---
*Phase: idi-04.1-radix*
*Completed: 2026-09-20*
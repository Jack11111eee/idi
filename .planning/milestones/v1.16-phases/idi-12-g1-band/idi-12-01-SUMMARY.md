---
phase: idi-12-g1-band
plan: 01
subsystem: ui
tags: [css, design-tokens, playwright, gate, mutation-testing, fixture, markdown-grammar]

# Dependency graph
requires:
  - phase: idi-11-decard-and-hairline-dividers
    provides: 统一面 = 白(D-11-1)、check-09 的 c1..c5 运行时契约、`--color-surface-page` 的就地改写与其承重注释写法
provides:
  - "`#latest-check` 的宿主绘制面由内陷面(gray-2)就地改归统一面(白)⇒ 报告区表头读作一条独立的 band"
  - "`scripts/check-09-idi09-validation.py` 的新运行时项 `c6`(G1 band 两侧钉死 + fixture 模式不变量),经两条变异证明会失败"
  - "`scripts/ui-states/checking/docs/DESIGN-check-2.md` 补上后端文法强制的「问题分级」表 ⇒ `checking` 样本首次真的渲染出表头"
  - "围栏 `:129-130` 承重注释的就地改写(保留仍为真的那半句 + 记录旧句为何为假)"
affects: [idi-12-02, idi-12-03, check-05, check-06, check-07, check-09, check-10]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
actuals:
  tokens: 2581
  tasks: 3
  commits: 5
  plan_head_before: a1c3a4d1168f8590fa806e429eab60dc590db908

# #3968 ledger fields, repeated at top level: verify-work extracts them with column-0
# anchored greps (`^commits:` / `^plan_head_before:`), which the nested `actuals:` block
# above does not satisfy. Both record the count measured immediately before this closing
# commit, so verify-work's same-instrument check sees ACTUAL == CLAIMED + 1.
commits: 5
plan_head_before: a1c3a4d1168f8590fa806e429eab60dc590db908

tech-stack:
  added: []
  patterns:
    - "band 判据两侧钉死:宿主 == 令牌解析值 == 写死白字面量,且宿主 != 表头"
    - "变异证明守卫可失败:定点受控改写 → 逐字抄录 FAIL → 定向 git checkout 还原 → git diff --exit-code rc=0 且 git hash-object 逐字符相同"

key-files:
  created: []
  modified:
    - frontend/style.css
    - scripts/check-09-idi09-validation.py
    - scripts/ui-states/checking/docs/DESIGN-check-2.md

key-decisions:
  - "沿用 D-12-1 选定路线:改宿主(移宿主 → 改白),不是改全局 `.markdown-body th`、也不是局部覆盖 `#latest-check th`"
  - "新判据另立 `c6` 而不并进 `c1..c5`:`c1..c5` 是 Phase 11 的 REG-01 契约载体,分开才让「哪条判据钉哪一次改动」可分辨(D-12-6 的 Discretion 项)"
  - "`c6` 的「表头可读」走硬 FAIL(`ok_true`)而不是 BLOCKED;每一处令牌解析断言都走 `ok_true` 并显式处理 `None`"
  - "fixture 的问题分级表至少一行 P1:全 P2 会让 `is_pure_p2` 为真 ⇒ `mode` 翻成 `p2` ⇒ 涟漪波及五条浏览器门与全部截图"
  - "fixture 的表紧跟 `# 核查报告 2` 标题行:`max-height: 30vh` 使它成滚动区,表放靠下就拍不到 band(D-12-10)"

patterns-established:
  - "Pattern 1: 令牌解析断言一律 `ok_true` + 显式 None 分支(堵住 `ok()` 在期望侧为 None 时降级成 BLOCKED)"
  - "Pattern 2: fixture 模式不变量断言 —— `#btn-continue-check` 不带 `.hidden` ∧ `#verdict-cards` 无 `.verdict-card` ⇒ `mode === 'running'`"

requirements-completed: [G1-01]

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "`#latest-check` 的宿主绘制面改归统一面(白),其内表头在真实浏览器里读作一条独立的 band"
    requirement: "G1-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c6 → item c6: PASS (7 条断言,0 FAIL,0 BLOCKED), exit=0"
        status: pass
    human_judgment: false
  - id: D2
    description: "`c6` 经两条变异证明会失败(M1 两条钉死半条同时红;M2 证明「宿主 == 白」半条不可省)"
    requirement: "G1-01"
    verification:
      - kind: automated_ui
        ref: "M1/M2 两次 --item c6 运行读数(本 SUMMARY「Mutation Proofs」段逐字抄录),还原后 rc=0 且 hash-object 相同"
        status: pass
    human_judgment: false
  - id: D3
    description: "`checking` fixture 报告忠于后端文法(`## 问题分级` 标题 + 逐字表头 + 至少一行 P1),样本仍处 `running` 态"
    requirement: "G1-01"
    verification:
      - kind: unit
        ref: "backend.grammar.parse_problem_grades / is_pure_p2 / is_pass_conclusion over the fixture → rows 2 / levels [P1, P2] / pure_p2 False / pass_conclusion False"
        status: pass
    human_judgment: false
  - id: D4
    description: "围栏承重注释就地改写:声明数不变(119)、零新增对比度条目(PAIR 仍 53)"
    requirement: "G1-01"
    verification:
      - kind: unit
        ref: "fence decl regex count == 119 / unique 119; check-02 `PASS: 0 failures`; `grep -c '/\\* PAIR '` == 53"
        status: pass
    human_judgment: false

# Metrics
duration: 82min
completed: 2026-09-29
status: complete
---

# Phase 12 Plan 01: G1 表头 band —— 宿主改归统一面 + `c6` 运行时判据 + fixture 补文法表

`#latest-check` 的宿主绘制面由内陷面 gray-2 就地改归统一面白,使其内的 markdown 表头在报告区读作一条独立的 band(gray-2 on white = 1.053,与文档区表头同款读感);该读数落成 `check-09` 的新运行时项 `c6`,并以两条真实变异读数证明两个钉死半条各自可失败。

## Performance

- **Duration:** 82 min(含一次因传输层错误中断并重试的尝试)
- **Started:** 2026-09-29T14:08+08:00(计划定稿后)
- **Completed:** 2026-09-29T15:30+08:00
- **Tasks:** 3/3
- **Files modified:** 3
- **Commits:** 5(measured:`git rev-list --count a1c3a4d..HEAD`,取本计划收口提交落定前的读数 —— 2 条任务提交 + 1 条元数据提交 + 2 条 SUMMARY 修正提交;收口提交本身构成 verify-work 容许的 +1)

## Accomplishments

- **G1 根因消除**:`#latest-check` 是四个 `.markdown-body` 宿主里唯一自画灰底的;把它改归统一面后,它内部的 `th`(仍消费 gray-2)不再与宿主同色 —— 消除的是**不对称本身**,不是给表头换色。
- **band 在真实浏览器里可读**:`#latest-check` 计算底色 `rgb(255, 255, 255)` vs `#latest-check th` 计算底色 `rgb(249, 249, 249)`,两侧钉死(`== --color-surface-page` 解析值 **且** `== rgb(255, 255, 255)` 字面量)。
- **fixture 首次忠于后端文法**:`checking` 报告补上 `## 问题分级` 标题 + 逐字表头 + P1/P2 两行 ⇒ `parse_problem_grades` 返回 2 行,`is_pure_p2` / `is_pass_conclusion` 均为 False ⇒ `mode` 保持 `running`(以运行时模式不变量正面断言)。
- **守卫可失败**:M1(改回内陷面)⇒ 3 条 FAIL;M2(改指 gray-3)⇒ 2 条 FAIL 而「两者不同」半条保持 PASS —— 机械证明「只钉不同」不够。
- **零涟漪**:`c1..c5`(Phase 11 的 REG-01 契约)全绿、四条静态门全绿、`check-02` 零新增条目、pytest 基线 219 passed / 6 skipped 不变。

## Task Commits

Each task was committed atomically:

1. **Task 1: G1 band 单条路径端到端(fixture 补表 + 宿主改白 + `c6` 双钉判据)** - `00bf51b` (fix)
2. **Task 2: 围栏承重注释就地改写** - `39bce0b` (docs)
3. **Task 3: 两条变异证明** - 净产出为零代码改动(交付物是本 SUMMARY 的「Mutation Proofs」段),随本计划的元数据提交一并入册

**Plan metadata:** `bfb32d2` (docs: complete G1 header-band plan) — SUMMARY + STATE + ROADMAP + REQUIREMENTS
**SUMMARY fixup:** `eab5ca1` (docs: rename SUMMARY gate-evidence heading so `verify-summary` reads PASSED)

## Files Created/Modified

- `frontend/style.css` - `#latest-check` 规则体内 `background` 由 `var(--color-surface)` 就地改写为 `var(--color-surface-page)`(仅此一条声明值);围栏 `:129-150` 承重注释就地改写
- `scripts/check-09-idi09-validation.py` - 新增运行时项 `c6` + `ITEMS` 六项 + 模块 docstring 映射表补 `c6 → G1-01` 一行 + 顶部 `read_classlist` 别名
- `scripts/ui-states/checking/docs/DESIGN-check-2.md` - 首行标题之后插入 `## 问题分级` + 逐字表头 + 分隔行 + 两行数据(P1 / P2);其余内容逐字节保留

## Decisions Made

- **路线**:沿用 D-12-1「移宿主 → 改白」。不采用路线 (b)(改全局 `th`),也不追加 `#latest-check th` 局部覆盖 —— 前者会让文档区表头读感一并变深并打破 `check-10` 的 `t1`/`t2`,后者会引入宿主特例。
- **判据落位**:新判据另立 `c6`,不并进 `c1..c5`(`c1..c5` 是 Phase 11 的 REG-01 契约载体)。
- **判据形态**:两侧钉死 —— 既钉「宿主 != 表头」,也钉「宿主 == 统一面令牌 == 白字面量」。只钉前者会被「把宿主改成 gray-4 之类」满足(M2 是这条论证的机械证据)。
- **`c6` 的失败语义**:「表头可读」是硬 FAIL(走 `ok_true`),不是 BLOCKED;令牌解析断言一律 `ok_true` + 显式 `None` 分支。
- **fixture 加法规格**:必须带 `## 问题分级` 二级标题(`_extract_table` 只认二级标题下的表)且至少一行 P0/P1(防 `mode` 翻成 `p2`)。

## Mutation Proofs (Task 3)

### 前置条件(逐条记录)

| 项 | 值 |
|---|---|
| `git status --porcelain frontend/` | 空(两条变异都做在**已提交的树**上) |
| `git rev-parse HEAD` | `39bce0b4e84391c9847eda0537525077043272d7` |
| `git hash-object frontend/style.css` | `6dd19801494f4f02b261884bb251247723527345` |
| 基线 `.venv/bin/python scripts/check-09-idi09-validation.py --item c6` | `item c6: PASS (7 条断言,0 FAIL,0 BLOCKED)`,`exit=0` |
| 变异手法 | 定点受控改写:定位 `#latest-check {` 到其后第一个 `}`,断言块内目标子串**恰出现一次**,只替换块内那一处(其余 `--color-surface` 消费者一律不动) |
| 还原手法 | 定向 `git checkout -- frontend/style.css` |

**⚠ 全程未使用 `git stash`**(它跨工作树共享,本项目明令禁止);还原一律用定向 `git checkout -- frontend/style.css`。

### M1 —— 把宿主底色改回内陷面令牌

**注入:** `#latest-check` 块内 `background: var(--color-surface-page);` → `background: var(--color-surface);`(整文件仅此一处改动,`git diff` 确认)。

**观察到的读数(`rc=1`,`item c6: FAIL (7 条断言,3 FAIL,0 BLOCKED)`):**

```
INFO c6 #latest-check 计算 background-color 原始读数: rgb(249, 249, 249)
INFO c6 #latest-check th 计算 background-color 原始读数: rgb(249, 249, 249)
INFO c6 统一面 --color-surface-page 解析值: rgb(255, 255, 255)
FAIL [checking] #latest-check 计算底色 != #latest-check th 计算底色(表头读作一条独立 band): expected=host != th actual=host=rgb(249, 249, 249) th=rgb(249, 249, 249)  # G1 的准确含义是「灰底压灰底」:th 的下边线一直在(th, td 共享 gray-6 下边线),消失的是表头那一档底色 —— 表头行因此与数据行读起来一样
FAIL [checking] #latest-check 计算底色 == --color-surface-page 解析值(底色来自令牌): expected=== rgb(255, 255, 255) actual=rgb(249, 249, 249)  # 等值复核:证明底色来自令牌而不是硬编码的 rgb()。少了这条,把宿主写成字面量再删掉令牌声明也能全绿
FAIL [checking] #latest-check 计算底色 == rgb(255, 255, 255)(统一面写死字面量): expected=rgb(255, 255, 255) actual=rgb(249, 249, 249)  # 两侧钉死的第二半(D-12-7):只钉「两者不同」的话,将来有人把宿主改成 gray-4 之类仍然绿 —— 这一条把「改白」这件事本身也锁住。与上一条互补:只跟令牌比是**自指**的
```

**还原判据(两条,实测输出):**

- `git diff --exit-code -- frontend/style.css` → `rc=0`
- `git hash-object frontend/style.css` → `6dd19801494f4f02b261884bb251247723527345`(与前置记录值逐字符相同)

### M2 —— 把宿主底色改指 `--color-surface-sunken`(gray-3,与表头不同但**不是白**)

**注入:** `#latest-check` 块内 `background: var(--color-surface-page);` → `background: var(--color-surface-sunken);`。

**观察到的读数(`rc=1`,`item c6: FAIL (7 条断言,2 FAIL,0 BLOCKED)`):**

```
INFO c6 #latest-check 计算 background-color 原始读数: rgb(240, 240, 240)
INFO c6 #latest-check th 计算 background-color 原始读数: rgb(249, 249, 249)
INFO c6 统一面 --color-surface-page 解析值: rgb(255, 255, 255)
PASS [checking] #latest-check 计算底色 != #latest-check th 计算底色(表头读作一条独立 band): expected=host != th actual=host=rgb(240, 240, 240) th=rgb(249, 249, 249)  # G1 的准确含义是「灰底压灰底」:th 的下边线一直在(th, td 共享 gray-6 下边线),消失的是表头那一档底色 —— 表头行因此与数据行读起来一样
FAIL [checking] #latest-check 计算底色 == --color-surface-page 解析值(底色来自令牌): expected=== rgb(255, 255, 255) actual=rgb(240, 240, 240)  # 等值复核:证明底色来自令牌而不是硬编码的 rgb()。少了这条,把宿主写成字面量再删掉令牌声明也能全绿
FAIL [checking] #latest-check 计算底色 == rgb(255, 255, 255)(统一面写死字面量): expected=rgb(255, 255, 255) actual=rgb(240, 240, 240)  # 两侧钉死的第二半(D-12-7):只钉「两者不同」的话,将来有人把宿主改成 gray-4 之类仍然绿 —— 这一条把「改白」这件事本身也锁住。与上一条互补:只跟令牌比是**自指**的
```

**核心主张成立:** 「两者不同」半条在 M2 下**保持 PASS**(host=gray-3 != th=gray-2),而「宿主 == 白」半条必 FAIL ⇒ 两侧钉死不是冗余。这正是 D-12-7「只钉不同会被任何别的灰满足、判别力接近『只断言规则被写下了』」的机械证据。

**还原判据(两条,实测输出):**

- `git diff --exit-code -- frontend/style.css` → `rc=0`
- `git hash-object frontend/style.css` → `6dd19801494f4f02b261884bb251247723527345`(与 M1 还原值及前置记录值三者逐字符相同)

## Deviations from Plan

### Auto-fixed Issues

None —— 三处改动均按计划逐字执行。

### Documented criterion tension(非代码偏离,须显式登记)

**1. [Rule 4 - 计划内部张力] Task 3 的 M2 验收判据「只有「宿主 == 白」那条在 FAIL 行里出现」与 `<action>` 的断言清单不可同时满足**

- **Found during:** Task 3(M2 变异读数)
- **Issue:** Task 3 的 `<acceptance_criteria>` 要求 M2 的 FAIL 行里**只有**「宿主 == 白」一条。但同一任务的 `<action>` 第 3 条**强制**存在第三条断言「钉「宿主 == 令牌」」(`host_bg` 与 `--color-surface-page` 解析值 `norm()` 相等),而 `<done>` 也要求证明「宿主底色 == 统一面令牌 == 白」。在 M2 的注入下(宿主 = gray-3),宿主既不等于令牌、也不等于白 ⇒ 该条与「宿主 == 白」**同时**变红。故字面判据不可满足。
- **Fix(处置):** 保留 `<action>` 强制的那条断言(它是更严的门,且是 `<done>` 明文要求),**不删断言、不放宽判据**。逐字抄录 M2 的**实际** FAIL 集(2 条:「宿主 == 令牌」+「宿主 == 白」),并显式声明该判据的核心主张 —— 「两者不同」半条在 M2 下保持 PASS —— 已成立且已在上面留档。
- **Files modified:** 无(纯文档登记)
- **Verification:** 上面 M2 段落的逐字读数;`--item c6` 在未变异树上 `exit=0`、0 FAIL、0 BLOCKED
- **Committed in:** 本计划的元数据提交

---

**Total deviations:** 0 auto-fixed(代码),1 documented criterion tension(计划内部,已留档)
**Impact on plan:** 无实现影响 —— 交付的门比字面判据更严(多一条等值复核断言),且其可失败性由 M1/M2 两条真实读数共同证明。

## Issues Encountered

- **第一次执行尝试因传输层错误(SSL certificate hostname mismatch)中断**,未留下任何提交或文件改动;重试后从零开始执行,故本计划的墙上时钟(82 min)含该次失败尝试。**无任何工作丢失、无任何半成品状态。**
- 无其它问题。

## Gate Evidence(本计划收口时的整体检查)

| 检查 | 结果 |
|---|---|
| `bash scripts/check-01-token-conformance.sh` | `PASS`,rc=0 |
| `bash scripts/check-03-hidden-uniqueness.sh` | `PASS`,rc=0 |
| `bash scripts/check-04-important-count.sh` | `PASS`,rc=0 |
| `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`;`ORDER 0.363  --color-text-muted before --color-text on --color-surface` 逐字不变 |
| `grep -c '/\* PAIR ' frontend/style.css` | `53`(零新增对比度条目) |
| 围栏内 `(--[a-z0-9-]+)\s*:\s*([^;]+);` 匹配数 | `119`(去重后亦 `119`) |
| `grep -cF -- 'background: var(--color-surface-page);' frontend/style.css` | `5`(HEAD 基线 4 + 本计划 1) |
| `grep -cF -- 'still read as recessed' frontend/style.css` | `0` |
| `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4,c5,c6` | `exit=0`;c1 59 / c2 19 / c3 6 / c4 39 / c5 5 / c6 7 条断言,**0 FAIL,0 BLOCKED** |
| `backend.grammar` 直读 fixture | `rows 2` / `levels ['P1', 'P2']` / `pure_p2 False` / `pass_conclusion False` |
| `.venv/bin/python -m pytest backend/tests -q --tb=short` | `219 passed, 6 skipped`(与规划期基线逐项相同) |
| `git status --porcelain -- frontend/ scripts/ backend/ frontend/vendor/ ':(exclude)scripts/.check09-old.py'` | 空(改动全部已提交,只涉上表三个路径) |
| `git diff --stat -- frontend/app.js frontend/index.html backend/ frontend/vendor/` | 空(逐字节未改) |
| `ls frontend/vendor/` | 仅 `marked.min.js` |

## Known Stubs

None —— 无硬编码空值、无占位文案、无未接线组件。

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **计划 02(VIS-01 截图)可开工**:`checking` 样本现在真的渲染出表头,`#latest-check` 的元素截图有内容可拍;`#latest-check` 的 `max-height: 30vh` 与 `border` / `border-radius` 逐字节未动(D-12-3),`probe-card-border-token.py` 读的 gray-6 边框读数不变。
- **计划 03(REG-04 复跑)的前置已满足**:这是**最后一次** `style.css` 改动,四条静态门 + `check-09` 六项 + pytest 基线在本计划收口时全绿;`idi-11-VERIFICATION.md` 的连带作废判定可据此进行。
- **`check-10` 保持全绿**(本计划零改动 `th`,其 `t1` 的 gray-2 字面量断言不受影响)。

---
*Phase: idi-12-g1-band*
*Completed: 2026-09-29*

## Self-Check: PASSED

- FOUND: `frontend/style.css`
- FOUND: `scripts/check-09-idi09-validation.py`
- FOUND: `scripts/ui-states/checking/docs/DESIGN-check-2.md`
- FOUND: `.planning/phases/idi-12-g1-band/idi-12-01-SUMMARY.md`
- FOUND: commit `00bf51b` (Task 1)
- FOUND: commit `39bce0b` (Task 2)
- FOUND: `ITEMS` 含六个键 `c1..c6`;`parse_args()` 仍有且仅有 `--item` / `--screenshot` / `--keep`

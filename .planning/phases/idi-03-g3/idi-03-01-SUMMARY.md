---
phase: idi-03-g3
plan: "01"
subsystem: backend
tags: [g3-gate, authorization, self-check, tier, verdict, pure-functions, tdd]

requires:
  - phase: idi-02-g2
    provides: grammar.py 六条锁定文法解析器 / annotations.select_pending / state.derive_state 八行推导表 / g1.py 后端受控产物写入模子
provides:
  - backend/g3.py: g3_available 四查组合判定 + authorize_write AUTHORIZATION.md 后端写入
  - backend/checks.py: tier 签名文件读写(write/read) + 报告尾部追加三件(待裁决/裁决/PASS)
  - backend/grammar.py 增量: TIER_LINE_STRICT/LOOSE 常量 + parse_tier_line / parse_problem_grades / is_pure_p2 / scan_pending_questions
affects: [idi-03-02, idi-03-03, idi-03-04, idi-03-05, wave-2-session-routes, wave-4-views]

actuals:
  tokens: 11324    # chars/4 over realized diff (45295 chars, 6 files)
  tasks: 3
  commits: 5      # MEASURED: git rev-list --count 3a9d7b5..HEAD
  plan_head_before: 3a9d7b595acbd901fc85c16a038ad199bf60159a

tech-stack:
  added: []        # 零新增第三方依赖(纯标准库 pathlib/re/datetime,禁令守住)
  patterns:
    - 四查组合判定:derive_state 门控 + 单一文档快照复用(读一次文本判四条,D-P3-1)
    - 内容级幂等 vs 同号拒绝:append 族两类幂等形态的分立(§6.4)
    - 正则派生不复制:_PENDING_QUESTION_RE 从 _VERDICT_RE 待裁决分支同风格派生
    - 常量单源:TIER_LINE_STRICT/LOOSE 供 checks 落盘与 Wave 3 prompt 逐字引用

key-files:
  created:
    - backend/g3.py
    - backend/checks.py
    - backend/tests/test_g3.py
    - backend/tests/test_checks.py
  modified:
    - backend/grammar.py
    - backend/tests/test_grammar.py

key-decisions:
  - "g3_available 纯 bool:四查任一不过即 False(理由门控语义);reasons 列表归 Wave 2 路由层(本计划 PATTERNS 开放项择简)"
  - "append 族选「读全文 rstrip + 空行 + 行」整写形态(非 'a' 模式):同轮幂等判定需读现文,整写不增形态分支"
  - "scan_pending_questions 行内代码防御 = strip 后以反引号开头的行跳过(§6.4 写作纪律字面实现,择简)"
  - "is_pure_p2 复用 _last_conclusion_index 判 None(半份 fail-closed),不新建第二锚点判据"

patterns-established:
  - "门文件族第三员:g3.py 照 g1.py 模子(FileExistsError 幂等 + 中文 docstring 引 DESIGN 章节)"
  - "追加不改写正文:_append_line 只接文件尾(T-idi03-03 正文保全有逐字断言用例)"
  - "TDD 双任务 RED→GREEN:骨架 NotImplementedError 占位,RED 证据 = 目标函数断言点失败(照 idi-02-01 先例)"

requirements-completed: [FLOW-05, DATA-04]

coverage:
  - id: D1
    description: "g3_available 四查组合判定(§4.4 权威定义)——合规正例 + 四条污染反例逐条独立 + 非 phase3 三态 + 跨轮不回落"
    requirement: FLOW-05
    verification:
      - kind: unit
        ref: backend/tests/test_g3.py#test_g3_available_all_four_checks_pass 等 8 用例
        status: pass
    human_judgment: false
  - id: D2
    description: "authorize_write AUTHORIZATION.md 写入(项目根两要素 ISO-8601 + 确认授权标记)+ FileExistsError 幂等"
    requirement: FLOW-05
    verification:
      - kind: unit
        ref: backend/tests/test_g3.py#test_authorize_write_two_elements_and_idempotency
        status: pass
    human_judgment: false
  - id: D3
    description: "grammar 四新解析器:parse_tier_line / parse_problem_grades(number int)/ is_pure_p2(半份 fail-closed)/ scan_pending_questions(行内代码防误收)"
    requirement: DATA-04
    verification:
      - kind: unit
        ref: backend/tests/test_grammar.py#test_tier_line_strict_and_loose 等新增 14 用例
        status: pass
    human_judgment: false
  - id: D4
    description: "tier 签名三件:write_tier(白名单+覆盖幂等)/ read_tier(不存在/脏内容 None)"
    requirement: DATA-04
    verification:
      - kind: unit
        ref: backend/tests/test_checks.py#test_write_tier_and_read_back 等 4 用例
        status: pass
    human_judgment: false
  - id: D5
    description: "报告尾部追加三件:待裁决(内容级幂等)/ 裁决(同号 FileExistsError)/ PASS 收口(末行锚点 is_pass_conclusion True 断言)"
    requirement: DATA-04
    verification:
      - kind: unit
        ref: backend/tests/test_checks.py#test_append_user_verdict_and_same_number_reject 等 7 用例
        status: pass
    human_judgment: false
  - id: D6
    description: "既有六条文法锁定语义零触碰(check-14 锁定版只消费)"
    verification:
      - kind: other
        ref: git diff main -- backend/grammar.py(零删除行,纯增量)
        status: pass
    human_judgment: false

duration: 31min
completed: 2026-09-11
status: complete
---

# Phase idi-03 Plan 01: 数据脊柱 Summary

**G3 四查组合判定 + AUTHORIZATION.md 后端写入、tier 档位签名与报告尾部追加族(待裁决/裁决/PASS)、grammar 四新解析器(tier 行/问题分级表/纯 P2/待裁决扫描)——Phase 3 全部上层的纯函数 import 基座,143→176 passed 零失败**

## Performance

- **Duration:** 31 min
- **Started:** 2026-09-11T17:10:51Z
- **Completed:** 2026-09-11T17:42:07Z
- **Tasks:** 3/3
- **Files modified:** 6(4 created + 2 modified)

## Accomplishments

- backend/g3.py:g3_available 四查在同一份当前轮文档快照上判定(D-P3-1 不跨轮;读文档失败 fail-closed),四条「AI 产物污染」反例逐条单测证明「机械校验而非采信 AI 自评」(D-17);authorize_write 项目根两要素落盘 + FileExistsError 幂等(G3 只走一次)
- backend/grammar.py 纯增量四解析器:tier 行三态、问题分级表(number 列 int 化消除裁决卡混型配对隐患)、is_pure_p2 半份 fail-closed(堵 p2 死局态)、scan_pending_questions 从 _VERDICT_RE 派生正则 + 行内代码防误收;既有六条锁定函数体经 git diff 纯增量证明零触碰
- backend/checks.py 六件:tier 签名写读(白名单/脏内容 None 兜底)+ 追加族三件(待裁决内容级幂等/裁决同号拒绝/PASS 收口成为末锚点),三类追加正文逐字保全(T-idi03-03)
- TDD 双任务严格执行 RED→GREEN(Task 2: 4152d41→7fa31ff;Task 3: e029b90→88b86ee),RED 证据全部为目标函数断言点失败(非导入错误)
- 全量回归:143 passed + 4 skipped 基线 → 176 passed + 4 skipped(零失败零跳过新增)

## Task Commits

Each task was committed atomically:

1. **Task 1: g3.py 纯模块(g3_available + authorize_write)** - `c9ce6cf` (feat, tracer)
2. **Task 2: grammar.py 三解析器 + scan_pending_questions** - `4152d41` (test RED) → `7fa31ff` (feat GREEN)
3. **Task 3: checks.py tier 签名 + 报告尾部追加三件** - `e029b90` (test RED) → `88b86ee` (feat GREEN)

**Plan metadata:** (SUMMARY 提交,见下)

## Files Created/Modified

- `backend/g3.py`(NEW)- G3 四查组合判定 g3_available + authorize_write AUTHORIZATION.md 写入(§4.4/§7.4/D-P3-1/2/4)
- `backend/checks.py`(NEW)- write_tier/read_tier 档位签名 + append_pending_question/append_user_verdict/append_pass_conclusion(§8.2/§6.4/D-P3-11/12/17/19)
- `backend/grammar.py`(MOD +99)- TIER_LINE_STRICT/LOOSE 常量、parse_tier_line、parse_problem_grades、is_pure_p2、scan_pending_questions;__all__ 扩六名
- `backend/tests/test_g3.py`(NEW,8 用例)- 四查正例 + 四条污染反例 + 非 phase3 三态 + 跨轮不回落 + 两要素/幂等
- `backend/tests/test_grammar.py`(MOD +14 用例,共 46)- tier 行/问题表/纯 P2/待裁决扫描正反例矩阵
- `backend/tests/test_checks.py`(NEW,11 用例)- tier 三件 + 追加三件 + 正文保全

## Decisions Made

- g3_available 返回纯 bool(非 {available, reasons}):四查任一不过即 False 是门控语义;reasons 列表供前端 title 的需求归 Wave 2 路由层——本计划 PATTERNS.md 开放项"planner 择简"取简
- append 族选「读现文 rstrip + 空行 + 行」整写形态:内容级幂等与同号判定都需读现文,整写不引入第二套文件打开形态(计划 action 两选项择简)
- scan_pending_questions 的行内代码防御 = strip 后以反引号开头的行跳过:§6.4 写作纪律「引用文法样例须置于行内代码」的字面实现,一个显式用例锁定
- is_pure_p2 复用既有 _last_conclusion_index 判 None(半份报告 fail-closed),不新建第二锚点判据(锁定函数只读消费)

## Deviations from Plan

None - plan executed exactly as written.

---

**Total deviations:** 0
**Impact on plan:** n/a

## Issues Encountered

- Task 3 GREEN 周期一处测试侧断言修正:test_append_pending_question 的内容级幂等断言原为「行数 +1」,但计划的追加形态(现文 rstrip + 空行 + 行)会同时补一个空行分隔(行数 +2,§6.4 报告的裁决段空行惯例)。修正为「与首次追加后逐字相同」的字节级断言——行为契约(内容级幂等)不变,断言语义更严;修正发生在 GREEN 循环内、feat 提交(88b86ee)之前,非计划偏离

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Wave 2(session/routes)可直接 import:g3_available/authorize_write(POST /api/authorize:先 derive_state==phase3 + g3_available 再查 → authorize_write,FileExistsError → 409);checks.write_tier/read_tier(POST /api/checks/tier);checks.append 族(POST /api/checks/verdict 同号 409)
- Wave 3(prompts)逐字消费 TIER_LINE_STRICT/TIER_LINE_LOOSE 与问题表头字面(| 编号 | 级别 | 位置 | 问题 | 建议修法 |)——两端同字面是 D-P3-29 硬要求,常量已就位
- 既有六条文法锁定语义零触碰已由 git diff 证明;state.py 零改动(本计划未触碰)
- 无阻塞项;基线 176 passed + 4 skipped 可作为后续计划回归锚

## Self-Check: PASSED

- [x] backend/g3.py / backend/checks.py / backend/tests/test_g3.py / backend/tests/test_checks.py 存在于盘
- [x] 5 个任务提交全部在 git log(c9ce6cf / 4152d41 / 7fa31ff / e029b90 / 88b86ee)
- [x] 三个任务 acceptance criteria 全数复跑通过(见各任务执行日志)
- [x] 全量回归 176 passed + 4 skipped(基线 143 只增不减)
- [x] STATE.md / ROADMAP.md / REQUIREMENTS.md 零改动(git status 空)

---
*Phase: idi-03-g3*
*Completed: 2026-09-11*

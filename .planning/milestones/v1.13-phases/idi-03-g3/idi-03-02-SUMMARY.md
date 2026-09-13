---
phase: idi-03-g3
plan: "02"
subsystem: backend
tags: [g3-authorization, writing-tmp-rename, self-check-loop, tier, verdict, snap-pass, routes, session]

requires:
  - phase: idi-03-g3-01
    provides: g3.py g3_available/authorize_write + checks.py write_tier/read_tier/append 族 + grammar.py parse_tier_line/parse_problem_grades/is_pure_p2/scan_pending_questions + TIER_LINE_STRICT/LOOSE 常量
provides:
  - backend/session.py: authorize() / set_tier() / verdict_append()(含 _residue_cleared 收口)/ start_writing()(tmp 原子改名)/ start_check()(循环驱动)/ start_repair()(抛问截存,auto 参数双门)/ writing_available / check_available / repair_available / _next_check_n / _drive_next / _selfcheck_substate(快照伪层)
  - backend/prompts.py: build_writing_prompt / build_check_prompt / build_repair_prompt 三族四段 prompt + _WRITING_INSTRUCTIONS / _CHECK_GRAMMAR_EXAMPLES / _CHECK_INSTRUCTIONS / _REPAIR_INSTRUCTIONS
  - backend/main.py: POST /api/authorize(无请求体)、POST /api/checks/tier、POST /api/checks/verdict、GET /api/design、GET /api/checks 五路由 + TierBody/VerdictBody
  - _session_snapshot 新字段: g3_available / writing_tmp_exists / selfcheck({tier, mode, questions})
affects: [idi-03-03, idi-03-04, idi-03-05, wave-3-routes, wave-4-views, wave-5-e2e]

actuals:
  tokens: 28852    # chars/4 over realized diff (115410 chars, 6 files)
  tasks: 3
  commits: 3      # MEASURED: git rev-list --count faf8079..HEAD
  plan_head_before: faf8079261e446ccedef667b7f97fc3f2fb046ee

tech-stack:
  added: []        # 零新增第三方依赖(纯 pathlib/threading/标准库,禁令守住)
  patterns:
    - done-回调直排:else 分支不自调,finally 解锁后由 _drive_next 外层 wrapper 串调下一跳(单飞锁不死锁,D-P3-16 定案形态)
    - 用户门与自动链分立:start_repair(auto) 双门——用户按钮走判定式②;自动链只重验 phase5_checking + 无未配对待裁决(§8.2 两跳自动与 D-P3-20 互斥的调和)
    - 残余清零双源判定:_residue_cleared 用问题表编号 ∪ 待裁决编号 ⊆ 裁决编号(纯 P2 残余与修复者抛问两源同一配对式)
    - 快照伪层组装:selfcheck 子状态经 _selfcheck_substate 组装,不新增 derive_state 值(D-P3-23)

key-files:
  created: []
  modified:
    - backend/session.py
    - backend/prompts.py
    - backend/main.py
    - backend/tests/test_session.py
    - backend/tests/test_ai_caller.py
    - backend/tests/test_route_session.py

key-decisions:
  - "start_repair(auto: bool) 参数化双门:用户「继续修复」走 repair_available 判定式②;严格档自动链(check-done 后)走 auto 分支只重验 phase5_checking + 无未配对——否则报告刚落盘的 running 态(无裁决行)会拒掉第一跳自动修复,§8.2 两跳自动与 D-P3-20 互斥不可两全时按 §8.2 字面调和"
  - "抛问截存扫描源 = say 事件流(\\n join)+ 当轮报告文本先流后文本(D-P3-18 两者都扫;报告文本兜底覆盖修复者把抛问写进报告正文的形态);截存后 unpaired_verdicts 非空天然断链,无需独立标志位"
  - "_next_check_n 半份判定 = 报告全文无 `> 核查结论:` 行(复用 is_pure_p2 的锚点语义但独立判 None):半份 → 同轮覆盖重跑不跳号,完整 → max+1(D-P3-21 字面)"
  - "verdict_append 的状态门在先、同号扫描在后:收口(PASS 追加 → mission_complete)后再裁决命中「仅自检进行中可裁决」409,同号 FileExistsError 用双待裁决盘独立用例证明(单问题盘收口后状态门先拦是既定契约)"
  - "route 测试的盘态隔离:_reenter_fresh_route 以全新子目录重进(旧盘 AUTHORIZATION/DESIGN/报告残留会把 phase3 场景顶成 phase4+),避免共享 tmp_path 的盘态污染"

patterns-established:
  - "第 4/5/6 次复制 process_round 模子:入口三查 + _worker + SSE + done-else + finally 解锁;start_writing 是最贴形复刻,check/repair 的 finally 尾部多出驱动串调"
  - "检查者/修复者 prompt 用『写入 docs/DESIGN-check-N.md』锚定目标编号(测试 fake 解析同一锚点,不取资料段的既有报告文件名)"
  - "TestClient 造盘 helper 族(_enter_phase3_compliant/_enter_phase4/_enter_phase5 + route 侧同构副本)在 session 与 route 两测试文件各持一份,避免跨文件 import 测试态"

requirements-completed: [FLOW-05, DATA-02, DATA-04]

coverage:
  - id: D1
    description: "G3 授权链:authorize() 服务端四查再查(D-P3-4 防绕过)→ AUTHORIZATION.md 落盘 → state=phase4;已授权幂等 False/409"
    requirement: FLOW-05
    verification:
      - kind: unit
        ref: backend/tests/test_session.py#test_authorize_accepts_and_persists
        status: pass
      - kind: integration
        ref: backend/tests/test_route_session.py#test_route_authorize_all_branches(200/409/409 幂等三分支)
        status: pass
    human_judgment: false
  - id: D2
    description: "撰写链:start_writing WritingFake 写 tmp → done 后 Path.replace 原子改名 → DESIGN.md + state=phase5_awaiting_tier;tmp 缺失 error 事件可重跑"
    requirement: DATA-02
    verification:
      - kind: unit
        ref: backend/tests/test_session.py#test_start_writing_closes_loop / test_start_writing_error_when_no_tmp / test_start_writing_entry_rejects
        status: pass
    human_judgment: false
  - id: D3
    description: "build_writing_prompt:全量完整轮 + 各轮批注 + _KNOWN_DOCS 资料段,绝不读 tmp/AUTHORIZATION.md(D-P3-9);DESIGN.md.tmp 落盘指令 + 直写明禁逐字"
    requirement: DATA-02
    verification:
      - kind: unit
        ref: backend/tests/test_session.py#test_build_writing_prompt_contains_materials / test_build_writing_prompt_excludes_tmp_and_auth
        status: pass
    human_judgment: false
  - id: D4
    description: "选档/裁决同步三件:set_tier(phase5_awaiting_tier 门 + 白名单 ValueError)、verdict_append(同号 FileExistsError + _residue_cleared 双源收口 → append_pass_conclusion)"
    requirement: DATA-04
    verification:
      - kind: unit
        ref: backend/tests/test_session.py#test_set_tier_accepts_and_rejects / test_verdict_append_persists_and_closes / test_verdict_append_same_number_rejects
        status: pass
      - kind: integration
        ref: backend/tests/test_route_session.py#test_route_tier_all_branches / test_route_verdict_all_branches
        status: pass
    human_judgment: false
  - id: D5
    description: "严格档两跳自动驱动全链:check-1(P1)→ repair(恰好 1 次)→ check-2(纯 P2)→ 停残余裁决;PASS 报告 done 后零修复跳;无 scheduler(AST 级验证)"
    requirement: DATA-04
    verification:
      - kind: unit
        ref: backend/tests/test_session.py#test_start_check_two_hop_chain(2 报告 1 修复)/ test_start_check_pass_stops
        status: pass
    human_judgment: false
  - id: D6
    description: "抛问截存暂停:RepairFake say 事件含 > 待裁决: → 报告尾部截存行 + 无下一跳推广(check 计数不增);续跑 verdict → start_repair resumed 态 prompt 含裁决行"
    requirement: DATA-04
    verification:
      - kind: unit
        ref: backend/tests/test_session.py#test_start_check_pending_question_intercepts / test_resume_after_verdict
        status: pass
    human_judgment: false
  - id: D7
    description: "check/repair prompt 与 grammar 两端一字不差:问题表头 / TIER_LINE 常量 / 结论行 PASS/FIX 正反例 / 抛问协议行内代码纪律逐字注入(D-P3-29)"
    requirement: DATA-04
    verification:
      - kind: unit
        ref: backend/tests/test_session.py#test_build_check_prompt_three_sections / test_build_check_prompt_multi_round_trend / test_build_repair_prompt_contains
        status: pass
    human_judgment: false
  - id: D8
    description: "半份自愈不跳号(D-P3-21):半份盘(报告缺结论行)重跑同轮覆盖(_next_check_n 返回 max);完整盘取 max+1"
    requirement: DATA-04
    verification:
      - kind: unit
        ref: backend/tests/test_session.py#test_next_check_n_half_report_no_skip
        status: pass
    human_judgment: false
  - id: D9
    description: "repair_available 三态互斥(D-P3-20):running(报告刚落盘无裁决行)False / 判定式②(配对裁决 + 非_PASS)True / paused(unpaired 非空)False / 纯 P2 False——「继续修复」单一路径放行"
    requirement: DATA-04
    verification:
      - kind: unit
        ref: backend/tests/test_session.py#test_repair_available_three_states
        status: pass
    human_judgment: false
  - id: D10
    description: "权限矩阵零改动消费:AI 写 AUTHORIZATION.md → reject 断言在位(Specific Ideas 红线);tmp 写入 allow"
    requirement: FLOW-05
    verification:
      - kind: unit
        ref: backend/tests/test_ai_caller.py#test_permission_authorization_md_reject / test_permission_tmp_allow
        status: pass
    human_judgment: false
  - id: D11
    description: "snapshot 扩展:g3_available(phase3 四查)/ writing_tmp_exists(phase4 tmp 二态)/ selfcheck 五 mode(running/paused/resumed/p2/done)+ awaiting_tier tier 恢复;既有字段零删除(git diff 证明)"
    requirement: DATA-04
    verification:
      - kind: integration
        ref: backend/tests/test_route_session.py#test_route_snapshot_g3_available / test_route_snapshot_writing_tmp_exists / test_route_snapshot_selfcheck_paused / test_route_snapshot_selfcheck_p2 / test_route_snapshot_selfcheck_half_p2_running / test_route_snapshot_selfcheck_resumed_running_done
        status: pass
    human_judgment: false
  - id: D12
    description: "GET /api/design(全文 / null)+ GET /api/checks(编号列表 + latest 全文 + selfcheck 透传)两路由契约固定(Wave 4 唯一数据源)"
    requirement: DATA-02
    verification:
      - kind: integration
        ref: backend/tests/test_route_session.py#test_route_design / test_route_checks
        status: pass
    human_judgment: false
  - id: D13
    description: "真 CLI 的撰写/自检全链(真实 tmp 改名、两跳循环)未在本计划跑——归 idi-03-04 的 IDI_E2E 门控用例(计划 verification 第 4 条明示)"
    requirement: FLOW-05
    verification: []
    human_judgment: true
    rationale: "Fake 级全链已证(单元);真实调用链的节奏与产物形态需 idi-03-04 E2E 门控验证,非本层可自动化判定"

duration: 686min
completed: 2026-09-12
status: complete
---

# Phase idi-03 Plan 02: 后端全层 Summary

**G3 授权入口(四查服务端再查→AUTHORIZATION.md)与撰写 tmp 原子改名流水线、检查者/修复者两角色 prompt 族、严格档两跳自动循环引擎(done-回调直排 + 抛问截存暂停 + 半份不跳号)、选档/裁决同步落盘与残余收口、快照 selfcheck 子状态 + 5 条新路由(authorize/tier/verdict 三 POST + design/checks 两 GET)——176→209 passed 零失败**

## Performance

- **Duration:** 686 min(含中断恢复与会话切换;净执行三任务)
- **Completed:** 2026-09-12T05:26:27Z
- **Tasks:** 3/3
- **Files modified:** 6(0 created + 6 modified)
- **Tokens (actuals):** 28,852(chars/4 over 115,410 diff chars)

## Accomplishments

- backend/session.py:authorize()/set_tier()/verdict_append() 同步三件(busy 防漂移、FileExistsError 供 409、_residue_cleared 双源收口判 D-P3-17「全部处理完即收敛收口」);start_writing() 复刻 process_round 模子,done-else 用 Path.replace 同 inode 原子改名 tmp→DESIGN.md(改名前不校验内容,D-P3-8),tmp 缺失 error 事件留 phase4 可重跑
- 循环引擎:check_available/repair_available/{}三入口判定(_next_check_n 半份判定同轮覆盖不跳号 D-P3-21)、start_check 的 done-else 三分支(PASS 停 / 纯 P2 停 / 其余 finally 解锁后 _drive_next 串调修复)、start_repair 的抛问扫描先流后文本 → append_pending_question 截存 + 不推进;外层 wrapper 形态:else 不自调、finally 后串调(AST 级验证无 scheduler/Timer/轮询)
- backend/prompts.py:三族四段 prompt 与常量(_WRITING_INSTRUCTIONS 落盘指令 + 直写明禁;_CHECK_GRAMMAR_EXAMPLES 逐字:问题表头、TIER_LINE 常量字面、结论行 PASS/FIX 正反例、裁决追加行内代码纪律;_REPAIR_INSTRUCTIONS 抛问协议 + 宽松档 PASS 特例)——prompt 与 grammar 两端一字不差(D-P3-29)
- backend/main.py:五路由(authorize 无请求体防 FastAPI 422、tier 白名单 400、verdict 同号 409、design 全文、checks 组装;writing/start/repair 三条 202 归 idi-03-03 未建——app.routes 级证明)
- 测试:三文件扩 33 用例(session 21 + ai_caller 2 + route 11),全量 176+4 → 209+4(零失败)

## Task Commits

Each task was committed atomically:

1. **Task 1: authorize()/set_tier()/verdict_append() + build_writing_prompt + start_writing(tmp 原子改名)+ 三 POST 路由** - `c9fb63c` (feat)
2. **Task 2: build_check_prompt/build_repair_prompt + start_check/start_repair 循环引擎(done-回调直排 + 抛问截存)+ AUTHORIZATION reject 断言** - `48fc89d` (feat, tracer)
3. **Task 3: snapshot 扩三字段 + GET /api/design + GET /api/checks + 路由级全分支用例** - `110f5b8` (feat)

**Plan metadata:**(SUMMARY 提交,见下)

## Files Created/Modified

- `backend/session.py`(MOD,+~690)- 授权/选档/裁决同步三件 + writing/check/repair 三流水线 + 入口判定四件 + _next_check_n/_drive_next/_residue_cleared/_selfcheck_substate + 快照三新字段
- `backend/prompts.py`(MOD,+400)- build_writing_prompt / build_check_prompt / build_repair_prompt + 四常量组(_WRITING_INSTRUCTIONS / _CHECK_GRAMMAR_EXAMPLES / _CHECK_INSTRUCTIONS / _REPAIR_INSTRUCTIONS)
- `backend/main.py`(MOD,+115)- POST /api/authorize、/api/checks/tier、/api/checks/verdict + GET /api/design、/api/checks + TierBody/VerdictBody
- `backend/tests/test_session.py`(MOD,+21 用例)- WritingFake/CheckWritingFake/RepairWritingFake/DualRoleFake/_enter_phase3_compliant/_enter_phase4/_enter_phase5/_check_report 族
- `backend/tests/test_ai_caller.py`(MOD,+2 用例)- AUTHORIZATION.md reject + tmp allow 断言
- `backend/tests/test_route_session.py`(MOD,+11 用例)- 路由级盘造 helper 族 + snapshot/authorize/tier/verdict/design/checks 全分支

## Decisions Made

- **start_repair(auto: bool) 双门参数**(最大设计判断):计划 must_haves 的「repair 入口 = 判定式②双条件」与 D-P3-16「check done 后自动链入 start_repair」在首跳自动修复冲突——报告刚落盘(running 态无裁决行)被判定式②拒绝。调和:用户按钮(auto=False)走判定式②;严格档自动链(auto=True)只重验 phase5_checking + 无未配对待裁决。§8.2「两跳均后端自动,无需用户点击」是字面契约,判定式②互斥的本意是「用户不误点重跑」(check-10),不是卡自动链
- 抛问扫描源取 say 流 + 当轮报告文本(先流后文本):计划行为条目说「say 事件流 + 最终文本」,报告文本兜底覆盖修复者把 `> 待裁决:` 写进报告正文的形态;截存后 unpaired_verdicts 非空是驱动链天然断点,无需自建标志位
- 路由测试的盘态污染用 _reenter_fresh_route(全新子目录)解决:共享 tmp_path 时 phase4/5 的 AUTHORIZATION/DESIGN/报告残留会把后续 phase3 场景顶到 phase4+(derive_state 行 4 命中),单一 reset 不够
- verdict_append 状态门(仅 phase5_checking)先于同号扫描:收口后重复裁决命中「仅自检进行中可裁决」(同为 409);同号 FileExistsError 在双待裁决盘独立用例证明——两 plan 字面各自成立

## Deviations from Plan

**1. [Rule 1 - Bug] start_repair 自动链首跳被自身入口门拒绝**
- **Found during:** Task 2(两跳链用例:repair_calls == 0)
- **Issue:** 计划把 start_repair 入口定为 repair_available 双条件(判定式②),但严格档自动链发生在报告刚落盘的 running 态(无裁决行)→ 第一跳自动修复被 409 语义拒掉,§8.2 两跳自动断链
- **Fix:** start_repair(auto: bool = False) 双门——用户按钮走判定式②(计划原义);_drive_next 串调 auto=True 分支只重验 phase5_checking + 无未配对待裁决
- **Files modified:** backend/session.py
- **Verification:** test_start_check_two_hop_chain(2 报告恰 1 修复)全绿
- **Commit:** 48fc89d

**2. [Rule 3 - Blocker] 临时测试设施问题(非产品缺陷,GREEN 循环内修正)**
- **Found during:** Task 1/2 GREEN 循环
- **Issue:** ①set_tier/verdict 用例在共享 tmp_path 重进 phase3 时,残留 AUTHORIZATION/DESIGN 顶掉目标态;②DualRoleFake 用正则取 prompt 首个 DESIGN-check-N.md 文件名,误把资料段「既有报告」标题当目标编号;③testVerifier 单问题盘收口后同号断言命中状态门
- **Fix:** 全部测试侧修正(子目录重进 / `_target_check_n` 取「写入 docs/DESIGN-check-N」锚 / 同号 FileExistsError 用双待裁决盘独立用例),产品代码契约未动
- **Files modified:** backend/tests/test_session.py, backend/tests/test_route_session.py
- **Verification:** 全量 209 passed + 4 skipped
- **Commit:** c9fb63c / 48fc89d / 110f5b8

---

**Total deviations:** 2 auto-fixed(Rule 1 × 1,Rule 3 测试设施 × 1)
**Impact on plan:** start_repair 的 auto 参数是实现形态微调(计划未预见两字面冲突);行为契约(两跳自动、判定式②用户门、互斥)全部保持,假级全链证明

## Issues Encountered

- 执行中断一次(API 503 后恢复,续接 agent 确认磁盘状态无丢失);期间一个红灯用例(test_verdict_append 收口后状态门先拦)由续接诊断正确归类为测试侧断言问题,按其建议以双待裁决盘独立用例覆盖同号 FileExistsError 一字面
- Task 2 tracer gate:verify 重跑全绿后放行 Task 3(AUTO 模式,无人检项)

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- idi-03-03(wave 3)可直接建 POST /api/writing、/api/checks/start、/api/checks/repair 三条 202 受理路由:session 层 start_writing/start_check/start_repair 三函数已交付(入口三查已定,路由层照 /api/rounds/process 模子);错误消息字面表已落码(「撰写入口已关闭…「自检入口已关闭…「修复入口已关闭…在本计划 session docstring/主 409 分支)
- Wave 4(idi-03-04)可按三契约渲染:/api/session(g3_available/writing_tmp_exists/selfcheck 子状态 mode-driven 视图)、/api/design、/api/checks;p2 裁决卡键集 {number, location, issue, suggestion} 与 paused 卡 {number, text} 已锁
- idi-03-05 E2E:真 CLI 撰写/自检全链(真实 tmp 改名、两跳循环节奏)按计划在该用例门控验证
- 基线:209 passed + 4 skipped(只增不减)

## Self-Check: PASSED

- [x] backend/session.py / backend/prompts.py / backend/main.py / backend/tests/test_session.py / backend/tests/test_ai_caller.py / backend/tests/test_route_session.py 存在于盘
- [x] 三个任务提交全部在 git log(c9fb63c / 48fc89d / 110f5b8)
- [x] 三个任务 acceptance criteria 全数复跑通过(含 advisory-2 的 grep ≥ 4 阈值:实际 5 行,其中 4 行为路由命中)
- [x] advisory-1 守住:authorize/tier/verdict + design/checks 恰 5 条;writing/start/repair 零注册(app.routes 遍历证明)
- [x] 全量回归 209 passed + 4 skipped(基线 176+4 只增不减)
- [x] STATE.md / ROADMAP.md / REQUIREMENTS.md 零改动(本 SUMMARY 为唯一 .planning 写入)

---
*Phase: idi-03-g3*
*Completed: 2026-09-12*

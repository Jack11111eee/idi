---
phase: idi-03-g3
plan: "03"
subsystem: backend
tags: [routes, writing-entry, selfcheck-repair, process-template, d-p3-27, route-acceptance]

requires:
  - phase: idi-03-g3-02
    provides: session.start_writing/start_check/start_repair(True/False/RuntimeError 语义)+ writing_available/check_available/repair_available 三入口判定 + authorize/tier/verdict 三 POST + design/checks 两 GET 路由 + build_writing/check/repair_prompt 三族
provides:
  - backend/main.py: POST /api/writing、POST /api/checks/start、POST /api/checks/repair 三条 202 受理路由(分支逐字照 /api/rounds/process 模子;无请求体无 Body 类;路由层零判定透传 session)——与 Wave 2 五条合成 D-P3-27 全量八条路由族
  - backend/tests/test_route_session.py: writing/start/repair 三路由 202/409/400 全分支 + 三入口 busy 互斥共 7 用例(FakeAICaller route 环境复用,受理后 wait_route_idle 收流)
affects: [idi-03-04, idi-03-05, wave-4-views, wave-5-e2e, milestone-close]

actuals:
  tokens: 3845     # chars/4 over realized diff (15382 chars, 2 files)
  tasks: 1
  commits: 2       # MEASURED: git rev-list --count 9333927..HEAD
  plan_head_before: 933392771739a83d8c56887db78d8190a604eb5b

tech-stack:
  added: []        # 零新增依赖(纯 FastAPI 路由接线,禁令守住)
  patterns:
    - 三受理路由照 /api/rounds/process 模子的第五次复制:try RuntimeError→400 / False→409(字面表消息)/ True→202 {"status":"accepted"}
    - 无请求体 POST 路由直接 @app.post 无 Body 类(照 /api/authorize 先例,防 FastAPI 422)
    - RED→GREEN 两段式:route 用例先落(405/404 证缺失)→ 路由注册后同用例全绿

key-files:
  created: []
  modified:
    - backend/main.py
    - backend/tests/test_route_session.py

key-decisions:
  - "三条路由 409 消息逐字采用 Wave 2 错误消息字面表(「撰写入口已关闭(非阶段 4 或当前有调用进行中)」/「自检入口已关闭(非自检阶段或当前有调用进行中)」/「修复入口已关闭(无待修问题或当前有调用进行中)」)——False 不带原因,前端按 state 呈现"
  - "check-start 202 用例取「无报告 + tier 签名」盘:Fake 不产报告 → done 后 latest 空 → 驱动链不排下一跳,单跳确定性收尾(报告文法链归 session 级已测);repair 202 用例取宽松档 resumed 盘:finally 尾 tier==宽松 提前返回,恰一次调用"
  - "RED 用 405(FastAPI 未匹配 POST)作缺失证明——intentional-RED 证据落在 test 提交 9c598ed,7 用例全失败而既有 21 用例全绿"

patterns-established:
  - "受理路由(无请求体 POST)的 process 模子定版:三行 session 调用 + except RuntimeError 400 + if not accepted 409 + return 202,路由体永不出现 derive_state/available 判定"
  - "route 环境的盘态互斥用 _reenter_fresh_route(全新子目录)复用 Wave 2 形态;busy 互斥用 HangingFake gate/release(挂起 send_message 在飞,断言三入口 409 且不另起调用)"

requirements-completed: [FLOW-05, DATA-04]

coverage:
  - id: D1
    description: "POST /api/writing 三分支路由:phase4 造盘 + Fake 写 tmp → 202 {status:accepted}(done 后 tmp 改名 DESIGN.md);非 phase4(phase3 造盘)→ 409;busy 在飞 → 409 且不另起调用;未进项目 → 400"
    requirement: FLOW-05
    verification:
      - kind: integration
        ref: backend/tests/test_route_session.py#test_route_writing_accepted / test_route_writing_409_non_phase4_and_busy / test_route_writing_400_without_project
        status: pass
    human_judgment: false
  - id: D2
    description: "POST /api/checks/start:phase5_awaiting_tier + tier 签名 → 202(单跳恰一次调用);无 tier 签名 → 409(check_available False 透传,T-idi03-12 服务端强制);未进项目 → 400"
    requirement: DATA-04
    verification:
      - kind: integration
        ref: backend/tests/test_route_session.py#test_route_check_start_accepted_and_409 / test_route_check_repair_400_without_project(start 分支)
        status: pass
    human_judgment: false
  - id: D3
    description: "POST /api/checks/repair:判定式②盘(配对裁决 + 末行非 PASS)→ 202 宽松档单跳收尾;phase5_awaiting_tier → 409;unpaired 待裁决非空(paused)→ 409(判定式①服务端强制,T-idi03-13);未进项目 → 400"
    requirement: DATA-04
    verification:
      - kind: integration
        ref: backend/tests/test_route_session.py#test_route_check_repair_accepted_and_409s / test_route_check_repair_400_without_project
        status: pass
    human_judgment: false
  - id: D4
    description: "三受理路由 busy 互斥(单飞锁,多窗口同点只有一个被受理,D-P3-26):挂住在飞调用时 /api/checks/start 与 /api/checks/repair 同 409 且不另起调用(writing busy 409 在 D1 用例内证)"
    requirement: FLOW-05
    verification:
      - kind: integration
        ref: backend/tests/test_route_session.py#test_route_three_entries_busy_mutex
        status: pass
    human_judgment: false
  - id: D5
    description: "prompts.py 三族核对确认:build_writing_prompt / build_check_prompt / build_repair_prompt 全部已在 Wave 2 交付(grep 393/549/661 行全命中)——本计划零改动(git diff --stat 空)"
    requirement: DATA-04
    verification:
      - kind: other
        ref: "grep -n 'def build_writing_prompt|def build_check_prompt|def build_repair_prompt' backend/prompts.py → 3/3 命中;git diff 9333927..HEAD --stat -- backend/prompts.py → 零输出"
        status: pass
    human_judgment: false
  - id: D6
    description: "真 CLI 按钮链(浏览器点「撰写总设计文档」/「继续自检」/「继续修复」→ SSE 流 → done 拉新)与 mission_complete 归档视图——归 idi-03-04 前端挂接与 idi-03-05 E2E 门控用例验证"
    requirement: FLOW-05
    verification: []
    human_judgment: true
    rationale: "路由级受理/拒绝分支已自动化证明;真实浏览器交互链与 Wave 4 视图联动需前端挂接后 E2E/UAT 层验证,非本层可自动化判定"

duration: 68min
completed: 2026-09-13
status: complete
---

# Phase idi-03 Plan 03: 路由补口 Summary

**D-P3-27 八条路由族收口:POST /api/writing、/api/checks/start、/api/checks/repair 三条 202 受理路由照 /api/rounds/process 模子接线(路由层零判定透传 session)+ 7 条 route 级全分支用例——209→216 passed 零失败,prompts.py 零改动确认**

## Performance

- **Duration:** 68 min(净执行;会话跨中断恢复一次,磁盘状态无丢失)
- **Completed:** 2026-09-13T09:13:43Z
- **Tasks:** 1/1
- **Files modified:** 2(0 created + 2 modified)
- **Tokens (actuals):** 3,845(chars/4 over 15,382 diff chars;计划估 45,000——实际为纯接线,prompts 三族 Wave 2 已全交付零补齐,偏差主因)

## Accomplishments

- backend/main.py:三条受理路由落在 Wave 2「阶段 3/4/5 路由族」分节内(479/502/524 行),分支逐字照 /api/rounds/process:try RuntimeError → 400(未进项目)/ False → 409(字面表消息)/ True → 202 {"status":"accepted"};三条均无请求体无 Body 类(照 /api/authorize 先例);路由体内零 derive_state/check_available/repair_available/writing_available 调用(判定全在 session 层,D-P3-27 与 prohibition 双重申明的 grep 证明)
- backend/tests/test_route_session.py:7 用例(writing 202 / 409×2 / 400;start 202+409;repair 202+409×2+400;三入口 busy 互斥),FakeAICaller 模式 route 环境复用(WritingFake 写 tmp、NoReportFake 单跳、RepairFake 宽松档、HangingFake gate/release);RED 先行提交(405 缺失证明)→ GREEN 全绿
- 八路由族清单核对(见下表):本计划交付 3 条 + Wave 2 已交付 5 条核对确认,D-P3-27 路由契约完整性收口,Wave 4 前端可按八条契约开发

## Task Commits

Each task was committed atomically:

1. **Task 1: 三条受理路由 + route 全分支用例** - `9c598ed` (test,RED:7 用例因路由缺失全失败,既有 21 用例全绿)
2. **Task 1(GREEN): 路由注册** - `aad7f15` (feat,三路由落分节 + 字面表消息)

**Plan metadata:**(本 SUMMARY 提交,见下)

## Files Created/Modified

- `backend/main.py`(MOD,+71/-3)- POST /api/writing、/api/checks/start、/api/checks/repair 三条路由 + 分节注释更新(归 idi-03-03 的三条移出备注改为已交付归属)
- `backend/tests/test_route_session.py`(MOD,+258)- 7 用例 + _wait_route_idle helper + 四个 route 环境 Fake(WritingFake/NoReportFake/RepairFake/HangingFake)
- `backend/prompts.py`(**零改动,核对确认**)- build_writing_prompt(393 行)/ build_check_prompt(549 行)/ build_repair_prompt(661 行)三族全部 Wave 2 已交付,grep 全命中,git diff --stat 空输出

## 八路由清单核对表(D-P3-27 完整性收口,计划 verification 第 2 条)

| # | 路由 | 方法 | 负责人计划 | 状态 | 证明 |
|---|------|------|-----------|------|------|
| 1 | /api/authorize | POST(无请求体) | idi-03-02 Task 1 | 已交付 | test_route_authorize_all_branches(200/409/409) |
| 2 | /api/checks/tier | POST | idi-03-02 Task 1 | 已交付 | test_route_tier_all_branches(200/400/409) |
| 3 | /api/checks/verdict | POST | idi-03-02 Task 1 | 已交付 | test_route_verdict_all_branches(200/409/409/400) |
| 4 | /api/design | GET | idi-03-02 Task 3 | 已交付 | test_route_design(200 全文 / null) |
| 5 | /api/checks | GET | idi-03-02 Task 3 | 已交付 | test_route_checks(列表 + latest + selfcheck) |
| 6 | /api/writing | POST(无请求体) | **idi-03-03(本计划)** | **已交付** | test_route_writing_accepted / _409_non_phase4_and_busy / _400_without_project |
| 7 | /api/checks/start | POST(无请求体) | **idi-03-03(本计划)** | **已交付** | test_route_check_start_accepted_and_409(202/409)+ 400 分支 |
| 8 | /api/checks/repair | POST(无请求体) | **idi-03-03(本计划)** | **已交付** | test_route_check_repair_accepted_and_409s / _400_without_project + busy 互斥 |

八条全部就位:D-P3-27 路由族完整,Wave 4(idi-03-04)前端视图有固定接口可挂接。

## Decisions Made

- **三条 409 消息逐字采用 Wave 2 错误消息字面表**(撰写/自检/修复入口已关闭三条)——不自由发挥文案,False 不带原因由前端按 state 呈现,route 层消息即分流依据
- **check-start 202 用例的盘态选择**:无报告 + tier 签名盘( Fake 不产报告 → latest 空 → 驱动链不排下一跳,单跳确定性);repair 202 用例取宽松档 resumed 盘(finally 尾 tier==宽松 提前返回,恰一次调用)——避免在 route 层重度收流验证事件链(事件链归 session 级已测,本处断言受理码与 409 分支即可,计划 action 第 3 条字面)
- **RED 证明取 405**(FastAPI 未匹配 POST 而非 404):intentional-RED 证据 = test 提交 9c598ed 上 7 用例全失败(405/404)、既有 21 用例全绿——路由缺失是唯一失败原因

## Deviations from Plan

None - plan executed exactly as written.

(prompts.py 预期零改动的核对结果为「确认零缺」:三族 grep 393/549/661 全命中,无 Wave-2 缺口需补齐,故无 Rule 2 补齐偏差;计划 objective 预留的「已存在则仅核对」分支成立)

## Issues Encountered

- 执行中断一次(429 限流后恢复):续接前核对磁盘状态——分支 clean、9333927 基线、无提交丢失、grep 无 Wave-2 负向断言测试(app.routes 枚举证明仅在 plan 02 执行期进行,未持久化为用例,无 reconciliations 需求)——按原计划续跑,零返工

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- idi-03-04(wave 4 前端):八条路由契约全部就位可挂接——阶段 3 视图(g3_available 授权按钮 + 确认词模态 → POST /api/authorize;拒绝 → 普通批注通道)、phase4 撰写按钮(writing_tmp_exists 二态文案 → POST /api/writing)、phase5_awaiting_tier 档位模态(→ POST /api/checks/tier)、phase5_checking 报告视图 + 继续/裁决控件(POST /api/checks/start、/api/checks/repair、/api/checks/verdict;p2 裁决卡 {number, location, issue, suggestion} 与 paused 卡 {number, text})、mission_complete 归档视图(GET /api/design、/api/checks、/api/session)——挂点 applySessionGates else 分支(D-P3-28)
- idi-03-05(wave 5 E2E):真 CLI 撰写/自检全链按计划在 IDI_E2E 门控用例验证(D13 coverage 项)
- 基线:216 passed + 4 skipped(本计划前 209+4,只增不减守住)

## Self-Check: PASSED

- [x] backend/main.py / backend/tests/test_route_session.py 修改在盘;backend/prompts.py 零改动(git diff --stat 空)
- [x] 两任务提交在 git log(9c598ed RED / aad7f15 GREEN)
- [x] Task 1 acceptance criteria 六条全数复跑:AC1 三装饰器 479/502/524 各 ≥1 命中且归 364 行分节;AC2 路由体判定函数 0 调用;AC3 202 响应体 accepted 三处断言;AC4 409 分支(非 phase4/无 tier/非 checking/unpaired/busy)用例全覆盖;AC5 prompts 三族 grep 全命中;AC6 全量 216 passed 零失败
- [x] 计划 fails_when 三条全过:pytest 无 failed/error;新用例 grep 计 6 ≥ 计划阈值(writing 3 + start 1 + repair 2 前缀命名,共 7 个测试函数含 busy 互斥);全量 216 ≥ 143
- [x] STATE.md / ROADMAP.md / REQUIREMENTS.md 零改动(本 SUMMARY 为唯一 .planning 写入;settings.local.json 的 M 为执行环境扰动非本计划产物,未纳入提交)

---
*Phase: idi-03-g3*
*Completed: 2026-09-13*

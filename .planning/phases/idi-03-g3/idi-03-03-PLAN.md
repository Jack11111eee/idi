---
phase: idi-03
plan: 03
type: execute
wave: 3
depends_on: ["idi-03-02"]
files_modified:
  - backend/prompts.py
  - backend/main.py
  - backend/tests/test_route_session.py
autonomous: true
requirements:
  - FLOW-05
  - DATA-04

estimate:
  tokens: 45000
  raw_tokens: 45000
  tasks: 1
  confidence: low

must_haves:
  truths:
    - "main.py 五条缺失路由按 Wave 2 已定的 session 契约补齐:POST /api/writing(202 受理 / busy 或非 phase4 → 409 / 未进项目 → 400)、POST /api/checks/start(202 / 409)与 POST /api/checks/repair(202 / 409)——完成 Wave 2 Task 3 检查清单上「归 Task 3 补」的 writing/start/repair 三条 route 分支 ← D-P3-27"
    - "「继续自检」的 check_n 计算服务端完成:start_check 内部重跑同轮覆盖或 max+1 的逻辑在 session 层已交付(Wave 2);路由零自算,只透传受理结果 ← D-P3-21"
    - "路由层全部错误分支照 /api/rounds/process 模子:True → 202 受理响应体 status=accepted;False → 409;RuntimeError → 400 ← D-P3-27"
    - "Wave 2 遗留的路由补充与新增的 writing/start/repair 合并为一族(route 层不重复 session 判定,不新增全局)← D-P3-27"
    - "全量 pytest 回归基线只增不降;route 级 writing/start/repair 受理与全部 409 分支有专属用例"
  artifacts:
    - path: "backend/prompts.py(微扩)"
      provides: "无新增函数(本任务预期仅视 Wave 2 交付面核对;若 Wave 2 已含全部三族 prompt 则零改动,执行者确认后记 SUMMARY)"
    - path: "backend/main.py(扩展)"
      provides: "POST /api/writing、POST /api/checks/start、POST /api/checks/repair 三条 202/409/400 路由(与 Wave 2 Task 1 交付的 authorize/tier/verdict 及 Task 3 交付的 GET 两组合成八条完整族)"
    - path: "backend/tests/test_route_session.py(扩展)"
      provides: "writing/start/repair 三路由的 202/409/400 全分支用例(FakeAICaller 不触发真调用,202 受理后 wait_idle)"
  key_links:
    - from: "backend/main.py POST /api/writing"
      to: "backend/session.py start_writing"
      via: "202 受理/409 拒绝,照 /api/rounds/process 分支模子"
      pattern: "start_writing"
    - from: "backend/main.py POST /api/checks/start 与 /api/checks/repair"
      to: "backend/session.py start_check / start_repair"
      via: "「继续自检」/「继续修复」按钮的 HTTP 面;服务端入口判定防绕过(409)"
      pattern: "start_check"
  prohibitions:
    - statement: "路由层不得重复实现 session 入口判定(check_available/repair_available/writing_available 语义归 session;路由只透传受理结果)"
      status: unverified
      flagged: true
    - statement: "不得新增专用收尾 SSE 事件或全局变量(done 后前端拉 /api/session 照旧)"
      status: unverified
      flagged: true
    - statement: "不新增第三方依赖、不引入新测试基建(D-P3-30)"
      status: unverified
      flagged: true
---

## Phase Goal

**As a** 阶段 4/5 中的用户,**I want to** 点「撰写总设计文档」/「继续自检」/「继续修复」按钮时后端受理我的请求并在状态不满足时明确拒绝,**so that** 阶段 3/4/5 的全部八条路由契约完整定形,Wave 4 前端有固定接口可挂接。

<objective>
本计划补齐 Wave 2 因任务密度移出的三条 202 受理路由(writing/start/repair)及其 route 级全分支用例,并与 Wave 2 已交付的 authorize/tier/verdict + design/checks 组合成 D-P3-27 项下完整的八条路由族。此为一个小型补口计划:Wave 2 的 session 六函数与 prompt 三族已全部交付,本计划纯接线 + 测试(Wave 2 Task 3 的 checks 路由清单若已盖 writing/start/repair 三条,实施前先核对——已存在则本计划仅剩核对与用例补强并记 SUMMARY「零路由新增」)。

Purpose: D-P3-27 路由契约的完整性收口——Wave 4 视图消费的全部端点在一处验收。
Output: 三条 202/409/400 路由 + route 全分支用例 + 八路由清单核对表(入 SUMMARY)。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/phases/idi-03-g3/03-CONTEXT.md
@.planning/phases/idi-03-g3/idi-03-PATTERNS.md
@.planning/phases/idi-03-g3/idi-03-02-SUMMARY.md

依赖接口(来自 Wave 2,直接接线):
- backend/session.py:start_writing() / start_check() / start_repair() -> bool(三查语义,False = busy 或入口判定不过)
- backend/main.py:Wave 2 已交付的「阶段 3/4/5 路由族」分节(authorize/tier/verdict + GET design/checks);POST /api/rounds/process 332-350 的 202/409/400 分支模子
- DESIGN.md §7.3①②(「继续撰写」「继续自检」「继续修复」入口语义)
- D-P3-21(重跑同轮覆盖,不跳号——服务端逻辑在 session 层已交付)

分支纪律(per 仓库 CLAUDE.md §5):小改动——执行者从当前分支 HEAD 切出 phase-03/idi-03-03 工作分支,plan 完成后合回原分支。

测试纪律(D-P3-30):一切 pytest 必须 `.venv/bin/python -m pytest`。
</context>

<tasks>

<task type="auto">
  <name>Task 1: POST /api/writing + /api/checks/start + /api/checks/repair 三条受理路由 + route 全分支用例</name>
  <reversibility rating="cheap">三条路由路径与请求/响应形状是 Wave 4 的固定契约;实现本身是纯接线(session 函数已交付),改动面小且可回退。</reversibility>
  <files>backend/main.py, backend/tests/test_route_session.py, backend/prompts.py</files>
  <read_first>
  - backend/main.py(332-350 /api/rounds/process 的 202/409/400 完整分支模子;Wave 2 增设的「阶段 3/4/5 路由族」分节注释区;56-87 Body 类位置)
  - backend/session.py(Wave 2:writing_available / check_available / repair_available 三入口判定 + start_writing / start_check / start_repair 的 True/False/RuntimeError 语义)
  - backend/prompts.py(Wave 2 已交付的 build_writing_prompt / build_check_prompt / build_repair_prompt——核对三族均已在,若缺任一补齐并记 SUMMARY)
  - backend/tests/test_route_session.py(route_env 24-29;Wave 2 Task 3 已加的 checks/design/authorize 用例族;FakeAICaller + wait_idle 模式在 route 环境的用法)
  - .planning/phases/idi-03-g3/03-CONTEXT.md(D-P3-27 路由清单原文)
  </read_first>
  <behavior>
    - POST /api/writing:phase4 造盘 + FakeAICaller(写 tmp)→ 202 {"status":"accepted"};busy → 409;phase3 造盘(非 phase4)→ 409;未进项目 → 400
    - POST /api/checks/start:phase5_awaiting_tier + tier 签名 → 202;无 tier 签名 → 409(check_available False);busy → 409
    - POST /api/checks/repair:phase5_checking(最新报告非 PASS)→ 202;phase5_awaiting_tier → 409;busy → 409;unpaired 待裁决非空 → 409(判定式①服务端强制)
    - 三路由全部:成功受理后 SSE 流照常(done 收尾),响应体 {"status":"accepted"} 与 /api/rounds/process 同形
  </behavior>
  <action>(1)核对 + 补齐 prompts.py 三族(Wave 2 应已全交付;缺则照 idi-03-02 Task 2 的 action 规格补齐,记 SUMMARY 偏差)。

(2)backend/main.py:三条路由加在 Wave 2 的「阶段 3/4/5 路由族」分节内(POST /api/writing → session.start_writing;POST /api/checks/start → session.start_check;POST /api/checks/repair → session.start_repair),分支逐字照 POST /api/rounds/process 模子:try RuntimeError → 400(未进项目);返回 False → 409(busy 或入口判定);True → 202 {"status":"accepted"}。**路由零自算**(check_n 与重跑判定全在 session 层,D-P3-27 与本计划 prohibition 双重申明)。无请求体的三条直接 @app.post(无 Body 类)。

(3)backend/tests/test_route_session.py 扩用例 ≥ 6(writing 202/409×2、check start 202/409、check repair 202/409×2、busy 互斥一条,HangingFake;FakeAICaller 类照 test_session 的 script 事件模式在 route 环境复用,FakeAICaller monkeypatch 或 session._set_caller_for_tests 注入):behavior 列表逐条,受理用例后 wait_idle 收流再断言(202 只证明受理,事件链归 session 级已测——本处断言受理码与 409 分支即可,Fake 免重度收流)。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_route_session.py -q 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1'</automated>
    <fails_when>任一 pytest 输出含 failed/error;test_route 新增 writing/start/repair 用例 < 6(grep -c "def test_route_writing\|def test_route_check_start\|def test_route_check_repair" 为 0);任一 202/409 分支断言失败;全量回归 passed < 143。</fails_when>
  </verify>
  <acceptance_criteria>
  - backend/main.py 三路由装饰器逐一命中:`grep -n "api/writing\|api/checks/start\|api/checks/repair" backend/main.py` 三路径各 ≥ 1;分节注释归属「阶段 3/4/5 路由族」
  - 三路由体均无 derive_state / check_available 等判定重复实现(grep 路由函数体内无这些调用——判定全在 session)
  - 202 响应体与 /api/rounds/process 同形 {"status":"accepted"}(route 用例断言)
  - 409 分支:非 phase4/无 tier 签名/非 phase5_checking/unpaired 非空/busy 各有用例覆盖
  - prompts.py 三族 prompt(build_writing/build_check/build_repair)经 grep 全部命中(零缺)
  - 全量回归零失败
  </acceptance_criteria>
  <done>八条阶段 3/4/5 路由全部就位并 route 级全分支证明(writing/start/repair 三条由本计划交付,其余五条 Wave 2 已交付经核对);路由层零判定重复、零新增全局;Wave 4 前端可按八条契约开发。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 浏览器 → 三条受理路由 | 状态伪造(非 phase4 发 writing、无 tier 发 start)全部由服务端 session 入口判定拦截 |
| 并发窗口 | 多窗口同点 start/repair/writing 的单飞锁语义(session 层已交付,路由透传) |

## STRIDE Threat Register

| Threat ID | Category | Severity | Disposition | Mitigation Plan |
|-----------|----------|----------|-------------|-----------------|
| T-idi03-12 | Elevation of Privilege | POST /api/checks/start 在未选档(无 tier 签名)时直接起检 | high | mitigate | check_available 含 tier 签名前置检查(写入 checks.read_tier None → False);route 用例覆盖无签名 409 |
| T-idi03-13 | Tampering | unpaired 待裁决期间 POST /api/checks/repair 误重跑 | high | mitigate | repair_available 的判定式①服务端强制(unpaired 非空 → False → 409);「继续修复」只由判定式②放行(D-P3-20);busy 单飞双防线 |
| T-idi03-14 | Denial of Service | 三路由被高频刷导致单飞长期占用 | low | accept | 单飞锁天然拒绝并发;单机单人本地工具,无外部暴露面(localhost) |

执行说明:零新包安装,无供应链项。
</threat_model>

<verification>
1. Task 1 automated:pytest test_route_session.py(writing/start/repair ≥ 6 用例)+ 全量回归
2. 八路由清单核对表(writing/start/repair/authorize/tier/verdict/design/checks 各一行:负责人计划 + 状态)写入 SUMMARY
3. 无人检项
</verification>

<success_criteria>
- 三条受理路由 202/409/400 分支 route 级全绿;单飞互斥用例在位
- 路由层零判定重复(grep 证明);八路由族清单核对完整
- 全量回归 143 基线只增不减
</success_criteria>

## Artifacts this phase produces(本计划新增符号清单)

- backend/main.py:POST /api/writing、POST /api/checks/start、POST /api/checks/repair(三条受理路由;与 Wave 2 五条合成 D-P3-27 全量八条)
- backend/tests/test_route_session.py:test_route_writing 系列、test_route_check_start 系列、test_route_check_repair 系列(≥ 6 用例)
- backend/prompts.py:预期零新增(三族核对确认;缺则补齐并记 SUMMARY)

<output>
Create `.planning/phases/idi-03-g3/idi-03-03-SUMMARY.md` when done
</output>

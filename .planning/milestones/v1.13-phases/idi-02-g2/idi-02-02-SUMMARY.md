---
phase: idi-02-g2
plan: "02"
subsystem: api
tags: [fastapi, sse, ai-caller, prompts, session, writeback, annotations, g2-pipeline]

# Dependency graph
requires:
  - phase: idi-02-g2(plan 01)
    provides: backend/annotations.py(load/append_item/writeback/select_pending)与 backend/grammar.py(parse_annotation_responses 等六条 §6.4 文法)——process_round 回写链与 answer_plain/add_annotation 落盘的全部数据契约
  - phase: idi-01-1-2
    provides: session.trigger_divergence 模子(入口三查/单飞锁/后台线程/SSE 直播)、main.py 路由风格(202/409/400)、ai_caller.ask_lite 签名预定义(D-P1-6)、prompts 四段结构先例
provides:
  - backend/ai_caller.py:SdkAICaller.ask_lite 与 SubprocessAICaller.ask_lite 双路线真实现(同一 dict(answer) 契约,失败返回 {answer:"", error} 不抛;D-P2-8/D-P2-24)
  - backend/prompts.py:build_plain_prompt(轻量三段)与 build_round_prompt(G2 四段,§3.3 四步 + §6.3 五件套 + §6.4 文法模板逐字)+ _ROUND_INSTRUCTIONS/_GRAMMAR_EXAMPLES 模块常量
  - backend/session.py:process_round()(G2 全流水线,done 后回应表回写 prev_round)、round_process_available(纯磁盘入口判定)、answer_plain(同步轻量封装)、add_annotation(建条目)、_session_snapshot rounds/pending_annotations 字段
  - backend/main.py:五条轮次路由(GET /api/rounds、GET /api/rounds/{n}、POST annotations、POST plain、POST process;202/409/404/400/502 语义按 D-P2-22)
  - FakeAICaller ask_lite/lite_calls/lite_answers 扩展(run/abort 形态不变)
affects: [idi-02 (Wave 3 前端消费五路由与快照字段), idi-02-04 (IDI_E2E 真 CLI 全链验证), idi-03 (G3 校验消费 annotations answered 状态)]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
# Same estimateTokens scale (chars/4 over the realized diff), never a harness token count.
actuals:
  tokens: 17107    # 68428 diff chars / 4(git diff over plan_head_before..HEAD)
  tasks: 3
  commits: 3        # MEASURED: git rev-list --count 2c11f1d..HEAD
  plan_head_before: 2c11f1dfcb1fe4f437aa4901a24d1bb176e6113b

# Tech tracking
tech-stack:
  added: []   # 零新增第三方依赖(subprocess/asyncio/threading 均标准库)
  patterns:
    - "done 后回写 = 重拉 derive_state 判轮次前进 → parse_annotation_responses → writeback(prev_round)(AI 产物不可信,回写只认回应表 id;不前进不回写不报错——半成品自愈零新分支)"
    - "轻量调用同步化:answer_plain 不起线程不产事件(单机单人秒级响应,§3.4),与主调用单飞锁共用 busy 判定"
    - "prompt 文法模板逐字嵌入:_GRAMMAR_EXAMPLES 常量把三表头/标记行正例贴进 build_round_prompt,三关键词(覆盖维度表/未决问题清单/批注回应)与 grammar.py 解析字面一致"
    - "入口校验助手 _current_round_guard:add_annotation 与 answer_plain 共用(未进项目 400/非当前轮或非 phase3 409)"

key-files:
  created: []
  modified:
    - backend/ai_caller.py
    - backend/prompts.py
    - backend/session.py
    - backend/main.py
    - backend/tests/test_session.py
    - backend/tests/test_route_session.py

key-decisions:
  - "ask_lite 失败约定:双路线均返回 {answer:\"\", error:中文原因} 不抛(上层路由转 4xx/5xx);answer_plain 以「大白话调用失败」前缀 RuntimeError 供路由层识别 502"
  - "SubprocessAICaller.ask_lite 保留 --output-format stream-json + --verbose(stdout 仍逐行 JSON 可解析 result 行),只去掉输入侧双向协议(--input-format stream-json 与 --permission-prompt-tool);禁工具用 CLI 原生 --tools \"\""
  - "SdkAICaller.ask_lite 用顶层 claude_agent_sdk.query() 异步迭代器(而非 ClaudeSDKClient 长连接)+ ClaudeAgentOptions(tools=[], setting_sources=[], 无 can_use_tool)——纯问答无权限回环;asyncio.run 同步收 ResultMessage"
  - "E2BIG 回退取 argv 优先、OSError 时整体改 stdin 传递(实现取其一并写进 docstring;T-idi02-08 缓解)"
  - "process_round 的回写动作放 _worker else 段(try 正常收流后才回写;异常/中止路径不回写);finally 段保持唯一一条 kind=done 收尾事件,回写异常仅发 error 事件不悬空进度"
  - "add_annotation 不加 busy 检查(D-P2-22:409 仅非当前轮/非 phase3 两条件;annotations 写当前轮文件与 AI 回写上一轮不同对象无竞态),与 answer_plain(busy 检查)刻意不同"
  - "回写用 prev_round 在 _worker 外闭包捕获(build 前的值),回写时重拉 derive_state 取新轮——两个轮号都来自磁盘推导,不依赖内存中间态"
  - "GET /api/rounds/{n} 的 404 判据用 snapshot 的 rounds 列表(完整轮);session.current_project_path() 只读访问器供路由读文档,不加新全局"

patterns-established:
  - "Pattern: G2 全流水线 = trigger_divergence 模子(入口三查/单飞/线程/直播)+ done 后磁盘重拉回写——第三次复制该模式,后续 G3 撰写可再平移"
  - "Pattern: prompt 模板正例逐字常量(_GRAMMAR_EXAMPLES)与解析器关键字同源校验——两端字面一致由 build_round_prompt 测试断言锁定"

requirements-completed: [FLOW-04, UI-02, DATA-01]

# Coverage metadata (#1602) — one entry per shipped deliverable.
coverage:
  - id: D1
    description: "ask_lite 双路线实现:SdkAICaller 与 SubprocessAICaller 同一签名同一契约(返回 dict 含 answer;失败 {answer:\"\",error} 不抛);FakeAICaller 打桩(lite_calls 三元组 + lite_answers 注入,run/abort 形态不变)"
    requirement: UI-02
    verification:
      - kind: unit
        ref: backend/tests/test_session.py#test_fake_ai_caller_ask_lite_records_and_returns
        status: pass
      - kind: unit
        ref: backend/tests/test_session.py#test_subprocess_ask_lite_argv_construction
        status: pass
      - kind: unit
        ref: backend/tests/test_session.py#test_subprocess_ask_lite_error_no_result
        status: pass
      - kind: unit
        ref: backend/tests/test_session.py#test_sdk_ask_lite_options_construction
        status: pass
    human_judgment: false
  - id: D2
    description: "build_plain_prompt:三要素(当前文档全文/划选原文/用户问题)+ §3.8 红线 + 只解释不改设计;prompt 不含 docs/ 读取指令、不给工具、不要求写文件"
    requirement: UI-02
    verification:
      - kind: unit
        ref: backend/tests/test_session.py#test_build_plain_prompt_three_materials_and_rules
        status: pass
      - kind: unit
        ref: backend/tests/test_session.py#test_subprocess_ask_lite_argv_construction(用例 4 断言:prompt 无 docs/ 指令、无 Write、「不要读取其他文件」)
        status: pass
    human_judgment: false
  - id: D3
    description: "build_round_prompt + _ROUND_INSTRUCTIONS/_GRAMMAR_EXAMPLES:§3.3 四步逐条、§6.3 五件套点名、三表头与标记行逐字正例 + 切勿改列名硬指令、目标文件名 docs/discuss-round-(N+1).md 明示、禁止写 annotations、空批注显式「当前轮暂无待处理批注」"
    requirement: FLOW-04
    verification:
      - kind: unit
        ref: backend/tests/test_session.py#test_process_round_prompt_contains
        status: pass
      - kind: unit
        ref: backend/tests/test_session.py#test_process_round_empty_annotations_ok
        status: pass
    human_judgment: false
  - id: D4
    description: "process_round 全流水线:入口三查(未进项目 RuntimeError/在飞 False/非 phase3 False)+ 单飞锁 + 后台线程 + 事件照常 SSE 直播 + done 后回写(prev_round 闭包捕获;重拉 derive_state;新轮前进时 parse_annotation_responses → writeback;未前进不回写不报错——半成品自愈)"
    requirement: FLOW-04
    verification:
      - kind: unit
        ref: backend/tests/test_session.py#test_round_process_available
        status: pass
      - kind: unit
        ref: backend/tests/test_session.py#test_process_round_writeback(a1-01 answered/a1-02 pending/current_round 1→2)
        status: pass
      - kind: unit
        ref: backend/tests/test_session.py#test_process_round_incomplete_new_round(轮次不动+批注未动+可重跑+重跑后回写)
        status: pass
      - kind: unit
        ref: backend/tests/test_session.py#test_process_round_busy_rejects
        status: pass
      - kind: unit
        ref: backend/tests/test_session.py#test_process_round_non_phase3_rejects
        status: pass
    human_judgment: false
  - id: D5
    description: "answer_plain 同步封装 + add_annotation:同步调 ask_lite(lite_calls 记录三元组、不 publish 任何 SSE 事件)、plain 落盘 type=plain/status=answered/answer 有值;在飞拒绝;comment/pending 建条目;非当前轮→RuntimeError 供路由 409;plain 不计 pending_annotations"
    requirement: UI-02
    verification:
      - kind: unit
        ref: backend/tests/test_session.py#test_answer_plain_records_and_persists
        status: pass
      - kind: unit
        ref: backend/tests/test_session.py#test_answer_plain_busy_rejects
        status: pass
      - kind: unit
        ref: backend/tests/test_session.py#test_add_annotation_creates_pending_comment
        status: pass
    human_judgment: false
  - id: D6
    description: "五条轮次路由(HTTP 面,D-P2-22):GET /api/rounds(200 列表)/ GET /api/rounds/{n}(200 或 404)/ POST annotations(200/409 非当前轮或非 phase3/400 空 quote)/ POST plain(200/409/400/502 AI 失败)/ POST process(202/409);错误语义服务端强制"
    requirement: FLOW-04
    verification:
      - kind: integration
        ref: backend/tests/test_route_session.py#test_route_rounds_list_and_current
        status: pass
      - kind: integration
        ref: backend/tests/test_route_session.py#test_route_round_single_and_404
        status: pass
      - kind: integration
        ref: backend/tests/test_route_session.py#test_route_post_annotation_creates_and_409s
        status: pass
      - kind: integration
        ref: backend/tests/test_route_session.py#test_route_post_plain_answers
        status: pass
      - kind: integration
        ref: backend/tests/test_route_session.py#test_route_post_plain_502_on_ai_error
        status: pass
      - kind: integration
        ref: backend/tests/test_route_session.py#test_route_process_round_202_or_409 + test_route_process_round_409_non_phase3
        status: pass
      - kind: integration
        ref: "uvicorn 冒烟(uvicorn backend.main:app --port 8766 + curl):health 200 / enter 200 / GET rounds 200 含 current_round / GET rounds/1 200 含 annotations / POST annotations grep pending / 非当前轮 POST annotations HTTP 409 → rounds-api-ok"
        status: pass
    human_judgment: false
  - id: D7
    description: "_session_snapshot 轮次字段:rounds(list_complete_rounds 列表)+ pending_annotations(当前轮 comment+pending 计数,仅 phase3 有值其余 0;plain 条目不计)插在 current_check 之后,既有字段不重命名"
    requirement: DATA-01
    verification:
      - kind: integration
        ref: backend/tests/test_route_session.py#test_route_session_snapshot_rounds_fields(rounds=[1]、pending=1——1 条 pending comment + 1 条 plain 不计)
        status: pass
      - kind: unit
        ref: backend/tests/test_session.py#test_answer_plain_records_and_persists(纯 plain 条目快照计数 0)
        status: pass
    human_judgment: false
  - id: D8
    description: "AI 不直接改写 annotations(建条目仅 POST 路由经 append_item;回写仅 process_round done 后后端动作;prompt 明确禁止写 annotations 文件)+ 回写不依赖 AI 自觉(只认回应表 id,未出现保持 pending)"
    requirement: DATA-01
    verification:
      - kind: unit
        ref: backend/tests/test_session.py#test_process_round_writeback(回应表只含 a1-01 → a1-01 answered、a1-02 保持 pending)
        status: pass
      - kind: unit
        ref: backend/tests/test_session.py#test_process_round_prompt_contains(prompt 含「批注记录由本工具后端管理」禁令——目标文件名与禁写指令明示)
        status: pass
    human_judgment: false
  - id: D9
    description: "全量 pytest 回归不降:Wave 1 基线 120 passed + 2 skipped 之上叠加 23 新用例零失败(143 passed + 2 skipped)"
    requirement: FLOW-04
    verification:
      - kind: automated
        ref: ".venv/bin/python -m pytest backend/tests/ -q → 143 passed, 2 skipped(120 基线 + 23 新增)"
        status: pass
    human_judgment: false
  - id: D10
    description: "真 CLI 的 ask_lite 双路线实际秒级响应与 process_round 真实新轮产出——本计划为 Fake 级;真实链在 idi-02-04 的 IDI_E2E 门控用例"
    requirement: UI-02
    verification: []
    human_judgment: true
    rationale: "本计划测试均为 Fake 级(PLAN 验证第 4 条明示:真 CLI 全链在 idi-02-04 的 IDI_E2E 门控用例验证,不在本计划);双路线真实现的行为一致性在真实调用下的表现需要 idi-02-04 的真链证据,人检/真 E2E 归后续计划"

# Metrics
duration: 36 min
completed: 2026-09-09
status: complete
---

# Phase idi-02 Plan 02: 轮次收敛循环——G2 后端全层 Summary

**G2 全流水线(process_round 入口三查+单飞+SSE 直播+done 后回应表解析回写上一轮 annotations)与大白话 ask_lite 双路线同步调用、五条轮次路由(202/409/404/400/502)落下,23 新用例 + uvicorn 冒烟全绿,基线 120→143 不降**

## Performance

- **Duration:** 36 min
- **Started:** 2026-09-09T16:55:11Z
- **Completed:** 2026-09-09T17:31:16Z
- **Tasks:** 3 / 3
- **Files modified:** 6

## Accomplishments

- **ask_lite 双路线真实现**(替换 Phase 1 NotImplementedError 占位):SubprocessAICaller(一次性 `--tools ""` 禁工具纯问答,保留 `--setting-sources=` 与 `--append-system-prompt`,E2BIG 时 argv→stdin 回退,result 行同步解析)、SdkAICaller(顶层 query() + tools=[]/setting_sources=[] 无 can_use_tool,asyncio.run 同步收 ResultMessage)——同一 dict(answer) 契约,失败返回 {answer:"", error} 不抛;build_plain_prompt 三段结构(§3.8 红线 + 只解释不改设计 + 仅两块资料显式声明)
- **process_round() G2 全流水线**:照 trigger_divergence 模子(入口三查/单飞锁/后台线程/事件 SSE 直播/done 收尾唯一);done 后回写闭环挂通——prev_round 闭包捕获 → worker 正常收流后重拉 derive_state → 轮次前进时读新轮文档 → grammar.parse_annotation_responses → annotations.writeback(prev_round);未前进(AI 写废/中止半成品)不回写不报错,可重跑(§7.3 自愈零新增分支)
- **build_round_prompt 四段组装**:资料段读全量 docs/(当前轮文档全文含半成品重跑场景 + annotations 逐条 id/quote/note + 空/非空显式分支「当前轮暂无待处理批注」 + transcript/draft/brainstorm);任务段注入 §3.3 四步逐条 + §6.3 五件套 + §6.4 三表头/标记行逐字正例 + 切勿改列名硬指令 + 目标文件名 docs/discuss-round-(N+1).md + 禁止写 annotations
- **answer_plain / add_annotation**:同步封装(无线程、无 SSE 事件,D-P2-8/D-P2-10)→ ask_lite → append_item(type=plain, answer, status=answered);add_annotation 建 comment/pending 条目;409 语义刻意区分(plain 有 busy 检查,annotation 无——D-P2-22 两条件 409);_session_snapshot 扩 rounds + pending_annotations 字段(plain 不计)
- **五条轮次路由**:GET /api/rounds、GET /api/rounds/{n}(404 非完整轮)、POST annotations(200/409 两条件/400)、POST plain(200/409/400/502 AI 失败)、POST process(202/409)——全部经 uvicorn 真起服务 curl 冒烟验证(rounds-api-ok)

## Task Commits

Each task was committed atomically:

1. **Task 1: ask_lite 双路线实现 + build_plain_prompt(FakeAICaller 打桩)** - `df63cd7` (feat)
2. **Task 2: process_round 全流水线——build_round_prompt + done 后回应表回写(tracer 切穿四层)** - `a74df69` (feat)
3. **Task 3: answer_plain 同步封装 + 五条轮次路由 + _session_snapshot 轮次字段** - `64bf158` (feat)

**Plan metadata:** 本 commit(docs: complete plan)

## Files Created/Modified

- `backend/ai_caller.py` - AICaller.ask_lite 契约 docstring + SdkAICaller.ask_lite(query 单轮 + asyncio.run)与 SubprocessAICaller.ask_lite(subprocess.run + stream-json 解析 + E2BIG stdin 回退)
- `backend/prompts.py` - build_plain_prompt(三段轻量)与 build_round_prompt(G2 四段)+ _ROUND_INSTRUCTIONS/_GRAMMAR_EXAMPLES/_PLAIN_ROLE 模块常量(表头/标记行逐字,三关键词与 grammar.py 解析字面一致)
- `backend/session.py` - round_process_available/process_round(done 后回写)/answer_plain(同步)/add_annotation/current_project_path/_current_round_guard/_session_snapshot 新字段(rounds/pending_annotations)
- `backend/main.py` - AnnotationBody/PlainBody pydantic 模型 + 五条轮次路由(在 get_transcript 之后、Plan 01 骨架分节之前)
- `backend/tests/test_session.py` - FakeAICaller 扩展(lite_calls/lite_answers/ask_lite)+ RoundWritingFake/_enter_phase3 helper + Task 1 五例 + Task 2 七例 + Task 3 三例(共 15 新用例)
- `backend/tests/test_route_session.py` - _enter_phase3_route helper + 八条路由级用例(列表/单轮 404/建批注 200+409+400/plain 200/502/process 202+409/快照字段)

## Decisions Made

- **ask_lite 失败约定**:双路线统一返回 {answer:"", error:中文原因} 不抛;answer_plain 在 AI 失败时 raise RuntimeError("大白话调用失败:…"),路由层按「大白话调用失败」前缀识别 502(与「在飞/进行中」409、「轮/阶段」409 的消息子串分支互斥——502 判定放最前防 error 文本误命中"轮"字)
- **SubprocessAICaller.ask_lite 的 stream-json 取舍**:保留 --output-format stream-json + --verbose(stdout 是逐行 JSON,result 行可同步解析)但去掉输入侧双向协议(--input-format stream-json 与 --permission-prompt-tool)——合规于 D-P2-9「非流式单向」的语义(单向 = 无控制协议回环,输入侧不保持打开)
- **SdkAICaller.ask_lite 用顶层 query()**(async for 一遍耗尽)而非 ClaudeSDKClient 长连接——纯问答单轮,无中止/控制需求,代码量最小;asyncio.run 照 run() 先例形态
- **禁工具的实现**:CLI 用原生 `--tools ""`(claude CLI 2.x 支持:Use "" to disable all tools),SDK 用 `tools=[]`(SDK 文档:empty list = disable all built-in tools)——两侧等效且都是官方一等参数,不用 disallowed_tools 黑名单(残余枚举不完)
- **回写放在 worker 的 else 段**(try 正常收流后)而非 finally:异常/中止路径不应触发对半成品的回写尝试;finally 只保留 done 收尾事件 + 解锁——「回写动作不发第二条 done」由结构保证
- **add_annotation 无 busy 检查**(PLAN action 明示):写当前轮文件与 AI 回写上一轮是不同对象,无竞态;保持 D-P2-22 的 409 契约字面一致(409 仅非当前轮/非 phase3 两条件)
- **回写的轮号来源**:prev_round 在 _worker 外闭包捕获(build 前值),new_round 在回写时重拉 derive_state——两值都源于磁盘推导,回写完全无内存态依赖(重跑/中断天然安全)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Task 3 verify 行的 uvicorn 冒烟整链无法以内联 bash 单命令过沙箱(命令过长)**
- **Found during:** Task 3(执行 verify 时)
- **Issue:** PLAN `<verify>` 的整链 bash 命令(含 && 连接的 pytest×2 + uvicorn 后台起 + until 等 health 循环 + mktemp 造盘 + 5 个 curl 判定 + kill 收尾)超出权限沙箱对单条 Bash 命令的长度/引号接受度
- **Fix:** 按编排者指引,把同样判定语义写为 /tmp shell 脚本执行;判定行逐条保留原语义(health 等待 120×0.5s 上限、enter 造盘 docs/discuss-round-1.md 带合规末行、GET rounds grep current_round、GET rounds/1 grep annotations、POST annotations grep pending、非当前轮 POST status_code grep 409);pytest×2 部分单独先跑(全部通过);uvicorn 部分照原语义跑出 rounds-api-ok,结束 lsof -ti:8766 | xargs kill 清理(已验证端口空)
- **Files modified:** 无仓库文件(仅 /tmp/idi-02-02-smoke.sh 临时脚本;文件在 /tmp 下,被沙箱禁止 rm,无害残留)
- **Verification:** 冒烟输出 rounds-api-ok;端口 8766 lsof 空;pytest 38 passed(两文件)+ 143 passed(全量)
- **Committed in:** 无(临时脚本不入库)

**2. [Rule 1 - Bug] prompt 文件位置初版放在 build_divergence_prompt 之前,破坏文件逻辑分组**
- **Found during:** Task 1(编写 build_plain_prompt 时)
- **Issue:** 初版把 build_plain_prompt 插在 build_divergence_prompt 之前,文件读起来如同「轻量调用优先于主流程」(与 docstring 声明的结构不符)
- **Fix:** build_plain_prompt 保持在既有两个 build 函数之间插入(最终位置无关紧要——函数无相互调用;以最小 diff 为准);实际实现放 build_divergence_prompt 之后、build_phase12_prompt 之前,文件尾部追加 build_round_prompt(Task 2)——文件可读性以「每函数就近 + 不改既有函数」为准
- **Files modified:** backend/prompts.py
- **Verification:** python import 通过 + 三 prompt 测试全绿
- **Committed in:** df63cd7 / a74df69(两个 task commit 内)

---

**Total deviations:** 2 auto-fixed(1 Rule 3 blocking§冒烟脚本、1 Rule 1 cosmetic§文件位置)
**Impact on plan:** 两个偏差都是执行层面的工程项目——冒烟语义零变化(逐行保留 PLAN 判定),文件位置纯可读性;零范围蔓延、零契约变化。

## Issues Encountered

None —— 三任务线性推进;Task 1/3 的 pytest 与冒烟一次全绿,Task 2 的七用例一次全绿;无第三方依赖新增、无路由开关新增。

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Wave 3(前端)可完全按本契约开发**:GET /api/session 快照(rounds/pending_annotations)+ 五路由 + answer 落盘字段(前端直读 annotation.answer)+ done 后拉新先例(refreshGatesAfterStream 挂 /api/rounds)
- **idi-02-04(IDI_E2E)**:真 CLI 链下 ask_lite 的双路线行为一致性(SDK 与 subprocess 同 prompt 同答案形态)与 process_round 真实新轮产出是遗留的真链验证面——本计划 D10 已声明 human_judgment(true, rationale 记「Fake 级」),真链证据在彼计划补
- **idi-03(G3)**:annotations 的 answered 状态由 writeback 机械落定——G3 四处校验「①annotations 无 pending」可直接复用 select_pending(与 D-P2-15 同语义)

## Self-Check: PASSED

- 关键文件:backend/ai_caller.py FOUND、backend/prompts.py FOUND、backend/session.py FOUND、backend/main.py FOUND、backend/tests/test_session.py FOUND、backend/tests/test_route_session.py FOUND(6/6)
- 提交:df63cd7 FOUND、a74df69 FOUND、64bf158 FOUND(3/3)
- commits 实测:git rev-list --count 2c11f1d..HEAD = 3(生产 3 + 本 SUMMARY 1 = 4)
- 全量:.venv/bin/python -m pytest backend/tests/ -q → 143 passed, 2 skipped(基线 120 不降,新增 23)
- 冒烟:uvicorn + curl → rounds-api-ok(五路由 + 非当前轮 409)

---
*Phase: idi-02-g2*
*Completed: 2026-09-09*

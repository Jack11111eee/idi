---
phase: idi-01-1-2
verified: 2026-09-09T09:18:23Z
status: gaps_found
score: 7/8 must-haves verified
covered_files:
  - .planning/phases/idi-01-1-2/01-CONTEXT.md
  - .planning/phases/idi-01-1-2/idi-01-01-PLAN.md
  - .planning/phases/idi-01-1-2/idi-01-01-SUMMARY.md
  - .planning/phases/idi-01-1-2/idi-01-02-PLAN.md
  - .planning/phases/idi-01-1-2/idi-01-02-SUMMARY.md
  - .planning/phases/idi-01-1-2/idi-01-03-PLAN.md
  - .planning/phases/idi-01-1-2/idi-01-03-SUMMARY.md
  - .planning/phases/idi-01-1-2/idi-01-04-PLAN.md
  - .planning/phases/idi-01-1-2/idi-01-04-SUMMARY.md
  - .gitignore
  - backend/__init__.py
  - backend/ai_caller.py
  - backend/cli_check.py
  - backend/config.py
  - backend/events.py
  - backend/g1.py
  - backend/main.py
  - backend/prompts.py
  - backend/session.py
  - backend/state.py
  - backend/transcript.py
  - backend/tests/__init__.py
  - backend/tests/test_ai_caller.py
  - backend/tests/test_e2e_smoke.py
  - backend/tests/test_g1.py
  - backend/tests/test_session.py
  - backend/tests/test_state.py
  - backend/tests/test_transcript.py
  - frontend/app.js
  - frontend/index.html
  - frontend/style.css
  - frontend/vendor/marked.min.js
  - config.json
  - pytest.ini
  - requirements.txt
  - run.sh
covered_digest: "v1:sha256:a1ac56ee4f8d0f44b2ef76245b9f4a21cb1d20cce11e8f7a7c9ab1bcd75195fc"
behavior_unverified: 6
overrides_applied: 0
gaps:
  - truth: "点「中止」按钮随时能杀掉当前调用且不留损坏状态(会话路径)— ROADMAP 成功判据 4 / AI-02 / Plan 01 must-have 真值 4"
    status: failed
    reason: >-
      POST /api/abort 路由只中止 main._current_caller(仅 /api/dev/ping 探针线程会设置它);
      会话流水线(send_message / trigger_divergence,即浏览器「发送」按钮的真实链路)的 caller
      存于 session._caller,路由从不调用 session.abort()。实测(FastAPI TestClient + 挂起
      FakeAICaller):会话调用在飞时点「中止」返回 {killed: false},caller 的 abort() 从未被调,
      busy 锁不释放,此后 /api/message 与 /api/divergence 全部 409 直至 AI 自然收尾。
      session.abort() 本身行为正确(实测:caller 被杀 + pending 强制释放 + busy 解锁),
      缺的只是 HTTP 接线。执行者在 Plan 01 的中止探针走的是 dev/ping 路径(_current_caller),
      所以 SUMMARY 的 PASS 记录为真但只覆盖了探针路径——Plan 03 会话接管 caller 管理后此回归无人覆盖。
    artifacts:
      - path: "backend/main.py"
        issue: "/api/abort 路由(第 235-241 行)只查 _current_caller;未接 session.abort()。会话调用在飞时 killed 恒为 false"
      - path: "backend/session.py"
        issue: "会话层 abort() 完备(caller.abort + pending 全部强制释放为 False + inflight 解锁)但无任何 HTTP 入口触达它"
    missing:
      - "backend/main.py 的 /api/abort 路由接入 session.abort():会话在飞时优先中止会话调用(并广播释放),dev/ping 探针路径保持既有 _current_caller 中止"
      - "补一条会话路径中止的行为测试(FakeAICaller 在飞 → POST /api/abort → caller.abort 被调、busy 释放、transcript 无脏 [ai])——现有 test_abort_leaves_no_dirty_ai_entry 直调 session.abort(),不经 HTTP 路由,所以没拦住这个缺口"
behavior_unverified_items:
  - truth: "浏览器端到端用户流(goal 全句):打开应用 → 进目录 → (没想法→发散→挑方向) → 阶段 1-2 会话直播 → 认可雏形 → 轮次视图"
    test: "bash run.sh 后浏览器走 Plan 04 verification 第 5 条的完整 UAT 路径(空目录 → 没想法 → 看 brainstorm → 发方向 → 认可雏形 → 轮次占位)"
    expected: "每一步界面按 DESIGN.md §3.2/§4.1/§4.4 呈现;最终 discuss-round-1.md 落盘且界面切「已进入轮次阶段…当前轮:第 1 轮」"
    why_human: "点击交互与视觉呈现只有浏览器能确认;后端链路已全部机器验证(见行为抽检表),但 DOM 渲染与交互体验无 JS 测试覆盖"
  - truth: "SSE 事件逐条渲染进右侧工作面板(说话/读文件/写文件可区分,marked 渲染,折叠可用)"
    test: "发起一次会话消息,亲眼看事件逐条出现在面板;点面板标题折叠/展开"
    expected: "事件分级标签与颜色正确,say 走 markdown,面板可折叠"
    why_human: "SSE → EventSource → DOM 的最后一跳是纯浏览器行为;后端事件流已双路线 live 验证"
  - truth: "权限弹窗闭环的浏览器交互(AI confirm 时弹模态框,同意/拒绝两按钮回传)"
    test: "诱导一次越权写(如在会话里让 AI 写项目根非保护文件),看弹窗、点同意与拒绝各一次"
    expected: "模态框出现并说明工具与目标;同意放行/拒绝驳回,面板出现权限确认事件"
    why_human: "模态视觉与点击回路只有浏览器可验;session 层回环已有 3 个用例覆盖(pend/allow/deny)"
  - truth: "CLI 自检失败两分支的指引浮层(未装 npm 指引 / 未登录 claude 指引)与「重新检测后放行」"
    test: "人为让 /api/cli-check 返回失败(或读代码走查浮层逻辑),看指引文案浮层与重检按钮"
    expected: "浮层显示对应中文指引;点击「我已装好,重新检测」通过后浮层消失且不再出现(只挡第一次)"
    why_human: "本机 CLI 已装且已登录,两个失败分支无法在本机真实触发;代码接线已验证(cli_check.py 两分支文案 + 前端浮层 + 无服务端缓存)"
  - truth: "会话气泡布局(用户右对齐/AI 左对齐)、草稿排版、发散候选虚线框等视觉呈现"
    test: "走一遍会话与发散,目检样式"
    expected: "样式与 §4.1/§4.2 布局一致,无排版破损"
    why_human: "纯视觉判断;元素与类名接线已机器验证(HTML 结构 grep)"
  - truth: "重启浏览器后的恢复体验(关页重开、重进同目录)"
    test: "走一段会话后关闭页面,重开浏览器进同一目录"
    expected: "会话流与草稿从磁盘全量恢复,无需任何恢复操作"
    why_human: "浏览器会话语境下的恢复体验;数据层恢复已由 E2E test_restart_recovery(真实 CLI + importlib.reload)行为验证"
---

# Phase 1: 行走骨架——服务器、单界面与阶段 1-2 会话 验证报告

**Phase Goal:** 用户打开应用、选中一个项目目录后,能和 AI 走完一段完整的阶段 1-2 会话(含没想法的零起步发散),在草稿区实时看到 AI 每一步动作,点「认可雏形」把草稿定稿为 discuss-round-1.md;重启后一切状态从磁盘完整恢复

**Verified:** 2026-09-09T09:18:23Z
**Status:** gaps_found
**Re-verification:** No — initial verification(verification.status 此前为 missing)

---

## 总判定

8 条 roadmap 成功判据中 7 条 VERIFIED、**1 条 FAILED**(中止按钮在会话路径失灵——集成接线缺失,实测确证)。除此之外,全部 10 个需求的机器可验证部分均已验证:测试套件 62 passed + 2 skipped(与基线一致)、§5.4 权限矩阵 9/9 实测全过、§7.4 八行推导表逐行实测、G1 定稿全链条实测、双轨 AICaller 各真实跑通一次、真实 CLI 的 E2E(会话一轮 + 重启恢复)实跑通过、HTTP 契约(enter/message/permission/g1/divergence/config)进程内全验、15 项 CONTEXT 决策 15/15 落地。浏览器视觉/交互部分按预期转人检(6 项,见 behavior_unverified_items)。

**结论:目标未完全达成——差一处已定位、修复面很小的接线缺口(见 Gaps Summary)。**

---

## Goal Achievement

### Observable Truths(合并 ROADMAP 8 条成功判据与 4 个 PLAN 的 must_haves,按 SC 为主契约去重)

| # | Truth(来源) | Status | Evidence |
|---|---|---|---|
| 1 | 未装/未登录 claude CLI 时给出指引并只挡第一次进入(SC1 ← AI-05) | ✓ VERIFIED | `backend/cli_check.py` 两分支文案(npm 装/claude 登录)+ `GET /api/cli-check` 无服务端缓存(代码:「只挡第一次」语义在前端,后端不记忆)+ 前端 `runCliCheck()` 浮层与 recheck 按钮接线完整(app.js:519-535);本机实测 CLI 已装已登录(2.1.266) |
| 2 | 选目录进入后界面按磁盘现状自动呈现对的状态,无需手工恢复(SC2 ← FLOW-01) | ✓ VERIFIED | `derive_state` 八行表**逐行 live 实测**(phase1_new→phase12→phase3→phase4→phase5_awaiting→phase5_checking→mission_complete 一条链推进)+ 17 用例;`POST /api/enter` HTTP 实测返回 state/transcript/draft/brainstorm/divergence_available/g1_available 全字段;前端 `applySessionView` 子视图切换接线完整 |
| 3 | 会话双句落盘 transcript.md,杀进程重启后从磁盘恢复,草稿继续演进(SC3 ← FLOW-02) | ✓ VERIFIED | `test_send_message_pipeline`(prompt 含 docs/ 全部文档 + 红线句)、`test_multi_segment_say_single_ai_entry`(多段合一条)、`test_abort_leaves_no_dirty_ai_entry`;**E2E 真跑**:`IDI_E2E=1 pytest -m slow` → `test_full_conversation_roundtrip` + `test_restart_recovery` 2 passed(真实 claude CLI 调用,[user, ai] 序列 + reload 重进恢复) |
| 4 | AI 事件原始直播到工作面板;点「中止」随时杀掉当前调用且不留损坏状态(SC4 ← AI-02) | ✗ FAILED | 直播半边已验证(两路线 live 实跑:subprocess kinds=[command,result,read,result,say,done] / sdk kinds=[command,read,say,done];SSE 端点 + broker + EventSource 全链接线)。**中止半边失败**:实测会话路径在飞时 `POST /api/abort` 返回 `{killed: false}`,caller 的 abort() 未被调,busy 锁卡死,后续 message/divergence 全 409(详见 Gaps Summary) |
| 5 | 「没想法」发散:三步模板、brainstorm.md 反复整体覆盖不编号、雏形存在即关闭入口(SC5 ← FLOW-06) | ✓ VERIFIED | `build_divergence_prompt` **live 结构断言**(风暴/收敛 3~5/挑选三步 + 4 固定视角 + 红线 + 覆盖落盘指令全部在场);`test_divergence_available_gating`(无 draft/有 draft/有完整轮三态 + 触发侧防绕过)、`test_trigger_divergence_writes_and_overwrites`(mtime 变化、无 -2 变体、旧内容不在、同链路用发散模板);HTTP 实测:开放时 202、关闭时 409 |
| 6 | 点「认可雏形」后后端定稿 discuss-round-1.md(末行合规标记),draft 保留,界面切轮次视图(SC6 ← FLOW-03) | ✓ VERIFIED | `finalize_g1` **live 全链条**实测(末行恰 `> 申请授权:否`、draft 字节不变、重复定稿 FileExistsError、derive_state 判 phase3/current_round=1)+ test_g1 6 用例 + HTTP 契约(200/409 幂等/无 draft 400);前端 direct-through 接线(决策门选项 A,记录于 SUMMARY 04) |
| 7 | SDK 与子进程两路线界面上行为一致、可配置替换、无需改前端(SC7 ← AI-01, AI-03) | ✓ VERIFIED | `make_ai_caller` 工厂切线用例 + **两路线各真实跑一次**(同一 kind 枚举终止于 done)+ `POST /api/config` 运行时换线(HTTP 契约实测写回生效,config.json 原子写)+ 前端只有 routeSelect 下拉,无路线分支代码;SDK 路线 ClaudeSDKClient 单事件循环 + 子进程路线双向控制协议,normalize 纯函数两套同构测试 |
| 8 | 权限门按 §5.4 矩阵:DESIGN.md/AUTHORIZATION.md 拒、docs/ 放行、项目外/执行弹窗(SC8 ← AI-04) | ✓ VERIFIED | 9/9 矩阵 **live 复测**(PERM-MATRIX-9/9-OK,九断言逐条过);confirm 回环 3 用例(`test_confirm_pends_until_resolved` 挂起→resolve 放行、`test_resolve_permission_deny_reaches_caller` 驳回传回 caller、未知 id 404);两路线 confirm 接线:SDK `can_use_tool` confirm 分支 + 子进程 control_request 应答,均经注入回调无降级;`setting_sources=[]`/`--setting-sources=` 屏蔽全局 allow 绕过(两路线代码在场,SUMMARY 03 记录实测) |

**Score:** 7/8 truths verified(6 项 present-but-behavior-unverified 转人检,见 frontmatter `behavior_unverified_items`——不扣真值分,按角色规则单独上报)

### User Flow Coverage(MVP 模式)

> **格式差异说明(非缺陷):** 本阶段 ROADMAP 标注 `Mode: mvp`,但 goal 是中文结果陈述而非英文 "As a…, I want to…, so that…" 格式,`user-story.validate` 判 `valid: false`——该验证器是英文正则,对全中文 goal(本 ROADMAP 三个阶段皆是)恒不通过。goal 的**实质**是一个完整的用户流结果陈述,各 PLAN.md 内亦各有中文 As-a/I-want/So-that 形态的 goal,故本报告按实质继续 goal-backward 验证(上表 8 条 SC 即操作契约),不因此拒绝验证。如需严格合规可运行 `/gsd-phase` 重排 goal 为故事格式,但这是工具链格式问题,不影响本阶段目标达成度的判定。

用户流(goal 全句)逐步映射:

| Step | Expected | Evidence | Status |
|------|----------|----------|--------|
| 打开应用(bash run.sh → localhost:8765) | 单页呈现;CLI 自检过即不挡 | run.sh(venv 自举 + uvicorn:8765,幂等)+ main.py 静态挂载 + Task 3 verify e2e-ok(uvicorn 起首页含 `<html>`)+ CLI 自检接线(真值 1) | ✓ |
| 选中/输入项目目录进入 | 状态按磁盘推导呈现 | /api/enter HTTP 实测三种目录形态返回对的状态与载荷(真值 2) | ✓ |
| 没想法 → 点「没想法」 | 发散直播,brainstorm.md 落盘,可反复覆盖;雏形诞生即入口关闭 | 模板/触发/覆盖/关闭四环测试 + HTTP 202/409(真值 5) | ✓(浏览器点击体验 → 人检) |
| 会话流发消息 | [user]/[ai] 落盘、事件直播、草稿演进 | session 用例 + E2E 真跑(真值 3、4 直播半边) | ✓ |
| 点「中止」 | 当前调用被杀、服务器存活 | **会话路径实测定点失败**(真值 4 中止半边) | ✗ |
| 点「认可雏形」 | discuss-round-1.md + 标记行 + 切轮次视图 | G1 live 全链条 + HTTP + 前端接线(真值 6) | ✓(浏览器点击体验 → 人检) |
| 杀进程重启 | 一切从磁盘恢复 | E2E test_restart_recovery(真实 CLI,importlib.reload 模拟重启) | ✓ |

### Required Artifacts

机器验证(`verify.artifacts`)+ 逐文件通读(存在/实质/接线三层):

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `backend/ai_caller.py` | AICaller 抽象 + 双实现 + 权限路由 | ✓ VERIFIED | 642 行实质实现;`make_permission_decision` §5.4 矩阵 + `normalize_stream_line`/`normalize_sdk_message` 纯函数 + SDK 事件循环架构 + 子进程双向控制协议;ask_lite 签名预定义(D-P1-6)按计划 NotImplementedError |
| `backend/main.py` | FastAPI 应用全路由 | ✓ VERIFIED(abort 路由除外) | 15 路由全在场(health/events SSE/abort/dev/ping/cli-check/config/enter/message/permission/draft/transcript/divergence/brainstorm/g1);SSE `asyncio.to_thread` 防冻结;**/api/abort 的会话接线缺失(gap)** |
| `backend/session.py` | 会话状态管理全链 | ✓ VERIFIED(abort 的接线上游 gap) | enter/send_message 流水线(pending 权限队列 uuid+Event 无超时 + abort 强制释放)/resolve/divergence/finalize_g1;模块级单例 + 测试 seam |
| `backend/state.py` | derive_state 八行表 | ✓ VERIFIED | 严格照抄 §7.4 表条件;完整轮判据 exact-match;PASS 前缀匹配;防御兜底回退行 2 |
| `backend/transcript.py` | §6.1 文法 parse/append | ✓ VERIFIED | 整行精确匹配起始行、多行体保留、脏头丢弃、无尾换行容错、父目录自举 |
| `backend/g1.py` | G1 定稿纯函数 | ✓ VERIFIED | FileNotFoundError/FileExistsError 防护、rstrip+空行+标记行文法、draft 保留 |
| `backend/prompts.py` | 阶段 1-2 提示词 + 发散模板 | ✓ VERIFIED | 四段结构 + §3.8 红线;发散三步走 + 4 固定视角 + 覆盖落盘指令 |
| `backend/cli_check.py` | CLI 自检 | ✓ VERIFIED | which + `claude -p ping` 30s 超时,两分支中文指引 |
| `backend/config.py` | read_config/make_ai_caller | ✓ VERIFIED | 失败回落 sdk、原子写、工厂切线 |
| `backend/events.py` | EventBroker | ✓ VERIFIED | register/unregister/publish,Lock 保护,满队列丢最旧 |
| `frontend/index.html` | 单页三区骨架 | ✓ VERIFIED | 进入表单/draft-view/rounds-placeholder/会话流/工作面板/权限弹窗/CLI 浮层/发散入口/brainstorm 区/approve-row 全在场 |
| `frontend/app.js` | 全部前端逻辑 | ✓ VERIFIED | `node --check` 语法过;dispatchEvent_ 分发/stripUnsafeNodes XSS 防护/applySessionView/renderBrainstorm/direct-through G1/发散点击;20K 行无桩 |
| `frontend/style.css` | 布局与样式 | ✓ VERIFIED | 358 行;§4.1 flex 布局、折叠、气泡、模态、徽标 |
| `frontend/vendor/marked.min.js` | vendored 渲染库 | ✓ VERIFIED | marked v12.0.2 官方单文件发行版(头注释确认),无 CDN 依赖 |
| `run.sh` | 一键启动 | ✓ VERIFIED | venv 自举(幂等:检查 .venv/bin/uvicorn)+ exec uvicorn:8765 |
| `backend/tests/*`(6 文件) | 测试资产 | ✓ VERIFIED | 64 用例(15 ai_caller + 17 state + 11 transcript + 13 session + 6 g1 + 2 e2e)= 62 passed + 2 skipped(IDI_E2E 门控的 slow 对,已实跑转 2 passed) |

**注:** PLAN 03/04 的 artifacts 字段写了 `frontend/app.js(扩展)`、`backend/prompts.py(扩展)` 字面路径,`verify.artifacts` 按字面量找文件报 not-found——这是计划书写法问题,实际文件存在且本表已逐一实质验证,不构成 gap。

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| backend/main.py | backend/ai_caller.py | SSE 端点 yield AICaller 事件 | ✓ WIRED | 工具验证 Pattern found;dev/ping 路径 + session 流水线双路 publish 到 broker |
| frontend/app.js | /api/events | EventSource 订阅 | ✓ WIRED | `initEventSource()` → `dispatchEvent_` 分发到面板/会话流/弹窗 |
| backend/config.py | backend/ai_caller.py | make_ai_caller 切线 | ✓ WIRED | 工厂 + /api/config 运行时换线(HTTP 实测) |
| backend/state.py | backend/transcript.py | 文件即状态脊柱(设计上无直接调用) | ✓ WIRED(设计如此) | 计划原文即声明「无直接调用」;二者在 session 层合流 |
| backend/session.py | backend/transcript.py | append_message 落盘 | ✓ WIRED | send_message ① [user] 先落盘 + finally [ai] 落盘 |
| backend/main.py | backend/state.py | /api/enter 调 derive_state | ✓ WIRED | enter_project → _session_snapshot → derive_state |
| backend/ai_caller.py | backend/events.py | confirm 分支发 permission_request | ✓ WIRED(依赖倒置形态) | 工具 grep 按两文件字面量未命中(设计即如此:ai_caller 不 import session);人工链路追踪完整:ai_caller `_ask_user_permission`(SDK can_use_tool confirm 分支 / 子进程 control_request confirm 分支)→ session 注入的 `request_permission` → `_register_pending` publish `kind=permission_request` → SSE → 前端 `showPermissionModal` → POST /api/permission → `resolve_permission` → Event 置位回传 caller。session 侧与前端侧双向 grep 均命中 |
| backend/main.py | backend/g1.py | /api/g1 调 finalize_g1 | ✓ WIRED | route → session.finalize_g1 → g1.finalize_g1 纯函数(HTTP 实测 200/409/400) |
| backend/session.py | backend/prompts.py | 发散走 build_divergence_prompt | ✓ WIRED | trigger_divergence → build_divergence_prompt(测试断言 prompt 含发散模板) |

### Data-Flow Trace(Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|--------------|--------|-------------------|--------|
| /api/enter transcript | snapshot["transcript"] | parse_transcript(磁盘) | 是(HTTP 实测 + E2E) | ✓ FLOWING |
| /api/draft、draft 区渲染 | snapshot["draft"] | docs/draft.md 读盘 | 是(HTTP 实测) | ✓ FLOWING |
| /api/brainstorm | snapshot["brainstorm"] | docs/brainstorm.md 读盘 | 是(HTTP 实测) | ✓ FLOWING |
| SSE /api/events | broker.publish ← caller.run 事件 | 真实 AICaller 双路线 | 是(两路线 live kinds 序列) | ✓ FLOWING |
| derive_state | state/current_round | 磁盘文件形态 | 是(live 八行推进实测) | ✓ FLOWING |
| make_ai_caller | config.get("ai_caller") | config.json 读盘 | 是(工厂用例 + HTTP 换线实测) | ✓ FLOWING |
| 界面状态徽标 | STATE_LABELS[data.state] | /api/enter 真实载荷 | 是 | ✓ FLOWING |

无 STATIC / DISCONNECTED / HOLLOW_PROP。

### Behavioral Spot-Checks(本次验证实跑,全部单命令、不改产品状态)

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| 全量回归 | `.venv/bin/python -m pytest backend/tests/ -q` | 62 passed, 2 skipped in 1.62s(与预期基线一致) | ✓ PASS |
| §5.4 权限矩阵 9 分支 | 九断言 live 脚本 | PERM-MATRIX-9/9-OK | ✓ PASS |
| §7.4 八行推导表 | 临时目录逐行推进 live | DERIVE-STATE-8-ROWS-OK | ✓ PASS |
| G1 定稿全链条 | live:标记行/draft md5/幂等/phase3 | G1-FULL-OK | ✓ PASS |
| 发散模板三步结构 | live 结构断言(12 标记) | DIVERGENCE-TEMPLATE-OK | ✓ PASS |
| HTTP 契约(health/enter 三态/g1 200-409-400/divergence 202-409/permission 404) | TestClient 进程内 | HTTP-CONTRACT-ALL-OK | ✓ PASS |
| 子进程路线真实调用 | live claude CLI 一次 | kinds=[command,result,read,result,say,done] | ✓ PASS |
| SDK 路线真实调用 | live claude CLI 一次 | kinds=[command,read,say,done] | ✓ PASS |
| 真实会话一轮 + 重启恢复(E2E) | `IDI_E2E=1 pytest -m slow` | 2 passed in 9.11s | ✓ PASS |
| **会话中途中止** | TestClient:在飞 send → POST /api/abort | killed:false,caller 存活,busy 卡死  
(对照:直调 session.abort() 一切正常) | ✗ FAIL |
| 模块可导入性 | import 全部 9 后端模块 | ALL-IMPORTS-OK | ✓ PASS |
| JS 语法 | `node --check frontend/app.js` | JS-SYNTAX-OK | ✓ PASS |

### Probe Execution

无 `scripts/*/tests/probe-*.sh` 类仓库探针(本阶段 PLAN 的探针为内联 verify 命令,执行者按 SUMMARY 记录经 /tmp 同语义脚本跑过;判据行回执见各 SUMMARY 自检)。等效验证由上表行为抽检承担(含两路线 live 与 E2E),不另设探针。

### Requirements Coverage(10/10 全账)

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| FLOW-01 | 02, 03 | 目录进入 + 状态推导 | ✓ SATISFIED | derive_state 17 用例 + live 八行 + /api/enter HTTP 实测 |
| FLOW-02 | 03 | 阶段 1-2 连续会话 + transcript 恢复 | ✓ SATISFIED | session 用例 + E2E 真跑(restart_recovery 含) |
| FLOW-03 | 04 | G1 后端定稿 + 标记行 | ✓ SATISFIED | test_g1 6 用例 + live + HTTP;draft 保留 |
| FLOW-06 | 04 | 发散模式四条 | ✓ SATISFIED | 模板/触发/覆盖/关闭四环测试 + HTTP 202/409 |
| UI-03 | 03 | 单界面三区 + 阶段视图 | ✓ SATISFIED(接线) | HTML/JS 结构与接线验证;视觉呈现转人检(CONTEXT deferred 项按计划收口批注交互在 Phase 2) |
| AI-01 | 01 | 无状态文件驱动调用 | ✓ SATISFIED | build_phase12_prompt 每次从磁盘读 docs/ 全文档(test_send_message_pipeline 断言注入) |
| AI-02 | 01 | 事件直播 + 中止 | ⚠️ PARTIAL | 直播已验(两路线 live + SSE);**会话路径中止失败(gap)**;唯一缺口,修复面一行路由 + 一条测试 |
| AI-03 | 01 | 双轨可替换 | ✓ SATISFIED | 工厂 + 双路线 live 同 kind 枚举 + 运行时换线 |
| AI-04 | 01, 03 | 权限门完整矩阵 | ✓ SATISFIED | 9/9 live + confirm 回环 3 用例 + 两路线接线 |
| AI-05 | 01 | CLI 自检只挡第一次 | ✓ SATISFIED | 两分支文案 + 端点不缓存 + 前端浮层;失败分支视觉转人检 |

无 ORPHANED 需求:REQUIREMENTS.md 映射到 Phase 1 的 10 个 ID 全部出现在计划 frontmatter 中;Traceability 表 10 行全部勾选 Complete,与实际代码证据相符(仅 AI-02 因上述 gap 应视为部分完成)。

### Test Quality Audit(禁用测试/循环测试扫描)

- **禁用测试:** 唯二 skip 是 `test_e2e_smoke.py` 的 `IDI_E2E` 环境门控(设计如此,本次验证已设 `IDI_E2E=1` 实跑转 2 passed)——不是禁用测试;其余 62 用例无 skip/xfail/todo。
- **循环测试:** 测试目录无写 fixture 的生成脚本;E2E 断言的是行为结果(消息序列、文件存在性),非系统自产基线。
- **真实依赖测试的忠实性:** E2E 用真实 CLI(本机已登录),非 mock 充数。

### Decision Coverage(非阻塞门,step: verify_decisions)

`check.decision-coverage-verify`:**15/15 decisions honored, 0 not_honored** — CONTEXT 全部 D-P1-1..15 决策(技术栈、目录结构、SDK 双轨、SSE、权限矩阵、文件即状态、G1 后端动作、发散模板、单页三文件、阶段 1-2 视图形态)在交付物中均有落点。(此门为 warning-only,不影响状态判定;本次全绿。)

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| (无 TBD/FIXME/XXX/PLACEHOLDER 标记;无空实现桩;无 console.log-only) | — | — | — | 全仓 grep 零命中 |
| backend/main.py | 235-241 | /api/abort 会话接线缺失 | 🛑 Blocker(gap 主体) | 见 Gaps Summary |
| (仓库未跟踪文件 `.gsd/`、`.planning/state.json`) | — | 工具运行时产物未纳管 | ℹ️ Info | GSD 工具自生产物,非本阶段交付内容;建议入 .gitignore 或纳入管理,无碍目标 |
| (CLI stderr `unrecognized_model` 噪声) | — | 本机环境代理模型名噪声 | ℹ️ Info | SUMMARY 01/03 已记录;本次 SDK live 探针 kind 序列干净([command,read,say,done]),事件流不受污染,环境性非缺陷 |

### Human Verification Required

(overall status 为 gaps_found,人检项按角色规则保留在 frontmatter `behavior_unverified_items`;gap 修复后这些将升为 human_needed 待办)

1. **浏览器端到端 UAT(主批次)** — 空白临时目录进入 →「没想法」发散 → 看 brainstorm 候选 → 会话流发所选方向 → 草稿出来 → 点「认可雏形」→ 界面切「第 1 轮」占位(Plan 04 verification 第 5 条、Plan 01 第 4 条、Plan 03 第 5 条的三段人检合并为此一条主链)。
2. **SSE 面板直播亲检** — 发起会话消息,亲眼见事件逐条渲染(say markdown / read/write/command 路径 / result 折行),面板折叠可用。
3. **权限弹窗交互亲检** — 诱导一次越权写,弹窗同意/拒绝各点一次,看放行/驳回效果(session 层已有单测,浏览器回路待人检)。
4. **CLI 自检失败分支视觉** — 未装/未登录两分支指引浮层与「重新检测后放行」(本机 CLI 常态无法触发)。
5. **视觉样式目检** — 气泡对齐、模态布局、草稿排版、发散候选虚线框。
6. **重启浏览器体验** — 关页重开重进同目录,会话流与草稿完整恢复。

### Gaps Summary

**1 个 BLOCKER(修复面小、已精确定位):会话路径的「中止」按钮失灵。**

- **现象(实测):** 会话调用(浏览器「发送」触发的 `send_message`/`trigger_divergence` 流水线)在飞时点「中止」,`POST /api/abort` 返回 `{killed: false}`,AI 调用进程不被杀,busy 锁不释放——用户只能等 AI 自然收尾,期间发消息/发散/定稿全部 409。SC4 的「随时能杀掉当前调用」在主用户流上不成立。
- **根因:** `backend/main.py` 的 `/api/abort` 路由只查 `main._current_caller`(只有 `/api/dev/ping` 探针线程会设置它),从不调 `session.abort()`。而 `backend/session.py` 的 `abort()` 本身完备(caller.abort + 挂起权限强制释放 + inflight 解锁——我直调实测全部生效)。**这是 Plan 03 会话层接管 caller 管理后遗留的接线缺口**:Plan 01 时代 caller 归 main 管(探针路径中止 PASS 是真的),Plan 03 把 caller 挪进 session 后 `/api/abort` 没跟着改;现有 `test_abort_leaves_no_dirty_ai_entry` 直调 `session.abort()` 不经 HTTP 路由,所以测试全绿但接线断了——正是 SUMMARY CLAIMS ≠ CODE 的典型形态。
- **修复(供 /gsd-plan-phase --gaps 直接消费):** main.py `/api/abort` 接入 `session.abort()`(会话在飞时优先;dev/ping 路径保持 _current_caller 中止);补一条经 HTTP 路由的会话中止行为测试(FakeAICaller 在飞 → POST /api/abort → caller.abort 被调 + busy 释放 + transcript 无脏 [ai])。
- **其余全部干净:** 除此外 7/8 真值、10/10 需求的机器可验部分、15 决策、9 工件、9 链路、全部测试(含真实 CLI E2E)均验证通过;浏览器视觉/交互 6 项按计划转人检。

---

_Verified: 2026-09-09T09:18:23Z_
_Verifier: Claude (gsd-verifier)_

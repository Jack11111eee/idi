---
phase: idi-01
plan: 03
type: execute
wave: 2
depends_on: ["idi-01-01", "idi-01-02"]
files_modified:
  - backend/main.py
  - backend/session.py
  - backend/ai_caller.py
  - backend/prompts.py
  - backend/tests/test_session.py
  - frontend/index.html
  - frontend/app.js
  - frontend/style.css
autonomous: true
requirements:
  - FLOW-02
  - UI-03
  - AI-04

estimate:
  tokens: 90000
  raw_tokens: 90000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "用户选中项目目录进入后,界面按 derive_state 结果呈现对的状态与视图:阶段 1-2 显示草稿区 + 会话流,阶段 3+ 显示轮次最小占位"
    - "用户在会话流发一条消息,后端先追加 [user] 到 transcript.md,再发起一次全新无头 AI 调用(读 docs/ 全部文档),AI 每条回复段落在结束后追加 [ai] 落盘"
    - "浏览器/进程杀掉重启后重进同一目录,会话流从 transcript.md 完整恢复,草稿区继续显示 draft.md 内容"
    - "权限门三态闭环:AI 尝试写 docs/ 内文件自动放行;AI 直写 DESIGN.md 或 AUTHORIZATION.md 被拒绝;写项目内 docs/ 外路径时前端弹同意对话框,点同意放行、点拒绝驳回"
  artifacts:
    - path: "backend/session.py"
      provides: "会话状态管理:进入项目(set current project)、发消息流水线(append user → AI 调用 → append ai)、权限确认挂起队列"
      contains: "def send_message"
    - path: "backend/prompts.py"
      provides: "阶段 1-2 系统提示词模板(docs/ 全文档注入 + §3.8 语言红线 + draft 维护指引)"
      contains: "def build_phase12_prompt"
    - path: "backend/tests/test_session.py"
      provides: "会话流水线与权限确认队列的 pytest 用例(受死进程,不起真 AI)"
    - path: "frontend/app.js(扩展)"
      provides: "进入项目/发消息/SSE 会话渲染/权限弹窗/草稿区 markdown 渲染"
  key_links:
    - from: "backend/session.py"
      to: "backend/transcript.py"
      via: "消息发出与 AI 回复均经 append_message 落盘"
      pattern: "append_message"
    - from: "backend/main.py"
      to: "backend/state.py"
      via: "POST /api/enter 调 derive_state 决定返回给前端的状态载荷"
      pattern: "derive_state"
    - from: "backend/ai_caller.py"
      to: "backend/events.py"
      via: "权限 confirm 分支 publish permission_request 事件,前端弹窗回传 /api/permission 决定"
      pattern: "permission_request"
---

## Phase Goal

**As a** 讨论中的用户,**I want to** 在阶段 1-2 连续会话里发消息、看 AI 回复与草稿实时演进,并在 AI 要越权写文件时被弹窗拦下,**so that** 我与 AI 的完整讨论可追溯、可重启恢复,且我的文件系统不暴露危险面。

<objective>
把 Plan 01 骨架与 Plan 02 脊柱接线成真正的阶段 1-2 会话:进入项目端点(状态推导)、发消息流水线(transcript 追加 + 无头调用 + AI 回复落盘 + 草稿演进)、前端会话流与草稿区渲染、权限门 confirm 弹窗闭环(UI-03 的阶段 1-2 视图 + 最小轮次占位)。重启恢复:重进目录,会话流与草稿从磁盘完整读出。

Purpose: FLOW-02 是本阶段核心交互闭环;AI-04 的完整矩阵在真实调用上闭合(含用户弹窗),保护的是用户文件系统(D-P1-9)。
Output: 可用浏览器走一段真实阶段 1-2 会话的工具(含重启恢复)。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/phases/idi-01-1-2/01-CONTEXT.md
@.planning/phases/idi-01-1-2/idi-01-01-SUMMARY.md

依赖接口(来自 Wave 1,直接使用,不重定义):
- backend/ai_caller.py:make_ai_caller(config) → AICaller;caller.run(project_path, prompt) 生成器产 {kind, content, ...} 事件(kind ∈ say/read/write/command/result/error/done);caller.abort();make_permission_decision(project_path, action, target) → allow/reject/confirm;事件经 events.EventBroker publish
- backend/state.py:derive_state(path) → {state, current_round, current_check}
- backend/transcript.py:parse_transcript(path)、append_message(path, role, content)

DESIGN.md 权威依据:
- §5.1(无状态:每次调用 = 全新无头,启动自磁盘读 docs/ 全部文档)
- §5.4 权限矩阵(confirm 三类:写项目内 docs/ 外、读项目外、任何执行)与 AI 写 docs/ 自动放行
- §4.1/§4.2 布局与阶段 1-2 交互(左侧草稿、右侧会话流;无划词批注)
- §6.1 transcript.md(后端在用户发送 / AI 回复时追加)
- §3.8 语言红线(注入 system prompt)
- §4.4 G1 前的 draft.md 格式自由(阶段 1-2 的 AI 不要求按 §6.3 模板维护 draft)
</context>

<tasks>

<task type="auto" tdd="true">
  <name>Task 1: 发消息流水线与权限确认队列(后端会话层)</name>
  <reversibility rating="costly">权限确认的 SSE 事件名与 POST /api/permission 契约被前端依赖,Phase 2 大白话调用复用同一回路。</reversibility>
  <behavior>
    - 用例 1:send_message(project_path, user_text) 依次产生:transcript 追加一条 [user]、AI prompt 组装含 docs/ 全部文档内容、调用完成后追加 [ai] 条目(content = 消化后全文)
    - 用例 2:AI 输出为多段时,[ai] 条目作为一条多行消息落盘(不是多条)
    - 用例 3:权限确认队列:判定函数返回 confirm 时挂起任务、登记 pending_permission(id 与 tool 参数),释放前 AI 调用线程阻塞
    - 用例 4:resolve_permission(id, approved=True) 放行挂起调用;approved=False 时 AICaller 收到拒绝结果(abort 或向进程发拒绝事件,按实现文档化)
    - 用例 5:abort 调用后 transcript 无半条脏 [ai](中止时未完成的 AI 回复不落盘)
    - 用例 6:build_phase12_prompt:注入用户消息、历史 transcript、draft.md 现状、docs/ 文档清单与内容、§3.8 语言红线句
  </behavior>
  <files>backend/prompts.py, backend/session.py, backend/ai_caller.py, backend/tests/test_session.py</files>
  <action>(1)backend/prompts.py:build_phase12_prompt(project_path, user_message) -> str,拼装四段:系统段(角色 = 项目前的讨论搭档;§3.8 语言红线原文要义:简洁精准、术语先用一句大白话定义、一次讲透一个小点);资料段(docs/ 目录下各文档——transcript.md 历史、draft.md 现状、brainstorm.md 若存在——以文件名标题 + 全文注入;docs/ 为空时说明「这是全新讨论」);任务段(用户本次消息;阶段 1-2 会话指令:目标是对齐需求与雏形,产出会持续演进 docs/draft.md 草稿,草稿格式自由,但每次有实质进展时应更新草稿文件)。

(2)backend/session.py:模块级会话管理(单机单人,一个当前项目足矣)。current_project: Path|None 与 threading.Lock;enter_project(path) 校验目录存在后 Set,返回 derive_state 结果;send_message(user_text):完整流水线——append_message(transcript, "user", user_text) → build_phase12_prompt → 后台线程起 caller.run(current_project, prompt):事件逐条 publish 到 broker(前端在 SSE 上收);调用期间累积 say 文本;调用 done 且非 abort 时把累积文本 append_message(transcript, "ai", 累积文本)(多段合一条,多行体文法);abort() 委托 caller.abort()。权限确认队列:pending 字典 {id: threading.Event + decision};AICaller 的 confirm 分支调用 request_permission(tool, params) → publish 一个 kind=permission_request 事件(带 id 与工具参数摘要)并阻塞等待 Event;POST 侧 resolve_permission(id, approved) 设置 Event 与决定,函数返回决定给 AICaller;超时策略 = 无超时(用户慢慢看,阻塞保留),但 abort 流程会强制 release 所有 pending 为 False。

(3)backend/ai_caller.py 扩展confirm 分支(替换 Plan 01 的"默认 reject + 日志"过渡实现):SdkAICaller 的权限回调接入 session 提供的 request_permission(经构造函数注入回调,保持 ai_caller 不直接 import session——依赖倒置,主模块注入);SubprocessAICaller 的 confirm 分支:claude CLI 的权限模式跑 --permission-mode ask 或等效(按 CLI 实际支持情况;若 CLI 无每操作回调形态,则用 --allowedTools 不含危险工具 + 拒绝清单模式实现 etc——实现时查 CLI 文档,把 confirm 类操作默认排除在 allowed 外、经 request_permission 用户同意后重试单条命令的实现路径不必须:子进程路线可简化为"confirm 一律拒绝并附中文说明事件",但 SDK 路线必须完整闭环)。若走此简化,必须在 SUMMARY 记录限制与理由。

(4)backend/tests/test_session.py:用 FakeAICaller(伪造 caller,产固定事件序列,含 say/read/write 事件与可注入的 confirm 场景)测六个 behavior 用例,所有用例不起真 claude 进程。send_message 全流水线用直接调(不 via FastAPI)。先红后绿。</action>
  <verify>
    <automated>bash -c 'cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_session.py -q 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1'</automated>
  </verify>
  <fails_when>任一 pytest 输出含 failed 或 error;用例数 < 6(session);全量测试回归少于 state(10)+ transcript(6)+ ai_caller(3)+ session(6)基线。</fails_when>
  <done>六用例全绿 + 全量回归绿;权限弹窗回路后端语义完备(confirm 阻塞 → resolve → 放行/拒绝;abort 强制释放)。</done>
</task>

<task type="auto">
  <name>Task 2: 会话与草稿的前端视图(UI-03 的阶段 1-2 形态)</name>
  <files>backend/main.py, frontend/index.html, frontend/app.js, frontend/style.css</files>
  <action>(1)backend/main.py 挂正式会话路由:POST /api/enter {path} → session.enter_project 返回 {state, current_round, current_check, transcript: [...], draft: str|null, brainstorm: str|null};POST /api/message {text} → session.send_message(异步起,立即 202);POST /api/permission {id, approved} → session.resolve_permission;GET /api/draft → 当前 draft.md 内容(供前端在流中拉新);GET /api/transcript → 全量消息列表(备用拉)。保留 /api/health、/api/events、/api/abort、/api/dev/ping(dev 探针继续可用)。

(2)frontend 三文件扩展(不重写骨架结构):index.html——进入表单(目录路径输入 + 进入按钮 + CLI 指引浮层位置);文档区拆两个子视图容器「draft-view」(markdown 渲染区 + 底部「认可雏形」按钮位——按钮禁用态,Task 3/Plan 04 才实现点击)与「rounds-placeholder」(阶段 3+ 时显示「已进入轮次阶段(本阶段占位)」+ 当前轮号,导自 derive_state);侧栏会话流区:消息列表(用户右对齐气泡、AI 左对齐、AI 文本过 marked.parse)+ 底部输入框 + 发送按钮;工作面板保持 Plan 01 形态;页面右上角显示当前推导状态中文名。app.js——initEventSource 扩展消息分派:kind=say 流式插到工作中的会话气泡;kind=permission_request 弹模态确认框(说明工具与目标路径,同意/拒绝两按钮,点后 POST /api/permission);kind=done 收尾会话气泡并可轮询 /api/draft 刷新草稿区;enterProject()/sendMessage() 两个 fetch 封装;进入后按返回 state 切换 doc 区子视图与侧栏会话流(将 transcript 历史渲染出来)。style.css 增加:会话气泡样式、模态确认框样式、子视图切换的 hidden 类。(3)重启恢复语义:重新 POST /api/enter 同一目录,transcript 与 draft 从磁盘全量重渲染——不需要专门"恢复"按钮(文件即状态)。</action>
  <verify>
    <automated>bash -c 'cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && (.venv/bin/uvicorn backend.main:app --port 8766 &) && sleep 2 && D=$(mktemp -d) && mkdir -p $D/docs && printf "[user]\n你好\n" > $D/docs/transcript.md && curl -sf -X POST http://localhost:8766/api/enter -H "Content-Type: application/json" -d "{\"path\": \"$D\"}" | grep -o "\"state\": \"phase12_in_progress\"" && lsof -ti:8766 | xargs kill; echo "enter-ok"'</automated>
  </verify>
  <fails_when>curl -sf 失败或响应含非 phase12_in_progress 的 state(grep -o 无输出返回非零),uvicorn 起不来,无 enter-ok。</fails_when>
  <done>构造磁盘现状(有 docs/ 无完整轮)→ /api/enter 正确返回 phase12_in_progress + transcript 列表;前端视图切换与会话流可用;权限弹窗与同意/拒绝按钮存在。已 commit。</done>
</task>

<task type="auto">
  <name>Task 3: 端到端冒烟——真实会话一次 + 重启恢复 + 权限闭环</name>
  <precondition>/api/enter 已可用(Task 2 automated 过)且 claude CLI 已登录(Plan 01 自检过)。</precondition>
  <files>backend/tests/test_e2e_smoke.py</files>
  <action>新建 backend/tests/test_e2e_smoke.py 两个标记为 slow 的 pytest 用例(测试函数头加 @pytest.mark.slow,并在 pytest 配置注册 marker;环境变量 IDI_E2E 未设时 skip——常规跑不依赖真 AI):(1)test_full_conversation_roundtrip:mktemp 造项目目录,调 session.enter_project + send_message(消息:「请向我介绍你自己,一句话即可」,不要求写 draft),轮询 transcript 文件出现 [ai] 条目后断言 parse_transcript 得 [user, ai] 序列;(2)test_restart_recovery:上一用例后新起一枚 session 实例(模拟重启:重建 session 模块状态),重进同目录,断言 transcript 恢复且 draft(若产生)可读。权限闭环以 FakeAICaller 在 test_session.py 中覆盖(单元级),本任务不重复。执行本任务时把两用例真正跑一遍(IDI_E2E=1),确认通过。</action>
  <verify>
    <automated>bash -c 'cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && IDI_E2E=1 .venv/bin/python -m pytest backend/tests/test_e2e_smoke.py -q -m slow 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1'</automated>
  </verify>
  <fails_when>slow 用例 failed/error,或在 IDI_E2E=1 下输出含 skipped(真实依赖链路未验证),或全量回归非绿。</fails_when>
  <done>真实 claude 依赖端到端链条经一次真调用验证;重启恢复经新会话实例验证;suite 全绿。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 浏览器 → FastAPI | 消息文本、路径、权限决定均用户输入 |
| AI 调用 → transcript.md/draft.md 写入 | 写 docs/ 放行;内容为 AI 产出,落盘前不解析执行 |
| AI 调用 → 权限门 confirm 面 | 项目外路径与命令执行必须过用户弹窗 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi03-01 | Escalation of Privilege | confirm 弹窗回路被绕过(前端直接 POST /api/permission 未展示) | high | mitigate | permission id 必须来自后端生成的挂起队列(随机 uuid),resolve 未知 id 一律 404;驳回即终 |
| T-idi03-02 | Tampering | AI 生成内容注入脚本/HTML 进前端(markdown XSS) | high | mitigate | marked 渲染关闭 raw HTML(marked({async:false}) 配置或 sanitize;或渲染前 HTML escape)+ CSP meta 标签 |
| T-idi03-03 | Tampering | AI 骚扰性反复请求权限(弹窗轰炸) | medium | mitigate | 单次调用内同类 confirm 聚合;拒绝后同类工具直接拒 |
| T-idi03-04 | Denial of Service | send_message 并发重入打乱 transcript 顺序 | medium | mitigate | 会话级 Lock:同一时刻只允许一个在飞调用,进行中再 send 返回 409 |
</threat_model>

<verification>
1. pytest backend/tests/test_session.py:流水线与权限队列(6 用例)
2. pytest 全量回归(含 Plan 01/02 用例)
3. /api/enter 冒烟:构造目录 → phase12_in_progress
4. slow E2E:真实调用一次 + 重启恢复(需要 CLI 已登录)
5. 人检(UAT 批次):浏览器走一遍——进入、发消息、看直播、权限弹窗伪装场景(可选)、重启后恢复
</verification>

<success_criteria>
- 阶段 1-2 会话双句落盘([user] 即时、[ai] 于调用完成)
- 重启后 transcript/draft 从磁盘恢复,无专门恢复操作
- 权限 confirm 弹窗闭环(同意放行/拒绝驳回),AI-04 三类弹窗、DESIGN.md/AUTHORIZATION.md 拒绝、docs/ 自动放行
- UI-03:单界面呈现文档区 + 侧栏会话流 + 工作面板;阶段 3+ 显示最小轮次占位
</success_criteria>

<output>
Create `.planning/phases/idi-01-1-2/idi-01-03-SUMMARY.md` when done
</output>

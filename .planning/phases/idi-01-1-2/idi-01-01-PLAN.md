---
phase: idi-01
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - requirements.txt
  - run.sh
  - .gitignore
  - backend/__init__.py
  - backend/config.py
  - backend/cli_check.py
  - backend/ai_caller.py
  - backend/events.py
  - backend/main.py
  - frontend/index.html
  - frontend/app.js
  - frontend/style.css
  - frontend/vendor/marked.min.js
autonomous: true
requirements:
  - AI-01
  - AI-02
  - AI-03
  - AI-05

estimate:
  tokens: 90000
  raw_tokens: 90000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "bash run.sh 启动后,浏览器打开本地地址立即呈现单页面(左文档区/右侧栏布局),未装或未登录 claude CLI 时出现指引文案而非崩溃"
    - "在页面输入一个临时项目目录并进入后,触发一次真实 AI 无头调用,其每条事件(说话/读文件/写文件)逐条出现在右侧工作面板"
    - "backend 配置项切换 AICaller 实现路线(SDK 或子进程)后,前端零改动,面板行为一致"
    - "点「中止」按钮,当前 AI 调用被杀死,服务器不崩、后续操作可继续"
  artifacts:
    - path: "backend/ai_caller.py"
      provides: "AICaller 抽象接口(SubprocessAICaller 实现 + 权限路由层 + 轻量调用接口签名)"
      contains: "class AICaller"
    - path: "backend/main.py"
      provides: "FastAPI 应用:/api/health、/api/events SSE 流、/api/abort、/api/dev/ping(Task 2 增 /api/cli-check、Task 3 增 /api/config)"
      contains: "StreamingResponse"
    - path: "frontend/index.html"
      provides: "单页骨架:文档区 + 侧栏(会话流占位 + AI 工作面板可折叠)"
    - path: "run.sh"
      provides: "一条本地全栈启动命令(venv 自举 + uvicorn 启动)"
    - path: "backend/cli_check.py"
      provides: "claude CLI 已装+已登录自检"
      contains: "def check_claude_cli"
  key_links:
    - from: "backend/main.py"
      to: "backend/ai_caller.py"
      via: "SSE 端点把 AICaller 产生的事件逐条 yield 到浏览器"
      pattern: "AICaller"
    - from: "frontend/app.js"
      to: "/api/events"
      via: "EventSource 订阅 SSE 流,事件渲染进工作面板 DOM"
      pattern: "EventSource"
    - from: "backend/config.py"
      to: "backend/ai_caller.py"
      via: "配置项选择 AICaller 实现路线"
      pattern: "make_ai_caller"
---

## Phase Goal

**As a** 单人开发者用户,**I want to** 启动本工具、通过 CLI 自检后看到单界面并把一次真实 AI 调用的全过程直播在右侧工作面板里,**so that** 整个"服务器 + 前端 + AI 双轨调用 + 事件直播"骨架被端到端打通,后续一切阶段叠在这条被证明的链路上。

<objective>
行走骨架追踪弹(tracer):用最薄的一条端到端路径打通 Phase 1 的全部架构层——venv 脚手架 → FastAPI 服务器 → 静态单页界面 → claude CLI 启动自检 → AICaller 双轨抽象(SDK 首选 + 子进程兜底,接口契约一致)→ SSE 事件直播到工作面板 → 中止。本计划交付的是可保留的生产骨架,不是原型:后续阶段(会话/批注/轮次)全部在这套文件上扩展,不推翻。

Purpose: 一条链路证明所有架构决策(前后端结构、双轨 AICaller、SSE、文件即状态)可行,并在代理最优质的早期上下文里暴露架构死路(而不是在十个已提交的层之后)。
Output: 可 `bash run.sh` 一键启动的本地工具雏形 + 双轨 AICaller + 事件直播面板 + CLI 自检。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/idi-01-1-2/01-CONTEXT.md

DESIGN.md 权威依据:
- §5.3(双轨实现路线)、§5.1(无状态文件驱动)、§5.2(事件直播)、§5.5(中止)、§9(技术栈)
- §7.1(启动自检 claude CLI)、§3.8(语言红线,注入 system prompt)
- §4.1/§4.3(布局与工作面板:左文档区/右侧栏、全量事件、可折叠)

执行约定:
- 工具自身仓库的 docs/、DESIGN.md、CLAUDE.md、.planning/ 为既有产物,严禁触碰(D-P1-4)
- 代码标识符、命令、路径用英文;面向用户(prose/界面文案)用中文
- 本阶段不引入任何后续阶段的功能(无批注、无轮次循环);骨架允许的功能空缺仅限"后续可无架构变更地填入"
</context>

<tasks>

<task type="tracer">
  <name>Task 1: 端到端追踪弹——服务器启动→页面呈现→一次子进程 AI 调用的 SSE 事件直播</name>
  <reversibility rating="costly">目录布局(backend/+frontend/)与 SSE 事件通道形态被 Phase 2/3 全部叠加使用,变更需协调多调用点。</reversibility>
  <precondition>本机已装 claude CLI 且已登录(命令 claude --version 能出版本号)——AI-05 自检目标即此事实,运行时用户可按指引补装。</precondition>
  <files>requirements.txt, run.sh, .gitignore, backend/__init__.py, backend/config.py, backend/ai_caller.py, backend/events.py, backend/main.py, frontend/index.html, frontend/app.js, frontend/style.css, frontend/vendor/marked.min.js</files>
  <behavior>
    - GET /api/health 返回 200 与 JSON(status: ok)
    - AICaller 子进程路线对临时目录里一个真实任务发起调用,产出的事件流被 SSE 逐条转发
    - 前端 EventSource 收到事件后,工作面板 DOM 里追加对应条目(说话/读文件/写文件可区分)
    - GET /api/abort 进行中调用后,子进程被杀死、SSE 流以终止事件收尾
  </behavior>
  <action>搭通最薄端到端路径,一次 Write 每文件、不可中途留桩。分五个部分:

(1)脚手架:创建 requirements.txt(fastapi、uvicorn、claude-agent-sdk 三项,固定到当前可用版本),创建 run.sh:检查 .venv 存在与否(不存在则 python3 -m venv .venv 并 pip install -r requirements.txt),然后 exec .venv/bin/uvicorn backend.main:app --port 8765(端口可按序换用,仅此一个自定义值)。把 .venv/ 追加进 .gitignore。

(2)backend/config.py:定义 make_ai_caller() 工厂与 read_config()。配置来源 = 仓库根 config.json(新增文件属骨架,提供默认 {"ai_caller": "sdk"}),字段 ai_caller ∈ {sdk, subprocess},另定义 AI_MODEL 等后续阶段可扩展键。配置读取失败时回落默认 sdk,并在日志注明。

(3)backend/ai_caller.py:定义 AICaller 抽象基类(按 D-P1-5/D-06):核心方法 run(project_path, prompt) 为生成器逐条产出统一事件;轻量调用方法 ask_lite(document_text, quoted_text, question) 按接口契约定义签名并抛 NotImplementedError(Phase 2 实现,D-P1-6——只定义签名,不实现逻辑);abort() 杀当前调用。SubprocessAICaller 实现类:subprocess.Popen 启动 claude -p {prompt} --output-format stream-json --verbose,工作目录 = project_path;逐行读 stdout、解析 JSON 事件,归一化为统一事件字典后 yield。归一化语义(命名 = 事件字段,前端可见,本阶段内自洽):kind ∈ {say, read, write, command, result, error, done},各带 content 与原始 JSON。语料:claude CLI stream-json 的每行是一个 JSON 对象,类型在 type 字段(如 system/assistant/result),assistant 消息内含 tool_use 内容——把 message 文本归 kind=say,tool_use 的 Read/Write/Edit/Bash 归对应 kind,tool_result 归 kind=result。进程退出后按 returncode 产 done 或 error 事件。stderr 逐行归 kind=error。abort() 用 process.terminate()/kill()。权限路由层(实现完整,是本任务核心安全件,per D-P1-9/§5.4):make_permission_decision(project_path, action, target_path) 纯函数,自上而下首条命中返回 allow / reject / confirm 三态——规则序:写且目标是项目根 DESIGN.md 或 AUTHORIZATION.md → reject;写且目标是 DESIGN.md.tmp → allow;写且目标在 docs/ 内 → allow;读且目标在项目内 → allow;写项目内其他位置 / 读项目外 / 写项目外 / 任何执行 → confirm。SubprocessAICaller 在把 prompt 交给 claude CLI 时于 system prompt 段落声明本权限约定(供 AI 遵守;硬执行拦截后续任务扩展,但纯函数与其单测本任务即完备)。系统提示词中注入 §3.8 语言红线原文要义:简洁精准、术语先大白话定义。

(4)backend/events.py + backend/main.py:events.py 维护一个进程内 EventBroker(register/unregister/publish,threading.Lock 保护)。main.py 建 FastAPI app,路由:GET /api/health;GET /api/events 为 SSE 流端点(async def + StreamingResponse media_type text/event-stream,内部订阅 broker 并按行 yield 事件;POST /api/abort 调用当前调用句柄 abort;POST /api/dev/ping 是本任务专属开发探针:接收 {project_path, prompt},在后台线程起 make_ai_caller(config) 的 run(),把产出事件 publish 到 broker,流结束后发布 done 事件。app 静态挂载:app.mount("/", StaticFiles(directory="frontend", html=True))。CORS 不加(同源)。

(5)frontend/index.html + app.js + style.css:index.html 含左文档区(占位文本「文档区」)与右侧栏;侧栏含两个分区:上「AI 工作面板」(默认展开,可点标题折叠——点击切换 class)与下方「会话流占位」。引入 vendored 的 marked.min.js(markdown 渲染库,任选 marked 或 markdown-it 的官方单文件发行版,直接下游文件,不用 CDN——无网络依赖)。script 里写 minimal 逻辑:app.js 里 initEventSource() 建立 EventSource('/api/events'),按事件 kind 渲染到工作面板(say 用 marked.parse 渲染 markdown、read/write/command 显示目标路径、result/error 折行);一个「发起测试调用」按钮 POST /api/dev/ping 传 {project_path: 一个由用户输入框提供的路径, prompt: 固定测试指令},一个「中止」按钮 POST /api/abort。style.css 实现 §4.1 骨架布局(flex 左主右栏)、面板折叠态、事件条目分级颜色。注释一律中文、遵守简单优先——总行数克制。

写完后自查:这条路径 = 启动 run.sh → curl /api/health 得 ok → 浏览器页面加载 → 点发起测试调用 → SSE 事件逐条出现在面板 → 点中止进程死、流收尾。这是后续所有阶段的唯一架构基线。</action>
  <verify>
    <automated>bash -c 'cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt && .venv/bin/python -c "import backend.main; import backend.ai_caller; print(\"imports-ok\")" && .venv/bin/python - <<PYEOF
import sys
sys.path.insert(0, ".")
from backend.ai_caller import make_permission_decision
from pathlib import Path
p = Path("/tmp/fakeproj")
# §5.4 矩阵判定(D-P1-9)
assert make_permission_decision(p, "write", p / "DESIGN.md") == "reject"
assert make_permission_decision(p, "write", p / "AUTHORIZATION.md") == "reject"
assert make_permission_decision(p, "write", p / "DESIGN.md.tmp") == "allow"
assert make_permission_decision(p, "write", p / "docs" / "x.md") == "allow"
assert make_permission_decision(p, "read", p / "src" / "a.py") == "allow"
assert make_permission_decision(p, "write", p / "src" / "a.py") == "confirm"
assert make_permission_decision(p, "read", Path("/tmp/outside.txt")) == "confirm"
assert make_permission_decision(p, "write", Path("/tmp/outside.txt")) == "confirm"
assert make_permission_decision(p, "command", "git status") == "confirm"
print("perm-matrix-ok")
PYEOF'</automated>
  </verify>
  <fails_when>任一 assert 失败(python 进程非零退出、无 perm-matrix-ok / imports-ok 输出行)、requirements 装不上、或 backend.main 不可导入。</fails_when>
  <done>骨架五部分全部就位:/api/health 返回 ok;权限矩阵九个断言全过;AICaller 双文件(接口 + SubprocessAICaller + make_permission_decision)可导入并有单测脚本验证;frontend 三文件 + vendored 渲染库存在;run.sh 可重复执行。本任务代码被 commit。</done>
</task>

<task type="auto">
  <name>Task 2: Claude Agent SDK 路线 + claude CLI 启动自检</name>
  <reversibility rating="costly">AICaller 接口是全部后续阶段的调用面,Phase 2 轻量调用直接叠在 ask_lite 签名上。</reversibility>
  <files>backend/ai_caller.py, backend/cli_check.py, backend/main.py, backend/config.py, config.json, backend/tests/test_ai_caller.py</files>
  <action>(1)backend/cli_check.py:check_claude_cli() 用 shutil.which("claude") 检查已装;再跑 subprocess.run(["claude", "-p", "ping", "--output-format", "json"], capture_output=True, timeout=30) 验证可登录可调用(退出码 0 即视为通过;登录失败/超时返回结构化失败信息)。返回 dict {ok: bool, installed: bool, logged_in: bool, guidance: str};guidance 为中文指引文案,按失败原因两分支:未装 → 「安装 Claude Code CLI:npm install -g @anthropic-ai/claude-code」;未登录 → 「在终端运行 claude 完成登录后回到此页」。

(2)backend/main.py 挂 GET /api/cli-check,调用上述函数;**只挡第一次的语义(:AI-05)**不在后端记忆——前端收到 ok=false 显示指引浮层与「我已装好,重新检测」按钮,用户点重检通过即进;后端不缓存失败、不拒绝后续请求。注意 §7.1「未满足给出指引,只挡第一次进入」。

(3)backend/ai_caller.py 增加 SdkAICaller:用 claude-agent-sdk 的 Python 客户端(claude_agent_sdk 模块,查询式调用;具体入口按包内文档:通常为 ClaudeSDKClient 或 query 函数,以 SDK 实际 API 为准——实现前先 pip show / 查包内 __init__ 导出名,不要凭记忆写导入)。结构与 SubprocessAICaller 完全对称:run(project_path, prompt) 生成器、事件归一化为同一 kind 枚举(say/read/write/command/result/error/done)、abort() 大力关会话(依赖 SDK 的 cancel/close 语义;若无,设置 threading.Event 标志并在迭代器侧提前 break + 尽力杀子进程)。SDK 权限回调(hooks/can_use_tool 形态,视 SDK 版本)接入 make_permission_decision:allow 直接放行、reject 直接拒绝、confirm 需转 SSE 弹窗——本任务先接 allow/reject 分支,confirm 分支挂一个向 broker publish 事件并阻塞等待(条件变量)的实现,超时按默认放行处理不会出现(permission 默认 deny 更安全:confirm 位默认按 reject 处理并打日志,Phase 1 的会话任务不会写 docs/ 外路径,完整弹窗闭环 Task 3/后续计划完成)。修改 make_ai_caller(config) 按 config.json 的 ai_caller 键在 SdkAICaller 与 SubprocessAICaller 之间选择。

(4)vendored 渲染库不动。写 backend/tests/test_ai_caller.py(pytest):三个纯函数级测试——make_permission_decision 的 DESIGN.md reject / docs allow / command confirm 三个代表断言(权限矩阵在 Task 1 已布遍 9 例,这里只保回归);make_ai_caller 在 ai_caller=config.json 为 "subprocess" 时返回 SubprocessAICaller 类型、为 "sdk" 时返回 SdkAICaller;SubprocessAICaller 的事件归一化:用一个喂人造 JSON 行的辅助函数(把行解析逻辑拆出来,便于纯测)断言 assistant 文本行归 kind=say、tool_use Read 行归 kind=read。归一化逻辑拆成独立函数 normalize_stream_line(line) -> dict 以便测试,不真实起 claude 进程。</action>
  <verify>
    <automated>bash -c 'cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_ai_caller.py -q 2>&1 | tail -3 && .venv/bin/python -c "
import sys; sys.path.insert(0, \".\")
from backend.cli_check import check_claude_cli
r = check_claude_cli()
print(\"cli-check-returned\", r[\"ok\"], r[\"installed\"])"'</automated>
  </verify>
  <fails_when>pytest 输出含 failed / error(退出码非零),或 cli_check 调用抛异常(无 cli-check-returned 输出行),本机 CLI 正常但 ok=False。</fails_when>
  <done>config.json 切 ai_caller=sdk / subprocess 时 make_ai_caller 返回不同实现类;SDK 路线与子进程路线事件枚举同构;CLI 自检未装/未登录两分支文案就位;pytest 全绿。已 commit。</done>
</task>

<task type="auto">
  <name>Task 3: 前端工作面板接入双轨直播与中止(端到端验证)</name>
  <files>frontend/index.html, frontend/app.js, frontend/style.css, backend/main.py</files>
  <action>扩展 Task 1 的前端探针为可切换双轨的真实界面:(1)index.html 增加路线选择下拉(「Claude Agent SDK / 子进程兜底」)与项目目录输入框;选择 POST 到一个新端点 POST /api/config(backend/main.py 挂载,写回 config.json 的 ai_caller 键并重建 caller 工厂——运行时换线不重进程)。(2)/api/dev/ping 语义升级为 dev/demo 调用:prompt 固定为「读取本目录下任意一个文件并向我说明它的内容」——在目标项目目录(用户输入的临时目录,建议测试时用 mktemp -d 预先造一个含 markdown 文件的目录)真实执行,事件流(SDK 与子进程两路线均验证)经 SSE 渲染进面板。(3)「中止」按钮绑定既存 /api/abort,并在前端把正在流式中的面板标记为「已中止」。三个文件按既有风格改,不重写。注意 app.js 中 EventSource 重连属浏览器默认行为,可保留。dev 探针端点在本任务保留——它是骨架的自证通道,Phase 2 正式会话上线后由后续计划拆除或保留为调试功能,不属本计划职责。</action>
  <verify>
    <automated>bash -c 'cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && (.venv/bin/uvicorn backend.main:app --port 8765 &) && sleep 2 && curl -sf http://localhost:8765/api/health && curl -sf -X POST http://localhost:8765/api/config -H "Content-Type: application/json" -d "{\"ai_caller\": \"subprocess\"}" && curl -sf http://localhost:8765/ | grep -c "index" && lsof -ti:8765 | xargs kill; echo "e2e-ok"'</automated>
  </verify>
  <fails_when>任意 curl -sf 失败(非零退出,页面拉取失败或 grep 计数为 0),或 uvicorn 起不来(无 e2e-ok 输出)。</fails_when>
  <done>服务器可起、/api/health 与 /api/config 均应答、静态页可达;配置切线在运行时生效。真实双轨端到端(浏览器中看到子进程路线与 SDK 路线各跑一次直播)留给人检步骤(见计划 verification):执行者已用 curl 证明链路。已 commit。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 浏览器 → FastAPI | 单机本地回环流量;请求体含项目路径自由文本 |
| FastAPI → claude CLI 子进程/SDK | 工具后端把用户 prompt 交给 AI 进程,产物落用户项目目录磁盘 |
| AI 进程 → 用户文件系统 | 权限门必须拦截的越权写(DESIGN.md / AUTHORIZATION.md / 项目外) |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi01-01 | Tampering | AI 直写受保护文件(DESIGN.md/AUTHORIZATION.md) | critical | mitigate | Task 1 make_permission_decision 矩阵 + Task 2 SDK 权限回调接入 reject 分支 + pytest 回归 |
| T-idi01-02 | Tampering | AI 写项目外路径 | high | mitigate | 权限矩阵 confirm/reject 分支;SDK 侧默认 deny |
| T-idi01-03 | Information Disclosure | SSE 流事件含文件内容被浏览器_history 保留 | low | accept | 单机单人本地,localhost 回环;无第三方网络面 |
| T-idi01-04 | Denial of Service | 子进程 hang 住不退出(kernel 级死循环) | medium | mitigate | abort() terminate→kill 两段;SSE 心跳;无操作超时本阶段不硬杀执行中调用(D-8 中止语义用户驱动) |
| T-idi01-SC | Tampering | pip install 依赖包(fastapi/uvicorn/claude-agent-sdk) | high | mitigate | 三包都是主流合法包,审计通过 PyPI 官方页;安装前逐包校验存在 + 他人项目标记较低(抽样核名后信任度可上げ);不装 [SUS] 包 |
</threat_model>

<verification>
1. 脚手架体检:python 依赖安装成功、backend 前端导入均通过(Task 1 automated)
2. 权限矩阵:9 断言单测过(Task 1 automated)+ pytest 回归(Task 2 automated)
3. 服务器链条:/api/health、/api/config、静态页(Task 3 automated curl)
4. 人检(端到端,一次性):bash run.sh → 浏览器 localhost:8765 → 各路线发起测试调用,亲眼看事件逐条渲染 → 点中止。执行者在 Task 3 的 <verify> 只是机器性回归;真实 AI 直播链路最后须由用户在 UAT 步骤确认一次
</verification>

<success_criteria>
- run.sh 启动即用,不依赖手工 pip/uvicorn 步骤
- AICaller 接口 + 两条实现都存在且 make_ai_caller 可切换,事件枚举完全一致
- 权限门矩阵纯函数全过单测(含 DESIGN.md/AUTHORIZATION.md reject)
- claude CLI 自检两分支文案 + 「只挡第一次」行为
- 工作面板直播 + 中止 + 折叠可用
</success_criteria>

<output>
Create `.planning/phases/idi-01-1-2/idi-01-01-SUMMARY.md` when done
</output>

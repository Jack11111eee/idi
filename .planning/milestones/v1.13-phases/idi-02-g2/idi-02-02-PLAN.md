---
phase: idi-02
plan: 02
type: execute
wave: 2
depends_on: ["idi-02-01"]
files_modified:
  - backend/ai_caller.py
  - backend/prompts.py
  - backend/session.py
  - backend/main.py
  - backend/tests/test_session.py
autonomous: true
requirements:
  - FLOW-04
  - UI-02
  - DATA-01

estimate:
  tokens: 95000
  raw_tokens: 95000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "SdkAICaller 与 SubprocessAICaller 都实现 ask_lite(document_text, quoted_text, question) -> dict(返回含 answer 键),同一签名同一契约(D-P2-8/D-01);FakeAICaller 同步打桩(lite_calls 记录 + lite_answers 返回)← UI-02 / D-P1-6 预定义签名本阶段兑现"
    - "ask_lite 调用形态:全新轻量无头调用,仅携带当前文档 + 划选原文(不读全量 docs/、不给工具能力、不走逐轮四步),prompt 注入 §3.8 红线 +「只解释,不改设计」(D-P2-8/D-P2-9)← UI-02 秒级响应前提"
    - "ask_lite 轻量调用不产 SSE 直播事件(事件不进工作面板,§4.3 面板是 AI 工作过程直播;大白话是用户查询,D-P2-8/D-P2-10)← UI-02"
    - "build_round_prompt(project_path, current_round) 组装四段结构 prompt:资料段读全量 docs/(当前轮文档全文 + 当前轮全部 annotations 逐条 id/quote/note,无批注时显式说明「当前轮暂无待处理批注」+ transcript/draft)+ 任务段注入 §3.3 四步 + §6.3 五件套 + §6.4 文法模板逐字(表头行/标记行正例 + 切勿改列名/标记行硬指令 + 目标文件名 docs/discuss-round-(N+1).md 明示)(D-P2-11/D-P2-18)← FLOW-04"
    - "session.process_round():入口校验 derive_state == phase3 且 current_round 非空(否则 False 转路由层 409)+ 单飞锁 + 后台线程 caller.run + 事件照常 SSE 直播(§5.2 从点击起全程可见)+ done 后三步回写:重拉 derive_state → 新轮前进时用 grammar.parse_annotation_responses 解析新轮文档 → annotations.writeback 回写上一轮 answer/status(D-P2-12/D-P2-14)← FLOW-04"
    - "半成品自愈:AI 写出末行非合规标记的新文档 → is_complete_round 判半成品 → current_round 仍为原轮 → process_round 可重跑,无新增判错分支(D-P2-13);回应表中未出现的批注保持 pending 下次重处理 ← FLOW-04 boundary:不合规产物 = 重跑覆盖(§7.3),不是报错路径"
    - "ask_lite 的 session 封装(如 answer_plain):同步调用(不起后台线程)、单飞锁语义(在飞中再发起被拒 409)、answer 由后端 append_item(type=plain, answer 即时写回, status=answered)落盘(D-P2-7/D-P2-10);plain 不计入未处理数(计数仅 type=comment 且 status=pending,D-P2-15)← UI-02 / §3.3「大白话在产生时已即时回答,不进入轮次循环」"
    - "五条新路由按既有风格:GET /api/rounds(轮次列表+当前轮号)、GET /api/rounds/{n}(文档+annotations 合并视图,非完整轮 404)、POST /api/rounds/{n}/annotations(非当前轮/非 phase3 → 409)、POST /api/rounds/{n}/plain(同步 ask_lite+落盘,返回 answer)、POST /api/rounds/process(202 受理/409 否则)(D-P2-22)← FLOW-04/UI-02 的 HTTP 面"
    - "_session_snapshot 扩轮次字段:rounds(list_complete_rounds 列表)+ 当前轮 pending 批注计数(D-P2-15),插在 current_check 之后,不重命名既有字段 ← DATA-01"
    - "AI 不直接改写 annotations:建条目仅 POST annotations 路由经 annotations.append_item;回写仅 process_round done 后的后端动作(prompt 明确禁止 AI 写 annotations 文件 + 后端回写不依赖 AI 遵守,D-P2-7)← DATA-01"
    - "全量 pytest 回归不下降(Wave 1 完成后的基线 + 本计划新增用例全绿)"
  artifacts:
    - path: "backend/prompts.py(扩展)"
      provides: "build_round_prompt(G2 处理本轮批注的服务端 prompt)与 build_plain_prompt(大白话轻量 prompt)"
      contains: "def build_round_prompt"
    - path: "backend/session.py(扩展)"
      provides: "process_round()(G2 全流水线)、answer_plain()(大白话同步封装)、round_process_available 纯磁盘入口判定、_session_snapshot 轮次字段"
      contains: "def process_round"
    - path: "backend/ai_caller.py(扩展)"
      provides: "SdkAICaller.ask_lite 与 SubprocessAICaller.ask_lite 真实现(替换 NotImplementedError 占位),双路线同契约"
      contains: "ask_lite"
    - path: "backend/main.py(扩展)"
      provides: "五条轮次路由(GET /api/rounds、GET /api/rounds/{n}、POST /api/rounds/{n}/annotations、POST /api/rounds/{n}/plain、POST /api/rounds/process)"
    - path: "backend/tests/test_session.py(扩展)"
      provides: "FakeAICaller.ask_lite 打桩 + process_round 回写/在飞拒绝/入口校验 + answer plain 落盘用例"
  key_links:
    - from: "backend/session.py process_round _worker finally 段"
      to: "backend/grammar.py parse_annotation_responses + backend/annotations.py writeback"
      via: "done 后重拉 derive_state,新轮出现 → 解析新轮文档回应表 → 回写上一轮 answer/status(D-P2-12)"
      pattern: "parse_annotation_responses"
    - from: "backend/main.py POST /api/rounds/process"
      to: "backend/session.py process_round"
      via: "202 受理/409 拒绝,照 /api/divergence 先例"
      pattern: "process_round"
    - from: "backend/session.py answer_plain"
      to: "backend/annotations.py append_item"
      via: "大白话即时答 type=plain 落盘(answer 即时写回,status=answered)"
      pattern: "append_item"
  prohibitions:
    - statement: "ask_lite 不得走逐轮四步、不得读全量 docs/、不得给工具能力(纯问答,无文件读写,D-P2-8)"
      status: unverified
      flagged: true
    - statement: "轻量调用事件不得进工作面板直播(它不代表用户主动任务,D-P2-8)"
      status: unverified
      flagged: true
    - statement: "AI 子进程不得直接改写 annotations 文件(建条目走后端 API、回写走 process_round done 后的后端动作;prompt 禁止 + 回写不依赖 AI 自觉,D-P2-7)"
      status: unverified
      flagged: true
    - statement: "process_round 不得在 AI 产物不合规时新增报错分支(半成品 → derive_state 仍回原轮 → 重跑覆盖,现有自愈语义零新增分支,D-P2-13)"
      status: unverified
      flagged: true
    - statement: "回写不得依赖 AI 自觉(只认回应表中的 id;未出现的 id 保持 pending,D-P2-13)"
      status: unverified
      flagged: true
    - statement: "plain 条目不得计入未处理数/未决清单(§3.3/D-P2-9/D-P2-15:计数只统计 type=comment 且 status=pending)"
      status: unverified
      flagged: true
    - statement: "不得新增路线开关/依赖(config.ai_caller 沿用,双路线 ask_lite 行为一致,D-P2-24;零新增第三方依赖)"
      status: unverified
      flagged: true
    - statement: "空批注轮的处理不得被拒绝(phase3 即可受理「处理本轮批注」,§3.3 新批注不存在不阻碍回应完毕,D-P2-15)"
      status: unverified
      flagged: true
---

## Phase Goal

**As a** 讨论收敛中的用户,**I want to** 点「处理本轮批注」后看到 AI 全程直播地批量回应我的全部批注并产出下一轮文档,划词要大白话时数秒内拿到即时回答,**so that** 轮次收敛主循环(G2)从后端到 AI 调用链完整打通,被回应的批注由后端机械回写而非依赖 AI 自觉。

<objective>
把 Wave 1 的纯模块接进 Phase 1 的调用链,交付 G2 全流水线与大白话轻量调用的后端全层:ai_caller.ask_lite 双路线真实现、prompts.build_round_prompt / build_plain_prompt、session.process_round() / answer_plain() / round_process_available、main.py 五条轮次路由、_session_snapshot 轮次字段、FakeAICaller 扩展与全部测试。这一层完成后,前端(Wave 3)只需消费固定的 HTTP 契约即可呈现完整轮次视图。

Purpose: FLOW-04 的服务端语义(G2 入口防绕过 + 单飞锁 + SSE 直播 + done 后回写)全部在本计划落地;DATA-01 的"后端解析回应表回写 answer/status,AI 不直接改写 annotations"由 process_round 的 finally 段动作兑现;UI-02 的秒级轻量调用由 ask_lite 双路线实现。
Output: 五条路由可 curl 造盘验证;FakeAICaller 级全流水线测试全绿;全量回归绿。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/phases/idi-02-g2/02-CONTEXT.md
@.planning/phases/idi-02-g2/idi-02-PATTERNS.md
@.planning/phases/idi-02-g2/idi-02-01-SUMMARY.md

依赖接口(来自 Wave 1,直接使用):
- backend/annotations.py:load / append_item(quote,before,type,note,answer=None)/ writeback(round, answers dict)/ select_pending / locate_quote / ANNOTATIONS_TEMPLATE
- backend/grammar.py:parse_annotation_responses(md_text) -> [{"id","quote","response"}](回应表提取,直接转 writeback 的 answers dict)
- 来自 Phase 1(已在 source):session.trigger_divergence(433-484 行,process_round 的模子)、busy/g1_available/divergence_available(纯磁盘入口判定先例)、main.py /api/divergence 的 202/409 分支、prompts.build_phase12_prompt 四段结构、ai_caller.ask_lite 签名占位(222-227 行 NotImplementedError)

DESIGN.md 权威依据:
- §3.3(未决清单四步:逐条回应上轮实质批注 → 更新文档已对齐 → 追问新细节 → 文末公开清单;大白话不进入轮次循环;空批注不阻碍申请授权)
- §3.4(D-05 双轨:轻量无头调用仅携带当前文档与划选原文,保证秒级;实质批注批量处理)
- §4.4 G2(无独立按钮;处理本轮批注 → AI 批量回应 + 产出 discuss-round-(N+1).md;批注转已回应 + 下一轮产生即自动冻结)
- §5.1(无状态:启动自磁盘读 docs/ 全部文档与批注)
- §5.2(事件直播:从用户点「处理本轮批注」起全程可见)
- §5.4(权限门:写 docs/ 内放行——AI 写 discuss-round-(N+1).md 零改动放行)
- §6.2(字段写回职责;plain 即时写回 answer、不入未决清单)
- §6.3(五件套与批注回应表,id 与上一轮 annotations 一一对应)
- §6.4(文法模板逐字遵守——build_round_prompt 把表头行逐字贴进 prompt)
- §7.3(半成品判据:重跑覆盖自愈;当前轮取最大完整轮)
- §9(setting_sources 屏蔽先例沿用到 ask_lite 两路线)

分支纪律(per 仓库 CLAUDE.md §5):本计划跨 5 个既有文件大改动——执行者从当前分支 HEAD 切出 phase-02/idi-02-02 工作分支,plan 完成后合回原分支(工作分支生命周期与 plan 对齐,不引入 worktree)。
</context>

<tasks>

<task type="auto">
  <name>Task 1: ask_lite 双路线实现 + build_plain_prompt(FakeAICaller 打桩)</name>
  <reversibility rating="costly">ask_lite 的三参签名(document_text, quoted_text, question)与返回 dict(answer 键)是 D-P1-6 预定义契约,前端与 session 层依赖此形状;变更即破坏两路线一致性硬要求。</reversibility>
  <files>backend/ai_caller.py, backend/prompts.py, backend/tests/test_session.py</files>
  <read_first>
  - backend/ai_caller.py(218-232 行:ask_lite 占位签名;set_request_permission 依赖注入;SubprocessAICaller run() 的 argv 形态与 normalize_stream_line 的 result 行解析 182-187 行;_VERDICT 或 argv 中 --setting-sources= 与 --append-system-prompt 的用法;SdkAICaller._build_options 与 asyncio.run 形态)
  - backend/prompts.py(21-44 行:_LANGUAGE_RULES 常量与模块级元组常量风格)
  - DESIGN.md §3.4(75 行:轻量调用形态定义)、§3.8(语言红线)、§9
  - .planning/phases/idi-02-g2/idi-02-PATTERNS.md(Modified Files #5:SubprocessAICaller/SdkAICaller 的 ask_lite 实现模式)
  - .planning/phases/idi-02-g2/02-CONTEXT.md(D-P2-8/D-P2-9/D-P2-10/D-P2-24)
  - backend/tests/test_session.py(29-60 行:FakeAICaller 现有形态,run_calls 记录模式)
  </read_first>
  <behavior>
    - 用例 1:build_plain_prompt(document_text, quoted_text, question) 产物含三要素(当前文档全文、划选原文、用户问题)+ §3.8 红线句 + 「只解释,不改设计」指令
    - 用例 2:FakeAICaller.ask_lite(document_text, quoted_text, question) 记录 lite_calls 三元组并返回 {"answer": ...}(lite_answers 可注入固定答)
    - 用例 3:SubprocessAICaller.ask_lite 不挂起——对(有 CLI 的本机)此用例仅做参数组装级单测(argv/prompt 构造纯函数断言),真 CLI 调用留给人检/IDI_E2E exclusive;SDK 路线同理由
    - 用例 4:ask_lite prompt 不含 docs/ 读取指令、不要求 AI 写任何文件(纯问答)
    </behavior>
  <action>(1)backend/prompts.py 新增 build_plain_prompt(document_text: str, quoted_text: str, question: str) -> str:三段结构(照 _LANGUAGE_RULES 复用同一常量,不复制红线字符串)——角色段(你是大白话解释器;_LANGUAGE_RULES + 「只解释,不改设计:大白话是消歧不是新决定」);资料段(当前文档全文 + 划选原文两块,显式标注「仅此两块资料,不读其他文件、不使用任何工具」);任务段(用大白话解释用户关于划选原文的问题)。此 prompt 走 system/append 段不含工具指令。

(2)backend/ai_caller.py:基类 ask_lite 方法由"占位 NotImplementedError"改为可实现契约(docstring 更新为 D-P2-8 语义:仅 document_text/quoted_text/question 三入参,不收 project_path;不产 SSE 事件;返回 {"answer": str};两路线同形)。

(3)SubprocessAICaller.ask_lite 实现:subprocess.run([cli, "-p", plain_prompt 来源(由使用 build_plain_prompt 组装——ai_caller 侧只接收 document_text/quoted_text/question 并 import backend.prompts.build_plain_prompt,或由调用方传入成品 prompt,执行者取更简:ai_caller import prompts 组装), "--setting-sources=", "--append-system-prompt", build_system_prompt()], capture_output=True, text=True, timeout=120) ——非流式单向,无 --input-format stream-json、无 --permission-prompt-tool(纯问答不起控制协议),保留 --setting-sources=(屏幕全局 allow 规则,与 run() 同因);解析 stdout:result 行(JSON)取 result 字段文本为 answer;无 result 行或 returncode != 0 时返回 {"answer": "", "error": 中文原因}(不抛——上层路由转 4xx/5xx 文案)。注意 "-p" 的 prompt 通过命令行参数传入;prompt 过长时的上限问题用 stdin 传递回退:优先 argv,遇 OSError(E2BIG)时改 subprocess.run(..., input=plain_prompt, ...) 的 stdin 形态(实现取其一并写进 docstring)。

(4)SdkAICaller.ask_lite 实现:照 _build_options 建 ClaudeAgentOptions 但禁工具(disallowed_tools 全禁或等效 options;纯问答无文件读写)、setting_sources=[];asyncio.run(...) 包同步收 ResultMessage 的 result 文本为 answer(照 run() 597-610 行 asyncio.run 形态裁剪);异常路径同 subprocess:返回 {"answer": "", "error": ...} 不抛。

(5)backend/tests/test_session.py 扩 FakeAICaller:__init__ 增 self.lite_calls: list[tuple[str,str,str]] = [] 与 self.lite_answers: dict[str,str] | None = None;新方法 ask_lite(self, document_text, quoted_text, question) -> dict:append 三元组到 lite_calls;lite_answers 非 None 时返回 {"answer": self.lite_answers.get(question, "测试即时答")},None 时返回 {"answer": "测试即时答") 固定形。不改 run/abort 既有形态(duck-type 兼容不变,D-P2-24)。另外为两条真实路线各补一个"参数构造级"单测:断言 prompt 组装(build_plain_prompt 断言三要素与红线句)与 FakeAICaller 打桩行为(behavior 用例 2/4)。真 CLI 的 ask_lite 全链验证在 Task 3 的 IDI_E2E 门控用例中(不在本任务)。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_session.py -q 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1'</automated>
    <fails_when>任一 pytest 输出含 failed/error;test_session 新增用例(plain prompt 三要素/打桩记录)任一缺失;grep -c "ask_lite" backend/tests/test_session.py 为 0(未打桩);全量回归 passed 数较 Wave 1 完成时下降。</fails_when>
  </verify>
  <acceptance_criteria>
  - backend/prompts.py 含 `def build_plain_prompt`(grep 命中)且函数引用 _LANGUAGE_RULES 常量(不复制红线字符串字面量,`grep -n "语言红线" backend/prompts.py` 仅命中既有定义行)
  - backend/ai_caller.py 的 `grep -n "def ask_lite"` 命中 ≥ 3 处(基类 + SdkAICaller + SubprocessAICaller),基类不再 raise NotImplementedError("ask_lite 将在 Phase 2 实现"原文消失)
  - SubprocessAICaller.ask_lite 的 argv 含 --setting-sources=(grep 可见)
  - test_session.py 的 FakeAICaller 含 lite_calls 记录(grep "lite_calls" 命中)且 ask_lite 用例 pass
  - 全量回归零失败
  </acceptance_criteria>
  <done>双路线 ask_lite 实现就位、契约一致(返回 dict 含 answer);build_plain_prompt 含红线与「只解释,不改设计」;FakeAICaller 打桩可记录调用;参数构造级用例全绿。</done>
</task>

<task type="tracer">
  <name>Task 2: process_round() 全流水线——build_round_prompt + done 后回应表回写( tracer 切穿 prompt→调用→解析→回写 四层)</name>
  <reversibility rating="costly">process_round 的回写动作(哪一轮、依据什么解析、写回哪些字段)是 DATA-01 的核心职责分离(AI 不改写 annotations),后续 Phase 3 G3 校验直接读这些字段;prompt 模板一旦被 AI 学到,改动会带来跨轮格式漂移。</reversibility>
  <files>backend/prompts.py, backend/session.py, backend/tests/test_session.py</files>
  <read_first>
  - backend/prompts.py(104-157 行 build_phase12_prompt 四段结构;47-102 行 build_divergence_prompt 的任务段常量风格)
  - backend/session.py(433-484 行 trigger_divergence 完整模子;420-431 行 divergence_available 入口判定;134-152 行 _session_snapshot;364-371 行 busy)
  - backend/state.py(derive_state 返回形状、STATE_PHASE3 常量、list_complete_rounds、is_complete_round)
  - backend/annotations.py(Wave 1:load/append_item/writeback/select_pending)
  - backend/grammar.py(Wave 1:parse_annotation_responses)
  - DESIGN.md §3.3(四步原文)、§4.4(G2 语义)、§6.3(五件套)、§6.4(文法模板)、§7.3(重跑覆盖)
  - .planning/phases/idi-02-g2/02-CONTEXT.md(D-P2-11/D-P2-12/D-P2-13/D-P2-14/D-P2-15)
  </read_first>
  <behavior>
    - 用例 1:round_process_available(project):derive_state 为 phase3 且 current_round 非空 → True;phase12_in_progress / phase1_new → False(纯磁盘判定,防绕过)
    - 用例 2:process_round 受理(FakeAICaller)→ build_round_prompt 收到当前轮号与磁盘现状(prompt 含当前轮文档全文、逐条批注 id/quote/note、「当前轮暂无待处理批注」的显式分支、全量 transcript/draft 资料、§3.3 四步、§6.4 表头模板、目标文件名 discuss-round-(N+1).md);事件照常 publish(done 收尾)
    - 用例 3:回写闭环——FakeAICaller 的 before_done 钩子里写盘合规 discuss-round-2.md(含批注回应表 a1-01)→ process_round 收流后:上轮 annotations a1-01 answered/answer 有值、a1-02 保持 pending、derive_state 前进到新轮
    - 用例 4:半成品——AI 写出的新文档末行非合规标记 → 收流后 current_round 仍原轮、上轮批注未被回写、process_round 可再次受理(重跑覆盖语义)
    - 用例 5:在飞拒绝—— HangingFake(gate/release event)挂住 in-flight → process_round 返回 False(单飞锁)
    - 用例 6:非 phase3 拒绝——phase12 目录直接调 process_round → False(入口校验)
    - 用例 7:空批注轮合法——当前轮零 annotations 时 process_round 照常受理(prompt 显式说明无批注,D-P2-15)
    </behavior>
  <action>(1)backend/prompts.py 新增 build_round_prompt(project_path, current_round: int) -> str(照 build_phase12_prompt 四段结构,放在两个既有 build 函数之后):角色段(轮次收敛引擎 + _LANGUAGE_RULES 复用);资料段 = 读全量 docs/(§5.1)——当前轮文档 discuss-round-{N}.md 全文(含半成品时的原文,重跑场景)、当前轮 annotations 逐条(id: quote: note: 行格式,is_complete 前提不判,直接 annotations.load;items 空时显式一句「当前轮暂无待处理批注」)、transcript.md/draft.md/brainstorm.md 按 _KNOWN_DOCS 既有循环注入;任务段 = 新建模块级常量 _ROUND_INSTRUCTIONS(照 _PHASE12_INSTRUCTIONS 元组风格),内容四个要点:①§3.3 四步原文逐条(逐条回应上轮全部实质批注(plain 已即时答不进入本轮)→ 更新文档本轮版次并标注已对齐 → 追问新的更深层细节问题进清单 → 文末公开当前未决清单);②§6.3 五件套点名(批注回应表/决策登记/维度表/未决清单/授权申请标记——每轮必须全部包含);③§6.4 文法模板**逐字**贴入:表头行正例 `| 批注id | 原文摘录 | 回应 |`、`| 维度 | 状态 | 说明 |(状态仅 ✓ ◐ ✗)`、`| 编号 | 问题 | 状态 |(状态仅 待决/已决)`、标记行正例 `> 申请授权:是` 与 `> 申请授权:否`,且给硬指令「切勿改列名、切勿改标记行格式——工具按此逐字解析,改动即解析失败」;④结果落盘指令:用 Write 工具产出 `docs/discuss-round-(N+1).md`(N+1 按 prompt 中当前轮号计算明示,如当前轮 1 → 写 discuss-round-2.md),不要写其他文件、不要写 annotations 文件(批注记录由本工具后端管理)。落盘段尾注明「写完后在回复里简述本轮改动」。

(2)backend/session.py:(a)新增 round_process_available(project_path) -> bool 纯磁盘判定(照 divergence_available 形态,当前导入区已有 derive_state):derive_state(project)["state"] == STATE_PHASE3 且 ["current_round"] 非 None → True,否则 False;(b)新增 process_round() -> bool(照 trigger_divergence 模子逐段对照写):入口三查(未进项目 RuntimeError/在飞 False/round_process_available False)→ _inflight Event 置起 → build_round_prompt(project, current_round)(current_round 从 derive_state 取)→ _worker 后台线程:事件循环照 trigger_divergence(权限回调接入 _wire_permission_callback、事件 _publish_for_tests、done 跳出),_ai_texts 在此不落盘(G2 无 say 落盘需求,与 divergence 同);**finally 段新增 done 后回写动作**(try 包裹,回写异常发 error 事件不悬空进度):重拉 derive_state(project) → 若 current_round 前进(prev_round < new_round):读新轮文档文本(路径用 ROUND 文件名模板)→ grammar.parse_annotation_responses(文本) → 组 answers dict {id: response} → annotations.writeback(project, prev_round, answers)(标准 mold 的 finally 段 done 收尾事件仍是本流水线唯一一条 kind=done——此处的回写动作不发第二条 done,仅查 writeback 结果,如需向用户报告回写情况可发非 done 的信息性事件);若 current_round 未前进(AI 写废/中止):不回写、不报错(半成品自愈,D-P2-13;derive_state 已把判据做掉)。prev_round 在 _worker 外闭包捕获(build 前的值)。

(3)backend/tests/test_session.py 扩 7 用例(behavior 列表;FakeAICaller 模式照 426-488 行 BrainstormWritingFake → 新 RoundWritingFake 同构:before_done 钩子里写盘合规 discuss-round-2.md 五件套样本;HangingFake 挂起模式照 552-579 行):

- test_round_process_available(用例 1:三态目录直造)
- test_process_round_prompt_contains(用例 2:断言 run_calls[0][1] prompt 含当前轮文档全文片段、a1-01 批注行、四步关键词、三表头行原文、目标文件名 discuss-round-2.md)
- test_process_round_writeback(用例 3:闭环断言)
- test_process_round_incomplete_new_round(用例 4:写的文档末行坏 → current_round 不变、annotations 未动、可重跑)
- test_process_round_busy_rejects(用例 5)
- test_process_round_non_phase3_rejects(用例 6)
- test_process_round_empty_annotations_ok(用例 7:零批注照常受理 + prompt 含「当前轮暂无待处理批注」)

先红后绿。写完后自查:prompt 模板里的 §6.4 表头字符串与 grammar.py 解析的 keyword 字面一致(「覆盖维度表」「未决问题清单」「批注回应」三关键词必须同时出现在模板正例中——两端同为 §6.4 字面);process_round 不落 transcript;round_process_available 不读内存态。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_session.py -q 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1'</automated>
    <fails_when>任一 pytest 输出含 failed/error;test_session 用例数 < 既有数 + 7(七个新用例名 grep -c "test_process_round\|test_round_process" 应 ≥ 7);用例 3/4(回写闭环与半成品自愈)失败;全量回归 passed 下降。</fails_when>
  </verify>
  <acceptance_criteria>
  - backend/prompts.py 含 `def build_round_prompt`(grep),且源码含三表头字面量 "| 批注id | 原文摘录 | 回应 |"、"| 维度 | 状态 | 说明 |"、"| 编号 | 问题 | 状态 |" 与 "> 申请授权:是" 正例(grep 全命中)
  - backend/session.py 含 `def process_round` 与 `def round_process_available`(grep 命中)且 finally 段含 parse_annotation_responses 与 writeback 调用链
  - test_session.py 新增 ≥ 7 个 test_process_round*/test_round_process* 用例全绿,其中回写闭环用例断言 a1-01 answered、a1-02 pending、current_round 前进
  - 半成品用例断言 current_round 不变 + 可重跑受理
  - 全量回归零失败(在 Wave 1 基线上叠加)
  </acceptance_criteria>
  <done>G2 全流水线(prompt 组装 → 后台调用直播 → 新轮产出 → 后端解析回应表回写)在 Fake 级全绿;半成品重跑、在飞拒绝、入口防绕过、空批注轮四边界各有专属用例;SSE 直播沿用既有通道零第二条路径。</done>
</task>

<task type="auto">
  <name>Task 3: answer_plain 同步封装 + 五条轮次路由 + _session_snapshot 轮次字段</name>
  <reversibility rating="costly">五条路由的路径与载荷形状是 Wave 3 前端的固定契约(D-P2-22);409 语义(非当前轮/非 phase3/busy)是防绕过的服务端强约束,定形后前端与测试都依赖。</reversibility>
  <files>backend/session.py, backend/main.py, backend/tests/test_session.py</files>
  <read_first>
  - backend/session.py(Task 2 的 process_round/round_process_available;134-158 行 _session_snapshot 既有字段;busy)
  - backend/main.py(56-75 行 pydantic 请求体先例;151-169 行 202/409 分支先例;182-203 行 g1 错误分支先例;125-132 行 get_draft 形态)
  - backend/annotations.py(Wave 1:append_item/load/select_pending)
  - backend/state.py(list_complete_rounds/derive_state)
  - DESIGN.md §6.1(文件名形态)、§6.2(建条目字段)
  - .planning/phases/idi-02-g2/02-CONTEXT.md(D-P2-10/D-P2-15/D-P2-21/D-P2-22)
  - backend/tests/test_route_session.py(route_env fixture 形态 23-29 行)
  </read_first>
  <behavior>
    - 用例 1:answer_plain(round_n, quote, before, question):同步调 caller.ask_lite → append_item(type=plain, answer=回答文本)→ 返回条目;FakeAICaller 的 lite_calls 记录了三元组;落盘条目 status=answered、type=plain;在飞主调用进行中再发起 → 拒绝(409 语义)
    - 用例 2:POST /api/rounds/{n}/annotations(phase3 当前轮):建条目落盘(status=pending、type=comment)→ 返回条目;对非当前轮轮号 → 409;对非 phase3 项目 → 409(409 仅此两条件,与 D-P2-22 的 409 契约逐字一致)
    - 用例 3:GET /api/rounds:返回 {"rounds": [1,2], "current_round": 2} 形态(整列表来自 list_complete_rounds)
    - 用例 4:GET /api/rounds/2:完整轮 → 返回文档文本 + annotations 对象;非完整轮号 5 → 404
    - 用例 5:POST /api/rounds/process:phase3 → 202 {"status":"accepted"};非 phase3 → 409;在飞 → 409
    - 用例 6:GET /api/session 快照:新增 rounds(列表)与 pending_annotations(当前轮 comment+pending 计数)字段;plain 条目不计入 pending_annotations
    - 用例 7:route_env 场景:phase3 目录 + 手造 annotations(pending 一条 + plain 一条)→ snapshot 计数为 1(plain 不计)——D-P2-15
    </behavior>
  <action>(1)backend/session.py:(a)新增 answer_plain(round_n: int, quote: str, before: str, question: str) -> dict:单飞检查(busy() → raise RuntimeError("当前有调用进行中"——路由层转 409,与既有在飞文案风格一致)→ 取当前项目(未进入 RuntimeError)→ 校验 derive_state == phase3 且 round_n == current_round(否则 RuntimeError("仅当前轮可批注")供路由层 409)→ 读当前轮文档文本(不存在 FileNotFoundError)→ caller.ask_lite(document_text=文档全文, quoted_text=quote, question=question) → annotations.append_item(project, round_n, quote=quote, before=before, type="plain", note=question, answer=结果["answer"]) → 返回新条目 dict。**同步执行**(不起后台线程,D-P2-10:秒级响应,无并发压力);**不产 SSE 事件**(D-P2-8)。(b)_session_snapshot 在 current_check 之后插入两字段:"rounds": list_complete_rounds(project / "docs")(session 顶部已 import list_complete_rounds)、"pending_annotations": 当前轮 annotations.load 后 select_pending 的长度(仅 phase3/current_round 有值,否则 0)。既有字段不动、不重命名。(c)建条目辅助 add_annotation(round_n, quote, before, note):同 answer_plain 前两步校验(未进项目 RuntimeError/非当前轮或非 phase3 RuntimeError 供路由层 409)→ append_item(type="comment", note=note, status=pending)→ 返回条目。**不加 busy 检查**:annotations 的写入目标是当前轮文件,与 AI 回写的上一轮文件不同对象,无竞态;与 D-P2-22 的 409 契约一致(409 仅 非当前轮/非 phase3 两条件)。

(2)backend/main.py:pydantic 模型 AnnotationBody(quote: str / before: str / note: str)与 PlainBody(quote: str / before: str / question: str)加在 PermissionBody 之后;五条路由加在 get_transcript(206-213 行)之后、config 分节之前,保持既有分节注释:

- GET /api/rounds:session.snapshot() 的 rounds/current_round 转发;RuntimeError → 400(既有风格)
- GET /api/rounds/{n}:n 非 list_complete_rounds 内 → 404 {"status":"error","message":"该轮不存在或不完整"};存在 → {"status":"ok","round": n, "document": 文档文本, "annotations": annotations.load(project, n)}(读当前项目路径,session 暴露 current_project 只读访问器或复用 snapshot 内字段——执行者照 session 既有对外函数就近取,不加新全局)
- POST /api/rounds/{n}/annotations:调 session.add_annotation;RuntimeError 文案含「轮」或「阶段"」 → 409;ValueError(quote 空等) → 400;成功 200 {"status":"ok","annotation": 条目}
- POST /api/rounds/{n}/plain:调 session.answer_plain;RuntimeError 含「在飞」 → 409;含「轮」/「阶段」→ 409;AI 调用失败(answer 空 error 键)→ 502 {"status":"error","message":原因};成功 200 {"status":"ok","annotation": 条目}(answer 在条目的 answer 字段,前端可直读)
- POST /api/rounds/process:调 session.process_round,返回 True → 202 {"status":"accepted"},False/在飞 → 409(照 /api/divergence 151-169 行逐字风格)

(3)backend/tests/test_session.py 扩 4 用例(answer_plain 用例 1、route 级用例走 test_route_session.py 的 route_env 形态补用例 2-7 中 route 侧四条——执行者可拆两文件,合计新增 ≥ 7);过 phase3 目录直造 helper:docs/discuss-round-1.md 带合规末行 + 一条 pending annotations。

写完后自查:批注路由的非当前轮 409 在服务端强制(前端只是显示约束,D-P2-21);answer_plain 不 publish 任何事件;five 路由的错误 status code 与 CONTEXT D-P2-22 表逐条一致。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_session.py backend/tests/test_route_session.py -q 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1 && (.venv/bin/uvicorn backend.main:app --port 8766 &) && n=0 && until curl -sf http://127.0.0.1:8766/api/health >/dev/null 2>&1; do n=$((n+1)); if [ $n -gt 120 ]; then lsof -ti:8766 | xargs kill 2>/dev/null; exit 1; fi; sleep 0.5; done && D=$(mktemp -d) && mkdir -p $D/docs && printf "# 第 1 轮\n\n内容\n\n> 申请授权:否\n" > $D/docs/discuss-round-1.md && curl -sf -X POST http://127.0.0.1:8766/api/enter -H "Content-Type: application/json" -d "{\"path\": \"$D\"}" >/dev/null && curl -sf http://127.0.0.1:8766/api/rounds | grep -q current_round && curl -sf http://127.0.0.1:8766/api/rounds/1 | grep -q annotations && curl -sf -X POST http://127.0.0.1:8766/api/rounds/1/annotations -H "Content-Type: application/json" -d "{\"quote\": \"内容\", \"before\": \"第 1 轮\", \"note\": \"这里没看懂\"}" | grep -q pending && curl -s -o /dev/null -w "%{http_code}" -X POST http://127.0.0.1:8766/api/rounds/2/annotations -H "Content-Type: application/json" -d "{\"quote\": \"x\", \"before\": \"\", \"note\": \"y\"}" | grep -q 409; rc=$?; lsof -ti:8766 | xargs kill 2>/dev/null; [ $rc -eq 0 ] && echo "rounds-api-ok"'</automated>
    <fails_when>任一 pytest 输出含 failed/error;cuvicorn 起不来(等待循环 60s 上限后退出非零);任一 curl -sf 失败(轮次列表/单轮/建批注任一 4xx/5xx);非当前轮 2 的建批注未返回 409(grep -q 409 失败);无 rounds-api-ok(rc 捕获在 kill 之前,失败路径同样先杀 uvicorn)。</fails_when>
  </verify>
  <acceptance_criteria>
  - backend/main.py 含 grep -c "api/rounds" ≥ 5(五条路由:GET rounds、GET rounds/{n}、POST annotations、POST plain、POST process)
  - backend/session.py 含 `def answer_plain` 与 `def add_annotation`(grep),answer_plain 体内无 broker.publish / threading.Thread(同步 + 不直播)
  - GET /api/session 响应含 "rounds" 与 "pending_annotations" 键(uvicorn 冒烟紧跟)
  - 非当前轮 POST annotations 返回 409(curl 冒烟已证);plain 条目不计入 pending_annotations(用例 7 断言)
  - test_session.py + test_route_session.py 新增 ≥ 7 用例全绿;全量回归零失败
  </acceptance_criteria>
  <done>五条路由 + answer_plain 同步封装 + snapshot 轮次字段全部可用并经 curl 冒烟;409 边界(非当前轮/非 phase3/在飞)服务端强制;plain 落盘即时 answered 且不进未处理数;Wave 3 前端可完全按本契约开发。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 浏览器 → 五条新路由 | quote/before/note/question 均用户自由文本;round 参数可被伪造打到非当前轮 |
| AI 产出新轮文档 → 后端回写 | AI 文档不可信(可能不含回应表/末行坏),回写必须配对失败安全 |
| ask_lite 输入 → CLI 子进程/SDK | prompt 拼进 argv/stdin,document_text 可能极长(E2BIG 边界) |
| annotations 建条目路径 | 唯一合法后端入口;AI 子进程被禁止写(权限上 docs/ 放行但 prompt 禁止 + 后端不依赖遵守) |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi02-06 | Tampering | 伪造 round 参数 POST /api/rounds/9/annotations 把批注挂到冻结轮 | high | mitigate | 服务端强制:answer_plain/add_annotation 校验 round_n == derive_state 的 current_round,否则 409(D-P2-21);冒烟用例已含 409 断言 |
| T-idi02-07 | Tampering | AI 篡改 annotations 回应表ного格式误导回写(多余 id 重复 id) | medium | mitigate | writeback 只认现有 items 的 id(Answers 中未知 id 忽略——Wave 1 已测);duplicate id 在 parse\AnnotationResponses 提取层保持原文序、writeback 以最后出现为准或首现(实现文档化),单测覆盖 |
| T-idi02-08 | Denial of Service | ask_lite prompt 拼进 argv 超 OS 参数上限(E2BIG)崩路由 | medium | mitigate | Task 1 action 已列:优先 argv,遇 OSError 回退 stdin 传递(prompt 文档全文可能很大);timeout=120 上限 |
| T-idi02-09 | Information Disclosure | 划选原文(quote)经 prompt 外发给 CLI 进程 | low | accept | 单机本地、CLI 即用户登录态;与 send_message 同一信任面(Phase 1 已接受) |
| T-idi02-10 | Tampering | X 经 /api/rounds/process 绕过单飞锁并发双跑引起新轮互写 | high | mitigate | process_round 入口 _inflight 单飞检查(继承 session 锁语义,trigger_divergence 同形);在飞 409 用例 5 已覆盖 |
| T-idi02-11 | Repudiation | 轻量调用无事件直播,用户无法回顾 ask_lite 历史 | low | accept | 落盘为 plain 条目(answer 在 annotations.json 常驻可查,D-P2-9)——面即为审计面,非缺失 |

执行说明:本计划零新 pip 依赖(ask_lite 用既有 SDK/CLI),无供应链项。
</threat_model>

<verification>
1. Task 1 automated:pytest test_session.py(ask_lite 打桩 + plain prompt 用例)+ 全量回归
2. Task 2 automated:pytest test_session.py(process_round 7 用例,含回写闭环/半成品/在飞/入口/空批注)+ 全量回归
3. Task 3 automated:pytest 两测试文件 + 全量回归 + uvicorn 冒烟(五路由 + 非当前轮 409)
4. 真 CLI 的 ask_lite 与 process_round 全链(真实数秒即时答、真实新轮产出)在 idi-02-04 的 IDI_E2E 门控用例验证,不在本计划
5. 人检项:无(本计划是后端层;浏览器人检在 Wave 3 计划,真实 AI 人检在 idi-02-04)
</verification>

<success_criteria>
- ask_lite 双路线同契约可用(返回 dict 含 answer),FakeAICaller 可观测(lite_calls)
- process_round 全流水线经 7 用例证明:prompt 含全部模板要素、done 后回写命中、未命中保持 pending、半成品可重跑处理
- 五条路由 curl 可用,409/404/400 边界与 D-P2-22 表逐条一致
- plain 不计入未处理数经用例证明
- 全量回归在 Wave 1 基线上只增不减
</success_criteria>

## Artifacts this phase produces(本计划新增符号清单)

- backend/prompts.py:build_plain_prompt(document_text, quoted_text, question) -> str、build_round_prompt(project_path, current_round) -> str、_ROUND_INSTRUCTIONS 模块常量
- backend/session.py:process_round() -> bool、round_process_available(project_path) -> bool、answer_plain(round_n, quote, before, question) -> dict、add_annotation(round_n, quote, before, note) -> dict、_session_snapshot 新增字段 rounds / pending_annotations
- backend/ai_caller.py:AICaller.ask_lite 实现化、SdkAICaller.ask_lite、SubprocessAICaller.ask_lite
- backend/main.py:AnnotationBody、PlainBody、GET /api/rounds、GET /api/rounds/{n}、POST /api/rounds/{n}/annotations、POST /api/rounds/{n}/plain、POST /api/rounds/process
- backend/tests/test_session.py:FakeAICaller.ask_lite/lite_calls/lite_answers 扩展、RoundWritingFake、test_round_process_available、test_process_round_prompt_contains、test_process_round_writeback、test_process_round_incomplete_new_round、test_process_round_busy_rejects、test_process_round_non_phase3_rejects、test_process_round_empty_annotations_ok、answer_plain/route 系用例

<output>
Create `.planning/phases/idi-02-g2/idi-02-02-SUMMARY.md` when done
</output>

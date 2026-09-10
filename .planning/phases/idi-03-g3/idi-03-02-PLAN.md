---
phase: idi-03
plan: 02
type: execute
wave: 2
depends_on: ["idi-03-01"]
files_modified:
  - backend/prompts.py
  - backend/session.py
  - backend/main.py
  - backend/tests/test_session.py
autonomous: true
requirements:
  - FLOW-05
  - DATA-02
  - DATA-04

estimate:
  tokens: 100000
  raw_tokens: 100000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "session.authorize():入口 = derive_state == phase3 + g3_available(project) 后端四查再查(任一不过 → False 转 409;按钮亮否只是前端呈现,服务端独立重判防绕过)→ g3.authorize_write 落 AUTHORIZATION.md → 返回写入后 derive_state(state=phase4);已授权(Phase4+ 或 FileExistsError)→ False/异常转 409 幂等 ← FLOW-05 / D-P3-4 / ROADMAP 判据 1"
    - "session.set_tier(tier):入口 = derive_state == phase5_awaiting_tier(有 DESIGN.md、无 check 报告)→ checks.write_tier 落盘签名文件;非 phase5_awaiting_tier → RuntimeError 转 409;已是同值 → 覆盖写入幂等合法 ← DATA-04 / D-P3-11 / ROADMAP 判据 3"
    - "session.start_writing():照 process_round 模子三查(未进项目 RuntimeError / 在飞 False / writing_available = derive_state == phase4)→ 后台线程 caller.run(build_writing_prompt) + SSE 直播;done 后 else 分支后端动作:derive_state 重拉 → tmp 存在且无 DESIGN.md → (tmp_path).replace(DESIGN.md) 原子改名(改名前不校验 tmp 内容完整性)→ 撰写完成;tmp 不存在(AI 没写)→ error 事件「撰写未产出 tmp,可重跑」、状态留 phase4 可重跑 ← DATA-02 / D-P3-6 / D-P3-8 / ROADMAP 判据 2"
    - "build_writing_prompt(project) 四段结构(照 build_round_prompt 同族):角色(总设计文档撰写引擎)+_LANGUAGE_RULES → 资料段全量 docs/(全部完整轮文档 + 全部 annotations 逐条 + transcript/draft/brainstorm)——**绝不读 DESIGN.md.tmp 与 AUTHORIZATION.md(半份 tmp 是被覆盖物,D-P3-9)**→ 任务段(覆盖维度表七维度全部内容、吸收决策登记与已对齐结论、不含未决问题)+ 落盘指令(用 Write 工具写 DESIGN.md.tmp 项目根整体覆盖式写入后即结束,绝不直接写 DESIGN.md 或 AUTHORIZATION.md——权限门会拒绝,提示语写明目的与格式) ← FLOW-05 / DATA-02 / D-P3-7"
    - "session.start_check():三查(check_available = phase5_awaiting_tier 或 phase5_checking 且无在飞)→ 后台线程 caller.run(build_check_prompt(project, check_n, tier)) + SSE 直播;check_n = max_check_number + 1(接入点后算好注入 prompt 防编号错);done 后 else = 循环驱动判定:①最新报告末行 PASS → 自然结束(mission_complete 由 derive_state 推导,Wave 4 呈现);②报告含 P0/P1(非纯 P2、非 PASS)→ 自动链入 start_repair(**done-回调直排,无 scheduler**);③纯 P2 报告 → 不修复,结束(残余裁决 UI 态由 Wave 4 呈现,D-P3-17);④修复者抛问扫描未命中不影响本函数 ← DATA-04 / D-P3-13 / D-P3-16"
    - "session.start_repair():三查(repair 入口 = phase5_checking + 最新报告存在)→ caller.run(build_repair_prompt) + SSE;done 后 else:全文本扫描 `> 待裁决:` 前缀(say 事件流 + 最终文本,先流后文本)→ 命中 → checks.append_pending_question 截存到当轮报告 + error/暂停语义的事件(不启动下一跳);无命中且 tmp 已写 → tmp 改名 DESIGN.md → 宽松档:改完即结束(修复者已在报告追加 PASS 或由收口动作处理);严格档:自动链入 start_check(check_n+1,同轮驱动器)← DATA-04 / D-P3-14 / D-P3-16 / D-P3-18 / ROADMAP 判据 4"
    - "session.verdict_append(number, decision, note):入口 = phase5_checking + 最新报告存在 → checks.append_user_verdict 落盘 `> 裁决:#K:`(同号 FileExistsError 转路由 409);**纯 P2 残余裁决全部处理完时**同一调用内判定:报告问题表逐条比对已配对裁决 → 全部配对 → checks.append_pass_conclusion 立即收口(D-P3-17 「全部处理完即视为收敛收口」的后端动作);宽松档同通道复用(math 同一函数)← DATA-04 / D-P3-17 / D-P3-19"
    - "build_check_prompt(project, check_n, tier) 与 build_repair_prompt(project, check_n) 四段结构:check 资料段 = DESIGN.md 全文 + 全部轮次文档 + 全部 annotations + 已有全部 DESIGN-check 报告(严格档趋势照读);角色段「干净的眼睛」+ **绝不修改 DESIGN.md(只写自家报告)明禁**;问题分级表头 `| 编号 | 级别 | 位置 | 问题 | 建议修法 |` 逐字贴入 + TIER_LINE 头部行逐字 + 末行结论行文法(;repair 资料段 = DESIGN.md + 最新报告全文(含裁决行)+ 其他报告 + 轮次文档/批注;任务段 = 报告问题按裁决逐条修复、用 Write 写 DESIGN.md.tmp 整体落盘、用户职权问题发 `> 待裁决:#K:<问题>` 停下、宽松档在报告末追加 PASS ← D-P3-13 / D-P3-14 / D-P3-15 / D-P3-29"
    - "_session_snapshot 扩两字段(既有字段不动不重命名):g3_available(bool,phase3 态四查)、selfcheck({tier, mode}——mode ∈ running/paused/resumed/done,由 derive_state + latest_check_content + unpaired_verdicts/配对 判定组装;不新增 derive_state 状态值,不缓存)← D-P3-23 / D-P3-26"
    - "四条新路由:POST /api/authorize(g3:成功 200 返回新 derive_state / 四查不过或已授权 → 409 / 未进项目 → 400)、POST /api/checks/tier(白名单外 → 400 / 非 phase5_awaiting_tier → 409)、POST /api/writing(202 受理 / busy 或非 phase4 → 409)、POST /api/checks/start(202 / 409)、POST /api/checks/repair(202 / 409)、POST /api/checks/verdict(200 追加 / 同号 FileExistsError → 409 / 400)← D-P3-27"
    - "AI 无任何直写 AUTHORIZATION.md 或 DESIGN.md 的路径:权限矩阵规则 1/2 零改动消费(test_ai_caller 补 AUTHORIZATION.md reject 断言);后半程所有 DESIGN.md 落盘均走 tmp → 后端 rename ← FLOW-05 / §5.4 / ROADMAP 判据 2"
    - "全量 pytest 回归基线 143 + 新增全绿(见 verify)"
  artifacts:
    - path: "backend/session.py(扩展)"
      provides: "authorize() / set_tier() / start_writing() / start_check() / start_repair() / verdict_append() / writing_available / check_available / repair_available + _session_snapshot 新增 g3_available / selfcheck 字段"
      contains: "def start_check"
    - path: "backend/prompts.py(扩展)"
      provides: "build_writing_prompt / build_check_prompt / build_repair_prompt 三族四段 prompt + _CHECK_GRAMMAR_EXAMPLES 报告文法模板(_ROUND_INSTRUCTIONS 同族常量)"
      contains: "def build_check_prompt"
    - path: "backend/main.py(扩展)"
      provides: "POST /api/authorize、POST /api/checks/tier、POST /api/writing、POST /api/checks/start、POST /api/checks/repair、POST /api/checks/verdict、GET /api/design、GET /api/checks 八路由 + AuthorizeBody/TierBody/VerdictBody"
    - path: "backend/tests/test_session.py(扩展)"
      provides: "WritingFake / CheckWritingFake / RepairWritingFake / 待裁决 ThrowingFake + start_writing 改名与 error 分支 + start_check 循环驱动四分支 + verdict_append 截存与收口 + 入口判定与单飞用例"
  key_links:
    - from: "backend/session.py start_writing 的 done-else 分支"
      to: "项目根 DESIGN.md"
      via: "(project/DESIGN.md.tmp).replace(project/DESIGN.md) 原子改名(同 inode,半份 DESIGN.md 不可能存在,§7.4 行 4)"
      pattern: "Path.replace"
    - from: "backend/session.py start_check 的 done-else 分支(循环驱动器)"
      to: "backend/session.py start_repair → start_check(next_n)"
      via: "外层 driver 串调/else 尾部直排——每跳结束重拉 derive_state 判下一步,无常驻 scheduler(D-P3-16);finally 解锁后由外层 wrapper 串调(避免 else 内自调被单飞锁拒)"
      pattern: "done-回调直排"
    - from: "backend/session.py verdict_append"
      to: "backend/checks.py append_user_verdict + append_pass_conclusion"
      via: "裁决落盘同报告;纯 P2 残余全配对 → 后端立即追加 PASS 收口(D-P3-17)"
      pattern: "append_user_verdict"
    - from: "backend/prompts.py _CHECK_GRAMMAR_EXAMPLES"
      to: "backend/grammar.py parse_tier_line / parse_problem_grades 的字面"
      via: "| 编号 | 级别 | 位置 | 问题 | 建议修法 | 表头与 > 自检档位: 头部行在 prompt 与解析器两端一字不差(TIER_LINE 常量引用,D-P3-29)"
      pattern: "逐字注入"
  prohibitions:
    - statement: "AI 写 DESIGN.md 必须只走 tmp(权限门已有);后端原子改名是唯一合法落盘——不得新增任何 AI 直写 DESIGN.md 的路径,也不得改名前校验/修补 tmp 内容(D-P3-8:AI 产物不修补,靠重跑覆盖)"
      status: unverified
      flagged: true
    - statement: "严格档循环驱动不得引入常驻后台 scheduler/定时器(推荐 done-回调直排;每步结束拉磁盘判定下一步)"
      status: unverified
      flagged: true
    - statement: "「继续自检」「继续修复」重跑不得重算确认词(AUTHORIZATION.md 已存在即凭证,§7.3 原文);也不得跳号(check_n 重跑同轮覆盖或 max+1,不重排已落盘报告编号)"
      status: unverified
      flagged: true
    - statement: "状态不新增 derive_state 七常量之外的状态值(selfcheck 子状态经 session snapshot 组装,D-P3-23);snapshot 函数内不得调 AI、不做超出 derive 派生的厚重 IO"
      status: unverified
      flagged: true
    - statement: "「> 待裁决:」扫描:自动推进仅在调用正常结束且全程无该标记时触发;识别不到该标记不得当作正常完成(识别失败 → 循环停在当前跳,不误推进,D-P3-18 兜底语义)"
      status: unverified
      flagged: true
    - statement: "拒绝 = 一条普通批注走既有 annotations 通道(session 层转调 add_annotation 即 D-P3-5 拒绝路径),不得发明独立拒绝文件"
      status: unverified
      flagged: true
    - statement: "不得新增专用收尾 SSE 事件种类(kind 面向 SSE 照旧,done 后前端拉 /api/session);不得改 Phase 1/2 已定版式与既有路由契约"
      status: unverified
      flagged: true
    - statement: "不新增第三方依赖;不引入新测试基建(测试族扩展照既有 FakeAICaller/fresh_session/wait_idle 模式,D-P3-30)"
      status: unverified
      flagged: true
---

## Phase Goal

**As a** 已完成收敛的用户,**I want to** 点亮并确认 G3 授权后,AI 在我授权的范围内写出总设计文档、由后端原子落盘,选择宽松或严格档后看到工具自动跑核查与修复循环直至 PASS——而我的每一条裁决都成为磁盘上的正式签名,**so that** 三道门后半程(阶段 4/5)从后端到 AI 调用链完整打通,授权永不越权、循环无需我 babysit、崩溃中断重开即自愈。

<objective>
Wave 1 纯函数接进 Phase 1/2 的调用链,交付阶段 4/5 的后端全层。

Purpose: FLOW-05 的授权语义(G3 服务端防绕过 + AUTHORIZATION.md 唯一凭证)、DATA-02 的撰写侧(tmp 原子落盘 + 继续撰写自愈)、DATA-04 的流程侧(档位落盘、两角色自动循环、抛问截存暂停、裁决续跑、纯 P2 残余裁决收口)全部在本计划落地;Wave 4 视图按固定 HTTP 契约消费即得完整阶段 4/5/归档界面。
Output: session 六函数 + prompt 三族 + 八路由(Fake 级测试全绿);DERIVATION 链:四查通过 → AUTHORIZATION.md → tmp → DESIGN.md → check-N → PASS → mission_complete。
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
@.planning/phases/idi-03-g3/idi-03-01-SUMMARY.md

依赖接口(来自 Wave 1,直接使用):
- backend/g3.py:g3_available(project) / authorize_write(project) / AUTHORIZATION_FILENAME
- backend/checks.py:write_tier / read_tier / append_pending_question / append_user_verdict / append_pass_conclusion / TIER_FILENAME
- backend/grammar.py(增量):parse_tier_line / parse_problem_grades / is_pure_p2 / scan_pending_questions / TIER_LINE_STRICT / TIER_LINE_LOOSE;既有锁定六条(is_pass_conclusion / parse_verdict_lines / unpaired_verdicts)
- 来自 Phase 1/2(已在 source):process_round 模子(session.py 528-629:入口三查 + _worker + SSE + done-else + finally 解锁)、round_process_available 纯磁盘入口判定模式(517-525)、_current_round_guard / add_annotation(拒绝转批注直接复用,D-P3-5 零新代码)、fake 测试族(test_session.py 29-97 FakeAICaller / fresh_session / wait_idle;744-762 RoundWritingFake;578-595 HangingFake;765-772 _enter_phase3)、prompts.py build_round_prompt 四段模子(259-352)+ _GRAMMAR_EXAMPLES / _ROUND_INSTRUCTIONS 常量三件套(210-256)、main.py 错误分支三模子(/api/g1 194-215、/api/rounds/process 332-350、pydantic Body 56-87)

DESIGN.md 权威依据:
- §4.4(G3 权威定义 + 默认拒绝)、§5.1(无状态全量读——prompt 资料段)、§5.2(事件直播:两跳照常走 SSE)、§5.4(权限矩阵消费——tmp 放行/DESIGN.md 拒绝已实现)、§6.1(目录:AUTHORIZATION.md 项目根;DESIGN-check-N)、§6.4(判定式锁定版只消费)、§7.3①②(撰写与自检中断重跑自愈)、§7.4 行 4-7(推导表:AUTHORIZATION/DESIGN.md/check 报告/PASS 完成)、§8.1(G3)、§8.2 全节(两角色 / 两跳自动 / 抛问契约 / 裁决落盘续跑 / D-22 残余裁决 / 宽松档追加 PASS)
- §§11 决策表:D-13(重跑覆盖)/ D-17(机械校验)/ D-21(完成态)/ D-22(纯 P2 残余裁决)

分支纪律(per 仓库 CLAUDE.md §5):本计划跨 3 个既有文件大改动——执行者从当前分支 HEAD 切出 phase-03/idi-03-02 工作分支,plan 完成后合回原分支(工作分支生命周期与 plan 对齐,不引入 worktree)。

测试纪律(D-P3-30):一切 pytest 必须 `.venv/bin/python -m pytest`。循环驱动实现形态已定:外层 wrapper(PATTERNS Modified Files #3 推荐方案②——else 分支短路不直接自调,由 finally 解锁后的驱动函数串调两跳)。
</context>

<tasks>

<task type="auto">
  <name>Task 1: authorize() + set_tier() + verdict_append() 同步动作三件 + build_writing_prompt + start_writing 流水线(tmp 原子改名)</name>
  <reversibility rating="costly">AUTHORIZATION.md 写入时机(仅确认词通过瞬间 + 后端)+ tmp→DESIGN.md 改名链是 §5.4/§7.4 行 4 的字面契约;路由载荷(POST /api/authorize 返回新 derive_state)是 Wave 4 前端的固定契约。</reversibility>
  <files>backend/session.py, backend/prompts.py, backend/main.py, backend/tests/test_session.py</files>
  <read_first>
  - backend/g3.py(Wave 1:g3_available 三查 + authorize_write FileExistsError 语义)
  - backend/session.py(g1 finalize 入口的 busy 检查 415-431 行做 authorize 的 busy 参考;process_round 528-629 完整模子;left 未进项目三查;add_annotation 667-685(D-P3-5 拒绝转批注就是它))
  - backend/prompts.py(210-232 _GRAMMAR_EXAMPLES 模板近似、235-256 _ROUND_INSTRUCTIONS 任务段模子、259-352 build_round_prompt 四段与资料段拼装)
  - backend/state.py(STATE_PHASE4 = "phase4" 行 24;derive_state 行 4:AUTHORIZATION 存在 + 无 check + 无 DESIGN.md → phase4)
  - backend/main.py(194-215 /api/g1 错误分支三分支模子;56-87 Body 类形态)
  - DESIGN.md §4.4(G3)、§7.4(行 4 + 授权痕迹)、§8.2(档位选择时机:DESIGN.md 初稿写完后弹出);§7.3①(撰写中断重跑)
  - .planning/phases/idi-03-g3/03-CONTEXT.md(D-P3-4 / D-P3-5 / D-P3-6 / D-P3-7 / D-P3-8 / D-P3-9 / D-P3-11 / D-P3-19)
  - backend/tests/test_session.py(29-97 FakeAICaller / fresh_session / wait_idle;744-762 RoundWritingFake 写盘 fake 模子;765-772 _enter_phase3 直造目录)
  </read_first>
  <behavior>
    - 用例 authorize 受理:造盘 phase3 四查合规 → authorize() 落 AUTHORIZATION.md → 再次 authorize() → False(幂等)
    - 用例 authorize 四查防绕过:phase3 但维度表含 ◐ → authorize() False;未进入项目 → RuntimeError
    - 用例 set_tier:phase5_awaiting_tier(有 DESIGN.md 无 check 报告造盘)→ 落 docs/DESIGN-check-tier.md;非该态(phase3/phase4)→ RuntimeError;"超严格" → ValueError
    - 用例 verdict_append:phase5_checking 造盘(DESIGN.md + check-1 报告含 `> 待裁决:#1:x` 无配对)→ verdict_append(1, "修", "按建议")追加 `> 裁决:#1:修——按建议` 形态行;重复 verdict 同号 → FileExistsError 冒出供路由 409
    - 用例 start_writing 闭环:WritingFake(写 tmp)→ done 后 tmp 消失、DESIGN.md 出现、derive_state = phase5_awaiting_tier(授权→写入→落盘全链 Fake 级)
    - 用例 start_writing tmp 缺失:fake 不写 tmp → error 事件含「撰写未产出 tmp」、状态留 phase4、start_writing 可重跑
    - 用例 start_writing 入口:phase3 造盘 → False;busy 在飞 → False
    - 用例 build_writing_prompt:产物含全部完整轮文档正文片段 + annotations 逐条(id/quote/note)+ transcript 片段 + 「DESIGN.md.tmp」落盘指令 + 明禁直写 DESIGN.md/AUTHORIZATION.md 语句 + 语言红线
    - 用例 build_writing_prompt 资料段不含 tmp/授权文件:造盘加半份 DESIGN.md.tmp 后组装 → 产物不含 tmp 内容片段(半份不入资料)
    - 用例路 409:POST /api/authorize 对 phase3 四查不过项目 → 409;POST /api/checks/tier 白名单外 → 400;POST /api/writing 非 phase4 → 409
  </behavior>
  <action>(1)backend/session.py 顶部 import 区扩展:from backend.state import 增 STATE_PHASE4、STATE_PHASE5_AWAITING_TIER, STATE_PHASE5_CHECKING, STATE_MISSION_COMPLETE(照既有 import 形态);from backend import g3、from backend import checks 模块引入(函数用点号,防命名冲突)。

(2)同步三件(照 answer_plain 的同步 + 单飞风格,均不起线程):
- authorize() -> bool:三查(未进项目 RuntimeError;busy → False(拒绝瞬时写授权,防在飞期间状态漂移);derive_state != phase3 或 not g3_available(project) → False 由路由层 409)→ g3.authorize_write(project)(FileExistsError 上抛——理论不可达(derive_state phase4 后 != phase3)但保留防御)→ True。docstring:四查后端再查的 D-P3-4 防绕过语义(前端按钮亮否只是呈现,服务端独立重判)。
- set_tier(tier: str) -> bool:未进项目 RuntimeError;derive_state != STATE_PHASE5_AWAITING_TIER → RuntimeError(f"仅待选档阶段可选(当前:{state})"——供路由 409);checks.write_tier(project, tier)(ValueError 白名单冒出供 400);返回 True。
- verdict_append(number: int, decision: str, note: str) -> bool:未进项目 RuntimeError;busy → False(单飞防双写竞态,D-P3-26);derive_state != STATE_PHASE5_CHECKING → RuntimeError→409;report_path = docs/DESIGN-check-{current_check}.md(derive_state 取)→ verdict_text = f"{decision}——{note}" → checks.append_user_verdict(report_path, number, verdict_text)(FileExistsError 冒出→409)。追加后判定残余是否清零:type=comment 的源暂为纯 P2 残余裁决场景——用 grammar.parse_problem_grades(latest) 与 parse_verdict_lines(latest) 比对:问题表全部问题均有同号裁决 → checks.append_pass_conclusion(report_path, "残余裁决收口")(D-P3-17 收口动作,单测证明)→ 返回 True。

(3)backend/prompts.py 新增 build_writing_prompt(project_path) -> str(照 build_round_prompt 四段结构,函数卡片式 docstring 登记 D-P3-7):角色段「总设计文档撰写引擎」+ _LANGUAGE_RULES;资料段——list_complete_rounds 循环注入全部完整轮文档全文 + 各轮 annotations_mod.load 逐条(id: quote: note:)+ _KNOWN_DOCS 既有循环注入 transcript/draft/brainstorm(**不读 DESIGN.md.tmp / AUTHORIZATION.md——docstring 记 D-P3-9**);任务段落盘指令常量 _WRITING_INSTRUCTIONS(照 _ROUND_INSTRUCTIONS 元组风格):产出无歧义总设计文档——覆盖维度表七个维度全部内容、吸收决策登记与已对齐结论、不含未决问题;用 Write 工具写 **DESIGN.md.tmp**(项目根,整体覆盖式写入)后即结束;**绝不直接写 DESIGN.md 或 AUTHORIZATION.md(权限门将拒绝)**——tmp 是 DESIGN.md 唯一合法落盘路径,后端会原子改名。

(4)backend/session.py 新增 writing_available(project) -> bool(照 round_process_available 纯磁盘风格:derive_state == STATE_PHASE4)+ start_writing() -> bool(照 process_round 模子逐段:三查(authorize 风格 + writing_available)→ prompt = build_writing_prompt(project) → 后台 _worker(事件循环照 process_round,支持中止)→ **done-else 分支后端动作**:重拉 derive_state → tmp = project/DESIGN.md.tmp、design = project/DESIGN.md;tmp.is_file() 且 design 未存在 → tmp.replace(design)(Path.replace 同 inode 原子改名,D-P3-8:改名前不校验 tmp 内容)→ 发信息性 say 事件「总设计文档已落盘」;tmp 不存在 → error 事件「撰写未产出 tmp,可重跑」(状态自然留 phase4,state 不变即可重跑)→ finally 解锁照抄。

(5)backend/main.py:Body 类 AuthorizeBody/TierBody(tier: str)加在 PlainBody 之后;路由加在 rounds 族之后、config 分节之前(新分节注释「阶段 3/4/5 路由族(PLAN idi-03-02)」):POST /api/authorize(RuntimeError→400 / 返回 False→409 / FileExistsError→409 / 成功 → 200 {"status":"ok", "state": 新 derive_state dict})、POST /api/checks/tier(set_tier:RuntimeError→409 / ValueError→400 / 成功 200)、POST /api/writing(start_writing True→202 accepted / False→409 / RuntimeError→400)。

(6)backend/tests/test_session.py 扩用例(造盘 helper:_enter_phase3_compliant——四查合规轮 + _enter_phase4 已授权 + _enter_phase5 DESIGN.md 与报告直造;WritingFake = FakeAICaller 子类照 RoundWritingFake 模子:run 时 write_text DESIGN.md.tmp):behavior 列表逐条,≥ 9 用例。route 级 409 分支入 test_route_session.py 可留 Task 3 统一补(RouteEnv 同款)——本任务先 session 级。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_session.py -q 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1'</automated>
    <fails_when>任一 pytest 输出含 failed/error;test_session.py 新增 authorize/start_writing/set_tier/verdict 用例合计 < 9(grep -c "def test_authorize\|def test_start_writing\|def test_set_tier\|def test_verdict" 为 0);WritingFake 闭环用例(改名/phase5 派生)失败;全量回归 passed < 143。</fails_when>
  </verify>
  <acceptance_criteria>
  - backend/session.py 四函数(authorize/set_tier/start_writing/verdict_append)逐名 `grep -n "def <名>" backend/session.py` 各命中且 `grep -n "def writing_available" backend/session.py` 命中
  - backend/session.py 的 start_writing done-else 分支含 `.replace(` 调用(grep -n "replace(design" 或 tmp 路径 replace 链可见)
  - backend/prompts.py 含 `grep -n "def build_writing_prompt" backend/prompts.py` 命中且源码含「DESIGN.md.tmp」字面与「绝不直接写 DESIGN.md」明禁语句(两处 grep 都命中)
  - build_writing_prompt 产物曲线:相关单测断言产物不含 tmp 内容片段(资料隔离证明)
  - POST /api/authorize 三分支(200/409/400)的 route 用例在本任务或 Task 3 补齐后全绿
  - WritingFake 闭环:done 后 DESIGN.md 存在 + tmp 不存在 + derive_state == phase5_awaiting_tier 三断言齐
  - 全量回归零失败
  </acceptance_criteria>
  <done>G3 授权链(四查→凭证→state=phase4)与撰写链(授权→AI 写 tmp→后端改名→state=phase5_awaiting_tier)Fake 级全绿;tmp 缺失 error 分支 + 可重跑证明;同步三件(选档/裁决)落盘动作就位;Wave 4 可按契约渲染确认词模态与撰写按钮。</done>
</task>

<task type="tracer">
  <name>Task 2: build_check_prompt / build_repair_prompt + start_check / start_repair 循环引擎(done-回调直排两跳 + 抛问截存暂停)</name>
  <reversibility rating="costly">报告文法(头部档位行/问题表/结论行)在 prompt 与解析器两端一字不差的联动是 D-P3-29 锁定;两跳自动推进的驱动形态(done-回调直排)是 §8.2「无需用户点击」的落地——引入 scheduler 或改锚点语义都会破坏自愈模型。</reversibility>
  <files>backend/prompts.py, backend/session.py, backend/tests/test_session.py, backend/tests/test_ai_caller.py</files>
  <read_first>
  - backend/prompts.py(Task 1 已加的 build_writing_prompt;210-256 _GRAMMAR_EXAMPLES/_ROUND_INSTRUCTIONS 模板常量模子)
  - backend/grammar.py(Wave 1:parse_tier_line / parse_problem_grades / is_pure_p2 / scan_pending_questions / TIER_LINE_STRICT / TIER_LINE_LOOSE;锁定六条)
  - backend/checks.py(Wave 1:append_pending_question / append_user_verdict / append_pass_conclusion / read_tier)
  - backend/session.py(Task 1 的 start_writing 与 writing_available;process_round 528-629 四段完整模子——本次最重要的复刻对象;threading 段 550-565 入口三查)
  - backend/state.py(75-85 max_check_number / latest_check_content;42 _CHECK_TEMPLATE)
  - backend/ai_caller.py(35-70 make_permission_decision:规则 1 DESIGN.md/AUTHORIZATION.md reject、规则 2 tmp allow——零改动消费)
  - DESIGN.md §8.2 全节(两角色/两跳自动/抛问识别契约/裁决落盘续跑/D-22 残余/宽松档 PASS)、§5.4(권限矩阵)、§7.3②(自检中断重跑)
  - .planning/phases/idi-03-g3/03-CONTEXT.md(D-P3-13 / D-P3-14 / D-P3-15 / D-P3-16 / D-P3-17 / D-P3-18 / D-P3-21 / D-P3-22)
  - .planning/phases/idi-03-g3/idi-03-PATTERNS.md(Modified Files #2 检查族 prompt 四段拼装 详细摘录;Modified Files #3 段 3/循环驱动/单飞锁解锁死锁别——外层 wrapper 方案②推荐说明)
  - backend/tests/test_ai_caller.py(25-44 矩阵断言族——补 AUTHORIZATION.md reject 断言)
  </read_first>
  <behavior>
    - 用例 build_check_prompt 三段:产物含 DESIGN.md 全文片段 + tier 头部行正例(引用 TIER_LINE 常量字面)+ 问题表头 `| 编号 | 级别 | 位置 | 问题 | 建议修法 |` 逐字 + 结论行文法(PASS 正例与 FIX 反例)+ 目标文件名 docs/DESIGN-check-{n}.md(n 参数注入)+ 干净的眼睛角色句 + 绝不修改 DESIGN.md 明禁 + 语言红线
    - 用例 build_check_prompt 多轮:已有 check-1 时 prompt 资料段含 check-1 全文(趋势照读)
    - 用例 build_repair_prompt:产物含最新报告全文 + `> 待裁决:#K:` 抛问协议说明 + tmp 落盘纪律 + DESIGN.md 全文
    - 用例 start_check 闭环 P1 报告:phase5_awaiting_tier + tier 签名 + CheckWritingFake(写 docs/DESIGN-check-1.md:头部档位行 + P1 问题表 + 末行 FIX)→ start_check → wait → 自动链入 start_repair(RepairFake 计数 1)→ RepairFake 写 tmp + 改名 → done → 自动回到检查(check-2 出现,CheckingCount 2)→ 第二轮 fake 产出纯 P2 报告 → 循环停在残余裁决态(无修复调用)——**严格档两跳自动驱动全链 Fake 级**
    - 用例 start_check PASS 报告:fake 写 PASS 末行报告 → done 后无下一跳(修复零调用)、derive_state = mission_complete
    - 用例 抛问截存:RepairFake 在 say 事件文本含 `> 待裁决:#2:范围问题` → done 后报告尾部出现 `> 待裁决:#2:范围问题` 行(checks.append_pending_question)、无下一跳 check-2(start_check 调用计数不增)、_ai_texts 已含该行(扫描源)
    - 用例 续跑:verdict_append 落盘裁决 → start_repair 再跑 → 报告含裁决行的新 prompt(资料段以磁盘为准)
    - 用例 start_check 入口拒绝:phase3/phase4 → False;busy → False;start_check 单飞在飞互斥(HangingFake)
    - 用例 权限矩阵回归:test_ai_caller 补 make_permission_decision(p, "write", p / "AUTHORIZATION.md") == "reject"(Specific Ideas 红线)
  </behavior>
  <action>(1)backend/prompts.py 新增两函数 + 一常量组(照 build_round_prompt 族):
- _CHECK_GRAMMAR_EXAMPLES(照 _GRAMMAR_EXAMPLES 元组形态,逐字):报告首行 `> 自检档位:严格|宽松`(与 tier 签名一致字面——引用时 f-string 拼注入 TIER_LINE 常量,不复制字面量)、问题分级表(二级标题「问题分级」,表头逐字 `| 编号 | 级别 | 位置 | 问题 | 建议修法 |`,级别仅 P0/P1/P2)、末行结论(`> 核查结论:FIX(P1×2 …)` 或零问题 `> 核查结论:PASS`)、裁决追加形态(`> 待裁决:#K:…` / `> 裁决:#K:…` 仅由后端追加,AI 正文不得以这两前缀开头,引用样例置于行内代码——§6.4 写作纪律)+ 硬指令「切勿改列名、切勿改头部/结论行格式——工具按此逐字解析」。
- build_check_prompt(project_path, check_n: int, tier: str) -> str:四段:角色「干净的眼睛:独立核查引擎,无讨论立场,只依据磁盘文件」+ 明禁「绝不修改 DESIGN.md,只写自家的核查报告」+ _LANGUAGE_RULES;资料段 = DESIGN.md 全文 + 全部完整轮文档 + 全部 annotations 逐条 + 已有全部 DESIGN-check 报告全文(max_check_number 循环,报告缺给显式说明);任务段 = 五维核查(内部一致性/历史批注符合度/决策无歧义/可实施性/结论覆盖)+ _CHECK_GRAMMAR_EXAMPLES 逐字 + 零问题时末行 PASS 否则 FIX 及计数 + 落盘指令「用 Write 工具产出 docs/DESIGN-check-{check_n}.md(编号由任务方给出,勿自定)」。
- build_repair_prompt(project_path, check_n: int, tier: str) -> str:资料段 = DESIGN.md 全文 + 最新报告全文(含裁决行,磁盘即状态)+ 其他既有报告 + 轮次文档/批注;任务段 = 报告问题按裁决逐条修复(如仍有未配对待裁决,先停下)+ 用户职权问题(范围与非目标类)不得替用户决定——在最终回复文本里单独一行输出 `> 待裁决:#K:<问题>` 后即结束(抛问协议正式说明)+ 用 Write 工具整体写 DESIGN.md.tmp 后结束(修复同样走 tmp 单次整体落盘纪律,绝不直写 DESIGN.md)+ 宽松档特例指令:唯一一轮修复完成后在报告末追加 PASS 结论行(用 Write 整体重写报告含原内容 + 末行 PASS,或 Edit 追加——落盘物必须末行前缀合规)。

(2)backend/session.py 三入口 + 驱动器:
- check_available(project) -> bool:derive_state ∈ {STATE_PHASE5_CHECKING} → True;**STATE_PHASE5_AWAITING_TIER 在起检前必须有 tier 签名文件**(checks.read_tier(project) 非 None;选档是起检前置,D-P3-11/D-P3-14 相关)→ True;其余 False。
- repair_available(project) -> bool:derive_state == STATE_PHASE5_CHECKING(最新报告存在非 PASS)→ True(细化的判定式②暂停态约束在 UI 层由 snapshot 呈现,服务端以 409 入口判定为准——start_repair 对 unpaired 非空也放行会被 Wave 4 限制,本层守住 phase5_checking + 无在飞即可,对 D-P3-20 判定式②「裁决待续跑」的服务端强制为「unpaired_verdicts 非空时 start_repair 拒绝」加一条判定——写并用例证明)。
- start_check() -> bool 与 start_repair() -> bool:照 process_round 模子(三查 + _worker + SSE + finally 解锁);start_check 的 done-else 分支后端动作 = 循环驱动的判定头部(重拉 derive_state → 读最新报告 → ① is_pass_conclusion(latest) → 结束(mission_complete 推导态自然出现,Wave 4 弹窗)②is_pure_p2(latest) → 结束不修复(残余裁决态)③其余 → 驱动 start_repair);start_repair 的 done-else = 全文本扫描 `> 待裁决:`(用 scan_pending_questions(_ai_texts 合并文本)——只取首个命中号,按 D-P3-18 幂等截存)命中 → checks.append_pending_question 当轮报告尾部 + error 事件「修复者抛问,已截存暂停,等待用户裁决」、不驱动下一跳;未命中 → tmp 存在则 tmp.replace 改名 → 驱动判定(宽松档:tier == "宽松" → 结束(不下一跳;PASS 由修复者已追加或残余收口动作);严格档 → start_check(check_n + 1))。
- **驱动实现形态(定案=外层 wrapper)**:else 分支不直接自调(单飞锁未释放会自我拒绝)——两函数尾部解耦:else 分支只把「下一步动作」记为函数局部 pending_action(或驱动函数 _drive_next(project, kind)),finally 解锁后由驱动函数串调(每跳独立入栈一层,线程尾部串新线程/直接同步调——推荐 finally 后直接调 start_repair/start_check 的同步形式,每跳结束重拉磁盘判定,无 scheduler,D-P3-16 字面)。abort 语义:任何时刻 _aborted → 驱动链条断(else 不排下一跳),「继续自检/继续修复」恢复。
- verdict 侧已在 Task 1(残余全配对 → append_pass_conclusion 收口)。unpaired_verdicts(repair 拒绝)用 grammar 既有锁定函数判定(判定式①服务端强制)。

(3)backend/tests/test_ai_caller.py 补一条(AUTHORIZATION reject 断言,Specific Ideas 红线「AI 尝试写 AUTHORIZATION.md 被拒」测试覆盖)。

(4)backend/tests/test_session.py 扩用例(≥ 9,fake 族扩展:CheckWritingFake(scripts 事件序列里 before_done 写报告)/ RepairWritingFake(写 tmp,或 say 事件带 `> 待裁决:` 行)、fake.tier/脚本参数化):behavior 列表逐条覆盖(闭环两跳/纯 P2 停/PASS 停/抛问截存/续跑/入口拒绝/单飞)。**两跳自动链的断言核心 = 修复调用计数与 check 报告最终编号**(check-1 → repair(1) → check-2 → 纯 P2 停:2 份报告、1 次修复)。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_session.py backend/tests/test_ai_caller.py -q 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1'</automated>
    <fails_when>任一 pytest 输出含 failed/error;两跳自动链用例失败(修复调用计数 0 或 check-2 未出现);抛问截存用例失败(报告尾部无 `> 待裁决:` 行或 check 计数仍推进);AUTHORIZATION reject 断言失败;全量回归 passed < 143。</fails_when>
  </verify>
  <acceptance_criteria>
  - backend/prompts.py 的 `grep -n "def build_check_prompt\|def build_repair_prompt" backend/prompts.py` 命中行数 ≥ 2 且源码 grep -n "| 编号 | 级别 | 位置 | 问题 | 建议修法 |" 命中(表头字面逐字)
  - backend/session.py 四函数(start_check/start_repair/check_available/repair_available)逐名 `grep -n "def <名>" backend/session.py` 各命中,且两 done-else 分支均含 derive_state 重拉判定
  - backend/session.py 的自检驱动实现无 scheduler / threading.Timer / while True 轮询(grep 后两词为 0;循环只经驱动函数逐跳串调)
  - test_session.py 两跳自动链用例:check-1(非 PASS 非 P2)触发 start_repair 真被调(fake 计数 ≥ 1),纯 P2 报告后无新 check 编号
  - 抛问截存:报告尾行出现 `> 待裁决:#K:`(内容级幂等),且无下一跳推进
  - test_ai_caller.py 含 AUTHORIZATION.md reject 断言(grep "AUTHORIZATION" 命中 ≥ 2:import 行 + 断言行)
  - 全量回归零失败
  </acceptance_criteria>
  <done>两角色循环引擎 Fake 级全链证明:严格档 check→repair→check-2 的两跳自动推进、纯 P2 停在残余裁决、PASS 即 mission_complete、抛问截存暂停且不误推进;check/repair promp 字面与 grammar 解析器两端一字不差;AI 写 AUTHORIZATION.md 被矩阵拒绝的最终断言在位。</done>
</task>

<task type="auto">
  <name>Task 3: 二入 GET 路由 + _session_snapshot 扩展(g3_available / selfcheck 子状态)+ 路由级全分支用例</name>
  <reversibility rating="costly">GET /api/design 与 GET /api/checks 的响应形状(selfcheck 子状态 tier/mode/questions)是 Wave 4 阶段 5/归档视图的唯一数据源;mode 的判定边界(paused 的.No.①判定式)与 §6.4 锁定版一致即定形。</reversibility>
  <files>backend/session.py, backend/main.py, backend/tests/test_route_session.py</files>
  <read_first>
  - backend/session.py(_session_snapshot 135-163 现形态;Task 1/2 已加六函数)
  - backend/grammar.py(锁定:unpaired_verdicts / is_pass_conclusion;Wave 1:parse_tier_line / parse_problem_grades / scan_pending_questions)
  - backend/state.py(latest_check_content 87-92;STATE_MISSION_COMPLETE 行 27)
  - backend/main.py(GET /api/rounds 234-246 与 get_draft 138-148 组装模子;GET /api/rounds/{round_n} 250-275 的嵌套组装;202/409 分支 332-350)
  - DESIGN.md §6.4(判定式①②锁定/同号配对)、§7.4 完成、§8.2(暂停态/裁决待续跑的界面规格)
  - .planning/phases/idi-03-g3/03-CONTEXT.md(D-P3-20 / D-P3-23 / D-P3-27)
  - backend/tests/test_route_session.py(route_env 24-29 形态;_enter_phase3_route helper)
  </read_first>
  <behavior>
    - 用例 snapshot(phase3 四查合规):响应含 g3_available: true;维度污染盘 → false
    - 用例 snapshot(phase5_checking 报告含未配对待裁决):selfcheck.mode == "paused"、selfcheck.questions 非空(裁决卡数据:number + text)
    - 用例 snapshot(phase5_checking 报告含配对裁决无未配对 + 末行非 PASS):mode == "resumed"
    - 用例 snapshot(phase5_checking 报告正常 without 裁决):mode == "running"、tier 从报告头部行恢复
    - 用例 snapshot(mission_complete):mode == "done"
    - 用例 snapshot(phase5_awaiting_tier):tier = tier 文件值或 None(重开恢复档位,无报告时 tier 文件为中间态凭证)
    - 用例路由 GET /api/design(phase4 及以后):200 {status: ok, design: 文本};DESIGN.md 不存在 → design: null
    - 用例路由 GET /api/checks(phase5_checking):200 含 checks: [编号列表] + latest 报告全文 + selfcheck 对象(透传 snapshot 字段)
    - 用例路由 POST /api/checks/verdict:200 追加 / 同号 FileExistsError → 409 / busy → 409 / 非 phase5_checking → 409
    - 用例路由 POST /api/authorize:成功 200 返回新 state / 四查不过 409 / 已授权 409(phase4 造盘直接 POST → 409 幂等)
  </behavior>
  <action>(1)backend/session.py _session_snapshot 扩展(既有字段不动、不重命名):新增 "g3_available": 条件为 phase3 态时调 g3.g3_available(project)(否则 False);新增 "selfcheck" 子状态对象——按 state 组装:STATE_MISSION_COMPLETE → {"tier": 报告头部 parse_tier_line(latest), "mode": "done", "questions": []};STATE_PHASE5_CHECKING → latest = latest_check_content(docs);tier = parse_tier_line(latest) 或 read_tier(project) 兜底;mode:unpaired_verdicts(latest) 非空 → "paused"(questions = scan_pending_questions(latest) 映射的裁决卡数据)→ 有配对裁决行且无未配对且末行非 PASS → "resumed" → 否则 "running";STATE_PHASE5_AWAITING_TIER → {"tier": read_tier(project), "mode": "running", "questions": []};其余态 → {"tier": None, "mode": "running", "questions": []}(注意:推导函数只认磁盘不缓存,不调 AI——D-P3-23)。

(2)backend/main.py:GET /api/design(session.current_project_path() + DESIGN.md read_text 兜底 None;未进项目 RuntimeError → 400 照 get_draft;STYLE 上照 get_draft 138-148)——JSONResponse {"status":"ok", "design": content};GET /api/checks(checks 列表 = derive_state current_check 或 max 编号遍历、latest 报告全文 = latest_check_content、selfcheck = snapshot 的 selfcheck 透传、unpairedQuestions 可选——按 snapshot 已有字段直接组合,不重复判定)——{"status":"ok", "checks": [...], "latest": ...};**新路由 GET /api/design + GET /api/checks 与 Task 1 的 POST 六条一起归入「阶段 3/4/5 路由族」分节**;TierBody/VerdictBody(number: int, decision: str, note: str)pydantic 类;POST /api/checks/verdict 分支(RuntimeError 消息含「裁决」或「阶段」→ 409;FileExistsError → 409;ValueError → 400)。

(3)backend/tests/test_route_session.py 扩用例(≥ 8;route_env + 造盘 helper 直造各态盘:phase3/p hase4/phase5_awaiting_tier/phase5_checking 各态、带报告各分支):behavior 列表逐条(模式三态 + tier 恢复 + design/checks 组装 + 全 409 分支)。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_session.py backend/tests/test_route_session.py -q 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1'</automated>
    <fails_when>任一 pytest 输出含 failed/error;test_route_session.py 新增 selfcheck/design/checks/authorize 用例 < 8(grep -c "def test_route_authorize\|def test_route_checks\|def test_route_design\|def test_route_verdict" 为 0);判定式①②的 mode 三分支任一失败;全量回归 passed < 143。</fails_when>
  </verify>
  <acceptance_criteria>
  - GET /api/session 响应含 "g3_available" 键与 "selfcheck" 键(route 用例断言);selfcheck.mode 三值(running/paused/resumed)与 done 各有专属用例
  - backend/main.py 的 `grep -n "api/design\|api/checks" backend/main.py` 命中行数 ≥ 6(GET 两 + POST 四 tier/start/repair/verdict + authorize 计)
  - 自检子状态判定消费 grammar 锁定函数(grep -n "unpaired_verdicts" backend/session.py 命中,无第二份同判定重实现)
  - _session_snapshot 既有字段(rounds / pending_annotations / transcript / draft / brainstorm / divergence_available / g1_available)全部保留不动(git diff 零删除)
  - 全量回归零失败
  </acceptance_criteria>
  <done>快照两新字段与两条 GET 组装路由就位;自检子状态三态 + done 的判定式消费(与 §6.4 锁定版一致)全部 route 级证明;Wave 4 可按 /api/session + /api/design + /api/checks 三契约渲染全部阶段视图。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 浏览器 → POST /api/authorize | 确认词在前端模态完成(呈现层),服务端防线 = 四查 + phase3 再判 + AUTHORIZATION.md 后端写入动作本身——前端校验不是安全边界 |
| AI 产出 tmp/报告 → 后端改名/追加 | AI 输出不可信:tmp 可能缺失、报告可能不合规、修复者可能输出伪 `> 待裁决:` 行(引用样例) |
| 循环驱动 → 磁盘判定 | 两跳自动推进必须每步重拉磁盘(不依赖闭包内存),识别不到待裁决标记不得当作正常完成 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi03-06 | Elevation of Privilege | 绕过前端确认词直接 POST /api/authorize 写入 AUTHORIZATION.md | critical | mitigate | 服务端入口三查:derive_state == phase3 + g3_available 四查再查(任一不过 409);AUTHORIZATION.md 已存在 → FileExistsError → 409 幂等;唯一凭证是后端写入本身,不存在绕过确认词的 API 路径(D-P3-3/4) |
| T-idi03-07 | Tampering | AI 直写 DESIGN.md 绕过 tmp 纪律 | high | mitigate | 权限矩阵规则 1 reject 已实现(零改动消费);test_ai_caller 补 AUTHORIZATION.md reject 断言;所有 DESIGN.md 落盘 = start_writing/start_repair 的后端 rename,别无路径 |
| T-idi03-08 | Tampering | 修复者输出伪 `> 待裁决:` 行(报告引用样例/无关文本)导致误暂停 | medium | mitigate | scan_pending_questions 行内代码引用形态防误收(Wave 1 用例已盖);截存内容级幂等不重复追加;识别到标记一律暂停(误暂停代价 = 用户看一眼跳过,比误推进安全——D-P3-18 兜底语义) |
| T-idi03-09 | Denial of Service | 严格档循环因 AI 永不 PASS 死循环跑 | medium | mitigate | 每跳结束重拉磁盘判定(磁盘是唯一依据);abort 随时杀 + 驱动链断;纯 P2 报告停(不再修复);无 scheduler——每跳线程串行,天然有界;E2E Wave 5 真实验证循环节奏 |
| T-idi03-10 | Tampering | 多窗口并发:撰写/核查/修复/裁决同时落盘竞态 | high | mitigate | start_writing/start_check/start_repair 入口 _inflight 单飞(五先例);verdict_append busy 检查 + append_user_verdict 同号 FileExistsError 双防线;路由层 409 |
| T-idi03-11 | Repudiation | 裁决落盘无痕迹无法追溯 | low | mitigate | `> 裁决:#K:<decision>——<note>` 形态保留用户原话;换行内容级幂等保留首答 |

执行说明:本计划零新包安装(纯 SDK/CLI 既有),无供应链项;SSE 与权限矩阵均消费 Phase 1 已建机制。
</threat_model>

<verification>
1. Task 1 automated:pytest test_session.py(authorize/set_tier/verdict/start_writing ≥ 9 用例)+ 全量回归
2. Task 2 automated:pytest test_session.py + test_ai_caller.py(两跳自动链/纯 P2 停/PASS 停/抛问截存/AUTHORIZATION reject)+ 全量回归
3. Task 3 automated:pytest test_route_session.py(snapshot 两字段 + GET design/checks + 409 全分支 ≥ 8 用例)+ 全量回归
4. 真 CLI 的撰写/自检全链(真实 tmp 改名、真实两跳循环)在 idi-03-04 的 IDI_E2E 门控用例验证,不在本计划
5. 无人检项(后端层;浏览器人检在 Wave 4/5)
</verification>

<success_criteria>
- authorize 防绕过链(四查服务端再查 + FileExistsError 幂等)与撰写改名链(tmp→DESIGN.md→phase5_awaiting_tier)Fake 级全绿
- 严格档两跳自动驱动全链 Fake 级证明(check-1→repair→check-2,纯 P2 停,PASS 停);抛问截存暂停 + 裁决定续跑闭环
- set_tier/verdict_append 同步落盘动作 + snapshot 的 g3_available/selfcheck 子状态(tier + mode 三态)可被路由直接消费
- 六 POST + 两 GET 路由契约固定,409/400/404 分支与 CONTEXT 逐条一致
- AI 写 AUTHORIZATION.md/DESIGN.md 被矩阵拒绝的断言在位(零改动消费)
- 全量回归 143 基线只增不减
</success_criteria>

## Artifacts this phase produces(本计划新增符号清单)

- backend/session.py:authorize() -> bool、set_tier(tier) -> bool、verdict_append(number, decision, note) -> bool、writing_available(project) -> bool、start_writing() -> bool、check_available(project) -> bool、repair_available(project) -> bool、start_check() -> bool、start_repair() -> bool、自检驱动函数(_drive_next 或等价形态)、_session_snapshot 新增 g3_available / selfcheck 字段
- backend/prompts.py:WRITING/CHECK/REPAIR 三族——build_writing_prompt(project_path) -> str、build_check_prompt(project_path, check_n, tier) -> str、build_repair_prompt(project_path, check_n, tier) -> str、_WRITING_INSTRUCTIONS、_CHECK_GRAMMAR_EXAMPLES、_REPAIR_INSTRUCTIONS(或等价命名)
- backend/main.py:AuthorizeBody、TierBody、VerdictBody、POST /api/authorize、POST /api/checks/tier、POST /api/writing、POST /api/checks/start、POST /api/checks/repair、POST /api/checks/verdict、GET /api/design、GET /api/checks
- backend/tests/test_session.py:WritingFake、CheckWritingFake、RepairWritingFake、_enter_phase3_compliant / _enter_phase4 / _enter_phase5 造盘 helper、authorize/start_writing/set_tier/verdict_append/start_check(两跳闭环/纯 P2/PASS)/抛问截存/续跑/入口/单飞用例族
- backend/tests/test_route_session.py:snapshot 两字段 + GET design/checks + 全 409 分支用例

<output>
Create `.planning/phases/idi-03-g3/idi-03-02-SUMMARY.md` when done
</output>

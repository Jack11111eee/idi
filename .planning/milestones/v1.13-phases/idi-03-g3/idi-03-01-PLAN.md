---
phase: idi-03
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - backend/g3.py
  - backend/checks.py
  - backend/grammar.py
  - backend/tests/test_g3.py
  - backend/tests/test_checks.py
  - backend/tests/test_grammar.py
autonomous: true
requirements:
  - FLOW-05
  - DATA-04

estimate:
  tokens: 85000
  raw_tokens: 85000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "backend/g3.py 的 g3_available(project) 四条机械校验全部命中才 True,且四条在同一份当前轮文档快照上判定(读一次文本复用,不跨轮):①annotations.select_pending(load(current_round)) 为空;②grammar.is_pending_list_clear;③grammar.is_dimension_table_green;④grammar.parse_auth_marker == \"yes\";current_round 取 derive_state 的最大完整轮(半成品轮视为不存在),derive_state != phase3 或四查任一不过 → False ← FLOW-05 / D-P3-1 / D-P3-2 / ROADMAP 判据 1"
    - "g3 的 authorize_write(project) 在项目根写入 AUTHORIZATION.md(不在 docs/ 下):明文 UTF-8,含「授权时间(ISO-8601)+ 操作者确认词标记行」两要素(§7.4 授权痕迹);AUTHORIZATION.md 已存在 → FileExistsError(G3 只走一次,幂等防护照 g1.py 先例);写入前调用方负责先过 g3_available 四查再查(本模块不重复查,职责单一) ← FLOW-05 / D-P3-4(纯函数半)"
    - "backend/grammar.py 新增三个纯增量解析器,不触碰既有六条锁定语义(check-14 锁定版只消费):parse_tier_line(report_text)(返回 \"严格\"/\"宽松\"/None——首部 prefix 扫描 `> 自检档位:` 行 strip 后恰为两串之一)、parse_problem_grades(report_text)(问题分级表 → [{number(int), level, location, issue, suggestion}],表头 | 编号 | 级别 | 位置 | 问题 | 建议修法 |;number 转 int 与 scan_pending_questions/裁决行 #K 同型)、is_pure_p2(report_text)(全部问题 level == P2 → True;空表/无表/无结论行锚点(半份)→ False,fail-closed)← DATA-04 / D-P3-15 / D-P3-17(纯 P2 判据)"
    - "backend/grammar.py 新增 scan_pending_questions(text):无锚点全文扫 `> 待裁决:#K:` 形态行,返回 [{number, text}](number 为 int),供修复者输出扫描(D-P3-18 先流后文本两处均可复用)与暂停态问题呈现;匹配正则 _PENDING_QUESTION_RE 从 _VERDICT_RE 的待裁决分支派生(同文件常量,不复制第二份独立形态来源) ← D-P3-18 / D-P3-19"
    - "backend/checks.py 档位签名与报告追加三件套:write_tier(project, tier) 落盘 docs/DESIGN-check-tier.md(头部一行 `> 自检档位:严格|宽松`,覆盖式写入幂等);read_tier(project)(文件不存在/脏内容 → None);append_pending_question(report_path, number, text) 内容级幂等(同内容已存在 → 跳过返回 False);append_user_verdict(report_path, number, text) 同号拒绝(已存在同号裁决行 → 拒绝);append_pass_conclusion(report_path, note) 在报告末追加 `> 核查结论:PASS(...)` 行(成为最后一个非空行) ← DATA-04 / D-P3-11(落盘半)/ D-P3-12 / D-P3-17(收口半)/ D-P3-19"
    - "全部新增解析器配构造正反例测试(照 D-P2-17/D-P2-18 先例):tier 行 正/脏/缺、问题表 正/空表/级别脏值/混 P0P1P2、待裁决行 配对后滤除、同号裁决重复拒绝 ← D-P3-29 / FLOW-07 延续"
    - "全量 pytest 回归基线 143 passed + 4 skipped 不下降(新增用例另计,常轨零失败)← D-P3-30"
  artifacts:
    - path: "backend/g3.py"
      provides: "G3 纯函数模块:g3_available(project) 四查组合判定 + authorize_write(project) AUTHORIZATION.md 后端写入(g1.py 同级零依赖 pathlib 模块)"
      contains: "def g3_available"
    - path: "backend/checks.py"
      provides: "自检磁盘签名读写纯函数:write_tier / read_tier / append_pending_question / append_user_verdict / append_pass_conclusion"
      contains: "def append_user_verdict"
    - path: "backend/grammar.py(扩展)"
      provides: "报告侧纯增量解析器:parse_tier_line / parse_problem_grades / is_pure_p2 / scan_pending_questions(既有六条零改动)"
      contains: "def parse_problem_grades"
    - path: "backend/tests/test_g3.py"
      provides: "四查组合正反例(四条各一「AI 产物污染」反例)+ authorize_write FileExistsError 幂等 + 内容两要素"
    - path: "backend/tests/test_checks.py"
      provides: "tier 落盘/读回/脏内容、待裁决内容级幂等、裁决同号拒绝、PASS 追加成为末行"
    - path: "backend/tests/test_grammar.py(扩展)"
      provides: "新解析器正反例矩阵(tier 行/问题表/纯 P2/待裁决文本扫描)"
  key_links:
    - from: "backend/g3.py g3_available"
      to: "backend/grammar.py + backend/annotations.py"
      via: "select_pending / is_pending_list_clear / is_dimension_table_green / parse_auth_marker 四函数组合(不重新实现第二套,D-P3-1 铁律)"
      pattern: "from backend.grammar import"
    - from: "backend/checks.py append_user_verdict"
      to: "backend/grammar.py parse_verdict_lines"
      via: "同号裁决已存在的判定消费(锁定函数只读不改)"
      pattern: "parse_verdict_lines"
    - from: "backend/g3.py authorize_write"
      to: "Wave 2 session.authorize() → POST /api/authorize"
      via: "路由入口先 derive_state==phase3 + g3_available 再查后调 authorize_write(FileExistsError → 409)"
      pattern: "authorize_write"
  prohibitions:
    - statement: "grammar.py 既有六条文法(判定式①②语义、锚点取末一处、同号配对、strip 全等)禁改——check-14 锁定互斥版已实现,本阶段只消费;新增解析器仅限报告头部档位行与 P0/P1/P2 问题分级表(含待裁决文本扫描)"
      status: unverified
      flagged: true
    - statement: "G3 四查必须复用 grammar.py/annotations.py 既有解析器与 select_pending,不得重新实现第二套(含同义包装函数重写判定逻辑)"
      status: unverified
      flagged: true
    - statement: "g3.py 不得含确认词解析(后端不重复解析自然语言,后端防线 = 仅确认词通过瞬间由路由层调 authorize_write 的动作本身,D-P3-3/D-P3-4)"
      status: unverified
      flagged: true
    - statement: "tier 档位必须落盘为磁盘签名文件 docs/DESIGN-check-tier.md(不落盘的选档违反文件即状态),且不落 docs/ 外的其他位置"
      status: unverified
      flagged: true
    - statement: "裁决/待裁决追加必须保持「结论行之后追加 + 末行前缀判定不受影响」——追加动作只 append 到报告尾部,不改写正文"
      status: unverified
      flagged: true
    - statement: "不新增第三方依赖(纯标准库 pathlib/re/datetime);不得引入新测试基建(D-P3-30)"
      status: unverified
      flagged: true
---

## Phase Goal

**As a** 即将走完三道门的用户,**I want to** 工具用机械校验(而非采信 AI 自评)告诉我何时点亮「授权撰写总设计文档」,我的授权成为唯一落盘凭证,自检档位与每一条裁决都有磁盘签名,**so that** G3 门与阶段 5 的一切判定都有可靠的数据地基(Wave 2/3 流水线与 Wave 4 视图直接消费本计划契约)。

<objective>
Phase 3 的纯数据脊柱(tracer 切到最底层,照 idi-02-01 模子):交付三个零依赖纯模块——backend/g3.py(G3 四查组合判定 g3_available + AUTHORIZATION.md 后端写入 authorize_write)、backend/checks.py(tier 签名文件与报告尾部追加族:待裁决截存/用户裁决/PASS 收口三件)、backend/grammar.py 纯增量解析器(报告头部档位行、P0/P1/P2 问题分级表、纯 P2 判定、待裁决文本扫描)。全部构造正反例单测证明。既有六条文法语义零触碰(state.py 零改动)。

Purpose: G3 是 Core Value 红线(未经用户明确授权绝不进入撰写),四查与授权凭证必须机器可复核且不可被 AI 绕过;档位/裁决/PASS 的磁盘签名是阶段 5 判定式的唯一依据(D-P3-11/12/17/19)。
Output: backend/g3.py + backend/checks.py + grammar.py 增量 + 三个测试文件(全绿),Phase 3 全部上层的 import 基座。
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

依赖接口(来自 Phase 1/2,直接消费,不重定义):
- backend/state.py:derive_state 返回 {state, current_round, current_check}(行 95-147);STATE_PHASE3 常量(行 23);list_complete_rounds / last_nonempty_line;**本计划对 state.py 零改动**
- backend/grammar.py:is_pending_list_clear / is_dimension_table_green / parse_auth_marker(四查的三条解析现成,锁定版);parse_verdict_lines / unpaired_verdicts / is_pass_conclusion(判定式核心,本计划只 import 消费);_extract_table(md_text, heading_keyword) 表格共通解析(行 73-109,问题表解析复用)
- backend/annotations.py:load(project, round_n) / select_pending(annotations)
- backend/g1.py:后端受控产物写入 + FileExistsError 幂等防护的模子(全文件 52 行)

DESIGN.md 权威依据:
- §4.4(G3 权威定义:四处机械校验 + 默认拒绝 + AUTHORIZATION.md 后端写入)
- §5.4(权限矩阵:写 AUTHORIZATION.md 仅后端;写 DESIGN.md.tmp 放行——AI 调用侧零改动消费)
- §6.1(目录结构:AUTHORIZATION.md 在项目根;docs/DESIGN-check-N.md 自检报告)
- §6.4(判定式①②锁定版——只消费;裁决追加文法 + 内容级幂等)
- §7.4 行 3/行 4(授权痕迹两要素:授权时间 + 操作者确认词标记;行 4「继续撰写」)
- §8.2(档位记录于报告头部落盘;D-22 纯 P2 残余裁决;裁决追加落盘同报告末尾)

分支纪律(per 仓库 CLAUDE.md §5,照 idi-02-01 形态):执行者从当前分支 HEAD 切出 phase-03/idi-03-01 工作分支,plan 完成后合回原分支(工作分支生命周期与 plan 对齐,不引入 worktree)。

测试纪律(D-P3-30):一切 pytest 必须 `.venv/bin/python -m pytest`(系统 Python 无 claude_agent_sdk);基线 143 passed + 4 skipped 只增不减。
</context>

<tasks>

<task type="tracer">
  <name>Task 1: g3.py 纯模块——g3_available 四查组合判定 + authorize_write AUTHORIZATION.md 写入</name>
  <reversibility rating="costly">四查语义与 AUTHORIZATION.md 落点(项目根、后端写入、幂等)是 §4.4/§7.4 字面契约——Wave 2 路由(POST /api/authorize 的服务端再查)与 Wave 4 按钮(g3_available 显隐)都消费这一形状,改动即破坏 Core Value 红线。</reversibility>
  <files>backend/g3.py, backend/tests/test_g3.py</files>
  <read_first>
  - backend/g1.py(全文件 52 行:模块头 docstring 形态 1-16、FileExistsError 双查顺序 37-43、构造文本→写盘 45-51)
  - backend/state.py(21-27 状态常量;61-73 list_complete_rounds;95-147 derive_state 的行 3「当前轮 = 最大完整轮」语义;158-162 _read_text 兜底形态)
  - backend/grammar.py(120-153 parse_dimension_table / is_dimension_table_green;155-181 parse_pending_list / is_pending_list_clear;183-201 parse_auth_marker 三态)
  - backend/annotations.py(load / select_pending 签名与返回形态)
  - DESIGN.md §4.4(G3 权威定义四处校验)、§5.4(AUTHORIZATION.md 仅后端写)、§7.4(行 3 + 授权痕迹段落:授权时间 + 操作者确认词标记两要素)
  - .planning/phases/idi-03-g3/idi-03-PATTERNS.md(New Files #1:g3.py 全部模子摘录与偏差说明)
  - .planning/phases/idi-03-g3/03-CONTEXT.md(D-P3-1 / D-P3-2 / D-P3-4)
  </read_first>
  <behavior>
    - 四查全过(当前轮文档:维度表全 ✓、清单全已决、末行 `> 申请授权:是`、annotations 无 pending comment)→ g3_available True
    - ①污染:当前轮 annotations 含一条 pending comment → False(其余三条合规)
    - ②污染:清单含一行「待决」→ False
    - ③污染:维度表含一行 ◐ → False
    - ④污染:末行 `> 申请授权:否` → False
    - derive_state 非 phase3(无完整轮 / 已授权 phase4 / phase1_new)→ False
    - authorize_write:写入 project/AUTHORIZATION.md,内容含 ISO-8601 授权时间与「确认授权」确认词标记;再次调用 → FileExistsError
    - g3.py 不得 import fastapi/pydantic/AI 层(零依赖纯模块)
  </behavior>
  <action>新建 backend/g3.py(零第三方依赖纯 pathlib 模块,模块头 # -*- coding: utf-8 -*- + 中文 docstring 引用 §4.4/§7.4/D-P3-1/D-P3-4;import 仅 logging/datetime/pathlib + from backend.state import STATE_PHASE3, derive_state + from backend import annotations as annotations_mod + from backend.grammar import is_dimension_table_green, is_pending_list_clear, parse_auth_marker)。公开 API 两个:

(1)AUTHORIZATION_FILENAME = "AUTHORIZATION.md"(项目根,§7.4 行 3;注意不在 docs/ 下,注释引 §6.1)。g3_available(project_path) -> bool:纯靠磁盘推导(照 session.round_process_available 的「纯磁盘、防绕过」风格):derive_state → state == STATE_PHASE3 且 current_round 非 None,否则 False;取 project/docs/discuss-round-{N}.md 文本读**一次**(OSError/不存在 → False——文档在则轮完整,防御读失败即关闸,fail-closed);同一份文本快照上连判四条:select_pending(annotations_mod.load(project, N)) 为空、is_pending_list_clear(text)、is_dimension_table_green(text)、parse_auth_marker(text) == "yes"——四条全过才 True。docstring 铭记 D-17「机械校验而非采信 AI 自评」与 D-P3-1「同一份当前轮文档快照,不跨轮」。

(2)authorize_write(project_path) -> Path:前置幂等查——(project / AUTHORIZATION_FILENAME).is_file() → raise FileExistsError(中文消息引「G3 只走一次,重开已授权项目按 §7.4 行 4 显示继续撰写」);写内容 = 明文 UTF-8 markdown,含两要素行:授权时间 = datetime.now(timezone.utc).isoformat()、操作者确认词标记行含「确认授权」(具体排版照 Claude's Discretion,两要素文本可 grep 到为准);write_text 落盘 project 根(项目目录必已存在——enter 前置,不加 mkdir);logger.info 记录;返回路径。docstring 写明:调用方(Wave 2 路由)负责先 derive_state==phase3 + g3_available 再查后调用——本模块不重复四查(职责单一,组合判定在入口层)。

新建 backend/tests/test_g3.py(照 test_g1.py 同族:tmp_path 直造 + 合规文档样本 helper):样本 helper 造一个「四查合规」当前轮文档(五件套最小样本:含全 ✓ 维度表、全已决清单、末行 > 申请授权:是)+ 空 annotations;八条正反用例如 behavior 所列(四查各自污染反例必须每条一个独立用例,ROADMAP 判据 1 的机器可复核性证明)+ FileExistsError 幂等(先 authorize_write 一次成功,二次 raise)+ 内容两要素断言(read_text 后 in 检查 ISO 日期片段与「确认授权」)。测试不得读本项目自身 docs/ 历史文档(样本全部手造,D-P2-19 延续)。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_g3.py -q 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1'</automated>
    <fails_when>任一 pytest 输出含 failed 或 error(退出码非零,pipefail 保证 tail 不吞);test_g3.py 用例数 < 8;全量回归 passed < 143(基线下穿)。</fails_when>
  </verify>
  <acceptance_criteria>
  - backend/g3.py 存在且 `grep -n "def g3_available" backend/g3.py` 与 `grep -n "def authorize_write" backend/g3.py` 各命中一行定义
  - `grep -n "AUTHORIZATION_FILENAME = " backend/g3.py` 命中且值为 "AUTHORIZATION.md"(项目根)
  - g3.py 的 import 区无 fastapi/pydantic/claude 关键词(零框架依赖纯模块)
  - `grep -n "from backend.grammar import\|from backend import annotations" backend/g3.py` 命中(四查复用既有解析器,非重实现)
  - test_g3.py ≥ 8 用例全绿,其中四查污染反例 ≥ 4 个(用例名含 pending/待决/◐或 dimension/标记关键词可 grep)
  - 全量回归 143 passed 4 skipped 之上叠加新用例零失败
  </acceptance_criteria>
  <done>g3.py 两函数可用:四查组合判定经四条污染反例 + 合规正例证明;AUTHORIZATION.md 写入含两要素且 FileExistsError 幂等;零第三方依赖;Wave 2 可直接 import。</done>
</task>

<task type="auto" tdd="true">
  <name>Task 2: grammar.py 三解析器增量——parse_tier_line / parse_problem_grades / is_pure_p2 + scan_pending_questions</name>
  <reversibility rating="costly">报告头部档位行与问题分级表的表头字面(| 编号 | 级别 | 位置 | 问题 | 建议修法 |)是与 prompt 逐字注入联动的机器文法(Wave 3 的 build_check_prompt 按 D-P3-29 逐字贴入同一字面)——两端必须一字不差,定形后改动即导致 AI 产出解析失败。</reversibility>
  <files>backend/grammar.py, backend/tests/test_grammar.py</files>
  <read_first>
  - backend/grammar.py(37-47 __all__ 登记形态;51 _VERDICT_RE;73-109 _extract_table 共通表格解析;120-133 parse_dimension_table 的列→dict 映射模子;183-201 parse_auth_marker 三态返回模子;248-283 parse_verdict_lines / unpaired_verdicts;**既有六条函数体一行不改**)
  - backend/tests/test_grammar.py(既有正反例族形态与样本 helper)
  - DESIGN.md §6.4(锁定版判定式——本任务所有新增只增量不触碰)、§8.2(档位记录于报告头部;D-22 纯 P2 判据;`> 待裁决:#K:` 抛问协议)
  - .planning/phases/idi-03-g3/03-CONTEXT.md(D-P3-15 / D-P3-17 / D-P3-18)
  - .planning/phases/idi-03-g3/idi-03-PATTERNS.md(Modified Files #4:parse_tier_line 首部 prefix 扫描建议与 parse_problem_grades 列映射)
  </read_first>
  <behavior>
    - parse_tier_line:报告首部存在 strip 后恰为 `> 自检档位:严格` 的行 → "严格";恰为 `> 自检档位:宽松` → "宽松";无该行/脏变体(如「> 自检档位:超严格」或行内有尾注)→ None(H1 标题行在前不干扰——扫「首个以 `> 自检档位:` 开头的行」)
    - parse_problem_grades:报告含二级标题「问题分级」(关键词与 prompt 注入字面一致)下的表格 → [{"number"(int),"level","location","issue","suggestion"}](列 = 编号/级别/位置/问题/建议修法,各列 strip,number 列转 int——脏编号(如「一」)保留 0 + warning 不抛;表头行与分隔行丢弃);无该表 → [];级别列脏值(如「高」)照读不抛(消费方 is_pure_p2 自然判 False)
    - is_pure_p2:问题表全为 P1×2 + P2×1 → False;全 P2 → True;空表/无表 → False(零问题报告走 PASS 路径,不以纯 P2 处理,fail-closed);**无 `> 核查结论:` 锚点行(半份 P2 报告,P2 表已写结论行未写)→ False**(回落 running 态由「继续自检」恢复,不得进 p2 死局)
    - scan_pending_questions:文本含 `> 待裁决:#3:范围问题` 行 → [{"number": 3, "text": "范围问题"}];同文本含 `> 裁决:#3:接受` 不进结果(只扫待裁决);形态不符(`> 待裁决 3:` 无冒号井号)→ 不收;多行多号全收
    - 既有六条函数与 __all__ 既有项零变化(git diff 中六函数体无改动)
  </behavior>
  <action>backend/grammar.py 纯增量追加(放在 unpaired_verdicts 之后,分节注释照既有 `# ---` 形态;__all__ 同步扩四个新名):

(1)parse_tier_line(md_text: str) -> str | None:splitlines 扫描,取**首个** strip 后 startswith("> 自检档位:") 的行;整行 strip 后恰为 "> 自检档位:严格" → "严格",恰为 "> 自检档位:宽松" → "宽松",其余(存在但脏)→ None;扫完全文无该前缀行 → None。模块级常量 TIER_LINE_STRICT = "> 自检档位:严格" / TIER_LINE_LOOSE = "> 自检档位:宽松"(供 Wave 3 prompt 逐字引用同一常量,不复制字面量)。

(2)parse_problem_grades(md_text: str) -> list[dict]:复用 _extract_table(md_text, "问题分级")(heading_keyword = "问题分级",与 prompt 注入的二级标题字面一致——两端同字面是 D-P3-29 硬要求);列序 = 编号/级别/位置/问题/建议修法 → {"number", "level", "location", "issue", "suggestion"}(照 parse_dimension_table 的列→dict 映射模子,列不足补空串);**number 列转 int**(int(cell.strip());转不动(脏值如「一」)→ 保留 0 并 warning——与 scan_pending_questions 的 int number 同型,裁决卡 number 直接可 POST /api/checks/verdict 配对 `> 裁决:#K:` 的整数 K,不做字符串/整数混型比较);无表 → []。挂导出。

(3)is_pure_p2(md_text: str) -> bool:rows = parse_problem_grades(md_text);rows 为空 → False;**报告无 `> 核查结论:` 锚点行 → False(半份报告,fail-closed——P2 表已写但结论行未写的中途崩溃形态不得判纯 P2,否则 mode 推 p2 藏「继续自检」成死局态,须回落 running 走 D-P3-20/§7.3② 恢复;复用 grammar 既有 _last_conclusion_index 判 None)**;全部 row["level"] == "P2" → True(P0/P1 任一出现即 False)。

(4)scan_pending_questions(text: str) -> list[dict]:全文无锚点扫描,逐行匹配待裁决行——**不新建第二份正则字面量**:`_VERDICT_RE` 锚定「结论行之后」不可直接复用,故从它**派生**新常量 _PENDING_QUESTION_RE = re.compile(r"^>\s*待裁决:#(\d+):(.*)$")(同 _VERDICT_RE 的前缀/分组风格书写,行注释声明「形态来源 _VERDICT_RE 的待裁决分支」,两常量同文件同节放置);匹配 → {"number": int(group(1)), "text": group(2).strip()}。**不改 parse_verdict_lines**(锁定)——新函数独立,服务于修复者输出扫描(D-P3-18:say 事件流与最终文本都能喂进来)与暂停态问题呈现。

新建用例入 backend/tests/test_grammar.py(先红后绿):正反例矩阵 ≥ 12 条——tier 行 正严格/正宽松/无行/脏值/尾注脏变体、问题表 正例三行混级(number 断言为 int 型)/空表/列脏值照读/编号脏值(「一」→ number == 0 且不抛)、is_pure_p2 全P2/混P1/空表False/**半份P2盘False(P2 表有 + 结论行无)**、scan_pending 多号/配对裁决不收/形态不符/文本中行内代码引用样例不误收(引用样例形如「`> 待裁决:#1:` 整段在行内代码」——按 §6.4 写作纪律行内代码引用不进配对,本扫描器对整行为行内代码包裹的形态是否误收做一个显式用例,实现按「strip 后以 ` 开头的行跳过」或等价防御,择简实现并写注释)。样本全部手造,不读本项目 docs/ 历史报告(D-P2-19 延续)。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_grammar.py -q 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1'</automated>
    <fails_when>任一 pytest 输出含 failed/error;test_grammar 新增用例 < 12(用例名含 tier/problem/p2/pending_question 计数不足);git diff 显示既有六条函数体被改动(diff 区块越界到 is_pending_list_clear/is_pass_conclusion 等函数体);全量回归 passed < 143。</fails_when>
  </verify>
  <acceptance_criteria>
  - backend/grammar.py 的 `grep -n "def parse_tier_line\|def parse_problem_grades\|def is_pure_p2\|def scan_pending_questions" backend/grammar.py` 命中行数 ≥ 4(且逐名 `grep -n "def <名>"` 各命中)且四名进 __all__
  - `grep -n "TIER_LINE_STRICT\|TIER_LINE_LOOSE" backend/grammar.py` 命中(常量供 prompt 逐字引用)
  - `git diff backend/grammar.py` 中 is_pending_list_clear / is_dimension_table_green / parse_auth_marker / parse_annotation_responses / is_pass_conclusion / parse_verdict_lines / unpaired_verdicts 七函数体零改动(diff 只含追加区)
  - test_grammar.py 新增 ≥ 12 用例全绿,空表 is_pure_p2 → False 与行内代码引用防误收两类边界各有具名用例
  - 全量回归零失败
  </acceptance_criteria>
  <done>四个新解析器就位且既有六条锁定语义经 git diff 证明零触碰;表头字面与 TIER 常量定案(Wave 3 prompt 逐字消费);正反例矩阵全绿。</done>
</task>

<task type="auto" tdd="true">
  <name>Task 3: checks.py 纯模块——tier 签名文件读写 + 报告尾部追加三件(待裁决截存/用户裁决/PASS 收口)</name>
  <reversibility rating="costly">tier 签名文件落点(docs/DESIGN-check-tier.md)与裁决追加文法(内容级幂等 vs 同号拒绝)是 §8.2/§6.4 的磁盘签名契约——Wave 3 的 start_check/set_tier/verdict_append 与 Wave 4 的档位恢复都消费;改语义即破坏判定式的唯一依据。</reversibility>
  <files>backend/checks.py, backend/tests/test_checks.py</files>
  <read_first>
  - backend/g1.py(后端受控产物写入模子:幂等防护 + 构造文本 + write_text)
  - backend/annotations.py(load 的「不存在返回空形态 + 脏内容 warning 兜底」模子——read_tier 照抄语义)
  - backend/grammar.py(Task 2 的 TIER_LINE_STRICT/TIER_LINE_LOOSE 常量与 is_pass_conclusion;parse_verdict_lines 供同号判定消费)
  - backend/state.py(_CHECK_TEMPLATE = "DESIGN-check-{n}.md" 行 42;75-85 max_check_number)
  - DESIGN.md §6.4(裁决追加文法:结论行之后、内容级幂等)、§8.2(档位选择落盘、待裁决追加到报告末尾、裁决落盘同报告、宽松档/残余收口 PASS 追加)
  - .planning/phases/idi-03-g3/03-CONTEXT.md(D-P3-11 / D-P3-12 / D-P3-17 / D-P3-19)
  </read_first>
  <behavior>
    - write_tier(project, "严格") → docs/DESIGN-check-tier.md 存在且内容含头部行 `> 自检档位:严格`;再次 write_tier(project, "宽松") → 覆盖为宽松(覆盖式幂等,重选可改)
    - read_tier:文件不存在 → None;内容头部行合法 → "严格"/"宽松";脏内容 → None + warning 日志(不抛)
    - write_tier 传入白名单外值(如 "超严格")→ ValueError(中文消息)
    - append_pending_question(report_path, 3, "范围问题"):报告尾部追加 `> 待裁决:#3:范围问题`;同内容重复调用 → 返回 False 不重复追加(内容级幂等);同号新内容 → 追加第二行(判定式按 §6.4 不受影响——幂等为内容级,非号级)
    - append_user_verdict(report_path, 3, "修"):追加 `> 裁决:#3:修`;同号已存在裁决行 → raise FileExistsError(同号拒绝,D-P3-19「择拒绝重复 POST 同号」的纯函数层)
    - append_pass_conclusion(report_path, "残余裁决收口"):报告末追加 `> 核查结论:PASS(残余裁决收口)`;追加后该行成为最后一个非空行(grammar.is_pass_conclusion → True 经断言)
    - 三类追加都只 append 到文件尾(先读后写整文件 或 "a" 模式 append 单行——择简,语义 = 不改写正文任何行)
  </behavior>
  <action>新建 backend/checks.py(零第三方依赖纯 pathlib 模块,中文 docstring 引 §8.2/§6.4/D-P3-11/12/17/19;import 仅 logging/datetime/pathlib + from backend.grammar import is_pass_conclusion, parse_verdict_lines, TIER_LINE_STRICT, TIER_LINE_LOOSE):

(1)TIER_FILENAME = "DESIGN-check-tier.md"(docs/ 下,§6.1 目录树;D-P3-11 落点)。TIER_VALUES = {"严格", "宽松"} 白名单。

(2)write_tier(project_path, tier: str) -> Path:tier 不在白名单 → ValueError(中文);target = project/docs/DESIGN-check-tier.md;内容 = f"{TIER_LINE_STRICT 或 TIER_LINE_LOOSE}\n"(单行文件,头部行即全文;tier 参数选常量,不手拼字符串)+ 一行来源说明注释可选(保持单行纯净由 planner 择简——内容必须使 read_tier 命中);write_text 覆盖落盘(重选档覆盖,幂等);返回路径。

(3)read_tier(project_path) -> str | None:文件不存在 → None;读文本首非空行 strip 恰为两常量之一 → 对应值;否则(warning 日志)→ None。

(4)append_pending_question(report_path, number: int, text: str) -> bool:构造行 = f"> 待裁决:#{number}:{text}";读现文(不存在 → FileNotFoundError,中文消息——报告必须先存在,调用方保证);该行已在文中(整行 strip 全等)→ return False(内容级幂等);否则在末尾追加(现文rstrip + "\n\n" + 行 + "\n" 或 "a" 模式——择简,不改正文);return True。

(5)append_user_verdict(report_path, number: int, text: str) -> Path:读现文(FileNotFoundError 同上);parse_verdict_lines(现文) 中存在 kind=="裁决" 且 number 相同 → raise FileExistsError(中文:「#K 已有裁决,一问一答,不重复受理」——路由层 409);追加 f"> 裁决:#{number}:{text}" 行到末尾;返回路径。

(6)append_pass_conclusion(report_path, note: str) -> Path:读现文;构造 f"> 核查结论:PASS({note})"(前缀匹配语义,§6.4);若 is_pass_conclusion(现文) 已 True → 直接返回不重复追加(幂等);否则末尾追加;返回路径。

新建 backend/tests/test_checks.py(tmp_path 直造 + 手造报告样本 helper——样本含一个非 PASS 结论行如 `> 核查结论:FIX(P1×1)` + 一个 P2 问题表,确保追加行落在结论行之后):behavior 列表逐条成用例 ≥ 10(tier 写读回/白名单 ValueError/脏内容 None、待裁决追加 + 内容级幂等跳过、裁决追加 + 同号 FileExistsError、PASS 追加后 is_pass_conclusion 断言为 True + 幂等二跳不重复)。**追加后 is_pass_conclusion(现文) 为 True 的断言必须有**——PASS 行成为末锚点的机器证明。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_checks.py -q 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1'</automated>
    <fails_when>任一 pytest 输出含 failed/error;test_checks.py 用例数 < 10;append_user_verdict 的同号拒绝用例失败(FileExistsError 未按预期抛出);全量回归 passed < 143。</fails_when>
  </verify>
  <acceptance_criteria>
  - backend/checks.py 存在且五个函数(write_tier/read_tier/append_pending_question/append_user_verdict/append_pass_conclusion)逐名 `grep -n "def <名>" backend/checks.py` 各命中一行定义
  - `grep -n "DESIGN-check-tier.md" backend/checks.py` 命中(落点字面)
  - checks.py import 区无 fastapi/pydantic;`grep -n "TIER_LINE_STRICT" backend/checks.py` 命中(常量复用不复制)
  - test_checks.py ≥ 10 用例全绿,含 is_pass_conclusion 追加后转 True 断言与同号 FileExistsError 用例
  - 全量回归零失败(143 基线 + 新增)
  </acceptance_criteria>
  <done>档位签名三件(写/读/白名单)与报告尾部追加三件(待裁决内容级幂等/裁决同号拒绝/PASS 收口)全部有绿色用例;Wave 3 的 session 层可把这些纯函数直接挂接为「选档落盘、截存暂停、裁决续跑、残余收口」动作。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| AI 产出的轮次文档/报告 → g3_available / 新解析器 | AI 写出的内容不可信(维度表可能脏、标记可能缺失、报告尾部可能被污染),四查与解析器必须对任意文本给确定判定不崩 |
| 磁盘 tier/报告文件 → checks.py 读写 | 签名文件可能被外部改动或损坏(半写/脏内容),读路径必须给 None 兜底,写路径必须幂等防重复追加 |
| 修复者输出文本 → scan_pending_questions | 不可信 AI 输出文本,`> 待裁决:` 行可能是引用样例(行内代码)而非真实抛问——误收即误暂停 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi03-01 | Elevation of Privilege | AI/外部调用绕过四查直接让 g3_available 判 True(如构造脏文档骗过解析) | critical | mitigate | 四查全部消费锁定版 grammar 解析(strip 全等/锚点取末一处),脏值 fail-closed(维度脏值行判非绿、标记三态只有恰等才 yes);四条污染反例单测逐条证明;g3_available 读文档失败一律 False |
| T-idi03-02 | Tampering | append 族被并发调用造成重复裁决行/重复 PASS | medium | mitigate | 内容级幂等(append_pending_question 同内容跳过)+ 同号拒绝(append_user_verdict FileExistsError)+ PASS 已存在直接返回;Wave 3 路由层再加单飞锁双防线;单测覆盖三幂等分支 |
| T-idi03-03 | Tampering | 报告正文被追加动作改写(修历史问题清单破坏审计) | medium | mitigate | 三追加函数只 append 到文件尾不改写正文任何行;acceptance criteria 的 diff 级断言(追加前后正文逐字不变)作为用例 |
| T-idi03-04 | Denial of Service | scan_pending_questions 对畸形输入抛异常拖垮修复调用收流 | medium | mitigate | 纯文本逐行匹配,无 IO;对空文本/无匹配返回 [](空列表合法返回,不抛);正反例含形态不符用例 |
| T-idi03-05 | Repudiation | AUTHORIZATION.md 无时间戳导致授权时刻不可追溯 | low | mitigate | authorize_write 内容含 ISO-8601 授权时间(两要素之一);测试断言 ISO 日期片段存在 |

执行说明:本计划零 npm/pip/cargo 安装(纯标准库),无 T-{phase}-SC 供应链威胁项。AI 写 AUTHORIZATION.md 被权限门拒绝属 §5.4 已实现矩阵,本计划纯函数层不涉 AI 调用(Phase 1 matrix 测试,test_ai_caller.py 32 行已有 DESIGN.md reject;AUTHORIZATION.md reject 断言由 Wave 2 计划补)。
</threat_model>

<verification>
1. Task 1 automated:pytest test_g3.py ≥ 8 用例(四查污染反例 ≥ 4)+ 全量回归
2. Task 2 automated:pytest test_grammar.py 新增 ≥ 12 用例 + git diff 证明既有六条零触碰 + 全量回归
3. Task 3 automated:pytest test_checks.py ≥ 10 用例(含 PASS 末行锚点断言与同号拒绝)+ 全量回归
4. 全部任务的 verify 已含全量回归(143 passed + 4 skipped 基线不降);本计划无人检项(纯后端函数层,浏览器面在 Wave 4)
</verification>

<success_criteria>
- g3.py / checks.py 两个纯模块 + grammar.py 四个增量解析器可被任何上层直接 import(零 FastAPI/AI 依赖)
- 四查「机械校验而非采信 AI 自评」经每条污染反例单测证明;AUTHORIZATION.md 两要素 + FileExistsError 幂等
- tier 签名落盘/读回/脏内容兜底、待裁决内容级幂等、裁决同号拒绝、PASS 收口成为末行锚点全部有绿色用例
- 既有六条文法锁定语义经 git diff 证明零改动
- 全量 pytest 回归:143 + 新增用例全绿
</success_criteria>

## Artifacts this phase produces(本计划新增符号清单)

- backend/g3.py:AUTHORIZATION_FILENAME、g3_available(project_path) -> bool、authorize_write(project_path) -> Path
- backend/grammar.py(增量):TIER_LINE_STRICT / TIER_LINE_LOOSE 常量、parse_tier_line(md_text) -> str|None、parse_problem_grades(md_text) -> list[dict]、is_pure_p2(md_text) -> bool、scan_pending_questions(text) -> list[dict];__all__ 扩四名
- backend/checks.py:TIER_FILENAME、TIER_VALUES、write_tier(project_path, tier) -> Path、read_tier(project_path) -> str|None、append_pending_question(report_path, number, text) -> bool、append_user_verdict(report_path, number, text) -> Path、append_pass_conclusion(report_path, note) -> Path
- backend/tests/test_g3.py、backend/tests/test_checks.py(新测试文件)、backend/tests/test_grammar.py(增量用例)

<output>
Create `.planning/phases/idi-03-g3/idi-03-01-SUMMARY.md` when done
</output>

---
phase: idi-02
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - backend/annotations.py
  - backend/grammar.py
  - backend/tests/test_annotations.py
  - backend/tests/test_grammar.py
autonomous: true
requirements:
  - FLOW-07
  - DATA-01

estimate:
  tokens: 80000
  raw_tokens: 80000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "backend/annotations.py 的 load 对不存在的 discuss-round-N.annotations.json 返回 {\"round\": N, \"items\": []} 空形态而非抛异常;JSON 脏文件同样返回空形态并记 warning 日志(不抛不悬空,D-P2-5) ← DATA-01 / FLOW-04 boundary:文件不存在与文件损坏是两类不同输入,同一确定返回"
    - "append_item 落盘条目字段一字不差 = id/quote/before/type/note/status/answer/created_at,顶层含 round;id 形如 a3-01(N=轮次,NN=该轮条目递增序号),同轮第二条为 a3-02 ← DATA-01 / §6.2 字面契约"
    - "writeback(project, round, answers) 仅回写回应表中出现的 id(命中项 answer 被填、status pending→answered),未在表中的 id 保持 pending 不动,返回命中条数 ← DATA-01 / D-P2-13 精确契约:回写以 id 配对为唯一依据,AI 未提及的批注绝不误标已回应"
    - "locate_quote 在 quote 于全文唯一时命中起点;quote 出现多次且某匹配点前文以 before 结尾时取那一处;仍不唯一取第一处;无匹配返回 None(精确匹配,不引入模糊匹配,D-P2-6) ← UI-01 定位精度 / FLOW-04:被批注文本永不变化由轮次冻结保证,定位不漂移"
    - "backend/grammar.py 能解析六条 §6.4 结构:维度表(二级标题含「覆盖维度表」,全绿 ⇔ 无 ◐ 与 ✗)、未决清单(标题含「未决问题清单」,清零 ⇔ 无待决)、授权申请标记(末非空行 strip 后恰为两串之一)、批注回应表(标题含「批注回应」,id 与回应两列可提取)、PASS 结论行(锚点取最后一处 `> 核查结论:` 行,前缀匹配)、裁决追加行(`> (待裁决|裁决):#K:` 形态、仅统计结论行之后、同号配对)——全部以正反例单测证明 ← FLOW-07 / ROADMAP 成功判据 6(含结论行锚点取末一处、同号配对边界)"
    - "grammar.py 复用 backend/state.py 的 AUTH_MARKER_YES/AUTH_MARKER_NO/PASS_PREFIX/last_nonempty_line,不重复实现两套判定(D-P2-16)——源码无第二份标记字符串常量定义 ← FLOW-07"
    - "本项目自身 docs/discuss-round-0~4 不进任何单测正例;测试样本全部手造合规文档(D-P2-19) ← FLOW-07 边界:历史文档不回溯"
    - "全量 pytest 回归基线 66 passed 2 skipped 不下降(test_annotations + test_grammar 新增用例另计)"
  artifacts:
    - path: "backend/annotations.py"
      provides: "annotations.json 纯读写模块:load / append_item / writeback / locate_quote(与 state.py / transcript.py 同级零依赖 pathlib 模块)"
      contains: "def append_item"
    - path: "backend/grammar.py"
      provides: "§6.4 六条机器文法解析器(纯文本函数,复用 state.py 常量,不与 state.py 重复实现)"
      contains: "def parse_dimension_table"
    - path: "backend/tests/test_annotations.py"
      provides: "annotations 存储文法与定位算法用例(正反例)"
    - path: "backend/tests/test_grammar.py"
      provides: "六条文法正反例用例矩阵(合规/非合规/脏变体/锚点取末一处/同号配对)"
  key_links:
    - from: "backend/grammar.py(批注回应表解析器)"
      to: "backend/annotations.py(writeback)"
      via: "process_round 在 done 后把回应表行(批注id→回应)交给 writeback 回写 answer/status(本计划定契约,Wave 2 计划消费)"
      pattern: "writeback"
    - from: "backend/grammar.py"
      to: "backend/state.py"
      via: "import AUTH_MARKER_YES/AUTH_MARKER_NO/PASS_PREFIX/last_nonempty_line,同一语义不复制第二份"
      pattern: "from backend.state import"
  prohibitions:
    - statement: "AI 子进程不得直接写 annotations 文件(建条目与回写全部走后端函数,D-P2-7)"
      status: unverified
      flagged: true
    - statement: "annotations.py 存盘结构不得用 pydantic 重定义字段(存盘 JSON 字面即 §6.2;pydantic 仅可选用于 API 入口校验,D-P2-5)"
      status: unverified
      flagged: true
    - statement: "grammar.py 不得与 state.py 重复实现两套授权标记/PASS 判定(必须 import 复用,D-P2-16)"
      status: unverified
      flagged: true
    - statement: "不得解析本项目自身的历史 discuss-round-0~4 文档作为单测正例或判定输入(D-P2-19)"
      status: unverified
      flagged: true
    - statement: "不得新增第三方依赖(annotations/grammar 均为标准库 pathlib+json+re 模块)"
      status: unverified
      flagged: true
    - statement: "locate_quote 不得引入模糊匹配/编辑距离等复杂算法(DESIGN.md §6.2 直接否决:轮次冻结保证精确匹配足够,D-P2-6)"
      status: unverified
      flagged: true
---

## Phase Goal

**As a** 讨论收敛中的用户,**I want to** 我写下的每条批注被精确保存并挂在我划选的那段原文上,AI 产出的每一轮文档能被工具逐字机械解析,**so that** 批注永不丢失定位、回应可被配对回写、§6.4 六处机械校验全部由工具可靠判定(而不是采信 AI 自觉)。

<objective>
Phase 2 的纯数据脊柱(tracer 切到最底层):交付两个零依赖纯模块——backend/annotations.py(§6.2 annotations.json 读写 + quote/before 定位算法)与 backend/grammar.py(§6.4 六条机器文法解析,复用 state.py 常量)。全部正反例单测证明:维度表全绿判定、清单清零判定、授权标记精确匹配、回应表 id 配对、PASS 锚点取末一处、裁决同号配对,以及 annotations 的空形态/建条目/回写/定位四类行为。这两个模块是 Wave 2(process_round 回写)与 Wave 3(前端批注流渲染)消费的唯一数据契约。

Purpose: 文法判定和批注存储是「四处机械校验」的地基——AI 写乱轮次文档时 annotations 不被连带污染(D-P2-5 纯模块隔离),回写只认回应表中的 id、不依赖 AI 自觉(D-P2-13)。
Output: backend/annotations.py + backend/grammar.py + 两个测试文件(全绿),Phase 2 全部上层的 import 基座。
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

依赖接口(来自 Phase 1,直接使用,不重定义):
- backend/state.py:AUTH_MARKER_YES / AUTH_MARKER_NO / PASS_PREFIX / last_nonempty_line / is_complete_round / list_complete_rounds / ROUND 文件名约定(discuss-round-N.md)
- backend/transcript.py:纯 pathlib 模块的形态模子(不存在返回空形态 + 父目录自举 + warning 兜底)
- backend/g1.py:后端读-改-写受控产物先例(writeback 的整文件重写形态模子)

DESIGN.md 权威依据:
- §6.2(D-18):annotations.json 完整字段契约(顶层 round + items 八字段)、定位靠精确文本匹配(quote + before 辅助)、字段写回职责(后端建条目、批量处理后回写 answer 与 status、AI 不直接改写)、plain 不计入未决清单
- §6.4:六条机器文法全部原文(维度表/未决清单/授权标记/批注回应表四表 + PASS 结论行锚点取末一处 + 裁决追加行同号配对、判定式自上而下首条命中)
- §6.3:五件套与批注回应表列(批注id/原文摘录/回应,id 对应上一轮 annotations)
- §3.5(D-07):轮次冻结保证被批注文本永不变化——定位精确匹配的法律依据
- §7.3:半成品判据与重跑覆盖(回应表缺失时不回写、保持 pending 的语义地基)

分支纪律(per 仓库 CLAUDE.md §5):本计划全部为新增文件(零触碰既有源码)——执行者从当前分支 HEAD 切出 phase-02/idi-02-01 工作分支,plan 完成后合回原分支(工作分支生命周期与 plan 对齐,不引入 worktree)。

本计划任务结构说明:三个任务按「store → parse → verify 定位配对」推进,Task 1 与 Task 2 相互独立可在同一分支顺序实施;Task 3 校验两者拼合的回写闭环(纯函数级,不起任何 AI/服务)。
</context>

<tasks>

<task type="tracer">
  <name>Task 1: annotations.py 纯存储模块——load 空形态 / append_item 建条目 / writeback 回写</name>
  <reversibility rating="costly">annotations.json 字段集与文件命名(discuss-round-N.annotations.json)是 §6.2 字面契约:Wave 2 process_round 回写与 Wave 3 前端批注流都消费这一形状,改字段即破坏 DESIGN.md 权威定义。</reversibility>
  <files>backend/annotations.py, backend/tests/test_annotations.py</files>
  <read_first>
  - backend/transcript.py(形态模子:不存在返回空形态 34-39 行、父目录自举 81-84 行、warning 兜底)
  - backend/g1.py(读-改-写整文件重写先例,45-51 行)
  - backend/state.py(文件名模板常量风格,42-43 行 _ROUND_TEMPLATE)
  - DESIGN.md §6.2(字段八项 + 顶层 round 的字面契约,195-215 行)
  - .planning/phases/idi-02-g2/idi-02-PATTERNS.md(New Files #1:函数边界建议与 id 方案)
  - .planning/phases/idi-02-g2/02-CONTEXT.md(D-P2-5/D-P2-7/D-P2-13)
  </read_first>
  <behavior>
    - 文件不存在 → load 返回 {"round": N, "items": []}(空形态带轮号,不抛)
    - JSON 脏文件(手写坏 JSON) → 同样返回空形态 + warning 日志,不抛(D-P2-5:AI 写乱轮次文档时 annotations 不被连带污染)
    - append_item 首条 → id = "a1-01";同轮第二条 → "a1-02";round=3 轮 → "a3-01"(aN-NN 方案,与 §6.2 示例同构)
    - append_item 后落盘 JSON 字段一字不差:id/quote/before/type/note/status/answer/created_at + 顶层 round
    - append_item(type=plain)时 answer 可随建随写、status 落 answered(大白话即时答);type=comment 时 status 落 pending、answer 为 null
    - writeback({"a1-01": "回应内容"}) → 该条目 answer="回应内容"、status="answered";未提及的 "a1-02" 保持 pending;返回命中数 1
    - writeback 传入不存在的 id → 忽略,不抛,返回命中数不含它
    </behavior>
  <action>新建 backend/annotations.py(零第三方依赖纯 pathlib 模块,模块头 # -*- coding: utf-8 -*- + 中文 docstring 引用 §6.2/D-18/D-P2-5),导入仅 logging/json/pathlib/datetime。公开 API 四个:

(1)ANNOTATIONS_TEMPLATE = "discuss-round-{n}.annotations.json"(§6.1 文件名字面;照 state.py 的 _ROUND_TEMPLATE 常量风格,注释引 §6.1)。annotations_path(project_path, round_n) -> Path 辅助函数返回 project/docs/discuss-round-N.annotations.json。

(2)load(project_path, round_n) -> dict:文件不存在返回 {"round": round_n, "items": []};json.JSONDecodeError 与 OSError 同样 warning + 返回空形态(照 transcript.py 34-39 行"读不到给确定判定"模式;单测断言两类失败同形态)。顶层 round 字段以参数 N 为准(读到的文件 round 不可信时不覆写本判定——直接返回盘上 items + 参数 round)。

(3)append_item(project_path, round_n, *, quote, before, type, note, answer=None) -> dict:load 全量 → 生成 id = f"a{round_n}-{len(items)+1:02d}"(aN-NN)→ 追加条目 {id, quote, before, type, note, status, answer, created_at}(status:type=comment 落 "pending"、type=plain 落 "answered";created_at = datetime.now(timezone.utc).isoformat();answer:plain 时调用方传入即时答文本,comment 时 None)→ 父目录自举(docs/ 不存在则 mkdir parents,照 transcript.py 81-84 行)→ json.dumps(obj, ensure_ascii=False, indent=2) 整体写盘 → 返回新建条目 dict。type 仅接受 "comment"/"plain" 之外的值时 ValueError(中文错误消息)。

(4)writeback(project_path, round_n, answers: dict[str, str]) -> int:load 全量 → 对 items 中每个 id 在 answers 里出现的条目:answer = answers[id]、status pending→answered(已是 answered 的重写 answer 也合法,覆盖语义)→ 未在 answers 中出现的 id 一律不动(D-P2-13:回写只认表中 id,不依赖 AI 自觉)→ 整体重写落盘 → 返回命中条数。answers 中的 id 不存在于 items → 忽略不抛(返回值不含)。

(5)select_pending(annotations: dict) -> list[dict]:纯内存过滤 type=comment 且 status=pending 的条目(session 层与前端计数共用语义,D-P2-15:plain 不计)。此函数无 IO。

(6)locate_quote(full_text, quote, before) -> int | None(见 Task 3 详述,可与本任务同文件一并交付或 Task 3 补——函数必须在本模块,D-P2-6 前后端共用配对语义)。

新建 backend/tests/test_annotations.py(照 test_transcript.py 骨架:模块头中文 docstring + write helper + tmp_path 直写;sys.path 注入头照 tests 既有形态):behavior 列表逐条成用例,至少 8 个(空形态×2(不存在/坏 JSON)、建条目字段齐全断言(id/quote/before/type/note/status/answer/created_at 逐键 in)、id 递增 a1-01→a1-02、跨轮 a3-01、plain 建条目即 answered、writeback 命中+未命中混合、return 值命中数、select_pending 过滤 plain)。字段齐全断言用 set(item.keys()) == {"id","quote","before","type","note","status","answer","created_at"} 精确全等。
  </action>
  <read_first>补充:backend/tests/test_transcript.py(1-24 行:模块头 + write helper + import 形态)</read_first>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_annotations.py -q 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1'</automated>
    <fails_when>任一 pytest 输出含 failed 或 error(退出码非零,pipefail 保证 tail 不吞);test_annotations 用例数 < 8;全量回归低于基线(66 passed 2 skipped——回归输出行 passed 数 < 66 即失败)。</fails_when>
  </verify>
  <acceptance_criteria>
  - backend/annotations.py 存在且 `grep -c "def append_item\|def writeback\|def load\|def locate_quote\|def select_pending" backend/annotations.py` ≥ 5
  - `grep -n "discuss-round-{n}.annotations.json" backend/annotations.py` 命中(文件名模板常量)
  - backend/annotations.py 的 import 区无 fastapi/pydantic/claude 关键词(零框架依赖纯模块)
  - test_annotations.py 全绿且用例 ≥ 8(pytest 输出 "N passed",N ≥ 8)
  - 全量回归 66 passed 2 skipped 之上叠加新用例零失败
  </acceptance_criteria>
  <done>annotations.py 五函数可用;§6.2 八字段在落盘 JSON 中一字不差(aN-NN id 方案经测试证明);空形态/坏 JSON/回写命中/未命中保持 pending 全部有绿色用例;全量回归不降基线。</done>
</task>

<task type="auto" tdd="true">
  <name>Task 2: grammar.py 六条 §6.4 文法解析器(复用 state.py 常量)+ 正反例矩阵测试</name>
  <reversibility rating="costly">六条文法的解析语义(锚点取末一处、同号配对、strip 后全等)被 G3 按钮逻辑(Phase 3)与 process_round 回写(Wave 2)共同消费,语义变更会在两个消费方同时破坏判定。</reversibility>
  <files>backend/grammar.py, backend/tests/test_grammar.py</files>
  <read_first>
  - backend/state.py(1-60 行:常量 AUTH_MARKER_YES/AUTH_MARKER_NO/PASS_PREFIX、last_nonempty_line、is_complete_round——grammar 必须 import 复用这些,禁止重新定义字符串常量)
  - backend/tests/test_state.py(183-197 行:正反例断言形态 valid_round_text + write helper)
  - DESIGN.md §6.4 全节(222-233 行:四表定义 + PASS 锚点取末一处 + 裁决同号配对 + 判定式)
  - DESIGN.md §6.3(217-220 行:五件套与批注回应表)
  - .planning/phases/idi-02-g2/idi-02-PATTERNS.md(New Files #2:表格解析思路 + 六条覆盖清单 + _VERDICT_RE 正则形态)
  - .planning/phases/idi-02-g2/02-CONTEXT.md(D-P2-16/D-P2-17/D-P2-18/D-P2-19)
  </read_first>
  <behavior>
    - 维度表:合规样本(全 ✓)→ is_dimension_table_green True;含 ◐ 或 ✗ → False;状态列值不在 {✓,◐,✗} 的行(如"待定")→ 该行视为非绿(False)
    - 未决清单:全部已决 → is_pending_list_clear True;存在任一待决 → False
    - 授权申请标记:末非空行恰为 > 申请授权:是 → "yes";恰为 否 → "no";脏变体(前缀/后缀/末行后有空白行)→ None(非两串之一)
    - 批注回应表:parse_annotation_responses 返回 [{"id": "a1-01", "quote": "...", "response": "..."}];命中/未命中由调用方配对,解析器只负责提取;表内行 id 空白 strip 后仍空 → 跳过该行不抛
    - PASS 结论行:双结论行样本(第一处 > 核查结论:FIX(2 项)、第二处 > 核查结论:PASS)→ 取最后 PASS 为锚 → is_pass_conclusion True;仅 FIX → False;PASS 带括注 "> 核查结论:PASS(问题 N 项修复完毕)" → True(前缀匹配)
    - 裁决追加行:结论行之后 "> 待裁决:#1:" 未配对 → pending_verdicts 含 1;"> 裁决:#1:" 同号追加后配对消失;报告头部(结论行之前)出现待裁决样式行 → 不进配对空间;形态不符("> 待裁决 1:")→ 不是裁决行
    - 表格行按 | split 后各列 strip;标题不含关键词的二级标题下的表格不被误收
    </behavior>
  <action>新建 backend/grammar.py(零依赖纯文本函数模块;from backend.state import AUTH_MARKER_YES, AUTH_MARKER_NO, PASS_PREFIX 直接复用——D-P2-16 硬要求,grep 确认本模块无第二份 "> 申请授权" 字符串字面量)。六条公开能力(解析函数与判定函数分离,照 state.py 的 list_complete_rounds/is_complete_round 分离风格):

(1)表格共通解析 _extract_table(md_text, heading_keyword) -> list[list[str]]:扫 splitlines,定位 line.startswith("## ") 且 heading_keyword in 标题文本 的首个二级标题;其后连续 startswith("|") 的行按 "|" split → strip 各列 → 首个表头行丢弃;遇到非表格行(不以 | 开头)即终止该表。两次连续的二维标题定位(若同名标题多现,取第一处,DESIGN.md 每轮一份的结构假设)。

(2)维度表:parse_dimension_table(md_text) -> list[dict](列 维度/状态/说明 → {"dimension","status","note"});is_dimension_table_green(md_text) -> bool:无 ◐ 且无 ✗(空表 = 无行动 = 绿,判定写进 docstring 并给用例)。heading_keyword = "覆盖维度表"。

(3)未决清单:parse_pending_list(md_text) -> list[dict]({"number","question","status"});is_pending_list_clear(md_text) -> bool:无任何 status == "待决" 的行。heading_keyword = "未决问题清单"。

(4)授权申请标记:parse_auth_marker(md_text) -> str | None:last_nonempty_line(md_text)(state.py 复用)恰为 AUTH_MARKER_YES → "yes"、AUTH_MARKER_NO → "no"、其余 → None。本函数即 state.is_complete_round 的三分化语义重组(合法两态 + None),不复判 is_complete_round(后者继续留给 derive_state 用,两者共享底层常量)。

(5)批注回应表:parse_annotation_responses(md_text) -> list[dict]({"id","quote","response"};heading_keyword = "批注回应";id 列 strip 后空的行跳过);供 Wave 2 process_round 消费转 writeback 的 answers dict。

(6)PASS 结论行 + 裁决追加:_last_conclusion_index(md_text) -> int | None 找最后一处以 "> 核查结论:" 开头(strip 后 startswith)的行号;is_pass_conclusion(md_text) -> bool:该末锚点行 startswith(PASS_PREFIX)(等价于 state 的最新报告末行 PASS 判定但按"末一处锚点"语义重新表述,含双结论行样本);parse_verdict_lines(md_text) -> list[dict]:仅扫描末锚点行之后的行,匹配 _VERDICT_RE = re.compile(r"^>\s*(待裁决|裁决):#(\d+):") 的行 → {"kind": "待裁决"/"裁决", "number": int};unpaired_verdicts(md_text) -> list[int]:待裁决的 number 存在、同号裁决不存在 → 未配对;同号已配对不出现。

新建 backend/tests/test_grammar.py(照 test_state.py 正反例骨架,手造合规样本 helper——NOT 用本项目 docs/discuss-round-0~4 做输入,D-P2-19):样本 helper 造最小合规轮次文档(五件套:批注回应表 + 决策登记标题 + 维度表 + 未决清单 + 末行授权标记,逐字用 §6.4 表头 | 批注id | 原文摘录 | 回应 |、| 维度 | 状态 | 说明 |、| 编号 | 问题 | 状态 |)。用例矩阵(D-P2-17 逐项):维度表全绿/含◐/含✗/空表、清单清零/有待决/状态列脏值、标记 是/否/前缀/后缀/末行后空行、回应表正常提取/空 id 行跳过/空表、PASS 单结论/双结论取末一处/仅FIX/带括注、裁决 同号配对/未配对/锚前行不收/形态不符。合计 ≥ 16 用例(其中双结论行锚点取末一处、同号配对、未配对三类边界各至少 1 例,ROADMAP 成功判据 6 验收锚点)。先红后绿(先写测试见 NotImplementedError/ImportError,再实现转绿)。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_grammar.py -q 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1'</automated>
    <fails_when>任一 pytest 输出含 failed/error;test_grammar 用例数 < 16;双结论行锚点/同号配对/未配对三类边界用例任一缺失(grep -c "待裁决" test_grammar.py 为 0);全量回归 passed < 66。pydantic/fastapi import 进 grammar.py(grep 快速自检应为 0)。</fails_when>
  </verify>
  <acceptance_criteria>
  - backend/grammar.py 存在且含 grep -c "def parse_dimension_table\|def parse_pending_list\|def parse_auth_marker\|def parse_annotation_responses\|def is_pass_conclusion\|def unpaired_verdicts" 结果 ≥ 6
  - `grep -n "from backend.state import" backend/grammar.py` 命中且 grammar.py 内无第二处 "> 申请授权:" 字符串字面量定义(常量复用证明,D-P2-16)
  - test_grammar.py ≥ 16 用例全绿(含 testdouble 结论行锚点取末一处、同号裁决配对、未配对 verdict 三类具名边界用例)
  - test_grammar.py 无对本项目 docs/ 目录的任何读取(grep "discuss/或本项目仓库路径" 为 0——D-P2-19)
  - 全量回归零失败(66 基线 + 新增)
  </acceptance_criteria>
  <done>六条文法解析函数 + 判定函数全部就位并经正反例矩阵证明;边界三类(锚点取末一处/同号配对/未配对)有专属绿色用例;grammar.py 零重复常量、零第三方依赖、零本项目历史文档输入。</done>
</task>

<task type="auto">
  <name>Task 3: locate_quote 定位算法 + grammar×annotations 回写闭环纯函数验证</name>
  <reversibility rating="costly">quote/before 定位语义被前端高亮渲染(D-P2-4)与后端回写前的数据自检共用,D-P2-6 明确"前端与后端共用同一语义的配对函数"——语义改动需两侧同步。</reversibility>
  <files>backend/annotations.py, backend/tests/test_annotations.py, backend/tests/test_grammar.py</files>
  <read_first>
  - backend/annotations.py(Task 1 已交付的 load/writeback——本任务在其中有 locate_quote)
  - backend/grammar.py(Task 2 已交付的 parse_annotation_responses)
  - DESIGN.md §6.2(213 行:定位靠精确文本匹配 quote + before 辅助;冻结保证文本永不变化)
  - .planning/phases/idi-02-g2/02-CONTEXT.md(D-P2-4 / D-P2-6)
  </read_first>
  <behavior>
    - quote 全文唯一 → 返回该匹配起点(首字符 index)
    - quote 出现两次、其中一处前文以 before 结尾 → 返回那一处(多匹配 before 二次定位)
    - quote 出现两次、before 均不匹配任一前文 → 返回第一处(仍不唯一取第一)
    - quote 无匹配 → 返回 None(定位失败是合法返回,不是异常)
    - 闭环:手造上一轮 annotations(两条 pending)→ 手造新一轮文档(回应表只含第一条 id)→ parse_annotation_responses 转 answers dict → writeback 回写后:第一条 answered+answer 有值、第二条仍 pending
    </behavior>
  <action>(1)在 backend/annotations.py 实现 locate_quote(full_text: str, quote: str, before: str) -> int | None(若 Task 1 未一并交付):全文 str.find 精确匹配循环——收集所有匹配起点;若仅一处返回之;多处于优先匹配点前文(起点前取 max(0, start-len(before)) 起)以 before 为后缀的那一处;无 before 匹配取第一处(0 号起点);无匹配 None。纯标准库,容错:quote 为空串 → None(空 quote 无语义,防呆)。

(2)在 test_annotations.py 补 locate_quote 五用例(唯一命中/多命中 before 辅助/多命中无 before 匹配取第一/无命中 None/空串 None)。

(3)在 test_grammar.py(或 test_annotations.py,执行者按就近原则定)补闭环用例:构造 tmp 项目(docs/discuss-round-2.md 内含手造合规批注回应表,只含 id a1-01)→ 前置 docs/discuss-round-1.annotations.json(a1-01/a1-02 均 pending)→ parse_annotation_responses(round2_text) 提取 → 组 answers dict → annotations.writeback(project, 1, answers) → 断言 a1-01 status=answered 且 answer 非空、a1-02 status 保持 pending、返回值 == 1。此用例即 D-P2-12/D-P2-13 回写路径的纯函数级证明(Wave 2 process_round 只是把它挂到 done 后执行)。

写完后自查三条:locate_quote 不引入 re 模糊/容错匹配;闭环用例的两个文件名都走 ANNOTATIONS_TEMPLATE 模板;无新增第三方 import。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_annotations.py backend/tests/test_grammar.py -q 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1'</automated>
    <fails_when>任一 pytest 输出含 failed/error;locate_quote 五用例任一缺失或失败(输出 passed 数较 Task 2 完成时不再增加 ≥ 6);闭环用例失败(混合断言中 answered/pending 状态错乱);全量回归 passed 数下降。</fails_when>
  </verify>
  <acceptance_criteria>
  - `grep -n "def locate_quote" backend/annotations.py` 命中,函数含 before 后缀二次定位分支(源码可见 startswith 或切片比较逻辑)
  - 定位五用例 + 闭环一用例全部 pass(两文件合计用例数 ≥ Task 2 完成时的数量 + 6)
  - 闭环用例断言可核对:a1-01 answered、a1-02 pending、writeback 返回 1(test 输出零 failed)
  - locate_quote 实现无 edit distance/fuzzy 等复杂算法痕迹(import 区无 difflib/re 相关调用)
  </acceptance_criteria>
  <done>定位算法四分支 + 防呆分支都有绿色用例;grammar 回应表 → annotations 回写的纯函数闭环经测试证明(命中回写/未命中保持 pending);Wave 2 可以直接 import 这组契约。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| AI 产出的轮次文档 → grammar.py 解析 | AI 写出的 markdown 是不可信输入(格式可能不合规、字段可能缺失/脏——D-P2-13 半成品场景),解析器必须对任意文本给确定判定不崩 |
| 磁盘 JSON → annotations.py 读 | annotations.json 可能被外部改动或损坏(半写/非法 JSON),读路径必须给空形态不抛 |
| 测试样本 → 本项目历史文档 | 本项目自身 docs/ 是文法不合规历史样本,绝不能进解析正例(D-P2-19) |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi02-01 | Denial of Service | grammar.py 对畸形输入(AI 产出空文档/无表/脏表格行)抛异常拖垮 process_round | high | mitigate | 全部解析函数对空文本/无标题/空表格返回空列表或确定 False,None 不抛;正反例矩阵含脏数据用例;Task 2 behavior "空 id 行跳过"即此防线 |
| T-idi02-02 | Tampering | 坏 JSON 被静默当空形态后 writeback 覆写丢失旧批注 | medium | mitigate | JSONDecodeError 路径记 warning 日志(可追溯)+ 单测断言该路径;写盘用整文件重写(读-改-写),读失败即返回空形态不会走到写(writeback 对空 items 零命中、无覆盖损失面) |
| T-idi02-03 | Tampering | locate_quote 前后颠倒匹配顺序导致回收错位置 → 前端高亮错段 | medium | mitigate | 多匹配时 before 后缀定位分支有专属用例(多命中 before 辅助);仍不唯一取第一处的 tie-break 写进 docstring 与用例 |
| T-idi02-04 | Repudiation | annotations 无历史,回写覆盖旧 answer 无法审计 | low | accept | 单机单人本地工具;writeback 幂等语义(重跑同轮覆盖)是 §7.3 自愈承诺的一部分,不是审计面 |
| T-idi02-05 | Tampering | 历史文档(本项目 discuss-round-0~4)被当正例输入导致误判(如 round-1 清单状态列"待批注") | medium | mitigate | 测试样本全部手造合规文档(acceptance criteria 明确 grep 校验无本项目 docs/ 读入);文档级约束写入模块 docstring |

执行说明:本计划零 npm/pip/cargo 安装(纯标准库),无 T-{phase}-SC 供应链威胁项。
</threat_model>

<verification>
1. Task 1 automated:pytest test_annotations.py ≥ 8 用例 + 全量回归
2. Task 2 automated:pytest test_grammar.py ≥ 16 用例(含三类边界具名用例)+ 全量回归
3. Task 3 automated:两文件合计新增 ≥ 6 用例 + 闭环用例 + 全量回归
4. 全部任务的 verify 已含全量回归(66 基线不降);本计划无人检项(纯后端函数层,浏览器面在 Wave 3)
</verification>

<success_criteria>
- annotations.py / grammar.py 两个纯模块可被任何上层直接 import(零 FastAPI/AI 依赖)
- §6.2 八字段字面契约、aN-NN id 方案、writeback 命中/未命中语义全部有绿色用例
- 六条 §6.4 文法解析 + 两类 PASS/裁决边界(锚点取末一处、同号配对)全部有正反例证明
- state.py 常量被复用而非复制(grep 证明)
- 全量 pytest 回归:66 + 新增用例全绿
</success_criteria>

## Artifacts this phase produces(本计划新增符号清单)

- backend/annotations.py:ANNOTATIONS_TEMPLATE、annotations_path(project_path, round_n)、load(project_path, round_n) -> dict、append_item(project_path, round_n, *, quote, before, type, note, answer=None) -> dict、writeback(project_path, round_n, answers) -> int、select_pending(annotations) -> list[dict]、locate_quote(full_text, quote, before) -> int | None
- backend/grammar.py:parse_dimension_table(md_text)、is_dimension_table_green(md_text) -> bool、parse_pending_list(md_text)、is_pending_list_clear(md_text) -> bool、parse_auth_marker(md_text) -> str|None、"yes"/"no"/None 三态、parse_annotation_responses(md_text) -> list[dict]、is_pass_conclusion(md_text) -> bool、parse_verdict_lines(md_text)、unpaired_verdicts(md_text) -> list[int]、_extract_table(md_text, heading_keyword) 私有共通、_VERDICT_RE 常量
- backend/tests/test_annotations.py、backend/tests/test_grammar.py(新测试文件)

<output>
Create `.planning/phases/idi-02-g2/idi-02-01-SUMMARY.md` when done
</output>

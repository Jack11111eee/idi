---
phase: idi-01
plan: 02
type: execute
wave: 1
depends_on: []
files_modified:
  - backend/state.py
  - backend/transcript.py
  - backend/tests/__init__.py
  - backend/tests/test_state.py
  - backend/tests/test_transcript.py
autonomous: true
requirements:
  - FLOW-01

estimate:
  tokens: 60000
  raw_tokens: 60000
  tasks: 2
  confidence: low

must_haves:
  truths:
    - "对任意构造的目录形态(空目录/G1 前/轮次中/已授权/写稿中/自检中/使命完成),derive_state 返回 §7.4 八行表对应的那一行,自上而下首条命中"
    - "末行不是合规授权标记的轮次文档被判为半成品、视为不存在(当前轮取最大完整轮)"
    - "transcript.md 按 [user]/[ai] 起始行文法逐条解析出完整消息列表;追加一条消息后重读,新消息在列表末尾且既有消息不变"
    - "以上全部行为有 pytest 用例覆盖(含边界:多行消息体、半成品轮、check 文件末行前缀匹配)"
  artifacts:
    - path: "backend/state.py"
      provides: "derive_state(project_path) 纯函数 + 完整轮判据辅助函数"
      contains: "def derive_state"
    - path: "backend/transcript.py"
      provides: "transcript.md 的 parse(读取全量消息)与 append(追加一条)读写函数"
      contains: "def append_message"
    - path: "backend/tests/test_state.py"
      provides: "§7.4 八行表的构造目录用例"
    - path: "backend/tests/test_transcript.py"
      provides: "transcript 文法正反例用例"
  key_links:
    - from: "backend/state.py"
      to: "backend/transcript.py"
      via: "无直接调用——state 只看磁盘文件形态;transcript 是 FLOW-02(Plan 03)读取恢复的数据源,二者共同构成文件即状态脊柱"
      pattern: "derive_state"
---

## Phase Goal

**As a** 本工具的使用者,**I want to** 选中任何项目目录后界面自动呈现正确的流程状态(空目录 = 新讨论、有轮次 = 接续阶段),**so that** 我不需要任何手工"恢复"操作——状态永远从磁盘现状推导出来。

<objective>
实现工具的脊柱(D-P1-11,D-19 文件即状态):derive_state() 纯函数(DESIGN.md §7.4 八行推导表,含完整轮判据)与 transcript.md 文法读写(§6.1,`[user]`/`[ai]` 起始行,per D-P1-10——追加式落盘由后端在用户发送/AI 回复时执行,文法 = 起始行独占一行 + 任意多行消息体)。这两个纯后端模块零框架依赖、可独立于 Wave 1 其他计划并行开发,由 pytest 覆盖全部行为分支。

Purpose: D-P1-11 明确本阶段就要全表实现——Phase 2/3 的所有按钮逻辑都叠在它上面;transcript 文法是会话恢复(FLOW-02,Plan 03)的唯一依据。
Output: backend/state.py、backend/transcript.py + 配套测试,全部纯函数式,不碰 FastAPI 层。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/phases/idi-01-1-2/01-CONTEXT.md

DESIGN.md 权威依据(逐行实现,不得简化):
- §7.4 阶段推导与完成判定表(8 行,自上而下首条命中;行间条件已互斥化)
- §7.3 完整轮判据:最新轮次文档末行不是合规 `> 申请授权:是|否` 标记即判半成品、视为不存在
- §6.4 授权申请标记文法:文档最后一个非空行恰为 `> 申请授权:是` 或 `> 申请授权:否`
- §6.1 transcript.md 文法:每条消息 = 起始行 [user] 或 [ai](独占一行)+ 任意多行消息体,以下一条起始行或文件末尾为界
- PASS 结论行前缀(`> 核查结论:PASS 开头`,报告最后一行以之开头即使命完成)

工程约定:pytest 已由 Plan 01 引入依赖环境(.venv);本计划不新增任何第三方依赖(纯 pathlib + 标准库)。
</context>

<tasks>

<task type="auto" tdd="true">
  <name>Task 1: derive_state()——§7.4 八行推导表 + 完整轮判据</name>
  <reversibility rating="costly">返回结构(state 字段、current_round、可推阶段上限)被 Phase 2/3 全部按钮逻辑消费,改形状需要协调多调用点。</reversibility>
  <behavior>
    - 用例 1(行 1):空目录(无 docs/)→ state="phase1_new"
    - 用例 2(行 2):有 docs/、无完整轮、无 DESIGN.md、无 AUTHORIZATION.md(含"G1 定稿前旧轮残留"形态:仅存在末行不合格的轮次文档)→ state="phase12_in_progress"
    - 用例 3(行 3):有 discuss-round-1..3 且 round-3 末行合规、round-4 末行不合规(半成品)、无 DESIGN.md、无 AUTHORIZATION.md → state="phase3" 且 current_round=3
    - 用例 4(行 4):有 AUTHORIZATION.md、无 DESIGN.md、无 DESIGN-check 文件(有残留 DESIGN.md.tmp 不影响判定)→ state="phase4"
    - 用例 5(行 5):有 DESIGN.md、无 DESIGN-check 文件 → state="phase5_awaiting_tier"
    - 用例 6(行 6):有 DESIGN.md 与 check-1(末行非 PASS,含"报告已落盘但无结论行"形态)、check-2 不存在 → state="phase5_checking" 且 current_check=1
    - 用例 7(行 7):最新 DESIGN-check 末行以 `> 核查结论:PASS` 开头 → state="mission_complete"
    - 用例 8(边界):allAbsent 时(空目录)与行 2 中"discuss-round 全不存在"等价;圆整:round 编号非连续(有 1、3 无 2)时最大完整轮取实际存在的最大完整编号
    - 用例 9(边界):末行授权标记后随空行/行尾空白(合规标记是"最后一个非空行"语义)
    - 用例 10(边界):多个 check 文件取最大编号为最新;check 末行前缀匹配用 startswith 而非全等,尾注如 (问题 3 项修复完毕) 仍算 PASS
  </behavior>
  <files>backend/state.py, backend/tests/__init__.py, backend/tests/test_state.py</files>
  <action>在 backend/state.py 实现 derive_state(project_path: Path) -> dict 纯函数。先建 backend/tests/__init__.py(空文件)。derive_state 返回结构自洽且本阶段内固定:{state: str, current_round: int|None, current_check: int|None}。实现顺序:

(1)辅助函数 is_valid_auth_marker_line(text) / last_nonempty_line(md_text):取文档最后一个非空行;"最后一个非空行"按行 strip 后取末一个非空。

(2)is_complete_round(md_text) -> bool:文档存在且最后一个非空行在 strip 后恰等于 `> 申请授权:是` 或 `> 申请授权:否`(§6.4 授权申请标记;恰为——前缀不算,后缀不算,exact match after strip)。

(3)list_complete_rounds(docs_dir) -> list[int]:遍历 docs/ 下文件名匹配 discuss-round-{N}.md 形态(order:用正则 r'^discuss-round-(\d+)\.md$' 提取编号),对每个读文本判 is_complete_round,返回完整轮编号列表(升序)。

(4)max_check_number(docs_dir):同法匹配 DESIGN-check-{N}.md,返回最大编号(不存在返回 None);latest_check_content(docs_dir) 返回最新编号报告的文本。

(5)derive_state 主函数按 §7.4 八行表**自上而下**逐行判(行间条件已互斥化——严格照抄表条件,不要自行改写条件组合):行 1 无 docs/ → phase1_new;行 2 有 docs/ 且完整轮列表为空且无 DESIGN.md 且无 AUTHORIZATION.md → phase12_in_progress;行 3 完整轮列表非空且无 DESIGN.md 且无 AUTHORIZATION.md → phase3(current_round = max(完整轮列表));行 4 有 AUTHORIZATION.md 且无 DESIGN.md 且无 DESIGN-check 文件 → phase4(注意:DESIGN.md.tmp 残留不影响本行,DESIGN.md 半成品不可能存在——tmp 改名是原子操作);行 5 有 DESIGN.md 且无 DESIGN-check 文件 → phase5_awaiting_tier;行 6 有 DESIGN.md 且有 DESIGN-check 文件且最新一份末行非以 `> 核查结论:PASS` 开头 → phase5_checking(current_check = max 编号);行 7 最新 DESIGN-check 末行以 `> 核查结论:PASS` 开头 → mission_complete。current_round/current_check 只在 phase3/phase5_checking 下有值,其余为 None。先写 test_state.py 的 10 个用例(上面 behavior 列表即断言依据,用 pytest 的 tmp_path 构造目录),先跑红再实现转绿。</action>
  <verify>
    <automated>bash -c 'cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_state.py -q 2>&1 | tail -2'</automated>
  </verify>
  <fails_when>pytest 输出含 failed 或 error,或用例数 < 10(collected 少于预期)。</fails_when>
  <done>test_state.py 10 用例全绿;derive_state 对八行表每行各有一个命中用例。已 commit。</done>
</task>

<task type="auto" tdd="true">
  <name>Task 2: transcript.md 文法——parse 与 append</name>
  <reversibility rating="costly">文法写入用户真实项目目录、G1 后永久保留,变更即数据迁移。</reversibility>
  <behavior>
    - 用例 1(基础解析):三段消息 [user]/[ai]/[user],各含单行体 → parse 返回 3 条 {role, content}
    - 用例 2(多行体):某条消息体含 3 段落(含空行)→ 内容原样保留(首尾 strip,内部空行不动)
    - 用例 3(追加):对 2 条既有消息 append(role=ai, content=多行文)后 parse 返回 3 条,前 2 条不变,末条 role/content 精确
    - 用例 4(空文件):parse(不存在文件)返回 [];parse(空文件)返回 []
    - 用例 5(追加建文件):对不存在的 transcript.md append → 文件被创建且内容以起始行开头
    - 用例 6(无尾换行容错):既有文件末行无换行符时 append 仍产出正确结构(先补换行再追加)
  </behavior>
  <files>backend/transcript.py, backend/tests/test_transcript.py</files>
  <action>在 backend/transcript.py 实现三个函数,全部纯 pathlib 无状态(per D-P1-10:落盘动作由后端在用户发送/AI 事件回落时执行,本模块即该落地件):(1)parse_transcript(path: Path) -> list[dict],每条 {role: "user"|"ai", content: str};按行扫描,遇到恰等于 [user] 或 [ai] 的整行(strip 后比较)即开新条目,其余行累积为当前条目体,直到下一起始行或文件末尾;条目体首尾 strip。起始行之前若出现非空内容(脏头,正常不出现)丢弃并打 warning 日志。(2)append_message(path: Path, role: str, content: str):以 a 模式打开(不存在会建),写入一行 [role] 换行,再写 content 尾换行(role 只接受 user/ai,别的抛 ValueError);若文件已存在且非空且末字符非换行,先补一个换行再追加。(3)transcript_exists(path) -> bool。先写 test_transcript.py 六个用例(behavior 即断言依据,tmp_path 起目录),跑红转绿。</action>
  <verify>
    <automated>bash -c 'cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_transcript.py -q 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/test_state.py -q 2>&1 | tail -1'</automated>
  </verify>
  <fails_when>任一 pytest 输出含 failed 或 error,用例数 < 6(transcript)/< 10(state)。</fails_when>
  <done>两套测试全绿;transcript 文法与 §6.1 逐字一致(机器可解析、多行体不需转义);append 特性幂等可重入(每次调用只追加新条目)。已 commit。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 用户项目目录磁盘 → derive_state/parse 输入 | 磁盘文件内容不受信:畸形文件名、超长行、非 UTF-8 内容、半成品残留,函数必须不崩、给出确定判定 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi02-01 | Denial of Service | 畸形/超大轮次文档使 parse OOM 或死循环 | medium | mitigate | 逐行读(不整读),正则有界([0-9]+ 编号),utf-8 errors="replace" |
| T-idi02-02 | Tampering | 畸形文件伪装完整轮(如标记行后藏命令) | low | accept | 推导只读不执行;标记行 exact-match 判定,无注入面 |
</threat_model>

<verification>
1. pytest backend/tests/test_state.py:八行表全覆盖(10 用例)
2. pytest backend/tests/test_transcript.py:文法正反例(6 用例)
3. 两套同跑无回归
</verification>

<success_criteria>
- derive_state 对 §7.4 表每一行各有一个通过的构造用例(含半成品轮、非连续编号、tmp 残留三个边界)
- transcript parse/append 完全按 §6.1 文法,多行体保留
- 两个模块零第三方依赖、零全局状态,其他计划可直接导入
</success_criteria>

<output>
Create `.planning/phases/idi-01-1-2/idi-01-02-SUMMARY.md` when done
</output>

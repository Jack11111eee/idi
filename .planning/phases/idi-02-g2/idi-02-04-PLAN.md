---
phase: idi-02
plan: 04
type: execute
wave: 4
depends_on: ["idi-02-02", "idi-02-03"]
files_modified:
  - backend/tests/test_e2e_rounds.py
  - pytest.ini
  - .planning/phases/idi-02-g2/idi-02-04-SUMMARY.md
autonomous: false
requirements:
  - FLOW-04
  - FLOW-07
  - UI-01
  - UI-02
  - UI-04
  - DATA-01

estimate:
  tokens: 70000
  raw_tokens: 70000
  tasks: 2
  confidence: low

must_haves:
  truths:
    - "IDI_E2E=1 门控的真实 CLI 端到端用例:造盘 phase3 项目(轮 1 + 两条批注)→ answer_plain 真调用数秒返回非空 answer 且落盘 plain 条目 → process_round 真调用产出 discuss-round-2.md(末行合规授权标记)→ 上一轮 annotations 经后端回应表解析回写(a1-01 answered/answer 非空) ← FLOW-04 / UI-02 / DATA-01 全链真验证"
    - "半成品真实验证:AI 产出不合规新文档的造盘模拟已由 idi-02-02 用例覆盖;本计划补 process_round 失败重跑的真路径断言依赖同一自愈语义(不新增分支) ← FLOW-04 boundary(D-P2-13)"
    - "全量测试套件(66 基线 + Wave 1-3 新增全部用例)绿;IDI_E2E 未设时 slow 用例 skip(常轨跑不依赖真 CLI)← Phase 1 pytest.ini slow marker 先例"
    - "generate-rounds 全量 docstring 式 UAT 名单照 idi-02-03 的六点人检清单在浏览器复走一遍(真 CLI),结果记入 SUMMARY(六点逐项打钩)← ROADMAP 成功判据 1-5 的浏览器面验收"
    - "目录结构按 §6.1 落盘齐全:transcript/draft(若有)/轮次文档/annotations.json/check-list 清点(造盘项目里全套可见;本工具自身仓库不适用——其为运行时产物) ← DATA-01 / ROADMAP 成功判据 7"
  artifacts:
    - path: "backend/tests/test_e2e_rounds.py"
      provides: "真实 CLI 门控端到端用例:answer_plain 秒级回 + process_round 出新轮回写(两条 @slow 用例)"
    - path: "pytest.ini(扩展)"
      provides: "复用既有 slow marker 注册(Phase 1 已建,如需新增 category 文案不改语义)"
  key_links:
    - from: "backend/tests/test_e2e_rounds.py"
      to: "backend/session.py process_round / answer_plain"
      via: "真实 CLI 调用链验证 Fake 级测试覆盖不到的最终一环(超时 deadline 300s)"
      pattern: "IDI_E2E"
  prohibitions:
    - statement: "E2E 用例不得在无 IDI_E2E 环境变量时真实调用 CLI(常轨回归必须可跑、秒级完成)"
      status: unverified
      flagged: true
    - statement: "不得为了通过 E2E 修改 process_round 的回写语义或 prompt 模板(发现 AI 不按文法产出时,先修 prompt 的文法模板贴入部分,不改解析/回写逻辑——D-P2-18 不修补 AI 产物,靠重跑覆盖)"
      status: unverified
      flagged: true
    - statement: "人检 UAT 名单不得以截图代替逐项文字确认记录(SUMMARY 六点逐项打钩)"
      status: unverified
      flagged: true
---

## Phase Goal

**As a** 即将进入 Phase 3 的用户,**I want to** 在真实环境里完整走一遍「划词批注 → 处理本轮批注 → 下一轮产生 → 上一轮冻结回写」的轮次循环,**so that** Phase 2 的全部 6 个 REQ(7 条成功判据)在真实 CLI 与真实浏览器里被最终证明,Phase 3 可以放心叠加。

<objective>
Phase 2 收口验证计划:新建 backend/tests/test_e2e_rounds.py 两条 IDI_E2E 门控 @slow 用例(真实 CLI 跑 answer_plain 与 process_round 全链,断言秒级回答、新轮产出、回应表回写、冻结数据只读);补跑全量回归确认零退化; browser 人检 UAT 六点清单复走并记录。本计划不写产品代码——只写测试与验收产物;发现实现缺陷时按缺陷所在回 Wave 2/3 的文件修复(修复动作记 SUMMARY,commit 在本计划分支)。

Purpose: ROADMAP 的 7 条成功判据需要一条真实链路证据(Fake 级测试已证明逻辑,真实 AI 遵守文法的能力与秒级响应只有在真调用里可证——D-P2-18 的「模板逐字遵守」最终检验)。
Output: 两条 slow E2E 用例绿 + 全量回归绿 + 人检 UAT 六点记录 + Phase 2 收口 SUMMARY。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/phases/idi-02-g2/02-CONTEXT.md
@.planning/phases/idi-02-g2/idi-02-01-SUMMARY.md
@.planning/phases/idi-02-g2/idi-02-02-SUMMARY.md
@.planning/phases/idi-02-g2/idi-02-03-SUMMARY.md

依赖接口(来自 Wave 1-3,全部直接消费):
- backend/session.py:enter_project / answer_plain(round_n, quote, before, question) / process_round() / busy()
- backend/annotations.py:load / append_item / writeback
- backend/state.py:derive_state(phase3 + current_round)
- frontend/app.js + index.html + style.css(六点人检对象)
- pytest.ini 既有 slow marker 注册(IDI_E2E 门控)与 test_e2e_smoke.py 的门控写法(9-21 行 sys.path + skip 判定形态)

DESIGN.md 权威依据:
- §3.4(轻量调用秒级)、§3.5(冻结)、§4.4(G2)、§5.1(无状态重跑可复现)、§5.4(AI 写 docs/ 放行)、§6.1(目录结构齐全——判据 7)、§6.2(回写职责)、§6.4(文法——AI 真实遵守度的检验对象)、§7.3(重跑覆盖)

分支纪律(per 仓库 CLAUDE.md §5):执行者从当前分支 HEAD 切出 phase-02/idi-02-04 工作分支,plan 完成后合回原分支。本计划若需修复 Wave 2/3 缺陷,修复 commit 也在本分支(单一分支单 plan 原则,缺陷归属记 SUMMARY)。

前置条件(执行本计划时):claude CLI 已装并已登录(真实调用必需;未登录则向用户报告并暂停——人检 UAT 前置)。
</context>

<tasks>

<task type="auto">
  <name>Task 1: E2E 真调用用例——answer_plain 秒回 + process_round 出新轮回写(IDI_E2E 门控)</name>
  <reversibility rating="cheap">测试文件独立新增,零产品代码改动(发现缺陷时的修复属受控回写,不破契约)。</reversibility>
  <files>backend/tests/test_e2e_rounds.py, pytest.ini</files>
  <read_first>
  - backend/tests/test_e2e_smoke.py(1-94 行:IDI_E2E 门控写法、sys.path 头、slow marker、轮询 deadline 模式)
  - backend/session.py(answer_plain / process_round 的 RuntimeError 语义;enter_project)
  - backend/state.py(derive_state 形状;is_complete_round 消费用例)
  - backend/annotations.py(load / writeback)
  - backend/prompts.py(build_round_prompt——理解 prompt 对 AI 产出文法的约束面,测试断言按 §6.4 文法查产物)
  - DESIGN.md §3.4(秒级)、§6.3(批注回应表一一对应)、§6.4(标记行/表头文法——断言对象)、§7.3(重跑覆盖)
  </read_first>
  <behavior>
    - 用例 1 test_answer_plain_real_cli:mktemp 项目造盘 phase3(docs/discuss-round-1.md 末行合规 + 一条 quote 文本已知)→ enter_project → answer_plain(1, quote=已知段, before, question="这段讲什么?")→ 断言:返回条目 type=plain、status=answered、answer 非空;annotations.json 落盘该条目;耗时 < 60s(秒级宽限;超时即失败)
    - 用例 2 test_process_round_real_cli:同一造盘模式前置两条 comment 批注(pending)→ process_round() 返回 True → 轮询 wait_idle(deadline 300s)→ 断言:discuss-round-2.md 存在且末行恰为 > 申请授权:是 或 否(is_complete_round);文档含三表头文法(批注回应表/维度表或清单——按 §6.4 可解析:grammar.parse_annotation_responses(新文档) 非空 且 批注id 含 a1-01);process_round 收流后 a1-01 的 status=answered、answer 非空(后端回写真实发生);derive_state 前进 current_round == 2;上一轮(r1)annotations 再读不丢 items(只读保留)
    - 用例 3(防退化断言,非 slow):全量套件在本文件加入后常轨(IDI_E2E 未设)跑,suite 全绿且新文件两条用例 skipped
    </behavior>
  <action>(1)新建 backend/tests/test_e2e_rounds.py(照 test_e2e_smoke.py 头形态:sys.path 注入 + `pytestmark = [pytest.mark.slow]`(或函数级装饰器,照先例形态) + `if not os.environ.get("IDI_E2E"): pytest.skip(...)` 门控):两个测试函数如 behavior 所列。造盘 helper 写 phase3 目录(docs/discuss-round-1.md 正文含一句可引用的中文句子如「这一段是可以被划选的说明文字」。annotations 手写 JSON 两条 pending a1-01/a1-02(quote = 该句子的前半或全句,before 取空前缀)。用例 1 在造盘后直接调 session(进入项目 → answer_plain),计时用 time.monotonic 差值断言 < 60(命题「数秒内」的保守上限——真实观察值记 SUMMARY);断言 answer 非空且落盘条目字段齐全(type=plain/id/quote/before/created_at 全在)。用例 2 前置 session._set_caller_for_tests 不用(真路线)——直接 process_round() 后 wait_idle(sess)(照 test_session 的 wait_idle helper 形态复制本文件或 import,超时 300s);断言链:新文档存在 → 读文本 → is_complete_round(§7.3 标记)= True → grammar.parse_annotation_responses(文本)提取的 id 列表含 a1-01 → annotations.load(1) 后 a1-01 status=answered/answer 非空、a1-02 视回应表实际覆盖断言(表中含则 answered,不含则 pending——测试对 AI 产出的最小只断言 a1-01 被 prompt 的「逐条回应全部实质批注」覆盖,若 AI 漏答记为产物缺陷→ 按 failures 分支处理:测试失败即真实发现,报告而非放宽断言)→ derive_state(project) 的 current_round == 2。**每条断言失败时输出中文字定位说明(便于修复定位)。**

(2)pytest.ini:确认 slow marker 已注册(Phase 1 已建,通常零改动;若需加 description 前缀仅作文案补,不改语义——本 files 列它作为「可能不动」项,执行者确认后写 SUMMARY「pytest.ini 未动」或补丁差异)。

(3)执行本任务时把两条 slow 用例真正跑一遍:IDI_E2E=1 .venv/bin/python -m pytest backend/tests/test_e2e_rounds.py -q -m slow(需 CLI 已登录;发现真实缺陷——AI 不按文法、回写漏 id、秒级超时——按缺陷所在文件回修:prompt 模板贴字不全 → 补 prompts._ROUND_INSTRUCTIONS 的正例;解析边界 → 修 grammar;UI 不在范围。修复 commit 留在本计划分支并在 SUMMARY 记录缺陷→修复对照)。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && IDI_E2E=1 .venv/bin/python -m pytest backend/tests/test_e2e_rounds.py -q -m slow 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1'</automated>
    <fails_when>slow 用例 failed/error(真实链路断:CLI 登录失效/秒级超时 >60s/AI 产出不合规/回写漏 id——任何一条都是真发现,不是放宽对象);IDI_E2E=1 下两条用例出现 skipped(门控写反或条件错误);全量回归(常轨)含 failed;总用例数较 Wave 3 完成时下降。</fails_when>
  </verify>
  <acceptance_criteria>
  - backend/tests/test_e2e_rounds.py 存在,含 grep -c "IDI_E2E" ≥ 1(命中行数 ≥ 1)且 grep -n "def test_answer_plain_real_cli\|def test_process_round_real_cli" 恰命中两行定义
  - IDI_E2E=1 下两用例 passed(非 skipped 非 failed);输出尾行 "2 passed"
  - 常轨全量回归全绿,新文件两用例在无 IDI_E2E 时 skipped(tail 行含 skipped 计数)
  - 用例 2 的断言链含 current_round == 2 与 a1-01 answered(grep test 文件可见断言文本)
  - pytest.ini 的 slow marker 语义未改动(仅允许 description 文案差异)
  </acceptance_criteria>
  <done>真实 CLI 链路证明:大白话秒级回 + 落盘 plain;process_round 真实产出含文法合规回应表的新轮文档,后端回写命中,推导态前进,上一轮 annotations 只读保留;发现的缺陷已定位修复并记录。</done>
</task>

<task type="auto">
  <name>Task 2: Phase 2 收口——全量回归 + 浏览器 UAT 六点人检 + 目录结构清点 + SUMMARY</name>
  <reversibility rating="cheap">验收与文档产物;无产品代码。</reversibility>
  <files>backend/tests/test_e2e_rounds.py, .planning/phases/idi-02-g2/idi-02-04-SUMMARY.md</files>
  <read_first>
  - .planning/phases/idi-02-g2/idi-02-03-SUMMARY.md(Wave 3 人检 checklist 六点——本任务复走对象)
  - .planning/ROADMAP.md(Phase 2 的 7 条成功判据——逐条对账)
  - DESIGN.md §6.1(判据 7 的目录结构清单:transcript/draft/轮次/annotations/brainstorm/check 命名)
  - backend/tests/ 全目录(清单核对:各测试文件的 REQ 归属)
  </read_first>
  <behavior>
    - 全量回归一次通过(所有新增文件 + Phase 1 全部)且零 warning 量级恶化
    - 浏览器 UAT 六点(idi-02-03 定义)逐点在真实环境复走并以文字记录每点结果
    - ROADMAP 7 条成功判据逐条核对并标注证据来源(哪条测试/哪个人检点)
    - 造盘项目的 docs/ 目录结构按 §6.1 清点(discuss-round-N.md / discuss-round-N.annotations.json / transcript.md 若阶段 1-2 起步 / check 报告注记 Phase 3 无)
    </behavior>
  <action>(1)跑全量:.venv/bin/python -m pytest backend/tests/ -q,记录最终用例数(基线 66+2skip + Wave 1-3 全部新增 + 本计划 2 slow skipped 常轨)。

(2)人检 UAT 交接(执行者能跑则跑,不能跑则写清操作步骤交用户):bash run.sh 启动 → 浏览器输入造盘的 phase3 项目目录(Task 1 用例 2 造过的目录可复用)→ 六点逐项走:①划选轮次文档中一段文字松开鼠标 → 弹出两菜单项(「批注」「用大白话讲这段」)②点批注写 note → 侧栏出现该条(quote 摘录+note+「待处理」)③点大白话 → 数秒出灰斜体即时答(记录实测秒数)④被批注段落高亮(mark 背景)⑤点「处理本轮批注」→ 工作面板直播 AI 的读/写事件 → done 后切到新轮、切回旧轮看灰化与批注「已回应」+ AI 回答展示 ⑥旧轮划词不弹菜单。每个点一行结论(通过/问题+描述)记入 SUMMARY 的 UAT 表。

(3)7 条成功判据对账表(写入 SUMMARY):每条判据一行 ← 责任 REQ + 证据(测试函数名 / 冒烟对账输出 / 人检点编号),7 条全部找到证据才算收口;判据 7(§6.1 目录结构)以造盘项目 docs/ 实际文件清单为证据(ls 输出粘贴)。

(4)SUMMARY 按模板产出:REQ 覆盖(FLOW-04/FLOW-07/UI-01/UI-02/UI-04/DATA-01 六条全勾)+ 7 判据对账 + UAT 六点 + 实测数据(大白话秒数、E2E 耗时)+ 缺陷修复对照(若有)。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1 && grep -c "成功判据\|UAT" .planning/phases/idi-02-g2/idi-02-04-SUMMARY.md 2>/dev/null; echo "summary-check-done"'</automated>
    <fails_when>全量回归含 failed/error;SUMMARY 文件不存在(grep -c 无输出路径错误时输出 0);SUMMARY 中无判据对账章节(grep 计数为 0——收口表缺失);无 summary-check-done。</fails_when>
  </verify>
  <acceptance_criteria>
  - 全量回归输出 "N passed, 2 skipped"(N ≥ 66 + 所有 Wave 新增;无 failed)
  - .planning/phases/idi-02-g2/idi-02-04-SUMMARY.md 存在且含 7 条判据对账表与 UAT 六点结果表(grep "判据" 命中 ≥ 1、"UAT" 命中 ≥ 1)
  - 六条 REQ(FLOW-04/07、UI-01/02/04、DATA-01)在 SUMMARY 中逐条标注完成证据
  - 判据 7 目录结构以真实 ls 输出为证据(SUMMARY 内含 docs/ 文件名清单)
  </acceptance_criteria>
  <done>Phase 2 六 REQ 收口:7 条判据全部有证据(测试/冒烟/人检);全量回归绿;SUMMARY 完整;Phase 3 可启动。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 真实 CLI 进程 → 造盘临时项目 | E2E 期间 AI 在 mktemp 目录上真跑(权限门 docs/ 放行面);测试产物不碰本工具仓库 |
| 测试注入的 prompt → CLI | 可复现重跑(§5.1)——超时/失败都走既有 error 路径 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi02-17 | Denial of Service | E2E 用例对真实 AI 依赖超时挂死(网络/登录失效) | medium | mitigate | 两处 deadline 轮询(60s/300s 超时即 fail 并输出已等待时长;test_e2e_smoke 先例);wait_idle 收流兜底 |
| T-idi02-18 | Tampering | E2E 误用本工具自身仓库作为项目目录(写入污染) | high | mitigate | 全部造盘走 mktemp -d / tmp_path;测试断言路径以 /tmp 前缀为界(固定 helper 从 tmp_path 参数派生,不硬编码仓库路径);grep 测试文件无本仓库绝对路径字符串 |
| T-idi02-19 | Repudiation | E2E 通过但人检未做即划勾 | medium | mitigate | SUMMARY 模板把 UAT 六点列为显式表格逐点记录(空表 = 未完成,不视为收口);autonomous: false 本计划保留人检面 |

执行说明:纯测试/文档计划,零包安装,无供应链项。涉及真实 CLI 的检查(慢用例)已由 IDI_E2E 门控在常轨回归中排除。
</threat_model>

<verification>
1. Task 1 automated:IDI_E2E=1 slow 两条真调用用例 + 全量回归
2. Task 2 automated:全量回归 + SUMMARY 章节存在性检查
3. 人检:浏览器六点 UAT(详 Task 2;执行者能跑则跑,否则交付步骤清单给用户;结果必须落 SUMMARY 才算收口)
4. 收口门槛:ROADMAP 7 判据对账表全证据 + 六 REQ 全勾 → Phase 2 完成,可启动 Phase 3 规划
</verification>

<success_criteria>
- 真实 CLI:大白话秒级回(记录实测值)+ process_round 产文法合规新轮 + 回写 a1-01 answered + current_round 前进
- 全量回归全绿(66 + 全部新增)
- 人检 UAT 六点记录完整
- 7 条 ROADMAP 判据对账表填满证据
- SUMMARY 产出且 REQ 六条全勾
</success_criteria>

## Artifacts this phase produces(本计划新增符号清单)

- backend/tests/test_e2e_rounds.py:test_answer_plain_real_cli、test_process_round_real_cli、mktemp 造盘 helper(write_phase3_project)
- .planning/phases/idi-02-g2/idi-02-04-SUMMARY.md(7 判据对账表 + UAT 六点表 + 实测数据)
- pytest.ini:预期零改动(确认记录)

<output>
Create `.planning/phases/idi-02-g2/idi-02-04-SUMMARY.md` when done
</output>

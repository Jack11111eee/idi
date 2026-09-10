---
phase: idi-03
plan: 05
type: execute
wave: 5
depends_on: ["idi-03-04"]
files_modified:
  - backend/tests/test_e2e_g3.py
  - pytest.ini
  - .planning/phases/idi-03-g3/idi-03-05-SUMMARY.md
autonomous: false
requirements:
  - FLOW-05
  - DATA-02
  - DATA-03
  - DATA-04

estimate:
  tokens: 75000
  raw_tokens: 75000
  tasks: 2
  confidence: low

must_haves:
  truths:
    - "IDI_E2E=1 门控的真实 CLI 端到端用例(照 idi-02-04 / test_e2e_rounds.py 形态G3→PASS 全链):造盘 phase3 四查合规项目 → authorize()(真调用前半段纯后端)→ 撰写链真调用 start_writing → AI 产出 DESIGN.md.tmp、后端原子改名 DESIGN.md、derive_state → phase5_awaiting_tier(AI 文档含维度覆盖与对齐结论;真实耗时记 SUMMARY)← FLOW-05 / DATA-02 / ROADMAP 判据 2"
    - "自检链真调用:POST tier(宽松)→ start_check 真调用产出 docs/DESIGN-check-1.md(头部档位行 + 问题分级表合规 + 结论行)→ 宽松档修复者追加 PASS(或残余收口)→ derive_state = mission_complete;全程 SSE 事件流照旧 ← DATA-04 / ROADMAP 判据 3、4"
    - "修复者抛问/裁决链若真 AI 未触发:纯函数级已覆盖(idi-03-02 抛问截存用例);E2E 报告如实记录真调用覆盖的分支(不冒充;未触发分支记 SUMMARY「真调用未覆盖,由 Fake 级覆盖」——照 idi-02-04 路线覆盖度诚实记录先例)← D-P3-30 / 路由覆盖度诚实原则"
    - "全量测试套件(143 基线 + Wave 1-4 全部新增)在常轨(IDI_E2E 未设)全绿且新文件用例 skip ← D-P3-30"
    - "浏览器人检 UAT 清单(五判据逐条)由用户真机复走,结果逐项记入 SUMMARY(空表 = 未收口,不视为完成)← ROADMAP 5 条成功判据的浏览器面验收"
    - "ROADMAP 五条成功判据逐条对账(证据 = 测试函数名 / 冒烟 sentinel / 人检点编号),全部找到证据才算 Phase 3 收口 → milestone 归档就绪(此后 /gsd-complete-milestone)← Phase 收口门"
  artifacts:
    - path: "backend/tests/test_e2e_g3.py"
      provides: "真实 CLI 门控端到端用例:authorize→write DESIGN(tmp 改名)→tier→check→PASS→mission_complete 全链(@slow 用例 + IDI_E2E 门控)"
    - path: "pytest.ini(零改动确认)"
      provides: "复用既有 slow marker 注册(缺则确认记录,不注入新语义)"
    - path: ".planning/phases/idi-03-g3/idi-03-05-SUMMARY.md"
      provides: "五判据对账表 + REQ 四条勾稽 + UAT 人检清单 + 实测耗时 + 真调用覆盖度诚实记录 + milestone 收口声明"
  key_links:
    - from: "backend/tests/test_e2e_g3.py"
      to: "backend/session.py 全六函数 + backend/g3.py"
      via: "真实 CLI 调用链验证 Fake 级与冒烟覆盖不到的最终一环(授权后真撰写、真核查报告文法、真 PASS 收口)"
      pattern: "IDI_E2E"
  prohibitions:
    - statement: "E2E 用例不得在无 IDI_E2E 环境变量时真实调用 CLI(常轨回归必须可秒级完成)"
      status: unverified
      flagged: true
    - statement: "不得为了通过 E2E 修改已锁定语义(判定式/解析文法/权限矩阵);发现 AI 产物不合规时修 prompt 的文法贴入部分,不改解析器或回写逻辑(D-P2-18/D-13 延续——AI 产物不修补,靠重跑覆盖)"
      status: unverified
      flagged: true
    - statement: "人检 UAT 不得以截图代替逐项文字确认记录(SUMMARY 清单逐项结论);不得在判据无证据时勾收口"
      status: unverified
      flagged: true
    - statement: "不引入新测试基建(不新增 fixture/插件;真路线凭 denier 线程等照 test_e2e_rounds.py 既有形态复用,D-P3-30)"
      status: unverified
      flagged: true
---

## Phase Goal

**As a** 走完整个流程的用户,**I want to** 在真实 CLI 与真实浏览器里完整走一遍「四查合规 → 确认授权 → AI 撰写 → 原子落盘 → 选档 → 自检循环 → 使命完成 → 只读归档」的完整旅程,**so that** Phase 3 的四个 REQ(ROADMAP 五条成功判据)在真实环境中被最终证明,v1.13 milestone 可以收口归档。

<objective>
Phase 3 收口验证计划(mirror idi-02-04 结构):新建 backend/tests/test_e2e_g3.py 的 IDI_E2E 门控 @slow 用例(authorize→writing→tier→check→PASS→mission_complete 真链路);补跑全量回归;浏览器人检 UAT 五判据清单复走(用户执行);ROADMAP 五判据对账表 + REQ 勾稽 + SUMMARY 产出。本计划不写产品代码——只写测试与验收产物;发现实现缺陷按缺陷所在回 Wave 1-4 文件修复(修复记 SUMMARY,commit 留本计划分支)。

Purpose: ROADMAP 五条成功判据需要真实链路证据(Fake 级已证明逻辑;真 AI 遵守报告文法/确认词防误触/循环自动推进只有在真调用里可证——D-P3-29 的「模板逐字遵守」最终检验)。Phase 3 是 v1.13 milestone 的最后一块:本计划收口 = 可走 `/gsd-complete-milestone`。
Output: E2E 真链用例绿 + 全量回归绿 + 五判据对账表填满 + 人检 UAT 结果记录 + Phase 3 收口 SUMMARY。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/phases/idi-03-g3/03-CONTEXT.md
@.planning/phases/idi-03-g3/idi-03-01-SUMMARY.md
@.planning/phases/idi-03-g3/idi-03-02-SUMMARY.md
@.planning/phases/idi-03-g3/idi-03-03-SUMMARY.md
@.planning/phases/idi-03-g3/idi-03-04-SUMMARY.md

依赖接口(来自 Wave 1-4,全部直接消费):
- backend/session.py:authorize() / set_tier(tier) / start_writing() / start_check() / start_repair() / verdict_append() / snapshot()
- backend/g3.py:g3_available / authorize_write;backend/checks.py 全件;backend/grammar.py 新解析器
- backend/main.py 八路由(uvicorn 冒烟已由 idi-03-04 交付,本计划用 session 层直跑)
- test_e2e_rounds.py 全形态门控先例(54-66 环境门控 + 69-75 造盘 + 超时门卫 + 无人值守 denier 线程 277-289);pytest.ini slow marker(Phase 1)
- backend/tests/test_e2e_smoke.py(权限不可登录线程等支撑形态)

DESIGN.md 权威依据(判据对账用):§4.4(G3)、§7.3①②(自愈)、§7.4(行 4-7 + 只读归档)、§8.1/§8.2(授权与自检全节 + D-22)、§5.4(权限矩阵)。

分支纪律(per 仓库 CLAUDE.md §5):本计划执行者从当前分支 HEAD 切出 phase-03/idi-03-05 工作分支,plan 完成后合回原分支。发现 Wave 1-4 缺陷时修复 commit 也在本分支(单一分支单 plan;缺陷归属记 SUMMARY)。

前置条件(执行本计划时);claude CLI 已装并已登录(真实调用必需;未登录则向用户报告并暂停——人检 UAT 前置)。E2E 真调用建议宽松档(一检一修即止,时长可控,严格档循环真调用耗时不可预算——多轮一检一修复刻在 SUMMARY 备注,严格档两跳自动由 Fake 级闭环用例已证,真调用以宽松档全链 + 严格档首跳为合理平衡;执行者可按实际耗时择宽松档为主)。
</context>

<tasks>

<task type="auto">
  <name>Task 1: E2E 真调用链——authorize → start_writing(tmp 改名)→ tier → start_check → PASS → mission_complete(IDI_E2E 门控)</name>
  <reversibility rating="cheap">测试文件独立新增,零产品代码改动(发现缺陷时的修复属受控回写,不破契约)。</reversibility>
  <files>backend/tests/test_e2e_g3.py, pytest.ini</files>
  <read_first>
  - backend/tests/test_e2e_rounds.py(全文件门控形态:sys.path 头 + pytestmark + 门控函数 36-76 造盘与超时积分 + 277-289 denier 线程 + 真实耗时参数 43-48)
  - backend/tests/test_e2e_smoke.py(权限/登录兜底支撑形态)
  - backend/session.py(Wave 2 六函数语义;enter_project;snapshot)
  - backend/g3.py + backend/checks.py + backend/grammar.py(Wave 1 契约——断言按这些函数的返回形状)
  - backend/prompts.py(build_writing_prompt / build_check_prompt / build_repair_prompt——理解真调用对 AI 产出的文法约束面;断言按报告文法查产物)
  - DESIGN.md §6.4(报告文法——断言对象)、§8.2、§7.4(推导)
  - .planning/phases/idi-03-g3/03-CONTEXT.md(D-P3-30)
  </read_first>
  <behavior>
    - 用例 1 test_authorize_and_writing_real_cli:mktemp 造盘 phase3 四查合规项目(轮次文档全绿五件套 + 末行 `> 申请授权:是` + 空 annotations)→ enter_project → 断言 g3_available True → authorize() → AUTHORIZATION.md 存在且 derive_state=phase4 → start_writing() True → 轮询 wait_idle(deadline 420s 照 idi-02-04 节奏)→ 断言:DESIGN.md 存在、DESIGN.md.tmp 不存在(后端改名发生)、derive_state ∈ {phase5_awaiting_tier}(初稿无 check 报告)
    - 用例 2 test_selfcheck_real_cli_loose:同项目接续 → set_tier("宽松")→ tier 签名文件落盘 → start_check() True → wait_idle(deadline 600s,含自动修复跳)→ 断言:docs/DESIGN-check-1.md 存在、报告头部档位行 `> 自检档位:宽松`、问题分级表可被 parse_problem_grades 解析(或零问题)、最终 derive_state = mission_complete(宽松一检一修+PASS 即止)或 residual 收口(纯 P2 → verdict_append(修)→ PASS → mission_complete——两条分支都合法,按真实报告断言并记录)
    - 用例 3(防退化,非 slow):常轨(IDI_E2E 未设)全量跑,新文件两用例 skipped
    - 每 20s 输出进度行(照 test_e2e_rounds 的轮询日志模式);每条断言失败输出中文定位说明
  </behavior>
  <action>(1)新建 backend/tests/test_e2e_g3.py(照 test_e2e_rounds.py 头形态:sys.path 注入 + pytestmark = pytest.mark.slow + `if not os.environ.get("IDI_E2E"): pytest.skip` 门控):

造盘 helper _write_g3_ready_project(project):docs/discuss-round-1.md 手造四查合规文档(全 ✓ 维度表 + 全已决清单 + 批注回应表空说明 + 决策登记最小化 + 末行 > 申请授权:是)+ docs/discuss-round-1.annotations.json 写 {"round":1,"items":[]}(空 items 证明无 pending)+ 简短 docs/transcript.md。

用例 1 造盘后:session.enter_project → snapshot g3_available → authorize() True → (project/AUTHORIZATION.md).is_file() → derive_state phase4 → start_writing() → wait(sess, deadline)→ 断言链:DESIGN.md is_file、tmp not is_file、derive_state == phase5_awaiting_tier。计时记 SUMMARY(真实撰写耗时)。

用例 2:同 helper 前进一步(复用用例 1 的项目目录或重造)→ set_tier("宽松") → (docs/DESIGN-check-tier.md) 落盘断言 → start_check() → wait → 读最新报告(报告头部与问题表断言:parse_tier_line(latest)=="宽松";报告可解析或零问题)→ derive_state 断言:mission_complete(理想分支)或 phase5_checking(纯 P2 残余分支)→ 残余分支:snapshot.selfcheck.questions 逐条 verdict_append(决策 "修" 或 "接受现状"——E2E 主张全修)→ 断言 derive_state = mission_complete(残余清零自动收口)→ 最终态经 GET 视图核对归档只读(浏览器点击留人检)。真实分支走向与耗时如实记 SUMMARY。

(2)pytest.ini:确认 slow marker 已注册(Phase 1 已建,零改动预期;仅确认记录)。

(3)执行本任务时把 slow 用例真跑一遍:IDI_E2E=1 .venv/bin/python -m pytest backend/tests/test_e2e_g3.py -q -m slow(CLI 已登录前提;发现真实缺陷——AI 不写 tmp、报告文法不合规、PASS 不落、改名竞态——按缺陷所在文件回修 Wave 1-4;**修 prompt 的文法贴入部分而非解析器**(prohibition);修复 commit 留本计划分支,SUMMARY 记缺陷→修复对照)。**路线覆盖度诚实记录**:E2E 只跑 config.ai_caller 当前路线,另一条路线在 SUMMARY 一行注明(照 idi-02-04 先例);真调用未触发的分支(如严格档完整循环、修复者真抛问)同样如实记「由 Fake 级用例覆盖」,不冒充。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && IDI_E2E=1 .venv/bin/python -m pytest backend/tests/test_e2e_g3.py -q -m slow 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1'</automated>
    <fails_when>slow 用例 failed/error(真实链路断:CLI 登录失效/AI 不写 tmp/报告文法不合规/PASS 不落/改名竞态——任何一条都是真发现,不是放宽对象);IDI_E2E=1 下两用例出现 skipped(门控写反);常轨全量回归含 failed;总用例数较 Wave 4 完成时下降。</fails_when>
  </verify>
  <acceptance_criteria>
  - backend/tests/test_e2e_g3.py 存在,含 `grep -n "IDI_E2E" backend/tests/test_e2e_g3.py` 命中行数 ≥ 1 且 grep -n "def test_authorize_and_writing_real_cli\|def test_selfcheck_real_cli_loose" 恰命中两行定义
  - IDI_E2E=1 下两用例 passed(非 skipped 非 failed);输出尾行 "2 passed"
  - 常轨全量回归全绿,新文件两用例无 IDI_E2E 时 skipped
  - 用例 1 断言链含 AUTHORIZATION.md is_file + tmp not is_file + phase5_awaiting_tier(grep test 文件可见断言文本)
  - pytest.ini slow marker 未改语义(零改动记录)
  - SUMMARY 含真实耗时(撰写/核查)与路线覆盖度记录(当前路线 + 未覆盖路线一行)
  </acceptance_criteria>
  <done>真实 CLI 全链:四查→授权凭证→tmp 改名→DESIGN.md→档位落盘→真核查报告(文法合规)→PASS/残余收口→mission_complete;发现的缺陷已修复并记录;真调用覆盖度诚实入档。</done>
</task>

<task type="auto">
  <name>Task 2: Phase 3 收口——全量回归 + 浏览器 UAT 五判据人检 + 判据对账 + SUMMARY + milestone 交接</name>
  <reversibility rating="cheap">验收与文档产物;无产品代码。</reversibility>
  <files>backend/tests/test_e2e_g3.py, .planning/phases/idi-03-g3/idi-03-05-SUMMARY.md</files>
  <read_first>
  - .planning/phases/idi-03-g3/idi-03-04-SUMMARY.md(Wave 4 冒烟与已验面——人检清单的对象基线)
  - .planning/ROADMAP.md(Phase 3 五条成功判据——逐条对账对象)
  - DESIGN.md §7.4(完成态段:判据 5 的验收对象;§6.1 目录结构清单:AUTHORIZATION.md/docs 全套)
  - backend/tests/ 全目录(REQ 归属清单核对)
  </read_first>
  <behavior>
    - 全量回归一次通过(143 + Wave 1-4 全部新增 + 本计划 2 slow skipped 常轨)
    - 浏览器人检 UAT 判据五点逐项真机复走(bash run.sh 或 uvicorn + 浏览器,真实 CLI),每点一行结论(通过/问题+描述)记入 SUMMARY UAT 表
    - ROADMAP 五判据对账表:每条一行(判据 + 责任 REQ + 证据:测试函数名/sentinel/人检点),五条全证据才算收口
    - REQ 四条(FLOW-05/DATA-02/03/04)在 SUMMARY 逐条标注完成证据
    - 造盘真实项目的目录结构按 §6.1 清点(AUTHORIZATION.md 项目根 / docs/DESIGN-check-N / tier 签名 / DESIGN.md——ls 输出粘贴)
    - 30 条 D-P3 决策覆盖对账(plans 1-5 各自 D 清单 → 决策覆盖表一行一决策;无遗漏)
    - milestone 交代:Phase 3 完成 → 下一步 `/gsd-complete-milestone`(v1.13 归档);Deferred 清单确认(超出 v1.13 范围的想法记 Deferred,不塞本 phase)
  </behavior>
  <action>(1)跑全量:.venv/bin/python -m pytest backend/tests/ -q,记录最终用例数(143 基线 + 全部新增 + 2 slow skipped)。

(2)人检 UAT 交接(执行者能跑则跑,不能跑则写清操作步骤交用户;bash run.sh / uvicorn 启动 → 浏览器造盘项目进入)五判据五点:①四查不合规时按钮 disabled、合规时点亮——点开确认 → 输错词放行不动 → 输「确认授权」放行 → 授权后进入撰写视图与直播 ②撰写中途杀进程重启 → 「继续撰写」出现 → 点击重跑覆盖(tmp 残留覆盖验证)③初稿完成 → 档位模态弹出 → 选宽松 → 开始自检 → 报告出现头部档位行 ④(如入纯 P2/抛问分支)裁决卡逐条修/接受现状 → 继续修复 → 收口;或 running 态意外中断 → 继续自检恢复 ⑤最新报告 PASS → 「使命完成」欢呼模态弹出一次 → 只读归档态(DESIGN.md/轮次/报告可浏览;划词/处理批注/授权三面不可用;重启项目再开重现欢呼一次)。每点一行结论记 UAT 表(不足五点时按真实项目走向走到的分支记录,未走到的人为造盘补验——造盘指令写清)。

(3)五判据对账表写入 SUMMARY(每条:判据原文摘 + 责任 REQ + 证据指针 = 具体测试函数名(带文件名)/冒烟 sentinel/人检点编号);目录结构 ls 输出为判据 5 的证据粘贴;D-P3 覆盖对账表(30 行:D-P3-1..30 → 所在 plan/task)。

(4)SUMMARY 按模板产出 + milestone 交接段(下一步 /gsd-complete-milestone;Deferred 表确认零塞入)。REQ 四条勾稽完成。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1 && grep -c "成功判据\|UAT\|D-P3" .planning/phases/idi-03-g3/idi-03-05-SUMMARY.md 2>/dev/null && echo "summary-check-done"'</automated>
    <fails_when>全量回归 failed/error(退出码经 pipefail 直达整体);SUMMARY 文件不存在(grep 退 2);判据对账/UAT/D-P3 覆盖章节缺失(grep -c 计数为 0 → grep 退 1);summary-check-done 未吐出(任一环节阻断)。</fails_when>
  </verify>
  <acceptance_criteria>
  - 全量回归输出 "N passed, 6 skipped"(N ≥ 143 + 全部新增;无 failed)
  - .planning/phases/idi-03-g3/idi-03-05-SUMMARY.md 存在且 grep "成功判据" ≥ 1、"UAT" ≥ 1、"D-P3" ≥ 1(三章节在位)
  - 四条 REQ(FLOW-05/DATA-02/03/04)在 SUMMARY 逐条标注完成证据
  - 五判据对账表填满证据(测试函数名/sentinel/人检点);30 条 D-P3 覆盖表无遗漏行
  - SUMMARY 含「下一步:/gsd-complete-milestone」交接段与真实耗时/覆盖度记录
  </acceptance_criteria>
  <done>Phase 3 四 REQ 收口:五判据全证据(测试/冒烟/人检);全量回归绿;SUMMARY 完整含 milestone 交接;v1.13 milestone 可归档。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 真实 CLI 进程 → mktemp 造盘项目 | E2E 期间 AI 在临时目录真跑(权限门 tmp 放行面);测试产物不碰本工具仓库 |
| 全链真调用 → 磁盘签名 | AUTHORIZATION.md / DESIGN.md / check 报告在真链中产生;断言以文件现状为唯一依据(与生产行为同路径) |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi03-19 | Denial of Service | E2E 对真实 AI 依赖超时挂死(网络/登录/长文档撰写) | medium | mitigate | deadline 轮询(420-600s 超时即 fail 输出已等待时长;照 test_e2e_rounds 先例);wait_idle 收流兜底;宽松档优先控制时长 |
| T-idi03-20 | Tampering | E2E 误用本工具自身仓库作为项目目录(污染本项目) | high | mitigate | 全部造盘走 mktemp -d / tmp_path;测试断言路径以临时目录派生,零仓库绝对路径硬编码;grep 测试文件无本仓库路径 |
| T-idi03-21 | Repudiation | E2E 通过但人检未做即判收口 | high | mitigate | SUMMARY 模板把 UAT 五点列为显式表(空表 = 未完成);autonomous: false 保留人检面;判据对账表五条必须各有证据指针 |
| T-idi03-22 | Tampering | 为过 E2E 改锁定语义(判定式/解析器/矩阵) | high | mitigate | prohibition 显式声明修方向 = prompt 文法贴入,不碰解析器/回写/矩阵;修复对照入 SUMMARY 可审计 |

执行说明:纯测试/文档计划,零包安装,无供应链项;涉及真 CLI 的慢用例由 IDI_E2E 门控在常轨回归排除。
</threat_model>

<verification>
1. Task 1 automated:IDI_E2E=1 slow 两用例真调用链 + 全量回归
2. Task 2 automated:全量回归 + SUMMARY 三章节存在性检查(grep 计数)
3. 人检:浏览器五判据 UAT(详 Task 2;执行者能跑则跑,否则交付步骤清单给用户;结果必须落 SUMMARY 才算收口)
4. 收口门槛:五判据对账全证据 + 四 REQ 全勾 + 30 D-P3 全覆盖 → Phase 3 完成 → `/gsd-complete-milestone`
</verification>

<success_criteria>
- 真实 CLI 全链(授权→撰写改名→选档→核查→PASS/残余→mission_complete)passed 并记录真实耗时
- 全量回归全绿(143 + 全部新增 + 2 slow skipped)
- 人检 UAT 五判据记录完整;五判据对账表填满证据;30 D-P3 覆盖无遗漏
- SUMMARY 产出且四 REQ 全勾 + milestone 交接段在位
- v1.13 milestone 收口就绪(/gsd-complete-milestone)
</success_criteria>

## Artifacts this phase produces(本计划新增符号清单)

- backend/tests/test_e2e_g3.py:test_authorize_and_writing_real_cli、test_selfcheck_real_cli_loose、_write_g3_ready_project 造盘 helper
- .planning/phases/idi-03-g3/idi-03-05-SUMMARY.md(五判据对账表 + UAT 五点表 + 30 D-P3 覆盖表 + 实测耗时 + 真调用覆盖度记录 + milestone 交接段)
- pytest.ini:预期零改动(确认记录)

<output>
Create `.planning/phases/idi-03-g3/idi-03-05-SUMMARY.md` when done
</output>

---
phase: idi-01
plan: 04
type: execute
wave: 3
depends_on: ["idi-01-03"]
files_modified:
  - backend/prompts.py
  - backend/session.py
  - backend/main.py
  - backend/g1.py
  - backend/tests/test_g1.py
  - frontend/index.html
  - frontend/app.js
  - frontend/style.css
autonomous: false
requirements:
  - FLOW-03
  - FLOW-06

estimate:
  tokens: 70000
  raw_tokens: 70000
  tasks: 2
  confidence: low

must_haves:
  truths:
    - "全新项目(无 docs/)时,进入界面出现「没想法」入口;点它跑内置发散指令模板,过程照常直播,产物落盘为 docs/brainstorm.md"
    - "发散可反复触发,brainstorm.md 每次整体覆盖、不编号、不冻结"
    - "draft.md(或 brainstorm 深化后的雏形)存在时,「没想法」入口消失/禁用——发散模式一经雏形诞生即关闭"
    - "点「认可雏形」(G1)后,项目 docs/ 下出现 discuss-round-1.md,内容 = draft.md 全文 + 末行合规的 > 申请授权:否(后端写入,非 AI);draft.md 本身保留不删;界面切到轮次视图占位"
  artifacts:
    - path: "backend/g1.py"
      provides: "G1 定稿纯函数:copy draft → discuss-round-1.md + 追加标记行"
      contains: "def finalize_g1"
    - path: "backend/prompts.py(扩展)"
      provides: "发散指令模板(§3.7 三要点)与发散后深化提示词"
      contains: "def build_divergence_prompt"
    - path: "backend/tests/test_g1.py"
      provides: "G1 落盘文法与幂等防重用例"
    - path: "frontend/app.js(扩展)"
      provides: "「没想法」入口与「认可雏形」按钮交互"
  key_links:
    - from: "backend/main.py"
      to: "backend/g1.py"
      via: "POST /api/g1 调 finalize_g1,产物由 derive_state 随后判为 phase3"
      pattern: "finalize_g1"
    - from: "backend/session.py"
      to: "backend/prompts.py"
      via: "发散触发时走 build_divergence_prompt,产物写 docs/brainstorm.md"
      pattern: "build_divergence_prompt"
---

## Phase Goal

**As a** 没有明确想法的用户,**I want to** 一键进入发散模式让多视角风暴产出候选方向,或在雏形成熟后点「认可雏形」正式定稿,**so that** 零起步也能走完阶段 1-2,并留下第一份带授权标记的正式轮次文档。

<objective>
补齐 Phase 1 的两个剩余门:发散模式(FLOW-06:内置发散指令模板、brainstorm.md 覆盖落盘、雏形存在即关闭入口)与 G1 定稿(FLOW-03:后端复制 draft.md → docs/discuss-round-1.md 并追加合规 `> 申请授权:否` 标记行,draft 保留)。跑在同一 AICaller 链路(与既有会话/直播/权限门零特殊化)。

Purpose: FLOW-06 解决零起步冷启动;FLOW-03 是阶段 2→3 的唯一正式出口,其标记行文法由 derive_state 的完整轮判据消费(Plan 02),三点闭合。
Output: 发散模式 + G1 定稿可用,Phase 1 全部 10 个 REQ 收口。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/phases/idi-01-1-2/01-CONTEXT.md
@.planning/phases/idi-01-1-2/idi-01-03-SUMMARY.md

依赖接口(直接使用):
- backend/session.py:enter_project/send_message 流水线、current_project
- backend/ai_caller.py:make_ai_caller → run 生成器、事件流经 EventBroker 出 SSE
- backend/state.py:derive_state(phase1_new 判定 = 无 docs/)
- backend/prompts.py:§3.8 语言红线句已有

DESIGN.md 权威依据:
- §3.7 发散模式(D-16 四条):入口仅阶段 1-2(雏形诞生前)、模板要点(多视角风暴 N 固定视角各 2~3 方向鼓励离谱 → 收敛 3~5 候选每个含一句话说明+为什么值得做 → 引导用户挑选或委托 AI 挑)、产物 docs/brainstorm.md 覆盖不编号不冻结不进未决清单、出口 = 挑选后深化为雏形回主干
- §4.4 G1:草稿区末尾常驻「认可雏形」按钮;点击 = 后端将当前草稿定稿为 discuss-round-1.md、**后端**追加合规 `> 申请授权:否` 末行;draft.md 保留;阶段 1-2 的 AI 不要求 §6.3 模板,草稿格式自由
- §6.4 授权申请标记:文档最后一个非空行恰为 `> 申请授权:否`
- §3.8 语言红线注入发散 prompt

分支纪律(per 仓库 CLAUDE.md §5):本计划属多文件大改动——执行者从当前分支 HEAD 切出 phase-01/idi-01-04 工作分支,plan 完成后合回原分支(工作分支生命周期与 plan 对齐,不引入 worktree)。
</context>

<tasks>

<task type="checkpoint:decision" gate="blocking-human">
  <decision>G1「认可雏形」是不可回滚门,确认交互形态</decision>
  <context>按 reversibility 规则,one-way 决策须由人确认后才走过。本任务要定的是:点「认可雏形」后的交互形态(见选项)。DESIGN.md §4.4 字面 = 按钮常驻、点击即 G1 通过(无任何二次确认要求)。选项 A 即规范对齐形态;选 B/C 属交互增强,若选带确认的形态,须在 SUMMARY 记录为「记录在案的偏差」。</context>
  <options>
    <option id="direct-through">
      <name>A:点击即定稿(规范对齐,零确认)</name>
      <pros>逐字对齐 §4.4「点击即 G1 通过」原文;无多余交互</pros>
      <cons>误触即走到不可回滚门(单机自用,个人风险偏好可接受)</cons>
    </option>
    <option id="confirm-dialog-only">
      <name>B:前端一次性确认对话框</name>
      <pros>防误触;偏离 §4.4 字面(增加了它未要求的确认框)</pros>
      <cons>在 §4.4 之上追加交互步骤,属记录在案的偏差</cons>
    </option>
    <option id="require-recheck">
      <name>C:后端加二次确认参数</name>
      <pros>防误触最强,任何客户端都须显式带确认意图参数</pros>
      <cons>在 §4.4 之上追加未在 DESIGN.md 出现的交互协议,偏离最大</cons>
    </option>
  </options>
  <resume-signal>Select: direct-through 或 confirm-dialog-only 或 require-recheck</resume-signal>
</task>

<task type="auto" tdd="true">
  <name>Task 1: 发散模式——模板、触发与入口关闭逻辑</name>
  <behavior>
    - 用例 1:build_divergence_prompt 产物含三段结构标记:多视角风暴指令(N ≥ 4 固定视角列写明)、收敛指令(3~5 候选 + 一句话说明/为什么值得做)、挑选引导指令(用户挑或委托 AI 挑);含 §3.8 红线句;指定产物写 docs/brainstorm.md
    - 用例 2:触发发散(relay 后)brainstorm.md 被创建;再次触发后被整体覆盖(文件内容替换,mtime 变化,无 -2 编号新文件)
    - 用例 3:入口判定函数 divergence_available(project_path):无 draft.md 且无完整轮 → True;draft.md 存在 → False;有完整轮 → False(雏形已定稿即关闭)
    - 用例 4:prompt 含既有 brainstorm.md 内容(再次发散时看得见上一轮候选)
  </behavior>
  <files>backend/prompts.py, backend/session.py, backend/main.py, backend/tests/test_session.py</files>
  <action>(1)backend/prompts.py 增 build_divergence_prompt(project_path) -> str(发散模板要点 per D-P1-13/D-16:跑在同一 AICaller 链路;视角清单与三步结构按 §3.7):系统段(角色 + §3.8 红线);现况段(项目目录现状、既有 docs/brainstorm.md 全文若有);任务段(三步走:① 多视角风暴——从固定视角各出 2~3 个方向、鼓励离谱;视角清单写死在模板:解决谁的什么痛点 / 最省事的版本 / 最贵的版本 / 没人做但该有人做的;② 收敛——汇成 3~5 个候选方向,每个含一句话说明 + 一句为什么值得做;③ 引导用户挑选或委托 AI 挑选);落盘指令(把风暴与候选全文写入 docs/brainstorm.md,整体覆盖旧文件)。

(2)backend/session.py 增 trigger_divergence():校验 divergence_available(current_project) 为 True(不满足返回错误给前端,防绕过),走既有 AI 调用链(build_divergence_prompt → caller.run,事件照常出 SSE);并发限制沿用会话锁。增 divergence_available(project_path) 判定函数(逻辑见 behavior 用例 3——判定纯靠磁盘)。

(3)backend/main.py:POST /api/divergence → trigger_divergence(202);/api/enter 返回载荷增加 divergence_available 字段;GET /api/brainstorm → 当前 brainstorm.md 内容(前端展示候选列表用)。

(4)backend/tests/test_session.py 扩四个用例(behavior 列表):用 FakeAICaller 产伪事件,assert 落盘 / 覆盖 / 判定 / prompt 结构(greps marker)。先红后绿。</action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_session.py -q 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1'</automated>
  </verify>
  <fails_when>任一 pytest 输出含 failed/error;session 用例数 < 10(既有 6 + 新 4);全量回归基线(25+)下降。</fails_when>
  <done>发散条链路(Fake 级)全绿:模板三段、覆盖落盘、入口关闭逻辑、再发散可见旧候选。</done>
</task>

<task type="auto" tdd="true">
  <name>Task 2: G1 定稿——finalize_g1 纯函数 + 「认可雏形」按钮 + 界面接线</name>
  <reversibility rating="one-way">任意一次合法 G1 后,产出的 discuss-round-1.md 与其末行标记被 derive_state 永久消费为"阶段 3 已进入"——误触发走的是用户文件系统的不可回滚状态变更(需删文件才能退出轮次),故前置决策门确认交互形态(选择项含"零确认直通"选项)。</reversibility>
  <behavior>
    - 用例 1:临时目录含 docs/draft.md(多行内容),finalize_g1(project_path) 后 docs/discuss-round-1.md 存在,内容 = draft 全文 + 末行恰为 `> 申请授权:否`(strip 后全等,前缀不算)
    - 用例 2:draft.md 原 file 保留、内容不变(定稿不改草稿)
    - 用例 3:幂等防护:discuss-round-1.md 已存在时 finalize_g1 抛错(G1 只走一次,重入合法路径不存在——重开即 phase3)
    - 用例 4:标记行前 allow 空行存在时 last_nonempty_line 语义不破坏(用 state.is_complete_round 复核产出的文档被确认为完整轮)
    - 用例 5:finalize 后 derive_state(project_path) 返回 phase3、current_round=1(三模块闭环)
  </behavior>
  <files>backend/g1.py, backend/main.py, backend/session.py, backend/tests/test_g1.py, frontend/index.html, frontend/app.js, frontend/style.css</files>
  <action>(1)backend/g1.py:finalize_g1(project_path: Path) -> Path 纯后端函数(不涉及 AI——D-P1-12,G1 是后端动作):读 docs/draft.md(不存在抛 FileNotFoundError 并提示先有雏形);若 docs/discuss-round-1.md 已存在抛 FileExistsError(防护重入);写 docs/discuss-round-1.md = draft 全文 + 换行 + `> 申请授权:否` + 换行(确保“最后一个非空行”语义成立,draft 尾部多余空白不破坏标记——必要时 rstrip draft 尾后接标记;draft.md 不删不改)。写完返回新文件路径。

(2)backend/main.py:POST /api/g1 → session 转调 finalize_g1(current_project),成功后返回新 derive_state 结果;失败(无 draft/已定稿)返回 4xx 与中文原因。session 层:若 AI 调用在飞,拒绝(锁语义同 send_message)。

(3)前端:「认可雏形」按钮从禁用态转正,常驻 draft-view 末尾(§4.4 常驻,不是弹窗确认式)。交互形态按前置决策门(checkpoint)所选选项实现:direct-through = 点击即 POST /api/g1,零确认;confirm-dialog-only = 点击先弹一次性确认对话框(文案:「定稿后进入轮次阶段,不可退回阶段 1-2 会话」)再 POST;require-recheck = 后端 /api/g1 加确认意图参数,前端带参调用。POST /api/g1 成功后返回新 derive_state 结果,界面重进(POST /api/enter)刷新状态,切到轮次占位视图(Plan 03 的 rounds-placeholder,显示当前轮号 1)。「没想法」入口:进入 phase1_new 且 divergence_available 时,空草稿区上方显示「没想法?让 AI 发散出候选方向」按钮 → POST /api/divergence,过程中工作面板照常直播,brainstorm.md 就绪后 GET /api/brainstorm 渲染候选(markdown)。「挑选候选后」交互 = 用户在会话流发消息告知所选方向(轻实现:说明文案引导,无专门 UI)——发散出口即回到主干深化。

(4)backend/tests/test_g1.py:五用例(behavior 列表)先红后绿,其中用例 5 断言跨模块闭环(finalize 后 derive_state = phase3)。</action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python -m pytest backend/tests/test_g1.py backend/tests/test_session.py -q 2>&1 | tail -2 && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1 && (.venv/bin/uvicorn backend.main:app --port 8767 &) && n=0 && until curl -sf http://127.0.0.1:8767/api/health >/dev/null 2>&1; do n=$((n+1)); if [ $n -gt 120 ]; then lsof -ti:8767 | xargs kill 2>/dev/null; exit 1; fi; sleep 0.5; done && D=$(mktemp -d) && mkdir -p $D/docs && printf "# 雏形\n内容\n" > $D/docs/draft.md && DRAFT_MD5=$(md5 -q $D/docs/draft.md) && curl -sf -X POST http://127.0.0.1:8767/api/enter -H "Content-Type: application/json" -d "{\"path\": \"$D\"}" >/dev/null && curl -sf -X POST http://127.0.0.1:8767/api/g1 >/dev/null && grep -qx "> 申请授权:否" <(tail -1 $D/docs/discuss-round-1.md) && [ "$DRAFT_MD5" = "$(md5 -q $D/docs/draft.md)" ]; rc=$?; lsof -ti:8767 | xargs kill 2>/dev/null; [ $rc -eq 0 ] && echo "g1-e2e-ok"'</automated>
  </verify>
  <fails_when>任一 pytest 含 failed/error(pipefail 保证 tail 不吞退出码);g1 用例 < 5;curl -sf 任一步失败;discuss-round-1.md 末行非恰为 > 申请授权:否(grep -qx 全等断言,前缀/后缀不算);draft.md 内容变化(md5 前后不一致 = 草稿被改动或删除);uvicorn 起不来(等待循环 60s 上限)或失败路径 uvicorn 未清理;无 g1-e2e-ok(echo 仅在 rc=0 时发出)。
  <done>G1 后端纯函数五用例全绿;真实 HTTP 链路冒烟过(draft→discuss-round-1.md、标记行、draft 保留);「没想法」与「认可雏形」前端入口可用;Phase 1 全部 10 个 REQ 落地。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 浏览器 → /api/g1、/api/divergence | 不可逆动作触发(G1)与发散触发均经用户点击 |
| AI 发散产物 → docs/brainstorm.md | 写入 docs/ 放行面;内容为 AI 产出,渲染须防 XSS |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi04-01 | Tampering | 直接 POST /api/g1 绕过确认对话框(用户没点确认) | high | mitigate | 后端幂等防护(已定稿抛错)+ 前端确认框;单机自用,浏览器即唯一入口面,可接受 |
| T-idi04-02 | Tampering | AI 直写 discuss-round-1.md 冒充 G1(绕过申请授权:否标记) | high | mitigate | prompt 指令轮次产物只出 AI 侧草稿;G1 文件由后端函数独占写入;轮次编号对齐由 derive_state 判定——AI 伪造的文件若末行非法仍判半成品(完整轮判据兜底) |
| T-idi04-03 | Repudiation | G1 误触发后无法追认“不是我点的” | medium | mitigate | 一次性确认对话框 + 响应中返回新状态;本地单人工具无审计面,接受 |
| T-idi04-04 | Tampering | brainstorm 内容注入 HTML(markdown XSS 同 T-idi03-02) | high | mitigate | 沿用 Plan 03 的 marked 无 raw-HTML 配置,统管 draft/brainstorm/会话渲染 |
</threat_model>

<verification>
1. pytest test_g1.py:G1 文法/幂等/闭环(5 用例)
2. pytest test_session.py 扩展:发散四用例(4 用例,总 10)
3. 全量回归绿(state 10 + transcript 6 + ai_caller 3 + session 10 + g1 5 + smoke 2)
4. HTTP 冒烟:构造 draft → POST /api/g1 → 文件存在、末行合格、draft 不动
5. 人检(UAT 批次):空目录走没想法 → 看 brainstorm → 会话发方向 → 认可雏形 → 轮次占位
</verification>

<success_criteria>
- FLOW-06 四条(入口限制、模板三段、覆盖不编号、雏形后关闭)全部有测试或行为证据
- FLOW-03:后端定稿、标记行合规、draft 保留、derive_state 判 phase3
- 发散跑在同一 AICaller 链路,过程照常直播(无第二套调用路径)
- Phase 1 十个 REQ 全收口(见 ROADMAP 成功判据 5、6)
</success_criteria>

<output>
Create `.planning/phases/idi-01-1-2/idi-01-04-SUMMARY.md` when done
</output>

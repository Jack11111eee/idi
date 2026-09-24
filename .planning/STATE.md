---
gsd_state_version: "1.0"
milestone: v1.14
milestone_name: 前端视觉与可访问性
current_phase: 08
current_phase_name: 可访问性语义与键盘
status: ready_for_verification
stopped_at: Completed idi-08-03-PLAN.md
last_updated: "2026-09-24T06:16:27.476Z"
last_activity: 2026-09-24
last_activity_desc: Completed idi-08-03-PLAN.md — all 3 plans done, awaiting phase verification
state_head: fa7813a12b6b002a896805dfb4d7d0a989e84a6a
progress:
  total_phases: 6
  completed_phases: 5
  total_plans: 21
  completed_plans: 21
  percent: 83
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-09-21)

**Core value:** 未经用户明确授权,流程绝不进入"撰写总设计文档"步骤;文档通过自检提示「使命完成」即为终点(只读归档态)。
**Current focus:** Phase idi-08 — 可访问性语义与键盘

## Current Position

Phase: idi-08 (可访问性语义与键盘) — EXECUTING
Plan: 3 of 3
Status: Phase complete — ready for verification
Last activity: 2026-09-24 — Completed idi-08-03-PLAN.md

Progress: [████████░░] 83%

## Performance Metrics

**Velocity:**

- Total plans completed: 31
- Average duration: -
- Total execution time: 0 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. 行走骨架 | 4 | - | - |
| 2. 轮次收敛循环 | 4 | - | - |
| 3. 授权、自检与终点 | 5 | - | - |
| idi-04.1 | 4 | - | - |
| idi-04 | 3 | - | - |
| idi-05 | 4 | - | - |
| idi-06 | 4 | - | - |
| idi-07 | 3 | - | - |

**Recent Trend:**

- Last 5 plans: -
- Trend: -

*Updated after each plan completion*
**Per-Plan Metrics:**

| Plan | Duration | Tasks | Files |
|------|----------|-------|-------|
| Phase idi-01 P02 | 10min | 2 tasks | 5 files |
| Phase 1 P01 | 122min | 3 tasks | 16 files |
| Phase idi-01 P03 | 125min | 3 tasks | 10 files |
| Phase idi-01 P04 | 33min | 2 tasks | 9 files |
| Phase idi-02 P01 | - | 2 tasks | 4 files |
| Phase idi-02 P02 | - | 3 tasks | 6 files |
| Phase idi-02 P03 | - | 2 tasks | 3 files |
| Phase idi-02 P04 | - | 2 tasks | 2 files |
| Phase idi-03 P01 | - | 3 tasks | 5 files |
| Phase idi-03 P02 | - | 3 tasks | 5 files |
| Phase idi-03 P03 | - | 2 tasks | 3 files |
| Phase idi-03 P04 | - | 3 tasks | 3 files |
| Phase idi-03 P05 | - | 2 tasks | 3 files |
| Phase idi-04 P01 | ~30min | 3 tasks | 4 files |
| Phase idi-04 P03 | 11min | 2 tasks | 2 files |
| Phase 04.1 P01 | 22min | 3 tasks | 2 files |
| Phase 04.1 P02 | 2min | 2 tasks | 1 files |
| Phase idi-04.1-radix P03 | 41min | 3 tasks | 2 files |
| Phase idi-04.1 P04 | 20min | 3 tasks | 2 files |
| Phase idi-05 P01 | 20min | 3 tasks | 2 files |
| Phase idi-05 P03 | ~45min | 3 tasks | 2 files |
| Phase idi-05 P04 | 17 min | 3 tasks | 3 files |
| Phase idi-06 P01 | 12 min | 2 tasks | 2 files |
| Phase idi-06 P02 | 24min | 3 tasks | 2 files |
| Phase idi-06 P03 | 46 | 3 tasks | 2 files |
| Phase idi-06 P04 | 16m | 3 tasks | 5 files |
| Phase idi-07 P01 | 10 min | 3 tasks | 3 files |
| Phase idi-07 P02 | 14 min | 3 tasks | 2 files |
| Phase idi-07 P03 | 33 min | 3 tasks | 2 files |
| Phase idi-08 P01 | 8 min | 3 tasks | 2 files |
| Phase idi-08 P02 | 12min | 3 tasks | 2 files |
| Phase idi-08 P03 | 16min | 3 tasks | 1 files |

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- [Roadmap]: v1.14 阶段边界 = 5 阶段(Phases 4-8),按"风险面 + 契约依赖"切,而非按审计报告的六支柱切——P4 设计契约与令牌层(硬前置,唯一纯重构阶段)、P5 排版与视觉层级(承载核心价值修复)、P6 布局稳健性(回归风险最高的 CSS 阶段)、P7 交互状态与焦点样式(纯追加)、P8 可访问性语义与键盘(唯一触碰 app.js/index.html 的阶段)。四份研究的建序分歧按"Architecture 的骨架胜出、Pitfalls 的 Phase E 折入 P8 作收口 gate、STACK 的六步作为 P4 的提交序"调和
- [Roadmap]: v1.14 压缩裁定——6 阶段压到 5 阶段,采用的唯一合并是研究自陈允许的那一条(交互状态 P3 并入焦点样式 P5,即本路线图 P7);**未**采用"P3 并入 P4"这一被研究明令禁止的合并。焦点规则在 P7 落地、`tabindex` 在 P8 落地,以满足"tabindex 与 :focus 同提交"硬规则的实质(不存在可聚焦而焦点不可见的中间状态)
- [Roadmap]: CHECK-01/02 两条校验脚本并入 P4 而非独立前置阶段——它们校验的不变量(块外零 hex、声明令牌配对达 AA)正是 P4 的中心主张;在必须满足该不变量的同一阶段交付检查器,把该阶段的中心主张从散文变成一条命令,后续每个阶段免费继承该工具
- [Roadmap]: A11Y-04(4 处对比度失败)归 P4 而非 a11y 阶段——AA 达标值是**令牌值决策**,在声明处选定;实测失败面为 ≥9 对(审计的 4 是抽样低估),含 `.annotation-answered` 1.88:1 等 opacity 合成项
- [Roadmap]: A11Y-07(WCAG 2.5.8 命中区)归 P6——其边界条件由 420px 侧栏定义,必须与侧栏宽度决策同一次权衡;明确不得为此重构侧栏
- [Roadmap]: REG-03(重跑 b9664e0 五条修复的全部人工验收项)作为 P8 的收口 gate 而非事后补记——五条修复无任何自动化覆盖,而本里程碑重写它们所依赖的 CSS;无重跑即无"未破坏它们"的证据
- [Roadmap]: `#probe-controls` 的移除/重定位与暗色模式**不进本里程碑任何阶段**——前者是产品行为变更(且双路线界面契约是真功能),后者会翻倍对比度校验面;均记为独立未来候选
- [Roadmap]: 阶段边界采用纵向 MVP 切法——P1 = 行走骨架(AI 调用链 + 阶段 1-2 会话 + G1),P2 = 轮次收敛循环(批注 + G2 + 机器文法),P3 = 门与终点(G3 + 自检 + 归档),而非按后端/前端/集成横向分层
- [Roadmap]: 需求总数以 REQUIREMENTS.md 磁盘现状为准 = 20 条(编排器提示中的"17"为误计,FLOW 7 + UI 4 + AI 5 + DATA 4),覆盖率按 20/20 验证
- [Phase 1]: idi-01-02: derive_state 返回 {state, current_round, current_check} 锁定——current_round 仅 phase3、current_check 仅 phase5_checking 有值,Phase 2/3 按钮逻辑消费此形状
- [Phase 1]: idi-01-02: §7.4 推导表自上而下首条命中,行 1「无 docs/」先于一切——授权/设计文件不可能在无 docs/ 的目录出现,超出表的形态回退 phase12_in_progress 保证确定判定
- [Phase 1]: idi-01-02: 文法判定三态语义——起始行整行精确匹配(strip 后)、授权标记 strip 后全等(前缀后缀均不算)、PASS 结论行 startswith 前缀(尾注仍算)
- [Phase 1]: idi-01-03: AI-04 权限回环走依赖倒置——AICaller 经 set_request_permission 注入用户征求回调(session 挂起队列 + SSE permission_request 弹窗),ai_caller 不 import session
- [Phase 1]: idi-01-03: 用户全局 settings.json 的 Write(*) 等 allow 规则会在权限回调前自动放行、绕过 §5.4 权限门——两路线必须 setting_sources=[](SDK)/--setting-sources=(CLI);auth 不受影响(进程环境变量级)
- [Phase 1]: idi-01-04: G1 交互形态=direct-through(点击即定稿零确认)——决策门按 orchestrator 全自动授权 + DESIGN.md §4.4 字面选规范对齐选项;不可回滚兜底=后端幂等防护(FileExistsError)
- [Phase 1]: idi-01-04: finalize_g1 产物文法 = draft rstrip + 空行 + 标记行——draft 尾部多余空白不破坏完整轮判据;发散调用不落 [user] transcript(它是后台自主指令,产物走 brainstorm.md)
- [Phase 1]: idi-01-04: 入口判定后端化(divergence_available/g1_available 纯磁盘函数)——/api/enter 载荷返回供前端显隐,触发端点服务端强制防绕过;Phase 3 AUTHORIZATION.md 后端写入可复用 G1 纯函数+幂等防护形态
- [Phase 2]: plan-checker 收口通过(iteration 2,0 blockers/0 warnings/1 advisory)——B1(idi-02-04 verify 尾部 `;echo` 掩蔽退出码,改 && 链)、W1(annotations 路由 busy-409 与 D-P2-22 两条件契约矛盾,按契约收敛)、W2(before 计算改 selection.getRangeAt(0).start 方向无关)全修于 a8ecc20;advisory:annotations append 与 writeback 的毫秒级交错窗口可由模块级锁收口(执行期可选);6/6 REQ、24/24 D-P2、30/30 gap 项全覆盖
- [Phase 3]: 计划修订裁定(iteration 1 反馈 3B+5W+2I,9 修 + 1 外部已解)——B1(纯 P2 残余裁决链断:mode 增第四值 "p2" 于 D-P3-23 开放集内,questions = parse_problem_grades 四键卡数据;verdict_append 配对判定改「读追加后报告」双源收口)与 B2(裁决卡键契约 02/04 两端一字不差:p2={number,location,issue,suggestion}/paused={number,text})修于 06603c9;B3(repair_available 双条件恰一放行,running 态 False 防「继续自检/继续修复」双门)同修;W4(writing_tmp_exists snapshot 伪层字段,D-P3-10 二态文案逐字)、W3(archive 409 冒烟改 `curl -s -o /dev/null -w %{http_code}` 整数比较)、W2(半份判定 = 结论行缺失 → _next_check_n 同轮覆盖不跳号)同 commit;W1(W PATTERNS 未提交)由 orchestrator 预先解决于 ed32674;I1(预算边界)以 70% context 收口纪律条款注入 02/04;I2(route 409 分流)以「错误消息字面表」五条逐字落码;补丁 0b32056:parse_problem_grades number 列转 int 消除卡号混型配对隐患;4/4 REQ、30/30 D-P3 本地 gate 全过
- [Phase 3]: 计划修订二(iteration 2 反馈 1B+3W+1I 全修于 2997f89)——B1(idi-03-04 冒烟盘 D 缺 `> 核查结论:` 锚点 → 锁定 grammar 配对扫描空间为空,paused 断言必挂;补 FIX(P2×1) 锚点行,经真模块实测 unpaired=[1] 复活)修;W1(is_pure_p2 增「无锚点行 → False」半份 fail-closed 前置 + 半份 P2 盘回落 running 用例,堵 p2 死局态)修;W2(POST /api/writing 路由交付权从 02 Task 1 摘除归 03,三处计数 六→四/五→三 修正)修;W3(AuthorizeBody 删除,authorize 路由无请求体——防 FastAPI 422 断 04 冒烟无体 POST 链)修;I1(①scan_pending 正则措辞统一为「从 _VERDICT_RE 派生 _PENDING_QUESTION_RE」②build_repair_prompt truth 改三参与 action 一致 ③04 不可达态 behavior 删除)全修;30/30 D-P3、12/12 verify-directions、plan-structure×5 本地 gate 复跑全过

- [Phase 3]: UAT 四处运行时缺陷修复(503f374,复验 862703c)——G-idi03-1(high):start_repair finally 守卫从「tmp 在盘即 return」改为 hop-local `tmp_consumed` 标志(仅 tmp_path.replace 实际执行处分支置 True),堵死严格档无界自动链(修复前实测 84 跳/1.5s→修复后恰 1 跳),命名 flake test_next_check_n_half_report_no_skip 转 10/10 确定;G-idi03-2:新增 session 层 _unpaired_pending_questions 以 unpaired 编号过滤锚点无关扫描,裁决与呈现共用同一配对空间(grammar.py 锁定语义零触碰);G-idi03-3:loadArchiveView 复位两推进按钮(归档态 继续自检/继续修复 不可见);G-idi03-4:applyPhase3Extras 隐藏 checksPanel(跨项目状态残留);修复仅 3 文件(session.py +35/−5、test_session.py +117、app.js +5),grammar/state/checks/g3/main/prompts 零改动
- [Phase 3]: 决策覆盖 gate 30/30 通过 ≠ 运行时语义成立——G-idi03-1 是 D-P3-16 的活偏差,而该 gate 当时报 30/30(只扫 PLAN/SUMMARY 文本);记入方法论教训:门通过须以行为验证佐证
- [Phase 3]: 遗留已知项(已闭合)——Phase 2 `02-VERIFICATION.md` 的 covered_digest 漂移,已在里程碑收口由复验代理刷新至当前冻结树(commit a5bfcad),三阶段验证指纹与代码树一致
- [Phase 4]: idi-04-01 颜色契约落地——单一围栏 `:root` 块(25 tier-1 primitive + 50 tier-2 语义令牌 = 75);块外裸 hex 由 117 归 0(CHECK-01 PASS);S-3 已批准并落地(10 处控件边框 `#ccc`→`#8a8a8a`);`--gray-600: #6a6a6a` 为每个背景上都通过的最浅 muted 灰(`#767676` 在 `#fafafa` 仅 4.35:1);`--color-action-irreversible*` 机械确认只被 `#btn-authorize` 消费;12 个 `#2e8b57` 站点全部归位(含使命完成模态边框 → `--color-border-success`)
- [Phase 4]: idi-04-01 令牌声明采用「与消费者同提交」纪律(Hard Rule 5)——`--color-text-inverse`/`--color-kind-fg`/`--color-border-danger-subtle` 延至 Task 3 与其唯一消费者同提交声明;`--color-surface-success` 刻意**不声明**(其假想消费者各自已持 `-surface` 令牌,Phase 5 还会把两族改为实心填充)
- [Phase 4]: idi-04-01 结构性纯度已机械复核——`f912c1a` 与工作树的「选择器行」diff 只多出 `:root {` 一行;无既有选择器改位、改名或增删声明。S-4(`#round-doc.round-frozen` 的 `opacity: 0.55`)**不属本计划**,由 Plan 02 落地
- [Phase 4]: idi-04-01 pytest 基线照实记录为**实测 225 收集**(219 passed + 6 skipped),不照抄 ROADMAP/REQUIREMENTS 的陈旧 219;本计划的 actuals = 6584 tokens(chars/4 over 26334 字符),远低于 estimate 95000 —— 记录真实值以校准后续估算
- [Phase 04]: idi-04-03: CHECK-02 对比度校验落地——配对清单以令牌名书写于 :root 围栏内(与令牌同一 diff,漂移可见),29 TEXT + 5 NON-TEXT = 34 对(下限 ≥24/≥20/≥4),另 1 条 ORDER 层级断言;脚本零依赖(仅 re/sys)、只读、对未声明令牌名与未列出的 ORDER 操作数大声失败(exit 1)
- [Phase 04]: idi-04-03: ORDER 断言取严格序关系(ratio(quieter) < ratio(louder)),非 ≤0.30 阈值门——UI-SPEC 已显式接受 0.311 对 ≤~0.30 guide 的残差,阈值门会在 HEAD 上立即失败;实测打印 ORDER 0.311(=5.18/16.67)。失败方向已实证:把 --gray-600 加深到 #000000 时四条 muted 背景对全部 PASS(20.12/21.00/19.26/18.10),只有 ORDER 报 FAIL: hierarchy inverted 1.207 并 exit 1 —— 这正是 SC3「层级与比值一起校验」的机器化形态
- [Phase 04]: idi-04-03: --gray-100 保持 #eeeeee,实测 muted 比值 4.66(非折叠前 #f0f0f0 上的 4.75);不得为凑 4.75 回改——那会违反 D-15 并带动 --color-surface-hover / --color-border-subtle 漂移
- [Phase 04]: idi-04-03: 四条命令的失败方向全部实证(CHECK-02 两次:阈值失败 + 层级倒置);Task 2 为纯注入→观察→还原,净 diff 为零,故无独立提交——残留扫描即为验收(grep #deadbe=0 / 注入对=0 / !important;=1 / --gray-600:#6a6a6a=1)
- [Phase 04.1]: D-16 核实成立:无 muted-text 类元素落在 <button> 内,PAIR --color-text-muted ON --color-surface-hover 不进清单,CHECK-02 清单为 43 对(34 TEXT + 9 NON-TEXT)+ 1 ORDER
- [Phase 04.1]: R-3 只删 .tier-desc 的 opacity: 0.9 一条声明,font-size/font-weight 一字未动;R-1 只加 z-index 一条声明,不加 position(#state-badge 刻意不是 position: fixed 浮层)
- [Phase 04.1]: 新 shadow 令牌 shadow-overlay 与 .overlay-card 的 box-shadow 消费者同一次提交落地(Hard Rule 5);item_smoke 的 R-2 断言用短 needle "0.2",守住 wave 3 的「全文件唯一颜色字面」计数不变量
- [Phase 04.1]: CHECK-01 的 tier-1 交替式加宽为含 radix(仅一处正则),其余断言逐字未动;D-03 改名后旧交替式对 var(--radix-… 不匹配,守卫静默空转而仍打印 PASS,加宽后重新可机械查
- [Phase 04.1]: 空转对照被实证:同一份注入 var(--radix-gray-11) 的样式表,新守卫 FAIL/exit=1,用 sed 's/|radix//' 重建的旧守卫 PASS/exit=0 —— 这是本次修复的全部理由,不是推论
- [Phase 04.1]: check-02-contrast.py 在 43 对清单上四条硬失败路径逐一复证(未知名/标记数 44 vs 43/覆盖率 10 below floor 24/20/4/ORDER inverted 2.753),代码 delta 为零故无独立提交,沿 idi-04-03 先例
- [Phase 04.1]: 全部八次变异运行在 mktemp -d 临时仓库根上完成;frontend/style.css 是本阶段已提交的交付物,变异前后逐字节一致(git diff --exit-code 为空)
- [Phase 04.1]: D-14 断言改造落地:#btn-authorize 的 color 接 --color-action-irreversible-fg(green-12),不是 --color-action-irreversible(green-11) —— 计划原文的令牌对位有误,照抄会让 item 3 永远 FAIL
- [Phase 04.1]: box-shadow 的 rgba(0, 0, 0, 0.2) 是全文件唯一保留的颜色字面(计数不变量 == 1),其形状由 R-2 的 --shadow-overlay 固定,不是令牌接线对象
- [Phase 04.1]: C-1 复核:ROADMAP 五处 + 04-UI-SPEC.md 携带项 #7 的 #brainstorm-view h2 = 14px / #8a6508 全部失真(实测 16px / #4f3422);只留证不改写,裁决权交用户
- [Phase idi-04.1]: CR-01 关闭:resolve_color 令牌未声明时返回 None,ok() 把 None 期望值记 BLOCKED —— 只改两处 helper,24 处调用点与全部 expected 字面值一字未动 — D-14 把 22 条硬编码 rgb(...) 断言换成令牌接线,移除了假 FAIL 的根因,同时移除了改名/删除时的 FAIL 能力;plan 03 已把该损失登记为由 check-02 的 43 对实测比值与接线断言旁的 info() 补偿 —— CR-01 证明该补偿只覆盖值轴,接线轴仍空转
- [Phase idi-04.1]: CR-01 的修复用变异证明钉死:反事实常量(68309d0 的探针体)+ 浏览器侧拦截 /style.css 删掉 --color-text-muted 声明 + 未变异对照支,三件套进 scripts/probe-05-resolve-color.py(不是门,不进守卫契约) — 变异测试是唯一能证明守卫真的会失败的手段(本项目已记录的教训);只跑一次真实树无法区分「守卫在工作」与「守卫静默空转」,故反事实与对照两支缺一不可
- [Phase 05]: D-07: --text-2xl 取 22px 而非契约的 18px(18px 已被 --text-lg 占用,改回会让 18px 有两个令牌名);围栏注释写明「名同值不同,不是笔误」
- [Phase 05]: D-10: 行高复用 --lh-tight 零新增令牌;整数配对数学上不可得,改写为比率配对,18/28 算术错误修正为 18/24,--lh-compact 单列注明 chrome-only
- [Phase 05]: D-08: TYPE-02 只复证、零 CSS 改动(三处已由 qrq 归入刻度与令牌,重写会改坏正确状态并使 --text-base 消费者计数漂移)
- [Phase 05]: 执行期用户裁决:收窄三条 chrome 标题规则的选择器为 #draft-view > h2 / #round-title / #brainstorm-view > h2(后代形态 1-0-1 会伸进 .markdown-body 压掉 0-1-1 的 h2);声明体逐字不动,未改动任何规则先后位置
- [Phase 05]: [Phase 05]: D-18 新开 --color-marker-active(= --radix-blue-11)承载活动面板标记,不复用 --color-action-primary —— 那个名字说的是「主要动作」,拿它做面板指示器会让名说谎(04.1 的 D-03 为同一条方法论付过代价)。颜色值不变,只换承载令牌名;60/30/10 的 Accent 域偏离登记为 A-7
- [Phase 05]: [Phase 05]: D-17 竖条用 box-shadow: inset 3px 0 0 而非 border-left(零布局位移),落在 .panel-header 而非 <section>(三个 section 的子元素都带背景色,会盖住左边缘的 inset 竖条);标题只改 color 不改 font-weight。3px 是 box-shadow 的偏移分量,不是 --space-* 刻度值(L-1…L-5 从未覆盖 box-shadow,冻结轮已有先例)
- [Phase 05]: [Phase 05]: D-20/D-21/D-22 两处 emoji 改用 mask-image + background-color 而非契约的 content: url(data-URI) —— 后者经 content 渲染为图片、不继承页面 CSS、currentColor 不可用,只能把 fill 钉死为转义 hex,那让「跟文字色」成为人工同步的约定。mask 只看 alpha,故 <path> 不带 fill、data-URI 内零颜色信息,契约字面量例外 L-3 整个撤掉(Gate 5 机械钉死)
- [Phase 05]: [Phase 05]: D-23 .collapse-indicator 零触碰(app.js 用 textContent 赋值,内联 <svg> 会被静默擦掉);mask 方案顺带消解 Pitfall 7 的第二半 —— 本阶段 DOM 里没有任何内联 <svg>
- [Phase 05]: [Phase 05]: D-05 连带义务履行完毕 —— idi-04.1-radix 因 covered_files 内容真变而 stale,走重新验证而非补指纹:四条守卫重跑全绿,04.1 三处结论逐条从 HEAD 重算(ORDER 0.363 / 4.53 / 3.24+3.15 / 冻结轮 1+saturate(0.6)+inset 琥珀 逐字不变),数量差值已登记(tier-1 25 不变、tier-2 47→48、清单 43→47)。04.1 报告文件零改动,指纹写回留给 /gsd-verify-work idi-04.1-radix
- [Phase idi-05]: 嵌入刻度取 24 / 18 / 16(文档档沿契约的数值阶梯下移一档),不是 28 / 22 / 18(同档会让 SC3 的「文档 h1 是全屏最大」为假)也不是 22 / 18 / 16(嵌入 h1 会与文档 h2 撞档)
- [Phase idi-05]: 修法是逐容器列举而非一条全局标题规则 —— 全局规则对四处 chrome 覆盖与 .markdown-body 都是惰性的,于是只命中这五个容器,却把影响面重新变成不可枚举(那正是 G-idi-05-1 的成因)
- [Phase idi-05]: 影响面枚举按 renderMarkdown() 的调用点而非按类名:九个目标里 #round-doc 有两个调用点,故 renderMarkdown( 计数是 11 而非 9;只枚举四个 .markdown-body 宿主正是缺陷存活到验证后的直接原因
- [Phase idi-05]: 变异探针抓到 item7 的静默 PASS 洞:all(w != "700") 对 None 恒真,故「无第四字重档」断言在标题读不到时会记 PASS;已改为 any(w is None) 与缺失同处置记 BLOCKED
- [Phase idi-06]: sticky 表头自带背景 var(--color-surface):.panel-header 规则体内无 background 声明,不加背景则滚动正文从标题行底下穿过;该令牌已被 #doc-panel 消费(:474)⇒ 零新增令牌(硬规则 5/8)
- [Phase idi-06]: 新规则不加 z-index:sticky 元素是 positioned,默认画在静态内容之上;实测滚动无正文穿透,故不新增 --z-* 消费者(若日后补须连带登记序关系断言)
- [Phase idi-06]: L-5/L-6 普查由单样本扩为 p1+p3 双样本:被祖先藏住的元素 getBoundingClientRect 全零,单样本会把隐藏静默读成 clearance 0 / 命中区 0(假 PASS 同型陷阱)
- [Phase idi-06]: 六目标 overflow-wrap 合并为一条规则而非通配:通配会波及已裁定的 .event-content word-break: break-all 并把影响面重新变成不可枚举(G-idi-05-1 的成因)
- [Phase idi-06]: 恒 FAIL 的断言与被断言对象同属缺陷:计算样式对 vh 返回 px 用值(30vh→270px)⇒ #latest-check 的保留项护栏改读源码文本计数;末条子元素高于容器时 last.top >= container.top 恒假 ⇒ 判据改为 last.bottom 落在可视带内
- [Phase idi-06]: #doc-panel 的 overflow-y: auto 必须保留:它是另一列的滚动者,不在面板区普查范围内,但 L-1 的 sticky 表头依赖它仍是最近的可滚祖先;删掉它凑计数会同时打破 L-1 与计数门(期望值是 4 不是 3)
- [Phase 06]: L-2 走「被实测推翻」这一支:三宽度(1440/1024/768)文档级溢出在波次 2 之后仍为 0px(与波次 1 基线逐字相同,该读数对目标失效模式结构性失明),另立判别性探针 #doc-panel 实测宽 vs clamp(340px, 30vw, 480px) 上界,实测 432/340/340 逐位等于上界 ⇒ @media 不写,计数保持 0
- [Phase 06]: A11Y-07 的落点由普查定:全文件唯一实测 < 24×24 的是未被需求点名的 .annotation-answer summary(722 × 17),需求点名的 #btn-authorize 实测 178 × 40 本就达标。机制锁定为原地加 min-height/min-width 两条裸字面量(24px 是 WCAG 2.5.8 常数,刻意不挂 var(--space-6))
- [Phase 06]: L-5 走「被实测推翻」:三样本判定行最小 clearance 40px,远高于 4px 阈值 ⇒ 零 padding 改动,#main-pane / #doc-panel / #chat-messages / #latest-check 一个都没抬
- [Phase 06]: clearance 断言的判定面收窄为「visible 且 intersects」:p3 的 #btn-authorize × #doc-panel = -122.6px 是滚出视口(与 padding 盒不相交)而非被裁切,不收窄会把正常状态记成缺陷
- [Phase 06]: [Phase idi-06]: Plan 04(gap closure)按项目所有者的显式裁定 remediation (b)把 LAYOUT-02 的 768px 承诺收窄为「badge 不被横幅遮挡」,并把 check-05 的 768px 分支改写为显式「未覆盖」+ 实测数值(h1 439.0–481.0 × 8–28 vs banner 285.3–482.7 × 12–39,相交带 768–855px);收窄登记于 UI-SPEC §L-2 / A-10 与 VERIFICATION.md frontmatter 的 override(accepted_by=Jack11111eee,overrides_applied 保持 0 留给复验);frontend/ 与 REQUIREMENTS/ROADMAP 零 diff
- [Phase idi-07]: **`ui.safety-gate` 经项目所有者预授权为已知假阳性(2026-09-23,执行期),且实测该门在整个阶段一次都没开火 —— 原因是它结构性地看不见本阶段的任何 UI 改动**。该门判据为 `block = frontend && hasUiFiles && !hasUiSpec`,只读**最后一次提交**的 `git diff HEAD~1..HEAD`。Phase 7 的 `frontend=true`(ROADMAP 带 `**UI hint**: yes`)、`hasUiSpec=false`(无 `idi-07-UI-SPEC.md`),故 `block` 退化为 `hasUiFiles`。**判为假阳性的依据:** 同能力的确定性门 `ui.plan-gate` 对本阶段返回 `block: false`,因为它的判据多一个 `hasFrontendEvidence`(需要带 UI 框架依赖的 `package.json`)——本仓库是 Python + 原生 HTML/JS,该信号恒为 false;两个门用不同谓词,`ui.safety-gate` 不咨询该信号。本阶段的契约面是 `07-CONTEXT.md` 的 D-01…D-20 + `idi-07-PATTERNS.md`,且 `idi-07-03-PLAN.md:71` 的 D-11 明文**禁止**新建 UI-SPEC 文件(`不得为了凑齐三处而新建 UI-SPEC 文件`)。故执行期不生成 UI-SPEC、不修改本阶段任何计划。
  **⚠ 修正执行前的预测(必须留档,原预测已被实测推翻):** 规划期曾推断「wave 2 / wave 3 的末次提交改 `style.css` ⇒ 该门会 halt」。**实测不成立。** GSD executor 的收尾提交恒为 docs/metadata 提交(只碰 `.planning/`),而该门只看末次提交,故 wave 1 / wave 2 实测 `hasUiFiles=false`、`block=false`,**预授权未被行使**。wave 1 的 `ee47beb`/`0e5820a`/`0243d6b` 与 wave 2 的 `cd5a1a1`/`0b40da5`/`aa7194b` 六次提交全部改过 `frontend/style.css`,该门一次都没看过。⇒ 该门的真实缺陷不是「偶尔误报」,而是**对本阶段完全失明**:它的单提交窗口恒落在 docs 提交上,故恒绿。**门绿不等于该波 UI 改动被审查过** —— 这是本阶段必须留档的方法论结论(与 `[Phase 3]` 的「门通过须以行为验证佐证」同族)。
- [Phase idi-07]: 环色 --color-focus 取 #1f63bd,逐字遵从 04-UI-SPEC S-4 的签核算术(「删除 opacity 后环回到 5.62」);它是整个颜色层里唯一不在 Radix 刻度上的值,与 04.1「值必须来自 Radix 步」相冲 —— 这条冲突已写进围栏注释,否则会被后来者当成漂移「修掉」。实测代价面:--radix-blue-11 在 .archive-mode 的 0.75 合成下只剩 3.03:1(余量 0.03);--radix-blue-12 是高对比文字步,作为 2px 环视觉上接近边框。
- [Phase idi-07]: item 10 的焦点环普查把「判定集为空集」判为 blocked 而不是 info() + return —— 这是对 item9 第 3 条的有意收紧。理由:item_verdict 只读行级裁决,一条未判定的探针会以 `item 10: PASS (N 条断言,0 FAIL,0 BLOCKED)` 的形态现身,「0 条断言静默通过」正是假 PASS 的形态。同一条根因也适用于 SC4(它的判定集更窄,空集更不可能是巧合)。
- [Phase idi-07]: item 10 的环读数只在「该元素成为 document.activeElement 的那一刻」采,唯一来源是 _IDI07_TAB_READ_JS;本项不存在「未聚焦时的 outline 读数」这个概念(未聚焦元素计算 outline-width 为 0px、outline-color 回落到 UA 值,拿静态读数判定会把每一个元素都判成 bad)。配套结论:焦点读数不得用 read_style(page, sel, prop)(它按选择器取值,结构上读不到「当前焦点元素」)。
- [Phase idi-07]: idi-07-02:D-07 的 gate 落在既有 L627 选择器上(`button:where(:not(:disabled)):hover:where(:not(:active))`),不落在新增规则上 —— 新增 `button:not(:disabled):hover`(0-2-1)既修不了缺陷(`:not(:disabled)` 不匹配禁用按钮,而旧规则仍匹配它,`.verdict-buttons button:disabled` 只设 opacity / cursor、不钉 background),又引入回归(类列 2 > `button.primary` / `.overlay-card button` 的类列 1,两族填充按钮 hover 时变灰底)。`:where()` 贡献 0 特异性 ⇒ 改写后特异性逐位不变(0-1-1),声明体逐字节不变。
- [Phase idi-07]: idi-07-02:朴素按钮的 :active 停在 0-1-0,让位由 L627 的 :where(:not(:active)) 承担 —— 特异性死结(必须胜过 hover 要求 >= 0-1-1,必须让 0-1-1 的填充族保住填充要求 <= 0-1-0)不在特异性上解。两半是一对选择器改写,改一必须改另一;**后来者不得为「对齐」把朴素 active 升到 0-1-1**(同特异性下源码顺序会夺走 button.primary 与 .overlay-card button 的填充,白字落在灰底上)。
- [Phase idi-07]: idi-07-02:D-08 的 rgba 落点选「围栏内令牌」支 —— --color-overlay-hover(0.06)/ --color-overlay-active(0.12)与消费者同提交,R-2 的「围栏外无裸 rgba()」不变量保住。check-01 不数裸 rgba()(这条纪律本无机械守卫),本计划把它落成围栏外 grep -c 为 0 的显式断言。两令牌不是对比度边界 ⇒ 不进 PAIR 清单(--shadow-* 同族也没有配对)。
- [Phase idi-07]: idi-07-02:两处值碰撞显式登记 —— --color-surface-active 与 --color-surface-user 同值(gray-4,注释点名 04.1-N-4 并同步扩写既有「Three values that must NOT be helpfully changed back」第 3 条,否则同一份注释自相矛盾);--color-border-hover 与 --color-text-muted 同值(gray-11)。同值不同名、不共享消费者,不得当违规「修掉」。
- [Phase idi-07]: idi-07-02:SC5 的填充半场取 #btn-send,不用 #btn-process-round —— 后者在 p1 标记里带 disabled(index.html:73),applySessionGates() 只 classList.remove(hidden)、从不清 disabled,故 #btn-process-round:not(:disabled):hover 根本不匹配,断言会 FAIL 而非 BLOCKED。SC5-朴素按下 的目标取 renderVerdictCard() 造出的裁决卡首个按钮(样本中稳定可达的朴素无底色按钮;.modal-buttons button 与 .tier-buttons button 都在 .overlay-card 内、已被填成主色,不是朴素族)。**「可见」不等于「可交互」**:前提检查必须是存在 ∧ 可见 ∧ 未被禁用三合一。
- [Phase idi-07]: idi-07-02:两条承重断言经变异测试证明非空转 —— 去掉 L627 的 :where(:not(:active)) ⇒ SC5-朴素按下 的「③ 按住不放读数 != ② 悬停读数」FAIL、item 10 报 2 FAIL;去掉 :where(:not(:disabled)) ⇒ SC5′ 的「禁用态 hover 背景 == 静默背景」FAIL。变异在已提交的树上做、定向 git checkout -- frontend/style.css 复原(不用 git stash —— 它跨工作树共享,本项目明令禁止)。
- [Phase idi-07]: idi-07-02:围栏内注释不能出现「令牌名 + 冒号」—— check-02 的 DECL_RE 扫围栏全文(含注释),写 --radix-gray-12: ... 会被当成一条值不可解析的声明而 FAIL;围栏外的机械判据是子串计数,连「规则体不写裸 rgba()」这样一句论证性散文都会把 grep -c 顶成 1。两条陷阱各付过一次 FAIL,修法都只是改写措辞。
- [Phase idi-07]: idi-07-02:**state.update-progress 再次把派生进度往回改**(写完 0 / 0%),已按 ROADMAP 的 ## Progress 校正为 completed_phases: 4 / percent: 67 / [███████░░░] 67%;同一批写入还把 .planning/state.json 的 next.reason 从 Phase 7 of 6 · 67% · executing 改成 Phase 07 of 6 · 0% · executing,已改回。completed_plans 的 16 → 17 是正确的增量,保留。**下一份计划执行后请复跑同样的核盘判据,不要采信该 handler 的输出。**
- [Phase idi-07]: idi-07-03:过渡挂载规则 + 减弱动效媒体块 + EXPECTED_MEDIA_QUERIES 0→1 **三者同一次提交** —— 只落块不改常量会让 check-05 --item 8 立刻变红,只改常量不落块会让守卫恒红。决策注释与 ok_true 标签一并改写,明确区分「这是 Phase 7 的减弱动效块」与「L-2 的窄窗口守卫仍走被实测推翻支、仍未写出」:混为一谈会让后来者把计数 1 读成「L-2 的守卫被写了」。删除该媒体块的人必须同时把常量改回 0。
- [Phase idi-07]: idi-07-03:行业标准的减弱动效片段在本项目里**不存在** —— 通行写法带两个 !important 声明,而本仓库的 !important 声明数必须恒为 1(唯一一条是 .hidden 的 display:none,44 处 classList 依赖它),采纳会让 check-04 从 1 变 3 而立刻变红。改走**按选择器重写为 transition: none** 的路线:它是确定性的、可被 getComputedStyle 直接断言的终态,而「几乎为零」不是;枚举写死而非通配,延续 Phase 5/6「影响面必须可枚举」的口径。
- [Phase idi-07]: idi-07-03:过渡落地暴露了跨计划耦合 —— 计划 02 的两条 hover 探针在 page.hover() / mouse.down() 之后**立刻**读 getComputedStyle,读到的是**过渡中间值**(实测 #message-input 读到 rgb(112,112,112) 而终态是 rgb(100,100,100);裁决按钮的悬停/按下同理),4 条 FAIL。修法是新增 read_settled_style 把读数**推到终态**(等两帧确保过渡已注册,再 await 该元素上所有动画 finished),**不是**放宽期望值 / 加容差 / 改读中间值 —— 后者会把过渡的瞬时行为写进契约。
- [Phase idi-07]: idi-07-03:时长判据**先按逗号拆成列表再逐项比**,不用子串包含 —— transition-duration 对两个属性序列化成 0.12s, 0.12s,而 0s 是它的子串,用 0s in raw 判「reduce 下全为 0s」会在**未生效**时假绿(与本项目已记录的 all(w != 700) 对 None 恒真是同型陷阱)。
- [Phase idi-07]: idi-07-03:收口记录 idi-07-VERIFICATION.md 刻意声明 status: human_needed 且**不声明** covered_files / covered_digest。前者因为本阶段有一条具名人工项(5″:禁用态仍一眼看出不可点);后者因为 #4155 的指纹对是 fail-closed 的(声明其一而缺另一直接判 stale),且指纹必须在**全部 PLAN/SUMMARY 都在盘之后**才能算(allCurrentArtifactsCovered 会扫活目录)。指纹写回与独立复核留给 /gsd-verify-work idi-07。
- [Phase idi-07]: idi-07-03:D-19 的四份报告(idi-04 / idi-04.1-radix / idi-05 / idi-06)**全部判为「内容真变 ⇒ 重新验证」**而非「重算 + 披露」—— 四份的 covered_files 都含 frontend/style.css(三份另含 scripts/check-05-ui-uat.py),两个文件在本阶段三个计划里都**真的变了字节**。**不得**用 gsd-tools query verification status 判定(这些相位目录一律返回 missing);判据只能是逐份比对 covered_files + 以 HEAD 内容重算 digest。四份各自的自身门已在 HEAD 上复跑全绿(证据见 SUMMARY),报告文件本身零改动。
- [Phase idi-08]: 键盘划词的提交手势 = **松开 Shift**(D-05),落成 initSelectionMenu() 内的独立 Shift 专用监听器;handleSelectionTrigger **一字不改**。原因:该函数挂在**每一次** keyup 上,在里面移焦会让键盘用户永远只能选中一个字符,而 A11Y-03 的验收项「Shift+方向键选区 → 菜单出现 → 焦点已入菜单」**仍会照常通过**(它测状态,不测可用性)—— 这就是「按路线图字面实现会假绿」的机制事实。
- [Phase idi-08]: 焦点交还写在 hideSelectionMenu() **这一个**函数里(四个调用点散落必然漏),且判据 selectionMenu.contains(document.activeElement) 必须在 classList.add 隐藏类 **之前**取 —— 焦点元素一旦 display:none,document.activeElement 立刻回落到 body,之后再判永远为假。实测已用反控钉死:焦点在菜单内 ⇒ 交还 round-doc;焦点在 #round-switcher ⇒ 不动。
- [Phase idi-08]: idi-08-01 实测推翻三条计划前提(登记,不改门不改样式表):①check-05 --item 10 的样本集是 p1/checking/p3(**不含 archive,也从不跑 p12**),CLI 无 --state 开关 ⇒ 「p3/checking/archive 三样本」与「p12 里 #round-doc 被 visible 过滤」两条验收面各自有一半无法用该门测;②D-01 的几何前提「盒高数千像素 ⇒ 左右两条贯穿全高的竖线」在 p3 样本不成立(实测盒高 778.64px < 视口 900px,环画成**完整矩形**),因为该样本的轮次文档只有 883 字节;新增实测:应用自身滚动位置下环**下边缘**越出 #doc-panel 滚动裁切界 3.64px,滚动 4px 即可四边全入(横向余量 36px);③Task 3 的 Escape 断言与九步脚本第 6/7 步归**计划 02**(本计划不装 Escape 处理器)。另:item 10 在改动前后均 PASS(41 条断言),判定集 p1 9→9 / checking 8→9 / p3 9→10,_idi07_tab_drive 上限 36→37 与 Tab 序 +1 相抵,无需改门 —— 是普查集变化,不是缺陷修复。
- [Phase 08]: idi-08-02: ARIA 三件套落 `.overlay` 而非 `.overlay-card` —— 被切换的节点(classList.toggle('hidden') 的作用对象)与被告白的节点是同一个,「宣告与实现一致」因此结构性可查,而不是两处需要同步的记账;无障碍名称用 aria-labelledby 指向弹窗内既有 <h3>(新增 2 个 id,id 总数 80→82,零改名零删除,G-idi01-8 未触发)
- [Phase 08]: idi-08-02: `inert` 走单点派生(读两个弹窗的 .hidden 现状)而非 open/close 成对记账,5 个调用点全部落在既有函数体内;只挂 #app —— 五个 .overlay 与 #selection-menu 都是它的兄弟,挂 document.body 或任何共享祖先会让打开的弹窗自身惰性、键盘与指针双路锁死(T-idi08-05)
- [Phase 08]: idi-08-02: Escape 取「单点监听器 + 显式优先级表」(划词菜单 → #confirmation-modal → #tier-modal),不取各弹窗各自的监听器 —— 后者会把「谁先响应」变成源码顺序事实;确认弹窗分支仅关闭、零决定(D-12,不代替「拒绝」以免把用户推进原生 window.prompt);档位分支复位 tierModalShown 但不复位 selfcheck.tier、不发任何请求(D-13)
- [Phase 08]: idi-08-02: D-16 实测(非「预期成立」)—— 用 Element.prototype.setAttribute 钩子捕获,setAttribute('inert') 执行的**那一瞬间** document.activeElement 仍是背景触发者(btn-enter)、不在弹窗内 ⇒ 显式 tierLooseBtn.focus() 是承重的,不是装饰;顺序锁定 remove('hidden') → syncBackgroundInert() → .focus()
- [Phase 08]: idi-08-02: 「背景在指针层面惰性」在本应用**不是判别性证据** —— .overlay 是 position:fixed; inset:0(style.css:800),背景点击本就被覆盖层吞掉,elementFromPoint 在背景元素中心返回的是覆盖层。故该断言改由「反射属性 + 判别性对照(惰性下 enter-path-input.focus() 为 no-op,摘掉属性后同一调用生效)」承担,指针半场按 human_judgment:true 交人眼收口
- [Phase 08]: [Phase idi-08]: idi-08-03: S8-1 是硬规则 5 的**授权例外**,不是违例 —— 编辑落在 renderAnnotations(app.js:1156-1212)内部,该函数被 ROADMAP §全局硬规则 5 / UI-SPEC §Do-Not-Touch List / 08-CONTEXT §明确不含 三处同时列为不得触碰。两条授权来源已逐字登记(UI-SPEC §Sign-Off Items 的 S8-1 行「用户裁定(2026-09-23)」列 + §本阶段的改动面 那一行)。**例外仅限 app.js:1162 的一个词**,清单未被推翻也未扩大;同函数的 L1164 历史轮串与 textContent-only 写入路径逐字未动。⚠ UI-SPEC 表里仍写 app.js:1121 是 wave 1 之前的旧锚点,HEAD 实测为 1162。
- [Phase 08]: [Phase idi-08]: idi-08-03: REG-02 门②的基线取**实测 9**,不是 08-CONTEXT D-21 的 6 —— 照抄 6 会造出一条永远不会失败的假门(A-5 已登记)。pytest 判据逐字记录为「219 passed / 6 deselected / 225 collected」:219 是**通过数**、225 是**收集数**;`-m "not slow"` 下 pytest 对那 6 条 slow 标记的端到端测试的官方标签是 **deselected**,本项目散文一直称 skipped —— 同一批 6 条,两个标签都记以免被读成漂移。两条 REG-02 门按 D-21/A-4 落为计划级 grep,**不写进 check-05**(它在 5 份 live 报告的 covered_files 里);代价已登记:它们不是常驻守卫。
- [Phase 08]: [Phase idi-08]: idi-08-03: **发现一条本阶段引入的功能缺陷,登记而非修复 —— Escape 无法关闭划词菜单**(菜单在 Escape 的 keyup 上重新弹出)。机制已用事件日志钉死:keydown 的目标是 #btn-annotate ⇒ 分派器关闭菜单并把焦点交还 #round-doc(F1-a)⇒ **keyup 到达时目标已变成 #round-doc**,命中既有的 roundDoc keyup 绑定 ⇒ handleSelectionTrigger 守卫全过 ⇒ showSelectionMenu()。三条判别性对照:T2 焦点在菜单外 ⇒ 保持关闭;T3 选区已折叠 ⇒ 保持关闭;T4 完全不按 Escape、只按任意键 ⇒ 菜单重现。**不修的两个理由**:①计划级 <verification> 明写「本计划只改一处文案」,修它就证伪计划级验证;②正确修法是至少三种形态的设计选择(抑制后续 keyup / 推迟交还 / 把交还搬出共享挂点),而 keyup 落入的 handleSelectionTrigger 函数体本身在不得触碰清单上 ⇒ Rule 4,用户的设计决定不由执行器自裁。它打破的契约:D-08、§K-2.6 第 6 步、REQUIREMENTS 的 A11Y-03 键盘半场人工验收项。
- [Phase 08]: [Phase idi-08]: idi-08-03: **D-23 的机制描述不成立(实测更正)** —— 归档切轮**不经过** updateFrozenPresentation。该函数全文件只有一个调用点(app.js:1082,在 loadRoundView 内);归档切换器的 change 处理器按 currentState === 'mission_complete' 分支走 **loadArchiveRoundDoc**(app.js:1295 → 915-924),既不碰 class 也不碰 disabled ⇒ applyArchiveView 在 L871 设的 disabled = true **在这条路上根本不会被复位**。**实测结果比计划预测更强**:切轮之后按钮同时保持 hidden **与** disabled,Pitfall 3 UI-6.3 那个场景在这条路上不可能发生。
- [Phase 08]: [Phase idi-08]: idi-08-03: **A11Y-08 的 Tab 序普查实测(两个状态)** —— 阶段 3:判定集 10 个元素、全部 Tab 可达、**#round-doc 位于第 2 位**,紧接 #round-switcher 之后、#btn-authorize(该状态下可见的 #authorize-row 按钮)之前,与 §K-1.7 逐字相符,环读数 2px / rgb(31, 99, 189) / offset 2px / :focus-visible=true;自检视图(checking):判定集 8 个、全部可达,#round-switcher 正确地不在判定集里(display:none)。**新登记**:自检视图里 #round-doc 是**零高度**(351×0,因 applyPhase5View 在 app.js:629 把它清空)却仍是第 1 个 Tab 停靠点、环仍画出 —— 这是计划 01 无条件 tabindex 的后果,首次在此实测,登记不修(计划 03 是零源码改动任务)。
- [Phase 08]: [Phase idi-08]: idi-08-03: 收口登记四份 —— (a) **指纹义务:D-01 路径下零债务实测成立**(frontend/app.js 与 index.html 不在任何 live 报告的 covered_files 里,style.css 逐字节未改,D-02 未触发故无报告需重算);**不得用 gsd-tools query verification status <phase> 判定 stale**(这些相位目录一律返回 missing),若日后真改 CSS 须以 HEAD 内容重算、不要看 mtime。(b) D-26 的 /gsd-verify-work idi-04.1-radix 登记为**既有、非本阶段引入**,本阶段既不加深也不清除。(c) D-17(#permission-modal 弹了键盘用户不知道)与 D-19(键盘划词无可发现性提示,唯一视觉信号是焦点环)**两条都不修**,归属 v2 A11Y-V2-02 与已登记已知局限。(d) STATE.md 的 [v1.14 P8] Deferred Item **不因本阶段关闭** —— 它被履行了一次(六条人工重跑 + check-03),但两者都不是常驻守卫。
- [Phase 08]: [Phase idi-08]: idi-08-03 收口后**用户裁定「现在修」,上一条的 Escape 缺陷已修复**(该条目「登记而非修复」的结论由此被取代;它不修的两个理由在当时成立,而 Rule 4 的决策权已按流程交回用户)。**修法**(app.js 的 Escape 分派器菜单分支,~4 行 + 围栏注释):`hideSelectionMenu()` 之后装一个 **capture 阶段的 `once` keyup 监听器**,对 Escape 的 keyup 调 `stopPropagation()`。为什么这样有效:document 的**捕获**阶段先于目标元素上的监听器 ⇒ 事件根本到不了 #round-doc,`handleSelectionTrigger` 不触发 ⇒ 菜单不会被重开。**三条设计边界**:①**不清空选区**(D-08 明文禁止,那会毁掉 Escape 后续选);②**一行都不碰 `handleSelectionTrigger`**(其函数体在 Do-Not-Touch 名单上,硬规则 5);③`once:true` 让监听器在首个 keyup 后自动摘除 ⇒ 无需记账、不会泄漏(与本项目「派生优于成对记账」的口径一致)。**修复前先做了形态验证再动手**(不靠推断):把候选机制注入活页面重跑同一场景 —— 未打补丁:菜单 `menuHidden=False`(缺陷复现);打补丁:`menuHidden=True`(修好);同时 **Shift 手势回归通过**(松开 Shift 仍把焦点送进 #btn-annotate)、**D-08 选区保留**(selLen=15 非零)。**修后复跑**:S1/S2/S3 三条 Escape 场景全过(菜单被关、焦点交还 #round-doc、选区保留);wave-2 的弹窗分支 A1/A2/B1/C1/C2/C3/D1/D2/D4/D5 全过(未受影响);`node --check` OK;`hideSelectionMenu`=8、`window.getSelection`=2、`syncBackgroundInert`=6、`tierModalShown`=4、`clearInlineError();`=9、`role=`=2、`id="`=82、`tabindex`=1、`:focus-visible`=9、`inline-error`=1;pytest **219 passed / 6 skipped**;`check-05 --item 1/4/10` PASS(45/65/41 条断言,0 FAIL,0 BLOCKED)。
- [Phase 08]: [Phase idi-08]: **一条计数门因本次修复而更正,并留下一条可复用的教训。** `grep -c 'hideSelectionMenu' frontend/app.js` 的门原写「必须仍为 7」,理由是「交还写在函数体内、不新增调用点」。实测已是 **8**:计划 02 的 Escape 分派器**必须**关闭划词菜单,而它**正确地**调用了这个单点关闭函数 —— 那正是 D-08 单点要求想要的行为,**不是**把交还散落到调用点。故门改为 8,并把判据从「计数等于某个数」改成**「交还逻辑是否仍只出现在函数体内、不出现在任何调用点」**(用 `grep -n` 逐行看)。**教训(本阶段第二次踩同一个坑):注释散文同样计入按子串计数的门。** 我本次的修复注释里写了函数名,计数 8→9,门当场变红 —— 与计划 02 那次 `role=`/`aria-modal`/`aria-labelledby` 三门的形态逐字相同。处置与那次一致:**改注释措辞(用「上面那次关闭」指代),不改门的期望值、不删注释**。**可复用的规则:凡有 `grep -c 'X'` 门的地方,X 的字面量就不得出现在解释性注释里;要指代就用散文。**
- [Phase 08]: [Phase idi-08]: **一处必须留档的自省:这条缺陷的证据在 wave 1 就已经出现过,是我读漏了。** wave 1 的 T3 探针实测到「菜单已隐藏 + 选区非折叠 + 焦点在 #round-doc ⇒ 一次 keyup 就让菜单重开」,我在当时把它判为「我的探针构造了一个不可能持续的状态」并结案 —— 那个判断**对 T3 的问题本身成立**,但我没有追问下一步:*如果任何 keyup 都能重开菜单,那么 Escape 的交还把焦点送进 #round-doc 之后会发生什么?* 该追问正是本缺陷。**教训:探针报出「不符合预期」时,「我的探针错了」与「实现错了」可以同时成立** —— 前者解释观测不到的原因,后者解释为什么这个观测**能**发生。只结前者就会把真缺陷留到下一波。**佐证:wave 3 的执行器用捕获阶段事件日志独立复现了同一机制,与 wave 1 的观测逐字一致。**
- [Phase 08]: [Phase idi-08]: **上一条「已修复」的结论不完整 —— 代码评审(CR-01)判定那次修复只覆盖了一次按键,判定正确,已在 `09b170d` 重做。** 旧修法用 `{capture:true, once:true}` 抑制「紧随 Escape 的那一次 keyup」,但它守护的状态(菜单已隐藏 + 选区仍存活 + 焦点已交还 #round-doc)**活得比一次 keyup 长**;`once` 的额度还会被**任意**按键的 keyup 花掉。动手前先独立复现,四条路径实测全部把菜单弹回来,只有单次 Escape 通过:**S2** 连按两次 Escape(奇偶次来回开关)、**S3** Escape 后按任意方向键、**S5** 按住 Shift 时按 Escape 且**先松 Shift**(额度被 Shift 的 keyup 花掉)、**S6** 滚轮关掉菜单后按任意键(**全程没有 Escape 参与**)。**根因不是抑制器**:#round-doc 既有的 keyup 处理器只要「选区非折叠且落在 #round-doc 内」就弹菜单,而只读容器里方向键**不改变**选区 —— 这个处理器此前是死代码,正是本阶段的 `tabindex="0"` 让它第一次活起来。
- [Phase 08]: [Phase idi-08]: **重做的修法与一条只有插桩才能看见的第二缺陷。** 修法:**登记「被关掉的那份选区」**(`dismissedSelectionRange`),keyup 进 `handleSelectionTrigger` 之前先比对**选区身份**(不是按键)—— 选区真的变了就自清放行,故**不订阅任何事件、不依赖任何时序**。**评审给的两个选项里只有一个是合法的**:其「durable」方案 (a) 要给 `handleSelectionTrigger` 加按键过滤/关闭标记,而 **D-06 明文禁止按键白名单进入该函数、且其函数体整段在 Do-Not-Touch 名单上** —— 故只能走 (b) 在它**之前**拦截,它的函数体一字未动。**第二缺陷(评审未发现,插桩才发现):** `hideSelectionMenu()` 被**每一个 scroll 事件**调用,而它自己的 `roundDoc.focus()` 就可能触发一次滚动 ⇒ 紧接着第二次调用,此时 `menuSelection` 已被置 null,**把刚登记的关闭态覆写成「无」**。这解释了「单独跑 S5 通过、放在序列里跑就失败」—— 失败只在焦点移回 #round-doc **真的滚动了页面**时出现。修法:**只在「可见 → 隐藏」那一次登记**(`wasVisible` 判据)。**可复用的教训:把「只在状态真的发生变化时记账」当作默认,重复调用必须幂等** —— 本项目的 `hideSelectionMenu` 是 scroll 监听的目标,天然会被高频重入。
- [Phase 08]: [Phase idi-08]: **本轮同时修掉评审的 1 条 Warning + 3 条 Info,并明确不改 2 条。** 已修:**WR-01**(Shift 提交手势在无关的 Shift 抬起时夺焦 —— 典型是 Shift+Tab 反向移焦后焦点被从刚到达的控件拽进菜单,而 #selection-menu 在文档序末尾,用户要重新穿过整个侧栏;判据加「焦点仍须在 #round-doc」)、**IN-02**(分派器分支 3 缺 `return`,与分支 1/2 不对称的潜在陷阱)、**IN-04**(注释里「四个调用点」的过期数字 —— 按本项目反复踩的形态**删数字留枚举**)、**IN-05**(输入法组字期间的 Escape 是「取消候选窗」,而 `#confirm-word-input` 收中文、组字是常态 ⇒ 加 `e.isComposing` 放行)。**不改:WR-02**(`.claude/settings.local.json` 的 `Bash(node -e ' *)` 预授权任意代码执行 —— 属实,但删除会同时打断本流水线自身的内联 `node -e` 调用,且其边际风险与**既存**的 `Bash(git *)` 同级;信任边界属仓库所有者,故**上报不擅改**)、**IN-03**(`focus()` 未带 `preventScroll` 可能移动 #doc-panel 滚动位置 —— **实测证伪**:交接前后 scrollTop 均为 67,不复现则不修)。**IN-01** 是措辞冲突:S8-1 授权的 `app.js:1162` 改动落在继承来的 Do-Not-Touch 条目 `renderAnnotations` 之内,用户后来明确裁定过这一处,故以**后者的显式授权**为准(该条目保护的是它的渲染逻辑/DOM 构造,未被动过)。
- [Phase 08]: [Phase idi-08]: **修后复跑 17/17 全绿**(修前 4/6 失败):S1 单次 Escape、S2 连按两次、S2b 第三次(幂等)、S3 Escape+方向键、S4 Escape+Tab(且焦点确实离开菜单)、S5 抬手顺序、S6 滚轮关掉后按键、**S8 D-08 路径(选区真的改变后菜单必须重新弹出 —— 守卫不得过度抑制)**、W1(Shift+Tab 不再夺焦)、N1(交接前后 scrollTop 不变)、R1(F1-a 交还)、R2/R3(两个弹窗仍可 Escape 关闭)、R4(菜单项仍关闭菜单)。门:`check-01/02/03/04` PASS、`check-05 --item 1/4/10` PASS、`check-06` 6 项 PASS、pytest **219 passed / 6 skipped**、`node --check` OK、`style.css` 逐字节未改。**计数门只动了一处**:`window.getSelection` 2 → 3(关闭态守卫必须读一次当前选区才能比对),已按本项目口径更新计划 01 的 `fails_when` 并写明**真判据是「每一处读取都服务于一个具名判据」**而非某个数字。
- [Phase 08]: [Phase idi-08]: **本阶段的探针自身出过两次错,两次都不是实现缺陷,已分别核实。** ①S8 首跑报失败:我的 `arm()` 把选区选到文本节点**末尾**,于是「扩展选区」被 clamp 成 no-op(节点恰 15 字),守卫正确地判定「选区没变」而抑制 —— 改 `arm()` 只选前 8 字后 S8 通过。②`!important` 我一度按 `grep -c` 数到 **5** 而以为违反「唯一 `!important`」,实为**数行而非数声明**:`check-04` 数的是 `!important;`(带分号)**声明**数,恰为 1,另 4 处是注释散文 —— 又一次「计数门是 scope-blind 的」实证。**两次都印证:门报红先逐字复测原命令,再怀疑自己的探针。**
- [Phase 08]: [Phase idi-08]: **阶段验证发现一条我的收口漏掉的缺口,且它是真的:Phase 6 的 L-5 门被本阶段打红。** `check-05 --item 9` 由 `idi-06` 记录的 PASS 转为 **FAIL**(`16 条断言,1 FAIL`,行 `('#round-doc','#doc-panel',-66.6)`),⇒ **ROADMAP Phase 8 的 Gate 行「Phase 4/6/7 全部 gate 仍通过」为假**。**因果链已独立核实**(不是采信验证代理的结论):`FOCUSABLE_SELECTOR` 含 `[tabindex]` 一臂(`check-05-ui-uat.py:1748`),`#round-doc` 是普通 `<div>`、**只在本阶段加了 `tabindex="0"` 才首次进入该判定集**,而 `scripts/check-05-ui-uat.py` 本阶段逐字节未改 ⇒ 断言文本与选择器与阶段前完全一致。**为什么收口没看见:** 计划 03 的 must_haves 把「仍绿」的真值收窄成 `check-01…04`,于是执行器只扫了 item 1/4/10,**item 9 从未重跑** —— 这本身就是相对 ROADMAP Gate 行的范围缩减。
- [Phase 08]: [Phase idi-08]: **我自己先做了一个「结构性不可修」的假设,实测把它推翻了 —— 记下来以免被当成结论。** 我先算:L-5 的 `gap` 是四边取最小,若元素高于容器 padding 盒则 `gap_top+gap_bottom<0` ⇒ 恒负、任何 padding 都救不了。**但实测 `#round-doc` 是 778.64px < 容器 900px**,不是那种情形。真实几何:元素在盒内**顶部偏移 188px**(面板标题行 + 内边距),故默认滚动位(0)下底边越界 **66.64px**;浏览器把元素滚入视野后落到 scrollTop 67,底边**恰好贴边**(clearance **0.36px**)—— 因为 Chrome 把这类元素对齐到滚动口边缘。**且它在某些滚动位是可以达标的**(scrollTop 71 → 4.36px、100 → 33.36px),所以「结构性不可满足」是错的。**真正的性质是:该元素的 clearance 恰在阈值边界上,且其高度由文档内容决定、无上界。** 另注意 0.36px 与 D-02 早先测到的「底边被裁 3.64px」是同一件事的两种读法(4 − 0.36 = 3.64)。
- [Phase 08]: [Phase idi-08]: **用户裁定「改门范围」,已在 `check-05-ui-uat.py` 落地(S8-2 / A-11)。** 做法:`L5_CONTENT_REGION_MIN_RATIO = 0.5` —— 高度 >= 容器 padding 盒**一半**的可聚焦元素是**内容区**,进**声明集**(逐行 `info()` 报出、**不断言**);其余仍断言;**声明集与断言集同时为空时走 `blocked()`**(fail-closed),防止判定集被吃光后退化成空转 PASS。判据取**客观比例**而非元素名清单。`_IDI06_CENSUS_JS` 相应加 `elH` / `padBoxH` 两个字段(纯增量,不触 `hits`)。**落地后 `check-05 --item 9` 复跑 PASS(16 条断言)**,且声明只命中该命中的:p1/checking **0 行**声明,p3 **1 行**(`#round-doc`,778.6/900)。
- [Phase 08]: [Phase idi-08]: **两条变异测试证明新判据既不放水也不误伤**(本项目口径:只有变异测试能证明守卫真的会失败)。**测试 A(不放水)**:注入一个 30px 的贴边控件(clearance 0)⇒ 它落在**断言集**里、断言**仍判 FAIL** ⇒ 声明集没有吞掉真控件。**测试 B(不空转)**:把比例临时设为 `0.0`(全体声明)⇒ item 9 返回 **BLOCKED(16 条断言,0 FAIL,3 BLOCKED)**,**不是 PASS** ⇒ 兜底生效;随后按 `diff` 逐行核对还原(除比例行外与备份逐字节相同)。
- [Phase 08]: [Phase idi-08]: **指纹账:作废 4 份,不是 5 份;且不做重基线。** D-21 / A-4 原写「改 `check-05` 会作废 5 份 live 指纹」,**实测只有 4 份**把该脚本列入 `covered_files`(`idi-04.1` / `idi-05` / `idi-06` / `idi-07`);**`idi-04` 只在正文提到它、未列入 `covered_files`**,故不受影响。**另:`idi-04` 的 `covered_digest` 本就已失配,与本项无关** —— 它的 `covered_files` 含 `frontend/style.css` 与 `.planning/REQUIREMENTS.md`,二者在 `idi-04` 验证(2026-09-20 提交 `812a224`)之后被 Phase 5–8 合法改动。**未做重算/重基线,这是刻意的:** 重算会把 `covered_digest` 刷成当前值,从而断言「自该验证以来覆盖输入无变化」—— 而 `style.css` 确已变化,那是不实陈述;指纹的价值正在于**留下这个信号**。**若要闭合,正确做法是重跑那四个阶段的 verify-work,不是改指纹。** `idi-08` 自身指纹不受影响(其 `covered_files` 不含 `check-05`)。重算工具已验证可信:用 `gsd-tools query verification.fingerprint` 复算 `idi-08` 的 `covered_digest`,与验证代理写入的**逐字节相同**。
- [Phase 08]: [Phase idi-08]: **评审其余条目的最终处置**(用户 2026-09-24 裁定):**WR-02 保留现状** —— `.claude/settings.local.json` 的 `Bash(node -e ' *)` 预授权任意 JS 执行属实,但它的边际风险与**既存**的 `Bash(git *)`(第 13 行,`git -c core.pager=…` 同样可执行任意命令)同级,且删除会打断本流水线自身的内联 `node -e` 调用 ⇒ 作为**信任边界**保留,已登记而非静默。**IN-01** 是措辞冲突:S8-1 授权的 `app.js:1162` 落在继承来的 Do-Not-Touch 条目 `renderAnnotations` 之内,以**用户后来的显式授权**为准(该条目保护其渲染逻辑/DOM 构造,未被动过)。**IN-03 实测证伪**(交接前后 `#doc-panel.scrollTop` 均为 67),不复现则不修。

### Pending Todos

None yet.

### Blockers/Concerns

- [v1.14 P4] ~~规划前必须先答复 ARCHITECTURE.md 向 UI-SPEC 作者提的 7 个未决问题~~ **已关闭(2026-09-17,`24a9abe`)** — 7 个问题全部在 `04-UI-SPEC.md` 的 `## Design Decisions` 中给出裁定(令牌命名与三族切分、不可逆动作处理、字号锚点、`--fw-medium` 不声明、窄窗口范围、`#state-badge` 采 `calc()`、emoji 走 data-URI 内联 SVG)。**取而代之的是四个待用户签核的偏差 S-1…S-4**(见 Operator Next Steps)—— ✅ **已签核(2026-09-17,规划期)**:用户在 `/gsd-plan-phase 4` 呈上四项时**逐项照契约原文批准**(S-1 保留半步带 / S-2 保留 14px / S-3 接受 `#ccc`→`#8a8a8a` / S-4 删除冻结轮 opacity 改用结构性标记)。四项的一行式替代方案**均不执行**;S-1/S-2 是超越已锁 TOKEN-05 / TOKEN-08 字面的授权依据。签核为 planning 期用户决定,不是 checker 裁定。
- [v1.14 P8] 五条 b9664e0 修复无自动化覆盖,而本里程碑重写其依赖的 CSS;`.hidden { display: !important }` 是 5 路单点故障
- [v1.14 全局] gate 算术陷阱:`grep -c '!important' frontend/style.css` 返回 3(其中 2 行是 L13-14 注释散文),而声明数必须为 1——写 gate 时按"声明"计数
- [v1.14 P4] ~~idi-04-01 的人工 DevTools Computed 检查与冻结轮 backstop 真值尚未执行~~ **已执行(2026-09-19,`cc11e9f`)** — `scripts/check-05-ui-uat.py` 把 6 项全部自动化并实跑。**已闭合(2026-09-20):6/6 pass** —— 当时的 3 fail 是 260918-qrq 令牌值漂移造成的**假 FAIL**,已由 04.1 的 D-14(断言改令牌接线)+ D-10(值层重写)结构性消解;本阶段实跑 item 1/2/3/4/6 全 PASS(0 FAIL / 0 BLOCKED),item 5 的 2 BLOCKED 是需真实 AI 调用的冒烟(已用 `--ai-smoke` 补齐并 PASS)。**结果 3 pass / 3 fail** 为历史记录:
  - **PASS**:① SC4 `.hidden` 实检(38 断言,含 3 个 1-0-0 竞争者);② 冻结轮 backstop(`inset 3px 0 0 rgb(138,101,8)` / `opacity 1` / `filter saturate(0.6)` / 正文对比度 19.44:1);⑥ CR-06(两侧均为运行时 `--color-text-muted`)
  - **FAIL**:③④⑤ 共 20 条断言失败。**根因单一**:UAT 期望值定稿于 `0c658aa`(2026-09-17),其后 `448686b`「令牌值层换血」(属 quick 260918-qrq)改动了令牌值——`--gray-600 #6a6a6a→#8f8f8f`、`--gray-500 #8a8a8a→#d9d9d9`、`--blue-700 #1f63bd→#3a83f7`、`--gray-900 #1a1a1a→#0d0d0d`、`--gray-25 #fafafa→#ffffff`、字号 13/14/15/16→14/16/18/24,并删除 `.overlay-card` box-shadow 与 `#state-badge` z-index。**不是新缺陷,是「UAT 期望值 vs HEAD 现状」差异待裁**;已按 YAML 写入 UAT `## Gaps` 供 `/gsd-plan-phase --gaps` 消费。待裁:更新 UAT 期望值,或回退令牌值(注:令牌颜色族已定于 v1.14 重写为 Radix Colors,该裁决将随之消解)
  - **S-2 依赖 PASS**:`--text-base` = 14px 存活(Phase 5 SC5 / Phase 6 SC5 的下游门仍可满足)
  - **UAT 里「本环境无法自动化」的三条理由,两条被证伪**:screenshots 可用(`channel` 与 headless 策略见 `scripts/check-05-ui-uat.py` 头部注释),DevTools computed-style 有等价物(`getComputedStyle`)。**「键盘文本选区无法自动化」仍成立**,保留
- [v1.14 P4] ~~**对比度 AA 倒退(真实,新发现)**:`--color-text-muted` = `#8f8f8f` 在 `#ffffff` 上 **3.23:1**~~ **已结构性解决(2026-09-20,Phase 04.1)** — Radix 重写后 `--color-text-muted: var(--radix-gray-11)`,实测 `check-02-contrast.py`:`5.62 --color-text-muted on --color-surface` / `5.77 … on --color-surface-page` / `5.19 … on --color-surface-sunken` / `5.82 … on --color-surface-warning-subtle`,脚本 exit 0。与 260918-qrq 的 check-02 14 条失败同源,一并消解
- [v1.14 P4] ~~**阶段 3 的「发送」按钮不可点(功能缺陷,新发现)**~~ **已修复(2026-09-19,`1d849b1`)** — 根因与 D1/D2 同源:`app.js` **从未引用过** `#session-panel`(grep 零匹配;`git log -S` 证明是长期 bug,非 260918-qrq 引入),而 `style.css:566` 的 `flex: 1 1 auto` 让它吃掉主区全部剩余高度。修复 = 在 `applySessionGates`(`app.js:343`,唯一必经派发点)加一行 `classList.toggle('hidden', !isSessionPhase)`。**实测五个样本:`p1=flex` / `p12=flex` / `p3=` / `checking=` / `archive=`**。`.hidden` 靠 `style.css:238` 的 `!important` 压过 `display:flex`,**无需改 CSS**;`style.css`/`index.html` 零改动。守卫经 RED→GREEN 实证非空转(修前 3 条 `FAIL expected=actual=flex`)
- [v1.14 P7] **UI 审计(19/24)的三条既有缺陷已转 backlog `999.2`**(用户 2026-09-23 裁定):①`#session-panel .panel-header` 有 `cursor: pointer` 却无点击行为(文件自己的惯例对另两个面板显式复位);②`.annotation-answer summary` 无 `:hover`/`:active` 且不在过渡挂载规则里,更关键的是**三个样本都没有 fixture 渲染 `<summary>`**,故 item 10 的普查从未见过它——「已覆盖」是名义的;③焦点环的 PAIR 清单漏 `--color-surface-warning-subtle`(`.verdict-card` 的底色,环在其上实测 5.77:1 达标),与本文件自订纪律「a token drawn as a UI boundary must have its own NON-TEXT pair on each ground it is drawn on」直接冲突,而兄弟令牌 `--color-border-hover` 正是按该纪律补上了这处底色。**修 999.2 会作废 `idi-07` 的 `passed` 指纹**(`frontend/style.css` 与 `scripts/check-05-ui-uat.py` 都在其 `covered_files` 里),须连带重新验证。
- [v1.14 P7] **`phase.complete` 的 STATE.md 字段异常第三次复现**(`completed_phases` 4→1、`percent` 67→17,进度条同步退化)。已注册的 `tech-debt`,不会自愈;判据一律取 ROADMAP 的 `## Milestones` + `## Progress`。**注意 `state.json` 的 `phases` 数组本次是正确的**(1-7 全 complete、8 pending),错的只有 STATE.md 的派生计数——不要把 `state.json` 当判据来源。
- [v1.14 P7] **归档半场的焦点环断言仍无服务对象**(五个样本 `#round-doc` 内 `a[href]` 计数为 0)。已按 `accept` 登记于 `idi-07-SECURITY.md` 的 Accepted Risks Log;一次性反事实探针 `scripts/probe-07-focus-composite.py` 承担可外推性。**Phase 8 给 `#round-doc` 加 `tabindex="0"` 后该场景变为活体,届时须复跑该探针**。
- [v1.14 P8] **同一派生计数缺陷第四次复现,且本次的触发者是新动词。** Phase 8 的 discuss 收口跑 `state.record-session` 后,`progress.completed_phases` 从 **5 改回 1**、`percent` **83 → 17**(进度条同步退化)。**新增三条事实**:①`state.record-session` 也会触发(此前只记录了 `phase.complete` 与 `state.update-progress`);②**`state.sync` 会把它改得更差**(17% → 13%,且不动 `completed_phases`),`state.rebuild --dry-run` 报 `Nothing to rebuild`(它的推导源已经同意那个错值)⇒ **三个动词(`sync` / `rebuild` / `record-session`)都不能作为修正手段**;③**它是确定性的,不是偶发** —— 同一次会话里 ui-phase 收口再跑一次 `record-session`,同样把 5/83% 改回 1/17%,两次逐字一致。已按 ROADMAP 的 `## Progress` 校正为 **5 / 83%**(两次都校正了)。判据仍取 ROADMAP 的 `## Milestones` + `## Progress`,不从 `state.json` 的 `phases` 推(本次 `state.json` 的 `phases` 数组依然正确:1-8 全 complete、8 pending)。
- [v1.14 P8] **第五次复现,触发者是 `state.planned-phase`,且破坏面比前四次宽。** 前四次的症状都是 `completed_phases` 被改回 1(连同 `percent`);**本次 `completed_phases` 反而是对的(5),错的是 `total_phases`** —— 它写 **8**(数的是阶段**编号** 1..8,把 v1.13 的三个阶段并进了 v1.14 作用域的分母),而 `completed_phases: 5` 只数 v1.14 的五个 ⇒ 两者不同源,`percent` 被算成 **63**(5/8),ROADMAP 真值 83%(5/6)。**同一批写入里 `total_plans` 的 18 → 21 是正确的**(纯增量,作用域一致)—— **⇒ 该 handler 的增量型字段可信、比值型字段不可信,判据仍取 ROADMAP。** 本次还**删除了四个已声明的 schema 字段**:`current_phase` / `current_phase_name` / `last_activity_desc`(`state-md-schema.cjs:102/106/198`)与 `state_head`(`:205`,契约是 `preservation: derive`、注释明写「**Never preserved**: a stale stamp would claim STATE.md was written against a commit it wasn't」——即每次写入都应**重算**,不是删除),并把 `gsd_state_version: "1.0"` 的引号去掉(把 `type: 'string'` 的字段变成 YAML 浮点 1.0),另在正文两处列表中间插入空行。**均已手工修复并复跑核盘**(`git show 41a2f52`)。**方法论结论:`state.*` 的写入没有一个是可信的,动词清单又长了(`planned-phase`),且失败模式会随动词变化(改值 / 改分母 / 删字段),所以核盘不能只比对 `percent` 一个数——须逐字段对照写入前的快照。**
- [v1.14 P8] **`gsd-tools gap-analysis` 对本项目结构性地看不见 CONTEXT 裁定**(与 `[Phase idi-07]` 的 `ui.safety-gate` 失明同族,必须留档)。它按字面文件名找 `${PHASE_DIR}/CONTEXT.md`,而本项目全阶段的命名是 `NN-CONTEXT.md`(实测 `08-CONTEXT.md` / `07-CONTEXT.md` 皆是),故走「CONTEXT.md missing → REQUIREMENTS-only report」的降级分支:输出里 **0 条 D-ID 行**,却不报错、不提示 —— 一份「26 条裁定全部未覆盖」的报告和一份「裁定根本未被检查」的报告长得一模一样,后者还会以 `✓` 的形态误导。另:它的 REQUIREMENTS 匹配是**全里程碑、按子串**的,不分阶段也不看覆盖语义 —— 本次它把 `REG-02` 记成 `✓ Covered`(只因 `idi-08-03-PLAN.md` 提到该 id 作为回归门引用,而 REG-02 早在 `260917-fqh` 就已完成,根本不在 Phase 8 范围内),同时把其余 30 条已完结阶段的需求列为 `✗ Not covered`。**⇒ 该步非阻塞,但它的输出不可作为判据;决策覆盖率须自跑阶段级核盘**(本次用 `grep -ho 'D-[0-9][0-9]' *-PLAN.md | sort -u` 逐 id 对照 `08-CONTEXT.md` 的 D-01…D-26,得 26/26)。
- [v1.14 P8] **Phase 8 的 CONTEXT 已落盘**(`idi-08-accessibility-semantics-and-keyboard/08-CONTEXT.md`,D-01…D-26)。三条会改变下游行为的裁定:①**两个阻塞弹窗按实测换成 `#confirmation-modal` + `#tier-modal`**(路线图点名的 `#permission-modal` 可 Tab 出去、不卡;真正卡死的是无取消按钮且不移焦的 `#tier-modal`);②**键盘划词的提交手势 = 抬起 Shift**(路线图字面「keyup 分支移焦」会让键盘用户只能选中一个字符,而验收项仍会假绿);③**焦点环沿用整盒环、`style.css` 零改动** ⇒ Phase 8 在 D-01 路径下**不欠任何验证指纹**(`frontend/app.js` / `index.html` 不在任何 live 报告的 `covered_files` 里)。
- [v1.14 P8] **同一派生计数缺陷第六次复现,本次是「三动词连击」,且 `update-progress` 是传播者而不是修正者。** `idi-08-01` 收口序列逐段实测:`state.advance-plan` 把 `completed_phases` **5 → 1**、`percent` **83 → 17**(与第 1-4 次同症状);紧接着 `state.update-progress` **没有**从磁盘重算,而是拿那个已被污染的 `completed_phases` 算 `percent = 1/6 = 17` 并回写 —— **它把错值固化了**(前四次只记录了它「把进度往回改」,没记它「不回算」);最后 `state.record-session` 再把它压到 **`completed_phases: 0` / `percent: 0` / 进度条 `[░░░░░░░░░░] 0%`** ⇒ **该字段不是被写成某个固定错值,而是被逐步推向 0,即 `record-session` 的破坏是累加式的**(第 4 次记录的是 5→1,本次同一次会话内 1→0)。**同批写入中正确的部分(照第 5 次的方法论结论:增量型可信、比值型不可信):** `completed_plans` 18 → 19 ✅、`total_plans: 21` 未动 ✅、`state.record-metric` 正确追加 `Phase idi-08 P01 | 8 min | 3 tasks | 2 files` ✅、`roadmap.update-plan-progress idi-08` 正确写 `1/3 | In Progress` ✅、`requirements.mark-complete A11Y-02 A11Y-03` 只改 4 行(2 复选框 + 2 追溯行)无越权 ✅。已按 ROADMAP 的 `## Progress` 手工校正为 **5 / 83%**(判据:ROADMAP 表格 v1.14 作用域 6 阶段中 5 个 Complete)。**⇒ 收口序列里唯一可信的判据仍是 ROADMAP;`state.*` 的四个动词(`advance-plan` / `update-progress` / `record-session` / `planned-phase`)在这一条上全部不可信,且 `update-progress` 不可作为修正手段 —— 它会用坏值重算。**

- [v1.14 P8] **第七次复现(2026-09-24,`idi-08-02` 收口)。** 本次序列:`state.advance-plan` 把 `completed_phases` **5 → 0**、`percent` **83 → 0**(首次一步到 0;前六次是先到 1 再被压到 0);`state.update-progress` 随后回显 `{"percent": 0, "completed": 20, "total": 21, "bar": "[░░░░░░░░░░] 0%"}` —— **它仍然不重算**,直接用被污染的 `completed_phases` 算出 0 并回写(与第六次逐字同症状);`state.record-session` 把进度条固化为 `[░░░░░░░░░░] 0%`。**同批写入中正确的部分:** `completed_plans` 19 → 20 ✅、`total_plans: 21` 未动 ✅、`state_head` 正确重算为 `2a75ba1`(preservation: derive 的契约被遵守,未像第五次那样删除字段)✅、`Plan: 2 of 3 → 3 of 3` ✅、`state.record-metric` 正确追加 `Phase idi-08 P02 | 12min | 3 tasks | 2 files` ✅、五条 `state.add-decision` 全部落盘且不越权 ✅、`roadmap.update-plan-progress idi-08` 正确写 `2/3 | In Progress` ✅、`requirements.mark-complete A11Y-05 A11Y-06` 只改 4 行(2 复选框 + 2 追溯行)无越权 ✅、`state.json` 的 `phases[8].status: pending → in_progress` 正确 ✅。已按 ROADMAP 的 `## Progress` 手工校正为 **5 / 83%**(判据:ROADMAP 表格 v1.14 作用域 6 阶段中 5 个 Complete),并把 `state.json` 的 `next.reason` 从 `0%` 改回 `83%`。**⇒ 与第六次的方法论结论逐条一致,无需新增结论;本条的增量事实只有一条:「一步到 0」的形态也存在,故核盘判据不能写成「期望看到 1」。**
- [v1.14 P8] **Escape 无法关闭划词菜单 —— 本阶段引入的功能缺陷,已登记、未修复,待用户裁定。** 症状:菜单打开、焦点在 `#btn-annotate`、轮次文档内有非折叠选区时,按 Escape 后菜单**重新弹出**。机制已用 capture 阶段事件日志钉死:`keydown` 的目标是 `btn-annotate` ⇒ 分派器关闭菜单并把焦点交还 `#round-doc`(F1-a)⇒ **`keyup` 到达时目标已变成 `round-doc`**,命中既有的 `roundDoc` keyup 绑定 ⇒ `handleSelectionTrigger` 守卫全过 ⇒ `showSelectionMenu()`。三条判别性对照:T2 焦点在菜单外 ⇒ 保持关闭;T3 选区已折叠 ⇒ 保持关闭;T4 完全不按 Escape、只按任意键 ⇒ 菜单重现。两条腿都是本阶段新增(计划 02 的分派器 + 计划 01 的交还),故为本阶段引入。打破的契约:D-08、`idi-08-UI-SPEC.md` §K-2.6 第 6 步、REQUIREMENTS 的「A11Y-03 键盘划词部分」人工验收项(「Escape 关闭并交还焦点」的后半不成立)。**未修的两个理由**:①计划 03 的计划级 `<verification>` 明写「本计划只改一处文案」,修它就证伪计划级验证;②正确修法是至少三种形态的设计选择(新监听器抑制后续 keyup / 推迟 F1-a 交还 / 把交还搬出共享挂点),而 keyup 落入的 `handleSelectionTrigger` 函数体本身在不得触碰清单上 ⇒ Rule 4。完整证据见 `idi-08-03-SUMMARY.md` §Newly discovered finding。
- [v1.14 P8] **同一派生计数缺陷第八次复现,但本次的失效形态是新的:不是改错值,而是「静默什么都不做」。** `idi-08-03` 收口序列:`state.advance-plan` 走 `last_plan` 分支返回 `{"advanced": false, "reason": "last_plan", "current_plan": 3, "total_plans": 3, "status": "ready_for_verification", "updated": []}` —— **`updated: []`,它一个字都没写**。根因已定位(`state-transition.cjs:1328-1337`):该分支用 `stateReplaceFieldIfTemplate` 写 `Status: Phase complete — ready for verification`,而该 helper **只在当前值等于模板默认值时才替换**;本项目的 `## Current Position` 早已把 `Status:` 定制成 `Executing Phase idi-08`,于是两次替换都是 no-op,而函数仍返回 `status: ready_for_verification` 让人以为写成功了。⇒ **前七次是「改错值」,本次是「假报成功 + 零写入」;核盘判据必须同时覆盖「值对不对」与「到底写没写」。** 同批写入中正确的部分:`completed_plans` 20 → 21 ✅、`total_plans: 21` 未动 ✅、`state_head` 正确重算为 `fa7813a` ✅、`state.record-metric` 正确追加 `Phase idi-08 P03 | 16min | 3 tasks | 1 files` ✅、六条 `state.add-decision` 全部落盘 ✅、`state.record-session` 正确写 `Stopped at: Completed idi-08-03-PLAN.md` ✅、`roadmap.update-plan-progress idi-08` 正确写 `3/3 | In Progress` ✅、`requirements.mark-complete A11Y-08 REG-03` 只改 4 行(2 复选框 + 2 追溯行)无越权 ✅。**错误的部分:`state.update-progress` 把 `completed_phases` 5 → 0、`percent` 83 → 0、进度条 → `[░░░░░░░░░░] 0%`**(它仍然不重算,直接用被污染的 `completed_phases` 算 0 并回写)。已按 ROADMAP 的 `## Progress` 手工校正为 **5 / 83%**(判据:ROADMAP 表格 v1.14 作用域 6 阶段中 5 个 Complete;Phase 8 在 `roadmap.update-plan-progress` 后是 `3/3 | In Progress`,尚未 Complete),并把 `## Current Position` 的 `Status:` 按该分支的意图手工写成 `Phase complete — ready for verification`。**附:`gsd-tools windows append` 本次被拒**(`Ledger table … disagrees with the fenced JSON entries … for row id(s): 17`,与派发说明预警的既有不一致一致),三条应入账的条目(Escape 缺陷 / 自检视图零高度 Tab 停靠点 / 两条 REG-02 门与六条人工项都不是常驻守卫)已改记于 `idi-08-03-SUMMARY.md` 与 STATE.md,未与该文件相争。

### Quick Tasks Completed

| # | Description | Date | Commit | Directory |
|---|-------------|------|--------|-----------|
| 260916-t8g | 修复 UI 审计报告 5 条功能性 BLOCKER(.hidden 全局规则 / SSE 断流可见化 / 归档只读态加固 / 键盘划词路径 / 错误内联) | 2026-09-16 | 0912429 | [260916-t8g-ui-5-blocker-hidden-sse-onerror](./quick/260916-t8g-ui-5-blocker-hidden-sse-onerror/) |
| 260917-fqh | 修复 b9664e0 自身引入的两条缺陷(.hidden 注释理由错误 / 错误内联提示被挤成 flex 窄列)并补齐视图切换时不清除内联错误 | 2026-09-17 | 793071e | [260917-fqh-b9664e0-hidden-flex](./quick/260917-fqh-b9664e0-hidden-flex/) |
| 260918-qrq | 信息架构对调(会话流入主区、文档区变可折叠右栏)+ ChatGPT 视觉语言换肤 + DESIGN.md §4.1/§4.2 修订。check-02 按用户知情决策红着交出(14 条失败) | 2026-09-18 | 65536dd | [260918-qrq-frontend-chatgpt](./quick/260918-qrq-frontend-chatgpt/) |
| 4 | 260918-qrq 后续修正:会话流撑满主区(composer 贴底)+ 空态 :has()/:empty 居中问候 + 文档面板收窄至 480px + 修「进入」按钮换行 | 2026-09-18 | 253d4d3 | — |
| 260919-0h3 | 建立前端验证 harness(`scripts/check-05-ui-uat.py` + `scripts/ui-states/` 5 个磁盘状态样本 + `requirements-dev.txt`),跑掉 idi-04 UAT 6 项。**结果 3 pass / 3 fail**——FAIL 全部是 260918-qrq 令牌值漂移(UAT 期望值定稿于 `0c658aa`,其后 `448686b` 换了令牌值层),非新缺陷;已按 YAML 写入 UAT `## Gaps` | 2026-09-19 | cc11e9f | [260919-0h3-harness-idi-04-uat-6](./quick/260919-0h3-harness-idi-04-uat-6/) |
| 260919-1w1 | **P6 前置修正**:`#session-panel` 在阶段 3+ 该隐藏却从未隐藏(DESIGN.md §4.1/§4.2 明文「切换」非「叠加」)。一次修掉 D1(主区 90% 空白)/ D2(归档态与阶段5 仍渲染输入框)/ 发送按钮被批注流覆盖不可点 三个症状。harness 加五态显隐守卫,经 RED→GREEN 实证非空转 | 2026-09-19 | 1d849b1 | [260919-1w1-session-panel-3-d1-d2](./quick/260919-1w1-session-panel-3-d1-d2/) |

### Roadmap Evolution

- Phase 04.1 inserted after Phase 4: Radix 颜色族重写

## Deferred Items

Items acknowledged and deferred at milestone close, most recent first:

| Category | Item | Status | Deferred At | Milestone |
|----------|------|--------|-------------|-----------|
| known-limitation | 已归档阶段的 `covered_digest` 不可解析:`covered_files` 声明 `.planning/phases/...` 路径,归档后移至 `.planning/milestones/v1.13-phases/`,重算返回 `null`(fail-closed=stale)。归档后的阶段报告不再被 staleness 机制消费,故记为已知限制而非回填重算 | acknowledged | 2026-09-14 | v1.13 |
| tech-debt | `SdkAICaller.abort` 在 CLI 已挂死时无法杀掉孤儿 SDK 子进程(磁盘侧「无脏状态」语义仍成立)— PROJECT.md 已登记 | acknowledged | 2026-09-14 | v1.13 |
| tech-debt | `annotations` append 与 writeback 存在毫秒级交错窗口(模块级锁可收口)— PROJECT.md 已登记 | acknowledged | 2026-09-14 | v1.13 |
| tech-debt | STATE.md 在 `phase.complete` 后偶发字段异常(`completed_phases` 计数、By-Phase 表重复、进度条 0%),需人工修正 — PROJECT.md 已登记 | acknowledged | 2026-09-14 | v1.13 |
| tool-defect | `phase.complete` 释放 `milestone.lock` 时按 `normalizePhaseToken` 匹配,锁内存 `idi-03`、完成时传 `3`,两者不匹配 → 释放 no-op,锁只能等 4h TTL 自然过期(过期后惰性无害,不影响新会话 claim)。GSD 工具侧问题,非本项目代码 | acknowledged | 2026-09-14 | v1.13 |
| housekeeping | `.planning/tmp/`(GSD scratch)与 `.planning/milestone.lock`(机器相关瞬时 claim)曾被 git 跟踪,已解除跟踪并 gitignore;物理文件留存盘上 | resolved | 2026-09-14 | v1.13 |

## Session Continuity

Last session: 2026-09-24T06:15:08.951Z
Stopped at: Completed idi-08-03-PLAN.md
Resume file: None

## Operator Next Steps

- **当前待办(一条):** **`/gsd-plan-phase 8`** —— `idi-07`(交互状态与焦点样式)已收口:UAT 1/1 pass(唯一人工项 D-17 的 5″ 经用户确认)、`idi-07-VERIFICATION.md` `status: passed`(8/9 机器 + 1 具名人工)、`threats_open: 0`、Nyquist 0 缺口、UI 审计 19/24。
  - **本阶段收口时的两条登记(不阻断 Phase 8):**
    1. **`phase.complete` 的 STATE.md 字段异常第三次复现。** 本次把 `progress.completed_phases` 从 **4 改回 1**、`percent` **67 → 17**(进度条同步退化)。成因与 idi-05 那次逐字相同(见本文件 `## Deferred Items` 的 `tech-debt` 行与下方第 1 条的注),已按 ROADMAP 的 `## Progress` 校正为 **5 / 83%**。`total_plans` / `completed_plans`(18/18)与 `Total plans completed`(31)本次**正确**,未越权翻需求(`requirements_updated: false`)。**判据一律取 ROADMAP 的 `## Milestones` + `## Progress`,不从 `state.json` 的 `phases` 推。**
    2. **UI 审计的三条既有缺陷已转 backlog `999.2`**(用户 2026-09-23 裁定):`#session-panel .panel-header` 的假 `cursor: pointer`、`.annotation-answer summary` 无交互态且普查从未见过它、焦点环 PAIR 清单漏 `--color-surface-warning-subtle` 底色。**注意:修 999.2 会作废 `idi-07` 的 `passed` 指纹**(`frontend/style.css` 与 `scripts/check-05-ui-uat.py` 都在其 `covered_files` 里),须连带重新验证 idi-07。
- ~~**当前待办:规划 Phase 5**~~ **已完成** —— `idi-05` 的 3 个计划(`idi-05-01` / `idi-05-02` / `idi-05-03`)全部执行完毕,各有 SUMMARY。
- **当前待办(一条):**
  1. ~~**`/gsd-verify-work idi-05`**~~ **已收口(2026-09-21,`/gsd-execute-phase idi-05 --gaps-only`)** —— 计划 04 关闭 BLOCKER `G-idi-05-1`,verifier 独立复核报 9/9 must-haves `passed`;`phase.complete` 已执行(ROADMAP Phase 5 → `Complete 2026-09-21`,REQUIREMENTS 的 8 条阶段行已翻)。收口后两条门(`check-05 --item 7` / `check-06`)已在 post-complete 树上复跑,仍绿。**注:本次 `phase.complete` 未越权翻需求(`requirements_updated: false`),但把 `progress.completed_phases` 从 2 改回 1、`percent` 33 → 17 —— 已按 ROADMAP 的 `## Progress` 校正为 3 / 50%。**
  2. **`/gsd-verify-work idi-04.1-radix`** —— **D-05 的连带义务,本计划已把输入备齐但未写指纹**。`idi-04.1-radix` 的 `covered_digest`(`v1:sha256:25d5f1fe…`)因 `frontend/style.css` 与 `scripts/check-05-ui-uat.py` 被 wave 1/2/3 改写而 **stale**;成因是**内容真变**,故走**重新验证**而非补指纹。重算后的全部数值与逐条核对结果见 `idi-05-03-SUMMARY.md` 的「D-05 复验记录」节(`ORDER 0.363` 不变 / `--color-text-info ON --color-surface-info` 4.53 逐字不变 / `--color-border-strong` 3.24+3.15 逐字不变 / 冻结轮 `opacity 1` + `filter saturate(0.6)` + `inset 3px 0 0` 琥珀 逐字不变 / tier-1 25 不变、tier-2 47 → **48**、清单 43 → **47**)。**`idi-04.1-VERIFICATION.md` 一字未改**(`git status --porcelain` 为空)。
- ~~04.1 的上游三步路线~~ **已走完(2026-09-20)** —— discuss → ui-phase → plan → execute → verify 全程完成,4/4 计划交付,`idi-04.1-UAT.md` 3/3 pass。
- ~~**当前待办:Phase 4 的复验收口**~~ **已收口(2026-09-20)** —— `/gsd-verify-work idi-04` 完成:
  - 旧报告指纹 stale 成因为**内容真变**(04.1 重写了它覆盖的 `frontend/style.css` 值层,实测 `f4dd04b6…` → `cd9aa761…`),故走**重新验证**而非补指纹:新 `idi-04-VERIFICATION.md` 对 HEAD 逐条重核,`14/15`、`behavior_unverified: 0`,全部数值从 HEAD 重算(`ORDER 0.363`、43 对、`--color-text-muted` `rgb(100,100,100)` 5.62)。
  - UAT 6 项全部与报告的人工项一一对应并复现(除第 5 项两次需真实 AI 调用的冒烟,沿用已记录的 `--ai-smoke` 证据)。
  - 复核中发现一条**阶段后引入**的新缺口:`frontend/style.css:434` `.collapse-indicator { font-size: 20px; line-height: 1; }`(由 quick `260918-qrq` / `3684353` 在 Phase 4 收口后引入)。**用户裁定为 Phase 4 范围外**,以 `overrides:` 落证并指派到 backlog **`999.1`**(连同 `check-05-ui-uat.py:588` 的陈旧诊断文案)。TOKEN-08 因此标为 `Complete (PARTIAL — …)`。
  - `phase.complete` 已跑:ROADMAP Progress 表 Phase 4 → `Complete 2026-09-20`;REQUIREMENTS.md 的 Phase 4 需求行随之翻转。两份报告(idi-04 / idi-04.1)的指纹因 `REQUIREMENTS.md` 被改而重算一次,各自在报告内披露。
- **~~当前待办:规划 Phase 5~~ 已执行** —— `idi-05`(排版与视觉层级)3/3 计划完成,待 `/gsd-verify-work idi-05` 收口。Pitfall 7 把触碰 `.collapse-indicator` 的范围锁死为两处 `content:` emoji(本阶段已把这两处换成 mask 字形),而 backlog `999.1` 的第 1 项是该元素的 `font-size` —— 两者未互相覆盖,`.collapse-indicator` 逐字节与 HEAD 相同。
  以下 S-1…S-4 签核项仍然有效(04.1 明令不改 S-1/S-2),规划器/执行器不得重新讨论,也不得执行任何一行式替代方案:
  - **S-1** ✅ 批准:间距刻度保留 12 档,含 1/2/6/10/14 五个非 4px 倍数档(TOKEN-05 的七档是子集而非上限;压平会移动像素、违反 SC2)
  - **S-2** ✅ 批准:保留 14px 为一级字号档(7 档而非字面 6 档;删除会同时打破 Phase 5 SC5 与 Phase 6 SC5)
  - **S-3** ✅ 批准:控件边框 `#ccc` → `#8a8a8a`(10 处;本阶段最大视觉变更,依据 SC 1.4.11)
  - **S-4** ✅ 批准:冻结轮删除 `opacity: 0.55`,改用 `filter: saturate(0.6)` + 琥珀色 `box-shadow: inset` 结构性标记(替代路线 opacity 0.65 会使 Phase 7 焦点环在冻结态降至 2.85:1、低于 3:1 非文本下限)

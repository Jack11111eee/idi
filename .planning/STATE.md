---
gsd_state_version: "1.0"
milestone: v1.14
milestone_name: 前端视觉与可访问性
current_phase: 07
current_phase_name: 交互状态与焦点样式
status: executing
stopped_at: Completed idi-07-02-PLAN.md
last_updated: "2026-09-23T06:31:08.029Z"
last_activity: 2026-09-23
last_activity_desc: Phase idi-07 execution started
state_head: aa7194b41d01e6a3d4d2f88d17efe7a9132425db
progress:
  total_phases: 6
  completed_phases: 4
  total_plans: 18
  completed_plans: 17
  percent: 67
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-09-21)

**Core value:** 未经用户明确授权,流程绝不进入"撰写总设计文档"步骤;文档通过自检提示「使命完成」即为终点(只读归档态)。
**Current focus:** Phase idi-07 — 交互状态与焦点样式

## Current Position

Phase: idi-07 (交互状态与焦点样式) — EXECUTING
Plan: 3 of 3
Status: Executing Phase idi-07
Last activity: 2026-09-23 — Phase idi-07 execution started

Progress: [███████░░░] 67%

## Performance Metrics

**Velocity:**

- Total plans completed: 28
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
- [Phase idi-07]: **`ui.safety-gate` 的 halt 经项目所有者预授权为已知假阳性(2026-09-23,执行期)**。该门判据为 `block = frontend && hasUiFiles && !hasUiSpec`,只读**最后一次提交**的 `git diff HEAD~1..HEAD`。Phase 7 的 `frontend=true`(ROADMAP 带 `**UI hint**: yes`)、`hasUiSpec=false`(无 `idi-07-UI-SPEC.md`),故 `block` 退化为 `hasUiFiles`;wave 2 / wave 3 的末次提交都改 `frontend/style.css` ⇒ 该门会 halt。**判为假阳性的依据:** 同能力的确定性门 `ui.plan-gate` 对本阶段返回 `block: false`,因为它的判据多一个 `hasFrontendEvidence`(需要带 UI 框架依赖的 `package.json`)——本仓库是 Python + 原生 HTML/JS,该信号恒为 false;两个门用不同谓词,`ui.safety-gate` 不咨询该信号。本阶段的契约面是 `07-CONTEXT.md` 的 D-01…D-20 + `idi-07-PATTERNS.md`,且 `idi-07-03-PLAN.md:71` 的 D-11 明文**禁止**新建 UI-SPEC 文件(`不得为了凑齐三处而新建 UI-SPEC 文件`)。故执行期不生成 UI-SPEC、不修改本阶段任何计划,该 halt 记录在案后放行。**该门另有一处已知结构性缺陷同案登记:** 它只看 `HEAD~1..HEAD`,故 wave 1(Task 1/2 改 `style.css`、Task 3 只改 `check-05`)会因末次提交无 UI 文件而 `hasUiFiles=false` 静默放行 —— 门绿并不代表它看过本波的 UI 改动
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

### Pending Todos

None yet.

### Blockers/Concerns

- [v1.14 P4] ~~规划前必须先答复 ARCHITECTURE.md 向 UI-SPEC 作者提的 7 个未决问题~~ **已关闭(2026-09-17,`24a9abe`)** — 7 个问题全部在 `04-UI-SPEC.md` 的 `## Design Decisions` 中给出裁定(令牌命名与三族切分、不可逆动作处理、字号锚点、`--fw-medium` 不声明、窄窗口范围、`#state-badge` 采 `calc()`、emoji 走 data-URI 内联 SVG)。**取而代之的是四个待用户签核的偏差 S-1…S-4**(见 Operator Next Steps)—— ✅ **已签核(2026-09-17,规划期)**:用户在 `/gsd-plan-phase 4` 呈上四项时**逐项照契约原文批准**(S-1 保留半步带 / S-2 保留 14px / S-3 接受 `#ccc`→`#8a8a8a` / S-4 删除冻结轮 opacity 改用结构性标记)。四项的一行式替代方案**均不执行**;S-1/S-2 是超越已锁 TOKEN-05 / TOKEN-08 字面的授权依据。签核为 planning 期用户决定,不是 checker 裁定。
- [v1.14 P8] 五条 b9664e0 修复无自动化覆盖,而本里程碑重写其依赖的 CSS;`.hidden { display: none !important }` 是 5 路单点故障
- [v1.14 全局] gate 算术陷阱:`grep -c '!important' frontend/style.css` 返回 3(其中 2 行是 L13-14 注释散文),而声明数必须为 1——写 gate 时按"声明"计数
- [v1.14 P4] ~~idi-04-01 的人工 DevTools Computed 检查与冻结轮 backstop 真值尚未执行~~ **已执行(2026-09-19,`cc11e9f`)** — `scripts/check-05-ui-uat.py` 把 6 项全部自动化并实跑。**已闭合(2026-09-20):6/6 pass** —— 当时的 3 fail 是 260918-qrq 令牌值漂移造成的**假 FAIL**,已由 04.1 的 D-14(断言改令牌接线)+ D-10(值层重写)结构性消解;本阶段实跑 item 1/2/3/4/6 全 PASS(0 FAIL / 0 BLOCKED),item 5 的 2 BLOCKED 是需真实 AI 调用的冒烟(已用 `--ai-smoke` 补齐并 PASS)。**结果 3 pass / 3 fail** 为历史记录:
  - **PASS**:① SC4 `.hidden` 实检(38 断言,含 3 个 1-0-0 竞争者);② 冻结轮 backstop(`inset 3px 0 0 rgb(138,101,8)` / `opacity 1` / `filter saturate(0.6)` / 正文对比度 19.44:1);⑥ CR-06(两侧均为运行时 `--color-text-muted`)
  - **FAIL**:③④⑤ 共 20 条断言失败。**根因单一**:UAT 期望值定稿于 `0c658aa`(2026-09-17),其后 `448686b`「令牌值层换血」(属 quick 260918-qrq)改动了令牌值——`--gray-600 #6a6a6a→#8f8f8f`、`--gray-500 #8a8a8a→#d9d9d9`、`--blue-700 #1f63bd→#3a83f7`、`--gray-900 #1a1a1a→#0d0d0d`、`--gray-25 #fafafa→#ffffff`、字号 13/14/15/16→14/16/18/24,并删除 `.overlay-card` box-shadow 与 `#state-badge` z-index。**不是新缺陷,是「UAT 期望值 vs HEAD 现状」差异待裁**;已按 YAML 写入 UAT `## Gaps` 供 `/gsd-plan-phase --gaps` 消费。待裁:更新 UAT 期望值,或回退令牌值(注:令牌颜色族已定于 v1.14 重写为 Radix Colors,该裁决将随之消解)
  - **S-2 依赖 PASS**:`--text-base` = 14px 存活(Phase 5 SC5 / Phase 6 SC5 的下游门仍可满足)
  - **UAT 里「本环境无法自动化」的三条理由,两条被证伪**:screenshots 可用(`channel` 与 headless 策略见 `scripts/check-05-ui-uat.py` 头部注释),DevTools computed-style 有等价物(`getComputedStyle`)。**「键盘文本选区无法自动化」仍成立**,保留
- [v1.14 P4] ~~**对比度 AA 倒退(真实,新发现)**:`--color-text-muted` = `#8f8f8f` 在 `#ffffff` 上 **3.23:1**~~ **已结构性解决(2026-09-20,Phase 04.1)** — Radix 重写后 `--color-text-muted: var(--radix-gray-11)`,实测 `check-02-contrast.py`:`5.62 --color-text-muted on --color-surface` / `5.77 … on --color-surface-page` / `5.19 … on --color-surface-sunken` / `5.82 … on --color-surface-warning-subtle`,脚本 exit 0。与 260918-qrq 的 check-02 14 条失败同源,一并消解
- [v1.14 P4] ~~**阶段 3 的「发送」按钮不可点(功能缺陷,新发现)**~~ **已修复(2026-09-19,`1d849b1`)** — 根因与 D1/D2 同源:`app.js` **从未引用过** `#session-panel`(grep 零匹配;`git log -S` 证明是长期 bug,非 260918-qrq 引入),而 `style.css:566` 的 `flex: 1 1 auto` 让它吃掉主区全部剩余高度。修复 = 在 `applySessionGates`(`app.js:343`,唯一必经派发点)加一行 `classList.toggle('hidden', !isSessionPhase)`。**实测五个样本:`p1=flex` / `p12=flex` / `p3=none` / `checking=none` / `archive=none`**。`.hidden` 靠 `style.css:238` 的 `!important` 压过 `display:flex`,**无需改 CSS**;`style.css`/`index.html` 零改动。守卫经 RED→GREEN 实证非空转(修前 3 条 `FAIL expected=none actual=flex`)

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

Last session: 2026-09-23T06:31:07.943Z
Stopped at: Completed idi-07-02-PLAN.md
Resume file: None

## Operator Next Steps

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

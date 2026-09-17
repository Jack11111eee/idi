---
gsd_state_version: "1.0"
milestone: v1.14
milestone_name: 前端视觉与可访问性
current_phase: 4
current_phase_name: v1.14 第 1/5 阶段
status: planning
stopped_at: Phase 4 UI-SPEC approved (checker APPROVED; UI-consideration probe resolved)
last_updated: "2026-09-17T08:57:15.197Z"
last_activity: 2026-09-17
last_activity_desc: "完成 quick 260917-fqh:修复 b9664e0 自身引入的两条缺陷(REG-01/REG-02)"
state_head: 24a9abefa7e1f7b1dab521e8ab02adc785f2b14a
progress:
  total_phases: 5
  completed_phases: 0
  total_plans: 0
  completed_plans: 0
  percent: 0
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-09-17)

**Core value:** 未经用户明确授权,流程绝不进入"撰写总设计文档"步骤;文档通过自检提示「使命完成」即为终点(只读归档态)。
**Current focus:** v1.14 前端视觉与可访问性 — 路线图已创建(Phases 4-8),待规划 Phase 4(v1.13 已 shipped 并归档)

## Current Position

Phase: 4 of 8 (设计契约、令牌层与契约校验) — v1.14 第 1/5 阶段
Plan: 0 of TBD in current phase
Status: UI-SPEC approved — ready to plan
Last activity: 2026-09-17 — Phase 4 UI-SPEC 通过 checker(APPROVED)并经 UI-consideration 探针裁定(79 条:4 resolved / 1 backstop / 13 deferred / 61 dismissed),提交 `24a9abe`

Progress: [░░░░░░░░░░] 0%

## Performance Metrics

**Velocity:**

- Total plans completed: 13
- Average duration: -
- Total execution time: 0 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. 行走骨架 | 4 | - | - |
| 2. 轮次收敛循环 | 4 | - | - |
| 3. 授权、自检与终点 | 5 | - | - |

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

### Pending Todos

None yet.

### Blockers/Concerns

- [v1.14 P4] ~~规划前必须先答复 ARCHITECTURE.md 向 UI-SPEC 作者提的 7 个未决问题~~ **已关闭(2026-09-17,`24a9abe`)** — 7 个问题全部在 `04-UI-SPEC.md` 的 `## Design Decisions` 中给出裁定(令牌命名与三族切分、不可逆动作处理、字号锚点、`--fw-medium` 不声明、窄窗口范围、`#state-badge` 采 `calc()`、emoji 走 data-URI 内联 SVG)。**取而代之的是四个待用户签核的偏差 S-1…S-4**(见 Operator Next Steps)
- [v1.14 P8] 五条 b9664e0 修复无自动化覆盖,而本里程碑重写其依赖的 CSS;`.hidden { display: none !important }` 是 5 路单点故障
- [v1.14 全局] gate 算术陷阱:`grep -c '!important' frontend/style.css` 返回 3(其中 2 行是 L13-14 注释散文),而声明数必须为 1——写 gate 时按"声明"计数

### Quick Tasks Completed

| # | Description | Date | Commit | Directory |
|---|-------------|------|--------|-----------|
| 260916-t8g | 修复 UI 审计报告 5 条功能性 BLOCKER(.hidden 全局规则 / SSE 断流可见化 / 归档只读态加固 / 键盘划词路径 / 错误内联) | 2026-09-16 | 0912429 | [260916-t8g-ui-5-blocker-hidden-sse-onerror](./quick/260916-t8g-ui-5-blocker-hidden-sse-onerror/) |
| 260917-fqh | 修复 b9664e0 自身引入的两条缺陷(.hidden 注释理由错误 / 错误内联提示被挤成 flex 窄列)并补齐视图切换时不清除内联错误 | 2026-09-17 | 793071e | [260917-fqh-b9664e0-hidden-flex](./quick/260917-fqh-b9664e0-hidden-flex/) |

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

Last session: 2026-09-17T08:57:15.180Z
Stopped at: Phase 4 UI-SPEC approved (checker APPROVED; UI-consideration probe resolved)
Resume file: /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md

## Operator Next Steps

- Plan the first v1.14 phase: `/gsd-plan-phase 4` — UI-SPEC 已就绪并通过 checker(APPROVED),7 个未决问题已全部关闭,不再是规划前置。
  **规划时须先向用户呈上四个签核项 S-1…S-4**(见 `04-UI-SPEC.md` 的 `## Sign-Off Items`),它们是契约刻意不替用户做的决定:
  - **S-1** 间距刻度偏离 TOKEN-05 的字面七档(保留 1/2/6/10/14 半步带;压平会移动像素、违反 SC2)
  - **S-2** 字号锚点偏离 TOKEN-08 的"删除 14px"(保留 14px;删除会同时打破 Phase 5 SC5 与 Phase 6 SC5)
  - **S-3** 控件边框 `#ccc` → `#8a8a8a`(本阶段最大视觉变更,来源是研究调和范围而非编号需求,留有退出口)
  - **S-4** 冻结轮裁定:保留结构性标记(删 opacity);改用 opacity 0.65 亦可,代价是 Phase 7 焦点环在冻结态降至 2.85:1、低于 3:1 非文本下限

# 交互式讨论迭代系统(Interactive Discussion Iteration)

## What This Is

一个本地运行的 Web 工具,把"AI 项目开工前的讨论、细化、对齐"做成固定流程:想法进、无歧义的总设计文档出。单机、单人、本地运行,讨论文档以中文为主。**唯一权威设计文档为项目根 `DESIGN.md`(v1.13 收口版),本文件及 `.planning/` 全部为实施辅助视图,冲突时以 DESIGN.md 为准。**

## Core Value

未经用户明确授权,流程绝不进入"撰写总设计文档"步骤——总设计文档通过自检、界面提示「使命完成」即为终点(只读归档态)。

## Current Milestone: v1.14 前端视觉与可访问性

**Goal:** 把前端从"零设计契约下长出来的功能骨架"变成有设计契约、键盘可用、视觉可信的工具界面。

**Target features:**
- **设计令牌体系** — 颜色/间距/字号/圆角四类 CSS 自定义属性 + 语义色分层,收掉 32 个硬编码 hex 与"0 个变量"的现状
- **视觉层级** — G3 授权按钮的不可逆动作权重(现与例行「继续自检」视觉完全相同)、页面级层级(现全屏最大字是容器标签 `<h1>文档区</h1>`)、侧栏面板活动态、emoji 图标替代
- **排版系统** — 字号阶梯(现 7 个字号、13px 用了 14 次)、字重层级(现仅 600/400 两档)、markdown 正文字号受控(现 `.markdown-body h1/h2/h3` 无 font-size 规则,落到浏览器默认)
- **可访问性** — 全站 `:focus` 样式(现 grep 命中 0)、键盘可达性(`tabindex` 与 focus 样式必须一起定)、4 处 WCAG AA 对比度失败
- **布局稳健性** — `#state-badge { right: 448px }` 魔法数、420px 侧栏内 4 个滚动容器套娃、窄窗口不破版
- **交互状态** — hover/active/disabled/transition(现为 2/0/8/1)

**Source:** 六支柱 UI 审计 13/24、7 个 BLOCKER(`.planning/milestones/v1.13-phases/idi-03-g3/03-UI-REVIEW.md`)。其中 5 条功能性 BLOCKER 已于 2026-09-16 修复并合入 main(`b9664e0`);本里程碑收的是被显式延后的部分——延后理由一致:修法本身就是设计决策,必须先定契约再落地。

## Requirements

### Validated

- ✓ 行走骨架(阶段 1-2 全链路:进入/会话/发散/G1/恢复/权限门/双轨 AICaller/中止)— Phase 1
- ✓ FLOW-01/02/03/06、UI-03、AI-01~05 共 10 条需求 — Phase 1(见 .planning/milestones/v1.13-phases/idi-01-1-2/01-VERIFICATION.md,8/8 真值 + UAT 6/6)
- ✓ 轮次收敛循环(划词批注/大白话即时答/处理本轮批注 G2/轮次冻结/批注回应回写/§6.4 机器文法全解析)— Phase 2
- ✓ FLOW-04/07、UI-01/02/04、DATA-01 共 6 条需求 — Phase 2(见 .planning/milestones/v1.13-phases/idi-02-g2/02-VERIFICATION.md,7/7 SC + UAT 7/7 零 gap)
- ✓ 授权、自检与终点(G3 四处机械校验 + 确认词、DESIGN.md.tmp 原子落盘、宽松/严格自检两角色自动循环、D-22 残余裁决、崩溃自愈、使命完成只读归档)— Phase 3
- ✓ FLOW-05、DATA-02/03/04 共 4 条需求 — Phase 3(见 .planning/milestones/v1.13-phases/idi-03-g3/03-VERIFICATION.md,5/5 ROADMAP 判据 + UAT 8 检查点,4 处运行时缺陷修复后复验 passed)

**全部 20 条需求(DESIGN.md v1.13 全范围)已交付并验证。**

### Active

**v1.14 前端视觉与可访问性** — 需求清单见 `.planning/REQUIREMENTS.md`(由 `/gsd-new-milestone` 定义)。范围来源为 UI 审计的延后项,不含新功能。

v1.13 范围内工作已全部交付(旧的 v1.13 需求清单已归档至 `.planning/milestones/v1.13-REQUIREMENTS.md`)。

### Out of Scope

见 DESIGN.md §1.5 与 REQUIREMENTS.md 的 Out of Scope 表——写代码实施本工具之外的功能、多项目并行、多人协作、云端部署、批注以外的文档编辑、AI 生成中途插话(v2 再议)。

## Context

- **设计已完成:** DESIGN.md v1.13,由 22 条已确认决策(D-01~D-22)、4 轮讨论(docs/discuss-round-0~4.md)、14 轮自检核查(docs/DESIGN-check-1~14.md)收敛而来。第 14 轮为 PASS 收口。
- **为什么存在:** 用 AI 做项目最大的浪费是"开工前没对齐"。本工具把对齐流程产品化。
- **唯一权威:** 一切入 implement 细节以 DESIGN.md 为准;`.planning/` 文档若与 DESIGN.md 冲突,DESIGN.md 胜出。
- **当前代码状态(v1.13 shipped, 2026-09-13):** 13,322 LOC(不含 vendor);Python + FastAPI 后端(`backend/` 15 个测试文件,219 passed / 6 skipped),原生 HTML/JS 前端(`frontend/`,仅 vendored `marked.min.js`);SSE 事件直播 + 双轨 AICaller(SDK / 子进程);纯模块 `grammar.py`/`annotations.py`/`g3.py`/`checks.py` 承载全部 §6.4 文法与磁盘签名逻辑。
- **已知技术债:** ①`SdkAICaller.abort` 在 CLI 已挂死时无法杀掉孤儿 SDK 子进程(磁盘侧"无脏状态"语义仍成立);②`annotations` append 与 writeback 存在毫秒级交错窗口(模块级锁可收口);③STATE.md 在 `phase.complete` 后偶发字段异常(需人工修正)。
- **方法论教训:** 真浏览器 UAT 抓出了机器级验证漏掉的 6 处真实缺陷(含一处高危无界自动链);文本级 gate 通过不等于运行时语义成立(详见 `.planning/RETROSPECTIVE.md`)。
- **前端设计债(v1.14 的处理对象):** v1.13 的前端在**零设计契约**下建成——`DESIGN.md` §4 只规定了布局区域与交互语义,未规定任何间距刻度、字号阶梯、颜色令牌、断点或文案契约。2026-09-16 的六支柱审计给出 13/24,7 个 BLOCKER。对一个自称价值是"无歧义对齐"的工具而言,2435 行 UI 无设计契约本身就是结构性缺口。
- **UAT 环境事实(省得重踩):** Playwright 必须用 `chromium.launch({ channel: 'chrome' })`,捆绑版 chromium 版本对不上;键盘文本选区**无法自动化**(连 `contenteditable` 都选不中),依赖 Shift+方向键的验收项必须标注为人工检查。

## Constraints

- **Tech stack**: Python + FastAPI 后端,原生 HTML/JS + markdown 渲染库前端,Claude Agent SDK 首选(子进程 `claude -p --output-format stream-json` 兜底,两路线界面契约一致) — DESIGN.md D-06/D-01/§9,不得更换
- **Runtime**: 单机单人本地运行,无云端 — D-03
- **AI 调用前提**: 本机已装 claude CLI 并登录,启动时自检 — D-19
- **数据**: 纯 Markdown + JSON 落盘,"文件即状态",工具不维护独立流程状态,一切由磁盘现状推导(§7) — D-19
- **语言**: 讨论文档以中文为主;面向用户的输出遵守 DESIGN.md §3.8 语言红线(简洁精准、大白话定义术语)
- **Scope**: 代码实施不在本工具职责范围内(工具产出设计文档后归档;本仓库的"实施"是把这个工具本身建起来)
- **Git**: 实施分支活动按仓库 CLAUDE.md 第 5 条纪律执行

## Key Decisions

既有 22 条决策(D-01~D-22)已定案于 DESIGN.md §11 附录,此处不重复维护。实施期新增决策追加于下表:

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 实施框架选用 GSD Core 1.13.0(open-gsd) | 五步循环 Discuss→Plan→Execute→Verify→Ship 与本项目"先讨论后动手"哲学同构;DESIGN.md 22 条决策直接充当 Discuss 阶段输入 | ✓ Good |
| GSD 安装为 local 模式(.claude/ 入库) | 项目自含,依赖可追溯;用户全局 gitignore 对 `**/.claude/` 有忽略,已 `git add -f` 破例入库 | ✓ Good |
| Phase 1:SDK/子进程两路线均强制 setting_sources=[](SDK)/--setting-sources=(CLI) | 用户全局 ~/.claude/settings.json 的 Write(*)/Bash(*) allow 规则会在权限回调前自动放行、绕过 §5.4 权限门;屏蔽来源不掩蔽 auth(环境变量级) | ✓ Good(实测双路线权限矩阵 9/9) |
| Phase 1:/api/abort 会话接线 = session.busy() 时优先 session.abort() | Plan 03 把 caller 挪进 session 后路由需跟随;dev/ping 探针的 _current_caller 路径保留 | ✓ Good(路由级测试 + UAT 实证) |
| Phase 1:会话后门控刷新走 GET /api/session 端点 + applySessionGates/renderTranscript 拆分 | done 后原地刷新 g1_available/divergence_available 门控,不重渲染 transcript(避免清掉刚流完的气泡,且 [ai] 落盘晚于 done) | ✓ Good(UAT G-idi01-7 复测) |
| Phase 1:app.js 脚本移到 body 末尾(#cli-check-overlay 之后) | DOM 先于脚本执行,CLI 自检浮层才能真跑(原顺序 recheckBtn 为 null 抛 TypeError) | ✓ Good(UAT G-idi01-8 复测) |
| Phase 2:PASS/裁决行文法解析归 P2、消费归 P3 | FLOW-07 措辞"文法全部由工具可靠解析" + ROADMAP 判据 6 明确 P2 验期;解析器(backend/grammar.py)P2 交付,Phase 3 按钮逻辑消费 | ✓ Good(47 live 边界抽检) |
| Phase 2:ask_lite 同步调用、事件不进工作面板 | §3.4"数秒内…"不打断阅读 + 单机单人;走 SSE 直播面板的是用户驱动的批处理任务(§4.3),轻量问答不属此列 | ✓ Good(UAT 真调 55s 灰斜体秒级感) |
| Phase 2:冻结 = 纯磁盘推导(轮号 < current_round 即只读),非当前轮批注 API 层拒绝 409 | 不新增后端状态;§7.4 文件即状态的直接推论 | ✓ Good(路由 19 契约 + UAT 冻结检查点) |
| Phase 2:annotations 写回(AI 不碰 JSON)与标记脏变体免疫 | §6.2 字段写回职责——后端解析响应表统一回写 answer/status,格式漂移归零 | ✓ Good(UAT a1-01 回写 answered) |
| Phase 3:裁决行锚点取末一处 `> 核查结论:` + 同号配对 | 宽松档裁决轮报告可含双结论行,锚点取末一处才能让尾部追加段进配对空间;配对与呈现必须共用同一编号空间 | ⚠️ Revisit(G-idi03-2 暴露:anchor 受限扫描与锚点无关扫描曾口径不一,已修) |
| Phase 3:自检自动推进以 hop-local 标志(而非"tmp 在盘")守卫 | 原 `finally` 守卫写反导致严格档无界自动链(实测 84 跳/1.5s);仅当 `tmp_path.replace` 实际执行处置 `tmp_consumed=True` | ✓ Good(修复后恰 1 跳,复验 passed) |
| Phase 3:prompt 契约必须由测试锁死参数注入 | `build_check_prompt` 接受 `tier` 却未注入,AI 写出非法档位行导致 `parse_tier_line` 返回 None——靠真 CLI E2E 才暴露 | ✓ Good(已补 `test_build_check_prompt_injects_tier_line`) |
| Phase 04.1:颜色族换成 Radix Colors 12 步语义刻度(25 primitive / 47 `--color-*` / 43 对清单) | 吸收 idi-04 UAT 的 3 项 FAIL 与 `--color-text-muted` 3.23:1 的 AA 倒退;结构产出(围栏 `:root`、四条守卫)不动,只重写值层 | ✓ Good(`check-01`…`05` 全 PASS;`--color-text-muted` 实测 5.62:1) |
| Phase 04.1:TOKEN-07 的「断言序关系」半场裁定 **manual-only**,不补机械断言 | 实测把四个 `--z-*` 值重排后 `check-01`…`check-05` **全部仍会通过** —— 该不变量只存在于 `style.css:229-231` 的散文注释。用户裁定本阶段不加断言,但 `REQUIREMENTS.md` 的 `Complete` 在机械层面不成立,故降级为 `Complete (PARTIAL)` 并把序关系核对移入人工验收项,不静默调和 | ⚠️ Revisit(Phase 5+ 可补一条 `ORDER` 式断言收口) |
| Phase 04.1:验证报告的 `covered_files` 必须覆盖相位目录内**全部** `*-PLAN.md` / `*-SUMMARY.md` | `verification.cjs:716` 的 `allCurrentArtifactsCovered` 要求逐一声明;idi-04.1-VERIFICATION.md 漏了 `01-PLAN.md`,仅此一项即令 `status=stale`,而指纹本身与记录值逐字节一致 | ✓ Good(补声明 + 重算指纹后 stale→human_needed→passed) |
| Phase 4:阶段**收口后**引入的字面量不算该阶段的偏差,以 `overrides:` 落证而非静默放过 | `style.css:434` `.collapse-indicator { font-size: 20px; line-height: 1; }` 由 quick `260918-qrq`(`3684353`)在 Phase 4 收口(`0c658aa`)后约 20 小时引入;Phase 4 自己的提交区间干净、已交付枚举基线范围。用户裁定为范围外,但**必须留证并指派去向**,否则就是「无人认领的洞」 | ✓ Good(记入 `idi-04-VERIFICATION.md` 的 `overrides:` + `REQUIREMENTS.md` 标 `Complete (PARTIAL)` + backlog `999.1`) |
| Phase 4:stale 的两种成因走**方向相反**的补救,不得混用 | 「内容真变」→ 重新验证(idi-04 的旧报告被取代,全部数值从 HEAD 重算);「记账性编辑」(UAT 状态归一、`phase.complete` 翻需求行)→ 重算指纹并**在报告内披露改了什么、为何不移动任何被核验的事实**。判据是拿 HEAD 内容重算指纹比对,不是看 mtime | ✓ Good(两条路径各自留证,未出现「重新盖章」掩盖内容变更) |
| Phase 4:`REQUIREMENTS.md` 不该进 `covered_files`(待后续裁决) | 它同时存在于 `idi-04` 与 `idi-04.1` 的报告里,而 `phase.complete` **每次收口都会改它** → 任何一次阶段收口都会同时打掉此前所有覆盖该文件的报告(本次收口即打掉两份)。`covered_files` 的语义应是「其变更足以使本报告结论失效的输入」,需求索引表属**下游记账**,不满足该语义 | ⚠️ Revisit(建议移出 `covered_files`,或让 `phase.complete` 的翻转不参与指纹)|

| Phase 5:嵌入标题刻度 = 文档档沿**数值**阶梯下移一档(28→24 / 22→18 / 18→16),逐容器列举而非写全局 `h1,h2,h3` 规则 | 全局裸类型选择器特异性 0-0-1,对四处 chrome 覆盖与 `.markdown-body` 规则都是惰性的,于是「恰好只命中这五个失控容器」——看起来更省事,但无法表达三档各不相同,且会把**任何将来的标题**一并捕获,正是本缺陷(影响面不透明)的成因;枚举还能逐条对照 `app.js` 的调用点 | ✓ Good(G-idi-05-1 关闭;文档 h1 28 > 嵌入 h1 24 由 5 条严格不等式保证,不依赖 fixture 恰好有内容) |
| Phase 5:渲染目标枚举**按 `renderMarkdown()` 调用点**而非按类名,并配一条会失败的静态普查守卫 | 同一类错误在本阶段发作了两次:plan 01 只探一个 `.markdown-body` 宿主,让 chrome 后代选择器的层叠缺陷活到执行期;修法把探针扩到 4 个宿主,但没问等价的反向问题「`renderMarkdown()` 到底注入到哪些容器」——`app.js` 有 10 个调用点 / 9 个目标,只枚举了 4 个 | ✓ Good(守卫比的是两个独立量:app.js 的 token 计数 vs `MARKDOWN_TARGETS` 条数,非自比) |
| Phase 5:`phase.complete` 又一次把 `progress.completed_phases` / `percent` 往回改(2→1 / 33→17),收口后由编排器按 ROADMAP `## Progress` 校正 | 与 `advance-plan` 同一族缺陷(既往已有复现记录)。本次未越权翻需求(`requirements_updated: false`),但进度计数器仍不可信;`state.json` 的 phases 也不是判据来源 | ⚠️ Revisit(编排器每次收口后必须自己核盘并校正) |

---
*Last updated: 2026-09-21 after Phase 5 (排版与视觉层级) — BLOCKER `G-idi-05-1` 关闭(九个渲染目标的嵌入标题刻度 + 按调用点枚举的门);verifier 独立复核 `9/9 must-haves` passed;收口后两条门复跑仍绿;下一阶段为 Phase 6(布局稳健性)*

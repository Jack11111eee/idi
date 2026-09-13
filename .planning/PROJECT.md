# 交互式讨论迭代系统(Interactive Discussion Iteration)

## What This Is

一个本地运行的 Web 工具,把"AI 项目开工前的讨论、细化、对齐"做成固定流程:想法进、无歧义的总设计文档出。单机、单人、本地运行,讨论文档以中文为主。**唯一权威设计文档为项目根 `DESIGN.md`(v1.13 收口版),本文件及 `.planning/` 全部为实施辅助视图,冲突时以 DESIGN.md 为准。**

## Core Value

未经用户明确授权,流程绝不进入"撰写总设计文档"步骤——总设计文档通过自检、界面提示「使命完成」即为终点(只读归档态)。

## Requirements

### Validated

- ✓ 行走骨架(阶段 1-2 全链路:进入/会话/发散/G1/恢复/权限门/双轨 AICaller/中止)— Phase 1
- ✓ FLOW-01/02/03/06、UI-03、AI-01~05 共 10 条需求 — Phase 1(见 .planning/phases/idi-01-1-2/01-VERIFICATION.md,8/8 真值 + UAT 6/6)
- ✓ 轮次收敛循环(划词批注/大白话即时答/处理本轮批注 G2/轮次冻结/批注回应回写/§6.4 机器文法全解析)— Phase 2
- ✓ FLOW-04/07、UI-01/02/04、DATA-01 共 6 条需求 — Phase 2(见 .planning/phases/idi-02-g2/02-VERIFICATION.md,7/7 SC + UAT 7/7 零 gap)
- ✓ 授权、自检与终点(G3 四处机械校验 + 确认词、DESIGN.md.tmp 原子落盘、宽松/严格自检两角色自动循环、D-22 残余裁决、崩溃自愈、使命完成只读归档)— Phase 3
- ✓ FLOW-05、DATA-02/03/04 共 4 条需求 — Phase 3(见 .planning/phases/idi-03-g3/03-VERIFICATION.md,5/5 ROADMAP 判据 + UAT 8 检查点,4 处运行时缺陷修复后复验 passed)

**全部 20 条需求(DESIGN.md v1.13 全范围)已交付并验证。**

### Active

v1.13 范围内工作已全部交付,当前无在办需求。下一里程碑的需求将在 `/gsd-new-milestone` 中重新定义(旧的 v1.13 需求清单已归档至 `.planning/milestones/v1.13-REQUIREMENTS.md`;`.planning/REQUIREMENTS.md` 保留在盘但内容已冻结)。

### Out of Scope

见 DESIGN.md §1.5 与 REQUIREMENTS.md 的 Out of Scope 表——写代码实施本工具之外的功能、多项目并行、多人协作、云端部署、批注以外的文档编辑、AI 生成中途插话(v2 再议)。

## Context

- **设计已完成:** DESIGN.md v1.13,由 22 条已确认决策(D-01~D-22)、4 轮讨论(docs/discuss-round-0~4.md)、14 轮自检核查(docs/DESIGN-check-1~14.md)收敛而来。第 14 轮为 PASS 收口。
- **为什么存在:** 用 AI 做项目最大的浪费是"开工前没对齐"。本工具把对齐流程产品化。
- **唯一权威:** 一切入 implement 细节以 DESIGN.md 为准;`.planning/` 文档若与 DESIGN.md 冲突,DESIGN.md 胜出。
- **当前代码状态(v1.13 shipped, 2026-09-13):** 13,322 LOC(不含 vendor);Python + FastAPI 后端(`backend/` 15 个测试文件,219 passed / 6 skipped),原生 HTML/JS 前端(`frontend/`,仅 vendored `marked.min.js`);SSE 事件直播 + 双轨 AICaller(SDK / 子进程);纯模块 `grammar.py`/`annotations.py`/`g3.py`/`checks.py` 承载全部 §6.4 文法与磁盘签名逻辑。
- **已知技术债:** ①`SdkAICaller.abort` 在 CLI 已挂死时无法杀掉孤儿 SDK 子进程(磁盘侧"无脏状态"语义仍成立);②`annotations` append 与 writeback 存在毫秒级交错窗口(模块级锁可收口);③STATE.md 在 `phase.complete` 后偶发字段异常(需人工修正)。
- **方法论教训:** 真浏览器 UAT 抓出了机器级验证漏掉的 6 处真实缺陷(含一处高危无界自动链);文本级 gate 通过不等于运行时语义成立(详见 `.planning/RETROSPECTIVE.md`)。

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

---
*Last updated: 2026-09-13 after v1.13 milestone — 交互式讨论迭代系统 MVP shipped(3 phases / 13 plans / 28 tasks,20/20 REQ 交付并验证;真浏览器 UAT 抓出 6 处运行时缺陷并全部修复)*

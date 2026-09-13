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

实施 DESIGN.md 全部范围内的功能,详见 `.planning/REQUIREMENTS.md`(REQ-ID 追溯至 DESIGN.md 章节)。

### Out of Scope

见 DESIGN.md §1.5 与 REQUIREMENTS.md 的 Out of Scope 表——写代码实施本工具之外的功能、多项目并行、多人协作、云端部署、批注以外的文档编辑、AI 生成中途插话(v2 再议)。

## Context

- **设计已完成:** DESIGN.md v1.13,由 22 条已确认决策(D-01~D-22)、4 轮讨论(docs/discuss-round-0~4.md)、14 轮自检核查(docs/DESIGN-check-1~14.md)收敛而来。第 14 轮为 PASS 收口。
- **为什么存在:** 用 AI 做项目最大的浪费是"开工前没对齐"。本工具把对齐流程产品化。
- **唯一权威:** 一切入implement细节以 DESIGN.md 为准;`.planning/` 文档若与 DESIGN.md 冲突,DESIGN.md 胜出。

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

---
*Last updated: 2026-09-13 after Phase 3(授权/自检/终点收口:验证 passed 5/5 + UAT 8 检查点,4 处运行时缺陷修复)——milestone v1.13 全 20 需求交付*

# 交互式讨论迭代系统(Interactive Discussion Iteration)

## What This Is

一个本地运行的 Web 工具,把"AI 项目开工前的讨论、细化、对齐"做成固定流程:想法进、无歧义的总设计文档出。单机、单人、本地运行,讨论文档以中文为主。**唯一权威设计文档为项目根 `DESIGN.md`(v1.13 收口版),本文件及 `.planning/` 全部为实施辅助视图,冲突时以 DESIGN.md 为准。**

## Core Value

未经用户明确授权,流程绝不进入"撰写总设计文档"步骤——总设计文档通过自检、界面提示「使命完成」即为终点(只读归档态)。

## Requirements

### Validated

(尚未有——设计已完成,实施待启动)

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

---
*Last updated: 2026-09-09 after GSD new-project --auto (idea document = DESIGN.md)*

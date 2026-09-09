<!-- GSD:project-start source:PROJECT.md -->

## Project

**交互式讨论迭代系统(Interactive Discussion Iteration)**

一个本地运行的 Web 工具,把"AI 项目开工前的讨论、细化、对齐"做成固定流程:想法进、无歧义的总设计文档出。单机、单人、本地运行,讨论文档以中文为主。**唯一权威设计文档为项目根 `DESIGN.md`(v1.13 收口版),本文件及 `.planning/` 全部为实施辅助视图,冲突时以 DESIGN.md 为准。**

**Core Value:** 未经用户明确授权,流程绝不进入"撰写总设计文档"步骤——总设计文档通过自检、界面提示「使命完成」即为终点(只读归档态)。

### Constraints

- **Tech stack**: Python + FastAPI 后端,原生 HTML/JS + markdown 渲染库前端,Claude Agent SDK 首选(子进程 `claude -p --output-format stream-json` 兜底,两路线界面契约一致) — DESIGN.md D-06/D-01/§9,不得更换
- **Runtime**: 单机单人本地运行,无云端 — D-03
- **AI 调用前提**: 本机已装 claude CLI 并登录,启动时自检 — D-19
- **数据**: 纯 Markdown + JSON 落盘,"文件即状态",工具不维护独立流程状态,一切由磁盘现状推导(§7) — D-19
- **语言**: 讨论文档以中文为主;面向用户的输出遵守 DESIGN.md §3.8 语言红线(简洁精准、大白话定义术语)
- **Scope**: 代码实施不在本工具职责范围内(工具产出设计文档后归档;本仓库的"实施"是把这个工具本身建起来)
- **Git**: 实施分支活动按仓库 CLAUDE.md 第 5 条纪律执行

<!-- GSD:project-end -->

<!-- GSD:stack-start source:STACK.md -->

## Technology Stack

Technology stack not yet documented. Will populate after codebase mapping or first phase.
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->

## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->

## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->

## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->

## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:

- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->

<!-- GSD:profile-start -->

## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->

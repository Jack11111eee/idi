# Phase 1: 行走骨架——服务器、单界面与阶段 1-2 会话 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in 01-CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-09
**Phase:** 1-行走骨架
**Areas discussed:** 技术栈与项目结构、AI 集成层、数据与状态、界面
**Mode:** --auto(Claude 按推荐项自动选择;决策源 = DESIGN.md 既有 22 条决策)

---

## 技术栈与项目结构

| Option | Description | Selected |
|--------|-------------|----------|
| FastAPI + 原生 HTML/JS | D-06 定案 | ✓ |
| (其他栈) | 与 D-06 冲突,不考虑 | |

**User's choice:** [auto] 承袭 D-06(DESIGN.md §9)
**Notes:** backend/frontend 目录分工、requirements.txt + venv 均为"最简方案"取向,无争议。

## AI 集成层

| Option | Description | Selected |
|--------|-------------|----------|
| Agent SDK 首选 + CLI 子进程兜底,同一接口两实现 | D-10/§5.3 | ✓ |
| 仅 SDK 单路线 | 违反 D-10 可替换要求 | |
| 仅 CLI 单路线 | 同上 | |

**User's choice:** [auto] 承袭 D-10
**Notes:** SSE 而非 WebSocket(单向推送 + D-20 不做双向);权限门矩阵本阶段全量实现(保护用户文件系统);大白话轻量接口本阶段定义、Phase 2 实现 UI。

## 数据与状态

| Option | Description | Selected |
|--------|-------------|----------|
| derive_state 纯函数全量实现 §7.4 八行表 | 推导表是工具脊柱 | ✓ |
| 本阶段只实现前几行,P3 再补全 | Phase 2/3 按钮逻辑全叠在推导上,晚补风险大 | |

**User's choice:** [auto] 选全量实现
**Notes:** transcript 文法、G1 定稿行为、发散模板要点均按 DESIGN.md 原文。

## 界面

| Option | Description | Selected |
|--------|-------------|----------|
| 单页三文件(index.html/app.js/style.css),无构建 | D-08 单界面 + 最简 | ✓ |
| 引入前端框架 | 与 D-06 冲突 | |

**User's choice:** [auto] 原生三文件
**Notes:** 轮次视图本阶段只做状态占位,划词批注全在 Phase 2——垂直切片优先走通骨架。

---

## Claude's Discretion

- markdown 渲染库选型、FastAPI 路由命名、SSE payload 字段、端口与文案细节

## Deferred Ideas

- 划词批注 / 大白话 UI / G2 循环 / G3 与自检 / 归档态界面 → Phase 2/3(见 01-CONTEXT.md deferred 节)

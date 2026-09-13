# Walking Skeleton — 交互式讨论迭代系统

**Phase:** 1
**Generated:** 2026-09-09

## Capability Proven End-to-End

用户用 `run.sh` 启动本工具、通过 claude CLI 自检后,在浏览器打开单页面、选中一个空项目目录,从右侧工作面板实时看到一次真实 AI 无头调用(每句话、每条工具事件逐条直播);会话与草稿落盘,重启后由磁盘推导恢复。(阶段 1-2 之外的轮次交互不在本骨架内)

## Architectural Decisions

| Decision | Choice | Rationale |
|---|---|---|
| 后端框架 | Python 3.13 + FastAPI + uvicorn(依赖经 `requirements.txt` + venv 管理) | D-P1-1/D-P1-3/D-06;流式推送一等支持 |
| 前端 | 原生 HTML/JS/CSS 单页(`frontend/index.html` + `app.js` + `style.css`),markdown 渲染库 vendored 单文件,无框架、无构建、无路由 | D-P1-14/D-06/D-08 |
| 静态服务 | FastAPI 静态挂载 `/` → `frontend/`,前后端同仓(`backend/` + `frontend/`) | D-P1-2/D-P1-14 |
| AI 调用层 | `AICaller` 抽象接口 + 两个实现:Claude Agent SDK(首选)与子进程 `claude -p --output-format stream-json`(兜底),配置项切换,界面契约一致 | D-P1-5/D-01/D-10 |
| 事件推送 | SSE(Server-Sent Events),单向,不做双向流 | D-P1-7/D-20 |
| 权限门 | §5.4 完整矩阵作为 `AICaller` 内的路由层(放行/拒绝/弹窗三态),弹窗经 SSE + 前端对话框回传 | D-P1-9/§5.4 |
| 状态推导 | 纯函数 `derive_state(path)` 实现 §7.4 八行表(含完整轮判据),文件即状态,无独立流程状态 | D-P1-11/D-19 |
| 数据层 | 纯 Markdown + JSON 落盘(transcript.md 追加式、`[user]`/`[ai]` 文法),无数据库 | D-P1-10/D-19/§6.1 |
| 运行前提 | 启动自检 claude CLI(已装 + 已登录),不满足给指引、只挡第一次 | D-P1-15 收尾/AI-05/§7.1 |
| 目录分离 | 工具源代码 = 本仓库根;工具运行时操作的"项目目录"为用户另选的外部目录,严格分离 | D-P1-4 |

## Stack Touched in Phase 1

- [x] 项目脚手架(venv、requirements.txt、run.sh、backend/ + frontend/ 布局)
- [x] 路由——至少一组真实 API(`/api/health`、目录进入、状态推导、会话、G1 定稿、发散模式)
- [x] 数据落盘——真实读 + 写:transcript.md 追加落盘、draft.md/brainstorm.md 演进、discuss-round-1.md 定稿(纯文件,无 DB——本项目的"数据库"就是磁盘文件)
- [x] UI——至少一个真实交互:目录选择 → 发消息 → 工作面板直播事件流(SSE)
- [x] 运行——`run.sh` 一条本地全栈运行命令(服务器 + 浏览器界面,单机单人,无部署)

## Out of Scope (Deferred to Later Slices)

- 划词批注、大白话即时答、annotations 落盘与回写 → Phase 2(UI-01/02/04、FLOW-04、DATA-01)
- 「处理本轮批注」、G2、轮次冻结视图、§6.4 批注回应表文法 → Phase 2(FLOW-07 相关部分)
- G3 授权门、确认词、AUTHORIZATION.md、DESIGN.md.tmp 原子落盘 → Phase 3(FLOW-05、DATA-02)
- 宽松/严格自检、D-22 残余裁决、崩溃自愈完整判定 → Phase 3(DATA-02/03/04)
- 推导表的完成态/归档分支的界面呈现(推导函数本阶段全量实现) → Phase 3
- 多项目并行、多人协作、云端部署、AI 生成中途插话 → 范围外(§1.5/D-20)
- 大白话轻量调用的**实现** → Phase 2(UI-02);但 AICaller 轻量调用接口本阶段定义,避免 Phase 2 改接口(D-P1-6)
- 轮次视图的完整批注交互 → Phase 2;本阶段仅最小占位(显示推导状态,D-P1-15)

## Subsequent Slice Plan

每个后续阶段在此骨架上叠加一个纵向切片,不改动其架构决策:

- Phase 2: 轮次收敛循环——划词批注大菜单、大白话轻量调用、G2 批量处理、annotations 写回、§6.4 文法解析
- Phase 3: 授权与终点——G3 四处机械校验、确认词、原子落盘、自检档位与循环、只读归档态

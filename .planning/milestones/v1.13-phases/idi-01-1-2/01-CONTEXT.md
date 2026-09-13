# Phase 1: 行走骨架——服务器、单界面与阶段 1-2 会话 - Context

**Gathered:** 2026-09-09
**Status:** Ready for planning
**Mode:** --auto(disicuss-phase 单遍完成;决策源 = DESIGN.md v1.13,22 条已确认决策,非新造)

<domain>
## Phase Boundary

交付 DESIGN.md 范围内的"行走骨架":FastAPI 服务器 + 单一界面 + AI 调用链全程打通。本阶段结束时,用户能:启动应用 → claude CLI 自检 → 选择/输入项目目录 → 按 §7.4 推导出状态 → 走一段完整的阶段 1-2 连续会话(transcript 落盘、可恢复)→ 没想法时走发散模式 → 点「认可雏形」由后端定稿 discuss-round-1.md。划词批注、轮次循环、G3/自检一律不在本阶段(Phase 2/3)。

</domain>

<decisions>
## Implementation Decisions

(全部承袭 DESIGN.md 既有决策 D-01~D-22,auto 模式下逐领域自选推荐/已定项)

### 技术栈与项目结构
- **D-P1-1:** 后端 = Python + FastAPI,前端 = 原生 HTML/JS + markdown 渲染库(引 CDN 或 vendored 单文件库,不引前端框架)。理由:D-06 已定,不可更换。
- **D-P1-2:** 前后端同仓,代码放 `/backend`(FastAPI app)与 `/frontend`(静态文件,由 FastAPI 挂载 serves),不引入 monorepo 工具。理由:单机单人本地工具,最简结构(CLAUDE.md 简单优先)。
- **D-P1-3:** Python 依赖管理用 `requirements.txt` + venv(不引入 poetry/uv 等工具)。理由:依赖面小(claude-agent-sdk、fastapi、uvicorn),最简方案够用。
- **D-P1-4:** 本项目仓库根即工具的源代码仓;工具运行时操作的"项目目录"是用户另选的外部目录,两者严格分离。工具自身的 docs/、DESIGN.md 等讨论产物不被工具运行时触碰。

### AI 集成层
- **D-P1-5:** 首选 Claude Agent SDK(Python),兜底子进程 `claude -p --output-format stream-json`;两条路线实现为同一后端接口(`AICaller`)的两个实现类,界面契约完全一致,由配置项切换。理由:D-10/§5.3,可替换是硬要求。
- **D-P1-6:** 大白话轻量调用**不在本阶段实现**(Phase 2 的 UI-02),但 AICaller 的轻量调用接口在本阶段一并定义,避免 Phase 2 改接口。理由:§3.4 接口契约一致性。
- **D-P1-7:** 事件直播用 SSE(Server-Sent Events),不用 WebSocket。理由:单向服务器→浏览器推送,FastAPI 原生支持,断线重连语义简单;DESIGN.md 明确不做双向流(D-20)。
- **D-P1-8:** 「中止」= 后端终止当前 AI 调用进程/SDK 会话,孤儿半成品由重跑覆盖(本阶段只需保证杀掉无损;完整自愈判定 Phase 3 DATA-02 收口)。
- **D-P1-9:** 权限门按 §5.4 完整矩阵实现为 AICaller 内的路由层(读项目内放行、写 docs/ 与 DESIGN.md.tmp 放行、DESIGN.md/AUTHORIZATION.md 直写拒绝、其余弹窗)。弹窗交互 = SSE 推送到前端 + 用户点同意后放行。理由:§5.4 + D-10;矩阵行为本阶段就要全对,因为它保护的是用户文件系统。

### 数据与状态
- **D-P1-10:** transcript.md 追加式落盘由后端在用户发送 / AI 事件回落时执行,文法 = `[user]`/`[ai]` 起始行独占一行 + 任意多行消息体。理由:§6.1 唯一定义。
- **D-P1-11:** 阶段推导 = 纯函数 `derive_state(path)`,实现 §7.4 八行表(自上而下首条命中),含完整轮判据(末行合规授权标记)。本阶段就要全表实现——它是整个工具的脊柱,Phase 2/3 的按钮逻辑都叠在它上面。理由:文件即状态(D-19)。
- **D-P1-12:** G1 定稿:后端把 draft.md 复制为 docs/discuss-round-1.md,并追加 `> 申请授权:否` 末行;draft.md 本身保留。理由:§4.4 权威定义。
- **D-P1-13:** 发散模式:内置「发散指令模板」作为专用提示词,跑在同一 AICaller 链路,产物 brainstorm.md 可反复覆盖;模板要点按 §3.7(多视角风暴 → 3~5 候选 → 引导挑选)。理由:D-16 四条。

### 界面
- **D-P1-14:** 单页应用,一个 index.html + 一段 app.js + 一个 style.css,不做路由、不做构建步骤。布局按 §4.1:左文档区 / 右侧栏(会话流→轮次批注流、AI 工作面板可折叠)。理由:D-08 单一界面 + D-06 原生前端。
- **D-P1-15:** 阶段 1-2 界面 = 草稿区(draft.md 渲染)+ 会话流(输入框 + 消息列表,来自 transcript)。轮次视图本阶段仅做最小占位(能显示推导状态即可),批注交互 Phase 2。理由:垂直切片——先把骨架走通。

### Claude's Discretion
- markdown 渲染库选型(marked/markdown-it 等任一,CDN 或 vendored 均可)
- FastAPI 路由命名、pydantic 模型字段细节
- SSE 事件 payload 字段命名(但对前端可见,需在本阶段内自洽)
- 服务器默认端口、启动脚本报错文案细节

</decisions>

<specifics>
## Specific Ideas

- 工作面板要展示**全部原始事件**(每条工具调用与结果),"透明优先,兼作调试出口"(D-11)。
- 「认可雏形」按钮**常驻**草稿区末尾(不是弹窗确认式)。
- 语言红线(§3.8)注入每个阶段的 system prompt:简洁精准、术语先大白话定义。
- 后端启动时对 claude CLI 的自检:检查「已装 + 已登录」,不满足给出指引,只挡第一次(§7.1)。

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

- `DESIGN.md` — 唯一权威设计文档(v1.13)。本阶段重点:§4(界面)、§5(AI 集成层全节)、§6.1(transcript 文法)、§7.1/7.4(启动与推导表)、§3.7(发散模式)、§2(用户与场景)、§9(技术栈)
- `DESIGN.md` §5.4 权限矩阵 — 逐行实现依据,含"首条命中即取"规则
- `DESIGN.md` §6.4 机器可解析文法 — 完整轮判据的末行标记规则本阶段用于推导函数
- `docs/discuss-round-3.md` — D-10(无头+直播+权限门)的原始讨论上下文,理解设计意图时参考

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- 无(绿地项目;仓库现有内容是本工具的设计文档与讨论产物,不是代码)

### Established Patterns
- 讨论文档的中文写作风格(§3.8 语言红线)应延续到面向用户的 UI 文案

### Integration Points
- 工具源代码进入本仓库根;注意 `.planning/`、`docs/`、`DESIGN.md`、`CLAUDE.md` 为既有产物,构建配文件与代码目录不得覆盖它们

</code_context>

<deferred>
## Deferred Ideas

- 划词批注与大白话即时答 → Phase 2(UI-01/02)
- 「处理本轮批注」、轮次冻结视图、annotations 回写 → Phase 2(FLOW-04/DATA-01)
- G3 四处校验、确认词、AUTHORIZATION.md、DESIGN.md.tmp 原子落盘 → Phase 3(FLOW-05/DATA-02)
- 宽松/严格自检与 D-22 残余裁决 → Phase 3(DATA-04)
- 状态推导的完成态/归档分支的界面呈现 → Phase 3(推导函数本阶段全量实现,仅界面收口在 P3)

</deferred>

---

*Phase: idi-01-1-2*

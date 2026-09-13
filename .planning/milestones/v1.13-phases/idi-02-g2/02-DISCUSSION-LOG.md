# Phase 2: 轮次收敛循环——划词批注、G2 与机器文法 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in 02-CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-09
**Phase:** 2-轮次收敛循环——划词批注、G2 与机器文法
**Areas discussed:** 阶段边界、划词批注前端、annotations 数据层、大白话轻量调用、G2 处理流水线、§6.4 文法解析器、阶段 3 轮次视图、路由与契约
**Mode:** --auto(Claude 按推荐项自动选择;决策源 = DESIGN.md v1.13 既有章节/决策,非新造)

---

## 阶段边界

| Option | Description | Selected |
|--------|-------------|----------|
| 划词批注 + 大白话 + G2 流水线 + §6.4 解析器 + 轮次视图 | ROADMAP Phase 2 范围字面 | ✓ |
| 把 G3/自检一起做 | ROADMAP 明确划入 Phase 3 | |
| PASS 行/裁决行解析也推给 Phase 3 | FLOW-07 明确"文法**全部**由工具可靠解析"是 Phase 2 判据 | |

**User's choice:** [auto] 按 ROADMAP 字面;边界模糊:PASS 结论行与裁决追加行这两条文法的**解析判定**归本阶段(FLOW-07),其**消费场景**(按钮逻辑)归 Phase 3
**Notes:** 判据 6 原文点名"结论行锚点取末一处、配对同号等边界"要在本阶段构造正反例验证。

## 划词批注前端(UI-01/UI-04)

| Option | Description | Selected |
|--------|-------------|----------|
| 原生 Selection API + mouseup 弹菜单 | §9 表格字面:"划词高亮用浏览器原生选区接口,引框架收益低" | ✓ |
| 引入文本批注专用库(如 annotator.js 类) | 与 D-06/D-P1-1 原生前端冲突 | |
| contenteditable 包裹改写 | 复杂且引入不可控编辑(§1.5 批注以外无编辑能力) | |

**User's choice:** [auto] 原生 Selection API
**Notes:** 阶段 1-2 视图不绑划词(§4.2"此时无划词批注");阶段 4+ 不触达。

## annotations 数据层(DATA-01)

| Option | Description | Selected |
|--------|-------------|----------|
| 独立纯模块 backend/annotations.py(与 state/transcript 同级) | 三模块先例,纯函数零依赖 | ✓ |
| 并进 state.py | state 是推导单一职责,混入读写会破坏取向 | |
| 并进 session.py | session 有锁与线程,纯函数不可测 | |

**User's choice:** [auto] 独立纯模块
**Notes:** 字段严格照 §6.2 一字不差;id 方案 aN-NN 同 DESIGN.md 示例;AI 不直接改写 annotations(后端建条目 + 回写)。

## 大白话轻量调用(UI-02)

| Option | Description | Selected |
|--------|-------------|----------|
| AICaller.ask_lite 双路线各自实现,同一签名(Phase 1 已预定义) | D-01/§5.3"两路线界面契约完全一致" | ✓ |
| 仅 SDK 路线实现 | 违反双轨一致 | |
| 走全量 run() 但换 prompt | §3.4 明确轻量调用"不读全量 docs/、不走逐轮四步" | |

**User's choice:** [auto] 双路线各自实现 ask_lite
**Notes:** 仅携带当前文档 + 划选原文;事件不进工作面板直播;同步请求(秒级,单机单人无并发压力);语言红线照注入;plain 落盘不计入未处理数(D-12)。

## G2 处理流水线(FLOW-04)

| Option | Description | Selected |
|--------|-------------|----------|
| 新 prompt 组装函数 + session.process_round() 照 trigger_divergence 模子;AI 写 round-(N+1),后端解析回应表回写 | §3.3 四步 + §6.2 写回职责 + §5.1 无状态 | ✓ |
| 后端拼新文档(不靠 AI 写) | 与 §4.4/AI-05"AI 产出写回磁盘"冲突 | |
| 处理过程不回写、前端翻新文档自取答案 | 需 AI 直接改 annotations,违反 §6.2 | |

**User's choice:** [auto] AI 写新轮文档 + 后端回写 annotations
**Notes:** 回写按回应表 id 配对,未出现的保持 pending;新文档半成品(末行非合规标记)判不存在,重跑覆盖(§7.3),不新增判错分支。

## §6.4 文法解析器(FLOW-07)

| Option | Description | Selected |
|--------|-------------|----------|
| 独立纯模块 backend/grammar.py,复用 state.py 已有常量 | 授权标记/PASS 前缀 state.py 已实现,不重复造 | ✓ |
| 函数族要零依赖、可单测正反例 | ROADMAP 判据 6 字面 | ✓ |
| AI 产物解析失败由后端修补 | 违反"AI 生成模板逐字遵守 + 重跑覆盖"哲学 | |

**User's choice:** [auto] 独立纯模块 + 正反例测试
**Notes:** 六条文法:维度表/未决清单/授权标记/批注回应表/PASS 结论行(锚点取末一处)/裁决追加行(同号配对、仅统计结论行之后)。历史文档 discuss-round-0~4 不回溯。

## 阶段 3 轮次视图(UI-03 完成 Phase 2 半边)

| Option | Description | Selected |
|--------|-------------|----------|
| 替换 rounds-placeholder:当前轮渲染 + 侧栏批注流 + 旧轮只读可浏览 | §4.2"进入轮次后切换为轮次文档 + 批注流" | ✓ |
| 只做当前轮、不提供旧轮浏览 | §3.5 冻结 = 只读归档(可看不可改),"成为只读归档" | |

**User's choice:** [auto] 完整轮次视图(当前轮 + 旧轮只读浏览)
**Notes:** 冻结 = 纯前端呈现约束(权威 = derive_state 的 current_round);新批注只能挂当前轮(非当前轮 409)。

## 路由与契约

| Option | Description | Selected |
|--------|-------------|----------|
| 新路由族 /api/rounds*(照 main.py 既有风格) | 202/409 语义与 JSONResponse 先例 | ✓ |
| 处理完成推送 SSE 专用事件触发前端刷新 | 自造新机制违反"done 后拉新"既有惯例 | |

**User's choice:** [auto] 路由族 + 前端拉新
**Notes:** XSS:批注内容/AI 回应渲染一律走 renderMarkdown→stripUnsafeNodes 管线或 textContent(Phase 1 T-idi03-02 先例平移)。

---

## Claude's Discretion

- 弹菜单位置样式、跨段落选区截断、轮次切换器控件、新模块函数签名、pydantic 可选性、SSE 事件字段扩展(见 02-CONTEXT.md)

## Deferred Ideas

- G3 全链、自检档位与流程侧、崩溃恢复按钮、归档态、阶段 4/5 界面 → Phase 3(D-20 插话与历史回溯为永久非目标)

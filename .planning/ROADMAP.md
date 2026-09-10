# Roadmap: 交互式讨论迭代系统

## Overview

把 DESIGN.md v1.13 全部范围内的工作拆为三个纵向可交付的阶段:阶段 1 打通"服务器 + 单界面 + AI 调用链"的行走骨架(启动自检、目录进入、阶段 1-2 连续会话、事件直播、发散模式、G1 定稿);阶段 2 建立轮次收敛主循环(划词批注、G2 冻结、机器文法、annotations 写回);阶段 3 收口三道门的后半程与终点(G3 授权原子落盘、宽松/严格自检、D-22 残余裁决制、崩溃自愈与只读归档)。每个阶段结束用户都能用真实项目目录完整走一段端到端流程。唯一权威为项目根 `DESIGN.md`,本文若与之冲突以 DESIGN.md 为准。

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: 行走骨架——服务器、单界面与阶段 1-2 会话** - 启动自检 CLI、选目录进入单界面、状态由磁盘推导、阶段 1-2 连续会话(transcript 恢复)、AI 双轨调用与事件直播、发散模式、G1 认可雏形 (completed 2026-09-09)
- [x] **Phase 2: 轮次收敛循环——划词批注、G2 与机器文法** - 划词批注与大白话双轨、处理本轮批注产出下一轮、上轮冻结只读、§6.4 文法机械校验、annotations 字段写回 (completed 2026-09-10)
- [ ] **Phase 3: 授权、自检与终点——G3、档位、使命完成归档** - G3 四处校验与确认词、DESIGN.md.tmp 原子落盘、宽松/严格自检循环与 D-22 残余裁决、崩溃自愈、完成态只读归档

## Phase Details

### Phase 1: 行走骨架——服务器、单界面与阶段 1-2 会话

**Goal**: 用户打开应用、选中一个项目目录后,能和 AI 走完一段完整的阶段 1-2 会话(含没想法的零起步发散),在草稿区实时看到 AI 每一步动作,点「认可雏形」把草稿定稿为 discuss-round-1.md;重启后一切状态从磁盘完整恢复
**Mode**: mvp
**Depends on**: Nothing (first phase)
**Requirements**: FLOW-01, FLOW-02, FLOW-03, FLOW-06, UI-03, AI-01, AI-02, AI-03, AI-04, AI-05
**Success Criteria** (what must be TRUE):

  1. 启动应用时,本机未装 claude CLI 或未登录则给出指引并只挡第一次进入,装好登录后即可正常使用(其余功能不被反复阻塞) ← AI-05
  2. 用户选择或输入项目目录进入单界面后,界面按磁盘现状自动呈现对的状态(空目录 = 阶段 1 开新讨论;已有 docs/ 或轮次文档 = 接续到对应阶段),不需要任何手工"恢复"操作 ← FLOW-01
  3. 阶段 1-2 会话中用户的每一句话和 AI 的每条回复都实时逐条追加落盘为 docs/transcript.md,杀掉进程重启后,界面从 transcript 恢复出完整上下文继续聊,草稿 draft.md 继续演进 ← FLOW-02
  4. 从用户发送第一条消息起,AI 说的话、每次读写文件、每条命令结果都原始直播到右侧工作面板,点「中止」按钮随时能杀掉当前调用且不留损坏状态 ← AI-02
  5. 新建项目时选「没想法」进入发散模式,多视角风暴产出的 3~5 个候选方向写入 docs/brainstorm.md(可反复覆盖不编号),用户挑选后深化为雏形;一旦雏形存在,发散模式入口关闭 ← FLOW-06
  6. 点「认可雏形」后,后端把当前草稿定稿为 discuss-round-1.md(末尾带合规的 `> 申请授权:否` 标记行),界面切换进入阶段 3 轮次视图 ← FLOW-03
  7. Claude Agent SDK 路线与子进程 `claude -p --output-format stream-json` 兜底路线在界面上行为完全一致、可配置替换,无需改前端 ← AI-01, AI-03
  8. 运行全程权限门按 §5.4 矩阵处置:AI 直写 DESIGN.md 一律拒绝、写 AUTHORIZATION.md 一律拒绝、写项目外/执行命令弹窗征求用户同意 ← AI-04

**Plans**: 4/4 plans executed
Plans:

- [x] idi-01-01-PLAN.md — 行走骨架追踪弹:服务器脚手架 + 双轨 AICaller(SDK/子进程)+ SSE 事件直播 + CLI 自检 + 中止
- [x] idi-01-02-PLAN.md — 状态脊柱:derive_state() §7.4 八行推导表(完整轮判据)+ transcript.md 文法读写
- [x] idi-01-03-PLAN.md — 阶段 1-2 会话闭环:发消息流水线、重启恢复、权限门弹窗、UI-03 视图
- [x] idi-01-04-PLAN.md — 发散模式(brainstorm.md 覆盖落盘)+ G1 定稿(discuss-round-1.md + 授权标记行)

**UI hint**: yes

### Phase 2: 轮次收敛循环——划词批注、G2 与机器文法

**Goal**: 进入阶段 3 后,用户能对轮次文档划词写实质批注(或即时要大白话),点「处理本轮批注」后 AI 批量回应并产出下一轮,被回应的轮次自动冻结只读,四处机械校验所需的文法全部由工具可靠解析
**Mode**: mvp
**Depends on**: Phase 1
**Requirements**: FLOW-04, FLOW-07, UI-01, UI-02, UI-04, DATA-01
**Success Criteria** (what must be TRUE):

  1. 用户划选任意轮次文档中的一段文字弹出小菜单,可选「批注」或「用大白话讲这段」;批注与被选原文绑定(quote + 前 40 字辅助定位)持久落盘,已解决的批注变灰但不消失 ← UI-01
  2. 划词选「用大白话讲这段」后数秒内得到一段灰色斜体的即时回答(仅携带当前文档与划选原文的轻量无头调用),回答落盘为 type=plain 批注且不计入"本轮批注未处理数" ← UI-02
  3. 侧栏实时显示"本轮批注未处理数",文档区有批注的段落有高亮;点「处理本轮批注」后 AI 一次性看到全部批注统一回应,产出 discuss-round-(N+1).md ← UI-04, FLOW-04
  4. 下一轮文档产生后,上一轮的文档与它的 annotations 在界面上变只读不可再批注;新批注只能挂在当前轮上,被批注文本永不变化 ← FLOW-04
  5. 批量处理完成后,界面上上一轮的所有实质批注变成"已回应"状态,AI 回应内容显示在侧栏对应批注旁(后端解析新文档的批注回应表回写 answer 与 status,AI 不直接改写 annotations 文件) ← DATA-01
  6. 工具能按 §6.4 文法机械解析 AI 产出的维度表、未决清单、授权申请标记、批注回应表、PASS 结论行与裁决追加行(构造正反例轮次文档验证解析与判定,含结论行锚点取末一处、配对同号等边界) ← FLOW-07
  7. 目录结构按 §6.1 落盘齐全(transcript/draft/轮次文档/annotations/brainstorm/check 报告),annotations.json 字段与 §6.2 完全一致 ← DATA-01

**Plans**: 4/4 plans executed planned
Plans:
**Wave 1**

- [x] idi-02-01-PLAN.md — 数据脊柱:annotations.py(§6.2 读写+定位)+ grammar.py(§6.4 六条文法解析)+ 正反例测试矩阵

**Wave 2** *(blocked on Wave 1 completion)*

- [x] idi-02-02-PLAN.md — G2 后端全层:ask_lite 双路线、build_round_prompt、process_round 回写、五条轮次路由

**Wave 3** *(blocked on Wave 2 completion)*

- [x] idi-02-03-PLAN.md — 前端轮次视图:划词弹菜单、批注流侧栏、高亮、未处理数、冻结只读

**Wave 4** *(blocked on Wave 3 completion)*

- [x] idi-02-04-PLAN.md — 端到端收口:真 CLI E2E(plain 秒回+新轮回写)+ 7 判据对账 + 人检 UAT 六点

**UI hint**: yes

### Phase 3: 授权、自检与终点——G3、档位、使命完成归档

**Goal**: 收敛达标后用户能走完 G3 授权(默认拒绝、确认词、后端写 AUTHORIZATION.md)、拿到原子落盘的 DESIGN.md、跑宽松或严格档自检直至 PASS 看到「使命完成」,此后项目进入只读归档态;全程任何崩溃中断重开即自愈
**Mode**: mvp
**Depends on**: Phase 2
**Requirements**: FLOW-05, DATA-02, DATA-03, DATA-04
**Success Criteria** (what must be TRUE):

  1. 「授权撰写总设计文档」按钮仅当四处机械校验全过(annotations 无 pending + 未决清单清零 + 维度表全绿 + 授权标记为「是」)才点亮;点击后弹确认框须输入「确认授权」才通过;默认拒绝,拒绝被记为一条普通批注进入下一轮 ← FLOW-05
  2. 授权通过后,AI 写 DESIGN.md.tmp、由后端原子改名为 DESIGN.md 落盘(全程 AI 无法直写 DESIGN.md);撰写或自检中途崩溃,重开界面出现「继续撰写」/「继续自检」按钮,点一下重跑覆盖残留半成品即恢复,无需重新确认词 ← FLOW-05, DATA-02
  3. DESIGN.md 初稿写完后界面弹出宽松/严格档位选择,选择结果记在每份核查报告头部,重开据此恢复档位 ← DATA-04
  4. 宽松档:一次核查 + 修复 + 报告追加 PASS 即止。严格档:核查者/修复者两角色自动循环至零问题轮 PASS 中途无需用户点击;遇纯 P2 轮进入残余裁决制——问题逐条在界面抛给用户裁决「修/接受现状」,修复者抛 `> 待裁决:` 后端截存暂停并落盘磁盘签名,用户裁决落盘后续跑「继续修复」,全部处理完收口 ← DATA-04
  5. 最新 check 报告末行以 `> 核查结论:PASS` 开头时,界面弹出「使命完成」;此后再打开项目呈现只读归档态(轮次/批注/DESIGN.md/核查报告全部可浏览,划词批注、「处理本轮批注」、授权按钮均不可用) ← DATA-03

**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. 行走骨架——服务器、单界面与阶段 1-2 会话 | 4/4 | Complete    | 2026-09-09 |
| 2. 轮次收敛循环——划词批注、G2 与机器文法 | 4/4 | Complete    | 2026-09-10 |
| 3. 授权、自检与终点——G3、档位、使命完成归档 | 0/0 | Not started | - |

# Requirements: 交互式讨论迭代系统

**Defined:** 2026-09-28
**Milestone:** v1.16 界面去卡片化 —— 连续面与发丝分隔线
**Core Value:** 未经用户明确授权,流程绝不进入"撰写总设计文档"步骤——总设计文档通过自检、界面提示「使命完成」即为终点(只读归档态)。

> **REQ-ID 说明:** 本文件只覆盖 v1.16。v1.15 的 12 条需求(CARD / VIS / REG / TABLE / RADIUS)已随里程碑收口归档于 `.planning/milestones/v1.15-REQUIREMENTS.md`。本文件编号自 v1.16 重新起算,与 v1.15 的编号**不构成续号关系**(`REG` 类别在三个里程碑里都出现过,各自独立)。
>
> **本里程碑的性质:反转,不是新增。** v1.15 Phase 9 把界面做成「独立白卡片 + 灰缝 + 页面下沉」,那是**一次已 shipped 的用户裁定**(D-9-1 / D-9-2 / D-9-3)。用户 2026-09-28 看过成品后裁定反转为「连续白面 + 1px 发丝分隔线」(参照 ChatGPT)。因此本里程碑的「门禁同步」是**承重需求**:`check-09` 的 c1/c2/c3/c4 逐条断言卡片语言,反转后**必然全红** —— 那正是门在正确工作的证据。判据必须**改写为断言新契约**,不得删除、不得放宽为恒真(仓库方法论:`一条不能失败的门比没有门更糟`)。

## v1.16 Requirements

### 连续面

- [ ] **SURF-01**: 左栏 4 个面板(会话流 / 本轮批注流 / 自检报告 / AI 工作面板)与右栏文档区**不再各自绘制容器边界** —— `border` / `box-shadow` / `border-radius` 三者从这五个容器上移除;界面读作**一张连续的平面**,不再是"一块块浮起的卡片"(交互控件如按钮 / 输入框**仍保留**各自的圆角与边界)
- [ ] **SURF-02**: 面板底色与页面底色**统一为同一档** —— 不再存在「白卡片浮在灰页面之上」的 elevation 差;页面不再有可辨的灰色底(用户可见:分块感的机械成因消失)
- [ ] **SURF-03**: 灰缝与居中侧沟归零 —— `#main-pane` 的面板间距不再透出页面底色,主区内容列不再因居中而露出左右灰色侧沟;面板区与文档区**直接相邻**

### 发丝分隔线

- [ ] **DIV-01**: 主区与文档区之间由一条 **1px 竖线**分隔,该线**跨满面板可视高度**(不是只画在内容旁的一段)
- [ ] **DIV-02**: 左栏面板之间由 **1px 横线**分隔,替代原 12px 灰缝 —— 分区靠"线",不靠"留白"
- [ ] **DIV-03**: 分隔线取**既有语义令牌**(零新增颜色值、零新增 tier-1 primitive);线宽为 1px

### 门禁同步(承重)

- [ ] **REG-01**: `check-09` 的 c1 / c2 / c3 / c4 判据**改写为断言新契约**(连续面 + 发丝线 + 留白),并**以变异测试证明改写后的判据会真的失败**;不得删除断言、不得降级为恒真、不得只断言"规则被写下了"
- [ ] **REG-02**: `check-02` 对比度清单中**归属卡片底色(`--color-surface-card`)的配对**按元素**实际绘制面重新归属并重算**(非刷新旧值、非调色、非放宽阈值)
- [ ] **REG-03**: `check-05 --item 8` 的 sticky 断言余量(实测恰 `1.000px`,由 Phase 9 给 `#doc-panel` 加的 1px 上边框引入)在 `#doc-panel` 边界改动后**仍成立**;若不成立则判据同步更新并说明改了什么
- [ ] **REG-04**: 五条浏览器门(`check-05` / `06` / `07` / `08` / `09` / `10`)+ 四个静态门(`check-01`…`check-04`)+ pytest 基线(**219 passed / 6 skipped**)复跑**零新增失败**;因 `frontend/style.css` 变更而作废的 `passed` 报告按既有「可执行性分诊」口径逐份处置

### 表头 band(承接 v1.15 审计 G1)

- [ ] **G1-01**: `#latest-check` 内的表格表头读作**一条独立的 band** —— 表头底色与其宿主绘制面不再同令牌相撞、band 不再消失;以运行时读数或人眼截图取证(不是只断言"`th` 画了某个令牌")

### 视觉取证

- [ ] **VIS-01**: 产出 5 张 1440×900 整窗截图(`scripts/ui-states/` 的 p1 / p12 / p3 / checking / archive 五个样本),作为"分块割裂感已消除"的人眼取证

## v2 Requirements

(本里程碑不设 v2 项)

## Out of Scope

| Feature | Reason |
|---------|--------|
| 引入 shadcn/ui 或其任何依赖 | 组件为 `.tsx`(React + Tailwind + Radix primitives),与「原生 HTML/JS、零构建」(D-06)直接冲突 |
| Tailwind / 任何 CSS 框架或构建步骤 | D-06 硬约束 |
| 新增 tier-1 颜色原语 | `check-01` 的硬不变式:primitive 名私有于围栏 |
| 暗色模式 | v1.14 已显式排除(`TOKEN-V2-01`) |
| 图标与空状态 | 用户 2026-09-27 与 2026-09-28 两次均**未点名**,仍待另行裁定 |
| G2(围栏「声明即消费」通用断言 / `--radix-gray-1` 零消费) | 用户 2026-09-28 只裁定「连带 G1」;**G2 未点名**,留待下一里程碑 |
| `999.2`(Phase 7 交互态暴露的三条 affordance 缺陷) | 未点名;执行它会作废 `idi-07` 的 `passed` 指纹 |
| `A11Y-V2-01/02`、`FLOW-V2-01/02`、`TOKEN-V2-01` | 均未点名 |
| Nyquist 缺口(`idi-04` / `idi-06` / `idi-09` / `idi-10` 无 `VALIDATION.md`) | 未点名;建议走 `/gsd-validate-phase`,不占本里程碑范围 |

> **已移出 Out of Scope(2026-09-28):** G1(`#latest-check` 表头 band 消失)由用户裁定「连带 G1」,已转为本里程碑的 `G1-01`。它原列于 v1.15 审计的待裁定项与 `PROJECT.md` 的候选池。

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| SURF-01 | TBD | Pending |
| SURF-02 | TBD | Pending |
| SURF-03 | TBD | Pending |
| DIV-01 | TBD | Pending |
| DIV-02 | TBD | Pending |
| DIV-03 | TBD | Pending |
| REG-01 | TBD | Pending |
| REG-02 | TBD | Pending |
| REG-03 | TBD | Pending |
| REG-04 | TBD | Pending |
| G1-01 | TBD | Pending |
| VIS-01 | TBD | Pending |

**Coverage:**
- v1.16 requirements: 12 total
- Mapped to phases: 0 (待路线图填写)
- Unmapped: 12 ⚠️

---

*Requirements defined: 2026-09-28*
*Last updated: 2026-09-28 — 初次定义。范围由用户逐项裁定:视觉方向「全站去卡片」、落地方式「走 GSD 新阶段」、范围「去卡片化**连带 G1**」、跳过领域研究。*

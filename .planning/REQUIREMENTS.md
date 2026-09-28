# Requirements: 交互式讨论迭代系统

**Defined:** 2026-09-28
**Milestone:** v1.16 界面去卡片化 —— 连续面与发丝分隔线
**Core Value:** 未经用户明确授权,流程绝不进入"撰写总设计文档"步骤——总设计文档通过自检、界面提示「使命完成」即为终点(只读归档态)。

> **REQ-ID 说明:** 本文件只覆盖 v1.16。v1.15 的 12 条需求(CARD / VIS / REG / TABLE / RADIUS)已随里程碑收口归档于 `.planning/milestones/v1.15-REQUIREMENTS.md`。本文件编号自 v1.16 重新起算,与 v1.15 的编号**不构成续号关系**(`REG` 类别在三个里程碑里都出现过,各自独立)。
>
> **本里程碑的性质:反转,不是新增。** v1.15 Phase 9 把界面做成「独立白卡片 + 灰缝 + 页面下沉」,那是**一次已 shipped 的用户裁定**(D-9-1 / D-9-2 / D-9-3)。用户 2026-09-28 看过成品后裁定反转为「连续白面 + 1px 发丝分隔线」(参照 ChatGPT)。因此本里程碑的「门禁同步」是**承重需求**:`check-09` 的 c1/c2/c3/c4 逐条断言卡片语言,反转后**必然全红** —— 那正是门在正确工作的证据。判据必须**改写为断言新契约**,不得删除、不得放宽为恒真(仓库方法论:`一条不能失败的门比没有门更糟`)。

## v1.16 Requirements

### 连续面

- [x] **SURF-01**: 左栏 4 个面板(会话流 / 本轮批注流 / 自检报告 / AI 工作面板)与右栏文档区**不再各自绘制容器边界** —— `border` / `box-shadow` / `border-radius` 三者从这五个容器上移除;界面读作**一张连续的平面**,不再是"一块块浮起的卡片"(交互控件如按钮 / 输入框**仍保留**各自的圆角与边界)
- [x] **SURF-02**: 面板底色与页面底色**统一为同一档** —— 不再存在「白卡片浮在灰页面之上」的 elevation 差;页面不再有可辨的灰色底(用户可见:分块感的机械成因消失)
- [x] **SURF-03**: 灰缝与居中侧沟归零 —— `#main-pane` 的面板间距不再透出页面底色,主区内容列不再因居中而露出左右灰色侧沟;面板区与文档区**直接相邻**

### 发丝分隔线

- [x] **DIV-01**: 主区与文档区之间由一条 **1px 竖线**分隔,该线**跨满面板可视高度**(不是只画在内容旁的一段)
- [x] **DIV-02**: 左栏面板之间由 **1px 横线**分隔,替代原 12px 灰缝 —— 分区靠"线",不靠"留白"
- [x] **DIV-03**: 分隔线取**既有语义令牌**(零新增颜色值、零新增 tier-1 primitive);线宽为 1px

### 门禁同步(承重)

- [x] **REG-01**: `check-09` 的 c1 / c2 / c3 / c4 判据**改写为断言新契约**(连续面 + 发丝线 + 留白),并**以变异测试证明改写后的判据会真的失败**;不得删除断言、不得降级为恒真、不得只断言"规则被写下了"
- [x] **REG-02**: `check-02` 对比度清单中**归属卡片底色(`--color-surface-card`)的配对**按元素**实际绘制面重新归属并重算**(非刷新旧值、非调色、非放宽阈值)
- [x] **REG-03**: `check-05 --item 8` 的 sticky 断言余量(实测恰 `1.000px`,由 Phase 9 给 `#doc-panel` 加的 1px 上边框引入)在 `#doc-panel` 边界改动后**仍成立**;若不成立则判据同步更新并说明改了什么
- [ ] **REG-04**: 五条浏览器门(`check-05` / `check-06` / `check-07` / `check-09` / `check-10`)+ 四个静态门(`check-01`…`check-04`)+ pytest 基线(**219 passed / 6 skipped**)复跑**零新增失败**;因 `frontend/style.css` 变更而作废的 `passed` 报告按既有「可执行性分诊」口径逐份处置。**门清单以磁盘现状为准** —— `scripts/` 实为 `check-01`…`check-07` + `check-09` + `check-10`,外加探针 `probe-05` / `probe-07`,**没有 `check-08`**(本文件初稿曾误列,2026-09-28 规划期由路线图子代理核盘纠正)

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
| G2(围栏「声明即消费」通用断言 / `--radix-gray-1` 零消费) | 用户 2026-09-28 只裁定「连带 G1」;**G2 未点名**,留待下一里程碑。**边界说明:** v1.16 Phase 11 会处置**本次反转自己孤立掉的**两个令牌(`--color-surface-card` / `--shadow-card` 的消费者归零),那是围栏既有规则(「只声明被消费的令牌」/ Hard Rule 5 / D-04)的直接适用,与 Phase 10 删 `--radius-lg` 同型;**不得**顺手补一条通用的围栏消费断言(那才是 G2) |
| `999.2`(Phase 7 交互态暴露的三条 affordance 缺陷) | 未点名;执行它会作废 `idi-07` 的 `passed` 指纹 |
| `A11Y-V2-01/02`、`FLOW-V2-01/02`、`TOKEN-V2-01` | 均未点名 |
| Nyquist 缺口(`idi-04` / `idi-06` / `idi-09` / `idi-10` 无 `VALIDATION.md`) | 未点名;建议走 `/gsd-validate-phase`,不占本里程碑范围 |

> **已移出 Out of Scope(2026-09-28):** G1(`#latest-check` 表头 band 消失)由用户裁定「连带 G1」,已转为本里程碑的 `G1-01`。它原列于 v1.15 审计的待裁定项与 `PROJECT.md` 的候选池。

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| SURF-01 | Phase 11 | Complete |
| SURF-02 | Phase 11 | Complete |
| SURF-03 | Phase 11 | Complete |
| DIV-01 | Phase 11 | Complete |
| DIV-02 | Phase 11 | Complete |
| DIV-03 | Phase 11 | Complete |
| REG-01 | Phase 11 | Complete |
| REG-02 | Phase 11 | Complete |
| REG-03 | Phase 11 | Complete |
| REG-04 | Phase 12 | Pending |
| G1-01 | Phase 12 | Pending |
| VIS-01 | Phase 12 | Pending |

**Coverage:**

- v1.16 requirements: 12 total
- Mapped to phases: 12 (Phase 11: 9 / Phase 12: 3)
- Unmapped: 0

**阶段归属的裁定理由(供下游消费):**

- **Phase 11 = 反转本体 + 它的三条门禁同步义务(SURF 3 + DIV 3 + REG 3)。** `REG-01` / `REG-02` / `REG-03` 与反转是**同一次改动、两副面孔**:`check-09` c1..c4 断言的正是被移除的卡片语言(必红)、`check-02` 的 2 条卡片地面 PAIR 描述的那块面已不存在(数字仍达标 ⇒ 门会绿着说谎)、`check-05 --item 8` 的 sticky 余量 `1.000px` 的成因正是被移除的那条 1px 上边框。拆开会造出「改了面但没人验」的中间态(与 v1.15 把 REG-01/REG-02 与 CARD/VIS 同阶段交付的裁定同型)。
- **Phase 12 = G1 定点修复 + 里程碑收口(G1-01 + REG-04 + VIS-01)。** G1-01 与反转机制独立(不在同一区域、不共享规则)但**有依赖**(表头的宿主绘制面在 Phase 11 变),故排其后;`REG-04` 的「零新增失败」必须在**最后一次 `style.css` 改动之后**跑才成立,故归收口阶段;`VIS-01` 的截图只有拍最终态才有取证价值。
- **`REG-01` 归 Phase 11,`REG-04` 归 Phase 12** —— 本路线图的显式裁定。
- **SURF 与 DIV 同阶段落地**:只去卡片不留线,等于把 4 个面板之间原本承载层次的 12px 灰缝一并抹掉、分区彻底消失 —— 比任一终点都差的中间态。

---

*Requirements defined: 2026-09-28*
*Last updated: 2026-09-28 — 路线图创建,12 条需求 100% 映射到 Phase 11(9)/ Phase 12(3),无 orphan、无跨阶段重复。*

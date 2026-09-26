# Requirements: 交互式讨论迭代系统

**Defined:** 2026-09-26
**Milestone:** v1.15 视觉构图升级
**Core Value:** 未经用户明确授权,流程绝不进入"撰写总设计文档"步骤——总设计文档通过自检、界面提示「使命完成」即为终点(只读归档态)。

> **REQ-ID 说明:** 本文件只覆盖 v1.15。v1.14 的 38 条需求(TOKEN / VISUAL / TYPE / A11Y / LAYOUT / INTERACT / CHECK / REG)已随里程碑收口归档于 `.planning/milestones/v1.14-REQUIREMENTS.md`,其 `REQUIREMENTS.md` 已 `git rm`。故本文件编号自 v1.15 重新起算,与 v1.14 的编号**不构成续号关系**。

## v1.15 Requirements

### 卡片容器

- [ ] **CARD-01**: 左栏 4 个面板(会话流 / 本轮批注流 / 自检报告 / AI 工作面板)各自呈现为独立卡片 —— 白底 + 可见边界 + 圆角,彼此间有明确间隙
- [ ] **CARD-02**: 右栏文档区呈现为独立卡片,与左栏卡片视觉同族(同底色 / 同边框语言 / 同圆角 / 同阴影)
- [ ] **CARD-03**: 页面底色下沉,与白色卡片形成明确的 elevation 层次 —— 卡片视觉上"浮"于页面之上

### 视觉令牌

- [ ] **VIS-01**: 卡片底色与卡片阴影作为新令牌写入围栏 `:root` 块内;令牌块外零裸 `#hex`、零 tier-1 原语引用(`check-01` 绿)
- [ ] **VIS-02**: 卡片圆角取自现有 `--radius-*` 刻度,不引入新值;阴影不参与布局(零位移)

### 回归保障

- [ ] **REG-01**: 页面底色换值后 `check-02` 全部对比度对仍达标;受影响的配对逐条以 `/* PAIR */` 注释**重算并登记**进清单(不是刷新旧值)
- [ ] **REG-02**: 五条 UI 门复跑无新增失败 —— 折叠行为 / 滚动容器收敛 / sticky 表头 / badge 流内机制 / 焦点环 / 24×24 命中区 / 窄窗口不破版全部保持

## v2 Requirements

(本里程碑不设 v2 项)

## Out of Scope

| Feature | Reason |
|---------|--------|
| 引入 shadcn/ui 或其任何依赖 | 组件为 `.tsx`(React + Tailwind + Radix primitives),与「原生 HTML/JS、零构建」(D-06)直接冲突;`npx shadcn init` 会装 npm 依赖并改写 tsconfig |
| Tailwind / 任何 CSS 框架或构建步骤 | D-06 硬约束 |
| 新增 tier-1 颜色原语 | `check-01` 的硬不变式:primitive 名私有于围栏 |
| 表格重做(全边框 → 只留横向分隔线) | 独立视觉决策,待 Phase 9 效果确认后另开 phase |
| 图标与空状态 | 同上 |
| 圆角刻度收敛(`--radius-lg: 28px` 与其他档不成比例) | 同上;影响面已实测收窄(只 2 处消费),但属独立决策 |
| 暗色模式 | v1.14 已显式排除(`TOKEN-V2-01`) |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CARD-01 | Phase 9 | Pending |
| CARD-02 | Phase 9 | Pending |
| CARD-03 | Phase 9 | Pending |
| VIS-01 | Phase 9 | Pending |
| VIS-02 | Phase 9 | Pending |
| REG-01 | Phase 9 | Pending |
| REG-02 | Phase 9 | Pending |

**Coverage:**
- v1.15 requirements: 7 total
- Mapped to phases: 7
- Unmapped: 0 ✓

---

*Requirements defined: 2026-09-26*
*Last updated: 2026-09-26 after roadmap creation — 7/7 需求映射至唯一阶段 Phase 9(CARD-01..03 / VIS-01..02 / REG-01..02),无 orphan、无跨阶段重复;覆盖来源为 `.planning/ROADMAP.md` 的 `## Milestones` 与 `### Phase 9:` 详情段*

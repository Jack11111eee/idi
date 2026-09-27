# Requirements: 交互式讨论迭代系统

**Defined:** 2026-09-26
**Milestone:** v1.15 视觉构图升级
**Core Value:** 未经用户明确授权,流程绝不进入"撰写总设计文档"步骤——总设计文档通过自检、界面提示「使命完成」即为终点(只读归档态)。

> **REQ-ID 说明:** 本文件只覆盖 v1.15。v1.14 的 38 条需求(TOKEN / VISUAL / TYPE / A11Y / LAYOUT / INTERACT / CHECK / REG)已随里程碑收口归档于 `.planning/milestones/v1.14-REQUIREMENTS.md`,其 `REQUIREMENTS.md` 已 `git rm`。故本文件编号自 v1.15 重新起算,与 v1.14 的编号**不构成续号关系**。

## v1.15 Requirements

### 卡片容器

- [x] **CARD-01**: 左栏 4 个面板(会话流 / 本轮批注流 / 自检报告 / AI 工作面板)各自呈现为独立卡片 —— 白底 + 可见边界 + 圆角,彼此间有明确间隙
- [x] **CARD-02**: 右栏文档区呈现为独立卡片,与左栏卡片视觉同族(同底色 / 同边框语言 / 同圆角 / 同阴影)
- [x] **CARD-03**: 页面底色下沉,与白色卡片形成明确的 elevation 层次 —— 卡片视觉上"浮"于页面之上

### 视觉令牌

- [x] **VIS-01**: 卡片底色与卡片阴影作为新令牌写入围栏 `:root` 块内;令牌块外零裸 `#hex`、零 tier-1 原语引用(`check-01` 绿)
- [x] **VIS-02**: 卡片圆角取自现有 `--radius-*` 刻度,不引入新值;阴影不参与布局(零位移)

### 回归保障（Phase 9）

- [x] **REG-01**: 页面底色换值后 `check-02` 全部对比度对仍达标;受影响的配对逐条以 `/* PAIR */` 注释**重算并登记**进清单(不是刷新旧值)
- [x] **REG-02**: 五条 UI 门复跑无新增失败 —— 折叠行为 / 滚动容器收敛 / sticky 表头 / badge 流内机制 / 焦点环 / 24×24 命中区 / 窄窗口不破版全部保持

### 表格重做（Phase 10）

- [ ] **TABLE-01**: 文档区表格由「每格 1px 全边框」改为「表头浅底 + 仅横向分隔线」—— 去掉全部竖线与外框;`.markdown-body th` 获得 gray-2(`--color-surface`)浅底 + 1px 下边线;`.markdown-body td` 保留行间极浅分隔线。就地改写原 `border` 声明,不追加覆盖规则
- [ ] **TABLE-02**: 表格涉及的颜色全部落在**既有令牌**上;表头新绘制面(gray-2)的对比度配对经 `check-02` 实际输出证实已登记 —— 零新增颜色值、零新增 primitive、零阈值改动

### 圆角刻度收敛（Phase 10）

- [ ] **RADIUS-01**: 圆角刻度收敛为 **8 / 10 / 胶囊** 三档 —— 删除 `--radius-lg: 28px`(围栏内零声明残留、全文零 `var(--radius-lg)` 引用);其 2 处消费者改归既有档位:`.chat-user` → `--radius-md`、`#chat-input-row input` → `--radius-pill`
- [ ] **RADIUS-02**: 收敛**零视觉回归** —— `#chat-input-row input` 的计算 `border-radius` 等于 `--radius-pill` 的解析值且外观与收敛前一致(以收敛前后的运行时读数并排为证,不用算术推断);`.chat-user` 为 10px 且尖角(`border-bottom-right-radius: 8px`)保留

### 回归保障（Phase 10）

- [ ] **REG-03**: 五条浏览器门复跑无新增失败、四个静态门全 PASS、pytest 基线不降(219 passed / 6 skipped);因 `frontend/style.css` 变更而作废的 **6 份** VERIFICATION 指纹(`idi-04` / `idi-04.1` / `idi-05` / `idi-06` / `idi-07` / `idi-09`)已以 HEAD 内容**重新验证**而非刷新

## v2 Requirements

(本里程碑不设 v2 项)

## Out of Scope

| Feature | Reason |
|---------|--------|
| 引入 shadcn/ui 或其任何依赖 | 组件为 `.tsx`(React + Tailwind + Radix primitives),与「原生 HTML/JS、零构建」(D-06)直接冲突;`npx shadcn init` 会装 npm 依赖并改写 tsconfig |
| Tailwind / 任何 CSS 框架或构建步骤 | D-06 硬约束 |
| 新增 tier-1 颜色原语 | `check-01` 的硬不变式:primitive 名私有于围栏 |
| 图标与空状态 | 用户 2026-09-27 只点名了表格与圆角两项;此项**未点名**,仍待用户另行裁定 |
| 暗色模式 | v1.14 已显式排除(`TOKEN-V2-01`) |

> **已移出 Out of Scope(2026-09-27):** 「表格重做」与「圆角刻度收敛」两项由用户裁定「做这两个」,已转为 Phase 10 的 `TABLE-01/02` 与 `RADIUS-01/02`。移出时的档位由用户在 `AskUserQuestion` 中选定:表格取「表头浅底 + 仅横向分隔」,圆角取「严格收敛: 8 / 10 / 胶囊」。

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CARD-01 | Phase 9 | Complete |
| CARD-02 | Phase 9 | Complete |
| CARD-03 | Phase 9 | Complete |
| VIS-01 | Phase 9 | Complete |
| VIS-02 | Phase 9 | Complete |
| REG-01 | Phase 9 | Complete |
| REG-02 | Phase 9 | Complete |
| TABLE-01 | Phase 10 | Pending |
| TABLE-02 | Phase 10 | Pending |
| RADIUS-01 | Phase 10 | Pending |
| RADIUS-02 | Phase 10 | Pending |
| REG-03 | Phase 10 | Pending |

**Coverage:**
- v1.15 requirements: 12 total
- Mapped to phases: 12
- Unmapped: 0 ✓

---

*Requirements defined: 2026-09-26*
*Last updated: 2026-09-27 — 用户裁定「表格重做, 圆角刻度收敛。做这两个」后另开 Phase 10,新增 TABLE-01/02、RADIUS-01/02、REG-03 共 5 条;覆盖来源为 `.planning/ROADMAP.md` 的 `## Milestones` 与 `### Phase 10:` 详情段*

# Phase 9 Context — 卡片容器化与页面底色下沉

> **来源说明:** 本文件**不是** `/gsd-discuss-phase` 的产物。用户裁定「直接规划」,
> 但在规划前直接答复了三个设计问题(2026-09-26)。本文件只把那些答复与规划期实测的
> 事实**如实存档**,使 planner 不必自行发明数值。所有条目均为**已裁定**,不重开。

## 已裁定的设计决策(用户,2026-09-26)

### D-9-1:底色关系 = 页面下沉 + 白卡片

- 页面 `--color-surface-page`:`--radix-gray-1`(#fcfcfc) → **`--radix-gray-3`**(#f0f0f0)
- 卡片底色:**白**(`--white` = #ffffff)
- 由此接成三级连贯刻度:`gray-3`(页面) < `gray-2`(`--color-surface`,控件内陷面) < `白`(卡片)
  —— 对应 shadcn 的 canvas / inset / raised 三档
- **不重开此项决策。**

### D-9-2:卡片密度 = 紧凑

- 卡片内边距:**16px**(`var(--space-4)`)
- 卡片间距:**12px**(`var(--space-3)`),替换 `#main-pane` 现有的 `gap: var(--space-1-5)`(6px)
- 理由:左栏 4 个面板叠放在 900px 视口里,**竖向预算本来就紧**。此项竖向多消耗约 66px,
  信息密度基本保住;标准档(24px/16px)会多消耗约 142px,AI 面板展开时会把会话流压得很矮。
- 现状对照:内边距 10px(`.panel-body { padding: var(--space-2-5) }`)、间距 6px

### D-9-3:卡片阴影 = 极轻

- 值:`0 1px 2px rgba(0, 0, 0, 0.04)`
- 强度几乎不可见,只给边缘一点重量;**层次主要靠边框 + 底色差(ΔL≈6%)**
- 与现有极克制的风格一致(现有 `--shadow-composer` / `--shadow-overlay` 都是低透明度多层)
- 必须是**零位移**声明,不得用 `margin` / `position` 模拟浮起

## 规划期实测的现状(硬数据,浏览器 computed style 读数)

| 容器 | 计算底色 | 边框 | 圆角 | 阴影 |
|---|---|---|---|---|
| `body` | `rgb(252,252,252)` gray-1 ← **全场最亮** | — | 0 | 无 |
| `#session-panel` | **`rgba(0,0,0,0)` 完全透明** | 无 | 0 | 无 |
| `#annotations-panel` | **完全透明** | 无 | 0 | 无 |
| `#ai-panel` | **完全透明** | 无 | 0 | 无 |
| `#doc-panel` | `rgb(249,249,249)` gray-2 ← 比页面**更暗** | 1px 左 | **0px** | 无 |
| `#ai-events` | gray-2 | 1px | 8px | 无 |

**结论:现有层次是反的** —— 页面最亮、左栏面板完全透明、文档区反而更暗(读作"凹陷")、
全场零阴影、文档区零圆角。这是"平 / 丑"的机械成因,**不是配色问题**。

## 规划期实测的对比度影响面(关键,防执行期撞墙)

页面换值后,现有 54 条 PAIR 中画在 `--color-surface-page` 上的 **8 条**全部失效
(`style.css:455/465/470/514/523/526/542/562`)。逐条重算结果:

| 配对 | 需要 | gray-1(现状) | gray-3(换后) | 判定 |
|---|---|---|---|---|
| `--color-text` TEXT | 4.5 | 15.88 | 14.30 | PASS |
| `--color-text-secondary` TEXT | 4.5 | 5.77 | 5.19 | PASS |
| `--color-text-muted` TEXT | 4.5 | 5.77 | 5.19 | PASS |
| `--color-focus` NON-TEXT | 3.0 | 5.72 | 5.15 | PASS |
| `--color-marker-active` TEXT | 4.5 | 4.65 | **4.18** | **FAIL** |
| `--color-border-strong` NON-TEXT | 3.0 | 3.24 | **2.91** | **FAIL** |
| `--color-border-hover` NON-TEXT | 3.0 | 5.77 | 5.19 | PASS |
| `--color-marker-active` NON-TEXT | 3.0 | 4.65 | 4.18 | PASS |

**反直觉之处(已实测):** 页面变暗**不**让所有配对变好。深色前景对比度上升,但**中间调**
前景(blue-11 `#0d74ce` / gray-9 `#8d8d8d`)对比度**下降**。两条 FAIL 都是中间调。

### 两条 FAIL 的正解 = 重新归属配对(不是调色,不是放宽阈值)

两条的元素**全部画在面板内部**:

- `--color-marker-active` — 仅 2 处消费者(`style.css:1429` / `1434`),
  是 `#session-panel` / `#annotations-panel` / `#checks-panel` 的 `.panel-header`
  (inset 3px 竖条 + h2 颜色)
- `--color-border-strong` — 10 处消费者(`701/710/717/850/1040/1082/1224/1288/1316/1378`),
  全是 input / select 的静止边框

它们今天被记为 ON surface-page,**是因为面板当前完全透明、页面底色透上来**。卡片化后它们
坐在**白卡片**上 ⇒ 配对须改记为卡片底色。在白底实测:

| 配对 | 需要 | 白卡片上 | 判定 |
|---|---|---|---|
| `--color-marker-active` TEXT | 4.5 | **4.77** | PASS |
| `--color-border-strong` NON-TEXT | 3.0 | **3.32** | PASS |

**因此本阶段不需要改任何颜色值、不需要引入新 primitive、不需要放宽阈值。**

### 禁止的两种错误修法

1. **改颜色值** —— `check-01` 的硬不变式禁止围栏外引用 tier-1 原语;改 `--radix-blue-11` /
   `--radix-gray-9` 的值会连锁影响它们的**全部**其他配对(二者分别被多处消费)。
2. **放宽 `check-02` 阈值** —— 那是"把门改小以让结论成立",本仓库明令禁止。

## 已核实的非问题(规划期不必再查)

**固定定位元素不受页面换值影响** —— `style.css` 只有两处 `position: fixed`,两者都**自带底色**:

| 元素 | 行 | 自身底色 | 结论 |
|---|---|---|---|
| `#stream-banner` | 873 | `--color-surface-mark`(amber-3) | 自足,不受影响 |
| `.overlay`(五弹窗共用) | 809 | `--color-overlay-backdrop` | 遮罩层,自足 |

## 留待用户看图后裁定的开放项(不在本阶段范围)

- **`.overlay-card` 的底色**(`style.css:818`)当前是 `--color-surface`(gray-2) + `--shadow-overlay`。
  页面下沉后它会显得比主界面卡片"内陷一档"。是否改白底以同族 = **设计决策,本阶段不动**,
  截图时提请用户裁定。
- 表格重做 / 圆角刻度收敛 / 图标与空状态 —— 均在 REQUIREMENTS.md Out of Scope,
  **不得预先构建**。

## 范围边界

本阶段**只做**:卡片容器化 + 页面底色下沉 + 配对重算登记 + 门禁复跑 + 供用户评审的截图。

## 编辑纪律(来自 v1.14,每个改动必须遵守)

- `grep -c '^\.hidden {' frontend/style.css` 恒为 **1**
- `!important` **声明**数恒为 **1**(按声明计数,不是命中行数 —— 散文注释会把 `grep -c` 顶高)
- **追加,不重排**(至少一对等特异性规则由源码顺序决定)
- 不得新增 `!important`、不得令牌化 `display`、不得引入 `@layer` / `@property` / `var(--x, #fallback)`
- 零新增运行时依赖、零构建步骤
- 每个 `style.css` 计划必须带至少一项**运行时**验证(真实浏览器 computed style 读数)
- 不得删 `#doc-panel` 的 `overflow-y: auto` —— 它是另一列的滚动者,L-1 的 sticky 表头依赖它
  仍是最近的可滚祖先(删它会同时打破 L-1 与计数门,期望值是 4 不是 3)

## 门禁环境事实(省得重踩)

- `check-05` 必须走 `.venv/bin/python` + `--browser bundled`;该路线的 `channel="chrome"` +
  headless 在本机会**挂死**
- `check-05` 全量跑 exit=2 是**设计如此**(item 5 两条 `--ai-smoke` 腿 BLOCKED),不是回归
- pytest 必须用项目 `.venv`(环境 `python3` 是 miniconda,会让 4 个 `ai_caller` 测试假失败);
  基线 **219 passed / 6 skipped**

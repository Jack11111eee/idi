# Roadmap: 交互式讨论迭代系统

## Milestones

- ✅ **v1.13 交互式讨论迭代系统 MVP** — Phases 1-3 (shipped 2026-09-13) — 详见 `milestones/v1.13-ROADMAP.md`
- ✅ **v1.14 前端视觉与可访问性** — Phases 4-8 (shipped 2026-09-26) — 38 条需求(TOKEN 8 / VISUAL 5 / TYPE 3 / A11Y 9 / LAYOUT 4 / INTERACT 2 / CHECK 4 / REG 3)全部交付 — 详见 `milestones/v1.14-ROADMAP.md`
- 🚧 **v1.15 视觉构图升级** — Phase 9 (in progress) — 7 条需求(CARD 3 / VIS 2 / REG 2)**全部映射至唯一阶段 Phase 9**;用户裁定「开一个 phase,先看看效果吧」,后续候选待看过截图后再定

## Phases

<details>
<summary>✅ v1.13 交互式讨论迭代系统 MVP (Phases 1-3) — SHIPPED 2026-09-13</summary>

- [x] **Phase 1: 行走骨架——服务器、单界面与阶段 1-2 会话** (4/4 plans) — completed 2026-09-09
  启动自检 CLI、选目录进入单界面、状态由磁盘推导、阶段 1-2 连续会话(transcript 恢复)、AI 双轨调用与事件直播、发散模式、G1 认可雏形
- [x] **Phase 2: 轮次收敛循环——划词批注、G2 与机器文法** (4/4 plans) — completed 2026-09-10
  划词批注与大白话双轨、处理本轮批注产出下一轮、上轮冻结只读、§6.4 文法机械校验、annotations 字段写回
- [x] **Phase 3: 授权、自检与终点——G3、档位、使命完成归档** (5/5 plans) — completed 2026-09-13
  G3 四处校验与确认词、DESIGN.md.tmp 原子落盘、宽松/严格自检循环与 D-22 残余裁决、崩溃自愈、完成态只读归档

**Milestone scope:** DESIGN.md v1.13 全部 20 条需求(FLOW 7 + UI 4 + AI 5 + DATA 4)交付并验证。
验证记录:各阶段 `*-VERIFICATION.md`(Phase 1: 8/8 真值、Phase 2: 7/7 SC、Phase 3: 5/5 ROADMAP 判据)与 `*-UAT.md`(6/6、7/7、8 检查点)均 passed。

</details>

<details>
<summary>✅ v1.14 前端视觉与可访问性 (Phases 4-8) — SHIPPED 2026-09-26</summary>

- [x] **Phase 4: 设计契约、令牌层与契约校验** (3/3 plans) — completed 2026-09-20
  书面 UI-SPEC(含含义清单)+ 单一 `:root` 令牌块 + 全部字面量替换 + 四条契约校验命令
- [x] **Phase 4.1: Radix 颜色族重写** (4/4 plans) — completed 2026-09-20
  颜色族从手调 hex 换成 Radix Colors 12 步语义刻度(25 primitive / 47 `--color-*`),CHECK-02 清单重算为 43 对
- [x] **Phase 5: 排版与视觉层级** (4/4 plans) — completed 2026-09-21
  markdown 正文字号受控、不可逆动作权重、页面级层级、面板活动态、两处内联 SVG
- [x] **Phase 6: 布局稳健性** (4/4 plans) — completed 2026-09-22
  魔法数消除、窄窗口不破版、滚动容器收敛、24×24 命中区
- [x] **Phase 7: 交互状态与焦点样式** (3/3 plans) — completed 2026-09-23
  hover/active/disabled/transition + 全站 `:focus-visible`
- [x] **Phase 8: 可访问性语义与键盘** (3/3 plans) — completed 2026-09-24
  唯一触碰 `app.js`/`index.html` 的阶段:tabindex、划词焦点交接、Escape、dialog 语义、内联错误结构修复、五条修复回归复验

**Milestone scope:** 六支柱 UI 审计 13/24 的 13 项**显式延后项**——延后理由一致:修法本身就是设计决策,必须先定契约再落地。38 条需求全部交付;6/6 阶段在 `0b6283a` 复验 `passed`。
**回归面(本里程碑最高风险):** 5 条功能性 BLOCKER 的修复(`b9664e0`)全部依赖本里程碑重写的 CSS 且无自动化覆盖 —— 已由 Phase 8 的 REG-03 全量人工重跑收口。
**收口期发现的跨阶段回归:** Phase 6 的 L-4 滚动容器收敛静默杀掉了 AI 事件自动跟随(`app.js:253` 的 `scrollTop` 赋值按 CSS 规范成为 no-op),而当时的 `check-05 --item 9` 不但零覆盖该回归,还正面断言了它的前提。已修复(追加节点上 `scrollIntoView({ block: 'nearest' })`,不回退 L-4)并新增一条经变异证明会失败的门。
**验证记录:** `milestones/v1.14-phases/` 各阶段 `*-VERIFICATION.md` 与 `*-UAT.md`;里程碑审计 `milestones/v1.14-MILESTONE-AUDIT.md`(`status: passed`,`remediated: 2026-09-25`)。

</details>

### 🚧 v1.15 视觉构图升级 (In Progress)

**Milestone Goal:** 把界面的**构图层次**补齐 —— 左栏 4 个面板与右栏文档区成为白底卡片容器(圆角 + 可见边界 + 极轻阴影 + 内边距),页面底色下沉,界面**首次**拥有 elevation 层次。

**范围裁定(用户,2026-09-26):** 「开一个 phase。先看看效果吧」⇒ **本里程碑只有一个阶段(Phase 9)**。后续候选(表格重做 / 圆角刻度收敛 / 图标与空状态)已在 `.planning/REQUIREMENTS.md` 的 Out of Scope 表逐条列明,**待用户看过 Phase 9 的截图后再决定是否另开 phase**;本里程碑**不得**为其预建阶段。

**为什么是构图而不是配色:** v1.14 的六个范围域(TOKEN / VISUAL / TYPE / A11Y / LAYOUT / INTERACT)全部花在**正确性** —— 颜色、对比度、焦点环;构图(容器层次、视觉重量、组件变体)**从未被任何阶段覆盖**,界面因此仍然"丑"。`shadcn/ui` 的实地核查结论是「不能引入,但可借鉴配方」:配色层面本项目并不落后(已在用 Radix Colors 12 步语义刻度),**缺的是构图**。实测的机械成因(真浏览器探针,非推断):`body` 底色 `rgb(252,252,252)`(gray-1)是**全场最亮**;`#session-panel` / `#annotations-panel` / `#ai-panel` **完全透明**;`#doc-panel` 是更暗的 `rgb(249,249,249)`(gray-2,读作"凹陷")且 **`border-radius: 0px`、零 `box-shadow`**;全应用零 `box-shadow`。

**硬约束(每个计划都适用):** `scripts/check-01-token-conformance.sh`(围栏外零裸 `#hex`、零 tier-1 原语引用;新令牌必须声明在围栏 `:root` 内)、`scripts/check-02-contrast.py`(围栏内 PAIR 清单)、`scripts/check-03-hidden-uniqueness.sh`(`^\.hidden {` 恒为 1)、`scripts/check-04-important-count.sh`(`!important` **声明**数恒为 1);**追加,不重排**(至少一对等特异性规则由源码顺序决定);零新增 `!important`、不令牌化 `display`、不引入 `@layer` / `@property` / `var(--x, #fallback)`;零新增运行时依赖、零构建步骤(DESIGN.md D-06)。

**回归面(本里程碑最高风险):** 五条浏览器门 —— `scripts/check-05-ui-uat.py`(Playwright UAT)、`scripts/check-06-idi05-validation.py`、`scripts/check-07-idi08-validation.py`、`scripts/probe-05-resolve-color.py`、`scripts/probe-07-focus-composite.py` —— 大量断言绑死具体 DOM 与 computed style(焦点环 2px 与其解析后的 `--color-focus`、sticky 表头、badge 流内机制、滚动容器收敛、命中区 24×24、窄窗口不破版)。**任何 surface 改动都可能打破它们** ⇒ 每次改动必须复跑。环境事实:`check-05` 走 `.venv/bin/python` 且**必须** `--browser bundled`(该机 `channel="chrome"` + headless 会挂死);全量跑 exit=2 是 item 5 两条 `--ai-smoke` 腿按设计 BLOCKED,不是回归。

- [x] **Phase 9: 卡片容器化与页面底色下沉** - 左栏 4 个面板与右栏文档区成为白底卡片;页面底色下沉至 gray-3,形成 gray-3 < gray-2 < 白 三级 elevation 刻度;受影响的对比度对重算并登记;五条 UI 门复跑无新增失败 (completed 2026-09-26)

## Phase Details

### Phase 9: 卡片容器化与页面底色下沉

**Goal**: 左栏 4 个面板(会话流 / 本轮批注流 / 自检报告 / AI 工作面板)与右栏文档区各自成为**白底卡片容器**(白底 + 可见边界 + 圆角 + 极轻阴影 + 内边距),页面底色下沉至 `--radix-gray-3`(#f0f0f0) —— 界面首次拥有 elevation 层次,并与既有 `--color-surface`(gray-2,控件内陷面)接成连贯三级刻度:gray-3(页面)< gray-2(内陷面)< 白(卡片)。
**Depends on**: Nothing(v1.15 唯一阶段;v1.14 的 6 个阶段已 shipped 并归档)
**Requirements**: CARD-01, CARD-02, CARD-03, VIS-01, VIS-02, REG-01, REG-02

**Rationale**: 底色关系取「**页面下沉 + 白卡片**」已由用户裁定(2026-09-26,PROJECT.md Key Decisions),**本阶段不重开该决策**。三个候选中此项层次最强(ΔL≈6%),且顺带把现有三层接成连贯刻度 —— 正好是 shadcn 的 canvas / inset / raised 三档。本阶段真正的难点不是选色,而是**在落地它的同时不打破五条浏览器门**:它们是本仓库唯一能证明"渲染语义仍然成立"的机器,而它们断言的正是 computed style。

**Deliverables**:

- `frontend/style.css` 围栏 `:root` 内的**卡片令牌**(卡片底色 / 卡片阴影);卡片圆角取自现有 `--radius-*` 刻度,**不引入新圆角值**;阴影**零位移**(不参与布局)。令牌块外零裸 `#hex`、零 tier-1 原语引用。
- `--color-surface-page` 换值为 `--radix-gray-3`(#f0f0f0):页面底色与白卡片形成明确层次(现值 `rgb(252,252,252)` 是全场最亮,层次是反的)。
- 左栏 4 个面板 + 右栏文档区的**卡片容器规则**(白底 + 可见边界 + 圆角 + 极轻阴影 + 内边距 + 卡片间可见间隙),**追加不重排**。
- `scripts/check-02-contrast.py` 围栏内 PAIR 清单的**重算与登记**:现有 54 条配对中有 **8 条画在 `--color-surface-page` 上**(`style.css` 第 455 / 465 / 470 / 514 / 523 / 526 / 542 / 562 行:`--color-text` / `--color-text-secondary` / `--color-text-muted` / `--color-focus` / `--color-marker-active` ×2(TEXT + NON-TEXT)/ `--color-border-strong` / `--color-border-hover`)。页面换值后这 8 条全部失效,须逐条以 HEAD 内容重新计算比值后登记(不是刷新旧值)。
  **其中 2 条会直接 FAIL(已实测,规划期预判):** `--color-marker-active` TEXT **4.18 < 4.5**、`--color-border-strong` NON-TEXT **2.91 < 3.0**。原因是二者都是**中间调**前景(blue-11 `#0d74ce` / gray-9 `#8d8d8d`)—— 页面变暗会让深色前景对比度上升,却让中间调**下降**,与直觉相反。
  **解法 = 重新归属,不是调色、也不是放宽阈值:** 这 2 条的元素全部画在**面板内部** —— `--color-marker-active` 仅 2 处消费者(`style.css:1429` / `1434`,`#session-panel`/`#annotations-panel`/`#checks-panel` 的 `.panel-header` inset 竖条 + h2 颜色);`--color-border-strong` 的 10 处消费者(`701/710/717/850/1040/1082/1224/1288/1316/1378`)全是 input/select 的静止边框。它们今天被记为 ON surface-page,是因为面板当前**完全透明**、页面底色透上来;卡片化后它们坐在**白卡片**上 ⇒ 配对须改记为卡片底色,在白底实测 **4.77 / 3.32,双双达标**。**因此本阶段不需要改任何颜色值、不需要引入新 primitive。**
- 五条浏览器门的复跑记录(`check-05` / `check-06` / `check-07` / `probe-05` / `probe-07`),含 `check-05` 全量结果与 item 5 两条 BLOCKED 腿的按设计说明。
- 供用户评审的**截图** —— 用户将据此裁定后续候选(表格重做 / 圆角刻度收敛 / 图标与空状态)是否另开 phase。

**Success Criteria** (what must be TRUE):

1. 左栏 4 个面板(会话流 / 本轮批注流 / 自检报告 / AI 工作面板)在浏览器里各自呈现为**独立卡片** —— 每个容器的计算底色为白、计算圆角非零、计算阴影非 `none`,彼此之间有可见间隙;不再是 v1.14 收口时的"完全透明贴页面底色"。
2. 右栏文档区呈现为**同族卡片**(同底色 / 同边框语言 / 同圆角 / 同阴影),其原有的 `border-left: 1px` 凹陷读感被卡片语言取代。
3. 页面底色确实**比卡片更暗**:`body` 的计算底色为 gray-3(`rgb(240,240,240)`),与白卡片构成可见层次;屏幕上同时可见的三档顺序正确 —— gray-3(页面)< gray-2(`--color-surface`,控件内陷面)< 白(卡片),控件内陷面仍读作"凹"、卡片仍读作"凸"。
4. 卡片令牌全部落在围栏 `:root` 内:`scripts/check-01-token-conformance.sh` 通过(令牌块外零裸 `#hex`、零 tier-1 原语引用);圆角取自现有 `--radius-*` 刻度;阴影零位移、不参与布局。
5. 页面换值后 `scripts/check-02-contrast.py` 全部对比度对仍达标 —— 画在 `--color-surface-page` 上的 **8 条** PAIR 逐条以 HEAD 内容重算比值、以 `/* PAIR */` 注释**登记**(非刷新旧值);其中重算后不达标的 2 条(`--color-marker-active` TEXT 4.18、`--color-border-strong` NON-TEXT 2.91)已按**卡片化后元素的实际绘制面**重新归属到卡片底色,并在白底实测达标(4.77 / 3.32),**全程未改动任何颜色值、未新增 primitive、未放宽阈值**;五条浏览器门复跑**无新增失败** —— 折叠行为 / 滚动容器收敛 / sticky 表头 / badge 流内机制 / 焦点环 / 24×24 命中区 / 窄窗口不破版全部保持。

**Avoids** (Pitfalls):

- **"刷新"旧 PAIR 值** —— `--color-surface-page` 现值是 `var(--radix-gray-1)`(#fcfcfc),换值会使画在其上的 **8 条** PAIR(见 Deliverables)全部失效;刷新等于断言"自验证以来什么都没变",而这里是假的。必须逐条以 HEAD 内容重算并登记。**注意:其中 2 条重算后是 FAIL,不是"数值变了但仍达标"**(见 Deliverables 的实测值与重新归属解法)—— 把它们当成"重算一下就好"会在执行期撞墙。
- **为救 2 条 FAIL 去动颜色值或放宽阈值** —— 两者都是错的方向。`check-01` 的硬不变式禁止在围栏外引用 tier-1 原语,而改 `--radix-blue-11` / `--radix-gray-9` 的值会连锁影响它们的**全部**其他配对(二者分别被多处消费);放宽 `check-02` 的 4.5 / 3.0 阈值则是**把门改小以让结论成立**,是本仓库明令禁止的"门绿但没在看"。正解只有一条:**把配对重新归属到卡片底色**(见 Deliverables)—— 因为卡片化本身确实改变了这些元素的绘制面,这不是变通,是如实登记。
- **重排规则** —— 至少一对等特异性规则由源码顺序决定;重排即渲染变更,而源码 diff 看起来完全无辜。只追加。
- **计数门的算术陷阱** —— `check-04` 数的是 `!important;` **声明**数(恰为 1),不是命中行数;解释性注释的散文会把 `grep -c` 顶高(本项目已因此红过三次)。
- **为凑卡片效果删掉 `#doc-panel` 的 `overflow-y: auto`** —— 它是另一列的滚动者,L-1 的 sticky 表头依赖它仍是最近的可滚祖先;删它会同时打破 L-1 与计数门(期望值是 4 不是 3)。
- **把阴影做成参与布局的东西** —— 阴影必须零位移;用 `margin` / `position` 模拟"浮起"会移动既有几何,直接打在命中区与窄窗口门上。
- **只在静态 grep 上验收** —— 每个 `style.css` 计划必须带至少一项运行时验证(真实浏览器的 computed style 读数);`grep -c 'var(--'` 对渲染结果零证明力。
- **范围蔓延到后续候选** —— 表格重做 / 圆角刻度收敛 / 图标与空状态**不在本阶段**(用户裁定先看效果)。

**Gates**: `scripts/check-01-token-conformance.sh` PASS;`scripts/check-02-contrast.py` PASS(受影响 PAIR 全部重算并登记,`ORDER` 断言不退化);`scripts/check-03-hidden-uniqueness.sh`(`^\.hidden {` = 1);`scripts/check-04-important-count.sh`(`!important` 声明 = 1);五条浏览器门复跑无新增失败(`check-05` 走 `.venv/bin/python` + `--browser bundled`);`node --check frontend/app.js`;`.venv/bin/python -m pytest backend/tests -q --tb=short` 基线不降(**219 passed / 6 skipped** —— 必须用项目 `.venv`,环境 `python3` 是 miniconda 会让 4 个 `ai_caller` 测试假失败);`git status --porcelain frontend/` 仅预期文件、`frontend/vendor/` 仍只有 `marked.min.js`。
**Plans**: 3/3 plans executed

- [x] `idi-09-01-PLAN.md` — 卡片令牌(围栏内 `--color-surface-card` / `--shadow-card`)+ 左栏 4 个 section 与右栏 `#doc-panel` 的卡片语言 + `#doc-panel-header` 底色跟随 + 2 条 PAIR 的地面重新归属(4.77 / 3.32)+ 新建运行时门 `check-09-idi09-validation.py`
- [x] `idi-09-02-PLAN.md` — 密度收档(卡片间距 12px / 面板内边距 16px)+ 页面底色下沉到 `--radix-gray-3` + 画在页面上的 6 条 PAIR 逐条重算并登记(不是刷新旧值)+ 三层刻度与滚动契约的运行时门
- [x] `idi-09-03-PLAN.md` — 五条浏览器门复跑与失败分诊 + 四个静态门与 pytest 基线复核 + 5 个状态样本的截图(供用户评审)

**UI hint**: yes

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. 行走骨架 | v1.13 | 4/4 | Complete | 2026-09-09 |
| 2. 轮次收敛循环 | v1.13 | 4/4 | Complete | 2026-09-10 |
| 3. 授权、自检与终点 | v1.13 | 5/5 | Complete | 2026-09-13 |
| 4. 设计契约、令牌层与契约校验 | v1.14 | 3/3 | Complete | 2026-09-20 |
| 4.1. Radix 颜色族重写 | v1.14 | 4/4 | Complete | 2026-09-20 |
| 5. 排版与视觉层级 | v1.14 | 4/4 | Complete | 2026-09-21 |
| 6. 布局稳健性 | v1.14 | 4/4 | Complete | 2026-09-22 |
| 7. 交互状态与焦点样式 | v1.14 | 3/3 | Complete | 2026-09-23 |
| 8. 可访问性语义与键盘 | v1.14 | 3/3 | Complete | 2026-09-24 |
| 9. 卡片容器化与页面底色下沉 | v1.15 | 3/3 | Complete    | 2026-09-26 |

**v1.13 / v1.14 共 9 个阶段已收口。** v1.15 为**单一阶段**(Phase 9),**进行中** —— 计划 2/3 已完成(卡片容器化端到端落地 + 页面底色下沉到 gray-3 与密度收档);余下计划 03 复跑五条浏览器门、复核 pytest 基线并出 5 张截图。用户裁定「开一个 phase,先看看效果吧」,看过 Phase 9 的截图后再决定后续候选(表格重做 / 圆角刻度收敛 / 图标与空状态)是否另开 phase。

## Backlog

### Phase 999.1: Phase 4 残留的两条卫生项 (BACKLOG)

**Goal:** 清掉 Phase 4 收口后遗留、已由用户裁定为 Phase 4 范围外的两条小项。二者都是「已记录但无人认领」的真项,不是延期项。

1. **`.collapse-indicator` 的越轨字面量** —— `frontend/style.css:434` 为
   `.collapse-indicator { font-size: 20px; line-height: 1; }`,围栏外两个裸字面量,属 Phase 4 已令牌化的
   `--text-*` / `--lh-*` 族,且在 `04-UI-SPEC.md:841` 的封闭例外清单(L-1…L-5)之外。
   由 quick 任务 `260918-qrq`(`3684353`,2026-09-18 20:01)在 Phase 4 收口(`0c658aa`)之后引入;
   Phase 4 自己的提交区间干净。已在 `idi-04.1-UI-REVIEW.md` Pillar 4 记分(3/4,「undeclared 6th size」)。
   **HEAD 字号刻度为 12 / 14 / 16 / 18 / 24 —— `20px` 不在刻度上,故修法是排版决策而非机械替换**:
   加一档(改刻度,牵动 UI-SPEC 的「5 sizes」声明与 S-2 `--text-base = 14px` 的下游门)、重映射到 `18px`/`24px`
   (改已出货的 ▾/▸ 视觉),或加一条 L-6 例外(不改 `style.css`,但 `20px` 永久留在出货 chrome 里)。
   **注意:** 任何对 `frontend/style.css` 的编辑都会作废 `idi-04.1-radix` 的 `passed` 指纹(其 `covered_files`
   含该文件,digest 为原始字节 sha256),需连带复验 04.1。另见 Phase 5 Pitfall 7:`app.js:1550` 用 `textContent`
   赋值 `.collapse-indicator`,触碰它时不得引入内联 `<svg>`。
2. **`scripts/check-05-ui-uat.py:588` 的陈旧诊断文案** —— 仍打印「`--color-text-muted` … 变为 #8f8f8f,
   低于 AA 4.5:1」,而 HEAD 实为 `rgb(100,100,100)`、在 `--color-surface` 上 5.62 达标。周围断言正确,
   仅该 INFO 行陈旧。**改它同样会作废 04.1 的指纹**(该脚本也在 04.1 的 `covered_files` 里),
   故与第 1 项合并为同一批处理,一次性连带复验 04.1。

**裁定记录:** `idi-04-VERIFICATION.md` frontmatter `overrides:`(`accepted_by: Jack11111eee`,2026-09-20)与
其 Gaps Summary。未写进 Phase 5 的理由:Phase 5 的 Pitfall 7 把触碰 `.collapse-indicator` 的范围锁死为
两处 `content:` emoji,其 SC1 只点名四处 chrome 覆盖 —— 插入新交付物等于改写已签核的门。

> ✅ **已于 2026-09-25 关闭** —— quick `260925-iin` 同时处置了两项:第 1 项按用户裁定**加第 8 档字号**
> (`--text-lg-plus: 20px` + `--lh-none: 1`,字形渲染尺寸不变);第 2 项把陈旧 INFO 串更正为
> `rgb(100,100,100)` / 5.62:1 达标,未改任何断言。该 quick 同时新增一条经变异证明的自动跟随门
> (`check-05 --item 9`)与一条 `FOCUSABLE_SELECTOR` ↔ `:focus-visible` 对齐门(`check-07` 静态守卫 ⑤)。
> 连带复验:因 `frontend/style.css` 与 `scripts/check-05-ui-uat.py` 变更,`idi-04.1-radix` 与 `idi-07` 的
> 指纹作废 —— 六个阶段的指纹最终全部作废,并在收口前逐份以 HEAD 内容重新验证通过。见
> `.planning/milestones/v1.14-phases/idi-04-tokens-contract/idi-04-VERIFICATION.md` 与 `idi-05-*/idi-05-UI-SPEC.md`。

**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /gsd-review-backlog when ready)

### Phase 999.2: Phase 7 交互态契约暴露的三条既有 affordance 缺陷 (BACKLOG)

**Goal:** 清掉 `idi-07-UI-REVIEW.md`(2026-09-23,19/24)在建立「每个交互控件对 hover / active / disabled
有可辨反馈」这条契约时**暴露出来**的三条缺陷。三者都不是本阶段改动引入的(第 1、2 条是 Phase 7 之前就在的
affordance 谎报;第 3 条虽属 Phase 7 自己那份 PAIR 清单,但补它要动 `style.css` ⇒ 作废刚过的指纹),
但都只有在 Phase 7 的契约下才成为可判定的项。

1. **`#session-panel .panel-header` 宣称了一个不存在的点击** —— `frontend/style.css:665-674` 的基类
   `.panel-header` 规则体带 `cursor: pointer` + `user-select: none`,但只有 `#ai-panel-header` 与
   `#doc-panel-header` 有监听(`frontend/app.js:1561` / `1567`)。文件自己的惯例是对不可点的两个面板显式复位:
   `#annotations-panel .panel-header { cursor: default; }`(`style.css:1085`)与
   `#checks-panel .panel-header { cursor: default; }`(`style.css:1304`)。
   `#session-panel .panel-header`(`frontend/index.html:15`,该 header 无 id)两者皆无 ⇒ 鼠标移到「会话流」
   标题上会得到可点的指针。**修法:** 按既有惯例补一条 `#session-panel .panel-header { cursor: default; }`
   (一条声明,零重排)。
2. **`.annotation-answer summary` 没有任何交互态,也没有运行时覆盖** —— `style.css:1189` 定义了它;它带
   `cursor: pointer`、受 Phase 6 的 A11Y-07 门约束(24×24 命中区)、并被 Phase 7 的焦点环覆盖
   (`style.css:1513` 的七选择器含 `summary`),但**没有任何 `:hover` / `:active` 规则**,也不在过渡挂载规则里
   (`style.css:1675` 只覆盖 `button, input, select`)。更关键的是:**三个样本里没有任何 fixture 会渲染出
   `<summary>`**,故 item 10 的焦点环普查(每样本 28 个元素)从未见过它 —— 它的「已覆盖」是名义上的。
   **修法(两半,缺一不可):** 把 `summary` 并入朴素按钮的 hover 组;**并且**在 `p3` fixture 里加一个
   `summary`,或按 D-18 对 `a[href]` 的先例把该缺口**显式登记**。只做前半场会让「已覆盖」继续是名义的。
3. **焦点环的 PAIR 清单漏掉一处它真实渲染其上的底色** —— `style.css:498-507` 的清单列三处验证面
   (`--color-surface` / `--color-surface-page` / `--color-surface@0.75`),并**显式论证**为何排除
   `--color-surface-sunken`,却对 `--color-surface-warning-subtle`(amber-1)只字未提。而
   `.verdict-card`(`style.css:1341`,底色即该令牌)正是 item 10 在 `checking` 样本里实测
   `.verdict-note-input` 与两个 `.verdict-buttons button` 的宿主 —— 焦点环在这处底色上确实渲染。
   这是**与本文件自订纪律的直接冲突**:`style.css:435-437` 逐字写明「a token drawn as a UI boundary must
   have its own NON-TEXT pair on each ground it is drawn on」,而兄弟令牌 `--color-border-hover` 正是按这条
   纪律补上了这一处底色(`7b4ae18`,+3 ⇒ 53 对);`--color-focus` 同为 UI 边界却漏了同一处。
   实测环色在其上为 **5.77:1(达标)** ⇒ 这是**覆盖一致性缺陷,不是可辨性缺陷**。
   **修法:** 补一条 `/* PAIR --color-focus ON --color-surface-warning-subtle NON-TEXT */`,与 `7b4ae18` 对齐。

**指纹影响(执行前必读):** `frontend/style.css` 与 `scripts/check-05-ui-uat.py` **同时**在
`idi-07-VERIFICATION.md` 的 `covered_files` 里(digest `v1:sha256:5964d53c…`)。第 1、2、3 条的修法都要动
`frontend/style.css`,第 2 条的后半场还要动 `scripts/check-05-ui-uat.py` —— 故本项一旦执行,`idi-07` 的
`passed` 指纹即失效,须**连带重新验证 idi-07**(与 999.1 对 `idi-04.1-radix` 的关系同型)。
建议三条合并为同一批处理,一次性连带复验。

**裁定记录:** `idi-07-UI-REVIEW.md`(19/24;Pillar 2 Visuals 2/4、Pillar 3 Color 3/4、Pillar 6 Experience
Design 3/4 的扣分主因即此三条)与 `idi-07-VERIFICATION.md`。未写进 Phase 7 的理由:第 1、2 条是**既有**
affordance —— Phase 7 只改了声明式 CSS 的交互态与焦点环,`frontend/app.js` / `frontend/index.html` 逐字节未改,
按外科手术式改动纪律不在本阶段边界内;第 3 条虽属 Phase 7 自己的清单,但补它要动 `style.css` ⇒ 作废刚过的
指纹,而 UAT 已 1/1 通过、阶段收口在即,故由用户裁定转为 backlog 而非当场展开。
**用户裁定:`2026-09-23`(本 backlog 条目的建立即该裁定)。**

**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /gsd-review-backlog when ready)

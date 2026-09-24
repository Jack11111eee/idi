# Roadmap: 交互式讨论迭代系统

## Milestones

- ✅ **v1.13 交互式讨论迭代系统 MVP** — Phases 1-3 (shipped 2026-09-13) — 详见 `milestones/v1.13-ROADMAP.md`
- 🚧 **v1.14 前端视觉与可访问性** — Phases 4-8 (in progress) — 38 条需求(TOKEN 8 / VISUAL 5 / TYPE 3 / A11Y 9 / LAYOUT 4 / INTERACT 2 / CHECK 4 / REG 3),其中 **REG-01/REG-02 已于 2026-09-17 由 quick `260917-fqh` 前置收口**,余 36 条映射至 Phases 4-8

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

### 🚧 v1.14 前端视觉与可访问性 (In Progress)

**Milestone Goal:** 把前端从"零设计契约下长出来的功能骨架"变成有设计契约、键盘可用、视觉可信的工具界面。

**范围来源:** 六支柱 UI 审计 13/24、7 个 BLOCKER 的**显式延后项**(`.planning/milestones/v1.13-phases/idi-03-g3/03-UI-REVIEW.md`)。延后理由一致:修法本身就是设计决策,必须先定契约再落地。5 条功能性 BLOCKER 已于 2026-09-16 修复并合入 main(`b9664e0`),不在本清单内——但它们**是本里程碑最高的回归风险面**:五条修复全部依赖本里程碑要重写的 CSS,且**无任何自动化覆盖**。

**本里程碑不含:** 新功能、新依赖、新前端文件、构建步骤。六个范围域中四个是纯 `style.css` 改动;只有一个阶段触碰 `app.js`/`index.html`。

**全局硬规则(每个阶段、每个计划都适用,来源:PITFALLS.md / ARCHITECTURE.md)**

1. `grep -c '^\.hidden {' frontend/style.css` 必须等于 **1**。`.hidden { display: none !important }` 是**机制而非样式**:不得令牌化、不得移动、不得弱化、不得用 `:where()` 降特异性。五个元素(`#draft-empty` / `#rounds-hint` / `#btn-process-round` / `#round-switcher` / `#writing-hint`)**只靠它隐藏**,且三个竞争者(`#selection-menu` / `#annotations-panel` / `#checks-panel`)靠 **ID 特异性 1-0-0** 取胜,与源码顺序无关。
2. `style.css` 中含 `!important` 的**声明行**数为 1。注意算术陷阱:当前 `grep -c '!important' frontend/style.css` 返回 **3**,其中 2 行是 L13-14 的注释散文。写 gate 时必须按"声明"计数,不能直接数命中行(先前的修复轮已犯过一次同类 gate 算术错误)。
3. **追加,不重排。** 至少一对等特异性规则由源码顺序决定(`#draft-view h2` L230 与 `#brainstorm-view h2` L296 同为 1-0-1,后者胜出 → 14px / `#8a6508`)。重排即渲染变更,而源码 diff 看起来完全无辜。
4. 不得新增 `!important`;不得令牌化 `display`;不得引入 `@layer` / `@property` / `var(--x, #fallback)`(三者都会重新打开 `.hidden` 的特异性竞速,或重建第二事实源)。
5. **不得触碰:** `.fatal` 修饰符(`#stream-banner` 的致命/非致命两态必须仍可区分)、`applyArchiveView` 的两行(`app.js:817-818`)、`#selection-menu` 的 DOM 位置(必须是 `<body>` 直接子元素,任何 `filter`/`transform`/`opacity` 祖先都会改变其包含块)、`showInlineError` 的 `textContent`-only 规则(XSS 缓解 T-260916-01,不是风格选择)、`renderAnnotations` / `renderVerdictCard`、`app.js:4-75` 的约 70 个顶层 `getElementById` 句柄(id 不得改名或删除)。
6. 零新增运行时依赖、零构建步骤(DESIGN.md D-06)。CHECK-01/02 两个脚本必须零依赖;任何需要安装的写法都是计划偏差与停止条件。
7. 每个 `style.css` 计划都必须带**至少一项运行时验证**,不能只有静态计数。`grep -c 'var(--'` 对渲染结果零证明力。

**本里程碑之外(已裁定,记录以防范围蔓延):**

- `#probe-controls` 的移除或重定位 —— **产品行为变更**,且双路线界面契约(AI-03 / D-06)是真功能。列为独立未来候选,不进本里程碑任何阶段。
- 暗色模式 / `prefers-color-scheme` —— 会翻倍对比度校验面,是唯一会迫使引入 primitive 语义层(除颜色外)的理由。令牌写法只需使其将来"多一个 `@media` 块重赋现有语义名"即可(软约束)。
- 完整 ARIA / 焦点陷阱 / 其余 2-3 个非阻塞弹窗的 `role` —— 用户已裁定取窄切片。
- 两处 `window.prompt` 替换、响应式/移动端断点系统、图标库、组件级令牌层、任何 lint 工具链 —— 见 REQUIREMENTS.md 的 Out of Scope 表。

- [x] **Phase 4: 设计契约、令牌层与契约校验** - 书面 UI-SPEC(含含义清单)+ 单一 `:root` 令牌块 + 全部字面量替换 + 四条契约校验命令 (completed 2026-09-20)
- [x] **Phase 5: 排版与视觉层级** - markdown 正文字号受控、不可逆动作权重、页面级层级、面板活动态、两处内联 SVG (completed 2026-09-21)
- [x] **Phase 6: 布局稳健性** - 魔法数消除、窄窗口不破版、滚动容器收敛、24×24 命中区 (completed 2026-09-22)
- [x] **Phase 7: 交互状态与焦点样式** - hover/active/disabled/transition + 全站 `:focus-visible` (completed 2026-09-23)
- [ ] **Phase 8: 可访问性语义与键盘** - 唯一触碰 `app.js`/`index.html` 的阶段:tabindex、划词焦点交接、Escape、dialog 语义、内联错误结构修复、五条修复回归复验

## Phase Details

### Phase 4: 设计契约、令牌层与契约校验

**Goal**: `style.css` 拥有一份书面设计契约与单一令牌来源;全部字面量被替换为 `var()`,令牌块之外零裸 `#hex`;四条契约校验命令可独立运行;AA 达标值在**声明处**即选定。
**Depends on**: Nothing (v1.14 首个阶段;v1.13 三阶段已 shipped)
**Requirements**: TOKEN-01, TOKEN-02, TOKEN-03, TOKEN-04, TOKEN-05, TOKEN-06, TOKEN-07, TOKEN-08, CHECK-01, CHECK-02, CHECK-03, CHECK-04, A11Y-04, A11Y-04b

**Rationale**: 硬前置——后续四个阶段全部消费它,且它是唯一一个成功判据是**纯重构**的阶段(除刻意修复的对比度外零视觉变化),因而是发现"迁移方法本身错了"最便宜的地方。它必须最先落地:后续每一个修复(对比度、层级、焦点)都是令牌**值**的改动,在存在两个事实源时无法验证。

**Deliverables**:

- `UI-SPEC.md`(阶段目录下):令牌清单 + **含义清单**(每个颜色名对应哪一语义——这是把"绿色意味着七件事"收敛为可命名概念的前提,必须**先于**令牌)、间距/字号/圆角刻度、焦点规则、"不在 v1.14"表(把每条被延后的审计发现连同理由写下来)。
- `style.css` 顶部带围栏注释的**单一** `:root` 令牌块(插在 `* { box-sizing }` 之后、`html, body` 之前,`/* ===== DESIGN TOKENS: START/END ===== */` 围栏)。
- 全部字面量的替换:34 个 hex(120 次出现)、3 处 `rgba()`、14 个 padding / 11 个 margin / 5 个 gap 值、7 个字号、8 个圆角、4 个 `z-index`。
- 令牌块之外的 `style.css` 含**零**裸 hex;`--z-*` 序关系在块内注释中显式断言(badge 10 < banner 20 < overlay 100 < selection-menu 200)。
- **AA 达标值在此选定**(`.hint` 用最浅的通过值而非"安全的"深灰;`opacity` 文字弱化改为颜色令牌,含 `#round-doc.round-frozen` 0.55 与归档态 0.75 两处整篇文档灰化——冻结灰化与 AA 的冲突须在此裁定)。这同时交付 A11Y-04 / A11Y-04b。
- CHECK-01/02/03/04 四条零依赖命令。
- ✅ **REG-01 已完成**(quick `260917-fqh`,`fac268d`):`.hidden` 注释的**错误理由**已修正——原注释称 `.overlay`/`.doc-subview` 为 0-1-0 竞争者;`.doc-subview` 根本没有 `display` 声明,而决定性的三个 ID 特异性竞争者(`#selection-menu`/`#annotations-panel`/`#checks-panel`,均 1-0-0)全部未被提及。`!important` 的结论正确,理由在两个方向上都不对。**本相位仍须以 CHECK-03/04 守住 `.hidden` 唯一性与 `!important` 声明数=1**(该规则是 5 路单点故障)。

**Success Criteria** (what must be TRUE):

1. `style.css` 顶部存在单一 `:root` 令牌块,块外零裸 `#hex`——CHECK-01 一条命令即可证明,而非靠人读文件。
2. 除刻意修复的对比度外,页面渲染与令牌落地前一致:没有任何既有选择器改变位置、改名或增删声明(纯值替换)。
3. 每处闸门说明文字仍比主正文"次要",且其自身达到 WCAG AA——层级关系与比值一起校验,不只校验比值。
4. `.hidden` 仍是全站唯一一条 `!important` 声明;五个只依赖它的元素在浏览器里仍正确隐藏(实检,不靠读 CSS)。
5. CHECK-01/02/03/04 四条命令可独立运行,各自给出明确的通过/失败结论。

**Avoids** (Pitfalls):

- **Pitfall 1 半迁移令牌调色板**——迁移必须**一次性、机械、按值族原子提交**;绝不定义一个在同一次提交中不消费的令牌,也绝不为已令牌化的值留下字面量。
- **Pitfall 2 `.hidden` 级联回归**——见全局硬规则 1/2/4;`!important` 保留,`.hidden` 不动。
- **Pitfall 3 回归五条已交付修复**——把"不得触碰"清单写进 UI-SPEC,并由 Phase 8 的 REG-03 复验。
- **Pitfall 4a 对比度修到比值却毁掉层级**——取**最浅的通过值**;断言 hint/正文比值 ≤ ~0.30;`opacity` 文字弱化一律改颜色令牌(`.annotation-answered` 现为 1.88:1)。
- **Pitfall 8 范围蔓延**——UI-SPEC 的"不在 v1.14"表。
- **Pitfall 9 重排即渲染变更**——见全局硬规则 3。
- **Pitfall M6 `#confirm-error` 的 `.hint` 耦合**——保留 ID,或以等于/高于 `.hint` 的特异性显式设定错误色,否则 G3 确认失败信息会退化成灰色提示。
- **Pitfall M1 靠 grep 计数验收**——四条脚本是**补充**,每个计划仍须带运行时验证。

**Research flag**: **需要 UI-SPEC 决策,不是研究缺口。** ARCHITECTURE.md 向 UI-SPEC 作者提了 7 个未决问题(令牌命名与 positive/gate/irreversible 三分;不可逆动作的处理方式;字号锚点 13px vs 14px;`--fw-medium: 500` 是否真的被消费;窄窗口范围;`#state-badge` 的 `calc()` vs `absolute`;两处 emoji 的图标机制)。**这 7 个问题在 Phase 4 可被规划之前必须答复。** 令牌分类学的建议结论(三份研究分歧的调和):**颜色两层(primitive → semantic),间距/字号/圆角单层,无组件层**;硬不变量 = **primitive 名绝不出现在 `:root` 块之外**(机械可查)。

**Gates**: CHECK-01(块外 hex = 0)、CHECK-02(全部声明令牌配对达 AA)、CHECK-03(`^\.hidden {` = 1)、CHECK-04(`!important` 声明 = 1);每个 `var(--x)` 都能解析到已声明的 `--x`;`node --check app.js`;pytest 基线不变(**注意:此处原写 219,但规划时实测收集数为 225** —— quick `260917-fqh` 之后新增了用例;门按"通过数 ≥ 执行前实测收集数"判定并记录实际数字,照抄 219 会造出必然失败的假门,正是本里程碑反复警告的 gate 算术错误);`git status --porcelain frontend/` 仅三个已知文件、`frontend/vendor/` 仍只有 `marked.min.js`;`app.js`/`index.html` 零改动。
**Plans**: 3/3 plans executed
Plans:
**Wave 1**

- [x] idi-04-01-PLAN.md — 围栏令牌块 + 颜色契约(25 primitive / 50 tier-2)+ CHECK-01/03/04 三条守卫命令;tracer 先行走通「校验层 ↔ 令牌层」端到端,CHECK-01 由 117 归 0 ✅ 完成(8c9e6f9 / 5b898bf / f773355;CHECK-01 PASS,块外裸 hex = 0)

**Wave 2** *(blocked on Wave 1 completion)*

- [x] idi-04-02-PLAN.md — 间距(12 档)/字号(6 档)/字重(2)/行高(3)/圆角(3)/z-index(4)+ `--sidebar-w`;冻结轮结构性标记(S-4)与 N-4 前景色规则

**Wave 3** *(blocked on Wave 2 completion)*

- [x] idi-04-03-PLAN.md — CHECK-02 对比度校验脚本 + 围栏内 PAIR 配对清单(20 文本 + 4 非文本)+ 四条命令的失败方向实证

**UI hint**: yes

### Phase 04.1: Radix 颜色族重写 (INSERTED)

**Goal:** 把颜色族从手调 hex 换成 Radix Colors 的 12 步语义刻度(1-2 底 / 3-5 组件底 / 6-8 边框 / 9-10 实心填充 / 11-12 文字),并据此重算 UI-SPEC 令牌清单与 CHECK-02 的 34 对对比度配对。
**非紧急插入**:这是 Phase 4 **值层**的刻意重写(结构产出——围栏 `:root`、75 个令牌、四条守卫命令——不动),同时吸收 idi-04 UAT 的 3 项 FAIL 与 `--color-text-muted` 3.23:1 的 AA 倒退。
**不含暗色模式**(与 v1.14 的已记录排除项一致);**不改** S-1 间距 12 档与 S-2 的 14px 一级字号档。
**Requirements**: TOKEN-01, TOKEN-02, TOKEN-04, TOKEN-07, CHECK-01, CHECK-02, CHECK-03, CHECK-04, A11Y-04, A11Y-04b(全部是 Phase 4 已列需求 —— 04.1 是它们的**值层重写**,不新增需求。口径:本阶段**实质关闭** A11Y-04 / A11Y-04b / CHECK-02 / TOKEN-07 / CHECK-01(AA 倒退、`.tier-desc` 的 opacity 越轨、43 对清单重算、z-index 序断言重新有消费者、D-03 改名后空转的 tier-1 守卫);**沿用并复证** TOKEN-01 / TOKEN-02 / TOKEN-04 / CHECK-03 / CHECK-04。**不触碰** TOKEN-03 / TOKEN-05 / TOKEN-06 / TOKEN-08)
**Depends on:** Phase 4
**Plans:** 4/4 plans complete

Plans:
**Wave 1**

- [x] idi-04.1-01-PLAN.md — 围栏值层与对比度清单的原子重写(tracer:25 个 Radix primitive / 47 个 `--color-*` / 43 对清单)+ 围栏注释 V-12 + 围栏外三处声明(R-1 / R-2 / R-3)与运行时接线证据

**Wave 2** *(blocked on Wave 1 completion)*

- [x] idi-04.1-02-PLAN.md — 守卫加固:CHECK-01 的 tier-1 交替式加宽到覆盖 `radix` 并做变异证明(含「旧交替式会空转」的对照证据);复证 `check-02-contrast.py` 的四条硬失败路径(依赖 01 —— 复证对象是重算后的 43 对清单)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] idi-04.1-03-PLAN.md — UAT 断言改令牌接线(D-14)+ D-13 选择器名 / D-12 期望值修正 + `idi-04-UAT.md` 更新 + C-1 下游门引用复核 + 全量门禁收口

**Wave 4** *(gap closure — blocked on Wave 3 completion; closes VERIFICATION.md's only BLOCKER CR-01)*

- [x] idi-04.1-04-PLAN.md — 关闭 CR-01:让 `check-05-ui-uat.py` 的 `resolve_color` 在令牌未声明时返回 `None`、`ok()` 把 `None` 期望值记 BLOCKED,并用变异证明钉死「修复前 PASS / 修复后 BLOCKED」的对照(新文件 `scripts/probe-05-resolve-color.py`)。范围外项 W-2…W-6 / CR-02 / IN-01…03 与两条人工项显式登记为 deferred,不修

**UI hint**: yes

### Phase 5: 排版与视觉层级

**Goal**: 渲染出的文档与界面 chrome 各有一套受控的排版刻度;产品最重要的一步(不可逆的 G3 授权)在视觉上不再与例行按钮混同;页面级层级正确。
**Depends on**: Phase 4
**Requirements**: TYPE-01, TYPE-02, TYPE-03, VISUAL-01, VISUAL-02, VISUAL-03, VISUAL-04, VISUAL-05

**Rationale**: 用户可见价值最高,承载本里程碑的核心价值发现——"工具目前在对自己说谎":G3 授权按钮与例行「继续自检」在样式上逐字节相同。纯 CSS:面板活动态由 `:not(.hidden)` 推导(无需 JS 状态属性),`<h1>` 由新增的 `#doc-pane > h1` 规则承担,emoji 是 CSS `content`。

**Deliverables**:

- `.markdown-body h1/h2/h3` 的**显式** `font-size`,且**作用域限定在 `.markdown-body` 内**(现无任何 `font-size` 规则,落到 UA 默认 28/21/16.4px——正文的排版刻度由浏览器决定)。
- `#doc-pane > h1` 降级:容器标签不再以约 32px 粗体成为全屏最大最重的文字。
- `#btn-authorize` 的不可逆动作独立处理(实心填充,而非六个按钮共享的淡色底),配保留令牌 `--color-action-irreversible-*`;`#btn-approve-draft` / `#btn-start-writing` 为第二档;例行按钮保持中性。
- 侧栏四个面板的活动/非活动态可区分(纯 CSS 推导)。
- `.annotation-quote::before` 的 `📌` 与 `.verdict-location::before` 的 `📍` 替换为**内联 SVG**(定义一次、引用)。
- markdown 内容排版归入刻度与令牌:`table th/td`、`code`(现 12.5px 分数值)、`blockquote`;字重层级。

**Success Criteria** (what must be TRUE):

1. 渲染出的 DESIGN.md 的 h1/h2/h3 有受控字号(不再由浏览器默认决定),且侧栏面板标题(`.panel-header h2`)、`#draft-view h2`、`#brainstorm-view h2`、`.overlay-card h3` 四处 chrome 覆盖**未被带偏**。
2. `#btn-authorize` 与例行按钮(如「继续自检」)一眼可区分——计算样式不同,且授权按钮的字面文本达 AA。
3. 全屏最大最重的文字不再是容器标签「文档区」。
4. 侧栏当前活动面板(会话流 / 本轮批注流 / 自检报告)可辨认,且 `#ai-panel` 的折叠行为不变。
5. 批注引用与裁决位置两处标记以内联 SVG 呈现,`frontend/vendor/` 无新增文件、无 CDN `<link>`。

**Avoids** (Pitfalls):

- **Pitfall M4 chrome 与正文共用 `h2`**——内容排版一律限定在 `.markdown-body` 下;chrome 标题是**独立**的令牌族。全局 `h1,h2,h3` 规则会与四处 chrome 覆盖碰撞。
- **Pitfall 7 emoji 替换引入图标依赖 / 破坏折叠指示器**——范围锁死为两处 `content:` emoji;不引入图标系统;若触碰 `.collapse-indicator`,`app.js:1550` 用 `textContent` 赋值会**擦掉**内联 `<svg>`(`#ai-panel` 是唯一可折叠面板)。
- **Pitfall M5 弱化 `:disabled`**——它是 G3 前提条件唯一的视觉信号,不得软化。
- **Pitfall 3 / 全局硬规则 5**——不触碰 `renderAnnotations` / `renderVerdictCard`(已验收路径)。
- **Pitfall 9**——追加,不重排(`#brainstorm-view h2` 的 14px / `#8a6508` 是顺序决定的)。

**Research flag**: 标准实践,无需研究阶段。项目特有的碰撞已在上方逐条枚举。
**Gates**: markdown 标题不再解析为 UA 默认(浏览器计算样式实检);`#btn-authorize` 计算样式与 `#btn-continue-check` 不同;`#brainstorm-view h2` 仍解析为 `--text-md` 与 `--color-action-warning`(D-02:改写为令牌接线表述,与 04.1 的 D-14 同构);Phase 4 全部 gate 仍通过。
**Plans**: 4/4 plans executed

Plans:
**Wave 1**

- [x] idi-05-01-PLAN.md — 排版刻度 7 档(`--text-2xl`/`--text-3xl` 与 `.markdown-body h1/h2/h3` 同提交)+ 行高比率配对注释 + 字重三档分工(按钮 600→500,`#btn-authorize` 保留 600)+ TYPE-02 复证

**Wave 2** *(blocked on Wave 1 completion)*

- [x] idi-05-02-PLAN.md — 三段坡道值层重写(commit green-11/white、irreversible green-12/white)+ `#btn-authorize` 字号步进 14→16px + D-04 断言反转(档内相同 / 档间两两不同)+ VISUAL-03 复证

**Wave 3** *(blocked on Wave 2 completion)*

- [x] idi-05-03-PLAN.md — 活动面板标记(`--color-marker-active` + 两处 `box-shadow: inset` 追加规则)+ 两处 emoji 改 `mask-image` 字形 + D-05 连带复验 idi-04.1

**Wave 4** *(缺口闭合 —— 依赖 Wave 3 全部完成)*

- [x] idi-05-04-PLAN.md — 关闭 `G-idi-05-1`(BLOCKER):把标题刻度作用域扩到 `renderMarkdown()` 的全部九个注入目标(五个非 `.markdown-body` 容器取 24 / 18 / 16px + `--fw-semibold`,消除 UA 默认值与第四字重档 700)+ check-05 的枚举改为按调用点并加普查守卫 + 契约补 P-19 / P-20 / A-9

**UI hint**: yes

### Phase 6: 布局稳健性

**Goal**: 布局结构常量只有一个来源;窄窗口不破版;侧栏不再是四个滚动容器的套娃;紧凑控件达到 24×24 命中区。
**Depends on**: Phase 4
**Requirements**: LAYOUT-01, LAYOUT-02, LAYOUT-03, LAYOUT-04, A11Y-07

**Rationale**: **一个不可分的工作单元,不是三件事。** `#state-badge { right: 448px }` 与侧栏宽度决策、以及窄窗口要求彼此纠缠:拆开必然返工。同时这是**回归风险最高的 CSS 阶段**——它改动的是结构性规则,而非新增规则。

**Deliverables**:

- `--sidebar-w` 令牌 + `#state-badge { right: calc(var(--sidebar-w) + var(--space-6)) }`(448px 曾是 420+28,算术只记录在注释里;28 吸附到刻度后为 24)。**采用 `calc()` 版本**(零行为变更的迁移),使窄窗口的 `@media` 块退化为"重赋令牌"而零额外规则。
- 一条 `@media` 守卫(**字面**断点值——CSS 禁止在媒体查询条件中使用 `var()`,该规则会被静默丢弃),范围是"**不破版**"而非"适配":≥1024px 无横向溢出,≥768px 无内容遮挡。
- `#state-badge` 不再遮挡滚动内容;同时解决它与 `#stream-banner` 的 fixed 定位碰撞(1280px 重叠 48px、1024px 重叠 90px,而 z-index 更高的横幅**盖住了唯一的状态读数**)——**不得把 badge 移入正常流**。
- 侧栏滚动容器套娃收敛:删掉 `.event-list` / `#annotation-list` / `#latest-check` 的 `max-height` 与 `overflow-y`,保留 `#chat-messages` 作为唯一合理的第二滚动者(输入行必须钉底);`#session-panel { min-height: 320px }` 改 `flex: 0 0 auto`。
- `#doc-pane { min-width: 0 }` + `.markdown-body { overflow-wrap: anywhere }`(flex 项默认 `min-width: auto` 会被不可断长内容撑破视口)。
- 抬升 `#chat-messages`(2px)与 `#annotation-list`(2px)的 padding——**为 Phase 7 的焦点环解裁切**;padding 落在此阶段,环在 Phase 7 验证。
- A11Y-07:裁决按钮(实测约 21–22px 高)等紧凑控件达 24×24。**边界:若与布局冲突,不得为此重构侧栏**(裁决按钮是为在 420px 侧栏塞下 3 个而故意紧凑的)。

**Success Criteria** (what must be TRUE):

1. 窗口从 1440 收到 768:无横向溢出、无内容被遮挡。
2. `#state-badge` 在所有宽度下都贴在文档区右上角,且**不被 `#stream-banner` 盖住**(1024px 与 1280px 两处实检)。
3. 420px 侧栏内只剩一个滚动条(`#chat-messages` 除外),滚动到侧栏底部时内容可达。
4. 裁决按钮等紧凑控件的命中区达到 24×24,而侧栏结构未被重构。
5. `#brainstorm-view h2` 仍计算为 14px / `#8a6508`(未因结构性改动而变)。

**Avoids** (Pitfalls):

- **Pitfall M2 `#state-badge` / `#stream-banner` fixed 定位碰撞**——见上方;修复不得把 badge 移入正常流。
- **Pitfall 3 UI-6.3 归档只读态**——不得为 DRY 让归档视图复用 `loadRoundView`;`updateFrozenPresentation(true)`(`app.js:1166`)会把 `applyArchiveView` 设的 `disabled = true` 复位。
- **Pitfall 3 UI-6.2 SSE 横幅**——`.fatal` 修饰符必须保留为独立选择器,两态(4.78:1 / 4.76:1)继续达 AA。
- **Pitfall 8 项 3/4**——不重构 header、不做响应式重设计;`#selection-menu` 的定位数学不要"顺手改进"(它在旗舰交互路径上且工作正常)。
- **Pitfall 5 的裁剪面**——padding 改动必须与 Phase 7 同一次发布内落地,不得留出"环被裁切"的窗口。
- **Anti-Pattern 3**——断点值是该规则唯一的合法字面量例外,须在 UI-SPEC 中显式声明为例外,否则会被读成疏漏。

**Research flag**: `calc()` vs `position: absolute` 是真实的行为取舍(fixed 且可能遮挡 vs 随内容滚走)。**本路线图按研究建议提交 `calc()`**——零行为变更的迁移步骤;但该取舍须在规划时与用户确认。A11Y-07 是否与 420px 侧栏冲突也需在规划时实测判定。
**Gates**: 1440 → 1024 → 768 无横向溢出;badge 在每个宽度都在文档区右上角;1024/1280 下横幅不盖 badge;恰好一个侧栏滚动条 + `#chat-messages`;`#brainstorm-view h2` 仍 14px / `#8a6508`;Phase 4 全部 gate 仍通过。
**Plans**: 4 plans (3 executed + 1 gap-closure)

Plans:
**Wave 1**

- [x] idi-06-01-PLAN.md — 徽标收口:`#doc-panel-header { position: sticky; top: 0; background: var(--color-surface); border-radius: 0 }` + check-05 item 8 三条断言(流内机制 / 768·1024·1280 三宽度 badge×banner 不相交 / 滚动到底后表头仍可见)+ 三项只读诊断(三宽度文档级溢出 / 焦点环 clearance 普查 / 命中区普查)落盘为波次 3 的判据基线

**Wave 2** *(blocked on Wave 1 completion)*

- [x] idi-06-02-PLAN.md — 换行与 flex 最小尺寸(六目标 `overflow-wrap: anywhere` + `#main-pane` / `#doc-panel` 各补 `min-width: 0`)+ 滚动容器收敛(删 `.event-list` 与 `#annotation-list` 的 `max-height` / `overflow-y`,保留 `#latest-check` 与 `#chat-messages`)+ check-05 item 9(滚动者 DOM 普查 / 末条可达性 / `max-height == none` / 保留项护栏)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] idi-06-03-PLAN.md — 窄窗口守卫决策(在 L-3/L-4 已落地的树上重测三宽度,按实测决定是否写唯一一条 `@media (max-width: 1023px)`)+ L-6 命中区与 L-5 焦点环解裁切(按元素普查施加 `min-height`/`min-width: 24px` 与条件 padding 抬升)+ item 8/item 9 两条普查门 + D-19 连带复验 `idi-04.1-radix` + 全量门禁收口

**Wave 4** *(gap closure — blocked on Wave 3 completion)*

- [x] idi-06-04-PLAN.md — LAYOUT-02 的 768px 承诺收窄登记(用户裁定 remediation (b)「Narrow the promise, fix the claim」):更正 check-05 item 8 的失效覆盖主张使其陈述实测真相 + UI-SPEC 新增 A-10 收窄行与 §L-2 判据表注解 + 填实 VERIFICATION 的 override 条目 + 就地更正 03-PLAN / 03-SUMMARY 里的同一主张。**零布局改动**

**UI hint**: yes

### Phase 7: 交互状态与焦点样式

**Goal**: 每个交互控件对 hover / active / disabled 有可辨反馈,并有可见的键盘焦点环;过渡限定在明确允许的属性上且尊重减弱动效偏好。
**Depends on**: Phase 4, Phase 6
**Requirements**: INTERACT-01, INTERACT-02, A11Y-01

**Rationale**: **纯追加**——不编辑任何既有规则,回归风险最低。架构研究刻意把它排在布局阶段之后:先做安全的新增工作,再让结构性 diff 独立可审。它对 Phase 6 的依赖是真实的:焦点环会被容器的 padding 裁切(`#chat-messages` 2px、`#annotation-list` 2px、`#sidebar` 0),在布局稳定之前验证环等于"验证一个即将改变的状态"。

**本阶段与 Phase 8 的关系(调和来源冲突):** 研究把"焦点层"(P5)与"tabindex/键盘语义"(P6)拆成两阶段,而硬规则要求"`tabindex` 与 `:focus` 同一次提交落地"。**调和结论:焦点规则作为 CSS 在本阶段先落地,`tabindex` 作为 HTML 在 Phase 8 落地**——硬规则的实质(绝不出现"可聚焦但焦点不可见"的中间状态)因此被满足,且 Phase 8 的提交不是焦点样式第一次出现的地方。Phase 8 依赖 Phase 7 正是为了这条保证。

**Deliverables**:

- `:hover` / `:active` / `:disabled` 覆盖交互控件(基线 2 / 0 / 8);`:disabled` 保持明确不可点且与 `:hover` 可区分。
- 一条全局 `:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px }`,覆盖 21 个按钮 / 8 个输入框 / 4 个下拉(基线 `:focus` 与 `outline` 规则均为 **0**,UA 默认环目前是激活的——本里程碑是**新增**作者化焦点样式,不是恢复被移除的)。用 `outline`,**绝不用 `border`/`padding`**(后者会 reflow `#probe-controls`,Tab 一次按钮跳一次)。
- transition 限定在 `background-color` / `border-color` / `opacity`,约 120–150ms;`@media (prefers-reduced-motion: reduce)` 与任何新增 transition **在同一次提交**。
- 环色对**合成后**背景的验证:`.round-frozen`(0.55)与 `.archive-mode`(0.75)会把环一并合成——`#2c7be5` 满不透明度只有 3.97:1,进入冻结态降到 **2.05:1**、归档态 **2.73:1**,两者都失败。

**Success Criteria** (what must be TRUE):

1. 键盘 Tab 到任一按钮 / 输入框 / 下拉,焦点环清晰可见。
2. 鼠标点击控件**不**出现焦点环(`:focus-visible` 语义成立)。
3. 焦点环在冻结轮次(0.55)与归档态(0.75)下仍可辨认。
4. 把侧栏滚到底部再 Tab,焦点环不被裁切。
5. 交互控件有 hover / active 反馈,而 `#btn-authorize` 的禁用态仍一眼看出不可点(未被软化)。

**Avoids** (Pitfalls):

- **Pitfall 5 全部四种失效模式**——布局位移(border)、裁切(嵌套滚动容器)、被祖先 `opacity` 相乘、以及在数千像素高的盒子上不可见。**不要把环套在 `#round-doc` 整体上**;若文档区需要焦点标识,环 `#doc-pane`。
- **Pitfall M3 全局 transition**——不得写 `* { transition: all }`(`renderEvent` 每个事件都设 `scrollTop`,`.streaming` 类切换会让整块面板闪);不得对 `opacity` 做"平滑隐藏"来对抗 `display: none`,那条路的变通(改 `visibility`/`opacity`)会重新打开 Pitfall 2,并让隐藏内容仍可 Tab 到。
- **Pitfall M5 弱化 `:disabled`**——它是 G3 前提条件唯一的视觉信号。
- **Anti-Pattern 5 `outline: none` 当焦点样式**——保留 outline。

**Research flag**: 标准实践,无需研究阶段(`:focus-visible` + `outline-offset` 文档完备)。项目特有的工作(环色 vs 合成背景)研究阶段已算完。
**Gates**: `grep -c ':focus-visible'` > 0;**没有任何焦点规则设置 `border` 或 `padding`**;每个环都对 0.55 与 0.75 合成背景验过;`prefers-reduced-motion` 与任何新 transition 同提交;Phase 4/6 全部 gate 仍通过。
**Plans**: 3/3 plans executed

Plans:
**Wave 1**

- [x] idi-07-01-PLAN.md — 焦点环端到端(A11Y-01):`--color-focus` 令牌 + 7 选择器 `:focus-visible` 规则 + 三处验证面的 PAIR + `check-05` 第 10 项的元素普查 + 归档半场的一次性反事实探针

**Wave 2** *(blocked on Wave 1 completion)*

- [x] idi-07-02-PLAN.md — 交互态 hover / active / disabled(INTERACT-01):四个新 tier-2 令牌 + L587 选择器的 `:not(:disabled)` gate + 填充按钮 rgba 叠层 + input/select hover 加深

**Wave 3** *(blocked on Wave 2 completion)*

- [x] idi-07-03-PLAN.md — 过渡与减弱动效 + 契约计数门(INTERACT-02):过渡挂载规则 + `@media (prefers-reduced-motion: reduce)` 块 + `EXPECTED_MEDIA_QUERIES` 同步 + 静态契约守卫 + 整阶段收口与指纹披露

**UI hint**: yes

### Phase 8: 可访问性语义与键盘

**Goal**: 键盘用户能真实完成一次划词批注,能 Esc 关闭两个阻塞式弹窗;两个阻塞弹窗向辅助技术宣告的语义与其实现一致;内联错误不再破坏控件行;五条已交付修复的人工验收项全部重跑通过。
**Depends on**: Phase 7
**Requirements**: A11Y-02, A11Y-03, A11Y-05, A11Y-06, A11Y-08, REG-03

**Rationale**: **唯一触碰 `app.js` / `index.html` 的阶段,因而放在最后。** `app.js:4-75` 有约 70 个顶层 `getElementById` 句柄,任何 HTML 编辑删除或改名一个 id 都会在解析期静默杀死其下全部处理器(已记录的 G-idi01-8 失效形态)。**全部 HTML/JS 风险集中于此。** 按代码 diff 面积它是**最小**的阶段——1 个 `tabindex` 属性、2 个弹窗 × 2 个属性、约 8 行焦点交接、约 10 行 Escape 处理——但**每一个改动都可能致命**,必须按这个分量对待。

**关键框定(不是"加属性"):**

- `#round-doc` 的 `tabindex="0"` 是让 `b9664e0` 已交付的 `keyup` 监听器(`app.js:1327`)**第一次真正执行**的东西。`#round-doc` 是普通 `<div>`,其子元素不可聚焦,焦点永不进入该子树——**键盘划词路径今天仍是鼠标专属**,不得把这个"已交付修复"报告为已生效。
- `role="dialog"` 配不上 Escape 关闭,**比不加 role 更糟**:它宣告了一个实现并不兑现的契约。
- 焦点交接是必需项而非镀金:`#selection-menu` 是 `<body>` 里**最后一个**元素(在五个弹窗之后),从 `#round-doc` 起按 Tab 要穿过整个文档区与整个侧栏才能到达它,而任何"失焦即关"的中间可聚焦元素都会让这条路彻底失效。

**Deliverables**:

- `#round-doc` 加 `tabindex="0"` —— 与已存在的 `:focus-visible` 规则**同一次提交**(不得在焦点样式缺席的提交里落地);环落在 `#doc-pane` 或采用内嵌处理(`#round-doc` 有数千像素高,整体环只露出上下边缘)。
- 键盘划词路径的焦点交接:`handleSelectionTrigger` 的键盘分支把焦点移入 `#selection-menu` 首个按钮;Escape 关闭并把焦点交还 `#round-doc`。
- 两个阻塞式弹窗(G3 确认、授权)支持 **Escape 关闭**(G3 确认弹窗按设计是默认拒绝,按不了 Escape 的键盘用户会被卡住),并加 `role="dialog"` + `aria-modal="true"`。**范围锁死为这两个弹窗**——其余 2-3 个非阻塞弹窗的 `role` 与焦点陷阱是 Out of Scope。
- ✅ **REG-02 已完成**(quick `260917-fqh`,`46e8ea3` + `793071e`):`showInlineError(processRoundBtn, …)` 的**结构性修复**已落地——锚点改为 `#probe-controls`(块级流容器,错误落在整行下方全宽;UAT 实测宽度 388px = 探针行宽度 100%),未给 flex 行打 CSS 补丁;三条视图切换路径(轮次切换 / 归档视图 / 撰写视图)已补 `clearInlineError()`。**本相位仍须守住两条回归门**:`grep -c 'inline-error' frontend/style.css` 仍为 1、`clearInlineError` 调用点计数只增不减。**已裁定排除**:`inlineErrorEl` 单例"两个并发错误只显示一个"不是缺陷。
- REG-03:**`b9664e0` 五条修复的全部人工验收项重跑**——本阶段的收口 gate,不是事后补记。

**Success Criteria** (what must be TRUE):

1. 键盘可到达每一个交互控件;Esc 能关闭 G3 确认与授权两个弹窗。
2. 键盘用户能真实完成一次划词批注(**人工检查**——见下方)。
3. 两个阻塞弹窗向辅助技术宣告为模态对话框,且该宣告与实现一致(可 Esc 关闭)。
4. `#probe-controls` 内的错误提示不再被挤成窄列;切换视图不再残留陈旧错误;错误路径仍只用 `textContent`(无 `innerHTML`)。
5. `b9664e0` 五条修复的人工验收项全部重跑通过;`node --check app.js` 通过;pytest 219 基线不变。

**Avoids** (Pitfalls):

- **Pitfall 6 `tabindex` 无 `:focus`,以及路线图把它们拆到两个阶段**——本路线图的解法:焦点规则在 Phase 7 已落地,Phase 8 依赖 Phase 7;gate = `tabindex` 计数与 `:focus` 计数不得独立移动(两者同为零或同为正)。
- **Pitfall 3 全部五条已交付修复**——UI-6.1 键盘选区路径的 UI-6.1 人工 UAT 必须**重跑**:"先聚焦文档区这一步仍需鼠标点击一次"这条已记录的局限不再成立,原先通过的检查现在测的是另一件事。UI-6.3 归档只读态:须在归档切换器**切轮之后**确认「处理本轮批注」不可点(走 `updateFrozenPresentation` 复位路径)。
- **Pitfall 10 内联错误**——含 `textContent` 不变量(它是 XSS 缓解,不是风格选择)与 `clearInlineError` 的视图切换调用。
- **Pitfall M7 `aria-live` 用在流式容器上**——`appendSayToChat` 每个 SSE 事件追加一个 DOM 节点,`aria-live` 绝不可加在 chunk 容器上。本阶段**不加** `aria-live`(用户已裁定为 Out of Scope),记录以防蔓延。
- **Anti-Pattern 6 把 a11y 阶段当成"加属性"**——每条 ARIA 属性必须配对它承诺的行为,并由键盘 UAT 验证。

**Research flag**: ARIA 范围已由用户裁定(窄切片),不再是未决问题。规划时需决定的一处:焦点交接是否属于 A11Y-03 的验收必需项(研究论证"是"——否则键盘用户选完词要按十几次 Tab 才能到达刚触发的菜单;成本约 8 行 JS)。`#round-doc` 的 `role="region"` + `aria-label` 是否随 `tabindex` 一起加,也在同一次决策内。

**Manual checks (本环境无法自动化,必须标注为人工验收):**

- **A11Y-08** —— tab 序到达每一个交互控件;键盘划词路径可用。**本环境无法自动化键盘文本选区(连 `contenteditable` 都选不中),不得因自动测试 FAIL 判定功能缺陷。**
- **A11Y-03 的键盘划词部分** —— Shift+方向键选区 → 菜单出现 → 焦点已入菜单 → Escape 关闭并交还焦点。
- **REG-03 中依赖键盘选区的项** —— 人工重跑,逐项记录步骤与观察结果。
- Playwright 若用于其余运行时验证,**必须** `chromium.launch({ channel: 'chrome' })`;本环境**截图不可用**(headless 渲染被挡,且常驻 `/api/events` SSE 流使采集处理器无法终止)——按计算样式检查 + 具名人工步骤规划,不要规划视觉 diff。

**Gates**: 键盘路径人工验收通过;`node --check app.js`;pytest 219 基线不变;归档路径在切轮后无可点「处理本轮批注」;`grep -c 'inline-error' style.css` 仍为 1;`clearInlineError` 调用点计数只增不减;Phase 4/6/7 全部 gate 仍通过。
**Plans**: 3/3 plans executed

Plans:
**Wave 1**

- [x] idi-08-01-PLAN.md — `#round-doc` 的 Tab 停靠点与整盒焦点环 + 键盘划词手势与焦点交接(A11Y-02 + A11Y-03):`tabindex="0"` 端到端(零 CSS 环)+ Shift 专用提交监听器 + `hideSelectionMenu()` 单点交还 + 环可辨性实测与 D-02 判定 + probe-07 复跑

**Wave 2** *(blocked on Wave 1 completion)*

- [x] idi-08-02-PLAN.md — 两个弹窗的 dialog 语义、Escape 与背景 inert(A11Y-05 + A11Y-06):2 个新 id + `role`/`aria-modal`/`aria-labelledby` + `syncBackgroundInert()` 单点派生(5 个调用点)+ `#tier-modal` 移焦 + Escape 单点分派器 + `tierModalShown` 复位 + F1-d 两条交还

**Wave 3** *(blocked on Wave 2 completion)*

- [x] idi-08-03-PLAN.md — 验收与回归收口(A11Y-08 + REG-03):S8-1 一个词的文案修正 + 两条 REG-02 门 + pytest 基线 + REG-03 六条人工项全量重跑(第 4 条按 D-05 重写)+ 归档切轮专项 + Tab 序全量普查 + 指纹义务登记

**UI hint**: yes

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. 行走骨架 | v1.13 | 4/4 | Complete | 2026-09-09 |
| 2. 轮次收敛循环 | v1.13 | 4/4 | Complete | 2026-09-10 |
| 3. 授权、自检与终点 | v1.13 | 5/5 | Complete | 2026-09-13 |
| 4. 设计契约、令牌层与契约校验 | v1.14 | 3/3 | Complete    | 2026-09-20 |
| 4.1. Radix 颜色族重写 | v1.14 | 4/4 | Complete    | 2026-09-20 |
| 5. 排版与视觉层级 | v1.14 | 4/4 | Complete    | 2026-09-21 |
| 6. 布局稳健性 | v1.14 | 4/4 | Complete    | 2026-09-22 |
| 7. 交互状态与焦点样式 | v1.14 | 3/3 | Complete    | 2026-09-23 |
| 8. 可访问性语义与键盘 | v1.14 | 3/3 | In Progress|  |

**Execution Order:** Phases execute in numeric order: 4 → 4.1 → 5 → 6 → 7 → 8

Phase 5/6/7 相互独立,理论上可重排——但有两条不可动:**Phase 4 不得移动**(四个阶段消费它),**Phase 6 不得移到 Phase 7 之后**(焦点环依赖布局稳定)。

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

---
phase: "8"
slug: "idi-08-accessibility-semantics-and-keyboard"
status: approved
reviewed_at: "2026-09-23T12:29:15Z"
shadcn_initialized: false
preset: none
created: "2026-09-23"
supersedes_decisions:
  - "ROADMAP Phase 8 交付物的「两个阻塞式弹窗(G3 确认、授权)」→ D-11 按实测替换为 #confirmation-modal + #tier-modal"
  - "ROADMAP Phase 8 交付物的「handleSelectionTrigger 的键盘分支把焦点移入 #selection-menu 首个按钮」→ D-05/D-06 替换为独立 Shift 监听器 + 抬起 Shift 提交"
  - "ROADMAP Phase 8 交付物的「环落在 #doc-pane 或采用内嵌处理」「整体环只露出上下边缘」→ D-01 用整盒环;PITFALLS 5 失效模式 4 被几何推翻(且 #doc-pane 这个选择器在 HEAD 上根本不存在)"
  - "PITFALLS §Pitfall 6 的「prefer not adding tabindex to #round-doc」反对意见 → 用户已裁定加(D-01/D-18),以窄切片接受「通用容器」的宣告代价"
  - "ROADMAP Phase 8 SC2/SC3 的「Esc 能关闭 G3 确认与授权两个弹窗」→ 对象集按 D-11 替换"
  - "frontend/style.css L1499-1501 围栏注释的「Phase 8 加 tabindex 时连同它自己的内嵌处理一起落地」→ D-01 不做内嵌(除非 D-02 触发);注释留证不改(零 CSS 改动)"
  - "06-UI-SPEC.md §Copywriting Contract 冻结的 app.js:1121 文案「在左侧文档划词即可批注。」→ 与 DESIGN.md §4.1(文档面板在右)矛盾;**用户 2026-09-23 裁定:修**(改为「在右侧文档」),见 §Sign-Off Items S8-1(已 RESOLVED)"
---

# Phase 8 — UI Design Contract(可访问性语义与键盘)

> 前端阶段的视觉与交互契约。由 `gsd-ui-researcher` 生成,由 `gsd-ui-checker` 验证。

## 权威声明 —— 用本文件之前先读这一节

**本文件是一份交互/状态契约,刻意不是视觉契约。** Phase 8 的整个 diff 是
`frontend/app.js` + `frontend/index.html`,`frontend/style.css` **零改动**(D-01)
⇒ **本阶段零新增令牌、零视觉变更、零新增依赖、零新增文件。**
它锁的是**键盘路径与两个弹窗的交互与状态契约**,以及把三条已签核偏离登记成
「刻意,不是遗漏」,使下游读不出漂移。

**与上游契约的关系:**

| 节 | 权威来源 |
|---|---|
| `## 键盘契约`(本文件) | **本文件** —— 它是全新的。`DESIGN.md` 全文对键盘 / 无障碍 / 焦点 / `tabindex` / Escape / ARIA **零提及**(已核实)⇒ 本阶段是在**零可访问性设计契约**下建立契约 |
| `## 弹窗契约`(本文件) | **本文件** —— 全新;五个 `.overlay` 此前无任何语义声明(`grep -c 'role=' frontend/index.html` = **0**,实测) |
| `## Spacing Scale` | `04-UI-SPEC.md`(S-1,12 档,已签核)—— **本阶段零消费、零改动** |
| `## Typography` | `idi-05-UI-SPEC.md`(7 档字号 / 3 档字重 / 4 档行高)—— **零改动** |
| `## Color` / 对比度 | `idi-04.1-UI-SPEC.md`(25 tier-1 / 47 tier-2 / 47 对)—— **零改动、零新增令牌** |
| 焦点环的几何与枚举 | `idi-07-UI-SPEC.md` + `style.css:1508-1517` —— 本阶段**只消费它,不修改它** |
| Global Hard Rules 1–7 | `ROADMAP.md` §全局硬规则 + `04-UI-SPEC.md` —— 本文件复述并**追加 8–12** |
| Do-Not-Touch List | `04/05/06-UI-SPEC.md` —— 本文件只**追加**本阶段的条目 |

**用本文件之前必须知道的六件事:**

1. **零 `style.css` 改动是本阶段最大的一条流程性质(D-01)。** 因为 `app.js` / `index.html`
   不在任何 live 报告的 `covered_files` 里 ⇒ **Phase 8 在 D-01 路径下不欠任何验证指纹**。
   唯一会打破它的动作是 D-02 的升级(实测判定整盒环不可辨 ⇒ 改 CSS ⇒ 作废 5 份 live 指纹)。
2. **按 ROADMAP 字面实现会假绿(D-05)。** 路线图写「`handleSelectionTrigger` 的键盘分支把焦点
   移入菜单首按钮」,而该函数挂在**每一次** `keyup` 上 ⇒ 键盘用户永远只能选中一个字符;
   而 A11Y-03 的验收项「Shift+方向键选区 → 菜单出现 → 焦点已入菜单」**会照常通过**
   (它测状态,不测可用性)。**必须按 §键盘契约 K-2 的手势实现。**
3. **两条点名对象被实测替换:** 弹窗对象集(D-11)与键盘提交手势(D-05)。两者都是
   「路线图点名的对象是错的」这一形态的第四次与第五次复现(前两次:Phase 6 A11Y-07、
   Phase 7 D-02)。
4. **本阶段是唯一触碰 `app.js` / `index.html` 的阶段。** `app.js:4-75` 有约 70 个顶层
   `getElementById` 句柄,**改名或删除一个 id 会在解析期静默杀死其下全部处理器**
   (已记录的 G-idi01-8 失效形态)。**新增 id 是安全的**(硬规则 5 禁的是改名与删除)。
5. **环境事实(不得重新推导、不得对抗):** 截图不可用(headless 渲染被阻,且常驻
   `/api/events` SSE 流让采集处理器无法终止)⇒ **用计算样式检查 + 具名人工步骤,不要计划视觉 diff**;
   若用 Playwright **必须** `chromium.launch({ channel: 'chrome' })`(或按 `check-05-ui-uat.py`
   头部的 `--browser` 策略);**键盘文本选区无法自动化**(连 `contenteditable` 都选不中)
   ⇒ A11Y-08 / A11Y-03 键盘半场 / REG-03 第 4 条**必须**是具名人工验收,
   **不得因自动测试 FAIL 判定功能缺陷**。
6. **`inert` 与 `.hidden` 是两个正交机制,不要互相替代**(硬规则 12)。`.hidden` 管显隐,
   `inert` 管「背景对辅助技术与指针惰性」;后者是让 `aria-modal="true"` 的宣告成真(D-14)。

---

## Design System

| Property | Value |
|----------|-------|
| Tool | none |
| Preset | not applicable |
| Component library | none — native HTML/JS, no framework(DESIGN.md D-06) |
| Icon library | none. 两个内联 `mask-image` 数据 URI 字形(Phase 5 / VISUAL-05)—— 本阶段零新增字形 |
| Font | `-apple-system, "PingFang SC", "Helvetica Neue", sans-serif`(未变) |
| Token substrate | 原生 CSS 自定义属性(单一围栏 `:root`)。**本阶段围栏内零改动** |
| Build step | none(D-06)。无 Tailwind / PostCSS / Sass / lint 流水线 |

**Design-system gate:** `components.json` / `tailwind.config.*` / `package.json` 均**不存在**;
技术栈是 Python + FastAPI + 原生 HTML/JS。shadcn **不适用**且未被提议 —— 硬约束 D-06 禁止框架与
构建步骤。**无 registry 门适用**(见 §Registry Safety)。

---

## Component Inventory

**本节按模板在 `Tool: none` 时整节省略。** 为满足下游的 provenance 判据,在此保留其唯一一行:

Could not enumerate: 本项目没有设计系统包可枚举 —— 无 `components.json` / `package.json` /
`node_modules`,前端是原生 HTML/JS + 一份 1697 行的 `style.css`(DESIGN.md D-06 禁止框架与构建步骤)。

本阶段的「组件」是 `frontend/index.html` 里既有的 **80 个 id** 与 `frontend/app.js` 里的既有函数,
其清单以磁盘现状为唯一事实。**本阶段新增 2 个 id、新增 1 个顶层 DOM 句柄、零新增文件、零新增依赖。**

---

## 本阶段的改动面(唯一事实)

| 文件 | 改动 | 依据 |
|---|---|---|
| `frontend/index.html` | `#round-doc`(L139)加 `tabindex="0"` | A11Y-02 / D-01 |
| `frontend/index.html` | 两个 `<h3>`(L172 / L186)各加一个**新** id | D-15 |
| `frontend/index.html` | `#confirmation-modal`(L170)/ `#tier-modal`(L184)的 `.overlay` 加 `role="dialog"` + `aria-modal="true"` + `aria-labelledby` | A11Y-06 / D-14 / D-15 |
| `frontend/app.js` | Shift 提交监听器(约 6 行,落 `initSelectionMenu()` 内) | A11Y-03 / D-05 / D-06 |
| `frontend/app.js` | Escape **单点分派**监听器(约 12 行) | A11Y-05 / D-08 / D-12 / D-13 |
| `frontend/app.js` | 焦点交接:菜单首按钮 / 菜单项执行后 / Escape 交还(三处) | D-05 / D-07 / D-08 |
| `frontend/app.js` | 焦点交接:**两个弹窗关闭后各交还一个目标**(`#btn-authorize` / `#btn-continue-check`) | **A-8(用户 2026-09-23 裁定采纳)** |
| `frontend/app.js` | `inert` 的**单点派生函数** + 5 个调用点 | D-14 |
| `frontend/app.js` | `#tier-modal` 打开时移焦 + Escape 时复位 `tierModalShown` | D-13 / D-16 |
| `frontend/app.js` | 新增 1 个顶层句柄 `const appEl = document.getElementById('app')`(**新增,不是改名**) | D-14 |
| `frontend/app.js` | **`app.js:1121` 的一处用户可见字符串**:`在左侧文档` → `在右侧文档`(空态文案;**仅此一个词**,见 §Sign-Off Items S8-1) | S8-1(用户 2026-09-23 裁定) |
| `frontend/style.css` | **零改动**(围栏内与围栏外都是) | D-01 |
| `scripts/check-05-ui-uat.py` | **零改动** —— 保住零指纹债务 | D-21 |
| `scripts/check-01…04` | 零改动;四条守卫必须仍然通过 | §契约校验命令 |
| `frontend/vendor/` | 仍只有 `marked.min.js` | 硬规则 6 |

**属性级规格(执行器的逐字落点):**

| # | 落点(HEAD 行号) | 现值 | 目标值 |
|---|---|---|---|
| 1 | `index.html:139` `<div id="round-doc" class="markdown-body">` | 无 `tabindex` | 加 `tabindex="0"` |
| 2 | `index.html:172` `<h3>授权确认</h3>` | 无 id | 加 `id="confirmation-modal-title"` |
| 3 | `index.html:186` `<h3>选择自检档位</h3>` | 无 id | 加 `id="tier-modal-title"` |
| 4 | `index.html:170` `#confirmation-modal` 的 `.overlay` | 无 `role` / `aria-*` | 加 `role="dialog" aria-modal="true" aria-labelledby="confirmation-modal-title"` |
| 5 | `index.html:184` `#tier-modal` 的 `.overlay` | 无 `role` / `aria-*` | 加 `role="dialog" aria-modal="true" aria-labelledby="tier-modal-title"` |

**两个新 id 的命名裁定(Claude's Discretion,D-15 授权):** `confirmation-modal-title` /
`tier-modal-title`。判据:与既有 kebab-case 命名风格一致(`confirm-word-input` / `tier-modal` /
`btn-tier-loose`)、**实测零碰撞**(`grep` 于 `index.html` / `app.js` / `style.css` 三处均为 0)、
且**是新增而非改名**(硬规则 5 安全)。文案**不复制**:`aria-labelledby` 指向弹窗内既有的 `<h3>`,
使「无障碍名称」与「屏幕上的标题」是同一处真相(「名必须说实话」)。

---

## 基线与契约漂移口径(实测,不采信上游文档)

**D-01:以磁盘 HEAD 为唯一现实基线。** 规划与执行一律以 `frontend/app.js` /
`frontend/index.html` 的磁盘现状为准;`ROADMAP.md` Phase 8 段、`PITFALLS.md` 的相关论断
**仅作意图参考**(其两处关键论断已被本阶段推翻,见 §契约修正登记)。

### 执行前基线(本次会话实测,2026-09-23)

| 命令 | 实测值 | 期望/用途 |
|---|---|---|
| `node --check frontend/app.js` | **OK** | 零语法错误 |
| `grep -c 'inline-error' frontend/style.css` | **1** | REG-02 门①的基线 |
| `grep -c 'clearInlineError();' frontend/app.js` | **9** | REG-02 门②的基线(**不是 6**,见漂移项 3) |
| `grep -c 'clearInlineError' frontend/app.js` | **10** | = 9 调用 + 1 定义行(L303) |
| `grep -c tabindex frontend/index.html` | **0** | Pitfall 6 门:本阶段后应为 **1** |
| `grep -c tabindex frontend/app.js` | **0** | 本阶段后应仍为 **0**(`app.js` 不写 `tabindex`) |
| `grep -c ':focus-visible' frontend/style.css` | **9** | 本阶段后应仍为 **9**(零 CSS 改动) |
| `grep -c '^\.hidden {' frontend/style.css` | **1** | 硬规则 1 |
| `grep -c '!important' frontend/style.css` | **5**(4 行注释散文 + 1 条声明) | 硬规则 2 的**声明**数为 1,由 `check-04` 判定 |
| `grep -c 'role=' frontend/index.html` | **0** | 本阶段后应为 **2**(两行,每行一个) |
| `grep -o 'aria-modal' frontend/index.html \| wc -l` | **0** | 本阶段后应为 **2** |
| `grep -o 'aria-labelledby' frontend/index.html \| wc -l` | **0** | 本阶段后应为 **2** |
| `grep -c 'aria-' frontend/index.html` | **0** | 本阶段后应为 **2 行**(算术陷阱:`grep -c` 数**行**,不数出现次数 ⇒ 用上面的 `-o \| wc -l` 写门) |
| `grep -c 'inert' frontend/index.html frontend/app.js` | **0 / 0** | 本阶段后 `app.js` 应为非零(`index.html` 保持 0 —— 属性由 JS 挂) |
| `bash scripts/check-01…04` | **四条全 PASS,exit 0** | 必须保持 |
| `python3 scripts/check-02-contrast.py` | **PASS: 0 failures**(47 对 + ORDER 0.363) | 零颜色改动 ⇒ 必须逐字不变 |
| `.venv/bin/python -m pytest -q -m "not slow"` | **219 passed + 6 skipped / 225 collected** | 见漂移项 2 |

### 三条契约漂移(逐条登记,全部由实测产生)

| # | 上游/本文件上游的声称 | 实测 | 本阶段处置 |
|---|---|---|---|
| 1 | ROADMAP Phase 8 交付物:「环落在 `#doc-pane` 或采用内嵌处理」;PITFALLS 5 失效模式 4:「整体环只露出上下边缘」 | `#doc-pane` **在 HEAD 上不存在**(04.1 D-13 已改名 `#doc-panel-body`);`#doc-panel-body { padding: 32px 40px }`(`style.css:657`)⇒ `outline-offset: 2px` 的环外伸 2–4px 落在 40px padding 里、**不被裁切**;`#round-doc` 盒高数千像素 ⇒ 视口里是**左右两条贯穿全高的竖线** | **按 D-01 用整盒环,零 CSS 改动。** 两条论断作废(§契约修正登记 A-3) |
| 2 | ROADMAP Phase 8 Gates:「pytest 219 基线不变」;**Phase 4 段**写「225」 | 实测 `219 passed + 6 skipped / 225 collected` —— 219 是**通过数**、225 是**收集数**,两者不是一回事 | **门的判据是「219 passed + 6 skipped」**(D-24)。照抄「225」会造出必然失败或必然通过的假门 |
| 3 | **`08-CONTEXT.md` D-21 的基线口径:「`clearInlineError` 调用点基线 6 个」** | **实测 9 个**(`grep -c 'clearInlineError();' frontend/app.js` = 9;L311 / L320 / L461 / L603 / L822 / L1252 / L1461 / L1511 / L1535) | **门的基线取实测 9**(§契约校验命令)。照抄 6 会造出一条**永远不会失败**的假门 —— 与本项目反复警告的 gate 算术错误同型 |

**不得重新推导的两条(已实测,直接采用):**

- 五个状态样本(p1 / p12 / p3 / checking / archive)里 `#round-doc` 内 `a[href]` 计数为 **0**;
  `#round-doc` 在 **p1 / p12 里不可见**(落在 `.hidden` 子视图内)⇒ 被普查的 `visible` 过滤排除,
  只有 **p3 / checking / archive** 三个样本会真的把它纳入判定集(D-03)。
- 全文件 `.focus()` 调用**只有一处**:`app.js:488` 的 `confirmWordInput.focus()`。

---

## 焦点契约的单一不变量(本阶段全部焦点行为的唯一判据)

> **F1:焦点永远不停在一个不可见元素上,也永远不因隐藏而回落到 `<body>`。**

**理由(不是风格选择):** 两条都会让键盘用户丢失位置,而「从 `#round-doc` 起按 Tab 要穿过整个
文档区与整个侧栏才能到达菜单」正是 ROADMAP Phase 8 关键框定第三条点名的成本。
F1 在本阶段有**四个落点**,全部是它的实例:

| # | 落点 | 机制 | 依据 |
|---|---|---|---|
| F1-a | 菜单被隐藏时,若焦点在菜单内 ⇒ 交还 `#round-doc` | `hideSelectionMenu()` **单点** | D-08 |
| F1-b | 菜单项执行后 ⇒ 交还 `#round-doc` | 同上(两个菜单项都先调 `hideSelectionMenu()`) | D-07 |
| F1-c | Escape 关菜单 ⇒ 交还 `#round-doc` | 同上 | D-08 |
| F1-d | **弹窗关闭后 ⇒ 交还触发者**(confirmation → `#btn-authorize`;tier → `#btn-continue-check`) | Escape 分支内 | **A-8:用户 2026-09-23 裁定采纳**(镜像 D-07/D-08;见 §契约修正登记 A-8) |

**F1 不覆盖的两种情形(显式登记,不是遗漏):**
① **成功路径不交还**:`#confirmation-modal` 的「放行」成功后整个视图即将切换(`refreshRoundsAfterStream()`),
此时把焦点钉回 `#btn-authorize` 是错的(它下一刻就随 `#authorize-row` 一起隐藏)—— 故
**交还只写在 Escape 分支里,不写进 `closeConfirmModal()`**;
② **目标不可聚焦时静默降级**:`#btn-authorize` 若在弹窗打开期间变成 `disabled`(Chrome 下
`.focus()` 对禁用按钮是 no-op),焦点停在原处 —— 登记为已知边界,**不新增兜底逻辑**。

---

## 键盘契约 K-1 —— `#round-doc` 的 Tab 停靠点与整盒焦点环(A11Y-02)

### K-1.1 交付物:一个属性,零 CSS

`index.html:139` 的 `<div id="round-doc" class="markdown-body">` 加 **`tabindex="0"`**。
**这是本阶段唯一一处 HTML 属性变更就换来一条完整交互路径的地方** —— 因为 Phase 7 的
枚举规则 `[tabindex]:focus-visible`(`style.css:1514`)是**刻意**为这一刻预留的
(Phase 7 D-05「枚举含 `[tabindex]`」的设计意图就是让本阶段零 CSS 履约)。
落 `tabindex="0"` 的瞬间:

```
[tabindex]:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px }
```

自动生效 —— **不得新增任何 `:focus` / `:focus-visible` 规则,不得写 `#round-doc:focus` 之类的
专用规则**(那会与 Phase 7 的枚举集分叉,正是 G-idi-05-1 的成因)。

### K-1.2 环的几何与「可辨」的判据(实测证据,规划期必须写进计划)

| 事实 | 值 | 来源 |
|---|---|---|
| 环色 | `--color-focus: #1f63bd` | `style.css:259` |
| 环几何 | `outline: 2px` + `outline-offset: 2px` ⇒ 外伸 4px | `style.css:1515-1516` |
| `#round-doc` 的盒宽 | 面板宽 − 80px(父级 `#doc-panel-body` 的 `padding: var(--space-8) var(--space-10)` = `32px 40px`) | `style.css:657` |
| 盒高 | 数千像素(远超视口) | 轮次文档的实际内容长度 |
| 裁切面 | 环画在边框盒**外** 2–4px,落在父级 40px 水平 padding 里 ⇒ **不被裁切** | 几何 |
| 视口里的形态 | **左右两条贯穿全高的竖线**(不是「只有上下边缘」) | 几何 |

**⇒ PITFALLS 5 失效模式 4 的「只有上下边缘可见」被几何推翻。** 规划期必须把这条实测证据写进计划
(本项目已记录的纪律:**实测驱动,不采信上游文档的论断**)。

**「可辨」的两半判据(缺一不可):**

- **机器半场 —— 已被现成的门自动覆盖,不新写断言(D-03):** `check-05-ui-uat.py --item 10` 的
  元素普查会把 `#round-doc` 纳入判定集(判定集 = `FOCUSABLE_SELECTOR` 去掉 `[tabindex="-1"]`
  与 `:disabled`,再经 `visible` ∧ `focusable` 过滤),对它断言 `:focus-visible` 下的计算
  `outline-width` / `outline-color` 非零且等于 `("2px", rgb(31, 99, 189))`。
  **登记两处变化:** ①判定集在 **p3 / checking / archive** 三个样本里多一个成员;
  ②`_idi07_tab_drive(page, len(data) + 8)` 的上限是**数据驱动**的 —— 判定集 +1 使上限 +1,
  而 Tab 序也多一个停靠点(+1),两者恰好相抵,**无需改门**(但必须在计划里登记这条算术)。
  **若该项在某个样本变红,先判它是「真缺陷」还是「普查集变化」,不要直接改门。**
- **人半场 —— 具名人工步骤(A11Y-08 的一部分):** 进 p3 样本 → 按 Tab 直到焦点落在轮次文档区 →
  观察:①环是否为**左右两条贯穿视口全高的竖线**;②环与 `#doc-panel` 背景(`#f9f9f9`)是否
  一眼可区分(实测 5.62:1,远高于 3:1 非文本下限);③环是否压住正文首字/末字(整盒环**不应**压字)。
  **判据「不可辨」的定义(触发 D-02 的唯一条件,须逐条记录观察结果):**
  环的任一段被裁切 **或** 与相邻像素对比 < 3:1 **或** 无法据此定位焦点在哪。
  **不得把「不可辨」静默降级为已知局限** —— 那会造出「名义上可聚焦、实际看不出焦点在哪」的状态,
  正是 Pitfall 6 的失效形态。

### K-1.3 D-02 的升级路径(已签核;由实测触发,不是备选偏好)

**若实测判定整盒环不可辨 ⇒ 当场升级为改 `frontend/style.css`,并接受作废 5 份 live 指纹
(`idi-04` / `idi-04.1-radix` / `idi-05` / `idi-06` / `idi-07`)、连带复验(D-25)。**
两条备选承载面(二选一,由实测与规划期裁定),**本文件给出一条建议但不替用户裁定**:

| 备选 | 形态 | 代价 | 建议 |
|---|---|---|---|
| **B-1 内嵌环** | `#round-doc:focus-visible { outline-offset: -2px }` | 实测:`.markdown-body` **无内边距**(`style.css:891-894` 只有 `line-height` 与 `font-size`)⇒ 内嵌竖线**压在每行正文的首字与末字上** | **不推荐** |
| **B-2 页头环** | `#doc-panel:has(#round-doc:focus-visible) #doc-panel-header { outline: 2px solid var(--color-focus); outline-offset: -2px }` | 36px 高的紧凑环,画在恒可见的 sticky 页头(`style.css:641-646`)上;不与正文重叠;`:has()` 有 Phase 6 的 `:has(:empty)` 先例 | **推荐** |

**走升级路径时必须一并登记:** ①`style.css` 从「零改动」变为「+1 条规则」;
②5 份 live 指纹**以 HEAD 内容重算**、**不要看 mtime**(stale 有两种成因:内容真变 vs 记账性编辑,
补救方向相反);③`check-05` 的 `EXPECTED_FOCUS_VISIBLE_MIN` 等静态计数门是否受影响;
④§Deliberate Delta Ledger 的 **D8-9** 由「条件项」转为实际项。
⚠ **不得用 `gsd-tools query verification status <phase>` 判定 stale** —— 本项目已记录:这些相位目录
一律返回 `missing`(相位目录命名与工具的相位令牌解析不匹配)。

### K-1.4 刻意不做的四件事(知情接受,不是疏漏)

| # | 不做 | 理由 | 依据 |
|---|---|---|---|
| 1 | **不给 `#round-doc` 加 `role`,也不加 `aria-label`** | 加了 `tabindex` 之后它是一个**裸 `<div>` 的 Tab 停靠点**,辅助技术只会报「通用容器」—— **知情接受的代价**。理由取自用户自己立的立场:REQUIREMENTS 的 Out of Scope 表把「完整 ARIA」排除的原话是「ARIA 服务于不带上下文到达、且看不见屏幕的用户;本工具恰好一个用户,既是作者也看得见屏幕」 | D-18 |
| 2 | **不加任何键盘划词的可发现性提示** | 新路径全流程唯一的视觉信号就是焦点环 —— **没有任何东西告诉键盘用户 Shift+方向键能划词**。**已登记的后果:这个缺口不会让任何门变红**(A11Y-08 的人工验收由知道步骤的用户执行),所以要**显式登记**而不是假装被覆盖 | D-19 |
| 3 | **阶段 1-2 的 `#draft-content`(同为 `.markdown-body`)不加 `tabindex`** | 这是**正确的**、不是漏项:`handleSelectionTrigger` 的第一条实质守卫是 `if (currentState !== 'phase3') return`(`app.js:1327`)⇒ 阶段 1-2 根本没有批注功能,给它加 Tab 停靠点是**死代码**(违反「不声明不被消费的东西」的纪律,且无法被运行时验证)。**规划期必须把这条理由写进计划**,否则会被读者当成「A11Y-02 只点名了 `#round-doc`」的漏项去补 | D-20 |
| 4 | **`#selection-menu` 不加 `tabindex="-1"`** | 焦点落在首按钮即可,菜单容器不需要成为焦点目标。加它会引入一个「可被程序聚焦但永远不在 Tab 序里」的元素,且它会被 item 10 的普查**排除**(`focusable` 判据显式排除 `tabindex="-1"`)—— 零收益、多一个需要解释的例外 | 本文件裁定 |

### K-1.5 鼠标路径的行为变化(D-09,必须复跑 REG-03 第 4 条)

`tabindex="0"` 的 `<div>` **被鼠标点击即获焦**(但鼠标点击**不**匹配 `:focus-visible`,
所以不出环 —— SC2 的语义仍成立)。后果:**鼠标用户 Shift+点击扩选后,松开 Shift 也会把焦点
送进菜单**。判定为**可接受**(焦点去的正是用户接下来要点的地方),但必须:
①写进计划;②复跑 REG-03 的人工检查第 4 条;③登记于 §Deliberate Delta Ledger 的 **D8-2**。

### K-1.6 Pitfall 6 的门的形态(本阶段必须写对)

ROADMAP 的门是「`tabindex` 计数与 `:focus` 计数**不得独立移动**」。
**在本阶段这个门由构造满足:** `tabindex` 由 **0 → 1**,`:focus-visible` 由 **9 → 9** ——
看似「独立移动」,实则不然:Phase 7 已把 `[tabindex]` 写进枚举集,**环的承载面在本阶段之前
就已经落地**(这正是 Phase 7 与本阶段拆两阶段的调和结论)。
**机械证据不是计数,是 `check-05 --item 10` 的运行时读数**(`#round-doc` 成为
`document.activeElement` 的那一刻读到 `2px / rgb(31, 99, 189)`)—— 计数只证明规则存在,
运行时读数才证明它套在了新停靠点上。**规划期必须把这条「为什么 0→1 / 9→9 不构成违规」写进计划。**

### K-1.7 焦点序契约(SC 2.4.3)

新增停靠点在 Tab 序里的**位置** = `#round-switcher`(`index.html:136`)**之后**、
`#authorize-row` 的按钮(可见时)**之前** —— 因为它落在 `rounds-placeholder` 子视图内的
`#rounds-hint`(非可聚焦 `<p>`)与 `#authorize-row` 之间。人工验收须逐项记录这个位置
(它是 A11Y-08 的一部分),**不得只记「Tab 能到」**。

### K-1.8 探针复跑义务(D-04)

`#round-doc` 入册后**必须复跑** `scripts/probe-07-focus-composite.py`
(`.venv/bin/python scripts/probe-07-focus-composite.py`)。原因:STATE.md 的 Deferred Items 已逐字登记
「Phase 8 给 `#round-doc` 加 `tabindex="0"` 后该场景变为活体,届时须复跑该探针」——
五个样本的 `#round-doc` 内 `a[href]` 计数为 0 ⇒ `.archive-mode` 0.75 合成下的**运行时**环断言
今天无服务对象,由常驻算术门(`check-02` 的 `--color-focus ON --color-surface NON-TEXT@0.75`,3.45 ≥ 3)
+ 该一次性探针共同承担。**探针不进守卫契约**(与 `scripts/probe-05-resolve-color.py` 同定位)。
**实测其 Tab 驱动是数据驱动的**(上限 40 次、命中即停)⇒ 新增的 Tab 停靠点会被自然吸收,
**但复跑时必须逐字记录「探针的注入前/注入后计数仍为 0 / 1」**,否则无法区分「探针在工作」与
「探针静默空转」。

---

## 键盘契约 K-2 —— 键盘划词手势与焦点交接(A11Y-03)

### K-2.1 手势:抬起 Shift 提交(锁定)

**契约:** 按住 Shift 扩选时**焦点不动**(扩选全程不被打断);**松开 Shift** 时菜单弹出
并把焦点送入 `#selection-menu` 的首个按钮(`#btn-annotate`)。

**为什么必须有提交手势(本阶段最重要的机制事实,规划期必须写进计划):**
`roundDoc.addEventListener('keyup', handleSelectionTrigger)`(`app.js:1350`)对**每一次** keyup 都触发。
若照 ROADMAP 字面「keyup 分支把焦点移入菜单首按钮」实现:Shift+→ 选中 1 个字符 ⇒ keyup ⇒
焦点跳到 `#btn-annotate` ⇒ 再按 Shift+→ 时事件目标已是菜单按钮,`roundDoc` 的 keyup 不再触发,
且浏览器不会给按钮内的文本扩选 ⇒ **键盘用户永远只能选中一个字符**。
而 A11Y-03 的验收项「Shift+方向键选区 → 菜单出现 → 焦点已入菜单」**会照常通过** ——
**它测的是状态,不是可用性。** 这与 Pitfall 6 的「人工检查被继承而非重跑」是同一失效类。

### K-2.2 实现落点(逐字)

**在 `initSelectionMenu()`(`app.js:1344`)内、紧跟 `app.js:1350` 的 `keyup` 绑定之后**新增:

```js
  // 键盘划词的提交手势(D-05):松开 Shift 才把焦点送入菜单首按钮。
  // 为什么不写在 handleSelectionTrigger 里:那个函数挂在**每一次** keyup 上,
  // 在里面移焦会让键盘用户永远只能选中一个字符(见 UI-SPEC §K-2.1)。
  // 判据三条同时成立才移焦,任一条不成立即 no-op(D-06):
  //   ① e.key === 'Shift' ② 菜单可见 ③ 选区非折叠。
  // 空选区 / 折叠选区 / 菜单已隐藏,都由 handleSelectionTrigger 的既有守卫处理。
  document.addEventListener('keyup', (e) => {
    if (e.key !== 'Shift') return;
    if (selectionMenu.classList.contains('hidden')) return;
    const selection = window.getSelection();
    if (!selection || selection.isCollapsed) return;
    annotateBtn.focus();
  });
```

**D-06 的白名单边界(围栏注释必须写清,否则会被后来的读者当成违例删掉):**
`handleSelectionTrigger` **一字不改** —— 它挂在每一次 keyup 上,给**它**加按键白名单会改变
鼠标路径与既有 t8g 决定的实质。**白名单只存在于这个新增的 Shift 专用监听器里。**
t8g 的既有决定原文(`app.js:1321-1322`)「不对 keyup 做按键白名单——『折叠/空白选区即关闭菜单』
已让非选择类按键成为安全 no-op」**继续对 `handleSelectionTrigger` 生效**。

**为什么这个设计成立(机制事实,写进计划):** Shift 的 keyup **只在焦点位于 `#round-doc` 子树内时**
才在扩选语境下发生 —— 那恰好是「扩选结束」的时刻。

**已登记的代价:** ①「松开 Shift 即提交」是**自造惯例**(非平台约定);②它引入了一个按键白名单事实;
③鼠标路径的副作用(§K-1.5)。

### K-2.3 焦点交接三条腿(全部落 F1)

| 腿 | 触发 | 机制 | 落点 | 依据 |
|---|---|---|---|---|
| 1 | 松开 Shift | 新增监听器 | `annotateBtn.focus()` | D-05 |
| 2 | 菜单项执行后(`#btn-annotate` / `#btn-plain-ask` 被激活) | `hideSelectionMenu()` 的 F1-a | `roundDoc.focus()` | D-07 |
| 3 | Escape 关菜单 | 同上 | `roundDoc.focus()` | D-08 |

**腿 2 的理由(ROADMAP 未提):** 两个菜单项都会先 `hideSelectionMenu()`,而焦点当时停在一个
**已隐藏的按钮**上 ⇒ 回落到 `<body>`,键盘用户丢失位置(需重新 Tab 穿过整个侧栏)。

### K-2.4 `hideSelectionMenu()` 是统一挂点(D-08,逐字)

`hideSelectionMenu()`(`app.js:1296-1299`)今天有四个调用点(`document` 的 `mousedown` 关闭器、
`window` 的 `scroll` 捕获关闭器、`handleSelectionTrigger` 的两条守卫、菜单项点击)。
**「若焦点在菜单内则交还 `#round-doc`」写在这一个函数里** —— 单点、自解释,不散落到四个调用点
(散落必然漏)。目标形态:

```js
function hideSelectionMenu() {
  // D-07 / D-08(F1-a):焦点此刻若停在菜单内,隐藏后它会回落到 <body>,
  // 键盘用户要重新 Tab 穿过整个侧栏才能回到文档区 —— 交还 #round-doc。
  // **必须在 classList.add('hidden') 之前取判据**:焦点元素一旦变成 display:none,
  // document.activeElement 立刻回落到 body,之后再判就永远为假。
  const hadFocus = selectionMenu.contains(document.activeElement);
  selectionMenu.classList.add('hidden');
  menuSelection = null;
  if (hadFocus) roundDoc.focus(); // round-doc 不可聚焦时(非 phase3 / 被祖先藏住)静默降级
}
```

**两条硬约束:**
① **不得把 `window.getSelection()` 一并清空** —— 那会毁掉「Escape 后接着 Shift+→ 继续扩选」这条路径(D-08);
② **判据必须在隐藏之前取**(上面的注释就是这条的实现理由)。

### K-2.5 两条待实测项(不得写成「预期成立」,D-10)

`hideSelectionMenu()` 只清 `menuSelection` 快照,**不清 `window.getSelection()`**;
Chrome 里焦点移到按钮通常不清除文档选区(高亮可能变灰)。**两个后果必须实测并逐条记录:**

| # | 待测 | 若为「否」的后果 |
|---|---|---|
| ① | 焦点入菜单后,**用户能否看见自己选了什么**(高亮是否仍可见) | 键盘用户是「盲批注」⇒ **直接伤 A11Y-03 的 SC1** ⇒ 必须当场上报,不得静默登记 |
| ② | Escape 交还焦点后,**能否接着 Shift+→ 继续扩选**(选区锚点是否保留) | 若锚点已重置 ⇒ 用户须重新划选 ⇒ **登记为已知局限**(不新增机制) |

### K-2.6 A11Y-03 的具名人工验收脚本(D-22 第 4 条重写后的形态)

**REG-03 第 4 条的原文预期是「菜单出现」,而 D-05 之后键盘路径多了一个「松开 Shift」的动作
⇒ 原先通过的检查现在测的是另一件事**(与 Pitfall 3 / Pitfall 6 的「人工检查被继承而非重跑」同类)。
重写后的步骤(逐项记录观察结果,**含每一步的焦点位置**):

1. 进入 p3 样本(或任何 phase3 项目)。
2. 按 Tab 到轮次文档区(焦点环画出) —— 记下它在 Tab 序里的位置(§K-1.7)。
3. 按住 Shift,连按 → 数次,扩选一段文字 —— **观察:焦点环全程仍画在文档区、不跳走**(这是 K-2.1 的判据)。
4. **松开 Shift** —— 菜单出现在选区右下,焦点落在 `#btn-annotate` —— **观察:扩选高亮是否仍可见**(§K-2.5 ①)。
5. 按 Tab → 焦点移到 `#btn-plain-ask`;按 Shift+Tab → 回到 `#btn-annotate`。
6. 按 Escape → 菜单消失,焦点回到 `#round-doc`(环重新画在文档区)。
7. 再次按住 Shift + → —— **观察:能否继续扩选**(§K-2.5 ②)。
8. **真实完成一次批注:** 重做 3–4 → 按 Enter 激活 `#btn-annotate` → 原生 `window.prompt` 收 note
   (prompt 本身键盘可用)→ 输入 → 确定 → 批注条目出现在主区批注流、`#pending-count` 增加。
9. 同上走一遍 `#btn-plain-ask`(固定 question 直接 POST plain)。

**`window.prompt` 的定位:** 它是本路径上的**已知非设计物**(v2 `FLOW-V2-01` 才替换),
本阶段**不动**;但它是键盘可用的,故第 8 步成立。**不得因它「丑」而顺手替换。**

---

## 弹窗契约 M-1 —— 对象集与语义(A11Y-05 / A11Y-06)

### M-1.1 对象集 = `#confirmation-modal` + `#tier-modal`(D-11,用户已签核)

**偏离 ROADMAP 点名的名单**(路线图点名的是 `#confirmation-modal` + `#permission-modal`)。
判据是「键盘用户今天真的会卡住」:

| 弹窗 | 打开时是否移焦 | 有取消按钮? | 判定 |
|---|---|---|---|
| `#confirmation-modal` | **✓ `app.js:488`** | ✓ 拒绝 | 键盘用户**已经**能 Tab 到「拒绝」——不卡 |
| `#permission-modal` | ✗ | ✓ 拒绝 | 弹了键盘用户**不知道**(不移焦);但可 Tab 出去 ⇒ 不卡 |
| `#tier-modal` | ✗ | **✗ 没有** | **真正的卡死**:必须二选一,且焦点不在里面 |
| `#mission-complete-modal` | ✗ | 单关闭按钮 | 可 Tab 到达 |
| `#cli-check-overlay` | ✗ | 单按钮 | 可 Tab 到达 |

**与项目反复出现的同一形态同构**:Phase 6 A11Y-07「唯一确定不达标的是没被点名的那个」、
Phase 7 D-02「路线图点名的缺陷对象是错的」。**裁定记录:用户 2026-09-23 在本讨论中裁定取
「按实测:confirmation + tier」。** ⇒ 范围锁死为这两个,其余三个弹窗的 `role` / `aria-modal`
**不在本阶段**(v2 `A11Y-V2-02`)。

### M-1.2 语义三件套(落点与值,逐字)

| 属性 | 值 | 落点 | 依据 |
|---|---|---|---|
| `role="dialog"` | 字面 | **`.overlay`**(不是 `.overlay-card`) | 本文件裁定 |
| `aria-modal="true"` | 字面 | 同上 | D-14 |
| `aria-labelledby` | `confirmation-modal-title` / `tier-modal-title` | 同上 | D-15 |

**`role` 落在 `.overlay` 而非 `.overlay-card` 的裁定理由:**
① **被切换的节点与被告白的节点是同一个** —— `.overlay` 就是 `classList.toggle('hidden')` 的作用对象,
「宣告与实现一致」(SC3)因此是**结构性可查**的,而不是两处需要同步的记账;
② `.overlay-card` **没有 id**、五个弹窗共用同一个类名 ⇒ 把 ARIA 挂在一个类共享的内层 `<div>` 上,
会让「声明」与「状态」分居两个节点,必然漂移;
③ `aria-labelledby` 无论挂在哪一层,都解析到卡片内的同一个 `<h3>`。

**为什么不选 `aria-label` 写字面串(D-15):** 文案会变成第二处真相来源 —— 与「名必须说实话」的纪律相冲。

### M-1.3 `inert`:让宣告成真(D-14)

`aria-modal="true"` 的语义是「弹窗之外的背景对辅助技术是惰性的」,而**焦点陷阱是已裁定 Out of Scope**
⇒ 只加两个属性就是**宣告一个实现并不兑现的契约**,与 ROADMAP 自己警告 `role="dialog"` 时点名的
形态完全一致。原生 `inert` 属性是零依赖、零构建的解法(满足硬规则 6),且顺带拿到焦点陷阱的**主要**
效果(背景不可聚焦、不可点)。**用户裁定原话:「加 inert,让宣告成真」。**

**边界(已核实,`index.html`):** `#app` 在 **L10 起、L155 闭合**;五个 `.overlay`
(L158 / L170 / L184 / L196 / L213)与 `#selection-menu`(L207)都是它的**兄弟** ⇒ `inert` 挂 `#app`
天然只作用于背景、不会波及弹窗自身。
**`#selection-menu` 也在 `#app` 之外 ⇒ 弹窗打开时它不会被 inert。**
**两者同时可见的场景不存在,判据是结构性的:** 菜单只在 `currentState === 'phase3'` 时显示
(`app.js:1327` 的第一条实质守卫),而 `#tier-modal` 只在 `phase5_awaiting_tier` 弹出 —— 状态互斥。
**规划期须确认这一点并登记**(不得只写「理论上互斥」)。

### M-1.4 实现形态:单点派生,不成对记账

```js
// D-14:让 aria-modal="true" 的宣告成真 —— 背景对辅助技术与指针都惰性。
// 原生 HTML 属性,零依赖零构建(硬规则 6);焦点陷阱是 Out of Scope,inert 不是陷阱。
// 从两个弹窗的 .hidden 现状**派生**,不靠 open/close 成对记账:
// 成对记账会在任何一条早退路径上漏去属性(与 STATE.md 反复出现的派生计数缺陷同型),
// 派生式在结构上不可能失配,且天然幂等。
function syncBackgroundInert() {
  const anyDialogOpen = !confirmationModal.classList.contains('hidden')
    || !tierModal.classList.contains('hidden');
  if (anyDialogOpen) appEl.setAttribute('inert', '');
  else appEl.removeAttribute('inert');
}
```

**5 个调用点(全部在既有函数体内,不新增函数):** `openConfirmModal()`(L483,`remove('hidden')` 之后)、
`closeConfirmModal()`(L491,`add('hidden')` 之后)、`#tier-modal` 的打开分支(`app.js:640` 之后)、
`chooseTier()` 成功路径(`app.js:799` 之后)、Escape 分派的 tier 分支。
**`appEl` 是新增的顶层句柄**(`const appEl = document.getElementById('app');`,加在 `app.js:83` 之后)——
**新增是安全的,改名或删除既有句柄才是 G-idi01-8 的失效形态**(硬规则 5)。

### M-1.5 打开时移焦(D-16)

| 弹窗 | 现状 | 本阶段 |
|---|---|---|
| `#confirmation-modal` | **已有** —— `app.js:488` `confirmWordInput.focus()`(全文件唯一的 `.focus()` 调用) | 保持;只把 `syncBackgroundInert()` 插在它**之前** |
| `#tier-modal` | **缺** | **补**:焦点送入 `#btn-tier-loose`(首个可操作控件) |

**为什么必须补(D-11 判定的「卡死」的实质修复):** `#tier-modal` 的陷阱不是「没有 Escape」而是
「焦点不在里面」;`inert`(D-14)落地后背景不可聚焦,**焦点若不在弹窗内会掉到 `<body>`** ⇒
下一次 Tab 会绕开整个背景、落到弹窗外围,比不 inert 更糟。
**选择首个可操作控件(而非弹窗容器)的理由:** 与 `openConfirmModal()` 的既有形态对称
(`confirmWordInput.focus()` 就是「首个可操作控件」),且**不引入任何新属性**
(容器作焦点目标需要给它 `tabindex="-1"`,那会被 item 10 的普查排除,又是一个需要解释的例外)。
**顺序锁定:** `classList.remove('hidden')` → `syncBackgroundInert()` → `.focus()`。
**规划期须实测 `inert` 生效瞬间焦点落在哪里**,并据此确认是否需要显式 `.focus()`
(这是 D-16 明文要求的实测项)。

---

## 弹窗契约 M-2 —— Escape 分派(A11Y-05)

### M-2.1 单点分派器(裁定:一个 `document` 监听器 + 显式优先级表)

**新增一段,紧接 `initSelectionMenu()` 的定义之后**(`app.js:1344` 起的菜单绑定块之后)。
**绑定在顶层**(不在任何 handler 内)⇒ 一次性、与菜单的初始化路径解耦。

**为什么取「单点 + 优先级表」而不是「各弹窗各自的监听器」(Claude's Discretion,裁定并写明理由):**
① 三个响应对象里有一个是菜单(它已经在 `initSelectionMenu` 那一段),分派器与它相邻使
**「Escape 的完整语义在一个屏幕内可读完」**;② 分散到各弹窗会把「谁先响应」变成**源码顺序事实**
(硬规则 3 的同型风险);③ 单点可解释、可枚举(本项目「影响面必须可枚举」的既定口径)。

```js
// Escape 单点分派(A11Y-05 / D-08 / D-12 / D-13)。
// 优先级按 z 序:--z-selection-menu(200)> --z-overlay(100)。
// 三个响应对象今天互斥(菜单只在 phase3、#tier-modal 只在 phase5_awaiting_tier),
// 但优先级表使行为与「谁先打开」无关 —— 源码顺序不参与判定。
document.addEventListener('keydown', (e) => {
  if (e.key !== 'Escape') return;
  if (!selectionMenu.classList.contains('hidden')) {          // 1. 划词菜单
    hideSelectionMenu();                                      //    含 F1-a 焦点交还
    e.preventDefault();
    return;
  }
  if (!confirmationModal.classList.contains('hidden')) {      // 2. G3 授权确认
    closeConfirmModal();                                      //    D-12:仅关闭,零决定
    authorizeBtn.focus();                                     //    F1-d:交还触发者
    e.preventDefault();                                       //    (inert 的去除已在
    return;                                                   //     closeConfirmModal 内完成)
  }
  if (!tierModal.classList.contains('hidden')) {              // 3. 自检档位
    tierModal.classList.add('hidden');
    tierModalShown = false;                                   //    D-13:允许重弹
    syncBackgroundInert();
    continueCheckBtn.focus();                                 //    F1-d:交还下一个动作
    e.preventDefault();
  }
  // 4. 其余三个弹窗(#permission-modal / #mission-complete-modal / #cli-check-overlay)
  //    **刻意不响应 Escape** —— 范围锁死为 D-11 的两个对象。这是刻意的,不是漏项。
});
```

### M-2.2 逐分支的行为契约

| 分支 | Escape 的行为 | 明确**不**做的事 |
|---|---|---|
| `#selection-menu` | 关闭菜单 + 交还 `#round-doc`(F1-c) | **不清 `window.getSelection()`**(会毁掉「Escape 后接着 Shift+→ 继续扩选」) |
| `#confirmation-modal` | **仅关闭**(`closeConfirmModal()`),**不产生任何决定** | **不代替「拒绝」** —— 那会走 `rejectAuthorization()`,把用户**直接推进一个原生 `window.prompt`**;而替换 `window.prompt` 是 v2 `FLOW-V2-01`。**也不新增一条「拒绝但不弹 prompt」的写批注路径** —— 那要引入第二处真相来源 |
| `#tier-modal` | 关闭 + **复位 `tierModalShown = false`** | **不复位 `selfcheck.tier`**;不做任何 POST |
| 其余三个弹窗 | 无响应(范围锁) | 不因「顺手」而扩张 A11Y-05/06 的对象集 |

**`#confirmation-modal` 选「Escape = 仅关闭」的理由:** 最小、零副作用;键盘用户本来就能 Tab 到
「拒绝」(`openConfirmModal()` 已 `confirmWordInput.focus()`,Tab 跳过 disabled 的「放行」直达「拒绝」),
所以 Escape 不需要代替拒绝。

### M-2.3 `#tier-modal` 的死状态与复位(D-13,已核实的现场)

**已核实的死状态风险:** 该弹窗在 `sessionData.state === 'phase5_awaiting_tier'` 且未选档时弹出,
**打开时立刻把 `tierModalShown = true`**(`app.js:639`);只有选档成功才 `classList.add('hidden')`
(`app.js:799`)。**若被关掉而没选,`selfcheck.tier` 仍为空而 `tierModalShown` 已是 true ⇒
它不会再弹** —— 用户落进「档位未定且入口消失」。
**复位该标志使下一个自检事件(`refreshChecksAfterStream`)能重新弹出。**
**已登记的代价:** 复位后弹窗可能在用户做别的事时重现 —— 但这正是「档位未定就该继续问」的正确行为。
**保留 A11Y-05 与 SC3 的「可 Esc 关闭」字面。**

### M-2.4 已知缺口(登记,不修)

**`#permission-modal` 的「弹了键盘用户不知道」(打开时不移焦,无任何宣告)** ——
归 v2 `A11Y-V2-02`,本阶段**不修**(D-17)。理由:用户已裁定取 `confirmation + tier` 两个对象,
而该弹窗可 Tab 出去、不构成卡死。**登记位置:** `08-UAT.md` 或 VERIFICATION 的 manual/advisory 节。
**不得在本阶段顺手修** —— 用户已裁定对象集。

**`aria-live` 在本阶段一律不加(M7 防线,登记以防蔓延):** `appendSayToChat` 每个 SSE 事件追加一个
DOM 节点 ⇒ **`aria-live` 绝不可加在 chunk 容器上**。`#stream-banner` 的 `aria-live="assertive"`
与气泡层的 `aria-busy` / `role="log"` 分别是 v2 `A11Y-V2-04` / `A11Y-V2-03`。

---

## 焦点与状态契约(本阶段零 CSS 新增)

**本阶段不新增、不修改任何 `:focus` / `:focus-visible` / `:hover` / `:active` / `:disabled` /
`transition` 规则。** 下表是**本阶段结束时**各交互面的状态来源(全部继承 Phase 7):

| 交互面 | 状态来源 | 本阶段 |
|---|---|---|
| 21 个按钮 / 8 个输入框 / 4 个下拉 | `style.css:1508-1517` 的七选择器枚举 | **零改动** |
| **`#round-doc`(新)** | **同一条枚举里的 `[tabindex]:focus-visible`** | **零 CSS:靠 `tabindex="0"` 自动命中** |
| `#selection-menu` 的两个按钮 | 同一枚举的 `button:focus-visible` | 零改动(焦点入菜单后环照常出) |
| `:hover` / `:active` / `:disabled` | Phase 7 的既有规则 | 零改动 |
| 过渡与减弱动效 | Phase 7 的过渡挂载规则 + `@media (prefers-reduced-motion: reduce)` | 零改动;**环必须瞬变**(outline 不在过渡允许列表内) |
| `inert` 的背景 | **原生属性,不是样式** | 新增(JS 挂载);**与 `.hidden` 正交,不得互相替代** |

**软化的禁令重申:** `:disabled` 是 G3 前提条件唯一的视觉信号,**不得软化**(Pitfall M5)。
`#btn-authorize` 的禁用态本阶段零改动。

---

## Spacing Scale —— 本阶段零消费、零改动

**`04-UI-SPEC.md` 的 12 档刻度(S-1,已签核)本阶段一字不动,且本阶段不消费任何一档。**
理由:本阶段的全部改动是属性(HTML)与行为(JS),没有一条声明式间距。
**`#doc-panel-body { padding: var(--space-8) var(--space-10) }`(`style.css:657`)是本阶段的
几何前提(D-01 的 40px 水平 padding 决定环不被裁切)—— 但它不得被改动**,改它等于把环的几何论证作废。
**本阶段不新增任何间距字面量,也不新增例外行。**

---

## Typography —— 本阶段零改动

**`idi-05-UI-SPEC.md` 的排版契约全部继续有效:7 档字号(12 / 14 / 16 / 18 / 22 / 24 / 28)、
3 档字重(400 / 500 / 600)、4 档行高。本阶段一个字号、一个字重、一行行高都不动。**

| Role | Size | Weight | Line Height |
|------|------|--------|-------------|
| 轮次文档正文(焦点环的承载面) | `--text-md` 16px | `--fw-regular` 400 | `--lh-reading` 1.625 |
| 弹窗 `<h3>`(无障碍名称的来源) | `--text-xl` 24px | 继承 | 继承 |
| 菜单按钮文案 | `--text-base` 14px | 继承 | 继承 |

**两条硬约束:** ①不得新增/修改任何 `font-size` / `font-weight` / `line-height` 声明;
②**不得触碰 `.collapse-indicator`**(backlog `999.1` 第 1 项;硬规则 5 / 05-CONTEXT D-23;
`app.js:1550` 用 `textContent` 赋值,不得引入内联 `<svg>`)。

---

## Color —— 本阶段零改动

**`idi-04.1-UI-SPEC.md` 的 25 个 tier-1 / 47 个 tier-2 / 47 对清单全部继续有效。
本阶段零颜色改动、零新增令牌、围栏 `:root` 零改动。**

| Role | Value | Usage |
|------|-------|-------|
| Dominant (60%) | `--color-surface-page` / `--color-surface` | 页面与面板底、卡片、控件、**焦点环的背景** |
| Secondary (30%) | `--color-surface-sunken` + `--color-border*` | 面板 chrome、分隔线 |
| Accent (10%) | `--color-action-primary` / `--color-action-warning` | 见下方「Accent reserved for」 |
| Destructive | `--color-action-danger` | 仅破坏性动作 |

**Accent reserved for:** 主要动作按钮(发送 / 进入 / 同意 / 放行)、`#btn-divergence`、`#state-badge`、
`mark` 高亮、活动面板标记(Phase 5)。**绝不含「所有交互元素」。** 绿色三档是**动作族**而非 accent。

**本阶段唯一涉色的事实(且不是颜色改动):** 焦点环用 `--color-focus`(`#1f63bd`),它**已声明、已被消费**
(`style.css:259` / `:1515`)⇒ 不违反硬规则 5。**它的三对 PAIR 与本阶段的关系:**

| PAIR | 门 | 本阶段 |
|---|---|---|
| `--color-focus ON --color-surface NON-TEXT` | `check-02` | 逐字不变 |
| `--color-focus ON --color-surface-page NON-TEXT` | `check-02` | 逐字不变 |
| `--color-focus ON --color-surface NON-TEXT@0.75` | `check-02`(常驻算术) + `probe-07`(一次性) | **由 D-04 的探针复跑重新承担** —— 因为 `#round-doc` 入册后 `.archive-mode` 下的运行时环断言**第一次有了服务对象** |

**两条不得触碰的对比度不变量:** ①`#stream-banner` 的 `.fatal` 修饰符必须保留为**独立选择器**;
②`#round-doc.round-frozen` 的 `filter: saturate(0.6)` + 琥珀 `box-shadow: inset` 不得改动
(S-4 已签核,删除 `opacity` 正是为了让环回到 5.62:1)。

---

## Copywriting Contract —— 本阶段仅改一处文案(S8-1)

**本阶段唯一改动的用户可见字符串是 `app.js:1121` 的一个词(`在左侧文档` → `在右侧文档`,见
§Sign-Off Items S8-1,已 RESOLVED)。** 除此之外不新增元素、不改按钮、不改提示、不改空态与错误态。
下表**冻结既有文案**(唯一例外是 S8-1 那一行),使后续阶段有参照且不能静默漂移
(与 `04/05/06-UI-SPEC.md` 一致)。

| Element | Copy(frozen —— 逐字来自 `index.html` / `app.js`) |
|---|---|
| 划词菜单项 1 | `批注`(`index.html:208`) |
| 划词菜单项 2 | `用大白话讲这段`(`index.html:209`) |
| 弹窗标题(`#confirmation-modal`,**也是它的无障碍名称**) | `授权确认`(`index.html:172`) |
| 弹窗标题(`#tier-modal`,**也是它的无障碍名称**) | `选择自检档位`(`index.html:186`) |
| 档位按钮 | `宽松` / `严格`(各带 `.tier-desc` 说明) |
| G3 闸门确认 | `放行` / `拒绝` |
| 不可逆动作(G3 —— 核心价值红线) | `授权撰写总设计文档` |
| 空态(批注流) | **本阶段修改(S8-1,用户 2026-09-23 裁定)**:`本轮暂无批注——在左侧文档划词即可批注。` → **`本轮暂无批注——在右侧文档划词即可批注。`**(`app.js:1121`;原串与 `DESIGN.md` §4.1 矛盾,改后一致) |
| 空态(批注流,历史轮) | `该轮暂无批注。`(`app.js:1123`) |
| 错误态(内联) | `showInlineError(anchor, message)` —— 服务端消息,**`textContent`-only** |
| 错误态(G3 确认) | `#confirm-error` —— 必须渲染为**红色**而非灰色(Pitfall M6) |
| 断流横幅 | `事件流已断开,正在自动重连……` |

**文案规则(后续阶段适用,记录在此以防被重新发明):**
- 面向用户的输出遵守 DESIGN.md §3.8 语言红线 —— 简洁精准、大白话定义术语;讨论文档以中文为主。
- **错误文本绝不经 `innerHTML` 渲染**(T-260916-01)。
- **无障碍名称不新写字符串**:两个弹窗的名称通过 `aria-labelledby` **指向既有的 `<h3>`**,
  使「屏幕上的标题」与「辅助技术读到的名称」是同一处真相(D-15)。
- **本阶段不新增任何可发现性提示文案**(D-19)—— 键盘划词路径今天唯一的视觉信号是焦点环,
  这是一个**已登记的已知局限**,不是待补的文案缺口。

---

## Deliberate Delta Ledger(本阶段)

**每一项都是刻意的视觉/行为变更。没有列的就不是变更。**

| # | 变更 | 视觉/行为 delta | 依据 | 门 |
|---|---|---|---|---|
| D8-1 | `#round-doc` 加 `tabindex="0"` | **Tab 序新增一个停靠点**(位置见 §K-1.7);**整盒焦点环首次真实出现**(此前是 `[tabindex]` 枚举规则的零服务对象) | A11Y-02 / D-01 | `check-05 --item 10`(三样本) |
| D8-2 | `#round-doc` 现在**可被鼠标点击聚焦** | 鼠标 Shift+点击扩选后**松开 Shift 也会把焦点送进菜单**。不出环(鼠标点击不匹配 `:focus-visible`)⇒ SC2 语义仍成立 | D-09 | REG-03 第 4 条复跑 |
| D8-3 | 键盘划词**多了一个动作**:松开 Shift 才提交 | 自造惯例(非平台约定)。**不松手就不提交** | D-05 | A11Y-03 人工脚本(§K-2.6) |
| D8-4 | 菜单项执行后焦点**交还 `#round-doc`** | 此前焦点停在已隐藏的按钮上 ⇒ 回落到 `<body>` | D-07 | §K-2.6 第 8/9 步 |
| D8-5 | Escape 关菜单并把焦点交还 `#round-doc` | 新增键位响应 | D-08 | §K-2.6 第 6 步 |
| D8-6 | 两个弹窗获得 `role="dialog"` + `aria-modal="true"` + `aria-labelledby`;**背景 `#app` 被 `inert`** | **背景不可聚焦、不可点**(指针层面也可感)。**行为变更,不是纯语义** | A11Y-06 / D-14 / D-15 | 人工:弹窗打开时 Tab 不进入背景 |
| D8-7 | `#tier-modal` **打开时移焦** + Escape 关闭 + `tierModalShown` 复位 | 弹窗可在用户做别的事时**重现**(这是「档位未定就该继续问」的正确行为);焦点进入弹窗(此前不在) | D-13 / D-16 | 人工:A11Y-05 的 tier 分支 |
| D8-8 | `#confirmation-modal` 的 Escape = **仅关闭,零决定** | 新增键位响应;不代替「拒绝」 | D-12 | 人工 |
| D8-9 | **(条件)** D-02 触发时 `style.css` 的环承载面变更 | 仅在实测判定整盒环不可辨时存在;会**作废 5 份 live 指纹**并连带复验 | D-02 / D-25 | 实测 + 指纹重算 |
| D8-10 | **两个弹窗关闭后把焦点交还触发者**(confirmation → `#btn-authorize`;tier → `#btn-continue-check`) | 此前弹窗关闭后焦点回落到 `<body>`;交还后键盘用户停在**同一个逻辑位置**上(可继续授权流程 / 继续自检流程)。**成功路径不交还**(见 §焦点契约的 F1 不覆盖情形①) | **A-8(用户 2026-09-23 裁定采纳)** | 人工:关弹窗后按 Tab,焦点从触发者处继续 |
| D8-11 | **`app.js:1121` 的空态文案改一个词**:`在左侧文档` → `在右侧文档` | **用户可见文案变更**(本阶段唯一一处);改后与 `DESIGN.md` §4.1(v1.14 文档面板在右)一致 | **S8-1(用户 2026-09-23 裁定)** | 人工:阶段 3 空批注流下读该串 |

**本阶段明确不产生的 delta:** 零 `style.css` 改动(D-01 路径)、零新增令牌、零颜色/字号/字重/行高改动、
零新增依赖、零新增文件、**零新增用户可见字符串**(D8-11 是**改写一个既有词**,不是新增文案)、
`scripts/check-05-ui-uat.py` 零改动、`frontend/vendor/` 仍恰好一个文件。

---

## 契约修正登记(全部由已锁定决策产生,不是新问题)

| # | 修正 | 依据 | 影响 |
|---|---|---|---|
| **A-1** | **ROADMAP Phase 8 的「两个阻塞式弹窗(G3 确认、授权)」→ `#confirmation-modal` + `#tier-modal`** | D-11(用户 2026-09-23 裁定) | A11Y-05 / A11Y-06 的对象集按实测重排;`#permission-modal` 归 v2 `A11Y-V2-02`。**不改 `ROADMAP.md` / `REQUIREMENTS.md`**(改会作废指纹),只在计划与验证记录里登记 |
| **A-2** | **ROADMAP 的「`handleSelectionTrigger` 的键盘分支把焦点移入菜单首按钮」→ 独立 Shift 监听器 + 抬起 Shift 提交** | D-05 / D-06 | **按字面实现会假绿**(§K-2.1)。规划期必须把这条写进计划,否则会被当成「已按路线图实现」 |
| **A-3** | **PITFALLS 5 失效模式 4「环套在 `#round-doc` 上只有上下边缘可见」被几何推翻;ROADMAP 的落点 `#doc-pane` 在 HEAD 上不存在** | D-01(实测) | 整盒环 + `style.css` 零改动;`#doc-pane` 的真实落点是 `#doc-panel-body`(04.1 D-13 已改名)。**这条推翻直接换来「Phase 8 零指纹债务」** |
| **A-4** | **两条 REG-02 门落为计划级 `<verify>` grep + 人工 UAT 条目,不写进 `scripts/check-05-ui-uat.py`** | D-21(用户裁定) | `check-05-ui-uat.py` 在 5 份 live 报告的 `covered_files` 里 ⇒ 把断言写进去会让零指纹债务当场消失。**已登记的代价:这两条不是常驻守卫,下次改 `style.css` 的人不会自动被拦** |
| **A-5** | **REG-02 门②的基线由「6」更正为实测 9** | 本文件实测(§基线与契约漂移口径 漂移项 3) | 门的写法是 `>= 9`;**照抄 6 会造出一条永远不会失败的假门** |
| **A-6** | **pytest 口径 = 「219 passed + 6 skipped / 225 collected」** | D-24 | ROADMAP Phase 8 Gates 的「219」正确;**Phase 4 段里的「225」是 collected 数** —— 照抄会造假门。必须用项目 venv(`.venv/bin/python -m pytest`),环境 `python3` 是 miniconda 会让 4 个 `ai_caller` 测试假失败 |
| **A-7** | **SC2 / SC3 的措辞按 D-11 / D-14 读** | D-11 / D-14 | SC2「Esc 能关闭 G3 确认与授权两个弹窗」→ 对象是 confirmation + tier;SC3「该宣告与实现一致」→ 靠 `inert` 兑现,不是靠焦点陷阱 |
| **A-8** | **F1-d(弹窗关闭后交还触发者)—— 契约项,已由用户采纳** | **源:D-07 / D-08 的同一条理由**(镜像);**采纳本身是用户 2026-09-23 的裁定,不是本文件的推断** | **已采纳的契约项,两个弹窗都适用:**`#confirmation-modal` 关闭后 → `#btn-authorize`;`#tier-modal` 关闭后 → `#btn-continue-check`。用户接受的理由:D-07/D-08 已确立「焦点绝不停在已隐藏元素上,也绝不回落到 `<body>`」,而**弹窗关闭是同一形态**。两个返回目标已由 checker 独立核实存在:`#btn-authorize` 在 `index.html:143`、`#btn-continue-check` 在 `index.html:49` |
| **A-9** | **`frontend/style.css:1499-1501` 围栏注释的「Phase 8 加 tabindex 时连同它自己的内嵌处理一起落地」不再成立** | D-01 / D-02 | 本阶段**不做内嵌**(整盒环已可辨);注释**留证不改**(零 CSS 改动)。**下游不得把该注释读成本阶段的契约** |

---

## Sign-Off Items(须用户裁定,不是 checker 裁定)

**本阶段共四项,全部已于 2026-09-23 由用户裁定完毕 —— 无未决项。**
D-01 / D-11 / D-14 三项关键偏离在讨论中裁定(原话见 `08-CONTEXT.md`);
**S8-1 与 A-8 在规划期由用户裁定**(原话见下表的「用户裁定」列)。
**四项均不得重开、不得重新讨论。**

| # | 裁定项 | 本文件的建议 | 用户裁定(2026-09-23) | 落地位置 |
|---|---|---|---|---|
| **S8-1** | **`app.js:1121` 的空态文案「本轮暂无批注——在左侧文档划词即可批注。」是否在本阶段改为「右侧」** | **改(一个字)**:`左侧` → `右侧`。理由:①它与**唯一权威设计文档** `DESIGN.md` §4.1 矛盾(v1.14 明写「主区(左)…文档面板(右)」),而本项目对面向用户的输出立有「名必须说实话」与 §3.8 语言红线;②`06-UI-SPEC.md` 的 checker 已把该串登记为**已知过期串并明确指派给「拥有 `app.js` 的阶段(Phase 8)」**;③它是**一个词**,在**本阶段已经在改的文件**里,零新字符串、零新元素、零新依赖;④不修则它在**本阶段正要打通的那条键盘路径上误导用户** | ✅ **裁定「改」** —— `本轮暂无批注——在左侧文档划词即可批注。` → **`本轮暂无批注——在右侧文档划词即可批注。`**(`app.js:1121`,仅此一个词) | §Copywriting Contract 对应行(已由「冻结」改为「本阶段修改」)+ §Deliberate Delta Ledger **D8-11** + §Files Modified 表 |
| **A-8** | **F1-d(弹窗关闭后交还触发者)是否采纳为契约项** | 采纳 —— 源:D-07 / D-08 的同一条理由(镜像) | ✅ **裁定「两个都交还焦点」** —— `#confirmation-modal` 关闭后 → `#btn-authorize`;`#tier-modal` 关闭后 → `#btn-continue-check`。用户接受的理由:D-07/D-08 已确立「焦点绝不停在已隐藏元素上,也绝不回落到 `<body>`」,而**弹窗关闭是同一形态** | §焦点契约 **F1-d** + §Deliberate Delta Ledger **D8-10** + §Files Modified 表 |

**已登记的两条落地约束:**
1. **S8-1 使 `frontend/app.js` 的 diff 多一行** —— 该文件本就在本阶段的改动面内(§Files Modified),不引入新文件、不引入新字符串以外的任何东西。
2. **A-8 的两个返回目标已由 checker 独立核实存在**:`#btn-authorize` 在 `index.html:143`、`#btn-continue-check` 在 `index.html:49`。**成功路径不交还焦点**(见 §焦点契约的 F1 不覆盖情形①)。

---

## 契约校验命令

**执行前基线(规划期必须先跑一遍,再逐条登记打破项):**

```bash
cd frontend && node --check app.js                     # 期望 OK
.venv/bin/python -m pytest -q -m "not slow"            # 期望 219 passed + 6 skipped / 225 collected
bash scripts/check-01-token-conformance.sh             # PASS(围栏外裸 hex = 0)
python3 scripts/check-02-contrast.py                   # PASS: 0 failures(47 对 + ORDER 0.363)
bash scripts/check-03-hidden-uniqueness.sh             # PASS(^\.hidden { 计数 == 1)
bash scripts/check-04-important-count.sh               # PASS(!important 声明数 == 1)
```

**本阶段自己的门:**

```bash
python3 scripts/check-05-ui-uat.py --item 10    # 焦点环元素普查:#round-doc 入册(p3 / checking / archive)
python3 scripts/check-05-ui-uat.py --item 1     # 五态显隐(.hidden 的层叠证据 —— 本阶段不碰它,但必须仍绿)
python3 scripts/check-05-ui-uat.py --item 4     # SC5 的两条令牌接线 + #state-badge z-index
.venv/bin/python scripts/probe-07-focus-composite.py   # D-04 的探针复跑(不是门,不进守卫契约)
```

**本阶段的静态计数门(注意每条都按「声明/出现次数」写,不按命中行数):**

```bash
grep -c tabindex frontend/index.html                   # 0 → 1(且 app.js 仍为 0)
grep -c ':focus-visible' frontend/style.css            # 9 → 9(零 CSS 改动)
grep -c 'role=' frontend/index.html                    # 0 → 2
grep -o 'aria-modal' frontend/index.html | wc -l       # 0 → 2
grep -o 'aria-labelledby' frontend/index.html | wc -l  # 0 → 2
grep -c inert frontend/app.js                          # 0 → >0(index.html 保持 0:属性由 JS 挂)
grep -c '^\.hidden {' frontend/style.css               # == 1(硬规则 1)
bash scripts/check-04-important-count.sh               # !important 声明数 == 1(硬规则 2)
```

**两条 REG-02 门(计划级 `<verify>` + 人工 UAT 条目,不写进 harness —— D-21 / A-4 / A-5):**

```bash
grep -c 'inline-error' frontend/style.css              # == 1(基线实测 1)
grep -c 'clearInlineError();' frontend/app.js          # >= 9(基线实测 9,只增不减)
```

**必须保留的既有门(本阶段会打破它们的表面形态,但不得打破断言本身):**
`check-01…04` 四条;`check-05 --item 1 / 4`;`check-02` 的 47 对逐字不变。
**`check-05 --item 10` 的判定集在三个样本里 +1 是预期的**(D-03),不是回归。

---

## Global Hard Rules(每个 Phase 8 计划都适用)

**继承 `ROADMAP.md` §全局硬规则 1–7(逐条复述,不改动):**

1. `grep -c '^\.hidden {' frontend/style.css` 必须等于 **1**。`.hidden { display: none !important }` 是
   **机制而非样式**:不得令牌化、不得移动、不得弱化、不得用 `:where()` 降特异性。
2. `style.css` 中含 `!important` 的**声明行**数为 **1**。算术陷阱:直接 `grep -c '!important'` 返回 **5**
   (4 行注释散文),**写门时必须按「声明」计数**。
3. **追加,不重排。** 本阶段不编辑 `style.css`(D-01)⇒ 该规则只约束「不得顺手改 CSS」。
   `app.js` 的新增代码一律**追加**在既有函数内或文件逻辑段之后,**不得移动既有语句的先后位置**。
4. 不得新增 `!important`;不得令牌化 `display`;不得引入 `@layer` / `@property` / `var(--x, #fallback)`。
5. **不得触碰:** `.fatal` 修饰符;`applyArchiveView` 的两行(`app.js:817-818`);`#selection-menu` 的
   **DOM 位置**(必须是 `<body>` 直接子元素,任何 `filter`/`transform`/`opacity` 祖先都会改变其包含块)
   与定位数学;`showInlineError` 的 **`textContent`-only** 规则(XSS 缓解 T-260916-01,**不是风格选择**);
   `renderAnnotations` / `renderVerdictCard`;`app.js:4-75` 的约 70 个顶层 `getElementById` 句柄
   (**id 不得改名或删除;新增安全**)。
6. 零新增运行时依赖、零构建步骤(D-06)。`check-01/02` 必须保持零依赖。
7. 每个 `style.css` 计划都必须带**至少一项运行时验证** —— **本阶段在 D-01 路径下没有 `style.css` 计划**;
   若走 D-02 升级,该规则立即生效(环的可辨性必须由运行时读数佐证,不能只有静态计数)。

**本阶段追加:**

8. **`app.js` / `index.html` 的每一次编辑都必须先确认「没有改名、没有删除既有 id」** ——
   删除或改名一个 id 会在解析期静默杀死其下全部处理器(G-idi01-8)。
   **新增 id / 新增顶层句柄是安全的**(本阶段新增 2 个 id + 1 个句柄)。
9. **零 `style.css` 改动**(D-01)。唯一合法的例外是 D-02 被实测触发,届时必须一并登记
   §Deliberate Delta Ledger D8-9 + 5 份指纹重算 + 复跑四条守卫。
10. **不得新增 `:focus` / `:focus-visible` 规则,不得给 `#round-doc` 写专用焦点规则** ——
    环由 Phase 7 的 `[tabindex]:focus-visible` 枚举自动命中。新增专用规则会让「规则覆盖了谁」
    与「门检查了谁」分叉(G-idi-05-1 的成因)。
11. **不得把 `aria-live` 加在任何流式容器上**(Pitfall M7);本阶段不加任何 `aria-live`。
12. **`inert` 与 `.hidden` 是两个正交机制,不得互相替代**;`inert` 只挂 `#app`,不加在弹窗或
    `#selection-menu` 上。
13. **`hideSelectionMenu()` 里「交还焦点」的判据必须在 `classList.add('hidden')` 之前取**(§K-2.4);
    **不得在其中清空 `window.getSelection()`**。

---

## Do-Not-Touch List(继承 + 本阶段追加)

**继承(逐条复述,来源:`04/05/06-UI-SPEC.md`):**
`.hidden` 唯一性与其注释 · `!important` 声明数 = 1 · `.fatal` 两态 · `#selection-menu` 的 DOM 位置与
定位数学 · `showInlineError` 的 `textContent`-only · `renderAnnotations` / `renderVerdictCard` ·
`app.js:4-75` 的约 70 个 id · `applyArchiveView` 两行 · `#round-doc.round-frozen` 的
`filter: saturate(0.6)` + 琥珀 inset · `.annotation-answered` 的 `--color-text-muted` 弱化 ·
五处 `.panel-header` 的活动标记 · `.collapse-indicator` · 嵌入目标的标题刻度规则 ·
`#round-switcher` / `#check-switcher` 的 token 接线 · `#doc-panel-body` 的 padding(本阶段的环几何前提)。

**本阶段追加:**

| 不得触碰 | 理由 |
|---|---|
| `handleSelectionTrigger`(`app.js:1323`)的**函数体** | D-06:按键白名单只存在于新增的 Shift 监听器里;给它加白名单会改变鼠标路径与 t8g 决定的实质 |
| `app.js:1321-1322` 的 t8g 注释原文 | 它是既有决定的记录;**新增监听器**偏离它,不是它被推翻 |
| `#selection-menu` 的两个菜单项 handler 的**既有语义** | 本阶段只在 `hideSelectionMenu()` 里加焦点交还,不改它们的请求/渲染行为 |
| `window.getSelection()` 的生命周期 | D-08:清空它会毁掉「Escape 后接着 Shift+→ 继续扩选」 |
| `rejectAuthorization()`(`app.js:496`)与两处 `window.prompt` | v2 `FLOW-V2-01`;**D-12 选「Escape 仅关闭」正是为了不把键盘用户推进其中一个** |
| `showPermissionModal()`(`app.js:1202`) | D-17:已知缺口归 v2 `A11Y-V2-02`,本阶段不修 |
| 其余三个弹窗的 `role` / `aria-modal` | D-11 的范围锁 |
| `#draft-content` | D-20:加 `tabindex` 是死代码(阶段 1-2 无批注功能) |
| `#rounds-hint` 的内容与显隐时机 | D-19:改它是可见行为变更,且它是「已进入轮次阶段」的占位语义 |
| `check-05-ui-uat.py` 的任何断言与常量 | D-21:改它会作废 5 份 live 指纹 |

---

## 不在本阶段(范围锁 —— Pitfall 8 / Anti-Pattern 6)

| 项 | 理由 | 状态 |
|---|---|---|
| 焦点陷阱实现(含 Shift+Tab 环绕与动态内容) | REQUIREMENTS Out of Scope 表;`inert`(D-14)只拿到它的**主要**效果,不是完整实现 | 不在本阶段(v2 `A11Y-V2-01`) |
| 完整 ARIA / 屏幕阅读器合规(其余三弹窗的 `role`、`aria-describedby` 接线等) | 用户已裁定取「窄切片」;保留 A11Y-05/06 两处,**理由是安全而非无障碍** | 不在本阶段(v2 `A11Y-V2-02`) |
| `#permission-modal` 的「弹了键盘用户不知道」 | D-17:可 Tab 出去、不构成卡死 | 不在本阶段(v2 `A11Y-V2-02`) |
| `#round-doc` 的 `role="region"` + `aria-label` | D-18:裁定不加(保持窄切片) | 不在本阶段 |
| 键盘划词的可发现性提示 | D-19:登记为**已知局限** | 不在本阶段 |
| `aria-live` 在流式聊天区 / `#stream-banner` | Pitfall M7;**绝不可加在 chunk 容器上** | 不在本阶段(v2 `A11Y-V2-03` / `A11Y-V2-04`) |
| 两处 `window.prompt` 的替换 | v2 `FLOW-V2-01` | 不在本阶段 |
| 暗色模式 / `prefers-color-scheme` | v2 `TOKEN-V2-01` | 不在本阶段 |
| 响应式 / 移动端断点系统 | UI-SPEC Q5 明文 Out of scope | 不在本阶段 |
| `#probe-controls` 的移除或重定位 | 产品行为变更,v1.14 全局已裁定不进任何阶段 | 不在本阶段 |
| `.collapse-indicator` 的越轨字面量 | backlog `999.1`;`app.js:1550` 用 `textContent` 赋值 | 留证不修 |
| backlog `999.1` / `999.2` | 各自会作废 `idi-04.1-radix` / `idi-07` 的指纹;**与本阶段合并会搅浑两批复验** | 各自独立成批处理 |
| `#selection-menu` 的定位数学与 DOM 位置 | Pitfall 8:它在旗舰交互路径上且工作正常,**不得「顺手改进」** | 不在本阶段 |

---

## UI Considerations

> 本节由 ui-phase 的 **UI-consideration probe(Step 9.5)** 在 checker 通过之后生成,
> 由 plan-phase 的 `## UI Considerations` lift 规则提升。**整节替换,不追加**(幂等)。
> 空态 / 错误态 / 加载态的**文案**不在本节重复 —— 见 `## Copywriting Contract`(去重)。
>
> **本节的当前状态:probe 尚未运行(Step 9.5 在 checker APPROVED 之后执行)。**
> 下面给出的是**供 probe 使用的元素面(作者已按 kind 预分类)** —— 它同时是 probe 的输入,
> 也是本阶段影响面的可枚举清单(本项目「影响面必须可枚举」的口径)。

**元素面(6 个,作者预分类的 kind):**

| id | 界面面 | 本阶段与它的关系 | 作者裁定的 kind |
|---|---|---|---|
| E1 | `#round-doc`(轮次文档渲染区) | **新增 Tab 停靠点 + 整盒焦点环**(K-1) | `static-content`, `interactive-control` |
| E2 | `#selection-menu` + `#btn-annotate` / `#btn-plain-ask` | **键盘路径的焦点目标**(K-2) | `interactive-control` |
| E3 | `#confirmation-modal`(含 `#confirm-word-input` / `#confirm-error` / 两个按钮) | **新增 dialog 语义 + Escape + 背景 inert**(M-1 / M-2) | `form`, `interactive-control` |
| E4 | `#tier-modal`(两个档位按钮,**无取消按钮**) | **新增 dialog 语义 + Escape + 移焦 + 标志复位**(M-1 / M-2) | `form`, `interactive-control` |
| E5 | `#app`(背景区) | **新增 `inert` 的挂载点**(M-1.3) | `static-content` |
| E6 | `#permission-modal` / `#mission-complete-modal` / `#cli-check-overlay` | **本阶段零改动**(范围锁,D-11 / D-17) | `form`, `interactive-control`, `nav` |

**两条必须先读的 probe 事实(沿用 `idi-06-UI-SPEC.md` 已登记的记录,防止把分类失真读成覆盖率):**

1. **probe 的 cue 是英文匹配,中文散文会被大量判为 `unclassified`。** 上一阶段的实测:
   首跑 10 个元素里 **8 个 unclassified**,而该阶段的核心类别(`overflow` / `long-text`)
   **全部漏检(0 条)**;作者逐条裁定 kind 覆盖后重跑才得到 `applicable 43 / unresolved 0`。
   ⇒ **首跑的数字不是覆盖率,是分类失真**;两行必须一起读,否则会把**作者裁定的成分**
   误读成**引擎的认同**。
2. **元素面必须由作者喂 override,不能只靠启发式。** 本节的 kind 列就是那份 override。

**适用类别(probe 结果未出前**不得**预先填写的部分):** 本阶段的核心状态维度是
`loading`(弹窗与菜单的中间态)与 `error`(两个弹窗的失败路径与内联错误),它们**全部继承既有实现**,
本阶段零改动;`long-text` / `overflow` 与本阶段的关系是**零**(本阶段不引入任何新容器、不改变任何换行行为)。
**具体行数(covered / backstop / unresolved)以 Step 9.5 的 probe 输出为准,由该步整节替换本表下方的空白。**

<!-- probe 输出在此下方插入(Step 9.5)。probe 未运行前本节不写任何"已覆盖"的结论。 -->

---

## Registry Safety

Not applicable —— 无 shadcn、无 registry、无第三方 block。项目没有设计系统包,也没有构建步骤(D-06)。
**本阶段零新增依赖**(硬规则 6),`frontend/vendor/` 含**恰好一个文件**(`marked.min.js`),
本阶段每个计划之后都必须仍是恰好一个文件。

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| none | none | not applicable — 无 registry 可及,也未被使用 |

---

## Checker Sign-Off

- [ ] Dimension 1 Copywriting: PASS
- [ ] Dimension 2 Visuals: PASS
- [ ] Dimension 3 Color: PASS
- [ ] Dimension 4 Typography: PASS
- [ ] Dimension 5 Spacing: PASS
- [ ] Dimension 6 Registry Safety: PASS
- [ ] Dimension 7 Inventory Provenance: PASS

**Approval:** approved(2026-09-23;checker 报 `## UI-SPEC VERIFIED`,0 BLOCKER / 2 FLAG)

**本文件为下游准备的三处「读之前必须知道」的提醒(供 checker 与 planner):**

1. **本阶段没有视觉令牌可查** —— Dimension 3 / 4 / 5 的答案是「零改动 + 零新增」,
   逐条引自 `04 / 04.1 / 05-UI-SPEC.md`,**不是本文件新写的契约**。
   本文件的契约面是**交互与状态**(键盘路径、焦点不变量 F1、两个弹窗的语义与 Escape 分派)。
2. **Dimension 1 的答案是「零新增文案」** —— 唯一例外是 §Sign-Off Items 的 **S8-1**,
   它是一条**继承自 `06-UI-SPEC.md` 的 checker FLAG**、且 06 已明确指派给「拥有 `app.js` 的阶段」。
   **该串已由用户于 2026-09-23 裁定「改」**(`左侧` → `右侧`,`app.js:1121`,一个词),
   故它现在是一条**已定稿的契约变更**,不是待裁定项 —— 下游按「本阶段要改这一处」读。
3. **Dimension 7 的答案是 `Could not enumerate: …`** —— `Tool: none`,本项目没有设计系统包。
   模板明令该情形下省略本节;本文件保留那一行以留下 provenance 槽位。

---

## Provenance

**本文件的输入(全部读自磁盘,无外部来源):**

| 来源 | 用途 |
|---|---|
| `.planning/phases/idi-08-accessibility-semantics-and-keyboard/08-CONTEXT.md` | **主输入。** D-01…D-26 全部为已锁定决策;本文件的 §键盘契约 / §弹窗契约 是它们的规格化形态 |
| `.planning/ROADMAP.md` §Phase 8 / §Phase 7 / §全局硬规则 1–7 | 意图与承诺边界;两处点名对象经 D-11 / D-05 替换后登记于 §契约修正登记 |
| `.planning/REQUIREMENTS.md` §A11Y-02/03/05/06/08 / §REG-02 / §REG-03 / §Out of Scope 表 / 文末人工验收项 | 六条需求的原文;D-18 的立场来源(Out of Scope 表原话);人工验收项的三条 |
| `.planning/STATE.md` §Operator Next Steps / §Deferred Items / §Blockers | D-04 的探针义务原文、D-26 的 04.1 复验待办、`[v1.14 P8]` 的「五条 b9664e0 修复无自动化覆盖」 |
| `frontend/index.html`(227 行,磁盘 HEAD) | **唯一事实来源。** `#app` L10–L155 · `#round-doc` L139 · 五个 `.overlay` L158/L170/L184/L196/L213 · 两个 `<h3>` L172/L186 · `#selection-menu` L207;80 个 id 全量核对 |
| `frontend/app.js`(1658 行,磁盘 HEAD) | 落点行号逐条取自该文件:L4–L83 顶层句柄 · L302-315 内联错误 · L483-556 确认弹窗与授权 · L637-640 `tierModalShown = true` · L787-807 `chooseTier` · L1202-1215 `showPermissionModal` · L1296-1300 `hideSelectionMenu` · L1323 `handleSelectionTrigger` · L1344-1350 菜单绑定 · L1361/L1391 两个菜单项 |
| `frontend/style.css`(1697 行,磁盘 HEAD) | `--color-focus` L259 · `.hidden` L574 · `#doc-panel` L603-616 · `#doc-panel-header` L641-646 · `#doc-panel-body` padding L657 · `.markdown-body` L891-894 · `#selection-menu` L1209-1225 · `#round-doc.round-frozen` L1239 · `:focus-visible` 枚举 L1508-1517 |
| `scripts/check-05-ui-uat.py`(1672 行) | `FOCUSABLE_SELECTOR` L1748 · 第 10 项的普查与判定集过滤 L1937-1992 · `_idi07_tab_drive` L2772 · 头部 docstring 的归档半场无服务对象登记 |
| `scripts/probe-07-focus-composite.py` | D-04 的复跑对象;其 Tab 驱动为数据驱动(上限 40、命中即停)⇒ 新增停靠点被自然吸收 |
| `scripts/check-01…04` | 四条不变量守卫;**本次会话实跑全部 PASS,exit 0** |
| `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` | S-1(12 档刻度)/ 硬规则 5 原始清单 / Do-Not-Touch / 例外 L-1…L-5 |
| `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` | 25 tier-1 / 47 tier-2 / 47 对清单(本阶段零改动) |
| `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` | 7 档字号 / 3 档字重 / 4 档行高;「按调用点枚举」方法论 |
| `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` | 本文件的形态范本(增量契约 / 漂移登记 / Delta Ledger / probe 记录纪律);其 checker FLAG 的过期串 → S8-1 |
| `.planning/phases/idi-07-interaction-states-and-focus/07-CONTEXT.md` + `idi-07-VERIFICATION.md` | D-05(`[tabindex]` 枚举集)/ D-06(`#round-doc` 的环指派给本阶段)/ D-14(环必须瞬变)/ `covered_files` 清单(D-25 的来源) |
| `.planning/research/PITFALLS.md` §Pitfall 6 / 5 失效模式 4 / 3 / 10 / M7 / "Looks Done But Isn't" | 本阶段的核心失效面;两处论断被本文件的实测推翻(§契约修正登记 A-3) |
| `.planning/research/SUMMARY.md` §Baseline Reconciliation | 基线数字口径(审计报告的计数是 `b9664e0` 之前的旧值) |

**外部规范依赖(仅三条,均为判据来源而非设计来源):**

- **WCAG 2.1 SC 2.1.1(Keyboard)/ SC 2.4.3(Focus Order)** —— 键盘可达性与焦点序的达标依据(§K-1.7)。
- **WCAG 2.1 SC 4.1.2(Name, Role, Value)** —— `role` 与无障碍名称的达标依据(D-14 / D-15)。
- **WAI-ARIA Authoring Practices: Dialog (Modal) Pattern** + **MDN `inert`(全局 HTML 属性)** ——
  `aria-modal` 的「背景惰性」语义是 D-14 的判据来源;`inert` 是原生、零依赖、零构建的机制(满足硬规则 6)。
- 无其他外部来源。

**环境事实(不得重新推导、不得对抗):** 截图不可用(headless 渲染被阻,且常驻 `/api/events` SSE 流让
capture handler 无法退出)⇒ **计划用计算样式检查 + 命名人工步骤,不要计划视觉 diff**;
若用 Playwright **必须** `chromium.launch({ channel: 'chrome' })`(或按 `check-05-ui-uat.py` 头部的
`--browser` 策略);**键盘文本选区无法自动化**,不得因自动测试 FAIL 判定功能缺陷。

**本次会话实测的基线(全部读自 HEAD,2026-09-23):** `node --check` OK · 四条守卫全 PASS ·
`check-02` 47 对 0 failures · `tabindex`(html/js)= 0/0 · `:focus-visible` = 9 · `role=` = 0 ·
`aria-*` = 0 · `inert` = 0/0 · `inline-error`(style.css)= 1 · `clearInlineError();`(app.js)= **9** ·
`^\.hidden {` = 1 · `!important` 命中行 = 5(声明数由 `check-04` 判为 1)。

*Phase: 8 — 可访问性语义与键盘 · UI-SPEC generated: 2026-09-23*

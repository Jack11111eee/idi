---
phase: idi-08-accessibility-semantics-and-keyboard
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - frontend/index.html
  - frontend/app.js
autonomous: true
requirements: [A11Y-02, A11Y-03]
estimate:
  tokens: 48000
  raw_tokens: 48000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # —— A11Y-02 的边界面(edge-probe resolved / explicit)——
    - "tabindex 计数与 :focus-visible 计数不得独立移动:加 tabindex=\"0\" 后 `grep -c tabindex frontend/index.html` 由 0 → 1,而 `grep -v '^#' frontend/style.css | grep -c ':focus-visible'` 保持 9(> 0)。两者同为零或同为正 —— 不存在「可聚焦但焦点不可见」的中间状态。门 = 两条计数命令 + `node --check app.js`"
    # —— 用户视角的可观察行为 ——
    - "键盘用户按 Tab 能进入轮次文档区,整盒焦点环画在 #round-doc 上"
    - "#round-doc 成为 document.activeElement 的那一刻,其计算 outline-width 恰为 2px、outline-color 等于运行时解析的 --color-focus"
    - "按住 Shift 连按方向键扩选时焦点不移动 —— 焦点环全程留在文档区(这是「键盘用户能选中多于一个字符」的唯一机械判据)"
    - "松开 Shift 时 #selection-menu 出现且焦点落在 #btn-annotate"
    - "Escape 关闭菜单后焦点回到 #round-doc(环重新画出);焦点不停在已隐藏的按钮上,也不回落到 <body>"
    - "菜单项 #btn-annotate / #btn-plain-ask 执行后焦点回到 #round-doc"
    - "#draft-content 保持无 tabindex(阶段 1-2 无批注功能 ⇒ 加它是死代码,不是漏项)"
    - "#round-doc 除 tabindex 外零新增属性:不加 role(含 role=\"region\"),不加 aria-label —— 裸 <div> 的 Tab 停靠点是知情接受的代价(D-18,用户裁定「都不加」,保持窄切片);role 与焦点陷阱一起归 v2 A11Y-V2-02"
    # —— UI-SPEC §UI Considerations 提升(E1 #round-doc / E2 #selection-menu)——
    - "E1 overflow(explicit):#round-doc 在内容超出容器时仍走既有滚动/换行路径 —— .markdown-body 的 overflow-wrap: anywhere(Phase 6 落地)与 #doc-panel-body { padding: 32px 40px } 均未改动,本阶段不新增任何容器、不新增任何裁剪规则"
    - "E1 long-text(explicit):#round-doc 的计算 overflow-wrap 仍为 anywhere,且加 tabindex=\"0\" 与整盒焦点环之后其换行行为与 HEAD 逐字一致(长不可断串仍折行、不撑破视口)"
    - "E2 long-text(explicit):#selection-menu 的两个按钮文案逐字保持「批注」/「用大白话讲这段」,不因新增的焦点交接而改动;长文案在既有宽度下不截断"
    - statement: "E1 loading(backstop):What is shown while data or content is still loading (skeleton, spinner, progressive reveal)?"
      verification: backstop
    - statement: "E1 error(backstop):What is shown when the load or submit fails (message, retry affordance, partial fallback)?"
      verification: backstop
    - statement: "E2 loading(backstop):What is shown while data or content is still loading (skeleton, spinner, progressive reveal)?"
      verification: backstop
    - statement: "E2 error(backstop):What is shown when the load or submit fails (message, retry affordance, partial fallback)?"
      verification: backstop
    - statement: "E2 overflow(backstop):What happens when content exceeds its container — scroll, clip, wrap, or truncate?"
      verification: backstop
    # —— A11Y-02 的精度面(edge-probe resolved / backstop)——
    - statement: "A11Y-02 精度面(backstop):Where can precision loss, overflow, or rounding/tie-breaking occur — and what is the exact contract (e.g. half-up vs half-to-even, ceil/floor/truncate)? —— 本阶段零数值计算面:新增的只有一个 HTML 布尔属性与约十行事件/焦点代码,无算术、无舍入、无阈值;唯一的「算术」是焦点环外伸量 2px + outline-offset 2px = 4px,它由 check-05 的 CLEARANCE_MIN_PX 承担"
      verification: backstop
  artifacts:
    - path: "frontend/index.html"
      provides: "#round-doc 带 tabindex=\"0\"(本阶段唯一一处 HTML 属性改动);零新增 id、零改名、零删除"
      contains: 'id="round-doc" class="markdown-body" tabindex="0"'
    - path: "frontend/app.js"
      provides: "initSelectionMenu() 内、紧随 L1350 keyup 绑定之后的 Shift 提交监听器 + hideSelectionMenu() 的 F1-a/b/c 焦点交还"
      contains: "hideSelectionMenu"
  key_links:
    - from: "frontend/index.html:139 (#round-doc)"
      to: "frontend/style.css:1514 ([tabindex]:focus-visible)"
      via: "Phase 7 刻意写进枚举的 [tabindex] 选择器 —— 属性一落,整盒环零 CSS 自动生效"
      pattern: "\\[tabindex\\]:focus-visible"
    - from: "frontend/app.js(initSelectionMenu 内新增的 Shift keyup 监听器)"
      to: "frontend/index.html:208 (#btn-annotate)"
      via: "松开 Shift ∧ 菜单可见 ∧ 选区非折叠 ⇒ annotateBtn.focus()"
      pattern: "annotateBtn\\.focus\\(\\)"
    - from: "frontend/app.js (hideSelectionMenu)"
      to: "frontend/index.html:139 (#round-doc)"
      via: "F1-a/b/c:隐藏前取判据 selectionMenu.contains(document.activeElement),命中则 roundDoc.focus()"
      pattern: "roundDoc\\.focus\\(\\)"
  prohibitions:
    - statement: "#round-doc 的整盒焦点环不得在实测不可辨时被静默降级为「已知局限」—— 那会造出「名义上可聚焦、实际看不出焦点在哪」的状态,正是 Pitfall 6 的失效形态;唯一合法处置是按 D-02 当场升级并接受作废 5 份 live 指纹"
      status: unresolved
    - statement: "编辑 frontend/index.html / frontend/app.js 时不得改名或删除任何既有 id —— app.js:4-75 有约 70 个顶层 getElementById 句柄,改名或删除一个 id 会在解析期静默杀死其下全部处理器(G-idi01-8);新增 id 是安全的"
      status: unresolved
    - statement: "不得把焦点移动写进 handleSelectionTrigger 或任何挂在每一次 keyup 上的处理器 —— roundDoc 的 keyup 绑定对每一次 keyup 都触发,在里面移焦会让键盘用户永远只能选中一个字符,而 A11Y-03 的验收项「Shift+方向键选区 → 菜单出现 → 焦点已入菜单」仍会照常通过(它测状态,不测可用性)"
      status: unresolved
    - statement: "焦点不得停在已隐藏的元素上,也不得因隐藏而回落到 <body> —— 键盘用户会丢失位置,要重新 Tab 穿过整个文档区与整个侧栏才能回到文档区(F1)"
      status: unresolved
    - statement: "不得在 hideSelectionMenu() 中清空 window.getSelection() —— 那会毁掉「Escape 关菜单后接着 Shift+→ 继续扩选」这条路径(D-08)"
      status: unresolved
  assumptions:
    - statement: "edge-probe 对 A11Y-03 返回 unclassified ⇒ 其边界/精度面按具名假设登记,不静默丢弃。实际边界条件已由 08-CONTEXT.md 的 D-05 / D-06 / D-09 / D-10 与 idi-08-UI-SPEC.md §K-2.1 / §K-2.5 穷举(提交手势的三条判据、鼠标路径的行为变化、焦点入菜单后高亮是否仍可见、Escape 后能否续选),规划期不另造判据"
      status: flagged
---

<!-- planner-discipline-allow: tabindex -->

<objective>
把 `#round-doc` 变成一个真实的键盘 Tab 停靠点并让键盘划词路径端到端可用(A11Y-02 + A11Y-03)。

本计划交付三件事:①`frontend/index.html:139` 的 `#round-doc` 加 `tabindex="0"`,使 Phase 7 的 `[tabindex]:focus-visible` 枚举规则**零 CSS 自动**把整盒焦点环套上去(这是本阶段唯一一处「一个属性换一条完整交互路径」的地方);②在 `initSelectionMenu()` 内、紧随既有的 `keyup` 绑定之后新增一个 **Shift 专用**提交监听器(按住 Shift 扩选时焦点不动,松开 Shift 才把焦点送入 `#selection-menu` 的首个按钮),并把 F1-a/b/c 的焦点交还写进 `hideSelectionMenu()` 这个**单点**;③把「环可辨」的实测证据、D-02 的升级判据、`probe-07-focus-composite.py` 的复跑(D-04)与 A11Y-03 的具名人工脚本一并落成可复跑的证据。

Purpose: 本阶段**按 ROADMAP 字面实现会假绿** —— 路线图写「`handleSelectionTrigger` 的键盘分支把焦点移入菜单首按钮」,而该函数挂在**每一次** `keyup` 上(`app.js:1350`):Shift+→ 选中 1 个字符即触发 keyup ⇒ 焦点跳到 `#btn-annotate` ⇒ 再按 Shift+→ 时事件目标已是菜单按钮,`roundDoc` 的 keyup 不再触发 ⇒ **键盘用户永远只能选中一个字符**;而 A11Y-03 的验收项「Shift+方向键选区 → 菜单出现 → 焦点已入菜单」**会照常通过**(它测状态,不测可用性)。本计划按 D-05/D-06 的手势实现,并把这条「按字面实现会假绿」的事实写进代码围栏注释,否则会被后来者当成「已按路线图实现」。
Output: `frontend/index.html` 的 `#round-doc` 属性;`frontend/app.js` 的 Shift 提交监听器与 `hideSelectionMenu()` 的焦点交还;以及 Task 2 / Task 3 记录的三份证据(环可辨性、D-02 判据、探针 0/1 计数、A11Y-03 人工脚本)。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/idi-08-accessibility-semantics-and-keyboard/08-CONTEXT.md
@.planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-UI-SPEC.md
@.planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-PATTERNS.md
@.planning/phases/idi-07-interaction-states-and-focus/07-CONTEXT.md
@.planning/research/PITFALLS.md
</context>

<decision_register>
**D-01 零 CSS 改动(D-01 路径):** 整盒焦点环**不需要任何新 CSS**。Phase 7 的 `[tabindex]:focus-visible`(`frontend/style.css:1514`)是**刻意**为这一刻预留的 —— 落 `tabindex="0"` 的瞬间它自动生效。**不得新增任何 `:focus` / `:focus-visible` 规则,不得写 `#round-doc:focus` 之类的专用规则**(那会与 Phase 7 的枚举集分叉,正是 `G-idi-05-1` 的成因;硬规则 10)。本计划 `frontend/style.css` **零改动** ⇒ 本阶段在 D-01 路径下**零验证指纹债务**(`frontend/app.js` / `frontend/index.html` 不在任何 live 报告的 `covered_files` 里,D-25)。

**D-01 的几何前提(实测证据,规划期已写进计划):** `#round-doc` 的父级 `#doc-panel-body { padding: var(--space-8) var(--space-10) }`(`frontend/style.css:657` = `32px 40px`);环 `outline: 2px` + `outline-offset: 2px` 画在边框盒**外** 2–4px,落在父级 40px 水平 padding 里 ⇒ **不被裁切**;`#round-doc` 盒高数千像素(远超视口)⇒ 视口里看到的是**左右两条贯穿全高的竖线**,不是「只有上下边缘」。**研究 `PITFALLS.md` §Pitfall 5 失效模式 4 的「只有上下边缘可见」论断因此被几何推翻** —— 本项目纪律是「实测驱动,不采信上游文档的论断」。**注意 ROADMAP 点名的落点 `#doc-pane` 在 HEAD 上根本不存在**(04.1 D-13 已改名 `#doc-panel-body`)。

**D-05 / D-06 提交手势:** 提交手势 = **抬起 Shift**。按住 Shift 扩选时焦点**不动**;**松开 Shift** 时菜单弹出并把焦点送入 `#btn-annotate`。`handleSelectionTrigger`(`app.js:1323-1340`)**一字不改** —— 它挂在每一次 keyup 上,给**它**加按键白名单会改变鼠标路径与 t8g 既有决定的实质。**白名单只存在于本计划新增的 Shift 专用监听器里。** t8g 的既有决定原文(`app.js:1321-1322`)继续对它生效。

**D-20 `#draft-content` 的刻意不对称:** `frontend/index.html:113` 的 `#draft-content` 同为 `.markdown-body`,**不加 `tabindex`**。这是**正确的、不是漏项**:`handleSelectionTrigger` 的第一条实质守卫是 `if (currentState !== 'phase3') return`(`app.js:1327`)⇒ 阶段 1-2 根本没有批注功能,给它加 Tab 停靠点是**死代码**(违反本项目「不声明不被消费的东西」的纪律,且无法被运行时验证)。**读代码的人若不看这条理由,会把它当漏项补上。**

**D-02 升级路径(已签核,由实测触发而非备选偏好):** 若实测判定整盒环**不可辨**,当场升级为改 `frontend/style.css`,并接受作废 5 份 live 指纹(`idi-04` / `idi-04.1-radix` / `idi-05` / `idi-06` / `idi-07`)、连带复验(D-25)。**不得把「不可辨」静默降级为已知局限。** 判据「不可辨」的定义(触发 D-02 的唯一条件):环的任一段被裁切 **或** 与相邻像素对比 < 3:1 **或** 无法据此定位焦点在哪。

**D-03 两处普查变化(登记,不「修」):** ①`#round-doc` 在 **p3 / checking / archive** 三个样本里进入 `check-05 --item 10` 的判定集;**p1 / p12 里它在 `.hidden` 子视图内 ⇒ 被 `visible` 过滤排除**。②`_idi07_tab_drive(page, len(data) + 8)` 的上限是**数据驱动**的:判定集 +1 ⇒ 上限 +1,而 Tab 序也多一个停靠点(+1),两者恰好相抵,**无需改门**(但必须在 SUMMARY 里登记这条算术)。**若该项在某个样本变红,先判它是「真缺陷」还是「普查集变化」,不要直接改门。**

**D-04 探针复跑义务:** `#round-doc` 入册后**必须复跑** `scripts/probe-07-focus-composite.py`(STATE.md 的 Deferred Items 已逐字登记该义务)。**复跑时必须逐字记录「注入前 / 注入后计数仍为 0 / 1」**,否则无法区分「探针在工作」与「探针静默空转」。**探针不进守卫契约**(与 `scripts/probe-07-focus-composite.py` 同定位的一次性探针)。

**D-25 指纹义务:** 本计划在 D-01 路径下**零债务**;只有 D-02 被实测触发(改 `frontend/style.css`)才作废 5 份。⚠ **不得用 `gsd-tools query verification status <phase>` 判定 stale** —— 本项目已记录:这些相位目录一律返回 `missing`(相位目录命名与工具的相位令牌解析不匹配)。

**硬规则 5 / 8:** `frontend/index.html` / `frontend/app.js` 的每一次编辑都必须先确认「没有改名、没有删除既有 id」。`frontend/index.html` 今天恰好 **80 个 id**,本计划**一个都不增**。
</decision_register>

<flagged_assumptions>
边缘覆盖探针对本阶段六条需求里的五条(A11Y-03 / A11Y-05 / A11Y-06 / A11Y-08 / REG-03)全部返回 `unclassified` / `unresolved` —— 探针的分类词表是**英文**的,而本阶段的需求文本是**中文散文**,故分类基本无信息量(`A11Y-02` 的两条 `resolved` 行也部分是分类器产物)。**不得把 `unclassified` 当作「无边缘情况」,也不得自动 resolve。** 本计划登记 A11Y-03 一条:

- **A11Y-03(本计划)** — 假设:键盘划词的边缘条件**已由上游决策穷举**,本计划不另造判据 —— 提交手势的三条合取判据(`e.key === 'Shift'` ∧ 菜单可见 ∧ 选区非折叠)见 `08-CONTEXT.md` D-06;鼠标路径的行为变化(鼠标 Shift+点击扩选后松开 Shift 也会移焦,判定为可接受)见 D-09;两条**必须实测而非假设**的项(焦点入菜单后高亮是否仍可见;Escape 交还后能否接着 Shift+→ 续选)见 D-10 与 UI-SPEC §K-2.5。**不在范围内**:焦点陷阱、完整 ARIA、键盘划词的可发现性提示(D-19,登记为已知局限)、`window.prompt` 的替换(v2 `FLOW-V2-01`)。
</flagged_assumptions>

<artifacts_this_phase_produces>
本阶段(三个计划合计)新建的符号与路径 —— 每个计划重复列出同一份清单,便于逐计划对照:

**新的 DOM id(2 个,全部在 `frontend/index.html`;硬规则 5 禁的是改名与删除,新增是安全的):**
- `confirmation-modal-title`(计划 02;`#confirmation-modal` 的 `<h3>`)
- `tier-modal-title`(计划 02;`#tier-modal` 的 `<h3>`)

**新的 HTML 属性:**
- `#round-doc` 的 `tabindex="0"`(本计划,`frontend/index.html:139`)
- `#confirmation-modal` / `#tier-modal` 的 `role="dialog"` + `aria-modal="true"` + `aria-labelledby`(计划 02)

**新的 JS 顶层句柄(1 个,`frontend/app.js`):**
- `appEl`(`document.getElementById('app')`,加在 `app.js:83` 之后;计划 02)

**新的 JS 函数(1 个):**
- `syncBackgroundInert()`(计划 02;从两个弹窗的 `.hidden` 现状**派生**,不成对记账)

**新的 JS 事件监听器(2 个,均为匿名箭头函数,不引入具名 handler):**
- Shift 提交监听器(本计划;`document` 上的 `keyup`,写在 `initSelectionMenu()` 内 ⇒ 继承该函数的一次性绑定守卫)
- Escape 单点分派监听器(计划 02;顶层 `document` 上的 `keydown`,一次性绑定)

**新的 JS 代码(无新符号):**
- `hideSelectionMenu()` 体内的 F1-a/b/c 焦点交还(本计划)
- `#tier-modal` 打开分支的移焦 + `tierModalShown` 复位(计划 02)
- `syncBackgroundInert()` 的 5 个调用点(计划 02;全部在既有函数体内)
- `app.js:1121` 空态文案的一个词(计划 03)

**新的 CSS:零。** 焦点环由 Phase 7 的 `[tabindex]:focus-visible` 枚举自动命中,本阶段 `frontend/style.css` **逐字节不变**(D-01)。

**新的脚本 / 新文件 / 新依赖:零。** `scripts/check-05-ui-uat.py` 与 `scripts/check-01…04` 零改动(D-21 / A-4);`frontend/vendor/` 仍恰好一个文件(`marked.min.js`);无构建步骤(硬规则 6)。
</artifacts_this_phase_produces>

<tasks>

<task type="tracer">
  <name>Task 1 (tracer):#round-doc 的 Tab 停靠点端到端 —— 一个属性 → Phase 7 的枚举规则 → 浏览器里读到的整盒环</name>
  <files>frontend/index.html</files>
  <read_first>
    - frontend/index.html(L133-146:`#rounds-placeholder` 子视图、`#rounds-hint`、`#round-doc`(L139)、`#authorize-row`;L113 的 `#draft-content` —— 那个**不得**加属性的对照物;L207-211 的 `#selection-menu`)
    - frontend/style.css(L1496-1517:围栏注释 + 七选择器 `:focus-visible` 枚举,`[tabindex]:focus-visible` 在 L1514;L657 的 `#doc-panel-body { padding: var(--space-8) var(--space-10) }` —— D-01 的几何前提;L259 的 `--color-focus`)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-UI-SPEC.md(§K-1.1 / §K-1.2 / §K-1.6 / §K-1.7)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-PATTERNS.md(H-1 与 Shared Patterns § Focus ring)
    - scripts/check-05-ui-uat.py(L1748 的 `FOCUSABLE_SELECTOR`、L1988 的 `focusable` 判据、L2830-2854 的判定集与 `bad` 过滤、L31-105 的 docstring 登记)
  </read_first>
  <action>
    在 `frontend/index.html:139` 的 `#round-doc` 上**只加一个属性**。当前形态是 `<div id="round-doc" class="markdown-body">`,目标形态是 `<div id="round-doc" class="markdown-body" tabindex="0">` —— 属性顺序照本文件既有惯例(`id` → `class` → 新属性),`tabindex="0"` 放在 `class` 之后。**不新增 id、不改名、不删除任何既有 id**(硬规则 5 / G-idi01-8:`app.js:4-75` 约 70 个顶层 `getElementById` 句柄,改名或删除一个会在解析期静默杀死其下全部处理器)。**`frontend/index.html` 今天恰好 80 个 id,本任务之后仍是 80。**

    **不要动 `frontend/index.html:113` 的 `#draft-content`。** 它同为 `.markdown-body`,但阶段 1-2 没有批注功能(`handleSelectionTrigger` 的第一条实质守卫是 `if (currentState !== 'phase3') return`,`app.js:1327`)⇒ 给它加 Tab 停靠点是**死代码**,违反本项目「不声明不被消费的东西」的纪律,且无法被运行时验证(D-20)。**这条理由必须写进下面那条围栏注释**,否则读代码的人会把它当漏项补上。

    **不要改 `frontend/style.css` 的任何一行。** 落 `tabindex="0"` 的瞬间,`frontend/style.css:1514` 的 `[tabindex]:focus-visible` 自动把 `outline: 2px solid var(--color-focus)` + `outline-offset: 2px` 套上去。**不得新增任何 `:focus` / `:focus-visible` 规则,不得写针对 `#round-doc` 的专用焦点规则** —— 那会让「规则覆盖了谁」与「门检查了谁」分叉(`G-idi-05-1` 的成因;硬规则 10)。

    **`#round-doc` 除了这个属性之外一个属性都不加(D-18,用户裁定「都不加」,保持窄切片)。** 不加 `role`(不加 `role="region"`),不加 `aria-label`。加了 `tabindex="0"` 之后它是一个**裸 `<div>` 的 Tab 停靠点**,辅助技术只会报「通用容器」—— 这是**知情接受的代价,不是疏漏**。理由取自用户自己立的立场:`REQUIREMENTS.md` 的 Out of Scope 表把「完整 ARIA」排除的原话是「ARIA 服务于不带上下文到达、且看不见屏幕的用户;本工具恰好一个用户,既是作者也看得见屏幕」。`role` 与焦点陷阱等一起归 v2 `A11Y-V2-02`。**这条必须写进围栏注释**,否则会被读者当成漏项补上。

    **围栏注释(加在 `#round-doc` 上方,照本文件既有的 `<!-- … -->` 形态;注释一律中文,写「为什么」而不是「是什么」):** 必须写明四条事实 ——
    ① **零 CSS 履约的机制**:环来自 `frontend/style.css:1514` 的 Phase 7 焦点环枚举规则(Phase 7 D-05 刻意把「带本任务新加的这个属性的元素」写进 `:focus-visible` 枚举,就是为了让本阶段零 CSS 交付),**不是**本文件或 `style.css` 里新写的规则;⚠ **点名该出处时不得写出选择器字面量**(`[tabindex]:focus-visible`)—— 那一行本身会引入第二个命中行,直接打破本任务 `grep -c 'tabindex' frontend/index.html` == 1 的门;用「`frontend/style.css:1514` 的 Phase 7 焦点环枚举规则」这样的措辞指代即可(验收面只要求规则出处,不要求字面量);
    ② **整盒环的几何**:`#doc-panel-body` 有 `32px 40px` 的内边距 ⇒ `outline-offset: 2px` 的环外伸 2–4px 落在父级 40px 水平 padding 里、**不被裁切**;盒高数千像素 ⇒ 视口里是**左右两条贯穿全高的竖线**。点名这条推翻了上游研究里「只有上下边缘可见」的论断,本项目纪律是「实测驱动,不采信上游文档的论断」;
    ③ **`#draft-content` 的刻意不对称**(上面那段 D-20 的理由);
    ④ **Pitfall 6 的门为什么由构造满足**:`tabindex` 计数 0 → 1 而 `:focus-visible` 计数 9 → 9,看似「独立移动」,实则不然 —— Phase 7 已把环的承载面先落地;**机械证据不是计数,是 `check-05 --item 10` 的运行时读数**(`#round-doc` 成为 `document.activeElement` 的那一刻读到 `2px` / 运行时解析的 `--color-focus`)。

    ⚠ **注释散文同样计入按子串计数的判据**:本任务**不得**在注释里写出任何 `tabindex` 之外的新属性字面量形态;`grep -c tabindex frontend/index.html` 的期望值恰为 **1**,所以注释里**不要**出现第二个 `tabindex` 字样 —— 讲「为什么加」时用「这个属性」「焦点停靠点」等措辞,不要复述属性名。

    最后,把**执行前基线**跑一遍并逐条登记到 SUMMARY 的「基线对账」节:`grep -c 'inline-error' frontend/style.css`(期望 1)、`grep -c 'clearInlineError();' frontend/app.js`(期望 **9**,不是 6 —— `08-CONTEXT.md` D-21 的「6」来自 `b9664e0` 时代的旧 gate,照抄会造出永远不会失败的假门)、`grep -c ':focus-visible' frontend/style.css`(期望 9)、`grep -c '^\.hidden {' frontend/style.css`(期望 1)、`grep -c 'role=' frontend/index.html`(期望 0)、`grep -c inert frontend/app.js`(期望 0)、`grep -c 'hideSelectionMenu' frontend/app.js`(期望 **7** —— Task 3 的绝对判据)、`grep -c 'window.getSelection' frontend/app.js`(期望 **1** —— Task 3 的绝对判据,Task 3 之后应为 **2**)。**先建立基线,再登记本任务打破的项(只有 `tabindex` 一项:0 → 1)。**
  </action>
  <verify>
    <automated>grep -c 'tabindex' frontend/index.html</automated>
    <fails_when>输出不是恰好 `1`(`grep -c` 在计数为 0 时退出码为 1;输出 `2` 或更多说明注释或元素里混进了第二个属性字面量)</fails_when>
    <automated>grep -c 'tabindex' frontend/app.js</automated>
    <fails_when>输出不是恰好 `0`(`app.js` 不写属性;非零说明改动越界到了 JS 侧)</fails_when>
    <automated>grep -v '^#' frontend/style.css | grep -c ':focus-visible'</automated>
    <fails_when>输出不是恰好 `9`(少于 9 说明误删或误改了 Phase 7 的枚举;多于 9 说明新增了专用焦点规则 —— 硬规则 10)</fails_when>
    <automated>cd frontend && node --check app.js</automated>
    <fails_when>任何非空输出或非零退出(本任务不改 `app.js`,这一步只证明改动没有意外波及 JS 侧)</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 10</automated>
    <fails_when>退出码非 0(0 = 全 PASS;1 = 有 FAIL 断言;2 = 有 BLOCKED 断言 —— 环色读不出、期望令牌解析不出、或 Tab 后 `activeElement` 不是预期元素都会走 BLOCKED),或输出里出现任何 `FAIL` / `BLOCKED` 开头的行,或 `item10` 的普查 INFO 行里不含 `round-doc`</fails_when>
    <human-check>
      <test>在 p3 样本里按 Tab 直到焦点进入轮次文档区(焦点环画出)</test>
      <expected>环是**左右两条贯穿视口全高的竖线**(不是只有上下边缘);环与 `#doc-panel` 背景(`#f9f9f9`)一眼可区分;环**不压住**正文首字/末字。判据「不可辨」的定义(触发 D-02 的唯一条件):环的任一段被裁切 **或** 与相邻像素对比 &lt; 3:1 **或** 无法据此定位焦点在哪</expected>
      <why_human>「可辨」是人眼判断;本环境截图不可用(headless 渲染被阻,常驻 `/api/events` SSE 流让采集处理器无法终止)⇒ 用计算样式检查 + 具名人工步骤,不得计划视觉 diff。机器半场已由 `check-05 --item 10` 的运行时读数覆盖(§K-1.2)</why_human>
    </human-check>
  </verify>
  <acceptance_criteria>
    - `frontend/index.html` 的 `#round-doc` 元素带 `tabindex="0"`,且该文件里 `tabindex` 的出现次数恰为 1。
    - `frontend/index.html` 里 `#draft-content` 仍然无 `tabindex`;`frontend/index.html` 的 id 总数仍为 80。
    - `frontend/style.css` 逐字节未改(`git status --porcelain -- frontend/style.css` 为空),`:focus-visible` 计数仍为 9。
    - `frontend/app.js` 未改(`tabindex` 计数 0,`node --check` 通过)。
    - `#round-doc` 上方存在围栏注释,逐条写明:零 CSS 履约的机制与规则出处(`frontend/style.css:1514`)、整盒环的几何(父级 40px 水平 padding ⇒ 不被裁切 ⇒ 左右两条竖线)、`#draft-content` 不加的 D-20 理由、以及「计数 0→1 / 9→9 不构成 Pitfall 6 违规、机械证据是运行时读数」。
    - `check-05 --item 10` 在 p3 样本上把 `#round-doc` 纳入判定集,且其运行时读数 `outline-width` == `2px`、`outline-color` == 运行时解析的 `--color-focus`;p1 / p12 两个样本里 `#round-doc` 因落在 `.hidden` 子视图内而不进判定集(这是 D-03 的预期,不是回归)。
    - SUMMARY 里登记 `_idi07_tab_drive` 上限的数据驱动算术(判定集 +1 ⇒ 上限 +1,与 Tab 序 +1 相抵,无需改门)。
  </acceptance_criteria>
  <reversibility rating="costly">D-01 的承载面一旦由实测判定不可辨就要换成改 frontend/style.css,作废 5 份 live 指纹并连带复验(D-25);回退是改 CSS 换承载面,不是改一个属性。</reversibility>
  <done>#round-doc 是一个真实的 Tab 停靠点,且整盒焦点环零 CSS 自动生效;`check-05 --item 10` 在 p3 / checking / archive 三个样本上读到 `2px` / 运行时解析的 `--color-focus`;四条既有不变量守卫(check-01…04)仍全绿;基线对账节记录了 `clearInlineError();` = 9 与 `:focus-visible` = 9。整条链路(HTML 属性 → 继承的 CSS 规则 → 浏览器计算样式读数)已在一个提交里可复跑。</done>
</task>

<task type="auto">
  <name>Task 2:环的可辨性实测与 D-02 判定 + probe-07 的复跑(D-04)+ #draft-content 的反漏项登记</name>
  <files>scripts/probe-07-focus-composite.py(仅复跑,零改动)</files>
  <precondition>.venv 里可导入 playwright 且捆绑 chromium 可用(`.venv/bin/python -c "import playwright; print('ok')"` 退出 0),并且 `scripts/ui-states/` 下 p3 / checking / archive 三个样本目录都存在</precondition>
  <read_first>
    - scripts/probe-07-focus-composite.py(L1-30 的 docstring:它是**反事实证据而不是门**;L160-235 的六段断言 —— 态的前提检查、注入前计数 == 0、注入后计数 == 1、Tab 驱动到注入链接、环色/环宽读数、归档 0.75 合成下的对比度)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-UI-SPEC.md(§K-1.2 的「可辨」两半判据与「不可辨」定义;§K-1.3 的 D-02 两条备选承载面 B-1 / B-2;§K-1.8 的探针复跑义务)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/08-CONTEXT.md(D-02 / D-03 / D-04 / D-20 / D-25)
    - .planning/STATE.md(§Deferred Items 里 `[v1.14 P7]` 那条逐字登记的探针复跑义务)
    - scripts/check-05-ui-uat.py(L2830-2854:判定集与 `bad` 过滤 —— 判红时先读它再决定动作)
  </read_first>
  <action>
    **第一件:复跑 `scripts/probe-07-focus-composite.py`,逐字记录两个计数。** 用 `.venv/bin/python scripts/probe-07-focus-composite.py`。该探针是 D-04 的复跑对象,原因逐字来自 STATE.md 的 Deferred Items:`#round-doc` 入册后,`.archive-mode` 0.75 合成下的**运行时**环断言**第一次有了服务对象**(五个样本里 `#round-doc` 内 `a[href]` 计数为 0,此前由常驻算术门 `check-02` 的 `--color-focus ON --color-surface NON-TEXT@0.75` 单独承担)。**探针不进守卫契约**(与一次性注入探针同定位)。

    ⚠ **必须在 SUMMARY 里逐字记录探针的两条自证输出**:`PROBE links-before=0` 与 `PROBE links-after=1 (mutation-applied=yes)`,以及 `PROBE archive-state opacity=0.75 …`、`PROBE focus=…`、`PROBE ring outline-color=… outline-width=…`、`PROBE composite ring=… ratio=… (>= 3.0)`。**不记录这两条计数就无法区分「探针在工作」与「探针静默空转」** —— 这是探针自己的设计承诺,也是本任务的验收面。探针的 Tab 驱动是**数据驱动**的(上限 40 次、命中即停)⇒ 新增的 Tab 停靠点会被自然吸收,探针**零改动**。

    **第二件:在 p3 / checking / archive 三个样本上各跑一次 `check-05 --item 10`**,逐样本记录判定集大小与 `#round-doc` 的读数,并登记 D-03 的两处普查变化(判定集在这三个样本里 +1;p1 / p12 里因 `.hidden` 子视图被 `visible` 过滤排除)。**若某个样本变红,先判它是「真缺陷」还是「普查集变化」,不要直接改门**(D-03);判据在 `scripts/check-05-ui-uat.py:2830-2854` 的 `judged` / `bad` 两段。

    **第三件:把「环可辨」的人半场判据落成一条具名人工步骤,并登记 D-02 的分支。** 具名步骤(逐条记录观察结果):进 p3 样本 → 按 Tab 直到焦点落在轮次文档区 → 观察 ①环是否为**左右两条贯穿视口全高的竖线**;②环与 `#doc-panel` 背景(`#f9f9f9`)是否一眼可区分(实测 5.62:1,远高于 3:1 非文本下限);③环是否压住正文首字/末字(整盒环**不应**压字)。**「不可辨」= 环的任一段被裁切 ∨ 与相邻像素对比 < 3:1 ∨ 无法据此定位焦点在哪 —— 三条任一成立即触发 D-02。**

    **D-02 的分支处置(必须写进 SUMMARY,不得留空):**
    - **可辨** ⇒ 记录「D-01 路径成立,本阶段零 CSS 改动、零指纹债务」,继续 Task 3。
    - **不可辨** ⇒ **不得静默降级为已知局限**(那会造出「名义上可聚焦、实际看不出焦点在哪」的状态,正是 Pitfall 6 的失效形态)。**停下并上报用户**,因为该升级**超出本计划的 `files_modified`**:它要改 `frontend/style.css`(新增一条规则),并连带 ①5 份 live 指纹以 **HEAD 内容重算**(不是看 mtime —— stale 有两种成因,「内容真变」走重新验证、「记账性编辑」走重算 + 披露,补救方向相反);②`check-05` 的静态计数门是否受影响;③`§Deliberate Delta Ledger` 的 **D8-9** 由条件项转为实际项;④硬规则 7 生效(该 `style.css` 计划必须带运行时验证,不能只有静态计数)。备选承载面两条(UI-SPEC §K-1.3):**B-1 内嵌环**(`outline-offset: -2px`;**不推荐** —— `.markdown-body` 无内边距,竖线会压在每行正文的首字与末字上);**B-2 页头环**(把环挑到恒可见的 sticky `#doc-panel-header` 上,**推荐** —— 36px 紧凑环、不与正文重叠、`:has()` 有 Phase 6 的 `:has(:empty)` 先例)。

    **第四件:登记 `#draft-content` 的反漏项事实。** 在 SUMMARY 里写明 `frontend/index.html:113` 的 `#draft-content` **刻意不加** `tabindex`(D-20 的理由:`handleSelectionTrigger` 的第一条实质守卫是 `currentState !== 'phase3'`,阶段 1-2 无批注功能 ⇒ 加它是死代码且无法被运行时验证)。**这条登记的目的是让后来的读者读不出「A11Y-02 只点名了 `#round-doc`」的漏项。**

    本任务**不改任何文件**;它的产物是三份记录(探针计数、三样本读数、可辨性判定 + D-02 分支)。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/probe-07-focus-composite.py</automated>
    <fails_when>退出码非 0,或 stderr 出现 `PROBE FAILED`,或 stdout 缺 `PROBE links-before=0` / 缺 `PROBE links-after=1 (mutation-applied=yes)`,或 `PROBE composite` 行里的 `ratio=` 值 &lt; 3.00</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 10</automated>
    <fails_when>退出码非 0,或输出里出现任何 `FAIL` / `BLOCKED` 开头的行(判红时先按 D-03 判「真缺陷 vs 普查集变化」,不要直接改门)</fails_when>
    <automated>git status --porcelain -- frontend/style.css scripts/probe-07-focus-composite.py</automated>
    <fails_when>输出非空(本任务零改动;`frontend/style.css` 出现任何 diff 说明 D-01 路径被破坏)</fails_when>
    <human-check>
      <test>在 p3 样本里按 Tab 把焦点送进轮次文档区,逐条记录三个观察:①环的形态;②环与 `#doc-panel` 背景(`#f9f9f9`)是否一眼可区分;③环是否压住正文首字/末字</test>
      <expected>①环是左右两条贯穿视口全高的竖线(不是只有上下边缘);②一眼可区分(实测 5.62:1);③不压字。三条任一不成立即为「不可辨」⇒ 触发 D-02,停下并上报,不得静默降级为已知局限</expected>
      <why_human>「可辨」是人眼判断,且本环境截图不可用(headless 渲染被阻 + 常驻 `/api/events` SSE 流让采集处理器无法终止)⇒ 用计算样式检查 + 具名人工步骤,不得计划视觉 diff</why_human>
    </human-check>
  </verify>
  <acceptance_criteria>
    - SUMMARY 里逐字记录了探针的 `PROBE links-before=0` 与 `PROBE links-after=1 (mutation-applied=yes)` 两条自证输出,以及 `PROBE archive-state opacity=0.75`、`PROBE focus=`、`PROBE ring outline-color=… outline-width=…`、`PROBE composite … ratio=… (>= 3.0)` 四条读数。
    - SUMMARY 里逐样本记录了 `check-05 --item 10` 在 p3 / checking / archive 三个样本上的判定集大小与 `#round-doc` 读数,并登记了 D-03 的两处普查变化与 `_idi07_tab_drive` 上限的数据驱动算术。
    - SUMMARY 里记录了「可辨 / 不可辨」的判定与逐条观察结果;若判为「不可辨」,则记录了已停下上报、未静默降级,并列明 D-02 的 4 项连带登记与两条备选承载面。
    - SUMMARY 里登记了 `#draft-content` 刻意不加 `tabindex` 的 D-20 理由。
    - `git status --porcelain` 对 `frontend/style.css` 与 `scripts/probe-07-focus-composite.py` 均为空(探针是复跑,不是修改)。
  </acceptance_criteria>
  <reversibility rating="costly">D-02 一旦触发就要改 frontend/style.css 并作废 5 份 live 指纹(idi-04 / idi-04.1-radix / idi-05 / idi-06 / idi-07),连带复验;这不是一行回退能收口的。</reversibility>
  <done>探针复跑通过且两条自证计数(0 / 1)被逐字记录;三个样本的 `check-05 --item 10` 读数被逐样本记录并登记了 D-03 的普查变化;环的可辨性判定被逐条记录,且 D-02 的分支处置(可辨 → 继续;不可辨 → 停下上报并登记 4 项连带义务)有明确结论;`#draft-content` 的反漏项理由已登记。</done>
</task>

<task type="auto">
  <name>Task 3:键盘划词的提交手势与焦点交接(A11Y-03)—— Shift 专用监听器 + hideSelectionMenu() 单点交还 + 具名人工脚本</name>
  <files>frontend/app.js</files>
  <precondition>应用可在本机启动并能在浏览器里打开,且 `scripts/ui-states/` 下存在一个 phase3 可用的状态样本(p3)</precondition>
  <read_first>
    - frontend/app.js(L1285-1300:`selectionInRoundDoc` / `hideSelectionMenu` 的现状;L1302-1320:`showSelectionMenu`;L1321-1340:t8g 的「不做按键白名单」注释原文与 `handleSelectionTrigger` 全文 —— **它一字不改**;L1342-1423:`initSelectionMenu` 全文,尤其 L1349-1350 的两条绑定、L1352-1358 的 mousedown/scroll 关闭器、L1361/L1391 两个菜单项 handler;L94 的 `tierModalShown` 声明区 —— 了解顶层 `let` 的既有写法)
    - frontend/index.html(L207-211:`#selection-menu` 与两个菜单项按钮 —— **DOM 位置不得改动**)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-UI-SPEC.md(§K-2.1 / §K-2.2 / §K-2.3 / §K-2.4 / §K-2.5 / §K-2.6)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-PATTERNS.md(J-2 / J-4 / J-9 与 Shared Patterns § F1)
    - .planning/quick/260916-t8g-ui-5-blocker-hidden-sse-onerror/260916-t8g-PLAN.md(§`<verification>` 的第 4 条原文 —— 本任务第 4 步要重写它)
  </read_first>
  <action>
    **第一处:`initSelectionMenu()` 内新增 Shift 专用提交监听器。** 落点在 `frontend/app.js:1350` 的 `roundDoc.addEventListener('keyup', handleSelectionTrigger);` **之后**(仍在 `initSelectionMenu()` 函数体内 —— 这样它继承该函数的一次性绑定守卫,`app.js:1343-1346`,不会重复绑定)。绑定目标是 `document`(不是 `roundDoc` —— Shift 的 keyup 只在焦点位于 `#round-doc` 子树内时才在扩选语境下发生,那恰好是「扩选结束」的时刻;绑 `document` 才能在该时刻稳定捕获)。

    监听器的形态照本函数内既有的两个关闭器(`app.js:1353-1358`)的**守卫优先、匿名箭头函数、无具名 handler** 形态。三条合取判据**同时成立才移焦**,任一条不成立即 no-op:①`e.key === 'Shift'`;②菜单**未**隐藏(`selectionMenu.classList.contains('hidden')` 为假 —— 这是 `classList.contains` 的既有用法,见 `app.js:1354` 与 `:1305` 的正反两例);③选区存在且**非折叠**(复用 `app.js:1329-1330` 的 `window.getSelection()` 判据形态:`!selection || selection.isCollapsed` 为假)。三条都成立时调用 `annotateBtn.focus()`(`annotateBtn` 是 `app.js:52` 的既有顶层句柄)。空选区、折叠选区、菜单已隐藏这三种情形**都不需要在这里处理** —— `handleSelectionTrigger` 的既有守卫已经覆盖。

    **围栏注释必须写明四件事(否则会被后来的读者当成违例删掉):**
    ① 手势语义:**按住 Shift 扩选时焦点不动,松开 Shift 才把焦点送入菜单首按钮**;
    ② **为什么不能写在 `handleSelectionTrigger` 里** —— 那个函数挂在**每一次** `keyup` 上(`app.js:1350`),在里面移焦会让键盘用户**永远只能选中一个字符**(Shift+→ 选中 1 个字符 ⇒ keyup ⇒ 焦点跳到 `#btn-annotate` ⇒ 再按 Shift+→ 时事件目标已是菜单按钮,`roundDoc` 的 keyup 不再触发);而 A11Y-03 的验收项「Shift+方向键选区 → 菜单出现 → 焦点已入菜单」**仍会照常通过**(它测状态,不测可用性)—— 这就是「按路线图字面实现会假绿」的机制事实;
    ③ **白名单的边界**:`handleSelectionTrigger` **一字不改**;t8g 的既有决定(`app.js:1321-1322` 的「不对 keyup 做按键白名单 —— 『折叠/空白选区即关闭菜单』已让非选择类按键成为安全 no-op」)**继续对它生效**;按键白名单**只存在于这个新增的 Shift 专用监听器里**。**新增监听器偏离该决定的实质,不是它被推翻**;
    ④ 已登记的代价:「松开 Shift 即提交」是**自造惯例**(非平台约定);它引入了一个按键白名单事实;鼠标路径的副作用见 §K-1.5。

    **第二处:`hideSelectionMenu()` 加 F1-a/b/c 焦点交还(单点,不散落到四个调用点)。** 该函数今天只有两行(`selectionMenu.classList.add('hidden'); menuSelection = null;`),**四个调用点**是 `document` 的 mousedown 关闭器、`window` 的 scroll 捕获关闭器、`handleSelectionTrigger` 的两条守卫、两个菜单项点击 —— **散落到调用点必然漏**,所以写在这一个函数里。

    两条硬约束:
    ① **判据必须在 `classList.add('hidden')` 之前取** —— 焦点元素一旦变成 `display: none`,`document.activeElement` 会立刻回落到 `<body>`,之后再判**永远为假**。判据形态:`selectionMenu.contains(document.activeElement)`(本文件唯一的 `.contains(document.activeElement)` 用法;最近的既有「包含」写法是 `app.js:1292` 的 `roundDoc.contains(el)`)。把结果存进一个局部常量,再隐藏,再按该常量决定是否 `roundDoc.focus()`。
    ② **不得清空 `window.getSelection()`** —— 那会毁掉「Escape 关菜单后接着 Shift+→ 继续扩选」这条路径(D-08)。
    目标形态:取判据 → `selectionMenu.classList.add('hidden')` → `menuSelection = null` → 若判据为真则 `roundDoc.focus()`。**目标不可聚焦时静默降级**(`#round-doc` 不可聚焦的情形:非 phase3、或被祖先 `.hidden` 藏住)—— **不新增任何兜底逻辑**。
    注释写明这条交还覆盖 F1 的三个落点(F1-a 菜单被隐藏时、F1-b **菜单项执行后 —— D-07 的第三条腿,ROADMAP 未提**:两个菜单项都会先 `hideSelectionMenu()`,而焦点当时停在一个**已隐藏的按钮**上 ⇒ 回落到 `<body>`,键盘用户要重新 Tab 穿过整个侧栏;两个菜单项都先调它、F1-c Escape 关菜单),并写明为什么写在这里而不是四个调用点。

    **第三处:A11Y-03 的具名人工验收脚本(逐项记录观察结果,含每一步的焦点位置)。** 这是 REG-03 第 4 条重写后的形态 —— **原文预期是「菜单出现」,而 D-05 之后键盘路径多了一个「松开 Shift」的动作 ⇒ 原先通过的检查现在测的是另一件事**(与 Pitfall 3 / Pitfall 6 的「人工检查被继承而非重跑」同类失效)。步骤:
    1. 进入 p3 样本(或任何 phase3 项目)。
    2. 按 Tab 到轮次文档区(焦点环画出)—— 记下它在 Tab 序里的位置(在 `#round-switcher` 之后、`#authorize-row` 的按钮可见时之前;§K-1.7)。
    3. 按住 Shift,连按 → 数次,扩选一段文字 —— **观察:焦点环全程仍画在文档区、不跳走**(这是 K-2.1 的判据)。
    4. **松开 Shift** —— 菜单出现在选区右下,焦点落在 `#btn-annotate` —— **观察:扩选高亮是否仍可见**(§K-2.5 ①)。
    5. 按 Tab → 焦点移到 `#btn-plain-ask`;按 Shift+Tab → 回到 `#btn-annotate`。
    6. 按 Escape → 菜单消失,焦点回到 `#round-doc`(环重新画在文档区)。
    7. 再次按住 Shift + → —— **观察:能否继续扩选**(§K-2.5 ②)。
    8. 真实完成一次批注:重做 3–4 → 按 Enter 激活 `#btn-annotate` → 原生 `window.prompt` 收 note(prompt 本身键盘可用)→ 输入 → 确定 → 批注条目出现在主区批注流、`#pending-count` 增加。
    9. 同上走一遍 `#btn-plain-ask`(固定 question 直接 POST plain)。
    **§K-2.5 的两条是「必须实测,不得写成『预期成立』」的项**:①焦点入菜单后用户能否看见自己选了什么(高亮是否仍可见)—— 若为「否」,**键盘用户是「盲批注」,直接伤 A11Y-03 的 SC1 ⇒ 必须当场上报,不得静默登记**;②Escape 交还焦点后能否接着 Shift+→ 继续扩选(选区锚点是否保留)—— 若为「否」,**登记为已知局限**(不新增机制)。

    **`window.prompt` 的定位:** 它是本路径上的**已知非设计物**(v2 `FLOW-V2-01` 才替换),本阶段**不动**;但它是键盘可用的,故第 8 步成立。**不得因它「丑」而顺手替换。**

    **不要做的事:** 不给 `handleSelectionTrigger` 加按键白名单(一字不改);不改两个菜单项 handler 的既有语义(请求 / 渲染行为);不改 `#selection-menu` 的 DOM 位置或定位数学(硬规则 5 / Pitfall 8);不给 `#selection-menu` 加 `tabindex="-1"`(焦点落在首按钮即可;加它会引入一个「可被程序聚焦但永远不在 Tab 序里」的元素,且会被 item 10 的普查**排除**);不新增任何 `:focus` 规则(硬规则 10);不新增用户可见字符串(D-19:键盘划词路径今天唯一的视觉信号就是焦点环,**不加任何可发现性提示** —— 这是一个**已登记的已知局限**,不是待补的文案缺口)。
  </action>
  <verify>
    <automated>cd frontend && node --check app.js</automated>
    <fails_when>任何非空输出或非零退出(语法错误)</fails_when>
    <automated>grep -c 'hideSelectionMenu' frontend/app.js</automated>
    <fails_when>输出不是恰好 `7`(`grep -c` 数**行**;**HEAD 实测 7**,逐行是 L1296 的定义行、L1331/L1335 的两条守卫、L1356/L1358 的两个关闭器、L1363/L1393 的两个菜单项调用点 —— 交还是写在函数**体内**,不新增调用点,故该计数**必须仍为 7**;变了说明交还被散落到了调用点,违反 D-08 的单点要求)</fails_when>
    <automated>grep -c 'window.getSelection' frontend/app.js</automated>
    <fails_when>输出不是恰好 `2`(**HEAD 实测 1**(L1329 的既有读取);本任务新增的 Shift 监听器按 `<action>` 复用 `window.getSelection()` 的判据形态 ⇒ +1,改动后恰为 **2**)。输出 `1` 说明新监听器没有按 `<action>` 指定的形态读选区状态(或误删了既有读取);输出 >2 说明多写了读取,或把交还判据写成了清空选区的写法(D-08 禁清空)</fails_when>
    <automated>grep -c 'role=' frontend/index.html</automated>
    <fails_when>输出不是恰好 `0`(本任务不该给 `#selection-menu` 加任何 ARIA;两个弹窗的 `role` 是计划 02 的事)</fails_when>
    <human-check>
      <test>按 UI-SPEC §K-2.6 的九步脚本逐项执行:进 p3 → Tab 到文档区(记位置)→ 按住 Shift 连按 → 扩选(看环是否不跳走)→ 松开 Shift(看菜单与焦点,并看扩选高亮是否仍可见)→ Tab / Shift+Tab 在两项间移动 → Escape(看焦点是否回到 #round-doc)→ 再按住 Shift+→(看能否续选)→ Enter 激活 #btn-annotate 走完一次真实批注 → 同法走一遍 #btn-plain-ask</test>
      <expected>第 3 步焦点环全程不跳走;第 4 步菜单出现且焦点在 #btn-annotate;第 5 步 Tab 序在两项之间往返;第 6 步菜单消失且焦点回到 #round-doc(环重新画出);第 8/9 步批注条目真的出现在批注流且 #pending-count 增加。§K-2.5 ①(扩选高亮是否仍可见)若为「否」⇒ 当场上报,不得静默登记;§K-2.5 ②(能否续选)若为「否」⇒ 登记为已知局限</expected>
      <why_human>本环境**无法自动化键盘文本选区**(连 `contenteditable` 都选不中)⇒ A11Y-08 / A11Y-03 的键盘半场 / REG-03 第 4 条**必须**是具名人工验收;且**不得因自动测试 FAIL 判定功能缺陷**(ROADMAP Phase 8 §Manual checks)</why_human>
    </human-check>
  </verify>
  <acceptance_criteria>
    - `frontend/app.js` 的 `initSelectionMenu()` 函数体内、L1350 的 `roundDoc.addEventListener('keyup', handleSelectionTrigger);` 之后,存在一个绑定在 `document` 上的 `keyup` 监听器,其三条合取判据逐字为 `e.key === 'Shift'` ∧ 菜单未隐藏 ∧ 选区存在且非折叠,成立时调用 `annotateBtn.focus()`。
    - `handleSelectionTrigger` 的函数体逐字节未改(改动只出现新增行,该函数体内不出现任何删除行);`app.js:1321-1322` 的 t8g 注释原文仍在且未被改写。
    - `hideSelectionMenu()` 体内:交还判据在 `classList.add('hidden')` **之前**取值,取值形态为 `selectionMenu.contains(document.activeElement)`;命中时调用 `roundDoc.focus()`;函数体内**没有**清空 `window.getSelection()` 的语句。
    - Shift 监听器的围栏注释写明四件事:手势语义、「为什么不能写在 `handleSelectionTrigger` 里(会让键盘用户只能选中一个字符,而验收项仍会通过)」、「白名单只在这里合法而 `handleSelectionTrigger` 一字不改」、以及自造惯例的已登记代价。
    - `hideSelectionMenu()` 的注释写明它覆盖 F1-a / F1-b / F1-c 三个落点,并写明「写在这一个函数里是因为四个调用点散落必然漏」。
    - 九步人工脚本的每一步观察结果(含每步的焦点位置)被逐项记录;§K-2.5 的两条待测项有明确的「是 / 否」结论与相应的处置(①为否 ⇒ 已上报;②为否 ⇒ 已登记为已知局限)。
    - `frontend/index.html` 未改(`role=` 仍为 0,`#selection-menu` 仍在 `frontend/index.html:207` 且仍是 `<body>` 直接子元素);`frontend/style.css` 未改。
  </acceptance_criteria>
  <done>键盘用户能按住 Shift 用方向键扩选一段文字(焦点全程不移动),松开 Shift 时菜单弹出且焦点落在 `#btn-annotate`;Escape 关菜单后焦点回到 `#round-doc`;两个菜单项执行后焦点也回到 `#round-doc`;`handleSelectionTrigger` 与 t9g 的既有注释一字未改;九步人工脚本的观察结果与 §K-2.5 两条待测项的结论已逐项记录;`node --check app.js` 通过。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 服务端 / AI 产出的 markdown → DOM | 轮次文档与批注内容经 marked 渲染 + `stripUnsafeNodes` 过滤后进入页面;本阶段不改这条链路 |
| 服务端错误消息 → 内联错误节点 | `showInlineError` 是唯一写错误文案的地方,其 `textContent`-only 规则是 XSS 缓解(T-260916-01),**不是风格选择**(硬规则 5) |
| 浏览器选区 API → 焦点管理 | 新增的 Shift 监听器读 `window.getSelection()` 的状态(是否折叠),并调用 `.focus()` |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi08-01 | Tampering | `initSelectionMenu()` 内新增的 Shift keyup 监听器 | low | mitigate | 该监听器只读 `window.getSelection()` 的 `isCollapsed` 状态并调用 `annotateBtn.focus()`,**不向 DOM 写入任何文本**、不拼接字符串、不构造选择器。选区文本的消费仍只在既有的两个菜单项 handler 里(经 `computeBefore` / `quote`,走既有 POST 路径),本阶段零改动 |
| T-idi08-02 | Tampering | `hideSelectionMenu()` 新增的焦点交还 | low | mitigate | 新增的只有 `selectionMenu.contains(document.activeElement)` 的布尔判据与 `roundDoc.focus()`;不写文本、不读选区内容。`showInlineError` 的 `textContent`-only 规则不在本任务的改动面内(硬规则 5) |
| T-idi08-03 | Elevation of Privilege | `#round-doc` 获得 `tabindex="0"` | low | accept | 元素本身是一个渲染容器(既有 markdown 输出面),不含新的输入 sink;新增的能力只有「可被 Tab 聚焦」与「鼠标点击可聚焦」(D-09)。渲染面的既有 XSS 防线(`stripUnsafeNodes` 的 `on*` 属性与 `javascript:` 链接剥离)不受影响 |
| T-idi08-04 | Denial of Service | 焦点环的可辨性判定 | low | mitigate | 若环不可辨且被静默接受,产物是「名义上可聚焦、实际看不出焦点在哪」—— Pitfall 6 的失效形态。Task 2 把它落成具名人工步骤 + D-02 的强制升级分支,不允许静默降级 |
| T-idi08-SC | Tampering | npm / pip / cargo 安装 | high | mitigate | **本阶段零新增运行时依赖、零构建步骤**(硬规则 6 / DESIGN.md D-06)。`frontend/vendor/` 之后必须仍**恰好一个文件**(`marked.min.js`);`check-01` / `check-02` 必须保持零依赖。任何需要安装的写法都是计划偏差与**停止条件** |
</threat_model>

<verification>
**本计划的整体验收:**

```bash
cd frontend && node --check app.js                          # OK
grep -c 'tabindex' frontend/index.html                      # == 1
grep -c 'tabindex' frontend/app.js                          # == 0
grep -v '^#' frontend/style.css | grep -c ':focus-visible'  # == 9(零 CSS 改动)
bash scripts/check-01-token-conformance.sh                  # PASS
.venv/bin/python scripts/check-02-contrast.py | tail -1      # PASS: 0 failures
bash scripts/check-03-hidden-uniqueness.sh                  # PASS(^\.hidden { == 1)
bash scripts/check-04-important-count.sh                    # PASS(!important 声明数 == 1)
.venv/bin/python scripts/check-05-ui-uat.py --item 10        # 三样本 PASS,#round-doc 入册
.venv/bin/python scripts/probe-07-focus-composite.py        # D-04 复跑,记录 0 / 1 两条计数
git status --porcelain -- frontend/style.css scripts/check-05-ui-uat.py   # 空
ls frontend/vendor/                                          # 恰好 marked.min.js 一个文件
```

**本计划会打破的既有断言(显式登记,不是回归):** `check-05 --item 10` 的判定集在 p3 / checking / archive 三个样本里 +1(`#round-doc` 入册)—— D-03 的预期变化;`_idi07_tab_drive` 的上限随之 +1 而 Tab 序也 +1,两者相抵,**无需改门**。
</verification>

<success_criteria>
- `#round-doc` 是一个真实的键盘 Tab 停靠点,整盒焦点环零 CSS 自动生效(Phase 7 的 `[tabindex]:focus-visible` 枚举是唯一来源)。
- 键盘用户能真实完成一次划词批注:按住 Shift 扩选(焦点不移动)→ 松开 Shift(菜单出现、焦点入菜单)→ Escape(焦点交还文档区)→ Enter(真实建出一条批注)。
- `#draft-content` 保持无 Tab 停靠点,且该不对称的理由被写进代码注释与 SUMMARY。
- 环的可辨性被实测并逐条记录;D-02 的分支有明确结论(可辨 ⇒ 零指纹债务;不可辨 ⇒ 已停下上报,未静默降级)。
- `probe-07-focus-composite.py` 复跑通过,两条自证计数(0 / 1)逐字记录。
- `frontend/style.css`、`scripts/check-05-ui-uat.py`、`frontend/vendor/` 逐字节未改。
</success_criteria>

<output>
Create `.planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-01-SUMMARY.md` when done
</output>

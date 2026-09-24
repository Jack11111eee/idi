---
phase: idi-08-accessibility-semantics-and-keyboard
plan: 02
type: execute
wave: 2
depends_on: [idi-08-01]
files_modified:
  - frontend/index.html
  - frontend/app.js
autonomous: true
requirements: [A11Y-05, A11Y-06]
estimate:
  tokens: 52000
  raw_tokens: 52000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # —— 用户视角的可观察行为 ——
    - "两个阻塞弹窗(#confirmation-modal / #tier-modal)在打开时向辅助技术宣告为模态对话框:role=dialog、aria-modal=true,且无障碍名称来自弹窗内既有的 <h3>(aria-labelledby 指向新增的 confirmation-modal-title / tier-modal-title)"
    - "宣告与实现一致:弹窗打开时背景 #app 带原生 inert 属性,两个弹窗都关闭后该属性被移除 —— 背景在键盘与指针两个层面都惰性"
    - "Escape 关闭 #confirmation-modal,且不产生任何决定(不代替「拒绝」、不新增写批注的路径)"
    - "Escape 关闭 #tier-modal 并把 tierModalShown 复位为 false(允许下一个自检事件重弹);不复位 selfcheck.tier,不发任何请求"
    - "#tier-modal 打开时焦点落在 #btn-tier-loose(此前焦点不在弹窗内);顺序是 remove('hidden') → syncBackgroundInert() → .focus()"
    - "弹窗关闭后焦点交还触发者:#confirmation-modal → #btn-authorize;#tier-modal → #btn-continue-check(F1-d)。成功路径不交还(F1 不覆盖情形①)"
    - "其余三个弹窗(#permission-modal / #mission-complete-modal / #cli-check-overlay)刻意不响应 Escape —— 这是范围锁(D-11),不是漏项"
    - "Escape 分派按显式优先级表:划词菜单 → #confirmation-modal → #tier-modal;行为与源码顺序无关"
    - "背景惰性属性的加/去由单点派生函数从两个弹窗的 .hidden 现状推导,不成对记账 —— 任何早退路径上都不会失配,且天然幂等"
    # —— UI-SPEC §UI Considerations 提升(E3 #confirmation-modal / E4 #tier-modal / E5 #app / E6 其余三弹窗)——
    - "E3 empty(explicit):#confirm-word-input 为空时 #btn-confirm-authorize.disabled === true(G3 前提条件的唯一视觉信号),且本阶段新增的 focus-on-open 与背景惰性不改变该态"
    - "E3 error(explicit):输入非「确认授权」时 #confirm-error 可见且 #btn-confirm-authorize 仍为 disabled;错误文案仍只经 textContent 写入(无 innerHTML 渲染)"
    - statement: "E3 loading(backstop):What is shown while data or content is still loading (skeleton, spinner, progressive reveal)?"
      verification: backstop
    - statement: "E3 partial(backstop):What is shown for partial or incomplete data — some fields or rows present, others missing?"
      verification: backstop
    - statement: "E3 long-text(backstop):What happens with unusually long text — truncation, wrapping, ellipsis, or reflow?"
      verification: backstop
    - statement: "E4 empty(backstop):What is shown when there is no data — zero items, an unfilled form, or absent media?"
      verification: backstop
    - statement: "E4 loading(backstop):What is shown while data or content is still loading (skeleton, spinner, progressive reveal)?"
      verification: backstop
    - statement: "E4 error(backstop):What is shown when the load or submit fails (message, retry affordance, partial fallback)?"
      verification: backstop
    - statement: "E4 partial(backstop):What is shown for partial or incomplete data — some fields or rows present, others missing?"
      verification: backstop
    - statement: "E4 long-text(backstop):What happens with unusually long text — truncation, wrapping, ellipsis, or reflow?"
      verification: backstop
    - statement: "E5 overflow(backstop):What happens when content exceeds its container — scroll, clip, wrap, or truncate?"
      verification: backstop
    - statement: "E5 long-text(backstop):What happens with unusually long text — truncation, wrapping, ellipsis, or reflow?"
      verification: backstop
    - statement: "E6 empty(backstop,其余三个弹窗):What is shown when there is no data — zero items, an unfilled form, or absent media?"
      verification: backstop
    - statement: "E6 loading(backstop,其余三个弹窗):What is shown while data or content is still loading (skeleton, spinner, progressive reveal)?"
      verification: backstop
    - statement: "E6 error(backstop,其余三个弹窗):What is shown when the load or submit fails (message, retry affordance, partial fallback)?"
      verification: backstop
    - statement: "E6 partial(backstop,其余三个弹窗):What is shown for partial or incomplete data — some fields or rows present, others missing?"
      verification: backstop
    - statement: "E6 overflow(backstop,其余三个弹窗):What happens when content exceeds its container — scroll, clip, wrap, or truncate?"
      verification: backstop
    - statement: "E6 long-text(backstop,其余三个弹窗):What happens with unusually long text — truncation, wrapping, ellipsis, or reflow?"
      verification: backstop
  artifacts:
    - path: "frontend/index.html"
      provides: "两个新 id(confirmation-modal-title / tier-modal-title)+ 两个 .overlay 上的 role/aria-modal/aria-labelledby;id 总数 80 → 82,零改名、零删除"
      contains: 'aria-labelledby="tier-modal-title"'
    - path: "frontend/app.js"
      provides: "appEl 顶层句柄 + syncBackgroundInert() 单点派生函数 + 5 个调用点 + #tier-modal 打开时移焦 + Escape 单点分派监听器 + tierModalShown 复位 + F1-d 两条焦点交还"
      contains: "syncBackgroundInert"
  key_links:
    - from: "frontend/app.js (syncBackgroundInert)"
      to: "frontend/index.html:10-155 (#app)"
      via: "从两个弹窗的 .hidden 现状派生一个属性 —— 打开则 setAttribute,都关闭则 removeAttribute;幂等、不成对记账"
      pattern: "appEl\\.(set|remove)Attribute\\('inert'"
    - from: "frontend/index.html:170 (#confirmation-modal)"
      to: "frontend/index.html:172 (#confirmation-modal-title)"
      via: "aria-labelledby —— 无障碍名称与屏幕上的标题是同一处真相(名必须说实话)"
      pattern: "aria-labelledby=\"confirmation-modal-title\""
    - from: "frontend/app.js (Escape 单点分派监听器)"
      to: "hideSelectionMenu() / closeConfirmModal() / #tier-modal 的关闭分支"
      via: "显式优先级表(菜单 → 确认 → 档位),读三者的 .hidden 现状决定响应对象"
      pattern: "e\\.key !== 'Escape'"
    - from: "frontend/app.js (Escape 的 tier 分支)"
      to: "frontend/app.js:638-641 的 tierModalShown 置真处"
      via: "复位 tierModalShown = false,使下一个自检事件(refreshChecksAfterStream)能重新弹出 —— 消掉「档位未定且入口消失」的死状态"
      pattern: "tierModalShown = false"
  prohibitions:
    - statement: "Escape 在 #confirmation-modal 上不得产生任何决定(不得代替「拒绝」)—— 那会走 rejectAuthorization() 把用户直接推进一个原生 window.prompt,而替换 window.prompt 是 v2 FLOW-V2-01,本阶段不动;也不得新增一条「拒绝但不弹 prompt」的写批注路径,那要引入第二处真相来源"
      status: unresolved
    - statement: "不得只加 role/aria-modal 而不让宣告成真 —— 焦点陷阱是已裁定 Out of Scope,若不加背景惰性属性,产物就是「宣告了一个实现并不兑现的契约」,比不加 role 更糟(ROADMAP 自己点名的形态)"
      status: unresolved
    - statement: "背景惰性属性不得挂到任何「当前打开的弹窗」的祖先上(含 document.body 或任何共享祖先)—— 那会让打开的弹窗自身变惰性、键盘与指针双路锁死;它只挂 #app,而 #app 在 index.html:155 闭合,五个 .overlay 与 #selection-menu 都是它的兄弟"
      status: unresolved
    - statement: "不得把 aria-live 加在任何流式容器上 —— appendSayToChat 每个 SSE 事件追加一个 DOM 节点(Pitfall M7);本阶段不加任何 aria-live"
      status: unresolved
  assumptions:
    - statement: "edge-probe 对 A11Y-05 返回 unclassified ⇒ 按具名假设登记,不静默丢弃。实际边界条件已由 08-CONTEXT.md 的 D-11 / D-12 / D-13 与 idi-08-UI-SPEC.md §M-2.1 / §M-2.2 / §M-2.3 穷举(对象集按实测重排为 confirmation + tier;Escape 仅关闭、零决定;tier 的死状态与标志复位;其余三个弹窗刻意不响应),规划期不另造判据"
      status: flagged
    - statement: "edge-probe 对 A11Y-06 返回 unclassified ⇒ 按具名假设登记,不静默丢弃。实际边界条件已由 08-CONTEXT.md 的 D-14 / D-15 / D-16 与 idi-08-UI-SPEC.md §M-1.2 / §M-1.3 / §M-1.4 / §M-1.5 穷举(role 落 .overlay 而非 .overlay-card;inert 的挂载边界与派生式;aria-labelledby 而非 aria-label;tier 的移焦目标与顺序),规划期不另造判据"
      status: flagged
---

<objective>
让两个阻塞弹窗的语义宣告**成真**,并让它们支持 Escape 关闭(A11Y-05 + A11Y-06)。

本计划交付三件事:①`frontend/index.html` 的两个弹窗拿到 `role="dialog"` + `aria-modal="true"` + `aria-labelledby`(指向两个 `<h3>` 的**新** id,使无障碍名称与屏幕上的标题是同一处真相);②`frontend/app.js` 新增 `appEl` 句柄与 `syncBackgroundInert()` 单点派生函数(从两个弹窗的 `.hidden` 现状**派生**一个原生 `inert` 属性,挂在 `#app` 上),补 `#tier-modal` 打开时的移焦,并新增一个 Escape **单点分派**监听器(优先级:划词菜单 → 确认弹窗 → 档位弹窗),含 `tierModalShown` 复位与 F1-d 的两条焦点交还;③把弹窗路径的人工验收与 D-16 的「`inert` 生效瞬间焦点落在哪里」实测落成记录。

Purpose: `aria-modal="true"` 的语义是「弹窗之外的背景对辅助技术是惰性的」,而**焦点陷阱是已裁定 Out of Scope** ⇒ 只加两个属性就是**宣告一个实现并不兑现的契约**,与 ROADMAP 自己警告 `role="dialog"` 时点名的形态完全一致。原生 `inert` 是零依赖、零构建的解法(满足硬规则 6),顺带拿到焦点陷阱的**主要**效果(背景不可聚焦、不可点)。**用户裁定原话:「加 inert,让宣告成真」。** 另一条关键事实:按实测重排后的对象集**偏离 ROADMAP 点名的名单** —— 路线图点名 `#confirmation-modal` + `#permission-modal`,而 `#confirmation-modal` 恰是**唯一已经移焦**的那个(`app.js:488` 是全文件唯一的 `.focus()` 调用 ⇒ 不卡);真正卡死的是 **`#tier-modal`**(**没有取消按钮** ∧ 打开时不移焦)。
Output: `frontend/index.html` 的 2 个新 id 与两组 ARIA 属性;`frontend/app.js` 的 `appEl` / `syncBackgroundInert()` / 5 个调用点 / tier 移焦 / Escape 单点分派器 / 标志复位 / 两条 F1-d 交还;以及 Task 3 记录的弹窗人工验收与 D-16 实测结果。
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
@.planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-01-PLAN.md
@.planning/research/PITFALLS.md
</context>

<decision_register>
**D-11 对象集 = `#confirmation-modal` + `#tier-modal`(偏离 ROADMAP 点名的名单,用户已签核)。** 判据是「键盘用户今天真的会卡住」:`#confirmation-modal` 打开时**已经**移焦(`app.js:488`)且有「拒绝」按钮 ⇒ 不卡;`#permission-modal` 弹了键盘用户不知道(不移焦)但可 Tab 出去 ⇒ 不卡;`#tier-modal` **没有取消按钮** ∧ 打开时不移焦 ⇒ **真正的卡死**。范围锁死为这两个;其余三个弹窗的 `role` / `aria-modal` 归 v2 `A11Y-V2-02`。

**D-12 `#confirmation-modal` 的 Escape = 仅关闭(`closeConfirmModal()`),不产生任何决定。** 理由:最小、零副作用;键盘用户本来就能 Tab 到「拒绝」(`openConfirmModal()` 已 `confirmWordInput.focus()`,Tab 跳过 disabled 的「放行」直达「拒绝」)。**不选「Escape = 拒绝」** 的理由:那会走 `rejectAuthorization()`,把用户**直接推进一个原生 `window.prompt`**,而替换 `window.prompt` 是 v2 `FLOW-V2-01`。**不选「Escape = 拒绝但不弹 prompt」** 的理由:那要新增一条写批注的路径,与「不引入第二处真相来源」的立场相冲。

**D-13 `#tier-modal` 的 Escape = 关闭 + 复位 `tierModalShown = false`(允许重弹)。** 已核实的死状态:该弹窗在 `sessionData.state === 'phase5_awaiting_tier'` 且未选档时弹出,**打开时立刻把 `tierModalShown = true`**(`app.js:638-640`);只有选档成功才 `classList.add('hidden')`(`app.js:799`)。**若被关掉而没选,`selfcheck.tier` 仍为空而 `tierModalShown` 已是 true ⇒ 它不会再弹** —— 用户落进「档位未定且入口消失」。复位该标志使下一个自检事件(`refreshChecksAfterStream`)能重新弹出。**已登记的代价:** 复位后弹窗可能在用户做别的事时重现 —— 但这正是「档位未定就该继续问」的正确行为。**不复位 `selfcheck.tier`;不发任何请求。**

**D-14 `role="dialog"` + `aria-modal="true"` + 原生 `inert`,让宣告成真。** 在打开/关闭两个弹窗时给 `#app` 加/去原生 `inert`。**已核实 `#app` 的边界**:`frontend/index.html` 的 `#app` 在 **L10 起、L155 闭合**,五个 `.overlay`(L158 / L170 / L184 / L196 / L213)与 `#selection-menu`(L207)都是它的**兄弟** ⇒ 挂 `#app` 天然只作用于背景、不会波及弹窗自身。**`#selection-menu` 也在 `#app` 之外 ⇒ 弹窗打开时它不会被惰性化。两者同时可见的场景不存在,判据是结构性的**:菜单只在 `currentState === 'phase3'` 时显示(`app.js:1327` 的第一条实质守卫),而 `#tier-modal` 只在 `phase5_awaiting_tier` 弹出 —— 状态互斥。**规划期已确认这一点并登记(不是「理论上互斥」)。**

**D-14 的实现形态 = 单点派生,不成对记账。** 从两个弹窗的 `.hidden` 现状**派生**,不靠 open/close 成对记账 —— 成对记账会在任何一条早退路径上漏去属性(与 STATE.md 反复出现的派生计数缺陷同型),派生式在结构上不可能失配,且天然幂等。**5 个调用点**(全部在既有函数体内,**不新增函数**):`openConfirmModal()`(`remove('hidden')` 之后)、`closeConfirmModal()`(`add('hidden')` 之后)、`#tier-modal` 的打开分支(`app.js:640` 之后)、`chooseTier()` 成功路径(`app.js:799` 之后)、Escape 分派的 tier 分支。**`appEl` 是新增的顶层句柄**(加在 `app.js:83` 之后)—— **新增是安全的,改名或删除既有句柄才是 G-idi01-8 的失效形态**(硬规则 5)。

**D-15 `aria-labelledby` 指向弹窗内的 `<h3>`,需给这两个 `<h3>` 各加一个**新** id。** 文案只存一处(随 `<h3>` 走,不会漂移)。**硬规则 5 禁的是改名/删除既有 id;新增 id 安全。** 已核实 `#confirmation-modal` 的 `<h3>` 是「授权确认」(`index.html:172`)、`#tier-modal` 的是「选择自检档位」(`index.html:186`)。**不选 `aria-label` 写字面串** 的理由:文案会变成第二处真相来源,与「名必须说实话」的纪律相冲。

**D-16 两个弹窗打开时都要移焦。** `#confirmation-modal` 已有(`app.js:488`);**`#tier-modal` 缺,须补**。**顺序锁定:`classList.remove('hidden')` → `syncBackgroundInert()` → `.focus()`。** 移焦目标是 `#btn-tier-loose`(首个可操作控件,与 `openConfirmModal()` 的既有形态对称;不选弹窗容器是因为那需要给它 `tabindex="-1"`,会被 item 10 的普查排除,又是一个需要解释的例外)。**规划期须实测 `inert` 生效瞬间焦点落在哪里**,并据此确认是否需要显式 `.focus()`(这是 D-16 明文要求的实测项,**不得写成「预期成立」**)。

**D-17 `#permission-modal` 的「弹了键盘用户不知道」登记为已知缺口,归 v2 `A11Y-V2-02`,本阶段不修。** 登记位置:`08-UAT.md` 或 VERIFICATION 的 manual/advisory 节。

**A-8(F1-d,用户 2026-09-23 裁定采纳):** 弹窗关闭后焦点**交还触发者** —— `#confirmation-modal` 关闭后 → `#btn-authorize`;`#tier-modal` 关闭后 → `#btn-continue-check`。**两个返回目标已由 checker 独立核实存在**:`#btn-authorize` 在 `index.html:143`、`#btn-continue-check` 在 `index.html:49`。**成功路径不交还**(F1 不覆盖情形①):`#confirmation-modal` 的「放行」成功后整个视图即将切换(`refreshRoundsAfterStream()`),把焦点钉回 `#btn-authorize` 是错的 ⇒ **交还只写在 Escape 分支里,不写进 `closeConfirmModal()`**。**目标不可聚焦时静默降级**(Chrome 下 `.focus()` 对禁用按钮是 no-op),**不新增兜底逻辑**。

**硬规则 8:** `frontend/index.html` / `frontend/app.js` 的每一次编辑都必须先确认「没有改名、没有删除既有 id」。`frontend/index.html` 今天恰好 **80 个 id**,本计划把它带到 **82**。**硬规则 12:** `inert` 与 `.hidden` 是两个**正交机制**,不得互相替代;`inert` 只挂 `#app`,不加在弹窗或 `#selection-menu` 上。
</decision_register>

<flagged_assumptions>
边缘覆盖探针对 A11Y-05 / A11Y-06 均返回 `unclassified`(探针的分类词表是**英文**的,读不了中文需求文本)。**不得把 `unclassified` 当作「无边缘情况」,也不得自动 resolve。** 本计划登记两条:

- **A11Y-05** — 假设:Escape 的边缘条件**已由上游决策穷举** —— 响应对象只有三个(划词菜单 / `#confirmation-modal` / `#tier-modal`),其余三个弹窗**刻意不响应**(D-11 的范围锁);Escape 的语义逐分支固定(菜单 ⇒ 关闭 + 交还;确认 ⇒ **仅关闭、零决定**;档位 ⇒ 关闭 + 标志复位、**不复位 `selfcheck.tier`、不发请求**);三者的 `.hidden` 现状今天互斥,但**优先级表使行为与「谁先打开」无关**,源码顺序不参与判定。**不在范围内**:焦点陷阱、其余三个弹窗的 Escape、`window.prompt` 的替换(v2 `FLOW-V2-01`)。
- **A11Y-06** — 假设:语义的边缘条件**已由上游决策穷举** —— `role` 落 `.overlay` 而非 `.overlay-card`(被切换的节点与被告白的节点是同一个 ⇒「宣告与实现一致」结构性可查;`.overlay-card` 没有 id 且五个弹窗共用同一个类名);无障碍名称**不新写字符串**而是 `aria-labelledby` 指向既有 `<h3>`;背景惰性的挂载点是 `#app` 且**只**挂 `#app`。**不在范围内**:`aria-describedby` 接线、其余三个弹窗的 `role` / `aria-modal`、完整 ARIA / 屏幕阅读器合规(REQUIREMENTS §Out of Scope 表,用户已裁定取窄切片)。
</flagged_assumptions>

<artifacts_this_phase_produces>
本阶段(三个计划合计)新建的符号与路径 —— 每个计划重复列出同一份清单,便于逐计划对照:

**新的 DOM id(2 个,全部在 `frontend/index.html`;硬规则 5 禁的是改名与删除,新增是安全的):**
- `confirmation-modal-title`(本计划;`#confirmation-modal` 的 `<h3>`)
- `tier-modal-title`(本计划;`#tier-modal` 的 `<h3>`)

**新的 HTML 属性:**
- `#round-doc` 的 `tabindex="0"`(计划 01,`frontend/index.html:139`)
- `#confirmation-modal` / `#tier-modal` 的 `role="dialog"` + `aria-modal="true"` + `aria-labelledby`(本计划)

**新的 JS 顶层句柄(1 个,`frontend/app.js`):**
- `appEl`(`document.getElementById('app')`,加在 `app.js:83` 之后;本计划)

**新的 JS 函数(1 个):**
- `syncBackgroundInert()`(本计划;从两个弹窗的 `.hidden` 现状**派生**,不成对记账)

**新的 JS 事件监听器(2 个,均为匿名箭头函数,不引入具名 handler):**
- Shift 提交监听器(计划 01;`document` 上的 `keyup`,写在 `initSelectionMenu()` 内 ⇒ 继承该函数的一次性绑定守卫)
- Escape 单点分派监听器(本计划;顶层 `document` 上的 `keydown`,一次性绑定)

**新的 JS 代码(无新符号):**
- `hideSelectionMenu()` 体内的 F1-a/b/c 焦点交还(计划 01)
- `#tier-modal` 打开分支的移焦 + `tierModalShown` 复位(本计划)
- `syncBackgroundInert()` 的 5 个调用点(本计划;全部在既有函数体内)
- `app.js:1121` 空态文案的一个词(计划 03)

**新的 CSS:零。** 焦点环由 Phase 7 的 `[tabindex]:focus-visible` 枚举自动命中,本阶段 `frontend/style.css` **逐字节不变**(D-01)。

**新的脚本 / 新文件 / 新依赖:零。** `scripts/check-05-ui-uat.py` 与 `scripts/check-01…04` 零改动(D-21 / A-4);`frontend/vendor/` 仍恰好一个文件(`marked.min.js`);无构建步骤(硬规则 6)。
</artifacts_this_phase_produces>

<tasks>

<task type="auto">
  <name>Task 1:两个弹窗的 dialog 语义与无障碍名称(index.html 的 2 个新 id + 两组属性)</name>
  <files>frontend/index.html</files>
  <read_first>
    - frontend/index.html(L155 `#app` 闭合处与 L156-220 的五个 `.overlay` + `#selection-menu` —— **证明五个 overlay 与菜单都是 `#app` 的兄弟**;L170-181 `#confirmation-modal` 全卡;L184-193 `#tier-modal` 全卡;L196-205 `#mission-complete-modal`;L213-220 `#cli-check-overlay`)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-UI-SPEC.md(§属性级规格表 —— 5 行逐字落点与目标值;§M-1.2 的「role 落 .overlay 而非 .overlay-card」三条裁定理由)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-PATTERNS.md(H-2 的命名惯例与 `index.html` 现有 80 个 id 的计数;H-3 的五个 `.overlay` 逐字形态与结构边界)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/08-CONTEXT.md(D-11 / D-15)
  </read_first>
  <action>
    **第一处:给两个弹窗的 `<h3>` 各加一个新 id。** `frontend/index.html:172` 的 `<h3>授权确认</h3>` 加 `id="confirmation-modal-title"`;`frontend/index.html:186` 的 `<h3>选择自检档位</h3>` 加 `id="tier-modal-title"`。命名判据:与既有 kebab-case 风格一致(`confirm-word-input` / `tier-modal` / `btn-tier-loose`),且规划期已实测**零碰撞**(在 `frontend/index.html` / `frontend/app.js` / `frontend/style.css` 三处 grep 均为 0)。**这是新增而不是改名** —— 硬规则 5 禁的是改名与删除既有 id。`frontend/index.html` 的 id 总数由 **80 → 82**。

    **第二处:两个 `.overlay` 各加三个属性。** `frontend/index.html:170` 的 `<div id="confirmation-modal" class="overlay hidden">` 与 `frontend/index.html:184` 的 `<div id="tier-modal" class="overlay hidden">` 各加 `role="dialog"` + `aria-modal="true"` + `aria-labelledby`(前者指 `confirmation-modal-title`,后者指 `tier-modal-title`)。属性顺序:`id` → `class` → `role` → `aria-modal` → `aria-labelledby`。

    **落点是 `.overlay` 而不是 `.overlay-card`(逐字裁定,不得改):** ①**被切换的节点与被告白的节点是同一个** —— `.overlay` 就是 `classList.toggle('hidden')` 的作用对象,「宣告与实现一致」(SC3)因此是**结构性可查**的,而不是两处需要同步的记账;②`.overlay-card` **没有 id**、五个弹窗共用同一个类名 ⇒ 把 ARIA 挂在一个类共享的内层 `<div>` 上,会让「声明」与「状态」分居两个节点,必然漂移;③`aria-labelledby` 无论挂在哪一层,都解析到卡片内的同一个 `<h3>`。

    **为什么用 `aria-labelledby` 而不是 `aria-label` 写字面串:** 后者会让文案变成**第二处真相来源** —— 与「名必须说实话」的纪律相冲。**不新写任何字符串**:无障碍名称就是屏幕上那个 `<h3>`。

    **其余三个弹窗(`frontend/index.html:158` 的 `#permission-modal`、`:196` 的 `#mission-complete-modal`、`:213` 的 `#cli-check-overlay`)一个属性都不加** —— 范围锁死为 D-11 的两个对象,这是**刻意的,不是漏项**。

    **不要做的事:** 不改任何既有 id(改名或删除会在解析期静默杀死 `app.js:4-75` 的约 70 个句柄之下的全部处理器,G-idi01-8);不动 `.overlay-card` 的类名或结构;不动 `#selection-menu` 的 DOM 位置(硬规则 5:它必须是 `<body>` 直接子元素);不改 `#app` 的开闭边界(硬规则 5 之外的独立理由 —— `inert` 的挂载点依赖「五个 overlay 与菜单都是 `#app` 的兄弟」这条结构事实);不写任何 `aria-live`(Pitfall M7,本阶段一律不加);不改任何文案。

    ⚠ **围栏注释里的属性字面量会打穿本任务的计数门(与 Task 1 的 `#round-doc` 注释同类,规划 01 已为 `tabindex` 立过同一条规矩)。** 本任务的三个计数门是 `grep -c 'role='`(**数行**)、`grep -o 'aria-modal' | wc -l`(**数出现次数**)、`grep -o 'aria-labelledby' | wc -l`(**数出现次数**),期望值都是**恰好 2**(两个弹窗各一处)。**注释散文同样计入这三条判据**:若你在弹窗上方写围栏注释解释「为什么落 `.overlay` 而不是 `.overlay-card`」「为什么只有两个弹窗加」,而注释里**复述了 `role="dialog"` / `aria-modal` / `aria-labelledby` 这些字面量**,计数会变成 3,门会红 —— 而 `fails_when` 会把它误报成「范围越界到了其余三个弹窗」,**把你引向一个不存在的缺陷**(实测会发生的形态:注释写得越清楚,门越红)。**故:注释照写(本项目惯例鼓励写「为什么」),但用措辞指代属性,不要复述字面量** —— 写「dialog 语义三件套」「无障碍名称指向既有标题元素」「role 与 aria-modal 两条宣告」等,不要写出 `属性名=` 的形态。**判据是「index.html 里这三个属性的出现处恰为两个弹窗」,不是「文件里这三个字符串出现两次」。** 若门报 3 而你的改动确实只落在两个弹窗上,**先 `grep -n 'role=' frontend/index.html` 看第三个命中是不是注释行**,是则改注释措辞(不要改门的期望值、不要删注释、更不要去动其余三个弹窗)。
  </action>
  <verify>
    <automated>grep -c 'role=' frontend/index.html</automated>
    <fails_when>输出不是恰好 `2`。**判红时先分辨两种成因,不要直接改门或删注释:** ①`grep -n 'role=' frontend/index.html` 的第三个命中若是**围栏注释行**(散文里复述了 `role="dialog"` 字面量),那是**注释措辞问题** ⇒ 改注释用措辞指代属性,门的期望值**不动**;②第三个命中若落在 `#permission-modal` / `#mission-complete-modal` / `#cli-check-overlay` 上,那才是真的范围越界 ⇒ 摘掉那三个弹窗上的属性。输出 `1` 说明只落了一个弹窗</fails_when>
    <automated>grep -o 'aria-modal' frontend/index.html | wc -l</automated>
    <fails_when>输出不是恰好 `2`(`grep -c` 数**行**、不数出现次数,所以这一条必须用 `-o | wc -l` 写)。**注意本门数的是出现次数 ⇒ 围栏注释里复述一次 `aria-modal` 字面量就会让它变成 3**;判红时同样先看第三个命中是否在注释里(是 ⇒ 改注释措辞),再考虑范围越界</fails_when>
    <automated>grep -o 'aria-labelledby' frontend/index.html | wc -l</automated>
    <fails_when>输出不是恰好 `2`。**与上一条同理:注释里复述一次 `aria-labelledby` 字面量即变 3** ⇒ 判红时先分辨「注释措辞」与「范围越界」两种成因(成因判定同 `role=` 那条)</fails_when>
    <automated>grep -c 'id="confirmation-modal-title"' frontend/index.html; grep -c 'id="tier-modal-title"' frontend/index.html</automated>
    <fails_when>任一条输出不是恰好 `1`</fails_when>
    <automated>grep -o 'id="' frontend/index.html | wc -l</automated>
    <fails_when>输出不是恰好 `82`(80 + 两个新 id;少于 82 说明误删或误改了既有 id —— 硬规则 5 的失效形态)</fails_when>
    <automated>cd frontend && node --check app.js</automated>
    <fails_when>任何非空输出或非零退出(本任务不改 JS,这一步只证明改动没有意外波及 JS 侧)</fails_when>
  </verify>
  <acceptance_criteria>
    - `frontend/index.html` 的 `#confirmation-modal` 与 `#tier-modal` 两个 `.overlay` 各带 `role="dialog"`、`aria-modal="true"`、`aria-labelledby`;其余三个 `.overlay` 一个属性都不加。
    - 两个 `<h3>`(「授权确认」/「选择自检档位」)各带一个新 id:`confirmation-modal-title` / `tier-modal-title`;两个 id 在 `frontend/index.html` 各出现恰好 1 次。
    - `frontend/index.html` 的 id 总数为 82,且原有 80 个 id 全部逐字保留(零改名、零删除)。
    - 无障碍名称通过 `aria-labelledby` 指向既有 `<h3>`,**没有**新增任何字符串常量、**没有**使用 `aria-label`。
    - `#app` 的开闭边界(L10-L155)与 `#selection-menu` 在 `frontend/index.html:207` 的位置均未改动 —— 五个 `.overlay` 与菜单仍是 `#app` 的兄弟。
    - `frontend/index.html` 不出现任何 `aria-live`;`frontend/app.js` 与 `frontend/style.css` 未改。
  </acceptance_criteria>
  <reversibility rating="costly">对象集一旦要从 confirmation + tier 换回 ROADMAP 点名的名单,就要重开 A11Y-05 / A11Y-06 的对象集并重算 UI-SPEC 的覆盖声明;但属性本身是增量的,回退代价落在文档与验收面而非代码。</reversibility>
  <done>两个阻塞弹窗向辅助技术宣告为模态对话框,且无障碍名称来自弹窗内既有的 `<h3>`(不是第二处字符串);其余三个弹窗零改动;`frontend/index.html` 的 id 总数 82 且零改名零删除;`frontend/app.js` / `frontend/style.css` 未改。</done>
</task>

<task type="auto">
  <name>Task 2:背景惰性的单点派生(5 个调用点)+ #tier-modal 打开时移焦 —— 让宣告成真</name>
  <files>frontend/app.js</files>
  <read_first>
    - frontend/app.js(L81-83:顶层句柄分组的末尾形态 —— 新句柄的落点与注释惯例;L483-495:`openConfirmModal` / `closeConfirmModal` 全文,含 L488 的 `confirmWordInput.focus()`(全文件唯一的 `.focus()` 调用);L632-643:`phase5_awaiting_tier` 分支与 `tierModalShown = true`(`app.js:638-640`);L786-800:`chooseTier()` 的成功路径与 `tierModal.classList.add('hidden')`;L94 的 `tierModalShown` 声明)
    - frontend/index.html(L10 / L155:`#app` 的开闭边界 —— 背景惰性挂载点的结构前提)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-UI-SPEC.md(§M-1.3 的边界核实;§M-1.4 的派生式实现形态与 5 个调用点清单;§M-1.5 的移焦与顺序锁定)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-PATTERNS.md(J-1 / J-5 / J-6 / J-7;No Analog Found 表的第一行 —— 该属性在 `index.html` 与 `app.js` 里今天出现次数均为 0,无 in-file 先例)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/08-CONTEXT.md(D-14 / D-16)
  </read_first>
  <action>
    **第一处:新增顶层句柄。** 在 `frontend/app.js:83` 的 `const docPanelHeader = document.getElementById('doc-panel-header');` **之后**加一行 `const appEl = document.getElementById('app');`,带自己的中文注释说明消费者是 D-14 的背景惰性挂载。**这是新增,不是改名** —— `app.js:4-75` 的约 70 个句柄一个都不动(硬规则 5 / G-idi01-8)。

    **第二处:新增 `syncBackgroundInert()` 单点派生函数。** 形态照本文件既有的「一个函数读当前状态、派生出若干呈现效果、由每个变更点调用」的形状(范本是 `app.js:1174-1184` 的 `updateFrozenPresentation(isCurrent)`)。函数体:读两个弹窗的 `.hidden` 现状,若**任一**未隐藏则给 `appEl` 设该属性,否则移除。**从状态派生,不成对记账** —— 注释必须写明理由:成对记账会在任何一条早退路径上漏去属性(与 STATE.md 反复出现的派生计数缺陷同型),派生式在结构上不可能失配,且天然幂等。注释还要写明:该属性是**原生 HTML 属性**,零依赖零构建(硬规则 6);焦点陷阱是 Out of Scope,**这个属性不是陷阱**,它只拿到陷阱的**主要**效果(背景不可聚焦、不可点);以及**硬规则 12** —— 它与 `.hidden` 是**两个正交机制**,不得互相替代(前者管「背景对辅助技术与指针惰性」,后者管显隐)。**属性值用空字符串**(布尔属性的既有挂法),不用 `"true"` 之类的字面量。

    **第三处:5 个调用点(全部插在既有函数体内,不新增函数、不移动既有语句):**
    1. `openConfirmModal()` —— 在 `confirmationModal.classList.remove('hidden');` **之后**、`confirmWordInput.focus();` **之前**(顺序锁定:`remove('hidden')` → `syncBackgroundInert()` → `.focus()`)。
    2. `closeConfirmModal()` —— 在 `confirmationModal.classList.add('hidden');` **之后**。
    3. `#tier-modal` 的打开分支(`app.js:638-641` 的 `if (!selfcheck.tier && !tierModalShown) { … }` 块)—— 在 `tierModal.classList.remove('hidden');` **之后**,并在其后补**打开时移焦**:焦点送入 `#btn-tier-loose`(`tierLooseBtn`,既有句柄)。顺序同样是 `remove('hidden')` → `syncBackgroundInert()` → `.focus()`。
    4. `chooseTier()` 的成功路径 —— 在 `tierModal.classList.add('hidden');` **之后**。
    5. Escape 分派的档位分支(Task 3 落)。
    **注意 3 与 4 都在既有的 if/else 或 try 块内,插入位置必须保持既有的缩进层级与语句先后(硬规则 3:追加,不重排)。**

    **第四处:补 `#tier-modal` 的打开时移焦(D-16)。** 这是 D-11 判定的「卡死」的**实质修复** —— `#tier-modal` 的陷阱**不是「没有 Escape」而是「焦点不在里面」**;背景惰性落地后背景不可聚焦,**焦点若不在弹窗内会掉到 `<body>`**,下一次 Tab 会绕开整个背景、落到弹窗外围,**比不惰性化更糟**。移焦目标选 `#btn-tier-loose`(首个可操作控件)而不是弹窗容器:与 `openConfirmModal()` 的既有形态对称(`confirmWordInput.focus()` 就是「首个可操作控件」),且**不引入任何新属性**(容器作焦点目标需要给它一个程序化聚焦用的负值停靠点,那会被 item 10 的普查排除,又是一个需要解释的例外)。注释写明这条理由。

    **第五处:D-16 明文要求的实测项。** 在浏览器里实测「背景惰性生效的瞬间焦点落在哪里」,并据此确认是否需要保留显式的 `.focus()`。**不得写成「预期成立」。** 记录形态见 Task 3 的验收步骤;本任务先把 `.focus()` 写上,实测结果若显示不需要,则由 Task 3 记录结论(不删 `.focus()` —— 显式移焦是确定性的,而依赖「惰性生效后浏览器自动收拢焦点」是隐式行为)。

    **不要做的事:** 不把该属性挂到 `document.body` 或任何共享祖先上(那会让打开的弹窗自身变惰性,键盘与指针双路锁死 —— 本计划最重的一条禁令);不加在弹窗上;不加在 `#selection-menu` 上(硬规则 12);不写 open/close 成对记账;不改 `openConfirmModal()` 的既有语句顺序;不动 `closeConfirmModal()` 里除新增调用点之外的任何东西(尤其**不把 F1-d 的交还写进它** —— 见 Task 3);不改 `chooseTier()` 的请求/渲染行为;不新增依赖或构建步骤。
  </action>
  <verify>
    <automated>grep -c 'inert' frontend/app.js</automated>
    <fails_when>输出为 `0`(该属性在 `app.js` 里今天出现次数为 0,本任务之后必须为正 —— 覆盖函数定义、属性名与注释)</fails_when>
    <automated>grep -c 'syncBackgroundInert' frontend/app.js</automated>
    <fails_when>输出小于 `6`(1 个定义 + 5 个调用点;少于 6 说明有调用点漏落,而漏落的调用点会让属性在早退路径上失配)</fails_when>
    <automated>grep -c 'appEl' frontend/app.js</automated>
    <fails_when>输出小于 `2`(1 个句柄声明 + 至少 1 处属性写入)</fails_when>
    <automated>grep -c 'tierLooseBtn' frontend/app.js</automated>
    <fails_when>输出小于 `3`(1 个句柄声明 + 1 个既有的 click 绑定 + 1 处新增的移焦;少于 3 说明 tier 的打开时移焦没落)</fails_when>
    <automated>cd frontend && node --check app.js</automated>
    <fails_when>任何非空输出或非零退出(语法错误)</fails_when>
    <automated>grep -c 'id="app"' frontend/index.html</automated>
    <fails_when>输出不是恰好 `1`(背景惰性的挂载点依赖 `#app` 存在且其边界未变;`frontend/index.html` 本任务不改,这一步只证明挂载点仍在)</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 1</automated>
    <fails_when>退出码非 0(0 = 全 PASS;1 = 有 FAIL 断言;2 = 有 BLOCKED 断言),或输出里出现任何 `FAIL` / `BLOCKED` 开头的行。**本任务是全阶段唯一改动两个弹窗 `.hidden` 开闭点的任务**(`openConfirmModal` / `closeConfirmModal` / `#tier-modal` 的打开分支 / `chooseTier()` 成功路径),而 `--item 1` 就是五态显隐(`.hidden` 的层叠证据,六元素 × 五样本)的运行时门 —— 它是本阶段契约 `idi-08-UI-SPEC.md` §契约校验命令 逐字点名「必须仍绿」的门之一,本任务必须实跑它而不是把它留给收口。判红时先读 `scripts/check-05-ui-uat.py` 的 `HIDDEN_MATRIX` / `COMPETITORS` 两段判「真缺陷 vs 普查集变化」,**不得直接改门**(D-21:该文件在 5 份 live 报告的 `covered_files` 里)</fails_when>
    <human-check>
      <test>打开 p3 之外的一个 phase5_awaiting_tier 场景(或直接触发 #tier-modal),观察三件事:①弹窗打开时焦点是否落在 #btn-tier-loose 上(第一下 Tab 是否在弹窗内部移动);②弹窗打开期间按 Tab 是否能进入背景区(应当**不能**);③用鼠标点击背景区(应当**无反应**)</test>
      <expected>①焦点在 #btn-tier-loose 上;②Tab 不进入背景(背景惰性生效);③鼠标点击背景无反应。若 ② 或 ③ 不成立,说明属性没有生效或挂错了节点 —— 停下上报,不要静默登记</expected>
      <why_human>本环境截图不可用(headless 渲染被阻 + 常驻 `/api/events` SSE 流让采集处理器无法终止)⇒ 用计算样式检查 + 具名人工步骤,不得计划视觉 diff;而「背景在键盘与指针两个层面都惰性」是行为观察,不是静态计数</why_human>
    </human-check>
  </verify>
  <acceptance_criteria>
    - `frontend/app.js` 在 L83 之后有 `appEl` 的顶层句柄声明;`app.js:4-75` 的既有句柄一个都没改名或删除。
    - `syncBackgroundInert()` 存在,其判据是两个弹窗的 `.hidden` 现状的**派生**(任一未隐藏 ⇒ 设属性;都隐藏 ⇒ 去属性),不是 open/close 成对记账。
    - 5 个调用点全部落在既有函数体内:`openConfirmModal()`、`closeConfirmModal()`、`#tier-modal` 的打开分支、`chooseTier()` 的成功路径、Escape 分派的档位分支。
    - `openConfirmModal()` 与 `#tier-modal` 打开分支的顺序均为 `classList.remove('hidden')` → `syncBackgroundInert()` → `.focus()`;`#tier-modal` 的移焦目标是 `#btn-tier-loose`。
    - 该属性只挂在 `appEl` 上,没有任何一处挂在 `document.body`、弹窗、或 `#selection-menu` 上。
    - `closeConfirmModal()` 里只有新增的 `syncBackgroundInert()` 调用,没有 F1-d 的焦点交还(交还只写在 Escape 分支里 —— 成功路径不交还)。
    - 注释写明:派生而非成对记账的理由、原生属性零依赖零构建、它**不是**焦点陷阱、以及它与 `.hidden` 是两个正交机制不得互相替代。
    - `frontend/index.html` 与 `frontend/style.css` 本任务未改;`node --check app.js` 通过。
  </acceptance_criteria>
  <reversibility rating="costly">回退要同时去掉该属性的挂载点与 aria-modal,并把 SC3 重述为「可 Esc 关闭 + 移焦」而非「背景惰性」—— 宣告与实现是一对,拆一半即回到「宣告不兑现」的形态。</reversibility>
  <done>两个弹窗打开时背景 `#app` 带原生惰性属性、都关闭后该属性被移除;`#tier-modal` 打开时焦点落在 `#btn-tier-loose`;5 个调用点全部落位且派生式在早退路径上不失配;`node --check app.js` 通过;背景在键盘与指针两个层面都惰性这一行为已由具名人工步骤确认。</done>
</task>

<task type="auto">
  <name>Task 3:Escape 单点分派器 + tierModalShown 复位 + F1-d 两条焦点交还 + 弹窗人工验收与 D-17 登记</name>
  <files>frontend/app.js</files>
  <precondition>应用可在本机启动并能在浏览器里打开,且能进入一个会弹出 #tier-modal 的状态(phase5_awaiting_tier)</precondition>
  <read_first>
    - frontend/app.js(L1342-1423:`initSelectionMenu` 的完整边界(它的收尾大括号在 L1423)—— 分派器的插入点就在它之后、`refreshPendingCount`(L1426)之前;L1352-1358:文档级监听器的守卫优先形态(范本);L807-808:顶层 column-0 绑定的既有惯例;L483-495:`openConfirmModal` / `closeConfirmModal`;L786-800:`chooseTier`;L632-643:tier 的打开分支与 `tierModalShown = true`;L1296-1300:`hideSelectionMenu`(计划 01 已改);L58 / L76:`authorizeBtn` / `continueCheckBtn` 两个既有句柄)
    - frontend/index.html(L143 的 `#btn-authorize`、L49 的 `#btn-continue-check` —— 两个 F1-d 返回目标)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-UI-SPEC.md(§M-2.1 的单点分派器与优先级表;§M-2.2 的逐分支行为契约与「明确不做什么」列;§M-2.3 的死状态;§M-2.4 的已知缺口;§焦点契约的 F1 表与「F1 不覆盖的两种情形」)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-PATTERNS.md(J-3 / J-6 的第五行)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/08-CONTEXT.md(D-08 / D-12 / D-13 / D-17 / A-8)
  </read_first>
  <action>
    **第一处:新增 Escape 单点分派监听器。** 落点是 `initSelectionMenu()` 的收尾大括号(`frontend/app.js:1423`)**之后**、`refreshPendingCount`(L1426)之前,作为一个**新的顶层小节**(column 0,带一条中文注释说明消费者是 A11Y-05)。**绑定在顶层 ⇒ 一次性、与菜单的初始化路径解耦**(不需要一次性绑定守卫)。

    **为什么取「单点 + 优先级表」而不是「各弹窗各自的监听器」(裁定并写明理由):** ①三个响应对象里有一个是菜单(它已经在 `initSelectionMenu` 那一段),分派器与它相邻使「Escape 的完整语义在一个屏幕内可读完」;②分散到各弹窗会把「谁先响应」变成**源码顺序事实**(硬规则 3 的同型风险);③单点可解释、可枚举(本项目「影响面必须可枚举」的既定口径)。

    监听器形态:绑定 `document` 的 `keydown`;首行守卫 `e.key !== 'Escape'` 即 return;然后按**显式优先级表**(按 z 序:`--z-selection-menu` 200 > `--z-overlay` 100)依次探测三个对象的 `.hidden` 现状,命中即处理并 `e.preventDefault()` 后 return:
    1. **划词菜单**:调 `hideSelectionMenu()`(它已含计划 01 落的 F1-a 焦点交还)⇒ `e.preventDefault()` ⇒ return。**不清 `window.getSelection()`** —— 那会毁掉「Escape 关菜单后接着 Shift+→ 继续扩选」这条路径。
    2. **`#confirmation-modal`**:调 `closeConfirmModal()`(**D-12:仅关闭,零决定** —— 不代替「拒绝」、不新增写批注的路径)⇒ `authorizeBtn.focus()`(**F1-d:交还触发者**)⇒ `e.preventDefault()` ⇒ return。**背景惰性的去除已在 `closeConfirmModal()` 内完成,不在这里重复。**
    3. **`#tier-modal`**:`tierModal.classList.add('hidden')` ⇒ **`tierModalShown = false`(D-13:复位,允许重弹)** ⇒ `syncBackgroundInert()` ⇒ `continueCheckBtn.focus()`(**F1-d:交还下一个动作**)⇒ `e.preventDefault()`。**不复位 `selfcheck.tier`;不发任何请求。**
    4. **其余三个弹窗(`#permission-modal` / `#mission-complete-modal` / `#cli-check-overlay`)刻意不响应** —— 注释必须写明这是**范围锁(D-11)**,**刻意的,不是漏项**。

    注释还要写明两条已登记的事实:①三个响应对象今天**互斥**(菜单只在 `currentState === 'phase3'` 显示,`#tier-modal` 只在 `phase5_awaiting_tier` 弹出),但**优先级表使行为与「谁先打开」无关,源码顺序不参与判定**;②`#confirmation-modal` 选「Escape = 仅关闭」的理由(最小、零副作用;键盘用户本来就能 Tab 到「拒绝」,因为 `openConfirmModal()` 已 `confirmWordInput.focus()`,Tab 跳过 disabled 的「放行」直达「拒绝」)。

    **第二处:F1-d 的两条焦点交还(只写在 Escape 分支里)。** `#confirmation-modal` → `authorizeBtn`(`app.js:58` 的既有句柄,目标在 `frontend/index.html:143`);`#tier-modal` → `continueCheckBtn`(`app.js:76` 的既有句柄,目标在 `frontend/index.html:49`)。**成功路径不交还**(F1 不覆盖情形①):`#confirmation-modal` 的「放行」成功后整个视图即将切换(`refreshRoundsAfterStream()`),此时把焦点钉回 `#btn-authorize` 是错的(它下一刻就随 `#authorize-row` 一起隐藏)⇒ **交还只写在 Escape 分支里,绝不写进 `closeConfirmModal()`**。**目标不可聚焦时静默降级**(Chrome 下 `.focus()` 对禁用按钮是 no-op)⇒ **不新增兜底逻辑**,注释登记这是已知边界。

    **第三处:登记 `#permission-modal` 的已知缺口(D-17,不修)。** 在 SUMMARY 里写明:`#permission-modal` 打开时不移焦、无任何宣告 ⇒ 「弹了键盘用户不知道」,归 v2 `A11Y-V2-02`,**本阶段不修**(理由:用户已裁定取 confirmation + tier 两个对象,而该弹窗可 Tab 出去、不构成卡死)。**不得在本阶段顺手修。**

    **第四处:弹窗路径的具名人工验收(逐条记录观察结果与每一步的焦点位置)。**
    1. **确认弹窗的 Escape**:进入 phase3、点亮 `#btn-authorize`、打开 `#confirmation-modal`(焦点应在 `#confirm-word-input`)⇒ 按 Escape ⇒ 弹窗消失,焦点落在 `#btn-authorize`,**且没有产生任何决定**(不出现 `window.prompt`、不新增批注、`#authorize-row` 状态不变)。
    2. **确认弹窗的背景惰性**:弹窗打开期间按 Tab,焦点只在弹窗内部移动,**不进入背景**;关闭后按 Tab 能从 `#btn-authorize` 继续。
    3. **档位弹窗的移焦与 Escape**:进入 `phase5_awaiting_tier` ⇒ 弹窗打开时焦点落在 `#btn-tier-loose` ⇒ 按 Escape ⇒ 弹窗消失,焦点落在 `#btn-continue-check`;**再触发一次自检事件**(如再走一次 `refreshChecksAfterStream` 的路径)⇒ 弹窗**重新弹出**(证明 `tierModalShown` 的复位生效)。
    4. **档位弹窗的背景惰性**:同第 2 条。
    5. **D-16 的实测项**:记录背景惰性生效**那一瞬间**焦点落在哪里(弹窗打开前焦点在 `#btn-continue-check`,打开后是否落在 `#btn-tier-loose`),并据此说明显式 `.focus()` 是否必要 —— **不得写成「预期成立」**。
    6. **F1-d 的两条交还**:分别按 Escape 关闭两个弹窗后,按一次 Tab,确认焦点从触发者处继续(不是从 `<body>` 重新开始)。
    7. **其余三个弹窗不响应 Escape**:分别打开 `#permission-modal` / `#mission-complete-modal` / `#cli-check-overlay` 后按 Escape,确认**无任何变化**(这是范围锁的预期,不是缺陷)。

    **不要做的事:** 不给其余三个弹窗加 Escape 响应(范围锁);不把 `rejectAuthorization()` 接进 Escape 分支;不清 `window.getSelection()`;不加任何 `aria-live`(Pitfall M7);不改 `#selection-menu` 的 DOM 位置或定位数学;不改两个菜单项 handler 的既有语义;不把 F1-d 交还写进 `closeConfirmModal()`。
  </action>
  <verify>
    <automated>grep -c "key !== 'Escape'" frontend/app.js</automated>
    <fails_when>输出不是恰好 `1`(分派器是单点 —— 出现两次说明落了第二个 Escape 监听器,「谁先响应」就变成了源码顺序事实)</fails_when>
    <automated>grep -c 'tierModalShown' frontend/app.js</automated>
    <fails_when>输出不是恰好 `4`。**HEAD 实测 3**,逐行是:L94 的声明 `let tierModalShown = false;`、L638 的**读取**(`if (!selfcheck.tier && !tierModalShown) {`)、L639 的置真 `tierModalShown = true;` —— 注意 **L638 是读不是写**,把它当成「打开分支里的置真」会数错(HEAD 上真实的「写」只有 L639 一处)。本任务在 Escape 分派器的档位分支新增 D-13 的复位一行 ⇒ 改动后恰为 `4`。**输出 `3` 说明复位没落,「档位未定且入口消失」的死状态仍在**(这是本门存在的唯一理由);输出 >4 说明写了第二处复位或落了第二个分支</fails_when>
    <automated>grep -c 'authorizeBtn.focus()' frontend/app.js; grep -c 'continueCheckBtn.focus()' frontend/app.js</automated>
    <fails_when>任一条输出不是恰好 `1`(两条 F1-d 交还各应出现一次;出现两次说明交还被同时写进了 `closeConfirmModal()`,违反「成功路径不交还」)</fails_when>
    <automated>grep -c 'closeConfirmModal()' frontend/app.js</automated>
    <fails_when>输出不是恰好 `4`。**HEAD 实测 3**,逐行是:L491 的函数定义 `function closeConfirmModal() {`、L547 与 L557 两处**既有**调用点。本任务的分派器**复用既有函数**(调一次 `closeConfirmModal()`)⇒ 改动后恰为 `4`。**输出 `3` 说明分派器没有复用 `closeConfirmModal()`、而是自己写了关闭逻辑**(HEAD 的 3 已经满足任何 `>= 3` 的写法,所以本门必须写成绝对等值,否则它在复用与不复用之间恒定通过);输出 >4 说明新增了第二处关闭路径</fails_when>
    <automated>cd frontend && node --check app.js</automated>
    <fails_when>任何非空输出或非零退出(语法错误)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>任一条不是恰好一行 `PASS`(本阶段零 CSS 改动,三条守卫必须逐字不变)</fails_when>
    <automated>git status --porcelain -- frontend/style.css</automated>
    <fails_when>输出非空(硬规则 9:零 frontend/style.css 改动)</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 4</automated>
    <fails_when>退出码非 0(0 = 全 PASS;1 = 有 FAIL;2 = 有 BLOCKED),或输出里出现任何 `FAIL` / `BLOCKED` 开头的行。`--item 4` = SC5 的两条令牌接线 + `#state-badge` z-index 的 computed-style 抽查,是 `idi-08-UI-SPEC.md` §契约校验命令 逐字点名「必须仍绿」的另一条门;本阶段**零 CSS 改动**,它必须逐字保持绿。判红说明改动波及了 CSS 面 ⇒ 先停下判因,**不得改门**(D-21)</fails_when>
    <human-check>
      <test>按 Task 3 的七条具名步骤逐条执行:确认弹窗的 Escape(且零决定)、确认弹窗的背景惰性、档位弹窗的移焦与 Escape 与重弹、档位弹窗的背景惰性、背景惰性生效瞬间的焦点落点、两条 F1-d 交还、其余三个弹窗不响应 Escape</test>
      <expected>第 1 条:Escape 后焦点在 #btn-authorize 且无任何决定(不弹原生 prompt、不新增批注);第 3 条:Escape 后焦点在 #btn-continue-check,且下一个自检事件能让弹窗重弹;第 5 条:如实记录焦点落点(不得写「预期成立」);第 6 条:关闭后按 Tab 从触发者处继续,不是从 &lt;body&gt; 重新开始;第 7 条:三个弹窗按 Escape 无任何变化(范围锁的预期,不是缺陷)</expected>
      <why_human>本环境截图不可用,且「Escape 是否产生了决定」「背景是否真的惰性」「焦点交还到哪个元素」都是行为观察,不是静态计数;`#permission-modal` 的「弹了键盘用户不知道」也只有人眼能确认</why_human>
    </human-check>
  </verify>
  <acceptance_criteria>
    - `frontend/app.js` 在 `initSelectionMenu()` 的收尾大括号之后、`refreshPendingCount` 之前,存在**唯一一个**绑定 `document` 的 `keydown` 监听器,首行守卫为 `e.key !== 'Escape'`。
    - 该监听器按显式优先级表依次响应:划词菜单(`hideSelectionMenu()`)→ `#confirmation-modal`(`closeConfirmModal()` + `authorizeBtn.focus()`)→ `#tier-modal`(`classList.add('hidden')` + `tierModalShown = false` + `syncBackgroundInert()` + `continueCheckBtn.focus()`);每个分支都 `e.preventDefault()`。
    - 其余三个弹窗在分派器里**无分支**,且注释写明这是范围锁(D-11)、刻意而非漏项。
    - `closeConfirmModal()` 里**没有** F1-d 的焦点交还(交还只写在 Escape 分支里);`authorizeBtn.focus()` 与 `continueCheckBtn.focus()` 在文件里各出现恰好一次。
    - 分派器的 tier 分支复位 `tierModalShown`,但**不**复位 `selfcheck.tier`、**不**发任何请求。
    - 分派器不清 `window.getSelection()`;不新增任何 `aria-live`。
    - SUMMARY 里登记了 `#permission-modal` 的已知缺口(D-17,归 v2 `A11Y-V2-02`,本阶段不修)。
    - 七条具名人工步骤的观察结果(含每步的焦点位置)被逐项记录;D-16 的「背景惰性生效瞬间焦点落在哪里」有实测记录,不是「预期成立」。
    - `frontend/style.css` 逐字节未改(`git status --porcelain` 为空);三条不变量守卫仍全绿。
  </acceptance_criteria>
  <done>Escape 能关闭两个阻塞弹窗:确认弹窗仅关闭、零决定,档位弹窗关闭并复位 `tierModalShown`(下一个自检事件能重弹);关闭后焦点分别交还 `#btn-authorize` / `#btn-continue-check`;其余三个弹窗不响应(范围锁);背景在两个弹窗打开期间对键盘与指针都惰性;`#permission-modal` 的已知缺口已登记且未修;七条人工步骤的观察结果与 D-16 的实测记录已逐项落盘。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 弹窗标题文案 → 无障碍名称 | `aria-labelledby` 指向弹窗内既有的 `<h3>`;本阶段**不新写任何字符串**(避免第二处真相来源) |
| 背景惰性属性 → 背景可交互性 | 该属性决定背景在键盘与指针两个层面是否可及;挂错节点会把打开的弹窗自身锁死 |
| Escape 键 → 应用决定 | 分派器决定 Escape 是否触发关闭、以及是否触发任何业务决定(如「拒绝」) |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi08-05 | Denial of Service | `syncBackgroundInert()` 的挂载点 | **high** | mitigate | 属性**只**挂 `appEl`(`#app`,`frontend/index.html:10-155`)。五个 `.overlay` 与 `#selection-menu` 都是 `#app` 的**兄弟** ⇒ 挂 `#app` 天然只作用于背景。**禁止挂 `document.body` 或任何共享祖先** —— 那会让当前打开的弹窗自身变惰性,键盘与指针双路锁死。该禁令已作为 `must_haves.prohibitions` 的一条登记,并在 Task 2 的 `<action>` 里点名 |
| T-idi08-06 | Spoofing | `#confirmation-modal` / `#tier-modal` 的 `aria-modal="true"` | medium | mitigate | 只加属性而无背景惰性就是「宣告一个实现并不兑现的契约」(比不加 `role` 更糟)。`aria-modal` 与 `syncBackgroundInert()` 的挂载**在同一次提交**落地,使宣告与实现在结构上一致(SC3) |
| T-idi08-07 | Tampering | Escape 分派器的确认分支 | medium | mitigate | Escape **只关闭、零决定**(D-12):不调 `rejectAuthorization()`(那会把用户推进原生 `window.prompt`,而替换它是 v2 `FLOW-V2-01`),不新增「拒绝但不弹 prompt」的写批注路径。分派器只调既有的 `closeConfirmModal()` / `hideSelectionMenu()` / 一次 `classList.add` |
| T-idi08-08 | Elevation of Privilege | 新增的 2 个 id 与 `aria-labelledby` | low | accept | 无障碍名称指向既有 `<h3>`,**不新写字符串**、不做字符串拼接、不构造选择器;新增 id 不引入任何输入 sink。渲染面的既有 XSS 防线(`stripUnsafeNodes`)不受影响 |
| T-idi08-09 | Information Disclosure | `#confirm-error` 的错误文案 | low | mitigate | 错误文案仍只经 `textContent` 写入(XSS 缓解 T-260916-01)。本计划零改动该路径;Task 3 的 `check-01/03/04` 复跑守住 `frontend/style.css` 零改动 |
| T-idi08-SC | Tampering | npm / pip / cargo 安装 | high | mitigate | **本阶段零新增运行时依赖、零构建步骤**(硬规则 6)。原生 HTML 属性零依赖;`frontend/vendor/` 之后必须仍**恰好一个文件**(`marked.min.js`)。任何需要安装的写法都是计划偏差与**停止条件** |
</threat_model>

<verification>
**本计划的整体验收:**

```bash
cd frontend && node --check app.js                          # OK
grep -c 'role=' frontend/index.html                         # == 2
grep -o 'aria-modal' frontend/index.html | wc -l            # == 2
grep -o 'aria-labelledby' frontend/index.html | wc -l       # == 2
grep -o 'id="' frontend/index.html | wc -l                  # == 82(80 + 2)
grep -c 'syncBackgroundInert' frontend/app.js               # >= 6(1 定义 + 5 调用点)
grep -c "key !== 'Escape'" frontend/app.js                  # == 1(单点)
grep -c 'authorizeBtn.focus()' frontend/app.js              # == 1
grep -c 'continueCheckBtn.focus()' frontend/app.js          # == 1
bash scripts/check-01-token-conformance.sh                  # PASS
bash scripts/check-03-hidden-uniqueness.sh                  # PASS
bash scripts/check-04-important-count.sh                    # PASS
.venv/bin/python scripts/check-05-ui-uat.py --item 1         # PASS(Task 2;.hidden 五态显隐的层叠证据)
.venv/bin/python scripts/check-05-ui-uat.py --item 4         # PASS(Task 3;SC5 令牌接线 + #state-badge z-index)
git status --porcelain -- frontend/style.css                       # 空(硬规则 9)
ls frontend/vendor/                                          # 恰好 marked.min.js 一个文件
```

**本计划不打破任何既有门。** `check-05 --item 10` 的判定集变化是计划 01 引入的(D-03);本计划只改 `index.html` 的两个 `.overlay` 与 `app.js` 的三个区域,**不新增任何可聚焦元素**(新增的 2 个 id 挂在 `<h3>` 上,`<h3>` 不可聚焦;属性不改变 Tab 序)。**`check-05 --item 1` 与 `--item 4` 是本阶段契约 `idi-08-UI-SPEC.md` §契约校验命令 逐字点名「必须仍绿」的门,本计划实跑它们**(`--item 1` 落在 Task 2 —— 全阶段唯一改动两个弹窗 `.hidden` 开闭点的任务;`--item 4` 落在 Task 3),不留到收口才第一次跑。
</verification>

<success_criteria>
- 两个阻塞弹窗向辅助技术宣告为模态对话框,且该宣告**成真**(背景在键盘与指针两个层面都惰性)。
- Escape 能关闭两个弹窗:确认弹窗仅关闭、零决定;档位弹窗关闭并复位 `tierModalShown`,下一个自检事件能重弹。
- 弹窗关闭后焦点交还触发者(确认 → `#btn-authorize`;档位 → `#btn-continue-check`),成功路径不交还。
- 其余三个弹窗不响应 Escape(范围锁),`#permission-modal` 的已知缺口已登记且未修。
- `frontend/style.css` 逐字节未改;`frontend/vendor/` 仍恰好一个文件;三条不变量守卫仍全绿。
</success_criteria>

<output>
Create `.planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-02-SUMMARY.md` when done
</output>

# Phase 8: 可访问性语义与键盘 - Context

**Gathered:** 2026-09-23
**Status:** Ready for planning

<domain>
## Phase Boundary

让键盘用户能**真实完成**一次划词批注、让两个阻塞式弹窗支持 Escape 关闭并向辅助技术宣告与实现一致的模态语义、守住 REG-02 的两条回归门、并把 `b9664e0` 五条修复的全部人工验收重跑一遍。

**改动面(用户裁定后的实际形态):纯 `frontend/app.js` + `frontend/index.html`。`frontend/style.css` 零改动。** 前提是运行时实测确认「整盒焦点环」可辨(见 D-01);若不可辨,当场升级为改 CSS(见 D-02),届时作废 5 份 live 指纹。

**本阶段的性质:唯一触碰 `app.js` / `index.html` 的阶段。** 按代码 diff 面积最小(1 个 `tabindex` 属性、2 个弹窗 × 若干属性、约 10 行焦点交接、约 10 行 Escape 处理),但按风险最大:`app.js:4-75` 有约 70 个顶层 `getElementById` 句柄,**删除或改名一个 id 会在解析期静默杀死其下全部处理器**(已记录的 G-idi01-8 失效形态)。**新增 id 是安全的**——硬规则 5 禁的是改名与删除。

**已实测的环境基线(规划期直接采用,不必重新推导):**

| 事实 | 值 |
|---|---|
| `tabindex` / `role=` / `aria-` 在 `frontend/` 的计数 | **全为 0**;`:focus-visible` = 9(Phase 7 落地) |
| 全文件 `.focus()` 调用 | **只有一处** —— `app.js:488` `confirmWordInput.focus()` |
| `frontend/app.js` / `frontend/index.html` 在 live 指纹里的覆盖 | **零**。五份 live VERIFICATION(idi-04 / 04.1-radix / 05 / 06 / 07)只覆盖 `frontend/style.css` 与 `scripts/` |
| pytest 基线 | `219/225 collected (6 deselected)` ⇒ **219 passed + 6 skipped**。ROADMAP 的「219」正确;Phase 4 段里的「225」是 **collected** 数,两者不是一回事 |
| 五个状态样本里 `#round-doc` 内 `a[href]` | 计数 0(归档半场的运行时断言今天无服务对象) |
| `scripts/ui-states/` 里 `#round-doc` 的可见性 | p1 / p12 中它在 `.hidden` 子视图内 ⇒ **不可见** ⇒ 被普查的 `visible` 过滤排除;只有 p3 / checking / archive 三个样本会真的把它纳入判定集 |

**明确不含:**
- 新功能、新依赖、新前端文件、构建步骤(ROADMAP 里程碑章程)
- 焦点陷阱实现(REQUIREMENTS Out of Scope 表)—— **但 `inert` 例外,见 D-14**
- 完整 ARIA / 屏幕阅读器合规(用户已裁定取「窄切片」)—— 只做 `#confirmation-modal` / `#tier-modal` 两处
- `aria-live` 在流式聊天区(Pitfall M7:绝不可加在 chunk 容器上;**本阶段不加**,记录以防蔓延)
- 两处 `window.prompt` 替换(v2 `FLOW-V2-01`)—— 含 `rejectAuthorization()` 里的那个
- 暗色模式 / `prefers-color-scheme`(v1.14 全局已裁定排除)
- 动效 / 动画设计体系(INTERACT-02 的 120–150ms 就是全部规格)
- 响应式 / 移动端断点系统、`#probe-controls` 的移除或重定位(均为独立未来候选)
- `#selection-menu` 的 DOM 位置与定位数学(Pitfall 8 + 硬规则 5:必须保持 `<body>` 直接子元素,任何 `filter`/`transform`/`opacity` 祖先都会改变其包含块)
- `.collapse-indicator` 的越轨字面量(backlog `999.1`,**不得触碰**;`app.js:1550` 用 `textContent` 赋值,不得引入内联 `<svg>`)
- `showInlineError` 的 `textContent`-only 规则(XSS 缓解 T-260916-01,**不是风格选择**)
- `renderAnnotations` / `renderVerdictCard`(已验收路径)
- `applyArchiveView` 的两行(`app.js:817-818`)
- backlog `999.1` / `999.2`(各自会作废 `idi-04.1-radix` / `idi-07` 的指纹,与本阶段合并会搅浑两批复验)

**已签核、不得重开:** S-1(间距 12 档)、S-2(14px 为一级字号档)、S-3(`#ccc`→`#8a8a8a`)、S-4(冻结轮删除 `opacity`,改 `filter: saturate(0.6)` + 琥珀 `box-shadow: inset`)、04.1 的 S-5/S-6。04.1 原话:「all four signed off 2026-09-17; **none may be re-opened, and no one-line alternative may be executed**」。

</domain>

<decisions>
## Implementation Decisions

### 环的承载面与指纹口径(A11Y-02 的下半场)

- **D-01:** **`#round-doc` 的焦点环沿用 Phase 7 的整盒环,`style.css` 零改动。** 给 `#round-doc` 加 `tabindex="0"` 后,Phase 7 D-05 的枚举规则 `[tabindex]:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px }` **自动**生效,不需要任何新 CSS。

  **研究 PITFALLS 5 失效模式 4 的「环套在 `#round-doc` 上只有上下边缘可见」论断被推翻** —— 但**推翻它的理由是「水平方向恒不被裁切」**(父级 40px 水平 padding),**不是**「盒高数千像素」。

  ⚠ **执行期更正(2026-09-24,`idi-08-01` Task 2 实测;UI-SPEC §契约修正登记 A-10)。** 本条原文把「盒高数千像素 ⇒ 视口里是左右两条贯穿全高的竖线」写成了**实测证据**,但那是**规划期的几何推断,不是实测**。执行期实测:**p3 样本盒高 778.64px < 900px 视口** ⇒ 环是**完整矩形**(上边 + 左右两条竖边 + 下边);**环的垂直形态取决于文档长度与视口的关系,不是恒定的**(长于视口时才是两条竖线);底部边缘在默认滚动位被 `#doc-panel` 滚动边界裁 3.64px(scrollTop 67→71 即归零)。**D-01 的结论不变** —— 整盒环 + `style.css` 零改动**已由用户 2026-09-24 裁定为最终态**(实测对比度 5.57:1、环清晰可辨、D-02 不触发)。**但下游不得再引用本条原文的「两条竖线」当判据** —— 照它执行会对一个正确的实现**误触发 D-02**。

  **本项的实际收益是流程性的:Phase 8 因而成为唯一不欠任何指纹的阶段。** Phase 8 除环之外没有任何需要改 `style.css` 的理由(Escape 与焦点交接是 JS;`role`/`aria-modal`/`inert` 是 HTML/属性),而 `app.js` / `index.html` 不在任何 live 报告的 `covered_files` 里。 — **Reversibility:** costly — 回退是改 `style.css` 换承载面,作废 5 份 live 指纹并连带复验(见 D-25)。

- **D-02:** **若运行时实测发现整盒环不够可辨,当场升级为改 `style.css`,并接受作废 5 份 live 指纹、连带复验。** 用户裁定的原话是「实测不行就当场升级」。备选承载面两条(二选一,由实测与规划期裁定):`#round-doc:focus-visible { outline-offset: -2px }`(inset,注意 `.markdown-body` 若无内边距则竖线压在正文首字上);或把环挑到恒可见的 sticky 页头 `#doc-panel:has(#round-doc:focus-visible) #doc-panel-header { outline: 2px solid var(--color-focus); outline-offset: -2px }`(36px 高的紧凑环,Phase 6 起钉在顶;`:has()` 有 Phase 6 的 `:has(:empty)` 先例)。

  **不得把「不可辨」静默降级为已知局限** —— 那会造出一个「名义上可聚焦、实际看不出焦点在哪」的状态,正是 Pitfall 6 的失效形态。 — **Reversibility:** costly — 与 D-01 同因。

- **D-03:** **「可辨」的机器半场已由 `check-05` item 10 自动覆盖,不必新写断言。** `#round-doc` 入册后(item 10 的判定集 = `FOCUSABLE_SELECTOR` 去掉 `[tabindex="-1"]` 与 `:disabled`),普查会对它断言 `:focus-visible` 下计算 `outline-width` / `outline-color` 非零。**登记两处变化:** ①判定集在 **checking / p3** 两个样本里多一个成员 —— ⚠ **执行期更正:item 10 的实际样本集是 `p1` / `checking` / `p3`**(`check-05-ui-uat.py:3704` + `:3740`),**不跑 `archive`、不跑 `p12`,CLI 无 `--state` 旗标**;原文的「p3 / checking / archive」与「p1 / p12」两句不可满足/不可验证,`archive` 下的环覆盖是**已知未覆盖项**;②`_idi07_tab_drive(page, len(data)+8)` 的上限是数据驱动的,会自然吸收这个新 Tab 停靠点。**若该项在某个样本变红,先判它是「真缺陷」还是「普查集变化」,不要直接改门。** — **Reversibility:** costly — 与 D-25 同理。

- **D-04:** **`#round-doc` 入册后必须复跑 `scripts/probe-07-focus-composite.py`。** STATE.md 的 Deferred Items 已逐字登记该义务:「Phase 8 给 `#round-doc` 加 `tabindex="0"` 后该场景变为活体,届时须复跑该探针」。原因:五个样本的 `#round-doc` 内 `a[href]` 计数为 0 ⇒ `.archive-mode` 0.75 合成下的**运行时**环断言今天无服务对象,由常驻算术门(`check-02` 的 `--color-focus ON --color-surface NON-TEXT@0.75`,3.45 ≥ 3)+ 该一次性探针共同承担。**探针不进守卫契约**(与 `scripts/probe-05-resolve-color.py` 同定位)。 — **Reversibility:** reversible — 探针不是门。

### 键盘划词的提交手势(A11Y-03)

- **D-05:** **提交手势 = 抬起 Shift。** 按住 Shift 扩选时焦点**不动**(扩选全程不被打断),**松开 Shift** 时菜单弹出并把焦点送入 `#selection-menu` 的首个按钮(`#btn-annotate`)。

  **为什么必须有提交手势(本阶段最重要的机制事实):** `roundDoc.addEventListener('keyup', handleSelectionTrigger)`(`app.js:1350`)对**每一次** keyup 都触发。若照 ROADMAP 字面「keyup 分支把焦点移入菜单首按钮」实现:Shift+→ 选中 1 个字符 ⇒ keyup ⇒ 焦点跳到 `#btn-annotate` ⇒ 再按 Shift+→ 时事件目标已是菜单按钮,`roundDoc` 的 keyup 不再触发,且浏览器不会给按钮内的文本扩选 ⇒ **键盘用户永远只能选中一个字符**。而 A11Y-03 的验收项「Shift+方向键选区 → 菜单出现 → 焦点已入菜单」**会照常通过** —— 它测的是状态,不是可用性。规划期必须在计划里显式登记这条「按字面实现会假绿」的事实。

  **已登记的代价:** ①「松开 Shift 即提交」是**自造惯例**(非平台约定);②它引入了一个按键白名单事实(见 D-06);③鼠标路径的副作用(见 D-09)。 — **Reversibility:** costly — 手势是 A11Y-03 与 A11Y-08 验收脚本的共同前提,换手势要重述两条验收项并重跑人工 UAT。

- **D-06:** **`handleSelectionTrigger` 本身保持零按键白名单;Shift 提交写成独立监听器。** t8g 的既有决定原文是「不对 keyup 做按键白名单——『折叠/空白选区即关闭菜单』已让非选择类按键成为安全 no-op」(`app.js:1321-1322`)。**本项刻意偏离该决定的实质,但偏离只发生在新增的 Shift 专用监听器里** —— `handleSelectionTrigger` 一字不改,白名单不进入它。

  **规划期必须把这条理由写进围栏注释**,否则会被后来的读者当成违例删掉。判据口径:Shift 监听器只在「`e.key === 'Shift'` ∧ 菜单可见 ∧ 选区非折叠」三条同时成立时才移焦;任一条不成立即 no-op(空选区、折叠选区、菜单已隐藏都由 `handleSelectionTrigger` 的既有守卫处理)。

  **注意 Shift 的 keyup 只在焦点位于 `#round-doc` 子树内时才被该监听器捕获** —— 这恰好是「扩选结束」的时刻,也是为什么这个设计成立。 — **Reversibility:** reversible。

- **D-07:** **菜单项执行后也把焦点交还 `#round-doc`。** 用户裁定原话:「菜单项执行后也交还焦点」。理由:两个菜单项(`#btn-annotate` / `#btn-plain-ask`)都会先 `hideSelectionMenu()`,而焦点当时停在一个**已隐藏的按钮**上 ⇒ 回落到 `<body>`,键盘用户丢失位置(需重新 Tab 穿过整个侧栏)。**这是焦点交接的第三条腿,ROADMAP 未提。** — **Reversibility:** reversible。

- **D-08:** **Escape 关闭菜单并把焦点交还 `#round-doc`;`hideSelectionMenu()` 是统一挂点。** `hideSelectionMenu()`(`app.js:1296-1299`)今天有四个调用点(`document` 的 `mousedown` 关闭器、`window` 的 `scroll` 捕获关闭器、`handleSelectionTrigger` 的两条守卫、菜单项点击)。**「若焦点在菜单内则交还 `#round-doc`」写在这一个函数里** —— 单点、自解释,不散落到四个调用点(散落必然漏)。**不得把 `window.getSelection()` 一并清空**:那会毁掉「Escape 后接着 Shift+→ 继续扩选」这条路径。 — **Reversibility:** reversible。

- **D-09:** **鼠标路径的行为变化必须登记:`#round-doc` 现在是可点击聚焦的。** `tabindex="0"` 的 `<div>` 被鼠标点击即获焦(但鼠标点击**不**匹配 `:focus-visible`,所以不出环 —— SC2 语义仍成立)。后果:鼠标用户 Shift+点击扩选后**松开 Shift 也会把焦点送进菜单**。判定为**可接受**(焦点去的正是用户接下来要点的地方),但必须写进计划并复跑 REG-03 的人工检查第 4 条。 — **Reversibility:** reversible。

- **D-10:** **「焦点离开文档区后选区是否保留」是实测项,不是假设。** 已核实:`hideSelectionMenu()` 只清 `menuSelection` 快照,不清 `window.getSelection()`;Chrome 里焦点移到按钮通常不清除文档选区(高亮可能变灰)。**两个后果必须实测:** ①焦点入菜单后用户能否看见自己选了什么(若高亮被清 ⇒ 键盘用户是「盲批注」,直接伤 A11Y-03 的 SC1);②Escape 交还焦点后能否接着 Shift+→ 继续扩选(若锚点已重置 ⇒ 用户须重新划选,须登记为已知局限)。**规划期不得把这两条写成「预期成立」。** — **Reversibility:** reversible。

### 弹窗的语义与 Escape(A11Y-05 / A11Y-06)

- **D-11:** **「两个阻塞式弹窗」= `#confirmation-modal`(G3 确认词)+ `#tier-modal`(自检档位)—— 偏离 ROADMAP 点名的名单,用户已签核。** ROADMAP 点名的是「G3 确认、授权」(即 `#confirmation-modal` + `#permission-modal`);实测按「键盘用户今天真的会卡住」这条判据重排后:

  | 弹窗 | 打开时是否移焦 | 有取消按钮? | 判定 |
  |---|---|---|---|
  | `#confirmation-modal` | **✓ `app.js:488`** | ✓ 拒绝 | 键盘用户**已经**能 Tab 到「拒绝」——不卡 |
  | `#permission-modal` | ✗ | ✓ 拒绝 | 弹了键盘用户**不知道**(不移焦);但可 Tab 出去 ⇒ 不卡 |
  | `#tier-modal` | ✗ | **✗ 没有** | **真正的卡死**:必须二选一,且焦点不在里面 |
  | `#mission-complete-modal` | ✗ | 单关闭按钮 | 可 Tab 到达 |
  | `#cli-check-overlay` | ✗ | 单按钮 | 可 Tab 到达 |

  **这与本项目反复出现的同一形态同构**:Phase 6 A11Y-07「唯一确定不达标的是没被点名的那个」、Phase 7 D-02「路线图点名的缺陷对象是错的」。**裁定记录:用户 2026-09-23 在本讨论中裁定取「按实测:confirmation + tier」。** — **Reversibility:** costly — 换回名单要重开 A11Y-05/06 的对象集并重算 UI-SPEC 的覆盖声明。

- **D-12:** **`#confirmation-modal` 的 Escape = 仅关闭(`closeConfirmModal()`),不产生任何决定。** 理由:最小、零副作用;键盘用户本来就能 Tab 到「拒绝」(`openConfirmModal()` 已 `confirmWordInput.focus()`,Tab 跳过 disabled 的「放行」直达「拒绝」),所以 Escape 不需要代替拒绝。**不选「Escape = 拒绝」** 的理由:那会走 `rejectAuthorization()`,把用户**直接推进一个原生 `window.prompt`**;而替换 `window.prompt` 是 v2 `FLOW-V2-01`,本阶段不动。**不选「Escape = 拒绝但不弹 prompt」** 的理由:那要新增一条写批注的路径(用默认理由「授权被拒,继续完善」),与「不引入第二处真相来源」的立场相冲。 — **Reversibility:** reversible。

- **D-13:** **`#tier-modal` 的 Escape = 关闭 + 复位 `tierModalShown = false`(允许重弹)。** 已核实的死状态风险:该弹窗在 `sessionData.state === 'phase5_awaiting_tier'` 且未选档时弹出,**打开时立刻把 `tierModalShown = true`**(`app.js:638-640`);只有选档成功才 `classList.add('hidden')`(`app.js:799`)。**若被关掉而没选,`selfcheck.tier` 仍为空而 `tierModalShown` 已是 true ⇒ 它不会再弹** —— 用户落进「档位未定且入口消失」。复位该标志使下一个自检事件(`refreshChecksAfterStream`)能重新弹出。**已登记的代价:** 复位后弹窗可能在用户做别的事时重现 —— 但这正是「档位未定就该继续问」的正确行为。**保留 A11Y-05 与 SC3 的「可 Esc 关闭」字面。** — **Reversibility:** reversible — 回退是删一行。

- **D-14:** **`role="dialog"` + `aria-modal="true"` + 原生 `inert`,让宣告成真。** 在打开/关闭两个弹窗时给 `#app` 加/去原生 `inert` 属性。理由:`aria-modal="true"` 的语义是「弹窗之外的背景对辅助技术是惰性的」,而焦点陷阱是已裁定 Out of Scope ⇒ 只加两个属性会复现 ROADMAP 警告 `role="dialog"` 时点名的同一形态:**宣告了一个实现并不兑现的契约**。`inert` 是原生 HTML 属性,零依赖、零构建、约 4 行,且顺带拿到焦点陷阱的**主要**效果(背景不可聚焦、不可点)。**用户裁定原话:「加 inert,让宣告成真」。**

  **已核实 `#app` 的边界**:`index.html` 的 `#app`(`L10` 起)在 `L155` 闭合,五个 `.overlay` 与 `#selection-menu`(`L158-219`)都是 `#app` 的**兄弟**,故 `inert` 只作用于背景、不会波及弹窗自身。**注意 `#selection-menu` 也在 `#app` 之外** ⇒ 弹窗打开时它不会被 inert(两者同时可见的场景不存在,规划期须确认这一点并登记)。 — **Reversibility:** costly — 回退要同时去掉 `inert` 的挂载点与 `aria-modal`,并把 SC3 重述为「可 Esc 关闭 + 移焦」而非「背景惰性」。

- **D-15:** **两个弹窗用 `aria-labelledby` 指向弹窗内的 `<h3>`,需给这两个 `<h3>` 各加一个**新** id。** 文案只存一处(随 `<h3>` 走,不会漂移)。**硬规则 5 禁的是改名/删除既有 id;新增 id 安全。** 已核实 `#confirmation-modal` 的 `<h3>` 是「授权确认」、`#tier-modal` 的是「选择自检档位」(`index.html:172` / `L186`)。**不选 `aria-label` 写字面串** 的理由:文案变成第二处真相来源,与本项目「名必须说实话」的纪律相冲。 — **Reversibility:** reversible。

- **D-16:** **两个弹窗打开时都要移焦。** `#confirmation-modal` 已有(`app.js:488` `confirmWordInput.focus()`);**`#tier-modal` 缺,须补** —— 焦点送入弹窗内(首个可操作控件,或弹窗容器本身)。理由:这是 D-11 判定的「卡死」的**实质修复** —— `#tier-modal` 的陷阱不是「没有 Escape」而是「焦点不在里面」;`inert`(D-14)落地后背景不可聚焦,焦点若不在弹窗内会掉到 `<body>`。**规划期须实测 `inert` 生效瞬间焦点落在哪里**,并据此决定是否需要显式 `.focus()`。 — **Reversibility:** reversible。

- **D-17:** **`#permission-modal` 的「弹了键盘用户不知道」(打开时不移焦)登记为已知缺口,归 v2 `A11Y-V2-02`。** 本阶段**不修**。登记位置:`08-UAT.md` 或 VERIFICATION 的 manual/advisory 节 + 本 CONTEXT 的 deferred。理由:用户已裁定取 `confirmation + tier` 两个对象(D-11),而该弹窗可 Tab 出去、不构成卡死。 — **Reversibility:** reversible。

### `#round-doc` 的 ARIA(A11Y-02 的上半场)

- **D-18:** **`#round-doc` 不加 `role`,也不加 `aria-label`。** 加了 `tabindex="0"` 之后它是一个**裸 `<div>` 的 Tab 停靠点**,辅助技术只会报「通用容器」—— 这是**知情接受**的代价,不是疏漏。理由取自用户自己立的立场:REQUIREMENTS 的 Out of Scope 表把「完整 ARIA」排除的原话是「ARIA 服务于不带上下文到达、且看不见屏幕的用户;本工具恰好一个用户,既是作者也看得见屏幕」。**用户裁定原话:「都不加(保持窄切片)」。** `role` 与焦点陷阱等一起归 v2 `A11Y-V2-02`。 — **Reversibility:** reversible。

- **D-19:** **不加任何键盘划词的可发现性提示,登记为已知局限。** 新键盘路径是「Tab 进文档区 → Shift+方向键扩选 → 松开 Shift → 焦点入菜单」,全流程唯一的视觉信号就是焦点环 —— **没有任何东西告诉键盘用户 Shift+方向键能划词**。**已登记的后果:这个缺口不会让任何门变红**,因为 A11Y-08 的人工验收由用户执行(用户当然知道步骤)。**不选「复用 `#rounds-hint` 加一句」** 的理由:改既有元素的内容与显隐时机属可见行为变更,且它是「已进入轮次阶段(本阶段占位)。」的占位语义。**不选「新增一处 `.hint`」** 的理由:那是新 UI 元素 + 新 DOM,与「唯一触碰 app.js/index.html 的阶段」的交付物清单不符。 — **Reversibility:** reversible。

- **D-20:** **阶段 1-2 的 `#draft-content`(同为 `.markdown-body`)不加 `tabindex`。** 这是**正确的**、不是漏项:`handleSelectionTrigger` 的第一条实质守卫是 `if (currentState !== 'phase3') return`(`app.js:1327`),阶段 1-2 根本没有批注功能,给它加 Tab 停靠点是**死代码**(违反本项目「不声明不被消费的东西」的纪律,且无法被运行时验证)。**规划期须把这条理由写进计划**,否则会被读者当成「A11Y-02 只点名了 `#round-doc`」的漏项去补。 — **Reversibility:** reversible。

### 验收门与回归(REG-02 / REG-03 / A11Y-08)

- **D-21:** **两条 REG-02 回归门落为计划级 `<verify>` grep 步骤 + 人工 UAT 条目,不写进 `scripts/check-05-ui-uat.py`。** 两条门是:`grep -c 'inline-error' frontend/style.css` 仍为 **1**;`clearInlineError` 调用点计数**只增不减**(基线 6 个 `clearInlineError();` 调用 + 1 定义)。理由:`scripts/check-05-ui-uat.py` **在 5 份 live 报告的 `covered_files` 里**,把断言写进去会让 D-01 的「零指纹债务」当场消失 —— 而这五份的复验对象全是 CSS/令牌,与本次的 JS/HTML 改动几乎不相干。**已登记的代价:** 这两条不是常驻守卫,下次改 `style.css` 的人不会自动被拦。**用户裁定原话:「落为计划级 grep(保住零债务)」。** — **Reversibility:** costly — 改为写进 harness 就要连带复验五份,且要重算 `idi-07` 的指纹。

- **D-22:** **REG-03 = `b9664e0` 五条修复的全部人工验收项重跑,这是收口 gate,不是事后补记。** 原文六条(`.planning/quick/260916-t8g-ui-5-blocker-hidden-sse-onerror/260916-t8g-PLAN.md` 的 `<verification>` 节):①阶段 1-2 项目只显示草稿正文、「尚无草稿」提示不可见;②阶段 3 项目轮次文档上方无占位提示、撰写/自检视图中轮次切换器不可见;③走完流程至 `mission_complete` → 「处理本轮批注」不可见且 `disabled === true`、授权行不可见、轮次切换器**仍可见可切**;④**用 Shift+方向键在轮次文档中划选 → 菜单出现**(依赖键盘选区,**须按 D-05 的新手势重写步骤并逐项记录观察结果**);⑤停掉后端 → 横幅出现「正在自动重连……」,恢复 → 自动消失;致命断开 → 红色横幅;⑥不存在的路径点「进入」→ 错误出现在输入框正下方,再次点击时旧错误先消失。

  **第 4 条必须重写**:它的原文预期是「菜单出现」,而 D-05 之后键盘路径多了一个「松开 Shift」的动作,**原先通过的检查现在测的是另一件事**(与 Pitfall 3 / Pitfall 6 的「人工检查被继承而非重跑」是同一类失效)。 — **Reversibility:** reversible — 复验是流程义务。

- **D-23:** **归档路径的专项复验:切轮之后确认「处理本轮批注」不可点。** 走 `updateFrozenPresentation` 的复位路径(`app.js:1166` 会把 `applyArchiveView` 设的 `disabled = true` 复位 —— Pitfall 3 UI-6.3 的现场)。ROADMAP Phase 8 的 Gates 明列此条。 — **Reversibility:** reversible。

- **D-24:** **pytest 基线的算术口径:判据是「219 passed + 6 skipped / 225 collected」,照抄「225」会造出必然失败或必然通过的假门。** ROADMAP Phase 8 Gates 写的是「pytest 219 基线不变」(正确);Phase 4 段里的「225」是 `--collect-only` 的数。**本阶段后端零改动,该门只是回归证明。** 必须用项目 venv(`.venv/bin/python -m pytest`):环境 `python3` 是 miniconda,会让 4 个 `ai_caller` 测试假失败。 — **Reversibility:** reversible。

- **D-25:** **指纹义务登记:本阶段在 D-01 路径下零债务;升级到 D-02 则作废 5 份。** 逐份核实:`idi-04` / `idi-04.1-radix` / `idi-05` / `idi-06` / `idi-07` 的 `covered_files` 均含 `frontend/style.css`(其中 04.1 / 05 / 06 / 07 还含 `scripts/check-05-ui-uat.py`)。**`frontend/app.js` 与 `frontend/index.html` 不在任何一份里。** 收口时若真的改了 CSS,须**以 HEAD 内容重算指纹**、不要看 mtime(本项目已记录:stale 有两种成因 ——「内容真变」走重新验证,「记账性编辑」走重算 + 披露,补救方向相反)。⚠ **`gsd-tools query verification status <phase>` 对这些报告一律返回 `missing`**(相位目录命名与工具的相位令牌解析不匹配),**不得用该命令判定 stale**。 — **Reversibility:** reversible — 复验是流程义务。

- **D-26:** **`idi-04.1-radix` 的复验义务**本阶段开始前**仍未收口**(STATE.md Operator Next Steps 第 2 条:`/gsd-verify-work idi-04.1-radix`,其 `covered_digest` 因 Phase 5 改写 `style.css` 与 `check-05-ui-uat.py` 而 stale,成因是内容真变)。**本阶段在 D-01 路径下不新增这一层**;若走 D-02,则它叠加一层。规划期须在计划里显式登记这条既有待办,不要把它当成 Phase 8 引入的。 — **Reversibility:** reversible。

### Claude's Discretion

- **`inert` 的挂载时机与多弹窗同时开**:两个弹窗同时打开的场景是否存在(`#tier-modal` 与 `#confirmation-modal` 会在同一流程的不同阶段出现,理论上互斥);若存在,`inert` 的加/去必须成对且幂等。规划期实测后裁定。
- **Escape 监听器的归属**:`document` 上的单点监听器(带「哪个弹窗可见」的优先级判定)vs. 各弹窗各自的监听器。前者单点、可解释,后者更局部但会引入「谁先响应」的顺序事实。规划期裁定并写明理由。
- **`hideSelectionMenu()` 里「焦点在菜单内则交还 `#round-doc`」的判据形态**(`selectionMenu.contains(document.activeElement)` 或等价写法)。
- **`role="dialog"` 落在 `.overlay` 还是 `.overlay-card` 上**(前者是遮罩 + 居中容器,后者是卡片本体)。
- **Shift 提交是否额外 gate 在「菜单可见」上**(D-06 已给定三条判据,但「菜单可见」是必要条件还是仅充分条件之一,由规划期裁定)。
- **`#selection-menu` 是否要 `tabindex="-1"`**(若焦点落在首按钮则不需要;注意 `tabindex="-1"` 会被 `check-05` item 10 的普查排除 —— 这是设计而非漏项)。
- **两个新 id 的命名**(D-15),须与既有命名风格一致且不与 70 个 `getElementById` 句柄冲突。
- **实测的工具与判据的具体形态**(D-02 的「可辨」、D-10 的两条选区行为、D-16 的 `inert` 焦点落点)。环境事实:截图不可用(headless 渲染被阻,常驻 `/api/events` SSE 流让采集处理器无法终止)⇒ **用计算样式检查 + 具名人工步骤,不要计划视觉 diff**;若用 Playwright **必须** `chromium.launch({ channel: 'chrome' })`。
- 围栏注释与代码注释的措辞与粒度(尤其 D-06 的「为什么这里可以引入按键白名单而 `handleSelectionTrigger` 不行」、D-20 的「为什么 `#draft-content` 不加 `tabindex` 不是漏项」、D-14 的「`inert` 是让宣告成真而不是扩大范围」)。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 本阶段的直接上游(必须读)
- `.planning/ROADMAP.md` §Phase 8 — 本阶段的 goal / Deliverables / Success Criteria / Avoids(Pitfall 6 / 3 / 10 / M7 / Anti-Pattern 6)/ Research flag / Manual checks / Gates。**注意:其「两个阻塞弹窗」的名单已被 D-11 按实测替换,其「keyup 分支移焦」的字面已被 D-05 替换 —— 交付物须以本文件的决定读**
- `.planning/ROADMAP.md` §全局硬规则 1-7 — **每个计划都适用**;尤其规则 5(不得触碰清单:`.fatal` 修饰符、`applyArchiveView` 两行、`#selection-menu` 的 DOM 位置、`showInlineError` 的 `textContent`-only、`renderAnnotations` / `renderVerdictCard`、`app.js:4-75` 约 70 个 `getElementById` 句柄的 id 不得改名或删除)、规则 6(零新增依赖 / 零构建)、规则 7(每个 `style.css` 计划须带运行时验证 —— D-01 路径下本阶段无 `style.css` 计划)
- `.planning/ROADMAP.md` §Phase 7 — **本阶段的上游**;D-05/D-06 的 `[tabindex]` 枚举、D-14 的「焦点环必须瞬变」、以及「`#round-doc` 的环承载面明确指派给 Phase 8」的原文
- `.planning/REQUIREMENTS.md` §A11Y-02 / §A11Y-03 / §A11Y-05 / §A11Y-06 / §A11Y-08 / §REG-02 / §REG-03 — 本阶段六条需求的原文
- `.planning/REQUIREMENTS.md` §Out of Scope 表 — 「完整 ARIA / 屏幕阅读器合规」(D-18 的立场来源)、「焦点陷阱实现」(D-14 的边界)、「图标库」等
- `.planning/REQUIREMENTS.md` 文末「人工验收项」节 — A11Y-08 / A11Y-03 键盘半场 / REG-03 依赖键盘选区的项
- `.planning/STATE.md` §Operator Next Steps + §Deferred Items — D-04 的探针义务原文(`[v1.14 P7]` 那条)、D-22/D-23 的收口登记、D-26 的 04.1 复验待办、以及 `[v1.14 P8]` 那条「五条 b9664e0 修复无自动化覆盖,而本里程碑重写其依赖的 CSS」

### 契约与签核(必须读)
- `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` §Sign-Off Items **S-4** — 冻结轮 route 1 vs route 2 的裁定原文(含「route 1 会把环降到 2.85:1」的实测理由)。**D-01 沿用整盒环的算术前提**
- `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` §Do-Not-Touch List / §Global Hard Rules / §The Four Contract-Check Commands — 硬规则 5 的原始清单
- `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` §Color / §Contrast Verification — tier-1 / tier-2 名与计数的权威
- `.planning/phases/idi-07-interaction-states-and-focus/07-CONTEXT.md` — **D-05(枚举集 = `check-05` 普查的可聚焦集)** / D-06(`#round-doc` 的环指派给 Phase 8)/ D-14(环必须瞬变)/ D-15(`check-02` / `check-05` 的扩写落点)/ **D-19(四份报告的连带复验义务,D-25 的起点)** / D-20(须显式登记被打破的断言)
- `.planning/phases/idi-06-layout-robustness/06-CONTEXT.md` — D-01(基线口径)/ D-13(焦点环解裁切按元素普查)/ D-17(`.annotation-answer summary` 是唯一确定不达标的紧凑控件)/ D-19(连带复验义务)
- `.planning/phases/idi-05-typography-and-visual-hierarchy/05-CONTEXT.md` — D-01(基线口径)/ D-23(不得触碰 `.collapse-indicator`)
- `.planning/phases/idi-07-interaction-states-and-focus/idi-07-VERIFICATION.md` §frontmatter `covered_files` / `covered_digest` — D-25 的清单来源
- `.planning/phases/idi-04-tokens-contract/idi-04-VERIFICATION.md` §frontmatter `overrides:` — backlog `999.1` 的指派记录

### 研究输入(必须读 —— 本阶段是 Pitfall 5/6/10 的正面战场)
- `.planning/research/PITFALLS.md` §Pitfall 6(`tabindex` without `:focus` —— **本阶段的核心**;含「prefer not adding tabindex to `#round-doc`」的反对意见,以及「若加则须重跑 UI-6.1 人工 UAT」的强制项)
- `.planning/research/PITFALLS.md` §Pitfall 5 失效模式 4(「环套在 `#round-doc` 上不可见」—— **D-01 已用几何推翻,须以本文件读**)
- `.planning/research/PITFALLS.md` §Pitfall 3(五条已交付修复的回归)/ §Pitfall 10(内联错误的 flex 缺陷与 `textContent` 不变量)/ §M7(`aria-live` 绝不可加在 chunk 容器上)
- `.planning/research/PITFALLS.md` §"Looks Done But Isn't" Checklist — 尤其 `tabindex` 与 `:focus` 计数不得独立移动、五条人工检查重跑、归档切轮后按钮不可点、`showInlineError` 仍用 `textContent`
- `.planning/research/SUMMARY.md` §"Baseline Reconciliation" — **基线数字一律取此表**(审计报告的计数是 `b9664e0` 之前的旧值)

### 代码面(本阶段的唯一改动面)
- `frontend/index.html` §L139 — `#round-doc`(本轮文档 markdown 渲染区,`tabindex="0"` 的落点)
- `frontend/index.html` §L158-219 — 五个 `.overlay`(`#permission-modal` / `#confirmation-modal` / `#tier-modal` / `#mission-complete-modal` / `#cli-check-overlay`)+ `#selection-menu`;`#app` 在 **L155** 闭合,故这六个元素都是它的兄弟(D-14 的关键事实)
- `frontend/index.html` §L172 / §L186 — 两个弹窗的 `<h3>`(「授权确认」/「选择自检档位」,D-15 的新 id 落点)
- `frontend/app.js` §L4-75 — 约 70 个顶层 `getElementById` 句柄(**id 不得改名或删除**;新增安全)
- `frontend/app.js` §L301-320(`showInlineError` / `clearInlineError` / `inlineErrorEl`)—— REG-02 的现场与 `textContent` 不变量
- `frontend/app.js` §L483-560(`openConfirmModal` / `closeConfirmModal` / `rejectAuthorization` / `#btn-authorize` 的监听器与两条分支)—— D-12 的对象;`L488` 是全文件唯一的 `.focus()`
- `frontend/app.js` §L632-643(`phase5_awaiting_tier` 的弹窗分支,含 `tierModalShown = true`)/ §L786-807(`chooseTier` / `tierModal.classList.add('hidden')`)—— **D-13 的死状态现场**
- `frontend/app.js` §L1202-1215(`showPermissionModal` —— **不移焦**)—— D-11 / D-17 的对象
- `frontend/app.js` §L1285-1360(`selectionInRoundDoc` / `hideSelectionMenu` / `showSelectionMenu` / `handleSelectionTrigger` / `initSelectionMenu`)—— **D-05…D-10 的全部现场**;`L1321-1322` 是 t8g 的「不做按键白名单」注释原文;`L1349-1350` 是 `mouseup` + `keyup` 两条绑定
- `frontend/app.js` §L1166(`updateFrozenPresentation`)/ §L817-818(`applyArchiveView` 的两行,硬规则 5 不得触碰)—— D-23 的对象
- `frontend/style.css` §围栏 `:root` 的 PAIR 清单 + `:focus-visible` 规则(Phase 7 的七选择器枚举含 `[tabindex]`)—— **D-01 不触碰它,但要读懂它为什么会自动生效**
- `frontend/style.css` §`#doc-panel-body { padding: var(--space-8) var(--space-10) }`(=`32px 40px`)—— D-01 几何论证的关键事实
- `frontend/style.css` §`#round-doc.round-frozen`(S-4 落地形态:无 `opacity`)/ §`#rounds-placeholder.archive-mode #round-doc { opacity: 0.75 }`(唯一存活的合成源)—— D-04 的两个半场

### 门与脚本
- `scripts/check-05-ui-uat.py` — Playwright UAT harness(`--item N` 单跑);**item 10 是焦点环的元素普查**(`FOCUSABLE_SELECTOR` 在 `:1748` = `button, input, select, textarea, a[href], summary, [tabindex]`;判定集过滤 `visible` ∧ `focusable` 且排除 `[tabindex="-1"]` 与 `:disabled`;`_idi07_tab_drive` 的上限是 `len(data)+8`);**`:43-105` 的 docstring 逐字登记了归档半场无服务对象的事实与枚举同步纪律**;**D-03 的判定集变化与 D-21 的「不写进这里」都以它为准**
- `scripts/check-01-token-conformance.sh` / `check-02-contrast.py` / `check-03-hidden-uniqueness.sh` / `check-04-important-count.sh` — 四条不变量守卫,**本阶段不得破坏**(D-01 路径下不触碰)
- `scripts/probe-07-focus-composite.py` — **D-04 的复跑对象**;一次性注入探针的定位范本(「不是门,不进守卫契约」)
- `scripts/probe-05-resolve-color.py` — 同上的定位先例
- `scripts/ui-states/` — p1 / p12 / p3 / checking / archive 五个磁盘状态样本;**`#round-doc` 在 p1/p12 里不可见**(D-03 的关键事实)
- `scripts/check-06-idi05-validation.py` — 编号已被占用

### 已交付修复的原始记录(REG-03 的判据来源)
- `.planning/quick/260916-t8g-ui-5-blocker-hidden-sse-onerror/260916-t8g-PLAN.md` §`<verification>` — **六条人工检查的原文**(D-22)
- `.planning/quick/260916-t8g-ui-5-blocker-hidden-sse-onerror/260916-t8g-SUMMARY.md` — 五条修复的 coverage 表与 `human_judgment` 理由(尤其 D4 的「已知限制:`#round-doc` 是不可聚焦的普通 div,keyup 仅在焦点已落在容器内时生效」—— **本阶段正是要消掉这条限制**)
- `.planning/quick/260917-fqh-b9664e0-hidden-flex/` — REG-01 / REG-02 的修复记录(`46e8ea3` + `793071e`)
- `.planning/milestones/v1.13-phases/idi-03-g3/03-UI-REVIEW.md` — v1.14 范围的来源(13/24,7 BLOCKER)

### 需求与状态
- `DESIGN.md` — 项目唯一权威设计文档;**已核实其全文对键盘 / 无障碍 / 焦点 / `tabindex` / Escape / ARIA 零提及** ⇒ 本阶段是在**零可访问性设计契约**下建立契约,与 v1.14 里程碑章程的立意一致;§3.8 是语言红线;§4.1 两栏契约(不得改变其含义);§4.4 的 G3 授权路径;§5.4 的权限表(「弹窗」的语义来源)
- `.planning/PROJECT.md` §Current Milestone / §Key Decisions — 「`tabindex` 与 focus 样式必须一起定」的立项表述
- `.planning/REQUIREMENTS.md` §Traceability — A11Y-02/03/05/06/08 与 REG-03 均为 Phase 8、状态 Pending

### 外部
- **WCAG 2.1 SC 2.1.1(Keyboard)/ SC 2.4.3(Focus Order)** —— 键盘可达性的达标依据
- **WCAG 2.1 SC 4.1.2(Name, Role, Value)** —— D-14 / D-15 的达标依据(`role` 与无障碍名称)
- **WAI-ARIA Authoring Practices: Dialog (Modal) Pattern** —— `aria-modal` 的「背景惰性」语义是 D-14 的判据来源
- **MDN `inert`(全局 HTML 属性)** —— D-14 的机制;原生、零依赖、零构建(满足硬规则 6)
- 无其他外部规范依赖。

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **Phase 7 的 `[tabindex]:focus-visible` 枚举规则**(`style.css`):**D-01 的核心杠杆** —— `tabindex="0"` 一落,环零 CSS 自动生效。这是 Phase 7 D-05「枚举含 `[tabindex]`」的刻意设计,本阶段正是它的消费者。
- **`check-05` item 10 的元素普查**(`:1748` `FOCUSABLE_SELECTOR`,`_idi07_tab_*` 三个探针):**D-03 的现成门** —— `#round-doc` 一入册就被断言,零新代码。
- **`scripts/probe-07-focus-composite.py`**:D-04 的复跑对象;一次性注入探针的定位范本。
- **原生 `inert` 属性**:D-14 的机制 —— 零依赖、零构建,且不需要写焦点陷阱。
- **`#app` 的 DOM 边界**(`index.html` L10-L155):五个 `.overlay` 与 `#selection-menu` 都是它的**兄弟** ⇒ `inert` 挂 `#app` 天然只作用于背景。
- **`hideSelectionMenu()` 单函数**(`app.js:1296`):D-08 的**单点挂点** —— 四个调用点都经过它。
- **`closeConfirmModal()` 已存在**(`app.js:491`):D-12 直接复用,零新函数。

### Established Patterns
- **「按元素普查,不按选择器计数」**(Phase 5 `G-idi-05-1` → Phase 6 D-13/D-14 → Phase 7 D-16):D-03 沿用。
- **「实测驱动,不采信上游文档的论断」**(Phase 6 D-08/D-15、Phase 7 D-02):**D-01 推翻 PITFALLS 5 失效模式 4、D-10 拒绝把选区行为写成「预期成立」、D-16 要求实测 `inert` 的焦点落点 —— 三处都是它的实例。**
- **「名必须说实话」**(04.1 D-03 / Phase 5 D-18):D-15 选 `aria-labelledby` 而非 `aria-label` 字面串。
- **「与消费者同提交」**(硬规则 5):D-14 的 `inert` 与 `role`/`aria-modal` 同提交;D-05 的 Shift 监听器与它消费的菜单可见性同提交。
- **「追加,不重排」**(硬规则 3):本阶段不编辑 `style.css`(D-01),该规则只约束「不得顺手改 CSS」。
- **「防御性非冗余必须写注释」**(06-CONTEXT D-09 / 07-CONTEXT D-10):D-06 的「白名单只在这里合法」、D-20 的「`#draft-content` 不加不是漏项」、D-16 的「`inert` 是让宣告成真而非扩范围」三处都适用。
- **`.hidden` 是机制而非样式**:`display: none !important` 不得令牌化/移动/弱化;`#selection-menu` 与两个弹窗的显隐都靠它。**`inert` 与 `.hidden` 是两个正交机制,不要互相替代。**
- **环境事实(不得重新推导、不得对抗)**:截图不可用(headless 渲染被阻,常驻 `/api/events` SSE 流让采集处理器无法终止)⇒ **用计算样式检查 + 具名人工步骤,不要计划视觉 diff**;若用 Playwright **必须** `chromium.launch({ channel: 'chrome' })`;**键盘文本选区无法自动化**(连 `contenteditable` 都选不中)⇒ A11Y-08 / A11Y-03 键盘半场 / REG-03 第 4 条**必须**是具名人工验收,**不得因自动测试 FAIL 判定功能缺陷**。

### Integration Points
- **改动面** = `frontend/index.html`(`#round-doc` 的 `tabindex`;两个弹窗的 `role` / `aria-modal` / `aria-labelledby`;两个 `<h3>` 的新 id)+ `frontend/app.js`(Shift 提交监听器、Escape 分派、焦点交接三处、`inert` 挂载、`#tier-modal` 的移焦与标志复位)。**`frontend/style.css` 零改动(D-01)**;`frontend/vendor/` 保持只有 `marked.min.js`。
- **`scripts/check-05-ui-uat.py` 零改动(D-21)** —— 保住零指纹债务。
- **跨阶段接口(Phase 7 → 8)**:Phase 7 D-06 把 `#round-doc` 的环承载面**明确指派**给本阶段;Phase 7 刻意不写针对它的规则(会变死代码)。**本阶段必须履约 —— 且履约方式是「确认枚举规则已自动覆盖 + 实测可辨」,而不是新增规则。**
- **本阶段会打破/触及的既有断言(必须在计划里显式登记,D-25 的口径)**:`check-05` item 10 的判定集(p3 / checking / archive 三个样本多一个成员);`check-05` 的 `_idi07_tab_drive` 上限(数据驱动,自然吸收);`probe-07-focus-composite.py` 的复跑(D-04)。**其余四条不变量守卫(check-01…04)在 D-01 路径下不受影响。**
- **规划期必须先跑的「执行前基线」**:`node --check app.js`;`.venv/bin/python -m pytest -q -m "not slow"`(期望 219 passed / 6 skipped);`grep -c 'inline-error' frontend/style.css`(期望 1);`grep -c 'clearInlineError();' frontend/app.js`(期望 6);`grep -c tabindex frontend/index.html`(期望 0);`grep -c ':focus-visible' frontend/style.css`(期望 9)。**先建立基线再逐条登记打破项。**

</code_context>

<specifics>
## Specific Ideas

- **本阶段最重要的一条机制事实:「按路线图字面实现会假绿」。** ROADMAP 写「`handleSelectionTrigger` 的键盘分支把焦点移入 `#selection-menu` 首个按钮」,而该函数挂在**每一次** keyup 上 ⇒ 键盘用户永远只能选中一个字符;而 A11Y-03 的验收项「Shift+方向键选区 → 菜单出现 → 焦点已入菜单」**会照常通过**(它测状态,不测可用性)。这与 Pitfall 6 的「人工检查被继承而非重跑」是同一失效类。规划期必须把这条写进计划,否则会被当成「已按路线图实现」。
- **第二个「点名对象是错的」**:ROADMAP 点名 `#confirmation-modal` + `#permission-modal`,而实测 `#confirmation-modal` 恰是**唯一已经移焦**的那个(不卡),真正卡死的是 `#tier-modal`(无取消 + 不移焦)。这与 Phase 6 A11Y-07「唯一确定不达标的是没被点名的那个」、Phase 7 D-02「路线图点名的缺陷对象是错的」三次同构。
- **第三个「研究论断被几何推翻」**:PITFALLS 5 说环套在 `#round-doc` 上「只有上下边缘可见」,而父级有 40px 水平 padding ⇒ **水平方向恒不被裁切**。**这条推翻直接换来「Phase 8 零指纹债务」这个流程性质。** ⚠ **执行期更正(2026-09-24)**:本条原文还写了「左右两条竖线贯穿全高」,那是**几何推断而非实测** —— 执行期实测 p3 盒高 **778.64px < 900px 视口** ⇒ 环是**完整矩形**,垂直形态取决于文档长度。**推翻上游论断的理由只是「水平方向」**,与「两条竖线」无关(UI-SPEC §契约修正登记 **A-10**)。
- **`aria-modal="true"` 的诚实性问题被 ROADMAP 自己立为判据**(SC3「该宣告与实现一致」),而焦点陷阱是已排除项 ⇒ 只加两个属性就是「宣告一个不兑现的契约」,与 ROADMAP 警告 `role="dialog"` 时点名的形态完全一致。原生 `inert` 是零依赖的解法,用户已授权。
- **`#tier-modal` 的 Escape 不能等于「关闭」**:它打开时立刻把 `tierModalShown` 置真,关掉不选 ⇒ 档位未定且入口消失。复位该标志是 1 行的解法,且「档位未定就该继续问」本来就是正确行为。
- **`inert` 的边界是白送的**:五个 `.overlay` 与 `#selection-menu` 都是 `#app` 的兄弟(`index.html` L155 闭合 `#app`),所以 `inert` 挂 `#app` 天然只作用于背景 —— 不需要逐个元素处理。
- **`#round-doc` 与 `#draft-content` 的不对称是刻意的**:后者同为 `.markdown-body` 但阶段 1-2 无批注功能(`handleSelectionTrigger` 第一条实质守卫是 `currentState !== 'phase3'`),加 `tabindex` 是死代码。规划期须写清理由,否则会被当漏项补上。
- **两条 REG-02 门的落点是一次真实的取舍**:写进 harness 会作废 5 份 live 指纹,而那 5 份的复验对象全是 CSS/令牌,与本次 JS/HTML 改动几乎不相干 —— 所以用户选了「落为计划级 grep,保住零债务」,代价是它不再是常驻守卫。
- **`#permission-modal` 的「弹了键盘用户不知道」是本次讨论新暴露的真缺陷**,已登记归 v2 `A11Y-V2-02`(D-17)。不要在本阶段顺手修 —— 用户已裁定对象集。
- **D-19 的诚实性**:可发现性提示的缺口**不会让任何门变红**(人工验收由知道步骤的用户执行),所以要显式登记而不是假装被覆盖 —— 与 Phase 7 D-18 的「归档半场今天没有服务对象,登记这个事实而不是假装断言覆盖了它」是同一类警惕。

</specifics>

<deferred>
## Deferred Ideas

- **`#permission-modal` 的「弹了键盘用户不知道」**(打开时不移焦,无任何宣告)—— 归 v2 `A11Y-V2-02`。本阶段不修(D-17)。
- **焦点陷阱实现**(含 Shift+Tab 环绕与动态内容)—— v2 `A11Y-V2-01`;`inert`(D-14)只拿到它的主要效果,不是完整实现。
- **其余三个弹窗(`#permission-modal` / `#mission-complete-modal` / `#cli-check-overlay`)的 `role` / `aria-modal`** —— v2 `A11Y-V2-02`。
- **`aria-live` 在流式聊天区** —— v2 `A11Y-V2-03`;**约束**:绝不可加在 chunk 容器上(`appendSayToChat` 每个 SSE 事件追加一个 DOM 节点),应在气泡层配 `aria-busy` 或用 `role="log"`。`#stream-banner` 的 `aria-live="assertive"` 是 `A11Y-V2-04`。
- **`#round-doc` 的 `role="region"` + `aria-label`** —— D-18 裁定不加;若日后要加,与 v2 `A11Y-V2-02` 合并。
- **键盘划词的可发现性提示** —— D-19 裁定不加,登记为已知局限。
- **两处 `window.prompt` 的替换**(`app.js:486`、`app.js:1354`,含 `rejectAuthorization()` 里的那个)—— v2 `FLOW-V2-01`。**D-12 选「Escape 仅关闭」正是为了不把键盘用户推进其中一个。**
- **`#probe-controls` 的移除或重定位** —— 产品行为变更,v1.14 全局已裁定不进任何阶段,列为独立未来候选。
- **暗色模式 / `prefers-color-scheme`** —— v2 `TOKEN-V2-01`。
- **响应式 / 移动端断点系统、`#app { flex-direction: column }`、任何 1024px 以下的堆叠布局** —— UI-SPEC Q5 明文 Out of scope。
- **骨架屏 / spinner / 进度指示** —— 新产品功能,超出章程。
- **backlog `999.1`(`.collapse-indicator` 的 `20px`/`line-height: 1` + `check-05-ui-uat.py:588` 的陈旧诊断文案)** 与 **`999.2`(`#session-panel .panel-header` 的假 `cursor: pointer`、`.annotation-answer summary` 无交互态且普查从未见过它、焦点环 PAIR 清单漏 `--color-surface-warning-subtle`)** —— 两者各自会作废 `idi-04.1-radix` / `idi-07` 的指纹,**与本阶段合并会搅浑两批复验**;各自独立成批处理。
- **`#selection-menu` 的定位数学与 DOM 位置** —— Pitfall 8 明文:它在旗舰交互路径上且工作正常,**不得「顺手改进」**;硬规则 5 点名其必须保持 `<body>` 直接子元素。

### Reviewed Todos (not folded)
无 —— `gsd-tools query todo.match-phase 8` 返回 `todo_count: 0`,本阶段无待办匹配。

</deferred>

---

*Phase: 8-可访问性语义与键盘*
*Context gathered: 2026-09-23*
# Phase 8: 可访问性语义与键盘 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-23
**Phase:** 8-可访问性语义与键盘
**Areas discussed:** 环的承载面, 键盘划词手势, 弹窗 Escape 语义, #round-doc 的 ARIA, 回归门落点(结构性)

---

## 环的承载面

### Q1. `#round-doc` 的焦点环用哪个承载面?

| Option | Description | Selected |
|--------|-------------|----------|
| 沿用整盒环(零 CSS) | 什么都不写;`#round-doc` 继承 Phase 7 的 `[tabindex]:focus-visible`,得到左右两条贯穿全高的竖线(offset +2px,不压正文)。代价:零 CSS 改动、零指纹债务。风险:视觉形态非惯例,需运行时实测确认可辨 | ✓ |
| inset 环(改 CSS) | `#round-doc:focus-visible { outline-offset: -2px }`。环画在边框盒**内**,若 `.markdown-body` 无内边距,竖线会压在正文首字上。代价:作废 5 份 live 指纹 | |
| 环挑到 sticky 页头 | `#doc-panel:has(#round-doc:focus-visible) #doc-panel-header { outline: 2px solid var(--color-focus); outline-offset: -2px }`。信号最明确(36px 紧凑环,Phase 6 起钉在顶)。代价:作废 5 份指纹 + 引入一处 `:has()` 推导 | |

**User's choice:** 沿用整盒环(零 CSS)
**Notes:** 讨论中先用几何推翻了研究 PITFALLS 5 失效模式 4 的「只有上下边缘可见」论断 —— `#doc-panel-body` 有 `32px 40px` padding,`outline-offset: 2px` 落在父级 padding 里不被裁切,故左右竖线贯穿全高可见。这条推翻直接换来「Phase 8 零指纹债务」这个流程性质(没有任何 live 报告覆盖 `frontend/app.js` / `frontend/index.html`)。

### Q2. 若运行时实测发现整盒环不够可辨,怎么处理?

| Option | Description | Selected |
|--------|-------------|----------|
| 实测不行就当场升级 | 当场改 `style.css` 换承载面(inset 或挑到 sticky 页头),接受作废 5 份 live 指纹、连带复验 | ✓ |
| 登记为已知局限 | 写死「零 CSS 改动」;若实测不可辨则登记为具名人工验收项 + 已知局限,不当场改 | |
| 先实测再定 | 规划期先跑一次实测,把结论写进 CONTEXT/UI-SPEC 后再定(把决策推到规划之后) | |

**User's choice:** 实测不行就当场升级
**Notes:** 不把「不可辨」静默降级 —— 那会造出「名义上可聚焦、实际看不出焦点在哪」的状态,正是 Pitfall 6 的失效形态。另记录:机器半场已由 `check-05` item 10 自动覆盖(`#round-doc` 一入普查就断言计算 `outline-width`/`outline-color` 非零),所以「可辨」是纯感知半场。

---

## 键盘划词手势

### Q1. 键盘划词用哪种「提交手势」把焦点送进菜单?

| Option | Description | Selected |
|--------|-------------|----------|
| Tab 提交 | 菜单照旧自动弹出;在 `#round-doc` 里按 Tab 且菜单可见 → `preventDefault` + 焦点入菜单首按钮。直接修好路线图抱怨的那条路 | |
| Enter 提交 | 同上机制,手势是 Enter | |
| 抬起 Shift 提交 | 按住 Shift 扩选(焦点不动),**松开 Shift** 时菜单弹出并把焦点送入。单手势、最贴近自然划词节奏 | ✓ |
| Enter 才开菜单 | 键盘路径改为「Shift+方向键选 → Enter → 菜单弹出且焦点已在里面」,不再每次 keyup 自动弹 | |

**User's choice:** 抬起 Shift 提交
**Notes:** 讨论中确立了本阶段最重要的机制事实:`roundDoc.addEventListener('keyup', handleSelectionTrigger)` 对**每一次** keyup 都触发,若照路线图字面「keyup 分支把焦点移入菜单首按钮」实现,焦点会在第一次 keyup 后跳走 ⇒ 键盘用户永远只能选中一个字符,而 A11Y-03 的验收项**会照常通过**(它测状态,不测可用性)。已登记的代价:①「松开 Shift 即提交」是自造惯例;②引入一个按键白名单事实(见 Q2);③鼠标路径副作用(见 Q3)。

### Q2. `handleSelectionTrigger` 的「不做按键白名单」立场怎么办?

**User's choice:**(在 Q1 的选项描述中一并确认)白名单只发生在新增的 Shift 专用监听器里,`handleSelectionTrigger` 一字不改。
**Notes:** t8g 的既有决定原文是「不对 keyup 做按键白名单——『折叠/空白选区即关闭菜单』已让非选择类按键成为安全 no-op」(`app.js:1321-1322`)。本项刻意偏离其实质,但偏离只发生在新增监听器里。规划期必须把理由写进围栏注释,否则会被后来的读者当成违例删掉。

### Q3. 菜单项执行(批注 / 用大白话讲这段)之后,焦点要不要交还 `#round-doc`?

| Option | Description | Selected |
|--------|-------------|----------|
| 菜单项执行后也交还焦点 | 两个菜单项都会先 `hideSelectionMenu()`,而焦点当时停在一个已隐藏的按钮上 ⇒ 回落到 `<body>`,键盘用户丢失位置。这是交接的第三条腿,ROADMAP 未提 | ✓ |
| 只管进出两处 | 只在「抬起 Shift 进入」与「Escape 退出」两处交接;菜单项执行后交给浏览器/后续渲染接管 | |
| 只给不弹 prompt 的那项 | 「用大白话讲这段」交还焦点;「批注」路径交给 `window.prompt` 的后续行为 | |

**User's choice:** 菜单项执行后也交还焦点
**Notes:** 连带确立 `hideSelectionMenu()`(`app.js:1296`)是「若焦点在菜单内则交还 `#round-doc`」的**统一挂点**(四个调用点都经过它,散落必然漏),且**不得**把 `window.getSelection()` 一并清空(否则毁掉「Escape 后接着 Shift+→ 继续扩选」)。另登记两项实测义务:①焦点离开文档区后选区高亮是否保留(若被清 ⇒ 键盘用户「盲批注」);②Escape 交还焦点后能否接着扩选。

---

## 弹窗 Escape 语义

### Q1. 「两个阻塞式弹窗」到底指哪两个?

| Option | Description | Selected |
|--------|-------------|----------|
| 按路线图:confirmation + permission | 按路线图字面(`#confirmation-modal` + `#permission-modal`) | |
| 按实测:confirmation + tier | 按「键盘用户今天真的会卡住」实测重排:`#confirmation-modal` + `#tier-modal` | ✓ |
| 三个都做(突破 fence) | `#confirmation-modal` + `#permission-modal` + `#tier-modal`,突破路线图「范围锁死为这两个弹窗」的 fence | |

**User's choice:** 按实测:confirmation + tier
**Notes:** 实测依据 —— `frontend/app.js` 全文件**只有一处** `.focus()`(`app.js:488` `confirmWordInput.focus()`):`#confirmation-modal` 是**唯一已经移焦**的那个(键盘用户已能 Tab 到「拒绝」,不卡);`#permission-modal` 不移焦(弹了键盘用户不知道,但可 Tab 出去);**`#tier-modal` 不移焦且没有取消按钮 ⇒ 真正的卡死**。这与 Phase 6 A11Y-07「唯一确定不达标的是没被点名的那个」、Phase 7 D-02「路线图点名的缺陷对象是错的」三次同构。**须作为用户签核的偏差登记。**连带登记:`#permission-modal` 的「不移焦」归 v2 `A11Y-V2-02`。

### Q2. G3 确认弹窗的 Escape 语义?

| Option | Description | Selected |
|--------|-------------|----------|
| Escape = 仅关闭 | `closeConfirmModal()`,仅隐藏,不产生任何决定 | ✓ |
| Escape = 拒绝(含 prompt) | 走 `rejectAuthorization()` 的完整路径(含原生 `window.prompt` 收理由) | |
| Escape = 拒绝但不弹 prompt | 用默认理由「授权被拒,继续完善」直接建一条批注 | |

**User's choice:** Escape = 仅关闭
**Notes:** 理由:最小、零副作用;键盘用户本来就能 Tab 到「拒绝」,所以 Escape 不需要代替拒绝;而「Escape = 拒绝」会把用户直接推进一个原生 `window.prompt`(替换它是 v2 `FLOW-V2-01`,本阶段不动)。

### Q3. 档位弹窗的 Escape 语义?

| Option | Description | Selected |
|--------|-------------|----------|
| Escape = 关闭 + 允许重弹 | 关闭 + 复位 `tierModalShown = false`,使下一个自检事件能重新弹出 | ✓ |
| Escape 无操作 + 只补移焦 | 承认它是强制二选一,「不卡住」由移焦兑现;A11Y-05 / SC3 的「可 Esc 关闭」须重述 | |
| Escape = 默认选宽松 | Escape = 默认选「宽松」档并关闭 | |

**User's choice:** Escape = 关闭 + 允许重弹
**Notes:** 已核实的死状态风险:弹窗打开时立刻 `tierModalShown = true`(`app.js:638-640`),只有选档成功才隐藏(`app.js:799`)⇒ 关掉不选会让「档位未定且入口消失」。复位该标志是 1 行的解法,且保留 A11Y-05 / SC3 的「可 Esc 关闭」字面。

### Q4. 两个弹窗的 `aria-modal="true"` 怎么处理?

| Option | Description | Selected |
|--------|-------------|----------|
| 加 inert,让宣告成真 | `role="dialog"` + `aria-modal="true"` + 打开/关闭时给 `#app` 加/去原生 `inert` | ✓ |
| 只加两属性 + 登记名义部分 | 照字面加,接受 `aria-modal` 的「背景惰性」部分是名义的并显式登记 | |
| 只加 role,不加 aria-modal | 只加 `role="dialog"`,把 `aria-modal` 与焦点陷阱合并延后到 v2 `A11Y-V2-01` | |

**User's choice:** 加 inert,让宣告成真
**Notes:** 讨论中确立了判据来源:ROADMAP 的 SC3 自己要求「该宣告与实现一致」,而焦点陷阱是已裁定 Out of Scope ⇒ 只加两个属性会复现路线图警告 `role="dialog"` 时点名的同一形态(宣告一个不兑现的契约)。原生 `inert` 零依赖、零构建、约 4 行,且顺带拿到焦点陷阱的主要效果。已核实 `#app` 在 `index.html` **L155** 闭合,五个 `.overlay` 与 `#selection-menu` 都是它的兄弟 ⇒ `inert` 天然只作用于背景。**须作为用户签核的偏差登记**(超出路线图「两个属性」的字面)。

### Q5. 两个弹窗要不要无障碍名称?

| Option | Description | Selected |
|--------|-------------|----------|
| aria-labelledby 指 h3 | 给两个弹窗内的 `<h3>` 各加一个**新** id,用 `aria-labelledby` 指过去。文案只存一处 | ✓ |
| aria-label 写字面串 | 零 DOM 改动,但文案变成第二处真相来源 | |
| 不加名称 | AT 只报「dialog」不报是哪个对话框 | |

**User's choice:** aria-labelledby 指 h3
**Notes:** 已核实两个 `<h3>` 的文案是「授权确认」(`index.html:172`)/「选择自检档位」(`L186`)。硬规则 5 禁的是**改名/删除**既有 id;**新增** id 安全。

---

## #round-doc 的 ARIA

### Q1. `#round-doc` 要不要 `role` / `aria-label`?

| Option | Description | Selected |
|--------|-------------|----------|
| role=region + aria-label | 让这个 Tab 停靠点有名字,与「可聚焦必须有意义」一致 | |
| role=document + aria-label | 语义上更贴切(渲染的确实是一份 markdown 文档),但会改变 AT 的浏览模式 | |
| 都不加(保持窄切片) | 加 `tabindex="0"` 后它是裸 `<div>` 的 Tab 停靠点,AT 只报「通用容器」—— 知情接受 | ✓ |

**User's choice:** 都不加(保持窄切片)
**Notes:** 理由取自用户自己立的立场:REQUIREMENTS 的 Out of Scope 表把「完整 ARIA」排除的原话是「ARIA 服务于不带上下文到达、且看不见屏幕的用户;本工具恰好一个用户,既是作者也看得见屏幕」。`role` 与焦点陷阱等一起归 v2 `A11Y-V2-02`。

### Q2. 要不要给键盘划词加一处可发现性提示?

| Option | Description | Selected |
|--------|-------------|----------|
| 不加,登记为已知局限 | 焦点环已兑现「可聚焦」;「Shift+方向键能划词」是键盘用户的常识性预期 | ✓ |
| 复用 #rounds-hint 加一句 | 改既有元素的内容与显隐时机(属可见行为变更) | |
| 新增一处提示 | 新 UI 元素 + 新 DOM,与「唯一触碰 app.js/index.html 的阶段」的交付物清单不符 | |

**User's choice:** 不加,登记为已知局限
**Notes:** 已登记的后果:这个缺口**不会让任何门变红**,因为 A11Y-08 的人工验收由用户执行(用户当然知道步骤)。显式登记而不是假装被覆盖。

---

## 回归门落点(结构性)

### Q1. 两条 REG-02 回归门写在哪?

| Option | Description | Selected |
|--------|-------------|----------|
| 落为计划级 grep(保住零债务) | 两条断言落为计划级 `<verify>` grep 步骤 + 人工 UAT 条目,不写进 harness | ✓ |
| 写进 harness(接五份复验) | 写进 `scripts/check-05-ui-uat.py`,接受作废 5 份 live 指纹、连带复验 | |
| 折中:一条进 harness | 只把与 REG-02 直接相关的那一条写进 harness | |

**User's choice:** 落为计划级 grep(保住零债务)
**Notes:** 两条门是 `grep -c 'inline-error' frontend/style.css` 仍为 **1**、`clearInlineError` 调用点计数**只增不减**。理由:`scripts/check-05-ui-uat.py` 在 5 份 live 报告的 `covered_files` 里,写进去会让「零指纹债务」当场消失,而那五份的复验对象全是 CSS/令牌,与本次 JS/HTML 改动几乎不相干。已登记的代价:这两条不再是常驻守卫。另记录:`#round-doc` 进 item 10 普查**不需要改脚本**(普查集 `FOCUSABLE_SELECTOR` 已含 `[tabindex]`,Tab 驱动上限是 `len(data)+8` 的数据驱动值;且 p1/p12 样本里 `#round-doc` 在 `.hidden` 子视图内 ⇒ 不可见 ⇒ 被过滤排除)。

---

## Claude's Discretion

- `inert` 的挂载时机与多弹窗同时开时的成对/幂等处理。
- Escape 监听器的归属:`document` 单点(带优先级判定)vs. 各弹窗各自的监听器。
- `hideSelectionMenu()` 里「焦点在菜单内则交还 `#round-doc`」的判据形态。
- `role="dialog"` 落在 `.overlay` 还是 `.overlay-card` 上。
- Shift 提交是否额外 gate 在「菜单可见」上。
- `#selection-menu` 是否要 `tabindex="-1"`(注意它会被 item 10 的普查排除 —— 这是设计而非漏项)。
- 两个新 id 的命名(D-15)。
- 实测工具与判据的具体形态(D-02 的「可辨」、D-10 的两条选区行为、D-16 的 `inert` 焦点落点)。
- 围栏注释与代码注释的措辞与粒度(尤其 D-06 / D-14 / D-20 三处的「为什么」)。

## Deferred Ideas

- `#permission-modal` 的「弹了键盘用户不知道」—— v2 `A11Y-V2-02`。
- 焦点陷阱实现 —— v2 `A11Y-V2-01`(`inert` 只拿到主要效果)。
- 其余三个弹窗的 `role` / `aria-modal` —— v2 `A11Y-V2-02`。
- `aria-live` 在流式聊天区 / `#stream-banner` 的 `aria-live` —— v2 `A11Y-V2-03` / `A11Y-V2-04`。
- `#round-doc` 的 `role="region"` + `aria-label` —— 与 v2 `A11Y-V2-02` 合并。
- 键盘划词的可发现性提示 —— 已知局限。
- 两处 `window.prompt` 的替换 —— v2 `FLOW-V2-01`。
- `#probe-controls` 的移除或重定位 —— 独立未来候选。
- 暗色模式 / `prefers-color-scheme` —— v2 `TOKEN-V2-01`。
- 响应式 / 移动端断点系统 —— UI-SPEC Q5 明文 Out of scope。
- backlog `999.1` / `999.2` —— 各自独立成批处理(合并会搅浑两批复验)。
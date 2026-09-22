# Phase 7: 交互状态与焦点样式 - Context

**Gathered:** 2026-09-22
**Status:** Ready for planning

<domain>
## Phase Boundary

给每个交互控件补上 hover / active / disabled 的**可辨反馈**,加一条全站 `:focus-visible` 焦点环,并把过渡限定在明确允许的属性上、尊重减弱动效偏好。

**改动面:纯 `frontend/style.css` 追加。** 围栏 `:root` 内新增一个 tier-2 令牌(`--color-surface-active`,消费已声明的 `--radix-gray-4`)+ 围栏外的交互态/焦点/过渡规则。**`app.js` / `index.html` / `frontend/vendor/` 零改动**(硬规则 5;那是 Phase 8 的活)。

**本阶段的性质:纯追加。** 路线图已把这一点记为「回归风险最低」。**因此除了两处被显式裁定为「登记例外」的对象(既有的 `.event-list` 300ms 过渡),不得编辑任何既有规则的声明** —— 新过渡写成一条独立的挂载规则,新态写成新规则,不改 `button { ... }` / `input` / `select` 的基础规则体。

**明确不含:**
- 新功能、新依赖、新前端文件、构建步骤(ROADMAP 里程碑章程)
- 暗色模式 / `prefers-color-scheme`(v1.14 全局已裁定排除)
- 动效 / 动画设计体系(REQUIREMENTS Out of Scope 表:「INTERACT-02 的 120–150ms 背景/透明度过渡就是全部规格」)
- `tabindex` / ARIA / 键盘语义 / 划词焦点交接 / 两个弹窗的 Escape 与 `role="dialog"`(`Phase 8`)
- **`#round-doc` 的焦点环内嵌处理**(环落在 `#doc-panel-body` 或 `outline-offset: -2px`)—— **明确指派给 Phase 8**(见 D-06)
- 焦点陷阱实现、完整 ARIA、骨架屏 / spinner(REQUIREMENTS Out of Scope 表)
- `.collapse-indicator` 的越轨字面量(`font-size: 20px` / `line-height: 1`)—— backlog `999.1`,**不得触碰**(硬规则 5 / 05-CONTEXT D-23)
- `#selection-menu` 的 DOM 位置与定位数学(Pitfall 8 + 硬规则 5:任何 `filter`/`transform`/`opacity` 祖先都会改变其包含块)
- `#probe-controls` 的视觉重做(产品行为变更,v1.14 全局已裁定排除)

**已签核、不得重开:** S-1(间距 12 档)、S-2(14px 为一级字号档)、S-3(`#ccc`→`#8a8a8a`)、**S-4(冻结轮删除 `opacity`,改用 `filter: saturate(0.6)` + 琥珀 `box-shadow: inset`)**。04.1 原话:「all four signed off 2026-09-17; **none may be re-opened, and no one-line alternative may be executed**」。

</domain>

<decisions>
## Implementation Decisions

### 基线与契约漂移(最优先 —— 决定后面所有取值)

- **D-01:** **沿用 05-CONTEXT D-01 / 06-CONTEXT D-01 的基线口径:以磁盘 HEAD 为唯一现实基线。** 规划与执行一律以 `frontend/style.css` 的磁盘现状 + `scripts/check-05-ui-uat.py` 的断言为准;ROADMAP Phase 7 段与 `04-UI-SPEC.md` 的环色条款**仅作意图参考**。规划期必须把 D-02 的登记表逐条落实为「已由 S-4 实现」/「已被 HEAD 推翻」/「仍然成立」。**不动 `04-UI-SPEC.md` / `ROADMAP.md` 正文**(改 ROADMAP 会作废已通过的验证指纹)。 — **Reversibility:** reversible — 基线口径是读取约定,不改任何文件。

- **D-02:** **六项路线图交付物/前提被 HEAD 推翻或需重述,逐条登记。** 规划期应以本表为起点,而不是以路线图的交付物清单为起点。

  | # | 路线图/契约声称 | HEAD 实况 | 处置 |
  |---|---|---|---|
  | 1 | `.round-frozen`(0.55)会把焦点环合成到 **2.05:1** | **该 `opacity` 已由 S-4 删除**;`style.css:1085-1087` 现为 `filter: saturate(0.6)` + `box-shadow: inset 3px 0 0 var(--color-action-warning)`,注释明写「删除后正文回到 16.67:1、环回到 5.62:1」 | **已由 S-4 实现**;0.55 这一支**不存在**,路线图的 2.05 行整行作废 |
  | 2 | `.archive-mode`(0.75)合成环 → **2.73:1** | `#rounds-placeholder.archive-mode #round-doc { opacity: 0.75 }` **仍在**(`style.css:1225`)。但它**只合成 `#round-doc` 子树**;`#round-switcher` / `#btn-authorize` / `#btn-start-writing` 是它的**兄弟**,不受影响 | **仍然成立,但范围须收窄**:唯一受影响的是 `#round-doc` **内部**的可聚焦元素(即 markdown 渲染出的 `<a href>`)。且全站只剩这一个会合成焦点环的 opacity(`.annotation-answered` 0.65 与 `.tier-desc` 0.8 均已令牌化消掉) |
  | 3 | 环色 `--color-focus: #1f63bd`「declared and consumed in Phase 7」 | 该令牌**从未声明**(`:root` 围栏内 grep `--color-focus` = 0);`#1f63bd` 是 Radix 之前的 `--blue-700` | **仍然成立且必须落地**,但见 D-04:它的实测面必须**重算**(04-UI-SPEC 的 5.62/3.44 是对旧地面 `#fafafa` 算的;HEAD 地面是 `--color-surface` `#f9f9f9` / `--color-surface-page` `#fcfcfc`) |
  | 4 | 覆盖 **21 个按钮 / 8 个输入框 / 4 个下拉** | `index.html` 静态是 **21 / 4 / 3**;`app.js` 另建 2 个按钮(`:709`/`:711`)+ 1 个输入(`:701`)+ 1 个 `<summary>`(`:1152`)。**8 / 4 这两个数对不上任何口径** | **数字陈旧,走实测普查**(与 Phase 6 的 A11Y-07「21–22px」同型)。门按**元素普查**断言,不按这三个数 |
  | 5 | `:disabled`「保持明确不可点且与 `:hover` 可区分」 | **今天不成立,但对象不是路线图说的那个**。`#btn-authorize` 因 1-0-0 规则钉住填充色而**免疫**;真正会「禁用态仍响应 hover」的是 **`.verdict-buttons button`** —— `.verdict-buttons button:disabled`(`:1222`)只设 `opacity`/`cursor`,没有任何规则为它钉住 `background`,于是 `button:hover`(`:587`)照样生效 | **前提修正 + 缺陷真实**(见 D-07) |
  | 6 | 过渡「约 120–150ms」 | 全文件唯一一条是 `.event-list { transition: background-color **0.3s** }`(`:602`),**在规格外**;且它服务的是 `.streaming` / `.aborted` 两个**流式状态指示类**,不是控件态 | **在规格外,但按 D-11 保留并登记为具名例外** |

  另有一条**覆盖面的前提修正**(不构成推翻,但规划期必须用):路线图把 hover 基线记为「2」,而那是**规则数不是覆盖面**。`button:hover`(`:587`,0-1-1)被所有**填充按钮**自己的规则盖掉 —— `#btn-authorize` / `#btn-approve-draft` / `#btn-divergence` / `#btn-process-round` 是 1-0-0;`button.primary`(`:901`)/ `.overlay-card button`(`:667`)/ `#chat-input-row button`(`:883`)是 0-1-1 或更高且源码在 587 之后。**结论:今天所有有底色语义的按钮 hover 时零反馈**,只有朴素无底色按钮会变灰。 — **Reversibility:** reversible — 登记表是读取约定。

### 焦点环(A11Y-01)

- **D-03:** **环色的验证面必须包含 `.archive-mode` 的 0.75 合成。** 环色须对**三处**通过 WCAG 1.4.11 的 3:1:全不透明下的 `--color-surface-page` 与 `--color-surface`,以及 `.archive-mode` 的 0.75 合成。

  已实测(HEAD 地面,不是 04-UI-SPEC 的旧 `#fafafa`):

  | 环色候选 | `#fcfcfc`(surface-page) | `#f9f9f9`(surface) | 0.75 合成后(`#f9f9f9`) |
  |---|---|---|---|
  | `#1f63bd`(04-UI-SPEC 指定) | 5.72 | 5.57 | **3.45** ✓ |
  | `--radix-blue-11` `#0d74ce` | 4.65 | 4.53 | **3.03** ✓(余量 0.03) |
  | `--radix-blue-12` `#113264` | 12.30 | 11.99 | 5.73 ✓(视觉过重) |
  | `#2c7be5`(路线图旧值) | 4.04 | 3.93 | **2.73** ✗ |

  `--color-surface-sunken`(#f0f0f0)**不进验证面**:实测它只是 `.markdown-body code`(`:765`)与 `.badge-answered`(`:1004`)的背景,不是任何可聚焦元素的相邻地面。 — **Reversibility:** reversible — 验证面是判据约定。

- **D-04:** **`--color-focus` 取值 = `#1f63bd`,与 `:focus-visible` 规则同一次提交声明。** 理由:S-4 的签核算术(`04-UI-SPEC.md` §Sign-Off Items S-4)就是拿这个值算的 —— 「删除 `opacity` 后环回到 5.62」;换值会改变一个**已签核决策的前提**。实测在 HEAD 地面下仍是三者中余量最大的(5.57 全 / 3.45 合成)。

  **已登记的代价:`#1f63bd` 是整个颜色层里唯一不在 Radix 刻度上的值**(除 `--white` 与两个 `rgba()` 阴影)。这与 04.1 的「值必须来自 Radix 步」纪律相冲;规划期必须在围栏注释里写明「这是对已签核契约的字面遵从,不是漏改」,否则会被后来的读者当成漂移修掉。

  **不选 `--radix-blue-11`** 的理由:它在 0.75 合成下只剩 3.03:1,余量 0.03;值是确定字面量、不会飘,但后续任何一次调整都很容易把它推过线,而 S-4 的签核正是为了给这条环留出余量。**不选 `--radix-blue-12`** 的理由:它是 Radix 的高对比**文字**步,作为 2px 环视觉上接近边框而非焦点提示。 — **Reversibility:** costly — 环色是 Phase 8 的 `tabindex` 承诺与 S-4 签核算术共同依赖的量;换值要重开一份已签核契约的算术,并连带重算 `check-02` 的配对断言。

- **D-05:** **`:focus-visible` 写成枚举,不写裸通配。** 枚举集 = `check-05-ui-uat.py` 普查脚本的可聚焦集(`:1680`):`button, input, select, textarea, a[href], summary, [tabindex]`。

  ```css
  button:focus-visible,
  input:focus-visible,
  select:focus-visible,
  textarea:focus-visible,
  a[href]:focus-visible,
  summary:focus-visible,
  [tabindex]:focus-visible {
    outline: 2px solid var(--color-focus);
    outline-offset: 2px;
  }
  ```

  **为什么选枚举而不是裸 `:focus-visible`:** 与本项目在 Phase 5(`G-idi-05-1`)/ Phase 6(`overflow-wrap`)建立的同一口径 —— 影响面必须**可枚举、可对照**。裸通配在这里不是「更全」而是「不可审」:无法回答「哪些元素被覆盖了」。枚举还有一个具体好处:它与门普查的枚举**同集**,两者可以逐条对照。

  **必须用 `outline`,绝不用 `border` / `padding`:** 后者会 reflow `#probe-controls`(路线图明文);且 `outline` 不参与布局,零位移。

  **几何固定为 `2px` + `outline-offset: 2px`:** 外伸量恰为 4px,正是 Phase 6 `check-05` item 9 的 `CLEARANCE_MIN_PX = 4.0`(`:2040`)所假设的值。改几何即改那个门的阈值。 — **Reversibility:** costly — 枚举集与 `check-05` 普查脚本同集,两者必须同步;将来新增一类可聚焦元素要改两处并重算 `check-05` 参与的指纹。

- **D-06:** **枚举含 `[tabindex]`;`#round-doc` 的焦点环承载面明确指派给 Phase 8,Phase 7 不写任何针对它的规则。**

  Phase 8 会给 `#round-doc` 加 `tabindex="0"`(A11Y-02)。枚举含 `[tabindex]` 意味着届时那条全局规则会**自动**把环套到一个数千像素高的盒子上 —— 只有上下边缘可见,且落在 `.archive-mode` 的 0.75 合成里。路线图 Phase 8 的 Deliverables 已明文承接这一条:「环落在 `#doc-pane` 或采用内嵌处理(`#round-doc` 有数千像素高,整体环只露出上下边缘)」。

  **Phase 7 不写 `#round-doc:focus-visible { outline-offset: -2px }`:** `#round-doc` 今天**不可聚焦**,那会是一条**死代码**,违反本项目「不声明不被消费的东西」纪律(硬规则 5 的同一立场),且无法被运行时验证。Phase 8 加 `tabindex` 时连同它自己的规则一起落地。

  **本项必须出现在 CONTEXT 的 deferred 与 canonical_refs 里**,作为 Phase 8 的必办项 —— 否则「可聚焦但焦点不可见/不可用」会以另一种形态重现。 — **Reversibility:** reversible — 回退是 Phase 8 侧改一条规则。

### 交互态语言(INTERACT-01)

- **D-07:** **`:hover` / `:active` 一律 gate 在 `:not(:disabled)` 上。**

  ```css
  button:not(:disabled):hover { ... }
  button:not(:disabled):active { ... }
  ```

  理由:D-02 第 5 条已实测确认缺陷真实存在 —— `.verdict-buttons button:disabled` 今天会因 `button:hover` 而改变背景色。禁用态是 **G3 前提条件唯一的视觉信号**(INTERACT-02 明文),悬停时**必须零反馈**,可辨识性由 `opacity: 0.55` 独家承担。

  **不选「不 gate + 给 `:disabled` 回写背景」** 的理由:那是一条**专门用来抵消**的规则,且每个填充色族都要跟一条;gate 是一次性、单点、自解释的。

  **`#btn-authorize` 的不可逆权重必须保住:** 它是 1-0-0 且 `Phase 5` 给了它 `--color-action-irreversible*` 的深绿填充 + 白字 + 16px 字号。新增的 hover/active 不得把它拉回与例行按钮同一视觉档。 — **Reversibility:** reversible。

- **D-08:** **填充按钮的 hover 用统一的 rgba 压暗叠层:`box-shadow: inset 0 0 0 999px rgba(0,0,0,0.06)`。**

  覆盖对象(D-02 已证明它们今天零 hover 反馈):`#btn-authorize` / `#btn-approve-draft` / `#btn-divergence` / `#btn-process-round` / `#btn-start-writing` / `button.primary` / `.overlay-card button`(+ `.danger`) / `#chat-input-row button`。

  **为什么不用 `opacity`(它在 INTERACT-02 的允许列表内、可过渡):实测不可行。** `opacity` 会把**白字一起变浅**,三个色族跌破 AA 4.5:1:

  | 填充按钮 | 满不透明文字对比度 | `opacity: 0.88` 后 | rgba 叠层后 |
  |---|---|---|---|
  | primary(blue-11) | 4.77 | **3.93** ✗ | 5.27 ✓ |
  | danger(red-11) | 5.21 | 4.42 ✗ | 5.75 ✓ |
  | commit(green-11) | 4.72 | **3.81** ✗ | 5.23 ✓ |
  | irreversible(green-12) | 12.32 | 8.60 ✓ | 12.97 ✓ |

  rgba 叠层把**填充变深、文字不动**,对比度反而上升。`box-shadow` 不参与布局 ⇒ 零位移。

  **已登记的代价:①** 引入一个 `rgba()` 字面量(围栏内合法,已有 `--color-overlay-backdrop: rgba(0,0,0,0.45)` 先例);**②** `box-shadow` **不在** INTERACT-02 的过渡允许列表里 ⇒ 填充按钮的 hover 是**瞬变**(朴素按钮仍可过渡)。②是刻意的:见 D-14。

  **不选「按族开 `--color-action-*-hover` 令牌」** 的理由:实测深填充三族(blue-11 / red-11 / green-11)在 Radix 刻度上**没有更深的可用档**(blue-12 `#113264` 是近黑,跳变过大),只能靠新字面量 —— 与 04.1「值必须来自 Radix 步」的纪律冲突,且要新增 4–6 个令牌。 — **Reversibility:** reversible。

- **D-09:** **`:active` 用「同机制加深」,不引入新语汇。**

  - **朴素按钮:** 新开 `--color-surface-active: var(--radix-gray-4)`,与既有的 `--color-surface-hover: var(--radix-gray-3)`(`:184`)构成 **3 → 4 的递进**。`--radix-gray-4` **已声明**且已被 `--color-surface-user` 消费 ⇒ **零新增 primitive**(硬规则 5 只要求「与消费者同提交」,本令牌与它的 `:active` 规则同提交)。
  - **填充按钮:** 同一套 rgba 叠层机制,alpha 提到 `0.12`。
  - **不复用 `--color-surface-user`** 承载 active:那个名字说的是「用户消息背景」(Phase 5 D-18 的同一条方法论 —— 名必须说实话,04.1 的 D-03 为同类错误付过代价)。
  - **不用 `box-shadow: inset 0 1px 3px`(凹陷感):** 它会**替换**而不是叠加 hover 的叠层,按下时压暗反而消失,需要把两者合并写 —— 复杂度换不来清晰度。
  - **不用 `transform: translateY(1px)`:** 不在过渡允许列表;1px 位移在 flex 行里容易读成抖动;且 `#selection-menu` 的包含块是硬规则 5 点名的雷区(它必须保持 `<body>` 直接子元素、无 `filter`/`transform`/`opacity` 祖先)。 — **Reversibility:** reversible。

- **D-10:** **`input` 与 `select` 统一加 hover:`border-color` 加深一步;不加 `:active`。**

  文本框的「按下」无意义,故只做 hover。`border-color` 在 INTERACT-02 的过渡允许列表内,可平滑过渡。全站**没有**被禁用的 `input`/`select`(8 条 `:disabled` 规则全部是按钮),故 `:not(:disabled)` 在这里是防御性写法而非当下必需 —— 规划期须在注释里说明这一点,免得被当成冗余删掉(与 06-CONTEXT D-09 的 `min-width: 0` 同型)。 — **Reversibility:** reversible。

### 过渡(INTERACT-02)

- **D-11:** **既有的 `.event-list { transition: background-color 0.3s }` 保留 300ms,登记为具名例外。**

  理由:它服务的是 `.streaming` / `.aborted` 两个**流式状态指示类**(`:604-605`),不是控件态过渡;INTERACT-02 的 120–150ms 规格针对的是控件反馈。更重要的是 —— Phase 7 的价值主张是「纯追加、回归风险最低」,**编辑这条声明会打破该性质**(它是全文件唯一一条过渡,且服务一个已交付的视觉信号)。

  **登记要求:** 例外必须同时写进 CONTEXT(本项)、UI-SPEC 的字面量/例外清单、以及新过渡的围栏注释里(说明「全站有两个时长,300ms 那个不是控件态」)。**不得静默留下两个时长。** — **Reversibility:** reversible — 回退是把它改成 120ms(须登记为可见行为变化)。

- **D-12:** **新过渡写成一条独立的挂载规则,不改既有基础规则体。**

  ```css
  button, input, select { transition: background-color 120ms, border-color 120ms; }
  ```

  放在文件末尾。**纯追加**:不编辑 `button { ... }`(`:578`)/ `#ai-route-select` / `#project-path-input` 等既有规则。特异性 0-0-1,与 `.event-list`(0-1-0,不同元素)零竞争。

  时长取 **120ms**,在 INTERACT-02 的「约 120–150ms」区间内;缓动不显式声明(浏览器默认 `ease`)。 — **Reversibility:** reversible。

- **D-13:** **`prefers-reduced-motion` 在 `reduce` 里按选择器重写为 `none`,枚举含 `.event-list`。**

  ```css
  @media (prefers-reduced-motion: reduce) {
    button, input, select, .event-list { transition: none; }
  }
  ```

  **行业标准写法在本项目里不存在:** 通行片段是 `*, *::before, *::after { transition-duration: 0.01ms !important; ... }` —— 两个 `!important`。而本仓库的 `!important` **声明数必须恒为 1**(硬规则 2/4;唯一一条是 `.hidden { display: none !important }`,44 处 `classList` 依赖它),`check-04-important-count.sh` 会立刻变红。**规划期不得采纳任何带 `!important` 的减弱动效写法。**

  枚举**含 `.event-list`** 是刻意的:否则减弱动效用户仍会看到流式状态的 0.3s 背景淡入。

  **与 D-12 同一次提交**(硬规则:减弱动效偏好必须与任何新增 transition 一起落地)。 — **Reversibility:** reversible。

- **D-14:** **过渡属性列表不含 `opacity` —— 禁用态是瞬变的。**

  `opacity` 在 INTERACT-02 的允许列表内,故这是个**可用但刻意不用**的选择:禁用态是 G3 前提条件唯一的视觉信号,应当被**立即感知**;0.55 的淡入容易被读成「加载中」而非「不可点」;且它属于路线图警告的「平滑隐藏」家族。

  **派生结论(未提问,由 INTERACT-02 的允许列表强制):焦点环本身必须瞬变。** `outline-color` / `outline-width` 不在允许过渡的三个属性内,所以环的出现与消失是硬切。**这是正确的** —— 过渡焦点环是已知的无障碍反模式(延迟的焦点反馈)。规划期不得为「让环更柔和」而把它加进过渡列表。 — **Reversibility:** reversible。

### 验收门(本阶段的可执行契约)

- **D-15:** **门分三段,每类断言落在职责相符的已有门里。不新建脚本。**

  | 断言类别 | 落点 | 内容 |
  |---|---|---|
  | **算术比值** | `scripts/check-02-contrast.py` 的 PAIR 清单(围栏内) | 加 `/* PAIR --color-focus ON --color-surface-page NON-TEXT */`、`/* PAIR --color-focus ON --color-surface NON-TEXT */`、`/* PAIR --color-focus ON --color-surface NON-TEXT@0.75 */`。**该脚本已内建 alpha 合成**(`composite()` `:125`,PAIR 的 `@<alpha>` 后缀 `:178-196`)⇒ 零新代码即可断言 3.45 ≥ 3 |
  | **契约计数** | 新的零依赖静态断言 | `:focus-visible` 计数 > 0;**没有任何焦点规则设置 `border` 或 `padding`**;`prefers-reduced-motion` 与新增 transition 同提交;`--color-focus` 已声明且被消费 |
  | **运行时** | `scripts/check-05-ui-uat.py` 新增 item 10 | 见 D-16 / D-17 |

  **不新建 `check-06`** 的理由:该编号**已被占用**(`scripts/check-06-idi05-validation.py` 存在);且与 Phase 6「扩在既有门」的先例(D-06 / D-14)相悖,还会多出一份要连带复验的指纹。

  **不把比值断言塞进 `check-05`** 的理由:它是纯算术、对渲染零依赖,放进需要 Playwright + 五个状态样本的 harness 是职责错配,也把一个快门变成慢门。 — **Reversibility:** costly — 改 `check-02` / `check-05` 会作废它们参与的验证指纹(见 D-19)。

- **D-16:** **运行时门按「元素普查」口径断言焦点环覆盖,不按选择器计数。**

  与 Phase 6 的 D-14 同口径:枚举 `button, input, select, textarea, a[href], summary, [tabindex]` 的**全部实例**,逐个断言在 `:focus-visible` 下计算 `outline-width` / `outline-color` 非零,并断言**「未被覆盖的可聚焦元素数为 0」**。

  **为什么不按选择器计数:** 那只证明规则被写下了,不证明它覆盖了每一个可聚焦元素 —— 而「枚举会漏项」正是 D-05 选枚举路线的**已知代价**,门必须正面回答这个问题。 — **Reversibility:** costly — 与 D-15 同理。

- **D-17:** **Success Criteria 的自动化边界:SC1–SC4 全部自动化;SC5 拆两半。**

  | SC | 判据 | 自动化 |
  |---|---|---|
  | 1 键盘 Tab 到控件,环可见 | `page.keyboard.press('Tab')` 后读计算 `outline-width` / `outline-color` | ✓ 机器 |
  | 2 鼠标点击**不**出现环 | `page.click(sel)` 后读计算 `outline`(应为 UA 基线,非环) | ✓ 机器 |
  | 3 冻结轮与归档态下仍可辨认 | 冻结轮半场:**已被 S-4 结构性满足**(0.55 已删,环回到 5.57);归档半场:见 D-18 | ✓ 机器 |
  | 4 侧栏滚到底再 Tab,环不被裁切 | 复用 `check-05` item 9 的 L-5 clearance 普查(`CLEARANCE_MIN_PX = 4.0`)+ 新增 Tab 探针 | ✓ 机器 |
  | 5 交互控件有 hover/active 反馈 | 读 hover / `mouse.down()` 后的计算 `background` / `border-color` | ✓ 机器 |
  | 5′ `#btn-authorize` 禁用态**仍一眼看出不可点** | **机器半场**:禁用按钮 hover 时背景与静默时**相同**(D-07 的 gate 生效证明)+ `opacity` 仍为 0.55(未被软化) | ✓ 机器 |
  | 5″ 同上,「一眼看出」 | 这是关于**感知**的主张,不是关于数值的主张 | ⚠ **具名人工验收项**,写进 VERIFICATION 的 manual list |

  **本阶段只有 5″ 一条人工项。** 规划期不得把它删掉换成机器代理量 —— 门绿不等于视觉上真的没被软化。 — **Reversibility:** reversible。

- **D-18:** **SC3 的归档半场 = 常驻算术门 + 一次性注入探针。**

  已核实的事实:**五个状态样本(`scripts/ui-states/`)的 `#round-doc` 内 `a[href]` 计数为 0** —— `#round-doc` 是 markdown 渲染区,当前样本里没有链接,故**运行时那半场今天没有服务对象**。

  - **常驻门:** `check-02` 的 `--color-focus ON --color-surface NON-TEXT@0.75`(断言 3.45 ≥ 3)。这是算术,不需要真实渲染。
  - **一次性探针(反事实证据,不进守卫契约):** 在 `#round-doc` 里合成一个 `<a href>` 并实测环在 0.75 合成下的实际渲染值。定位与 `scripts/probe-05-resolve-color.py` 一致 —— 证明该断言**真的会失败/成立**,而不是静默空转。本项目已记录:「变异测试是唯一能证明守卫真的会失败的手段」。
  - **门里必须显式登记**「五个样本的 `#round-doc` 内 `a[href]` 计数为 0」,否则读者会把「没有断言」误读成「没有风险」。 — **Reversibility:** reversible — 探针不进守卫契约,删掉不影响任何门。

### 流程义务(本阶段必然触发,不是可选项)

- **D-19:** **本阶段会作废 `frontend/style.css` 与 `scripts/check-05-ui-uat.py` 参与的全部 live 验证指纹。**

  已按 `covered_files` 逐份核实,当前**仍在 `.planning/phases/` 下**(未归档、会被 staleness 机制消费)且覆盖这两个文件的报告有**四份**:`idi-04` / `idi-04.1-radix` / `idi-05` / `idi-06`(各自的 `covered_digest` 是原始字节 sha256)。

  **Phase 6 的 D-19 只登记了 `idi-04.1-radix` 一份,义务面比既往记录更宽。** 收口时必须**以 HEAD 内容重算指纹**,不要看 mtime(本项目已记录:stale 有两种成因 —— 「内容真变」走重新验证,「记账性编辑」走重算 + 披露,补救方向相反)。`STATE.md` 的 Operator Next Steps 第 2 条(`/gsd-verify-work idi-04.1-radix`)在 Phase 7 开始前**仍未收口**。

  ⚠ 注:`gsd-tools query verification status <phase>` 对这四份报告一律返回 `missing`(相位目录命名与工具的相位令牌解析不匹配),故**不得用该命令判定 stale**;判据只能是拿 `covered_files` 逐份比对 + 重算 digest。

  — **Reversibility:** reversible — 复验是流程义务。

- **D-20:** **本阶段会打破/触及的既有断言必须在计划里显式登记。** 至少:`check-05` item 9 的 L-5 clearance 普查(几何 `2px + offset 2px` 与 `CLEARANCE_MIN_PX = 4.0` 的绑定)、`check-02` 的配对清单(新增三条 `--color-focus` 条目)、`check-01`(围栏外裸 hex 必须仍为 0 —— 新增的 `#1f63bd` 在围栏内,合法)、`check-04`(`!important` 声明数仍为 1 —— D-13 不得引入)。规划期须先跑一遍 HEAD 上的既有门,建立「执行前基线」,再逐条登记。 — **Reversibility:** reversible。

### Claude's Discretion

- 新过渡挂载规则的具体位置与围栏注释措辞(尤其 D-11 的「两个时长」说明与 D-10 的「`input`/`select` 没有禁用态,`:not(:disabled)` 是防御性写法」)。
- `textarea` 是否进新过渡的枚举:今天全站 `<textarea>` 计数为 0;进枚举则与焦点环枚举同集(一致性),不进则严格「不声明不被消费的」。**两种都站得住,规划期裁定并写明理由。**
- D-08 的 rgba 叠层规则**怎么组织**:一条共享选择器列表,还是与各填充按钮的既有规则分组;alpha 的精确值(0.06 是实测点,可在 0.05–0.08 间微调,但须重跑文字对比度)。
- `#selection-menu button`(`:1069`,`#selection-menu button:hover` 用 `--color-surface-info` 背景)的态是否并入统一的一套:`#btn-annotate` / `#btn-plain-ask` 是浮层内控件,`--color-surface-info` 是浅蓝填充。
- D-10 的「加深一步」具体取值:`--color-border-strong`(`--radix-gray-9` `#8d8d8d`)→ 哪一档(`--radix-gray-11` `#646464`?`--radix-gray-12` `#202020`?)。须实测并登记为新配对进 `check-02`。
- 围栏注释的粒度:尤其 D-04 的「`#1f63bd` 是对已签核契约的字面遵从,不是漏改」与 D-05 的「为什么枚举而不是通配」。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 本阶段的直接上游(必须读)
- `.planning/ROADMAP.md` §Phase 7 — 本阶段的 goal / 交付物 / Success Criteria / Avoids(Pitfall 5 四种失效模式、M3 全局 transition、M5 弱化 `:disabled`、Anti-Pattern 5 `outline: none`)/ Research flag / Gates。**注意:交付物多已被 HEAD 推翻或需重述,须以 D-02 的登记表读**
- `.planning/ROADMAP.md` §Phase 8 — **本阶段的下游**,也是 D-06 的指派对象。其 Deliverables 明文承接「`#round-doc` 的环落在 `#doc-pane` 或采用内嵌处理」,并解释了「焦点规则在 Phase 7 落地、`tabindex` 在 Phase 8 落地」的调和结论
- `.planning/ROADMAP.md` §全局硬规则 1-7 — **每个计划都适用**;尤其规则 1(`.hidden` 唯一性)、规则 2(`!important` 声明数恒为 1)、规则 3(追加不重排)、规则 4(不得新增 `!important` / `@layer` / `@property` / `var(--x, #fallback)`)、规则 5(不得触碰清单)、规则 7(**每个 `style.css` 计划必须带至少一项运行时验证**)
- `.planning/REQUIREMENTS.md` §INTERACT-01 / §INTERACT-02 / §A11Y-01 — 本阶段三条需求的原文;**注意 INTERACT-01 的「基线 2 / 0 / 8」是规则数不是覆盖面,以 D-02 读**
- `.planning/REQUIREMENTS.md` §Out of Scope 表 — 「动效 / 动画设计体系」条目:「INTERACT-02 的 120–150ms 背景/透明度过渡就是全部规格」
- `.planning/STATE.md` §Operator Next Steps — S-1…S-4 签核原文(不得重开)、04.1 复验待办(D-19)、以及「UAT 环境事实」节

### 契约与签核(必须读)
- `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` §「Phase 7 consequence recorded now (not Phase 4's work)」 — **`--color-focus: #1f63bd` 的规范出处与三个比值(5.62 / 3.44 / 5.62)**。注意:这些数是对旧地面 `#fafafa` 算的,D-03 已用 HEAD 地面重算
- `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` §Sign-Off Items **S-4** — 冻结轮 route 1 vs route 2 的裁定原文,含「route 1 会把环降到 2.85:1」的实测理由。**D-04 保住其算术前提的根据**
- `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` §Deliberate Delta Ledger — 「Anything not on this list is a defect」的登记纪律
- `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` §Color / §Contrast Verification — tier-1 名、tier-2 名与计数的权威(43 → 47 对的演化)
- `.planning/phases/idi-04.1-radix/idi-04.1-CONTEXT.md` — D-03(名必须说实话)/ D-04(只声明消费到的步)/ D-13(`#doc-pane` → `#doc-panel-body`)/ D-14(断言改令牌接线表述)
- `.planning/phases/idi-05-typography-and-visual-hierarchy/05-CONTEXT.md` — **D-01(基线口径,D-01 直接沿用)** / D-23(不得触碰 `.collapse-indicator`)
- `.planning/phases/idi-06-layout-robustness/06-CONTEXT.md` — **D-01(基线口径)** / D-09(`min-width: 0` 的「防御性非冗余」注释纪律,D-10 同型)/ D-13(焦点环解裁切按元素普查)/ D-19(连带复验义务,D-19 的起点)
- `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` §L-5 — **焦点环解裁切的口径与「4px = `outline: 2px` + `outline-offset: 2px`」的绑定**,以及「零 padding 改动」的结论。**D-05 的几何由此固定**
- `.planning/phases/idi-06-layout-robustness/idi-06-VERIFICATION.md` §frontmatter `overrides:` — LAYOUT-02 的收窄登记与 `covered_files`(D-19 的清单来源)

### 代码面
- `frontend/style.css` §围栏 `:root`(L5-430)— **本阶段唯一新增令牌 `--color-surface-active` 的落点**;`--color-surface-hover`(L184)/ `--color-surface-user`(L185)/ `--color-surface`(L183)/ `--color-surface-page`(L122)/ `--radix-gray-4`(L52)/ `--radix-blue-11`(L58)/ `--radix-gray-9`(L54);PAIR 清单(L344-425)是 D-15 的扩写对象
- `frontend/style.css` §`button`(L578-587)— `padding` / `border` / `background: var(--color-surface)` / `font-size` / `font-weight` / `cursor` + **唯一一条 hover**(`button:hover { background: var(--color-surface-hover) }`,0-1-1)
- `frontend/style.css` §`.event-list`(L594-605)— **D-11 的保留对象**:`transition: background-color 0.3s` + `.streaming`(L604)/ `.aborted`(L605)两个状态类
- `frontend/style.css` §`.panel-header`(L536-545)— `cursor: pointer` 但**不可聚焦**(无 `tabindex`),故不在焦点环枚举内
- `frontend/style.css` §`.overlay-card button`(L667-675)/ §`#chat-input-row button`(L883-891)/ §`button.primary`(L901-905)— D-08 的填充按钮对象
- `frontend/style.css` §`#btn-approve-draft`(L771-779)/ §`#btn-divergence`(L785-793)/ §`#btn-process-round`(L1047-1053)/ §`#btn-authorize`(L1096-1106)/ §`#btn-start-writing`(L1111-1118)— **1-0-0 的填充按钮**:今天全部零 hover 反馈(D-02 第 7 条)
- `frontend/style.css` §`#selection-menu button`(L1064-1070)— 浮层内控件,hover 用 `--color-surface-info`
- `frontend/style.css` §`.verdict-buttons button:disabled`(L1222)/ §`.overlay-card .modal-buttons button:disabled`(L1132)/ §`#btn-continue-check, #btn-continue-repair:disabled`(L1176-1178)— **8 条 `:disabled` 规则**(`opacity: 0.55` 或 `0.5` + `cursor: not-allowed`);**L1222 是 D-02 第 5 条实测缺陷的现场**
- `frontend/style.css` §`#round-doc.round-frozen`(L1081-1087)— **S-4 的落地形态**(`filter: saturate(0.6)` + 琥珀 inset),注释逐字记录了「删除 opacity 后环回到 5.62:1」
- `frontend/style.css` §`#rounds-placeholder.archive-mode #round-doc`(L1225)— **D-03 唯一存活的合成源**(`opacity: 0.75`)
- `frontend/style.css` §`.markdown-body`(L737-757)— `#round-doc` 的渲染样式;末尾 L1227-1265 是 Phase 5 `idi-05-04` 的注入目标枚举注释(D-05 的枚举范本)
- `frontend/style.css` §`.hidden`(L441-446)— **机制而非样式,不得触碰**(硬规则 1)
- `frontend/index.html` §L82-150 — `#doc-panel` > `#doc-panel-header` + `#doc-panel-body` > `#rounds-placeholder` > **`#round-doc`(L139,可聚焦性由 Phase 8 赋予)**;`#round-switcher`(L136)/ `#authorize-row`(L142)/ `#writing-view`(L147)是 `#round-doc` 的**兄弟**,不受 0.75 合成影响(D-02 第 2 条)
- `frontend/index.html` §L22-217 — 21 个 `<button>` / 4 个 `<input>` / 3 个 `<select>` 的静态清单(D-02 第 4 条的普查起点)
- `frontend/app.js` §L701-711(`noteInput` / `fixBtn` / `keepBtn`)/ §L1150-1156(`<details>` + `<summary>`) — 动态控件,D-02 第 4 条与 D-05 枚举的完整性依据
- `scripts/check-05-ui-uat.py` — Playwright UAT harness(`--item N` 单跑);**item 9 是 Phase 6 的 L-5/L-6 普查**(`:2179` `_idi06_clearance_assert`,`:2040` `CLEARANCE_MIN_PX = 4.0`);**`:1680` 的可聚焦枚举是 D-05 的同集依据**;D-15/D-16 的扩写对象
- `scripts/check-02-contrast.py` — 对比度校验;**`:125` `composite()` 与 `:178-196` 的 `@<alpha>` 后缀是 D-15 零新代码的依据**;D-15/D-18 的扩写对象
- `scripts/check-01-token-conformance.sh` / `scripts/check-03-hidden-uniqueness.sh` / `scripts/check-04-important-count.sh` — 三条不变量守卫,**本阶段不得破坏**(尤其 D-13 不得引入 `!important`)
- `scripts/check-06-idi05-validation.py` — **编号已被占用**,是 D-15 不新建 `check-06` 的事实依据
- `scripts/probe-05-resolve-color.py` — **一次性注入探针的定位范本**(「不是门,不进守卫契约」),D-18 照此写
- `scripts/ui-states/` — p1 / p12 / p3 / checking / archive 五个磁盘状态样本,D-16/D-17 的运行时环境;**已核实其 `#round-doc` 内 `a[href]` 计数为 0**(D-18 的前提)

### 需求与状态
- `DESIGN.md` — 项目唯一权威设计文档;**已核实其全文对 hover / `:focus` / 过渡 / 键盘零提及** —— 本阶段是在**零交互态设计契约**下建立契约,与 v1.14 里程碑章程的立意一致;§3.8 是语言红线
- `.planning/PROJECT.md` §Current Milestone / §Key Decisions — 「交互状态 — hover/active/disabled/transition(现为 2/0/8/1)」的立项表述
- `.planning/REQUIREMENTS.md` §Traceability — A11Y-01 / INTERACT-01 / INTERACT-02 均为 Phase 7、状态 Pending

### 外部
- **WCAG 2.1 SC 1.4.11(Non-text Contrast, AA, ≥3:1)** —— 焦点环的达标依据。**SC 2.4.7 / 2.4.11 未采用**:本阶段不做焦点可见性的感知判据,只做环色的对比度判据(D-03)。
- **WCAG 2.1 SC 1.4.3 的「非活动组件」豁免** —— 8 处 `:disabled` 的 `opacity` 不属 AA 范围,故它们不进 `check-02` 的配对清单(A11Y-04b 已登记)。
- 无其他外部规范依赖。

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **`scripts/check-02-contrast.py` 的 alpha 合成能力**(`:125` `composite(fg, bg, alpha)` + PAIR 条目的 `@<alpha>` 后缀):**D-15 的核心杠杆** —— 环对 0.75 归档合成的比值断言零新代码。这是 04.1 的 D-14「断言改令牌接线」之后该脚本第二次免费承接新需求。
- **`scripts/check-05-ui-uat.py` 的可聚焦枚举**(`:1680`,`button, input, select, textarea, a[href], summary, [tabindex]`):**D-05 的枚举集直接取它** —— 焦点环规则与门普查同集,两者可逐条对照。
- **`scripts/check-05-ui-uat.py` item 9 的 L-5 clearance 普查**(`:2040` `CLEARANCE_MIN_PX = 4.0`):**SC4 的判据已经在盘**,Phase 7 只需保证几何 `2px + offset 2px` 不变,并补一条 Tab 探针。
- **`scripts/probe-05-resolve-color.py`**:一次性注入探针的**定位范本**(「不是门,不进守卫契约」),D-18 照此写。
- **`--radix-gray-4`**(`:52`,已被 `--color-surface-user` 消费):**D-09 的 `--color-surface-active` 零新增 primitive** 的依据。
- **`rgba()` 字面量先例**(`--color-overlay-backdrop: rgba(0, 0, 0, 0.45)`,`:196`):D-08 引入 `rgba(0,0,0,0.06)` 的合法性依据(围栏内合法,`check-01` 只统计裸 `#hex`)。

### Established Patterns
- **「与消费者同提交」纪律(硬规则 5)**:`--color-focus` 与 `:focus-visible` 规则同提交;`--color-surface-active` 与 `:active` 规则同提交。
- **「追加,不重排」(硬规则 3)**:Phase 7 的性质是**纯追加** —— 新过渡写成独立挂载规则(D-12),新态写成新规则,不改既有规则体。**唯一例外是 D-11 保留的 `.event-list` 300ms(它本来就存在,不动)**。
- **「名必须说实话」**(04.1 D-03 / Phase 5 D-18):不复用 `--color-surface-user` 承载 `:active`;不复用 `--color-action-primary` 承载环色(故 `--color-focus` 是新名)。
- **「按元素普查,不按容器名/选择器名」**(Phase 5 `G-idi-05-1` → Phase 6 D-13/D-14/D-17):D-05 的枚举、D-16 的门口径都采用它。**代价是「枚举会漏项」,故 D-16 必须正面断言「未被覆盖的可聚焦元素数为 0」。**
- **「实测驱动,不采信上游文档的论断」**(Phase 6 D-08/D-15):D-02 的六项登记、D-03 的比值重算、D-08 的 `opacity` 排除,全部以 HEAD 实测为准。
- **「防御性非冗余必须写注释」**(06-CONTEXT D-09):D-10 的 `input:not(:disabled)` 今天无服务对象,注释须说明。
- **`.hidden` 是机制而非样式**:不得令牌化、移动、弱化或用 `:where()` 降特异性。
- **环境事实(不得重新推导、不得对抗)**:截图不可用(headless 渲染被阻,SSE 长连接让 capture handler 无法退出)→ **计划用计算样式检查 + 命名人工步骤,不要计划视觉 diff**;若用 Playwright **必须** `chromium.launch({ channel: 'chrome' })`;**键盘文本选区无法自动化**(Phase 8 的 A11Y-03/A11Y-08 受此约束,Phase 7 不受)。

### Integration Points
- **唯一改动面** = `frontend/style.css`:围栏内 1 个新 tier-2 令牌 + 围栏外的新规则(D-05 / D-07 / D-08 / D-09 / D-10 / D-12 / D-13)。**围栏外裸 `#hex` 必须仍为 0**(`check-01`);`!important` 声明数必须仍为 1(`check-04`)。
- **`scripts/check-02-contrast.py`** 的 PAIR 清单加三条 `--color-focus` 条目(D-15/D-18);**`scripts/check-05-ui-uat.py`** 加 item 10(D-16/D-17)。
- **`app.js` / `index.html` / `frontend/vendor/` 零改动** —— 硬规则 5 的约 70 个顶层 `getElementById` 句柄 id 不得改名或删除;`frontend/vendor/` 保持只有 `marked.min.js`。
- **`#round-doc` 的焦点环承载面是 Phase 7 与 Phase 8 的接口**:Phase 7 的枚举含 `[tabindex]`(D-06),Phase 8 必须为它写内嵌处理。这是本阶段唯一跨阶段的开放项。
- **本阶段会打破/触及的既有断言(必须在计划里显式登记,D-20)**:`check-05` item 9 的 L-5 clearance 普查、`check-02` 的配对清单、`check-01`、`check-04`。

</code_context>

<specifics>
## Specific Ideas

- **本阶段的三个「前提已死」是最重要的事实**:0.55 的冻结轮合成**已被 S-4 删除**(路线图的 2.05 行整行作废);`--color-focus` 从未声明且其规范值是 Radix 之前的字面量;而「21/8/4」的控制数对不上任何口径。规划期应以 D-02 的登记表为起点。
- **「基线 2」是规则数不是覆盖面**:`button:hover` 被所有填充按钮自己的规则盖掉,**今天所有有底色语义的按钮 hover 时零反馈**。这是「数规则数」这种 gate 口径会漏掉、而「按元素普查」能抓到的典型例子 —— 与 Phase 5 `G-idi-05-1`、Phase 6 A11Y-07(「唯一确定不达标的是没被点名的那个」)三者同构。
- **路线图点名的缺陷对象是错的**:它说 `#btn-authorize:disabled` 会响应 hover,实测它因 1-0-0 钉住填充色而**免疫**;真正会响应的是 **`.verdict-buttons button:disabled`** —— 而裁决按钮恰是路线图 SC5 点名要保护的那个。
- **`opacity` 是本阶段「可用但刻意不用」的属性**:它在 INTERACT-02 的允许列表内,却因为会让白字跌破 AA(实测 4.77→3.93)而不可用于 hover,又因为禁用态应被立即感知而不可用于 `:disabled`。**唯一合法的 `opacity` 用途在本阶段是零。**
- **行业标准的减弱动效片段在本项目里根本不存在**:通配 + 两个 `!important` 会让 `check-04` 立刻变红。这是「项目的全局硬规则会排除行业惯例」的一个具体实例。
- **S-4 的签核算术是本阶段环色决策的锚**:选 `#1f63bd` 不是因为它在 Radix 系统内(它不在),而是因为一个**已签核决策的前提**是拿它算的。这与「值必须来自 Radix 步」的纪律相冲 —— 规划期必须在注释里写明这是**刻意的字面遵从**,否则会被后来的读者当成漂移修掉。
- **`#round-doc` 的环是本阶段唯一跨阶段的开放项**:枚举含 `[tabindex]` 是刻意的(契约「凡可聚焦必有环」无缺口),代价是 Phase 8 必须履约。这条必须出现在 deferred 与 canonical_refs 两处。
- **D-18 的诚实性**:归档半场的运行时断言**今天没有服务对象**(五个样本里 `#round-doc` 内零链接)。登记这个事实而不是假装断言覆盖了它 —— 与 Phase 6「单样本会把隐藏静默读成 clearance 0」是同一类警惕。

</specifics>

<deferred>
## Deferred Ideas

- **`#round-doc` 的焦点环内嵌处理** —— **明确指派给 Phase 8**(D-06)。Phase 8 会给 `#round-doc` 加 `tabindex="0"`,届时 Phase 7 的枚举规则会自动把环套到一个数千像素高的盒子上;路线图 Phase 8 的 Deliverables 已明文承接(「环落在 `#doc-pane` 或采用内嵌处理」)。**这是本阶段唯一跨阶段的开放项,不得静默丢掉。**
- **`check-05` 普查脚本的可聚焦集若日后新增类别,焦点环枚举须同步** —— 两者同集是 D-05 的设计,也是它的已知脆弱点;D-16 的门正面回答它(「未被覆盖的可聚焦元素数为 0」)。
- **`.collapse-indicator` 的 `font-size: 20px` / `line-height: 1` 越轨字面量** —— backlog `999.1` 第 1 项,与 `check-05-ui-uat.py:588` 的陈旧诊断文案合并为同一批处理。**本阶段不得触碰该元素**(硬规则 5 / 05-CONTEXT D-23)。
- **`:disabled` 的 8 条重复声明**(`opacity: 0.55/0.5` + `cursor: not-allowed` 各写一遍)是否收敛为一条 `button:disabled` —— 属重构而非本阶段交付物,且收敛会改变特异性(可能翻掉某条 1-0-0 的填充色),风险大于收益。
- **`#selection-menu` 的定位数学与 DOM 位置** —— Pitfall 8 明文:它在旗舰交互路径上且工作正常,**不得「顺手改进」**;硬规则 5 点名其必须保持 `<body>` 直接子元素。
- **`#probe-controls` 的视觉重做** —— 产品行为变更,v1.14 全局已裁定不进任何阶段,列为独立未来候选。
- **暗色模式 / `prefers-color-scheme`** —— v2 `TOKEN-V2-01`;会翻倍对比度校验面。
- **焦点陷阱 / 完整 ARIA / 其余弹窗的 `role`** —— REQUIREMENTS Out of Scope 表(用户已裁定取窄切片)。
- **`tabindex` / ARIA / 键盘语义 / 划词焦点交接 / 两个弹窗的 Escape 与 `role="dialog"`** —— Phase 8。**本阶段不触碰 `app.js` / `index.html`。**
- **响应式 / 移动端断点系统、`#app { flex-direction: column }`、任何 1024px 以下的堆叠布局** —— UI-SPEC Q5 明文 Out of scope。
- **骨架屏 / spinner / 进度指示** —— 新产品功能,超出章程。

### Reviewed Todos (not folded)
无 —— `gsd-tools query todo.match-phase 7` 返回 `todo_count: 0`,本阶段无待办匹配。

</deferred>

---

*Phase: 7-交互状态与焦点样式*
*Context gathered: 2026-09-22*
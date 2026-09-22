# Phase 6: 布局稳健性 - Context

**Gathered:** 2026-09-22
**Status:** Ready for planning

<domain>
## Phase Boundary

让布局结构本身站得住:状态徽标不再与断流横幅打架、不再遮挡正文;窄窗口不破版;面板区滚动容器收敛;紧凑交互控件达到 24×24 命中区。

**改动面:纯 `frontend/style.css`** —— 围栏 `:root` 内零新增声明(本阶段不新增任何令牌)+ 围栏外的布局/换行/定位规则。**`app.js` / `index.html` / `frontend/vendor/` 零改动**(本里程碑只有 Phase 8 触碰前两者)。

**本阶段的性质与 Phase 5 不同:** Phase 5 是「新增规则」,本阶段是**结构性 diff**——它改动的是既有布局规则的声明,而非追加。路线图已把这一点记为「回归风险最高的 CSS 阶段」。因此每个计划都必须显式登记它打破的既有断言。

**明确不含:**
- 新功能、新依赖、新前端文件、构建步骤(ROADMAP 里程碑章程)
- 暗色模式 / `prefers-color-scheme`(v1.14 全局已裁定排除)
- 响应式/移动端断点系统、`#app { flex-direction: column }`、任何堆叠布局(UI-SPEC Q5「Out of scope」;LAYOUT-02 只承诺「不破版」而非「适配」)
- 焦点样式本身(`A11Y-01`,Phase 7)——本阶段只为它**解裁切**,不写任何 `:focus` 规则
- hover / active / transition 态(`INTERACT-01` / `INTERACT-02`,Phase 7)
- `tabindex` / ARIA / 键盘语义(`Phase 8`)
- 图标库 / SVG sprite 体系 / 图标字体(REQUIREMENTS Out of Scope 表)
- `.collapse-indicator` 的越轨字面量(`font-size: 20px` / `line-height: 1`)——已裁定为 backlog `999.1`,**不得触碰**(硬规则 5 / 05-CONTEXT D-23)
- `#selection-menu` 的定位数学——它在旗舰交互路径上且工作正常,**不得「顺手改进」**(Pitfall 8)

**已签核、不得重开:** S-1(间距 12 档)、S-2(14px 为一级字号档)、S-3(`#ccc`→`#8a8a8a`)、S-4(冻结轮 route 2)、04.1 的 S-5/S-6。04.1 原话:「all four signed off 2026-09-17; **none may be re-opened, and no one-line alternative may be executed**」。

</domain>

<decisions>
## Implementation Decisions

### 基线与契约漂移(最优先 —— 决定后面所有取值)

- **D-01:** **沿用 05-CONTEXT D-01 的基线口径,并把它从「值」扩展到「结构决策」:以磁盘 HEAD 为唯一现实基线。** 规划与执行一律以 `frontend/style.css` 的磁盘现状 + `scripts/check-05-ui-uat.py` 的断言为准;ROADMAP Phase 6 段、`04-UI-SPEC.md` 的 Q5/Q6 与 `## UI Considerations` **仅作意图参考**。规划期必须把下面「契约漂移清单」逐条登记为「已由 qrq 实现」或「已由 qrq 推翻」或「仍然成立」。**不动 `04-UI-SPEC.md` / `ROADMAP.md` 正文**(改 ROADMAP 会作废已通过的验证指纹)。 — **Reversibility:** reversible — 基线口径是读取约定,不改任何文件。

- **D-02:** **六项路线图交付物被 HEAD 推翻,逐条登记。** 这是本阶段最重要的一个事实:**路线图 Phase 6 的核心交付物几乎全部需要重新表述**,而非「还没做」。六条如下(逐条均已核实到行):

  | # | 路线图/契约声称 | HEAD 实况 | 处置 |
  |---|---|---|---|
  | 1 | `#state-badge { right: 448px }`(LAYOUT-01 的对象) | **该声明不存在**;badge 是 `#doc-panel-header` 内的流内元素,无 `position`、无 `right` | 已由 qrq 实现(见 D-03) |
  | 2 | LAYOUT-03:「badge 是 `position: fixed` + 不透明背景,正文从其底下穿过被挡」 | badge 不再是 fixed ⇒ **结构上不可能遮挡正文** | 已由 qrq 实现 |
  | 3 | Pitfall M2:1280px 重叠 48px / 1024px 重叠 90px | 该算术基于 fixed badge;横幅仍是 `position:fixed; top:12px; left:50%` 居中 | 已由 qrq 实现(残余碰撞实测不存在,见 D-06) |
  | 4 | 「`#session-panel { min-height: 320px }` 改 `flex: 0 0 auto`」 | HEAD 是 `min-height: 200px` + `flex: 1 1 auto`,且**执行该交付物会造成回归** | **已由 qrq 推翻**(见 D-12) |
  | 5 | A11Y-07 边界:「裁决按钮(实测约 **21–22px** 高)」 | 按 `font-size: 14px` + `padding: 4px 10px` + `border: 1px` + `line-height: normal` 算,盒高约 **26–30px**;21–22px 需 line-height ≈ 0.8×14,不可得 | 数字陈旧,走实测(见 D-15) |
  | 6 | A11Y-07 边界:「裁决按钮是为在 **420px 侧栏**塞下 **3 个**而故意紧凑的」 | 420px 侧栏不存在(`--doc-panel-w: clamp(340px,30vw,480px)`);按钮现为 **2 个**(`app.js:709-711` 只建 `fixBtn` / `keepBtn`) | fence 随前提失效(见 D-18) |

  另有两条**前提值漂移**(不构成推翻,但规划期必须用 HEAD 值):`--sidebar-w: 420px` 与 `#sidebar` 均不存在(是 `--doc-panel-w` 与 `#doc-panel`);`#doc-pane` 不存在(04.1 D-13 已登记改名为 `#doc-panel-body`)。 — **Reversibility:** reversible — 登记表是读取约定。

### 徽标收口(LAYOUT-01 / LAYOUT-03 / Pitfall M2)

- **D-03:** **接受 HEAD 的流内机制,并用 `position: sticky` 把「恒可见」补回来。** qrq 已把 `#state-badge` 改成 `#doc-panel-header` 内的流内元素,一次性消掉了 LAYOUT-01 的魔法数、LAYOUT-03 的遮挡、M2 碰撞的主因。但 HEAD 引入两条**已核实**的代价:

  1. **滚动即丢失状态读数**——`#doc-panel { overflow-y: auto }` 且全文件 `position: sticky` 数量 = **0**,故 `#doc-panel-header` 会随面板内容滚走,**连折叠指示符一起**。这正是 `04-UI-SPEC.md` Q6 反对 `position: absolute` 时给出的理由原话:「`#doc-pane` has `overflow-y: auto`, so the badge would scroll away — a behaviour change to a shipped element」。**该理由对 HEAD 同样成立。**
  2. **折叠态彻底无状态读数**——`style.css:485` `#doc-panel.collapsed #state-badge { display: none }`。

  契约侧被推翻的文本:`04-UI-SPEC.md` Q6「**`calc()`. Committed.**」与 Pitfall 8「the fix must not move the badge into normal flow」;`style.css:668-669` 留有 qrq 的逐字反驳注释:「改用 calc() 只是把一个魔法数换成另一个耦合,面板收起时还会失真」。**采纳 qrq 的理由,撤销契约 Q6 与 Pitfall 8 的该条禁令。** — **Reversibility:** costly — 回退到 `fixed` + `calc()` 会重新引入 LAYOUT-03 的遮挡与 M2 碰撞,并要重开一份已签核的 UI-SPEC 决策;`--doc-panel-w` 现在是 `clamp()`,calc() 版本在面板收起时仍会失真。

- **D-04:** **折叠态保持 `display: none`,登记为「有意设计」而非缺口。** 理由:可折叠面板的语义就是用户**主动**让出空间;48px 竖条(`--doc-panel-w-collapsed: 48px`)要容纳折叠指示符,badge 的 pill 形态放不下。与 M2 性质不同——横幅盖住 badge 是**非自愿**丢失读数(路线图判为缺陷),折叠是用户主动选择。**本阶段只修 D-03 的第 1 条(非自愿丢失),不碰折叠态。** — **Reversibility:** reversible。

- **D-05:** **sticky 只加在 `#doc-panel-header` 一个选择器上,并必须补背景。** 落法:`position: sticky; top: 0; background: var(--color-surface);`

  - **背景是必需的,不是可选:** `.panel-header` 规则里**没有任何 `background` 声明**(只有 `display` / `justify-content` / `align-items` / `height: 36px` / `padding` / `border-radius` / `cursor` / `user-select`),sticky 之后面板正文会从标题行底下穿过去。`#doc-panel` 自身的背景就是 `var(--color-surface)`(`style.css:476`),该令牌**已被消费**——本阶段**零新增令牌**,不违反硬规则 5。
  - **不加 `z-index`:** sticky 元素是 positioned,默认就画在静态内容之上。实测若有穿透再补(届时须注意 TOKEN-07 断言的 `--z-badge 10 < --z-banner 20 < --z-overlay 100 < --z-selection-menu 200` 序关系,新增 `--z-*` 要连带登记)。
  - **不选「`#doc-panel` 改 `overflow: hidden` + `#doc-panel-body` 单独滚」的理由:** 那会改变 LAYOUT-04 要统计的滚动容器数(见 D-14),须与那一区一并裁定;且它把标题行移出滚动容器,是对既有结构的更大改动。
  - 待处理细节:`.panel-header` 有 `border-radius: var(--radius-md)`,sticky + 背景后圆角处可能有内容从四角露出,需实测微调。

  — **Reversibility:** reversible — 回退是删三条声明。

- **D-06:** **徽标收口的门扩到 `scripts/check-05-ui-uat.py`,断言三件事:**
  1. `#state-badge` 是流内元素(计算 `position` 为 `static` / 无 `right` 声明);
  2. **768 / 1024 / 1280 三处** `#state-badge` 与 `#stream-banner` 的 `getBoundingClientRect()` 不相交;
  3. 滚动 `#doc-panel` 到底后 `#doc-panel-header` 仍可见(sticky 生效)。

  第 2 条**必须补上 768px**——路线图 Success Criterion #2 原本只在 1024/1280 两处实检,而 768 是承诺的窄窗口下限。**残余碰撞经核实不存在:** `showStreamBanner` 文案「事件流已断开,正在自动重连……」15 字 × 12px + 24px padding + 2px border ≈ 206px,居中于视口;badge 最宽文案「待选自检档(阶段 5)」9 字 ≈ 132px,在文档面板标题行右端;相交条件是 `banner宽 > 视口宽 - 284`,代入 206px 得**视口 < 490px**,远低于 768px 下限。 — **Reversibility:** costly — 断言写进 `check-05-ui-uat.py` 后,回退要同时改断言并重算该脚本自身参与的指纹;且本阶段已因改 `style.css` 触发 `idi-04.1-radix` 指纹失效(见 D-19),门再改会叠加一层。

### 窄窗口守卫(LAYOUT-02)

- **D-07:** **`overflow-wrap: anywhere` 枚举全部六个 `renderMarkdown()` 注入目标。** 六目标 = `.markdown-body`(宿主:`#doc-panel-body` 与 `#latest-check`)+ 五个**非** `.markdown-body` 容器:`.event-content` / `.chat-bubble` / `.say-chunk` / `.annotation-note` / `.annotation-answer-body`。该枚举**已由 Phase 5 的缺口闭合计划 `idi-05-04` 建立**(`style.css` 末尾注释 + `check-05-ui-uat.py` 的 `MARKDOWN_TARGETS` 与调用点普查守卫),直接沿用。

  HEAD 换行保护现状(已逐条核实):`.event-content` 有 `word-break: break-all` + `white-space: pre-wrap`(日志用,**已裁定,不动**);`.chat-bubble` 有 `word-break: break-word`;**其余四处零保护**;`overflow-wrap` 在全文件**零命中**。

  **必须用 `anywhere` 而不是 `break-word`**:按 CSS Text 3,只有 `anywhere` 参与 min-content 内在尺寸计算,`break-word` 不参与——这是 D-09 能成立的前提。**不写通配规则**的理由:那会波及已裁定的 `.event-content { break-all }`,并把「哪些容器受影响」重新变成不可枚举——正是 Phase 5 注释里明写要避免的失败模式。 — **Reversibility:** reversible — 回退是删声明;但门的枚举普查须一并回退。

- **D-08:** **`@media` 窄窗口守卫走「实测驱动」,不预设它必须存在。** 规划期在 **1440 / 1024 / 768** 三处量:`document.documentElement.scrollWidth > clientWidth`(横向溢出)与关键元素 rect 相交(遮挡)。

  - **只在实测出破版处写守卫**;若实测无破版,**不写** `@media`,并把契约要求的这条交付物登记为「被实测推翻」。
  - 背景:`--doc-panel-w: clamp(340px, 30vw, 480px)` **本身已是视口自适应**(1024px 时 30vw=307 被夹到 340px 下限;768px 时 30vw=230 同样夹到 340px,占 44%,主区剩 428px)。路线图把守卫范围定死为「**不破版**」而非「适配」,判据是「无横向溢出、无内容被遮挡」。
  - 分析(未实测):横向溢出的**真因是不可断长内容撑破 flex 项**(即 D-09 的 `min-width: 0` 缺失),而不是面板宽度占比;428px 的主区列**窄但不是破版**。故 D-07 + D-09 落地后,LAYOUT-02 可能已被满足。

  — **Reversibility:** reversible。

- **D-09:** **`min-width: 0` 加在 `#app` 的**两个** flex 子项上:`#main-pane` 与 `#doc-panel`。**

  `#app { display: flex }` 的两个子项 `#main-pane { flex: 1 1 auto }` 与 `#doc-panel { flex: 0 0 var(--doc-panel-w) }` 都是 `min-width: auto`。**`flex-basis` 不是硬约束——`min-width: auto` 胜出**,所以长不可断内容能把 `#doc-panel` 顶得比它的 `clamp()` 还宽,不只是撑破主区。路线图写的 `#doc-pane { min-width: 0 }` 指向一个不存在的选择器,真正的落点是这两个。

  **为什么不只靠 D-07:** 理论上六处 `anywhere` 落地后这些子树的 min-content 会塌缩,`min-width: auto` 自然失效,两条声明看似冗余。选两处都加是因为它**不依赖「六个目标全覆盖」长期成立**——将来新增一个未被 `overflow-wrap` 覆盖的渲染容器时仍能兜住。**注释必须写清为什么在 `anywhere` 已生效时它不是冗余。** — **Reversibility:** reversible。

- **D-10:** **断点字面量例外「条件声明」。** 仅在实际写出 `@media` 时,于该段首的围栏注释里声明该例外(理由:CSS 禁止在媒体查询条件中使用 `var()`,该规则会被静默丢弃),并同步登记进 `idi-06-UI-SPEC.md` 的字面量例外清单。实测无破版则不声明、不落地。

  已核实两点:断点是**非 hex 字面量**,`scripts/check-01-token-conformance.sh` 只统计裸 `#hex`,不会触发门(与已登记的旧 `448px` 同理);硬规则 4 禁止 `var(--x, #fallback)`,所以「用带 fallback 的 var 绕过」这条路本就被堵死。 — **Reversibility:** reversible。

### 滚动容器收敛(LAYOUT-04)

- **D-11:** **删 `#ai-events`(即 `.event-list`,55vh)与 `#annotation-list`(32vh)的 `max-height` + `overflow-y`;保留 `#latest-check` 的 30vh 滚动。**

  DOM 已核实:`#app` > `main#main-pane`(四个 `section`:`#session-panel` / `#annotations-panel` / `#checks-panel` / `#ai-panel`)+ `aside#doc-panel`。面板区内滚动容器分布:`#main-pane`(`overflow-y: auto`,唯一外层滚动者)/ `#ai-events` 55vh / `#annotation-list` 32vh / `#latest-check` 30vh / `#chat-messages`(`flex: 1` + `min-height: 160px`,保留)。路线图基线写的 40vh 那只**已不存在**,故基线从「4 个」修正为「3 个嵌套 + 1 个外层」。

  **保留 `#latest-check` 的理由:** 它下方就是 `#check-controls`,而**裁决按钮(`#verdict-cards` 的「修」/「接受现状」)是交互面**。去掉限高后,长自检报告会把按钮推到视口之外,必须滚动才能操作——那是**把交互面推到折叠线以下**。

  **已接受的代价:Success Criterion #3 必须登记偏离。** 路线图写「侧栏内只剩一个滚动条(`#chat-messages` 除外)」;本阶段的实际目标状态是**面板区内恰好两个滚动者:`#main-pane` + `#latest-check`**。 — **Reversibility:** reversible — 回退要把 SC#3 的偏离登记与门一并改回,并重算可达性。

- **D-12:** **`#session-panel` 零改动,路线图「改 `flex: 0 0 auto`」登记为「被 HEAD 推翻 + 执行会造成回归」。**

  已核实 HEAD:`#session-panel { flex: 1 1 auto; min-height: 200px }` + `.panel-body { flex: 1; min-height: 0 }` + `#chat-messages { flex: 1; min-height: 160px; overflow-y: auto }`,`#chat-input-row` 是 `.panel-body` 的**最后一个子元素**。这正是 `style.css:781-782` 注释写的设计:「消息区吃掉剩余高度,输入行自然贴底(不再吊在半空)」——**输入行现在就是钉在视口底部的**。

  改成 `flex: 0 0 auto` 会让面板按内容定高,`#chat-messages { flex: 1 }` 没有可分配空间 → 随消息无限增高 → 输入行落到视口之外。**该交付物与路线图自己的「输入行必须钉底」互相矛盾。** 另:`min-height: 200px` **不是死代码**——空态下 `#chat-messages` 的 `min-height` 被 `:has(:empty)` 规则置 0,面板自身的 200px 是居中问候语唯一的空间来源,故**不得删除**(否则会改变空态渲染)。 — **Reversibility:** reversible。

- **D-13:** **焦点环解裁切按「可聚焦元素」枚举,不按容器名。** 门按元素普查,而非按路线图点名的容器。

  已核实:
  - `#annotation-list` **确有可聚焦后代**——`app.js:1150-1154` 把 AI 答复渲染成 `<details>` + `<summary>`,而 `<summary>` 默认可聚焦 → **抬 padding 确有作用**;
  - `#chat-messages` **没有任何可聚焦后代**——气泡是 `div`(`app.js:260-262`)与 `p`(`app.js:282`),无 `button`、无 `details`/`summary` → 抬它的 padding 在 HEAD 上是**空动作**;
  - 路线图 Phase 7 段自己写了**三个**裁切容器(`#chat-messages` 2px、`#annotation-list` 2px、`#sidebar` **0**),但 `#sidebar` 不存在;真正 0 padding 且 `overflow-y: auto` 的是 **`#main-pane`** 与 **`#doc-panel`**。**路线图内部不一致**:Phase 6 只抬两个,第三个既没抬也没改名。

  HEAD padding 现状:`#chat-messages { padding: var(--space-1) var(--space-half) }` = `4px 2px`;`#annotation-list { padding: var(--space-half) }` = `2px`。**具体哪些容器需要抬、抬到多少,由规划期的普查结论定**;`#main-pane` / `#doc-panel` 若需抬,须注意前者会移动其居中布局下的 section 位置、后者会与既有的 `#doc-panel-body { padding: 32px 40px }` 叠加。 — **Reversibility:** reversible。

- **D-14:** **LAYOUT-04 的门扩到 `scripts/check-05-ui-uat.py`,断言三件事:**
  1. 面板区内计算 `overflow` != `visible` 的滚动容器**恰好两个**(`#main-pane` + `#latest-check`)——按 **DOM 普查**而非硬编码选择器;
  2. 两者都能滚到底(内容可达性);
  3. `#ai-events` / `#annotation-list` 的计算 `max-height` 为 `none`。

  口径取「恰好两个」而非「至多两个」,以便抓到「意外新增第三个滚动者」这类回归。 — **Reversibility:** costly — 与 D-06 同理:断言写进 `check-05` 后回退要改断言并重算指纹。

### 紧凑控件命中区(A11Y-07)

- **D-15:** **A11Y-07 走「实测驱动」判定。** 规划期用 Playwright 量每个候选控件的 `getBoundingClientRect()`;若已 ≥24×24 则登记该交付物为「被 HEAD 推翻」,**零 CSS 改动**;若不足则按 D-16 补。

  理由:路线图写的「实测约 21–22px 高」与 HEAD 对不上。按 `font-size: var(--text-base)` = 14px、`padding: var(--space-1) var(--space-2-5)` = 4px 10px、`border: 1px solid`、`line-height` 取 UA 默认 `normal`(`html, body` **没有** `line-height` 声明)算,盒高 = `line-height + 10` ≈ **26–30px**;要得到 21–22px 需 line-height ≈ 11–12px(即 0.8×14),不可得。**字体度量必须实测,不能靠算。** — **Reversibility:** reversible。

- **D-16:** **机制用 `min-height: 24px` + `min-width: 24px`。** 不动现有 `padding`(4px 10px),只抬下限:对已达标的控件**零影响**,对不足的只补差额。不选「抬 padding」(改的是外观而非命中区,且连锁影响行高与相邻间距观感);不选「`::after` 撑开命中区」(`.verdict-buttons { gap: var(--space-2) }` = 8px,扩展后的相邻命中区会**互相重叠**,反而可能违反 WCAG 2.5.8 的「不与他者相交」要求)。 — **Reversibility:** reversible。

- **D-17:** **范围按「可交互元素」普查枚举,只对实测未达标者施加。** 已枚举(逐条核实):

  | 控件 | 盒高 | 判定 |
  |---|---|---|
  | 所有 `<button>`(`button { padding: 6px 10px }` + border) | ≈ line-height + 14 ≈ **30–34px** | ✓ |
  | `#selection-menu button`(`#btn-annotate` / `#btn-plain-ask`) | 同上 ≈ **30px** | ✓ |
  | `.verdict-buttons button`(padding 覆盖为 4px 10px) | ≈ **26–30px** | 待实测,很可能已达标 |
  | **`.annotation-answer summary`** | **`font-size: var(--text-xs)` = 12px,无 padding、无 min-height** → ≈ **14–17px** | ✗ **确定不达标** |
  | `.collapse-indicator` | `<span>`,属**不得触碰**;其可点父级 `.panel-header` 为 36px | ✓(父级达标) |

  **即:REQUIREMENTS 点名的裁决按钮很可能本来就达标,而唯一确定不达标的是 `.annotation-answer summary`**(`<details>` 的展开控件)——它正是「等紧凑控件」里那个「等」所指,却未被点名。**注意:给 `summary` 加 `min-height` 会改变 `.annotation-item` 的高度,属一次视觉变更,须在计划里显式登记。** — **Reversibility:** reversible。

- **D-18:** **「若与布局冲突,不得为此重构侧栏」这条 fence 随前提失效。** fence 的前提**两处都已不成立**:420px 侧栏不存在(现为 `--doc-panel-w: clamp(340px,30vw,480px)`,且裁决卡在 `#checks-panel` 里、内容列 `max-width: 768px`),按钮数量也已从 3 个变成 2 个(`app.js:709-711`)。fence 的**实质**(不为命中区去重构侧栏)保留为一般原则,但**不再构成对本阶段的具体约束**。 — **Reversibility:** reversible。

### 流程义务(本阶段必然触发,不是可选项)

- **D-19:** **`frontend/style.css` 的任何编辑都会作废 `idi-04.1-radix` 的 `passed` 指纹**(其 `covered_files` 含 `style.css` 与 `scripts/check-05-ui-uat.py`,digest 为原始字节 sha256)。本阶段**必然**编辑 `style.css`(D-03 / D-07 / D-09 / D-11 / D-13 / D-16 / D-17)且**必然**编辑 `check-05-ui-uat.py`(D-06 / D-14),故必须**连带复验 04.1**。

  ⚠ **本义务当前尚未收口**:STATE.md 的 Operator Next Steps 第 2 条(`/gsd-verify-work idi-04.1-radix`)仍为待办,`idi-04.1-VERIFICATION.md` 一字未改。Phase 6 会在其上**再叠一层**——收口时应以 HEAD 内容重算指纹,不要看 mtime。 — **Reversibility:** reversible — 复验是流程义务。

- **D-20:** **本阶段会打破的既有断言必须在计划里显式登记。** 至少:`check-05-ui-uat.py` 中与 `#chat-messages` / `#annotation-list` / `#latest-check` 的 `max-height` / `overflow` 相关的条目(若存在)、与 `#session-panel` 相关的条目、以及 Success Criterion #3 的表述。规划期须先跑一遍 HEAD 上的既有门,建立「执行前基线」,再逐条登记打破项。 — **Reversibility:** reversible。

### Claude's Discretion

- `#doc-panel-header` 的 `border-radius: var(--radius-md)` 在 sticky + 背景下的处置(保留、改 `0`、或只圆下缘)。
- 六处 `overflow-wrap: anywhere` 的**声明组织方式**(合并成一条选择器列表、还是按容器分组)。
- D-13 的普查结论:**具体哪些容器需要抬 padding、抬到多少**(`--space-half` 2px → `--space-1` 4px,或别的档)。
- D-08 实测的**具体工具与判据**(Playwright 量 `scrollWidth` vs DevTools 计算样式;「遮挡」的精确定义)。
- 围栏外注释的措辞与粒度(尤其 D-03 的「为什么采纳 qrq 而非契约 Q6」与 D-09 的「为什么 `min-width: 0` 不是冗余」)。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 本阶段的直接上游(必须读)
- `.planning/ROADMAP.md` §Phase 6 — 本阶段的 goal / 交付物 / Success Criteria / Pitfalls M2 / 3 / 8 / Anti-Pattern 3 / Research flag / Gates。**注意:其交付物多已被 HEAD 推翻,须以 D-02 的登记表读**
- `.planning/ROADMAP.md` §全局硬规则 1-7 — **每个计划都适用**;尤其规则 1(`.hidden` 唯一性)、规则 3(追加不重排)、规则 4(不得引入 `@layer` / `@property` / `var(--x, #fallback)`)、规则 5(不得触碰清单)、规则 7(**每个 `style.css` 计划必须带至少一项运行时验证**)
- `.planning/ROADMAP.md` §Phase 7 — **本阶段的下游**。它记录了「焦点环会被容器的 padding 裁切(`#chat-messages` 2px、`#annotation-list` 2px、`#sidebar` 0)」,其中 `#sidebar` 在 HEAD 上不存在 —— 该条内部不一致是 D-13 的起因,规划期须一并读
- `.planning/REQUIREMENTS.md` §LAYOUT(01-04)/ §A11Y-07 — 本阶段 5 条需求的原文;**注意 A11Y-07 的两处边界前提(21–22px / 420px 侧栏 3 个按钮)均已失效,以 D-02 的登记表读**
- `.planning/STATE.md` §Operator Next Steps — D-19 的未收口义务(`/gsd-verify-work idi-04.1-radix`)与 S-1…S-4 签核原文(不得重开)

### 契约与漂移(必须读)
- `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` §Q5 — 窄窗口范围(「**Does not break.** Not "adapts."」+ 断点字面量例外 + `--sidebar-w: 420px` 的原始设计)。**其 `--sidebar-w` 部分已被 qrq 推翻**
- `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` §Q6 — `#state-badge` 的 `calc()` vs `absolute` 取舍。**「`calc()`. Committed.」整条已被 qrq 推翻,D-03 是采纳 qrq 理由的裁定**
- `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` §UI Considerations — **13 条 `overflow` 延后项(E2–E14)的原始信号**,「Deferred rather than dismissed so Phase 6 planning inherits the signal」。**注意:04.1 的 probe 已取代而非继承这些处置**
- `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` §The Four Contract-Check Commands / §Sign-Off Items / §Do-Not-Touch List / §Global Hard Rules
- `.planning/phases/idi-04-tokens-contract/idi-04-VERIFICATION.md` §frontmatter `overrides:` — 用户裁定把 `.collapse-indicator` 越轨项指派到 backlog `999.1`
- `.planning/phases/idi-04.1-radix/idi-04.1-CONTEXT.md` — D-02(tier-2 名冻结)/ D-04(只声明消费到的步)/ D-13(`#doc-pane` → `#doc-panel-body`)/ D-14(断言改令牌接线表述)
- `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` — Color 与 Contrast Verification 两节的权威(tier-1 名、tier-2 名与计数)
- `.planning/phases/idi-05-typography-and-visual-hierarchy/05-CONTEXT.md` — **D-01(基线口径,D-01 直接沿用)**/ D-02 / D-03(断言分类)/ D-05(连带复验义务,D-19 同源)/ D-23(不得触碰 `.collapse-indicator`)
- `.planning/phases/idi-05-typography-and-visual-hierarchy/05-CONTEXT.md` §deferred — 「UI Considerations 的 13 条 `overflow` 延后项 —— Phase 6(LAYOUT-02/03);04.1 的 probe 已**取代**而非继承这些处置」

### 代码面
- `frontend/style.css` §`#app` / `#main-pane` / `#doc-panel`(L447-482)—— D-09 的落点;`#main-pane { flex: 1 1 auto; overflow-y: auto; align-items: center }`,`#doc-panel { flex: 0 0 var(--doc-panel-w); overflow-y: auto }`
- `frontend/style.css` §围栏 `:root`(L5-343)—— **本阶段零新增令牌**;`--doc-panel-w`(L228)/ `--doc-panel-w-collapsed`(L229)/ `--z-*` 序关系(L269-275)
- `frontend/style.css` §间距刻度(L211-222)—— `--space-half: 2px` / `--space-1: 4px` / `--space-1-5: 6px` / `--space-2-5: 10px`,D-13 与 D-16 的取值来源
- `frontend/style.css` §`.panel-header`(L529-537)—— **无 `background` 声明**,是 D-05 必须补背景的原因
- `frontend/style.css` §`.event-list`(L566-576,`max-height: 55vh`)/ §`#annotation-list`(L914-919,`max-height: 32vh`)/ §`#latest-check`(L1114-1122,`max-height: 30vh`)—— D-11 的删改对象
- `frontend/style.css` §`#session-panel` 族(L783-811)—— D-12 的零改动对象,含 `:has(:empty)` 空态规则
- `frontend/style.css` §`#chat-messages`(L791-799,`padding: var(--space-1) var(--space-half)`)—— D-13 的普查对象
- `frontend/style.css` §`#state-badge`(L671-679)—— **流内元素,无 `position` / `right`**;L668-669 是 qrq 的反驳注释
- `frontend/style.css` §`#doc-panel.collapsed`(L478-485)—— 含 `#state-badge { display: none }`(D-04 的登记对象)
- `frontend/style.css` §`#stream-banner`(L682-696)—— `position: fixed; top: 12px; left: 50%`;`.fatal` 修饰符**不得触碰**(硬规则 5)
- `frontend/style.css` §`.markdown-body`(L709-712)—— D-07 的目标之一;§末尾 L1227-1265 是 **Phase 5 `idi-05-04` 的注入目标枚举注释**,D-07 直接沿用
- `frontend/style.css` §`button`(L551-560)/ §`.verdict-buttons button`(L1174-1176)/ §`.annotation-answer summary`(L991-996)—— D-16 / D-17 的对象
- `frontend/style.css` §`.hidden`(L441-446)—— **机制而非样式,不得触碰**(硬规则 1)
- `frontend/index.html` §L10-84 — `#app` > `main#main-pane`(四个 `section`)+ `aside#doc-panel`;§L82-91 是文档面板标题行 DOM(badge 的宿主);§L206-210 是 `#selection-menu`
- `frontend/app.js` §L260-285(`appendSayToChat` / 流式气泡)/ §L676-717(`renderVerdictCard`,2 个按钮)/ §L1150-1156(`<details>` + `<summary>` 的 AI 答复)—— D-17 与 D-13 的普查依据
- `scripts/check-05-ui-uat.py` — Playwright UAT harness(`--item N` 单跑);`MARKDOWN_TARGETS` 与调用点普查守卫是 **D-07 的范本**;D-06 / D-14 的扩写对象;test 6 是「令牌接线表述」的范本(04.1 D-14 的产物)
- `scripts/check-01-token-conformance.sh` — 围栏外裸 `#hex` 必须为 0(D-10 已核实断点字面量不触发它)
- `scripts/check-02-contrast.py` / `scripts/check-03-hidden-uniqueness.sh` / `scripts/check-04-important-count.sh` — 三条不变量守卫,本阶段不得破坏
- `scripts/ui-states/` — p1 / p12 / p3 / checking / archive 五个磁盘状态样本,D-08 实测与 D-06 / D-14 门的运行时环境

### 需求与状态
- `DESIGN.md` — 项目唯一权威设计文档;§3.8 语言红线;§4.1 两栏契约(LAYOUT-02 不得改变其含义)
- `.planning/REQUIREMENTS.md` §Traceability — LAYOUT-01…04 / A11Y-07 均为 Phase 6、状态 Pending
- `.planning/REQUIREMENTS.md` §Out of Scope 表 — 「移动端 / 手机宽度适配」条目(「LAYOUT-02 只承诺"窄窗口不破版"」)

### 外部
- 无。本阶段为纯 CSS 改动,**无外部规范依赖**;唯一的外部标准引用是 WCAG 2.5.8(Target Size Minimum,AA)—— 其**间距例外**存在,但 A11Y-07 明文要求「达到 24×24」,故按字面走尺寸而非例外(D-16 / D-17)。

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **`scripts/check-05-ui-uat.py`**:既有的 Playwright harness,5 个磁盘状态样本,支持 `--item N` 单跑。**D-06 与 D-14 的门都扩在这里**(而非新建脚本),理由是它与既有断言风格、状态样本体系、以及 04.1 D-14 的「令牌接线表述」范本一致。其 `MARKDOWN_TARGETS` 与调用点普查守卫是 **D-07 的现成范本**。
- **`scripts/ui-states/`**:五个状态样本,幂等、仓库样本只读 —— D-08 的三宽度实测与 D-06 / D-14 的运行时断言直接跑在这里。
- **`#doc-panel` 自身的 `background: var(--color-surface)`**(`style.css:476`):D-05 的 sticky header 背景直接复用它,**零新增令牌**。
- **Phase 5 `idi-05-04` 建立的「按调用点枚举 + 普查守卫」方法论**(`style.css` 末尾注释 + `check-05` 的 `MARKDOWN_TARGETS`):D-07 直接沿用,D-13 与 D-17 采用同一口径(按元素/调用点普查,不按容器名)。

### Established Patterns
- **「与消费者同提交」纪律(Hard Rule 5)**:绝不声明一个在同一次提交中不消费的令牌。**本阶段零新增令牌**,故该规则只约束「不得顺手开新令牌」。
- **「追加,不重排」(硬规则 3)**:至少一对等特异性规则由源码顺序决定(`#draft-view h2` L611 与 `#brainstorm-view h2` L679 同为 1-0-1,后者靠源码顺序取胜)。**本阶段是结构性 diff,重排的风险比 Phase 5 更高**——任何删除 `max-height` 的操作都必须原地改声明,不得移动规则块。
- **「最浅的通过值」原则(Pitfall 4a)**:不适用本阶段(无对比度改动),但「断言层级/序关系而非阈值」的立场适用。
- **`.hidden` 是机制而非样式**:`.hidden { display: none !important }` 不得令牌化、移动、弱化或用 `:where()` 降特异性;三个 ID 特异性竞争者(`#selection-menu` / `#annotations-panel` / `#checks-panel`,均 1-0-0)靠它压制。
- **环境事实(不得重新推导、不得对抗)**:截图不可用(headless 渲染被阻,SSE 长连接让 capture handler 无法退出)→ **计划用 DevTools 计算样式检查 + 命名人工步骤,不要计划视觉 diff**;若用 Playwright **必须** `chromium.launch({ channel: 'chrome' })`;键盘划词无法自动化。
- **`overflow-wrap: anywhere` vs `break-word` 的语义差**:只有 `anywhere` 参与 min-content 内在尺寸计算。这是 D-07 与 D-09 的**共同技术依据**,注释里必须写明,否则会被读成任选其一。

### Integration Points
- **唯一改动面** = `frontend/style.css`:围栏外新增/修改的布局、换行、定位规则(D-03 / D-07 / D-09 / D-11 / D-13 / D-16 / D-17)。**围栏 `:root` 内零改动。**
- **`scripts/check-05-ui-uat.py`** 的断言按 D-06 / D-14 扩写(改它同样作废 04.1 指纹,与 `style.css` 合并为同一批处理,一次性连带复验)。
- **`app.js` / `index.html` / `frontend/vendor/` 零改动** —— 硬规则 5 的约 70 个顶层 `getElementById` 句柄 id 不得改名或删除;`frontend/vendor/` 保持只有 `marked.min.js`(Phase 4 gate 原样成立)。
- **D-08 的实测是本阶段唯一的新增工作类型**:规划期需在 1440 / 1024 / 768 三处量横向溢出与遮挡,结论决定 `@media` 是否存在。这是**计划之前的步骤**,不是计划里的一步。
- **本阶段会打破的既有断言(必须在计划里显式登记)**:`check-05-ui-uat.py` 中与 `#chat-messages` / `#annotation-list` / `#latest-check` 的 `max-height` / `overflow` 相关条目、与 `#session-panel` 相关条目、以及 Success Criterion #3 的表述(D-20)。

</code_context>

<specifics>
## Specific Ideas

- **本阶段的核心事实:路线图的核心交付物几乎全部需要重新表述。** 六项被推翻(LAYOUT-01、LAYOUT-03、M2 主因、`#session-panel` 的 flex、A11Y-07 的 21–22px 数字、fence 的 420px 前提),这与 Phase 5 的 D-01 是同一类问题但**规模更大**。规划期应以 D-02 的登记表为起点,而不是以路线图的交付物清单为起点。
- **两条方法论立场的延续**(沿用 04.1 / Phase 5):①名必须说实话(D-05 不加 z-index 而非复用 `--z-badge`);②不采信上游文档的论断,一律以 HEAD 实测/实算为准(D-08 / D-15 的实测驱动)。
- **「唯一确定不达标的是没被点名的那个」**:A11Y-07 点名了裁决按钮(很可能已达标),而唯一确定不达标的是 `.annotation-answer summary`(12px 字号、无 padding、≈14–17px)。这是「按容器名/点名枚举」会漏掉、而「按元素普查」能抓到的典型例子——与 Phase 5 `G-idi-05-1` 同构。
- **D-09 的双保险是刻意的**:`overflow-wrap: anywhere` 落地后 `min-width: 0` 理论上冗余,但保留它是对「将来新增未被覆盖的渲染容器」的兜底。注释必须写清这一点,否则会被当成冗余代码删掉。
- **D-11 的取舍是一次真实的交互面 vs 收敛度的权衡**:保留 `#latest-check` 的滚动是为了不让长自检报告把裁决按钮推出视口。代价是 Success Criterion #3 必须登记偏离(面板区内两个滚动者而非一个)。
- **D-12 的教训**:路线图的交付物**可能与它自己的 Success Criteria 互相矛盾**(「改 `flex: 0 0 auto`」vs「输入行必须钉底」)。规划期遇到这类条目时,应以 Success Criteria 的意图为准并登记,而不是机械执行交付物。

</specifics>

<deferred>
## Deferred Ideas

- **折叠态的状态读数** —— D-04 保持隐藏并登记为有意设计。若日后要恢复,属独立候选(需为 48px 竖条设计一个紧凑形态,接近新能力)。
- **`.collapse-indicator` 的 `font-size: 20px` / `line-height: 1` 越轨字面量** —— backlog `999.1` 第 1 项,与 `check-05-ui-uat.py:588` 的陈旧诊断文案合并为同一批处理。**本阶段不得触碰该元素**(硬规则 5 / 05-CONTEXT D-23)。
- **UI Considerations 的 13 条 `overflow` 延后项(E2–E14)** —— 04.1 的 probe 已**取代**而非继承这些处置(05-CONTEXT 已登记);本阶段只按 D-07 / D-08 / D-09 处理实际的换行与溢出,不逐条消解那 13 项。
- **响应式 / 移动端断点系统、`#app { flex-direction: column }`、任何 1024px 以下的堆叠布局** —— UI-SPEC Q5 明文 Out of scope:它们改变 DESIGN.md §4.1 两栏契约的**含义**,是新设计决策而非 CSS 重构。
- **`#probe-controls` 的移除或重定位** —— 产品行为变更,v1.14 全局已裁定不进任何阶段。
- **暗色模式 / `prefers-color-scheme`** —— v2 `TOKEN-V2-01`。
- **焦点样式本身** —— `A11Y-01`,Phase 7。**本阶段只为它解裁切**(D-13),不写任何 `:focus` 规则。
- **hover / active / transition 态** —— `INTERACT-01` / `INTERACT-02`,Phase 7。**本阶段不新增任何 hover 规则。**
- **`tabindex` / ARIA / 键盘语义 / 划词焦点交接** —— Phase 8。本阶段不触碰 `app.js` / `index.html`。
- **`#latest-check` 的长报告折叠机制** —— D-11 选 B 时明确不引入;若日后裁决按钮的可达性成为实际问题,属独立候选(接近新能力)。
- **`#selection-menu` 的定位数学** —— Pitfall 8 明文:它在旗舰交互路径上且工作正常,**不得「顺手改进」**。
- **`#main-pane` / `#doc-panel` 的 padding 抬升**(若 D-13 普查判定需要) —— 会移动前者居中布局下的 section 位置、并与 `#doc-panel-body { padding: 32px 40px }` 叠加;须在计划里显式登记为视觉变更,不做「顺手统一」。

### Reviewed Todos (not folded)
无 —— `gsd-tools query todo.match-phase 6` 返回 `todo_count: 0`,本阶段无待办匹配。

</deferred>

---

*Phase: 6-布局稳健性*
*Context gathered: 2026-09-22*
# Phase 6: 布局稳健性 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-22
**Phase:** 6-布局稳健性
**Areas discussed:** 徽标收口口径, 窄窗口守卫职责, 滚动容器收敛, 24×24 命中区

---

## 徽标收口口径

### Q1: #state-badge 的收口机制取哪一条?

| Option | Description | Selected |
|--------|-------------|----------|
| A) 接受 HEAD + 补 sticky | 保留 qrq 消掉魔法数/遮挡/碰撞主因的收益,给 #doc-panel-header 加 position: sticky 把「恒可见」拿回来 | ✓ |
| B) 接受 HEAD,代价照收 | 只登记两条已知代价(滚动即丢失状态读数 + 折叠态无读数),不改 CSS | |
| C) 回退 fixed + calc() | badge 恒可见,但重新引入 LAYOUT-03 的遮挡与 M2 碰撞 | |

**User's choice:** A) 接受 HEAD + 补 sticky
**Notes:** 讨论前核实到磁盘 HEAD 上 `#state-badge` 已是 `#doc-panel-header` 内的流内元素(无 `position`、无 `right`),LAYOUT-01 的 448px 魔法数已消失。但 HEAD 引入两条已核实代价:(1) 全文件 `position: sticky` 数量 = 0 且 `#doc-panel { overflow-y: auto }`,故标题行(含 badge 与折叠指示符)会随面板内容滚走 —— 这正是 UI-SPEC Q6 反对 `absolute` 时给出的理由原话;(2) `style.css:485` 折叠态 `display: none`。契约侧被推翻的文本:UI-SPEC Q6「calc(). Committed.」+ Pitfall 8「the fix must not move the badge into normal flow」;`style.css:668-669` 留有 qrq 的逐字反驳注释。

### Q2: 折叠态的 #state-badge 怎么处置?

| Option | Description | Selected |
|--------|-------------|----------|
| A) 保持隐藏,登记为有意设计 | 可折叠面板的语义就是主动让出空间;48px 竖条放不下 pill | ✓ |
| B) 折叠态显示紧凑形态 | 只留一个状态色点,读数在两种形态下都不中断 | |
| C) 保持隐藏,记入 backlog | 不当作有意设计,升级为「已知缺口」留给独立候选 | |

**User's choice:** A) 保持隐藏,登记为有意设计
**Notes:** 与 M2 性质不同 —— 横幅盖住 badge 是非自愿丢失读数(路线图判为缺陷),折叠是用户主动选择。本阶段只修「滚动即丢失」这一条非自愿丢失。

### Q3: sticky 的实现取哪一种?

| Option | Description | Selected |
|--------|-------------|----------|
| A) 仅 sticky + 背景,不加 z-index | 只碰 #doc-panel-header 一个选择器,零新令牌 | ✓ |
| B) sticky + 显式 z-index 档 | 额外加一档 z-index(新令牌或复用 --z-badge,后者会让名说谎) | |
| C) 改成 #doc-panel-body 单独滚 | #doc-panel 改 overflow: hidden,把标题行彻底移出滚动容器 | |

**User's choice:** A) 仅 sticky + 背景,不加 z-index
**Notes:** 必须补背景 —— `.panel-header` 规则里没有任何 `background` 声明,sticky 后正文会从标题行底下穿过。`#doc-panel` 自身背景 `var(--color-surface)`(style.css:476)已被消费,零新令牌。z-index 不加:sticky 元素是 positioned,默认画在静态内容之上。不选 C 是因为它会改变 LAYOUT-04 要统计的滚动容器数。待处理细节:`.panel-header` 的 `border-radius: var(--radius-md)` 圆角处可能有内容从四角露出。

### Q4: 徽标收口用什么门验证?

| Option | Description | Selected |
|--------|-------------|----------|
| A) 扩 check-05-ui-uat.py | 断言流内 + 768/1024/1280 不重叠 + 滚动后 header 可见 | ✓ |
| B) 新建专用脚本 | 不动 check-05,不叠加 04.1 指纹风险 | |
| C) 仅静态断言 + 人工步骤 | diff 最小,但违反硬规则 7 | |

**User's choice:** A) 扩 check-05-ui-uat.py
**Notes:** 路线图 Success Criterion #2 原本只在 1024/1280 两处实检,须补上 768(承诺的窄窗口下限)。**残余碰撞经核实不存在**:`showStreamBanner` 文案「事件流已断开,正在自动重连……」15 字 × 12px + 24px padding + 2px border ≈ 206px,居中于视口;badge 最宽文案「待选自检档(阶段 5)」9 字 ≈ 132px 在文档面板标题行右端;相交条件是 `banner宽 > 视口宽 - 284`,代入 206px 得视口 < 490px,远低于 768px 下限。代价:再叠一层 idi-04.1 指纹失效。

---

## 窄窗口守卫职责

### Q1: overflow-wrap 的作用域取哪一档?

| Option | Description | Selected |
|--------|-------------|----------|
| A) 枚举全部六个目标 | 照 Phase 5 G-idi-05-1 先例,门按 renderMarkdown() 调用点普查 | ✓ |
| B) 只护 .markdown-body | 照路线图字面 | |
| C) 写通配规则 | 统一给 #main-pane / #doc-panel 的后代加 | |

**User's choice:** A) 枚举全部六个目标
**Notes:** 六目标 = `.markdown-body`(宿主 `#doc-panel-body` 与 `#latest-check`)+ 五个非 `.markdown-body` 容器:`.event-content` / `.chat-bubble` / `.say-chunk` / `.annotation-note` / `.annotation-answer-body`。该枚举已由 `idi-05-04` 建立。HEAD 现状:`.event-content` 有 `break-all` + `pre-wrap`(已裁定不动);`.chat-bubble` 有 `break-word`;其余四处零保护;`overflow-wrap` 全文件零命中。不选 B:漏掉的三个是 AI 流式回复与批注正文,会撑出 `#chat-messages` / `#annotation-list` 的横向滚动条,与 LAYOUT-04 冲突。不选 C:会波及已裁定的 `.event-content break-all`,并把影响面重新变成不可枚举。

### Q2: @media 窄窗口守卫的存在性判据取哪一条?

| Option | Description | Selected |
|--------|-------------|----------|
| A) 实测驱动 | 1440/1024/768 量横向溢出与遮挡,只在实测破版处写 | ✓ |
| B) 契约驱动,照写 | 无论实测都写一条,窄宽度重赋 --doc-panel-w | |
| C) 现在判定不需要 | 直接认定由 min-width + overflow-wrap 满足 | |

**User's choice:** A) 实测驱动
**Notes:** `--doc-panel-w: clamp(340px, 30vw, 480px)` 本身已视口自适应(1024px 时 30vw=307 被夹到 340px 下限;768px 时 30vw=230 同样夹到 340px,占 44%,主区剩 428px)。路线图把守卫范围定死为「不破版」而非「适配」。分析(未实测):横向溢出的真因是不可断长内容撑破 flex 项,428px 主区列窄但不是破版。

### Q3: min-width: 0 的落点取哪一种?

| Option | Description | Selected |
|--------|-------------|----------|
| A) 两个子项都加 | #main-pane 与 #doc-panel 都加,双保险 | ✓ |
| B) 只加 #main-pane | 覆盖路线图意图的最近似落点 | |
| C) 不加 min-width | 只靠 overflow-wrap: anywhere 收窄 min-content | |

**User's choice:** A) 两个子项都加
**Notes:** `#app` 的两个子项都是 `min-width: auto`,`flex-basis` 不是硬约束 —— `min-width: auto` 胜出,长内容能把 `#doc-panel` 顶得比 `clamp()` 还宽。技术依据(CSS Text 3):`overflow-wrap: anywhere` 参与 min-content 内在尺寸计算,`break-word` 不参与。选 A 是因为它不依赖「六个目标全覆盖」长期成立。注释须写清为什么在 `anywhere` 已生效时它不是冗余。

### Q4: 断点字面量例外的声明协议取哪一种?

| Option | Description | Selected |
|--------|-------------|----------|
| A) 条件声明 | 仅在实际写出 @media 时于段首围栏注释声明并登记进 UI-SPEC | ✓ |
| B) 预先声明 | 无论是否写 @media 都先在 UI-SPEC 里登记 | |
| C) 只文档登记 | 不写围栏注释 | |

**User's choice:** A) 条件声明
**Notes:** UI-SPEC Q5 原话要求「Phase 6 declares it in a fenced comment at the head of its @media section」,理由是 CSS 禁止在媒体查询条件里用 `var()`。与 Q2 的实测驱动一致。已核实:断点是非 hex 字面量,CHECK-01 只管裸 `#hex`,不会触发门;硬规则 4 禁止 `var(--x, #fallback)`,绕过路径本就被堵死。

---

## 滚动容器收敛

### Q1: 三个嵌套滚动容器的处置范围取哪一档?

| Option | Description | Selected |
|--------|-------------|----------|
| A) 三个全删 | 照路线图,#main-pane 成为唯一滚动者 | |
| B) 保留 #latest-check | 删 #ai-events 与 #annotation-list,保留 30vh | ✓ |
| C) 全删 + 另立机制 | 为 #latest-check 加折叠机制 | |

**User's choice:** B) 保留 #latest-check
**Notes:** DOM 已核实:`#app` > `main#main-pane`(四个 section)+ `aside#doc-panel`。保留理由:它下方就是 `#check-controls`,而裁决按钮是交互面;去掉限高后长自检报告会把按钮推到视口之外。已接受代价:Success Criterion #3 必须登记偏离 —— 面板区内会剩两个滚动者(`#main-pane` + `#latest-check`)。路线图基线的 40vh 那只已不存在。

### Q2: #session-panel 的 min-height / flex 怎么处置?

| Option | Description | Selected |
|--------|-------------|----------|
| A) 零改动 + 登记推翻 | 登记路线图交付物为「被 HEAD 推翻 + 执行会造成回归」 | ✓ |
| B) 照路线图执行 flex: 0 0 auto | 接受输入行不再钉在视口底部 | |
| C) 只去掉 min-height | 保留 flex: 1 1 auto | |

**User's choice:** A) 零改动 + 登记推翻
**Notes:** 已核实 HEAD:`flex: 1 1 auto` + `min-height: 200px` + `.panel-body { flex: 1; min-height: 0 }` + `#chat-messages { flex: 1; min-height: 160px }`,`#chat-input-row` 是 `.panel-body` 最后一个子元素。这正是 `style.css:781-782` 注释写的设计「输入行自然贴底」。改成 `flex: 0 0 auto` 会让面板按内容定高,输入行落到视口之外 —— **路线图该交付物与它自己的「输入行必须钉底」互相矛盾**。另:`min-height: 200px` 不是死代码(空态下是居中问候语唯一的空间来源),不得删除。

### Q3: 焦点环解裁切的容器枚举取哪种口径?

| Option | Description | Selected |
|--------|-------------|----------|
| A) 按可聚焦元素枚举 | 门按元素普查,不按容器名 | ✓ |
| B) 照路线图抬两个 | 只抬 #chat-messages 与 #annotation-list | |
| C) 四个全抬 | 不做普查,以 padding 换确定性 | |

**User's choice:** A) 按可聚焦元素枚举
**Notes:** 已核实:`#annotation-list` 确有可聚焦后代(`app.js:1150-1154` 的 `<details>` + `<summary>`)→ 抬 padding 确有作用;`#chat-messages` 没有任何可聚焦后代(气泡是 `div` 与 `p`)→ 抬它是空动作。路线图 Phase 7 段自己写了三个裁切容器(`#chat-messages` 2px、`#annotation-list` 2px、`#sidebar` **0**),但 `#sidebar` 不存在;真正 0 padding 且 `overflow-y: auto` 的是 `#main-pane` 与 `#doc-panel`。**路线图内部不一致。**

### Q4: LAYOUT-04 的验证门取哪一种?

| Option | Description | Selected |
|--------|-------------|----------|
| A) 恰好两个 + 可达性 | 面板区内滚动容器恰好两个 + 两者都能滚到底 + 两处 max-height 为 none | ✓ |
| B) 至多两个 | 口径放宽 | |
| C) 静态 + 仅可达性 | 成本最低 | |

**User's choice:** A) 恰好两个 + 可达性
**Notes:** 口径取「恰好两个」而非「至多两个」,以便抓到「意外新增第三个滚动者」这类回归。滚动容器按 DOM 普查而非硬编码选择器。

---

## 24×24 命中区

### Q1: A11Y-07 的判定基准取哪一条?

| Option | Description | Selected |
|--------|-------------|----------|
| A) 实测驱动 | Playwright 量 getBoundingClientRect,已达标则零改动 | ✓ |
| B) 照路线图数字补 | 照 21–22px 直接补,不实测 | |
| C) 直接加 min-height | 无条件保险 | |

**User's choice:** A) 实测驱动
**Notes:** 路线图写的「实测约 21–22px 高」与 HEAD 对不上。按 `font-size: 14px` + `padding: 4px 10px` + `border: 1px` + `line-height: normal`(`html, body` 没有 `line-height` 声明)算,盒高 = `line-height + 10` ≈ **26–30px**;要得到 21–22px 需 line-height ≈ 0.8×14,不可得。字体度量必须实测。

### Q2: 若实测不足,命中区机制取哪一种?

| Option | Description | Selected |
|--------|-------------|----------|
| A) min-height + min-width | 不动现有 padding,只抬下限 | ✓ |
| B) 抬 padding | 改的是外观而非命中区 | |
| C) ::after 撑开命中区 | 视觉不变,但相邻命中区会互相重叠 | |

**User's choice:** A) min-height: 24px + min-width: 24px
**Notes:** 对已达标的控件零影响,对不足的只补差额。不选 C 是因为 `.verdict-buttons { gap: var(--space-2) }` = 8px,扩展后的相邻命中区会互相重叠,反而可能违反 WCAG 2.5.8 的「不与他者相交」要求。

### Q3: A11Y-07 的作用范围取哪一档?

| Option | Description | Selected |
|--------|-------------|----------|
| A) 可交互元素普查 | 只对实测未达标者施加 | ✓ |
| B) 只做点名的裁决按钮 | 交付物最小、最贴字面 | |
| C) 普查 + 全部加 min-height | 统一、不留判断 | |

**User's choice:** A) 可交互元素普查
**Notes:** 已枚举全部可交互元素:所有 `<button>` ≈ 30–34px ✓;`#selection-menu button` ≈ 30px ✓;`.verdict-buttons button` ≈ 26–30px(待实测,很可能已达标);**`.annotation-answer summary` ≈ 14–17px(12px 字号、无 padding、无 min-height)→ 唯一确定不达标**;`.collapse-indicator` 属不得触碰,其可点父级 `.panel-header` 为 36px ✓。注意:给 `summary` 加 `min-height` 会改变 `.annotation-item` 的高度,属一次视觉变更,须显式登记。

### Q4: 「不得为此重构侧栏」这条 fence 怎么处置?

| Option | Description | Selected |
|--------|-------------|----------|
| A) fence 随前提失效 | 登记前提失效,实质保留为一般原则 | ✓ |
| B) fence 仍然生效 | 保守解读,任何触及侧栏结构的改动一律禁止 | |
| C) 重述为可验证判据 | 把陈述式边界变成门能查的东西 | |

**User's choice:** A) fence 随前提失效
**Notes:** fence 的前提两处都已不成立:420px 侧栏不存在(现为 `--doc-panel-w: clamp(340px,30vw,480px)`,裁决卡在 `#checks-panel` 里、内容列 `max-width: 768px`);按钮数量已从 3 个变成 2 个(`app.js:709-711` 只建 `fixBtn` / `keepBtn`)。

---

## Claude's Discretion

- `#doc-panel-header` 的 `border-radius: var(--radius-md)` 在 sticky + 背景下的处置(保留、改 `0`、或只圆下缘)。
- 六处 `overflow-wrap: anywhere` 的声明组织方式(合并成一条选择器列表、还是按容器分组)。
- D-13 的普查结论:具体哪些容器需要抬 padding、抬到多少。
- D-08 实测的具体工具与判据(Playwright 量 `scrollWidth` vs DevTools 计算样式;「遮挡」的精确定义)。
- 围栏外注释的措辞与粒度(尤其 D-03 的「为什么采纳 qrq 而非契约 Q6」与 D-09 的「为什么 `min-width: 0` 不是冗余」)。

## Deferred Ideas

- 折叠态的状态读数(D-04 保持隐藏;若日后恢复属独立候选)。
- `.collapse-indicator` 的越轨字面量 —— backlog `999.1`,本阶段不得触碰。
- UI Considerations 的 13 条 `overflow` 延后项(E2–E14)—— 04.1 的 probe 已取代而非继承。
- 响应式 / 移动端断点系统、`#app { flex-direction: column }` —— UI-SPEC Q5 明文 Out of scope。
- 焦点样式本身(A11Y-01,Phase 7);hover / active / transition(INTERACT-01/02,Phase 7);`tabindex` / ARIA(Phase 8)。
- `#latest-check` 的长报告折叠机制(D-11 选 B 时明确不引入)。
- `#main-pane` / `#doc-panel` 的 padding 抬升(若 D-13 普查判定需要,须登记为视觉变更)。
- `#probe-controls` 的移除或重定位;暗色模式;`#selection-menu` 的定位数学 —— 均已在 v1.14 全局裁定排除。

### Reviewed Todos (not folded)

无 —— `gsd-tools query todo.match-phase 6` 返回 `todo_count: 0`。
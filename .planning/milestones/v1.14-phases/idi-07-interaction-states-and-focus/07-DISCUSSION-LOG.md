# Phase 7: 交互状态与焦点样式 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-22
**Phase:** 7-交互状态与焦点样式
**Areas discussed:** 焦点环:落点与颜色, 交互态语言与 disabled, 过渡的边界, 验收门与自动化边界

---

## 焦点环:落点与颜色

### Q1 — 环色的验证面:WCAG 1.4.11 的 3:1 必须对哪些背景成立?

| Option | Description | Selected |
|--------|-------------|----------|
| 只算实际相邻地面 | 环只需对 `--color-surface-page` / `--color-surface`(4.65 / 4.53)过关;`--radix-blue-11` 直接可用 | |
| 必须含 0.75 归档合成 | 路线图 Gate 原文要求「每个环都对 0.75 合成背景验过」;`--radix-blue-11` 只剩 3.03:1,需要有余量的值 | ✓ |
| 连 sunken 也算 | 把 `--color-surface-sunken`(#f0f0f0)也算进去 | |

**User's choice:** 必须含 0.75 归档合成
**Notes:** 讨论中核实——`.round-frozen` 的 0.55 已被 S-4 删除,`.annotation-answered` 0.65 与 `.tier-desc` 0.8 均已令牌化消掉,全站只剩 `.archive-mode #round-doc { opacity: 0.75 }` 一个会合成焦点环的 opacity。`--color-surface-sunken` 经核实只是 `.markdown-body code` 与 `.badge-answered` 的背景,不是任何可聚焦元素的相邻地面。

### Q2 — `--color-focus` 取哪个值?

| Option | Description | Selected |
|--------|-------------|----------|
| `#1f63bd`(04-UI-SPEC 原值) | 5.57 全 / 3.45 归档合成。S-4 的签核算术就是拿它算的;代价是它是颜色层里唯一不在 Radix 刻度上的值 | ✓ |
| `var(--radix-blue-11)` = `#0d74ce` | 4.53 全 / 3.03 归档合成。系统内、零新增 primitive;代价是归档态只剩 0.03 余量 | |
| `var(--radix-blue-12)` = `#113264` | 11.99 全 / 5.73 归档合成。系统内且余量巨大;代价是它是高对比**文字**步,作为 2px 环视觉上接近边框 | |

**User's choice:** `#1f63bd`(04-UI-SPEC 原值)
**Notes:** 理由是 S-4 的签核算术(`04-UI-SPEC.md` §Sign-Off Items S-4:「删除 opacity 后环回到 5.62」)以此为据;换值会改变一个已签核决策的前提。实测在 HEAD 地面(`#f9f9f9` / `#fcfcfc`)下仍是三者中余量最大的。

### Q3 — `:focus-visible` 写成一条通配规则,还是枚举可聚焦元素?

| Option | Description | Selected |
|--------|-------------|----------|
| 裸 `:focus-visible` 通配 | 一条规则覆盖全部;代价是影响面不可枚举 | |
| 枚举(与普查脚本同集) | `button, input, select, textarea, a[href], summary, [tabindex]:focus-visible`;与 `check-05` 普查脚本的可聚焦集完全同集 | ✓ |
| 通配 + 显式排除文档区 | 通配为主,在同一条规则里显式排除文档区 | |

**User's choice:** 枚举(与普查脚本同集)
**Notes:** 沿 Phase 5 `G-idi-05-1` 与 Phase 6 `overflow-wrap` 建立的「影响面必须可枚举、可对照」口径。枚举与门普查同集,两者可逐条对照。

### Q4 — `#round-doc` 的焦点环承载面怎么处理?

| Option | Description | Selected |
|--------|-------------|----------|
| 含 `[tabindex]`,指派给 Phase 8 | 枚举含 `[tabindex]`,契约「凡可聚焦必有环」无缺口;`#round-doc` 的内嵌处理作为明确指派写进 CONTEXT | ✓ |
| 枚举不含 `[tabindex]` | Phase 7 只覆盖今天真实可聚焦的六类;代价是枚举与普查脚本出现一处差异 | |
| Phase 7 现在就写内嵌规则 | 现在就写 `#round-doc:focus-visible { outline-offset: -2px }`;代价是死代码,且无法运行时验证 | |

**User's choice:** 含 `[tabindex]`,指派给 Phase 8
**Notes:** 讨论中核实 `#round-doc` 今天不可聚焦(Phase 8 才加 `tabindex="0"`),且它落在 `.archive-mode` 的 0.75 合成里。路线图 Phase 8 的 Deliverables 已明文承接这一条。

---

## 交互态语言与 disabled

### Q1 — `:hover` / `:active` 要不要 gate 在 `:not(:disabled)` 上?

| Option | Description | Selected |
|--------|-------------|----------|
| gate 在 `:not(:disabled)` 上 | 禁用按钮悬停/按下零反馈;可辨识性由 opacity 0.55 独家承担 | ✓ |
| 不 gate,另加 `:disabled` 回写 | 给 `button:disabled` 补一条 background 回写钉住原值 | |
| 不处理,接受现状 | 接受禁用按钮悬停时也变灰 | |

**User's choice:** gate 在 `:not(:disabled)` 上
**Notes:** 讨论中核实了缺陷现场:路线图说 `#btn-authorize:disabled` 会响应 hover,实测它因 1-0-0 钉住填充色而**免疫**;真正会响应的是 `.verdict-buttons button:disabled`(`:1222` 只设 `opacity`/`cursor`,没有规则钉住 `background`)。

### Q2 — 填充按钮的 hover 反馈怎么补?

| Option | Description | Selected |
|--------|-------------|----------|
| 统一 rgba 压暗叠层 | `box-shadow: inset 0 0 0 999px rgba(0,0,0,0.06)`;一条规则覆盖全部填充按钮,零新令牌 | ✓ |
| 按族开 hover 令牌 | 按色族开 `--color-action-*-hover`;代价是深填充三族在 Radix 刻度上没有更深的可用档 | |
| 填充按钮不加 hover | 只加 `:active` | |

**User's choice:** 统一 rgba 压暗叠层
**Notes:** 讨论中实测排除了 `opacity` 路线(它在 INTERACT-02 的允许列表内、可过渡,但会让白字一起变浅):primary 4.77→**3.93**、danger 5.21→4.42、commit 4.72→**3.81**,三族跌破 AA 4.5:1。rgba 叠层把填充变深、文字不动,对比度反而上升(5.27 / 5.75 / 5.23 / 12.97)。

### Q3 — `:active` 用什么视觉语汇?

| Option | Description | Selected |
|--------|-------------|----------|
| 同机制加深 | 朴素按钮新开 `--color-surface-active: var(--radix-gray-4)`(与 hover 的 gray-3 构成 3→4 递进);填充按钮同套 rgba 叠层、alpha 0.12 | ✓ |
| 内阴影凹陷感 | `box-shadow: inset 0 1px 3px`;代价是它会替换而非叠加 hover 的叠层 | |
| 1px 位移 | `transform: translateY(1px)`;代价是不在过渡允许列表,且 `#selection-menu` 的包含块是硬规则 5 点名的雷区 | |

**User's choice:** 同机制加深
**Notes:** `--radix-gray-4` 已声明且已被 `--color-surface-user` 消费 ⇒ 零新增 primitive。刻意不复用 `--color-surface-user` 承载 active,因为那个名字说的是「用户消息背景」(04.1 D-03 的方法论)。

### Q4 — 输入框与下拉要不要 hover 反馈?

| Option | Description | Selected |
|--------|-------------|----------|
| input 与 select 统一加 hover | `border-color` 加深一步;不加 `:active`(文本框的「按下」无意义) | ✓ |
| 只给 select | 只给点击型控件 | |
| 都不加 | hover/active 是按钮语义,交给焦点环与 UA | |

**User's choice:** input 与 select 统一加 hover
**Notes:** 全站没有被禁用的 `input`/`select`(8 条 `:disabled` 规则全部是按钮),故 `:not(:disabled)` 在这里是防御性写法而非当下必需——须写注释说明,免得被当成冗余删掉(与 06-CONTEXT D-09 同型)。

---

## 过渡的边界

### Q1 — 既有的 `.event-list { transition: background-color 0.3s }` 怎么处置?

| Option | Description | Selected |
|--------|-------------|----------|
| 保留 300ms,登记例外 | 它是流式状态指示器(`.streaming` / `.aborted`)而非控件态过渡;保住 Phase 7 的纯追加性质 | ✓ |
| 归一化到 150ms | INTERACT-02 字面要求「约 120–150ms」,规格就是全部规格 | |
| 删掉这条过渡 | 消除两个时长的问题 | |

**User's choice:** 保留 300ms,登记例外
**Notes:** 登记要求:例外必须同时写进 CONTEXT、UI-SPEC 的字面量/例外清单、以及新过渡的围栏注释里,不得静默留下两个时长。

### Q2 — 新的过渡声明挂在哪里?

| Option | Description | Selected |
|--------|-------------|----------|
| 新增一条独立规则 | 文件末尾 `button, input, select { transition: ... }`;零编辑既有规则 | ✓ |
| 写进既有基础规则 | 写进 `button { ... }`(`:578`)+ `input`/`select` 规则;代价是编辑三条既有规则 | |
| 逐条写进 hover/active | 每条新增规则各写一遍;代价是重复 6+ 次 | |

**User's choice:** 新增一条独立规则
**Notes:** 特异性 0-0-1,与 `.event-list`(0-1-0,不同元素)零竞争。

### Q3 — `prefers-reduced-motion` 写成什么形态?

| Option | Description | Selected |
|--------|-------------|----------|
| reduce 里按选择器重写为 none | 枚举与挂载点同集,**且顺带覆盖既有的 300ms**;零 `!important` | ✓ |
| 用 `no-preference` 包裹 | 把新增过渡写进 `no-preference` 媒体查询;代价是盖不到既有的 `.event-list` | |
| 只关新增的 | 最窄 | |

**User's choice:** reduce 里按选择器重写为 none
**Notes:** 讨论中核实——行业标准写法 `*, *::before, *::after { ... !important }` 会引入两个 `!important`,而本仓库 `!important` 声明数必须恒为 1(硬规则 2/4,`check-04` 会变红),故那条路在本项目里根本不存在。枚举含 `.event-list` 是刻意的。

### Q4 — 过渡列表要不要包含 `opacity`?

| Option | Description | Selected |
|--------|-------------|----------|
| 不含 opacity,禁用态瞬变 | 禁用态是 G3 前提条件唯一的视觉信号,应被立即感知 | ✓ |
| 含 opacity,禁用态淡入 | 8 处 `:disabled` 的 0.55 会淡入/淡出 | |

**User's choice:** 不含 opacity,禁用态瞬变
**Notes:** 讨论中另得一条**派生结论**(未提问,由 INTERACT-02 的允许列表强制):焦点环本身必须瞬变——`outline-color` / `outline-width` 不在允许过渡的三个属性内。这是正确的,过渡焦点环是已知的无障碍反模式。

---

## 验收门与自动化边界

### Q1 — 本阶段的门放在哪里?

| Option | Description | Selected |
|--------|-------------|----------|
| 三段分工 | 算术比值→`check-02` 的 PAIR 清单;契约计数→新的零依赖静态断言;运行时→`check-05` 新增 item 10 | ✓ |
| 全塞进 `check-05` item 10 | 单点;代价是把纯算术塞进需要 Playwright 的慢门 | |
| 新建 `check-06` | 本阶段契约自含一份;代价是编号已被 `check-06-idi05-validation.py` 占用,且与 Phase 6 先例相悖 | |

**User's choice:** 三段分工
**Notes:** 讨论中核实 `check-02-contrast.py` **已内建 alpha 合成**(`:125` `composite()`,PAIR 的 `@<alpha>` 后缀 `:178-196`)⇒ 环对 0.75 归档合成的比值断言零新代码。

### Q2 — 本阶段的自动化边界画在哪里?

| Option | Description | Selected |
|--------|-------------|----------|
| SC1–SC4 自动化 + SC5 拆两半 | SC5 的可测半场进机器门(禁用按钮 hover 背景不变 + opacity 仍为 0.55),「一眼看出不可点」作为具名人工验收项 | ✓ |
| 全部自动化,零人工项 | 把「未被软化」换成机器代理量 | |
| SC1 与 SC5 都标人工 | 人工项更多 | |

**User's choice:** SC1–SC4 自动化 + SC5 拆两半
**Notes:** 「一眼看出不可点」是关于**感知**的主张,不是关于数值的主张,故保留为 VERIFICATION 的 manual list 里的一条具名项。**本阶段只有这一条人工项。**

### Q3 — SC3 的归档态那一半怎么验?

| Option | Description | Selected |
|--------|-------------|----------|
| 算术进常驻门 + 注入探针 | `check-02` 的 `NON-TEXT@0.75` PAIR 作常驻门;另写一次性注入探针作反事实证据,不进守卫契约 | ✓ |
| 只走算术 | 最小;代价是算术断言从未在真实归档态下被观察过 | |
| 注入并写成常驻断言 | 常驻真渲染证据;代价是断言对象是合成 DOM,且永久加进慢门 | |

**User's choice:** 算术进常驻门 + 注入探针
**Notes:** 讨论中核实**五个状态样本的 `#round-doc` 内 `a[href]` 计数为 0** —— 运行时那半场今天没有服务对象。探针定位与 `scripts/probe-05-resolve-color.py` 一致(「不是门,不进守卫契约」);门里须显式登记这个计数事实。

### Q4 — 焦点环覆盖的门用哪种口径?

| Option | Description | Selected |
|--------|-------------|----------|
| 按元素普查 | 逐个断言计算 outline 非零 + 断言「未被覆盖的可聚焦元素数为 0」 | ✓ |
| 硬编码选择器计数 | 只证明规则被写下了 | |
| 两者都做 | 同一件事两处维护 | |

**User's choice:** 按元素普查
**Notes:** 与 Phase 6 D-14 同口径。「枚举会漏项」正是 D-05 选枚举路线的已知代价,门必须正面回答它。

---

## Claude's Discretion

- 新过渡挂载规则的具体位置与围栏注释措辞(尤其两个时长并存的说明、`input:not(:disabled)` 的防御性说明)。
- `textarea` 是否进新过渡的枚举(今天 `<textarea>` 计数为 0;进则与焦点环枚举同集,不进则严格「不声明不被消费的」)。
- D-08 的 rgba 叠层规则怎么组织(一条共享选择器列表 vs 与各填充按钮分组);alpha 的精确值(0.06 是实测点,可在 0.05–0.08 间微调但须重跑文字对比度)。
- `#selection-menu button`(hover 用 `--color-surface-info`)的态是否并入统一的一套。
- D-10 的「加深一步」具体取值:`--color-border-strong`(`--radix-gray-9` `#8d8d8d`)→ 哪一档(须实测并登记为新配对进 `check-02`)。
- 围栏注释的粒度,尤其「`#1f63bd` 是对已签核契约的字面遵从,不是漏改」与「为什么枚举而不是通配」。

## Deferred Ideas

- **`#round-doc` 的焦点环内嵌处理** —— 明确指派给 Phase 8(本阶段唯一跨阶段的开放项)。
- **`check-05` 普查脚本的可聚焦集若日后新增类别,焦点环枚举须同步**。
- `.collapse-indicator` 的越轨字面量 —— backlog `999.1`,不得触碰。
- `:disabled` 的 8 条重复声明是否收敛 —— 属重构,且会改变特异性。
- `#selection-menu` 的定位数学与 DOM 位置 —— Pitfall 8 明文不得顺手改进。
- `#probe-controls` 的视觉重做、暗色模式、焦点陷阱 / 完整 ARIA、响应式断点系统、骨架屏 —— 均已裁定不进本里程碑或另属阶段。
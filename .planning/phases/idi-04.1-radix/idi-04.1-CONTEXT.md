# Phase 04.1: Radix 颜色族重写 - Context

**Gathered:** 2026-09-19
**Status:** Ready for planning

<domain>
## Phase Boundary

把 `style.css` 的颜色族从手调 hex 换成 Radix Colors 的 12 步语义刻度,并据此重算 UI-SPEC 的颜色契约与 CHECK-02 的对比度配对清单。同时吸收 idi-04 UAT 的 3 项 FAIL 与 `--color-text-muted` 3.23:1 的 AA 倒退。

**这是值层的刻意重写。结构产出不动:** 围栏 `:root`(L5-L224)的位置与围栏标记、75 个令牌的**分层结构**、四条守卫命令、`.hidden` 唯一性、`!important` 声明数 = 1。

**明确不含:**
- 暗色模式(与 v1.14 已记录排除项一致)
- S-1 间距 12 档与 S-2 的 14px 一级字号档(已签核,不得重新讨论)
- 任何新的运行时依赖或构建步骤
- `frontend/` 下除 `style.css` 之外的任何文件改动(`app.js` / `index.html` / `vendor/` 零改动)

</domain>

<decisions>
## Implementation Decisions

### Radix 交付方式

- **D-01:** Radix 的色值以**手工转抄 hex 进围栏内 tier-1** 的方式落地 —— 把每族用到的步的 hex 值直接写成 `:root` 内的 primitive 声明。**不 vendor Radix 的 CSS 文件。** 理由:零新文件、`frontend/vendor/` 保持只有 `marked.min.js`(Phase 4 gate 原样成立)、依赖为零,且颜色值仍然只有围栏**一个事实源** —— 与本里程碑反复警告的「双事实源」问题同源。代价(已接受):Radix 上游更新需手工同步。

### 令牌名与契约归属

- **D-02:** tier-2 的 49 个语义令牌名(`--color-text-muted` / `--color-action-irreversible` / …)**逐字冻结**。它们被全部选择器、CHECK-02 的按名配对清单、以及 Phase 5 的 VISUAL-01/02 引用。冻结后本阶段是真正的纯值替换(SC2),diff 只落在围栏内。名与 Radix 步数的映射关系靠围栏内注释记录。 — **Reversibility:** costly — 改名要同时改 933 行里的全部 `var()` 引用、CHECK-02 清单、以及 Phase 5 已规划的计划文本。
- **D-03:** tier-1 的 26 个 primitive 名换成 **Radix 刻度名**(`--radix-<family>-<step>`,如 `--radix-gray-11`)。原 Tailwind 式名与 Radix 的 1-12 编号语义直接冲突:`--gray-600` 现在指「中灰」,而 Radix 的 `gray-6` 指「细边框」—— 保留旧名会让名说谎。CHECK-02 清单里作为背景出现的 tier-1 名一并重算。tier-1 名不得出围栏(与 TOKEN-02 硬不变量同源,机械可查)。 — **Reversibility:** costly — 回退要同时改围栏与 CHECK-02 清单。
- **D-04:** **只声明本阶段真正消费到的步**,不声明完整 12 步。遵守 Phase 4 已立的 Pitfall 1 / Hard Rule 5(「绝不定义同一次提交不消费的令牌」)。代价(已接受):刻度不完整,Phase 5 取新步(如实心填充的 9/10 步)时要改围栏 —— 那是普通编辑,不是结构变更。
- **D-05:** 新建 `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md`,**只重写 Color 与 Contrast Verification 两节**;其余节(Spacing Scale / Typography / Design Decisions / Do-Not-Touch / 四条命令 / Sign-Off)在文件头**显式声明 `04-UI-SPEC.md` 仍为权威**,并在 canonical_refs 中指向它。**不复制 1179 行全文**(那会造出第二份事实源 —— 正是本阶段要消除的东西)。 — **Reversibility:** costly — 日后若要合并回单份契约,需要迁移 Phase 5-8 已经建立的对 04.1 目录的引用。

### 色族选型与 AA 步骤

- **D-06:** 中性族取 **Radix `gray`**(纯中性)。现有 gray 值全部是 r=g=b(`#0d0d0d` / `#8f8f8f` / `#d9d9d9`),选 `gray` 是字面对应,视觉变化最小。 — **Reversibility:** costly — 换族等于再重写一遍全部中性色值。
- **D-07:** 强调色**逐族取与现有色相最接近的 Radix 族**(blue→blue / green→green / amber→amber / red→red / purple→violet)。**关键依据:AA 保证来自步的选择,不来自族的归属** —— 同一族内取第 11 / 12 步即成立,所以不必为了对比度牺牲色相。具体族-步对应由规划期按现有 hex 逐族比对后定,并写入围栏注释。 — **Reversibility:** costly — 换族要重写全部强调色值。
- **D-08:** 当第 11 步在某背景上过不了 4.5:1 时,**换背景步**(把该背景提到更浅的步,如 gray-1/2),**保住 muted = 11 / 正文 = 12 的同族层级结构**。不把 muted 提到 12 步(那会让 ORDER 断言失去同族内的序依据)。 — **Reversibility:** costly — 回退要重新分配全部表面/边框的步。
- **D-09:** **全部颜色角色都重映射**:底(1-2)/ 组件底(3-5)/ 边框(6-8)/ 实心填充(9-10)/ 文字(11-12)。即 goal 的字面。代价(已接受):边框与实心填充也换值,这是本阶段最大的视觉面。 — **Reversibility:** costly — 半途回退会留下「Radix 值与手调 hex 并存」的半迁移状态(Pitfall 1)。

### UAT 3 项消解口径

UAT 的 20 条失败按性质分四类,答案不同:

- **D-10:** **颜色值漂移**(`.hint` / `.badge-answered` / `#state-badge` / `.chat-user` / `#ai-route-select` 与 `#selection-menu` 的 border-top-color / `.markdown-body` / `.hint` 背景)**随重写消解** —— 这些值本来就要全换。
- **D-11:** 被 260918-qrq **删除的两条声明都恢复**:`#state-badge` 的 `z-index: var(--z-badge)` 与 `.overlay-card` 的 box-shadow。理由:SC2 要求「无增删声明」,这两条删除是 260918-qrq 遗留的 SC2 偏差;且 `#state-badge` 的 z-index 被删后 `--z-badge: 10` **失去了消费者**,而围栏 L152-153 明写 `badge < banner` 是 b9664e0 FIX 2 的**承重序关系** —— TOKEN-07 断言的序关系现在没有一端被消费,这是正确性问题而非观感问题。恢复 box-shadow 需要**新立一个 shadow 令牌**(否则围栏外出现裸 `rgba`)。
- **D-12:** 间距 / 字号的 7 条漂移(`.panel-header` padding 10/16→6/10;5 处 font-size 14/16/18/24)**更新 UAT 期望值接受 HEAD 现状**。理由:04.1 明令不改 S-1/S-2;且 `6px` = `--space-1-5`、`10px` = `--space-2-5` 都是刻度内合法档。**附带必做:复核 Phase 5 SC5 / Phase 6 SC5 下游门引用的具体字号**(UAT 已单列 `S-2 DEPENDENCY --text-base = 14px` 并 PASS,但下游门引用的其它字号需一并核对)。
- **D-13:** UAT 里 `#doc-pane` 这条 BLOCKED **改 UAT 为 `#doc-panel-body`**。硬规则 5 明写「`app.js` 约 70 个顶层 `getElementById` 句柄的 id 不得改名或删除」。实测 `#doc-panel-body` 的 padding 32px/40px 与期望一致,只是名对不上。
- **D-14:** UAT 断言**全部改为令牌接线表述** —— 运行时读 `getComputedStyle` 解析出的 `--token` 值再比对,不再硬编码 rgb。`scripts/check-05-ui-uat.py` 的 test 6 已用这个写法并 PASS。这是根因的**结构性修复**:令牌值层改动不再产生一批假 FAIL(本次 20 条假 FAIL 的根因正是期望值定稿于值层改动之前)。 — **Reversibility:** costly — 回退要重写全部断言,且这确实牺牲了「硬编码值能抓令牌接错线」的那部分检测力。

### 两个补讨论的空白

- **D-15:** CHECK-02 配对清单重算后**按实际落地对重新枚举**,规模随之增减。依据:围栏 L160-166 自述的契约是「枚举真实发生的组合」,不是覆盖面指标。附带记档:ROADMAP Phase 4 写 24 对(20 文本 + 4 非文本)、磁盘现状是 34 对(29 TEXT + 5 NON-TEXT,另 1 条 ORDER)、goal 写 34 —— 三个数字的差异需在计划中说明。
- **D-16:** `PAIR --color-text-muted ON --gray-100 TEXT`(`--gray-100` = `--color-surface-hover`)**先当作一项待核事实**。已核实的静态证据:`--color-surface-hover` 只有**一个**消费者 `button:hover`(L353);`--color-text-muted` 的消费者是 `.hint` / `.markdown-body blockquote` / `.badge-answered` / `.annotation-plain .annotation-note` / `.annotation-answer summary` / `.verdict-suggestion`,全是 `<p>` / `<span>` / `<summary>` / `<div>`;扫过 `index.html` 全部 `<button>` 块,**没有任何一个包含 muted-text 类的元素**。若核实 `app.js` 动态渲染后仍不成立,就从清单删掉该对,hover 底保持足够可见的步 —— **「hover 变浅」的代价随之归零**。

### Claude's Discretion

- 每族具体取哪个 Radix 族与哪几个步(在 D-06/D-07/D-08 的原则下),由规划期按现有 hex 逐族比对后定。
- 恢复 `.overlay-card` box-shadow 所新立的 shadow 令牌的**命名与形状**。
- 围栏内注释的措辞与粒度(映射表怎么写、步语义怎么标注)。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 本阶段的直接上游(必须读)
- `.planning/ROADMAP.md` §Phase 04.1 — 本阶段的 goal 与「非紧急插入」说明
- `.planning/ROADMAP.md` §全局硬规则 1-7 — 每个计划都适用;特别注意规则 3「追加不重排」与规则 6「零新增依赖/构建步骤」
- `.planning/phases/idi-04-tokens-contract/idi-04-UAT.md` — 3 项 FAIL 的逐条 expected/actual,以及 `## Gaps` 里的单条根因(令牌值层换血 `448686b`)
- `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` — **颜色两节之外的权威来源**;本阶段只重写它的 Color 与 Contrast Verification 两节
- `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` §Notes N-1…N-5 — 值层决策的来由(N-1 是 muted 值最可能被「好心改回」的警告)
- `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` §Sign-Off Items — S-1…S-4,本阶段不得重新讨论,也不得执行任何一行式替代方案
- `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` §The Four Contract-Check Commands — 四条命令的规格

### 代码面
- `frontend/style.css` L5-L224 — 围栏 `:root` 令牌块 + CHECK-02 的 `/* PAIR */` 配对清单(以注释形式与令牌同一 diff)
- `frontend/style.css` L353 — `button:hover`,唯一消费 `--color-surface-hover` 的规则(D-16 的核实对象)
- `scripts/check-02-contrast.py` — 从围栏读配对清单、算真实 WCAG 比值;零依赖、只读、对未声明令牌名大声失败
- `scripts/check-01-token-conformance.sh` — 块外裸 hex 必须为 0
- `scripts/check-03-hidden-uniqueness.sh` / `scripts/check-04-important-count.sh` — 两条不变量守卫
- `scripts/check-05-ui-uat.py` — Playwright UAT harness(`--item N` 单跑;test 6 是「令牌接线表述」的范本)
- `scripts/ui-states/` — p1 / p12 / p3 / checking / archive 五个磁盘状态样本

### 需求与状态
- `.planning/REQUIREMENTS.md` §TOKEN / §CHECK — TOKEN-01…08、CHECK-01…04
- `.planning/REQUIREMENTS.md` §A11Y — A11Y-04 / A11Y-04b(本阶段消解其倒退)
- `.planning/STATE.md` §Blockers/Concerns — AA 倒退与 UAT 漂移两条的完整记录
- `.planning/STATE.md` §Operator Next Steps — 三步路线(discuss → ui-phase → plan)与 S-1…S-4 的签核原文
- `DESIGN.md` — 项目唯一权威设计文档;§3.8 语言红线

### 外部
- Radix Colors 官方文档(12 步语义刻度)—— **注意:本次会话的 web 访问被阻断,未能核对官方文档。** 12 步语义(1-2 底 / 3-5 组件底 / 6-8 边框 / 9-10 实心填充 / 11-12 文字)作为**工作假设**记录;其 AA 论断**不采信、不作为依据** —— 一律由 `scripts/check-02-contrast.py` 算出的真实比值仲裁。

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **围栏 `:root` 令牌块**(`frontend/style.css` L5-L224):单一事实源。本阶段的全部改动面都在这里面。
- **`scripts/check-02-contrast.py`**:从围栏读 `/* PAIR --fg ON --bg TEXT|NON-TEXT[@alpha] */` 清单,算真实 WCAG 相对亮度比值。零依赖(仅 `re`/`sys`)、只读、对**未声明的令牌名**大声失败(exit 1)——所以清单与令牌块无法漂移。本阶段重算清单后直接复用它验证。
- **`scripts/check-05-ui-uat.py`**:Playwright harness,5 个磁盘状态样本,支持 `--item N` 单跑与 `--ai-smoke`。test 6 演示了「按令牌接线表述」的断言写法(D-14 的范本)。
- **`scripts/ui-states/`**:p1 / p12 / p3 / checking / archive 五个状态样本,幂等、仓库样本只读。

### Established Patterns
- **「与消费者同提交」纪律(Hard Rule 5)**:绝不声明一个在同一次提交中不消费的令牌 —— 直接约束 D-04。
- **「最浅的通过值」原则(Pitfall 4a)**:对比度修到比值却毁掉层级是本项目已记录的失败模式;取最浅的通过值,并断言层级关系。
- **配对清单以令牌名书写于围栏内**:清单与令牌同一 diff,漂移可见。这是 CHECK-02 设计里最关键的一条。
- **ORDER 断言取严格序关系而非阈值门**:`ratio(quieter) < ratio(louder)`;UI-SPEC 已显式接受 0.311 对 ≤~0.30 guide 的残差,阈值门会在 HEAD 上立即失败。
- **追加,不重排**(硬规则 3):至少一对等特异性规则由源码顺序决定,重排即渲染变更而 diff 看起来完全无辜。

### Integration Points
- **唯一改动面** = `frontend/style.css` 的围栏内(L5-L224)+ 两处围栏外的声明恢复(D-11:`#state-badge` 的 z-index、`.overlay-card` 的 box-shadow)。
- **`frontend/vendor/` 保持只有 `marked.min.js`** —— Phase 4 gate 的原始断言,本阶段不动它(D-01)。
- **`scripts/check-02-contrast.py` 的配对清单**随令牌重算(D-15)。
- **`scripts/check-05-ui-uat.py` 的断言表述**改为令牌接线(D-14)。
- **`app.js` / `index.html` 零改动** —— 硬规则 5 的 id 不得改名。

</code_context>

<specifics>
## Specific Ideas

- **Radix 12 步语义**(工作假设,未经官方文档核对):1-2 底 / 3-5 组件底 / 6-8 边框 / 9-10 实心填充 / 11-12 文字。用户选定的映射方案直接采用这组语义。
- **AA 倒退的结构性解法**:muted = 第 11 步、正文 = 第 12 步 —— 把「muted 比正文更浅、但两者都过 AA」变成**刻度内的两个相邻档**,而不是手调出来的折中(现状 `--gray-600` 与 `--gray-700` 同值 `#8f8f8f`,围栏 L12 自陈是「AA 倒退为用户知情决策」)。
- **不采信 Radix 的 AA 论断**:一律以 CHECK-02 算出的真实比值为准。这是本阶段最重要的方法论立场 —— 上游文档的保证在**我们的**背景组合上未必成立,而 CHECK-02 恰好就是为了回答这个问题存在的。

</specifics>

<deferred>
## Deferred Ideas

- **暗色模式 / `prefers-color-scheme`** —— v2 `TOKEN-V2-01`;本阶段与 v1.14 全局均已排除。
- **`#state-badge { right: 448px }` 魔法数消除** —— `LAYOUT-01`,Phase 6。UI-SPEC 的 L-5 已记录它是**非 hex 字面量**,CHECK-01 不管它。
- **`.overlay-card` box-shadow 令牌的最终形状** —— 本阶段只要求「新立一个 shadow 令牌」使其不成为围栏外裸 `rgba`;具体层数/参数由规划期定。
- **`#probe-controls` 的移除或重定位** —— 产品行为变更,v1.14 全局已裁定不进任何阶段。
- **Phase 5 的实心填充分化**(`--color-action-irreversible` 从与 routine/commit 共享值改为独立处理)—— 本阶段保持三族共享值不动,只把它指向 Radix 的对应步。

</deferred>

---

*Phase: 04.1-radix*
*Context gathered: 2026-09-19*
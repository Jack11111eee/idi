# Roadmap: 交互式讨论迭代系统

## Milestones

- ✅ **v1.13 交互式讨论迭代系统 MVP** — Phases 1-3 (shipped 2026-09-13) — 20 条需求(FLOW 7 / UI 4 / AI 5 / DATA 4)全部交付 — 详见 `milestones/v1.13-ROADMAP.md`
- ✅ **v1.14 前端视觉与可访问性** — Phases 4-8 (shipped 2026-09-26) — 38 条需求(TOKEN 8 / VISUAL 5 / TYPE 3 / A11Y 9 / LAYOUT 4 / INTERACT 2 / CHECK 4 / REG 3)全部交付 — 详见 `milestones/v1.14-ROADMAP.md`
- ✅ **v1.15 视觉构图升级** — Phases 9-10 (shipped 2026-09-28) — 12 条需求(CARD 3 / VIS 2 / REG 2 / TABLE 2 / RADIUS 2 / REG-03)全部交付 — 详见 `milestones/v1.15-ROADMAP.md`
- ✅ **v1.16 界面去卡片化 —— 连续面与发丝分隔线** — Phases 11-12 (shipped 2026-09-30) — 12 条需求(SURF 3 / DIV 3 / REG 4 / G1 1 / VIS 1)全部交付 — 详见 `milestones/v1.16-ROADMAP.md`

## Phases

<details>
<summary>✅ v1.13 交互式讨论迭代系统 MVP (Phases 1-3) — SHIPPED 2026-09-13</summary>

- [x] **Phase 1: 行走骨架——服务器、单界面与阶段 1-2 会话** (4/4 plans) — completed 2026-09-09
  启动自检 CLI、选目录进入单界面、状态由磁盘推导、阶段 1-2 连续会话(transcript 恢复)、AI 双轨调用与事件直播、发散模式、G1 认可雏形
- [x] **Phase 2: 轮次收敛循环——划词批注、G2 与机器文法** (4/4 plans) — completed 2026-09-10
  划词批注与大白话双轨、处理本轮批注产出下一轮、上轮冻结只读、§6.4 文法机械校验、annotations 字段写回
- [x] **Phase 3: 授权、自检与终点——G3、档位、使命完成归档** (5/5 plans) — completed 2026-09-13
  G3 四处校验与确认词、DESIGN.md.tmp 原子落盘、宽松/严格自检循环与 D-22 残余裁决、崩溃自愈、完成态只读归档

**Milestone scope:** DESIGN.md v1.13 全部 20 条需求(FLOW 7 + UI 4 + AI 5 + DATA 4)交付并验证。
验证记录:各阶段 `*-VERIFICATION.md`(Phase 1: 8/8 真值、Phase 2: 7/7 SC、Phase 3: 5/5 ROADMAP 判据)与 `*-UAT.md`(6/6、7/7、8 检查点)均 passed。

</details>

<details>
<summary>✅ v1.14 前端视觉与可访问性 (Phases 4-8) — SHIPPED 2026-09-26</summary>

- [x] **Phase 4: 设计契约、令牌层与契约校验** (3/3 plans) — completed 2026-09-20
  书面 UI-SPEC(含含义清单)+ 单一 `:root` 令牌块 + 全部字面量替换 + 四条契约校验命令
- [x] **Phase 4.1: Radix 颜色族重写** (4/4 plans) — completed 2026-09-20
  颜色族从手调 hex 换成 Radix Colors 12 步语义刻度(25 primitive / 47 `--color-*`),CHECK-02 清单重算为 43 对
- [x] **Phase 5: 排版与视觉层级** (4/4 plans) — completed 2026-09-21
  markdown 正文字号受控、不可逆动作权重、页面级层级、面板活动态、两处内联 SVG
- [x] **Phase 6: 布局稳健性** (4/4 plans) — completed 2026-09-22
  魔法数消除、窄窗口不破版、滚动容器收敛、24×24 命中区
- [x] **Phase 7: 交互状态与焦点样式** (3/3 plans) — completed 2026-09-23
  hover/active/disabled/transition + 全站 `:focus-visible`
- [x] **Phase 8: 可访问性语义与键盘** (3/3 plans) — completed 2026-09-24
  唯一触碰 `app.js`/`index.html` 的阶段:tabindex、划词焦点交接、Escape、dialog 语义、内联错误结构修复、五条修复回归复验

**Milestone scope:** 六支柱 UI 审计 13/24 的 13 项**显式延后项**——延后理由一致:修法本身就是设计决策,必须先定契约再落地。38 条需求全部交付;6/6 阶段在 `0b6283a` 复验 `passed`。
**回归面(本里程碑最高风险):** 5 条功能性 BLOCKER 的修复(`b9664e0`)全部依赖本里程碑重写的 CSS 且无自动化覆盖 —— 已由 Phase 8 的 REG-03 全量人工重跑收口。
**收口期发现的跨阶段回归:** Phase 6 的 L-4 滚动容器收敛静默杀掉了 AI 事件自动跟随(`app.js:253` 的 `scrollTop` 赋值按 CSS 规范成为 no-op),而当时的 `check-05 --item 9` 不但零覆盖该回归,还正面断言了它的前提。已修复(追加节点上 `scrollIntoView({ block: 'nearest' })`,不回退 L-4)并新增一条经变异证明会失败的门。
**验证记录:** `milestones/v1.14-phases/` 各阶段 `*-VERIFICATION.md` 与 `*-UAT.md`;里程碑审计 `milestones/v1.14-MILESTONE-AUDIT.md`(`status: passed`,`remediated: 2026-09-25`)。

</details>

<details>
<summary>✅ v1.15 视觉构图升级 (Phases 9-10) — SHIPPED 2026-09-28</summary>

- [x] **Phase 9: 卡片容器化与页面底色下沉** (3/3 plans) — completed 2026-09-26
  左栏 4 个面板与右栏文档区成为白底卡片;页面底色下沉至 gray-3,形成 gray-3 < gray-2 < 白 三级 elevation 刻度;受影响的对比度对重算并登记;五条 UI 门复跑无新增失败
- [x] **Phase 10: 表格重做与圆角刻度收敛** (4/4 plans) — completed 2026-09-27
  文档表格由「每格 1px 全边框」改为「表头浅底 + 仅横向分隔线」;圆角刻度收敛为 8 / 10 / 胶囊三档,删掉未并入刻度的 `--radius-lg: 28px`;两项均不引入新颜色值、不放宽阈值、不新增 `!important`

**Milestone scope:** 12 条需求(CARD 3 / VIS 2 / REG 2 / TABLE 2 / RADIUS 2 / REG-03)全部交付并验证。范围裁定两次均由用户逐项作出:Phase 9 先只做卡片化(「开一个 phase,先看看效果吧」),用户看过截图后裁定「表格重做, 圆角刻度收敛。做这两个」⇒ 另开 Phase 10;第三项候选(图标与空状态)**未点名,仍留 Out of Scope**。
**验证记录:** Phase 9 `passed` 24/24(收口前经用户裁定追加一次强度微调 quick `260926-vaf`,已按「以 HEAD 内容重新验证」处置,非刷新指纹);Phase 10 `passed` 62/62。里程碑审计 `milestones/v1.15-MILESTONE-AUDIT.md`(`status: tech_debt` —— 12/12 需求满足、无 critical blocker,14 项已登记 tech debt 待用户裁定)。
**产品面:** 仅 `frontend/style.css`(+258)与 `scripts/`(新 `check-09` / `check-10` / `probe-card-border-token.py`,`check-05` +10);后端与 `app.js` / `index.html` 逐字节未改。
**v1.16 与本里程碑的关系:** v1.16 **反转** Phase 9 的卡片语言(D-9-1 / D-9-2 / D-9-3 是一次已 shipped 的用户裁定,用户 2026-09-28 看过成品后逐项裁定反转);本里程碑审计登记的 **G1**(`#latest-check` 表头 band 消失)由用户裁定「连带」纳入 v1.16 的 `G1-01`。Phase 9 引入的 **sticky 余量为零**由 v1.16 的 `REG-03` 处置。

</details>

<details>
<summary>✅ v1.16 界面去卡片化 —— 连续面与发丝分隔线 (Phases 11-12) — SHIPPED 2026-09-30</summary>

- [x] **Phase 11: 去卡片化与发丝分隔线** (5/5 plans) — completed 2026-09-29
  左栏 4 个 section 与 `#doc-panel` 移除边框/阴影/圆角、面板与页面统一为同一档底色、12px 灰缝与 768px 居中侧沟归零;分区改由 1px 发丝线承担(主区↔文档区竖线跨满高、左栏面板间横线);同步改写 `check-09` 的 c1..c4 并以变异证明其会失败、重新归属 `check-02` 的卡片地面配对、复测 `check-05 --item 8` 的 sticky 余量
- [x] **Phase 12: G1 表头 band 与里程碑收口** (3/3 plans) — completed 2026-09-29
  `#latest-check` 内表头读作独立 band(宿主绘制面与表头底色不再同令牌相撞,以运行时读数 + 截图取证);五条浏览器门 + 四个静态门 + pytest 基线复跑零新增失败;连带作废的 `passed` 报告按既有口径逐份处置;5 张 1440×900 整窗截图

**Milestone scope:** 12 条需求(SURF 3 / DIV 3 / REG 4 / G1-01 / VIS-01)全部交付并验证;2/2 阶段 `passed`,跨阶段集成 10/10,E2E 五状态全部在像素级走通。
**本里程碑的性质:反转,不是新增。** 反转对象是 v1.15 Phase 9 的卡片语言(D-9-1 / D-9-2 / D-9-3)—— 一次已 shipped 的用户裁定。用户 2026-09-28 看过成品后逐字裁定:「分块太割裂了,完全没有联动性…chatgpt 的界面就是一根细的衬线来分割不同的分区,我们的确实很大的一块」。故**门禁同步是承重需求**:`check-09` 的 c1..c4 逐条断言卡片语言,反转后必然全红;判据被改写为断言新契约,并以变异测试证明其会真的失败(不得删除、不得降级为恒真)。范围裁定(用户,2026-09-28,逐项):视觉方向 = 全站去卡片;落地方式 = 走 GSD 新阶段;范围 = 去卡片化 **连带 G1**;跳过领域研究。
**验证记录:** Phase 11 `passed` 12/12 must-haves(经四轮 re-verification);Phase 12 `passed` 15/15。里程碑审计 `milestones/v1.16-MILESTONE-AUDIT.md`(`status: tech_debt` —— 12/12 需求满足、无 critical blocker、无 orphan,15 项 tech debt 已登记)。
**产品面:** 仅 4 个源文件,`+959 / −317` 行(`frontend/style.css`、重写的 `scripts/check-09-idi09-validation.py`、`scripts/check-05-ui-uat.py`、`scripts/ui-states/checking/docs/DESIGN-check-2.md`);`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` / `backend/` 自里程碑基址至 HEAD **逐字节为空**。

</details>

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. 行走骨架 | v1.13 | 4/4 | Complete | 2026-09-09 |
| 2. 轮次收敛循环 | v1.13 | 4/4 | Complete | 2026-09-10 |
| 3. 授权、自检与终点 | v1.13 | 5/5 | Complete | 2026-09-13 |
| 4. 设计契约、令牌层与契约校验 | v1.14 | 3/3 | Complete | 2026-09-20 |
| 4.1. Radix 颜色族重写 | v1.14 | 4/4 | Complete | 2026-09-20 |
| 5. 排版与视觉层级 | v1.14 | 4/4 | Complete | 2026-09-21 |
| 6. 布局稳健性 | v1.14 | 4/4 | Complete | 2026-09-22 |
| 7. 交互状态与焦点样式 | v1.14 | 3/3 | Complete | 2026-09-23 |
| 8. 可访问性语义与键盘 | v1.14 | 3/3 | Complete | 2026-09-24 |
| 9. 卡片容器化与页面底色下沉 | v1.15 | 3/3 | Complete | 2026-09-26 |
| 10. 表格重做与圆角刻度收敛 | v1.15 | 4/4 | Complete | 2026-09-27 |
| 11. 去卡片化与发丝分隔线 | v1.16 | 5/5 | Complete | 2026-09-29 |
| 12. G1 表头 band 与里程碑收口 | v1.16 | 3/3 | Complete | 2026-09-29 |

**四个里程碑共 12 个阶段全部收口。** v1.16(界面去卡片化 —— 连续面与发丝分隔线)已 shipped 并归档于 2026-09-30 —— Phase 11 交付反转本体(连续白面 + 1px 发丝分隔线)与其三条承重门禁同步义务,Phase 12 交付 G1 表头 band 定点修复与里程碑收口;12/12 需求满足,里程碑审计 `status: tech_debt`(无 critical blocker、无 unsatisfied 需求、无 orphan,15 项 tech debt 已登记待裁定)。

**v1.16 的性质是反转,不是新增** —— 它整体推翻了 v1.15 Phase 9 的卡片语言(D-9-1 / D-9-2 / D-9-3 是一次已 shipped 的用户裁定,用户 2026-09-28 看过成品后逐项裁定反转)。因此 `check-09` 的 c1..c4 在反转后**必然全红**,那正是门在正确工作的证据;判据被改写为断言新契约,并以六条变异测试逐条证明其会真的失败。

**下一步 = 启动 v1.17 里程碑**(`/gsd-new-milestone`)。v1.16 审计登记的待裁定项:①**REG-02 范围缺口** —— `style.css:740-742` 的 PAIR 归因散文仍描述已不存在的地面(两条受守护的 PAIR 在任一面均 ≥ `NON_TEXT_MIN` ⇒ 门绿,错的是**归属**),`style.css:716-717` 同型第二处,`check-05:827` 的 `5.77` 读数已过期(现为 5.92);②**G2** —— `--radix-gray-1` 已声明但零消费;③`check-09` c2/c4 断言重叠、`WR-01` 恒真、`WR-04` 登记数字写错;④**Nyquist 缺口** —— `idi-11` / `idi-12` 无 `VALIDATION.md`(建议 `/gsd-validate-phase 11` 与 `12`);⑤3 份未跟踪文件(`scripts/.check09-old.py` 等)。另:`999.1` 已关闭,`999.2`(Phase 7 三条既有 affordance 缺陷)仍在 Backlog,执行它会作废 `idi-07` 的 `passed` 指纹,须连带重新验证。

## Backlog

### Phase 999.1: Phase 4 残留的两条卫生项 (BACKLOG)

**Goal:** 清掉 Phase 4 收口后遗留、已由用户裁定为 Phase 4 范围外的两条小项。二者都是「已记录但无人认领」的真项,不是延期项。

1. **`.collapse-indicator` 的越轨字面量** —— `frontend/style.css:434` 为
   `.collapse-indicator { font-size: 20px; line-height: 1; }`,围栏外两个裸字面量,属 Phase 4 已令牌化的
   `--text-*` / `--lh-*` 族,且在 `04-UI-SPEC.md:841` 的封闭例外清单(L-1…L-5)之外。
   由 quick 任务 `260918-qrq`(`3684353`,2026-09-18 20:01)在 Phase 4 收口(`0c658aa`)之后引入;
   Phase 4 自己的提交区间干净。已在 `idi-04.1-UI-REVIEW.md` Pillar 4 记分(3/4,「undeclared 6th size」)。
   **HEAD 字号刻度为 12 / 14 / 16 / 18 / 24 —— `20px` 不在刻度上,故修法是排版决策而非机械替换**:
   加一档(改刻度,牵动 UI-SPEC 的「5 sizes」声明与 S-2 `--text-base = 14px` 的下游门)、重映射到 `18px`/`24px`
   (改已出货的 ▾/▸ 视觉),或加一条 L-6 例外(不改 `style.css`,但 `20px` 永久留在出货 chrome 里)。
   **注意:** 任何对 `frontend/style.css` 的编辑都会作废 `idi-04.1-radix` 的 `passed` 指纹(其 `covered_files`
   含该文件,digest 为原始字节 sha256),需连带复验 04.1。另见 Phase 5 Pitfall 7:`app.js:1550` 用 `textContent`
   赋值 `.collapse-indicator`,触碰它时不得引入内联 `<svg>`。
2. **`scripts/check-05-ui-uat.py:588` 的陈旧诊断文案** —— 仍打印「`--color-text-muted` … 变为 #8f8f8f,
   低于 AA 4.5:1」,而 HEAD 实为 `rgb(100,100,100)`、在 `--color-surface` 上 5.62 达标。周围断言正确,
   仅该 INFO 行陈旧。**改它同样会作废 04.1 的指纹**(该脚本也在 04.1 的 `covered_files` 里),
   故与第 1 项合并为同一批处理,一次性连带复验 04.1。

**裁定记录:** `idi-04-VERIFICATION.md` frontmatter `overrides:`(`accepted_by: Jack11111eee`,2026-09-20)与
其 Gaps Summary。未写进 Phase 5 的理由:Phase 5 的 Pitfall 7 把触碰 `.collapse-indicator` 的范围锁死为
两处 `content:` emoji,其 SC1 只点名四处 chrome 覆盖 —— 插入新交付物等于改写已签核的门。

> ✅ **已于 2026-09-25 关闭** —— quick `260925-iin` 同时处置了两项:第 1 项按用户裁定**加第 8 档字号**
> (`--text-lg-plus: 20px` + `--lh-none: 1`,字形渲染尺寸不变);第 2 项把陈旧 INFO 串更正为
> `rgb(100,100,100)` / 5.62:1 达标,未改任何断言。该 quick 同时新增一条经变异证明的自动跟随门
> (`check-05 --item 9`)与一条 `FOCUSABLE_SELECTOR` ↔ `:focus-visible` 对齐门(`check-07` 静态守卫 ⑤)。
> 连带复验:因 `frontend/style.css` 与 `scripts/check-05-ui-uat.py` 变更,`idi-04.1-radix` 与 `idi-07` 的
> 指纹作废 —— 六个阶段的指纹最终全部作废,并在收口前逐份以 HEAD 内容重新验证通过。见
> `.planning/milestones/v1.14-phases/idi-04-tokens-contract/idi-04-VERIFICATION.md` 与 `idi-05-*/idi-05-UI-SPEC.md`。

**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /gsd-review-backlog when ready)

### Phase 999.2: Phase 7 交互态契约暴露的三条既有 affordance 缺陷 (BACKLOG)

**Goal:** 清掉 `idi-07-UI-REVIEW.md`(2026-09-23,19/24)在建立「每个交互控件对 hover / active / disabled
有可辨反馈」这条契约时**暴露出来**的三条缺陷。三者都不是本阶段改动引入的(第 1、2 条是 Phase 7 之前就在的
affordance 谎报;第 3 条虽属 Phase 7 自己那份 PAIR 清单,但补它要动 `style.css` ⇒ 作废刚过的指纹),
但都只有在 Phase 7 的契约下才成为可判定的项。

1. **`#session-panel .panel-header` 宣称了一个不存在的点击** —— `frontend/style.css:665-674` 的基类
   `.panel-header` 规则体带 `cursor: pointer` + `user-select: none`,但只有 `#ai-panel-header` 与
   `#doc-panel-header` 有监听(`frontend/app.js:1561` / `1567`)。文件自己的惯例是对不可点的两个面板显式复位:
   `#annotations-panel .panel-header { cursor: default; }`(`style.css:1085`)与
   `#checks-panel .panel-header { cursor: default; }`(`style.css:1304`)。
   `#session-panel .panel-header`(`frontend/index.html:15`,该 header 无 id)两者皆无 ⇒ 鼠标移到「会话流」
   标题上会得到可点的指针。**修法:** 按既有惯例补一条 `#session-panel .panel-header { cursor: default; }`
   (一条声明,零重排)。
2. **`.annotation-answer summary` 没有任何交互态,也没有运行时覆盖** —— `style.css:1189` 定义了它;它带
   `cursor: pointer`、受 Phase 6 的 A11Y-07 门约束(24×24 命中区)、并被 Phase 7 的焦点环覆盖
   (`style.css:1513` 的七选择器含 `summary`),但**没有任何 `:hover` / `:active` 规则**,也不在过渡挂载规则里
   (`style.css:1675` 只覆盖 `button, input, select`)。更关键的是:**三个样本里没有任何 fixture 会渲染出
   `<summary>`**,故 item 10 的焦点环普查(每样本 28 个元素)从未见过它 —— 它的「已覆盖」是名义上的。
   **修法(两半,缺一不可):** 把 `summary` 并入朴素按钮的 hover 组;**并且**在 `p3` fixture 里加一个
   `summary`,或按 D-18 对 `a[href]` 的先例把该缺口**显式登记**。只做前半场会让「已覆盖」继续是名义的。
3. **焦点环的 PAIR 清单漏掉一处它真实渲染其上的底色** —— `style.css:498-507` 的清单列三处验证面
   (`--color-surface` / `--color-surface-page` / `--color-surface@0.75`),并**显式论证**为何排除
   `--color-surface-sunken`,却对 `--color-surface-warning-subtle`(amber-1)只字未提。而
   `.verdict-card`(`style.css:1341`,底色即该令牌)正是 item 10 在 `checking` 样本里实测
   `.verdict-note-input` 与两个 `.verdict-buttons button` 的宿主 —— 焦点环在这处底色上确实渲染。
   这是**与本文件自订纪律的直接冲突**:`style.css:435-437` 逐字写明「a token drawn as a UI boundary must
   have its own NON-TEXT pair on each ground it is drawn on」,而兄弟令牌 `--color-border-hover` 正是按这条
   纪律补上了这一处底色(`7b4ae18`,+3 ⇒ 53 对);`--color-focus` 同为 UI 边界却漏了同一处。
   实测环色在其上为 **5.77:1(达标)** ⇒ 这是**覆盖一致性缺陷,不是可辨性缺陷**。
   **修法:** 补一条 `/* PAIR --color-focus ON --color-surface-warning-subtle NON-TEXT */`,与 `7b4ae18` 对齐。

**指纹影响(执行前必读):** `frontend/style.css` 与 `scripts/check-05-ui-uat.py` **同时**在
`idi-07-VERIFICATION.md` 的 `covered_files` 里(digest `v1:sha256:5964d53c…`)。第 1、2、3 条的修法都要动
`frontend/style.css`,第 2 条的后半场还要动 `scripts/check-05-ui-uat.py` —— 故本项一旦执行,`idi-07` 的
`passed` 指纹即失效,须**连带重新验证 idi-07**(与 999.1 对 `idi-04.1-radix` 的关系同型)。
建议三条合并为同一批处理,一次性连带复验。

**裁定记录:** `idi-07-UI-REVIEW.md`(19/24;Pillar 2 Visuals 2/4、Pillar 3 Color 3/4、Pillar 6 Experience
Design 3/4 的扣分主因即此三条)与 `idi-07-VERIFICATION.md`。未写进 Phase 7 的理由:第 1、2 条是**既有**
affordance —— Phase 7 只改了声明式 CSS 的交互态与焦点环,`frontend/app.js` / `frontend/index.html` 逐字节未改,
按外科手术式改动纪律不在本阶段边界内;第 3 条虽属 Phase 7 自己的清单,但补它要动 `style.css` ⇒ 作废刚过的
指纹,而 UAT 已 1/1 通过、阶段收口在即,故由用户裁定转为 backlog 而非当场展开。
**用户裁定:`2026-09-23`(本 backlog 条目的建立即该裁定)。**

**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /gsd-review-backlog when ready)

# Roadmap: 交互式讨论迭代系统

## Milestones

- ✅ **v1.13 交互式讨论迭代系统 MVP** — Phases 1-3 (shipped 2026-09-13) — 详见 `milestones/v1.13-ROADMAP.md`
- ✅ **v1.14 前端视觉与可访问性** — Phases 4-8 (shipped 2026-09-26) — 38 条需求(TOKEN 8 / VISUAL 5 / TYPE 3 / A11Y 9 / LAYOUT 4 / INTERACT 2 / CHECK 4 / REG 3)全部交付 — 详见 `milestones/v1.14-ROADMAP.md`

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

**全部 9 个阶段已收口。** 下一里程碑待 `/gsd-new-milestone` 定义。

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

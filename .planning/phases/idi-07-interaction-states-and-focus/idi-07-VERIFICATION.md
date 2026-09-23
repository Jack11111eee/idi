---
phase: idi-07-interaction-states-and-focus
status: human_needed
verified: 2026-09-23T09:18:28Z
score: 8/9 truths machine-verified + 1 named human item (5″)
covered_files:
  - .planning/phases/idi-07-interaction-states-and-focus/idi-07-01-PLAN.md
  - .planning/phases/idi-07-interaction-states-and-focus/idi-07-01-SUMMARY.md
  - .planning/phases/idi-07-interaction-states-and-focus/idi-07-02-PLAN.md
  - .planning/phases/idi-07-interaction-states-and-focus/idi-07-02-SUMMARY.md
  - .planning/phases/idi-07-interaction-states-and-focus/idi-07-03-PLAN.md
  - .planning/phases/idi-07-interaction-states-and-focus/idi-07-03-SUMMARY.md
  - .planning/REQUIREMENTS.md
  - frontend/style.css
  - scripts/check-05-ui-uat.py
  - scripts/probe-07-focus-composite.py
covered_digest: "v1:sha256:5964d53cc475ca2539dd68d78e0e08ace21fd18866d21096c075bb655ee6dcc0"
behavior_unverified: 0
overrides_applied: 0
coincidental_reliance_items:
  - truth: "焦点环在归档态(0.75 合成)下仍可辨认(SC3 后半场)"
    reason: fixture-only
    harden: "探针在 #round-doc 里注入一个 <a href> 才让该断言有服务对象;生产路径今天没有等价物(五个样本的 #round-doc 内 a[href] 计数为 0,D-18 已登记)。常驻算术半场(check-02 的 @0.75 = 3.45)不依赖该 fixture,故本条只降级探针的可外推性,不降级结论。Phase 8 给 #round-doc 加 tabindex=\"0\" 后该场景变为活体,届时须复跑探针"
human_verification:
  - test: "进入阶段 3(p3 样本)后把鼠标移到 #btn-authorize 上并停留/按下,观察它是否仍「一眼看出不可点」——是否被 hover / 按下点亮成可点的样子"
    expected: "禁用态一眼可辨,且悬停/按下时零视觉反馈(颜色不变亮、不变浅、无按压感);它作为 G3 前提条件唯一视觉信号的 0.55 淡化不被削弱"
    why_human: "这是关于感知的主张,不是关于数值的主张。机器半场(SC5′)覆盖的是另一条规则 .verdict-buttons button:disabled(opacity 0.5);#btn-authorize:disabled(opacity 0.55)今天没有任何机器断言读过它的 opacity,只被 L741 那条 gate 间接保护"
---

# Phase 7: 交互状态与焦点样式 (idi-07) Verification Report

**Phase Goal:** 每个交互控件对 hover / active / disabled 有可辨反馈,并有可见的键盘焦点环;过渡限定在明确允许的属性上且尊重减弱动效偏好。
**Verified:** 2026-09-23T09:18:28Z
**Status:** human_needed
**Re-verification:** No — **初次独立验证**。

> **本文件取代了同名的旧文件。** 旧 `idi-07-VERIFICATION.md` 是 `idi-07-03-PLAN.md` Task 3 要求的**阶段收口记录**,由 executor 撰写、并自陈「不声称独立验证」且刻意不声明指纹。本次复核独立重跑全部门与探针,重算了它对全部条目的判定,并补上 `covered_files` / `covered_digest`。**旧文件的 `status` / 分数 / 条目措辞一概不作为依据**;凡与 HEAD 冲突之处,以 HEAD 为准(见 §B)。
>
> **本报告验证的是 HEAD 树,不是 SUMMARY 描述的那棵树。** 计划执行之后又落了四个代码评审修复提交(`7b4ae18` / `774a79c` / `4d9cebd` / `8d08f38`),触及 `frontend/style.css`、`scripts/check-05-ui-uat.py`、`scripts/probe-07-focus-composite.py`。SUMMARY 早于这些修复,故多处行号与断言数与 HEAD 不符 —— 逐条登记在 §B。

## Goal Achievement

### Observable Truths

判定集 = 5 条 ROADMAP Success Criteria + 计划 frontmatter 中**不重复**的 must_haves truth。

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | **SC1** 键盘 Tab 到任一按钮 / 输入框 / 下拉,焦点环清晰可见 | ✓ VERIFIED | 三个样本(p1 / checking / p3)各自 `page.keyboard.press("Tab")` 后读**当前 `document.activeElement`** 的计算值:`outline-width == "2px"`、`outline-offset == "2px"`、`outline-color == rgb(31, 99, 189)`(运行时解析的 `--color-focus`),`focusVisible == True`。期望侧全部来自运行时令牌解析,无硬编码 rgb |
| 2 | **SC2** 鼠标点击控件**不**出现焦点环(`:focus-visible` 语义成立) | ✓ VERIFIED | 先 Tab 让环出现(证明规则此刻是活的),再 `page.click("#btn-send")`,断言点击后 `document.activeElement` 就是它,且 `outline-color` 为 `rgb(255, 255, 255)` != 环色。三步缺一即空转,均已落地 |
| 3 | **SC3** 焦点环在冻结轮次(0.55)与归档态(0.75)下仍可辨认 | ✓ VERIFIED | **归档半场**:`check-02` 的 `--color-focus ON --color-surface NON-TEXT@0.75` = **3.45 ≥ 3**(WCAG 1.4.11);一次性探针 `probe-07` 在真实渲染上实测 `composited=(86,136,204) ratio=3.45`,exit 0。**冻结半场**:`opacity: 0.55` 已由 Phase 4 的 S-4(`4f323c0`)删除,`#round-doc.round-frozen`(L1239-1240)今天只剩 `filter: saturate(0.6)` + 琥珀竖条 ⇒ **0.55 合成背景已不存在**,该半场无服务对象(见 §C-1 与 §D-3) |
| 4 | **SC4** 把侧栏滚到底部再 Tab,焦点环不被裁切 | ✓ VERIFIED | 探针**先走应用自己的渲染路径撑高**容器(`renderEvent` / `renderMarkdown`),回读三元组确认真可滚:`#main-pane` [1740, 2640, 900]、`#doc-panel` [4348, 5248, 900] ⇒ 「滚到底」是真到达的状态,不是 no-op;再 Tab 12 次逐行测 clearance,判定 11 行全部 >= `CLEARANCE_MIN_PX = 4.0`(实测 40 / 129.5 / 130 / 252)。撑高后仍无容器可滚则 `blocked(...)`,不记 PASS |
| 5 | **SC5a** 交互控件有 hover / active 反馈 | ✓ VERIFIED | 填充族:`#btn-send` hover 时 `background-color` **不变**且 `box-shadow` 出现 `inset 0 0 0 999px` 叠层,颜色 == 运行时解析的 `--color-overlay-hover`;按住不放叠层换为 `--color-overlay-active` 且 != hover 读数。朴素族:`rgb(249,249,249) → rgb(240,240,240) → rgb(232,232,232)`,且断言 ③ != ②。输入控件:`#message-input` 与动态 `.verdict-note-input` 的 `border-color` `rgb(141,141,141) → rgb(100,100,100)`(且 != 静默值) |
| 6 | **SC5b** `#btn-authorize` 的禁用态**仍一眼看出不可点**(未被软化) | ⚠️ NEEDS HUMAN | 机器半场(SC5′)覆盖的是**另一条规则** `.verdict-buttons button:disabled`(L1376,`opacity: 0.5`);本条的 `#btn-authorize:disabled`(L1260,`opacity: 0.55`)**今天没有任何机器断言读过它的 `opacity`**。见「Human Verification Required」 |
| 7 | 焦点环**元素普查**:判定集(可见 ∧ 可聚焦)非空,且「未被环覆盖的元素数」为 0(D-16) | ✓ VERIFIED | 三样本各枚举 28 个实例;判定集分别 9 / 9 / 9 个元素,未覆盖 `[]`。判定集为空走 `blocked(...)` 而非 `info()+return`(空转 PASS 的形态已被显式封死) |
| 8 | 过渡只声明 `background-color` 与 `border-color`,时长 120ms;`reduce` 下全为 `0s`;`.event-list` 300ms 例外一个字节未改 | ✓ VERIFIED | 运行时实测 button / input / select 的 `transition-property == "background-color, border-color"`、`transition-duration == "0.12s, 0.12s"`;`.event-list` 为 `background-color` / `0.3s`;`page.emulate_media(reduced_motion="reduce")` 下四个目标**全为 `0s`**(判据先按 `,` 拆列表再逐项比,不用子串包含)。`git diff 69dea49 HEAD -- frontend/style.css` 中 `.event-list` 规则体(L748-757)**零行变动** |
| 9 | 阶段禁令面保持:焦点规则不设 `border` / `padding`;无 `outline: none`;无 `transition: all` / 通配;无 `@layer` / `@property` / `var(--x, #fallback)`;`!important` 声明数恒为 1;`@media` 计数与 `EXPECTED_MEDIA_QUERIES` 一致 | ✓ VERIFIED | 逐条机械核对(见「Anti-Patterns Found」与 §C-4):焦点规则块(L1508-1517)块内声明只有 `outline` / `outline-offset`;全文件无 `outline: none|0`;唯一的 `*` 规则是既有的 `* { box-sizing: border-box }`;唯一的 `!important;` 是 `.hidden { display: none !important; }`;`@media` 计数 1 == 常量 1 |

**Score:** 8/9 truths 机器验证通过;**第 6 条是具名人工项**(D-17 的 5″),不得换成机器代理量。`behavior_unverified: 0`(无「状态迁移 / 取消清理 / 顺序不变量」型 truth 未被测试覆盖)。

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `frontend/style.css` | 焦点环 / 交互态 / 过渡与减弱动效的追加规则 | ✓ EXISTS + SUBSTANTIVE + WIRED | `--color-focus: #1f63bd` 围栏内(L259)+ 7 选择器 `:focus-visible`(L1508-1517)+ `button:hover` 的 gate 与让位(L741)+ 朴素 `:active`(L1540)+ 填充 hover/active 叠层组(L1574-1585 / L1593-1604)+ input/select hover 组(L1637-1646)+ 过渡挂载(L1675)+ `@media (prefers-reduced-motion: reduce)`(L1695-1697)。**运行时消费已证**:环色被 `:focus-visible` 经 `var()` 消费,四个交互态令牌围栏内声明 == 1 且围栏外被 `var()` 消费 == 1(五条逐令牌断言) |
| `scripts/check-05-ui-uat.py` | 第 10 项的元素普查 + SC1/SC2/SC4/SC5/SC5′ + 四条静态契约守卫 + 过渡/减弱动效探针 | ✓ EXISTS + SUBSTANTIVE + WIRED | `item 10: PASS (41 条断言, 0 FAIL, 0 BLOCKED)`,exit 0。四条静态守卫 + 五条逐令牌断言 + 三样本运行时探针全部落地并被 `item10` 调用一次 |
| `scripts/probe-07-focus-composite.py` | 归档 0.75 合成的一次性反事实探针(**不进守卫契约**) | ✓ EXISTS + SUBSTANTIVE + WIRED | exit 0;自证非空转(`links-before=0` → 注入 → `links-after=1 (mutation-applied=yes)`);用运行时实测值复算 `check-02` 的 `composite()` 得 `ratio=3.45` |

**Artifacts:** 3/3 verified。`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` **零改动**(`git diff --numstat 69dea49 HEAD` 中不出现),与禁令一致。

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| `--color-focus`(L259) | `:focus-visible` 规则(L1515) | `outline: 2px solid var(--color-focus)` | ✓ WIRED | 围栏内声明 1 次、围栏外 `var()` 消费 1 次(静态守卫逐令牌断言);运行时 `outline-color` == 令牌解析值 |
| `:focus-visible` 枚举(L1508-1514) | harness 可聚焦普查集(`FOCUSABLE_SELECTOR`,L1748) | 逐字同集 | ✓ WIRED | **我逐字比对**:CSS 侧去 `:focus-visible` 后的列表 == 常量,7 项顺序亦同。harness 侧**已是单一事实源**(两份普查脚本经 `_focusable_census_js` 用占位符 `__FOCUSABLE_SELECTOR__` 从常量生成,IN-02 已修);**CSS 侧仍是字面量**,只能靠注释承诺 —— 但运行时普查对**样本中真实存在的**元素类仍构成行为级守卫(见 §C-3) |
| 过渡挂载规则(L1675) | `@media (prefers-reduced-motion: reduce)`(L1695-1697) | 同一次提交落地 | ✓ WIRED | 静态守卫证明两者**同时存在**;运行时 `reduce` 下四个目标全 `0s`。「同提交」是 git 维度事实,静态断言**在结构上无法证明**,门内 `info()` 已逐字声明该局限 —— 我核对提交历史:`4892fdf` 一次提交同时落 media 块与 `EXPECTED_MEDIA_QUERIES` 同步 |
| 过渡挂载规则(L1675) | `.event-list` 既有 300ms 例外(L756) | 无(刻意零竞争,不同元素) | ✓ WIRED | 运行时实测 `.event-list` 仍为 `background-color` / `0.3s`;`git diff` 中该规则体零变动 |
| `button:hover` 的 gate(L741) | `:where(button:not(:disabled)):active`(L1540) | 成对改写(让位 `:where(:not(:active))`) | ✓ WIRED | 运行时证明两半真的配套:朴素按钮 ③ 按住不放读数 != ② 悬停读数(`rgb(232,232,232)` != `rgb(240,240,240)`);若让位失效,③ 会读到 ② 的值,而「③ == surface-active」仍会成立 ⇒ 该「不相等」半条是判据本体 |

**Wiring:** 5/5 connections verified。

### Data-Flow Trace (Level 4)

本阶段是 CSS + 测试脚本,无数据渲染链路;唯一「值从声明流到消费者」的链路是令牌 → 渲染:

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `:focus-visible` 环色 | `outline-color` | `--color-focus` 围栏内声明(L259)→ `var()` 消费(L1515) | 是 — 运行时 `getComputedStyle` 读得 `rgb(31, 99, 189)`,且 == `resolve_color(page, "--color-focus")` | ✓ FLOWING |
| 填充按钮 hover 叠层 | `box-shadow` | `--color-overlay-hover` / `--color-overlay-active`(L282-283)→ `var()` 消费(L1584 / L1603) | 是 — 运行时读到 `inset 0 0 0 999px <令牌值>`,且按下时值换为 active 令牌 | ✓ FLOWING |
| 输入控件 hover 边框 | `border-color` | `--color-border-hover`(L231)→ `var()` 消费(L1645) | 是 — 运行时静默 `rgb(141,141,141)` → hover `rgb(100,100,100)`,且 == 令牌解析值 | ✓ FLOWING |
| 减弱动效 | `transition-duration` | `@media (prefers-reduced-motion: reduce)` 块(L1695-1697) | 是 — `emulate_media(reduced_motion="reduce")` 下四目标 `0s` | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| 第 10 项(焦点环端到端) | `.venv/bin/python scripts/check-05-ui-uat.py --item 10` | `item 10: PASS (41 条断言, 0 FAIL, 0 BLOCKED)`,exit 0 | ✓ PASS |
| 归档 0.75 合成环色 | `.venv/bin/python scripts/probe-07-focus-composite.py` | exit 0,`composited=(86,136,204) ratio=3.45 (>= 3.0)` | ✓ PASS |
| 跨阶段 UAT 无回归(ROADMAP Gates 的「Phase 4/6 全部 gate 仍通过」) | `.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8,9` | 9/9 PASS(smoke 9、1 45、2 5、3 17、4 65、6 6、7 38、8 13、9 16 条断言),**0 FAIL / 0 BLOCKED** | ✓ PASS |
| 令牌围栏一致性 | `bash scripts/check-01-token-conformance.sh` | `PASS` | ✓ PASS |
| 对比度配对清单 | `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`;`--color-focus` 三条 5.57 / 5.72 / 3.45;`--color-border-hover` 三条 5.77 / 5.62 / 5.82 | ✓ PASS |
| `.hidden` 唯一性 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` | ✓ PASS |
| `!important` 计数 | `bash scripts/check-04-important-count.sh` | `PASS`(`!important;` 声明数恒为 1) | ✓ PASS |
| **守卫非空转(IN-01 的修复)** | 在内存中删掉整条 `:focus-visible` 规则块,再调 `_idi07_focus_rule_blocks()` | 规则块数 **1 → 0**(守卫 1 会 FAIL、守卫 2 会 BLOCKED),而旧写法 `text.count(":focus-visible")` **9 → 2**(仍 >= 1,旧守卫会假绿) | ✓ PASS(独立证明修复有效且旧形态确实空转) |

### Probe Execution

| Probe | Command | Result | Status |
|-------|---------|--------|--------|
| `scripts/probe-07-focus-composite.py` | `.venv/bin/python scripts/probe-07-focus-composite.py` | exit 0;`PROBE archive-state opacity=0.75`、`links-before=0`、`links-after=1 (mutation-applied=yes)`、`ratio=3.45` | PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| `A11Y-01` | `idi-07-01-PLAN.md` | 全站 `:focus-visible` 样式,覆盖 21 按钮 / 8 输入框 / 4 下拉(基线 `:focus` / `outline` 规则均为 0) | ✓ SATISFIED | 7 选择器规则 + 三样本元素普查(判定集各 9 个,未覆盖 0)+ SC1 运行时读数 + `check-02` 三条 PAIR |
| `INTERACT-01` | `idi-07-02-PLAN.md` | `:hover` / `:active` / `:disabled` 覆盖交互控件(基线 2 / 0 / 8) | ✓ SATISFIED | 填充族叠层 + 朴素族递进 + D-07 的 gate(SC5′ 禁用按钮 hover 背景 == 静默)+ input/select hover 边框;9 条既有 `:disabled` 规则**一条未改** |
| `INTERACT-02` | `idi-07-03-PLAN.md` | transition 限定在 `background-color` / `border-color` / `opacity`,约 120–150ms;不建动效系统;**不得软化 `:disabled`** | ✓ SATISFIED | 运行时 120ms / 两属性;`reduce` 下 `0s`;`opacity` **刻意不在**属性列表(禁用态瞬变);`.event-list` 300ms 登记为具名例外 |

**Coverage:** 3/3 requirements satisfied。**无 ORPHANED**:`REQUIREMENTS.md` 把 Phase 7 映射到 `A11Y-01` / `INTERACT-01` / `INTERACT-02`(L39 / L58 / L59),三个 ID 分别被三份 PLAN 的 `requirements:` 字段认领,无一遗漏。

### Decision Coverage

`gsd_run query check.decision-coverage-verify` → `{skipped: false, blocking: false, total: 20, honored: 20, not_honored: []}`。
`07-CONTEXT.md` 的 D-01…D-20 全部在 shipped artifacts 中有对应面。**非阻塞门,仅登记。** 一处措辞级差异见 §C-2。

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `frontend/style.css` | — | `TBD` / `FIXME` / `XXX` / `TODO` / `HACK` / `PLACEHOLDER` | — | **0 处**(债务标记门不触发) |
| `scripts/check-05-ui-uat.py` | — | 同上 | — | **0 处** |
| `scripts/probe-07-focus-composite.py` | — | 同上 | — | **0 处** |
| `frontend/style.css` | 全文件 | `outline: none` / `outline: 0` 当焦点样式 | — | **0 处**(ROADMAP 的 Anti-Pattern 5 未复发) |
| `frontend/style.css` | 全文件 | `* { transition: all }` / 全局通配 transition | — | **0 处**;唯一的 `*` 规则是既有的 `* { box-sizing: border-box }`(L3,非本阶段) |
| `frontend/style.css` | 全文件 | `@layer` / `@property` / `var(--x, #fallback)` | — | **0 处** |
| `frontend/style.css` | 全文件 | `!important` 声明 | — | **恰 1 条**(`.hidden { display: none !important }`),`check-04` PASS;未采纳带两个 `!important` 的行业标准减弱动效片段 |
| `frontend/style.css` | L1508-1517 | 焦点规则设 `border` / `padding` | — | **0 条**;块内声明只有 `outline`(L1515)、`outline-offset`(L1516) |
| `frontend/style.css` | — | 针对 `#round-doc` 的焦点规则 | — | **0 条**(D-06 遵守:`#round-doc` 今天不可聚焦,该规则会是死代码) |

**Anti-patterns:** 0 found。

## Human Verification Required

**本阶段只有一条人工项**(D-17 的 5″)。**不得把它删掉换成机器代理量 —— 门绿不等于视觉上真的没被软化。**

### 1. 5″ —— 禁用态仍一眼看出不可点(`#btn-authorize`)

**Test:** 进入阶段 3(`p3` 样本)后,把鼠标移到 `#btn-authorize` 上并停留/按下,观察它是否仍「一眼看出不可点」——它是否被 hover 或按下「点亮」成可点的样子。

**Expected:** 禁用态一眼可辨,且悬停/按下时**零视觉反馈**(颜色不变亮、不变浅、不出现按压感);它作为 G3 前提条件唯一的视觉信号(0.55 的淡化)不被削弱。

**Why human:** 这是关于**感知**的主张,不是关于数值的主张。

**两个禁用态数值必须分开读,不得混成一个值:**

1. **机器半场**(`check-05` 第 10 项的 **SC5′**)覆盖的是 **`.verdict-buttons button:disabled`**
   (HEAD **L1376**,`_IDI07_DISABLED_OPACITY = "0.5"`,L1853),它断言 hover 时背景与静默**相同**(`rgb(249,249,249)`)且计算 `opacity` 仍为 **0.5**。
2. **人工项针对的 `#btn-authorize:disabled`**(HEAD **L1260**)是**另一条规则**、`opacity` 为 **0.55**;
   它的 hover 零反馈由同一处 gate(L741 的 `:where(:not(:disabled))` 与 L1574 的 `:not(:disabled)`)承担,但**今天没有任何机器断言读过它的 `opacity`** —— 它只被那条 gate **间接**保护。

人工半场要回答的问题正是:门绿不等于视觉上真的没被软化 —— 尤其 `#btn-authorize` 那条 0.55 的规则今天只被 gate 间接保护、未被任何探针读数。

## 独立复核发现的登记面(必须保留)

### A. D-19 指纹义务:四份历史报告判 stale,处置 = **重新验证**

本阶段改了 `frontend/style.css`(HEAD vs `69dea49`:`377 增 / 4 删`)与 `scripts/check-05-ui-uat.py`(`1414 增 / 14 删`)。四份仍在 `.planning/phases/` 下、`covered_files` 含其一或两者的报告,其 live 指纹因此失效。**我在 HEAD 上逐份重算**(`gsd-tools verification fingerprint <phase-dir> <files…> --raw`,covered files 是**位置参数**):

| 报告 | 记录值(前缀) | HEAD 重算值(前缀) | 结论 |
|------|---------------|--------------------|------|
| `idi-04` | `v1:sha256:4fd8b793…` | `v1:sha256:02a26269…` | **stale** |
| `idi-04.1-radix` | `v1:sha256:25d5f1fe…` | `v1:sha256:927ca77c…` | **stale** |
| `idi-05` | `v1:sha256:300abaa4…` | `v1:sha256:2de514a2…` | **stale** |
| `idi-06` | `v1:sha256:c07e9994…` | `v1:sha256:04d8cfa7…` | **stale** |

**完整重算值:**
```
idi-04          v1:sha256:02a262698e508d732d37d2fec92f610df25d70aaac03b33fe93d3ebaae7fbbd8
idi-04.1-radix  v1:sha256:927ca77c9f6837dd5ae10d2eebb87defef6129e9299276cd4c2d4c384cc1aa8a
idi-05          v1:sha256:2de514a2ab21a0a03c8e0872a55fbc71c48d37246f4ffb1150c863922a9a00bc
idi-06          v1:sha256:04d8cfa79f92cfd570e636435d50b7bb0793e3053ad547781f25340a277bab45
```

**成因(逐份核验,不采信 mtime):** `git log --since=<各报告 verified 时间戳> --oneline -- <covered file>` 逐文件枚举,四份的 covered 集合中都**确有** `frontend/style.css`(后三份另含 `scripts/check-05-ui-uat.py`)被本阶段改动。这是**内容真变**,不是记账性编辑 ⇒ **处置一律为「重新验证」(re-verify),不是「重算 + 披露」**。补救方向相反的两种处置不得混用。

**⚠ 不得用 `gsd-tools query verification status <phase>` 判定这四份**:相位目录命名与工具的相位令牌解析不匹配,该命令对它们一律返回 `missing`。判据只能是「逐份比对 `covered_files` 是否真的变了 + 在 HEAD 上重算 digest」。

**结构性观察(留给后续裁决,本报告不单方面改动):** `.planning/REQUIREMENTS.md` 同时在本报告与四份历史报告的 `covered_files` 内,而 `phase.complete` 每次收口都会改它 ⇒ **任何一次阶段收口都会打掉此前所有覆盖该文件的报告**。`covered_files` 的语义应是「其变更足以使本报告结论失效的输入」,而需求索引表属**下游记账**。建议后续把它移出 `covered_files`,或让 `phase.complete` 的翻转不参与指纹。本报告按 #4155 的要求仍将其列入(它被映射到本阶段)。

### B. SUMMARY 与 HEAD 的差异 —— **以树为准**

计划执行后落了四个评审修复提交,SUMMARY 早于它们。以下差异**不是缺陷**,是登记(凡冲突处以 HEAD 为准):

| SUMMARY 的说法 | HEAD 的事实 | 归因 |
|----------------|-------------|------|
| `idi-07-02-SUMMARY`:选择器在 **L627**;`idi-07-03-SUMMARY` 提到 **L587** | HEAD 在 **L741** | 行号漂移(本阶段在文件靠前处新增了注释/规则) |
| `idi-07-02-SUMMARY`:`item 10` 为 **26 条断言**;旧 VERIFICATION 为 **38 条** | **41 条断言** | 评审修复 WR-01 / WR-04 / IN-01 / IN-02 各增断言 |
| 旧 VERIFICATION:`:focus-visible` **计数 9**(含注释) | 守卫计的是**规则块数 = 1**(起始行 L1508) | IN-01 修复:改用 `_idi07_focus_rule_blocks()` 剔除注释提及(我已独立证明旧形态空转) |
| 旧 VERIFICATION:`FOCUSABLE_SELECTOR` 常量「逐字等于普查集」但未被消费 | 常量**已被消费**:两份普查脚本经 `_focusable_census_js` 的 `__FOCUSABLE_SELECTOR__` 占位符生成 | IN-02 修复 |
| 旧 VERIFICATION:`outline-offset` 无机械守卫 | SC1 **已增** `outline-offset == 2px` 断言(L2911-2916) | WR-04 修复 |
| 旧 VERIFICATION:SC4「滚到底」可能是 no-op | 探针**先撑高**容器再判定,不可滚则 `blocked` | WR-01 修复 |
| 旧 VERIFICATION:`style.css` 为 `354 增 / 4 删` | **`377 增 / 4 删`** | 评审修复新增约 23 行 |
| 旧 VERIFICATION 的行号 L1247 / L1363(`#btn-authorize:disabled` / `.verdict-buttons button:disabled`) | **L1260 / L1376** | 行号漂移 |
| `idi-07-02-SUMMARY`「本计划在 style.css 上的实际删除数为 6」 | 该计划**自身基线**上确为 `229 增 / 6 删`;但**阶段整体** vs 前阶段基线为 `377 增 / 4 删` | 两个口径都对,不是矛盾;报告阶段数字时应用**4** |

### C. 证据薄弱处(如实登记,均不构成阻塞)

1. **SC3 的冻结轮(0.55)半场无服务对象。** `opacity: 0.55` 已由 Phase 4 的 S-4(`4f323c0`)删除,`#round-doc.round-frozen` 今天只有 `filter: saturate(0.6)`。`filter` **不是 alpha 合成**,故 ROADMAP Gates 那句「每个环都对 0.55 与 0.75 合成背景验过」的 **0.55 支已随 S-4 作废**——它没有可验的对象,既不该判「已满足」也不该判「缺口」。补充算术(供参考,非门):即便把 `saturate(0.6)` 施加到环色,`#1f63bd` → ≈`rgb(55,96,150)`,对灰 `rgb(249,249,249)` 的对比度 ≈ **6.09:1**,仍远高于 3:1。故该半场无论如何都不构成风险。
2. **D-17 的 5′ 机器半场措辞与实现不一致。** `07-CONTEXT.md` D-17 的表格把「机器半场」写成断言 `#btn-authorize` 的 `opacity` 仍为 **0.55**;实现断言的是**另一条规则** `.verdict-buttons button:disabled` 的 **0.5**。SC 层面不构成缺口(SC5 的感知半场本就由 D-17 自己指派为具名人工项 5″),但**决策文本与实现有实质差异**,已由旧 VERIFICATION 与 `idi-07-03-SUMMARY` 的 `coverage.D5` 显式披露,本报告确认该披露准确。
3. **CSS 侧枚举与 harness 普查集的耦合不是机械强制,只是注释承诺。** harness 侧已单源(IN-02 修复);CSS 侧仍是字面量。**行为级守卫仍存在但对 4/7 个选择器无效**:运行时普查对样本中真实存在的元素类(button / input / select,均带 id)构成真守卫 —— 若 CSS 丢掉 `button`/`input`/`select`,判定集会出现未覆盖元素并 FAIL;但 `a[href]` / `summary` / `textarea` / `[tabindex]` 在三个样本中**零实例**(`a[href]`:探针实测 `#round-doc` 内为 0;`textarea` / `summary` / `[tabindex]`:全站静态计数为 0),故这四项若在 CSS 侧被误删,今天**没有任何门会变红**。这是本阶段最薄的一处机械保障,已在 `idi-07-03-SUMMARY` 与旧 VERIFICATION 中作为「靠注释承诺承担」登记。
4. **plan-02 的「填充按钮 hover 时前景文字对比度不低于静默时」无专门断言。** 该结论是**结构性**的:`--color-overlay-hover` 是 `rgba(0,0,0,0.06)`(均匀黑色蒙层),对任何非黑填充严格降低其相对亮度,而文字为白 ⇒ 对比度严格上升。CSS 注释引用的实测值(5.27 / 5.75 / 5.23)未被任何门复算(`check-02` 的 PAIR 清单不含叠层后的地面)。结论成立,但证据是推理 + 注释,不是探针。
5. **SC5 两条承重断言的「非空转」依赖 executor 自报的变异测试。** `idi-07-02-SUMMARY` 记载两次变异(去掉 `:where(:not(:active))` / 去掉 `:where(:not(:disabled))`)各使对应断言 FAIL。我**未**重跑这两次变异(会改动被覆盖文件,且评审已独立在运行时复测过相关读数);但我核对了两条断言的结构:它们各自断言了「③ != ②」与「禁用态 hover == 静默」这两条**在门失效时会变红**的对照量,且目标选择器与 gate 在 HEAD 上逐条存在。**结论:机制成立,变异证据沿用 executor 记录。**

### D. 阶段性质:ROADMAP「纯追加」的准确表述

ROADMAP Phase 7 的 Rationale 原文是「**纯追加** —— 不编辑任何既有规则」。**不得无条件复述。** 准确表述是:

> 本阶段是「**除一处选择器就地改写与三处注释就地改写外,纯追加**」。

- 唯一的非注释编辑:`frontend/style.css` 的 `button:hover` → `button:where(:not(:disabled)):hover:where(:not(:active))`(L741)。**声明体逐字节不变**;特异性**逐位不变**(均 0-1-1);匹配集收窄**两处** —— 禁用按钮(D-07 的缺陷修复)与按住不放中的按钮(D-09 的朴素按下态所必需)。
- 阶段整体 vs 前阶段基线 `69dea49`:`git diff --numstat 69dea49 HEAD -- frontend/style.css` = **`377 4`**。4 行删除逐条可归因(1 行选择器 + 3 行清单头部注释),**无一行是意外删除**。
- `07-CONTEXT.md` 的禁令面更窄(只禁「编辑既有规则的**声明**」),该改写不触犯它;但 ROADMAP 的阶段级措辞更宽,故上面这句限定是必须的。

## Gaps Summary

**无阻塞性缺口。** 阶段目标达成;全部自动化门与运行时探针在 HEAD 上全绿:

| # | 命令 | 结论 |
|---|------|------|
| 1 | `bash scripts/check-01-token-conformance.sh` | `PASS` |
| 2 | `.venv/bin/python scripts/check-02-contrast.py` | 末行 `PASS: 0 failures`;`--color-focus` 三条 5.57 / 5.72 / 3.45 |
| 3 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` |
| 4 | `bash scripts/check-04-important-count.sh` | `PASS`(`!important;` 声明数恒为 1) |
| 5 | `.venv/bin/python scripts/check-05-ui-uat.py --item 10` | `item 10: PASS (41 条断言, 0 FAIL, 0 BLOCKED)`,exit 0 |
| 6 | `.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8,9` | 9/9 PASS,0 FAIL / 0 BLOCKED(跨阶段无回归) |
| 7 | `.venv/bin/python scripts/probe-07-focus-composite.py` | exit 0,`ratio=3.45` |

**唯一的非机器项**是上面那条具名人工项(5″)。`status: human_needed` 反映的正是它 —— **不是自动化失败**。

**连带流程义务(不在本阶段可闭合范围内,但必须显式登记):** §A 的四份历史报告(idi-04 / idi-04.1-radix / idi-05 / idi-06)因本阶段的内容变更而指纹失效,处置为**重新验证**,各需 `/gsd-verify-work <phase>`。

## Verification Metadata

**Verification approach:** 目标回溯独立复核 —— 5 条 SC + 计划 must_haves 逐条在 HEAD 上找证据;自跑全部门与探针;独立重算四份历史指纹;独立做一次守卫非空转的内存变异
**Must-haves source:** `idi-07-01/02/03-PLAN.md` frontmatter 的 `must_haves` + `ROADMAP.md` § Phase 7 的 Success Criteria(合并去重,未削减)
**Automated checks:** 7 条命令全绿;`check-05` 共 10 项 PASS(item 5 需 `--ai-smoke`,本次未复跑)
**Human checks required:** 1(5″)
**Override:** 未适用任何 override(`overrides_applied: 0`);无 must-have 被判 FAIL
**Fingerprint:** 本报告的 `covered_files` / `covered_digest` 由 verifier 在**全部 PLAN / SUMMARY 落盘之后**计算

---

_Verified: 2026-09-23T09:18:28Z_
_Verifier: Claude (gsd-verifier) — 独立复核,取代 executor 的收口记录_

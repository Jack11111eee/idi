---
phase: idi-07-interaction-states-and-focus
status: passed
verified: 2026-09-25T09:11:00Z
score: 8/9 truths machine-verified + 1 named human item (5″)
covered_files:
  - .planning/phases/idi-07-interaction-states-and-focus/idi-07-01-PLAN.md
  - .planning/phases/idi-07-interaction-states-and-focus/idi-07-01-SUMMARY.md
  - .planning/phases/idi-07-interaction-states-and-focus/idi-07-02-PLAN.md
  - .planning/phases/idi-07-interaction-states-and-focus/idi-07-02-SUMMARY.md
  - .planning/phases/idi-07-interaction-states-and-focus/idi-07-03-PLAN.md
  - .planning/phases/idi-07-interaction-states-and-focus/idi-07-03-SUMMARY.md
  - frontend/style.css
  - scripts/check-05-ui-uat.py
  - scripts/probe-07-focus-composite.py

covered_digest: "v1:sha256:dad43802709c17ca6145312df6f7a3493c567cbc57af6dd0d3d9f4d8a5150df2"
behavior_unverified: 0
overrides_applied: 0
coincidental_reliance_items:

  - truth: "焦点环在归档态(0.75 合成)下仍可辨认(SC3 后半场)"
    reason: fixture-only
    harden: "**2026-09-25 复核:该条的状态已变,`fixture-only` 的「生产路径无等价物」半边被取代。** Phase 8 给 `#round-doc` 加了 `tabindex=\"0\"`,故归档地面上今天有**活体**服务对象,我已在 HEAD 上实测:archive 态 `#rounds-placeholder` 带 `archive-mode`、`#round-doc` 计算 `opacity=0.75` 且 `tabindex=0`/visible,Tab 第 2 跳即聚焦它,读到 `outlineWidth=2px` / `outlineColor=rgb(31, 99, 189)` / `outlineOffset=2px` / `focusVisible=True`。探针本身仍注入自己的 `<a href>`(`#round-doc` 内 `a[href]` 生产计数仍为 0),但它所测的**场景**(0.75 地面上出现焦点环)已可在生产路径直接观测。残留的口径缺口是**归档态无门采样** —— item 10 的普查只跑 p1 / checking / p3,不跑 archive。常驻算术半场(check-02 的 `--color-focus ON --color-surface NON-TEXT@0.75` = 3.45)不依赖任何 fixture。"
human_verification:

  - test: "在**阶段 3 且四处机械校验未全绿**的态下(`g3_available=false`,按钮 `disabled` 且 `#authorize-row` 可见),把鼠标移到 `#btn-authorize` 上并停留/按下,观察它是否仍「一眼看出不可点」——是否被 hover / 按下点亮成可点的样子(亦可直接在 devtools 里强制该元素 `disabled` 后观察)"
    expected: "禁用态一眼可辨,且悬停/按下时零视觉反馈(颜色不变亮、不变浅、无按压感);它作为 G3 前提条件唯一视觉信号的 0.55 淡化不被削弱"
    why_human: "这是关于**感知**的主张,不是关于数值的主张。机器半场(SC5′)覆盖的是另一条规则 `.verdict-buttons button:disabled`(opacity 0.5);`#btn-authorize:disabled`(opacity 0.55)今天没有任何机器断言读过它的 opacity,只被 `:not(:disabled)` 那条 gate 间接保护。**本轮实测:上一条 `test` 原先写的「进入阶段 3(p3 样本)」不成立 —— p3 样本里该按钮是 enabled(`disabled=false`、`opacity=1`),而它真正 disabled 的四个样本(p1/p12/checking/archive)里 `#authorize-row` 带 `.hidden`、`rects=0`,该按钮**在全部五个随附样本中都不可见**(见 §D-3)。故人工项的场景必须自建,不能照原样在 p3 上执行。**"
re_verification:
  previous_status: passed
  previous_score: "8/9 truths machine-verified + 1 named human item (5″)"
  previous_verified: 2026-09-23T09:18:28Z
  previous_covered_digest: "v1:sha256:5964d53cc475ca2539dd68d78e0e08ace21fd18866d21096c075bb655ee6dcc0"
  gaps_closed: []
  gaps_remaining: []
  regressions: []
---

# Phase 7: 交互状态与焦点样式 (idi-07) Verification Report

**Phase Goal:** 每个交互控件对 hover / active / disabled 有可辨反馈,并有可见的键盘焦点环;过渡限定在明确允许的属性上且尊重减弱动效偏好。
**Verified:** 2026-09-25T09:11:00Z · **HEAD:** `0b6283a`(branch `ui/baseline-and-tokens`)
**Status:** `passed`(canonical:UAT 已裁定后按仓库惯例 canonicalize —— 同型先例见 §重验证披露)。**本轮复核的验证代理判定仍为 `human_needed`**,唯一构成是那条具名人工项 5″(见 §Human Verification Required)。
**Re-verification:** **Yes — 内容真变后的重验证**(不是指纹刷新)。`covered_files` 里的两个文件在上一版验证之后真的变了字节(见 §重验证披露)。

## Goal Achievement

### Observable Truths

判定集 = 5 条 ROADMAP Success Criteria + 计划 frontmatter 中**不重复**的 must_haves truth。

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | **SC1** 键盘 Tab 到任一按钮 / 输入框 / 下拉,焦点环清晰可见 | ✓ VERIFIED | item 10 在 p1 / checking / p3 三样本上各读**当前 `document.activeElement`** 的计算值:`outline-width == 2px`、`outline-offset == 2px`、`outline-color == rgb(31, 99, 189)`(运行时解析的 `--color-focus`)、`focusVisible == True`。期望侧全部来自运行时令牌解析,无硬编码 rgb。`item 10: PASS (42 条断言, 0 FAIL, 0 BLOCKED)`,exit 0 |
| 2 | **SC2** 鼠标点击控件**不**出现焦点环(`:focus-visible` 语义成立) | ✓ VERIFIED | 先 Tab 让环出现(实测 `#ai-route-select` outlineColor=rgb(31,99,189) focusVisible=True,证明规则此刻是活的),再 `page.click("#btn-send")`,断言点击后 `outline-color` 为 `rgb(255, 255, 255)` != 环色。三步缺一即空转,均已落地 |
| 3 | **SC3** 焦点环在冻结轮次(0.55)与归档态(0.75)下仍可辨认 | ✓ VERIFIED | **归档半场**:`check-02` 的 `--color-focus ON --color-surface@0.75` = **3.45 ≥ 3**(WCAG 1.4.11);探针 `probe-07` 在真实渲染上实测 `composited=(86,136,204) ratio=3.45`,exit 0;本轮**新增活体实测**:archive 态 `#round-doc`(opacity 0.75)Tab 聚焦后环 `2px / rgb(31,99,189)` / focusVisible=True。**冻结半场**:`opacity: 0.55` 已由 Phase 4 的 S-4(`4f323c0`)删除,`#round-doc.round-frozen`(L1239-1240)今天只剩 `filter: saturate(0.6)` + 琥珀竖条 ⇒ **0.55 合成背景已不存在**,该半场无服务对象(见 §C-1 与 §D-3) |
| 4 | **SC4** 把侧栏滚到底部再 Tab,焦点环不被裁切 | ✓ VERIFIED | 探针**先走应用自己的渲染路径撑高**容器(`renderEvent` / `renderMarkdown`),回读三元组确认真可滚(`#main-pane` [1740, 2640, 900]、`#doc-panel` [4348, 5248, 900]);再 Tab 逐行测 clearance,判定行全部 >= `CLEARANCE_MIN_PX = 4.0`(实测 40 / 129.5 / 130 / 252)。撑高后仍无容器可滚则 `blocked(...)`,不记 PASS |
| 5 | **SC5a** 交互控件有 hover / active 反馈 | ✓ VERIFIED | 填充族:`#btn-send` hover 时 `background-color` **不变**且 `box-shadow` 出现 `inset 0 0 0 999px` 叠层;按住不放叠层换为 `--color-overlay-active` 且 != hover 读数。朴素族:`rgb(249,249,249) → rgb(240,240,240) → rgb(232,232,232)`,且断言 ③ != ②。输入控件:`#message-input` 与动态 `.verdict-note-input` 的 `border-color` `rgb(141,141,141) → rgb(100,100,100)`(且 != 静默值) |
| 6 | **SC5b** `#btn-authorize` 的禁用态**仍一眼看出不可点**(未被软化) | ⚠️ NEEDS HUMAN | 机器半场(SC5′)覆盖的是**另一条规则** `.verdict-buttons button:disabled`(L1384,`opacity: 0.5`);本条的 `#btn-authorize:disabled`(L1268,`opacity: 0.55`)**今天没有任何机器断言读过它的 `opacity`**。见「Human Verification Required」 |
| 7 | 焦点环**元素普查**:判定集(可见 ∧ 可聚焦)非空,且「未被环覆盖的元素数」为 0(D-16) | ✓ VERIFIED | 三样本各枚举 29 个实例;判定集分别 9 / 9 / 10 个元素,未覆盖 `[]`。判定集为空走 `blocked(...)` 而非 `info()+return` |
| 8 | 过渡只声明 `background-color` 与 `border-color`,时长 120ms;`reduce` 下全为 `0s`;`.event-list` 300ms 例外一个字节未改 | ✓ VERIFIED | 运行时实测 button / input / select 的 `transition-property == "background-color, border-color"`、`transition-duration == "0.12s, 0.12s"`;`.event-list` 为 `background-color` / `0.3s`;`page.emulate_media(reduced_motion="reduce")` 下四个目标**全为 `0s`**(判据先按 `,` 拆列表再逐项比)。`git diff 69dea49 HEAD -- frontend/style.css` 的 12 个 hunk **无一落在 `.event-list` 规则体**(L756-…);该规则体零行变动 |
| 9 | 阶段禁令面保持:焦点规则不设 `border` / `padding`;无 `outline: none`;无 `transition: all` / 通配;无 `@layer` / `@property` / `var(--x, #fallback)`;`!important` 声明数恒为 1;`@media` 计数与 `EXPECTED_MEDIA_QUERIES` 一致 | ✓ VERIFIED | 逐条机械核对(见「Anti-Patterns Found」与 §C-4):焦点规则块(L1519-1528)块内声明只有 `outline` / `outline-offset`;全文件无 `outline: none\|0`;唯一的 `*` 规则是既有的 `* { box-sizing: border-box }`(L3);唯一的 `!important;` 是 `.hidden { display: none !important; }`;`@media (prefers-reduced-motion` 计数 1 == 常量 `EXPECTED_MEDIA_QUERIES = 1` |

**Score:** 8/9 truths 机器验证通过;**第 6 条是具名人工项**(D-17 的 5″),不得换成机器代理量。`behavior_unverified: 0`(无「状态迁移 / 取消清理 / 顺序不变量」型 truth 未被测试覆盖)。

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `frontend/style.css` | 焦点环 / 交互态 / 过渡与减弱动效的追加规则 | ✓ EXISTS + SUBSTANTIVE + WIRED | `--color-focus: #1f63bd` 围栏内(L259)+ 7 选择器 `:focus-visible`(L1519-1528)+ `button:hover` 的 gate 与让位(L749)+ 朴素 `:active`(L1551)+ 填充 hover/active 叠层组(L1585-1596 / L1604-1615)+ input/select hover 组(L1648-1657)+ 过渡挂载(L1686)+ `@media (prefers-reduced-motion: reduce)`(L1706-1708)。**运行时消费已证**:环色被 `:focus-visible` 经 `var()` 消费,五个交互态令牌围栏内声明 == 1 且围栏外 `var()` 消费 == 1 |
| `scripts/check-05-ui-uat.py` | 第 10 项的元素普查 + SC1/SC2/SC4/SC5/SC5′ + **五条**静态契约守卫 + 过渡/减弱动效探针 | ✓ EXISTS + SUBSTANTIVE + WIRED | `item 10: PASS (42 条断言, 0 FAIL, 0 BLOCKED)`,exit 0。**第 ⑤ 条静态守卫(quick `260925-iin` FIX 5)是本轮新增覆盖点**:`FOCUSABLE_SELECTOR`(L1751)与 style.css `:focus-visible` 枚举逐项(含顺序)一致 —— 我另做内存变异证明它双向有效(见「Behavioral Spot-Checks」) |
| `scripts/probe-07-focus-composite.py` | 归档 0.75 合成的一次性反事实探针(**不进守卫契约**) | ✓ EXISTS + SUBSTANTIVE + WIRED | exit 0;自证非空转(`links-before=0` → 注入 → `links-after=1 (mutation-applied=yes)`);用运行时实测值复算 `check-02` 的 `composite()` 得 `ratio=3.45` |

**Artifacts:** 3/3 verified。`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` **零改动**(本阶段区间 `git diff --stat 69dea49 <phase-7 close>` 中不出现),与禁令一致。

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| `--color-focus`(L259) | `:focus-visible` 规则(L1526) | `outline: 2px solid var(--color-focus)` | ✓ WIRED | 围栏内声明 1 次、围栏外 `var()` 消费 1 次(静态守卫逐令牌断言);运行时 `outline-color` == 令牌解析值 |
| `:focus-visible` 枚举(L1519-1525) | harness 可聚焦普查集(`FOCUSABLE_SELECTOR`,L1751) | 逐项(含顺序)同集,**由 item 10 断言 ⑤ 机械比对** | ✓ WIRED | 守卫 ⑤ 的 INFO 行逐字:`CSS 侧(规则块起始行=1519)= ['button', 'input', 'select', 'textarea', 'a[href]', 'summary', '[tabindex]'];Python 侧(常量定义行=1751)= [同];对称差=[]`。**两侧今天真的被一条门绑在一起**(本里程碑审计 §7 登记的「无门比较」缺口已由 FIX 5 关闭) |
| 过渡挂载规则(L1686) | `@media (prefers-reduced-motion: reduce)`(L1706-1708) | 同一次提交落地 | ✓ WIRED | 静态守卫证明两者**同时存在**;运行时 `reduce` 下四个目标全 `0s`。「同提交」是 git 维度事实,门内 `info()` 已逐字声明该局限 —— 提交历史:`4892fdf` 一次提交同时落 media 块与 `EXPECTED_MEDIA_QUERIES` 同步 |
| 过渡挂载规则(L1686) | `.event-list` 既有 300ms 例外(L757) | 无(刻意零竞争,不同元素) | ✓ WIRED | 运行时实测 `.event-list` 仍为 `background-color` / `0.3s`;`git diff 69dea49 HEAD` 的 hunk 表无一触及该规则体 |
| `button:hover` 的 gate(L749) | `:where(button:not(:disabled)):active`(L1551) | 成对改写(让位 `:where(:not(:active))`) | ✓ WIRED | 运行时证明两半真的配套:朴素按钮 ③ 按住不放读数 != ② 悬停读数(`rgb(232,232,232)` != `rgb(240,240,240)`);若让位失效,③ 会读到 ② 的值,而「③ == surface-active」仍会成立 ⇒ 该「不相等」半条是判据本体 |
| `:focus-visible` 的 `[tabindex]` 臂(L1525) | Phase 8 的 `#round-doc tabindex="0"` | 零 CSS 改动自动套环 | ✓ WIRED | archive 态实测:`#round-doc` `tabindex=0` / visible / opacity 0.75,Tab 第 2 跳聚焦后 `outlineWidth=2px` / `outlineColor=rgb(31,99,189)` / `focusVisible=True` |

**Wiring:** 6/6 connections verified。

### Data-Flow Trace (Level 4)

本阶段是 CSS + 测试脚本,无数据渲染链路;唯一「值从声明流到消费者」的链路是令牌 → 渲染:

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `:focus-visible` 环色 | `outline-color` | `--color-focus` 围栏内声明(L259)→ `var()` 消费(L1526) | 是 — 运行时 `getComputedStyle` 读得 `rgb(31, 99, 189)` | ✓ FLOWING |
| 填充按钮 hover 叠层 | `box-shadow` | `--color-overlay-hover` / `--color-overlay-active`(L282-283)→ `var()` 消费(L1595 / L1614) | 是 — 运行时读到 `inset 0 0 0 999px <令牌值>`,且按下时值换为 active 令牌 | ✓ FLOWING |
| 输入控件 hover 边框 | `border-color` | `--color-border-hover`(L231)→ `var()` 消费(L1656) | 是 — 运行时静默 `rgb(141,141,141)` → hover `rgb(100,100,100)` | ✓ FLOWING |
| 减弱动效 | `transition-duration` | `@media (prefers-reduced-motion: reduce)` 块(L1706-1708) | 是 — `emulate_media(reduced_motion="reduce")` 下四目标 `0s` | ✓ FLOWING |

### Behavioral Spot-Checks

全部命令在 HEAD `0b6283a` 上由本轮复核**独立重跑**,逐字输出如下。

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| 第 10 项(焦点环端到端,含 FIX 5 静态守卫) | `.venv/bin/python scripts/check-05-ui-uat.py --item 10 --browser bundled` | `item 10: PASS  (42 条断言,0 FAIL,0 BLOCKED)`;`exit=0` | ✓ PASS |
| 第 9 项(L-5/L-6 与 4px 环外伸量的交叉面) | `.venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled` | `item 9: PASS  (17 条断言,0 FAIL,0 BLOCKED)`;`exit=0` | ✓ PASS |
| 跨阶段无回归 | `.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8 --browser bundled` | `smoke 9 / 1 45 / 2 5 / 3 17 / 4 65 / 6 6 / 7 38 / 8 13` 条断言,**0 FAIL / 0 BLOCKED**,exit 0 | ✓ PASS |
| Phase 8 验证面(焦点交接与 Escape 行为,与本阶段焦点面相邻) | `.venv/bin/python scripts/check-07-idi08-validation.py` | `item g1: PASS (21) / g2: PASS (39) / g3: PASS (10) / g4: PASS (3)`,0 FAIL / 0 BLOCKED,exit 0 | ✓ PASS |
| 归档 0.75 合成环色 | `.venv/bin/python scripts/probe-07-focus-composite.py` | exit 0;`PROBE composite ring=(31, 99, 189) ground=rgb(249, 249, 249) alpha=0.75 composited=(86, 136, 204) ratio=3.45 (>= 3.0)` | ✓ PASS |
| 令牌围栏一致性 | `bash scripts/check-01-token-conformance.sh` | `PASS`,exit 0 | ✓ PASS |
| 对比度配对清单 | `.venv/bin/python scripts/check-02-contrast.py` | 末行 `PASS: 0 failures`;`53` 条 PASS 配对 + `1` 条 ORDER 0.363;`--color-focus` 三条 **5.57 / 5.72 / 3.45** | ✓ PASS |
| `.hidden` 唯一性 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS`,exit 0 | ✓ PASS |
| `!important` 计数 | `bash scripts/check-04-important-count.sh` | `PASS`,exit 0 | ✓ PASS |
| 后端基线 | `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped, 1 warning in 6.32s` | ✓ PASS |
| 前端语法 | `node --check frontend/app.js` | `app.js OK` | ✓ PASS |
| **守卫 ⑤ 非空转(本轮独立内存变异)** | 内存替换 style.css 文本 / `FOCUSABLE_SELECTOR`,再调 `_idi07_focus_contract_guards()` | 见下表:基线 PASS,**四种变异全部 FAIL** | ✓ PASS |

**FIX 5 守卫双向性(独立变异证明,逐字):**

```
case                                           | FIX5     | non-PASS rows in call
----------------------------------------------------------------------------------------------------
BASELINE (HEAD, unmutated)                     | PASS     | []  (total rows=9)
A: CSS enum reduced (drop summary)             | FAIL     | [('FAIL', '[static] FOCUSABLE_SELECTOR 与 :focus-visible 枚举逐项(')]  (total rows=9)
B: PY const narrowed (drop summary)            | FAIL     | [('FAIL', '[static] FOCUSABLE_SELECTOR 与 :focus-visible 枚举逐项(')]  (total rows=9)
C: CSS enum reordered (swap button/input)      | FAIL     | [('FAIL', '[static] FOCUSABLE_SELECTOR 与 :focus-visible 枚举逐项(')]  (total rows=9)
D: CSS enum widened (add video)                | FAIL     | [('FAIL', '[static] FOCUSABLE_SELECTOR 与 :focus-visible 枚举逐项(')]  (total rows=9)
```

变异 A 的失败行逐字:`expected=['button', 'input', 'select', 'textarea', 'a[href]', '[tabindex]'] actual=['button', 'input', 'select', 'textarea', 'a[href]', 'summary', '[tabindex]']` ⇒ **项目数不等走的是 `ok_true` 的 FAIL 分支,不是 `blocked()`**。

**`blocked()` 前置条件逐条核对(只读代码):** 守卫 ⑤ 只有两处 `blocked()` —— ① `if len(blocks) != 1:`(**规则块数**,不是枚举项数;0 块无比对对象,>1 块选择器列表有歧义)与 ② `if not selector_text.strip():`(选择器部分为空)。**没有任何「项数」前置条件**:项数不等直接落进 `css_base == py_items` 的有序比较并判 FAIL。这正是本阶段计划明令的形态(项数前置条件会让 CSS 收窄型变异落到 BLOCKED,而 BLOCKED 不是可判定的红)。

### Probe Execution

| Probe | Command | Result | Status |
|-------|---------|--------|--------|
| `scripts/probe-07-focus-composite.py` | `.venv/bin/python scripts/probe-07-focus-composite.py` | exit 0;`PROBE archive-state opacity=0.75`、`links-before=0`、`links-after=1 (mutation-applied=yes)`、`ratio=3.45` | PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| `A11Y-01` | `idi-07-01-PLAN.md` | 全站 `:focus-visible` 样式,覆盖 21 按钮 / 8 输入框 / 4 下拉(基线 `:focus` / `outline` 规则均为 0) | ✓ SATISFIED | 7 选择器规则 + 三样本元素普查(判定集 9/9/10,未覆盖 0)+ SC1 运行时读数 + `check-02` 三条 PAIR + **新增守卫 ⑤(枚举 ↔ 常量逐项一致)** |
| `INTERACT-01` | `idi-07-02-PLAN.md` | `:hover` / `:active` / `:disabled` 覆盖交互控件(基线 2 / 0 / 8) | ✓ SATISFIED | 填充族叠层 + 朴素族递进 + D-07 的 gate(SC5′ 禁用按钮 hover 背景 == 静默)+ input/select hover 边框;9 条既有 `:disabled` 规则**一条未改** |
| `INTERACT-02` | `idi-07-03-PLAN.md` | transition 限定在 `background-color` / `border-color` / `opacity`,约 120–150ms;不建动效系统;**不得软化 `:disabled`** | ✓ SATISFIED | 运行时 120ms / 两属性;`reduce` 下 `0s`;`opacity` **刻意不在**属性列表(禁用态瞬变);`.event-list` 300ms 登记为具名例外 |

**Coverage:** 3/3 requirements satisfied。**无 ORPHANED**:三份 PLAN 的 `requirements:` 字段分别认领 `A11Y-01` / `INTERACT-01` / `INTERACT-02`,无一遗漏。

### Decision Coverage

`gsd_run query check.decision-coverage-verify <phase-dir> <phase-dir>/07-CONTEXT.md` → `{skipped: false, blocking: false, total: 20, honored: 20, not_honored: []}`,message:`All trackable CONTEXT.md decisions are honored by shipped artifacts.`
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
| `frontend/style.css` | L1519-1528 | 焦点规则设 `border` / `padding` | — | **0 条**;块内声明只有 `outline`(L1526)、`outline-offset`(L1527) |
| `frontend/style.css` | — | 针对 `#round-doc` 的焦点规则 | — | **0 条**(D-06 遵守:本阶段不为 `#round-doc` 写焦点规则;Phase 8 加 `tabindex` 后由 `[tabindex]` 臂自动覆盖) |

**Anti-patterns:** 0 found。

## Human Verification Required

**本阶段只有一条人工项**(D-17 的 5″)。**不得把它删掉换成机器代理量 —— 门绿不等于视觉上真的没被软化。**

### 1. 5″ —— 禁用态仍一眼看出不可点(`#btn-authorize`)

**Test:** 在**阶段 3 且四处机械校验未全绿**的态下(`g3_available=false`,按钮 `disabled` 且 `#authorize-row` 可见),把鼠标移到 `#btn-authorize` 上并停留/按下,观察它是否仍「一眼看出不可点」——它是否被 hover 或按下「点亮」成可点的样子。(亦可直接在 devtools 里强制该元素 `disabled` 后观察。)

**Expected:** 禁用态一眼可辨,且悬停/按下时**零视觉反馈**(颜色不变亮、不变浅、不出现按压感);它作为 G3 前提条件唯一的视觉信号(0.55 的淡化)不被削弱。

**Why human:** 这是关于**感知**的主张,不是关于数值的主张。

**两个禁用态数值必须分开读,不得混成一个值:**

1. **机器半场**(`check-05` 第 10 项的 **SC5′**)覆盖的是 **`.verdict-buttons button:disabled`**
   (HEAD **L1384**,`_IDI07_DISABLED_OPACITY = "0.5"`),它断言 hover 时背景与静默**相同**(`rgb(249,249,249)`)且计算 `opacity` 仍为 **0.5**。
2. **人工项针对的 `#btn-authorize:disabled`**(HEAD **L1268**)是**另一条规则**、`opacity` 为 **0.55**;
   它的 hover 零反馈由同一处 gate(L749 的 `:where(:not(:disabled))` 与 L1585 的 `:not(:disabled)`)承担,但**今天没有任何机器断言读过它的 `opacity`** —— 它只被那条 gate **间接**保护。

**本轮可测半场(已实测,见 §D-3):** 声明 `opacity: 0.55`(L1268)在位;在它 disabled 的样本(p1/checking/archive)里计算 `opacity` 读得 `0.55`,且 hover/按下时 `background-color` 与 `opacity` **都不变**;全部 `#btn-authorize` 的 hover/active 规则逐条带 `:not(:disabled)`(无一条裸 `:hover`/`:active` 能匹配禁用态)。

**本轮新发现(必须随人工项一起读):** 原 `Test` 写的「进入阶段 3(p3 样本)」**不成立** —— p3 样本里该按钮 `disabled=false`、`opacity=1`;而它 disabled 的四个样本里 `#authorize-row` 带 `.hidden`、`rects=0`,该按钮**在全部五个随附样本中都不可见**。故人工项的场景必须自建(阶段 3 + 四查未全绿,或 devtools 强制 `disabled`),不能照原样在 p3 上执行。**这不改变该条的结论**(它仍是人工项),但使 `idi-07-UAT.md` 那条 `pass`(按 p3 措辞记录)**不足以充当本条的感知证据**。

## 独立复核发现的登记面(必须保留)

### A. D-19 指纹义务:四份历史报告的处置 —— **已完成(2026-09-25)**

上一版本报告判 `idi-04` / `idi-04.1-radix` / `idi-05` / `idi-06` 四份报告**内容真变 ⇒ stale**,处置为「**重新验证**」。**该处方已全部执行完毕**,四份均在 2026-09-25 重跑复核,并按用户 2026-09-25 的裁定**各自删除了 `.planning/REQUIREMENTS.md`** 后重算指纹:

| 报告 | 上一版记录的旧值(前缀) | 本阶段当时的重算值(前缀) | 2026-09-25 复验后的现状(前缀) | 结论 |
|------|--------------------------|----------------------------|-------------------------------|------|
| `idi-04` | `v1:sha256:4fd8b793…` | `v1:sha256:02a26269…` | `v1:sha256:3d583e6d…` | ✅ 已重新验证(2026-09-25T08:01:44Z) |
| `idi-04.1-radix` | `v1:sha256:25d5f1fe…` | `v1:sha256:927ca77c…` | `v1:sha256:27957cea…` | ✅ 已重新验证(2026-09-25T08:18:03Z) |
| `idi-05` | `v1:sha256:300abaa4…` | `v1:sha256:2de514a2…` | `v1:sha256:bee9dea6…` | ✅ 已重新验证(2026-09-25T08:36:09Z) |
| `idi-06` | `v1:sha256:c07e9994…` | `v1:sha256:04d8cfa7…` | `v1:sha256:ccc470b1…` | ✅ 已重新验证(2026-09-25T08:52:23Z) |

**关于上一版记录的重算值的时效性:** 上一版写下的 `idi-04 → v1:sha256:02a262698e508d73…` 等四个值,是在**当时的 `covered_files`(含 `REQUIREMENTS.md`)** 上算出的,因此**已被取代** —— 复验时四份都移除了 `REQUIREMENTS.md`,重算值即上表末列。上一版的那四个值只应作为历史记录读,不得再当作 live 指纹。

**成因(逐份核验,不采信 mtime):** 四份的 covered 集合中都**确有** `frontend/style.css`(后三份另含 `scripts/check-05-ui-uat.py`)被本阶段改动。这是**内容真变**,不是记账性编辑 ⇒ 处置一律为「重新验证」,不是「重算 + 披露」。

**⚠ 不得用 `gsd-tools query verification status <phase>` 判定这四份**:相位目录命名与工具的相位令牌解析不匹配,该命令对它们一律返回 `missing`。判据只能是「逐份比对 `covered_files` 是否真的变了 + 在 HEAD 上重算 digest」。

**结构性观察 —— 已由用户裁定并落地:** 上一版提出的「`.planning/REQUIREMENTS.md` 同时在本报告与四份历史报告的 `covered_files` 内,而每次 `phase.complete` 都改它 ⇒ 任何一次阶段收口都会打掉此前所有覆盖该文件的报告」这一观察,**用户已于 2026-09-25 裁定采纳**,适用于全部六份 v1.14 阶段报告:该文件从六份的 `covered_files` 中删除。本报告随之删除该行并按**剩余文件集**重算 `covered_digest`(见 §重验证披露)。

### B. SUMMARY 与 HEAD 的差异 —— **以树为准**

计划执行后落了四个评审修复提交,SUMMARY 早于它们。以下差异**不是缺陷**,是登记(凡冲突处以 HEAD 为准):

| SUMMARY 的说法 | HEAD 的事实 | 归因 |
|----------------|-------------|------|
| `idi-07-02-SUMMARY`:选择器在 **L627**;`idi-07-03-SUMMARY` 提到 **L587** | HEAD 在 **L749** | 行号漂移(本阶段在文件靠前处新增了注释/规则) |
| `idi-07-02-SUMMARY`:`item 10` 为 **26 条断言**;旧 VERIFICATION 为 **38 条** | **42 条断言**(41 → 42:quick `260925-iin` FIX 5 新增守卫 ⑤) | 评审修复 WR-01 / WR-04 / IN-01 / IN-02 + FIX 5 各增断言 |
| 旧 VERIFICATION:`:focus-visible` **计数 9**(含注释) | 守卫计的是**规则块数 = 1**(起始行 L1519) | IN-01 修复:改用 `_idi07_focus_rule_blocks()` 剔除注释提及 |
| 旧 VERIFICATION:`FOCUSABLE_SELECTOR` 常量「逐字等于普查集」但未被消费 | 常量**已被消费**(两份普查脚本经 `_focusable_census_js` 的 `__FOCUSABLE_SELECTOR__` 占位符生成),且**已被守卫 ⑤ 与 CSS 侧绑定** | IN-02 修复 + FIX 5 |
| 旧 VERIFICATION:`outline-offset` 无机械守卫 | SC1 **已增** `outline-offset == 2px` 断言 | WR-04 修复 |
| 旧 VERIFICATION:SC4「滚到底」可能是 no-op | 探针**先撑高**容器再判定,不可滚则 `blocked` | WR-01 修复 |
| 旧 VERIFICATION:`style.css` 为 `354 增 / 4 删` | 本阶段收口时为 **`377 增 / 4 删`**;今天(含 quick `260925-iin` 的 17 增 / 6 删)为 **`394 增 / 10 删`** | 评审修复 + FIX 3 |
| 旧 VERIFICATION 的行号 L1247 / L1363(`#btn-authorize:disabled` / `.verdict-buttons button:disabled`) | **L1268 / L1384** | 行号漂移 |
| 旧 VERIFICATION 的行号 L1508-1517(焦点规则块) | **L1519-1528** | 行号漂移 |

### C. 证据薄弱处(如实登记,均不构成阻塞)

1. **SC3 的冻结轮(0.55)半场无服务对象。** `opacity: 0.55` 已由 Phase 4 的 S-4(`4f323c0`)删除,`#round-doc.round-frozen` 今天只有 `filter: saturate(0.6)`。`filter` **不是 alpha 合成**,故 ROADMAP Gates 那句「每个环都对 0.55 与 0.75 合成背景验过」的 **0.55 支已随 S-4 作废** —— 它没有可验的对象,既不该判「已满足」也不该判「缺口」。补充算术(供参考,非门):即便把 `saturate(0.6)` 施加到环色,`#1f63bd` → ≈`rgb(55,96,150)`,对灰 `rgb(249,249,249)` 的对比度 ≈ **6.09:1**,仍远高于 3:1。
2. **D-17 的 5′ 机器半场措辞与实现不一致。** `07-CONTEXT.md` D-17 的表格把「机器半场」写成断言 `#btn-authorize` 的 `opacity` 仍为 **0.55**;实现断言的是**另一条规则** `.verdict-buttons button:disabled` 的 **0.5**。SC 层面不构成缺口(SC5 的感知半场本就由 D-17 自己指派为具名人工项 5″),但**决策文本与实现有实质差异**,已由旧 VERIFICATION 与 `idi-07-03-SUMMARY` 的 `coverage.D5` 显式披露,本报告确认该披露准确。
3. **CSS 侧枚举与 harness 普查集的耦合 —— 已由 FIX 5 机械强制(本条的旧形态已失效)。** 上一版登记的是「harness 侧已单源;CSS 侧仍是字面量,只能靠注释承诺」,并指出「`a[href]` / `summary` / `textarea` / `[tabindex]` 若在 CSS 侧被误删,今天没有任何门会变红」。**quick `260925-iin` FIX 5 已把这条耦合落成 item 10 的静态守卫 ⑤**,逐项(含顺序)比较两侧。本轮我另做内存变异独立证明它双向有效(基线 PASS;CSS 收窄 / 常量收窄 / CSS 换序 / CSS 加项 四种变异**全部 FAIL**,见「Behavioral Spot-Checks」)。**故本条不再是薄弱处**;残留的只是「静态守卫读文件文本、不读渲染结果」这一与其余四条守卫同型的性质(运行时普查仍对样本中真实存在的元素类构成行为级守卫)。
4. **plan-02 的「填充按钮 hover 时前景文字对比度不低于静默时」无专门断言。** 该结论是**结构性**的:`--color-overlay-hover` 是 `rgba(0,0,0,0.06)`(均匀黑色蒙层),对任何非黑填充严格降低其相对亮度,而文字为白 ⇒ 对比度严格上升。CSS 注释引用的实测值(5.27 / 5.75 / 5.23)未被任何门复算。结论成立,但证据是推理 + 注释,不是探针。
5. **SC5 两条承重断言的「非空转」依赖 executor 自报的变异测试。** `idi-07-02-SUMMARY` 记载两次变异(去掉 `:where(:not(:active))` / 去掉 `:where(:not(:disabled))`)各使对应断言 FAIL。我**未**重跑这两次变异(会改动被覆盖文件);但我核对了两条断言的结构:它们各自断言了「③ != ②」与「禁用态 hover == 静默」这两条**在门失效时会变红**的对照量,且目标选择器与 gate 在 HEAD 上逐条存在。**结论:机制成立,变异证据沿用 executor 记录。**

### D. 阶段性质与人工项的可执行性

**D-1. ROADMAP「纯追加」的准确表述。** ROADMAP Phase 7 的 Rationale 原文是「**纯追加** —— 不编辑任何既有规则」。**不得无条件复述。** 准确表述是:

> 本阶段是「**除一处选择器就地改写与三处注释就地改写外,纯追加**」。

- 唯一的非注释编辑:`frontend/style.css` 的 `button:hover` → `button:where(:not(:disabled)):hover:where(:not(:active))`(L749)。**声明体逐字节不变**;特异性**逐位不变**(均 0-1-1);匹配集收窄**两处** —— 禁用按钮(D-07 的缺陷修复)与按住不放中的按钮(D-09 的朴素按下态所必需)。
- 阶段整体 vs 前阶段基线 `69dea49`:`git diff --numstat 69dea49 HEAD -- frontend/style.css` = **`394 10`**(其中 quick `260925-iin` 贡献 `17 6`,即本阶段自己的收口口径为 `377 4`)。删除行逐条可归因(1 行选择器 + 注释头部),**无一行是意外删除**。
- `07-CONTEXT.md` 的禁令面更窄(只禁「编辑既有规则的**声明**」),该改写不触犯它;但 ROADMAP 的阶段级措辞更宽,故上面这句限定是必须的。

**D-2. 本阶段的交互态工作未被 quick `260925-iin` 触及。** `git diff bc563d7 HEAD -- frontend/style.css` 只有 4 个 hunk,全部落在**排版刻度**上(字号围栏注释 + `--text-lg-plus: 20px`、行高围栏注释 + `--lh-none: 1`、`.collapse-indicator` 改为消费这两个令牌、嵌入档注释各一段)。`:focus-visible` 规则块、hover/active/disabled 规则、过渡挂载规则与 `prefers-reduced-motion` 块**一个字节未改** —— 已由 item 10 的 42 条断言与守卫 ⑤ 在 HEAD 上复核。

**D-3. 人工项 5″ 的可执行性(本轮新发现)。** 本轮用真实浏览器逐个样本实测 `#btn-authorize`:

```
[p3]       disabled=False rects=1 rect=178x40 inHidden=False   opacity rest/hover/press = 1 / 1 / 1
[checking] disabled=True  rects=0 rect=0x0   inHidden=True     opacity rest/hover/press = 0.55 / 0.55 / 0.55
[archive]  disabled=True  rects=0 rect=0x0   inHidden=True     opacity rest/hover/press = 0.55 / 0.55 / 0.55
[p1]       disabled=True  rects=0 rect=0x0   inHidden=True     opacity rest/hover/press = 0.55 / 0.55 / 0.55
```

即:**p3 里按钮是 enabled 的**(`applyPhase3Extras` 在 `g3_available=true` 时 `authorizeBtn.disabled = false`),而它 disabled 的四个样本里 `#authorize-row` 带 `.hidden`(rects=0)。**该按钮的禁用态在全部五个随附样本中都不可见。** 故 `idi-07-UAT.md` 按 p3 措辞记录的那条 `pass`,并未在 p3 上真正看到禁用态。这不改变本条是人工项的结论(机器半场 `opacity: 0.55` 与 gate 覆盖在 HEAD 上均成立,已实测),但**人工项的场景必须自建**;见「Human Verification Required」中已改写的 `Test`。

### E. 与 Phase 8 的交接面(本轮新增)

Phase 8 给 `#round-doc` 加了 `tabindex="0"`,使本阶段 `[tabindex]:focus-visible` 臂(L1525)从「防御性非冗余」变为**活体**。archive 态实测:`#round-doc` `tabindex=0` / visible / 计算 `opacity=0.75`,Tab 第 2 跳聚焦后 `outlineWidth=2px` / `outlineColor=rgb(31, 99, 189)` / `outlineOffset=2px` / `focusVisible=True`。这正是 `style.css:1509-1514` 注释承诺的「Phase 8 加 tabindex 后本臂自动套环,无需再动本文件」。**残留口径缺口**:item 10 的普查只跑 p1 / checking / p3,**不跑 archive**,故归档地面上的活体环没有门采样(仅有常驻算术门 + 一次性探针)。

## 重验证披露(内容真变,非记账性刷新)

**为什么重验证而不是重算指纹。** 本报告上一版 `verified: 2026-09-23T09:18:28Z`,记录的 `covered_digest` 为 `v1:sha256:5964d53c…`。其 `covered_files` 里的两个文件在该时间戳之后**真的变了字节**:

- `frontend/style.css` —— quick `260925-iin` FIX 3 在 `:root` 围栏内新增两条声明(`--text-lg-plus: 20px`、`--lh-none: 1`),改写 `.collapse-indicator`(L686)去消费它们,并更新三处围栏注释(`17 增 / 6 删`,vs `bc563d7`)。**本阶段自己的交互态工作未被触及**(见 §D-2)。
- `scripts/check-05-ui-uat.py` —— quick `260925-iin` 的三处改动:FIX 2 给 item 9 加了一条 auto-follow 断言(16→17),FIX 4 修正一条陈旧散文,**FIX 5 给 `_idi07_focus_contract_guards()` 新增第 ⑤ 条静态守卫(item 10 的 41→42)**。**FIX 5 直接落在本阶段 A11Y-01 的验证面上**,故本轮必须正面覆盖它(已覆盖,见「Behavioral Spot-Checks」与 §C-3)。

因此本轮是**重跑复核**(全部门与探针在 HEAD 上重跑、逐条重判),不是「重算 digest + 披露」。

**`covered_files` 的变更(用户 2026-09-25 裁定)。** 删除了 `.planning/REQUIREMENTS.md`。理由是上一版 §A 已提出的结构性观察:该文件同时出现在本报告与四份历史报告的 `covered_files` 里,而每次 `phase.complete` 都会改它 —— 于是**任何一次阶段收口都会同时打掉此前所有覆盖该文件的报告**。`covered_files` 的语义应是「其变更足以使本报告结论失效的输入」,需求索引表属**下游记账**(且里程碑收口会 `git rm` 掉它),不满足该语义。用户已采纳该建议并适用于全部六份 v1.14 阶段报告(本报告之外的五份另行处理,本报告**未改动任何其他报告**)。`covered_digest` 随之按**剩余文件集**用位置参数形式重算为 `v1:sha256:dad43802…0df2`。

**状态字段的两半,以及它们的来历。** 上一版本报告 frontmatter 的 `status: passed` 与正文 `**Status:** human_needed` 不一致,这不是笔误 —— 2026-09-23 的 `f0f0c31`(「canonicalize verification status to passed after UAT」)**只改 frontmatter、正文保留 `human_needed`**;`idi-07-UAT.md` 已对唯一人工项裁定 `pass`。本轮据仓库既有惯例(同型先例见 `idi-04.1-VERIFICATION.md` §重验证披露)把两半写清而非留一个无解释的矛盾:**frontmatter `status: passed` 是 canonical 状态(UAT 已裁定);正文明确标出「本轮复核的验证代理判定仍为 `human_needed`」**,其唯一构成是那条具名人工项 5″。读者不应再把两半读成互相矛盾。

**本轮未改动任何其他产物。** 未改 `REQUIREMENTS.md`、`ROADMAP.md`、`idi-07-UI-SPEC.md`(该文件**从未存在**,见下)、`idi-07-VALIDATION.md`、`idi-07-UAT.md`、`idi-07-UI-REVIEW.md`、`frontend/`、`scripts/`,也未触碰其他五份阶段报告与 backlog `999.2`;唯一的写入是本文件。

> **附注(任务清单与仓库现实的差异,如实登记):** 本次任务的必读清单点名 `idi-07-UI-SPEC.md`,但该文件**在 git 历史中从未存在**(`git log --all -- '*idi-07-UI-SPEC*'` 为空;相位目录内只有 `idi-07-UI-REVIEW.md`)。本阶段的设计契约载体是 `07-CONTEXT.md` 的 D-01…D-20(decision-coverage 门即针对它),不是 UI-SPEC。这不构成本阶段的缺口。

## Gaps Summary

**无阻塞性缺口。** 阶段目标达成;全部自动化门与运行时探针在 HEAD `0b6283a` 上全绿:

| # | 命令 | 结论 |
|---|------|------|
| 1 | `bash scripts/check-01-token-conformance.sh` | `PASS` |
| 2 | `.venv/bin/python scripts/check-02-contrast.py` | 末行 `PASS: 0 failures`;53 条配对 + ORDER 0.363;`--color-focus` 三条 5.57 / 5.72 / 3.45 |
| 3 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` |
| 4 | `bash scripts/check-04-important-count.sh` | `PASS`(`!important;` 声明数恒为 1) |
| 5 | `.venv/bin/python scripts/check-05-ui-uat.py --item 10 --browser bundled` | `item 10: PASS (42 条断言, 0 FAIL, 0 BLOCKED)`,exit 0 |
| 6 | `.venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled` | `item 9: PASS (17 条断言, 0 FAIL, 0 BLOCKED)`,exit 0 |
| 7 | `.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8 --browser bundled` | 8/8 PASS,0 FAIL / 0 BLOCKED(跨阶段无回归) |
| 8 | `.venv/bin/python scripts/probe-07-focus-composite.py` | exit 0,`ratio=3.45` |
| 9 | `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped` |
| 10 | `node --check frontend/app.js` | `app.js OK` |
| 11 | `.venv/bin/python scripts/check-07-idi08-validation.py` | g1/g2/g3/g4 全 PASS,0 FAIL / 0 BLOCKED |
| 12 | 内存变异(守卫 ⑤ 双向性) | 基线 PASS;四种变异全 FAIL |

**唯一的非机器项**是上面那条具名人工项(5″)。`status` 的两半(§重验证披露)反映的正是它 —— **不是自动化失败**。

**连带流程义务:** §A 的四份历史报告(idi-04 / idi-04.1-radix / idi-05 / idi-06)的指纹义务**已全部执行完毕**(均于 2026-09-25 重新验证)。本报告不再留有未闭合的连带义务。

## Verification Metadata

**Verification approach:** 目标回溯独立复核 —— 5 条 SC + 计划 must_haves 逐条在 HEAD 上找证据;自跑全部门与探针(含跨阶段切片与 Phase 8 的 check-07);**独立做一次守卫 ⑤ 的内存变异(四种变异)**;独立做一次人工项可执行性的浏览器实测;逐份核对四份历史报告的复验状态
**Must-haves source:** `idi-07-01/02/03-PLAN.md` frontmatter 的 `must_haves` + `ROADMAP.md` § Phase 7 的 Success Criteria(合并去重,未削减)
**Automated checks:** 12 条命令/变异全绿;`check-05` 共 10 项 PASS(item 5 需 `--ai-smoke`,本次未复跑;其 BLOCKED 系 opt-in 设计,非本阶段缺口)
**Human checks required:** 1(5″;其场景措辞已按 §D-3 修正)
**Override:** 未适用任何 override(`overrides_applied: 0`);无 must-have 被判 FAIL
**Fingerprint:** `covered_files` / `covered_digest` 由 verifier 在**全部 PLAN / SUMMARY 落盘之后**、按**用户裁定的剩余文件集**计算

---

_Verified: 2026-09-25T09:11:00Z · HEAD `0b6283a`_
_Verifier: Claude (gsd-verifier) — 内容真变后的重验证,取代 2026-09-23 版_
_covered_files 变更: 2026-09-25 —— 移除 `.planning/REQUIREMENTS.md`,指纹按剩余文件集重算(用户裁定)_

---
phase: idi-07-interaction-states-and-focus
verified: 2026-09-23T07:18:33Z
status: human_needed
score: 6/7 success criteria machine-verified + 1 named human item (5″)
behavior_unverified: 0
---

# Phase 7: 交互状态与焦点样式 Verification Report

**Phase Goal:** 每个交互控件对 hover / active / disabled 有可辨反馈,并有可见的键盘焦点环;过渡限定在明确允许的属性上且尊重减弱动效偏好。
**Verified:** 2026-09-23T07:18:33Z
**Status:** human_needed

> **本文件的定位(必须读)。** 这是 `idi-07-03-PLAN.md` Task 3 要求的**阶段收口记录** ——
> 它把本阶段的收口证据与全部登记项固定下来。**它不声称独立验证**:独立复核与指纹写回仍欠
> `/gsd-verify-work idi-07`。故本文件**刻意不声明 `covered_files` / `covered_digest`**
> (#4155 的指纹对是 fail-closed 的:声明其一而缺另一会直接判 `stale`)—— 指纹必须由 verifier
> 在**全部 PLAN / SUMMARY 都在盘之后**计算,否则 `allCurrentArtifactsCovered` 会因本计划自己的
> `idi-07-03-SUMMARY.md` 尚未落地而立刻判 stale。这不是漏写,是有意的负空间。

## 阶段性质(复述时必须带限定 —— 不得无条件写「纯追加」)

ROADMAP Phase 7 的 Rationale 原文是「**纯追加** —— 不编辑任何既有规则」。本阶段实际有**且仅有**一处就地编辑:

- `frontend/style.css` 的 `button:hover` 选择器被就地改写为
  `button:where(:not(:disabled)):hover:where(:not(:active))`(计划 02 落地;规划期记作 **L587**,HEAD 上在 **L728**)。
  声明体逐字节不变,特异性改写前后**逐位相同**(均 0-1-1);**匹配集收窄两处** —— 禁用按钮
  (D-07 的缺陷修复)与按住不放中的按钮(D-09 的朴素按下态需要 hover 让位)。

另有三处**注释**的就地改写(计划 02 的 Task 1 与 Task 3 明令):「Three values that must NOT be
'helpfully' changed back」第 3 条的同步扩写,以及 PAIR 清单头部计数注释的两行。

⇒ **本阶段的准确性质是「除 L587 的选择器改写与那三行注释改写外纯追加」。**
`git diff --numstat 69dea49 HEAD -- frontend/style.css` = `354 4`(354 增 / 4 删),4 行删除逐条可归因到
上面这四处,**无一行是意外删除**。`idi-07-03` 自身的 diff 是 **51 增 / 0 删**(零删除)。
`07-CONTEXT.md` 的禁令面更窄(只禁「编辑既有规则的**声明**」),该改写不触犯它;
但 ROADMAP 的阶段级措辞更宽,**不得无条件复述**。

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | 键盘 Tab 到任一按钮 / 输入框 / 下拉,焦点环清晰可见 | ✓ VERIFIED | `check-05 --item 10` 的 SC1 在 p1 / checking / p3 三样本上读到 `outline-width == 2px` 且 `outline-color == rgb(31, 99, 189)`(运行时解析的 `--color-focus`) |
| 2 | 鼠标点击控件**不**出现焦点环(`:focus-visible` 语义成立) | ✓ VERIFIED | SC2:点击 `#btn-send` 后 `document.activeElement` 就是它,`outline-color` 为 `rgb(255, 255, 255)` != 环色 |
| 3 | 焦点环在冻结轮次(0.55)与归档态(0.75)下仍可辨认 | ✓ VERIFIED | 冻结轮半场由 **S-4 结构性满足**(0.55 的 `opacity` 已删,环回到 5.57);归档半场由 `check-02` 的 `--color-focus ON --color-surface NON-TEXT@0.75` = **3.45 ≥ 3** + 一次性探针 `probe-07-focus-composite.py`(exit 0,`composited=(86,136,204) ratio=3.45`)共同承担 |
| 4 | 把侧栏滚到底部再 Tab,焦点环不被裁切 | ✓ VERIFIED | SC4:滚到底后每个新 Tab 聚焦元素的 clearance 全部 >= `CLEARANCE_MIN_PX = 4.0`(几何 `2px + outline-offset: 2px` 双向绑定) |
| 5 | 交互控件有 hover / active 反馈 | ✓ VERIFIED | SC5(`#btn-send` 的 inset 叠层)/ SC5-朴素按下(`rgb(249,249,249) → rgb(240,240,240) → rgb(232,232,232)`,且断言 ③ != ②)/ 输入控件 hover 边界(`rgb(141,141,141) → rgb(100,100,100)`) |
| 6 | 过渡限定在允许的属性上、时长在规格内、尊重减弱动效偏好 | ✓ VERIFIED | `check-05 --item 10` 的运行时探针:button / input / select 的 `transition-property` = `background-color, border-color`、`transition-duration` = `0.12s`;`.event-list` = `background-color` / `0.3s`;`reduced_motion='reduce'` 下四者全为 `0s` |
| 7 | `#btn-authorize` 的禁用态**仍一眼看出不可点**(未被软化) | ⚠️ NEEDS HUMAN | 机器半场(SC5′)覆盖的是**另一条规则** `.verdict-buttons button:disabled`(HEAD L1363,`opacity: 0.5`);见下方「Human Verification Required」 |

**Score:** 6/7 machine-verified;第 7 条是**具名人工项**,不得换成机器代理量(D-17)。

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `frontend/style.css` | 焦点环 / 交互态 / 过渡与减弱动效的追加规则 | ✓ EXISTS + SUBSTANTIVE | `--color-focus: #1f63bd` 围栏内声明 + 七选择器 `:focus-visible`(L1492-1501)+ 五处交互态追加规则 + 过渡挂载规则 + `@media (prefers-reduced-motion: reduce)` 块;围栏外裸 `#hex` 计数 0 |
| `scripts/check-05-ui-uat.py` | 第 10 项的元素普查 + SC1/SC2/SC4/SC5/SC5-朴素按下/SC5′ + 静态契约守卫 + 过渡/减弱动效探针 | ✓ EXISTS + SUBSTANTIVE | `item 10: PASS (38 条断言,0 FAIL,0 BLOCKED)`;`EXPECTED_MEDIA_QUERIES == 1`;`_idi07_focus_contract_guards` 被 `item10` 调用一次 |
| `scripts/probe-07-focus-composite.py` | 归档 0.75 合成的一次性反事实探针(**不进守卫契约**) | ✓ EXISTS + SUBSTANTIVE | exit 0;注入 0 → 1 自证非空转;用运行时实测值复算 `check-02` 的 `composite()` 得 3.45 |

**Artifacts:** 3/3 verified

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| `--color-focus` | `:focus-visible` 规则 | `outline: 2px solid var(--color-focus)` | ✓ WIRED | 令牌在围栏内声明 **1** 次、围栏外被 `var()` 消费 **1** 次(静态守卫逐令牌断言,五个令牌全绿) |
| `@media (prefers-reduced-motion: reduce)` 块 | `check-05` 的 `EXPECTED_MEDIA_QUERIES` | 静态计数守卫(`_l2_guard_shape`) | ✓ WIRED | 常量 `0 → 1` 与 media 块**同一次提交**;`--item 8` PASS(13 条断言) |
| 过渡挂载规则 | `.event-list` 的既有 300ms 例外 | 无(刻意零竞争,不同元素) | ✓ WIRED | 运行时实测 `.event-list` 仍为 `background-color` / `0.3s`,**一个字节未改** |
| `:focus-visible` 枚举 | `check-05` 的可聚焦普查集 | 逐字同集(`button, input, select, textarea, a[href], summary, [tabindex]`) | ✓ WIRED | 两侧注释互相点名「新增一类可聚焦元素要**同时**改两处」 |

**Wiring:** 4/4 connections verified

## Requirements Coverage

| Requirement | Status | Blocking Issue |
|-------------|--------|----------------|
| A11Y-01:全站作者化焦点环 | ✓ SATISFIED | - |
| INTERACT-01:hover / active / disabled 可辨反馈 | ✓ SATISFIED | - |
| INTERACT-02:过渡限定在允许属性 + 尊重减弱动效 | ✓ SATISFIED | - |

**Coverage:** 3/3 requirements satisfied

## Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| — | — | 无 | — | 本阶段未引入任何 stub / TODO / FIXME / 硬编码空值;`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` / `scripts/ui-states/` **零改动** |

**Anti-patterns:** 0 found

### ROADMAP Gates 里那行 0.55 / 0.75 门的作废半场(必须登记,否则收口会静默跳过一行 gate 文本)

ROADMAP Phase 7 的 Gates 原文含「**每个环都对 0.55 与 0.75 合成背景验过**」。

- **0.75 半场有门**:三条 `--color-focus` PAIR(计划 01),其中 `@0.75` 那条由 `check-02` 的 alpha 合成
  承担(实测 **3.45 ≥ 3**);归档半场的**运行时**空缺已由 D-18 显式登记(五个样本的 `#round-doc` 内
  `a[href]` 计数为 0)并由一次性探针 `probe-07-focus-composite.py` 补上可复跑证据。
- **0.55 半场整行作废**:那个 `opacity: 0.55` 已由 **S-4 删除**(`07-CONTEXT.md` D-02 第 1 条),
  `#round-doc.round-frozen`(HEAD L1226-1229)今天只剩 `filter: saturate(0.6)` +
  琥珀 `box-shadow: inset 3px 0 0 var(--color-action-warning)`。
  **`filter: saturate()` 不是 alpha 合成** —— 它不做「环色与地面按比例混合」这件事 ⇒ Pitfall 5 的
  「被祖先 `opacity` 相乘」那一支**已不存在**,没有任何 0.55 合成背景可供验色。
- **结论与动作:不新增 PAIR、不改任何代码、也**不得**把这行 gate 当成「已满足」。**
  该 gate 的 0.55 支**无服务对象,已随 S-4 作废**;存活的 `filter` 不构成合成背景。

## Human Verification Required

**本阶段只有一条人工项**(D-17 的 5″)。**不得把它删掉换成机器代理量 —— 门绿不等于视觉上真的没被软化。**

### 1. 5″ —— 禁用态仍一眼看出不可点(`#btn-authorize`)

**Test:** 进入阶段 3(`p3` 样本)后,把鼠标移到 `#btn-authorize` 上并在它上面停留/按下,观察它是否仍然「一眼看出不可点」——它是否被 hover 或按下「点亮」成可点的样子。
**Expected:** 禁用态一眼可辨、且悬停/按下时**零视觉反馈**(颜色不变亮、不变浅、不出现按压感);它作为 G3 前提条件唯一的视觉信号(0.55 的淡化)不被削弱。

**Why human:** 这是关于**感知**的主张,不是关于数值的主张。

**两个禁用态数值必须分开读,不得混成一个值:**

1. **机器半场**(`check-05` 第 10 项的 **SC5′**)覆盖的是 **`.verdict-buttons button:disabled`**
   (HEAD **L1363**,**朴素**按钮),它断言 hover 时背景与静默**相同**(`rgb(249,249,249)`)且计算
   `opacity` 仍为 **0.5**。
2. **人工项针对的 `#btn-authorize:disabled`**(HEAD **L1247**)是**另一条规则**、`opacity` 为 **0.55**;
   它的 hover 零反馈由同一处 gate(HEAD **L728** 的选择器)承担,但**今天没有任何机器断言读过它的
   `opacity`** —— 它只被那条 gate **间接**保护。

**人工半场要回答的问题正是:门绿不等于视觉上真的没被软化** —— 尤其 `#btn-authorize` 那条 0.55 的规则
今天只被 gate 间接保护、未被任何探针读数。

## Registrations(本计划 Task 3 的登记面 —— 缺一条即收口不完整)

1. **D-11 的修正案:UI-SPEC 那一处登记面不存在。** D-11 要求 300ms 例外同时写进 CONTEXT、
   **UI-SPEC 的字面量/例外清单**、以及新过渡的围栏注释。本阶段**没有 UI-SPEC 且不得创建**
   (`idi-07-03-PLAN.md:71` 明文「不得为了凑齐三处而新建 UI-SPEC 文件」)。故登记面收窄为两处:
   **CONTEXT.md(已由 `07-CONTEXT.md` D-11 满足)+ 新过渡规则的围栏注释(计划 03 Task 1 已落)**。
   **不得据此认为例外未登记。**
2. **`#round-doc` 的焦点环承载面指派给 Phase 8(D-06)。** 本阶段唯一跨阶段的开放项。Phase 7 的枚举含
   `[tabindex]`(今天全站计数为 0,是防御性非冗余写法);Phase 8 给 `#round-doc` 加 `tabindex="0"` 时,
   那条规则会**自动**把环套到一个数千像素高的盒子上 —— 只有上下边缘可见,且落在 `.archive-mode` 的
   0.75 合成里。**Phase 8 必须写内嵌处理**(`outline-offset: -2px` 或把环落在 `#doc-pane`)。
3. **`EXPECTED_MEDIA_QUERIES` 的耦合(B1)。** 该常量已随 media 块同步为 **1**;若日后有人删除该 media
   块,必须**同时把常量改回 0**,否则 `check-05 --item 8` 会误报。
4. **本阶段唯一的非追加编辑已在上面「阶段性质」一节登记(L587 的选择器改写)。**
5. **ROADMAP Gates 的 0.55 合成支已随 S-4 作废** —— 见上方专门小节。

## Gaps Summary

**无阻塞性缺口。** 阶段目标达成;全部自动化门与运行时探针在 HEAD 上全绿:

| # | 命令 | 结论 |
|---|------|------|
| 1 | `bash scripts/check-01-token-conformance.sh` | `PASS` |
| 2 | `.venv/bin/python scripts/check-02-contrast.py` | 末行 `PASS: 0 failures`;`^PASS` 行数 **53**;FAIL 0 |
| 3 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` |
| 4 | `bash scripts/check-04-important-count.sh` | `PASS`(`!important;` 声明数恒为 1) |
| 5 | `.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,5,6,7,8,9,10` | **0 FAIL**;item 5 的 2 条 BLOCKED 是需真实 AI 调用的冒烟,已由 `--item 5 --ai-smoke` 补齐 ⇒ `item 5: PASS (9 条断言,0 FAIL,0 BLOCKED)`,exit 0。其余十项全 PASS |
| 6 | `.venv/bin/python scripts/probe-07-focus-composite.py` | exit 0,`ratio=3.45` |

**唯一的非机器项**是上面那条具名人工项(5″)。`status: human_needed` 反映的正是它 —— 不是自动化失败。

## Verification Metadata

**Verification approach:** 收口记录(executor-authored close-out)+ 逐门复跑
**Must-haves source:** `idi-07-01/02/03-PLAN.md` frontmatter 的 `must_haves`
**Automated checks:** 6 条命令全绿;`check-05` 逐项 11/11 PASS(item 5 需 `--ai-smoke`)
**Human checks required:** 1(5″)
**Independent verification:** 欠 `/gsd-verify-work idi-07`(含 `covered_files` / `covered_digest` 的写回)

---
*Verified: 2026-09-23T07:18:33Z*
*Author: idi-07-03 executor (close-out record — not an independent verification)*

---
phase: 260925-iin-v1-14-ai-999-1
verified: 2026-09-25T06:52:38Z
status: passed
score: 8/8 must-haves verified
covered_files:
  - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md
  - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md
  - .planning/quick/260925-iin-v1-14-ai-999-1/260925-iin-PLAN.md
  - .planning/quick/260925-iin-v1-14-ai-999-1/260925-iin-SUMMARY.md
  - frontend/app.js
  - frontend/style.css
  - scripts/check-05-ui-uat.py
covered_digest: "v1:sha256:4bde66b20e07a84bdbd75092b0a06de1b4a7b7ae09a624e7997b87eba08d3eee"
behavior_unverified: 0
overrides_applied: 0
---

# Phase 260925-iin: v1.14 收口前修复(五修一票)Verification Report

**Phase Goal:** v1.14 收口前修复(五修一票):恢复 AI 事件自动跟随(Phase 6 的 L-4 改动引入的零门覆盖回归)+ 补一条真能失败的门 + 处置 backlog 999.1 的两项 + 新增 `FOCUSABLE_SELECTOR` ↔ `:focus-visible` 枚举对齐门。
**Verified:** 2026-09-25T06:52:38Z
**Status:** passed
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | 自动跟随恢复:经应用自身的 `renderEvent` 追加事件后,`#main-pane.scrollTop > 0`,末条 `.event-item` rect 完全落在 `#main-pane` 可见盒内,harness 全程未设 `scrollTop` | ✓ VERIFIED | `frontend/app.js:253` = `item.scrollIntoView({ block: 'nearest' })`;旧 no-op 串 `eventsEl.scrollTop = eventsEl.scrollHeight` 在 app.js 内计数 1 → **0**。`check-05 --item 9` 实跑:`before=0 after=1721 ... last=[848,900] pane=[0,900]` PASS |
| 2 | 新增的门**能失败**:中和 FIX 1 后 `--item 9` 新断言 FAIL 且 exit 1;还原后 PASS | ✓ VERIFIED | 变异证明由编排器第一手复现(中和 `item.scrollIntoView` → `item 9: FAIL (17 条断言, 1 FAIL, 0 BLOCKED)`,exit 1,`after=0 last=[2569,2621] pane=[0,900]`)。本轮**未重跑该变异**(见 §Mutation-Proof Note);我独立核了使其成立的机制:断言置于 `item9()` 内**第一个** `_idi06_reach()` 之前(新块 L2733-2800 vs 首个 `_idi06_reach` L2811),而 `_IDI06_REACH_JS` 自身在 L2486 设 `c.scrollTop = scrollHeight` |
| 3 | `FOCUSABLE_SELECTOR` ↔ `:focus-visible` 枚举由**一条静态门**守住;两侧逐项(含顺序)不等即 FAIL;任一方向收窄都 FAIL | ✓ VERIFIED | `scripts/check-05-ui-uat.py:3724-3778` 断言 5:`ok_true(item, ..., css_base == py_items, py_items, css_base, ...)` —— **有序列表相等**。双向变异由编排器第一手复现(A 常量侧、B CSS 侧,expected/actual 恰好互换,均 FAIL、exit 1)。我独立在无浏览器进程内调用该守卫:9 行 item-10 记录,断言 5 PASS,两侧均 7 项 |
| 4 | `.collapse-indicator` computed `font-size` 仍为 `20px`(字形渲染尺寸不变),且围栏外不再有裸字号/行高字面量:规则消费 `--text-lg-plus` 与 `--lh-none` | ✓ VERIFIED | 我**自己重跑**浏览器探针 `/tmp/idi-iin-260925/probe-font.py`:两个实例(`#ai-panel` / `#doc-panel`)均 `font-size=20px line-height=20px`,exit 0。`grep -c 'font-size: 20px' style.css` = **0**(基线 1);`grep -c 'line-height: 1;'` = **0**(基线 1);规则体 = `font-size: var(--text-lg-plus); line-height: var(--lh-none);` |
| 5 | `:root` 围栏内多两条声明(`--text-lg-plus: 20px` / `--lh-none: 1`),各恰一个消费者且同提交;围栏注释记录「第 8 档、值序在 18 与 22 之间、命名阶梯非单调依据 D-07」 | ✓ VERIFIED | `style.css:326` `--text-lg-plus: 20px;` 紧接 `--text-lg: 18px;`;`style.css:350` `--lh-none: 1;` 紧接 `--lh-reading: 1.625;`。各令牌全文件出现 2 次 = 1 次声明 + 1 次 `var()` 消费(唯一消费者 `.collapse-indicator`,L686)。注释:`8 sizes`=1(基线 0)、`7 sizes`=0、`Line height — 五条`=1、`18 / 20 / 22`=1。声明与消费者同在提交 `3e50dca` |
| 6 | 硬规则 1/2 仍成立:`.hidden` == 1;`!important` **声明**数 == 1 | ✓ VERIFIED | `grep -c '^\.hidden {' frontend/style.css` = **1**;`grep -o '!important;' frontend/style.css \| wc -l` = **1**(`grep -c '!important'` = 5 为注释散文陷阱,未用作判据) |
| 7 | check-05 的 blockquote 诊断串陈述真实值(`#646464` / 5.62:1 达标),`item2()` 断言零改动 | ✓ VERIFIED | `git show 7c991d8` 仅改 2+/1− 一条散文串,无断言改动。实跑 `--item 2` PASS(5 条断言);INFO 打印 `ratio=5.62 (color=rgb(100, 100, 100) ...)`。`grep -c '8f8f8f'` = 0(基线 1);`check-02` 独立报 `PASS 5.62 --color-text-muted on --color-surface` |
| 8 | 全套门在改动后仍为绿 | ✓ VERIFIED | 我本轮逐条实跑:check-01 PASS / check-02 `PASS: 0 failures` / check-03 PASS / check-04 PASS / `--item 9` PASS(17)/ `--item 10` PASS(42)/ `--item 2` PASS(5)/ `--item 7` PASS(38)/ `pytest -q` **219 passed, 6 skipped** / `node --check frontend/app.js` OK |

**Score:** 8/8 truths verified (0 present-but-behavior-unverified)

### Required Artifacts

| Artifact | Expected | Status | Details |
| --- | --- | --- | --- |
| `frontend/app.js` | `renderEvent()` 内 `item.scrollIntoView({block:'nearest'})`,旧 no-op 已删 | ✓ VERIFIED | L252-253;旧串计数 0;`node --check` OK;`scrollIntoView` 计数 1 |
| `scripts/check-05-ui-uat.py` | `item9()` 新增自动跟随断言(置于注入块之前) | ✓ VERIFIED | L2733-2800,先于 L2811 的首个 `_idi06_reach`;item 9 断言 16 → 17 |
| `frontend/style.css` | 两条新令牌 + `.collapse-indicator` 消费二者 | ✓ VERIFIED | L326 / L350 / L686;`--text-*` 声明 8(基线 7)、`--lh-*` 声明 5(基线 4) |
| `.planning/phases/idi-05-.../idi-05-UI-SPEC.md` | 刻度表 7 → 8 档 + 999.1 第 1 项关闭 + hard rule 9 引用登记 | ✓ VERIFIED | L166 / L174 表已 8 档;L368、L680-684 登记关闭;L1063-1065 第 9 条引用登记 |
| `.planning/phases/idi-04-.../04-UI-SPEC.md` | 仅一条如实指向行;6 档表与 L-1…L-5 清单不变 | ✓ VERIFIED | `git show 3e50dca` 仅 +6 行 blockquote 指向行,正文表零改动 |
| `scripts/check-05-ui-uat.py:824` | 陈旧诊断串订正为真值 | ✓ VERIFIED | 见 Truth 7 |
| `_idi07_focus_contract_guards()` 第 ⑤ 条 + docstring | 静态枚举比对 + 「四条 → 五条」同步 | ✓ VERIFIED | 模块 docstring L85、函数 docstring L3622 均已改;item 10 断言 41 → 42 |

### Key Link Verification

| From | To | Via | Status | Details |
| --- | --- | --- | --- | --- |
| `renderEvent()` `eventsEl.appendChild(item)` | 外层滚动者 `#main-pane` 跟随 | `item.scrollIntoView({block:'nearest'})` | ✓ WIRED | 浏览器实跑:after=1721,末条 rect 落入 pane 可见盒 |
| check-05 `item9()` 新断言 | 应用自身的 `renderEvent`(SSE handler L196 同一函数) | `page.evaluate` 内调 `renderEvent` 40 次,探针 JS 零 `scrollTop` 赋值 | ✓ WIRED | 断言 `after>0 ∧ 末条 rect ⊆ 可见盒`;变异即 FAIL |
| `.collapse-indicator` `font-size` | `--text-lg-plus`(20px) | `var(--text-lg-plus)` | ✓ WIRED | computed `font-size=20px`(浏览器实读) |
| `FOCUSABLE_SELECTOR`(L1751) | `_focusable_census_js()` → `_IDI07_FOCUS_CENSUS_JS` | 常量字符串 → `querySelectorAll(...)` 参数 | ✓ WIRED | 新静态门 L3724-3778 守住该常量与 CSS 枚举(L1519-1525)的一致性 |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| --- | --- | --- | --- | --- |
| `frontend/app.js` `renderEvent()` | `eventsEl` / 追加的 `item` | 真实 DOM 追加 + `scrollIntoView` | Yes — 浏览器实读 `scrollTop` 0 → 1721 | ✓ FLOWING |
| `frontend/style.css` `.collapse-indicator` | computed `font-size` | `--text-lg-plus` 令牌(`:root` 围栏内) | Yes — 20px(两实例) | ✓ FLOWING |
| `_idi07_focus_contract_guards` 断言 5 | `css_base` / `py_items` | `frontend/style.css` 文本 + `FOCUSABLE_SELECTOR` 常量 | Yes — 两侧各 7 项,对称差 `[]` | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| --- | --- | --- | --- |
| AI 事件自动跟随(应用自身路径) | `.venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled` | `item 9: PASS (17 条断言,0 FAIL,0 BLOCKED)`,exit 0;`before=0 after=1721 last=[848,900] pane=[0,900]` | ✓ PASS |
| `.collapse-indicator` 字形渲染 20px | `.venv/bin/python /tmp/idi-iin-260925/probe-font.py` | 2 实例 `font-size=20px line-height=20px`,exit 0 | ✓ PASS |
| 静态枚举对齐门(零浏览器) | 进程内 `_idi07_focus_contract_guards("item10")` | 9 行 item-10 记录,断言 5 `PASS`,两侧 7 项,对称差 `[]` | ✓ PASS |
| `--color-text-muted` 诊断串真值 | `.venv/bin/python scripts/check-05-ui-uat.py --item 2 --browser bundled` | `item 2: PASS (5 条断言)`;INFO `ratio=5.62`、`#646464` | ✓ PASS |
| 围栏外裸字号字面量清零 | `grep -c 'font-size: 20px' frontend/style.css` | 0(基线 1) | ✓ PASS |

### Probe Execution

| Probe | Command | Result | Status |
| --- | --- | --- | --- |
| 仓库内常规探针 `scripts/*/tests/probe-*.sh` | `find scripts -path '*/tests/probe-*.sh'` | 无命中(本任务不含此类探针) | N/A |
| FIX 3 computed-style 探针(临时,未提交) | `.venv/bin/python /tmp/idi-iin-260925/probe-font.py` | exit 0;两实例 20px/20px | PASS |

**Mutation-Proof Note.** FIX 2 与 FIX 5 的单/双向变异由编排器**第一手复现**过,本轮**未重跑**;按任务口径这不算缺口。我独立核验的是使变异有意义的三处机制:(a) FIX 2 断言的文本落点先于首个 `_idi06_reach`(L2733-2800 vs L2811),而后者自身在 L2486 设 `c.scrollTop = scrollHeight`;(b) 断言判据 `after>0 ∧ 末条 rect ⊆ 可见盒`,在无 `scrollIntoView` 时 `after=0` 且末条在 pane 之外(与编排器逐字读数一致);(c) FIX 5 的 `blocked()` 前提只有「恰 1 个含 `:focus-visible` 的规则块」与「选择器部分非空」两条**结构性**条件,项数**不**进前提 —— 故 CSS 侧收窄会流入逐项比较记 FAIL,而非 BLOCKED。

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
| --- | --- | --- | --- | --- |
| LAYOUT-04 | 01 | 侧栏滚动容器套娃收敛 | ✓ SATISFIED | `.event-list` 仍未恢复 `max-height`/`overflow-y`(L-4 未回退);`--item 9` 滚动者集合普查仍 PASS |
| TOKEN-08 | 01 | 字号刻度令牌化,消除裸字面量 | ✓ SATISFIED | 第 8 档 `--text-lg-plus` 落地;`font-size: 20px` 裸字面量 1 → 0 |
| CHECK-01 | 01 | `:root` 围栏外裸 hex = 0 | ✓ SATISFIED | `check-01` PASS |
| CHECK-02 | 01 | 全部令牌配对达 AA | ✓ SATISFIED | `check-02` `PASS: 0 failures`(53 PASS + 1 ORDER) |
| CHECK-03 | 01 | `^\.hidden {` == 1 | ✓ SATISFIED | `check-03` PASS;`grep -c` = 1 |
| CHECK-04 | 01 | `!important` 声明数 == 1 | ✓ SATISFIED | `check-04` PASS;`grep -o '!important;' \| wc -l` = 1 |
| A11Y-01 | 01 | 全站 `:focus-visible` 覆盖 | ✓ SATISFIED | 新静态门守住常量 ↔ CSS 枚举;`--item 10` PASS(42),焦点环未覆盖数 0 |

无 ORPHANED 需求(`grep -E "Phase 260925-iin" REQUIREMENTS.md` 无映射;本任务为 quick,不新增需求映射)。

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| --- | --- | --- | --- | --- |
| `.planning/phases/idi-05-.../idi-05-UI-SPEC.md` | 1088 | 「不在本阶段」范围锁表中仍以 `.collapse-indicator` 的 `font-size: 20px` / `line-height: 1` 为条目名 | ℹ️ Info | 该行**未**出现在 SUMMARY §B 的「刻意保留」枚举(只列了 :555-556 / :913 / :1329-1330)。行本身不断言字面量在 HEAD 仍存在,且整表标题 `## 不在本阶段(范围锁 —— Pitfall 8)` 把它限定为 Phase 5 决定 ⇒ 作为历史可辩护。**非阻断**,交里程碑收口自行决定是否收窄措辞 |
| `.planning/phases/idi-05-.../idi-05-UI-SPEC.md` | 110-111 | 「明确不含:… `.collapse-indicator` 的越轨字面量(backlog `999.1`)」 | ℹ️ Info | 同上,Phase 5 范围声明;`越轨字面量` 一词在 HEAD 已不再描述存在物。非阻断 |

**无债务标记**(`TBD` / `FIXME` / `XXX`)出现在本任务改动的 5 个文件内(逐文件 grep 为 0)。**无新增** `!important` / `@layer` / `@property` / `var(--x, fallback)`;`@layer`=0、`@property`=0、`var(--x, `=0、`display: var(`=0。**硬规则 3(追加不重排)机械复核:** 提取 `bc563d7` 与 HEAD 的顶层规则块头各 **173** 个,difflib 比对**无非 equal opcode** ⇒ 零块移动、零增删。

### Human Verification Required

None. 两条行为依赖的性质(自动跟随、字形渲染尺寸)都由浏览器断言/探针在本轮实跑覆盖,无需人工测试。

### Gaps Summary

无缺口。审计 §5 的**唯一阻断项**已闭合且带一条经变异证明的门;backlog 999.1 两项均已处置;本里程碑第三次出现的门弱点类型在 item 9 与 item 10 各补一处。四个 `must_haves` 工件全部存在、实质、接线且数据流通。硬规则 1/2/3/4 全部保持。全套门在本轮实跑为绿(pytest 219 passed / 6 skipped)。

---

_Verified: 2026-09-25T06:52:38Z_
_Verifier: [CL] (gsd-verifier)_

---
phase: idi-07-interaction-states-and-focus
plan: 01
subsystem: ui
tags: [css, a11y, wcag-1.4.11, focus-visible, outline, design-tokens, contrast-pairs, playwright, uat-harness, element-census, counterfactual-probe]

# Dependency graph
requires:
  - phase: idi-04-tokens-contract
    provides: "`--color-focus: #1f63bd` 的规范出处与三个比值(04-UI-SPEC §「Phase 7 consequence recorded now」)、S-4 的签核算术(「删除 opacity 后环回到 5.62」)—— 本计划环色决策的锚"
  - phase: idi-04.1-radix
    provides: "围栏 `:root` 的 tier-1/tier-2 命名与围栏注释纪律、`check-02-contrast.py` 的 PAIR 清单机制(`PAIR_RE` / `composite()` / `@<alpha>` 后缀 / 覆盖地板)"
  - phase: idi-06-layout-robustness
    provides: "`check-05-ui-uat.py` item 9 的 L-5 clearance 普查与 `CLEARANCE_MIN_PX = 4.0`(SC4 的判据已在盘)、可聚焦普查集 `button, input, select, textarea, a[href], summary, [tabindex]`(D-05 枚举集的直接来源)、`scripts/probe-05-resolve-color.py`(一次性注入探针的定位范本)"
provides:
  - "`frontend/style.css`:围栏内 `--color-focus: #1f63bd` 声明(含「唯一不在 Radix 刻度上」「对已签核契约的字面遵从」「为何不选 blue-11 / blue-12」三条承重注释)"
  - "`frontend/style.css`:文件末尾的七选择器 `:focus-visible` 规则(`outline: 2px solid var(--color-focus)` + `outline-offset: 2px`),含枚举理由 / 同集纪律 / 几何双向绑定 / `[tabindex]` 防御性非冗余四条注释"
  - "`frontend/style.css`:三条 `--color-focus` PAIR 条目(`--color-surface` 5.57 / `--color-surface-page` 5.72 / `--color-surface@0.75` 3.45)+ 清单头部扩写为五层计数 `24 / 34 / 43 / 47 / 50`"
  - "`scripts/check-05-ui-uat.py`:item 10 的四处登记点 + `_idi07_focus_census_assert`(判定集 = 可见 ∧ 可聚焦,非空且未覆盖数为 0)+ SC1 / SC2 / SC4 三条运行时探针 + `FOCUSABLE_SELECTOR` / `FOCUS_RING_WIDTH_PX` / `FOCUS_RING_OFFSET_PX` 与 `_IDI07_*` 三个 JS 常量"
  - "`scripts/probe-07-focus-composite.py`:归档 0.75 合成的一次性反事实探针(**不进守卫契约**)"
affects: ["Phase 7 计划 02 / 03(hover/active 与过渡复用同一套追加位置、同一份 item 10 骨架)", "Phase 8(A11Y-02 的 `tabindex` 承诺:枚举含 `[tabindex]`,届时环自动套上 `#round-doc`;Phase 7 刻意不写针对它的规则,见 D-06)", "/gsd-verify-work idi-07", "/gsd-verify-work idi-04 / idi-04.1-radix / idi-05 / idi-06(本计划改动了 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`,作废这四份报告的全部 live 指纹 —— D-19)"]

actuals:
  tokens: 13341     # chars/4 over the realized diff of the three changed files (53364 chars)
  tasks: 3
  commits: 3        # MEASURED: git rev-list --count 69dea49..HEAD
  plan_head_before: 69dea4985b461a1f91f543d00ab01c533975c885

tech-stack:
  added: []
  patterns:
    - "**环读数只在「该元素成为 `document.activeElement` 的那一刻」采**:`outline` 是焦点伪类的产物,未聚焦元素在 `:focus-visible` 下计算 `outline-width` 为 `0px`、`outline-color` 回落到 UA 值 —— 拿静态读数去判定会把**每一个**元素都判成 bad。故本项的判定面是「采样表 vs 判定集」,不是「静态读数 vs 期望值」"
    - "**判定集必须由合取定义,且空集走 `blocked` 而不是 `info() + return`**:`item_verdict` 只读行级裁决,一条未判定的探针会以 `PASS (N 条断言,0 FAIL,0 BLOCKED)` 的形态现身 —— 「0 条断言静默通过」正是假 PASS 的形态,`len(judged) > 0` 必须是真实守卫"
    - "**「未聚焦读数」不是第二种说法,是已废弃的说法**:本项把「环读数只有一个来源」写进常量注释(清单常量只出清单、`_IDI07_TAB_READ_JS` 只出焦点读数),并用它解释了为什么不得写 `read_style(page, sel, prop)`(那个 helper 按选择器取值,结构上读不到「当前焦点元素」)"
    - "**反事实探针用「注入必须真的发生」自证非空转**:照 `probe-05-resolve-color.py` 的变异防线,断言注入前 `a[href]` 计数 == 0、注入后 == 1;并直接导入 `check-02` 的 `composite()` 复算,而不是自己写一份「差不多的」算术"

key-files:
  created:
    - scripts/probe-07-focus-composite.py
  modified:
    - frontend/style.css
    - scripts/check-05-ui-uat.py

key-decisions:
  - "`--color-focus: #1f63bd` 逐字遵从 S-4 的签核算术,**不改成 `--radix-blue-11`**:`#1f63bd` 是整个颜色层里唯一不在 Radix 刻度上的值(除 `--white` 与两个 `rgba()`),与 04.1「值必须来自 Radix 步」相冲 —— 这条冲突写进围栏注释,否则会被后来者当成漂移「修掉」。实测代价面:blue-11 在 `.archive-mode` 的 0.75 合成下只剩 3.03:1(余量 0.03);blue-12 是高对比文字步,作为 2px 环视觉上接近边框"
  - "三条 `--color-focus` PAIR 用 `check-02` **已有的** `@<alpha>` 合成机制落地,**零新代码**:环对 `--color-surface` 5.57 / 对 `--color-surface-page` 5.72 / 对 `--color-surface@0.75` 3.45。`--color-surface-sunken` 明确**不进验证面**(实测它只是 `.markdown-body code` 与 `.badge-answered` 的背景,不是任何可聚焦元素的相邻地面)—— 理由写进分组注释与清单头部注释"
  - "`focusable` 用 `:disabled` 而不是 `[disabled]`,且排除面**登记而非静默**:前者覆盖「实际被禁用」的全部形态(含被外层 `<fieldset disabled>` 包裹的控件),后者只认写在元素自己身上的属性。禁用控件与 `tabindex=\"-1\"` 的元素 rect 非零、确实渲染在树里,却不在顺序焦点序里 —— 拿它们去要求「被环覆盖」会造出一条**永远无法满足**的判据。本判据是 **Reachable**,不是 Exists"
  - "SC1 实现为「Tab 若干次直到落在**控件**上」而不是「恰好一次 Tab」:实测 `document.body` 是 Tab 循环里的一站(焦点走到最后一个可聚焦元素后落回 BODY),那里 `:focus-visible` 为假、`outline-width` 是 UA 的 `3px` —— 恰好一次会让 SC1 在正常树上 FAIL。全部原始载荷经 `info()` 落盘,不隐藏任何一跳"
  - "反事实探针**额外**用运行时实测的三个输入(环色 / 地面 / 合成因子)复算 `check-02` 的 `composite()`,断言 3.45 >= 3:没有这一步,探针只证明了「服务对象可以造出来」,没有证明「造出来之后那条算术断言成立」—— 而后者才是 D-18 让探针存在的理由"
  - "SC2 目标取 `#btn-send`,**不用** `#btn-process-round`:后者在 p1 的标记里带 `disabled`,`page.click()` 会因 Playwright 的 actionability「enabled」检查抛 `TimeoutError`;而 `force=True` 的「弄绿」写法是假 PASS(禁用控件永远不会成为 `document.activeElement`,`outline-color != --color-focus` 无论 CSS 怎么写都成立)"

patterns-established:
  - "Pattern 1: 焦点样式类断言的判据必须锚在「元素的某一瞬状态」上 —— 把伪类状态当成静态读数会同时产生假 FAIL(未聚焦元素读不到环)与假 PASS(禁用控件读不到环)"
  - "Pattern 2: 枚举式规则的枚举集与门的普查集**逐字同集**,并在两侧都写明「新增一类可聚焦元素要同时改两处」—— 只改一处会让「规则覆盖了谁」与「门检查了谁」重新分叉,那正是 G-idi-05-1 的成因"
  - "Pattern 3: 反事实探针(不进守卫契约)与常驻门的分工 —— 门承担可重复的算术断言,探针承担「这条断言有没有服务对象、它的算术在真实渲染值上成不成立」"

requirements-completed: [A11Y-01]

coverage:
  - id: D1
    description: "全站作者化焦点环:`--color-focus: #1f63bd` 在围栏内声明一次,并由文件末尾的七选择器 `:focus-visible` 规则消费(`outline: 2px solid var(--color-focus)` + `outline-offset: 2px`);规则体不含 `border` / `padding`,不含置空 outline 的写法"
    requirement: "A11Y-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 10(SC1:Tab 到控件后 outline-width == 2px 且 outline-color == var(--color-focus),p1 / checking / p3 三样本)"
        status: pass
      - kind: other
        ref: "bash scripts/check-01-token-conformance.sh(围栏外裸 hex == 0 且 tier-1 `var()` 泄漏 == 0)"
        status: pass
    human_judgment: false
  - id: D2
    description: "环色的三处验证面全部进 `check-02` 的 PAIR 清单并达标(5.72 / 5.57 / 3.45 >= 3:1);清单头部的值层计数注释扩写为五层 `24 / 34 / 43 / 47 / 50` 并与清单实际条目数一致"
    requirement: "A11Y-01"
    verification:
      - kind: unit
        ref: ".venv/bin/python scripts/check-02-contrast.py(3 条 --color-focus 配对全 PASS,末行 `PASS: 0 failures`)"
        status: pass
    human_judgment: false
  - id: D3
    description: "归档半场的**一次性反事实探针** `scripts/probe-07-focus-composite.py`(不进守卫契约):注入真的发生(0 -> 1)、归档态真的生效(opacity 0.75)、注入链接真的被环覆盖,且用运行时实测值复算合成算术 3.45 >= 3"
    requirement: "A11Y-01"
    verification:
      - kind: integration
        ref: ".venv/bin/python scripts/probe-07-focus-composite.py(exit 0)"
        status: pass
    human_judgment: false
  - id: D4
    description: "`check-05` item 10 的焦点环**元素普查**(D-16):判定集(可见 ∧ 可聚焦,即 Tab 可达)非空,且其中未被环覆盖的元素数为 0;禁用控件与 `tabindex=\"-1\"` 的排除已登记"
    requirement: "A11Y-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 10(p1 判定集 9 个 / checking 8 个 / p3 9 个,未覆盖均为空)"
        status: pass
    human_judgment: false
  - id: D5
    description: "SC1(Tab 出环)/ SC2(鼠标点击不出环)/ SC4(滚到底后环不被裁切)三条运行时探针,各有明确 PASS 或 BLOCKED,无空转 PASS"
    requirement: "A11Y-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 10(item 10: PASS,11 条断言,0 FAIL,0 BLOCKED;exit 0)"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8,9(既有九项仍全绿,exit 0)"
        status: pass
    human_judgment: false

duration: 10min
completed: 2026-09-23
status: complete
---

# Phase 7 Plan 01: 焦点环端到端(令牌 → 规则 → 算术门 → 浏览器读数)Summary

**`--color-focus: #1f63bd` 从零建成可断言:围栏内一条令牌 + 文件末尾一条七选择器 `:focus-visible` 规则 + `check-02` 的三条配对(5.72 / 5.57 / 3.45)+ `check-05` 新增 item 10 的**元素普查**(三个样本的判定集 9 / 8 / 9 个 Tab 可达元素,未被环覆盖数均为 0)与 SC1 / SC2 / SC4 三条运行时探针,外加一条不进守卫契约的归档合成反事实探针。**

## Performance

- **Duration:** 10 min
- **Started:** 2026-09-23T05:49:52Z
- **Completed:** 2026-09-23T06:00:11Z
- **Tasks:** 3
- **Files modified:** 3(1 新建 / 2 修改)

## Accomplishments

- **令牌与消费者同一次提交(硬规则 5)**:`--color-focus: #1f63bd` 落在围栏 `:root` 的 tier-2 分组里,注释逐字登记了三条承重事实 —— 它是整个颜色层里**唯一不在 Radix 刻度上**的值(除 `--white` 与两个 `rgba()`)、这是**对 S-4 已签核契约的字面遵从而非漏改**、以及为何不选 `--radix-blue-11`(0.75 合成下只剩 3.03:1,余量 0.03)/ `--radix-blue-12`(高对比文字步,2px 环视觉上接近边框)。
- **焦点规则追加在文件末尾(硬规则 3)**:七选择器枚举与 `check-05` 的可聚焦普查集**逐字同集**(`button, input, select, textarea, a[href], summary, [tabindex]`,顺序亦同),注释写明「新增一类可聚焦元素要**同时**改两处」;几何 `2px + outline-offset: 2px` 的外伸量恰为 4px,正是 `CLEARANCE_MIN_PX = 4.0` 与 `idi-06-UI-SPEC.md §L-5` 假设的值 —— **改几何即改那个门的阈值**。`[tabindex]` 今天无服务对象(全站计数 0),照 06-CONTEXT D-09 的 `min-width: 0` 形态写成**防御性非冗余**,并登记 Phase 8 给 `#round-doc` 加 `tabindex="0"` 时这一条会自动套上环;本阶段**不写**任何针对 `#round-doc` 的规则(D-06,今天不可聚焦 ⇒ 死代码)。
- **环色的三处验证面零新代码落地**:复用 `check-02` 已内建的 `@<alpha>` 合成机制,`--color-focus` 对 `--color-surface` 5.57 / 对 `--color-surface-page` 5.72 / 对 `--color-surface@0.75` 3.45 全部 >= 3:1;清单头部的值层计数注释同步扩写为五层 `24 / 34 / 43 / 47 / 50`,并写明 `--color-surface-sunken` **不进验证面**的理由。`^PASS` 行数由基线 48 增至 51。
- **item 10 按「元素普查」口径断言环覆盖(D-16)**:判定集 = 可见 ∧ 可聚焦(即 Tab 可达),三个样本分别为 9 / 8 / 9 个元素,**未被环覆盖数均为 0**;判定集为空集走 `blocked(...)` 而不是 `info() + return`(对 item9 第 3 条的有意收紧),理由是 `item_verdict` 只读行级裁决 —— 未判定的探针会以 `PASS (N 条断言,0 FAIL,0 BLOCKED)` 的形态现身,那正是假 PASS。
- **SC1 / SC2 / SC4 三条运行时探针各有明确结论**:SC1(p1 / checking / p3 三样本,Tab 到控件后 `outline-width == 2px` 且 `outline-color == rgb(31, 99, 189)`)、SC2(p1,点击 `#btn-send` 后 `document.activeElement` 就是它、`outline-color` 为 `rgb(255, 255, 255)` != 环色)、SC4(p1,滚到底后 11 行 clearance 全部 >= 4px)。`item 10: PASS (11 条断言,0 FAIL,0 BLOCKED)`,exit 0。
- **归档半场的运行时空缺被显式登记,并由一次性探针提供可复跑证据**:五个状态样本的 `#round-doc` 内 `a[href]` 计数为 0 这一事实写进了 item 10 的说明块(不登记它,读者会把「没有断言」误读成「没有风险」);`scripts/probe-07-focus-composite.py` 在 `archive` 样本里向 `#round-doc` 合成一个 `<a href>`(**注入前 0 → 注入后 1**,自证非空转),Tab 驱动焦点后读到环色 == 运行时解析的 `--color-focus`,并用**运行时实测**的环色 / 地面 / alpha 复算 `check-02` 的 `composite()`,得 `ratio=3.45` —— 与常驻算术门的结论逐位一致。

## Task Commits

Each task was committed atomically:

1. **Task 1 (tracer): 焦点环端到端 —— 一条令牌 → 一条 CSS 规则 → 算术门 → 浏览器里读到的环** - `ee47beb` (feat)
2. **Task 2: 补齐环色的三处验证面 + 清单计数注释 + 归档半场的一次性反事实探针** - `0e5820a` (feat)
3. **Task 3: 焦点环覆盖的元素普查(D-16)+ SC1 / SC2 / SC4 三条运行时探针** - `0243d6b` (feat)

**Plan metadata:** 见本计划的 docs 元数据提交(SUMMARY + STATE + ROADMAP + REQUIREMENTS)

## Files Created/Modified

- `frontend/style.css` - 围栏内 `--color-focus: #1f63bd` 声明与它的三条承重注释;围栏内 PAIR 清单新增三条 `--color-focus` 条目与分组注释;清单头部计数注释扩写为五层;文件末尾追加七选择器 `:focus-visible` 规则与其四条注释
- `scripts/check-05-ui-uat.py` - item 10 的四处登记点(docstring 运行方式 / docstring 逐项说明 / `--item` help / `normalize_items` + `known` + 分发块);`FOCUSABLE_SELECTOR` / `FOCUS_RING_WIDTH_PX` / `FOCUS_RING_OFFSET_PX` / `FOCUS_RING_WIDTH_CSS` / `_IDI07_TAB_LIMIT` 与 `_IDI07_FOCUS_CENSUS_JS` / `_IDI07_TAB_READ_JS` / `_IDI07_TAB_CLEARANCE_JS`;`_idi07_blur_reset` / `_idi07_tab_drive` / `_idi07_focus_census_assert` / `_idi07_sc1_assert` / `_idi07_sc2_assert` / `_idi07_sc4_assert`;`item10`
- `scripts/probe-07-focus-composite.py` - **新建**。归档 0.75 合成的一次性反事实探针,定位逐字照 `scripts/probe-05-resolve-color.py`(不进四条守卫命令契约、不被任何门引用),复用 harness 的 `make_fixture` / `enter_project` / `read_style` / `resolve_color` / `effective_bg` 与 `check-02` 的 `composite()` / `contrast_ratio()`

## Decisions Made

- **环色逐字遵从 S-4 的签核算术,不「修正」成 `--radix-blue-11`**:`#1f63bd` 不在 Radix 刻度上,与 04.1 的「值必须来自 Radix 步」纪律相冲 —— 这条冲突本身写进了围栏注释,并给出实测代价面(blue-11 在 0.75 合成下 3.03:1,余量 0.03)。
- **`--color-surface-sunken` 明确不进环色的验证面**:实测它只是 `.markdown-body code` 与 `.badge-answered` 的背景,不是任何可聚焦元素的相邻地面;理由同时写进 PAIR 分组注释与清单头部注释。
- **`focusable` 用 `:disabled` 而不是 `[disabled]`**:前者覆盖「实际被禁用」的全部形态(含被外层 `<fieldset disabled>` 包裹的控件)。排除面逐个点名本仓库真实实例(`index.html:126` 的 `#btn-approve-draft[disabled]`、`index.html:143` 的 `#btn-authorize[disabled]`、计划 02 的两个 `.verdict-buttons button:disabled`),并写明结论:**本判据是 Reachable,不是 Exists**。
- **SC1 实现为「Tab 若干次直到落在控件上」**:实测 `document.body` 是 Tab 循环里的一站,那里 `:focus-visible` 为假、`outline-width` 是 UA 的 `3px` —— 恰好一次 Tab 会让 SC1 在正常树上 FAIL。全部原始载荷经 `info()` 落盘。
- **SC2 目标取 `#btn-send` 而非 `#btn-process-round`**:后者在 p1 的标记里带 `disabled`,`page.click()` 会因 Playwright 的 actionability「enabled」检查抛 `TimeoutError`;`force=True` 的「弄绿」写法是假 PASS。
- **反事实探针额外复算合成算术**:用运行时实测的环色 / 地面 / alpha 直接调用 `check-02` 的 `composite()`,断言 `3.45 >= 3`。没有这一步,探针只证明了「服务对象可以造出来」,没有证明「造出来之后那条算术断言成立」。

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] SC1 由「恰好一次 Tab」改为「Tab 若干次直到落在控件上」**
- **Found during:** Task 3(item 10 的 SC1 探针)
- **Issue:** 计划写的是「`page.keyboard.press("Tab")` 后读 `_IDI07_TAB_READ_JS` 返回的载荷 ... 载荷为 `null` ⇒ `blocked`」。但实测 `document.body` 是 Tab 循环里的一站(p1 实测序列 `#btn-divergence → body → #message-input → ...`,checking 与 p3 同形),`body` 是 `HTMLElement` 故载荷不为 `null`,而那里 `:focus-visible` 为假、`outline-width` 是 UA 的 `3px` —— 恰好一次 Tab 会让 SC1 在**正常树上** FAIL,而这不是探针写错,是「一次 Tab」这个假设不成立。
- **Fix:** 循环 Tab 至多 `_IDI07_TAB_LIMIT`(12)次,停在第一个落在**控件**(`tag not in ("body", "html")`)上的载荷;全部原始载荷经 `info()` 落盘,不隐藏任何一跳;始终没落到控件上仍走 `blocked(...)`。计划的「Tab 驱动的探针先跑、SC2 最后跑」这条顺序约束原样保留。
- **Files modified:** scripts/check-05-ui-uat.py
- **Verification:** `--item 10` exit 0,SC1 在 p1 / checking / p3 三个样本上各两条 PASS(`outline-width == 2px`、`outline-color == rgb(31, 99, 189)`,焦点伪类匹配均为 `True`)。
- **Committed in:** `0243d6b` (Task 3 commit)

**2. [Rule 2 - Missing Critical] 反事实探针补上「用运行时实测值复算合成算术」这一步**
- **Found during:** Task 2(`scripts/probe-07-focus-composite.py`)
- **Issue:** 计划列出的断言(注入前 0 / 注入后 1、`outline-color == resolve_color(--color-focus)`、archive-mode 在位)只证明了「那个服务对象可以被造出来」。而 D-18 让这条探针存在的理由是「证明 `--color-focus ON --color-surface NON-TEXT@0.75` 这条算术断言**真的会失败/成立**,而不是静默空转」—— 少了算术那一半,探针证明不了它的立身之本。
- **Fix:** 探针额外从运行时读三个输入(环的计算 `outline-color`、`effective_bg()` 沿祖先链得到的地面、`#round-doc` 的计算 `opacity`),**直接导入 `check-02` 的 `composite()` / `contrast_ratio()`**(不另写一份「差不多的」实现)复算并断言 `>= 3:1`;同时把 `#round-doc` 的计算 `opacity` 恰为 `0.75` 升为**断言**(而不是采信常量),确保被测态与 PAIR 条目所建模的态是同一个。
- **Files modified:** scripts/probe-07-focus-composite.py
- **Verification:** `.venv/bin/python scripts/probe-07-focus-composite.py` exit 0,输出 `composited=(86, 136, 204) ratio=3.45`,与常驻算术门 `check-02` 的 `PASS 3.45 --color-focus on --color-surface@0.75` 逐位一致。
- **Committed in:** `0e5820a` (Task 2 commit)

---

**Total deviations:** 2 auto-fixed(1 blocking,1 missing critical)
**Impact on plan:** 两处都是「让断言真的在测它声称要测的东西」,没有扩大改动面 —— `frontend/app.js` / `frontend/index.html` / `frontend/vendor/` / `scripts/ui-states/` 零改动(硬规则 5),`check-01`…`check-04` 四条既有门与既有九项 UAT 全绿。零新增运行时依赖、零构建步骤、零 `!important`、零 `@media`(T-idi-07-SC 的 accept 面未被触及)。

## Tracer Feedback Gate(Task 1 是 `type="tracer"`)

- Task 1 无 `gate` 属性 ⇒ 不触发 `blocking-human` 分支。
- 实测 auto 模式**活跃**:`gsd_run query check auto-mode` 返回 `{"active": true, "source": "auto_advance"}`(与 `.planning/config.json` 的 `workflow.auto_advance: true` 一致),`HUMAN_VERIFY_MODE` = `end-of-phase`。
- 按 auto 模式分支**端到端复跑 Task 1 的 `<verify>`**:`check-01` PASS、`check-02` 末行 `PASS: 0 failures`、`check-03` PASS、`check-04` PASS、`grep -v '^#' frontend/style.css | grep -c ':focus-visible'` = 9(>= 7)、`.venv/bin/python scripts/check-05-ui-uat.py --item 10` exit 0 —— **全绿,未 HALT**,记 `⚡ Tracer verified end-to-end — expanding`,随后才进入 Task 2 与 Task 3 的扩展面。

## Issues Encountered

- **Task 2 的 `<files>` 列了 `scripts/check-05-ui-uat.py`,但该任务对该文件零改动。** 原因是计划在 Task 1 的四处登记点里**已经**要求「在 item 10 的 docstring 说明块里登记五个状态样本 `#round-doc` 内 `a[href]` 计数为 0 这一事实」,而 Task 2 的动作又重复了同一条要求。两处要求指向同一段文字,故 Task 1 落地后 Task 2 无需再改 —— 这是计划内的**重复登记**,不是遗漏。Task 2 的 `<done>` 判据(「`check-05` 的说明块里登记了 …」)由 Task 1 落下的同一段文字满足,已逐字复核。
- **Task 3 的编辑过程中曾误删 `_rects_intersect` 的一处换行**(Edit 的 `old_string` 多吃了一个换行,导致 docstring 与 `return not (` 并到一行)。同一步内立即修正;最终提交的 diff 对该函数**零改动**(`git diff --numstat` 显示 477 增 / 50 删,删除全部来自被替换的 Task 1 版 `item10` 骨架)。无残留。
- **`state.update-progress` 把 `completed_phases` / `percent` 往回改了,已手工纠正。** 该 handler 执行后 `STATE.md` 的 frontmatter 从 `completed_phases: 1 / percent: 17` 变成 `0 / 0`,正文进度条从 `[██░░░░░░░░] 17%` 变成 `[░░░░░░░░░░] 0%`(它似乎是从 `.planning/state.json` 的 `phases` 数组推的,而那个数组的 `status` 字段不是权威 —— 见本项目已登记的同类记录)。按 **ROADMAP 的 `## Milestones` + `## Progress`** 判据(v1.14 的 6 个阶段里 4 / 4.1 / 5 / 6 为 Complete)纠正为 `completed_phases: 4` / `percent: 67` / `[███████░░░] 67%` —— 这正是本仓库 `0f5ffd7`(「correct the derived percent in state.json next.reason (17 -> 67)」)已确立的派生值,与历史进度条的 `67%` 形态逐字一致。`completed_plans` 的 `15 -> 16` 是正确的增量,保留。同一 handler 还把 `.planning/state.json` 的 `next.reason` 从 `Phase 7 of 6 · 67% · executing` 改成 `Phase 07 of 6 · 0% · executing`,已改回原值(该文件与 HEAD 的唯一差异现在只剩 `updated_at` 时间戳)。**下一份计划执行后请复跑同样的核盘判据,不要采信该 handler 的输出。**
- **三个一次性临时文件未能删除(权限系统拒绝 `rm` / `unlink`),留在工作区且未提交**:`.planning/.idi07-dec1.txt` / `.idi07-dec2.txt` / `.idi07-dec3.txt`。它们只是喂给 `gsd-tools query state.add-decision` 的输入文本(内容已逐字进入 `STATE.md` 的 Decisions 区),不参与任何门或构建。**请手工 `rm` 掉这三个文件**;执行器在多次尝试后被权限系统拒绝,未采取任何绕过手段。
- **环境事实(照旧,未对抗)**:截图不可用 ⇒ 全部验收走计算样式读数;浏览器走默认 `--browser bundled`(Playwright 自带 chromium 153.0.8010.12,可无头);`page.keyboard.press("Tab")` 不受「键盘文本选区无法自动化」那条限制(该限制只针对 Shift+方向键选字)。

## Known Stubs

无 —— 本计划新增/修改的三个文件里没有硬编码空值、占位文案、TODO/FIXME,也没有「组件没有数据源」的形态。新增的两个断言常量(`FOCUSABLE_SELECTOR` / `FOCUS_RING_*`)都是被消费的(`grep -o 'FOCUSABLE_SELECTOR' | wc -l` = 3)。

## Threat Flags

无 —— 本计划只新增声明式 CSS 与测试脚本,未引入任何新的网络端点、认证路径、文件访问模式或信任边界上的 schema 变更。计划 `<threat_model>` 的 T-idi-07-01…05 逐条落到实现面:T-01(祖先 `opacity` 合成)由三条 PAIR + 探针承担;T-02(几何里的 `border` / `padding`)由规则体只声明 `outline` 与 `outline-offset` 承担(静态判据:`awk` 提取围栏外 `outline:` 行数恰为 1、`outline: none` 计数为 0);T-03(环色「顺手修正」)由围栏注释承担;T-04(假 PASS)由「判定集空集 ⇒ `blocked`」与「SC4 空集 / 不可见 ⇒ `blocked`」承担;T-05(归档半场无服务对象)由显式登记 + 一次性探针承担。

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Ready for idi-07-02**(交互态语言 INTERACT-01):本计划已把环色令牌、`:focus-visible` 规则的追加位置(文件末尾)、PAIR 清单的记账位置、item 10 的骨架与四处登记点全部就位;计划 02 只需在同一处追加 `:hover` / `:active` 规则与它自己的 PAIR 条目,并往 item 10 里加 SC5 / SC5′。
- **Phase 8 的接口已就位**:枚举含 `[tabindex]`,Phase 8 给 `#round-doc` 加 `tabindex="0"` 时这一条会**自动**把环套上去;Phase 7 刻意不写针对 `#round-doc` 的规则(D-06)—— 这是本阶段唯一跨阶段的开放项,已在 `07-CONTEXT.md` 的 deferred 与 canonical_refs 两处登记。
- **D-19 的连带复验义务已被本计划触发**:`frontend/style.css` 与 `scripts/check-05-ui-uat.py` 的字节都变了 ⇒ `.planning/phases/` 下覆盖这两个文件的四份报告(`idi-04` / `idi-04.1-radix` / `idi-05` / `idi-06`)的 `covered_digest` 全部作废。收口时须**以 HEAD 内容重算指纹**(不要看 mtime),且**不得**用 `gsd-tools query verification status <phase>` 判定(相位目录命名与该工具的相位令牌解析不匹配,一律返回 `missing`)。`STATE.md` 的 Operator Next Steps 第 2 条(`/gsd-verify-work idi-04.1-radix`)在本计划开始前仍未收口。
- **本计划的验收边界(不得误读)**:item 10 的普查证明的是**几何覆盖与可达性**(判定集里每个 Tab 可达元素都被环覆盖),不是环色的**视觉**充分性 —— 后者的数值面由 `check-02` 承担(5.72 / 5.57 / 3.45),而 SC5″(「一眼看出不可点」的感知主张)是计划 02 的具名人工验收项,不在本计划内。

---
*Phase: idi-07-interaction-states-and-focus*
*Completed: 2026-09-23*

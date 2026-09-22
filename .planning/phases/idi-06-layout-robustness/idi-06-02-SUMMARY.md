---
phase: idi-06-layout-robustness
plan: 02
subsystem: ui
tags: [css, layout, overflow-wrap, min-width, scroll-containers, playwright, uat-harness]

# Dependency graph
requires:
  - phase: idi-06-layout-robustness
    provides: "`#doc-panel-header` 的 sticky 规则与 `item8`(L-1 切片);`#doc-panel { overflow-y: auto }` 仍是 sticky 的滚动容器 ⇒ 本计划必须保留它"
  - phase: idi-05-typography-and-visual-hierarchy
    provides: "`MARKDOWN_TARGETS` 的九目标枚举纪律、`check_render_markdown_call_sites` 的「读文件文本算计数、比两个独立量」范式、item7 的「对 None 恒真」陷阱登记"
provides:
  - "`frontend/style.css` 末尾追加的一条六选择器 `overflow-wrap: anywhere` 规则(全文件首条 `overflow-wrap`)+ `#main-pane` / `#doc-panel` 两条既有规则体内各新增一行 `min-width: 0;`"
  - "`.event-list` 与 `#annotation-list` 两条既有规则体内各删除 `max-height` + `overflow-y` 两条声明(面板区滚动者 3 → 1 个外层 + 1 个保留的内层)"
  - "`scripts/check-05-ui-uat.py` 的 `item9`(滚动者 DOM 普查两条 + 末条可达性两条 + 计算 `max-height == none` 两条 + 保留项护栏两条)与三处派发接入"
  - "波次 2 之后的三宽度文档级溢出读数(1440 / 1024 / 768 均为 0px)—— 计划 03 的 L-2 判据对照值"
affects: ["idi-06-03(L-2 的判据必须用本计划之后的读数;L-5 普查读 `#annotation-list` 的 padding)", "Phase 7(焦点环 4px clearance 与 `overflow-wrap` 的 min-content 交互)"]

actuals:
  tokens: 5690      # chars/4 over the realized diff of the two changed files (22758 chars)
  tasks: 3
  commits: 3        # MEASURED: git rev-list --count 3f5e729..HEAD
  plan_head_before: 3f5e7293913a807f8e77c027bade9770e543ebf6

tech-stack:
  added: []
  patterns:
    - "「追加,不重排」(硬规则 3)在**结构性 diff** 上的双形态:新增规则追加在文件末尾,删除/新增声明一律原地改规则体,规则块零移动"
    - "断言必须能 PASS:恒 FAIL 的断言(计算样式对 `vh` 返回 px 用值 ⇒ `== \"30vh\"`;末条子元素高于容器 ⇒ `last.top >= container.top`)与被断言对象同属缺陷,按 Rule 1 改正并登记,不靠改源码去凑绿"
    - "一条可达性主张拆成两个样本各出一半证据(容器可见性是前提,不可见的样本记 blocked 而非假 PASS)"
    - "保留项护栏读两种量:能读关键字值的读计算样式,只能读字面量的读源码文本计数 —— 互补抓「被改值」与「被悄悄删掉」"

key-files:
  created: []
  modified:
    - frontend/style.css
    - scripts/check-05-ui-uat.py

key-decisions:
  - "六目标合并为**一条六选择器规则**而非六条:与 Phase 5「逐容器列举而非一条全局规则」同一口径,既让影响面机械可枚举,又不误伤 `.event-content` 已裁定的 `word-break: break-all`(通配规则会波及它,那正是 `G-idi-05-1` 的成因)"
  - "`min-width: 0` 的注释里**不写**带分号的同形串:验收用 `grep -o 'min-width: 0;' | wc -l` 计数(基线 1 + 本计划 2 = 3),注释里的同形串会把计数抬到 5。六目标规则的注释同理不复写 `overflow-wrap: anywhere;`"
  - "`#doc-panel` 的 `overflow-y: auto` **保留**:它是**另一列**的滚动者,不在面板区普查范围内,但 L-1 的 sticky 表头依赖它仍是最近的可滚祖先。删掉它「凑到 3」会同时打破 L-1 与全文件计数门(6 − 2 = 4)"
  - "`#latest-check` 的保留项护栏**按源码文本计数**而非计算样式:捆绑 chromium 下 `max-height: 30vh` 在 1440×900 解析为 `270px`(本次实测容器高恰为 270.0),`getComputedStyle` 永远不会返回字符串 `\"30vh\"` ⇒ 计算样式断言是恒 FAIL 的"
  - "`item9` 的末条可达性拆两个样本:`#main-pane` 在 `p1`(需 `#ai-events` 可见),`#latest-check` 在 `checking`(需 `#checks-panel` 可见,`p1` 下它是 `display: none`、rect 全零)"
  - "滚动者普查只跑 `p1`:七个 `overflow` 声明所在的元素全部是 `index.html` 的静态元素,普查结果与磁盘状态样本无关 —— 这是它比「按样本逐格探」更强的地方"

patterns-established:
  - "Pattern 1: 几何/可达性断言必带**显式前提检查**(容器可见且 rect 高 > 0),前提不成立记 blocked() —— 与 item7 的 `all(w != \"700\")` 对 None 恒真同型陷阱"
  - "Pattern 2: 一条主张若在两个样本上各有一半证据,就分两段跑并在注释里写明「为什么必须是这个样本」,不合并成一条会空转的断言"
  - "Pattern 3: 断言自身也要做变异测试(把期望集合改错,确认它真的 FAIL),否则无法区分「守卫通过」与「守卫恒真」"

requirements-completed: [LAYOUT-02, LAYOUT-04]

coverage:
  - id: D1
    description: "六目标换行保护:`.markdown-body` / `.event-content` / `.chat-bubble` / `.say-chunk` / `.annotation-note` / `.annotation-answer-body` 获得 `overflow-wrap: anywhere`(文件末尾追加一条六选择器规则),不可断长串换行而不撑破视口"
    requirement: "LAYOUT-02"
    verification:
      - kind: other
        ref: "grep -o 'overflow-wrap: anywhere;' frontend/style.css | wc -l  # == 1;grep -c '^\\.markdown-body, \\.event-content, \\.chat-bubble, \\.say-chunk, \\.annotation-note, \\.annotation-answer-body {' # == 1(行号 1303 > 末尾三条嵌入标题刻度规则 1292,确在文件末尾)"
        status: pass
      - kind: other
        ref: "grep -o 'word-break: break-all;' frontend/style.css | wc -l  # == 1;grep -o 'white-space: pre-wrap;' | wc -l  # == 1(已裁定的 .event-content 保护逐字存活)"
        status: pass
    human_judgment: false
  - id: D2
    description: "`#main-pane` 与 `#doc-panel` 两条**既有**规则体内各原地新增一行 `min-width: 0;`,`#doc-panel` 不再能被不可断长内容顶得比它的 `clamp(340px, 30vw, 480px)` 还宽"
    requirement: "LAYOUT-02"
    verification:
      - kind: other
        ref: "grep -o 'min-width: 0;' frontend/style.css | wc -l  # == 3(1 条既有 @ :685 + 新增 2 条 @ :465 / :486);grep -n -A 12 '^#main-pane {' | grep -o 'min-width: 0;' | wc -l  # == 1;同 #doc-panel"
        status: pass
    human_judgment: false
  - id: D3
    description: "面板区滚动容器收敛:`.event-list` 与 `#annotation-list` 不再内部滚动,面板区内计算 `overflow-y` 为 `auto`/`scroll` 的集合恰为 `{#main-pane, #chat-messages, #latest-check}`(排除 SC#3 明文豁免的 `#chat-messages` 后恰为两者)"
    requirement: "LAYOUT-04"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 9  # 两条滚动者集合断言,实测数组 ['#main-pane', '#chat-messages', '#latest-check']"
        status: pass
      - kind: other
        ref: "grep -o 'max-height: 55vh;' frontend/style.css | wc -l  # == 0;grep -o 'max-height: 32vh;' | wc -l  # == 0;grep -o 'overflow-y: auto;' | wc -l  # == 4"
        status: pass
    human_judgment: false
  - id: D4
    description: "删除两个内层滚动者之后内容仍可达:`#main-pane` 与 `#latest-check` 滚到底后末条内容落在各自可视区内"
    requirement: "LAYOUT-04"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 9  # #main-pane: scrollHeight=2640 clientHeight=900 scrollTop=1740 last=#ai-panel last.bottom=900 container=[0,900];#latest-check: scrollHeight=4585 clientHeight=268 scrollTop=4317 last=p last.bottom=338.6875 container=[84,354]"
        status: pass
    human_judgment: false
  - id: D5
    description: "保留项护栏:`#latest-check` 的 30vh 内滚动仍在(裁决按钮不被推出折叠线),`#chat-messages` 的 `overflow-y` 与 `#session-panel` 族零改动(输入行仍钉底)"
    requirement: "LAYOUT-04"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 9  # 「#chat-messages overflow-y == auto」(计算样式)+「frontend/style.css 的 max-height: 30vh 声明计数 == 1」(源码文本,命中行 1144)"
        status: pass
      - kind: other
        ref: "grep -o 'min-height: 160px;' frontend/style.css | wc -l  # == 1;grep -o 'min-height: 200px;' | wc -l  # == 1;grep -c '^#session-panel {' # == 1;grep -o 'max-height: 30vh;' | wc -l  # == 1"
        status: pass
    human_judgment: false
  - id: D6
    description: "`scripts/check-05-ui-uat.py` 新增 `item9` 并接入三处派发,`--item 9` 可单跑并全绿;`item8`(波次 1 的 tracer 门)无回归"
    requirement: "LAYOUT-04"
    verification:
      - kind: e2e
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 9  # exit=0,item 9: PASS (10 条断言,0 FAIL,0 BLOCKED)"
        status: pass
      - kind: e2e
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,4,7,8  # 9 / 45 / 65 / 38 / 7 条,全 PASS,与波次 1 结束时逐字相同"
        status: pass
    human_judgment: false
  - id: D7
    description: "窄窗口(1440 / 1024 / 768)文档级无横向溢出 —— LAYOUT-02 的**最终判据**"
    requirement: "LAYOUT-02"
    verification: []
    human_judgment: true
    rationale: "本计划只落 L-3 的换行与最小尺寸;**判据要等计划 03 在波次 2 之后的树上重测**(UI-SPEC §L-2 的窄窗口守卫是计划 03 的条件交付物,且最多一条 `@media`)。本计划实测三宽度 overflow 均为 0px,但波次 1 的基线**同样**是 0px ⇒ 该读数不能区分「L-3 修好了」与「本来就没破」,故不据此宣称 LAYOUT-02 达标。"

# Metrics
duration: 24min
completed: 2026-09-22
status: complete
---

# Phase 6 Plan 02: 布局稳健性 — 换行 / flex 最小尺寸 / 滚动容器收敛 Summary

**六目标 `overflow-wrap: anywhere` 把不可断长内容的横向撑破从根上堵死(配 `#main-pane` / `#doc-panel` 两处 `min-width: 0` 兜底),`.event-list` 与 `#annotation-list` 的限高与内滚动原地删除后面板区滚动者收敛为「1 个外层 + 1 个保留的内层 + 1 个明文豁免的会话流」,并由 check-05 `item9` 的 DOM 普查 + 末条可达性 + 两条保留项护栏机械复核**

## Performance

- **Duration:** 24 min
- **Started:** 2026-09-22T03:41:55Z
- **Completed:** 2026-09-22T04:06:19Z
- **Tasks:** 3
- **Files modified:** 2

## Accomplishments

- `frontend/style.css` 末尾**追加**一条六选择器规则 `.markdown-body, .event-content, .chat-bubble, .say-chunk, .annotation-note, .annotation-answer-body { overflow-wrap: anywhere; }`(全文件**首条** `overflow-wrap`),带 UI-SPEC §L-3 的逐字承重注释(枚举与调用点一一对应 / 不写通配规则 / 必须 `anywhere` 而非 `break-word`)。围栏 `:root` 内零改动、零新增令牌。
- `#main-pane` 与 `#doc-panel` 两条**既有**规则体内各原地新增一行 `min-width: 0;`(带 D-09 的「不是冗余代码」注释)—— `#app` 的两个 flex 子项不再被 `min-width: auto` 顶破 `clamp()`。
- `.event-list` 删掉 `max-height: 55vh;` + `overflow-y: auto;`,`#annotation-list` 删掉 `max-height: 32vh;` + `overflow-y: auto;`,**原地改声明、规则块零移动**;其余声明与 `.event-list.streaming` / `.aborted` 逐字保留。
- `scripts/check-05-ui-uat.py` 新增 `item9`:滚动者 DOM 普查两条(全集 == 三者 / 排除豁免后 == 两者,比的是两个独立量)、末条可达性两条(`#main-pane` @ p1、`#latest-check` @ checking,各带可见性前提检查)、计算 `max-height == none` 两条、保留项护栏两条;三处派发接入齐备,`--item 9` 全绿(10 条断言,0 FAIL / 0 BLOCKED)。
- 四条既有静态守卫、`check-06`(g1…g6 全 PASS)、`--item smoke,1,4,7,8`(9 / 45 / 65 / 38 / 7)与 `pytest`(219 passed / 6 skipped)全部与执行前基线逐字一致。

## Task Commits

Each task was committed atomically:

1. **Task 1: L-3 换行与 flex 最小尺寸** - `b623215` (feat)
2. **Task 2: L-4 滚动容器收敛** - `6adcaa3` (refactor)
3. **Task 3: item 9 —— 滚动者普查 + 末条可达性 + `max-height == none`** - `1bd93a6` (feat)

**Plan metadata:** `docs(idi-06-02): complete layout-robustness wrapping-and-convergence plan`(承载本 SUMMARY、STATE.md、ROADMAP.md 与 REQUIREMENTS.md)

## Files Created/Modified

- `frontend/style.css` — 3 个 hunk,全部是**纯新增或纯删除**,无规则块移动:
  `@@ -459,0 +460,6 @@`(`#main-pane` 的注释 5 行 + `min-width: 0;`)、
  `@@ -474,0 +481,6 @@`(`#doc-panel` 同上)、
  `@@ -578,0 +591,3 @@` + `@@ -583,2 +597,0 @@`(`.event-list` 加 3 行注释、删 2 行声明)、
  `@@ -927,0 +941,3 @@` + `@@ -932,2 +947,0 @@`(`#annotation-list` 同形)、
  `@@ -1280,0 +1295,13 @@`(文件末尾的六选择器规则 + 11 行注释)。围栏 `:5` … `:431` 之外。
- `scripts/check-05-ui-uat.py` — 新增 `PANEL_SCROLLERS` / `PANEL_SCROLLERS_EXEMPT` / `STYLE_CSS` / `LATEST_CHECK_MAX_HEIGHT_DECL` / `LATEST_CHECK_PROBE_MD` 五个模块级常量、两个 JS 常量(`_IDI06_SCROLLERS_JS` / `_IDI06_REACH_JS`)、三个函数(`_latest_check_max_height_guard` / `_idi06_reach` / `item9`);`normalize_items` 默认列表、`known` 集合、`main()` 派发三处接入 `"9"`;模块 docstring 新增第 9 项说明并同步运行方式块;`--item` help 项清单加到 `9`。

## Decisions Made

- **六目标合并为一条规则,不用通配。** 通配 `overflow-wrap` 会波及已裁定的 `.event-content { word-break: break-all }`,并把「哪些容器受影响」重新变成不可枚举 —— 那正是 `G-idi-05-1` 的成因。合并为一条六选择器列表既保持机械可枚举,又不误伤。
- **注释里不复写带分号的声明串。** 验收用 `grep -o 'min-width: 0;' | wc -l`(基线 1 + 本计划 2 = 3)与 `grep -o 'overflow-wrap: anywhere;' | wc -l`(须为 1)计数,注释里的同形串会污染计数。两段注释都写不带分号的形式。
- **`#doc-panel` 的 `overflow-y: auto` 保留。** 它是**另一列**的滚动者,不在面板区普查范围内,但 L-1 的 sticky 表头依赖它仍是最近的可滚祖先;删掉它「凑到全文件 3 处」会同时打破 L-1 与计数门(期望值是 4,不是 3)。
- **`#latest-check` 的护栏读源码文本,不读计算样式。** 实测:1440×900 下 `max-height: 30vh` 的容器高恰为 **270.0px** —— `getComputedStyle` 返回的是 px 用值,断言 `== "30vh"` 恒 FAIL。改为 `frontend/style.css` 文本计数 == 1(命中行 1144)。
- **末条可达性拆两个样本。** `#main-pane` 需 `#ai-events` 可见(仅 `p1`),`#latest-check` 需 `#checks-panel` 可见(仅 `checking`;`p1` 下它 `display: none`、rect 全零)。在错误的样本上读到的几何量全零,那正是威胁表 T-idi-06-10(假 PASS)的落点。
- **滚动者普查只跑 `p1`。** 七个 `overflow` 声明所在的元素全部是 `index.html` 的静态元素,普查与磁盘状态样本无关。

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] 末条可达性判据的上边缘一项恒不成立,改为下边缘落在可视带内**

- **Found during:** Task 3(item 9 实现前的几何探针)
- **Issue:** 计划把可达性不变量写成 `last.bottom <= container.bottom + 1 && last.top >= container.top - 1`。实测 `p1` 下 `#main-pane` 的末条子元素是 `#ai-panel`,高 **2434px**,而容器高 **900px** —— `last.top = -1534` 永远 `< container.top - 1`。即:只要末条子元素本身高于容器(滚动容器的常态),该式**恒 FAIL**。这与计划自己点名要避免的 `== "30vh"` 是同一类缺陷:恒 FAIL 的断言会让 `--item 9` 永远无法转绿,并使计划 03 的 `--item smoke,1,2,3,4,6,7,8,9` 收口门同样不可达。
- **Fix:** 判据改为 `container.top <= last.bottom <= container.bottom + 1`。真正的承重主张是「内容**末端**可达」(T-idi-06-06 的机器化形态),即末条的下边缘落在可视带内;上边缘属于被滚动遮住的部分,不影响末端可达性。注释里写明了这次改写与理由。
- **Files modified:** `scripts/check-05-ui-uat.py`
- **Verification:** `--item 9` 两条可达性断言 PASS(`#main-pane`: `last.bottom=900` ∈ `[0, 900]`;`#latest-check`: `last.bottom=338.6875` ∈ `[84, 354]`);对 `#latest-check` 而言新旧判据**同时成立**,故改写不放松既有证明力,只修掉恒假的那一半。
- **Committed in:** `1bd93a6` (part of Task 3 commit)

**2. [Rule 3 - Blocking] 末条可达性证据按容器拆到两个样本**

- **Found during:** Task 3(几何探针)
- **Issue:** 计划在 (b) 里不点名样本,但两个目标容器分属两个互斥的可见态:`#main-pane` 的可达性要 `#ai-events` 有内容(需 `#session-panel` 可见 ⇒ 仅 `p1`),`#latest-check` 的可达性要 `#checks-panel` 可见(仅 `checking`)。在 `p1` 上对 `#latest-check` 做同一条断言,读到的是 `display: none` / rect 全零,只会得到一条 BLOCKED(或更糟:一条空转 PASS)。
- **Fix:** `#main-pane` 在 `p1` 上注入 40 条 `renderEvent` 事件;`#latest-check` 在 `checking` 上经 `renderMarkdown` 注入 60 段探针正文。`_idi06_reach` 对两者共用同一前提检查链(内容已注入 → 容器存在 → 容器可见且 rect 高 > 0),不成立即 `blocked(...)`。
- **Files modified:** `scripts/check-05-ui-uat.py`
- **Verification:** 两条断言均 PASS,且 `info()` 行打印了完整原始几何量(`#main-pane`: scrollHeight 2640 / clientHeight 900 / scrollTop 1740;`#latest-check`: scrollHeight 4585 / clientHeight 268 / scrollTop 4317,容器高 270.0 = 30vh 的用值)。
- **Committed in:** `1bd93a6` (part of Task 3 commit)

**3. [Rule 1 - Bug] Task 2 的「规则体上方加注释」与「hunk 只有删除行」冲突,按后者定形**

- **Found during:** Task 2
- **Issue:** Task 2 的 `<action>` 要求「在规则体上方加一行注释」,而同一任务的验收与计划级 Gate B 都要求 `.event-list` / `#annotation-list` 的 hunk **只有删除行**、无规则块位置变化。字面同时满足两者不可能 —— 加注释必然产生新增行。
- **Fix:** 把注释放在**选择器行之上**(即「规则体上方」的字面位置),使**规则体内部**只剩删除行;规则块位置零移动,既有声明零改动。这是两个要求唯一相容的落点。
- **Files modified:** `frontend/style.css`
- **Verification:** `git diff` hunk 形态:`@@ -578,0 +591,3 @@`(3 行注释)+ `@@ -583,2 +597,0 @@`(2 行声明删除),`#annotation-list` 同形;`grep -n -A 9 '^\.event-list {'` 仍命中 `transition: background-color 0.3s;`(计数 1),`grep -n -A 6 '^#annotation-list {'` 仍命中 `padding: var(--space-half);`(计数 1)。
- **Committed in:** `6adcaa3` (part of Task 2 commit)

---

**Total deviations:** 3 auto-fixed (2 bugs, 1 blocking)
**Impact on plan:** 三条都是「让断言/验收能成立」所必需,不是范围蔓延:没有一条改动产品行为、没有一条新增或删除本计划之外的声明、没有一条触碰范围锁内的文件。Deviation 1 与 3 是计划文本内部的不自洽(恒假判据 / 互斥要求),Deviation 2 是计划未点名的样本选择。

## Issues Encountered

- **自审抓到一条恒真的断言(提交前已修)。** `item9` 第二条普查断言初次写成了 `ok_true(item, label, expected_two, exempted, note)` —— 第 3 个位置是 `cond`,传进去的是一个非空列表 ⇒ 恒真。第一次 `--item 9` 的输出里 `actual=` 显示的是 note 文本而不是集合,正是这一错误的表征。已改为 `ok_true(item, label, exempted == expected_exempted, expected_exempted, exempted, note)`,重跑后 `actual=['#latest-check', '#main-pane']` 正确显示。
- **变异测试证明两条普查断言真的会 FAIL。** 把 `PANEL_SCROLLERS` 改成含 `#ai-events` 的四元组后重跑,两条断言都 FAIL(`actual` 仍是三元组)—— 排除了「守卫恒真」的可能(MEMORY 已登记:变异测试是唯一能证明守卫真的会失败的手段)。
- **三宽度诊断在波次 2 之后仍是 0px(与波次 1 基线相同)。** 见下方「测量记录」块 2。这**不是**缺陷,但它意味着三宽度读数**不能**用来证明 L-3 起了作用 —— 该判据在波次 1 就已经是绿的。计划 03 的 L-2 决策必须用本节的读数作为「波次 2 之后」的对照,并另找能区分两者的证据。

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- 波次 2 的交付物齐备:`frontend/style.css` 的两组改动已在磁盘上,`item9` 可单跑并全绿,四条既有守卫、`check-06`、`--item smoke,1,4,7,8` 与 `pytest` 全部无回归。
- **计划 03 的输入:** 三宽度文档级溢出读数(下方块 2)、`item9` 的逐条结论(下方块 3)、D6-4 / D6-5 两条行为变更登记(下方块 1)。
- **LAYOUT-02 尚未收口:** 它在计划 02 与计划 03 中**同时**声明,按共享 ID 门(#2388)只在最后一个声明它的计划产出 SUMMARY 后才可标 Complete;本计划已把该行的实测证据落盘,但不宣称达标(coverage D7 = `human_judgment: true`)。
- **无阻塞项。** 本计划零新增依赖、零新文件、零新构建步骤;`frontend/app.js` / `index.html` / `vendor/` / `scripts/ui-states/` / `scripts/check-01…04` / `scripts/check-06-idi05-validation.py` 零 diff(逐条 `git status --porcelain` 核实为空)。

---

## 测量记录

> 本节是计划 03(`idi-06-03`)与 Phase 7 的输入契约。原始命令与原始输出,不给结论替代证据。
> 采集时间:2026-09-22T03:45Z – 04:05Z;全部在 Task 3 的生产提交 `1bd93a6` 之上跑出。

### 块 1 —— 本阶段的两条行为变更登记(D6-4 / D6-5,UI-SPEC §Deliberate Delta Ledger)

| Delta | 容器 | 改动 | **行为变更**(不是纯视觉) | 门 |
|---|---|---|---|---|
| **D6-4** | `#ai-events`(即 `.event-list`) | 原地删除 `max-height: 55vh;` 与 `overflow-y: auto;` | AI 面板**不再内部滚动**;条目随外层 `#main-pane` 滚动。滚到面板区底部时内容可达,但**不再有独立的 AI 面板滚动条** —— 用户滚动的是整个主区 | `check-05 --item 9`(滚动者普查 + 末条可达性) |
| **D6-5** | `#annotation-list` | 原地删除 `max-height: 32vh;` 与 `overflow-y: auto;` | 批注面板**不再内部滚动**;展开某条 `<details>` 后不再把后续条目挤出内部滚动区,条目随 `#main-pane` 滚动 | `check-05 --item 9` |

两条都是**交互行为变更**,不是纯视觉调整:改动前用户可在面板内部独立滚动,改动后滚动责任移交外层。`#latest-check` 的 30vh 内滚动**保留**(去掉它会把 `#check-controls` 的裁决按钮推出视口),故面板区内仍是「1 个外层 + 1 个保留的内层」,外加 SC#3 明文豁免的 `#chat-messages`。

### 块 2 —— 三宽度文档级溢出:波次 1 基线 vs 波次 2 之后

命令:`.venv/bin/python scripts/check-05-ui-uat.py --item 8`,取 `item8 L-2 文档级溢出基线` 行。诊断前已给 `#doc-panel-body` 注入含 12 列宽表格与 240 字符不可断 token 的 markdown(经应用自身的 `renderMarkdown`)。

| 宽度 | 波次 1 基线(`idi-06-01-SUMMARY.md` 块 2) | **波次 2 之后(Task 1 + Task 2 均已落地)** | 差 |
|---|---|---|---|
| 1440 | scrollWidth 1440 / clientWidth 1440 / overflow **0px** | scrollWidth 1440 / clientWidth 1440 / overflow **0px** | 0 |
| 1024 | scrollWidth 1024 / clientWidth 1024 / overflow **0px** | scrollWidth 1024 / clientWidth 1024 / overflow **0px** | 0 |
| 768 | scrollWidth 768 / clientWidth 768 / overflow **0px** | scrollWidth 768 / clientWidth 768 / overflow **0px** | 0 |

原始输出(波次 2 之后):

```
INFO item8 L-2 文档级溢出基线 @1440px(波次 1 基线,L-3 / L-4 尚未落地;面板内部横向滚动条不计入): scrollWidth=1440 clientWidth=1440 overflow=0px
INFO item8 L-2 文档级溢出基线 @1024px(波次 1 基线,L-3 / L-4 尚未落地;面板内部横向滚动条不计入): scrollWidth=1024 clientWidth=1024 overflow=0px
INFO item8 L-2 文档级溢出基线 @768px(波次 1 基线,L-3 / L-4 尚未落地;面板内部横向滚动条不计入): scrollWidth=768 clientWidth=768 overflow=0px
```

**判读(供计划 03):** 该读数在波次 1 就已经是 0px,波次 2 之后仍是 0px ⇒ **它无法区分「L-3 / L-4 修好了」与「本来就没破」**。计划 03 的 L-2 决策若要用它作判据,必须另找能区分两者的证据(例如在窄窗口下用不可断长 token 探针测 `#doc-panel` 的实际宽度是否被顶破 `clamp(340px, 30vw, 480px)` 的上界 —— 那正是 L-3 的 `min-width: 0` 直接作用的对象,而文档级 `scrollWidth` 因为 `#doc-panel` 自身 `overflow-y: auto` 会把 `overflow-x` 的 used value 一并算成 `auto`,永远看不到这个失效模式)。

### 块 3 —— `item9` 的逐条结论(原始输出)

命令:`.venv/bin/python scripts/check-05-ui-uat.py --item 9` → `exit=0`,`item 9: PASS (10 条断言,0 FAIL,0 BLOCKED)`。

```
PASS [p1] 面板区滚动者集合 == {#main-pane, #chat-messages, #latest-check}: expected=['#chat-messages', '#latest-check', '#main-pane'] actual=['#chat-messages', '#latest-check', '#main-pane']
PASS [p1] 排除 #chat-messages(SC#3 明文豁免)后 == {#main-pane, #latest-check}: expected=['#latest-check', '#main-pane'] actual=['#latest-check', '#main-pane']
PASS [p1] #ai-events 计算 max-height == none: expected=none actual=none
PASS [p1] #annotation-list 计算 max-height == none: expected=none actual=none
PASS [p1] #chat-messages overflow-y == auto: expected=auto actual=auto
PASS [static] frontend/style.css 的 max-height: 30vh 声明计数 == 1: expected=1 actual=1
PASS [p1] #main-pane 滚到底(scrollTop + clientHeight >= scrollHeight - 1): expected=>= 2639 actual=2640
PASS [p1] #main-pane 末条子元素落在容器可视区内: expected=container.top <= last.bottom <= container.bottom + 1 actual=last.bottom=900 container=[0, 900]
PASS [checking] #latest-check 滚到底(scrollTop + clientHeight >= scrollHeight - 1): expected=>= 4584 actual=4585
PASS [checking] #latest-check 末条子元素落在容器可视区内: expected=container.top <= last.bottom <= container.bottom + 1 actual=last.bottom=338.6875 container=[84, 354]
```

配套诊断行(同一命令):

```
INFO item9 [p1] 面板区滚动者普查(实测数组): 3 个:['#main-pane', '#chat-messages', '#latest-check']
INFO item9 [static] #latest-check 保留项护栏: frontend/style.css 里 'max-height: 30vh;' 计数=1 命中行=[1144]
INFO item9 [p1] #main-pane 末条内容可达 原始数值: scrollHeight=2640 clientHeight=900 scrollTop=1740 last=#ai-panel lastRect={'top': -1534, 'bottom': 900, 'width': 768, 'height': 2434} container={'top': 0, 'bottom': 900, 'width': 1008, 'height': 900}
INFO item9 [checking] #latest-check 末条内容可达 原始数值: scrollHeight=4585 clientHeight=268 scrollTop=4317 last=p lastRect={'top': 315.9375, 'bottom': 338.6875, 'width': 730, 'height': 22.75} container={'top': 84, 'bottom': 354, 'width': 748, 'height': 270}
```

**`#latest-check` 容器高 270.0 = 1440×900 视口下 30vh 的 px 用值** —— 这是保留项生效的直接几何证据,也印证了「不能用计算样式断言 `"30vh"`」的理由。

### 块 4 —— 既有门无回归(与执行前基线逐条对照)

| 门 | 执行前基线 | 波次 2 之后 |
|---|---|---|
| `bash scripts/check-01-token-conformance.sh` | `PASS` (exit 0) | `PASS` (exit 0) |
| `python3 scripts/check-02-contrast.py \| tail -1` | `PASS: 0 failures` | `PASS: 0 failures` |
| `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` (exit 0) | `PASS` (exit 0) |
| `bash scripts/check-04-important-count.sh` | `PASS` (exit 0) | `PASS` (exit 0) |
| `--item smoke,1,4,7,8` | 9 / 45 / 65 / 38 / 7,全 PASS | **9 / 45 / 65 / 38 / 7,全 PASS**(逐字相同) |
| `.venv/bin/python scripts/check-06-idi05-validation.py` | 全 PASS | **g1…g6 全 PASS**(9 / 2 / 12 / 5 / 5 / 7) |
| `.venv/bin/python -m pytest -q` | 219 passed / 6 skipped | **219 passed / 6 skipped** |
| `--item 9` | 不存在 | **PASS**(10 条断言,0 FAIL / 0 BLOCKED) |

零项被打破。断言条数与执行前基线逐字相同(D-20 的登记结论成立)。

## Self-Check: PASSED

- 创建/修改的文件存在:`frontend/style.css` FOUND,`scripts/check-05-ui-uat.py` FOUND
- 提交存在:`b623215` / `6adcaa3` / `1bd93a6` FOUND(`git log --oneline --all`)
- 计划级验收复跑:四条静态守卫 PASS / `check-02` = `PASS: 0 failures` / `--item 9` = PASS(10 条,0 FAIL / 0 BLOCKED)/ `--item smoke,1,4,7,8` = PASS(9 / 45 / 65 / 38 / 7,与基线逐字相同)/ `check-06` 全 PASS / `pytest` 219 passed 6 skipped
- 计划级 Gate A(围栏纯度):`git diff` 的 hunk 全部落在 `:459` 之后,围栏 `:5` … `:431` 内零改动 ✓
- 计划级 Gate B(硬规则 3):`.event-list` / `#annotation-list` 两个 hunk 为「加 3 行注释 + 删 2 行声明」,`#main-pane` / `#doc-panel` 为纯新增,末尾规则为纯新增 —— 无任何规则块位置变化 ✓
- 计划级 Gate C(保留项):`grep -o 'overflow-y: auto;' frontend/style.css | wc -l` == 4;`grep -o 'max-height: 30vh;' | wc -l` == 1 ✓
- 计划级 Gate D(零外溢):`git status --porcelain -- frontend/app.js frontend/index.html frontend/vendor/ scripts/ui-states/ scripts/check-01-token-conformance.sh scripts/check-02-contrast.py scripts/check-03-hidden-uniqueness.sh scripts/check-04-important-count.sh scripts/check-06-idi05-validation.py` 输出为空 ✓
- 计划级 Gate E(证据落盘):本文件含块 1(D6-4 / D6-5)、块 2(三宽度波次 1 vs 波次 2)、块 3(`item 9` 逐条结论)、块 4(既有门无回归) ✓
- 变异测试:把 `PANEL_SCROLLERS` 改为含 `#ai-events` 的四元组后,两条普查断言均 FAIL ⇒ 守卫非恒真 ✓
- `commits:` 为实测值(3),非叙述值:ledger `plan_head_before = 3f5e7293913a807f8e77c027bade9770e543ebf6`

---
*Phase: idi-06-layout-robustness*
*Completed: 2026-09-22*
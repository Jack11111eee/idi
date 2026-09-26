---
phase: idi-06-layout-robustness
plan: 01
subsystem: ui
tags: [css, layout, sticky, playwright, uat-harness, tracer, measurement-baseline]

# Dependency graph
requires:
  - phase: idi-04.1-radix
    provides: "四条静态守卫脚本(check-01…04)、check-02 的 47 对清单与 ORDER 断言、`--color-surface` 等已消费令牌"
  - phase: idi-05-typography-and-visual-hierarchy
    provides: "`scripts/check-05-ui-uat.py` 的 item7 新项骨架、`MARKDOWN_TARGETS` 枚举纪律、`getBoundingClientRect()` 的 `page.evaluate` 读数形状与「绝不记假 PASS」约定"
provides:
  - "`frontend/style.css` 围栏外新增的一条 `#doc-panel-header` 规则(position: sticky / top: 0 / background: var(--color-surface) / border-radius: 0)—— 全文件**首条** `position: sticky`,把「状态读数恒可见」补回 HEAD 引入的非自愿丢失"
  - "`scripts/check-05-ui-uat.py` 的 `item8`(L-1 三条断言 + 三项只读诊断)与三处派发接入;harness 里**第一次** viewport 变更(含 1440×900 复位)"
  - "波次 1 的原始测量数值:三宽度文档级 `scrollWidth` / `clientWidth`、L-5 clearance 普查表、L-6 命中区普查表 —— 计划 03 的 L-2 / L-5 / L-6 三个决策的唯一输入契约"
affects: ["idi-06-02(L-3 / L-4 落地)", "idi-06-03(L-2 / L-5 / L-6 决策与 A11Y-07)", "Phase 7(焦点环样式 —— 本计划的 4px clearance 判据是它的输入)"]

actuals:
  tokens: 5612      # chars/4 over the realized diff of the two changed files (22450 chars)
  tasks: 2
  commits: 1        # MEASURED: git rev-list --count 042e582..HEAD (Task 1 生产提交;Task 2 是证据任务,零 diff)
  plan_head_before: 042e5829c55e05d88770b9db520da32046ced06f

tech-stack:
  added: []
  patterns:
    - "「追加,不重排」(硬规则 3):新规则插在既有规则块之后,既有规则块零移动 —— 结构性 diff 阶段的风险控制"
    - "几何断言必带**前提检查**,前提不成立记 blocked() 而非 ok_true() —— 空转断言(假 PASS)是本阶段登记的高危威胁 T-idi-06-04"
    - "只读诊断经 info() 输出、不升为断言,使上游计划能在判据尚未成立时先产出可复核的原始数值"
    - "普查按**元素**枚举而非按容器名 —— 按点名枚举会漏掉没被点名的那个(Phase 5 G-idi-05-1 与本阶段 A11Y-07 的同构教训)"

key-files:
  created: []
  modified:
    - frontend/style.css
    - scripts/check-05-ui-uat.py

key-decisions:
  - "sticky 表头**自带背景** `var(--color-surface)`:`.panel-header` 规则体内没有任何 background 声明(已逐字核实 `style.css:509-518`),不加背景则滚动正文会从标题行底下穿过去。该令牌已被 `#doc-panel` 自身消费(`:474`)⇒ 零新增令牌,硬规则 5 / 8 同时满足"
  - "新规则**不加** `z-index`:sticky 元素是 positioned,默认画在静态内容之上;实测未出现正文穿透,故不新增 `--z-*` 消费者(若日后要补,须连带登记 badge 10 < banner 20 < overlay 100 < selection-menu 200 的序关系断言)"
  - "`border-radius: 0`(UI-SPEC 签核项 06-S-1):半径在本元素上是加背景之后才**首次可见**的新视觉物,10px 圆角会让滚动正文从四角露出;`0` 是无单位零,命中已登记例外 L-2,不新增例外行"
  - "viewport 复位放进 `finally`:这是 harness 里第一次 `set_viewport_size`,不复位会污染其后所有项(item 9 与任何依赖 1440 宽度的既有断言)。三宽度断言与三宽度诊断各一个 try/finally"
  - "三项诊断跑**两个样本**(p1 + p3 补渲染一条批注):被祖先藏住的元素 rect 全零,普查会失真 —— `#session-panel` 只在 p1 可见,`#annotations-panel` 只在 p3 可见,单样本无法同时覆盖两侧"
  - "item 8 只加 `8`、不加 `9`:item 9 是计划 02 的产出,现在加会在 `main()` 里引用一个不存在的函数"

patterns-established:
  - "Pattern 1: 上游计划用 info() 先产出原始数值、下游计划再把它升为断言 —— 使「判据尚未成立」不阻塞「证据先落盘」"
  - "Pattern 2: 普查脚本给每行带 `visible` 布尔,把「被祖先藏住(rect 全零)」与「真的不达标」分开,杜绝把隐藏元素读成命中区不足"
  - "Pattern 3: 几何断言前置 `display != none` + rect 宽高 > 0 的显式前提检查,不成立即 blocked()"

requirements-completed: [LAYOUT-01, LAYOUT-03]

coverage:
  - id: D1
    description: "文档面板标题行在滚动时钉在面板顶部(`#doc-panel-header` 获得 `position: sticky; top: 0`)—— 状态徽标与折叠指示符不再随正文滚走"
    requirement: "LAYOUT-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 8  # 「滚动到底后 #doc-panel-header 仍落在 #doc-panel 可视区内」与「sticky 把 #doc-panel-header 钉在 #doc-panel 顶部(<=1px)」两条断言"
        status: pass
      - kind: other
        ref: "grep -o 'position: sticky;' frontend/style.css | wc -l  # == 1"
        status: pass
    human_judgment: false
  - id: D2
    description: "`#state-badge` 的流内机制一字不动(仍无 `position`、无 `right`,仍是 `#doc-panel-header` 的子元素),`z-index: var(--z-badge)` 声明保留"
    requirement: "LAYOUT-03"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 8  # 「#state-badge position == static」与「#state-badge right 无声明」两条断言"
        status: pass
      - kind: other
        ref: "grep -n -A 8 '^#state-badge {' frontend/style.css | grep -oE '(position|right)[[:space:]]*:' | wc -l  # == 0;z-index 计数 == 1"
        status: pass
    human_judgment: false
  - id: D3
    description: "768 / 1024 / 1280 三处 `#state-badge` 与 `#stream-banner` 的 `getBoundingClientRect()` 不相交"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 8  # 三条「#state-badge 与 #stream-banner 不相交」断言,各带可见性/非零 rect 前提检查"
        status: pass
    human_judgment: false
  - id: D4
    description: "`scripts/check-05-ui-uat.py` 新增 `item8` 并接入三处派发(normalize_items 默认列表 / known 集合 / main() 派发),`--item 8` 可单跑"
    verification:
      - kind: e2e
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 8  # exit=0,item 8: PASS (7 条断言,0 FAIL,0 BLOCKED)"
        status: pass
    human_judgment: false
  - id: D5
    description: "三项只读诊断(三宽度文档级 scrollWidth / L-5 clearance 普查 / L-6 命中区普查)的原始数值落盘,成为计划 03 的输入契约"
    verification:
      - kind: other
        ref: "grep -c 'scrollWidth' / grep -c 'clearance' .planning/phases/idi-06-layout-robustness/idi-06-01-SUMMARY.md  # 原始输出逐行抄录"
        status: pass
    human_judgment: false
  - id: D6
    description: "L-6 命中区普查对 `.verdict-buttons button` 的覆盖"
    verification: []
    human_judgment: true
    rationale: "两个普查样本里 `#verdict-cards` 都是空的(裁决卡由 `renderVerdictCard` 在真实裁决轮次才注入),故 `.verdict-buttons button` 的实测盒高**本轮拿不到**。UI-SPEC 的静态预期是 26–30px(很可能已达标),但那是估算不是实测。计划 03 承担 A11Y-07 的落点,必须在它自己的样本里造出裁决卡再测,或显式接受该行的静态预期。"

# Metrics
duration: 12min
completed: 2026-09-22
status: complete
---

# Phase 6 Plan 01: 布局稳健性 — sticky 表头 tracer 切片 Summary

**文档面板标题行由 `position: sticky; top: 0` 钉在面板顶部(自带 `var(--color-surface)` 背景、零新增令牌),配 check-05 `item8` 的三条 L-1 运行时门(流内 badge / 三宽度几何不相交 / 滚到底后表头仍可见),并把三宽度溢出、L-5 clearance、L-6 命中区三项原始数值落盘为计划 03 的输入契约**

## Performance

- **Duration:** 12 min
- **Started:** 2026-09-22T03:16:08Z
- **Completed:** 2026-09-22T03:28:21Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- `frontend/style.css` 围栏外新增**恰好一条** `#doc-panel-header` 规则(4 条声明 + UI-SPEC §L-1 的逐字承重注释),插在既有 `#doc-panel.collapsed #doc-panel-header` 规则块**之后**;围栏 `:root` 内零改动、零新增令牌、零新文件、零新依赖。全文件 `position: sticky` 计数由 0 变为 1。
- `#state-badge` 的流内机制、折叠态三条规则、`.panel-header`、`#stream-banner.fatal` 四条规则族**逐字未变**(逐条 grep 计数核实)。
- `scripts/check-05-ui-uat.py` 新增 `item8`:L-1 三条断言各带**前提检查**(元素可见且 rect 非全零 / `#doc-panel` 真的可滚),前提不成立记 `blocked(...)` 而非 `ok_true(...)`;三处派发接入齐备,`--item 8` 可单跑并全绿(7 条断言,0 FAIL / 0 BLOCKED)。
- 三项只读诊断(经 `info()` 输出、不升为断言)在**两个样本**上跑通,原始数值逐行抄录于下方,成为计划 03 的 L-2 / L-5 / L-6 三个决策的唯一输入。
- 四条既有静态守卫与 `--item smoke,1,4,7` 全部仍绿,断言条数**与执行前基线逐字相同**(9 / 45 / 65 / 38)。

## Task Commits

Each task was committed atomically:

1. **Task 1 (tracer): sticky 表头端到端 —— 一条 CSS 规则 → 浏览器几何 → harness item 8 → 派发可单跑** - `9828dff` (feat)
2. **Task 2: 执行前基线复核 + 三项诊断原始数值的落盘(零代码改动)** - 零 diff:证据任务,产物即本节末尾的测量记录节,由承载本文件的 docs 提交落地

**Plan metadata:** `docs(idi-06-01): complete layout-robustness tracer plan`(承载本 SUMMARY、STATE.md、ROADMAP.md 与 REQUIREMENTS.md)

## Files Created/Modified

- `frontend/style.css` — 围栏外新增一条 `#doc-panel-header` 规则(`position: sticky` / `top: 0` / `background: var(--color-surface)` / `border-radius: 0`)+ 9 行承重注释;插在 `#doc-panel.collapsed #doc-panel-header`(`:487-490`)之后,新规则选择器在 `:500`。`git diff -U0` 的 hunk 只有一个:`@@ -491,0 +492,15 @@`,落在围栏(`:5` … `:431`)之外。
- `scripts/check-05-ui-uat.py` — 新增 `def item8(page, tmp_root)` 与三个模块级 JS 常量(`_IDI06_BADGE_BANNER_JS` / `_IDI06_SCROLL_JS` / `_IDI06_CENSUS_JS`)、`_rects_intersect()`、`_idi06_census()`、四个配置常量(`BADGE_BANNER_WIDTHS` / `VIEWPORT_RESTORE` / `BANNER_TEXT` / `LONG_DOC_MD` / `WIDE_MD`);`normalize_items` 默认列表、`known` 集合、`main()` 派发三处接入 `"8"`;模块 docstring 新增第 8 项说明并同步运行方式块;`--item` help 项清单加到 `8`。

## Decisions Made

- **sticky 表头自带背景是必需的,不是可选。** `.panel-header` 规则体内没有任何 `background` 声明(逐字核实 `style.css:509-518` 只有 `display` / `justify-content` / `align-items` / `height: 36px` / `padding` / `border-radius` / `cursor` / `user-select`),不加背景则面板正文会从标题行底下穿过去。`var(--color-surface)` 与 `#doc-panel` 自身背景同值且**已被消费**(`:474`)⇒ 零新增令牌(硬规则 5 / 8)。
- **新规则不加 `z-index`。** sticky 元素是 positioned,默认画在静态内容之上;实测滚动过程未出现正文穿透,故不新增 `--z-*` 消费者。若日后要补,须连带登记 badge 10 < banner 20 < overlay 100 < selection-menu 200 的序关系断言。
- **`border-radius: 0`**(UI-SPEC 签核项 06-S-1)。半径在本元素上是加背景之后才**首次可见**的新视觉物,10px 圆角会让滚动正文从四角露出;全宽条带没有卡片边缘需要圆角。`0` 是无单位零,命中已登记例外 L-2,不新增例外行。
- **viewport 复位放进 `finally`。** 这是 harness 里第一次 `set_viewport_size`(全文件此前只有 `new_context(viewport=…)` 一个设置点);不复位会污染其后所有项。三宽度断言与三宽度诊断各用一个 `try/finally` 包住。
- **三项诊断跑两个样本(p1 + p3 补渲染一条批注)。** 被祖先藏住的元素 `getBoundingClientRect()` 全零,普查会失真:`#session-panel` / `#chat-messages` 只在 p1 可见,`#annotations-panel` / `#annotation-list` 只在 p3 可见。单样本无法同时覆盖两侧,故普查在每行带 `visible` 布尔,把「被藏住」与「真的不达标」分开。
- **item 8 只加 `8`、不加 `9`。** item 9 是计划 02 的产出,现在加会在 `main()` 里引用一个不存在的函数(已由 `grep -c 'def item9'` == 0 与 `"9"` 计数 == 0 双向核实)。

## Deviations from Plan

**1. [Rule 2 - Missing Critical] L-5 / L-6 普查由单样本扩为双样本**

- **Found during:** Task 1(item 8 实现)
- **Issue:** 计划把 item 8 的样本定为 `p1`,并同时要求 L-5 普查覆盖 `#annotation-list` 的 `<summary>`(UI-SPEC 静态预期 clearance ≈ 13px)、L-6 普查覆盖 `.annotation-answer summary`。但 `p1` 下 `#annotations-panel` 带 `.hidden`(`app.js:362` 在阶段 1-2 显式 `annotationsPanel.classList.add('hidden')`),其所有后代的 `getBoundingClientRect()` 全零 —— 单样本普查会把「被祖先藏住」静默读成「clearance 0 / 命中区 0」,正是本阶段威胁表 T-idi-06-04(假 PASS)的同型失真。
- **Fix:** 普查循环改为 `for state, with_annotations in (("p1", False), ("p3", True))`;p3 分支经应用自身的 `renderAnnotations({items: [...]}, true)` 造出一条带 `<details>` 的批注(与 item7 同一手法,不手工拼 DOM)。每行输出都带 `visible` 布尔,隐藏行标 `visible=False` 且 `below24=None`(而不是 `True`)。
- **Files modified:** `scripts/check-05-ui-uat.py`
- **Verification:** p3 样本实测拿到 `summary × #annotation-list = 13.0px visible=True` 与 `summary w=722.0 h=17.0 visible=True below24=True` —— 与 UI-SPEC 的静态预期(13px / 14–17px)逐条吻合,证明该扩展是必要的(单样本拿不到这两行)。
- **Committed in:** `9828dff` (part of Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 missing critical)
**Impact on plan:** 该扩展是**证据完整性**所必需,不是范围蔓延 —— 它只增加 `info()` 诊断行,不增加任何断言、不改任何 CSS、不改样本的可断言面(`--item 8` 的 7 条断言仍全部跑在 p1 上)。若不扩展,计划 03 的 L-5 / L-6 两个决策将建立在「0px / 0×0」的假数值上。

## Issues Encountered

- **`.verdict-buttons button` 的实测盒高本轮拿不到。** `#verdict-cards` 在 p1 与 p3 两个样本里都是空的(裁决卡由 `renderVerdictCard` 在真实裁决轮次才注入)。UI-SPEC 的静态预期是 26–30px(很可能已达标),但那是估算不是实测。已登记为 coverage 条目 **D6**(`human_judgment: true`),由计划 03 在它自己的样本里造出裁决卡再测。
- **`#latest-check` 的 L-5 空动作结论未在两个样本中被实测证实。** `#checks-panel` 在 p1 / p3 下均隐藏,故普查表里没有 `× #latest-check` 的行。UI-SPEC 的静态预期是「无可聚焦后代(只渲染 markdown 元素)」,本轮**既未证实也未推翻**。计划 03 若需要该行的实测依据,应在 `checking` 样本上补一次普查。
- **p3 下 `#btn-authorize × #doc-panel = -122.6px` 是负值,但不是裁切缺陷。** 该元素的 rect 落在 `#doc-panel` 可视盒之外(`top=982.6 > panel.bottom=900`),即它被**滚动到视口外**、可达但当前不可见。普查的 clearance 公式度量的是「到最近裁剪祖先 padding 边的距离」,对滚出视口的元素会给出负值。计划 03 消费该表时应把 `visible=True` 且 clearance < 0 的行读作「需滚动才能到达」而非「被裁切」。

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- 波次 1 的交付物齐备:`#doc-panel-header` 的 sticky 规则已在磁盘上,`item8` 可单跑并全绿,四项既有守卫与 `--item smoke,1,4,7` 无回归。
- **计划 02 的输入**:三宽度文档级溢出基线在 1440 / 1024 / 768 三处均为 `overflow=0px`(见下方原始数值)。这是 L-3 / L-4 **尚未落地**时的读数,故「本来就没破」也是结论 —— 计划 03 的 L-2 决策必须用**波次 2 之后**的同一读数,不能直接引用本节的基线值。
- **计划 03 的输入**:L-5 clearance 普查表与 L-6 命中区普查表的原始数值见下节;两处覆盖缺口(`.verdict-buttons button` / `#latest-check`)已在上方 Issues Encountered 中显式登记。
- **无阻塞项。** 本计划零新增依赖、零新文件、零构建步骤,`frontend/app.js` / `index.html` / `vendor/` / `scripts/ui-states/` 零 diff。

---

## 测量决策记录

> 本节是计划 03(`idi-06-03`)的**唯一输入契约**。四块内容全部带原始命令与原始输出,**不给结论替代证据**。
> 采集时间:2026-09-22T03:26Z 前后;采集命令见各块首行;全部在 Task 1 的生产提交 `9828dff` 之上跑出。

### 块 1 —— 八条门的执行前基线复核(Task 2 第 1 步)

| # | 命令 | 原始输出 | 与 objective 基线表 |
|---|---|---|---|
| 1 | `bash scripts/check-01-token-conformance.sh` | `PASS`(exit 0) | 一致 |
| 2 | `python3 scripts/check-02-contrast.py \| tail -1` | `PASS: 0 failures` | 一致(47 对清单 + ORDER 未动) |
| 3 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS`(exit 0) | 一致(`^\.hidden {` == 1) |
| 4 | `bash scripts/check-04-important-count.sh` | `PASS`(exit 0) | 一致(`!important` 声明数 == 1) |
| 5 | `.venv/bin/python scripts/check-05-ui-uat.py --item smoke` | `item smoke: PASS  (9 条断言,0 FAIL,0 BLOCKED)` | 一致(基线 9) |
| 6 | `.venv/bin/python scripts/check-05-ui-uat.py --item 1` | `item 1: PASS  (45 条断言,0 FAIL,0 BLOCKED)` | 一致(基线 45) |
| 7 | `.venv/bin/python scripts/check-05-ui-uat.py --item 4` | `item 4: PASS  (65 条断言,0 FAIL,0 BLOCKED)` | 一致(基线 65) |
| 8 | `.venv/bin/python scripts/check-05-ui-uat.py --item 7` | `item 7: PASS  (38 条断言,0 FAIL,0 BLOCKED)` | 一致(基线 38) |

合并跑的原始尾块(命令:`.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,4,7,8`):

```
=== 逐项结论 ===
item smoke: PASS  (9 条断言,0 FAIL,0 BLOCKED)
item 1: PASS  (45 条断言,0 FAIL,0 BLOCKED)
item 4: PASS  (65 条断言,0 FAIL,0 BLOCKED)
item 7: PASS  (38 条断言,0 FAIL,0 BLOCKED)
item 8: PASS  (7 条断言,0 FAIL,0 BLOCKED)

exit=0  (0=全 pass,1=有 fail,2=有 blocked)
```

**结论:零项被打破。** 断言条数与 objective 的「执行前基线」表逐字相同,本计划未打破任何既有断言(D-20 的登记结论成立)。

### 块 2 —— 三宽度文档级溢出(L-2 的判据基线)

命令:`.venv/bin/python scripts/check-05-ui-uat.py --item 8`,取 `item8 L-2 文档级溢出基线` 行。诊断前已给 `#doc-panel-body` 注入一段含 12 列宽表格与 240 字符不可断 token 的 markdown(经应用自身的 `renderMarkdown`,真实渲染路径)。

```
INFO item8 L-2 文档级溢出基线 @1440px(波次 1 基线,L-3 / L-4 尚未落地;面板内部横向滚动条不计入): scrollWidth=1440 clientWidth=1440 overflow=0px
INFO item8 L-2 文档级溢出基线 @1024px(波次 1 基线,L-3 / L-4 尚未落地;面板内部横向滚动条不计入): scrollWidth=1024 clientWidth=1024 overflow=0px
INFO item8 L-2 文档级溢出基线 @768px(波次 1 基线,L-3 / L-4 尚未落地;面板内部横向滚动条不计入): scrollWidth=768 clientWidth=768 overflow=0px
```

| 宽度 | `document.documentElement.scrollWidth` | `document.documentElement.clientWidth` | 溢出 |
|---|---|---|---|
| 1440 | 1440 | 1440 | 0px |
| 1024 | 1024 | 1024 | 0px |
| 768 | 768 | 768 | 0px |

**明确标注:这是波次 1 的基线值(L-3 / L-4 尚未落地),不是 L-2 的最终判据。** L-2 的决策在计划 03 用**波次 2 之后**的同一读数做出。基线值的用途是让计划 03 能区分「L-3 / L-4 修好了」与「本来就没破」。三处基线均不溢出 ⇒ 即使波次 2 后仍为 0,也**不能**据此断定 L-3 / L-4 起了作用 —— 该判据在波次 1 就已经是绿的。

**为什么宽表格没有产生文档级溢出(供计划 03 判读):** `#doc-panel { overflow-y: auto }` 会把 `overflow-x` 的 used value 一并算成 `auto`,故宽内容在**面板内部**产生横向滚动条,不推高文档级 `scrollWidth`。这正是 UI-SPEC §L-2 明文「面板内部的横向滚动条不算破版、判据一律取文档级 `scrollWidth`」所指的现象。

### 块 3 —— L-5 clearance 普查(可聚焦元素 × 最近裁剪祖先 × 实测 clearance;阈值 4px)

命令同上,取 `item8 [<state>] L-5 clearance` 行。判据:一个裁剪容器(computed `overflow != visible`)必须让它的每一个可聚焦后代距离其 **padding 边**至少 **4px**(Phase 7 的 `outline: 2px solid` + `outline-offset: 2px` 的环外伸量)。

**p1 样本(17 对,`#session-panel` / `#chat-messages` / `#doc-panel` 可见):**

```
INFO item8 [p1] L-5 clearance: #message-input × #main-pane = 130.0px visible=True rect={'left': 130, 'top': 416.5, 'right': 808, 'bottom': 468.5, 'width': 678, 'height': 52}
INFO item8 [p1] L-5 clearance: #btn-send × #main-pane = 130.0px visible=True rect={'left': 816, 'top': 416.5, 'right': 878, 'bottom': 468.5, 'width': 62, 'height': 52}
INFO item8 [p1] L-5 clearance: #check-switcher × #main-pane = 0.0px visible=False rect={'left': 0, 'top': 0, 'right': 0, 'bottom': 0, 'width': 0, 'height': 0}
INFO item8 [p1] L-5 clearance: #btn-continue-check × #main-pane = 0.0px visible=False rect={'left': 0, 'top': 0, 'right': 0, 'bottom': 0, 'width': 0, 'height': 0}
INFO item8 [p1] L-5 clearance: #btn-continue-repair × #main-pane = 0.0px visible=False rect={'left': 0, 'top': 0, 'right': 0, 'bottom': 0, 'width': 0, 'height': 0}
INFO item8 [p1] L-5 clearance: #ai-route-select × #main-pane = 40.0px visible=True rect={'left': 130, 'top': 826, 'right': 282, 'bottom': 860, 'width': 152, 'height': 34}
INFO item8 [p1] L-5 clearance: #project-path-input × #main-pane = 40.0px visible=True rect={'left': 290, 'top': 826, 'right': 592, 'bottom': 860, 'width': 302, 'height': 34}
INFO item8 [p1] L-5 clearance: #btn-ping × #main-pane = 40.0px visible=True rect={'left': 600, 'top': 826, 'right': 706, 'bottom': 860, 'width': 106, 'height': 34}
INFO item8 [p1] L-5 clearance: #btn-process-round × #main-pane = 40.0px visible=True rect={'left': 714, 'top': 826, 'right': 820, 'bottom': 860, 'width': 106, 'height': 34}
INFO item8 [p1] L-5 clearance: #btn-abort × #main-pane = 40.0px visible=True rect={'left': 828, 'top': 826, 'right': 878, 'bottom': 860, 'width': 50, 'height': 34}
INFO item8 [p1] L-5 clearance: #enter-path-input × #doc-panel = 40.0px visible=True rect={'left': 1049, 'top': 68, 'right': 1342, 'bottom': 102, 'width': 293, 'height': 34}
INFO item8 [p1] L-5 clearance: #btn-enter × #doc-panel = 40.0px visible=True rect={'left': 1350, 'top': 68, 'right': 1400, 'bottom': 102, 'width': 50, 'height': 34}
INFO item8 [p1] L-5 clearance: #btn-divergence × #doc-panel = 40.0px visible=True rect={'left': 1049, 'top': 185.9375, 'right': 1267.34375, 'bottom': 223.9375, 'width': 218.34375, 'height': 38}
INFO item8 [p1] L-5 clearance: #btn-approve-draft × #doc-panel = 40.0px visible=True rect={'left': 1049, 'top': 373.9375, 'right': 1139, 'bottom': 411.9375, 'width': 90, 'height': 38}
INFO item8 [p1] L-5 clearance: #round-switcher × #doc-panel = -1009.0px visible=False rect={'left': 0, 'top': 0, 'right': 0, 'bottom': 0, 'width': 0, 'height': 0}
INFO item8 [p1] L-5 clearance: #btn-authorize × #doc-panel = -1009.0px visible=False rect={'left': 0, 'top': 0, 'right': 0, 'bottom': 0, 'width': 0, 'height': 0}
INFO item8 [p1] L-5 clearance: #btn-start-writing × #doc-panel = -1009.0px visible=False rect={'left': 0, 'top': 0, 'right': 0, 'bottom': 0, 'width': 0, 'height': 0}
```

**p3 样本(18 对,`#annotations-panel` / `#annotation-list` 可见;经应用自身的 `renderAnnotations` 造出一条带 `<details>` 的批注):**

```
INFO item8 [p3] L-5 clearance: #message-input × #main-pane = 0.0px visible=False rect={'left': 0, 'top': 0, 'right': 0, 'bottom': 0, 'width': 0, 'height': 0}
INFO item8 [p3] L-5 clearance: #btn-send × #main-pane = 0.0px visible=False rect={'left': 0, 'top': 0, 'right': 0, 'bottom': 0, 'width': 0, 'height': 0}
INFO item8 [p3] L-5 clearance: summary × #annotation-list = 13.0px visible=True rect={'left': 143, 'top': 109, 'right': 865, 'bottom': 126, 'width': 722, 'height': 17}
INFO item8 [p3] L-5 clearance: #check-switcher × #main-pane = 0.0px visible=False rect={'left': 0, 'top': 0, 'right': 0, 'bottom': 0, 'width': 0, 'height': 0}
INFO item8 [p3] L-5 clearance: #btn-continue-check × #main-pane = 0.0px visible=False rect={'left': 0, 'top': 0, 'right': 0, 'bottom': 0, 'width': 0, 'height': 0}
INFO item8 [p3] L-5 clearance: #btn-continue-repair × #main-pane = 0.0px visible=False rect={'left': 0, 'top': 0, 'right': 0, 'bottom': 0, 'width': 0, 'height': 0}
INFO item8 [p3] L-5 clearance: #ai-route-select × #main-pane = 130.0px visible=True rect={'left': 130, 'top': 254, 'right': 282, 'bottom': 288, 'width': 152, 'height': 34}
INFO item8 [p3] L-5 clearance: #project-path-input × #main-pane = 254.0px visible=True rect={'left': 290, 'top': 254, 'right': 592, 'bottom': 288, 'width': 302, 'height': 34}
INFO item8 [p3] L-5 clearance: #btn-ping × #main-pane = 254.0px visible=True rect={'left': 600, 'top': 254, 'right': 706, 'bottom': 288, 'width': 106, 'height': 34}
INFO item8 [p3] L-5 clearance: #btn-process-round × #main-pane = 188.0px visible=True rect={'left': 714, 'top': 254, 'right': 820, 'bottom': 288, 'width': 106, 'height': 34}
INFO item8 [p3] L-5 clearance: #btn-abort × #main-pane = 130.0px visible=True rect={'left': 828, 'top': 254, 'right': 878, 'bottom': 288, 'width': 50, 'height': 34}
INFO item8 [p3] L-5 clearance: #enter-path-input × #doc-panel = 40.0px visible=True rect={'left': 1049, 'top': 66, 'right': 1342, 'bottom': 100, 'width': 293, 'height': 34}
INFO item8 [p3] L-5 clearance: #btn-enter × #doc-panel = 40.0px visible=True rect={'left': 1350, 'top': 66, 'right': 1400, 'bottom': 100, 'width': 50, 'height': 34}
INFO item8 [p3] L-5 clearance: #btn-divergence × #doc-panel = -1009.0px visible=False rect={'left': 0, 'top': 0, 'right': 0, 'bottom': 0, 'width': 0, 'height': 0}
INFO item8 [p3] L-5 clearance: #btn-approve-draft × #doc-panel = -1009.0px visible=False rect={'left': 0, 'top': 0, 'right': 0, 'bottom': 0, 'width': 0, 'height': 0}
INFO item8 [p3] L-5 clearance: #round-switcher × #doc-panel = 110.8px visible=True rect={'left': 1119.796875, 'top': 144, 'right': 1275.796875, 'bottom': 172, 'width': 156, 'height': 28}
INFO item8 [p3] L-5 clearance: #btn-authorize × #doc-panel = -122.6px visible=True rect={'left': 1049, 'top': 982.640625, 'right': 1227, 'bottom': 1022.640625, 'width': 178, 'height': 40}
INFO item8 [p3] L-5 clearance: #btn-start-writing × #doc-panel = -1009.0px visible=False rect={'left': 0, 'top': 0, 'right': 0, 'bottom': 0, 'width': 0, 'height': 0}
```

**逐条「实测 vs 预期」(UI-SPEC §L-5 的静态分析预期表,必须由实测确认或推翻):**

| 裁剪容器 | UI-SPEC 预期 | 实测 | 判定 |
|---|---|---|---|
| `#annotation-list` | padding `var(--space-half)` = 2px;有可聚焦后代(`<summary>`);**无裁切**,clearance = 2px(列表)+ 1px(卡片 border)+ 10px(卡片 padding)= **13px** ≥ 4px | `summary × #annotation-list = 13.0px`(p3,`visible=True`,rect 宽 722 / 高 17) | **一致,逐位吻合**。预期未被推翻,该容器零 padding 改动 |
| `#chat-messages` | padding `4px 2px`;可聚焦后代**无**(气泡是 `div` / `p`);**空动作** | 两个样本的普查表里**没有任何** `× #chat-messages` 的行 ⇒ 实测遍历结果为空 | **一致**(空动作由实测遍历为空证实,不是照抄预期) |
| `#latest-check` | padding `6px 8px`;无(只渲染 markdown 元素);零改动 | **未测得**:`#checks-panel` 在 p1 / p3 下均隐藏,普查表无 `× #latest-check` 的行 | **既未证实也未推翻** —— 已登记为覆盖缺口(见 Issues Encountered),计划 03 若需要实测依据应在 `checking` 样本上补一次 |
| `#main-pane` | padding **0**;有可聚焦后代;**无裁切**,最浅祖先链含 `.panel-body { padding: 10px }`,故 ≥ 10px | 可见行最小值 **40.0px**(p1 的 `#ai-route-select` / `#project-path-input` / `#btn-ping` / `#btn-process-round` / `#btn-abort`);其余 130 / 188 / 254px | **一致(实测优于预期)**。预期未被推翻,该容器零 padding 改动 |
| `#doc-panel` | padding **0**;有可聚焦后代;**无裁切**,由 `#doc-panel-body { padding: 32px 40px }` 撑开 | 可见行 **40.0px**(两样本的 `#enter-path-input` / `#btn-enter`;p3 的 `#round-switcher` = 110.8px) | **一致**。预期未被推翻,该容器零 padding 改动 |

**需计划 03 特别判读的两行:**

- `#btn-authorize × #doc-panel = -122.6px`(p3,`visible=True`):负值来自该元素被**滚动到 `#doc-panel` 可视盒之外**(`top=982.6 > panel.bottom=900`),不是被裁切。clearance 公式度量的是「到最近裁剪祖先 padding 边的距离」,对滚出视口的元素会给出负值。应读作「需滚动才能到达」而非「被裁切」。
- 所有 `visible=False` 的行(p1 的 `#check-switcher` / `#btn-continue-*` / `#round-switcher` / `#btn-authorize` / `#btn-start-writing`;p3 的 `#message-input` / `#btn-send` / `#btn-divergence` / `#btn-approve-draft` / `#btn-start-writing`)其 rect 全零,clearance 是 `0.0px` 或 `-1009.0px` 的**噪声**,不得当作裁切证据。

**即:实测与静态分析一致 ⇒ 按 UI-SPEC §L-5 的决策规则,本阶段**不改任何 padding**,该交付物登记为「被实测推翻」,普查原始数据如上。**

### 块 4 —— L-6 命中区普查(可交互元素 rect;阈值 24×24)

命令同上,取 `item8 [<state>] L-6 命中区` 行。判据:每个可交互元素的计算盒 `getBoundingClientRect()` 的宽与高均 ≥ 24px(WCAG 2.5.8 Target Size Minimum,AA,按字面走尺寸不走间距例外)。

**p1 样本(28 个,含隐藏元素;`visible=True` 的完整清单):**

```
INFO item8 [p1] L-6 命中区: #message-input w=678.0 h=52.0 visible=True below24=False
INFO item8 [p1] L-6 命中区: #btn-send w=62.0 h=52.0 visible=True below24=False
INFO item8 [p1] L-6 命中区: #ai-route-select w=152.0 h=34.0 visible=True below24=False
INFO item8 [p1] L-6 命中区: #project-path-input w=302.0 h=34.0 visible=True below24=False
INFO item8 [p1] L-6 命中区: #btn-ping w=106.0 h=34.0 visible=True below24=False
INFO item8 [p1] L-6 命中区: #btn-process-round w=106.0 h=34.0 visible=True below24=False
INFO item8 [p1] L-6 命中区: #btn-abort w=50.0 h=34.0 visible=True below24=False
INFO item8 [p1] L-6 命中区: #enter-path-input w=293.0 h=34.0 visible=True below24=False
INFO item8 [p1] L-6 命中区: #btn-enter w=50.0 h=34.0 visible=True below24=False
INFO item8 [p1] L-6 命中区: #btn-divergence w=218.3 h=38.0 visible=True below24=False
INFO item8 [p1] L-6 命中区: #btn-approve-draft w=90.0 h=38.0 visible=True below24=False
```

**p3 样本(29 个,含隐藏元素;`visible=True` 的完整清单):**

```
INFO item8 [p3] L-6 命中区: summary w=722.0 h=17.0 visible=True below24=True
INFO item8 [p3] L-6 命中区: #ai-route-select w=152.0 h=34.0 visible=True below24=False
INFO item8 [p3] L-6 命中区: #project-path-input w=302.0 h=34.0 visible=True below24=False
INFO item8 [p3] L-6 命中区: #btn-ping w=106.0 h=34.0 visible=True below24=False
INFO item8 [p3] L-6 命中区: #btn-process-round w=106.0 h=34.0 visible=True below24=False
INFO item8 [p3] L-6 命中区: #btn-abort w=50.0 h=34.0 visible=True below24=False
INFO item8 [p3] L-6 命中区: #enter-path-input w=293.0 h=34.0 visible=True below24=False
INFO item8 [p3] L-6 命中区: #btn-enter w=50.0 h=34.0 visible=True below24=False
INFO item8 [p3] L-6 命中区: #round-switcher w=156.0 h=28.0 visible=True below24=False
INFO item8 [p3] L-6 命中区: #btn-authorize w=178.0 h=40.0 visible=True below24=False
```

**逐条「实测 vs 预期」(UI-SPEC §L-6 的普查表):**

| 控件 | UI-SPEC 预期 | 实测 | 判定 |
|---|---|---|---|
| 所有 `<button>` | ≈ 30–34px ✓ | **34px**(`#btn-enter` / `#btn-ping` / `#btn-process-round` / `#btn-abort`),`#btn-divergence` / `#btn-approve-draft` **38px** | **一致(实测达标)** |
| `#selection-menu button`(`#btn-annotate` / `#btn-plain-ask`) | ≈ 30px ✓ | 两样本均 `w=0.0 h=0.0 visible=False`(`#selection-menu` 隐藏) | **未测得** —— 计划 03 若需实测应在有划词选区的样本上补 |
| `.verdict-buttons button` | ≈ 26–30px,**待实测** | **未测得**:`#verdict-cards` 在两样本中均为空(裁决卡由 `renderVerdictCard` 在真实裁决轮次注入) | **未测得** —— 已登记为 coverage 条目 D6(`human_judgment: true`) |
| `.annotation-answer summary` | ≈ 14–17px,**✗ 确定不达标** | `summary w=722.0 h=17.0 visible=True below24=True`(p3) | **一致,确认不达标** |
| `.collapse-indicator` | `<span>`,属**不得触碰**;其可点父级 `.panel-header` 为 36px ✓ | 普查表里**没有** `.collapse-indicator` 行(它是 `<span>`,不进可交互选择器);`.panel-header` 高 36px(由 CSS 与 `#doc-panel-header` 的实测 rect 高 34px 佐证) | **一致**;`.collapse-indicator` **未**被列入待修清单 |
| `#round-switcher`(UI-SPEC 未点名) | —— | `w=156.0 h=28.0` ✓ | 达标,零改动 |
| `#btn-authorize`(UI-SPEC 未点名) | —— | `w=178.0 h=40.0` ✓ | 达标,零改动 |

**实测 < 24×24 的控件清单(计划 03 施加 `min-height` / `min-width` 的对象):**

| # | 控件 | 实测宽 × 高 | 样本 | 备注 |
|---|---|---|---|---|
| 1 | `.annotation-answer summary`(选择器标签显示为 `summary`) | **722.0 × 17.0** | p3 | **唯一一个实测不达标者**,与 UI-SPEC 的「确定不达标」逐条吻合。UI-SPEC §L-6 已锁定机制:原地加 `min-height: 24px; min-width: 24px;` 到 `.annotation-answer summary` 的既有规则体,不动现有四条声明 |

**未被本计划升为断言的控件(实测不足 24×24 但不在「可交互元素」判据内):** 无 —— 普查表里 `below24=True` 的行只有 `summary` 一条。所有 `below24=None` 的行都是 `visible=False`(元素被祖先藏住,rect 全零),**不是**不达标。

**普查口径的自我说明(供计划 03 核对):** 遍历在 `page.evaluate` 里做,可交互选择器为 `button, input, select, textarea, summary, a[href], [role=button], [onclick]`;`.collapse-indicator` 是 `<span>` 且无 `role` / `onclick`,故**不会**进入该集合(这正是 UI-SPEC §L-6 要求的「不得把它列进待修清单」在机制上的落实)。

### 块 5 —— L-1 三条门的原始几何数值(附,非计划 03 的输入但同批产出)

```
INFO item8 [768px] badge × banner 原始 rect: badge={'left': 638.96875, 'right': 739.890625, 'top': 7, 'bottom': 32, 'width': 100.921875, 'height': 25} display=inline | banner={'left': 285.34375, 'right': 482.65625, 'top': 12, 'bottom': 39, 'width': 197.3125, 'height': 27} display=block
INFO item8 [1024px] badge × banner 原始 rect: badge={'left': 894.96875, 'right': 995.890625, 'top': 7, 'bottom': 32, 'width': 100.921875, 'height': 25} display=inline | banner={'left': 413.34375, 'right': 610.65625, 'top': 12, 'bottom': 39, 'width': 197.3125, 'height': 27} display=block
INFO item8 [1280px] badge × banner 原始 rect: badge={'left': 1150.96875, 'right': 1251.890625, 'top': 7, 'bottom': 32, 'width': 100.921875, 'height': 25} display=inline | banner={'left': 541.34375, 'right': 738.65625, 'top': 12, 'bottom': 39, 'width': 197.3125, 'height': 27} display=block
INFO item8 sticky 原始数值: scrollTop=4348 scrollHeight=5248 clientHeight=900 header={'top': 0, 'bottom': 34, 'left': 1009, 'right': 1440} panel={'top': 0, 'bottom': 900, 'left': 1008, 'right': 1440}
```

- 三宽度下 badge 与 banner 在**垂直方向重叠**(badge `[7, 32]` vs banner `[12, 39]`)但在**水平方向分离**,故几何不相交成立 —— 门断言的是不相交,不是「横幅不存在」。
- 滚动到底(`scrollTop=4348`,容器确实可滚:`scrollHeight=5248 > clientHeight=900`)后,表头 `top=0` 与面板 `top=0` 的差为 **0.000px** —— sticky 把标题行钉在面板顶部。

## Self-Check: PASSED

- 创建/修改的文件存在:`frontend/style.css` FOUND,`scripts/check-05-ui-uat.py` FOUND
- 提交存在:`9828dff` FOUND(`git log --oneline --all`)
- 计划级验收复跑:四条静态守卫 PASS / `check-02` = `PASS: 0 failures` / `--item 8` = PASS(7 条,0 FAIL / 0 BLOCKED)/ `--item smoke,1,4,7` = PASS(9 / 45 / 65 / 38,与基线逐字相同)/ 全部 16 条 `<automated>` 与 18 条 `<acceptance_criteria>` 逐条核对通过
- `commits:` 为实测值(1),非叙述值:ledger `plan_head_before = 042e5829c55e05d88770b9db520da32046ced06f`

---
*Phase: idi-06-layout-robustness*
*Completed: 2026-09-22*
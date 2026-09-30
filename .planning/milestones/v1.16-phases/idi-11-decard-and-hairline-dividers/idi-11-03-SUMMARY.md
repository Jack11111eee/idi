---
phase: idi-11-decard-and-hairline-dividers
plan: 03
subsystem: test
tags: [playwright, computed-style, runtime-gate, mutation-testing, decard, hairline, check-09]

requires:
  - phase: idi-11-decard-and-hairline-dividers
    plan: 01
    provides: 反转本体已定型(连续面 + 统一面 + 灰缝归零 + 两条发丝线),本计划断言的就是它的渲染结果
  - phase: idi-11-decard-and-hairline-dividers
    plan: 02
    provides: 两个被孤立令牌已删净、围栏内点名它们的注释已改写 ⇒ 两条专用残留断言以「围栏内计数为 0」为前置
  - phase: idi-10-tables-and-radius-scale
    provides: 专用残留断言的先例(check-10 的 r1)与双断言的字面量半条形态(TH_BORDER_LITERAL)
provides:
  - check-09 的 c1..c4 改写为断言 Phase 11 的新契约(连续面 + 统一面 + 灰缝归零 + 两条发丝线)
  - fence_text() 与两条专用残留断言(围栏内子串计数、含注释)—— 明确不是 G2 的通用围栏消费断言
  - 交互控件对照组与活动标记的正面断言(使「移除边界」不可被过度执行)
  - 六条变异测试的真实「变异 → FAIL」读数 + 逐字节还原证据
affects: [idi-11-04, idi-12]

actuals:
  tokens: 11860
  tasks: 3
  commits: 1
plan_head_before: 0b05b0382d7ed6e8417e8327c957d250ede1323f

tech-stack:
  added: []
  patterns:
    - "门被反转时的正解是**改写判据**而不是删门:旧契约反转后必然全红,那正是门在正确工作的证据"
    - "令牌解析断言一律走 ok_true 并显式处理 None —— ok() 的 None-期望侧会降级成 BLOCKED(exit 2,本项目当良性码)"
    - "双断言:计算色 == 运行时令牌 == 写死字面量。只跟令牌比是**自指的**,换令牌会两侧一起变、恒过"
    - "专用残留断言(围栏内子串计数、含注释)≠ 通用围栏消费断言(G2,已排除)"

key-files:
  created: []
  modified:
    - scripts/check-09-idi09-validation.py

key-decisions:
  - "改写而非删除 check-09:它断言的正是本阶段移除的卡片语言,反转后必红是设计预期;判据只能改写,不得删除 / 降级为恒真 / 只断言「规则被写下了」"
  - "判据取真实浏览器 getComputedStyle 计算读数;令牌解析降为 info() 诊断(D-11-12)"
  - "c1 的边界宽度按**异形**形状断言,不写成一条统一循环:#session-panel 是 DOM 第一个 section,section + section 永不匹配它"
  - "c1 底色断言两侧都写死(body 计算底色 + rgb(255,255,255) 字面量),防止「令牌被改坏而消费者仍接线」时假绿"
  - "两条发丝线的颜色带双断言(令牌 + gray-6 字面量)—— 没有字面量半条,D-11-8 否决的 gray-7 备选对门是不可见的"
  - "c3 判据取令牌级读数而非 effective_bg:两级刻度里未被任何元素采用的那一档会被祖先链整个跳过,断言就在看不见的那一档上恒真"
  - "交互控件对照组第三列声明该控件是否承载 resting border:`.overlay-card` 从未声明过 border(计算 border-top-width 恒 0px),它的反向证据是圆角 + elevation,不是边框"
  - "`fence_text()` 逐字照抄 check-10;两条残留断言是**专用**的,注释里显式写明「这不是通用围栏消费断言 —— 通用断言属 G2,不在 v1.16 范围」"
  - "删掉 shadow_lengths() / 三个卡片字面量常量后,import re 随之成为孤儿 import,一并删除(CLAUDE.md 第 3 条)"
  - "变异 1 用**字面量**阴影而不是 var(--shadow-card):后者在波次 2 已被删除,computed-value 阶段失效解析成 none —— 恰好等于断言值,是条空转的变异"

patterns-established:
  - "一条不能失败的门比没有门更糟:门改写后必须用变异测试逐条证明它会失败,只跑一次真实树无法区分「守卫在工作」与「守卫静默空转」"
  - "变异测试的还原判据是两道独立证据:git diff --exit-code 为空 **且** git hash-object 与变异前记录值逐字符相同,不靠记忆"

requirements-completed: [REG-01]

coverage:
  - id: D1
    description: "check-09 的 c1..c4 已改写为断言新契约(连续面 + 统一面 + 灰缝归零 + 两条发丝线),零条断言被删除、零条降级为恒真;断言总数由 HEAD 的 46 升到 102(>= 46 的机器判据)"
    requirement: "REG-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4 → exit=0;c1 PASS (59) / c2 PASS (17) / c3 PASS (6) / c4 PASS (20),0 FAIL,0 BLOCKED"
        status: pass
    human_judgment: false
  - id: D2
    description: "改写后的四条判据**逐条被证明会真的失败**:六条变异各给出至少一行 FAIL 的完整原文(含 expected= / actual=),每条触发的判据就是计划表中指定的那一项"
    requirement: "REG-01"
    verification:
      - kind: automated_ui
        ref: "六条变异逐条实跑(m1 c1: 4 FAIL / m2 c2: 3 FAIL / m3 c2: 1 FAIL / m4 c3: 2 FAIL / m5 c4: 1 FAIL / m6 c4: 9 FAIL),每条 exit=1"
        status: pass
    human_judgment: false
  - id: D3
    description: "六条变异全部在**已提交的树**上做,定向 git checkout -- frontend/style.css 还原;还原后 git diff --exit-code 为空且 git hash-object 逐字符相同(cfcaef098d957abc885413793cd8b1a9dc12193f,六次一致);全程未使用 git stash"
    requirement: "REG-01"
    verification:
      - kind: other
        ref: "六次还原后 `git diff --exit-code -- frontend/style.css` rc=0 且 `git hash-object` = cfcaef09…;`git status --porcelain frontend/` 为空"
        status: pass
    human_judgment: false
  - id: D4
    description: "c5 的滚动契约原样保留并仍 PASS(5 条断言,与 HEAD 基线一致);ITEMS / parse_args() / main() / --screenshot 路径逐字未动;scripts/ 下其它文件与 frontend/style.css 本计划零改动"
    requirement: "REG-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c5 → exit=0,item c5: PASS (5 条断言,0 FAIL,0 BLOCKED)"
        status: pass
      - kind: other
        ref: "git diff --name-only 0b05b03..HEAD → 仅 scripts/check-09-idi09-validation.py;git diff --stat 0b05b03..HEAD -- frontend/app.js frontend/index.html backend/ frontend/vendor/ → 空"
        status: pass
    human_judgment: false
  - id: D5
    description: "两条专用残留断言(围栏内子串计数、含注释)就位,且**不是**通用的围栏消费断言(G2 未纳入 v1.16)"
    requirement: "REG-01"
    verification:
      - kind: other
        ref: "PASS c1 [源码] 围栏内 --color-surface-card 残留计数 == 0(含注释): actual=0 / PASS c1 [源码] 围栏内 --shadow-card 残留计数 == 0(含注释): actual=0;两条「被删令牌已不可解析」探测器 actual=None"
        status: pass
    human_judgment: true
    rationale: "「这是专用而非通用」是注释里的边界声明,须人眼确认它没有被扩写成通用形态;机器判据只能证明这两条专用断言存在且为真。"

duration: 30min
completed: 2026-09-28
status: complete
---

# Phase 11 Plan 03: check-09 判据改写与六条变异证明 Summary

**把 Phase 9 自建的运行时门 `check-09` 的 `c1..c4` 从「断言卡片语言」改写为「断言连续面 + 统一面 + 灰缝归零 + 两条发丝线」,并用六条变异测试逐条证明改写后的判据**真的会失败** —— 全部改动集中在 `scripts/check-09-idi09-validation.py` 一个文件。**

## Performance

- **Duration:** ~30 min
- **Completed:** 2026-09-28
- **Tasks:** 3
- **Files modified:** 1 (`scripts/check-09-idi09-validation.py`)

> **过程偏差(已登记):** 计划要求在执行开始时记下 `PLAN_START_TIME`。本次**未落盘**该时间戳,故 `duration` 是由首个证据文件的 mtime 反推的近似值(约 30 min),不是精确读数。

## Accomplishments

- **门被改写而不是被删除。** 文件头 docstring 改写为 Phase 11 语境,并写下「本文件在 Phase 11 被**改写**而非删除 —— 它断言的旧契约反转后必然全红,那正是门在正确工作的证据」。Phase 9 的「为什么另开一个文件」论证(五条既有门的盲区)**逐字保留**;退出码语义与浏览器路线两段也逐字保留。
- **`c1` 改写为连续面 + 对照组 + 残留断言 + 探测器。** 两条**专用**残留断言(`fenced.count(<令牌名>) == 0`,子串计数、**含注释**;依据围栏抬头 + Hard Rule 5 / D-04;先例是 Phase 10 删圆角档位时的 `check-10` `r1`)+ 两条「被删令牌已不可解析」探测器(`resolve_token(...) is None`,走 `ok_true`)+ 四个 section 的 `box-shadow == none` / 四角长手 `0px` / 底色双断言 / **异形**边界宽度 + 交互控件对照组 + 活动标记的正面断言。
- **`c2` 改写为单边竖线 + sticky 表头。** `#doc-panel` 的 `box-shadow == none`、四角 `0px`、四条边中**仅** `border-left-width == 1px`、`border-left-style == solid`、`border-left-color` **双断言**、`overflow-y == auto`(承重的滚动契约,理由**只**写 L-1);`#doc-panel-header` 的 `position == sticky` / `top == 0px` / 背景非透明 **且** == 统一面计算底色。
- **`c3` 由三级刻度改写为两级。** `body` 计算底色 == 统一面令牌解析值 **且** == 写死字面量白 **且** != 旧的 `rgb(240, 240, 240)`;内陷面令牌解析值 == `rgb(249, 249, 249)` **且**其相对亮度**严格低于**统一面。判据是**令牌级**读数,不是 `effective_bg`。
- **`c4` 覆盖灰缝归零 + 两条发丝线 + 竖线跨满几何。** `#main-pane` 计算 `gap == 0px`;竖线与三条横线的宽度 `1px` 与颜色**双断言**(令牌 + gray-6 字面量);`#session-panel` 的 `border-top-width == 0px`;`#doc-panel` 的 `getBoundingClientRect()` 实测 `{top:0, bottom:900, height:900}` 对上视口高 900;三条对照组(`.panel-body` `16px` / `#doc-panel-body` `32px 40px` / `.panel-header` `padding-top` `6px`)在位。
- **断言总数由 46 升到 102**(c1 59 + c2 17 + c3 6 + c4 20),远超计划要求的 `>= 46` —— **零条断言被删除、零条降级为恒真**。
- **六条变异逐条给出真实 FAIL 读数,并逐字节还原。** 六次 `git hash-object frontend/style.css` 全部等于变异前的 `cfcaef098d957abc885413793cd8b1a9dc12193f`,`git diff --exit-code` 六次 rc=0。**全程未使用 `git stash`。**
- **`c5` 原样保留并仍 PASS**(5 条断言,与 HEAD 基线一致)。`ITEMS` / `parse_args()` / `main()` / `--screenshot` 路径逐字未动。
- **零范围外改动。** `git diff --name-only 0b05b03..HEAD` 仅 `scripts/check-09-idi09-validation.py`;`frontend/style.css` / `frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**` / `scripts/` 下其它门与探针**逐字节未改**。

## Task Commits

| Task | 内容 | 提交 |
|---|---|---|
| Task 1 | 改写 `c1` / `c2`(连续面 + 单边竖线 + 对照组 + 残留断言 + 探测器) | `315af14` (feat) |
| Task 2 | 改写 `c3` / `c4`(两级刻度 + 灰缝 + 两条发丝线 + 竖线跨满几何) | **无独立提交** —— 见「Deviations」第 3 条 |
| Task 3 | 六条变异测试(净 diff 为零,纯取证) | **无独立提交**(沿 `idi-11-02` Task 3 先例) |

**Plan metadata:** 见收尾的 docs 提交。

## Files Created/Modified

- `scripts/check-09-idi09-validation.py` — 唯一改动文件。406 insertions / 176 deletions。
  - **删除的既有符号**(全文件零引用已复核):`SHADOW_CARD_LITERAL` / `SHADOW_CARD_COLOR` / `CARD_WHITE` / `_SHADOW_COLOR_RE` / `shadow_lengths()` / `GRAY3_BODY` / `TIER_TOKENS`,以及随 `_SHADOW_COLOR_RE` 一并成为孤儿的 `import re`。
  - **新增的模块级符号**:`STYLE_CSS` / `FENCE_START` / `FENCE_END` / `fence_text()`(逐字照抄 `check-10`)/ `SURFACE_PAGE_LITERAL` / `SURFACE_SUNKEN_LITERAL` / `HAIRLINE_LITERAL` / `RETIRED_CARD_TOKENS` / `CONTROL_GROUP` / `HAIRLINE_SECTIONS` / `RADIUS_CORNER_PROPS` / `BORDER_SIDES`。
  - **未改动**:`ITEMS`(仍是 `c1..c5`)/ `parse_args()` / `main()` / `run_screenshots()` / `png_size()` / `load_check05()` / `c5()` 与其 `_C5_SCROLL_JS`。

## `=== 逐项结论 ===` 原文(最终树,逐字抄录)

```
=== 逐项结论 ===
item c1: PASS  (59 条断言,0 FAIL,0 BLOCKED)
item c2: PASS  (17 条断言,0 FAIL,0 BLOCKED)
item c3: PASS  (6 条断言,0 FAIL,0 BLOCKED)
item c4: PASS  (20 条断言,0 FAIL,0 BLOCKED)

exit=0  (0=全 pass,1=有 fail,2=有 blocked)
```

```
=== 逐项结论 ===
item c5: PASS  (5 条断言,0 FAIL,0 BLOCKED)

exit=0  (0=全 pass,1=有 fail,2=有 blocked)
```

**改写前后的断言计数对照(计划要求的机器判据是 `>= 46`):**

| 项 | HEAD(旧契约,红) | 改写后(新契约,绿) |
|---|---|---|
| c1 | 26(14 FAIL / 6 BLOCKED) | **59**(0 / 0) |
| c2 | 13(8 FAIL / 1 BLOCKED) | **17**(0 / 0) |
| c3 | 3(1 FAIL / 1 BLOCKED) | **6**(0 / 0) |
| c4 | 4(1 FAIL / 0) | **20**(0 / 0) |
| **合计** | **46** | **102** |

## 两条专用残留断言与两条探测器的原始读数(逐字抄录)

```
PASS c1 [源码] 围栏内 --color-surface-card 残留计数 == 0(含注释): expected=== 0 actual=0  # 读 DESIGN TOKENS 围栏内的**全文含注释**(子串计数):只删声明行不够,点名它的注释也会让计数非零(D-04 / Hard Rule 5;Phase 10 的 --radius-lg 先例)。这不是通用围栏消费断言 —— 通用断言属 G2,不在 v1.16 范围
PASS c1 [源码] 围栏内 --shadow-card 残留计数 == 0(含注释): expected=== 0 actual=0  # (同上)
PASS c1 [令牌] 被删令牌 --color-surface-card 已不可解析(解析值 None): expected=None actual=None  # 被删令牌的探测器:它若还能解析出值,说明删漏了或消费者没搬完。令牌未声明按 FAIL 计,不得降级为 BLOCKED
PASS c1 [令牌] 被删令牌 --shadow-card 已不可解析(解析值 None): expected=None actual=None  # (同上)
```

**这不是 G2。** G2 是「补一条**通用的**围栏消费断言(每个声明的令牌都被消费)+ 处置零消费的 `--radix-gray-1`」,用户 2026-09-28 只裁定「连带 G1」,**G2 未点名**,已明确排除在 v1.16 范围外。本阶段只处置**本次反转自己孤立掉**的两个令牌,每个令牌一条专用断言 —— 照 Phase 10 删 28px 圆角档位时给它加专用残留断言的先例。这条边界同时写进了 `c1` 的注释(见上,`# 这不是通用围栏消费断言 …`)。

## 六条变异测试 —— 逐条「变异 → FAIL」真实读数

> **前置条件(第 1 步,逐条记录):**
> - `git status --porcelain frontend/` **干净**(波次 1/2 的改动已提交)⇒ 变异确实做在**已提交的树**上
> - `git rev-parse HEAD` = `315af14e53b58ee7ca8ccda3bc68620edef1dfe0`
> - `git hash-object frontend/style.css` = `cfcaef098d957abc885413793cd8b1a9dc12193f`
> - 基线 `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4` → `exit=0`
>
> **⚠ 全程未使用 `git stash`**(它跨工作树共享,本项目明令禁止)。还原一律 `git checkout -- frontend/style.css`。

### 变异 1 — 给 `#main-pane > section` 加回一条**字面量**阴影 → `c1` 必红

- **注入:** `#main-pane > section` 的 `box-shadow: none;` → `box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);`
- **观察(FAIL 原文,4 条,含 `expected=` / `actual=`):**

```
FAIL [p1] #session-panel 计算 box-shadow == none(不绘制阴影): expected=none actual=rgba(0, 0, 0, 0.08) 0px 1px 3px 0px  # Phase 9 的卡片阴影随去卡片化整段作废
FAIL [p1] #annotations-panel 计算 box-shadow == none(不绘制阴影): expected=none actual=rgba(0, 0, 0, 0.08) 0px 1px 3px 0px  # Phase 9 的卡片阴影随去卡片化整段作废
FAIL [p1] #checks-panel 计算 box-shadow == none(不绘制阴影): expected=none actual=rgba(0, 0, 0, 0.08) 0px 1px 3px 0px  # Phase 9 的卡片阴影随去卡片化整段作废
FAIL [p1] #ai-panel 计算 box-shadow == none(不绘制阴影): expected=none actual=rgba(0, 0, 0, 0.08) 0px 1px 3px 0px  # Phase 9 的卡片阴影随去卡片化整段作废
item c1: FAIL  (59 条断言,4 FAIL,0 BLOCKED)
exit=1  (0=全 pass,1=有 fail,2=有 blocked)
```

- **还原:** `git checkout -- frontend/style.css` → `git diff --exit-code -- frontend/style.css` **rc=0**;`git hash-object` = `cfcaef098d957abc885413793cd8b1a9dc12193f`(逐字符相同)

> **为什么用字面量阴影而不是 `var(--shadow-card)`:** 波次 2 已从围栏里删掉 `--shadow-card` 声明,而本计划 `depends_on: [idi-11-01, idi-11-02]`。到波次 3 该令牌已不存在 ⇒ `box-shadow: var(--shadow-card)` 在 computed-value 阶段失效(IACVT)、解析成初始值 `none` —— **恰好等于 `c1` 断言的那个值** ⇒ 那条路线**不会变红**,是条空转的变异。加回一条**字面量**阴影才是真实回归的忠实模拟。

### 变异 2 — 给 `#doc-panel` 加回四边边界 → `c2` 必红

- **注入:** `#doc-panel` 的 `border-left: 1px solid var(--color-border-subtle);` → `border: 1px solid var(--color-border-subtle);`
- **观察(FAIL 原文,3 条):**

```
FAIL [p1] #doc-panel 计算 border-top-width == 0px(单边,非四边): expected=0px actual=1px  # 四边边界收成单边竖线(D-11-9);残留的顶侧边框会顶破 check-05 --item 8 的 sticky 容差
FAIL [p1] #doc-panel 计算 border-right-width == 0px(单边,非四边): expected=0px actual=1px  # (同上)
FAIL [p1] #doc-panel 计算 border-bottom-width == 0px(单边,非四边): expected=0px actual=1px  # (同上)
item c2: FAIL  (17 条断言,3 FAIL,0 BLOCKED)
exit=1  (0=全 pass,1=有 fail,2=有 blocked)
```

- **还原:** `git diff --exit-code` rc=0;`git hash-object` = `cfcaef098d957abc885413793cd8b1a9dc12193f`

### 变异 3 — 删掉 `#doc-panel` 的 `overflow-y: auto;` → `c2` 必红

- **注入:** 删除 `#doc-panel` 规则体内的 `overflow-y: auto;` 一行(仅此一行)
- **观察(FAIL 原文,1 条):**

```
FAIL [p1] #doc-panel 计算 overflow-y == auto(承重的滚动契约): expected=auto actual=visible  # L-1 的 sticky 表头依赖 #doc-panel 仍是最近的可滚祖先
item c2: FAIL  (17 条断言,1 FAIL,0 BLOCKED)
exit=1  (0=全 pass,1=有 fail,2=有 blocked)
```

- **还原:** `git diff --exit-code` rc=0;`git hash-object` = `cfcaef098d957abc885413793cd8b1a9dc12193f`
- **过程留档:** 本条的第一次注入把 new_string 误写成 `border: 1px solid …`,**同时**施加了变异 2 的改动(两个变异叠在一起)。发现后立刻 `git checkout -- frontend/style.css` 还原,并按最小改动重做 —— 上表读数取自**只删一行**的干净注入。

### 变异 4 — 把统一面改回 `var(--color-surface)`,使两档塌成一档 → `c3` 必红

- **注入:** 围栏内 `--color-surface-page: var(--white);` → `--color-surface-page: var(--color-surface);`
- **观察(FAIL 原文,2 条 + 三条值 INFO):**

```
INFO c3 body 计算 background-color 原始读数: rgb(249, 249, 249)
INFO c3 统一面 --color-surface-page 解析值: rgb(249, 249, 249)
INFO c3 内陷面 --color-surface 解析值: rgb(249, 249, 249)
FAIL [p1] body 计算底色 == rgb(255, 255, 255)(统一面写死字面量): expected=rgb(255, 255, 255) actual=rgb(249, 249, 249)  # 与上一条互补:两侧都写死,防止「令牌被改坏而消费者仍接线」时假绿
INFO c3 统一面相对亮度: 0.947307
INFO c3 内陷面相对亮度: 0.947307
INFO c3 统一面 vs 内陷面 对比度比值(只读诊断,不判定): 1.0000
FAIL [p1] 内陷面相对亮度严格低于统一面(两级刻度未塌成一档): expected=lum(内陷面) < lum(统一面) actual=内陷面=0.947307 统一面=0.947307  # 严格小于(不是 <=):两档若相等,内陷面这一档就没有画出来
item c3: FAIL  (6 条断言,2 FAIL,0 BLOCKED)
exit=1  (0=全 pass,1=有 fail,2=有 blocked)
```

- **还原:** `git diff --exit-code` rc=0;`git hash-object` = `cfcaef098d957abc885413793cd8b1a9dc12193f`

### 变异 5 — 把 `gap` 改回 `var(--space-3)` → `c4` 必红

- **注入:** `#main-pane` 的 `gap: 0;` → `gap: var(--space-3);`
- **观察(FAIL 原文,1 条):**

```
FAIL [p1] #main-pane 计算 gap == 0px(灰缝归零): expected=0px actual=12px  # Phase 9 把间隙当作卡片层次的载体(间隙里透出页面底色);Phase 11 里面板与页面同色,间隙不再承载任何东西,分区改由发丝线承担(SURF-03)
item c4: FAIL  (20 条断言,1 FAIL,0 BLOCKED)
exit=1  (0=全 pass,1=有 fail,2=有 blocked)
```

- **还原:** `git diff --exit-code` rc=0;`git hash-object` = `cfcaef098d957abc885413793cd8b1a9dc12193f`

### 变异 6 — 删掉 `#main-pane > section + section { border-top: … }` 整条规则块 → `c4` 必红

- **注入:** 删除整行 `#main-pane > section + section { border-top: 1px solid var(--color-border-subtle); }`
- **观察(FAIL 原文,9 条 —— 3 个 section × {宽度, 令牌色, 字面量色}):**

```
FAIL [p1] 横线 #annotations-panel 计算 border-top-width == 1px: expected=1px actual=0px
FAIL [p1] 横线 #annotations-panel 计算 border-top-color == var(--color-border-subtle): expected=rgb(217, 217, 217) actual=rgb(32, 32, 32)
FAIL [p1] 横线 #annotations-panel 计算 border-top-color == gray-6 字面量: expected=rgb(217, 217, 217) actual=rgb(32, 32, 32)  # 字面量半条是承重的:使 D-11-8 否决的 gray-7 备选对本门可见
FAIL [p1] 横线 #checks-panel 计算 border-top-width == 1px: expected=1px actual=0px
FAIL [p1] 横线 #checks-panel 计算 border-top-color == var(--color-border-subtle): expected=rgb(217, 217, 217) actual=rgb(32, 32, 32)
FAIL [p1] 横线 #checks-panel 计算 border-top-color == gray-6 字面量: expected=rgb(217, 217, 217) actual=rgb(32, 32, 32)  # 字面量半条是承重的:使 D-11-8 否决的 gray-7 备选对本门可见
FAIL [p1] 横线 #ai-panel 计算 border-top-width == 1px: expected=1px actual=0px
FAIL [p1] 横线 #ai-panel 计算 border-top-color == var(--color-border-subtle): expected=rgb(217, 217, 217) actual=rgb(32, 32, 32)
FAIL [p1] 横线 #ai-panel 计算 border-top-color == gray-6 字面量: expected=rgb(217, 217, 217) actual=rgb(32, 32, 32)  # 字面量半条是承重的:使 D-11-8 否决的 gray-7 备选对本门可见
item c4: FAIL  (20 条断言,9 FAIL,0 BLOCKED)
exit=1  (0=全 pass,1=有 fail,2=有 blocked)
```

- **还原:** `git diff --exit-code` rc=0;`git hash-object` = `cfcaef098d957abc885413793cd8b1a9dc12193f`

### 六条变异汇总

| # | 变异(最小改动) | 必须变红的判据 | 实测结果 | 还原后 hash |
|---|---|---|---|---|
| 1 | `#main-pane > section` 加回字面量阴影 | `c1` 的 `box-shadow == none` | `c1` **FAIL**(4 FAIL / 0 BLOCKED) | `cfcaef09…` ✓ |
| 2 | `#doc-panel` 加回四边边界 | `c2` 的「仅 `border-left-width == 1px`」 | `c2` **FAIL**(3 / 0) | `cfcaef09…` ✓ |
| 3 | 删 `#doc-panel` 的 `overflow-y: auto` | `c2` 的 `overflow-y == auto` | `c2` **FAIL**(1 / 0) | `cfcaef09…` ✓ |
| 4 | 统一面改回 `var(--color-surface)` | `c3` 的两级刻度未塌 | `c3` **FAIL**(2 / 0) | `cfcaef09…` ✓ |
| 5 | `gap` 改回 `var(--space-3)` | `c4` 的 `gap == 0px` | `c4` **FAIL**(1 / 0) | `cfcaef09…` ✓ |
| 6 | 删掉横线规则块 | `c4` 的横线宽度/颜色 | `c4` **FAIL**(9 / 0) | `cfcaef09…` ✓ |

**六条全部按设计变红,没有一条是「变异没生效」或「判据在空转」。** 每条触发的判据就是计划表中指定的那一项,故没有改判据去迁就的余地。

## 收口时的树状态(逐条实测)

| 判据 | 实测 |
|---|---|
| `git status --porcelain frontend/` | **空**(六条变异全部还原) |
| `git diff --exit-code -- frontend/style.css` | **rc=0**(逐字节相同) |
| `git hash-object frontend/style.css` | `cfcaef098d957abc885413793cd8b1a9dc12193f`(与变异前记录值逐字符相同) |
| `git status --porcelain scripts/ui-states/` | **空** |
| `git diff --name-only 0b05b03..HEAD` | **仅 `scripts/check-09-idi09-validation.py`** |
| `git diff --stat 0b05b03..HEAD -- frontend/app.js frontend/index.html backend/ frontend/vendor/` | **空** |
| `git diff --stat -- scripts/check-05-ui-uat.py scripts/check-02-contrast.py scripts/check-10-idi10-validation.py` | **空** |
| `ls frontend/vendor/` | 仅 `marked.min.js` |
| `ITEMS` / `parse_args()` / `main()` / `--screenshot` | `git diff` 里**零 +/- 行**触及它们 |
| 最终 `--item c1,c2,c3,c4` / `--item c5` | 均 `exit=0`、0 FAIL、0 BLOCKED |

## Decisions Made

- **门改写而非删除**:`check-09` 断言的正是本阶段移除的卡片语言,反转后 `c1..c4` 必然全红是**设计预期**。判据只能改写,不得删除 / 降级为恒真 / 只断言「规则被写下了」。
- **令牌解析断言一律走 `ok_true` 并显式处理 `None`**:`ok()` 在期望侧为 `None` 时降级成 `BLOCKED`(exit 2,本项目当良性码),文案还指向 DOM。令牌一旦被删,旧式「断言解析值」不会变红,而是静默变成「良性阻塞」。`c1` / `c2` / `c3` 里每一处令牌解析断言都按此改写。
- **`c1` 的边界宽度按异形形状断言**,不写成一条统一循环:`#session-panel` 是 DOM 第一个 `section`,`section + section` 永不匹配它 ⇒ 它四条边全 `0px`,其余三个各带一条上边线。
- **底色断言两侧都写死**(同一份读数里的 `body` 计算底色 + `rgb(255, 255, 255)` 字面量):只跟 `body` 比会跟着令牌一起变。
- **发丝线颜色双断言**(令牌 + gray-6 字面量):只跟令牌比是**自指的** —— 把令牌换成 `--color-border`(gray-7)会让两侧一起变、恒过,而那正是 D-11-8 显式否决的备选。**没有字面量半条,那个备选对门是不可见的。**
- **`c3` 判据取令牌级读数而非 `effective_bg`**:两级刻度里未被任何元素采用的那一档会被祖先链整个跳过,断言就在看不见的那一档上恒真(Phase 9 已为此付过代价)。另加一条「内陷面 == `rgb(249, 249, 249)` 字面量」—— 严格小于拦不住「内陷面被换成更暗的一档」。
- **交互控件对照组第三列声明该控件是否承载 resting border**(见 Deviations 第 1 条)。
- **删掉 `shadow_lengths()` / 三个卡片字面量常量后,`import re` 成为孤儿 import,一并删除**(CLAUDE.md 第 3 条:清理自己的改动造成的孤儿)。
- **变异 1 用字面量阴影而非 `var(--shadow-card)`**(理由见变异 1 下方)。

## Deviations from Plan

### 1. [Rule 1 - 计划验收措辞与磁盘事实不符] `.overlay-card` 没有 resting border,对照组的「`border-top-width != 0px`」对它不成立

- **Found during:** Task 1(`c1` 的交互控件对照组)
- **Issue:** 计划的 Task 1 验收与 `must_haves` 都写「`button` / `#project-path-input` / `#check-switcher` / `#ai-route-select` / `.overlay-card` **各自的** `border-top-left-radius` 非 `0px` **且** `border-top-width` 非 `0px`」。**实测证伪:** `.overlay-card`(`frontend/style.css:1092-1099`)只声明 `border-radius: var(--radius-md)` + `box-shadow: var(--shadow-overlay)`,**从未声明过 `border`** ⇒ 其计算 `border-top-width` 恒为 `0px`,改动前后都一样。计划写成一条统一断言会让本门**永久红**,且断言的是一个不成立的事实。
- **Fix:** 把对照组改成**逐条声明其证据形态** —— `CONTROL_GROUP` 的第三列 `has_border`:四个真正承载 resting border 的控件断言 `border-top-width != 0px`;`.overlay-card` 断言 `box-shadow != none`(elevation 仍在),五个条目**一律**断言 `border-top-left-radius != 0px`。**这不是放宽判据:** 对照组的目的(证明「移除边界」严格限于五个容器)被完整保留,而 `.overlay-card` 从未有过可被本次改动移除的边框 —— 对它断言非零边框宽度是把一条恒假命题写成门。这条事实在 `idi-11-01-SUMMARY.md` 的偏差第 1 条里已被独立登记(波次 1 的运行时读数:`control .overlay-card radius=10px border-top-width=0px box-shadow=rgba(0, 0, 0, 0.2) 0px 8px 30px 0px`),本计划与之**逐字一致**。
- **Files modified:** `scripts/check-09-idi09-validation.py`(Task 1 提交 `315af14` 内)
- **Verification:** `PASS [p1] 对照组 .overlay-card … 计算 border-top-left-radius != 0px: actual=10px` + `PASS … 计算 box-shadow != none: actual=rgba(0, 0, 0, 0.2) 0px 8px 30px 0px`;`INFO c1 对照组 .overlay-card 原始读数: border-top-left-radius=10px border-top-width=0px box-shadow=rgba(0, 0, 0, 0.2) 0px 8px 30px 0px` —— 读数与波次 1 登记值逐字相同。
- **Committed in:** `315af14`

### 2. [Rule 1 - 计划 verify 与原子提交协议冲突] Task 1 / Task 2 的 `git status --porcelain scripts/ frontend/` 在原子提交下为空

- **Found during:** Task 1 与 Task 2 的收口
- **Issue:** 计划的 `verify` 写「`git status --porcelain scripts/ frontend/` 只应列出 `scripts/check-09-idi09-validation.py`」,`fails_when` 把**空输出也判失败**。该措辞假设任务的改动**未提交**;而执行器协议要求**每个任务原子提交** ⇒ 工作树是干净的。
- **Fix:** **不改任何代码**。改以**计划区间的 diff**证明同一实质且更强:`git diff --name-only 0b05b03..HEAD` 输出**仅** `scripts/check-09-idi09-validation.py`(它证明整段计划只碰了一个文件,而不只是「此刻工作树只列它」)。
- **Files modified:** 无
- **Verification:** `git diff --name-only 0b05b03..HEAD` → `scripts/check-09-idi09-validation.py`;`git diff --stat 0b05b03..HEAD -- frontend/app.js frontend/index.html backend/ frontend/vendor/` 为空。
- **Committed in:** 无独立提交(证据在本 SUMMARY)。与 `idi-11-02-SUMMARY.md` 的偏差第 3 条同型。

### 3. [过程偏差 - 任务提交粒度] Task 2 的 `c3` / `c4` 改写与 Task 1 落在**同一次提交**里

- **Found during:** Task 1 的提交
- **Issue:** 本计划的 Task 1 与 Task 2 改的是**同一个文件的两个函数群**。我在写 Task 1 的提交之前就已把 `c3` / `c4` 的改写一并写进工作树,于是 `315af14` 同时包含了两者的内容 ⇒ Task 2 的净 diff 为零,**没有独立提交**。这偏离了「每个任务原子提交」的协议。
- **Fix:** **不改任何代码,不改写历史。** 如实登记:Task 2 的交付物(`c3` / `c4` 改写)在 `315af14` 里,Task 2 自身的剩余工作是**验证**(`--item c1,c2,c3,c4` 的计数与 `--item c5` 的复跑),净 diff 为零,故无独立提交 —— 与 `idi-11-02` 的 Task 3(纯取证、无独立提交)同型。**没有用 `git reset` / `git rebase` 去伪造一个中间态**:那需要构造一个从未真实存在过的文件版本。
- **Impact:** 对仓库最终状态**零影响**(同一个最终文件、同一批判据、同一份证据)。影响面仅限于「按提交粒度做二分定位」时 Task 1/2 不可分。若下游要求严格粒度,应在计划里把两个任务的文件落点拆开,而不是在执行期改写历史。
- **Files modified:** 无
- **Verification:** `git log --oneline 0b05b03..HEAD` → 仅 `315af14`;`git rev-list --count 0b05b03..HEAD` = **1**。
- **Committed in:** 无独立提交

### 4. [过程偏差 - 未落盘 PLAN_START_TIME]

- **Found during:** SUMMARY 撰写
- **Issue:** 执行流要求在开工时记 `PLAN_START_TIME` / `PLAN_START_EPOCH`。本次**未执行该步**,故 `duration` 只能由首个证据文件的 mtime 反推(约 30 min),不是精确读数。
- **Fix:** 不改任何代码;在 Performance 段显式标注该值是近似。
- **Files modified:** 无
- **Verification:** 无(这是过程记录的缺口,不是代码事实)
- **Committed in:** 无独立提交

---

**Total deviations:** 4(1 × Rule 1 计划措辞证伪 + 1 × Rule 1 计划 verify 与协议冲突 + 2 × 过程偏差)
**Impact on plan:** **零范围扩张、零代码放宽。** 第 1 条把一条恒假的断言改成两条各自成立、各自可失败的断言(对照组目的完整保留);第 2 / 3 / 4 条不改变交付物,只是把「计划措辞与执行模型不符」的事实如实登记。四条都**没有**删除断言、**没有**降级为恒真、**没有**改判据去迁就变异结果。

## Issues Encountered

- **`check-09` 在本次改写前是 RED BY DESIGN。** 规划期与执行期在 HEAD(`0b05b03`)上各实测一次,读数逐字相同:`item c1: FAIL (26 条断言,14 FAIL,6 BLOCKED)` / `c2: FAIL (13,8,1)` / `c3: FAIL (3,1,1)` / `c4: FAIL (4,1,0)` / `c5: PASS (5,0,0)`,`exit=1`。**那正是门在正确工作的证据**,不是回归。本计划把它改写为断言新契约后 `exit=0`。
- **`git stash` 全程未使用。** 六条变异的还原一律走定向 `git checkout -- frontend/style.css`,并以 `git diff --exit-code` 为空 + `git hash-object` 逐字符相同两道独立证据收口(见上表)。
- **变异 3 的首次注入被自己发现并作废重做**(它误把变异 2 的改动一并施加)。原始读数未采用,已按最小改动重跑。这是「逐条最小改动」纪律的一次实际生效,登记以留痕。
- **`frontend/style.css` 在本次执行前后逐字节相同**(`cfcaef098d957abc885413793cd8b1a9dc12193f`),本计划对 CSS 零改动 —— 它已在波次 1/2 定型。
- **端口 8765 上有一个既有的 uvicorn 进程**,`ensure_server()` 复用了它(未新起、结束时也未关闭),与既有阶段的门运行方式一致。

## Known Stubs

None。本计划不产生任何 stub:零新增 CSS 自定义属性、零新增颜色值、零新增 PAIR / ORDER 条目、零新依赖、零占位文案、零 `t.skip` / `test.todo`。三条任务的 `<verify>` **全部实际执行过**(六条变异各一次实跑 + 还原后复绿 + 最终 c1..c4 与 c5 各一次),没有未跑的验证项。

## Threat Flags

None。本计划只改一个**只读的本地运行时门脚本**的判据:零用户输入处理、零鉴权、零数据访问、零网络调用、零新增资源加载。威胁模型的四条缓解均已落地并被判据覆盖:
- **T-idi-11-12(变异对 `frontend/style.css` 的临时修改,high)** → 每条变异后立刻定向还原;判据是 `git diff --exit-code` 退出码 0 **且** `git hash-object` 与变异前记录值逐字符相同(两道独立判据,不靠记忆);**禁用 `git stash`**;收口时 `git status --porcelain frontend/` 为空。**六次全部通过。**
- **T-idi-11-13(把门改小以让结论成立,high)** → 断言总数由 46 **升到 102**(机器判据);六条变异逐条证明判据真的会失败;交互控件对照组与活动标记的正面断言使「移除边界」不可被过度执行;双断言的字面量半条使 gray-7 备选对门可见。
- **T-idi-11-14(结论缺少可复核的原始证据,high)** → 六条变异各给出 FAIL 行的**完整原文**(含 `expected=` / `actual=`);`=== 逐项结论 ===` 块与断言计数原文入册;还原后的 `git diff --exit-code` 与 `git hash-object` 值入册。
- **T-idi-11-15(fixture 生命周期,medium)** → 本计划**一行都没有重写** `check-05` 的 `make_fixture` / `enter_project`;`git status --porcelain scripts/ui-states/` 为空。

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **计划 04 可直接开始**(波次 4,门禁收口):本计划结束时 `check-09` 的 `c1..c5` **全绿且说真话**(`--item c1,c2,c3,c4` → `exit=0`;`--item c5` → `exit=0`)。
- **计划 04 的 REG-03 复测**:`check-05 --item 8` 的 sticky 余量读数与成因已在 `idi-11-01-SUMMARY.md` 登记(由 `1.000px` 变为 `0.000px`,成因是移除的 1px 上边框)。本计划的 `c2` 新增了一条对同一事实的**正向**断言(`#doc-panel` 的 `border-top-width == 0px`),故那条 1px 若被回填,本门会与 `check-05 --item 8` 一起变红。
- **`REG-04` 的连带指纹面(Phase 12)**:本计划改动的是 `scripts/check-09-idi09-validation.py` ⇒ 该脚本的覆盖者会被拖进重验名单,**份数须在磁盘上逐份读 `covered_files` 实测**(判据锚 frontmatter 的 `covered_files` 逐行匹配,不是全文 grep)。本 SUMMARY 只登记该事实,不做份数断言。
- **本计划结束时五条静态门未复跑** —— 计划把它显式留给计划 04(`gate-logs/` 落盘)。本计划的可复核改动只有 `scripts/` 下一个 python 文件,不触碰 `frontend/style.css`,故静态门的输入面未变。
- **无阻塞项。** 唯一待办是把本 SUMMARY 与 STATE / ROADMAP 的收尾提交落下。

---

*Phase: idi-11-decard-and-hairline-dividers*
*Completed: 2026-09-28*

## Self-Check: PASSED

- `scripts/check-09-idi09-validation.py` — FOUND(唯一改动文件;`git diff --name-only 0b05b03..HEAD` 仅列出它)
- `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-03-SUMMARY.md` — FOUND
- Commit `315af14` — FOUND
- `commits` 实测 = `git rev-list --count 0b05b03..HEAD` = 1(与 frontmatter 的 `actuals.commits: 1` 一致;Task 2 / Task 3 净 diff 为零,无独立提交)

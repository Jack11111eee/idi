---
phase: idi-11-decard-and-hairline-dividers
plan: 02
subsystem: ui
tags: [css, design-tokens, contrast, check-02, token-deletion, decard]

requires:
  - phase: idi-11-decard-and-hairline-dividers
    plan: 01
    provides: 5 处消费者已搬到统一面令牌(两个卡片令牌消费者归零)+ 统一面就地换值为白
  - phase: idi-10-tables-and-radius-scale
    provides: 「删除令牌必配专用残留断言」的先例(check-10 的 r1)与「就地改写 + 追加不重排」纪律
provides:
  - 两个被本次反转孤立掉的令牌声明已删除(--color-surface-card / --shadow-card)
  - 围栏内 7 处点名这两个令牌名的注释已改写为概念短语,围栏内出现次数归零
  - 2 条卡片地面 PAIR 按元素实际绘制面重归属到统一面
  - Phase 11 的地面重算登记段(六条重算 gray-3 → white 两列 + 两条重归属的「比值不变」消解)
affects: [idi-11-03, idi-11-04, idi-12]

actuals:
  tokens: 3936
  tasks: 3
  commits: 2
plan_head_before: 6fe03c6068dbec9c90f2532a636e1f7cd87650fc

tech-stack:
  added: []
  patterns:
    - "删除令牌时,围栏内点名它的注释必须同步改写为概念短语(子串计数判据扫含注释的围栏全文)"
    - "重归属 = 改地面标签 + 重算;重归属与删声明必须同一次改动(check-02 的 resolve() 对未声明令牌 exit 1)"
    - "「比值不变」必须在注释里主动消解(两条重归属的地面同值),否则会被后人误读成偷懒"

key-files:
  created: []
  modified:
    - frontend/style.css

key-decisions:
  - "两个令牌删除而非保留:围栏抬头与 Hard Rule 5 / D-04「只声明被消费的令牌」——与 Phase 10 删 28px 圆角档位同型(D-11-2 / D-11-4)"
  - "显式写明「这不是通用围栏消费断言(G2 不在本里程碑范围)」,防止后人把这次专用处置泛化"
  - "两条重归属的地面标签由卡片令牌改指 --color-surface-page(只改标签,不改前景令牌/种类);因两个地面同值(白),比值不变(4.77 / 3.32)"
  - "marker-active 的 NON-TEXT 半条仍留 --color-surface-page,但理由已从「更严的一侧」换成「地面本身就是它」——Phase 9 的 stricter-side 论证随两地面同值而退休"
  - "六条页面地面 PAIR 全部重算且全部上升(白面更亮 ⇒ 深色前景对比度上升):16.29 / 5.92 / 5.92 / 5.87 / 5.92 / 4.77"
  - "C-10 的既有陈旧注释(现 :727-729,声称 #doc-panel 声明内陷面底色)按计划只登记、不改"

patterns-established:
  - "围栏内注释的「令牌名出现次数 == 0」判据是子串计数、含注释 ⇒ 只删声明行不够,必须改写每一条点名它的注释"

requirements-completed: [REG-02]

coverage:
  - id: D1
    description: "两个被本次反转孤立掉的令牌声明已从围栏内删除;围栏内它们的名字出现次数各为 0;Phase 10 删掉的 28px 圆角档位名仍为 0"
    requirement: "REG-02"
    verification:
      - kind: other
        ref: ".venv/bin/python -c \"fence.count('--color-surface-card') / fence.count('--shadow-card') / fence.count('--radius-lg')\" → 0 / 0 / 0"
        status: pass
      - kind: other
        ref: "grep -nF -- 'var(--color-surface-card)' / 'var(--shadow-card)' frontend/style.css → rc=1(零消费者)"
        status: pass
    human_judgment: false
  - id: D2
    description: "2 条卡片地面 PAIR 按元素实际绘制面重归属到统一面;清单规模 53 对(35 TEXT + 18 NON-TEXT)+ 1 条 ORDER 逐字不变;无重复条目;check-02 PASS: 0 failures"
    requirement: "REG-02"
    verification:
      - kind: unit
        ref: ".venv/bin/python scripts/check-02-contrast.py → PASS: 0 failures;含 PASS 4.77 --color-marker-active on --color-surface-page 与 PASS 3.32 --color-border-strong on --color-surface-page"
        status: pass
      - kind: other
        ref: "grep -o '/\\* PAIR' frontend/style.css | wc -l → 53;grep -o '/\\* ORDER' → 1"
        status: pass
    human_judgment: false
  - id: D3
    description: "六条页面地面 PAIR 以新统一面(白)重算并在围栏内登记(gray-3 → white 两列并排),两条重归属的「比值不变是因为两地面同值」被显式消解,两条最紧判据被点名"
    requirement: "REG-02"
    verification:
      - kind: other
        ref: "grep -cF -- 'Phase 11' frontend/style.css → 25(含 Phase 11 page-ground RECOMPUTATION ledger 段)"
        status: pass
    human_judgment: true
    rationale: "登记段是承重注释,「重算 vs 刷新」的可区分性(旧值与新值并排)须人眼确认;数字本身由 check-02 实跑背书。"
  - id: D4
    description: "统一面与内陷面的亮度序在运行时仍成立(内陷面 gray-2 严格更暗),证明「统一」不是「压平」"
    requirement: "REG-02"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c3 (INFO 三行值读数)"
        status: pass
      - kind: other
        ref: "check-02 的 relative_luminance 独立复算:gray-2 = 0.947307 < white = 1.000000"
        status: pass
    human_judgment: false
  - id: D5
    description: "四条静态门全绿;零新增 primitive / 零阈值改动 / 零清单增删 / 零媒体查询;scripts/ 与 app.js / index.html / backend / vendor 逐字节未改"
    requirement: "REG-02"
    verification:
      - kind: other
        ref: "bash scripts/check-01-token-conformance.sh → PASS;check-03 → PASS;check-04 → PASS;check-02 → PASS: 0 failures"
        status: pass
      - kind: other
        ref: "git diff --name-only 6fe03c6..HEAD → 仅 frontend/style.css"
        status: pass
    human_judgment: false

duration: 27min
completed: 2026-09-28
status: complete
---

# Phase 11 Plan 02: 令牌处置与 check-02 地面重归属 Summary

**删除本次反转自己孤立掉的两个卡片令牌(声明 + 围栏内 7 处点名注释全部改写),把 2 条卡片地面 PAIR 按元素实际绘制面重归属到统一面,并在围栏内登记六条页面地面 PAIR 的 gray-3 → white 重算 —— 全部是 `frontend/style.css` 一个文件上的纯声明层 + 注释层改动。**

## Performance

- **Duration:** 27 min
- **Started:** 2026-09-28T05:53:31Z
- **Completed:** 2026-09-28T06:20:25Z
- **Tasks:** 3
- **Files modified:** 1 (`frontend/style.css`)

## Accomplishments

- **两个令牌删除。** `--color-surface-card` 与 `--shadow-card` 两行声明从围栏内删除(计划 01 已把 5 处消费者搬走)。依据是围栏抬头与 Hard Rule 5 / D-04「只声明被消费的令牌」——与 Phase 10 删 `--radius-lg` 同型(D-11-2 / D-11-4)。
- **围栏内两个令牌名的出现次数由 7 / 1 归零。** 判据是**子串计数、扫含注释的围栏全文**(`check-10` 的 `fence_text()` 语义)。只删声明行会立刻失败 —— 7 处点名它们的注释(含 `Tier 2 — the card container language` 块)全部改写为概念短语(「the raised ground」「the retired card container language」),Phase 10 删 28px 圆角档位时的注释同型:替代注释里被删的名字一个字都没出现。
- **显式划出 G2 边界。** 新注释块写明「这不是通用围栏消费断言 —— 那是 G2,用户明确排除在本里程碑范围外」,防止后人把这次**专用**处置泛化成通用断言(D-11-4)。
- **2 条 PAIR 按实际绘制面重归属。** `--color-marker-active … TEXT` 与 `--color-border-strong … NON-TEXT` 的地面标签由卡片令牌改指 `--color-surface-page`(只改标签,不改前景令牌与 `TEXT` / `NON-TEXT` 种类)。因两个地面同值(白),比值不变(4.77 / 3.32)—— 这一点在注释里被主动消解,否则会被后人误读成「没重算」。
- **六条页面地面 PAIR 重算并登记。** 新增 `Phase 11 page-ground RECOMPUTATION ledger` 段,逐条给出「Phase 9 的 gray-3 读数 → Phase 11 的白面读数」两列,并写明白面更亮 ⇒ 深色前景对比度上升(六条全部上升)。
- **marker-active 的 NON-TEXT 半条:stricter-side 论证退休而非被推翻。** Phase 9 把它留在页面地面是因为页面是更严的一侧(4.18 < 4.77);Phase 11 两个地面同值(都是白,4.77),该论证不再适用 —— 条目**仍**留页面地面,但理由是「地面本身就是它」,不是保守选择。
- **规模与阈值逐字不变。** 53 对(35 TEXT + 18 NON-TEXT)+ 1 条 ORDER;`TEXT_MIN = 4.5` / `NON_TEXT_MIN = 3.0` 与 HEAD 逐字节相同(`check-02` 脚本零 diff);`ORDER 0.363` 不退化。
- **四条静态门全绿;`frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**` 逐字节未改。**

## Task Commits

Each task was committed atomically:

1. **Task 1: 删两个被孤立的卡片令牌 + 围栏注释改写 + 2 条 PAIR 重归属** - `630ebb1` (feat)
2. **Task 2: Phase 11 地面重算登记段(六条重算 + 两条重归属)** - `b1b4c42` (docs)
3. **Task 3: 统一面运行时读数 + 四条静态门 + 零改动逐字节证据** - **无独立提交**(纯取证,净 diff 为零;证据在本 SUMMARY,沿 `idi-04-03` / `idi-09` 计划 02 先例)

**Plan metadata:** 见收尾的 docs 提交。

## Files Created/Modified

- `frontend/style.css` — 唯一改动文件。围栏内:删除 2 行令牌声明 + 改写 7 处注释 + 2 条 PAIR 地面标签 + 新增 1 段 `Phase 11` 重算登记段。围栏外:零改动。

## 运行时读数的原始输出(逐字抄录)

### `check-09 --item c3`(真实浏览器 computed style)

```
INFO c3 body 计算 background-color 原始读数: rgb(255, 255, 255)
INFO c3 --color-surface-page 令牌解析值: rgb(255, 255, 255)
INFO c3 页面 --color-surface-page 解析值: rgb(255, 255, 255)
INFO c3 内陷面 --color-surface 解析值: rgb(249, 249, 249)
INFO c3 卡片 --color-surface-card 解析值: None
```

**门此时报 `FAIL (3 条断言,1 FAIL,1 BLOCKED)` / exit 1 —— 设计预期,不是回归。** 它断言的仍是 Phase 9 的三级刻度(`body 计算底色 == gray-3` + 三档亮度严格递增);被删令牌那一档让「三档均可解析」记 BLOCKED,故**相对亮度诊断行未打印**(`check-09:312-315` 在任一档为 None 时提前 return)。**本计划一行都没有改 `check-09`** —— 其 c1..c4 的承重改写属计划 03。

**亮度序由 `check-02` 的 `relative_luminance` 独立复算补证**(用项目自己的算术,不是推断):

```
内陷面 gray-2 (#f9f9f9) 相对亮度 = 0.947307
统一面 white  (#ffffff) 相对亮度 = 1.000000
内陷面严格低于统一面 = True
```

⇒ SC2 的「内陷面仍是唯一比统一面更暗的一档」成立;「统一」是把卡片档并回页面档,**不是**把层次压平。

### `check-02` 的八条受影响读数(逐字抄录)

```
PASS  16.29  --color-text on --color-surface-page
PASS  5.92  --color-text-secondary on --color-surface-page
PASS  5.92  --color-text-muted on --color-surface-page
PASS  5.87  --color-focus on --color-surface-page
PASS  5.92  --color-border-hover on --color-surface-page
PASS  4.77  --color-marker-active on --color-surface-page
PASS  4.77  --color-marker-active on --color-surface-page
PASS  3.32  --color-border-strong on --color-surface-page
ORDER 0.363  --color-text-muted before --color-text on --color-surface
PASS: 0 failures
```

前六条是**重算**(地面标签不变),末两条是**重归属**(地面标签由卡片令牌改指统一面)。两条 `--color-marker-active on --color-surface-page` 分别是 NON-TEXT 与 TEXT 半条 —— 种类不同,无重复条目。

### 四条静态门的标准输出原文

```
=== check-01-token-conformance.sh ===   PASS   EXIT=0
=== check-02-contrast.py ===            PASS: 0 failures   EXIT=0
=== check-03-hidden-uniqueness.sh ===   PASS   EXIT=0
=== check-04-important-count.sh ===     PASS   EXIT=0
```

## 零改动 / 零放宽的逐字节证据

| 判据 | 实测 |
|---|---|
| 围栏内 `--color-surface-card` / `--shadow-card` / `--radius-lg` 出现次数 | **0 / 0 / 0**(子串计数,含注释) |
| 围栏外 `var(--color-surface-card)` / `var(--shadow-card)` 消费者 | **0 / 0**(两条 `grep -nF` 均 rc=1) |
| 解析后的声明集 vs 计划前 HEAD(`6fe03c6`) | removed `['--color-surface-card','--shadow-card']`;added `[]`;changed `{}` ⇒ 注释改写**未**混入伪声明(121 → 119 条) |
| `/* PAIR` / `/* ORDER`(文件全文) | **53 / 1** |
| `git diff --exit-code -- scripts/check-02-contrast.py` | **空**(rc=0)⇒ `TEXT_MIN` / `NON_TEXT_MIN` 与 HEAD 逐字节相同 |
| `git diff --stat 6fe03c6..HEAD -- scripts/` | **空** ⇒ 三个门脚本本计划零改动 |
| `git diff -U0 6fe03c6..HEAD -- frontend/style.css` 的新增 `--radix-` 行数 | **0**(rc=1)⇒ 零新增 tier-1 primitive |
| `@media` 出现次数 | **恰 1**(`frontend/style.css:2015`,Phase 7 的 prefers-reduced-motion 块) |
| `git diff --name-only 6fe03c6..HEAD` | **仅 `frontend/style.css`** |
| `git diff --stat 6fe03c6..HEAD -- frontend/app.js frontend/index.html backend/ frontend/vendor/` | **空** |
| `ls frontend/vendor/` | 仅 `marked.min.js` |

### D-11-3 的两个「不产生新孤儿」事实复核(逐行核对,非只数个数)

```
144:  --color-surface-sunken: var(--radix-gray-3);
216:  --color-surface-hover: var(--radix-gray-3);
215:  --color-surface: var(--radix-gray-2);
```

- `--radix-gray-3` 仍有 **2 个**消费者(`--color-surface-sunken` / `--color-surface-hover`)⇒ 统一面换值**未**造出新的零消费 primitive。
- `--radix-gray-2` **恰 1 个**消费者(`--color-surface`),未受影响。
- `--radix-gray-1` 仍**零**消费者(`grep` rc=1)⇒ G2 的事实基底一字未动。

## Decisions Made

- 两个令牌**删除**而非保留,援引围栏抬头 + Hard Rule 5 / D-04,与 Phase 10 删 `--radius-lg` 同型;并在注释里**显式声明这不是 G2**。
- 重归属只改**地面标签**,不改前景令牌与 `TEXT` / `NON-TEXT` 种类 —— 重归属与删声明同一次提交(否则 `resolve()` 的中间态会红)。
- 两条重归属的**比值不变**在注释里主动消解:白卡片与白统一面同值,所以数字不动,而不是「没重算」。
- marker-active 的 NON-TEXT 半条**仍留**页面地面,但把 Phase 9 的 stricter-side 论证记为**退休**(两地面同值)而非推翻 —— 并写明它不是「把条目搬走」的理由。
- 登记段用**两列**(gray-3 → white)而非只给新数字,使「重算」与「刷新」可区分(T-idi-11-10 的缓解)。

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - 计划措辞与磁盘事实不符] marker-active 的两处注释写「四个面板」会把活动标记说成落在 `#ai-panel` 上**

- **Found during:** Task 1(改写围栏注释)
- **Issue:** 计划把活动标记的宿主描述为「三个面板现在是**不透明白卡片**」。改写时我一度写成「the four left-hand panels now paint the same surface as the page」——**实测证伪**:活动标记的规则体是 `#session-panel` / `#annotations-panel` / `#checks-panel` 三条 ID 选择器(`frontend/style.css:1690-1693`),**不含 `#ai-panel`**。故「四个面板」会把标记的宿主多算一个。
- **Fix:** 改回精确措辞「the three panels that carry the marker」/「the three panels that carry it」。**这不是放宽判据** —— 没有任何门断言这段散文;它只是把事实写对。
- **Files modified:** `frontend/style.css`(围栏内注释,Task 1 提交内)
- **Verification:** `grep -n -B6 'inset 3px 0 0 var(--color-marker-active)' frontend/style.css` 确认宿主恰三条 ID 选择器;`check-02` 仍 `PASS: 0 failures`;围栏计数仍 0/0/0。
- **Committed in:** `630ebb1`(Task 1 提交)

### 计划验收项的实测更正(已登记,零代码改动)

**2. [Rule 1 - 计划 verify 的 grep 面与磁盘不符] `check-09 --item c3` 的相对亮度诊断行在令牌缺失时不打印**

- **Found during:** Task 3(运行时取证)
- **Issue:** 计划的 Task 3 verify 要求 `check-09 --item c3` 的输出里出现 `INFO c3 (内陷面|页面|卡片) 相对亮度` 行。**实测证伪**:`check-09:312-315` 在任一档令牌解析为 None 时**提前 `blocked()` 并 return**,亮度循环根本不会执行 —— 而被删的卡片令牌正是那一档。故该诊断行在本计划结束时**结构上不可能出现**。
- **Fix:** **不改 `check-09`**(其 c3 判据改写属计划 03)。改以 `check-02` 的 `relative_luminance` **独立复算**补足同一事实:内陷面 0.947307 < 统一面 1.000000。三条**值** INFO 行(计划 verify 的主判据)全部如实出现并已抄录。
- **Files modified:** 无
- **Verification:** `.venv/bin/python scripts/check-09-idi09-validation.py --item c3` 输出含三条值 INFO 行(见上);亮度序由项目自己的算术复算为 True。
- **Committed in:** 无独立提交(证据在本 SUMMARY)

**3. [Rule 1 - 执行模型差异] Task 3 的 `git status --porcelain frontend/ backend/ scripts/` 在原子提交下为空**

- **Found during:** Task 3(零改动边界取证)
- **Issue:** 计划的 Task 3 verify 写「`git status --porcelain frontend/ backend/ scripts/` 只应列出 `frontend/style.css`」,`fails_when` 把**空输出也判失败**。该措辞假设三个任务的改动**未提交**;而执行器协议要求**每个任务原子提交** —— Task 1/2 已把 `style.css` 落盘,故工作树是干净的。
- **Fix:** **不改任何代码**。改以**计划区间的 diff**证明同一实质:`git diff --name-only 6fe03c6..HEAD` 输出**仅** `frontend/style.css`(比「工作树只列它」更强:它证明整段计划只碰了一个文件)。工作树干净 + 计划区间单文件 = 计划想要的结论成立。
- **Files modified:** 无
- **Verification:** `git diff --name-only 6fe03c6..HEAD` → `frontend/style.css`;`git diff --stat 6fe03c6..HEAD -- frontend/app.js frontend/index.html backend/ frontend/vendor/` 为空。
- **Committed in:** 无独立提交(证据在本 SUMMARY)

---

**Total deviations:** 3 auto-fixed(3 × Rule 1;均为「计划措辞/验收面与磁盘事实或执行模型不符」,第 1 条是一处注释措辞更正,后两条零代码改动)
**Impact on plan:** 零范围扩张、零代码改动。三条都不改变交付物:两个令牌已删净、2 条 PAIR 已重归属、六条已重算并登记、四条静态门全绿。第 2 / 3 条是**计划验收措辞的实测更正**,不是放宽判据 —— 两者都另给了更强的替代证据。

## Issues Encountered

- **`check-09 --item c3` 在本计划结束时 FAIL / exit 1 —— 设计预期,不是回归。** 它断言的正是本阶段移除的 Phase 9 三级刻度;被删令牌那一档记 BLOCKED。本计划**一行都没有改** `check-09`;其 c1..c4 的承重改写属计划 03。判据取它的**值 INFO 原始读数**,不取它的整体裁决。
- **C-10 的既有陈旧注释已登记、未修改(计划明令)。** 现位于 `frontend/style.css:727-729`,原文声称「`#doc-panel` declares background: var(--color-surface)`」—— 它在 Phase 9 就已失真(`#doc-panel` 当时声明的是卡片令牌),本阶段让它**更**失真(现在是统一面令牌)。计划把「重归属它」明确排除在本阶段枚举范围外,**只登记**:
  ```
  727:  /* the two solid-fill steps are boundaries in their own right (SC 1.4.11). Each fill
  728-     sits on --color-surface: #approve-row / #writing-view / #authorize-row all live in
  729-     #doc-panel-body → #doc-panel, and #doc-panel declares background: var(--color-surface). */
  ```
  它影响的两条 PAIR(`--color-action-commit` / `--color-action-irreversible` ON `--color-surface` NON-TEXT)不在 D-11-15 / SC5 枚举的 2 + 6 条之内,且标签取的是**更保守**的一侧(gray-2 比白更暗),故无条目变红。**建议后续阶段(或 Phase 12)裁定是否重归属这两条。**
- **`gsd-tools windows append` 未在本计划使用** —— 本计划没有留下 stub / skipped-test / unrun-verify 类缺陷(见下节)。上条 C-10 属**计划显式登记的已知陈旧注释**,不是本计划引入的缺陷。

## Known Stubs

None。本计划不产生任何 stub:零新增 CSS 自定义属性、零新增颜色值、零新增 tier-1 primitive、零新增 / 零删除 PAIR / ORDER 条目、零新依赖、零占位文案。

**一条待后续阶段处置的既有事实(非 stub,登记以并入跨阶段缺陷视野):** C-10 的陈旧注释(现 `:727-729`)与它影响的两条 `--color-surface` 地面 PAIR —— 计划显式只登记不改(见上)。

## Threat Flags

None。本计划只改 `frontend/style.css` 围栏内的声明与注释(令牌层),零用户输入处理、零鉴权、零数据访问、零网络调用、零新依赖。威胁模型 T-idi-11-07 / 08 / 09 / 10 的缓解均已落地并被判据覆盖:重归属与删声明同一次改动(`check-02` 实跑出现两条 `on --color-surface-page` 行);围栏内两个令牌名计数为 0;`check-02` 脚本零 diff + 条目数 53/1 两条独立计数;八条实跑输出行原文入册。

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **计划 03 可开始改写 `check-09` 的 c1..c4**,并落地 D-11-4 的两条**专用**残留断言(照 `check-10` 的 `r1` 同型,`fenced.count(<被删令牌名>) == 0`)。注意:本 SUMMARY 与围栏注释刻意**不写出**那两个令牌名,故计划 03 写断言时须直接引用令牌名字面量 —— 那正是判据对象。
- **计划 04 的 REG-03 复测**:`check-05 --item 8` 的 sticky 余量读数与成因已在 `idi-11-01-SUMMARY.md` 登记(由 `1.000px` 变为 `0.000px`)。
- **本计划结束时 `check-02` 是唯一「绿且说真话」的对比度门** —— 它描述的地面全部是屏幕上真实存在的面。
- **无阻塞项。** 唯一待办是把本 SUMMARY 与 STATE / ROADMAP 的收尾提交落下。

---

*Phase: idi-11-decard-and-hairline-dividers*
*Completed: 2026-09-28*

## Self-Check: PASSED

- `frontend/style.css` — FOUND(唯一改动文件;`git diff --name-only 6fe03c6..HEAD` 仅列出它)
- `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-02-SUMMARY.md` — FOUND
- Commit `630ebb1` — FOUND
- Commit `b1b4c42` — FOUND
- `commits` 实测 = `git rev-list --count 6fe03c6..HEAD` = 2(与 frontmatter 的 `actuals.commits: 2` 一致;Task 3 净 diff 为零,无独立提交)

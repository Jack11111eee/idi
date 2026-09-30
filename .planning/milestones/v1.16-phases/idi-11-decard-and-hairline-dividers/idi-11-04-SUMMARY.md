---
phase: idi-11-decard-and-hairline-dividers
plan: 04
subsystem: test
tags: [playwright, runtime-gate, check-05, re-registration, reg-03, sticky-margin, gate-logs, decard]

requires:
  - phase: idi-11-decard-and-hairline-dividers
    plan: 01
    provides: 反转本体已定型(连续面 + 统一面 + 灰缝归零 + 两条发丝线),本计划复跑的门看的就是它的渲染结果
  - phase: idi-11-decard-and-hairline-dividers
    plan: 02
    provides: 两个被孤立令牌已删净 ⇒ check-05 的 `.hint` 断言的期望侧因令牌消失而降级成 BLOCKED(本计划处置的形态)
  - phase: idi-11-decard-and-hairline-dividers
    plan: 03
    provides: check-09 的 c1..c5 已改写并变异证明,本计划复跑的是它的最终形态
  - phase: idi-09-card-containers
    provides: 「重新登记 ≠ 放宽」的同文件同断先前例,与 `check-05 --item 8` 余量 1.000px 的引入
  - phase: idi-10-tables-and-radius-scale
    provides: gate-logs/ 原始门输出落盘的先例(13 份,逐项对照基线)
provides:
  - check-05 的 `.hint` 实际背景断言期望侧重新登记到统一面令牌(断言形式一字未变,不再 BLOCKED)
  - REG-03 的 sticky 余量新读数(0.000px)与成因机制登记,判据与产品代码均未回退
  - 13 份原始门日志落盘(含退出码),与 Phase 10 基线逐项并排对照
  - 连带指纹面的实测表(11 / 1 / 7,全部 fail-closed stale),标注为 Phase 12 REG-04 的输入
affects: [idi-12]

actuals:
  tokens: 45607
  tasks: 3
  commits: 2
plan_head_before: 4564195c868ad68531650ea4c848e532a353dd55

tech-stack:
  added: []
  patterns:
    - "门里一条断言「静默死亡」的判据是它记 BLOCKED 而非 FAIL —— 本项目把 exit 2 当良性码,故门不会变红,必须靠人逐条读断言"
    - "令牌被删时,任何「期望侧走 resolve_color 的 ok() 等值断言」都会静默降级成 BLOCKED;处置是**换指到仍存在的令牌**,不是改成 ok_contains / 非透明判据 / 硬编码 rgb / or 分支"
    - "读数变化的分诊判据是「该断言描述的事实是否被改变」,不是「数字是否变了」"
    - "全门复跑的证据是**原始输出 + 退出码**落盘,不是 SUMMARY 里的摘录(摘录是选过的)"

key-files:
  created:
    - .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/(13 份日志)
  modified:
    - scripts/check-05-ui-uat.py

key-decisions:
  - "采用本计划的主路线(改 check-05 的期望侧)而非编排器指令 C-2 的「不得触碰」:先复现了退化(BLOCKED expected=<UNRESOLVED>,item 5 由 2 变 3 BLOCKED,exit 仍 2),再换指;C-2 的成本理由(7 份覆盖者)经磁盘实测已失效 —— 7 份全部 fail-closed stale ⇒ 边际重验成本为零"
  - "断言形式一字未变:仍是 ok(...) 的精确等值(实测 computed 值 == 运行时解析的令牌值);未用 ok_contains / 非透明判据 / 硬编码 rgb / or 分支,也未删该断言"
  - "REG-03 的分诊结论:该断言描述的事实(sticky 表头遮挡滚动正文)未被改变 ⇒ 只更新余量读数与成因登记,判据不动;余量由 1.000px 变 0.000px 是事实被如实登记,不得把 1px 上边框加回去(D-11-16)"
  - "check-05 的改动面经 git diff -U0 逐行核对,只有期望侧令牌名 + 标签文本 + 相邻注释三处;其它任何一行未动"
  - "gate-logs 按 Phase 10 同形落盘 13 份(check-01..04 + check-05 全量 + 06 + 07 + 09 + 10 + pytest + node --check + probe-05 + probe-07),每份附 [gsd] EXIT=N"
  - "REG-04 只实测并登记,不做重验、不刷新任何指纹 —— 正式处置归 Phase 12"

patterns-established:
  - "「重新登记」的完整形态 = 先复现退化(证明断言真的会静默死亡)+ 换指到仍存在的令牌 + 断言形式一字未变 + 相邻注释写清「为什么必须改」"
  - "跨阶段门禁对照取归一化(剥临时路径)后的逐行 diff,不取「结论块看着一样」—— 这个粒度捞出了计划未点名的 check-06 几何位移"

requirements-completed: [REG-03]

coverage:
  - id: D1
    description: "check-05 里那条会静默死亡的 `.hint` 实际背景断言已重新登记:期望侧为 resolve_color(page, \"--color-surface-page\"),断言形式仍是 ok() 的精确等值;复跑后 PASS 且 item 5 的 BLOCKED 计数由 3 回到 2"
    requirement: "REG-03"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 5 --browser bundled → PASS expected=rgb(255, 255, 255) actual=rgb(255, 255, 255);item 5: BLOCKED (9 条断言,0 FAIL,2 BLOCKED);exit=2"
        status: pass
      - kind: other
        ref: "git diff -U0 -- scripts/check-05-ui-uat.py → 仅注释块 + 标签文本 + 期望侧三处;git diff --stat -- check-09/check-02/check-10/style.css 为空"
        status: pass
    human_judgment: false
  - id: D2
    description: "REG-03 的 sticky 余量复测:读数由 1.000px 变为 0.000px,成因机制已登记;D-11-16 的「事实是否被改变」分诊已做且结论为「未改变」⇒ 只更新读数,判据与产品代码均未回退"
    requirement: "REG-03"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled → item 8: PASS (13 条断言,0 FAIL,0 BLOCKED);INFO item8 sticky 原始数值 原文入册"
        status: pass
      - kind: other
        ref: "grep -nF 'abs(hp[\"top\"] - pp[\"top\"]) <= 1.0' → 命中(容差字面量逐字未改);git diff --stat -- frontend/style.css 为空;git hash-object frontend/style.css = cfcaef098d957abc885413793cd8b1a9dc12193f"
        status: pass
    human_judgment: true
    rationale: "「事实是否被改变」是设计判断(该断言描述的是「sticky 表头遮挡滚动正文」,而本阶段只改容器的边框/底色与间距),机器判据只能证明读数与容差字面量;分诊结论须人眼确认它没有把「数字变了」误当成「事实变了」。"
  - id: D3
    description: "13 份门的原始输出与退出码落盘;五条浏览器门 ^FAIL 计数均为 0;check-05 全量 exit=2 的成因集合仍只是 item 5 的两条 --ai-smoke 腿;pytest 219 passed / 6 skipped"
    requirement: "REG-03"
    verification:
      - kind: other
        ref: "ls gate-logs/ → 13 份;grep -c '^FAIL' 五条浏览器门日志 → 全 0;pytest.log → 219 passed, 6 skipped, 1 warning"
        status: pass
    human_judgment: false
  - id: D4
    description: "连带指纹面在磁盘上逐份实测(判据锚 frontmatter 的 covered_files 逐行匹配 + 路径是否在盘):style.css 11 份 / check-09 1 份 / check-05 7 份,全部 fail-closed stale ⇒ 本阶段零新增作废;未刷新任何指纹(REG-04 归 Phase 12)"
    requirement: "REG-03"
    verification:
      - kind: other
        ref: "一次性解析脚本(系统临时目录,跑完清空):.planning/** 下 20 份 VERIFICATION.md / UAT.md,命中 11 / 1 / 7,每份均报 status=fail-closed stale(missing 2..13 条)"
        status: pass
    human_judgment: false
  - id: D5
    description: "仓库卫生:app.js / index.html / backend / vendor 逐字节未改;style.css 本计划零改动且 hash 未变;PAIR 53 / ORDER 1;vendor 仅 marked.min.js"
    requirement: "REG-03"
    verification:
      - kind: other
        ref: "git diff --stat 6afe679..HEAD -- frontend/app.js frontend/index.html backend/ frontend/vendor/ 为空;git status --porcelain frontend/ scripts/ backend/ 为空(原子提交后);ls frontend/vendor/ 仅 marked.min.js"
        status: pass
    human_judgment: false

duration: 30min
completed: 2026-09-28
status: complete
---

# Phase 11 Plan 04: 门禁收口 — `.hint` 断言重新登记、REG-03 复测与全门复跑 Summary

**把 `check-05` 里一条因令牌被删而**静默死亡**的断言按 Phase 9 的同一条纪律重新登记(期望侧换指统一面令牌,断言形式一字未变),复测并登记 `check-05 --item 8` 的 sticky 余量变化(1.000px → 0.000px,事实未变 ⇒ 判据不动),并把 13 条门在最终树上复跑一遍、原始输出与退出码落盘。**

## Performance

- **Duration:** ~30 min
- **Started:** 2026-09-28T07:10:32Z
- **Completed:** 2026-09-28T07:40:50Z
- **Tasks:** 3(Task 2 净 diff 为零,无独立提交)
- **Files modified:** 1(`scripts/check-05-ui-uat.py`)+ 13 份新增日志

## Accomplishments

- **一条会静默死亡的断言被抓住并重新登记。** `check-05` 的 `[p1] .hint 实际背景 == <令牌>` 断言,其期望侧走 `resolve_color` 运行时解析;本阶段删掉了那个卡片底色令牌 ⇒ `resolve_color` 返回 `None` ⇒ `ok()` 在**期望侧为 `None`** 时记 **BLOCKED**(不是 FAIL)。`check-05` 的整体退出码本来就因两条 `--ai-smoke` 腿是 **2**,所以**门不会变红** —— 这条断言会从「在检查」静默退化成「不知道」。
- **退化先被复现,再改。** 改前实跑:`BLOCKED [p1] .hint 实际背景 == var(--color-surface-card): expected=<UNRESOLVED> actual=rgb(255, 255, 255)`、`item 5: BLOCKED (9 条断言,0 FAIL,3 BLOCKED)`、`exit=2`。BLOCKED 计数由 **2 变 3**,退出码**一动不动** —— 这就是「门绿着在看」的实测形态,不是推断。
- **期望侧换指统一面令牌,断言形式一字未变。** 改后该断言 `PASS expected=rgb(255, 255, 255) actual=rgb(255, 255, 255)`,`item 5` 的 BLOCKED 计数**回到 2**。断言函数仍是 `ok(...)` 的**精确等值**,实际侧仍是 `effective_bg(page, ".hint")`,**未**改成 `ok_contains` / 非透明判据 / 硬编码 rgb / `or` 分支,**未**删除该断言。
- **相邻注释改写为两段历史 + 一句关键线索。** 记下 Phase 9 把地面搬到卡片令牌、Phase 11 把卡片地面并回统一面 ⇒ 期望侧再次换指;并**新增**「`ok()` 在期望侧为 `None` 时记 BLOCKED,而本门退出码本来就是 2 ⇒ 门不会变红 ⇒ 断言会静默退化」这一句。
- **REG-03 复测完成。** `check-05 --item 8` → `PASS (13 条断言,0 FAIL,0 BLOCKED)`,余量由 HEAD 的 **`1.000px`** 变为 **`0.000px`**;成因机制已登记;容差字面量 `<= 1.0` 与 `frontend/style.css` 均**逐字未动**。
- **13 条门在最终树上复跑并落盘。** 五条浏览器门 `^FAIL` 计数**均为 0**;`check-05` 全量 `exit=2` 的成因集合仍**只是** item 5 的两条 `--ai-smoke` 腿;`pytest` **219 passed / 6 skipped**;两个探针各 `EXIT=0`。
- **连带指纹面在磁盘上逐份实测**:`frontend/style.css` 被 **11** 份列出、`scripts/check-09-idi09-validation.py` 被 **1** 份、`scripts/check-05-ui-uat.py` 被 **7** 份 —— **全部已是 fail-closed stale** ⇒ 本阶段**零新增作废**任何原本可执行的报告。

## Task Commits

| Task | 内容 | 提交 |
|---|---|---|
| Task 1 | `check-05` 的 `.hint` 实际背景断言期望侧重登记 | `747d5ff` (fix) |
| Task 2 | REG-03 复测与分诊 | **无独立提交**(计划默认路径零代码改动,纯取证 —— 见「Deviations」第 3 条) |
| Task 3 | 全门复跑 + 13 份原始日志落盘 | `56d62bf` (docs) |

**Plan metadata:** 见收尾的 docs 提交。

## ⚠ 与编排器指令 C-2 的偏离 —— 实际选择与理由(计划明令不得无声择一)

规划期收到的指令 **C-2** 写着「`scripts/check-05-ui-uat.py` **NOT** need modification. **Do not touch it.**」,**本计划采用了主路线(改了它)**,理由如下,逐条有实测背书:

| 判据 | 实测 |
|---|---|
| **C-2 漏掉了一条断言** | C-2 针对的是 `--item 8` 的 sticky 断言 —— 那条**确实不需要改**(它是容差,`0.000px` 仍通过,本计划确实一行都没动它)。但 `check-05` **还有**一条断言(`[p1] .hint 实际背景 == <令牌>`)的**期望侧**读的正是本阶段要删除的令牌 |
| **退化是实测的,不是推断的** | 改前实跑:`BLOCKED … expected=<UNRESOLVED> actual=rgb(255, 255, 255)`;`item 5: BLOCKED (9 条断言,0 FAIL,3 BLOCKED)`;**`exit=2` 不变** ⇒ 门不会变红 |
| **C-2 给出的成本理由已失效** | 规划期与执行期**各实测一次**,形状逐字一致:`check-05-ui-uat.py` 的覆盖者恰 **7** 份(`idi-04.1` / `idi-05` / `idi-06` / `idi-07` / `idi-08` / `idi-09` / `quick/260925-iin`),**7 份全部已是 fail-closed stale**(missing 8/12、8/11、8/10、6/9、6/10、6/10、2/7)⇒ 改它的**边际重验成本为零**。C-2 想避免的是「把 `idi-08` 拖进重验名单」,而 `idi-08` **本来就是** stale |
| **同文件同断先前例** | STATE.md 的 `[Phase idi-09]` 逐字记着对**同一行代码**的处置:「「重新登记」≠「放宽」—— `check-05` 的 `[p1] .hint 实际背景` 断言的期望侧由 `--color-surface` 换指 `--color-surface-card`,断言形式(与运行时解析值精确等值)一字未变」 |
| **替代路线(不推荐)** | 若裁定 C-2 优先:保留该断言不动、在 SUMMARY 登记它的静默退化(item 5 的 BLOCKED 由 2 变 3),并把这条登记交给 Phase 12 的 `REG-04`。本计划**未**走这条路 —— 本仓库的立场是「一条不能失败的门比没有门更糟」 |

**实际改动面(逐行核对):** `git diff -U0 -- scripts/check-05-ui-uat.py` 只有三处 —— 期望侧令牌名、标签文本、相邻注释块。`ok()` / `resolve_color()` / `effective_bg()` / `STATES` / `ITEMS` 与其它任何 item **一字未动**;`git diff --stat -- check-09 / check-02 / check-10 / style.css` 为空。

## 承重证据的原始输出(逐字抄录)

### Task 1 第 1 步 —— 退化复现(`--item 5 --browser bundled`,**改前**)

```
BLOCKED [p1] .hint 实际背景 == var(--color-surface-card): expected=<UNRESOLVED> actual=rgb(255, 255, 255)  # 令牌未声明或期望值解析失败

=== 逐项结论 ===
item 5: BLOCKED  (9 条断言,0 FAIL,3 BLOCKED)

exit=2  (0=全 pass,1=有 fail,2=有 blocked)
```

### Task 1 第 4 步 —— 恢复(`--item 5 --browser bundled`,**改后**)

```
PASS [p1] .hint 实际背景 == var(--color-surface-page): expected=rgb(255, 255, 255) actual=rgb(255, 255, 255)  # .hint 自身无背景,沿祖先链取到的实际底色

=== 逐项结论 ===
item 5: BLOCKED  (9 条断言,0 FAIL,2 BLOCKED)

exit=2  (0=全 pass,1=有 fail,2=有 blocked)
```

### Task 2 —— REG-03(`--item 8 --browser bundled`)

```
INFO item8 sticky 原始数值: scrollTop=4348 scrollHeight=5248 clientHeight=900 header={'top': 0, 'bottom': 34, 'left': 1009, 'right': 1440} panel={'top': 0, 'bottom': 900, 'left': 1008, 'right': 1440}

=== 逐项结论 ===
item 8: PASS  (13 条断言,0 FAIL,0 BLOCKED)

exit=0  (0=全 pass,1=有 fail,2=有 blocked)
```

## REG-03 —— sticky 余量的「改前 → 改后」与 D-11-16 分诊

| | HEAD(Phase 10 落盘基线) | 本阶段(最终树) | 机制 |
|---|---|---|---|
| `header.top` | `1` | **`0`** | sticky 元素被钳制在**滚动容器的 padding box** 上,其顶边离**边框盒** `border-top-width` 那么远 |
| `panel.top` | `0` | `0` | — |
| `abs(header.top - panel.top)` | **`1.000px`** | **`0.000px`** | 移除 `#doc-panel` 那条 1px **上**边框 ⇒ padding box 顶边抬到边框盒顶边 |
| `clientHeight` | `898` | **`900`** | 上下各 1px 边框被移除的直接后果 |
| `panel.right` | `1439` | **`1440`** | 右边框被移除(四边边框收成单边 `border-left`) |
| 判定 | `PASS`(`1.000 <= 1.0`,**余量为零**) | `PASS`(`0.000 <= 1.0`) | 断言是**容差**不是等值 |

**D-11-16 的「事实是否被改变」分诊 —— 结论:未被改变。**

- 该断言描述的事实是 **sticky 表头遮挡滚动正文**。本阶段改的是 `#doc-panel` 的**边框**与**底色**、`#main-pane` 的**横线**与 `gap`;`#doc-panel-header` 的 `position: sticky` / `top: 0` / `background` 三条**逐字未动**(波次 1 Task 2)⇒ **滚动正文仍从表头底下穿过,这件事没变**。
- 余量读数为什么变?**机制**:滚动容器的 padding box 顶边离边框盒 `border-top-width` 那么远;移除那条 1px 上边框把顶边对齐到边框盒顶边,故 `header.top - panel.top` 由 `1` 变为 `0`。这是**几何的如实变化**,不是回归。
- 因此处置是:**只更新余量读数与成因登记,判据本身不动。**
- **未回退任何产品改动:** `git diff --stat -- frontend/style.css` 为空;`git hash-object frontend/style.css` = `cfcaef098d957abc885413793cd8b1a9dc12193f`(与波次 1/2 定型值逐字符相同);容差字面量 `abs(hp["top"] - pp["top"]) <= 1.0` 命中于 `:2294`。**没有为了让旧数字继续成立而把 1px 上边框加回去。**

## Task 3 —— 13 份门日志与 Phase 10 基线的逐项并排对照

**日志清单(13 份,一个门一个):**

`check-01-token-conformance.log` / `check-02-contrast.log` / `check-03-hidden-uniqueness.log` / `check-04-important-count.log` / `check-05-full.log` / `check-06-idi05-validation.log` / `check-07-idi08-validation.log` / `check-09-idi09-validation.log` / `check-10-idi10-validation.log` / `pytest.log` / `node-check-app.log` / `probe-05-resolve-color.log` / `probe-07-focus-composite.log`。

**⚠ 磁盘上没有 `check-08`** —— 未为了对上清单去造一个。

### `=== 逐项结论 ===` 块逐项并排

| 门 / 项 | Phase 10 基线 | Phase 11(本阶段) | 判定 |
|---|---|---|---|
| check-05 `1` | `PASS (45)` | `PASS (45)` | 一致 |
| check-05 `2` | `PASS (5)` | `PASS (5)` | 一致 |
| check-05 `3` | `PASS (17)` | `PASS (17)` | 一致 |
| check-05 `4` | `PASS (65)` | `PASS (65)` | 一致 |
| check-05 `5` | `BLOCKED (9, 2 BLOCKED)` | **`BLOCKED (9, 2 BLOCKED)`** | 一致(且**不是 3** —— 这正是 Task 1 要消除的形态) |
| check-05 `6` | `PASS (6)` | `PASS (6)` | 一致 |
| check-05 `7` | `PASS (38)` | `PASS (38)` | 一致 |
| check-05 `8` | `PASS (13)` | **`PASS (13)`** | 一致(读数变,判据未变) |
| check-05 `9` | `PASS (17)` | `PASS (17)` | 一致 |
| check-05 `10` | `PASS (42)` | `PASS (42)` | 一致 |
| check-05 退出码 | `exit=2` | `exit=2` | 一致(成因集合仍只是 item 5 的两条 `--ai-smoke` 腿) |
| check-06 `g1..g6` | `9 / 2 / 12 / 5 / 5 / 7` | `9 / 2 / 12 / 5 / 5 / 7` | 一致 |
| check-07 `g1..g4` | `21 / 39 / 10 / 3` | `21 / 39 / 10 / 3` | 一致 |
| check-09 `c1..c5` | *(Phase 10 未跑该门)* | `59 / 17 / 6 / 20 / 5`,`exit=0` | 与波次 3 改写后的读数逐字一致 |
| check-10 `t1/t2/r1/r2` | `58 / 51 / 11 / 10` | `58 / 51 / 11 / 10` | 一致 |
| check-10 `shot` | `PASS (7)` | **不在运行中** | 见「Deviations」第 2 条(命令行选择项,非缺口) |
| 静态门 check-01..04 | `PASS` / exit 0 | `PASS` / exit 0 | 一致 |
| pytest | `219 passed, 6 skipped` | **`219 passed, 6 skipped`** | 一致(用项目 `.venv`) |
| `node --check frontend/app.js` | 无输出 / exit 0 | 无输出 / exit 0 | 一致 |
| probe-05 / probe-07 | 各 `EXIT=0` | 各 `EXIT=0`;probe-07 地面 `rgb(255, 255, 255)`、比值 `3.54` | 一致(统一面仍是白 ⇒ 比值不变) |

**`^FAIL` 计数(五条浏览器门日志,判据为行首 verdict 形态):全为 `0`。**

### 读数变化的逐处分诊(归一化剥临时路径后的逐行 diff)

> 判据:任何 FAIL 或**新增** BLOCKED 都是缺口;断言计数或**读数**变化允许,但必须有机制解释。**实测零 FAIL、零新增 BLOCKED**;所有变化行的 verdict 两侧都是 `PASS`(机器核对:`grep -E '^[<>] (FAIL|BLOCKED)'` 在 check-05 的 172 行 diff 上为空)。

| 门 | 变化处 | 改前 → 改后 | 机制 |
|---|---|---|---|
| check-05 | `.hint 实际背景` 断言的标签 | `var(--color-surface-card)` → `var(--color-surface-page)` | Task 1 的重新登记(期望值两侧均为 `rgb(255, 255, 255)`,未变) |
| check-05 | item8 sticky | `header.top 1→0`、`clientHeight 898→900`、`scrollTop 4350→4348`、`panel.right 1439→1440` | 移除 `#doc-panel` 的 1px 上/右/下边框(REG-03 的登记对象) |
| check-05 | item8 badge×banner rect(3 个宽度) | badge `left +1`、`top -1` | `#doc-panel` 去掉 1px 右边框 ⇒ `#main-pane`(flex 兄弟)宽 +1px ⇒ 居中列整体右移 1px;`gap` 归零 + 容器边框移除使纵向基线 -1px |
| check-05 | item8/9/10 的 L-5 clearance 与 L-6 命中区(共 56 行) | 1px 级位移(如 `#message-input` clearance `137.0→136.0`、rect `left 137→136` `width 664→666`) | 同上(1px 级几何位移);**全部仍 PASS**,无一项跌破阈值 |
| check-05 | item8 `[static] L-2 守卫形态` | `@media` 命中行 `[1910]` → `[2015]` | 波次 1/2 在 `style.css` 增删了行 ⇒ 同一处声明的**行号**移动,**计数仍为 1** |
| check-02 | 六条页面地面 PAIR 的比值 | `14.30 / 5.19 / 5.19 / 5.15 / 5.19 / 4.18` → `16.29 / 5.92 / 5.92 / 5.87 / 5.92 / 4.77` | 波次 1 把统一面换值为白 ⇒ 白面更亮 ⇒ 深色前景对比度上升(Wave 2 已登记的重算) |
| check-02 | 两条重归属 PAIR 的地面标签 | `--color-surface-card` → `--color-surface-page` | 波次 2 的重归属;**比值不变**(4.77 / 3.32),因两地面同值(白) |
| check-06 | g3 的 `radiusTL` / `scrollW` / `clientW` | `10px → 0px`;`766 → 768` | D-11-7 的圆角归零;四个 section 各去掉 1px 左右边框 ⇒ 内容宽 +2px。**全部仍 PASS**(`scrollW<=clientW` 两侧同增) |
| check-06 | g5 的 `bodyClientW` | `338 → 339` | 同上(1px 级);断言 `<=338px → <=339px` 是**期望值随实测面同步**,实际 `178px` 远低于阈值 |
| check-10 | `shot` 项整块 | 存在 → 不在运行中 | 见「Deviations」第 2 条 |
| 其它 | check-01/03/04/07、两个探针 | 仅 `[gsd] EXIT=` 行或末尾空行的差异 | 日志格式差异(本阶段每份都附退出码),无内容变化 |

**一条必须留档的对照结论:** Phase 10 的「本阶段零布局改动」措辞曾比事实更强(实测矮 3px)。本阶段**没有**写这类措辞 —— 每一处几何变化都由**同一次导航内的运行时读数**给出并附机制,不靠推断。

## 连带指纹面 —— 磁盘实测表(Phase 12 `REG-04` 的输入)

**判据:** 解析 `.planning/**` 下每份 `*VERIFICATION.md` / `*UAT.md` 的 frontmatter `covered_files`(**逐行匹配路径**,**不是**全文 grep),并**额外测「其 `covered_files` 里的每个路径是否还在盘上」**。扫描到 **20** 份报告。

| 本阶段改动的文件 | `covered_files` 列出它的报告数 | 其中可执行 | 其中 fail-closed stale |
|---|---|---|---|
| `frontend/style.css` | **11** | **0** | **11** |
| `scripts/check-09-idi09-validation.py` | **1** | **0** | **1** |
| `scripts/check-05-ui-uat.py` | **7** | **0** | **7** |

**逐份明细(报告路径 / 状态 / covered 条数 / 缺失条数):**

| 报告 | 状态 | covered | missing |
|---|---|---|---|
| `v1.13-phases/idi-01-1-2/01-VERIFICATION.md` | fail-closed stale | 41 | 12 |
| `v1.13-phases/idi-02-g2/02-VERIFICATION.md` | fail-closed stale | 26 | 11 |
| `v1.13-phases/idi-03-g3/03-VERIFICATION.md` | fail-closed stale | 31 | 13 |
| `v1.14-phases/idi-04-tokens-contract/idi-04-VERIFICATION.md` | fail-closed stale | 13 | 8 |
| `v1.14-phases/idi-04.1-radix/idi-04.1-VERIFICATION.md` | fail-closed stale | 12 | 8 |
| `v1.14-phases/idi-05-…/idi-05-VERIFICATION.md` | fail-closed stale | 11 | 8 |
| `v1.14-phases/idi-06-…/idi-06-VERIFICATION.md` | fail-closed stale | 10 | 8 |
| `v1.14-phases/idi-07-…/idi-07-VERIFICATION.md` | fail-closed stale | 9 | 6 |
| `v1.14-phases/idi-08-…/idi-08-VERIFICATION.md` | fail-closed stale | 10 | 6 |
| `v1.15-phases/idi-09-card-containers/idi-09-VERIFICATION.md` | fail-closed stale | 10 | 6 |
| `v1.15-phases/idi-10-…/idi-10-VERIFICATION.md` | fail-closed stale | 11 | 9 |
| `quick/260925-iin-…/260925-iin-VERIFICATION.md` | fail-closed stale | 7 | 2 |

**结论:** 规划期实测的形状(11 / 1 / 7,全部 stale)**在执行期逐字复现** ⇒ 本阶段**不新制作废**任何原本可执行的报告;改 `check-05` 的**边际重验成本确实为零**(含 C-2 想避免的 `idi-08` —— 它本来就是 stale,missing 6/10)。

**⚠ `REG-04` 的正式处置归 Phase 12。** 本步只**实测并登记**:**未**刷新任何指纹、**未**做「以 HEAD 内容重新验证」。本节即 Phase 12 `REG-04` 的输入。

## 仓库卫生(逐条实测)

| 判据 | 实测 |
|---|---|
| `git status --porcelain frontend/ scripts/ backend/` | **空**(三个任务的改动均已原子提交) |
| `git diff --name-only 6afe679..HEAD -- frontend/ scripts/ backend/` | **仅** `frontend/style.css` / `scripts/check-05-ui-uat.py` / `scripts/check-09-idi09-validation.py`(波次 3 的 check-09 已在波次 3 提交) |
| `git diff --stat 6afe679..HEAD -- frontend/app.js frontend/index.html backend/ frontend/vendor/` | **空** |
| `git hash-object frontend/style.css` | `cfcaef098d957abc885413793cd8b1a9dc12193f`(与波次 1/2 定型值逐字符相同) |
| `git diff --stat -- frontend/style.css` | **空**(本计划零产品改动) |
| `ls frontend/vendor/` | 仅 `marked.min.js` |
| `grep -o '/\* PAIR' frontend/style.css \| wc -l` | **53** |
| `grep -o '/\* ORDER' frontend/style.css \| wc -l` | **1** |
| `git status --porcelain .planning/phases/idi-11-…/` | 仅 `gate-logs/`(已提交);无其它未跟踪产物 |
| 一次性解析脚本的落点 | 系统临时目录(`mktemp -d`),**未落进仓库树**;`rm` 被本仓库权限系统拒绝,已就地清空其内容(与 `idi-11-01` 偏差第 3 条同型) |

## Decisions Made

- **采用主路线改 `check-05` 的期望侧**(理由与实测证据见上「与 C-2 的偏离」一节),并按 Phase 9 的同一纪律保持**断言形式一字未变**。
- **REG-03 的分诊结论是「事实未被改变」** ⇒ 只更新读数与成因登记,判据不动;容差 `<= 1.0` 与 `frontend/style.css` 均逐字未动,**未回退任何产品改动**。
- **`gate-logs/` 按 Phase 10 同形落盘 13 份**,每份附 `[gsd] EXIT=N`(Phase 10 的部分日志没有该行,本阶段统一补齐,使退出码与 stdout 同处一份)。
- **连带指纹面只实测并登记**,不做重验、不刷指纹(`REG-04` 归 Phase 12)。
- **跨阶段对照取归一化后的逐行 diff**,不取「结论块看着一样」—— 正是这个粒度捞出了计划未点名的 check-06 几何位移(766→768 / 338→339)。

## Deviations from Plan

### 1. [Rule 1 - 计划验收措辞与执行模型不符] `git status --porcelain` 在原子提交下为空

- **Found during:** Task 1 与 Task 3 的收口
- **Issue:** 计划的 verify 写「`git status --porcelain frontend/ scripts/ backend/` 只应列出 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`」,`fails_when` 把**空输出也判失败**。该措辞假设任务的改动**未提交**;而执行器协议要求**每个任务原子提交** ⇒ 工作树是干净的。
- **Fix:** **不改任何代码**。改以**计划区间的 diff** 证明同一实质且更强:`git diff --name-only 6afe679..HEAD -- frontend/ scripts/ backend/` 输出恰三个文件(其中 `check-09` 由波次 3 提交),`git diff --stat 6afe679..HEAD -- frontend/app.js frontend/index.html backend/ frontend/vendor/` 为空。工作树干净 + 计划区间单文件集合 = 计划想要的结论成立。
- **Files modified:** 无
- **Verification:** 见「仓库卫生」表;与 `idi-11-02` 偏差第 3 条、`idi-11-03` 偏差第 2 条同型。
- **Committed in:** 无独立提交(证据在本 SUMMARY)

### 2. [Rule 1 - 计划基线表与计划命令不符] `check-10` 的 `shot: 7` 项不在默认运行中

- **Found during:** Task 3 的逐项对照
- **Issue:** 计划的**对照基线表**把 `check-10` 记为 `t1: 58 / t2: 51 / r1: 11 / r2: 10 / **shot: 7**`,但同一计划的 **Task 3 命令表**写的是 `.venv/bin/python scripts/check-10-idi10-validation.py`(不带 `--screenshot`)。Phase 10 的日志里 `shot` 存在,是因为它当时传了 `--screenshot <DIR>`(VIS-01 的 5 张整窗截图)。
- **Fix:** **不改任何代码、不擅自扩范围**。按计划 Task 3 的命令表运行(不传 `--screenshot`)⇒ `shot` 项按设计不在本次运行中。**这不是 FAIL、不是新增 BLOCKED,是命令行选择项**:`--screenshot` 属 Phase 12 的 `VIS-01`,现在跑会往阶段目录写 5 张 PNG(VIS-01 的交付物),那是范围外产物。被比较的 `t1/t2/r1/r2` 四项读数与退出码**逐字一致**。
- **Files modified:** 无
- **Verification:** `check-10-idi10-validation.log` 的 `=== 逐项结论 ===` 块含 `t1/t2/r1/r2` 四项,`exit=0`;与 Phase 10 同名日志的 diff 仅 16 行,全部是 `shot` 块。
- **Committed in:** 无独立提交(证据在本 SUMMARY)

### 3. [过程偏差 - Task 2 无独立提交] Task 2 的净 diff 为零

- **Found during:** Task 2 的收口
- **Issue:** 协议要求「每个任务原子提交」。Task 2(REG-03 复测与分诊)按计划的**默认路径**是**零代码改动** —— 计划明写「本任务默认零代码改动」「本任务不得引入新的改动」,故工作树无可提交的内容。
- **Fix:** **不改任何代码、不为凑提交而制造改动**。如实登记:Task 2 的交付物是**读数与分诊结论**(本 SUMMARY 的「REG-03」一节),净 diff 为零 ⇒ 无独立提交 —— 与 `idi-11-02` 的 Task 3、`idi-11-03` 的 Task 2/3(纯取证、无独立提交)同型。
- **Impact:** 对仓库最终状态**零影响**。影响面仅限于「按提交粒度做二分定位」时 Task 2 不可分。
- **Files modified:** 无
- **Verification:** `git rev-list --count 4564195..HEAD` = **2**(仅 Task 1 与 Task 3);`git diff --stat -- scripts/check-05-ui-uat.py` 在 Task 2 收口时为空。
- **Committed in:** 无独立提交

### 4. [过程偏差 - 临时解析脚本无法用 `rm` 删除]

- **Found during:** Task 3 第 3 步(连带指纹面实测)
- **Issue:** 威胁模型 T-idi-11-21 要求一次性解析脚本「落在系统临时目录并随即删除」。`rm` 被本仓库权限系统拒绝(与 `idi-11-01` 偏差第 3 条、STATE.md 记录的 `git rm` 被拒同型)。
- **Fix:** 就地清空该文件内容(改写为一行说明),使其不再是可执行脚本。文件位于**系统临时目录**,从未落进仓库树(`git status --porcelain` 的已跟踪路径改动只有 `scripts/check-05-ui-uat.py`)。
- **Files modified:** 无(仓库外)
- **Verification:** `git status --porcelain .planning/phases/idi-11-…/` 仅 `gate-logs/`。
- **Committed in:** 无独立提交

---

**Total deviations:** 4(2 × Rule 1「计划措辞/基线表与磁盘事实或执行模型不符」+ 2 × 过程偏差)
**Impact on plan:** **零范围扩张、零判据放宽、零产品改动。** 四条都不改变交付物:`.hint` 断言已重新登记且不再 BLOCKED、REG-03 已复测并登记、13 条门零新增失败。两条 Rule 1 都是**计划措辞的实测更正**,且各自另给了更强的替代证据。

## Issues Encountered

- **`check-05` 的 `exit=2` 是设计如此,不是回归。** 成因集合仍**只是** item 5 的两条 `--ai-smoke` 腿(需真实 AI 调用,默认不执行)。item 5 的 BLOCKED 计数在 Task 1 之前是 **3**(多出来的那条正是被删令牌造成的静默退化),Task 1 之后**回到 2**。
- **端口 8765 上有一个既有的 uvicorn 进程**,`ensure_server()` 复用了它(未新起、结束时也未关闭),与既有阶段的门运行方式一致。所有浏览器门与探针的读数均取自它。
- **`check-09` 在 Phase 10 的 `gate-logs/` 里没有基线**(该门当时未跑)⇒ 本阶段的对照基线取波次 3 改写后的读数(c1 59 / c2 17 / c3 6 / c4 20 / c5 5),**逐字一致**。
- **本计划**未**使用 `gsd-tools windows append`** —— 三条任务的 `<verify>` **全部实际执行过**,没有留下 stub / skipped-test / unrun-verify 类缺陷(见下节)。

## Known Stubs

None。本计划不产生任何 stub:零新增 CSS 自定义属性、零新增颜色值、零新增 PAIR / ORDER 条目、零新依赖、零占位文案、零 `t.skip` / `test.todo`。

**一条不构成 stub 的既有事实(登记以并入跨阶段缺陷视野):** `ok()` 在**期望侧为 `None`** 时记 BLOCKED(而非 FAIL)是**已注册的项目缺陷**(PROJECT.md / MEMORY 索引)。本计划只处置了**它自己这一条**会因此静默死亡的断言 —— **未**修 `ok()` 本身,也**未**顺手补通用守卫(那是 G2,已明确排除在 v1.16 范围外)。

## Threat Flags

None。本计划只改一个**只读的本地运行时门脚本**的一处期望侧,并跑既有的门与探针:零用户输入处理、零鉴权、零数据访问、零网络调用、零新增资源加载。威胁模型的六条缓解均已落地并被判据覆盖:

- **T-idi-11-17(「零新增失败」缺少可复核的原始证据,high)** → 13 份原始输出与退出码落盘;与 Phase 10 基线逐项并排对照;判据是 `^FAIL` 计数为 0 与逐项计数,不是「看着一样」。
- **T-idi-11-18(`check-05` 的改动面可能越界,high)** → 唯一理由已实测(退化先复现);覆盖者**全部**已是 fail-closed stale ⇒ 零边际成本;`git diff -U0` **逐行人工核对**限定为「期望侧令牌名 + 标签文本 + 相邻注释」三处;断言形式判据是「仍是 `ok(...)` 的精确等值」。
- **T-idi-11-19(为迁就旧数字而回退产品改动,high)** → D-11-16 的分诊规则逐字执行;`git diff --stat -- frontend/style.css` 为空;`git hash-object` 与定型值逐字符相同;容差字面量 `<= 1.0` 逐字未改。
- **T-idi-11-20(`REG-04` 越界,medium)** → 只实测与登记,任务文本与验收都明写「不得刷新任何指纹、不得做以 HEAD 内容重新验证」;记录标注为 Phase 12 `REG-04` 的输入。
- **T-idi-11-21(一次性解析脚本的落点,low)** → 脚本落系统临时目录、跑完清空;`git status --porcelain` 的已跟踪路径改动只有 `scripts/check-05-ui-uat.py`。
- **T-idi-11-SC(安装,low)** → 零安装、零新增依赖;`ls frontend/vendor/` 仅 `marked.min.js`。

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **REG-03 已关闭。** `check-05 --item 8` 复跑 `PASS`,余量新读数(`0.000px`)与成因机制已登记,判据与产品代码均未回退。**STATE.md 的 `## Blockers/Concerns` 里那条「sticky 断言余量为零」的 Open 条目描述的就是本次复测的读数,已由本计划处置。**
- **Phase 11 的四条计划全部完成** ⇒ 可进入阶段验证(`/gsd-verify-work 11`)。本阶段 9 条需求(SURF-01/02/03 + DIV-01/02/03 + REG-01/02/03)的计划均已产出 SUMMARY。
- **Phase 12 的 `REG-04` 输入已就绪:** 连带指纹面的实测表(11 / 1 / 7,全部 fail-closed stale)在本 SUMMARY 的「连带指纹面」一节。`REG-04` 的全量复跑必须落在**最后一次 `style.css` 改动之后** —— 本计划是那之后的一次复跑,13 份日志可直接作为基线。
- **`check-09` 的基线缺口已登记:** Phase 10 未跑该门 ⇒ 跨阶段对照对 `check-09` 只能取波次 3 的读数。
- **`check-10 --screenshot`(VIS-01)留给 Phase 12** —— 现在跑会往阶段目录写 5 张 PNG,那是 Phase 12 的交付物。
- **无阻塞项。**

---
*Phase: idi-11-decard-and-hairline-dividers*
*Completed: 2026-09-28*

## Self-Check: PASSED

- `scripts/check-05-ui-uat.py` — FOUND(本计划唯一改动的源码文件)
- `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/` — FOUND(13 份日志)
- `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-04-SUMMARY.md` — FOUND
- Commit `747d5ff` — FOUND
- Commit `56d62bf` — FOUND
- `commits` 实测 = `git rev-list --count 4564195c868ad68531650ea4c848e532a353dd55..HEAD` = 2(与 frontmatter 的 `actuals.commits: 2` 一致;Task 2 净 diff 为零,无独立提交)

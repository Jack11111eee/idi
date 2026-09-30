---
phase: idi-12-g1-band
plan: 02
subsystem: testing
tags: [playwright, computed-style, screenshots, g1-header-band, vis-01, runtime-gate]

# Dependency graph
requires:
  - phase: idi-12-g1-band (plan 01)
    provides: "#latest-check host ground rewritten to var(--color-surface-page); `checking` fixture carrying the `## 问题分级` table; check-09 item c6"
provides:
  - "check-09 的第四个 CLI 参数 `--g1-snapshot DIR` 与 `g1_snapshot()` 函数:在 `checking` 样本上对 `#latest-check` 取元素级局部特写,并断言表头存在、落在 30vh 可视区内、PNG 宽高非零"
  - "VIS-01 的 5 张 1440×900 整窗人眼取证图(p1 / p12 / p3 / checking / archive),与 v1.15 先例同规格同文件名"
  - "G1-01 的局部特写 screenshots/latest-check/latest-check.png(独立子目录落点)"
affects: [idi-12-g1-band plan 03 (REG-04 全量复跑与连带面处置), /gsd-verify-work idi-12-g1-band]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
# tokens 只覆盖**文本 diff**(check-09 的 +82/-1 行);6 张 PNG 是二进制,chars/4 对它无意义。
actuals:
  tokens: 1425
  tasks: 2
  commits: 2

# Ledger fields at column 0 (#3968 / Wave-1 lesson): verify-work extracts these with
# `^commits:` / `^plan_head_before:` anchored greps — the nested `actuals:` block does NOT satisfy them.
commits: 2
plan_head_before: 04f146194e13f759780e12daa8ea770a80e6136e

tech-stack:
  added: []
  patterns:
    - "专用 CLI 参数 + 独立子目录承载元素级局部特写(照 check-10 的 --radius-snapshot 先例),使既有的「--screenshot 目录恰含 5 个 PNG」断言一字不动"
    - "三条可失败的取证断言:表头存在(count >= 1)→ 表头矩形落在宿主矩形内(30vh 滚动区)→ 元素截图宽高非零;把「截图落盘成功」与「band 拍到了」分开"

key-files:
  created:
    - .planning/phases/idi-12-g1-band/screenshots/p1.png
    - .planning/phases/idi-12-g1-band/screenshots/p12.png
    - .planning/phases/idi-12-g1-band/screenshots/p3.png
    - .planning/phases/idi-12-g1-band/screenshots/checking.png
    - .planning/phases/idi-12-g1-band/screenshots/archive.png
    - .planning/phases/idi-12-g1-band/screenshots/latest-check/latest-check.png
  modified:
    - scripts/check-09-idi09-validation.py

key-decisions:
  - "局部特写走**专用参数 + 独立子目录**(`--g1-snapshot` 收一个 DIR,图写到该 DIR 下的 latest-check.png;调用时 DIR 取 .planning/phases/idi-12-g1-band/screenshots/latest-check),而不是写进 `--screenshot` 的目录顶层 —— 顶层多一张会让既有的「恰含 5 个 PNG」断言变红,而放宽它属仓库明令禁止的「把门改小」"
  - "`g1_snapshot()` 三条断言全走 `ok_true`(期望侧是布尔条件),失败即 FAIL:表头存在、表头矩形落在 `#latest-check` 矩形之内(0.5px 浮点容差)、PNG 宽高非零;复用既有 `png_size()`,零新增读图工具"
  - "派发顺序照 check-10:`--g1-snapshot` 在 `--screenshot` **之前**,两者各自独立;`summary` 里追加 `\"g1-snapshot\"` 使它的结论行一定被打印(取证失败必须让门红,不能静默)"
  - "本计划**零改动渲染面**(`frontend/**` 与 `checking` fixture 逐字节未动),故 5 张整窗图与局部特写拍的是同一次最终态"

patterns-established:
  - "局部特写独立落点:元素级截图不与被断言的整窗图目录共用顶层"

requirements-completed: [VIS-01]

# Coverage metadata (#1602) — one entry per shipped deliverable.
coverage:
  - id: D1
    description: "5 张 1440×900 整窗人眼取证图(p1 / p12 / p3 / checking / archive),文件名与 v1.15 先例逐字相同"
    requirement: "VIS-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --screenshot .planning/phases/idi-12-g1-band/screenshots → item shot: PASS (7 条断言,0 FAIL,0 BLOCKED)"
        status: pass
    human_judgment: true
    rationale: "机械半边(恰好 5 个文件名、各 1440×900、字节非零)已由门断言;而「分块割裂感已消除」这条主张本身是屏幕级人眼判断,自动化无法替代"
  - id: D2
    description: "G1-01 的局部特写 screenshots/latest-check/latest-check.png(`checking` 样本上 `#latest-check` 的元素截图,画面含表头 band)"
    requirement: "VIS-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c6 --g1-snapshot .planning/phases/idi-12-g1-band/screenshots/latest-check → item g1-snapshot: PASS (3 条断言,0 FAIL,0 BLOCKED)"
        status: pass
    human_judgment: true
    rationale: "band 在 1440×900 整窗图里只占几十像素,局部图才是 G1-01 的直接人眼证据;机械半边(表头 count=5、表头矩形落在 30vh 可视区内、PNG 736×270 非零)已断言,「表头读作一条独立 band」的观感需人眼确认"
  - id: D3
    description: "check-09 的 `--g1-snapshot DIR` 参数与 `g1_snapshot()` 函数(表头存在 / 表头落在可视区内 / 元素截图非空三条断言)"
    verification:
      - kind: e2e
        ref: "同上 --item c6 --g1-snapshot 运行 → exit=0"
        status: pass
    human_judgment: false
  - id: D4
    description: "既有的「--screenshot 输出目录恰含 5 个 PNG」断言逐字保留且仍 PASS"
    verification:
      - kind: other
        ref: "grep -cF -- 'shot 输出目录恰含 5 个 PNG' scripts/check-09-idi09-validation.py → 1;同一次运行的 item shot: PASS"
        status: pass
    human_judgment: false

duration: 6min
completed: 2026-09-29
status: complete
---

# Phase 12 Plan 02: VIS-01 截图与 G1 局部特写 Summary

**check-09 获得独立的 `--g1-snapshot DIR` 参数与元素级 `#latest-check` 局部特写(表头存在 + 落在 30vh 可视区内 + PNG 非零三条断言),并在同一棵最终态树上产出 5 张 1440×900 整窗图与 1 张局部图;既有的「--screenshot 目录恰含 5 个 PNG」断言一字未动且仍 PASS。**

## Performance

- **Duration:** 6 min
- **Started:** 2026-09-29T07:47:31Z
- **Completed:** 2026-09-29T07:53:40Z
- **Tasks:** 2 completed
- **Files modified:** 7(1 个脚本 + 6 张 PNG;脚本 +82/−1 行)

## Accomplishments

- **VIS-01 的屏幕级证据全部落盘**:5 张 1440×900 整窗图(`p1` / `p12` / `p3` / `checking` / `archive`),文件名与 v1.15 两个阶段先例逐字相同,全部走**既有** `--screenshot` 路径 —— 零新 harness、零新增依赖、零构建步骤。
- **G1-01 的直接人眼证据落盘**:`.planning/phases/idi-12-g1-band/screenshots/latest-check/latest-check.png`(`checking` 样本上 `#latest-check` 的元素截图,736×270)。
- **落位硬约束以「专用参数 + 独立子目录」满足**:局部图不落进 5-PNG 目录顶层,既有的「恰含 5 个 PNG」断言**逐字保留**(`grep -cF` = 1)且在同一次运行里仍 PASS。
- **把「截图落盘成功」与「band 拍到了」分开**:`g1_snapshot()` 断言 `#latest-check th` 计数 >= 1 且表头矩形落在宿主矩形**之内** —— `max-height: 30vh` 使宿主是滚动区,表落在可视区外时截图照样会「成功落盘」,这条判据让该形态可失败。
- **渲染面零改动**:`frontend/**` 与 `scripts/ui-states/checking/docs/DESIGN-check-2.md` 逐字节未动,故 5 张整窗图与局部特写拍的是同一次最终态。

## 落盘读数抄录(盘上实测,不采信「命令退 0 所以图没问题」)

`.planning/phases/idi-12-g1-band/screenshots/` **顶层**恰 5 个 PNG(`glob("*.png")` 不递归 ⇒ 子目录不计入):

| 文件 | 宽×高 | 字节数 |
|---|---|---|
| `p1.png` | 1440×900 | 86,609 |
| `p12.png` | 1440×900 | 121,583 |
| `p3.png` | 1440×900 | 124,205 |
| `checking.png` | 1440×900 | 75,024 |
| `archive.png` | 1440×900 | 122,876 |

**子目录**局部特写:`.planning/phases/idi-12-g1-band/screenshots/latest-check/latest-check.png` —— PNG 签名 `True`,宽高 `(736, 270)`,字节数 25,737。

**两处落点的分工与各自目的:**

- **5 张整窗图 = 「分块割裂感已消除」的人眼取证**(VIS-01 本体):它们证明的是**整站**在同一帧里的分区观感(统一面 + 发丝分隔线),是屏幕级主张的唯一证据。
- **1 张局部特写 = G1-01 的 band 直接证据**(D-12-9):band 在 1440×900 整窗图里只占几十像素,整窗图上看不出「表头读作独立 band」;局部图把 `#latest-check` 单独框出来,画面里含 `| 编号 | 级别 | 位置 | 问题 | 建议修法 |` 表头行与数据行。

## Task Commits

Each task was committed atomically:

1. **Task 1: 给 check-09 加专用参数 `--g1-snapshot DIR`** — `6e9e43d` (feat)
2. **Task 2: 产出 5 张整窗图 + 1 张局部特写,并在盘上逐张取证** — `351be8f` (docs)

**Plan metadata:** `(本提交)` (docs: complete plan)

## Files Created/Modified

- `scripts/check-09-idi09-validation.py` — 新增第四个参数 `--g1-snapshot DIR`(`metavar="DIR"`,既有三个参数逐字不变)、新函数 `g1_snapshot(page, out_dir, tmp_root)`、`main()` 里在 `--screenshot` **之前**的独立派发、`summary` 追加 `"g1-snapshot"`、docstring 映射表新行与运行方式新示例。`run_screenshots()` 与那条「恰含 5 个 PNG」断言**一字未动**。
- .planning/phases/idi-12-g1-band/screenshots/{p1,p12,p3,checking,archive}.png — VIS-01 的 5 张整窗人眼取证图。
- `.planning/phases/idi-12-g1-band/screenshots/latest-check/latest-check.png` — G1-01 的局部特写(独立子目录落点)。

## Gate Evidence

同一次运行(`--screenshot ... --g1-snapshot ...`,未给 `--item` ⇒ 全量项)的原始结论块:

```
=== 逐项结论 ===
item c1: PASS  (59 条断言,0 FAIL,0 BLOCKED)
item c2: PASS  (19 条断言,0 FAIL,0 BLOCKED)
item c3: PASS  (6 条断言,0 FAIL,0 BLOCKED)
item c4: PASS  (39 条断言,0 FAIL,0 BLOCKED)
item c5: PASS  (5 条断言,0 FAIL,0 BLOCKED)
item c6: PASS  (7 条断言,0 FAIL,0 BLOCKED)
item g1-snapshot: PASS  (3 条断言,0 FAIL,0 BLOCKED)
item shot: PASS  (7 条断言,0 FAIL,0 BLOCKED)

exit=0  (0=全 pass,1=有 fail,2=有 blocked)
```

`g1_snapshot()` 的原始读数(stdout 抄录):

```
INFO g1-snapshot #latest-check 计算 background-color 原始读数: rgb(255, 255, 255)
INFO g1-snapshot #latest-check th 计算 background-color 原始读数: rgb(249, 249, 249)
INFO g1-snapshot #latest-check th 元素计数原始读数: 5
INFO g1-snapshot #latest-check bounding_box: {'x': 136, 'y': 90, 'width': 736, 'height': 270}
INFO g1-snapshot #latest-check th.first bounding_box: {'x': 145, 'y': 203.65625, 'width': 48, 'height': 31.25}
PASS [checking] #latest-check 元素截图落盘且宽高非零: ... actual=736x270
```

表头底边 203.65625 + 31.25 = 234.90625 ≤ 宿主底边 90 + 270 = 360,且顶边 203.65625 ≥ 90 —— 表头确实落在 30vh 可视带内。

**源码侧判据(逐条实测):**

| 判据 | 实测 |
|---|---|
| grep -cF -- 'shot 输出目录恰含 5 个 PNG' scripts/check-09-idi09-validation.py | 1(逐字保留、未复制、未删除) |
| grep -n 'add_argument' scripts/check-09-idi09-validation.py | 恰四个:--item / --screenshot / --g1-snapshot / --keep |
| `git status --porcelain frontend/` | 空(截图拍在最终渲染面上) |
| `git status --porcelain -- scripts/ ':(exclude)scripts/.check09-old.py'` | 空(唯一改动 `scripts/check-09-idi09-validation.py` 已提交) |
| `git diff --diff-filter=D --name-only HEAD~1 HEAD`(两次任务提交) | 空(无意外删除) |

## Decisions Made

- **局部特写的落点 = 专用参数 + 独立子目录**,而非把第 6 张图丢进 `--screenshot` 目录顶层。判据来自 D-12-9 的落位硬约束:顶层多一张会让既有的「恰含 5 个 PNG」断言变红,而放宽它属「把门改小」。形态照 `check-10` 的 `--radius-snapshot LABEL DIR` 先例(声明在 `:682-686`、派发在 `:730-732`)。
- **三条断言全走 `ok_true`**:期望侧是布尔条件(计数 / 矩形包含 / 宽高非零),失败即 FAIL;`ok()` 的 `None` 期望侧会降级成 BLOCKED(exit 2,本项目当良性码),不适用。
- **矩形包含判据取** `th.first.bounding_box()` 的上下边落在 `#latest-check.bounding_box()` 之内,0.5px 浮点容差。垂直包含是承重半边(30vh 滚动区),横向由嵌套结构天然满足(实测 th.x=145 ≥ host.x=136,且 th 宽 48 远小于宿主宽 736)。
- **`--item` 帮助文本未改**:它仍写「c1 / c2 / c3 / c4 / c5」(波次 1 加 c6 时未同步),但计划明确要求「既有三个的帮助文本与 `default` 逐字不变」—— 故不动它,不属本计划的改动面。

## Deviations from Plan

None - plan executed exactly as written.

两次任务提交均无意外删除(`git diff --diff-filter=D` 为空)。局部特写在 Task 2 重跑后与 Task 1 提交的副本**逐字节相同**(`git status` 无 diff),即该元素截图对同一次最终态是确定性的。

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Known Stubs

None. 本计划只新增一个门参数/函数与 6 张取证图,未引入任何硬编码空值、占位文案或未接线的数据源。

## Threat Flags

None. 本计划未新增网络端点、认证路径、文件访问模式或信任边界上的 schema 变更。威胁登记 T-12-06…T-12-09 的缓解均已落地:局部特写独立落点(T-12-06)、表头存在 + 可视区内双断言(T-12-07)、新项进 `summary` 使结论行必打印(T-12-08)、渲染面零改动 + `<verify>` 断言 `frontend/` 工作树为空(T-12-09)。

## Next Phase Readiness

- **Plan 03(REG-04 全量复跑与连带面处置)就绪**:本计划的产物(`check-09` 的新参数与 6 张图)已提交;`frontend/` 与 `scripts/` 工作树干净,`git status` 只剩三条与本计划无关的既有未跟踪条目(`scripts/.check09-old.py` / `.planning/.gsd-allow-shrink` / `.planning/milestones/v1.15-phases/idi-10-tables-and-radius-scale/.musthaves_rest.txt`),按计划要求一律不动。
- **D-12-7 的变异证明不在本计划内**:它由波次 1 的 `c6`(已配两条变异)与计划 03 的收口序列承担;本计划的 `g1_snapshot()` 是**取证**路径(把 band 拍下来 + 断言拍到了),不是 D-12-7 判据本体的变异对象。
- **`--g1-snapshot` 是 `check-09` 的第四个参数**,计划 03 的全量复跑须按四参数现状调用,不得按旧的三参数形态写命令。

## Self-Check: PASSED

- 已核实创建的产物均在盘:5 张整窗图(各 1440×900、字节非零)与 `.planning/phases/idi-12-g1-band/screenshots/latest-check/latest-check.png`(签名正确、736×270)。
- 已核实两次任务提交存在:`6e9e43d`、`351be8f`。
- 已核实 `commits: 2` 与 `plan_head_before: 04f146194e13f759780e12daa8ea770a80e6136e` 均由 `git rev-list --count 04f1461..HEAD` 实测得出,不是叙述。
- 已核实既有的「恰含 5 个 PNG」断言原文出现次数为 1,门在该断言上仍 PASS。

---
*Phase: idi-12-g1-band*
*Completed: 2026-09-29*

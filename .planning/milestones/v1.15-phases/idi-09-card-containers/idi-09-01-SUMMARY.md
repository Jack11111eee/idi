---
phase: idi-09-card-containers
plan: 01
subsystem: ui
tags: [css, design-tokens, card-containers, elevation, contrast-manifest, playwright, computed-style, wcag]

# Dependency graph
requires:
  - phase: idi-04.1-radix
    provides: "单一围栏 :root 令牌层(tier-1 Radix 原语 + tier-2 语义令牌)+ --white 与 --radius-md"
  - phase: idi-06
    provides: "#doc-panel 的 overflow-y: auto 滚动契约 + #doc-panel-header 的 sticky 表头(L-1)"
provides:
  - "围栏内新增两个 tier-2 令牌:--color-surface-card(var(--white) 别名)与 --shadow-card(0 1px 2px rgba(0, 0, 0, 0.04))"
  - "左栏 4 个 section 与右栏 #doc-panel 的卡片语言:白底 + 1px 既有容器边界 + 既有 --radius-md 圆角 + 零位移极轻阴影"
  - "#doc-panel-header 底色跟随卡片令牌,sticky 遮挡机制保持;border-radius: 0 一字未动"
  - "两条 PAIR 的地面重新归属到卡片底色(marker-active TEXT 4.77 / border-strong NON-TEXT 3.32)"
  - "scripts/check-09-idi09-validation.py —— Phase 9 的运行时门(c1 / c2)+ --screenshot DIR 出图"
  - "scripts/check-05-ui-uat.py 的 .hint 期望侧重新登记(等值形式不变)"
affects: [idi-09-02, idi-09-03]

# Actuals (#2632) — chars/4 over the realized diff, same scale as the plan's `estimate`.
actuals:
  tokens: 5252
  tasks: 3
  commits: 3
plan_head_before: c536d74d7ead1f28e995e76341969c66ce4b669b

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "卡片容器语言 = 白底令牌 + 既有容器边界令牌 + 既有 --radius-md + 极轻零位移阴影;零新增 tier-1 原语、零新增圆角刻度、零新增边界令牌"
    - "「重新登记」≠「放宽」:断言的事实被刻意改变时,只换期望侧所指的令牌,断言形式(与运行时解析值精确等值)一字不动"
    - "PAIR 清单的地面归属必须跟随元素的**实际绘制面**,而非它所在的页面;物理绘制面与登记地面不一致时在注释里显式登记(保守读数也要说明它是保守的)"

key-files:
  created:
    - scripts/check-09-idi09-validation.py
  modified:
    - frontend/style.css
    - scripts/check-05-ui-uat.py

key-decisions:
  - "两个新令牌的落点:紧接 --shadow-overlay 之后、同一组阴影/遮罩令牌段内;--color-surface-card 取 --white 别名(--white 已在围栏内声明 ⇒ 本阶段零新增 tier-1 原语)"
  - "卡片边界色复用既有 --color-border-subtle(gray-6)—— 它已是 #doc-panel 与 .event-list 的容器边界色;刻意零新增「卡片边界」令牌"
  - "check-09 的 c2 断言集落在计划 02 的提交里会与「波次 1 可见卡片改动」矛盾,故按计划边界在 Task 2 追加;Task 1 只落 c1(本计划 frontmatter 的 files_modified 已含该脚本,两个任务都改它)"
  - "REG-01 只有「重新归属并登记」半边在本计划关闭;其字面要求「页面底色换值后 check-02 全部对比度对仍达标」由计划 02 关闭 —— 本 SUMMARY 的 requirements-completed 按计划 frontmatter 全量登记 5 条,但收口判据须以计划 02 的结果为准(已在 STATE 显式登记,勿把勾读成页面换值半边已证)"

patterns-established:
  - "运行时门复用 check-05 的模块级设施(importlib 加载 / ensure_server / make_fixture / enter_project / ok / resolve_token),不重复实现、不改 check-05 的设施一行"
  - "BLOCKED 方向必须用满:元素读不到或令牌解析不出时记 BLOCKED,绝不记 PASS(卡片是画出来的,探针没读到就不构成证据)"

requirements-completed: [VIS-01, VIS-02, CARD-01, CARD-02, REG-01]

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "围栏 :root 内新增 --color-surface-card / --shadow-card 两个 tier-2 令牌,围栏外零裸 #hex、零 tier-1 原语引用"
    requirement: "VIS-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c1#令牌级两条断言"
        status: pass
      - kind: other
        ref: "bash scripts/check-01-token-conformance.sh"
        status: pass
    human_judgment: false
  - id: D2
    description: "左栏 4 个 section 在真实浏览器里呈现为白卡片:计算底色 == 卡片令牌、圆角 == --radius-md(10px)、四边 1px 实线边界、零位移阴影"
    requirement: "CARD-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c1#26 条断言 0 FAIL 0 BLOCKED"
        status: pass
    human_judgment: false
  - id: D3
    description: "右栏 #doc-panel 与左栏同族卡片:白底 + 四边 1px 实线 + 10px 圆角 + 零位移阴影,overflow-y: auto 保留"
    requirement: "CARD-02"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c2#13 条断言 0 FAIL 0 BLOCKED"
        status: pass
    human_judgment: false
  - id: D4
    description: "#doc-panel-header 底色与卡片同值,sticky 遮挡机制保持;阴影只在卡片上、不在表头上"
    requirement: "CARD-02"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c2#[p1] #doc-panel-header 计算 box-shadow == none(对照组)"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled#sticky 把 #doc-panel-header 钉在 #doc-panel 顶部(实测 1.000px,<= 1px 通过)"
        status: pass
    human_judgment: false
  - id: D5
    description: "两条中间调前景的 PAIR 地面重新归属到卡片底色并在白底达标(4.77 / 3.32);清单规模不变、阈值未动、零颜色值改动"
    requirement: "REG-01"
    verification:
      - kind: other
        ref: ".venv/bin/python scripts/check-02-contrast.py"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --screenshot DIR(5 个样本 × 1440x900,供人工看层次)"
        status: pass
    human_judgment: false
  - id: D6
    description: "check-05 的 [p1] .hint 实际背景断言按新事实重新登记(期望侧换指 --color-surface-card),断言形式仍是精确等值"
    requirement: "REG-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 5 --browser bundled#[p1] .hint 实际背景 == var(--color-surface-card) PASS"
        status: pass
    human_judgment: false

# Metrics
duration: 23min
completed: 2026-09-26
status: complete
---

# Phase 9 Plan 01: 卡片令牌端到端 Summary

**界面首次拥有 elevation 层次 —— 左栏 4 个 section 与右栏 #doc-panel 由「完全透明 / 比页面更暗的 gray-2」变为同族白卡片(白底 + 1px 既有容器边界 + 10px 既有圆角 + 零位移极轻阴影),并接进一个真实浏览器 computed-style 运行时门(c1/c2),两条中间调 PAIR 的地面重新归属到卡片底色(4.77 / 3.32)。**

## Performance

- **Duration:** 23 min
- **Started:** 2026-09-26T12:09:55Z
- **Completed:** 2026-09-26T12:32Z
- **Tasks:** 3
- **Files modified:** 3(2 改 1 建)

## Accomplishments

- 围栏 `:root` 内新增两个 tier-2 令牌(`--color-surface-card` / `--shadow-card`),紧接 `--shadow-overlay` 之后,附五条承重事实的注释;**零新增 tier-1 原语**(`--color-surface-card` 是已在围栏内的 `--white` 的别名)、零新增圆角刻度、零新增边界令牌。
- `#main-pane > section` 与 `#doc-panel` 就地扩写为卡片规则(选择器文本与源码顺序逐字不变 —— 硬规则 3「追加,不重排」)。真实浏览器实测:4 个 section 与 `#doc-panel` 的计算底色均为 `rgb(255, 255, 255)`、圆角均为 `10px`、四边均 `1px solid`、`box-shadow` 均为 `rgba(0, 0, 0, 0.04) 0px 1px 2px 0px`(水平偏移 `0px`,零位移)。
- `#doc-panel-header` 底色改指卡片令牌,`border-radius: 0` 一字未动;其上方注释按新事实重写(旧表述「`--color-surface` 与 `#doc-panel` 同值 ⇒ 零新增令牌」在本次改动后为假)。sticky 遮挡机制保持。
- 两条 PAIR 的地面按元素实际绘制面重新归属:`--color-marker-active ON --color-surface-card TEXT`(4.77 ≥ 4.5)与 `--color-border-strong ON --color-surface-card NON-TEXT`(3.32 ≥ 3.0)。清单规模逐字不变(53 对 = 35 TEXT + 18 NON-TEXT + 1 ORDER),阈值未动,`check-02-contrast.py` 零改动。
- 新建 `scripts/check-09-idi09-validation.py`:复用 check-05 的模块级设施,`c1` 26 条断言 + `c2` 13 条断言全 PASS(0 FAIL / 0 BLOCKED / exit=0);`--screenshot DIR` 逐样本出 5 张 **1440×900** 整窗截图,与 `STATES = ["p1","p12","p3","checking","archive"]` 逐项一一对应(计划 03 直接消费)。
- `check-05` 的 `[p1] .hint 实际背景` 断言重新登记后期望侧成立(item 5:0 FAIL,2 BLOCKED 按设计,exit=2)。

## Task Commits

Each task was committed atomically:

1. **Task 1 (tracer): 卡片令牌端到端 —— 围栏两行声明 → 左栏 4 个 section 卡片规则 → 运行时门 c1** - `7234044` (feat)
2. **Task 2: 右栏文档区同族卡片化 + #doc-panel-header 底色跟随 + check-05 的 .hint 期望侧重新登记** - `3bc9660` (feat)
3. **Task 3: 两条 PAIR 的地面重新归属 + 清单历史登记** - `76c5572` (fix)

**Plan metadata:** (本提交, docs: complete plan)

## Files Created/Modified

- `frontend/style.css` — 围栏内新增 `--color-surface-card` / `--shadow-card`;`#main-pane > section` 就地扩写四条声明;`#doc-panel` 的 `border-left` → `border`、底色改指卡片令牌 + 两条新声明;`#doc-panel-header` 底色跟随;2 条 PAIR 的地面重新归属 + 4 处注释登记(清单头部 Phase 9 段、marker-active 声明注释、marker-active NON-TEXT 半条、border-strong 组)
- `scripts/check-09-idi09-validation.py` — **新建**。Phase 9 的运行时门:c1(左栏 4 个 section)/ c2(`#doc-panel` + `#doc-panel-header` 对照组)/ `--screenshot DIR`
- `scripts/check-05-ui-uat.py` — 仅 `item5` 内的 2 处:`.hint` 断言的期望侧(→ `--color-surface-card`)与其上方注释

## Decisions Made

- **两个新令牌的落点与命名**:紧接 `--shadow-overlay` 之后、同一组阴影/遮罩令牌段内;`--color-surface-card` 取 `--white` 别名而非字面量,使「零新增 tier-1 原语」成为可机械核对的事实。
- **卡片边界色复用 `--color-border-subtle`(gray-6)**:它已是 `#doc-panel` 与 `.event-list` 的容器边界色,即本文件既有的容器边界语言 ⇒ 零新增令牌;不新声明「卡片边界」令牌。
- **`check-09` 的 c2 落在 Task 2 而非 Task 1**:与计划的波次边界一致(c2 断言的对象在 Task 2 才成为卡片);Task 1 只落 c1 并保持 `--item` 只认 c1,避免 Task 1 的提交点带上一条必然红的断言。
- **PAIR 重新归属的判据取「实际绘制面」而非「页面」**:`--color-border-strong` 的 10 处消费者全是 input/select 静止边框;select 自带 gray-2 已由既有条目覆盖,input 不声明 `background` ⇒ Chrome 画 UA 字段填充(白)—— 这条事实本文件早已逐字登记(含白底静止比值 3.32),故本次是**如实归位**,不是为 Phase 9 新造的主张。
- **`--color-marker-active` 的 NON-TEXT 半条刻意保留在页面地面**:它与 TEXT 半是同一元素族(同一 `.panel-header` 的 inset 竖条),物理绘制面同为卡片,但页面地面读数(HEAD 4.65 → 计划 02 后 4.18)恒**低于**卡片的 4.77 ⇒ 留在地面是更严的一侧。两个数值已写进注释,使「保留」可被独立核对。
- **REG-01 只关闭一半**:本计划关闭其「受影响配对重新归属并登记」半边;其字面要求「页面底色换值后 `check-02` 全部对比度对仍达标」由计划 02 关闭。`requirements-completed` 按计划 frontmatter 全量登记 5 条(计划 02/03 也各自声明 REG-01 / CARD-01 / CARD-02),但**收口判据须以计划 02 的结果为准** —— 勿把 REQUIREMENTS.md 的勾读成页面换值半边已证。

## Deviations from Plan

None - plan executed exactly as written.

(唯一一处执行期自纠:Task 1 初稿把断言集 `c2` 一并写进了新脚本,随即按计划的波次边界撤回、留到 Task 2 追加 —— 发生在任何提交之前,净 diff 与计划逐条一致,不构成偏差。)

## Issues Encountered

- **计划预判的零余量断言实测坐实。** `check-05 --item 8` 的 `sticky 把 #doc-panel-header 钉在 #doc-panel 顶部(<=1px)` 在 HEAD 上是 `0.0`;`#doc-panel` 新增四边 `1px` 边框后,sticky 元素被钳制在滚动容器的 padding box 上,读数变为 **`1.000px`** —— 闭区间 `<= 1.0` **仍通过,余量为零**。已实跑确认 PASS(item 8:13 条断言,0 FAIL,0 BLOCKED)。该断言的事实(sticky 仍生效)未被本阶段改变,故不构成打破、不需重新登记;**但任何后续对 `#doc-panel` 上边框的 1px 级改动都会把它顶破**。
- **为计划 03 预跑了相邻的两条浏览器门**(计划 01 的 `<verification>` 未要求,属额外确认):`--item 9`(面板区滚动容器普查)PASS 17 条 / `--item 10`(焦点环覆盖与交互态)PASS 42 条,exit=0。两条都直接受本计划禁令保护(未加 `overflow: hidden` ⇒ 焦点环未被裁剪;未删 `overflow-y: auto` ⇒ 滚动者计数仍为 4)。
- **`check-05 --item 5` 的 2 条 BLOCKED 是按设计**:两条 `--ai-smoke` 腿在无 `--ai-smoke` 时不执行 ⇒ `exit=2`,与计划基线逐字一致,不是回归。

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **计划 02 可以开工**:卡片地面已存在(这正是计划 02 换页面底色的前提 —— 先换页面会让两条中间调配对在中间态跌破阈值)。
- **计划 02 接手的两件事**:①`--color-surface-page` → `--radix-gray-3`(CARD-03);②画在页面地面上的其余 **6** 条 PAIR 以 gray-3 重算比值并**登记到清单历史段**(不是刷新旧值)。`ON --color-surface-page` 的 PAIR 条目数已由 8 降为 6。
- **计划 03 可直接消费的产物**:`.venv/bin/python scripts/check-09-idi09-validation.py --screenshot <DIR>` 产出 5 张 1440×900 整窗截图(与 `STATES` 逐项一一对应,无缺项无多余样本),以及 `--item c1 --item c2` 的 39 条断言读数。
- **无阻塞项**。`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` 零字节改动;`scripts/check-01…04` / `check-02-contrast.py` / `check-06` / `check-07` 零改动。

## Gate Evidence (HEAD = 76c5572)

| 门 | 命令 | 结果 |
|---|---|---|
| CHECK-01 | `bash scripts/check-01-token-conformance.sh` | `PASS` / exit 0 |
| CHECK-02 | `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`;含 `PASS  4.77  --color-marker-active on --color-surface-card` 与 `PASS  3.32  --color-border-strong on --color-surface-card`;53 对 + 1 ORDER |
| CHECK-03 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` |
| CHECK-04 | `bash scripts/check-04-important-count.sh` | `PASS` |
| check-09 c1 | `.venv/bin/python scripts/check-09-idi09-validation.py --item c1` | 26 条断言,0 FAIL / 0 BLOCKED,`exit=0` |
| check-09 c2 | `.venv/bin/python scripts/check-09-idi09-validation.py --item c2` | 13 条断言,0 FAIL / 0 BLOCKED,`exit=0` |
| check-09 shot | `.venv/bin/python scripts/check-09-idi09-validation.py --screenshot DIR` | 5 个 PNG,逐个 1440×900,与 `STATES` 一一对应 |
| check-05 item 5 | `.venv/bin/python scripts/check-05-ui-uat.py --item 5 --browser bundled` | 0 FAIL,2 BLOCKED(设计如此),`exit=2` |
| check-05 item 8/9/10 | 同上 `--item 8 --item 9 --item 10` | 13 / 17 / 42 条断言,全 0 FAIL / 0 BLOCKED,`exit=0` |
| 仓库卫生 | `git status --porcelain frontend/` / `ls frontend/vendor/` / `git diff scripts/check-02-contrast.py` | 空 / 仅 `marked.min.js` / 空 |

**实跑命令的变异证据(本计划的禁令有真实探测器):** `#main-pane > section` 与 `#doc-panel` 规则体内不含 `transform` / `filter` / `will-change` / `contain` / `perspective` / `opacity` / `position` / `z-index` / `overflow`(机械 grep 为 `NONE`);`#stream-banner`(`#doc-panel` 的后代、`position: fixed`)的层叠关系因此未被改变 —— 由 `check-05 --item 8` 的 badge × banner rect 不相交断言在计划 03 复跑作证。

## Self-Check: PASSED

- 创建的文件:`scripts/check-09-idi09-validation.py` — FOUND
- 提交:`7234044` / `3bc9660` / `76c5572` — 三条均在 `git log` 中 — FOUND
- `commits` 由磁盘 ledger 量得:`git rev-list --count c536d74..HEAD` == 3(在 SUMMARY 写入时量得,不含本次 docs 元数据提交 —— 与 `idi-08-02` 的 `commits: 3` 同口径)
- 工作树:执行结束时 `git status --porcelain` 为空(无未提交的代码改动)

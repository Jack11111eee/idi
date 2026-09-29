---
phase: idi-11-decard-and-hairline-dividers
plan: 05
subsystem: ui
tags: [css, hairlines, computed-style, playwright, mutation-testing, gate-integrity]

# Dependency graph
requires:
  - phase: idi-11 (plans 01-04)
    provides: 连续白面 + 两条 1px 发丝线 + 改写后的 check-09 c1..c5 + 门禁复跑基线(13 份日志)
provides:
  - 面板间发丝线的绘制边由「非 DOM 首子元素的上边线」换向为「非 DOM 末子元素的下边线」——窗口边缘线缺陷消除
  - check-09 c4 的逐状态发丝线普查(遍历 c05.STATES 全部 5 个样本状态)
  - check-09 c2 的 #doc-panel 自身底色断言(第五个容器首次有门)
  - 三条变异测试的真实 FAIL 读数与逐字节还原证明
  - 围栏内三处被本阶段自己账目推翻的现在时陈述的更正
  - 17 份门原始输出落盘(gate-logs/idi-11-05/)
affects: [Phase 12 (G1 表头 band + 里程碑收口), 任何后续改 frontend/style.css 发丝线规则的阶段]

actuals:
  tokens: 6146
  tasks: 3
  commits: 2

tech-stack:
  added: []
  patterns:
    - "发丝线键控于「非 DOM 末子元素」而非「非 DOM 首子元素」—— 前提是 #ai-panel 恒为 DOM 末子元素且不被 .hidden 隐藏"
    - "判据落在**线的位置**上(有无线落在窗口边缘),不落在面板的位置上(面板 rect.top 恒为 0 是合法的)"
    - "逐状态普查(遍历全部样本状态)取代单点采样:单点采样会在唯一不可能出缺陷的状态里恒真"

key-files:
  created:
    - .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/ (17 份门日志)
  modified:
    - frontend/style.css
    - scripts/check-09-idi09-validation.py

key-decisions:
  - "修法路线由用户 2026-09-28 逐项裁定:**纯 CSS 下边线**,以保住 frontend/app.js 逐字节不改 —— 未采用 JS 加类,也未采用已被验证者否决的 section.hidden + section:not(.hidden)(它会同时抹掉 p3 下 #checks-panel → #ai-panel 的分隔线)"
  - "check-09 的 c1/c4 边框宽度断言随规则**换向**是 BINDING-1 的机械后果,不是范围扩张:不换向则改完仍红,而那不是门在正确工作,是判据仍在断言一条已被裁定改变的事实"
  - "c4 采用**逐状态普查**(全部 5 个样本状态)而非只在 p1 上加一条断言:旧 c4 的唯一断言在 p1 下恒真,而 p1 恰是唯一不可能出缺陷的状态"

patterns-established:
  - "断言落在**契约本身**上而非其单点样本上:契约是「每对相邻可见面板之间恰 1 条、窗口边缘 0 条」,故判据写成三条(可视首个面板无顶线 / 可见线数 == 可见面板数 − 1 / 无线落窗口边缘),而非「恒 1 条」"
  - "**先测量再断言**:1px 级几何变化一律取改动前/后的真实浏览器并排读数(geometry-before/after.log),不得把预测值写成断言"

requirements-completed: [SURF-01, SURF-02, SURF-03, DIV-01, DIV-02, DIV-03, REG-01, REG-02, REG-03]

coverage:
  - id: D1
    description: "面板间发丝线的绘制边换向:规则由 `#main-pane > section + section { border-top }` 就地改写为 `#main-pane > section:not(:last-child) { border-bottom }`,窗口边缘线缺陷消除(5 个样本状态里 3 个曾中招)"
    requirement: "DIV-02"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4,c5 → exit=0"
        status: pass
      - kind: other
        ref: "gate-logs/idi-11-05/geometry-before.log vs geometry-after.log(p3/checking/archive 可视首个面板 borderTopWidth 1px → 0px)"
        status: pass
    human_judgment: false
  - id: D2
    description: "check-09 c4 的逐状态发丝线普查:遍历 c05.STATES 全部 5 个状态,逐状态断三条(可视首个面板 border-top == 0px / 可见线数 == 可见面板数 − 1 / 无线落窗口边缘)"
    requirement: "REG-01"
    verification:
      - kind: automated_ui
        ref: "check-09 --item c4 → 39 条断言,0 FAIL,0 BLOCKED(c4 由 20 增至 39)"
        status: pass
    human_judgment: false
  - id: D3
    description: "check-09 c2 补上 #doc-panel 自身底色断言(== body 计算底色 + == 写死字面量白),第五个容器首次有门"
    requirement: "SURF-02"
    verification:
      - kind: automated_ui
        ref: "check-09 --item c2 → 19 条断言,0 FAIL(c2 由 17 增至 19)"
        status: pass
    human_judgment: false
  - id: D4
    description: "三条变异测试证明改写后的判据会真的失败(M1 规则还原为相邻兄弟 + border-top → c4 21 FAIL;M2 补一条 border-top → c4 13 FAIL;M3 #doc-panel 底色改归 --color-surface → c2 2 FAIL)"
    requirement: "REG-01"
    verification:
      - kind: other
        ref: "idi-11-05 commit bc33cc4 body 逐条登记 FAIL 读数;三次还原均 git checkout -- frontend/style.css,git diff --exit-code rc=0 且 git hash-object == 482310b4511fc116506bbd8f047ba9d08ec72765(逐字节相同,未用 git stash)"
        status: pass
    human_judgment: false
  - id: D5
    description: "围栏内三处被本阶段自己账目推翻的现在时陈述已更正(--color-surface-page 消费者 ONE → FOUR;--color-marker-active 白面 4.65/0.15 → 4.77/0.27;gray-9 白面 3.24 → 3.32),历史账目段逐字保留"
    verification:
      - kind: other
        ref: "grep -cE 'Measured 4\\.65|thinnest margin \\(0\\.15\\)' → 0;grep -cE '3\\.24 / 3\\.15' → 0;grep -cE 'exactly ONE consumer' → 0;grep -cE '分区改由相邻兄弟规则' → 0"
        status: pass
    human_judgment: false
  - id: D6
    description: "1px 级几何变化的运行时并排取证(#ai-panel rect.top 767.00 → 768.00;总高不变)"
    requirement: "REG-03"
    verification:
      - kind: other
        ref: "gate-logs/idi-11-05/geometry-before.log vs geometry-after.log"
        status: pass
    human_judgment: false
  - id: D7
    description: "全门复跑零新增失败(四静态门 / check-05 全量与 item 8·9 / check-06 / check-07 / check-09 / check-10 / 两探针 / node --check / pytest 基线 219 passed 6 skipped)"
    requirement: "REG-03"
    verification:
      - kind: other
        ref: "gate-logs/idi-11-05/ 17 份日志:check-01/03/04 PASS、check-02 PASS:0 failures、check-05 全量 exit=2(item 5 两条 --ai-smoke 腿按设计 BLOCKED,0 FAIL)、item 8 PASS(13)/item 9 PASS(17)、check-06/07/09/10 exit=0、pytest 219 passed 6 skipped"
        status: pass
    human_judgment: false

duration: 62min
completed: 2026-09-29
status: complete
---

# Phase idi-11: 去卡片化与发丝分隔线 — Plan 05 (gap-closure) Summary

**面板间发丝线的绘制边由「非 DOM 首子元素的上边线」换向为「非 DOM 末子元素的下边线」,消除 p3 / checking / archive 三个状态下画在窗口边缘的那条线;`check-09` 的 c4 扩写为遍历全部 5 个样本状态的逐状态普查、c2 补上第五个容器 `#doc-panel` 的底色断言,并以三条变异证明新判据会真的失败。**

## Performance

- **Duration:** 62min(含 2×10min 子代理卡死等待)
- **Started:** 2026-09-29T00:29:00+08:00(≈,wave 5 dispatch)
- **Completed:** 2026-09-29T01:31:00+08:00(≈,最后一份门日志落盘)
- **Tasks:** 3
- **Files modified:** 2(`frontend/style.css`、`scripts/check-09-idi09-validation.py`)+ 17 份门日志

## Accomplishments

- **BLOCKER 消除(DIV-02 / D-11-10):** `frontend/style.css:875` 的规则**就地改写**(不是追加覆盖、位置一字未移)为 `#main-pane > section:not(:last-child) { border-bottom: 1px solid var(--color-border-subtle); }`,线色线宽逐字不变。修因是旧规则键控于 **DOM 相邻**,而 `#session-panel` 在 p3 / checking / archive 被 `app.js:363` 加 `.hidden`(display:none),此时可视的第一个面板(`#annotations-panel` / `#checks-panel`)带着 `border-top` 落在 `#main-pane` 的 `top == 0` ⇒ **5 个样本里 3 个在窗口边缘多画一条设计明令禁止的线**。新机制键控于「非 DOM 末子元素」,而 `#ai-panel` 恒为 `#main-pane` 的 DOM 末子元素且从不被 `.hidden` 隐藏 ⇒ 等价于「除最后一个**可见** section 外」,恒 1 条可见线且永不在窗口边缘。该前提已**显式登记**在承重注释里。
- **判据扩写为契约本身(REG-01):** c4 新增模块级探针 `HAIRLINE_CENSUS_JS` 与遍历 `c05.STATES` 全部 5 个状态的普查,逐状态断三条 —— (i) 可视的第一个面板 `border-top-width == 0px`;(ii) 可见发丝线数 == 可见面板数 − 1;(iii) 没有发丝线落在窗口边缘。**这修掉了旧判据的结构性失明**:旧 c4 的「第一个面板顶部不画线」只在 p1 fixture 上跑,而 p1 下 `#session-panel` 恰是可视的第一个面板 ⇒ 该断言在**唯一不可能出缺陷的状态**里恒真,缺陷存在的树上 `check-09` 仍 exit=0、0 FAIL。
- **第五个容器首次有门(WR-03):** c2 补上 `#doc-panel` 自身底色断言(== body 计算底色 + == 写死字面量白)。修前 c2 只在 `:322` 把它的底色读进 `bg` 却**没有任何断言消费它** ⇒ 面板被重新上色成任何颜色时本门全绿(表头自绘背景,header 断言仍会过;`check-05` 也不断言它)。
- **围栏权威记录自洽(WR-02):** 三处被本阶段自己账目推翻的现在时陈述已更正 —— `--color-surface-page` 的消费者由「exactly ONE」改为**四个**(`html, body` / `#main-pane > section` / `#doc-panel` / `#doc-panel-header`),并写明改它会同时重绘页面、四个面板与 sticky 表头;`--color-marker-active` 白面实测 4.65/0.15 → **4.77/0.27**;gray-9 白面 3.24 → **3.32**。历史账目段逐字保留。
- **第三处机制注释:** `frontend/style.css:781`(`#main-pane` 规则体自身注释)的旧机制描述一并就地改写;三处描述发丝线机制的注释(`:781` / `:814-815` / `:828-855`)现全部与代码一致。
- **变异证明:** 三条变异各给出真实 FAIL 读数,还原后逐字节相同(见下)。

## Task Commits

Each task was committed atomically:

1. **Task 1: 发丝线规则就地换向 + 承重注释与围栏内三处现在时陈述改写** - `764d55c` (fix)
2. **Task 2: check-09 的 c1/c4 换向 + c4 逐状态普查 + c2 补 #doc-panel 底色断言** - `bc33cc4` (fix)
3. **Task 3: 全门复跑与原始输出落盘** - 无独立 commit;17 份日志由本收尾提交一并落盘(见「Issues Encountered」的子代理卡死)

**Plan metadata:** 本 SUMMARY + gate-logs + tracking 更新合并为一个 docs commit

## Files Created/Modified

- `frontend/style.css` — 发丝线规则换向(第 875 行)+ 三处机制注释改写 + 围栏内三处现在时陈述更正(+39/−20)
- `scripts/check-09-idi09-validation.py` — c1/c4 边框宽度断言换向、`HAIRLINE_SECTIONS` 由后三个改为前三个、c4 新增 `HAIRLINE_CENSUS_JS` 与五状态普查、c2 补两条 `#doc-panel` 断言、模块 docstring 契约描述同步改写(+119/−30)
- `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/` — 17 份:14 份门日志 + `geometry-before.log` / `geometry-after.log` + `pytest.log`(独立子目录,`idi-11-04` 的 13 份基线未被覆盖)

## Decisions Made

- **修法路线由用户 2026-09-28 逐项裁定:纯 CSS 下边线。** 用户选择这条路线**正是为了保住 `frontend/app.js` 逐字节不改**;未采用 JS 加类(会动 `app.js`),也未采用 `section.hidden + section:not(.hidden)`(验证者已显式否决:它会同时抹掉 p3 下 `#checks-panel → #ai-panel` 的分隔线)。
- **c1/c4 的边框宽度断言随规则换向是机械后果,不是范围扩张。** 规则从「后三个面板的上边线」变成「前三个面板的下边线」后,仍在断言 `border-top-width == 1px` 的旧判据会变红 —— 而那**不是**门在正确工作,是判据仍在断言一条已被裁定改变的事实。换向时**零条删除、零条降级**;c1 断言数不变(59),c2 / c4 只增。
- **c4 取逐状态普查而非单点采样。** 契约是「每对相邻可见面板之间恰 1 条、窗口边缘 0 条」,不是「恒 1 条」,故判据按契约写成三条并在全部 5 个状态上运行。

## Deviations from Plan

**1. [编排层] 子代理连续卡死三次,Task 3 的门日志落盘与 SUMMARY 由编排者代写**

- **Found during:** Task 3(全门复跑)
- **Issue:** 执行子代理连续三次卡死(stream watchdog 无进展 600s)。三次的**共同形态**是「活干完了但没返回」:第一次卡死时 Task 1 / Task 2 的两个 commit 已落地;续跑时 `probe-07` 已完成(exit=0,ratio=3.54);卡死点都在「写 SUMMARY」前后。
- **Fix:** 依本项目已登记的纪律「同提示两次卡死就改问用户是否授权代写」,向用户呈报并取得授权后,由编排者代写 SUMMARY 并完成落盘 / 提交 / tracking。**编排者在代写前独立复核了全部证据**(两条 commit 的代码状态、`check-09` 实跑、17 份日志的退出码、变异读数、`app.js`/`index.html`/`check-05`/`check-02` 的逐字节未改),未采信子代理的自我报告。
- **Files modified:** 无产品代码改动;仅 SUMMARY 与 gate-logs 的落盘与提交。
- **Verification:** `check-09 --item c1,c2,c3,c4,c5` 由编排者在本机实跑 → exit=0(c1 59 / c2 19 / c3 6 / c4 39 / c5 5,0 FAIL 0 BLOCKED);静态门、pytest、check-05/06/07/10 逐份读日志核对。
- **Committed in:** 本收尾 commit

**2. [编排层] `state.begin-phase` 再次改写派生计数**

- **Found during:** 执行前 `validate_phase` 步
- **Issue:** 该动词把 `progress.percent` 由 **80 覆写为 0** 并抹掉进度条(`state.json` 的 `next.reason` 此前也被同类覆写)。本项目已 15 次复现该组动词不可信。
- **Fix:** 按「判据取 ROADMAP 的 ## Milestones + ## Progress」的口径核盘后手工恢复为 80,并在收口序列的**最后一个动词之后**再核盘一次。
- **Verification:** 见「Issues Encountered」。

---

**Total deviations:** 2(均为编排层,无产品代码偏差)
**Impact on plan:** 产品面**零偏差** —— 计划按原文执行,三个任务的产品改动与计划逐条一致。两处偏差都在编排层(子代理卡死的收尾代写、状态动词的派生计数覆写)。

## Issues Encountered

- **子代理卡死 ×3** —— 见上「Deviations」第 1 条。**不影响正确性**:每次卡死都发生在实质工作完成之后,而编排者一律以「核盘(commit + 门禁实跑)」代替「采信返回」,故未发生重复劳动或半成品落盘。
- **`state.*` 动词再次覆写派生值** —— `state.begin-phase` 把 `percent` 80 → 0。已恢复。收口后复跑核盘判据,不采信该组动词的输出。
- **`probe-07` 首次运行时卡死(89 字节残缺日志)** —— 续跑后完成:`exit=0`、`ratio=3.54 (>= 3.0)`,与 `idi-11-04` 的基线读数逐字一致。该探针**不是门**(其自身 docstring:「不是门」),不进任何守卫命令契约、不被 CI 调用,是 `--color-focus ON --color-surface NON-TEXT@0.75` 那条 PAIR 的反事实证据。
- **`timeout` 命令在本机不存在**(macOS 无 coreutils `timeout`),首次尝试以 `timeout 300 …` 调用 `check-09` 失败(`command not found`)。改为直接调用,无影响。

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **本计划收口了独立验证报出的 1 个 BLOCKER(DIV-02 窗口边缘发丝线)与 2 条 Warning(WR-02 围栏陈旧散文、WR-03 `#doc-panel` 无门)。** 验证报告 `idi-11-VERIFICATION.md` 的 `status: gaps_found` 需由 verifier 复跑后更新。
- **`check-09` 的断言数在三条判据上只增不减**(c1 59 持平 / c2 17→19 / c3 6 持平 / c4 20→39 / c5 5 持平),零项下降;三条变异各给出真实 FAIL 读数。
- **产品面零改动于 `frontend/app.js` / `frontend/index.html` / 后端 / `frontend/vendor/`** —— 与计划预期一致(用户选择纯 CSS 路线正是为保住这条)。`scripts/check-05-ui-uat.py` 与 `scripts/check-02-contrast.py` 亦逐字节未改(WR-01 显式排除在范围外)。
- **Phase 12 待办:** `G1-01`(`#latest-check` 表头 band)、`REG-04`(全里程碑复跑)、`VIS-01`(5 张 1440×900 整窗截图)。**`REG-04` 的「零新增失败」必须在最后一次 `style.css` 改动之后跑才成立** —— 本计划即该次改动。
- **⚠ 一条给 Phase 12 的提示:** 本计划改动了 `scripts/check-09-idi09-validation.py`,按 `REG-04` 的口径这会把该脚本的覆盖者拖进连带指纹名单;**份数须在磁盘上逐份读 `covered_files` 实测**(锚 frontmatter 逐行匹配 + 额外测路径是否仍在盘),不得凭记忆断言。

---
*Phase: idi-11-decard-and-hairline-dividers*
*Completed: 2026-09-29*

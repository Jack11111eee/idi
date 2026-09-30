---
phase: idi-09-card-containers
plan: 03
subsystem: ui
tags: [verification, regression-gates, playwright, computed-style, screenshots, pytest, contrast-manifest, evidence, wcag]

# Dependency graph
requires:
  - phase: idi-09-card-containers
    plan: 01
    provides: "卡片地面(两个 tier-2 令牌 + 五个容器的卡片语言)+ scripts/check-09-idi09-validation.py 的 --screenshot 出图能力"
  - phase: idi-09-card-containers
    plan: 02
    provides: "页面底色下沉到 gray-3 + 密度 12px/16px + 6 条页面地面 PAIR 逐条重算并登记"
provides:
  - "五条浏览器门的复跑记录:check-05 全量 exit=2 且 0 FAIL、check-06 / check-07 / probe-05 / probe-07 全部 exit=0(含 item 5 两条 --ai-smoke BLOCKED 腿的按设计说明)"
  - "四个静态门 + pytest 基线的复核记录(check-01/03/04 PASS、check-02 PASS: 0 failures、pytest 219 passed / 6 skipped)"
  - "8 条受影响配对实测值与清单登记值逐位一致的证据(14.30 / 5.19 / 5.19 / 5.15 / 5.19 / 4.18 / 4.77 / 3.32,ORDER 0.363)"
  - "5 个状态样本的 1440x900 整窗截图(p1 / p12 / p3 / checking / archive)"
  - "SC3 屏幕级半边的正面证据:5 个样本各自同帧渲染 gray-2 内陷面 rgb(249,249,249) 与白卡片 rgb(255,255,255),页面 rgb(240,240,240)"
  - "4 条供用户裁定的开放项 + REQUIREMENTS.md Out of Scope 四项的重申"
  - "原始门禁输出逐份落盘(.planning/phases/idi-09-card-containers/gate-logs/,9 份)供独立复核"
affects: [idi-09-verify, v1.15-milestone-close]

# Actuals (#2632) — chars/4 over the realized diff, same scale as the plan's `estimate`.
actuals:
  tokens: 34578
  tasks: 3
  commits: 3
plan_head_before: f121a2fed144c9b5727e440a14be282d02cad80b

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "复核计划把「门绿了」变成可独立复核的结论:每条门的退出码 + 汇总块原文 + FAIL/BLOCKED 行的完整原文逐份落盘(gate-logs/),SUMMARY 只做索引与分诊,不替代原始输出"
    - "「按设计的非绿」必须与「新回归」在文本上不可混淆:item 5 的两条 BLOCKED 腿与 probe-05 的 BLOCKED 对照各自写明成因,读者不必回读脚本即可判读"
    - "「零处门改动」本身也要有证据形态:判据取 `git status --porcelain scripts/` 与 `git diff HEAD -- scripts/` 同时为空,而不是「我记得没改」"
    - "截图的验收分两层:机器层(check-09 --screenshot 断言 5 个 PNG 逐个 1440x900、清单逐项一一对应)与屏幕层(逐样本运行时读 gray-2 承载者与白卡片同帧共存,补上 SC3 只有令牌级读数的空白)"

key-files:
  created:
    - .planning/phases/idi-09-card-containers/screenshots/p1.png
    - .planning/phases/idi-09-card-containers/screenshots/p12.png
    - .planning/phases/idi-09-card-containers/screenshots/p3.png
    - .planning/phases/idi-09-card-containers/screenshots/checking.png
    - .planning/phases/idi-09-card-containers/screenshots/archive.png
    - .planning/phases/idi-09-card-containers/gate-logs/（9 份原始 stdout）
  modified: []

key-decisions:
  - "零处门改动 —— 计划预期的唯一受影响断言(`check-05` 的 `[p1] .hint 实际背景`)已在计划 01 重新登记,故本计划对 `scripts/` 的净 diff 为零。判据取 `git status --porcelain scripts/` 与 `git diff HEAD -- scripts/` 双空,不是记忆"
  - "`probe-05` 的 `BLOCKED [mutated] ... post-fix` 是**变异证明的对照支**,不是门失败:该探针在同一份被变异的样式表上跑同一条断言两次,「修复前 PASS / 修复后 BLOCKED」正是它要证明的对照(修复后的 `resolve_color` 在令牌未声明时返回 None ⇒ `ok()` 记 BLOCKED)。退出码仍为 0"
  - "`probe-07` 的焦点环地面在本阶段漂移:该探针从 `#round-doc` 取运行时地面,而计划 01 之后其最近不透明祖先是卡片化的 `#doc-panel` ⇒ 地面由 `--color-surface`(3.431)变为卡片白(实测 **3.54**)。断言形式与强度一字未变、退出码仍为 0;但本条的措辞不得被读成「仍在证明 `--color-surface` 上的算术」—— 它证明的是卡片白上的同一算术,而卡片白是更容易的一侧"
  - "SC3 的**屏幕级**半边由本计划补证:`idi-09-02` 的 `c3` 只证明三档**令牌**亮度序与 `body` 计算底色,没有任何断言证明「gray-2 表面与白卡片在同一视口里同时被渲染」。本计划逐样本运行时读得 5/5 样本同帧共存,承载者是三个自带 `background: var(--color-surface)` 的 `<select>` 与 `.overlay-card`(archive 帧内 `.overlay-card` 第 4 个可见,余 4 个的父 `.overlay` 带 `hidden`)"
  - "原始门禁输出落盘为 `gate-logs/`(9 份)而非只留 SUMMARY 摘录。依据是 `<threat_model>` 的 T-idi-09-03(「门绿了」这一结论无原始证据,severity medium,disposition mitigate):摘录是我选过的,原始 stdout 不是。三条提交按任务切分,使每份日志可追溯到产生它的那一条命令"
  - "输入框在白卡片上画 UA 白填充 = **本阶段新增的开放项**(计划只把它列为待写进 SUMMARY 的一条)。实测坐实:`#project-path-input` / `#chat-input-row input` / `#enter-form input[type=\"text\"]` / `#confirmation-modal input[type=\"text\"]` 四者的计算 `background-color` 全部是 `rgb(255,255,255)`,即它们不声明 `background`、由浏览器 UA 画字段填充。故三档刻度里的**中间档**在屏幕上实际只由三个 `<select>` 与 `.overlay-card` 承载。**注:`frontend/style.css:866-872` 的 `#project-path-input` 块内确实没有 `background` 声明 —— 同文件 `:878` 的 `background: var(--color-surface)` 属于紧随其后的 `button` 规则**(初查时用 `grep -A 12` 越过块边界,已按块边界与运行时读数两次更正)"

patterns-established:
  - "「计划里所有行号都是波次之前的旧锚点」在本计划第二次坐实:`.overlay-card` 的底色声明计划写 `:819`,HEAD 实测 `:978`。一律按选择器文本与源码内容定位"
  - "把「哪一侧是更难的一侧」写进复核结论:probe-07 的地面漂移是**往容易的方向**漂(白底比 gray-2 底更容易达标),这类漂移必须写明方向,否则「仍绿」会被读成「同样的强度仍然成立」"

requirements-completed: [REG-02, CARD-01, CARD-02, CARD-03]

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "五条浏览器门复跑无新增失败:check-05 全量 exit=2 且 `=== 逐项结论 ===` 块 10 项 FAIL 计数全 0、唯一的 2 条 BLOCKED 是 item 5 的两条 --ai-smoke 腿(无 --ai-smoke 时按设计不跑);check-06(g1…g6)/ check-07(g1…g4)/ probe-05 / probe-07 全部 exit=0"
    requirement: "REG-02"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --browser bundled → exit=2;item 1:45 / item 2:5 / item 3:17 / item 4:65 / item 5:9(2 BLOCKED) / item 6:6 / item 7:38 / item 8:13 / item 9:17 / item 10:42 条断言,0 FAIL"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-06-idi05-validation.py → exit=0(g1:9 / g2:2 / g3:12 / g4:5 / g5:5 / g6:7,0 FAIL 0 BLOCKED)"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-07-idi08-validation.py → exit=0(g1:21 / g2:39 / g3:10 / g4:3,0 FAIL 0 BLOCKED)"
        status: pass
      - kind: other
        ref: ".venv/bin/python scripts/probe-05-resolve-color.py → exit=0(变异证明:mutated-prefix-verdict=PASS / mutated-postfix-verdict=BLOCKED / control-verdict=PASS)"
        status: pass
      - kind: other
        ref: ".venv/bin/python scripts/probe-07-focus-composite.py → exit=0(archive 合成 opacity=0.75,环 2px rgb(31,99,189) 在卡片白上 ratio=3.54 >= 3.0)"
        status: pass
    human_judgment: false
  - id: D2
    description: "四个静态门全绿 + pytest 基线不降:check-01 / check-03 / check-04 打印 PASS,check-02 打印 `PASS: 0 failures`,pytest 摘要行为 `219 passed, 6 skipped`(必须用项目 .venv)"
    requirement: "REG-02"
    verification:
      - kind: other
        ref: "bash scripts/check-01-token-conformance.sh → PASS / exit 0;bash scripts/check-03-hidden-uniqueness.sh → PASS / exit 0;bash scripts/check-04-important-count.sh → PASS / exit 0"
        status: pass
      - kind: other
        ref: ".venv/bin/python scripts/check-02-contrast.py → PASS: 0 failures / exit 0(53 对 + 1 ORDER)"
        status: pass
      - kind: unit
        ref: ".venv/bin/python -m pytest backend/tests -q --tb=short → 219 passed, 6 skipped, 1 warning in 9.01s / exit 0"
        status: pass
    human_judgment: false
  - id: D3
    description: "check-02 的 8 条受影响配对实测值与 frontend/style.css 清单历史段的登记值逐位一致(14.30 / 5.19 / 5.19 / 5.15 / 5.19 / 4.18 / 4.77 / 3.32),ORDER 仍 0.363;登记未把实跑改成想要的样子"
    requirement: "REG-02"
    verification:
      - kind: other
        ref: ".venv/bin/python scripts/check-02-contrast.py → 8 条目标行逐行读得 14.30 / 5.19 / 5.19 / 5.15 / 5.19 / 4.18 / 4.77 / 3.32;ORDER 0.363"
        status: pass
    human_judgment: false
  - id: D4
    description: "5 个状态样本的 1440x900 整窗截图落盘于 .planning/phases/idi-09-card-containers/screenshots/,文件名以样本名为主干;机器层断言:5 个 PNG 逐个 1440x900、样本清单逐项一一对应、输出目录恰含 5 个 PNG"
    requirement: "CARD-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --screenshot .planning/phases/idi-09-card-containers/screenshots → exit=0,c1:26 / c2:13 / c3:3 / c4:4 / c5:5 / shot:7 条断言 0 FAIL 0 BLOCKED"
        status: pass
      - kind: manual_procedural
        ref: "人工看 5 张 PNG:页面灰、可见容器为白卡片且有边界与圆角、卡片间灰色间隙、archive 帧内归档只读 0.75 合成与白卡片并存"
        status: pass
    human_judgment: false
  - id: D5
    description: "SC3 的屏幕级半边:5/5 样本在同一个 1440x900 视口里同时渲染 gray-2(--color-surface)内陷面与白卡片,页面为 gray-3 —— 承载者是三个自带 background 的 <select> 与 .overlay-card"
    requirement: "CARD-03"
    verification:
      - kind: automated_ui
        ref: "逐样本运行时读 computed background-color:p1/p12 #ai-route-select; p3 #ai-route-select + #round-switcher; checking #ai-route-select + #check-switcher; archive #ai-route-select + #round-switcher + #check-switcher + .overlay-card,全部 rgb(249,249,249),与白卡片 rgb(255,255,255) 同帧共存,body rgb(240,240,240)"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c3 → 三档令牌亮度严格递增 0.871367 < 0.947307 < 1.000000 + body 计算底色 == 令牌解析值"
        status: pass
    human_judgment: false
  - id: D6
    description: "供用户裁定的 4 条开放项(.overlay-card 底色 / 卡片边界与阴影强度 / 页面级留白 / 输入框在白卡片上画 UA 白填充)连同「本阶段未构建」的依据一并列出,并重申 Out of Scope 四项不得预先构建 —— 后续候选是否另开 phase 由用户看截图后裁定"
    requirement: "REG-02"
    verification: []
    human_judgment: true
    rationale: "这是设计裁定而非可自动化判据:每一项的「该不该改」取决于用户对截图的主观评审(卡片是否够凸、弹窗是否该同族、是否要页面级留白),执行器不得自裁。本阶段的范围边界(REQUIREMENTS.md Out of Scope + 用户裁定「先看看效果」)明文禁止就地构建其中任何一项"

# Metrics
duration: 17min
completed: 2026-09-26
status: complete
---

# Phase 9 Plan 03: 门禁复跑与截图交付 Summary

**本阶段是纯 CSS 的构图改动,本计划用本仓库唯一能证明「渲染语义仍然成立」的机器复核它:五条真实浏览器门 + 四个静态门 + pytest 基线全部复跑,零 FAIL、零处门改动、断言强度零降低;并产出 5 张 1440×900 整窗截图,补上 SC3 一直缺的「屏幕级」半边证据(gray-2 内陷面与白卡片在 5/5 样本里同帧共存)。**

## Performance

- **Duration:** 17 min
- **Started:** 2026-09-26T13:45:56Z
- **Completed:** 2026-09-26T14:03:20Z
- **Tasks:** 3
- **Files modified:** 0 代码文件;新增 14 个产物(5 张 PNG + 9 份原始门禁日志)

## Accomplishments

- **五条浏览器门复跑,零 FAIL,零处门改动。** `check-05 --browser bundled` 全量跑 `=== 逐项结论 ===` 十项 FAIL 计数全 0,退出码 **2**(唯一的 2 条 BLOCKED 是 item 5 的两条 `--ai-smoke` 腿,无 `--ai-smoke` 时按设计不跑);`check-06`(g1…g6)/ `check-07`(g1…g4)/ `probe-05` / `probe-07` 全部 `exit=0`。**`git status --porcelain scripts/` 与 `git diff HEAD -- scripts/` 同时为空** ⇒ 计划预期的「零处门改动」实测成立 —— 计划 01 已把唯一一条受影响断言(`check-05` 的 `[p1] .hint 实际背景`)重新登记,本计划无需再动任何一条。
- **三条「预期存活」的断言组实测全部存活。** ①`#doc-panel-header box-shadow == none` 与 `#ai-panel .panel-header box-shadow == none` 对照组全 PASS(p1 / p3 / checking 各两条)—— 证明卡片阴影加在了 `#doc-panel` 与 `#main-pane > section` 上、**没有**误加到表头上。②item 4 的 `#doc-panel-body padding == "32px 40px"` 与 `.panel-header padding-top == "6px"` 全 PASS —— 证明密度改动只落在 `.panel-body`、没有溢出到裁定范围之外。③item 9 的面板区滚动者普查仍**恰好** `{#main-pane, #chat-messages, #latest-check}` —— 证明卡片规则里没有混进 `overflow`。计划 01 预判的零余量 sticky 断言实测仍为 **`1.000px`** 对闭区间 `<= 1.0`,通过且余量为零(事实未变故不重新登记,与波次 1/2 处置一致)。
- **四个静态门 + pytest 基线逐字复核。** `check-01` / `check-03` / `check-04` 打印 `PASS`,`check-02` 打印 `PASS: 0 failures`;`check-02` 的 8 条受影响配对实测 **14.30 / 5.19 / 5.19 / 5.15 / 5.19 / 4.18 / 4.77 / 3.32**、`ORDER 0.363`,与 `frontend/style.css` 清单历史段的登记值**逐位一致** —— 登记没有把实跑改成想要的样子。`.venv/bin/python -m pytest backend/tests -q --tb=short` → **`219 passed, 6 skipped`**,与 v1.14 收口基线逐字一致。
- **5 张 1440×900 整窗截图产出,每张都能看到卡片化的机械后果。** `check-09 --screenshot` 出图 `exit=0`(c1…c5 + shot 共 58 条断言 0 FAIL 0 BLOCKED),文件名以样本名为主干(`p1.png` / `p12.png` / `p3.png` / `checking.png` / `archive.png`),落点是 `.planning/phases/idi-09-card-containers/screenshots/`(不进 `frontend/`)。人工看 5 张:页面是灰的、可见容器是白的且有边界与圆角、卡片之间有灰色间隙;`archive` 帧内归档只读 0.75 合成(`#round-doc` 计算 `opacity` 实测 `0.75`、`#rounds-placeholder` 带 `archive-mode` 类)与白卡片并存而不互相干扰。
- **SC3 的屏幕级半边由本计划正面补证。** `idi-09-02` 的 `c3` 只证明了三档**令牌**的亮度序与 `body` 的计算底色 —— 没有任何断言证明「gray-2 表面与白卡片在**同一视口**里同时被渲染」,而那正是 SC3 的原话(「屏幕上**同时可见**的三档顺序正确」)。本计划逐样本运行时读 computed `background-color`:**5/5 样本**同帧共存 gray-2 `rgb(249,249,249)` 内陷面与白卡片 `rgb(255,255,255)`,页面 `rgb(240,240,240)`。承载者是三个自带 `background: var(--color-surface)` 的 `<select>`(`#ai-route-select` / `#round-switcher` / `#check-switcher`)与 `.overlay-card`。
- **原始门禁输出逐份落盘。** 9 份 stdout 存于 `.planning/phases/idi-09-card-containers/gate-logs/`,按任务切分提交,使「门绿了」这一结论第一次带有**未经我筛选**的原始证据(`<threat_model>` T-idi-09-03 的缓解)。

## Task Commits

Each task was committed atomically:

1. **Task 1: 五条浏览器门复跑 + 失败分诊(零 FAIL ⇒ 零处门改动)** - `32fa653` (test)
2. **Task 2: 四个静态门 + pytest 基线 + 仓库卫生复核** - `284963d` (test)
3. **Task 3: 产出供用户评审的截图 + 移交说明** - `4b83c07` (test)

**Plan metadata:** (本提交,docs: complete plan)

## Files Created/Modified

**零代码改动 —— 本计划对 `frontend/` 与 `scripts/` 的净 diff 均为零。** 新增的全部是复核产物:

- `.planning/phases/idi-09-card-containers/screenshots/` — 5 张 PNG,每张 1440×900:`p1.png`(88,685 B)/ `p12.png`(123,949 B)/ `p3.png`(123,449 B)/ `checking.png`(68,115 B)/ `archive.png`(124,136 B)
- `.planning/phases/idi-09-card-containers/gate-logs/` — 9 份原始 stdout:`check-05-full.log`(524 行)/ `check-06-idi05-validation.log`(76)/ `check-07-idi08-validation.log`(108)/ `probe-05-resolve-color.log`(9)/ `probe-07-focus-composite.log`(7)/ `static-gates.log`(11)/ `check-02.log`(55)/ `pytest.log`(11)/ `check-09-shot.log`(116)

**计划明令零改动的文件(实测确认):** `frontend/style.css` / `frontend/app.js` / `frontend/index.html` / `frontend/vendor/` / `scripts/check-01…04` / `scripts/check-02-contrast.py` / `scripts/check-05-ui-uat.py` / `scripts/check-06` / `scripts/check-07` / `scripts/probe-05` / `scripts/probe-07` / `scripts/check-09-idi09-validation.py`。

## Gate Evidence(HEAD = 4b83c07)

### 五条浏览器门

| 门 | 命令 | 退出码 | 结论块原文 | FAIL | BLOCKED |
|---|---|---|---|---|---|
| CHECK-05 | `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` | **2** | 见下方逐项块 | **0** | **2**(仅 item 5) |
| CHECK-06 | `.venv/bin/python scripts/check-06-idi05-validation.py` | **0** | `item g1..g6: PASS (9/2/12/5/5/7 条断言,0 FAIL,0 BLOCKED)` | 0 | 0 |
| CHECK-07 | `.venv/bin/python scripts/check-07-idi08-validation.py` | **0** | `item g1..g4: PASS (21/39/10/3 条断言,0 FAIL,0 BLOCKED)` | 0 | 0 |
| probe-05 | `.venv/bin/python scripts/probe-05-resolve-color.py` | **0** | `mutated-prefix-verdict=PASS` / `mutated-postfix-verdict=BLOCKED` / `control-verdict=PASS` | — | — |
| probe-07 | `.venv/bin/python scripts/probe-07-focus-composite.py` | **0** | `PROBE composite ring=(31,99,189) ground=rgb(255,255,255) alpha=0.75 composited=(87,138,206) ratio=3.54 (>= 3.0)` | — | — |

`check-05` 的 `=== 逐项结论 ===` 块逐字:

```
item 1: PASS  (45 条断言,0 FAIL,0 BLOCKED)
item 2: PASS  (5 条断言,0 FAIL,0 BLOCKED)
item 3: PASS  (17 条断言,0 FAIL,0 BLOCKED)
item 4: PASS  (65 条断言,0 FAIL,0 BLOCKED)
item 5: BLOCKED  (9 条断言,0 FAIL,2 BLOCKED)
item 6: PASS  (6 条断言,0 FAIL,0 BLOCKED)
item 7: PASS  (38 条断言,0 FAIL,0 BLOCKED)
item 8: PASS  (13 条断言,0 FAIL,0 BLOCKED)
item 9: PASS  (17 条断言,0 FAIL,0 BLOCKED)
item 10: PASS  (42 条断言,0 FAIL,0 BLOCKED)

exit=2  (0=全 pass,1=有 fail,2=有 blocked)
```

**item 5 的两条 BLOCKED 腿完整原文(按设计,不是回归):**

```
BLOCKED [p3] 交互冒烟「处理本轮批注」: expected=无错误完成 actual=<未执行>  # 需要真实 AI 调用,默认不执行;加 --ai-smoke 重跑
BLOCKED [p3] 交互冒烟「发送」: expected=无错误完成 actual=<未执行>  # 需要真实 AI 调用,默认不执行;加 --ai-smoke 重跑
```

两条都是「需要真实 AI 调用」的冒烟腿,无 `--ai-smoke` 时按设计不执行 ⇒ 退出码 2。**本计划未新增任何 BLOCKED。**

**`probe-05` 的 BLOCKED 完整原文(对照支,不是失败):**

```
PROBE mutation-applied=yes
PASS [mutated] .hint color == var(--color-text-muted) (pre-fix): expected=rgb(32, 32, 32) actual=rgb(32, 32, 32)
PROBE mutated-prefix-verdict=PASS
BLOCKED [mutated] .hint color == var(--color-text-muted) (post-fix): expected=<UNRESOLVED> actual=rgb(32, 32, 32)  # 令牌未声明或期望值解析失败
PROBE mutated-postfix-verdict=BLOCKED
PASS [control] .hint color == var(--color-text-muted): expected=rgb(100, 100, 100) actual=rgb(100, 100, 100)
PROBE control-verdict=PASS
```

该探针在同一份**被变异的**样式表(浏览器侧拦截 `/style.css`、只删 `--color-text-muted:` 那一行声明;磁盘文件逐字节不变)上跑同一条断言两次:**修复前形态恒真记 PASS(这就是缺陷的实证),修复后形态因令牌未声明返回 `None` 而记 BLOCKED(这就是修复的实证)**。退出码 `0`。第三条未变异对照 `control-verdict=PASS` 排除「一个永远返回 `None` 的 `resolve_color` 也会通过」。

### 关键断言逐条(计划指定的「预期存活」组)

| 断言 | 实测 | 判读 |
|---|---|---|
| `[p1] .hint 实际背景 == var(--color-surface-card)` | `rgb(255,255,255)` == `rgb(255,255,255)` **PASS** | 计划 01 的重新登记在实跑中成立 |
| 对照组 `#ai-panel .panel-header box-shadow == none` | `none` == `none` **PASS**(p1/p3/checking 各一条) | 阴影加对了元素 |
| 对照组 `#doc-panel-header box-shadow == none` | `none` == `none` **PASS**(p1/p3/checking 各一条) | 同上 |
| item 4 `#doc-panel-body padding` | `32px 40px` == `32px 40px` **PASS** | 密度改动未溢出 |
| item 4 `.panel-header padding-top` | `6px` == `6px` **PASS** | 同上 |
| item 8 sticky(`abs(header.top - panel.top) <= 1.0`) | **`1.000px`** **PASS** | 零余量,事实未变(计划 01 已登记) |
| item 8 badge × banner rect(768 / 1024 / 1280px) | 三档全 **PASS** 不相交 | 卡片规则未加 `contain` 类属性 |
| item 9 滚动者普查 | `['#chat-messages','#latest-check','#main-pane']` **PASS** | 口径「恰好」,未新增第四个 |
| check-06 g6 `box-shadow 恒 none` 对照组 | `none` **PASS** | 折叠往返未被卡片阴影干扰 |
| check-06 g5 340px 最窄面板 | 5 条断言全 **PASS** | 窄窗口未破版 |

### 四个静态门 + pytest 基线

| 门 | 命令 | 结果 |
|---|---|---|
| CHECK-01 | `bash scripts/check-01-token-conformance.sh` | `PASS` / exit 0 |
| CHECK-02 | `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures` / exit 0;53 对 + 1 ORDER |
| CHECK-03 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` / exit 0 |
| CHECK-04 | `bash scripts/check-04-important-count.sh` | `PASS` / exit 0 |
| pytest | `.venv/bin/python -m pytest backend/tests -q --tb=short` | **`219 passed, 6 skipped, 1 warning in 9.01s`** / exit 0 |
| node | `node --check frontend/app.js` | exit 0,无输出 |

**`check-02` 的 8 条受影响配对逐行原文(与清单登记值逐位一致):**

```
PASS  14.30  --color-text on --color-surface-page
PASS  5.19   --color-text-secondary on --color-surface-page
PASS  5.19   --color-text-muted on --color-surface-page
PASS  5.15   --color-focus on --color-surface-page
PASS  5.19   --color-border-hover on --color-surface-page
PASS  4.18   --color-marker-active on --color-surface-page
PASS  4.77   --color-marker-active on --color-surface-card
PASS  3.32   --color-border-strong on --color-surface-card
ORDER 0.363  --color-text-muted before --color-text on --color-surface
```

**阈值与清单规模零改动(断言强度未降低的机械判据):** `check-02-contrast.py` 的 `TEXT_MIN` / `NON_TEXT_MIN` 未被本计划触碰(`git diff HEAD -- scripts/` 为空);`grep -o '/\* PAIR' frontend/style.css | wc -l` == **53**;`grep -o '/\* ORDER' frontend/style.css | wc -l` == **1**。

### 仓库卫生

| 判据 | 实测 | 判读 |
|---|---|---|
| `git status --porcelain frontend/` | **空** | 计划写「期望仅 `M frontend/style.css`」是**旧快照** —— 波次 1/2 已把该文件提交,HEAD 工作树干净。相位起点 `c536d74..HEAD` 的 `git diff --name-only -- frontend/` 恰为 `frontend/style.css` 一个文件,五条相位提交均只碰它 |
| `ls frontend/vendor/` | 仅 `marked.min.js` | PASS |
| `git ls-files frontend/` | 恰 4 个文件(`app.js` / `index.html` / `style.css` / `vendor/marked.min.js`) | 截图未落进 `frontend/` |
| `git status --porcelain`(收口前) | 仅本计划新增的 `screenshots/` 与 `gate-logs/` | 改动面未越界 |

### 门改动登记

**预期零处门改动,实测零处。** 判据:`git status --porcelain scripts/` 为空**且** `git diff HEAD -- scripts/` 为空(两个判据同时成立,不是记忆)。因此**没有**任何一条断言被重新登记、被弱化、被跳过或被删除;`check-02` 的阈值未被放宽,`check-05` 的 24×24 命中区 / sticky 表头 / badge 流内机制 / 窄窗口不破版四条判据的阈值未动。

## Decisions Made

- **原始门禁输出落盘而非只留摘录。** 依据是 `<threat_model>` 的 T-idi-09-03:「门绿了」这一结论若只有我的转述就没有原始证据。摘录是我**选过的**,原始 stdout 不是。9 份日志按产生它们的任务切分提交,使每份都可追溯到具体命令。
- **`probe-05` 的 `BLOCKED` 不按失败处理,但也不按「无关」略过。** 它是该探针**要证明的对照支**之一(修复后形态在令牌未声明时记 BLOCKED)。把它写成「探针也绿」会抹掉这条证明的核心;写成「有一条 BLOCKED」而不解释则会与 item 5 的按设计 BLOCKED 混为一谈。故在 SUMMARY 里连原文与机制一并写清。
- **`probe-07` 的地面漂移按新地面读,并写明漂移方向。** 它证明的算术仍在成立(3.54 >= 3.0),但地面已由 `--color-surface`(3.431)变为卡片白 —— **这是往更容易的方向漂**。计划 03 的 must_haves 明令不得把这条读成「仍在证明 `--color-surface` 上的算术」,故本条在 SUMMARY 与 key-decision 里都写明方向。
- **SC3 的屏幕级半边必须由本计划补证,不能靠 `c3` 顶上。** `c3` 的读数取**令牌级**(三档分别 `resolve_color`),它证明的是令牌亮度序,结构上不含「两个表面同帧被渲染」这回事。故本计划逐样本做了一次运行时 `computed background-color` 读数,把 SC3 的原话(「屏幕上**同时可见**」)落成 5/5 的正面证据。
- **输入框 UA 白填充登记为开放项,并把它与「中间档承载者」的关系写明。** 三档刻度里的中间档在屏幕上实际只由三个 `<select>` 与 `.overlay-card` 承载 —— 文本 input 因不声明 `background` 而画 UA 白填充,读作「白底 + 边框」而非内陷面。这条是**本阶段新增**的开放项(计划只要求把它写进 SUMMARY),不就地构建。

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] 原始门禁输出落盘为 `gate-logs/`(计划只声明了 `screenshots/` 与 `check-05` 两个 `files_modified`)**

- **Found during:** Task 1(五条浏览器门复跑)
- **Issue:** 计划的 `files_modified` 只列 `scripts/check-05-ui-uat.py`(预期零改动)与 `screenshots/`,即原始门禁 stdout 没有落点。但 `<threat_model>` 的 T-idi-09-03 把「『门绿了』这一结论无原始证据」列为 medium 风险、disposition 为 `mitigate`,而 Task 1 的 `<action>` 只要求把原文「抄进 SUMMARY」—— SUMMARY 里的摘录是我筛选过的,不构成原始证据。同时本协议禁止留下未跟踪的生成文件。
- **Fix:** 把 9 份原始 stdout 存入 `.planning/phases/idi-09-card-containers/gate-logs/`,按任务切分提交(5 份随 Task 1、3 份随 Task 2、1 份随 Task 3)。SUMMARY 仍按计划抄录退出码与汇总块原文,原始日志作为其**上游**证据而非替代。
- **Files modified:** `.planning/phases/idi-09-card-containers/gate-logs/*.log`(9 个新文件,共 927 行)
- **Verification:** `git status --porcelain` 收口时为空;9 份日志内容与实跑 stdout 逐字节一致(经重定向直接落盘,未经编辑)
- **Committed in:** `32fa653`(Task 1,5 份)/ `284963d`(Task 2,3 份)/ `4b83c07`(Task 3,1 份)

---

**Total deviations:** 1 auto-added(1 missing critical)
**Impact on plan:** 无范围蔓延 —— 新增的只有复核证据,零产品代码改动、零门改动、零新增依赖。它把 T-idi-09-03 的缓解从「SUMMARY 转述」加强为「原始输出 + SUMMARY 索引」。

## Issues Encountered

- **计划的 `files_modified` 与 `<action>` 在「原始输出落在哪」上留了空白。** 见上条偏差。处置是补齐证据落点,而不是把摘录当原始证据。
- **计划里 `#project-path-input` 的「不声明 background」初查被自己的 grep 误导。** 用 `grep -A 12 '^#project-path-input {'` 时,`frontend/style.css:878` 的 `background: var(--color-surface)` 落进了 12 行窗口内,一度读成「该输入框有灰底」。按**块边界**复核(`:866-872` 块内确实无 `background`,`:878` 属于紧随其后的 `button` 规则)与**运行时**读数(计算值 `rgb(255,255,255)`)两次更正后,计划的表述成立。这正是本项目已登记的口径:文本级检索越界会造出与渲染结果无关的结论。
- **计划里的行号第二次是旧锚点。** 计划写 `.overlay-card` 的底色在 `frontend/style.css:819`,HEAD 实测 **`:978`**(与波次 2 记录的同类现象一致)。本计划一律按选择器文本与源码内容定位。
- **本机 8765 端口仍有一个先前遗留的 uvicorn 在服务**,本计划全部六次浏览器调用(五条门 + 出图 + 三次一次性读数探针)都走了 `ensure_server()` 的「复用,不新起、结束时也不关闭」分支(`INFO server: 127.0.0.1:8765 已在服务 —— 复用,不新起、结束时也不关闭`)。**这是证据的口径提示,不是缺陷**:被测页面仍是本仓库的 `frontend/`,编排器已用 HTTP 抓取核实该进程所服务的 CSS 与磁盘当前内容**逐字节一致**,故读数有效;但这些读数不是在全新进程上取得的。若日后出现与「陈旧服务进程」相关的可疑读数,先排查该残留进程。
- **`state.*` 动词第十一次复现的核盘结论见 STATE.md 的 Blockers/Concerns**(本计划收口序列的实测行为与处置)。

## Known Stubs

None — 本计划零新增代码路径、零占位值。全部产物是实测得到的确定值(门退出码 / 断言读数 / PNG 字节)或对已裁定值的转述,没有任何一条走 `TODO` / 占位 / 空值渲染路径。`gate-logs/` 里唯一的「`<未执行>`」字面是 item 5 两条 `--ai-smoke` 腿的按设计标记,已在本文档与 STATE.md 两处写明。

## Threat Flags

None — 本计划的改动面与 `<threat_model>` 逐条一致:T-idi-09-01(截图产物)落点在 `.planning/`,不进 `frontend/` 也不进发布路径,内容只含本工具的本地界面;T-idi-09-02(分诊中改门)零发生,已用 `git diff HEAD -- scripts/` 双空作机械判据;T-idi-09-03 由 `gate-logs/` 加强;T-idi-09-04 全程走 `--browser bundled`;T-idi-09-SC 零安装(`frontend/vendor/` 仍只有 `marked.min.js`)。未发现计划威胁模型之外的任何新安全相关面。

## 供用户裁定的开放项(截图评审)

以下 4 项**本阶段全部未构建**。请在看过 `screenshots/` 的 5 张图后逐项裁定;每项的依据一并写明。

1. **`.overlay-card` 的底色**(`frontend/style.css:978` 当前 `background: var(--color-surface)` gray-2 + `box-shadow: var(--shadow-overlay)`)。
   **本阶段未构建,依据:** 页面下沉后它会显得比主界面卡片「内陷一档」;是否改白以同族 = **设计决策**,`09-CONTEXT.md` 已登记为留待裁定的开放项。**截图佐证:** `archive.png` 里「使命完成」弹窗卡片(`rgb(249,249,249)`)与右栏白卡片(`rgb(255,255,255)`)同帧并存,可直接对比两者的读感。
2. **卡片边界与阴影的强度。**
   **本阶段未构建,依据:** 边界取的是既有 `--color-border-subtle`(gray-6,与 `#doc-panel` 原有边界同令牌)、阴影取的是用户裁定的 `0 1px 2px rgba(0, 0, 0, 0.04)`。层次目前**主要靠底色差**(ΔL≈6%,三档亮度 0.871367 < 0.947307 < 1.000000),阴影几乎不可见。是否要更强的边界 = 设计决策。
3. **页面级留白。**
   **本阶段未构建,依据:** 没有给 `#main-pane` 加 `padding`、也没给卡片加 `margin` —— 那会移动既有几何并可能打在滚动 / 命中区 / 窄窗口门上。**后果在截图里可见:卡片贴着视口上/下边缘**(`p1.png` / `p3.png` / `checking.png` 的左栏首张卡片顶到 y=0,`archive.png` 的右栏卡片顶到 y=0)。是否要留白 = **未裁定项**。
4. **输入框在白卡片上的填充(本阶段新增的开放项)。**
   **本阶段未构建,依据:** 本应用的文本 input(`#project-path-input` / `#chat-input-row input` / `#enter-form input[type="text"]` / `#confirmation-modal input[type="text"]`)一律**不声明 `background`**,卡片化之后它们在白卡片上画的是浏览器 UA 字段填充(实测四者计算 `background-color` 全为 `rgb(255,255,255)`)—— 输入框因此读作「白底 + 边框」,**不构成 gray-2 内陷面**。三档刻度里的**中间档**在屏幕上实际只由三个 `<select>` 与 `.overlay-card` 承载(见 D5)。「输入框是否该带一层 gray-2 内陷底」= **设计决策**。

**Out of Scope 四项重申(REQUIREMENTS.md 明文,本阶段不得预先构建):**

| 项 | 排除理由 |
|---|---|
| 表格重做(全边框 → 只留横向分隔线) | 独立视觉决策,待 Phase 9 效果确认后另开 phase |
| 图标与空状态 | 同上 |
| 圆角刻度收敛(`--radius-lg: 28px` 与其他档不成比例) | 同上;影响面已实测收窄(只 2 处消费),但属独立决策 |
| 暗色模式 | v1.14 已显式排除(`TOKEN-V2-01`) |

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Phase 9 的三个计划全部收口。** 计划 03 关闭 **REG-02**(五条 UI 门复跑无新增失败);CARD-01 / CARD-02 / CARD-03 的复核半边亦在本计划证成。
- **用户手上的裁定材料已齐:** 5 张 1440×900 整窗截图(`.planning/phases/idi-09-card-containers/screenshots/`)+ 上节的 4 条开放项 + Out of Scope 四项重申。下一步是**用户看截图后裁定**后续候选(表格重做 / 圆角刻度收敛 / 图标与空状态)是否另开 phase —— 本里程碑刻意不含它们。
- **可独立复核的门禁记录已落盘:** `gate-logs/` 9 份原始 stdout + 本文档的 Gate Evidence 表。任何一条结论都可回读原始输出来验证。
- **无阻塞项。** `frontend/app.js` / `frontend/index.html` / `frontend/vendor/` 零字节改动;`frontend/style.css` 在本计划内零改动;`scripts/` 净 diff 为空。
- **两条留给后续的既有登记项(不因本计划关闭):** ①`check-05 --item 8` 的 sticky 断言余量为零(本计划实测仍 `1.000px`),任何后续对 `#doc-panel` 上边框的 1px 级改动都会把它顶破;②本机 8765 端口的残留 uvicorn 进程。

## Self-Check: PASSED

- 创建的文件:`screenshots/p1.png` / `p12.png` / `p3.png` / `checking.png` / `archive.png` — FOUND(5/5,逐个 1440×900)
- 创建的文件:`gate-logs/` 9 份 `.log` — FOUND(9/9)
- 提交:`32fa653` / `284963d` / `4b83c07` — 三条均在 `git log` 中 — FOUND
- `commits` 由磁盘 ledger 量得:`git rev-list --count f121a2f..HEAD` == **3**(在 SUMMARY 写入时量得,不含本次 docs 元数据提交 —— 与 `idi-08-02` / `idi-09-01` / `idi-09-02` 同口径)
- `actuals.tokens` 由同一把尺量得:`git diff f121a2f..HEAD | wc -c` == 138311 → chars/4 = **34578**(计划 `estimate.tokens` 为 30000,故本计划实际消耗约估算的 115%)
- 提交删除检查:`git diff --diff-filter=D --name-only HEAD~1 HEAD` 为空 — 无意外删除
- 工作树:执行结束时 `git status --porcelain` 为空(无未提交的代码改动)

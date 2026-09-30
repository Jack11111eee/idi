---
phase: idi-10-tables-and-radius-scale
plan: 03
subsystem: ui
tags: [regression-gate, playwright, screenshots, evidence, table, radius, visual-regression]

# Dependency graph
requires:
  - phase: idi-10-tables-and-radius-scale
    provides: 表格规则改造(表头 gray-2 浅底 + 仅横向分隔线)与运行时门 t1 / t2 + --screenshot(计划 01)
  - phase: idi-10-tables-and-radius-scale
    provides: 圆角刻度收敛 8 / 10 / 999(--radius-lg 删除、两处消费者改归属)与运行时门 r1 / r2 + --radius-snapshot(计划 02)
provides:
  - 五条浏览器门在改动后的渲染语义上复跑完毕:check-05 / check-06 / check-07 / probe-05 / probe-07 逐门原始 stdout 落盘于 gate-logs/
  - 四个静态门 + pytest 基线 + node --check 的原始输出入册(check-01/02/03/04 全 PASS,pytest 219 passed / 6 skipped)
  - 5 个状态样本的 1440×900 整窗截图,其中 p3 的截图同时可见三个机器可解析表(SC1「至少两张」的实测依据)
  - .chat-user 圆角收敛的人眼取证图(chat-user/p1-chat-user-evidence.png)—— 计划 02 的 D5 人工判断项入口
  - 与 phase 9 基线的逐项对照结论:逐项结论块逐项同形,关键几何读数逐值相同;一条未被计划点名的读数差 3px,成因已由受控 A/B 证明
affects: [idi-10-04]

# Actuals (#2632) —— 同一 estimateTokens 口径(chars/4 over the realized diff)。
# ⚠ 口径说明:本计划**零手写代码**(产品与门脚本都零改动),交付物即门禁的捕获输出。
# 故按「实际产出的文本 diff」计量:gate-logs/ 全部日志正文 147048 字节 / 4 = 36762。
# 二进制 PNG(617825 字节)不计入。若沿用计划 01/02 更严的「仅手写文件」规则,本计划为 0 ——
# 两种口径都写在这里,读者可自行换算,不替读者选一个好看的数字。
actuals:
  tokens: 36762
  tasks: 3
  commits: 3
plan_head_before: dd2caafb75d53ae2e3e11b5539193a85d1da5d0d

tech-stack:
  added: []
  patterns:
    - "「门里没有 FAIL」的判据不能按子串搜:门自己的 PASS 行标签里就可能带 FAIL 一词(本项目既有的 scope-blind 计数坑的**新变体**)—— 判据必须锚行首 verdict 形态 ^FAIL,且必须做阳性对照证明该判据非空转"
    - "跨阶段基线对照的正确粒度是**归一化后逐行 diff**:先剥掉每次运行必然不同的临时路径,再比对;否则「同形」这个结论会被噪声掩埋,而真正的差异(本阶段实测:一条 INFO 里的 3px)也会被当成噪声跳过"
    - "计划声称「零布局改动」时,必须把它声称的**具体读数**与**全部读数**分开核:本计划声称的四个读数(docPanelWidth / scrollWidth / clientWidth / sticky 坐标)逐值相同,但同一次输出里另一条读数(#round-doc 高度)差 3px —— 只核声称的那几条就会漏掉它"
    - "几何差异的成因用**同一次导航内的受控 A/B** 证明:在活页面上注入只还原被改属性的覆盖样式再量一次,差值即该改动的机械后果(本计划实测 3 张表 × 1px = 3px),而不是靠算术推断"

key-files:
  created:
    - .planning/phases/idi-10-tables-and-radius-scale/gate-logs/check-05-full.log
    - .planning/phases/idi-10-tables-and-radius-scale/gate-logs/check-06-idi05-validation.log
    - .planning/phases/idi-10-tables-and-radius-scale/gate-logs/check-07-idi08-validation.log
    - .planning/phases/idi-10-tables-and-radius-scale/gate-logs/probe-05-resolve-color.log
    - .planning/phases/idi-10-tables-and-radius-scale/gate-logs/probe-07-focus-composite.log
    - .planning/phases/idi-10-tables-and-radius-scale/gate-logs/check-01-token-conformance.log
    - .planning/phases/idi-10-tables-and-radius-scale/gate-logs/check-02-contrast.log
    - .planning/phases/idi-10-tables-and-radius-scale/gate-logs/check-03-hidden-uniqueness.log
    - .planning/phases/idi-10-tables-and-radius-scale/gate-logs/check-04-important-count.log
    - .planning/phases/idi-10-tables-and-radius-scale/gate-logs/pytest.log
    - .planning/phases/idi-10-tables-and-radius-scale/gate-logs/node-check-app.log
    - .planning/phases/idi-10-tables-and-radius-scale/gate-logs/check-10-idi10-validation.log
    - .planning/phases/idi-10-tables-and-radius-scale/screenshots/p1.png
    - .planning/phases/idi-10-tables-and-radius-scale/screenshots/p12.png
    - .planning/phases/idi-10-tables-and-radius-scale/screenshots/p3.png
    - .planning/phases/idi-10-tables-and-radius-scale/screenshots/checking.png
    - .planning/phases/idi-10-tables-and-radius-scale/screenshots/archive.png
    - .planning/phases/idi-10-tables-and-radius-scale/screenshots/chat-user/p1-chat-user-evidence.png
  modified: []

key-decisions:
  - "「门里没有 FAIL」的判据由计划字面的子串搜改为锚行首的 verdict 形态 ^FAIL —— 计划字面的 `grep -n 'FAIL' | grep -v '0 FAIL'` 会命中 check-05 第 399 行那条**标签里带 FAIL 一词的 PASS 行**,故在本项目恒非空、是一条无法通过的判据;修正式在五份日志上均为 0,并做了阳性对照证明它非空转"
  - "p3 是唯一自然渲染表格的样本(实测 #round-doc 内恰 3 张表);archive 的轮次文档虽含表,但首屏渲染的是零表格行的 DESIGN.md ⇒ SC1 的「至少两张」指**表**不指**样本**,该读法由实跑坐实"
  - ".chat-user 的人眼取证图另置 screenshots/chat-user/ 子目录而非平铺进 screenshots/ —— 平铺会把目录里的 PNG 数从 5 变成 6,直接违反计划 Task 3 的「恰含 5 个 PNG」判据;子目录同时让「这 5 张是状态样本、这一张是探针取证」在文件系统层面自明"
  - "本计划对 frontend/style.css 与 scripts/ 下全部文件**零改动** —— 判据取 `git status --porcelain frontend/` 与 `git status --porcelain scripts/` 双空 + `git diff --stat dd2caaf..HEAD -- frontend/style.css` 为空,不是记忆"
  - "门改动实测**零处**:`git diff -- scripts/check-05-ui-uat.py` 为空,`git status --porcelain scripts/` 为空 ⇒ 无任何断言被重新登记、放宽、跳过或删除"
  - "本计划的 actuals 同时给出两种口径(捕获文本 diff 36762 / 严格手写文件口径 0),因为本计划零手写代码 —— 只报一个数会把口径差异藏起来"

patterns-established:
  - "跨阶段门禁基线对照 = 归一化(剥临时路径)→ 逐行 diff → 对每一处差异定成因;「逐项同形」不能靠眼看结论块"
  - "计划声称「零 X 改动」时,声称的读数与同批输出里的其余读数必须分别核 —— 前者证明承诺兑现,后者防止承诺的措辞比事实更强"
  - "被断言的值变了但断言仍通过时,要区分「事实未被改变(断言没在看)」与「事实被改变但仍在阈值内」;本计划的 3px 属后者,阈值余量已逐条给出"

requirements-completed: [TABLE-01, TABLE-02, RADIUS-01, RADIUS-02]

coverage:
  - id: D1
    description: "五条浏览器门在「表格重做 + 圆角收敛」之后的渲染语义上复跑零 FAIL:check-05 逐项结论块零 FAIL(exit=2 系 item 5 两条 --ai-smoke 腿按设计 BLOCKED)、check-06 / check-07 / probe-05 / probe-07 均 exit=0;且与 phase 9 基线的逐项结论块逐项同形"
    requirement: "REG-03"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --browser bundled ⇒ exit=2,10 个 item 零 FAIL,BLOCKED 仅 item 5 的 2 条 --ai-smoke 腿"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-06-idi05-validation.py / check-07-idi08-validation.py / probe-05-resolve-color.py / probe-07-focus-composite.py ⇒ 四条均 exit=0"
        status: pass
      - kind: other
        ref: "逐行 diff(归一化临时路径)本次 check-05-full.log vs .planning/phases/idi-09-card-containers/gate-logs/check-05-full.log ⇒ 逐项结论块 10 行逐字相同"
        status: pass
      - kind: other
        ref: "grep -nE '^FAIL' 五份日志 ⇒ 0 / 0 / 0 / 0 / 0;阳性对照:同判据在合成 FAIL 行上返回 1 行"
        status: pass
    human_judgment: false
  - id: D2
    description: "四个静态门 + pytest 基线 + node --check:check-01/02/03/04 全 PASS(check-02 为 PASS: 0 failures 且含表头绘制面那条 PASS 15.48 --color-text on --color-surface 原文行);pytest 219 passed, 6 skipped;node --check frontend/app.js exit=0 零输出;PAIR=53 / ORDER=1 / @media=1 / ^.hidden {=1 零清单增删"
    verification:
      - kind: other
        ref: "bash scripts/check-01-token-conformance.sh / check-03 / check-04 ⇒ PASS;.venv/bin/python scripts/check-02-contrast.py ⇒ PASS: 0 failures"
        status: pass
      - kind: unit
        ref: ".venv/bin/python -m pytest backend/tests -q --tb=short ⇒ 219 passed, 6 skipped in 6.35s(项目 .venv)"
        status: pass
      - kind: other
        ref: "node --check frontend/app.js ⇒ exit=0 且零输出;git status --porcelain frontend/ 与 scripts/ 双空;ls frontend/vendor/ 仅 marked.min.js"
        status: pass
    human_judgment: false
  - id: D3
    description: "5 个状态样本(p1 / p12 / p3 / checking / archive)的 1440×900 整窗截图落盘,逐张实测 IHDR 宽高;其中 p3 的截图同时可见三个机器可解析表(批注回应 / 覆盖维度 / 未决问题清单),表格呈「无竖线、无外框、表头浅灰底、行间极浅横向分隔线」"
    requirement: "TABLE-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-10-idi10-validation.py --screenshot .planning/phases/idi-10-tables-and-radius-scale/screenshots ⇒ exit=0,item shot 7 条断言 0 FAIL 0 BLOCKED"
        status: pass
      - kind: other
        ref: "struct.unpack 逐张读 IHDR ⇒ 5/5 为 1440×900;受控探针实测 p3 的 #round-doc 内 tableCount=3、rowCount=[3,6,3]"
        status: pass
    human_judgment: false
  - id: D4
    description: "门改动零处:本计划对 frontend/style.css、frontend/app.js、frontend/index.html、scripts/ 下全部文件零改动;没有任何断言被重新登记、放宽、跳过或删除"
    requirement: "REG-03"
    verification:
      - kind: other
        ref: "git diff -- scripts/check-05-ui-uat.py 为空;git status --porcelain scripts/ 为空;git status --porcelain frontend/ 为空;git diff --stat dd2caaf..HEAD -- frontend/style.css 为空"
        status: pass
    human_judgment: false
  - id: D5
    description: "表格是否真的读作「白卡片内的一个内陷块」而非另一种网格 —— 计算样式能证明「底色 == gray-2 且只剩一条横向分隔线」,不能证明它读起来是内陷块"
    requirement: "TABLE-01"
    verification: []
    human_judgment: true
    rationale: "计划 01 的 coverage D3 遗留的人工判断项。本计划产出的 p3 截图(同时可见三个机器可解析表)是它的评审入口:表格已无竖线与外框、表头一条浅灰底、行间极浅横向分隔线,该形态是否读作内陷块只有人眼能判。"
  - id: D6
    description: ".chat-user 由 28px 大圆角气泡变为 10px 卡片圆角(其右下角仍是 8px 尖角)的观感是否与 Phase 9 的卡片语言同族 —— 这是本阶段唯一外观真的变了的消费者"
    requirement: "RADIUS-02"
    verification:
      - kind: automated_ui
        ref: "screenshots/chat-user/p1-chat-user-evidence.png 的读数:.chat-user 四个物理角长手 = 10px / 10px / 10px / 8px,简写 = '10px 10px 8px',--radius-md=10px / --radius-sm=8px"
        status: pass
    human_judgment: true
    rationale: "计算样式能证明「TL/TR/BL == 10px 且 BR == 8px」,不能证明那个形态读起来是卡片档气泡而不是被削平了一块。计划 02 的 coverage D5 即本条;入口是 screenshots/chat-user/p1-chat-user-evidence.png —— p1 fixture 无 transcript.md,该元素自然状态不存在,故用应用自身的 appendChatMessage('user', …) 造出探针气泡后再整窗截图(手法照抄 scripts/check-05-ui-uat.py:876-879)。"

duration: 15 min
completed: 2026-09-27
status: complete
---

# Phase 10 Plan 03: 五条浏览器门复跑与截图交付 Summary

**本阶段两处纯 CSS 改动(表格重做 + 圆角收敛)在五条真实浏览器门上复跑零 FAIL、与 phase 9 基线逐项结论块逐项同形、门改动实测零处;5 张 1440×900 整窗截图落盘(p3 一张同时可见三个机器可解析表),另出一张 `.chat-user` 10px 圆角的人眼取证图**

## Performance

- **Duration:** 15 min
- **Started:** 2026-09-27T11:52:08Z
- **Completed:** 2026-09-27T12:07:29Z
- **Tasks:** 3
- **Files modified:** 0(产品代码与门代码零改动);新增 12 份门禁日志 + 6 张 PNG

## Accomplishments

- **五条浏览器门复跑,零 FAIL、零门改动。** `check-05 --browser bundled` exit=2(设计如此),`=== 逐项结论 ===` 块 10 个 item **零 FAIL**,唯一的 `BLOCKED` 是 item 5 的两条 `--ai-smoke` 腿;`check-06` / `check-07` / `probe-05` / `probe-07` 四条均 `exit=0`。逐门 stdout **原文未截断**落盘于 `gate-logs/`,尾部追加 `[gsd] EXIT=<code>` 供独立复核。
- **与 phase 9 基线的对照是逐行 diff,不是眼看。** 归一化临时路径后,本次 `check-05-full.log` 与 `.planning/phases/idi-09-card-containers/gate-logs/check-05-full.log` 的差异**只有 6 处**,其中 5 处是 style.css 行号漂移(本阶段新增 45 行)与本次临时目录名,第 6 处是下面「3px 发现」那条。**逐项结论块 10 行逐字相同**。
- **计划点名的「预期存活」断言逐条实测存活。** `[p1] .markdown-body td font-size == var(--text-base)` 为 **PASS**(不是 BLOCKED);item 8 的 L-2 三宽度溢出诊断 `overflow=0px` ×3、`docPanelWidth` = 432 / 340 / 340、`badge × banner 不相交` 三条 PASS 且 rect 与 phase 9 逐值相同;item 4 的四条几何断言全 PASS;item 9 的滚动者普查(口径「恰好」)PASS;item 2 的 `#round-doc` 正文对比度 `ratio=16.29` PASS;`check-06` g3 / g5 / g6 全 pass(含 g6 两条 `box-shadow 恒 none` 对照组与 `#doc-panel.collapsed` 折叠往返);`check-07` 四条行为断言全 pass。
- **静态门与基线全绿。** `check-01` / `check-03` / `check-04` 打印 `PASS`;`check-02` 为 `PASS: 0 failures`,且**当场复现**了表头新绘制面的既有条目原文 `PASS  15.48  --color-text on --color-surface`(规划期 Pattern Map 报的同一个数,本次由执行器实跑坐实)。`PAIR=53` / `ORDER=1` / `@media=1` / `^\.hidden {=1` 零清单增删。pytest(项目 `.venv`)**219 passed, 6 skipped** 与基线逐字一致。`node --check frontend/app.js` exit=0 且零输出。
- **5 张状态样本截图 + 1 张人眼取证图落盘。** 每张 IHDR 实测 **1440×900**;`p3` 的截图里**同时可见三个机器可解析表**(批注回应表 / 覆盖维度表 / 未决问题清单),它们同在 `p3` 当前轮的 `docs/discuss-round-2.md` 的 §1 / §2 / §3,表格呈**无竖线、无外框、表头一条浅灰底、行间极浅横向分隔线**。受控探针实测 `#round-doc` 内 `tableCount=3`、`rowCount=[3,6,3]`。
- **本计划对产品与门代码零改动**:`git diff -- scripts/check-05-ui-uat.py` 为空,`git status --porcelain scripts/` 为空,`git status --porcelain frontend/` 为空。

## Task Commits

Each task was committed atomically:

1. **Task 1: 五条浏览器门复跑 + 失败分诊 + 逐门原始日志落盘** - `a98c788` (test)
2. **Task 2: 四个静态门 + pytest 基线 + `node --check` + 仓库卫生复核** - `712ef40` (test)
3. **Task 3: 产出供用户评审的截图 + 开放项与移交说明** - `c07d973` (test)

**Plan metadata:** 见本次收口的 docs 提交

## Files Created/Modified

- `gate-logs/check-05-full.log`(525 行)- check-05 全量原文,含 `=== 逐项结论 ===` 与 item 8 的全部 INFO 几何读数
- `gate-logs/check-06-idi05-validation.log`(78 行)/ `check-07-idi08-validation.log`(110 行)- 两条浏览器门原文
- `gate-logs/probe-05-resolve-color.log`(11 行)/ `probe-07-focus-composite.log`(9 行)- 两条变异证明探针原文
- `gate-logs/check-01-token-conformance.log` / `check-03-hidden-uniqueness.log` / `check-04-important-count.log`(各 1 行:`PASS`)
- `gate-logs/check-02-contrast.log`(55 行)- 53 条 PAIR + 1 条 ORDER + `PASS: 0 failures`
- `gate-logs/pytest.log`(11 行)- `219 passed, 6 skipped, 1 warning in 6.35s`
- `gate-logs/node-check-app.log`(**0 字节**)- `node --check` 零输出即通过
- `gate-logs/check-10-idi10-validation.log`(171 行)- 本阶段自建运行时门的 `--screenshot` 模式原文
- `screenshots/{p1,p12,p3,checking,archive}.png` - 5 张 1440×900 整窗截图
- `screenshots/chat-user/p1-chat-user-evidence.png` - `.chat-user` 10px 圆角的人眼取证图(见 Deviations 第 2 条)

## Gate Evidence(原始输出,不是摘录)

### 五条浏览器门

```
$ .venv/bin/python scripts/check-05-ui-uat.py --browser bundled
=== 逐项结论 ===
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
$ echo "exit=$?"
exit=2
```

```
$ .venv/bin/python scripts/check-06-idi05-validation.py    → exit=0
$ .venv/bin/python scripts/check-07-idi08-validation.py    → exit=0
$ .venv/bin/python scripts/probe-05-resolve-color.py       → exit=0
$ .venv/bin/python scripts/probe-07-focus-composite.py     → exit=0
```

### 「没有 FAIL」的判据(scope-blind-safe,且做了阳性对照)

```
$ for f in check-05-full check-06-idi05-validation check-07-idi08-validation \
           probe-05-resolve-color probe-07-focus-composite; do
    printf "%s ^FAIL=" "$f"; grep -cE '^FAIL' gate-logs/$f.log
  done
check-05-full ^FAIL=0
check-06-idi05-validation ^FAIL=0
check-07-idi08-validation ^FAIL=0
probe-05-resolve-color ^FAIL=0
probe-07-focus-composite ^FAIL=0

# 阳性对照:证明该判据非空转
$ printf 'FAIL [p1] synthetic verdict: expected=a actual=b\n' | grep -cE '^FAIL'
1
```

### 四个静态门 + 基线

```
$ bash scripts/check-01-token-conformance.sh   → PASS      (exit=0)
$ bash scripts/check-03-hidden-uniqueness.sh   → PASS      (exit=0)
$ bash scripts/check-04-important-count.sh     → PASS      (exit=0)
$ .venv/bin/python scripts/check-02-contrast.py
PASS  15.48  --color-text on --color-surface          # ← 表头新绘制面的既有条目,本次实跑原文
ORDER 0.363  --color-text-muted before --color-text on --color-surface
PASS: 0 failures                                       (exit=0)

$ .venv/bin/python -m pytest backend/tests -q --tb=short
219 passed, 6 skipped, 1 warning in 6.35s               (exit=0)

$ node --check frontend/app.js                          (exit=0,零输出)
```

### 仓库卫生与计数

```
$ git status --porcelain frontend/     → (空)
$ git status --porcelain scripts/      → (空)
$ git diff -- scripts/check-05-ui-uat.py → (空)
$ ls frontend/vendor/                  → marked.min.js
$ grep -o '/\* PAIR'  frontend/style.css | wc -l   → 53
$ grep -o '/\* ORDER' frontend/style.css | wc -l   → 1
$ grep -c '@media'    frontend/style.css           → 1
$ grep -c '^\.hidden {' frontend/style.css         → 1
```

### 本阶段自建运行时门(阶段末尾仍全绿)

```
$ .venv/bin/python scripts/check-10-idi10-validation.py --item t1 --item t2 --item r1 --item r2
item t1: PASS  (53 条断言,0 FAIL,0 BLOCKED)
item t2: PASS  (46 条断言,0 FAIL,0 BLOCKED)
item r1: PASS  (10 条断言,0 FAIL,0 BLOCKED)
item r2: PASS  (9 条断言,0 FAIL,0 BLOCKED)
exit=0

$ .venv/bin/python scripts/check-10-idi10-validation.py \
    --screenshot .planning/phases/idi-10-tables-and-radius-scale/screenshots
item t1: PASS  (53 条断言,0 FAIL,0 BLOCKED)
item t2: PASS  (46 条断言,0 FAIL,0 BLOCKED)
item r1: PASS  (10 条断言,0 FAIL,0 BLOCKED)
item r2: PASS  (9 条断言,0 FAIL,0 BLOCKED)
item shot: PASS  (7 条断言,0 FAIL,0 BLOCKED)
exit=0
```

## 与 phase 9 基线的逐项对照

### `=== 逐项结论 ===` 块(两边 10 行全文抄录)

| item | 本次(idi-10-03) | phase 9 基线(`idi-09-card-containers/gate-logs/check-05-full.log`) | 一致? |
|---|---|---|---|
| 1 | `PASS (45 条断言,0 FAIL,0 BLOCKED)` | `PASS (45 条断言,0 FAIL,0 BLOCKED)` | ✅ |
| 2 | `PASS (5 条断言,0 FAIL,0 BLOCKED)` | `PASS (5 条断言,0 FAIL,0 BLOCKED)` | ✅ |
| 3 | `PASS (17 条断言,0 FAIL,0 BLOCKED)` | `PASS (17 条断言,0 FAIL,0 BLOCKED)` | ✅ |
| 4 | `PASS (65 条断言,0 FAIL,0 BLOCKED)` | `PASS (65 条断言,0 FAIL,0 BLOCKED)` | ✅ |
| 5 | `BLOCKED (9 条断言,0 FAIL,2 BLOCKED)` | `BLOCKED (9 条断言,0 FAIL,2 BLOCKED)` | ✅ |
| 6 | `PASS (6 条断言,0 FAIL,0 BLOCKED)` | `PASS (6 条断言,0 FAIL,0 BLOCKED)` | ✅ |
| 7 | `PASS (38 条断言,0 FAIL,0 BLOCKED)` | `PASS (38 条断言,0 FAIL,0 BLOCKED)` | ✅ |
| 8 | `PASS (13 条断言,0 FAIL,0 BLOCKED)` | `PASS (13 条断言,0 FAIL,0 BLOCKED)` | ✅ |
| 9 | `PASS (17 条断言,0 FAIL,0 BLOCKED)` | `PASS (17 条断言,0 FAIL,0 BLOCKED)` | ✅ |
| 10 | `PASS (42 条断言,0 FAIL,0 BLOCKED)` | `PASS (42 条断言,0 FAIL,0 BLOCKED)` | ✅ |
| 末行 | `exit=2` | `exit=2` | ✅ |

**结论:10 个 item 的断言数与 FAIL / BLOCKED 分布逐项一致,零差异。** item 5 的 2 条 BLOCKED 在两边是同两条(见下)。

### 归一化逐行 diff 的全部差异(6 处,逐处给出成因)

命令:`sed -E 's#/var/folders/[^ ]*/idi-05-uat-[A-Za-z0-9_]+/[^ ]+#<TMPDIR>#g'` 后 `diff`。

| # | 差异 | 本次 | phase 9 | 成因 |
|---|---|---|---|---|
| 1 | 临时工作目录名 | `…/idi-05-uat-vr02fygq` | `…/idi-05-uat-cxkguzc9` | 每次 `mkdtemp` 必然不同 —— 非差异 |
| 2 | `@media` 命中行 | `[1910]` | `[1865]` | 本阶段在 style.css 新增 45 行,行号下移 —— **非语义差异** |
| 3 | `max-height: 30vh;` 命中行 | `[1527]` | `[1482]` | 同上(+45) |
| 4 | `:focus-visible` 规则块起始行 | `[1723]` | `[1678]` | 同上(+45) |
| 5 | `FOCUSABLE_SELECTOR ↔ :focus-visible` 的 CSS 侧行号 | `1723` | `1678` | 同上(+45);两侧枚举值逐字相同、对称差 `[]` |
| 6 | **`#round-doc` 高度与 L-5 clearance** | `-65.6px` / `775.640625` | `-68.6px` / `778.640625` | **真实几何差异,见下节** |

### item 8 的关键 INFO 读数逐值对照(计划点名的那几条)

| 读数 | 本次 | phase 9 | 一致? |
|---|---|---|---|
| `L-2 @1440px` scrollWidth / clientWidth / overflow / docPanelWidth | `1440 / 1440 / 0px / 432` | `1440 / 1440 / 0px / 432` | ✅ 逐值相同 |
| `L-2 @1024px` | `1024 / 1024 / 0px / 340` | `1024 / 1024 / 0px / 340` | ✅ 逐值相同 |
| `L-2 @768px` | `768 / 768 / 0px / 340` | `768 / 768 / 0px / 340` | ✅ 逐值相同 |
| `sticky` scrollTop / scrollHeight / clientHeight | `4350 / 5248 / 898` | `4350 / 5248 / 898` | ✅ 逐值相同 |
| `sticky` header | `{top:1, bottom:35, left:1009, right:1439}` | 逐字相同 | ✅ |
| `sticky` panel | `{top:0, bottom:900, left:1008, right:1440}` | 逐字相同 | ✅ |
| `badge × banner` @768px | `badge 637.97–738.89 × 8–33` / `banner 285.34–482.66 × 12–39` | 逐字相同 | ✅ |
| `badge × banner` @1024px | `badge 893.97–994.89` / `banner 413.34–610.66` | 逐字相同 | ✅ |
| `badge × banner` @1280px | `badge 1149.97–1250.89` / `banner 541.34–738.66` | 逐字相同 | ✅ |
| sticky 断言实测 | `1.000px`(`<= 1.0` PASS,余量为零) | `1.000px` | ✅ 与 STATE.md 登记的零余量事实一致 |

**⇒ 计划点名的全部读数逐值相同。** 「去掉表格竖线只会让表更窄、方向安全」这条结论由**实测**承担:`#doc-panel` 实测宽仍逐位等于 `clamp()` 上界,文档级 `scrollWidth` 仍等于 `clientWidth`(溢出 0px)。

## 一条未被计划点名的读数差异:`#round-doc` 高度 −3px(成因已证明)

计划的 `must_haves` 写着「本阶段零宽度改动、**零布局改动**」。归一化 diff 显示这条措辞**比事实更强**:

| 读数 | 本次(HEAD) | phase 9 | 差 |
|---|---|---|---|
| `item8 [p3] L-5 clearance: #round-doc × #doc-panel` | `-65.6px`,`height=775.640625` | `-68.6px`,`height=778.640625` | **+3px(元素矮了 3px)** |
| `item8 [p3] L-5 clearance: #btn-authorize × #doc-panel` | `-121.6px` | `-124.6px` | +3px(随之改善) |
| `item9 [p3] L-5 声明集` | `('#round-doc','#doc-panel',775.6,898,-65.6)` | `(…,778.6,898,-68.6)` | 同源 |

**成因用受控 A/B 证明,不是推断。** 在同一次导航、同一个 `p3` fixture 上,先量 HEAD 现状,再注入一条**只还原被改属性**的覆盖样式(`#round-doc th, #round-doc td { border: 1px solid var(--color-border) !important; }`)重新量:

```
AFTER  (HEAD, border: none + border-bottom): {'docH': 775.640625, 'tableCount': 3, 'tableHeights': [95.25, 190.5, 95.25], 'rowCount': [3, 6, 3]}
BEFORE (override restores 4-side border):    {'docH': 778.640625, 'tableCount': 3, 'tableHeights': [96.25, 191.5, 96.25], 'rowCount': [3, 6, 3]}
DELTA docH = 3.0
DELTA per-table = [1.0, 1.0, 1.0]
```

**机制:** `border-collapse: collapse` 下,`border: 1px solid`(四边)给表格盒贡献 1px 顶边;计划 01 就地改写为 `border: none` + `border-bottom: 1px solid` 后顶边消失,每张表矮 **1px**。`p3` 当前轮的 `docs/discuss-round-2.md` 恰有 **3 张表**(受控探针实测 `tableCount=3`,`rowCount=[3,6,3]` = 三个表头行 + 2/5/2 个数据行)⇒ `3 × 1px = 3px`。**这是计划 01 那处改动的直接、必然的机械后果,不是本计划的改动,也不是缺陷。**

**为什么不构成「打破」:** 该事实(表格有边框)正是本阶段**刻意改变**的对象,而这条读数上的**断言**是 item 8 的 `L-5 clearance >= 4px`(在 item 9 里断言),实测未达标集为 `[]`、PASS;方向也与计划预判一致(表更矮/更窄,元素 clearance 从 `-68.6` 改善到 `-65.6`)。**⇒ 无需重新登记,零门改动。**

**计划措辞的更正(留档以免被后来者当成缺陷):** 「零布局改动」应读作「零 `padding` / `margin` / 宽度 / 定位改动」—— 本阶段确实一条都没碰。**边框属于盒模型的一部分,去掉表格四边框必然改变表格盒高度**;`#doc-panel` 的宽与文档级溢出(计划 `key_links` 真正点名的那几条)逐值未变。

## Decisions Made

- **「没有 FAIL」的判据锚行首 `^FAIL`,不按子串搜。** 计划字面的 `grep -n 'FAIL' <log> | grep -v '0 FAIL'` 在本项目**恒非空**(见 Deviations 第 1 条),照它执行会得出「门红了」的假结论;改用锚 verdict 形态的 `grep -nE '^FAIL'` 后五份日志均为 0,并做了阳性对照。这不是放宽判据 —— 修正式比原式**更严**(原式把 PASS 行也算命中)。
- **跨阶段对照取归一化后的逐行 diff,不取「结论块看着一样」。** 这个粒度既确认了「逐项同形」,也捞出了计划没点名的那条 3px。
- **`.chat-user` 取证图另置子目录,不平铺。** 平铺会把 `screenshots/` 的 PNG 数从 5 变成 6,直接违反计划 Task 3 的「恰含 5 个 PNG」判据;子目录让「5 张状态样本 + 1 张探针取证」在文件系统层面自明。
- **`probe-05` 的 1 条 BLOCKED 按设计解释,不当失败。** 该探针在同一份被变异的样式表上跑同一条断言两次,「修复前 PASS / 修复后 BLOCKED」正是它要证明的对照支,退出码仍为 0(与 STATE.md 既有登记逐字一致)。
- **`p3` 是唯一自然渲染表格的样本,该读法由实跑坐实。** 受控探针实测 `#round-doc` 内 `tableCount=3`;`archive` 的轮次文档虽含表,但首屏渲染的是零表格行的 `DESIGN.md`,故 SC1 的「至少两张」指**表**不指**样本**。

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] 计划的 FAIL 判据在本项目恒非空 —— 它会命中一条标签里带 `FAIL` 一词的 PASS 行**

- **Found during:** Task 1 第 2 步(scope-blind-safe 判定)
- **Issue:** 计划把判据写死为 `grep -n 'FAIL' <log> | grep -v '0 FAIL'`,并在 `<prohibitions>` 里明令不得用 `grep -c 'FAIL'` 的裸计数。**该判据本身同样不成立** —— `check-05-full.log:399` 是一条 **PASS** 行,但它的标签文本里含 `FAIL` 一词:

  ```
  399:PASS [p1] 面板区滚动者集合 == {#main-pane, #chat-messages, #latest-check}: expected=[…] actual=[…]  # 口径取「恰好」而非「至多」:意外新增第四个滚动者会在这里 FAIL
  ```

  这是本项目已登记的「计数门是 scope-blind 的」坑的**新变体**:计划把注意力全放在「别数汇总行的 `0 FAIL`」上,而漏了「**门自己的 PASS 行标签里就写着 FAIL**」。**判别性证据:phase 9 自己的基线日志第 399 行逐字相同** —— 若照字面执行,phase 9 收口时那一次也会被判成「门红了」。
- **Fix:** 判据改为锚 verdict 行首形态的 `grep -nE '^FAIL'`(五份日志均为 0),并加**阳性对照**证明它非空转(`printf 'FAIL [p1] …' | grep -cE '^FAIL'` → `1`)。**不变量未被放宽**:修正式比原式更严 —— 原式把 PASS 行也算命中,修正式只看 verdict。`BLOCKED` 一侧同理核过:`check-05-full.log` 的非汇总行 `BLOCKED` 恰 2 条(第 215 / 216 行),**均在 item 5 内**,item 5 之外零 BLOCKED。
- **Files modified:** 无(判据措辞修正,零代码改动)
- **Verification:** 五份日志 `^FAIL` 计数 = 0 / 0 / 0 / 0 / 0;阳性对照返回 1 行;`check-05` 的非汇总 `BLOCKED` 全部落在 item 5
- **Committed in:** 不适用(零文件改动)

**2. [Rule 3 - Blocking] 计划 Task 3 的交付面装不下编排器要求的人眼取证图**

- **Found during:** Task 3 第 2 步(逐张自检)
- **Issue:** 计划 Task 3 的验收面是「`screenshots/` 下**恰好 5 个** PNG,文件名逐一对上 `p1` / `p12` / `p3` / `checking` / `archive`」,而 `--screenshot` 只产出这 5 张自然样本。但编排器派发说明明写:计划 02 遗留一条 `human_judgment: true`(其 D5,`.chat-user` 由 28px 大圆角变 10px 卡片圆角的观感),**入口是本计划产出的截图,且至少要有一张真的看得见 `.chat-user` 气泡**。实测 5 张自然截图**一张都没有**:`p1` 目录只有 `.gitkeep`、无 `transcript.md`,`p12` / `checking` / `archive` 的会话流也不含用户气泡 ⇒ 自然状态下该元素不存在。⇒ 计划字面的交付面**无法**承载编排器要求的证据。
- **Fix:** 用**应用自身**的 `appendChatMessage('user', …)` 造出探针气泡后再整窗截图(手法照抄 `scripts/check-05-ui-uat.py:876-879`,真实渲染路径、零 AI 调用、零网络、零手工拼 DOM),产物落在 **`screenshots/chat-user/p1-chat-user-evidence.png`** —— **另置子目录而非平铺**,使 `screenshots/` 顶层的 PNG 数仍恰为 5(计划的验收判据 `out_dir.glob("*.png")` 与 `ls` 都仍返回 5)。该图同为 1440×900,并附实测读数。
- **Files modified:** 新增 `screenshots/chat-user/p1-chat-user-evidence.png`(唯一新增产物;无任何既有文件被改)
- **Verification:** 顶层 PNG 计数 = 5 ✅;递归 `struct.unpack` 读 IHDR:6/6 全为 1440×900 ✅;实测读数 `.chat-user` 四角长手 `10px / 10px / 10px / 8px`、简写 `'10px 10px 8px'`、`--radius-md=10px` / `--radius-sm=8px`(与计划 02 的 r1 断言逐值相符);`git status --porcelain frontend/` 仍为空 ✅
- **Committed in:** `c07d973`(Task 3 提交)

**3. [Rule 1 - Bug] 计划 Task 2 的「`git status --porcelain frontend/` 必须非空且只含 `style.css`」在本执行方式下不可满足**

- **Found during:** Task 2 第 5 步(仓库卫生)
- **Issue:** 计划的 `fails_when` 写着「output contains any path other than `frontend/style.css`, **or output is empty**」,前提是「本阶段的 `style.css` 改动仍在工作树里」。但本阶段两处改动**已由计划 01 / 02 提交**,且本计划按 `<task_commit_protocol>` 逐任务提交 ⇒ 工作树在该判据运行时**不可能**是脏的。字面判据不可满足。(与计划 02 的 Deviation 2 同源 —— 计划里的若干判据建立在「改动尚未提交」的假设上。)
- **Fix:** 按判据的**意图**取证,不为了凑非空而制造改动:取 `git status --porcelain frontend/` **为空**(工作树干净 ⇒ 比字面要求更严格),另以 `git diff --stat ac5dcd3..HEAD -- frontend/style.css` 证明 `style.css` 确实带着本阶段的两处改动。
- **Files modified:** 无(取证方式修正,零代码改动)
- **Verification:** `git status --porcelain frontend/` 输出 0 行;`git status --porcelain scripts/` 输出 0 行;`git diff --stat ac5dcd3..HEAD -- frontend/style.css` → `1 file changed, 48 insertions(+), 5 deletions(-)`(证明改动在盘);`git diff --stat dd2caaf..HEAD -- frontend/style.css` → 空(证明**本计划**零产品改动)
- **Committed in:** 不适用(零文件改动)

**4. [Rule 1 - Bug] 计划的「零布局改动」措辞比事实更强 —— 一条未被点名的读数差 3px**

- **Found during:** Task 1 第 3 步(与 phase 9 基线逐行对照)
- **Issue:** 计划 `must_haves` 写着「本阶段零宽度改动、**零布局改动**」,并要求 item 8 的 L-2 / sticky 原始读数「逐值相同」。**计划点名的那几条读数确实逐值相同**(见上文对照表),但同一次输出里另有一条读数不同:`item8 [p3] L-5 clearance: #round-doc × #doc-panel` 的 `height` 由 `778.640625` 变为 `775.640625`(**−3px**),连带 `#btn-authorize` 的 clearance 由 `-124.6px` 改善到 `-121.6px`。
- **Fix:** 用**同一次导航内的受控 A/B** 证明成因(而非推断):注入只还原被改属性的覆盖样式后重测,得 `DELTA docH = 3.0`、`DELTA per-table = [1.0, 1.0, 1.0]`。机制:计划 01 把表格的 `border: 1px solid`(四边)就地改为 `border: none` + `border-bottom: 1px solid`,表格盒顶边消失 ⇒ 每张表矮 1px;`p3` 当前轮恰有 3 张表 ⇒ 共 3px。**这是计划 01 那处改动的必然机械后果。** 该读数上的**断言**(item 9 的 `L-5 clearance >= 4px`)实测未达标集为 `[]`、PASS,方向与计划预判一致(表更矮/更窄)。⇒ **无需重新登记,零门改动**;仅更正计划措辞。
- **Files modified:** 无(记录与措辞更正,零代码改动)
- **Verification:** 受控 A/B 输出见上文;item 9 的 `L-5 未达标 []` PASS;`L-2` 三宽度的 `scrollWidth` / `clientWidth` / `docPanelWidth` 与 sticky 坐标逐值相同
- **Committed in:** 不适用(零文件改动)

---

**Total deviations:** 4 auto-fixed(4 Rule 1 + 1 Rule 3 —— 其中第 4 条同时是 Rule 1)
**Impact on plan:** 零产品代码改动、零门改动、零范围变化。第 1 条修正的是**判据的措辞**(修正式更严);第 2 条补上计划交付面装不下的证据(唯一新增产物,且不破坏计划的计数判据);第 3 条修正取证方式(判据意图不变);第 4 条是**计划的措辞比事实更强**的记录与更正(事实本身无缺陷)。四条的共同成因:**计划里若干判据建立在「改动尚未提交」或「按子串搜即可」的假设上,且「零布局改动」这句措辞未把盒模型效应算进去** —— 与计划 01 / 02 已登记的同类教训同族。

## Issues Encountered

- **`probe-05` 的 1 条 `BLOCKED` 是变异证明的对照支,不是门失败。** 该探针在同一份被变异的样式表上跑同一条断言两次:原文为 `PROBE mutated-prefix-verdict=PASS` / `PROBE mutated-postfix-verdict=BLOCKED`,并另有 `PASS [control] .hint color == var(--color-text-muted): expected=rgb(100, 100, 100) actual=rgb(100, 100, 100)` 的未变异对照支。退出码 `0`。与 STATE.md 既有登记逐字一致。
- **`probe-07` 的焦点环地面仍是卡片白(实测 3.54)。** 原文:`PROBE composite ring=(31, 99, 189) ground=rgb(255, 255, 255) alpha=0.75 composited=(87, 138, 206) ratio=3.54 (>= 3.0)`。这是 Phase 9 卡片化之后 `#round-doc` 最近不透明祖先变为 `#doc-panel` 的结果,已在 STATE.md 登记为「往更容易的方向漂,不得被读成仍在证明 `--color-surface` 上的算术」;断言形式与强度一字未变、退出码仍为 0,本计划不改动它。
- **本机 8765 端口仍存在先前遗留的 uvicorn 进程**,五条浏览器门与两次一次性探针全部走了「复用,不新起、结束时也不关闭」分支(日志首行 `INFO server: 127.0.0.1:8765 已在服务`)。读数不受影响(被测页面仍是本仓库的 `frontend/`),但意味着这些证据不是在全新进程上取得的 —— 与 STATE.md 的既有登记一致。
- **`state.*` 动词第十四次复现**(见 STATE.md 本次新增条目),已逐条核盘修正。核盘放在收口序列的**最后一个动词之后**。
- **未使用 `gsd-tools windows append`** —— 本计划零 stub、零跳过测试、零未跑的 `<verify>`、四条 deviation 均为**判据措辞 / 取证方式 / 交付面**层面且零产品代码改动,无跨阶段缺陷需登记进 `WINDOWS.md`;四条 deviation 完整记于本 SUMMARY 与 STATE.md。

## Known Stubs

None —— 本计划未引入任何 stub、占位文案或硬编码空值。新增的 12 份日志是门的**完整未截断** stdout;6 张 PNG 是真实浏览器的整窗截图,逐张以 IHDR 实测 1440×900。5 张状态样本截图由 `check-10 --screenshot` 在真实浏览器里逐样本导航后产出(每张都带 `shot [<state>] 截图落盘且为 1440×900` 的 PASS 行),`.chat-user` 取证图由应用自身的 `appendChatMessage('user', …)` 渲染路径产出 —— 无一张是合成页或手工拼 DOM 的产物。

## Threat Flags

None —— 本计划**零产品代码改动、零新增依赖、零新增网络调用**。`<threat_model>` 的六条 `mitigate` 项逐条落地:

| Threat ID | 缓解计划 | 实测 |
|---|---|---|
| T-idi-10-01 | 截图与日志落 `.planning/` 下、不进 `frontend/` | `git status --porcelain frontend/` 为空 ✅ |
| T-idi-10-02 | 「把门跑绿」的诱惑 —— 只允许重新登记、`check-05` 列入禁止改动 | `git diff -- scripts/check-05-ui-uat.py` 为空;`git status --porcelain scripts/` 为空 ⇒ **门改动零处** ✅ |
| T-idi-10-03 | 「门绿了」须有原始证据;计数门是 scope-blind 的 | 12 份逐门原文未截断落盘;判据锚 `^FAIL` 并做阳性对照 ✅ |
| T-idi-10-04 | 必须走 `--browser bundled`(本机 `channel="chrome"` + headless 挂死) | 全部浏览器门走 `.venv/bin/python … --browser bundled`/默认 bundled,零挂死 ✅ |
| T-idi-10-05 | 截图 / 日志落点不得进 `frontend/` | 同上;`ls frontend/vendor/` 仅 `marked.min.js` ✅ |
| T-idi-10-06 | 不触碰鉴权 / 权限门 / 服务端路径 | 本计划零代码改动 ✅ |
| T-idi-10-SC | 本阶段零安装、零新增依赖 | `frontend/vendor/` 仍只有 `marked.min.js`;零 pip / npm 安装 ✅ |

## 开放项(本阶段未构建,只登记)

**沿用上阶段的口径,用户本次仍未点名的四条 Phase 9 开放项:**

| # | 开放项 | 现状(实测 / 源码) | 本阶段为何不动 |
|---|---|---|---|
| 1 | `.overlay-card` 的底色 | `frontend/style.css:988` 为 `background: var(--color-surface)`(gray-2)+ `--shadow-overlay`。页面已下沉到 gray-3,它比主界面白卡片内陷一档 —— `archive.png` 里「使命完成」弹窗即该元素 | 是否改白 = **设计决策**,用户本次未点名 |
| 2 | 页面级留白 | 本阶段没给 `#main-pane` 加 `padding`、也没给卡片加 `margin` | 是否留白 = **未裁定项** |
| 3 | 输入框在白卡片上的填充 | 应用的文本 input 一律不声明 `background`,故画的是 **UA 字段白填充**,不构成 gray-2 内陷面 | 是否该带一层内陷底 = **设计决策** |
| 4 | 图标与空状态 | 未构建 | 用户本次未点名的第三项候选 |

**Out of Scope 的重申:** 表格重做与圆角刻度收敛已在本阶段**完成**;图标与空状态、暗色模式**仍未点名**,**不得预先构建**(`.planning/REQUIREMENTS.md` §Out of Scope)。

**本阶段的实现观察(不构建,只记录):** `--radius-lg` 的删除让圆角刻度与 `04-UI-SPEC.md` 的圆角账本之间的对齐问题浮出水面 —— 该账本(`.planning/milestones/v1.14-phases/idi-04-tokens-contract/04-UI-SPEC.md:545-547`)至今写着 `--radius-sm: 4px` / `--radius-md: 8px` / `--radius-pill: 999px`,**既没有 `8px / 10px` 这组值,也没有本阶段的三档语义描述**(卡片档 / 控件档 / 胶囊档)。是否回填账本是**文档层的独立事项**,不在本阶段边界内。

**用户评审点(本阶段唯一的未闭合出口,不是缺陷):** 本阶段真正的终点是**用户看过截图后的设计裁定** —— 表格的新形态是否读作「白卡片内的一个内陷块」(D5)、`.chat-user` 的 10px 圆角是否与 Phase 9 的卡片语言同族(D6)、以及上述四条开放项是否另开 phase。`gate-logs/` 12 份原始 stdout 与 6 张截图构成可独立复核的评审记录。

## Next Phase Readiness

- **计划 04(`idi-09` 的连带指纹重验)可以开工。** 本计划的五条浏览器门复跑与四个静态门构成它的前置证据面;`REQUIREMENTS.md` 的 `REG-03` 勾选由计划 04 触发(共享-ID 门实测 `blocked: [REG-03]`,见下)。
- **计划 04 必须复核本计划登记的那条 3px 发现** —— 它证明「本阶段零布局改动」这句措辞需要按「零 `padding`/`margin`/宽度/定位改动」读。若 `idi-09-VERIFICATION.md` 的连带重验引用了 `#round-doc` 的绝对高度读数,须按同一机制解释。
- **`REQUIREMENTS.md` 的勾选:`TABLE-01` / `TABLE-02` / `RADIUS-01` / `RADIUS-02` 由本计划触发**(它们此前被共享-ID 门拦在计划 01 / 02);`REG-03` **不由**本计划触发 —— `requirements.ready-ids` 实测返回 `ready: [TABLE-01, TABLE-02, RADIUS-01, RADIUS-02]` / `blocked: [REG-03]`(`idi-10-04-PLAN.md` 也声明了 `REG-03`),按 #2388 只勾选 ready 子集。
- **`screenshots/` 的读法已写进本 SUMMARY**,使计划 04 与后续 verifier 不必重新推断:`p3` 是唯一自然渲染表格的样本,SC1 的「至少两张」指表不指样本;`.chat-user` 的取证图在 `chat-user/` 子目录。
- **待决出口**:用户评审(表格形态 D5 / `.chat-user` 观感 D6 / 四条开放项)与本阶段收口的 `/gsd-verify-work idi-10`。本计划不代其收口。

## Self-Check: PASSED

- 三个任务提交均在盘:`git log --oneline` 含 `a98c788`(Task 1)/ `712ef40`(Task 2)/ `c07d973`(Task 3);`commits: 3` 由 `git rev-list --count dd2caaf..HEAD` **实测**(非叙述),`plan_head_before: dd2caafb75d53ae2e3e11b5539193a85d1da5d0d` 取自落盘 ledger
  - **口径说明(免得被读成漂移):** `commits: 3` 数的是**本计划的三个任务提交**,测量点是 SUMMARY 落盘时(与计划 01 的 `2`、计划 02 的 `3` 同一口径)。其后的两次收口提交(`b3feb48` SUMMARY、`07a34d6` 状态更新)按本项目既有惯例不计入该字段;故 `git rev-list --count dd2caaf..HEAD` 在收口全部完成后返回 **5**。两个数都对,差的是测量时点。
- 12 份日志文件全部存在于 `gate-logs/`;6 张 PNG 全部存在于 `screenshots/`(顶层 5 + `chat-user/` 1)
- 五条浏览器门实跑:check-05 `exit=2`(设计如此,零 FAIL,BLOCKED 仅 item 5 的 2 条 `--ai-smoke` 腿)、check-06 / check-07 / probe-05 / probe-07 均 `exit=0`
- 四个静态门 `PASS`(`check-02` 为 `PASS: 0 failures`);pytest(项目 `.venv`)`219 passed, 6 skipped`;`node --check frontend/app.js` `exit=0` 零输出
- 零门改动:`git diff -- scripts/check-05-ui-uat.py` 为空、`git status --porcelain scripts/` 为空;零产品改动:`git status --porcelain frontend/` 为空、`git diff --stat dd2caaf..HEAD -- frontend/style.css` 为空
- 5 张状态样本 PNG 的 IHDR 逐张实测 `1440×900`;`screenshots/chat-user/p1-chat-user-evidence.png` 同为 `1440×900`

---

*Phase: idi-10-tables-and-radius-scale*
*Completed: 2026-09-27*

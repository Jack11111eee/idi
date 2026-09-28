---
phase: idi-10-tables-and-radius-scale
plan: 03
type: execute
wave: 3
depends_on:
  - idi-10-02
files_modified:
  - .planning/phases/idi-10-tables-and-radius-scale/screenshots/
  - .planning/phases/idi-10-tables-and-radius-scale/gate-logs/
autonomous: true
requirements:
  - TABLE-01
  - TABLE-02
  - RADIUS-01
  - RADIUS-02
  - REG-03

estimate:
  tokens: 40000
  raw_tokens: 40000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- REG-03 — 五条浏览器门是真正的回归面 ----
    - "`.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` 的 `=== 逐项结论 ===` 块里**没有任何** `FAIL`;退出码为 `2`;`BLOCKED` 只出现在 item 5 的两条 `--ai-smoke` 腿(无 `--ai-smoke` 时按设计不跑,**不是回归**)"
    - "`.venv/bin/python scripts/check-06-idi05-validation.py` 退出码为 `0`;`.venv/bin/python scripts/check-07-idi08-validation.py` 退出码为 `0`"
    - "`.venv/bin/python scripts/probe-05-resolve-color.py` 退出码为 `0`;`.venv/bin/python scripts/probe-07-focus-composite.py` 退出码为 `0`"
    - "本次复跑与 `.planning/phases/idi-09-card-containers/gate-logs/check-05-full.log` 的 `=== 逐项结论 ===` 块**逐项同形** —— 10 个 item 的断言数与 FAIL / BLOCKED 分布均与 phase 9 收口时一致(item 5 两条 `--ai-smoke` 腿按设计 BLOCKED、其余全 0 FAIL / 0 BLOCKED)。任何一项的数量差异都要在 SUMMARY 里给出成因"
    - "`check-05` 的 `[p1] .markdown-body td font-size == var(--text-base)` 为 PASS(不是 BLOCKED)—— 它锁死的是 `td` 的 `font-size`,而本阶段一字未动该属性"
    - "`check-05` item 8 的三条 `badge × banner 不相交`(768 / 1024 / 1280px)与三条 `#doc-panel 实测宽 <= clamp(340px, 30vw, 480px) 上界` 仍 PASS,且其 INFO 行的原始读数与 phase 9 的同名读数**逐值相同**(本阶段零宽度改动、零布局改动)。**本阶段去掉表格竖线只会让表更窄,方向安全** —— 但这是**实测**结论:两侧的 `scrollWidth` / `clientWidth` / `docPanelWidth` 数字都要抄进 SUMMARY"
    - "`check-05` item 4 的 `#doc-panel-body padding == \"32px 40px\"`、`.panel-header padding-top`、`button padding-top`、`.overlay-card padding-top` 四条几何断言仍 PASS —— 本阶段的改动只落在 `.markdown-body` 的表格规则与两处 `border-radius`,不触碰任何内边距"
    - "`check-05` item 9 的面板区滚动者普查(口径是「**恰好** `{#main-pane, #chat-messages, #latest-check}`」)仍 PASS;`check-05` item 2 的 `#round-doc` 正文对比度断言(≥4.5)仍 PASS —— 它取的是 `effective_bg(\"#round-doc\")`,而本阶段不改任何底色"
    - "`check-06` 的 g3 / g5 / g6 全 pass:**g6 的两条 `box-shadow 恒 none` 对照组**(`#ai-panel-header` / `#doc-panel-header`)与 `#doc-panel.collapsed` 折叠往返仍成立 —— 本阶段零 `box-shadow` 改动;g5 的 340px 最窄面板单行 / 不裁切断言仍成立 —— 本阶段零宽度改动"
    - "`.venv/bin/python scripts/check-10-idi10-validation.py --item t1 --item t2 --item r1 --item r2` 仍 `exit=0`、0 FAIL / 0 BLOCKED(本阶段自建的门在阶段末尾仍全绿)"
    - "每一条被判定为「门断言的事实被本阶段刻意改变」的失败,其期望侧都以**重新登记**处置 —— 断言形式(等值 / 阈值 / 几何判据)一字不变,只换指到新事实;没有任何一条被改成弱判据、被跳过、被删除。每一处门改动都在 SUMMARY 里逐条列出并给出理由。**预期为零处**"
    # ---- 静态门与基线 ----
    - "四个静态门(check-01 / check-02 / check-03 / check-04)全部打印 `PASS`(`check-02` 为 `PASS: 0 failures`)"
    - "`.venv/bin/python -m pytest backend/tests -q --tb=short` 的输出为 `219 passed, 6 skipped`,与基线逐字一致(**必须**用项目 `.venv` —— 环境 `python3` 是 miniconda,会让 4 个 `ai_caller` 测试假失败,把基线误判成回归)"
    - "`node --check frontend/app.js` 退出码 0(`app.js` 本阶段零字节改动,这条是形式化复核)"
    - "`git status --porcelain frontend/` 只列出 `frontend/style.css`;`ls frontend/vendor/` 只有 `marked.min.js`"
    - "**本阶段不得改动 `scripts/check-05-ui-uat.py`**(它在 `idi-08` 的 `covered_files` 里,`idi-08` 不含 `frontend/style.css`)—— 改它会把连带指纹的重验面从 1 份变成 2 份。判据:`git diff -- scripts/check-05-ui-uat.py` 相对 HEAD **为空**"
    # ---- 截图(ROADMAP Deliverables)----
    - "`.planning/phases/idi-10-tables-and-radius-scale/screenshots/` 下存在覆盖 5 个状态样本(p1 / p12 / p3 / checking / archive)的 PNG,每张都是 1440×900 的整窗截图"
    - "截图里可见表格改造的机械后果:文档区表格**没有竖线与外框**、表头有一条浅灰底、行间有极浅的横向分隔线。ROADMAP SC1 的「截图仍须取到**至少两张**作为证据」指的是**表**、不是**样本** —— 它紧接在「三个机器可解析表(批注回应表 / 覆盖维度表 / 未决问题清单)在截图里读数一致」之后,是在要求这三张表里至少取到两张的可见证据。而这三张表**同属一份文档**:`p3` 的当前轮是第 2 轮,`#round-doc` 首屏渲染 `scripts/ui-states/p3/docs/discuss-round-2.md`,该文件的 §1 / §2 / §3 正是这三张表(实测 `^|` 行 15 行,含三张表的表头与数据行)。⇒ **判据是「`p3` 的截图里同时可见这三张机器可解析表」**(三 ≥ 二,自动满足「至少两张」),**不是**「两个不同样本各自有表」"
    - "截图里可见圆角收敛的机械后果:`.chat-user` 气泡是 10px 卡片圆角(不再是 28px 的大圆角),其右下角仍是 8px 尖角;`#chat-input-row` 的输入框外观与收敛前一致"
    # ---- 原始证据 ----
    - "`.planning/phases/idi-10-tables-and-radius-scale/gate-logs/` 下每个门一个日志文件(文件名即门的名字),内含该门的**完整原文**输出(未被 head / tail 截断),供独立复核 —— 不是只记「绿」"

  artifacts:
    - path: ".planning/phases/idi-10-tables-and-radius-scale/screenshots/"
      provides: "5 个状态样本的 1440×900 整窗截图,供用户评审表格重做与圆角收敛的机械后果"
    - path: ".planning/phases/idi-10-tables-and-radius-scale/gate-logs/"
      provides: "五条浏览器门 + 四个静态门 + pytest + 新运行时门的原始 stdout,一个门一个文件"
    - path: ".planning/phases/idi-10-tables-and-radius-scale/idi-10-03-SUMMARY.md"
      provides: "五条浏览器门的复跑记录(含 check-05 全量结果与 item 5 两条 BLOCKED 腿的按设计说明、与 phase 9 基线的逐项对照)、四静态门原文、pytest 基线、门改动逐条登记(预期零处)、截图路径与逐张说明、开放项清单"

  key_links:
    - from: "`scripts/check-10-idi10-validation.py` 的 `--screenshot DIR`"
      to: "`.planning/phases/idi-10-tables-and-radius-scale/screenshots/*.png`"
      via: "Playwright 的 `page.screenshot()`,每进入一个状态样本出一张图,并逐张断言 1440×900"
      pattern: "screenshot"
    - from: "五条浏览器门"
      to: "本阶段改动后的渲染语义"
      via: "它们断言的是 computed style 与几何 —— 静态 grep 对渲染结果零证明力,只有它们能证明「表格重做 + 圆角收敛」之后既有行为仍然成立"
      pattern: "exit="
    - from: "`grep -n 'FAIL' <log> | grep -v '0 FAIL'` 的输出为空"
      to: "「门里真的没有 FAIL」这一结论"
      via: "**计数门是 scope-blind 的**:`grep -c 'FAIL'` 会把汇总行里的 `0 FAIL` 也数进去(本项目为此红过一次)⇒ 判据必须取「含 FAIL 词但不含 `0 FAIL` 的行」,不能取 `grep -c` 的裸计数"
      pattern: "grep -n 'FAIL' | grep -v '0 FAIL'"
    - from: "`check-05-full.log` 的 INFO 原始几何读数"
      to: "phase 9 的 `gate-logs/check-05-full.log` 同名读数"
      via: "逐值对照 —— 本阶段零布局改动,故 L-2 的 `scrollWidth` / `clientWidth` / `docPanelWidth` 与 sticky 的 header/panel 坐标应逐值相同"
      pattern: "docPanelWidth"

  prohibitions:
    - statement: "不得为了把门跑绿而放宽任何判据。允许的门改动**只有一种**:门断言的事实被本阶段**刻意改变**了,此时把期望侧重新登记到新事实,断言形式与强度一字不变。**禁止**改阈值、改 `TEXT_MIN` / `NON_TEXT_MIN`、把等值断言降为子串 / 「非空」/ 「非透明」判据、加 `or` 分支、把断言标成跳过、删除断言、给门加白名单。本阶段规划期已逐条普查,**预期零处门改动**"
      status: active
      verification: flagged
    - statement: "**不得改动 `scripts/check-05-ui-uat.py` 的任何一行。** 它在 `idi-08` 的 `covered_files` 里(`idi-08` 不含 `frontend/style.css`),改它会把它也拖进连带指纹重验名单,把重验面从 1 份变成 2 份(ROADMAP Deliverables 与 Pitfalls 逐字写明)。若实跑发现某条 `check-05` 断言确实被本阶段的改动打破,处置是**停下报回**并给出原始输出 —— **不是**就地改它"
      status: active
      verification: flagged
    - statement: "不得把 `BLOCKED` 当 `PASS` 解释。`check-05` 的 `ok()` 在元素读不到或令牌解析不出时记 `BLOCKED`,那是「探针没读到」而不是「行为正确」。本阶段允许的 `BLOCKED` 只有 item 5 的两条 `--ai-smoke` 腿(无 `--ai-smoke` 时按设计不跑);任何**新增** `BLOCKED` 都按失败处理,必须查明原因"
      status: active
      verification: flagged
    - statement: "不得用 `grep -c 'FAIL'` 的裸计数下「门是绿的」结论 —— 该计数会把汇总行里的 `0 FAIL` 数进去(本项目已为此红过一次)。判据一律写成 `grep -n 'FAIL' <log> | grep -v '0 FAIL'` 的行为空"
      status: active
      verification: flagged
    - statement: "不得用 `channel=\"chrome\"` 跑 `check-05`。本机 `.venv` 的 Python 是 x86_64(Rosetta),`channel=\"chrome\"` + `headless=True` 会让 CDP 永不连上、超时挂死。必须走 `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled`(Playwright 自带 chromium 已缓存,零下载)"
      status: active
      verification: flagged
    - statement: "pytest **必须**用项目 `.venv`(`.venv/bin/python -m pytest`)。环境的 `python3` 是 miniconda,会让 4 个 `ai_caller` 测试假失败,把「219 passed / 6 skipped」误判成回归"
      status: active
      verification: flagged
    - statement: "不得把截图或日志写进 `frontend/`。ROADMAP 的 Gate 要求 `git status --porcelain frontend/` 仅含预期文件;截图落 `.planning/phases/idi-10-tables-and-radius-scale/screenshots/`,日志落同阶段的 `gate-logs/`"
      status: active
      verification: flagged
    - statement: "不得在 harness 里手工拼 DOM 伪造被测状态,不得改动被测样本(`scripts/ui-states/`)。需要构造状态时走应用自身已导出的函数与 `c05.make_fixture` 的副本隔离(与既有 item 的做法一致);`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` 零字节改动"
      status: active
      verification: flagged
    - statement: "不得在本计划里新增功能或「顺手」修视觉细节。本阶段的范围边界是表格重做 + 圆角刻度收敛 + 门禁复跑 + `idi-09` 的连带指纹重验 + 截图;图标与空状态 / 暗色模式 / `.overlay-card` 底色 / 页面级留白 / 输入框 UA 白填充全部**不在本阶段**(用户本次未点名的四项 Phase 9 开放项)。发现的问题只登记进 SUMMARY 的开放项,不就地构建"
      status: active
      verification: flagged
---

<objective>
用本仓库唯一能证明「渲染语义仍然成立」的机器 —— 五条真实浏览器门 —— 复核本阶段的两处改动,并产出供用户评审的截图与逐门原始日志。

Purpose: 本阶段是纯 CSS 的**构图**改动,它的成败判据不是「CSS 里写下了什么」而是「浏览器里画出来什么」。`grep -c 'var(--'` 对渲染结果零证明力。而本阶段改的两处恰好都踩在回归面上:表格规则动了 `.markdown-body` 里被 `check-05` 断言过的元素族(`td` 的 `font-size` 被活断言锁死),圆角动了 `--radius-lg` 这个被零个门引用、但**删错相邻令牌(`--radius-md`)就会红**的位置。计划 01 / 02 已在规划期逐条普查并识别出**零处**会被打破的断言 —— 本计划的任务是把这件事在实跑中证成:全绿,或把新发现逐条分诊。

**为什么预期零处门改动(逐条口径,不是乐观):**

| 被盯住的断言 | 为什么应当存活 |
|---|---|
| `check-05` `[p1] .markdown-body td font-size == var(--text-base)` | 本阶段**一字未动** `td` 的 `font-size`;且期望侧由 `resolve_token` 运行时解析 ⇒ 值层不改就恒过 |
| `check-05` item 8 的 L-2 三宽度溢出诊断 | 它测的是**文档级 `scrollWidth`** 与 `#doc-panel` 的**实测宽 vs 声明上界**。去掉表格竖线只会让表更窄(方向安全),`#doc-panel` 的宽由 `clamp(340px, 30vw, 480px)` 决定,表格内容更窄不会把它顶破 |
| `check-05` item 4 的四条几何断言 | 本阶段只改表格的 `border` / `background` 与两处 `border-radius`;不触碰任何 `padding` / `margin` |
| `check-05` item 9 的滚动者普查(口径「恰好」) | 本阶段零 `overflow` 改动 |
| `check-05` item 2 的 `#round-doc` 正文对比度 | 它取 `effective_bg("#round-doc")`,本阶段不改任何底色 ⇒ 地面与比值都不变 |
| `check-06` g6 的两条 `box-shadow 恒 none` 对照组 + `#doc-panel.collapsed` 折叠往返 | 本阶段零 `box-shadow` 改动、零 `#doc-panel` 改动 |
| `check-06` g5 的 340px 最窄面板单行 / 不裁切 | 本阶段零宽度改动 |
| `check-09` c1 / c2 的卡片圆角断言 | 它动态解析 `--radius-md`,而本阶段**保留**该令牌(计划 02 已把这条作为禁令并复跑验证) |
| 四个静态门 | `check-01`(围栏外裸 hex / tier-1 引用)与 `check-04`(`!important;` 声明数)对本阶段的改动结构性失明;`check-02` 零清单增删;`check-03` 零 `.hidden` 改动 |

**⚠ 计数门是 scope-blind 的(本项目已为此红过一次)。** `grep -c 'FAIL'` 会把汇总行里的 `0 FAIL` 也数进去。本计划所有「门里没有 FAIL」的判据一律写成 `grep -n 'FAIL' <log> | grep -v '0 FAIL'` 的**行为空**,不得用 `grep -c` 的裸计数下结论。

**分诊流程(对每一条新出现的 FAIL / 新增 BLOCKED 逐条执行)。** 问一个问题:**这条门断言的事实,是不是本阶段刻意改变的?**

- **是** ⇒ 处置 = **重新登记**:把期望侧换指到新事实,断言形式与强度**一字不变**;改完必须**重跑该门**证明回到绿,并把改动逐条写进 SUMMARY(改哪一行 / 旧期望 / 新期望 / 依据哪条裁定)。**但 `check-05` 属于禁止改动清单**(见 `<prohibitions>`),若它红,处置是停下报回。
- **否** ⇒ 处置 = **产品缺陷**:停下,把失败原文、涉及的 CSS 声明、以及为什么不是「事实被刻意改变」写进 SUMMARY,作为未关闭项报回。**不要**就地改 `frontend/style.css`(本计划对产品代码零改动),也**不要**用放宽判据的方式绕过去。

Output: 五条浏览器门的复跑记录(逐门日志文件)、四个静态门 + pytest 基线的复核、5 个状态样本的截图、以及一份写明门改动(预期零处)与开放项的 SUMMARY。

**前置(执行前须复核,由 `idi-10-01` / `idi-10-02` 落地):** 表格规则已改造、`--radius-lg` 已删除、两处消费者已改归属。复核方式:`.venv/bin/python scripts/check-10-idi10-validation.py --item t1 --item t2 --item r1 --item r2`(应全绿)与 `grep -cF -- '--radius-lg' frontend/style.css`(应为 `0`)。

**本计划不触碰:** `frontend/style.css` 与 `scripts/` 下所有文件(零改动 —— 若门红且分诊结论是产品缺陷,则停下并把结论报回,不就地改);`frontend/app.js` / `index.html` / `vendor/` 零字节。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/REQUIREMENTS.md
@.planning/phases/idi-10-tables-and-radius-scale/10-CONTEXT.md
@.planning/phases/idi-10-tables-and-radius-scale/idi-10-01-SUMMARY.md
@.planning/phases/idi-10-tables-and-radius-scale/idi-10-02-SUMMARY.md
@.planning/phases/idi-09-card-containers/idi-09-03-PLAN.md
@scripts/check-05-ui-uat.py
@scripts/check-10-idi10-validation.py
</context>

## Artifacts this phase produces

> 本节的用途:**plan-review-convergence 的 source-grounding pass 读它,把本阶段新建的符号从漂移校验里排除**。
> 本节列出**全阶段**(四个计划)的产出;本计划只登记自己那部分。

**本计划新增 / 填充的产物目录:**

| # | 路径 | 备注 |
|---|---|---|
| 3 | `.planning/phases/idi-10-tables-and-radius-scale/screenshots/` | **03** —— 5 个状态样本的 1440×900 整窗截图(由计划 01 实现的 `--screenshot` 产出) |
| 4 | `.planning/phases/idi-10-tables-and-radius-scale/gate-logs/` | **03**(五条浏览器门 + 四静态门 + pytest + node check)/ 04(补一份指纹复核日志)—— 一个门一个日志文件,文件名即门的名字 |

**日志文件名约定(与 Phase 9 的 `gate-logs/` 同名同规格):**

```
check-01-token-conformance.log      check-06-idi05-validation.log
check-02-contrast.log               check-07-idi08-validation.log
check-03-hidden-uniqueness.log      probe-05-resolve-color.log
check-04-important-count.log        probe-07-focus-composite.log
check-05-full.log                   check-10-idi10-validation.log
pytest.log                          node-check-app.log
```

**本计划明确不产生的新符号:** 零新增代码文件、零新增令牌、零新增 CSS 规则、零新依赖、零新构建步骤;`frontend/style.css` 与 `scripts/` 下全部文件在本计划内零改动。

## 五条浏览器门的复跑口径(逐条,含已知的按设计结果)

| 门 | 命令 | 期望结果 | 已知的按设计非绿项 |
|---|---|---|---|
| `check-05` | `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` | `=== 逐项结论 ===` 块零 `FAIL`;`exit=2` | item 5 的两条 `--ai-smoke` 腿在无 `--ai-smoke` 时 `BLOCKED` ⇒ 退出码 2。**这是设计如此,不是回归** |
| `check-06` | `.venv/bin/python scripts/check-06-idi05-validation.py` | `exit=0` | 无 |
| `check-07` | `.venv/bin/python scripts/check-07-idi08-validation.py` | `exit=0` | 无 |
| `probe-05` | `.venv/bin/python scripts/probe-05-resolve-color.py` | `exit=0` | 无(它是变异证明,不是门) |
| `probe-07` | `.venv/bin/python scripts/probe-07-focus-composite.py` | `exit=0` | 无(同上) |

<tasks>

<task type="auto" tdd="false">
  <name>Task 1: 五条浏览器门复跑 + 失败分诊 + 逐门原始日志落盘</name>
  <files>.planning/phases/idi-10-tables-and-radius-scale/gate-logs/</files>
  <precondition>.venv/bin/python 可导入 playwright 且自带 chromium 已缓存;`grep -cF -- '--radius-lg' frontend/style.css` 输出 `0`,且 `.venv/bin/python scripts/check-10-idi10-validation.py --item t1 --item t2 --item r1 --item r2` 全绿</precondition>
  <reversibility rating="reversible">门复跑本身可重跑;本计划对产品代码与门代码零改动,失败只暴露问题、不引入问题。</reversibility>
  <read_first>
    - `scripts/check-05-ui-uat.py` 文件头的运行方式块与「本机 `.venv` 是 x86_64(Rosetta),`channel="chrome"` + `headless=True` 会挂死」的环境事实 —— **必须走 `--browser bundled`**
    - `scripts/check-05-ui-uat.py` 的 `_emit()` 输出格式(`PASS|FAIL|BLOCKED <label>: expected=… actual=…`)与 `ok` / `ok_true` / `blocked` / `info` / `item_verdict` 的语义(两处 BLOCKED 分支)
    - `scripts/check-05-ui-uat.py` 的 `main()` 派发与汇总块:`item N: VERDICT  (n 条断言,f FAIL,b BLOCKED)` 与 `exit={code}`(0=全 pass / 1=有 fail / 2=有 blocked)
    - `scripts/check-05-ui-uat.py` 的 `[p1] .markdown-body td font-size == var(--text-base)` 断言 —— **本阶段的关键对照物**:它锁死的是 `td` 的 `font-size`,而本阶段一字未动
    - `scripts/check-05-ui-uat.py` 的 item 8(L-2 三宽度溢出 + sticky 表头 + `badge × banner`)、item 9(面板区滚动者普查,口径「恰好」)、item 4(四条 padding 几何)、item 2(`#round-doc` 正文对比度)—— 本阶段最可能被误伤的五组,逐组确认应存活
    - `scripts/check-06-idi05-validation.py` 的 g3 / g5 / g6(两条 `box-shadow 恒 none` 对照组 + `#doc-panel.collapsed` 折叠往返 + 340px 最窄面板单行)
    - `scripts/check-07-idi08-validation.py` 文件头的四条行为断言映射(Escape / dialog 语义 / 菜单不复弹 / 焦点交还)
    - `scripts/probe-05-resolve-color.py` 与 `scripts/probe-07-focus-composite.py` 的「变异证明」性质与运行方式
    - `.planning/phases/idi-09-card-containers/gate-logs/check-05-full.log` —— **基线对照**:phase 9 收口时的 `=== 逐项结论 ===` 块(10 个 item 的断言数与 FAIL / BLOCKED 分布)与 item 8 的 L-2 / sticky INFO 原始读数
    - `.planning/phases/idi-10-tables-and-radius-scale/10-CONTEXT.md` §「门禁环境事实(省得重踩)」
  </read_first>
  <action>
    **第 1 步 —— 逐条复跑五条门,并把原始输出**逐门**落到 `gate-logs/`。**

    先 `mkdir -p .planning/phases/idi-10-tables-and-radius-scale/gate-logs`。按上面的复跑口径表逐条执行,把每条的**完整 stdout**写进同名日志文件(重定向即可):

    - `check-05-full.log` ← `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled`
    - `check-06-idi05-validation.log` ← `.venv/bin/python scripts/check-06-idi05-validation.py`
    - `check-07-idi08-validation.log` ← `.venv/bin/python scripts/check-07-idi08-validation.py`
    - `probe-05-resolve-color.log` ← `.venv/bin/python scripts/probe-05-resolve-color.py`
    - `probe-07-focus-composite.log` ← `.venv/bin/python scripts/probe-07-focus-composite.py`

    日志必须是**原文**(不要 `head` / `tail` 截断 —— 截断会让「没有 FAIL」这个结论无法被独立复核)。每条命令的**退出码**要记录(追加到日志尾部或写进 SUMMARY)。

    **第 2 步 —— 用 scope-blind-safe 的方式判定「没有 FAIL」。**

    对每个日志跑 `grep -n 'FAIL' <log> | grep -v '0 FAIL'`,输出必须为**空**。⚠ **不得**用 `grep -c 'FAIL' <log>` 的裸计数下结论 —— 汇总行里的 `0 FAIL` 会被它数进去(本项目已为此红过一次)。

    对 `check-05-full.log` 还要单独核对:任何**非汇总行**的 `BLOCKED` 都必须落在 item 5 内。任何 **item 5 之外**的 BLOCKED 都按失败处理。

    **第 3 步 —— 与 phase 9 基线逐项对照。**

    把本次 `check-05-full.log` 的 `=== 逐项结论 ===` 块(10 行的 `item N: VERDICT  (n 条断言,f FAIL,b BLOCKED)` + 末行 `exit=`)与 `.planning/phases/idi-09-card-containers/gate-logs/check-05-full.log` 的同名块**逐项对照**,把两边一并抄进 SUMMARY。断言数与 FAIL / BLOCKED 分布应当一致;任何差异都要给出成因。

    同样对照 item 8 的 INFO 原始读数:L-2 的 `scrollWidth` / `clientWidth` / `docPanelWidth`(@768 / @1024 / @1440)与 sticky 的 `scrollTop` / `scrollHeight` / `clientHeight` / `header` / `panel` —— 本阶段零布局改动,这些数字应逐值相同。**数字的对照结果(两边都贴出来)本身就是「方向安全」这条结论的实测证据**,不是推断。

    **第 4 步 —— 分诊(对每一条 FAIL / 新增 BLOCKED 逐条执行)。**

    按 `<objective>` 里的分诊流程走二元判定:**是 / 不是「本阶段刻意改变的事实」**。

    - **是** ⇒ 重新登记(换期望侧,形式与强度一字不变),重跑该门证明回到绿,改动逐条写进 SUMMARY。**但 `check-05` 在禁止改动清单里** —— 若它红,处置是停下报回并给出原始输出。
    - **否** ⇒ 产品缺陷:停下,把失败原文、涉及的 CSS 声明、为什么不是「事实被刻意改变」写进 SUMMARY 作为未关闭项报回。**不要**就地改 `frontend/style.css`(本计划对产品代码零改动),也**不要**放宽判据。

    三类**绝不允许**的处置,无论失败看起来多小:改阈值 / 把等值降为弱判据 / 跳过或删除断言。

    **第 5 步 —— 特别核对四组「预期存活」的断言。它们红了一定有具体成因。**

    (a) `check-05` 的 `[p1] .markdown-body td font-size == var(--text-base)`:`td` 的 `font-size` 本阶段一字未动。若红 ⇒ 计划 01 顺手改了它,属产品缺陷。
    (b) `check-05` item 8 的 L-2 三宽度溢出与 `#doc-panel` 实测宽上界:去掉表格竖线**只会让表更窄**。若红 ⇒ 说明表格宽度**增大**了(方向反了),属产品缺陷。
    (c) `check-05` item 4 的四条几何断言:本阶段零 `padding` 改动。若红 ⇒ 改动溢出到了内边距,属产品缺陷。
    (d) `check-06` g6 的两条 `box-shadow 恒 none` 对照组 + `#doc-panel.collapsed` 折叠往返:本阶段零 `box-shadow` / 零 `#doc-panel` 改动。若红 ⇒ 改动溢出,属产品缺陷。

    **第 6 步 —— 把五条门的原始结论与分诊结论写进 SUMMARY。** SUMMARY 必须能让读者独立复核:每条的**退出码**、`FAIL` / `BLOCKED` 计数、`check-05` 的 item 5 两条 BLOCKED 腿的按设计说明、与 phase 9 基线的逐项对照、以及任何门改动的逐条登记。若本步骤零改动,明确写「预期零处门改动,实测零处」。

    **第 7 步 —— 不触碰任何代码。** 本计划只跑命令、写日志与 SUMMARY。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --browser bundled > .planning/phases/idi-10-tables-and-radius-scale/gate-logs/check-05-full.log 2>&1; echo "exit=$?"</automated>
    <fails_when>the printed code is not "exit=2" (item 5 的两条 --ai-smoke 腿在无 --ai-smoke 时按设计 BLOCKED), or the log file is empty, or the log contains no "=== 逐项结论 ===" block</fails_when>
    <automated>grep -n 'FAIL' .planning/phases/idi-10-tables-and-radius-scale/gate-logs/check-05-full.log | grep -v '0 FAIL'</automated>
    <fails_when>output is non-empty (a line naming FAIL other than the summary's "0 FAIL" means a verdict failed)</fails_when>
    <automated>.venv/bin/python scripts/check-06-idi05-validation.py > .planning/phases/idi-10-tables-and-radius-scale/gate-logs/check-06-idi05-validation.log 2>&1; echo "exit=$?"</automated>
    <fails_when>the printed code is not "exit=0", or the log is empty</fails_when>
    <automated>.venv/bin/python scripts/check-07-idi08-validation.py > .planning/phases/idi-10-tables-and-radius-scale/gate-logs/check-07-idi08-validation.log 2>&1; echo "exit=$?"</automated>
    <fails_when>the printed code is not "exit=0", or the log is empty</fails_when>
    <automated>.venv/bin/python scripts/probe-05-resolve-color.py > .planning/phases/idi-10-tables-and-radius-scale/gate-logs/probe-05-resolve-color.log 2>&1; echo "exit=$?"</automated>
    <fails_when>the printed code is not "exit=0", or the log is empty</fails_when>
    <automated>.venv/bin/python scripts/probe-07-focus-composite.py > .planning/phases/idi-10-tables-and-radius-scale/gate-logs/probe-07-focus-composite.log 2>&1; echo "exit=$?"</automated>
    <fails_when>the printed code is not "exit=0", or the log is empty</fails_when>
    <automated>ls .planning/phases/idi-10-tables-and-radius-scale/gate-logs/</automated>
    <fails_when>output does not contain all of "check-05-full.log", "check-06-idi05-validation.log", "check-07-idi08-validation.log", "probe-05-resolve-color.log", "probe-07-focus-composite.log"</fails_when>
    <automated>git diff -- scripts/check-05-ui-uat.py</automated>
    <fails_when>output is not empty (any diff to check-05-ui-uat.py would pull idi-08 into the re-verification set)</fails_when>
  </verify>
  <acceptance_criteria>
    - `gate-logs/` 下存在五个日志文件(`check-05-full.log` / `check-06-idi05-validation.log` / `check-07-idi08-validation.log` / `probe-05-resolve-color.log` / `probe-07-focus-composite.log`),内容为该门**完整未截断**的 stdout。
    - `check-05 --browser bundled` 的退出码为 `2`;`grep -n 'FAIL' check-05-full.log | grep -v '0 FAIL'` 输出为空;非汇总行的 `BLOCKED` 只出现在 item 5。
    - `check-06` / `check-07` / `probe-05` / `probe-07` 的退出码均为 `0`,其日志里 `grep -n 'FAIL' <log> | grep -v '0 FAIL'` 输出为空。
    - SUMMARY 里逐项列出与 phase 9 基线 `check-05-full.log` 的 `=== 逐项结论 ===` 对照(两边的 10 行都贴出来),差异项给出成因;预期逐项一致。
    - SUMMARY 里贴出 item 8 的 L-2 三宽度读数(`scrollWidth` / `clientWidth` / `docPanelWidth` @768 / @1024 / @1440)与 sticky 坐标,并与 phase 9 的同名读数逐值对照。
    - `check-05` 的 `[p1] .markdown-body td font-size == var(--text-base)` 为 PASS(不是 BLOCKED);item 4 的四条几何断言、item 8 的 L-2 与 `badge × banner`、item 9 的滚动者普查、item 2 的 `#round-doc` 对比度均 PASS。
    - `check-06` g3 / g5 / g6 全 pass;`check-07` 四条行为断言全 pass。
    - `git diff -- scripts/check-05-ui-uat.py` 为空(**零处门改动**,预期与实测一致);SUMMARY 明确写出「预期零处门改动,实测零处」。
    - 本任务没有编辑任何产品代码或门代码(除日志与 SUMMARY)。
  </acceptance_criteria>
  <done>五条浏览器门复跑完毕,零 FAIL;`check-05` 全量退出码 2 且唯一的 BLOCKED 是 item 5 的两条 `--ai-smoke` 腿;与 phase 9 基线逐项同形、关键几何读数逐值相同;分诊结论与原始输出逐条记入 SUMMARY(实测零处门改动)。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 2: 四个静态门 + pytest 基线 + `node --check` + 仓库卫生复核</name>
  <files>.planning/phases/idi-10-tables-and-radius-scale/gate-logs/</files>
  <reversibility rating="reversible">本任务不产生任何代码改动;它是对已落地状态的复核,失败只暴露问题、不引入问题。</reversibility>
  <read_first>
    - `scripts/check-01-token-conformance.sh` 全文 —— 围栏 START / END 配对断言、围栏外裸 `#hex` 与 tier-1 原语引用的计数逻辑
    - `scripts/check-02-contrast.py` 的阈值常量、覆盖地板、`raw_pairs == len(pairs)` 计数一致性、输出格式
    - `scripts/check-03-hidden-uniqueness.sh` / `scripts/check-04-important-count.sh` 全文 —— `^[[:space:]]*\.hidden[[:space:]]*\{` 计数 == 1、`!important;` **声明**计数 == 1
    - `.planning/ROADMAP.md` §`### Phase 10:` 的 `**Gates**:` 行 —— 本任务逐条覆盖它列出的每一条
    - `.planning/phases/idi-10-tables-and-radius-scale/10-CONTEXT.md` §「门禁环境事实(省得重踩)」 —— pytest 必须用项目 `.venv`,基线 `219 passed / 6 skipped`
    - `.planning/config.json` —— `workflow.test_command` 为 `.venv/bin/python -m pytest backend/tests -q --tb=short`
  </read_first>
  <action>
    **第 1 步 —— 逐条跑四个静态门,把原始输出落到 `gate-logs/` 并记录退出码。**

    - `check-01-token-conformance.log` ← `bash scripts/check-01-token-conformance.sh`
    - `check-02-contrast.log` ← `.venv/bin/python scripts/check-02-contrast.py`
    - `check-03-hidden-uniqueness.log` ← `bash scripts/check-03-hidden-uniqueness.sh`
    - `check-04-important-count.log` ← `bash scripts/check-04-important-count.sh`

    每条的标准输出**原文**与**退出码**都写进日志与 SUMMARY。

    **第 2 步 —— 复核 `check-02` 的输出结构(零清单增删)。**

    从 `check-02-contrast.log` 里记录:清单规模(PAIR 对数的 TEXT / NON-TEXT 分解)、ORDER 行、以及表头新绘制面那条 `PASS  <比值>  --color-text on --color-surface` 的**原文行**。这些数字必须与 `frontend/style.css` 清单历史段的既有登记一致 —— **不一致就是登记错了**,按产品缺陷报回,**不得**改清单去迁就实跑(那是把结论改成想要的样子)。

    另记录 `grep -o '/\* PAIR' frontend/style.css | wc -l`(应 == 53)与 `grep -o '/\* ORDER' frontend/style.css | wc -l`(应 == 1)—— 本阶段零清单增删。

    **第 3 步 —— pytest 基线。**

    用项目 `.venv` 跑 `.venv/bin/python -m pytest backend/tests -q --tb=short`,输出落到 `pytest.log`,记录摘要行。期望 `219 passed, 6 skipped`。**不得**用环境的 `python3`(它是 miniconda,会让 4 个 `ai_caller` 测试假失败,把基线误判成回归)。若数字与基线不同,逐条查明差异来源再下结论。

    **第 4 步 —— `node --check frontend/app.js`。**

    输出落到 `node-check-app.log`,记录退出码(期望 0)。`app.js` 本阶段零字节改动,这条是形式化复核,证明本阶段确实没碰它。

    **第 5 步 —— 仓库卫生。**

    记录 `git status --porcelain frontend/`(期望仅 `M frontend/style.css`)、`ls frontend/vendor/`(期望仅 `marked.min.js`)、`grep -c '@media' frontend/style.css`(期望 1 —— Phase 7 的 prefers-reduced-motion 块)与 `grep -c '^\.hidden {' frontend/style.css`(期望 1)。

    **第 6 步 —— 不触碰任何代码。** 本任务只跑命令与记录;不编辑任何文件(SUMMARY 与日志除外)。任何一条不达标都按产品缺陷报回,不就地修。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh | tee .planning/phases/idi-10-tables-and-radius-scale/gate-logs/check-01-token-conformance.log</automated>
    <fails_when>the piped stdout is not exactly "PASS" (the tee'd log is the artifact; a non-"PASS" line means the fence or the out-of-fence scan broke)</fails_when>
    <automated>.venv/bin/python scripts/check-02-contrast.py | tee .planning/phases/idi-10-tables-and-radius-scale/gate-logs/check-02-contrast.log</automated>
    <fails_when>any line begins with "FAIL", or the final line is not "PASS: 0 failures", or no line matches "^PASS .*  --color-text on --color-surface$"</fails_when>
    <automated>bash scripts/check-03-hidden-uniqueness.sh | tee .planning/phases/idi-10-tables-and-radius-scale/gate-logs/check-03-hidden-uniqueness.log</automated>
    <fails_when>the piped stdout is not exactly "PASS"</fails_when>
    <automated>bash scripts/check-04-important-count.sh | tee .planning/phases/idi-10-tables-and-radius-scale/gate-logs/check-04-important-count.log</automated>
    <fails_when>the piped stdout is not exactly "PASS"</fails_when>
    <automated>.venv/bin/python -m pytest backend/tests -q --tb=short | tee .planning/phases/idi-10-tables-and-radius-scale/gate-logs/pytest.log</automated>
    <fails_when>the summary line does not contain both "219 passed" and "6 skipped"</fails_when>
    <automated>node --check frontend/app.js | tee .planning/phases/idi-10-tables-and-radius-scale/gate-logs/node-check-app.log</automated>
    <fails_when>non-zero exit, or any output written to stderr</fails_when>
    <automated>git status --porcelain frontend/</automated>
    <fails_when>output contains any path other than "frontend/style.css", or output is empty</fails_when>
    <automated>ls frontend/vendor/</automated>
    <fails_when>output contains any name other than "marked.min.js"</fails_when>
    <automated>grep -o '/\* PAIR' frontend/style.css | wc -l; grep -o '/\* ORDER' frontend/style.css | wc -l; grep -c '@media' frontend/style.css</automated>
    <fails_when>the three counts are not exactly "53", "1" and "1" respectively</fails_when>
  </verify>
  <acceptance_criteria>
    - `gate-logs/` 下新增四个静态门日志 + `pytest.log` + `node-check-app.log`,内容为该命令**完整未截断**的标准输出。
    - 四个静态门全部打印 `PASS`(`check-02` 为 `PASS: 0 failures`);`check-02` 输出含表头绘制面那条 `PASS  <比值>  --color-text on --color-surface` 的原文行,该行原文抄进 SUMMARY。
    - `grep -o '/\* PAIR' frontend/style.css | wc -l` == 53;`grep -o '/\* ORDER' frontend/style.css | wc -l` == 1(零清单增删)。
    - `.venv/bin/python -m pytest backend/tests -q --tb=short` 的摘要行为 `219 passed, 6 skipped` 且退出码 0;SUMMARY 记明用的是项目 `.venv`。
    - `node --check frontend/app.js` 退出码 0 且无输出。
    - `git status --porcelain frontend/` 仅含 `frontend/style.css`;`ls frontend/vendor/` 仅含 `marked.min.js`;`grep -c '@media' frontend/style.css` == 1;`grep -c '^\.hidden {' frontend/style.css` == 1。
    - 本任务没有编辑任何文件(除日志与 SUMMARY)。
  </acceptance_criteria>
  <done>四个静态门全绿且原文入册;`check-02` 的表头绘制面配对行原文入册;pytest 基线 `219 passed, 6 skipped`;`node --check frontend/app.js` 通过;仓库卫生与 PAIR / ORDER / `@media` / `.hidden` 四个计数逐项复核通过。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 3: 产出供用户评审的截图 + 开放项与移交说明</name>
  <files>.planning/phases/idi-10-tables-and-radius-scale/screenshots/, .planning/phases/idi-10-tables-and-radius-scale/gate-logs/</files>
  <precondition>.venv/bin/python 可导入 playwright,且 Playwright 自带 chromium 已缓存</precondition>
  <reversibility rating="reversible">只新增 PNG 与文档段落,不触碰任何代码;回退是删除该目录。</reversibility>
  <read_first>
    - `scripts/check-10-idi10-validation.py` 的 `run_screenshots()` 与 `--screenshot DIR`(计划 01 产出)—— 它遍历的样本清单与逐张宽高断言
    - `scripts/check-05-ui-uat.py` 的 `STATES = ["p1", "p12", "p3", "checking", "archive"]` 与 `HIDDEN_MATRIX` / `MARKDOWN_HOSTS` —— 5 个样本各自哪个面板可见、哪个宿主承载文档(这决定每张图能看到哪张表、哪个容器)
    - `scripts/ui-states/` 的样本内容(规划期实测,执行器须当场复核)—— 含表行的只有 `p3/docs/discuss-round-{1,2}.md`(17 / 15 行以 `|` 开头)与 `archive/docs/discuss-round-{1,2}.md`(17 / 15 行);`p1` 目录**只有 `.gitkeep`**;`p12/docs/draft.md`、`checking/DESIGN.md`、`checking/docs/DESIGN-check-2.md`、`archive/DESIGN.md`、`archive/docs/DESIGN-check-1.md` 的表格行数**均为 0**。⚠ `archive` 的轮次文档虽含表,但 `loadArchiveView()` 首屏只把 `DESIGN.md`(0 行表格)渲染进 `#round-doc`,轮次文档只在用户切轮次选择器时才加载 ⇒ **自然首屏只有 `p3` 一个样本渲染表格**。这是「SC1 的『至少两张』指表不指样本」这条读法的实测依据
    - `frontend/app.js` 的 `loadRoundsView()` / `loadRoundView()` —— 默认目标轮是 `current_round`(p3 即第 2 轮),故 `#round-doc` 首屏渲染 `docs/discuss-round-2.md`;该文件 §1「批注回应」/ §2「覆盖维度表」/ §3「未决问题清单」正是 DESIGN.md §6.4 点名的三张机器可解析表
    - `.planning/phases/idi-09-card-containers/idi-09-03-PLAN.md` Task 3 —— **同规格的出图与自检流程**(每张图至少能看到哪几件事、不要把「图出了」当「图对了」)
    - `frontend/style.css` 的 `.markdown-body table` / `th, td` 与 `.markdown-body th`(计划 01 的最终形态)、`.chat-user` 与 `#chat-input-row input`(计划 02 的最终形态)—— 截图要能看出这四处的机械后果
    - `.planning/ROADMAP.md` §`### Phase 10:` 的 Deliverables 最后一条与 Success Criteria 1、4
    - `.planning/REQUIREMENTS.md` §`Out of Scope` —— 明确「本阶段不得预先构建」的四项
  </read_first>
  <action>
    **第 1 步 —— 出图。**

    跑 `.venv/bin/python scripts/check-10-idi10-validation.py --screenshot .planning/phases/idi-10-tables-and-radius-scale/screenshots`,覆盖 5 个状态样本(p1 / p12 / p3 / checking / archive),每张为 1440×900 的整窗截图。同时把它 stdout 原文落到 `gate-logs/check-10-idi10-validation.log`。

    文件名由 `run_screenshots()` 决定(`<样本名>.png`),使读者不看 SUMMARY 也能对上号。

    **第 2 步 —— 逐张自检至少能看到三件事(看不到就重出,不要把「图出了」当「图对了」)。**

    (a) **表格没有竖线与外框**:文档区里的表格只有横向的浅色分隔线,表头有一条浅灰底,旁边没有竖线、没有外框。**`p3` 的截图里要同时可见三个机器可解析表**(批注回应表 / 覆盖维度表 / 未决问题清单 —— 它们同在 `p3` 当前轮的 `docs/discuss-round-2.md` 的 §1 / §2 / §3),这满足 ROADMAP SC1 的「至少两张作为证据」(三 ≥ 二)。⚠ SC1 的「至少两张」指的是**表**、不是**样本**:自然首屏只有 `p3` 一个样本渲染表格(`p1` 目录只有 `.gitkeep`;`p12` / `checking` / `archive` 的文档零表格行,`archive` 首屏渲染的是零表格行的 `DESIGN.md`),**不得**把它读成「两张不同样本的截图各自有表」。
    (b) **圆角收敛可见**:样本里出现 `.chat-user` 气泡时,它是 10px 卡片圆角(不再是 28px 的大圆角),其右下角仍是 8px 尖角;`#chat-input-row` 的输入框外观与收敛前一致(它就是胶囊)。
    (c) **前序构图未被打破**:页面仍是灰的、容器仍是白卡片、卡片之间有灰色间隙(Phase 9 的成果在本阶段后仍成立)。

    若某张图看不到上述任一项,说明出图时机(样本切换 / 等待渲染)不对 —— 重出。

    **第 3 步 —— 在 SUMMARY 里写明截图路径、逐张说明与开放项。**

    逐张写明该样本下可见的是哪个面板 / 哪个文档宿主(依 `HIDDEN_MATRIX` 与 `MARKDOWN_HOSTS`),以及该张图上能看到哪些表格与哪一处圆角。

    开放项逐条写明「本阶段未构建」及其依据 —— **本阶段的四项沿用上阶段的口径,用户本次仍未点名**:
    - `.overlay-card` 的底色(当前是 gray-2 + `--shadow-overlay`;页面已下沉,它显得比主界面卡片内陷一档。是否改白 = 设计决策,本阶段不动);
    - 页面级留白(本阶段没给 `#main-pane` 加 `padding`、也没给卡片加 `margin`;是否留白 = 未裁定项);
    - 输入框在白卡片上的填充(应用的文本 input 一律不声明 `background`,故画的是 UA 字段白填充,不构成 gray-2 内陷面;是否该带一层内陷底 = 设计决策);
    - 图标与空状态(用户本次未点名的第三项候选)。
    并明确重申 **Out of Scope 四项不得预先构建**(表格重做与圆角刻度收敛已在本阶段**完成**;图标与空状态、暗色模式仍未点名)。

    另登记一条**本阶段的实现观察**(不构建,只记录):`--radius-lg` 的删除让圆角刻度与 `04-UI-SPEC.md` 的圆角账本(`4px / 8px / 999px`)的对齐问题浮出水面 —— 账本里既没有 `8px / 10px` 这组值,也没有本阶段的三档语义描述。是否回填账本是**文档层的独立事项**,不在本阶段边界内。

    **第 4 步 —— 不构建任何后续候选。** 本任务只出图与写说明。发现的问题一律登记进 SUMMARY 的开放项,不就地实现。

    **第 5 步 —— 截图不得落在 `frontend/`。** ROADMAP 的 Gate 要求 `git status --porcelain frontend/` 仅含预期文件;截图的落点是 `.planning/phases/idi-10-tables-and-radius-scale/screenshots/`。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-10-idi10-validation.py --screenshot .planning/phases/idi-10-tables-and-radius-scale/screenshots | tee .planning/phases/idi-10-tables-and-radius-scale/gate-logs/check-10-idi10-validation.log</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or a non-zero BLOCKED count in the "=== 逐项结论 ===" block, or the trailing "exit=" line not "exit=0"</fails_when>
    <automated>ls .planning/phases/idi-10-tables-and-radius-scale/screenshots/</automated>
    <fails_when>output does not contain one PNG per state sample (p1, p12, p3, checking, archive), i.e. fewer than 5 .png entries; or any listed name is not one of those five</fails_when>
    <automated>python3 -c "import struct,glob;bad=[p for p in sorted(glob.glob('.planning/phases/idi-10-tables-and-radius-scale/screenshots/*.png')) if struct.unpack('>II', open(p,'rb').read(24)[16:24])!=(1440,900)];print(bad)"</automated>
    <fails_when>the printed list is non-empty (any PNG not being exactly 1440x900), or the glob matched zero files</fails_when>
    <automated>git status --porcelain frontend/</automated>
    <fails_when>output contains any path other than "frontend/style.css" (a screenshot or log landing in frontend/ would show up here), or output is empty</fails_when>
  </verify>
  <acceptance_criteria>
    - `.planning/phases/idi-10-tables-and-radius-scale/screenshots/` 下存在恰好 5 个 PNG,文件名逐一对上 `p1` / `p12` / `p3` / `checking` / `archive`。
    - 每张 PNG 的 IHDR 宽高都恰为 **1440×900**(逐张实测,不是「有文件就算」)。
    - `--screenshot` 命令 `exit=0`、0 FAIL / 0 BLOCKED,其 stdout 原文落在 `gate-logs/check-10-idi10-validation.log`。
    - SUMMARY 里列出全部截图路径,并逐张写明该样本下可见的面板与文档宿主(依 `HIDDEN_MATRIX` 与 `MARKDOWN_HOSTS`)。
    - SUMMARY 里明确记录:**`p3` 的截图里同时可见三个机器可解析表**(批注回应表 / 覆盖维度表 / 未决问题清单,来自 `p3` 当前轮的 `docs/discuss-round-2.md` 的 §1 / §2 / §3),且表格里没有竖线与外框、表头有浅灰底、行间有极浅横向分隔线。ROADMAP SC1 的「至少两张」指**表**不指**样本**;SUMMARY 里要写明这条读法,并记下 `p3` 是唯一自然渲染表格的样本(其余四个样本的文档零表格行)。
    - SUMMARY 里记录截图里可见的圆角收敛机械后果(10px 气泡圆角 + 8px 尖角 / 输入框外观不变),以及 Phase 9 的构图(灰页面 / 白卡片 / 卡片间间隙)仍成立。
    - SUMMARY 里列出至少 4 条开放项(`.overlay-card` 底色 / 页面级留白 / 输入框 UA 白填充 / 图标与空状态),每条写明「本阶段未构建」及其依据;并重申 Out of Scope 中仍未点名的项不得预先构建。
    - `git status --porcelain frontend/` 仍仅列出 `frontend/style.css`(截图与日志未落进 `frontend/`)。
  </acceptance_criteria>
  <done>5 个状态样本的 1440×900 截图落在 `.planning/phases/idi-10-tables-and-radius-scale/screenshots/`,其中 `p3` 的截图同时可见三个机器可解析表(满足 SC1 的「至少两张」,该判据指表不指样本),表格呈「无竖线、无外框、表头浅灰底」,且圆角收敛的机械后果可见;SUMMARY 列出截图路径、逐张说明、至少 4 条开放项与 Out of Scope 的重申。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 无外部输入边界 | 本计划只跑既有验证脚本与出图:零用户输入处理、零鉴权、零数据访问、零新增网络调用(Playwright 用已缓存的 chromium,零下载)、零产品代码改动。攻击面限于本地起服务跑 Playwright 与写本地产物 |
| 本地文件系统边界 | 日志与截图分别写进 `.planning/phases/idi-10-tables-and-radius-scale/gate-logs/` 与 `screenshots/`。它们**不得**写进 `frontend/`(否则 `git status --porcelain frontend/` 会多出条目,且产物会进入发布路径) |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-10-01 | Information Disclosure | 截图产物与门日志 | low | accept | 截图只含本工具的本地界面(样本状态目录在临时目录内,截图不含真实项目内容);日志含令牌值与几何读数,均来自公开的样式表与本地 fixture。落点都在 `.planning/` 下,不进 `frontend/`、不进发布路径。验收:`git status --porcelain frontend/` 仅含 `frontend/style.css` |
| T-idi-10-02 | Tampering | 分诊流程中改动回归门 | **high** | mitigate | 「把门跑绿」的诱惑是本计划唯一的真实风险:放宽阈值或弱化判据会让门绿而没在看。缓解:(a) 本计划只允许**一种**门改动(期望侧换指到被本阶段刻意改变的事实),形式与强度一字不变;(b) **`check-05` 被显式列入禁止改动清单** —— 它若红,处置是停下报回而非就地改(改它会把 `idi-08` 拖进重验名单);(c) 每条改动必须逐条写进 SUMMARY(改哪一行 / 旧期望 / 新期望 / 依据哪条裁定);(d) `<prohibitions>` 逐条列出禁止的处置方式;(e) 复核 `check-02` 的 `TEXT_MIN` / `NON_TEXT_MIN` 与 HEAD 逐字节相同;(f) 验收:`git diff -- scripts/check-05-ui-uat.py` 为空 |
| T-idi-10-03 | Repudiation | 「门绿了」这一结论无原始证据;**且计数门是 scope-blind 的** | medium | mitigate | SUMMARY 必须抄录每条门的**退出码 + 汇总块原文 + 任何 FAIL / BLOCKED 行的完整原文**,并把逐门 stdout **原文未截断**落进 `gate-logs/`。判据一律用 `grep -n 'FAIL' <log> \| grep -v '0 FAIL'` 的行为空,**禁止**用 `grep -c 'FAIL'` 的裸计数(它会把汇总行里的 `0 FAIL` 数进去 —— 本项目已为此红过一次)。`check-05` 的 item 5 两条 BLOCKED 腿要按设计说明写清,防止读者把「设计如此」与「新回归」混为一谈 |
| T-idi-10-04 | Denial of Service | `check-05` 的浏览器路线选择 | low | mitigate | 本机 `.venv` 是 x86_64(Rosetta),`channel="chrome"` + `headless=True` 会 CDP 永不连上、超时挂死。缓解:`<prohibitions>` 明令必须走 `--browser bundled`(自带 chromium 已缓存,零下载) |
| T-idi-10-05 | Tampering | 截图 / 日志落点 | medium | mitigate | 产物若落进 `frontend/`,会污染交付面并把非产品文件带进发布路径。缓解:截图的输出目录由 `--screenshot DIR` 显式给定为 `.planning/phases/idi-10-tables-and-radius-scale/screenshots/`;日志同阶段 `gate-logs/`;<prohibitions> 明令禁止写进 `frontend/`;验收 `git status --porcelain frontend/` 仅含 `frontend/style.css` |
| T-idi-10-06 | Elevation of Privilege | 无 | low | accept | 本计划不触碰鉴权、权限门、服务端路径或任何 API |
| T-idi-10-SC | Tampering | npm / pip / cargo 安装 | low | accept | 本阶段**零安装**:零新增依赖、零构建步骤(DESIGN.md D-06);Playwright 与 chromium 均已在项目 `.venv` 中就绪,不触发下载。`frontend/vendor/` 仍只有 `marked.min.js`。验收:`ls frontend/vendor/` 输出仅 `marked.min.js` |
</threat_model>

<verification>
**五条浏览器门:**

- `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` → `=== 逐项结论 ===` 零 FAIL,`exit=2`,BLOCKED 仅 item 5 的两条 `--ai-smoke` 腿
- `.venv/bin/python scripts/check-06-idi05-validation.py` → `exit=0`
- `.venv/bin/python scripts/check-07-idi08-validation.py` → `exit=0`
- `.venv/bin/python scripts/probe-05-resolve-color.py` → `exit=0`
- `.venv/bin/python scripts/probe-07-focus-composite.py` → `exit=0`

**四个静态门 + 基线:**

- `bash scripts/check-01-token-conformance.sh` / `check-03` / `check-04` → `PASS`
- `.venv/bin/python scripts/check-02-contrast.py` → `PASS: 0 failures`(含表头绘制面那条 `PASS  <比值>  --color-text on --color-surface`)
- `.venv/bin/python -m pytest backend/tests -q --tb=short` → `219 passed, 6 skipped`
- `node --check frontend/app.js` → exit 0

**本阶段自建运行时门(阶段末尾仍须全绿):**

- `.venv/bin/python scripts/check-10-idi10-validation.py --item t1 --item t2 --item r1 --item r2` → `exit=0`,0 FAIL / 0 BLOCKED

**仓库卫生:**

- `git status --porcelain frontend/` 仅 `frontend/style.css`;`ls frontend/vendor/` 仅 `marked.min.js`
- `git diff -- scripts/check-05-ui-uat.py` 为空
- `grep -o '/\* PAIR' frontend/style.css | wc -l` == 53;`grep -o '/\* ORDER' frontend/style.css | wc -l` == 1;`grep -c '@media' frontend/style.css` == 1;`grep -c '^\.hidden {' frontend/style.css` == 1

**交付物:**

- `.planning/phases/idi-10-tables-and-radius-scale/screenshots/` 下 5 个状态样本的 1440×900 PNG
- `.planning/phases/idi-10-tables-and-radius-scale/gate-logs/` 下逐门原始 stdout
</verification>

<success_criteria>
- 五条浏览器门复跑**无新增失败**:`check-05` 零 FAIL(退出码 2 系 item 5 两条 `--ai-smoke` 腿按设计 BLOCKED),`check-06` / `check-07` / `probe-05` / `probe-07` 均 `exit=0`;`=== 逐项结论 ===` 块与 phase 9 基线逐项同形。
- 任何门改动都是「期望侧换指到被本阶段刻意改变的事实」,断言形式与强度一字不变,并在 SUMMARY 里逐条登记;零阈值放宽、零判据弱化、零断言删除。**实测零处门改动**;`check-05` 未被改动一行。
- 四个静态门全绿;pytest 基线 `219 passed, 6 skipped`;`node --check frontend/app.js` 通过。
- 5 个状态样本的 1440×900 截图已产出,其中 `p3` 的截图同时可见三个机器可解析表(「至少两张」指表不指样本),表格呈「无竖线、无外框、表头浅灰底」;SUMMARY 列出截图路径、逐张说明、至少 4 条开放项与 Out of Scope 的重申。
- `frontend/style.css` 与 `scripts/` 下全部文件在本计划内零改动;`frontend/app.js` / `index.html` / `vendor/` 零字节改动。
- 逐门 stdout 原文落在 `gate-logs/`,使「门绿了」这一结论可被独立复核。
</success_criteria>

<output>
Create `.planning/phases/idi-10-tables-and-radius-scale/idi-10-03-SUMMARY.md` when done
</output>

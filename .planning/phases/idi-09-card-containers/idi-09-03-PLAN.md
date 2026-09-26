---
phase: idi-09-card-containers
plan: 03
type: execute
wave: 3
depends_on:
  - idi-09-02
files_modified:
  - scripts/check-05-ui-uat.py
  - .planning/phases/idi-09-card-containers/screenshots/
autonomous: true
requirements:
  - REG-02
  - CARD-01
  - CARD-02
  - CARD-03

estimate:
  tokens: 30000
  raw_tokens: 30000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- REG-02 — the five browser gates are the real regression surface ----
    - "`.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` 的 `=== 逐项结论 ===` 块里**没有任何** `FAIL`;退出码为 `2`;BLOCKED 只出现在 item 5 的两条 `--ai-smoke` 腿(设计如此,不是回归)"
    - "`.venv/bin/python scripts/check-06-idi05-validation.py` 退出码为 `0`(g1…g6 全 pass)"
    - "`.venv/bin/python scripts/check-07-idi08-validation.py` 退出码为 `0`(g1…g4 全 pass)"
    - "`.venv/bin/python scripts/probe-05-resolve-color.py` 退出码为 `0`(令牌解析的变异证明仍成立)"
    - "`.venv/bin/python scripts/probe-07-focus-composite.py` 退出码为 `0`(焦点环合成算术的反事实证明仍成立)"
    - "每一条被判定为「门断言的事实被本阶段刻意改变」的失败,其期望侧都以**重新登记**处置 —— 断言形式(等值 / 阈值 / 几何判据)一字不变,只换指到新事实;没有任何一条被改成弱判据、被跳过、被删除。每一处门改动都在 SUMMARY 里逐条列出并给出理由"
    - "断言强度未被降低:`scripts/check-02-contrast.py` 的 `TEXT_MIN` / `NON_TEXT_MIN` 未动;`check-05` 的 24×24 命中区、sticky 表头、badge 流内机制、窄窗口不破版四条判据的阈值未动"
    # ---- 静态门与基线 ----
    - "四个静态门(check-01 / check-02 / check-03 / check-04)全部打印 `PASS`(check-02 为 `PASS: 0 failures`)"
    - "`.venv/bin/python -m pytest backend/tests -q --tb=short` 的输出为 `219 passed, 6 skipped`,与 v1.14 收口基线逐字一致(必须用项目 `.venv` —— 环境 `python3` 是 miniconda,会让 4 个 `ai_caller` 测试假失败)"
    - "`node --check frontend/app.js` 退出码 0(app.js 零字节改动,这条是形式化复核)"
    - "`git status --porcelain frontend/` 只列出 `frontend/style.css`;`ls frontend/vendor/` 只有 `marked.min.js`"
    # ---- 截图(ROADMAP Deliverables 的最后一项)----
    - "`.planning/phases/idi-09-card-containers/screenshots/` 下存在覆盖 5 个状态样本(p1 / p12 / p3 / checking / archive)的 PNG,每张都是 1440×900 的整窗截图"
    - "截图里可见卡片化的机械后果:页面是灰的、五个容器是白的、卡片之间有灰色间隙、`#doc-panel` 与左栏同族"
    - "SUMMARY 里列出供用户裁定的开放项(至少:`.overlay-card` 底色是否改白、卡片边界 / 阴影强度是否够、是否要加页面级留白),每项都写明「本阶段未构建」及其依据"
    - "被复核的三项用户裁定值(D-9-1 页面下沉 + 白卡片 / D-9-2 密度 16px 与 12px / D-9-3 阴影 `0 1px 2px rgba(0, 0, 0, 0.04)` 零位移)在浏览器里全部成立,且它们的落地未打破五条浏览器门中的任何一条"

  artifacts:
    - path: ".planning/phases/idi-09-card-containers/screenshots/"
      provides: "5 个状态样本的 1440×900 整窗截图,供用户据此裁定后续候选(表格重做 / 圆角刻度收敛 / 图标与空状态)"
    - path: "scripts/check-05-ui-uat.py"
      provides: "仅在分诊判定为「断言的事实被本阶段刻意改变」时改动的期望侧(预期为零处 —— 计划 01 已把唯一一条已知受影响的 `.hint` 断言重新登记)"
    - path: ".planning/phases/idi-09-card-containers/idi-09-03-SUMMARY.md"
      provides: "五条浏览器门的复跑记录(含 check-05 全量结果与 item 5 两条 BLOCKED 腿的按设计说明)、pytest 基线、门改动逐条登记、截图路径与开放项清单"

  key_links:
    - from: "`scripts/check-09-idi09-validation.py` 的 `--screenshot DIR`"
      to: "`.planning/phases/idi-09-card-containers/screenshots/*.png`"
      via: "Playwright 的 `page.screenshot()`,每进入一个状态样本出一张图"
      pattern: "screenshot"
    - from: "五条浏览器门"
      to: "本阶段改动后的渲染语义"
      via: "它们断言的是 computed style 与几何 —— 静态 grep 对渲染结果零证明力,只有它们能证明「卡片化 + 页面下沉」之后既有行为仍然成立"
      pattern: "exit="

  prohibitions:
    - statement: "不得为了把门跑绿而放宽任何判据。允许的门改动只有一种:门断言的事实被本阶段**刻意改变**了(例如某个元素的有效背景由 gray-2 变白),此时把期望侧重新登记到新事实,断言形式与强度一字不变。**禁止**改阈值、改 `TEXT_MIN` / `NON_TEXT_MIN`、把等值断言降为子串 / 「非空」/ 「非透明」判据、加 `or` 分支、把断言标成跳过、删除断言、给门加白名单"
      status: active
      verification: flagged
    - statement: "不得把 BLOCKED 当 PASS 解释。`check-05` 的 `ok()` 在元素读不到或令牌解析不出时记 BLOCKED,这是「探针没读到」而不是「行为正确」。本阶段允许的 BLOCKED 只有 item 5 的两条 `--ai-smoke` 腿(无 `--ai-smoke` 时按设计不跑);任何**新增** BLOCKED 都按失败处理,必须查明原因"
      status: active
      verification: flagged
    - statement: "不得在 harness 里手工拼 DOM 伪造被测状态。需要构造状态时走应用自身已导出的函数(与既有 item 的做法一致);`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` 零字节改动,截图与门复跑都不得改动它们"
      status: active
      verification: flagged
    - statement: "不得用 `channel=\"chrome\"` 跑 `check-05`。本机 `.venv` 的 Python 是 x86_64(Rosetta),`channel=\"chrome\"` + `headless=True` 会让 CDP 永不连上、180s 超时挂死。必须走 `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled`(Playwright 自带 chromium,revision 1243 已缓存,零下载)"
      status: active
      verification: flagged
    - statement: "pytest 必须用项目 `.venv`(`.venv/bin/python -m pytest`)。环境的 `python3` 是 miniconda,会让 4 个 `ai_caller` 测试假失败,把「基线 219 passed / 6 skipped」误判成回归"
      status: active
      verification: flagged
    - statement: "不得把截图写进 `frontend/`。ROADMAP 的 Gate 要求 `git status --porcelain frontend/` 仅含预期文件;截图落在 `.planning/phases/idi-09-card-containers/screenshots/`"
      status: active
      verification: flagged
    - statement: "不得在本计划里新增功能或「顺手」修视觉细节。本阶段的范围边界是卡片容器化 + 页面底色下沉 + 配对重算登记 + 门禁复跑 + 截图;表格重做 / 圆角刻度收敛 / 图标与空状态 / `.overlay-card` 底色 / 页面级留白全部**不在本阶段**(REQUIREMENTS.md Out of Scope,用户裁定「先看看效果」)。发现的问题只登记进 SUMMARY 的开放项,不就地构建"
      status: active
      verification: flagged
---

<objective>
用本仓库唯一能证明「渲染语义仍然成立」的机器 —— 五条真实浏览器门 —— 复核本阶段的改动,并产出供用户评审的截图。

Purpose: 本阶段是纯 CSS 的**构图**改动,它的成败判据不是「CSS 里写下了什么」而是「浏览器里画出来什么」。`grep -c 'var(--'` 对渲染结果零证明力 —— 本仓库的方法论教训逐字写着「文本级 gate 通过不等于运行时语义成立」。而卡片化 + 页面下沉恰好动的是**每一处表面的底色**:五条门断言的正是 computed style 与几何(折叠行为 / 滚动容器收敛 / sticky 表头 / badge 流内机制 / 焦点环 / 24×24 命中区 / 窄窗口不破版),任何表面改动都可能打破它们。计划 01 已在规划期逐条普查并识别出**唯一一条**会被打破的断言(`check-05` 的 `.hint` 实际背景,已重新登记),本计划的任务是把这件事在实跑中证成:全绿,或把新发现逐条分诊。

Output: 五条浏览器门的复跑记录、四个静态门 + pytest 基线的复核、5 个状态样本的截图、以及一份写明开放项的 SUMMARY。

**本计划复核的三项设计值全部是用户已裁定的,本计划不改动其中任何一项:** D-9-1(页面下沉到 gray-3 + 白卡片的三级刻度)/ D-9-2(密度:卡片内边距 16px、卡片间距 12px)/ D-9-3(卡片阴影 `0 1px 2px rgba(0, 0, 0, 0.04)`,零位移)。复核口径是「它们是否在浏览器里真的成立、是否打破了既有门」,不是「它们是否该取这些值」。

**前置(执行前须复核):** `idi-09-01` 与 `idi-09-02` 已落地 —— 五个容器是白卡片、`--color-surface-page` 是 gray-3、密度是 16px / 12px。复核方式:`.venv/bin/python scripts/check-09-idi09-validation.py`(c1…c5 全绿)与 `.venv/bin/python scripts/check-02-contrast.py`(`PASS: 0 failures`)。

**本计划关闭的需求:** REG-02(CARD-01 / CARD-02 / CARD-03 的复核半边)。**本计划不触碰:** `frontend/style.css`(零改动 —— 若门红且分诊结论是产品缺陷,则停下并把结论报回,不就地改);`scripts/check-01…04` / `check-06` / `check-07` / `probe-05` / `probe-07` 代码零改动;`frontend/app.js` / `index.html` / `vendor/` 零字节。
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
@.planning/phases/idi-09-card-containers/09-CONTEXT.md
@.planning/phases/idi-09-card-containers/idi-09-01-SUMMARY.md
@.planning/phases/idi-09-card-containers/idi-09-02-SUMMARY.md
@scripts/check-05-ui-uat.py
@scripts/check-09-idi09-validation.py
</context>

## Artifacts this phase produces

> 本节的用途:**plan-review-convergence 的 source-grounding pass 读它,把本阶段新建的符号从漂移校验里排除**。
> 本节列出**全阶段**(三个计划)的产出;本计划只登记自己那部分。

**新增 CSS 自定义属性(围栏 `:root` 内,由计划 01 创建):**

| # | 符号 | 值 | 计划 | 备注 |
|---|---|---|---|---|
| 1 | `--color-surface-card` | `var(--white)` | 01 | 本计划零改动 |
| 2 | `--shadow-card` | `0 1px 2px rgba(0, 0, 0, 0.04)` | 01 | 本计划零改动 |

**新增文件:**

| # | 路径 | 计划 | 备注 |
|---|---|---|---|
| 3 | `scripts/check-09-idi09-validation.py` | 01(骨架 + c1 / c2)/ 02(c3 / c4 / c5) | 本计划**复用**它的 `--screenshot` 出图,不改它的断言 |
| 4 | `.planning/phases/idi-09-card-containers/screenshots/*.png` | **03** | 供用户评审的截图(ROADMAP Deliverables 的最后一项) |

**就地改值的既有声明(规则块位置与源码顺序逐字不变):**

| # | 符号 | HEAD 位置 | 计划 | 动作 |
|---|---|---|---|---|
| 5 | `--color-surface-page` | `:122` | 02 | `var(--radix-gray-1)` → `var(--radix-gray-3)` |
| 6 | `#main-pane` 的 `gap` | `:594` | 02 | 6px → 12px |
| 7 | `.panel-body` 的 `padding` | `:688` | 02 | 10px → 16px |
| 8 | `#main-pane > section` / `#doc-panel` / `#doc-panel-header` | `:605-608` / `:611-624` / `:649-654` | 01 | 卡片语言就地扩写 |

**本计划明确不产生的新符号:** 零新增令牌、零新增 CSS 文件、零新依赖、零新构建步骤;`frontend/style.css` 零改动。

## 五条浏览器门的复跑口径(逐条,含已知的按设计结果)

| 门 | 命令 | 期望结果 | 已知的按设计非绿项 |
|---|---|---|---|
| `check-05` | `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` | `=== 逐项结论 ===` 块零 `FAIL`;`exit=2` | item 5 的两条 `--ai-smoke` 腿在无 `--ai-smoke` 时 BLOCKED ⇒ 退出码 2。**这是设计如此,不是回归** |
| `check-06` | `.venv/bin/python scripts/check-06-idi05-validation.py` | `exit=0` | 无 |
| `check-07` | `.venv/bin/python scripts/check-07-idi08-validation.py` | `exit=0` | 无 |
| `probe-05` | `.venv/bin/python scripts/probe-05-resolve-color.py` | `exit=0` | 无(它是变异证明,不是门) |
| `probe-07` | `.venv/bin/python scripts/probe-07-focus-composite.py` | `exit=0` | 无(同上) |

**规划期已识别、且已在计划 01 重新登记的受影响断言(恰好 1 条):** `check-05` 的 `[p1] .hint 实际背景 == var(--color-surface)`(`:1305`)。`.hint` 无自身背景,`effective_bg()` 沿祖先链取到的最近不透明祖先是 `#doc-panel`;卡片化后它是白 ⇒ 期望侧已换指到 `--color-surface-card`。因此**本计划预期零处门改动** —— 若实跑出现 FAIL,那是新发现,必须走下面的分诊流程。

<tasks>

<task type="auto">
  <name>Task 1: 五条浏览器门复跑 + 失败分诊</name>
  <precondition>.venv/bin/python 可导入 playwright(`.venv/bin/python -c "import playwright"` 退出码 0),且 Playwright 自带 chromium 已缓存(不需要联网下载)</precondition>
  <files>scripts/check-05-ui-uat.py</files>
  <reversibility rating="costly">门复跑本身可重跑;但若分诊判定需要改某条门的期望侧,那处改动必须与它所登记的产品事实成对回退 —— 只回退 CSS 不回退门会让门红,只回退门不回退 CSS 会让门断言一个不存在的状态。故评级 costly。</reversibility>
  <read_first>
    - `scripts/check-05-ui-uat.py` `:1-60` —— 运行方式块与「本机 `.venv` 是 x86_64(Rosetta),`channel=\"chrome\"` + `headless=True` 会挂死」的环境事实;**必须走 `--browser bundled`**
    - `scripts/check-05-ui-uat.py` `:185-300` —— `_emit` 的输出格式(`PASS|FAIL|BLOCKED <label>: expected=… actual=…`)与 `ok` / `ok_true` / `blocked` / `info` / `item_verdict` 的语义(两处 BLOCKED 分支)
    - `scripts/check-05-ui-uat.py` `:4020-4110` —— `main()` 的派发与汇总:`item N: VERDICT  (n 条断言,f FAIL,b BLOCKED)` 与 `exit={code}`(0=全 pass / 1=有 fail / 2=有 blocked)
    - `scripts/check-05-ui-uat.py` `:1295-1306` —— 计划 01 已重新登记的 `.hint` 断言(本计划**只读**,除非分诊判定还要动它)
    - `scripts/check-05-ui-uat.py` `:780-786` —— `check_marker_control()` 的两条 `box-shadow == none` 对照组(`#ai-panel .panel-header` / `#doc-panel-header`)。**这两条是本阶段最容易误伤的断言**:卡片阴影加在 `#doc-panel` 自身、不加在表头,故应存活 —— 若它们红了,说明阴影加错了元素
    - `scripts/check-05-ui-uat.py` `:1045-1062` —— `.panel-header padding-top` / `#doc-panel-body padding` / `button padding-top` / `.overlay-card padding-top` 四条几何断言;`#doc-panel-body` 与 `.panel-header` 的 padding 在本阶段逐字未动,故应存活
    - `scripts/check-05-ui-uat.py` `:2682-2760` —— item 9 的面板区滚动者普查,口径是「**恰好** `{#main-pane, #chat-messages, #latest-check}`」;本阶段零 `overflow` 改动,故应存活
    - `scripts/check-06-idi05-validation.py` `:233-275`(g3 竖条几何与 `h2Delta >= 3`)、`:365-410`(g5 340px 最窄面板单行 / 不裁切)、`:430-490`(g6 折叠往返 + 两条 `box-shadow 恒 none` 对照组)—— 本阶段最可能误伤的三组
    - `scripts/check-07-idi08-validation.py` `:1-60` —— 四条行为断言的映射(Escape / dialog 语义 / 菜单不复弹 / 焦点交还)
    - `scripts/probe-05-resolve-color.py` `:1-40` 与 `scripts/probe-07-focus-composite.py` `:1-45` —— 两者的「变异证明」性质与运行方式
    - `.planning/phases/idi-09-card-containers/09-CONTEXT.md` §`门禁环境事实(省得重踩)`
  </read_first>
  <action>
    **第 1 步 —— 逐条复跑五条门,记录原始输出。** 按上面的复跑口径表逐条执行,把每条的退出码、`逐项结论` 块(或等价汇总)、以及任何 `FAIL` / `BLOCKED` 行的**完整原文**抄进 SUMMARY。不要只记「绿 / 红」。

    **第 2 步 —— 分诊流程(对每一条 FAIL / 新增 BLOCKED 逐条执行)。**

    对每一条失败,回答一个问题:**这条门断言的事实,是不是本阶段刻意改变的?**

    - **是** ⇒ 处置 = **重新登记**:把期望侧换指到新事实(例如某个元素的有效背景由 `--color-surface` 变 `--color-surface-card`、某个地面由 gray-1 变 gray-3),断言形式与强度**一字不变**。改完必须**重跑该条门**证明它回到绿,并把改动逐条写进 SUMMARY(改哪一行、旧期望、新期望、依据哪条裁定)。
    - **否** ⇒ 处置 = **产品缺陷**:停下,把失败原文、涉及的 CSS 声明、以及为什么不是「事实被刻意改变」写进 SUMMARY,并把它作为未关闭项报回。**不要**就地改 `frontend/style.css`(本计划对产品代码零改动),也**不要**用放宽判据的方式绕过去。

    三类**绝不允许**的处置,无论失败看起来多小:改阈值 / 把等值降为弱判据 / 跳过或删除断言。放宽阈值是「把门改小以让结论成立」,本仓库明令禁止。

    **第 3 步 —— 特别核对三条「预期存活」的断言组,它们红了一定有具体成因。**
    - `check-05` 的两条 `#doc-panel-header box-shadow == none` / `#ai-panel .panel-header box-shadow == none` 对照组:本阶段的卡片阴影加在 `#doc-panel` 与 `#main-pane > section` 上,**不加在 `.panel-header` 上**。若红了 ⇒ 阴影加错了元素,属产品缺陷。
    - `check-05` item 3 的 `#doc-panel-body padding == "32px 40px"` 与 `.panel-header padding-top == "6px"`:本阶段的密度改动只落在 `.panel-body`(`:688`)。若红了 ⇒ 改错了选择器(例如把 `.panel-body` 的规则扩成也命中 `#doc-panel-body`),属产品缺陷。
    - `check-05` item 9 的滚动者普查(口径「恰好」):本阶段零 `overflow` 改动。若红了 ⇒ 卡片规则里混进了 `overflow`,属产品缺陷。

    **第 4 步 —— 把五条门的原始结论与分诊结论写进 SUMMARY。** SUMMARY 必须能让读者独立复核:每条的退出码、FAIL / BLOCKED 计数、`check-05` 的 item 5 两条 BLOCKED 腿的按设计说明、以及任何门改动的逐条登记。若本步骤零改动,明确写「预期零处门改动,实测零处」。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --browser bundled</automated>
    <fails_when>exit code is not 2 (item 5 的两条 --ai-smoke 腿在无 --ai-smoke 时按设计 BLOCKED), or any verdict line beginning with "FAIL", or the "=== 逐项结论 ===" block showing a non-zero FAIL count for any item, or any BLOCKED entry outside item 5</fails_when>
    <automated>.venv/bin/python scripts/check-06-idi05-validation.py</automated>
    <fails_when>exit code is not 0, or any verdict line beginning with "FAIL", or any BLOCKED entry in the summary block</fails_when>
    <automated>.venv/bin/python scripts/check-07-idi08-validation.py</automated>
    <fails_when>exit code is not 0, or any verdict line beginning with "FAIL", or any BLOCKED entry in the summary block</fails_when>
    <automated>.venv/bin/python scripts/probe-05-resolve-color.py</automated>
    <fails_when>non-zero exit, or any line on stderr naming a failed assertion</fails_when>
    <automated>.venv/bin/python scripts/probe-07-focus-composite.py</automated>
    <fails_when>non-zero exit, or any line on stderr naming a failed assertion</fails_when>
  </verify>
  <acceptance_criteria>
    - `check-05 --browser bundled` 的 `=== 逐项结论 ===` 块里每一项的 FAIL 计数均为 0;退出码为 2;BLOCKED 只出现在 item 5(两条 `--ai-smoke` 腿)。
    - `check-06` / `check-07` / `probe-05` / `probe-07` 的退出码均为 0。
    - `check-05` 的 `[p1] .hint 实际背景 == var(--color-surface-card)` 为 PASS(不是 BLOCKED)。
    - `check-05` 的两条 `#doc-panel-header box-shadow == none` / `#ai-panel .panel-header box-shadow == none` 对照组为 PASS。
    - `check-05` item 3 的 `#doc-panel-body padding == "32px 40px"` 与 `.panel-header padding-top == "6px"` 为 PASS;item 9 的滚动者普查为 PASS。
    - `check-06` g3 / g5 / g6 全 pass(竖条几何 / 340px 单行 / 折叠往返 + 两条 `box-shadow 恒 none` 对照组)。
    - `git diff scripts/check-05-ui-uat.py` 相对计划 01 的产出为空(**预期零处门改动**);若不为空,则 SUMMARY 里逐条列出改动行、旧期望、新期望与依据,且每处都是「期望侧换指到新事实」而非判据弱化。
    - `git status --porcelain frontend/` 仅列出 `frontend/style.css`。
  </acceptance_criteria>
  <done>五条浏览器门复跑完毕,零 FAIL;`check-05` 全量退出码 2 且唯一的 BLOCKED 是 item 5 的两条 `--ai-smoke` 腿;分诊结论与原始输出逐条记入 SUMMARY(预期零处门改动)。</done>
</task>

<task type="auto">
  <name>Task 2: 四个静态门 + pytest 基线 + 仓库卫生复核</name>
  <files>scripts/check-05-ui-uat.py</files>
  <reversibility rating="reversible">本任务不产生任何产品代码改动;它是对已落地状态的复核,失败只暴露问题、不引入问题。</reversibility>
  <read_first>
    - `scripts/check-01-token-conformance.sh` 全文 —— 围栏的 START / END 配对断言、围栏外裸 `#hex` 与 tier-1 原语引用的计数逻辑(`radix` 分支是承重的)
    - `scripts/check-02-contrast.py` `:1-40` 与 `:135-235` —— 阈值常量、覆盖地板 24/20/4、`raw_pairs == len(pairs)` 计数一致性、输出格式
    - `scripts/check-03-hidden-uniqueness.sh` / `scripts/check-04-important-count.sh` 全文 —— `^[[:space:]]*\.hidden[[:space:]]*\{` 计数 == 1、`!important;` **声明**计数 == 1
    - `.planning/ROADMAP.md` §`### Phase 9:` 的 `**Gates**:` 行 —— 本任务逐条覆盖它列出的每一条
    - `.planning/phases/idi-09-card-containers/09-CONTEXT.md` §`门禁环境事实(省得重踩)` —— pytest 必须用项目 `.venv`,基线 `219 passed / 6 skipped`
    - `.planning/config.json` —— `workflow.test_command` 为 `.venv/bin/python -m pytest backend/tests -q --tb=short`
  </read_first>
  <action>
    **第 1 步 —— 逐条跑四个静态门,记录原始输出。** `bash scripts/check-01-token-conformance.sh` / `.venv/bin/python scripts/check-02-contrast.py` / `bash scripts/check-03-hidden-uniqueness.sh` / `bash scripts/check-04-important-count.sh`。把每条的标准输出原文与退出码抄进 SUMMARY。

    **第 2 步 —— 复核 `check-02` 的 8 条受影响配对。** 从输出里逐条摘出这 8 行并抄进 SUMMARY:`--color-text` on page(14.30)/ `--color-text-secondary`(5.19)/ `--color-text-muted`(5.19)/ `--color-focus`(5.15)/ `--color-border-hover`(5.19)/ `--color-marker-active` on page NON-TEXT(4.18)/ `--color-marker-active` on card TEXT(4.77)/ `--color-border-strong` on card NON-TEXT(3.32)。同时记录 ORDER 行(`ORDER 0.363 …`)。这 8 个数字必须与 `frontend/style.css` 清单历史段的登记值逐位一致 —— **不一致就是登记错了**,按产品缺陷报回,不得改清单去迁就实跑(那是把结论改成想要的样子)。

    **第 3 步 —— pytest 基线。** 用项目 `.venv` 跑 `.venv/bin/python -m pytest backend/tests -q --tb=short`,记录摘要行。期望 `219 passed, 6 skipped`。**不得**用环境的 `python3`(它是 miniconda,会让 4 个 `ai_caller` 测试假失败,把基线误判成回归)。若数字与基线不同,逐条查明差异来源再下结论。

    **第 4 步 —— `node --check frontend/app.js`。** 记录退出码(期望 0)。`app.js` 本阶段零字节改动,这条是形式化复核,证明本阶段确实没碰它。

    **第 5 步 —— 仓库卫生。** 记录 `git status --porcelain frontend/`(期望仅 `M frontend/style.css`)、`ls frontend/vendor/`(期望仅 `marked.min.js`)、`git status --porcelain`(确认改动面只落在 `frontend/style.css`、`scripts/` 与 `.planning/phases/idi-09-card-containers/`)、以及 `grep -o '/\* PAIR' frontend/style.css | wc -l` == 53、`grep -o '/\* ORDER' frontend/style.css | wc -l` == 1。

    **第 6 步 —— 不触碰任何代码。** 本任务只跑命令与记录;不编辑任何文件(SUMMARY 除外)。任何一条不达标都按产品缺陷报回,不就地修。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>non-zero exit, or stdout not exactly "PASS"</fails_when>
    <automated>.venv/bin/python scripts/check-02-contrast.py</automated>
    <fails_when>non-zero exit, or any line beginning with "FAIL", or the final line not "PASS: 0 failures"</fails_when>
    <automated>bash scripts/check-03-hidden-uniqueness.sh</automated>
    <fails_when>non-zero exit, or stdout not exactly "PASS"</fails_when>
    <automated>bash scripts/check-04-important-count.sh</automated>
    <fails_when>non-zero exit, or stdout not exactly "PASS"</fails_when>
    <automated>node --check frontend/app.js</automated>
    <fails_when>non-zero exit, or any output written to stderr</fails_when>
    <automated>.venv/bin/python -m pytest backend/tests -q --tb=short</automated>
    <fails_when>non-zero exit, or the summary line not "219 passed, 6 skipped"</fails_when>
    <automated>git status --porcelain frontend/</automated>
    <fails_when>output contains any path other than "frontend/style.css", or output is empty</fails_when>
    <automated>ls frontend/vendor/</automated>
    <fails_when>output contains any name other than "marked.min.js"</fails_when>
  </verify>
  <acceptance_criteria>
    - 四个静态门全部打印 `PASS`(`check-02` 为 `PASS: 0 failures`)。
    - `check-02` 输出里 8 条受影响配对的数值为 14.30 / 5.19 / 5.19 / 5.15 / 5.19 / 4.18 / 4.77 / 3.32,且与 `frontend/style.css` 清单历史段的登记值逐位一致;ORDER 行仍为 `ORDER 0.363`。
    - `grep -o '/\* PAIR' frontend/style.css | wc -l` == 53;`grep -o '/\* ORDER' frontend/style.css | wc -l` == 1。
    - `.venv/bin/python -m pytest backend/tests -q --tb=short` 的摘要行为 `219 passed, 6 skipped`,退出码 0。
    - `node --check frontend/app.js` 退出码 0 且无输出。
    - `git status --porcelain frontend/` 仅含 `frontend/style.css`;`ls frontend/vendor/` 仅含 `marked.min.js`。
    - `git status --porcelain` 列出的改动路径只落在 `frontend/style.css`、`scripts/check-09-idi09-validation.py`、`scripts/check-05-ui-uat.py`,以及本阶段新增的 `.planning/phases/idi-09-card-containers/` 内容;无其他路径。
    - 本任务没有编辑任何文件(除 SUMMARY)。
  </acceptance_criteria>
  <done>四个静态门全绿;8 条受影响配对的实测值与清单登记值逐位一致;pytest 基线 `219 passed, 6 skipped`;`node --check` 通过;仓库卫生三项复核通过。</done>
</task>

<task type="auto">
  <name>Task 3: 产出供用户评审的截图 + 移交说明</name>
  <files>.planning/phases/idi-09-card-containers/screenshots/</files>
  <precondition>.venv/bin/python 可导入 playwright,且 Playwright 自带 chromium 已缓存</precondition>
  <reversibility rating="reversible">只新增 PNG 与文档段落,不触碰任何代码;回退是删除该目录。</reversibility>
  <read_first>
    - `scripts/check-09-idi09-validation.py`(计划 01 产出)—— `--screenshot DIR` 参数的实现与它遍历的状态样本清单
    - `scripts/ui-states/` —— 5 个状态样本目录(p1 / p12 / p3 / checking / archive);截图应覆盖全部 5 个,使「会话流 / 批注流 / 自检报告 / 归档只读」四类版式都被看到
    - `scripts/check-05-ui-uat.py` `:480-506` —— `make_fixture` 与 `HIDDEN_MATRIX`:5 个样本各自哪个面板可见(`p1` 会话流 / `p3` 批注流 / `checking` 自检报告 / `archive` 归档),这决定每张图能看到哪张卡片
    - `frontend/index.html` `:12-92` —— 五个容器的 DOM 结构,便于在截图里逐一点认
    - `.planning/phases/idi-09-card-containers/09-CONTEXT.md` §`留待用户看图后裁定的开放项` —— 截图评审时要提请裁定的项
    - `.planning/REQUIREMENTS.md` §`Out of Scope` —— 明确「本阶段不得预先构建」的四项(表格重做 / 圆角刻度收敛 / 图标与空状态 / 暗色模式)
    - `.planning/ROADMAP.md` §`### Phase 9:` Deliverables 最后一条与 Goal 末句 —— 截图是阶段收口的交付物,用户据此裁定后续候选
  </read_first>
  <action>
    **第 1 步 —— 出图。** 跑 `.venv/bin/python scripts/check-09-idi09-validation.py --screenshot .planning/phases/idi-09-card-containers/screenshots`,覆盖 5 个状态样本(p1 / p12 / p3 / checking / archive),每张为 1440×900 的整窗截图。文件名须自解释(样本名进文件名,例如以样本名作主干的 PNG),使读者不看 SUMMARY 也能对上号。

    **第 2 步 —— 自检每张图至少能看到三件事。** (a) 页面是灰的(`#f0f0f0`);(b) 该样本下可见的容器是白的、与页面有可见边界与圆角;(c) 卡片之间有灰色间隙(12px)。`archive` 样本还要能看到归档只读态(0.75 透明合成)与卡片并存而不互相干扰。若某张图看不到这些,说明出图时机(样本切换 / 等待渲染)不对,重出 —— 不要把「图出了」当「图对了」。

    **第 3 步 —— 在 SUMMARY 里写明截图路径与提请用户裁定的开放项。** 逐项写明「本阶段未构建」及其依据:
    - `.overlay-card` 的底色(`frontend/style.css:819` 当前是 `--color-surface` gray-2 + `--shadow-overlay`)。页面下沉后它会显得比主界面卡片「内陷一档」;是否改白以同族 = **设计决策,本阶段不动**(`09-CONTEXT.md` 已登记为留待裁定的开放项)。
    - 卡片边界与阴影的**强度**:边界取的是既有 `--color-border-subtle`(gray-6,与 `#doc-panel` 原有边界同令牌)、阴影取的是用户裁定的 `0 1px 2px rgba(0, 0, 0, 0.04)`。层次目前主要靠底色差(ΔL≈6%)。是否要更强的边界 = 设计决策,本阶段不动。
    - **页面级留白**:本阶段没有给 `#main-pane` 加 `padding`、也没给卡片加 `margin`(那会移动既有几何并可能打在滚动 / 命中区门上)。卡片因此贴着视口上/下边缘。是否要留白 = 未裁定项,本阶段不动。
    - 明确重申 **Out of Scope 四项不得预先构建**:表格重做(全边框 → 只留横向分隔线)、圆角刻度收敛(`--radius-lg: 28px` 与其他档不成比例)、图标与空状态、暗色模式。

    **第 4 步 —— 不构建任何后续候选。** 本任务只出图与写说明。发现的问题一律登记进 SUMMARY 的开放项,不就地实现(用户裁定「先看看效果」,后续 phase 待效果确认后再定)。

    **第 5 步 —— 截图不得落在 `frontend/`。** ROADMAP 的 Gate 要求 `git status --porcelain frontend/` 仅含预期文件;截图的落点是 `.planning/phases/idi-09-card-containers/screenshots/`。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --screenshot .planning/phases/idi-09-card-containers/screenshots</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or the trailing "exit=" line not "exit=0"</fails_when>
    <automated>ls .planning/phases/idi-09-card-containers/screenshots/</automated>
    <fails_when>output does not contain one PNG per state sample (p1, p12, p3, checking, archive), i.e. fewer than 5 .png entries</fails_when>
  </verify>
  <acceptance_criteria>
    - `.planning/phases/idi-09-card-containers/screenshots/` 下存在至少 5 个 PNG,覆盖 p1 / p12 / p3 / checking / archive 五个状态样本,每个文件名含其样本名。
    - `check-09 --screenshot` 命令 `exit=0`,0 FAIL / 0 BLOCKED。
    - SUMMARY 里列出全部截图路径,并逐张写明该样本下可见的是哪个容器(依 `HIDDEN_MATRIX`:p1 会话流 / p3 批注流 / checking 自检报告 / archive 归档)。
    - SUMMARY 里列出至少 3 条开放项(`.overlay-card` 底色 / 边界与阴影强度 / 页面级留白),每条写明「本阶段未构建」及其依据;并重申 Out of Scope 四项不得预先构建。
    - `git status --porcelain frontend/` 仍仅列出 `frontend/style.css`(截图未落进 `frontend/`)。
  </acceptance_criteria>
  <done>5 个状态样本的截图落在 `.planning/phases/idi-09-card-containers/screenshots/`,每张都能看到灰页面 / 白卡片 / 卡片间灰色间隙;SUMMARY 列出截图路径与至少 3 条开放项及 Out of Scope 四项的重申。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 无外部输入边界 | 本计划只跑既有验证脚本与出图:零用户输入处理、零鉴权、零数据访问、零新增网络调用(Playwright 用已缓存的 chromium,零下载)、零产品代码改动。攻击面限于本地起服务跑 Playwright |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-09-01 | Information Disclosure | 截图产物 | low | accept | 截图只含本工具的本地界面(样本状态目录在临时目录内,截图不含真实项目内容)。落点是 `.planning/phases/idi-09-card-containers/screenshots/`,不进 `frontend/`、不进发布路径 |
| T-idi-09-02 | Tampering | 分诊流程中改动回归门 | high | mitigate | 「把门跑绿」的诱惑是本计划唯一的真实风险:放宽阈值或弱化判据会让门绿而没在看。缓解:本计划只允许**一种**门改动(期望侧换指到被本阶段刻意改变的事实),形式与强度一字不变;每条改动必须逐条写进 SUMMARY(改哪一行 / 旧期望 / 新期望 / 依据哪条裁定);`<prohibitions>` 逐条列出禁止的处置方式;并复核 `scripts/check-02-contrast.py` 的 `TEXT_MIN` / `NON_TEXT_MIN` 未动 |
| T-idi-09-03 | Repudiation | 「门绿了」这一结论无原始证据 | medium | mitigate | SUMMARY 必须抄录每条门的**退出码 + 汇总块原文 + 任何 FAIL / BLOCKED 行的完整原文**,而不是只写「绿」。`check-05` 的 item 5 两条 BLOCKED 腿要按设计说明写清,防止读者把「设计如此」与「新回归」混为一谈 |
| T-idi-09-04 | Denial of Service | `check-05` 的浏览器路线选择 | low | mitigate | 本机 `.venv` 是 x86_64(Rosetta),`channel="chrome"` + `headless=True` 会 CDP 永不连上、180s 超时挂死。缓解:`<prohibitions>` 明令必须走 `--browser bundled`(自带 chromium 已缓存,零下载) |
| T-idi-09-05 | Elevation of Privilege | 无 | low | accept | 本计划不触碰鉴权、权限门、服务端路径或任何 API |
| T-idi-09-SC | Tampering | npm / pip / cargo 安装 | low | accept | 本阶段**零安装**:零新增依赖、零构建步骤(DESIGN.md D-06);Playwright 与 chromium 均已在项目 `.venv` 中就绪,不触发下载。`frontend/vendor/` 仍只有 `marked.min.js` |
</threat_model>

<verification>
**五条浏览器门:**

- `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` → `逐项结论` 零 FAIL,`exit=2`,BLOCKED 仅 item 5 的两条 `--ai-smoke` 腿
- `.venv/bin/python scripts/check-06-idi05-validation.py` → `exit=0`
- `.venv/bin/python scripts/check-07-idi08-validation.py` → `exit=0`
- `.venv/bin/python scripts/probe-05-resolve-color.py` → `exit=0`
- `.venv/bin/python scripts/probe-07-focus-composite.py` → `exit=0`

**四个静态门 + 基线:**

- `bash scripts/check-01-token-conformance.sh` / `check-03` / `check-04` → `PASS`
- `.venv/bin/python scripts/check-02-contrast.py` → `PASS: 0 failures`(8 条受影响配对 14.30 / 5.19 / 5.19 / 5.15 / 5.19 / 4.18 / 4.77 / 3.32;ORDER 0.363)
- `.venv/bin/python -m pytest backend/tests -q --tb=short` → `219 passed, 6 skipped`
- `node --check frontend/app.js` → exit 0

**仓库卫生:**

- `git status --porcelain frontend/` 仅 `frontend/style.css`;`ls frontend/vendor/` 仅 `marked.min.js`
- `grep -o '/\* PAIR' frontend/style.css | wc -l` == 53;`grep -o '/\* ORDER' frontend/style.css | wc -l` == 1

**交付物:**

- `.planning/phases/idi-09-card-containers/screenshots/` 下 5 个状态样本的 PNG
</verification>

<success_criteria>
- 五条浏览器门复跑**无新增失败**:`check-05` 零 FAIL(退出码 2 系 item 5 两条 `--ai-smoke` 腿按设计 BLOCKED),`check-06` / `check-07` / `probe-05` / `probe-07` 均 `exit=0`。
- 任何门改动都是「期望侧换指到被本阶段刻意改变的事实」,断言形式与强度一字不变,并在 SUMMARY 里逐条登记;零阈值放宽、零判据弱化、零断言删除。
- 四个静态门全绿;`check-02` 的 8 条受影响配对实测值与清单登记值逐位一致;pytest 基线 `219 passed, 6 skipped`。
- `frontend/app.js` / `index.html` / `vendor/` 零字节改动;`frontend/style.css` 在本计划内零改动。
- 5 个状态样本的截图已产出,SUMMARY 列出截图路径、逐张说明、以及至少 3 条开放项与 Out of Scope 四项的重申。
- 阶段收口时用户手上有一份可据以裁定的截图与一份可独立复核的门禁记录。
</success_criteria>

<output>
Create `.planning/phases/idi-09-card-containers/idi-09-03-SUMMARY.md` when done
</output>

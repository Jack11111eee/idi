---
phase: idi-04.1-radix
plan: 04
type: execute
gap_closure: true
wave: 4
depends_on:
  - idi-04.1-03
files_modified:
  - scripts/check-05-ui-uat.py
  - scripts/probe-05-resolve-color.py
autonomous: true
requirements:
  - CHECK-02
  - A11Y-04

estimate:
  tokens: 38000
  raw_tokens: 38000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "`resolve_color` 对**未声明**的令牌返回 `None`;对**已声明**的令牌返回与修复前逐字相同的探针 computed rgb ← CR-01 / CHECK-02 / A11Y-04"
    - "`ok()` 在**期望值**为 `None` 时记 BLOCKED(而不是落进比较分支、用 `norm(actual) == norm(None)` 恒 False 记 FAIL),使「令牌未声明」这一状态不可能被记成 PASS ← CR-01"
    - "变异证明成立:在只删掉 `--color-text-muted` 声明的临时副本上,`.hint` 那条颜色断言**修复前记 PASS、修复后记 BLOCKED**;这份对照必须逐字进 SUMMARY ← CR-01 / 本项目已记录的「守卫静默空转」失败类"
    - "修复没有把断言变成恒 BLOCKED:未变异的世界里同一条断言仍记 PASS,且全量 harness 的逐项结论与 VERIFICATION.md P3.7 基线逐项一致(0 FAIL;item 1/2/3/4/6 为 PASS 且 0 BLOCKED;item 5 为 BLOCKED (9,0,2);`exit=2`)"
    - "真实仓库的 `frontend/style.css` 逐字节未变,`frontend/` 下零改动 —— 变异只存在于浏览器侧被拦截的那一份副本里"
    - "四条守卫命令与 `pytest` 与基线一致(`check-01`/`check-03`/`check-04` 打印 `PASS`;`check-02` 末行 `PASS: 0 failures`;`219 passed, 6 skipped`)← CHECK-01 / CHECK-03 / CHECK-04 / TOKEN-01 / TOKEN-04 的复证"
    - "范围外项(W-2 / W-3 / W-4 / W-5 / W-6、CR-02、IN-01 / IN-02 / IN-03)与两条人工项被**显式登记为 deferred** 并进 SUMMARY —— 既未修,也未静默丢弃"

  artifacts:
    - path: "scripts/check-05-ui-uat.py"
      provides: "`resolve_color` 的「令牌未声明 → None」分支 + `ok()` 的「期望值为 None → BLOCKED」分支;24 处调用点与全部期望值一字未动"
      contains: "expected is None"
    - path: "scripts/probe-05-resolve-color.py"
      provides: "CR-01 的变异证明:路由拦截 `/style.css`、只删 `--color-text-muted` 声明,打印修复前 PASS / 修复后 BLOCKED 的四行对照;不是门,不进四条守卫命令契约"
      contains: "PROBE mutated-postfix-verdict=BLOCKED"

  key_links:
    - from: "`scripts/check-05-ui-uat.py` 的 `resolve_color`"
      to: "`document.documentElement` 上该令牌的声明是否存在"
      via: "修复前:探针 div 的 `style.color = var(--t)` 在 computed-value 阶段失效 → 继承 `body` 的 color;真实消费者用的是同一个 `var(--t)`,两侧退化成同一个继承值 → 断言恒真。修复后:先读 `getComputedStyle(document.documentElement).getPropertyValue(t)`,空串即返回 `None`"
      pattern: "getPropertyValue"
    - from: "`scripts/check-05-ui-uat.py` 的 `ok()`"
      to: "`resolve_color` / `resolve_token` 可能返回的 `None` 期望值"
      via: "`ok()` 的 `actual is None` 分支只看实际值;期望值侧为 `None` 时会落进比较分支。新增 `expected is None` → BLOCKED 分支后,未声明令牌记 BLOCKED 而非 FAIL(两者都不是假 PASS,但 binding scope 明写 BLOCKED)"
      pattern: "expected is None"
    - from: "`scripts/probe-05-resolve-color.py` 的 `/style.css` 路由拦截"
      to: "`frontend/style.css` L120 的 `--color-text-muted` 声明与 L415 的 `.hint` 规则"
      via: "handler 用 `route.fetch()` 取真实响应、删掉声明行后 `route.fulfill(response=resp, body=mutated)` —— 变异只活在浏览器这一侧,仓库工作树逐字节不变"
      pattern: "--color-text-muted:"

  prohibitions:
    - statement: "不得改 `frontend/style.css` —— 它是本阶段已提交的交付物,也是被验证的对象。变异只允许存在于浏览器侧被拦截的那一份副本里"
      status: active
      verification: flagged
    - statement: "不得放宽、删除或改写 `scripts/check-05-ui-uat.py` 的任何既有断言、期望值或调用点;本 run 只改 `resolve_color` 与 `ok()` 两个 helper"
      status: active
      verification: flagged
    - statement: "不得让 `ok()` 的 `expected is None` 分支吞掉真实 FAIL —— 该分支只在期望值解析不出时生效,真实树上全量 harness 的逐项结论必须与 VERIFICATION.md P3.7 基线逐项一致"
      status: active
      verification: flagged
    - statement: "不得修 W-2 / W-3 / W-4 / W-5 / W-6、CR-02、IN-01 / IN-02 / IN-03 —— 用户已显式划出范围外;若认为其中某项必须修才能关闭 CR-01,必须在计划或 SUMMARY 里明说,不得静默扩范围"
      status: active
      verification: flagged
    - statement: "不得把两条人工项(28 条 UI-SPEC backstop 陈述、E16 的 `--color-text ON --color-surface-mark` 比值归属)标为已解决"
      status: active
      verification: flagged
    - statement: "不得新增任何运行时依赖或构建步骤;不得把新探针加入四条守卫命令契约,也不得让任何门禁依赖它"
      status: active
      verification: flagged
    - statement: "不得改 `frontend/app.js` / `frontend/index.html` / `frontend/vendor/`(`vendor/` 必须仍只含 `marked.min.js`)"
      status: active
      verification: flagged
---

<objective>
关闭 VERIFICATION.md 的唯一 BLOCKER **CR-01**:`scripts/check-05-ui-uat.py` 的 `resolve_color` 不区分「令牌已声明」与「令牌未声明」,使 24 处调用点里的颜色断言在令牌改名/删除下**恒真**(假 PASS)。修法是让 `resolve_color` 在令牌未声明时返回 `None`,并让 `ok()` 把 `None` 期望值记成 BLOCKED;随后用一条与 plan 02 同规格的**变异证明**把「修复前 PASS / 修复后 BLOCKED」的对照钉死。

Purpose: `0 FAIL` 是本阶段(idi-04.1)的头条证据,而 `check-05` 正是产出它的验收仪器。D-14 把 22 条硬编码 `rgb(...)` 断言换成 `resolve_color` 调用,移除了「值层改动产生假 FAIL」的根因 —— 代价是本阶段**同时**移除了「令牌接错线/被改名时响亮 FAIL」的能力。这不是推测:VERIFICATION.md 的 B-1 在真实 chromium-1243 上拦截 `/style.css` 删掉 `--color-text-muted` 声明后复现 —— `.hint` computed 与 `resolve_color` 都变成 `rgb(32, 32, 32)`(提示灰已变成正文黑,渲染明显是坏的),而 harness 记 **PASS**。计划 02 在**同一阶段内**刚修掉一个同类的空转守卫(`check-01` 的 tier-1 交替式),并专门要求用变异证明修复不是修辞;本 run 用同一把尺子补上 `check-05` 这一处。

Output: `scripts/check-05-ui-uat.py` 里 `resolve_color` 的未声明分支与 `ok()` 的期望值 `None` 分支;新文件 `scripts/probe-05-resolve-color.py`(变异证明,可复跑);SUMMARY 里的四行对照证据与「范围外项 + 人工项」的显式登记。

**范围(用户已裁定,不得扩张):** IN SCOPE 只有 CR-01。OUT OF SCOPE 且**不修**的:W-2 / W-3(`check-01` 两处残余缺口:带空格的 `var( … )`、标记搬移)、W-4(清单缺 `--color-text ON --color-surface-mark`;plan 01 的 E16 backstop 引用了不存在的 `15.88`)、W-5(`smoke #state-badge 可见` 在元素缺席时记 PASS)、W-6(z-index 序关系只有散文注释)、CR-02(`wait_done("#btn-send")` 谓词是死代码,**预先存在**于 `6f52602`,本阶段未触碰该函数)、IN-01 / IN-02 / IN-03。两条 `human_verification` 项(28 条 backstop 陈述;E16 比值归属)是人工判断项 —— **不代它转绿,也不代它裁决**。

**本 run 不重做值层。** 已执行的 plan 01 / 02 / 03 是 DONE:25 个 Radix tier-1 / 47 个 `--color-*` / 43 对清单 / `check-01` 交替式加宽都在 HEAD 上成立且已被 VERIFICATION.md 独立复证(R1–R6、P1.1–P1.14、P2.1–P2.7、P3.2–P3.11)。本计划只修那一处 BLOCKER 并证明它被修好了。

**为什么不是 tracer:** TRACER_MODE 为 true,但本阶段是 gap-closure 而非 greenfield —— tracer 切片由**已执行的 plan 01** 承载(围栏值层 + 43 对清单 + 运行时接线断言,一条竖切贯穿 `style.css` → `check-02` → `check-05`)。本计划不新写 tracer 任务,而是按 orchestrator 的指示,以「修 `resolve_color` → 用变异证明它 → 复跑全量 harness」这条**最小的端到端切片**领起。

**两个 checkpoint 探测器的结论(留档,避免复核时再问):** `api-coverage` 与 `assumption-delta` 对 phase scope 均返回 `detected: false`(本阶段不集成任何外部 API/SDK;不引入第二平台/可选字段/由导出变选定的假设)。故不产出 `COVERAGE.md`,也不产出 assumption-delta 决策块。

**决策归属(可追溯性,不是覆盖声明):** 本 run **只落地 D-14 的代价条款** —— D-14 把断言改成令牌接线时自陈「这确实牺牲了『硬编码值能抓令牌接错线』的那部分检测力」,CR-01 正是那部分检测力丧失后的具体形态,本 run 把它补回。**D-01…D-13、D-15、D-16 已由已执行的 plans 01–03 落地**,本 run 不重做、不改写它们的口径,也不重新认领它们的交付物。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/idi-04.1-radix/idi-04.1-CONTEXT.md
@.planning/phases/idi-04.1-radix/idi-04.1-VERIFICATION.md
@.planning/phases/idi-04.1-radix/idi-04.1-02-PLAN.md
@.planning/phases/idi-04.1-radix/idi-04.1-03-PLAN.md
@.planning/phases/idi-04-tokens-contract/idi-04-UAT.md
@scripts/check-05-ui-uat.py
</context>

<assumptions>
**Spec-less probe fallback(本阶段无 `*-SPEC.md`,`EDGE_ABSENT` / `PROHIB_ABSENT`)。** 边角覆盖报告 12 行**全部** `unclassified` / `unresolved`(`coverage: {applicable:12, resolved:0, unresolved:12, byVerification:{explicit:0,backstop:0}}`)。按 §A,`unclassified` 行保持 `unresolved`、绝不用 backstop 自动转绿,并以**显式 flagged assumption** 形式记录 —— 不从它们铸造 `must_haves.truths` 谓词,也不静默丢弃:

| 需求 | 类别 | 状态 | 本 run 的处置 |
|---|---|---|---|
| TOKEN-01 | unclassified | unresolved | 沿用已执行 plans 01–03 的处置,不重新推导 |
| TOKEN-02 | unclassified | unresolved | 同上(其机械缺口 W-2 属范围外,见 `<deferred>`) |
| TOKEN-04 | unclassified | unresolved | 同上 |
| TOKEN-07 | unclassified | unresolved | 同上(其机械缺口 W-6 属范围外,见 `<deferred>`) |
| CHECK-01 | unclassified | unresolved | 同上 |
| CHECK-02 | unclassified | unresolved | 同上;**本 run 交付的是它的验收仪器侧** |
| CHECK-03 | unclassified | unresolved | 同上 |
| CHECK-04 | unclassified | unresolved | 同上 |
| A11Y-04 | boundary | unresolved | 同上;探针问句「min/max/阈值两侧各一步会怎样」在值层由 `check-02` 的实测比值回答,本 run 不动 |
| A11Y-04 | precision | unresolved | 同上;探针问句「精度损失/溢出/舍入与平局规则的确切契约」在值层由 `check-02` 的 WCAG 公式回答,本 run 不动 |
| A11Y-04b | boundary | unresolved | 同上 |
| A11Y-04b | precision | unresolved | 同上 |

**这 12 行的处置与已执行 plans 01–03 完全相同 —— 本 run 不重新推导它们**(gap-closure 的范围只有一个 BLOCKER)。它们继续以 `unresolved` 存在,由 Phase 5/6/7 与最终验收自行面对。

**UI-SPEC `## UI Considerations` 的 lift 同样不重做:** `idi-04.1-UI-SPEC.md` 的 `## UI Considerations` 已被 plans 01–03 按同一条规则 lift 过(28 条 `verification: backstop` 陈述进了 plan 01 的 `must_haves`)。本 run 只**引用**它们(它们是两条 `human_verification` 项的来源),不重 lift、不复制、不改写。
</assumptions>

<deferred>
**用户显式裁定为范围外、本 run 不修、但必须可见地登记(不得静默丢弃)。** 全部条目逐字来自 VERIFICATION.md `## Anti-Patterns Found` 与 frontmatter `human_verification`:

| 编号 | 位置 | 性质 | 本 run 的处置 |
|---|---|---|---|
| W-2 (WR-01) | `scripts/check-01-token-conformance.sh:41-43` | 交替式要求 `var(--` 无空格,CSS 允许 `var( --radix-gray-11 )` → TOKEN-02 的硬不变量仍有机械缺口 | deferred,不修 |
| W-3 (WR-02) | `scripts/check-01-token-conformance.sh:17-27` | 成对断言只数 START/END 数量、不管位置;标记被搬移时 `$outside` 退化为空而打印 `PASS` | deferred,不修 |
| W-4 (WR-03) | `frontend/style.css:279-341` 清单 + plan 01 的 E16 backstop | 清单缺 `--color-text ON --color-surface-mark`;引用的 `15.88` 实为 `--color-text ON --color-surface-page` 的数,该引用在 `check-02` 输出里不存在(实测 text-on-mark = 15.0:1) | deferred,不修;与人工项 2 同源 |
| W-5 (WR-04) | `scripts/check-05-ui-uat.py:996-997` | `read_style(...) != "none"` 在元素缺席时返回 `None`,`None != "none"` 为真 → `smoke #state-badge 可见` 记 PASS | deferred,不修(同文件 `item1` L404-405 的写法是对的,但改它属范围外) |
| W-6 | `frontend/style.css:229-231` | z-index 序关系(`badge < banner`)只有散文注释,无任何脚本比较两个值;`--z-overlay` 无运行时断言 | deferred,不修 |
| CR-02 | `scripts/check-05-ui-uat.py:873-883`(`wait_done`)、923-930(发送分支) | `wait_done("#btn-send")` 的谓词是 `el.disabled === false`,而 `app.js` 只在归档态 disable `#btn-send` → 90s 截止是死代码 | deferred,不修;**预先存在**(`6f52602`),本阶段未触碰 `run_ai_smoke` |
| IN-01 | `scripts/check-05-ui-uat.py:477-480` | `goto_frozen_round(page, item)` 的 `item` 参数从未使用 | deferred,不修 |
| IN-02 | `scripts/check-05-ui-uat.py:845` vs `:926` | 同一验收项在两个运行模式下标签不同(`[p3]` / `[p12]`) | deferred,不修 |
| IN-03 | `scripts/check-05-ui-uat.py:842-847` / `1124-1127` | 默认运行必然 `exit 2`(`code = 1 if any_fail else (2 if any_blocked else 0)`) | deferred,不修(文档已记明) |
| H-1 | VERIFICATION.md frontmatter `human_verification[0]` | 28 条 UI-SPEC backstop 陈述(约 21 条无自动化证据) | deferred 为**人工判断项**;不代其转绿 |
| H-2 | VERIFICATION.md frontmatter `human_verification[1]` | E16 的 `--color-text ON --color-surface-mark` 比值归属 | deferred 为**人工判断项**;不代其裁决 |

**本 run 的范围外项不计入「未规划项」** —— 它们是用户在 `--gaps` 裁定里逐条点名的 deferred,不是遗漏。CR-01 的关闭不依赖其中任何一条:CR-01 的成因是 `resolve_color` 的退化分支,与 W-2…W-6 / CR-02 / IN-* 无因果关系。
</deferred>

<tasks>

<task type="auto">
  <name>Task 1: `resolve_color` 区分「已声明 / 未声明」,`ok()` 把 `None` 期望值记 BLOCKED</name>
  <files>scripts/check-05-ui-uat.py</files>
  <reversibility rating="reversible">两处都是小改动(一个 helper 的 JS 前置检查 + `ok()` 的一个分支),回退是两处编辑;但它确实改变了 harness 对「期望值解析不出」这一状态的判定类别(FAIL → BLOCKED),故 docstring 与退出码释义需同批对齐。</reversibility>
  <read_first>
    - `scripts/check-05-ui-uat.py` L1-58 —— 模块 docstring:退出码语义(`0/1/2` 的定义在 L39-42,`2` 的释义含「状态造不出 / 元素不可见 / 选择器不存在」)、设计要点
    - `scripts/check-05-ui-uat.py` L80-160 —— 断言记录器:`_emit`、`ok`(L102-114)、`norm`(L117-121)、`ok_true`、`ok_contains`、`blocked`、`info`、`item_verdict`
    - `scripts/check-05-ui-uat.py` L229-292 —— `_READ_JS`、`read_style`、`read_classlist`、`resolve_color`(L250-262)、`resolve_token`(L265-275,参照形状)、`effective_bg`
    - `scripts/check-05-ui-uat.py` L490-500 / L580-690 / L770-840 / L965-1005 —— 24 处 `resolve_color` 调用点的全部聚集区(含 L775、L804-826),确认已声明令牌下的行为**一字不改**
    - `scripts/check-05-ui-uat.py` **L271** 与 **L782** —— 仓库里**仅有的两处** `getPropertyValue`:L271 在 `resolve_token`(本次修复的参照形状),L782 在 item4 的 `--text-base` 存活断言里(与本 run 无关,但它在下面那条 `grep -c` 门里计入分母 —— 漏读它正是本计划早先算错这个数的原因)
    - `.planning/phases/idi-04.1-radix/idi-04.1-PATTERNS.md` §check-05(L220-283,尤其 L278-279)—— 该 Pattern Map 已把本 run 要恢复的不变量写成纪律:「`resolve_color` return `None` … `ok()` turns `None` into `BLOCKED`, never a pass — preserve that」
    - `.planning/phases/idi-04.1-radix/idi-04.1-VERIFICATION.md` `## Gaps Summary` 与 `## Behavioral Spot-Checks` 的 **B-1** 行 —— 缺陷的独立复现与「修复面很小且有验证过的形态」的原文
    - `.planning/phases/idi-04.1-radix/idi-04.1-CONTEXT.md` **D-14** —— 「全部改为令牌接线表述」的决定与它自陈的代价条款(「这确实牺牲了『硬编码值能抓令牌接错线』的那部分检测力」);本 run 正是补这个代价
    - `.planning/phases/idi-04.1-radix/idi-04.1-03-PLAN.md` —— D-14 的落地条款与「每条接线断言旁 `info()`」的补偿条款
  </read_first>
  <action>
    **本任务只动 `scripts/check-05-ui-uat.py` 的两个 helper,不动任何调用点、期望值或断言。**

    **改动 1 —— `resolve_color`(L250-262)加一条「令牌未声明」的前置分支。** 在探针 div 被创建**之前**,先在页面里读 `getComputedStyle(document.documentElement).getPropertyValue(t)`;把该字符串 `trim()` 后若为空(空串或纯空白),直接返回 `null`(Python 侧即 `None`)。**已声明令牌的路径逐字保留**:创建 `div` → `p.style.color = \`var(${t})\`` → `document.body.appendChild(p)` → 读 `getComputedStyle(p).color` → `p.remove()` → 返回该值。docstring 补一句:未声明令牌返回 `None`,与 `resolve_token`(L265-275)同形 —— 后者已是这个形状,是本次修复的参照。**该 docstring 不得逐字复述那串读取表达式**(照 plan 02 Task 1 的同款纪律:仓库里现有 2 处 `getPropertyValue` —— L271 的 `resolve_token` 与 L782 的 item4 `--text-base` 断言,本改动加第 3 处;注释里再抄一遍会让下面的 `grep -c` 计数从 3 变成 4);用散文说「先确认 `documentElement` 上该令牌确有声明」即可。

    **改动 2 —— `ok()`(L102-114)加一条「期望值解析不出」的分支。** 在现有 `if actual is None:` 分支**之前**插入 `if expected is None:` 分支:`_emit(item, "BLOCKED", label, "<UNRESOLVED>", actual, "令牌未声明或期望值解析失败")`。其余三条路径(`actual is None` → BLOCKED、`norm(actual) == norm(expected)` → PASS、否则 FAIL)与 `norm` 本身**逐字保留**。docstring 补一句说明这两类 BLOCKED 的区别(实际值读不到 vs 期望值解析不出)。

    **为什么必须加改动 2(把它写进 SUMMARY 的理由段):** `ok()` 现有的 `actual is None` 分支只看**实际值**。`resolve_color` 未声明时返回的是**期望值**侧的 `None`,不加这一支会落进比较分支 —— `norm(actual) == norm(None)` 恒为 False —— 于是记 **FAIL**。FAIL 同样**不是**假 PASS(证伪能力已经恢复),但本次 `--gaps` 的 binding scope 明写「使 `ok()` 记 BLOCKED 而非假 PASS」,故必须补上这一支才能兑现该措辞。附带收益:走 `resolve_token` 的**四条**断言(L750-752 的三条 item4 z-index 断言 `#selection-menu` / `#state-badge` / `#stream-banner`,加 L1008 smoke 的 `--z-badge` 断言)本来就该有这个对称保护。

    **改动 3 —— 模块 docstring L42 的退出码释义对齐。** 把 `2` 的括号释义从「状态造不出 / 元素不可见 / 选择器不存在」扩为「状态造不出 / 元素不可见 / 选择器不存在 / 期望值解析不出」。**只改这一处括号,不动 L39-41 的 `0` / `1` 释义,也不动文件其余任何散文。**

    **明确不做:** 不改 24 处调用点、不改任何 `expected` 字面值、不改 `read_style` / `effective_bg` / `resolve_token` / `norm` / `parse_rgb` / `item_verdict` / `_emit`;不修 W-5(`item_smoke` 的 `!= "none"`)与 CR-02(`wait_done` 的谓词)—— 两者都是范围外;不重构本文件。

    **证伪由 Task 2 承担。** 本任务的门是「不回归」:在真实树上全量 harness 的逐项结论必须与 VERIFICATION.md P3.7 基线逐项一致(见下)。
  </action>
  <verify>
    <automated>grep -c 'getPropertyValue' scripts/check-05-ui-uat.py</automated>
    <fails_when>计数不等于 3(`resolve_token` L271 原有 1 处 + item4 的 `--text-base` 存活断言 L782 原有 1 处 + `resolve_color` 新增 1 处;若为 4 说明 `resolve_color` 的 docstring 逐字复述了那串读取表达式,若为 2 说明前置分支没写进去 —— 先跑 `grep -n 'getPropertyValue' scripts/check-05-ui-uat.py` 看命中的行号再判因,不要凭计数猜)</fails_when>
    <automated>grep -c 'expected is None' scripts/check-05-ui-uat.py</automated>
    <fails_when>计数不等于 1(`ok()` 的新分支缺失,或被重复写入)</fails_when>
    <automated>.venv/bin/python -m py_compile scripts/check-05-ui-uat.py</automated>
    <fails_when>非零退出(Python 语法错误)</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py</automated>
    <fails_when>输出中出现任何 `FAIL` 行;或 `item 1`/`item 2`/`item 3`/`item 4`/`item 6` 任一行的结论不是 `PASS (n,0,0)`(出现 BLOCKED 说明修复把真断言变成了 BLOCKED);或 `item 5` 那行不是 `BLOCKED  (9,0,2)`;或末行不是 `exit=2  (0=全 pass,1=有 fail,2=有 blocked)`</fails_when>
    <automated>git status --porcelain -- frontend/</automated>
    <fails_when>输出非空(`frontend/` 下任何文件被改动 —— 本任务只允许改 `scripts/` 下的文件)</fails_when>
  </verify>
  <acceptance_criteria>
    - `resolve_color` 的 JS 里存在「先读 `documentElement` 上该令牌的声明、为空即返回 `null`」的前置分支;已声明令牌的探针路径(建 div → `var()` → appendChild → 读 computed color → remove → 返回)逐字保留
    - `grep -c 'getPropertyValue' scripts/check-05-ui-uat.py` 等于 3(仓库原有 2 处:L271 的 `resolve_token`、L782 的 item4 `--text-base` 断言;加 `resolve_color` 新增 1 处);`grep -c 'expected is None' scripts/check-05-ui-uat.py` 等于 1
    - `ok()` 的 `expected is None` 分支在 `actual is None` 分支之前,记 `BLOCKED`;其余三条路径与 `norm` 一字未动
    - 模块 docstring L42 的 `2` 释义已含「期望值解析不出」,`0`/`1` 释义未动
    - `.venv/bin/python scripts/check-05-ui-uat.py` 输出 0 条 `FAIL`;item 1/2/3/4/6 结论为 `PASS` 且 BLOCKED 计数为 0;item 5 为 `BLOCKED  (9,0,2)`;末行 `exit=2` —— 与 VERIFICATION.md P3.7 基线逐项一致
    - `git status --porcelain -- frontend/` 输出为空
    - 24 处 `resolve_color` 调用点、`resolve_token`、`read_style`、`effective_bg`、`item_smoke` 的 `!= "none"` 写法、`wait_done` 的谓词全部一字未动
  </acceptance_criteria>
  <done>`resolve_color` 在令牌未声明时返回 `None`(不再是继承色),`ok()` 把 `None` 期望值记 BLOCKED;真实树上全量 harness 的逐项结论与基线逐项一致(0 FAIL、item 5 恰两条 BLOCKED、`exit=2`),`frontend/` 零改动。</done>
</task>

<task type="auto">
  <name>Task 2: 变异证明 —— 删掉 `--color-text-muted` 声明后该断言不再记 PASS(修复前 PASS / 修复后 BLOCKED)</name>
  <files>scripts/probe-05-resolve-color.py</files>
  <read_first>
    - `scripts/check-05-ui-uat.py` L60-78 —— imports、`ROOT` / `STATES_SRC` / `VENV_UVICORN` / `HOST, PORT` / `BASE_URL` 的定位方式
    - `scripts/check-05-ui-uat.py` L200-227 —— `port_open` / `ensure_server`(「端口已在服务则复用,不新起、结束时也不关闭」的既有纪律)
    - `scripts/check-05-ui-uat.py` L229-292 —— `_READ_JS` / `read_style` / `resolve_color`(本任务要对照的对象)/ `resolve_token` / `effective_bg`
    - `scripts/check-05-ui-uat.py` L294-330 —— `make_fixture`(复制 `scripts/ui-states/<name>` 到临时目录)/ `enter_project`(导航 + 经 `#enter-path-input` + `#btn-enter` 进入样本;SSE 常驻故禁 `networkidle`)
    - `scripts/check-05-ui-uat.py` L1054-1111 —— `main()` 的浏览器启动(`--browser bundled` 默认:`pw.chromium.launch(headless=True)`)与 `finally` 收尾(关浏览器、关自起的 uvicorn、清临时目录)
    - `frontend/style.css` L120(`--color-text-muted: var(--radix-gray-11);` —— 围栏内**唯一**一处声明)与 L415(`.hint { color: var(--color-text-muted); … }`)
    - `.planning/phases/idi-04.1-radix/idi-04.1-02-PLAN.md` Task 1 —— 变异证明的规格(临时副本 + 「旧守卫会空转」的对照证据 + 「必须确认仓库工作树逐字节未变」)与本项目对 **darwin/BSD `sed` 静默不替换**的纪律
    - `.planning/phases/idi-04.1-radix/idi-04.1-VERIFICATION.md` `## Behavioral Spot-Checks` 的 **B-1** 行 —— 验证者用**路由拦截 `/style.css`** 复现该缺陷的既有做法(本任务的机制来源)
  </read_first>
  <action>
    新建 `scripts/probe-05-resolve-color.py` —— **这是 CR-01 的变异证明,不是门**。文件顶部注释必须写明:它不进四条守卫命令契约、不被任何门禁/CI 调用,存在的唯一目的是把「修复前 PASS / 修复后 BLOCKED」的对照变成可复跑的证据。

    **复用 harness 而不是另写一套。** 用 `importlib.util.spec_from_file_location` 按路径导入 `scripts/check-05-ui-uat.py`(该文件末尾是 `if __name__ == "__main__": sys.exit(main())`,导入无副作用),复用它的 `ensure_server` / `make_fixture` / `enter_project` / `resolve_color` / `read_style` / `ok` / `norm` / `ROWS` / `HOST, PORT` / `BASE_URL`。**不复制这些函数的实现** —— 否则探针测的就不是真实 helper。

    **反事实常量。** 模块级常量(命名如 `PREFIX_PROBE_JS`)持有**修复前** `resolve_color` 的探针体:创建 `div` → `p.style.color = \`var(${t})\`` → `document.body.appendChild(p)` → 读 `getComputedStyle(p).color` → `p.remove()` → 返回该值。注释必须写明它引自 `68309d0`(本 run 动手前的树),以及它为什么存在:它是「没有前置分支时会算出什么」的反事实,没有它就没有对照。

    **变异只活在浏览器一侧。** 起服务用 `ensure_server()`;浏览器用 `sync_playwright().start()` + `pw.chromium.launch(headless=True)`(与 harness 默认的 `--browser bundled` 一致,**不引入新的浏览器选择逻辑**)。进入样本前先装路由:`page.route("**/style.css", handler)`。handler 内用 `route.fetch()` 取真实响应,把 body 里 `--color-text-muted:` 那一行声明**用 Python 字符串操作删掉**(逐行过滤,匹配 `--color-text-muted:` 的声明行),再用 `route.fulfill(response=resp, body=mutated)` 返回。**不得用 `sed`** —— 本机是 darwin,BSD `sed` 的 `0,/re/` 地址会静默不替换(plan 02 已实测并把它写成纪律),那会让变异变成空转、整条证明失去意义。

    **必须断言变异真的发生(空转变异的防线)。** handler 内或进入样本后断言两件事:mutated 与原始 body 不相等,且 mutated 不再含 `--color-text-muted:`。任一条不成立即退出码 1。

    **PASS A(变异)。** 新 context 新 page,装好路由后 `make_fixture("p1", tmp_root)` + `enter_project(page, proj)`,然后依次:
    1. `hint_computed = read_style(page, ".hint", "color")` —— 真实消费者的 computed 值
    2. `pre_fix_expected = page.evaluate(PREFIX_PROBE_JS, "--color-text-muted")` —— 断言它**非 None**,且 `norm(pre_fix_expected) == norm(hint_computed)`(两侧退化成同一个继承值 —— 这正是 CR-01 的机制)
    3. 调 harness 的 `ok("probe", "[mutated] .hint color == var(--color-text-muted) (pre-fix)", pre_fix_expected, hint_computed)`,然后断言 `ROWS[-1]["verdict"] == "PASS"` —— **这就是缺陷的实证**
    4. `post_fix_expected = resolve_color(page, "--color-text-muted")` —— 断言它 `is None`
    5. 调 `ok("probe", "[mutated] .hint color == var(--color-text-muted) (post-fix)", post_fix_expected, hint_computed)`,然后断言 `ROWS[-1]["verdict"] == "BLOCKED"` —— **这就是修复的实证**

    **PASS B(未变异的对照)。** 新 context 新 page,**不装路由**;同样进 p1 样本;断言 `resolve_color(page, "--color-text-muted")` 非 None 且 `norm(...) == norm(read_style(page, ".hint", "color"))`,再调 `ok(...)` 并断言 `ROWS[-1]["verdict"] == "PASS"`。这一支是「修复没有把断言变成恒 BLOCKED」的证据 —— 没有它,一个永远返回 `None` 的 `resolve_color` 也会让 PASS A 通过。

    **输出契约(下面的门按逐字串匹配,必须照印)。** 打印四行稳定前缀的行:
    - `PROBE mutation-applied=yes`
    - `PROBE mutated-prefix-verdict=PASS`
    - `PROBE mutated-postfix-verdict=BLOCKED`
    - `PROBE control-verdict=PASS`
    再打印一行逐字的对照表(把 `pre_fix_expected`、`hint_computed`、修复前判定、修复后判定四个值摊开),供 Task 3 抄进 SUMMARY。全部断言成立 → 退出码 0;任一条不成立 → 退出码 1 并在 stderr 写明是哪一条。

    **收尾照 harness 的 `finally` 写法:** 关浏览器、`pw.stop()`;自起的 uvicorn 才 terminate/wait/kill(`ensure_server` 返回 `None` 表示复用了已在服务的实例,那时不关);临时目录用 `tempfile.mkdtemp` 建、结束时清理(`--keep` 风格的保留开关可选,不做也行)。

    **明确不做:** 不改 `frontend/style.css`(变异只在被拦截的那份响应里);不改 `scripts/check-05-ui-uat.py`(本任务对它零 diff);不把探针加进四条守卫命令契约;不新增任何第三方依赖(只用标准库 + 已在 `.venv` 里的 playwright)。
  </action>
  <verify>
    <automated>.venv/bin/python -m py_compile scripts/probe-05-resolve-color.py</automated>
    <fails_when>非零退出(Python 语法错误)</fails_when>
    <automated>.venv/bin/python scripts/probe-05-resolve-color.py; echo "exit=$?"</automated>
    <fails_when>输出不含 `PROBE mutation-applied=yes`(变异是空转的),或不含 `PROBE mutated-prefix-verdict=PASS`(修复前的缺陷未被实证),或不含 `PROBE mutated-postfix-verdict=BLOCKED`(修复未被实证),或不含 `PROBE control-verdict=PASS`(对照不成立 —— 修复可能把断言变成恒 BLOCKED),或 `exit=` 不是 0</fails_when>
    <automated>git diff --exit-code -- frontend/style.css; echo "exit=$?"</automated>
    <fails_when>`exit=` 不是 0(真实样式表被变异污染 —— 变异必须只存在于浏览器侧被拦截的副本里)</fails_when>
    <automated>git status --porcelain -- scripts/check-05-ui-uat.py</automated>
    <fails_when>输出非空(本任务对 harness 的期望 delta 为零;它的改动只属于 Task 1)</fails_when>
    <automated>.venv/bin/python -c "import ast;t=ast.parse(open('scripts/probe-05-resolve-color.py').read());m=sorted({n.names[0].name.split('.')[0] for n in ast.walk(t) if isinstance(n,ast.Import)}|{n.module.split('.')[0] for n in ast.walk(t) if isinstance(n,ast.ImportFrom) and n.module});print(m)"</automated>
    <fails_when>打印的模块集合里出现任何第三方包名(除标准库与 `playwright` 之外;`playwright` 已在 `.venv` 里,不是本 run 引入的新依赖)</fails_when>
  </verify>
  <acceptance_criteria>
    - `scripts/probe-05-resolve-color.py` 存在,顶部注释明写「这是变异证明,不是门;不进四条守卫命令契约」
    - 探针按路径导入 `scripts/check-05-ui-uat.py` 并复用 `resolve_color` / `ok` / `ensure_server` / `make_fixture` / `enter_project`,不复制它们的实现
    - 变异通过 `page.route("**/style.css", …)` + `route.fetch()` / `route.fulfill(response=resp, body=mutated)` 完成,不使用 `sed`
    - 探针断言变异真的发生(mutated ≠ 原始 body 且不再含 `--color-text-muted:`)
    - 输出逐字包含 `PROBE mutation-applied=yes` / `PROBE mutated-prefix-verdict=PASS` / `PROBE mutated-postfix-verdict=BLOCKED` / `PROBE control-verdict=PASS`,退出码 0
    - 输出含一行把 `pre_fix_expected`、`hint_computed`、修复前判定、修复后判定四个值摊开的对照表(Task 3 要逐字抄进 SUMMARY)
    - `git diff --exit-code -- frontend/style.css` 退出码 0;`git status --porcelain -- scripts/check-05-ui-uat.py` 输出为空
    - 未新增任何第三方依赖;不引入新的浏览器选择逻辑
  </acceptance_criteria>
  <done>一条可复跑的变异证明落地:在只删掉 `--color-text-muted` 声明的副本上,`.hint` 颜色断言修复前记 PASS、修复后记 BLOCKED;未变异的对照仍记 PASS;真实 `frontend/style.css` 逐字节未变。</done>
</task>

<task type="auto">
  <name>Task 3: 全量门禁收口 + 把变异对照与范围外登记写进 SUMMARY</name>
  <files>.planning/phases/idi-04.1-radix/idi-04.1-04-SUMMARY.md</files>
  <read_first>
    - `.planning/phases/idi-04.1-radix/idi-04.1-04-SUMMARY.md` —— 本任务要**新建**的文件(尚不存在);形状照 `.claude/gsd-core/templates/summary.md`
    - `.planning/phases/idi-04.1-radix/idi-04.1-VERIFICATION.md` —— 全文,特别是 `## Gaps Summary`(CR-01 的成因与修复面)、`## Anti-Patterns Found`(范围外项 W-2…W-6 / CR-02 / IN-01…03 的逐条原文)、frontmatter `human_verification`(两条人工项)、`## Behavioral Spot-Checks`(B-1 与收口基线)
    - `.planning/phases/idi-04.1-radix/idi-04.1-02-SUMMARY.md` —— SUMMARY 里记录变异对照(命令 + 逐字输出 + 退出码)的既有格式,照它写
    - `.planning/phases/idi-04.1-radix/idi-04.1-03-PLAN.md` 末尾的全量门禁收口段 —— 收口任务的既有形状
    - `.planning/phases/idi-04-tokens-contract/idi-04-UAT.md` `## Carry-Forward ④` —— 「门 / 命令 / 结果」三列收口证据表的既有格式,照它写
    - `.planning/phases/idi-04.1-radix/idi-04.1-04-PLAN.md` —— 本计划的 `<deferred>` 与 `<assumptions>` 两张表(SUMMARY 要照录,不得改写口径)
  </read_first>
  <action>
    在真实树上跑完整门禁套件,并把本 run 的对照证据与范围登记写进 `.planning/phases/idi-04.1-radix/idi-04.1-04-SUMMARY.md`。**本任务不产出代码改动** —— 它产出 SUMMARY 的三块内容与一次全量复跑。

    **1. 全量门禁复跑(逐条记命令 + 逐字输出 + 退出码,照 `idi-04-UAT.md` `## Carry-Forward ④` 的三列表):**
    - 四条守卫:`bash scripts/check-01-token-conformance.sh` / `python3 scripts/check-02-contrast.py`(末行必须是 `PASS: 0 failures`,且含 `ORDER 0.363`)/ `bash scripts/check-03-hidden-uniqueness.sh` / `bash scripts/check-04-important-count.sh` —— 各自 `PASS` / 退出码 0
    - 全量 harness:`.venv/bin/python scripts/check-05-ui-uat.py` —— 0 条 `FAIL`;item 1/2/3/4/6 为 `PASS` 且 0 BLOCKED;item 5 为 `BLOCKED  (9,0,2)`;末行 `exit=2`。**逐项与 VERIFICATION.md P3.7 基线对照,逐项写明「一致」**
    - 变异证明:`.venv/bin/python scripts/probe-05-resolve-color.py` —— 退出码 0 与四行 `PROBE …` 输出
    - 回归:`.venv/bin/python -m pytest -q 2>&1 | grep -c '219 passed, 6 skipped'` —— 计数必须为 1,**按子串判定而不是匹配整行**(pytest 汇总行永远带 warning 计数与耗时后缀,实测 `219 passed, 6 skipped, 1 warning in 5.91s`,耗时每次不同);**必须走项目 venv**;环境 `python3` 是 miniconda,会让四个 `ai_caller` 测试假失败
    - 零改动面:`git status --porcelain -- frontend/` 为空;`git status --porcelain -- . ':!.claude/settings.local.json' ':!.planning/config.json'` 只出现 `scripts/check-05-ui-uat.py` / `scripts/probe-05-resolve-color.py` / 本 SUMMARY(两个排除项是本 run 动手前既有的工作树状态)

    **2. CR-01 的对照证据块(本 SUMMARY 的承重内容)。** 逐字抄进探针打印的那行四值对照表:`pre_fix_expected`(修复前的期望值 = 继承色,如 `rgb(32, 32, 32)`)、`hint_computed`(真实消费者的 computed 值)、**修复前判定 = PASS**(渲染已坏 —— 提示灰变成正文黑 —— 而 harness 记 PASS)、**修复后判定 = BLOCKED**。同时写明两条修复的**形状**:`resolve_color` 先读 `documentElement` 上该令牌的声明、为空即返回 `None`;`ok()` 把 `None` 期望值记 BLOCKED(并写明「不加这一支会落进比较分支记 FAIL —— FAIL 同样不是假 PASS,但 binding scope 明写 BLOCKED」)。再写明缺陷的**成因链**:D-14 把 22 条硬编码 `rgb(...)` 断言换成 `resolve_color` 调用,移除了假 FAIL 的根因,**同时**移除了改名/删除时的 FAIL 能力,而计划与 SUMMARY 当时只写了收益、未披露这一损失。

    **3. 范围登记(照录本计划 `<deferred>` 与 `<assumptions>` 两张表的口径,不得改写、不得省略)。** 逐条登记 W-2 / W-3 / W-4 / W-5 / W-6 / CR-02 / IN-01 / IN-02 / IN-03 为 **deferred、本 run 未修**,并写明 CR-02 是**预先存在**于 `6f52602`、本阶段未触碰 `run_ai_smoke`;逐条登记两条 `human_verification` 项(28 条 backstop 陈述;E16 的 `--color-text ON --color-surface-mark` 比值归属)为**人工判断项、本 run 不代其转绿/裁决**;逐条登记 12 行 `unclassified` / `unresolved` 边角项**沿用 plans 01–03 的处置、本 run 不重新推导**。并写明一句:CR-01 的关闭不依赖上述任何一条。

    **明确不做:** 不改 `frontend/style.css`;不改 `scripts/check-05-ui-uat.py` 或 `scripts/probe-05-resolve-color.py`(两者在 Task 1 / Task 2 已定稿);不改 `.planning/phases/idi-04-tokens-contract/idi-04-UAT.md`(它的 6 项已全 `pass`,本 run 不触碰);不改 `ROADMAP.md` 里 Phase 5 / Phase 6 已签核的验收判据(携带项 #7 的下游门引用失真属用户裁决范围);不给任何范围外项顺手补一刀。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh && python3 scripts/check-02-contrast.py</automated>
    <fails_when>任一条非零退出,或任一条 stdout 不含 `PASS`,或 `check-02` 的末行不是 `PASS: 0 failures`,或 `check-02` 的输出不含 `ORDER 0.363`</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py</automated>
    <fails_when>输出中出现任何 `FAIL` 行;或 `item 1`/`2`/`3`/`4`/`6` 任一行的结论不是 `PASS (n,0,0)`;或 `item 5` 那行不是 `BLOCKED  (9,0,2)`;或末行不是 `exit=2  (0=全 pass,1=有 fail,2=有 blocked)`</fails_when>
    <automated>.venv/bin/python scripts/probe-05-resolve-color.py; echo "exit=$?"</automated>
    <fails_when>输出不含 `PROBE mutated-prefix-verdict=PASS` 或 `PROBE mutated-postfix-verdict=BLOCKED` 或 `PROBE control-verdict=PASS`,或 `exit=` 不是 0</fails_when>
    <automated>.venv/bin/python -m pytest -q 2>&1 | grep -c '219 passed, 6 skipped'</automated>
    <fails_when>计数小于 1(基线偏移)。**按子串判定,不要匹配整行** —— pytest 的汇总行永远带 warning 计数与耗时后缀(实测 `219 passed, 6 skipped, 1 warning in 5.91s`,耗时每次不同),故整行匹配必然失败;有测试失败时该行变成 `… failed, … passed, 6 skipped`,子串即消失。必须用 `.venv/bin/python`,环境 `python3` 是 miniconda,会让四个 `ai_caller` 测试假失败</fails_when>
    <automated>git status --porcelain -- frontend/</automated>
    <fails_when>输出非空(`frontend/` 下任何文件被改动 —— 本 run 不得触碰被验证对象)</fails_when>
    <automated>git status --porcelain -- . ':!.claude/settings.local.json' ':!.planning/config.json'</automated>
    <fails_when>输出中出现除 `scripts/check-05-ui-uat.py` / `scripts/probe-05-resolve-color.py` / `.planning/phases/idi-04.1-radix/idi-04.1-04-SUMMARY.md` 之外的路径,或出现任何未跟踪的临时文件(探针的临时目录必须自清)。**范围刻意排除两个既有工作树条目**:`.claude/settings.local.json` 与 `.planning/config.json` —— 二者在本 run 动手之前就已是 modified,不是本 run 的产出</fails_when>
    <automated>grep -c 'PROBE mutated-postfix-verdict=BLOCKED' .planning/phases/idi-04.1-radix/idi-04.1-04-SUMMARY.md</automated>
    <fails_when>计数小于 1(修复后的对照判定未进 SUMMARY)</fails_when>
    <automated>grep -oE 'W-2|W-3|W-4|W-5|W-6|CR-02|IN-01|IN-02|IN-03' .planning/phases/idi-04.1-radix/idi-04.1-04-SUMMARY.md | sort -u | wc -l</automated>
    <fails_when>计数小于 9(范围外项未被逐条登记 —— 九条各自至少出现一次)。**必须数去重后的匹配项**:`grep -c` 数的是命中**行数**,九条写在同一行只会得 1,会把登记齐全的 SUMMARY 误判为失败</fails_when>
  </verify>
  <acceptance_criteria>
    - 四条守卫命令全部 `PASS` / 退出码 0;`check-02` 末行 `PASS: 0 failures` 且输出含 `ORDER 0.363`
    - `.venv/bin/python scripts/check-05-ui-uat.py` 输出 0 条 `FAIL`;item 1/2/3/4/6 为 `PASS` 且 0 BLOCKED;item 5 为 `BLOCKED  (9,0,2)`;末行 `exit=2` —— 与 VERIFICATION.md P3.7 基线**逐项**对照并写明一致
    - `.venv/bin/python scripts/probe-05-resolve-color.py` 退出码 0,输出含四行 `PROBE …`
    - `.venv/bin/python -m pytest -q 2>&1 | grep -c '219 passed, 6 skipped'` 计数为 1(pytest 汇总行永远带 warning 计数与耗时后缀,故按子串判定、不按整行)
    - SUMMARY 里有一块 CR-01 对照证据:四值对照表(`pre_fix_expected` / `hint_computed` / 修复前判定 PASS / 修复后判定 BLOCKED)+ 两条修复的形状 + 缺陷的成因链(D-14 的收益与代价)
    - SUMMARY 里逐条登记 W-2 / W-3 / W-4 / W-5 / W-6 / CR-02 / IN-01 / IN-02 / IN-03 为 deferred 且未修(CR-02 注明预先存在于 `6f52602`);逐条登记两条人工项为未解决;逐条登记 12 行 unclassified 沿用 plans 01–03 的处置
    - SUMMARY 里写明「CR-01 的关闭不依赖上述任何一条范围外项」
    - `git status --porcelain -- frontend/` 为空;`git status --porcelain -- . ':!.claude/settings.local.json' ':!.planning/config.json'` 只出现本 run 的两个脚本与 SUMMARY
  </acceptance_criteria>
  <done>四条守卫 + 全量 harness + 变异证明 + pytest 在真实树上全部与基线一致;CR-01 的四值对照与两条修复的形状进 SUMMARY;九条范围外项与两条人工项逐条登记为 deferred;`frontend/` 零改动。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 变异探针 → 浏览器侧被拦截的 `/style.css` 响应 | 唯一的「不可信输入」是探针自己构造的那份被删掉一处声明的 CSS。它**不落盘**、不进入仓库工作树 |
| 断言记录器 → 验收结论 | `ok()` 的判定类别(PASS / FAIL / BLOCKED)直接决定 harness 的退出码,也就是本阶段头条证据 `0 FAIL` 的语义 |
| 仓库工作树 → 探针 | 探针只读 `frontend/style.css` 与 `scripts/ui-states/`;不写任何仓库内文件 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi041-11 | Tampering | 变异证明污染真实 `frontend/style.css` | medium | mitigate | 变异只在 `page.route("**/style.css", …)` 拦截到的响应里构造(`route.fetch()` → 字符串删除 → `route.fulfill(response=resp, body=mutated)`),**不写任何磁盘文件**;Task 2 与 Task 3 各有一条 `git diff --exit-code -- frontend/style.css` / `git status --porcelain -- frontend/` 门,输出非空即失败 |
| T-idi041-12 | Tampering | 空转变异(变异其实没发生,证明变成空转) | medium | mitigate | 本机是 darwin,BSD `sed` 的 `0,/re/` 地址会**静默不替换**(plan 02 已实测并写成纪律)。故探针禁用 `sed`,改用 Python 字符串操作,并**显式断言** mutated ≠ 原始 body 且不再含 `--color-text-muted:`;探针必须打印 `PROBE mutation-applied=yes` 才可能通过 |
| T-idi041-13 | Repudiation | 修复被断言为「有效」而非被证明 | medium | mitigate | 每条修复断言都配一条变异运行:同一份被删掉声明的副本上,修复前记 PASS、修复后记 BLOCKED,对照逐字进 SUMMARY。这正是本项目已记录的教训 —— 变异测试是唯一能证明守卫真的会失败的手段 |
| T-idi041-14 | Tampering | 修复把断言变成**恒 BLOCKED**(另一种空转) | medium | mitigate | PASS B(未变异的对照)断言同一条断言仍记 PASS;Task 1 / Task 3 的全量 harness 门要求 item 1/2/3/4/6 的 BLOCKED 计数为 0 —— 一个永远返回 `None` 的 `resolve_color` 会被这两道门同时抓住 |
| T-idi041-15 | Tampering | `ok()` 的新分支吞掉真实 FAIL(把真缺陷降级成 BLOCKED) | medium | mitigate | 该分支**只在 `expected is None` 时生效**,而真实树上全部令牌都已声明、`resolve_color` / `resolve_token` 均返回非 None 值 —— 故 Task 1 与 Task 3 的全量 harness 门要求逐项结论与 VERIFICATION.md P3.7 基线**逐项一致**(0 FAIL、item 5 恰两条 BLOCKED、`exit=2`);任何降级都会让计数偏移而被抓住 |
| T-idi041-16 | Repudiation | 新探针被当成门禁而长期腐烂 | low | mitigate | 探针顶部注释明写「变异证明,不是门」;不得加入四条守卫命令契约,也不得让任何门禁依赖它。它是一次性证明的固化形态,不是第五条守卫 |
| T-idi041-SC | Tampering | npm / pip / cargo 安装 | none | accept | **本 run 不安装任何包**。探针只用标准库 + `.venv` 里已装的 `playwright`(harness 早已依赖它,本 run 未新增依赖);`check-01`…`check-04` 仍零依赖。供应链面为零 |

**诚实结论:本计划不存在 high 或 critical 级威胁。** 改动面是一个 helper 的前置检查、一个断言记录器的分支、以及一个只读的浏览器侧变异探针 —— 全部在本机、离线、无凭据。
</threat_model>

<verification>
- `grep -c 'getPropertyValue' scripts/check-05-ui-uat.py` == 3(仓库原有 2 处 + `resolve_color` 新增 1 处);`grep -c 'expected is None' scripts/check-05-ui-uat.py` == 1
- `.venv/bin/python scripts/check-05-ui-uat.py` 0 FAIL;item 1/2/3/4/6 `PASS` 且 0 BLOCKED;item 5 `BLOCKED (9,0,2)`;`exit=2` —— 与 VERIFICATION.md P3.7 基线逐项一致
- `.venv/bin/python scripts/probe-05-resolve-color.py` 退出码 0,含 `PROBE mutation-applied=yes` / `PROBE mutated-prefix-verdict=PASS` / `PROBE mutated-postfix-verdict=BLOCKED` / `PROBE control-verdict=PASS`
- `bash scripts/check-01-token-conformance.sh` / `bash scripts/check-03-hidden-uniqueness.sh` / `bash scripts/check-04-important-count.sh` 各自 `PASS`;`python3 scripts/check-02-contrast.py` 末行 `PASS: 0 failures` 且含 `ORDER 0.363`
- `.venv/bin/python -m pytest -q 2>&1 | grep -c '219 passed, 6 skipped'` 计数为 1(pytest 汇总行永远带 warning 计数与耗时后缀,故按子串判定、不按整行)
- `git status --porcelain -- frontend/` 为空;`git diff --exit-code -- frontend/style.css` 退出码 0
- `git status --porcelain -- . ':!.claude/settings.local.json' ':!.planning/config.json'` 只出现 `scripts/check-05-ui-uat.py` / `scripts/probe-05-resolve-color.py` / `idi-04.1-04-SUMMARY.md`
- SUMMARY 含 CR-01 四值对照表、两条修复的形状、成因链,以及九条范围外项 + 两条人工项 + 12 行 unclassified 的逐条登记
</verification>

<success_criteria>
1. CR-01 关闭:`resolve_color` 区分「令牌已声明 / 未声明」,未声明时返回 `None`;`ok()` 把 `None` 期望值记 BLOCKED —— 24 处颜色断言在令牌改名/删除下重新具备证伪能力
2. 修复被**证明**而非被断言:同一份被删掉 `--color-text-muted` 声明的副本上,修复前记 PASS、修复后记 BLOCKED,对照逐字进 SUMMARY
3. 修复没有引入另一种空转:未变异的对照仍记 PASS,全量 harness 的逐项结论与 VERIFICATION.md P3.7 基线逐项一致
4. 被验证对象未被污染:`frontend/` 零改动,变异只活在浏览器侧被拦截的副本里
5. 范围纪律:W-2 / W-3 / W-4 / W-5 / W-6 / CR-02 / IN-01 / IN-02 / IN-03 与两条人工项逐条登记为 deferred,既未修也未静默丢弃;12 行 unclassified 沿用 plans 01–03 的处置
6. 无新增依赖、无构建步骤;四条守卫命令契约与 `pytest` 基线不变
</success_criteria>

<artifacts_this_phase_produces>
**本计划新建 / 改动的符号:**

- `scripts/check-05-ui-uat.py` 的 `resolve_color(page, token)` —— **签名不变**,行为契约改变:令牌未声明时返回 `None`(此前返回探针继承到的 `body` 颜色)。新增的 JS 前置检查读 `documentElement` 上该令牌的声明
- `scripts/check-05-ui-uat.py` 的 `ok(item, label, expected, actual, note="")` —— **签名不变**,新增一条判定路径:`expected is None` → `BLOCKED`(reason `令牌未声明或期望值解析失败`,expected 打印 `<UNRESOLVED>`)
- `scripts/check-05-ui-uat.py` 模块 docstring L42 —— `2` 的括号释义扩为「状态造不出 / 元素不可见 / 选择器不存在 / 期望值解析不出」
- **新文件** `scripts/probe-05-resolve-color.py` —— CR-01 的变异证明。内部符号(命名可调,行为契约固定):`PREFIX_PROBE_JS`(修复前探针体的反事实常量,引自 `68309d0`)、`main()`、退出码 `0`(全部断言成立)/ `1`(任一条不成立)。**输出契约(逐字)**:`PROBE mutation-applied=yes` / `PROBE mutated-prefix-verdict=PASS` / `PROBE mutated-postfix-verdict=BLOCKED` / `PROBE control-verdict=PASS`。它**不是**门,不进四条守卫命令契约
- **新文件** `.planning/phases/idi-04.1-radix/idi-04.1-04-SUMMARY.md` —— 本计划执行时由 executor 产出(CR-01 对照证据块 + 范围登记块)

**删除的符号:** 无。24 处 `resolve_color` 调用点、全部 `expected` 字面值、`resolve_token` / `read_style` / `effective_bg` / `norm` / `item_smoke` / `wait_done` 一字未动。

**`files_modified` 之外的一切均不改动** —— 特别是 `frontend/style.css`(被验证对象)、`frontend/app.js`、`frontend/index.html`、`frontend/vendor/`、`scripts/check-01-token-conformance.sh`、`scripts/check-02-contrast.py`、`scripts/check-03-hidden-uniqueness.sh`、`scripts/check-04-important-count.sh`、`.planning/phases/idi-04-tokens-contract/idi-04-UAT.md`。
</artifacts_this_phase_produces>

<output>
Create `.planning/phases/idi-04.1-radix/idi-04.1-04-SUMMARY.md` when done
</output>
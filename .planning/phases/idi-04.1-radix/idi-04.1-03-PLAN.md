---
phase: idi-04.1-radix
plan: 03
type: execute
wave: 3
depends_on:
  - idi-04.1-01
  - idi-04.1-02
files_modified:
  - scripts/check-05-ui-uat.py
  - .planning/phases/idi-04-tokens-contract/idi-04-UAT.md
autonomous: true
requirements:
  - A11Y-04
  - A11Y-04b
  - TOKEN-07
  - CHECK-02
  - CHECK-03
  - CHECK-04

estimate:
  tokens: 68000
  raw_tokens: 68000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "`scripts/check-05-ui-uat.py` 的全部颜色断言改为**令牌接线**形式:期望侧来自运行时解析出的 `--token`(`resolve_color`),不再硬编码 `rgb(...)`;模块常量 `FROZEN_AMBER = \"rgb(138, 101, 8)\"` 及其三处使用被删除 ← D-14"
    - "携带项 #9 的具名运行时清单**逐条覆盖**:`.hint` color、`.badge-answered` color、`#btn-authorize` color / border-color / background-color、`.kind-write .event-kind` background、`#state-badge` color / background / **z-index**、`#ai-route-select` border-top-color、`#selection-menu` border-top-color、`.overlay-card` box-shadow、`.tier-desc` computed opacity。后三项由 `idi-04.1-01-PLAN.md` Task 3 的 `item_smoke` 三条断言覆盖,本计划覆盖其余六组 ← 携带项 #9 / 硬规则 7"
    - "`#doc-pane` 的选择器字符串改为 `#doc-panel-body`(D-13),该项由 `blocked` 转为 `ok`,期望 `32px 40px`;`frontend/app.js` 的约 70 个顶层 `getElementById` id 一字未动 —— 改的是 UAT 的**期望字符串**,不是 id ← D-13 / 硬规则 5"
    - "D-12 的 7 条间距/字号漂移以**更新期望值**的方式接受 HEAD 现状,`frontend/style.css` 一字未动:`.panel-header` padding `6px` / `10px`、`#brainstorm-view h2` 16px、`#draft-view h2` 18px、`.overlay-card h3` 24px、`.markdown-body`(探针 `#draft-content`)16px、`.markdown-body code` 14px、`button` color 由 `--color-text` 解析 ← D-12"
    - "z-index 三条断言也走令牌接线:`#selection-menu` / `#state-badge` / `#stream-banner` 的 computed `z-index` 分别等于运行时解析出的 `--z-selection-menu` / `--z-badge` / `--z-banner`,使 `badge < banner` 的承重序关系在**渲染层**被断言(而不只在围栏注释里被声明)← TOKEN-07 / R-1 / D-11"
    - "D-14 已接受的检测力损失被显式补偿:每条接线断言旁都有 `info()` 记录运行时解析出的令牌值(`--color-text-muted` → `rgb(100, 100, 100)`、`--color-border-strong` → `rgb(141, 141, 141)`、`--color-action-warning` → `rgb(79, 52, 34)`、`--color-kind-done` → `rgb(32, 32, 32)`、`--color-surface` → `rgb(249, 249, 249)`),使「接线对但值错」留下可人工核对的痕迹;值本身的仲裁者是 `check-02-contrast.py`,不是本 harness ← D-14 的代价条款 / 携带项 #2"
    - "`.venv/bin/python scripts/check-05-ui-uat.py` 全量运行(默认 item 1..6,捆绑 chromium-1243 无头)退出码 **0**,0 FAIL / 0 BLOCKED;`smoke` 项亦 PASS ← 携带项 #9 / 硬规则 7"
    - "`idi-04-UAT.md` 的三条 gap 按 D-10 / D-12 / D-13 消解并留证:颜色漂移类随值层重写消解、间距字号类更新期望值、`#doc-pane` 改名;`## Gaps` 的 YAML 块不再列出任何未决项,`## Summary` 的 passed / issues 计数按新结果更新 ← D-10 / D-12 / D-13 / 携带项 #6"
    - "C-1 的下游门引用复核完成并留证:`#brainstorm-view h2` 在 HEAD 上计算为 **16px**(不是 `04-UI-SPEC.md` 携带项 #7 与 `ROADMAP.md:37` / `:166` / `:169` / `:197` / `:209` 五处所写的 14px),其颜色为 `--color-action-warning` = `#4f3422`(不是那五处所写的 `#8a6508`);全部失真引用作为**下游义务**记入 SUMMARY 与 UAT 记录,**不在本阶段单方面改写未来阶段的验收判据** ← D-12 附带必做 / 携带项 #7"
    - "携带项 #8 被记录而非执行:Phase 7 的焦点环 `--color-focus: #1f63bd` 必须在 Phase 7 自己的门里对 `--color-surface`(`#f9f9f9`)与 `--color-surface-page`(`#fcfcfc`)重新测 ≥3:1 —— 本阶段不改环色,只改它所落的地面 ← 携带项 #8"
    - "`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` 零改动,`frontend/vendor/` 仍只含 `marked.min.js` ← 携带项 #10"

  artifacts:
    - path: "scripts/check-05-ui-uat.py"
      provides: "令牌接线形式的 UAT 断言:item2 / item3 / item4 / item5 的期望侧全部来自运行时解析的 `--token`;新增对 `--z-*` 的 `resolve_token` 用法"
      contains: "resolve_color(page, \"--color-text-muted\")"
    - path: ".planning/phases/idi-04-tokens-contract/idi-04-UAT.md"
      provides: "按 D-10 / D-12 / D-13 更新后的期望值与已消解的 `## Gaps`"
      contains: "## Gaps"

  key_links:
    - from: "scripts/check-05-ui-uat.py 的 item3 / item4 / item5 断言"
      to: "frontend/style.css 围栏内的 47 个 `--color-*` 令牌"
      via: "`resolve_color` 把令牌挂到一个探针元素的 `color` 上读 computed 值,再与消费者的 computed 值比对 —— 值层再改,断言不动(D-14 的结构性修复)"
      pattern: "resolve_color\\(page, \"--color-"
    - from: "scripts/check-05-ui-uat.py 的 z-index 断言"
      to: "frontend/style.css 围栏内的 `--z-badge` / `--z-banner` / `--z-selection-menu`"
      via: "`resolve_token(page, name)` 读 `getComputedStyle(document.documentElement).getPropertyValue(name)` —— 该助手由 `idi-04.1-01-PLAN.md` Task 3 新增,本计划依赖它"
      pattern: "resolve_token\\(page, \"--z-"
    - from: ".planning/phases/idi-04-tokens-contract/idi-04-UAT.md 的 `## Gaps`"
      to: "scripts/check-05-ui-uat.py 的断言表述"
      via: "D-14 把 20 条假 FAIL 的根因(期望值定稿于值层改动之前)结构性移除:值层改动不再产生一批假 FAIL"
      pattern: "令牌接线|token"

  prohibitions:
    - statement: "不得改动 `frontend/style.css` —— 值层已在 `idi-04.1-01-PLAN.md` 落地;本计划只改断言表述与 UAT 文档。若某条断言在真实树上失败,修的是断言或把事实记下来,不是把 CSS 改回期望值"
      status: active
      verification: flagged
    - statement: "不得改 `frontend/app.js` / `frontend/index.html` / `frontend/vendor/` 任何一个字节;`#doc-pane` → `#doc-panel-body` 只是 UAT 的**期望字符串**改名,绝不是 id 改名(硬规则 5:约 70 个顶层 `getElementById` id 不得改名或删除)"
      status: active
      verification: flagged
    - statement: "不得在断言里重新引入硬编码的 `rgb(...)` 期望值(D-14);唯一允许保留颜色字面的地方是 `norm()` / `parse_rgb()` 等解析辅助与 `.overlay-card` box-shadow 的 needle(`rgba(0, 0, 0, 0.2)`,该值由 R-2 的令牌形状固定)"
      status: active
      verification: flagged
    - statement: "不得为迎合 UAT 期望值去改 S-1 间距刻度或 S-2 字号档 —— D-12 的方向是**更新期望值接受 HEAD 现状**,不是改 CSS(D-12 附带必做只要求复核下游门引用)"
      status: active
      verification: flagged
    - statement: "不得软化 8 处 `:disabled` 的 `opacity: 0.55 / 0.5` 或改动它们的断言 —— SC 1.4.3 豁免非活动组件,且它是 G3 前提条件唯一的视觉信号(Pitfall M5)"
      status: active
      verification: flagged
    - statement: "不得采信 Radix 自己的 AA 论断,也不得把 `check-02-contrast.py` 的比值换成任何文档里的数字 —— 比值一律以脚本在真实围栏上的实测为准(携带项 #2)"
      status: active
      verification: flagged
    - statement: "不得单方面改写 `ROADMAP.md` §Phase 6 SC5 的验收判据(其 `14px` / `#8a6508` 两处引用在本阶段之后失真)—— 那是未来阶段已签核的门,只记录、交用户裁决"
      status: active
      verification: flagged
    - statement: "不得把浏览器路线改成「无头系统 Chrome」或「静态分析代替渲染」来绕过验证 —— `.venv` 的 Python 是 x86_64,系统 Chrome 走 Rosetta,`channel='chrome'` + headless 在本机会挂死(CDP 180s 连不上);harness 的正确路线是默认的**捆绑 chromium-1243 无头**(零下载、arm64 原生)。换路线 = 换掉证据"
      status: active
      verification: flagged
---

<!-- planner-discipline-allow: FROZEN_AMBER -->
<!-- planner-discipline-allow: doc-pane -->
<!-- planner-discipline-allow: doc-panel-body -->

<objective>
把 `scripts/check-05-ui-uat.py` 的全部颜色断言从硬编码 `rgb(...)` 改成**令牌接线**形式(D-14),补齐 `idi-04.1-UI-SPEC.md` `## Carry-Forward Obligations` 第 9 条那条**具名运行时清单**在 `item3` / `item4` / `item5` 上的其余六组,并按 D-10 / D-12 / D-13 更新 `idi-04-UAT.md`。

Purpose: idi-04 的 20 条假 FAIL 的**单条根因**是期望值定稿于值层改动之前 —— 每次值层一动就产生一批假 FAIL,而假 FAIL 会淹掉真 FAIL。D-14 是对这个根因的**结构性修复**:断言解析运行时令牌,值层再改也不产生假 FAIL。本阶段正是那一次「值层大改」,所以它是这个修复唯一有意义的落地时机。同时,本阶段的值层改动(实心填充移到第 11 步、边框移到第 9 步、三个绿色 `-fg` 与 `--color-action-warning` 移到第 12 步)会让 UAT 里**全部**颜色字面期望失真 —— 逐条重写字面值是治标,改接线才是治本。

Output: 令牌接线形式的 `scripts/check-05-ui-uat.py`(item2 / item3 / item4 / item5 全部改完,`FROZEN_AMBER` 常量删除);`idi-04-UAT.md` 的期望值与 `## Gaps` 按 D-10 / D-12 / D-13 更新;C-1 下游门引用复核的留证;全量 harness 与四条守卫的收口证据。

**本计划与 01 的分工(不得重复):** `idi-04.1-01-PLAN.md` Task 3 已经在 `item_smoke` 里加了三条令牌接线断言(`#state-badge` 的 z-index 走 `resolve_token`、`.overlay-card` 的 box-shadow 非 `none`、`.tier-desc` 的 computed `opacity` 为 `1`),并新增了 `resolve_token(page, name)` 助手。**本计划不重复这三条**,而是在 `item3` / `item4` / `item5` 上覆盖携带项 #9 的其余六组:`.hint` color、`.badge-answered` color、`#btn-authorize` color / border-color / background-color、`.kind-write .event-kind` background、`#ai-route-select` border-top-color、`#selection-menu` border-top-color。

**本计划关闭 vs 沿用:** **关闭** D-14 的断言改造与 D-13 / D-12 的 UAT 口径修正、携带项 #6 / #7 的复核;**沿用/复证** A11Y-04、A11Y-04b、TOKEN-07、CHECK-02、CHECK-03、CHECK-04(以本计划末尾的全量门禁收口为准)。
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
@.planning/phases/idi-04.1-radix/idi-04.1-PATTERNS.md
@.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md
@.planning/phases/idi-04.1-radix/idi-04.1-01-PLAN.md
@.planning/phases/idi-04-tokens-contract/idi-04-UAT.md
@scripts/check-05-ui-uat.py
@frontend/style.css
</context>

<tasks>

<task type="auto">
  <name>Task 1: `item2` 与 `item3` 的断言改令牌接线,删除 `FROZEN_AMBER` 常量</name>
  <files>scripts/check-05-ui-uat.py</files>
  <read_first>
    - `scripts/check-05-ui-uat.py` L442-L630 —— `FROZEN_AMBER`(L445)、`parse_box_shadow`(L448-L459)、`check_frozen_marker`(L468-L511,含 L484/L501/L507 三处 `FROZEN_AMBER` 使用)、`item2`(L514-L553)、`item3`(L559-L629,15 条断言)
    - `scripts/check-05-ui-uat.py` L85-L149 —— `_emit` / `ok` / `norm` / `ok_true` / `ok_contains` / `blocked` / `info` 的语义(尤其 `ok()` 在 `actual is None` 时转 `BLOCKED`、`ok_contains` 用于子串)
    - `scripts/check-05-ui-uat.py` L232-L262 —— `_READ_JS` / `read_style` / `read_classlist` / `resolve_color` / `effective_bg`
    - `scripts/check-05-ui-uat.py` L860-L932 —— `item6`(L894-L905)与 `item_smoke`(L911-L932)是 D-14 的**在文件内的范本**,照它们的写法改
    - `.planning/phases/idi-04.1-radix/idi-04.1-PATTERNS.md` §`scripts/check-05-ui-uat.py — assertions move to token-wiring form (D-14)` —— 「要替换的硬编码字面量」清单与四条改写注意事项
    - `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` `### Tier 2 — semantic` —— 每个 `--color-*` 的新 Radix 值与 hex,用于写 `info()` 里的人工核对值
    - `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` `## Carry-Forward Obligations` 第 5 / 9 条
    - `.planning/phases/idi-04.1-radix/idi-04.1-CONTEXT.md` D-11 / D-14
  </read_first>
  <action>
    **原则:** 每条断言的**期望侧**改成「运行时解析出的令牌值」,消费者侧继续用 `read_style` / `effective_bg` 读 computed 值。`ok()` 已对 `rgb()` 内部空白做归一(L111、L117-L121),所以改动只关乎**哪一侧是动态的**;`ok()` 在任一侧为 `None` 时转 `BLOCKED` 的语义必须保留(L109-L110)—— 元素缺失或令牌解析失败绝不得记为 pass。

    **1. 删除 `FROZEN_AMBER` 常量(L445)及其三处使用(L484、L501、L507)。** 在 `check_frozen_marker` 内改为:
    - 用 `resolve_color(page, "--color-action-warning")` 取运行时值,存为局部变量(例如 `frozen_amber`)。
    - L489-L496 的 `semantic_ok` 里 `parsed["color"] == FROZEN_AMBER` 改成与该局部变量比较。
    - L484 与 L501 的 `expected` 参数改用该局部变量;L507 的 `info()` 文字里那句「`inset 3px 0 0 rgb(138, 101, 8)` present=...」改为用局部变量拼串,并保留原有解释(Chrome 把颜色序列化在最前、`inset` 在最后,故字面序不存在 —— 这是 harness 规格修正,不是产品缺陷)。
    - 冻结轮的 `opacity`(`"1"`)与 `filter`(`"saturate(0.6)"`)两条断言**保持字面值** —— 它们不是颜色令牌,且 S-4 的裁定已把它们固定为结构性标记。

    **2. `item3` 的 15 条断言逐条改接线**(期望侧全部来自 `resolve_color`,消费者侧不变):
    - `[p1] .hint color` → `resolve_color(page, "--color-text-muted")`
    - `[p1] #ai-route-select border-top-color` → `resolve_color(page, "--color-border-strong")`
    - `[p1] #selection-menu border-top-color` → `resolve_color(page, "--color-border-strong")`
    - `[p1] #stream-banner border-top-color` → `resolve_color(page, "--color-action-warning")`
    - `[p1] .kind-write .event-kind background` → `resolve_color(page, "--color-kind-write")`
    - `[p1] .kind-done .event-kind background` → `resolve_color(page, "--color-kind-done")`
    - `[p1] .chat-user background` → `resolve_color(page, "--color-surface-user")`
    - `[p3] #btn-authorize color` 与 `border-color` → `resolve_color(page, "--color-action-irreversible")`
    - `[p3] #btn-authorize background-color` → `resolve_color(page, "--color-action-irreversible-surface")`
    - `[p3] #state-badge color` → `resolve_color(page, "--color-text-info")`
    - `[p3] #state-badge background-color` → `resolve_color(page, "--color-surface-info")`
    - `[p3] .badge-answered color` → `resolve_color(page, "--color-text-muted")`
    - `[p3] #btn-process-round 与 #btn-authorize 三属性逐字节相同` 这条 `ok_true` **逻辑不动**(它比较两个消费者的 computed 值,与值层无关),但把 `expected`/`actual` 参数保留原样。
    - `.overlay-card box-shadow 含 rgba(0,0,0,0.2)` 这条 `ok_contains` 的 needle **保持字面** `rgba(0, 0, 0, 0.2)`:box-shadow 不是颜色令牌,该 needle 由 R-2 的令牌形状固定(与 `idi-04.1-01-PLAN.md` Task 3 在 `item_smoke` 里的写法一致)。在紧邻处加一行注释说明为什么它是本文件里唯一保留的颜色字面。

    **3. 每条接线断言旁加一条 `info()`**,把运行时解析出的令牌值打印出来,标签用中文且写明令牌名(照 `item_smoke` 的 `info("smoke 令牌解析", ...)` 写法)。这些 `info()` 是 D-14 已接受的检测力损失的补偿:值错了在这里看得见,而值的**仲裁者**是 `check-02-contrast.py`。本任务至少要让下列五条出现在日志里:`--color-text-muted`、`--color-border-strong`、`--color-action-warning`、`--color-kind-done`、`--color-surface-user`。

    **4. `item3` 的构造说明 `info()`(L588-L590)保留原样** —— 它解释的是探针节点如何被应用自身的 `renderEvent` / `appendChatMessage` 渲染,与值层无关。

    **不得改动本任务范围之外的任何东西**:`item1`、`item4`、`item5`、`item6`、`item_smoke`、`main()`、`parse_args`、`normalize_items`、以及 `resolve_color` / `read_style` / `effective_bg` / `ok` 系辅助一律逐字不动。
  </action>
  <verify>
    <automated>awk '/^def check_frozen_marker/,/^def item2/' scripts/check-05-ui-uat.py | grep -c 'rgb(' ; awk '/^def item3\(/,/^def item4\(/' scripts/check-05-ui-uat.py | grep -c '"rgb('</automated>
    <fails_when>第一个计数不为 0(`check_frozen_marker` 里仍有硬编码颜色),或第二个计数不为 0(`item3` 的期望侧仍有字面 `rgb(`)</fails_when>
    <automated>grep -c 'FROZEN_AMBER' scripts/check-05-ui-uat.py</automated>
    <fails_when>计数不为 0(常量或它的使用未删净)</fails_when>
    <automated>awk '/^def item3\(/,/^def item4\(/' scripts/check-05-ui-uat.py | grep -c 'resolve_color'</automated>
    <fails_when>计数少于 11(`item3` 的接线断言未铺开:15 条断言里除三属性对比与 box-shadow 两条外,期望侧都应来自 `resolve_color`)</fails_when>
    <automated>grep -c 'rgba(0, 0, 0, 0.2)' scripts/check-05-ui-uat.py</automated>
    <fails_when>计数不等于 1(box-shadow 的 needle 是本文件唯一允许保留的颜色字面,多一处就是漏改)</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 2,3</automated>
    <fails_when>退出码不为 0,或输出中出现 `FAIL`,或 `item 2` / `item 3` 的结论不是 `PASS`</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 2,3 2>&1 | grep -E 'item (2|3):'</automated>
    <fails_when>输出的两行里出现 `BLOCKED`(元素缺失或令牌解析失败必须显式暴露,不得静默)</fails_when>
    <automated>git diff --name-only HEAD</automated>
    <fails_when>输出的文件清单超出 `scripts/check-05-ui-uat.py` 与 `.planning/phases/idi-04-tokens-contract/idi-04-UAT.md`</fails_when>
  </verify>
  <acceptance_criteria>
    - `grep -c 'FROZEN_AMBER' scripts/check-05-ui-uat.py` == 0,且 `check_frozen_marker` 的期望色来自 `resolve_color(page, "--color-action-warning")`
    - `item3` 函数体内不含任何字面 `"rgb(` 期望值;含 ≥11 处 `resolve_color`
    - 全文件里 `rgba(0, 0, 0, 0.2)` 恰出现 1 次(唯一的颜色字面,且带解释注释)
    - `.venv/bin/python scripts/check-05-ui-uat.py --item 2,3` 退出码 0,`item 2` 与 `item 3` 均为 `PASS`(0 FAIL / 0 BLOCKED)
    - 日志中含五条以上令牌解析 `info()`(`--color-text-muted` / `--color-border-strong` / `--color-action-warning` / `--color-kind-done` / `--color-surface-user` 各至少一条)
    - `item1` / `item4` / `item5` / `item6` / `item_smoke` / `main()` / `parse_args` / `normalize_items` 的函数体逐字未变
    - 冻结轮的 `opacity` == `"1"` 与 `filter` == `"saturate(0.6)"` 两条断言仍以字面值断言并通过
  </acceptance_criteria>
  <done>`item2` 与 `item3` 的期望侧全部改为运行时令牌解析,`FROZEN_AMBER` 删除,唯一保留的颜色字面是 box-shadow 的 needle;两项在真实浏览器里 `PASS`,令牌解析值逐条 `info()` 留痕。</done>
</task>

<task type="auto">
  <name>Task 2: `item4` 与 `item5` 改令牌接线 + D-13 选择器改名 + D-12 期望值更新</name>
  <files>scripts/check-05-ui-uat.py</files>
  <read_first>
    - `scripts/check-05-ui-uat.py` L632-L722 —— `item4` 全文(含 L643-L653 的 `#doc-pane` `blocked` 块、L669-L688 的字号断言、L690-L692 的 z-index 三条、L703-L708 的归档态与 button color、L710-L721 的 S-2 依赖断言)
    - `scripts/check-05-ui-uat.py` L724-L770 —— `item5` 全文(L733-L747 的五条颜色断言与 `.markdown-body color`、L748-L759 的层级断言)
    - `scripts/check-05-ui-uat.py` L250-L262 —— `resolve_color`;以及 `idi-04.1-01-PLAN.md` Task 3 新增的 `resolve_token(page, name)`(读 `getComputedStyle(document.documentElement).getPropertyValue(name)`)
    - `.planning/phases/idi-04-tokens-contract/idi-04-UAT.md` 第 4 项的 evidence —— D-12 要接受的 **HEAD 实测值**逐条来源(`.panel-header` padding-top 6px / padding-left 10px、`#brainstorm-view h2` 16px、`#draft-view h2` 18px、`.overlay-card h3` 24px、`.markdown-body` 16px、`.markdown-body code` 14px)
    - `.planning/phases/idi-04-tokens-contract/idi-04-UAT.md` 第 4 项的 blocked 条目与第 5 项的 failing 列表 —— D-13 与 D-12 的原文依据
    - `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` `## Carry-Forward Obligations` 第 5 / 6 / 9 条;`## Value-Layer Delta Ledger` 的 C-1 行
    - `.planning/phases/idi-04.1-radix/idi-04.1-CONTEXT.md` D-12 / D-13 / D-14
  </read_first>
  <action>
    **1. D-13 —— `#doc-pane` 的期望字符串改为 `#doc-panel-body`。** 把 L644-L653 的 `blocked(...)` 块换成一条正常的 `ok()`:选择器 `#doc-panel-body`,属性 `padding`,期望 `32px 40px`。**这不是 id 改名** —— `frontend/index.html` 里本来就没有 `#doc-pane`,`app.js` 的 id 一字不动;改的是 UAT 的期望字符串。保留一句注释说明原期望串写错了名字(实测 `#doc-panel-body` 的 padding 一直是 32px/40px,与期望值一致,只是名对不上)。

    **2. D-12 —— 7 条间距/字号漂移更新期望值接受 HEAD 现状**(`frontend/style.css` 一字不动):
    - `.panel-header` `padding-top` → `6px`;`padding-left` → `10px`
    - `#brainstorm-view h2` `font-size` → `16px`
    - `#draft-view h2` `font-size` → `18px`
    - `.overlay-card h3` `font-size` → `24px`
    - `.markdown-body`(探针 `#draft-content`)`font-size` → `16px`
    - `.markdown-body code` `font-size` → `14px`
    - 在每一条旁边加一句注释说明「D-12:该值在 HEAD 上是刻度内的合法档(`6px` = `--space-1-5`、`10px` = `--space-2-5`),04.1 明令不改 S-1/S-2,故更新期望值而非改 CSS」。

    **3. `item4` 的颜色断言改接线:**
    - `#brainstorm-view h2 color` → `resolve_color(page, "--color-action-warning")`
    - `[archive] button color(通用规则,探针 #btn-enter)` → `resolve_color(page, "--color-text")`

    **4. `item4` 的三条 z-index 断言改走 `resolve_token`(值层无关,但属于同一根因的结构性修复):**
    - `#selection-menu z-index` → 期望侧 `resolve_token(page, "--z-selection-menu")`
    - `#state-badge z-index` → 期望侧 `resolve_token(page, "--z-badge")`
    - `#stream-banner z-index` → 期望侧 `resolve_token(page, "--z-banner")`
    - 这三条同时是 TOKEN-07 在**渲染层**的证据:`--z-badge` 由 R-1 恢复消费者后不再空转,`badge < banner` 的承重序关系两端都在真实 DOM 上被读到。加一句注释点明这一点。
    - `--z-*` 的令牌值本身(`10` / `20` / `100` / `200`)仍由围栏注释与 `frontend/style.css` 固定;若三者解析失败,`ok()` 会转 `BLOCKED`,不得记为 pass。

    **5. `item5` 的五条颜色断言改接线:**
    - `#ai-route-select border-top-color` → `resolve_color(page, "--color-border-strong")`
    - `#ai-route-select background-color` → `resolve_color(page, "--color-surface")`
    - `.hint color` → `resolve_color(page, "--color-text-muted")`
    - `.hint 实际背景` → `resolve_color(page, "--color-surface")`(该值由 `effective_bg` 沿祖先链取到。**实测**:`document.querySelector('.hint')` 命中的是 `frontend/index.html:98` 那条,它位于 `#doc-panel-body`(`index.html:92`)→ `#doc-panel`(`index.html:82`)内,而 `frontend/style.css:267` 是 `#doc-panel { background: var(--color-surface); }` —— 故该元素解析到的底色是 `--color-surface`,**不是** `--color-surface-page`。两者在 Plan 01 之后是 `#f9f9f9` 与 `#fcfcfc`,接错线会让这条断言永远失败)
    - `#stream-banner border-top-color` → `resolve_color(page, "--color-action-warning")`
    - `.markdown-body color` → `resolve_color(page, "--color-text")`

    **6. `item5` 的层级断言(`.markdown-body` 亮度显著低于 `.hint`)逻辑不动。** 它比较两个消费者的相对亮度,与值层无关;只把它的注释里那句「ORDER 0.311 的可观察形态」更新为「ORDER 0.363 的可观察形态」(UI-SPEC 04.1-N-1 记录该比值由 0.311 放宽到 0.363,是刻度强制的,不是判断失误)。若该断言失败,那是真缺陷,不得放宽。

    **7. `item4` 的 S-2 依赖断言(L710-L721)保持原样** —— `--text-base` == `14px` 是用户签核的一级字号档,Phase 5 SC5 / Phase 6 SC5 的下游门依赖它,本阶段不动它。

    **8. 与 `item_smoke` 的分工:** 不重复 `idi-04.1-01-PLAN.md` Task 3 已在 `item_smoke` 里加的三条断言(`#state-badge` z-index、`.overlay-card` box-shadow、`.tier-desc` opacity)。`item4` 里原有的 `#state-badge z-index` 断言是本任务要改的**另一处**(它在 `item4`,不在 `smoke`),两者共存不冲突。

    **不得改动本任务范围之外的任何东西**:`item1`、`item2`、`item3`、`item6`、`item_smoke`、`main()`、`parse_args`、`normalize_items` 与全部辅助函数逐字不动。
  </action>
  <verify>
    <automated>awk '/^def item4\(/,/^def item5\(/' scripts/check-05-ui-uat.py | grep -c '"rgb(' ; awk '/^def item5\(/,/^def item6\(/' scripts/check-05-ui-uat.py | grep -c '"rgb('</automated>
    <fails_when>任一计数不为 0(`item4` / `item5` 的期望侧仍有字面 `rgb(`)</fails_when>
    <automated>awk '/^def item4\(/,/^def item5\(/' scripts/check-05-ui-uat.py | grep -c 'resolve_token'; awk '/^def item4\(/,/^def item5\(/' scripts/check-05-ui-uat.py | grep -c 'resolve_color'</automated>
    <fails_when>第一个计数少于 3(z-index 三条未走 `resolve_token`),或第二个计数少于 2(`item4` 的两条颜色断言未接线)</fails_when>
    <automated>awk '/^def item5\(/,/^def item6\(/' scripts/check-05-ui-uat.py | grep -c 'resolve_color'</automated>
    <fails_when>计数少于 6(`item5` 的六条颜色断言未全部接线)</fails_when>
    <automated>grep -c 'doc-pane' scripts/check-05-ui-uat.py; grep -c 'doc-panel-body' scripts/check-05-ui-uat.py</automated>
    <fails_when>第一个计数不为 0(D-13 未改净),或第二个计数少于 1</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 4,5</automated>
    <fails_when>退出码不为 0,或输出中出现 `FAIL`,或 `item 4` / `item 5` 的结论不是 `PASS`</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 4,5 2>&1 | grep -E 'item (4|5):'</automated>
    <fails_when>输出的两行里出现 `BLOCKED`(D-13 的 `#doc-pane` 项必须由 BLOCKED 转为 PASS,不得残留任何阻塞项)</fails_when>
    <automated>git diff --name-only HEAD</automated>
    <fails_when>输出的文件清单超出 `scripts/check-05-ui-uat.py` 与 `.planning/phases/idi-04-tokens-contract/idi-04-UAT.md`</fails_when>
  </verify>
  <acceptance_criteria>
    - `item4` 与 `item5` 函数体内不含任何字面 `"rgb(` 期望值
    - `item4` 含 ≥3 处 `resolve_token`(三条 z-index)与 ≥2 处 `resolve_color`(`#brainstorm-view h2` color、button color)
    - `item5` 含 ≥6 处 `resolve_color`(border-top-color、background-color、`.hint` color、`.hint` 背景、`#stream-banner` border、`.markdown-body` color)
    - `grep -c 'doc-pane' scripts/check-05-ui-uat.py` == 0 且 `grep -c 'doc-panel-body'` ≥ 1;`item4` 中该条断言为 `ok` 且期望 `32px 40px`
    - D-12 的六条期望值逐条落位:`.panel-header` 6px / 10px、`#brainstorm-view h2` 16px、`#draft-view h2` 18px、`.overlay-card h3` 24px、`#draft-content` 16px、`#draft-content code` 14px
    - `.venv/bin/python scripts/check-05-ui-uat.py --item 4,5` 退出码 0,两项均 `PASS`(0 FAIL / 0 BLOCKED)
    - `--text-base` == `14px` 的 S-2 依赖断言仍在且 PASS
    - `item1` / `item2` / `item3` / `item6` / `item_smoke` / `main()` 与全部辅助函数逐字未变
  </acceptance_criteria>
  <done>`item4` 与 `item5` 的期望侧全部改为令牌接线,z-index 三条走 `resolve_token`,`#doc-pane` → `#doc-panel-body` 由 BLOCKED 转 PASS,D-12 的六条期望值更新;两项在真实浏览器里 `PASS`。</done>
</task>

<task type="auto">
  <name>Task 3: `idi-04-UAT.md` 按 D-10 / D-12 / D-13 更新 + C-1 下游门复核 + 全量门禁收口</name>
  <files>.planning/phases/idi-04-tokens-contract/idi-04-UAT.md</files>
  <read_first>
    - `.planning/phases/idi-04-tokens-contract/idi-04-UAT.md` 全文 —— `## Current Test`、`## Tests` 的 6 项 `expected:` / `result:` / `evidence:`、`## Summary` 计数、`## Gaps` 的 YAML 块(含三条 gap 与末尾那段「另记」的 AA 倒退)
    - `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` `## Carry-Forward Obligations` 第 6 / 7 / 8 条 —— UAT 期望值更新、C-1 的字号复核、Phase 7 焦点环的重测义务
    - `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` `### What this phase fixes that Phase 4 could not` —— 3 条 FAIL + AA 倒退被本阶段吸收的逐条对照表
    - `.planning/ROADMAP.md` §Phase 5 `**Success Criteria**` 与 §Phase 6 `**Success Criteria**` —— C-1 要复核的**下游门引用**原文(Phase 6 SC5 写 `#brainstorm-view h2` 仍计算为 `14px` / `#8a6508`)
    - `frontend/style.css` `#brainstorm-view h2` 规则(约 L558-L562)—— 它的 `font-size: var(--text-md)` 与 `color: var(--color-action-warning)`
    - `frontend/style.css` 围栏内的 `--text-md: 16px` 与 `--radix-amber-12: #4f3422`
    - `.planning/phases/idi-04.1-radix/idi-04.1-CONTEXT.md` D-10 / D-12 / D-13
  </read_first>
  <action>
    **1. 更新 `## Tests` 的期望值与结果。** 三项 FAIL(第 3 / 4 / 5 项)按 D-10 / D-12 / D-13 重述:
    - **D-10(颜色漂移,随值层重写消解)**:第 3 项的 7 条失败中属于颜色值的那些(`.hint` color、`.badge-answered` color、`#state-badge` color、`.chat-user` background、`#ai-route-select` / `#selection-menu` border-top-color)与第 5 项的四条失败,期望值改为**令牌接线表述**(「消费者 computed 值 == 运行时解析出的 `--<token>`」),并在 evidence 里写明:重写后的实测值由 `scripts/check-05-ui-uat.py` 逐条给出,值本身的仲裁者是 `scripts/check-02-contrast.py`。
    - **D-11(两条声明恢复)**:`.overlay-card box-shadow` 与 `#state-badge z-index` 两条失败改为「R-1 / R-2 恢复后 PASS」,并写明 `#state-badge` 的 z-index 恢复是**正确性**修复(否则 `--z-badge` 无消费者、围栏断言的 `badge < banner` 序关系空转)。
    - **D-12(间距/字号漂移,更新期望值接受 HEAD)**:第 4 项的 7 条间距/字号失败改为 HEAD 实测值(`.panel-header` `6px` / `10px`、`#brainstorm-view h2` 16px、`#draft-view h2` 18px、`.overlay-card h3` 24px、`.markdown-body` 16px、`.markdown-body code` 14px、`button` color 走 `--color-text`),并写明理由(04.1 明令不改 S-1/S-2;`6px` = `--space-1-5`、`10px` = `--space-2-5` 都是刻度内合法档)。
    - **D-13**:第 4 项的 BLOCKED 条目 `#doc-pane` 改为 `#doc-panel-body`,并写明「改的是期望字符串,不是 id —— 硬规则 5 的约 70 个 `getElementById` id 一字未动」。
    - 每项的 `result:` 更新为 `pass`,并在 `evidence:` 里写入**本阶段实跑的输出**(逐项断言数、FAIL / BLOCKED 计数、退出码),不要写「预计通过」这类无证据的表述。

    **2. 重写 `## Gaps` 块。** 三条 gap 逐条标为**已消解**,每条写一句消解口径(颜色类随值层重写消解 / 间距字号类更新期望值 / `#doc-pane` 改名),并保留原 gap 的 `observed` 与 `failing` 作为历史对照(不要删掉原始证据 —— 它是「假 FAIL 的根因」这条教训的载体)。末尾那段「另记:`--color-text-muted` = `#8f8f8f` 在 `#ffffff` 上 3.23:1 的 AA 倒退」改写为**已修复**:新值 `--radix-gray-11` `#646464` 在 `--color-surface` `#f9f9f9` 上 **5.62:1**(由 `check-02-contrast.py` 实测)。更新 `## Summary` 的 `passed` / `issues` 计数与 `updated` 时间戳。

    **3. C-1 的下游门引用复核(携带项 #7)—— 必须实测,不得照抄。** 用真实浏览器读 `#brainstorm-view h2` 的 computed `font-size` 与 `color`(可以直接用刚改好的 `.venv/bin/python scripts/check-05-ui-uat.py --item 4` 的输出,它已断言这两条),并对照**全部**下游引用点(同一句 `#brainstorm-view h2` = `14px` / `#8a6508` 的说法在 ROADMAP 里出现多次,复核时逐点列全,不要只点其中一处):
    - `.planning/ROADMAP.md:197` §Phase 6 SC5 写「`#brainstorm-view h2` 仍计算为 **14px** / **`#8a6508`**」。
    - `.planning/ROADMAP.md:37`(硬规则「追加,不重排」)写「后者胜出 → 14px / `#8a6508`」。
    - `.planning/ROADMAP.md:166`(Pitfall 9)写「`#brainstorm-view h2` 的 14px / `#8a6508` 是顺序决定的」。
    - `.planning/ROADMAP.md:169` §Phase 5 Gates 写「`#brainstorm-view h2` 仍计算为 14px / `#8a6508`」。
    - `.planning/ROADMAP.md:209` §Phase 7/8 Gates 写「`#brainstorm-view h2` 仍 14px / `#8a6508`」。
    - `04-UI-SPEC.md` 的携带项 #7(§Q3)写「`#brainstorm-view h2` = 14px is confirmed alive at HEAD」。
    - 静态事实:`frontend/style.css` 的 `#brainstorm-view h2` 用的是 `font-size: var(--text-md)`,而围栏内 `--text-md: 16px`;它的颜色是 `var(--color-action-warning)`,本阶段后等于 `--radix-amber-12` = `#4f3422`。
    - 把实测值、上述六个引用点的原文(逐点写出行号)、以及「这些引用在本阶段之后失真」的结论写进 `## Gaps` 块之后的 `## Carry-Forward`(若该节不存在则新建一节)。**同时明确写下:本阶段不单方面改写 `ROADMAP.md` §Phase 6 SC5 的验收判据** —— 那是未来阶段已签核的门,改它属于范围外,须由用户裁决。给出一行式修正建议(`14px` → 实测值;`#8a6508` → `#4f3422`)供用户直接采纳。

    **4. 记录携带项 #8(不执行)。** 在 `## Carry-Forward` 里记一条:Phase 7 的焦点环 `--color-focus: #1f63bd` 必须在 Phase 7 自己的门里对**新的**地面重新测 ≥3:1(`--color-surface` `#f9f9f9`、`--color-surface-page` `#fcfcfc`);本阶段不改环色,只改它落的地面。

    **5. 不要在本文件里写实现细节。** 它是 UAT 记录,不是计划;不复制 `idi-04.1-UI-SPEC.md` 的表格(那会造出第二份事实源 —— 正是本阶段要消除的东西)。引用一律写路径与节名。
  </action>
  <verify>
    <automated>grep -c 'doc-pane' .planning/phases/idi-04-tokens-contract/idi-04-UAT.md; grep -c 'doc-panel-body' .planning/phases/idi-04-tokens-contract/idi-04-UAT.md</automated>
    <fails_when>第一个计数不为 0(D-13 未改净),或第二个计数少于 1</fails_when>
    <automated>grep -c 'result: \[pass\]' .planning/phases/idi-04-tokens-contract/idi-04-UAT.md; grep -c 'result: \[fail\]' .planning/phases/idi-04-tokens-contract/idi-04-UAT.md</automated>
    <fails_when>第一个计数不为 6,或第二个计数不为 0(三项 FAIL 未全部转为 pass)</fails_when>
    <automated>grep -c '8a6508' .planning/phases/idi-04-tokens-contract/idi-04-UAT.md; grep -c '4f3422' .planning/phases/idi-04-tokens-contract/idi-04-UAT.md; grep -c 'Carry-Forward' .planning/phases/idi-04-tokens-contract/idi-04-UAT.md</automated>
    <fails_when>`8a6508` 计数为 0(失真的下游引用原文未留证),或 `4f3422` 计数为 0(新值未记录),或 `Carry-Forward` 计数为 0(C-1 / 携带项 #8 的义务未落纸)</fails_when>
    <automated>grep -c '14px' .planning/phases/idi-04-tokens-contract/idi-04-UAT.md</automated>
    <fails_when>计数为 0(C-1 的 14px/16px 复核结论未写入)</fails_when>
    <automated>grep -n 'Phase 6 SC5\|Phase 5 SC5' .planning/phases/idi-04-tokens-contract/idi-04-UAT.md | head -5</automated>
    <fails_when>无输出(C-1 复核未点名下游门)</fails_when>
    <automated>grep -cE 'ROADMAP\.md:(37|166|169|197|209)' .planning/phases/idi-04-tokens-contract/idi-04-UAT.md</automated>
    <fails_when>计数少于 5(C-1 的引用点枚举不完整 —— 同一句 `14px` / `#8a6508` 在 ROADMAP 里出现于 L37 / L166 / L169 / L197 / L209 五处,复核须逐点列出,不得只点其中一处)</fails_when>
    <automated>git status --porcelain -- .planning/ROADMAP.md frontend/style.css frontend/app.js frontend/index.html frontend/vendor/</automated>
    <fails_when>输出非空(ROADMAP 或任何 frontend/ 源文件被改动 —— 本任务只允许改 idi-04-UAT.md)</fails_when>
  </verify>
  <acceptance_criteria>
    - `grep -c 'doc-pane'` == 0 且 `grep -c 'doc-panel-body'` ≥ 1(D-13 落纸)
    - `## Tests` 的六项 `result:` 全部为 `[pass]`,无 `[fail]`;每项 evidence 写入本阶段实跑的断言数与退出码
    - `## Gaps` 的三条 gap 逐条标为已消解,原始 `observed` / `failing` 保留为历史对照;末尾的 AA 倒退段改为已修复并给出新值 `#646464` / 5.62:1
    - `## Summary` 的 `passed` / `issues` 计数与时间戳更新为 6 / 0
    - 新增 `## Carry-Forward` 一节,含三条:①C-1 的 `#brainstorm-view h2` 实测(16px / `#4f3422`)与**五个 ROADMAP 引用点**的原文(`ROADMAP.md:37` 硬规则、`:166` Pitfall 9、`:169` §Phase 5 Gates、`:197` §Phase 6 SC5、`:209` §Phase 7/8 Gates 各自的 `14px` / `#8a6508`)+ `04-UI-SPEC.md` 携带项 #7 的 14px + 一行式修正建议 + 「本阶段不改写未来阶段验收判据」的说明;②携带项 #8 的 Phase 7 焦点环重测义务;③D-15 的三数差异(24 / 34 / 43)留档
    - `.planning/ROADMAP.md`、`frontend/style.css`、`frontend/app.js`、`frontend/index.html`、`frontend/vendor/` 在本任务中零改动
    - 本文件不复制 `idi-04.1-UI-SPEC.md` 的任何表格,引用一律写路径与节名
  </acceptance_criteria>
  <done>`idi-04-UAT.md` 的六项全部 `pass`、三条 gap 标为已消解、AA 倒退记为已修复;C-1 的下游门失真引用被实测确认并留证,连同携带项 #8 与 D-15 的三数差异一起写入 `## Carry-Forward`;ROADMAP 与全部 frontend/ 源文件零改动。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 本地应用 → Playwright harness | harness 启动本地 uvicorn 并用浏览器进入 `scripts/ui-states/` 的磁盘状态样本;样本每次复制到临时目录,仓库样本只读 |
| harness → 仓库工作树 | 断言脚本**只读**:它不写 `frontend/`、不写 `scripts/`;唯一写入的是 `mktemp` 临时工作目录(默认跑完删除) |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi041-09 | Repudiation | 「运行时验证」被断言而非执行 | high | mitigate | 携带项 #9 的九组具名检查逐条落到 `item_smoke`(01 的三条)与 `item3` / `item4` / `item5`(本计划的六组),每一条都配可运行的 `<automated>` 命令与 `<fails_when>`;`.venv/bin/python scripts/check-05-ui-uat.py` 全量退出码必须是 0,且 `grep -c 'var(--'` 这类静态计数被明确拒绝作为证据。**这是本计划唯一的高危项,因为「验证没做却写成做了」是本阶段最容易发生的失败** |
| T-idi041-10 | Repudiation | 令牌接线断言掩盖「值本身错了」 | medium | mitigate | D-14 已接受该检测力损失(它换掉了「硬编码值能抓令牌接错线」的能力),本计划用两条措施补偿:①每条接线断言旁的 `info()` 打印运行时解析值,值错时在日志里看得见;②值的仲裁者是 `check-02-contrast.py` 的 43 对实测比值,不由 harness 承担。二者合起来覆盖「接线」与「值」两个轴 |
| T-idi041-11 | Tampering | 为让断言通过而改 `frontend/style.css` | medium | mitigate | 本计划的 `files_modified` 不含 `frontend/style.css`;verify 以 `git status --porcelain -- frontend/style.css frontend/app.js frontend/index.html frontend/vendor/` 断言输出为空,并以 `git diff --name-only HEAD` 断言改动面只有两个计划文件 |
| T-idi041-12 | Spoofing | 用无头系统 Chrome 或静态分析冒充真实渲染 | low | mitigate | `.venv` 的 Python 是 x86_64,系统 Chrome 走 Rosetta,`channel='chrome'` + headless 在本机会挂死(CDP 180s 连不上);harness 的正确路线是默认的捆绑 chromium-1243 无头(arm64 原生、零下载)。verify 命令一律不传 `--browser`,并在 prohibitions 里禁止换路线 |
| T-idi041-13 | Information disclosure | harness 读取的内容 | none | accept | 只读本地磁盘状态样本与本地应用的 computed style,不含凭据、不外联 |
| T-idi041-SC | Tampering | npm / pip / cargo 安装 | none | accept | **本阶段不安装任何包。** Playwright 1.63.0 已在 `.venv` 中就位且**不得跑 `playwright install`**(捆绑 chromium-1243 已在本机缓存);硬规则 6 要求零新增依赖 |

**诚实结论:本计划唯一的高危项是 T-idi041-09 —— 它不是外部攻击面,而是「验证被声称而非被执行」这一内部完整性风险。** 本阶段没有网络面、没有输入解析、没有新依赖、没有新文件,不存在外部可利用的 high / critical 威胁。
</threat_model>

<verification>
- `.venv/bin/python scripts/check-05-ui-uat.py` 全量(默认 item 1..6 + 不跑 smoke 之外的额外项)→ 退出码 0,`item 1..6` 全部 `PASS`
- `.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,6` → 退出码 0(含 01 的三条令牌接线断言)
- `python3 scripts/check-02-contrast.py` → 末行 `PASS: 0 failures`,43 条配对 + `ORDER 0.363`
- `bash scripts/check-01-token-conformance.sh` / `check-03-hidden-uniqueness.sh` / `check-04-important-count.sh` → 各自 `PASS`
- `node --check frontend/app.js` 与 `.venv/bin/python -m pytest -q`(基线 225 collected / 219 passed / 6 skipped)不变
- `git status --porcelain -- frontend/app.js frontend/index.html frontend/vendor/` 输出为空;`test "$(ls frontend/vendor/)" = "marked.min.js"`
- `git diff --name-only HEAD` 只列出 `scripts/check-05-ui-uat.py` 与 `.planning/phases/idi-04-tokens-contract/idi-04-UAT.md`
- 断言脚本里除 `.overlay-card` box-shadow 的 needle 外,无其它硬编码颜色期望值
</verification>

<success_criteria>
1. 携带项 #9 的九组具名运行时检查全部有断言、有可运行命令、有真实浏览器证据
2. `scripts/check-05-ui-uat.py` 的颜色断言全部改为令牌接线形式,`FROZEN_AMBER` 删除,`#doc-pane` → `#doc-panel-body`
3. `idi-04-UAT.md` 六项全 `pass`,三条 gap 标为已消解,AA 倒退记为已修复
4. C-1 的两处下游门失真引用被实测确认并留证(不在本阶段单方面改写 ROADMAP §Phase 6 SC5)
5. 全量 harness + 四条守卫 + `check-02` + pytest 基线 + 零 diff 门全部通过
6. `frontend/app.js` / `frontend/index.html` / `frontend/vendor/` 零改动
</success_criteria>

<artifacts_this_phase_produces>
**本计划新建的符号:**

- 无新增源文件、无新增函数、无新增依赖
- 新增/改写的**断言标签字符串**(中文,含令牌名)与 `info()` 记录键,例如 `"[p1] .hint color == var(--color-text-muted)"` 形态的标签;这些标签字符串是本阶段新造的标识符,不应被 source-grounding 当作漂移
- 新增对 `resolve_token(page, name)`(由 `idi-04.1-01-PLAN.md` Task 3 创建)的三处调用(`--z-selection-menu` / `--z-badge` / `--z-banner`)
- `.planning/phases/idi-04-tokens-contract/idi-04-UAT.md` 新增 `## Carry-Forward` 一节

**删除的符号:**

- `scripts/check-05-ui-uat.py` 的模块常量 `FROZEN_AMBER` 及其三处使用
- `#doc-pane` 这一**期望选择器字符串**(不是 id;`frontend/index.html` 里从来没有这个 id)
</artifacts_this_phase_produces>

<output>
Create `.planning/phases/idi-04.1-radix/idi-04.1-03-SUMMARY.md` when done
</output>
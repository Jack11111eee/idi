---
phase: idi-05-typography-and-visual-hierarchy
plan: 04
type: execute
wave: 4
depends_on:
  - idi-05-01
  - idi-05-02
  - idi-05-03
files_modified:
  - frontend/style.css
  - scripts/check-05-ui-uat.py
  - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md
autonomous: true
gap_closure: true
gap_ids: [G-idi-05-1]
requirements:
  - TYPE-01
  - TYPE-03
  - VISUAL-03

estimate:
  tokens: 40000
  raw_tokens: 40000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "`renderMarkdown()` 的**全部九个**注入目标上,h1/h2/h3 都解析为契约内的字号档与 `--fw-semibold`(600):四个 `.markdown-body` 宿主仍是 28 / 22 / 18,五个非 `.markdown-body` 目标改为 24 / 18 / 16。**任何目标都不再出现 UA 默认值**(`.chat-bubble` 上下文里的 32px、`.event-content` 上下文里的 28px),也不再有第四个字号档以外的**第四个字重档 700** ← G-idi-05-1 的 `missing` 第 1 项 / TYPE-01 / TYPE-03"
    - "文档 h1(28px)在**任何**状态下都**严格大于**五个嵌入目标里的 h1(24px):「全屏最大最重的文字是文档自己的 h1」在 AI 吐出发散标题时仍然成立 ← SC3 / VISUAL-03 / E2。这不是措辞选择:check-06 的 g2 用的是**严格不等式**(`doc_h1 > worst`),把嵌入 h1 定成 28px 会让 g2 在会话流里有标题时直接失败"
    - "嵌入刻度的取值由一条**可复算的规则**给出,不是逐容器手调:每个嵌入档 = 它在文档刻度里的对应档**沿契约自己的数值阶梯下移一档**。契约阶梯的数值序为 12 / 14 / 16 / 18 / 22 / 24 / 28,故 `--text-3xl`(28)→ `--text-xl`(24)、`--text-2xl`(22)→ `--text-lg`(18)、`--text-lg`(18)→ `--text-md`(16) ← 本计划定稿(见 `<objective>` 的取值推导与两个被否决的候选)"
    - "check-05 的渲染目标枚举**按 `renderMarkdown()` 的调用点**而非按类名,并且有静态普查守卫:`frontend/app.js` 的 `renderMarkdown(` 出现次数一变,门立刻 FAIL 并指明要更新枚举。**只枚举 `.markdown-body` 的四个宿主正是本缺陷存活到验证后的直接原因**(与本阶段 plan 01 已登记的教训同型)← G-idi-05-1 的 `missing` 第 2 项"
    - "五个嵌入目标在门里是**造出来再断言**的:用应用自身的渲染函数(`renderEvent` / `appendChatMessage` / `appendSayToChat` / `renderAnnotations`)把带 h1/h2/h3 的 markdown 注入进去再读 computed style;容器造不出时记 **BLOCKED**,绝不记 PASS(与 check-06 的 g4 / g5 同约定)。**不得**靠「fixture 里本来就没有 `.chat-bubble`」而空过 ← G-idi-05-1 的 `missing` 第 2 项 / check-05 的 `ok()` 语义"
    - "UI-SPEC 的 Deliberate Delta Ledger 补齐 **P-19**(chrome 标题选择器由后代形态收窄为子组合器 / id 形态)与 **P-20**(五个渲染目标的嵌入刻度),`:805` 的零列表同步除外;契约的 `## 契约修正登记` 增 **A-9**:硬规则 9 与 REQUIREMENTS 的 TYPE-01 里「作用域限定在 `.markdown-body` 内」这一句按 G-idi-05-1 收窄为「不得写全局 `h1, h2, h3` 规则;渲染目标必须在 style.css 侧逐个列举」← G-idi-05-1 的 `missing` 第 3 项"
    - "四条不变量全绿:`^\\.hidden {` == 1、`!important;` 声明数 == 1、`@media` 计数 == 0、围栏外零裸 hex;`frontend/app.js` / `index.html` / `frontend/vendor/` 零 diff;零新增令牌、零新增依赖、零新增文件 ← 硬规则 1 / 2 / 6 / 8 / 9 与 Do-Not-Touch 清单"
    - "`idi-04.1-radix` 的连带义务再次履行(D-05):四条守卫 + 三处结论在 HEAD 上重算通过,`ORDER 0.363`、`--color-text-info ON --color-surface-info` 4.53、`--color-border-strong` 3.24 / 3.15、tier-1 25 / tier-2 48、清单 47 对全部逐字不变;04.1 的报告文件零改动 ← D-05 / A-8"

  artifacts:
    - path: "frontend/style.css"
      provides: "文件末尾追加 3 条嵌入刻度规则(每条 5 个选择器,对应 `.event-content` / `.chat-bubble` / `.say-chunk` / `.annotation-note` / `.annotation-answer-body`),分别声明 `font-size: var(--text-xl)` / `var(--text-lg)` / `var(--text-md)` 与 `font-weight: var(--fw-semibold)`;配一条注释写明取值规则、为什么不写全局 `h1, h2, h3` 规则、以及为什么这组规则落在文件末尾"
      contains: "font-size: var(--text-xl); font-weight: var(--fw-semibold);"
    - path: "scripts/check-05-ui-uat.py"
      provides: "把渲染目标的枚举提为单一事实源 `MARKDOWN_TARGETS`(9 条:选择器 + 注入它的 app.js 函数 + 刻度族),由它派生 `MARKDOWN_HOSTS`(4 个文档宿主)与 `RENDER_TARGETS`(5 个嵌入目标);新增 `check_render_markdown_call_sites` 静态普查守卫;新增 `item7` 逐目标断言(尺寸 / 字重 / 严格小于文档 h1)+ `item_smoke` 一条快速切片;`normalize_items` / `known` / `main` / 模块 docstring 同步登记"
      contains: "MARKDOWN_TARGETS"
    - path: ".planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md"
      provides: "Deliberate Delta Ledger 增 P-19 / P-20 并修正 `:805` 的零列表;`## 契约修正登记` 增 A-9;`## Global Hard Rules` 的第 9 条改写;§字号刻度的范围栅栏 增渲染目标影响面表(9 个目标 × 注入函数);§未在 HEAD 上受控的字号 增「五个目标曾回落 UA 默认值」的登记;Notes 增 05-N-7"
      contains: "P-20"

  key_links:
    - from: "`renderMarkdown()` 的每个调用点(`frontend/app.js`)"
      to: "`MARKDOWN_TARGETS` 的一条枚举项"
      via: "调用点普查守卫(`renderMarkdown(` 计数 == 10)—— 新增调用点即 FAIL,强制枚举跟上"
      pattern: "MARKDOWN_TARGETS = \\("
    - from: "五个嵌入容器的 `h1` / `h2` / `h3`"
      to: "`frontend/style.css` 末尾三条规则的 `font-size` / `font-weight`"
      via: "运行时逐目标断言:computed 值 == 运行时解析的令牌值(值层再改也不产生假 FAIL)"
      pattern: "\\.annotation-answer-body h1"
    - from: "check-06 的 g2 严格不等式(`doc_h1 > 全屏最大字号`)"
      to: "嵌入 h1 取 `--text-xl`(24px)而非 `--text-3xl`(28px)"
      via: "28 > 28 为假 ⇒ 嵌入 h1 必须严格小于文档 h1,这是取值规则的硬约束"
      pattern: "doc_h1 > worst"

  prohibitions:
    - statement: "**不得**改用一个全局 `h1, h2, h3` 规则来解决本缺陷。它在本例里确实「看起来能work」—— 它的特异性 0-0-1 对四处 chrome 覆盖(`.panel-header h2` / `.overlay-card h3` 为 0-1-1,`#draft-view > h2` / `#round-title` / `#brainstorm-view > h2` 为 1-0-1)与 `.markdown-body h1/h2/h3`(0-1-1)都是惰性的,于是它**只**命中恰好这五个失控容器。但:①它被 ROADMAP 的 Pitfall M4 与本契约的硬规则 9 双重禁止;②它无法表达「h1/h2/h3 三档各不相同」而不写成三条全局规则,而那会把**任何将来的标题**一并捕获 —— 正是本缺陷的成因(影响面不透明);③枚举才是可核的:门能把枚举逐条对照 `app.js` 的调用点,全局规则不能。故本计划的形态是**逐容器列举**"
      status: active
      verification: flagged
    - statement: "**不得**触碰 `.verdict-location` / `.annotation-quote` 的掩码字形与活动面板标记 —— 三者是 plan 03 的已验收交付物(`--icon-pin` / `--icon-location` / `--color-marker-active`),与本缺陷无关。本计划的 5 个选择器里**不含** `.annotation-quote` 与 `.verdict-location`"
      status: active
      verification: flagged
    - statement: "**不得**修改 `frontend/app.js` / `frontend/index.html` / `frontend/vendor/` 的任何字节(含「给五个容器加一个共享类」这条看似更干净的路)。ROADMAP 明确「只有一个阶段触碰 app.js / index.html」= Phase 8;而 UI-REVIEW 的 Pillar 1(4/4)与 Pillar 6 的「没有任何 loading / error / empty 态能回归」两条结论都以 `frontend/` 的 porcelain 为空作**结构性证明** —— 加一个类会让那两条结论同时失效,代价远大于 15 个选择器"
      status: active
      verification: flagged
    - statement: "**不得**顺手修 UI-REVIEW 的 6 条 WARNING / 4 条 INFO(60/30/10 面积核查、G3 配对的 0.22 余量、chrome 子视图标题 18/18/16 不一致、`mask-image` 的 `@supports` 回退、`#session-panel .panel-header` 的 `cursor: pointer`)。用户已裁定只修 BLOCKER;P-19 的账本条目是**唯一**的例外,因为它是本缺陷 `missing` 清单点名的必要后果"
      status: active
      verification: flagged
---

<objective>
关闭 `G-idi-05-1`(BLOCKER):`renderMarkdown()` 的返回值被注入**五个不是 `.markdown-body`** 的容器(`.event-content` / `.chat-bubble` / `.say-chunk` / `.annotation-note` / `.annotation-answer-body`),而标题尺寸规则只存在于 `.markdown-body` 作用域内(`style.css:719-721` 是全文件唯一给 h1/h2/h3 定 `font-size` 的规则)。于是这五个容器里的 `#` / `##` / `###` 全部回落到 UA 默认值 —— `.chat-bubble`(16px 上下文)里 h1 是 **32px / 700**,`.event-content`(14px 上下文)里是 **28px / 700**,都超过 `.markdown-body h2`(22px),并与文档 h1(28px)持平或反超。SC3 的「全屏最大最重的文字是文档自己的 h1」因此在任何 AI 吐出发散标题的状态下为假,同时 **700** 作为第四个字重档进入了契约只声明三档(400 / 500 / 600)的应用。

Purpose: 这不是「补一条漏掉的规则」,而是**影响面枚举错误**的第二次发作。本阶段 plan 01 已经为同一个错误付过一次代价:当时只探一个 `.markdown-body` 宿主,让 chrome 后代选择器压掉 `.markdown-body h2` 的层叠缺陷活到了执行期,修法是把探针从 1 个宿主扩到 4 个(`MARKDOWN_HOSTS`)。但那次修复只问了「四个 `.markdown-body` 宿主都探到了吗」,**没有问等价的反向问题** —— 「`renderMarkdown()` 到底注入到哪些容器?」`app.js` 里有 **10 个调用点、9 个不同目标**,而 `MARKDOWN_HOSTS` 只枚举了其中 4 个。本计划把枚举从「按类名」改成「按调用点」,并给枚举加一条会失败的普查守卫,使这个错误类型不能再以同样的形态复发。

**取值规则(本计划定稿,可复算):** 嵌入目标的每个标题档 = 它在文档刻度里的对应档,沿契约自己的数值阶梯**下移一档**。契约阶梯的数值序是 12 / 14 / 16 / 18 / 22 / 24 / 28(`--text-2xl` 22 与 `--text-xl` 24 的名字序与数值序不单调,这是 D-07 已登记的),故:

| 档 | 文档刻度(`.markdown-body`,D-06 定稿) | 嵌入刻度(本计划) | 令牌 |
|---|---|---|---|
| h1 | `--text-3xl` 28px | **24px** | `--text-xl` |
| h2 | `--text-2xl` 22px | **18px** | `--text-lg` |
| h3 | `--text-lg` 18px | **16px** | `--text-md` |

三档都落在契约**既有**的七档里(零新增令牌、零刻度外字面量);三档严格降序;最高档 24px **严格小于**文档 h1 的 28px。字重取 `--fw-semibold`(600)—— D-09 的分工里这五个容器渲染的是**内容**(AI 输出 / 用户批注),不是 chrome 标题,故归内容标题档;这也正是消除第四档 700 的方式。

**两个被否决的候选(记录理由,防止日后被"优化"回来):**
- **28 / 22 / 18(与文档刻度同档)** —— 被否决,不是审美理由:嵌入 h1 与文档 h1 同档会让 check-06 的 g2 失败。g2 断言的是**严格**不等式(`doc_h1 > 全屏最大字号`),且它扫描**可见元素**;`.chat-bubble` 与 `#draft-content` 在 `p1` 下同时可见,故 28 > 28 为假。SC3 的措辞是「文档自己的 h1 是全屏最大最重的文字」,同档即不再是「最大」。
- **22 / 18 / 16(下移两档)** —— 被否决:嵌入 h1 会与文档 h2 同档,嵌入内容的最高档与文档的**次级**标题平齐,「内容标题层级」与「文档标题层级」在视觉上无法区分;且它不再是「下移一档」这条可复算规则的产物,而是一次逐档手调。
- **共享类 `.md-scope`(UI-REVIEW 给的另一条路)** —— 被否决,理由见 `prohibitions` 第 3 条:它要改 `app.js`,而 ROADMAP 把 `app.js` 划给 Phase 8,且 UI-REVIEW 的 Pillar 1 / Pillar 6 两条 4/4 结论都建立在「`frontend/` porcelain 为空」这个结构性证明上。

Output: `frontend/style.css` 末尾 3 条嵌入刻度规则(5 个选择器 × 3 档);`scripts/check-05-ui-uat.py` 的单一事实源枚举 `MARKDOWN_TARGETS` + 调用点普查守卫 + `item7`(逐目标断言,含严格小于文档 h1);`idi-05-UI-SPEC.md` 的 P-19 / P-20 / A-9 / 硬规则 9 改写 / 渲染目标影响面表;`idi-04.1-radix` 的连带复验证据。

**本计划关闭的缺口:** `G-idi-05-1`(blocker)。**本计划不触碰:** plan 01 / 02 / 03 的任何交付物(字号刻度七档、三段坡道、活动面板标记、两处掩码字形);`frontend/app.js` / `index.html` / `vendor/` / `scripts/ui-states/` 零 diff;`scripts/check-02-contrast.py` 与 `check-06-idi05-validation.py` 代码零改动;零新增令牌、零新增依赖、零新增文件。

**本计划的最后一项任务是 D-05 的连带义务,不是可选项:** `frontend/style.css` 与 `scripts/check-05-ui-uat.py` 都在 `idi-04.1-radix` 的 `covered_files` 里(指纹是原始字节 sha256),本计划的编辑使它的 `passed` 指纹**再次** stale。成因是内容真变,故走**重新验证**而非补指纹。指纹的写回由编排器的 `/gsd-verify-work idi-04.1-radix` 完成,不在本计划内。**同一批编辑也会让 `idi-05` 自己的 `covered_digest` stale**(它的 `covered_files` 同样含这两个文件)—— 这是缺口闭合后必然要重跑 `/gsd-verify-work idi-05` 的原因,在本计划的 SUMMARY 里登记,不改 `idi-05-VERIFICATION.md`。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/idi-05-typography-and-visual-hierarchy/05-CONTEXT.md
@.planning/phases/idi-05-typography-and-visual-hierarchy/05-UAT.md
@.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md
@.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-REVIEW.md
@.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-01-SUMMARY.md
@.planning/phases/idi-04.1-radix/idi-04.1-VERIFICATION.md
@frontend/style.css
@frontend/app.js
@scripts/check-05-ui-uat.py
@scripts/check-06-idi05-validation.py
</context>

## Artifacts this plan produces

**Plan 04 新建/改写的符号:**

| 类别 | 符号 | 位置 | 备注 |
|---|---|---|---|
| 新 CSS 规则(追加在文件末尾) | `.event-content h1, .chat-bubble h1, .say-chunk h1, .annotation-note h1, .annotation-answer-body h1` | `frontend/style.css` 末尾 | 0-1-1;`--text-xl` + `--fw-semibold` |
| 新 CSS 规则(追加在文件末尾) | 同上,`h2` | `frontend/style.css` 末尾 | 0-1-1;`--text-lg` + `--fw-semibold` |
| 新 CSS 规则(追加在文件末尾) | 同上,`h3` | `frontend/style.css` 末尾 | 0-1-1;`--text-md` + `--fw-semibold` |
| 新常量(单一事实源) | `MARKDOWN_TARGETS` | `scripts/check-05-ui-uat.py` | 9 条:`(选择器, 注入它的 app.js 函数, 刻度族)` |
| 派生常量 | `MARKDOWN_HOSTS`(4 个文档宿主)/ `RENDER_TARGETS`(5 个嵌入目标) | 同上 | 由 `MARKDOWN_TARGETS` 派生,不再是手写清单 |
| 新函数 | `check_render_markdown_call_sites(...)` | 同上 | 静态普查:`renderMarkdown(` 计数 == 10 |
| 新函数 | `item7(page, tmp_root)` | 同上 | 五个嵌入目标的逐目标断言 |
| 新断言标签 | `item7`:逐目标 × 逐档的 `font-size` / `font-weight` | item7 | 30 条(5 目标 × 3 档 × 2 属性) |
| 新断言标签 | `item7`:文档 h1 严格大于每个目标 h1 | item7 | 5 条(SC3) |
| 新断言标签 | `item7`:任何目标标题的字重 != 700 | item7 | 1 条(第四字重档) |
| 新断言标签 | `smoke`:`.chat-bubble h1` == `--text-xl` | `item_smoke` | 快速切片 |
| 契约修正 | P-19 / P-20 / A-9 / 硬规则 9 / 渲染目标影响面表 / 05-N-7 | `idi-05-UI-SPEC.md` | 见 Task 2 |

## 本计划与 05-CONTEXT 决策的关系

**直接承接(本计划的动作由它们决定):**

| 决策 | 本计划如何承接 |
|---|---|
| **D-01** | 基线口径:一律以磁盘 HEAD 的 `style.css` 值与 `check-05` 的断言为准;**不动 `04-UI-SPEC.md` / `ROADMAP.md` / `REQUIREMENTS.md` 正文**(改它们会作废已通过的验证指纹)。Task 2 的 A-9 正是 D-01 的应用:契约措辞的收窄写在**本阶段自己的** UI-SPEC 与验证记录里,不去改需求索引表 |
| **D-03** | 断言分类第一类:本计划**主动改动的字号**(五个嵌入目标的 h1/h2/h3)走**令牌接线**表述,期望侧由 `resolve_token()` 在运行时解析 —— 值层再改也不产生假 FAIL。第二类(守卫「不该变」的值)在本计划里是**负向门**:`^\.hidden {` == 1、`!important;` == 1、`@media` == 0、无全局标题规则 —— 它们保持字面,因为字面才能抓到「误伤 chrome / 机制」 |
| **D-05** | 连带义务:`frontend/style.css` 与 `scripts/check-05-ui-uat.py` 都在 `idi-04.1-radix` 的 `covered_files` 里,本计划的编辑使它**再次** stale。Task 3 逐条重跑四条守卫与三项 `human_verification` 并从 HEAD 重算;**同一批编辑也让 `idi-05` 自己的指纹 stale**,两条义务的归属都在 Task 3 登记 |
| **D-06** | 文档刻度**已定稿**为 h1 28 / h2 22 / h3 18 / 本体 16,**本计划一字不改**。嵌入刻度由它**沿数值阶梯下移一档**推出(28 → 24、22 → 18、18 → 16)—— 这是 D-06 的直接推论,不是对它的修订 |
| **D-07** | `--text-2xl`(22)与 `--text-xl`(24)的名字序与数值序不单调,故取值规则必须写明**按数值序不按名字序**;否则「下移一档」会被误读成「名字降一档」(那会给出 22 → 18 → 16,与文档 h2 撞档) |
| **D-09** | 字重三档分工:内容标题 = `--fw-semibold` 600。五个容器渲染的是**内容**(AI 输出 / 用户批注),故归内容标题档取 600 —— 这正是消除第四字重档 700 的方式 |
| **D-10** | 新开档位复用 `--lh-tight`、**零新增行高令牌**。本计划连 `line-height` 声明都不加:本缺陷的判据只有字号与字重,给标题加 `line-height` 而同一容器里的 `p` 仍走 UA 边距会造成半套节奏 —— 那是没有契约锚点的视觉扩张 |
| **D-19** | 页面级层级链已由 qrq 实现且本阶段只做复证:文档 h1(28)> `.overlay-card h3`(24)> 文档 h2(22)> 容器标签(14)。**本计划的取值规则保证这条链不因嵌入目标而失效**:嵌入 h1 取 24 而非 28,故 `28 > 24` 在 `.chat-bubble` 与 `#draft-content` 同时可见时仍成立(check-06 的 g2 断言的是严格不等式) |

**不触碰(plan 01 / 02 / 03 已交付,本计划对它们零 diff):** D-02、D-04、D-08、D-11、D-12、D-13、D-14、D-15、D-16、D-17、D-18、D-20、D-21、D-22、D-23。它们对应的交付物(七档刻度、三段坡道、`#btn-authorize` 的字重 / 字号例外、活动面板标记、两处掩码字形、`.collapse-indicator` 的零改动)在本计划的 `prohibitions` 与 verify 里以「零 diff」的形式被守住,不重复实现。

<tasks>

<task type="tracer" tdd="true">
  <name>Task 1 (tracer): 端到端「九个渲染目标的标题刻度受控」—— 门先红后绿 + 五个嵌入目标的刻度规则 + 按调用点的枚举普查</name>
  <files>frontend/style.css, scripts/check-05-ui-uat.py</files>
  <reversibility rating="reversible">取值规则(下移一档)与枚举形态(按调用点)都是纯追加:回退只需删掉末尾 3 条规则并还原枚举,既有规则的位置 / 名字 / 声明一律未动。**唯一 costly 的成分是「嵌入 h1 不得等于 28px」这条约束** —— 它由 check-06 的 g2 严格不等式锁定,想改嵌入 h1 到 28 就必须同时改 g2,那是改门而不是改值。</reversibility>
  <read_first>
    - `frontend/style.css` L714-L741 —— `.markdown-body` 的标题块与它的注释原文(「标题字号显式化,作用域限定在 `.markdown-body` 内——不写全局 h1/h2/h3」)。**这五行是本缺陷的现场**:`719-721` 是全文件唯一给 h1/h2/h3 定 `font-size` 的规则
    - `frontend/style.css` L1218-L1227 —— 文件末尾(活动面板标记的两条追加规则)。本计划的 3 条规则追加在 L1227 之后;该块的注释是「追加在文件末尾 —— 硬规则 3:追加,不重排」的既有先例
    - `frontend/style.css` L238-L250 —— 七档字号与三档字重的围栏声明(24 = `--text-xl`、18 = `--text-lg`、16 = `--text-md`;`--fw-semibold: 600`)。注意 D-07 已登记:数值序与名字序在 `xl`(24) → `2xl`(22) 这一处不单调 —— 取值规则按**数值**阶梯,不按名字
    - `frontend/style.css` L595-L604 —— `.event-content` 及其两条后代规则(`:first-child` 的 margin、`p` 的 margin)。**全文没有任何 `.event-content h1/h2/h3` 规则** —— 这是 UA 回落的确证
    - `frontend/style.css` L812-L839 —— `.chat-bubble`(16px 上下文)与 `.say-chunk`(其 `p` 有 margin 规则、无标题规则)
    - `frontend/style.css` L959-L997 —— `.annotation-note`(`color`)与 `.annotation-answer-body`(`margin-top`),以及 L986-L989 的 `.annotation-plain .annotation-note, .annotation-plain .annotation-answer-body`(0-2-0,**只声明 `font-style` 与 `color`** —— 不含 `font-size` / `font-weight`,故与本计划的 0-1-1 规则无竞争)。L1187-L1190 的 `.annotation-answered` 组同理(只 `color`)
    - `frontend/style.css` L704-L707 与 L775-L779 —— 两条收窄后的 chrome 规则(`#draft-view > h2, #round-title` / `#brainstorm-view > h2`)。确认它们**够不到**这五个容器(既非子元素,也不在 `#draft-view` / `#brainstorm-view` 之内)
    - `frontend/app.js` L112-L137 —— `renderMarkdown(text)` 的签名与返回值(一个 `DocumentFragment`,注入后成为容器的**子元素**,故后代选择器可用)
    - `frontend/app.js` L226-L247 —— `renderEvent(event)`:`kind === 'say'` 且 `window.marked` 时把 `renderMarkdown(event.content)` 追加进 `.event-content`(挂在 `#ai-events`)
    - `frontend/app.js` L259-L271 —— `makeBubble(role)` / `appendChatMessage(role, content)`:AI 角色时把 `renderMarkdown(content)` 直接追加进 `.chat-bubble`
    - `frontend/app.js` L277-L286 —— `appendSayToChat(text)`:创建或复用 `streamingBubble`,把 `renderMarkdown(text)` 追加进新建的 `.say-chunk`(`streamingBubble` 是 L88 的顶层 `let`,初值 null)
    - `frontend/app.js` L1115-L1170 —— `renderAnnotations(annotations, isCurrentRound)` 的**签名陷阱**:它读的是 `annotations.items`,**不是**数组;`.annotation-note`(:1144)与 `.annotation-answer-body`(:1157)分别承载 `item.note` 与 `item.answer`;`type === 'plain'` 时 `details.open = true`
    - `frontend/app.js` L620-L630 / L845-L852 / L903-L920 / L1047 —— 四个文档宿主的注入点(`applyPhase5View` → `#latest-check`;`loadArchiveView` → `#round-doc`;`renderDraft` → `#draft-content`;`renderBrainstorm` → `#brainstorm-content`;L1047 是 `#round-doc` 的第二个调用点)。**这四处是普查守卫要覆盖的另一半影响面**
    - `scripts/check-05-ui-uat.py` L80-L160 —— `_emit` / `ok` / `ok_true` / `ok_contains` / `blocked` 的语义:**actual 为 None ⇒ BLOCKED,绝不记 PASS**;expected 为 None(令牌未声明)⇒ 同样 BLOCKED
    - `scripts/check-05-ui-uat.py` L240-L266 —— `read_style` / `resolve_token` / `resolve_color` 三个读取器(D-03 第一类:本计划主动改动的值走令牌接线,期望侧由 `resolve_token` 在运行时解析)
    - `scripts/check-05-ui-uat.py` L390-L412 —— `make_fixture(name, tmp_root)` / `enter_project(page, project_path)`(`enter_project` 走 `page.goto` ⇒ **每个 item 都是整页重载**,顶层 `let` 不会跨 item 残留)
    - `scripts/check-05-ui-uat.py` L860-L1010 —— `MARKDOWN_HOSTS` 的定义与它的注释(「四个都要探……只探一个宿主正是它存活到执行期的原因」),以及 item4 的探针全文(用应用自身的 `renderMarkdown` 渲染一条含三级标题 / 代码 / 表格 / 引用块的探针串,再逐宿主断言)
    - `scripts/check-05-ui-uat.py` L1319-L1355 —— `item_smoke` 全文(快速切片;`check_active_marker` 已在此被调用,是本任务加一条切片的先例)
    - `scripts/check-05-ui-uat.py` L1359-L1445 —— `parse_args` / `normalize_items` / `known` / `main`(新增一项要同时改这四处 + 模块 docstring 的运行方式段与退出码语义段)
    - `scripts/check-06-idi05-validation.py` L140-L180 —— **g2 的严格不等式**(`doc_h1 > worst["size"]`,扫描面是「可见且非零 client rect」的全页元素)。这是「嵌入 h1 不得取 28px」的机械依据;g1 则断言四个 `.markdown-body` 宿主的三档严格降序 —— 两者在本任务后必须仍 PASS
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`### 字号刻度的范围栅栏(Pitfall M4 / TYPE-01)` —— 影响面枚举的方法论(「栅栏成立与否,不能只看 chrome 标题元素落在哪里,必须看 chrome 选择器能匹配到哪些元素」)与 `#brainstorm-content` 那条「记录,不处理」
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-01-SUMMARY.md` 的 `patterns-established` 第 3 条 —— 「探针宿主集合必须覆盖影响面的全部实例 —— 只探一个宿主正是本阶段层叠缺陷存活到执行期的原因」。本任务是同一教训的第二次应用
  </read_first>
  <behavior>
    - **先红后绿是本任务的验收形态,不是可选的仪式。** 门写好后、CSS 未改前,`--item 7` 必须**失败**,且失败信息里能逐字读到:`.chat-bubble h1` 的 computed `font-size` 是 `32px`(期望 `--text-xl` 的解析值 24px)、`.event-content h1` 是 `28px`、字重是 `700`(期望 600)。这段原始输出必须逐字进 SUMMARY —— 项目已记录的方法论:**变异测试是唯一能证明守卫真的会失败的手段**,一个从未红过的门无法证明它能看见本缺陷
    - 改完 CSS 后同一条命令必须转 PASS(0 FAIL / 0 BLOCKED),且**断言条数不变**(先红后绿是同一条命令的两次运行,不是两个门)
    - 容器造不出时记 BLOCKED 而非 PASS:把四个渲染函数的调用删掉(或让 `window.marked` 为假)时,`--item 7` 必须退化为 BLOCKED 而非静默 PASS。这是与 check-06 的 g4 / g5 相同的约定
    - 普查守卫本身必须可失败:把 `MARKDOWN_TARGETS` 里删掉一条时,普查断言必须 FAIL(它比的是 `app.js` 的调用点数与枚举条数,不是自比)
  </behavior>
  <action>
    **第 1 步 —— 先写门(此时必须红)。** 在 `scripts/check-05-ui-uat.py` 里做三件事,**先不改 `style.css`**:

    (a) **把渲染目标的枚举提为单一事实源。** 在 `MARKDOWN_HOSTS` 的位置定义 `MARKDOWN_TARGETS` —— 一个 9 元组,每项形如 `(选择器, 注入它的 app.js 函数名, 刻度族)`,刻度族取 `"doc"` 或 `"embedded"`。九条按影响面(调用点)列全,不按类名:`#draft-content` / `renderDraft` / doc;`#brainstorm-content` / `renderBrainstorm` / doc;`#round-doc` / `loadArchiveView` / doc;`#latest-check` / `applyPhase5View` / doc;`.event-content` / `renderEvent` / embedded;`.chat-bubble` / `appendChatMessage` / embedded;`.say-chunk` / `appendSayToChat` / embedded;`.annotation-note` / `renderAnnotations` / embedded;`.annotation-answer-body` / `renderAnnotations` / embedded。然后**由它派生**两个既有 / 新用的视图:`MARKDOWN_HOSTS = tuple(sel for sel, _fn, fam in MARKDOWN_TARGETS if fam == "doc")`(item4 的既有循环继续消费它,顺序不变),`RENDER_TARGETS = tuple(sel for sel, _fn, fam in MARKDOWN_TARGETS if fam == "embedded")`。把原 `MARKDOWN_HOSTS` 上方的注释改写为枚举纪律的登记:**枚举按 `renderMarkdown()` 的调用点,不按类名;只枚举 `.markdown-body` 的四个宿主正是 `G-idi-05-1` 存活到验证后的直接原因**;并写明「函数名」一栏是给人核对的锚点(它比行号稳,Phase 8 改 `app.js` 时行号会漂),不参与断言。

    (b) **调用点普查守卫(静态)。** 新增 `check_render_markdown_call_sites(item)`:`frontend/app.js` 的文本里 `renderMarkdown(` 的出现次数必须等于 **10**(定义行 1 次 + 9 个调用点;`#round-doc` 有两个调用点:`loadArchiveView` 与冻结轮路径),且 `len(MARKDOWN_TARGETS)` 必须等于 **9**。两条都不满足时 FAIL,`actual` 打印实测计数,`reason` 写明**可执行的动作**:「`renderMarkdown(` 的调用点数变了 —— 按调用点更新 `MARKDOWN_TARGETS`,再跑本项」。**这条守卫的用途是让枚举无法悄悄过期**:新增一个渲染目标而不更新枚举,门立刻失败。用 Python 读文件计数(`Path.read_text`),不要用 shell 管道 —— 门的判据必须由脚本自己算出。

    (c) **新增 `item7(page, tmp_root)`。** 用 `make_fixture("p1", tmp_root)` + `enter_project(page, proj)`,然后在**一次** `page.evaluate` 里用应用自身的四个渲染函数把带三级标题的探针 markdown 注入五个容器(真实渲染路径,零网络、零 AI 调用 —— 与 item4 用 `renderVerdictCard` 的 idiom 相同;`.chat-bubble` / `.say-chunk` **不需要**真实 AI 轮次,`appendChatMessage` / `appendSayToChat` 就是应用自己的注入路径),并返回五个选择器各自是否存在。探针 markdown 用 `# 探针一级` / `## 探针二级` / `### 探针三级` 三行;`renderAnnotations` 的入参必须是**对象** `{items: [...]}`,不是数组,且条目用 `type: 'plain'`(`details.open = true`,两个容器都真实渲染)、`note` 与 `answer` 都非空。返回后逐个目标断言:
      - 目标存在 ⇒ 对 h1 / h2 / h3 各断言 computed `font-size` == `resolve_token(page, "--text-xl" / "--text-lg" / "--text-md")`、computed `font-weight` == `resolve_token(page, "--fw-semibold")`(期望侧运行时解析,值层再改不产生假 FAIL);目标**不存在** ⇒ `blocked(item, ..., "<MISSING>", "容器未渲染出来")`,绝不记 PASS;
      - 五条 SC3 断言:把 `renderMarkdown` 注入 `#draft-content` 后读 `#draft-content h1`,断言它**严格大于**每个目标自己的 h1(解析成整数再比,不要比字符串 —— `"14px" < "9px"` 的序陷阱在 item4 已踩过一次);
      - 一条第四字重档断言:五个目标的 h1/h2/h3 里没有任何一个的 computed `font-weight` 等于 `700`;
      - 最后调 `check_render_markdown_call_sites(item)`。

    (d) **注册 item7。** 同步改四处:`normalize_items` 的默认列表(加 `"7"`)、`known` 集合(加 `"7"`)、`main()` 的分派(加 `if "7" in items: item7(page, tmp_root)`)、模块 docstring 的「运行方式」段(加 `--item 7` 示例)与「退出码语义」段不受影响(语义不变,仍 0/1/2)。**注意 `--item` 的默认集必须包含 7**,否则缺口闭合后的常规运行不会覆盖它。

    (e) **实跑 `--item 7`,把红色输出逐字记下来**(见 `<behavior>` 第 1 条)。此时 CSS 未改,预期看到 `.chat-bubble h1` = 32px、`.event-content h1` = 28px、字重 700。

    **第 2 步 —— 加 CSS,让门转绿。** 取值规则由三条已锁决策推出,逐条写进注释而不是留给读者推断:**D-06**(文档刻度已定稿为 28 / 22 / 18 / 本体 16,本计划一字不改,嵌入刻度是它下移一档的推论)、**D-07**(数值序与名字序在 `xl` 24 → `2xl` 22 处不单调,故「下移一档」按数值序)、**D-09**(内容标题 = `--fw-semibold` 600;五个容器渲染的是内容,故取 600,这正是消除第四字重档 700 的方式);**D-10**(零新增行高令牌,故本组规则连 `line-height` 都不加);**D-19**(页面级层级链 28 > 24 > 22 > 14 不因嵌入目标失效 —— 嵌入 h1 取 24 而非 28 正是为了这条)。断言侧按 **D-03** 第一类走令牌接线(期望值由 `resolve_token()` 运行时解析)。

    在 `frontend/style.css` **文件末尾**(L1227 的活动面板标记块之后)追加 **3 条**规则,每条一行声明体(与该文件既有的紧凑风格一致,如 L520 / L718 的写法),选择器顺序固定为 `.event-content` → `.chat-bubble` → `.say-chunk` → `.annotation-note` → `.annotation-answer-body`:
      - h1 组:`font-size: var(--text-xl); font-weight: var(--fw-semibold);`
      - h2 组:`font-size: var(--text-lg); font-weight: var(--fw-semibold);`
      - h3 组:`font-size: var(--text-md); font-weight: var(--fw-semibold);`

    配一条注释(多行,放在这组规则之前),把四件事写进去:**(1)** 这五个容器是 `renderMarkdown()` 的注入目标,不是 `.markdown-body`,所以 `.markdown-body` 的标题规则够不到它们 —— 在此之前它们回落 UA 默认值(`.chat-bubble` 里 h1 = 32px / 700,`.event-content` 里 28px / 700),既超过 `.markdown-body h2` 也与文档 h1 持平,**第四字重档 700 由此进入应用**;**(2)** 取值规则是「沿契约数值阶梯下移一档」:28 → 24(`--text-xl`)、22 → 18(`--text-lg`)、18 → 16(`--text-md`),**按数值序不按名字序**(`--text-2xl` 22 与 `--text-xl` 24 的名字序不单调,D-07 已登记);**(3)** 为什么不用全局 `h1, h2, h3` 规则 —— 它对四处 chrome 覆盖与 `.markdown-body` 都是惰性的,于是**只**命中这五个容器,看起来更省事,但它无法表达三档各不相同(要写成三条全局规则),而那会把任何将来的标题一并捕获(正是本缺陷的成因:影响面不透明),且无法把枚举逐条对照 `app.js` 的调用点;**(4)** 为什么追加在文件末尾 —— 硬规则 3(追加,不重排);这组选择器全部是 0-1-1,与既有规则无竞争(`.annotation-plain .annotation-note` 等 0-2-0 规则只声明 `font-style` / `color`,不含 `font-size` / `font-weight`)。

    **不得**给这组规则加 `margin` 或 `line-height`。理由要写进注释:本缺陷的判据是「字号 / 字重刻度受控」(`G-idi-05-1` 的 truth 与 missing 都只点名这两项);`margin` 与 `line-height` 不在该判据内,给标题加上它们而同一容器里的 `p` 仍走 UA 边距,只会造成半套节奏 —— 那是一次没有契约锚点的视觉扩张,不是本缺陷的修法。**注释里列举标题档位时,任何一行都不得以 `h1` / `h2` / `h3` 起头** —— 第 3 步的负向门按「行首或逗号后的裸类型选择器」匹配,注释自证失败会让门读起来像缺陷仍在。

    **第 3 步 —— 复核不变量并转绿。** 实跑并记录原始输出:`.venv/bin/python scripts/check-05-ui-uat.py --item 7,4,smoke`(必须 0 FAIL / 0 BLOCKED;item4 的四宿主循环必须仍绿 —— 本任务不动 `.markdown-body` 一行)、`python3 scripts/check-06-idi05-validation.py --item g1,g2`(**g2 的严格不等式是 SC3 的机械依据,必须仍 PASS**;g1 断言四宿主三档严格降序)、`bash scripts/check-01-token-conformance.sh` / `check-03` / `check-04`、`python3 scripts/check-02-contrast.py | tail -1`。核对 `^\.hidden {` 仍为 1、`!important;` 声明数仍为 1、`@media` 计数仍为 0(硬规则 8)、`frontend/app.js` 与 `index.html` 零 diff。

    **第 4 步 —— 快速切片。** 在 `item_smoke` 里加一条:用 `appendChatMessage('ai', '# 探针')` 造一个 `.chat-bubble`,断言其 `h1` 的 computed `font-size` == `resolve_token(page, "--text-xl")`。这是本缺陷在最小切片上的可失败证据,也让后续阶段的常规 `--item smoke` 能挡住同类回归。
  </action>
  <verify>
    <automated>grep -oE '(^|,)[[:space:]]*h[123][[:space:]]*[,{]' frontend/style.css | wc -l</automated>
    <fails_when>the count is not 0 (a bare/global heading type selector would collide with the four chrome overrides and with `.markdown-body`'s own rules — ROADMAP Pitfall M4 / Hard Rule 9)</fails_when>
    <automated>for c in event-content chat-bubble say-chunk annotation-note annotation-answer-body; do printf '%s=' "$c"; grep -oE "\\.$c h[123]" frontend/style.css | wc -l; done</automated>
    <fails_when>any of the five counts is not 3 (each render target needs exactly one rule per heading level)</fails_when>
    <automated>grep -o 'font-size: var(--text-xl); font-weight: var(--fw-semibold);' frontend/style.css | wc -l; grep -o 'font-size: var(--text-lg); font-weight: var(--fw-semibold);' frontend/style.css | wc -l; grep -o 'font-size: var(--text-md); font-weight: var(--fw-semibold);' frontend/style.css | wc -l</automated>
    <fails_when>any of the three counts is not 1 (the embedded scale must be exactly 24 / 18 / 16 with the semibold weight, and must not be duplicated)</fails_when>
    <automated>grep -o 'renderMarkdown(' frontend/app.js | wc -l</automated>
    <fails_when>the count is not 10 (1 definition + 9 call sites; a new call site must force the enumeration to be updated)</fails_when>
    <automated>grep -c 'MARKDOWN_TARGETS' scripts/check-05-ui-uat.py</automated>
    <fails_when>the count is less than 3 (definition + the two derived views must all reference the single source)</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 7,4,smoke</automated>
    <fails_when>exit code is not 0, or the `=== 逐项结论 ===` block reports anything other than PASS for items 7, 4 and smoke (exit 2 means at least one assertion went BLOCKED — a container could not be created, which is a failure to reach the target, not a pass)</fails_when>
    <automated>.venv/bin/python scripts/check-06-idi05-validation.py --item g1,g2</automated>
    <fails_when>exit code is not 0, or g2's strict inequality `doc_h1 > worst` fails (that assertion is the mechanical form of SC3 and is what forbids the embedded h1 from being 28px)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>any script exits non-zero or prints anything other than `PASS`</fails_when>
    <automated>python3 scripts/check-02-contrast.py | tail -1; python3 scripts/check-02-contrast.py | grep '^PASS  ' | wc -l</automated>
    <fails_when>the last line is not exactly `PASS: 0 failures`, or the pair count is not 47 (this plan adds no PAIR and changes no token value)</fails_when>
    <automated>grep -o '@media' frontend/style.css | wc -l; grep -o '!important;' frontend/style.css | wc -l</automated>
    <fails_when>the first count is not 0 (Hard Rule 8) or the second is not 1 (Hard Rule 2 — declaration lines only; this plan adds zero `!important`)</fails_when>
    <automated>git diff --stat -- frontend/app.js frontend/index.html frontend/vendor/</automated>
    <fails_when>the command prints a non-empty stat line (all three must be byte-identical to HEAD — the structural proof UI-REVIEW's Pillar 1 / Pillar 6 rest on)</fails_when>
    <automated>git status --porcelain -- frontend/</automated>
    <fails_when>the output is non-empty (the whole `frontend/` tree must be byte-identical to HEAD — this is the structural proof UI-REVIEW's Pillar 1 and Pillar 6 rest on, and it is what rules out the shared-class route through `app.js`)</fails_when>
  </verify>
  <acceptance_criteria>
    - 文件末尾追加**恰 3 条**新规则,五组选择器(`.event-content` / `.chat-bubble` / `.say-chunk` / `.annotation-note` / `.annotation-answer-body`)各出现**恰 3 次**(h1 / h2 / h3),全部为 0-1-1
    - 三档声明逐字为 `font-size: var(--text-xl); font-weight: var(--fw-semibold);` / `var(--text-lg)` / `var(--text-md)`,各恰 1 次;三档全部落在契约既有七档内,**零新增令牌、零刻度外字面量**
    - 全文件**无**行首 / 逗号后的裸 `h1` / `h2` / `h3` 类型选择器(负向门计数 == 0)
    - 新规则**不含** `margin` / `line-height`(本缺陷的判据只有字号与字重;半套节奏是无锚点的视觉扩张)
    - `MARKDOWN_TARGETS` 是单一事实源(9 条),`MARKDOWN_HOSTS` 与 `RENDER_TARGETS` 由它派生,`len(MARKDOWN_TARGETS) == 9`
    - `check_render_markdown_call_sites` 存在且断言 `frontend/app.js` 的 `renderMarkdown(` 计数 == 10;删掉 `MARKDOWN_TARGETS` 的一条会让它 FAIL(它比的是调用点数与枚举条数,不是自比)
    - `item7` 已注册进 `normalize_items` 默认集 / `known` / `main()` 分派 / 模块 docstring;`--item 7` 可单跑
    - `item7` 用四个渲染函数**造出**五个容器再断言;容器不存在时记 BLOCKED。断言含:5 目标 × 3 档的 `font-size` 与 `font-weight`(30 条)、5 条「文档 h1 严格大于目标 h1」(SC3)、1 条「无任何目标标题字重为 700」
    - **先红后绿证据齐备**:CSS 改动前的 `--item 7` 原始输出(含 32px / 28px / 700 三项实测)与改动后的全 PASS 输出,都逐字进 SUMMARY
    - `item_smoke` 新增一条 `.chat-bubble h1` == `--text-xl` 的快速切片
    - `--item 7,4,smoke` 全 PASS(0 FAIL / 0 BLOCKED);`check-06 --item g1,g2` 全 PASS;`check-01` / `03` / `04` PASS;`check-02` 47 对 `PASS: 0 failures`
    - `^\.hidden {` == 1、`!important;` == 1、`@media` == 0;`frontend/app.js` / `index.html` / `vendor/` 零 diff
  </acceptance_criteria>
  <done>五个非 `.markdown-body` 渲染目标里的 h1/h2/h3 解析为 24 / 18 / 16px 与 `--fw-semibold`,UA 默认值(32px / 28px)与第四字重档 700 双双消失;文档 h1 仍是全屏最大(28 > 24,check-06 的 g2 仍 PASS);check-05 的枚举改为按 `renderMarkdown()` 调用点,并有会失败的普查守卫;门有先红后绿的原始输出作证。</done>
</task>

<task type="auto">
  <name>Task 2: 契约补齐 —— P-19 / P-20 / A-9 / 硬规则 9 改写 / 渲染目标影响面表</name>
  <files>.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md</files>
  <reversibility rating="reversible">纯记账:本任务只改契约文本,零渲染影响。回退是删除新增行并把硬规则 9 与零列表还原。</reversibility>
  <read_first>
    - `idi-05-UI-SPEC.md` §`## Deliberate Delta Ledger(本阶段)` 全节 —— P-1…P-18 的行格式(五列:`#` / Delta / 站点 / 幅度 / 为什么),以及紧随其后的**零列表**原文(「不在本 ledger、且必须是零的:任何既有选择器的位置 / 名字 / 声明增删(除 P-2…P-4 与 P-12 / P-13 点名的那些)……」)
    - `idi-05-UI-SPEC.md` §`## 契约修正登记` 全节 —— A-1…A-8 的行格式(`#` / 修正 / 依据 / 影响)。**注意 A-5 的先例**:「不改 REQUIREMENTS.md(改它会作废指纹),只在计划与验证记录里登记」—— 本任务的 A-9 与它同型
    - `idi-05-UI-SPEC.md` §`## Global Hard Rules` 的**第 9 条**原文 —— 「不得给 `.markdown-body` 容器之外的任何 `h1` / `h2` / `h3` 写字号规则」及其三段理由(全局规则特异性 0-0-1、对四处 chrome 覆盖惰性、真正的暴露面是「任何落在 `.markdown-body` 之外又没有更具体规则兜底的标题」)。**最后半句正是本缺陷的现场:它已经点出了暴露面,却没有把暴露面枚举出来**
    - `idi-05-UI-SPEC.md` §`### 字号刻度的范围栅栏(Pitfall M4 / TYPE-01)` 全节 —— chrome 标题的五行表、订正记录、以及「`.markdown-body` 的四个宿主(改动的影响面,计划必须点名)」那一句(本任务把「影响面」从四个宿主扩到九个目标)
    - `idi-05-UI-SPEC.md` §`### 标题映射(D-06,定稿)` 的四行表(文档 h1/h2/h3/本体)与 §`### TYPE-03 —— 字重三档分工显式化(D-09)` 的分工表(「内容标题 | `--fw-semibold` 600 | `.markdown-body h1, .markdown-body h2, .markdown-body h3`」那一行)
    - `idi-05-UI-SPEC.md` §`### 未在 HEAD 上受控的字号(不属本阶段,见 §不在本阶段)` 全节 —— 它只列了 `.collapse-indicator` 的 20px 与 `#confirm-error` 的 16px。**本任务要把「五个渲染目标回落 UA 默认值」这条漏掉的普查项补进去并标注已闭合**
    - `idi-05-UI-SPEC.md` §`## Notes(05-N-1 … 05-N-6)` 的格式(每条一段,首句加粗带编号)
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-REVIEW.md` 的 **Top Fix 2** 与 **Finding 4.1** —— 前者是 P-19 的原始发现(「ledger 是这一阶段的机器可读『一切都是故意的』契约;a reader auditing『这是不是回归?』会在这阶段最承重的一次编辑上拿到假阳性」),后者是 P-20 的实测表(五个目标 × 三档的 UA 实际值)
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-04-PLAN.md` 的 `<objective>` —— 取值规则表与被否决的两个候选(契约里要引用同一条规则,不得写出第三种说法)
  </read_first>
  <action>
    六处编辑,全部在 `idi-05-UI-SPEC.md` 内。**不得**改 `04-UI-SPEC.md` / `idi-04.1-UI-SPEC.md` / `ROADMAP.md` / `REQUIREMENTS.md` 的正文(D-01 与 A-5 已裁定:改它们会作废已通过的验证指纹)。

    **第 1 处 —— Deliberate Delta Ledger 增两行(P-19 / P-20),紧接 P-18 之后。** 行格式与 P-1…P-18 一致(五列)。

    **P-19 —— chrome 标题选择器由后代形态收窄为子组合器 / id 形态(补记)。** Delta 一栏写:`#draft-view h2, #rounds-placeholder h2` → `#draft-view > h2, #round-title`(一条规则),`#brainstorm-view h2` → `#brainstorm-view > h2`(一条规则)。站点一栏写 `:704` 与 `:775`。幅度一栏写 **2 条规则 / 3 个选择器名**(原形态的三个选择器名里,`#rounds-placeholder h2` 被换成 `#round-title`)。为什么一栏写:层叠修复 —— 原形态是 1-0-1 **后代**选择器,会伸进 `.markdown-body` 容器把 `.markdown-body h2`(0-1-1)无条件压回 chrome 字号(ID 列胜过类列,与源码顺序无关);改用子组合器 / id 形态后两者在层叠上永不相遇,22px 才在三个宿主上可达。**必须写明这是「补记」**:该改动发生在 plan 01 的执行期(已登记在契约的订正记录、`WINDOWS.md` 第 15 条与 `idi-05-01-SUMMARY.md`),但此前**没有 P-item** —— 按本 ledger 自己的规则(「不在此表上的变化即回归」),未登记的改动会让审计者在全阶段最承重的一次编辑上拿到假阳性。这正是 `G-idi-05-1` 的 `missing` 第 3 项。

    **P-20 —— 五个非 `.markdown-body` 渲染目标的嵌入标题刻度。** Delta 一栏写:`.event-content` / `.chat-bubble` / `.say-chunk` / `.annotation-note` / `.annotation-answer-body` 的 h1/h2/h3 获得显式 `font-size` 与 `font-weight`。站点一栏写「文件末尾追加的 3 条规则」。幅度一栏写:`.chat-bubble` 上下文 h1 32 → 24、h2 24 → 18、h3 18.7 → 16;`.event-content` 上下文 h1 28 → 24、h2 21 → 18、h3 16.4 → 16;字重一律 700 → 600。为什么一栏写:`G-idi-05-1` —— `renderMarkdown()`(app.js:112)的返回值被注入这五个容器,而它们**不是** `.markdown-body`,故标题回落 UA 默认值:既超过 `.markdown-body h2`(22px)又与文档 h1(28px)持平或反超,使 SC3 的「文档 h1 是全屏最大最重的文字」为假,并把第四个字号档与第四个字重档 700 带进只声明三档(400 / 500 / 600)的应用。取值规则是「沿契约数值阶梯下移一档」(`--text-3xl` 28 → `--text-xl` 24、`--text-2xl` 22 → `--text-lg` 18、`--text-lg` 18 → `--text-md` 16,**按数值序不按名字序**),三档全在既有七档内,零新增令牌。

    **第 2 处 —— 修正零列表。** 把「(除 P-2…P-4 与 P-12 / P-13 点名的那些)」改写为「(除 P-2…P-4、P-12 / P-13、**P-19** 与 **P-20** 点名的那些)」。P-19 是**既有选择器的名字改动**(正是零列表原本要拦的那一类),P-20 是**新增规则**(不在零列表的字面范围内,但必须一起点名,否则读者会以为它越过了零列表)。两处都要写清各自属于哪一类。

    **第 3 处 —— `## 契约修正登记` 增 A-9。** 修正一栏写:**硬规则 9 与 REQUIREMENTS 的 TYPE-01 里「作用域限定在 `.markdown-body` 内」这一句,按 `G-idi-05-1` 收窄为「不得写全局 `h1, h2, h3` 规则;`renderMarkdown()` 的每个渲染目标必须在 style.css 侧逐个列举」。依据一栏写 `G-idi-05-1` 的 truth 与 missing 第 1 项。影响一栏写:硬规则 9 的**原字面**禁止了本缺陷唯一的 CSS 侧修法(它把「不得写全局规则」这条正确的意图,写成了「不得给 `.markdown-body` 之外的任何 h1/h2/h3 写字号规则」这条会自相矛盾的措辞 —— 缺陷本身正是「`.markdown-body` 之外的标题无人管」);TYPE-01 的需求行**不改**(改 `REQUIREMENTS.md` 会作废指纹,A-5 同型),只在计划与验证记录里登记。同时写明:**A-9 收窄的是措辞,不是意图** —— 全局规则仍然禁止,禁止的理由仍是原第 9 条自己写的那半句。

    **第 4 处 —— 改写硬规则 9 的正文。** 新措辞的实质(逐句写进契约,保留原有的三段理由):**(a)** 不得写裸类型选择器的全局标题规则(`h1` / `h2` / `h3` 单独成条,或 `h1, h2, h3` 合并成条;特异性 0-0-1)—— 它对四处 chrome 覆盖与 `.markdown-body` 的标题规则都是**惰性的**,于是只会命中「`.markdown-body` 之外、又没有更具体规则兜底的标题」,而**那正是 `G-idi-05-1` 的五个容器**:一条全局规则会让它们暂时变对,却把「哪些容器受影响」这件事重新变成不可枚举;**(b)** 因此本阶段的形态是**逐容器列举**:凡给 `.markdown-body` 之外的标题写字号规则,必须在同一次提交里把 `renderMarkdown()` 的**全部**注入目标列进选择器表,并让 check-05 的枚举(按调用点)与之一一对应;**(c)** 可机械核的形态:`grep -oE '(^|,)[[:space:]]*h[123][[:space:]]*[,{]' frontend/style.css` 必须为 **0**;五个嵌入容器的 `h[123]` 各恰出现 3 次。把原来的第三段理由(「真正的暴露面是四处 chrome 规则未声明的那些属性,以及任何落在 `.markdown-body` 之外又没有更具体规则兜底的标题」)保留并**追加一句**:那半句已经点出了暴露面,但没有把暴露面枚举出来 —— `G-idi-05-1` 就是只读这半句、没做枚举的结果。

    **第 5 处 —— §字号刻度的范围栅栏 增「渲染目标影响面」表。** 表里的刻度族一栏要引用同一条取值规则(出自 **D-06** 的文档刻度按 **D-07** 的数值序下移一档,字重按 **D-09** 取内容标题档 600;本组规则不加 `line-height`,与 **D-10** 的「零新增行高令牌」一致);影响面一栏要引用 **D-19** 的层级链(28 > 24 > 22 > 14),说明嵌入 h1 取 24 而非 28 正是为了让这条链在会话流有标题时仍成立。在既有「`.markdown-body` 的四个宿主」那一句之后追加这个表,列出 `renderMarkdown()` 的**全部九个**注入目标:选择器 / 注入它的 `app.js` 函数 / 刻度族(`doc` = 文档刻度 28 / 22 / 18;`embedded` = 嵌入刻度 24 / 18 / 16)。九条为:`#draft-content` / `renderDraft` / doc;`#brainstorm-content` / `renderBrainstorm` / doc;`#round-doc` / `loadArchiveView` / doc;`#latest-check` / `applyPhase5View` / doc;`.event-content` / `renderEvent` / embedded;`.chat-bubble` / `appendChatMessage` / embedded;`.say-chunk` / `appendSayToChat` / embedded;`.annotation-note` / `renderAnnotations` / embedded;`.annotation-answer-body` / `renderAnnotations` / embedded。表下写明三条:(a) 枚举**按调用点,不按类名**(`#round-doc` 有两个调用点:`loadArchiveView` 与冻结轮路径);(b) check-05 的 `MARKDOWN_TARGETS` 是本表的机器可核形态,调用点普查守卫(`renderMarkdown(` 计数 == 10)使两者无法漂移;(c) 表里的「函数名」是给人核对的锚点,比行号稳。同时把「改动的影响面,计划必须点名」那一句改为「改动的影响面 = 下表九行,计划必须逐行点名」。

    **第 6 处 —— §未在 HEAD 上受控的字号 与 Notes。** 在 §未在 HEAD 上受控的字号 里追加一段:本节此前的普查**漏了五个渲染目标**(`.event-content` / `.chat-bubble` / `.say-chunk` / `.annotation-note` / `.annotation-answer-body`),它们在本阶段之前一直回落 UA 默认值(`.chat-bubble` 上下文 32 / 24 / 18.7px、`.event-content` 上下文 28 / 21 / 16.4px,字重一律 700)—— 这条漏项使该节「刻度外的第 6 个渲染字号」这个计数本身不成立;现已由 P-20 闭合,该段要写明**闭合状态**(不是「仍存在」)。然后在 Notes 末尾加 **05-N-7**:check-06 的 g2(全页最大字号扫描)的扫描面是**当前状态里已存在的可见元素**,故它对本缺陷的五个容器是**状态盲**的 —— `p1` 下 fixture 里没有 `.chat-bubble` 时 g2 看不到任何 UA 回落的标题。本阶段把 g2 的严格不等式(`doc_h1 > 全屏最大字号`)搬进 check-05 的 item7(那里**先造容器再断言**),使这条判据不再依赖「fixture 恰好有内容」;g2 自身的扫描面加固**不在本阶段**,记录在此以防日后被误读为已覆盖。

    **不得**在本任务里做范围外的事:不修 UI-REVIEW 的 6 条 WARNING / 4 条 INFO(60/30/10 面积、G3 的 0.22 余量、chrome 子视图标题 18/18/16、`mask-image` 的 `@supports` 回退、`#session-panel .panel-header` 的 `cursor`),P-19 是唯一例外且只因为它被本缺陷的 `missing` 清单点名;不改任何既有 P-item / A-item 的措辞;不改 REQUIREMENTS.md / ROADMAP.md / 两份旧 UI-SPEC。
  </action>
  <verify>
    <automated>grep -c '^| \*\*P-19\*\*' .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md; grep -c '^| \*\*P-20\*\*' .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md</automated>
    <fails_when>either count is not 1 (the ledger must gain exactly one P-19 row and one P-20 row, in the same five-column format as P-1…P-18)</fails_when>
    <automated>grep -c 'P-19' .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md; grep -c 'P-20' .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md</automated>
    <fails_when>either count is less than 2 (each must appear both as its ledger row and in the amended zero-list exception list)</fails_when>
    <automated>grep -c 'A-9' .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md; grep -c '05-N-7' .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md</automated>
    <fails_when>either count is less than 1 (A-9 must be registered in the amendment table; 05-N-7 must be added to the Notes)</fails_when>
    <automated>for s in '#draft-content' '#brainstorm-content' '#round-doc' '#latest-check' '.event-content' '.chat-bubble' '.say-chunk' '.annotation-note' '.annotation-answer-body'; do printf '%s=' "$s"; grep -cF -- "$s" .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md; done</automated>
    <fails_when>any of the nine selectors is missing from the contract (the impact-surface table must enumerate all nine render targets, not only the four `.markdown-body` hosts)</fails_when>
    <automated>for f in 'renderDraft' 'renderBrainstorm' 'loadArchiveView' 'applyPhase5View' 'renderEvent' 'appendChatMessage' 'appendSayToChat' 'renderAnnotations'; do printf '%s=' "$f"; grep -cF -- "$f" .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md; done</automated>
    <fails_when>any of the eight injection functions is missing (the enumeration must be by call site, with the injecting function named as the human-checkable anchor)</fails_when>
    <automated>grep -cE '(^|,)[[:space:]]*h[123][[:space:]]*[,{]' .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md</automated>
    <fails_when>the count is 0 (the rewritten Hard Rule 9 must state the mechanical form of its own gate, so a reader can run it; the pattern appearing here is contract prose, not CSS)</fails_when>
    <automated>git status --porcelain -- .planning/REQUIREMENTS.md .planning/ROADMAP.md .planning/phases/idi-04-tokens-contract/ .planning/phases/idi-04.1-radix/</automated>
    <fails_when>the output is non-empty (A-9 registers the TYPE-01 scope narrowing in the plan/verification record; editing REQUIREMENTS.md would invalidate the verification fingerprints — same disposition as A-5)</fails_when>
    <automated>git status --porcelain</automated>
    <fails_when>the output lists anything other than the UI-SPEC, `frontend/style.css` and `scripts/check-05-ui-uat.py` as modified (this plan's surface is exactly those three files plus its own PLAN/SUMMARY)</fails_when>
  </verify>
  <acceptance_criteria>
    - Ledger 增 **P-19**(chrome 选择器收窄,五列格式,明确标注为**补记**并引用 WINDOWS #15 / plan 01)与 **P-20**(五个渲染目标的嵌入刻度,含五个目标 × 三档的实测幅度与「下移一档」的取值规则)
    - 零列表的例外项改为「P-2…P-4、P-12 / P-13、P-19 与 P-20」,并写清 P-19 属「既有选择器改名」、P-20 属「新增规则」
    - `## 契约修正登记` 增 **A-9**:硬规则 9 与 TYPE-01 的「作用域限定在 `.markdown-body` 内」按 `G-idi-05-1` 收窄为「不得写全局标题规则 + 渲染目标必须逐个列举」;`REQUIREMENTS.md` **零改动**(A-5 同型处置)
    - 硬规则 9 的正文已改写:禁止裸类型选择器的全局标题规则、要求逐容器列举、并写出可机械核的负向门正则;原有的三段理由保留,第三段追加「只点出暴露面而不枚举暴露面,就是本缺陷的成因」
    - §字号刻度的范围栅栏 新增九行影响面表(选择器 / 注入函数 / 刻度族),并写明「按调用点不按类名」与「`MARKDOWN_TARGETS` 是本表的机器可核形态」
    - §未在 HEAD 上受控的字号 补记五个目标曾回落 UA 默认值并标注**已闭合**(P-20)
    - Notes 增 **05-N-7**:g2 对五个容器状态盲,严格不等式已搬进 check-05 的 item7,g2 自身加固不在本阶段
    - 契约里不出现第三种取值说法(与 `<objective>` 的取值规则表逐字一致);未修任何 WARNING / INFO 项(除 P-19 这条被 `missing` 点名的)
    - `git status --porcelain` 只列出本计划的三个改动面(加 PLAN / SUMMARY)
  </acceptance_criteria>
  <done>契约不再自相矛盾:硬规则 9 的措辞与 `G-idi-05-1` 的修法一致;ledger 能回答「P-19 的 chrome 收窄是不是回归」(否)与「五个容器的标题刻度是哪来的」(P-20);影响面表把 `renderMarkdown()` 的九个目标点名,与 check-05 的枚举一一对应;`REQUIREMENTS.md` / `ROADMAP.md` / 两份旧 UI-SPEC 零改动。</done>
</task>

<task type="auto">
  <name>Task 3: D-05 连带义务 —— 再次复验 idi-04.1-radix(从 HEAD 重算,不补指纹)</name>
  <files>scripts/check-05-ui-uat.py</files>
  <read_first>
    - `.planning/phases/idi-04.1-radix/idi-04.1-VERIFICATION.md` frontmatter —— `covered_files` 清单(含 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`)、`covered_digest` 的形态(`v1:sha256:…`)、`human_verification` 的三项
    - `.planning/phases/idi-04.1-radix/idi-04.1-VERIFICATION.md` 正文 §`## Gaps Summary` 附近与 `_指纹重算_` 一节 —— 04.1 自己记录过「`REQUIREMENTS.md` 同时在多份报告的 `covered_files` 里,任何一次阶段收口都会同时打掉此前所有覆盖该文件的报告」这条结构性观察。本任务只重算、不补指纹,理由与它一致
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-03-PLAN.md` 的 Task 3 —— **同一义务的上一次履行范本**(四条守卫 + 三项 `human_verification` + 三处结论的逐条核对 + 数量差值登记 + 指纹写回留给编排器)。本任务是它的重演,数值口径按本阶段当前状态更新
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-VERIFICATION.md` frontmatter —— `covered_files` 含 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`,`covered_digest` 为 `v1:sha256:b34a2d19…`。**本计划的编辑会让它同样 stale** —— 这条要登记进 SUMMARY
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`### D-05 连带义务 —— 本阶段必须复验 idi-04.1-radix` —— 复验时必须逐条确认的三处 04.1 结论表
    - `scripts/check-05-ui-uat.py` 的 item2(冻结轮 backstop)与 item6 —— 复验的三项之一
  </read_first>
  <action>
    **本任务不改 `frontend/style.css`,也不改任何断言逻辑;产物是复验证据,零 diff。** 逐条重跑 `idi-04.1-radix` 的验证项并**从 HEAD 重算全部数值**(D-05:stale 的成因是内容真变,故走重新验证而非补指纹),把原始输出与结论写进本计划的 SUMMARY。

    **第 1 步 —— 重跑四条守卫并记录原始输出。** `bash scripts/check-01-token-conformance.sh`(期望 `PASS`)、`python3 scripts/check-02-contrast.py`(期望 `PASS: 0 failures` + 逐行比值)、`bash scripts/check-03-hidden-uniqueness.sh`(`^\.hidden {` == 1)、`bash scripts/check-04-important-count.sh`(`!important;` 声明数 == 1)。

    **第 2 步 —— 重跑 04.1 的三项 `human_verification` 与 `--item 1,2,3,4,6,7`。** 三项按 `idi-04.1-VERIFICATION.md` frontmatter 逐条执行并记录:①`check-05` 的 `## UI Considerations` backstop 陈述(16 条 E1…E16 的视觉 / 几何行为,其中 7 条含 CHECK-02 比值半边);②`--color-text ON --color-surface-mark` 的比值(该对**不在**围栏清单里,`check-02` 看不见它 —— 用与 `check-02` 同一模型独立算出并记录);③TOKEN-07 的「断言序关系」半场(`REQUIREMENTS.md` 标 `Complete`,但代码库里没有任何脚本比较四个 `--z-*` 的值 —— 这是已由用户在 `VALIDATION.md` 裁定的 manual-only 处置,**照实记录其状态,不得单方面翻转**)。第 5 项的两条真实 AI 冒烟沿用已记录的 `--ai-smoke` 证据(或按需重跑并记录);**本计划新增的 item7 也在这一批里跑一次**,证明缺口闭合后的门与 04.1 的复验互不干扰。

    **第 3 步 —— 逐条核对 04.1 的三处结论未因本计划的改动而失效,并记录数量差值。** 逐条:
    - **清单全 PASS + `ORDER 0.363`** → 本计划**不动任何令牌值与任何 `/* PAIR */` 行**,故清单仍 **47 对(35 TEXT + 12 NON-TEXT)**,`ORDER` 应**仍为 0.363** —— 核对并记录实测值。
    - **`--color-text-info ON --color-surface-info` = 4.53**(0.03 余量)→ 未触碰,该行须**逐字不变**。
    - **冻结轮**:`opacity 1` + `filter saturate(0.6)` + `inset 3px 0 0 --color-action-warning` → 未触碰(plan 03 新增的活动态竖条是**另一个**元素上的同形声明);`--item 2` 须仍 PASS。
    - **`--color-border-strong` = `--radix-gray-9`,实测 3.24 / 3.15** → 未触碰,`check-02` 两行须逐字不变。
    - **25 tier-1 / 48 tier-2** → 本计划**新增令牌 0 个**,两数均不变(04.1 的 `## Color` 节写的是 47 tier-2,那是它那一代的数;plan 03 已把 47 → 48 登记过,本任务只需确认 48 未变)。
    - 逐条写明:本计划只追加了 3 条**没有声明任何新令牌**的 CSS 规则与一组 `check-05` 的断言 / 枚举代码,故 04.1 的每一处结论都应逐字不变;若有任何一处变了,那是本计划的缺陷,不是 04.1 的过期。

    **第 4 步 —— 登记两条指纹义务的归属。** 在 SUMMARY 里明确写出:(a) `idi-04.1-radix` 的 `covered_digest` 因本计划改动了它的两个 `covered_files` 而 stale,指纹写回由编排器执行 `/gsd-verify-work idi-04.1-radix`;(b) **`idi-05` 自己的 `covered_digest`(`v1:sha256:b34a2d19…`)同样因本计划而 stale** —— 它的 `covered_files` 也含 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`,缺口闭合后必须重跑 `/gsd-verify-work idi-05`。**两份报告文件都不得自行改写**(那会让「谁改了什么」不可追溯)。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh</automated>
    <fails_when>non-zero exit, or any of the three scripts prints something other than `PASS`</fails_when>
    <automated>python3 scripts/check-02-contrast.py | tail -1; python3 scripts/check-02-contrast.py | grep '^PASS  ' | wc -l; python3 scripts/check-02-contrast.py | grep '^ORDER 0.363' | wc -l</automated>
    <fails_when>the last line is not exactly `PASS: 0 failures`, the pair count is not 47, or the ORDER line count is not 1</fails_when>
    <automated>python3 scripts/check-02-contrast.py | grep '^PASS  4.53  --color-text-info on --color-surface-info' | wc -l; python3 scripts/check-02-contrast.py | grep -E '^PASS  3\.(24|15)  --color-border-strong on --color-surface' | wc -l</automated>
    <fails_when>the first count is not 1, or the second is not 2 (04.1's thin-margin pair and its border-strong lines must be byte-unchanged)</fails_when>
    <automated>grep -oE '^[[:space:]]*--(white|radix-[a-z]+-[0-9]+):' frontend/style.css | wc -l; grep -oE '^[[:space:]]*--color-[a-z0-9-]+:' frontend/style.css | wc -l</automated>
    <fails_when>the first count is not 25 or the second is not 48 (this plan declares zero new tokens — the fix uses only existing ranks)</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 1,2,3,4,6,7</automated>
    <fails_when>exit code is not 0, or the `=== 逐项结论 ===` block reports anything other than PASS for items 1, 2, 3, 4, 6 and 7</fails_when>
    <automated>git status --porcelain -- .planning/phases/idi-04.1-radix/ .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-VERIFICATION.md</automated>
    <fails_when>the output is non-empty (neither report may be rewritten by this task — the fingerprint refresh belongs to the orchestrator's verify-work step)</fails_when>
  </verify>
  <acceptance_criteria>
    - 四条守卫全绿:CHECK-01 `PASS`、CHECK-02 `PASS: 0 failures`(47 对 + `ORDER 0.363`)、CHECK-03 `PASS`、CHECK-04 `PASS`
    - 04.1 的三处结论逐条核对并记录:`ORDER 0.363` 不变;`--color-text-info ON --color-surface-info` 4.53 逐字不变;`--color-border-strong` 两行 3.24 / 3.15 逐字不变;冻结轮标记(`--item 2`)仍 PASS
    - 数量口径已登记并确认不变:tier-1 **25**、tier-2 **48**、清单 **47 对**(本计划新增令牌 0 个、新增 PAIR 0 条)
    - `--item 1,2,3,4,6,7` 六项全 PASS(0 FAIL / 0 BLOCKED),其中 item7 是缺口闭合后的新门
    - 04.1 的三项 `human_verification` 逐条复核并记录(含 TOKEN-07 序关系半场的 manual-only 状态照实记录,不翻转)
    - `.planning/phases/idi-04.1-radix/` 与 `idi-05-VERIFICATION.md` **零改动**;两条指纹义务(`/gsd-verify-work idi-04.1-radix` 与 `/gsd-verify-work idi-05`)在 SUMMARY 里逐条写明归属
  </acceptance_criteria>
  <done>D-05 的连带义务再次履行:04.1 的四条守卫与三项人工验证项在 HEAD 上重跑通过,全部数值从 HEAD 重算而非补指纹,三处结论与三处数量口径逐字不变,两份报告文件零改动;`idi-05` 自身的指纹 stale 已登记并归给编排器。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| `renderMarkdown()` 的输出 → 五个非 `.markdown-body` 容器 | AI 与用户内容经 `stripUnsafeNodes` 消毒后注入(`T-idi03-02` 的既有缓解,**本计划零改动**)。本计划只给这些容器里的标题加字号 / 字重,不触碰注入路径、不改 `app.js` 一个字节 |
| 围栏 `:root` → 浏览器 | 令牌值的唯一事实源。本计划**不改任何令牌值、不新增任何令牌** —— 3 条新规则只消费既有档(`--text-xl` / `--text-lg` / `--text-md` / `--fw-semibold`) |
| `frontend/app.js` 的调用点 → check-05 的枚举 | 本计划新增的主边界:枚举必须由**调用点**推出,并由静态普查守卫钉住。这条边界此前不存在,正是缺陷存活的原因 |
| `scripts/check-06-idi05-validation.py` 的 g2 → 本计划 | g2 的严格不等式(`doc_h1 > 全屏最大字号`)是对本计划取值规则的**外部约束**,不是本计划的一部分;本计划必须让它继续 PASS,不得改它来迁就取值 |
| 本计划无新增网络 / 输入 / 依赖面 | `frontend/app.js` / `index.html` / `vendor/` 零 diff;零新增文件、零新增依赖、零构建步骤 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|-----------|-----------|----------|-------------|-----------------|
| T-idi-05-04-01 | Elevation of Privilege | SC3 的页面级层级声明(「文档 h1 是全屏最大最重的文字」) | high | mitigate | 本缺陷的实质是**一句关于全屏的声明被一个局部探针担保**。缓解:item7 逐目标断言 + 5 条「文档 h1 严格大于目标 h1」,且 check-06 的 g2(全页扫描,严格不等式)必须仍 PASS。两条判据一内一外,任一条失败即 FAIL |
| T-idi-05-04-02 | Tampering | 新规则与四处 chrome 覆盖 / `.markdown-body` 标题规则的层叠 | medium | mitigate | 负向门禁止裸类型选择器(`grep -oE '(^|,)[[:space:]]*h[123][[:space:]]*[,{]'` == 0);新规则全为 0-1-1 且追加在文件末尾;`.annotation-plain` / `.annotation-answered` 的 0-2-0 规则只声明 `font-style` / `color`(已逐条核过,不含 `font-size` / `font-weight`),故无竞争。`check-01` / `03` / `04` 每任务复跑;本计划新增 0 条 `!important`、0 条 `@media` |
| T-idi-05-04-03 | Tampering | 枚举与 `app.js` 调用点的漂移 | high | mitigate | 静态普查守卫断言 `renderMarkdown(` 计数 == 10 且 `len(MARKDOWN_TARGETS) == 9`;计数一变即 FAIL 并给出可执行动作。**这条是本计划针对缺陷根因的直接缓解** —— 前两次同类缺陷都是「枚举不全而无人发现」 |
| T-idi-05-04-04 | Denial of Service | 渲染回归(会话流 / 事件流 / 批注正文的标题字号) | medium | mitigate | 每个 `style.css` 任务带至少一项运行时验证(硬规则 7):item7 用应用自身的四个渲染函数**造出**五个容器再读 computed style;容器造不出记 BLOCKED 而非 PASS;`item_smoke` 加一条 `.chat-bubble h1` 快速切片 |
| T-idi-05-04-05 | Information Disclosure | 本计划的改动内容 | low | accept | 改动只有 3 条 CSS 规则(5 个选择器 × 3 档)、一组 check-05 的枚举与断言、一份契约的记账段落;无用户数据、无网络请求、无外部资源 |
| T-idi-05-04-SC | Tampering | npm / pip / cargo 安装 | high | mitigate | 本阶段零安装(硬规则 6):不新增依赖、文件或构建步骤;`ls frontend/vendor/` 断言仍只含 `marked.min.js`。无 `[ASSUMED]` / `[SUS]` 包,故无需 package-legitimacy 人工签核门 |

</threat_model>

<verification>
- `grep -oE '(^|,)[[:space:]]*h[123][[:space:]]*[,{]' frontend/style.css | wc -l` → `0`(无全局标题规则;ROADMAP Pitfall M4 / 硬规则 9)
- 五个嵌入容器的 `h[123]` 各恰 3 次(`.event-content` / `.chat-bubble` / `.say-chunk` / `.annotation-note` / `.annotation-answer-body`)
- 三档声明各恰 1 次:`font-size: var(--text-xl); font-weight: var(--fw-semibold);` / `var(--text-lg)` / `var(--text-md)`
- `grep -o 'renderMarkdown(' frontend/app.js | wc -l` → `10`(1 定义 + 9 调用点);`MARKDOWN_TARGETS` 为单一事实源
- `.venv/bin/python scripts/check-05-ui-uat.py --item 7,4,smoke` → 全 PASS(0 FAIL / 0 BLOCKED);**改动前的同一条命令有 FAIL 原始输出存证**(先红后绿)
- `.venv/bin/python scripts/check-06-idi05-validation.py --item g1,g2` → 全 PASS(**g2 的严格不等式是 SC3 的机械依据,不得改它来迁就取值**)
- `.venv/bin/python scripts/check-05-ui-uat.py --item 1,2,3,4,6,7` → 全 PASS(D-05 复验批次)
- `bash scripts/check-01-token-conformance.sh` → `PASS`;`check-03` → `PASS`(`^\.hidden {` == 1);`check-04` → `PASS`(`!important;` 声明数 == 1)
- `python3 scripts/check-02-contrast.py` → `PASS: 0 failures`,**47 对(35 TEXT + 12 NON-TEXT)+ `ORDER 0.363`**,`4.53` 与 `3.24` / `3.15` 三行逐字不变
- `grep -o '@media' frontend/style.css | wc -l` → `0`(硬规则 8)
- tier-1 == 25;tier-2 `--color-*` == 48(本计划新增令牌 0 个)
- `git diff --stat -- frontend/app.js frontend/index.html frontend/vendor/` 为空;`git status --porcelain` 只有本计划的三个改动面(+ PLAN / SUMMARY)
- 契约:`P-19` / `P-20` 各 1 行且各在零列表被点名;`A-9` 已登记;硬规则 9 含可机械核的负向门正则;影响面表列出全部九个目标与八个注入函数;`05-N-7` 在 Notes;`REQUIREMENTS.md` / `ROADMAP.md` / 两份旧 UI-SPEC 零改动
- D-05:`.planning/phases/idi-04.1-radix/` 与 `idi-05-VERIFICATION.md` 零改动;复验数值与两条指纹义务已记录在 `idi-05-04-SUMMARY.md`,指纹写回留给编排器的 `/gsd-verify-work idi-04.1-radix` 与 `/gsd-verify-work idi-05`
</verification>

<success_criteria>
- `G-idi-05-1` 关闭:`renderMarkdown()` 的全部九个注入目标上,h1/h2/h3 解析为契约内的字号档与 `--fw-semibold`;UA 默认值(32px / 28px)与第四字重档 700 双双消失(TYPE-01 / TYPE-03)
- 文档 h1 仍是全屏最大最重的文字(28 > 24),在任何 AI 吐出发散标题的状态下都成立;check-06 的 g2 仍 PASS(VISUAL-03 / SC3)
- 门能看见它该看见的东西:五个嵌入目标是**造出来再断言**的,容器造不出记 BLOCKED;枚举按调用点且有会失败的普查守卫;先红后绿证据齐备
- 契约不再自相矛盾:P-19 / P-20 入账,零列表同步除外,A-9 收窄硬规则 9 与 TYPE-01 的措辞,影响面表把九个目标点名
- 四条不变量与既有交付物零回归:`^\.hidden {` == 1、`!important;` == 1、`@media` == 0、围栏外零裸 hex;`check-02` 47 对全 PASS;plan 01 / 02 / 03 的交付物(app.js / index.html / vendor 零 diff)未被触碰
- D-05 的连带义务履行完毕,复验证据齐备,两条指纹 stale 的归属已登记
</success_criteria>

<output>
Create `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-04-SUMMARY.md` when done
</output>
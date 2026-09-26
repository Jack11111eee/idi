---
phase: idi-09-card-containers
plan: 02
type: execute
wave: 2
depends_on:
  - idi-09-01
files_modified:
  - frontend/style.css
  - scripts/check-09-idi09-validation.py
autonomous: true
requirements:
  - CARD-03
  - REG-01
  - VIS-02

estimate:
  tokens: 34000
  raw_tokens: 34000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- CARD-03 — the page sinks, and the three tiers read in the right order ----
    - "`body` 的计算 `background-color` 为 `rgb(240, 240, 240)`(gray-3)—— 页面不再是全场最亮的东西"
    - "屏幕上同时可见的三档亮度顺序在真实浏览器里成立且可机器判定:页面(gray-3)< `--color-surface`(gray-2,控件内陷面)< 卡片(`--color-surface-card`,白);控件内陷面仍读作「凹」、卡片仍读作「凸」"
    - "画在 `--color-surface-page` 上的 6 条 PAIR 以 gray-3 重算后全部达标,且清单里**登记**的重算值就是运行时实测值:`--color-text` 14.30 / `--color-text-secondary` 5.19 / `--color-text-muted` 5.19 / `--color-focus` 5.15(NON-TEXT)/ `--color-border-hover` 5.19(NON-TEXT)/ `--color-marker-active` 4.18(NON-TEXT)"
    - "登记动作是**重算**,不是刷新旧值:清单历史段逐条写出 8 条配对的「旧值 → 新值」,其中 2 条(`--color-marker-active` TEXT 与 `--color-border-strong` NON-TEXT)已在计划 01 重新归属到卡片底色,此处登记的是它们「页面旧值 → 页面新值(不达标)→ 卡片值(达标)」的完整链条"
    - "`--color-surface-page` 的**声明值**是 `var(--radix-gray-3)`,且它仍只有一个消费者:`html, body` 的 `background`;围栏内零新增令牌、零新增 tier-1 原语"
    # ---- 密度(D-9-2)— 几何判据,不是文本判据 ----
    - "`#main-pane` 的计算 `gap` 为 `12px`(`var(--space-3)`),替换 HEAD 的 `6px`(`var(--space-1-5)`);卡片之间因此有可见间隙"
    - "`.panel-body` 的计算 `padding` 为 `16px`(`var(--space-4)`),替换 HEAD 的 `10px`(`var(--space-2-5)`);`#doc-panel-body` 的 `padding` 逐字未动(它不带 `.panel-body` 类,且 `check-05` item 4 有活断言)"
    # ---- 契约保持 ----
    - "`#doc-panel` 的计算 `overflow-y` 仍为 `auto`,`#chat-messages` 的计算 `overflow-y` 仍为 `auto`;`#doc-panel` 仍是 `#doc-panel-header` 的最近可滚祖先(sticky 表头因此仍生效)"
    - "`#main-pane` 仍是面板区唯一的面板级滚动容器祖先;本计划零 `overflow` 改动"
    # ---- gates ----
    - "`.venv/bin/python scripts/check-02-contrast.py` 打印 `PASS: 0 failures`,且 8 条受影响配对的运行时实测值与清单登记值逐条一致"
    - "`bash scripts/check-01-token-conformance.sh` / `check-03` / `check-04` 全部打印 `PASS`"
    - "`.venv/bin/python scripts/check-09-idi09-validation.py --item c3 --item c4 --item c5` 全 PASS,`exit=0`,0 FAIL / 0 BLOCKED"

  artifacts:
    - path: "frontend/style.css"
      provides: "`--color-surface-page` 换值为 `var(--radix-gray-3)`;`#main-pane` 的 `gap` 与 `.panel-body` 的 `padding` 就地改为紧凑档;清单历史段新增 Phase 9 的 8 条重算登记"
      contains: "--color-surface-page: var(--radix-gray-3);"
    - path: "scripts/check-09-idi09-validation.py"
      provides: "追加断言集 `c3`(三层刻度亮度序 + `body` 计算底色)/ `c4`(`#main-pane` gap 与 `.panel-body` padding 的几何读数)/ `c5`(滚动契约)"
      contains: "--item"

  key_links:
    - from: "`frontend/style.css` 围栏内的 `--color-surface-page`(`:122`)"
      to: "`html, body` 的 `background`(`:574`)"
      via: "唯一消费者 —— 换值即整页换色,无第二处需要同步"
      pattern: "background: var\\(--color-surface-page\\);"
    - from: "`#main-pane` 的 `gap: var(--space-3)`(`:594`)"
      to: "左栏 4 个 section 之间的可见间隙"
      via: "flex 容器的 gap —— 间隙里透出的是页面底色(gray-3),这正是「卡片浮在页面之上」的可见形态"
      pattern: "gap: var\\(--space-3\\);"
    - from: "`.panel-body { padding: var(--space-4); }`(`:688`)"
      to: "左栏 4 个面板的正文内边距"
      via: "`.panel-body` 是左栏 4 个 section 的正文容器;`#doc-panel-body` 是 id 选择器且不带该类,不受影响"
      pattern: "padding: var\\(--space-4\\);"
    - from: "`/* PAIR --color-text ON --color-surface-page TEXT */` 等 6 条(`:455/465/470/514/542/562`)"
      to: "清单历史段 Phase 9 的重算登记"
      via: "条目名逐字不变;登记的是「以 HEAD 内容重算后的比值」,由 check-02 的运行时实测复核"
      pattern: "on --color-surface-page"

  prohibitions:
    - statement: "不得「刷新」旧 PAIR 值。`--color-surface-page` 的旧值是 gray-1(`#fcfcfc`),换值使画在它上面的 8 条配对全部失效 —— 刷新等于断言「自验证以来什么都没变」,而这里是假的。必须逐条以 HEAD 内容**重算**并登记,且登记值必须与 `check-02` 的运行时实测输出逐位一致"
      status: active
      verification: flagged
    - statement: "不得为了让 6 条重算后的配对达标而改任何颜色值或放宽阈值。这 6 条换值后**本来就达标**(深色前景对比度上升);若实测出现不达标,正确动作是停下来重新测量并把结果报回,不是改色、不是改 `scripts/check-02-contrast.py` 的任何一行、不是删条目"
      status: active
      verification: flagged
    - statement: "不得改动 `#doc-panel-body { padding: var(--space-8) var(--space-10); }`(`:665`)。它是阅读列的呼吸空间,且 `check-05` item 4 有活断言 `[p1] #doc-panel-body padding == \"32px 40px\"`。密度改动只落在 `.panel-body`(左栏 4 个面板),两者互不影响"
      status: active
      verification: flagged
    - statement: "不得为了「让间距看起来更大」而给 `#main-pane` 加 `padding` 或给卡片加 `margin`。`#main-pane` 是滚动容器,加 padding 会改变滚动几何与末条可达性(`check-05` item 9 断言面板区滚动者集合**恰好**是 `{#main-pane, #chat-messages, #latest-check}`,且断言末条内容可达);卡片加 margin 会移动既有几何并可能打在 24×24 命中区门上。页面级留白是**未裁定项**,列入截图后由用户裁定的开放清单,不在本阶段构建"
      status: active
      verification: flagged
    - statement: "不得新增任何 PAIR 条目、不得删除任何 PAIR 条目、不得改动任何 PAIR 的 `TEXT` / `NON-TEXT` 种类标记。本计划的清单改动只在注释层面(历史登记)与围栏内 `--color-surface-page` 的声明值;`grep -o '/\\* PAIR' frontend/style.css | wc -l` 必须仍为 53、`grep -o '/\\* ORDER' frontend/style.css | wc -l` 必须仍为 1"
      status: active
      verification: flagged
    - statement: "不得移动任何既有规则块的位置(硬规则 3:追加,不重排)。`--color-surface-page` 的换值是围栏内一行声明的就地改值;`#main-pane` 的 `gap` 与 `.panel-body` 的 `padding` 是既有声明体的就地改值;没有任何新增规则块"
      status: active
      verification: flagged
    - statement: "不得改动 `frontend/app.js` / `frontend/index.html` / `frontend/vendor/`(零字节);不得新增依赖、构建步骤、CSS 框架或新文件;不得在 `frontend/style.css` 里新增 `@layer` / `@property` / `var(--x, #fallback)` / 媒体查询 / `!important`,也不得在任何注释里写字面量 `!important;`(check-04 按出现次数计数)"
      status: active
      verification: flagged
---

<objective>
把页面底色下沉到 `--radix-gray-3`(#f0f0f0),并把左栏的密度收到用户裁定的紧凑档(内边距 16px / 卡片间距 12px)—— 让「白卡片浮在灰页面之上」这件事在屏幕上真的成立,而不只是 CSS 里成立。

Purpose: 计划 01 让五个容器变成白卡片,但页面当时仍是 gray-1(`#fcfcfc`)—— 那是全场**最亮**的值,白卡片贴在它上面几乎没有层次。CARD-03 就是这一步:页面下沉一档,三档刻度(gray-3 页面 < gray-2 控件内陷面 < 白卡片)才接成连贯的 elevation 序列(shadcn 的 canvas / inset / raised)。密度同理由用户裁定(D-9-2):左栏 4 个面板叠放在 900px 视口里竖向预算本来就紧,紧凑档(16px / 12px)比标准档(24px / 16px)少消耗约 76px。

本计划同时承担本阶段最高风险的一项:**页面换值会作废画在它上面的全部 8 条对比度配对**。其中 6 条换值后仍达标(深色前景在更暗的地面上对比度**上升**),2 条(中间调前景)已在计划 01 重新归属到卡片底色。本计划必须逐条以 HEAD 内容**重算**并登记 —— 不是刷新旧值。这条纪律的理由:`--color-surface-page` 的旧值是 gray-1,刷新等于断言「自验证以来什么都没变」,而这里是假的。

Output: `frontend/style.css` 的 `--color-surface-page` 换值、`#main-pane` 的 `gap` 与 `.panel-body` 的 `padding` 改值、清单历史段的 8 条重算登记;`scripts/check-09-idi09-validation.py` 追加 `c3` / `c4` / `c5` 三组断言。

**依赖与前置:** 本计划依赖 `idi-09-01`。它假定计划 01 已把 `--color-surface-card` / `--shadow-card` 声明进围栏、五个容器已卡片化、2 条 PAIR 已重新归属到 `--color-surface-card`。执行前先复核:`grep -n -- '--color-surface-card' frontend/style.css` 至少 4 处命中,且 `.venv/bin/python scripts/check-02-contrast.py` 打印 `PASS: 0 failures`。

**一处须以磁盘为准的口径差(规划期实测,勿被文档带偏):** 文档里的「54 条 PAIR」是「53 条 `/* PAIR */` + 1 条 `/* ORDER */`」的**清单条目**合计数。判据一律取磁盘计数:`grep -o '/\* PAIR' frontend/style.css | wc -l` == 53,`grep -o '/\* ORDER' frontend/style.css | wc -l` == 1。

**本计划关闭的需求:** CARD-03、REG-01(页面换值半边)。**本计划不触碰:** 卡片语言本身(计划 01 已交付,本计划零回改);`frontend/app.js` / `index.html` / `vendor/` 零字节;`scripts/check-01…07` / `probe-05` / `probe-07` 代码零改动;`check-05-ui-uat.py` 零改动;表格重做 / 圆角刻度收敛 / 图标与空状态 / `.overlay-card` 底色 / 页面级留白(Out of Scope 或未裁定项)。
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
@frontend/style.css
@scripts/check-09-idi09-validation.py
</context>

## Artifacts this phase produces

> 本节的用途:**plan-review-convergence 的 source-grounding pass 读它,把本阶段新建的符号从漂移校验里排除**。
> 本节列出**全阶段**(三个计划)的产出;本计划只登记自己那部分。

**新增 CSS 自定义属性(围栏 `:root` 内,由计划 01 创建,本计划零新增):**

| # | 符号 | 值 | 计划 | 备注 |
|---|---|---|---|---|
| 1 | `--color-surface-card` | `var(--white)` | 01 | 本计划把它作为「三层刻度」的最亮档引用,不改值 |
| 2 | `--shadow-card` | `0 1px 2px rgba(0, 0, 0, 0.04)` | 01 | 本计划零改动 |

**新增文件:**

| # | 路径 | 计划 | 备注 |
|---|---|---|---|
| 3 | `scripts/check-09-idi09-validation.py` | 01(骨架 + c1 / c2) | 本计划追加 `c3` / `c4` / `c5` |
| 4 | `.planning/phases/idi-09-card-containers/screenshots/*.png` | 03 | 供用户评审的截图 |

**就地改值的既有声明(规则块位置与源码顺序逐字不变):**

| # | 符号 | HEAD 位置 | 计划 | 动作 |
|---|---|---|---|---|
| 5 | `--color-surface-page` | `:122` | **02** | `var(--radix-gray-1)` → `var(--radix-gray-3)` |
| 6 | `#main-pane` 的 `gap` | `:594` | **02** | `var(--space-1-5)`(6px)→ `var(--space-3)`(12px) |
| 7 | `.panel-body` 的 `padding` | `:688` | **02** | `var(--space-2-5)`(10px)→ `var(--space-4)`(16px) |

**清单改动(围栏内):**

| # | 符号 | HEAD 位置 | 计划 | 动作 |
|---|---|---|---|---|
| 8 | `PAIR --color-marker-active ON --color-surface-page TEXT` | `:523` | 01 | 地面已改记为 `--color-surface-card`(4.77) |
| 9 | `PAIR --color-border-strong ON --color-surface-page NON-TEXT` | `:526` | 01 | 地面已改记为 `--color-surface-card`(3.32) |
| 10 | 其余 6 条页面地面配对 | `:455/465/470/514/542/562` | **02** | 条目名逐字不变;清单历史段登记 8 条配对的「旧值 → 新值」重算链 |
| 11 | 清单历史段 Phase 9 段 | `:427-452` | 01 / **02** | 01 记地面重新归属;02 记 8 条重算前后值 |

**明确不产生的新符号:** 零新增 tier-1 原语、零新增 tier-2 颜色令牌、零新增圆角 / 间距刻度值、零新依赖、零构建步骤、零新应用文件。

## 波次与依赖形状(本阶段的真实约束,不是保守)

| 波次 | 计划 | 落点 | 为什么必须在这个位置 |
|---|---|---|---|
| 1 | `idi-09-01` | 卡片令牌 + 五个容器的卡片语言 + 2 条 PAIR 重新归属 | 卡片地面必须先存在:2 条中间调配对的正解是「重新归属到卡片底色」,而卡片底色是本波次创建的 |
| 2 | `idi-09-02`(本计划) | 页面下沉 + 6 条 PAIR 重算登记 + 密度 | 页面换值是唯一会作废 8 条配对的动作,必须在卡片地面已存在、2 条已重新归属之后才动 —— 否则 `check-02` 会在中间态红着 |
| 3 | `idi-09-03` | 五条浏览器门复跑 + pytest 基线 + 截图 | 回归门必须看到波次 1/2 的全部改动 |

## 8 条受影响配对的完整账(规划期已实测,执行器须复核)

| 配对 | 需要 | gray-1(旧页面) | gray-3(新页面) | 卡片白 | 处置 |
|---|---|---|---|---|---|
| `--color-text` TEXT | 4.5 | 15.88 | **14.30** | — | 条目名不变,登记重算值 |
| `--color-text-secondary` TEXT | 4.5 | 5.77 | **5.19** | — | 同上 |
| `--color-text-muted` TEXT | 4.5 | 5.77 | **5.19** | — | 同上 |
| `--color-focus` NON-TEXT | 3.0 | 5.72 | **5.15** | — | 同上 |
| `--color-border-hover` NON-TEXT | 3.0 | 5.77 | **5.19** | — | 同上 |
| `--color-marker-active` NON-TEXT | 3.0 | 4.65 | **4.18** | — | 条目名不变(保留页面地面作保守读数,计划 01 已登记理由) |
| `--color-marker-active` TEXT | 4.5 | 4.65 | ~~4.18~~ FAIL | **4.77** | 计划 01 已重新归属到 `--color-surface-card` |
| `--color-border-strong` NON-TEXT | 3.0 | 3.24 | ~~2.91~~ FAIL | **3.32** | 计划 01 已重新归属到 `--color-surface-card` |

**反直觉之处(已实测,别按直觉推断):** 页面变暗**不**让所有配对变好。深色前景对比度上升,但**中间调**前景(blue-11 / gray-9)对比度**下降**。两条 FAIL 都是中间调 —— 这正是「重新归属」而不是「调色」的理由。

<tasks>

<task type="auto">
  <name>Task 1: 密度收档 —— `#main-pane` 的卡片间距 6px → 12px,`.panel-body` 的内边距 10px → 16px</name>
  <files>frontend/style.css, scripts/check-09-idi09-validation.py</files>
  <reversibility rating="reversible">两处都是既有声明的单值改回,单文件一行即可回退;本任务不新增令牌、不新增规则、不改变任何选择器。</reversibility>
  <read_first>
    - `frontend/style.css` `#main-pane { … gap: var(--space-1-5); overflow-y: auto; align-items: center; min-width: 0; }`(`:590-603`)—— **本任务就地改值的第一个目标**,`gap` 在 `:594`;其 `min-width: 0` 上方那段「不得当作冗余代码删除」的注释逐字保留
    - `frontend/style.css` `.panel-body { padding: var(--space-2-5); }`(`:688`)与紧随的 `.panel-body.collapsed { display: none; }`(`:689`)—— **第二个目标**;`padding` 是 `.panel-body` 唯一的声明
    - `frontend/style.css` `#doc-panel-body { padding: var(--space-8) var(--space-10); }`(`:665`)—— **不得改动**;它是 id 选择器且元素不带 `.panel-body` 类
    - `frontend/style.css` 间距刻度 `--space-1-5: 6px;` / `--space-2-5: 10px;` / `--space-3: 12px;` / `--space-4: 16px;`(`:295-300`)—— 四个值都已声明且已被消费,本任务**不新增刻度值**
    - `frontend/style.css` `#main-pane > section { … }`(`:605-608`)—— 计划 01 已就地扩写为卡片规则;本任务只读它,确认卡片之间透出的间隙就是 `#main-pane` 的 `gap`
    - `frontend/style.css` `#checks-panel .panel-body { display: flex; flex-direction: column; gap: var(--space-2-5); }`(`:1313`)与 `#session-panel .panel-body { display: flex; flex-direction: column; flex: 1; min-height: 0; }`(`:974-979`)—— 只读:两条规则都**不**声明 `padding`,故 `.panel-body` 的 `padding` 改值对四个面板一致生效,无覆盖冲突
    - `scripts/check-05-ui-uat.py` `:1045-1062` —— 规划期已逐条确认:这里断言的是 `.panel-header padding-top == "6px"`、`#doc-panel-body padding == "32px 40px"`、`button padding-top == "6px"`、`.overlay-card padding-top == "24px"`。**没有一条**断言 `.panel-body` 的 `padding` 或 `#main-pane` 的 `gap` ⇒ 本任务的改值不打破任何既有断言(执行器须自行复核这一点)
    - `scripts/check-09-idi09-validation.py`(计划 01 产出)—— 本任务按同一形态追加 `c4`
    - `.planning/phases/idi-09-card-containers/09-CONTEXT.md` §`D-9-2:卡片密度 = 紧凑` —— 16px / 12px 的用户裁定值与竖向预算算术
  </read_first>
  <action>
    **第 1 步 —— `#main-pane` 的 `gap`(`:594`)由 `var(--space-1-5)` 改为 `var(--space-3)`。** 就地改值,选择器文本与规则块位置逐字不变。改后卡片间距为 12px,间隙里透出的是页面底色 —— 这正是「卡片浮在页面之上」的可见形态。

    **第 2 步 —— `.panel-body` 的 `padding`(`:688`)由 `var(--space-2-5)` 改为 `var(--space-4)`。** 就地改值。改后左栏 4 个面板的正文内边距为 16px。

    **第 3 步 —— 给 `scripts/check-09-idi09-validation.py` 追加断言集 `c4`(几何读数,不是文本匹配)。**
    - `#main-pane` 的计算 `gap` == `12px`;
    - `document.querySelector('.panel-body')`(文档序第一个 `.panel-body`,即 `#session-panel` 内的那一个)的计算 `padding` == `16px`;
    - 对照组:`#doc-panel-body` 的计算 `padding` == `32px 40px`(证明密度改动没有漏到右栏 —— 与 `check-05` item 4 的既有断言同口径,不是重复劳动:这里是**回归护栏**,防止后续有人把 `.panel-body` 的选择器扩成同时命中 `#doc-panel-body`);
    - 对照组:`.panel-header` 的计算 `padding-top` == `6px`(表头内边距**未**随卡片内边距一起改,这是刻意的 —— 表头是 36px 固定高的 chrome 条,它的内边距不在 D-9-2 的裁定范围内)。

    三个期望值都用字面量 px 字符串(几何读数,不是颜色令牌),与 `check-05` 里 `padding` 断言的既有写法一致。元素读不到时走 `blocked()` 分支,绝不记 PASS。

    **第 4 步 —— 不触碰清单之外的一切。** 本任务**不**改 `--color-surface-page`(Task 2)、**不**改任何 PAIR 条目、**不**改任何颜色值、**不**改 `#doc-panel` / `#doc-panel-body` / `.panel-header` 的既有声明。`frontend/app.js` / `index.html` / `vendor/` 零字节;`scripts/check-05-ui-uat.py` 本计划零改动。

    **注释纪律**同计划 01:围栏外注释不得含裸 `#hex` / tier-1 原语名 / 字面量 `!important;` / `@layer` / `@property` / `var(--x, #fallback)`。
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
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c4</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or the trailing "exit=" line not "exit=0"</fails_when>
  </verify>
  <acceptance_criteria>
    - `frontend/style.css` 中 `#main-pane` 规则体的 `gap` 值为 `var(--space-3)`,其选择器文本与 HEAD 逐字一致,且改动全部落在既有规则体内部(源码顺序未变,未移动任何既有规则块);`.panel-body` 规则体的 `padding` 值为 `var(--space-4)`,其选择器文本与 HEAD 逐字一致,且改动全部落在既有规则体内部(源码顺序未变,未移动任何既有规则块)。
    - `grep -n 'gap: var(--space-3);' frontend/style.css` 命中数相对 HEAD **恰好 +1**(HEAD 已有的 `--space-3` gap 消费者不受影响);`grep -n 'gap: var(--space-1-5);' frontend/style.css` 的命中数相对 HEAD **恰好 −1**。
    - `grep -n 'padding: var(--space-2-5);' frontend/style.css` 相对 HEAD **恰好 −1**;`#doc-panel-body` 的 `padding: var(--space-8) var(--space-10);` 逐字未变。
    - `.venv/bin/python scripts/check-09-idi09-validation.py --item c4` 全 PASS,`exit=0`,BLOCKED 计数 0;INFO 行可见 `#main-pane` 的 gap 原始读数与 `.panel-body` 的 padding 原始读数。
    - `bash scripts/check-01-token-conformance.sh` / `check-03` / `check-04` 打印 `PASS`;`.venv/bin/python scripts/check-02-contrast.py` 打印 `PASS: 0 failures`(本任务零颜色改动,清单逐字不变)。
    - `git diff frontend/style.css` 在本任务范围内的改动**恰好 2 处声明值**(`gap` 与 `.panel-body padding`),无其他行被触碰。
    - `git status --porcelain frontend/` 仅列出 `frontend/style.css`;`frontend/vendor/` 仍只有 `marked.min.js`。
  </acceptance_criteria>
  <done>卡片间距为 12px、左栏面板内边距为 16px,均以真实浏览器的计算几何证明;`#doc-panel-body` 与 `.panel-header` 的内边距逐字未动;四个静态门 + `check-09 --item c4` 全绿。</done>
</task>

<task type="auto">
  <name>Task 2: 页面底色下沉到 gray-3 + 画在页面上的 6 条 PAIR 逐条重算并登记</name>
  <files>frontend/style.css</files>
  <reversibility rating="costly">声明本身是一行改值即可回退;但这次换值作废了画在页面上的全部 8 条配对 —— 回退必须连同清单历史段的重算登记一起回退,否则登记值与实测值不一致,`check-02` 的复核会指向错误的方向。两处成对,故评级 costly 而非 reversible。</reversibility>
  <read_first>
    - `frontend/style.css` 围栏内 `--color-surface-page: var(--radix-gray-1);`(`:122`)与它周边的 tier-2 声明区(`:118-126`);`--radix-gray-1: #fcfcfc;` / `--radix-gray-2: #f9f9f9;` / `--radix-gray-3: #f0f0f0;`(`:48-50`)
    - `frontend/style.css` `html, body { … background: var(--color-surface-page); … }`(`:570-576`)—— **该令牌的唯一消费者**;规划期已 grep 确认围栏外只有这一处引用
    - `frontend/style.css` 清单段 `:416-566` —— 逐条读 8 条画在页面上的配对:`:455`(`--color-text`)/ `:465`(`--color-text-secondary`)/ `:470`(`--color-text-muted`)/ `:514`(`--color-focus` NON-TEXT)/ `:542`(`--color-border-hover` NON-TEXT)/ `:562`(`--color-marker-active` NON-TEXT);另两条 `:523` / `:526` 已在计划 01 改记为卡片地面
    - `frontend/style.css` `:427-452` —— 清单头部台账(六个 value layer 的规模 `24 / 34 / 43 / 47 / 50 / 53`、覆盖地板、标记计数一致性)。**本任务在此追加 Phase 9 的重算登记段**
    - `frontend/style.css` `:564-566` —— `/* ORDER --color-text-muted BEFORE --color-text ON --color-surface */`。它的两个操作数都画在 `--color-surface` 上,**与页面换值无关** ⇒ ORDER 行的比值(`0.363`)本任务后不变
    - `scripts/check-02-contrast.py` 全文(`:1-235`)—— `PAIR_RE` / `DECL_RE` / `resolve()` / 覆盖地板 / `raw_pairs` 计数一致性 / `TEXT_MIN` / `NON_TEXT_MIN` / 输出格式 `PASS  %.2f  %s`。**本任务一行都不改它**
    - `.planning/phases/idi-09-card-containers/09-CONTEXT.md` §`规划期实测的对比度影响面`(8 条逐条重算表)与 §`两条 FAIL 的正解 = 重新归属配对` 与 §`禁止的两种错误修法`
    - `.planning/ROADMAP.md` §`### Phase 9:` Deliverables 第 4 条、Success Criterion 5、Pitfalls 第 1 / 2 条
  </read_first>
  <action>
    **第 1 步 —— 围栏内 `--color-surface-page` 的声明值由 `var(--radix-gray-1)` 改为 `var(--radix-gray-3)`。** 就地改值,不新增令牌、不新增 primitive(`--radix-gray-3` 已在 `:50` 声明且已被 `--color-surface-sunken`(`:123`)与 `--color-surface-hover`(`:184`)消费)。改值后 `html, body` 的底色即 `rgb(240, 240, 240)`。

    在该声明旁追加一句注释(围栏内,可写数值),记下:Phase 9 把页面从 gray-1 下沉到 gray-3(CARD-03,用户裁定 D-9-1),目的是与白卡片接成 gray-3 < gray-2 < 白的三级刻度;该令牌只有一个消费者(`html, body`),换值即整页换色;页面换值作废了画在它上面的 8 条配对,处置见清单历史段的 Phase 9 记录。

    **第 2 步 —— 在 `:427-452` 的清单头部台账之后追加一段 Phase 9 的**重算登记**,逐条写出 8 条配对的完整链条。** 这是本任务的核心交付物 —— REG-01 的「逐条以 HEAD 内容重算并登记,不是刷新旧值」就落在这里。登记格式为「配对 | 旧页面(gray-1) | 新页面(gray-3) | 卡片白 | 处置」,数值必须与下表逐位一致(规划期已实测,执行器须用 `check-02` 的实跑输出复核):

    - `--color-text` TEXT:15.88 → **14.30** → 条目名不变,达标
    - `--color-text-secondary` TEXT:5.77 → **5.19** → 条目名不变,达标
    - `--color-text-muted` TEXT:5.77 → **5.19** → 条目名不变,达标
    - `--color-focus` NON-TEXT:5.72 → **5.15** → 条目名不变,达标
    - `--color-border-hover` NON-TEXT:5.77 → **5.19** → 条目名不变,达标
    - `--color-marker-active` NON-TEXT:4.65 → **4.18** → 条目名不变,达标(保留页面地面作保守读数,理由见 `:559-562`)
    - `--color-marker-active` TEXT:4.65 → 4.18(**FAIL**)→ 已重新归属到 `--color-surface-card`,白底 **4.77** 达标
    - `--color-border-strong` NON-TEXT:3.24 → 2.91(**FAIL**)→ 已重新归属到 `--color-surface-card`,白底 **3.32** 达标

    登记段还必须写明三件事:(a) **反直觉之处** —— 页面变暗不让所有配对变好:深色前景对比度上升,中间调前景(blue-11 `#0d74ce` / gray-9 `#8d8d8d`)对比度**下降**,两条 FAIL 都是中间调;(b) **正解是重新归属,不是调色、不是放宽阈值** —— 这 2 条的元素全部画在面板内部,卡片化后它们确实坐在白卡片上,如实登记绘制面不是变通;(c) **本阶段全程未改动任何颜色值、未新增 primitive、未放宽阈值**。**不得**改写那六个历史规模数字(`24 / 34 / 43 / 47 / 50 / 53`),**不得**把 Phase 9 混进那串数字 —— 本阶段清单规模不变(53 对 + 1 条 ORDER = 54 条清单条目),变的是地面归属与实测值。

    **第 3 步 —— 明令禁止。** 不得新增 / 删除任何 PAIR 条目;不得改动任何 `TEXT` / `NON-TEXT` 标记;不得改动 `scripts/check-02-contrast.py` 的任何一行(含 `TEXT_MIN` / `NON_TEXT_MIN`);不得改任何 `--radix-*` 值或 tier-2 颜色值。若实测发现某条重算后不达标(规划期预判不会发生 —— 这 6 条换值后本来就是上升的),**停下来**把实测值报回,不得就地改色或改阈值。

    **第 4 步 —— 注释纪律。** 本任务的注释都写在围栏内,裸 `#hex` 合法;仍不得含字面量 `!important;`(check-04 按出现次数计数)。不得新增 `@layer` / `@property` / `var(--x, #fallback)`。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-02-contrast.py</automated>
    <fails_when>non-zero exit, or any line beginning with "FAIL", or the final line not "PASS: 0 failures", or the output missing any of the exact lines "PASS  14.30  --color-text on --color-surface-page", "PASS  5.19  --color-text-secondary on --color-surface-page", "PASS  5.19  --color-text-muted on --color-surface-page", "PASS  5.15  --color-focus on --color-surface-page", "PASS  5.19  --color-border-hover on --color-surface-page", "PASS  4.18  --color-marker-active on --color-surface-page", "PASS  4.77  --color-marker-active on --color-surface-card", "PASS  3.32  --color-border-strong on --color-surface-card"</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>non-zero exit, or stdout not exactly "PASS"</fails_when>
    <automated>bash scripts/check-03-hidden-uniqueness.sh</automated>
    <fails_when>non-zero exit, or stdout not exactly "PASS"</fails_when>
    <automated>bash scripts/check-04-important-count.sh</automated>
    <fails_when>non-zero exit, or stdout not exactly "PASS"</fails_when>
  </verify>
  <acceptance_criteria>
    - `frontend/style.css` 围栏内 `--color-surface-page: var(--radix-gray-3);` 逐字成立;逐行核对 `git diff -U0 frontend/style.css` 的输出:除该行外不存在任何其他 `--radix-` 增删行(无任何 primitive 值被改动)。
    - `grep -o '/\* PAIR' frontend/style.css | wc -l` == 53;`grep -o '/\* ORDER' frontend/style.css | wc -l` == 1(两者与 HEAD 逐字相同)。
    - `.venv/bin/python scripts/check-02-contrast.py` 打印 `PASS: 0 failures`,且输出含上表 8 个数值对应的 8 行 PASS(含两条卡片地面的 4.77 / 3.32);ORDER 行仍为 `ORDER 0.363  --color-text-muted before --color-text on --color-surface`。
    - 清单历史段的 Phase 9 登记里,6 条重算值的数字与 `check-02` 实跑输出**逐位一致**(14.30 / 5.19 / 5.19 / 5.15 / 5.19 / 4.18),且两条 FAIL → 重新归属的链条完整写出(含 4.18 / 2.91 两个失败值与 4.77 / 3.32 两个卡片值)。
    - 清单历史段里 `24 / 34 / 43 / 47 / 50 / 53` 六个数字逐字保留,Phase 9 记录以独立段落追加。
    - `git diff scripts/check-02-contrast.py` 为空。
    - `git status --porcelain frontend/` 仅列出 `frontend/style.css`。
  </acceptance_criteria>
  <done>页面底色为 gray-3(`body` 计算值 `rgb(240, 240, 240)` 由 Task 3 的运行时门证明);画在页面上的 6 条配对以新底色重算后全部达标并逐条登记;2 条 FAIL 的重新归属链条完整;零颜色值改动、零阈值放宽、零条目增删;`check-02` 全绿。</done>
</task>

<task type="auto">
  <name>Task 3: 三层刻度的运行时门 —— `body` 底色 + 三档亮度序 + 滚动契约(c3 / c5)</name>
  <files>scripts/check-09-idi09-validation.py</files>
  <reversibility rating="reversible">只新增断言,不改任何产品代码;回退是删除本任务追加的两个断言集。</reversibility>
  <read_first>
    - `scripts/check-09-idi09-validation.py`(计划 01 产出 + Task 1 追加的 `c4`)—— 本任务按同一形态追加 `c3` / `c5`,并同步模块 docstring 的断言映射表与 `--item` help 文本
    - `scripts/check-05-ui-uat.py` `:289-300` —— `contrast_ratio` / `relative_luminance` 的既有实现(**直接复用,不另写一份** —— 与 `probe-07` 的纪律一致:「直接导入它自己的实现,不另写一份」)
    - `scripts/check-05-ui-uat.py` `:471-484` —— `effective_bg()`;本任务读的是**令牌级**的三档值(不是某个元素的有效背景),故用 `resolve_color()` 分别解析 `--color-surface-page` / `--color-surface` / `--color-surface-card` 三个令牌后比较
    - `scripts/check-05-ui-uat.py` `:2682-2760` —— item 9 的面板区滚动者普查与其「口径取『恰好』而非『至多』」注释。**本任务不重复那条普查**(它已由 item 9 承担,计划 03 复跑);本任务只断言本阶段改动的两个具体滚动者
    - `frontend/style.css` `#doc-panel { … overflow-y: auto; … }`(计划 01 后仍逐字保留)、`#chat-messages { flex: 1; min-height: 160px; overflow-y: auto; … }`(`:980-988`)、`#doc-panel-header { position: sticky; top: 0; … }`(`:649-654`)
    - `.planning/phases/idi-09-card-containers/09-CONTEXT.md` §`D-9-1:底色关系 = 页面下沉 + 白卡片`(三级刻度的裁定)与 §`已核实的非问题`(两处 `position: fixed` 元素自带底色,不受页面换值影响)
  </read_first>
  <action>
    **第 1 步 —— 追加断言集 `c3`(三层刻度,CARD-03 的渲染判据)。**
    - `body` 的计算 `background-color` == `rgb(240, 240, 240)`(gray-3 的字面读数;同时用 `resolve_color("--color-surface-page")` 做一次等值复核,证明它确实来自令牌而不是硬编码);
    - 用 `resolve_color` 分别解析三个令牌得到三档实测色:页面 = `--color-surface-page`、内陷面 = `--color-surface`、卡片 = `--color-surface-card`;用 check-05 的 `relative_luminance` 算出三个相对亮度,断言**严格递增**:`lum(页面) < lum(内陷面) < lum(卡片)`。用 `ok_true` 记 PASS/FAIL,并在 `info()` 里打印三个 rgb 值与三个亮度值(便于独立诊断);
    - 附一条对照组:三档两两之间都用 `contrast_ratio` 算出比值并打印(不判定)—— 这条只读诊断是给用户看「ΔL 到底有多小」的锚点,截图评审时会用到。

    **第 2 步 —— 追加断言集 `c5`(滚动契约保持)。**
    - `#doc-panel` 的计算 `overflow-y` == `auto`(`:615` 的声明必须存活 —— 它是右列的滚动者,L-1 的 sticky 表头依赖它仍是最近的可滚祖先);
    - `#chat-messages` 的计算 `overflow-y` == `auto`(`:983` 的声明必须存活 —— 输入行钉底靠它);
    - `#doc-panel-header` 的计算 `position` == `sticky` 且计算 `top` == `0px`;
    - 运行时证明 sticky 的**可滚前提**成立:在 `p1` 样本下 `#doc-panel` 的 `scrollHeight > clientHeight`(不足则先经应用自身的渲染路径把文档内容加长,再复查;仍不可滚则记 `blocked()`,**绝不**在不可滚的容器上断言「滚到底后表头仍可见」—— 那是空转断言)。前提成立后把 `#doc-panel.scrollTop` 设为其 `scrollHeight`,断言 `#doc-panel-header` 的 rect 仍落在 `#doc-panel` 的 rect 内,并在 `info()` 里打印滚动前后两个 rect。
    - 本任务**不重复** item 9 的滚动者集合普查(那一条已存在且更严:口径是「恰好」)。

    **第 3 步 —— 同步模块 docstring 的断言映射表与 `--item` help 文本**,把 `c3` / `c4` / `c5` 三组补进去(与 check-06 / check-07 的做法一致)。

    **第 4 步 —— 不触碰任何产品代码。** 本任务只改 `scripts/check-09-idi09-validation.py`,不碰 `frontend/style.css`、不碰 check-05 / check-06 / check-07 / probe-05 / probe-07。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c3 --item c4 --item c5</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or the trailing "exit=" line not "exit=0"</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>non-zero exit, or stdout not exactly "PASS"</fails_when>
    <automated>.venv/bin/python scripts/check-02-contrast.py</automated>
    <fails_when>non-zero exit, or any line beginning with "FAIL", or the final line not "PASS: 0 failures"</fails_when>
  </verify>
  <acceptance_criteria>
    - `.venv/bin/python scripts/check-09-idi09-validation.py --item c3` 断言 `body` 计算底色为 `rgb(240, 240, 240)`,并断言三档亮度严格递增,`exit=0`,0 FAIL / 0 BLOCKED。
    - 该命令的 INFO 行里可见三档的 rgb 读数与相对亮度读数,以及三档两两之间的对比度比值(只读诊断)。
    - `.venv/bin/python scripts/check-09-idi09-validation.py --item c5` 断言 `#doc-panel` 与 `#chat-messages` 的 `overflow-y` 均为 `auto`、`#doc-panel-header` 的 `position` 为 `sticky` 且 `top` 为 `0px`,并在**证明可滚前提成立后**断言滚到底时表头仍在面板可视区内;`exit=0`,0 FAIL / 0 BLOCKED。
    - `--item c3 --item c4 --item c5` 三条一起跑时 `exit=0`;模块 docstring 的断言映射表与 `--item` help 文本都已列出 c1…c5。
    - `git status --porcelain frontend/` 与 HEAD 相比无变化(本任务零产品代码改动);`bash scripts/check-01-token-conformance.sh` 与 `.venv/bin/python scripts/check-02-contrast.py` 仍全绿。
  </acceptance_criteria>
  <done>三层刻度的亮度序与 `body` 的 gray-3 底色由真实浏览器读数证明;`#doc-panel` / `#chat-messages` 的滚动契约与 sticky 表头在运行时成立;`check-09` 的 c1…c5 五组断言齐备且全绿。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 无外部输入边界 | 本阶段只改 `frontend/style.css` 的令牌值与密度取值:零用户输入处理、零鉴权、零数据访问、零网络调用、零新增资源加载。攻击面限于**浏览器对 CSS 的解析与渲染**,以及页面换值对既有层叠 / 定位几何的副作用 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-09-01 | Information Disclosure | `--color-surface-page` 换值 + 密度改值 | low | accept | 纯颜色与间距数值,不含 URL、不引入 `@import` / 远程字体 / `url()`;`git diff frontend/style.css` 中新增行不含 `url(` / `@import`。CSS 侧不存在数据外泄面 |
| T-idi-09-02 | Tampering | 页面换值对 `position: fixed` 元素的影响 | low | accept | 规划期已核实:全文件只有两处 `position: fixed`(`#stream-banner` `:872-885` 自带 `--color-surface-mark` 底色;`.overlay` `:808-816` 自带 `--color-overlay-backdrop`),两者都自足,不受页面底色换值影响。本计划不新增任何定位 / 层叠相关属性。探测器:`check-05 --item 8` 的 badge × banner 三宽度 rect 不相交断言(计划 03 复跑) |
| T-idi-09-03 | Tampering | 密度改值对既有几何的位移 | medium | mitigate | `.panel-body` 的 padding 由 10px 增至 16px 会使左栏 4 个面板各增高 12px,`#main-pane` 的 gap 由 6px 增至 12px 会使三处间隙各增 6px —— 左栏内容整体下移约 66px。风险是「AI 面板展开时把会话流压得很矮」与窄窗口下的换行。缓解:`#session-panel` 的 `flex: 1 1 auto` 与 `min-height: 200px` 逐字未动(它会吸收增量);`#doc-panel-body` 的 32/40 内边距与 `#doc-panel` 的宽度令牌逐字未动,故右栏几何零变化。探测器:`check-05 --item 9`(末条内容可达 + 滚动者集合恰好)、`check-06` g5(340px 最窄面板单行 / 不裁切)、`check-05 --item 10`(24×24 命中区)在计划 03 复跑 |
| T-idi-09-04 | Elevation of Privilege | 无 | low | accept | 本阶段不触碰鉴权、权限门、服务端路径或任何 API;纯呈现层改动,无提权面 |
| T-idi-09-SC | Tampering | npm / pip / cargo 安装 | low | accept | 本阶段**零安装**:零新增依赖、零构建步骤(DESIGN.md D-06)。`frontend/vendor/` 仍只有 `marked.min.js`,无供应链面进入 |
</threat_model>

<verification>
**静态门(全部必须绿):**

- `bash scripts/check-01-token-conformance.sh` → `PASS`(`--color-surface-page` 换值后围栏外仍零裸 `#hex`、零 tier-1 原语引用)
- `.venv/bin/python scripts/check-02-contrast.py` → `PASS: 0 failures`;8 条受影响配对的实测值 = 14.30 / 5.19 / 5.19 / 5.15 / 5.19 / 4.18 / 4.77 / 3.32;ORDER 行仍为 `ORDER 0.363`
- `bash scripts/check-03-hidden-uniqueness.sh` → `PASS`
- `bash scripts/check-04-important-count.sh` → `PASS`

**运行时门(本计划扩写):**

- `.venv/bin/python scripts/check-09-idi09-validation.py --item c3 --item c4 --item c5` → `exit=0`,0 FAIL / 0 BLOCKED
  - `c3`:`body` 计算底色 `rgb(240, 240, 240)`;三档亮度严格递增(页面 < 内陷面 < 卡片)
  - `c4`:`#main-pane` gap `12px`;`.panel-body` padding `16px`;`#doc-panel-body` padding `32px 40px`(对照);`.panel-header` padding-top `6px`(对照)
  - `c5`:`#doc-panel` / `#chat-messages` 的 `overflow-y` 均为 `auto`;`#doc-panel-header` `position: sticky` / `top: 0px`;可滚前提下滚到底表头仍可见

**仓库卫生:**

- `git status --porcelain frontend/` 仅列出 `frontend/style.css`
- `git diff scripts/check-02-contrast.py` 为空;`git diff -U0 frontend/style.css` 的输出里 `--radix-` 增删行仅有 `--color-surface-page` 那一行
- `ls frontend/vendor/` 仅 `marked.min.js`
</verification>

<success_criteria>
- 页面底色为 `--radix-gray-3`(#f0f0f0),`body` 的计算底色为 `rgb(240, 240, 240)`;屏幕上同时可见的三档顺序正确:gray-3(页面)< gray-2(`--color-surface`,控件内陷面)< 白(卡片)。
- 画在 `--color-surface-page` 上的 6 条 PAIR 以新底色**重算并登记**(不是刷新旧值),登记值与 `check-02` 的运行时实测逐位一致;2 条 FAIL 的重新归属链条在登记段完整可核。
- 卡片间距 12px、左栏面板内边距 16px,均以真实浏览器的计算几何证明;`#doc-panel-body` 与 `.panel-header` 的内边距逐字未动。
- `#doc-panel` / `#chat-messages` 的滚动契约与 `#doc-panel-header` 的 sticky 行为在运行时保持。
- 零颜色值改动、零 primitive 改动、零阈值放宽、零 PAIR 条目增删;清单规模仍为 53 对 + 1 条 ORDER。
- `frontend/app.js` / `frontend/index.html` / `frontend/vendor/` 零字节改动;`scripts/check-05-ui-uat.py` 本计划零改动。
</success_criteria>

<output>
Create `.planning/phases/idi-09-card-containers/idi-09-02-SUMMARY.md` when done
</output>

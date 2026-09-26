---
phase: idi-09-card-containers
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - frontend/style.css
  - scripts/check-09-idi09-validation.py
  - scripts/check-05-ui-uat.py
autonomous: true
requirements:
  - VIS-01
  - VIS-02
  - CARD-01
  - CARD-02
  - REG-01

estimate:
  tokens: 45000
  raw_tokens: 45000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- CARD-01 / CARD-02 — rendered, not textual ----
    - "左栏 4 个 section(`#session-panel` / `#annotations-panel` / `#checks-panel` / `#ai-panel`)在真实浏览器里各自的计算 `background-color` 等于运行时解析的 `--color-surface-card`(`rgb(255, 255, 255)`);不再是 v1.14 收口时的 `rgba(0, 0, 0, 0)` 完全透明"
    - "左栏 4 个 section 的计算 `border-top-left-radius` 等于运行时解析的 `--radius-md`(10px),计算 `border-top` 为 `1px solid`,计算 `box-shadow` 非 `none`"
    - "右栏 `#doc-panel` 的计算 `background-color` 同样等于 `--color-surface-card`,四边边框均为 `1px solid`,圆角等于 `--radius-md`,阴影非 `none` —— 原有的 `border-left: 1px` 单边凹陷读感被同族卡片语言取代"
    - "`#doc-panel-header` 的计算 `background-color` 与卡片底色同值(白),sticky 遮挡机制因此保持:滚动 `#doc-panel` 时表头仍遮住从其下穿过的正文,不再是一条比卡片更暗的条带"
    - "`#doc-panel` 的计算 `overflow-y` 仍为 `auto` —— 它是右列的滚动者,L-1 的 sticky 表头依赖它仍是最近的可滚祖先;本计划不得删除它"
    # ---- VIS-01 / VIS-02 ----
    - "`--color-surface-card` 与 `--shadow-card` 声明在围栏 `:root` 内;`bash scripts/check-01-token-conformance.sh` 打印 `PASS`(围栏外裸 `#hex` 计数 0、tier-1 原语引用计数 0)"
    - "`--shadow-card` 的声明值是 `0 1px 2px rgba(0, 0, 0, 0.04)`(用户裁定值,D-9-3),且以 `box-shadow` 呈现 —— 零位移、不参与布局;卡片规则内不得出现 `margin` / `position` 模拟浮起"
    - "卡片圆角取自既有 `--radius-md`,零新增圆角值;`--color-surface-card` 是 `var(--white)` 的别名,零新增 tier-1 原语(`--white` 已在 `style.css:47` 声明)"
    - "卡片规则内不含任何建立「fixed 定位包含块」或新层叠上下文的属性(`transform` / `filter` / `will-change` / `contain` / `perspective` / `opacity` / `position` / `z-index` / `overflow`)—— `#stream-banner` 是 `#doc-panel` 的后代且 `position: fixed`,上述任一属性都会把它钉到卡片上而不是视口"
    # ---- REG-01 — the manifest's ground, re-attributed not recoloured ----
    - "`/* PAIR --color-marker-active ON --color-surface-card TEXT */` 与 `/* PAIR --color-border-strong ON --color-surface-card NON-TEXT */` 已登记;`check-02` 打印 `PASS  4.77` 与 `PASS  3.32` 两行,全清单 0 failures"
    - "全程未改动任何 `--radix-*` 原语值、未改动任何 tier-2 颜色值、未新增 primitive、未放宽 `scripts/check-02-contrast.py` 的 `TEXT_MIN` / `NON_TEXT_MIN`、未删除任何 PAIR 条目(清单规模不变:53 对 + 1 条 ORDER = 54 条清单条目)"
    - "`--color-marker-active` 的 NON-TEXT 半条保留在 `--color-surface-page` 地面并**带注释登记**其物理绘制面是卡片:该条与 TEXT 半由同一元素族绘制,保留页面地面是刻意的保守读数(4.18 < 卡片的 4.77),不是遗漏"
    # ---- gates ----
    - "`bash scripts/check-03-hidden-uniqueness.sh` 打印 `PASS`(`^[[:space:]]*\\.hidden[[:space:]]*\\{` 计数 == 1)"
    - "`bash scripts/check-04-important-count.sh` 打印 `PASS`(`!important;` **声明**计数 == 1;本计划新增的注释不得包含该字面量)"
    - "`.venv/bin/python scripts/check-09-idi09-validation.py --item c1` / `--item c2` 在真实浏览器里全 PASS(0 FAIL / 0 BLOCKED),`exit=0`"
    - "`.venv/bin/python scripts/check-05-ui-uat.py --item 5 --browser bundled` 的输出中 item 5 的 FAIL 计数为 0(`.hint` 实际背景断言已按新事实重新登记期望侧,断言强度不变)"

  artifacts:
    - path: "frontend/style.css"
      provides: "围栏内新增 `--color-surface-card` / `--shadow-card`;`#main-pane > section` 与 `#doc-panel` 就地扩写为卡片规则;`#doc-panel-header` 的 background 改指卡片令牌;2 条 PAIR 的地面改记为 `--color-surface-card` 并附承重注释"
      contains: "--color-surface-card: var(--white);"
    - path: "scripts/check-09-idi09-validation.py"
      provides: "Phase 9 的卡片语言运行时门:真实浏览器 `getComputedStyle` 读数断言 c1(左栏 4 个 section)/ c2(`#doc-panel`)+ `--item` 选择 + `--screenshot DIR` 出图;复用 check-05 的模块级设施(服务生命周期 / fixture / 断言记录器)"
      contains: "def main"
    - path: "scripts/check-05-ui-uat.py"
      provides: "`.hint` 实际背景断言的期望侧由 `--color-surface` 重新登记为 `--color-surface-card`(同一等值断言,期望侧换指到本阶段改动的真实事实),及其上方注释的事实更新"
      contains: "effective_bg(page, \".hint\")"

  key_links:
    - from: "`frontend/style.css` 围栏内的 `--color-surface-card`"
      to: "`#main-pane > section` / `#doc-panel` / `#doc-panel-header` 的 `background`"
      via: "var() 引用 —— 三处消费者全部落在围栏外,围栏外只写令牌名不写字面量"
      pattern: "background: var\\(--color-surface-card\\);"
    - from: "`frontend/style.css` 围栏内的 `--shadow-card`"
      to: "`#main-pane > section` 与 `#doc-panel` 的 `box-shadow`"
      via: "零位移的普通 box-shadow,不参与布局"
      pattern: "box-shadow: var\\(--shadow-card\\);"
    - from: "`#main-pane > section` 的 `border-radius: var(--radius-md)`"
      to: "`.panel-header` 既有的 `border-radius: var(--radius-md)`(`style.css:679`)"
      via: "同值 —— 表头自身四角已圆,故不会把卡片四角顶成方角;左栏卡片无需 `overflow: hidden`"
      pattern: "border-radius: var\\(--radius-md\\);"
    - from: "`#doc-panel` 既有的 `overflow-y: auto`(`style.css:615`)"
      to: "`#doc-panel-header` 的 sticky 遮挡"
      via: "滚动容器把后代裁剪到带圆角的 padding box —— 表头因此无需自己带圆角,`border-radius: 0` 保持一字不动"
      pattern: "overflow-y: auto;"
    - from: "`/* PAIR --color-marker-active ON --color-surface-card TEXT */`"
      to: "`#session-panel` / `#annotations-panel` / `#checks-panel` 的 `.panel-header h2`(`style.css:1431-1435`)"
      via: "卡片化后标题确实画在白卡片上;旧地面 `--color-surface-page` 只在面板透明时成立"
      pattern: "PAIR --color-marker-active ON --color-surface-card TEXT"
    - from: "`/* PAIR --color-border-strong ON --color-surface-card NON-TEXT */`"
      to: "`#project-path-input` / `#chat-input-row input` / `#enter-form input[type=\"text\"]` 的静止边框"
      via: "这些 input 不声明 background ⇒ Chrome 画 UA 字段填充(白),边框实际画在白上 —— 本文件 `style.css:538-541` 已登记这一事实"
      pattern: "PAIR --color-border-strong ON --color-surface-card NON-TEXT"

  prohibitions:
    - statement: "不得改任何 `--radix-*` 原语的值,尤其不得动 `--radix-blue-11`(`--color-marker-active` 的背书)与 `--radix-gray-9`(`--color-border-strong` 的背书)。二者分别被多处 tier-2 令牌消费,改值会连锁改掉它们的**全部**其他配对;而且 `check-01` 的硬不变式禁止围栏外引用 tier-1 原语,`--radix-blue-11` 背后还挂着 `style.css:161-168` 已登记的「最薄余量 0.15,不要『求稳』加深」警告"
      status: active
      verification: flagged
    - statement: "不得放宽 `scripts/check-02-contrast.py` 的 `TEXT_MIN`(4.5)/ `NON_TEXT_MIN`(3.0),不得改动该脚本的任何一行,不得删除或注释掉任何 `/* PAIR */` 条目。放宽阈值是「把门改小以让结论成立」,本仓库明令禁止;删除条目会同时打破脚本的覆盖地板(≥24 对 / ≥20 TEXT / ≥4 NON-TEXT)与 `raw_pairs == len(pairs)` 的标记计数一致性检查"
      status: active
      verification: flagged
    - statement: "不得给卡片规则加 `overflow`(尤其 `overflow: hidden`)。左栏 4 个 section 的圆角由 `.panel-header` 自身的 `border-radius: var(--radius-md)` 承担,无需裁剪;加 `overflow: hidden` 会裁剪子元素并可能切断 `:focus-visible` 的 2px 焦点环 —— `check-05` item 10 断言「判定集里未被环覆盖的元素数为 0」,被裁掉的环会让那条门红"
      status: active
      verification: flagged
    - statement: "不得给卡片规则加 `transform` / `filter` / `will-change` / `contain` / `perspective` / `opacity` / `position` / `z-index`。前六个会建立「fixed 定位包含块」或新层叠上下文,把 `#stream-banner` 钉到卡片上而不是视口(`#stream-banner` 是 `#doc-panel` 的后代且 `position: fixed`,见 `frontend/index.html:101` 与 `frontend/style.css:872-885`),并把它的 `z-index: var(--z-banner)` 关进 `#doc-panel` 的层叠上下文里。**注意边界**:`.overlay` 两个弹窗与 `#selection-menu` 都在 `#doc-panel` 之外(`frontend/index.html:207/238/249`),本阶段不会改变它们的层叠关系 —— 不要把它们写成本项的风险。`check-05` item 8 的 badge × banner 三宽度 rect 不相交断言是这条禁令的探测器"
      status: active
      verification: flagged
    - statement: "不得移动任何既有规则块的位置(硬规则 3:追加,不重排)。至少一对等特异性规则由源码顺序决定(例:`.chat-ai` 与 `.chat-bubble` 同为 0-1-0,`style.css:1017-1019` 的注释逐字登记了这条依赖)。本计划的全部改动都是**就地扩写既有规则体**(选择器位置与源码顺序逐字不变)+ 围栏内新增两行声明,没有任何新增规则块插到既有规则之前"
      status: active
      verification: flagged
    - statement: "不得改动 `#doc-panel-body` 的 `padding: var(--space-8) var(--space-10)`(`style.css:665`)。它是阅读列的呼吸空间,且 `check-05` 有活断言 `[p1] #doc-panel-body padding == \"32px 40px\"`(item 3);本计划的密度改动只落在 `.panel-body`(左栏 4 个面板的正文容器),`#doc-panel-body` 不带 `.panel-body` 类,两者互不影响"
      status: active
      verification: flagged
    - statement: "不得改动 `frontend/app.js` / `frontend/index.html` / `frontend/vendor/`(零字节);不得新增依赖、构建步骤、CSS 框架或任何新的 CSS/JS 文件(唯一允许的新文件是 `scripts/check-09-idi09-validation.py`,它属验证工具而非应用代码);不得在 `frontend/style.css` 里新增 `@layer` / `@property` / `var(--x, #fallback)` / 媒体查询 / `!important`"
      status: active
      verification: flagged
    - statement: "不得在 `frontend/style.css` 的任何注释里写字面量 `!important;`。`check-04` 按**出现次数**数 `!important;`,散文注释会把计数从 1 顶高(本项目已因此红过三次)。同理,写在围栏外的注释不得含裸 `#hex` 或 `var(--radix-…` / `var(--white)` —— `check-01` 扫的是围栏外全文"
      status: active
      verification: flagged
---

<objective>
让界面首次拥有 elevation 层次:把左栏 4 个 section 与右栏文档区从「裸贴页面底色 / 完全透明」改成**白底卡片容器**(白底 + 可见边界 + 圆角 + 极轻阴影),并把这条改动端到端接进一个真实浏览器的运行时门。

Purpose: `09-CONTEXT.md` 的规划期实测给出了「平 / 丑」的机械成因 —— 页面 `#fcfcfc` 是全场最亮,左栏 3 个面板的计算底色是 `rgba(0, 0, 0, 0)`(**完全透明**),`#doc-panel` 是比页面更暗的 gray-2 且**零圆角零阴影**,全场零阴影。这是**构图**问题,不是配色问题,所以本阶段不动任何颜色值,只补容器层次。用户已裁定底色关系取「页面下沉 + 白卡片」(D-9-1,PROJECT.md Key Decisions),卡片密度取紧凑档(D-9-2),阴影取极轻档(D-9-3),**本阶段不重开这三项决策**。

本计划只做**卡片语言**(白底 / 边界 / 圆角 / 阴影)与随之而来的**对比度地面重新归属**。页面底色下沉(CARD-03)与密度(内边距 / 间距)分别落在计划 02 —— 页面换值会作废画在它上面的 8 条 PAIR,那是独立可验的一步,单独成波次才能在门红时定位到它。

Output: `frontend/style.css` 围栏内两个新令牌(`--color-surface-card` / `--shadow-card`)、`#main-pane > section` 与 `#doc-panel` 就地扩写为卡片规则、`#doc-panel-header` 底色跟随卡片、2 条 PAIR 的地面重新归属;新增运行时门 `scripts/check-09-idi09-validation.py`;`scripts/check-05-ui-uat.py` 的 `.hint` 断言期望侧按新事实重新登记。

**基线口径(磁盘 HEAD 是唯一现实基线)。** 本计划的每一个「现状」值都取自 `frontend/style.css` 的磁盘内容(1708 行)与 `scripts/check-05-ui-uat.py` 的断言。**行号锚点一律以选择器文本为准**;下面给出的行号是规划期实测,执行器须以选择器文本复核后再动手。

**一处须以磁盘为准的口径差(规划期实测,勿被文档带偏):** `09-CONTEXT.md` 与 ROADMAP 写作「现有 **54** 条 PAIR」,而磁盘实测是 **53** 条 `/* PAIR */` 标记 + **1** 条 `/* ORDER */` 标记 —— 那 54 是把两者合起来数的**清单条目**数。判据一律取磁盘计数:`grep -o '/\* PAIR' frontend/style.css | wc -l` == 53,`grep -o '/\* ORDER' frontend/style.css | wc -l` == 1。其中画在 `--color-surface-page` 上的恰好 **8** 条(`:455/465/470/514/523/526/542/562`),与文档一致。TEXT / NON-TEXT 分解为 35 / 18(与 `check-02` 覆盖地板 20 / 4 对照)。

**执行前基线(规划期已实测,执行器须复核):**

| 门 | 规划期在 HEAD 上的实测结果 |
|---|---|
| `bash scripts/check-01-token-conformance.sh` | `PASS` / exit 0 |
| `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`(53 对 = 35 TEXT + 18 NON-TEXT,加 1 条 ORDER = 54 条清单条目) |
| `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` |
| `bash scripts/check-04-important-count.sh` | `PASS` |
| `.venv/bin/python scripts/check-05-ui-uat.py --item 5 --browser bundled` | item 5 FAIL 计数 0;两条 `--ai-smoke` 腿 BLOCKED ⇒ `exit=2`(设计如此) |
| `.venv/bin/python -m pytest backend/tests -q --tb=short` | `219 passed, 6 skipped`(必须用项目 `.venv`) |

**本计划会打破的既有断言(规划期已逐条普查,恰好 1 条,已在本计划内重新登记)。** `scripts/check-05-ui-uat.py` 的 `[p1] .hint 实际背景 == var(--color-surface)`(`:1305`):`.hint` 自身无背景,该断言经 `effective_bg()` 沿祖先链取到的最近不透明祖先是 `#doc-panel`。本计划把 `#doc-panel` 的底色改为卡片白之后,该断言必然红 —— 它断言的**事实**被本阶段刻意改变了。处置:把期望侧从 `--color-surface` 换指到 `--color-surface-card`,断言形式(与运行时解析的令牌做精确等值)一字不变。**不得**改成「非透明」「包含 rgb(255」之类的弱化写法。除此之外,`check-05` / `check-06` / `check-07` / `probe-05` / `probe-07` 的其余断言**没有任何一条**触及五个容器的 `background` / `border` / `border-radius` / `box-shadow`(规划期逐条 grep 确认):`check-05` item 3 断言的是 `#doc-panel-body padding`(不动)、`.panel-header padding-top`(不动)、`button padding-top`(不动)、`.overlay-card padding-top`(不动);`check-06` g3 的 `radiusTL` 是 `info()` 观察项;`check-05` item 2 的 `#round-doc` 正文对比度用 `effective_bg("#round-doc")`,卡片化后地面由 gray-2 变白,比值**上升**,断言(≥4.5)仍绿。

**本计划关闭的需求:** VIS-01、VIS-02、CARD-01、CARD-02、REG-01(REG-01 的页面换值半边由计划 02 关闭)。**本计划不触碰:** CARD-03(页面底色)与 D-9-2 的密度值(计划 02);`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` 零字节改动;`scripts/check-01…04` / `check-06` / `check-07` / `probe-05` / `probe-07` 代码零改动;表格重做 / 圆角刻度收敛 / 图标与空状态 / `.overlay-card` 底色(REQUIREMENTS.md Out of Scope,用户裁定「先看看效果」)。

**为什么三个计划串行而非并行。** 本阶段的改动面是单一文件 `frontend/style.css` 加两个验证脚本;`execute-phase` 的同波次规则要求同波次计划的 `files_modified` 零重叠,故三个计划必须落在三个波次。这不是本阶段可以优化的地方 —— 它是「纯 CSS 阶段」的定义。
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
@frontend/style.css
@frontend/index.html
@scripts/check-05-ui-uat.py
</context>

## Artifacts this phase produces

> 本节的用途:**plan-review-convergence 的 source-grounding pass 读它,把本阶段新建的符号从漂移校验里排除**。
> 本节列出**全阶段**(三个计划)的产出;每个计划的 SUMMARY 只登记自己那部分。

**新增 CSS 自定义属性(围栏 `:root` 内,全部由本阶段创建):**

| # | 符号 | 值 | 计划 | 备注 |
|---|---|---|---|---|
| 1 | `--color-surface-card` | `var(--white)` | 01 | tier-2;`--white` 已在 `style.css:47` 声明 ⇒ **零新增 tier-1 原语** |
| 2 | `--shadow-card` | `0 1px 2px rgba(0, 0, 0, 0.04)` | 01 | tier-2;用户裁定值(D-9-3);零位移 |

**新增文件:**

| # | 路径 | 计划 | 备注 |
|---|---|---|---|
| 3 | `scripts/check-09-idi09-validation.py` | 01(骨架 + c1)/ 02(c3 / c4 / c5) | Phase 9 的运行时门;复用 check-05 的模块级设施,不重写服务生命周期 |
| 4 | `.planning/phases/idi-09-card-containers/screenshots/*.png` | 03 | 供用户评审的截图(ROADMAP Deliverables 的最后一项) |

**就地扩写的既有规则(规则块位置与源码顺序逐字不变):**

| # | 符号 | HEAD 位置 | 计划 | 动作 |
|---|---|---|---|---|
| 5 | `#main-pane > section` | `:605-608` | 01 | 加 `background` / `border` / `border-radius` / `box-shadow` |
| 6 | `#doc-panel` | `:611-624` | 01 | `border-left` → `border`;`background` → 卡片令牌;加 `border-radius` / `box-shadow` |
| 7 | `#doc-panel-header` | `:649-654` | 01 | `background` → 卡片令牌;`border-radius: 0` 一字不动;上方注释事实更新 |
| 8 | `#main-pane` | `:590-603` | 02 | `gap` 由 `--space-1-5`(6px)改为 `--space-3`(12px) |
| 9 | `.panel-body` | `:688` | 02 | `padding` 由 `--space-2-5`(10px)改为 `--space-4`(16px) |
| 10 | `--color-surface-page`(围栏内声明) | `:122` | 02 | `var(--radix-gray-1)` → `var(--radix-gray-3)` |

**PAIR 清单改动(围栏内):**

| # | 符号 | HEAD 位置 | 计划 | 动作 |
|---|---|---|---|---|
| 11 | `PAIR --color-marker-active ON --color-surface-page TEXT` | `:523` | 01 | 地面改记为 `--color-surface-card`(4.77) |
| 12 | `PAIR --color-border-strong ON --color-surface-page NON-TEXT` | `:526` | 01 | 地面改记为 `--color-surface-card`(3.32) |
| 13 | 画在 `--color-surface-page` 上的其余 6 条(文本 / secondary / muted / focus / border-hover / marker-active NON-TEXT) | `:455/465/470/514/542/562` | 02 | 条目名逐字不变;以 gray-3 重算比值并**登记**到清单历史段(不是刷新旧值) |
| 14 | 清单历史段新增 Phase 9 一段 | `:427-452` | 01 / 02 | 01 记地面重新归属;02 记 8 条的重算前后值 |

**明确不产生的新符号:** 零新增 tier-1 颜色原语、零新增圆角值、零新增 `--space-*` 刻度值、零新依赖、零构建步骤、零新 CSS/JS 应用文件、`frontend/app.js` / `index.html` / `vendor/` 零字节改动。

## 波次与依赖形状(本阶段的真实约束,不是保守)

| 波次 | 计划 | 落点 | 为什么必须在这个位置 |
|---|---|---|---|
| 1 | `idi-09-01`(本计划) | 卡片令牌 + 五个容器的卡片语言 + 2 条 PAIR 重新归属 + 运行时门 c1 / c2 | 卡片语言是页面换值的**前提**:`--color-surface-page` 一换值,画在它上面的 8 条 PAIR 全部失效;其中 2 条(中间调前景)会直接跌破阈值。它们今天的正解是「重新归属到卡片地面」,而卡片地面必须**先存在**。反过来,先换页面再补卡片会让 `check-02` 在中间态红着 |
| 2 | `idi-09-02` | 页面底色下沉 + 6 条 PAIR 重算登记 + 密度 | 页面换值是 CARD-03 本身,且是唯一会作废 8 条 PAIR 的动作;必须能看到波次 1 的全部卡片改动才动它。密度(16px / 12px)是独立的取值改动,判据是几何而非颜色 |
| 3 | `idi-09-03` | 五条浏览器门复跑 + pytest 基线 + 截图 | 回归门必须看到波次 1/2 的全部改动。`check-05` 是 228KB 的真实浏览器 UAT,它断言 computed style 与几何 —— 只有它能在「卡片化 + 页面下沉」全部落地后证明渲染语义仍然成立 |

<tasks>

<task type="tracer">
  <name>Task 1 (tracer): 卡片令牌端到端 —— 围栏两行声明 → 左栏 4 个 section 的卡片规则 → 真实浏览器 computed style → 运行时门 c1</name>
  <files>frontend/style.css, scripts/check-09-idi09-validation.py</files>
  <reversibility rating="costly">回退是删围栏内两行 + 还原一条规则体的四条声明,单文件即可完成;但本计划同时新建了 `scripts/check-09-idi09-validation.py` 并把它接进后续两个计划的验收,回退需连带删除该脚本与计划 02 对它的扩写,故评级 costly 而非 reversible。</reversibility>
  <read_first>
    - `frontend/style.css` 围栏段 —— `/* ===== DESIGN TOKENS: START ===== */`(`:5`)到 `/* ===== DESIGN TOKENS: END ===== */`(`:568`)。重点读:`--white: #ffffff;`(`:47`)、`--radix-gray-1/2/3`(`:48-50`)、tier-2 声明区(`:118-289`)、`--color-surface-page: var(--radix-gray-1);`(`:122`)、`--color-surface: var(--radix-gray-2);`(`:183`)、`--color-border-subtle: var(--radix-gray-6);`(`:233`)、`--color-border-strong: var(--radix-gray-9);`(`:215`)、`--shadow-composer` / `--shadow-overlay`(`:284-285`,**新阴影令牌就声明在这一组之后**)、`--radius-sm/md/lg/pill`(`:353-356`)、`--space-1-5` / `--space-2-5` / `--space-3` / `--space-4`(`:295-300`)
    - `frontend/style.css` 清单段 `:416-566` —— 清单头部注释(阈值 4.5 / 3.0、覆盖地板 24/20/4、`raw_pairs` 计数一致性)、`--color-marker-active` 的 tier-2 声明与其上方 `:147-168` 的「最薄余量 0.15,不要求稳加深」警告、`:517-523`(marker-active TEXT 半的地面说明)、`:525-527`(非文本边界组)、`:528-541`(**UA 字段填充为白、静止边界在白上 = 3.32** 的既登记事实)、`:559-562`(marker-active NON-TEXT 半的地面说明)、`:564-566`(ORDER 条)
    - `frontend/style.css` `html, body { … background: var(--color-surface-page); … }`(`:570-576`)—— 页面底色的唯一消费者,**本计划不动**
    - `frontend/style.css` `.hidden { display: none !important; }`(`:578-582`)—— 全站唯一一条 `!important` 声明及其承重注释;**本计划不动**
    - `frontend/style.css` `#app { display: flex; height: 100vh; }`(`:584-587`)
    - `frontend/style.css` `#main-pane { … gap: var(--space-1-5); overflow-y: auto; align-items: center; min-width: 0; }`(`:590-603`)—— 只读,密度改动在计划 02
    - `frontend/style.css` `#main-pane > section { width: 100%; max-width: 768px; }`(`:605-608`)—— **本任务就地扩写的目标规则**
    - `frontend/style.css` `#doc-panel`(`:611-624`)与 `#doc-panel.collapsed`(`:626-629`)—— 只读,`#doc-panel` 的卡片化在 Task 2
    - `frontend/style.css` `.panel-header { … height: 36px; padding: var(--space-1-5) var(--space-2-5); border-radius: var(--radius-md); … }`(`:673-682`)—— **注意它体内没有任何 `background`**,且圆角已是 `--radius-md`:这是左栏卡片不需要 `overflow: hidden` 的依据
    - `frontend/style.css` `#session-panel:not(.hidden) .panel-header { box-shadow: inset 3px 0 0 var(--color-marker-active); }` 与紧随的 h2 规则(`:1426-1435`)—— `--color-marker-active` 的**全部**消费者,二者都在 `.panel-header` 内 ⇒ 卡片化后画在白卡片上
    - `frontend/index.html` `:12-79` —— `main#main-pane` 的 4 个 `<section>`(`#session-panel` / `#annotations-panel` / `#checks-panel` / `#ai-panel`)与它们各自的 `header.panel-header` + `div.panel-body`;`:82-92` 的 `aside#doc-panel` > `header.panel-header#doc-panel-header` + `div#doc-panel-body`(**注意 `#doc-panel-body` 不带 `.panel-body` 类**)
    - `scripts/check-05-ui-uat.py` `:86-300` —— 断言记录器与工具全文:`_emit` / `ok`(expected 为 `None` ⇒ `<UNRESOLVED>` BLOCKED;actual 为 `None` ⇒ `<MISSING>` BLOCKED)/ `norm` / `ok_true` / `blocked` / `info` / `item_verdict` / `relative_luminance` / `contrast_ratio` / `read_style` / `resolve_color` / `resolve_token` / `effective_bg` / `make_fixture` / `enter_project`。**两处 BLOCKED 方向都是承重的,新门必须用满**
    - `scripts/check-05-ui-uat.py` `:4020-4110` —— `main()` 的派发与汇总格式(`item N: VERDICT  (n 条断言,f FAIL,b BLOCKED)` + `exit={code}`,0=全 pass / 1=有 fail / 2=有 blocked)
    - `scripts/check-06-idi05-validation.py` 文件头 `:1-60` 与 `:200-250` —— **本任务要照抄的复用模式**:用 `importlib.util.spec_from_file_location` 加载 check-05 为模块、复用其服务生命周期 / fixture / 断言 API,而不重复实现、不改动 check-05 一行
    - `.planning/phases/idi-09-card-containers/09-CONTEXT.md` —— 已裁定的三项设计值(D-9-1 / D-9-2 / D-9-3)、规划期实测的容器现状表、对比度影响面表
    - `.planning/ROADMAP.md` §`### Phase 9:` —— Goal / Deliverables / 5 条 Success Criteria / Pitfalls / Gates
  </read_first>
  <action>
    **第 1 步 —— 围栏内声明两个新令牌。**

    位置:紧接 `--shadow-overlay: 0 8px 30px rgba(0, 0, 0, 0.2);`(`:285`)之后,同一组阴影/遮罩令牌段内。逐字两行声明:`--color-surface-card: var(--white);` 与 `--shadow-card: 0 1px 2px rgba(0, 0, 0, 0.04);`。

    两行上方必须带一段承重注释,逐条记下五件事(缺一即会被读成任选):(a) 卡片底色的**关系**是用户裁定的三级刻度 —— 页面 gray-3 < `--color-surface`(gray-2,控件内陷面)< 白(卡片),对应 shadcn 的 canvas / inset / raised 三档(D-9-1,PROJECT.md Key Decisions,不重开);(b) 阴影值是用户裁定值(D-9-3),强度几乎不可见,层次主要靠边框 + 底色差(ΔL≈6%);(c) 阴影必须**零位移**,是普通 `box-shadow`,不得用 `margin` / `position` 模拟浮起;(d) **圆角不在这里** —— 卡片圆角取自既有 `--radius-md`(VIS-02:不引入新圆角值);(e) `--color-surface-card` 是 `var(--white)` 的别名,`--white` 已在 `:47` 声明 ⇒ 本阶段**零新增 tier-1 原语**。注释写在围栏内,故裸 `#hex` 合法,但仍优先写令牌名。

    **第 2 步 —— 就地扩写 `#main-pane > section`(`:605-608`)。**

    在既有的 `width: 100%;` 与 `max-width: 768px;` 之后追加四条声明,逐字:`background: var(--color-surface-card);` / `border: 1px solid var(--color-border-subtle);` / `border-radius: var(--radius-md);` / `box-shadow: var(--shadow-card);`。

    **选择器文本与规则块位置逐字不变** —— 这是「追加,不重排」的落地形态:改动是既有规则体就地扩写,源码顺序不变,没有任何新增规则块插到既有规则之前。边界色取 `--color-border-subtle`(gray-6)是**刻意零新增令牌**的选择:它已经是 `#doc-panel`(`:616`)与 `.event-list`(`:760`)的容器边界色,即既有容器边界语言;不得顺手改成别的令牌,也不得新声明一个卡片边界令牌。

    规则体上方必须带一段注释,记下三件事:(a) 边界色复用既有容器边界令牌 ⇒ 零新增令牌;(b) **禁止**在本规则内出现 `transform` / `filter` / `will-change` / `contain` / `perspective` / `opacity` / `position` / `z-index` / `overflow` —— 前六个会建立「fixed 定位包含块」或新层叠上下文,把 `#stream-banner`(`#doc-panel` 的后代、`position: fixed`、`z-index: var(--z-banner)`)钉到卡片上而不是视口;`overflow: hidden` 会裁剪 `:focus-visible` 的 2px 焦点环(左栏卡片**不需要**它,因为 `.panel-header` 自身的圆角已是 `--radius-md`,不会把卡片四角顶成方角);(c) 阴影是 `--shadow-card`,零位移。

    **第 3 步 —— 新建 `scripts/check-09-idi09-validation.py`(本任务的运行时门)。**

    结构照抄 `scripts/check-06-idi05-validation.py`:文件头 docstring 用中文写明「为什么另开一个文件」(既有五条门里没有任何一条断言五个容器的 `background` / `border` / `border-radius` / `box-shadow` —— 需求 CARD-01 / CARD-02 / CARD-03 的渲染判据在本文件之前**零自动化覆盖**)、运行方式、退出码语义(0=全 pass / 1=至少一条 FAIL / 2=无 FAIL 但有 BLOCKED,与 check-05 一致)、以及本文件断言与需求的映射表。

    用 `importlib.util.spec_from_file_location` 把 `scripts/check-05-ui-uat.py` 加载为模块,复用其 `ensure_server` / `make_fixture` / `enter_project` / `read_style` / `resolve_color` / `resolve_token` / `ok` / `ok_true` / `blocked` / `info` / `ROWS` / `item_verdict`。**不得改动 `scripts/check-05-ui-uat.py` 的这一部分**(本计划对它的唯一改动在第 4 步,是断言的期望侧)。

    断言集 `c1`(本任务落地;样本 `p1`,左栏 4 个 section 在 `p1` 下全部存在,`getComputedStyle` 对 `display: none` 的元素同样返回解析值,故无需为每个面板切样本 —— 与 check-05 item 9 读 `#annotation-list` 同一依据)。对 `#session-panel` / `#annotations-panel` / `#checks-panel` / `#ai-panel` 四个选择器逐一:
    - 计算 `background-color` == `resolve_color("--color-surface-card")`;
    - 计算 `border-top-left-radius` == `resolve_token("--radius-md")`(证明圆角取自既有刻度,零新增值);
    - 计算 `border-top-width` == `1px` 且 `border-top-style` == `solid`;
    - 计算 `box-shadow` != `none`,且其字符串包含 `rgba(0, 0, 0, 0.04)`、水平偏移为 `0px`(零位移,VIS-02);用 `info()` 打印原始读数以便独立诊断。
    另加两条令牌级断言:`resolve_token("--shadow-card")` == `0 1px 2px rgba(0, 0, 0, 0.04)`;`resolve_color("--color-surface-card")` == `rgb(255, 255, 255)`。

    每条断言一律走 `ok` / `ok_true`:元素读不到(`read_style` 返回 `None`)或令牌解析不出(`resolve_*` 返回 `None`)时自动落进 BLOCKED 分支,**绝不记 PASS**。断言标签里带选择器名与样本名。

    命令行:`--item` 可重复,取值 `c1`(本任务)与 `c2`(Task 2 落地);默认跑全部已实现的项。`--screenshot DIR` 参数在本任务一并实现:进入每个状态样本后调 `page.screenshot(path=…)` 出图(见计划 03 的用法),本任务只需让参数存在且可跑通、图能落地。

    **第 4 步 —— 不触碰清单之外的一切。** 本任务**不**改任何 PAIR 条目、**不**改 `--color-surface-page`、**不**改密度值、**不**改 `#doc-panel`。`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` 零字节改动;`scripts/check-01…04` / `check-06` / `check-07` / `probe-05` / `probe-07` 代码零改动。

    **注释纪律(本任务与后续任务共同遵守)。** 写在围栏外的任何注释:不得含裸 `#hex`(check-01 扫围栏外全文)、不得含 `var(--radix-…` 或 `var(--white)`(tier-1 原语名私有于围栏)、不得含字面量 `!important;`(check-04 按出现次数计数,散文会把它从 1 顶高)、不得含 `@layer` / `@property` / `var(--x, #fallback)`。要指代颜色时写令牌名(`--color-surface-card` / `--color-border-subtle` / `--radius-md`),不写数值。
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
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c1</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or the trailing "exit=" line not "exit=0"</fails_when>
  </verify>
  <acceptance_criteria>
    - `frontend/style.css` 围栏内(`/* ===== DESIGN TOKENS: START ===== */` 与 `/* ===== DESIGN TOKENS: END ===== */` 之间)恰含两行新声明,逐字为 `--color-surface-card: var(--white);` 与 `--shadow-card: 0 1px 2px rgba(0, 0, 0, 0.04);`;两行都紧跟 `--shadow-overlay` 之后。
    - `grep -o -- '--color-surface-card' frontend/style.css | wc -l` >= 2(1 处围栏内声明 + 1 处消费者 `#main-pane > section` 的 `background`);`grep -o -- '--shadow-card' frontend/style.css | wc -l` >= 2(1 处围栏内声明 + 1 处消费者 `box-shadow`)。
    - `grep -n -- '--color-surface-card: var(--white);' frontend/style.css` 与 `grep -n -- '--shadow-card: 0 1px 2px rgba(0, 0, 0, 0.04);' frontend/style.css` 各命中恰好 1 行,且两个行号都落在 `===== DESIGN TOKENS: START` 与 `===== DESIGN TOKENS: END` 两行之间。
    - `frontend/style.css` 围栏外零裸 `#hex`、零 tier-1 原语引用(`bash scripts/check-01-token-conformance.sh` 打印 `PASS`、exit 0)。
    - `#main-pane > section` 规则体的选择器文本与行号与 HEAD 逐字一致(就地扩写,未移动);其声明集 = HEAD 的 2 条 + 新增的 4 条,无删除。
    - `#main-pane > section` 规则体内不含 `transform` / `filter` / `will-change` / `contain` / `perspective` / `opacity` / `position` / `z-index` / `overflow` 任何一项。
    - `scripts/check-09-idi09-validation.py` 存在,可用 `.venv/bin/python` 直接运行,退出码语义与 check-05 一致(0/1/2),且 `--item c1` 与 `--screenshot DIR` 两个参数都被 `parse_args` 接受。
    - `.venv/bin/python scripts/check-09-idi09-validation.py --item c1` 输出中 4 个左栏 section 的底色断言各为 PASS,`exit=0`,且 BLOCKED 计数为 0(任何 BLOCKED 都说明探针没读到元素,不构成 PASS)。
    - `.venv/bin/python scripts/check-09-idi09-validation.py --item c1` 的 INFO 行里能看到 4 个 section 的原始 `box-shadow` 读数,且其中水平偏移为 `0px`。
    - `bash scripts/check-02-contrast.py` 仍打印 `PASS: 0 failures`,清单规模与 ORDER 行逐字不变(本任务零 PAIR 改动)。
    - `bash scripts/check-03-hidden-uniqueness.sh` 打印 `PASS`;`bash scripts/check-04-important-count.sh` 打印 `PASS`。
    - `git status --porcelain frontend/` 仅列出 `frontend/style.css`;`frontend/vendor/` 内容仍只有 `marked.min.js`。
  </acceptance_criteria>
  <done>围栏内两个新令牌就位;左栏 4 个 section 在真实浏览器里的计算底色为白、圆角 10px、阴影非 none 且零位移;四个静态门 + 新运行时门 `--item c1` 全绿;`#main-pane > section` 的规则块位置与源码顺序逐字未变。</done>
</task>

<task type="auto">
  <name>Task 2: 右栏文档区同族卡片化 + `#doc-panel-header` 底色跟随 + check-05 的 `.hint` 期望侧重新登记</name>
  <files>frontend/style.css, scripts/check-09-idi09-validation.py, scripts/check-05-ui-uat.py</files>
  <reversibility rating="costly">CSS 侧回退是三条声明的还原;但本任务同时改了 `scripts/check-05-ui-uat.py` 的一条既有断言的期望侧 —— 只回退 CSS 不回退该断言,会让 `--item 5` 立刻红。两处必须成对回退,故评级 costly 而非 reversible。</reversibility>
  <read_first>
    - `frontend/style.css` `#doc-panel`(`:611-624`)—— 逐字读:`flex: 0 0 var(--doc-panel-w); display: flex; flex-direction: column; overflow-y: auto; border-left: 1px solid var(--color-border-subtle); background: var(--color-surface); min-width: 0;` 与其中 `min-width: 0` 上方那段「不得当作冗余代码删除」的注释
    - `frontend/style.css` `#doc-panel.collapsed { flex-basis: var(--doc-panel-w-collapsed); overflow: hidden; }`(`:626-629`)与 `#doc-panel.collapsed #doc-panel-header { justify-content: center; padding-inline: 0; }`(`:636-639`)—— 只读
    - `frontend/style.css` `#doc-panel-header`(`:641-654`)—— **含上方那段必须改写的注释**:它现在断言「背景是必需的」+「`--color-surface` 与 `#doc-panel` 自身背景同值且已被消费(`:474`)⇒ 零新增令牌」+「`border-radius: 0`:半径在本元素上是加背景之后才首次可见的新视觉物,而 10px 圆角会让滚动正文从四角露出」+「不加 `z-index`」。改底色后前两条与 `border-radius` 那条的理由都需按新事实重写
    - `frontend/style.css` `#doc-panel-body { padding: var(--space-8) var(--space-10); }`(`:665`)—— 只读,**不得改动**(check-05 item 3 有活断言)
    - `frontend/style.css` `.hint { color: var(--color-text-muted); … }`(`:667`)—— 它自身无 `background`,这是 `effective_bg()` 会沿祖先链上溯的原因
    - `frontend/index.html` `:82-98` —— `aside#doc-panel` > `header.panel-header#doc-panel-header` + `div#doc-panel-body`(`#doc-panel-body` **不带** `.panel-body` 类)> `div#enter-form` + `p.hint`。`document.querySelector('.hint')` 命中的就是这一条(全文件文档序第一条 `.hint`)
    - `scripts/check-05-ui-uat.py` `:471-484` —— `effective_bg()` 的定义(沿祖先链找第一个非透明 `background-color`,元素自身优先)
    - `scripts/check-05-ui-uat.py` `:1295-1306` —— 被本任务重新登记的那条断言全文与它上方的注释
    - `scripts/check-05-ui-uat.py` `:202-252` —— `ok()` 的两处 BLOCKED 分支(期望侧 `None` ⇒ `<UNRESOLVED>`;实测侧 `None` ⇒ `<MISSING>`)
    - `scripts/check-06-idi05-validation.py` `:430-490` —— g6 的两条 `box-shadow 恒 none` 对照组(`#ai-panel-header` / `#doc-panel-header`)与 `#doc-panel.collapsed` 折叠往返。**只读不改**:本任务把阴影加在 `#doc-panel` 自身,不加在 `#doc-panel-header`,这两条断言因此存活
    - `scripts/check-09-idi09-validation.py`(Task 1 产出)—— 本任务要按同一形态追加 `c2`
  </read_first>
  <action>
    **第 1 步 —— 就地改写 `#doc-panel`(`:611-624`)。**

    三条改动,全部在既有声明体上原地进行,选择器文本与规则块位置逐字不变:
    - `border-left: 1px solid var(--color-border-subtle);` → `border: 1px solid var(--color-border-subtle);`(**不是**追加一条 `border` 覆盖它 —— 留下一条已死的 `border-left` 会让注释与代码互相矛盾);
    - `background: var(--color-surface);` → `background: var(--color-surface-card);`;
    - 追加两条:`border-radius: var(--radius-md);` 与 `box-shadow: var(--shadow-card);`。

    `overflow-y: auto` 与 `min-width: 0` 及其上方注释**逐字保留**。`overflow-y: auto` 是右列的滚动者,L-1 的 sticky 表头依赖 `#doc-panel` 仍是最近的可滚祖先;删它会同时打破 `check-05 --item 8` 与面板区滚动者普查门(期望值是 4 不是 3)。

    追加一段注释(围栏外,故不得含裸 `#hex` / tier-1 原语名 / `!important;`),记下:右栏与左栏**同族**(同底色令牌 / 同边界令牌 / 同圆角令牌 / 同阴影令牌,CARD-02);`border-left: 1px` 的单边凹陷读感由四边边界 + 卡片底色取代;`overflow-y: auto` 是承重的滚动契约,不得删除。

    **第 2 步 —— 改写 `#doc-panel-header`(`:641-654`)。**

    - 声明改动只有一处:`background: var(--color-surface);` → `background: var(--color-surface-card);`。
    - `border-radius: 0` **一字不动**。理由(须写进注释):`#doc-panel` 是溢出容器(`overflow-y: auto`,且按规范另一轴的可视值会一并算成 `auto`),其后代被裁剪到**带圆角的 padding box** —— 表头的方角因此不可能把卡片四角顶成方角,卡片自己的圆角照常可见。改 `border-radius` 是**没有被迫的编辑**,不做。
    - 上方那段注释必须按新事实重写,尤其:`--color-surface` 与 `#doc-panel` 自身背景同值 ⇒ 零新增令牌」这句**现在是假的**(`#doc-panel` 已改指 `--color-surface-card`);新的表述是:表头底色与卡片底色同值 ⇒ sticky 的遮挡机制保持(滚动正文不会从表头底下穿出来),且不会在白色卡片上出现一条比卡片更暗的条带。`border-radius: 0` 那条的旧理由(「10px 圆角会让滚动正文从四角露出」)已被本阶段**刻意反转**(卡片圆角本来就该在四角裁切),须改写成:`#doc-panel-body` 的 32/40 内边距使正文与四角保持距离,10px 的裁切不触及任何文字。`不加 z-index` 那条理由不变,逐字保留。

    **第 3 步 —— 重新登记 `scripts/check-05-ui-uat.py` 的 `.hint` 断言(`:1295-1306`)。**

    该断言为 `ok(item, "[p1] .hint 实际背景 == var(--color-surface)", resolve_color(page, "--color-surface"), effective_bg(page, ".hint"), note=".hint 自身无背景,沿祖先链取到的实际底色")`。第 2 步之后,`.hint` 的最近不透明祖先是 `#doc-panel`,其底色已是卡片白 ⇒ 该断言必然红。

    处置(这是**重新登记**,不是放宽):把期望侧从 `resolve_color(page, "--color-surface")` 换成 `resolve_color(page, "--color-surface-card")`,标签文本里的令牌名同步换成 `--color-surface-card`。**断言形式一字不变** —— 仍是「实测 computed 值 == 运行时解析的令牌值」的精确等值。**禁止**改成 `ok_contains` / 子串匹配 / 「非透明」/ 硬编码 `rgb(255, 255, 255)` / 加 `or` 分支 / 删除该条。

    其上方注释(现写「实测:命中的是 index.html 里 #doc-panel-body → #doc-panel 内的那条,而 #doc-panel { background: var(--color-surface) } —— 故是 --color-surface,不是 --color-surface-page(两者在 04.1 之后是 #f9f9f9 / #fcfcfc)」)须改写为 Phase 9 的事实:`#doc-panel` 现在画 `--color-surface-card`(卡片白),`.hint` 的实际地面因此是卡片表面而不是 `--color-surface`。

    本步骤**只改这一条断言与它上方的注释**,不得触碰 `check-05` 的任何其他行。

    **第 4 步 —— 给 `scripts/check-09-idi09-validation.py` 追加断言集 `c2`(`#doc-panel`)。**

    样本 `p1`,断言:`#doc-panel` 的计算 `background-color` == `resolve_color("--color-surface-card")`;四边边框宽度均为 `1px` 且四边样式均为 `solid`(逐边断言或断言 `border-top-width == border-right-width == border-bottom-width == border-left-width == "1px"`,并打印四条原始读数);计算 `border-top-left-radius` == `resolve_token("--radius-md")`;计算 `box-shadow` != `none` 且含 `rgba(0, 0, 0, 0.04)`;计算 `overflow-y` == `auto`(**承重事实**:它是右列的滚动者,L-1 的 sticky 表头依赖它仍是最近的可滚祖先)。另加一条对照组:`#doc-panel-header` 的计算 `box-shadow` == `none`(阴影在卡片上,不在表头上 —— 与 `check-06` g6 的既有对照组同口径)。

    **注释纪律**同 Task 1。本任务不改任何 PAIR 条目、不改 `--color-surface-page`、不改密度值。
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
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c2</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or the trailing "exit=" line not "exit=0"</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 5 --browser bundled</automated>
    <fails_when>exit code is not 2 (item 5 的两条 --ai-smoke 腿在无 --ai-smoke 时按设计 BLOCKED), or any verdict line beginning with "FAIL", or the "=== 逐项结论 ===" block showing a non-zero FAIL count for item 5</fails_when>
  </verify>
  <acceptance_criteria>
    - `#doc-panel` 规则体的选择器文本与行号与 HEAD 逐字一致(就地改写,未移动);声明集 = HEAD 的 6 条 − `border-left` + `border` + 新增 2 条;`overflow-y: auto;` 与 `min-width: 0;` 逐字保留。
    - `#doc-panel` 规则体内不含 `transform` / `filter` / `will-change` / `contain` / `perspective` / `opacity` / `position` / `z-index` / `overflow: hidden` 任何一项。
    - `#doc-panel-header` 规则体内 `border-radius: 0;` 逐字保留;其 `background` 指向 `--color-surface-card`;其上方注释里不再出现「`--color-surface` 与 `#doc-panel` 自身背景同值」「零新增令牌」这类现已为假的表述。
    - `frontend/style.css` 围栏外零裸 `#hex`、零 tier-1 原语引用(`check-01` 打印 `PASS`);`!important;` 声明计数仍为 1(`check-04` 打印 `PASS`);`^[[:space:]]*\.hidden[[:space:]]*\{` 计数仍为 1(`check-03` 打印 `PASS`)。
    - `.venv/bin/python scripts/check-09-idi09-validation.py --item c2` 全 PASS,`exit=0`,BLOCKED 计数 0;其 INFO 行可见 `#doc-panel` 的四条边框宽度原始读数与 `overflow-y` 读数为 `auto`。
    - `check-09` 的 `#doc-panel-header box-shadow == none` 对照组为 PASS。
    - `.venv/bin/python scripts/check-05-ui-uat.py --item 5 --browser bundled` 的 item 5 FAIL 计数为 0;`[p1] .hint 实际背景` 一行为 PASS(不是 BLOCKED)。
    - 逐行核对 `git diff scripts/check-05-ui-uat.py` 的输出:改动恰好 2 处,且都落在 `.hint` 断言所在的那一个函数内(1 条断言的期望侧 + 其上方注释),无其他函数被触碰。
    - `git status --porcelain frontend/` 仅列出 `frontend/style.css`;`frontend/vendor/` 仍只有 `marked.min.js`。
  </acceptance_criteria>
  <done>右栏 `#doc-panel` 呈现为与左栏同族的白卡片(白底 + 四边 1px 边界 + 10px 圆角 + 极轻阴影),`overflow-y: auto` 未动;`#doc-panel-header` 底色与卡片同值、`border-radius: 0` 保留;`check-09 --item c2` 与 `check-05 --item 5` 全绿。</done>
</task>

<task type="auto">
  <name>Task 3: 两条 PAIR 的地面重新归属(不是调色、不是放宽阈值)+ 清单历史登记</name>
  <files>frontend/style.css</files>
  <reversibility rating="costly">这条登记与「卡片化」是同一次改动的两面:回退登记而不回退卡片会让 `check-02` 的两条断言失去地面;回退卡片而不回退登记则会让这两条断言断言的是一张不存在的白卡片。两处必须成对回退,且回退后必须重新测量,故评级 costly 而非 reversible。</reversibility>
  <read_first>
    - `frontend/style.css` 清单段 `:416-566` —— 逐条读清单头部注释(阈值 4.5 / 3.0、覆盖地板 24/20/4、`raw_pairs == len(pairs)` 的标记计数一致性、六个 value layer 的规模台账 `24 / 34 / 43 / 47 / 50 / 53`)
    - `frontend/style.css` `:517-523` —— `--color-marker-active` TEXT 半的注释与 `/* PAIR --color-marker-active ON --color-surface-page TEXT */`。注释现断言「All three panels live inside #main-pane, and #main-pane and its ancestors declare no background (html, body is what sets --color-surface-page), so the ground is --color-surface-page」—— **本任务后这句为假**
    - `frontend/style.css` `:525-527` —— 非文本边界组标题 + `/* PAIR --color-border-strong ON --color-surface-page NON-TEXT */` + `/* PAIR --color-border-strong ON --color-surface NON-TEXT */`(**后一条保留,它服务三个自带 gray-2 底色的 select**)
    - `frontend/style.css` `:528-541` —— `--color-border-hover` 的注释,其中逐字登记了「No input in this app declares a background, so Chrome paints the field fill white and the border is drawn against it, not against the container surface; measured, the hover boundary on white is 5.92 and the resting one 3.32」。**这条既登记事实是本任务重新归属的依据,注释必须引用它**
    - `frontend/style.css` `:559-562` —— `--color-marker-active` NON-TEXT 半的注释与 `/* PAIR --color-marker-active ON --color-surface-page NON-TEXT */`
    - `frontend/style.css` `:147-168` —— `--color-marker-active` 的 tier-2 声明与「Measured 4.65 on --color-surface-page — it clears TEXT (>=4.5) and NON-TEXT (>=3) at once, and is this phase's thinnest margin (0.15). Do NOT "play it safe" and step it darker」—— 本任务**不动这个值**,但该段里「4.65 on --color-surface-page」这句在本阶段后需按新事实补一句(见 action 第 5 步)
    - `frontend/style.css` `:89-96` —— `--color-border-strong` 的 role-band 登记(gray-9 = 3.24 / 3.15),证明该令牌被多处消费,改值会连锁
    - `scripts/check-02-contrast.py` 全文(`:1-235`)—— `DECL_RE` / `PAIR_RE` / `ORDER_RE` 的正则形态、`resolve()` 的「未知令牌即 FAIL」、覆盖地板、`raw_pairs` / `raw_orders` 计数一致性、阈值常量与闭区间比较。**本任务一行都不改它**
    - `.planning/phases/idi-09-card-containers/09-CONTEXT.md` §`规划期实测的对比度影响面` 与 §`两条 FAIL 的正解 = 重新归属配对` 与 §`禁止的两种错误修法`
    - `.planning/ROADMAP.md` §`### Phase 9:` 的 Deliverables 第 4 条与 Success Criterion 5、Pitfalls 第 1、2 条
  </read_first>
  <action>
    **第 1 步 —— `/* PAIR --color-marker-active ON --color-surface-page TEXT */`(`:523`)的地面改记为 `--color-surface-card`。**

    逐字新行:`/* PAIR --color-marker-active ON --color-surface-card TEXT */`。

    依据(须写进它上方的注释):该令牌只有 2 处消费者,全在 `.panel-header` 内 —— `#session-panel` / `#annotations-panel` / `#checks-panel` 的 inset 3px 竖条(`style.css:1426-1430`)与同三个表头的 h2 颜色(`:1431-1435`)。卡片化后这三个面板都是**不透明白卡片**,标题确实画在白卡片上;旧地面 `--color-surface-page` 只在面板**完全透明**时成立(那正是 HEAD 的状态,所以旧登记当时是对的、现在不是)。白底实测比值 **4.77 >= 4.5**。

    同时改写 `:517-522` 那段注释里现已为假的断言(「All three panels live inside #main-pane, and #main-pane and its ancestors declare no background …, so the ground is --color-surface-page」):新的表述是这三个面板各自声明了 `background: var(--color-surface-card)`(`#main-pane > section`),故地面是卡片表面。

    **第 2 步 —— `/* PAIR --color-border-strong ON --color-surface-page NON-TEXT */`(`:526`)的地面改记为 `--color-surface-card`。**

    逐字新行:`/* PAIR --color-border-strong ON --color-surface-card NON-TEXT */`。**紧邻的 `/* PAIR --color-border-strong ON --color-surface NON-TEXT */`(`:527`)逐字保留** —— 它服务三个自带 `background: var(--color-surface)` 的 select(`#ai-route-select` / `#check-switcher` / `#round-switcher`),那张地面没有变。

    依据(须写进注释):该令牌有 10 处消费者,全是 input / select 的静止边框。其中 select 自带 gray-2 底色、已由 `:527` 那条覆盖;input 全部**不声明 background** ⇒ Chrome 画 UA 字段填充(白),边框实际画在白上 —— 这条事实本文件 `:528-541` 已逐字登记,并记下静止边界在白上是 **3.32**。白底实测 3.32 >= 3.0。**不要**在注释里把它说成「卡片化带来的新事实」:它是本文件早已登记的事实的如实归位。

    **第 3 步 —— 在 `:559-562` 的 NON-TEXT 半注释里登记保留页面地面的理由。**

    `/* PAIR --color-marker-active ON --color-surface-page NON-TEXT */`(`:562`)的**条目名逐字不变**(本阶段登记的重新归属恰好是 2 条,ROADMAP Success Criterion 5 / Deliverables 逐条列举的就是第 1、2 步那两条)。但该条的物理绘制面与 TEXT 半是**同一元素族**(同一个 `.panel-header` 的 inset 竖条),所以必须在注释里把这件事写明,以免日后被读成自相矛盾:

    - 该条的物理地面同样是卡片表面(与 `:523` 同元素族);
    - 它保留在 `--color-surface-page` 是**刻意的保守读数**:页面地面上的比值(HEAD 的 gray-1 上 4.65,gray-3 上 4.18)恒**低于**卡片地面的 4.77,所以留在页面地面是更严的那一侧,不是遗漏;
    - 两个数值(4.18 与 4.77)都要写出来,使「保留」这一动作可被独立核对。

    **第 4 步 —— 清单头部台账登记 Phase 9。** 在 `:427-452` 的「Manifest size across six value layers (D-15): 24 / 34 / 43 / 47 / 50 / 53」段之后追加一段 Phase 9 记录:**清单规模不变**(53 对 = 35 TEXT + 18 NON-TEXT,加 1 条 ORDER);变的是 1 组地面的重新归属(2 条),不是规模。**不得**改写那六个历史数字,也**不得**把 Phase 9 混进那串数字里。

    **第 5 步 —— 在 `:147-168` 的 `--color-marker-active` 声明注释里补一句按新事实的登记。** 该段现有「Measured 4.65 on --color-surface-page — it clears TEXT (>=4.5) and NON-TEXT (>=3) at once, and is this phase's thinnest margin (0.15)」与「Do NOT "play it safe" and step it darker (05-N-2 / Pitfall 4a)」。**不改值、不删任何一句**,只追加一句:Phase 9 卡片化后该令牌的两处消费者都画在 `--color-surface-card` 上,白底实测 4.77;页面换为 gray-3 后页面地面上的读数是 4.18 —— 仍 >= NON-TEXT 的 3.0,但已跌破 TEXT 的 4.5,这正是 TEXT 半条必须重新归属的原因。

    **第 6 步 —— 明令禁止的两种错误修法(本任务绝不做)。**
    - **不得改任何颜色值**:不得动 `--radix-blue-11`、不得动 `--radix-gray-9`、不得动任何 `--radix-*`、不得动任何 tier-2 颜色值。二者分别被多处消费(`--radix-blue-11` 还挂着 `:161-168` 的「最薄余量,不要求稳加深」警告),改值会连锁改掉它们的**全部**其他配对。
    - **不得放宽阈值**:不得改 `scripts/check-02-contrast.py` 的任何一行(含 `TEXT_MIN = 4.5` / `NON_TEXT_MIN = 3.0`),不得删除任何 PAIR 条目(会打破覆盖地板与标记计数一致性)。

    **第 7 步 —— 注释纪律。** 本任务的所有注释都写在**围栏内**,故裸 `#hex` 合法;但仍不得含字面量 `!important;`(check-04 按出现次数计数)。不得新增 `@layer` / `@property` / `var(--x, #fallback)`。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-02-contrast.py</automated>
    <fails_when>non-zero exit, or any line beginning with "FAIL", or the final line not "PASS: 0 failures", or the output missing the exact lines "PASS  4.77  --color-marker-active on --color-surface-card" and "PASS  3.32  --color-border-strong on --color-surface-card"</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>non-zero exit, or stdout not exactly "PASS"</fails_when>
    <automated>bash scripts/check-04-important-count.sh</automated>
    <fails_when>non-zero exit, or stdout not exactly "PASS"</fails_when>
  </verify>
  <acceptance_criteria>
    - `frontend/style.css` 围栏内恰含 `/* PAIR --color-marker-active ON --color-surface-card TEXT */` 与 `/* PAIR --color-border-strong ON --color-surface-card NON-TEXT */` 两条新地面条目;`ON --color-surface-page` 的 PAIR 条目数由 8 条降为 6 条(`--color-marker-active ON --color-surface-page NON-TEXT` 仍在其中)。
    - `.venv/bin/python scripts/check-02-contrast.py` 打印 `PASS: 0 failures`,且输出中同时含 `PASS  4.77  --color-marker-active on --color-surface-card` 与 `PASS  3.32  --color-border-strong on --color-surface-card` 两行(数值精确到小数点后两位,闭区间)。
    - `grep -o '/\* PAIR' frontend/style.css | wc -l` == 53;`grep -o '/\* ORDER' frontend/style.css | wc -l` == 1(两者与改动前逐字相同)。
    - `git diff -U0 frontend/style.css` 的**全部输出**人工核对:除 `--color-surface-page` 那一行外,不存在任何其他以 `--radix-` 开头的增删行(本任务零 primitive 值改动)。
    - `git diff scripts/check-02-contrast.py` 为空(该文件零改动)。
    - `:559-562` 的注释里同时出现 `4.18` 与 `4.77` 两个数值,并说明保留页面地面是保守读数。
    - `:427-452` 的六个历史规模数字 `24 / 34 / 43 / 47 / 50 / 53` 逐字保留;Phase 9 的记录以独立段落追加,未混入那串数字。
    - `:147-168` 段落中「Do NOT "play it safe" and step it darker」逐字保留,且 `--color-marker-active: var(--radix-blue-11);` 这一行未被改动。
    - `bash scripts/check-01-token-conformance.sh` 打印 `PASS`;`bash scripts/check-04-important-count.sh` 打印 `PASS`。
    - `git status --porcelain frontend/` 仅列出 `frontend/style.css`。
  </acceptance_criteria>
  <done>两条中间调前景的配对按「卡片化后元素的实际绘制面」重新归属到卡片底色并在白底达标(4.77 / 3.32);NON-TEXT 半条的保留以注释登记为保守读数;零颜色值改动、零阈值放宽、零条目删除;`check-02` 全绿。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 无外部输入边界 | 本阶段只改 `frontend/style.css`(呈现层):零用户输入处理、零鉴权、零数据访问、零网络调用、零新增资源加载。攻击面限于**浏览器对 CSS 的解析与渲染**,以及新 CSS 对既有层叠 / 定位几何的副作用 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-09-01 | Information Disclosure | 本阶段新增的卡片选择器(`#main-pane > section` / `#doc-panel` / `#doc-panel-header`) | low | accept | 选择器只用既有 ID 与元素名,不含属性选择器、不读用户数据、不引入 `url()` / `@import` / 远程字体 —— CSS 侧不存在数据外泄面。新增令牌 `--color-surface-card` / `--shadow-card` 的值是纯颜色与阴影,不含任何 URL。验收:`git diff frontend/style.css` 中新增行不含 `url(` / `@import` |
| T-idi-09-02 | Tampering | `#doc-panel` 上新增的 CSS 属性 | medium | mitigate | `#stream-banner` 是 `#doc-panel` 的**后代**且 `position: fixed`(`style.css:872-885`,`z-index: var(--z-banner)`);任何建立「fixed 定位包含块」或新层叠上下文的属性(`transform` / `filter` / `will-change` / `contain` / `perspective` / `opacity` / `position` / `z-index`)都会把横幅钉到卡片上而不是视口,并把它的 `z-index: var(--z-banner)` 关进 `#doc-panel` 的层叠上下文里。`.overlay` 两个弹窗与 `#selection-menu` 在 `#doc-panel` 之外(`frontend/index.html:207/238/249`),不受本项影响。缓解:卡片规则只用 `background` / `border` / `border-radius` / `box-shadow` —— 四者均不建立包含块、不建层叠上下文;上述八个属性列入本计划的 `<prohibitions>` 并在 `check-09 --item c2` 旁以只读诊断记录横幅几何。探测器:`check-05 --item 8` 的 768 / 1024 / 1280 三处 badge × banner rect 不相交断言(计划 03 复跑) |
| T-idi-09-03 | Tampering | 1px 边框对既有几何的位移 | low | accept | 全局 `* { box-sizing: border-box }`(`style.css:3`)⇒ 1px 边框落在容器外框之内,不改变容器外框尺寸;圆角与阴影不参与布局。残留风险是内容盒收窄 2px(可能影响窄窗口下的换行)。探测器:`check-06` g5 的 340px 最窄面板 `#btn-authorize` 单行 / 不裁切断言(计划 03 复跑) |
| T-idi-09-04 | Elevation of Privilege | 无 | low | accept | 本阶段不触碰鉴权、权限门、服务端路径或任何 API;纯呈现层改动,无提权面 |
| T-idi-09-SC | Tampering | npm / pip / cargo 安装 | low | accept | 本阶段**零安装**:零新增依赖、零构建步骤、零新增第三方包(DESIGN.md D-06 硬约束)。`frontend/vendor/` 仍只有 `marked.min.js`,无供应链面进入。验收:`ls frontend/vendor/` 输出仅 `marked.min.js` |
</threat_model>

<verification>
**静态门(全部必须绿):**

- `bash scripts/check-01-token-conformance.sh` → `PASS`(围栏外零裸 `#hex`、零 tier-1 原语引用)
- `.venv/bin/python scripts/check-02-contrast.py` → `PASS: 0 failures`(53 对 + 1 条 ORDER;两条新地面 4.77 / 3.32)
- `bash scripts/check-03-hidden-uniqueness.sh` → `PASS`
- `bash scripts/check-04-important-count.sh` → `PASS`

**运行时门(本计划新建):**

- `.venv/bin/python scripts/check-09-idi09-validation.py --item c1` → `exit=0`,0 FAIL / 0 BLOCKED(左栏 4 个 section 的卡片语言)
- `.venv/bin/python scripts/check-09-idi09-validation.py --item c2` → `exit=0`,0 FAIL / 0 BLOCKED(`#doc-panel` 的卡片语言 + `#doc-panel-header` 的对照组)

**既有门(本计划会打破的那一条已重新登记,须证明它回到绿):**

- `.venv/bin/python scripts/check-05-ui-uat.py --item 5 --browser bundled` → item 5 FAIL 计数 0(`.hint` 实际背景断言按新事实重新登记后期望侧成立);两条 `--ai-smoke` 腿仍按设计 BLOCKED ⇒ `exit=2`

**仓库卫生:**

- `git status --porcelain frontend/` 仅列出 `frontend/style.css`
- `ls frontend/vendor/` 仅 `marked.min.js`
- `git diff scripts/check-02-contrast.py` 为空;`git diff -U0 frontend/style.css` 的输出里除 `--color-surface-page` 那一行外无其他 `--radix-` 增删行
</verification>

<success_criteria>
- 左栏 4 个 section 与右栏 `#doc-panel` 在真实浏览器里各自呈现为白底卡片:计算底色 == `--color-surface-card`(白)、计算圆角 == `--radius-md`(10px)、计算 `box-shadow` 非 `none` 且零位移、四边可见边界。
- 页面底色、密度值、任何颜色值在本计划内**零改动**(它们属计划 02);本计划对颜色的唯一动作是 2 条 PAIR 的地面重新归属。
- `#doc-panel-header` 的底色与卡片同值,sticky 遮挡机制保持;`#doc-panel` 的 `overflow-y: auto` 与 `#doc-panel-body` 的 padding 逐字未动。
- `frontend/style.css` 的全部改动都是**就地扩写既有规则体**或围栏内新增声明 —— 没有任何既有规则块被移动,源码顺序逐字不变。
- 四个静态门 + 新运行时门全绿;`check-05 --item 5` 的 FAIL 计数回到 0。
- `frontend/app.js` / `frontend/index.html` / `frontend/vendor/` 零字节改动。
</success_criteria>

<output>
Create `.planning/phases/idi-09-card-containers/idi-09-01-SUMMARY.md` when done
</output>

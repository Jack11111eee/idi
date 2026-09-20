---
phase: idi-05-typography-and-visual-hierarchy
plan: 03
type: execute
wave: 3
depends_on:
  - idi-05-01
  - idi-05-02
files_modified:
  - frontend/style.css
  - scripts/check-05-ui-uat.py
autonomous: true
requirements:
  - VISUAL-04
  - VISUAL-05

estimate:
  tokens: 55000
  raw_tokens: 55000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- lifted from idi-05-UI-SPEC.md `## UI Considerations` — explicit tier (12 of 22; E4 + E5 + E6 + E7) ----
    - "E4 侧栏三面板标题行的 loading 态:三面板的显隐由 `.hidden` 驱动(app.js 既有句柄);本阶段 app.js / index.html 零 diff,活动态由纯 CSS `:not(.hidden)` 推导,不引入新状态 ← UI-SPEC UI-Considerations E4 `loading`(explicit)"
    - "E4 侧栏三面板标题行的 error 态:CHECK-03(`^\\.hidden {` == 1)与 CHECK-04(`!important;` == 1)钉住 `.hidden` 的唯一性,任何面板态的显隐结构不可能移动 ← UI-SPEC UI-Considerations E4 `error`(explicit)"
    - "E5 `#ai-panel` 的 loading 态:折叠态由 `#ai-panel-body` 上的 `.collapsed` 驱动(app.js:1563-1569),本阶段零改动;它从不被 `.hidden`,故不参与三选一活动态推导(D-16)← UI-SPEC UI-Considerations E5 `loading`(explicit)"
    - "E5 `#ai-panel` 的 error 态:其折叠行为按 SC4 要求保持不变 ← UI-SPEC UI-Considerations E5 `error`(explicit)"
    - "E6 `.annotation-quote` 引用行的 empty 态:该行的存在与否由 app.js 的 `renderAnnotations` 驱动(已验收路径,硬规则 5 不得触碰);本阶段零 diff,故空态结构不变 ← UI-SPEC UI-Considerations E6 `empty`(explicit)"
    - "E6 `.annotation-quote` 引用行的 loading 态:本阶段只把 `::before` 的机制换成 mask 字形,不触碰渲染函数 ← UI-SPEC UI-Considerations E6 `loading`(explicit)"
    - "E6 `.annotation-quote` 引用行的 error 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E6 `error`(explicit)"
    - "E6 `.annotation-quote` 引用行的 populated 态:批注列表的正常填充态结构与文案均不变 ← UI-SPEC UI-Considerations E6 `populated`(explicit)"
    - "E7 `.verdict-location` 位置行的 empty 态:该行的存在与否由 app.js 的 `renderVerdictCard` 驱动(已验收路径,不得触碰);本阶段零 diff,故空态结构不变 ← UI-SPEC UI-Considerations E7 `empty`(explicit)"
    - "E7 `.verdict-location` 位置行的 loading 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E7 `loading`(explicit)"
    - "E7 `.verdict-location` 位置行的 error 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E7 `error`(explicit)"
    - "E7 `.verdict-location` 位置行的 populated 态:裁决卡片的正常填充态结构与文案均不变 ← UI-SPEC UI-Considerations E7 `populated`(explicit)"
    # ---- lifted from idi-05-UI-SPEC.md `## UI Considerations` — backstop tier (8 of 18) ----
    - statement: "E4 3px 竖条在**每个**活动面板上真实可见 —— 既不被该面板标题行内的元素盖住,也不因 `border-radius: var(--radius-md)` 在角落断开。这是 05-N-4 的实测验收。"
      verification: backstop
    - statement: "E4 面板标题文本变长时竖条仍贴左缘,标题变色(标记色)不溢出标题行。"
      verification: backstop
    - statement: "E5 `#ai-panel` 折叠/展开两态下,竖条(若适用)与既有折叠指示器并存且不重叠。"
      verification: backstop
    - statement: "E5 折叠指示器不因标题变长而漂移;`.collapse-indicator` 本阶段零触碰(D-23)。"
      verification: backstop
    - statement: "E6 两个 12px mask 字形与相邻文字基线视觉对齐,且不撑高行盒(行高仍由 `--lh-snug` / `--lh-reading` 决定)。计算样式看不见这一项,只能看渲染结果。"
      verification: backstop
    - statement: "E6 图标在折行的引用文本里仍与首行文字对齐,不在换行处漂移;`--color-text-secondary` 在 `.annotation-item`(`--color-surface` 5.62)地面上可辨。"
      verification: backstop
    - statement: "E7 两个 12px mask 字形与相邻文字基线视觉对齐,且不撑高行盒。"
      verification: backstop
    - statement: "E7 图标在折行的位置文本里仍与首行文字对齐;`--color-text-secondary` 在 `.verdict-card`(`--color-surface-warning-subtle` 5.82)地面上可辨。"
      verification: backstop
    # ---- phase-specific truths ----
    - "新增 tier-2 令牌 `--color-marker-active: var(--radix-blue-11);`,与它的消费者(两条追加规则)**同一次提交**落地(Hard Rule 5 —— 新令牌不得成为孤儿);**不复用 `--color-action-primary`** ← D-18 / A-7"
    - "活动面板标记 = 左侧 3px 蓝竖条 + 面板标题文字改用标记色,实现用 `box-shadow: inset 3px 0 0 var(--color-marker-active)`(而非 `border-left` —— 它会加 3px 宽度造成布局位移);竖条落在 `.panel-header` 而非 `<section>`(section 的带背景子元素会盖住左边缘的 inset 竖条)← D-17 / 05-N-4"
    - "两条规则**追加在文件末尾**(硬规则 3:追加,不重排);`:not(.hidden)` 只**读取** `.hidden` 机制,不修改它 ← 硬规则 1 / D-16"
    - "VISUAL-04 的范围口径为「三选一活动态 + AI 面板折叠态」:`p1` → `#session-panel`、`p3` → `#annotations-panel`、`checking` → `#checks-panel`;`#ai-panel` 从不被 `.hidden`(grep `aiPanel` 在 app.js 零命中),它的可辨状态是既有的折叠指示器 ← D-16 / A-5"
    - "`#doc-panel-header` 虽是 `.panel-header` 但不被三条 ID 选择器匹配 —— 无意外覆盖 ← UI-SPEC §VISUAL-04 层叠核账"
    - "清单新增 2 条配对(`--color-marker-active ON --color-surface-page` 的 TEXT 与 NON-TEXT 各一),规模 45 → **47 对(35 TEXT + 12 NON-TEXT)+ 1 ORDER**,实测均 4.65 ← CHECK-02 / SC 1.4.5 与 SC 1.4.11"
    - "新增两个围栏内令牌 `--icon-pin` / `--icon-location`,各恰有一个同提交消费者(`.annotation-quote::before` / `.verdict-location::before`);`<path>` **不带 `fill` 属性**,data-URI 内**零颜色信息**(无 `%23`、无 `#`、无 `fill=`),`viewBox='0 0 12 12'`、`xmlns` 齐备、`<path>` 恰 1 个 ← D-20 / D-22"
    - "机制为 `mask-image` + `background-color: var(--color-text-secondary)`(刻意偏离契约的 `content: url(data-URI)`):data-URI 经 `content` 渲染为图片、不继承页面 CSS、`currentColor` 不可用,只能把 fill 钉死为转义 hex —— 那让「跟文字色」成为人工同步的约定而非机制;mask 只看 alpha,故零颜色信息,契约的字面量例外 **L-3 可以整个撤掉** ← D-20 / D-21 / A-1 / A-2"
    - "两处伪元素规则**原地改写**,不在文件末尾追加重复选择器 —— 两个选择器全文各只出现一次、无竞争者,故原地改写在层叠上等价于追加,且避免了在末尾留一条被覆盖的死规则 ← 硬规则 3 的实质"
    - "三条实现细节齐备:`margin-right: var(--space-1)`(原 emoji 自带尾随空格,12px 盒没有)、`-webkit-mask-*` 与 `mask-*` 成对书写、`mask-repeat: no-repeat` 与 `mask-size: 12px 12px` 显式声明 ← UI-SPEC §VISUAL-05 三条实现细节"
    - "`.collapse-indicator` 零改动:`grep -n '^\\.collapse-indicator' frontend/style.css` 仍恰 1 行且逐字节与 HEAD 相同;`frontend/app.js` 与 `frontend/index.html` 零 diff ← D-23 / Pitfall 7 / Gate 6"
    - "运行时:`p1` / `p3` / `checking` 三个样本下,当前活动面板的 `.panel-header` 的 computed `box-shadow` 解析为 `inset 3px 0 0 <--color-marker-active 的运行时值>`,其 `h2` 的 computed `color` == 该令牌值;`#ai-panel .panel-header` 与 `#doc-panel-header` 的 `box-shadow` == `none` ← 硬规则 7 / D-16 / D-17"
    - "运行时:两处 `::before` 的 computed `width` / `height` == `12px`、`background-color` == `--color-text-secondary` 的运行时值、`mask-image` != `none` ← 硬规则 7 / D-20 / D-21 / D-22"
    - "D-05 的连带义务已履行:`idi-04.1-radix` 的三项 `human_verification` 与四条守卫在本阶段的值改动之后逐条重跑,全部数值**从 HEAD 重算**而非补指纹;tier-1 仍 25、tier-2 47 → 48、清单 43 → 47、`ORDER 0.363` 与 `--color-text-info ON --color-surface-info` 的 4.53 逐字不变 ← D-05 / A-8"

  artifacts:
    - path: "frontend/style.css"
      provides: "围栏内新增 `--color-marker-active: var(--radix-blue-11);` 与两个 data-URI 令牌 `--icon-pin` / `--icon-location`;清单新增 2 条 `--color-marker-active` 配对;文件末尾追加两条活动态标记规则;`.annotation-quote::before` 与 `.verdict-location::before` 的规则体原地改写为 mask 盒模型"
      contains: "--color-marker-active: var(--radix-blue-11);"
    - path: "scripts/check-05-ui-uat.py"
      provides: "新增伪元素读取器 `read_pseudo_style`;item4 新增活动态标记断言(p1 / p3 / checking 三态 + `#ai-panel` 与 `#doc-panel-header` 的对照组)与 `.verdict-location::before` 的 mask 断言;item6 新增 `.annotation-quote::before` 的 mask 断言;item_smoke 扩一条活动态标记的快速切片"
      contains: "def read_pseudo_style"

  key_links:
    - from: "`--color-marker-active`(围栏 tier-2)"
      to: "文件末尾两条追加规则(`#…-panel:not(.hidden) .panel-header` 的 `box-shadow` 与 `.panel-header h2` 的 `color`)"
      via: "同一次提交落地(Hard Rule 5)—— 新令牌不得成为孤儿"
      pattern: "box-shadow: inset 3px 0 0 var\\(--color-marker-active\\);"
    - from: "`.hidden { display: none !important }`(机制)"
      to: "`:not(.hidden)`(读取)"
      via: "隐藏时选择器根本不匹配;规则本身零改动(CHECK-03 / CHECK-04 守卫)"
      pattern: "#session-panel:not\\(\\.hidden\\) \\.panel-header"
    - from: "`--icon-pin` / `--icon-location`(围栏内的 data-URI)"
      to: "`.annotation-quote::before` / `.verdict-location::before` 的 `mask-image`"
      via: "mask 只看 alpha ⇒ `<path>` 不带 fill ⇒ data-URI 内零颜色信息 ⇒ 契约例外 L-3 整个撤掉(Gate 5)"
      pattern: "mask-image: var\\(--icon-pin\\);"

  prohibitions:
    - statement: "不得复用 `--color-action-primary` 承载活动面板标记 —— 该名字说的是「主要动作」,拿它做面板指示器会让**名说谎**;本项目为此付过代价(04.1 的 D-03 把 26 个 primitive 全部改名,理由正是「保留旧名会让名说谎」)。本阶段保留 accent 行的**元素清单**,只把承载它的**令牌名**换成一个说实话的新名字(D-18 / A-7)"
      status: active
      verification: flagged
    - statement: "不得把 `--color-marker-active` 换成更浅或更深的蓝步 —— blue-11 在 `--color-surface-page` 上实测 4.65,同时满足 TEXT(≥4.5)与 NON-TEXT(≥3),是本族唯一同时满足两条阈值的可用步;0.15 的薄余量是「最浅通过值」规则的代价,加深它才是违反规则(blue-2/3 太浅,blue-12 会把标题变成深海军蓝并放弃该规则)(05-N-2 / Pitfall 4a)"
      status: active
      verification: flagged
    - statement: "不得触碰 `.collapse-indicator` —— `app.js:1563` / `:1569` 用 `textContent` 赋值,内联 `<svg>` 会被静默擦掉;它的 `font-size: 20px` / `line-height: 1` 越轨字面量属 backlog `999.1`,本阶段不修(D-23 / Pitfall 7)。这是本阶段范围锁最硬的一条"
      status: active
      verification: flagged
    - statement: "不得用 `border-left` 实现活动态竖条 —— 它会加 3px 宽度,把标题行内的 `#pending-count` / `#check-state` 往右推;`box-shadow: inset` 不参与布局,冻结轮已经是这个写法(05-N-4 / D-17)"
      status: active
      verification: flagged
    - statement: "不得把竖条落在 `<section>` 上而不是 `.panel-header` —— 三个 section 的子元素都带背景色(`.chat-bubble` / `.annotation-item` / `.event-list` / `.panel-body`),`box-shadow: inset` 画在元素自身的背景层上,带背景的子元素会盖住左边缘的竖条。这不是审美偏好,是层叠事实(05-N-4)"
      status: active
      verification: flagged
    - statement: "不得在 `--icon-*` 的 data-URI 里留下任何颜色信息(`%23` / `#` / `fill=`)—— 「零颜色信息」是撤掉字面量例外 L-3 的**唯一依据**,必须机械可核(Gate 5 / A-1 / D-20)。也不得给 `<path>` 加 `fill` 属性 —— mask 只看 alpha,默认黑即不透明"
      status: active
      verification: flagged
    - statement: "不得引入图标库 / SVG sprite 体系 / 图标字体 / 任何第三方包,也不得新增任何文件 —— 两个字形是手写的围栏内 data-URI,零新文件、零依赖、零 CDN;`frontend/vendor/` 仍只含 `marked.min.js`(REQUIREMENTS §Out of Scope / 硬规则 6)"
      status: active
      verification: flagged
    - statement: "不得把活动面板标题的 `font-weight` 改成 600 —— D-09 已把 chrome 标题统一为 500,且 `.panel-header` 是 `height: 36px` + `justify-content: space-between` 的 flex 行,改字重会移动行内的 `#pending-count` / `#check-state`。标题只改 `color`(D-09 / D-17)"
      status: active
      verification: flagged

  assumptions:
    # ---- edge probe fallback ($COVERAGE): 2 rows for this plan's requirement IDs, ALL unresolved ----
    - statement: "VISUAL-04 的边缘面未经探针确认(probe 返回 `unclassified — review manually`):「活动/非活动态可区分」在 `.hidden` 之外是否存在别的状态轴(例如面板可见但内容为空)?本计划按 D-16 的范围修正(三选一活动态 + AI 面板折叠态)执行,并把该行记为 flagged assumption。"
      status: unresolved
      verification: flagged
    - statement: "VISUAL-05 的边缘面未经探针确认(probe 返回 `unclassified — review manually`):mask 盒模型的基线对齐(`vertical-align: -2px` 是起点而非结论,05-N-5)与两个字形在 12px 下的可辨性无法由计算样式读出,只能看渲染结果。本计划把它列为实测项(已作为 E6 / E7 的 backstop 陈述记录),并把该行记为 flagged assumption。"
      status: unresolved
      verification: flagged
---

<!-- planner-discipline-allow: content: '📌 ' -->
<!-- planner-discipline-allow: content: '📍 ' -->
<!-- 本计划的任务确实要把两处伪元素规则的现有 `content` 声明整条替换掉,但那两条规则由选择器
     `.annotation-quote::before` / `.verdict-location::before` 唯一标识(全文各只出现一次、无竞争者),
     故本计划的 `<action>` 与验收命令都不引用 emoji 字面量,而用选择器 + `content: '';` 的出现次数
     作为判据。这两条 allow 标记是为「本计划正文引用了 UI-SPEC 对这两处规则的处置」而备。 -->

<objective>
把侧栏当前活动面板变得可辨认(VISUAL-04),并把两处写死的 emoji 字形换成跟随令牌的内联掩码字形(VISUAL-05);最后履行 D-05 的连带义务,复验 `idi-04.1-radix`。

Purpose: VISUAL-04 与 VISUAL-05 是同一类改动 —— 把「人工同步的约定」换成「机制」。VISUAL-04 的现状是:三个面板靠 `.hidden` 互斥切换(任一状态恰有一个可见),但**活动的那一个看不出是活动的**。VISUAL-04 的实质不是「四个面板都可区分」—— `#ai-panel` **从不被 `.hidden`**,它的可辨状态是既有的折叠指示器,故 REQUIREMENTS 的字面措辞按 D-16 收窄为「三选一活动态 + AI 面板折叠态」。VISUAL-05 的现状是两处 `content` 里写死的 emoji:emoji 是字体引擎渲染的字形,颜色由字体决定,**不跟随页面 CSS**;契约原本的 `content: url(data-URI)` 方案把 fill 钉死为转义 hex —— 那让「跟文字色」成为**人工同步的约定**而非机制。本计划改用 `mask-image` + `background-color`:mask 只看 alpha,`<path>` 不带 `fill` 即可,data-URI 里**零颜色信息**,于是契约的字面量例外 L-3 可以整个撤掉。

Output: 侧栏活动面板的左侧 3px 蓝竖条 + 标题变色(纯 CSS `:not(.hidden)` 推导,`app.js` 零 diff);两个围栏内 data-URI 掩码字形(实心图钉 / 实心地图标记,12×12,`--color-text-secondary` 上色);`check-02` 在 **47 对**清单上 `PASS: 0 failures`;`idi-04.1-radix` 的连带复验结果。

**D-11 / D-18 / D-22 委派给规划期的取值,本计划定稿(必须逐字照抄):**
- **活动态标记令牌名与它指向的 Radix 步**:`--color-marker-active: var(--radix-blue-11);`。选蓝而非契约划定的琥珀,是因为琥珀在本系统已承载**警告**(`--color-action-warning` / `#pending-count` / `#state-badge`)与**冻结轮**(`#round-doc.round-frozen` 的琥珀 inset 竖线)两重含义,再加「活动面板」即三重撞车;蓝在本系统已是「信息 / 流式」色(`--color-surface-info` / `--color-text-info` / `--color-border-streaming`),与琥珀明确分离。blue-11 已声明、已消费(它已承载 `--color-action-primary` / `--color-text-info` / `--color-kind-say` / `--color-border-streaming` 四个 tier-2 名),本阶段把它变成第五个 —— 这是刻意的,不是重复;实测 4.65 同时满足两条阈值。**这是对契约 60/30/10 表 Accent 域的刻意偏离并已登记(A-7)**:元素清单与颜色值都不变,只有承载令牌的名字变。
- **两个字形的 `d` 路径数据**(实心,`viewBox='0 0 12 12'`,恰 1 个 `<path>`,无 `fill`):
  - `--icon-pin`(实心图钉):`M6 0.6 L8.8 2.2 L8.8 5.2 L10.6 7.4 L7.1 7.4 L7.1 10.6 L6 12 L4.9 10.6 L4.9 7.4 L1.4 7.4 L3.2 5.2 L3.2 2.2 Z`
  - `--icon-location`(实心地图标记,内含一个反向绕行的内圈形成「孔」):`M6 0 C3.5 0 1.6 1.9 1.6 4.3 C1.6 6.2 3.4 8.4 6 12 C8.6 8.4 10.4 6.2 10.4 4.3 C10.4 1.9 8.5 0 6 0 Z M6 2.6 C7.5 2.6 8.7 3.8 8.7 5.2 C8.7 6.6 7.5 7.8 6 7.8 C4.5 7.8 3.3 6.6 3.3 5.2 C3.3 3.8 4.5 2.6 6 2.6 Z`
  两个形状必须彼此可辨:图钉有**宽平的头 + 靠下的法兰 + 细针**,地图标记是**平滑的水滴 + 上部的孔**。
- **竖条宽度 3px**(与 `.markdown-body blockquote` 的 `border-left: 3px` 一致;它是 `box-shadow` 的偏移分量,**不是** `--space-*` 刻度值 —— L-1…L-5 从未覆盖 `box-shadow` 分量,冻结轮的 `inset 3px 0 0` 已是既有先例,这一点必须写进围栏外注释,否则会被读成疏漏)。**标题只改 `color`,不改 `font-weight`。**

**本计划关闭的需求:** VISUAL-04、VISUAL-05。**本计划不触碰:** TYPE-01…03(Plan 01)与 VISUAL-01…03(Plan 02)的交付物;`frontend/app.js` / `index.html` / `vendor/` / `ui-states/` 零 diff;`scripts/check-02-contrast.py` 代码零改动;`.collapse-indicator` 零改动(D-23)。

**本计划的最后一项任务是 D-05 的连带义务,不是可选项:** `frontend/style.css` 与 `scripts/check-05-ui-uat.py` 都在 `idi-04.1-radix` 的 `covered_files` 里(`covered_digest` 是原始字节 sha256),本阶段的编辑使它的 `passed` 指纹 stale。本次 stale 的成因是**内容真变**,故走**重新验证**而非补指纹 —— 逐条重跑它的 `human_verification` 三项与四条守卫,并**从 HEAD 重算全部数值**。指纹的写回由编排器的 `/gsd-verify-work idi-04.1-radix` 完成,不在本计划内。
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
@.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-PATTERNS.md
@.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md
@.planning/phases/idi-04.1-radix/idi-04.1-VERIFICATION.md
@.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-01-PLAN.md
@.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-02-PLAN.md
@frontend/style.css
@frontend/index.html
@scripts/check-05-ui-uat.py
@scripts/check-02-contrast.py
</context>

## Artifacts this phase produces

**Plan 03 新建/改写的符号(本阶段最后一批):**

| 类别 | 符号 | 位置 | 备注 |
|---|---|---|---|
| 新 CSS 自定义属性 | `--color-marker-active` | `frontend/style.css` 围栏,紧随 `--color-action-*` 族之后 | tier-2,值 `var(--radix-blue-11)` |
| 新 CSS 自定义属性 | `--icon-pin` | 围栏内 | data-URI,零颜色信息 |
| 新 CSS 自定义属性 | `--icon-location` | 围栏内 | data-URI,零颜色信息 |
| 新清单行 | `/* PAIR --color-marker-active ON --color-surface-page TEXT */` | 围栏清单 | 4.65 |
| 新清单行 | `/* PAIR --color-marker-active ON --color-surface-page NON-TEXT */` | 围栏清单 | 4.65 |
| 新选择器(追加在文件末尾) | `#session-panel:not(.hidden) .panel-header` 等三条 | `style.css` 末尾 | 1-2-0 |
| 新选择器(追加在文件末尾) | `#session-panel:not(.hidden) .panel-header h2` 等三条 | `style.css` 末尾 | 1-2-1 |
| 改写规则体 | `.annotation-quote::before` | `style.css:836` | 原地改写为 mask 盒模型 |
| 改写规则体 | `.verdict-location::before` | `style.css:1021` | 同上,换 `--icon-location` |
| 新增读取器 | `read_pseudo_style(page, sel, pseudo, prop)` | `scripts/check-05-ui-uat.py` | 伪元素 computed style |
| 新增断言标签 | 活动态标记(p1 / p3 / checking 三态 + `#ai-panel` 与 `#doc-panel-header` 对照组) | item4 | 复用 `parse_box_shadow` |
| 新增断言标签 | 活动面板 `h2` color == `--color-marker-active` | item4 | 三条 |
| 新增断言标签 | 两处 `::before` 的 width / height / background-color / mask-image | item6(item 引用行)+ item4(裁决位置行) | 需 `renderVerdictCard` 探针 |
| 新增探针 | `renderVerdictCard({number, location, issue, suggestion}, 'p2')` | item4 | 应用自身的渲染函数,零网络 |
| 新增快速切片 | item_smoke 一条活动态标记断言 | item_smoke | PATTERNS 建议先扩它 |

本阶段(Plan 01 + Plan 02 + Plan 03)的完整新建符号清单到此结束;未列在三张表里的符号即既有符号。

<tasks>

<task type="tracer">
  <name>Task 1 (tracer): 活动面板标记端到端 —— 围栏新令牌 → 两条追加规则 → 三态运行时断言</name>
  <files>frontend/style.css, scripts/check-05-ui-uat.py</files>
  <reversibility rating="costly">D-18:令牌名一旦落地即与 04.1 的 D-02 一样被下游引用冻结(围栏、两条规则、两条清单行、check-05 的断言、以及 60/30/10 的偏离登记 A-7 都引用它);改名要同批改五处。</reversibility>
  <read_first>
    - `frontend/style.css` L117-L182 —— 围栏 tier-2 的声明形状与注释 register(`--color-marker-active` 要插在 `--color-action-*` 族之后)
    - `frontend/style.css` L912-L920 —— `#round-doc.round-frozen` 的**机制范本与注释 register**:`box-shadow: inset 3px 0 0 var(--color-action-warning)`,以及注释里「box-shadow 不参与布局 ⇒ 零位移,绝不用 border-left」的原文。本任务复制该机制与该 register
    - `frontend/style.css` L421-L434 —— `.panel-header`(flex / `height: 36px` / `justify-content: space-between` / `border-radius: var(--radius-md)`)与 `.panel-header h2`(`--fw-medium`)
    - `frontend/style.css` L353-L357 —— `.hidden { display: none !important }` 及其注释(机制而非样式;三个 1-0-0 竞争者)
    - `frontend/style.css` L1042-L1054 —— 文件末尾的两个**追加式**块与其注释(「追加在文件末尾 —— 硬规则 3」的既有先例;新规则追加在 L1054 之后)
    - `frontend/index.html` L10-L70 —— 四个 section 的 DOM;`#ai-panel` 的 `.panel-header` 与 `#doc-panel-header` 的位置
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`## VISUAL-04 落地规格 —— 侧栏活动面板标记` 全节 —— 范围修正(D-16)、形态与实现(D-17)的四条承重决定、层叠核账表、与 `.hidden` 机制的关系
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`### 活动面板标记色(VISUAL-04 / D-18)` —— 为什么新开令牌、为什么是蓝、为什么是 blue-11、60/30/10 的登记
    - `scripts/check-05-ui-uat.py` L479-L546 —— `parse_box_shadow` 与 `check_frozen_marker`(**直接复用**的读取器与断言 idiom:解析成 `{inset, color, x, y, blur, spread}`,逐分量断言,期望侧用运行时解析的令牌值,缺失或不可解析记 `blocked`)
    - `scripts/check-05-ui-uat.py` L310-L460 —— `make_fixture` / `enter_project` 与 `STATES`(五个磁盘状态样本;`checking` 样本可用)
    - `scripts/check-05-ui-uat.py` L707-L810 —— item4 全文(新断言的落点;`p1` / `p3` / `archive` 已进入,`checking` 需新增一次 `make_fixture` + `enter_project`)
  </read_first>
  <action>
    **第 1 步 —— 围栏内新增 tier-2 令牌 `--color-marker-active`(D-18)。** 在 `frontend/style.css` 围栏内 `--color-action-irreversible-fg` 之后、`/* Tier 2 — event-kind vocabulary */` 之前插入一行:`--color-marker-active: var(--radix-blue-11);`,并配一条注释写明:(a) 它承载**侧栏活动面板标记**,不是「主要动作」—— 故不复用 `--color-action-primary`(那个名字说的是主要动作,拿它做面板指示器会让名说谎;04.1 的 D-03 为同一条方法论付过代价);(b) 选蓝的理由(琥珀已承载警告与冻结轮两重含义,蓝在本系统是信息/流式色,与琥珀明确分离);(c) 指向的是**已声明、已消费**的 `--radix-blue-11`,故本阶段**新增 tier-1 primitive = 0**。**不得**新增任何 `--radix-blue-*` 声明。

    **第 2 步 —— 两条规则追加在文件末尾(D-17,硬规则 3)。** 在 `style.css` 最后一行(L1054 的 `button, input, select { color: var(--color-text); }`)之后追加两条规则:
    - 第一条:`#session-panel:not(.hidden) .panel-header,` / `#annotations-panel:not(.hidden) .panel-header,` / `#checks-panel:not(.hidden) .panel-header { box-shadow: inset 3px 0 0 var(--color-marker-active); }`
    - 第二条:`#session-panel:not(.hidden) .panel-header h2,` / `#annotations-panel:not(.hidden) .panel-header h2,` / `#checks-panel:not(.hidden) .panel-header h2 { color: var(--color-marker-active); }`
    并配一条注释,把四条承重决定写进去:**(1)** 用 `box-shadow: inset` 而非 `border-left` —— `box-shadow` 不参与布局、零位移,`border-left` 会给标题行加 3px 宽度把 `#pending-count` / `#check-state` 往右推(冻结轮已是这个写法);**(2)** 竖条落在 `.panel-header` 而非 `<section>` —— 三个 section 的子元素都带背景色(`.chat-bubble` / `.annotation-item` / `.event-list` / `.panel-body`),inset shadow 画在元素自身背景层上,带背景的子元素会盖住左边缘的竖条,而标题行没有带背景的左边缘子元素;**(3)** 标题只改 `color` 不改 `font-weight` —— D-09 已把 chrome 标题统一为 500,且 `.panel-header` 是 `height: 36px` + `space-between` 的 flex 行,改字重会移动行内徽标;**(4)** `3px` 是 `box-shadow` 的偏移分量、**不是** `--space-*` 刻度值,04-UI-SPEC 的 L-1…L-5 从未覆盖 `box-shadow` 分量,冻结轮的 `inset 3px 0 0` 已是既有先例 —— **这一点必须写明,否则会被读成新增了一个刻度外字面量**。`#doc-panel-header` 虽是 `.panel-header` 但不被三条 ID 选择器匹配,故无意外覆盖。

    **第 3 步 —— 清单新增两条配对。** 在围栏清单的 TEXT 组追加 `/* PAIR --color-marker-active ON --color-surface-page TEXT */`,在 NON-TEXT 组追加 `/* PAIR --color-marker-active ON --color-surface-page NON-TEXT */`,并在它们之前加一行注释写明落地面:`#session-panel` / `#annotations-panel` / `#checks-panel` 都在 `#main-pane` 内,而 `#main-pane` 及其祖先**无背景声明**(`html, body` 才是 `background: var(--color-surface-page)`),故底色是 `--color-surface-page`。清单规模 45 → **47 对(35 TEXT + 12 NON-TEXT)+ 1 ORDER**;两条新配对实测均 **4.65**(3px 竖条是非文本状态指示器 SC 1.4.11,面板标题是文本 SC 1.4.5)。**不得**新增第二条 `--color-marker-active` 之外的任何配对。

    **第 4 步 —— 运行时断言(D-16 / D-17 / D-03 第一类)。** 在 `scripts/check-05-ui-uat.py` 里:
    (a) 新增一个 `check_active_marker(page, item, label_prefix, panel_selector)` 读取器,复用既有的 `parse_box_shadow` 与 `check_frozen_marker` 的 idiom:读 `read_style(page, "<panel> .panel-header", "box-shadow")`,期望侧由 `resolve_color(page, "--color-marker-active")` 在运行时解析,逐分量断言 `inset` / `x == "3px"` / `y == "0px"` / `blur == "0px"` / `spread == "0px"` / 颜色相等;`box-shadow` 缺失或不可解析、或令牌解析失败时记 `blocked`,绝不记 PASS。同时断言该面板的 `.panel-header h2` 的 computed `color` == 同一个运行时解析值。
    (b) 在 item4 里对**三个活动态样本**各调一次:`p1` → `#session-panel`、`p3` → `#annotations-panel`、`checking` → `#checks-panel`(后两者需要 `make_fixture("checking", tmp_root)` + `enter_project`,item4 目前只进了 `p1` / `p3` / `archive`)。
    (c) **对照组**(D-16 的核心):在同样三个样本下断言 `#ai-panel .panel-header` 的 computed `box-shadow` == `"none"`(它从不被 `.hidden`,不参与三选一推导),并断言 `#doc-panel-header` 的 `box-shadow` == `"none"`(它是 `.panel-header` 但不被三条 ID 选择器匹配 —— 无意外覆盖)。
    (d) 在 `item_smoke` 里扩一条活动态标记断言(快速反馈切片,先扩它)。

    **第 5 步 —— 实跑。** 实跑 CHECK-01 / CHECK-02(47 对)/ `--item smoke,4` 并记录原始输出。核对 `^\.hidden {` 仍为 1、`!important;` 声明数仍为 1(本任务新增 0 条 `!important`)、`@media` 计数仍为 0(硬规则 8)。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>non-zero exit, or the only stdout line is not exactly `PASS`</fails_when>
    <automated>python3 scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>the last line is not exactly `PASS: 0 failures`, or the command exits non-zero</fails_when>
    <automated>python3 scripts/check-02-contrast.py | grep '^PASS  ' | wc -l</automated>
    <fails_when>the count is not 47</fails_when>
    <automated>python3 scripts/check-02-contrast.py | grep '^PASS  4.65  --color-marker-active ON --color-surface-page' | wc -l</automated>
    <fails_when>the count is not 2 (one TEXT, one NON-TEXT)</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item smoke,4</automated>
    <fails_when>exit code is not 0, or the `=== 逐项结论 ===` block reports anything other than PASS for items 4 and smoke</fails_when>
    <automated>grep -o -- '--color-marker-active: var(--radix-blue-11);' frontend/style.css | wc -l</automated>
    <fails_when>the count is not 1</fails_when>
    <automated>grep -o 'box-shadow: inset 3px 0 0 var(--color-marker-active);' frontend/style.css | wc -l</automated>
    <fails_when>the count is not 1</fails_when>
    <automated>grep -o 'panel:not(.hidden) .panel-header' frontend/style.css | wc -l</automated>
    <fails_when>the count is not 6 (three ID selectors times two rules)</fails_when>
    <automated>bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>either script exits non-zero or prints anything other than `PASS`</fails_when>
    <automated>grep -o '@media' frontend/style.css | wc -l</automated>
    <fails_when>the count is not 0 (硬规则 8:本阶段不得引入 @media)</fails_when>
  </verify>
  <acceptance_criteria>
    - `--color-marker-active: var(--radix-blue-11);` 在围栏内恰出现 1 次,且它的行号**早于**两条追加规则的行号(同提交落地,Hard Rule 5)
    - tier-1 primitive 数仍为 25(`grep -oE '^[[:space:]]*--(white|radix-[a-z]+-[0-9]+):' frontend/style.css | wc -l` == 25)
    - tier-2 `--color-*` 名数 47 → 48(`grep -oE '^[[:space:]]*--color-[a-z0-9-]+:' frontend/style.css | wc -l` == 48)
    - 两条追加规则在文件**末尾**(其行号大于 `button, input, select` 那一行的行号),且共含 6 个 `:not(.hidden)` 选择器
    - 清单 `/* PAIR` 标记数 == 47,`/* ORDER` == 1;两条新配对实测均 4.65
    - 追加规则**不含** `border-left`,也**不含** `font-weight`(`grep -n -A 12 'panel:not(.hidden) .panel-header' frontend/style.css | grep -o 'border-left' | wc -l` == 0)
    - `^\.hidden {` == 1、`!important;` 声明数 == 1、`@media` == 0
    - item4 与 item_smoke 在 `p1` / `p3` / `checking` 三态下:活动面板的 `box-shadow` 语义成立、`h2` color == `--color-marker-active`;`#ai-panel .panel-header` 与 `#doc-panel-header` 的 `box-shadow` == `none`
    - `--item smoke,4` 全 PASS(0 FAIL / 0 BLOCKED)
  </acceptance_criteria>
  <done>活动面板标记落地(3px 蓝竖条 + 标题变色),`#ai-panel` 与 `#doc-panel-header` 对照组保持 `box-shadow: none`;清单 47 对 + `ORDER 0.363` 全 PASS;四条守卫与 `@media` 计数全绿。</done>
</task>

<task type="auto">
  <name>Task 2: 两处 emoji → 内联掩码字形(零颜色信息的 data-URI)</name>
  <files>frontend/style.css, scripts/check-05-ui-uat.py</files>
  <reversibility rating="costly">D-20:回退要恢复 `content: url()`、重新引入字面量例外 L-3、重调对齐 —— 三处必须同批改,且 L-3 的撤掉(A-1)与契约 Q7 第 2 条的作废(A-2)都要一并回退。</reversibility>
  <read_first>
    - `frontend/style.css` L834-L840 —— `.annotation-quote` 与 `.annotation-quote::before` 的**现状逐字**(规则体是单条 `content` 声明)
    - `frontend/style.css` L1019-L1023 —— `.verdict-location` 与 `.verdict-location::before` 的**现状逐字**
    - `frontend/style.css` L829-L833(`.annotation-item` 的 `background: var(--color-surface)`)与 L1012-L1018(`.verdict-card` 的 `background: var(--color-surface-warning-subtle)`)—— 两个图标的落地面,用来确认**不需要新增配对**
    - `frontend/style.css` L750-L758 —— `#chat-input-row input` 的 `box-shadow: var(--shadow-composer)`(围栏令牌被普通声明消费的 in-file 先例)
    - `frontend/style.css` L42-L70 —— 围栏 tier-1 的声明形状(两个 `--icon-*` 是围栏内的字面量,与 primitive 同形但不是颜色令牌)
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`## VISUAL-05 落地规格 —— 两处内联字形(D-20 / D-21 / D-22)` 全节 —— 机制对比表、围栏内两个令牌的声明形状、**令牌形状契约表**(6 条可机械核的约束)、两条伪元素规则的目标形态、**三条实现细节**、用色与对齐表
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`## 契约修正登记` 的 A-1 与 A-2 —— L-3 撤掉的唯一依据、Q7 第 2 条整条作废
    - `frontend/app.js` L1561-L1570 —— `#ai-panel-body` 的 `.collapsed` 切换与两处 `textContent` 赋值(**零改动的对象**;D-23 的根据)
    - `scripts/check-05-ui-uat.py` L240-L248(`read_style` 的现状 —— 它不接受伪元素参数,故需要新增读取器)、L955-L1002(item6 的全文 —— `.annotation-quote` 在其中的落点)、L707-L810(item4 —— `.verdict-location` 的落点)
    - `frontend/app.js` L675-L700 —— `renderVerdictCard(question, mode)` 的签名与 `'p2'` 模式下创建 `.verdict-location` 的路径(探针要调用它)
  </read_first>
  <action>
    **第 1 步 —— 围栏内新增两个 data-URI 令牌(D-20 / D-22)。** 在围栏内新增两行声明,形状为 `--icon-pin: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'%3E%3Cpath d='<路径>'/%3E%3C/svg%3E");` 与 `--icon-location: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'%3E%3Cpath d='<路径>'/%3E%3C/svg%3E");`。**路径数据取本计划 `<objective>` 里定稿的两串,逐字照抄。** 形状契约(可机械核,缺一即错):`viewBox='0 0 12 12'`;**恰 1 个 `<path>`**;**不得出现 `fill=` 属性**(mask 只看 alpha,默认黑即不透明);**data-URI 内零颜色信息** —— 不得出现 `%23`、`#`、`fill=`(这是撤掉字面量例外 L-3 的**唯一依据**);`xmlns` 必须带(无命名空间的 SVG 在部分引擎下不渲染);形状风格为**实心**;两个形状必须彼此可辨。**data-URI 内不得出现分号** —— `scripts/check-02-contrast.py` 的 `DECL_RE` 用 `[^;]+` 取声明值,一个分号会截断它。配一条注释写明:mask 只看 alpha ⇒ `<path>` 不带 fill ⇒ data-URI 内零颜色信息 ⇒ 契约例外 L-3 整个撤掉;`d` 数据由规划期手写,无外部来源、无许可证、无供应链面。

    **第 2 步 —— 两条伪元素规则原地改写(D-20 / D-21 / D-22)。** 把 `frontend/style.css:836` 的 `.annotation-quote::before` 规则体整条替换为 mask 盒模型:`content: '';`(空串,不带尾随空格)、`display: inline-block;`、`width: 12px;`、`height: 12px;`、`margin-right: var(--space-1);`、`vertical-align: -2px;`、`background-color: var(--color-text-secondary);`、`-webkit-mask-image: var(--icon-pin);`、`mask-image: var(--icon-pin);`、`-webkit-mask-size: 12px 12px;`、`mask-size: 12px 12px;`、`-webkit-mask-repeat: no-repeat;`、`mask-repeat: no-repeat;`、`-webkit-mask-position: center;`、`mask-position: center;`。`frontend/style.css:1021` 的 `.verdict-location::before` 同形改写,只把 `--icon-pin` 换成 `--icon-location`。**原地改写而非在文件末尾追加重复选择器** —— 两个选择器全文各只出现一次、**无竞争者**,故原地改写在层叠上等价于追加,且避免了在末尾留一条被覆盖的死规则(这是硬规则 3 的实质,不是例外)。三条实现细节缺一即错:**(1)** `margin-right: var(--space-1)` 是必需的 —— 原来的 `content` 自带一个尾随空格,`content: ''` 的 12px 盒没有,不加间距图标会贴住文字;**(2)** `-webkit-mask-*` 与 `mask-*` **都要写**(这是本阶段唯一允许的冗余声明:无前缀是现代 Chrome 的写法,前缀是 WebKit 系的写法);**(3)** `mask-repeat: no-repeat` 必须显式声明(默认值是 `repeat`),`mask-size` 也必须显式声明(SVG 有 viewBox 但无内在尺寸,`auto` 的落点依赖引擎)。

    **第 3 步 —— 运行时断言(硬规则 7)。** 在 `scripts/check-05-ui-uat.py` 里新增一个读取器 `def read_pseudo_style(page, selector, pseudo, prop)`,用 `getComputedStyle(el, pseudo)[prop]` 读伪元素的 computed style(既有的 `read_style` 不接受伪元素参数,不能直接复用)。然后:
    (a) 在 **item6** 里新增四条断言:`.annotation-quote::before` 的 `width` == `"12px"`、`height` == `"12px"`、`background-color` == `resolve_color(page, "--color-text-secondary")`、`mask-image` != `"none"`。item6 已经写出批注并渲染出 `.annotation-quote`,是这条断言的天然落点。
    (b) 在 **item4** 里新增同样的四条断言给 `.verdict-location::before`:先用应用自身的渲染函数把一张裁决卡渲染进 `#verdict-cards` —— `host.innerHTML = ''` 之后 `host.appendChild(renderVerdictCard({ number: 1, location: 'harness 探针位置', issue: 'i', suggestion: 's' }, 'p2'))`(`'p2'` 模式才会创建 `.verdict-location`;真实渲染路径,零网络、零 AI 调用)。元素未渲染出来时记 `blocked`,绝不记 PASS。
    (c) **不新增任何配对** —— 两个图标的落地面已被既有 TEXT 配对覆盖(`--color-text-secondary ON --color-surface` 5.62、`--color-text-secondary ON --color-surface-warning-subtle` 5.82);TEXT 阈值(4.5)严于 NON-TEXT 阈值(3.0),同一对 fg/bg 的 TEXT 通过即蕴含 NON-TEXT 通过,再加一条 NON-TEXT 配对是**同义反复**。这是刻意的零新增,不是遗漏。

    **第 4 步 —— Gate 5 / Gate 6 与实跑。** 实跑并记录:
    - **Gate 5**(mask data-URI 内零颜色信息,A-1 撤掉 L-3 的唯一依据):`grep -oE '%23[0-9a-fA-F]{3,8}' frontend/style.css | wc -l` 必须打印 `0`;并补两条同源的机械证据:`grep -oE "fill='" frontend/style.css | wc -l` == 0(不得有 fill 属性)。
    - **Gate 6**(`.collapse-indicator` 零改动,D-23 / Pitfall 7):`grep -n '^\.collapse-indicator' frontend/style.css` 恰 1 行且逐字节与 HEAD 相同 —— 用直接对源文件的字面断言来证明(`grep -o '.collapse-indicator { font-size: 20px; line-height: 1; }' frontend/style.css | wc -l` == 1),不用「git 的输出里不出现」这种把 `git` 放在管道非末段的形态(那样 git 失败会被吞掉,读起来像干净)。
    - 实跑 CHECK-01 / CHECK-02(47 对)/ `--item 4,6,smoke`,并核对 `frontend/app.js` 与 `frontend/index.html` 零 diff。
  </action>
  <verify>
    <automated>grep -oE '%23[0-9a-fA-F]{3,8}' frontend/style.css | wc -l</automated>
    <fails_when>the count is not 0 (Gate 5 — zero color information inside the mask data URIs is the sole basis for retiring literal exception L-3)</fails_when>
    <automated>grep -oE "fill='" frontend/style.css | wc -l</automated>
    <fails_when>the count is not 0 (a `fill` attribute would reintroduce color information and make L-3 un-retirable)</fails_when>
    <automated>grep -o 'mask-image: var(--icon-pin);' frontend/style.css | wc -l; grep -o 'mask-image: var(--icon-location);' frontend/style.css | wc -l</automated>
    <fails_when>either count is not 1</fails_when>
    <automated>grep -o "content: '';" frontend/style.css | wc -l</automated>
    <fails_when>the count is not 2 (both pseudo-element rule bodies must be rewritten in place)</fails_when>
    <automated>grep -o '.collapse-indicator { font-size: 20px; line-height: 1; }' frontend/style.css | wc -l</automated>
    <fails_when>the count is not 1 (Gate 6 — the selector's rule body must be byte-identical to HEAD; D-23 / Pitfall 7)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>non-zero exit, or the only stdout line is not exactly `PASS`</fails_when>
    <automated>python3 scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>the last line is not exactly `PASS: 0 failures`, or the command exits non-zero</fails_when>
    <automated>python3 scripts/check-02-contrast.py | grep '^PASS  ' | wc -l</automated>
    <fails_when>the count is not 47</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 4,6,smoke</automated>
    <fails_when>exit code is not 0, or the `=== 逐项结论 ===` block reports anything other than PASS for items 4, 6 and smoke</fails_when>
    <automated>git diff --stat -- frontend/app.js frontend/index.html</automated>
    <fails_when>the command prints a non-empty stat line (both files must be byte-identical to HEAD)</fails_when>
    <automated>ls frontend/vendor/</automated>
    <fails_when>the listing is anything other than exactly `marked.min.js`</fails_when>
  </verify>
  <acceptance_criteria>
    - 围栏内 `--icon-pin` 与 `--icon-location` 各恰 1 条声明;两者的 data-URI 各含恰 1 个 `<path>`、`viewBox='0 0 12 12'`、`xmlns`、**无 `fill=`**、**零 `%23` / `#`**
    - Gate 5:`grep -oE '%23[0-9a-fA-F]{3,8}' frontend/style.css | wc -l` == 0;`grep -oE "fill='" frontend/style.css | wc -l` == 0
    - `content: '';` 恰出现 2 次(两条伪元素规则原地改写);`.annotation-quote::before` 与 `.verdict-location::before` 各仍只出现 1 次(未在末尾追加重复选择器)
    - 两条规则体内 `-webkit-mask-*` 与 `mask-*` **成对**出现(`-webkit-mask-image` / `mask-image` / `-webkit-mask-size` / `mask-size` / `-webkit-mask-repeat` / `mask-repeat` / `-webkit-mask-position` / `mask-position` 各 2 次)
    - `margin-right: var(--space-1);` 在两处规则体内各出现 1 次
    - Gate 6:`grep -n '^\.collapse-indicator' frontend/style.css` 恰 1 行,且其内容逐字节为 `.collapse-indicator { font-size: 20px; line-height: 1; }`
    - item6 的 `.annotation-quote::before` 四条断言与 item4 的 `.verdict-location::before` 四条断言均存在且 PASS(未渲染出来时必须 BLOCKED,不得 PASS)
    - `--item 4,6,smoke` 全 PASS(0 FAIL / 0 BLOCKED);`check-02` 仍 47 对 + `ORDER 0.363`
    - `frontend/app.js` / `frontend/index.html` 零 diff;`frontend/vendor/` 仍只含 `marked.min.js`
  </acceptance_criteria>
  <done>两处 emoji 变为跟随令牌的掩码字形:12×12、`--color-text-secondary` 上色、`mask-image` 接上围栏令牌、data-URI 内零颜色信息(L-3 可撤);`.collapse-indicator` 与 `app.js` / `index.html` 零改动;`--item 4,6,smoke` 全 PASS。</done>
</task>

<task type="auto">
  <name>Task 3: D-05 连带义务 —— 复验 idi-04.1-radix(从 HEAD 重算,不补指纹)</name>
  <files>scripts/check-05-ui-uat.py</files>
  <read_first>
    - `.planning/phases/idi-04.1-radix/idi-04.1-VERIFICATION.md` frontmatter —— `covered_files` 清单(含 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`)、`covered_digest` 的形态(`v1:sha256:…`)、`human_verification` 的三项与 `behavior_unverified: 0`
    - `.planning/phases/idi-04.1-radix/idi-04.1-VERIFICATION.md` 正文 —— 37/38 的 must-haves 口径与那一条 `human_needed` 的性质
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`### D-05 连带义务 —— 本阶段必须复验 idi-04.1-radix` —— `covered_files` 逐行表、「义务(不是建议)」段、以及**复验时必须逐条确认的三处 04.1 结论**表(43 对 + `ORDER 0.363`;`--color-text-info ON --color-surface-info` = 4.53;冻结轮 `opacity 1` + `filter saturate(0.6)` + `inset 3px 0 0 --color-action-warning`;`--color-border-strong` 3.24 / 3.15;25 tier-1 / 47 tier-2 的数量)
    - `.planning/phases/idi-04.1-radix/idi-04.1-01-PLAN.md` 与 `idi-04.1-03-PLAN.md` —— 04.1 的四条守卫命令与它们的期望输出形态
    - `scripts/check-05-ui-uat.py` L549-L590(item2 的冻结轮 backstop —— 复验的三项之一)、L810-L950(item5 的两条需真实 AI 调用的冒烟,由 `--ai-smoke` 补齐)
  </read_first>
  <action>
    **本任务不改 `frontend/style.css`,也不改任何断言逻辑。** 它的产物是**复验证据**:逐条重跑 `idi-04.1-radix` 的验证项并**从 HEAD 重算全部数值**(D-05 明写:本次 stale 的成因是内容真变 —— 本阶段重写了 04.1 覆盖的两个文件 —— 故走**重新验证**而非补指纹),把结果写进本计划的 SUMMARY。

    **第 1 步 —— 重跑四条守卫并记录原始输出。** `bash scripts/check-01-token-conformance.sh`(期望 `PASS`)、`python3 scripts/check-02-contrast.py`(期望 `PASS: 0 failures` + 逐行比值)、`bash scripts/check-03-hidden-uniqueness.sh`(期望 `^\.hidden {` == 1)、`bash scripts/check-04-important-count.sh`(期望 `!important;` 声明数 == 1)。

    **第 2 步 —— 重跑 04.1 的三项 `human_verification`。** 按 `idi-04.1-VERIFICATION.md` frontmatter 的三项逐条执行并记录:①`scripts/check-05-ui-uat.py` 的 `## UI Considerations` backstop 陈述(16 条 E1…E16 的视觉/几何行为,其中 7 条含 CHECK-02 比值半边);②`--color-text ON --color-surface-mark` 的比值(该对**不在**围栏清单里,check-02 看不见它 —— 用与 `check-02` 同一模型独立算出并记录);③TOKEN-07 的「断言序关系」半场(`REQUIREMENTS.md` 标 `Complete`,但代码库里没有任何脚本比较四个 `--z-*` 的值 —— 这是**已由用户在 `VALIDATION.md` 裁定的 manual-only 处置**,复验时照实记录其状态,不得单方面翻转)。同时跑 `--item 1,2,3,4,6`(第 5 项的两条真实 AI 冒烟沿用已记录的 `--ai-smoke` 证据,或按需重跑并记录)。

    **第 3 步 —— 逐条核对 04.1 的三处结论未因本阶段的值改动而失效,并记录数量差值。** 逐条:
    - **43 对清单全 PASS + `ORDER 0.363`** → 本阶段后清单规模变 **47**;`ORDER` 的两个操作数(`--color-text-muted` / `--color-text`)本阶段未改值,故 `ORDER` **应仍为 0.363** —— 核对并记录实测值。
    - **`--color-text-info ON --color-surface-info` = 4.53**(0.03 余量)→ 未触碰,该行须**逐字不变**。
    - **冻结轮**:`opacity 1` + `filter saturate(0.6)` + `inset 3px 0 0 --color-action-warning` → 未触碰(本阶段新增的活动态竖条是**另一个**元素上的同形声明);`--item 2` 须仍 PASS。
    - **`--color-border-strong` = `--radix-gray-9`,实测 3.24 / 3.15** → 未触碰,check-02 两行须逐字不变。
    - **25 tier-1 / 47 tier-2 的数量** → tier-1 仍 **25**(本阶段新增 primitive = 0);tier-2 **47 → 48**(新增 `--color-marker-active`)。**这是 04.1 的 `## Color` 节里「47 个 tier-2」这一句在本阶段之后不再成立的地方 —— 不改 04.1 的文件**(改它会作废它自己的其余结论),只在复验记录里登记该差值。
    - **清单规模 43 → 47** 同理登记(04.1 的「43 对」是它那一代值层的真实数)。

    **第 4 步 —— 记录指纹的义务归属。** 在 SUMMARY 里明确写出:`idi-04.1-radix` 的 `covered_digest` 因本阶段改动了它的两个 `covered_files` 而 stale;**指纹的重新写回由编排器执行 `/gsd-verify-work idi-04.1-radix`**,不在本计划内 —— 本计划提供的是它的输入(重算后的数值与逐条核对结果)。**不得**自行改写 `idi-04.1-VERIFICATION.md` 的 frontmatter(那会让「谁改了什么」不可追溯)。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh</automated>
    <fails_when>non-zero exit, or any of the three scripts prints something other than `PASS`</fails_when>
    <automated>python3 scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>the last line is not exactly `PASS: 0 failures`, or the command exits non-zero</fails_when>
    <automated>python3 scripts/check-02-contrast.py | grep '^ORDER 0.363' | wc -l</automated>
    <fails_when>the count is not 1 (04.1's ordering assertion must survive unchanged)</fails_when>
    <automated>python3 scripts/check-02-contrast.py | grep '^PASS  4.53  --color-text-info ON --color-surface-info' | wc -l</automated>
    <fails_when>the count is not 1 (04.1's 0.03-margin pair must be byte-unchanged)</fails_when>
    <automated>python3 scripts/check-02-contrast.py | grep -E '^PASS  3\.(24|15)  --color-border-strong ON --color-surface' | wc -l</automated>
    <fails_when>the count is not 2 (04.1's border-strong lines must be byte-unchanged)</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 1,2,3,4,6</automated>
    <fails_when>exit code is not 0, or the `=== 逐项结论 ===` block reports anything other than PASS for items 1, 2, 3, 4 and 6</fails_when>
    <automated>grep -oE '^[[:space:]]*--(white|radix-[a-z]+-[0-9]+):' frontend/style.css | wc -l; grep -oE '^[[:space:]]*--color-[a-z0-9-]+:' frontend/style.css | wc -l</automated>
    <fails_when>the first count is not 25, or the second count is not 48 (tier-1 unchanged at 25; tier-2 grew 47 → 48)</fails_when>
    <automated>git status --porcelain -- .planning/phases/idi-04.1-radix/</automated>
    <fails_when>the output is non-empty (this task must not rewrite 04.1's verification report — the fingerprint refresh belongs to the orchestrator's verify-work step)</fails_when>
  </verify>
  <acceptance_criteria>
    - 四条守卫全绿:CHECK-01 `PASS`、CHECK-02 `PASS: 0 failures`、CHECK-03 `PASS`、CHECK-04 `PASS`
    - 04.1 的三处结论逐条核对并记录:`ORDER 0.363` 不变;`--color-text-info ON --color-surface-info` = 4.53 逐字不变;`--color-border-strong` 两行 3.24 / 3.15 逐字不变;冻结轮标记(`--item 2`)仍 PASS
    - 数量差值已登记:tier-1 25(不变)、tier-2 47 → 48、清单 43 → 47
    - `--item 1,2,3,4,6` 五项全 PASS(0 FAIL / 0 BLOCKED)
    - `.planning/phases/idi-04.1-radix/` 零改动(`git status --porcelain` 为空)—— 指纹写回明确留给编排器的 `/gsd-verify-work idi-04.1-radix`
    - SUMMARY 里逐条写出重算后的数值与三项 `human_verification` 的复核结论(含 TOKEN-07 序关系半场的 manual-only 状态照实记录)
  </acceptance_criteria>
  <done>D-05 的连带义务履行完毕:04.1 的四条守卫与三项人工验证项在 HEAD 上重跑通过,全部数值从 HEAD 重算,tier-1/tier-2/清单三处数量差值已登记,04.1 的报告文件零改动。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| `:not(.hidden)` → `.hidden` 机制 | 新规则**读取**面板的显隐状态,不修改它。`.hidden { display: none !important }` 承载六个元素、压制三个 1-0-0 竞争者,是本项目最硬的机制之一(硬规则 1) |
| 围栏内 data-URI → 浏览器渲染 | 两个手写 SVG data-URI 是唯一的新内容来源;不进 DOM、无脚本执行面、无外部 URL 抓取。零颜色信息是撤掉字面量例外 L-3 的唯一依据,必须机械可核 |
| `scripts/check-02-contrast.py` → 上游文档 | 比值的唯一仲裁者;blue-11 的 4.65 由实算给出,不采信上游 AA 论断 |
| 本阶段无新增网络 / 输入 / 依赖面 | `frontend/app.js` / `index.html` / `vendor/` 零 diff;零新增文件、零新增依赖、零构建步骤 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-05-01 | Elevation of Privilege | `#btn-authorize`(G3 授权门)的视觉形态 | high | mitigate | 本计划不改三段坡道(Plan 02 已交付),但必须复跑 D-04 的三档两两不同断言不回归;`--color-action-irreversible*` 的单消费者不变量(D-15)在复验中一并核对 |
| T-idi-05-02 | Tampering | `.hidden` 机制与新规则的层叠 | medium | mitigate | CHECK-03(`^\.hidden {` == 1)与 CHECK-04(`!important;` 声明数 == 1)每任务复跑;新规则追加在文件末尾且特异性为 1-2-0 / 1-2-1,靠 ID 分量取胜;本计划新增 0 条 `!important`、0 条 `@media` |
| T-idi-05-03 | Tampering | 两处 data-URI 的内容 | low | accept | 手写、无外部来源、无许可证、无供应链面;不进 DOM,故无脚本执行面;data-URI 内零颜色信息由 Gate 5 机械断言;`<path>` 不带 fill 由第二条断言钉住 |
| T-idi-05-04 | Denial of Service | 渲染回归(标记可见性 / 图标对齐) | medium | mitigate | 每个 `style.css` 任务带至少一项运行时验证(硬规则 7):活动态标记在 `p1` / `p3` / `checking` 三态实读,`#ai-panel` 与 `#doc-panel-header` 作对照组;两处 `::before` 的 computed 尺寸 / 色 / `mask-image` 实读。**基线对齐(`vertical-align: -2px`)是计算样式看不见的实测项**,已作为 E6 / E7 的 backstop 陈述记录,由人工在渲染结果上核(05-N-5) |
| T-idi-05-05 | Information Disclosure | 本阶段的改动内容 | low | accept | 改动只有 1 个颜色令牌、2 个 data-URI 令牌、2 条追加规则、2 条清单行、2 处伪元素规则体与注释;无用户数据、无网络请求、无外部资源 |
| T-idi-05-SC | Tampering | npm / pip / cargo 安装 | high | mitigate | 本阶段零安装(硬规则 6):不新增依赖、文件或构建步骤;`ls frontend/vendor/` 断言仍只含 `marked.min.js`。无 `[ASSUMED]` / `[SUS]` 包,故无需 package-legitimacy 人工签核门 |
</threat_model>

<verification>
- `bash scripts/check-01-token-conformance.sh` → `PASS` / exit 0
- `bash scripts/check-03-hidden-uniqueness.sh` → `PASS`(`^\.hidden {` == 1)
- `bash scripts/check-04-important-count.sh` → `PASS`(`!important;` 声明数 == 1)
- `python3 scripts/check-02-contrast.py` → `PASS: 0 failures`,**47 对(35 TEXT + 12 NON-TEXT)+ `ORDER 0.363`**
- `.venv/bin/python scripts/check-05-ui-uat.py --item 1,2,3,4,6` → 五项全 PASS(0 FAIL / 0 BLOCKED)
- **Gate 5**:`grep -oE '%23[0-9a-fA-F]{3,8}' frontend/style.css | wc -l` → `0`;`grep -oE "fill='" frontend/style.css | wc -l` → `0`
- **Gate 6**:`grep -o '.collapse-indicator { font-size: 20px; line-height: 1; }' frontend/style.css | wc -l` → `1`(该选择器的规则体与 HEAD 逐字节相同)
- Gate 2:`comm -23 <(grep -o 'var(--[a-z0-9-]*' frontend/style.css | sed 's/var(//' | sort -u) <(grep -o '\-\-[a-z0-9-]*:' frontend/style.css | sed 's/:$//' | sort -u)` 输出为空(每个被消费的自定义属性都已声明)
- Gate 3:`ls frontend/vendor/` 只有 `marked.min.js`;`git diff --stat -- frontend/app.js frontend/index.html` 为空
- `grep -o '@media' frontend/style.css | wc -l` → `0`(硬规则 8)
- tier-1 == 25;tier-2 `--color-*` == 48
- D-05:`.planning/phases/idi-04.1-radix/` 零改动;复验数值已记录在 `idi-05-03-SUMMARY.md`,指纹写回留给编排器的 `/gsd-verify-work idi-04.1-radix`
</verification>

<success_criteria>
- 侧栏当前活动面板可辨认(3px 蓝竖条 + 标题变色),`#ai-panel` 与 `#doc-panel-header` 不被误标记(VISUAL-04 / SC4)
- 两处标记以内联掩码字形呈现,`frontend/vendor/` 无新增文件、无 CDN `<link>`(VISUAL-05 / SC5)
- `check-02` 47 对全 PASS,`ORDER 0.363` 与 04.1 的三处结论逐字不变
- `.collapse-indicator`、`app.js`、`index.html` 零改动
- D-05 的连带义务履行完毕,复验证据齐备且数量差值已登记
</success_criteria>

<output>
Create `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-03-SUMMARY.md` when done
</output>
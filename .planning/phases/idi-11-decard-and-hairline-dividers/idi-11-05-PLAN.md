---
phase: idi-11-decard-and-hairline-dividers
plan: 05
type: execute
wave: 5
depends_on:
  - idi-11-01
  - idi-11-02
  - idi-11-03
  - idi-11-04
files_modified:
  - frontend/style.css
  - scripts/check-09-idi09-validation.py
autonomous: true
gap_closure: true
requirements:
  - SURF-01
  - SURF-02
  - SURF-03
  - DIV-01
  - DIV-02
  - DIV-03
  - REG-01
  - REG-02
  - REG-03

estimate:
  tokens: 80000
  raw_tokens: 80000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- BINDING-1 —— 窗口边缘发丝线(BLOCKER,DIV-02 / D-11-10)----
    - "**5 个样本状态里,任何一条**被画出来的**发丝线都不落在窗口边缘**(`#main-pane` 的 `top == 0` 处)。独立验证的原始缺陷是:p3 / checking / archive 下可视的第一个面板(`#annotations-panel` / `#checks-panel`)带 `border-top` 且 `rect.top == 0.00` ⇒ 5 个样本里 3 个在窗口边缘多画一条设计明令禁止的线(像素级:y=0 内容列 `rgb(217,217,217)`)。修法由用户逐项裁定:**纯 CSS 下边线** —— 规则由「除 DOM 首个外都加上边线」改为「除 DOM 末个外都加下边线」(`D-11-10` 的实现路线裁定,2026-09-28,不得改选)"
    - "**每个样本状态里,可见的发丝线数恰等于「可见面板数 − 1」**(5 个样本里可见面板恒 2 个 ⇒ 恒 1 条可见发丝线)。契约不是「恒 1 条」而是「每对相邻可见面板之间恰 1 条、窗口边缘 0 条」;`#ai-panel` 是 DOM 末子元素且恒可见,故「除 DOM 末个外都加下边线」≡「除最后一个**可见** section 外都加下边线」"
    - "`frontend/style.css` 第 856 行**就地改写**(不是追加覆盖):选择器改为 `#main-pane > section:not(:last-child)`,声明由 `border-top` 改为 `border-bottom`,线色与线宽逐字不变(仍 `1px solid var(--color-border-subtle)`,取既有语义令牌 gray-6,`D-11-8`)。规则的**源码位置一字未移**(「追加,不重排」纪律)"
    - "`frontend/style.css` 第 828-855 行那段**承重注释**已如实改写:新机制键控于「非 DOM 末子元素」而非「非 DOM 首子元素」;**该机制成立的前提被显式登记** —— `#ai-panel` 是 `#main-pane` 的 DOM 末子元素,且 `frontend/app.js` 从不给它加 `.hidden`(前提一旦被破坏,规则即失效)。**不得**留下与代码矛盾的注释(本项目反复为此付过代价);`#main-pane > section` 规则体内那句「后者只给后三个 section 补回一条上边线」的旧机制描述一并改写,`#main-pane` 规则体**自身**注释(`:781`)里那句旧机制描述(分区机制由相邻兄弟规则的一条上边线承担)同样一并改写 —— **描述发丝线机制的三处注释必须全部与代码一致**"
    # ---- BINDING-1 —— 判据扩写与变异证明 ----
    - "`scripts/check-09-idi09-validation.py` 的 **c4 已扩写**:在**至少一个 `#session-panel` 被隐藏的状态**上断言「可视的第一个面板顶部无发丝线」。采用**更强的做法**:对 `c05.STATES` 全部 5 个样本状态**逐状态**断言 ——(i) 可视的第一个面板 `border-top-width == 0px`;(ii) 可见发丝线数 == 可见面板数 − 1;(iii) 没有发丝线落在窗口边缘。**不得**降级为「只断言规则被写下了」"
    - "**c1 / c4 的边框宽度断言已随规则换向**(`border-top` → `border-bottom`,宿主由后三个改为前三个)—— 这是 BINDING-1 第 1 条改写的**机械后果**,不是范围扩张:规则从「后三个面板的上边线」变成「前三个面板的下边线」后,仍在断言 `border-top-width == 1px` 的旧判据会**变红**,而那不是门在正确工作,是判据仍在断言一条已被裁定改变的事实(`REG-01`)。c1 / c4 的断言**零条删除、零条降级**,只换向"
    - "**变异测试至少两条,逐条给出真实「变异 → FAIL」读数**(`D-11-13` 的纪律:在**已提交的树**上做,定向 `git checkout -- frontend/style.css` 还原,**禁用 `git stash`**;还原后 `git diff --exit-code` rc=0 且 `git hash-object` 逐字节相同):(M1) 把第 856 行的选择器与声明还原成改动前的相邻兄弟形态(`+ section` + `border-top`)⇒ 扩写后的 **c4 必 FAIL**;(M2) 给新规则补一条 `border-top: 1px solid var(--color-border-subtle);` ⇒ 扩写后的 **c4 必 FAIL**;(M3) 把 `#doc-panel` 的 `background` 改归另一档 ⇒ **c2 必 FAIL**。每条须给出 FAIL 原文与退出码,不得只声明做过"
    - "`check-09 --item c1,c2,c3,c4,c5` 在改动后的树上 `exit=0`、`0 FAIL`、`0 BLOCKED`;每个 item 的断言数**只增不减**(HEAD 基线:c1 59 / c2 17 / c3 6 / c4 20 / c5 5)"
    # ---- BINDING-1 —— 1px 级几何变化的运行时确认 ----
    - "1px 级几何变化**由运行时读数确认,不是推断**:旧机制把那条线记在 `#ai-panel` 的 `border-top` 上(p1 实测 `#ai-panel` `rect.top = 767.00`),新机制把它记在**可见面板的 `border-bottom`** 上 ⇒ 预期 `#ai-panel` 的 `rect.top` 由 `767.00` 变 `768.00`(总高不变,1px 位移)。改动**前/后**的并排读数已在真实浏览器里取得并落盘登记;若某条门因此变化,按 `D-11-16` 的分诊口径处置(先问「事实是否被改变」),**不得为了让旧数字成立而回退**(`D-11-16` 的显式禁令)"
    # ---- BINDING-2 —— 围栏内三处被本阶段自己账目推翻的现在时陈述 ----
    - "`frontend/style.css` 围栏内三处**现在时陈述**已改写为 Phase 11 之后的事实,**历史段落逐字保留、不得删除**:(1) `--color-surface-page` 的消费者由「exactly ONE (`html, body`)」改为**四个**(`html, body` / `#main-pane > section` / `#doc-panel` / `#doc-panel-header`),并写明「改这个值会同时重绘页面、四个面板与 sticky 表头」—— 旧句里「nothing else needs synchronising」是更危险的那一半;(2) `--color-marker-active` 在统一白面上的实测由 `4.65`(margin `0.15`)改为 `4.77`(margin `0.27`);(3) gray-9 的白面读数由 `3.24` 改为 `3.32`(`3.15` 那一半仍正确,不动)。**不得顺手改任何值、不得新增令牌、不得动 `check-02` 的阈值或 PAIR 清单**;围栏内注释**不得**出现「令牌名 + 冒号」(`check-02` 的 `DECL_RE` 扫围栏全文含注释),也**不得**点名两个已删卡片令牌(围栏子串计数须为 0)"
    # ---- BINDING-3 —— 第五个容器的统一面断言 ----
    - "`scripts/check-09-idi09-validation.py` 的 **c2 已补上 `#doc-panel` 自身底色的断言**:`#doc-panel` 计算底色 == body 计算底色(复用 c2 内已算好的 `body_bg` 与已读到的 `bg`),并补字面量那一半(`SURFACE_PAGE_LITERAL`)。修前 c2 只在第 322 行把 `#doc-panel` 的底色**读进 `bg`** 却从无断言消费它 ⇒ 面板被重新上色成任何颜色时本门全绿(表头自绘背景,c2 的 header 断言仍会过;`check-05` 也不断言 `#doc-panel` 底色)⇒ 本阶段头号交付物的**五分之一没有门**"
    # ---- 门禁收口 ----
    - "`check-01` … `check-04`、`check-05`(全量)、`check-06`、`check-07`、`check-09`(c1..c5)、`check-10`、两个探针、`node --check frontend/app.js`、pytest 基线逐条复跑,**零新增失败**;`check-05 --item 8` 与 `--item 9` 另以独立日志复跑。每条门的**原始输出与退出码**落盘到 `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/`(沿用 `idi-11-04` 的「一个门一个文件」落盘先例;写进**子目录**以免覆盖 `idi-11-04` 落盘的对照基线)"
    - "`check-05` 全量运行的 `exit=2` **仍只因 item 5 的两条 `--ai-smoke` 腿按设计 BLOCKED**(item 5 的 BLOCKED 计数仍为 **2**),不是回归;`item 8` 仍 `PASS`、`item 9` 仍 `PASS`。任何 FAIL 或**新增** BLOCKED 都是缺口,须停下报回"
    - "pytest 基线不降:`.venv/bin/python -m pytest backend/tests -q --tb=short` → **219 passed / 6 skipped**(必须用项目 `.venv`;环境 `python3` 是 miniconda,会让 4 个 `ai_caller` 测试假失败)"
    - "**零范围外改动**:`frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**` / `scripts/check-05-ui-uat.py` / `scripts/check-02-contrast.py` / `scripts/check-10-idi10-validation.py` 与其它任何门逐字节未改。`WR-01`(check-05 的 `.hint` 断言)、`IN-01` / `IN-02`、`G2`、`999.2`、暗色模式、Nyquist 缺口、图标与空状态、`.overlay-card` 底色、`G1-01` / `REG-04` / `VIS-01` 全部**不碰**"

  artifacts:
    - path: "frontend/style.css"
      provides: "第 856 行的发丝线规则就地改写为「非 DOM 末子元素加下边线」;第 828-855 行承重注释如实改写并登记机制前提;围栏内三处现在时陈述改写为 Phase 11 之后的事实"
      contains: "#main-pane > section:not(:last-child) { border-bottom: 1px solid var(--color-border-subtle); }"
    - path: "scripts/check-09-idi09-validation.py"
      provides: "c1 / c4 的边框宽度断言换向(border-top → border-bottom);c4 新增 5 状态逐状态发丝线普查(可视首个面板无顶线 + 可见发丝线数 == 可见面板数 − 1 + 无线落窗口边缘);c2 新增 #doc-panel 自身底色断言"
      contains: "HAIRLINE_CENSUS_JS"
    - path: ".planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/"
      provides: "改动前/后的几何并排读数 + 15 条门的原始输出与退出码(一个门一个文件)"
      contains: "=== 逐项结论 ==="

  key_links:
    - from: "`#main-pane > section:not(:last-child)` 的 `border-bottom`"
      to: "`#ai-panel` 是 `#main-pane` 的 DOM 末子元素且从不被 `.hidden` 隐藏这一事实"
      via: "规则键控于「非 DOM 末子元素」⇒ 只有当 DOM 末子元素恒可见时,它才等价于「非最后一个**可见** section」;前提一旦被破坏,最后一个可见面板会多画一条下边线"
      pattern: "not\\(:last-child\\)"
    - from: "c4 的逐状态发丝线普查"
      to: "5 个样本状态里「可视的第一个面板」"
      via: "在 `#session-panel` 被隐藏的状态(p3 / checking / archive)上断言可视的第一个面板顶部无发丝线 —— 旧 c4 只在 p1 上跑,而 p1 下 `#session-panel` 恰是可视的第一个面板 ⇒ 旧断言在唯一不可能出缺陷的状态里恒真、对本缺陷结构性失明"
      pattern: "HAIRLINE_CENSUS_JS"
    - from: "c2 新增的 `#doc-panel` 底色断言"
      to: "围栏内 `--color-surface-page: var(--white);`"
      via: "`#doc-panel` 计算底色 == body 计算底色(统一面)+ 写死字面量 ⇒ 面板被重新上色时本门可见"
      pattern: "#doc-panel 计算底色 == body 计算底色"

  prohibitions:
    - statement: "不得改选实现路线。用户 2026-09-28 已逐项裁定走**纯 CSS 下边线**;`section.hidden + section:not(.hidden) { border-top: none }` 这条路线已被验证者显式否决(它会同时抹掉 p3 下 `#checks-panel → #ai-panel` 的分隔线)。**若方案需要动 `frontend/app.js`(例如加类键控规则),那是选错了实现方式的信号 —— 停下,回到 `:not(:last-child)` 路线。**"
      status: active
      verification: flagged
    - statement: "不得为了让门绿、或为了让某个旧读数继续成立,而删除 / 降级 / 放宽任何断言、阈值或判据,也不得回退已裁定的产品改动。`#ai-panel` 的 `rect.top` 由 `767` 变 `768` 是**事实被如实登记**,不是回归"
      status: active
      verification: flagged
    - statement: "不得修改 `scripts/check-05-ui-uat.py`(只读运行它)、`scripts/check-02-contrast.py`、`scripts/check-10-idi10-validation.py`、`frontend/app.js`、`frontend/index.html` 与任何后端文件。围栏内不得出现「令牌名 + 冒号」,不得点名两个已删卡片令牌,不得改任何**值**"
      status: active
      verification: flagged
    - statement: "变异测试的还原**禁用 `git stash`**(它跨工作树共享,本项目明令禁止),一律 `git checkout -- frontend/style.css`,并以 `git diff --exit-code` rc=0 与 `git hash-object` 逐字节相同两道独立证据收口"
      status: active
      verification: flagged
---

<objective>
收口 Phase 11 独立验证报出的**一个 BLOCKER 与两条 Warning**,范围由用户 2026-09-28 逐项裁定,**不得扩张**:

**BINDING-1(BLOCKER,DIV-02 / D-11-10)** —— `frontend/style.css:856` 的 `#main-pane > section + section { border-top: … }` 按 **DOM 相邻** 判定;`#session-panel` 是 DOM 第一个 section 故永不带线,但 `frontend/app.js:363` 在非 phase1/phase12 状态给它加 `.hidden` ⇒ 这些状态下**可视的**第一个面板是 `#annotations-panel`(p3)或 `#checks-panel`(checking / archive),它们各自带 `border-top` 且落在 `#main-pane` 的 `top == 0`(窗口边缘)⇒ **5 个样本里 3 个多画一条设计明令禁止的窗口边缘线**。用户裁定走**纯 CSS 下边线**:规则改为「除 DOM 末个外都加下边线」。同时扩写 `check-09` 的 c4 —— 现行「第一个面板顶部不画线」判据只在 `p1` fixture 上运行,而 p1 下 `#session-panel` 恰是可视的第一个面板 ⇒ 该断言在**唯一不可能出缺陷的状态**里恒真,对本缺陷结构性失明(缺陷存在的树上 `check-09 --item c1,c2,c3,c4` 仍 `exit=0`、0 FAIL)。并以变异测试证明新判据真的会失败(`D-11-13`)。

**BINDING-2(WR-02)** —— `frontend/style.css` 围栏内三处**现在时陈述**被本阶段自己的账目推翻(`:136-137` 的「exactly ONE consumer」、`:185-188` 的「4.65 / margin 0.15」、`:93` 的「gray-9 = 3.24 / 3.15」)。围栏是**权威令牌记录**,只改现在时陈述,不删历史段落。

**BINDING-3(WR-03)** —— `check-09` 的 c2 在第 322 行把 `#doc-panel` 的底色读进 `bg` 却从无断言消费它 ⇒ 本阶段头号交付物的**五分之一没有门**。补一条 `#doc-panel` 计算底色 == body 计算底色的断言。

**Purpose:** 三条都是「门绿着在看」形态:契约被违反 / 权威记录说谎 / 交付物的一部分无门。本仓库的立场是「一条不能失败的门比没有门更糟」,故三条必须同一次收口,且每条都以**运行时读数**或**变异 FAIL** 取证,不接受「看着一样」。

**Output:** `frontend/style.css` 的第 856 行规则与第 828-855 行注释就地改写、围栏内三处现在时陈述改写;`scripts/check-09-idi09-validation.py` 的 c1/c4 换向 + c4 逐状态普查 + c2 新增 `#doc-panel` 断言;三条变异的真实 FAIL 读数;改动前后的几何并排读数;`.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/` 下的落盘日志。

**本计划关闭的需求:** SURF-01 / SURF-02 / SURF-03 / DIV-01 / DIV-02 / DIV-03 / REG-01 / REG-02 / REG-03 —— 即 Phase 11 的全部 9 条 ID(本计划是收口计划,重新声明全阶段的需求归属;`REG-04` / `G1-01` / `VIS-01` 归 Phase 12,不得声明)。

**本计划不触碰:** `frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**`(逐字节);`scripts/check-05-ui-uat.py`(只读运行)、`scripts/check-02-contrast.py`、`scripts/check-10-idi10-validation.py`、`check-01…04` / `check-06` / `check-07` / `probe-*`(零改动);`REG-04` / `G1-01` / `VIS-01`(Phase 12);`WR-01` / `IN-01` / `IN-02` / `G2` / `999.2` / 暗色模式 / Nyquist 缺口 / 图标与空状态 / `.overlay-card` 底色(全部 Out of Scope)。

## ⚠ 范围裁定记录(用户 2026-09-28 两次 AskUserQuestion 逐项选定)

| 项 | 裁定 | 本计划的落地 |
|---|---|---|
| `CR-01` 窗口边缘发丝线 | 走**纯 CSS 下边线**(不改 `app.js`、不加类) | Task 1 第 856 行就地改写 + Task 2 的 c4 扩写与变异 |
| `WR-02` 围栏三处现在时陈述 | 改 | Task 1 的围栏改写 |
| `WR-03` c2 未断言 `#doc-panel` 底色 | 改 | Task 2 的 c2 断言 |
| `WR-01` check-05 的 `.hint` 断言 | **不改**(避免扩大连带指纹面) | **不碰 `check-05`**;只在 Task 3 只读运行它 |
| `IN-01` / `IN-02` | **不做**(Info 级) | 不建任务 |
| `G1-01` / `REG-04` / `VIS-01` | 归 **Phase 12** | 不碰 `#latest-check` / `th` 表头 band;不做 5 张截图;不做全里程碑复跑 |

**若在调查中撞上上述任何一项的真缺陷:记一行到 SUMMARY 的观察区即可,不要为它建任务。**

**执行前对照基线(取自 `idi-11-04` 落盘的 `gate-logs/`;执行器须复核):**

| 门 | `idi-11-04` 落盘的对照基线(本计划改动前) | 本计划预期 |
|---|---|---|
| `check-01`…`check-04` | 全 `PASS` / exit 0 | 全 `PASS` |
| `check-05` 全量 | `item 1: 45` / `2: 5` / `3: 17` / `4: 65` / **`5: BLOCKED (9, 2 BLOCKED)`** / `6: 6` / `7: 38` / **`8: PASS (13)`** / **`9: PASS (17)`** / `10: 42`;`exit=2` | 零新增 FAIL;item 5 仍 `2 BLOCKED`;item 8 / item 9 仍 `PASS`;几何类读数**允许**变化但须有机制解释 |
| `check-09` c1..c5 | `c1 59` / `c2 17` / `c3 6` / `c4 20` / `c5 5`;`exit=0` | `exit=0`;c2 与 c4 断言数**增长**;零删除 |
| `check-06` / `check-07` / `check-10` | `exit=0` | `exit=0`,零新增 FAIL |
| `probe-05` / `probe-07` | 各 `EXIT=0` | 各 `EXIT=0` |
| pytest | `219 passed, 6 skipped` | 不降(必须用项目 `.venv`) |

> ⚠ **`--item 9` 的滚动者普查期望值不得写成「4」。** 磁盘实测 `scripts/check-05-ui-uat.py:2436` 的 `PANEL_SCROLLERS = ("#chat-messages", "#latest-check", "#main-pane")` 是 **3** 个成员,`:2438` 的 `PANEL_SCROLLERS_EXEMPT` 是 **1** 个;item 9 的基线读数是 `PASS (17 条断言)`。CONTEXT D-11-9 与 ROADMAP 里「期望值是 4」的措辞在盘上不成立 —— 判据以**门自己的输出**为准。

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
@.planning/phases/idi-11-decard-and-hairline-dividers/11-CONTEXT.md
@.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-PATTERNS.md
@.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md
@.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-REVIEW.md
@.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-01-SUMMARY.md
@.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-03-SUMMARY.md
@.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/check-05-full.log
@frontend/style.css
@frontend/index.html
@scripts/check-09-idi09-validation.py
</context>

## Artifacts this phase produces

> 本节列出**本计划**新产生的符号,供 plan-review 的 source-grounding 通道排除「新建符号」误报。全阶段产出表在 `idi-11-01-PLAN.md` 的 §「Artifacts this phase produces」,不重复。

**新增目录:** `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/`

**新增日志文件(17 个):** `geometry-before.log` / `geometry-after.log`(Task 1)+ `check-01-token-conformance.log` / `check-02-contrast.log` / `check-03-hidden-uniqueness.log` / `check-04-important-count.log` / `check-05-full.log` / `check-05-item8.log` / `check-05-item9.log` / `check-06-idi05-validation.log` / `check-07-idi08-validation.log` / `check-09-idi09-validation.log` / `check-10-idi10-validation.log` / `node-check-app.log` / `probe-05-resolve-color.log` / `probe-07-focus-composite.log` / `pytest.log`(Task 3)。

**`scripts/check-09-idi09-validation.py` 新增/改写的符号:**

| # | 符号 | 锚点 | 动作 |
|---|---|---|---|
| 1 | `HAIRLINE_CENSUS_JS` | 新模块级常量(与 `_C5_SCROLL_JS` 并列) | **新增**。返回 4 个 section 的 `{sel, display, top, bottom, borderTop, borderBottom}` 的 JS 探针串 |
| 2 | `HAIRLINE_SECTIONS` | 现 `:109` | **改值**:由后三个(`#annotations-panel` / `#checks-panel` / `#ai-panel`)改为前三个(`#session-panel` / `#annotations-panel` / `#checks-panel`);注释同步改写 |
| 3 | `c1` 的边框宽度断言块 | 现 `:253-266` | **换向**:三个非末位 section 断 `border-top/right/left == 0px` + `border-bottom == 1px`;`#ai-panel`(DOM 末位)四条边全 `0px` |
| 4 | `c4` 的横线断言块 | 现 `:432-446` | **换向 + 扩写**:三宿主断 `border-bottom` 宽度与色(令牌 + gray-6 字面量)+ `border-top == 0px`;`#ai-panel` 断两条边全 `0px` |
| 5 | c4 的逐状态发丝线普查 | c4 内新增循环 | **新增**:对 `c05.STATES` 5 个状态各 3 条断言(见 Task 2) |
| 6 | c2 的 `#doc-panel` 底色断言 | 现 `:385-387` 旁 | **新增** 2 条:`#doc-panel` 计算底色 == `body_bg`;== `SURFACE_PAGE_LITERAL` |

**本计划不产生的新符号:** 零新增函数、零新增门、零新增探针、零新增依赖、零新增令牌、零新增颜色值。`frontend/app.js` 与 `frontend/index.html` 零改动(用户选择纯 CSS 路线正是为了保住这条)。

## 波次与依赖形状

| 波次 | 计划 | 为什么必须在这个位置 |
|---|---|---|
| 5 | `idi-11-05`(本计划) | 收口必须看到**全部**既有改动(波次 1/2 的 `style.css`、波次 3 的 `check-09` 改写、波次 4 的门禁收口与 `gate-logs/` 基线);且本计划的变异测试必须在**已提交**的树上做 |

<tasks>

<task type="auto" tdd="false">
  <name>Task 1: 发丝线规则就地改写为下边线 + 承重注释如实改写 + 围栏内三处现在时陈述改写(BINDING-1 第 1/2 条 + BINDING-2)</name>
  <files>frontend/style.css, .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/geometry-before.log, .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/geometry-after.log</files>
  <reversibility rating="reversible">回退是把第 856 行的选择器与声明、以及四处注释改回去;不牵连其它产物、不动任何值。</reversibility>
  <read_first>
    - `frontend/style.css` 的 **第 828-856 行全文** —— 逐字读那段承重注释的每一句,尤其是断言「相邻选择器按 **DOM 相邻**判定、不按渲染相邻,故中间两个面板带 .hidden 时 #ai-panel 仍带自己的上边线 —— 两种显隐状态下都恰好 1 条可见分界」那一句(**与实测矛盾,本任务要改写的核心**)与「特异性:本选择器(1-0-2)高于 #main-pane > section(1-0-1)」那一句(**:not(:last-child) 的参数贡献一个伪类,特异性变 1-1-2**)
    - `frontend/style.css` 的 **第 806-826 行全文** —— `#main-pane > section` 规则体上方的注释,其中「`border: none` 与紧随其后的相邻兄弟规则是一对:前者去掉四条边,后者只给后三个 section 补回一条上边线(第一个 section 的顶部是窗口边缘,画了会读成多一条)」那句描述的旧机制同样作废,须一并改写
    - `frontend/style.css` 的 **第 775-796 行全文**(`#main-pane` 规则体**自身**的注释块)—— 其中第 **781** 行那句把分区机制说成由「相邻兄弟规则」的一条「1px 上边线」承担,描述的是**旧机制**,改动后即与代码矛盾,**须一并就地改写**(第三处机制注释);同一注释块里 `align-items: center` 与 `#main-pane > section` 的 `max-width` 是「一对仍在工作」的声明那段、以及「卡片本身不得加 margin」那条纪律段与本次改动无关,**逐字保留**(D-11-5)
    - `frontend/style.css` 的 **第 136-142 行**(「exactly ONE consumer」那句)、**第 182-200 行**(「Measured 4.65 … thinnest margin (0.15)」那句与紧随其后的 Phase 11 update 段)、**第 89-96 行**(「gray-9 = 3.24 / 3.15」那句)—— 本任务要改写的三处现在时陈述
    - `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md` 的 `gaps:` 段与 §「Gaps Summary」—— **缺陷的原始判据与实测读数**(p3 / checking / archive 三态的可视首个面板 `border-top=1px` 且 `top=0.00`;像素级 y=0 = `rgb(217,217,217)`)
    - `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-REVIEW.md` 的 §`CR-01` 与 §`WR-02` —— 缺陷原文与三处陈旧陈述的逐条事实对照(四个消费者行号、4.77 / 0.27、3.32)
    - `frontend/index.html` 的 `#main-pane` 段(**第 12-79 行**)—— 逐字确认 4 个 section 的 DOM 顺序与 `#ai-panel` 是 `</main>` 前的**末子元素**
    - `frontend/app.js` 的 `#ai-panel` 与 `.hidden` toggle 处 —— 逐字确认全文只有 `#ai-panel-header` / `#ai-panel-body` 两个元素引用,**从不**对 `#ai-panel` 做 `classList` 切换
    - `.planning/phases/idi-11-decard-and-hairline-dividers/11-CONTEXT.md` §D-11-5 / §D-11-8 / §D-11-10 —— 保留 `max-width: 768px` 与 `align-items: center` 的裁定、线取 gray-6 的裁定、以及「第一个面板顶部不画(顶部是窗口边缘)」的裁定原文
    - `scripts/check-05-ui-uat.py` 的 `make_fixture()` / `enter_project()` / `STATES` / `ensure_server()` —— 几何探针要复用它们
  </read_first>
  <action>
    **第 1 步 —— 先取「改动前」的几何读数(必须在本任务编辑任何文件之前做)。**

    写一个一次性 Playwright 探针脚本到系统临时目录(`mktemp -d`,跑完删除,**不落进仓库树**):按 `scripts/check-09-idi09-validation.py` 的 `load_check05()` 手法用 `importlib.util.spec_from_file_location` 把 `scripts/check-05-ui-uat.py` 当模块加载,调用 `c05.ensure_server()` 起(或复用)服务,`sync_playwright().start()` 后 **`pw.chromium.launch(headless=True)`(Playwright 自带 chromium;本机 `channel="chrome"` + headless 会挂死)**,`browser.new_context(viewport={"width": 1440, "height": 900})`。对 `c05.STATES` 的 5 个状态各 `c05.make_fixture(state, tmp_root)` + `c05.enter_project(page, proj)`,然后用一次 `page.evaluate` 取 `["#session-panel", "#annotations-panel", "#checks-panel", "#ai-panel"]` 四个元素的 `getComputedStyle(el).display`、`el.getBoundingClientRect().top` / `.bottom`、`getComputedStyle(el).borderTopWidth` / `.borderBottomWidth`。逐状态逐元素打印。

    把完整输出存到 `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/geometry-before.log`。**这一步不是可选的** —— 它是「1px 位移真的发生了」的对照侧,不得用验证报告里的数字代替。

    **第 2 步 —— 就地改写第 856 行的规则。**

    把该行的选择器由改动前的**相邻兄弟**形态改为 `#main-pane > section:not(:last-child)`,并把声明的属性由 `border-top` 改为 `border-bottom`;**线色与线宽逐字不变**,仍是 `1px solid var(--color-border-subtle)`。

    - **就地改写,不追加覆盖、不搬迁**(「追加,不重排」纪律:至少一对等特异性规则由源码顺序决定)。
    - **不得**动 `#main-pane > section` 规则体(`:819-826`)的任何一行。
    - **不得**用 `section.hidden` 之类的写法 —— 那条路线已被验证者显式否决(它会同时抹掉 p3 下 `#checks-panel → #ai-panel` 的分隔线)。
    - **不得**动 `frontend/app.js`(用户选择纯 CSS 路线正是为了保住这条;需要动它即说明选错了实现方式)。

    **第 3 步 —— 如实改写承重注释(第 828-855 行),并显式登记机制前提。**

    注释里「相邻选择器按 **DOM 相邻**判定、不按渲染相邻,故中间两个面板带 .hidden 时 #ai-panel 仍带自己的上边线 —— 两种显隐状态下都恰好 1 条可见分界」这一整句**与实测矛盾**,必须改写为新机制:

    - 新机制键控于「**非 DOM 末子元素**」而不是「非 DOM 首子元素」;`#main-pane` 的 DOM 末子元素是 `#ai-panel`,故是**前三个** section 各带一条**下边线**。
    - **显式登记前提(承重,不得省略):** `#ai-panel` 是 `#main-pane` 的 DOM 末子元素,**且 `frontend/app.js` 从不给它加 `.hidden`**(全文只有 `#ai-panel-header` / `#ai-panel-body` 两个元素引用)。**正因为这条前提,「除 DOM 末个外都加下边线」才等价于「除最后一个可见 section 外都加下边线」**;前提一旦被破坏(例如日后给 `#ai-panel` 加了隐藏切换,或在其后插入新的 section),规则即失效 —— 最后一个可见面板会多画一条下边线。把这句写进注释。
    - 说明契约本身:可见的发丝线数 == 可见面板数 − 1;可视的第一个面板顶部**永不**带线(它至多带下边线),故**永不**在窗口边缘(`#main-pane` 的 `top == 0`)画线。
    - **特异性那一句必须同步更正:** 本选择器现在是 **1-1-2**(`:not(:last-child)` 的参数是一个伪类,贡献 0-1-0),仍高于 `#main-pane > section` 的 1-0-1,故与源码先后无关。
    - **保留**「档位取 gray-6」段、「线宽等于内容列宽」段、以及整段**不登记 NON-TEXT 对比度对**的论证(`D-11-8` / `D-11-14`:分隔线不标识任何控件 / 状态 ⇒ SC 1.4.11 不适用;反证 gray-6 在白面仅 1.412)—— 这些与本次改动无关,逐字保留。
    - **不得**把改动前的相邻兄弟选择器写成字面量留在注释里(围栏外的机械判据是子串计数,连论证性散文都会把它顶高)。

    同时改写 `#main-pane > section` 注释里那句「`border: none` 与紧随其后的相邻兄弟规则是一对:前者去掉四条边,后者只给后三个 section 补回一条上边线(第一个 section 的顶部是窗口边缘,画了会读成多一条)」—— 它描述的是旧机制,须改为新机制(去掉四条边 + 给前三个 section 补一条**下边线**;可视的第一个面板顶部永不带线)。

    并改写 `#main-pane` 规则体**自身**注释块里第 **781** 行那句(现文把分区机制说成由「相邻兄弟规则」的一条「1px 上边线」承担)—— 它同样描述**旧机制**,改动后即与代码矛盾,须按同一口径就地改写为新机制(分区改由**非 DOM 末位面板的下边线**承担)。**保留**同一注释块里仍然成立的两段:①「`align-items: center` 与 #main-pane > section 的 max-width 是一对仍在工作的声明」那段;②「卡片本身不得加 margin」那条纪律段 —— 两者与本次改动无关,逐字保留(D-11-5)。

    **第 4 步 —— 改写围栏内三处现在时陈述(BINDING-2)。只改现在时,不删历史段落。**

    1. **第 136-142 行**:那句现在时陈述断言 `--color-surface-page` **只有一个消费者**(`html, body` 的 background),并由此推出「改这个值只需重绘页面、别处无需同步」。**该断言已被本阶段推翻** —— 它现在有**四个**消费者(`html, body` 的 background、`#main-pane > section`、`#doc-panel`、`#doc-panel-header`)。改写为四个消费者的事实,并写明改这个值会**同时**重绘页面、四个左栏面板与 sticky 表头。**旧句里「别处无需同步」那半句是更危险的一半**(它会让读者以为改这个值只动页面),必须被替换掉。
    2. **第 182-200 行**:那句现在时测量写的是该令牌在**旧地面**上的旧读数与「本阶段最薄的余量」旧值。统一白面之后实测为 **4.77**、余量 **0.27**;把这句现在时测量改写为白面上的事实。**只改这句**;紧随其后的 Phase 11 update 段(它已写「measured 4.77 there」与 Phase 9 的 4.18 历史)逐字保留 —— 改完后两者必须互相一致。
    3. **第 89-96 行**:那句现在时测量写 gray-9 的两个读数(一个白面、一个内陷面)。**白面**那一个在统一白面上实测为 **3.32**;另一个(on `--color-surface`)仍正确,**不动**。只改写白面那一个。

    **硬性约束(围栏内):**
    - **不得**出现「令牌名 + 冒号」的写法(`check-02-contrast.py` 的 `DECL_RE = re.compile(r"(--[a-z0-9-]+)\s*:\s*([^;]+);")` 扫**围栏全文含注释**,`parse_decls` 让最后一个匹配胜出 —— 一句 `` `--color-surface-page`: … `` 会被解析成声明并让 `resolve()` 退出 1)。
    - **不得**点名两个已删卡片令牌(`--color-surface-card` / `--shadow-card`):围栏子串计数须仍为 0。
    - **不得**改任何**值**、不得新增令牌、不得动 `check-02` 的阈值或 PAIR 清单。

    **第 5 步 —— 顺带核正同类陈旧表述(零额外文件面,范围严格有界)。**

    ① **消费者清单:** `grep -n 'exactly ONE\|ONE consumer\|consumers' frontend/style.css` 一次,逐行核对**是否还有**关于 `--color-surface-page` **消费者清单**的现在时陈述被推翻。若还有,按同一口径核正;把扫描结果(命中行号 + 判定)写进 SUMMARY。

    ② **发丝线机制短语:** `grep -n '相邻兄弟规则\|上边线' frontend/style.css` 一次,逐行核对每一处是否仍在描述**旧机制**。HEAD 实测命中 **4 行**:`781`(`#main-pane` 自身注释)、`814-815`(`#main-pane > section` 注释)、`835`(第 828-855 行承重注释)—— **三处全部落在本任务的改写范围内**,改写后这三处对旧机制的描述必须全部消失;若扫描发现另有命中,按同一口径核正。把扫描结果(命中行号 + 判定)写进 SUMMARY。

    ⚠ **明确不在本步范围的一项(记为观察,不要改):** 第 727-729 行那句「`#doc-panel` declares background: var(--color-surface).」在本阶段之后同样不成立,但它**不是** `--color-surface-page` 的消费者陈述,而且改它必须连带把紧随的两条 `PAIR … ON --color-surface` 重新归属 —— **那正是 BINDING-2 明令不得动的 PAIR 清单**(且 `idi-11-PATTERNS.md` 已把它登记为「范围决定,交 planner 裁定,不得单方面扩张」)。**只在 SUMMARY 的观察区记一行,不建任务、不修改。**

    **第 6 步 —— 取「改动后」的几何读数并与改动前并排登记。**

    重跑第 1 步的同一个探针,输出存到 `…/gate-logs/idi-11-05/geometry-after.log`。在 SUMMARY 里给出**并排两列**并写明机制:

    - 预期 `p1` 的 `#ai-panel` `rect.top` 由 `767.00` 变 `768.00`(`#session-panel` 现在带一条 1px 下边线 ⇒ 它自己的盒高 +1px,`#ai-panel` 被下推 1px);总高不变。
    - 预期 `p1` 的 `#session-panel` `borderTopWidth` 由 `0px` 保持 `0px`、`borderBottomWidth` 由 `0px` 变 `1px`;`#ai-panel` 的 `borderTopWidth` 由 `1px` 变 `0px`。
    - 预期 p3 / checking / archive 下可视的第一个面板(`#annotations-panel` / `#checks-panel`)的 `borderTopWidth` 由 `1px` 变 `0px`(**这正是本 gap 的修复读数**)。
    - 若实测与预期不符,**不要改读数去凑** —— 把实测原文与机制写进 SUMMARY 报回。

    **第 7 步 —— 确认四条静态门未受影响。**

    `bash scripts/check-01-token-conformance.sh` / `.venv/bin/python scripts/check-02-contrast.py` / `bash scripts/check-03-hidden-uniqueness.sh` / `bash scripts/check-04-important-count.sh` 逐条跑一次,须全 `PASS`(本任务不动任何令牌声明与颜色值,围栏内只改注释散文;`check-04` 数的是 `!important;` **声明**数,恒为 1)。

    **第 8 步 —— 确认改动面。** `git diff --name-only` 只应列出 `frontend/style.css`(以及新增的 `gate-logs/idi-11-05/` 下两个日志文件)。`frontend/app.js` / `frontend/index.html` / `backend/**` / `scripts/**` 逐字节未改。

    > ⚠ **中间态说明(预期,不是缺陷):** 本任务提交后、Task 2 完成前,`check-09` 的 c1 / c4 会**变红** —— 它们仍在断言旧机制(后三个面板的上边线)。这与波次 1(plan 01 改 `style.css`)→ 波次 3(plan 03 改写 `check-09`)之间的中间态同型,是既有的、已登记过的形态。**不得**为了让 c1 / c4 此刻变绿而回退第 2 步的规则。
  </action>
  <verify>
    <automated>grep -nE '#main-pane > section:not\(:last-child\)' frontend/style.css</automated>
    <fails_when>no line is found, or the matched line does not also contain the declaration `border-bottom: 1px solid var(--color-border-subtle);`</fails_when>
    <automated>grep -cE 'section \+ section' frontend/style.css</automated>
    <fails_when>the count is not exactly 0 (the adjacent-sibling form must be gone from both the rule and the surrounding prose)</fails_when>
    <automated>grep -cE '^#main-pane > section \{' frontend/style.css</automated>
    <fails_when>the count is not exactly 1 (the base rule must survive untouched, so the hairline rule's specificity still needs to beat it)</fails_when>
    <automated>grep -cE '1-1-2' frontend/style.css</automated>
    <fails_when>the count is 0 (the specificity note in the rewritten comment must state the new 1-1-2, not the stale 1-0-2)</fails_when>
    <automated>grep -cE '分区改由相邻兄弟规则' frontend/style.css</automated>
    <fails_when>the count is not exactly 0 (the `#main-pane` rule's own comment at :781 still carries the OLD mechanism sentence — adjacent-sibling rule plus a top border — which contradicts the code after this change; it must be rewritten in place). HEAD reading: 1 (line 781) — red before the rewrite, 0 after</fails_when>
    <automated>grep -cE 'exactly ONE consumer' frontend/style.css</automated>
    <fails_when>the count is not exactly 0 (the one-consumer claim is the stale sentence BINDING-2 requires corrected)</fails_when>
    <automated>grep -cE 'Measured 4\.65|thinnest margin \(0\.15\)' frontend/style.css</automated>
    <fails_when>the count is not exactly 0 (the present-tense sentence being rewritten — its 4.65 reading and its 0.15 margin are both stale on the unified white surface). The scan is deliberately ANCHORED to that sentence: 4.65 also occurs on line 100 (green-1's contrast — a different fact) and on the 540-559 ledger rows, all of which BINDING-2 orders preserved verbatim, so a whole-file count of 4.65 can never reach 0 on a correct tree. HEAD reading of this anchored form: 2 (line 185 + line 187) — red before the rewrite, 0 after</fails_when>
    <automated>grep -cE '3\.24 / 3\.15' frontend/style.css</automated>
    <fails_when>the count is not exactly 0 (the pattern is the stale reading PAIR in the gray-9 white-ground present-tense sentence — `3.24 / 3.15`; the white-ground half must become `3.32 / 3.15`). Anchored to that pair because the 542 / 550 / 559 ledger rows keep 3.24 verbatim by BINDING-2, so a whole-file 3.24 count can never reach 0 on a correct tree. HEAD reading: 1 (line 93) — red before the rewrite, 0 after</fails_when>
    <automated>grep -c '^--color-surface-card\|--shadow-card' frontend/style.css; grep -o '/\* PAIR' frontend/style.css | wc -l; grep -o '/\* ORDER' frontend/style.css | wc -l</automated>
    <fails_when>the first count is non-zero, or the PAIR count is not 53, or the ORDER count is not 1 (the fence rewrite must not reintroduce a deleted token name or disturb the manifest)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh && .venv/bin/python scripts/check-02-contrast.py</automated>
    <fails_when>any of the four commands exits non-zero or prints a FAIL (the fence prose rewrite must not break the static gates)</fails_when>
    <automated>ls -1 .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/</automated>
    <fails_when>the listing does not contain both geometry-before.log and geometry-after.log</fails_when>
    <automated>git --no-pager diff --name-only HEAD</automated>
    <fails_when>the output lists any path other than frontend/style.css (frontend/app.js, frontend/index.html and everything under scripts/ and backend/ must be byte-identical; the two new geometry logs are untracked and therefore do not appear here)</fails_when>
  </verify>
  <acceptance_criteria>
    - `frontend/style.css` 含 `#main-pane > section:not(:last-child)`,且同一行含 `border-bottom: 1px solid var(--color-border-subtle);`;`grep -cE 'section \+ section' frontend/style.css` == **0**。
    - `#main-pane > section` 规则体(四条声明 `width` / `max-width` / `background` / `border` / `border-radius` / `box-shadow`)逐字未改;规则行**位置未移动**(就地改写)。
    - 第 828-855 行的注释已改写为新机制(键控于「非 DOM 末子元素」),并**显式登记前提**:`#ai-panel` 是 `#main-pane` 的 DOM 末子元素且 `frontend/app.js` 从不给它加 `.hidden`;注释里不再出现「两种显隐状态下都恰好 1 条可见分界」这句与实测矛盾的断言;特异性数字已更正为 **1-1-2**。
    - `#main-pane > section` 注释里描述旧机制的那句(「只给后三个 section 补回一条上边线」)已改写。
    - 围栏内三处现在时陈述已改写:`exactly ONE consumer` 出现 0 次;`Measured 4.65` / `thinnest margin (0.15)` 出现 0 次;gray-9 白面读数那句里的 `3.24 / 3.15` 这一对出现 0 次(改为 `3.32 / 3.15`);消费者清单已写明四个。历史段落(Phase 9 / Phase 11 的账目段)逐字保留 —— 三条判据均**按句锚定**,**不**要求清空围栏内 `4.65` / `3.24` 的全部出现:第 100 行 green-1 的 `4.65` 与第 540-559 行账目段里的 `4.65` / `3.24` 是**不同事实 / 历史**,BINDING-2 明令逐字保留,整文件计数永远到不了 0。
    - 描述发丝线机制的注释**三处全部**与代码一致:`#main-pane` 规则体自身注释第 **781** 行那句旧机制描述(把分区机制说成由相邻兄弟规则的一条 1px 上边线承担)已就地改写为下边线机制,该句的旧短语出现 0 次;同一注释里 `align-items: center` / `max-width` 那段与「卡片不得加 margin」那条纪律段逐字保留(D-11-5)。
    - 围栏内零「令牌名 + 冒号」写法;`--color-surface-card` / `--shadow-card` 在围栏内出现 0 次;`/* PAIR` 计数仍 53、`/* ORDER` 计数仍 1;零值改动、零新增令牌。
    - 四条静态门(check-01…check-04)全 `PASS`。
    - `geometry-before.log` 与 `geometry-after.log` 均已落盘,SUMMARY 里给出并排两列 + 机制说明(`#ai-panel` `rect.top` 767→768;p3 / checking / archive 可视首个面板 `borderTopWidth` 1px→0px)。
    - `git diff --name-only` 只列出 `frontend/style.css` 与两个几何日志;`frontend/app.js` / `frontend/index.html` / `backend/**` / `scripts/**` 逐字节未改。
    - SUMMARY 里记录了「顺带核正」那一步的扫描结果,以及第 727-729 行那项**只观察、不修改**的判定与理由。
  </acceptance_criteria>
  <done>第 856 行的发丝线规则已就地改写为「非 DOM 末子元素加下边线」(线色线宽不变、位置未移);承重注释已如实改写并显式登记「`#ai-panel` 是 DOM 末子元素且从不被 `.hidden` 隐藏」这条前提,与实测矛盾的旧断言已消失;围栏内三处现在时陈述已改写为 Phase 11 之后的事实且历史段落保留;四条静态门仍全 PASS;改动前后的几何读数已并排落盘登记;`app.js` / `index.html` / 后端逐字节未改。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 2: check-09 的 c1/c4 换向 + c4 逐状态发丝线普查 + c2 补 #doc-panel 底色断言,并以三条变异证明会失败(BINDING-1 第 3/4 条 + BINDING-3)</name>
  <files>scripts/check-09-idi09-validation.py</files>
  <reversibility rating="reversible">回退是把 c1/c4 的边框断言换回 `border-top`、删掉 c4 的普查循环与 c2 的两条新断言;不牵连产品代码。</reversibility>
  <read_first>
    - `scripts/check-09-idi09-validation.py` 的 **c1 全文(第 190-304 行)** —— 逐字读 `:253-266` 那段「边界宽度是**异形**的,不是一条统一循环」的注释与它的 `if sel == "#session-panel"` 分支(**本任务要换向的对象**),以及 `:248-252` 的两条底色断言(它们不动)
    - `scripts/check-09-idi09-validation.py` 的 **c2 全文(第 313-387 行)** —— 逐字读 `:322` 的 `bg = read_style(page, "#doc-panel", "background-color")`(**读进来却从无断言消费它**)、`:376` 的 `body_bg`、`:385-387` 的 `#doc-panel-header` 底色断言(**新断言要放在它旁边**)
    - `scripts/check-09-idi09-validation.py` 的 **c4 全文(第 404-490 行)** —— 逐字读 `:432-446` 的横线断言块(宿主是 `HAIRLINE_SECTIONS`,断的是 `border-top-width`)、`:448-472` 的 `#doc-panel` rect 几何断言(**保留不动**)、`:474-490` 的三条对照组(**保留不动**)
    - `scripts/check-09-idi09-validation.py` 的 `:104-156` —— `LEFT_SECTIONS` / `HAIRLINE_SECTIONS` / `RADIUS_CORNER_PROPS` / `BORDER_SIDES` / 三档字面量 / `RETIRED_CARD_TOKENS` / `CONTROL_GROUP` 的现有定义与注释
    - `scripts/check-09-idi09-validation.py` 的 `:574-679`(c5 的 `_C5_SCROLL_JS` 与它的用法)—— 新增的 JS 探针常量要沿用同一写法(`page.evaluate` 传一个字符串常量)
    - `scripts/check-09-idi09-validation.py` 的 `:707`(`ITEMS`)与 `:720-778`(`main()` 的逐项结论与退出码)—— 判据:任何 FAIL → exit 1;任何 BLOCKED → exit 2
    - `scripts/check-05-ui-uat.py` 的 `ok()` / `ok_true()` / `read_style()` / `make_fixture()` / `enter_project()` / `STATES` —— 逐字读 `ok()` 在 **expected 为 None** 时记 BLOCKED 的那一支(本项目把 exit 2 当良性码,故令牌类断言一律走 `ok_true`)
    - `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-03-SUMMARY.md` 的 §「六条变异测试 —— 逐条「变异 → FAIL」真实读数」—— **变异测试的取证格式与还原判据的现成先例**(每条给出 FAIL 原文 + 退出码 + `git diff --exit-code` rc + `git hash-object`;**全程未使用 `git stash`**)
    - `.planning/phases/idi-11-decard-and-hairline-dividers/11-CONTEXT.md` §D-11-12(判据走真实浏览器 computed style 读数、令牌解析降为 `info()`)、§D-11-13(变异纪律)、§D-11-14(发丝线不登记 NON-TEXT 对)
    - `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md` 的 `gaps:` 第 2 条 —— 「c4 的判据只在 p1 fixture 上运行;c4 在 p3 / checking / archive 从不运行 ⇒ 对本缺陷结构性失明」的原始判据
    - `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-REVIEW.md` 的 §`WR-03` —— c2 未消费 `bg` 的原始判据与建议断言文本
  </read_first>
  <action>
    **第 1 步 —— c1 的边框宽度断言换向(第 253-266 行)。**

    规则已由「后三个面板的上边线」变成「前三个面板的下边线」,故旧判据必红。换向为:

    - `#session-panel` / `#annotations-panel` / `#checks-panel`(三个**非 DOM 末位** section):断 `border-top-width == 0px`、`border-right-width == 0px`、`border-left-width == 0px`、`border-bottom-width == 1px`。
    - `#ai-panel`(**DOM 末位**):四条边全 `== 0px`。
    - 断言数**不变**(每 section 4 条 × 4 = 16):**零条删除、零条降级**。
    - 把那段「边界宽度是**异形**的」注释改写为新形状的理由:线现在记在非末位 section 的**下边线**上;`#ai-panel` 是 DOM 末子元素故四条边全零 —— 并写明这依赖「`#ai-panel` 恒可见」这条前提(与 Task 1 的注释同一口径)。
    - `:248-252` 的两条底色断言与 `:243-247` 的阴影 / 圆角断言**逐字不动**。

    **第 2 步 —— c4 的横线断言块换向(第 432-446 行)。**

    - 把 `HAIRLINE_SECTIONS`(第 109 行)的值由后三个改为**前三个**:`#session-panel` / `#annotations-panel` / `#checks-panel`;第 107-108 行的注释同步改写(旧注释说「只有后三个」与「`#session-panel` 是 DOM 第一个 section」—— 两者都作废)。
    - 对每个宿主断:`border-bottom-width == 1px`、`border-bottom-color == var(--color-border-subtle)`(令牌侧)、`border-bottom-color == gray-6 字面量`(`HAIRLINE_LITERAL`),外加 `border-top-width == 0px`。**字面量那半条是承重的**(`D-11-8` 显式否决的 gray-7 备选必须对本门可见)—— 逐字保留它的 note。
    - 另加 `#ai-panel`(DOM 末位)两条:`border-top-width == 0px` 且 `border-bottom-width == 0px`。
    - `:448-472` 的 `#doc-panel` rect 几何断言与 `:474-490` 的三条对照组**逐字不动**。

    **第 3 步 —— c4 新增逐状态发丝线普查(本计划的核心新增)。**

    在 c4 内新增一个模块级 JS 探针常量 `HAIRLINE_CENSUS_JS`(与 `_C5_SCROLL_JS` 并列,同一写法):对 `["#session-panel", "#annotations-panel", "#checks-panel", "#ai-panel"]` 逐个返回 `{sel, display, top, bottom, borderTop, borderBottom}`(display 取 `getComputedStyle(el).display`;top / bottom 取 `el.getBoundingClientRect()`;两个 border 宽度取 `getComputedStyle(el).borderTopWidth` / `.borderBottomWidth`)。

    然后对 `c05.STATES` 的**全部 5 个状态**各做一次 `c05.make_fixture(state, tmp_root)` + `c05.enter_project(page, proj)` + `page.evaluate(HAIRLINE_CENSUS_JS)`,逐状态断三条:

    - **(i) 可视的第一个面板顶部无发丝线。** `visible` = 按 DOM 顺序过滤出 `display != "none"` 的元素;断 `visible[0]` 的 `borderTop == "0px"`。note 写明:**这是本 gap 的回归判据** —— 旧 c4 只在 p1 上跑,而 p1 下 `#session-panel` 恰是可视的第一个面板,该断言在唯一不可能出缺陷的状态里恒真;本项在 `#session-panel` 被隐藏的 p3 / checking / archive 上也运行。
    - **(ii) 可见发丝线数 == 可见面板数 − 1。** 可见发丝线 = `visible` 中 `borderTop != "0px"` 或 `borderBottom != "0px"` 的元素;断其计数 == `len(visible) - 1`(5 个样本里恒 1)。note 写明契约本身是「每对相邻可见面板之间恰 1 条、窗口边缘 0 条」,不是「恒 1 条」。
    - **(iii) 没有发丝线落在窗口边缘。** 断不存在「`borderTop != "0px"` 且 `top <= 0.5`」的可见元素(`0.5px` 是浮点读数容差)。note 写明:**「可视的第一个面板 `rect.top > 0`」这条措辞是按「线」的位置写的** —— 可视的第一个面板**自身**的 `rect.top` 在 5 个状态里**恒为 0**(它就在窗口顶;这是合法的,因为它只带下边线),故判据落在「线不落在 y == 0」上,而不是「面板不在 y == 0」。把这条实测依据写进 note(不得写成「面板 `rect.top > 0`」那样不可满足的形式)。
    - 若某状态的探针返回非 list 或元素缺失:记 `blocked(...)`,**不得**记 PASS。
    - **不得**把本项降级为「只断言规则被写下了」(例如只 grep 选择器文本)。

    **第 4 步 —— c2 补 `#doc-panel` 自身底色的断言(BINDING-3)。**

    在第 385-387 行那条 `#doc-panel-header` 底色断言**旁边**补两条(复用第 376 行已算好的 `body_bg` 与第 322 行已读到的 `bg`):

    - `#doc-panel` 计算底色 == body 计算底色(统一面)—— note 写明:「五个容器统一面的一部分;c2 原先只把 `#doc-panel` 的底色**读进 `bg`** 却从无断言消费它 ⇒ 面板被重新上色时本门看不见(表头自绘背景,c2 的 header 断言仍会过;`check-05` 也不断言 `#doc-panel` 的底色)」。
    - `#doc-panel` 计算底色 == `SURFACE_PAGE_LITERAL`(写死字面量)—— 与 c1 同一理由(只跟 body 比会跟着令牌一起变;这一条把统一面钉死在白)。

    两条都走 `ok(...)`(两侧都是已解析的字符串,不是令牌解析值,故不触发 `ok()` 的 None-期望侧降级)。

    **第 5 步 —— 先确认真实树全绿。**

    `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4,c5` → `exit=0`,逐项 `0 FAIL`、`0 BLOCKED`。把 `=== 逐项结论 ===` 的 5 行原文抄进 SUMMARY,并与 HEAD 基线(59 / 17 / 6 / 20 / 5)逐项对照:c2 与 c4 的计数**增长**,c1 不变,c3 / c5 不变,**零项下降**。

    **第 6 步 —— 三条变异测试,逐条给出真实「变异 → FAIL」读数。**

    全部在**已提交的树**上做(Task 1 已提交)。**禁用 `git stash`**(它跨工作树共享,本项目明令禁止)。每次变异前记录 `git hash-object frontend/style.css`。

    - **M1(本 gap 的回归形态,必须有一条直接覆盖它):** 把第 856 行的选择器由 `:not(:last-child)` 还原成改动前的相邻兄弟组合子,并把声明的属性由 `border-bottom` 改回 `border-top`(即逐字复现改动前的规则)。预期:扩写后的 **c4 FAIL**,且触发的正是第 3 步的 (i) 与 (iii)(p3 下可视的第一个面板带顶线且 `top == 0`),很可能连带 (ii)(可见发丝线数变 2)。
    - **M2:** 给 `#main-pane > section:not(:last-child)` 的规则体补一条 `border-top: 1px solid var(--color-border-subtle);`。预期:扩写后的 **c4 FAIL**(p1 下可视的第一个面板 `#session-panel` 带顶线且 `top == 0`)。
    - **M3:** 把 `#doc-panel` 的 `background: var(--color-surface-page);` 改成另一档(例如 `var(--color-surface)`)。预期:**c2 FAIL**,触发的正是第 4 步新增的 `#doc-panel` 底色断言。

    每条须在 SUMMARY 里给出:**注入的最小改动描述 → `check-09 --item <项>` 的 FAIL 原文(含 expected= / actual=)→ 退出码**。**不得只声明做过。**

    还原:每条之后 `git checkout -- frontend/style.css`;然后以**两道独立证据**收口:`git diff --exit-code -- frontend/style.css` **rc=0** **且** `git hash-object frontend/style.css` 与变异前记录值**逐字符相同**。三条全部还原后 `git status --porcelain frontend/` 必须为空。

    **第 7 步 —— 复跑确认还原后的真实树仍全绿。** 再跑一次 `--item c1,c2,c3,c4,c5`,读数须与第 5 步逐项一致。

    **第 8 步 —— 确认改动面只有 `check-09`。** `git diff --name-only` 只应列出 `scripts/check-09-idi09-validation.py`。`frontend/style.css` 必须与 Task 1 提交时逐字节相同(变异已全部还原)。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4,c5</automated>
    <fails_when>the exit code is not 0, or any item line in "=== 逐项结论 ===" reports a non-zero FAIL or BLOCKED count</fails_when>
    <automated>grep -cE 'border-bottom-width' scripts/check-09-idi09-validation.py; grep -cE 'HAIRLINE_CENSUS_JS' scripts/check-09-idi09-validation.py</automated>
    <fails_when>either count is 0 (the reoriented border-side expectation must be expressed as reads of border-bottom-width — c1's three non-last sections and c4's three hosts; and the new census probe constant must be present). HEAD readings: border-bottom-width = 0, HAIRLINE_CENSUS_JS = 0 — both red before the edit. NOTE: the CSS rule selector literal is deliberately NOT grepped here — check-09 asserts computed styles, not source text, so a correct implementation has no reason to embed that selector</fails_when>
    <automated>grep -nE 'c05\.STATES' scripts/check-09-idi09-validation.py</automated>
    <fails_when>no match appears inside c4 (the census must iterate all five sample states, not just p1)</fails_when>
    <automated>grep -cE '#doc-panel 计算底色 == body 计算底色' scripts/check-09-idi09-validation.py</automated>
    <fails_when>the count is not exactly 1 (the BINDING-3 assertion must exist exactly once, next to the other c2 assertions)</fails_when>
    <automated>git --no-pager diff --name-only HEAD</automated>
    <fails_when>the output lists any path other than scripts/check-09-idi09-validation.py (all three mutations must have been restored; frontend/style.css must be byte-identical to its Task-1 commit)</fails_when>
    <automated>git --no-pager diff --stat HEAD -- frontend/app.js frontend/index.html scripts/check-05-ui-uat.py scripts/check-02-contrast.py scripts/check-10-idi10-validation.py backend/</automated>
    <fails_when>the output is not empty (this task changes only scripts/check-09-idi09-validation.py)</fails_when>
    <automated>git status --porcelain frontend/</automated>
    <fails_when>the output is not empty (every mutation must be fully restored on the committed tree)</fails_when>
  </verify>
  <acceptance_criteria>
    - `check-09 --item c1,c2,c3,c4,c5` → `exit=0`,逐项 `0 FAIL`、`0 BLOCKED`;c1 断言数 == 59(不变),c2 与 c4 断言数**严格大于** HEAD 基线(17 / 20),c3 / c5 不变(6 / 5);**零项下降、零条删除**。
    - c1 的边框宽度断言已换向:三个非末位 section 断 `border-top/right/left == 0px` + `border-bottom == 1px`;`#ai-panel` 四条边全 `0px`。
    - `HAIRLINE_SECTIONS` 的值是前三个 section;c4 对它们断 `border-bottom` 的宽度与色(令牌 + `HAIRLINE_LITERAL` 双断言)并断 `border-top-width == 0px`;`#ai-panel` 断两条边全 `0px`。
    - c4 含 `HAIRLINE_CENSUS_JS` 常量与一个遍历 `c05.STATES` 的循环,逐状态断三条:(i) 可视的第一个面板 `borderTop == "0px"`;(ii) 可见发丝线数 == 可见面板数 − 1;(iii) 无线落在窗口边缘。探针不可读时记 `blocked`。
    - c2 含且仅含一条 `#doc-panel 计算底色 == body 计算底色` 断言(外加字面量那一半)。
    - **三条变异的真实读数入册**:M1 → c4 FAIL、M2 → c4 FAIL、M3 → c2 FAIL;每条给出 FAIL 原文与退出码;三次还原后 `git diff --exit-code -- frontend/style.css` rc=0 且 `git hash-object` 逐字节相同;**全程未使用 `git stash`**。
    - `git --no-pager diff --name-only` 只有 `scripts/check-09-idi09-validation.py`;`git status --porcelain frontend/` 为空;`check-05` / `check-02` / `check-10` / `app.js` / `index.html` / `backend/` 零 diff。
  </acceptance_criteria>
  <done>c1 与 c4 的边框断言已随规则换向(零删除);c4 新增了覆盖全部 5 个样本状态的逐状态发丝线普查,且该普查在缺陷状态(p3 / checking / archive)上真的运行;c2 补上了 `#doc-panel` 自身底色的断言;三条变异各给出真实的「变异 → FAIL」读数并逐字节还原(未用 `git stash`);真实树上 `check-09` 全绿且断言数只增不减。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 3: 全门复跑与原始日志落盘 + 1px 敏感门的读数登记与分诊(BINDING-1 第 5/6 条)</name>
  <files>.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/</files>
  <reversibility rating="reversible">本任务只跑命令、写日志与登记,不产生产品代码改动。</reversibility>
  <read_first>
    - `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/` 的**文件清单与命名**(13 个文件,`idi-11-04` 落盘)—— 本任务的落盘格式模板与**逐项对照基线**
    - `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/check-05-full.log` 的 `=== 逐项结论 ===` 块(逐字读 item 1…item 10 的断言数与 verdict)—— 本任务改动后的并排对照基线
    - `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/check-09-idi09-validation.log` —— `check-09` 的对照基线(c1..c5 的断言数)
    - `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/geometry-before.log` 与 `geometry-after.log`(Task 1 落盘)—— 1px 位移的实测依据
    - `.planning/ROADMAP.md` §`### Phase 11:` 的 Gates 行(「五条浏览器门复跑无新增失败」)
    - `.planning/phases/idi-11-decard-and-hairline-dividers/11-CONTEXT.md` §D-11-16(**sticky 余量的分诊规则原文**)与 §D-11-9 的连带后果第 ② 条
    - `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-04-PLAN.md` 的 §「执行前对照基线」表与 Task 3 的落盘命令表 —— 本任务沿用同一形状
    - `scripts/check-05-ui-uat.py` 的 `STATES` 常量与 `--browser` 参数取值;**`:2436` 的 `PANEL_SCROLLERS` 与 `:2438` 的 `PANEL_SCROLLERS_EXEMPT`**(item 9 的滚动者普查成员,判据以门自己的输出为准)
  </read_first>
  <action>
    **第 1 步 —— 建日志子目录。** 建 `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/`(**子目录,不覆盖 `idi-11-04` 落盘的 13 份基线** —— 那 13 份是本任务逐项对照的输入,覆盖掉就没有对照侧了)。

    **第 2 步 —— 逐门运行,把标准输出 + 标准错误 + 退出码写入同名日志。**

    | 日志文件 | 命令 | 预期 |
    |---|---|---|
    | `check-01-token-conformance.log` | `bash scripts/check-01-token-conformance.sh` | `PASS` / exit 0 |
    | `check-02-contrast.log` | `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures` / exit 0 |
    | `check-03-hidden-uniqueness.log` | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` / exit 0 |
    | `check-04-important-count.log` | `bash scripts/check-04-important-count.sh` | `PASS` / exit 0 |
    | `check-05-full.log` | `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` | **`exit=2`(设计如此:item 5 的两条 `--ai-smoke` 腿 BLOCKED)** |
    | `check-05-item8.log` | `.venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled` | `item 8: PASS` / exit 0 |
    | `check-05-item9.log` | `.venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled` | `item 9: PASS` / exit 0 |
    | `check-06-idi05-validation.log` | `.venv/bin/python scripts/check-06-idi05-validation.py` | `exit=0` |
    | `check-07-idi08-validation.log` | `.venv/bin/python scripts/check-07-idi08-validation.py` | `exit=0` |
    | `check-09-idi09-validation.log` | `.venv/bin/python scripts/check-09-idi09-validation.py` | `exit=0`(c1..c5 全 PASS) |
    | `check-10-idi10-validation.log` | `.venv/bin/python scripts/check-10-idi10-validation.py` | `exit=0` |
    | `pytest.log` | `.venv/bin/python -m pytest backend/tests -q --tb=short` | `219 passed, 6 skipped` |
    | `node-check-app.log` | `node --check frontend/app.js` | 无输出 / exit 0 |
    | `probe-05-resolve-color.log` | `.venv/bin/python scripts/probe-05-resolve-color.py` | `EXIT=0` |
    | `probe-07-focus-composite.log` | `.venv/bin/python scripts/probe-07-focus-composite.py` | `EXIT=0` |

    **门环境事实(省得重探,已由前四个计划实测):** `check-05` / `check-09` / `check-10` / 两个探针在本机**必须**用 Playwright 自带 chromium(无头);`check-05` 必须 `--browser bundled`(`channel="chrome"` + headless 会 CDP 挂死)。pytest **必须**用项目 `.venv`(环境 `python3` 是 miniconda,会让 4 个 `ai_caller` 测试假失败)。本机**没有 `timeout` 命令**。8765 端口可能有遗留 uvicorn,门走「复用,不新起」是预期。

    **第 3 步 —— 与 `idi-11-04` 基线逐项并排对照,并把每一处差异分诊。**

    把本任务的 `=== 逐项结论 ===` 块与 `idi-11-04` 的基线**逐项并排**写进 SUMMARY。判据:

    - **任何 FAIL 都是缺口** —— 停下报回;
    - **任何新增 BLOCKED 都是缺口** —— 停下报回(注意 `check-05` 的 item 5 必须仍是 **2** BLOCKED);
    - 断言**计数**或**读数**变化**允许**,但必须有**机制解释**。已知的预期差异:本计划把那条 1px 发丝线由「后三个面板的**上**边线」改为「前三个面板的**下**边线」⇒ `#ai-panel` 的 `rect.top` 位移 1px(p1:767→768),`#session-panel` 多一条 1px 下边线。**由 `geometry-before.log` / `geometry-after.log` 的实测读数确认,不得靠推断**(Phase 10 就出现过计划写「零布局改动」而实测矮了 3px);
    - `check-05` 全量 `exit=2` 的**成因集合必须仍是「item 5 的两条 `--ai-smoke` 腿」** —— 若成因集合扩大了,那就是缺口;
    - `check-09` 的 c2 / c4 断言数**必须增长**、**不得下降**(下降即断言被删)。

    **第 4 步 —— 1px 敏感门的读数登记与 `D-11-16` 分诊。**

    把 `check-05-item8.log` 与 `check-05-item9.log` 的**原始读数**与 `idi-11-04` 基线并排写进 SUMMARY:

    - `item 8`:基线 `PASS (13 条断言,0 FAIL,0 BLOCKED)`。登记 `INFO item8 sticky 原始数值` 的 `header.top` / `panel.top` 与那条容差断言的 actual 值。按 `D-11-16` 先问「**事实是否被改变**」:该断言描述的事实是「sticky 表头遮挡滚动正文」,而本计划只动 `#main-pane > section` 的横线边(`#doc-panel` 的 `border-left`、`position: sticky` / `top: 0` / `background` 三条逐字未动)⇒ **事实未被改变**;若读数有变,只更新读数与成因登记,**不得改判据**。
    - `item 9`:基线 `PASS (17 条断言,0 FAIL,0 BLOCKED)`。登记滚动者普查的实际成员与基线一致。**不得**把期望值写成「4」—— 判据以门自己的输出为准(磁盘实测 `PANEL_SCROLLERS` 是 3 个成员)。
    - 若 item 8 / item 9 出现 FAIL:**先停下**,把原始读数与机制写进 SUMMARY 报回;**绝不**为了让旧数字继续成立而回退 Task 1 的产品改动(`D-11-16` 的显式禁令)。

    **第 5 步 —— 仓库卫生与最终状态。**

    - `git status --porcelain frontend/` 仅列出 `frontend/style.css`;
    - `git status --porcelain scripts/` 仅列出 `scripts/check-09-idi09-validation.py`;
    - `git diff --stat -- frontend/app.js frontend/index.html backend/ frontend/vendor/ scripts/check-05-ui-uat.py` 为空;
    - `ls frontend/vendor/` 仅 `marked.min.js`;
    - `grep -o '/\* PAIR' frontend/style.css | wc -l` == 53;`grep -o '/\* ORDER' frontend/style.css | wc -l` == 1。

    **第 6 步 —— 不触碰任何代码。** 本任务只跑命令、写日志、写 SUMMARY。任何一条不达标都按产品缺陷报回,不就地修门、不就地修产品。
  </action>
  <verify>
    <automated>ls -1 .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/ | sort | tr '\n' ' '</automated>
    <fails_when>the listing does not contain all seventeen names: geometry-after.log, geometry-before.log, check-01-token-conformance.log, check-02-contrast.log, check-03-hidden-uniqueness.log, check-04-important-count.log, check-05-full.log, check-05-item8.log, check-05-item9.log, check-06-idi05-validation.log, check-07-idi08-validation.log, check-09-idi09-validation.log, check-10-idi10-validation.log, node-check-app.log, probe-05-resolve-color.log, probe-07-focus-composite.log, pytest.log</fails_when>
    <automated>grep -c '^FAIL' .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/check-05-full.log .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/check-06-idi05-validation.log .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/check-07-idi08-validation.log .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/check-09-idi09-validation.log .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/check-10-idi10-validation.log</automated>
    <fails_when>any of the five counts is non-zero (a verdict line begins at column 0 with "FAIL"; zero across all five is the "no new failures" criterion). NOTE: check-05's overall exit code is 2 BY DESIGN (item 5's two --ai-smoke legs are BLOCKED) — never read that exit code as a failure</fails_when>
    <automated>grep -E '^item (5|8|9):' .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/check-05-full.log</automated>
    <fails_when>the item 5 line does not read "item 5: BLOCKED  (9 条断言,0 FAIL,2 BLOCKED)", or the item 8 line does not read "item 8: PASS  (13 条断言,0 FAIL,0 BLOCKED)", or the item 9 line does not read "item 9: PASS  (17 条断言,0 FAIL,0 BLOCKED)"</fails_when>
    <automated>grep -E '^item c[0-9]:' .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/check-09-idi09-validation.log</automated>
    <fails_when>any of the five lines does not read PASS, or c2's count is not greater than 17, or c4's count is not greater than 20, or c1's count is not 59</fails_when>
    <automated>grep -E 'passed|failed' .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/pytest.log | tail -1</automated>
    <fails_when>the pytest summary line does not report 219 passed and 6 skipped (a lower passed count, or any failed count, is a gap)</fails_when>
    <automated>git status --porcelain frontend/ scripts/ backend/; git --no-pager diff --stat HEAD -- frontend/app.js frontend/index.html frontend/vendor/ scripts/check-05-ui-uat.py</automated>
    <fails_when>the status output lists any path other than "frontend/style.css" and "scripts/check-09-idi09-validation.py", or the diff --stat output is not empty</fails_when>
  </verify>
  <acceptance_criteria>
    - `gate-logs/idi-11-05/` 下恰有 17 个文件(2 个几何日志 + 15 条门的日志),名字与本计划表格逐条对应;`idi-11-04` 落盘的 13 份基线**未被覆盖**。
    - 五条浏览器门日志里 `^FAIL` 计数均为 **0**;`check-05-full.log` 的 item 5 = `BLOCKED (9 条断言,0 FAIL,2 BLOCKED)`、item 8 = `PASS (13)`、item 9 = `PASS (17)`;`check-05` 全量 `exit=2` 的成因集合仍只是 item 5 的两条 `--ai-smoke` 腿。
    - `check-09` 日志的 c1 = `PASS (59)`、c2 计数 > 17、c4 计数 > 20、c3 = `PASS (6)`、c5 = `PASS (5)`,全部 0 FAIL / 0 BLOCKED。
    - `pytest.log` 报告 `219 passed, 6 skipped`(用项目 `.venv`);`node-check-app.log` 无输出;两个探针日志各 `EXIT=0`。
    - SUMMARY 里给出与 `idi-11-04` 基线的**逐项并排对照表**;每一处差异都有「改前 → 改后」两列 + **机制解释**;`check-05 --item 8` 与 `--item 9` 的原始读数入册,并写明 `D-11-16` 的分诊结论(事实未变 ⇒ 只更新读数,不改判据);**未**回退任何产品改动。
    - `git status --porcelain frontend/ scripts/ backend/` 只列出 `frontend/style.css` 与 `scripts/check-09-idi09-validation.py`;`git diff --stat -- frontend/app.js frontend/index.html frontend/vendor/ scripts/check-05-ui-uat.py` 为空。
    - `grep -o '/\* PAIR' frontend/style.css | wc -l` == 53;`grep -o '/\* ORDER' frontend/style.css | wc -l` == 1;`ls frontend/vendor/` 仅 `marked.min.js`。
    - 本任务没有编辑任何代码文件(除写日志与 SUMMARY)。
  </acceptance_criteria>
  <done>17 份原始日志已落盘到 `gate-logs/idi-11-05/`(未覆盖 `idi-11-04` 的基线);逐项与基线并排对照且每处差异有机制解释;五条浏览器门零 FAIL、`check-05` 全量的 exit=2 仍只因 item 5 的两条 `--ai-smoke` 腿;`check-09` 的 c2 / c4 断言数增长、零下降;pytest 219 passed / 6 skipped;`check-05 --item 8` 与 `--item 9` 的读数已按 `D-11-16` 分诊登记且未回退产品改动;`app.js` / `index.html` / 后端 / vendor / `check-05` 逐字节未改。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 无外部输入边界 | 本计划只改 `frontend/style.css` 的一条 CSS 规则与注释、改 `scripts/check-09-idi09-validation.py` 的判据,并跑既有的门与探针:零用户输入处理、零鉴权、零数据访问、零网络调用、零新增资源加载、零新增依赖。攻击面限于**门脚本自起 `uvicorn` 并驱动无头浏览器**这一次本地动作 |
| 本地进程边界(门与探针) | `check-05` / `check-06` / `check-07` / `check-09` / `check-10` / 两个探针 / Task 1 的一次性几何探针都会 `ensure_server()` 自起(或复用)`uvicorn` 并用 Playwright 驱动无头 chromium 访问 `localhost`。它们与被测样本之间必须是**只读**关系 |
| 一次性探针脚本边界 | Task 1 的几何探针落在系统临时目录(`mktemp -d`)、跑完删除,不落进仓库树 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-11-23 | Tampering | 为让门绿而回退已裁定的产品改动 | **high** | mitigate | `#ai-panel` 的 `rect.top` 由 `767` 变 `768` 是**事实被如实登记**。缓解:(a) `D-11-16` 的分诊规则逐字写进 Task 3;(b) Task 1 的验收含「`#main-pane > section` 规则体逐字未改」与「规则位置未移」;(c) Task 3 的验收含 `git status --porcelain frontend/` 仅列 `style.css`,任何回退都会在这里现形;(d) 禁令块明写「不得为了让旧读数成立而回退」 |
| T-idi-11-24 | Tampering | 判据被降级为恒真 / 断言被删除 | **high** | mitigate | 「门绿着在看」正是本计划要修的形态,故本计划自己不得重犯。缓解:(a) Task 2 的验收要求 c1 计数 == 59、c2 / c4 **严格大于**基线、**零项下降**;(b) 三条变异逐条给出真实 FAIL 读数(唯一能证明守卫真的会失败的手段);(c) 明写禁止「只断言规则被写下了」;(d) 明写禁止 `section.hidden + section:not(.hidden)` 这条被验证者否决的路线 |
| T-idi-11-25 | Repudiation | 「零新增失败」这一结论缺少可复核的原始证据 | **high** | mitigate | 15 条门的原始输出与退出码全部落盘到 `gate-logs/idi-11-05/`,且**不覆盖** `idi-11-04` 的 13 份基线;SUMMARY 给出逐项并排对照表。判据是「`^FAIL` 计数为 0」与逐项计数,不是「看着一样」 |
| T-idi-11-26 | Tampering | 变异测试污染工作树 | medium | mitigate | `D-11-13` 的三条硬性要求逐字写进 Task 2:在**已提交**的树上做、`git checkout -- frontend/style.css` 定向还原、**禁用 `git stash`**;以 `git diff --exit-code` rc=0 与 `git hash-object` 逐字节相同两道独立证据收口;Task 2 验收含 `git status --porcelain frontend/` 为空 |
| T-idi-11-27 | Tampering | 围栏注释写坏静态门 | medium | mitigate | 围栏内注释**不得**出现「令牌名 + 冒号」(`check-02` 的 `DECL_RE` 扫围栏全文含注释)、不得点名两个已删卡片令牌(子串计数须为 0)。缓解:Task 1 验收含四条静态门全 PASS + `/* PAIR` == 53 + `/* ORDER` == 1 + 两个已删令牌名计数为 0 |
| T-idi-11-28 | Information Disclosure / Elevation | 无 | low | accept | 本计划零网络出口、零凭据、零鉴权路径、零用户数据处理;被测对象是本地静态文件与本地 `uvicorn` |
| T-idi-11-29 | Denial of Service | 全门复跑的运行时长 | low | accept | 与既有阶段同量级(单次 chromium 会话、多次导航);`--item` 可把范围收窄。本机无 `timeout` 命令,故不设外部超时 |
| T-idi-11-SC | Tampering | npm / pip / cargo 安装 | low | accept | 本阶段**零安装**:零新增依赖、零构建步骤(DESIGN.md D-06 硬约束)。验收:`ls frontend/vendor/` 仅 `marked.min.js` |
</threat_model>

<verification>
**承重证据(BINDING-1):**

- `grep -nE '#main-pane > section:not\(:last-child\)' frontend/style.css` 命中一行,且该行含 `border-bottom: 1px solid var(--color-border-subtle);`
- `grep -cE 'section \+ section' frontend/style.css` == 0
- `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4,c5` → `exit=0`;c1 `PASS (59)`、c2 计数 > 17、c3 `PASS (6)`、c4 计数 > 20、c5 `PASS (5)`,全 0 FAIL / 0 BLOCKED
- 三条变异的真实读数入册:M1 → c4 FAIL、M2 → c4 FAIL、M3 → c2 FAIL;三次还原后 `git diff --exit-code -- frontend/style.css` rc=0 且 `git hash-object` 逐字节相同;**全程未使用 `git stash`**
- `gate-logs/idi-11-05/geometry-before.log` 与 `geometry-after.log` 的并排读数:`#ai-panel` `rect.top` 767→768;p3 / checking / archive 可视首个面板 `borderTopWidth` 1px→0px
- `gate-logs/idi-11-05/` 下恰 17 个日志;五条浏览器门日志 `^FAIL` 计数均为 0;`check-05` 全量 `exit=2` 的成因集合仍只是 item 5 的两条 `--ai-smoke` 腿

**承重证据(BINDING-2):**

- `grep -cE 'exactly ONE consumer' frontend/style.css` == 0;`grep -cE 'Measured 4\.65|thinnest margin \(0\.15\)' frontend/style.css` == 0;`grep -cE '3\.24 / 3\.15' frontend/style.css` == 0 —— 三条均**按句锚定**:围栏内 `4.65` 另有 5 处(第 100 行 green-1 的读数 + 第 540 / 541 / 550 / 558 行的账目段)、`3.24` 另有 3 处(第 542 / 550 / 559 行的账目段)属**不同事实或历史**,BINDING-2 明令逐字保留,整文件计数永远到不了 0
- `grep -cE '分区改由相邻兄弟规则' frontend/style.css` == 0 —— `#main-pane` 规则体**自身**注释(`:781`)里的旧机制描述已就地改写;描述发丝线机制的注释**三处全部**与代码一致(`:781` / `:814-815` / `:828-855`)
- 围栏内零「令牌名 + 冒号」;`--color-surface-card` / `--shadow-card` 计数为 0;`/* PAIR` == 53、`/* ORDER` == 1
- `check-01`…`check-04` 全 PASS

**承重证据(BINDING-3):**

- `grep -cE '#doc-panel 计算底色 == body 计算底色' scripts/check-09-idi09-validation.py` == 1
- 变异 M3(`#doc-panel` 底色改归另一档)→ c2 FAIL

**仓库卫生:**

- `git status --porcelain frontend/ scripts/ backend/` 仅列出 `frontend/style.css` 与 `scripts/check-09-idi09-validation.py`
- `git diff --stat -- frontend/app.js frontend/index.html backend/ frontend/vendor/ scripts/check-05-ui-uat.py` 为空
- `ls frontend/vendor/` 仅 `marked.min.js`
- `.venv/bin/python -m pytest backend/tests -q --tb=short` → `219 passed, 6 skipped`
- `node --check frontend/app.js` 无输出
</verification>

<success_criteria>
- **BINDING-1 关闭:** 发丝线规则就地改写为「除 DOM 末个外都加下边线」;承重注释如实改写并显式登记机制前提;`check-09` 的 c4 扩写为覆盖全部 5 个样本状态的逐状态普查(可视首个面板顶部无发丝线 + 可见发丝线数 == 可见面板数 − 1 + 无线落窗口边缘),在 p3 / checking / archive 上真的运行;c1 / c4 的边框断言随规则换向(零删除);至少两条变异各给出真实 FAIL 读数并逐字节还原;1px 位移由改动前后的运行时读数确认并登记;全门复跑零新增失败、原始输出落盘。
- **BINDING-2 关闭:** 围栏内三处现在时陈述已改写为 Phase 11 之后的事实,历史段落保留,围栏仍是权威记录且不自我矛盾;静态门全 PASS。
- **BINDING-3 关闭:** c2 补上 `#doc-panel` 自身底色的断言,第五个容器不再「无门」,并以变异证明该断言会失败。
- **范围纪律:** 未改选实现路线;未改 `frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**` / `scripts/check-05-ui-uat.py` / `scripts/check-02-contrast.py` / `scripts/check-10-idi10-validation.py`;未处置 `WR-01` / `IN-01` / `IN-02` / `G2` / `999.2` / 暗色模式 / Nyquist 缺口 / 图标与空状态 / `.overlay-card` 底色 / `G1-01` / `REG-04` / `VIS-01`。
- **门禁:** `check-05` 全量 `exit=2` 的成因集合仍只是 item 5 的两条 `--ai-smoke` 腿;任何 FAIL 或新增 BLOCKED 都已停下报回,没有静默重述;pytest 基线 219 passed / 6 skipped 不降。
- 三条 BINDING 各自的实测证据(变异 FAIL 原文、几何并排读数、门日志)已写入 SUMMARY,不留推断。
</success_criteria>

<output>
Create `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-05-SUMMARY.md` when done
</output>

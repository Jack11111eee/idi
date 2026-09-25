---
phase: idi-06-layout-robustness
status: passed
verified: 2026-09-25T08:52:23Z
score: 10/10 must-haves verified
covered_files:

  - .planning/phases/idi-06-layout-robustness/idi-06-01-PLAN.md
  - .planning/phases/idi-06-layout-robustness/idi-06-01-SUMMARY.md
  - .planning/phases/idi-06-layout-robustness/idi-06-02-PLAN.md
  - .planning/phases/idi-06-layout-robustness/idi-06-02-SUMMARY.md
  - .planning/phases/idi-06-layout-robustness/idi-06-03-PLAN.md
  - .planning/phases/idi-06-layout-robustness/idi-06-03-SUMMARY.md
  - .planning/phases/idi-06-layout-robustness/idi-06-04-PLAN.md
  - .planning/phases/idi-06-layout-robustness/idi-06-04-SUMMARY.md
  - frontend/style.css
  - scripts/check-05-ui-uat.py
covered_digest: "v1:sha256:ccc470b1277f7311ecd96dbaa37d53b7364bd2b3b03aaa489fc8aadaf3f9e4c0"
behavior_unverified: 0
overrides_applied: 1
overrides:
  - must_have: "LAYOUT-02:窄窗口不破版 —— ≥768px 无内容遮挡"
    reason: "768–855px 下 fixed 居中横幅盖住 #doc-panel-header 的标题;几何既有且被 UI-SPEC 范围锁排除在阶段可修范围之外。经项目所有者本次会话显式选择 remediation (b)(收窄承诺 + 更正覆盖主张)后,本条登记为已知缺口,收窄为「badge 不被横幅遮挡」。"
    accepted_by: "Jack11111eee"
    accepted_at: "2026-09-22T06:43:50Z"
re_verification:
  previous_status: passed
  previous_score: 10/10
  previous_verified: "2026-09-22T08:05:02Z"
  gaps_closed: []
  gaps_remaining: []
  regressions: []
  reason: "内容真变后的重验证 —— frontend/style.css 与 scripts/check-05-ui-uat.py 在 2026-09-22 之后被 Phase 7/8 与 quick 260925-iin 改动,故在 HEAD 上重跑复核面而非只重算指纹。详见 §重验证披露。"
advisory:
  - finding: "WR-01: `_idi06_reach` 的前提链只拒绝 `injected is None`;两个调用点传的是整数计数,`0` 不是 `None`。容器不溢出时把「滚到底」降级为 info(),但末条断言仍照跑 —— 此时末条平凡落在容器内,记 PASS。"
    category: other
    reason: "改法(要求正计数 + 不可滚即 blocked)见 idi-06-REVIEW.md WR-01;不阻塞本阶段。今日两个调用点实测注入 40 / 60 条,未触发。"
    evidence_status: "none provided(未构造出可复现的红;今日注入计数为正)"
  - finding: "WR-02: `_idi06_clearance_assert` 判定的是滚动位置而非裁切 —— 部分滚出容器的元素 `intersects` 仍为 True 而 clearance 为负,会误报。"
    category: other
    reason: "标签声称测裁切,实际测滚动位置;改法见 REVIEW WR-02。**本轮复核新增一层:** 2026-09-24 用户裁定(commit `63fba08`,Phase 8 期间)给该普查加了「内容区声明集」——高度 ≥ 容器 padding 盒一半的可聚焦元素**声明**而不断言。当时唯一实测触发行 `#round-doc`(clearance -66.6px)因此离开断言集;机制本身未改,残余误报面收窄为「部分滚出容器的控件行」。"
    evidence_status: "none provided(需要一次面板滚动 + 一个部分滚出的控件行才复现)"
  - finding: "WR-03: `DOC_PANEL_W_MIN_PX / _VW / _MAX_PX` 是 `frontend/style.css:228` 的硬编码镜像,无绑定。收窄 clamp 会让探针静默失去判别力。"
    category: other
    reason: "失败方向是丢覆盖而非报错。改法(从文件文本解析 clamp 三参数并断言相等)见 REVIEW WR-03。常量现位于 `scripts/check-05-ui-uat.py:1655-1657`(仅行号漂移,内容未变)。"
    evidence_status: "none provided(未实际收窄 clamp 复现)"
  - finding: "WR-04: `#doc-panel` 实测宽探针无法在其标签所指的失效模式上失败 —— 该失效模式对滚动容器结构性不可能(`min-width: 0` 的承重归因不成立)。"
    category: architectural
    reason: "产品行为正确(屏幕无破损),故为 WARNING 而非 critical;门与两处承重 CSS 注释把正确结果归因给了未做功的声明。见 idi-06-REVIEW.md WR-04。"
    evidence_status: "none provided(由测量证明,非推断;未构造可复现的红)"
  - finding: "IN-01: `_idi06_census` 的 docstring 声称 item 9 消费其返回值,实际 item 9 从不调用它;唯一调用点丢弃返回值,每次运行多跑 6 次同一份 DOM 普查。"
    category: other
    reason: "注释与代码不符(「名必须说实话」的同一条方法论);无行为影响。HEAD 复核:`_idi06_census` 定义于 `:2131`,其 docstring `:2134-2135` 仍写「波次 3 起 item 9 消费同一份返回值做断言」;唯一调用点是 item 8 的 `:2390`(返回值丢弃);item 9 自己在 `:2596` / `:2654` 直接调 `_IDI06_CENSUS_JS`。"
    evidence_status: "none provided"
  - finding: "IN-02: `_l2_guard_shape` 用 `text.count('@media')` 统计子串,标签却写成「== 决策(被实测推翻 ⇒ 0)」。一条无关的 `@media` 会让它 FAIL 并把修复者指向 L-2 决策记录。"
    category: other
    reason: "**本轮复核:该项的前提已被后续阶段改变。** 计数现在是 **1** —— Phase 7 落地了 `@media (prefers-reduced-motion: reduce)`(`frontend/style.css:1706`),`EXPECTED_MEDIA_QUERIES` 随之由 0 改为 1,断言标签、`info()` 串与常量上方的注释都已同步写明「Phase 7 的减弱动效媒体块 ⇒ 1;L-2 的窄窗口守卫仍未写出 —— 两者不是同一件事」。故「标签写成被实测推翻 ⇒ 0」这一半已不再成立。**子串计数的脆弱性本身仍在**:任何再出现的无关 `@media` 都会让该断言 FAIL,且修复者仍需读注释才能分辨。改法(只统计含 `max-width` 的 `@media`)见 REVIEW IN-02。"
    evidence_status: "none provided(未再引入第三个 @media 复现)"
  - finding: "IN-03: 评审新增的第三条 info 项 —— `frontend/style.css` 里两处 `min-width: 0` 注释断言了一个在滚动容器上不可能发生的机制。"
    category: other
    reason: "见 idi-06-REVIEW.md IN-03。HEAD 复核:两条注释仍在(`frontend/style.css:597-601` 与 `:618-622`),仍称「`min-width: auto` 胜出,长不可断内容能把 `#doc-panel` 顶得比它的 `clamp()` 还宽」;而两个元素都声明了 `overflow-y: auto`(`:595` / `:615`),是自动最小尺寸为 0 的滚动容器,故该结论不成立。无行为影响。"
    evidence_status: "none provided"
  - finding: "A11Y-07 的普查覆盖边界:命中区普查只判定 `visible` 行,而样本只有 p1 / checking / p3。在三个样本里都 `display: none` 的控件其命中区在本阶段未被测量过。"
    category: other
    reason: "A11Y-07 的实质(紧凑控件达 24×24)在已采样状态上已证;此为覆盖边界的诚实登记,不是现行失败。HEAD 复核:`_idi06_hit_assert` 的 `rows = [r for r in data['hits'] if r['visible']]`(`:2659`)未变;item 8 的普查输出仍显式打印 `visible=False below24=None` 的行,不把它们算作达标或未达标。"
    evidence_status: "none provided(未构造未采样状态)"
---

# Phase 6: 布局稳健性 (idi-06) Verification Report

**Phase Goal:** 布局结构常量只有一个来源;窄窗口不破版;侧栏不再是四个滚动容器的套娃;紧凑控件达到 24×24 命中区。
**Verified:** 2026-09-25T08:52:23Z(HEAD `0b6283a`,分支 `ui/baseline-and-tokens`)
**Status:** passed
**Re-verification:** Yes —— **内容真变后的重验证**(非记账性指纹刷新)。上一轮为 LAYOUT-02 缺口闭合后的重验证(`0bc298e`,结论 `passed` / `10/10`);本轮因 `covered_files` 中的两个文件被后续阶段与 quick `260925-iin` 改动而在 HEAD 上重跑复核面。

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | 布局结构常量只有一个来源 | ✓ VERIFIED | `--doc-panel-w: clamp(340px, 30vw, 480px)`(`frontend/style.css:309`)是文档面板宽的唯一来源,被 `#doc-panel { flex: 0 0 var(--doc-panel-w) }`(`:612`)消费;收起态由 `--doc-panel-w-collapsed`(`:310`)控制。HEAD 复跑 item 8 的判别性探针:1440→432.0/432.0、1024→340.0/340.0、768→340.0/340.0,与 clamp 解析值逐位相等。`--sidebar-w` 按 D-03 不引入(该偏离已登记在 06-CONTEXT D-03 与 UI-SPEC L-1)。 |
| 2 | LAYOUT-01: `#state-badge { right: 448px }` 魔法数消除 | ✓ VERIFIED | HEAD 直接读源码:`#state-badge`(`frontend/style.css:861-869`)只有 `padding/border-radius/background/color/font-size/font-weight/z-index` —— 无 `position`、无 `right`;badge 是 `#doc-panel-header` 内的流内元素。运行时 item 8 读 computed `position: static`、`right: auto`(PASS)。机制是流内化而非 calc()/absolute,该契约反转由 06-CONTEXT D-03 显式采纳。 |
| 3 | LAYOUT-03: `#state-badge` 不再遮挡滚动内容 | ✓ VERIFIED | badge 在正常流内(见上条),结构上不可能压住 `#doc-panel-body` 的正文;`z-index: var(--z-badge)` 在静态元素上惰性。item 8 的 `position == static` + `right == auto` 两条断言机器化该禁令。 |
| 4 | LAYOUT-04: 侧栏滚动容器套娃收敛 | ✓ VERIFIED | HEAD 直接读源码:`.event-list`(`:756-765`)与 `#annotation-list`(`:1106-1111`)均**无** `max-height`、无 `overflow-y`(原地删除,`6adcaa3`)。item 9 的 DOM 普查断言面板区滚动者集合**恰为** `{#main-pane, #chat-messages, #latest-check}`(PASS,口径取「恰好」),`#ai-events` / `#annotation-list` 计算 `max-height == none`(PASS)。基线 3 个限高者降为 1。**已登记的偏离:** ROADMAP 交付物第 6 条要求连 `#latest-check` 一并删除,UI-SPEC D-11 保留它,并按 A-5(UI-SPEC :568)把 SC#3 措辞收窄为「面板区内恰好两个滚动者」;偏离有承重理由且被门机器化(`max-height: 30vh` 源码计数 == 1 的保留护栏,实测 1,命中 `:1323`)。**该收敛的副作用回归见下节 —— 已闭合。** |
| 5 | A11Y-07: 紧凑控件命中区达到 24×24,侧栏未重构 | ✓ VERIFIED | HEAD 直接读源码:`.annotation-answer summary`(`:1197-1204`)原地加 `min-height: 24px` / `min-width: 24px`(既有四条声明逐字保留)。item 9 的命中区普查按 DOM 遍历断言每个可见可交互元素 ≥24×24,p1(11 行)/checking(9 行)/p3(10 行)三样本全 PASS(未达标清单均为空),`<summary>` 实测 722×24。侧栏零重构。覆盖边界见 advisory 末条。 |
| 6 | LAYOUT-02 前半句:≥1024px 无横向溢出 | ✓ VERIFIED | item 8 在 1440 与 1024 两处的硬断言 `documentElement.scrollWidth <= clientWidth` PASS(复跑实测 1440/1440 与 1024/1024,overflow=0)。判别性探针 `#doc-panel` 实测宽 ≤ clamp 上界 PASS(见 Truth 1)。**这两条硬断言在 gap 收口后逐字未变,本轮逐字复核仍然在位**(`scripts/check-05-ui-uat.py:2332-2340`)。 |
| 7 | LAYOUT-02 后半句:≥768px 无内容遮挡 | ✓ PASSED (override) | 768–855px 下 `#stream-banner` 压住 `#doc-panel-header` 的 h1 是**实测事实**,经项目所有者显式裁定 remediation (b),登记为**已知偏离**(UI-SPEC A-10,`idi-06-UI-SPEC.md:585`)并把该承诺收窄为「badge 不被横幅遮挡」。收窄后的承诺由 item 8 的 badge × banner 不相交断言机器化(PASS @768 / 1024 / 1280)。**Override: 项目所有者显式裁定 — accepted by Jack11111eee on 2026-09-22T06:43:50Z。** 本轮**未重新提起**该偏离(见 §关于「不得凭空制造新失败」)。 |
| 8 | SC#2: badge 在每个宽度都贴在文档区右上角且不被 banner 盖住 | ✓ VERIFIED | item 8 的 badge × banner 不相交断言(`:2225-2232`)在 **768 / 1024 / 1280 三处** PASS(`BADGE_BANNER_WIDTHS = (768, 1024, 1280)`,`:1615`),且**该断言在 gap 收口后逐字未变**。badge 恒在面板标题行右端,banner 居中于视口。HEAD 实测:768px badge=[638.97,739.89]×[7,32] vs banner=[285.34,482.66]×[12,39];1024px badge=[894.97,995.89] vs banner=[413.34,610.66];1280px badge=[1150.97,1251.89] vs banner=[541.34,738.66]。**注:** 上一版报告此处写「五处」并把 900 / 1440 列入,与 harness 实际枚举不符(1440 只出现在文档级溢出诊断里);本轮据 HEAD 源码更正。 |
| 9 | SC#5: `#brainstorm-view h2` 未因结构性改动而变 | ✓ VERIFIED(以实际值为准) | item 4 PASS:`#brainstorm-view h2` 计算 `font-size` == `var(--text-md)`、`color` == `var(--color-action-warning)`。ROADMAP SC#5 写的字面值「14px / `#8a6508`」是**陈旧的路线图漂移**(Phase 4/4.1 令牌迁移已换值);SC#5 的**意图**(未因结构性改动而变)成立。 |
| 10 | 本阶段验收门自身诚实(item 8 的 768px 覆盖主张 == 它实际测到的) | ✓ VERIFIED | HEAD 直接读源码并复跑运行时:`scripts/check-05-ui-uat.py:2324-2348` 的注释与 `info()` 串均已改写 —— 显式写明 768px 的「无内容遮挡」承诺**未被覆盖**(「badge × banner 断言只测 badge 那一对,banner × #doc-panel-header 的 h1 不在覆盖范围内 —— 显式「未覆盖」」),并携带实测数值(h1 = 439.0–481.0 × 8–28 vs banner = 285.3–482.7 × 12–39,重叠 42×16px,相交带 768–855px),且指明其为**已知缺口**、指向 `idi-06-UI-SPEC.md §L-2(A-10 行)`。**本轮实跑 `--item 8` 逐字复现该 INFO 行。** |

**Score:** 10/10 truths verified(0 present-behavior-unverified,1 PASSED by override)

### 本阶段 L-4 的副作用回归 —— 已闭合(不记为缺口,亦不隐藏)

本节的目的是把本阶段**最重的一条后果**如实留在它自己的报告里。里程碑审计 `v1.14-MILESTONE-AUDIT.md` §5 记录的唯一阻断项正是由本阶段引入;它已在 quick `260925-iin` 中闭合并补上缺失的门。**本条不构成现行缺口**(现状已在 HEAD 上第一手复验为绿),故不进 `gaps:`、不改判 `status`。

| 环节 | 事实 | 证据 |
|---|---|---|
| 回归引入 | `idi-06-02` 的 L-4 收敛(commit `6adcaa3`)把 `max-height: 55vh` 与 `overflow-y: auto` 从 `.event-list` **原地删除**。`.event-list` 即 `#ai-events`(`frontend/index.html:76`,`frontend/app.js:5` 绑定)。无 `overflow` 声明 ⇒ 计算 `overflow-y: visible` ⇒ 它不再是滚动容器 | `git show 6adcaa3 -- frontend/style.css`;HEAD `.event-list`(`frontend/style.css:756-765`)确无这两条声明 |
| 失效机制 | `app.js` 的 `eventsEl.scrollTop = eventsEl.scrollHeight` 因此成为 **CSS 规范意义上的 no-op**(非可滚动元素的 `scrollTop` 恒为 0)。同文件其余 `scrollTop` 写入点全在 `chatMessages` 上,无人滚外层 `#main-pane` | 基线 `0c658aa:frontend/app.js:241` 该行存在且当时 `.event-list` 带 `max-height: 55vh; overflow-y: auto`(`0c658aa:frontend/style.css:307-312`)⇒ 基线可用;`6adcaa3:frontend/app.js:246` 该行仍在而 CSS 声明已删 |
| 门覆盖 | **零覆盖,且更差**:item 9 的滚动者普查**肯定地断言**了新状态(`#ai-events 计算 max-height == none`),而它唯一的滚动断言(「末条内容可达」)自己先设 `c.scrollTop = scrollHeight` 再读 rect —— 与「自动跟随」是不同性质 | 审计 §5;`_IDI06_REACH_JS` 在 `scripts/check-05-ui-uat.py:2486` 设 `c.scrollTop = scrollHeight` |
| 修复 | quick `260925-iin` FIX 1(commit `11fdedb`):`frontend/app.js:253` 改为 `item.scrollIntoView({ block: 'nearest' })` —— 跟随**外层** `#main-pane`,故 **L-4 未被回退**(`#ai-events` 仍无 `max-height` / `overflow-y`) | HEAD `frontend/app.js:253`;`grep -n 'eventsEl.scrollTop' frontend/app.js` 零命中;HEAD 复跑 item 9 的滚动者集合断言仍为 `{#main-pane, #chat-messages, #latest-check}` |
| 补门 | FIX 2(commit `1560bd6`):item 9 新增「自动跟随」断言,落点**在 `item9()` 内第一个 `_idi06_reach()` 之前**(新块 `:2733-2799` vs 首个 `_idi06_reach` 调用 `:2811`),因为 `_IDI06_REACH_JS`(`:2486`)自己会设 `scrollTop`,排在它之后「追加前 scrollTop == 0」的前提恒假、门会退化成空转 | 本轮第一手复核该落点;本轮实跑读数:`before=0 after=1721 scrollHeight=2640 clientHeight=900 pane=[0,900] last=[848,900]` ⇒ PASS |
| 反空转 | 该断言有五条 `blocked()` 前提(容器存在 / `renderEvent` 可用 / `before == 0` / 容器可见且高 > 0 / 注入后有条目 / 容器真的可滚),任一不成立记 BLOCKED 而非 PASS | `scripts/check-05-ui-uat.py:2766-2784` |
| 变异证明 | 中和 FIX 1 后该断言变 FAIL 且 exit 1(`after=0 last=[2569,2621] pane=[0,900]`);还原后回到 PASS(17) | `260925-iin-SUMMARY.md` coverage D2;`260925-iin-VERIFICATION.md` Truth 2。**本轮未重跑该变异** —— 它要求临时改写 `frontend/app.js`,超出本报告「只读复核」的范围;我改为独立核了使变异有意义的三处机制(落点、判据 `after>0 ∧ 末条 rect ⊆ 可见盒`、前提链形态) |

**因此:本阶段 L-4 的收敛结论**不变**;它留下的自动跟随副作用已闭合,并由一条经变异证明的门守着。** 本条同时修正了 ROADMAP §Phase 6 的 Deliverables 与 UI-SPEC §L-4 未预见的那一面 —— 两处文本均**未改**(改会作废指纹),故此处是它唯一的登记面之一。

### Deferred Items

无。Phase 7(交互状态与焦点样式)与 Phase 8(可访问性语义与键盘)均不涉及窄窗口布局或 `#stream-banner` 的定位;backlog 999.1 是 Phase 4 的两条卫生项(其字号档那一项已由 quick `260925-iin` FIX 3 关闭)。已裁定的 768–855px 遮挡不被任何后续阶段承接 —— 它是**已知偏离**(A-10),不是待办。自动跟随回归**已闭合**,故也不是 deferred。

### Advisory (New Scope, Unevidenced)

| # | Finding | Category | Why Advisory |
|---|---------|----------|--------------|
| 1 | WR-01 空转 PASS:`_idi06_reach` 只拒绝 `injected is None`,整数 0 通过 | other | 潜在,非现行失败(今日注入 40 / 60) |
| 2 | WR-02 clearance 断言测的是滚动位置而非裁切 | other | 2026-09-24 的内容区声明集把唯一实测触发行移出断言集;残余面为部分滚出的控件行,需一次滚动才复现 |
| 3 | WR-03 clamp 探针常量与 style.css 无绑定,收窄 clamp 会静默丢覆盖 | other | 未实际收窄复现 |
| 4 | WR-04 `#doc-panel` 宽探针在其标签所指失效模式上结构性不可能失败 | architectural | 产品行为正确;归因错误,未构造可复现的红 |
| 5 | IN-01 `_idi06_census` 的 docstring 与返回值无消费者,自相矛盾 | other | 注释与代码不符,无行为影响 |
| 6 | IN-02 `@media` 计数用子串匹配,标签高估了它统计的东西 | other | **前提已变**:计数现为 1(Phase 7 的 `prefers-reduced-motion` 块),标签与注释已同步;子串计数的脆弱性仍在 |
| 7 | IN-03 `frontend/style.css` 两处 `min-width: 0` 注释断言了滚动容器上不可能的机制 | other | 无行为影响;注释仍在 `:597-601` / `:618-622` |
| 8 | A11Y-07 普查只覆盖三样本中可见的控件,未采样状态下可见的控件未被测量 | other | 已采样状态上已证;覆盖边界登记 |

**Re-verification 说明:** 以上 8 条均为上一版报告 advisory 的延续(WR-04 / IN-03 为 `f9d7c33` 增量评审新增),**本轮逐条对照 HEAD 重核**。结论:7 条描述仍然准确(仅行号漂移);**IN-02 的前提被后续阶段改变**(见其 `reason`),故其描述已就地更新而非照抄。它们不是本阶段的缺口,亦不阻塞;均无确定性证据(未构造可复现的红),故维持 advisory 分类,不计入 Step 9 规则 1。

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `frontend/style.css` | sticky 表头 + `min-width: 0` ×2 + 六目标 `overflow-wrap: anywhere` + 删两条内滚动 + summary 尺寸下限 | ✓ VERIFIED | 全部改动在 HEAD 上逐条读源码确认在位:`#doc-panel-header { position: sticky; top: 0; background: var(--color-surface); border-radius: 0 }`(`:649-654`);`min-width: 0` 在 `#main-pane`(`:602`)与 `#doc-panel`(`:623`);六目标 `overflow-wrap: anywhere`(`:1486-1489`);`.event-list` / `#annotation-list` 两条内滚动已删;`.annotation-answer summary` 的 `min-height/min-width: 24px`(`:1202-1203`)。**上一版报告的「本阶段自评审基线 `d6c375c` 起零 diff」证据已不适用** —— 该文件被 Phase 7/8 与 quick `260925-iin` FIX 3 合法改动过(见 §重验证披露);本轮的替代证据是「逐条读源码 + 运行时门」,而非 diff 为空。 |
| `scripts/check-05-ui-uat.py` | item 8(L-1 三条 + 三宽度诊断)+ item 9(滚动者普查 / 可达性 / 保留项护栏 / 两条普查 / **自动跟随**) | ✓ VERIFIED | 断言确实执行、前提检查齐备、多数断言强(见下「断言强度复核」)。item 8 的 768px 分支仍显式声明「未覆盖」并携带实测数值(Truth 10)。item 9 现为 **17** 条断言(上一版 16),新增的第 7 条为自动跟随(见上节)。 |

**断言强度复核(不只看 exit code,本轮重做):** 我逐条核了可能「在坏实现上照样 PASS」的断言,并**特别核对新增的门有没有削弱既有断言、以及后续阶段的改动有没有削弱它们**。结论:
- **1440 / 1024 硬断言未削弱**:`if width >= 1024: ok_true(... scrollWidth <= clientWidth ...)` 逐字保留,标签仍为「LAYOUT-02 的字面承诺:≥1024px 无横向溢出」。
- **badge × banner 不相交断言未削弱、未改标签**:仍为 `ok_true(..., not _rects_intersect(badge, banner), "不相交", ..., "L-1 的门断言几何不相交,不是「横幅不存在」")`,且 `_IDI06_BADGE_BANNER_JS`(`:1707`)仍**只**返回 badge 与 banner 的 rect —— 这正是「未覆盖」为真的事实基础。
- **`#doc-panel` 上界探针与守卫形态断言**:仍在,未改(见 advisory WR-04 / IN-02)。
- **滚动者普查**:按 DOM 遍历 `#main-pane` 及其全部后代算 `overflowY`,用 `==` 而非 `<=` 比较集合 —— 新增第四个滚动者会 FAIL;另有范围自检(`#main-pane` 必须在实测结果里)。
- **保留项护栏是双条的**:`#chat-messages overflow-y == auto` 抓「被改值」,`#latest-check` 的 `max-height: 30vh` 按**源码文本计数 == 1** 抓「被悄悄删掉」。
- **命中区普查**:`require_summary=True` 分支先断言主要对象 `<summary>` 存在且可见,读不到即 `blocked`;`visible` 一栏被用作承重判据。
- **item 8 的 badge×banner 与 sticky 断言各有前提检查**,前提不成立记 `blocked` 而非 PASS。
- **新增的自动跟随断言是反空转的**:探针 JS 内**零 `scrollTop` 赋值**(只读),并有五条 `blocked()` 前提;落点在首个 `_idi06_reach()` 之前(见上节)。

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `#doc-panel-header` 的 sticky | `#doc-panel { overflow-y: auto }` 的滚动行为 | sticky 的滚动容器是最近可滚祖先;header 是 `#doc-panel` 的直接 flex 子项 | ✓ WIRED | 本轮复跑 item 8 PASS:滚到底后 `header.top == panel.top`(实测 0.000px ≤ 1px)。`position: sticky` 在 `frontend/style.css:650`;`#doc-panel { overflow-y: auto }` 在 `:615`。 |
| `--doc-panel-w` 令牌 | `#doc-panel { flex: 0 0 var(--doc-panel-w) }` | 单一来源 → 唯一消费者 | ✓ WIRED | 复跑实测 1440→432.0、1024→340.0、768→340.0,与 clamp 解析值逐位相等。 |
| `.annotation-answer summary` 的 `min-height/min-width: 24px` | item 9 的命中区普查断言 | 运行时 `getBoundingClientRect()` 逐元素读数 | ✓ WIRED | summary 实测 722×24;三样本普查未达标清单均为空。 |
| `renderEvent()` 的 `eventsEl.appendChild(item)` | 外层滚动者 `#main-pane` 跟随最新条目 | `item.scrollIntoView({ block: 'nearest' })`(`frontend/app.js:253`) | ✓ WIRED | 本轮复跑 item 9 的新断言 PASS:`before=0 after=1721`,末条 rect `[848,900]` ⊆ pane `[0,900]`;探针全程未设 `scrollTop`。**这是本阶段 L-4 副作用回归的闭合链接**(见上节)。 |
| `#stream-banner` 的 fixed 定位 | `#doc-panel-header` 的 h1(768–855px) | 两者都在同一 0–39px 带内,banner `z-index: 20` 高于 header 的 `z-index: auto` | ⚠️ ADJUDICATED (override) | 几何仍相交(本阶段未触碰 `#stream-banner`,后续阶段亦未改其定位)。**这不是本阶段的独立缺口**:它是 Truth 7(已 override)的直接因果链,已随 LAYOUT-02 的 768px 承诺收窄一并裁定,登记于 UI-SPEC A-10。本轮**不把它重新提起为 blocker**。 |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| item 8 badge/banner 几何 | `getBoundingClientRect()` on `#state-badge` / `#stream-banner` | 真实 DOM;banner 由应用自身 `showStreamBanner()` 置为可见(不手工拼 DOM) | Yes | ✓ FLOWING |
| item 9 滚动者普查 | `getComputedStyle(el).overflowY` 遍历 `#main-pane` 后代 | 真实 DOM | Yes | ✓ FLOWING |
| item 9 命中区普查 | `getBoundingClientRect()` on 交互元素 | 真实 DOM;`<summary>` 经应用自身 `renderAnnotations()` 造出 | Yes | ✓ FLOWING |
| item 9 可达性 | `scrollHeight` / `clientHeight` / `scrollTop` + 末条 rect | 真实 DOM;内容经应用自身 `renderEvent()` / `renderMarkdown()` 注入 | Yes | ✓ FLOWING |
| item 9 自动跟随 | `#main-pane.scrollTop` 前后读数 + 末条 rect | 真实 DOM;条目经应用自身 `renderEvent()` 注入,探针 JS 零 `scrollTop` 赋值 | Yes | ✓ FLOWING |
| 768px 遮挡判据 | — | **无数据源:该判据没有任何探针** | No | ✗ DISCONNECTED — **已登记为已知缺口(A-10),按 override 裁定,不再是待修项** |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| item 8 全绿(13 条断言) | `.venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled` | `item 8: PASS  (13 条断言,0 FAIL,0 BLOCKED)`,exit=0 | ✓ PASS |
| item 8 的 768px 诊断陈述实测真相 | 同上,过滤 `L-2 @768` | 运行时 INFO 行逐字输出「保持只读诊断(768px 处的承诺是「无内容遮挡」,该承诺未被覆盖:badge × banner 断言只测 badge 那一对,banner × #doc-panel-header 的 h1 不在覆盖范围内 —— 显式「未覆盖」。实测:h1 = 439.0–481.0 × 8–28 vs banner = 285.3–482.7 × 12–39,重叠 42×16px,相交带 768–855px。这是已知缺口(既未满足、也未断言),收窄已登记在 idi-06-UI-SPEC.md §L-2(A-10 行))」 | ✓ PASS |
| item 9 全绿(**17** 条断言,含新增的自动跟随) | `.venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled` | `item 9: PASS  (17 条断言,0 FAIL,0 BLOCKED)`,exit=0;自动跟随读数 `before=0 after=1721 scrollHeight=2640 clientHeight=900 pane=[0,900] last=[848,900]`;滚动者集合 `['#main-pane', '#chat-messages', '#latest-check']`;命中区三样本「未达标 []」 | ✓ PASS |
| item 10 全绿(42 条断言,含新增的枚举同步门) | `.venv/bin/python scripts/check-05-ui-uat.py --item 10 --browser bundled` | `item 10: PASS  (42 条断言,0 FAIL,0 BLOCKED)`;`FOCUSABLE_SELECTOR 与 :focus-visible 枚举逐项(含顺序)一致` PASS,两侧均 7 项、对称差 `[]` | ✓ PASS |
| 令牌门 | `bash scripts/check-01-token-conformance.sh` | `PASS`,exit=0 | ✓ PASS |
| 对比度门 | `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`(53 PASS + 1 ORDER 0.363),exit=0 | ✓ PASS |
| hidden 唯一性 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS`,exit=0 | ✓ PASS |
| `!important` 计数 | `bash scripts/check-04-important-count.sh` | `PASS`,exit=0 | ✓ PASS |
| 单元/集成测试基线 | `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped, 1 warning in 9.56s`(基线未变) | ✓ PASS |
| `app.js` 语法 | `node --check frontend/app.js` | exit=0 | ✓ PASS |
| 债务标记门(改动文件) | `grep -nE "TBD\|FIXME\|XXX" frontend/style.css scripts/check-05-ui-uat.py` | 零命中 | ✓ PASS |

**关于被裁定的 768px 遮挡:** 复验**未**重跑遮挡探针来「再证伪一次」—— 该事实已被前版报告独立复现两次(p1 / p3 两样本、`elementFromPoint` 四点采样、边界扫描 855/856),并在 gap 收口中被项目所有者显式裁定为已知偏离。重跑只会复述已裁定的事实。

### Probe Execution

无 `scripts/*/tests/probe-*.sh` 约定探针,PLAN/SUMMARY 亦未声明探针路径;本阶段的「探针」即 check-05 的 item 8 / item 9,已在上表实际运行。

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| LAYOUT-01 | 06-01, 06-04 | `#state-badge { right: 448px }` 魔法数消除 | ✓ SATISFIED | 见 Truth 2;实质达成(流内化),机制偏离已由 D-03 显式登记 |
| LAYOUT-02 | 06-02, 06-03, 06-04 | 窄窗口不破版:≥1024px 无横向溢出,**≥768px 无内容遮挡** | ✓ SATISFIED (override) | 前半句 ✓ VERIFIED(Truth 6);后半句的 768–855px 子段为**已裁定的已知偏离**(A-10),承诺收窄为「badge 不被横幅遮挡」并机器化(Truth 7/8)。**Override: 项目所有者显式裁定 remediation (b)。** |
| LAYOUT-03 | 06-01, 06-04 | `#state-badge` 不再遮挡滚动内容 | ✓ SATISFIED | 见 Truth 3 |
| LAYOUT-04 | 06-02, 06-04 | 侧栏滚动容器套娃收敛 | ✓ SATISFIED | 见 Truth 4;SC#3 措辞收窄已按 A-5 登记。**该收敛的副作用回归(自动跟随)已闭合并由新门守着** —— 见上节;它不改变本需求的达成判定(需求文本「收敛」已达成),但它是本需求历史的一部分。 |
| A11Y-07 | 06-03, 06-04 | 紧凑控件达到 24×24 命中区 | ✓ SATISFIED | 见 Truth 5;覆盖边界见 advisory 末条 |

**Orphaned requirements:** 无。四个计划的 `requirements:` 字段合计覆盖 `LAYOUT-01/02/03/04 + A11Y-07`,与 ROADMAP Phase 6 的 Requirements 行逐字一致。`06-04`(gap-closure)声明全部五个 ID。

**REQUIREMENTS.md 状态说明:** 该表反映的是 `phase.complete` 流程而非本复验,且**本轮已把该文件移出 `covered_files`**(见 §重验证披露),故其状态不再影响本报告指纹。按任务约束,复验**不编辑** `REQUIREMENTS.md` / `ROADMAP.md`(编辑会作废指纹)。`ROADMAP.md` §Phase 6 的 Gates 行与承诺文本在本轮复核中逐字未动 —— 即 A-10 声明的「路线图承诺不改」成立。

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `scripts/check-05-ui-uat.py` | 2324-2348 | **已修复**:原 768px 分支的**假覆盖主张**(声称「无内容遮挡」承诺已被覆盖) | ✅ RESOLVED | commit `b15bd89` 改写为显式「未覆盖」+ 实测数值 + A-10 指向;本轮逐字确认旧措辞在 harness 源码中零命中(`grep -rn` 于 `scripts/` 与 `frontend/` 均无返回) |
| `scripts/check-05-ui-uat.py` | 2539 / 2613-2620 / 2134-2135 / 1693 | 空转 PASS / 测错对象 / 常量无绑定 / docstring 与代码不符 | ⚠️ Warning | 见 advisory 1-3、5-6;均未在今日触发 |
| `frontend/style.css` | 597-601, 618-622 | 两处 `min-width: 0` 注释断言了一个在滚动容器上不可能发生的机制 | ⚠️ Warning | 见 advisory 7(IN-03);无行为影响 |
| `frontend/style.css` | 309, 872-886 | 既有几何:居中 fixed banner 与 340px 下限面板在 768–855px 相交 | ⚠️ Warning → **ADJUDICATED** | 遮挡本身非本阶段引入;已由项目所有者裁定为已知偏离(A-10),不再作为缺口 |
| `frontend/style.css`, `scripts/check-05-ui-uat.py` | — | `TBD` / `FIXME` / `XXX` | — | **无命中**(债务标记门通过) |
| `frontend/app.js` | 246 → 253 | **已修复**:L-4 收敛遗留的 no-op 自动跟随(`eventsEl.scrollTop = eventsEl.scrollHeight`) | ✅ RESOLVED | quick `260925-iin` FIX 1(`11fdedb`)改为 `item.scrollIntoView({block:'nearest'})`;HEAD `grep -n 'eventsEl.scrollTop' frontend/app.js` 零命中 |

**残留假主张扫描:** 全仓搜索旧覆盖主张的字面量,`scripts/` 与 `frontend/` 零命中。命中的仅 `.planning/phases/idi-06-layout-robustness/` 下的历史记录,且均为**被引用后当场更正**的形态:`idi-06-03-PLAN.md:37` / `:212` 与 `idi-06-03-SUMMARY.md:150` 各自在原句后追加 `【更正 2026-09-22】…一句为假 ……`。历史记录里的更正方式是「保留原句 + 就地标注为假」,而非删除 —— 这使历史可审计,且不产生新的假主张。

### Human Verification Required

**无。** 本阶段的每条 must-have 都由真实浏览器中运行的断言在真实 DOM 上度量(不是 grep 存在性):三宽度 `scrollWidth/clientWidth`、三宽度 badge×banner rect 不相交、滚到底后 header 与 panel 顶部对齐、`#main-pane` 后代的滚动者集合相等、三状态命中区普查、以及**经应用自身 `renderEvent()` 驱动、探针零 `scrollTop` 赋值**的自动跟随断言。唯一的未覆盖判据(768px 遮挡)已被**裁定为已知偏离**并写入 override,不是「留给人工去测的未知」。

前版报告记的两条可选人工复核(真实 SSE 断流下同样遮挡 / sticky 表头观感)在本轮**不再作为 human 项**:前者只是复述已裁定的几何事实(且应用自身的 `showStreamBanner()` 正是真实断流调用的同一条代码路径),后者的行为已被机器断言(`header.top == panel.top`)。二者均不改变本报告裁定。

---

## 重验证披露(内容真变,非记账性刷新)

**为什么重跑复核而不是只重算指纹。** 本报告的 `covered_digest` 是 `covered_files` 的原始字节 sha256,而其中两个文件在 2026-09-22 的验证之后**确实被改动**:

- `frontend/style.css` —— 被 Phase 7(焦点环、交互态、`prefers-reduced-motion` 块)与 Phase 8 改动,最近又被 quick `260925-iin` FIX 3(commit `3e50dca`)改动:在 `:root` 围栏内**追加**两条声明(`--text-lg-plus: 20px` 作为 `--text-lg` 之后的第 8 档、`--lh-none: 1`),并把 `.collapse-indicator`(`:686`)改写为消费这两条(原为 `font-size: 20px; line-height: 1`),另有三处围栏注释同步(字号档数 7→8、行高条数 4→5、嵌入刻度数字梯)。
- `scripts/check-05-ui-uat.py` —— 被 Phase 7/8 改动,最近被 quick `260925-iin` FIX 2(commit `1560bd6`,item9 新增自动跟随断言,16→17)、FIX 4(commit `7c991d8`,修正 `:824` 附近的陈旧散文串,`item2()` 断言零改动)、FIX 5(commit `eb01a3a`,新增静态 `FOCUSABLE_SELECTOR` ↔ `:focus-visible` 枚举同步门,item 10 41→42)。

**本阶段自己的布局改动没有被 `260925-iin` 触碰。** FIX 3 的改动面逐字限定为 `:root` 围栏内的两条新令牌与 `.collapse-indicator` 的两个值声明 —— L-4 的滚动容器收敛、L-1 的 sticky 表头、L-3 的六目标换行规则、L-5 的命中区下限、`#state-badge` 的流内化,全部**逐条读源码复核在位**(见 §Required Artifacts)。故本轮是「在 HEAD 上重跑复核面」,不是「重算指纹了事」—— 所有 gate 都在 HEAD 上第一手重跑,所有结论都在 HEAD 上重新落定。

**`covered_files` 的变更(用户 2026-09-25 裁定)。** 删除了 `.planning/REQUIREMENTS.md`。理由是:该文件是**下游记账**索引表 —— `phase.complete` 会翻转它的行,里程碑收口更会**删除整个文件**(`git rm .planning/REQUIREMENTS.md`)。只要它在 `covered_files` 里,每一次阶段或里程碑收口都会**静默作废所有列出它的报告**,而理由与那些报告的结论是否成立无关。`covered_files` 的语义应是「其变更足以使本报告结论失效的输入」,需求索引表不满足该语义。该建议由 `idi-04.1-radix` 的验证代理提出并被用户采纳,适用于全部六份 v1.14 阶段报告(本报告之外的五份另行处理)。`covered_digest` 随之按**剩余文件集**(10 个)用位置参数形式重算为 `v1:sha256:ccc470b1…f9e4c0`。

**上一版指纹为何确实失效(可复算)。** 上一版记录值 `v1:sha256:c07e9994…39ae4`(11 个文件,含 `REQUIREMENTS.md`)。按同一位置参数形式在 HEAD 上重算**旧文件集**得到 `v1:sha256:9c627f73…1e950b` —— 与记录值不同,因为 `frontend/style.css`、`scripts/check-05-ui-uat.py` 与 `REQUIREMENTS.md` 三者都已变。这确认了本轮是**内容真变**,不是记账性漂移。

**本轮未改动任何其他产物。** 未改 `REQUIREMENTS.md`、`ROADMAP.md`、`idi-06-UI-SPEC.md`、`frontend/`、`scripts/`,也未触碰其他五份阶段报告;唯一的写入是本文件。**未创建 `idi-06-VALIDATION.md`** —— 本阶段没有该文件(里程碑审计 §9 已登记为 Nyquist 覆盖缺口),创建它超出本报告范围。

---

_Verified: 2026-09-25T08:52:23Z · HEAD `0b6283a`_
_Verifier: Claude (gsd-verifier)_
_重验证: 2026-09-25 —— 内容真变后的重跑复核(见上节)_
_covered_files 变更: 2026-09-25 —— 移除 `.planning/REQUIREMENTS.md`,指纹按剩余文件集重算(用户裁定)_

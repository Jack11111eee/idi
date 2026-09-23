---
phase: idi-06-layout-robustness
status: passed
verified: 2026-09-22T08:05:02Z
score: 10/10 must-haves verified
covered_files:
  - .planning/REQUIREMENTS.md
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
covered_digest: "v1:sha256:c07e99941c1b4faa69ee947096db982c3407eb32f7a8617cff319a8944039ae4"
behavior_unverified: 0
overrides_applied: 1
overrides:
  - must_have: "LAYOUT-02:窄窗口不破版 —— ≥768px 无内容遮挡"
    reason: "768–855px 下 fixed 居中横幅盖住 #doc-panel-header 的标题;几何既有且被 UI-SPEC 范围锁排除在阶段可修范围之外。经项目所有者本次会话显式选择 remediation (b)(收窄承诺 + 更正覆盖主张)后,本条登记为已知缺口,收窄为「badge 不被横幅遮挡」。"
    accepted_by: "Jack11111eee"
    accepted_at: "2026-09-22T06:43:50Z"
re_verification:
  previous_status: gaps_found
  previous_score: 8/10
  gaps_closed:
    - "LAYOUT-02 后半句:≥768px 无内容遮挡 —— 经项目所有者显式裁定 remediation (b) 登记为已知偏离(UI-SPEC A-10,idi-06-UI-SPEC.md:585),收窄为「badge 不被横幅遮挡」;本条按 override 记 PASSED (override),不再计为失败。"
    - "本阶段的验收门自身诚实:item 8 的 768px 分支声称的覆盖范围 == 它实际测量的范围 —— 假主张已删除,改写成显式「未覆盖」并携带实测数值(commit b15bd89)。"
  gaps_remaining: []
  regressions: []
advisory:
  - finding: "WR-01: `_idi06_reach` 的前提链只拒绝 `injected is None`;两个调用点传的是整数计数,`0` 不是 `None`。容器不溢出时把「滚到底」降级为 info(),但末条断言仍照跑 —— 此时末条平凡落在容器内,记 PASS。"
    category: other
    reason: "改法(要求正计数 + 不可滚即 blocked)见 idi-06-REVIEW.md WR-01;不阻塞本阶段。今日两个调用点实测注入 40 / 60 条,未触发。"
    evidence_status: "none provided(未构造出可复现的红;今日注入计数为正)"
  - finding: "WR-02: `_idi06_clearance_assert` 判定的是滚动位置而非裁切 —— 部分滚出容器的元素 `intersects` 仍为 True 而 clearance 为负,会误报。"
    category: other
    reason: "标签声称测裁切,实际测滚动位置;改法见 REVIEW WR-02。"
    evidence_status: "none provided(需要一次面板滚动才复现)"
  - finding: "WR-03: `DOC_PANEL_W_MIN_PX / _VW / _MAX_PX` 是 `frontend/style.css:228` 的硬编码镜像,无绑定。收窄 clamp 会让探针静默失去判别力。"
    category: other
    reason: "失败方向是丢覆盖而非报错。改法(从文件文本解析 clamp 三参数并断言相等)见 REVIEW WR-03。"
    evidence_status: "none provided(未实际收窄 clamp 复现)"
  - finding: "WR-04: `#doc-panel` 实测宽探针无法在其标签所指的失效模式上失败 —— 该失效模式对滚动容器结构性不可能(`min-width: 0` 的承重归因不成立)。"
    category: architectural
    reason: "产品行为正确(屏幕无破损),故为 WARNING 而非 critical;门与两处承重 CSS 注释把正确结果归因给了未做功的声明。见 idi-06-REVIEW.md WR-04。"
    evidence_status: "none provided(由测量证明,非推断;未构造可复现的红)"
  - finding: "IN-01: `_idi06_census` 的 docstring 声称 item 9 消费其返回值,实际 item 9 从不调用它;唯一调用点丢弃返回值,每次运行多跑 6 次同一份 DOM 普查。"
    category: other
    reason: "注释与代码不符(「名必须说实话」的同一条方法论);无行为影响。"
    evidence_status: "none provided"
  - finding: "IN-02: `_l2_guard_shape` 用 `text.count('@media')` 统计子串,标签却写成「== 决策(被实测推翻 ⇒ 0)」。一条无关的 `@media` 会让它 FAIL 并把修复者指向 L-2 决策记录。"
    category: other
    reason: "改法(只统计含 max-width 的 @media)见 REVIEW IN-02。当前计数 0,故为潜伏项。"
    evidence_status: "none provided"
  - finding: "IN-03: 评审新增的第三条 info 项(见 idi-06-REVIEW.md);无行为影响。"
    category: other
    reason: "见 idi-06-REVIEW.md IN-03。"
    evidence_status: "none provided"
  - finding: "A11Y-07 的普查覆盖边界:命中区普查只判定 `visible` 行,而样本只有 p1 / checking / p3。在三个样本里都 `display: none` 的控件其命中区在本阶段未被测量过。"
    category: other
    reason: "A11Y-07 的实质(紧凑控件达 24×24)在已采样状态上已证;此为覆盖边界的诚实登记,不是现行失败。"
    evidence_status: "none provided(未构造未采样状态)"
---

# Phase 6: 布局稳健性 (idi-06) Verification Report

**Phase Goal:** 布局结构常量只有一个来源;窄窗口不破版;侧栏不再是四个滚动容器的套娃;紧凑控件达到 24×24 命中区。
**Verified:** 2026-09-22T08:05:02Z
**Status:** passed
**Re-verification:** Yes — after gap closure(前一版报告为 `gaps_found` / `8/10`,commit `0bc298e`)

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | 布局结构常量只有一个来源 | ✓ VERIFIED | `--doc-panel-w: clamp(340px, 30vw, 480px)`(`frontend/style.css:228`)是文档面板宽的唯一来源,被 `#doc-panel { flex: 0 0 var(--doc-panel-w) }`(:475)消费;收起态由 `--doc-panel-w-collapsed`(:229)控制。复验确认全 `frontend/` 无 `448` 命中。`--sidebar-w` 按 D-03 不引入(该偏离已登记在 06-CONTEXT D-03 与 UI-SPEC L-1)。 |
| 2 | LAYOUT-01: `#state-badge { right: 448px }` 魔法数消除 | ✓ VERIFIED | 复验直接读源码:`#state-badge`(:699-709)只有 `padding/border-radius/background/color/font-size/font-weight/z-index` —— 无 `position`、无 `right`;badge 是 `#doc-panel-header` 内的流内元素。运行时 item 8 读 computed `position: static`、`right: auto`(PASS)。机制是流内化而非 calc()/absolute,该契约反转由 06-CONTEXT D-03 显式采纳。 |
| 3 | LAYOUT-03: `#state-badge` 不再遮挡滚动内容 | ✓ VERIFIED | badge 在正常流内(见上条),结构上不可能压住 `#doc-panel-body` 的正文;`z-index: var(--z-badge)` 在静态元素上惰性。item 8 的 `position == static` + `right == auto` 两条断言机器化该禁令。 |
| 4 | LAYOUT-04: 侧栏滚动容器套娃收敛 | ✓ VERIFIED | 复验直接读源码:`.event-list`(:594-603)与 `#annotation-list`(:944-949)均**无** `max-height`、无 `overflow-y`(原地删除)。item 9 的 DOM 普查断言面板区滚动者集合**恰为** `{#main-pane, #chat-messages, #latest-check}`(PASS,口径取「恰好」),`#ai-events` / `#annotation-list` 计算 `max-height == none`(PASS)。基线 3 个限高者降为 1。**已登记的偏离:** ROADMAP 交付物第 6 条要求连 `#latest-check` 一并删除,UI-SPEC D-11 保留它,并按 A-5(UI-SPEC :568)把 SC#3 措辞收窄为「面板区内恰好两个滚动者」;偏离有承重理由且被门机器化(30vh 计数 == 1 的保留护栏)。 |
| 5 | A11Y-07: 紧凑控件命中区达到 24×24,侧栏未重构 | ✓ VERIFIED | 复验直接读源码:`.annotation-answer summary`(:1036-1043)原地加 `min-height: 24px` / `min-width: 24px`(既有四条声明逐字保留)。item 9 的命中区普查按 DOM 遍历断言每个可见可交互元素 ≥24×24,p1/checking/p3 三样本全 PASS(未达标清单为空,本轮复跑输出「共 10 行,未达标 []」)。侧栏零重构。覆盖边界见 advisory 末条。 |
| 6 | LAYOUT-02 前半句:≥1024px 无横向溢出 | ✓ VERIFIED | item 8 在 1440 与 1024 两处的硬断言 `documentElement.scrollWidth <= clientWidth` PASS(复跑实测 1440/1440 与 1024/1024,overflow=0)。判别性探针 `#doc-panel` 实测宽 ≤ clamp 上界(1440→432.0/432.0、1024→340.0/340.0)PASS。**这两条硬断言在 gap 收口后逐字未变**(见 Key Link / 断言强度)。 |
| 7 | LAYOUT-02 后半句:≥768px 无内容遮挡 | ✓ PASSED (override) | 768–855px 下 `#stream-banner` 压住 `#doc-panel-header` 的 h1 是**实测事实**,经项目所有者本次会话显式裁定 remediation (b),登记为**已知偏离**(UI-SPEC A-10,`idi-06-UI-SPEC.md:585`)并把该承诺收窄为「badge 不被横幅遮挡」。收窄后的承诺由 item 8 的 badge × banner 不相交断言机器化(PASS)。**Override: 项目所有者显式裁定 — accepted by Jack11111eee on 2026-09-22T06:43:50Z。** |
| 8 | SC#2: badge 在每个宽度都贴在文档区右上角且不被 banner 盖住 | ✓ VERIFIED | item 8 的 badge × banner 不相交断言(:1834 起)在 768/900/1024/1280/1440 五处 PASS,且**该断言在 gap 收口后逐字未变**。badge 恒在面板标题行右端,banner 居中于视口。 |
| 9 | SC#5: `#brainstorm-view h2` 未因结构性改动而变 | ✓ VERIFIED(以实际值为准) | item 4 PASS:`#brainstorm-view h2` 计算 `font-size` == `var(--text-md)`、`color` == `var(--color-action-warning)`。ROADMAP SC#5 写的字面值「14px / `#8a6508`」是**陈旧的路线图漂移**(Phase 4/4.1 令牌迁移已换值);SC#5 的**意图**(未因结构性改动而变)成立。 |
| 10 | 本阶段验收门自身诚实(item 8 的 768px 覆盖主张 == 它实际测到的) | ✓ VERIFIED | 复验直接读源码并复跑运行时:`scripts/check-05-ui-uat.py:1931-1938` 的注释与 `:1949-1955` 的 `info()` 串均已改写 —— 现在显式写明 768px 的「无内容遮挡」承诺**未被覆盖**(「badge × banner 断言只测 badge 那一对,banner × #doc-panel-header 的 h1 不在覆盖范围内 —— 显式「未覆盖」」),并携带实测数值(h1 = 439.0–481.0 × 8–28 vs banner = 285.3–482.7 × 12–39,重叠 42×16px,相交带 768–855px),且指明其为**已知缺口**、指向 `idi-06-UI-SPEC.md §L-2(A-10 行)`。运行时 INFO 行逐字复现该措辞。**假主张已消失;门的覆盖主张现在与它实际测量的范围一致。** |

**Score:** 10/10 truths verified(0 present-behavior-unverified,1 PASSED by override)

### Deferred Items

无。Phase 7(交互状态与焦点样式)与 Phase 8(可访问性语义与键盘)均不涉及窄窗口布局或 `#stream-banner` 的定位;backlog 999.1 是 Phase 4 的两条卫生项。已裁定的 768–855px 遮挡不被任何后续阶段承接 —— 它是**已知偏离**(A-10),不是待办。

### Advisory (New Scope, Unevidenced)

| # | Finding | Category | Why Advisory |
|---|---------|----------|--------------|
| 1 | WR-01 空转 PASS:`_idi06_reach` 只拒绝 `injected is None`,整数 0 通过 | other | 潜在,非现行失败(今日注入 40/60) |
| 2 | WR-02 clearance 断言测的是滚动位置而非裁切 | other | 三样本因面板恒在 scrollTop=0 而确定;需一次滚动才复现 |
| 3 | WR-03 clamp 探针常量与 style.css 无绑定,收窄 clamp 会静默丢覆盖 | other | 未实际收窄复现 |
| 4 | WR-04 `#doc-panel` 宽探针在其标签所指失效模式上结构性不可能失败 | architectural | 产品行为正确;归因错误,未构造可复现的红 |
| 5 | IN-01 `_idi06_census` 的 docstring 与返回值无消费者,自相矛盾 | other | 注释与代码不符,无行为影响 |
| 6 | IN-02 `@media` 计数用子串匹配,标签高估了它统计的东西 | other | 当前计数 0,潜伏 |
| 7 | IN-03 评审第三条 info 项 | other | 无行为影响 |
| 8 | A11Y-07 普查只覆盖三样本中可见的控件,未采样状态下可见的控件未被测量 | other | 已采样状态上已证;覆盖边界登记 |

**Re-verification 说明:** 以上 8 条均为上一版报告 advisory 的延续(WR-04 / IN-03 为 `f9d7c33` 增量评审新增),在 gap 收口提交里**未被触碰**;它们不是本次收口的缺口,亦不阻塞。均无确定性证据(未构造可复现的红),故维持 advisory 分类,不计入 Step 9 规则 1。

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `frontend/style.css` | sticky 表头 + `min-width: 0` ×4 + 六目标 `overflow-wrap: anywhere` + 删两条内滚动 + summary 尺寸下限 | ✓ VERIFIED | 全部改动在位且被消费(复验逐条读源码确认)。**本阶段自评审基线 `d6c375c` 起零 diff**:`git diff d6c375c -- frontend/` 为空,`git show d6c375c:frontend/style.css \| shasum -a 256` 与工作树逐位相等(`0aacdc02…`)。`frontend/index.html` / `frontend/app.js` / `frontend/vendor/` 零 diff(与 UI-SPEC 的范围锁一致)。 |
| `scripts/check-05-ui-uat.py` | item 8(L-1 三条 + 三宽度诊断)+ item 9(滚动者普查 / 可达性 / 保留项护栏 / 两条普查) | ✓ VERIFIED | 断言确实执行、前提检查齐备、多数断言强(见下「断言强度复核」)。上一版的 ⚠️ PRESENT_BUT_MISLABELED 已消除:item 8 的 768px 分支现在显式声明「未覆盖」并携带实测数值,覆盖主张不再超出实际测量范围(Truth 10)。 |

**断言强度复核(不只看 exit code,复验重做):** 我逐条核了可能「在坏实现上照样 PASS」的断言,并**特别核对 gap 收口是否顺手削弱了任何断言**。结论:
- **1440 / 1024 硬断言未削弱**:`if width >= 1024: ok_true(... scrollWidth <= clientWidth ...)` 逐字保留,标签仍为「LAYOUT-02 的字面承诺:≥1024px 无横向溢出」。
- **badge × banner 不相交断言未削弱、未改标签**:仍为 `ok_true(..., not _rects_intersect(badge, banner), "不相交", ..., "L-1 的门断言几何不相交,不是「横幅不存在」")`,且 `_IDI06_BADGE_BANNER_JS`(:1630)仍**只**返回 badge 与 banner 的 rect —— 这正是「未覆盖」为真的事实基础(它没有被悄悄扩成也测 header)。
- **`#doc-panel` 上界探针与守卫形态断言**:仍在,未改。
- **滚动者普查**:按 DOM 遍历 `#main-pane` 及其全部后代算 `overflowY`,用 `==` 而非 `<=` 比较集合 —— 新增第四个滚动者会 FAIL;另有范围自检。
- **保留项护栏是双条的**:`#chat-messages overflow-y == auto` 抓「被改值」,`#latest-check` 的 `max-height: 30vh` 按**源码文本计数 == 1** 抓「被悄悄删掉」。
- **命中区普查**:`require_summary=True` 分支先断言主要对象 `<summary>` 存在且可见,读不到即 `blocked`;`visible` 一栏被用作承重判据。
- **item 8 的 badge×banner 与 sticky 断言各有前提检查**,前提不成立记 `blocked` 而非 PASS。

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `#doc-panel-header` 的 sticky | `#doc-panel { overflow-y: auto }` 的滚动行为 | sticky 的滚动容器是最近可滚祖先;header 是 `#doc-panel` 的直接 flex 子项 | ✓ WIRED | 复跑 item 8 PASS:滚到底后 `header.top == panel.top`(≤1px)。`position: sticky` 在 `frontend/style.css:513`。 |
| `--doc-panel-w` 令牌 | `#doc-panel { flex: 0 0 var(--doc-panel-w) }` | 单一来源 → 唯一消费者 | ✓ WIRED | 复跑实测 1440→432.0、1024→340.0、768→340.0,与 clamp 解析值逐位相等。 |
| `.annotation-answer summary` 的 `min-height/min-width: 24px` | item 9 的命中区普查断言 | 运行时 `getBoundingClientRect()` 逐元素读数 | ✓ WIRED | summary 实测 ≥24px;普查未达标清单为空。 |
| `#stream-banner` 的 fixed 定位 | `#doc-panel-header` 的 h1(768–855px) | 两者都在同一 0–39px 带内,banner `z-index: 20` 高于 header 的 `z-index: auto` | ⚠️ ADJUDICATED (override) | 几何仍相交(style.css 本阶段零 diff,故机制未变)。**这不是本阶段的独立缺口**:它是 Truth 7(已 override)的直接因果链,已随 LAYOUT-02 的 768px 承诺收窄一并裁定,登记于 UI-SPEC A-10。复验**不把它重新提起为 blocker**。 |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| item 8 badge/banner 几何 | `getBoundingClientRect()` on `#state-badge` / `#stream-banner` | 真实 DOM;banner 由应用自身 `showStreamBanner()` 置为可见(不手工拼 DOM) | Yes | ✓ FLOWING |
| item 9 滚动者普查 | `getComputedStyle(el).overflowY` 遍历 `#main-pane` 后代 | 真实 DOM | Yes | ✓ FLOWING |
| item 9 命中区普查 | `getBoundingClientRect()` on 交互元素 | 真实 DOM;`<summary>` 经应用自身 `renderAnnotations()` 造出 | Yes | ✓ FLOWING |
| item 9 可达性 | `scrollHeight` / `clientHeight` / `scrollTop` + 末条 rect | 真实 DOM;内容经应用自身 `renderEvent()` / `renderMarkdown()` 注入 | Yes | ✓ FLOWING |
| 768px 遮挡判据 | — | **无数据源:该判据没有任何探针** | No | ✗ DISCONNECTED — **已登记为已知缺口(A-10),按 override 裁定,不再是待修项** |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| item 8 全绿(13 条断言) | `.venv/bin/python scripts/check-05-ui-uat.py --item 8` | `item 8: PASS (13 条断言,0 FAIL,0 BLOCKED)`,exit=0 | ✓ PASS |
| item 8 的 768px 诊断陈述实测真相 | 同上,过滤 `L-2 @768` | 运行时 INFO 行逐字输出「该承诺未被覆盖……显式「未覆盖」……h1 = 439.0–481.0 × 8–28 vs banner = 285.3–482.7 × 12–39,重叠 42×16px,相交带 768–855px……收窄已登记在 idi-06-UI-SPEC.md §L-2(A-10 行)」 | ✓ PASS |
| item 9 全绿(16 条断言) | `.venv/bin/python scripts/check-05-ui-uat.py --item 9` | `item 9: PASS (16 条断言,0 FAIL,0 BLOCKED)`,exit=0;命中区普查「共 10 行,未达标 []」 | ✓ PASS |
| 令牌门 | `bash scripts/check-01-token-conformance.sh` | `PASS`,exit=0 | ✓ PASS |
| 对比度门 | `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`,exit=0 | ✓ PASS |
| hidden 唯一性 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS`,exit=0 | ✓ PASS |
| `!important` 计数 | `bash scripts/check-04-important-count.sh` | `PASS`,exit=0 | ✓ PASS |
| idi-05 校验门 | `.venv/bin/python scripts/check-06-idi05-validation.py` | g1–g6 全 PASS,exit=0 | ✓ PASS |
| 债务标记门(改动文件) | `grep -nE "TBD\|FIXME\|XXX" frontend/style.css scripts/check-05-ui-uat.py` | 零命中 | ✓ PASS |

**关于被裁定的 768px 遮挡:** 复验**未**重跑遮挡探针来「再证伪一次」—— 该事实已被前版报告独立复现两次(p1 / p3 两样本、`elementFromPoint` 四点采样、边界扫描 855/856),并在本次收口中被项目所有者显式裁定为已知偏离。重跑只会复述已裁定的事实。几何未变这一前提由 `frontend/style.css` 与评审基线 `d6c375c` 逐字节相同来保证。

### Probe Execution

无 `scripts/*/tests/probe-*.sh` 约定探针,PLAN/SUMMARY 亦未声明探针路径;本阶段的「探针」即 check-05 的 item 8 / item 9,已在上表实际运行。

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| LAYOUT-01 | 06-01, 06-04 | `#state-badge { right: 448px }` 魔法数消除 | ✓ SATISFIED | 见 Truth 2;实质达成(流内化),机制偏离已由 D-03 显式登记 |
| LAYOUT-02 | 06-02, 06-03, 06-04 | 窄窗口不破版:≥1024px 无横向溢出,**≥768px 无内容遮挡** | ✓ SATISFIED (override) | 前半句 ✓ VERIFIED(Truth 6);后半句的 768–855px 子段为**已裁定的已知偏离**(A-10),承诺收窄为「badge 不被横幅遮挡」并机器化(Truth 7/8)。**Override: 项目所有者显式裁定 remediation (b)。** |
| LAYOUT-03 | 06-01, 06-04 | `#state-badge` 不再遮挡滚动内容 | ✓ SATISFIED | 见 Truth 3 |
| LAYOUT-04 | 06-02, 06-04 | 侧栏滚动容器套娃收敛 | ✓ SATISFIED | 见 Truth 4;SC#3 措辞收窄已按 A-5 登记 |
| A11Y-07 | 06-03, 06-04 | 紧凑控件达到 24×24 命中区 | ✓ SATISFIED | 见 Truth 5;覆盖边界见 advisory 末条 |

**Orphaned requirements:** 无。四个计划的 `requirements:` 字段合计覆盖 `LAYOUT-01/02/03/04 + A11Y-07`,与 ROADMAP Phase 6 的 Requirements 行逐字一致。`06-04`(gap-closure)声明全部五个 ID。

**REQUIREMENTS.md 状态说明:** `.planning/REQUIREMENTS.md:144-149` 现把这五个 ID 全标 `Complete`。这与本报告的结论**一致**(LAYOUT-02 现按 override 记 SATISFIED),但该表的更新来自 `phase.complete` 流程而非本复验;按任务约束,复验**不编辑** `REQUIREMENTS.md` / `ROADMAP.md`(编辑会作废 `covered_digest`)。`ROADMAP.md` 在本轮收口期间的唯一改动是 Plans 段登记 `idi-06-04`(书签性记录),其 Gates 行与承诺文本逐字未动 —— 即 A-10 声明的「路线图承诺不改」成立。

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `scripts/check-05-ui-uat.py` | 1931-1938, 1949-1955 | **已修复**:原「已由 badge × banner 不相交断言覆盖」的假主张 | ✅ RESOLVED | commit `b15bd89` 改写为显式「未覆盖」+ 实测数值 + A-10 指向;复验逐字确认旧措辞在 harness 与运行时输出中均已消失 |
| `scripts/check-05-ui-uat.py` | 2134 / 2158-2176 / 2186-2192 / 1588-1595 | 空转 PASS / 测错对象 / 常量无绑定 | ⚠️ Warning | 见 advisory 1-3;均未在今日触发 |
| `frontend/style.css` | 228, 709-723 | 既有几何:居中 fixed banner 与 340px 下限面板在 768–855px 相交 | ⚠️ Warning → **ADJUDICATED** | 遮挡本身非本阶段引入;已由项目所有者裁定为已知偏离(A-10),不再作为缺口 |
| `frontend/style.css`, `scripts/check-05-ui-uat.py` | — | `TBD` / `FIXME` / `XXX` | — | **无命中**(债务标记门通过) |

**残留假主张扫描:** 全仓搜索旧措辞「已由 badge × banner 不相交断言覆盖」,命中仅三处,且均为**被引用后当场更正**的记录:`idi-06-03-PLAN.md:37` / `:212` 与 `idi-06-03-SUMMARY.md:150` 各自在原句后追加 `【更正 2026-09-22】上文「已由 badge × banner 断言覆盖」一句为假 ……`;`idi-06-VERIFICATION.md`(前版报告)在 gaps 中引用它以描述缺陷。**harness 源码与运行时输出中零残留。** 历史记录里的更正方式是「保留原句 + 就地标注为假」,而非删除 —— 这使历史可审计,且不产生新的假主张。

### Human Verification Required

**无。** 本阶段的每条 must-have 都由真实浏览器中运行的断言在真实 DOM 上度量(不是 grep 存在性):三宽度 `scrollWidth/clientWidth`、五宽度 badge×banner rect 不相交、滚到底后 header 与 panel 顶部对齐、`#main-pane` 后代的滚动者集合相等、三状态命中区普查。唯一的未覆盖判据(768px 遮挡)已被**裁定为已知偏离**并写入 override,不是「留给人工去测的未知」。

前版报告记的两条可选人工复核(真实 SSE 断流下同样遮挡 / sticky 表头观感)在本轮**不再作为 human 项**:前者只是复述已裁定的几何事实(且应用自身的 `showStreamBanner()` 正是真实断流调用的同一条代码路径),后者的行为已被机器断言(`header.top == panel.top`)。二者均不改变本报告裁定。

## 复验裁定(两条 gap 的独立核验)

我按任务要求,把「两条 gap 已关闭」当作**待验证的输入**,逐条独立复核,不采信 orchestrator 的转述。

### Gap 1 — LAYOUT-02 的 768px 遮挡 → 已裁定为已知偏离(override 适用)

- **UI-SPEC A-10 行确实存在**:`idi-06-UI-SPEC.md:585`,内容与 override 一致(既有几何 / 范围锁 / 实测数值 / 跟随 A-5 先例 / `REQUIREMENTS.md` `ROADMAP.md` 不改)。
- **§L-2 判据表已就地注解**:`:194-199` 新增注解,明确「本阶段**只测量过 `badge × banner` 这一对**」且「「表头 × 正文」与「按钮 × 视口」两对在本阶段从未被测量过一次」,并写明「本表行未被删除、未被重排」。这是前版 gap 要求 (b) 中「把从未测过的两对一并说明」的落实。
- **几何未变的前提成立**:`frontend/style.css` 与评审基线 `d6c375c` 逐字节相同(`0aacdc02…`),`git diff d6c375c -- frontend/` 为空;`#stream-banner`(:709-723)与 `--doc-panel-w`(:224-227)未被触碰。遮挡是**既有几何**,不是本阶段引入,故不构成回归。
- **裁定来源是用户显式选择**,不是执行器单方:override 的 `accepted_by` / `accepted_at` 按任务要求逐字保留,`overrides_applied` 由 0 置 1。

### Gap 2 — 门的覆盖主张不诚实 → 已修复(逐字核验)

- **源码**:`scripts/check-05-ui-uat.py:1931-1938` 的注释现写「而**该承诺未被覆盖** …… 这里是显式「未覆盖」」并附实测数值;`:1949-1955` 的 `info()` 串同义。**旧措辞已不存在。**
- **运行时**:复跑 `--item 8` 实测打印上述「未覆盖」措辞(见 Behavioral Spot-Checks 第 2 行)。
- **未削弱**:1440/1024 硬断言与 `:1834` 的 badge×banner 断言逐字保留,标签未改;`_IDI06_BADGE_BANNER_JS` 仍只返回 badge 与 banner(故「未覆盖」为真,而非被悄悄扩测后自证)。
- **历史记录**:`idi-06-03-PLAN.md:37` / `:212` 与 `idi-06-03-SUMMARY.md:150` 各就原地标注为假,附实测数值与 A-10 指向。
- **非装饰性**:改写是**实质的**,不是换个说法继续报 PASS —— 768px 分支仍是只读 `info()`,且明确写「既未满足、也未断言」。唯一可挑之处是该 `info()` 串把实测数值**硬编码**为静态文本(几何若变会陈旧);但它声明的是「已知缺口」而非「已覆盖」,不构成覆盖主张,故不足以重新提起为缺口。

### 与「门是否在报它不交付的覆盖」相关的独立复查

我另外确认:item 8 本轮仍报 `PASS (13 条断言)`,但它的**标签集合**现在与它**实际测量的集合**一一对应 —— badge×banner 断言标的是 badge×banner,三宽度溢出断言标的是溢出,768px 那一支不再冒充「无内容遮挡」的覆盖。上一版 `gaps[1]`(门自身诚实性)据此关闭。

### 关于「不得凭空制造新失败」

768–855px 的遮挡是**已裁定**的偏离。我**不**把它重提为 blocker,也**不**把它记回 gaps;它作为 override 记录在 frontmatter,并在 Key Link 表中以 `⚠️ ADJUDICATED (override)` 如实呈现,供下一个读者看见,而非被抹去。

---

_Verified: 2026-09-22T08:05:02Z_
_Verifier: Claude (gsd-verifier)_
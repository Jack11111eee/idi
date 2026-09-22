---
phase: idi-06-layout-robustness
status: gaps_found
verified: 2026-09-22T06:09:33Z
score: 8/10 must-haves verified
covered_files:
  - .planning/REQUIREMENTS.md
  - .planning/phases/idi-06-layout-robustness/idi-06-01-PLAN.md
  - .planning/phases/idi-06-layout-robustness/idi-06-01-SUMMARY.md
  - .planning/phases/idi-06-layout-robustness/idi-06-02-PLAN.md
  - .planning/phases/idi-06-layout-robustness/idi-06-02-SUMMARY.md
  - .planning/phases/idi-06-layout-robustness/idi-06-03-PLAN.md
  - .planning/phases/idi-06-layout-robustness/idi-06-03-SUMMARY.md
  - frontend/style.css
  - scripts/check-05-ui-uat.py
covered_digest: "v1:sha256:c22afc1518c2b84ff59c4955035cc40fa5b587ed05f3b3a83411fc48fb23001e"
behavior_unverified: 0
overrides_applied: 0
overrides:
  - must_have: "LAYOUT-02:窄窗口不破版 —— ≥768px 无内容遮挡"
    reason: "768–855px 下 fixed 居中横幅盖住 #doc-panel-header 的标题;几何既有且被 UI-SPEC 范围锁(#stream-banner 声明不得触碰 / --doc-panel-w 值由用户裁决)排除在阶段可修范围之外。经项目所有者本次会话显式选择 remediation (b)(收窄承诺 + 更正覆盖主张)后,本条登记为已知缺口,收窄为「badge 不被横幅遮挡」。"
    accepted_by: "Jack11111eee"
    accepted_at: "2026-09-22T06:43:50Z"
re_verification:
  previous_status: none
  previous_score: 0/0
  gaps_closed: []
  gaps_remaining: []
  regressions: []
gaps:
  - truth: "LAYOUT-02 后半句:≥768px 无内容遮挡(窗口从 1440 收到 768,无内容被遮挡)"
    status: failed
    reason: "在恰好 768px 视口下,`#stream-banner`(position: fixed, z-index 20,不透明 rgb(255,247,194))完整压住 `#doc-panel-header h1`(文本「文档区」)。实测 h1 = 439.0–481.0 × 8–28,banner = 285.3–482.7 × 12–39:水平 42/42px 全覆盖、垂直 16/20px 覆盖。四次 elementFromPoint 采样(左缘中点 / 中心 / 右缘中点 / 左下角)全部返回 `#stream-banner`,即标题在整个 42×20 盒内不可命中、不可见。相交带宽为 768 ≤ vw ≤ 855(856 起不相交),即 LAYOUT-02 承诺区间 ≥768px 的整个 768–855 子段都命中。UI-SPEC §L-2 的判据表把该承诺写成「关键元素 rect 两两不相交(badge × banner、表头 × 正文、按钮 × 视口)」——「表头」是三个被点名的关键元素之一,而 banner 也是关键元素,故 banner ∩ 表头 正落在「两两不相交」之内。计划的 L-2 决策只测了横向溢出半边(SUMMARY 03 的「测量决策记录」只有 scrollWidth/clientWidth 与面板宽两列),据此登记「被实测推翻」,遮挡半边从未测量。"
    artifacts:
      - path: "scripts/check-05-ui-uat.py"
        issue: "item 8 的 768px 分支只记 info(),其注释(:1932-1933)与 INFO 串(:1945-1946)声称该承诺「已由 badge × banner 不相交断言覆盖」;该断言(:1834)只测 #state-badge,而 badge 实测 639.0–739.9 与 banner 285.3–482.7 确实不相交,故它在真实遮挡存在的宽度上报 PASS。UI-SPEC §L-2 点名的三对里,「表头 × 正文」与「按钮 × 视口」在全阶段(harness / SUMMARY / 任何探针)从未被测量过一次。"
      - path: "frontend/style.css"
        issue: "几何本身是既有的(`#stream-banner` :709-723 与 `--doc-panel-w: clamp(340px, 30vw, 480px)` :228 均未在本阶段改动;`frontend/index.html` 本阶段零 diff)。本阶段未引入该遮挡,但把它声明为已满足。"
    missing:
      - "二选一(CR-01 的两个选项,不得两条都不做):(a) 真正断言该判据 —— 把 `#doc-panel-header` 与它的 h1 的 rect 加进 `_IDI06_BADGE_BANNER_JS`(:1630),并在 768px 加一条 `not _rects_intersect(banner, geo['docHeader'])` 断言(它今天会 FAIL,那正是正确的信号;底层修复须先解决契约冲突,见 gaps 第 2 条);或 (b) 明确声明该对不在 LAYOUT-02 范围内 —— 用实测数值替换 :1932-1933 与 :1945-1946 两处措辞,写成显式「未覆盖」,并按本项目既有的 A-5 先例(UI-SPEC :568)把范围收窄登记进 UI-SPEC §L-2 与验证记录。**当前措辞把事实说反了**,比不写更糟:它让下一个读者不再去看。"
  - truth: "本阶段的验收门自身诚实:item 8 的 768px 分支声称的覆盖范围 == 它实际测量的范围"
    status: failed
    reason: "见上条 artifacts 第 1 项。这是一条独立于几何的缺口:几何是既有的,而「声称已覆盖」是本阶段新增的(`git diff` 确认 :1932-1933 两行与 :1945-1946 的措辞均为本阶段新增)。项目的既定纪律是「不看就报 PASS 的门比没有门更糟」;本项正是该纪律的反例,且与本阶段自登记的威胁 T-idi-06-04(假 PASS / 空转断言,idi-06-01-PLAN.md:412)同型。"
    artifacts:
      - path: "scripts/check-05-ui-uat.py"
        issue: "断言 :1834 的标签是「#state-badge 与 #stream-banner 不相交」,覆盖主张却写在 LAYOUT-02「无内容遮挡」的名下。"
    missing:
      - "把覆盖主张收窄到断言实际测到的东西,或补上缺失的断言(同上条 missing)。"
advisory:
  - finding: "WR-01: `_idi06_reach`(:2116-2167)的前提链只拒绝 `injected is None`;两个调用点传的是整数计数,`0` 不是 `None`。容器不溢出时 :2151 把「滚到底」降级为 info(),但 :2161 的末条断言仍照跑 —— 此时末条平凡落在容器内,记 PASS。今日两个调用点实测注入 40 / 60 条,故未触发;是潜在空转 PASS,不是现行失败。"
    category: other
    reason: "改法(要求正计数 + 不可滚即 blocked)见 idi-06-REVIEW.md WR-01;不阻塞本阶段。"
    evidence_status: "none provided(未构造出可复现的红;今日注入计数为正)"
  - finding: "WR-02: `_idi06_clearance_assert`(:2186-2192)判定的是滚动位置而非裁切 —— 部分滚出容器的元素 `intersects` 仍为 True 而 clearance 为负,会误报。今日三样本因 `enter_project` 重载页面、面板恒在 scrollTop=0 而确定;`#btn-authorize × #doc-panel = -122.6px` 只差约 123px 就会翻进判定集。"
    category: other
    reason: "标签声称测裁切,实际测滚动位置;改法见 REVIEW WR-02。"
    evidence_status: "none provided(需要一次面板滚动才复现)"
  - finding: "WR-03: `DOC_PANEL_W_MIN_PX / _VW / _MAX_PX`(:1588-1595)是 `frontend/style.css:228` 的硬编码镜像,无绑定。收窄 clamp(如 `clamp(300px, 24vw, 400px)`)会让探针静默失去判别力(1440 下仍拿 432 当上界,而面板只有 345.6)。"
    category: other
    reason: "同 T-idi-06-04 一类:失败方向是丢覆盖而非报错。改法(从文件文本解析 clamp 三参数并断言相等)见 REVIEW WR-03。"
    evidence_status: "none provided(未实际收窄 clamp 复现)"
  - finding: "IN-01: `_idi06_census`(:1738-1760)的 docstring 声称 item 9 消费其返回值,实际 item 9 从不调用它(:2177 / :2211 各自 evaluate 同一份普查),唯一调用点 :1988 丢弃返回值;每次运行因此多跑 6 次同一份 DOM 普查。"
    category: other
    reason: "注释与代码不符(「名必须说实话」的同一条方法论);无行为影响。"
    evidence_status: "none provided"
  - finding: "IN-02: `_l2_guard_shape`(:1602-1630)用 `text.count('@media')` 统计子串,标签却写成「== 决策(被实测推翻 ⇒ 0)」。一条无关的 `@media (prefers-reduced-motion: reduce)` 或打印样式表会让它 FAIL 并把修复者指向 L-2 决策记录。当前计数 0,故为潜伏项。"
    category: other
    reason: "改法(只统计含 max-width 的 @media)见 REVIEW IN-02。"
    evidence_status: "none provided"
  - finding: "A11Y-07 的普查覆盖边界:命中区普查只判定 `visible` 行,而样本只有 p1 / checking / p3。在三个样本里都 `display: none` 的控件(`#confirm-word-input` / `#btn-permission-allow|deny` / `#btn-confirm-authorize|cancel` / `#btn-tier-loose|strict` / `#btn-mission-close` / `#cli-recheck-btn` / `#btn-start-writing` / `#btn-annotate` / `#btn-plain-ask` / `#check-switcher` / `#btn-continue-check|repair` / `#btn-divergence` / `#btn-approve-draft`)的命中区在本阶段**未被测量过**。若其中某个只在未采样状态下可见的控件 < 24×24,门不会发现。"
    category: other
    reason: "A11Y-07 的实质(紧凑控件达 24×24)在已采样状态上已证;此为覆盖边界的诚实登记,不是现行失败。"
    evidence_status: "none provided(未构造未采样状态)"
human_verification_note: "状态为 gaps_found(Step 9 规则 1 优先),故不写 human_verification 列表。两处可人工复核但不阻塞:(1) 真实 SSE 断流(而非经应用自身 showStreamBanner 构造)在 768px 下同样遮挡;(2) sticky 表头背景 `var(--color-surface)` 与 `border-radius: 0` 的视觉观感。"
---

# Phase 6: 布局稳健性 (idi-06) Verification Report

**Phase Goal:** 布局结构常量只有一个来源;窄窗口不破版;侧栏不再是四个滚动容器的套娃;紧凑控件达到 24×24 命中区。
**Verified:** 2026-09-22T06:09:33Z
**Status:** gaps_found
**Re-verification:** No — initial verification(本阶段此前无 VERIFICATION.md)

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | 布局结构常量只有一个来源 | ✓ VERIFIED | `--doc-panel-w: clamp(340px, 30vw, 480px)`(`frontend/style.css:228`)是文档面板宽的唯一来源,被 `#doc-panel { flex: 0 0 var(--doc-panel-w) }`(:475)消费;收起态由 `--doc-panel-w-collapsed`(:229)控制。`--sidebar-w` 按 D-03 不引入(calc() 版本被撤销),该偏离已登记在 06-CONTEXT D-03 与 UI-SPEC L-1。全 `frontend/` 无 `448` 命中。 |
| 2 | LAYOUT-01: `#state-badge { right: 448px }` 魔法数消除 | ✓ VERIFIED | `#state-badge`(:699-709)无 `position`、无 `right`;badge 是 `#doc-panel-header`(`frontend/index.html:84-90`)内的流内元素。运行时实测 computed `position: static`、`right: auto`(item 8 PASS),我的探针同样读到 `pos=static`。机制不是 calc()/absolute 而是流内化 —— 该契约反转由 06-CONTEXT D-03 显式采纳并撤销 `04-UI-SPEC.md` Q6,UI-SPEC :108 登记「LAYOUT-01 的实质(魔法数消除)已达成」。 |
| 3 | LAYOUT-03: `#state-badge` 不再遮挡滚动内容 | ✓ VERIFIED | badge 在正常流内(见上条),结构上不可能压住 `#doc-panel-body` 的正文;`z-index: var(--z-badge)` 在静态元素上惰性。实测 768/900/1024/1440 四处 badge 均落在面板标题行右端(x 639.0–739.9 @768),不与任何正文相交。UI-SPEC :109 与 :671 的禁令(不得改回 fixed)由 item 8 的 `position == static` + `right == auto` 两条断言机器化。 |
| 4 | LAYOUT-04: 侧栏滚动容器套娃收敛 | ✓ VERIFIED | `.event-list` 的 `max-height: 55vh` / `overflow-y` 与 `#annotation-list` 的 `max-height: 32vh` / `overflow-y` 原地删除(见本阶段 diff);item 9 的 DOM 普查断言面板区滚动者集合**恰为** `{#main-pane, #chat-messages, #latest-check}`(PASS,口径取「恰好」),`#ai-events` / `#annotation-list` 计算 `max-height == none`(PASS)。基线 3 个限高者(55vh/32vh/30vh)降为 1。**已登记的偏离:** ROADMAP 交付物第 6 条要求连 `#latest-check` 一并删除,UI-SPEC D-11 保留它(去掉会把裁决按钮推出视口),并按 A-5(UI-SPEC :568)把 SC#3 措辞收窄为「面板区内恰好两个滚动者」;偏离有承重理由且被门机器化(30vh 计数 == 1 的保留护栏)。 |
| 5 | A11Y-07: 紧凑控件命中区达到 24×24,侧栏未重构 | ✓ VERIFIED | `.annotation-answer summary` 原地加 `min-height: 24px` / `min-width: 24px`(本阶段 diff),实测由 722×17 抬到 **722×24**(item 8 / item 9 原始行)。item 9 的命中区普查按 DOM 遍历断言每个可见可交互元素 ≥24×24,p1/checking/p3 三样本全 PASS(未达标清单为空)。需求点名的裁决按钮本来就达标(实测 178×40,SUMMARY 03 的 L-6 决策行)。侧栏零重构(diff 只加两条尺寸声明)。覆盖边界见 advisory 末条。 |
| 6 | LAYOUT-02 前半句:≥1024px 无横向溢出 | ✓ VERIFIED | item 8 在 1440 与 1024 两处的硬断言 `documentElement.scrollWidth <= clientWidth` PASS;我的独立探针在两处同样读到 1440/1440 与 1024/1024。判别性探针 `#doc-panel` 实测宽 ≤ clamp 上界(1440→432.0/432.0、1024→340.0/340.0)PASS。 |
| 7 | LAYOUT-02 后半句:≥768px 无内容遮挡 | ✗ FAILED | **见下节 CR-01 裁定。** 768px 下 `#stream-banner` 完整压住 `#doc-panel-header h1`:rect 相交 42×16px(elementFromPoint 四点全返回 `#stream-banner`);相交带 768–855px。UI-SPEC §L-2 点名的三对判据里两对从未被测量。 |
| 8 | SC#2: badge 在每个宽度都贴在文档区右上角且不被 banner 盖住 | ✓ VERIFIED | 我的独立探针在 768/900/1024/1280/1440 五处实测 `badge × banner = False`(badge 恒在面板标题行右端,banner 居中于视口,两者不相交)。CONTEXT D-03 的解析(相交条件 ≈ 视口 < 490px)与实测一致。注意:本条成立**不蕴含** LAYOUT-02 的遮挡半句成立 —— 被遮挡的是标题 h1,不是 badge。 |
| 9 | SC#5: `#brainstorm-view h2` 未因结构性改动而变 | ✓ VERIFIED(以实际值为准) | item 4 PASS:`#brainstorm-view h2` 计算 `font-size` == `var(--text-md)`、`color` == `var(--color-action-warning)`(实测 rgb(79,52,34))。ROADMAP SC#5 写的字面值「14px / `#8a6508`」是**陈旧的路线图漂移**:Phase 4/4.1 的令牌迁移已把它们换成 16px / amber-12,且在本阶段开始(`86f9e81`)时就已经是这两个值 —— 本阶段前后逐字未变,SC#5 的**意图**(未因结构性改动而变)成立,字面数值不可满足。 |
| 10 | 本阶段验收门自身诚实(item 8 的 768px 覆盖主张 == 它实际测到的) | ✗ FAILED | `scripts/check-05-ui-uat.py:1932-1933` 与 `:1945-1946` 声称 768px 的「无内容遮挡」承诺「已由 badge × banner 不相交断言覆盖」;该断言(`:1834`)只测 `#state-badge`,在真实遮挡存在的宽度上 PASS。措辞为本阶段新增。 |

**Score:** 8/10 truths verified(0 present-behavior-unverified)

### Deferred Items

无。Phase 7(交互状态与焦点样式)与 Phase 8(可访问性语义与键盘)均不涉及窄窗口布局或 `#stream-banner` 的定位;backlog 999.1 是 Phase 4 的两条卫生项。缺口 1/2 不被任何后续阶段承接。

### Advisory (New Scope, Unevidenced)

| # | Finding | Category | Why Advisory |
|---|---------|----------|--------------|
| 1 | WR-01 空转 PASS:`_idi06_reach` 只拒绝 `injected is None`,整数 0 通过 | other | 潜在,非现行失败(今日注入 40/60) |
| 2 | WR-02 clearance 断言测的是滚动位置而非裁切 | other | 三样本因面板恒在 scrollTop=0 而确定;需一次滚动才复现 |
| 3 | WR-03 clamp 探针常量与 style.css 无绑定,收窄 clamp 会静默丢覆盖 | other | 未实际收窄复现 |
| 4 | IN-01 `_idi06_census` 的 docstring 与返回值无消费者,自相矛盾 | other | 注释与代码不符,无行为影响 |
| 5 | IN-02 `@media` 计数用子串匹配,标签高估了它统计的东西 | other | 当前计数 0,潜伏 |
| 6 | A11Y-07 普查只覆盖三样本中可见的控件,未采样状态下可见的控件未被测量 | other | 已采样状态上已证;覆盖边界登记 |

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `frontend/style.css` | sticky 表头 + `min-width: 0` ×2 + 六目标 `overflow-wrap: anywhere` + 删两条内滚动 + summary 尺寸下限 | ✓ VERIFIED | 全部改动在位且被消费;本阶段 diff 仅此文件与 check-05;`frontend/index.html` / `frontend/app.js` / `vendor/` 零 diff(与 UI-SPEC 的范围锁一致) |
| `scripts/check-05-ui-uat.py` | item 8(L-1 三条 + 三宽度诊断)+ item 9(滚动者普查 / 可达性 / 保留项护栏 / 两条普查) | ⚠️ PRESENT_BUT_MISLABELED | 断言确实执行、前提检查齐备、多数断言强(见下「断言强度」);但 item 8 的 768px 分支对 LAYOUT-02 遮挡半句做出**超出实际测量范围**的覆盖主张(gaps 第 2 条) |

**断言强度复核(不只看 exit code):** 我逐条核了可能「在坏实现上照样 PASS」的断言。结论是**多数是强断言**,除 gaps/advisory 所列外未发现第二个假 PASS:
- 滚动者普查(`_IDI06_SCROLLERS_JS` :2048-2063)按 DOM 遍历 `#main-pane` 及其全部后代算 `overflowY`,并用 `==` 而非 `<=` 比较集合 —— 新增第四个滚动者会 FAIL;另有一条「实测结果里没有 `#main-pane` ⇒ blocked」的范围自检。
- 保留项护栏是双条的:`#chat-messages overflow-y == auto` 抓「被改值」,`#latest-check` 的 `max-height: 30vh` 按**源码文本计数 == 1** 抓「被悄悄删掉」(计算样式对 `vh` 返回 px 用值,断言 `== "30vh"` 会恒 FAIL —— 该陷阱在注释里被显式记录)。
- 命中区普查的 `require_summary=True` 分支先断言主要对象 `<summary>` 存在且可见,读不到即 `blocked`(复刻 item7 `all(w != "700")` 对 `None` 恒真的陷阱并显式记名)。
- `visible` 一栏被用作承重判据(被祖先藏住的元素 rect 全零,不得读成「命中区不足」)。
- item 8 的 badge×banner 与 sticky 断言各有前提检查(元素可见且 rect 非全零 / 容器真的可滚),前提不成立记 `blocked` 而非 PASS。

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `#doc-panel-header` 的 sticky | `#doc-panel { overflow-y: auto }` 的滚动行为 | sticky 的滚动容器是最近可滚祖先;header 是 `#doc-panel` 的直接 flex 子项 | ✓ WIRED | item 8 PASS:滚到底后 `header.top == panel.top`(≤1px),header 仍在面板可视区内;我的探针读到 `pos=sticky`、header 恒在面板顶部 0–34/36px |
| `--doc-panel-w` 令牌 | `#doc-panel { flex: 0 0 var(--doc-panel-w) }` | 单一来源 → 唯一消费者 | ✓ WIRED | 实测 1440→432.0、1024→340.0、768→340.0,与 clamp 解析值逐位相等 |
| `.annotation-answer summary` 的 `min-height/min-width: 24px` | item 9 的命中区普查断言 | 运行时 `getBoundingClientRect()` 逐元素读数 | ✓ WIRED | summary 实测 722×24,普查未达标清单为空 |
| `#stream-banner` 的 fixed 定位 | `#doc-panel-header` 的 h1(768–855px) | 两者都在同一 0–39px 带内,banner `z-index: 20` 高于 header 的 `z-index: auto` | ✗ BROKEN | 见 CR-01;此链是 LAYOUT-02 遮挡半句失败的直接机制 |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| item 8 badge/banner 几何 | `getBoundingClientRect()` on `#state-badge` / `#stream-banner` | 真实 DOM;banner 由应用自身 `showStreamBanner()` 置为可见(不手工拼 DOM) | Yes | ✓ FLOWING |
| item 9 滚动者普查 | `getComputedStyle(el).overflowY` 遍历 `#main-pane` 后代 | 真实 DOM | Yes | ✓ FLOWING |
| item 9 命中区普查 | `getBoundingClientRect()` on 交互元素 | 真实 DOM;`<summary>` 经应用自身 `renderAnnotations()` 造出 | Yes | ✓ FLOWING |
| item 9 可达性 | `scrollHeight` / `clientHeight` / `scrollTop` + 末条 rect | 真实 DOM;内容经应用自身 `renderEvent()` / `renderMarkdown()` 注入 | Yes | ✓ FLOWING |
| 768px 遮挡判据 | — | **无数据源:该判据没有任何探针** | No | ✗ DISCONNECTED |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| item 8 全绿(13 条断言) | `.venv/bin/python scripts/check-05-ui-uat.py --item 8` | `item 8: PASS (13 条断言,0 FAIL,0 BLOCKED)`,exit=0 | ✓ PASS |
| item 9 全绿(16 条断言) | `.venv/bin/python scripts/check-05-ui-uat.py --item 9` | `item 9: PASS (16 条断言,0 FAIL,0 BLOCKED)`,exit=0 | ✓ PASS |
| 既有项无回归 | `--item smoke,1,2,3,4,6,7` | smoke 9 / 1 45 / 2 5 / 3 17 / 4 65 / 6 6 / 7 38 条断言,全 PASS,exit=0 | ✓ PASS |
| 令牌门 | `bash scripts/check-01-token-conformance.sh` | `PASS`,exit=0 | ✓ PASS |
| 对比度门 | `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`,exit=0 | ✓ PASS |
| hidden 唯一性 / `!important` 计数 | `check-03` / `check-04` | 均 `PASS`,exit=0 | ✓ PASS |
| idi-05 校验门 | `.venv/bin/python scripts/check-06-idi05-validation.py` | g1–g6 全 PASS,exit=0 | ✓ PASS |
| **768px 遮挡(独立探针,复用 harness 自身的状态构造)** | `.venv/bin/python /tmp/idi06_cr01_probe.py` | p1 与 p3 两样本 @768 均 `h1 × banner = True (42.0 × 16.0px)`、`header × banner = True`、`badge × banner = False`;@900/1024/1440 三者皆 False | ✗ FAIL |
| **绘制顺序(决定性)** | `.venv/bin/python /tmp/idi06_paint_probe.py`(`document.elementFromPoint` 四点采样) | @768:左缘中点 / 中心 / 右缘中点 / 左下角 **全部返回 `#stream-banner`**(`is h1/child: False`);@1024 四点全部返回 `h1` | ✗ FAIL |
| **相交边界扫描** | `.venv/bin/python /tmp/idi06_boundary_probe.py` | 768→True、800→True、840→True、850→True、855→True、**856→False**、880/1024/1280→False(与解析解 vw < 855.3 一致) | ✗ FAIL(768–855 区间) |

### Probe Execution

无 `scripts/*/tests/probe-*.sh` 约定探针,PLAN/SUMMARY 亦未声明探针路径;本阶段的「探针」即 check-05 的 item 8 / item 9,已在上表与 Behavioral Spot-Checks 中实际运行。

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| LAYOUT-01 | 06-01 | `#state-badge { right: 448px }` 魔法数消除 | ✓ SATISFIED | 见 Truth 2;实质达成(流内化),机制偏离已由 D-03 显式登记 |
| LAYOUT-02 | 06-02, 06-03 | 窄窗口不破版:≥1024px 无横向溢出,**≥768px 无内容遮挡** | ✗ BLOCKED(前半句满足,后半句被证伪) | 见 CR-01 裁定;`REQUIREMENTS.md:147` 现标 Complete,与本报告不一致 |
| LAYOUT-03 | 06-01 | `#state-badge` 不再遮挡滚动内容 | ✓ SATISFIED | 见 Truth 3 |
| LAYOUT-04 | 06-02 | 侧栏滚动容器套娃收敛 | ✓ SATISFIED | 见 Truth 4;SC#3 措辞收窄已按 A-5 登记 |
| A11Y-07 | 06-03 | 紧凑控件达到 24×24 命中区 | ✓ SATISFIED | 见 Truth 5;覆盖边界见 advisory 末条 |

**Orphaned requirements:** 无。三个计划的 `requirements:` 字段合计覆盖 `LAYOUT-01/02/03/04 + A11Y-07`,与 ROADMAP Phase 6 的 Requirements 行逐字一致。

**Decision coverage:** 20/20 CONTEXT.md 决策被已交付产物覆盖(`check.decision-coverage-verify` → `All trackable CONTEXT.md decisions are honored`)。非阻塞。

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `scripts/check-05-ui-uat.py` | 1932-1933, 1945-1946 | 覆盖主张超出实际测量范围(「已由 badge × banner 不相交断言覆盖」) | 🛑 Blocker | 让 768px 的 LAYOUT-02 判据在真实遮挡下报 PASS;与自登记的 T-idi-06-04 同型 |
| `frontend/style.css` | 228, 709-723 | 既有几何:居中 fixed banner 与 340px 下限面板在 768–855px 相交 | ⚠️ Warning | 遮挡本身非本阶段引入;但在本阶段被声明为已满足 |
| `scripts/check-05-ui-uat.py` | 2116-2167 / 2186-2192 / 1588-1595 | 空转 PASS / 测错对象 / 常量无绑定 | ⚠️ Warning | 见 advisory 1-3;均未在今日触发 |
| `frontend/style.css`, `scripts/check-05-ui-uat.py` | — | `TBD` / `FIXME` / `XXX` | — | **无命中**(债务标记门通过) |

### Human Verification Required

状态为 `gaps_found`(Step 9 规则 1 优先于 human_needed),故不单列 human 项;以下两条可人工复核,均不阻塞、也不改变上述裁定:

1. **真实 SSE 断流下的遮挡** —— 在 768px 视口断开后端 SSE,观察 `#stream-banner` 是否如经 `showStreamBanner()` 构造时一样压住面板标题。预期:是(本报告用的是应用自身的横幅构造路径,未走真实断流)。
2. **sticky 表头的视觉观感** —— `background: var(--color-surface)` 与 `border-radius: 0` 在滚动时的观感(评审已实测其行为正确:`scrollTop=4348` 时 `header.top == 0`)。

## CR-01 裁定(LAYOUT-02 的状态)

我按任务要求,把独立评审的 CR-01 当作**待验证的输入**而非结论,逐条复核。结论:**CR-01 成立**,但它的两个组成部分要分开定性,因为它们对「本阶段该做什么」的答案相反。

### 1. 768px 遮挡是否违反 LAYOUT-02 的字面文本 —— 是

我独立复现了全部几何(未采信任何既有数字),并用评审未用的手段把「相交」升级为「遮挡」:

```
p1 @768×900:  h1     l=439.0 r=481.0 t=8.0  b=28.0   (42 × 20)
              banner l=285.3 r=482.7 t=12.0 b=39.0   (position:fixed, z-index:20, bg rgb(255,247,194))
              h1 ∩ banner      = True, overlap 42.0 × 16.0 px   ← 水平 100%、垂直 80%
              header ∩ banner  = True, overlap 53.7 × 24.0 px
              badge ∩ banner   = False
              elementFromPoint(440,18) / (460,18) / (480,18) / (441,26) → 全部 #stream-banner
p3 @768×900:  同一结论(overlap 42.0 × 15.0 px)
边界扫描:     768→True 800→True 840→True 850→True 855→True 856→False 880/1024/1280→False
```

`elementFromPoint` 返回的是**命中测试的最上层元素**:在 768px 下,标题盒内任意一点都命中 `#stream-banner`,意味着标题「文档区」在这 42×20 的盒子里既不可见也不可命中。这不再是「rect 相交」的间接推断,而是绘制顺序的直接读数。

**「无内容遮挡」是否被合理地读窄?** 我查了三处可能的窄读法,结论是都挡不住:

- **UI-SPEC §L-2 的判据表**(`idi-06-UI-SPEC.md:192`)写的是「关键元素 rect **两两不相交**(badge × banner、表头 × 正文、按钮 × 视口)」。括号里的枚举把**「表头」列为三个关键元素之一**;`#stream-banner` 也是关键元素(它正因「会盖住东西」才被点名)。故 banner ∩ 表头 落在「两两不相交」之内。相反,窄读法需要论证「表头不是关键元素」或「banner 不是关键元素」,两者都与该表自身的枚举冲突。
- **06-CONTEXT D-08**(:85)把判据定义为「`scrollWidth > clientWidth`(**横向溢出**)与关键元素 rect 相交(**遮挡**)」,并规定在 **1440 / 1024 / 768 三处**量 —— 即遮挡与溢出一同是 768px 的判据。
- **ROADMAP SC#1**(:219 上文)写「窗口从 1440 收到 768:**无横向溢出、无内容被遮挡**」,SC#2 才把 banner 的检查点收窄到 1024/1280 —— 但 SC#2 的对象是 **badge**,不是「内容」的总称。把 SC#2 的窄口径套到 SC#1 上,等于用一条关于 badge 的判据替换一条关于全部内容的判据。

反向证据我也核了,并且它确实存在:`ROADMAP.md:234` 的 **Gates** 行写「1024/1280 下横幅不盖 badge」。这是全篇唯一支持窄读法的句子。但它(a)说的是 badge、(b)与 REQUIREMENTS.md:52 的「≥768px 无内容遮挡」直接冲突。**规划阶段的选择是采纳了窄读法(只查 badge),却没有把这个读法登记下来** —— UI-SPEC §L-2 的判据表反而抄了宽口径。所以窄读法不是「被声明的范围收窄」,而是一个**未登记的口径替换**。按本项目自己的先例(UI-SPEC :568 的 A-5:SC#3 措辞收窄必须显式登记),它本该被登记;它没有。

**结论:按 REQUIREMENTS.md / ROADMAP SC#1 的字面文本,768px 遮挡构成 LAYOUT-02 的违反。**

### 2. 门是否在声称它不交付的覆盖 —— 是,两处,逐字如下

`scripts/check-05-ui-uat.py:1931-1933`(本阶段新增):

```python
# LAYOUT-02 的字面承诺「≥1024px 无横向溢出」—— 1440 与 1024 两处升为硬断言。
# 768 处保持只读诊断:它在 LAYOUT-02 里的承诺是「无内容遮挡」,已由本项前面的
# badge × banner 不相交断言覆盖(UI-SPEC §L-2 的判据表)。
```

`scripts/check-05-ui-uat.py:1943-1946`(本阶段新增,运行时逐宽度打印):

```python
                else:
                    info(f"item8 L-2 @{width}px",
                         "保持只读诊断(768px 处的承诺是「无内容遮挡」,"
                         "已由 badge × banner 不相交断言覆盖)")
```

它指向的断言是 `:1834`,标签为 `f"[p1 @{width}px] #state-badge 与 #stream-banner 不相交"` —— 只测 `#state-badge`。实测该断言**为真且应当为真**(badge 639.0–739.9 与 banner 285.3–482.7 确实不相交),所以它在真实遮挡存在的宽度上干净地 PASS。`item 8: PASS (13 条断言,0 FAIL,0 BLOCKED)` 因此是真的 —— 但「真」的是 badge 不被盖,不是「无内容遮挡」。

同一主张还被复制进计划与总结:`idi-06-03-PLAN.md:37` 与 `:212`、`idi-06-03-SUMMARY.md:150` 都写着「768 处保持只读诊断……已由 badge × banner 不相交断言覆盖」。**该措辞在本阶段新增**(`git diff` 确认)。

更要紧的一层:**UI-SPEC §L-2 点名的三对判据里,只有 `badge × banner` 被测量过。** 我全仓搜索 `表头 × 正文` 与 `按钮 × 视口`:`scripts/check-05-ui-uat.py` 零命中,SUMMARY / PLAN 里也只出现在复述 UI-SPEC 判据表的行里。也就是说,768px 的判据不但漏掉了实际发生的那一对(banner × 表头),连它自己表里另外两对也从未测过,却在 SUMMARY 的「测量决策记录」里被登记为「被实测推翻(三宽度均无破版)」。该决策记录的两列(`scrollWidth/clientWidth` 与 `#doc-panel` 实测宽)确实只覆盖了溢出半边。

### 3. 我是否独立复现了它 —— 是

我没有采信评审的任何数字。三个自写探针(均复用 `scripts/check-05-ui-uat.py` 自身的 `make_fixture` / `enter_project` / `showStreamBanner`,即与被测门同一条状态构造路径,不手工拼 DOM):

- `/tmp/idi06_cr01_probe.py` —— p1 与 p3 两样本 × 768/900/1024/1440 四宽度,读 panel/header/h1/badge/banner 的 rect 与 computed 样式。结果见上表;与评审的数字一致(评审 482.7 vs 我 482.66,同一位小数)。
- `/tmp/idi06_paint_probe.py` —— `document.elementFromPoint` 四点采样 + 截图。@768 全部 `#stream-banner`,@1024 全部 `h1`。
- `/tmp/idi06_boundary_probe.py` —— 10 个宽度的边界扫描,实测边界 855/856,与解析解(vw < 855.3)吻合。

我在**两个样本**(p1 / p3,横幅文案不同、badge 文案不同)上各测一遍,结论相同,故这不是某个样本的偶然。

### 4. 这是什么缺陷,以及 LAYOUT-02 的诚实状态

两个组成部分,定性不同:

**(a) 几何本身:既有的,且在本阶段的契约下不可修。** `#stream-banner` 的声明(`:709-723`)与 `--doc-panel-w` 的 `clamp()`(`:228`)都不在本阶段 diff 内;`frontend/index.html:84` 的 `#doc-panel-header` 本阶段零改动。我核实了本阶段对 index.html / app.js 的 diff 为空。所以这不是回归。而且 UI-SPEC 的范围锁把两条最直接的修法都堵死了:`#stream-banner` 的任何声明**不得触碰**(:665,理由「L-1 的门断言几何不相交,不得靠移动横幅来通过」);`--doc-panel-w` 的**值交由用户裁决,执行器不得自行改动**(`style.css:224-227` 的注释)。剩下的唯一合法路径是 L-2 的 `@media (max-width: 1023px)` 守卫,但它允许的形态是在媒体作用域内重赋 `--doc-panel-w` 或收窄 `#doc-panel-body` 的 padding —— 要把面板左缘推到 banner 右缘(482.7)之外,面板宽需 ≤ 285.3px,**低于 clamp 下限 340px**,即该路径在几何上也不通。**故这一半在阶段内不可修,应当被登记为已知缺口 + 范围收窄(照 A-5 的先例),而不是被声明为已满足。**

**(b) 覆盖主张:本阶段新增的,且是本阶段真正该修的。** 措辞是本阶段写进 harness 的,它把事实说反了。按项目的既定纪律(「不看就报 PASS 的门比没有门更糟」),这一条比 (a) 严重:几何缺陷至少是诚实的既有状态,而这条主张**阻止下一个读者去看**。它也是本阶段自己登记过的威胁 T-idi-06-04(「假 PASS(空转断言)」,`idi-06-01-PLAN.md:412`)的实例 —— 该威胁的缓解措施被写在 badge×banner 断言上,而那条断言缓解的恰恰不是它声称的那个风险。

**LAYOUT-02 的诚实状态:未达成(前半句达成、后半句被证伪)。** 它不应被标记为 Complete。两条 remediation(二选一,不可都不做)已写进 frontmatter 的 `gaps[0].missing`:

- **(a) 真正断言该判据** —— 扩展 `_IDI06_BADGE_BANNER_JS`(:1630)返回 `#doc-panel-header` 与其 h1 的 rect,并在 768px 加一条不相交断言。它今天会 FAIL,那正是正确的信号;但**底层修复需要先解开上述契约冲突**(改 banner 定位或改 `--doc-panel-w` 的值),不能只靠 harness。
- **(b) 声明该对不在范围内** —— 用实测数值替换 :1932-1933 与 :1945-1946 两处措辞,写成显式「未覆盖」,并照 A-5 的先例把范围收窄登记进 `idi-06-UI-SPEC.md` §L-2 与验证记录,同时把 UI-SPEC :192 判据表里从未测过的「表头 × 正文」「按钮 × 视口」两对一并说明。

如果项目决定采纳 (b),则 LAYOUT-02 的后半句应作为一次**有意偏离**走 override 机制(而不是悄悄留在 Complete 上)。

**【已接受 2026-09-22】** 项目所有者本次会话显式选择了 remediation (b),该 override 已写入本报告 **frontmatter** 的 `overrides:` 数组(`accepted_by` 取仓库 git 身份、`accepted_at` 为本次会话裁定时间戳;`overrides_applied` 仍为 0,留给复验时应用)。这份接受来自**用户的显式选择**,不是执行器的单方裁定。原先留空的模板已移除 —— override 只认 frontmatter,写在正文里的同名 YAML 复验器从不读取。在缺省(无 override)状态下,LAYOUT-02 就是 FAILED;现在它按 override 路径在复验时记 `PASSED (override)`。

### 与本阶段其余部分的区分

CR-01 不应被读成本阶段整体不可信。相反:我复核过的其余部分(LAYOUT-01/03/04、A11Y-07、sticky 表头、六目标换行、`min-width: 0`)全部有真实实现与真实断言支撑,六道静态门与九项 harness 全绿,且多数断言是强断言(见「断言强度复核」)。本阶段的失败是**单点的**:一条被声称覆盖而实际未覆盖的判据。它恰好落在本项目最在意的那一类上。

---

_Verified: 2026-09-22T06:09:33Z_
_Verifier: Claude (gsd-verifier)_
---
phase: idi-05-typography-and-visual-hierarchy
verified: 2026-09-21T07:12:16Z
status: human_needed
score: 8/8 must-haves verified
covered_files:
  - .planning/REQUIREMENTS.md
  - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-01-PLAN.md
  - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-01-SUMMARY.md
  - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-02-PLAN.md
  - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-02-SUMMARY.md
  - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-03-PLAN.md
  - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-03-SUMMARY.md
  - frontend/style.css
  - scripts/check-05-ui-uat.py
covered_digest: "v1:sha256:b34a2d19992727153ec64f46e11ed088bf866b2c73ae09024488e06d7696be07"
behavior_unverified: 0
overrides_applied: 0
deferred:  # Registered downstream obligation, not a phase gap (D-05)
  - truth: "idi-04.1-radix 的 passed 指纹(frontend/style.css 与 scripts/check-05-ui-uat.py 在其 covered_files 内)在本阶段编辑后 stale"
    addressed_in: "idi-04.1-radix re-verification via /gsd-verify-work idi-04.1-radix"
    evidence: "重算 HEAD 上的 13 个 covered_files 得 v1:sha256:dd4a46213d0c58a3c529c619f659d1ec00a541f1af190d3817b516c36ecfaf47,与记录的 25d5f1fe… 不同。成因是内容真变(本阶段重写这两个文件),故属重新验证而非补指纹。plan 03 Task 3 已在 HEAD 上逐条重算 04.1 的四条守卫与三处结论(全部逐字不变;tier-2 47→48、清单 43→47 两处差值已登记),报告文件本身零改动(git status --porcelain -- .planning/phases/idi-04.1-radix/ 为空)"
human_verification:
  - test: "E4/E5 —— 在 p1(会话流)/ p3(本轮批注流)/ checking(自检报告)三个样本下,确认活动面板标题行左侧的 3px 蓝竖条**真实可见**:不被标题行内元素盖住、不因 border-radius 在角落断开、标题文本变长时仍贴左缘"
    expected: "三条竖条在各自样本下完整可见;非活动面板与 #ai-panel / #doc-panel-header 无竖条"
    why_human: "check-05 读的是 .panel-header 的 computed box-shadow(语义 inset/3px/0/0/0/marker,已 PASS),但「不被遮挡、不在圆角处断裂」是渲染几何,computed style 看不见。UI-SPEC 已把它记为 E4/E5 的 backstop 陈述,不自动判过"
  - test: "E6/E7 —— 两个 12×12 mask 字形(.annotation-quote::before 的图钉、.verdict-location::before 的地图标记)与相邻文字的**基线视觉对齐**,且不撑高行盒(行高仍由 --lh-snug / --lh-reading 决定)"
    expected: "两个字形与首行文字视觉齐平,折行时不漂移,行盒高度不变"
    why_human: "宽度/高度/底色/mask-image 已由 check-05 逐条读到并 PASS,但基线对齐与行盒影响是渲染结果,只能看(05-N-5 / UI-SPEC E6·E7 backstop)"
  - test: "E8 —— 通读渲染后的页面,确认页面级层级「读起来」成立:文档 h1 > 模态 .overlay-card h3 > 文档 h2 > 容器标签「文档区」"
    expected: "全屏最大最重的文字是文档自己的 h1,不是容器标签;三级标题层级分明、不互相淹没"
    why_human: "字号半边由 check-05 的运行时断言钉死(28 > 24 > 22 > 14),但「层级读起来分明」是视觉判断,computed style 数值还原不出。plan 01 coverage D5 / plan 02 D3 均自标 human_judgment: true"
  - test: "E3 —— 在 --doc-panel-w 最窄值 340px(内容宽约 260px)下,确认 #btn-authorize 的文本「授权撰写总设计文档」在 16px 下**不换行、不裁切**"
    expected: "单行显示,不换行不裁切"
    why_human: "计划给出的算术(标签约 144px + padding-x 32px ≈ 176px < 260px)成立,但 check-05 不把面板压到 340px 实测,故换行半边无运行时证据(UI-SPEC E3 long-text backstop)"
  - test: "VISUAL-04 口径确认 —— #ai-panel 不参与「三选一活动态」推导(D-16 收窄),其可辨状态仍是既有的 ▾/▸ 折叠指示器"
    expected: "人工确认「四面板活动/非活动态可区分」这一 REQUIREMENTS 措辞按 D-16 的「三选一活动态 + AI 面板折叠态」口径被接受;若需给 AI 面板也加活动标记,则是新的范围"
    why_human: "REQUIREMENTS.md 的 VISUAL-04 原文写「侧栏四个面板…可区分」,而 ROADMAP SC4 只列三个面板 + 「#ai-panel 的折叠行为不变」。D-16 已登记该收窄且明写「本阶段不改 REQUIREMENTS.md(改它会作废指纹)」。这是口径裁决,不是代码缺陷"
  - test: "点击 #ai-panel 的折叠指示器,确认折叠/展开行为与改动前一致(本阶段新增的两条标记规则不匹配 #ai-panel)"
    expected: "#ai-panel-body 的 .collapsed 切换正常,指示器字形切换正常,标题行不出现竖条"
    why_human: "本阶段对 app.js / index.html 零 diff、.collapse-indicator 逐字节未动,且 check-05 的对照组已断言 #ai-panel .panel-header box-shadow == none —— 行为「按构造不变」是结构性证明,但没有任何测试**执行**这次切换。属低成本人工点击确认"
---

# Phase 5: 排版与视觉层级 — Verification Report

**Phase Goal:** 渲染出的文档与界面 chrome 各有一套受控的排版刻度;产品最重要的一步(不可逆的 G3 授权)在视觉上不再与例行按钮混同;页面级层级正确。
**Verified:** 2026-09-21T07:12:16Z
**Status:** human_needed
**Re-verification:** No — initial verification(本阶段目录下此前无 `*-VERIFICATION.md`)

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | **TYPE-01 / SC1** — `.markdown-body h1/h2/h3` 有显式 `font-size` 且作用域限定在 `.markdown-body` 内;四个宿主(`#draft-content` / `#brainstorm-content` / `#round-doc` / `#latest-check`)分别解析为 28 / 22 / 18px;四处 chrome 覆盖未被带偏 | ✓ VERIFIED | `style.css:719-721` 三条作用域规则(`var(--text-3xl/-2xl/-lg)`);`grep -c '^h1, h2'` = 0(无全局规则);`--item 4` 独立复跑 **65 条断言 / 0 FAIL / 0 BLOCKED**,含 4 宿主 × 3 档 = 12 条令牌接线断言 + 四条 chrome 守卫(`.panel-header h2` 14px、`#draft-view h2` 18px、`#brainstorm-view h2` 令牌接线、`.overlay-card h3` 24px)。层叠缺陷(三条 chrome 规则 1-0-1 后代选择器压掉 `.markdown-body h2`)已由收窄为 `#draft-view > h2` / `#round-title` / `#brainstorm-view > h2` 修复,DOM 结构核实三条规则均能匹配到目标元素 |
| 2 | **TYPE-02** — markdown 内容排版归入刻度与令牌:`table th/td`、`code`、`blockquote` | ✓ VERIFIED | `style.css:731-737`:`th, td` 与 `code` 均 `font-size: var(--text-base)`;`blockquote` `color: var(--color-text-muted)`。这是 D-08 的**复证项**(零 CSS 改动,已由 quick `260918-qrq` 实现);`--item 4` 出运行时证据(`td font-size` 令牌接线、`blockquote color` 令牌接线、`code font-size` 字面守卫 14px 三条 PASS)。`--text-base` 消费者 19 处,无孤儿 |
| 3 | **TYPE-03** — 字重层级(基线仅 600 / 400 两档 → 三档分工显式化) | ✓ VERIFIED | 三档 `--fw-regular` 400 / `--fw-medium` 500 / `--fw-semibold` 600 均声明且有消费者(各 1 / 8 / 8)。`--item 4` 六条字重断言:五只动作按钮 computed = 500、`#btn-authorize` = 600(D-12 唯一已登记例外)。内容标题 `.markdown-body h1/h2/h3` = `--fw-semibold`(600)、chrome 标题 `.panel-header h2` = `--fw-medium`(500)在源码中逐字可核 |
| 4 | **VISUAL-01 / SC2** — `#btn-authorize` 采用不可逆动作的独立视觉处理(实心填充)并配保留令牌;与例行按钮计算样式不同;授权按钮字面文本达 AA | ✓ VERIFIED | `style.css:143-145` 声明 `--color-action-irreversible/-surface/-fg`(green-12 / green-12 / white);`#btn-authorize`(1050-1058)是唯一消费者(围栏外恰 3 行,全在该规则体内,D-15)。`--item 3` 三档坡道断言:routine / commit / irreversible **三档两两不同**、档内各自相同。AA:`check-02` 实算 `--color-action-irreversible-fg ON --color-action-irreversible-surface` = **12.32**(我手工按 WCAG 公式复核 = 12.32),≥ 4.5 |
| 5 | **VISUAL-02** — `#btn-approve-draft`(G1)与 `#btn-start-writing` 为第二档;routine 三只保持中性 | ✓ VERIFIED | commit 族令牌 `style.css:140-142`(green-11 实心 + 白字);两条规则(743-750 / 1065-1071)消费之。routine 族 `137-139` 逐字节未变(淡底 green-3 + 绿字 green-12);`--item 3` 的 `trio()` 断言 routine=(green-12, green-11, green-3)、commit=(white, green-11, green-11)、irreversible=(white, green-12, green-12),三者互异 |
| 6 | **VISUAL-03 / SC3** — 容器标签「文档区」降级为视觉标签;全屏最大最重的文字不再是它 | ✓ VERIFIED | `style.css:493-498` `#doc-panel-header h1` = `--text-base`(14px)/ `--fw-medium`(500)/ `--color-text-secondary`;源码注释即「安静的容器标签,不是全屏最大最重的文字」。`--item 4` 字面守卫 14px / 500 + 页面级层级链严格降序 **28 > 24 > 22 > 14**(整数比较,避免 "14px" < "9px" 序陷阱)+ `#doc-pane` DOM 元素不存在断言(契约漂移登记)。零 CSS 改动,属复证 |
| 7 | **VISUAL-04 / SC4** — 侧栏当前活动面板可辨认;`#ai-panel` 折叠行为不变 | ✓ VERIFIED | `style.css:169` 新 tier-2 令牌 `--color-marker-active: var(--radix-blue-11)`;`style.css:1223-1228` 两条追加规则(`:not(.hidden) .panel-header` 3px inset 竖条 + 标题变色)。`--item 4` 三态实读(p1 `#session-panel` / p3 `#annotations-panel` / checking `#checks-panel`)各 4 条断言,含对照组 `#ai-panel .panel-header` 与 `#doc-panel-header` 必须 `box-shadow: none`。`#ai-panel` 从不被 `.hidden`(app.js 中 `aiPanel` 零命中,已复核);`app.js` / `index.html` 零 diff,`.collapse-indicator` 逐字节未动 |
| 8 | **VISUAL-05 / SC5** — 两处写死的 emoji 替换为 SVG;`frontend/vendor/` 无新增文件;无 CDN `<link>` | ✓ VERIFIED | `style.css:320-321` 两个 data-URI SVG 令牌(`--icon-pin` / `--icon-location`),`<path>` 不带 `fill`、data-URI 内零颜色信息;两处伪元素原地改写为 mask 盒模型(942-958 / 1147-1163)。`--item 4`/`--item 6` 各读到 12×12 + `background-color: var(--color-text-secondary)` + `mask-image` != none;`%23…` / `fill='` 字面均 0。`ls frontend/vendor/` = 仅 `marked.min.js`;`index.html` 仅一条本地 `<link rel="stylesheet" href="style.css">`,无 CDN |

**Score:** 8/8 truths verified (0 present, behavior-unverified)

**Note on the two mechanism deviations the phase registered (not silently greened):**
- **VISUAL-01/02 的填充步 = green-11 / green-12,不是契约预告的 green-9 / green-10。** UI-SPEC §S-7 用 `check-02` 实算说明原因(green 9 步白字 3.16 ✗、10 步 3.55 ✗、11 步 4.72 ✓、12 步 12.32 ✓),并指出「step 9 = 实心填充」的 Radix 规范用法在本项目每一族都过不了 4.5:1。**本阶段新增 tier-1 primitive = 0**,围栏 L42-45 的 9/10 预告已改写为真。D-11 本就写明「具体取哪两个步由规划期定」,故这是规划期裁量而非违约。
- **VISUAL-05 的机制 = `mask-image` + `background-color`,不是契约的 `content: var(--icon-*)`。** 这是 D-20 的刻意偏离,UI-SPEC §A-2 已登记。**关键裁定:`04-UI-SPEC.md` Q7 自己写的就是「Inline SVG, defined once as a data-URI token, referenced by `content: var(--icon-*)`」——契约从未要求 DOM `<svg><use>`(Q7 约束 1 显式排除它)。** 故 mask 方案仍落在「CSS 内嵌 SVG data-URI」这一族里,ROADMAP 的「内联 SVG」按项目自身的读法成立。附带收益:data-URI 内零颜色信息,契约字面量例外 L-3 整个撤掉(§A-1)。

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `frontend/style.css` | 唯一改动面:围栏内新增声明 + 围栏外排版/层级规则 | ✓ VERIFIED | 本阶段 diff +235 行;逐行核对全部增删:两条字号档、五个坡道令牌值、三个新令牌(marker + 两个 icon)、两处 `--icon-*` 声明、三条 chrome 选择器收窄、三条 markdown 标题字号、四行按钮字重、两条追加标记规则、两处 emoji→mask 原地改写、围栏注释四处改写。**无意外改动** |
| `scripts/check-05-ui-uat.py` | UAT 断言面随需求扩张(D-03/D-04 分类更新) | ✓ VERIFIED | +349 行;item4 27 → 65 条、item3 14 → 17、item6 2 → 6、smoke 6 → 8。新增 `read_pseudo_style` / `trio` / `check_active_marker` / `check_marker_control` / `check_mask_glyph`。**原 D-04 逐字节相同断言已删除并反转为三档断言(已核实旧断言不再存在)** |
| `frontend/app.js` / `index.html` / `frontend/vendor/` / `scripts/ui-states/` | 零 diff(硬规则 5 / 契约边界) | ✓ VERIFIED | `git diff --stat babae34^..HEAD -- <这四个面>` 为空 |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| `--text-3xl` / `--text-2xl` / `--text-lg` | `.markdown-body h1/h2/h3` | `font-size` 声明 | ✓ WIRED | 各 1 个消费者;`--item 4` 在四个宿主上读到解析值 |
| `--icon-pin` | `.annotation-quote::before` | `mask-image`(无前缀 + `-webkit-` 各 1) | ✓ WIRED | `--item 6` 读到 `mask-image != none` 且值是 `--icon-pin` 的 data-URI |
| `--icon-location` | `.verdict-location::before` | `mask-image`(无前缀 + `-webkit-` 各 1) | ✓ WIRED | `--item 4` 读到 |
| `--color-marker-active` | 三条 `:not(.hidden) .panel-header` 规则 | `box-shadow: inset 3px 0 0` + `h2 color` | ✓ WIRED | 三态实读语义 box-shadow + 标题 color;对照组为 `none` |
| `--color-action-irreversible*` | `#btn-authorize` | `background` / `border-color` / `color` | ✓ WIRED | 围栏外恰 3 行消费者,全在该规则体内(D-15 单消费者不变量成立) |
| `.hidden { display:none !important }` | 三条标记规则的 `:not(.hidden)` | 纯读取既有显隐机制 | ✓ WIRED | CHECK-03(`^\.hidden {` = 1)/ CHECK-04(`!important;` = 1)钉住唯一性;`.hidden` 规则零改动 |

### Data-Flow Trace (Level 4)

纯 CSS 阶段,「数据」是令牌层 → 消费者声明 → 浏览器 computed value → 断言。逐条追踪:

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `.markdown-body h2`(四宿主) | `var(--text-2xl)` | `:root` 围栏声明 22px | Yes(computed 22px × 4 宿主) | ✓ FLOWING |
| `#btn-authorize` | `--color-action-irreversible-surface` 等 | 围栏 → green-12 / white | Yes(computed + check-02 实算 12.32) | ✓ FLOWING |
| `.annotation-quote::before` | `var(--icon-pin)` | 围栏 data-URI | Yes(computed mask-image 返回该 data-URI) | ✓ FLOWING |
| `.panel-header`(活动) | `var(--color-marker-active)` | 围栏 → blue-11 | Yes(computed rgb(13,116,206)) | ✓ FLOWING |

无静态兜底、无硬编码空值、无 mock。**无 HOLLOW_PROP / STATIC / DISCONNECTED。**

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| 令牌一致性(围栏外零裸 hex) | `bash scripts/check-01-token-conformance.sh` | `PASS` / exit 0 | ✓ PASS |
| 对比度清单(47 对 + 1 序关系) | `python3 scripts/check-02-contrast.py \| tail -3` | `PASS: 0 failures`;末三行含 `4.65 --color-marker-active on --color-surface-page` 与 `ORDER 0.363` | ✓ PASS |
| `.hidden` 唯一性 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` / exit 0 | ✓ PASS |
| `!important` 计数 | `bash scripts/check-04-important-count.sh` | `PASS` / exit 0 | ✓ PASS |
| UAT item 1/2/3/4/6(真实浏览器 computed style) | `.venv/bin/python scripts/check-05-ui-uat.py --item 1,2,3,4,6` | item 1: 45 / item 2: 5 / item 3: 17 / item 4: **65** / item 6: 6 —— **全 0 FAIL / 0 BLOCKED** / exit 0 | ✓ PASS |
| 四宿主标题字号 | 含于 item 4 | 12 条断言全 PASS | ✓ PASS |
| 三档坡道两两不同 | 含于 item 3 | 3 条断言全 PASS | ✓ PASS |
| 页面级层级链 | 含于 item 4 | `28 > 24 > 22 > 14` 严格降序 PASS | ✓ PASS |
| AA(授权按钮白字对实心) | `check-02` + 手工 WCAG 复核 | 12.32(手工 = 12.32) | ✓ PASS |
| 零 diff 面 | `git diff --stat babae34^..HEAD -- frontend/app.js frontend/index.html frontend/vendor/ scripts/ui-states/` | 空 | ✓ PASS |
| 孤儿/未声明令牌 | 脚本比对声明集与消费集 | 未声明 used = []、声明未消费 = [] | ✓ PASS |

**Step 7b: SKIPPED 部分** —— 本阶段无独立 CLI/构建产物;运行面即上面的 Playwright UAT。截图路线按已知环境事实不可用(SSE 长连接),故渲染几何项路由到人工。

### Probe Execution

本阶段未声明或约定 `scripts/*/tests/probe-*.sh`;`find scripts -path '*/tests/probe-*.sh'` 无结果。**N/A — 无探针。**

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| TYPE-01 | 01 | `.markdown-body h1/h2/h3` 显式字号、作用域限定 | ✓ SATISFIED | 见 Truth 1 |
| TYPE-02 | 01 | table/code/blockquote 归入刻度与令牌 | ✓ SATISFIED | 见 Truth 2 |
| TYPE-03 | 01 | 字重层级 | ✓ SATISFIED | 见 Truth 3 |
| VISUAL-01 | 02 | 不可逆授权独立视觉处理 + 保留令牌 | ✓ SATISFIED | 见 Truth 4 |
| VISUAL-02 | 02 | G1/start-writing 第二档;routine 中性 | ✓ SATISFIED | 见 Truth 5 |
| VISUAL-03 | 02 | 页面级层级,容器标签降级 | ✓ SATISFIED | 见 Truth 6 |
| VISUAL-04 | 03 | 侧栏活动面板可辨 + ai 折叠不变 | ✓ SATISFIED | 见 Truth 7;口径收窄(D-16)见 Human #5 |
| VISUAL-05 | 03 | 两处 emoji → 内联 SVG,零第三方 | ✓ SATISFIED | 见 Truth 8 |

**ORPHANED requirements:** 无。Phase 5 的 8 条需求全部被计划 `requirements:` 字段认领(01→TYPE-01/02/03、02→VISUAL-01/02/03、03→VISUAL-04/05)。

**关于「标记 Complete 但证据不足」的核查结论:** 逐条核对 REQUIREMENTS.md 第 129-136 行,8 条均标 `Complete`。**未发现证据不支持的条目。** 需要用户知情的两点是**口径与机制的登记**,不是证据缺口:(a) VISUAL-04 的原文「四个面板…可区分」经 D-16 收窄为「三选一活动态 + AI 面板折叠态」,`#ai-panel` 无活动标记;(b) VISUAL-05 的「内联 SVG」按契约 Q7 自身的读法是 CSS 内嵌 data-URI(非 DOM `<svg>`),mask 方案落在同一族内。两者都在 UI-SPEC 登记且未改 REQUIREMENTS.md(改它会作废指纹)。

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| — | — | `TBD` / `FIXME` / `XXX` | — | **0 命中**(两个改动文件均无债务标记) |
| — | — | `TODO` / `HACK` / placeholder 文案 | — | 0(仅 `#rounds-placeholder` 元素 id 命中 `placeholder` 子串,非 stub) |
| — | — | 空实现 / 硬编码空值 / console-only | — | 0(纯 CSS 阶段) |
| `frontend/style.css` | 337 | `.collapse-indicator { font-size: 20px; line-height: 1; }` 刻度外字面量 | ℹ️ Info | 已由用户裁定为 backlog `999.1`,**本阶段范围外**(D-23);`.collapse-indicator` 逐字节未动 |

**Debt-marker gate:** 通过(无 `TBD`/`FIXME`/`XXX`)。

### Test Quality Audit

| Test File | Linked Req | Active | Skipped | Circular | Assertion Level | Verdict |
|-----------|-----------|--------|---------|----------|-----------------|---------|
| `scripts/check-05-ui-uat.py` | VISUAL-01…05 / TYPE-01…03 | Yes | 0 | No | Value / Behavioral | PASS |
| `scripts/check-02-contrast.py` | VISUAL-01 / VISUAL-04(比值) | Yes | 0 | No | Value(独立 WCAG 公式) | PASS |

**Disabled tests on requirements:** 0 —— 无 `skip` / `xfail` / `.only` 模式。
**Circular patterns detected:** 0 —— `check-05` 读的是真实浏览器渲染真实 CSS 的 `getComputedStyle`(独立 oracle);`check-02` 从围栏令牌值独立算 WCAG。期望值均**不是**被测系统自己产出的。`check-02` 的比值输出中无任何硬编码数字(`grep '4.65\|4.48\|11.70'` 在源码中零命中)。
**Insufficient assertions:** 0 —— 需求要求值级/行为级证据,断言达到 Value 级(逐属性 computed 值)与 Behavioral 级(四宿主 × 三档 + 三态 + 层级链)。

**两处观察(INFO,不改变判定):**
1. `trio()` 的「档内相同」用 `len({...}) == 1` 判定。若某只按钮选择器不存在,`read_style` 返回 `None`,`trio` 会退化为 `(None,None,None)` 并使该断言**空过**。**非空转的证明:** 六只按钮的存在性由 item4 的六条 `ok()` 字重断言独立覆盖(`ok()` 对 `actual is None` 记 BLOCKED,绝不记 PASS),而 item4 实测 0 BLOCKED ⇒ 六只全部存在 ⇒ 该断言不空转。
2. **D-04 的断言反转是本阶段修改了自己的门。** 这是**正当**的:旧断言(`#btn-process-round` 与 `#btn-authorize` 三属性逐字节相同)编码的正是本阶段要消除的缺陷,反转后的新断言**更强**(档内相同 ×2 + 档间两两不同 ×1)。已核实旧断言在 HEAD 上**不存在**。反转的是断言,不是现实。

### Decision Coverage

All trackable CONTEXT.md decisions are honored by shipped artifacts.(`check.decision-coverage-verify`:total 23 / honored 23 / not_honored [])

### Human Verification Required

见 frontmatter `human_verification` 六项。摘要:

1. **E4/E5 标记可见性几何** —— 3px 竖条在三个活动面板上不被遮挡、不在圆角处断裂、标题变长时仍贴左缘。
2. **E6/E7 字形基线对齐** —— 两个 12px mask 字形与相邻文字视觉齐平、不撑高行盒。
3. **E8 视觉层级判读** —— h1 > 模态 h3 > h2 > 容器标签「读起来」层级分明。
4. **E3 最窄面板下授权按钮不换行** —— 340px 面板宽实测。
5. **VISUAL-04 口径确认** —— 接受 D-16 的「三选一活动态 + AI 面板折叠态」收窄。
6. **`#ai-panel` 折叠点击确认** —— 行为「按构造不变」的结构性证明之外补一次实点。

### Downstream Obligations (not phase gaps)

**`idi-04.1-radix` 的 `passed` 指纹 stale(D-05)。** 该报告的 `covered_files` 含 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`(另含 `.planning/REQUIREMENTS.md`),三者都被本阶段改写。我独立重算 HEAD 上的全部 13 个 covered_files:

```
v1:sha256:dd4a46213d0c58a3c529c619f659d1ec00a541f1af190d3817b516c36ecfaf47   (HEAD)
v1:sha256:25d5f1fe52eaceb48939c1bc76bcd44734bb23f035a02b22f0017724475cb5f2   (记录值)
```

**不同 ⇒ 确证 stale。** 成因是内容真变,故属重新验证而非补指纹。plan 03 Task 3 已在 HEAD 上逐条重算 04.1 的四条守卫与三处结论(全部逐字不变;`ORDER 0.363`、4.53、冻结轮三属性、border-strong 3.24/3.15 均未变;tier-1 25 不变;tier-2 47→48 与清单 43→47 两处差值已登记),且**报告文件本身零改动**(`git status --porcelain -- .planning/phases/idi-04.1-radix/` 为空)——保住「谁改了什么」的可追溯性。指纹写回归 `/gsd-verify-work idi-04.1-radix`。

**这是已登记的流程义务,不是本阶段的隐藏缺口,故不进 `gaps:`、不影响 Phase 5 的 goal 判定。** 但它是**收口前必须履行的一步**:在 04.1 指纹重写之前,`idi-04.1-radix` 的 `passed` 状态在机械层面不成立。

### Gaps Summary

**无阻断性缺口。** 8/8 must-have truths 均 VERIFIED,无 MISSING / STUB 产物,无 NOT_WIRED 关键链接,无债务标记,无未认领需求。四层验证(exists / substantive / wired / data-flow)全部通过。

三点需要用户知情、但均**不构成缺口**的事项:
1. **人工/backstop 项**(frontmatter 六项)—— 渲染几何与视觉判读,computed style 看不见,UI-SPEC 已逐条记为 backstop。它们驱动 `human_needed`。
2. **两处已登记的机制偏离** —— 填充步 green-11/12(§S-7 有实算依据)与 mask 机制(§A-2;契约 Q7 本就读作 CSS 内嵌 data-URI)。均不违约。
3. **`idi-04.1-radix` 指纹 stale** —— 已登记的下游义务(见上),归 `/gsd-verify-work idi-04.1-radix`。

**关于「哪些是断言、哪些是判断」的坦白:** 字号、字重、坡道三档、层级链、令牌接线、AA 比值**全部是运行时读到的 computed 值与独立 WCAG 计算**,不是断言式声明;层级链用整数比较而非字符串比较。真正的判断项只有两处,且都已路由到人工:标记与字形的**渲染几何**(不可由 computed style 还原),以及 `#ai-panel` 折叠切换的**实点确认**(结构性证明之外的冗余确认)。

---

_Verified: 2026-09-21T07:12:16Z_
_Verifier: Claude (gsd-verifier)_
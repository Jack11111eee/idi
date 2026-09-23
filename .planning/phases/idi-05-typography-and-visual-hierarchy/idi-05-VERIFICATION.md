---
phase: idi-05-typography-and-visual-hierarchy
verified: 2026-09-21T13:25:51Z
status: passed
score: 9/9 must-haves verified
covered_files:
  - .planning/REQUIREMENTS.md
  - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-01-PLAN.md
  - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-01-SUMMARY.md
  - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-02-PLAN.md
  - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-02-SUMMARY.md
  - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-03-PLAN.md
  - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-03-SUMMARY.md
  - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-04-PLAN.md
  - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-04-SUMMARY.md
  - frontend/style.css
  - scripts/check-05-ui-uat.py
  - scripts/check-06-idi05-validation.py
covered_digest: "v1:sha256:300abaa46994338413693e446a8b89c6cea569a3c3284ea05cd397f8c86bd718"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: human_needed
  previous_score: 8/8
  gaps_closed:
    - "G-idi-05-1 (BLOCKER, from UI-REVIEW Top Fix 1): renderMarkdown() 的五个非 .markdown-body 注入目标回落 UA 默认值(32px / 28px)并带进第四字重档 700 —— 已由 plan 04 关闭;我独立复跑 item7(38 条断言 / 0 FAIL / 0 BLOCKED),五个容器全部真实创建后逐条读到 24 / 18 / 16 + 600"
  gaps_remaining: []
  regressions: []
  prior_human_items_disposition: "前一版 VERIFICATION.md 的 6 条 human_verification 已由用户 UAT 逐条判过并全部 pass(05-UAT.md:total 6 / passed 6 / issues 0)。本次不再重复路由。"
deferred:  # 已登记的下游义务,非本阶段缺口
  - truth: "idi-04.1-radix 的 passed 指纹(frontend/style.css 与 scripts/check-05-ui-uat.py 在其 covered_files 内)在本阶段编辑后 stale"
    addressed_in: "idi-04.1-radix re-verification via /gsd-verify-work idi-04.1-radix"
    evidence: "用 gsd-tools 的 verification.fingerprint 在 HEAD 上重算该报告全部 13 个 covered_files = v1:sha256:301afba6…,与记录的 v1:sha256:25d5f1fe… 不同 ⇒ 确证 stale。成因是内容真变(本阶段重写这两个文件),故属重新验证而非补指纹。plan 03/04 已在 HEAD 上逐条重算 04.1 的四条守卫与三处结论(ORDER 0.363 / 4.53 / border-strong 3.24 与 3.15 全部逐字不变;tier-1 25、tier-2 47→48、清单 43→47 三处差值已登记),报告文件本身零改动"
human_verification: []
advisory:
  - finding: "check-05 的 item7 调用点普查守卫锚在**计数**上(renderMarkdown( == 11、MARKDOWN_TARGETS == 9),而非把枚举的选择器与调用点逐一绑定;一个「删一个调用点、加另一个」的改动可保持两个计数不变而让枚举静默过期(REVIEW WR-03)"
    category: architectural
    reason: "本阶段正是为消灭「枚举按类名过期」这一缺陷类而存在。今日枚举经我独立核对**未**过期(11 处出现 = 1 定义 + 10 调用点,映射到 9 个互异选择器),故不是缺口;但守卫的形态弱于其标签所声称的强度"
    evidence_status: "none provided"
  - finding: "嵌入标题刻度只声明 font-size / font-weight,行高按容器继承:同一个嵌入 h1 在 .chat-bubble / .say-chunk 里占 39px 行盒、在 .event-content 里占 33px,而文档 h1 是 37.33px —— 嵌入 h1 的行盒**高于**文档 h1(REVIEW WR-06)"
    category: other
    reason: "我独立实测确认(见 Data-Flow / Behavioral 两节)。本阶段的 must_have 与 SC3 的判据是**字号与字重**,该不等式成立(28 > 24);且 CSS 注释显式说明不加 line-height 是 D-10「零新增行高令牌」的决定。故不构成 must-have 失败,但「嵌入刻度是一个刻度」这一措辞与实测不符,且无门覆盖"
    evidence_status: "reproduced — frontend/style.css:1263-1265"
  - finding: "四处 chrome 标题仍计算为 700(#draft-view > h2 18/700、#round-title 18/700、#brainstorm-view > h2 16/700、.overlay-card h3 24/700),而 plan 04 落地的嵌入规则注释声称 700 是「契约只声明三档之外的第四档」;无门扫描 chrome 标题(REVIEW WR-07)"
    category: other
    reason: "我独立实测确认。但该 700 在阶段基线(eaa338f)上**已经存在**(四条规则当时也未声明 font-weight,同样继承 UA bold),且这四处是 chrome 而非九个渲染目标 —— plan 04 的 must_have 把「不再有 700」明确限定在九个渲染目标内,故 must_have 成立。副作用是:本阶段把 .markdown-body h3 由 16px 提到 18px 后,文档 h3(18/600)与 #draft-view > h2(18/700)同尺寸而更轻"
    evidence_status: "reproduced — frontend/style.css:636 / 704-708 / 775-779"
---

# Phase 5: 排版与视觉层级 — Verification Report

**Phase Goal:** 渲染出的文档与界面 chrome 各有一套受控的排版刻度;产品最重要的一步(不可逆的 G3 授权)在视觉上不再与例行按钮混同;页面级层级正确。
**Verified:** 2026-09-21T13:25:51Z
**Status:** passed
**Re-verification:** Yes — 前一版报告(2026-09-21T07:12:16Z,human_needed,8/8)已被 plan 04 的改动判为 stale;本次为独立重导,不是对旧报告的确认。

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | **SC1 / TYPE-01** — 渲染出的 DESIGN.md 的 h1/h2/h3 有受控字号(不再由浏览器默认决定),四个 `.markdown-body` 宿主解析为 28 / 22 / 18px;四处 chrome 覆盖(`.panel-header h2` 14px、`#draft-view > h2` 18px、`#brainstorm-view > h2` 16px、`.overlay-card h3` 24px)**未被带偏** | ✓ VERIFIED | `frontend/style.css:718-721` 三条 `.markdown-body` 作用域规则;`grep -c '^h1, h2'` = 0(无全局规则);`.venv/bin/python scripts/check-05-ui-uat.py --item 4` **65 条断言 / 0 FAIL / 0 BLOCKED**。四条 chrome 守卫逐条实读 PASS。chrome 选择器由后代形态收窄为 `#draft-view > h2` / `#round-title` / `#brainstorm-view > h2`(P-19),我核对 `frontend/index.html:105/135/120`:三个目标元素分别是 `#draft-view` 的直接子、`#round-title` 的 id、`#brainstorm-view` 的直接子 —— **收窄未丢失任何目标元素** |
| 2 | **TYPE-02** — markdown 内容排版归入刻度与令牌:`table th/td`、`code`、`blockquote` | ✓ VERIFIED | `style.css:731-737`:`th, td` 与 `code` 均 `font-size: var(--text-base)`;`blockquote` `color: var(--color-text-muted)`。item4 出运行时令牌接线断言(`td font-size` / `code font-size` / `blockquote color` 三条 PASS) |
| 3 | **TYPE-03** — 字重层级显式化(三档 400 / 500 / 600 分工) | ✓ VERIFIED | `--fw-regular/-medium/-semibold` 三档均有消费者。item4 六条字重断言 PASS:五只动作按钮 = 500、`#btn-authorize` = 600(D-12 已登记唯一例外);内容标题 600、chrome 标题 500 |
| 4 | **SC2 / VISUAL-01** — `#btn-authorize` 独立视觉处理(实心填充)+ 保留令牌;与例行按钮计算样式不同;授权按钮字面文本达 AA | ✓ VERIFIED | `style.css:143-145` 声明 `--color-action-irreversible*`(green-12 / white),唯一消费者 `#btn-authorize`。item3 三档坡道断言 PASS:routine / commit / irreversible **三档两两不同**、档内各自相同。AA:`check-02` 实算 `--color-action-irreversible-fg ON --color-action-irreversible-surface` = **12.32**;我按 WCAG 公式手工复算 = 1.05 / (0.035256 + 0.05) = **12.32**,≥ 4.5 |
| 5 | **VISUAL-02** — `#btn-approve-draft`(G1)与 `#btn-start-writing` 为第二档;routine 三只保持中性 | ✓ VERIFIED | commit 族令牌 green-11 实心 + 白字;routine 族逐字节未变(淡底 green-3 + 绿字 green-12)。item3 实读 routine=(green-12, green-11, green-3)、commit=(white, green-11, green-11)、irreversible=(white, green-12, green-12),三者互异。`check-02` 实算 commit 白字对实心 = 4.72 ≥ 4.5 |
| 6 | **SC3 / VISUAL-03** — 容器标签「文档区」降级为视觉标签;全屏最大最重的文字不再是它 | ✓ VERIFIED | `style.css:493-498` `#doc-panel-header h1` = `--text-base`(14px)/ `--fw-medium`(500)/ `--color-text-secondary`。item4 层级链严格降序 **28 > 24 > 22 > 14**(整数比较)PASS。`check-06` g2 全页扫描:文档 h1 = 28px,所有其它可见元素最大 = 24px(`P#chat-greeting`),容器标签 = 14px —— **不是断言式声明,是真实浏览器里 `body *` 普查的最大值** |
| 7 | **SC4 / VISUAL-04** — 侧栏当前活动面板可辨认,且 `#ai-panel` 折叠行为不变 | ✓ VERIFIED | `style.css:169` 新令牌 `--color-marker-active`;`style.css:1223-1228` 两条追加规则。item4 三态实读(p1 `#session-panel` / p3 `#annotations-panel` / checking `#checks-panel`)各 4 条断言 PASS,对照组 `#ai-panel .panel-header` 与 `#doc-panel-header` = `none`。`check-06` g3 补几何(遮挡者 0 / 标题贴左缘 10px / 不溢出);**g6 真实执行折叠点击**:`.collapsed` 切换、`display: none`↔`block`、指示器 ▾↔▸、标题行 box-shadow 恒 `none` —— 行为不变量由**执行**的测试覆盖,非结构性推断。`grep -c aiPanel frontend/app.js` = 0,`.collapse-indicator` 在 `style.css` 恰 1 行且 `git diff` 零命中 |
| 8 | **SC5 / VISUAL-05** — 两处标记以内联 SVG 呈现;`frontend/vendor/` 无新增文件;无 CDN `<link>` | ✓ VERIFIED | `style.css:320-321` 两个 data-URI SVG 令牌。我实读 computed `mask-image`:`.annotation-quote::before` 拿到**图钉**路径(`M6 0.6 L8.8 2.2 …`),`.verdict-location::before` 拿到**地图标记**路径(`M6 0 C3.5 0 1.6 1.9 …`)—— 形状与位置**未互换**,两令牌互异(223 vs 319 字符)。`%23` / `fill='` 在围栏内零命中(唯一命中在 `:309` 的注释里)。`ls frontend/vendor/` = 仅 `marked.min.js`;`index.html` 仅一条本地 `<link rel="stylesheet" href="style.css">`,全文 `https?://` 零命中 |
| 9 | **G-idi-05-1 闭合(plan 04)** — `renderMarkdown()` 的全部九个注入目标都解析为契约内的字号档与 600;任何目标不再出现 UA 默认值(32px / 28px),也不再有 700;枚举按调用点且有普查守卫;P-19 / P-20 / A-9 已登记 | ✓ VERIFIED | item7 **38 条断言 / 0 FAIL / 0 BLOCKED**,且**容器全部真实创建**(`created: {5/5 True}`)—— 断言不空过。实测 `.chat-bubble h1` 与 `.event-content h1` 均为 **24px**(UA 默认的 32 / 28 已消失),15 个字重读数全为 600(无 700)。我独立核对 `frontend/app.js`:11 处 `renderMarkdown(`(1 定义 + 10 调用点),接收者映射到**恰好 9 个互异选择器**,与 `MARKDOWN_TARGETS` 一致 —— **普查守卫今日非空转**。UI-SPEC `:844` P-19 / `:845` P-20 / `:871` A-9 / `:1033` 硬规则 9 改写 / `:1136` 05-N-7 均在盘 |

**Score:** 9/9 truths verified (0 present, behavior-unverified)

**注:第 7、9 条是 behavior-dependent truth,且各有**执行**过的行为测试。** 第 7 条由 `check-06` g6 真实点击折叠指示器并断言状态迁移;第 9 条由 item7 用应用自身的 `renderEvent` / `appendChatMessage` / `appendSayToChat` / `renderAnnotations` 先造出五个容器再断言。两者都不是「符号存在 + 接线正确」推断出来的。

### Deferred Items

| # | Item | Addressed In | Evidence |
|---|------|-------------|----------|
| 1 | `idi-04.1-radix` 的 `passed` 指纹 stale(内容真变) | `idi-04.1-radix` 重新验证 | 见 frontmatter `deferred` 与文末 Downstream Obligations |

### Advisory (New Scope, Unevidenced)

见 frontmatter `advisory` 三项(普查守卫锚在计数上;嵌入刻度行高分歧;四处 chrome 标题仍 700)。三项均已实测复现,但均**不构成 must-have 失败** —— 理由逐条写在 `reason` 字段。

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `frontend/style.css` | 唯一改动面:围栏内新声明 + 围栏外排版/层级规则 | ✓ VERIFIED | 本阶段 diff `eaa338f..HEAD` = **+273/-… 行**;新增 5 个令牌(`--text-2xl` / `--text-3xl` / `--color-marker-active` / `--icon-pin` / `--icon-location`),各有消费者。逐行核对 diff:无意外改动 |
| `scripts/check-05-ui-uat.py` | UAT 断言面随需求扩张;新增 `MARKDOWN_TARGETS` 单一事实源 + item7 + 普查守卫 | ✓ VERIFIED | +567 行;item7 存在且**非空转**(见 Truth 9)。旧 D-04 逐字节相同断言已删除并反转为三档断言 |
| `scripts/check-06-idi05-validation.py` | 6 条行为/几何断言(TYPE-01 / SC3 / VISUAL-04 几何 / VISUAL-05 行盒 / VISUAL-01 窄面板 / 折叠点击) | ✓ VERIFIED | 新建文件;我实跑全 6 项:**40 条断言 / 0 FAIL / 0 BLOCKED / exit 0** |
| `.planning/phases/idi-05-…/idi-05-UI-SPEC.md` | P-19 / P-20 / A-9 / 硬规则 9 改写 / 05-N-7 | ✓ VERIFIED | 逐条在盘(行号见 Truth 9) |
| `frontend/app.js` / `index.html` / `frontend/vendor/` / `scripts/ui-states/` | 零 diff | ✓ VERIFIED | `git diff --stat eaa338f..HEAD -- <这四个面>` **为空** |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| `--text-3xl` / `--text-2xl` / `--text-lg` | `.markdown-body h1/h2/h3` | `font-size` 声明 | ✓ WIRED | 各 1 消费者;item4 在四个宿主读到解析值 |
| `--text-xl` / `--text-lg` / `--text-md` + `--fw-semibold` | 五个嵌入目标的 h1/h2/h3 | `style.css:1263-1265` 三条规则 | ✓ WIRED | item7 逐目标读到 computed 值 == 运行时令牌值 |
| `--icon-pin` / `--icon-location` | `.annotation-quote::before` / `.verdict-location::before` | `mask-image`(无前缀 + `-webkit-` 各 1) | ✓ WIRED | computed mask-image 返回对应 data-URI;两令牌互异且**未互换** |
| `--color-marker-active` | 三条 `:not(.hidden) .panel-header` 规则 | `box-shadow: inset 3px 0 0` + `h2 color` | ✓ WIRED | 三态实读语义 box-shadow + 标题 color;对照组 `none` |
| `--color-action-irreversible*` | `#btn-authorize` | `background` / `border-color` / `color` | ✓ WIRED | 围栏外恰 3 行消费者,全在该规则体内(D-15 单消费者不变量成立) |
| `frontend/app.js` 的 10 个 `renderMarkdown(` 调用点 | `MARKDOWN_TARGETS` 的 9 条枚举 | 静态普查守卫 | ✓ WIRED | 我独立映射 11 处出现 → 9 个互异选择器,今日**未**过期(残余弱点见 advisory) |
| `.hidden { display:none !important }` | 三条标记规则的 `:not(.hidden)` | 纯读取既有显隐机制 | ✓ WIRED | CHECK-03(`^\.hidden {` = 1)/ CHECK-04(`!important;` = 1)钉住唯一性;`.hidden` 规则零改动 |

### Data-Flow Trace (Level 4)

纯 CSS 阶段,「数据」是令牌层 → 消费者声明 → 浏览器 computed value → 断言。逐条追踪:

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `.markdown-body h2`(四宿主) | `var(--text-2xl)` | `:root` 围栏 22px | Yes(computed 22px × 4 宿主) | ✓ FLOWING |
| 五个嵌入目标的 h1 | `var(--text-xl)` | 围栏 24px | Yes(computed 24px × 5,容器真实创建) | ✓ FLOWING |
| `#btn-authorize` | `--color-action-irreversible-surface` 等 | 围栏 green-12 / white | Yes(computed + check-02 实算 12.32) | ✓ FLOWING |
| `.annotation-quote::before` / `.verdict-location::before` | `var(--icon-pin)` / `var(--icon-location)` | 围栏 data-URI | Yes(computed mask-image 返回该 data-URI,形状互异) | ✓ FLOWING |
| `.panel-header`(活动) | `var(--color-marker-active)` | 围栏 blue-11 | Yes(computed rgb(13,116,206)) | ✓ FLOWING |

无静态兜底、无硬编码空值、无 mock。**无 HOLLOW_PROP / STATIC / DISCONNECTED。**

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| 令牌一致性(围栏外零裸 hex) | `bash scripts/check-01-token-conformance.sh` | `PASS` / exit 0 | ✓ PASS |
| 对比度清单 | `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`;48 条 PASS 行(47 对 + 1 ORDER);含 `12.32` irreversible、`4.72` commit、`4.65` marker、`ORDER 0.363` | ✓ PASS |
| `.hidden` 唯一性 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` / exit 0 | ✓ PASS |
| `!important` 计数 | `bash scripts/check-04-important-count.sh` | `PASS` / exit 0 | ✓ PASS |
| 样式不变量(直接重导) | `grep -c '^\.hidden {'` / `!important;` / `@media` | **1 / 1 / 0** | ✓ PASS |
| UAT 全项(真实浏览器 computed style) | `.venv/bin/python scripts/check-05-ui-uat.py` | item1 45 / item2 5 / item3 17 / item4 65 / item6 6 / **item7 38** —— 全 0 FAIL / 0 BLOCKED;item5 = 9 断言 / **2 BLOCKED**(两条 `--ai-smoke` 真 AI 调用,默认不执行,见下) | ✓ PASS |
| 九目标标题刻度 | `.venv/bin/python scripts/check-05-ui-uat.py --item 7` | **38 条断言 / 0 FAIL / 0 BLOCKED / exit 0** | ✓ PASS |
| 行为/几何验证 | `.venv/bin/python scripts/check-06-idi05-validation.py` | **6 项全 PASS / 40 断言 / 0 FAIL / 0 BLOCKED / exit 0** | ✓ PASS |
| 全量测试基线 | `.venv/bin/python -m pytest -q` | **219 passed / 6 skipped** —— 与已知基线逐字一致 | ✓ PASS |
| 零 diff 面 | `git diff --stat eaa338f..HEAD -- frontend/app.js frontend/index.html frontend/vendor/ scripts/ui-states/` | 空 | ✓ PASS |
| 04.1 连带结论(HEAD 重算) | `check-02` 输出 | `4.53` text-info / `3.24` 与 `3.15` border-strong / `ORDER 0.363` 全部逐字不变 | ✓ PASS |

**关于 item5 的 2 条 BLOCKED:** 它们是 `--ai-smoke` 才执行的**真实 AI 调用**冒烟项(`处理本轮批注` / `发送`),默认不跑,记 BLOCKED 而非 PASS。它们与 Phase 5 的八条需求无映射(item5 是 plan 03 的 DevTools 抽查,7 条 PASS 已覆盖其目标属性)。**这不是缺陷,也不是本阶段的缺口。**

**关于 `--item 5` 之外我未跑的面:** 无。check-05 的 7 项、check-06 的 6 项、check-01..04、pytest 全部实跑。

### Probe Execution

`find scripts -path '*/tests/probe-*.sh'` 无结果;四份 PLAN 与四份 SUMMARY 里无 `probe-*.sh` 声明。**N/A — 无探针。** (check-06 是行为验证 harness,不是 `scripts/*/tests/probe-*` 约定的探针。)

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| TYPE-01 | 01, 04 | `.markdown-body h1/h2/h3` 显式字号、作用域限定 | ✓ SATISFIED | Truth 1 + Truth 9 |
| TYPE-02 | 01 | table/code/blockquote 归入刻度与令牌 | ✓ SATISFIED | Truth 2 |
| TYPE-03 | 01, 04 | 字重层级 | ✓ SATISFIED | Truth 3 |
| VISUAL-01 | 02 | 不可逆授权独立视觉处理 + 保留令牌 | ✓ SATISFIED | Truth 4 |
| VISUAL-02 | 02 | G1/start-writing 第二档;routine 中性 | ✓ SATISFIED | Truth 5 |
| VISUAL-03 | 02, 04 | 页面级层级,容器标签降级 | ✓ SATISFIED | Truth 6 |
| VISUAL-04 | 03 | 侧栏活动面板可辨 + ai 折叠不变 | ✓ SATISFIED | Truth 7 |
| VISUAL-05 | 03 | 两处 emoji → 内联 SVG,零第三方 | ✓ SATISFIED | Truth 8 |

**ORPHANED requirements:** 无。`.planning/REQUIREMENTS.md:129-136` 把 8 条需求全部映射到 Phase 5,且 8 条都被某份 PLAN 的 `requirements:` 字段认领(01→TYPE-01/02/03;02→VISUAL-01/02/03;03→VISUAL-04/05;04→TYPE-01/TYPE-03/VISUAL-03)。**无未被任何计划认领的 Phase 5 需求。**

**关于「标 Complete 但证据不足」的核查:** 8 条均标 `Complete`。逐条核对后**未发现证据不支持的条目**。需用户知情的两点仍是**口径与机制的登记**,不是证据缺口:(a) VISUAL-04 的原文「四个面板…可区分」经 D-16 收窄为「三选一活动态 + AI 面板折叠态」,`#ai-panel` 无活动标记 —— 用户已在 UAT 第 5 项明确接受;(b) VISUAL-05 的「内联 SVG」按契约 Q7 自身的读法是 CSS 内嵌 data-URI(非 DOM `<svg>`),mask 方案落在同一族内 —— UAT 第 2 项已按渲染结果判过。

### Anti-Patterns Found

**债务标记门:通过。** `TBD` / `FIXME` / `XXX` 在 `frontend/style.css`、`scripts/check-05-ui-uat.py`、`scripts/check-06-idi05-validation.py` 三个改动文件中 **0 命中**;`TODO` / `HACK` 亦 0。

`idi-05-REVIEW.md` 的 12 条发现我逐条独立复核(读代码 + 在真实浏览器里实测),结论如下。**没有任何一条构成 must-have 失败或 BLOCKER。**

| 文件 | 行 | 发现 | 我的判定 | 严重度 |
|------|----|------|----------|--------|
| `scripts/check-05-ui-uat.py` | 278-314 | **WR-01** `check_mask_glyph` 的 `icon_token` 参数只进断言标签,断言本身只证 `mask != none`;两令牌互换可全绿 | **确认**(读码)。我另测:两令牌互异(pin 223 / loc 319 字符)且今日**接线正确**(quote→图钉、verdict→地图标记)。是门的欠规格,不是当日缺陷 | ⚠️ Warning |
| `scripts/check-05-ui-uat.py` | 685-695 等 | **WR-02** 未断言「三个互斥面板恰有一个带竖条」;对照组只覆盖永不匹配的两个 header | **已复现**。在真实 `checking` 状态下移除 `#annotations-panel` 的 `.hidden` 后,`#checks-panel` 与 `#annotations-panel` 的 header **同时**为 `rgb(13,116,206) 3px 0 0 0 inset`,而 `check_marker_control` 的两个选择器仍为 `none` ⇒ 该轮全绿。**是未守护的不变量,不是空转断言** | ⚠️ Warning |
| `scripts/check-05-ui-uat.py` | 906-935 | **WR-03** 普查守卫锚在计数(`== 11` / `== 9`)而非选择器↔调用点绑定 | **确认**(读码)。我独立映射 11 处出现 → 9 个互异选择器,**今日未过期**。残余洞是「保计数的互换」 | ⚠️ Warning → advisory |
| `scripts/check-06-idi05-validation.py` | 127-129 | **WR-04** `.panel-header h2` 缺失时 `sizes[2] > None` 抛 `TypeError`,中止整轮而非记 BLOCKED | **确认**(读码:`px()` 可返 `None`)。当前 fixture 下该元素存在(实读 14px),故**未触发**;但它违反该文件自己写明的「读不到记 BLOCKED」契约 | ⚠️ Warning |
| `scripts/check-06-idi05-validation.py` | 406-408 | **WR-05** `bodyClientW` 是 `clientWidth`(**padding box**),标签却说「面板内容宽」 | **确认**。实测 `#doc-panel-body` padding = 40 + 40 = 80px;g5 自身那轮 `bodyClientW=339` ⇒ 真实内容宽 ≈ **259**,而断言允许到 339。同项的 `lineBoxes == 1` 与 `scrollW <= clientW` 仍带真实信号,故 E3 本身不因此失守 | ⚠️ Warning |
| `frontend/style.css` | 1263-1265 | **WR-06** 嵌入刻度只声明字号/字重,行高按容器继承 | **已实测复现**:文档 h1 = 28px / lh 37.3324px / 行盒 **37.33px**;`.chat-bubble h1` 与 `.say-chunk h1` = 24px / lh **39px** / 行盒 **39px**;`.event-content h1` = 24px / lh `normal` / 行盒 **33px**。即:同一嵌入档在 39px 与 33px 之间摆动,且 `.chat-bubble` 的 h1 **行盒高于**文档 h1。must_have 的判据是字号/字重(28 > 24 成立),CSS 注释亦显式说明不加 line-height 属 D-10 决定 —— 故**不是** must-have 失败,但「嵌入刻度是一个刻度」与实测不符 | ⚠️ Warning → advisory |
| `frontend/style.css` | 636 / 704-708 / 775-779 | **WR-07** 四处 chrome 标题仍计算为 700 | **已实测复现**:`#draft-view > h2` 18/700、`#round-title` 18/700、`#brainstorm-view > h2` 16/700、`.overlay-card h3` 24/700。**但在阶段基线 `eaa338f` 上这四条规则同样未声明 `font-weight`** ⇒ 700 是**既有**继承值,不是本阶段引入;且这四处是 chrome,不在九个渲染目标内,plan 04 的 must_have 把「不再有 700」限定在九个目标内 ⇒ must_have 成立。副作用:文档 h3 由 16 → 18px 后与 `#draft-view > h2` 同尺寸而更轻 | ⚠️ Warning → advisory |
| `scripts/check-06-idi05-validation.py` | 265-266 | **IN-05** 长标题下 `long["shadow"] == base["shadow"]` 比的是静态声明,恒真 | **确认**(读码)。同一 block 的 `h2Delta` / `scrollW` 两条带真实信号,故 g3 整体非空转 | ℹ️ Info |
| `scripts/check-06-idi05-validation.py` | 155-183 | **IN-03** g2 未断言文档 h1 **可见**(`getComputedStyle` 对隐藏元素同样解析) | **确认**(读码)。实测该元素可见且 `max_other = 24px < 28px`,断言今日有信号 | ℹ️ Info |
| `scripts/check-05-ui-uat.py` | 226-232 | **IN-04** `ensure_server()` 复用端口上任何监听者,不确认是 `backend.main:app` | **确认**(读码 + 实跑时反复见到「已在服务 —— 复用」)。读不到时全部记 BLOCKED(fail-closed),但诊断会指向错对象 | ℹ️ Info |
| `scripts/check-05-ui-uat.py` | 1099-1100 | **IN-02** `chain_px` 用 `int()`,非整数 px 抛 `ValueError` 中止 | **确认**(读码)。当前令牌值全为整数 px,未触发 | ℹ️ Info |
| `scripts/check-06-idi05-validation.py` | 399-400 | **IN-01** g5 硬编码 `"16px"` 而标签写「解析值」 | **确认**(读码)。item4 对同一元素用 `resolve_token(page, "--text-md")`,两门会在值层变更时分叉 | ℹ️ Info |
| `frontend/style.css` | 522 | `.collapse-indicator { font-size: 20px; line-height: 1 }` 刻度外字面量 | 用户已裁定为 backlog `999.1`,**本阶段范围外**(D-23);`git diff` 对该行零命中 | ℹ️ Info |

**我没有能证伪的发现:零。** REVIEW 的 12 条我全部复现或读码确认,无一条被推翻 —— 但也**无一条是 must-have 失败**:它们是门的欠规格(Warning)与已登记的机制决定(advisory)。

**关于「空转断言」这一本阶段存在的缺陷类,我的专门核查:** REVIEW 里唯一**恒真**的断言是 IN-05 的 `long["shadow"] == base["shadow"]`(拿静态声明与自己比),它旁边两条断言带真实信号,故 g3 不空转。此外我专门检验了三处最可能空转的地方并**排除**:(a) item7 的五个容器 —— `created` 报告 5/5 True,断言不是对空集合做的;(b) item7 的 `all(w != "700")` —— 源码在 `:1500-1503` 显式把 `None` 路由到 BLOCKED(plan 04 的变异探针修掉的洞),我实跑 15 个读数全非 None;(c) 普查守卫 —— 11 与 9 都是真实计数,我独立复算一致。

### Test Quality Audit

| Test File | Linked Req | Active | Skipped | Circular | Assertion Level | Verdict |
|-----------|-----------|--------|---------|----------|-----------------|---------|
| `scripts/check-05-ui-uat.py` | TYPE-01…03 / VISUAL-01…05 | Yes | 0 | No | Value / Behavioral | PASS(欠规格 3 处,见上) |
| `scripts/check-06-idi05-validation.py` | TYPE-01 / VISUAL-01 / 03 / 04 / 05 | Yes | 0 | No | Behavioral / Geometric | PASS(1 处恒真断言,2 处潜在中止) |
| `scripts/check-02-contrast.py` | VISUAL-01 / VISUAL-04(比值) | Yes | 0 | No | Value(独立 WCAG 公式) | PASS |

**Disabled tests on requirements:** 0 —— 无 `skip` / `xfail` / `.only` 模式。
**Circular patterns detected:** 0 —— `check-05` / `check-06` 读的是真实浏览器渲染真实 CSS 的 `getComputedStyle`(独立 oracle);`check-02` 从围栏令牌值独立算 WCAG。期望值均**不是**被测系统自己产出的(`resolve_token` 解析的是被测 CSS 的令牌,但比值与序关系由独立公式判定)。

### Decision Coverage

All trackable CONTEXT.md decisions are honored by shipped artifacts.(`check.decision-coverage-verify`:total 23 / honored 23 / not_honored [])

### Human Verification Required

**无。** 前一版报告的 6 条人工项已由用户在 `05-UAT.md` 中逐条判过并全部 pass(total 6 / passed 6 / issues 0 / blocked 0):

1. E4/E5 竖条几何可见性 —— pass
2. E6/E7 字形基线对齐 —— pass
3. E8 页面级层级判读 —— pass
4. E3 最窄面板 340px 不换行 —— pass(现另有 `check-06` g5 的机械半边)
5. VISUAL-04 口径收窄(D-16)确认 —— pass
6. `#ai-panel` 折叠点击 —— pass(现另有 `check-06` g6 的真实点击)

我本次独立重导未产生新的人工项:所有 must-have 都有运行时或行为证据,没有一条落在「只能看」的判据上。

### Downstream Obligations (not phase gaps)

**`idi-04.1-radix` 的 `passed` 指纹 stale(D-05)。** 用 `gsd-tools query verification.fingerprint` 在 HEAD 上重算该报告的全部 13 个 covered_files:

```
v1:sha256:301afba60dda25da7a4dbfa35c86fb5dab57772a918ad8ab2c5002de31eda833   (HEAD)
v1:sha256:25d5f1fe52eaceb48939c1bc76bcd44734bb23f035a02b22f0017724475cb5f2   (记录值)
```

**不同 ⇒ 确证 stale。** 成因是内容真变(`frontend/style.css` 与 `scripts/check-05-ui-uat.py` 被本阶段重写),故属**重新验证**而非补指纹。plan 03/04 已在 HEAD 上逐条重算 04.1 的四条守卫与三处结论(全部逐字不变:`ORDER 0.363`、`--color-text-info ON --color-surface-info` 4.53、`--color-border-strong` 3.24 / 3.15;tier-1 25、tier-2 47→48、清单 43→47 三处差值已登记),且**报告文件本身零改动**。

**这是已登记的流程义务,不是本阶段的隐藏缺口,故不进 `gaps:`、不影响 Phase 5 的 goal 判定。** 但它是收口前必须履行的一步:在 04.1 指纹重写之前,`idi-04.1-radix` 的 `passed` 在机械层面不成立。

**另需知情的一处台账:** `05-UAT.md` 的 frontmatter 仍是 `status: diagnosed`,其 `## Gaps` 里 `G-idi-05-1` 仍是 `status: failed`。该缺口已由 plan 04 关闭(见 Truth 9),但 UAT 文件未随之更新。这是台账滞后,不是代码缺陷 —— 归收口流程。

### Gaps Summary

**无阻断性缺口。** 9/9 must-have truths 均 VERIFIED,无 MISSING / STUB 产物,无 NOT_WIRED 关键链接,无债务标记,无未认领需求。四层验证(exists / substantive / wired / data-flow)全部通过。五个改动面之外零 diff。

需要用户知情、但**均不构成缺口**的四类事项:

1. **`idi-04.1-radix` 指纹 stale** —— 已登记的下游义务(见上),归 `/gsd-verify-work idi-04.1-radix`。
2. **REVIEW 的 7 条 Warning** —— 全部实测复现,全部是**门的欠规格**或**已登记的机制决定**,无一条是 must-have 失败。其中三条(WR-03 / WR-06 / WR-07)我已作为 `advisory` 记入 frontmatter,因为它们涉及「门比标签弱」与「措辞与实测不符」,值得在收口时由用户决定是否立项。
3. **`05-UAT.md` 的台账滞后** —— 缺口已闭,文件未更新。
4. **两处已登记的机制偏离** —— 填充步 green-11/12(§S-7 有实算依据:9 步 3.16 ✗、10 步 3.55 ✗、11 步 4.72 ✓、12 步 12.32 ✓)与 mask 机制(§A-2;契约 Q7 本就读作 CSS 内嵌 data-URI)。均不违约。

**关于「哪些是断言、哪些是判断」的坦白:** 字号、字重、坡道三档、层级链、令牌接线、AA 比值、九目标刻度、行盒高度、chrome 标题字重、活动态互斥逃逸 —— **全部是我在真实浏览器里读到的 computed 值或独立复算**,不是对文档的采信。本报告里唯一的**判断项**是 WR-06 / WR-07 的**严重度归类**(Warning 而非 Blocker),其判据是「must_have 是否被证伪」,我已在各自条目里写明判据。

---

_Verified: 2026-09-21T13:25:51Z_
_Verifier: Claude (gsd-verifier)_
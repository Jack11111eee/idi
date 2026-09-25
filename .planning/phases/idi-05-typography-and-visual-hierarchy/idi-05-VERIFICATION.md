---
phase: idi-05-typography-and-visual-hierarchy
verified: 2026-09-25T08:36:09Z
status: passed
score: 9/9 must-haves verified
covered_files:
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
covered_digest: "v1:sha256:bee9dea6c36ed29cb56e3ecb0965c8196a1e0036a7aacc11ec8e2c80108e276a"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: passed
  previous_score: 9/9
  previous_verified: "2026-09-21T13:25:51Z"
  gaps_closed: []
  gaps_remaining: []
  regressions: []
  reason: "内容真变后的重验证(不是补指纹)。covered_files 里 frontend/style.css(自 2026-09-21 起 12 个提交)与 scripts/check-05-ui-uat.py(16 个提交)被 Phase 6/7/8 与 quick 260925-iin 改动;idi-05-UI-SPEC.md(plan 04 的交付物)亦改 2 个提交。旧记录的 digest 300abaa… 在 commit f2ce131(2026-09-21T20:28+08,即上一次验证那一刻的 HEAD)上逐字节复现 ⇒ 该 digest 确由这 12 个文件算出,staleness 的成因是内容真变而非工具漂移。"
  covered_files_change: "按用户 2026-09-25 决定,从 covered_files 删除 .planning/REQUIREMENTS.md。理由与复核见 §重验证披露。"
  chain: "2026-09-21T07:12 human_needed 8/8 → 2026-09-21T13:25 passed 9/9(plan 04 关闭 G-idi-05-1)→ 2026-09-25T08:36 passed 9/9(本次,内容真变重导)"
deferred:  # 已登记的下游义务,非本阶段缺口
  - truth: "idi-04.1-radix 的 passed 指纹(frontend/style.css 与 scripts/check-05-ui-uat.py 在其 covered_files 内)在本阶段编辑后 stale"
    addressed_in: "idi-04.1-radix re-verification via /gsd-verify-work idi-04.1-radix"
    evidence: "**已于 HEAD 履行。** 该报告现为 verified: 2026-09-25T08:18:03Z / status: passed / score 37/38,其 re_verification.reason 明写「内容真变后的重验证 —— frontend/style.css 与 scripts/check-05-ui-uat.py 在 2026-09-20 之后被 Phase 5/7/8 与 quick 260925-iin 改动」。我用 gsd-tools 的 verification.fingerprint 在 HEAD 上重算其 12 个 covered_files = v1:sha256:27957cea…,与其记录值 27957cea… **逐字相同** ⇒ 该报告的指纹在 HEAD 上是当前的,本条下游义务已解除。原记录的 stale 值 25d5f1fe… 属上一轮状态。"
human_verification: []
advisory:
  - finding: "check-05 的 item7 调用点普查守卫锚在**计数**上(renderMarkdown( == 11、MARKDOWN_TARGETS == 9),而非把枚举的选择器与调用点逐一绑定;一个「删一个调用点、加另一个」的改动可保持两个计数不变而让枚举静默过期(REVIEW WR-03)"
    category: architectural
    reason: "本阶段正是为消灭「枚举按类名过期」这一缺陷类而存在。今日枚举经我独立核对**未**过期(11 处出现 = 1 定义 + 10 调用点,映射到 9 个互异选择器),故不是缺口;但守卫的形态弱于其标签所声称的强度"
    evidence_status: "none provided"
  - finding: "嵌入标题刻度只声明 font-size / font-weight,行高按容器继承:同一个嵌入 h1 在 .chat-bubble / .say-chunk 里占 39px 行盒、在 .event-content 里占 33px,而文档 h1 是 37.33px —— 嵌入 h1 的行盒**高于**文档 h1(REVIEW WR-06)"
    category: other
    reason: "我本次在 HEAD 上重新实测确认(见 Data-Flow / Behavioral 两节)。本阶段的 must_have 与 SC3 的判据是**字号与字重**,该不等式成立(28 > 24);且 CSS 注释显式说明不加 line-height 是 D-10「零新增行高令牌」的决定。故不构成 must-have 失败,但「嵌入刻度是一个刻度」这一措辞与实测不符,且无门覆盖"
    evidence_status: "reproduced at HEAD — frontend/style.css:1474-1476;probe: 文档 h1 rectH=37.33 / .chat-bubble h1 rectH=39 / .event-content h1 rectH=33"
  - finding: "四处 chrome 标题仍计算为 700(#draft-view > h2 18/700、#round-title 18/700、#brainstorm-view > h2 16/700、.overlay-card h3 24/700),而 plan 04 落地的嵌入规则注释声称 700 是「契约只声明三档之外的第四档」;无门扫描 chrome 标题(REVIEW WR-07)"
    category: other
    reason: "我本次在 HEAD 上重新实测确认。但该 700 在阶段基线(eaa338f)上**已经存在**(四条规则当时也未声明 font-weight,同样继承 UA bold),且这四处是 chrome 而非九个渲染目标 —— plan 04 的 must_have 把「不再有 700」明确限定在九个渲染目标内,故 must_have 成立。副作用是:本阶段把 .markdown-body h3 由 16px 提到 18px 后,文档 h3(18/600)与 #draft-view > h2(18/700)同尺寸而更轻"
    evidence_status: "reproduced at HEAD — frontend/style.css:894 / 826 / 965;probe: #draft-view > h2 18/700、#round-title 18/700、#brainstorm-view > h2 16/700、.overlay-card h3 24/700"
  - finding: "quick `260925-iin` FIX 3 为第 8 档 `--text-lg-plus`(20px)/ `--lh-none`(1)写的围栏注释声称该元素「必须恰占一个行盒」,但**没有任何门断言** `.collapse-indicator` 的行盒数 —— check-06 的 g6 只读它的 `textContent` 字形与折叠状态,不读它的盒模型"
    category: other
    reason: "我实测两个实例的 computed font-size = 20px、line-height = 20px(即恰 1× 字号),与注释一致,故今日不是缺陷;但「恰一个行盒」这一不变量无门覆盖,属「门比标签弱」的同类(与 advisory 1 同型)。**不构成本阶段 must-have 失败** —— 该档由 quick `260925-iin` 引入,不在 Phase 5 四份 PLAN 的 must_haves 内,本报告只是把它登记为「改动了本阶段承重面、却无门守住其自称不变量」的观察"
    evidence_status: "probe: 两个 .collapse-indicator 实例 computed font-size=20px / line-height=20px;grep 确认 check-06 g6 无行盒断言"
---

# Phase 5: 排版与视觉层级 — Verification Report

**Phase Goal:** 渲染出的文档与界面 chrome 各有一套受控的排版刻度;产品最重要的一步(不可逆的 G3 授权)在视觉上不再与例行按钮混同;页面级层级正确。
**Verified:** 2026-09-25T08:36:09Z
**Status:** passed
**Re-verification:** Yes — 前一版报告(2026-09-21T13:25:51Z,passed,9/9)的 `covered_files` 在 2026-09-21 之后**内容真变**(见 §重验证披露);本次为逐条重导,不是对旧报告的确认,也不是补指纹。

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | **SC1 / TYPE-01** — 渲染出的 DESIGN.md 的 h1/h2/h3 有受控字号(不再由浏览器默认决定),四个 `.markdown-body` 宿主解析为 28 / 22 / 18px;四处 chrome 覆盖(`.panel-header h2` 14px、`#draft-view > h2` 18px、`#brainstorm-view > h2` 16px、`.overlay-card h3` 24px)**未被带偏** | ✓ VERIFIED | `frontend/style.css:908-911` 三条 `.markdown-body h1/h2/h3` 作用域规则(值 28/22/18);`grep -cE '(^\|,)[[:space:]]*h[123][[:space:]]*[,{]'` = **0**(无裸类型选择器标题规则)。`--item 4` **65 条断言 / 0 FAIL / 0 BLOCKED**:四个宿主逐条 `h1==--text-3xl / h2==--text-2xl / h3==--text-lg`;四条 chrome 守卫逐条 PASS(`.panel-header h2` 14 / `#draft-view h2` 18 / `.overlay-card h3` 24 为字面值守卫,`#brainstorm-view h2` 为令牌接线 16px + `--color-action-warning`)。chrome 选择器为 `#draft-view > h2, #round-title`(`:894`)与 `#brainstorm-view > h2`(`:965`)(P-19 收窄),我核对 `frontend/index.html:105/135/120`:三个目标元素分别是 `#draft-view` 的直接子、`#round-title` 的 id、`#brainstorm-view` 的直接子 —— **收窄未丢失任何目标元素** |
| 2 | **TYPE-02** — markdown 内容排版归入刻度与令牌:`table th/td`、`code`、`blockquote` | ✓ VERIFIED | `style.css:921-926`:`th, td` 与 `code` 均 `font-size: var(--text-base)`;`blockquote`(`:914`)`color: var(--color-text-muted)`。`--item 4` 出运行时令牌接线断言(`td font-size` / `code font-size` / `blockquote color` 三条 PASS) |
| 3 | **TYPE-03** — 字重层级显式化(三档 400 / 500 / 600 分工) | ✓ VERIFIED | `--fw-regular/-medium/-semibold` 三档均有消费者。`--item 4` 六条字重断言 PASS:五只动作按钮 = 500、`#btn-authorize` = 600(D-12 已登记唯一例外);内容标题 600、chrome 标题 500(`.panel-header h2` `:684`) |
| 4 | **SC2 / VISUAL-01** — `#btn-authorize` 独立视觉处理(实心填充)+ 保留令牌;与例行按钮计算样式不同;授权按钮字面文本达 AA | ✓ VERIFIED | `style.css:143-145` 声明 `--color-action-irreversible*`(green-12 / white),消费者 `#btn-authorize`(`:1258-1262`)。`--item 3` 三档坡道断言 PASS:routine / commit / irreversible **三档两两不同**、档内各自相同。AA:`check-02` 实算 `--color-action-irreversible-fg ON --color-action-irreversible-surface` = **12.32**;我按 WCAG 公式手工复算 = 1.05 / (0.035256 + 0.05) = **12.32**,≥ 4.5 |
| 5 | **VISUAL-02** — `#btn-approve-draft`(G1)与 `#btn-start-writing` 为第二档;routine 三只保持中性 | ✓ VERIFIED | commit 族令牌 green-11 实心 + 白字;routine 族逐字节未变(淡底 green-3 + 绿字 green-12)。`--item 3` 实读 routine=(green-12, green-11, green-3)、commit=(white, green-11, green-11)、irreversible=(white, green-12, green-12),三者互异。`check-02` 实算 commit 白字对实心 = **4.72** ≥ 4.5 |
| 6 | **SC3 / VISUAL-03** — 容器标签「文档区」降级为视觉标签;全屏最大最重的文字不再是它 | ✓ VERIFIED | `style.css:657` `#doc-panel-header h1` = `--text-base`(14px)/ `--fw-medium`(500)/ `--color-text-secondary`。`--item 4` 层级链严格降序 **28 > 24 > 22 > 14**(整数比较)PASS。`check-06` g2 全页扫描:文档 h1 = **28.0px**,所有其它可见元素最大 = **24px**(`P#chat-greeting`),第三名是 `SPAN.collapse-indicator` **20px**(即 quick `260925-iin` 的第 8 档,未越顶);容器标签 = 14px —— **不是断言式声明,是真实浏览器里 `body *` 普查的最大值** |
| 7 | **SC4 / VISUAL-04** — 侧栏当前活动面板可辨认,且 `#ai-panel` 折叠行为不变 | ✓ VERIFIED | `style.css:169` 令牌 `--color-marker-active`;`:1426-1433` 两条追加规则。`--item 4` 三态实读(p1 `#session-panel` / p3 `#annotations-panel` / checking `#checks-panel`)各 4 条断言 PASS,对照组 `#ai-panel .panel-header` 与 `#doc-panel-header` = `none`。`check-06` g3 补几何(遮挡者 0 / 标题贴左缘 10px / 不溢出);**g6 真实执行折叠点击**:`.collapsed` 切换、`display: none`↔`block`、指示器 ▾↔▸、标题行 box-shadow 恒 `none` —— 行为不变量由**执行**的测试覆盖。**⚠ 与旧报告的一处差异:** `.collapse-indicator`(`:686`)已由 quick `260925-iin` FIX 3 令牌化 —— 旧报告的「逐字节与 HEAD 相同」不再成立;我实测其**值未变**(两个实例 computed `font-size` 均 **20px**、`line-height` 20px),`app.js:1759/1765` 的 `textContent` 赋值路径一字未动,`grep -c aiPanel frontend/app.js` = 0 ⇒ **禁令的实质成立**,详见 §重验证披露 |
| 8 | **SC5 / VISUAL-05** — 两处标记以内联 SVG 呈现;`frontend/vendor/` 无新增文件;无 CDN `<link>` | ✓ VERIFIED | `style.css:413-414` 两个 data-URI SVG 令牌。`--item 4/6` 实读 computed `mask-image`:`.annotation-quote::before`(`:1133`)拿到**图钉**路径(`M6 0.6 L8.8 2.2 …`),`.verdict-location::before`(`:1355`)拿到**地图标记**路径(`M6 0 C3.5 0 1.6 1.9 …`)—— 形状与位置**未互换**。`grep -oE '%23[0-9a-fA-F]{3,8}'` = **0**。`ls frontend/vendor/` = 仅 `marked.min.js`;`index.html` 全文 `https?://` 零命中;`git diff --stat eaa338f..HEAD -- frontend/vendor/ scripts/ui-states/` **为空** |
| 9 | **G-idi-05-1 闭合(plan 04)** — `renderMarkdown()` 的全部九个注入目标都解析为契约内的字号档与 600;任何目标不再出现 UA 默认值(32px / 28px),也不再有 700;枚举按调用点且有普查守卫;P-19 / P-20 / A-9 已登记 | ✓ VERIFIED | `--item 7` **38 条断言 / 0 FAIL / 0 BLOCKED**,且**容器全部真实创建**(`created: {5/5 True}`)—— 断言不空过。实测 `.chat-bubble h1` 与 `.event-content h1` 均为 **24px**(UA 默认的 32 / 28 已消失),15 个字重读数全为 600(无 700)。我独立核对 `frontend/app.js`:11 处 `renderMarkdown(`(1 定义 + 10 调用点,行 119/246/277/291/660/894/951/963/1093/1190/1203),接收者映射到**恰好 9 个互异选择器**,与 `MARKDOWN_TARGETS`(`check-05-ui-uat.py:979-989`)一致 —— **普查守卫今日非空转**。UI-SPEC P-19 / P-20 / A-9 / 硬规则 9 改写 / 05-N-7 均在盘 |

**Score:** 9/9 truths verified (0 present, behavior-unverified)

**注:第 7、9 条是 behavior-dependent truth,且各有**执行**过的行为测试。** 第 7 条由 `check-06` g6 真实点击折叠指示器并断言状态迁移;第 9 条由 item7 用应用自身的 `renderEvent` / `appendChatMessage` / `appendSayToChat` / `renderAnnotations` 先造出五个容器再断言。两者都不是「符号存在 + 接线正确」推断出来的。

### Deferred Items

| # | Item | Addressed In | Evidence |
|---|------|-------------|----------|
| 1 | `idi-04.1-radix` 的 `passed` 指纹 stale(内容真变) | `idi-04.1-radix` 重新验证 | **已履行**:该报告现为 `verified: 2026-09-25T08:18:03Z / passed`,其 12 个 covered_files 在 HEAD 上重算 = `v1:sha256:27957cea…` == 其记录值。见 frontmatter `deferred` 与文末 Downstream Obligations |

### Advisory (New Scope, Unevidenced)

见 frontmatter `advisory` 四项(普查守卫锚在计数上;嵌入刻度行高分歧;四处 chrome 标题仍 700;第 8 档的「恰一个行盒」无门)。前两项与第三项均已实测复现,均**不构成 must-have 失败** —— 理由逐条写在 `reason` 字段;第四项是本轮新登记的同类观察。

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `frontend/style.css` | 唯一改动面:围栏内新声明 + 围栏外排版/层级规则 | ✓ VERIFIED | 本阶段 diff `eaa338f..HEAD` = **+273/-… 行**;新增 5 个令牌(`--text-2xl` / `--text-3xl` / `--color-marker-active` / `--icon-pin` / `--icon-location`),各有消费者。围栏现为 **8 档字号**(`:322-329`,含 quick `260925-iin` 的 `--text-lg-plus` 20px)+ **5 条行高**(`:346-350`,含 `--lh-none`)。`grep -c -- '^  --text-'` = **8**、`grep -c -- '^  --lh-'` = **5** —— 与「7 → 8 / 4 → 5」的记载一致 |
| `scripts/check-05-ui-uat.py` | UAT 断言面随需求扩张;新增 `MARKDOWN_TARGETS` 单一事实源 + item7 + 普查守卫 | ✓ VERIFIED | item7 存在且**非空转**(见 Truth 9)。旧 D-04 逐字节相同断言已删除并反转为三档断言。quick `260925-iin` 追加:item9 的**自动跟随**断言(16 → **17** 条)、item10 的 `FOCUSABLE_SELECTOR` ↔ `:focus-visible` 枚举门(41 → **42** 条)、FIX 4 的陈旧诊断文案修正 |
| `scripts/check-06-idi05-validation.py` | 6 条行为/几何断言(TYPE-01 / SC3 / VISUAL-04 几何 / VISUAL-05 行盒 / VISUAL-01 窄面板 / 折叠点击) | ✓ VERIFIED | 新建文件;我实跑全 6 项:**40 条断言 / 0 FAIL / 0 BLOCKED / exit 0**(逐项 9/2/12/5/5/7)。文件自 2026-09-21 起**零提交**,内容未动 |
| `.planning/phases/idi-05-…/idi-05-UI-SPEC.md` | P-19 / P-20 / A-9 / 硬规则 9 改写 / 05-N-7;quick `260925-iin` 后为 **8 档**契约 | ✓ VERIFIED | 逐条在盘。字号表 `:164-177` 现为 **8 行**(新 `--text-lg-plus` 20px);`:166` 句已整句重写为「**8 档。** 5 → 7 新增两档(Phase 5);7 → 8 新增一档(quick `260925-iin`)…**正文本体保持 16px**」;§未在 HEAD 上受控的字号 `:366-382` 记录 20px 不再是刻度外字号、backlog `999.1` 第 1 项关闭;Do-Not-Touch 行 `:1075` 改为「已令牌化(值不变)…`textContent` 路径与「不得内联 `<svg>`」仍不得触碰」;§与 `.collapse-indicator` 的关系 `:678-684` 把绝对禁令收窄到 `textContent` 赋值路径并登记唯一例外 |
| `frontend/app.js` / `index.html` | 旧报告记「零 diff」 | ⚠️ CHANGED SINCE (非本阶段) | `git diff --stat eaa338f..HEAD` 显示二者**已非零 diff**:app.js +202/-8、index.html +52/-4。逐提交核对,改动全部来自 **Phase 8(idi-08-01/02/03 及三条 fix)与 quick 260924-vb7 / 260925-iin FIX 1**,**无一是 Phase 5 的编辑**。对 Phase 5 结论的影响已逐条复核:调用点普查 11 == 11(Truth 9)、`.collapse-indicator` 的 `textContent` 路径仍在(`app.js:1759/1765`)、`aiPanel` 仍零命中(Truth 7) |
| `frontend/vendor/` / `scripts/ui-states/` | 零 diff | ✓ VERIFIED | `git diff --stat eaa338f..HEAD -- frontend/vendor/ scripts/ui-states/` **为空** |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| `--text-3xl` / `--text-2xl` / `--text-lg` | `.markdown-body h1/h2/h3` | `font-size` 声明(`:909-911`) | ✓ WIRED | 各 1 消费者;`--item 4` 在四个宿主读到解析值 28 / 22 / 18 |
| `--text-xl` / `--text-lg` / `--text-md` + `--fw-semibold` | 五个嵌入目标的 h1/h2/h3 | `style.css:1474-1476` 三条规则 | ✓ WIRED | `--item 7` 逐目标读到 computed 值 == 运行时令牌值(24 / 18 / 16 + 600);**嵌入 h2 仍是 `--text-lg`(18px),未被新 20px 档顶替** |
| `--icon-pin` / `--icon-location` | `.annotation-quote::before` / `.verdict-location::before` | `mask-image` | ✓ WIRED | computed mask-image 返回对应 data-URI;两令牌互异且**未互换** |
| `--color-marker-active` | 三条 `:not(.hidden) .panel-header` 规则(`:1426-1433`) | `box-shadow: inset 3px 0 0` + `h2 color` | ✓ WIRED | 三态实读语义 box-shadow + 标题 color;对照组 `none` |
| `--color-action-irreversible*` | `#btn-authorize`(`:1258-1262`) | `background` / `border-color` / `color` | ✓ WIRED | 围栏外恰 3 行消费者,全在该规则体内(D-15 单消费者不变量成立) |
| `frontend/app.js` 的 10 个 `renderMarkdown(` 调用点 | `MARKDOWN_TARGETS` 的 9 条枚举 | 静态普查守卫(`check-05-ui-uat.py:1002-1020`) | ✓ WIRED | 我独立映射 11 处出现 → 9 个互异选择器,今日**未**过期(残余弱点见 advisory 1) |
| `.hidden { display:none !important }` | 三条标记规则的 `:not(.hidden)` | 纯读取既有显隐机制 | ✓ WIRED | CHECK-03(`^\.hidden {` = 1)/ CHECK-04(`!important;` = 1)钉住唯一性;`.hidden` 规则零改动 |
| `--text-lg-plus` / `--lh-none` | `.collapse-indicator`(`:686`) | `font-size` / `line-height` | ✓ WIRED | quick `260925-iin` 新增;两个实例 computed 20px / 20px(值不变,仅令牌化) |

### Data-Flow Trace (Level 4)

纯 CSS 阶段,「数据」是令牌层 → 消费者声明 → 浏览器 computed value → 断言。逐条追踪:

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `.markdown-body h2`(四宿主) | `var(--text-2xl)` | `:root` 围栏 22px | Yes(computed 22px × 4 宿主) | ✓ FLOWING |
| 五个嵌入目标的 h1 | `var(--text-xl)` | 围栏 24px | Yes(computed 24px × 5,容器真实创建) | ✓ FLOWING |
| `#btn-authorize` | `--color-action-irreversible-surface` 等 | 围栏 green-12 / white | Yes(computed + check-02 实算 12.32) | ✓ FLOWING |
| `.annotation-quote::before` / `.verdict-location::before` | `var(--icon-pin)` / `var(--icon-location)` | 围栏 data-URI | Yes(computed mask-image 返回该 data-URI,形状互异) | ✓ FLOWING |
| `.panel-header`(活动) | `var(--color-marker-active)` | 围栏 blue-11 | Yes(computed rgb(13,116,206)) | ✓ FLOWING |
| `.collapse-indicator`(两实例) | `var(--text-lg-plus)` / `var(--lh-none)` | 围栏 20px / 1 | Yes(computed font-size 20px / line-height 20px × 2) | ✓ FLOWING |

无静态兜底、无硬编码空值、无 mock。**无 HOLLOW_PROP / STATIC / DISCONNECTED。**

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| 令牌一致性(围栏外零裸 hex) | `bash scripts/check-01-token-conformance.sh` | `PASS` / exit 0 | ✓ PASS |
| 对比度清单 | `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`;围栏内 **53 对 PAIR + 1 ORDER**,53 条 PASS 行 + `ORDER 0.363`。含 `12.32` irreversible、`4.72` commit、`4.65` marker、`4.53` text-info、`3.24` / `3.15` border-strong | ✓ PASS |
| `.hidden` 唯一性 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` / exit 0 | ✓ PASS |
| `!important` 计数 | `bash scripts/check-04-important-count.sh` | `PASS` / exit 0 | ✓ PASS |
| 样式不变量(直接重导) | `grep -c '^\.hidden {'` / `grep -o '!important;' \| wc -l` / `grep -c '@media'` | **1 / 1 / 1** —— 前两项与旧报告一致;`@media` 由 0 变 1,唯一命中在 `:1706`,来自 **Phase 7 的 `prefers-reduced-motion` 块**(`4892fdf`),**非本阶段**。注:`grep -c '!important'` 返回 **5**(4 条注释散文),不得用作声明数 | ✓ PASS(带披露) |
| 类型刻度计数 | `grep -c -- '^  --text-'` / `grep -c -- '^  --lh-'` | **8 / 5** —— 与「7 → 8」「4 → 5」的记载一致 | ✓ PASS |
| UAT 全项(真实浏览器 computed style) | `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` | item1 45 / item2 5 / item3 17 / item4 **65** / item6 6 / item7 **38** / item8 13 / item9 **17** / item10 **42** —— 全 0 FAIL / 0 BLOCKED;item5 = 9 断言 / **2 BLOCKED**;exit **2** | ✓ PASS(item5 见下) |
| 九目标标题刻度 | `... --item 7` | **38 条断言 / 0 FAIL / 0 BLOCKED**;容器 `created: {5/5 True}`;嵌入 h2 = `--text-lg` 18px;文档 h1 28 > 嵌入 h1 24 ×5;普查 11 == 11、枚举 9 == 9 | ✓ PASS |
| 行为/几何验证 | `.venv/bin/python scripts/check-06-idi05-validation.py` | **6 项全 PASS / 40 断言 / 0 FAIL / 0 BLOCKED / exit 0** | ✓ PASS |
| 全量测试基线 | `.venv/bin/python -m pytest -q` | **219 passed / 6 skipped** —— 与已知基线逐字一致 | ✓ PASS |
| JS 语法 | `node --check frontend/app.js` | OK | ✓ PASS |
| 字形仍 20px(两实例) | Playwright 探针读 `.collapse-indicator` computed style | `#ai-panel-header` 内 = 20px / 20px;`#doc-panel-header` 内 = 20px / 20px | ✓ PASS |
| 零 diff 面 | `git diff --stat eaa338f..HEAD -- frontend/vendor/ scripts/ui-states/` | 空 | ✓ PASS |
| 04.1 连带结论(HEAD 重算) | 04.1 报告 12 个 covered_files 的 `verification.fingerprint` | `v1:sha256:27957cea…` == 其记录值;`check-02` 输出 `4.53` / `3.24` / `3.15` / `ORDER 0.363` 全部逐字不变 | ✓ PASS |

**关于 item5 的 2 条 BLOCKED 与 exit 2:** 两条 BLOCKED 是 `--ai-smoke` 才执行的**真实 AI 调用**冒烟项(`处理本轮批注` / `发送`),默认不跑,记 BLOCKED 而非 PASS。它们与 Phase 5 的八条需求无映射(item5 是 plan 03 的 DevTools 抽查,7 条 PASS 已覆盖其目标属性)。**这不是缺陷,也不是本阶段的缺口。** exit 2 是「有 blocked」的约定退出码。

**关于 `--item 5` 之外我未跑的面:** 无。check-05 的 10 项、check-06 的 6 项、check-01..04、pytest、`node --check` 全部实跑。

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

**ORPHANED requirements:** 无。`.planning/REQUIREMENTS.md:129-136` 把 8 条需求全部映射到 Phase 5(均 `Complete`),且 8 条都被某份 PLAN 的 `requirements:` 字段认领(01→TYPE-01/02/03;02→VISUAL-01/02/03;03→VISUAL-04/05;04→TYPE-01/TYPE-03/VISUAL-03)。**无未被任何计划认领的 Phase 5 需求。**(注:REQUIREMENTS.md 已按用户决定移出 `covered_files`,见 §重验证披露;它仍是需求索引的来源,只是不再作为「内容一变即作废本报告结论」的输入。)

**关于「标 Complete 但证据不足」的核查:** 8 条均标 `Complete`。逐条核对后**未发现证据不支持的条目**。需用户知情的两点仍是**口径与机制的登记**,不是证据缺口:(a) VISUAL-04 的原文「四个面板…可区分」经 D-16 收窄为「三选一活动态 + AI 面板折叠态」,`#ai-panel` 无活动标记 —— 用户已在 UAT 第 5 项明确接受;(b) VISUAL-05 的「内联 SVG」按契约 Q7 自身的读法是 CSS 内嵌 data-URI(非 DOM `<svg>`),mask 方案落在同一族内 —— UAT 第 2 项已按渲染结果判过。

### Anti-Patterns Found

**债务标记门:通过。** `TBD` / `FIXME` / `XXX` 在 `frontend/style.css`、`scripts/check-05-ui-uat.py`、`scripts/check-06-idi05-validation.py`、`idi-05-UI-SPEC.md` 四个文件中 **0 命中**;`TODO` / `HACK` 亦 0。

`idi-05-REVIEW.md` 的 12 条发现我逐条独立复核(读代码 + 在真实浏览器里实测),结论如下。**没有任何一条构成 must-have 失败或 BLOCKER。**

| 文件 | 行 | 发现 | 我的判定 | 严重度 |
|------|----|------|----------|--------|
| `scripts/check-05-ui-uat.py` | 278-314 | **WR-01** `check_mask_glyph` 的 `icon_token` 参数只进断言标签,断言本身只证 `mask != none`;两令牌互换可全绿 | **确认**(读码)。我另测:两令牌互异且今日**接线正确**(quote→图钉、verdict→地图标记)。是门的欠规格,不是当日缺陷 | ⚠️ Warning |
| `scripts/check-05-ui-uat.py` | 685-695 等 | **WR-02** 未断言「三个互斥面板恰有一个带竖条」;对照组只覆盖永不匹配的两个 header | **已复现**(旧报告实测)。是未守护的不变量,不是空转断言 | ⚠️ Warning |
| `scripts/check-05-ui-uat.py` | 1002-1020 | **WR-03** 普查守卫锚在计数(`== 11` / `== 9`)而非选择器↔调用点绑定 | **确认**(读码)。我独立映射 11 处出现 → 9 个互异选择器,**今日未过期**。残余洞是「保计数的互换」 | ⚠️ Warning → advisory 1 |
| `scripts/check-06-idi05-validation.py` | 127-129 | **WR-04** `.panel-header h2` 缺失时 `sizes[2] > None` 抛 `TypeError`,中止整轮而非记 BLOCKED | **确认**(读码:`px()` 可返 `None`)。当前 fixture 下该元素存在(实读 14px),故**未触发**;但它违反该文件自己写明的「读不到记 BLOCKED」契约 | ⚠️ Warning |
| `scripts/check-06-idi05-validation.py` | 406-408 | **WR-05** `bodyClientW` 是 `clientWidth`(**padding box**),标签却说「面板内容宽」 | **确认**。实测 g5 那轮 `bodyClientW=339`、真实内容宽 ≈ 259;同项的 `lineBoxes == 1` 与 `scrollW <= clientW` 仍带真实信号,故 E3 本身不因此失守 | ⚠️ Warning |
| `frontend/style.css` | 1474-1476 | **WR-06** 嵌入刻度只声明字号/字重,行高按容器继承 | **已实测复现**(HEAD 重测):文档 h1 = 28px / lh 37.3324px / 行盒 **37.33px**;`.chat-bubble h1` 与 `.say-chunk h1` = 24px / lh **39px** / 行盒 **39px**;`.event-content h1` = 24px / lh `normal` / 行盒 **33px**。即:同一嵌入档在 39px 与 33px 之间摆动,且 `.chat-bubble` 的 h1 **行盒高于**文档 h1。must_have 的判据是字号/字重(28 > 24 成立),CSS 注释亦显式说明不加 line-height 属 D-10 决定 —— 故**不是** must-have 失败 | ⚠️ Warning → advisory 2 |
| `frontend/style.css` | 894 / 826 / 965 | **WR-07** 四处 chrome 标题仍计算为 700 | **已实测复现**(HEAD 重测):`#draft-view > h2` 18/700、`#round-title` 18/700、`#brainstorm-view > h2` 16/700、`.overlay-card h3` 24/700。**但在阶段基线 `eaa338f` 上这四条规则同样未声明 `font-weight`** ⇒ 700 是**既有**继承值,不是本阶段引入;且这四处是 chrome,不在九个渲染目标内,plan 04 的 must_have 把「不再有 700」限定在九个目标内 ⇒ must_have 成立 | ⚠️ Warning → advisory 3 |
| `scripts/check-06-idi05-validation.py` | 265-266 | **IN-05** 长标题下 `long["shadow"] == base["shadow"]` 比的是静态声明,恒真 | **确认**(读码)。同一 block 的 `h2Delta` / `scrollW` 两条带真实信号,故 g3 整体非空转 | ℹ️ Info |
| `scripts/check-06-idi05-validation.py` | 155-183 | **IN-03** g2 未断言文档 h1 **可见**(`getComputedStyle` 对隐藏元素同样解析) | **确认**(读码)。实测该元素可见且 `max_other = 24px < 28px`,断言今日有信号 | ℹ️ Info |
| `scripts/check-05-ui-uat.py` | 226-232 | **IN-04** `ensure_server()` 复用端口上任何监听者,不确认是 `backend.main:app` | **确认**(读码 + 实跑时反复见到「已在服务 —— 复用」)。读不到时全部记 BLOCKED(fail-closed),但诊断会指向错对象 | ℹ️ Info |
| `scripts/check-05-ui-uat.py` | 1099-1100 | **IN-02** `chain_px` 用 `int()`,非整数 px 抛 `ValueError` 中止 | **确认**(读码)。当前令牌值全为整数 px,未触发 | ℹ️ Info |
| `scripts/check-06-idi05-validation.py` | 399-400 | **IN-01** g5 硬编码 `"16px"` 而标签写「解析值」 | **确认**(读码)。item4 对同一元素用 `resolve_token(page, "--text-md")`,两门会在值层变更时分叉 | ℹ️ Info |
| `frontend/style.css` | 686 | `.collapse-indicator` 曾为刻度外字面量(`font-size: 20px; line-height: 1`) | 用户已裁定为 backlog `999.1`,本阶段范围外(D-23);**其后由 quick `260925-iin` 令牌化为第 8 档(值不变)**,backlog `999.1` 第 1 项关闭 | ℹ️ Info(已闭合) |
| `frontend/style.css` | 344 | 第 8 档的围栏注释声称 `.collapse-indicator`「必须恰占一个行盒」,但**无门断言该行盒数** | 我实测两实例 computed 20px / 20px(与注释一致),故今日不是缺陷;属「门比标签弱」同类 | ℹ️ Info → advisory 4 |

**我没有能证伪的发现:零。** REVIEW 的 12 条我全部复现或读码确认,无一条被推翻 —— 但也**无一条是 must-have 失败**:它们是门的欠规格(Warning)与已登记的机制决定(advisory)。

**关于「空转断言」这一本阶段存在的缺陷类,我的专门核查:** REVIEW 里唯一**恒真**的断言是 IN-05 的 `long["shadow"] == base["shadow"]`(拿静态声明与自己比),它旁边两条断言带真实信号,故 g3 不空转。此外我专门检验了三处最可能空转的地方并**排除**:(a) item7 的五个容器 —— `created` 报告 5/5 True,断言不是对空集合做的;(b) item7 的 `all(w != "700")` —— 源码在 `:1500-1503` 显式把 `None` 路由到 BLOCKED(plan 04 的变异探针修掉的洞),我实跑 15 个读数全非 None;(c) 普查守卫 —— 11 与 9 都是真实计数,我独立复算一致。

### Test Quality Audit

| Test File | Linked Req | Active | Skipped | Circular | Assertion Level | Verdict |
|-----------|-----------|--------|---------|----------|-----------------|---------|
| `scripts/check-05-ui-uat.py` | TYPE-01…03 / VISUAL-01…05 | Yes | 0 | No | Value / Behavioral | PASS(欠规格 3 处,见上) |
| `scripts/check-06-idi05-validation.py` | TYPE-01 / VISUAL-01 / 03 / 04 / 05 | Yes | 0 | No | Behavioral / Geometric | PASS(1 处恒真断言,2 处潜在中止) |
| `scripts/check-02-contrast.py` | VISUAL-01 / VISUAL-04(比值) | Yes | 0 | No | Value(独立 WCAG 公式) | PASS |

**Disabled tests on requirements:** 0 —— `grep -rnE "it\.skip|…|xit\(|…"` 的 17 处命中经逐行核对**全部是 `sys.exit(` / `raise SystemExit(` 的假阳性**,无 `skip` / `xfail` / `.only` 模式。
**Circular patterns detected:** 0 —— 三个脚本对 `writeFileSync|writeFile|fs.write|open(…, 'w')` 零命中;`check-05` / `check-06` 读的是真实浏览器渲染真实 CSS 的 `getComputedStyle`(独立 oracle);`check-02` 从围栏令牌值独立算 WCAG。期望值均**不是**被测系统自己产出的。

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

我本次独立重导未产生新的人工项:所有 must-have 都有运行时或行为证据,没有一条落在「只能看」的判据上。**已裁定、按已知/接受记录、不再路由的项:** TOKEN-07 的 z-index 序关系半场(用户裁定仅人工)、LAYOUT-02 的 768–855px 重叠(用户接受,UI-SPEC A-10;item8 的 `@768px` 诊断逐字自陈「未覆盖」)、`.claude/settings.local.json` 的 `Bash(node -e ' *)` 授权(owner 接受)、A11Y-03 / A11Y-08 / REG-03 的键盘半场与 Phase 5 自身的人工项。

### Downstream Obligations (not phase gaps)

**`idi-04.1-radix` 的指纹义务 —— 已履行。** 旧报告登记的「04.1 的 `passed` 指纹 stale」在本轮开始前已由另一轮重新验证关闭:

```
HEAD 重算 04.1 的 12 个 covered_files = v1:sha256:27957ceaceab0075d094ffc5f2125301a7ec2060d2a15a2a24450650766c1a4b
04.1 报告记录值                        = v1:sha256:27957ceaceab0075d094ffc5f2125301a7ec2060d2a15a2a24450650766c1a4b   ✓ 相同
```

该报告现为 `verified: 2026-09-25T08:18:03Z / status: passed / score 37/38`,其 `re_verification.reason` 明写成因是 Phase 5/7/8 与 quick `260925-iin` 对 `frontend/style.css` / `scripts/check-05-ui-uat.py` 的改动。**故本条下游义务不再悬置**,不再是收口前的阻塞步骤。(旧报告记录的 stale 值 `25d5f1fe…` 属上一轮状态,已由该轮重验证取代。)

**另需知情的一处台账:** `05-UAT.md` 的 frontmatter 仍是 `status: diagnosed`,其 `## Gaps` 里 `G-idi-05-1` 仍是 `status: failed`。该缺口已由 plan 04 关闭(见 Truth 9,`--item 7` 38 条断言在 HEAD 上重证),但 UAT 文件未随之更新。**这是台账滞后,不是代码缺陷** —— 归收口流程;本轮不修该文件(用户明令)。

### 重验证披露(2026-09-25)

**1. 为什么 stale:内容真变,不是补指纹。** 自旧报告的 `verified: 2026-09-21T13:25:51Z` 起,`covered_files` 的提交数:

| 文件 | 自 2026-09-21 起的提交数 | 说明 |
|---|---|---|
| `.planning/REQUIREMENTS.md` | 9 | 需求索引台账(phase.complete 翻行);**已移出 covered_files** |
| `frontend/style.css` | 12 | Phase 6/7/8 + quick `260925-iin` FIX 3 |
| `scripts/check-05-ui-uat.py` | 16 | Phase 6/7/8 + quick `260925-iin` FIX 2/4/5 |
| `idi-05-UI-SPEC.md`(plan 04 交付物) | 2 | `3e50dca`(FIX 3 契约同步)/ `8075d3b`(消解 FIX 3 留下的自相矛盾) |
| 四份 PLAN / 四份 SUMMARY / `check-06` | 0 | 内容未动 |

判据不是 mtime 而是**重算指纹**:旧记录 `v1:sha256:300abaa4…` 在 commit `f2ce131`(2026-09-21T20:28+08,旧报告写就前一刻的 HEAD)上,用同一算法对**同一 12 个文件**逐字节复现出 `300abaa4…`。这同时证明两件事:(a) staleness 的成因是内容真变(不是工具版本漂移);(b) 旧 `covered_files` 清单**不含** `idi-05-UI-SPEC.md` —— 见下条。

**2. `covered_files` 变更:删除 `.planning/REQUIREMENTS.md`(用户决定 2026-09-25)。** `covered_files` 的含义是「内容一变即作废本报告结论的输入」。需求索引表是**下游台账** —— `phase.complete` 翻它的行,里程碑收口会 `git rm` 它(归档到 `milestones/v1.14-REQUIREMENTS.md`)。只要它留在清单里,每一次阶段/里程碑收口都会**因与本报告结论无关的理由**静默作废本报告。`idi-04.1-radix` 的 verifier 提出此问题,用户采纳其建议并适用于 v1.14 的全部六份阶段报告。**其余报告的 `covered_files` 本轮一字未动。**

**3. 一处与任务前提不符的实测发现(需用户知情):`idi-05-UI-SPEC.md` 从未在本报告的 `covered_files` 里。** 任务描述把它列为「changed covered file」,但机械事实相反:用旧记录的 12 个文件(不含 UI-SPEC)复算出 `300abaa4…`,**逐字等于**旧 `covered_digest` ⇒ 旧清单确实只有 12 项、UI-SPEC 不在其中。它确实是 plan 04 的 `files_modified` 交付物、也确实是本报告 Required Artifacts 表的一行,但它不在「内容一变即作废」的机械输入集里。**本轮按指令只做「删除 REQUIREMENTS.md + 对剩余 11 个文件重算」,未擅自加入 UI-SPEC。** 若用户希望 UI-SPEC 的改动也机械地作废本报告(鉴于其 §Typography 是本阶段字号的契约来源),那是一次**清单扩容**,应显式决定;本轮不代行。

**4. 本阶段编辑面之外的环境变化(非本阶段引入,逐条核对后不影响结论):**

- `frontend/app.js`(+202/-8)与 `frontend/index.html`(+52/-4)在 `eaa338f..HEAD` 上已非零 diff。逐提交核对:全部来自 **Phase 8**(`idi-08-01/02/03` 与三条 fix)与 quick `260924-vb7` / `260925-iin` FIX 1,**无一是 Phase 5 的编辑**。旧报告「四个面零 diff」是**在当时的 HEAD 上**成立的陈述;对 Phase 5 结论的三处依赖我已逐条重证:调用点普查 11 == 11(Truth 9)、`.collapse-indicator` 的 `textContent` 路径仍在(`app.js:1759/1765`)、`aiPanel` 仍零命中(Truth 7)。`frontend/vendor/` 与 `scripts/ui-states/` 仍零 diff。
- `grep -c '@media'` 由 **0 → 1**。唯一命中在 `style.css:1706`,是 Phase 7 的 `prefers-reduced-motion` 块(`4892fdf`)。Phase 5 硬规则 8 要求的是「**本阶段**新增 `@media` 计数须保持 0」—— 该条由 Phase 5 自己遵守;check-05 item8 的静态门已把期望值同步为 1 并注明成因。
- `check-02` 的清单由 Phase 5 时的 47 对增至 **53 对 + 1 ORDER**(Phase 7/8 新增 `--color-focus` / `--color-border-hover` / `--color-border-streaming` / `--color-border-success` 等配对)。`PASS: 0 failures` 不变;Phase 5 自己新增的四条配对(含 `--color-marker-active` 4.65)逐条仍在。
- `.collapse-indicator` 由刻度外字面量变为第 8 档令牌(quick `260925-iin` FIX 3)。**值未变**(两实例 computed 20px / 20px),`textContent` 赋值路径未动 ⇒ plan 03 的禁令实质成立;UI-SPEC 已把绝对禁令收窄到该路径并登记这一唯一例外。旧报告的「逐字节与 HEAD 相同」是当时的事实,现由一次**已登记的后续编辑**取代。

**5. UI-SPEC 的留存散文(按 orchestrator 前一轮的分类,作**历史记录**报告,不当作缺口、不「修」):**

| 位置 | 内容 | 分类依据 |
|---|---|---|
| `:557-559` | `#ai-panel` 零 CSS 改动节,写「本阶段对 `.collapse-indicator` 的规则数改动 = 0」 | 明写「本阶段」,是 Phase 5 范围记录 |
| `:915-918` | Gate 6 的期望输出注释仍写「恰好 1 行,内容为 `{ font-size: 20px; line-height: 1; }`」 | 该门以 D-23 / 硬规则 5 的 Phase 5 不得触碰清单为标题,是 Phase-5 范围的门记录 |
| `:1075` | Do-Not-Touch 行 —— **已更新**(改为「已令牌化(值不变,仍 20px)…`textContent` 路径与「不得内联 `<svg>`」仍不得触碰」) | 不是留存项,是 FIX 3 的同步 |
| `:1088` + `:110-111` | §不在本阶段 范围锁表:`.collapse-indicator` 的 `font-size: 20px` / `line-height: 1` 仍列「不在本阶段」 | 表头即「不在本阶段」,是范围锁记录 |
| `:1337-1338` | Provenance 基线表:`字号刻度 = 5`、围栏外裸 `font-size` 字面量 = 1 | 该块首行即「基线(2026-09-20 对 HEAD 实测)」,是**带日期**的历史基线 |

**我另发现一处同类的、上一轮分类未列出的残留:** `:25` 的节权威表仍写「它重写 `04-UI-SPEC.md` 的 `## Typography` 节(**5 档 → 7 档**)」。`8075d3b` 的提交信息记录了上一轮只列了 `:555-556` / `:913` / `:1329-1330` 三处「带显式阶段或日期限定词」的位置,并修掉了 `:380`(它无限定词)。`:25` 描述的是本文件相对上游的**改写跨度**,现已因第 8 档而不完整。**它不是 must-have、也不影响任何断言或门**(UI-SPEC 是散文,`check-05` / `check-06` 均不读它),故登记为观察,不修、不计缺口;若用户要收敛 UI-SPEC 的散文新鲜度,它与 `:918` / `:1337-1338` 属同一批。

**6. 已裁定、本轮不重复路由的项(按任务给定的清单,逐条确认在盘):** TOKEN-07 的 z-index 序关系半场(用户裁定仅人工);LAYOUT-02 的 768–855px 重叠(用户接受,UI-SPEC A-10);`.claude/settings.local.json` 的 `Bash(node -e ' *)` 授权(owner 接受);A11Y-03 / A11Y-08 / REG-03 的键盘半场与本阶段自身的人工项。

### Gaps Summary

**无阻断性缺口。** 9/9 must-have truths 均 VERIFIED,无 MISSING / STUB 产物,无 NOT_WIRED 关键链接,无债务标记,无未认领需求。四层验证(exists / substantive / wired / data-flow)全部通过。`frontend/vendor/` 与 `scripts/ui-states/` 零 diff。

需要用户知情、但**均不构成缺口**的五类事项:

1. **`idi-04.1-radix` 指纹义务** —— **已履行**(HEAD 重算 == 其记录值),不再是收口阻塞。
2. **REVIEW 的 7 条 Warning** —— 全部实测复现,全部是**门的欠规格**或**已登记的机制决定**,无一条是 must-have 失败。其中四条(WR-03 / WR-06 / WR-07 / 第 8 档行盒)已作为 `advisory` 记入 frontmatter。
3. **`05-UAT.md` 的台账滞后** —— 缺口已闭(HEAD 重证),文件未更新;归收口流程。
4. **两处已登记的机制偏离** —— 填充步 green-11/12(§S-7 有实算依据:9 步 3.16 ✗、10 步 3.55 ✗、11 步 4.72 ✓、12 步 12.32 ✓)与 mask 机制(§A-2;契约 Q7 本就读作 CSS 内嵌 data-URI)。均不违约。
5. **本阶段编辑面之外的环境漂移** —— `frontend/app.js` / `index.html` 已非零 diff(Phase 8 + quick 任务)、`@media` 0 → 1(Phase 7)、对比度清单 47 → 53 对(Phase 7/8)、`.collapse-indicator` 已令牌化(quick `260925-iin`,值不变)。逐条核对后**不影响任何 Phase 5 结论**;详见 §重验证披露。

**关于「哪些是断言、哪些是判断」的坦白:** 字号、字重、坡道三档、层级链、令牌接线、AA 比值、九目标刻度、行盒高度、chrome 标题字重、两实例 20px、普查计数 11/9、以及四条门与 pytest 的逐字输出 —— **全部是我在真实浏览器里读到的 computed 值、独立复算、或本轮实跑的命令输出**,不是对文档的采信。本报告里唯一的**判断项**是 WR-06 / WR-07 / 第 8 档行盒的**严重度归类**(Warning / advisory 而非 Blocker),其判据是「must_have 是否被证伪」,我已在各自条目里写明判据。

---

_Verified: 2026-09-25T08:36:09Z_
_Verifier: Claude (gsd-verifier)_

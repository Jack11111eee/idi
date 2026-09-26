---
status: diagnosed
phase: 05-typography-and-visual-hierarchy
source: [05-VERIFICATION.md]
started: 2026-09-21T07:12:16Z
updated: 2026-09-21T16:40:00Z
audit_acknowledged:
  milestone: v1.14
  at: 2026-09-25
  gap_snapshot: "diagnosed::scenarios=0"
---

## Current Test

[testing complete]

## Tests

### 1. E4/E5 —— 活动面板的 3px 蓝竖条在三个样本下真实可见

expected: 在 p1(会话流)/ p3(本轮批注流)/ checking(自检报告)三个样本下,活动面板标题行左侧的 3px 蓝竖条**真实可见**:不被标题行内元素盖住、不因 `border-radius` 在角落断开、标题文本变长时仍贴左缘。非活动面板、`#ai-panel`、`#doc-panel-header` 均无竖条。
result: pass

### 2. E6/E7 —— 两个 12×12 mask 字形与相邻文字的基线视觉对齐

expected: `.annotation-quote::before`(实心图钉)与 `.verdict-location::before`(实心地图标记)与首行文字**视觉齐平**,折行时不漂移,且**不撑高行盒**(行高仍由 `--lh-snug` / `--lh-reading` 决定)。
result: pass

### 3. E8 —— 页面级层级「读起来」成立

expected: 全屏最大最重的文字是**文档自己的 h1**,不是容器标签「文档区」;三级标题层级分明、不互相淹没。字号半边已由运行时断言钉死(28 > 24 > 22 > 14),此项判「读起来是否分明」。
result: pass

### 4. E3 —— 最窄面板下 `#btn-authorize` 文本不换行不裁切

expected: 在 `--doc-panel-w` 最窄值 340px(内容宽约 260px)下,「授权撰写总设计文档」在 16px 下**单行显示,不换行不裁切**。计划的算术(标签约 144px + padding-x 32px ≈ 176px < 260px)成立,但 check-05 不把面板压到 340px 实测。
result: pass

### 5. VISUAL-04 口径确认 —— `#ai-panel` 不参与「三选一活动态」推导

expected: 人工确认 REQUIREMENTS 的「侧栏四个面板…可区分」按 D-16 的**「三选一活动态 + AI 面板折叠态」**口径被接受(`#ai-panel` 从不被 `.hidden`,其可辨状态是既有的 ▾/▸ 折叠指示器)。若要求给 AI 面板也加活动标记,那是**新的范围**,不是本阶段的缺陷。
result: pass

### 6. `#ai-panel` 折叠点击穿透

expected: 点击 `#ai-panel` 的折叠指示器,`#ai-panel-body` 的 `.collapsed` 切换正常、指示器字形切换正常、标题行**不出现竖条**。本阶段对 `app.js` / `index.html` / `.collapse-indicator` 零 diff,check-05 的对照组也已断言 `#ai-panel .panel-header box-shadow == none`,故行为「按构造不变」是结构性证明 —— 此项只补一次低成本人工点击。
result: pass

## Summary

total: 6
passed: 6
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

<!-- Source: idi-05-UI-REVIEW.md BLOCKER (Top Fix 1), independently re-verified by the
     orchestrator on 2026-09-21 before being recorded as a gap. Not a UAT test failure —
     all 6 UAT tests passed; this gap comes from the verify:post ui-review hook. -->

- gap_id: G-idi-05-1
  truth: "页面级层级正确:文档自己的 h1 是全屏最大最重的文字,且字号/字重刻度在**所有** markdown 渲染目标上受控(SC3 / E2 / UI-SPEC 三级层级链)"
  status: failed
  reason: "UI audit finding (verified by orchestrator): renderMarkdown() 的返回值被注入五个**非** .markdown-body 容器,这些容器里没有任何规则给 h1/h2/h3 定尺寸,故回落 UA 默认值 —— .chat-bubble(16px 上下文)里 `#` 渲染为 32px/700,.event-content(14px 上下文)里为 28px/700,均超过 .markdown-body h2(22px)与文档 h1(28px);同时第 4 个字重档 700 进入应用,违背契约声明的三档(400/500/600)"
  severity: blocker
  test: null            # 非 UAT 测试产出;来源为 verify:post ui-review
  source: "idi-05-UI-REVIEW.md Top Fix 1 (BLOCKER)"
  root_cause: "标题尺寸规则只存在于 .markdown-body 作用域内(style.css:719-721 是唯一给 h1/h2/h3 定 font-size 的规则;全文件无任何非 .markdown-body 的标题尺寸规则)。renderMarkdown()(app.js:112)返回真实 <h1>/<h2>/<h3>,但被注入的五个容器不含 .markdown-body: .event-content(app.js:239)、.chat-bubble(app.js:270)、.say-chunk(app.js:284)、.annotation-note(app.js:1144)、.annotation-answer-body(app.js:1157)。index.html 中 .markdown-body 只出现在 4 个元素上(#latest-check :47 / #draft-content :113 / #brainstorm-content :121 / #round-doc :139),app.js 从不给其它元素加该类。check-05 的 MARKDOWN_HOSTS 常量(check-05-ui-uat.py:868)恰好只枚举这 4 个 .markdown-body 宿主 —— 与本阶段 plan 01 已登记的教训同型:「单宿主探针是缺陷存活的直接原因」。"
  artifacts:
    - path: "frontend/style.css"
      issue: "标题尺寸规则仅存在于 .markdown-body 作用域(:719-721);五个非 .markdown-body 渲染目标无任何标题尺寸/字重规则"
    - path: "frontend/app.js"
      issue: "renderMarkdown() 的输出注入五个非 .markdown-body 容器(:239 / :270 / :284 / :1144 / :1157);本阶段对其零 diff,故修复需触及该文件的容器类名或由 CSS 侧覆盖"
    - path: "scripts/check-05-ui-uat.py"
      issue: "MARKDOWN_HOSTS(:868)只枚举 4 个 .markdown-body 宿主,不含五个真实渲染目标 —— 这是本缺陷能存活到验证后的直接原因"
    - path: ".planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md"
      issue: "契约的 off-scale 枚举与 Deliberate Delta Ledger 未列出这五个容器,也未登记 UA 默认值回落"
  missing:
    - "把标题刻度作用域扩展到五个真实渲染目标(可加共享类 .md-scope,或在 style.css 侧列举五组选择器),使 h1/h2/h3 在其中解析为契约内的字号档与 --fw-semibold,消除第 4 个字重档 700"
    - "把 check-05 的 MARKDOWN_HOSTS 从「4 个 .markdown-body 宿主」扩为「全部 renderMarkdown 渲染目标」,逐个断言;枚举须按影响面(renderMarkdown 的调用点)而非按类名"
    - "在 UI-SPEC 的 Deliberate Delta Ledger 补 P-19:本阶段中途的 chrome 选择器收窄(#draft-view h2, #rounds-placeholder h2 → #draft-view > h2, #round-title;#brainstorm-view h2 → #brainstorm-view > h2),并在 :805 的零列表里除外"
  diagnosis_method: "orchestrator direct verification (grep + file:line + git base-commit comparison); no debug subagent spawned — root cause was already established with certainty and re-verified, so a re-diagnosis pass would have added cost without information"
  debug_session: ""

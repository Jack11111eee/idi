---
status: testing
phase: 05-typography-and-visual-hierarchy
source: [05-VERIFICATION.md]
started: 2026-09-21T07:12:16Z
updated: 2026-09-21T07:12:16Z
---

## Current Test

number: 1
name: E4/E5 —— 活动面板的 3px 蓝竖条在三个样本下真实可见
expected: |
  三条竖条在各自样本下完整可见;非活动面板与 #ai-panel / #doc-panel-header 无竖条
awaiting: user response

## Tests

### 1. E4/E5 —— 活动面板的 3px 蓝竖条在三个样本下真实可见
expected: 在 p1(会话流)/ p3(本轮批注流)/ checking(自检报告)三个样本下,活动面板标题行左侧的 3px 蓝竖条**真实可见**:不被标题行内元素盖住、不因 `border-radius` 在角落断开、标题文本变长时仍贴左缘。非活动面板、`#ai-panel`、`#doc-panel-header` 均无竖条。
result: [pending]

### 2. E6/E7 —— 两个 12×12 mask 字形与相邻文字的基线视觉对齐
expected: `.annotation-quote::before`(实心图钉)与 `.verdict-location::before`(实心地图标记)与首行文字**视觉齐平**,折行时不漂移,且**不撑高行盒**(行高仍由 `--lh-snug` / `--lh-reading` 决定)。
result: [pending]

### 3. E8 —— 页面级层级「读起来」成立
expected: 全屏最大最重的文字是**文档自己的 h1**,不是容器标签「文档区」;三级标题层级分明、不互相淹没。字号半边已由运行时断言钉死(28 > 24 > 22 > 14),此项判「读起来是否分明」。
result: [pending]

### 4. E3 —— 最窄面板下 `#btn-authorize` 文本不换行不裁切
expected: 在 `--doc-panel-w` 最窄值 340px(内容宽约 260px)下,「授权撰写总设计文档」在 16px 下**单行显示,不换行不裁切**。计划的算术(标签约 144px + padding-x 32px ≈ 176px < 260px)成立,但 check-05 不把面板压到 340px 实测。
result: [pending]

### 5. VISUAL-04 口径确认 —— `#ai-panel` 不参与「三选一活动态」推导
expected: 人工确认 REQUIREMENTS 的「侧栏四个面板…可区分」按 D-16 的**「三选一活动态 + AI 面板折叠态」**口径被接受(`#ai-panel` 从不被 `.hidden`,其可辨状态是既有的 ▾/▸ 折叠指示器)。若要求给 AI 面板也加活动标记,那是**新的范围**,不是本阶段的缺陷。
result: [pending]

### 6. `#ai-panel` 折叠点击穿透
expected: 点击 `#ai-panel` 的折叠指示器,`#ai-panel-body` 的 `.collapsed` 切换正常、指示器字形切换正常、标题行**不出现竖条**。本阶段对 `app.js` / `index.html` / `.collapse-indicator` 零 diff,check-05 的对照组也已断言 `#ai-panel .panel-header box-shadow == none`,故行为「按构造不变」是结构性证明 —— 此项只补一次低成本人工点击。
result: [pending]

## Summary

total: 6
passed: 0
issues: 0
pending: 6
skipped: 0
blocked: 0

## Gaps
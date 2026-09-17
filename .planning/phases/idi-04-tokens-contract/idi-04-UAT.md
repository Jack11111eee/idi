---
status: testing
phase: idi-04-tokens-contract
source: [idi-04-01-SUMMARY.md, idi-04-02-SUMMARY.md, idi-04-03-SUMMARY.md]
started: 2026-09-17T16:10:40Z
updated: 2026-09-17T16:10:40Z
---

## Current Test

number: 1
name: SC4 browser 实检 — the five elements hidden only by `.hidden`
expected: |
  `#draft-empty` / `#rounds-hint` / `#btn-process-round` / `#round-switcher` / `#writing-hint`
  are never visible in a state where they should be hidden, and the three 1-0-0
  competitors (`#selection-menu` / `#annotations-panel` / `#checks-panel`) still hide
  when `.hidden` is applied.
awaiting: user response

## 为什么这些项没有被自动化

本阶段以 `--auto` 运行(`workflow.auto_advance: true`),tracer 门与全部 `<human-check>` 都是**自动批准**而非实际执行。
本环境**无法**自动化这些检查:screenshots 不可用(无头渲染被阻断,且应用常驻的 `/api/events` SSE 流使截图无法终止);
键盘文本选区无法自动化;DevTools computed-style 读数没有无头等价物。

因此每一项都**以 `pending` 记录、不主张任何证据**。这正是计划本身要求的路由:无法确认的 backstop 走
`human_needed`(`insufficient_spec`),绝不静默通过。

**已由自动化层证明的部分**(无需你重验):四条守卫命令在真实树上 PASS 且各自可失败(verifier 独立做了 10 次变异测试);
块外裸 hex = 0;tier-1 primitive 泄漏 = 0;Gate 2 为空;`app.js`/`index.html`/vendor 零改动;pytest 219 passed / 6 skipped;
14/14 需求 SATISFIED。本文件只覆盖**必须由人眼/浏览器确认**的部分。

## Tests

### 1. SC4 browser 实检 — five `.hidden`-only elements
expected: `#draft-empty`、`#rounds-hint`、`#btn-process-round`、`#round-switcher`、`#writing-hint` 在任何应隐藏的状态下都不可见;三个 1-0-0 竞争者(`#selection-menu` / `#annotations-panel` / `#checks-panel`)施加 `.hidden` 后仍然隐藏
result: [pending]
note: CHECK-03 只证明规则文本唯一,不证明它仍赢得层叠。这是级联/渲染结果,必须实检。

### 2. 冻结轮 backstop
expected: 打开一个历史(冻结)轮次 → `#round-doc` 的 computed `box-shadow` 含 `inset 3px 0 0 rgb(138, 101, 8)`、`opacity` 为 `1`、`filter` 为 `saturate(0.6)`;正文文字对比度 ≥ 4.5:1
result: [pending]
note: `verification: backstop` 真值 —— 存在性与接线永远不足以确认。无法确认即走 `human_needed`(`insufficient_spec`)。

### 3. DevTools computed-style 抽查 — Plan 01(13 项)
expected: 每个具名属性读到令牌层/清单所断言的值:
`.hint` color = `rgb(106,106,106)`;`.badge-answered` color = `rgb(106,106,106)`;
`#btn-authorize` color/border-color/background-color = `rgb(38,117,74)` / `rgb(38,117,74)` / `rgb(233,247,239)`;
`#btn-process-round` 与 `#btn-authorize` 逐字节相同;`.kind-write .event-kind` background = `rgb(38,117,74)`;
`.kind-done .event-kind` background = `rgb(0,0,0)`;`#ai-route-select` border-top-color = `rgb(138,138,138)`;
`#selection-menu` border-top-color = `rgb(138,138,138)`;`#stream-banner` border-top-color = `rgb(138,101,8)`;
`#state-badge` color/background = `rgb(31,99,189)` / `rgb(238,244,255)`;`.chat-user` background = `rgb(31,99,189)`;
`.overlay-card` box-shadow 含 `rgba(0,0,0,0.2)`
result: [pending]

### 4. DevTools computed-style 抽查 — Plan 02(16 项)
expected: 间距按 D-16 账本落位(`.panel-header` 10px/16px、`#doc-pane` 32px/40px、`button` 6px/10px、
`.overlay-card` 24px(自 28px 吸附)、`#brainstorm-view` 24px(自 22px 吸附));
字号(`#brainstorm-view h2` 14px + `rgb(138,101,8)`、`#draft-view h2` 15px、`.panel-header h2` 14px、
`.overlay-card h3` 16px、`.markdown-body` 14px、`.markdown-body code` 13px(自 12.5px 折叠));
z-index(`#selection-menu` 200 / `#state-badge` 10 / `#stream-banner` 20);
冻结轮 box-shadow/opacity/filter;`#rounds-placeholder.archive-mode #round-doc` opacity `0.75`;任意 `button` color `rgb(26,26,26)`
result: [pending]
note: `14px` 存活为一级档是用户签核的 S-2 决定 —— Phase 5 SC5 / Phase 6 SC5 的下游门依赖它。

### 5. DevTools computed-style 抽查 — Plan 03(10 项)
expected: `#ai-route-select` border-top-color/background-color = `rgb(138,138,138)` / `rgb(255,255,255)`;
`.hint` color `rgb(106,106,106)` on `rgb(250,250,250)`;`#stream-banner` border-top-color `rgb(138,101,8)`;
`.markdown-body` color `rgb(26,26,26)` **肉眼可辨地**比 `.hint` 更深(这是 `ORDER 0.311` 的可观察形态);
外加一次「处理本轮批注」与一次「发送」交互无错误完成
result: [pending]

### 6. CR-06 渲染结果
expected: 一条普通的「已回应」批注 —— 用户批注与 AI 回应正文**都**以 `--color-text-muted` 渲染(D-11 意图的条目内层级)
result: [pending]
note: 该修复只经代码审阅确认(`app.js:1147` 在已回应路径上创建 `annotation-answer-body`;
`.annotation-plain` 之外无其它规则为其着色)。是渲染行为变更,任何语法检查或守卫都无法确认。

## Summary

total: 6
passed: 0
issues: 0
pending: 6
skipped: 0
blocked: 0

## Gaps

<!-- 测试后如发现 issue,按 YAML 格式追加;此节直接喂给 /gsd-plan-phase --gaps -->
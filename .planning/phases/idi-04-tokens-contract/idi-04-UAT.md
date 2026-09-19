---
status: resolved
phase: idi-04-tokens-contract
source: [idi-04-01-SUMMARY.md, idi-04-02-SUMMARY.md, idi-04-03-SUMMARY.md]
started: 2026-09-17T16:10:40Z
updated: 2026-09-19T14:05:00Z
---

## Current Test

number: 6
name: CR-06 渲染结果
expected: |
  一条普通的「已回应」批注 —— 用户批注与 AI 回应正文**都**以 `--color-text-muted` 渲染。
  6 项已全部通过(逐项结果见 `## Tests`,计数见 `## Summary`)。
awaiting: 无 —— 6 项全部 `pass`,三条 gap 已按 D-10 / D-12 / D-13 消解(见 `## Gaps`)

## 这 6 项现在如何被自动化

本阶段当初以 `--auto` 运行,tracer 门与全部 `<human-check>` 都是**自动批准**而非实际执行;
6 项因此一律记 `pending`、不主张任何证据。**那条前提已被证伪**:同一台机器、同一环境
可以完整跑通「启动应用 → 浏览器 → 进入磁盘状态样本 → 读 computed style」这条链路。

harness 路径:**`scripts/check-05-ui-uat.py`**(Playwright + 浏览器,单文件自述)。

```bash
.venv/bin/pip install -r requirements-dev.txt     # 只需一次(playwright==1.63.0)
.venv/bin/python scripts/check-05-ui-uat.py       # 跑第 1..6 项,退出码 0/1/2
.venv/bin/python scripts/check-05-ui-uat.py --item 3      # 只跑某一项
.venv/bin/python scripts/check-05-ui-uat.py --ai-smoke    # 额外真跑两次 AI 交互冒烟
```

- 磁盘状态样本固化在 `scripts/ui-states/`(p1 / p12 / p3 / checking / archive),
  运行不再依赖 `/tmp/idi-states/`;每次运行复制到临时目录,仓库样本只读。
- **不需要** `playwright install`(零下载)。
- 幂等:连跑两遍逐字节一致(`/tmp/idi-uat-all.log` 与 `/tmp/idi-uat-all-2.log`)。
- 退出码:0 = 全部 pass,1 = 有 fail,2 = 有 blocked。

**断言的期望侧自 04.1 起为「令牌接线」形式(D-14)。** 每条颜色断言的期望值不再硬编码
`rgb(...)`,而是运行时解析出的 `--token` 值(`resolve_color` / `resolve_token`),
消费者侧仍读 computed style。这是 20 条假 FAIL 的单条根因(期望值定稿于值层改动之前)
的结构性修复:值层再改,断言不动。代价是「硬编码值能抓令牌接错线」的那部分检测力被换掉,
补偿方式见 `## Gaps` 末尾的说明。

**仍然真实存在的限制(不试图绕过):键盘文本选区无法自动化。**
`keyboard.press("Shift+ArrowRight")` 与 `down("Shift")+press()` 两种写法,在普通 `<p>`、
`tabindex` 容器、甚至 `contenteditable` 里都选不中任何文字(`window.getSelection()` 恒为空),
`--enable-caret-browsing` 也无效。故任何依赖 Shift+方向键选字的验收项无法自动验证。
本文件的 6 项里没有这类项。

**已被证伪、不再成立的三条旧理由**(原文照录以备对照):
~~screenshots 不可用(无头渲染被阻断,且应用常驻的 `/api/events` SSE 流使截图无法终止)~~ ——
实测无头浏览器可正常启动并读 computed style;SSE 长连接只让 `networkidle` 永不返回,
改用 `waitUntil="domcontentloaded"` + 显式等待即可。
~~键盘文本选区无法自动化~~ —— 这条**仍然成立**,已上移保留。
~~DevTools computed-style 读数没有无头等价物~~ —— 实测等价物就是
`page.evaluate(el => getComputedStyle(el)[prop])`。

**已由自动化层证明的部分**(无需重验):四条守卫命令在真实树上 PASS 且各自可失败
(verifier 独立做了 10 次变异测试);块外裸 hex = 0;tier-1 primitive 泄漏 = 0;Gate 2 为空;
`app.js`/`index.html`/vendor 零改动;pytest 219 passed / 6 skipped;14/14 需求 SATISFIED。

## Tests

### 1. SC4 browser 实检 — five `.hidden`-only elements
expected: `#draft-empty`、`#rounds-hint`、`#btn-process-round`、`#round-switcher`、`#writing-hint` 在任何应隐藏的状态下都不可见;三个 1-0-0 竞争者(`#selection-menu` / `#annotations-panel` / `#checks-panel`)施加 `.hidden` 后仍然隐藏
result: [pass]
evidence: |
  本阶段实跑 `.venv/bin/python scripts/check-05-ui-uat.py`:**45 条断言全部 PASS(0 FAIL / 0 BLOCKED)**,
  该项结论 `PASS`,全量退出码 2(唯一的 BLOCKED 来自第 5 项,见下)。
  矩阵规模自本 UAT 定稿后扩大为 **6 个元素 × 5 个状态 = 30 格**(新增 `#session-panel`
  —— 主区在阶段 1-2 会话流 / 阶段 3+ 批注流之间是切换而非叠加,`app.js` 在 `applySessionGates`
  单点 toggle):该隐藏时 `display === "none"`,该可见时 `display !== "none"`。
  9 个元素**强制** `classList.add("hidden")` 后全部 `display === "none"`(含三个 1-0-0 竞争者
  `#selection-menu` / `#annotations-panel` / `#checks-panel`)—— 这正是 CHECK-03 覆盖不到的那一步:
  `.hidden { display: none !important }` 在真实层叠里仍然赢。
  反向证据:6 个元素摘掉 `.hidden` 后自身全部重新可见。
  覆盖说明:`#writing-hint` 在 5 个样本状态里没有任何一格是「app.js 给自身加 `.hidden`」——
  它只被祖先 `#writing-view` 藏住(故该行断言的是「自身未被 `.hidden` 藏」);
  它自身 `.hidden` 的层叠行为由上述强制加类断言覆盖,不是静默跳过。
note: CHECK-03 只证明规则文本唯一,不证明它仍赢得层叠。这是级联/渲染结果,必须实检。

### 2. 冻结轮 backstop
expected: 打开一个历史(冻结)轮次 → `#round-doc` 的 computed `box-shadow` 的 `inset` / `x` / `y` / `blur` / `spread` 与颜色**等于运行时解析出的 `--color-action-warning`**(令牌接线,D-14)、`opacity` 为 `1`、`filter` 为 `saturate(0.6)`;正文文字对比度 ≥ 4.5:1
result: [pass]
evidence: |
  p3 样本切到第 1 轮(历史轮)后,5 条断言全部 PASS(0 FAIL / 0 BLOCKED):
  `#round-doc` classList 含 `round-frozen`;computed `box-shadow` =
  `rgb(79, 52, 34) 3px 0px 0px 0px inset`(语义解析:inset ✓ / x=3px ✓ / y=0 ✓ / blur=0 ✓ /
  spread=0 ✓ / 色 == 运行时解析出的 `--color-action-warning` = `rgb(79, 52, 34)` ✓);
  `opacity` = `1`;`filter` = `saturate(0.6)`;
  正文对比度 `ratio=15.48`(color=`rgb(32, 32, 32)` on bg=`rgb(249, 249, 249)`),阈值 4.5。
  **harness 规格修正(非产品缺陷)**:Chrome 把 box-shadow 序列化成「颜色在前、`inset` 在最后」,
  故 UAT 原先写的字面子串 `inset 3px 0 0 <色>` 逐字匹配恒为 False;
  断言改用语义解析 + 令牌解析值比对,字面比对结果作为 INFO 打印在日志里。
  **诊断(不计入本项判定)**:引用块 `<p>`(`--color-text-muted` = `rgb(100, 100, 100)`)
  在同一底色上 `ratio=5.62` —— 该 AA 倒退已由 04.1 的值层重写消解(见 `## Gaps` 末段)。
note: `verification: backstop` 真值 —— 存在性与接线永远不足以确认。

### 3. DevTools computed-style 抽查 — Plan 01(13 项)
expected: 每个具名属性读到**运行时解析出的令牌值**(令牌接线,D-14):`.hint` color == `--color-text-muted`;`.badge-answered` color == `--color-text-muted`;`#btn-authorize` color/border-color/background-color == `--color-action-irreversible-fg` / `--color-action-irreversible` / `--color-action-irreversible-surface`;`#btn-process-round` 与 `#btn-authorize` 逐字节相同;`.kind-write .event-kind` background == `--color-kind-write`;`.kind-done .event-kind` background == `--color-kind-done`;`#ai-route-select` border-top-color == `--color-border-strong`;`#selection-menu` border-top-color == `--color-border-strong`;`#stream-banner` border-top-color == `--color-action-warning`;`#state-badge` color/background == `--color-text-info` / `--color-surface-info`;`.chat-user` background == `--color-surface-user`;`.overlay-card` box-shadow 含 `rgba(0,0,0,0.2)`
result: [pass]
evidence: |
  15 条断言**全部 PASS(0 FAIL / 0 BLOCKED)**。原 7 条 FAIL 的消解口径见 `## Gaps`:
  颜色值漂移随 04.1 的值层重写消解(D-10),`.overlay-card` box-shadow 由 R-2 恢复(D-11)。
  本阶段实跑解析出的令牌值(`scripts/check-05-ui-uat.py` 的 `INFO item3 令牌解析` 行):
  `--color-text-muted` = `rgb(100, 100, 100)`;`--color-border-strong` = `rgb(141, 141, 141)`;
  `--color-action-warning` = `rgb(79, 52, 34)`;`--color-kind-write` = `rgb(33, 131, 88)`;
  `--color-kind-done` = `rgb(32, 32, 32)`;`--color-surface-user` = `rgb(232, 232, 232)`;
  `--color-action-irreversible` = `rgb(33, 131, 88)`;`--color-action-irreversible-fg` = `rgb(25, 59, 45)`;
  `--color-action-irreversible-surface` = `rgb(230, 246, 235)`;`--color-text-info` = `rgb(13, 116, 206)`;
  `--color-surface-info` = `rgb(244, 250, 255)`。
  构造说明:`.kind-write` / `.kind-done` / `.chat-user` 三处用应用自身的
  `renderEvent` / `appendChatMessage` 渲染探针节点(真实代码路径,零 AI 调用、零网络)。
  值的仲裁者是 `scripts/check-02-contrast.py`(43 对实测比值 + `ORDER 0.363`),
  本 harness 只证明「消费者接上了正确的令牌」,不承担值的仲裁。
note: 本项判据以令牌接线表述 —— 值层再改不产生假 FAIL。`#btn-authorize` 的 `color` 接的是
`--color-action-irreversible-fg`(green-12),不是 `--color-action-irreversible`(green-11):
接线按 `frontend/style.css:928-934` 的三条声明逐条对位。

### 4. DevTools computed-style 抽查 — Plan 02(16 项)
expected: 间距/字号按 D-12 更新为 HEAD 实测值(`.panel-header` 6px/10px、`#doc-panel-body` padding 32px/40px(D-13)、`button` 6px/10px、`.overlay-card` 24px、`#brainstorm-view` margin-top 24px、`#brainstorm-view h2` 16px、`#draft-view h2` 18px、`.panel-header h2` 14px、`.overlay-card h3` 24px、`.markdown-body` 16px、`.markdown-body code` 14px);颜色按令牌接线(`#brainstorm-view h2` color == `--color-action-warning`、`button` color == `--color-text`);z-index 按令牌接线(`#selection-menu` / `#state-badge` / `#stream-banner` == `--z-selection-menu` / `--z-badge` / `--z-banner`);冻结轮 box-shadow/opacity/filter;`#rounds-placeholder.archive-mode #round-doc` opacity `0.75`
result: [pass]
evidence: |
  24 条断言**全部 PASS(0 FAIL / 0 BLOCKED)**,该项结论 `PASS`。
  原 9 条 FAIL 与 1 条 BLOCKED 的消解口径见 `## Gaps`:
  - 间距/字号 7 条按 D-12 **更新期望值接受 HEAD 现状**(`frontend/style.css` 一字未动);
  - `#state-badge` z-index 由 **R-1 恢复**后不再为 `auto`(D-11,正确性修复);
  - `button` color 改走 `--color-text` 的运行时解析(D-14);
  - 原 `#doc-pane` 那条 BLOCKED 改为 `#doc-panel-body` 的 `ok` 断言(D-13),期望 `32px 40px` 实测一致。
    原期望串写错了名字:`frontend/index.html` 里从来没有 `#doc-pane` 这个 id(实际是
    `#doc-panel-body`);`frontend/app.js` 的约 70 个顶层 `getElementById` id **一字未动** ——
    改的是 UAT 的**期望字符串**,不是 id(硬规则 5)。
  本阶段实跑解析出的令牌值(`INFO item4 令牌解析` 行):
  `--color-action-warning` = `rgb(79, 52, 34)`;`--color-text` = `rgb(32, 32, 32)`;
  `--z-selection-menu` = `200`;`--z-badge` = `10`;`--z-banner` = `20`。
  三条 z-index 走令牌接线同时是 **TOKEN-07 在渲染层的证据**:`--z-badge` 由 R-1 恢复消费者后
  不再空转,`badge < banner` 的承重序关系两端都在真实 DOM 上被读到(不只是围栏注释里的声明)。
note: `14px` 存活为一级字号档是用户签核的 S-2 决定 —— Phase 5 SC5 / Phase 6 SC5 的下游门依赖它。
本项单列的 `S-2 DEPENDENCY --text-base = 14px` 断言仍 PASS。

### 5. DevTools computed-style 抽查 — Plan 03(10 项)
expected: 六条颜色断言按令牌接线(D-14):`#ai-route-select` border-top-color/background-color == `--color-border-strong` / `--color-surface`;`.hint` color == `--color-text-muted`;`.hint` 实际背景 == `--color-surface`;`#stream-banner` border-top-color == `--color-action-warning`;`.markdown-body` color == `--color-text`,且 `.markdown-body` 亮度**显著低于** `.hint`(这是 `ORDER 0.363` 的可观察形态);外加一次「处理本轮批注」与一次「发送」交互无错误完成
result: [pass]
evidence: |
  默认运行(无 `--ai-smoke`):9 条断言 **7 PASS / 0 FAIL / 2 BLOCKED**,该项结论 `BLOCKED`。
  六条颜色断言 + 层级断言全部 PASS;原 4 条 FAIL(`#ai-route-select` border-top-color、
  `.hint` color、`.hint` 实际背景、`.markdown-body` color)随值层重写消解,口径见 `## Gaps`。
  层级断言实测 `lum(.markdown-body)=0.0144 < lum(.hint)=0.1274`(注释已由 ORDER 0.311
  更新为 ORDER 0.363 —— 该比值由 0.311 放宽到 0.363 是刻度强制的,见 04.1-UI-SPEC 04.1-N-1)。
  两条 BLOCKED 恰为两次交互冒烟,理由写明「需要真实 AI 调用,默认不执行;加 --ai-smoke 重跑」。
  **默认运行下这两条 BLOCKED 不构成待办**:它们需要真实 AI 调用与计费,harness 的退出码
  `code = 1 if any_fail else (2 if any_blocked else 0)` 意味着不带 `--ai-smoke` 时
  全量 `exit=0` 不可达;把它们改写成 PASS 的唯一办法是删掉那两次 `blocked()` 调用,
  而那正是「运行时验证被声称而非执行」所依赖的信号(T-idi041-09)。
  **补充证据(另跑 `.venv/bin/python scripts/check-05-ui-uat.py --item 5 --ai-smoke`,claude CLI 可用)**:
  两条冒烟**都真实跑通、均 PASS**:
  - 「处理本轮批注」(p3,临时副本,真实 AI 调用):无 console 错误、无 http 4xx-5xx、无未捕获异常。
  - 「发送」(p12,临时副本,真实 AI 调用):同上。
  侧记:「发送」原在 p3 执行时,Playwright 报 `#btn-send` 被 `#annotations-panel` 的 `.panel-body`
  遮挡不可点(诊断 `elementFromPoint` = `panel-body`,非 `btn-send`)—— 阶段 3 主区由批注流占据,
  会话流的发送键被挤到不可点位置。故「发送」冒烟改在 p12(会话流的自然活动面)执行。
  这是本次实测的附带观察,不属于本 UAT 6 项的任何一条判据。
note: 默认运行的 `exit=2` 与该项的 `BLOCKED` 是设计使然,不是缺陷。

### 6. CR-06 渲染结果
expected: 一条普通的「已回应」批注 —— 用户批注与 AI 回应正文**都**以 `--color-text-muted` 渲染(D-11 意图的条目内层级)
result: [pass]
evidence: |
  2 条断言全部 PASS(0 FAIL / 0 BLOCKED)。在 p3 临时副本写入一条八字段齐全的「已回应」批注
  (`quote` 精确取自 round-2 文档真实文本「建议进入授权环节」),重进项目后展开 `<details>`:
  - `.annotation-note`(用户批注)color = `rgb(100, 100, 100)`
  - `.annotation-answer-body`(AI 回应正文)color = `rgb(100, 100, 100)`
  两者都等于运行时解析出的 `--color-text-muted`(`rgb(100, 100, 100)`)—— 本项判据以**令牌接线**表述,
  故按令牌解析值比对,未硬编码任何字面色。
note: 该修复只经代码审阅确认(`app.js:1147` 在已回应路径上创建 `annotation-answer-body`;
`.annotation-plain` 之外无其它规则为其着色)。是渲染行为变更,任何语法检查或守卫都无法确认。

## Summary

total: 6
passed: 6
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

<!-- 测试后如发现 issue,按 YAML 格式追加;此节直接喂给 /gsd-plan-phase --gaps -->

**本节的三条 gap 已在 `idi-04.1-radix`(Radix 颜色族重写)中全部消解 —— 无未决项。**
下面的 `observed` / `failing` / `blocked` 原文**逐字保留为历史对照**:它们是「20 条假 FAIL 的
单条根因」这条教训的载体,不是待办清单。

```yaml
# 根因(单条,覆盖下面全部 3 个 gap):
#   UAT 的期望值定稿于 0c658aa(2026-09-17),而 448686b「fix(260918-qrq): 令牌值层换血」
#   在那之后改动了令牌值层:--gray-600 #6a6a6a→#8f8f8f、--gray-900 #1a1a1a→#0d0d0d、
#   --gray-500 #8a8a8a→#d9d9d9、--blue-700 #1f63bd→#3a83f7、--gray-25 #fafafa→#ffffff、
#   --text-base 13px→14px、--text-md 14px→16px、--text-lg 15px→18px、--text-xl 16px→24px,
#   并删除了 .overlay-card 的 box-shadow 与 #state-badge 的 z-index。
#   STATE.md 记 260918-qrq 为「按用户知情决策红着交出(check-02 14 条失败)」。
#   故下面的 gap 不是新缺陷,而是「UAT 期望值 vs HEAD 现状」的差异待裁:
#   (a) 更新 UAT 期望值以匹配已签核的换肤,或 (b) 回退 260918-qrq 的相应令牌值。
#   frontend/ 本次零改动 —— 本 harness 只观测、不修复。
#
#   裁定(idi-04.1-radix D-10 / D-12 / D-13):走 (a),并把根因**结构性**移除 ——
#   断言改为「令牌接线」形式(D-14),期望侧来自运行时解析出的 --token,值层再改不产生假 FAIL。

gaps:
  - test: 3
    item: "DevTools computed-style 抽查 — Plan 01(13 项)"
    severity: high
    status: resolved
    resolution: "D-10(颜色值漂移随值层重写消解)+ D-11(.overlay-card box-shadow 由 R-2 恢复)+ D-14(断言改令牌接线)。本阶段实跑 15 条断言全 PASS。"
    observed: "15 条断言 7 FAIL / 8 PASS"
    failing:
      - ".hint color: expected rgb(106,106,106) actual rgb(143,143,143)"
      - ".badge-answered color: expected rgb(106,106,106) actual rgb(143,143,143)"
      - "#state-badge color: expected rgb(31,99,189) actual rgb(58,131,247)"
      - ".chat-user background: expected rgb(31,99,189) actual rgb(236,236,236)"
      - "#ai-route-select border-top-color: expected rgb(138,138,138) actual rgb(217,217,217)"
      - "#selection-menu border-top-color: expected rgb(138,138,138) actual rgb(217,217,217)"
      - ".overlay-card box-shadow 含 rgba(0,0,0,0.2): actual none"

  - test: 4
    item: "DevTools computed-style 抽查 — Plan 02(16 项)"
    severity: high
    status: resolved
    resolution: "D-12(间距/字号更新期望值接受 HEAD 现状)+ D-13(#doc-pane → #doc-panel-body)+ D-11(#state-badge z-index 由 R-1 恢复)+ D-14(颜色改令牌接线)。本阶段实跑 24 条断言全 PASS,0 BLOCKED。"
    observed: "24 条断言 9 FAIL / 14 PASS / 1 BLOCKED"
    failing:
      - ".panel-header padding-top: expected 10px actual 6px"
      - ".panel-header padding-left: expected 16px actual 10px"
      - "#brainstorm-view h2 font-size: expected 14px actual 16px"
      - "#draft-view h2 font-size: expected 15px actual 18px"
      - ".overlay-card h3 font-size: expected 16px actual 24px"
      - ".markdown-body font-size: expected 14px actual 16px"
      - ".markdown-body code font-size: expected 13px actual 14px"
      - "#state-badge z-index: expected 10 actual auto"
      - "button color: expected rgb(26,26,26) actual rgb(13,13,13)"
    blocked:
      - "#doc-pane padding: 选择器不存在(实际 id 为 #doc-panel-body,其 padding 实测 32px 40px 与期望一致)。要么把 UAT 的选择器改名为 #doc-panel-body,要么恢复 #doc-pane 这一 id。"
    missing: "已裁定:D-13 改 UAT 的期望字符串为 #doc-panel-body —— 改的是期望字符串,不是 id(硬规则 5:约 70 个顶层 getElementById id 一字未动)。"

  - test: 5
    item: "DevTools computed-style 抽查 — Plan 03(10 项)"
    severity: medium
    status: resolved
    resolution: "D-10(颜色值漂移随值层重写消解)+ D-14(断言改令牌接线)。本阶段实跑 9 条断言 0 FAIL,2 BLOCKED 恰为两次交互冒烟。"
    observed: "9 条断言 4 FAIL / 3 PASS / 2 BLOCKED(默认运行);--ai-smoke 补充运行下两条交互冒烟均 PASS"
    failing:
      - "#ai-route-select border-top-color: expected rgb(138,138,138) actual rgb(217,217,217)"
      - ".hint color: expected rgb(106,106,106) actual rgb(143,143,143)"
      - ".hint 实际背景: expected rgb(250,250,250) actual rgb(255,255,255)"
      - ".markdown-body color: expected rgb(26,26,26) actual rgb(13,13,13)"
    blocked:
      - "两条交互冒烟在默认运行下 blocked(需要真实 AI 调用);已用 --ai-smoke 补齐证据,两条均真实跑通并 PASS。默认运行的 blocked 不构成待办。"
    missing: "无。附带观察(阶段 3 的 #btn-send 被 #annotations-panel 遮挡不可点)仍留在上方 evidence 里,不属于本 UAT 6 项的任何一条判据。"

# 另记(原为本次实测到的真实 AA 倒退)—— 已由 04.1 的值层重写**修复**:
#   --color-text-muted 由 #8f8f8f(在 #ffffff 上 3.23:1 ✗)改为 --radix-gray-11 = #646464,
#   在 --color-surface #f9f9f9 上 **5.62:1 ✓**。比值由 scripts/check-02-contrast.py 实测
#   (该脚本是值的唯一仲裁者,不是本 harness)。
#   受影响面(.hint / .badge-answered / .markdown-body blockquote / .annotation-answer summary /
#   .verdict-suggestion)随之全部恢复达标 —— 第 2 项日志里的 blockquote 诊断行已从 3.23 变为 5.62。
#   STATE.md 里「check-02 按用户知情决策红着交出(14 条失败)」的记载随之失效。
```

**D-14 的代价与补偿(检测力损失,已接受)。** 令牌接线换掉了「硬编码值能抓令牌接错线」的能力。
补偿有两条:①每条接线断言旁的 `info()` 打印运行时解析出的令牌值,值错时在日志里看得见;
②值本身的仲裁者是 `scripts/check-02-contrast.py` 的 43 对实测比值,不由本 harness 承担。
二者合起来覆盖「接线」与「值」两个轴。

**本阶段对断言的接线做了一处修正(不是放宽判据)。** `#btn-authorize` 的 `color` 接的是
`--color-action-irreversible-fg`(green-12),不是 `--color-action-irreversible`(green-11)——
按 `frontend/style.css:928-934` 的三条声明逐条对位。原先按后者接线的写法会让该断言永远失败,
那是接线错误而非产品缺陷。

## Carry-Forward

### ① C-1 的下游门引用复核(携带项 #7)—— 实测确认,不在本阶段改写

**实测(真实浏览器,`.venv/bin/python scripts/check-05-ui-uat.py --item 4` 已逐条断言):
`#brainstorm-view h2` 计算为 `16px`,其颜色为 `--color-action-warning` = `#4f3422`。**

静态依据:`frontend/style.css:679-683` 的 `#brainstorm-view h2` 用 `font-size: var(--text-md)`
与 `color: var(--color-action-warning)`;围栏内 `--text-md: 16px`(`style.css:207`)、
`--radix-amber-12: #4f3422`(`style.css:66`)。

**失真引用枚举 —— 判据是内容,不是行号。** 站点按「**同一行同时含 `#brainstorm-view h2`
与 `8a6508`**」识别;`grep -cE '#brainstorm-view h2.*8a6508' .planning/ROADMAP.md` 当前为 **5**。
行号会随任何 ROADMAP 编辑移动(本阶段自己的 wave 重排就移动过),故下面行内的行号只是
**复核当时的定位辅助,不是判据**。五个站点逐点一行:

- 硬规则 3「追加,不重排」(复核时 `.planning/ROADMAP.md:37`):原文「`#draft-view h2` L230 与 `#brainstorm-view h2` L296 同为 1-0-1,后者胜出 → 14px / `#8a6508`」—— 实测为 `16px` / `#4f3422`,该引用失真。
- Phase 5 Pitfall 9(复核时 `.planning/ROADMAP.md:169`):原文「`#brainstorm-view h2` 的 14px / `#8a6508` 是顺序决定的」—— 实测为 `16px` / `#4f3422`,该引用失真。
- §Phase 5 Gates(复核时 `.planning/ROADMAP.md:172`):原文「`#brainstorm-view h2` 仍计算为 14px / `#8a6508`」—— 实测为 `16px` / `#4f3422`,该引用失真。
- §Phase 6 SC5(复核时 `.planning/ROADMAP.md:200`):原文「`#brainstorm-view h2` 仍计算为 14px / `#8a6508`(未因结构性改动而变)」—— 实测为 `16px` / `#4f3422`,该引用失真。
- §Phase 6 Gates(复核时 `.planning/ROADMAP.md:212`):原文「`#brainstorm-view h2` 仍 14px / `#8a6508`」—— 实测为 `16px` / `#4f3422`,该引用失真。

另有一处非 ROADMAP 的引用:`.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` 携带项 #7(§Q3)
写「`#brainstorm-view h2` = 14px is confirmed alive at HEAD」—— 同属失真(实测 `16px`)。

**一行式修正建议(供用户直接采纳):** 上述六处的 `14px` → **`16px`**;`#8a6508` → **`#4f3422`**。

**本阶段不单方面改写这些验收判据。** §Phase 6 SC5 等是**未来阶段已签核的门**,改写它属于
范围外,须由用户裁决。本阶段只做复核与留证(prohibition:不得单方面改写 `ROADMAP.md`
§Phase 6 SC5 的验收判据)。

### ② 携带项 #8 —— Phase 7 的焦点环必须在 Phase 7 自己的门里重测(本阶段不执行)

`--color-focus: #1f63bd`(Phase 4 定的环色)原本对着旧地面 `#fafafa` 测。本阶段**不改环色,
只改它落的地面**:`--color-surface` 现为 `#f9f9f9`、`--color-surface-page` 现为 `#fcfcfc`。
**Phase 7 必须在这两个新地面上重新测 ≥ 3:1,该门才能通过。** 本阶段不代它做这个测量,
也不改环色 —— 记录为下游义务。

### ③ D-15 的三数差异留档(24 / 34 / 43)

CHECK-02 配对清单的规模有三个数字在流转,差异必须留档而不是被「对齐」掉:

- `ROADMAP.md` Phase 4 写 **24 对**(20 文本 + 4 非文本)—— 定稿时的计划值。
- 磁盘现状(04.1 动手前)是 **34 对**(29 TEXT + 5 NON-TEXT,另 1 条 `ORDER`)。
- `idi-04.1-radix` 的 goal 写 **34**,而重算后实际落地为 **43 对**(34 TEXT + 9 NON-TEXT,另 1 条 `ORDER`)。

D-15 的裁定是「按实际落地对重新枚举」—— 围栏自述的契约是**枚举真实发生的组合**,
不是覆盖面指标。故 43 是结果而非偏差;24 与 34 是历史值,保留在此供对照。
`scripts/check-02-contrast.py` 的末行 `PASS: 0 failures` 与 `ORDER 0.363` 是当前仲裁结论。

### ④ 本次实跑的收口证据

| 门 | 命令 | 结果 |
|---|---|---|
| 全量 harness | `.venv/bin/python scripts/check-05-ui-uat.py` | 0 FAIL;`item 1`/`2`/`3`/`4`/`6` 全 `PASS`(0 BLOCKED),`item 5` 为 `BLOCKED` 且其 2 条 BLOCKED 恰为已记录的两次交互冒烟;退出码 **2**(设计使然,见第 5 项 evidence) |
| 切片 | `.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,6` | 退出码 **0**;三项结论列全 `PASS` |
| 值的仲裁者 | `python3 scripts/check-02-contrast.py` | 末行 `PASS: 0 failures`;43 条配对 + `ORDER 0.363` |
| 守卫 | `bash scripts/check-01-token-conformance.sh` / `check-03-hidden-uniqueness.sh` / `check-04-important-count.sh` | 各自 `PASS` |
| 回归 | `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped`(基线不变) |
| 零改动面 | `git status --porcelain -- frontend/` | 空(`style.css` / `app.js` / `index.html` / `vendor/` 全部零改动) |
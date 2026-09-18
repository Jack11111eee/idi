---
status: testing
phase: idi-04-tokens-contract
source: [idi-04-01-SUMMARY.md, idi-04-02-SUMMARY.md, idi-04-03-SUMMARY.md]
started: 2026-09-17T16:10:40Z
updated: 2026-09-18T17:04:19Z
---

## Current Test

number: 3
name: DevTools computed-style 抽查 — Plan 01(13 项)
expected: |
  每个具名属性读到令牌层/清单所断言的值。
  实测:15 条断言中 7 条 FAIL,根因是 260918-qrq(`448686b` 令牌值层换血)在 UAT 定稿后
  改动了令牌值 —— 见 `## Gaps`。
awaiting: 修复决定 —— 逐条见 `## Gaps`(更新 UAT 期望值,还是回退 260918-qrq 的令牌值)

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
  38 条断言全部 PASS(0 FAIL / 0 BLOCKED)。5 个元素 × 5 个状态(p1/p12/p3/checking/archive)
  的 25 格矩阵逐格命中:该隐藏时 `display === "none"`(如 p12 `#draft-empty`、p3/checking/archive
  `#rounds-hint`、checking `#round-switcher`、archive `#btn-process-round`),该可见时
  `display !== "none"`(均为 `block`)。
  8 个元素**强制** `classList.add("hidden")` 后全部 `display === "none"`(含三个 1-0-0 竞争者
  `#selection-menu` / `#annotations-panel` / `#checks-panel`)—— 这正是 CHECK-03 覆盖不到的那一步:
  `.hidden { display: none !important }` 在真实层叠里仍然赢。
  反向证据:5 个元素摘掉 `.hidden` 后自身全部重新可见。
  覆盖说明:`#writing-hint` 在 5 个样本状态里没有任何一格是「app.js 给自身加 `.hidden`」——
  它只被祖先 `#writing-view` 藏住(故该行断言的是「自身未被 `.hidden` 藏」);
  它自身 `.hidden` 的层叠行为由上述强制加类断言覆盖,不是静默跳过。
note: CHECK-03 只证明规则文本唯一,不证明它仍赢得层叠。这是级联/渲染结果,必须实检。

### 2. 冻结轮 backstop
expected: 打开一个历史(冻结)轮次 → `#round-doc` 的 computed `box-shadow` 含 `inset 3px 0 0 rgb(138, 101, 8)`、`opacity` 为 `1`、`filter` 为 `saturate(0.6)`;正文文字对比度 ≥ 4.5:1
result: [pass]
evidence: |
  p3 样本切到第 1 轮(历史轮)后,5 条断言全部 PASS(0 FAIL / 0 BLOCKED):
  `#round-doc` classList 含 `round-frozen`;computed `box-shadow` =
  `rgb(138, 101, 8) 3px 0px 0px 0px inset`(语义解析:inset ✓ / x=3px ✓ / y=0 ✓ / blur=0 ✓ /
  spread=0 ✓ / 色=rgb(138,101,8) ✓);`opacity` = `1`;`filter` = `saturate(0.6)`;
  正文对比度 `ratio=19.44`(color=`rgb(13, 13, 13)` on bg=`rgb(255, 255, 255)`),阈值 4.5。
  **harness 规格修正(非产品缺陷)**:Chrome 把 box-shadow 序列化成「颜色在前、`inset` 在最后」,
  故 UAT 写的字面子串 `inset 3px 0 0 rgb(138, 101, 8)` 逐字匹配为 False;
  断言改用语义解析,字面比对结果作为 INFO 打印在日志里。
  **诊断(不计入本项判定)**:引用块 `<p>`(--color-text-muted)在同一底色上 `ratio=3.23`,低于 AA 4.5:1 ——
  这是 260918-qrq 把 `--gray-600` 由 `#6a6a6a` 改为 `#8f8f8f` 的已知后果。
note: `verification: backstop` 真值 —— 存在性与接线永远不足以确认。

### 3. DevTools computed-style 抽查 — Plan 01(13 项)
expected: 每个具名属性读到令牌层/清单所断言的值:
`.hint` color = `rgb(106,106,106)`;`.badge-answered` color = `rgb(106,106,106)`;
`#btn-authorize` color/border-color/background-color = `rgb(38,117,74)` / `rgb(38,117,74)` / `rgb(233,247,239)`;
`#btn-process-round` 与 `#btn-authorize` 逐字节相同;`.kind-write .event-kind` background = `rgb(38,117,74)`;
`.kind-done .event-kind` background = `rgb(0,0,0)`;`#ai-route-select` border-top-color = `rgb(138,138,138)`;
`#selection-menu` border-top-color = `rgb(138,138,138)`;`#stream-banner` border-top-color = `rgb(138,101,8)`;
`#state-badge` color/background = `rgb(31,99,189)` / `rgb(238,244,255)`;`.chat-user` background = `rgb(31,99,189)`;
`.overlay-card` box-shadow 含 `rgba(0,0,0,0.2)`
result: [fail]
evidence: |
  15 条断言:**8 PASS / 7 FAIL / 0 BLOCKED**。逐条 expected vs actual(失败项):
  - `.hint` color: expected `rgb(106,106,106)` actual `rgb(143, 143, 143)` — FAIL
  - `#ai-route-select` border-top-color: expected `rgb(138,138,138)` actual `rgb(217, 217, 217)` — FAIL
  - `#selection-menu` border-top-color: expected `rgb(138,138,138)` actual `rgb(217, 217, 217)` — FAIL
  - `.overlay-card` box-shadow 含 `rgba(0,0,0,0.2)`: actual `none`(该声明已被删除)— FAIL
  - `.chat-user` background: expected `rgb(31,99,189)` actual `rgb(236, 236, 236)` — FAIL
  - `#state-badge` color: expected `rgb(31,99,189)` actual `rgb(58, 131, 247)` — FAIL
  - `.badge-answered` color: expected `rgb(106,106,106)` actual `rgb(143, 143, 143)` — FAIL
  通过项:`#stream-banner` border-top-color `rgb(138, 101, 8)`;`.kind-write .event-kind` bg `rgb(38, 117, 74)`;
  `.kind-done .event-kind` bg `rgb(0, 0, 0)`;`#btn-authorize` color/border/bg
  `rgb(38, 117, 74)` / `rgb(38, 117, 74)` / `rgb(233, 247, 239)`;`#btn-process-round` 与
  `#btn-authorize` 三属性逐字节相同;`#state-badge` background `rgb(238, 244, 255)`。
  构造说明:`.kind-write` / `.kind-done` / `.chat-user` 三处用应用自身的
  `renderEvent` / `appendChatMessage` 渲染探针节点(真实代码路径,零 AI 调用、零网络)。
  根因:见 `## Gaps`。

### 4. DevTools computed-style 抽查 — Plan 02(16 项)
expected: 间距按 D-16 账本落位(`.panel-header` 10px/16px、`#doc-pane` 32px/40px、`button` 6px/10px、
`.overlay-card` 24px(自 28px 吸附)、`#brainstorm-view` 24px(自 22px 吸附));
字号(`#brainstorm-view h2` 14px + `rgb(138,101,8)`、`#draft-view h2` 15px、`.panel-header h2` 14px、
`.overlay-card h3` 16px、`.markdown-body` 14px、`.markdown-body code` 13px(自 12.5px 折叠));
z-index(`#selection-menu` 200 / `#state-badge` 10 / `#stream-banner` 20);
冻结轮 box-shadow/opacity/filter;`#rounds-placeholder.archive-mode #round-doc` opacity `0.75`;任意 `button` color `rgb(26,26,26)`
result: [fail]
evidence: |
  24 条断言:**14 PASS / 9 FAIL / 1 BLOCKED**。失败项逐条 expected vs actual:
  - `.panel-header` padding-top: expected `10px` actual `6px` — FAIL
  - `.panel-header` padding-left: expected `16px` actual `10px` — FAIL
  - `#brainstorm-view h2` font-size: expected `14px` actual `16px` — FAIL
  - `#draft-view h2` font-size: expected `15px` actual `18px` — FAIL
  - `.overlay-card h3` font-size: expected `16px` actual `24px` — FAIL
  - `.markdown-body` font-size: expected `14px` actual `16px` — FAIL
  - `.markdown-body code` font-size: expected `13px` actual `14px` — FAIL
  - `#state-badge` z-index: expected `10` actual `auto`(该声明已被删除)— FAIL
  - `button` color: expected `rgb(26,26,26)` actual `rgb(13, 13, 13)` — FAIL
  阻塞项:`#doc-pane` padding —— **选择器不存在**(index.html 里实际是 `#doc-panel-body`);
  诊断读数 `#doc-panel-body` padding = `32px 40px`,与期望值一致,但元素 id 对不上,故记 blocked 而非 pass。
  通过项(摘要):`button` padding 6px/10px;`.overlay-card` padding-top 24px;
  `#brainstorm-view` margin-top 24px;`#brainstorm-view h2` color `rgb(138, 101, 8)`;
  `.panel-header h2` 14px;`#selection-menu` z-index 200;`#stream-banner` z-index 20;
  冻结轮 box-shadow/opacity/filter;archive opacity 0.75;
  **`S-2 DEPENDENCY --text-base = 14px`(一级字号档存活,Phase 5 SC5 / Phase 6 SC5 的下游门依赖它)**。
  探针口径说明(不是放宽判据):
  - `button` 指的是**通用 `button` 规则**(D-16 账本里的 6px/10px)。用 `#btn-enter` 作探针 ——
    它没有更具体的选择器覆盖;而 `document.querySelector('button')` 会落到 `#btn-send`
    (`#chat-input-row button`,0-1-1,8px/16px + 主色前景),那不是通用规则的探针。
  - `.markdown-body` 的规范消费者是 `#draft-content`;`document.querySelector('.markdown-body')`
    会落到 `#latest-check`(它也带该类且自带 font-size 覆盖)。
  - `#brainstorm-view` 的「24px」按 `margin-top` 判读(该元素上唯一的 24px);
    其 padding 是 D-16 映射的 `--space-3`/`--space-3-5`(12px/14px),已在日志中打印。
  - `.markdown-body code` 用应用自身的 `renderMarkdown` 渲染一个真实 `<code>` 元素后读数。
note: `14px` 存活为一级字号档是用户签核的 S-2 决定 —— Phase 5 SC5 / Phase 6 SC5 的下游门依赖它。

### 5. DevTools computed-style 抽查 — Plan 03(10 项)
expected: `#ai-route-select` border-top-color/background-color = `rgb(138,138,138)` / `rgb(255,255,255)`;
`.hint` color `rgb(106,106,106)` on `rgb(250,250,250)`;`#stream-banner` border-top-color `rgb(138,101,8)`;
`.markdown-body` color `rgb(26,26,26)` **肉眼可辨地**比 `.hint` 更深(这是 `ORDER 0.311` 的可观察形态);
外加一次「处理本轮批注」与一次「发送」交互无错误完成
result: [fail]
evidence: |
  默认运行(无 `--ai-smoke`):9 条断言 **3 PASS / 4 FAIL / 2 BLOCKED**。失败项:
  - `#ai-route-select` border-top-color: expected `rgb(138,138,138)` actual `rgb(217, 217, 217)` — FAIL
  - `.hint` color: expected `rgb(106,106,106)` actual `rgb(143, 143, 143)` — FAIL
  - `.hint` 实际背景: expected `rgb(250,250,250)` actual `rgb(255, 255, 255)` — FAIL
  - `.markdown-body` color: expected `rgb(26,26,26)` actual `rgb(13, 13, 13)` — FAIL
  通过项:`#ai-route-select` background `rgb(255, 255, 255)`;`#stream-banner` border-top-color
  `rgb(138, 101, 8)`;层级断言 `lum(.markdown-body)=0.0040 < lum(.hint)=0.2747`(ORDER 0.311 的可观察形态成立)。
  两次交互冒烟在默认运行下记 blocked(需要真实 AI 调用),理由写明「加 --ai-smoke 重跑」。
  **补充证据(另跑 `.venv/bin/python scripts/check-05-ui-uat.py --item 5 --ai-smoke`,claude CLI 可用)**:
  两条冒烟**都真实跑通、均 PASS**:
  - 「处理本轮批注」(p3,临时副本,真实 AI 调用):无 console 错误、无 http 4xx-5xx、无未捕获异常。
  - 「发送」(p12,临时副本,真实 AI 调用):同上。
  侧记:「发送」原在 p3 执行时,Playwright 报 `#btn-send` 被 `#annotations-panel` 的 `.panel-body`
  遮挡不可点(诊断 `elementFromPoint` = `panel-body`,非 `btn-send`)—— 阶段 3 主区由批注流占据,
  会话流的发送键被挤到不可点位置。故「发送」冒烟改在 p12(会话流的自然活动面)执行。
  这是本次实测的附带观察,不属于本 UAT 6 项的任何一条判据。

### 6. CR-06 渲染结果
expected: 一条普通的「已回应」批注 —— 用户批注与 AI 回应正文**都**以 `--color-text-muted` 渲染(D-11 意图的条目内层级)
result: [pass]
evidence: |
  2 条断言全部 PASS。在 p3 临时副本写入一条八字段齐全的「已回应」批注
  (`quote` 精确取自 round-2 文档真实文本「建议进入授权环节」),重进项目后展开 `<details>`:
  - `.annotation-note`(用户批注)color = `rgb(143, 143, 143)`
  - `.annotation-answer-body`(AI 回应正文)color = `rgb(143, 143, 143)`
  两者都等于运行时解析出的 `--color-text-muted`(`rgb(143, 143, 143)`)—— 本项判据以**令牌接线**表述,
  故按令牌解析值比对,未硬编码任何字面色。
note: 该修复只经代码审阅确认(`app.js:1147` 在已回应路径上创建 `annotation-answer-body`;
`.annotation-plain` 之外无其它规则为其着色)。是渲染行为变更,任何语法检查或守卫都无法确认。

## Summary

total: 6
passed: 3
issues: 3
pending: 0
skipped: 0
blocked: 0

## Gaps

<!-- 测试后如发现 issue,按 YAML 格式追加;此节直接喂给 /gsd-plan-phase --gaps -->

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

gaps:
  - test: 3
    item: "DevTools computed-style 抽查 — Plan 01(13 项)"
    severity: high
    observed: "15 条断言 7 FAIL / 8 PASS"
    failing:
      - ".hint color: expected rgb(106,106,106) actual rgb(143,143,143)"
      - ".badge-answered color: expected rgb(106,106,106) actual rgb(143,143,143)"
      - "#state-badge color: expected rgb(31,99,189) actual rgb(58,131,247)"
      - ".chat-user background: expected rgb(31,99,189) actual rgb(236,236,236)"
      - "#ai-route-select border-top-color: expected rgb(138,138,138) actual rgb(217,217,217)"
      - "#selection-menu border-top-color: expected rgb(138,138,138) actual rgb(217,217,217)"
      - ".overlay-card box-shadow 含 rgba(0,0,0,0.2): actual none"
    missing: "裁定 UAT 期望值或令牌值。若走 (a):按 HEAD 令牌层重写本项 7 条期望值。若走 (b):恢复 --gray-600=#6a6a6a / --gray-500=#8a8a8a / --blue-700=#1f63bd / --gray-200=#ececec→蓝,并恢复 .overlay-card 的 box-shadow 令牌。"

  - test: 4
    item: "DevTools computed-style 抽查 — Plan 02(16 项)"
    severity: high
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
    missing: "同上裁定。另:字号 5 档已由 13/14/15/16 上移到 14/16/18/24 —— 若确认接受,S-2 的「14px 一级档」由 --text-base=14px 继续满足(本项已单列 S-2 DEPENDENCY 断言并 PASS),但 Phase 5 SC5 / Phase 6 SC5 的下游门引用的具体字号需一并复核。"

  - test: 5
    item: "DevTools computed-style 抽查 — Plan 03(10 项)"
    severity: medium
    observed: "9 条断言 4 FAIL / 3 PASS / 2 BLOCKED(默认运行);--ai-smoke 补充运行下两条交互冒烟均 PASS"
    failing:
      - "#ai-route-select border-top-color: expected rgb(138,138,138) actual rgb(217,217,217)"
      - ".hint color: expected rgb(106,106,106) actual rgb(143,143,143)"
      - ".hint 实际背景: expected rgb(250,250,250) actual rgb(255,255,255)"
      - ".markdown-body color: expected rgb(26,26,26) actual rgb(13,13,13)"
    blocked:
      - "两条交互冒烟在默认运行下 blocked(需要真实 AI 调用);已用 --ai-smoke 补齐证据,两条均真实跑通并 PASS。默认运行的 blocked 不构成待办。"
    missing: "同上裁定(与前两项同根因)。附带观察:阶段 3 的 #btn-send 被 #annotations-panel 遮挡不可点,若认为会话流在阶段 3 仍应可用,需单开一项处理。"

# 另记(不属于 6 项判据,但本次实测到的真实 AA 倒退):
#   --color-text-muted = #8f8f8f 在 #ffffff 上 ratio = 3.23:1,低于 AA 4.5:1
#   (换肤前 #6a6a6a 在 #fafafa 上约 5.41:1)。受影响面包括 .hint / .badge-answered /
#   .markdown-body blockquote / .annotation-answer summary / .verdict-suggestion 等。
#   STATE.md 已记为「check-02 按用户知情决策红着交出(14 条失败)」,此处仅留痕。
```
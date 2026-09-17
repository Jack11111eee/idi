---
phase: 260917-fqh-b9664e0-hidden-flex
plan: 01
subsystem: ui
tags: [frontend, vanilla-js, css, css-specificity, inline-error, flexbox]

# Dependency graph
requires:
  - phase: 260916-t8g-ui-5-blocker-hidden-sse-onerror
    provides: 唯一全局 `.hidden` 规则、`showInlineError`/`clearInlineError` 与 `.inline-error`、错误内联投递通道
provides:
  - 修正后的 `.hidden` 注释理由(点名三个 ID 特异性 1-0-0 竞争者,`.overlay` 正确降级为 0-1-0 弱竞争者,移除幻影类名)
  - 错误内联锚点由 `#btn-process-round` 改为 `#probe-controls`(结构性修复,不打 CSS 补丁)
  - 三条视图切换路径(轮次切换 / 归档视图 / 撰写视图)清除陈旧内联错误
affects: [frontend, ui-audit-remediation, v1.14-phase-4, v1.14-phase-8]

# Actuals (#2632)
# tokens = chars/4 over realized diff content (3438 chars -> 859).
# NOTE: plan `estimate.raw_tokens: 14000` is a whole-task/context estimate, NOT a diff-size
# estimate — the two are not on the same scale. Do not read 859 vs 14000 as a 16x miss.
actuals:
  tokens: 859
  tasks: 3
  commits: 3
plan_head_before: 8a134f6

tech-stack:
  added: []
  patterns:
    - "结构性修复优先于 CSS 补丁:改锚点容器而非给 flex 行加 flex-wrap"
    - "区域门必须带 `(async )?` 前缀,否则 async 函数匹配为空、grep -c 恒 0(假门)"
    - "`!important` 的声明门用 `grep -c '!important;'`(带分号),裸 `!important` 会命中注释散文"

key-files:
  created: []
  modified:
    - frontend/style.css
    - frontend/app.js

key-decisions:
  - "锚点改为 `#probe-controls` 而非给该行加 `flex-wrap`:后者会改变探针行自身的换行行为,属产品行为变更而非缺陷修复"
  - "`inlineErrorEl` 单例「两个并发错误只显示一个」经裁定**不是缺陷**(单错误显示是既定的「下次动作即清除」设计),不修"
  - "`hidePhase3Extras`/`applyPhase3Extras` 不加 `clearInlineError()`:发散失败时状态不变(仍在阶段 1-2),锚点 `#divergence-entry` 不会已隐藏,构不成可达的残留场景"
  - "`loadChecksView` 已有 `clearInlineError()`(第 592 行),不重复添加"

patterns-established:
  - "错误内联锚点必须选块级流容器;flex 行内的控件作锚点会让错误成为额外的 flex 项"
  - "视图切换路径统一调 `clearInlineError()`,消除「锚点控件已隐藏而错误仍在屏上」"

requirements-completed: [REG-01, REG-02]

coverage:
  - id: D1
    description: ".hidden 注释的理由与实际竞争关系一致(三个 1-0-0 竞争者被点名、.overlay 降级为 0-1-0 弱竞争者、幻影类名移除);!important 声明与 .hidden 规则零改动"
    requirement: "REG-01"
    verification:
      - kind: unit
        ref: "grep -c '!important;' frontend/style.css == 1; grep -c '^\\.hidden {' == 1; grep -c '1-0-0' == 1; grep -c 'doc-subview' == 0"
        status: pass
      - kind: manual_procedural
        ref: "阅读 style.css:13-15 确认理由正确、声明行逐字未变"
        status: pass
  - id: D2
    description: "「处理本轮批注」失败时错误 <p> 落在整条探针行下方并占满容器宽度,不再成为 #probe-controls 内的第 6 个 flex 项"
    requirement: "REG-02"
    verification:
      - kind: automated_ui
        ref: "playwright:/tmp/uat/uat-260917.mjs#2a-2f(错误父级=#ai-panel-body、top 626 ≥ probe.bottom 614、宽度 388=388 100%、探针行 5 项 tops 全 492)"
        status: pass
      - kind: unit
        ref: "grep -c 'showInlineError(probeControls' == 2; grep -c 'showInlineError(processRoundBtn' == 0; grep -c 'showInlineError(' == 9(未变); grep -c 'flex-wrap' == 0"
        status: pass
  - id: D3
    description: "切换轮次 / 进入归档视图 / 切到撰写视图时清除陈旧内联错误"
    requirement: "REG-02"
    verification:
      - kind: automated_ui
        ref: "playwright:/tmp/uat/uat-260917.mjs#3b(切轮次后 .inline-error 0 个)、#3c(进入归档视图:1 → 0)"
        status: pass
      - kind: unit
        ref: "区域门 roundSwitcher=1 / applyArchiveView=1 / applyWritingView=1 / loadChecksView=1(未变) / hidePhase3Extras=0;grep -c 'clearInlineError();' == 9"
        status: pass

# 代写说明
authored_by: orchestrator
authored_by_reason: |
  执行器在三次任务提交**全部落地之后**卡死(600s 无进展,stream watchdog 未恢复),
  未写 SUMMARY.md。编排器独立复核了全部门禁与真实浏览器 UAT 后代写本文件。
  代码改动本身全部由执行器完成,编排器未改动任何 frontend/ 文件。
---

# 260917-fqh SUMMARY — 修复 b9664e0 自身引入的两条缺陷

## 一句话

修正 `b9664e0` 引入的三处"代码声称的行为与实际行为不符":`.hidden` 注释把 `!important` 的理由写反了;错误内联提示在 flex 行里被挤成窄列;视图切换时陈旧错误残留在屏上。

## 三条缺陷与修法

### 缺陷 1(REG-01)— `.hidden` 注释理由错误 · `frontend/style.css`

原注释声称 `!important` 之所以必需,是因为 `.overlay` / `.doc-subview` 等自身 `display` 特异性"同为 0-1-0 且声明在后"。**两个方向都错**:

| 原注释的说法 | 实际 |
|---|---|
| `.overlay` 是同级并列竞争者 | 它是 0-1-0,**最弱**的竞争者,仅因声明在 `.hidden` 之后才被覆盖 |
| `.doc-subview` 是竞争者 | 它在整个 style.css 中**没有任何 `display` 声明**,完全不是竞争者 |
| (未提及) | **漏掉三个决定性竞争者**:`#selection-menu` / `#annotations-panel` / `#checks-panel`,均以 **ID 特异性 1-0-0** 声明 `display: flex`,无论源码顺序都压过 `.hidden`(0-1-0) |

`!important` 的**结论正确**,未改动声明行。修正后的注释点名三个真正的 1-0-0 竞争者、把 `.overlay` 正确降级、移除幻影类名。

**为什么这条重要**:该规则是 STATE.md 记录的 **5 路单点故障**(44 处 `classList` 调用依赖它)。错误理由会成为后续任何"这个 `!important` 是不是冗余"清理的错误依据——照着错理由动手,5 个模态会同时渲染,`#cli-check-overlay` 会永久盖住整个应用。

### 缺陷 2(REG-02)— 错误内联提示被挤成窄列 · `frontend/app.js`

`showInlineError(processRoundBtn, …)` 把错误 `<p>` 插到 `#btn-process-round` 之后,但该按钮是 `#probe-controls { display: flex; gap: 8px }` 内 5 个横向 flex 项的**第 4 个**——错误于是成为**第 6 个 flex 项**,按内容宽度收缩,被挤在「处理本轮批注」与「中止」之间。

它同时通过了 grep 门与人工检查,因为它**确实**紧邻发起控件。

**修法(结构性,非 CSS 补丁)**:新增 `probeControls` 句柄,把两处 processRound 失败分支的锚点由按钮改为 `#probe-controls`。该容器是块级流中的 flex 容器(`margin-bottom: 12px`),错误 `<p>` 成为它的**块级后继**,落在整行下方、占满宽度。**未**给 `#probe-controls` 加 `flex-wrap`(那会改变探针行自身的换行行为)。其余四个调用点位于块级流容器,零改动。

### 缺陷 3(REG-02 顺带)— 视图切换不清除陈旧错误 · `frontend/app.js`

`clearInlineError()` 原本只在每次请求发起前调用。错误 `<p>` 是发起控件的兄弟节点、不带 `hidden` 类,所以视图切走后**控件被隐藏而错误仍在屏上**。

三条视图切换路径各补一次 `clearInlineError()`:轮次切换(`roundSwitcher` change 处理器,在 `Number.isFinite` 守卫之后、归档/常规分流之前——一处覆盖两种模式)、`applyArchiveView` 首行、`applyWritingView` 首行。

## 变更范围

```
frontend/app.js   +6 -2
frontend/style.css +4 -2
```

三次提交,每个任务一次:
- `fac268d` 修正 `.hidden` 注释的 `!important` 理由(REG-01)
- `46e8ea3` 内联错误锚点由按钮改为探针行容器(REG-02)
- `793071e` 视图切换时清除陈旧内联错误(REG-02)

## 验证证据

**门禁(编排器独立复跑,全部与计划规定值一致):**

```
!important;            = 1   (期望 1)   ← 声明门;裸 !important = 3 因注释散文
^\.hidden {            = 1   (期望 1)
1-0-0                  = 1   (期望 1,0→1 新理由落文)
doc-subview            = 0   (期望 0,1→0 幻影类名移除)
probeControls          = 3   (期望 3)
showInlineError(probeControls   = 2   (期望 2)
showInlineError(processRoundBtn = 0   (期望 0)
showInlineError(       = 9   (期望 9,未变——只换锚点)
clearInlineError();    = 9   (期望 9,6→9)
flex-wrap              = 0   (期望 0,未打 CSS 补丁)
区域门: roundSwitcher=1 applyArchiveView=1 applyWritingView=1 loadChecksView=1(未变) hidePhase3Extras=0
node --check frontend/app.js   通过
.venv/bin/python -m pytest -q -m "not slow"   219 passed, 6 deselected(与基线一致)
git diff --name-only 8a134f6..HEAD   仅 frontend/app.js frontend/style.css
```

**真浏览器 UAT(`/tmp/uat/uat-260917.mjs`,12/12 通过):**

| 检查 | 读数 |
|---|---|
| 2b 错误不再是 `#probe-controls` 的子元素 | 父级 `#ai-panel-body`(兄弟关系) |
| 2c 落在整条探针行下方 | err.top 626.0 ≥ probe.bottom 614.0 |
| 2d 全宽未被挤成窄列 | err.width 388.0 = probe.width 388.0(**100%**) |
| 2e 探针行 5 个控件布局未变 | tops 全为 492 |
| 2f 探针行自身几何未变 | width 388.0 → 388.0 |
| 3b 切轮次清除陈旧错误 | 剩余 `.inline-error` = 0 |
| 3c 进入归档视图清除陈旧错误 | 1 → 0(badge「使命完成」) |
| 4a-4c 不回归:进入失败仍全宽落在输入区下方 | 是 `#enter-form` 的紧邻后继兄弟;width 779.0 = 779.0 |

## 未覆盖项(如实记录)

1. **`applyWritingView` 的运行时路径未实测。** 撰写视图需阶段 4 状态,三个 UAT 造假项目(阶段 1-2 / 阶段 3 / 归档)都产生不了该状态。该路径只有**静态区域门**覆盖(`applyWritingView` 区域含 1 次 `clearInlineError()`)。
2. **REG-02 中「`inlineErrorEl` 单例丢弃两个并发错误中的一个」按裁定不修** —— 单错误显示是既定的「下次动作即清除」设计,非缺陷。`.planning/REQUIREMENTS.md` 的 REG-02 条文已同步加入该裁定。
3. **`#probe-controls` 的视觉重做/移除**不在本次范围(产品行为变更,STATE.md 已记为独立未来候选)。

## 方法论记录

**执行器两次卡死。** 本任务与 `260916-t8g` 同症状:任务全部完成并提交后,在写 SUMMARY 前 600s 无进展。两次都由编排器复核门禁与 UAT 后代写 SUMMARY。代码零编排器改动。

**计划阶段抓到一个假门。** 初稿的区域门写作 `awk '/^function loadChecksView/,/^}/'`,但 `loadChecksView` 声明为 **`async function`**(app.js:591),该模式匹配为空、`grep -c` 恒返回 **0** —— 一个永远不会失败的门。定稿前改为 `/^(async )?function …/` 并实测为 1。**编排器随后独立复跑了全部五个区域门的匹配行数**(applyArchiveView 20 / applyWritingView 15 / loadChecksView 70 / hidePhase3Extras 7 行 + roundSwitcher 完整匹配),确认无第二个空转门。

**计划还对未修改的树干预跑了三条 verify 链,确认全部 FAIL** —— 这是证明门非空转的唯一办法。上一份计划(`260916-t8g`)的教训正是"门通过 ≠ 缺陷不存在"。
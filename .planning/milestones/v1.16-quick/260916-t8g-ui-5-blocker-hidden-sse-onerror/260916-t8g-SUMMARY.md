---
phase: 260916-t8g-ui-5-blocker-hidden-sse-onerror
plan: 01
subsystem: ui
tags: [frontend, vanilla-js, css, sse, eventsource, keyboard-a11y, inline-error, archive-readonly]

# Dependency graph
requires:
  - phase: idi-03
    provides: 归档只读态(D-P3-25)、G3 授权行、自检面板与 check 报告视图
  - phase: idi-02
    provides: 划词批注菜单(selection-menu)、冻结轮呈现(D-P2-21)、轮次切换器
provides:
  - 唯一全局 `.hidden { display: none !important; }` 规则(替代 14 处逐选择器重复)
  - 归档只读态呈现层双保险(processRoundBtn 隐藏 + disabled;authorizeRow 隐藏)
  - SSE 断流可见横幅(#stream-banner,琥珀重连中 / 红色致命态)
  - 划词菜单键盘路径(roundDoc keyup,与 mouseup 共用 handleSelectionTrigger)
  - 失败内联提示(showInlineError/clearInlineError + .inline-error),5 处失败分支落到发起控件正下方
affects: [ui-audit-remediation, frontend, future-ui-phases]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
# tokens = chars/4 over realized diff content (added+removed lines, 6734 chars -> 1684).
# NOTE: plan `estimate.raw_tokens: 22000` appears to be a whole-task/context estimate,
# not a diff-size estimate — the two are NOT on the same scale. Do not read 1684 vs 22000
# as a 13x miss without accounting for that basis difference.
actuals:
  tokens: 1684
  tasks: 3
  commits: 3
plan_head_before: cd29df1

tech-stack:
  added: []
  patterns:
    - "全局单一 `.hidden` 工具类 + !important(对抗同特异性后置 display 声明)"
    - "失败内联提示:anchor.insertAdjacentElement('afterend') + textContent,单例 inlineErrorEl"

key-files:
  created: []
  modified:
    - frontend/style.css
    - frontend/app.js
    - frontend/index.html

key-decisions:
  - "全局 `.hidden` 必须带 !important:`.overlay { display: flex }` 等自身 display 声明特异性同为 0-1-0 且位于其后,去掉 !important 会让遮罩层/#state-badge/.doc-subview 等重新无法隐藏"
  - "键盘划词不做 keyup 按键白名单:处理器自身的「折叠/空白选区即关闭菜单」守卫已让非选择类按键成为安全 no-op,加白名单会引入第二处「哪些键产生选区」的真相来源"
  - "5 处失败分支用 showInlineError 替换而非叠加 renderEvent:与 sendMessage(1138)先例一致(单一通道),且这 5 处失败均发生在请求未被受理时,工作面板「事件原样直播」契约不损失内容"
  - "错误文案只经 textContent 写入(绝不用 innerHTML):服务端返回的 message 不进入解析路径(T-260916-01)"
  - "归档态 processRoundBtn 隐藏之外再 disabled = true:纵深防御,即使 CSS 未生效也不可点"

patterns-established:
  - "单一全局 `.hidden` 工具类:新增需要显隐的元素时不必再补逐选择器规则"
  - "内联错误单例模式:showInlineError 先清旧再插新,请求发起前 clearInlineError 满足「下一次动作即清除」"

requirements-completed: [UI-1.1, UI-1.2, UI-1.4, UI-2.5, UI-6.1, UI-6.2, UI-6.3]

coverage:
  - id: D1
    description: "`.hidden` 全局规则收口——5 个此前无匹配规则的元素(#draft-empty / #rounds-hint / #btn-process-round / #round-switcher / #writing-hint)的 classList('hidden') 由静默 no-op 变为真实生效"
    requirement: "UI-1.1 / UI-1.2 / UI-2.5"
    verification:
      - kind: automated_ui
        ref: "grep -c '\\.hidden {' frontend/style.css == 1; grep -c 'display: none' == 2; grep -c 'display: none !important' == 1"
        status: pass
    human_judgment: true
    rationale: "静态计数只能证明规则唯一且已收口,不能证明 5 个元素在真实 DOM/层叠上下文中按预期显隐(遮罩层、状态徽标、子视图的层叠行为需浏览器验证)"
  - id: D2
    description: "归档只读态加固:applyArchiveView 中 processRoundBtn 追加 disabled = true,authorizeRow 追加 classList.add('hidden');roundSwitcher 保持可见可切"
    requirement: "UI-6.3"
    verification:
      - kind: automated_ui
        ref: "grep -c 'processRoundBtn.disabled = true' frontend/app.js == 3; grep -c \"authorizeRow.classList.add('hidden')\" == 2"
        status: pass
    human_judgment: true
    rationale: "计数无法证明走完流程至 mission_complete 后三个交互面的实际可见性与可点性,需按 PLAN 人工检查第 3 条在真实归档项目上确认"
  - id: D3
    description: "SSE 断流可见化:#stream-banner 横幅,onerror 按 readyState 区分 CONNECTING(琥珀「正在自动重连」)/ CLOSED(红色「无法自动恢复」),onopen 清除"
    requirement: "UI-6.2"
    verification:
      - kind: automated_ui
        ref: "grep -c 'source.onerror' == 1; grep -c 'source.onopen' == 1; grep -c 'EventSource.CONNECTING' == 1; grep -c 'id=\"stream-banner\"' index.html == 1"
        status: pass
    human_judgment: true
    rationale: "断流/重连是运行时事件,静态检查无法证明横幅在真实断开与恢复时出现/消失(PLAN 人工检查第 5 条:停掉后端再恢复)"
  - id: D4
    description: "划词菜单键盘路径:mouseup 回调体逐字提取为具名 handleSelectionTrigger(),四条守卫只存在一份,同时绑定 mouseup 与 keyup"
    requirement: "UI-6.1"
    verification:
      - kind: automated_ui
        ref: "grep -c 'handleSelectionTrigger' == 3; mouseup 绑定 == 1; keyup 绑定 == 1"
        status: pass
    human_judgment: true
    rationale: "已知限制:#round-doc 是不可聚焦的普通 div,keyup 仅在焦点已落在容器内时生效(让容器可聚焦需 tabindex/role,属审计显式排除范围)。需人工确认「焦点先在文档区内」时 Shift+方向键划选能弹出菜单"
  - id: D5
    description: "失败内联提示:showInlineError/clearInlineError + .inline-error 样式,enterProject/divergence/approveDraft/processRound/loadChecksView 五处失败分支落到发起控件正下方,中文文案逐字保留"
    requirement: "UI-1.4"
    verification:
      - kind: automated_ui
        ref: "grep -c 'clearInlineError();' == 6; grep -c 'inline-error' style.css == 1; 旧 renderEvent 通道文案计数均为 0"
        status: pass
    human_judgment: true
    rationale: "需人工确认错误出现在输入框/按钮正下方而非右下 AI 工作面板,且再次点击时旧错误先消失(PLAN 人工检查第 6 条)"

# Metrics
duration: ~25min
completed: 2026-09-16
status: complete
---

# Phase 260916-t8g Plan 01: UI 审计 5 条功能性 BLOCKER 修复 Summary

**`hidden` 静默失效收口为单一全局规则、SSE 断流从「与空闲不可区分」变为可见横幅、归档只读态补上呈现层双保险、划词批注获得键盘路径、5 处请求失败从工作面板改投发起控件正下方**

## Performance

- **Duration:** ~25 min(近似;三个任务提交时间 22:37:40 → 22:44:04,Task 1 执行跨度含看门狗中断后由编排器代为提交)
- **Started:** 2026-09-16(计划提交于 21:10:12 +08:00)
- **Completed:** 2026-09-16T22:44:04+08:00
- **Tasks:** 3/3
- **Files modified:** 3

## Accomplishments

- **FIX 1(UI-1.1 / UI-1.2 / UI-2.5)**:`style.css` 新增唯一全局 `.hidden { display: none !important; }`,删除 14 处逐选择器冗余规则(153/205/208/255/259/278/385/475/503/513/517/539/559/580)。此前 `#draft-empty` / `#rounds-hint` / `#btn-process-round` / `#round-switcher` / `#writing-hint` 五个元素带 `hidden` 类却无任何匹配规则,`classList('hidden')` 全部是静默 no-op——草稿与「尚无草稿」同屏、轮次占位文案常驻、阶段 4/5 仍显示轮次切换器。
- **FIX 3(UI-6.3)**:`applyArchiveView` 中 `processRoundBtn` 在隐藏之外追加 `disabled = true`(纵深防御),`authorizeRow` 追加 `classList.add('hidden')`,补齐 DESIGN §7.4 / D-P3-25 列举的不可用交互面;`roundSwitcher` 保持可见可切(归档必须能浏览历史轮,有意保留)。
- **FIX 2(UI-6.2)**:`index.html` 新增 `#stream-banner`,`app.js` 的 `initEventSource` 注册 `onopen`(清除横幅)与 `onerror`(按 `readyState` 区分 CONNECTING → 琥珀「事件流已断开,正在自动重连……」/ CLOSED → 红色「事件流已断开且无法自动恢复,请刷新页面。」)。不手动重建 EventSource(它会自行重连),消除「断流 = 空闲」的不可区分态。
- **FIX 4(UI-6.1 / D-02)**:`initSelectionMenu` 的 mouseup 匿名回调体逐字提取为模块作用域具名函数 `handleSelectionTrigger()`,四条守卫(冻结轮 / 非 phase3 / 折叠或空白选区 / 选区不在 roundDoc 内)原样保留且只存在一份,`mouseup` 与 `keyup` 共用同一处理器。
- **FIX 5(UI-1.4)**:新增 `inlineErrorEl` + `clearInlineError()` / `showInlineError(anchor, message)`(只用 `textContent`)+ `.inline-error` 样式;enterProject / divergence / approveDraft / processRound / loadChecksView 五处失败分支由 `renderEvent` 工作面板通道改为内联到发起控件正下方,中文文案逐字保留,每处请求发起前 `clearInlineError()`。

## Task Commits

Each task was committed atomically:

1. **Task 1: `.hidden` 全局规则收口 + 归档只读态加固** - `ed14c6e` (fix)
2. **Task 2: SSE 断流可见化** - `f7eae48` (fix)
3. **Task 3: 键盘划词路径 + 错误内联** - `0912429` (fix)

**Plan metadata:** 本次执行不提交 docs 产物(SUMMARY.md / STATE.md / PLAN.md)——由编排器统一提交。

## Files Created/Modified

- `frontend/style.css` — 新增全局 `.hidden`(!important)、`.inline-error`、`#stream-banner` + `#stream-banner.fatal`;删除 14 处逐选择器 `.hidden` 规则
- `frontend/app.js` — `streamBanner` 句柄 + `showStreamBanner`/`hideStreamBanner`;`initEventSource` 的 `onopen`/`onerror`;`inlineErrorEl` + `clearInlineError`/`showInlineError`;`handleSelectionTrigger` 提取与 `mouseup`/`keyup` 双绑定;5 处失败分支改内联;`applyArchiveView` 两行加固
- `frontend/index.html` — `#state-badge` 后新增 `<div id="stream-banner" class="hidden"></div>`

## Decisions Made

- **全局 `.hidden` 的 `!important` 是必需的,不是可清理的冗余**:`.overlay { display: flex }`(style.css:144)、`.doc-subview`、`#state-badge` 等自身 `display` 声明特异性同为 0-1-0 且位于其后,去掉 `!important` 会让这些容器重新无法隐藏,整条修复静默回退。已在 CSS 注释中写明该约束。
- **不对 `keyup` 做 Shift/Arrow 白名单**:处理器自身的「折叠/空白选区即关闭菜单」守卫已让非选择类按键成为安全 no-op(且顺带正确关闭陈旧菜单);加白名单会引入第二处「哪些键会产生选区」的真相来源,与浏览器实际行为漂移。
- **5 处失败分支用 `showInlineError` 替换而非叠加 `renderEvent`**:与 `sendMessage`(app.js:1138)既有先例一致(单一通道,避免同一条错误在屏上出现两遍);且这 5 处失败全部发生在请求未被受理时(HTTP 非 2xx),没有任何 AI 工作事件产生,工作面板「事件原样直播」契约不损失内容。
- **错误文案只经 `textContent` 写入**:服务端返回的 `message` 不进入 HTML 解析路径(T-260916-01 缓解措施落地)。
- **`loadChecksView` 失败分支按源码实际处理**:原实现是 `checkState.textContent = '报告拉取失败';`,**不调用** `renderEvent`(与计划任务描述不符),故改为 `showInlineError(checkSwitcher, '报告拉取失败')`,未额外引入 renderEvent 通道。

## Deviations from Plan

### Auto-fixed Issues

None — 三个任务的实现均严格按计划执行,未触发 Rule 1-3 的任何自动修复。

### Plan arithmetic correction applied (orchestrator-supplied, pre-dispatch)

**1. Task 1 `<automated>` 门的 `processRoundBtn.disabled = true` 期望值**

- **Found during:** 执行前基线测量
- **Issue:** 计划断言改动后计数为 `2`,但改动前实测基线已是 `2`(`app.js:1122` 在 `updateFrozenPresentation` 冻结轮分支、`app.js:1385` 在 processRound 点击处理器的 busy 守卫),Task 1 新增第三处后正确值为 `3`。
- **Fix:** 采用编排器预先下发的 CORRECTION 1,门改为 `= "3"`;两处既有 `disabled = true` 一律未删改(实测改动后 = 3,与预期一致)。
- **Files modified:** 无(仅门断言口径修正,不改代码)
- **Verification:** `grep -c 'processRoundBtn.disabled = true' frontend/app.js` = 3
- **Committed in:** 不适用(基线口径修正)

### Unresolved gate discrepancy (NOT auto-fixed — reported per orchestrator instruction)

**2. Task 3 `<automated>` 门的 `showInlineError(` 期望值与计划自身动作描述互相矛盾**

- **Found during:** Task 3 收口验证
- **Issue:** 门断言 `grep -c 'showInlineError(' frontend/app.js` = `6`,计划 `<verification>` 亦注明「期望 6(1 定义 + 5 调用)」。但同一计划的 Task 3 `<action>` 第 8 条明确要求 divergence / approveDraft / processRound **三个处理器的 `!resp.ok` 分支与 `catch` 分支都改为** `showInlineError`——即 3 个处理器各 2 处调用,加上 enterProject 1 处、loadChecksView 1 处 = **8 处调用**,再加 1 处函数定义 = **9 行**。门的「5 调用」与计划自身的动作描述不一致。
- **Fix:** **未做任何代码改动以迁就计数。** 按编排器指令「不要靠删既有代码/删分支来凑数」,保留了全部 8 处调用(错误分支覆盖完整),实测值为 **9**。
- **Actual measured:** `grep -c 'showInlineError(' frontend/app.js` = **9**(1 定义 @304 + 8 调用 @322/595/1452/1461/1502/1505/1526/1539)
- **Impact:** 若把该门当作硬门槛,Task 3 的自动化门会报失败;但**其余 7 条断言全部通过**,且把计数改成 6 的唯一办法是删除 3 个 `catch` 分支的内联错误处理——那会让网络异常重新失去用户可见反馈,属功能回退。建议将该门期望值修正为 `9`。
- **Files modified:** 无
- **Verification:** 逐条列出 9 处行号(见上);`grep -c 'clearInlineError();'` = 6 与门一致(1 处在 `showInlineError` 内 + 5 处请求发起前)
- **Committed in:** 不适用(未改代码)

---

**Total deviations:** 0 auto-fixed;1 条编排器预先下发的口径修正已应用;1 条门算术矛盾**按指示上报而未以改代码方式掩盖**。
**Impact on plan:** 五条 BLOCKER 的功能目标全部达成,改动范围严格限于三个前端文件。唯一的未闭合项是 Task 3 门中 `showInlineError(` 的期望数字,属计划文本的算术错误而非实现缺陷。

## Issues Encountered

- **pytest 基线含 4 项既有失败(与本次改动无关)**:`backend/tests/test_ai_caller.py` 的 4 个 `normalize_sdk_*` 用例因本机未安装 `claude_agent_sdk`(`ModuleNotFoundError: No module named 'claude_agent_sdk'`)而失败。改动前后逐项一致:**4 failed, 215 passed, 6 deselected**(注:编排器核验时报告的「219 passed」为 collect 口径;本机实测 passed 数为 215,两处失败计数相同,属同一既有环境缺口)。本次零后端改动,该失败为环境依赖缺失,已按 SCOPE BOUNDARY 判定为范围外,未修复。
- **Task 1 执行期间被执行看门狗判定停滞**:中断后由编排器代为提交 Task 1(`ed14c6e`)。本代理已核验其提交内容与基线口径(`.hidden {` 14→1、`display: none` 15→2、`!important` =1、`processRoundBtn.disabled = true` =3、`authorizeRow.classList.add('hidden')` =2)后继续执行 Task 2/3,未重复提交 Task 1。

## Known Limitations

- **键盘划词的焦点前提(计划已记录,不在本次范围)**:`#round-doc` 是普通 `<div class="markdown-body">`,默不可聚焦,因此 `keyup` 只在焦点已落在该容器内时生效。让容器可聚焦需要加 `tabindex`/`role`,属审计显式排除的 aria/role 范围,本次不触碰。即:键盘路径已具备,但「先聚焦文档区」这一步仍需鼠标点击一次。
- **归档态 `processRoundBtn.disabled = true` 不是跨项目锁死**:`loadRoundView` → `updateFrozenPresentation(true)` 会把它复位为 `processInFlight`,切出归档态后按钮可正常恢复。

## Known Stubs

None — 本次改动未引入任何硬编码空值、占位文案或未接数据源的组件。五处内联错误提示均为真实失败分支的完整实现。

## Threat Flags

None — 本次改动未引入计划 `<threat_model>` 之外的新信任边界。新增的 `#stream-banner` 文案全部为代码内写死的中文字面量,无外部输入参与拼接(T-260916-04 accept 已覆盖);`showInlineError` 的服务端字符串入口按 T-260916-01 以 `textContent` 落地。

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- 五条功能性 BLOCKER(UI-1.1 / UI-1.2 / UI-1.4 / UI-2.5 / UI-6.1 / UI-6.2 / UI-6.3)代码侧已闭合,`git diff --stat` 相对计划提交 `cd29df1` 仅三个前端文件(`frontend/app.js` +122/-54 区间、`frontend/index.html` +3、`frontend/style.css`),无第四个文件。
- **待人工 UAT**:前端无 pytest 覆盖,PLAN `<verification>` 的 6 条人工检查为 Nyquist 缺口的显式补偿,尚未执行(需启动本地服务)。建议在 `/gsd-verify-work` 阶段逐条走查,尤其第 1、2、4 条(依赖真实项目的阶段状态)。
- **已知未闭合项**:Task 3 自动化门 `showInlineError(` 期望值(计划写 6,实测 9)需修正;`#round-doc` 可聚焦性作为独立议题留给后续 UI 阶段。

---

*Phase: 260916-t8g-ui-5-blocker-hidden-sse-onerror*
*Completed: 2026-09-16*

## Self-Check: PASSED

- `frontend/index.html` — FOUND
- `frontend/style.css` — FOUND
- `frontend/app.js` — FOUND
- `.planning/quick/260916-t8g-ui-5-blocker-hidden-sse-onerror/260916-t8g-SUMMARY.md` — FOUND
- Commit `ed14c6e` (Task 1) — FOUND
- Commit `f7eae48` (Task 2) — FOUND
- Commit `0912429` (Task 3) — FOUND
- `git diff --name-only cd29df1 HEAD` = 三个前端文件,无第四个 — PASSED
- `node --check frontend/app.js` — PASSED
- `python -m pytest -q -m "not slow"` — 4 failed / 215 passed / 6 deselected,与改动前基线逐项一致(4 项失败为既有环境缺口,缺 `claude_agent_sdk`)
- 未提交 docs 产物(SUMMARY.md 保持 untracked,交由编排器提交);`.claude/settings.local.json` 的既有改动未被 stage/提交/回滚 — PASSED
- 唯一未闭合项:Task 3 门 `showInlineError(` 期望 6 与实测 9 不符(计划算术矛盾,已按指示上报,未以改代码方式掩盖)
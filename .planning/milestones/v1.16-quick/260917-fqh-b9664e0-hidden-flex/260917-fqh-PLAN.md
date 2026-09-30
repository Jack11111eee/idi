---
phase: 260917-fqh-b9664e0-hidden-flex
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - frontend/style.css
  - frontend/app.js
autonomous: true
requirements:
  - REG-01
  - REG-02
user_setup: []

estimate:
  tokens: 14000
  raw_tokens: 14000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "style.css 的 `.hidden` 注释给出的理由与实际竞争选择器一致:三个 ID 特异性(1-0-0)竞争者被点名,`.overlay` 被正确表述为 0-1-0 的弱竞争者(靠源码顺序才被覆盖),那个在 style.css 中根本没有 display 声明的类名不再被提及(REG-01)"
    - "`.hidden` 规则本身一字未改——仍是全文件唯一一条,仍带 `!important`(REG-01)"
    - "「处理本轮批注」失败时,错误 `<p>` 落在整条探针行下方并占满容器宽度,不再成为 `#probe-controls` 内的第 6 个 flex 项被挤成窄列(REG-02)"
    - "切换轮次、进入归档视图、切到撰写视图时,屏上陈旧的内联错误被清除,不再出现「锚点控件已隐藏而错误仍在屏上」(REG-02)"
    - "其余四个 `showInlineError` 调用点的锚点与行为零改动(它们位于块级流容器,无窄列问题)(REG-02)"
  artifacts:
    - "frontend/style.css:理由修正后的 `.hidden` 注释;声明行 `.hidden { display: none !important; }` 保持原样"
    - "frontend/app.js:`probeControls` DOM 句柄;两处 processRound 失败分支的锚点由 `processRoundBtn` 改为 `probeControls`"
    - "frontend/app.js:`roundSwitcher` change 处理器 / `applyArchiveView` / `applyWritingView` 各新增一次 `clearInlineError()`"
  key_links:
    - "showInlineError(probeControls, …) → #probe-controls 的 afterend → 错误 <p> 成为探针行的块级后继(全宽),而非 #probe-controls 内的第 6 个 flex 项"
    - "视图切换路径 → clearInlineError() → inlineErrorEl.remove() + 置 null,消除陈旧错误残留态"
---

<objective>
修复 `b9664e0`(quick 260916-t8g)自身引入的两条缺陷,并补齐同一特性的一处遗漏:`.hidden` 注释的理由写反了(REG-01);错误内联提示在 `#probe-controls` 这个 flex 行里被挤成窄列(REG-02);视图切换时不调 `clearInlineError()`,陈旧错误残留在屏上(REG-02 顺带项)。

Purpose: 这三条都是"代码声称的行为与实际行为不符"。注释声称的隐藏机制理由是错的——它把决定性的 ID 特异性竞争者和一个根本不存在的竞争者弄反了,后续任何"这个 `!important` 是不是冗余"的清理都会照着错理由下手,而 `!important` 恰恰是本里程碑 P8 记录的 5 路单点故障(`.planning/STATE.md` Blockers: `.hidden { display: none !important }` 是 5 路单点故障)。另两条是 `b9664e0` 新引入的错误投递通道的呈现缺陷:它在 grep 门与人工检查下都"通过"了(错误确实紧邻发起控件),但视觉上被 flex 行压成窄列、且视图切换后不消失。

Output: 两文件改动(`frontend/style.css`、`frontend/app.js`),零后端改动、零新增依赖、零设计令牌层。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/STATE.md
@.planning/REQUIREMENTS.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/CLAUDE.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/CLAUDE.md
@frontend/style.css
@frontend/app.js
@frontend/index.html
@.planning/quick/260916-t8g-ui-5-blocker-hidden-sse-onerror/260916-t8g-PLAN.md

**约束(项目 CLAUDE.md §2 简单优先 / §3 外科手术式改动):** 每一行改动都必须能追溯到下述三条缺陷之一。不重排格式、不"顺手改进"相邻代码、不删除既存死代码、不引入设计令牌层。总 diff 应远小于 30 行。

**源码事实基线(已由编排器逐条核对,执行期不要重新推导,直接按此施工):**

- `frontend/style.css:13-15` 现状:
  - 13-14 行是注释散文,声称 `.overlay` / 那个 `.doc-*` 类名与 `.hidden` 同为 0-1-0 且声明在后。
  - 15 行是唯一声明:`.hidden { display: none !important; }`。**结论正确,不得改动此行。**
- 实际竞争关系(已 grep 核对):
  - `#selection-menu`(style.css:480-483,`display: flex`)、`#annotations-panel`(397)、`#checks-panel`(565) 三条均为 **ID 特异性 1-0-0**,压过 `.hidden`(0-1-0),与源码顺序无关。**这才是 `!important` 的真正理由,现注释一字未提。**
  - `.overlay`(style.css:151-159,`display: flex`)是 **0-1-0**,与 `.hidden` 同特异性,靠源码顺序决定胜负——它在 151 行,位于 15 行之后。它是**较弱**的竞争者,不是原注释所称的同级并列。
  - 原注释点名的那个类名在**整个 style.css 中没有任何规则**(`grep -n` 仅命中 13 行的注释本身),即它**根本没有 `display` 声明**,完全不是竞争者。
- `frontend/index.html:134-143`:`#probe-controls { display: flex; gap: 8px; }`(style.css:62-66)内含 5 个横向子项——`#ai-route-select`、`#project-path-input`、`#btn-ping`、`#btn-process-round`、`#btn-abort`。`#btn-process-round` 是第 4 个。
- `frontend/app.js:295-311`:`inlineErrorEl` 单例 + `clearInlineError()` + `showInlineError(anchor, message)`(用 `insertAdjacentElement('afterend')`,只用 `textContent`)。
- `frontend/app.js` 现有 8 个 `showInlineError` 调用点:`322`(锚点 `enterForm`)、`595`(锚点 `checkSwitcher`)、`1452`/`1461`(锚点 `processRoundBtn`,同一失败的两个分支)、`1502`/`1505`(锚点 `divergenceBtn`)、`1526`/`1539`(锚点 `approveDraftBtn`)。
- 四个非 processRound 调用点的锚点容器(`#enter-form` 是 index.html:16 的块级 div、`#divergence-entry`、`#approve-row`、`#checks-panel .panel-body`)都位于块级流,错误 `<p>` 落点正常——**不得修改它们**。
- `frontend/app.js:1237-1245`:`roundSwitcher` 的 `change` 处理器,先 `Number.isFinite` 守卫,再按 `currentState === 'mission_complete'` 分流到 `loadArchiveRoundDoc(n)`(归档)或 `loadRoundView(n)`。这是轮次切换的唯一入口,两种模式共用。
- `frontend/app.js:810-829`:`applyArchiveView(data)`——进入归档视图。
- `frontend/app.js:450-464`:`applyWritingView(data)`——切到撰写视图。
- `frontend/app.js:580-588`:`applyPhase5View` → `loadChecksView`(591),而 `loadChecksView` 的**第一行(592)已经是 `clearInlineError()`**——自检视图路径**已经覆盖**,不要重复添加。

**明确不在范围内(即使它们看起来相邻):**
- `inlineErrorEl` 单例"两个并发错误只显示一个"——单错误显示是既定的"下次动作即清除"设计,不是缺陷。
- `#probe-controls` 的视觉改造或移除(产品行为变更,`STATE.md` 已记为独立未来候选)。
- 给 `#probe-controls` 加 `flex-wrap`——那会改变探针行自身的换行行为,是 CSS 补丁而非结构性修复。
- 设计令牌层、配色/间距/字号改动、`:focus` 样式、aria/role 属性。
- style.css 中其余 `display: none` 出现处(`.panel-body.collapsed` 等)。
- `hidePhase3Extras()` / `applyPhase3Extras()` 不加 `clearInlineError()`:发散错误的锚点 `#divergence-entry` 在阶段 1-2 才可见,而发散失败时状态不变(仍在阶段 1-2),构不成"锚点已隐藏而错误残留"的可达场景。**不要**顺手加。
</context>

<tasks>

<task type="auto">
  <name>Task 1: 修正 `.hidden` 注释的理由(REG-01)</name>
  <files>frontend/style.css</files>
  <read_first>
    frontend/style.css:13-15(待替换的注释 + 声明行)
    frontend/style.css:151-159(`.overlay` 的 display: flex,0-1-0)
    frontend/style.css:397-399、480-483、565-567(三个 ID 特异性 1-0-0 竞争者)
  </read_first>
  <action>
用**下述文本整体替换 style.css 第 13-14 两行注释散文**,第 15 行的声明行一字不动(仅替换注释,不碰 `.hidden { display: none !important; }`):

```
/* 唯一全局显隐规则:!important 必需——#selection-menu / #annotations-panel /
   #checks-panel 以 ID 特异性(1-0-0)声明 display: flex,压过 .hidden(0-1-0),
   与声明先后无关;.overlay(0-1-0)是较弱的竞争者,仅因声明在本规则之后才被覆盖。
   去掉 !important 会让上述容器重新无法隐藏。 */
```

要求与理由(逐条对应本缺陷的两个方向):
1. **补上决定性理由**:三个 ID 特异性竞争者是 `!important` 的真正原因——1-0-0 压过 0-1-0,源码顺序不起作用。原注释完全没提它们。
2. **正确降级 `.overlay`**:它是 0-1-0 的**弱**竞争者,靠源码顺序(151 行在 15 行之后)才被本规则覆盖;原注释把它说成与 `.hidden` 同级的并列,是错的。
3. **删除那个幻影类名**:原注释点名的第二个类名在 style.css 里没有任何规则、没有任何 `display` 声明,不是竞争者。新注释不再提及它(上面给出的文本里已经不含它,照抄即可)。
4. **`!important` 的结论保持不变**——不删除、不改写、不"顺手清理"该声明。理由被修正,结论不变。
5. 新注释散文中**不得出现带分号的 `!important;` 字面量**(会污染 Task 1 的门计数模式)。上面给出的文本只含不带分号的 `!important`,照抄即可。
6. 注释里不要写 `.doc-` 开头的任何类名——这是第 3 条的落实方式。
  </action>
  <verify>
    <automated>test "$(grep -c '!important;' frontend/style.css)" = "1" && test "$(grep -c '^\.hidden {' frontend/style.css)" = "1" && test "$(grep -c '1-0-0' frontend/style.css)" = "1" && test "$(grep -c 'doc-subview' frontend/style.css)" = "0" && test "$(grep -c 'display: none !important' frontend/style.css)" = "1" && node --check frontend/app.js && .venv/bin/python -m pytest -q -m "not slow"</automated>
  </verify>
  <done>
- `frontend/style.css` 第 13-15 行区域:注释散文已替换为上文给定文本;声明行 `.hidden { display: none !important; }` 与改动前逐字一致。
- 门计数(改动前 → 改动后,均已实测):
  - `grep -c '!important;' frontend/style.css`:1 → **1**(唯一的声明门;`grep -c '!important'` 返回 3 是因为其中 2 行是注释散文,**不得**用裸 `!important` 作为门)
  - `grep -c '^\.hidden {' frontend/style.css`:1 → **1**
  - `grep -c '1-0-0' frontend/style.css`:0 → **1**(新理由已落文)
  - `grep -c 'doc-subview' frontend/style.css`:1 → **0**(幻影类名已从注释移除)
  - `grep -c 'display: none !important' frontend/style.css`:1 → **1**
- `node --check frontend/app.js` 通过;`.venv/bin/python -m pytest -q -m "not slow"` 与基线逐项一致(**219 passed, 6 deselected**)。
- 本任务 diff 仅触及 style.css 的注释两行,无其他改动。
  </done>
</task>

<task type="auto">
  <name>Task 2: 错误内联锚点由按钮改为探针行容器(REG-02)</name>
  <files>frontend/app.js</files>
  <read_first>
    frontend/index.html:134-143(`#probe-controls` 的 5 个横向子项)
    frontend/style.css:62-66(`#probe-controls { display: flex; gap: 8px; margin-bottom: 12px; }`)
    frontend/app.js:44-48(阶段 3 句柄区,`processRoundBtn` 所在)
    frontend/app.js:1440-1465(processRound 的两个失败分支)
  </read_first>
  <action>
**结构性修复,不给 flex 行打 CSS 补丁。**

1. **新增 DOM 句柄**:在 app.js 第 47 行 `const processRoundBtn = document.getElementById('btn-process-round');` 之后新增一行:
   `const probeControls = document.getElementById('probe-controls');`
   (该句柄此前不存在——`grep -c 'probeControls' frontend/app.js` 基线为 0。)

2. **改锚点**:把 processRound 失败的两个分支的锚点从 `processRoundBtn` 改为 `probeControls`——即第 1452 行的 `showInlineError(processRoundBtn, \`处理发起失败:${err.message || resp.status}\`)` 与第 1461 行的 `showInlineError(processRoundBtn, '处理请求失败(网络)')`,两处**只改第一个实参**,错误文案逐字保留、两分支内的 `processInFlight = false` 与按钮文案/禁用复位逻辑原样保留。

3. **为什么是结构性修复**:`#probe-controls` 是普通块级流中的 flex 容器(`margin-bottom: 12px`),`insertAdjacentElement('afterend')` 插入的 `<p>` 成为它的**块级后继**——落在整条探针行下方、占满容器宽度,不再是行内第 6 个 flex 项。改用 `#probe-controls` 作锚点后,`#ai-route-select`、`#project-path-input`、`#btn-ping`、`#btn-abort` 与 `#btn-process-round` 五项的布局完全不受影响。

4. **禁止**:给 `#probe-controls` 加 `flex-wrap` 或其他 CSS 补丁(会改变探针行自身的换行行为,属产品行为变更);改动 `#probe-controls` 的 DOM 结构;改动 `clearInlineError()` 或 `showInlineError()` 的实现;触碰其余四个调用点(`enterForm` / `divergenceBtn` / `approveDraftBtn` / `checkSwitcher`)——它们位于块级流容器,无此问题。
  </action>
  <verify>
    <automated>node --check frontend/app.js && test "$(grep -c "const probeControls = document.getElementById('probe-controls')" frontend/app.js)" = "1" && test "$(grep -c 'showInlineError(probeControls' frontend/app.js)" = "2" && test "$(grep -c 'showInlineError(processRoundBtn' frontend/app.js)" = "0" && test "$(grep -c 'showInlineError(' frontend/app.js)" = "9" && test "$(grep -c 'probeControls' frontend/app.js)" = "3" && test "$(grep -c 'flex-wrap' frontend/style.css)" = "0" && .venv/bin/python -m pytest -q -m "not slow"</automated>
  </verify>
  <done>
- app.js 含唯一 `probeControls` 句柄;两处 processRound 失败分支的锚点为 `probeControls`,文案与两分支的复位逻辑逐字未变。
- 门计数(改动前 → 改动后,均已实测):
  - `grep -c 'probeControls' frontend/app.js`:0 → **3**(1 句柄 + 2 调用)
  - `grep -c 'showInlineError(probeControls' frontend/app.js`:0 → **2**
  - `grep -c 'showInlineError(processRoundBtn' frontend/app.js`:2 → **0**
  - `grep -c 'showInlineError(' frontend/app.js`:9 → **9**(调用点总数不变,只换锚点)
  - `grep -c 'flex-wrap' frontend/style.css`:0 → **0**(未引入 CSS 补丁)
- `node --check` 通过;`.venv/bin/python -m pytest -q -m "not slow"` 与基线一致(**219 passed, 6 deselected**)。
- 其余四个调用点的锚点未改动。
  </done>
</task>

<task type="auto">
  <name>Task 3: 视图切换时清除陈旧内联错误(REG-02)</name>
  <files>frontend/app.js</files>
  <read_first>
    frontend/app.js:295-311(clearInlineError / showInlineError 实现)
    frontend/app.js:450-464(applyWritingView)
    frontend/app.js:580-597(applyPhase5View → loadChecksView,注意 592 行已有 clearInlineError)
    frontend/app.js:810-829(applyArchiveView)
    frontend/app.js:1237-1245(roundSwitcher change 处理器)
  </read_first>
  <action>
错误 `<p>` 是发起控件的兄弟节点、不带 `hidden` 类,所以视图切走后控件被隐藏而错误**仍在屏上**。在三条视图切换路径上各新增一次 `clearInlineError();`——共 3 行:

1. **轮次切换**——`roundSwitcher` 的 `change` 处理器(app.js:1237-1245):在 `if (!Number.isFinite(n)) return;` 守卫**之后**、`if (currentState === 'mission_complete')` 分流**之前**插入 `clearInlineError();`。这是轮次切换的唯一入口,归档态与常规态两种分流共用同一行,故只需一处。放在守卫之后是因为非法值不构成一次视图切换。
2. **进入归档视图**——`applyArchiveView(data)`(app.js:810)函数体**第一行**插入 `clearInlineError();`。
3. **切到撰写视图**——`applyWritingView(data)`(app.js:450)函数体**第一行**插入 `clearInlineError();`。

**不要**给 `loadChecksView` 或 `applyPhase5View` 添加:`loadChecksView` 的第一行(app.js:592)已经是 `clearInlineError();`,自检视图路径已覆盖,重复添加属越界改动。

**不要**给 `hidePhase3Extras()` / `applyPhase3Extras()` 添加(理由见 context 的"明确不在范围内"末条)。
  </action>
  <verify>
    <automated>node --check frontend/app.js && test "$(grep -c 'clearInlineError();' frontend/app.js)" = "9" && test "$(awk '/^roundSwitcher\.addEventListener\(.change./,/^}\);/' frontend/app.js | grep -c 'clearInlineError();')" = "1" && test "$(awk '/^(async )?function applyArchiveView/,/^}/' frontend/app.js | grep -c 'clearInlineError();')" = "1" && test "$(awk '/^(async )?function applyWritingView/,/^}/' frontend/app.js | grep -c 'clearInlineError();')" = "1" && test "$(awk '/^(async )?function loadChecksView/,/^}/' frontend/app.js | grep -c 'clearInlineError();')" = "1" && test "$(awk '/^(async )?function hidePhase3Extras/,/^}/' frontend/app.js | grep -c 'clearInlineError();')" = "0" && .venv/bin/python -m pytest -q -m "not slow"</automated>
  </verify>
  <done>
- 三条视图切换路径各含一次 `clearInlineError()`;`loadChecksView` 仍恰好一次(未重复添加);`hidePhase3Extras` 零次(未越界)。
- 门计数(改动前 → 改动后,均已实测):
  - `grep -c 'clearInlineError();' frontend/app.js`:6 → **9**
  - `roundSwitcher` change 处理器区域:`0 → **1**`
  - `applyArchiveView` 区域:`0 → **1**`
  - `applyWritingView` 区域:`0 → **1**`
  - `loadChecksView` 区域:`1 → **1**(未变)`
  - `hidePhase3Extras` 区域:`0 → **0**(未变)`
- `node --check` 通过;`.venv/bin/python -m pytest -q -m "not slow"` 与基线一致(**219 passed, 6 deselected**)。
- 本任务 diff 恰为 3 行新增,无其他改动。
  </done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | 来源 → 去向 | 说明 |
|----------|-------------|------|
| 后端错误响应 → DOM | `/api/*` 的 `{message}` / `{status}` → `showInlineError` 文案 | 不可信字符串进入前端渲染管线(本次仅改锚点,不改写入方式) |
| CSS 规则优先级 | `.hidden`(0-1-0) vs 三个 ID 特异性竞争者(1-0-0) | 本次只改注释理由,不改优先级决策本身 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|-----------|-----------|----------|-------------|-----------------|
| T-260917-01 | Tampering / Injection | `showInlineError(probeControls, message)`(app.js:1452/1461) | low | accept | 本次只替换第一个实参(锚点),写入方式未变——仍为 `createElement('p')` + `textContent`,服务端返回的 `message` 不进入解析路径。注入面与改动前完全相同,无新增风险 |
| T-260917-02 | Elevation of Privilege(隐藏机制失效) | `.hidden { display: none !important; }`(style.css:15) | high | mitigate | 该规则是 STATE.md 记录的 5 路单点故障。本任务只改注释、不动声明,并用 `grep -c '!important;'` = 1 与 `grep -c '^\.hidden {'` = 1 双门锁死;修正后的注释把真正的理由(三个 1-0-0 竞争者)写清楚,消除后续"`!important` 冗余可清理"的错误依据 |
| T-260917-03 | Denial of Service(可用性) | 陈旧内联错误残留(app.js 视图切换路径) | low | mitigate | 三条切换路径各加 `clearInlineError()`,消除"控件已隐藏而错误仍在屏上"的误导态;不涉及请求路径,无可用性副作用 |
| T-260917-SC | Tampering | 依赖安装(npm/pip/cargo) | high | mitigate | 本计划零新增依赖、零安装步骤、零包管理器调用;`requirements.txt` / `package.json` 不触碰。若执行期出现任何安装需求,即为偏离计划,须停下 |
</threat_model>

<verification>
**改动前基线(已实测,执行期先复跑确认再动手):**
```bash
node --check frontend/app.js                                  # pass
.venv/bin/python -m pytest -q -m "not slow"                   # 219 passed, 6 deselected
grep -c '!important'      frontend/style.css                  # 3  ← 其中 2 行是注释散文,不是门
grep -c '!important;'     frontend/style.css                  # 1  ← 这才是声明门
grep -c '^\.hidden {'     frontend/style.css                  # 1
grep -c 'doc-subview'     frontend/style.css                  # 1
grep -c '1-0-0'           frontend/style.css                  # 0
grep -c 'showInlineError(' frontend/app.js                    # 9  (1 定义 + 8 调用)
grep -c 'showInlineError(processRoundBtn' frontend/app.js     # 2
grep -c 'probeControls'   frontend/app.js                     # 0
grep -c 'clearInlineError();' frontend/app.js                 # 6
grep -c 'flex-wrap'       frontend/style.css                  # 0
```

**改动后(三任务整体收口):**
```bash
node --check frontend/app.js                                  # pass
grep -c '!important;'     frontend/style.css                  # 1  (未变)
grep -c '^\.hidden {'     frontend/style.css                  # 1  (未变)
grep -c '1-0-0'           frontend/style.css                  # 1  (0→1,新理由落文)
grep -c 'doc-subview'     frontend/style.css                  # 0  (1→0,幻影类名移除)
grep -c 'showInlineError(' frontend/app.js                    # 9  (未变,只换锚点)
grep -c 'showInlineError(probeControls' frontend/app.js       # 2  (0→2)
grep -c 'showInlineError(processRoundBtn' frontend/app.js     # 0  (2→0)
grep -c 'probeControls'   frontend/app.js                     # 3  (1 句柄 + 2 调用)
grep -c 'clearInlineError();' frontend/app.js                 # 9  (6→9)
grep -c 'flex-wrap'       frontend/style.css                  # 0  (未变,未打 CSS 补丁)
.venv/bin/python -m pytest -q -m "not slow"                   # 219 passed, 6 deselected
git diff --stat                                               # 只应有 frontend/style.css 与 frontend/app.js
```

**门算术陷阱(必须遵守):** `grep -c '!important' frontend/style.css` 返回 **3**——其中 2 行命中是 style.css:13-14 的**注释散文**,而 `!important` 的**声明**数必须恒为 1。任何以裸 `grep -c '!important'` 作门的断言都是错的。本计划一律用 `grep -c '!important;'`(带分号,只命中声明行,基线 1)。因此新注释散文中**不得出现带分号的 `!important;` 字面量**。

**区域门写法说明(执行期不要"简化"):** Task 3 的区域计数门用 `awk '/^(async )?function <name>/,/^}/'`。`(async )?` 前缀是必需的——`loadChecksView` 声明为 `async function`(app.js:591),漏掉前缀会让该区域匹配为空、`grep -c` 恒返回 0,门就永远"通过"了(这正是本计划在定稿前实测抓到的一个假门)。四个区域门在改动前的实测值:`roundSwitcher` 0、`applyArchiveView` 0、`applyWritingView` 0、`loadChecksView` 1、`hidePhase3Extras` 0。

**人工验收(前端无 pytest 覆盖,以下为 Nyquist 缺口的显式补偿;需本地服务运行):**
1. **缺陷 2 回归(锚点修复)**:进入一个阶段 3 项目 → 让「处理本轮批注」失败(例如先中止后端 AI 调用,或在 `#probe-controls` 里把 `#ai-route-select` 切到不可用的路线)→ 错误文案出现在**整条探针行下方、占满宽度**,而不是被挤在「处理本轮批注」与「中止」之间成为窄列。同时确认探针行内 5 个控件的排布与改动前完全一致。
2. **缺陷 3 回归(陈旧错误清除)**:上一步的错误留在屏上后——
   (a) 用 `#round-switcher` 切到另一轮 → 错误消失;
   (b) 进入归档态(或归档态下切轮)→ 错误消失;
   (c) 走到撰写视图(阶段 4)→ 错误消失;
   (d) 走到自检视图(阶段 5)→ 错误消失(此路径改动前已覆盖,复验不回归)。
3. **缺陷 1 回归(注释理由)**:阅读 style.css:13-15——注释点名的三个竞争者是 `#selection-menu` / `#annotations-panel` / `#checks-panel`(ID 特异性 1-0-0),`.overlay` 被表述为 0-1-0 的弱竞争者,且不再出现任何在 style.css 中无规则的类名;声明行逐字未变。
4. **不回归**:点「进入」用不存在的路径 → 错误仍全宽出现在输入区下方(锚点未动);发散 / 定稿失败的内联提示行为不变。
</verification>

<success_criteria>
- REG-01 闭合:`.hidden` 注释的理由与实际竞争关系一致(三个 1-0-0 竞争者被点名、`.overlay` 正确降级、幻影类名移除);`!important` 声明与 `.hidden` 规则本身零改动。
- REG-02 闭合(本 quick 的两条实质项):`#probe-controls` 作锚点使错误 `<p>` 落在整条探针行下方全宽;三条视图切换路径各清除一次内联错误。REG-02 中"`inlineErrorEl` 单例丢弃并发错误"一项**按编排器裁定不在本计划范围**(单错误显示是既定设计,非缺陷),留待 P8 复核时按同样裁定处理。
- 改动严格限于 `frontend/style.css` 与 `frontend/app.js`;`git diff --stat` 无第三个文件。
- `.venv/bin/python -m pytest -q -m "not slow"` 与改动前基线逐项一致(**219 passed, 6 deselected**)。
- 无新增依赖、无设计令牌层、无换肤/间距/字号改动、无 aria/role 改动、未给 `#probe-controls` 打 CSS 补丁、未改动其余四个 `showInlineError` 调用点。
- 每一行 diff 都能追溯到上述三条缺陷之一(CLAUDE.md §3);总 diff 远小于 30 行。
</success_criteria>

<output>
Create `.planning/quick/260917-fqh-b9664e0-hidden-flex/260917-fqh-SUMMARY.md` when done
</output>
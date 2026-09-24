---
phase: idi-08-accessibility-semantics-and-keyboard
plan: 03
type: execute
wave: 3
depends_on: [idi-08-01, idi-08-02]
files_modified:
  - frontend/app.js
autonomous: true
requirements: [A11Y-08, REG-03]
estimate:
  tokens: 56000
  raw_tokens: 56000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # —— 用户视角的可观察行为 ——
    - "S8-1:app.js:1121 的空态文案逐字为「本轮暂无批注——在右侧文档划词即可批注。」(改后与 DESIGN.md §4.1 的 v1.14 信息架构一致:文档面板在右)"
    - "REG-02 门①:`grep -c 'inline-error' frontend/style.css` 仍为 1"
    - "REG-02 门②:`grep -c 'clearInlineError();' frontend/app.js` >= 9(基线实测 9,只增不减)"
    - "pytest 基线:219 passed + 6 skipped / 225 collected —— 219 是**通过数**、225 是**收集数**,两者不是一回事;必须用项目 venv(.venv/bin/python)"
    - "REG-03 的六条人工验收项全部**重跑**并逐项记录观察结果;第 4 条已按 D-05 的新手势重写(含「松开 Shift」这一步)"
    - "A11Y-08:Tab 序到达每一个交互控件;新增的 #round-doc 停靠点在 Tab 序里的位置被逐项记录 —— 位置是 #round-switcher 之后、#authorize-row 的按钮(可见时)之前;不得只记「Tab 能到」"
    - "归档路径专项:切轮之后「处理本轮批注」不可点(走 updateFrozenPresentation 的复位路径,app.js:1166)"
    - "四条不变量守卫(check-01…04)在收口树上仍全部 PASS;frontend/style.css 在 D-01 路径下逐字节未改;frontend/vendor/ 仍恰好一个文件(marked.min.js)"
    - "本阶段的指纹义务被显式登记:D-01 路径下零债务(frontend/app.js 与 frontend/index.html 不在任何 live 报告的 covered_files 里);只有 D-02 被实测触发才作废 5 份,且重算以 HEAD 内容为准而非 mtime"
  artifacts:
    - path: "frontend/app.js"
      provides: "app.js:1121 的一处用户可见字符串:在左侧文档 → 在右侧文档(本阶段唯一一处文案改动,仅一个词)"
      contains: "在右侧文档划词即可批注"
  key_links:
    - from: "frontend/app.js:1121 (renderAnnotations 的空态分支)"
      to: "DESIGN.md §4.1"
      via: "v1.14 信息架构改版把文档面板移到了右侧;该串是唯一权威设计文档与实现矛盾的最后一处"
      pattern: "在右侧文档划词即可批注"
    - from: "REG-02 的两条门"
      to: ".planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-UI-SPEC.md §契约校验命令"
      via: "两条门落为计划级 grep + 人工 UAT 条目,**不写进** scripts/check-05-ui-uat.py(该文件在 5 份 live 报告的 covered_files 里,写进去会让零指纹债务当场消失)"
      pattern: "clearInlineError\\(\\);"
    - from: "A11Y-08 的 tab 序普查"
      to: "frontend/index.html 的全部交互控件"
      via: "具名人工步骤逐控件走一遍 Tab 序并记录位置 —— 本环境无法自动化键盘文本选区,故不得以自动测试结果替代"
      pattern: "n/a"
  prohibitions:
    - statement: "不得把自动化测试的结果当作键盘可达性的证据 —— 本环境无法自动化键盘文本选区(连 contenteditable 都选不中),A11Y-08 / A11Y-03 键盘半场 / REG-03 第 4 条必须是具名人工验收;**不得因自动测试 FAIL 判定功能缺陷**,也不得因自动测试 PASS 声称已覆盖键盘可达性"
      status: unresolved
    - statement: "不得继承前一次的人工检查结论而不重跑 —— REG-03 第 4 条的原文预期是「菜单出现」,而 D-05 之后键盘路径多了一个「松开 Shift」的动作,原先通过的检查现在测的是另一件事(与 Pitfall 3 / Pitfall 6 的「人工检查被继承而非重跑」同类失效)"
      status: unresolved
    - statement: "不得写出永不失败的假门 —— REG-02 门②的基线是实测 9(不是 08-CONTEXT.md D-21 里那个来自 b9664e0 时代旧 gate 的「6」,照抄 6 会造出一条永远不会失败的假门);pytest 的判据是「219 passed + 6 skipped / 225 collected」,照抄「225」当通过数会造出必然失败或必然通过的假门"
      status: unresolved
    - statement: "不得为了让门变绿而修改 scripts/check-05-ui-uat.py 的断言或常量 —— 该文件在 5 份 live 报告(idi-04 / idi-04.1-radix / idi-05 / idi-06 / idi-07)的 covered_files 里,改它会作废 5 份指纹;且若 item 10 在某个样本变红,必须先判「真缺陷 vs 普查集变化」,不得直接改门"
      status: unresolved
    - statement: "不得声称键盘划词的可发现性缺口已被覆盖 —— 新键盘路径全流程唯一的视觉信号就是焦点环,没有任何东西告诉键盘用户 Shift+方向键能划词;这是一个已登记的已知局限,必须显式登记而不是假装被覆盖(它不会让任何门变红,因为人工验收由知道步骤的用户执行)"
      status: unresolved
  assumptions:
    - statement: "edge-probe 对 A11Y-08 返回 unclassified ⇒ 按具名假设登记,不静默丢弃。实际边界条件已由 REQUIREMENTS.md 文末「人工验收项」的 A11Y-08 条、ROADMAP Phase 8 §Manual checks 与 idi-08-UI-SPEC.md §K-1.7 穷举(逐控件 Tab 序;新增停靠点的位置记录;本环境无法自动化键盘选区故不得以自动结果替代),规划期不另造判据"
      status: flagged
    - statement: "edge-probe 对 REG-03 返回 unclassified ⇒ 按具名假设登记,不静默丢弃。实际边界条件已由 08-CONTEXT.md 的 D-21 / D-22 / D-23 / D-24 / D-25 / D-26 与 260916-t8g-PLAN.md §<verification> 的六条原文穷举(两条 REG-02 门的落点与基线、六条人工项重跑与第 4 条重写、归档切轮专项、pytest 口径、指纹义务、04.1 的既有待办),规划期不另造判据"
      status: flagged
---

<objective>
把本阶段的验收与回归收口成可复跑的证据(A11Y-08 + REG-03),并修正一处与唯一权威设计文档矛盾的文案(S8-1)。

本计划交付三件事:①`frontend/app.js:1121` 的空态文案改一个词(`在左侧文档` → `在右侧文档`),并守住 REG-02 的两条回归门与 pytest 基线;②REG-03 —— `b9664e0` 五条修复的**全部人工验收项重跑**(第 4 条按 D-05 的新手势**重写**),含归档路径在**切轮之后**的专项复验;③A11Y-08 —— Tab 序到达每一个交互控件,且新增的 `#round-doc` 停靠点在 Tab 序里的**位置**被逐项记录,并把本阶段的指纹义务与既有待办登记清楚。

Purpose: 这五条修复**无任何自动化覆盖**(STATE.md 的 `[v1.14 P8]` Deferred Item 逐字登记),而本里程碑重写了它们依赖的 CSS ⇒ **若不重跑,就没有「未破坏它们」的证据**。另一条同样重要的判据是 **Pitfall 3 / Pitfall 6 的「人工检查被继承而非重跑」**:REG-03 第 4 条的原文预期是「菜单出现」,而 D-05 之后键盘路径多了一个「松开 Shift」的动作 ⇒ **原先通过的检查现在测的是另一件事**。
Output: `frontend/app.js` 的一处文案修正;两份人工验收记录(REG-03 六条 + A11Y-08 的 tab 序普查);以及收口登记(指纹义务、既有待办、已知缺口)。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/REQUIREMENTS.md
@.planning/DESIGN.md
@.planning/phases/idi-08-accessibility-semantics-and-keyboard/08-CONTEXT.md
@.planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-UI-SPEC.md
@.planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-PATTERNS.md
@.planning/quick/260916-t8g-ui-5-blocker-hidden-sse-onerror/260916-t8g-PLAN.md
@.planning/quick/260917-fqh-b9664e0-hidden-flex/
</context>

<decision_register>
**S8-1 文案修正(用户 2026-09-23 裁定「改」)。** `frontend/app.js:1121` 的空态文案 `本轮暂无批注——在左侧文档划词即可批注。` 改为 `本轮暂无批注——在右侧文档划词即可批注。`(**仅此一个词**)。理由:①它与**唯一权威设计文档** `DESIGN.md` §4.1 矛盾(v1.14 明写「主区(左)… 文档面板(右)」),而本项目对面向用户的输出立有「名必须说实话」与 §3.8 语言红线;②`06-UI-SPEC.md` 的 checker 已把该串登记为**已知过期串并明确指派给「拥有 `app.js` 的阶段(Phase 8)」**;③它是**一个词**,在**本阶段已经在改的文件**里,零新字符串、零新元素、零新依赖;④不修则它在**本阶段正要打通的那条键盘路径上误导用户**。**这是本阶段唯一一处用户可见文案变更**(Delta Ledger D8-11),**不是新增文案**。

**D-21 两条 REG-02 门落为计划级 grep + 人工 UAT 条目,不写进 `scripts/check-05-ui-uat.py`。** 两条门是:`grep -c 'inline-error' frontend/style.css` 仍为 **1**;`clearInlineError` 调用点计数**只增不减**(基线实测 **9** 个 `clearInlineError();` 调用 + 1 定义)。理由:`scripts/check-05-ui-uat.py` **在 5 份 live 报告的 `covered_files` 里**,把断言写进去会让 D-01 的「零指纹债务」当场消失。**已登记的代价:这两条不是常驻守卫,下次改 `frontend/style.css` 的人不会自动被拦。**

**A-5 REG-02 门②的基线由「6」更正为实测 9。** `08-CONTEXT.md` D-21 的「6」来自 `b9664e0` 时代的旧 gate;**实测 9**(L311 / L320 / L461 / L603 / L822 / L1252 / L1461 / L1511 / L1535)。**照抄 6 会造出一条永远不会失败的假门** —— 与本项目反复警告的 gate 算术错误同型。

**D-24 pytest 的算术口径:判据是「219 passed + 6 skipped / 225 collected」。** ROADMAP Phase 8 的 Gates 写「pytest 219 基线不变」(正确);**Phase 4 段里的「225」是 `--collect-only` 的数**。**219 是*通过*数、225 是*收集*数,两者不是一回事。** 本阶段后端零改动,该门只是回归证明。**必须用项目 venv**(`.venv/bin/python -m pytest`):环境 `python3` 是 miniconda,会让 4 个 `ai_caller` 测试**假失败**(本项目已记录:正确基线 219 passed / 6 skipped)。

**D-22 REG-03 = `b9664e0` 五条修复的全部人工验收项重跑,这是收口 gate,不是事后补记。** 原文六条(逐字取自 `260916-t8g-PLAN.md` 的 `<verification>` 节)见 Task 2。**第 4 条必须重写**:它的原文预期是「菜单出现」,而 D-05 之后键盘路径多了一个「松开 Shift」的动作,**原先通过的检查现在测的是另一件事**。

**D-23 归档路径的专项复验:切轮之后确认「处理本轮批注」不可点。** 走 `updateFrozenPresentation` 的复位路径(`app.js:1166` 会把 `applyArchiveView` 设的 `disabled = true` 复位 —— Pitfall 3 UI-6.3 的现场)。ROADMAP Phase 8 的 Gates 明列此条。

**D-25 指纹义务登记:本阶段在 D-01 路径下零债务;升级到 D-02 则作废 5 份。** 逐份核实:`idi-04` / `idi-04.1-radix` / `idi-05` / `idi-06` / `idi-07` 的 `covered_files` 均含 `frontend/style.css`(其中 04.1 / 05 / 06 / 07 还含 `scripts/check-05-ui-uat.py`)。**`frontend/app.js` 与 `frontend/index.html` 不在任何一份里。** 收口时若真的改了 CSS,须**以 HEAD 内容重算指纹**、**不要看 mtime**(本项目已记录:stale 有两种成因 ——「内容真变」走重新验证,「记账性编辑」走重算 + 披露,补救方向相反)。⚠ **`gsd-tools query verification status <phase>` 对这些报告一律返回 `missing`**(相位目录命名与工具的相位令牌解析不匹配),**不得用该命令判定 stale**。

**D-26 `idi-04.1-radix` 的复验义务本阶段开始前仍未收口**(STATE.md Operator Next Steps 第 2 条:`/gsd-verify-work idi-04.1-radix`,其 `covered_digest` 因 Phase 5 改写 `frontend/style.css` 与 `scripts/check-05-ui-uat.py` 而 stale,成因是**内容真变**)。**本阶段在 D-01 路径下不新增这一层**;若走 D-02,则它叠加一层。**规划期须在计划里显式登记这条既有待办,不要把它当成 Phase 8 引入的。**

**D-17 `#permission-modal` 的「弹了键盘用户不知道」登记为已知缺口,归 v2 `A11Y-V2-02`,本阶段不修。** 登记位置:`08-UAT.md` 或 VERIFICATION 的 manual/advisory 节。

**D-19 键盘划词的可发现性缺口登记为已知局限,不加任何提示。** 新路径全流程唯一的视觉信号就是焦点环。**已登记的后果:这个缺口不会让任何门变红**(A11Y-08 的人工验收由知道步骤的用户执行),所以要**显式登记**而不是假装被覆盖。

**STATE.md `[v1.14 P8]` Deferred Item:** 五条 `b9664e0` 修复**无自动化覆盖**,而本里程碑重写其依赖的 CSS;`.hidden { display: none !important }` 是**5 路单点故障**。
</decision_register>

<flagged_assumptions>
边缘覆盖探针对 A11Y-08 与 REG-03 均返回 `unclassified`(探针的分类词表是**英文**的,读不了中文需求文本)。**不得把 `unclassified` 当作「无边缘情况」,也不得自动 resolve。** 本计划登记两条:

- **A11Y-08** — 假设:键盘可达性的边缘条件**已由上游文本穷举** —— 逐控件走一遍 Tab 序(每一个交互控件);新增的 `#round-doc` 停靠点在 Tab 序里的**位置**必须逐项记录(在 `#round-switcher` 之后、`#authorize-row` 的按钮可见时之前),**不得只记「Tab 能到」**;本环境**无法自动化键盘文本选区**(连 `contenteditable` 都选不中)⇒ 不得以自动测试结果替代人工验收。**不在范围内**:焦点陷阱、完整 ARIA / 屏幕阅读器合规、可发现性提示(D-19 登记为已知局限)。
- **REG-03** — 假设:回归面的边缘条件**已由上游文本穷举** —— 六条人工项逐条重跑(第 4 条按 D-05 重写);归档路径**在切轮之后**确认「处理本轮批注」不可点(走 `updateFrozenPresentation` 的复位路径);pytest 的口径是「219 passed + 6 skipped / 225 collected」且必须用项目 venv;两条 REG-02 门的基线是 1 与 9。**不在范围内**:把两条 REG-02 门写进 harness(D-21 已裁定不写)、backlog `999.1` / `999.2`(各自会作废 `idi-04.1-radix` / `idi-07` 的指纹,与本阶段合并会搅浑两批复验)。
</flagged_assumptions>

<artifacts_this_phase_produces>
本阶段(三个计划合计)新建的符号与路径 —— 每个计划重复列出同一份清单,便于逐计划对照:

**新的 DOM id(2 个,全部在 `frontend/index.html`;硬规则 5 禁的是改名与删除,新增是安全的):**
- `confirmation-modal-title`(计划 02;`#confirmation-modal` 的 `<h3>`)
- `tier-modal-title`(计划 02;`#tier-modal` 的 `<h3>`)

**新的 HTML 属性:**
- `#round-doc` 的 `tabindex="0"`(计划 01,`frontend/index.html:139`)
- `#confirmation-modal` / `#tier-modal` 的 `role="dialog"` + `aria-modal="true"` + `aria-labelledby`(计划 02)

**新的 JS 顶层句柄(1 个,`frontend/app.js`):**
- `appEl`(`document.getElementById('app')`,加在 `app.js:83` 之后;计划 02)

**新的 JS 函数(1 个):**
- `syncBackgroundInert()`(计划 02;从两个弹窗的 `.hidden` 现状**派生**,不成对记账)

**新的 JS 事件监听器(2 个,均为匿名箭头函数,不引入具名 handler):**
- Shift 提交监听器(计划 01;`document` 上的 `keyup`,写在 `initSelectionMenu()` 内 ⇒ 继承该函数的一次性绑定守卫)
- Escape 单点分派监听器(计划 02;顶层 `document` 上的 `keydown`,一次性绑定)

**新的 JS 代码(无新符号):**
- `hideSelectionMenu()` 体内的 F1-a/b/c 焦点交还(计划 01)
- `#tier-modal` 打开分支的移焦 + `tierModalShown` 复位(计划 02)
- `syncBackgroundInert()` 的 5 个调用点(计划 02;全部在既有函数体内)
- `app.js:1121` 空态文案的一个词(本计划)

**新的 CSS:零。** 焦点环由 Phase 7 的 `[tabindex]:focus-visible` 枚举自动命中,本阶段 `frontend/style.css` **逐字节不变**(D-01)。

**新的脚本 / 新文件 / 新依赖:零。** `scripts/check-05-ui-uat.py` 与 `scripts/check-01…04` 零改动(D-21 / A-4);`frontend/vendor/` 仍恰好一个文件(`marked.min.js`);无构建步骤(硬规则 6)。
</artifacts_this_phase_produces>

<tasks>

<task type="auto">
  <name>Task 1:S8-1 文案修正 + 两条 REG-02 门 + pytest 基线 + 四条守卫复跑</name>
  <files>frontend/app.js</files>
  <read_first>
    - frontend/app.js(L1115-1126:`renderAnnotations` 的空态分支 —— 目标串在 L1121,且 L1123 的「该轮暂无批注。」是历史轮的另一处,不改;L301-315:`showInlineError` / `clearInlineError` 的定义与 `textContent`-only 规则)
    - frontend/style.css(L570-575 附近的 `.inline-error` 规则 —— REG-02 门①的对象)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-UI-SPEC.md(§Copywriting Contract 的空态两行;§Sign-Off Items S8-1;§Deliberate Delta Ledger D8-11;§契约校验命令的两条 REG-02 门)
    - .planning/DESIGN.md(§4.1 两栏契约 —— 「主区(左)… 文档面板(右)」是该串被改的判据来源;§3.8 语言红线)
    - .planning/REQUIREMENTS.md(§REG-02 条与文末「人工验收项」节)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/08-CONTEXT.md(D-21 / D-24 / A-5 / A-6)
  </read_first>
  <action>
    **第一处:S8-1 文案修正(一个词)。** `frontend/app.js:1121` 的空态赋值串 `本轮暂无批注——在左侧文档划词即可批注。` 改为 `本轮暂无批注——在右侧文档划词即可批注。` —— **只把「左」改成「右」**,标点、破折号、其余字词逐字不动。**这是本阶段唯一一处用户可见文案变更**(Delta Ledger D8-11),**不是新增字符串**。判据:改后与 `DESIGN.md` §4.1 的 v1.14 信息架构一致(文档面板在右)。

    **⚠ 这处编辑落在硬规则 5 的「不得触碰」符号内部 —— 授权来源必须登记。** `frontend/app.js:1121` 位于 `renderAnnotations`(`app.js:1115-1172`)的函数体内,而 `renderAnnotations` 被 **ROADMAP §全局硬规则 5**、**`idi-08-UI-SPEC.md` §Do-Not-Touch List(继承段)** 与 **`08-CONTEXT.md` §明确不含** 三处同时列为**不得触碰**(理由:已验收路径)。**本次编辑是用户裁定的授权例外,不是违反硬规则 5**,两条授权来源都必须在 SUMMARY 里逐字登记:①用户 **2026-09-23 裁定「改」** —— 原文见 `idi-08-UI-SPEC.md` §Sign-Off Items 的 **S8-1** 行「用户裁定(2026-09-23)」列(「`本轮暂无批注——在左侧文档划词即可批注。` → `本轮暂无批注——在右侧文档划词即可批注。`(`app.js:1121`,仅此一个词)」);②`idi-08-UI-SPEC.md` §本阶段的改动面(唯一事实)有一行逐字授权该处(`frontend/app.js` | `app.js:1121` 的一处用户可见字符串:`在左侧文档` → `在右侧文档` | **S8-1(用户 2026-09-23 裁定)**)。**授权面只覆盖 L1121 这一个词**:不得触碰同一函数内任何其他行,也不得把这条例外扩大成「`renderAnnotations` 可改」—— 硬规则 5 的不得触碰清单**未被推翻**,例外仅限这一词。

    **SUMMARY 的登记要求(否则读者按硬规则 5 逐字核 diff 时会把这一行读成违例):** 在记录 S8-1 的同时写明「本次编辑在 `renderAnnotations`(`app.js:1115-1172`)内部,由用户 2026-09-23 的 S8-1 裁定(`idi-08-UI-SPEC.md` §Sign-Off Items)与 §改动面 授权;例外仅限 `app.js:1121` 的一个词,硬规则 5 的不得触碰清单未被推翻、也未扩大」。

    **不得顺手改的相邻串:** `frontend/app.js:1123` 的 `该轮暂无批注。`(历史轮的另一处空态,与左右无关)**一字不动**;该函数里的 `document.createElement` / `className` / `textContent` 三行**一字不动** —— 尤其 `textContent`:**该函数所在路径的 `textContent`-only 规则是 XSS 缓解(T-260916-01),不是风格选择**(硬规则 5),**不得引入任何 HTML 解析式的写入**。

    **第二处:跑两条 REG-02 门并把基线写进 SUMMARY。**
    - 门①:`grep -c 'inline-error' frontend/style.css` —— 期望 **1**(基线实测 1)。
    - 门②:`grep -c 'clearInlineError();' frontend/app.js` —— 期望 **>= 9**(基线实测 **9**;`grep -c 'clearInlineError'` 会返回 10 = 9 调用 + L303 的定义行)。**这个「9」是本计划最容易被写错的一处**:`08-CONTEXT.md` D-21 写的是「6」,那是 `b9664e0` 时代旧 gate 的数字;**照抄 6 会造出一条永远不会失败的假门**。本任务**只增加**调用点(若有),**绝不减少**;若因本阶段改动导致该计数变化,必须逐条登记是哪个文件/哪个函数引入的。
    - **这两条门不写进 `scripts/check-05-ui-uat.py`**(D-21 / A-4):该文件在 5 份 live 报告的 `covered_files` 里,把断言写进去会让本阶段的「零指纹债务」当场消失。**已登记的代价**:这两条不是常驻守卫,下次改 `frontend/style.css` 的人不会自动被拦。

    **第三处:跑 pytest 基线并逐字记录四个数字。** 用 `.venv/bin/python -m pytest -q -m "not slow"`。判据是 **`219 passed` + `6 skipped` / `225 collected`** —— **219 是通过数、225 是收集数,两者不是一回事**。**必须用项目 venv**:环境 `python3` 是 miniconda,会让 4 个 `ai_caller` 测试**假失败**(本项目已记录:正确基线 219 passed / 6 skipped)。**本阶段后端零改动,该门只是回归证明**;若数字与基线不同,先判「是本阶段引入的,还是环境/依赖漂移」,并把实测四个数字逐字写进 SUMMARY。

    **第四处:复跑四条不变量守卫并登记。** `bash scripts/check-01-token-conformance.sh`、`.venv/bin/python scripts/check-02-contrast.py`(判据 `PASS: 0 failures`,47 对 + ORDER 0.363)、`bash scripts/check-03-hidden-uniqueness.sh`(`^\.hidden {` 计数 == 1)、`bash scripts/check-04-important-count.sh`(`!important` **声明**数 == 1)。**注意硬规则 2 的算术陷阱**:`grep -c '!important' frontend/style.css` 会返回 **5**(4 行注释散文 + 1 条声明),**门必须按「声明」计数**(由 `check-04` 判定),**不得直接数命中行**。同时登记 `grep -c '^\.hidden {' frontend/style.css` == 1(硬规则 1)。

    **第五处:登记本阶段会打破/触及的既有断言。** 在 SUMMARY 里逐条写明:①`check-05 --item 10` 的判定集在 p3 / checking / archive 三个样本里 +1(`#round-doc` 入册,计划 01 引入)且 p1 / p12 里被 `visible` 过滤排除;②`_idi07_tab_drive` 的上限是数据驱动的(判定集 +1 ⇒ 上限 +1,与 Tab 序 +1 相抵,**无需改门**);③`scripts/probe-07-focus-composite.py` 的复跑义务已由计划 01 履行(D-04);④其余四条守卫(check-01…04)在 D-01 路径下不受影响。
  </action>
  <verify>
    <automated>grep -c '在右侧文档划词即可批注' frontend/app.js</automated>
    <fails_when>输出不是恰好 `1`(S8-1 的改法;出现 0 说明没改,出现 2 说明顺手动到了 L1123 那一处)</fails_when>
    <automated>grep -c 'inline-error' frontend/style.css</automated>
    <fails_when>输出不是恰好 `1`(REG-02 门①的基线;`frontend/style.css` 本阶段逐字节未改,该值必须逐字不变)</fails_when>
    <automated>grep -c 'clearInlineError();' frontend/app.js</automated>
    <fails_when>输出小于 `9`(REG-02 门②的基线是实测 9、只增不减;小于 9 说明误删了调用点)</fails_when>
    <automated>.venv/bin/python -m pytest -q -m "not slow"</automated>
    <fails_when>摘要行不是 `219 passed, 6 skipped`(或出现任何 `failed` / `error`);收集数不是 225 时须逐字记录实测四个数字并说明差异来源</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>任一条不是恰好一行 `PASS`(check-01 报围栏外裸 hex 或 tier-1 引用;check-03 报 `.hidden` 计数不是 1;check-04 报 `!important;` 声明数不是 1)</fails_when>
    <automated>.venv/bin/python scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>末行不是 `PASS: 0 failures`(零颜色改动 ⇒ 47 对与 ORDER 0.363 必须逐字不变)</fails_when>
    <automated>git status --porcelain -- frontend/style.css scripts/check-05-ui-uat.py</automated>
    <fails_when>输出非空(D-01 / D-21:两个文件本阶段零改动)</fails_when>
    <human-check>
      <test>进入阶段 3、且当前轮尚无批注时,读主区批注流的空态那一行</test>
      <expected>逐字为「本轮暂无批注——在右侧文档划词即可批注。」;切到历史轮时为空态「该轮暂无批注。」(不受本次改动影响)</expected>
      <why_human>用户可见文案的最终确认;`grep` 能证明字符串改了,不能证明它出现在正确的状态与位置</why_human>
    </human-check>
  </verify>
  <acceptance_criteria>
    - `frontend/app.js:1121` 的空态串逐字为 `本轮暂无批注——在右侧文档划词即可批注。`;`frontend/app.js:1123` 的历史轮空态串一字未改。
    - SUMMARY 里登记了「`app.js:1121` 的编辑落在硬规则 5 的不得触碰符号 `renderAnnotations`(`app.js:1115-1172`)内部,由用户 2026-09-23 的 S8-1 裁定(`idi-08-UI-SPEC.md` §Sign-Off Items)与 §本阶段的改动面 授权;例外仅限该一个词,不得触碰清单未被推翻、也未扩大」。
    - 该函数的写入方式仍只经 `textContent`(零新增 HTML 解析式写入;`showInlineError` 的 `textContent`-only 规则未被触碰)。
    - `grep -c 'inline-error' frontend/style.css` == 1;`grep -c 'clearInlineError();' frontend/app.js` >= 9,且 SUMMARY 里写明该基线的实测值、并显式登记「不是 08-CONTEXT.md D-21 的 6」。
    - SUMMARY 里逐字记录了 pytest 的四个数字(219 passed / 6 skipped / 225 collected),并说明 219 与 225 的区别;命令是 `.venv/bin/python -m pytest -q -m "not slow"`。
    - 四条不变量守卫全绿,且 SUMMARY 里登记了硬规则 2 的算术陷阱(`!important` 命中行 5 vs 声明数 1,门按声明计数)。
    - `frontend/style.css` 与 `scripts/check-05-ui-uat.py` 的 `git status --porcelain` 均为空。
    - SUMMARY 里登记了本阶段触及的三条既有断言(D-03 的判定集变化、`_idi07_tab_drive` 的数据驱动上限、probe-07 的复跑已完成)。
  </acceptance_criteria>
  <reversibility rating="costly">把两条 REG-02 门写进 harness 就要连带复验五份 live 报告并重算 idi-07 的指纹;本计划按 D-21 的裁定保持「计划级 grep」,代价是它们不是常驻守卫。</reversibility>
  <done>S8-1 的一个词已改且与 `DESIGN.md` §4.1 一致;两条 REG-02 门的基线与 pytest 的四个数字被逐字记录(并登记了「9 不是 6」「219 不是 225」两处 gate 算术陷阱);四条不变量守卫全绿;`frontend/style.css` 与 `scripts/check-05-ui-uat.py` 零改动。</done>
</task>

<task type="auto">
  <name>Task 2:REG-03 —— b9664e0 五条修复的六条人工验收项全量重跑(第 4 条按 D-05 重写)+ 归档切轮的专项复验</name>
  <files>frontend/app.js(仅当复验发现回归时才改;无回归则零改动)</files>
  <precondition>应用可在本机启动并能在浏览器里打开;`scripts/ui-states/` 下的五个状态样本可用;后端可启停(第 5 条要停掉后端观察断流横幅)</precondition>
  <read_first>
    - .planning/quick/260916-t8g-ui-5-blocker-hidden-sse-onerror/260916-t8g-PLAN.md(§`<verification>` —— **六条人工检查的原文,逐字**)
    - .planning/quick/260916-t8g-ui-5-blocker-hidden-sse-onerror/260916-t8g-SUMMARY.md(coverage 表与 `human_judgment` 理由;尤其 D4 的「已知限制:`#round-doc` 是不可聚焦的普通 div,keyup 仅在焦点已落在容器内时生效」—— **本阶段正是要消掉这条限制**)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-UI-SPEC.md(§K-2.6 —— 第 4 条重写后的九步形态;§K-1.5 的鼠标路径行为变化)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/08-CONTEXT.md(D-09 / D-22 / D-23)
    - frontend/app.js(L1166 附近的 `updateFrozenPresentation` 与 L817-818 的 `applyArchiveView` 两行 —— **硬规则 5 不得触碰**;D-23 的复位路径现场)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-01-PLAN.md(Task 3 的九步人工脚本 —— 第 4 条与本项有重叠,按「本项测回归面、计划 01 测新能力」分工,不要重复执行同一段)
  </read_first>
  <action>
    逐条重跑 `b9664e0` 五条修复的**全部六条**人工验收项,**逐项记录步骤与观察结果**。原文六条如下(逐字取自 `260916-t8g-PLAN.md` 的 `<verification>` 节),**第 4 条必须按下面的重写版执行**:

    1. **阶段 1-2 项目只显示草稿正文、「尚无草稿」提示不可见。**
    2. **阶段 3 项目轮次文档上方无占位提示、撰写/自检视图中轮次切换器不可见。**
    3. **走完流程至 `mission_complete`** ⇒ 「处理本轮批注」不可见且 `disabled === true`、授权行不可见、轮次切换器**仍可见可切**。
    4. **~~用 Shift+方向键在轮次文档中划选 → 菜单出现~~(重写版,见下)。**
    5. **停掉后端** ⇒ 横幅出现「事件流已断开,正在自动重连……」;**恢复** ⇒ 自动消失;**致命断开** ⇒ 红色横幅。
    6. **不存在的路径点「进入」** ⇒ 错误出现在输入框正下方;**再次点击时旧错误先消失。**

    **第 4 条的重写版(必须按这个执行,不得照抄原文预期):** 原文预期是「菜单出现」,而 D-05 之后键盘路径多了一个「松开 Shift」的动作 ⇒ **原先通过的检查现在测的是另一件事**(与 Pitfall 3 / Pitfall 6 的「人工检查被继承而非重跑」同类失效)。重写后的步骤:①进入 phase3 项目;②按 Tab 到轮次文档区(焦点环画出);③**按住 Shift**,连按 → 数次扩选一段文字(观察:焦点环全程仍画在文档区、不跳走);④**松开 Shift** ⇒ 菜单出现且焦点落在 `#btn-annotate`;⑤按 Enter 激活 `#btn-annotate` ⇒ 原生 `window.prompt` 收 note ⇒ 输入 ⇒ 确定 ⇒ 批注条目出现在主区批注流、`#pending-count` 增加。**逐项记录每一步的焦点位置与观察结果。**
    **同时复跑 D-09 登记的鼠标路径行为变化**:鼠标 Shift+点击扩选后**松开 Shift 也会把焦点送进菜单** —— 判定为**可接受**(焦点去的正是用户接下来要点的地方),但必须记录实测结果(含鼠标点击**不**出环这一 SC2 语义仍成立)。

    **归档路径的专项复验(D-23,ROADMAP Phase 8 的 Gates 明列):** 走 `applyArchiveView`(`app.js:817-818` 附近)进入只读归档态 ⇒ 确认「处理本轮批注」不可点 ⇒ **切轮**(走 `updateFrozenPresentation`,`app.js:1166`)⇒ **切轮之后再次确认「处理本轮批注」仍不可点**。**这是 Pitfall 3 UI-6.3 的现场**:`updateFrozenPresentation` 的复位路径会把 `applyArchiveView` 设的 `disabled = true` 复位。**硬规则 5:`applyArchiveView` 的两行不得触碰** —— 本项只观测,不改。

    **无回归时本任务零改动。** 若某一条复验发现回归,先判「是本阶段引入的,还是本阶段之前就存在的」;若是本阶段引入的,按最小改动修并登记;若不是,登记为已知项而**不在本计划里修**(除非它由本阶段的改动直接引起)。

    **登记义务:** 在 SUMMARY 里逐条写明六条的**步骤与观察结果**(不是「通过」两个字),并显式登记:①第 4 条已按 D-05 重写,原文预期不再适用;②`260916-t8g-SUMMARY.md` 里 D4 的那条已知限制(「`#round-doc` 是不可聚焦的普通 div,keyup 仅在焦点已落在容器内时生效」)**已被本阶段消掉**,并说明消掉的方式(计划 01 的 `tabindex="0"` + Shift 提交监听器);③归档切轮专项的观测结果。
  </action>
  <verify>
    <automated>grep -c 'updateFrozenPresentation' frontend/app.js</automated>
    <fails_when>输出小于改动前的计数(D-23 的复位路径是**观测对象**,本任务不得改它;计数变小说明误删了调用点或函数)</fails_when>
    <automated>grep -c 'clearInlineError();' frontend/app.js</automated>
    <fails_when>输出小于 `9`(第 6 条涉及内联错误的清除路径;本任务不得减少任何调用点)</fails_when>
    <automated>git status --porcelain -- frontend/style.css frontend/index.html</automated>
    <fails_when>输出非空(第 1/2/3/6 条都涉及 `.hidden` 与内联错误的呈现;若为让某条复验通过而改了 CSS 或 HTML,即为范围越界 —— D-01 / 硬规则 5)</fails_when>
    <human-check>
      <test>逐条执行六条人工验收项(第 4 条用重写版:Tab 进文档区 → 按住 Shift 连按 → 扩选 → 松开 Shift → 菜单与焦点 → Enter 走完一次真实批注),外加鼠标路径的 Shift+点击复跑与归档切轮专项</test>
      <expected>第 1 条:只显示草稿正文、「尚无草稿」提示不可见;第 2 条:轮次文档上方无占位提示、撰写/自检视图下轮次切换器不可见;第 3 条:「处理本轮批注」不可见且 disabled === true、授权行不可见、轮次切换器仍可见可切;第 4 条(重写版):松开 Shift 后菜单出现且焦点在 #btn-annotate,Enter 后批注真的出现在批注流且 #pending-count 增加;第 5 条:断流横幅出现/消失/致命态红色三态可分;第 6 条:错误在输入框正下方,再次点击时旧错误先消失。归档切轮专项:切轮之后「处理本轮批注」仍不可点</expected>
      <why_human>这六条**无任何自动化覆盖**(STATE.md `[v1.14 P8]` Deferred Item 逐字登记),而本里程碑重写了它们依赖的 CSS ⇒ 若不重跑就没有「未破坏它们」的证据;第 4 条还依赖本环境**无法自动化**的键盘文本选区。**不得因自动测试 FAIL 判定功能缺陷**</why_human>
    </human-check>
  </verify>
  <acceptance_criteria>
    - 六条人工验收项**全部重跑**,SUMMARY 里逐条记录的是**步骤与观察结果**,不是「通过」二字。
    - 第 4 条按 D-05 的重写版执行(含「松开 Shift」这一步),且 SUMMARY 里显式登记「原文预期『菜单出现』不再适用」。
    - 鼠标路径的 Shift+点击复跑有实测记录,含「鼠标点击不出环 ⇒ SC2 语义仍成立」这一条。
    - 归档切轮专项有独立记录:进入只读归档态后「处理本轮批注」不可点,**切轮之后**仍不可点(走 `updateFrozenPresentation` 的复位路径)。
    - SUMMARY 里登记了 `260916-t8g-SUMMARY.md` 的 D4 已知限制(「`#round-doc` 是不可聚焦的普通 div」)已被本阶段消掉,并写明消掉的方式。
    - `frontend/style.css` 与 `frontend/index.html` 的 `git status --porcelain` 均为空;`updateFrozenPresentation` 与 `clearInlineError` 的计数未减少;`applyArchiveView` 的两行未被触碰。
  </acceptance_criteria>
  <done>六条人工验收项全部重跑且逐条记录了步骤与观察结果;第 4 条按新手势重写后真的走通一次键盘批注;归档切轮之后「处理本轮批注」仍不可点;鼠标路径的行为变化被实测记录;D4 的旧已知限制被显式登记为已消掉。</done>
</task>

<task type="auto">
  <name>Task 3:A11Y-08 的 Tab 序全量人工普查 + 收口登记(指纹义务 / 既有待办 / 已知缺口)</name>
  <files>无源代码改动(普查与登记任务;产物是 SUMMARY 里的三份登记)</files>
  <precondition>应用可在本机启动并能在浏览器里打开;能进入阶段 3(轮次视图)与阶段 5(撰写/自检视图)两个状态</precondition>
  <read_first>
    - .planning/REQUIREMENTS.md(文末「人工验收项」节的 A11Y-08 条原文:「tab 序到达每一个交互控件;键盘划词路径可用」)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-UI-SPEC.md(§K-1.7 的焦点序契约 —— 新增停靠点的位置判据;§K-1.4 的刻意不做四件事;§K-1.5;§M-2.4 的已知缺口)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/08-CONTEXT.md(D-17 / D-19 / D-25 / D-26)
    - .planning/STATE.md(§Operator Next Steps 第 2 条 —— D-26 的既有待办原文;§Deferred Items 的 `[v1.14 P8]` 条)
    - frontend/index.html(L10-155 的 `#app` 全量可聚焦元素;L139 的 `#round-doc`;L143 的 `#btn-authorize`;L136 的 `#round-switcher`;L207-211 的 `#selection-menu`)
    - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-01-PLAN.md / idi-08-02-PLAN.md(前两个计划已记录的人工项 —— 本任务只做**全量 Tab 序普查**与**收口登记**,不重复执行它们的脚本)
  </read_first>
  <action>
    **第一处:A11Y-08 的全量 Tab 序人工普查。** 在两个状态里各走一遍完整 Tab 序(阶段 3 轮次视图;阶段 5 撰写/自检视图),**逐控件记录**:
    - 每一个交互控件(按钮 / 输入框 / 下拉 / 链接 / `summary`)都能被 Tab 到达;
    - **`#round-doc` 在 Tab 序里的位置**必须逐项记录 —— 判据是 §K-1.7:**在 `#round-switcher`(`frontend/index.html:136`)之后、`#authorize-row` 的按钮(可见时,`frontend/index.html:143`)之前**。**不得只记「Tab 能到」**;
    - `#round-doc` 的环在 Tab 到达时画出(整盒环;**形态随文档长度与视口的关系而变** —— 短文档为完整矩形、长文档为「上边 + 左右两条贯穿全高的竖线」,两种都算通过。⚠ **原写「左右两条贯穿全高的竖线」是规划期的几何推断,已被执行期实测推翻**(见 UI-SPEC §契约修正登记 A-10),**不要拿它当判据**,否则会对一个正确的实现误判为失败);
    - 键盘划词路径可用(按住 Shift 扩选 → 松开 Shift → 菜单 + 焦点 → Escape 交还)。
    **本环境无法自动化键盘文本选区**(连 `contenteditable` 都选不中)⇒ 这一段**必须**是具名人工验收;**不得因自动测试 FAIL 判定功能缺陷**(ROADMAP Phase 8 §Manual checks 明文)。

    **第二处:收口登记(三份,全部写进 SUMMARY)。**
    **(a) 指纹义务(D-25)。** 逐份核实并登记:`idi-04` / `idi-04.1-radix` / `idi-05` / `idi-06` / `idi-07` 的 `covered_files` 均含 `frontend/style.css`(其中 04.1 / 05 / 06 / 07 还含 `scripts/check-05-ui-uat.py`);**`frontend/app.js` 与 `frontend/index.html` 不在任何一份里** ⇒ **本阶段在 D-01 路径下零债务**。若计划 01 的 Task 2 判定「不可辨」并触发了 D-02,则登记:5 份报告**以 HEAD 内容重算**(**不要看 mtime** —— stale 有两种成因:「内容真变」走重新验证,「记账性编辑」走重算 + 披露,补救方向相反),并连带复跑四条守卫。⚠ **不得用 `gsd-tools query verification status <phase>` 判定 stale** —— 本项目已记录:这些相位目录一律返回 `missing`(相位目录命名与工具的相位令牌解析不匹配)。
    **(b) 既有待办(D-26,显式登记为**既有**、非本阶段引入)。** `/gsd-verify-work idi-04.1-radix` 本阶段开始前**仍未收口**(STATE.md Operator Next Steps 第 2 条;其 `covered_digest` 因 Phase 5 改写 `frontend/style.css` 与 `scripts/check-05-ui-uat.py` 而 stale,成因是**内容真变**)。**本阶段在 D-01 路径下不新增这一层**;若走 D-02,则它叠加一层。**登记的目的是不让它被误当成 Phase 8 引入的。**
    **(c) 已知缺口与已知局限(两条,都不修)。** ①**D-17**:`#permission-modal` 打开时不移焦、无任何宣告 ⇒「弹了键盘用户不知道」,归 v2 `A11Y-V2-02`(理由:它可 Tab 出去、不构成卡死;用户已裁定对象集为 confirmation + tier);②**D-19**:键盘划词路径全流程唯一的视觉信号就是焦点环 —— **没有任何东西告诉键盘用户 Shift+方向键能划词**。**已登记的后果:这个缺口不会让任何门变红**(A11Y-08 的人工验收由知道步骤的用户执行),所以要**显式登记**而不是假装被覆盖。两条都写明「本阶段不修」及归属。

    **第三处:把 STATE.md 的 `[v1.14 P8]` Deferred Item 与本阶段的对应关系登记清楚。** 该条原文:「五条 `b9664e0` 修复无自动化覆盖,而本里程碑重写其依赖的 CSS;`.hidden { display: none !important }` 是 5 路单点故障」。登记:本阶段通过 Task 2 的六条人工重跑 + Task 1 的 `check-03`(`.hidden` 唯一性)承担该条的两半;**这两条都不是常驻守卫**(人工项与计划级 grep),所以该 Deferred Item **不因本阶段而关闭**,只是被本阶段履行了一次。

    **第四处:登记本阶段的三条已签核偏离在验收记录里的位置**(供 VERIFICATION / UAT 消费):A-1(对象集按实测重排为 confirmation + tier)、A-2(键盘提交手势 = 抬起 Shift)、A-3(PITFALLS 5 失效模式 4 被几何推翻 ⇒ 整盒环 + `style.css` 零改动)。**这三条已在 UI-SPEC §契约修正登记 与 08-CONTEXT 里,本任务只做指针式登记,不复制正文。**
  </action>
  <verify>
    <automated>git status --porcelain -- frontend/ scripts/</automated>
    <fails_when>输出非空(本任务**零源代码改动** —— 它是普查与登记任务;出现任何 diff 说明越界)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>任一条不是恰好一行 `PASS`(收口树上的最终守卫复跑)</fails_when>
    <automated>grep -c 'tabindex' frontend/index.html; grep -v '^#' frontend/style.css | grep -c ':focus-visible'</automated>
    <fails_when>第一条输出不是恰好 `1`,或第二条输出不是恰好 `9`(本阶段的 D-01 路径签名:属性 +1、CSS 规则计数不变)</fails_when>
    <automated>ls -1 frontend/vendor/ | wc -l</automated>
    <fails_when>输出不是恰好 `1`(硬规则 6:vendor 目录仍只有 marked.min.js;多于 1 说明引入了 vendored 依赖)</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 1; .venv/bin/python scripts/check-05-ui-uat.py --item 4</automated>
    <fails_when>任一条退出码非 0(0 = 全 PASS;1 = 有 FAIL;2 = 有 BLOCKED),或输出里出现任何 `FAIL` / `BLOCKED` 开头的行。这两条与上面的 `check-01/03/04` 同属 `idi-08-UI-SPEC.md` §契约校验命令 的「必须保留的既有门」清单(`--item 1` = 五态显隐的 `.hidden` 层叠证据;`--item 4` = SC5 令牌接线 + `#state-badge` z-index);它们是收口树上的最终复跑,**判红时先判「真缺陷 vs 普查集变化」,不得改门**(D-21)</fails_when>
    <human-check>
      <test>在阶段 3 与阶段 5 两个状态里各走一遍完整 Tab 序,逐控件记录;并专门记录 #round-doc 在 Tab 序里的位置(应在 #round-switcher 之后、#authorize-row 的按钮可见时之前)</test>
      <expected>每一个交互控件都可 Tab 到达;#round-doc 的停靠点位置与 §K-1.7 一致(逐项记录,不得只记「Tab 能到」);#round-doc 被 Tab 到达时整盒环画出;键盘划词路径可用</expected>
      <why_human>本环境**无法自动化键盘文本选区**,且「Tab 序到达每一个交互控件」的完整枚举需要人眼逐控件确认;不得因自动测试 FAIL 判定功能缺陷(ROADMAP Phase 8 §Manual checks)</why_human>
    </human-check>
  </verify>
  <acceptance_criteria>
    - SUMMARY 里有两个状态的完整 Tab 序记录,且 `#round-doc` 的位置被逐项写明(在 `#round-switcher` 之后、`#authorize-row` 的按钮可见时之前),不是「Tab 能到」四个字。
    - SUMMARY 里登记了指纹义务的实测结论:`frontend/app.js` 与 `frontend/index.html` 不在任何 live 报告的 `covered_files` 里 ⇒ D-01 路径下零债务;并写明「不得用 `gsd-tools query verification status <phase>` 判定 stale」。
    - SUMMARY 里登记了 D-26 的既有待办(`/gsd-verify-work idi-04.1-radix`)为**既有、非本阶段引入**,并写明它是否因 D-02 而叠加。
    - SUMMARY 里登记了两条已知缺口/局限(D-17 的 `#permission-modal`、D-19 的键盘划词可发现性),各自写明归属与本阶段不修的理由。
    - SUMMARY 里登记了 STATE.md `[v1.14 P8]` Deferred Item 与本阶段的对应关系,并明确它**不因本阶段而关闭**。
    - SUMMARY 里对 A-1 / A-2 / A-3 三条已签核偏离做了指针式登记(不复制正文)。
    - `git status --porcelain -- frontend/ scripts/` 为空(本任务零源代码改动);三条守卫与 `check-05 --item 1 / --item 4` 仍全绿;`tabindex` == 1 且 `:focus-visible` == 9;`frontend/vendor/` 恰好一个文件。
  </acceptance_criteria>
  <done>A11Y-08 的全量 Tab 序普查在两个状态里完成且 `#round-doc` 的位置被逐项记录;三份收口登记(指纹义务、既有待办、已知缺口/局限)全部落盘;`[v1.14 P8]` 的 Deferred Item 与本阶段的关系被写明(不因本阶段关闭);本任务零源代码改动,收口树上三条守卫与 `check-05 --item 1 / --item 4` 仍全绿、`tabindex` == 1、`:focus-visible` == 9、vendor 恰好一个文件。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 服务端错误消息 → 内联错误节点 | `showInlineError` 的 `textContent`-only 规则是 XSS 缓解(T-260916-01),**不是风格选择**;REG-02 的两条门守住它所在的路径 |
| 验证记录 → 门 | 门的**算术**决定了阶段能否在未验证的情况下宣告通过:基线取错(6 而非 9、225 而非 219)会造出永不失败或必然失败的假门 |
| 验证 harness → 5 份 live 报告 | `scripts/check-05-ui-uat.py` 在 5 份 live 报告的 `covered_files` 里;改它的断言会作废 5 份指纹 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi08-10 | Repudiation | REG-02 门②与 pytest 的基线算术 | **high** | mitigate | 门的基线一律取**实测值**:REG-02 门② 写作 `>= 9`(`08-CONTEXT.md` D-21 的「6」是 `b9664e0` 时代的旧 gate,照抄会造出**永远不会失败**的假门);pytest 判据写作「219 passed + 6 skipped / 225 collected」并显式区分通过数与收集数(照抄「225」当通过数会造出必然失败或必然通过的假门)。SUMMARY 里逐字记录实测数字 |
| T-idi08-11 | Tampering | `scripts/check-05-ui-uat.py` 的断言与常量 | medium | mitigate | 该文件本阶段**零改动**(`git status --porcelain` 为空即为证据)。它是 5 份 live 报告 `covered_files` 的成员 ⇒ 改它会作废 5 份指纹;且 item 10 若在某样本变红,**必须先判「真缺陷 vs 普查集变化」**(D-03),不得直接改门 |
| T-idi08-12 | Information Disclosure | `showInlineError` 的 `textContent`-only 规则 | medium | mitigate | 本计划零改动该函数(硬规则 5)。REG-02 门① 守住 `frontend/style.css` 里 `inline-error` 的唯一性,门② 守住 `clearInlineError` 调用点只增不减 —— 两条门共同证明错误呈现路径未被改写 |
| T-idi08-13 | Repudiation | 人工验收项的「继承而非重跑」 | medium | mitigate | REG-03 第 4 条**按 D-05 的新手势重写**(原文预期「菜单出现」不再适用),并逐条记录**步骤与观察结果**而非「通过」二字;`260916-t8g-SUMMARY.md` 的 D4 已知限制被显式登记为「已消掉」而不是继续沿用 |
| T-idi08-SC | Tampering | npm / pip / cargo 安装 | high | mitigate | **本阶段零新增运行时依赖、零构建步骤**(硬规则 6)。收口时 `frontend/vendor/` 必须仍**恰好一个文件**(`marked.min.js`);`check-01` / `check-02` 保持零依赖。任何需要安装的写法都是计划偏差与**停止条件** |
</threat_model>

<verification>
**本计划的整体验收:**

```bash
grep -c '在右侧文档划词即可批注' frontend/app.js        # == 1
grep -c 'inline-error' frontend/style.css               # == 1(REG-02 门①)
grep -c 'clearInlineError();' frontend/app.js           # >= 9(REG-02 门②,基线实测 9)
.venv/bin/python -m pytest -q -m "not slow"             # 219 passed, 6 skipped / 225 collected
bash scripts/check-01-token-conformance.sh              # PASS
.venv/bin/python scripts/check-02-contrast.py | tail -1  # PASS: 0 failures
bash scripts/check-03-hidden-uniqueness.sh              # PASS(^\.hidden { == 1)
bash scripts/check-04-important-count.sh                # PASS(!important 声明数 == 1)
.venv/bin/python scripts/check-05-ui-uat.py --item 1    # PASS(Task 3;契约点名的「必须保留的既有门」)
.venv/bin/python scripts/check-05-ui-uat.py --item 4    # PASS(Task 3;同上)
grep -c 'tabindex' frontend/index.html                  # == 1
grep -v '^#' frontend/style.css | grep -c ':focus-visible'  # == 9
git status --porcelain -- frontend/style.css scripts/check-05-ui-uat.py  # 空
ls -1 frontend/vendor/ | wc -l                          # == 1
```

**本计划只改一处文案。** 除 `frontend/app.js:1121` 的一个词之外,`frontend/` 与 `scripts/` 的其余部分逐字节不变。
</verification>

<success_criteria>
- REG-02 的两条门按**实测基线**(1 与 9)守住,pytest 基线为 219 passed + 6 skipped / 225 collected。
- REG-03 的六条人工验收项全部**重跑**(第 4 条按 D-05 的新手势重写),归档切轮之后「处理本轮批注」仍不可点。
- A11Y-08 的 Tab 序普查覆盖两个状态,`#round-doc` 的停靠点位置被逐项记录。
- 三份收口登记(指纹义务 / 既有待办 D-26 / 已知缺口 D-17 与 D-19)全部落盘,且 `[v1.14 P8]` 的 Deferred Item 被写明**不因本阶段关闭**。
- `frontend/style.css`、`scripts/check-05-ui-uat.py`、`frontend/vendor/` 逐字节未改。
</success_criteria>

<output>
Create `.planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-03-SUMMARY.md` when done
</output>

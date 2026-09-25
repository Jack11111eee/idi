---
phase: 260925-iin-v1-14-ai-999-1
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - frontend/app.js
  - scripts/check-05-ui-uat.py
  - frontend/style.css
  - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md
  - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md
autonomous: true
requirements:
  - LAYOUT-04
  - TOKEN-08
  - CHECK-01
  - CHECK-02
  - CHECK-03
  - CHECK-04
  - A11Y-01
user_setup: []

estimate:
  tokens: 80000
  raw_tokens: 80000
  tasks: 4
  confidence: low

must_haves:
  truths:
    - "自动跟随恢复:在浏览器里经**应用自身的** `renderEvent` 追加事件后,`#main-pane.scrollTop > 0`,且最新一条 `.event-item` 的 rect 完全落在 `#main-pane` 的可见盒内 —— 全程 harness 未设置过任何 `scrollTop`(FIX 1)"
    - "新增的门**能失败**:把 FIX 1 中和掉(移除 `item.scrollIntoView` 那一行)后,check-05 `--item 9` 的新断言变 FAIL 且 exit 1;还原后回到 PASS —— 变异输出逐字记录(FIX 2)"
    - "`FOCUSABLE_SELECTOR` 与 `frontend/style.css` 的 `:focus-visible` 规则枚举**由一条静态门守住**:两侧逐项(含顺序)不等即 FAIL;把常量收窄一项**或**把 CSS 枚举删一项,该门都变 FAIL,还原后两侧与 HEAD 逐字相同(FIX 5)"
    - "`.collapse-indicator` 在浏览器里的 computed `font-size` 仍为 `20px`(字形渲染尺寸不变),但围栏外不再有裸字号/行高字面量:该规则消费 `--text-lg-plus` 与 `--lh-none`(FIX 3)"
    - "`:root` 围栏内多两条声明(`--text-lg-plus: 20px` / `--lh-none: 1`),各恰有一个消费者且同提交(Hard Rule 5);围栏注释记录了「第 8 档、值序位于 18 与 22 之间、命名阶梯非单调依据 D-07」(FIX 3)"
    - "硬规则 1/2 仍成立:`grep -c '^\\.hidden {' frontend/style.css` == 1;`!important` **声明**数 == 1(注意 `grep -c '!important'` 返回 5 是注释散文陷阱,判据是 `grep -o '!important;' | wc -l`)"
    - "`scripts/check-05-ui-uat.py` 的 blockquote 诊断串陈述真实值(`#646464` / 5.62:1 达标),该函数周围的断言零改动(FIX 4)"
    - "全套门在改动后仍为绿:check-01 / check-02 / check-03 / check-04 / `--item 9`(17 条断言)/ `--item 10`(42 条断言)/ `--item 2` / `--item 7` / `pytest 219 passed, 6 skipped` / `node --check frontend/app.js`"
  artifacts:
    - "frontend/app.js 的 `renderEvent()` 内为 `item.scrollIntoView({ block: 'nearest' })`,原 `eventsEl.scrollTop = eventsEl.scrollHeight;` 那条 no-op 已删除(该串在 app.js 内计数 1 → 0)"
    - "scripts/check-05-ui-uat.py 的 `item9()` 内新增一条判定「自动跟随」的断言(置于 40 条 `renderEvent` 注入块**之前**,因为 `_idi06_reach` 自己会设 `scrollTop`)"
    - "frontend/style.css 围栏内 `--text-lg-plus: 20px;`(紧接 `--text-lg: 18px;`)与 `--lh-none: 1;`(紧接 `--lh-reading: 1.625;`);`.collapse-indicator` 规则改为消费二者"
    - "字号刻度表 7 档 → 8 档的契约同步落盘(见 §已核实的偏差:实际承载该表的文件是 `idi-05-UI-SPEC.md`,不是 brief 写名的 `04-UI-SPEC.md`)"
    - "scripts/check-05-ui-uat.py 第 824 行的陈旧诊断串已订正为 5.62:1 达标"
    - "scripts/check-05-ui-uat.py 的 `_idi07_focus_contract_guards()` 内新增第 ⑤ 条**静态**断言(item 10,`FOCUSABLE_SELECTOR` ↔ `:focus-visible` 枚举逐项比对),连同模块 docstring 的「四条 → 五条」同步;`FOCUSABLE_SELECTOR` 的值与 `frontend/style.css` 均与 HEAD 逐字相同(净改动 0)"
  key_links:
    - "`renderEvent()` 的 `eventsEl.appendChild(item)` → `item.scrollIntoView({block:'nearest'})` → 外层滚动者 `#main-pane` 跟随 → 最新条目在可见盒内(修复的因果链)"
    - "check-05 `item9()` 的新断言 ← 驱动应用自身的 `renderEvent`(**不合成 DOM、不依赖 `--ai-smoke`**);变异(FIX 1 中和)必须让它 FAIL,否则该门与本任务要修的空转门同型"
    - "`.collapse-indicator` 的 `font-size` 声明 → `--text-lg-plus`(20px)→ 字形渲染尺寸不变(浏览器实读 computed,不靠 grep)"
    - "`FOCUSABLE_SELECTOR`(L1748)→ `_focusable_census_js()` → `_IDI07_FOCUS_CENSUS_JS` 的 `document.querySelectorAll(...)` 参数(item 10 的普查判定集);CSS 侧同一条规则的字面量枚举(L1508)消费不了 Python 常量 ⇒ 两侧只能靠**一条静态断言**同步,这条断言今天不存在(注释 L1734-1747 自述「同步靠注释承诺承担」)"
    - "frontend/style.css / frontend/app.js / scripts/check-05-ui-uat.py 改动 ⇒ 六个阶段(idi-04 / 04.1 / 05 / 06 / 07 / 08)的指纹按「内容真变」stale —— **刻意保留**,本任务不重算 `covered_digest`、不重跑那六个阶段的验证"
---

<objective>
v1.14 收口前的四修一票:恢复 AI 事件自动跟随、补一条**真能失败**的门、处置 backlog `999.1` 的两项。

**FIX 1(最重要)** —— `frontend/style.css` 的 `.event-list` 规则**就是** `#ai-events`(`frontend/index.html:76`;`frontend/app.js:5` 绑定 `const eventsEl = document.getElementById('ai-events')`)。Phase 6 的 L-4 收敛(`6adcaa3`,idi-06-02)**原地删掉**了该规则的 `max-height: 55vh` 与 `overflow-y: auto`,于是它计算为 `overflow-y: visible`、**不再是滚动容器** ⇒ `frontend/app.js:253` 的 `eventsEl.scrollTop = eventsEl.scrollHeight`(注释「保持最新可见」)按 CSS 规范**恒为空操作**(不可滚元素的 `scrollTop` 永远是 0)。`app.js` 另外三处 `scrollTop` 写入(`:270` / `:293` / `:299`)全部作用于 `chatMessages`,没有任何代码滚 `#main-pane`。基线 `0c658aa` 上自动跟随**是好用的** ⇒ 这是 v1.14 引入的**回归**,不是既有毛病。修法是让**刚追加的条目**在外层滚动容器里可见 —— **不恢复内滚动**(那会回退 L-4 并打破 check-05 `--item 9` 的滚动者普查,它断言面板区滚动者集合**恰好**是 `{#main-pane, #chat-messages, #latest-check}`)。

**FIX 2** —— check-05 `--item 9` 对此的覆盖是零,且比零更糟:它**正面断言了回归的前提**(`#ai-events 计算 max-height == none  # L-4:套娃第一层(55vh 限高 + 内滚动)已原地删除`),并把滚动者集合钉死在那一组上;它唯一涉及滚动的断言是「末条内容可达」,而那条**自己先设** `c.scrollTop = scrollHeight`(`scripts/check-05-ui-uat.py:2483`)再读 rect —— 那是「显式滚动后可到达」,与「自动跟随」是两个不同性质。新增的断言其**判定性质必须是自动跟随**,且必须**变异证明非空转**。

**FIX 3** —— `.collapse-indicator`(`frontend/style.css:678`)是 `font-size: 20px; line-height: 1;` 两个围栏外裸字面量,属已令牌化的 `--text-*` / `--lh-*` 族,且在 `04-UI-SPEC.md:841` 的封闭例外清单(L-1…L-5)之外。用户已拍定:**加一档字号,保持字形渲染尺寸不变**(不重映射到 18px、不加 L-6 例外)。

**FIX 4** —— `scripts/check-05-ui-uat.py:824` 的 INFO 串陈述在 HEAD 上是反的:该陈述称 `--color-text-muted` 变为 `#8f8f8f`、低于 AA;实测 `--color-text-muted: var(--radix-gray-11)`、`--radix-gray-11: #646464`(= rgb(100,100,100)),在 `--color-surface` 上 **5.62:1**、在 `--color-surface-page` 上 **5.77:1**,两者均达标;`scripts/check-02-contrast.py` 报 `PASS: 0 failures`。**只改那条 INFO / 散文串,不得改动任何断言。**

**FIX 5** —— `scripts/check-05-ui-uat.py:1748` 的 `FOCUSABLE_SELECTOR`(`"button, input, select, textarea, a[href], summary, [tabindex]"`,七项)与 `frontend/style.css` 文件末尾 `:focus-visible` 规则的枚举(规则块起始行 `L1508`,逐行 `button:focus-visible` … `[tabindex]:focus-visible`,同样七项)**今天逐字相同,但没有任何门比对它们**。本文件自己的注释(`:1735-1747`)已承认这一点并说明理由:CSS 侧消费不了 Python 常量,同步「靠注释承诺承担」。失效模式:把常量**收窄**一项(例如删掉 `summary` 或 `[tabindex]`),item 10 的普查判定集就会**静默缩水**(`_IDI07_FOCUS_CENSUS_JS` 经 `_focusable_census_js()` 用该常量生成 `document.querySelectorAll(...)` 的参数),而未覆盖数仍为 0 ⇒ **PASS**。门绿,但覆盖已经变窄 —— 这是本里程碑**第三次**出现的同一缺陷类型(前两次:item 8 的 768px 分支、item 9 的判定集)。修法是新增一条**静态**断言(不需要浏览器、不需要 `--ai-smoke`):从 `frontend/style.css` 解析出该规则的选择器列表,与 `FOCUSABLE_SELECTOR` 逐项比对,不等即 FAIL;并**双向变异证明**它真能失败。

Purpose: 审计(`.planning/v1.14-MILESTONE-AUDIT.md` §5)判 `gaps_found`,唯一的阻断项是 Phase 6 的 L-4 改动引入的**零门覆盖**跨阶段回归 —— 它破坏的是「看 AI 干活」这条核心流程。同时把 backlog `999.1` 的两项一并收口,并把「标签读起来像覆盖了某行为、实际没测」这一**在本里程碑已出现三次**的门弱点,用**两条**带变异证明的断言各补上一次(FIX 2 补 item 9 的自动跟随;FIX 5 补 item 10 的枚举同步)。

Output:
- `frontend/app.js`:一条 `scrollIntoView`(提交 1)
- `scripts/check-05-ui-uat.py`:`item9()` 新增自动跟随断言 + 变异证明记录(提交 2)
- `frontend/style.css`:`--text-lg-plus` / `--lh-none` 两档声明 + `.collapse-indicator` 规则改写 + 围栏注释同步;两份 UI-SPEC 的刻度表同步(提交 3)
- `scripts/check-05-ui-uat.py:824` 陈旧诊断串订正(提交 4)
- `scripts/check-05-ui-uat.py`:`_idi07_focus_contract_guards()` 新增第 ⑤ 条静态断言(`FOCUSABLE_SELECTOR` ↔ `:focus-visible` 枚举逐项比对)+ docstring 同步 + **双向**变异证明记录(提交 5)
- **五个修复各自一个逻辑提交**,全部留在分支 `ui/baseline-and-tokens`
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/quick/260925-iin-v1-14-ai-999-1/260925-iin-BRIEF.md
@.planning/v1.14-MILESTONE-AUDIT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@CLAUDE.md
@.claude/CLAUDE.md
@frontend/app.js
@frontend/style.css
@scripts/check-05-ui-uat.py

**分支:** 留在 `ui/baseline-and-tokens`(与 `260916-t8g` / `260917-fqh` / `260918-qrq` / `260924-vb7` 的先例一致)。`workflow.use_worktrees=false`,顺序执行,无 worktree。

## 锚点已在 HEAD 上逐一复核(计划期实测;**引用周边代码/名字,不靠裸行号**)

**漂移核对:** `git diff --stat bc563d7 ed20ca6 -- frontend/app.js frontend/style.css scripts/check-05-ui-uat.py .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` == **空**。故下表在 HEAD(`ed20ca6`,分支 `ui/baseline-and-tokens`)与 `bc563d7` 上逐字一致;下表的行号是 HEAD 实测值,同时给出**判定锚点的方法**,行号漂移时按方法重新定位。

| 文件 | 锚点(HEAD 实测行号 + 判定方法) |
|---|---|
| `frontend/app.js` | `function renderEvent(event) {` = **L233**;函数体内 `eventsEl.appendChild(item);` = **L252**;紧接一行 `eventsEl.scrollTop = eventsEl.scrollHeight; // 保持最新可见` = **L253** |
| `frontend/app.js` | `panelHeader.querySelector('.collapse-indicator').textContent = collapsed ? '▸' : '▾';` = **L1759**;`docPanelHeader.querySelector(...)` 同形另一处 = **L1765**(`#ai-panel` 与 `#doc-panel` 各一) |
| `frontend/style.css` | `^\.collapse-indicator { font-size: 20px; line-height: 1; }`(单行规则)= **L678** |
| `frontend/style.css` | 字号刻度围栏注释首行 `/* Type scale — 7 sizes …` = **L312**;其中「七档依次为 …」一句 = **L317**;`--text-lg: 18px;` = **L322**;`--text-3xl: 28px;` = **L325** |
| `frontend/style.css` | 行高围栏注释首行 `/* Line height — 四条声明,…` = **L333**;`--lh-reading: 1.625;` = **L342** |
| `frontend/style.css` | 嵌入刻度注释里「契约阶梯的数值序是 12 / 14 / 16 / 18 / 22 / 24 / 28」= **L1440** |
| `frontend/style.css` | `.event-list {` 规则体 = **L748**(已无 `max-height` / `overflow-y`;其上方注释 L746-747 已陈述「条目随外层 #main-pane 滚动」) |
| `frontend/style.css` | `:focus-visible` 规则块起始行 = **L1508**(七选择器,逐行 `button:` / `input:` / `select:` / `textarea:` / `a[href]:` / `summary:` / `[tabindex]:`;规则体 = L1515-1517)—— **FIX 5 的比对对象**。判定方法:用 check-05 已有的 `_idi07_focus_rule_blocks()`(注释感知,注释里的 `:focus-visible` 提及不算)切块,今天恰 1 块 |
| `scripts/check-05-ui-uat.py` | `FOCUSABLE_SELECTOR = "button, input, select, textarea, a[href], summary, [tabindex]"` = **L1748**;其上方注释块 = L1734-1747 |
| `scripts/check-05-ui-uat.py` | `def item2(page, tmp_root):` = **L785**;陈旧诊断串(`#8f8f8f,低于 AA 4.5:1`)= **L824**(在 item 2 内) |
| `scripts/check-05-ui-uat.py` | `_IDI06_REACH_JS` 内 `c.scrollTop = scrollHeight;` = **L2483**(故 FIX 2 的新断言必须排在 `_idi06_reach` **之前**) |
| `scripts/check-05-ui-uat.py` | `def item9(page, tmp_root):` = **L2679**;`_latest_check_max_height_guard(item)` 这一行调用 = **L2728**;40 条 `renderEvent` 注入块 = 注释行 **L2731** + `grown = page.evaluate("""() => {` **L2732** … `}""")` **L2739**;`_idi06_reach(page, item, "#main-pane", "p1", grown,` = **L2740**。判定方法:插入行必须在文本上位于 `_latest_check_max_height_guard(item)` 之后、且在**第一个** `_idi06_reach(` 调用之前(见 Task 2) |
| `scripts/check-05-ui-uat.py` | `def _idi07_focus_contract_guards(item):` = **L3550**;其函数体末尾是 `for token in _IDI07_DECLARED_AND_CONSUMED:` 循环 = **L3640-3651**;下**一个** `^def ` 是 `def _idi07_transition_motion_assert(page, item, state):` = **L3653** ⇒ FIX 5 的第 ⑤ 条插在 **L3651 与 L3653 之间**。判定方法:新代码在 `_idi07_focus_contract_guards` 的 `def` 之后、下一个 `^def ` 之前 |
| `scripts/check-05-ui-uat.py` | 模块 docstring 里 item 10 静态守卫的清单句「**静态契约计数**(`_idi07_focus_contract_guards`)**四条**:①…④…」= **L85**(FIX 5 改为「五条」) |
| `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` | `### 最终字号阶梯(D-06 / D-07,定稿)` = **L164**(表体 L164-181);`### 未在 HEAD 上受控的字号(不属本阶段,见 §不在本阶段)` = **L365**(该节 L365-380;其中把 20px 称作「刻度外的第 6 个渲染字号」的句子 = L367;引述该短语以推翻计数的句子 = L375;`#confirm-error` 16px 一句 = L378);`### 与 .collapse-indicator 的关系(D-23,零交互)` = **L675**,其下 `**`.collapse-indicator` 不得触碰。**` = **L677**(`本阶段不修` = L679);`#ai-panel` 零 CSS 改动段里对同一元素说「**不得触碰**」= **L555-556**;Gate 6 的 `grep -n '^\.collapse-indicator' …` 期望串 = **L913**;`基线(2026-09-20 对 HEAD 实测…)` 里的「字号刻度 = 5 … 裸字面量 = 1」= **L1329-1330**;`## Global Hard Rules` 第 9 条 = **L1033**;Do-Not-Touch List 里 `.collapse-indicator` 行 = **L1067** |
| `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` | `## Typography` = **L315**(Phase 4 的 6 档历史表,正文 L317-348);`### Literal exceptions (the complete list — nothing else may be a literal)` = **L841**;`## Global Hard Rules` = **L942**(只有 1-7 条,**无第 9 条**) |
| `.planning/phases/idi-04-tokens-contract/idi-04-VERIFICATION.md` | 把 `04-UI-SPEC.md:841` §Literal exceptions 列为 `.collapse-indicator` 的替代修法 = **L80** |
| 基线计数(计划期实测复跑) | `^\.hidden {` == **1**;`!important;` == **1**(`grep -c '!important'` == 5 是注释散文陷阱);`--text-*` 声明 **7** 条;`--lh-*` 声明 **4** 条;check-01 / check-03 / check-04 == PASS;`node --check frontend/app.js` == OK;**`--item 9` == `PASS (16 条断言)`;`--item 10` == `PASS (41 条断言)`** |
| 文档基线计数(决定 verify 是否非空转) | `idi-05-UI-SPEC.md`:`260925-iin` == **0**、`第 8 档` == **0**、`--text-lg-plus` == **0**、`8 档`/`八档` == **0**、`赋值路径` == **0**、`20px` 与 `刻度外` 同行 == **1**(仅 L367)、`999.1` == **13**(**故 `999.1` 不能当门** —— 见 Task 3);`04-UI-SPEC.md`:`--text-lg-plus` == **0**、`260925-iin` == **0**、`8 档` == **0** |

## 已核实的偏差(与 brief 不一致,须记入 SUMMARY,不自行扩大范围)

brief 的 FIX 3 末条写「更新 `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md`:字号刻度表(7 档 → 8 档)与其 "hard rule 9" 引用」。**该描述在 HEAD 上不成立:**

- `04-UI-SPEC.md` 的 `## Typography`(L315-348)是 **Phase 4 的 6 档历史表**(`11 / 12 / 13 / 14 / 15 / 16`),其值已被 `idi-04.1-radix` 的 Radix 重写与 Phase 5 推翻(文件 mtime 2026-09-17,此后零改动)。
- `04-UI-SPEC.md` 的 `## Global Hard Rules`(L942)只有 **1-7 条**,**没有第 9 条**。
- **7 档字号刻度表**在 `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §Typography(L164-181),该节自述「本文件重写 `04-UI-SPEC.md` 的同名节(5 档 → 7 档)」;**hard rule 9** 也在同一文件(`## Global Hard Rules` 的第 9 条,HEAD 实测 **L1033**);该文件 §未在 HEAD 上受控的字号(L365-380)**正是**点名 `.collapse-indicator` 的 `20px`「是刻度外的第 6 个渲染字号,属 backlog `999.1`」的地方(L367)—— FIX 3 落地后这句会变假。
- `04-UI-SPEC.md` **确实**在 `idi-04-VERIFICATION.md` 的 `covered_files` 内(brief 的这一句为真),且 `idi-04-VERIFICATION.md:80` 把 `04-UI-SPEC.md:841` §Literal exceptions 列为 `.collapse-indicator` 的**替代修法**(用户已否决该替代,故选令牌路线、不动 L-1…L-5 清单)。

**处置:** 承载「刻度表 7 → 8 档 + hard rule 9 引用」的文件是 `idi-05-UI-SPEC.md`,Task 3 在那里做实质同步;`04-UI-SPEC.md` 只加一条**如实的**「本节已被重写 / 现行刻度为 8 档」指向行(**不改那张 6 档表本身**),以满足 brief 写名的文件。两处都记入 SUMMARY 的 Deviation 一节。

## FIX 3 落地后会变假的散文:逐条分类(改 vs 刻意保留)

分类规则(本计划据此逐条判断,**不是**顺手清理):**带显式时间/阶段限定的陈述**(「本阶段」/ 日期)⇒ **刻意保留**为历史记录;**裸的、无时间限定的绝对禁令** ⇒ **就地收窄措辞**。无论改还是留,SUMMARY 都必须逐条登记。

**刻意保留(不改;SUMMARY 必须登记为「刻意保留,非疏漏」):**

- `idi-05-UI-SPEC.md:913` —— Gate 6 的期望串 `# PASS: 恰好 1 行,内容为 { font-size: 20px; line-height: 1; }`。它写在「**本阶段**新增的两条专用门(零依赖、可独立运行)」标题之下,是 **Phase 5 的门规格**(带「本阶段」限定)。
- `idi-05-UI-SPEC.md:1329-1330` —— 「字号刻度 = **5**(`12/14/16/18/24`);围栏外 `font-size: …px` 裸字面量 = **1**(`.collapse-indicator` 的 `20px`,L434,属 backlog `999.1`)」。它写在「**基线(2026-09-20 对 HEAD 实测,非引用上游文档)**」之下,是**带日期**的历史测量。
- `idi-05-UI-SPEC.md:555-556` —— 「`#ai-panel` 零 CSS 改动(D-16 / D-23)。它的 `▾`/`▸` 指示器(`.collapse-indicator`)是它唯一的可辨状态,**不得触碰** … 本阶段对 `.collapse-indicator` 的规则数改动 = **0**。」带「本阶段」限定,是 Phase 5 的 D-16/D-23 决定;末句对 Phase 5 仍为真。

**就地收窄措辞(改;Task 3 步骤 6b 承担):**

- `idi-05-UI-SPEC.md:677-679` —— 「**`.collapse-indicator` 不得触碰。** … 它的 `font-size: 20px` / `line-height: 1` 越轨字面量属 backlog `999.1`,**本阶段不修**。」**这一条必须改**,理由两条:(a) 它是该禁令的**段级陈述**,而它的**规范登记行**(Do-Not-Touch List 的 L1067)在**同一次提交**里被更新为「已令牌化」—— 登记行说「已改」而段级陈述说「不得触碰」,是文档内部自相矛盾;(b) 它的第一句是**无时间限定的绝对禁令**,FIX 3 落地后字面上为假。**这就是「一条被触碰的 do-not-touch 规则没有留下任何就地承认」这一形态** —— 本项目反复被咬的那一类。改法:只把禁令主体收窄为 `textContent` 赋值路径 / 不得内联 `<svg>`,并登记这一处唯一例外(见 Task 3 步骤 6b)。

**与 brief 的「不要顺手修别的陈旧散文」不冲突:** 上面「就地收窄」的那一条**不是别的散文**,它是 FIX 3 正在触碰的那条禁令本身。`ROADMAP.md` 硬规则 3 的具名源码序例子、`style.css:1498-1502` 的围栏注释等仍然**不碰**。

## 仍然生效的硬规则(源:`.planning/ROADMAP.md` §全局硬规则)

1. `grep -c '^\.hidden {' frontend/style.css` 必须**仍为 1**。
2. `!important` **声明**数必须**仍为 1**(按声明计数,不要数命中行)。
3. **追加,不重排** —— 任何**规则块**不得移动。`:root` 围栏内**新增声明行**不算重排(它不是选择器块,且计划期已核:改后 diff 的「选择器前移」数仍为 0)。
4. 不得新增 `!important`;不得令牌化 `display`;不得引入 `@layer` / `@property` / `var(--x, fallback)`。
5. **不得触碰:** `.fatal` 修饰符;`applyArchiveView` 的两行只读行;`#selection-menu` 的 DOM 位置(必须仍是 `<body>` 直接子元素);`showInlineError` 的 `textContent`-only 规则(XSS 缓解 T-260916-01,不是风格选择);`renderAnnotations` / `renderVerdictCard`;`app.js:4-75` 约 70 个顶层 `getElementById` 句柄(id 不得改名或删除);`.collapse-indicator` 的 `textContent` 赋值路径(`app.js:1759` / `:1765` —— **不得**引入内联 `<svg>`)。
6. 零新增运行时依赖、零构建步骤。

### FIX 3 × 「`.collapse-indicator` 不得触碰」—— 显式调和(必须记入 SUMMARY)

`idi-05-UI-SPEC.md:677` 写「**`.collapse-indicator` 不得触碰。**」,**FIX 3 触碰了这个元素** —— 一条明写的 do-not-touch 规则被触碰而不留承认,正是本项目反复被咬的静默越界形态。故在此显式调和:

- **FIX 3 的改动面被严格限定为该规则的两个「值」声明**:`font-size: 20px` → `var(--text-lg-plus)`、`line-height: 1` → `var(--lh-none)`。同一选择器、同一位置、同一规则块,只换值。
- **该禁令的「理由」未被违反,且仍然成立**:`:677` 给出的理由是「`app.js:1563` / `:1569` 用 `textContent` 赋值,内联 `<svg>` 会被擦掉」。FIX 3 **不碰** `app.js:1759` / `:1765` 的 `textContent` 赋值路径、**不引入**内联 `<svg>`、不改该元素的 DOM 结构、行为、折叠逻辑或任何其他声明。
- **结论:`idi-05-UI-SPEC.md:677` 在实质上仍然为真** —— 该条要守的东西(`textContent` 赋值路径 + 不得内联 `<svg>`)一字未动。
- **但措辞需要就地收窄**(判断,不是可选项):其第一句是**无时间限定的绝对禁令**(「不得触碰」),FIX 3 落地后字面上为假;且它的**规范登记行**(Do-Not-Touch List 的 `idi-05-UI-SPEC.md:1067`)在**同一次提交**里被更新为「已令牌化」—— 登记行说「已改」而段级陈述说「不得触碰」是文档内部自相矛盾。故 Task 3 步骤 6b 把该段的主体收窄为「`textContent` 赋值路径不得触碰」并登记这一处唯一例外。**这不是扩大范围**:它就是 FIX 3 正在触碰的那条禁令本身(逐条分类与理由见上节 §FIX 3 落地后会变假的散文)。
- **SUMMARY 必须记录**:FIX 3 的改动面(仅两个值声明)、`textContent` 路径与「不得内联 `<svg>`」未动、`:677` 在实质上仍为真、以及为何要收窄其措辞。


## 门基线(全部已在修复前 HEAD `bc563d7` 上实测为绿 —— 任何回归即 FAIL)

| 命令 | 基线 |
|---|---|
| `bash scripts/check-01-token-conformance.sh` | PASS |
| `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`(53 PASS + 1 ORDER) |
| `bash scripts/check-03-hidden-uniqueness.sh` | PASS |
| `bash scripts/check-04-important-count.sh` | PASS |
| `.venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled` | `PASS (16 断言, 0 FAIL, 0 BLOCKED)` → FIX 2 后应为 **17 条** |
| `.venv/bin/python scripts/check-05-ui-uat.py --item 10 --browser bundled` | `PASS (41 断言, 0 FAIL, 0 BLOCKED)` → FIX 5 后应为 **42 条** |
| `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped` |
| `node --check frontend/app.js` | OK |

- **必须**用项目 venv `.venv/bin/python` —— 环境 `python3` 是 miniconda,会造出 4 个 `ai_caller` 假失败。
- check-05 **必须**加 `--browser bundled`(`.venv` 路线必须用捆绑 chromium;`channel` + `headless` 在本机会挂死)。
- check-05 **全量**跑会 exit 2,因为 item 5 是**按设计** BLOCKED(两条 opt-in `--ai-smoke` 腿)—— 那是预期,不是回归。本计划**不依赖** `--ai-smoke`。
- 上表的 **item 9 = 16** 与 **item 10 = 41** 已在计划期**实测复跑确认**(不是引用旧记录):`.venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled` → `PASS (16 条断言, 0 FAIL, 0 BLOCKED)`;`--item 10` → `PASS (41 条断言, 0 FAIL, 0 BLOCKED)`。计划期另实测:`_idi07_focus_rule_blocks()` 今天恰切出 **1** 块(起始行 L1508),其选择器基项为 `['button','input','select','textarea','a[href]','summary','[tabindex]']`,与 `FOCUSABLE_SELECTOR.split(",")` 的七项**逐项同序** ⇒ FIX 5 的门在未改动的树上必然 PASS,且常量收窄/CSS 删项两个方向都实测 FAIL。

## 明确不要做的事

- **不要**碰 `.claude/settings.local.json`(其 `Bash(node -e ' *)` 授权是业主已接受的信任边界决定)。
- **不要**提交 `.planning/.idi07-dec*.txt`(未跟踪的临时文件)或 `.planning/v1.14-MILESTONE-AUDIT.md`。
- **不要**重新验证本任务作废指纹的那六个阶段(idi-04 / 04.1 / 05 / 06 / 07 / 08),**不要**重算它们的 `covered_digest`。刷新 digest 等于断言「验证之后什么都没变」,而这里是假的。陈旧性**刻意保留**为可见信号,由里程碑收口统一处理。
- **不要**顺手修别的陈旧散文(例如 `ROADMAP.md` 硬规则 3 的具名源码序例子、`style.css:1498-1502` 的围栏注释)—— 那是已登记的 tech debt,不在本任务范围。
- **不要**重排 `frontend/style.css` 的任何规则;FIX 3 只在原地换两个值,`!important` 声明数仍为 1、`.hidden` 计数仍为 1。
- **FIX 5 只读 `frontend/style.css`**:它**不得**改 style.css 的任何规则、任何声明、任何注释;FIX 5 对 style.css 的净改动必须为 **0**(变异证明里的临时删项必须 `git checkout` 还原)。
- **不要**改 `FOCUSABLE_SELECTOR` 的值(只在 FIX 5 的变异证明里临时收窄并还原),也**不要**改 `_focusable_census_js()` / `_IDI06_CENSUS_JS` / `_IDI07_FOCUS_CENSUS_JS` / `_idi07_focus_rule_blocks` / `_idi07_block_declarations` / `item10()` 的调用序列。
- **不要**顺手修 `scripts/check-05-ui-uat.py:1739` 那句陈旧指认(注释把 `_IDI06_CENSUS_JS` 说成「item 9 的普查」,而它的调用点在 item 7 / item 8)—— 已登记的类型,不在本任务范围。
</context>

<tasks>

<task type="tracer">
  <name>Task 1: FIX 1 — 恢复 AI 事件自动跟随(一条路径端到端打通)</name>
  <files>frontend/app.js</files>
  <action>
只改 `frontend/app.js` 的一处,让 `renderEvent()` 追加条目后把**该条目**滚入外层滚动容器 `#main-pane` 的视野 —— 这是旧行为「列表底边与容器底边齐平」的忠实等价物。这是本计划最薄的一条端到端切片:一次改动同时穿过「JS 追加节点 → CSS 滚动容器层级 → 浏览器实际滚动位置」三层,先证明它真的有效,再由 Task 2 把它固化成门。

1. 在 `renderEvent(event)`(`frontend/app.js:233`)内,把**当前第 253 行**的整条语句 `eventsEl.scrollTop = eventsEl.scrollHeight;` 替换为 `item.scrollIntoView({ block: 'nearest' });`。
   - 依据:`.event-list`(`#ai-events`)已不是滚动容器(Phase 6 L-4 原地删掉了 `max-height` / `overflow-y`),对不可滚元素赋 `scrollTop` 按 CSS 规范**恒为空操作**;真正可滚的是外层 `#main-pane`。
   - `block: 'nearest'` 是刻意选择:条目已在视野内时不产生位移(不打断用户阅读上方内容),不在时才最小幅度滚入。`inline` 用默认值,不要传。
2. 把紧随其后的行尾注释「保持最新可见」改写成陈述**新机制**的一句(点明「滚入外层 `#main-pane` 视野」),不要留一句描述已删除语句的注释。
3. **不要**恢复内滚动(`max-height` / `overflow-y`)—— 那会回退 L-4 并打破 check-05 `--item 9` 的滚动者普查(它断言面板区滚动者集合**恰好**是 `{#main-pane, #chat-messages, #latest-check}`,口径取「恰好」而非「至多」)。
4. **不要**加任何启发式(例如「仅当用户已在底部附近才跟随」)—— 那是超出修复范围的复杂度,且旧行为本身也不区分。
5. **不要**动 `app.js` 里另外三处 `scrollTop` 写入(`:270` / `:293` / `:299`,全部作用于 `chatMessages`,与本次缺陷无关),也**不要**动 `app.js:4-75` 的任何 `getElementById` 句柄(硬规则 5)。
6. 外科手术式改动:除上面这一行语句与其行尾注释外,`app.js` 不得有其他任何行的改动。

**改完自检:`node --check frontend/app.js` 必须 OK;`git diff --stat -- frontend/app.js` 只应显示 1 个文件、±2 行左右。**
  </action>
  <verify>
    <automated>
node --check frontend/app.js

# 端到端运行时证据(临时探针,不提交;写在 /tmp/idi-iin-260925/probe-follow.py)
# 复用 check-05 的模块级设施(与 scripts/check-06-idi05-validation.py 的 load_check05() 同型):
#   c05 = load_check05(); server = c05.ensure_server();
#   playwright bundled chromium(headless=True,viewport 1440x900;不要用 channel='chrome')
#   proj = c05.make_fixture("p1", tmp_root); c05.enter_project(page, proj)
# 单次 page.evaluate 内(该 JS **不得出现任何 scrollTop 赋值**):
#   读 before = #main-pane.scrollTop;
#   for 40 次 renderEvent({kind:'say', content:'第 i 条自动跟随探针:把面板撑到可滚。'});
#   读 after = #main-pane.scrollTop、#main-pane 的 {top,bottom,height} 与 scrollHeight/clientHeight、
#     最后一条 .event-item 的 rect 与标签;
#   返回全部读数。
# 退出码 0 的四个条件(任一不成立即 exit 1 并打印实测读数):
#   (a) before == 0(enter_project 的 page.goto 后为全新加载,锚定「harness 从未滚过」)
#   (b) after > 0(证明是**应用自己**滚的)
#   (c) #main-pane 的 scrollHeight > clientHeight(否则性质平凡成立,记 BLOCKED 不是 PASS)
#   (d) 最后一条 .event-item 的 rect 完全落在 #main-pane 的可见盒内(top >= 盒 top、bottom <= 盒 bottom)
.venv/bin/python /tmp/idi-iin-260925/probe-follow.py
    </automated>
    <human-check>不需要人工判读:四个条件是几何/数值判据。视觉观感(跟随是否「顺眼」)归 UAT,不在本任务。</human-check>
  </verify>
  <done>
- `frontend/app.js` 第 253 行位置上是 `item.scrollIntoView({ block: 'nearest' });`;原先那处对事件列表 `scrollTop` 的赋值语句已消失。核对方式:`grep -n 'scrollTop' frontend/app.js` 只剩 3 处命中,全部落在 `chatMessages` 上(`:270` / `:293` / `:299`);`grep -n 'scrollIntoView' frontend/app.js` 恰 1 处命中,在 `renderEvent()` 内。
- `node --check frontend/app.js` == OK。
- 临时探针 exit 0,四个条件实测值逐字记录进 SUMMARY(含 before=0 / after 的具体像素 / 末条 rect 与容器盒)。
- `git diff --stat -- frontend/app.js` 只有这一个文件、行数 ≤ ±3。
- 提交 1:`fix(260925-iin): restore AI event auto-follow via scrollIntoView on the outer scroller`
- **本任务不改任何 CSS** ⇒ 提交 1 之后 check-01/03/04 与 `--item 9` 应仍为基线值(这正是缺陷「零门覆盖」的体现,Task 2 存在的理由)。
  </done>
</task>

<task type="auto">
  <name>Task 2: FIX 2 — 把「自动跟随」落成一条能失败的门(含变异证明)</name>
  <files>scripts/check-05-ui-uat.py</files>
  <action>
在 check-05 `--item 9` 里新增一条断言,其**判定性质是自动跟随**(不是「显式滚动后可到达」),并**证明它非空转**。

**A. 断言的形状与落点**
1. 落点:在 `def item9(page, tmp_root):` 内(**HEAD 实测 L2679**),**紧接** `_latest_check_max_height_guard(item)` 这一行调用(**HEAD 实测 L2728**)**之后**,且**紧接** 40 条 `renderEvent` 注入块**之前** —— 该块以注释行 `# `#main-pane`:经应用自身的 renderEvent 注入足量条目到 #ai-events(不手工拼 DOM)。`(**L2731**)开头,块体是 `grown = page.evaluate("""() => {`(**L2732**)… `}""")`(**L2739**)。
   - **必须排在 `_idi06_reach(page, item, "#main-pane", "p1", grown, …)`(**HEAD 实测 L2740**)**之前** —— `_idi06_reach` 内部经 `_IDI06_REACH_JS` 自己设 `c.scrollTop = scrollHeight`(`scripts/check-05-ui-uat.py:2483`),会把「harness 从未滚过」这个前提毁掉,新断言排在它后面就恒绿。**这是本任务正确性的承重点**(排在它之后就恒绿,即空转门)。
   - **判定落点的方法(不靠行号,行号会漂移):** 新断言的插入行在文本上必须位于 `_latest_check_max_height_guard(item)` 这一行**之后**,且在 `item9()` 内的**第一个** `_idi06_reach(` 调用**之前**。落盘后用 `grep -n '_latest_check_max_height_guard(item)\|_idi06_reach(page, item\|renderEvent({kind: .say.' scripts/check-05-ui-uat.py` 逐行核对这三者的相对顺序。
2. 探针用一次 `page.evaluate` 完成「读 before → 经应用自身的 `renderEvent` 追加 N 条 → 读 after 与几何」,该 JS **不得出现任何 `scrollTop` 赋值**(这是「harness 自己从未设置过 `scrollTop`」的可核形态;把这一点写进断言旁的注释)。
   - 必须驱动**应用自己的** `renderEvent`(SSE handler 调用的同一个函数),**不得**合成 DOM、不得直接 `appendChild`。`kind` 取 `'say'`(对 `done` / `error`,`renderEvent` 会解除「发起」按钮禁用,污染后续项)。
   - **不得**依赖 `--ai-smoke`(那两条腿需要活的 CLI 调用且是 opt-in)。
3. 判据:追加后 `#main-pane.scrollTop > 0`,**且**最后一条 `.event-item` 的 rect 完全落在 `#main-pane` 的可见盒内。
   - **`before == 0` 不进判据,进第 4 步的前提链**(见下)。把它写进判据会让「起始滚动位非 0」——一个**被测前提不成立**的情形——报成 **FAIL**(回归信号),而它其实无从判定。前提不成立记 `BLOCKED`,判据不满足才记 `FAIL`;两者不是同一件事。
4. **反空转前提(任一不成立记 `blocked(...)`,绝不记 PASS —— 与 `_idi06_reach` 的前提链同型,威胁表 T-idi-06-10 的落点):** `#main-pane` 存在;**追加前 `#main-pane.scrollTop == 0`**(否则「自动跟随」与「本来就在底部」不可区分);`rect.height > 0` 且 `display != 'none'`;注入后 `scrollHeight > clientHeight`(否则性质平凡成立);注入后 `#ai-events .event-item` 计数 > 0;`renderEvent` 可用。
5. 断言文案要让「这条门测的是什么」一目了然,并在 note 里点明与既有「末条内容可达」的区别:后者是**显式滚动后**的可达性,本条是**应用自动跟随**。同时用 `info(...)` 逐行落盘原始读数(before / after / scrollHeight / clientHeight / 末条 rect / 容器盒)—— 本项目的纪律是不给结论替代证据。
6. 复用既有的 `ok_true(...)` / `blocked(...)` / `info(...)` 助手与 item 9 的既有标签风格;**不要**改 `_idi06_reach`、`_IDI06_REACH_JS`、滚动者普查、或 item 9 的任何既有断言(那条普查断言 `#ai-events 计算 max-height == none` 是 L-4 的正确断言,只是对自动跟随零覆盖 —— 保留它,补它)。

**B. 变异证明(本任务的核心交付,不可省)**
7. 先跑一次基线,确认新断言 PASS 且断言总数为 **17**(基线 **16** + 1)。**16 已在计划期实测复跑确认**(`.venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled` → `PASS (16 条断言, 0 FAIL, 0 BLOCKED)`),故 17 的得出方式是「实测基线 + 本任务无条件新增的恰 1 条」;条数不是 17 即为偏差,先查清再提交。
8. 中和 FIX 1:临时把 `frontend/app.js` 的 `item.scrollIntoView({ block: 'nearest' });` 那一行删掉(或注释掉)。
9. 重跑 `.venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled`,确认**新断言变 FAIL**(该次运行 exit 1),并把该次输出的相关片段**逐字**记录(至少含新断言的 `FAIL` 行、其 expected/actual、以及汇总的 `item 9: FAIL (17 条断言, …)` 与 `exit=1`)。
   - 若中和之后新断言仍 PASS,说明该门是空转的 —— **停下**,修断言(通常是判据落成了「显式滚动后可达」),再重跑变异,直到它真的 FAIL。
10. 还原 `app.js`(用 `git checkout -- frontend/app.js` 或手工还原),确认 `git diff -- frontend/app.js` **为空**(变异不得留残留),再重跑一次 `--item 9` 确认回到 PASS(17 条断言,0 FAIL,0 BLOCKED)。

**C. 提交**
11. 提交 2:`test(260925-iin): add a mutation-proven auto-follow assertion to check-05 item 9`(只含 `scripts/check-05-ui-uat.py`;`app.js` 的变异必须已还原)。

**不要**顺手改 item 9 的滚动者普查口径、L-5/L-6 普查、或任何别的项。**不要**新增 `--ai-smoke` 依赖。
  </action>
  <verify>
    <automated>
.venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled
#   期望:item 9: PASS  (17 条断言,0 FAIL,0 BLOCKED);exit=0
#   基线 16 条(计划期已实测复跑)⇒ 新增恰 1 条。条数不是 17 即为偏差,先查清再提交。

# 变异证明(逐字记录输出)
# 1) 删掉 frontend/app.js 里的 item.scrollIntoView 那一行
.venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled
#   期望:新断言 FAIL,item 9: FAIL (17 条断言, ≥1 FAIL, 0 BLOCKED);exit=1
#   变异输出必须逐字落进 SUMMARY(含 FAIL 行的 expected/actual)
# 2) 还原
git checkout -- frontend/app.js
git diff -- frontend/app.js
#   期望:空
.venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled
#   期望:回到 PASS (17 条断言, 0 FAIL, 0 BLOCKED)
node --check frontend/app.js
    </automated>
  </verify>
  <done>
- `scripts/check-05-ui-uat.py` 的 `item9()` 内新增恰一条断言,落点在 `_latest_check_max_height_guard(item)` 之后、40 条注入块之前;该断言经应用自身的 `renderEvent` 驱动,JS 内零 `scrollTop` 赋值。
- 修好树:`--item 9` == `PASS (17 条断言, 0 FAIL, 0 BLOCKED)`。
- 变异树:同一条命令下新断言 == `FAIL`,exit 1,**变异输出逐字记录**在 SUMMARY(证明非空转)。
- 还原后 `git diff -- frontend/app.js` 为空,`node --check` OK,`--item 9` 回到 PASS。
- item 9 既有断言(滚动者普查 / 两处 `max-height == none` / 末条可达 / L-5 / L-6)全部保留且仍 PASS。
- 提交 2 只含 `scripts/check-05-ui-uat.py`。
  </done>
</task>

<task type="auto">
  <name>Task 3: FIX 3 + FIX 4 — 字号第 8 档与契约同步(提交 3)、陈旧诊断文案订正(提交 4)</name>
  <files>frontend/style.css, .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md, .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md, scripts/check-05-ui-uat.py</files>
  <action>
**—— 提交 3:FIX 3(加一档字号,保持字形渲染尺寸不变)——**

**A. 围栏内新增两条声明(同提交各配一个消费者,Hard Rule 5)**
1. 在 `:root` 的 `--text-lg: 18px;`(`frontend/style.css:322`)之后**紧接**插入一行 `--text-lg-plus: 20px;`(保持「紧邻其余 `--text-*`」;声明序变为 xs 12 / base 14 / md 16 / lg 18 / **lg-plus 20** / xl 24 / 2xl 22 / 3xl 28)。
   - **不要**把它放到 `--text-3xl` 之后,也不要动任何既有声明行 —— 围栏内新增声明行**不是**硬规则 3 意义上的「重排」(重排指选择器块移动;改后「选择器前移」数仍须为 0)。
2. 在 `--lh-reading: 1.625;`(`:342`)之后**紧接**插入一行 `--lh-none: 1;`。
   - 围栏内是字面量的合法居所(L-4),`1` 是单位值不是裸 hex,CHECK-01 不受影响。
   - 行尾或上一行注释写明**唯一消费者**:`.collapse-indicator`(`▾`/`▸` 字形,须恰占一个行盒,否则 20px 的字形盒会被行高撑开)。

**B. 围栏注释同步(这是用户决策明确要求的记录)**
3. 字号刻度注释(`:312-317`):把 `7 sizes` 改为 `8 sizes`;把「七档依次为 xs 12px / … / 3xl 28px。」扩为**八档**并加入 `lg-plus 20px`;并**写明**:这是第 8 档,值 20px,**插在 `--text-lg`(18)与 `--text-2xl`(22)之间**;**命名阶梯非单调的依据是已登记的 D-07 冲突**(`--text-xl` 24 > `--text-2xl` 22),**不是笔误,不要「修正」它**;第 8 档的唯一消费者是 `.collapse-indicator`。
4. 行高注释(`:333-342`):把「四条声明」改为**五条**;把「与 7 档字号刻度按比率配对」改为「与 8 档字号刻度」;并补一句:新增的 `--lh-none`(1)是 **glyph-only** 行高,**不属字号刻度配对** —— 与既有的 `--lh-compact`(chrome-only)同型;因此第 8 档(20px)不进入上面那张比率配对表,该表逐项不变。
5. 嵌入刻度注释(`:1440-1442`):把「契约阶梯的数值序是 12 / 14 / 16 / 18 / 22 / 24 / 28」改为含 20 的数值序,并**补一句**说明:嵌入档的取值**钉在已出货的三对上**(28 → 24 / 22 → 18 / 18 → 16),**不**从数值阶梯重新推导 —— 否则插进 20 这一档后,22 的「下一档」会变成 20,而 `.markdown-body h2` 的嵌入档由 check-05 `--item 7` 断言为 `--text-lg`(18px)。这是本次加档的**直接后果**(注释若不改就自相矛盾),不是新增设计决策。

**C. 规则改写(围栏外零裸字面量)**
6. `frontend/style.css:678` 原地改写为消费两个新令牌:`.collapse-indicator { font-size: var(--text-lg-plus); line-height: var(--lh-none); }`。
   - **不要**重映射到 18px / 24px;「不要」加 L-6 例外(用户已否决这两个形态)。
   - 这是**同一选择器、同一位置**的声明值替换,**不是**规则块移动(硬规则 3)。
   - **不要**碰 `.collapse-indicator` 的 `textContent` 赋值路径(`app.js:1759` / `:1765`)—— 不得引入内联 `<svg>`(它会被 `textContent` 擦掉)。
   - **不要**碰该规则附近的任何其他规则。
   - **改动面必须逐字限定为该规则的两个「值」**:只把 `font-size: 20px` 的值换成 `var(--text-lg-plus)`、把 `line-height: 1` 的值换成 `var(--lh-none)`。不改该规则的选择器、不改规则块的起止行、不新增/删除该规则内的声明、不动该元素的 DOM 结构、行为、折叠逻辑或任何其他属性。**这正是 `idi-05-UI-SPEC.md:677` 的「不得触碰」在实质上仍然为真的依据**(该条要守的是 `textContent` 赋值路径 + 不得内联 `<svg>`,两者一字未动;详见 §FIX 3 × 「`.collapse-indicator` 不得触碰」—— 显式调和)。

6b. **收窄 `idi-05-UI-SPEC.md:677-679` 的措辞(与步骤 6 同提交)** —— 该段现为:「**`.collapse-indicator` 不得触碰。** `app.js:1563` / `:1569` 用 `textContent` 赋值,内联 `<svg>` 会被擦掉(`#ai-panel` 与 `#doc-panel` 是两个可折叠面板,各有自己的指示器)。它的 `font-size: 20px` / `line-height: 1` 越轨字面量属 backlog `999.1`,**本阶段不修**。」
    - 把第一句的主体从「整个元素」收窄为「`textContent` 赋值路径」,并**登记这一处唯一例外**。落盘文本:
      **「`.collapse-indicator` 的 `textContent` 赋值路径不得触碰。」** `app.js:1563` / `:1569` 用 `textContent` 赋值,内联 `<svg>` 会被擦掉(`#ai-panel` 与 `#doc-panel` 是两个可折叠面板,各有自己的指示器)。**唯一例外(quick `260925-iin`):** 该规则的 `font-size` / `line-height` 两个**声明值**已换成令牌(`--text-lg-plus` / `--lh-none`)—— 只改值,`textContent` 赋值路径与「不得内联 `<svg>`」一字未动,故本条禁令**在实质上仍然成立**;backlog `999.1` 第 1 项由此关闭。
    - 理由(SUMMARY 必须记录):原句是无时间限定的**绝对**禁令,而 FIX 3 确实触碰了该元素;且它的规范登记行(`:1067`)在同一次提交里被更新为「已令牌化」—— 登记行说「已改」而段级陈述说「不得触碰」是文档内部自相矛盾。**这是本项目反复被咬的「散文承诺与实际状态脱钩」形态,故不留着。**
    - **只改这一段的这两句**;`idi-05-UI-SPEC.md:555-556`、`:913`、`:1329-1330` 三处**刻意保留**(逐条分类与理由见 §FIX 3 落地后会变假的散文)。

**D. 契约文档同步(刻度表 7 → 8 档 + hard rule 9 引用)**
7. **主要承载文件是 `idi-05-UI-SPEC.md`**(见 §已核实的偏差;下面的行号是 HEAD 实测,判定方法见锚点表):
   - §Typography 的 §最终字号阶梯(该节标题 `### 最终字号阶梯(D-06 / D-07,定稿)` = **L164**,表体 L164-181):表由 **7 档 → 8 档**,加入 `--text-lg-plus` 20px 一行,并注明它位于 `--text-lg`(18)与 `--text-2xl`(22)之间、命名阶梯非单调依据 D-07。
     - 该节**L166 整句**改写:「**7 档。** 5 → 7,新增两档。」→「**8 档。** 5 → 7 新增两档(Phase 5);7 → 8 新增一档(quick `260925-iin`,`--text-lg-plus` 20px)。」——**不要把这一行只改一半**:该句的「7 档」与「5 → 7,新增两档」是同一个断言的两半,只改前者会让它自相矛盾。**`--text-md` 16px 正文本体不变这半句逐字保留。**
   - §未在 HEAD 上受控的字号(该节标题 = **L365**,节体 L365-380):把 **L367** 那句「`.collapse-indicator` 的 `font-size: 20px`(`:434`)是刻度外的第 6 个渲染字号,属 backlog `999.1`」改写为「**已不再是刻度外字号** —— 已由 quick `260925-iin` 落为第 8 档 `--text-lg-plus`,backlog `999.1` 第 1 项关闭」。
     - **判据:改后 `20px` 与 `刻度外` 不再出现在同一行**(计划期实测:今天恰 1 行即 L367)。**L375 那句引述该短语以推翻计数的句子不动** —— 它讲的是 P-20 那次「枚举不全」的发现,是另一件事,不属于本任务的改动面。
     - 同段的 `#confirm-error` 16px 一条(**L378**)**仍然存在**,不要顺手改它。
   - Do-Not-Touch List 里 `.collapse-indicator` 那一行(**L1067**;HEAD 实测,不是「L1043 附近」):把「本阶段零改动 / 属 backlog `999.1`」更新为「已由 quick `260925-iin` 令牌化(值不变,仍 20px);`textContent` 赋值路径仍不得触碰」。
   - hard rule 9 的**引用**处:该文件 `## Global Hard Rules` 第 9 条 = **L1033**,它本身讲的是「不得写全局标题规则 + 渲染目标逐个列举」,**与本改动无冲突,不要改写其正文**;只在紧邻处(或其所在清单的说明行)加一句**引用登记**:本次新增的令牌只被 `.collapse-indicator` 消费,未新增任何标题字号规则,故第 9 条不受影响 —— 这正是 brief 要求的「hard rule 9 引用」同步。
   - **刻意保留(不改,但 SUMMARY 必须登记为「刻意保留,非疏漏」):** `:555-556`(`#ai-panel` 零 CSS 改动段里的「不得触碰」+「本阶段…= 0」)、`:913`(Gate 6 的期望串)、`:1329-1330`(2026-09-20 的日期基线)。三处都带显式时间/阶段限定,是历史记录;逐条分类与理由见 §FIX 3 落地后会变假的散文。
8. **`04-UI-SPEC.md`(brief 写名的文件)**:在其 `## Typography` 节标题(现 L315)之下、正文之前**加一条如实指向行**:声明本节那张表是 Phase 4 的历史声明(6 档),已被 `idi-05-UI-SPEC.md` 的 `## Typography` 重写;截至 quick `260925-iin`,现行刻度为 **8 档**,含新增的 `--text-lg-plus` 20px。
   - **不要**改那张 6 档表本身,也**不要**往 L-1…L-5 §Literal exceptions 清单里加条目(加例外是用户已否决的替代修法)。
9. 提交 3(只含 `frontend/style.css` + 两份 UI-SPEC):
   `fix(260925-iin): declare an 8th type tier for .collapse-indicator and sync the scale contract`

**—— 提交 4:FIX 4(订正一条陈旧诊断文案)——**

10. `scripts/check-05-ui-uat.py:824` 的字符串字面量(`" —— --color-text-muted 在 260918-qrq 换肤后由 #6a6a6a 变为 #8f8f8f,低于 AA 4.5:1"`)改为陈述**真实值**:`--color-text-muted` = `--radix-gray-11` = `#646464`(rgb(100,100,100)),在 `--color-surface` 上 **5.62:1**、在 `--color-surface-page` 上 **5.77:1**,**两者均达标**;并保留「只记录不判定(非正文)」的口径。
    - **只改这一条 INFO / 散文串。** `item2()` 内周围的断言(含 `parse_rgb(colors["quoted"])` / `contrast_ratio` / 上面那条 `>=4.5:1` 的 `ok(...)`)是**正确的**,一字不动。
    - 该串内的数字必须与 `scripts/check-02-contrast.py` 的实测一致(计划期已跑:`PASS: 0 failures`);改完再跑一次 `--item 2` 复核。
11. 提交 4(只含 `scripts/check-05-ui-uat.py`):
    `docs(260925-iin): correct the stale --color-text-muted diagnostic in check-05`
  </action>
  <verify>
    <automated>
# ---- FIX 3:字形仍须渲染为 20px(浏览器实读 computed,不得只 grep)----
# 临时探针 /tmp/idi-iin-260925/probe-font.py(与 Task 1 同型:load_check05() + ensure_server()
# + bundled chromium headless + enter_project(p1));读**两个** .collapse-indicator 实例的
# getComputedStyle(el).fontSize 与 lineHeight;退出码 0 当且仅当两者 fontSize == "20px"
# 且 lineHeight == "20px"(line-height: 1 对 20px 字号解析为 20px)。打印逐实例读数。
.venv/bin/python /tmp/idi-iin-260925/probe-font.py

# ---- FIX 3:围栏外的裸字面量清零 + 硬规则 1/2 ----
grep -n 'font-size: 20px' frontend/style.css        # 0 命中(围栏外的裸字号已消失)
grep -n 'line-height: 1;' frontend/style.css        # 0 命中
grep -c -- '^  --text-' frontend/style.css          # 8(原 7)
grep -c -- '^  --lh-' frontend/style.css            # 5(原 4)
grep -n 'var(--text-lg-plus)' frontend/style.css    # 1(.collapse-indicator)
grep -n 'var(--lh-none)' frontend/style.css         # 1(.collapse-indicator)
grep -c '^\.hidden {' frontend/style.css            # 1
grep -o '!important;' frontend/style.css | wc -l    # 1(不是 grep -c '!important' 的 5)

# ---- FIX 3:围栏注释同步(步骤 3/4/5)。基线为 0(或旧串为 1)才证明非空转:
#      上面那批 `--text-*` / `--lh-*` / consumer 计数在**注释原封不动**时**照样通过**,
#      故它们**不能**充当注释同步的判据。这五对是全半场的唯一门。
grep -c '8 sizes' frontend/style.css                 # 1(基线 0;步骤 3)
grep -c '7 sizes' frontend/style.css                 # 0(基线 1;步骤 3 的旧串已消失)
grep -c 'Line height — 五条' frontend/style.css      # 1(基线 0;步骤 4)
grep -c 'Line height — 四条' frontend/style.css      # 0(基线 1;步骤 4 的旧串已消失)
grep -c '与 8 档字号刻度' frontend/style.css         # 1(基线 0;步骤 4 的配对表口径)
grep -c '18 / 20 / 22' frontend/style.css            # 1(基线 0;步骤 5 的新数值序含 20)
grep -c '18 / 22 / 24 / 28' frontend/style.css       # 0(基线 1;步骤 5 的旧数值序已消失)
#   ⚠ 裸 `grep -c '四条'` 不可用作判据(基线 5,散落多处);必须锚到整句 `Line height — 四条`。

bash scripts/check-01-token-conformance.sh          # PASS
bash scripts/check-03-hidden-uniqueness.sh          # PASS
bash scripts/check-04-important-count.sh            # PASS
.venv/bin/python scripts/check-02-contrast.py | tail -1   # PASS: 0 failures
node --check frontend/app.js                        # OK

# ---- FIX 3:契约文档 ----
# 括号里是**计划期在未改动的树上实测的基线**。基线为 0(或那条语句存在)才证明该条非空转:
# 一条改没改都给同样结果的计数是**空转门**,不能当判据。
F5=.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md
F4=.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md
grep -c '8 档\|八档' "$F5"                      # 期望 >= 1(基线 0)
grep -c -- '--text-lg-plus' "$F5"               # 期望 >= 2(基线 0:刻度表新行 + 999.1 节的关闭登记)
grep -c -- '--text-lg-plus' "$F4"               # 期望 == 1(基线 0:指向行)
grep -c '260925-iin' "$F5"                      # 期望 >= 2(基线 0:999.1 节 + Do-Not-Touch 行)
grep -c '260925-iin' "$F4"                      # 期望 == 1(基线 0:指向行)
grep -c '第 8 档' "$F5"                         # 期望 >= 1(基线 0)
grep -c '20px.*刻度外\|刻度外.*20px' "$F5"       # 期望 0(基线 1:今天只有 L367 把 20px 与「刻度外」写在同一行)
grep -c '赋值路径' "$F5"                        # 期望 >= 1(基线 0:L677 收窄后的禁令主体 + L1067 的登记行)
#   ⚠ 计划期实测 `grep -c '999.1' "$F5"` == **13** —— 该计数**不能当门**(改没改都 >= 1,
#     这正是 FIX 2 / FIX 5 要治的「门无法失败」同型缺陷),故本块不用它。
#   ⚠ `:555-556` / `:913` / `:1329-1330` 三处**刻意保留**,没有对应的门(它们是历史记录,
#     见 §FIX 3 落地后会变假的散文);SUMMARY 必须登记。

# ---- FIX 4:陈旧串消失、真值出现、断言零改动 ----
grep -c '8f8f8f' scripts/check-05-ui-uat.py         # 0
grep -c '5.62:1' scripts/check-05-ui-uat.py         # 1
.venv/bin/python scripts/check-05-ui-uat.py --item 2 --browser bundled
#   期望:item 2: PASS(0 FAIL, 0 BLOCKED);exit=0 —— 断言未受影响
    </automated>
  </verify>
  <done>
- `.collapse-indicator` 两个实例的 computed `font-size` 均为 `20px`(浏览器实读,逐实例记录);`line-height` 解析为 `20px`。
- 围栏内 `--text-*` 声明 7 → 8、`--lh-*` 4 → 5;`var(--text-lg-plus)` 与 `var(--lh-none)` 各恰 1 处消费(同一提交,Hard Rule 5 核账成立)。
- 围栏注释记录了第 8 档、值序位于 18 与 22 之间、命名阶梯非单调依据 D-07;行高注释记录了 `--lh-none` 的 glyph-only 性质与唯一消费者;嵌入刻度注释的数值序与「钉在已出货三对」的说明已同步。**这三处注释同步各有一条基线为 0 的 grep 守着**(`8 sizes` / `Line height — 五条` / `与 8 档字号刻度` / `18 / 20 / 22`),旧串各有一条「已消失」grep(`7 sizes` / `Line height — 四条` / `18 / 22 / 24 / 28` 计数 0)—— 声明与门同时存在,不留「有声明、无门」。
- 硬规则 1/2 仍成立(`^\.hidden {` == 1;`!important;` == 1);check-01/02/03/04 全 PASS;`node --check` OK。
- 两份 UI-SPEC 已按 §已核实的偏差 处置:`idi-05-UI-SPEC.md` 承载实质同步(7 → 8 档 + 999.1 关闭 + hard rule 9 引用登记,第 9 条正文未改),`04-UI-SPEC.md` 加如实的指向行(6 档历史表与 L-1…L-5 清单**未改**)。
- **FIX 3 落地后变假的散文已逐条分类处置**(见 §FIX 3 落地后会变假的散文):`:677-679` 的段级禁令**已收窄措辞**并登记唯一例外;`:555-556` / `:913` / `:1329-1330` 三处**刻意保留**为历史记录。四条都记入 SUMMARY。
- **`.collapse-indicator` 的改动面逐字限定为该规则的两个值声明**:`app.js:1759` / `:1765` 的 `textContent` 赋值路径与「不得内联 `<svg>`」一字未动;`git diff -- frontend/app.js` 在提交 3 内**为空**(该文件只被提交 1 改过)。
- **硬规则 3 / 4 无机械门,属人工核对项**(见 SUMMARY 义务):本次编辑在结构上不可能引入规则块移动、`@layer` / `@property` / `var(--x, fallback)`;`check-01` 只覆盖围栏标记 / 裸 hex / tier-1 泄漏。该覆盖缺口**记录**在 SUMMARY,不新造脚本。
- `scripts/check-05-ui-uat.py` 中 `8f8f8f` 计数 0、`5.62:1` 计数 1;`--item 2` PASS;`item2()` 的断言零改动(`git diff` 只显示那一行字符串)。
- 提交 3、提交 4 各自只含上述文件。
  </done>
</task>

<task type="auto">
  <name>Task 4: FIX 5 — 把 `FOCUSABLE_SELECTOR` 与 `:focus-visible` 枚举的同步落成一条**能失败**的静态门(含双向变异证明)</name>
  <files>scripts/check-05-ui-uat.py</files>
  <action>
**归属判断(先说清,再动手):本条进 item 10,不进 item 9。**
- 被守的性质是「`FOCUSABLE_SELECTOR` 的枚举 == `frontend/style.css` 的 `:focus-visible` 规则的选择器枚举」。那条规则**就是**焦点环的覆盖集,而 item 10 是「A11Y-01 焦点环」项;item 9 是「L-4 面板区滚动容器收敛」,把一条焦点环枚举断言塞进 item 9 是**错误标签**。
- item 10 已经有**同型、同文件、同一次读取**的静态契约守卫家族:`_idi07_focus_contract_guards(item)`(**HEAD 实测 L3550**)在 `item10()` 的**第一件事**就被调用(在 `make_fixture` / `enter_project` **之前**),其 docstring 明说这是「**静态**契约计数静态断言 … **不依赖任何运行时状态**」。第 ⑤ 条与该家族已有的四条共用同三条纪律(`OSError ⇒ blocked()`、打印命中行号、比的是「实测 vs 独立决策常量」不是自比),完全同型。
- 失效面在 item 10 一侧最直接:`_IDI07_FOCUS_CENSUS_JS` 经 `_focusable_census_js()` 用本常量生成 `document.querySelectorAll(...)` 的参数,收窄常量 ⇒ **item 10 的普查判定集静默缩水**,而未覆盖数仍为 0 ⇒ PASS。(注:`_IDI06_CENSUS_JS` 也消费同一常量,但它的调用点在 item 7 / item 8 —— 本文件注释 L1739 把 `_IDI06_CENSUS_JS` 说成「item 9 的普查」是陈旧指认,**不在本任务范围,不要顺手改**。)
- **断言目标数:item 10 由 41 → 42;item 9 不变(仍是 Task 2 后的 17)。****42 如何得出:** 计划期在 HEAD 上**实测复跑** `--item 10 --browser bundled` == `PASS (41 条断言, 0 FAIL, 0 BLOCKED)`;第 ⑤ 条在健康路径上**无条件恰好发出 1 条断言**(它只在一种情形下走 `blocked(...)` 分支,那也仍是 1 条),故 **41 + 1 = 42**。计划期另实测:该条在未改动的树上 PASS(两侧七项逐字同序),常量收窄一项 ⇒ FAIL,CSS 删一项 ⇒ FAIL。

**A. 断言的形状与落点**
1. 落点:`_idi07_focus_contract_guards(item)` 的函数体内,**紧接** `for token in _IDI07_DECLARED_AND_CONSUMED:` 那个循环之后(HEAD 实测该循环占 **L3640-3651**),即插在 **L3651 与 L3653**(`def _idi07_transition_motion_assert(page, item, state):`)之间。**判定落点的方法(不靠行号):** 新代码必须在 `_idi07_focus_contract_guards` 的 `def` 之后、且在下一个 `^def ` 之前。
2. 该条**只读文件文本**,不做任何 `page.*` 调用 —— 与同函数内已有的四条同型(它们都在 `make_fixture` 之前跑,故**不需要浏览器**)。**不得**依赖 `--ai-smoke`,**不得**依赖浏览器。
3. 复用本文件**已有**的注释感知切分器 `_idi07_focus_rule_blocks(text)`(HEAD 实测 **L3479**;它逐行跟踪注释状态,注释里的 `:focus-visible` 提及**不算**规则块),取含 `:focus-visible` 的规则块。
4. **反空转前提(任一不成立记 `blocked(...)`,绝不记 PASS —— 与同函数内已有各条同型):**
   - `len(blocks) == 1`(今天实测恰 1 块,起始行 **L1508**)。0 块 ⇒ 比对无对象;>1 块 ⇒ 选择器列表有歧义,不能拿 `blocks[0]` 冒充。(注释里的 `:focus-visible` 提及今天有 2 处 —— L239 / L1482 —— 正是切分器要剔除的东西。)
   - 该块的选择器部分(块内**第一个 `{` 之前**的代码)**非空**;否则 `blocked`。
   - **项数不进前提(本项的唯一前提就是上面两条结构性条件)。** 「恰 7 项」**不是**前提:项数不符(例如 CSS 侧被收窄成 6 项、或常量侧被收窄成 6 项)必须**流入第 6 步的逐项比较并记 `FAIL`**。把项数写进 `blocked()` 前提会让变异 B 得到 `BLOCKED` 而非 `FAIL`,与 `<done>` 要求的证据互斥 —— 变异证明要的是「门真的报了错」,而 `BLOCKED` 是「前提不成立、无从判定」,两者不是同一件事。
5. 归一两侧:
   - CSS 侧:把每个选择器项 `strip()`,若以 `:focus-visible` 结尾则去掉该后缀,得基选择器。
   - Python 侧:`[s.strip() for s in FOCUSABLE_SELECTOR.split(",")]`(HEAD 实测 `FOCUSABLE_SELECTOR = "button, input, select, textarea, a[href], summary, [tabindex]"` 在 **L1748**)。
6. **判据:`ok_true(...)`,条件为两侧列表「逐项相同」** —— `css_base == py_items`,**有序**比较,不是集合比较。
   - **为什么比集合更强(机制选择,已说明):** `FOCUSABLE_SELECTOR` 上方的注释(L1734-1747)已声明「`:focus-visible` 规则的选择器列表(**顺序亦同**)」,而那条「顺序亦同」今天**没有任何门在守** —— 一条声明了却没门守的不变量,正是本任务要治的缺陷类型。有序比较**蕴含**集合相等(故完全覆盖「集合不等即 FAIL」这条要求),今天两侧逐字同序 ⇒ **零假 FAIL 风险**(计划期实测两侧均为 `['button','input','select','textarea','a[href]','summary','[tabindex]']`)。若日后确需换序,两侧一起换即可(提示里会说明)。
   - 失败时的**可执行提示**(写进 note,照本文件既有惯例 —— item 10 现有普查断言的提示已经是「到 `frontend/style.css` 文件末尾补它的选择器,并同步本文件的 `FOCUSABLE_SELECTOR`」):
     - **两侧必须同一次改完,永远不要只改一侧。** 只改 CSS ⇒ 门仍按旧集合普查,于是「规则覆盖了谁」与「门检查了谁」重新分叉,而**门会绿**(静默缩水)—— 这正是 `G-idi-05-1` 的成因。只改常量 ⇒ 普查会枚举到 CSS 规则没给环的元素,item 10 的运行时普查断言会报「未覆盖数 > 0」,症状是响的、不是静的。
     - **哪一侧是权威:** CSS 规则是**真正授予环**的工件,常量是门对它的**镜像**。两者不一致时,先判断本次改动的**本意**是哪一侧(是「规则要多覆盖一类可聚焦元素」还是「常量被误收窄」),再把另一侧同步到它 —— 不要两边各改一半。
     - **顺序也要一致:** 同一份列表、同一顺序;确需换序时两侧一起换。
     - 打印今天两侧的完整列表,便于直接对照。
7. `info(...)` 落盘**两侧的有序列表**与**对称差**(`sorted(set(css_base) ^ set(py_items))`),并打印规则块起始行与常量定义行 —— 本项目的纪律是不给结论替代证据。
8. 同步模块 docstring 里 item 10 静态守卫的清单句(HEAD 实测 **L85**:「**静态契约计数**(`_idi07_focus_contract_guards`)**四条**:①…②…③…④…」):**四条 → 五条**,并补一句第 ⑤ 条的描述(两侧枚举逐项比对;失效模式是常量被收窄后普查判定集**静默缩水**而门仍绿)。docstring 与代码同提交。
9. **不要**改 `FOCUSABLE_SELECTOR` 的**值**(只在下面的变异证明里临时收窄,且必须还原);**不要**改 `_focusable_census_js()` / `_IDI06_CENSUS_JS` / `_IDI07_FOCUS_CENSUS_JS` / `_idi07_focus_rule_blocks` / `_idi07_block_declarations`;`item10()` 与 `item9()` 的调用序列**一字不动**;**不要**碰 `frontend/style.css` 的任何规则、声明或注释(本任务对 style.css **只读**)。
10. 顺带修 L1739 那句陈旧指认?**不要** —— 不在本任务范围(见上面归属判断的括号)。

**B. 提交与双向变异证明(本任务的核心交付,不可省)**
11. 先跑一次基线确认条数:`--item 10` == `PASS (41 条断言, 0 FAIL, 0 BLOCKED)`(计划期已实测)。
12. 加第 ⑤ 条与 docstring 同步后跑 `--item 10` == `PASS (42 条断言, 0 FAIL, 0 BLOCKED)`;并跑一次**无浏览器自证**(证明该断言确实不依赖浏览器):临时探针 `/tmp/idi-iin-260925/probe-fix5-nobrowser.py` —— 用 `importlib` 把 `scripts/check-05-ui-uat.py` 载入为模块(与 `scripts/check-06-idi05-validation.py` 的 `load_check05()` 同型),调用 `c05._idi07_focus_contract_guards("10")`,再从 `c05.ROWS` 取出本条(label 含「逐项」)的 `verdict`,exit 0 当且仅当 == `PASS`;**全程不启动服务器、不启浏览器**。(计划期已用同形探针实测:该函数在无浏览器下产出 8 行 item 10 记录;第 ⑤ 条加入后应为 9 行。)
13. **提交 5**(只含 `scripts/check-05-ui-uat.py`):
    `test(260925-iin): gate FOCUSABLE_SELECTOR against the :focus-visible enumeration (item 10)`
14. **变异 A(常量侧收窄一项):** 临时把 `FOCUSABLE_SELECTOR` 里的 `summary` 删掉,重跑
    - 无浏览器探针 ⇒ 本条 **FAIL**(exit 1);
    - `--item 10 --browser bundled` ⇒ **FAIL**(exit 1)。

    逐字记录该次输出(至少含本条 `FAIL` 行、其 expected/actual、item 10 的汇总与 exit code)。然后 `git checkout -- scripts/check-05-ui-uat.py`,确认 `git diff -- scripts/check-05-ui-uat.py` **为空**。
15. **变异 B(CSS 侧收窄一项):** 临时把 `frontend/style.css` 的 `:focus-visible` 枚举里 `summary:focus-visible,` 那一行删掉,重跑无浏览器探针与 `--item 10`,同样**逐字**记录 FAIL 输出;然后 `git checkout -- frontend/style.css`,确认 `git diff -- frontend/style.css` **为空**(本任务对 style.css 的净改动**必须是 0**)。
16. 两个变异都还原后,重跑 `--item 10` == `PASS (42 条断言, 0 FAIL, 0 BLOCKED)`、`--item 9` == `PASS (17 条断言, 0 FAIL, 0 BLOCKED)`(证明第 ⑤ 条对 item 9 零影响),并跑 `node --check frontend/app.js`。
17. 若变异 A 或 B 下本条仍 PASS,说明该门是空转的 —— **停下**修断言(常见成因:落成了集合比较而变异只换了顺序,或两侧其实读了同一个源),再重跑变异,直到它真的 FAIL。

**边界(仍然生效):** 不得重排 `frontend/style.css` 的任何规则;不得改 style.css 的任何规则(本任务只读);`!important` 声明数仍为 1;`.hidden` 计数仍为 1;零新增依赖。
  </action>
  <verify>
    <automated>
# ---- 目标条数(41 → 42:第 ⑤ 条无条件恰发 1 条)----
.venv/bin/python scripts/check-05-ui-uat.py --item 10 --browser bundled
#   期望:item 10: PASS (42 条断言,0 FAIL,0 BLOCKED);exit=0

# ---- 该断言不需要浏览器(静态,只读文件文本)----
.venv/bin/python /tmp/idi-iin-260925/probe-fix5-nobrowser.py
#   期望:exit 0;打印本条 verdict=PASS。全程不启服务器、不启浏览器。

# ---- 变异 A:常量侧收窄一项(临时删掉 `summary`)----
#   期望:探针 exit 1(本条 FAIL);--item 10 exit 1(汇总含 >=1 FAIL)
.venv/bin/python /tmp/idi-iin-260925/probe-fix5-nobrowser.py
.venv/bin/python scripts/check-05-ui-uat.py --item 10 --browser bundled
git checkout -- scripts/check-05-ui-uat.py
git diff -- scripts/check-05-ui-uat.py     # 期望:空

# ---- 变异 B:CSS 侧收窄一项(临时删掉 `summary:focus-visible,` 一行)----
.venv/bin/python /tmp/idi-iin-260925/probe-fix5-nobrowser.py
.venv/bin/python scripts/check-05-ui-uat.py --item 10 --browser bundled
git checkout -- frontend/style.css
git diff -- frontend/style.css             # 期望:空(FIX 5 对 style.css 的净改动 == 0)

# ---- 还原后回到绿,且 item 9 不受影响 ----
.venv/bin/python scripts/check-05-ui-uat.py --item 10 --browser bundled   # PASS (42 条断言)
.venv/bin/python scripts/check-05-ui-uat.py --item 9  --browser bundled   # PASS (17 条断言)
grep -n 'FOCUSABLE_SELECTOR = ' scripts/check-05-ui-uat.py                # 值仍是七项原文
grep -c '^\.hidden {' frontend/style.css                                  # 1
grep -o '!important;' frontend/style.css | wc -l                          # 1
node --check frontend/app.js                                              # OK
    </automated>
  </verify>
  <done>
- `_idi07_focus_contract_guards()` 内新增**恰一条**静态断言(item 10 的第 ⑤ 条),落点在 `_IDI07_DECLARED_AND_CONSUMED` 循环之后、`def _idi07_transition_motion_assert` 之前(用「下一个 `^def `」定位,不靠行号)。
- 该断言只读 `frontend/style.css` 的文件文本与 `FOCUSABLE_SELECTOR`,零 `page.*` 调用、零 `--ai-smoke` 依赖、零浏览器依赖(**无浏览器探针 exit 0 为证**)。
- 修好树:`--item 10` == `PASS (42 条断言, 0 FAIL, 0 BLOCKED)`;`--item 9` == `PASS (17 条断言, 0 FAIL, 0 BLOCKED)`。
- **变异 A(常量收窄一项)与变异 B(CSS 枚举删一项)下,本条都 FAIL** —— 两次输出的 FAIL 行、expected/actual、item 10 汇总与 exit code **逐字记录**在 SUMMARY(证明非空转,且**两个方向**都真的能失败)。
- 两个变异还原后 `git diff -- scripts/check-05-ui-uat.py` 与 `git diff -- frontend/style.css` **均为空**;`FOCUSABLE_SELECTOR` 的值与 style.css 的 `:focus-visible` 枚举**均与 HEAD 逐字相同**(FIX 5 对 style.css 净改动 == 0)。
- 模块 docstring 的 item 10 静态守卫清单句由「四条」改为「五条」并含第 ⑤ 条描述,与代码**同提交**。
- 硬规则 1/2 仍成立(`^\.hidden {` == 1;`!important;` == 1);`node --check frontend/app.js` == OK。
- 提交 5 只含 `scripts/check-05-ui-uat.py`。
  </done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 服务端 / AI 产出的 markdown → DOM | `renderEvent()` 对 `kind: 'say'` 走 `renderMarkdown()`(经 `stripUnsafeNodes` 过滤)。本计划**不改**这条链路:只在 `renderEvent` 已追加的节点上加一次 `scrollIntoView`,不新增任何解析、注入或 DOM sink |
| 服务端错误消息 → 内联错误节点 | `showInlineError` 的 `textContent`-only 规则是 XSS 缓解(T-260916-01),**不是风格选择**(硬规则 5)。五个修复都不碰它 —— FIX 4 改的是 check-05 里的一条 INFO 字符串,不是错误渲染路径 |
| 契约文档 → 后续执行者 | `idi-05-UI-SPEC.md` / `04-UI-SPEC.md` / `style.css` 的注释是后续计划的事实来源。陈旧或自相矛盾的散文会让下游执行者做出错误的「修正」(本任务 FIX 4 与 FIX 3 的注释同步都属这一面) |
| Python 常量 ↔ CSS 字面量(**无机制同步**) | `FOCUSABLE_SELECTOR`(check-05,L1748)与 `frontend/style.css` 的 `:focus-visible` 枚举(L1508)是同一份枚举的**两个手抄副本**:CSS 消费不了 Python 常量,反向也不行。两侧的「一致」今天只靠 `:1735-1747` 的注释承诺承担 —— 承诺不是门(FIX 5 的落点) |

本计划的输入面:**无新增输入处理、无新增网络面、无新增依赖、无新增 DOM sink**。仅一条 `scrollIntoView` 调用、两条 `:root` 令牌声明、一处规则值替换、一条注释字符串、三处契约散文与一条**只读文件文本**的静态断言。

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-260925-01 | Tampering (XSS) | `renderEvent()` 的 `kind: 'say'` 渲染路径 | low | accept | FIX 1 只在该函数**已 append 的节点**上加 `item.scrollIntoView({block:'nearest'})`;`renderMarkdown()` / `stripUnsafeNodes` / `textContent` 赋值路径一字未动,不引入 `innerHTML`、不新增 DOM sink。`block: 'nearest'` 是字面量参数,无用户输入进入该调用 |
| T-260925-02 | Tampering (XSS) | `showInlineError` 的 `textContent`-only 规则(T-260916-01) | low | accept | 硬规则 5 的禁改项。五个修复均不触碰错误渲染路径;FIX 4 只改 `item2()` 里一条 `info(...)` 字符串字面量,该函数的断言零改动(verify 以 `--item 2` 复核) |
| T-260925-03 | Repudiation | check-05 `item9()` 新增的自动跟随断言 | medium | mitigate | 一条**读起来覆盖了自动跟随、实际测的是显式滚动后可达**的断言,比没有断言更危险(本里程碑已出现三次同型弱点,见 audit §7)。缓解:断言经应用自身的 `renderEvent` 驱动、探针 JS 内零 `scrollTop` 赋值;反空转前提链(容器存在 / 可见 / 确实溢出 / 确有条目)不成立时记 `blocked()` 而非 PASS;**并强制变异证明** —— 中和 FIX 1 后该断言必须 FAIL,输出逐字记录;若中和后仍 PASS 则停下修断言 |
| T-260925-04 | Tampering | 契约散文与源码注释(加档后自相矛盾 / 被触碰的 do-not-touch 规则未留承认) | low | mitigate | 新增第 8 档会使 `style.css:1440-1442` 的数值序串与「数值阶梯下移一档」规则、以及 `idi-05-UI-SPEC.md` 的 7 档表与「刻度外第 6 个渲染字号」的表述变假;`idi-05-UI-SPEC.md:677` 的绝对禁令「`.collapse-indicator` 不得触碰」也会字面上变假。缓解:Task 3 同提交同步围栏注释、嵌入刻度注释、两份 UI-SPEC 的刻度表与 999.1 状态,**并把 `:677-679` 的禁令主体收窄为 `textContent` 赋值路径 + 登记唯一例外**(同时显式声明 FIX 3 只改该规则的两个值声明,故该禁令在实质上仍为真);`:555-556` / `:913` / `:1329-1330` 三处带时间限定的历史陈述**刻意保留**并记入 SUMMARY。显式写明嵌入档钉在已出货三对上、不重新推导 |
| T-260925-05 | Repudiation | check-05 `item10()` 的第 ⑤ 条静态枚举对齐断言(FIX 5) | medium | mitigate | 与 T-260925-03 同型:一条**读起来像在守「两侧枚举一致」、实际两侧都读了同一个源**的断言比没有断言更危险(本里程碑第三次)。缓解:反空转前提链(恰 1 个 `:focus-visible` 规则块 / 选择器项恰 7 个)不成立时记 `blocked()` 而非 PASS;**并强制双向变异证明** —— 常量收窄一项、CSS 删一项,两个方向都必须让本条 FAIL,输出逐字记录;若任一方向仍 PASS 则停下修断言 |
| T-260925-SC | Tampering | npm / pip / cargo 安装面 | low | accept | **本计划零新增依赖、零构建步骤**(D-06;硬规则 6)。无 install 面 ⇒ 包合法性门无适用对象,不设 `[ASSUMED]` / `[SUS]` 检查点。风险不适用,而非未缓解 |
</threat_model>

<verification>
**本计划的整体验收(五个提交全部落盘后,在 HEAD 上逐条跑):**

```bash
# 硬规则 1/2(注意 grep 算术陷阱:判据是声明数,不是命中行数)
grep -c '^\.hidden {' frontend/style.css            # 1
grep -o '!important;' frontend/style.css | wc -l    # 1

# 四条契约校验
bash scripts/check-01-token-conformance.sh          # PASS
.venv/bin/python scripts/check-02-contrast.py | tail -1   # PASS: 0 failures
bash scripts/check-03-hidden-uniqueness.sh          # PASS
bash scripts/check-04-important-count.sh            # PASS

# 浏览器门(必须 --browser bundled)
.venv/bin/python scripts/check-05-ui-uat.py --item 9  --browser bundled   # PASS (17 条断言, 0 FAIL, 0 BLOCKED)
.venv/bin/python scripts/check-05-ui-uat.py --item 10 --browser bundled   # PASS (42 条断言, 0 FAIL, 0 BLOCKED)
.venv/bin/python scripts/check-05-ui-uat.py --item 2  --browser bundled   # PASS(FIX 4 的断言未受影响)
.venv/bin/python scripts/check-05-ui-uat.py --item 7  --browser bundled   # PASS(嵌入刻度未受影响)

# FIX 5 的静态门在不启浏览器的前提下自证(与上面 --item 10 互补:后者证明集成,前者证明静态)
.venv/bin/python /tmp/idi-iin-260925/probe-fix5-nobrowser.py             # exit 0;本条 verdict=PASS

# FIX 5 的「两侧与 HEAD 逐字相同」净改动证据
grep -n 'FOCUSABLE_SELECTOR = ' scripts/check-05-ui-uat.py               # 值仍为七项原文
git diff --stat HEAD -- frontend/style.css                                # 空(FIX 5 对 style.css 净改动 == 0)

# 单元测试与语法(必须用项目 venv)
.venv/bin/python -m pytest -q                       # 219 passed, 6 skipped
node --check frontend/app.js                        # OK

# 工作树卫生
git status --porcelain frontend/                    # 只应有 frontend/app.js / frontend/style.css
ls frontend/vendor/                                 # 仍只有 marked.min.js(零新依赖)
git log --oneline -5                                # 五个修复各一个逻辑提交
```

**关于 FIX 3 的散文分类:** `idi-05-UI-SPEC.md` 的 `:677-679` 已按 §FIX 3 落地后会变假的散文 **就地收窄措辞**;`:555-556` / `:913` / `:1329-1330` 三处**刻意保留**为历史记录(带显式时间/阶段限定)。**刻意保留项没有对应的门** —— 它们由 SUMMARY 登记为决定,而不是由脚本断言。这是**记录在案**的覆盖缺口,不是疏漏。

**关于硬规则 3 / 4 的覆盖:** 两者**没有机械门**(`check-01` 只覆盖围栏标记 / 裸 hex / tier-1 泄漏)。本计划的编辑在结构上不可能引入规则块移动、`@layer` / `@property` / `var(--x, fallback)`(只换两个声明值、只在围栏内新增声明行、只改文件文本断言),故风险为零;该**人工核对**性质记录在 SUMMARY,不新造脚本。

**关于 check-05 全量跑:** 全量会 exit 2,因为 item 5 是**按设计** BLOCKED(两条 opt-in `--ai-smoke` 腿)—— 那是预期,不是回归,也不是本计划的验收判据。

**关于陈旧指纹:** `frontend/style.css` / `frontend/app.js` / `scripts/check-05-ui-uat.py` 的改动会按「内容真变」使 idi-04 / 04.1 / 05 / 06 / 07 / 08 的指纹 stale。**刻意保留**:不重跑那六个阶段的验证、不重算 `covered_digest`(刷新 digest 等于断言「验证之后什么都没变」,而这里是假的)。由里程碑收口统一处理。
</verification>

<success_criteria>
1. 用户在 `#ai-events` 追加事件时,工作面板**自动跟随**最新条目(应用自身路径驱动,浏览器实测 `#main-pane.scrollTop > 0` 且最新条目在可见盒内,harness 全程未设置 `scrollTop`)。
2. 该行为有一条**能失败**的门:check-05 `--item 9` 的新断言在 FIX 1 中和后变 FAIL、还原后 PASS,变异输出逐字留证。
3. `FOCUSABLE_SELECTOR` 与 `frontend/style.css` 的 `:focus-visible` 枚举**由一条静态门守住**(item 10 的第 ⑤ 条):常量收窄一项、或 CSS 枚举删一项,两个方向都让该门 FAIL;还原后两侧与 HEAD 逐字相同(style.css 净改动 0),item 10 断言数 41 → 42。
4. `.collapse-indicator` 的 `20px` 从裸字面量变为第 8 档令牌 `--text-lg-plus`,字形渲染尺寸**不变**(浏览器实读 computed 20px);该元素的 `textContent` 赋值路径与「不得内联 `<svg>`」一字未动,`idi-05-UI-SPEC.md:677` 在实质上仍为真(其措辞已就地收窄并登记唯一例外)。
5. 硬规则 1-7 全部仍成立,四条契约校验与三条浏览器门(`--item 9` / `--item 10` / `--item 2`)全绿,pytest 基线 219/6 不变。
6. 两份 UI-SPEC 的刻度表与 `.collapse-indicator` 状态不再陈旧(含 §已核实的偏差 的处置记录,以及 §FIX 3 落地后会变假的散文 的逐条分类:1 处收窄 + 3 处刻意保留)。
7. check-05 的 `--color-text-muted` 诊断串陈述真实值,断言零改动。
8. **五个**修复各自一个逻辑提交,全部在 `ui/baseline-and-tokens` 上。
</success_criteria>

<output>
Create `.planning/quick/260925-iin-v1-14-ai-999-1/260925-iin-SUMMARY.md` when done

SUMMARY 必须包含:
- **五个**提交的 hash 与 message
- FIX 1 的端到端探针原始读数(before / after / scrollHeight / clientHeight / 末条 rect / 容器盒)
- FIX 2 的**变异输出逐字记录**(中和 FIX 1 后新断言的 FAIL 行 + 汇总 + exit code),以及还原后 `git diff -- frontend/app.js` 为空的证据
- FIX 3 的浏览器 computed `font-size` 逐实例读数(两个 `.collapse-indicator`)与 `--text-*` / `--lh-*` 声明计数 7→8 / 4→5
- FIX 4 的 `8f8f8f` → `5.62:1` 计数证据与 `--item 2` 结论
- **FIX 5 的两次变异输出逐字记录**(变异 A:常量收窄一项;变异 B:CSS 枚举删一项 —— 各含本条的 FAIL 行 + expected/actual + item 10 汇总 + exit code),还原后两个 `git diff` 均为空的证据,以及无浏览器探针的 exit 0 输出;另记 item 10 断言数 41 → 42 的实测
- **Deviation 一节**:§已核实的偏差(brief 写名的 `04-UI-SPEC.md` 在 HEAD 上不含 7 档字号表、也不含 hard rule 9;实质同步落在 `idi-05-UI-SPEC.md`,`04-UI-SPEC.md` 只加指向行),以及 Task 3 对 `style.css:1440-1442` 嵌入刻度注释的同步(加档的直接后果)
- **散文分类一节(必须逐条记录,读起来是决定而不是疏漏):**
  - **刻意保留的陈旧陈述** —— `idi-05-UI-SPEC.md:913`(Gate 6 期望串,带「本阶段」限定)与 `:1329-1330`(2026-09-20 的日期基线);另加同类第三处 `:555-556`(`#ai-panel` 零 CSS 改动段,带「本阶段」限定)。三处均说明保留理由(显式时间/阶段限定 ⇒ 历史记录),并声明**刻意保留,非疏漏**。
  - **就地收窄的一处** —— `idi-05-UI-SPEC.md:677-679` 的段级禁令主体收窄为 `textContent` 赋值路径,并登记唯一例外;记录为何改(绝对禁令 + 登记行同提交更新导致的自相矛盾)。
  - **`.collapse-indicator` do-not-touch 调和** —— 明确记录:FIX 3 的改动面**逐字限定为该规则的两个值声明**(`font-size` / `line-height`),`app.js:1759` / `:1765` 的 `textContent` 赋值路径与「不得内联 `<svg>`」一字未动,故 `:677` **在实质上仍然为真**;以及为何仍要收窄其措辞。
  - **硬规则 3 / 4 的覆盖是人工核对,不是机械门** —— 记录 `check-01` 只覆盖围栏标记 / 裸 hex / tier-1 泄漏;本次编辑在结构上不可能引入规则块移动或 `@layer` / `@property` / `var(--x, fallback)`,故**记录该缺口**而不新造脚本。
- 门基线对照表(逐条命令 + 改动后实测值,含 `--item 9` = 17 与 `--item 10` = 42)
- 指纹影响声明:六个阶段的 stale 指纹**刻意保留**,未重算 digest
</output>

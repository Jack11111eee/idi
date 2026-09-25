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
  - CHECK-03
  - CHECK-04
user_setup: []

estimate:
  tokens: 60000
  raw_tokens: 60000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "自动跟随恢复:在浏览器里经**应用自身的** `renderEvent` 追加事件后,`#main-pane.scrollTop > 0`,且最新一条 `.event-item` 的 rect 完全落在 `#main-pane` 的可见盒内 —— 全程 harness 未设置过任何 `scrollTop`(FIX 1)"
    - "新增的门**能失败**:把 FIX 1 中和掉(移除 `item.scrollIntoView` 那一行)后,check-05 `--item 9` 的新断言变 FAIL 且 exit 1;还原后回到 PASS —— 变异输出逐字记录(FIX 2)"
    - "`.collapse-indicator` 在浏览器里的 computed `font-size` 仍为 `20px`(字形渲染尺寸不变),但围栏外不再有裸字号/行高字面量:该规则消费 `--text-lg-plus` 与 `--lh-none`(FIX 3)"
    - "`:root` 围栏内多两条声明(`--text-lg-plus: 20px` / `--lh-none: 1`),各恰有一个消费者且同提交(Hard Rule 5);围栏注释记录了「第 8 档、值序位于 18 与 22 之间、命名阶梯非单调依据 D-07」(FIX 3)"
    - "硬规则 1/2 仍成立:`grep -c '^\\.hidden {' frontend/style.css` == 1;`!important` **声明**数 == 1(注意 `grep -c '!important'` 返回 5 是注释散文陷阱,判据是 `grep -o '!important;' | wc -l`)"
    - "`scripts/check-05-ui-uat.py` 的 blockquote 诊断串陈述真实值(`#646464` / 5.62:1 达标),该函数周围的断言零改动(FIX 4)"
    - "全套门在改动后仍为绿:check-01 / check-02 / check-03 / check-04 / `--item 9` / `--item 10` / `pytest 219 passed, 6 skipped` / `node --check frontend/app.js`"
  artifacts:
    - "frontend/app.js 的 `renderEvent()` 内为 `item.scrollIntoView({ block: 'nearest' })`,原 `eventsEl.scrollTop = eventsEl.scrollHeight;` 那条 no-op 已删除(该串在 app.js 内计数 1 → 0)"
    - "scripts/check-05-ui-uat.py 的 `item9()` 内新增一条判定「自动跟随」的断言(置于 40 条 `renderEvent` 注入块**之前**,因为 `_idi06_reach` 自己会设 `scrollTop`)"
    - "frontend/style.css 围栏内 `--text-lg-plus: 20px;`(紧接 `--text-lg: 18px;`)与 `--lh-none: 1;`(紧接 `--lh-reading: 1.625;`);`.collapse-indicator` 规则改为消费二者"
    - "字号刻度表 7 档 → 8 档的契约同步落盘(见 §已核实的偏差:实际承载该表的文件是 `idi-05-UI-SPEC.md`,不是 brief 写名的 `04-UI-SPEC.md`)"
    - "scripts/check-05-ui-uat.py 第 824 行的陈旧诊断串已订正为 5.62:1 达标"
  key_links:
    - "`renderEvent()` 的 `eventsEl.appendChild(item)` → `item.scrollIntoView({block:'nearest'})` → 外层滚动者 `#main-pane` 跟随 → 最新条目在可见盒内(修复的因果链)"
    - "check-05 `item9()` 的新断言 ← 驱动应用自身的 `renderEvent`(**不合成 DOM、不依赖 `--ai-smoke`**);变异(FIX 1 中和)必须让它 FAIL,否则该门与本任务要修的空转门同型"
    - "`.collapse-indicator` 的 `font-size` 声明 → `--text-lg-plus`(20px)→ 字形渲染尺寸不变(浏览器实读 computed,不靠 grep)"
    - "frontend/style.css / frontend/app.js / scripts/check-05-ui-uat.py 改动 ⇒ 六个阶段(idi-04 / 04.1 / 05 / 06 / 07 / 08)的指纹按「内容真变」stale —— **刻意保留**,本任务不重算 `covered_digest`、不重跑那六个阶段的验证"
---

<objective>
v1.14 收口前的四修一票:恢复 AI 事件自动跟随、补一条**真能失败**的门、处置 backlog `999.1` 的两项。

**FIX 1(最重要)** —— `frontend/style.css` 的 `.event-list` 规则**就是** `#ai-events`(`frontend/index.html:76`;`frontend/app.js:5` 绑定 `const eventsEl = document.getElementById('ai-events')`)。Phase 6 的 L-4 收敛(`6adcaa3`,idi-06-02)**原地删掉**了该规则的 `max-height: 55vh` 与 `overflow-y: auto`,于是它计算为 `overflow-y: visible`、**不再是滚动容器** ⇒ `frontend/app.js:253` 的 `eventsEl.scrollTop = eventsEl.scrollHeight`(注释「保持最新可见」)按 CSS 规范**恒为空操作**(不可滚元素的 `scrollTop` 永远是 0)。`app.js` 另外三处 `scrollTop` 写入(`:270` / `:293` / `:299`)全部作用于 `chatMessages`,没有任何代码滚 `#main-pane`。基线 `0c658aa` 上自动跟随**是好用的** ⇒ 这是 v1.14 引入的**回归**,不是既有毛病。修法是让**刚追加的条目**在外层滚动容器里可见 —— **不恢复内滚动**(那会回退 L-4 并打破 check-05 `--item 9` 的滚动者普查,它断言面板区滚动者集合**恰好**是 `{#main-pane, #chat-messages, #latest-check}`)。

**FIX 2** —— check-05 `--item 9` 对此的覆盖是零,且比零更糟:它**正面断言了回归的前提**(`#ai-events 计算 max-height == none  # L-4:套娃第一层(55vh 限高 + 内滚动)已原地删除`),并把滚动者集合钉死在那一组上;它唯一涉及滚动的断言是「末条内容可达」,而那条**自己先设** `c.scrollTop = scrollHeight`(`scripts/check-05-ui-uat.py:2483`)再读 rect —— 那是「显式滚动后可到达」,与「自动跟随」是两个不同性质。新增的断言其**判定性质必须是自动跟随**,且必须**变异证明非空转**。

**FIX 3** —— `.collapse-indicator`(`frontend/style.css:678`)是 `font-size: 20px; line-height: 1;` 两个围栏外裸字面量,属已令牌化的 `--text-*` / `--lh-*` 族,且在 `04-UI-SPEC.md:841` 的封闭例外清单(L-1…L-5)之外。用户已拍定:**加一档字号,保持字形渲染尺寸不变**(不重映射到 18px、不加 L-6 例外)。

**FIX 4** —— `scripts/check-05-ui-uat.py:824` 的 INFO 串陈述在 HEAD 上是反的:该陈述称 `--color-text-muted` 变为 `#8f8f8f`、低于 AA;实测 `--color-text-muted: var(--radix-gray-11)`、`--radix-gray-11: #646464`(= rgb(100,100,100)),在 `--color-surface` 上 **5.62:1**、在 `--color-surface-page` 上 **5.77:1**,两者均达标;`scripts/check-02-contrast.py` 报 `PASS: 0 failures`。**只改那条 INFO / 散文串,不得改动任何断言。**

Purpose: 审计(`.planning/v1.14-MILESTONE-AUDIT.md` §5)判 `gaps_found`,唯一的阻断项是 Phase 6 的 L-4 改动引入的**零门覆盖**跨阶段回归 —— 它破坏的是「看 AI 干活」这条核心流程。同时把 backlog `999.1` 的两项一并收口,并把「标签读起来像覆盖了某行为、实际没测」这一**在本里程碑已出现三次**的门弱点,用一条带变异证明的断言补上一次。

Output:
- `frontend/app.js`:一条 `scrollIntoView`(提交 1)
- `scripts/check-05-ui-uat.py`:`item9()` 新增自动跟随断言 + 变异证明记录(提交 2)
- `frontend/style.css`:`--text-lg-plus` / `--lh-none` 两档声明 + `.collapse-indicator` 规则改写 + 围栏注释同步;两份 UI-SPEC 的刻度表同步(提交 3)
- `scripts/check-05-ui-uat.py:824` 陈旧诊断串订正(提交 4)
- **四个修复各自一个逻辑提交**,全部留在分支 `ui/baseline-and-tokens`
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

## 锚点已在 HEAD `bc563d7` 上逐一复核(计划期实测)

| 锚点 | HEAD 实测 |
|---|---|
| `frontend/app.js:233` | `function renderEvent(event) {` |
| `frontend/app.js:252-253` | `eventsEl.appendChild(item);` / `eventsEl.scrollTop = eventsEl.scrollHeight; // 保持最新可见` |
| `frontend/app.js:1759` / `:1765` | `panelHeader.querySelector('.collapse-indicator').textContent = collapsed ? '▸' : '▾';`(同形两处,`#doc-panel-header`) |
| `frontend/style.css:678` | `.collapse-indicator { font-size: 20px; line-height: 1; }` |
| `frontend/style.css:312-317` | 字号刻度围栏注释(`7 sizes` / 「七档依次为 …」) |
| `frontend/style.css:319-325` | `--text-xs: 12px;` … `--text-lg: 18px;`(322)/ `--text-xl: 24px;` / `--text-2xl: 22px;` / `--text-3xl: 28px;` |
| `frontend/style.css:333-342` | 行高围栏注释(「四条声明」)/ `--lh-tight` … `--lh-reading: 1.625;`(342) |
| `frontend/style.css:1440-1442` | 嵌入刻度注释里的「契约阶梯的数值序是 12 / 14 / 16 / 18 / 22 / 24 / 28」(**加档后会变陈旧,见 Task 3**) |
| `frontend/style.css:748-758` | `.event-list` 规则体(已无 `max-height` / `overflow-y`) |
| `scripts/check-05-ui-uat.py:824` | 陈旧诊断串(`#8f8f8f,低于 AA 4.5:1`) |
| `scripts/check-05-ui-uat.py:785` | `def item2(page, tmp_root):` —— **824 行所在项是 item 2** |
| `scripts/check-05-ui-uat.py:2483` | `_IDI06_REACH_JS` 内 `c.scrollTop = scrollHeight;`(故新断言必须排在它**之前**) |
| `scripts/check-05-ui-uat.py:2725` | `_latest_check_max_height_guard(item)`(新断言插在它之后) |
| `scripts/check-05-ui-uat.py:2731-2741` | 现有的 40 条 `renderEvent` 注入块 |
| `scripts/check-05-ui-uat.py:2742` | `_idi06_reach(page, item, "#main-pane", "p1", grown, …)` |
| 基线计数 | `^\.hidden {` == **1**;`!important;` == **1**(`grep -c '!important'` == 5 是注释散文);`--text-*` 声明 **7** 条;`--lh-*` 声明 **4** 条;check-01 / check-03 / check-04 == PASS;`node --check frontend/app.js` == OK |

## 已核实的偏差(与 brief 不一致,须记入 SUMMARY,不自行扩大范围)

brief 的 FIX 3 末条写「更新 `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md`:字号刻度表(7 档 → 8 档)与其 "hard rule 9" 引用」。**该描述在 HEAD 上不成立:**

- `04-UI-SPEC.md` 的 `## Typography`(L315-348)是 **Phase 4 的 6 档历史表**(`11 / 12 / 13 / 14 / 15 / 16`),其值已被 `idi-04.1-radix` 的 Radix 重写与 Phase 5 推翻(文件 mtime 2026-09-17,此后零改动)。
- `04-UI-SPEC.md` 的 `## Global Hard Rules`(L942)只有 **1-7 条**,**没有第 9 条**。
- **7 档字号刻度表**在 `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §Typography(L164-181),该节自述「本文件重写 `04-UI-SPEC.md` 的同名节(5 档 → 7 档)」;**hard rule 9** 也在同一文件(L1032);该文件 L365-380 的「未在 HEAD 上受控的字号」一节**正是**点名 `.collapse-indicator` 的 `20px`「是刻度外的第 6 个渲染字号,属 backlog `999.1`」的地方 —— FIX 3 落地后这句会变假。
- `04-UI-SPEC.md` **确实**在 `idi-04-VERIFICATION.md` 的 `covered_files` 内(brief 的这一句为真),且 `idi-04-VERIFICATION.md:80` 把 `04-UI-SPEC.md:841` §Literal exceptions 列为 `.collapse-indicator` 的**替代修法**(用户已否决该替代,故选令牌路线、不动 L-1…L-5 清单)。

**处置:** 承载「刻度表 7 → 8 档 + hard rule 9 引用」的文件是 `idi-05-UI-SPEC.md`,Task 3 在那里做实质同步;`04-UI-SPEC.md` 只加一条**如实的**「本节已被重写 / 现行刻度为 8 档」指向行(**不改那张 6 档表本身**),以满足 brief 写名的文件。两处都记入 SUMMARY 的 Deviation 一节。

## 仍然生效的硬规则(源:`.planning/ROADMAP.md` §全局硬规则)

1. `grep -c '^\.hidden {' frontend/style.css` 必须**仍为 1**。
2. `!important` **声明**数必须**仍为 1**(按声明计数,不要数命中行)。
3. **追加,不重排** —— 任何**规则块**不得移动。`:root` 围栏内**新增声明行**不算重排(它不是选择器块,且计划期已核:改后 diff 的「选择器前移」数仍为 0)。
4. 不得新增 `!important`;不得令牌化 `display`;不得引入 `@layer` / `@property` / `var(--x, fallback)`。
5. **不得触碰:** `.fatal` 修饰符;`applyArchiveView` 的两行只读行;`#selection-menu` 的 DOM 位置(必须仍是 `<body>` 直接子元素);`showInlineError` 的 `textContent`-only 规则(XSS 缓解 T-260916-01,不是风格选择);`renderAnnotations` / `renderVerdictCard`;`app.js:4-75` 约 70 个顶层 `getElementById` 句柄(id 不得改名或删除);`.collapse-indicator` 的 `textContent` 赋值路径(`app.js:1759` / `:1765` —— **不得**引入内联 `<svg>`)。
6. 零新增运行时依赖、零构建步骤。

## 门基线(全部已在修复前 HEAD `bc563d7` 上实测为绿 —— 任何回归即 FAIL)

| 命令 | 基线 |
|---|---|
| `bash scripts/check-01-token-conformance.sh` | PASS |
| `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`(53 PASS + 1 ORDER) |
| `bash scripts/check-03-hidden-uniqueness.sh` | PASS |
| `bash scripts/check-04-important-count.sh` | PASS |
| `.venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled` | `PASS (16 断言, 0 FAIL, 0 BLOCKED)` → 本任务后应为 **17 条** |
| `.venv/bin/python scripts/check-05-ui-uat.py --item 10 --browser bundled` | `PASS (41 断言, 0 FAIL, 0 BLOCKED)` |
| `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped` |
| `node --check frontend/app.js` | OK |

- **必须**用项目 venv `.venv/bin/python` —— 环境 `python3` 是 miniconda,会造出 4 个 `ai_caller` 假失败。
- check-05 **必须**加 `--browser bundled`(`.venv` 路线必须用捆绑 chromium;`channel` + `headless` 在本机会挂死)。
- check-05 **全量**跑会 exit 2,因为 item 5 是**按设计** BLOCKED(两条 opt-in `--ai-smoke` 腿)—— 那是预期,不是回归。本计划**不依赖** `--ai-smoke`。

## 明确不要做的事

- **不要**碰 `.claude/settings.local.json`(其 `Bash(node -e ' *)` 授权是业主已接受的信任边界决定)。
- **不要**提交 `.planning/.idi07-dec*.txt`(未跟踪的临时文件)或 `.planning/v1.14-MILESTONE-AUDIT.md`。
- **不要**重新验证本任务作废指纹的那六个阶段(idi-04 / 04.1 / 05 / 06 / 07 / 08),**不要**重算它们的 `covered_digest`。刷新 digest 等于断言「验证之后什么都没变」,而这里是假的。陈旧性**刻意保留**为可见信号,由里程碑收口统一处理。
- **不要**顺手修别的陈旧散文(例如 `ROADMAP.md` 硬规则 3 的具名源码序例子、`style.css:1498-1502` 的围栏注释)—— 那是已登记的 tech debt,不在本任务范围。
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
1. 落点:`item9()`(`scripts/check-05-ui-uat.py:2677`)内,紧接 `_latest_check_max_height_guard(item)`(现第 2725 行)**之后**、现有 40 条 `renderEvent` 注入块(现 2731-2741 行)**之前**。
   - **必须排在 `_idi06_reach(...)`(现 2742 行)之前** —— `_idi06_reach` 内部经 `_IDI06_REACH_JS` 自己设 `c.scrollTop = scrollHeight`(`:2483`),会把「harness 从未滚过」这个前提毁掉,新断言排在它后面就恒绿。
2. 探针用一次 `page.evaluate` 完成「读 before → 经应用自身的 `renderEvent` 追加 N 条 → 读 after 与几何」,该 JS **不得出现任何 `scrollTop` 赋值**(这是「harness 自己从未设置过 `scrollTop`」的可核形态;把这一点写进断言旁的注释)。
   - 必须驱动**应用自己的** `renderEvent`(SSE handler 调用的同一个函数),**不得**合成 DOM、不得直接 `appendChild`。`kind` 取 `'say'`(对 `done` / `error`,`renderEvent` 会解除「发起」按钮禁用,污染后续项)。
   - **不得**依赖 `--ai-smoke`(那两条腿需要活的 CLI 调用且是 opt-in)。
3. 判据:追加后 `#main-pane.scrollTop > 0`(**且** before == 0),**且**最后一条 `.event-item` 的 rect 完全落在 `#main-pane` 的可见盒内。
4. **反空转前提(任一不成立记 `blocked(...)`,绝不记 PASS —— 与 `_idi06_reach` 的前提链同型,威胁表 T-idi-06-10 的落点):** `#main-pane` 存在;`rect.height > 0` 且 `display != 'none'`;注入后 `scrollHeight > clientHeight`(否则性质平凡成立);注入后 `#ai-events .event-item` 计数 > 0;`renderEvent` 可用。
5. 断言文案要让「这条门测的是什么」一目了然,并在 note 里点明与既有「末条内容可达」的区别:后者是**显式滚动后**的可达性,本条是**应用自动跟随**。同时用 `info(...)` 逐行落盘原始读数(before / after / scrollHeight / clientHeight / 末条 rect / 容器盒)—— 本项目的纪律是不给结论替代证据。
6. 复用既有的 `ok_true(...)` / `blocked(...)` / `info(...)` 助手与 item 9 的既有标签风格;**不要**改 `_idi06_reach`、`_IDI06_REACH_JS`、滚动者普查、或 item 9 的任何既有断言(那条普查断言 `#ai-events 计算 max-height == none` 是 L-4 的正确断言,只是对自动跟随零覆盖 —— 保留它,补它)。

**B. 变异证明(本任务的核心交付,不可省)**
7. 先跑一次基线,确认新断言 PASS 且断言总数为 **17**(基线 16 + 1)。
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
#   基线 16 条 ⇒ 新增恰 1 条。条数不是 17 即为偏差,先查清再提交。

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

**D. 契约文档同步(刻度表 7 → 8 档 + hard rule 9 引用)**
7. **主要承载文件是 `idi-05-UI-SPEC.md`**(见 §已核实的偏差):
   - §Typography 的 §最终字号阶梯(L164-181):表由 **7 档 → 8 档**,加入 `--text-lg-plus` 20px 一行,并注明它位于 `--text-lg`(18)与 `--text-2xl`(22)之间、命名阶梯非单调依据 D-07;该节标题的「**7 档。**」改为 8 档。
   - §未在 HEAD 上受控的字号(L365-380):`.collapse-indicator` 的 `20px` 已**不再是刻度外字号**,改为登记「已由 quick `260925-iin` 落为第 8 档 `--text-lg-plus`,backlog `999.1` 第 1 项关闭」;同段的 `#confirm-error` 16px 一条**仍然存在**,不要顺手改它。
   - Do-Not-Touch List 里 `.collapse-indicator` 那一行(L1043 附近):把「本阶段零改动 / 属 backlog `999.1`」更新为「已由 quick `260925-iin` 令牌化(值不变,仍 20px);`textContent` 赋值路径仍不得触碰」。
   - hard rule 9 的**引用**处:该文件 `## Global Hard Rules` 第 9 条本身讲的是「不得写全局标题规则 + 渲染目标逐个列举」,**与本改动无冲突,不要改写其正文**;只在紧邻处(或其所在清单的说明行)加一句**引用登记**:本次新增的令牌只被 `.collapse-indicator` 消费,未新增任何标题字号规则,故第 9 条不受影响 —— 这正是 brief 要求的「hard rule 9 引用」同步。
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
bash scripts/check-01-token-conformance.sh          # PASS
bash scripts/check-03-hidden-uniqueness.sh          # PASS
bash scripts/check-04-important-count.sh            # PASS
.venv/bin/python scripts/check-02-contrast.py | tail -1   # PASS: 0 failures
node --check frontend/app.js                        # OK

# ---- FIX 3:契约文档 ----
grep -c '8 档\|八档' .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md   # >= 1
grep -n -- '--text-lg-plus' .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md  # 刻度表新行
grep -n -- '--text-lg-plus' .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md               # 指向行
grep -n '999.1' .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md       # 该节已改写为「已关闭」

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
- 围栏注释记录了第 8 档、值序位于 18 与 22 之间、命名阶梯非单调依据 D-07;行高注释记录了 `--lh-none` 的 glyph-only 性质与唯一消费者;嵌入刻度注释的数值序与「钉在已出货三对」的说明已同步。
- 硬规则 1/2 仍成立(`^\.hidden {` == 1;`!important;` == 1);check-01/02/03/04 全 PASS;`node --check` OK。
- 两份 UI-SPEC 已按 §已核实的偏差 处置:`idi-05-UI-SPEC.md` 承载实质同步(7 → 8 档 + 999.1 关闭 + hard rule 9 引用登记),`04-UI-SPEC.md` 加如实的指向行(6 档历史表与 L-1…L-5 清单**未改**)。
- `scripts/check-05-ui-uat.py` 中 `8f8f8f` 计数 0、`5.62:1` 计数 1;`--item 2` PASS;`item2()` 的断言零改动(`git diff` 只显示那一行字符串)。
- 提交 3、提交 4 各自只含上述文件。
  </done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 服务端 / AI 产出的 markdown → DOM | `renderEvent()` 对 `kind: 'say'` 走 `renderMarkdown()`(经 `stripUnsafeNodes` 过滤)。本计划**不改**这条链路:只在 `renderEvent` 已追加的节点上加一次 `scrollIntoView`,不新增任何解析、注入或 DOM sink |
| 服务端错误消息 → 内联错误节点 | `showInlineError` 的 `textContent`-only 规则是 XSS 缓解(T-260916-01),**不是风格选择**(硬规则 5)。四个修复都不碰它 —— FIX 4 改的是 check-05 里的一条 INFO 字符串,不是错误渲染路径 |
| 契约文档 → 后续执行者 | `idi-05-UI-SPEC.md` / `04-UI-SPEC.md` / `style.css` 的注释是后续计划的事实来源。陈旧或自相矛盾的散文会让下游执行者做出错误的「修正」(本任务 FIX 4 与 FIX 3 的注释同步都属这一面) |

本计划的输入面:**无新增输入处理、无新增网络面、无新增依赖、无新增 DOM sink**。仅一条 `scrollIntoView` 调用、两条 `:root` 令牌声明、一处规则值替换、一条注释字符串与三处契约散文。

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-260925-01 | Tampering (XSS) | `renderEvent()` 的 `kind: 'say'` 渲染路径 | low | accept | FIX 1 只在该函数**已 append 的节点**上加 `item.scrollIntoView({block:'nearest'})`;`renderMarkdown()` / `stripUnsafeNodes` / `textContent` 赋值路径一字未动,不引入 `innerHTML`、不新增 DOM sink。`block: 'nearest'` 是字面量参数,无用户输入进入该调用 |
| T-260925-02 | Tampering (XSS) | `showInlineError` 的 `textContent`-only 规则(T-260916-01) | low | accept | 硬规则 5 的禁改项。四个修复均不触碰错误渲染路径;FIX 4 只改 `item2()` 里一条 `info(...)` 字符串字面量,该函数的断言零改动(verify 以 `--item 2` 复核) |
| T-260925-03 | Repudiation | check-05 `item9()` 新增的自动跟随断言 | medium | mitigate | 一条**读起来覆盖了自动跟随、实际测的是显式滚动后可达**的断言,比没有断言更危险(本里程碑已出现三次同型弱点,见 audit §7)。缓解:断言经应用自身的 `renderEvent` 驱动、探针 JS 内零 `scrollTop` 赋值;反空转前提链(容器存在 / 可见 / 确实溢出 / 确有条目)不成立时记 `blocked()` 而非 PASS;**并强制变异证明** —— 中和 FIX 1 后该断言必须 FAIL,输出逐字记录;若中和后仍 PASS 则停下修断言 |
| T-260925-04 | Tampering | 契约散文与源码注释(加档后自相矛盾) | low | mitigate | 新增第 8 档会使 `style.css:1440-1442` 的数值序串与「数值阶梯下移一档」规则、以及 `idi-05-UI-SPEC.md` 的 7 档表与「刻度外第 6 个渲染字号」的表述变假。缓解:Task 3 同提交同步围栏注释、嵌入刻度注释、两份 UI-SPEC 的刻度表与 999.1 状态;并显式写明嵌入档钉在已出货三对上、不重新推导 |
| T-260925-SC | Tampering | npm / pip / cargo 安装面 | low | accept | **本计划零新增依赖、零构建步骤**(D-06;硬规则 6)。无 install 面 ⇒ 包合法性门无适用对象,不设 `[ASSUMED]` / `[SUS]` 检查点。风险不适用,而非未缓解 |
</threat_model>

<verification>
**本计划的整体验收(四个提交全部落盘后,在 HEAD 上逐条跑):**

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
.venv/bin/python scripts/check-05-ui-uat.py --item 10 --browser bundled   # PASS (41 条断言, 0 FAIL, 0 BLOCKED)
.venv/bin/python scripts/check-05-ui-uat.py --item 2  --browser bundled   # PASS(FIX 4 的断言未受影响)
.venv/bin/python scripts/check-05-ui-uat.py --item 7  --browser bundled   # PASS(嵌入刻度未受影响)

# 单元测试与语法(必须用项目 venv)
.venv/bin/python -m pytest -q                       # 219 passed, 6 skipped
node --check frontend/app.js                        # OK

# 工作树卫生
git status --porcelain frontend/                    # 只应有 frontend/app.js / frontend/style.css
ls frontend/vendor/                                 # 仍只有 marked.min.js(零新依赖)
git log --oneline -4                                # 四个修复各一个逻辑提交
```

**关于 check-05 全量跑:** 全量会 exit 2,因为 item 5 是**按设计** BLOCKED(两条 opt-in `--ai-smoke` 腿)—— 那是预期,不是回归,也不是本计划的验收判据。

**关于陈旧指纹:** `frontend/style.css` / `frontend/app.js` / `scripts/check-05-ui-uat.py` 的改动会按「内容真变」使 idi-04 / 04.1 / 05 / 06 / 07 / 08 的指纹 stale。**刻意保留**:不重跑那六个阶段的验证、不重算 `covered_digest`(刷新 digest 等于断言「验证之后什么都没变」,而这里是假的)。由里程碑收口统一处理。
</verification>

<success_criteria>
1. 用户在 `#ai-events` 追加事件时,工作面板**自动跟随**最新条目(应用自身路径驱动,浏览器实测 `#main-pane.scrollTop > 0` 且最新条目在可见盒内,harness 全程未设置 `scrollTop`)。
2. 该行为有一条**能失败**的门:check-05 `--item 9` 的新断言在 FIX 1 中和后变 FAIL、还原后 PASS,变异输出逐字留证。
3. `.collapse-indicator` 的 `20px` 从裸字面量变为第 8 档令牌 `--text-lg-plus`,字形渲染尺寸**不变**(浏览器实读 computed 20px)。
4. 硬规则 1-7 全部仍成立,四条契约校验与两条浏览器门全绿,pytest 基线 219/6 不变。
5. 两份 UI-SPEC 的刻度表与 `.collapse-indicator` 状态不再陈旧(含 §已核实的偏差 的处置记录)。
6. check-05 的 `--color-text-muted` 诊断串陈述真实值,断言零改动。
7. 四个修复各自一个逻辑提交,全部在 `ui/baseline-and-tokens` 上。
</success_criteria>

<output>
Create `.planning/quick/260925-iin-v1-14-ai-999-1/260925-iin-SUMMARY.md` when done

SUMMARY 必须包含:
- 四个提交的 hash 与 message
- FIX 1 的端到端探针原始读数(before / after / scrollHeight / clientHeight / 末条 rect / 容器盒)
- FIX 2 的**变异输出逐字记录**(中和 FIX 1 后新断言的 FAIL 行 + 汇总 + exit code),以及还原后 `git diff -- frontend/app.js` 为空的证据
- FIX 3 的浏览器 computed `font-size` 逐实例读数(两个 `.collapse-indicator`)与 `--text-*` / `--lh-*` 声明计数 7→8 / 4→5
- FIX 4 的 `8f8f8f` → `5.62:1` 计数证据与 `--item 2` 结论
- **Deviation 一节**:§已核实的偏差(brief 写名的 `04-UI-SPEC.md` 在 HEAD 上不含 7 档字号表、也不含 hard rule 9;实质同步落在 `idi-05-UI-SPEC.md`,`04-UI-SPEC.md` 只加指向行),以及 Task 3 对 `style.css:1440-1442` 嵌入刻度注释的同步(加档的直接后果)
- 门基线对照表(逐条命令 + 改动后实测值)
- 指纹影响声明:六个阶段的 stale 指纹**刻意保留**,未重算 digest
</output>

# 260925-iin — v1.14 收口前修复(五修一票)

**Background:** `.planning/v1.14-MILESTONE-AUDIT.md` 判 `gaps_found`:审计发现 Phase 6 的 L-4
改动引入了一个**零门覆盖**的跨阶段回归。本任务把它连同 backlog `999.1` 的两项一并收口,
并补上第三处同类门弱点(FIX 5)。
**五个决策均已由用户拍定,不得重开。**

**Branch:** 留在 `ui/baseline-and-tokens`(与 `260916-t8g` / `260917-fqh` / `260918-qrq` /
`260924-vb7` 的先例一致)。`workflow.use_worktrees=false`,顺序执行,无 worktree。

---

## FIX 1(最重要)—— 恢复 AI 事件自动跟随

**事实(已核,勿重复调查):**
- `frontend/style.css` 的 `.event-list` 规则**就是** `#ai-events`(`frontend/index.html:76`;
  `frontend/app.js:5` 绑定 `const eventsEl = document.getElementById('ai-events')`)。
- Phase 6 的 L-4 收敛(`6adcaa3`,idi-06-02)**原地删掉**了该规则的 `max-height: 55vh` 与
  `overflow-y: auto`。没有 overflow 声明 ⇒ 计算值 `overflow-y: visible` ⇒ **不再是滚动容器**
  ⇒ `frontend/app.js:253` 的 `eventsEl.scrollTop = eventsEl.scrollHeight; // 保持最新可见`
  按 CSS 规范**恒为空操作**(不可滚元素的 `scrollTop` 永远是 0)。
- **没有东西接手**:`app.js` 里另外三处 `scrollTop` 写入是 `:270` / `:293` / `:299`,全部作用于
  `chatMessages`(另一个元素)。没有任何代码滚 `#main-pane`。
- 基线 `0c658aa` 上该规则带 `max-height: 55vh; overflow-y: auto`,自动跟随**当时是好用的**
  ⇒ 这是 v1.14 引入的**回归**,不是既有毛病。

**修法(绑定):**
- **不得**恢复内滚动(那会回退 L-4,并打破 check-05 `--item 9` 的滚动者普查 —— 它断言面板区
  滚动者集合**恰好**是 `{#main-pane, #chat-messages, #latest-check}`)。
- 改为让**刚追加的条目**在外层滚动容器里可见。旧行为「列表底边与容器底边齐平」的忠实等价物是
  把刚追加的节点滚入 `#main-pane` 视野。预期形态:`item.scrollIntoView({ block: 'nearest' })`,
  放在 `app.js:253` 现在所在的位置。
- **保持最小**:不要加「仅当用户已在底部附近才跟随」之类的启发式 —— 那是超出修复范围的复杂度。

## FIX 2 —— 补一条**真能失败**的门

check-05 `--item 9` 对此的覆盖是零,而且比零更糟:它**正面断言了回归的前提**
(`#ai-events 计算 max-height == none  # L-4:套娃第一层(55vh 限高 + 内滚动)已原地删除`),
并把滚动者集合钉死在那一组上。它唯一涉及滚动的断言是「末条内容可达」,而那条**自己先设**
`c.scrollTop = scrollHeight`(`scripts/check-05-ui-uat.py:2483`)再读 rect —— 那是
「显式滚动后可到达」,与「自动跟随」是两个不同性质。

**要求(绑定):**
- 新增一条断言,其**判定性质是自动跟随**:驱动**应用自己的** `renderEvent` 路径
  (`app.js` 里 SSE handler 调用的**同一个函数**,不得合成 DOM)追加 N 个事件,然后断言
  **最新条目落在 `#main-pane` 的可见盒内,且 harness 自己从未设置过 `scrollTop`**。
- **必须证明非空转**:把 FIX 1 中和掉,展示该断言变 **FAIL**,并**逐字记录**变异输出。
- **不得**依赖 `--ai-smoke`(那两条腿需要活的 CLI 调用、且是 opt-in)。

## FIX 3 —— 处置 `.collapse-indicator` 的两个字面量(backlog 999.1 第 1 项)

**用户决策:加一档字号,保持字形渲染尺寸不变。不得替换为别的修法形态**
(不要重映射到 18px,不要加 L-6 例外)。

HEAD 现状(`frontend/style.css:678`):`.collapse-indicator { font-size: 20px; line-height: 1; }`
—— 围栏外两个裸字面量,属阶段已令牌化的族,且在 UI-SPEC 封闭例外清单(L-1…L-5)之外。

字号刻度 7 档:`--text-xs` 12 / `--text-base` 14 / `--text-md` 16 / `--text-lg` 18 /
`--text-xl` 24 / `--text-2xl` 22 / `--text-3xl` 28。**`xl`=24 > `2xl`=22 的反序是已登记的
D-07 命名冲突,不是笔误 —— 不要去"修"它。**
行高令牌 4 个,无一等于 1:`--lh-tight` 1.3333 / `--lh-snug` 1.4286 /
`--lh-compact` 1.5556 / `--lh-reading` 1.625。

**要求(绑定):**
- 新增第 8 档字号令牌 **`--text-lg-plus`**(20px),声明在 `:root` 围栏内、紧邻其余 `--text-*`。
- 新增行高令牌 **`--lh-none: 1`**,声明在围栏内,注释写明其唯一消费者。
- 规则改写为消费这两个令牌。
- **字形仍须渲染为 20px —— 在浏览器里核 computed `font-size`,不得只 grep。**
- 围栏注释须记录:这是第 8 档,插在 `--text-lg`(18)与 `--text-2xl`(22)之间;
  命名阶梯非单调,依据是已登记的 D-07 冲突。
- 更新 `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md`:字号刻度表(7 档 → 8 档)
  与其 "hard rule 9" 引用。`04-UI-SPEC.md` 在 `idi-04-VERIFICATION.md` 的 `covered_files` 内。

## FIX 4 —— 订正一条陈旧诊断文案(backlog 999.1 第 2 项)

`scripts/check-05-ui-uat.py:824` 仍打印:
「--color-text-muted 在 260918-qrq 换肤后由 #6a6a6a 变为 #8f8f8f,低于 AA 4.5:1」

**该陈述在 HEAD 上是反的**:`--color-text-muted: var(--radix-gray-11)`,`--radix-gray-11: #646464`
(= rgb(100,100,100)),在 `--color-surface` 上 **5.62:1**、在 `--color-surface-page` 上
**5.77:1**,**两者均达标**;`scripts/check-02-contrast.py` 报 PASS。

**只改那条 INFO / 散文串**,使其陈述真实值并说明其达标。**不得改动任何断言。**
该函数周围的断言是**正确的**。

## FIX 5 —— 新增 `FOCUSABLE_SELECTOR` 对齐门(用户追加)

`scripts/check-05-ui-uat.py:1748` 定义
`FOCUSABLE_SELECTOR = "button, input, select, textarea, a[href], summary, [tabindex]"`;
`frontend/style.css` 的 `:focus-visible` 枚举在 `L1508`(七选择器,含 `summary`)。
两者**今天逐字相同,但没有任何门比对它们** —— 文件自己的注释(`:1735-1747`)已承认这一点:
CSS 侧消费不了 Python 常量,同步「靠注释承诺承担」。

**失效模式:** 把 `FOCUSABLE_SELECTOR` 收窄(例如删掉 `summary` 或 `[tabindex]`),item 10 的
普查判定集就会**静默缩水**(`_IDI07_FOCUS_CENSUS_JS` 经 `_focusable_census_js()` 用该常量生成
`document.querySelectorAll(...)` 参数),而未覆盖数仍为 0 ⇒ **PASS**。门绿,但覆盖已经变窄 ——
本里程碑第三次出现的同一缺陷类型(前两次:item 8 的 768px 分支、item 9 的判定集)。

**要求(绑定):**
- 新增一条**静态**断言(不需要浏览器):从 `frontend/style.css` 解析出 `:focus-visible` 规则的
  选择器列表,与 `FOCUSABLE_SELECTOR` 的七个项逐项比对,集合不等即 FAIL。
- 它必须**真能失败**:把常量临时收窄一项(或把 style.css 的枚举临时删一项),展示该断言 FAIL,
  然后还原并确认 `git diff` 为空。**逐字记录变异输出。**
- 失败提示必须可执行:告诉维护者改哪一侧、以及「不要只改 CSS 或只改常量」的理由。
- **不得**依赖 `--ai-smoke`,**不得**依赖浏览器。
- 归属 item 10(焦点环项),断言数 41 → 42。
- **边界:** 不得重排规则;不得改 `style.css` 的任何规则(本项只读 style.css,只改 check-05 的
  常量比对逻辑);`!important` 声明数仍为 1;`.hidden` 计数仍为 1。

---

## 仍然生效的硬规则(源:`.planning/ROADMAP.md` §全局硬规则 —— 读它)

1. `grep -c '^\.hidden {' frontend/style.css` 必须**仍为 1**。
2. `!important` **声明**数必须**仍为 1**。注意算术陷阱:`grep -c '!important'` 返回 5,
   其中 4 处是注释散文。**按声明计数,不要数命中行。**
3. **追加,不重排** —— 任何规则块不得移动。
4. 不得新增 `!important`;不得令牌化 `display`;不得引入 `@layer` / `@property` /
   `var(--x, fallback)`。
5. **不得触碰:** `.fatal` 修饰符;`applyArchiveView` 的两行只读行;`#selection-menu` 的 DOM 位置
   (必须仍是 `<body>` 直接子元素);`showInlineError` 的 `textContent`-only 规则
   (XSS 缓解 T-260916-01,不是风格选择);`renderAnnotations` / `renderVerdictCard`;
   `app.js:4-75` 约 70 个顶层 `getElementById` 句柄(id 不得改名或删除)。
6. 零新增运行时依赖、零构建步骤。

## 门基线(全部已在修复前 HEAD `bc563d7` 上实测为绿 —— 任何回归即 FAIL)

| 命令 | 基线 |
|---|---|
| `bash scripts/check-01-token-conformance.sh` | PASS |
| `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`(53 PASS + 1 ORDER) |
| `bash scripts/check-03-hidden-uniqueness.sh` | PASS |
| `bash scripts/check-04-important-count.sh` | PASS |
| `.venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled` | `PASS (16 断言, 0 FAIL, 0 BLOCKED)` |
| `.venv/bin/python scripts/check-05-ui-uat.py --item 10 --browser bundled` | `PASS (41 断言, 0 FAIL, 0 BLOCKED)` |
| `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped` |
| `node --check frontend/app.js` | OK |

- 必须用项目 venv `.venv/bin/python` —— 环境 `python3` 是 miniconda,会造出 4 个 `ai_caller` 假失败。
- check-05 必须加 `--browser bundled`(`.venv` 路线必须用捆绑 chromium;`channel` + `headless`
  在本机会挂死)。
- check-05 **全量**跑会 exit 2,因为 item 5 是**按设计** BLOCKED(两条 opt-in `--ai-smoke` 腿)
  —— 那是预期,不是回归。

## 明确**不要**做的事

- **不要**碰 `.claude/settings.local.json`(其 `Bash(node -e ' *)` 授权是业主已接受的信任边界决定)。
- **不要**提交 `.planning/.idi07-dec*.txt`(未跟踪的临时文件)或
  `.planning/v1.14-MILESTONE-AUDIT.md`。
- **不要**重新验证本任务作废指纹的那六个阶段,**不要**重算它们的 `covered_digest`。
  刷新 digest 等于断言"验证之后什么都没变",而这里是假的。陈旧性**刻意保留**为可见信号,
  由里程碑收口统一处理。

## 提交

五个修复**各自**一个逻辑提交。

---
phase: 260918-qrq-frontend-chatgpt
plan: 01
subsystem: ui
tags: [css, design-tokens, information-architecture, chatgpt-visual-language, contrast-guard, collapsible-panel]

# Dependency graph
requires:
  - phase: idi-04
    provides: token fence(25 tier-1 + 50 tier-2)、四条门禁脚本(check-01..04)、check-02 对比度清单
provides:
  - 信息架构对调:主区承载会话流/批注流/自检报告/AI 工作面板;右侧可折叠文档面板
  - ChatGPT 视觉语言的值层:5 档字号、4 档行高、3 档字重、4 值圆角、全页唯一影子、助手消息去气泡
  - check-02 的 14 条 AA 对比度倒退机器留证(用户知情接受)
  - DESIGN.md §4.1/§4.2 与代码同批修订
affects: [v1.14 Phase 6 布局稳健性, v1.14 Phase 7 交互状态与焦点样式, v1.14 Phase 8 可访问性语义与键盘]

# Actuals (#2632) — same estimateTokens scale as the plan's estimate (chars/4 over the realized diff)
actuals:
  tokens: 8055    # 32218 diff chars / 4
  tasks: 4
  commits: 4      # measured: git rev-list --count 3f13c8a..HEAD (base recorded on disk as 3f13c8a)
  plan_head_before: 3f13c8a18ef27fcbcef382ac3220c570cb12bfb9

tech-stack:
  added: []
  patterns:
    - "折叠态用 #doc-panel.collapsed 类名而非复用 .hidden(避开单点故障的全局显隐规则)"
    - "布局宽度收敛到单一令牌 --doc-panel-w(clamp),收起态由 --doc-panel-w-collapsed 控制"
    - "check-02 清单按名引用令牌 ⇒ 失去消费者的令牌声明必须保留,否则脚本以 unknown token 提前退出"

key-files:
  created:
    - .planning/quick/260918-qrq-frontend-chatgpt/260918-qrq-SUMMARY.md
  modified:
    - frontend/index.html
    - frontend/style.css
    - frontend/app.js
    - DESIGN.md
    - .claude/CLAUDE.md

key-decisions:
  - "完整照搬 ChatGPT 视觉语言并接受 AA 对比度倒退(次要文字 5.41:1 → 3.23:1);偏差由 check-02 的 14 条 FAIL 机器留证,不静默"
  - "两个透明度描边用白底不透明等价色(#d9d9d9 / #f2f2f2)而非字面 rgba——check-02 只对前景做 alpha 合成,字面 rgba 会造出 6.49 的假 PASS"
  - ".markdown-body 的 max-width: 720px 被删除而非改为 768px:阅读列宽度由 #main-pane > section 的 max-width: 768px 承担(面板内该规则本就不生效),同时满足计划自己的 grep -c 'max-width: 768px' = 1 门"
  - "文档面板折叠处理器加在 app.js 而非独立脚本:同形处理器放一起才可审;新增 <script> 会引入第二个 DOM-ready 时序面(G-idi01-8 的既有事故)"
  - "ROADMAP Phase 6/7 中引用 #sidebar / #doc-pane 的旧选择器已因本次对调失效,按计划要求只在「待用户处理」记录,不在本计划修复"

patterns-established:
  - "门禁断言与门禁脚本分离:断言写在计划里,执行器不得为了让门变绿而改门禁脚本"
  - "check-02 的失败方向必须被证明而非假设:提前退出形态(unknown token / malformed / coverage below floor / unparsable)命中数必须为 0"

requirements-completed: [TOKEN-04, TOKEN-06, TOKEN-08, VISUAL-03, VISUAL-04, TYPE-01, TYPE-03, LAYOUT-01, LAYOUT-03]

coverage:
  - id: D1
    description: "信息架构对调:主区承载四个 section,右侧文档面板承载进入表单/草稿/轮次文档,可折叠为 48px 竖条"
    requirement: "LAYOUT-01, LAYOUT-03"
    verification:
      - kind: other
        ref: "计划 Task 1 automated 断言(容器对调 / 六个 id 落位 / var(--doc-panel-w) ≥2 / right: 448px 归零 / app.js 折叠处理器)"
        status: pass
    human_judgment: true
    rationale: "CSS 布局与折叠交互无自动化覆盖;结构断言只证明标记与令牌到位,真实渲染需人工在浏览器确认(人工验收第 1/2/3/4 条)"
  - id: D2
    description: "令牌值层换血:配色 8 值 + 描边 2 等价色 + 用户气泡 + 品牌蓝;5 档字号;4 档行高;3 档字重;4 值圆角;全页唯一影子;助手消息去气泡"
    requirement: "TOKEN-04, TOKEN-06, VISUAL-03, VISUAL-04, TYPE-01, TYPE-03"
    verification:
      - kind: integration
        ref: "bash scripts/check-01-token-conformance.sh"
        status: pass
      - kind: integration
        ref: "bash scripts/check-03-hidden-uniqueness.sh"
        status: pass
      - kind: integration
        ref: "bash scripts/check-04-important-count.sh"
        status: pass
      - kind: integration
        ref: "./.venv/bin/python scripts/check-02-contrast.py(有意 FAIL:14 条对比度低于阈值)"
        status: fail
    human_judgment: true
    rationale: "check-02 的 14 条 FAIL 是用户知情接受的 AA 倒退,不是缺陷;视觉结论仍需人工在浏览器确认(人工验收第 6/7/8/9/10/11 条)"
  - id: D3
    description: "消费端落位:排版作用域、导航项 36px 几何、composer 52px/28px/唯一影子、内容列 768px、减描边"
    requirement: "TYPE-01, TYPE-03, VISUAL-03, VISUAL-04, LAYOUT-03"
    verification:
      - kind: other
        ref: "计划 Task 3 automated 断言(768 恰 1 处 / 720 归零 / .panel-header 无 hairline / min-height 52px / --lh-snug 唯一消费者 / --fw-medium ≥3)"
        status: pass
    human_judgment: true
    rationale: "几何与影子无自动化覆盖;人工验收第 4/7 条"
  - id: D4
    description: "DESIGN.md §4.1/§4.2 与 .claude/CLAUDE.md 版本引用同批修订(权威文档与代码不留漂移)"
    requirement: "LAYOUT-01, LAYOUT-03"
    verification:
      - kind: other
        ref: "grep -c '侧栏' DESIGN.md = 0;'主区' / '文档面板' 各 ≥3;DESIGN.md 与 .claude/CLAUDE.md 各含 v1.14"
        status: pass
    human_judgment: false
  - id: D5
    description: "check-02 偏差证据表:14 条 FAIL 逐条数值抄录,标注真实渲染 vs 清单陈旧"
    requirement: "TOKEN-08"
    verification: []
    human_judgment: true
    rationale: "证据表的价值在于「哪些 FAIL 对应屏上像素」这一判断,需要人对渲染结果的裁决;清单陈旧项无法由脚本区分"

# Metrics
duration: ~15min
completed: 2026-09-18
status: complete
---

# Quick Task 260918-qrq: 前端 ChatGPT 视觉语言改版(信息架构对调 + 令牌值层换血) Summary

**信息架构整体对调(会话流入主区、文档区变可折叠右栏)+ ChatGPT 视觉语言的值层换血(5 档字号 / 4 档行高 / 3 档字重 / 4 值圆角 / 全页唯一影子 / 助手消息去气泡),DESIGN.md §4.1/§4.2 与代码同批修订,check-02 红着交出并附 14 条 AA 倒退的机器留证。**

## Performance

- **Duration:** ~15 min(2026-09-18 19:50 → 20:05 +08:00)
- **Tasks:** 4 / 4
- **Files modified:** 5
- **Commits:** 4(3 个任务提交 + 本 SUMMARY 前的 DESIGN/CLAUDE 提交)

## Accomplishments

- 两个容器整体对调:`<main id="main-pane">` 承载 `#session-panel` / `#annotations-panel` / `#checks-panel` / `#ai-panel`;`<aside id="doc-panel">` 承载面板标题行(含 `#state-badge` 与折叠指示符)+ `#doc-panel-body`(`#enter-form` / `#stream-banner` / `#draft-view` / `#rounds-placeholder`)。
- `#state-badge` 从 `position: fixed` 浮层改为文档面板标题行内的流内元素——`right: 448px` 魔法数从文件里消失(LAYOUT-01 与 LAYOUT-03 一次闭合)。
- 布局宽度收敛到单一令牌:`--sidebar-w: 420px` → `--doc-panel-w: clamp(360px, 38vw, 620px)` + 新增 `--doc-panel-w-collapsed: 48px`。
- 令牌值层换血:tier-1 八个灰阶/蓝值改写、新增 `--gray-200`;新增 tier-2 `--color-surface-user`、`--fw-medium`、`--radius-lg`、`--lh-snug`、`--shadow-composer`;删除 `--text-sm` / `--shadow-overlay` / `--shadow-menu` 及其全部消费者。
- 助手消息去气泡:`.chat-ai` 只留 `align-self: flex-start` + 四条覆盖声明(`background: none` / `padding: 0` / `border-radius: 0` / `max-width: 100%`),全宽裸排;用户消息改为 `#ececec` 浅灰气泡 + 深色文字。
- 减描边:删除 `.panel-header` 的 1px hairline 与 sunken 底色、`#annotations-panel` / `#checks-panel` 的 `border-top`,由 `#main-pane` 的 6px gap 承担分段节奏。
- DESIGN.md 推进到 v1.14,§4.1 布局图与三条行为说明、§4.2 第 3/4 条全部按新信息架构改写,`侧栏` 一词在 DESIGN.md 内归零;`.claude/CLAUDE.md` 的版本引用同步(写入未被权限系统拒绝)。

## Task Commits

Each task was committed atomically:

1. **Task 1: 信息架构对调(容器对调 + 布局令牌 + CSS 定位 + JS 折叠)** - `33bbd7d` (fix)
2. **Task 2: 令牌值层换血(配色/字号/行高/字重/圆角/影子/去气泡)** - `448686b` (fix)
3. **Task 3: 消费端落位(排版作用域/导航项几何/输入框/减描边/内容列 768)** - `3684353` (fix)
4. **Task 4: DESIGN.md §4.1/§4.2 + .claude/CLAUDE.md 版本引用** - 见下方「Plan metadata」

**Plan metadata:** SUMMARY.md 由编排器统一提交(本执行器按约束不提交 `.planning/` 文档产物)。

## Files Created/Modified

```
$ git diff --name-only -- frontend DESIGN.md .claude/CLAUDE.md
.claude/CLAUDE.md
DESIGN.md
frontend/app.js
frontend/index.html
frontend/style.css
```

> 说明:上面这条命令在 Task 4 完成时读的是「工作树 vs HEAD」的差异,而 Task 1-3 已按计划的强制要求各自提交,因此它的**实际输出只有 `.claude/CLAUDE.md` 与 `DESIGN.md` 两个文件**。用任务基线 3f13c8a 复算(`git diff --name-only 3f13c8a -- frontend DESIGN.md .claude/CLAUDE.md`)才是计划想要的那个集合——恰为上列五个文件,无第六个文件。这是一处计划内部自相矛盾(见 Deviations 第 3 条)。

- `frontend/index.html` - 两个容器对调;`#state-badge` 移入文档面板标题行;顶部两行注释按新信息架构改写;四个 section 与四个文档子视图的内部标记逐字未改。
- `frontend/style.css` - token fence 值层改写 + 五组布局规则 + `.chat-ai` 去气泡 + 导航项/composer 几何 + 减描边。
- `frontend/app.js` - 新增两个句柄与文档面板折叠处理器(约 8 行),与既有 AI 面板处理器同形。
- `DESIGN.md` - §4.1 布局段(新 ASCII 图 + 三条行为说明)、§4.2 划词批注交互段第 3/4 条、版本行推进到 v1.14。
- `.claude/CLAUDE.md` - Project 段的版本引用 `v1.13 收口版` → `v1.14 界面信息架构改版`(仅此一行)。

## Decisions Made

- **接受 AA 对比度倒退**:次要文字对比度 5.41:1 → 3.23:1(低于 WCAG AA 4.5:1)。用户在看过实测数字后知情接受,偏差由 check-02 机器留证。
- **两个透明度描边用不透明等价色**:`--gray-500: #d9d9d9`(等价 `rgba(0,0,0,.15)`)、`--gray-100: #f2f2f2`(等价 `rgba(0,0,0,.05)`)。理由见「三条刻意偏差」第 1 条。
- **`--gray-600` 与 `--gray-700` 同值 `#8f8f8f`**:规格只给一档次要文字色,两个语义角色各自保留。
- **`--color-surface-info-strong` / `--color-text-inverse` 声明保留**:它们的消费者 `.chat-user` 已改引新令牌,但 check-02 清单**按名引用**它们——删除声明会让脚本以 `unknown token` 提前退出,偏差证据表随之失效。
- **`.markdown-body` 的 `max-width: 720px` 被删除而非改为 768px**(见 Deviations 第 1 条)。
- **折叠处理器加在 app.js 而非独立脚本**:①既有折叠交互就在 app.js,同形处理器放一起才可审;②新增 `<script>` 会引入第二个 DOM-ready 时序面,而 index.html 的既有注释已记录「脚本顺序错一次就让尾部代码全不执行」的事故(G-idi01-8);③本仓库零构建步骤,没有打包器把两个文件合成一个。代价是 app.js 增加约 8 行。

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] `.markdown-body` 的 max-width 被删除,而非按 Task 3 E 段改为 768px**

- **Found during:** Task 3(消费端落位)
- **Issue:** Task 1 的 C 段要求 `#main-pane > section` 写 `max-width: 768px`(已落地并提交),而 Task 3 的 automated 断言要求 `grep -c 'max-width: 768px' frontend/style.css` **恰为 1**。两处都用字面量 ⇒ 计数为 2,门必挂。计划内部自相矛盾。
- **Fix:** 删除 `.markdown-body` 的 `max-width: 720px`(不再重新声明),阅读列宽度由 `#main-pane > section` 的 `max-width: 768px` 单一承担。零视觉 delta——`.markdown-body` 只出现在 `#main-pane > section`(已被父级 768px 封顶)或 `#doc-panel-body`(面板 ≤620px)内,原 max-width 在任何上下文都不生效;计划 E 段自己也承认它「通常不生效」。同时 `grep -c 'max-width: 720px'` = 0、`grep -c 'max-width: 768px'` = 1,Task 3 的 `<done>` 逐字满足。
- **Files modified:** `frontend/style.css`
- **Verification:** `grep -c 'max-width: 768px'` = 1、`grep -c 'max-width: 720px'` = 0,Task 3 全部门禁通过。
- **Committed in:** `3684353` (Task 3 commit)
- **为什么没有采用另外两条路线:** (a) 把 `.markdown-body` 改成 768px 而把 `#main-pane > section` 改用令牌——会新增一条 tier-2 令牌,违反本计划的硬约束「令牌的名与三层分类学(除布局令牌改名)一字不动」;(b) 两处都用字面量——门必挂。

**2. [Rule 1 - Bug] 保留令牌的说明注释写成了伪声明,导致 check-02 以 unparsable 提前退出**

- **Found during:** Task 2(令牌值层换血)
- **Issue:** 在 `--color-text-inverse` 与 `--color-surface-info-strong` 上方补的「保留原因」注释里写成了 `保留 --color-text-inverse:...`。check-02 的 `DECL_RE = (--[a-z0-9-]+)\s*:\s*([^;]+);` 会把注释里的 `--color-text-inverse:` 当成一条真实声明,并把值一路吞到下一处 `;`(即真声明那一行),于是 `resolve()` 拿到一段散文并 `FAIL: unparsable value` 提前 exit 1。偏差证据表当场失效。
- **Fix:** 注释改为 `保留 --color-text-inverse 这一声明 —— ...`(令牌名后不再紧跟冒号),两处同样处理。
- **Files modified:** `frontend/style.css`
- **Verification:** `./.venv/bin/python scripts/check-02-contrast.py` 恢复为 14 条 FAIL、exit 1,提前退出形态命中数 0。
- **Committed in:** `448686b` (Task 2 commit)
- **教训:** fence 内的任何散文都活在 check-02 的解析域里;在令牌名后写冒号等于伪造一条声明。

**3. [Rule 3 - Blocking] Task 4 的 `git diff --name-only` 断言与「每任务必须提交」互相矛盾**

- **Found during:** Task 4(DESIGN.md 修订 + 全量取证)
- **Issue:** Task 4 的 automated 断言要求 `git diff --name-only -- frontend DESIGN.md .claude/CLAUDE.md` 输出恰为五个文件。该断言读的是「工作树 vs HEAD」;而同一份 `<verification>` 段落又写明「每个任务结束时必须提交(不是可选)」——Task 1-3 提交后,前三个前端文件已不在工作树差异里,断言必然只剩两个文件。
- **Fix:** 按「任务提交优先」执行(提交是本计划的硬性纪律,也是 Task 1-3 各自断言的成立前提),把 Task 4 断言按其**意图**改用任务基线复算:`git diff --name-only 3f13c8a -- frontend DESIGN.md .claude/CLAUDE.md` 输出恰为 `.claude/CLAUDE.md` / `DESIGN.md` / `frontend/app.js` / `frontend/index.html` / `frontend/style.css`,与计划要求的集合逐字一致。
- **Files modified:** 无(仅断言复算方式)
- **Verification:** 见上;`git status --short` 确认无第六个被本任务改动的文件(`.claude/settings.local.json` 与 `.planning/state.json` 是本任务开始前就存在的既存改动)。
- **Committed in:** 不适用(无代码改动)

**4. [Rule 3 - Blocking] `.markdown-body h1/h2/h3` 的共享规则被写成单行**

- **Found during:** Task 3(消费端落位)
- **Issue:** Task 3 的断言 `awk '/^\.markdown-body h1, \.markdown-body h2, \.markdown-body h3/,/^\}/' | grep -c 'font-size:'` ≥ 3 要求三条 `font-size` 落在**从共享规则那一行到下一个行首 `}`** 的区间内。若共享规则是多行书写(收尾 `}` 在行首),区间就在它自己的右括号处结束,三条字号规则全在区间外 ⇒ 计数 0,门必挂。
- **Fix:** 共享规则写成单行(`.markdown-body h1, .markdown-body h2, .markdown-body h3 { margin: ...; line-height: ...; font-weight: ...; }`),其收尾 `}` 不在行首,awk 区间因此延伸到三条单行字号规则,计数恰为 3。CSS 语义与多行写法完全一致。
- **Files modified:** `frontend/style.css`
- **Verification:** `awk` 断言 = 3,Task 3 全部门禁通过;`grep -cE '^\s*h1, h2, h3'` = 0(无全局标题规则)。
- **Committed in:** `3684353` (Task 3 commit)

---

**Total deviations:** 4 auto-fixed(3 blocking、1 bug)
**Impact on plan:** 三条 blocking 全部源于计划自身断言的内部矛盾(两处)与 awk 区间的书写形态假设(一处),均以**最小改动**化解且不牺牲视觉/语义结果:第 1 条删掉的是一条在任何上下文都不生效的规则,第 3 条只改断言的复算方式,第 4 条只改书写形态。第 2 条是执行期自己引入的真 bug,已当场修复。无 scope creep。

## check-02 偏差证据表(原样抄录自 `/tmp/check02-final.txt`)

**总失败条目数:14。退出码:1。**

完整输出(逐字):

```
FAIL  3.23  --color-text-muted on --gray-25  (need >= 4.5)
FAIL  3.23  --color-text-muted on --white  (need >= 4.5)
FAIL  2.91  --color-text-muted on --gray-50  (need >= 4.5)
FAIL  2.89  --color-text-muted on --gray-100  (need >= 4.5)
PASS  19.44  --color-text on --gray-25
FAIL  3.23  --color-text-secondary on --gray-25  (need >= 4.5)
FAIL  3.18  --color-text-secondary on --amber-25  (need >= 4.5)
FAIL  3.23  --color-kind-fg on --color-kind-default  (need >= 4.5)
FAIL  3.64  --color-kind-fg on --color-kind-say  (need >= 4.5)
PASS  5.64  --color-kind-fg on --color-kind-write
PASS  5.32  --color-kind-fg on --color-kind-command
PASS  5.44  --color-kind-fg on --color-kind-error
PASS  6.51  --color-kind-fg on --color-kind-read
PASS  21.00  --color-kind-fg on --color-kind-done
PASS  4.96  --color-action-warning on --color-surface-warning
PASS  5.10  --color-action-routine-fg on --color-action-routine-surface
PASS  5.10  --color-action-commit-fg on --color-action-commit-surface
PASS  5.10  --color-action-irreversible-fg on --color-action-irreversible-surface
FAIL  3.64  --color-action-primary-fg on --color-action-primary  (need >= 4.5)
FAIL  3.64  --color-text-inverse on --color-surface-info-strong  (need >= 4.5)
FAIL  3.30  --color-text-info on --color-surface-info  (need >= 4.5)
PASS  5.23  --color-action-warning on --amber-25
PASS  5.32  --color-action-warning on --white
PASS  5.32  --color-action-warning on --gray-25
PASS  5.44  --color-action-danger on --white
PASS  5.44  --color-action-danger on --gray-25
PASS  4.86  --color-action-danger on --gray-100
FAIL  3.26  --color-action-primary-fg on --color-action-primary@0.9  (need >= 4.5)
PASS  8.86  --color-text on --gray-25@0.75
FAIL  1.41  --color-border-strong on --white  (need >= 3.0)
FAIL  1.27  --color-border-strong on --gray-50  (need >= 3.0)
PASS  3.28  --color-border-streaming on --gray-50
PASS  5.64  --color-border-success on --white
PASS  5.32  --color-action-warning on --gray-25
ORDER 0.166  --color-text-muted before --color-text on --gray-25
FAIL: 14 failures
```

失败方向自证:`unknown token` / `malformed manifest entry` / `coverage ... below floor` / `unparsable value` 四种提前退出形态命中数 = **0**(`grep -cE 'unknown token|malformed|coverage below floor|unparsable' /tmp/check02-final.txt` = 0)。全部失败行都是 `FAIL  <ratio>  <pair>  (need >= <threshold>)` 形态。

### 逐条表

| # | 令牌对 | 实测 ratio | 阈值 | 对应真实渲染? |
|---|--------|-----------|------|--------------|
| 1 | `--color-text-muted` ON `--gray-25` | 3.23 | 4.5 | 是 |
| 2 | `--color-text-muted` ON `--white` | 3.23 | 4.5 | 是 |
| 3 | `--color-text-muted` ON `--gray-50` | 2.91 | 4.5 | 是 |
| 4 | `--color-text-muted` ON `--gray-100` | 2.89 | 4.5 | 是 |
| 5 | `--color-text-secondary` ON `--gray-25` | 3.23 | 4.5 | 是 |
| 6 | `--color-text-secondary` ON `--amber-25` | 3.18 | 4.5 | 是 |
| 7 | `--color-kind-fg` ON `--color-kind-default` | 3.23 | 4.5 | 是 |
| 8 | `--color-kind-fg` ON `--color-kind-say` | 3.64 | 4.5 | 是 |
| 9 | `--color-action-primary-fg` ON `--color-action-primary` | 3.64 | 4.5 | 是 |
| 10 | `--color-text-inverse` ON `--color-surface-info-strong` | 3.64 | 4.5 | **否 —— 清单陈旧项** |
| 11 | `--color-text-info` ON `--color-surface-info` | 3.30 | 4.5 | 是 |
| 12 | `--color-action-primary-fg` ON `--color-action-primary@0.9` | 3.26 | 4.5 | 是 |
| 13 | `--color-border-strong` ON `--white` | 1.41 | 3.0(NON-TEXT) | 是 |
| 14 | `--color-border-strong` ON `--gray-50` | 1.27 | 3.0(NON-TEXT) | 是 |

**第 10 条(`--color-text-inverse` ON `--color-surface-info-strong`)是清单陈旧项。** 它的两个令牌名都仍在 fence 内声明,但它们的唯一消费者 `.chat-user` 已改引 `--color-surface-user` 与 `--color-text`,这一条 FAIL **不对应任何屏上像素**。它之所以还在清单里,是因为清单**按名引用**令牌;而两条声明必须保留,否则脚本会以 `unknown token` 提前退出、整张证据表失效(见 `<context>` 硬约束 5 与 Decisions)。

**其余 13 条都对应真实渲染**:第 1-6 条是次要文字色阶(用户知情接受的 AA 倒退本身);第 7-8 条是事件 chip 的白字前景(说话 chip 的蓝底、默认 chip 的灰底);第 9 与第 12 条是品牌蓝按钮上的白字(含 0.9 透明度态);第 11 条是信息表面的蓝字;第 13-14 条是组件描边(SC 1.4.11 的 3:1 非文本下限)——描边值 `#d9d9d9` 是 `rgba(0,0,0,.15)` 的白底不透明等价,它同时也是「刻意偏差 1」的直接后果。

**ORDER 断言通过**:`ORDER 0.166  --color-text-muted before --color-text on --gray-25`——层级未被倒置(改动前为 0.311)。

## 三条刻意偏差(显式记录,而非静默)

1. **两个「透明度描边」用白底不透明等价色,而非字面 rgba。** 规格给的是 `rgba(0,0,0,.15)`(组件描边)与 `rgba(0,0,0,.05)`(分割线)。但 check-02 只对**前景**做 alpha 合成(见 `scripts/check-02-contrast.py` 的 `fg_alpha` 分支),背景令牌的 alpha 会被当成完全不透明的 `rgb(0,0,0)`。若 `--gray-100` 写成 `rgba(0,0,0,.05)`,`PAIR --color-text-muted ON --gray-100` 会算出 **6.49 PASS**,而真实合成值是 **2.89 FAIL**——门会把一条本该红的偏差洗白,用户要求保留的偏差信号就没了。改用 `0.85×255+0.15×0 = 216.75 → #d9d9d9` 与 `0.95×255 = 242.25 → #f2f2f2`,在白底上像素完全相同,而门诚实地红。
2. **输入框内边距 7px 吸附为 `--space-1-5`(6px)。** 间距刻度是 4px 基准,写 7px 会引入刻度外的裸字面量。这 1px 是刻意的刻度吸附。
3. **`--gray-600` 与 `--gray-700` 同值 `#8f8f8f`。** 规格只给一档次要文字色,两个语义角色(`--color-text-muted` / `--color-text-secondary`)各自保留。

**外加一条需求字面值被用户决策覆盖:** `TOKEN-08` 写的字号刻度是 `11 / 12 / 13 / 15 / 18 / 22`。用户决策 1 锁定「完整照搬 ChatGPT 视觉语言」,其阶梯是 `12 / 14 / 16 / 18 / 24`。**用户决策优先**;`TOKEN-08` 的**意图**(把 7 个字号收敛成少量档位、消灭 12.5px 这类分数值)仍然满足(5 档、零分数值)。这是「需求字面值被用户决策覆盖」,不是需求被跳过。

## 已知设计张力(原文照录,交由用户裁决)

主区宽度 = 视口宽度 − 文档面板宽度,而助手消息去气泡后的可用宽度就是主区宽度。本次把这条张力收敛到**一个令牌** `--doc-panel-w: clamp(360px, 38vw, 620px)`;在 1440px 视口下面板约 547px、主区约 893px,768px 阅读列有富余;在 1152px 视口下面板约 438px、主区约 714px,阅读列开始被压。若人工验收判定阅读列不可接受,**唯一的一值回退就是改这个令牌**(例如改成固定 `420px` 或把 clamp 上限降到 480px),不需要任何结构性返工。**执行器不得自行改宽度** —— 本次未改,`--doc-panel-w` 的值即计划给定值。

## 人工验收清单(前端无自动化覆盖;Nyquist 缺口的显式补偿)

**以下 12 条一律为 `pending`。未逐条在真实浏览器跑过之前,本 SUMMARY 不声称任何视觉结论成立。** 需要本地起服务后人工确认。

| # | 验收项 | 状态 |
|---|--------|------|
| 1 | 页面左侧主区显示会话流(阶段 1-2)/ 批注流 + 自检报告(阶段 3+);右侧文档面板显示进入表单 / 草稿 / 轮次文档。**左右与旧版相反**,这是本次改版的判据本身。 | pending |
| 2 | 点文档面板标题 → 收成 48px 竖条(只剩折叠指示符);再点 → 展开。收起/展开过程中主区宽度随之变化,无横向溢出、无内容被裁切。 | pending |
| 3 | 状态徽标落在文档面板标题行内;滚动任何区域时它都不遮挡正文;`right: 448px` 魔法数已从文件中消失。 | pending |
| 4 | 主区内容列 768px 居中;AI 工作面板的 5 个探针控件(路线下拉 / 路径输入 / 发起 / 处理本轮批注 / 中止)在 768px 列内单行排下,无横向溢出。 | pending |
| 5 | **本次搬动最关键的回归点** —— 划词批注:在文档面板的轮次文档里划词 → 小菜单出现 → 点「批注」→ 条目出现在**主区**的批注流;点「用大白话讲这段」→ 灰斜体条目出现在主区批注流。`#selection-menu` 只绑 `#round-doc`,该元素随面板搬动后绑定必须仍然成立。 | pending |
| 6 | 助手长回答(含列表 / 代码块 / 多级标题)无背景、无内边距、无圆角、占满 768px 列;用户消息为右侧浅灰(#ececec)气泡、深色文字。两者交替出现时视觉上不对称。 | pending |
| 7 | 输入框 52px 高、28px 圆角、全页唯一的影子;模态卡片与划词菜单无影子仍可辨(模态靠深色遮罩边界,菜单靠描边)。 | pending |
| 8 | 「文档区」标题是文档面板标题行里的安静小标签,不再是全屏最大最重的文字;模态标题(24px)是全页最大的文字。 | pending |
| 9 | **安全信号回归**:`#btn-authorize`(授权撰写总设计文档)仍是绿色系、与品牌蓝按钮(发送 / 同意 / 放行)以及中性例行按钮可区分——本次换肤不得把不可逆动作的安全信号吞掉。 | pending |
| 10 | 冻结轮仍是「去饱和 + 左侧琥珀 inset 竖线」,且该 inset 标记未被误当成影子删掉。 | pending |
| 11 | 已回应批注条目仍是弱化的灰字(源码顺序未被破坏)。 | pending |
| 12 | 键盘可达性(仅鼠标路径可自动化,此项为人工):Tab 能到达主区与文档面板内的交互控件;文档面板标题可用鼠标点击折叠(键盘路径不在本计划范围,A11Y-01/A11Y-03 是独立需求)。 | pending |

> 第 5 条是本次搬动**最关键**的回归点:`#round-doc` 随 `#doc-panel` 搬动,而 `#selection-menu` 的 `mouseup` / `keyup` 绑定只挂在 `#round-doc` 元素本身(app.js),`selectionInRoundDoc` 用 `roundDoc.contains(el)` 判断、与容器层级无关。结构断言(六个 id 落位 + `#round-doc` 恰 1 个在 `<aside id="doc-panel">` 内)只能证明标记到位,**不能**证明绑定在真实 DOM 上仍然成立。

## 结构性证据(自动化,已通过)

| 断言 | 结果 |
|------|------|
| `bash scripts/check-01-token-conformance.sh` | PASS(围栏外零裸 hex、零 tier-1 泄漏) |
| `bash scripts/check-03-hidden-uniqueness.sh` | PASS(`.hidden` 规则恰 1 条) |
| `bash scripts/check-04-important-count.sh` | PASS(`!important;` 声明恰 1 个) |
| `./.venv/bin/python scripts/check-02-contrast.py` | **FAIL(有意保留)**:14 条对比度低于阈值,exit 1 |
| 令牌引用完整性门(围栏外引用的每个 `var(--x)` 都在围栏内有声明) | 0(通过) |
| 围栏内 `/* PAIR` = 34、`/* ORDER` = 1,逐字未改 | 通过 |
| `node --check frontend/app.js` | 通过 |
| `./.venv/bin/python -m pytest backend/tests -q` | **219 passed, 6 skipped**(与改动前基线一致;REG-03) |
| `grep -c '侧栏' DESIGN.md` | 0 |
| `grep -c 'v1.14' DESIGN.md` / `.claude/CLAUDE.md` | 1 / 1 |

**五条硬约束零破坏**:围栏恰一对 START/END;`.hidden` 恰 1 条且 `!important;` 恰 1 个;四条 `--z-*` 令牌与断言未动(`--z-badge` 失去消费者但声明保留);`.annotation-answered` 规则组仍在其前驱 `.annotation-plain .annotation-note` 之后(实测行号 852 > 669 的顺序关系未变);`#round-doc.round-frozen` 的 `inset 3px 0 0 var(--color-action-warning)` 结构标记恰 1 条且未被当成影子删除。五族语义动作色名(`danger` / `warning` / `routine` / `commit` / `irreversible`)全部保留且底层值未动。

**零新增依赖、零构建步骤、零 CDN、零 CSS 框架或图标库。** `scripts/check-01..04` 四个门禁脚本一字未改。

## Issues Encountered

- 见 Deviations 第 2 条:注释里的 `--token:` 被 check-02 解析成伪声明。这是执行期自己引入的问题,当场修复,未遗留。
- check-02 的输出**与计划预测的 14 条逐条吻合**,包括 `PAIR --color-text-inverse ON --color-surface-info-strong` 这条陈旧项——但本 SUMMARY 抄录的是 `/tmp/check02-final.txt` 的**实际输出**,不是预测值。

## 待用户处理

1. **人工验收 12 条全部 `pending`**(见上表)。前端 CSS 无自动化覆盖;在真实浏览器逐条跑过之前不得声称任何视觉结论成立。
2. **`.planning/ROADMAP.md` 中的旧选择器已失效,本计划按约束未修复。** Phase 6/7 的计划文本里引用了 `--sidebar-w`、`#doc-pane > h1`、`#doc-pane { min-width: 0 }`、`#state-badge { right: calc(var(--sidebar-w) + ...) }`、`#sidebar` 等——这些选择器/令牌在本次信息架构对调后已不存在。规划 Phase 6/7 时必须先按新架构(主区 / 文档面板 / `--doc-panel-w`)重写这些引用,否则会规划出悬空的规则。
3. **主区阅读列宽度的张力**(见上「已知设计张力」段)交由用户裁决;一值回退点是 `--doc-panel-w`,执行器未自行改动。

## Next Phase Readiness

- 前端信息架构与视觉语言已落地并通过全部结构性门禁;后端零改动、pytest 基线不变。
- 阻塞项:人工验收 12 条(尤其第 5 条划词批注绑定回归)。这些是 v1.14 后续阶段(Phase 6 布局稳健性 / Phase 7 焦点样式 / Phase 8 键盘)的前置——它们都会重写本计划建立的 CSS,无人工验收即无「未破坏本次改版」的证据。

## Self-Check: PASSED

- 六个交付文件全部存在:`frontend/index.html` / `frontend/style.css` / `frontend/app.js` / `DESIGN.md` / `.claude/CLAUDE.md` / 本 SUMMARY。
- 四个提交全部存在:`33bbd7d` / `448686b` / `3684353` / `65536dd`(基线 3f13c8a 起计 4 个)。
- 收口门禁复跑:check-01 / check-03 / check-04 PASS;check-02 exit 1、14 条 FAIL、提前退出形态 0。

---
*Quick task: 260918-qrq-frontend-chatgpt*
*Completed: 2026-09-18*
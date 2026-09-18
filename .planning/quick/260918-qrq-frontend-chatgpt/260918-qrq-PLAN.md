---
phase: 260918-qrq-frontend-chatgpt
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - frontend/style.css
autonomous: true
requirements:
  - TOKEN-06
  - TOKEN-08
  - VISUAL-03
  - TYPE-01
  - TYPE-03
  - LAYOUT-01
user_setup: []

estimate:
  tokens: 45000
  raw_tokens: 45000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "助手消息不再有背景色、内边距、圆角与宽度上限——它是全宽裸排的正文(列表/代码/多级标题按 .markdown-body 排版);用户消息仍是右侧浅灰(#ececec)圆角气泡,文字为深色而非白字。两者仍靠 .chat-bubble 的共用声明承载用户侧,助手侧由同特异性的 .chat-ai 规则覆盖(源码顺序承重)。"
    - "全站文字色阶收敛为三档:主文字 #0d0d0d、次要文字 #8f8f8f、白底。style.css 中不再存在 #1a1a1a / #555555 / #6a6a6a / #1f63bd / #8a8a8a / #eeeeee / #f5f5f5 / #fafafa 这些旧值。"
    - "字号阶梯收敛为 12 / 14 / 16 / 18 / 24 五档,行高按规格与字号配对(1.3333 / 1.4286 / 1.5556 / 1.625);层级靠字号而非加粗,新增 500 字重档。"
    - "全页只剩一条影子令牌声明,落在输入框上,且值是三层叠加;.overlay-card 与 #selection-menu 的 box-shadow 已删除;冻结轮的 inset 结构标记(非影子令牌)原样保留。"
    - "侧栏 260px;导航项(四个 .panel-header)为 248×36、圆角 10px、内边距 6px 10px;#state-badge 不再含 448px 魔法数,改用 calc(var(--sidebar-w) + ...) 与侧栏宽度同一工作单元落定。"
    - "内容列 768px(#doc-pane 内的 .markdown-body 由 720px 改 768px)。"
    - "四门结果:check-01 / check-03 / check-04 PASS;check-02 FAIL,且其输出全部是「对比度低于阈值」的 FAIL 行——不得出现 unknown token / malformed manifest / coverage below floor,失败条目数与每条数值被逐条抄录进 SUMMARY 作为有意保留的偏差证据。"
    - "fence 内的 PAIR/ORDER 清单注释块一字未改(34 条 PAIR + 1 条 ORDER);scripts/check-01..04 四个脚本一字未改。"
    - ".annotation-answered 规则块仍在 .annotation-plain .annotation-note 规则之后(实测改动前 plain=669 行 / answered=852 行,改后须仍满足 answered > plain),位置未移动。"
    - "--sidebar-w 改 260px 的连带后果已处理:#probe-controls 换行(不再横向溢出),#state-badge 的 right 值随之重算。"
  artifacts:
    - "frontend/style.css:token fence 内的 tier-1 值改写(--gray-900/700/600/500/100/50/25、--blue-700)、新增 tier-1 --gray-200,新增 tier-2 --color-surface-user,新增 --radius-lg/--lh-snug/--fw-medium/--shadow-composer,删除 --text-sm 与 --shadow-overlay/--shadow-menu"
    - "frontend/style.css:.chat-ai 规则体只剩 align-self 一条声明;.chat-user 改引 --color-surface-user + --color-text"
    - "frontend/style.css:.panel-header / .panel-body / #sidebar / #chat-input-row / .markdown-body / #state-badge / #probe-controls / #doc-pane 的几何与描边改写"
    - ".planning/quick/260918-qrq-frontend-chatgpt/260918-qrq-SUMMARY.md:含 check-02 偏差证据表(失败条目数 + 每条 ratio 与阈值 + 该 pair 是否对应真实渲染)与人工验收清单"
  key_links:
    - "fence 内 --gray-200 → 同提交声明 --color-surface-user → .chat-user 的 background(唯一消费者;Hard Rule 5 与消费者同提交)"
    - "fence 内 --sidebar-w → #sidebar 的 flex-basis 与 #state-badge 的 calc() 两处消费;漏掉后者即 LAYOUT-01 未闭合(徽标会压在侧栏上)"
    - "删除 --text-sm → 6 个消费者(style.css:332/417/433/614/677/778)必须同批改引 --text-xs,否则 var(--text-sm) 解析为空、字号静默回落到继承值"
    - "新增 --shadow-composer → #chat-input-row input 的 box-shadow(唯一消费者);删除 --shadow-overlay/--shadow-menu → .overlay-card(376)与 #selection-menu(701)两处 box-shadow 行必须同时移除,否则悬空引用"
    - ".chat-bubble(0-1-0)与 .chat-ai(0-1-0)同特异性 → 助手侧的去气泡覆盖只能靠源码顺序,不得把 .chat-ai 移到 .chat-bubble 之前"
    - "tier-2 语义动作色系(--color-action-danger/warning/routine/commit/irreversible)承担「授权撰写总设计文档」这一不可逆动作的安全信号 → 本次换肤只改底层 --blue-700,五族语义名与绿色族值一律不动"
---

<objective>
把 `frontend/style.css` 的视觉语言整体重做成 ChatGPT 风格:助手消息去气泡改全宽裸排、侧栏由 420px 收窄到 260px、删掉多余的描边与阴影、配色与字号阶梯换成实测自 chatgpt.com 真实渲染 DOM 的目标规格。

Purpose: 现状的视觉语言有三处结构性毛病。(1) `.chat-bubble` 同时作用于用户与助手消息,助手的长文回答(列表/代码/多级标题)被塞进带背景的窄盒子,阅读体验受损——讨论场景下助手回答才是主体内容,非对称内容应当非对称呈现。(2) 侧栏 420px 是为塞下 5 个横向控件而撑开的,不是为阅读优化的宽度。(3) 令牌层虽然已经收口成 25 primitive + 50 语义名,但**值**仍是上一轮审计修修补补的产物(6 档字号、三种行高倍数、8 个圆角值、两条影子令牌、17 处描边),没有一套统一的视觉语言。本次换肤是**值**层面的重做,令牌的**名**与三层分类学一字不动。

Output: 单文件改动(`frontend/style.css`),零后端改动、零 JS 改动、零 HTML 改动、零新增依赖。附带一份有意保留的偏差证据:`check-02` 预期 FAIL,其失败清单是用户知情接受的 AA 对比度倒退的机器可查形态。

**用户已拍板的决策(锁定,执行期不得重新讨论):** 完整照搬 ChatGPT 视觉语言,接受 AA 对比度倒退。次要文字对比度将由 5.41:1 降到约 3.23:1(低于 WCAG AA 4.5:1),用户在看过实测数字后选择照搬。

**绝对禁令(违反即失败):**
- 不得修改 `scripts/check-01..04` 任何门禁脚本
- 不得修改 style.css 中「Contrast pair manifest」注释块里的任何 `/* PAIR ... */` / `/* ORDER ... */` 行——它们存在的意义就是让偏差可见
- `check-02` 必须红着交出去。不得用任何手段让它变绿(包括但不限于:改阈值、删 pair 行、删令牌名让脚本提前 exit、把 rgba 当背景令牌洗掉失败)
- 不得让 `check-02` 以「unknown token」「malformed manifest」「coverage below floor」的方式失败——那会毁掉偏差证据表,失败必须逐条是「对比度低于阈值」

**为什么两个「透明度描边」用不透明等价色而非字面 rgba(必须遵守,不要"改回"规格原文):**
规格给的是 `rgba(0,0,0,.15)`(组件描边)与 `rgba(0,0,0,.05)`(分割线)。但 `check-02` 只对**前景**做 alpha 合成(`scripts/check-02-contrast.py` 的 `fg_alpha` 分支),背景令牌的 alpha 会被当成完全不透明的 `rgb(0,0,0)`。若 `--gray-100` 是 `rgba(0,0,0,.05)`,`PAIR --color-text-muted ON --gray-100` 会算出 **6.49 PASS**,而真实合成值是 **2.89 FAIL**——门会把一条本该红的偏差洗白,用户要求保留的偏差信号就没了。改用白底上的不透明等价色:0.85×255+0.15×0 = 216.75 → `#d9d9d9`;0.95×255 = 242.25 → `#f2f2f2`。**在白底上像素完全相同**,而门诚实地红。这是刻意的偏差,记录在 SUMMARY 里。
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
@frontend/index.html
@scripts/check-01-token-conformance.sh
@scripts/check-02-contrast.py
@scripts/check-03-hidden-uniqueness.sh
@scripts/check-04-important-count.sh
@.planning/quick/260917-fqh-b9664e0-hidden-flex/260917-fqh-PLAN.md

**改动前基线(已实测,执行期先复跑确认再动手):**

```
bash scripts/check-01-token-conformance.sh        # PASS
./.venv/bin/python scripts/check-02-contrast.py   # PASS: 0 failures(34 pair + 1 ORDER)
bash scripts/check-03-hidden-uniqueness.sh        # PASS
bash scripts/check-04-important-count.sh          # PASS
grep -c 'var(--text-sm)'   frontend/style.css     # 6   (332/417/433/614/677/778)
grep -cE '^\s*box-shadow:' frontend/style.css     # 3   (376 卡片 / 701 划词菜单 / 725 冻结轮 inset)
grep -c 'right: 448px'     frontend/style.css     # 1
grep -c 'max-width: 720px' frontend/style.css     # 1
grep -c 'flex-wrap'        frontend/style.css     # 0
grep -c '/\* PAIR'         frontend/style.css     # 34
grep -c '/\* ORDER'        frontend/style.css     # 1
grep -n '^\.annotation-plain \.annotation-note'   frontend/style.css   # 669
grep -n '^\.annotation-answered \.annotation-note' frontend/style.css  # 852
```

**令牌引用完整性门(改动前后都应返回 0;这是"删了 --text-sm 却漏改消费者"的唯一机械防线):**

```bash
awk '/DESIGN TOKENS: START/{f=1;next} /DESIGN TOKENS: END/{f=0} f' frontend/style.css \
  | grep -oE 'var\(--[a-z0-9-]+\)' | sed -E 's/var\(--(.*)\)/\1/' | sort -u > /tmp/u.txt
awk '/DESIGN TOKENS: START/{f=1;next} /DESIGN TOKENS: END/{f=0} f' frontend/style.css \
  | grep -oE '^\s*--[a-z0-9-]+' | sed -E 's/.*--//' | sort -u > /tmp/d.txt
comm -23 /tmp/u.txt /tmp/d.txt | wc -l     # 必须为 0
```

**约束(项目 CLAUDE.md §2 简单优先 / §3 外科手术式改动):** 每一行改动都必须能追溯到上面的目标规格之一。不重排格式、不"顺手改进"相邻代码、不删除既存死代码(唯一的例外是本计划显式点名的 `--text-sm` / `--shadow-overlay` / `--shadow-menu`)、不引入构建步骤、不引入任何依赖。

**必须保持原样的既有结构(四条硬约束):**
1. `/* ===== DESIGN TOKENS: START ===== */` … `/* ===== DESIGN TOKENS: END ===== */` 围栏必须仍**恰好一对**;裸 `#hex` 只能出现在围栏内;tier-1 primitive 名(`--white/--black/--gray-*/--green-*/--blue-*/--amber-*/--red-*/--purple-*`)只能在围栏内被 `var()` 引用,围栏外只准引用 tier-2 `--color-*` 名。新配色值必须作为 tier-1 primitive 进围栏,再经 tier-2 语义名暴露给选择器。
2. `.hidden { display: none !important; }` 必须仍**恰好 1 条**;`!important;` 声明必须仍**恰好 1 个**。因此本次新增的任何注释散文里不得出现带分号的 `!important;` 字面量。
3. `--z-badge(10) < --z-banner(20) < --z-overlay(100) < --z-selection-menu(200)` 四条 z-index 令牌与断言不得改动。
4. 文件末尾的 `.annotation-answered` 规则组(注释写明「绝不插入、绝不重排(Global Hard Rule 3)」)必须保持在 `.annotation-plain .annotation-note` 之后,不得移动、不得插入任何规则到它与其前驱之间。

**语义动作色系的安全职责(不得被换肤吞掉):** `--color-action-danger/warning/routine/commit/irreversible` 五族的语义名必须全部保留;它们的底层值本次一律不动(green-700 / amber-800 / red-600 原样)。`#btn-authorize`(「授权撰写总设计文档」)是不可逆操作,它的颜色是安全信号——本次唯一被改动的动作色是 `--color-action-primary`(经 `--blue-700` 变成品牌蓝),它服务的是「发送」「同意」「放行」这类可逆操作。
</context>

<tasks>

<task type="tracer">
  <name>Task 1: 配色换血 + 助手消息去气泡(一条端到端可见切片)</name>
  <files>frontend/style.css</files>
  <action>
这是本计划的纵向切片:从 token fence 的 tier-1 值一路穿到屏幕上一条真实消息的呈现,证明"新配色 + 非对称气泡"这条链路端到端成立。后续 Task 2/3 只是在这条已跑通的链路上横向铺开。

**A. 在 token fence 内改写 tier-1 primitive 的值**(只改值,不改名,不增删 tier-1 名):

| tier-1 | 现值 | 目标值 | 依据 |
|---|---|---|---|
| `--gray-900` | `#1a1a1a` | `#0d0d0d` | 主文字 |
| `--gray-700` | `#555555` | `#8f8f8f` | 次要文字 |
| `--gray-600` | `#6a6a6a` | `#8f8f8f` | 次要文字(规格只给一档 #8f8f8f;两个语义角色各自保留,值相同) |
| `--gray-500` | `#8a8a8a` | `#d9d9d9` | 组件描边 rgba(0,0,0,.15) 的白底不透明等价 |
| `--gray-100` | `#eeeeee` | `#f2f2f2` | 分割线 rgba(0,0,0,.05) 的白底不透明等价 |
| `--gray-50` | `#f5f5f5` | `#f3f3f3` | 次级表面 |
| `--gray-25` | `#fafafa` | `#ffffff` | 表面 |
| `--blue-700` | `#1f63bd` | `#3a83f7` | 品牌蓝 |

其余 tier-1(`--white`、`--black`、`--gray-300`、`--blue-100`、`--blue-50`、`--green-*`、`--amber-*`、`--red-*`、`--purple-600`)**一律不动**。

**B. 新增一个 tier-1 primitive**,插在灰阶阶梯的正确位置上(`--gray-300` 与 `--gray-100` 之间,保持"数字越小越浅"的单调性):

| 新增 tier-1 | 值 | 依据 |
|---|---|---|
| `--gray-200` | `#ececec` | 用户气泡 |

**C. 新增一个 tier-2 语义名**(与唯一消费者同提交,Hard Rule 5):

| 新增 tier-2 | 值 |
|---|---|
| `--color-surface-user` | `var(--gray-200)` |

**D. 改写消息气泡两条规则**(style.css 现 530-552 行区段):

- `.chat-user`:背景改引 `var(--color-surface-user)`,前景由 `var(--color-text-inverse)`(白字)改引 `var(--color-text)`(深字);`align-self: flex-end` 与右下角小圆角保持不变。
- `.chat-ai`:规则体只保留 `align-self: flex-start;` 一条声明。背景、圆角、以及任何继承自 `.chat-bubble` 的内边距/宽度上限都必须在此覆盖掉。`.chat-bubble` 保留的 `padding` / `border-radius` / `max-width` 仍服务用户侧气泡,因此助手侧必须在 `.chat-ai` 里显式给出 `max-width: 100%`、`padding: 0`、`border-radius: 0`、`background: none`——四者缺一都会让助手消息继续带着盒子。`.chat-ai` 必须留在 `.chat-bubble` **之后**(同特异性 0-1-0,靠源码顺序取胜)。
- `.chat-ai.streaming-ai` 的左侧流式竖线(3px `--color-border-streaming`)保留不动——它是"正在流式"的状态信号,不是气泡语义。
- `.chat-ai p` / `.say-chunk p` 的段间距保留。

**E. 两条令牌因此失去消费者,但必须保持声明**:`--color-surface-info-strong` 与 `--color-text-inverse` 在 `.chat-user` 改引新令牌后不再被任何选择器消费,但 `check-02` 的清单里有 `PAIR --color-text-inverse ON --color-surface-info-strong TEXT` 一条**按名引用**它们——删掉声明会让脚本以 "unknown token" 提前 exit,偏差证据表就没了。因此两条声明原样保留,并在它们上方补一行注释说明"保留是为 CHECK-02 清单的按名引用"(注释里不得出现带分号的 `!important;`)。

**F. 不得触碰**:fence 内的 Contrast pair manifest 注释块(34 条 PAIR + 1 条 ORDER,一行都不许改、不许删、不许加);`scripts/check-01..04`;`.hidden` 规则;四条 `--z-*` 令牌。
  </action>
  <verify>
    <automated>cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh && git diff -U0 -- frontend/style.css > /tmp/plan-diff.txt && test "$(grep -cE '^[+-].*/\* (PAIR|ORDER)' /tmp/plan-diff.txt)" = 0 && test "$(awk '/^\.chat-ai \{/,/^\}/' frontend/style.css | grep -oE '(background|padding|max-width|border-radius|border-bottom-left-radius|border-top-left-radius):' | wc -l | tr -d ' ')" -ge 4 && test "$(grep -c 'var(--gray-200)' frontend/style.css)" -ge 1 && test "$(grep -c 'var(--color-surface-user)' frontend/style.css)" -ge 1 && test "$(git diff --name-only -- frontend scripts)" = "frontend/style.css" && echo TASK1-STRUCTURE-OK; ./.venv/bin/python scripts/check-02-contrast.py; echo "check-02 exit=$? (预期非 0)"</automated>
  </verify>
  <done>
    check-01 / check-03 / check-04 全部 PASS;fence 内 34 条 PAIR + 1 条 ORDER 一行未改;`.chat-ai` 规则体含 4 条覆盖声明(背景/内边距/圆角/宽度上限),且除 `align-self` 外无其它声明;`var(--gray-200)` 与 `var(--color-surface-user)` 各至少 1 处消费;`git diff --name-only -- frontend scripts` 只有 `frontend/style.css`;check-02 非 0 退出,且其输出里**没有** `unknown token` / `malformed` / `coverage` 字样。
  </done>
</task>

<task type="auto">
  <name>Task 2: 字号阶梯 + 行高配对 + 字重档 + 圆角刻度 + 影子收敛到一条</name>
  <files>frontend/style.css</files>
  <action>
**A. 字号阶梯:6 档收敛为 5 档(改值 + 删一个名 + 同步 6 个消费者)**

| tier-2 | 现值 | 目标值 | 规格档位 |
|---|---|---|---|
| `--text-xs` | 11px | 12px | 12px/16px 页脚、辅助 |
| `--text-sm` | 12px | **删除** | —(消费者改引 `--text-xs`,值不变,零视觉 delta) |
| `--text-base` | 13px | 14px | 14px/20px 界面 chrome、按钮 |
| `--text-md` | 14px | 16px | 16px/26px 消息正文(比界面文字松) |
| `--text-lg` | 15px | 18px | 18px/28px 章节标题 |
| `--text-xl` | 16px | 24px | 24px/32px 大标题 |

删除 `--text-sm` 的声明行,并把 6 个消费者(style.css 现 332、417、433、614、677、778 行)对该令牌的引用逐处改为 `--text-xs`。**这 6 处必须同批完成**——漏一处,那条已删令牌的引用解析为空、字号静默回落到继承值,而四条门禁一条都不会报。改完后围栏外不得残留任何指向已删令牌的引用。

**B. 行高:三种倍数改为四种,与字号配对**

| tier-2 | 现值 | 目标值 | 配对 |
|---|---|---|---|
| `--lh-tight` | 1.35 | 1.3333 | 24/32 与 12/16 |
| `--lh-snug` | (新增) | 1.4286 | 14/20 |
| `--lh-compact` | 1.6 | 1.5556 | 18/28 |
| `--lh-reading` | 1.75 | 1.625 | 16/26 |

**C. 字重:新增 500 档**

| tier-2 | 值 |
|---|---|
| `--fw-medium` | 500 |

(`--fw-regular` 400 / `--fw-semibold` 600 不动。v1.14 Phase 4 曾按 Q4 刻意不声明 500 档,理由是"没有消费者";本次目标阶梯明确要求 chrome 用 w400/500/600,该理由不再成立,故声明。)

**D. 圆角:3 值扩为 4 值**

| tier-2 | 现值 | 目标值 | 用途 |
|---|---|---|---|
| `--radius-sm` | 4px | 8px | 小按钮、chip、行内 code |
| `--radius-md` | 8px | 10px | 导航项、卡片、菜单、批注条目 |
| `--radius-lg` | (新增) | 28px | 输入框(composer);用户气泡 |
| `--radius-pill` | 999px | 999px | 徽标、胶囊按钮 |

**E. 影子收敛为全页唯一一条**

- 删除 tier-2 `--shadow-overlay` 与 `--shadow-menu` 两条声明。
- 同时删除它们的两处消费者(style.css 现 376 行 `.overlay-card`、现 701 行 `#selection-menu`,各有一条指向影子令牌的 box-shadow 声明)——留着就是悬空引用。
- 新增 tier-2 `--shadow-composer`,值恰为三层叠加:`rgba(0, 0, 0, 0.04) 0 0 0 1px, rgba(0, 0, 0, 0.04) 0 2px 8px 0, rgba(0, 0, 0, 0.024) 0 4px 80px 8px`。
- **不得触碰** `#round-doc.round-frozen` 的 `box-shadow: inset 3px 0 0 var(--color-action-warning);`(现 725 行)——它是冻结轮的结构标记(S-4),不是影子,它的存在是为了在不用 opacity 的前提下表达只读。它的上一行注释(现 722 行)同样保留。

**F. 消费端按新阶梯落位**(只改字号/行高/字重/圆角,不改其它属性):

- `#doc-pane` 的直接子 `<h1>`(index.html 的「文档区」)必须显式降级为视觉标签:14px 档 + `--fw-medium` + 次要文字色,不再以 UA 默认约 32px 粗体成为全屏最重的文字(VISUAL-03)。用 `#doc-pane > h1` 限定,不要写全局 `h1` 规则。
- `.markdown-body h1/h2/h3` 获得**显式**字号且**作用域限定在 `.markdown-body` 内**(TYPE-01):h1 → `--text-xl`(24px)、h2 → `--text-lg`(18px)、h3 → `--text-md`(16px),三级一律 `--fw-semibold`。**不得**写成全局 `h1, h2, h3` 规则——那会与四处 chrome 覆盖碰撞(`.panel-header h2`、`#draft-view h2`、`#brainstorm-view h2`、`.overlay-card h3`)。
- `.markdown-body` 正文行高改引 `--lh-reading`(现已是);`.markdown-body` 的 `code` 与 `table th/td` 继续用 `--text-base`(14px),在正文 16px 之下形成"正文 > 表格/代码"的既定层级(TYPE-02 的刻度归位)。
- `.panel-header h2` 改 `--text-base` + `--fw-medium`(导航项 14px w500,覆盖 `--text-md` 变成 16px 的连带效应)。
- `.overlay-card h3` 用 `--text-xl`(24px),`.overlay-card p` 用 `--text-md`(16px)+ `--lh-compact`。
- `.chat-bubble` 的字号由 `--text-base` 改引 `--text-md`(16px/26px 消息正文,行高 `--lh-compact` 或 `--lh-reading`,取 1.625)。
- `.hint` / `.inline-error` / 按钮 / 输入框 / 下拉 / `.event-item` / `.annotation-item` / `.verdict-card` 等 chrome 一律 `--text-base`(14px)。
- `button` 基础规则补 `font-weight: var(--fw-medium)`。
- `.annotation-badge` 保持 `--text-xs`(12px);`.tier-desc` 由 `--text-sm` 改 `--text-xs` 后值不变(仍 12px),其 `opacity: 0.9` **不得改动**(它是 Phase 4 刚修过 AA 的敏感点,不在本次范围)。
- 用户气泡的圆角改为 `--radius-lg`(28px),右下角仍保留 `--radius-sm` 的小圆角作为"尾巴"——沿用既有的右下角小圆角惯用法。

**G. 不得触碰**:fence 内的 PAIR/ORDER 注释块;`scripts/check-01..04`;`.hidden`;四条 `--z-*`;`.annotation-answered` 规则组;`#round-doc.round-frozen` 的 inset 标记。
  </action>
  <verify>
    <automated>cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh && test "$(grep -c 'var(--text-sm)' frontend/style.css)" = 0 && test "$(grep -cE '^\s*--text-sm:' frontend/style.css)" = 0 && test "$(grep -c 'var(--shadow-overlay)\|var(--shadow-menu)' frontend/style.css)" = 0 && test "$(grep -cE '^\s*box-shadow: var\(--shadow' frontend/style.css)" -ge 1 && grep -q 'inset 3px 0 0 var(--color-action-warning)' frontend/style.css && git diff -U0 -- frontend/style.css > /tmp/plan-diff.txt && test "$(grep -cE '^[+-].*/\* (PAIR|ORDER)' /tmp/plan-diff.txt)" = 0 && test "$(grep -c 'var(--text-xs)' frontend/style.css)" -ge 7 && test "$(git diff --name-only -- frontend scripts)" = "frontend/style.css" && echo TASK2-STRUCTURE-OK; ./.venv/bin/python scripts/check-02-contrast.py; echo "check-02 exit=$? (预期非 0)"</automated>
  </verify>
  <done>
    check-01 / check-03 / check-04 PASS;`--text-sm` 的声明与 6 处引用全部消失,`--text-xs` 引用数 7(6 处迁移 + 原 `.annotation-badge`);`--shadow-overlay` / `--shadow-menu` 的声明与两处消费者全部消失,`box-shadow: var(--shadow-*)` 全文件恰好 1 条(输入框);冻结轮 inset 标记 1 条未动;fence 内 34 条 PAIR 未改;`git diff --name-only -- frontend scripts` 只有 `frontend/style.css`;check-02 非 0 退出。
  </done>
</task>

<task type="auto">
  <name>Task 3: 侧栏几何(260px)+ 导航项 + 输入框 + 内容列 768 + 减描边 + 全量门禁与偏差取证</name>
  <files>frontend/style.css</files>
  <action>
**A. 侧栏收窄到 260px,并处理三处连带后果**

- `--sidebar-w`:420px → **260px**。
- `#sidebar` 增加 `padding: var(--space-1-5)`(6px)与 `gap: var(--space-1-5)`(6px)。因全局 `box-sizing: border-box`,导航项可用宽度恰为 260 − 12 = **248px**,与规格一致。
- **连带后果一(LAYOUT-01,必须与侧栏宽度同一工作单元落定):** `#state-badge` 的右边距现在是写死的魔法数 448px(现 412 行,注释写「侧栏 420px + 呼吸空隙」)。改为 `right: calc(var(--sidebar-w) + var(--space-6));`(260 + 24 = 284px),并把该行注释改成陈述新关系。漏掉这一处,徽标会压在侧栏上。
- **连带后果二:** `#probe-controls` 现有 5 个横向控件(路线下拉 / 路径输入 / 发起测试调用 / 处理本轮批注 / 中止)在 248px 内不可能单行排下。加 `flex-wrap: wrap;` 让它们换行,消除横向溢出。**这是 260px 决策的必然结果,不是 `#probe-controls` 的重做**——不删控件、不重排控件、不改产品行为(STATE.md 已裁定 `#probe-controls` 的移除/重定位不进任何阶段)。
- **连带后果三:** `#doc-pane` 的 `border-right` 保留,但它的值经 Task 1 后已变为 `--color-border-subtle`(#f2f2f2)——两个窗格同为白底时这条分隔线是耳语级的。**这是刻意的**(ChatGPT 自身的侧栏/主区差异同样是耳语级),不要为了"看得见"把它换成 `--color-border-strong`。

**B. 导航项几何(四个 `.panel-header`)**

- `height: 36px`;`padding: var(--space-1-5) var(--space-2-5)`(6px 10px);`border-radius: var(--radius-md)`(10px)。
- **删除**下边界那条 1px hairline 与 sunken 背景色(减描边的核心动作:侧栏四段不再靠分隔线与色块区分,改靠 36px 的行高节奏与 6px 的段间距)。
- 字号 `--text-base` + `--fw-medium`(14px w500)。
- `.collapse-indicator` 的图标尺寸设为 20px(`font-size: 20px; line-height: 1;`)。
- 各 `.panel-header` 的 `cursor` 声明保持原样(`#ai-panel-header` 可折叠故为 pointer,其余三个为 default)。
- **不加 hover 态**——三个不可点的面板头若有 hover 会给出错误的可点暗示(INTERACT-01 不在本计划范围)。
- `.panel-body` 的 padding 由 `12px 16px` 改 `var(--space-2-5)`(10px),与导航项的水平内缩对齐。

**C. 输入框(composer):28px 圆角 + 52px 高 + 全页唯一的影子**

- `#chat-input-row input`:新增 `min-height: 52px;`、`border-radius: var(--radius-lg);`、`padding: 7px 10px;`(即 `var(--space-1-5) var(--space-2-5)`)、`box-shadow: var(--shadow-composer);`;字号 `--text-md`(16px,与消息正文同级)。
- `#chat-input-row button`:圆角改 `--radius-pill`(999px 胶囊),字号 `--text-base`,字重 `--fw-medium`。
- **规格里"输入框 768×52"的 768 不适用,记录为刻意偏差**:768px 是 ChatGPT 居中 composer 的宽度属性;本工具的 composer 落在 260px 侧栏内,宽度由容器决定,只有高度 52 / 圆角 28 / 内边距 7px 10px / 三层影子被照搬。

**D. 内容列 768px**

- `.markdown-body` 的 `max-width: 720px;`(现 446 行)→ `max-width: 768px;`。**保持左对齐,不要 `margin-inline: auto`**——`#doc-pane` 的其它子元素(进入表单、认可按钮行、发散产物区)不在 `.markdown-body` 内,只给 markdown 列居中会让同一窗格里的内容左右不齐。

**E. 减描边(其余站点)**

- `#annotations-panel` 与 `#checks-panel` 的上边界分段线(各一条 1px hairline)删除(它们与 `#session-panel` 的分隔已由 `#sidebar` 的 6px `gap` 承担)。
- `.event-list`、`#latest-check`、`.annotation-item`、`.verdict-card`、`#brainstorm-view`、`#selection-menu` 的描边保留(它们是内容容器,不是分段线);其值经 Task 1 后自动变为新的 hairline / 组件描边值,无需逐条改。
- `.overlay-card` 的阴影已在 Task 2 删除;它的 `border-radius` 经 `--radius-md` 自动变为 10px。模态卡片在深色遮罩(`--color-overlay-backdrop`)上仍有边界,不必补边框。

**F. 全量门禁与偏差取证(本任务的核心交付物)**

依次跑四条门禁并**原样抄录** check-02 的完整输出:

1. `bash scripts/check-01-token-conformance.sh` → 必须 PASS
2. `bash scripts/check-03-hidden-uniqueness.sh` → 必须 PASS
3. `bash scripts/check-04-important-count.sh` → 必须 PASS
4. `./.venv/bin/python scripts/check-02-contrast.py` → **必须 FAIL**。用 `./.venv/bin/python`(项目 venv),**不得**用 bash 调用它、也不得用环境 `python3`(环境 python3 是 miniconda,会给出与项目 venv 不同的结果)。把完整输出重定向到 `/tmp/check02-after.txt` 留档。

在 SUMMARY.md 里建一张偏差证据表,逐条列出 check-02 的每个 FAIL 行:令牌对名、实测 ratio、阈值。表下另起一段标注**哪些 FAIL 对应真实渲染、哪些是清单陈旧**——`PAIR --color-text-inverse ON --color-surface-info-strong` 的消费者(`.chat-user`)在 Task 1 后已改引新令牌,这一条 FAIL 是清单按名引用留下的陈旧项,不对应任何屏上像素;其余失败(次要文字四对、chip 前景、品牌蓝前景、组件描边两对等)都对应真实渲染,是用户知情接受的 AA 倒退。同时记录失败条目总数与 check-02 的退出码。

再跑一遍令牌引用完整性门(见 `<context>`)确认返回 0,以及 `git diff --stat` 确认只有 `frontend/style.css` 一个文件。

**G. 人工验收清单(写进 SUMMARY,标注 pending,不得声称已验证)**

前端 CSS 无 pytest 覆盖(Nyquist 缺口),以下必须在本地起服务后用真实浏览器逐条确认:

1. 助手长回答(含列表 / 代码块 / 多级标题)无背景、无内边距、占满侧栏宽度;用户消息为右侧浅灰气泡、深色文字。两者交替出现时视觉上不对称。
2. 侧栏 260px 下 `#probe-controls` 换行后无横向溢出、无控件被裁切;`#state-badge` 落在文档区右上角、不压侧栏。
3. 长文档阅读列 768px 左对齐;`#doc-pane` 里其它元素与 markdown 列左边缘对齐。
4. 输入框 52px 高、28px 圆角、三层影子;全页其它元素(模态卡片、划词菜单)无影子仍可辨。
5. 「文档区」标题是安静的小标签,不再是全屏最大最重的文字;模态标题(24px)是全页最大的文字。
6. **安全信号回归:`#btn-authorize`(授权撰写总设计文档)仍是绿色系、与「发送」「同意」「放行」等品牌蓝按钮以及中性例行按钮可区分**——本次换肤不得把不可逆动作的安全信号吞掉。
7. 冻结轮仍是"去饱和 + 左侧琥珀 inset 竖线",且该 inset 标记未被误当成影子删掉。
8. 已回应批注条目仍是弱化的灰字(源码顺序未被破坏)。
  </action>
  <verify>
    <automated>cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh && test "$(grep -c 'right: 448px' frontend/style.css)" = 0 && test "$(grep -c 'var(--sidebar-w)' frontend/style.css)" -ge 2 && test "$(grep -c 'flex-wrap' frontend/style.css)" = 1 && test "$(grep -c 'max-width: 768px' frontend/style.css)" = 1 && test "$(grep -c 'border-top: 1px solid var(--color-border-subtle)' frontend/style.css)" = 0 && test "$(grep -c 'border-bottom: 1px solid var(--color-border-subtle)' frontend/style.css)" = 0 && test "$(awk '/^\.panel-header \{/,/^\}/' frontend/style.css | grep -c 'height: 36px')" = 1 && git diff -U0 -- frontend/style.css > /tmp/plan-diff.txt && test "$(grep -cE '^[+-].*/\* (PAIR|ORDER)' /tmp/plan-diff.txt)" = 0 && test "$(awk '/DESIGN TOKENS: START/{f=1;next} /DESIGN TOKENS: END/{f=0} f' frontend/style.css | grep -oE 'var\(--[a-z0-9-]+\)' | sed -E 's/var\(--(.*)\)/\1/' | sort -u > /tmp/u.txt; awk '/DESIGN TOKENS: START/{f=1;next} /DESIGN TOKENS: END/{f=0} f' frontend/style.css | grep -oE '^\s*--[a-z0-9-]+' | sed -E 's/.*--//' | sort -u > /tmp/d.txt; comm -23 /tmp/u.txt /tmp/d.txt | wc -l | tr -d ' ')" = 0 && test "$(git diff --name-only -- frontend scripts)" = "frontend/style.css" && echo TASK3-STRUCTURE-OK; ./.venv/bin/python scripts/check-02-contrast.py > /tmp/check02-after.txt 2>&1; echo "check-02 exit=$? (预期非 0)"; grep -c '^FAIL ' /tmp/check02-after.txt; grep -cE 'unknown token|malformed|coverage below floor' /tmp/check02-after.txt</automated>
  </verify>
  <done>
    check-01 / check-03 / check-04 PASS;`right: 448px` 魔法数消失,`var(--sidebar-w)` 恰 2 处消费;`flex-wrap` 1 处;`max-width: 768px` 1 处;`.panel-header` 与 `#annotations-panel` / `#checks-panel` 的 border-top/bottom 分段线全部消失;`.panel-header` 规则体含 `height: 36px`;令牌引用完整性门返回 0;`git diff --name-only -- frontend scripts` 只有 `frontend/style.css`;check-02 非 0 退出,`/tmp/check02-after.txt` 里的 FAIL 行全部是「对比度低于阈值」形态,`unknown token|malformed|coverage below floor` 命中数为 0,失败条目数与原样输出已抄进 SUMMARY。
  </done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 无 | 本计划是纯静态 CSS 值改写:无网络请求、无用户输入进入样式层、无新增依赖、无 JS/HTML 改动。所有新增值都是围栏内的字面量常量。 |
| 语义色 → 用户对"不可逆操作"的判断 | `--color-action-irreversible` 是「授权撰写总设计文档」这一不可逆动作的安全信号;换肤若把它做成与可逆动作同色,等于移除一道人工防线。 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-260918-01 | Tampering | `--color-action-irreversible*` / `#btn-authorize`(style.css 现 734-741 行) | medium | mitigate | 五族语义动作名(`danger`/`warning`/`routine`/`commit`/`irreversible`)全部保留且底层值一律不动;本次唯一改动的动作色是 `--color-action-primary`(经 `--blue-700`),它只服务可逆操作。Task 3 人工验收第 6 条专门回归此点。 |
| T-260918-02 | Tampering | `--color-text-muted` / `--color-text-secondary`(次要文字) | low | accept | 次要文字对比度由约 5.41:1 降到约 3.23:1,低于 WCAG AA 4.5:1。这是**用户知情决策**:实测数字已呈上,用户选择完整照搬 ChatGPT 视觉语言。偏差由 check-02 的 FAIL 输出机器化留证,不静默。 |
| T-260918-03 | Information disclosure | 本次 diff 全为 CSS 字面量常量 | low | accept | 无凭据、无端点、无用户数据进入样式层;无新增网络面。 |
| T-260918-04 | Denial of service | `#state-badge` 的 `right: calc(var(--sidebar-w) + var(--space-6))` | low | mitigate | 若 `--sidebar-w` 未声明,`calc()` 整条失效、徽标回落到 `right: auto`。Task 3 的门断言 `var(--sidebar-w)` 恰 2 处消费,配合令牌引用完整性门(返回 0)保证名字不悬空。 |
| T-260918-SC | Tampering | 依赖安装(npm / pip / cargo) | high | mitigate | **本计划不安装任何依赖**:零新增包、零构建步骤、零 CDN。若执行期出现"顺手引入一个 CSS 框架/图标库"的念头,即为违反本计划,立即停止。 |
</threat_model>

<verification>
**四门(逐任务跑,Task 3 为最终收口):**

```bash
bash scripts/check-01-token-conformance.sh         # PASS —— 围栏外零裸 hex、零 tier-1 泄漏
bash scripts/check-03-hidden-uniqueness.sh         # PASS —— .hidden 规则恰 1 条
bash scripts/check-04-important-count.sh           # PASS —— !important; 声明恰 1 个
./.venv/bin/python scripts/check-02-contrast.py    # FAIL(预期)—— 必须用项目 venv 解释器
```

**check-02 的失败方向必须被"证明"而不是被"假设":** 失败行全部是 `FAIL  <ratio>  <pair>  (need >= <threshold>)` 形态;`unknown token` / `malformed manifest entry` / `coverage ... below floor` 三种提前退出形态命中数必须为 0。若出现后三种,说明令牌名被删或清单被改,偏差证据表已失效,必须回退到"只改值、不删被清单按名引用的令牌名"。

**结构性断言(见各 task 的 `<automated>`):**

- 围栏恰一对 START/END;`/* PAIR` = 34、`/* ORDER` = 1(与改动前逐字一致)
- 令牌引用完整性:围栏外引用的每个 `var(--x)` 都在围栏内有 `--x:` 声明(返回 0)
- `--text-sm` 的声明与引用全文件为 0;`--text-xs` 引用为 7
- `box-shadow: var(--shadow-*)` 全文件恰 1 条;冻结轮 `inset 3px 0 0 var(--color-action-warning)` 恰 1 条
- `right: 448px` 为 0;`var(--sidebar-w)` 为 2;`max-width: 768px` 为 1;`flex-wrap` 为 1
- `.annotation-answered .annotation-note` 的行号 > `.annotation-plain .annotation-note` 的行号(源码顺序承重,改动前 852 > 669)
- `git diff --name-only -- frontend scripts` 输出恰为 `frontend/style.css`(零 JS / 零 HTML / 零脚本改动;注意不能用裸 `git diff --name-only`——工作树里另有 `.claude/settings.local.json` 与 `.planning/state.json` 的既存改动,裸命令会污染这条断言)

**门算术陷阱(不得简化):** `grep -c 'box-shadow' frontend/style.css` 会命中一行**注释散文**(现 722 行),基线返回 4 而真实声明是 3。一律用 `grep -cE '^\s*box-shadow:'`(基线 3 → 目标 2:输入框 + 冻结轮 inset)。同理 `grep -c '!important'` 返回 3(两行注释散文),声明门必须用带分号的 `grep -o '!important;' | wc -l`。

**人工验收:** 见 Task 3 的 8 条清单,写入 SUMMARY 并标注 `pending`。前端 CSS 无自动化覆盖,这 8 条是 Nyquist 缺口的显式补偿;**未逐条跑过之前不得声称任何视觉结论成立**。

**已知设计张力(交付时必须如实记录,不得静默):** 助手消息改为全宽裸排后,它的可用宽度就是 248px(260px 侧栏 − 12px 内边距)。用户去气泡的动机是"长文塞进窄盒子损害阅读体验",去气泡确实移除了背景/内边距/宽度上限这三重损耗,但**列宽本身仍只有 248px**。若人工验收判定 248px 的阅读列不可接受,唯一的一值回退是 `--sidebar-w`(例如 320px),不需要任何结构性返工——因为 `#state-badge` 已改为 `calc()`、`#probe-controls` 已可换行,宽度不再是耦合点。这条张力必须在 SUMMARY 里写明,交由用户裁决,不得由执行器自行改宽度。
</verification>

<success_criteria>
- 用户拍板的目标规格逐项落地:配色 8 值(3 主色 + 2 描边等价色 + 次级表面 + 用户气泡 + 品牌蓝)、字号 5 档、行高 4 倍率、字重 3 档、圆角 4 值、影子 1 条三层叠加、侧栏 260px、导航项 248×36 圆角 10px 内边距 6px 10px 图标 20px、输入框 52px 高圆角 28px 内边距 7px 10px、内容列 768px。
- 助手消息去气泡:`.chat-ai` 规则体只承载定位,背景/内边距/圆角/宽度上限四者全部覆盖掉;用户消息保留浅灰气泡 + 深色文字。
- 令牌分类学零破坏:围栏恰一对、围栏外零裸 hex、零 tier-1 引用、围栏外引用的每个令牌名都在围栏内声明。
- 三条硬约束零破坏:`.hidden` 恰 1 条、`!important;` 恰 1 个、`.annotation-answered` 规则组仍在其前驱规则之后且未移动。
- 四个 `--z-*` 令牌与断言未动;五族语义动作色名全部保留且底层值未动。
- 改动严格限于 `frontend/style.css`:`git diff --name-only` 无第二个文件;`scripts/check-01..04` 与 `frontend/app.js` / `frontend/index.html` 零改动。
- check-01 / check-03 / check-04 PASS;check-02 红着交出,失败条目数与每条数值逐条抄进 SUMMARY,并标注哪些对应真实渲染、哪些是清单陈旧项。
- 三条刻意偏差被显式记录而非静默:① 两个"透明度描边"用白底不透明等价色(理由:check-02 不对背景令牌做 alpha 合成,字面 rgba 会造出 6.49 的假 PASS);② 输入框宽度不照搬 768px(容器是 260px 侧栏);③ `--gray-600` 与 `--gray-700` 同值 #8f8f8f(规格只给一档次要文字色,两个语义角色各自保留)。
- 人工验收 8 条清单写入 SUMMARY 且标注 `pending`;248px 阅读列的张力如实记录并交由用户裁决。
- 零新增依赖、零构建步骤、零 JS/HTML 改动、零新增门禁脚本。
</success_criteria>

<output>
Create `.planning/quick/260918-qrq-frontend-chatgpt/260918-qrq-SUMMARY.md` when done
</output>
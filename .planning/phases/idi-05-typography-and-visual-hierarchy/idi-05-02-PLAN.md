---
phase: idi-05-typography-and-visual-hierarchy
plan: 02
type: execute
wave: 2
depends_on:
  - idi-05-01
files_modified:
  - frontend/style.css
  - scripts/check-05-ui-uat.py
autonomous: true
requirements:
  - VISUAL-01
  - VISUAL-02
  - VISUAL-03

estimate:
  tokens: 50000
  raw_tokens: 50000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- lifted from idi-05-UI-SPEC.md `## UI Considerations` — explicit tier (4 of 22; E3 + E8) ----
    - "E3 六只动作按钮的 loading 关联态由 app.js 既有句柄驱动;本阶段 app.js / index.html 零 diff,故态的结构、文案与显隐不可能改变 —— 本阶段只改 font-weight / font-size / 填充形态 ← UI-SPEC UI-Considerations E3 `loading`(explicit)"
    - "E3 六只动作按钮的 error 态:`.disabled` 伪类是 G3 前提条件唯一的视觉信号(Pitfall M5),D-14 裁定沿用 opacity 0.55 零改动,错误态不可被本阶段改动 ← UI-SPEC UI-Considerations E3 `error`(explicit)"
    - "E8 `#doc-panel-header h1` 的 loading 态:容器标签的显隐由 `#doc-panel` 的既有折叠行为驱动,本阶段零改动;VISUAL-03 只做复证(D-19,零 CSS 改动)← UI-SPEC UI-Considerations E8 `loading`(explicit)"
    - "E8 `#doc-panel-header h1` 的 error 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E8 `error`(explicit)"
    # ---- lifted from idi-05-UI-SPEC.md `## UI Considerations` — backstop tier (4 of 18) ----
    - statement: "E3 `#btn-continue-check` 与 `#btn-continue-repair` 在 `#check-controls`(flex-direction: column)里各占一行,不溢出。"
      verification: backstop
    - statement: "E3 `#btn-authorize` 文本「授权撰写总设计文档」在 `--doc-panel-w` 最窄值 340px(内容宽 260px)下不换行、不裁切,且 16px 白字在 green-12 上可读(12.32)。换行半边无自动化证据,需实测。"
      verification: backstop
    - statement: "E8 `#doc-panel-header h1`「文档区」在面板收起态(48px 竖条)下不裁切、不换行。"
      verification: backstop
    - statement: "E8 `#doc-panel-header h1` 的 14px / 500「安静标签」定位在实测中成立,不因本阶段标题改动而变成全屏最大最重的文字(SC3)。"
      verification: backstop
    # ---- phase-specific truths ----
    - "三段坡道落地为纯值改动,选择器结构一字未动:routine 三只(`#btn-process-round` / `#btn-continue-check` / `#btn-continue-repair`)仍是淡底绿字;commit 两只(`#btn-approve-draft` / `#btn-start-writing`)变为实心填充 + 白字;irreversible(`#btn-authorize`)变为实心更深 + 白字 ← VISUAL-01 / VISUAL-02 / D-11"
    - "两个填充步取 green-11 / green-12,不是契约与围栏注释预告的 green-9 / green-10 —— white on green-9 = 3.16 ✗、green-10 = 3.55 ✗,green-11 = 4.72 ✓ 是该族最浅的通过步、green-12 = 12.32 是最深步;因此 **Phase 5 新增 tier-1 primitive = 0** ← D-11 的委派 / 04.1 的算术 / S-7 / A-3"
    - "`--color-action-commit-fg ON --color-action-commit-surface` 实测 4.72(HEAD 11.00);`--color-action-irreversible-fg ON --color-action-irreversible-surface` 实测 12.32(HEAD 11.00);`--color-action-routine-fg ON --color-action-routine-surface` 仍 11.00 ← CHECK-02 / UI-SPEC §实测表"
    - "`--color-action-commit ON --color-surface` 实测 4.48、`--color-action-irreversible ON --color-surface` 实测 11.70,两条 NON-TEXT 配对(阈值 3:1)进清单 ← CHECK-02 / SC 1.4.11"
    - "清单规模 43 → **45 对(34 TEXT + 11 NON-TEXT)+ 1 ORDER**,`PASS: 0 failures`,exit 0;`ORDER 0.363` 不变(两个操作数 `--color-text-muted` / `--color-text` 本阶段未改值)← CHECK-02"
    - "围栏 L42-45 的「Phase 5 declares the 9/10 fill steps together with their consumers」已改写为「Phase 5 复用已声明的 11/12 步,理由见本围栏的 role-band 记录」;前三行(D-04 / Hard Rule 5 的声明纪律)逐字保留 ← A-4"
    - "围栏清单注释 L311 的「three families, one value」已改写 —— 三族从此有三个不同的值对,一条解释清单的注释在前提消失后必须改,否则它会开始说谎 ← 04.1-N-8 同源"
    - "五处 `:disabled` 的 `opacity: 0.55`(L656 / L884 / L935 / L947 / L1005-1008)逐字节未动 —— 对实心按钮而言 0.55 是**更强的**淡化,区分度反而上升 ← D-14 / Pitfall M5"
    - "`#btn-authorize` 新增一条 `font-size: var(--text-md)`(16px,现有档,零新增令牌),**不加 padding 步进**;padding 仍为 `var(--space-2) var(--space-4)` ← D-13"
    - "`#btn-authorize` 的 `font-weight` 保持 `var(--fw-semibold)`(600),是 D-09「按钮统一 500」的唯一已登记例外 ← D-12"
    - "`--color-action-irreversible*` 仍**只**被 `#btn-authorize` 消费,永不出现第二个消费者;三族名未改(`commit` 而非 `gate`)← D-15"
    - "运行时:D-04 的反转断言成立 —— routine 三只三属性逐字节相同、commit 两只三属性逐字节相同、三档两两不同;`#btn-authorize` 的 computed `font-size` == `--text-md`、`font-weight` == `600` ← 硬规则 7 / D-04 / D-12 / D-13"
    - "VISUAL-03 复证成立:`#doc-panel-header h1` 仍为 14px / `--fw-medium` 500 / `--color-text-secondary`,**零 CSS 改动**;`#doc-pane > h1` 这个选择器在 `frontend/index.html` 与 `frontend/style.css` 里都不存在(契约文本的漂移,门的选择器名已更正)← D-19 / D-01"
    - "页面级层级链成立(SC3):文档 h1 28px > `.overlay-card h3` 24px > 文档 h2 22px > `#doc-panel-header h1` 14px/500 —— 全屏最大最重的文字不再是容器标签「文档区」← VISUAL-03 / SC3 / D-19"

  artifacts:
    - path: "frontend/style.css"
      provides: "围栏内五处 tier-2 值改动(`--color-action-commit-surface` → `--radix-green-11`、`--color-action-commit-fg` → `--white`、`--color-action-irreversible` → `--radix-green-12`、`--color-action-irreversible-surface` → `--radix-green-12`、`--color-action-irreversible-fg` → `--white`);清单新增 2 条 NON-TEXT 配对;围栏注释 L42-45 与 L311 重写;`#btn-authorize` 规则新增 `font-size: var(--text-md);`"
      contains: "--color-action-commit-surface: var(--radix-green-11);"
    - path: "scripts/check-05-ui-uat.py"
      provides: "`:689-695` 的三属性逐字节相同断言反转为「档内相同 + 三档两两不同」;新增 `#btn-authorize` font-size / font-weight 断言;新增 `#doc-panel-header h1` 字面 14px/500 守卫;新增页面级层级链断言;新增 `trio()` 读取器与 ROUTINE / COMMIT / IRREVERSIBLE 三个选择器常量"
      contains: "def item3"

  key_links:
    - from: "围栏内 `--color-action-commit-surface` / `--color-action-irreversible-surface`"
      to: "`#btn-approve-draft` / `#btn-start-writing` / `#btn-authorize` 的 `background`"
      via: "选择器结构一字未动的纯值改动 —— Phase 4 把契约放在最前面的全部理由"
      pattern: "--color-action-commit-surface: var\\(--radix-green-11\\);"
    - from: "三族的三个令牌值对"
      to: "check-02 的 TEXT / NON-TEXT 配对"
      via: "值的唯一仲裁者是 scripts/check-02-contrast.py,上游文档的 AA 论断一律不采信"
      pattern: "PAIR --color-action-commit ON --color-surface NON-TEXT"
    - from: "`#btn-authorize` 与五只按钮的计算样式"
      to: "check-05-ui-uat.py 的 D-04 反转断言"
      via: "getComputedStyle 对 display: none 子树仍返回解析后的 color / background-color / border-color,故一个 p3 样本足够"
      pattern: "len\\(\\{trio\\(page, s\\) for s in ROUTINE\\}\\) == 1"

  prohibitions:
    - statement: "不得抹平三段坡道的形态差异 —— `#btn-authorize` 必须与五只例行/承诺按钮在计算样式上不同。这是核心价值(未经用户明确授权,流程绝不进入撰写总设计文档)在视觉层的机器可读形态;D-04 的「三档两两不同 + 档内相同」断言是该红线的可执行形态,档内相同那一半同样承重(它能抓到「改错了一只」)"
      status: active
      verification: flagged
    - statement: "不得为了拉大余量把 commit 的填充退到 green-12,或把白字改回绿字 —— 前者会让 commit 与 irreversible 同色,「实心更深」的语义当场失效;后者会退回淡底形态。唯一允许的动作是把两条配对逐字抄进验收命令(05-N-3)"
      status: active
      verification: flagged
    - statement: "不得给 `--color-action-irreversible*` 增加第二个消费者 —— 它永远只被 `#btn-authorize` 消费。本计划改的是它的**值**,不是它的消费者集合;这两件事必须分别核对(D-15)"
      status: active
      verification: flagged
    - statement: "不得给 `#btn-authorize` 加 padding 步进 —— D-13 明写只改 `font-size`;padding 保持 `var(--space-2) var(--space-4)`(窄面板 340px 下内容宽 260px > 176px,不换行正是靠这个算术成立的)"
      status: active
      verification: flagged
    - statement: "不得把 `check-05-ui-uat.py` 的第二类守卫(`.panel-header h2` 14px / `#draft-view h2` 18px / `.overlay-card h3` 24px / `.markdown-body` 16px / `.markdown-body code` 14px / `--text-base` 14px)改成令牌接线表述 —— 字面值是**特性而非缺陷**,它是唯一能抓到「标题改动溢出到 chrome」的形态(D-03)"
      status: active
      verification: flagged
    - statement: "不得改 `#btn-divergence` 的字重 —— 它是 `--color-action-warning` 族的发散入口,不在六个动作按钮之列;拉进来会在三段坡道之外造出一个未登记的第四档(TYPE-03 / UI-SPEC §TYPE-03)"
      status: active
      verification: flagged
    - statement: "不得软化五处 `:disabled` 的 `opacity: 0.55` —— 对实心按钮而言它是更强的淡化;「为了让实心按钮的禁用态更好看」而调这个值是 Pitfall M5 点名的行为(D-14)"
      status: active
      verification: flagged

  assumptions:
    # ---- edge probe fallback ($COVERAGE): 4 rows for this plan's requirement IDs, ALL unresolved ----
    - statement: "VISUAL-01 的边缘面未经探针确认(probe 返回 `unclassified — review manually`):不可逆档的四个强调通道(形态 / 色深 / 字号 / 字重)在极端渲染条件下(缩放、字体回退、窄面板)是否仍可区分?本计划按 D-11 / D-12 / D-13 的定稿执行,并把该行记为 flagged assumption。"
      status: unresolved
      verification: flagged
    - statement: "VISUAL-02 的边界面未经探针确认(probe 返回 boundary 探针 `What happens exactly at each min/max/threshold — and one step either side?`):commit 档的 4.72 距 4.5 阈值只有 0.22 余量、`--color-marker-active` 的 4.65 只有 0.15 余量 —— 任何值的舍入或合成路径变化都可能翻转判定。本计划以 `check-02` 的闭区间实测为唯一仲裁,并把该行记为 flagged assumption。"
      status: unresolved
      verification: flagged
    - statement: "VISUAL-02 的精度面未经探针确认(probe 返回 precision 探针 `Where can precision loss, overflow, or rounding/tie-breaking occur — and what is the exact contract?`):`check-02` 用 8-bit sRGB 合成 + 闭区间比较(4.496 失败 / 4.504 通过),不 round 到阈值;浏览器侧 `getComputedStyle` 的 `rgb()` 序列化与脚本侧的 hex 解析必须落在同一模型上。本计划不引入任何新模型,并把该行记为 flagged assumption。"
      status: unresolved
      verification: flagged
    - statement: "VISUAL-03 的边缘面未经探针确认(probe 返回 `unclassified — review manually`):「页面级层级」除了字号大小序之外,是否还有别的可机械核的判据(字重、色值、视觉重量)?本计划以「28 > 24 > 22 > 14/500」这条链 + 一条 `#doc-panel-header h1` 字面守卫举证,并把该行记为 flagged assumption。"
      status: unresolved
      verification: flagged
---

<!-- planner-discipline-allow: opacity: 0.55 -->
<!-- `opacity: 0.55` 是承重的:本计划的核心禁令之一是「不得软化五处 :disabled 的 opacity」,
     执行器必须知道守的是哪一个值,而验收对源文件做出现次数计数来证明它逐字节未动。 -->

<objective>
把不可逆的 G3 授权从例行按钮里在视觉上分离出来(三段坡道),并复证 VISUAL-03 的页面级层级。

Purpose: 这是本里程碑的核心价值修复。工具目前在对自己说谎 —— `#btn-authorize` 与例行「继续自检」在样式上**逐字节相同**(HEAD 的三族共用一组 `green-3 / green-11 / green-12`),而 G3 授权是产品最重要且唯一不可逆的一步。Phase 4 把三个 `--color-action-*` 族名与消费者结构一次性铺好,并在围栏注释里写明「visual differentiation is Phase 5's one-line value edit」;本计划兑现那句话。VISUAL-03 则相反:它**已由 qrq 实现**(`#doc-panel-header h1` 已是 14px / 500 / `--color-text-secondary`),本计划只做复证并把门的选择器名从契约漂移的 `#doc-pane > h1` 更正为 `#doc-panel-header h1`(D-19),零 CSS 改动。

Output: 三段坡道(淡底 / 实心 / 实心更深 + 更大 + 更重);`check-02` 在 **45 对**清单上 `PASS: 0 failures`(`--color-action-commit-fg ON --color-action-commit-surface` = 4.72、`--color-action-irreversible-fg ON --color-action-irreversible-surface` = 12.32);D-04 的反转断言(三档两两不同 + 档内相同);页面级层级链的运行时断言。

**D-11 委派给规划期的两项取值,本计划定稿(必须逐字照抄):**
- **commit 档**(`#btn-approve-draft` / `#btn-start-writing`):`--color-action-commit-surface` = `var(--radix-green-11)`、`--color-action-commit-fg` = `var(--white)`;`--color-action-commit` 保持 `var(--radix-green-11)`(边框与填充同色)。
- **irreversible 档**(`#btn-authorize`):`--color-action-irreversible` = `var(--radix-green-12)`、`--color-action-irreversible-surface` = `var(--radix-green-12)`、`--color-action-irreversible-fg` = `var(--white)`。
- **routine 档**(三只)值**一字未动**。

**为什么不是契约与围栏注释预告的 green-9 / green-10(S-7 / A-3):** 围栏内已记录的实测是 white on green-9 = **3.16 ✗**、green-10 = **3.55 ✗**、green-11 = **4.72 ✓**、green-12 = **12.32 ✓**。「step 9 = 实心填充 + 白字」是 Radix 的规范用法,但在本项目的每一族上都过不了 4.5:1。green-11 是该族**最浅的通过步**(已签核的 Pitfall 4a 规则应用在填充上而非文字上),green-12 是最深步 —— 11 与 12 是唯一同时满足「commit 取较浅的通过步 / irreversible 取最深步」的分配。**连带结论:Phase 5 新增 tier-1 primitive = 0**,围栏 L42-45 的那句预告因此变成假话,必须重写。

**本计划关闭的需求:** VISUAL-01、VISUAL-02、VISUAL-03。**本计划不触碰:** VISUAL-04 / VISUAL-05(Plan 03);`.markdown-body` 的任何排版规则与字重(Plan 01 已落地);`frontend/app.js` / `index.html` / `vendor/` / `ui-states/` 零 diff;`scripts/check-02-contrast.py` 代码零改动。

**本计划必须显式登记的既有断言变动(D-04):** `check-05-ui-uat.py:689-695` 那条「`#btn-process-round` 与 `#btn-authorize` 三属性**逐字节相同**」的断言**反转为「档内相同 + 三档两两不同」** —— 反转后一个断言同时覆盖 VISUAL-01 与 VISUAL-02。**注意它反转的是断言而不是现实:** 反转前它在本计划之后会 FAIL(那正是本计划要做的事)。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/idi-05-typography-and-visual-hierarchy/05-CONTEXT.md
@.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-PATTERNS.md
@.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md
@.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md
@.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md
@.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-01-PLAN.md
@frontend/style.css
@scripts/check-05-ui-uat.py
@scripts/check-02-contrast.py
</context>

## Artifacts this phase produces

**Plan 02 新建/改写的符号:**

| 类别 | 符号 | 位置 | 备注 |
|---|---|---|---|
| 改写令牌值 | `--color-action-commit-surface` | `frontend/style.css` 围栏 | `var(--radix-green-3)` → `var(--radix-green-11)`(P-5) |
| 改写令牌值 | `--color-action-commit-fg` | 围栏 | `var(--radix-green-12)` → `var(--white)`(P-6) |
| 改写令牌值 | `--color-action-irreversible` | 围栏 | `var(--radix-green-11)` → `var(--radix-green-12)`(P-8) |
| 改写令牌值 | `--color-action-irreversible-surface` | 围栏 | `var(--radix-green-3)` → `var(--radix-green-12)`(P-7) |
| 改写令牌值 | `--color-action-irreversible-fg` | 围栏 | `var(--radix-green-12)` → `var(--white)`(P-9) |
| 新增声明 | `#btn-authorize { font-size: var(--text-md); }` | `style.css:928-934` | 零新增令牌(D-13) |
| 新清单行 | `/* PAIR --color-action-commit ON --color-surface NON-TEXT */` | 围栏清单 NON-TEXT 组 | 4.48 |
| 新清单行 | `/* PAIR --color-action-irreversible ON --color-surface NON-TEXT */` | 围栏清单 NON-TEXT 组 | 11.70 |
| 改写围栏注释 | `style.css:42-45` 的 9/10 预告 | 围栏内 | A-4:改为「复用已声明的 11/12 步」 |
| 改写围栏注释 | `style.css:311` 的「three families, one value」 | 围栏内 | 三族三值 |
| 新增断言读取器 | `trio(page, sel)` + `ROUTINE` / `COMMIT` / `IRREVERSIBLE` 常量 | `scripts/check-05-ui-uat.py` | D-04 反转的载体 |
| 反转断言 | `[p3] #btn-process-round 与 #btn-authorize 三属性逐字节相同` | item3(`:689-695`) | 删除,改为三条新断言 |
| 新增断言标签 | `#btn-authorize` font-size == `--text-md`、font-weight == `600` | item3 / item4 | D-12 / D-13 |
| 新增断言标签 | `[p1] #doc-panel-header h1` font-size `14px` + font-weight `500`(字面) | item4 | D-19 的守卫 |
| 新增断言标签 | 页面级层级链 28 > 24 > 22 > 14/500 | item4 | SC3 的证据链 |
| 新增断言标签 | `#doc-pane` 选择器不存在 | item4 | D-01 的契约漂移登记,机械可核 |

Plan 03 会继续往这张表追加符号(`--color-marker-active`、两个 `--icon-*`、两条追加规则、两处伪元素规则体、清单的另外 2 条新行)。

<tasks>

<task type="tracer">
  <name>Task 1 (tracer): 三段坡道端到端 —— 围栏五处值改动 → 三族消费者 → check-02 实测比值</name>
  <files>frontend/style.css</files>
  <reversibility rating="costly">D-11:回退要重挑 Radix 步、重算 CHECK-02 的配对、并复跑三档两两不同的 gate —— 三处必须同批改。两个步的取值本身已被 04.1 的算术钉死(green-11 是最浅通过步、green-12 是最深步),但一旦落地就会被清单注释、围栏注释与 check-05 的断言同时引用。</reversibility>
  <read_first>
    - `frontend/style.css` L127-L142 —— 三个 `--color-action-*` 族的**现状逐字**;注意 L127-128 的注释已经**点名本阶段**是执行差异化那一版
    - `frontend/style.css` L46-L70 —— tier-1 primitive 的声明表(确认 `--radix-green-11` / `--radix-green-12` / `--white` **都已声明**;本计划**不新增**任何 primitive)
    - `frontend/style.css` L72-L115 —— 围栏内的 role-band 记录(「solid fill band 9-10 → step 11 for every fill that carries white text」的实测数字就在 L81-86)
    - `frontend/style.css` L42-L45 —— 必须重写的那句预告;前三行(`Only the steps a tier-2 token consumes … Hard Rule 5 …`)是声明纪律,**逐字保留**
    - `frontend/style.css` L259-L341 —— 清单的现状逐字(43 条 `/* PAIR */` + 1 条 `/* ORDER */`;L311 的注释必须重写;NON-TEXT 组的最后一行在 L337)
    - `frontend/style.css` L648-L656 / L928-L935 / L940-L947 —— 三族的消费者规则(本计划**不改它们**;只改围栏里的值)
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`### 三段坡道(D-11 定稿)` 与 §`### 两个填充步:green-11 / green-12 —— 不是契约预告的 9/10(见 S-7)` 与 §`### 清单变化:43 对 → 47 对` 的前半(本计划只落 2 条 NON-TEXT,清单到 45)
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`## Deliberate Delta Ledger` 的 P-5…P-9 与 P-17 行 —— 逐条对照本任务的改动面
    - `scripts/check-02-contrast.py` L27-L41(DECL_RE / PAIR_RE / ORDER_RE / VAR_RE 的确切形状)与 L136-L202(覆盖率下限、raw 标记数必须等于解析数、闭区间比较)
  </read_first>
  <action>
    **第 1 步 —— 围栏内五处 tier-2 值改动(D-11),选择器结构与三族名一字不动。** 逐条:把 `--color-action-commit-surface` 的值由 `var(--radix-green-3)` 改为 `var(--radix-green-11)`;把 `--color-action-commit-fg` 的值由 `var(--radix-green-12)` 改为 `var(--white)`;把 `--color-action-irreversible` 的值由 `var(--radix-green-11)` 改为 `var(--radix-green-12)`;把 `--color-action-irreversible-surface` 的值由 `var(--radix-green-3)` 改为 `var(--radix-green-12)`;把 `--color-action-irreversible-fg` 的值由 `var(--radix-green-12)` 改为 `var(--white)`。**`--color-action-commit` 不改**(它已是 `var(--radix-green-11)`,与新填充同色)。**routine 三族的值一字未动。** **不得新增任何 tier-1 primitive** —— `--radix-green-11` / `--radix-green-12` / `--white` 都已声明且都已消费;`--radix-green-9` / `--radix-green-10` 明确**不得**声明(围栏 L81-86 的 role-band 记录已实测 white on green-9 = 3.16、green-10 = 3.55,均低于 4.5:1)。三族名不得改(`commit` 而非 `gate` —— 「gate」在本代码库已指决策门)。围栏外三族消费者规则(`#btn-approve-draft` / `#btn-start-writing` / `#btn-authorize`)的 `background` / `border-color` / `color` 三条声明**一字不动** —— 这是纯值改动。

    **第 2 步 —— 清单新增两条 NON-TEXT 配对(SC 1.4.11)。** 在围栏清单的 NON-TEXT 组(L337 之后、`ORDER` 行 L341 之前)追加两行,格式必须严格匹配 `/* PAIR <fg> ON <bg> NON-TEXT */`:`/* PAIR --color-action-commit ON --color-surface NON-TEXT */` 与 `/* PAIR --color-action-irreversible ON --color-surface NON-TEXT */`。并在这两条之前加一行解释性注释,写明落地面是 `--color-surface`:`#approve-row` / `#writing-view` / `#authorize-row` 都在 `#doc-panel-body` → `#doc-panel` 内,而 `#doc-panel` 声明 `background: var(--color-surface)`。**不得**新增 routine 三只对 `--color-surface-page` 的边界配对(routine 族本阶段未改动,其既有的 `--color-action-routine ON --color-action-routine-surface` 配对已覆盖其边界),也**不得**新增 commit 与 irreversible 互为背景的配对(两者永不并排渲染:`p3` 里 `#btn-approve-draft` 所在的 `#draft-view` 是 `display: none`)。清单规模因此变为 **45 对(34 TEXT + 11 NON-TEXT)+ 1 ORDER** —— 仍远高于覆盖率下限 24/20/4。**三条既有配对的行不改、值随令牌变**:`--color-action-routine-fg ON --color-action-routine-surface` 仍 11.00;`--color-action-commit-fg ON --color-action-commit-surface` 由 11.00 变 **4.72**;`--color-action-irreversible-fg ON --color-action-irreversible-surface` 由 11.00 变 **12.32**。

    **第 3 步 —— 重写两处围栏注释(A-4 与「三族一值」)。**
    (a) **L42-45**:把最后一句「Phase 5 declares the 9/10 fill steps together with their consumers」改写为「Phase 5 复用**已声明的 11/12 步**,理由是下面的 role-band 记录」。**前三行逐字保留** —— 它们是 D-04 / Hard Rule 5 的声明纪律,现在仍然为真。
    (b) **L311**:清单里那行 `/* amber text on its three real grounds, and the six green buttons (three families, one value) */` 的「three families, one value」在本任务之后**不再成立** —— 三族从此有三个不同的值对。按 04.1-N-8 的同源规则改写:一条解释代码的注释在前提消失后必须改,否则它会开始说谎。改写后的注释须写明三族各自的值对(淡底绿字 / 实心白字 / 实心更深白字)。

    **第 4 步 —— 实跑 check-02 并逐条记录比值。** 必须实跑 `python3 scripts/check-02-contrast.py`,记录:总 PASS 行数(45)、两条新配对与三条变值配对的**逐条实测比值**、以及 `ORDER 0.363` 是否仍为 0.363(`--color-text-muted` / `--color-text` 两个操作数本计划未改值,故应逐字不变)。**不得**为了凑一个「更好看」的比值而 round 或改写任何 Radix hex —— 4.72 的 0.22 余量与 4.48 的 1.48 余量都是「最浅通过值」规则的代价。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>non-zero exit, or the only stdout line is not exactly `PASS`</fails_when>
    <automated>python3 scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>the last line is not exactly `PASS: 0 failures`, or the command exits non-zero</fails_when>
    <automated>python3 scripts/check-02-contrast.py | grep '^PASS  ' | wc -l</automated>
    <fails_when>the count is not 45</fails_when>
    <automated>python3 scripts/check-02-contrast.py | grep '^PASS  4.72  --color-action-commit-fg ON --color-action-commit-surface' | wc -l</automated>
    <fails_when>the count is not 1</fails_when>
    <automated>python3 scripts/check-02-contrast.py | grep '^PASS  12.32  --color-action-irreversible-fg ON --color-action-irreversible-surface' | wc -l</automated>
    <fails_when>the count is not 1</fails_when>
    <automated>python3 scripts/check-02-contrast.py | grep '^PASS  11.00  --color-action-routine-fg ON --color-action-routine-surface' | wc -l</automated>
    <fails_when>the count is not 1 (the routine family must be byte-unchanged)</fails_when>
    <automated>python3 scripts/check-02-contrast.py | grep '^PASS  4.48  --color-action-commit ON --color-surface NON-TEXT' | wc -l; python3 scripts/check-02-contrast.py | grep '^PASS  11.70  --color-action-irreversible ON --color-surface NON-TEXT' | wc -l</automated>
    <fails_when>either count is not 1</fails_when>
    <automated>python3 scripts/check-02-contrast.py | grep '^ORDER 0.363' | wc -l</automated>
    <fails_when>the count is not 1</fails_when>
    <automated>grep -oE '^[[:space:]]*--(white|radix-[a-z]+-[0-9]+):' frontend/style.css | wc -l</automated>
    <fails_when>the count is not 25 (Phase 5 declares zero new tier-1 primitives — 不得新增 green-9 / green-10)</fails_when>
  </verify>
  <acceptance_criteria>
    - `grep -o -- '--color-action-commit-surface: var(--radix-green-11);' frontend/style.css | wc -l` == 1
    - `grep -o -- '--color-action-commit-fg: var(--white);' frontend/style.css | wc -l` == 1
    - `grep -o -- '--color-action-irreversible: var(--radix-green-12);' frontend/style.css | wc -l` == 1
    - `grep -o -- '--color-action-irreversible-surface: var(--radix-green-12);' frontend/style.css | wc -l` == 1
    - `grep -o -- '--color-action-irreversible-fg: var(--white);' frontend/style.css | wc -l` == 1
    - `grep -o -- '--color-action-routine-surface: var(--radix-green-3);' frontend/style.css | wc -l` == 1 且 `--color-action-routine-fg: var(--radix-green-12);` 与 `--color-action-routine: var(--radix-green-11);` 各 == 1(routine 族一字未动)
    - `grep -o -- '--radix-green-9' frontend/style.css | wc -l` == 0 且 `grep -o -- '--radix-green-10' frontend/style.css | wc -l` == 0(不得声明这两个步)
    - tier-1 primitive 数仍为 25(`grep -oE '^[[:space:]]*--(white|radix-[a-z]+-[0-9]+):' frontend/style.css | wc -l` == 25)
    - 清单 `/* PAIR` 标记数为 45(`grep -o '/\* PAIR' frontend/style.css | wc -l` == 45),`/* ORDER` 仍为 1
    - 围栏 L42-45 的注释**不再**出现 `9/10` 这个串,而「D-04」与「Hard Rule 5」两处仍在(前三行逐字保留)
    - 围栏 L311 的注释**不再**出现 `one value` 这个串
    - 三条既有配对的实测比值:routine 11.00(不变)、commit 4.72、irreversible 12.32;两条新配对 commit 4.48 / irreversible 11.70;`ORDER 0.363` 逐字不变
    - 围栏外三族消费者规则的选择器与声明**零改动**(`git diff -U0 -- frontend/style.css` 在本任务内的变更行只出现在围栏区间内)
  </acceptance_criteria>
  <done>三段坡道落地为纯值改动;清单 45 对(34 TEXT + 11 NON-TEXT)+ 1 ORDER、`PASS: 0 failures`;tier-1 仍 25(零新增 primitive);两处围栏注释改写为真;routine 族与三族消费者规则零改动。</done>
</task>

<task type="auto">
  <name>Task 2: D-04 断言反转 + `#btn-authorize` 的字号步进与字重例外</name>
  <files>frontend/style.css, scripts/check-05-ui-uat.py</files>
  <reversibility rating="reversible">D-13 / D-12:字号与字重两条声明各自独立,回退只影响一个选择器与一条断言。</reversibility>
  <read_first>
    - `frontend/style.css` L926-L936 —— `#btn-authorize` 规则**现状逐字**(`padding` / `background` / `border-color` / `color` / `font-weight`,以及紧随的 `:disabled` 行)
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`### The Four Contract-Check Commands` 的「D-04 的反转形态(计划照抄)」代码块 —— `trio()` 的形状、档内相同与三档两两不同两条断言的原文
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`### 三段坡道(D-11 定稿)` 的 `#btn-authorize` 行 —— 「实心更深 + 白字 + 字号步进 + 600」四个通道
    - `scripts/check-05-ui-uat.py` L594-L700 —— item3 全文,尤其是 L675-L695:既有的 `#btn-authorize` 三属性令牌接线断言(**保留**)与 `:689-695` 的逐字节相同断言(**反转对象**)
    - `scripts/check-05-ui-uat.py` L102-L133(`ok` / `ok_true` 的语义)与 L240-L248(`read_style`)
    - `scripts/check-05-ui-uat.py` L479-L546 —— `parse_box_shadow` / `check_frozen_marker`(「解析语义而非子串全等」的范本;本任务的 `trio()` 与之同构)
  </read_first>
  <action>
    **第 1 步 —— `#btn-authorize` 新增一条 `font-size`(D-13)。** 在该规则体内新增 `font-size: var(--text-md);`(16px,现有档,**零新增令牌**)。**不加 padding 步进** —— padding 保持 `var(--space-2) var(--space-4)`。这条算术是本任务的验收条件之一:`#btn-authorize` 的文本「授权撰写总设计文档」9 字,16px 下约 144px + padding-x 32px ≈ 176px;`--doc-panel-w` 最小值 340px 减 `#doc-panel-body` 的 `padding: var(--space-8) var(--space-10)`(32/40)= 内容宽 260px > 176px,故**不换行**。`font-weight` **保持 `var(--fw-semibold)`**(D-12,「按钮统一 500」的唯一已登记例外)。`:disabled` 行一字不动。

    **第 2 步 —— 反转 `check-05-ui-uat.py:689-695` 的断言(D-04)。** 删除那条「`#btn-process-round` 与 `#btn-authorize` 三属性逐字节相同」的断言(它在本任务之后会 FAIL —— 那正是本任务要做的事),替换为**三条**新断言:
    (a) 新增模块级读取器 `def trio(page, sel)`,返回 `(read_style(page, sel, "color"), read_style(page, sel, "border-top-color"), read_style(page, sel, "background-color"))` 三元组;
    (b) 新增三个选择器常量 `ROUTINE = ("#btn-process-round", "#btn-continue-check", "#btn-continue-repair")`、`COMMIT = ("#btn-approve-draft", "#btn-start-writing")`、`IRREVERSIBLE = ("#btn-authorize",)`;
    (c) 三条断言:`ok_true(item, "routine 三只三属性逐字节相同", len({trio(page, s) for s in ROUTINE}) == 1, ...)`、`ok_true(item, "commit 两只三属性逐字节相同", len({trio(page, s) for s in COMMIT}) == 1, ...)`、`ok_true(item, "routine / commit / irreversible 三档两两不同", len({trio(page, ROUTINE[0]), trio(page, COMMIT[0]), trio(page, IRREVERSIBLE[0])}) == 3, ...)`。**档内相同那一半同样承重** —— 它能抓到「改错了一只」。这三条断言放在 item3 里替换原断言的位置(`p3` 样本已进入)。**为什么一个状态就够:** 六只按钮全部常驻 DOM,`getComputedStyle` 对 `display: none` 的元素仍返回解析后的 `color` / `background-color` / `border-color`(它们不依赖布局),而该文件现在就已经在 `p3` 里读 `#btn-authorize` 而不检查可见性。**注意 item3 里既有的三条 `#btn-authorize` 三属性令牌接线断言(L675-L690)保留不动** —— 它们现在会自动跟随新值(routine 与 irreversible 的令牌解析值已不同),这正是「接线对但值错」的两种失败模式被分开诊断的形态。

    **第 3 步 —— 新增 `#btn-authorize` 的字号与字重断言(D-12 / D-13)。** 在 item4 里新增两条:`#btn-authorize` 的 computed `font-size` == `resolve_token(page, "--text-md")`;computed `font-weight` == `"600"`。并在每条断言旁用 `info()` 打印解析值。

    **第 4 步 —— 实跑并记录。** 实跑 CHECK-01 / CHECK-02(45 对)/ `--item 3` / `--item 4` / `--item smoke` 并记录原始输出。**同时核对 `--color-action-irreversible*` 的消费者集合未变**(D-15):`grep -n 'var(--color-action-irreversible' frontend/style.css` 命中的**围栏外**行必须只有 `#btn-authorize` 规则的那三行(以及它的 `:disabled` 行若引用);本计划改的是它的**值**,不是它的**消费者** —— 这两件事必须分别核对并分别写进 SUMMARY。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>non-zero exit, or the only stdout line is not exactly `PASS`</fails_when>
    <automated>python3 scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>the last line is not exactly `PASS: 0 failures`, or the command exits non-zero</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 3,4,smoke</automated>
    <fails_when>exit code is not 0, or the `=== 逐项结论 ===` block reports anything other than PASS for items 3, 4 and smoke</fails_when>
    <automated>grep -o 'font-size: var(--text-md);' frontend/style.css | wc -l</automated>
    <fails_when>the count is not 8 (7 pre-existing consumers plus the new #btn-authorize declaration)</fails_when>
    <automated>grep -n -A 8 '^#btn-authorize {' frontend/style.css | grep -o 'font-size: var(--text-md);' | wc -l; grep -n -A 8 '^#btn-authorize {' frontend/style.css | grep -o 'font-weight: var(--fw-semibold);' | wc -l</automated>
    <fails_when>either count is not 1</fails_when>
    <automated>grep -n -A 8 '^#btn-authorize {' frontend/style.css | grep -o 'padding: var(--space-2) var(--space-4);' | wc -l</automated>
    <fails_when>the count is not 1 (D-13 forbids a padding step)</fails_when>
    <automated>grep -n 'var(--color-action-irreversible' frontend/style.css</automated>
    <fails_when>any match outside the fence belongs to a selector other than `#btn-authorize` (D-15: exactly one consumer, forever)</fails_when>
    <automated>grep -o 'len({trio(page, s) for s in ROUTINE}) == 1' scripts/check-05-ui-uat.py | wc -l</automated>
    <fails_when>the count is not 1 (the D-04 within-tier half is load-bearing and must be present)</fails_when>
  </verify>
  <acceptance_criteria>
    - `#btn-authorize` 规则体内有 `font-size: var(--text-md);`,且 `padding` / `font-weight` / `background` / `border-color` / `color` 五条声明中除新增的 `font-size` 外逐字未变
    - `grep -o 'font-size: var(--text-md);' frontend/style.css | wc -l` == 8(HEAD 7 + 本任务 1)
    - `:689-695` 的「逐字节相同」断言**已删除**(`grep -o '#btn-process-round 与 #btn-authorize 三属性逐字节相同' scripts/check-05-ui-uat.py | wc -l` == 0)
    - `trio()` 读取器与 `ROUTINE` / `COMMIT` / `IRREVERSIBLE` 三个常量存在;三条新断言(档内相同 ×2 + 三档两两不同 ×1)存在
    - item3 里既有的三条 `#btn-authorize` 令牌接线断言保留
    - `--color-action-irreversible` / `-surface` / `-fg` 三个令牌在围栏外的**消费者集合未变**:只有 `#btn-authorize` 规则
    - `--item 3,4,smoke` 三项全 PASS(0 FAIL / 0 BLOCKED)
    - `check-02` 仍 45 对 + `ORDER 0.363`(本任务不改清单)
  </acceptance_criteria>
  <done>三段坡道可被一个断言同时验证(VISUAL-01 + VISUAL-02);`#btn-authorize` 为 16px / 600 / 实心更深,五只按钮为 500;`--color-action-irreversible*` 仍单消费者;`--item 3,4,smoke` 全 PASS。</done>
</task>

<task type="auto">
  <name>Task 3: VISUAL-03 复证 + 页面级层级链(SC3)</name>
  <files>scripts/check-05-ui-uat.py</files>
  <read_first>
    - `frontend/style.css` L404-L410 —— `#doc-panel-header h1` 规则**现状逐字**(`font-size: var(--text-base)` / `font-weight: var(--fw-medium)` / `color: var(--color-text-secondary)`)与它上方的源码注释(「安静的容器标签,不是全屏最大最重的文字」)
    - `frontend/style.css` L548-L549(`.overlay-card h3` = `var(--text-xl)` 24px)、L624-L626(Plan 01 之后 `.markdown-body h1/h2/h3` = 28 / 22 / 18px)、L611-L615(`#draft-view h2` = `var(--text-lg)` 18px)
    - `frontend/index.html` L10-L70(四个 section 的 DOM 结构)与 L84 附近(`#doc-panel-header` 是 `.panel-header` 但不被三条 ID 选择器匹配)
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`### VISUAL-03 —— 认定已由 qrq 实现,本阶段只做复证(D-19)` —— 两行判定表与「连带效果(页面级层级已立住)」的四行排名链
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/05-CONTEXT.md` D-19 与 D-01 的契约漂移清单里 `#doc-pane > h1` 那一行 —— 契约文本的漂移登记
    - `scripts/check-05-ui-uat.py` L707-L810 —— item4 全文(新断言的落点;`p1` 与 `p3` 两个样本已在其中进入)
    - `scripts/check-05-ui-uat.py` L258-L291(`resolve_token` / `resolve_color`)与 L240-L248(`read_style`)
  </read_first>
  <action>
    **第 1 步 —— 零 CSS 改动,只加断言(D-19)。** 本任务**不修改** `frontend/style.css` 的任何一个字节。VISUAL-03 已由 quick `260918-qrq` 实现:`#doc-panel-header h1` 是 14px / `--fw-medium` 500 / `--color-text-secondary`(`#646464`),源码注释即「安静的容器标签,不是全屏最大最重的文字」。本任务的产物是**门与记录**,不是样式。

    **第 2 步 —— 更正门里的选择器名(D-01 的漂移登记,机械可核)。** 在 item4 里新增两条断言:
    (a) `#doc-panel-header h1` 的 computed `font-size` == `"14px"`(字面值 —— 这是 VISUAL-03 的守卫,D-03 第二类:它守卫的是一个**不该变**的值,改成令牌接线会退化为同义反复)且 computed `font-weight` == `"500"`;
    (b) `#doc-pane` 这个选择器在页面上**不存在**(`document.querySelector('#doc-pane')` 返回 null)。这一条把契约文本的漂移登记成机械可核的事实:ROADMAP / 04-UI-SPEC 引用的 `#doc-pane > h1` 从来不是 HEAD 上的选择器,实际承担该职责的是 `#doc-panel-header h1`。**不得**为了「让契约文本成立」而新建一个 `#doc-pane` 元素或规则 —— 那是改 DOM / 加 CSS,两者都在本阶段的范围锁之外。

    **第 3 步 —— 页面级层级链(SC3 的证据链)。** 在 item4 里新增一组断言,把 UI-SPEC 的四行排名链变成运行时读数:在 `#draft-content`(带 `.markdown-body`)里用应用自身的 `renderMarkdown` 渲染一个含 h1 与 h2 的探针串,然后读四个 computed `font-size` 并断言**严格的数值大小序**:文档 h1(28px)> `.overlay-card h3`(24px)> 文档 h2(22px)> `#doc-panel-header h1`(14px)。断言写成「解析成整数后逐对比较」而不是字符串比较 —— 避免 `"14px"` 与 `"9px"` 这类字符串序陷阱。这一条是 SC3「全屏最大最重的文字不再是容器标签『文档区』」的机器化形态:字号半边由本断言覆盖,剩余的是视觉层级判断(已作为 E8 的 backstop 陈述记录)。

    **第 4 步 —— 实跑并记录。** 实跑 `--item 4` 与 `--item smoke` 并记录原始输出;把「门的选择器名从 `#doc-pane > h1` 更正为 `#doc-panel-header h1`」这一条连同 `#doc-pane` 不存在的机械证据写进 SUMMARY(这是 D-01 契约漂移清单在本阶段的登记动作之一)。**不改 `REQUIREMENTS.md`** —— 改它会作废指纹。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 4,smoke</automated>
    <fails_when>exit code is not 0, or the `=== 逐项结论 ===` block reports anything other than PASS for items 4 and smoke</fails_when>
    <automated>git status --porcelain -- frontend/</automated>
    <fails_when>the output lists any path other than `frontend/style.css` (this task must change zero bytes of frontend/style.css; capture git's exit code before reading the output)</fails_when>
    <automated>git diff --stat -- frontend/style.css</automated>
    <fails_when>the command prints a non-empty stat line (this task must not modify the stylesheet)</fails_when>
    <automated>grep -o 'doc-panel-header h1' scripts/check-05-ui-uat.py | wc -l</automated>
    <fails_when>the count is less than 2 (font-size and font-weight assertions)</fails_when>
    <automated>grep -o "'#doc-pane'" scripts/check-05-ui-uat.py | wc -l</automated>
    <fails_when>the count is not 1 (the contract-drift assertion must be present)</fails_when>
    <automated>grep -n '^#doc-panel-header h1 {' frontend/style.css</automated>
    <fails_when>the command prints no line, or the rule body no longer carries `font-size: var(--text-base);` and `font-weight: var(--fw-medium);`</fails_when>
  </verify>
  <acceptance_criteria>
    - `frontend/style.css` 在本任务内**零字节改动**(`git diff --stat -- frontend/style.css` 输出为空)
    - `#doc-panel-header h1` 的 computed `font-size` == `"14px"` 且 `font-weight` == `"500"`(字面断言,D-03 第二类)
    - `document.querySelector('#doc-pane')` 为 null 的断言存在且 PASS
    - 页面级层级链断言存在且 PASS:28 > 24 > 22 > 14(整数比较,非字符串比较)
    - `--item 4` 与 `--item smoke` 全 PASS(0 FAIL / 0 BLOCKED)
    - `REQUIREMENTS.md` 与 `ROADMAP.md` 零改动(`git status --porcelain` 不出现这两个路径)
  </acceptance_criteria>
  <done>VISUAL-03 复证成立且零 CSS 改动;门的选择器名更正为 `#doc-panel-header h1` 并有 `#doc-pane` 不存在的机械证据;页面级层级链 28 > 24 > 22 > 14/500 由运行时断言钉死。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 人类 → 流程(**本计划的主边界**) | G3 授权按钮的视觉形态是核心价值红线的机器可读信号。本计划把三段坡道落地,使 `#btn-authorize` 在**形态**上就与五只例行/承诺按钮不同(淡底 vs 实心),不依赖色深对比 |
| 围栏 `:root` → 浏览器 | 令牌值的唯一事实源。本计划改 5 个值、加 2 条清单行;围栏外三族消费者规则零改动,故「值层改动不产生假 FAIL」这条 04.1 已立的性质继续成立 |
| `scripts/check-02-contrast.py` → 上游文档 | 比值的唯一仲裁者是本脚本的实算值,Radix 与两份 UI-SPEC 的 AA 论断**一律不采信**(04.1 已立此方法论,并在自己的五个 band 里被推翻四次) |
| 本阶段无新增网络 / 输入 / 依赖面 | `frontend/app.js` / `index.html` / `vendor/` 零 diff;零新增文件、零新增依赖、零构建步骤 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-05-01 | Elevation of Privilege | `#btn-authorize`(G3 授权门)与五只例行/承诺按钮的可区分性 | high | mitigate | 三段坡道在**形态**上分离(淡底 vs 实心 vs 实心更深)+ 字号步进(D-13)+ 字重例外(D-12)+ `--color-action-irreversible*` 单消费者(D-15);D-04 的「档内相同 + 三档两两不同」断言是这条红线的可执行形态,一个断言同时覆盖 VISUAL-01 与 VISUAL-02 |
| T-idi-05-02 | Tampering | `frontend/style.css` 围栏与清单的一致性 | medium | mitigate | 新清单行必须命名围栏内**已声明**的令牌 —— `check-02` 对未声明名 `sys.exit(1)`;raw `/* PAIR` 标记数必须等于解析数(45 == 45);覆盖率下限 24/20/4;CHECK-01 断言围栏外零裸 hex、tier-1 名不出围栏 |
| T-idi-05-03 | Tampering | 为凑比值而篡改 Radix 步或采信上游 AA 论断 | medium | mitigate | 每个任务实跑 `check-02` 并把逐条实测比值写进 SUMMARY;`--radix-green-9` / `green-10` 的**不得声明**有机械断言(`grep -o -- '--radix-green-9' \| wc -l` == 0);tier-1 计数断言 == 25 |
| T-idi-05-04 | Denial of Service | 渲染回归(填充形态 / 字号 / 禁用态) | medium | mitigate | 每个 `style.css` 任务带至少一项运行时验证(硬规则 7):`--item 3,4,smoke` 在 p1 / p3 两个真实样本上读 computed style;五处 `:disabled` 的 `opacity: 0.55` 逐字节未变(D-14 / Pitfall M5) |
| T-idi-05-05 | Information Disclosure | 本阶段的改动内容 | low | accept | 改动只有 5 个令牌值、2 条清单行、1 条 `font-size` 声明与注释;无用户数据、无网络请求、无外部资源 |
| T-idi-05-SC | Tampering | npm / pip / cargo 安装 | high | mitigate | 本阶段零安装(硬规则 6):不新增依赖、文件或构建步骤;`frontend/vendor/` 仍只含 `marked.min.js`。无 `[ASSUMED]` / `[SUS]` 包,故无需 package-legitimacy 人工签核门 |
</threat_model>

<verification>
- `bash scripts/check-01-token-conformance.sh` → `PASS` / exit 0
- `bash scripts/check-03-hidden-uniqueness.sh` → `PASS`(`^\.hidden {` == 1)
- `bash scripts/check-04-important-count.sh` → `PASS`(`!important;` 声明数 == 1)
- `python3 scripts/check-02-contrast.py` → `PASS: 0 failures`,**45 对(34 TEXT + 11 NON-TEXT)+ `ORDER 0.363`**
- `.venv/bin/python scripts/check-05-ui-uat.py --item 3,4,smoke` → 三项全 PASS(0 FAIL / 0 BLOCKED)
- tier-1 primitive 数 == 25(Phase 5 新增 0 个);`--radix-green-9` / `--radix-green-10` 零出现
- Gate 2:`comm -23 <(grep -o 'var(--[a-z0-9-]*' frontend/style.css | sed 's/var(//' | sort -u) <(grep -o '\-\-[a-z0-9-]*:' frontend/style.css | sed 's/:$//' | sort -u)` 输出为空
- Gate 3:`git status --porcelain -- frontend/` 只出现 `frontend/style.css`;`ls frontend/vendor/` 只有 `marked.min.js`
</verification>

<success_criteria>
- 三段坡道落地:淡底 / 实心 / 实心更深,形态差异是第一区分手段(VISUAL-01 / VISUAL-02)
- `#btn-authorize` 与五只按钮的 computed 三属性两两不同,且档内逐字节相同(D-04)
- 授权按钮的字面文本达 AA:white on green-11 = 4.72、white on green-12 = 12.32
- VISUAL-03 复证成立且零 CSS 改动,页面级层级链 28 > 24 > 22 > 14/500 由运行时断言钉死
- 四条既有守卫全绿;`frontend/app.js` / `index.html` / `vendor/` / `ui-states/` 零 diff
</success_criteria>

<output>
Create `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-02-SUMMARY.md` when done
</output>
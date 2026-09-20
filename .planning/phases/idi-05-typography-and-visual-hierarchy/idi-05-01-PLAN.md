---
phase: idi-05-typography-and-visual-hierarchy
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - frontend/style.css
  - scripts/check-05-ui-uat.py
autonomous: true
requirements:
  - TYPE-01
  - TYPE-02
  - TYPE-03

estimate:
  tokens: 60000
  raw_tokens: 60000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- lifted from idi-05-UI-SPEC.md `## UI Considerations` — explicit tier (6 of 22; E9) ----
    - "E9 四处 chrome 标题的 empty 态内容与结构未被本阶段改动(四处 chrome 标题的显隐由 app.js / index.html 既有结构决定,本阶段两者零 diff,故空态结构不变)← UI-SPEC UI-Considerations E9 `empty`(explicit)"
    - "E9 四处 chrome 标题的 loading 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E9 `loading`(explicit)"
    - "E9 四处 chrome 标题的 error 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E9 `error`(explicit)"
    - "E9 四处 chrome 标题的 populated 态由 check-05 的字面 px 断言守卫(D-03:守卫项保持字面值,不得改成令牌接线表述)← UI-SPEC UI-Considerations E9 `populated`(explicit)"
    - "E9 四处 chrome 标题的 partial 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E9 `partial`(explicit)"
    - "E9 四处 chrome 标题的个数与位置由 DOM 决定,本阶段零 diff ← UI-SPEC UI-Considerations E9 `zero-one-many`(explicit)"
    # ---- lifted from idi-05-UI-SPEC.md `## UI Considerations` — backstop tier (6 of 18) ----
    - statement: "E1 `.markdown-body` 的四个宿主(`#draft-content` / `#brainstorm-content` / `#round-doc` / `#latest-check`):长文档在 `#draft-content` 内滚动而非撑破容器;本阶段只改标题字号,不新增滚动容器(布局归 Phase 6),此处只断言不回归。"
      verification: backstop
    - statement: "E1 超长 DESIGN.md 渲染后 `#doc-pane` 无横向滚动条,28px h1 不撑破内容宽。"
      verification: backstop
    - statement: "E2 文档 h1/h2/h3:28px h1 / 22px h2 在 `--doc-panel-w` 最窄值(340px)下不溢出容器。"
      verification: backstop
    - statement: "E2 三级标题层级可辨且不互相淹没;h1 是全屏最大文字(28 > `.overlay-card h3` 的 24 > 22)。字号半边已由 check-05 的令牌接线断言覆盖,剩余的是视觉层级判断。"
      verification: backstop
    - statement: "E9 四处 chrome 标题在两栏布局下均不溢出各自容器(SC1 的守卫对象,本阶段不得被带偏)。"
      verification: backstop
    - statement: "E9 四处 chrome 标题文本变长时各自保持既有字号与色值(`.panel-header h2` 14px / `#draft-view h2` 18px / `.overlay-card h3` 24px),不因本阶段标题改动而漂移。"
      verification: backstop
    # ---- phase-specific truths ----
    - "围栏内新增 `--text-2xl: 22px;` 与 `--text-3xl: 28px;`,插在 `--text-xl: 24px;` 之后、按名字序(xs → base → md → lg → xl → 2xl → 3xl),字号刻度 5 → 7 档 ← D-06 / D-07"
    - "`.markdown-body h1` / `.markdown-body h2` / `.markdown-body h3` 的 `font-size` 分别为 `var(--text-3xl)` / `var(--text-2xl)` / `var(--text-lg)`;作用域仍限定在 `.markdown-body` 内,未新增任何全局 `h1, h2, h3` 规则 ← TYPE-01 / 硬规则 9 / Pitfall M4"
    - "围栏 L204 注释已改写为 7 档,并写明「契约的 `--text-2xl` 指 18px,本围栏的 `--text-2xl` 指 22px,名同值不同,不是笔误」← D-07 / 05-N-1 / A-6"
    - "围栏 L217 行高注释已从「整数配对」改写为「比率配对」;既有算术错误 `18/28` 修正为 `18/24`;`four` 与三档配对的不自洽已消解(比率表 7 行 + `--lh-compact` 单列 chrome-only)← D-10 / UI-SPEC §行高"
    - "TYPE-02 复证成立:`.markdown-body th, .markdown-body td` 与 `.markdown-body code` 仍为 `var(--text-base)`(14px)、`.markdown-body blockquote` 仍为 `var(--color-text-muted)`,三处零 CSS 改动,由新增的运行时令牌接线断言 + 既有字面 px 守卫共同举证 ← TYPE-02 / D-08"
    - "字重三档分工显式化:`#btn-approve-draft` / `#btn-process-round` / `#btn-start-writing` / `#btn-continue-check` / `#btn-continue-repair` 五条规则的 `font-weight` 为 `var(--fw-medium)`(500);`#btn-authorize` 与 `#btn-divergence` 保持 `var(--fw-semibold)`(600)← TYPE-03 / D-09 / D-12"
    - "`bash scripts/check-01-token-conformance.sh` 打印 `PASS` 且 exit 0(围栏外裸 hex 仍为 0、tier-1 名仍不出围栏)← 硬规则 5 / CHECK-01"
    - "`python3 scripts/check-02-contrast.py` 仍打印 `PASS: 0 failures`,清单规模仍为 43 对(34 TEXT + 9 NON-TEXT)+ 1 ORDER,`ORDER 0.363` 不变(本计划不改清单、不改任何颜色令牌值)← CHECK-02"
    - "`--text-xl` 仍有消费者(`.overlay-card h3` / `#chat-greeting`),不产生孤儿字号档 ← Hard Rule 5 / UI-SPEC §既有档的消费者迁移核账"
    - "运行时:`.markdown-body h1` / `h2` / `h3` 的 computed `font-size` 分别等于运行时解析出的 `--text-3xl` / `--text-2xl` / `--text-lg`;五只动作按钮的 computed `font-weight` 为 `500` ← 硬规则 7 / D-03"

  artifacts:
    - path: "frontend/style.css"
      provides: "围栏内新增 `--text-2xl` 22px / `--text-3xl` 28px 两档并重写 L204(5 档→7 档 + 名同值不同警示)与 L217(整数配对→比率配对 + `18/24` 修正);围栏外 `.markdown-body h1/h2/h3` 三条 `font-size` 改值、五条动作按钮规则的 `font-weight` 改为 `var(--fw-medium)`"
      contains: "--text-3xl: 28px;"
    - path: "scripts/check-05-ui-uat.py"
      provides: "item4 新增令牌接线断言(`.markdown-body h1/h2/h3` 字号、`.markdown-body th/td` 字号、`.markdown-body blockquote` 色)、五只按钮 `font-weight` 断言;`:742` 的 `#brainstorm-view h2` 字号断言改为令牌接线(D-02);D-03 第二类字面守卫逐条保持"
      contains: "def item4"

  key_links:
    - from: "frontend/style.css 围栏内的 `--text-3xl` / `--text-2xl`"
      to: "`.markdown-body h1` / `.markdown-body h2` 的 `font-size`"
      via: "围栏外消费者与令牌同一次提交落地(Hard Rule 5 —— 新令牌不得成为孤儿)"
      pattern: "font-size: var\\(--text-3xl\\);"
    - from: "`.markdown-body h1/h2/h3` 的 `font-size`"
      to: "scripts/check-05-ui-uat.py 的运行时断言"
      via: "期望侧由 resolve_token(page, \"--text-3xl\") 在运行时解析,不硬编码 px(D-03 第一类)"
      pattern: "resolve_token\\(page, \"--text-3xl\"\\)"
    - from: "`.panel-header h2` / `#draft-view h2` / `.overlay-card h3` / `.markdown-body` 的字面 px 守卫"
      to: "四处 chrome 覆盖未被本阶段标题改动带偏(SC1)"
      via: "D-03 第二类:字面值是特性而非缺陷,它是唯一能抓到「标题改动溢出到 chrome」的形态"
      pattern: "read_style\\(page, \"\\.panel-header h2\", \"font-size\"\\)"

  prohibitions:
    - statement: "不得给 `.markdown-body` 容器之外的任何 `h1` / `h2` / `h3` 写字号规则。全局 `h1, h2, h3` 的特异性是 0-0-1,在 `font-size` 上对四处 chrome 覆盖(`#draft-view h2` / `#brainstorm-view h2` 为 1-0-1,`.panel-header h2` / `.overlay-card h3` 为 0-1-1)是惰性的 —— 真正的暴露面是它们未声明的 `line-height` / `margin` / `letter-spacing`,以及任何落在 `.markdown-body` 之外、又无更具体规则兜底的标题(硬规则 9 / Pitfall M4 / TYPE-01)"
      status: active
      verification: flagged
    - statement: "不得把 `--text-2xl` 从 22px「修正」回契约写的 18px —— 18px 在 HEAD 上已被 `--text-lg` 占用,改回会让 18px 有两个令牌名(`2xl` 与 `lg`),即第二事实源;围栏注释必须写明「名同值不同,不是笔误」(D-07 / 05-N-1 / A-6)"
      status: active
      verification: flagged
    - statement: "不得软化任何一处 `:disabled` 的 `opacity: 0.55` / `0.5` —— 它是 G3 前提条件唯一的视觉信号,SC 1.4.3 豁免非活动组件(Pitfall M5 / D-14)"
      status: active
      verification: flagged
    - statement: "不得改动任何用户可见文案 —— G3 授权按钮的标签是核心价值红线唯一的文字,本阶段 copy 零改动(Copywriting Contract 冻结)"
      status: active
      verification: flagged
    - statement: "不得重排 `style.css` 的任何规则或声明(硬规则 3「追加,不重排」)。`#draft-view h2`(L611)与 `#brainstorm-view h2`(L679)同为 1-0-1,后者靠源码顺序取胜 —— 重排即渲染变更,而源码 diff 看起来完全无辜"
      status: active
      verification: flagged
    - statement: "不得把 `check-05-ui-uat.py` 的第二类守卫(`.panel-header h2` 14px / `#draft-view h2` 18px / `.overlay-card h3` 24px / `.markdown-body` 16px / `.markdown-body code` 14px / `--text-base` 14px)改成令牌接线表述 —— 字面值是**特性而非缺陷**,它是唯一能抓到「标题改动溢出到 chrome」的形态(D-03)"
      status: active
      verification: flagged
    - statement: "不得把 `#btn-divergence` 拉进「按钮统一 500」—— 它属于 `--color-action-warning` 族,不属于三段坡道的任何一族;拉进来会在三段坡道之外造出一个未登记的第四档(TYPE-03 / UI-SPEC §TYPE-03)"
      status: active
      verification: flagged

  assumptions:
    # ---- edge probe fallback ($COVERAGE): 3 rows for this plan's requirement IDs, ALL unresolved ----
    # The edge probe is an English-cue classifier and misclassified the Chinese requirement prose;
    # `unclassified` stays `unresolved` (never auto-resolved with backstop, never dismissed).
    - statement: "TYPE-01 的边缘面未经探针确认(probe 返回 `unclassified — review manually`):「显式 font-size + 作用域限定」在字号刻度 5 → 7 档后是否存在未覆盖的标题宿主?本计划按已锁决策(D-06 只改 `.markdown-body` 内的三条规则)执行,并把该行记为 flagged assumption 而非已解决项。"
      status: unresolved
      verification: flagged
    - statement: "TYPE-02 的边缘面未经探针确认(probe 返回 `unclassified — review manually`):三处「已归入刻度与令牌」的复证对象在 14px / 16px 两个相邻档之间是否存在边界情形?本计划只复证、零 CSS 改动,并把该行记为 flagged assumption。"
      status: unresolved
      verification: flagged
    - statement: "TYPE-03 的边缘面未经探针确认(probe 返回 `unclassified — review manually`):字重三档(400 / 500 / 600)在「按钮统一 500」之后的分布边界(徽标 / 事件 chip 仍 600)是否完整?本计划按 D-09 的显式分工表执行,并把该行记为 flagged assumption。"
      status: unresolved
      verification: flagged
---

<!-- planner-discipline-allow: content: '📌 ' -->
<!-- planner-discipline-allow: content: '📍 ' -->
<!-- planner-discipline-allow: 18/28 -->
<!-- 本计划的两个任务(Plan 01 与 Plan 03)都不得把这两条 emoji 字面量当作验收命令的负向 grep 对象;
     Plan 03 的 Gate 5 只对 data-URI 内的颜色信息做负向断言,不对 emoji 字面量做断言。此处的 allow
     标记是为「本计划正文引用了 UI-SPEC 对这两处规则的处置」而备,不构成任何验收命令的负向判据。 -->
<!-- `18/28` 是承重的:Task 2 的任务就是修正围栏 L217 注释里这一处既有算术错误(18 × --lh-tight
     1.3333 = 24,不是 28),执行器必须知道删的是哪一个串;其验收对源文件做一次出现次数计数(须为 0)
     来证明改净。字面量在此是任务定义的一部分,不是散漫的散文引用。 -->

<objective>
把渲染出的 DESIGN.md 与界面 chrome 的排版刻度从 5 档扩到 7 档,把字重三档的分工显式化,并给 TYPE-02 的「已归入刻度与令牌」出可核证据。

Purpose: 本阶段的三条排版需求(TYPE-01 / TYPE-02 / TYPE-03)是同一次刻度重写。TYPE-01 的实质不是「有 font-size」——`260918-qrq` 已经加了作用域规则 —— 而是**刻度不够用**:h1 的 24px 已是旧刻度上限,不开两档就无法建立 h1 > h2 > h3 的三级标题层级。TYPE-02 的实质是**复证**:`table th/td` / `code` / `blockquote` 三处已由 qrq 归入刻度与令牌,本计划只出证据、零 CSS 改动(为「有交付物」而重写这三处会把一个已经正确的状态改坏,并让 `--text-base` 的消费者计数漂移)。TYPE-03 的实质是**分工**:六个动作按钮现在与内容标题同重(600),而 chrome 标题是 500 —— 按钮改为 500 是分工的由来。

Output: 7 档字号刻度(`--text-2xl` 22px / `--text-3xl` 28px 与消费者同提交);`.markdown-body h1/h2/h3` = 28 / 22 / 18;五条动作按钮规则的字重 = 500;两处围栏注释(字号档数、行高配对)改写为真;`scripts/check-05-ui-uat.py` 新增的令牌接线断言与保持字面的四处 chrome 守卫。

**基线口径(D-01):磁盘 HEAD 是唯一现实基线。** 本计划每一个「现状」值都取自 `frontend/style.css` 的磁盘内容(1054 行)与 `scripts/check-05-ui-uat.py` 的断言;两份 UI-SPEC / `ROADMAP.md` §Phase 5 / `REQUIREMENTS.md` 的具体数值**只作意图参考**。已登记的契约漂移中与本计划直接相关的两条:`ROADMAP` 的 `Gates` 行写 `#brainstorm-view h2` 仍计算为 14px / `#8a6508`,HEAD 实况是 16px / `--color-action-warning`(D-02 把该门改写为令牌接线表述);`REQUIREMENTS.md` 的 TYPE-01 写 `#draft-view h2` 15px / `.overlay-card h3` 16px,HEAD 实况是 18px / 24px(D-03 的四处 chrome 字面守卫以 HEAD 为准)。

**为什么三个计划串行而非并行(本阶段的结构约束,不是保守)。** 本阶段的改动面是**单一文件** `frontend/style.css` 加**单一测试文件** `scripts/check-05-ui-uat.py`;`execute-phase` 的同波次规则要求同波次计划的 `files_modified` 零重叠,故三个计划必须落在三个波次。这不是本阶段可以优化的地方 —— 它是「纯 CSS 阶段」的定义。

**本计划关闭的需求:** TYPE-01、TYPE-02、TYPE-03。**本计划不触碰:** VISUAL-01…05(Plan 02 / Plan 03);`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` / `scripts/ui-states/` 零改动;`scripts/check-02-contrast.py` 代码零改动;hover / 焦点 / 布局 / 窄窗口(Phase 6 / 7)。

**本计划必须显式登记的既有断言变动(D-03 分类):** `check-05-ui-uat.py:742` 的 `#brainstorm-view h2` 字号断言**改为令牌接线表述**(D-02:它守卫的 14px 已由 qrq 推翻,继续硬编码只会继续假 FAIL);`:745` `:746` `:747` `:751` `:760` `:800-807` 六处**保持字面 px**(D-03 第二类:它们是 SC1「标题改动没有溢出到 chrome」的唯一机器化形态)。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/REQUIREMENTS.md
@.planning/phases/idi-05-typography-and-visual-hierarchy/05-CONTEXT.md
@.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-PATTERNS.md
@.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md
@.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md
@frontend/style.css
@scripts/check-05-ui-uat.py
@scripts/check-02-contrast.py
</context>

## Artifacts this phase produces

> 本节的用途:**plan-review-convergence 的 source-grounding pass 读它,把本阶段新建的符号从漂移校验里排除**。
> 本阶段(全部三个计划)新建的符号逐条列出;未列在此的符号即既有符号,其变动必须能追到某条已锁决策。

**Plan 01 新建/改写的符号:**

| 类别 | 符号 | 位置 | 备注 |
|---|---|---|---|
| 新 CSS 自定义属性 | `--text-2xl`(22px) | `frontend/style.css` 围栏,紧随 `--text-xl: 24px;` 之后 | 名同值不同(契约的 `2xl` 指 18px) |
| 新 CSS 自定义属性 | `--text-3xl`(28px) | 同上 | 契约的 `3xl` 指 22px |
| 改写声明值 | `.markdown-body h1 { font-size }` | `style.css:624` | `var(--text-xl)` → `var(--text-3xl)` |
| 改写声明值 | `.markdown-body h2 { font-size }` | `style.css:625` | `var(--text-lg)` → `var(--text-2xl)` |
| 改写声明值 | `.markdown-body h3 { font-size }` | `style.css:626` | `var(--text-md)` → `var(--text-lg)` |
| 改写声明值 | 五条动作按钮规则的 `font-weight` | `style.css:654` `:882` `:945` `:1003` | `var(--fw-semibold)` → `var(--fw-medium)` |
| 改写围栏注释 | `style.css:204` 的字号刻度头 | 围栏内 | `5 sizes` → `7 sizes` + 名同值不同警示 |
| 改写围栏注释 | `style.css:217` 的行高头 | 围栏内 | 整数配对 → 比率配对;`18/28` → `18/24`;`four` 消解 |
| 新增断言标签 | `[p1] .markdown-body h1/h2/h3 font-size == var(--text-3xl/2xl/lg)` | `scripts/check-05-ui-uat.py` item4 | 令牌接线(D-03 第一类) |
| 新增断言标签 | `[p1] .markdown-body th/td font-size == var(--text-base)` | item4 | TYPE-02 复证证据 |
| 新增断言标签 | `[p1] .markdown-body blockquote color == var(--color-text-muted)` | item4 | TYPE-02 复证证据 |
| 新增断言标签 | 六只动作按钮 `font-weight`(五只 500 + `#btn-authorize` 600) | item4 | TYPE-03 |
| 改写断言 | `[p1] #brainstorm-view h2 font-size` | item4(`:742`) | 字面 `16px` → 令牌接线 `--text-md`(D-02) |
| 新增探针串 | `renderMarkdown` 的 harness 探针扩为「代码跨度 + 表格 + 引用块」 | item4 | 真实渲染路径,零网络、零 AI 调用 |

Plan 02 与 Plan 03 会继续往这张表追加符号(`--color-action-*` 五处值改动、`--color-marker-active`、两个 `--icon-*`、两条追加规则、两处伪元素规则体、清单的 4 条新行);本表只列 Plan 01 的产出。

<tasks>

<task type="tracer">
  <name>Task 1 (tracer): 字号刻度两档端到端 —— 围栏声明 → `.markdown-body` 消费 → 运行时断言</name>
  <files>frontend/style.css, scripts/check-05-ui-uat.py</files>
  <reversibility rating="costly">D-06 / D-07:回退要同时改围栏的两条声明、`.markdown-body h1/h2/h3` 三条规则、`check-05` 的三条断言与围栏注释里的档数说明 —— 四处必须同批改,任一处漏改即产生「声明与消费者漂移」或「第二事实源」。</reversibility>
  <read_first>
    - `frontend/style.css` L204-L221 —— 字号 / 字重 / 行高三个刻度块的**现状逐字**(`--text-xs 12` / `--text-base 14` / `--text-md 16` / `--text-lg 18` / `--text-xl 24`,头注释写 `5 sizes`)
    - `frontend/style.css` L616-L626 —— `.markdown-body` 与其 h1/h2/h3 三条规则**现状逐字**;注意 L620-622 的注释已经写着硬规则 9(作用域栅栏),**该注释必须原样保留**
    - `frontend/style.css` L5-L6 / L342-L343 —— 围栏的 START / END 标记(两条守卫都断言该对恰为 1/1,不得改写、移动或复制)
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`### 最终字号阶梯(D-06 / D-07,定稿)` —— 7 档表、插入位置与「按名字序不按数值序」的理由、`--text-2xl` 名同值不同的警示原文
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`### 标题映射(D-06,定稿)` 与 §`### 字号刻度的范围栅栏(Pitfall M4 / TYPE-01)` —— 四条 chrome 覆盖与 `.markdown-body` 的层叠不相遇的机械理由、`.markdown-body` 的四个宿主
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`### 既有档的消费者迁移核账(不得出现孤儿档)` —— `--text-lg` / `--text-md` / `--text-xl` 三档迁移后的净消费者数
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`## 基线与契约漂移口径(D-01 / D-02 / D-03)` 的 D-03 分类表 —— 哪一条断言改令牌接线、哪六条保持字面 px(照抄进计划)
    - `scripts/check-05-ui-uat.py` L102-L133(`ok` / `ok_true` 的 BLOCKED 语义)、L258-L291(`resolve_color` / `resolve_token`)、L594-L620(item3 的令牌接线范本)、L707-L810(item4 全文,`:742` 的改写对象与六条字面守卫所在)
    - `scripts/check-01-token-conformance.sh` —— 围栏外裸 hex 必须 0、tier-1 名不得出围栏(新声明 `var(--text-2xl)` 不触发 tier-1 分支)
    - `scripts/check-02-contrast.py` L136-L175 —— 覆盖率下限 24/20/4 与「raw `/* PAIR` 标记数必须等于解析数」;本计划不改清单
  </read_first>
  <action>
    **第 1 步 —— 围栏内新增两档(D-06 / D-07)。** 在 `frontend/style.css` 围栏内 `--text-xl: 24px;`(HEAD L209)之后**紧接**插入两行,按**名字序**而非数值序:`--text-2xl: 22px;` 然后 `--text-3xl: 28px;`。插入后 `--fw-*`(HEAD L211-215)与 `--lh-*`(HEAD L218-221)三块**一字不动** —— D-10 明确要求零新增行高令牌。围栏标记 `/* ===== DESIGN TOKENS: START ===== */` 与 `/* ===== DESIGN TOKENS: END ===== */` 必须仍各恰一处。

    **第 2 步 —— 改写围栏 L204 的头注释(D-07 / 05-N-1 / A-6)。** 头注释现状是「Type scale — 5 sizes …」;改写为 7 档,并**必须**写明:契约 `04-UI-SPEC.md` 的字号表把 `--text-2xl` 写作 18px、`--text-3xl` 写作 22px,而本围栏的 `--text-2xl` 是 22px、`--text-3xl` 是 28px —— **名同值不同,不是笔误**;理由是 18px 已被 `--text-lg` 占用,而 D-07 要求继续跟随 `xs / base / md / lg / xl` 的尺寸递进命名法,于是 2xl 只能是 xl(24)之上的下一档。同时写明「数值序与名字序在 `xl`(24) → `2xl`(22)这一处不单调」。这段注释的作用是防止日后有人把 22px「修正」回 18px —— 那会让 18px 有两个令牌名,即第二事实源。注释里不得使用 `…` 省略号替代档位清单(决策覆盖门按 `D-NN` 字面 token 扫描,逐条写全)。

    **第 3 步 —— 围栏外三条 `font-size` 改值(TYPE-01)。** `.markdown-body h1` 的 `font-size` 由 `var(--text-xl)` 改为 `var(--text-3xl)`;`.markdown-body h2` 由 `var(--text-lg)` 改为 `var(--text-2xl)`;`.markdown-body h3` 由 `var(--text-md)` 改为 `var(--text-lg)`。**只改这三个值**。同文件 L623 的共享规则(`margin` / `line-height: var(--lh-tight)` / `font-weight: var(--fw-semibold)`)一字不动 —— D-09 与 D-10 对这两项要求零改动。L620-622 的注释(已写着硬规则 9 的作用域栅栏)原样保留。**绝不新增全局 `h1, h2, h3` 规则** —— 那是硬规则 9 与本阶段最容易犯且最难发现的一处错误。

    **第 4 步 —— `scripts/check-05-ui-uat.py` 的断言更新(D-02 / D-03)。**
    (a) **新增三条令牌接线断言**(D-03 第一类):`.markdown-body h1` / `h2` / `h3` 的 computed `font-size` 分别等于 `resolve_token(page, "--text-3xl")` / `resolve_token(page, "--text-2xl")` / `resolve_token(page, "--text-lg")`。探针选择器必须落在真实宿主上 —— item4 在 p1 样本下已用 `#draft-content`(带 `.markdown-body`)作探针,故写 `#draft-content h1` / `#draft-content h2` / `#draft-content h3`,并在每条断言旁用 `info()` 打印解析值(这是「接线对但值错」留下的人工核对痕迹)。若探针元素不存在,`ok()` 记 BLOCKED,绝不记 PASS。
    (b) **改写 `:742` 的 `#brainstorm-view h2` 字号断言(D-02)**:字面 `"16px"` 改为 `resolve_token(page, "--text-md")`。该断言守卫的 14px 值已由 quick `260918-qrq` 推翻,继续硬编码只会继续假 FAIL。
    (c) **六条字面 px 守卫逐条保持不动(D-03 第二类)**:`.panel-header h2` 14px、`#draft-view h2` 18px、`.overlay-card h3` 24px、`#draft-content` 16px(`.markdown-body`)、`.markdown-body code` 14px、`--text-base == "14px"`(S-2 依赖)。**这是本任务最容易做错的一处**:把这六条改成令牌接线表述会让它们退化为同义反复,而它们存在的全部理由恰恰是保证本任务的标题改动没有溢出到 chrome。

    **第 5 步 —— 运行时验证(硬规则 7)。** 改完 `style.css` 后必须实跑四条命令并记录原始输出:CHECK-01、CHECK-02、`check-05 --item 4`、以及 `--item smoke`。CHECK-02 在本计划之后必须仍是 43 对 + `ORDER 0.363` —— 本计划不动任何颜色令牌值、不动清单。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>non-zero exit, or the only stdout line is not exactly `PASS`</fails_when>
    <automated>python3 scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>the last line is not exactly `PASS: 0 failures`, or the command exits non-zero</fails_when>
    <automated>python3 scripts/check-02-contrast.py | grep '^PASS  ' | wc -l</automated>
    <fails_when>the count is not 43</fails_when>
    <automated>python3 scripts/check-02-contrast.py | grep '^ORDER 0.363  --color-text-muted before --color-text on --color-surface' | wc -l</automated>
    <fails_when>the count is not 1</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 4</automated>
    <fails_when>exit code is not 0, or the `=== 逐项结论 ===` block reports anything other than `item 4: PASS`</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item smoke</automated>
    <fails_when>exit code is not 0, or the summary reports anything other than `item smoke: PASS`</fails_when>
    <automated>grep -o -- '--text-2xl: 22px;' frontend/style.css | wc -l; grep -o -- '--text-3xl: 28px;' frontend/style.css | wc -l</automated>
    <fails_when>either count is not exactly 1</fails_when>
    <automated>grep -o 'font-size: var(--text-3xl);' frontend/style.css | wc -l; grep -o 'font-size: var(--text-2xl);' frontend/style.css | wc -l; grep -o 'font-size: var(--text-lg);' frontend/style.css | wc -l</automated>
    <fails_when>the first two counts are not 1, or the third count is less than 2 (`.markdown-body h3` 与 `#draft-view h2, #rounds-placeholder h2` 都消费 `--text-lg`)</fails_when>
    <automated>grep -E '^[[:space:]]*(h1|h2|h3)[[:space:],{]' frontend/style.css | wc -l; grep -oE '(^|[,{ ])[[:space:]]*h1[[:space:]]*,[[:space:]]*h2' frontend/style.css | wc -l</automated>
    <fails_when>the second count is not 0 (a global `h1, h2` rule would be the phase's worst and least visible error — 硬规则 9)</fails_when>
  </verify>
  <acceptance_criteria>
    - `grep -o -- '--text-2xl: 22px;' frontend/style.css | wc -l` == 1 且 `grep -o -- '--text-3xl: 28px;' frontend/style.css | wc -l` == 1
    - `grep -n -- '--text-2xl: 22px;' frontend/style.css` 的行号**大于** `grep -n -- '--text-xl: 24px;' frontend/style.css` 的行号(名字序:2xl 插在 xl 之后)
    - `grep -o 'font-size: var(--text-3xl);' frontend/style.css | wc -l` == 1 且该行选择器是 `.markdown-body h1`
    - `grep -o 'font-size: var(--text-2xl);' frontend/style.css | wc -l` == 1 且该行选择器是 `.markdown-body h2`
    - `grep -o 'font-size: var(--text-lg);' frontend/style.css | wc -l` == 2(`.markdown-body h3` 与 `#draft-view h2, #rounds-placeholder h2`)
    - 围栏内 `--text-*` 声明数为 7(`grep -oE '^[[:space:]]*--text-[a-z0-9]+:' frontend/style.css | wc -l` == 7)
    - 围栏标记仍恰为 1/1:`grep -o '===== DESIGN TOKENS: START' frontend/style.css | wc -l` == 1 且 `grep -o '===== DESIGN TOKENS: END' frontend/style.css | wc -l` == 1
    - 围栏 L204 注释含 `7` 与 `22px` 与 `18px` 三个 token,并含「名同值不同」语义的中文表述(人工逐字核)
    - `git diff -- frontend/style.css` 的 hunk 里没有任何新增的全局 `h1` / `h2` / `h3` 选择器(硬规则 9)
    - `git diff --stat -- frontend/app.js frontend/index.html frontend/vendor/` 为空
    - `check-05-ui-uat.py` 内 `resolve_token(page, "--text-3xl")` / `resolve_token(page, "--text-2xl")` / `resolve_token(page, "--text-lg")` 各出现 ≥1 次
    - `check-05-ui-uat.py` 内 `"16px"` 作为 `#brainstorm-view h2` 期望值的断言**已不存在**(D-02),而 `.panel-header h2` 的 `"14px"`、`#draft-view h2` 的 `"18px"`、`.overlay-card h3` 的 `"24px"` 三条字面断言**仍在**(D-03 第二类)
    - `--item 4` 与 `--item smoke` 两项均 PASS(0 FAIL / 0 BLOCKED)
    - `--text-xl` 仍 ≥1 消费者:`grep -o 'var(--text-xl)' frontend/style.css | wc -l` ≥ 1
  </acceptance_criteria>
  <done>围栏内 7 档字号刻度落地,`.markdown-body h1/h2/h3` 解析为 28 / 22 / 18px;L204 注释写明 7 档与「名同值不同」;`check-05` 的三条新断言与 D-02 改写落地、六条字面守卫未动;CHECK-01 PASS、CHECK-02 仍 43 对 + `ORDER 0.363`、`--item 4` 与 `--item smoke` 全 PASS。</done>
</task>

<task type="auto">
  <name>Task 2: 行高注释改写 + TYPE-02 复证证据(零 CSS 改动)</name>
  <files>frontend/style.css, scripts/check-05-ui-uat.py</files>
  <read_first>
    - `frontend/style.css` L217-L221 —— 行高块**现状逐字**:头注释写「four, paired with the size scale (24/32, 12/16, 14/20, 18/28, 16/26)」
    - `frontend/style.css` L629-L646 —— `.markdown-body blockquote`(`border-left: 3px solid var(--color-border)` + `color: var(--color-text-muted)`)、`.markdown-body th, .markdown-body td`(`font-size: var(--text-base)`)、`.markdown-body code`(`font-size: var(--text-base)`)三处**现状逐字**
    - `frontend/style.css` L548-L549 —— `--lh-compact` 的**唯一**消费者 `.overlay-card p`(chrome-only 行高,不属字号刻度配对)
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`### 行高:D-10 —— 复用 --lh-tight,零新增令牌` —— 比率配对表 7 行、两处必须一并修正的既有缺陷(`18/28` 算术错误、`four` 与三档不自洽)
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`### TYPE-02 —— 认定已由 qrq 实现,本阶段只做复证(D-08)` —— 三处判定与「不得为了有交付物而重写这三处的值」的明文禁令
    - `frontend/style.css` L72-L115 —— 围栏内 role-band 记录块的**注释register 范本**(数字内联、点名 `scripts/check-02-contrast.py` 为仲裁者、显式声明不采信上游 AA 论断)
    - `scripts/check-05-ui-uat.py` L707-L770 —— item4 里 `renderMarkdown` 探针的既有写法(`host.innerHTML = ''` + `host.appendChild(renderMarkdown(...))`)与 `.markdown-body` / `.markdown-body code` 两条字面守卫
  </read_first>
  <action>
    **第 1 步 —— 改写围栏 L217 的行高头注释(D-10),并把两处既有缺陷一并修掉。** 头注释从「**整数配对**」改为「**比率配对**」,并写出 7 行配对表:`12/16.00`(`--lh-tight`)、`14/20.00`(`--lh-snug` 1.4286)、`16/26.00`(`--lh-reading` 1.625)、`18/24.00`(`--lh-tight`)、`24/32.00`(`--lh-tight`)、`22/29.33`(`--lh-tight`,非整数)、`28/37.33`(`--lh-tight`,非整数)。改写时必须同时修正两处既有缺陷,否则新注释仍自相矛盾:**(a)** 现状的 `18/28` 是**算术错误** —— `--text-lg` 18px 配 `--lh-tight` 1.3333 得 **24**,不是 28,新注释必须写 `18/24`;**(b)** 头注释说 `four` 而上表只列三档配对,`--lh-compact`(1.5556)是**纯 chrome** 行高(唯一消费者 `.overlay-card p`),不属字号刻度配对 —— 给它单列一行并注明「chrome-only」,**或**删掉 `four` 这个词,二者择一,不得保留现状的不自洽。注释里必须写明「整数配对在数学上不可得」的理由:28k 与 22k 同时为整数要求 k 是 0.5 的倍数,而 k = 1.5 太松(28 × 1.5 = 42px,标题会散开)。**只改注释,`--lh-*` 四条声明一字不动。**

    **第 2 步 —— TYPE-02 复证(D-08,零 CSS 改动)。** **不得**改写 `.markdown-body th, .markdown-body td` / `.markdown-body code` / `.markdown-body blockquote` 三处的任何值 —— 那会把一个已经正确的状态改坏,并让 `--text-base` 的消费者计数漂移。本步骤只**出可核证据**,分两层:
    (a) **源断言**:`grep -n 'font-size: var(--text-base);' frontend/style.css` 必须命中 `.markdown-body th, .markdown-body td` 与 `.markdown-body code` 两处(HEAD 行号 `:639` 与 `:645`);`grep -n 'color: var(--color-text-muted);' frontend/style.css` 必须命中 `.markdown-body blockquote`(HEAD 行号 `:633`)。
    (b) **运行时断言**(硬规则 7 要求至少一项运行时验证):在 item4 里**扩展现有的 `renderMarkdown` 探针串**,让它一次渲染出「代码跨度 + 表格 + 引用块」三种元素,然后新增两条令牌接线断言:`.markdown-body` 宿主内的 `td` 的 computed `font-size` == `resolve_token(page, "--text-base")`;同一宿主内的 `blockquote` 的 computed `color` == `resolve_color(page, "--color-text-muted")`。探针沿用 item4 既有的 `#draft-content` 宿主与 `host.innerHTML = ''` + `host.appendChild(renderMarkdown(...))` 写法(真实渲染路径,零网络、零 AI 调用)。若元素未渲染出来,`ok()` 必须记 BLOCKED,绝不记 PASS。**既有两条字面守卫(`#draft-content` 16px、`.markdown-body code` 14px)保持字面 px 不动**(D-03 第二类)。

    **第 3 步 —— 实跑验证。** 改完必须实跑 CHECK-01、CHECK-02 与 `--item 4`,并记录 `--text-base` 的消费者计数(HEAD 实测为 19 处,本计划之后应仍为 19 处 —— 本任务零 CSS 声明改动,迁移核账是净不变:`--text-md` 失去 `.markdown-body h3`、获得 `#btn-authorize` 是 Plan 02 的事,本计划不触碰 `#btn-authorize`)。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>non-zero exit, or the only stdout line is not exactly `PASS`</fails_when>
    <automated>python3 scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>the last line is not exactly `PASS: 0 failures`, or the command exits non-zero</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 4</automated>
    <fails_when>exit code is not 0, or the `=== 逐项结论 ===` block reports anything other than `item 4: PASS`</fails_when>
    <automated>grep -o -- '--lh-tight: 1.3333;' frontend/style.css | wc -l; grep -o -- '--lh-snug: 1.4286;' frontend/style.css | wc -l; grep -o -- '--lh-compact: 1.5556;' frontend/style.css | wc -l; grep -o -- '--lh-reading: 1.625;' frontend/style.css | wc -l</automated>
    <fails_when>any of the four counts is not exactly 1</fails_when>
    <automated>grep -o '18/28' frontend/style.css | wc -l</automated>
    <fails_when>the count is not 0 (the pre-existing arithmetic error must be gone from the rewritten comment)</fails_when>
    <automated>grep -n 'font-size: var(--text-base);' frontend/style.css</automated>
    <fails_when>fewer than 2 matching lines, or the matched selectors are not `.markdown-body th, .markdown-body td` and `.markdown-body code`</fails_when>
    <automated>grep -n -A 4 '^\.markdown-body blockquote {' frontend/style.css | grep 'color: var(--color-text-muted);' | wc -l</automated>
    <fails_when>the count is not 1</fails_when>
  </verify>
  <acceptance_criteria>
    - 围栏 L217 注释含 `18/24` 且**不含** `18/28`(`grep -o '18/28' frontend/style.css | wc -l` == 0)
    - 改写后的注释里 `--lh-compact` 有独立一行并注明 chrome-only,**或**头注释里不再出现 `four`(二者至少满足其一)
    - 注释含 `22/29.33` 与 `28/37.33` 两个比率配对串
    - `--lh-tight` / `--lh-snug` / `--lh-compact` / `--lh-reading` 四条声明逐字节未变(四个 `grep -o … | wc -l` 各 == 1)
    - `.markdown-body th, .markdown-body td` 与 `.markdown-body code` 两处的 `font-size` 仍逐字为 `var(--text-base)`,`.markdown-body blockquote` 的 `color` 仍逐字为 `var(--color-text-muted)`(零 CSS 改动,D-08)
    - item4 内新增两条 TYPE-02 运行时断言(表格 `td` 字号、引用块 `color`),且 `--item 4` 全 PASS(0 FAIL / 0 BLOCKED)
    - 本任务**不产生任何新的声明行**:四条 `--lh-*` 声明与三条 TYPE-02 声明的逐字断言(上一条与「.markdown-body th/td 与 code 仍为 var(--text-base)」)已覆盖全部被触碰的声明;本任务的改动面**只有**围栏 L217 的注释文本与 item4 里新增的两条断言
    - `--text-base` 的消费者计数仍为 19(`grep -o 'var(--text-base)' frontend/style.css | wc -l` == 19;HEAD 实测 19,本任务零 CSS 声明改动)
  </acceptance_criteria>
  <done>行高注释改写为比率配对、`18/24` 修正到位、`four` 与三档的不自洽消解、`--lh-*` 四条声明零改动;TYPE-02 三处的源断言 + 两条运行时断言齐备且全 PASS。</done>
</task>

<task type="auto">
  <name>Task 3: 字重三档分工显式化 —— 五只动作按钮 600 → 500</name>
  <files>frontend/style.css, scripts/check-05-ui-uat.py</files>
  <read_first>
    - `frontend/style.css` L648-L656(`#btn-approve-draft`)、L878-L884(`#btn-process-round`)、L928-L935(`#btn-authorize`)、L940-L947(`#btn-start-writing`)、L999-L1008(`#btn-continue-check, #btn-continue-repair`)—— 六条动作按钮规则的**现状逐字**;注意 L661-L668 的 `#btn-divergence`(琥珀族,**不在**六个之列)
    - `frontend/style.css` L432(`.panel-header h2` = `--fw-medium`)、L405-L410(`#doc-panel-header h1` = `--fw-medium`)、L623(`.markdown-body h1, h2, h3` = `--fw-semibold`)—— 分工表的三处既有正确形态
    - `frontend/style.css` L211-L215 —— 字重三档声明(`--fw-regular` / `--fw-medium` / `--fw-semibold`)
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` §`### TYPE-03 —— 字重三档分工显式化(D-09)` —— 分工表(内容标题 600 / chrome 标题 500 / **按钮 500** / 徽标与事件 chip 600 / 唯一例外 `#btn-authorize` 600 / 次级说明 400)、逐行改值表、`#btn-divergence` 为何不在六个之列
    - `.planning/phases/idi-05-typography-and-visual-hierarchy/05-CONTEXT.md` D-09 / D-12 —— 分工规则与「不可逆按钮的字重例外 600」是 D-09 的**唯一已登记例外**
    - `scripts/check-05-ui-uat.py` L102-L133(`ok` 的 BLOCKED 语义)与 L594-L700(item3 的令牌接线范本与既有的 `#btn-authorize` 三属性断言)
  </read_first>
  <action>
    **第 1 步 —— 五条规则的 `font-weight` 改值(D-09)。** 把下列五处规则的 `font-weight` 由 `var(--fw-semibold)` 改为 `var(--fw-medium)`:HEAD L654(`#btn-approve-draft`)、L882(`#btn-process-round`)、L945(`#btn-start-writing`)、L1003(`#btn-continue-check, #btn-continue-repair`)。**只改这四行(五只按钮)。** `#btn-authorize`(HEAD L933)保持 `var(--fw-semibold)` —— 这是 D-12 的**唯一已登记例外**,理由:核心价值要求授权绝不与例行混同,而它有四个可用强调通道(形态 / 色深 / 字号 / 字重),此处用满。`#btn-divergence`(HEAD L666)保持 `var(--fw-semibold)` —— 它属于 `--color-action-warning` 族,不在六个动作按钮之列,拉进来会在三段坡道之外造出一个未登记的第四档。**不得触碰任何 `:disabled` 行**(L656 / L884 / L935 / L947 / L1005-1008 的 `opacity: 0.55` / `0.5` 逐字节不动,Pitfall M5 / D-14)。

    **第 2 步 —— 运行时断言(D-03 第一类,新增)。** 在 item4 里新增六条 `font-weight` 断言:五只按钮(`#btn-approve-draft` / `#btn-process-round` / `#btn-start-writing` / `#btn-continue-check` / `#btn-continue-repair`)的 computed `font-weight` == `"500"`,`#btn-authorize` 的 == `"600"`。理由与形态:**这些是本阶段主动改动的值**,故按 D-03 第一类写成对**字面档值**的断言(500 / 600 是 `--fw-medium` / `--fw-semibold` 的运行时值,而 Chrome 把 `font-weight` 序列化为无单位的数字串,`resolve_token` 读到的自定义属性值是 `"500"` / `"600"`,两者可直接比较;若实跑发现序列化形式不同,以实跑输出为准并在 `info()` 里记录解析值)。**注意:六只按钮全部常驻 DOM**,`getComputedStyle` 对 `display: none` 的元素仍返回解析后的 `font-weight`(它不依赖布局),故在 item4 的 p1 与 p3 两个样本下都能读到;这与该文件现在就在 p3 里读 `#btn-authorize` 而不检查可见性是同一个事实。

    **第 3 步 —— 实跑验证并记录字重消费计数。** 本任务之后 `--fw-medium` 的消费者数应从 4 升到 8、`--fw-semibold` 从 12 降到 8 —— 两档都远 ≥1,不产生孤儿令牌。实跑 CHECK-01 / CHECK-02 / `--item 4` / `--item smoke` 并记录原始输出。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>non-zero exit, or the only stdout line is not exactly `PASS`</fails_when>
    <automated>python3 scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>the last line is not exactly `PASS: 0 failures`, or the command exits non-zero</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 4</automated>
    <fails_when>exit code is not 0, or the `=== 逐项结论 ===` block reports anything other than `item 4: PASS`</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item smoke</automated>
    <fails_when>exit code is not 0, or the summary reports anything other than `item smoke: PASS`</fails_when>
    <automated>grep -o 'var(--fw-medium)' frontend/style.css | wc -l; grep -o 'var(--fw-semibold)' frontend/style.css | wc -l</automated>
    <fails_when>the first count is not 8, or the second count is not 8</fails_when>
    <automated>grep -o 'opacity: 0.55;' frontend/style.css | wc -l; grep -o 'opacity: 0.5;' frontend/style.css | wc -l</automated>
    <fails_when>the first count is not 6, or the second count is not 2 (HEAD 实测:0.55 六处 = L656 / L668 / L884 / L935 / L947 / L1006,0.5 两处 = L961 / L1034;本计划不改任何 opacity 值,故这两个数是本任务必须保持的不变量)</fails_when>
    <automated>grep -n -A 6 '^#btn-divergence {' frontend/style.css | grep -o 'font-weight: var(--fw-semibold);' | wc -l</automated>
    <fails_when>the count is not 1 (the amber divergence entry must keep 600 — it is not one of the six action buttons)</fails_when>
  </verify>
  <acceptance_criteria>
    - `grep -o 'var(--fw-medium)' frontend/style.css | wc -l` == 8(HEAD 4 + 本任务 4 行覆盖 5 只按钮)
    - `grep -o 'var(--fw-semibold)' frontend/style.css | wc -l` == 8(HEAD 12 − 4)
    - `#btn-authorize` 规则的 `font-weight` 仍为 `var(--fw-semibold)`(D-12 的唯一例外)
    - `#btn-divergence` 规则的 `font-weight` 仍为 `var(--fw-semibold)`
    - 八处 `:disabled` 的 `opacity` 值逐字节未变(`grep -o 'opacity: 0.55;' frontend/style.css | wc -l` == 6、`grep -o 'opacity: 0.5;' frontend/style.css | wc -l` == 2;HEAD 实测 0.55 六处 = L656 / L668 / L884 / L935 / L947 / L1006,0.5 两处 = L961 / L1034,本计划不改任何 opacity 值)
    - item4 内六条 `font-weight` 断言存在(五只 500 + `#btn-authorize` 600),`--item 4` 与 `--item smoke` 全 PASS
    - 本任务内 `frontend/style.css` 的变更**只有** `font-weight` 四行(不含任何选择器增删):由「`var(--fw-medium)` 出现次数 4 → 8、`var(--fw-semibold)` 出现次数 12 → 8」与「`#btn-authorize` / `#btn-divergence` 的 `font-weight` 仍为 `var(--fw-semibold)`」共同证明;选择器行数与名字未变由 `grep -oE '^#btn-(approve-draft|process-round|start-writing|authorize|continue-check)' frontend/style.css | wc -l` == 10 佐证(HEAD 实测 10:五只按钮各命中**基础规则**与 `:disabled` 规则两行 —— L648/L656、L878/L884、L928/L935、L940/L947、L999/L1005;该计数守卫的是「选择器名与行数未增删」,故本任务之后仍为 10)
  </acceptance_criteria>
  <done>五只动作按钮的字重为 500,`#btn-authorize` 与 `#btn-divergence` 保持 600;`--fw-medium` 消费 8 / `--fw-semibold` 消费 8;六条运行时断言齐备且 `--item 4` / `--item smoke` 全 PASS。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 本阶段无新增信任边界 | 纯 `frontend/style.css` 的声明值改动 + `scripts/check-05-ui-uat.py` 的断言改动。零新增网络面、零新增输入面、零新增依赖、零新增文件(`frontend/app.js` / `index.html` / `vendor/` 零 diff) |
| 磁盘 → 浏览器 | `frontend/style.css` 是唯一被消费的样式来源;围栏 `:root` 是令牌的唯一事实源。任何绕过围栏的字面量都会削弱「值层改动不产生假 FAIL」这条 04.1 已立的性质 |
| 人类 → 流程 | G3 授权按钮的**视觉形态**是核心价值红线的机器可读信号(未经用户明确授权,流程绝不进入撰写总设计文档)。本计划改字重,该信号由 Plan 02 的形态改动承载 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-05-01 | Elevation of Privilege | `#btn-authorize`(G3 授权门)的视觉形态 | high | mitigate | 本计划把按钮统一到 500,但 `#btn-authorize` 按 D-12 保持 600(唯一已登记例外);Plan 02 的 D-04 断言(三档两两不同 + 档内相同)是该红线的机器化形态;`--color-action-irreversible*` 保持单消费者(D-15) |
| T-idi-05-02 | Tampering | `frontend/style.css` 围栏与四条守卫的不变量 | medium | mitigate | 每个任务复跑 CHECK-01 / CHECK-02;围栏标记 1/1;`^\.hidden {` == 1;`!important;` 声明数 == 1;本计划不改任何颜色令牌值,故 CHECK-02 的 43 对与 `ORDER 0.363` 必须逐字不变 |
| T-idi-05-03 | Tampering | 全局 `h1, h2, h3` 规则泄漏到 chrome | medium | mitigate | 硬规则 9;`grep -oE '(^\|[,{ ])[[:space:]]*h1[[:space:]]*,[[:space:]]*h2' frontend/style.css \| wc -l` == 0;六条 chrome 字面 px 守卫保持不动(D-03 第二类),它们是唯一能抓到该泄漏的形态 |
| T-idi-05-04 | Denial of Service | 渲染回归(标题 / 字重) | medium | mitigate | 每个 `style.css` 任务带至少一项运行时验证(硬规则 7):`--item 4` + `--item smoke` 在 p1 / p3 两个真实样本上读 computed style |
| T-idi-05-05 | Information Disclosure | 本阶段的改动内容 | low | accept | 改动只有字号与字重两个声明值,无用户数据、无网络请求、无外部资源;`frontend/vendor/` 仍只含 `marked.min.js` |
| T-idi-05-SC | Tampering | npm / pip / cargo 安装 | high | mitigate | 本阶段零安装(硬规则 6):不新增任何依赖、文件或构建步骤;Gate 3 断言 `frontend/vendor/` 仍只含 `marked.min.js`、`git status --porcelain frontend/` 只出现 `style.css`。无 `[ASSUMED]` / `[SUS]` 包,故无需 package-legitimacy 人工签核门 |
</threat_model>

<verification>
- `bash scripts/check-01-token-conformance.sh` → `PASS` / exit 0
- `bash scripts/check-03-hidden-uniqueness.sh` → `PASS`(`^\.hidden {` == 1)
- `bash scripts/check-04-important-count.sh` → `PASS`(`!important;` 声明数 == 1)
- `python3 scripts/check-02-contrast.py` → `PASS: 0 failures`,43 对(34 TEXT + 9 NON-TEXT)+ `ORDER 0.363`(本计划不改清单)
- `.venv/bin/python scripts/check-05-ui-uat.py --item smoke,4` → 两项全 PASS(0 FAIL / 0 BLOCKED)
- Gate 2:`comm -23 <(grep -o 'var(--[a-z0-9-]*' frontend/style.css | sed 's/var(//' | sort -u) <(grep -o '\-\-[a-z0-9-]*:' frontend/style.css | sed 's/:$//' | sort -u)` 输出为空(每个被消费的自定义属性都已声明)
- Gate 3:`git status --porcelain -- frontend/` 的输出行**只**出现 `frontend/style.css`(先捕获 `git` 的退出码再判读输出,不要把 `git` 放在管道非末段);`ls frontend/vendor/` 只有 `marked.min.js`
</verification>

<success_criteria>
- 7 档字号刻度落地,`.markdown-body h1/h2/h3` = 28 / 22 / 18px,四处 chrome 覆盖未被带偏(SC1)
- 字重三档分工显式化:五只动作按钮 500,`#btn-authorize` / `#btn-divergence` 600
- TYPE-02 三处复证成立且零 CSS 改动,证据为源断言 + 两条运行时断言
- 两处围栏注释(字号档数、行高配对)与代码一致,既有算术错误与不自洽消解
- 四条既有守卫全绿,`frontend/app.js` / `index.html` / `vendor/` / `ui-states/` 零 diff
</success_criteria>

<output>
Create `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-01-SUMMARY.md` when done
</output>
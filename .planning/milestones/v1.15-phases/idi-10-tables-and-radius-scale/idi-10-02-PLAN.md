---
phase: idi-10-tables-and-radius-scale
plan: 02
type: execute
wave: 2
depends_on:
  - idi-10-01
files_modified:
  - frontend/style.css
  - scripts/check-10-idi10-validation.py
  - .planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/
autonomous: true
requirements:
  - RADIUS-01
  - RADIUS-02

estimate:
  tokens: 50000
  raw_tokens: 50000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- RADIUS-01 — the token is gone, and gone from both places it was consumed ----
    - "圆角刻度只剩三档:`grep -cF -- '--radius-lg' frontend/style.css` 为 **0**;围栏(`===== DESIGN TOKENS: START/END` 之间)内的 `--radius-lg` 声明数为 **0**;`grep -o -- 'var(--radius-lg)' frontend/style.css | wc -l` 为 **0**(全文零引用)。这三个量是**独立**判据,不得只数一个 —— 本机 `grep` 是 ugrep,`-` 算词字符,`\\b` 对含连字符的令牌名不可靠"
    - "围栏内 `--radius-sm: 8px;` / `--radius-md: 10px;` / `--radius-pill: 999px;` 三条声明**值逐字未变**;**围栏内无未消费的令牌声明**(D-04 / Hard Rule 5:never declare a token you are not consuming)⇒ `--radius-lg` 是**删除**而非保留"
    - "`--radius-md` **不得删除** —— `scripts/check-09-idi09-validation.py` 动态解析它做卡片断言(令牌相对,改值不破;**删该令牌会破**)。判据:`.venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2` 仍 `exit=0`、0 FAIL / 0 BLOCKED"
    - "围栏内那条 `/* Radius — … values. */` 注释已由 `four values` 改为 `three values` 并记下被删的 28px 档与两处消费者的去向(注释与代码不互相矛盾);**注释里不得出现字面量令牌名 `--radius-lg`**(否则上面那条 `grep == 0` 立刻红),要指代它时用 `28px` 那一档 / 「former fourth step」这类行文"
    # ---- RADIUS-02 — re-attributed, not re-valued; the two destinations DIFFER on purpose ----
    - "`.chat-user` 的**四个物理角长手**逐角读数:`border-top-left-radius` / `border-top-right-radius` / `border-bottom-left-radius` 三者 == 运行时解析的 `--radius-md`(**本阶段唯一外观真的变了的消费者**:HEAD 上 28px 大圆角气泡 → 10px 卡片圆角),`border-bottom-right-radius` == 解析后的 `--radius-sm`(8px,气泡尾巴尖角**保留**)。**不得断言简写 `border-radius`**:该规则体内另有 `border-bottom-right-radius: var(--radius-sm)`,Chrome 把简写序列化成**三值** —— HEAD 上 `getComputedStyle(el)['border-radius']` 与 `getPropertyValue('border-radius')` 均为 `\"28px 28px 8px\"`、收敛后均为 `\"10px 10px 8px\"`,故 `== \"10px\"` 这条断言**不可满足**;四角长手与 `scripts/check-09-idi09-validation.py:147` 的 `border-top-left-radius` 读法同形。该元素的读数由 harness 用**应用自身的** `appendChatMessage('user', …)` 造出探针气泡后取得(`scripts/ui-states/p1/` 无 `transcript.md` ⇒ 自然状态下 `.chat-user` 不存在;手法与 `scripts/check-05-ui-uat.py:876-879` 同款),每次读数前重建"
    - "`#chat-input-row input` 的计算 `border-radius` == 运行时解析的 `--radius-pill`(`999px`);四个角长手等值;计算 `min-height` 仍为 `52px`。**两处去向不同是承重点,不得「统一」成同一个令牌** —— 一律改成 `--radius-md` 会让输入框外观真的变化(胶囊 → 10px 圆角矩形),那是用户没选的档位"
    - "`#chat-input-row input` 的**外观与收敛前一致**,以收敛**前后**的运行时读数并排为证:(a) 该元素的整份 computed style 前后差异键集合非空、是**八个**圆角相关键 —— 四个物理角长手(`border-top-left-radius` / `border-top-right-radius` / `border-bottom-left-radius` / `border-bottom-right-radius`)**加上**四个逻辑别名(`border-start-start-radius` / `border-start-end-radius` / `border-end-start-radius` / `border-end-end-radius`)—— 的**子集**,且**四个物理角长手必须全部**落在差异集合里 —— 任何**其它**键出现差异即判失败(实测:该元素 radius 由 28px → 999px 时,差异键恰为这 8 个;四个逻辑别名与物理角**同步变化**且同在 `getComputedStyle` 的迭代名单里,故允许集合必须覆盖它们);(b) `getBoundingClientRect()` 前后逐值相同(布局零变化);(c) 该元素的元素级截图前后**逐字节相同**。**不得**用「28px 会被钳成胶囊」这条算术推断替代上述任一条"
    - "`.chat-user` 与 `#chat-input-row input` 的规则块位置与选择器文本逐字未变(**就地改归属**,不搬迁、不追加覆盖规则);两条规则体上方各自带一段注释说明「为什么它去这一档」(否则会被后人「统一」掉)"
    # ---- 不得碰 ----
    - "`#doc-panel-header` 的 `border-radius: 0;` **一字未动** —— 它是就地改写过的**显式零值**、不消费任何 `--radius-*` 令牌,带一段 2026-09-26 的论证(溢出容器把后代裁到带圆角的 padding box),与本阶段的收敛无关"
    - "零新增颜色值、零新增 tier-1 primitive、零新增 `!important`、零新增 `@media` / `@layer` / `@property` / `var(--x, #fallback)`;`grep -o '/\\* PAIR' frontend/style.css | wc -l` 仍为 53、`grep -o '/\\* ORDER' frontend/style.css | wc -l` 仍为 1(圆角不涉色,零清单增删)"
    # ---- gates ----
    - "四个静态门全绿(`check-01` / `check-03` / `check-04` 打印 `PASS`;`check-02` 打印 `PASS: 0 failures`)"
    - "`.venv/bin/python scripts/check-10-idi10-validation.py --item r1` 与 `--item r2` 各自 `exit=0`、0 FAIL / **0 BLOCKED**(任何 BLOCKED 都说明探针没读到元素,不构成 PASS);`--item t1 --item t2` 仍全绿(计划 01 的表格断言未被本计划打破)"
    - "`.planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/` 下存在 `input-radius-before.{png,json}` 与 `input-radius-after.{png,json}` 四个文件;两份 JSON 各带捕获时 `frontend/style.css` 的 sha256,使证据可定位到具体版本"

  artifacts:
    - path: "frontend/style.css"
      provides: "围栏内 `--radius-lg: 28px;` 一行被删除、`/* Radius — … values. */` 注释改写为 `three values` 并记下被删档位;`.chat-user` 的 `border-radius` 由 `var(--radius-lg)` 改为 `var(--radius-md)`(尖角 `border-bottom-right-radius: var(--radius-sm)` 逐字保留);`#chat-input-row input` 的 `border-radius` 由 `var(--radius-lg)` 改为 `var(--radius-pill)`"
      contains: "border-radius: var(--radius-pill);"
    - path: "scripts/check-10-idi10-validation.py"
      provides: "追加 `r1`(圆角三档:围栏内声明数、三档两侧写死字面量、`.chat-user` 的 10px 与 8px 尖角)/ `r2`(`#chat-input-row input` 的胶囊归属 + 四角等值 + `min-height` 52px)两个断言集;追加 `--radius-snapshot {before,after} DIR` 单元素取证模式(整份 computed style dump + 矩形 + 元素截图 + 源码 sha256)"
      contains: "--radius-snapshot"
    - path: ".planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/"
      provides: "圆角收敛的**前后并排**运行时取证:`input-radius-before.{png,json}`(HEAD 状态)与 `input-radius-after.{png,json}`(收敛后),供独立复核「输入框外观零变化」与「只有圆角键变了」"

  key_links:
    - from: "`frontend/style.css` 的 `.chat-user { border-radius: var(--radius-md); }`"
      to: "围栏内既有的 `--radius-md: 10px;`"
      via: "var() 引用 —— 与卡片容器同档:28px 大圆角气泡收进卡片档"
      pattern: "border-radius: var\\(--radius-md\\);"
    - from: "`frontend/style.css` 的 `#chat-input-row input { border-radius: var(--radius-pill); }`"
      to: "围栏内既有的 `--radius-pill: 999px;`"
      via: "var() 引用 —— 如实登记:该元素 `min-height: 52px`,28px 下早已被钳成胶囊,改记 `--radius-pill` 是**外观零变化**的归位"
      pattern: "border-radius: var\\(--radius-pill\\);"
    - from: "`frontend/style.css` 的 `.chat-user { border-bottom-right-radius: var(--radius-sm); }`"
      to: "围栏内既有的 `--radius-sm: 8px;`"
      via: "逐字保留 —— 气泡尾巴的尖角是本阶段**刻意不动**的形态"
      pattern: "border-bottom-right-radius: var\\(--radius-sm\\);"
    - from: "`scripts/check-10-idi10-validation.py` 的 `--radius-snapshot` 产出的两份 JSON"
      to: "「输入框外观零变化」这一结论"
      via: "整份 computed style 的键级 diff + `getBoundingClientRect()` 逐值比对 + 同名 PNG 的逐字节比对 —— 是测量,不是算术推断"
      pattern: "input-radius-(before|after)"
    - from: "`scripts/check-09-idi09-validation.py` 对 `--radius-md` 的动态解析"
      to: "围栏内的 `--radius-md: 10px;` 声明"
      via: "该门在 HEAD 上已通过;`--radius-md` 若被删除,该门立刻红 ⇒ 它是「不得删 `--radius-md`」这条禁令的探测器"
      pattern: "resolve_token\\(\\\"--radius-md\\\"\\)"

  prohibitions:
    - statement: "**不得把两处消费者统一成同一个令牌。** 两处去向**不同**是本阶段的承重点:`.chat-user` → `var(--radius-md)`,`#chat-input-row input` → `var(--radius-pill)`。前者真的是大圆角气泡(外观**真变**),后者 `min-height: 52px` 下 28px 早已被 UA 钳到胶囊(外观**零变化**,改记令牌是如实登记)。一律改成 `--radius-md` 是用户没选的档位(ROADMAP Pitfalls 第 1 条)"
      status: active
      verification: flagged
    - statement: "不得删除或改写 `--radius-md` 令牌本身 —— `scripts/check-09-idi09-validation.py` 动态解析它做卡片断言(令牌相对,改值不破;删该令牌会破)。判据是那道门在本计划后仍 `exit=0`"
      status: active
      verification: flagged
    - statement: "不得改动 `#doc-panel-header` 的 `border-radius: 0;`(以及它上方那段 2026-09-26 的论证注释)。它是显式零值、不消费任何 `--radius-*` 令牌,与本阶段的收敛无关"
      status: active
      verification: flagged
    - statement: "不得用「28px 会被钳成胶囊」这条**算术推断**替代测量。判据必须取收敛**前后**的真实运行时读数并排比对:computed style 的键级 diff + `getBoundingClientRect()` + 元素截图的逐字节比对。钳制的落点依赖元素实际高度,而高度受字体与内边距影响,不是常量"
      status: active
      verification: flagged
    - statement: "不得用「刷新指纹」的写法对待任何连带证据 —— 本计划产出的前后读数必须是**新取**的两次真实读数(前一次在 HEAD 状态下、后一次在收敛后)。**不得**把同一次读数复制成两份、不得只跑一次后改标签"
      status: active
      verification: flagged
    - statement: "不得移动任何既有规则块的位置,不得追加覆盖规则。两处消费者的改动都是**就地改归属**(选择器文本与规则块位置逐字不变);围栏内的删除是**删行**,不是在别处补一条同名声明"
      status: active
      verification: flagged
    - statement: "不得新增 `!important`(`check-04` 按 `!important;` **声明**计数恒为 1;注释里也不得出现该字面量 —— 散文会把 `grep -c` 顶高,本项目已因此红过三次);不得令牌化 `display`;不得引入 `@layer` / `@property` / `var(--x, #fallback)` / `@media`(`check-05` 有一条静态断言锁死 style.css 里 `@media` 计数 == 1)。围栏内注释不得出现「令牌名 + 冒号」形态(`check-02` 的 `DECL_RE` 扫围栏全文含注释);围栏外注释不得含裸 `#hex` / `var(--radix-…` / `var(--white)`"
      status: active
      verification: flagged
    - statement: "不得改动 `scripts/check-05-ui-uat.py` 任何一行(它在 `idi-08` 的 `covered_files` 里,改它会把连带指纹重验名单从 1 份变成 2 份);不得改动 `scripts/check-01…04` / `check-06` / `check-07` / `check-09` / `probe-*`。本计划对 `scripts/` 的唯一改动是 `scripts/check-10-idi10-validation.py`"
      status: active
      verification: flagged
    - statement: "不得改动 `frontend/app.js` / `frontend/index.html` / `frontend/vendor/`(零字节);不得新增依赖、构建步骤或任何新的应用文件(DESIGN.md D-06)。不得顺手改图标与空状态 / 暗色模式 / `.overlay-card` 底色 / 页面级留白 / 输入框 UA 白填充 —— 用户本次未点名的四项 Phase 9 开放项。截图与前后取证不得落进 `frontend/`"
      status: active
      verification: flagged
---

<objective>
把圆角刻度由 `8 / 10 / 28 / 999` 收敛为 `8 / 10 / 999` 三档:删掉从未并入刻度的 `--radius-lg: 28px`,并把它的**两处消费者按各自真实形态改归既有档位**。

Purpose: `--radius-lg: 28px` 是 quick `260918-qrq` 那次临时视觉 pass 手调进来的(`git log -S` 已核实),由提交「令牌值层换血」引入,**从未并入任何刻度声明** —— `04-UI-SPEC.md` 的圆角账本至今还写着 `4px / 8px / 999px`,连 `--radius-lg` 这个名字都没出现过。它是「临时视觉 pass 的手调值」,与后来被清掉的 `20px` 字号越轨值是**同一次 quick 的同型产物**。它只有 **2 处消费者**,且这两处的**去向不同**,这正是本阶段的承重点(用户 2026-09-27 裁定「**严格收敛: 8 / 10 / 胶囊(推荐)**」,D-10-2):

| 消费者 | HEAD 现值 | 改为 | 外观后果 |
|---|---|---|---|
| `.chat-user` | `var(--radius-lg)` | `var(--radius-md)` | **真的变了**:28px 大圆角气泡 → 10px 卡片圆角,收进 Phase 9 的卡片语言 |
| `#chat-input-row input` | `var(--radius-lg)` | `var(--radius-pill)` | **零变化**:`min-height: 52px` 下 28px 早已被 UA 钳到 26px ⇒ 它**实际就是**一个胶囊,改记 `--radius-pill` 是**如实登记** |

删令牌而非保留,依据是围栏的 D-04 / Hard Rule 5:「never declare a token you are not consuming」⇒ 消费者搬走后不得留下未消费的 `--radius-lg` 声明。

**为什么必须做前后并排取证。** ROADMAP 明令:Pitfalls 第 2 条禁止把「28px 会被钳成胶囊」当结论用 —— 那是算术推断,不是测量;SC4 要求「以收敛前后的运行时读数并排为证」。钳制的落点依赖元素实际高度,而高度受字体与内边距影响,不是常量。所以本计划先把「收敛前」的**真实读数**取下来(整份 computed style + 矩形 + 元素截图),改完再取一次,然后做三项并排比对:computed style 的键级 diff、矩形逐值比对、元素截图的**逐字节**比对。

Output: `frontend/style.css` 围栏内删一行 + 注释改写 + 两处消费者就地改归属(各自带承重注释);`scripts/check-10-idi10-validation.py` 追加 `r1` / `r2` 与 `--radius-snapshot {before,after} DIR`;`.planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/` 下四份前后取证文件。

**基线口径(磁盘 HEAD 是唯一现实基线)。** 下面每个「现状」值都取自 `frontend/style.css` 的磁盘内容,以**选择器文本 / 令牌名**为锚点(规划期实测的行号会漂,执行器须以选择器文本复核后再动手)。

**HEAD 上的现状(逐字):**

```css
  /* Radius — four values. */
  --radius-sm: 8px;
  --radius-md: 10px;
  --radius-lg: 28px;
  --radius-pill: 999px;
```

```css
.chat-user {
  align-self: flex-end;
  border-radius: var(--radius-lg);
  background: var(--color-surface-user);
  color: var(--color-text);
  border-bottom-right-radius: var(--radius-sm);
}
```

```css
#chat-input-row input {
  flex: 1;
  min-height: 52px;
  padding: var(--space-1-5) var(--space-2-5);
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-composer);
  font-size: var(--text-md);
}
```

**`--radius-lg` 在 HEAD 上的全部出现(实测 3 处):** 围栏内 1 处声明 + `.chat-user` 1 处 + `#chat-input-row input` 1 处。**无任何门 / 探针引用它**(规划期已 grep:7 个门 + 2 个探针零命中)⇒ 删除是安全的。**不得碰**的相邻项:`#doc-panel-header` 的 `border-radius: 0;`(显式零值,不消费任何 `--radius-*` 令牌)。

**前置(执行前须复核,由 `idi-10-01` 落地):** 表格规则已改造(`.markdown-body th` 已有 gray-2 底、`td` 三条边为 `0px`),`scripts/check-10-idi10-validation.py` 已存在且 `--item t1` / `--item t2` 全绿。复核方式:`.venv/bin/python scripts/check-10-idi10-validation.py --item t1 --item t2`。

**一处必须写进计划的口径说明:** 计划 01 已改过 `frontend/style.css`(表格规则),但它**不碰圆角层** —— `#chat-input-row input` 的计算圆角在计划 01 前后逐值相同。故「收敛前」快照在 `idi-10-01` 落地之后取,与「收敛后」快照构成的前后对**干净地隔离了本计划的圆角改动**这一点,须在 SUMMARY 里写明。

**本计划关闭的需求:** RADIUS-01、RADIUS-02。**本计划不触碰:** TABLE-01 / TABLE-02(计划 01 已完成;本计划只保证 `t1` / `t2` 仍绿);REG-03 的门禁复跑与连带指纹重验(计划 03 / 04);`frontend/app.js` / `index.html` / `vendor/` 零字节;`scripts/check-01…04` / `check-05` / `check-06` / `check-07` / `check-09` / `probe-*` 零改动。
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
@.planning/phases/idi-10-tables-and-radius-scale/10-CONTEXT.md
@.planning/phases/idi-10-tables-and-radius-scale/idi-10-PATTERNS.md
@.planning/phases/idi-10-tables-and-radius-scale/idi-10-01-SUMMARY.md
@frontend/style.css
@scripts/check-10-idi10-validation.py
@scripts/check-09-idi09-validation.py
</context>

## Artifacts this phase produces

> 本节的用途:**plan-review-convergence 的 source-grounding pass 读它,把本阶段新建的符号从漂移校验里排除**。
> 本节列出**全阶段**(四个计划)的产出;本计划只登记自己那部分。

**新增文件 / 目录:**

| # | 路径 | 计划 | 备注 |
|---|---|---|---|
| 2 | `.planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/` | **02** | `input-radius-before.{png,json}` / `input-radius-after.{png,json}` —— 圆角收敛的前后并排取证 |
| 3 | `.planning/phases/idi-10-tables-and-radius-scale/screenshots/` | 03 | 供用户评审的 5 个样本截图 |
| 4 | `.planning/phases/idi-10-tables-and-radius-scale/gate-logs/` | 03 / 04 | 一个门一个日志文件 |

**`scripts/check-10-idi10-validation.py` 中由本计划新增的符号:**

| # | 符号 | 种类 | 用途 |
|---|---|---|---|
| 10 | `RADIUS_LITERALS` | 模块常量 | `{"--radius-sm": "8px", "--radius-md": "10px", "--radius-pill": "999px"}` —— 三档的两侧写死字面量(防止「令牌被改坏而消费者仍接线」时假绿) |
| 16 | `r1(page, tmp_root)` | item 函数 | 圆角刻度:围栏内 `--radius-lg` 声明数 == 0、三档解析值与字面量逐条相符、`.chat-user` 的**四个物理角长手**逐角断言(TL / TR / BL == `--radius-md`,BR == `--radius-sm`)—— **不读简写 `border-radius`**(该规则体的 `border-bottom-right-radius` 会让 Chrome 把简写序列化成三值)。`.chat-user` 的每一次读数前都用应用自身的 `appendChatMessage('user', …)` 造出探针气泡(`p1` fixture 无 `transcript.md`,自然状态下该元素不存在) |
| 17 | `r2(page, tmp_root)` | item 函数 | `#chat-input-row input`:计算 `border-radius` == 解析后的 `--radius-pill`、四个角长手等值、`min-height` 仍为 `52px` |
| 18 | `radius_snapshot(page, label, out_dir, tmp_root)` | 函数 | 对 `#chat-input-row input` 取单元素快照:整份 computed style dump(**由属性名迭代构建** —— 实测恰 477 个长手名,含四个物理角长手与四个逻辑别名、**不含** `border-radius` 简写 ⇒ 本计划一切圆角判据一律读四个物理角长手,绝不读 `computed["border-radius"]`)+ `getBoundingClientRect()` + 元素级 PNG + 捕获时 `frontend/style.css` 的 sha256;写 `<DIR>/input-radius-<label>.{json,png}` |
| 21 | `parse_args()` 的 `--radius-snapshot {before,after} DIR` | CLI 参数 | 单元素前后取证模式(与 `--screenshot` 互斥使用优先;两者同时给出时先跑 item、再跑 snapshot、最后跑 screenshots) |
| 20 | `ITEMS` 增加 `r1` / `r2` | 模块常量 | 派发表扩充 |

**就地改值的既有声明(规则块位置与源码顺序逐字不变):**

| # | 符号 | 锚点 | 动作 |
|---|---|---|---|
| 25 | `--radius-lg: 28px;` | `/* Radius — … values. */` 注释之后 | **删除**该行;注释改为 `three values` 并记下被删档位与两处消费者的去向 |
| 26 | `.chat-user` 的 `border-radius` | `.chat-user { … }` 规则体内 | `var(--radius-lg)` → `var(--radius-md)`;`border-bottom-right-radius: var(--radius-sm);` 逐字保留;新增一段说明「为什么去卡片档」的注释 |
| 27 | `#chat-input-row input` 的 `border-radius` | `#chat-input-row input { … }` 规则体内 | `var(--radius-lg)` → `var(--radius-pill)`;`min-height: 52px` 等其余声明逐字保留;新增一段说明「为什么去胶囊档」的注释 |

**本计划明确不产生的新符号:** 零新增令牌、零新增颜色值、零新增 PAIR / ORDER 条目、零新依赖、零新应用文件;`frontend/app.js` / `index.html` / `vendor/` 零字节改动;`#doc-panel-header` 的 `border-radius: 0` 零改动。

## 波次与依赖形状

| 波次 | 计划 | 落点 | 为什么必须在这个位置 |
|---|---|---|---|
| 2 | `idi-10-02`(本计划) | `--radius-lg` 删除 + 2 处消费者改归属 + 前后并排取证 + `r1` / `r2` | 圆角改的是**令牌层**,必须在能对「收敛前」取值之后才能动手;前后读数须在同一个门的同一次运行语义下取得,故本计划先扩展门、再取前值、后改 CSS、再取后值。放在波次 2 是因为它复用波次 1 建好的门骨架,且与波次 1 共用 `frontend/style.css`(同波次会文件冲突) |

<tasks>

<task type="auto" tdd="false">
  <name>Task 1: 给门追加 `--radius-snapshot {before,after} DIR` 取证模式,并在 HEAD 状态取「收敛前」读数</name>
  <files>scripts/check-10-idi10-validation.py, .planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/</files>
  <precondition>.venv/bin/python 可导入 playwright 且自带 chromium 已缓存;`frontend/style.css` 仍处 HEAD 的圆角状态(`grep -cF -- '--radius-lg' frontend/style.css` 输出 3)</precondition>
  <reversibility rating="reversible">只新增一个只读取证模式与四个产物文件;回退是删除该模式与产物目录。</reversibility>
  <read_first>
    - `scripts/check-10-idi10-validation.py`(计划 01 的产出)—— `load_check05()` / `png_size()` / `fence_text()` / `ITEMS` / `parse_args()` / `main()` 的现有形态;本任务要在其上追加一个模式,不重写既有部分
    - `scripts/check-09-idi09-validation.py` 的 `run_screenshots()` 与 `main()` 的 `--screenshot` 参数处理 —— **本任务要照抄的「一个额外 CLI 模式」形态**:参数在 `parse_args` 里声明、在 `main()` 的 item 派发之后按需调用、产物目录由调用方显式给定且 `mkdir(parents=True, exist_ok=True)`
    - `scripts/check-05-ui-uat.py` 的 `read_style()` / `resolve_color()` / `resolve_token()` / `make_fixture()` / `enter_project()` / `STATES` / `ok` / `ok_true` / `blocked` / `info` —— 本任务复用的全部设施
    - `frontend/style.css` 的 `#chat-input-row input` 规则体(`flex: 1; min-height: 52px; padding: …; border: 1px solid var(--color-border-strong); border-radius: var(--radius-lg); box-shadow: var(--shadow-composer); font-size: var(--text-md);`)与 `#chat-input-row { display: flex; gap: var(--space-2); margin-top: var(--space-2-5); }`
    - `frontend/index.html` 里 `#chat-input-row` 与 `#message-input` 的 DOM 形态(确认该 input 在 `p1` 样本下可见)
    - `.planning/ROADMAP.md` §`### Phase 10:` 的 Success Criterion 4 与 Pitfalls 第 1、2 条(两处去向不同 / 不得用算术推断)
  </read_first>
  <action>
    **第 1 步 —— 追加 CLI 参数。**

    在 `parse_args()` 里加一个参数:`--radius-snapshot`,带**两个**位置值 —— 形如 `--radius-snapshot before DIR` / `--radius-snapshot after DIR`。用 `nargs=2` 或两个独立参数均可,但用户可见形态必须是「标签 + 目录」两个值,且标签只接受 `before` / `after`(其它值 `raise SystemExit` 并给出可用取值)。帮助文本写明:对 `#chat-input-row input` 取一次单元素快照,写 `<DIR>/input-radius-<标签>.{json,png}`。

    **第 2 步 —— 实现 `radius_snapshot(page, label, out_dir, tmp_root)`。**

    进入 `p1` 样本(check-05 的 `make_fixture` + `enter_project`),然后对选择器 `#chat-input-row input`:

    (a) **让元素失焦**:截图前先 `page.evaluate` 把 `document.activeElement` blur 掉(避免焦点环或闪烁的光标进入元素截图,使前后比对失去可比性)。

    (b) **整份 computed style dump**:`page.evaluate` 遍历 `getComputedStyle(el)` 的**全部**属性名,返回 `{属性名: 值}` 的普通对象。这是「外观零变化」在键级上的判据 —— 任何与圆角无关的键出现差异都意味着改动溢出。
    ⚠ **这条迭代不枚举 `border-radius` 简写**(实测迭代名单恰 **477** 个长手名,`names.includes('border-radius')` 为 **false**;四个物理角长手与四个逻辑别名**都在**名单里)。故本计划**所有**圆角判据一律读四个**物理角长手**(`border-top-left-radius` / `border-top-right-radius` / `border-bottom-left-radius` / `border-bottom-right-radius`),**不**读 `computed["border-radius"]` —— 后者在这个字典里**不存在**,读它会抛 `KeyError`。若确要看简写,只能另用 `getPropertyValue('border-radius')` 显式取值;本计划不需要它。

    (c) **几何**:`page.evaluate` 取 `el.getBoundingClientRect()` 的 `x / y / width / height / top / right / bottom / left`。布局零变化的判据。

    (d) **令牌解析**:用 `c05.resolve_token` 依次解析 `--radius-sm` / `--radius-md` / `--radius-lg` / `--radius-pill`,做成一个 `tokens` 字典。收敛前 `--radius-lg` 应解析出 `28px`;收敛后应为 `None`(令牌已不存在)—— 这一处**允许**前后不同,且它是**预期**的差异。

    (e) **源码指纹**:对 `frontend/style.css` 求 sha256 十六进制摘要,写进 JSON 的 `style_css_sha256`。使每份证据可定位到它捕获时的具体版本 —— 这是「前后是两次**真实**读数、不是同一次复制两份」的可复核凭据。

    (f) **元素级截图**:`page.locator("#chat-input-row input").screenshot(path=out_dir / f"input-radius-{label}.png")`,然后**逐张**用 `png_size()` 断言宽高非零(元素截图没有固定的 1440×900,故断言 `width > 0 and height > 0`,并把实际宽高写进 INFO 行)。

    (g) **落盘 JSON**:`out_dir / f"input-radius-{label}.json"`,`json.dumps(..., ensure_ascii=False, indent=2)`。`out_dir.mkdir(parents=True, exist_ok=True)`。

    (h) **stdout 可读输出**:用 `info()` 打印 `label`、`out_dir`、`style_css_sha256`、`rect`、`tokens` 与**四个物理角长手**的读数 —— 使复查者不看 JSON 也能读到关键读数。(若也想看简写,须另用 `getPropertyValue('border-radius')` 显式取,不能从 `computed` 字典取 —— 该字典不含简写键。)

    断言纪律:元素读不到(`read_style` / `evaluate` 返回 `None`)或令牌全部解析不出时走 `blocked()`,**绝不记 PASS**。截图落盘失败或宽高为 0 判 FAIL。

    **第 3 步 —— 在 `main()` 里派发这个模式。**

    在 item 派发**之后**、`--screenshot` 处理**之前**插入:`if args.radius_snapshot: radius_snapshot(page, label, Path(dir), tmp_root)`。`=== 逐项结论 ===` 的汇总块要把 `radius-snapshot` 也作为一项纳入(`item_verdict`),使它参与退出码判定 —— 取证失败必须让门红,不能静默。

    **第 4 步 —— 在 HEAD 状态取「收敛前」快照。**

    跑 `.venv/bin/python scripts/check-10-idi10-validation.py --radius-snapshot before .planning/phases/idi-10-tables-and-radius-scale/radius-snapshots`。

    取完后立刻核对三件事并抄进 SUMMARY:(a) `input-radius-before.json` 里 `tokens["--radius-lg"]` == `"28px"`;(b) `computed` 的**四个物理角长手**(`border-top-left-radius` / `border-top-right-radius` / `border-bottom-left-radius` / `border-bottom-right-radius`)均为 HEAD 的 `28px`(该元素无逐角覆盖,四角等值;`getComputedStyle` 返回**计算值**,不是被钳制后的**使用值** —— 这一点要写进 SUMMARY,否则读者会以为「外观零变化」是从这个数字本身读出来的);(c) JSON 里 `style_css_sha256` 与 `shasum -a 256 frontend/style.css` 的输出一致,证明确实取自当前盘上版本。

    **第 5 步 —— 不触碰范围之外的一切。** 本任务**零 CSS 改动**(`git status --porcelain frontend/` 在本任务后应仍只有计划 01 已改的 `frontend/style.css`;本任务不新增对它的改动)。若第 4 步的快照显示 `tokens["--radius-lg"]` 不是 `28px`,说明 CSS 已被改过 —— **停下,不要继续**,把现状报回。

    **注释与命名纪律:** 新增代码里的注释可以自由写令牌名(它是 `.py`,不受 `check-01` / `check-02` 的围栏规则约束);但**不得**在 `frontend/style.css` 里加任何东西。
  </action>
  <verify>
    <automated>grep -nF -- '--radius-lg' frontend/style.css; echo "rc=$?"</automated>
    <fails_when>the output does not list exactly 3 matching lines (1 fenced declaration + 2 consumers), or rc is not "0" (rc 1 would mean fewer than 3 — the radius state has already moved and this task must not proceed)</fails_when>
    <automated>.venv/bin/python scripts/check-10-idi10-validation.py --radius-snapshot before .planning/phases/idi-10-tables-and-radius-scale/radius-snapshots</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or the "=== 逐项结论 ===" block showing a non-zero BLOCKED count, or the trailing "exit=" line not "exit=0"</fails_when>
    <automated>ls .planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/</automated>
    <fails_when>output does not contain both "input-radius-before.json" and "input-radius-before.png"</fails_when>
    <automated>python3 -c "import json; d=json.load(open('.planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/input-radius-before.json')); c=d['computed']; print(d['tokens']['--radius-lg'], c['border-top-left-radius'], c['border-top-right-radius'], c['border-bottom-left-radius'], c['border-bottom-right-radius'], len(c), d['style_css_sha256'])"</automated>
    <fails_when>the printed token value is not exactly "28px", or any of the four printed corner longhands is not exactly "28px", or the printed computed-style key count is not greater than 100, or the printed sha256 is not a 64-character lowercase hex string</fails_when>
    <automated>git status --porcelain frontend/</automated>
    <fails_when>output contains any path other than "frontend/style.css", or output is empty</fails_when>
  </verify>
  <acceptance_criteria>
    - `scripts/check-10-idi10-validation.py` 的 `--radius-snapshot` 参数接受 `before|after` 两个标签与一个目录;标签取其它值时命令行报错并列出可用取值;`--help` 能读到该参数的用途。
    - `.planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/` 下存在 `input-radius-before.json` 与 `input-radius-before.png` 两个文件。
    - `input-radius-before.json` 含四个顶层键:`computed`(整份 computed style,键数 > 100)、`rect`(含 `x` / `y` / `width` / `height` / `top` / `right` / `bottom` / `left`)、`tokens`(四个 `--radius-*` 的解析值)、`style_css_sha256`。
    - `input-radius-before.json` 的 `tokens["--radius-lg"]` == `"28px"`;`computed` 的**四个物理角长手**(`border-top-left-radius` / `border-top-right-radius` / `border-bottom-left-radius` / `border-bottom-right-radius`)均为 `"28px"`(HEAD 的计算值)。
    - `input-radius-before.json` 的 `style_css_sha256` 与 `python3 -c "import hashlib;print(hashlib.sha256(open('frontend/style.css','rb').read()).hexdigest())"` 的输出逐字符相同。
    - `input-radius-before.png` 的宽高均 > 0(用该脚本自己的 `png_size()` 或 `python3` 读 IHDR 验证)。
    - 该模式的 stdout 上有一组 INFO 行,含 `label`、`out_dir`、`style_css_sha256`、`rect`、四个 `--radius-*` 的解析值,以及**四个物理角长手**的读数。
    - `--radius-snapshot` 作为一项进入 `=== 逐项结论 ===` 汇总,其 FAIL / BLOCKED 计数参与退出码判定。
    - 本任务对 `frontend/style.css` 零改动(`git diff -- frontend/style.css` 相对计划 01 的产出为空)。
  </acceptance_criteria>
  <done>`--radius-snapshot {before,after} DIR` 模式就位并在 HEAD 状态下取到「收敛前」的完整读数:整份 computed style(**四个物理角长手**均为 `28px`;该字典不含简写键)、矩形、四个圆角令牌的解析值(`--radius-lg` == `28px`)、以及可定位版本的一式源码 sha256;元素截图落盘。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 2: 删除 `--radius-lg` + 两处消费者按各自真实形态就地改归属 + 取「收敛后」读数并做三项并排比对(D-10-2 / D-10-3)</name>
  <files>frontend/style.css, .planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/</files>
  <reversibility rating="costly">CSS 侧回退是删两行改两处、单文件即可完成;但回退后必须**重取**「收敛后」快照并重跑比对(旧快照对应的是已不存在的状态),故评级 costly 而非 reversible。</reversibility>
  <read_first>
    - `frontend/style.css` 围栏内的圆角刻度块:注释 `/* Radius — … values. */` 与其下四行声明 —— **以注释与令牌名为锚点定位**
    - `frontend/style.css` 的 `.chat-user` 规则体(逐字:`align-self: flex-end; border-radius: var(--radius-lg); background: var(--color-surface-user); color: var(--color-text); border-bottom-right-radius: var(--radius-sm);`)与它上方/下方的邻居规则 —— 特别注意 `.chat-ai` 与 `.chat-bubble` 附近**已登记的等特异性顺序依赖注释**(「与 .chat-bubble 同特异性(0-1-0),靠源码顺序取胜——不得移到 .chat-bubble 之前」)。**本任务不得移动任何规则块**
    - `frontend/style.css` 的 `#chat-input-row input` 规则体(逐字:`flex: 1; min-height: 52px; padding: …; border: 1px solid var(--color-border-strong); border-radius: var(--radius-lg); box-shadow: var(--shadow-composer); font-size: var(--text-md);`)
    - `frontend/style.css` 的 `#doc-panel-header` 规则体与其上方那段 2026-09-26 的论证注释(含 `border-radius: 0;`)—— **一字不动**的对照物,本任务只读它以确认边界
    - `frontend/style.css` 的 `#doc-panel` 规则与其上方注释 —— **就地改写**的同型先例(注释里逐字写着「是就地改写那条声明,不是追加一条 `border` 覆盖它(留下一条已死的 border-left 会让注释与代码互相矛盾)」)
    - `.planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/input-radius-before.json`(Task 1 的产出)—— 比对基准
    - `scripts/check-09-idi09-validation.py` 的 `c1` 段 —— 它对 `--radius-md` 的动态解析是「不得删 `--radius-md`」这条禁令的探测器
    - `.planning/ROADMAP.md` §`### Phase 10:` 的 Success Criteria 3、4 与 Pitfalls 第 1、2、4 条
    - `.planning/phases/idi-10-tables-and-radius-scale/idi-10-PATTERNS.md` §`--radius-lg 删除 + 2 处消费者改归属` 整节(含「为什么两处去向不同」的表格与两条 ⚠ 警告)
  </read_first>
  <action>
    **第 1 步 —— 删掉围栏内的那一行声明,并同步改写它上方的注释。**

    在圆角刻度块里删除整行 `--radius-lg: 28px;`。保留 `--radius-sm: 8px;` / `--radius-md: 10px;` / `--radius-pill: 999px;` 三行**逐字不变**。

    把上方注释里的 `four values` 改成 `three values`,并在同一段注释里(围栏内)追加三件事:

    (a) 被删的是**28px 那一档**,它由 quick `260918-qrq` 的临时视觉 pass 手调引入、**从未并入任何刻度声明**(`04-UI-SPEC.md` 的圆角账本至今写着 `4px / 8px / 999px`,连这个名字都没出现过);
    (b) 它只有两处消费者,且**去向不同**:`.chat-user` 去了卡片档(它真的是大圆角气泡,外观真变),`#chat-input-row input` 去了胶囊档(该元素在 52px 高下 28px 早已被 UA 钳制,它实际就是一个胶囊,改记是**如实登记**);
    (c) 删而不是留,依据是 Hard Rule 5「never declare a token you are not consuming」。

    ⚠ **围栏内的两条硬约束**(本步骤必须遵守):
    - 注释里**不得出现字面量令牌名 `--radius-lg`** —— 那是「围栏内声明数 == 0」与「全文出现数 == 0」两条判据的**共同**锚点,写了立刻红。要指代它时用「28px 那一档」/「former fourth step」这类行文,**不要**用 `令牌名 + 反引号` 写出来。
    - 围栏内注释**不得出现「令牌名 + 冒号」**形态 —— `scripts/check-02-contrast.py` 的 `DECL_RE` 扫围栏全文(含注释),`--radix-gray-12: …` 这样的写法会被当成一条值不可解析的声明而 FAIL。本段注释里提到其它令牌时写 `--radius-md` 这样的裸名,后面**不要**紧跟冒号。
    - 不得出现字面量 `!important;`(`check-04` 按出现次数计数)。

    **第 2 步 —— `.chat-user` 就地改归属,并加一段说明「为什么去卡片档」的注释。**

    `border-radius: var(--radius-lg);` → `border-radius: var(--radius-md);`

    规则体内其余四行(`align-self` / `background` / `color` / `border-bottom-right-radius: var(--radius-sm);`)**逐字保留** —— 尤其那条 `border-bottom-right-radius: var(--radius-sm)`(8px 尖角,气泡尾巴)是**刻意不动**的形态。

    选择器文本与规则块位置**逐字不变**(就地改归属,不搬迁、不追加覆盖规则)。

    在规则体上方加一段注释(围栏外,故不得含裸 `#hex` / `var(--radix-…` / `var(--white)` / 字面量 `!important;` / `@media`),说明:本元素是**本阶段唯一外观真的变了的消费者**(大圆角气泡 28px → 卡片档 10px,收进 Phase 9 的卡片语言);尖角仍取 `--radius-sm`;⚠ **不得**把它与 `#chat-input-row input` 「统一」成同一个令牌 —— 那一处的真实形态是胶囊,去向不同是刻意的。

    **第 3 步 —— `#chat-input-row input` 就地改归属,并加一段说明「为什么去胶囊档」的注释。**

    `border-radius: var(--radius-lg);` → `border-radius: var(--radius-pill);`

    规则体内其余六行(`flex` / `min-height: 52px` / `padding` / `border` / `box-shadow` / `font-size`)**逐字保留**。选择器文本与规则块位置**逐字不变**。

    在规则体上方加一段注释,说明:该元素 `min-height: 52px`,`28px` 的实际圆角早已被 UA 钳到约一半高度 ⇒ 它**实际就是一个胶囊**,改记 `--radius-pill` 是**如实登记**,外观零变化;⚠ 这一条的判据**不是**上面这条算术,而是 `radius-snapshots/` 里收敛前后的三份并排读数(键级 computed style diff + 矩形比对 + 元素截图逐字节比对)。

    **第 4 步 —— 立刻核对两条「不得破」的判据。**

    (a) `.venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2` 必须仍 `exit=0`、0 FAIL / 0 BLOCKED —— 它动态解析 `--radius-md` 做卡片断言,是「不得删 `--radius-md`」的探测器。
    (b) `frontend/style.css` 里 `#doc-panel-header` 的 `border-radius: 0;` 与其上方注释逐字未动。

    **第 5 步 —— 取「收敛后」快照。**

    跑 `.venv/bin/python scripts/check-10-idi10-validation.py --radius-snapshot after .planning/phases/idi-10-tables-and-radius-scale/radius-snapshots`。

    核对并抄进 SUMMARY:`tokens["--radius-lg"]` 现在是 `None`(令牌已不存在)、`tokens["--radius-pill"]` == `"999px"`、`computed` 的**四个物理角长手**均为 `"999px"`、`style_css_sha256` **已变**(与 before 那份不同 —— 这正是「两次真实读数」的凭据)。

    **第 6 步 —— 三项并排比对(全部必须通过;任一项不通过即停下报回,不得放宽)。**

    (a) **computed style 键级 diff**(用 `python3` 读两份 JSON 的 `computed` 字典):差异键集合必须**非空**,必须是**八个**圆角相关键 —— 四个物理角长手 `border-top-left-radius` / `border-top-right-radius` / `border-bottom-left-radius` / `border-bottom-right-radius`,**加上**四个逻辑别名 `border-start-start-radius` / `border-start-end-radius` / `border-end-start-radius` / `border-end-end-radius` —— 的**子集**,且**四个物理角长手必须全部**出现在差异集合里。任何**其它**键出现差异 ⇒ **判失败,停下报回**(说明改动溢出了)。
      说明:该元素的 radius 由 28px 变 999px 时,实测差异键**恰为上述 8 个** —— 四个逻辑别名与物理角**同步变化**,且同在 `getComputedStyle` 的迭代名单里(实测名单恰 477 个长手名,含这 8 个、**不含** `border-radius` 简写)。「允许差异键集合」必须覆盖预期改动能改到的**每一个**属性,故必须含这四个别名;这条**不**放宽「其它键不得变化」的意图。
    (b) **矩形逐值比对**:两份 JSON 的 `rect` 必须逐值相同(`x` / `y` / `width` / `height` / `top` / `right` / `bottom` / `left`)⇒ 布局零变化。
    (c) **元素截图逐字节比对**:`cmp -s input-radius-before.png input-radius-after.png` 必须 `exit=0`。逐字节相同即「外观与收敛前一致」的直接测量。
      若两张 PNG 不同:先排查可比性(元素是否在同一滚动位置、是否被失焦、窗口尺寸是否一致、是否有动画/光标),把排查结论与两份 PNG 的路径一起写进 SUMMARY 并**报回**;**不得**改用算术推断替代、**不得**只贴其中一张。

    **第 7 步 —— 不触碰范围之外的一切。** 不改 `--radius-sm` / `--radius-md` / `--radius-pill` 的值;不改任何颜色令牌(D-10-3:圆角收敛**只改归属、不改任何颜色**,零新增颜色值、零阈值放宽);不改 PAIR / ORDER 清单;不改 `#doc-panel-header`;不改计划 01 落地的表格规则;不改 `frontend/app.js` / `index.html` / `vendor/`;不改 `scripts/` 下任何既有文件;截图与快照不落进 `frontend/`。
  </action>
  <verify>
    <automated>grep -cF -- '--radius-lg' frontend/style.css; echo "rc=$?"</automated>
    <fails_when>the printed count is not "0", or rc is not "1" (grep exits 1 exactly when it found no line; a count of 0 with rc 0 would mean the file did not exist)</fails_when>
    <automated>awk '/===== DESIGN TOKENS: START/{f=1} f{print} /===== DESIGN TOKENS: END/{f=0}' frontend/style.css | grep -cF -- '--radius-lg'; echo "rc=$?"</automated>
    <fails_when>the printed count is not "0", or rc is not "1" (grep exits 1 exactly when it found no line; a fence that failed to extract would also print 0 — so cross-check that the same awk pipeline without the grep prints a non-empty fence)</fails_when>
    <automated>grep -o -- 'var(--radius-lg)' frontend/style.css | wc -l</automated>
    <fails_when>the count is not exactly "0" (any surviving consumer reference means a consumer was missed)</fails_when>
    <automated>grep -nF -- '--radius-sm: 8px;' frontend/style.css; grep -nF -- '--radius-md: 10px;' frontend/style.css; grep -nF -- '--radius-pill: 999px;' frontend/style.css</automated>
    <fails_when>any of the three greps returns zero matches, or the printed values are not exactly "8px" / "10px" / "999px"</fails_when>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or the "=== 逐项结论 ===" block showing a non-zero BLOCKED count</fails_when>
    <automated>.venv/bin/python scripts/check-10-idi10-validation.py --radius-snapshot after .planning/phases/idi-10-tables-and-radius-scale/radius-snapshots</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or the "=== 逐项结论 ===" block showing a non-zero BLOCKED count, or the trailing "exit=" line not "exit=0"</fails_when>
    <automated>cmp -s .planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/input-radius-before.png .planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/input-radius-after.png</automated>
    <fails_when>non-zero exit (the two element screenshots differ byte-for-byte), or either file missing, or either file empty</fails_when>
    <automated>python3 -c "import json;b=json.load(open('.planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/input-radius-before.json'));a=json.load(open('.planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/input-radius-after.json'));P={'border-top-left-radius','border-top-right-radius','border-bottom-left-radius','border-bottom-right-radius'};L={'border-start-start-radius','border-start-end-radius','border-end-start-radius','border-end-end-radius'};d={k for k in set(b['computed'])|set(a['computed']) if b['computed'].get(k)!=a['computed'].get(k)};print(sorted(d));print('rect_equal',b['rect']==a['rect']);print('subset',d<=P|L,'corners',P<=d,'sha_changed',b['style_css_sha256']!=a['style_css_sha256'])"</automated>
    <fails_when>the printed diff-key list is empty, or "subset" is not True, or "corners" is not True, or "rect_equal" is not True, or "sha_changed" is not True</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>non-zero exit for any of the three, or any of the three not printing exactly "PASS"</fails_when>
  </verify>
  <acceptance_criteria>
    - `grep -cF -- '--radius-lg' frontend/style.css` == **0**;围栏内 `--radius-lg` 计数 == **0**;`grep -o -- 'var(--radius-lg)' frontend/style.css | wc -l` == **0**。三条判据**互相独立**,逐条给出。
    - `grep -nF -- 'Radius — four values' frontend/style.css` 零命中;注释已改为 `three values`,且注释里说明了被删的是 28px 那一档、它从未并入刻度、以及两处消费者的去向。
    - `--radius-sm: 8px;` / `--radius-md: 10px;` / `--radius-pill: 999px;` 三行逐字存在且值未变。
    - `.chat-user` 规则体的 `border-radius` 为 `var(--radius-md);`,`border-bottom-right-radius: var(--radius-sm);` 逐字保留;规则体的选择器文本与其余四行声明逐字未变。
    - `#chat-input-row input` 规则体的 `border-radius` 为 `var(--radius-pill);`,其余六行声明(含 `min-height: 52px;`)逐字未变;规则体的选择器文本未变。
    - `.chat-user` 与 `#chat-input-row input` 规则体**各自上方**有一段注释说明「为什么去这一档」,并明确写出两处去向不同是刻意的、不得统一。
    - `#doc-panel-header` 的 `border-radius: 0;` 与其上方论证注释逐字未动(`grep -nF -- 'border-radius: 0;' frontend/style.css` 仍命中该行)。
    - `.venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2` `exit=0`、0 FAIL / 0 BLOCKED(`--radius-md` 未被删除、卡片圆角断言仍成立)。
    - `radius-snapshots/` 下四份文件齐全;两份 JSON 的 `style_css_sha256` **不同**(证明是两次真实读数);after 的 `tokens["--radius-lg"]` 为 `None`、`tokens["--radius-pill"]` == `"999px"`、`computed` 的**四个物理角长手**均为 `"999px"`。
    - computed style 键级 diff:差异键集合非空、是**八个**圆角相关键(四个物理角长手 + 四个逻辑别名)的子集、**四个物理角长手全部**在内;`rect` 前后逐值相同;两张元素 PNG `cmp -s` 返回 0。
    - 四个静态门全绿;`grep -o '/\* PAIR' | wc -l` == 53、`grep -o '/\* ORDER' | wc -l` == 1。
    - `grep -n '@media' frontend/style.css` 命中恰好 1 行(Phase 7 的 prefers-reduced-motion 块;本阶段不得新增媒体查询)。
    - `git diff -U0 -- frontend/style.css` 人工逐行核对:相对计划 01 的产出,新增改动只有「删 1 行声明 + 改 1 段围栏内注释 + 改 2 处 `border-radius` 值 + 新增 2 段围栏外注释」;**没有任何既有规则块被移动**(diff 里不存在「先删后加同一规则块」的形态);零 `--radix-` 增删行。
    - `git status --porcelain frontend/` 仅列出 `frontend/style.css`(快照与截图未落进 `frontend/`)。
  </acceptance_criteria>
  <done>`--radius-lg` 从围栏内删除,全文与围栏内两个计数、以及 `var(--radius-lg)` 引用数全部为 0;`.chat-user` 收到卡片档(10px)且保留 8px 尖角,`#chat-input-row input` 如实登记为胶囊档(999px);收敛前后的三份并排读数(键级 computed style diff / 矩形逐值 / 元素截图逐字节)全部通过;`check-09` c1/c2 仍绿;四个静态门全绿。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 3: 给门追加 `r1` / `r2` 断言集 —— 圆角三档与两处消费者的运行时判据</name>
  <files>scripts/check-10-idi10-validation.py</files>
  <reversibility rating="reversible">只新增两个断言集与一组常量;回退是删除它们,不影响产品代码。</reversibility>
  <read_first>
    - `scripts/check-10-idi10-validation.py` —— 其 `t1` / `t2` / `fence_text()` / `ITEMS` / `parse_args()` / `main()` 的现有形态(本任务按其同一形态追加)
    - `scripts/check-09-idi09-validation.py` 的 `c1` 段 —— 令牌级「两侧都写死」的断言形态(`SHADOW_CARD_LITERAL` / `CARD_WHITE` 与 `resolve_*` 的双重核对)、元素读不到时 `blocked()` 的处置、`LEFT_SECTIONS` 这类显式清单常量的写法
    - `scripts/check-06-idi05-validation.py` 里读 `borderTopLeftRadius` 的那一段 —— 它只经 `info()` 打印、**不**断言;本任务要补的正是那条「只打印不断言」的缝
    - `scripts/check-05-ui-uat.py:876-879` 的 `.chat-user` 探针构造段(`page.evaluate` 里调**应用自身的** `appendChatMessage('user', …)` 造出气泡,再读它的 `background-color`)与 `:1486` 的纪律登记「这五项断言是**造出容器再断言**,不靠『fixture 里本来就有 .chat-bubble』」—— **本任务 `r1` 要照抄的手法**:`.chat-user` 在 `p1` 下自然不存在,必须先造出探针节点再读数
    - `scripts/ui-states/p1/` 的目录内容(实测只有 `.gitkeep`、无 `transcript.md`)—— 证明 `.chat-user` 不是 fixture 自然渲染出来的
    - `frontend/style.css` 的 `.chat-user` / `#chat-input-row input` 规则体(Task 2 之后的最终形态)
  </read_first>
  <action>
    **第 1 步 —— 加常量。**

    `RADIUS_LITERALS = {"--radius-sm": "8px", "--radius-md": "10px", "--radius-pill": "999px"}`。字面量写死在这里的理由与 `t1` 的 `TH_BG_LITERAL` 同型:本断言的用途正是「运行时读到的值等于用户裁定/刻度声明的那个值」—— 若两侧都从同一个令牌解析,把令牌改坏也照样 PASS。常量上方加注释写明这一点。

    **第 2 步 —— `r1(page, tmp_root)`(圆角刻度 + `.chat-user`)。**

    进入 `p1` 样本,然后:

    (a) **源码文本级**:`fence_text()` 取出围栏内文本,断言其中 `--radius-lg` 计数为 `0`(标签写清「围栏内零声明残留」,并注明这一条读的是文件文本而非渲染结果 —— 与渲染断言互补)。
    (b) **令牌级双侧**:对 `RADIUS_LITERALS` 的三个条目,`resolve_token` 的解析值必须等于写死的字面量(逐条一断言)。
    (c) **先造出 `.chat-user` 探针气泡,再读它(这一步不是可选的,跳过它整组断言必落 BLOCKED)。** `.chat-user` 由 `appendChatMessage('user', …)` 产生,气泡源是 `transcript.md` 经 `renderTranscript()` 灌入的;而 `scripts/ui-states/p1/` **只有 `.gitkeep`**、无 `transcript.md` ⇒ `p1` 的自然状态下**不存在** `.chat-user`,直接 `read_style(page, ".chat-user", …)` 只会拿到 `None` 并落 BLOCKED。本仓库对这件事的既有做法同样是**造出容器再断言**:`scripts/check-05-ui-uat.py:876-879` 正是先 `page.evaluate("() => { appendChatMessage('user', 'harness: .chat-user 探针'); }")` 再读该元素的 `background-color`。本任务照抄这一手 —— 用**应用自身的** `appendChatMessage` 造节点(真实渲染路径,零网络、零 AI 调用),断言才读得到元素。
    ⚠ **每一次读 `.chat-user` 之前都要重新造一次**(不能只在开头造一次):该节点是 harness 造的、不在 fixture 里,任何重新进入样本 / 重新加载都会把它清掉;本步既要读**四个物理角长手**、又要读一条诊断 `info()`,**每次读之前都重新 `appendChatMessage` 一次**,否则后一次读数会落 BLOCKED。
    (d) **`.chat-user` 元素级 —— 逐角读长手,不读简写。** 在 (c) 造出探针之后,读四个**物理角长手**并逐角断言:`border-top-left-radius` / `border-top-right-radius` / `border-bottom-left-radius` 三者均 == `resolve_token("--radius-md")`(HEAD 上是 `28px`,收敛后是 `10px` —— 标签里写真值来源);`border-bottom-right-radius` == `resolve_token("--radius-sm")`(8px 尖角保留)。**不得**断言简写 `border-radius` == `"10px"`:该规则体内另有 `border-bottom-right-radius: var(--radius-sm)`,Chrome 把简写序列化成**三值** —— HEAD 上 `getComputedStyle(el)['border-radius']` 与 `getPropertyValue('border-radius')` 均为 `"28px 28px 8px"`、收敛后均为 `"10px 10px 8px"`;故 `== "10px"` 这条断言**永远不可满足**。四角长手与 `scripts/check-09-idi09-validation.py:147` 的 `border-top-left-radius` 读法同形。另打印一条 `info()` 记下四个角长手的原始读数(可选再加 `getPropertyValue('border-radius')` 的简写值),便于独立诊断「尖角只在一角」这件事。
    (e) **四个物理角长手逐条独立断言**(不是「四角等值」一条带过),标签里写清哪一个角是尖角 —— 这样「保留尖角」这一条不会被后人误读成「四角统一」。

    元素读不到或令牌解析不出时走 `blocked()`,**绝不记 PASS**;但 `.chat-user` 在 (c) 造出探针后**仍**读不到时按 **FAIL** 处理(说明 `appendChatMessage` 没生效、或该类名已改),不得以 BLOCKED 收场。

    **第 3 步 —— `r2(page, tmp_root)`(`#chat-input-row input` 的胶囊归属)。**

    进入 `p1` 样本,对 `#chat-input-row input`:

    - 计算 `border-radius` == `resolve_token("--radius-pill")`(标签注明:该元素 `min-height: 52px`,`getComputedStyle` 返回的是**计算值**,与外观零变化这件事是两回事 —— 外观判据由 `radius-snapshots/` 的前后三份读数承担,标签里点名它,防止读者误读);
    - 四个角长手(`border-top-left-radius` / `border-top-right-radius` / `border-bottom-left-radius` / `border-bottom-right-radius`)彼此等值且等于同一个解析值;
    - 计算 `min-height` 仍为 `52px`(**对照组**:证明那条算术的自变量没被顺手改掉);
    - 计算 `border-top-width` 仍为 `1px` 且 `border-top-style` 仍为 `solid`(**对照组**:`border: 1px solid var(--color-border-strong)` 逐字未动)。

    **第 4 步 —— 把 `r1` / `r2` 挂进派发表与帮助文本。**

    `ITEMS = {"t1": t1, "t2": t2, "r1": r1, "r2": r2}`;`--item` 的帮助文本列出四个取值。

    **第 5 步 —— 复跑并确认计划 01 的断言未被打破。**

    跑 `--item t1 --item t2`(必须仍全绿)、`--item r1 --item r2`(本任务新落地)、以及四个静态门。把每条的 `=== 逐项结论 ===` 块原文抄进 SUMMARY。

    **第 6 步 —— 不触碰范围之外的一切。** 不改 `frontend/style.css`;不改 `scripts/check-05-ui-uat.py` / `check-06` / `check-09` / `check-01…04` / `probe-*`。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-10-idi10-validation.py --item r1</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or the trailing line not starting with "exit=0", or the "=== 逐项结论 ===" block showing a non-zero BLOCKED count for item r1</fails_when>
    <automated>.venv/bin/python scripts/check-10-idi10-validation.py --item r2</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or the trailing line not starting with "exit=0", or the "=== 逐项结论 ===" block showing a non-zero BLOCKED count for item r2</fails_when>
    <automated>.venv/bin/python scripts/check-10-idi10-validation.py --item t1 --item t2</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or the trailing line not starting with "exit=0", or a non-zero BLOCKED count for either item</fails_when>
    <automated>.venv/bin/python scripts/check-02-contrast.py</automated>
    <fails_when>non-zero exit, or any line beginning with "FAIL", or the final line not "PASS: 0 failures"</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>non-zero exit, or stdout not exactly "PASS"</fails_when>
    <automated>bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>non-zero exit for either, or either not printing exactly "PASS"</fails_when>
    <automated>git diff -- frontend/style.css</automated>
    <fails_when>the diff is empty (frontend/style.css is expected to carry this plan's radius convergence at this point)</fails_when>
  </verify>
  <acceptance_criteria>
    - `.venv/bin/python scripts/check-10-idi10-validation.py --item r1` 的 `=== 逐项结论 ===` 块里 `r1` 的 FAIL 与 BLOCKED 计数均为 0,末行 `exit=0`。
    - `.venv/bin/python scripts/check-10-idi10-validation.py --item r2` 的 `=== 逐项结论 ===` 块里 `r2` 的 FAIL 与 BLOCKED 计数均为 0,末行 `exit=0`。
    - `--item t1 --item t2` 仍全绿(计划 01 的表格断言未被本阶段打破)。
    - `r1` 的断言里含一条读围栏文本的 `--radius-lg` 零计数断言,以及三条「`resolve_token` 解析值 == 写死字面量」的令牌级断言(`RADIUS_LITERALS` 三个条目逐条覆盖)。
    - `r1` 对 `.chat-user` 的圆角**逐角读四个物理角长手并逐条断言**(TL / TR / BL == `--radius-md` 解析值,BR == `--radius-sm` 解析值),**不含**任何读简写 `border-radius` 的断言(该规则体的 `border-bottom-right-radius` 会让 Chrome 把简写序列化成三值 `10px 10px 8px`,`== "10px"` 不可满足)。
    - `r1` 在读 `.chat-user` 的**每一次**读数之前都用应用自身的 `appendChatMessage('user', …)` 造出探针气泡(与 `check-05-ui-uat.py:876-879` 同款手法),因此该元素的每一条读数都读到了真实元素而非 `None`;`r1` 的 FAIL / BLOCKED 计数为 0 即证明这一点。**不得**依赖 `p1` fixture 自然存在 `.chat-user`(实测不存在:`scripts/ui-states/p1/` 只有 `.gitkeep`)。
    - `r2` 的断言里含「四角长手彼此等值且 == `--radius-pill` 解析值」、「`min-height` == `52px`」、以及「`border-top-width` == `1px` 且 `border-top-style` == `solid`」三组判据。
    - `r1` / `r2` 的标签里点名了外观判据由 `radius-snapshots/` 的前后读数承担,不把 `getComputedStyle` 的计算值直接当作外观判据。
    - `ITEMS` 含四个键(`t1` / `t2` / `r1` / `r2`);`--item` 帮助文本列出四个取值。
    - 四个静态门全绿(`check-02` 为 `PASS: 0 failures`)。
    - `git diff -- scripts/check-05-ui-uat.py` 为空;`git status --porcelain scripts/` 仅有 `scripts/check-10-idi10-validation.py` 一处改动/新增。
  </acceptance_criteria>
  <done>圆角刻度的渲染判据首次有了自动化运行时覆盖:`r1`(围栏内零残留 + 三档双侧字面量 + `.chat-user` 的四个角长手逐角断言 —— TL/TR/BL 为 10px、BR 为 8px 尖角,探针气泡由应用自身的 `appendChatMessage` 造出)/ `r2`(输入框胶囊归属 + 四角等值 + `min-height` 与边框对照组)全 PASS、0 BLOCKED;计划 01 的 `t1` / `t2` 仍绿;四个静态门全绿。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 无外部输入边界 | 本计划只改 `frontend/style.css` 的**令牌层与两处消费者**(呈现层),并扩展一个**只读**的本地运行时门:零用户输入处理、零鉴权、零数据访问、零网络调用、零新增资源加载。攻击面限于浏览器对 CSS 的解析与渲染,以及门脚本自起 `uvicorn` + 驱动无头浏览器这一次本地动作 |
| 本地进程 / 文件系统边界(取证模式) | `--radius-snapshot` 会读 `frontend/style.css` 做 sha256、写 JSON 与 PNG 到调用方给定的目录。它必须是**只读产品代码、只写自有产物目录** |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-10-01 | Information Disclosure | `.chat-user` / `#chat-input-row input` 的选择器与新的 `border-radius` 值 | low | accept | 选择器只用既有类名与 ID,不含属性选择器、不读用户数据、不引入 `url()` / `@import` / 远程字体。新增声明只有 `border-radius: var(--radius-md)` 与 `border-radius: var(--radius-pill)`,不含任何 URL。验收:`git diff -U0 -- frontend/style.css` 的新增行不含 `url(` / `@import` / `#hex` |
| T-idi-10-02 | Tampering | `--radius-snapshot` 的产物写入与 fixture 生命周期 | **high** | mitigate | 若该模式把产物落进 `frontend/`、或写回被测样本,就会污染被检对象并使后续门读到假状态。缓解:(a) 产物目录由调用方**显式给定**并只 `mkdir(parents=True, exist_ok=True)` 该目录;(b) fixture 走 `c05.make_fixture`,在 `tempfile.mkdtemp()` 下 `copytree` 出副本,`scripts/ui-states/` 零改动,临时根在 `finally` 里 `rmtree`(仅 `--keep` 保留);(c) 该模式对 `frontend/style.css` 只**读**(sha256),从不写;(d) 验收:`git status --porcelain frontend/` 仅含 `frontend/style.css`,`git status --porcelain scripts/ui-states/` 为空,`radius-snapshots/` 的四个文件都在 `.planning/` 下 |
| T-idi-10-03 | Tampering | 「不得删 `--radius-md`」这条禁令的探测器 | high | mitigate | 删除 `--radius-md` 会静默打破 `scripts/check-09-idi09-validation.py`(它动态解析该令牌做卡片圆角断言)。缓解:该门被**显式**纳入本计划 Task 2 与 Task 3 的 `<verify>`,判据是 `--item c1 --item c2` 仍 `exit=0`、0 FAIL / 0 BLOCKED;`<prohibitions>` 逐条列出该禁令 |
| T-idi-10-04 | Repudiation | 「输入框外观零变化」这一结论缺乏可复核的原始证据 | medium | mitigate | 该结论**不得**以算术推断给出。缓解:三项并排测量(整份 computed style 的键级 diff + `getBoundingClientRect()` 逐值比对 + 元素截图 `cmp -s` 逐字节比对),两份 JSON 各带捕获时 `frontend/style.css` 的 sha256(sha256 必须不同 —— 这是「两次真实读数」的凭据),四份产物全部落盘在 `radius-snapshots/` 供独立复核;任一项不通过即停下报回,不得放宽或只贴一张 |
| T-idi-10-05 | Denial of Service | 门脚本的浏览器路线选择与临时目录堆积 | low | mitigate | 该机 `.venv` 的 Python 是 x86_64(Rosetta),`channel="chrome"` + `headless=True` 会 CDP 永不连上、超时挂死。缓解:沿用 `check-09` 的固定写法 `pw.chromium.launch(headless=True)`(固定 bundled,**不提供** `--browser`);临时目录在 `finally` 里 `rmtree`(仅 `--keep` 保留);`radius_snapshot` 复用既有 fixture 机制,不另起服务 |
| T-idi-10-06 | Elevation of Privilege | 无 | low | accept | 本计划不触碰鉴权、权限门、服务端路径或任何 API;纯呈现层改动 + 只读取证,无提权面 |
| T-idi-10-SC | Tampering | npm / pip / cargo 安装 | low | accept | 本阶段**零安装**:零新增依赖、零构建步骤(DESIGN.md D-06 硬约束)。Playwright 与 chromium 均已在项目 `.venv` 中就绪,不触发下载。`frontend/vendor/` 仍只有 `marked.min.js` |
</threat_model>

<verification>
**静态门(全部必须绿):**

- `bash scripts/check-01-token-conformance.sh` → `PASS`
- `.venv/bin/python scripts/check-02-contrast.py` → `PASS: 0 failures`,清单规模 53 对 + 1 条 ORDER 逐字不变
- `bash scripts/check-03-hidden-uniqueness.sh` → `PASS`
- `bash scripts/check-04-important-count.sh` → `PASS`

**既有运行时门(证明没有删错令牌):**

- `.venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2` → `exit=0`,0 FAIL / 0 BLOCKED(`--radius-md` 仍在、卡片圆角断言仍成立)

**本阶段运行时门:**

- `.venv/bin/python scripts/check-10-idi10-validation.py --item r1` → `exit=0`,0 FAIL / 0 BLOCKED
- `.venv/bin/python scripts/check-10-idi10-validation.py --item r2` → `exit=0`,0 FAIL / 0 BLOCKED
- `.venv/bin/python scripts/check-10-idi10-validation.py --item t1 --item t2` → 仍 `exit=0`、0 BLOCKED(计划 01 的表格判据未被打破)

**圆角收敛的三条独立判据:**

- `grep -cF -- '--radius-lg' frontend/style.css` == 0
- `awk '/===== DESIGN TOKENS: START/{f=1} f{print} /===== DESIGN TOKENS: END/{f=0}' frontend/style.css | grep -cF -- '--radius-lg'` == 0
- `grep -o -- 'var(--radius-lg)' frontend/style.css | wc -l` == 0

**前后并排取证(四份产物):**

- `radius-snapshots/input-radius-before.{json,png}` / `input-radius-after.{json,png}`
- computed style 键级 diff:非空、是**八个**圆角相关键(四个物理角长手 + 四个逻辑别名)的子集、**四个物理角长手全部**在内
- `rect` 前后逐值相同
- `cmp -s` 两张元素 PNG 返回 0
- 两份 JSON 的 `style_css_sha256` 不同

**仓库卫生:**

- `git status --porcelain frontend/` 仅列出 `frontend/style.css`
- `ls frontend/vendor/` 仅 `marked.min.js`
- `git diff -- scripts/check-05-ui-uat.py` 为空;`git diff -- scripts/check-01…04` / `check-06` / `check-07` / `check-09` / `probe-*` 全为空
- `grep -o '/\* PAIR' frontend/style.css | wc -l` == 53;`grep -o '/\* ORDER' frontend/style.css | wc -l` == 1
- `grep -c '@media' frontend/style.css` == 1
</verification>

<success_criteria>
- 圆角刻度只剩 `--radius-sm: 8px` / `--radius-md: 10px` / `--radius-pill: 999px` 三档,三行值逐字未变;`--radius-lg` 在围栏内零声明残留、全文零出现、零 `var()` 引用;围栏内无未消费的令牌声明。
- `.chat-user` 的**四个物理角长手**中 TL / TR / BL 等于解析后的 `--radius-md`(卡片档)、BR 等于 `--radius-sm`(8px 尖角保留);`#chat-input-row input` 的计算圆角等于解析后的 `--radius-pill`(999px),`min-height: 52px` 与 `border` 逐字未动。两处去向不同,且有注释写明这是刻意的。
- 「输入框外观与收敛前一致」以**测量**为证,不是算术:computed style 键级 diff(只有圆角键变)、矩形逐值相同、元素截图逐字节相同;两项 JSON 各带捕获时的源码 sha256 且两份不同。
- `--radius-md` 未被删除(`check-09` c1/c2 仍 `exit=0`);`#doc-panel-header` 的 `border-radius: 0` 一字未动。
- 四个静态门全绿;`check-10` 的 `t1` / `t2` / `r1` / `r2` 四个断言集在真实浏览器里全 PASS、0 BLOCKED。
- `scripts/check-05-ui-uat.py` / `check-01…04` / `check-06` / `check-07` / `check-09` / `probe-*` 代码零改动;`frontend/app.js` / `index.html` / `vendor/` 零字节改动;零新增颜色值 / 令牌 / 配对。
</success_criteria>

<output>
Create `.planning/phases/idi-10-tables-and-radius-scale/idi-10-02-SUMMARY.md` when done
</output>

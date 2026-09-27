---
phase: idi-10-tables-and-radius-scale
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - frontend/style.css
  - scripts/check-10-idi10-validation.py
autonomous: true
requirements:
  - TABLE-01
  - TABLE-02

estimate:
  tokens: 60000
  raw_tokens: 60000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- TABLE-01 — rendered, not textual ----
    - "文档区表格在真实浏览器里**不再有竖线与外框**:`.markdown-body td` 的计算 `border-left-width` / `border-right-width` / `border-top-width` 均为 `0px`(HEAD 上是 `1px`)"
    - "`.markdown-body th` 的计算 `background-color` 是 gray-2 —— 等于运行时解析的 `--color-surface`,且等于写死的字面量 `rgb(249, 249, 249)`(两侧都写死,防止「令牌被改坏而消费者仍接线」时假绿);HEAD 上 `th` 无自身底色(透明)"
    - "`.markdown-body th` 与 `.markdown-body td` 的计算 `border-bottom-width` 为 `1px`、`border-bottom-style` 为 `solid`、`border-bottom-color` 等于运行时解析的 `--color-border-subtle`(gray-6)—— 行间与表头下的分隔线是同一档极浅线,不再是原 `--color-border`(gray-7)的深线"
    - "`.markdown-body th, .markdown-body td` 规则体的 `padding` 与 `font-size` 两行**逐字未动**(`font-size` 被 `scripts/check-05-ui-uat.py:1126` 的活断言锁死);`.markdown-body table` 的 `border-collapse: collapse` 一字未动"
    - "原 `border: 1px solid var(--color-border);` 那条声明是**就地改写**成 `border: none;` + `border-bottom: 1px solid var(--color-border-subtle);`,文件里**不存在**一条已死的、被后续规则覆盖的 `border` 声明(留下它会与注释互相矛盾 —— Phase 9 对 `#doc-panel` 的 `border-left` 用的是同一手法)"
    - "`.markdown-body th { background: var(--color-surface); }` 是**追加的新规则块**,插入位置紧接 `th, td` 并集规则之后;既有规则块的相对源码顺序逐字未变(新增块的选择器 `.markdown-body th` 在 HEAD 上不存在,故不参与任何既有等特异性对) —— 三个机器可解析表(批注回应表 / 覆盖维度表 / 未决问题清单)共用**这一条**规则,该一致性是结构性的"
    # ---- TABLE-02 — zero new colour values, zero threshold relaxation ----
    - "表头新绘制面(gray-2)上的文字色配对**已登记**:`.markdown-body th` 的文字色是从 `.markdown-body` 继承的 `--color-text`,而 `/* PAIR --color-text ON --color-surface TEXT */` 早已在围栏内清单里(`frontend/style.css` 的 PAIR 段)⇒ **零新增 PAIR 条目**;`check-02` 的实际输出里含一行 `PASS  <比值>  --color-text on --color-surface`,该行原文须被抄进 SUMMARY 作为证据(**不得**以「我认为已覆盖」结案)"
    - "行间与表头下的分隔线**不新增 NON-TEXT 条目**,其依据是两处**既有登记**而非本阶段的新发明:role-band 段写明「border band 6-8 … three borders stay in band 6-8: they are decorative, and SC 1.4.11 does not apply to a border that identifies nothing」,清单头部注释逐字写着「Decorative separators are deliberately absent — SC 1.4.11 does not apply to a border that identifies nothing」。计划与 SUMMARY 都要**引用这两处原文**,不得只写一句「不需要」"
    - "零新增颜色值、零新增 tier-1 primitive、零阈值改动:`git diff -- frontend/style.css` 的增删行里除 `border` / `background` / 注释外不含任何 `--radix-` 行;`git diff -- scripts/check-02-contrast.py` 为空(`TEXT_MIN` / `NON_TEXT_MIN` 与 HEAD 逐字节相同);`grep -o '/\\* PAIR' frontend/style.css | wc -l` 仍为 53、`grep -o '/\\* ORDER' frontend/style.css | wc -l` 仍为 1"
    - "围栏内注释未新增任何「令牌名 + 冒号」形态(会被 `check-02` 的 `DECL_RE` 当成值不可解析的声明而 FAIL);围栏外注释未新增裸 `#hex` / `var(--radix-…` / 字面量 `!important;`"
    # ---- gates ----
    - "`bash scripts/check-01-token-conformance.sh` 打印 `PASS`;`bash scripts/check-03-hidden-uniqueness.sh` 打印 `PASS`;`bash scripts/check-04-important-count.sh` 打印 `PASS`;`.venv/bin/python scripts/check-02-contrast.py` 打印 `PASS: 0 failures`"
    - "`scripts/check-10-idi10-validation.py` 存在,可用 `.venv/bin/python` 直接运行,退出码语义与 `check-05` 一致(0=全 pass / 1=有 FAIL / 2=有 BLOCKED);`--item`(可重复或逗号分隔)、`--screenshot DIR`、`--keep` 三个参数被 `parse_args` 接受"
    - "`.venv/bin/python scripts/check-10-idi10-validation.py --item t1` 与 `--item t2` 各自 `exit=0`、0 FAIL、**0 BLOCKED**(任何 BLOCKED 都说明探针没读到元素,不构成 PASS);其 INFO 行可见每个 (样本, 宿主) 对的 `th` / `td` 计数与逐条原始读数"
    - "`.venv/bin/python scripts/check-10-idi10-validation.py --screenshot <DIR>` 出图后 `<DIR>` 下**恰有 5 个 PNG**,与 `scripts/check-05-ui-uat.py` 的样本清单 `STATES = [\"p1\", \"p12\", \"p3\", \"checking\", \"archive\"]` 逐项一一对应,每张为 1440×900;该参数在本计划内即已实现(计划 03 直接消费它,其 `files_modified` 不含本脚本,无法自行补救)"

  artifacts:
    - path: "frontend/style.css"
      provides: "`.markdown-body th, .markdown-body td` 的 `border` 声明就地改写为 `border: none;` + `border-bottom: 1px solid var(--color-border-subtle);`;紧随其后新增一条 `.markdown-body th { background: var(--color-surface); }` 规则块;规则体上方新增承重注释(档位依据 / 就地改写的理由 / 装饰性边界的既有登记 / 零新增 PAIR 的依据 / 不得碰 `font-size`)"
      contains: ".markdown-body th { background: var(--color-surface); }"
    - path: "scripts/check-10-idi10-validation.py"
      provides: "Phase 10 的运行时门骨架:docstring 给出「为什么另开一个文件」的实测论证;复用 check-05 的模块级设施(服务生命周期 / fixture / 断言记录器 / 读数器 / 令牌解析 / 样本清单),不重复实现、不改动 check-05 一行;`t1`(表头)/ `t2`(数据格)两个断言集;`--screenshot DIR` 出图;`--json` 报告模式"
      contains: "def main"

  key_links:
    - from: "`frontend/style.css` 的 `.markdown-body th { background: var(--color-surface); }`"
      to: "围栏内 `--color-surface: var(--radix-gray-2);`"
      via: "var() 引用 —— 消费者在围栏外,只写令牌名不写字面量"
      pattern: "background: var\\(--color-surface\\);"
    - from: "`frontend/style.css` 的 `border-bottom: 1px solid var(--color-border-subtle);`"
      to: "围栏内 `--color-border-subtle: var(--radix-gray-6);`(既有的容器边界令牌)"
      via: "与 `#doc-panel` / `.event-list` 的容器边界同令牌 ⇒ 零新增令牌"
      pattern: "border-bottom: 1px solid var\\(--color-border-subtle\\);"
    - from: "`scripts/check-10-idi10-validation.py` 的 `t1` / `t2`"
      to: "`frontend/style.css` 的表格规则在真实浏览器里的 computed style"
      via: "Playwright `getComputedStyle` 读数 —— 表格是**画出来**的,文本里写着 `background` 不等于它真的生效"
      pattern: "read_style\\(page, f\\\"\\{host\\} (th|td)\\\""
    - from: "表头文字色(继承自 `.markdown-body` 的 `--color-text`)在其新绘制面 gray-2 上"
      to: "围栏内既有的 `/* PAIR --color-text ON --color-surface TEXT */`"
      via: "该 PAIR 条目早已登记 ⇒ 零新增配对;判据是 `check-02` 的实际输出行,不是推断"
      pattern: "PAIR --color-text ON --color-surface TEXT"

  prohibitions:
    - statement: "不得改写 `.markdown-body th, .markdown-body td` 的**并集选择器文本**,不得把 `th` 与 `td` 拆成两条规则。拆分是重排风险区(至少一对等特异性规则由源码顺序决定);稳妥形态是保留并集选择器逐字不动,只在其后**追加**一条 `.markdown-body th { … }` 规则块"
      status: active
      verification: flagged
    - statement: "不得移动任何既有规则块的位置(硬规则 3:追加,不重排)。新增的 `.markdown-body th` 规则块插入位置必须紧接 `th, td` 并集规则之后;不得插到 `.markdown-body code` / `.markdown-body h1…` 等既有规则**之前**作为新的前置块"
      status: active
      verification: flagged
    - statement: "不得碰 `td` 的 `font-size`(`scripts/check-05-ui-uat.py:1126` 有活断言 `[p1] .markdown-body td font-size == var(--text-base)`,期望侧由 `resolve_token` 运行时解析 ⇒ 值层不改就恒过;改它就红);不得碰 `padding` 那两行"
      status: active
      verification: flagged
    - statement: "不得改任何 `--radix-*` 原语的值、不得新增任何 tier-1 primitive、不得新增颜色令牌、不得放宽 `scripts/check-02-contrast.py` 的 `TEXT_MIN`(4.5)/ `NON_TEXT_MIN`(3.0)、不得改动该脚本任何一行、不得删除任何 `/* PAIR */` 或 `/* ORDER */` 条目(会同时打破脚本的覆盖地板与 `raw_pairs == len(pairs)` 的标记计数一致性)。表头底色必须落 `--color-surface`(gray-2 = 三级刻度里的「内陷面」档):落 `--color-surface-sunken` 或 `--radix-gray-4` 会同时破坏刻度语言与对比度登记面"
      status: active
      verification: flagged
    - statement: "不得新增 `!important`(check-04 按 `!important;` **声明**计数,恒为 1;散文注释会把 `grep -c` 顶高 —— 本项目已因此红过三次,故本计划加的任何注释都不得含该字面量);不得令牌化 `display`;不得引入 `@layer` / `@property` / `var(--x, #fallback)`;不得新增 `@media`(`scripts/check-05-ui-uat.py` 有一条静态断言: `frontend/style.css` 里 `@media` 计数必须恰为 1 —— Phase 7 的 prefers-reduced-motion 块)"
      status: active
      verification: flagged
    - statement: "不得在围栏内(两行 `===== DESIGN TOKENS: START/END` 之间)的任何注释里写「令牌名 + 冒号」形态(`scripts/check-02-contrast.py` 的 `DECL_RE` 扫围栏全文含注释,会把它当成一条值不可解析的声明而 FAIL);不得在围栏外的任何注释里写裸 `#hex` / `var(--radix-…` / `var(--white)`(`check-01` 扫围栏外全文)。要指代颜色时写令牌名"
      status: active
      verification: flagged
    - statement: "不得改动 `scripts/check-05-ui-uat.py` 的任何一行 —— 它在 `idi-08` 的 `covered_files` 里,改它会把连带指纹的重验面从 1 份变成 2 份(ROADMAP Pitfalls)。本计划对 `scripts/` 的**唯一**新增是 `scripts/check-10-idi10-validation.py`"
      status: active
      verification: flagged
    - statement: "不得改动 `frontend/app.js` / `frontend/index.html` / `frontend/vendor/`(零字节);不得新增依赖、构建步骤、CSS 框架或任何新的应用文件(DESIGN.md D-06 硬约束:零新增运行时依赖、零构建步骤)。零新增颜色值、零新令牌。**不得在本计划内做圆角刻度收敛**(RADIUS-01 / RADIUS-02 属计划 02),也不得顺手改图标与空状态 / 暗色模式 / `.overlay-card` 底色 / 页面级留白 / 输入框 UA 白填充 —— 这四项 Phase 9 的开放项用户本次未点名"
      status: active
      verification: flagged
---

<objective>
把文档区表格从「每格 1px 全边框的电子表格式网格」改为「表头浅底 + 仅横向分隔线」,并把这条渲染判据接进一个新的真实浏览器运行时门。

Purpose: 文档区右栏占比最大的内容就是表格(`docs/discuss-round-N.md` 几乎全是表格,其中三个是 DESIGN.md §6.4 明文规定的机器可解析表),而现规则(全边框、零表头底色)读起来像电子表格,与 Phase 9 刚刚建立的白卡片语言冲突。用户 2026-09-27 在 `AskUserQuestion` 中逐项选定档位:「**表头浅底 + 仅横向分隔(推荐)**」(D-10-1)。表头底色落 **gray-2**(`--color-surface`)不是随便挑的 —— 那正是 Phase 9 建立的三级 elevation 刻度里的「**内陷面**」档(`gray-3 页面 < gray-2 内陷面 < 白卡片`),于是表格从「与卡片语言无关的网格」变成「白卡片内的一个内陷块」。

为什么需要一个**新的**运行时门:规划期已 grep 全部 7 个门脚本 + 2 个探针,**没有任何一条**断言表格的边框 / 底色 / 布局。唯一的接触点是 `scripts/check-05-ui-uat.py:1126` 的 `[p1] .markdown-body td font-size == var(--text-base)`,它断言的**不是**本阶段要改的属性(且期望侧由 `resolve_token` 运行时解析 ⇒ 值层不改就恒过)。TABLE-01 / TABLE-02 的渲染判据在本计划之前**零自动化覆盖**。表格是**画出来**的:文本里写着 `background` 不等于浏览器里真的生效,所以判据必须是 `getComputedStyle` 读数,不是 `grep`。

Output: `frontend/style.css` 的表格规则改造(就地改写一条 `border` 声明 + 紧随其后追加一条 `.markdown-body th` 规则块 + 一段承重注释);新增运行时门 `scripts/check-10-idi10-validation.py`(骨架 + `t1` / `t2` + `--screenshot`);`check-02` 的表头配对实测输出与「零新增 / 零放宽」证据。

**基线口径(磁盘 HEAD 是唯一现实基线)。** 下面每一个「现状」值都取自 `frontend/style.css` 与 `scripts/check-05-ui-uat.py` 的**磁盘内容**,并一律以**选择器文本 / 令牌名**为锚点。规划期实测的行号会漂(本阶段开工时 style.css 已比 Pattern Map 撰写时又多了若干行),执行器须以选择器文本复核后再动手。

**执行前基线(规划期已实测,执行器须复核):**

| 检查 | 规划期在 HEAD 上的实测结果 |
|---|---|
| `bash scripts/check-01-token-conformance.sh` | `PASS` / exit 0 |
| `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`(清单 53 对 + 1 条 ORDER);其中含一行 `PASS  <比值>  --color-text on --color-surface` |
| `bash scripts/check-03-hidden-uniqueness.sh` | `PASS`(`^[[:space:]]*\.hidden[[:space:]]*\{` 计数 == 1) |
| `bash scripts/check-04-important-count.sh` | `PASS`(`!important;` 声明计数 == 1) |
| `grep -o '/\* PAIR' frontend/style.css \| wc -l` | `53` |
| `grep -o '/\* ORDER' frontend/style.css \| wc -l` | `1` |
| `scripts/check-10-idi10-validation.py` | **不存在**(命名空闲:`scripts/` 现有 check-01…check-07 + check-09,**无 check-08**) |

**HEAD 上的目标规则(逐字,以选择器文本为锚):**

```css
.markdown-body table { border-collapse: collapse; }
.markdown-body th, .markdown-body td {
  border: 1px solid var(--color-border);
  padding: var(--space-1) var(--space-2-5);
  font-size: var(--text-base);
}
```

相关令牌(围栏内,值取自磁盘):`--color-border: var(--radix-gray-7)`(`#cecece`,是**深**的那档)、`--color-border-subtle: var(--radix-gray-6)`(`#d9d9d9`,既有的容器边界令牌,`#doc-panel` / `.event-list` 在用)、`--color-surface: var(--radix-gray-2)`(`#f9f9f9`,即 `rgb(249, 249, 249)`,三级刻度的「内陷面」档)、`--color-surface-card: var(--white)`(白卡片)。

**「去掉外框」的判据口径(ROADMAP SC1 的逐字操作定义)。** ROADMAP Success Criterion 1 把「不再有竖线与外框」定义为「`.markdown-body td` 的计算 `border-left-width` / `border-right-width` / `border-top-width` 为 `0px`」。⇒ 单元格**保留一条 `border-bottom`**(行间分隔线 + 表头下边线)是 SC1 明确许可的形态,不是漏改;真正要去掉的是那三条边与它们的深色(`--color-border` gray-7)。本计划因此采用最小的等价形态:把并集规则里那**一条** `border` 声明就地改写成 `border: none;` + `border-bottom: 1px solid var(--color-border-subtle);`,而不是拆选择器或另加 `tr:last-child` 之类的规则。

**本计划关闭的需求:** TABLE-01、TABLE-02。**本计划不触碰:** RADIUS-01 / RADIUS-02(计划 02);REG-03 的门禁复跑与连带指纹重验(计划 03 / 04);`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` 零字节改动;`scripts/check-01…04` / `check-05` / `check-06` / `check-07` / `check-09` / `probe-*` 代码零改动;图标与空状态 / 暗色模式 / `.overlay-card` 底色 / 页面级留白 / 输入框 UA 白填充(用户本次未点名的四项 Phase 9 开放项)。

**为什么本计划与计划 02 不能并行。** 本阶段的改动面是单一文件 `frontend/style.css` 加一个新验证脚本;`execute-phase` 的同波次规则要求同波次计划的 `files_modified` 零重叠,故计划 01 / 02 必须落在两个波次。这不是可以优化的地方 —— 它是「纯 CSS 阶段」的定义。
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
@frontend/style.css
@scripts/check-09-idi09-validation.py
@scripts/check-05-ui-uat.py
</context>

## Artifacts this phase produces

> 本节的用途:**plan-review-convergence 的 source-grounding pass 读它,把本阶段新建的符号从漂移校验里排除**。
> 本节列出**全阶段**(四个计划)的产出;每个计划的 SUMMARY 只登记自己那部分。

**新增文件:**

| # | 路径 | 计划 | 备注 |
|---|---|---|---|
| 1 | `scripts/check-10-idi10-validation.py` | **01**(骨架 + `t1` + `t2` + `--screenshot` + `--json`)/ 02(`r1` + `r2` + `--radius-snapshot`) | Phase 10 的运行时门;复用 check-05 的模块级设施,不重写服务生命周期 |
| 2 | `.planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/` | 02 | `input-radius-before.{png,json}` / `input-radius-after.{png,json}` —— 圆角收敛的前后并排取证 |
| 3 | `.planning/phases/idi-10-tables-and-radius-scale/screenshots/` | 03 | 供用户评审的 5 个样本截图(1440×900) |
| 4 | `.planning/phases/idi-10-tables-and-radius-scale/gate-logs/` | 03 / 04 | 一个门一个日志文件,文件名即门的名字 |

**`scripts/check-10-idi10-validation.py` 的符号清单(创建于计划 01,扩展于计划 02):**

| # | 符号 | 种类 | 计划 | 用途 |
|---|---|---|---|---|
| 5 | `ROOT` | 模块常量 | 01 | 仓库根(`Path(__file__).resolve().parent.parent`) |
| 6 | `CHECK05` | 模块常量 | 01 | `scripts/check-05-ui-uat.py` 的路径 |
| 7 | `STYLE_CSS` | 模块常量 | 01 | `frontend/style.css` 的路径(供源码文本级断言) |
| 8 | `TH_BG_LITERAL` | 模块常量 | 01 | `"rgb(249, 249, 249)"` —— gray-2 的两侧写死字面量(防止「令牌被改坏而消费者仍接线」时假绿) |
| 9 | `TABLE_PROBES` | 模块常量 | 01 | `(样本, 宿主)` 对元组;覆盖 `c05.MARKDOWN_HOSTS` 的**全部四个** doc 宿主(`p1`)加一对自然渲染样本(`p3` / `#round-doc`)。**每个对在读数前都用应用自身的 `renderMarkdown` 注入含表格的探针 markdown**(见 Task 2 第 3 步),故不依赖 fixture 自然渲染 |
| 10 | `RADIUS_LITERALS` | 模块常量 | 02 | `{"--radius-sm": "8px", "--radius-md": "10px", "--radius-pill": "999px"}` —— 三档的两侧写死字面量 |
| 11 | `load_check05()` | 函数 | 01 | `importlib.util.spec_from_file_location` 加载 check-05(文件名含连字符,不能用 `import`) |
| 12 | `fence_text()` | 函数 | 01 | 返回两行 `===== DESIGN TOKENS: START/END` 之间的文本(供「围栏内零声明」断言) |
| 13 | `png_size(path)` | 函数 | 01 | 读 PNG 的 IHDR 取 `(width, height)` |
| 14 | `t1(page, tmp_root)` | item 函数 | 01 | `.markdown-body th`:计算底色 == gray-2、下边线 1px solid、色 == `--color-border-subtle` |
| 15 | `t2(page, tmp_root)` | item 函数 | 01 | `.markdown-body td`:左/右/上边框 `0px`、下边线 1px、色 == `--color-border-subtle`;`font-size` / `padding` 两条对照组 |
| 16 | `r1(page, tmp_root)` | item 函数 | 02 | 圆角三档:围栏内 `--radius` 声明数与三档解析值(字面量对照)+ `.chat-user` 的 10px 与 8px 尖角 |
| 17 | `r2(page, tmp_root)` | item 函数 | 02 | `#chat-input-row input`:计算 `border-radius` == 解析后的 `--radius-pill`,四个角长手等值,`min-height` 仍为 `52px` |
| 18 | `radius_snapshot(page, label, out_dir, tmp_root)` | 函数 | 02 | 单个元素(`#chat-input-row input`)的整份 computed style dump + 元素截图,写 `<label>` 后缀的 `.json` / `.png` |
| 19 | `run_screenshots(page, out_dir, tmp_root)` | 函数 | 01 | 遍历 `c05.STATES`,逐样本出一张 1440×900 整窗截图并逐张断言宽高 |
| 20 | `ITEMS` | 模块常量 | 01(`t1`/`t2`)/ 02(`r1`/`r2`) | item 名 → 函数的派发表 |
| 21 | `parse_args()` | 函数 | 01(`--item` / `--screenshot` / `--json` / `--keep`)/ 02(`--radius-snapshot {before,after}`) | CLI |
| 22 | `main()` | 函数 | 01 | 服务生命周期 + Playwright 启动 + 派发 + `=== 逐项结论 ===` 汇总 + 退出码 |

**就地改写的既有规则(规则块位置与源码顺序逐字不变):**

| # | 符号 | 锚点(选择器文本) | 计划 | 动作 |
|---|---|---|---|---|
| 23 | `.markdown-body th, .markdown-body td` 的 `border` 声明 | `.markdown-body { … }` 之后的 `.markdown-body table` 规则之后 | 01 | `border: 1px solid var(--color-border);` → `border: none;` + `border-bottom: 1px solid var(--color-border-subtle);` |
| 24 | `.markdown-body th { background: var(--color-surface); }` | 紧随 #23 的规则块之后 | 01 | **新增**规则块(插入位置紧接其所有者) |
| 25 | `--radius-lg: 28px;` 声明 | `/* Radius — … values. */` 注释之后 | 02 | **删除**该行;注释同时改为 `three values` 并记下两处消费者的去向 |
| 26 | `.chat-user` 的 `border-radius` | `border-radius: var(--radius-lg);` | 02 | → `var(--radius-md)` |
| 27 | `#chat-input-row input` 的 `border-radius` | `border-radius: var(--radius-lg);` | 02 | → `var(--radius-pill)` |

**明确不产生的新符号:** 零新增 CSS 自定义属性、零新增颜色值、零新增 tier-1 primitive、零新增 PAIR / ORDER 条目、零新依赖、零构建步骤、零新应用文件、`frontend/app.js` / `index.html` / `vendor/` 零字节改动。

## 波次与依赖形状(本阶段的真实约束,不是保守)

| 波次 | 计划 | 落点 | 为什么必须在这个位置 |
|---|---|---|---|
| 1 | `idi-10-01`(本计划) | 表格规则改造 + 运行时门骨架(`t1` / `t2` / `--screenshot`) | 表格与圆角是**两项独立**的视觉改动,但都落在同一个 `frontend/style.css` ⇒ 同波次会文件冲突。表格先做:它不触碰任何令牌层,静态门(check-01/02/03/04)对它结构性失明,故它是最干净的第一刀 |
| 2 | `idi-10-02` | `--radius-lg` 删除 + 2 处消费者改归属 + 前后并排取证 + `r1` / `r2` | 圆角改的是**令牌层**,必须在能对「收敛前」取值之后才能动手(前后读数必须在同一个门的同一次运行语义下取得)。放在波次 2 是因为它要复用波次 1 建好的门骨架 |
| 3 | `idi-10-03` | 五条浏览器门复跑 + 四静态门 + pytest 基线 + 截图 | 回归门必须看到波次 1/2 的**全部**改动。`check-05` 是真实浏览器 UAT,它断言 computed style 与几何 —— 只有它能在两处改动都落地后证明渲染语义仍然成立 |
| 4 | `idi-10-04` | `idi-09-VERIFICATION.md` 以 HEAD 内容重新验证 + REG-03 的「10 份覆盖 / 1 份可执行」分诊证据 | 指纹重验必须看到最终 HEAD(波次 3 之后 `frontend/style.css` 才定型),否则重算出来的 digest 立刻又 stale |

<tasks>

<task type="auto" tdd="false">
  <name>Task 1: 表格规则就地改写 —— 表头 gray-2 浅底 + 仅横向分隔线</name>
  <files>frontend/style.css</files>
  <reversibility rating="reversible">回退是单文件的一条声明还原 + 删除一条新增规则块,不牵连任何其他计划或产物。</reversibility>
  <read_first>
    - `frontend/style.css` 的 `.markdown-body` 段 —— 逐字读 `.markdown-body table { border-collapse: collapse; }`、`.markdown-body th, .markdown-body td { … }`(**本任务的改写目标**)、以及紧随其后的 `.markdown-body code` 规则(用于确认插入位置)。**以选择器文本定位,不要用行号**
    - `frontend/style.css` 的 `.markdown-body { line-height: var(--lh-reading); font-size: var(--text-md); }` —— `th` / `td` 的**文字色**从这里继承(`.markdown-body` 自身不声明 `color`,故最终来自 `html, body` 的 `--color-text`)
    - `frontend/style.css` 围栏内:`--color-surface: var(--radix-gray-2);`、`--color-border: var(--radix-gray-7);`、`--color-border-subtle: var(--radix-gray-6);`、`--color-surface-card: var(--white);`、`--radix-gray-2: #f9f9f9;`、`--radix-gray-6: #d9d9d9;`、`--radix-gray-7: #cecece;`
    - `frontend/style.css` 的 role-band 段(围栏内,`Radix's 12 steps are read as: 1-2 ground / 3-5 component surface / 6-8 border / 9-10 solid fill / 11-12 text` 那一段)与其后关于 `--color-border-strong` 的登记 —— 其中逐字写着「border band 6-8 … The other three borders stay in band 6-8: they are decorative, and SC 1.4.11 does not apply to a border that identifies nothing」。**这是本任务不新增 NON-TEXT 条目的依据,注释须引用它**
    - `frontend/style.css` 的 PAIR 清单头部注释 —— 其中逐字写着「Decorative separators are deliberately absent — SC 1.4.11 does not apply to a border that identifies nothing」,以及 `/* PAIR --color-text ON --color-surface TEXT */` 这一条(**表头文字在其新绘制面上的配对**)
    - `frontend/style.css` 围栏内 `--color-surface-card` / `--shadow-card` 上方那段 Phase 9 的承重注释 —— **本任务要照抄的注释形态**(逐条记下档位依据、为什么就地改写、零新增令牌/配对)
    - `frontend/style.css` 的 `#doc-panel` 规则与其上方注释 —— Phase 9 **就地改写** `border-left` → `border` 的同型先例(注释里逐字写着「是就地改写那条声明,不是追加一条 `border` 覆盖它(留下一条已死的 border-left 会让注释与代码互相矛盾)」)
    - `scripts/check-05-ui-uat.py` 的 `[p1] .markdown-body td font-size == var(--text-base)` 那条断言及其探针宿主 —— **本任务不得改动的属性**
    - `.planning/phases/idi-10-tables-and-radius-scale/10-CONTEXT.md` §D-10-1 与 §「表格:对比度」/§「表格:无门断言」
    - `.planning/ROADMAP.md` §`### Phase 10:` 的 Goal / Deliverables 第 1、3 条 / Success Criteria 1、2 / Pitfalls 第 3、4、6 条
  </read_first>
  <action>
    **第 1 步 —— 就地改写那一条 `border` 声明。**

    在 `.markdown-body th, .markdown-body td` 规则体内,把

    `border: 1px solid var(--color-border);`

    逐字改写成**两行**:

    `border: none;`
    `border-bottom: 1px solid var(--color-border-subtle);`

    `padding: var(--space-1) var(--space-2-5);` 与 `font-size: var(--text-base);` 两行**逐字保留**。选择器文本 `.markdown-body th, .markdown-body td` 与规则块位置**逐字不变**。

    这是**就地改写**,不是追加覆盖规则:`border: none` 去掉四条边(含全部竖线、外框与表行之间的**深**线 `--color-border` gray-7),紧随的 `border-bottom` 再把「行间分隔线 + 表头下边线」按 D-10-1 指定的极浅档 `--color-border-subtle`(gray-6)加回来。`--color-border-subtle` 是**既有**的容器边界令牌(`#doc-panel` / `.event-list` 在用)⇒ 零新增令牌。

    配合 `border-collapse: collapse`(一字不动),相邻单元格的 `border-bottom` 与上一行的边界折叠成**一条** 1px 线,故不会出现双线。`.markdown-body td` 的计算 `border-left-width` / `border-right-width` / `border-top-width` 因此全部为 `0px` —— 这正是 ROADMAP SC1 对「不再有竖线与外框」的逐字操作定义。

    **第 2 步 —— 紧随其后追加一条新规则块。**

    在 `.markdown-body th, .markdown-body td` 规则块**之后**(即 `.markdown-body code` 规则块之前),追加一条:

    `.markdown-body th { background: var(--color-surface); }`

    只此一条声明。**不要**把 `background` 加进 `th, td` 并集规则(那会给数据格也上 gray-2 底);**不要**拆分并集选择器(重排风险区)。新增块的选择器 `.markdown-body th` 在 HEAD 上不存在,故它不参与任何既有等特异性对 —— 插入到它所有者的正后方不改变任何既有规则的相对源码顺序。

    **第 3 步 —— 在 `.markdown-body table` 规则块上方写一段承重注释。**

    注释写在**围栏外**,逐条记下五件事(缺一即会被后人读成任选或漏改):

    (a) **档位依据**:表头底色是 `--color-surface`(gray-2),正是 Phase 9 建立的三级 elevation 刻度里的「内陷面」档(`gray-3 页面 < gray-2 内陷面 < 白卡片`)—— 表格因此读作「白卡片内的一个内陷块」,而不是与卡片语言无关的网格(D-10-1)。**不得**改落 `--color-surface-sunken`(那是页面档)或围栏外的 tier-1 原语。

    (b) **就地改写的理由**:原 `border: 1px solid var(--color-border)` 是**就地改写**成 `border: none` + `border-bottom: …`,**不是**追加一条覆盖规则 —— 留下一条已死的 `border` 会让注释与代码互相矛盾(与 Phase 9 对 `#doc-panel` 的 `border-left` 同一纪律)。

    (c) **分隔线的档位**:行间分隔线与表头下边线同取 `--color-border-subtle`(gray-6),比原 `--color-border`(gray-7)浅一档;它是**装饰性**边界,**不标识任何东西**,故 SC 1.4.11 不适用、不新增 NON-TEXT 条目 —— 依据是本文件 role-band 段与清单头部注释里的两处**既有**登记(本注释须点名这两处,不要只写结论)。

    (d) **零新增 PAIR**:`.markdown-body th` 的文字色从 `.markdown-body` 继承(即 `--color-text`),它在新的 gray-2 绘制面上的配对 **已登记** —— 清单里的 `--color-text ON --color-surface` 那一条 ⇒ 零新增条目。

    (e) **不得碰的属性**:`padding` 与 `font-size` 两行逐字保留;`font-size` 被 `scripts/check-05-ui-uat.py` 的一条活断言锁死(`.markdown-body td font-size == var(--text-base)`)。

    **围栏外注释禁令(本任务加的任何注释都适用):** 不得含裸 `#hex`(`check-01` 扫围栏外全文)、不得含 `var(--radix-…` 或 `var(--white)`(tier-1 原语名私有于围栏)、不得含字面量 `!important;`(`check-04` 按出现次数计数,散文注释会把计数从 1 顶高 —— 本项目已因此红过三次)、不得含 `@layer` / `@property` / `var(--x, #fallback)` / `@media`。要指代颜色时写**令牌名**(`--color-surface` / `--color-border-subtle` / `--color-border`),不写数值、不写 hex。

    **第 4 步 —— 不触碰本任务范围之外的一切。** 不改 `--radius-*`(计划 02)、不改任何颜色令牌的值、不改 PAIR / ORDER 清单、不改 `.markdown-body` 的其它规则(`h1`…`code` / `blockquote` / `ul`)、不改 `frontend/app.js` / `frontend/index.html` / `frontend/vendor/`(零字节)、不改 `scripts/` 下任何既有文件。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>non-zero exit, or stdout not exactly "PASS"</fails_when>
    <automated>bash scripts/check-03-hidden-uniqueness.sh</automated>
    <fails_when>non-zero exit, or stdout not exactly "PASS"</fails_when>
    <automated>bash scripts/check-04-important-count.sh</automated>
    <fails_when>non-zero exit, or stdout not exactly "PASS"</fails_when>
    <automated>.venv/bin/python scripts/check-02-contrast.py</automated>
    <fails_when>non-zero exit, or any line beginning with "FAIL", or the final line not "PASS: 0 failures", or the output containing no line matching "^PASS .*  --color-text on --color-surface$"</fails_when>
    <automated>grep -o '/\* PAIR' frontend/style.css | wc -l; grep -o '/\* ORDER' frontend/style.css | wc -l</automated>
    <fails_when>the two counts are not exactly "53" and "1" respectively (either number changing means a manifest entry was added or removed)</fails_when>
    <automated>awk '/^\.markdown-body th, \.markdown-body td \{/{f=1} f{print} f&&/^\}/{exit}' frontend/style.css > /tmp/idi-10-thtd-rule.txt; grep -cF -- 'border: none;' /tmp/idi-10-thtd-rule.txt; grep -cF -- 'border-bottom: 1px solid var(--color-border-subtle);' /tmp/idi-10-thtd-rule.txt; grep -cF -- 'border: 1px solid var(--color-border);' /tmp/idi-10-thtd-rule.txt; grep -cF -- 'padding: var(--space-1) var(--space-2-5);' /tmp/idi-10-thtd-rule.txt; grep -cF -- 'font-size: var(--text-base);' /tmp/idi-10-thtd-rule.txt</automated>
    <fails_when>the five printed counts are not exactly "1", "1", "0", "1", "1" in that order (the awk region must isolate the `.markdown-body th, .markdown-body td` rule body; a wrong region shows up as the wrong counts, so also eyeball the extracted file if any count is off)</fails_when>
    <automated>git status --porcelain frontend/</automated>
    <fails_when>output contains any path other than "frontend/style.css", or output is empty</fails_when>
  </verify>
  <acceptance_criteria>
    - `.markdown-body th, .markdown-body td` 规则体的选择器文本与 HEAD 逐字一致;其声明集 = HEAD 的 3 条 − `border: 1px solid var(--color-border);` + `border: none;` + `border-bottom: 1px solid var(--color-border-subtle);`(共 4 条)。`padding` 与 `font-size` 两行逐字未动。
    - **规则体域内计数**(用 `awk` 取 `.markdown-body th, .markdown-body td {` 到其闭合 `}` 之间的行域,再在该域内 `grep`):`border: none;` 恰 **1** 行、`border-bottom: 1px solid var(--color-border-subtle);` 恰 **1** 行、`border: 1px solid var(--color-border);` **零**行(那条声明已被就地改写,不是被覆盖);`padding: var(--space-1) var(--space-2-5);` 与 `font-size: var(--text-base);` 各恰 **1** 行。
    - **全文计数另记,且不得用全文裸计数代替域内计数**(HEAD 现状会让全文计数误报,故两条判据必须分开写):`grep -cF -- 'border: none;' frontend/style.css` == **2**(本任务新增的 1 行 + `#selection-menu button` 规则体内**既有**的 1 行 —— HEAD 上它已是 1);`grep -cF -- 'border: 1px solid var(--color-border);' frontend/style.css` == **2**(`#main-pane > section` 与 `#doc-panel` 两处容器规则,均**不在** `.markdown-body` 内;HEAD 上是 3,第 3 处正是被就地改写的那条);`grep -cF -- 'border-bottom: 1px solid var(--color-border-subtle);' frontend/style.css` == **1**(HEAD 上是 0)。
    - `grep -nF -- '.markdown-body th { background: var(--color-surface); }' frontend/style.css` 命中恰好 1 行。
    - `.markdown-body table { border-collapse: collapse; }` 逐字未动;`.markdown-body` 段的其它规则(`h1` / `h2` / `h3` / `p` / `ul, ol` / `blockquote` / `code`)逐字未动。
    - `git diff -- frontend/style.css` 人工逐行核对:改动**全部**落在 `.markdown-body table` / `th, td` 附近;新增的 `.markdown-body th` 块位于 `th, td` 并集规则之后、`.markdown-body code` 规则之前;**没有任何既有规则块被移动**(diff 里不存在「先删后加同一规则块」的形态)。
    - `git diff -U0 -- frontend/style.css` 的输出里**不存在**任何以 `--radix-` 开头的增删行(零 primitive 改动),也不存在任何 `--radius-` 相关行(圆角属计划 02)。
    - `frontend/style.css` 围栏外的**新增**注释里不含裸 `#hex`、不含 `var(--radix-`、不含 `var(--white)`、不含字面量 `!important;`(`check-01` / `check-04` 各自打印 `PASS`)、不含 `@media` / `@layer` / `@property`。
    - 新增注释**引用**了 role-band 段与清单头部注释里「装饰性边界 + SC 1.4.11 不适用」这两处既有登记,并点名 `--color-text ON --color-surface` 这条既有 PAIR 条目。
    - `bash scripts/check-01-token-conformance.sh` / `check-03` / `check-04` 全打印 `PASS`;`.venv/bin/python scripts/check-02-contrast.py` 打印 `PASS: 0 failures`;`grep -o '/\* PAIR' | wc -l` == 53、`grep -o '/\* ORDER' | wc -l` == 1。
    - `git status --porcelain frontend/` 仅列出 `frontend/style.css`;`ls frontend/vendor/` 仍只有 `marked.min.js`。
  </acceptance_criteria>
  <done>文档区表格的四条边框只剩 `border-bottom` 一条(色取 `--color-border-subtle` gray-6),`.markdown-body th` 拿到 `--color-surface`(gray-2)浅底;两个原声明被就地改写、一条新规则块追加在其所有者正后方;四个静态门全绿;零新增颜色值 / 零新增配对 / 零令牌改动。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 2: 新建运行时门 `scripts/check-10-idi10-validation.py` —— `t1` / `t2` + `--screenshot`</name>
  <files>scripts/check-10-idi10-validation.py</files>
  <precondition>.venv/bin/python 可导入 playwright(`.venv/bin/python -c "import playwright"` 退出码 0),且 Playwright 自带 chromium 已缓存(不需要联网下载)</precondition>
  <reversibility rating="costly">新建脚本本身可删除回退;但它被计划 02 扩展、被计划 03 的截图任务直接消费,回退需连带撤掉这两处的引用,故评级 costly 而非 reversible。</reversibility>
  <read_first>
    - `scripts/check-09-idi09-validation.py` **全文** —— 本任务要照抄的 exact 先例:文件头 docstring 的「为什么另开一个文件」论证形态、`load_check05()`、`png_size()`、令牌级「两侧都写死」的断言形态、元素读不到时走 `blocked()` 绝不记 PASS 的纪律、`ITEMS` 派发表、`parse_args()`、`main()` 的服务生命周期 + Playwright 启动 + `=== 逐项结论 ===` 汇总 + 退出码语义、`run_screenshots()`
    - `scripts/check-05-ui-uat.py` 的 `ensure_server()` / `make_fixture()` / `enter_project()` / `read_style()` / `resolve_color()` / `resolve_token()` / `effective_bg()` / `ok()` / `ok_true()` / `blocked()` / `info()` / `norm()` / `ROWS` / `item_verdict()` —— **本文件复用的全部设施,一行都不改**
    - `scripts/check-05-ui-uat.py` 的 `STATES = ["p1", "p12", "p3", "checking", "archive"]` 与 `MARKDOWN_TARGETS` / `MARKDOWN_HOSTS`(4 个 doc 宿主:`#draft-content` / `#brainstorm-content` / `#round-doc` / `#latest-check`;另有 5 个 embedded 目标)
    - `scripts/check-05-ui-uat.py` 的 item4 注入段(`page.evaluate` 里用 `renderMarkdown(md)` 把含表格的探针 markdown 写进 `list(MARKDOWN_HOSTS)` 的每一个宿主,随后才读 `td` 的 `font-size`)—— **本任务要照抄的注入手法**:用应用自身的渲染函数造出探针节点再读数,零网络、零 AI 调用、真实代码路径
    - `scripts/check-05-ui-uat.py` 的 `[p1] .markdown-body td font-size == var(--text-base)` 断言 —— 它锁死的是 `td` 的 `font-size`(本任务一字不动);注意它的 `#draft-content td` 之所以存在,是因为**同一函数前一段刚注入过含表格的 markdown**,不是 `p1` fixture 的自然渲染。**不得**把那次 PASS 当成「`p1` 的 `#draft-content` 本来就有 `<td>`」的证据
    - `scripts/check-05-ui-uat.py` 的 `#draft-content` / `#brainstorm-content` / `#round-doc` / `#latest-check` 四个 doc 宿主在 `p1` 下**全部存在于 DOM**(item4 的注入循环对四个宿主逐一取 `document.querySelector` 而不判空,phase 9 实测通过)—— 这是本任务把四个宿主都纳入 `TABLE_PROBES` 的依据
    - `scripts/ui-states/` 的样本内容(规划期实测)—— `p1` 目录下**只有 `.gitkeep`**;`p12/docs/draft.md`、`checking/DESIGN.md`、`checking/docs/DESIGN-check-2.md`、`archive/DESIGN.md`、`archive/docs/DESIGN-check-1.md` 的以 `|` 开头的表格行数**均为 0**;含表的只有 `p3/docs/discuss-round-{1,2}.md`(17 / 15 行)与 `archive/docs/discuss-round-{1,2}.md`(17 / 15 行)。而 `archive` 首屏由 `loadArchiveView()` 渲染的是 `DESIGN.md`(0 行表格),轮次文档只在用户切轮次选择器时才加载 ⇒ **自然首屏只有 `p3` 一个样本有表**。**本任务因此不得靠「哪个宿主本来就有表」选点**
    - `.planning/phases/idi-10-tables-and-radius-scale/idi-10-PATTERNS.md` §`scripts/check-10-idi10-validation.py` —— 模块级设施的复用形态、令牌级「两侧都写死」的形态、BLOCKED 纪律、CLI / 退出码 / 汇总形状、浏览器路线的实测结论(不提供 `--browser`,固定 bundled)
    - `scripts/probe-card-border-token.py` —— 「一次性探针 vs 门」的分野先例(避免把探针的写法误当门的写法)
  </read_first>
  <action>
    **第 1 步 —— 建文件与文件头。**

    路径 `scripts/check-10-idi10-validation.py`(命名空闲:`scripts/` 现有 check-01…check-07 + check-09,**无 check-08**)。`#!/usr/bin/env python3` + `# -*- coding: utf-8 -*-` + 中文 docstring,结构照抄 `check-09`。docstring 必须含四块:

    - **为什么另开一个文件**:给出**实测论证** —— 规划期已 grep 全部 7 个门脚本 + 2 个探针,**没有任何一条**断言表格的边框 / 底色 / 布局;唯一接触点是 `check-05-ui-uat.py` 的 `td font-size` 断言,它断言的**不是**本阶段要改的属性(且期望侧运行时解析)。⇒ TABLE-01 / TABLE-02 的渲染判据在本文件之前**零自动化覆盖**。全部断言是真实浏览器里的 `getComputedStyle` 读数,不是源码文本匹配 —— 表格是**画出来**的。
    - **与 check-05 的关系**:复用 check-05 的模块级设施,不重复实现,**也不改动 check-05 一行**(改它会把它所属的报告拖进连带指纹重验名单)。
    - **运行方式**:给出 `--item t1` / `--item t1,t2` / `--screenshot DIR` / `--json` / `--keep` 的示例命令行。
    - **退出码语义**(与 check-05 一致):`0 = 全 pass;1 = 至少一条 FAIL;2 = 无 FAIL 但至少一条 BLOCKED`。

    **第 2 步 —— 模块级设施。**

    `from __future__ import annotations`;`import argparse, importlib.util, json, re, shutil, struct, sys, tempfile`;`from pathlib import Path`。常量 `ROOT` / `CHECK05` / `STYLE_CSS`(= `ROOT / "frontend" / "style.css"`)。`load_check05()` 用 `importlib.util.spec_from_file_location`(文件名含连字符,不能用 `import`),然后从模块取出 `ok` / `ok_true` / `blocked` / `info` / `read_style` / `resolve_color` / `resolve_token` / `norm` 绑成模块级名字。`png_size(path)` 读 PNG 的 IHDR 取 `(width, height)`,非 PNG 或读不到返回 `(None, None)`。`fence_text()` 返回两行 `===== DESIGN TOKENS: START/END` 之间的文本(供计划 02 的围栏内零声明断言)。

    令牌级「两侧写死」常量:`TH_BG_LITERAL = "rgb(249, 249, 249)"`(gray-2)。注释里写明为什么写死:两侧都从同一个令牌解析时,令牌被改坏也照样 PASS。

    `TABLE_PROBES`:一个 `(样本, 宿主)` 元组,取值为

    `TABLE_PROBES = (("p1", "#draft-content"), ("p1", "#brainstorm-content"), ("p1", "#round-doc"), ("p1", "#latest-check"), ("p3", "#round-doc"))`

    —— 覆盖 `c05.MARKDOWN_HOSTS` 的**全部四个** doc 宿主(在 `p1` 下四个都在 DOM),外加一对**自然渲染**的样本(`p3` / `#round-doc` 渲染 `scripts/ui-states/p3/docs/discuss-round-2.md`,该文件含 SC1 点名的三个机器可解析表)。

    **为什么必须「先注入、再读数」而不是依赖 fixture 自然渲染(这条是承重的,不是风格偏好)。** 规划期逐样本实测:`scripts/ui-states/p1/` 只有 `.gitkeep`,`p12` / `checking` / `archive` 的文档表格行数**全部为 0**(`archive` 的两个轮次文档虽含表,但首屏 `loadArchiveView()` 只把 `DESIGN.md` 渲染进 `#round-doc`)⇒ 5 个样本 × 4 个宿主的笛卡尔积里**只有 `(p3, #round-doc)` 一对**自然有表。靠「哪个宿主本来就有表」选点,门就退化成**单点门** —— 本项目已登记过「只探一个宿主」的漏检教训。本仓库对这件事的既有解法是**造出容器再断言**:`scripts/check-05-ui-uat.py:1486` 逐字登记「这五项断言是**造出容器再断言**,不靠『fixture 里本来就有 .chat-bubble』」,其 item4 在 `:1086-1096` 正是用**应用自身的 `renderMarkdown`** 把一段含表格的 markdown 注入全部 doc 宿主后再读数。本任务照抄这一手 —— 注入走的是真实渲染路径(零网络、零 AI 调用),且注入后每个对都真的渲染出表格。

    **第 3 步 —— 两个断言集。**

    **共用的「造出容器再断言」前置(每个 `(样本, 宿主)` 对都必须走,不许省)。** 定义一个模块级常量 `TABLE_PROBE_MD`,内容是一段**含表头与数据格**的最小 markdown(表头行 + 分隔行 + 至少一行数据,例如三列两行)。对每个 `(样本, 宿主)` 对,顺序固定为:

    1. `c05.make_fixture(样本, tmp_root)` + `c05.enter_project(page, 宿主所在项目)`;
    2. **注入**:`page.evaluate` 里取 `document.querySelector(宿主)`,清空它,再 `host.appendChild(renderMarkdown(TABLE_PROBE_MD))` —— 与 `check-05-ui-uat.py:1086-1096` 同款手法,用的是**应用自身的** `renderMarkdown`(真实渲染路径,零网络、零 AI 调用);
    3. **断言注入成功**:注入后该宿主的 `td` 计数必须 > 0(用 `page.evaluate` 数 `querySelectorAll`)。**注入静默失败时立刻记 FAIL**,否则后面的读数会退化成对空宿主的空转断言(读不到元素只会落 BLOCKED,而 BLOCKED 不是 PASS);
    4. 打印 `info()` 诊断行,记下该样本 / 宿主名与注入后的 `th` / `td` 计数;
    5. 逐条断言(见下)。

    为省时间,**按样本分组**:同一 `样本` 的多个宿主只 `enter_project` 一次,对该样本的每个宿主各注入一次再读数。不得为了省事只注入一个宿主后把读数复制到其它宿主。

    `t1(page, tmp_root)` — **表头**。按上面 1–5 的固定顺序遍历 `TABLE_PROBES`,对 `th` 逐条断言:
    - `th` 的计算 `background-color` == `resolve_color("--color-surface")`(标签里带样本名与宿主名);
    - **令牌级两侧写死**:`resolve_color("--color-surface")` == `TH_BG_LITERAL`;
    - `th` 的计算 `border-bottom-width` == `1px` 且 `border-bottom-style` == `solid`;
    - `th` 的计算 `border-bottom-color` == `resolve_color("--color-border-subtle")`;
    - `th` 的计算 `border-left-width` / `border-right-width` / `border-top-width` 均为 `0px`;
    - **对照组**(证明没顺手改别的):`th` 的计算 `font-size` == `resolve_token("--text-base")`、计算 `padding` == HEAD 值(`var(--space-1) var(--space-2-5)` 解析后为 `4px 10px`)。

    `t2(page, tmp_root)` — **数据格**。同样按第 3 步 1–5 的固定顺序(含**逐宿主注入**与注入成功断言)遍历 `TABLE_PROBES`,对 `td` 断言:
    - 计算 `border-left-width` / `border-right-width` / `border-top-width` 均为 `0px`(HEAD 上是 `1px` —— 这是 SC1 对「不再有竖线与外框」的逐字操作定义,标签注释里引用它);
    - 计算 `border-bottom-width` == `1px`、`border-bottom-style` == `solid`、`border-bottom-color` == `resolve_color("--color-border-subtle")`;
    - **对照组**:计算 `font-size` == `resolve_token("--text-base")`(**这是 `check-05-ui-uat.py:1126` 锁死的属性,本阶段一字不动**)、计算 `padding` == HEAD 值。

    每条断言一律走 `ok` / `ok_true`:`read_style` 返回 `None` 或 `resolve_*` 解析不出时自动落进 BLOCKED 分支,**绝不记 PASS**。BLOCKED 的标签要写清是「元素读不到」还是「令牌解析不出」。

    **第 4 步 —— 核实「每一个对都真的渲染出表格」(本步骤是决定性的,不要跳过)。**

    首次运行 `t1` / `t2` 后读 INFO 行,核对每个 `(样本, 宿主)` 对的**注入后** `th` / `td` 计数:每一个对的 `td` 计数都必须 > 0。

    ⚠ **计数为 0 的处置是「报回」,不是「换点」。** 因为每个对都已按第 3 步注入过,计数为 0 只可能是三种成因之一:注入本身失败(`renderMarkdown` 抛错 / 宿主在 `page.evaluate` 里取不到)、宿主选择器拼错、或 `p1` 下该宿主并不在 DOM。**这三种都是产品缺陷或探针缺陷,必须停下报回**并给出该对的原始读数 —— **不得**悄悄把它从 `TABLE_PROBES` 里删掉(删点会让门退化成单点门,正是本条要防的事),**不得**用「至少一个宿主有表」的弱形式收口。

    `TABLE_PROBES` 的**至少 2 个对**这条判据因此是**结构性成立**的(5 个对里每个都注入了探针表),不再依赖 fixture 里恰好有哪个宿主带表。

    **第 5 步 —— `--screenshot DIR`。**

    照抄 `check-09` 的 `run_screenshots()`:遍历 `c05.STATES`(`["p1", "p12", "p3", "checking", "archive"]`),每个样本 `make_fixture` → `enter_project` → `page.screenshot(path=out_dir / f"{state}.png")`,并用 `png_size()` **逐张**断言 1440×900;最后两条汇总断言:样本清单逐项一一对应(无缺项、无多余样本)、输出目录恰含 5 个 PNG。出图断言是**逐张**的,不是「有文件就算」。

    **第 6 步 —— `--json` 报告模式。**

    `--json` 时把 `c05.ROWS` 全量序列化为 JSON 打到 stdout(替代/附加人类可读输出),使后续计划能机器消费门的结论而不必解析散文。默认行为不变(人类可读 + `=== 逐项结论 ===` 汇总 + 退出码)。

    **第 7 步 —— CLI / 派发 / 汇总 / 退出码。** 照抄 `check-09` 的形状:
    - `ITEMS = {"t1": t1, "t2": t2}`(计划 02 会追加 `r1` / `r2`);
    - `parse_args()`:`--item`(`action="append"`,可重复或逗号分隔)、`--screenshot DIR`、`--json`、`--keep`;
    - `main()`:`items` 解析与未知项报错 → `c05.ensure_server()` → `tempfile.mkdtemp(prefix="idi-10-gate-")` → `sync_playwright().start()` → `pw.chromium.launch(headless=True)` → `browser.new_context(viewport={"width": 1440, "height": 900})` → 逐项派发 → 可选 `run_screenshots` → `finally` 里关浏览器 / 关服务 / 清理临时目录(`--keep` 时不清理);
    - 汇总块逐项打印 `item {i}: {VERDICT}  ({n} 条断言,{f} FAIL,{b} BLOCKED)`,末尾 `print(f"\nexit={code}  (0=全 pass,1=有 fail,2=有 blocked)")`,返回码 `1 if any_fail else (2 if any_blocked else 0)`。

    **不提供 `--browser` 参数** —— 固定走 Playwright 自带 chromium + 无头。该机 `channel="chrome"` + headless 会让 CDP 挂死(见 `check-05` / `check-09` 文件头的实测记录)。

    **第 8 步 —— 不触碰范围之外的一切。** 不改 `scripts/check-05-ui-uat.py` 一行;不改 `frontend/style.css`(本任务零 CSS 改动);不改 `scripts/check-01…04` / `check-06` / `check-07` / `check-09` / `probe-*`;不改 `frontend/app.js` / `index.html` / `vendor/`。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-10-idi10-validation.py --item t1</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or the trailing line not exactly "exit=0  (0=全 pass,1=有 fail,2=有 blocked)", or the "=== 逐项结论 ===" block showing a non-zero BLOCKED count for item t1</fails_when>
    <automated>.venv/bin/python scripts/check-10-idi10-validation.py --item t2</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or the trailing line not exactly "exit=0  (0=全 pass,1=有 fail,2=有 blocked)", or the "=== 逐项结论 ===" block showing a non-zero BLOCKED count for item t2</fails_when>
    <automated>.venv/bin/python scripts/check-10-idi10-validation.py --item t1 --item t2 --json</automated>
    <fails_when>non-zero exit, or stdout being empty, or stdout containing no JSON array of assertion records, or the emitted records containing no entry whose label names a table header/cell probe</fails_when>
    <automated>.venv/bin/python scripts/check-10-idi10-validation.py --screenshot /tmp/idi-10-shot-selfcheck</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or the trailing line not starting with "exit=0", or the run not creating exactly 5 PNGs in the target directory</fails_when>
  </verify>
  <acceptance_criteria>
    - `scripts/check-10-idi10-validation.py` 存在,可用 `.venv/bin/python` 直接运行,`--item` / `--screenshot` / `--json` / `--keep` 四个参数都被 `parse_args` 接受,且**不提供** `--browser` 参数。
    - 文件头 docstring 含「为什么另开一个文件」的实测论证(指出唯一接触点是 `check-05` 的 `td font-size` 断言、它断言的不是本阶段要改的属性、故 TABLE-01/02 零自动化覆盖)、运行方式、退出码语义三块。
    - `.venv/bin/python scripts/check-10-idi10-validation.py --item t1` 的 `=== 逐项结论 ===` 块里 `t1` 的 FAIL 与 BLOCKED 计数均为 0,末行为 `exit=0`。
    - `.venv/bin/python scripts/check-10-idi10-validation.py --item t2` 的 `=== 逐项结论 ===` 块里 `t2` 的 FAIL 与 BLOCKED 计数均为 0,末行为 `exit=0`。
    - `t1` 的输出里含一条 INFO 行,逐条列出 `TABLE_PROBES` 中每个 `(样本, 宿主)` 对**注入后**的 `th` / `td` 计数;且**每一个**对的 `td` 计数都 > 0。每一个对在读数前都按第 3 步用应用自身的 `renderMarkdown` 注入过 `TABLE_PROBE_MD`,且注入成功本身有一条断言(注入后 `td` 计数 > 0)—— 判据不是「fixture 里本来就有表」。
    - `TABLE_PROBES` 含 **5** 个 `(样本, 宿主)` 对(≥ 2 的下界由它满足),覆盖 `c05.MARKDOWN_HOSTS` 的**全部四个** doc 宿主(`p1` 下四个都在 DOM),另含一对自然渲染样本 `(p3, #round-doc)`;宿主名与样本名都不是凭空写的。**不得**为「凑绿」删减对 —— 计数为 0 的对按第 4 步报回,不换点、不删点。
    - `t2` 的输出里含 `[p1] .markdown-body td font-size` 的 PASS(或该断言在其探针对上的等价 PASS 行),证明被锁死的属性未被顺手改动 —— **不是 BLOCKED**。
    - `t1` / `t2` 的断言里,`--color-surface` 与 `--color-border-subtle` 的期望侧取自 `resolve_color` **且**另有一条把解析值与写死字面量(`TH_BG_LITERAL`)比对的令牌级断言(两侧都写死,防「令牌被改坏而消费者仍接线」时假绿)。
    - `.venv/bin/python scripts/check-10-idi10-validation.py --screenshot <DIR>` 出图后 `<DIR>` 下**恰有 5 个 PNG**,与 `c05.STATES` 逐项一一对应,每张为 1440×900(逐张断言)。
    - `--json` 模式的 stdout 可被 `json.loads` 解析,且记录条数与人类可读模式的断言条数一致。
    - `git diff -- scripts/check-05-ui-uat.py` 为空;`git status --porcelain scripts/` 仅新增 `scripts/check-10-idi10-validation.py`(无其它改动)。
  </acceptance_criteria>
  <done>运行时门 `scripts/check-10-idi10-validation.py` 就位:`t1`(表头 gray-2 底 + 1px 下边线)/ `t2`(数据格三条边 0px + 行间浅线 + `font-size` 对照组)在真实浏览器里全 PASS、0 BLOCKED;`--screenshot DIR` 出 5 张 1440×900;`--json` 可机器消费;`check-05-ui-uat.py` 零改动。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 3: 表头新绘制面的对比度登记核实 + 四个静态门与「零新增 / 零放宽」逐字节证据(D-10-3)</name>
  <files>frontend/style.css</files>
  <reversibility rating="reversible">本任务只做取证与记录,不产生产品代码改动;失败只暴露问题、不引入问题。</reversibility>
  <read_first>
    - `scripts/check-02-contrast.py` **全文** —— `DECL_RE` / `PAIR_RE` / `ORDER_RE` 的正则形态、`resolve()` 的「未知令牌即 FAIL」、覆盖地板、`raw_pairs == len(pairs)` / `raw_orders == len(orders)` 的标记计数一致性检查、阈值常量 `TEXT_MIN = 4.5` / `NON_TEXT_MIN = 3.0`、输出格式 `PASS  %.2f  %s` 与收尾行 `PASS: 0 failures`。**本任务一行都不改它**
    - `frontend/style.css` 的 PAIR 清单段 —— 逐条读清单头部注释(阈值 / 覆盖地板 / 标记计数一致性 / 六个 value layer 的规模台账)、`/* PAIR --color-text ON --color-surface TEXT */` 这一条、非文本边界组的标题与注释、以及 `--color-border-hover` 那条注释里「No input in this app declares a background, so Chrome paints the field fill white…」的既登记事实
    - `frontend/style.css` 的 role-band 段(围栏内)—— `border band 6-8 → step 9 for --color-border-strong … nothing in 6-8 clears SC 1.4.11's 3:1 on any surface … The other three borders stay in band 6-8: they are decorative, and SC 1.4.11 does not apply to a border that identifies nothing`
    - `scripts/check-01-token-conformance.sh` / `scripts/check-03-hidden-uniqueness.sh` / `scripts/check-04-important-count.sh` 全文 —— 各自的计数逻辑(围栏外裸 `#hex` 与 tier-1 原语引用、`^[[:space:]]*\.hidden[[:space:]]*\{` 计数、`!important;` **声明**计数)
    - `.planning/ROADMAP.md` §`### Phase 10:` 的 Success Criterion 2 与 Pitfalls 第 6 条(「给表格加 `!important` 或令牌化 `display`」)
    - `.planning/phases/idi-10-tables-and-radius-scale/10-CONTEXT.md` §D-10-3 与 §「表格:对比度」
  </read_first>
  <action>
    **第 1 步 —— 实跑 `check-02` 并把表头配对那一行**原文**抄出来。**

    跑 `.venv/bin/python scripts/check-02-contrast.py`,在输出里找到 `--color-text on --color-surface` 那一行(形如 `PASS  <比值>  --color-text on --color-surface`),把该行**原文逐字**抄进 SUMMARY。

    ⚠ **不得沿用任何未在本机复现的数字。** 规划期的 Pattern Map 里写过一个比值,但那次读数**未能复现**(工具环境问题)。本阶段的 SUMMARY 只能贴**本次实跑**的输出行。若该行不存在或为 `FAIL`,那是产品缺陷:停下、把原始输出贴进 SUMMARY 报回,**不得**改清单去迁就实跑,也**不得**新增一条 PAIR 条目来「补上」。

    **第 2 步 —— 把「装饰性边界 ⇒ 零 NON-TEXT 条目」这条判断的**依据**逐条登记进 SUMMARY(不是只写结论)。**

    引用两处**既有**原文(本阶段不新发明判据):
    - role-band 段:`border band 6-8 … The other three borders stay in band 6-8: they are decorative, and SC 1.4.11 does not apply to a border that identifies nothing`;
    - 清单头部注释:`Decorative separators are deliberately absent — SC 1.4.11 does not apply to a border that identifies nothing`。

    判据:表头下边线与行间分隔线**不标识任何东西**(它们是视觉分组的装饰,不是控件的边界),故不需要 NON-TEXT 配对条目。SUMMARY 里要写明「依据是这两处既有登记」,而不是「我判断不需要」。

    **第 3 步 —— 「零新增颜色值 / 零新增 primitive / 零阈值改动」的逐字节证据(D-10-3)。**

    D-10-3 裁定:本阶段两项改动都**不引入新颜色值、不放宽阈值** —— 表头底色取**既有令牌** `--color-surface`,圆角收敛**只改归属**、不改任何颜色;`check-02` 的 `TEXT_MIN` / `NON_TEXT_MIN` 必须与 HEAD **逐字节相同**。逐条取证并抄进 SUMMARY:
    - `git diff -- scripts/check-02-contrast.py` **为空**(该文件零改动)⇒ `TEXT_MIN` / `NON_TEXT_MIN` 与 HEAD 逐字节相同。**放宽阈值是「把门改小以让结论成立」,本仓库明令禁止。**
    - `git diff -U0 -- frontend/style.css` 的输出里**不存在**任何以 `--radix-` 开头的增删行 ⇒ 零 primitive 改动。
    - `grep -o '/\* PAIR' frontend/style.css | wc -l` == **53**、`grep -o '/\* ORDER' frontend/style.css | wc -l` == **1**(与改动前逐字相同)⇒ 零新增、零删除的清单条目。
    - 围栏内新增的注释里**不含**「令牌名 + 冒号」形态(`check-02` 的 `DECL_RE` 扫围栏全文含注释,写 `--radix-gray-12: …` 会被当成一条值不可解析的声明而 FAIL)。本任务的改动都在围栏外,但仍须核对新增注释。
    - `frontend/style.css` 里 `@media` 出现次数仍**恰为 1**(Phase 7 的 prefers-reduced-motion 块)—— `scripts/check-05-ui-uat.py` 有一条读文件文本的静态断言锁死这个数;本阶段不得新增媒体查询。

    **第 4 步 —— 四个静态门逐条记录原始输出。** `bash scripts/check-01-token-conformance.sh` / `.venv/bin/python scripts/check-02-contrast.py` / `bash scripts/check-03-hidden-uniqueness.sh` / `bash scripts/check-04-important-count.sh`。把每条的**标准输出原文**与**退出码**抄进 SUMMARY(不要只写「绿」)。

    **第 5 步 —— 不触碰任何代码。** 本任务只跑命令与记录(SUMMARY 除外)。任何一条不达标都按产品缺陷报回,不就地修。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-02-contrast.py</automated>
    <fails_when>non-zero exit, or any line beginning with "FAIL", or the final line not "PASS: 0 failures", or the output containing no line matching "^PASS .*  --color-text on --color-surface$"</fails_when>
    <automated>git diff -- scripts/check-02-contrast.py</automated>
    <fails_when>output is not empty (any diff means the threshold file or a manifest rule was touched)</fails_when>
    <automated>git --no-pager diff -U0 -- frontend/style.css > /tmp/idi-10-style-diff.txt && grep -n '^[+-].*--radix-' /tmp/idi-10-style-diff.txt; echo "rc=$?"</automated>
    <fails_when>any matching line is printed, or rc is not "1" (rc 1 == grep found no "--radix-" added/removed line; rc 0 means one was found; any other rc means the git stage itself failed and the diff file must not be trusted)</fails_when>
    <automated>grep -o '/\* PAIR' frontend/style.css | wc -l; grep -o '/\* ORDER' frontend/style.css | wc -l</automated>
    <fails_when>the two counts are not exactly "53" and "1" respectively</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>non-zero exit for any of the three, or any of the three not printing exactly "PASS"</fails_when>
    <automated>grep -c '@media' frontend/style.css</automated>
    <fails_when>the count is not exactly "1"</fails_when>
  </verify>
  <acceptance_criteria>
    - SUMMARY 里贴出 `check-02` 的**实跑**输出行,形如 `PASS  <比值>  --color-text on --color-surface`(逐字原文);并注明该行来自本次实跑而非任何未复现的历史读数。
    - SUMMARY 里引用 role-band 段与清单头部注释两处既有原文,作为「分隔线是装饰性边界 ⇒ 零新增 NON-TEXT 条目」的依据。
    - `git diff -- scripts/check-02-contrast.py` 为空;SUMMARY 里明确记下 `TEXT_MIN` / `NON_TEXT_MIN` 与 HEAD 逐字节相同。
    - `git diff -U0 -- frontend/style.css` 的输出里以 `--radix-` 开头的增删行计数为 **0**。
    - `grep -o '/\* PAIR' | wc -l` == **53**;`grep -o '/\* ORDER' | wc -l` == **1**(零新增 / 零删除)。
    - `frontend/style.css` 的 `@media` 计数 == **1**。
    - 四个静态门的退出码与标准输出原文都抄进了 SUMMARY;`check-01` / `check-03` / `check-04` 各打印 `PASS`,`check-02` 打印 `PASS: 0 failures`。
    - D-10-3 的四条判据逐条取证:表头底色取自**既有令牌** `--color-surface`(零新增颜色值)、零新增 tier-1 primitive、`check-02` 的 `TEXT_MIN` / `NON_TEXT_MIN` 与 HEAD 逐字节相同、零 PAIR / ORDER 条目增删。
    - 本任务没有编辑任何文件(除 SUMMARY)。
  </acceptance_criteria>
  <done>表头新绘制面的配对以 `check-02` 实跑输出行的原文登记;装饰性边界的判断以两处既有登记为据并逐字引用;零新增颜色值 / 零新增 primitive / 零阈值改动 / 零清单增删 / 零媒体查询五项逐字节取证;四个静态门全绿且原文入册。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 无外部输入边界 | 本阶段只改 `frontend/style.css` 的**声明层**(呈现层)并新增一个**只读**的本地运行时门:零用户输入处理、零鉴权、零数据访问、零网络调用、零新增资源加载。攻击面限于**浏览器对 CSS 的解析与渲染**,以及新门脚本自起 `uvicorn` 并驱动无头浏览器这一次本地动作 |
| 本地进程边界(新门脚本) | `scripts/check-10-idi10-validation.py` 会 `c05.ensure_server()` 自起(或复用)`uvicorn`,并用 Playwright 驱动无头 chromium 访问 `localhost`。它与被测样本之间必须是**只读**关系 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-10-01 | Information Disclosure | 表格选择器 `.markdown-body th` / `.markdown-body td` 与新增的 `background` 声明 | low | accept | 选择器只用既有类名与元素名,不含属性选择器、不读用户数据、不引入 `url()` / `@import` / 远程字体 —— CSS 侧不存在数据外泄面。新增声明只有 `background: var(--color-surface);` 与 `border-bottom`,不含任何 URL。验收:`git diff -U0 -- frontend/style.css` 的新增行不含 `url(` / `@import` |
| T-idi-10-02 | Tampering | 新门脚本的 fixture 生命周期(`c05.make_fixture` / `emit_enter_project`) | **high** | mitigate | 门驱动真实浏览器进入**临时目录里的样本副本**。若它写回被测样本、或把产物落进 `frontend/`,就会污染被检对象并使后续门读到假状态。缓解:(a) fixture 一律走 `c05.make_fixture(name, tmp_root)`,它在 `tempfile.mkdtemp()` 下 `copytree` 出新副本,原始 `scripts/ui-states/` 零改动;(b) 临时根目录在 `finally` 里 `shutil.rmtree`(仅 `--keep` 保留供排查);(c) `--screenshot` 的输出目录由调用方显式给定,本计划的自检用 `/tmp/` 路径;(d) 验收:`git status --porcelain frontend/` 仅含 `frontend/style.css`,`git status --porcelain scripts/ui-states/` 为空 |
| T-idi-10-03 | Tampering | 自起的 `uvicorn` 进程与复用既有 8765 监听的判定 | medium | mitigate | 该机 8765 端口可能已有先前遗留的 uvicorn 进程,门走「复用,不新起」分支是既有事实。缓解:复用 `c05.ensure_server()` 的既有逻辑(本计划一行都不重写它),`main()` 的 `finally` 只 `terminate()` **本次自起**的进程(与 `check-09` 同形),不对复用来的进程动手;`--keep` 只保留临时目录,不影响进程 |
| T-idi-10-04 | Elevation of Privilege | 无 | low | accept | 本阶段不触碰鉴权、权限门、服务端路径或任何 API;纯呈现层改动 + 一个只读本地门,无提权面 |
| T-idi-10-05 | Repudiation | 「表格已改造」这一结论缺少可复核的原始证据 | medium | mitigate | 全部判据走**真实浏览器** `getComputedStyle` 读数并逐条打印 INFO 原始读数;SUMMARY 必须抄录门的退出码、`=== 逐项结论 ===` 块与任何 FAIL / BLOCKED 行的**完整原文**,而不是只写「绿」。`check-02` 的表头配对数值必须是**本次实跑**的输出行原文(规划期的历史读数未被复现,不得沿用) |
| T-idi-10-SC | Tampering | npm / pip / cargo 安装 | low | accept | 本阶段**零安装**:零新增依赖、零构建步骤、零新增第三方包(DESIGN.md D-06 硬约束);Playwright 与 chromium 均已在项目 `.venv` 中就绪,不触发下载。`frontend/vendor/` 仍只有 `marked.min.js`,无供应链面进入。验收:`ls frontend/vendor/` 输出仅 `marked.min.js` |
</threat_model>

<verification>
**静态门(全部必须绿):**

- `bash scripts/check-01-token-conformance.sh` → `PASS`(围栏外零裸 `#hex`、零 tier-1 原语引用)
- `.venv/bin/python scripts/check-02-contrast.py` → `PASS: 0 failures`,且输出含 `PASS  <比值>  --color-text on --color-surface`(原文入册)
- `bash scripts/check-03-hidden-uniqueness.sh` → `PASS`
- `bash scripts/check-04-important-count.sh` → `PASS`

**运行时门(本计划新建):**

- `.venv/bin/python scripts/check-10-idi10-validation.py --item t1` → `exit=0`,0 FAIL / 0 BLOCKED(表头 gray-2 底 + 1px 下边线 + 三条边 0px)
- `.venv/bin/python scripts/check-10-idi10-validation.py --item t2` → `exit=0`,0 FAIL / 0 BLOCKED(数据格三条边 0px + 行间浅线 + `font-size` 对照组)
- `.venv/bin/python scripts/check-10-idi10-validation.py --screenshot <TMP>` → `<TMP>` 下恰 5 个 1440×900 PNG

**仓库卫生:**

- `git status --porcelain frontend/` 仅列出 `frontend/style.css`
- `ls frontend/vendor/` 仅 `marked.min.js`
- `git diff -- scripts/check-02-contrast.py` 为空;`git diff -- scripts/check-05-ui-uat.py` 为空
- `grep -o '/\* PAIR' frontend/style.css | wc -l` == 53;`grep -o '/\* ORDER' frontend/style.css | wc -l` == 1
</verification>

<success_criteria>
- 文档区表格在真实浏览器里不再有竖线与外框(`td` 的 `border-left-width` / `border-right-width` / `border-top-width` == `0px`),`.markdown-body th` 的计算底色 == `--color-surface`(gray-2 = `rgb(249, 249, 249)`),表头下边线与行间分隔线为 `1px solid var(--color-border-subtle)`(gray-6)。
- 原 `border: 1px solid var(--color-border);` 被**就地改写**,文件里不存在被后续规则覆盖的已死声明;新增的 `.markdown-body th` 规则块追加在其所有者正后方,既有规则块的相对源码顺序逐字未变。
- 零新增颜色值、零新增 tier-1 primitive、零新增 PAIR / ORDER 条目、零阈值改动;`check-02` 的表头配对以实跑输出行原文登记。
- 表格的渲染判据首次有了自动化运行时覆盖:`scripts/check-10-idi10-validation.py` 的 `t1` / `t2` 在真实浏览器里全 PASS、0 BLOCKED;`--screenshot` 出 5 张 1440×900。
- `scripts/check-05-ui-uat.py` / `scripts/check-01…04` / `check-06` / `check-07` / `check-09` / `probe-*` 代码零改动;`frontend/app.js` / `index.html` / `vendor/` 零字节改动。
- `td` 的 `font-size` 与 `padding` 一字未动(被既有活断言锁死的属性)。
</success_criteria>

<output>
Create `.planning/phases/idi-10-tables-and-radius-scale/idi-10-01-SUMMARY.md` when done
</output>

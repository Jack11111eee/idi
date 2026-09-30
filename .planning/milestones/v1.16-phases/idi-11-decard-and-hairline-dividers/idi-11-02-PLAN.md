---
phase: idi-11-decard-and-hairline-dividers
plan: 02
type: execute
wave: 2
depends_on:
  - idi-11-01
files_modified:
  - frontend/style.css
autonomous: true
requirements:
  - REG-02

estimate:
  tokens: 65000
  raw_tokens: 65000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- 令牌删除(围栏自己的规则) ----
    - "两个被本次反转孤立掉的令牌声明**已从围栏内删除**:卡片底色令牌(3 处消费者)与卡片阴影令牌(2 处消费者)在计划 01 之后消费者归零,按围栏抬头与 Hard Rule 5 / D-04 的「只声明被消费的令牌」处置 —— 与 Phase 10 援引同一条规则删掉那个 28px 圆角档位同型。**这不是 G2**:G2 是「补一条**通用的**围栏消费断言」,已由用户明确排除在 v1.16 范围外"
    - "**围栏内**这两个令牌名的出现次数**各为 0**,且这是**源码文本级**判据 —— 用的是**子串计数**,扫的是**围栏全文含注释**(`scripts/check-10-idi10-validation.py` 的 `fence_text()` 语义,该函数只取两行 `===== DESIGN TOKENS: START/END` 之间的文本)。**这是本阶段最可能失败的一条**:实测 HEAD 上被删的卡片底色令牌在围栏内出现 **8 次**(注释 6 处 + 声明 1 处 + 两条 PAIR 条目 1 处各计),阴影令牌 **1 次**;⇒ **每一条点名它们的围栏内注释都必须改写成不写该令牌名的说法**,就像 Phase 10 的注释改写从不写出被删的那个圆角档位名一样"
    - "两条 PAIR 条目已按**元素实际绘制面重新归属**(不是刷新、不是调色、不是放宽阈值):原归属卡片底色的 `--color-marker-active … TEXT` 与 `--color-border-strong … NON-TEXT` 两条改记为统一面 `--color-surface-page`;`check-02` 的 `resolve()` 对未声明令牌 `sys.exit(1)`,故**重归属与删声明必须是同一次改动**,否则中间态会红"
    # ---- REG-02 — 清单重算与登记 ----
    - "`check-02` 打印 `PASS: 0 failures`;清单规模**逐字不变**:53 对(35 TEXT + 18 NON-TEXT)+ 1 条 ORDER;`TEXT_MIN = 4.5` / `NON_TEXT_MIN = 3.0` 与 HEAD **逐字节相同**(脚本文件零 diff);覆盖地板(≥24 对 / ≥20 TEXT / ≥4 NON-TEXT)与 `raw_pairs == len(pairs)` 标记计数一致性检查全部通过"
    - "六条页面地面 PAIR 以**新统一面(白)**重算并登记,实测值:正文 **16.29** / 次级正文 **5.92** / 弱化正文 **5.92** / 焦点环 NON-TEXT **5.87** / 输入悬停边界 NON-TEXT **5.92** / 活动标记 NON-TEXT **4.77** —— 全部达标,且比 HEAD 在 gray-3 上的读数**更高**(白面更亮,深色前景的对比度上升)"
    - "两条重归属后的实测值:活动标记 TEXT 在白面上 **4.77**(需 4.5);强边界 NON-TEXT 在白面上 **3.32**(需 3.0)。两条都**恰好擦边通过** —— 这是本阶段两条最紧的判据,须在 SUMMARY 里点名"
    - "`ORDER` 断言不退化:其操作数 `--color-text-muted` / `--color-text` 的地面都是 `--color-surface`(内陷面),**不在**本阶段改动面上 ⇒ 比值 `0.363` 逐字不变"
    - "`--color-surface`(gray-2)解析值 `rgb(249, 249, 249)` 的相对亮度 **0.947307** 仍**严格低于**统一面(白)的 **1.000000** ⇒ SC2 的「内陷面仍是唯一比统一面更暗的一档」成立;而旧的三档叙事(gray-3 页面档)已从围栏注释中消失"
    # ---- 注释纪律 ----
    - "围栏内**新增 / 改写**的任何注释都不含「令牌名 + 冒号」形态 —— `scripts/check-02-contrast.py` 的 `DECL_RE` 扫围栏全文含注释,`parse_decls` 让**最后一个**匹配胜出,写成「令牌名 + 冒号」会被当成一条值不可解析的声明而让 `resolve()` `exit 1`(本项目已为此红过一次,修法只是改写措辞)"
    - "围栏内注释**不得**出现 `/* PAIR` 或 `/* ORDER` 的**字面标记**(`check-02` 有一条 `raw_pairs == len(pairs)` / `raw_orders == len(orders)` 的标记计数一致性检查:散文里提到该标记会把裸计数顶高而 FAIL)"
    - "`frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**` 逐字节未改;`scripts/check-02-contrast.py` 零 diff;`scripts/check-09-idi09-validation.py` / `scripts/check-05-ui-uat.py` 本计划零改动(分别属计划 03 / 04)"

  artifacts:
    - path: "frontend/style.css"
      provides: "两个被孤立的令牌声明已删除;围栏内所有点名它们的注释已改写为不写令牌名的说法;两条 PAIR 条目重归属到统一面;新增 Phase 11 的地面重算登记段(六条重算值 + 两条重归属值)"
      contains: "Phase 11"

  key_links:
    - from: "被删的两个令牌声明"
      to: "`#main-pane > section` / `#doc-panel` / `#doc-panel-header` 的 `background` 与 `#main-pane > section` / `#doc-panel` 的 `box-shadow`"
      via: "计划 01 已把这 5 处消费者搬走 ⇒ 消费者归零 ⇒ 按围栏抬头与 Hard Rule 5 删除声明。顺序不可倒:先搬消费者,再删声明"
      pattern: "background: var\\(--color-surface-page\\);"
    - from: "两条重归属后的 PAIR 条目"
      to: "围栏内 `--color-surface-page: var(--white);`"
      via: "重归属改的是**地面标签**,不是颜色值 —— 期望侧由 `resolve()` 从新地面重算"
      pattern: "PAIR --color-marker-active ON --color-surface-page TEXT"
    - from: "`scripts/check-09-idi09-validation.py` 的两条专用残留断言(计划 03 写入)"
      to: "`frontend/style.css` 围栏内的文本"
      via: "`fence_text()` + `fenced.count(<令牌名>) == 0` —— 子串计数、含注释;故本计划的注释改写必须把令牌名**全部**消掉,不能只删声明行"
      pattern: "count\\(\"--color-surface-card\"\\)"

  prohibitions:
    - statement: "不得为了让门绿、或为了让某个旧读数继续成立,而删除 / 降级 / 放宽任何断言、阈值或判据。`TEXT_MIN` / `NON_TEXT_MIN` 与 HEAD 逐字节相同;`check-02` 的脚本文件零 diff;不得删除任何 PAIR / ORDER 条目(那会同时打破覆盖地板与标记计数一致性检查)"
      status: active
      verification: flagged
    - statement: "不得把「重归属」做成「刷新旧值」。两条卡片地面 PAIR 的地面标签必须真的改成统一面,六条页面地面 PAIR 必须按新地面**重算**;把旧数字原地保留、或只改数字不改地面标签,都会让清单描述一块**已不存在**的面 —— 那是「门绿着说谎」的形态"
      status: active
      verification: flagged
    - statement: "不得补一条**通用的**围栏消费断言(「每个声明的令牌都被消费」)。那是 G2,用户 2026-09-28 只裁定「连带 G1」,G2 **未点名**,留待下一里程碑。本阶段只处置**本次反转自己孤立掉的**两个令牌,每个令牌一条**专用**残留断言(计划 03 落地,照 Phase 10 删 28px 圆角档位时的 `r1` 同型)"
      status: active
      verification: flagged
---

<!-- planner-discipline-allow: --color-surface-card -->
<!-- planner-discipline-allow: --shadow-card -->

<objective>
处置本次反转**自己孤立掉的**两个令牌 —— 卡片底色令牌与卡片阴影令牌 —— 并把 `check-02` 对比度清单里**因本次改动而地面消失**的配对**按元素实际绘制面重新归属并重算**。

Purpose: 计划 01 把 5 处消费者搬到了统一面令牌上,两个卡片令牌的消费者因此归零。围栏抬头与 Hard Rule 5 / D-04 逐字要求「只声明被消费的令牌」—— Phase 10 正是援引这条规则删掉了那个 28px 圆角档位,并只给它加了一条**专用**残留断言。本计划按同一条规则处置这两个令牌。

**⚠ 这不是 G2。** G2 是「补一条**通用的**围栏消费断言 + 处置零消费的 `--radix-gray-1`」,已由用户明确排除在 v1.16 范围外(用户只裁定「连带 G1」)。本计划**只**处置本次改动自己孤立掉的两个令牌,**不得顺手补通用断言**。

为什么 `REG-02` 必须与反转同阶段:`check-02` 的两条卡片地面 PAIR 描述的**那块面在本阶段之后已不存在** —— 配对若不重新归属,数字仍然达标,但门会在描述一块不存在的面。这正是 ROADMAP Rationale 里「三条门在本阶段之后都会**绿着说谎**」的第二条。

**本计划关闭的需求:** REG-02。

**本计划不触碰:** `scripts/check-09-idi09-validation.py` 的 c1..c4 承重改写与两条专用残留断言(计划 03);`scripts/check-05-ui-uat.py`(计划 04);`scripts/check-02-contrast.py` 的**任何一行**(本计划只改它读的那份清单 —— 清单在 `frontend/style.css` 的围栏内);`frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**`(零字节);`G1-01` / `REG-04` / `VIS-01`(Phase 12);G2 / `999.2` / 暗色模式 / Nyquist 缺口 / 图标与空状态 / `.overlay-card` 底色(全部 Out of Scope);**C-10 的陈旧注释重归属**(`frontend/style.css` 围栏内 `:670-674` 那段声称 `#doc-panel` 声明内陷面底色的注释 —— 它在 Phase 9 就已失真,本阶段让它**更**失真,但重归属它**超出本阶段枚举的范围**:本计划只**登记**该事实,不得顺手改它)。

**执行前基线(规划期已在 HEAD 上实测,执行器须复核):**

| 检查 | 规划期在 HEAD 上的实测结果 |
|---|---|
| `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`;末行前含 `ORDER 0.363  --color-text-muted before --color-text on --color-surface`;含 `PASS  4.77  --color-marker-active on --color-surface-card` 与 `PASS  3.32  --color-border-strong on --color-surface-card` |
| 围栏内被删的卡片底色令牌出现次数 | **8**(注释 6 处 + 声明 1 处 + 该令牌名出现在一条 PAIR 条目的地面标签上 1 处) |
| 围栏内被删的卡片阴影令牌出现次数 | **1**(只有声明那一处) |
| 围栏内 28px 圆角档位名出现次数 | **0**(Phase 10 已删) |
| `grep -o '/\* PAIR' frontend/style.css \| wc -l` / `grep -o '/\* ORDER' …` | `53` / `1` |
| `git diff --exit-code -- scripts/check-02-contrast.py` | 空 |

**围栏内必须改写为「不再写出该令牌名」的注释区(以内容为锚,行号会漂):**

| # | 注释区的内容锚点 | HEAD 上点名了哪个待删令牌 |
|---|---|---|
| 1 | `Phase 9 sinks the page one step …` 段(统一面令牌声明上方,含三级刻度叙事与「Two of them … were re-attributed to the card ground by plan 01」) | 卡片底色令牌 |
| 2 | 活动标记令牌的 Tier-2 注释(含 `Phase 9 update (the value above is unchanged — only the ground moved) …` 与 `the colour is drawn on …` 那句) | 卡片底色令牌 |
| 3 | `Tier 2 — the card container language …` 五条承重事实注释块(**连同其下两行声明一起删除**) | 卡片底色令牌 + 卡片阴影令牌 |
| 4 | PAIR 清单头部注释 + `Phase 9 page-ground RECOMPUTATION ledger` 段(含 8 行重算表,表头有 `white` 一列) | 卡片底色令牌(2 处) |
| 5 | 活动标记 TEXT 那条 PAIR 条目**上方**的注释(含 `all three panels now declare a card background …` 与 `re-attributed to the card` 的说法) | 卡片底色令牌 |
| 6 | 强边界 NON-TEXT 那条 PAIR 条目**上方**的注释(含 `ground re-attributed (Phase 9) … the border is drawn on white` 的说法) | 卡片底色令牌 |

**两条要重归属的 PAIR 条目(逐字,以地面标签为锚):**

- 活动标记 TEXT 条目:地面标签由卡片令牌改为统一面令牌
- 强边界 NON-TEXT 条目:地面标签由卡片令牌改为统一面令牌

**六条要重算的页面地面 PAIR(地面标签不变,只重算数字并登记):** 正文 TEXT / 次级正文 TEXT / 弱化正文 TEXT / 焦点环 NON-TEXT / 输入悬停边界 NON-TEXT / 活动标记 NON-TEXT。

Output: `frontend/style.css` 的两个令牌声明删除 + 围栏内 6 个注释区的改写 + 两条 PAIR 重归属 + Phase 11 的地面重算登记段;`check-02` 的实跑输出(含八条新读数)。
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
@.planning/phases/idi-11-decard-and-hairline-dividers/11-CONTEXT.md
@.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-PATTERNS.md
@.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-01-PLAN.md
@.planning/milestones/v1.15-phases/idi-10-tables-and-radius-scale/10-CONTEXT.md
@frontend/style.css
@scripts/check-02-contrast.py
@scripts/check-10-idi10-validation.py
</context>

## Artifacts this phase produces

> 本节列出**本计划**那部分;全阶段的产出表在 `idi-11-01-PLAN.md` 的 §「Artifacts this phase produces」,不重复。

**删除的既有符号(计划 02,本计划):**

| # | 符号 | 锚点 | 动作 |
|---|---|---|---|
| 6 | 卡片底色令牌的声明行 | `Tier 2 — the card container language …` 注释块之后 | **删除**该行(3 处消费者已在计划 01 搬走) |
| 7 | 卡片阴影令牌的声明行 | 紧随 #6 之后 | **删除**该行(2 处消费者已在计划 01 搬走) |

**新增的围栏内注释区(计划 02):** `Phase 11` 的地面重算登记段 —— 逐条列出六条页面地面 PAIR 的重算值(白面)、两条重归属后的值、以及「与 Phase 9 的 gray-3 读数相比每一条都更高」的事实。**不得**只写一句「已重算」。

**本计划不产生的新符号:** 零新增 CSS 自定义属性、零新增颜色值、零新增 tier-1 primitive、零新增 / 零删除 PAIR / ORDER 条目、零新依赖。

## 波次与依赖形状

| 波次 | 计划 | 为什么必须在这个位置 |
|---|---|---|
| 1 | `idi-11-01` | 反转本体 —— 它把 5 处消费者从两个卡片令牌搬到统一面令牌上。**消费者不搬走,令牌就不能删**(否则页面在中间态会掉底色) |
| 2 | `idi-11-02`(本计划) | 与计划 01 同文件 ⇒ 必须错开波次。它读的是计划 01 的**结果**(消费者归零、统一面换值) |

<tasks>

<task type="auto" tdd="false">
  <name>Task 1: 删除两个被孤立的令牌声明 + 改写围栏内全部点名它们的注释 + 两条 PAIR 条目重归属</name>
  <files>frontend/style.css</files>
  <reversibility rating="costly">撤销要恢复两条声明、删除专用残留断言(计划 03)、并把 2 条 PAIR 的地面标签改回去(D-11-2 的 Reversibility 评级)。</reversibility>
  <read_first>
    - `frontend/style.css` 围栏内 `Tier 2 — the card container language (Phase 9 / VIS-01 / VIS-02 / CARD-01 / CARD-02)` 注释块**全文**(五条承重事实)**与其下紧邻的两行声明** —— **本任务的删除目标**。逐字读第 1 条的三档刻度叙事、第 2 条的用户裁定阴影值、第 4 条的「卡片圆角刻意不在此声明」、第 5 条的「卡片底色令牌是 `--white` 的别名 ⇒ Phase 9 零新增 tier-1 primitive」
    - `frontend/style.css` 围栏内 `--color-surface-page` 声明**上方**的 `Phase 9 sinks the page one step …` 注释全文 —— 含三级刻度叙事与「Two of them (the mid-tone blue-11 and gray-9 foregrounds) could not clear their thresholds on gray-3 and were re-attributed to the card ground by plan 01」那句(**本任务的改写目标之一**)
    - `frontend/style.css` 围栏内活动标记令牌(`--color-marker-active`)上方的 Tier-2 注释全文 —— 含 `Phase 9 update (the value above is unchanged — only the ground moved): both consumers live in .panel-header, and the three panels are now opaque white cards, so the colour is drawn on …` 一段
    - `frontend/style.css` 围栏内 PAIR 清单头部注释全文 + `Phase 9 page-ground RECOMPUTATION ledger` 段全文(含 8 行重算表与 `The last two are the complete chain, not a refresh` 一段)
    - `frontend/style.css` 围栏内活动标记 TEXT 那条 PAIR 条目**上方**的注释全文(含 `all three panels now declare a card background … measured 4.77 >= 4.5 there` 与 `re-attribution, not recolouring` 一段)
    - `frontend/style.css` 围栏内强边界 NON-TEXT 那条 PAIR 条目**上方**的注释全文(含 `ground re-attributed (Phase 9) … the border is drawn on white — a fact this file already registered verbatim in the hover-boundary note further down, together with the measured resting ratio 3.32 on white` 一段)
    - `frontend/style.css` 围栏内 `--color-surface: var(--radix-gray-2);` 与 `--color-surface-page: var(--white);`(计划 01 已改)两行声明,以及 `--white: #ffffff;` / `--radix-gray-2: #f9f9f9;` 两条 primitive
    - `frontend/style.css` 围栏内 `:670-674` 那段关于两个实心填充步的注释(含 `and #doc-panel declares background: var(--color-surface)` 一句)—— **本任务只读它、不改它**:它是 C-10 点名的**既有**陈旧注释,重归属它超出本阶段范围,只登记
    - `scripts/check-02-contrast.py` **全文** —— `DECL_RE` / `PAIR_RE` / `ORDER_RE` 的正则形态、`parse_decls` 的「最后一个匹配胜出」、`resolve()` 的「未知令牌即 `sys.exit(1)`」、覆盖地板、`raw_pairs == len(pairs)` / `raw_orders == len(orders)` 标记计数一致性、阈值常量 `TEXT_MIN = 4.5` / `NON_TEXT_MIN = 3.0`。**本任务一行都不改它**
    - `scripts/check-10-idi10-validation.py` 的 `fence_text()` 与 `r1` 的源码残留断言(`fenced.count(...) == 0`)—— **计划 03 要照抄的形态**,本任务须理解它的判据是**子串计数、含注释**
    - `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-PATTERNS.md` §"The two tokens to delete" / §"The fence-wide residue list (this is the forcing function)" / §"Analog C" / §"Analog D"
    - `.planning/ROADMAP.md` §`### Phase 11:` 的 Deliverable 6 / Success Criterion 5 / Avoids 第 7 条
  </read_first>
  <action>
    **第 1 步 —— 先搬完,再删(顺序不可倒)。**

    确认计划 01 已把这两个令牌的**全部 5 处消费者**搬走:4 个 `section` 与 `#doc-panel` / `#doc-panel-header` 的 `background` 已改指统一面令牌,`#main-pane > section` 与 `#doc-panel` 的 `box-shadow` 已改指 `none`。用 `grep -nF -- 'var(--color-surface-card)' frontend/style.css` 与 `grep -nF -- 'var(--shadow-card)' frontend/style.css` 逐行核对:**围栏外**(即规则体里)必须零命中;围栏内的命中全部是注释与那两条 PAIR 条目。若围栏外仍有命中,停下报回 —— 说明计划 01 漏搬了一处。

    **第 2 步 —— 删除两行声明。**

    在围栏内把那两行声明各删除一行:

    - 卡片底色令牌的声明行(`Tier 2 — the card container language …` 注释块之后的第一行)
    - 紧随其后的卡片阴影令牌的声明行

    **连同其上方那段 `Tier 2 — the card container language …` 注释块一起改写**(见第 3 步)。删除后围栏内不得留下任何指向已删声明的散句。

    **与删除配套的义务(本任务只做删除这一半):** 这两个被删的令牌名,各由**计划 03** 写入一条**专用**残留断言兜底(判据为围栏内子串计数 `fenced.count(...) == 0`),照 Phase 10 删除未并入刻度的圆角档位时给它加一条专用残留断言的先例 —— **D-11-4**。本任务负责把令牌删干净(第 3 步的注释改写 + 本步的声明删除),断言在计划 03 落地;**不得**在此补任何**通用**的围栏消费断言(D-11-4 与 `must_haves.prohibitions` 都明令禁止 —— 那是 G2,不在本里程碑范围)。

    **第 3 步 —— 改写 6 个注释区(逐条,以内容为锚)。**

    这是本任务**最容易失败**的一步。判据是**围栏内子串计数 == 0**,扫的是**含注释的围栏全文** ⇒ **每一条点名了这两个令牌的注释都必须改写成不写该令牌名的说法**。指代被删的档位一律用**概念短语**(如「the former card ground」「the retired card-surface alias」「the retired card shadow」),**不得**写出令牌名。Phase 10 删那个 28px 圆角档位时的注释就是这么写的 —— 它的替代注释里那个档位名一个字都没出现。

    逐条改写(顺序与本计划 objective 的表格一致):

    1. `Phase 9 sinks the page one step …` 段:三级刻度叙事改为**两级**(统一面白 > 内陷面 gray-2);「Two of them … were re-attributed to the card ground by plan 01」改为描述 Phase 9 那一次**与** Phase 11 这一次的两段历史(Phase 9 把它们搬去卡片地面,Phase 11 把卡片地面本身并回页面地面 ⇒ 它们自然回到页面地面,数值更高)。
    2. 活动标记令牌的 Tier-2 注释:把「三个面板现在是**不透明白卡片**,故该色画在卡片地面上」改为「三个面板与页面**同色**(统一面),故该色画在统一面上」;数值从卡片地面的 4.77 改为统一面的 4.77(见 Task 2 的实测)。**保留**该注释原有的「为什么 TEXT 半条要重归属」的因果链。
    3. `Tier 2 — the card container language …` 注释块:**整块重写**。五条事实里第 1 条(三档刻度)、第 2 条(阴影值)、第 4 条(圆角刻意不在此声明)、第 5 条(卡片底色是 `--white` 的别名)全部失去对象。新注释要记下:(a) Phase 9 曾在此声明卡片容器语言的两个令牌;(b) Phase 11 把面板并回统一面 ⇒ 两者消费者归零;(c) 依据是围栏抬头与 Hard Rule 5 / D-04「只声明被消费的令牌」,与 Phase 10 删除未并入刻度的圆角档位同型;(d) **明确写出「这不是通用围栏消费断言」**并点明通用断言属 G2、不在本里程碑范围;(e) 指代两个被删令牌时**不得写出它们的名字**。
    4. PAIR 清单头部注释 + `Phase 9 page-ground RECOMPUTATION ledger` 段:把「two entries move from page ground to the card ground」改为「Phase 11 把卡片地面并回页面地面 ⇒ 那两条回到页面地面,同时页面地面的六条全部重算」;旧表里 `white` 那一列的语义改写(白不再是「卡片」而是**统一面本身**);并追加本阶段的重算登记(见 Task 2)。**不得**写出被删令牌名,也**不得**出现 `/* PAIR` / `/* ORDER` 的字面标记。
    5. 活动标记 TEXT 条目上方的注释:把「三个面板现在声明卡片底色 ⇒ 该标题画在白卡片上」改为「面板与页面同色 ⇒ 该标题画在统一面上」;`re-attribution, not recolouring` 的立场句**保留**(它是本阶段同一条纪律的既有表述)。
    6. 强边界 NON-TEXT 条目上方的注释:把「地面重归属到卡片」的历史段落改写为「地面是统一面」;该注释里「输入控件不声明 background,Chrome 画 UA 白填充 ⇒ 边界画在白上」那条**既有事实**要保留(它在统一面下**更强**成立:统一面本身就是白)。

    **围栏内注释禁令(本任务加的任何围栏内注释都适用):** 不得出现「令牌名 + 冒号」形态;不得出现 `/* PAIR` / `/* ORDER` 字面标记;不得出现被删的两个令牌名。

    **第 4 步 —— 两条 PAIR 条目重归属。**

    把这两条条目的**地面标签**由卡片令牌改为统一面令牌(**只改标签,不改前景令牌、不改 `TEXT` / `NON-TEXT` 种类**):

    - 活动标记 `TEXT` 条目:地面标签 → `--color-surface-page`
    - 强边界 `NON-TEXT` 条目:地面标签 → `--color-surface-page`

    重归属后**不得产生重复条目**:围栏内已有一条活动标记的 `NON-TEXT` 条目(地面就是统一面)与一条强边界的 `NON-TEXT` 条目(地面是内陷面)—— 种类不同或地面不同,故无重复。改完后用 `grep -nF '/\* PAIR' frontend/style.css` 逐行核对:总行数仍为 53,且不存在两条完全相同的条目。

    **第 5 步 —— 跑 `check-02`,把输出原文抄进 SUMMARY。**

    `.venv/bin/python scripts/check-02-contrast.py`。要求 `PASS: 0 failures`。若报 `FAIL: unknown token`,说明还有条目在引用被删令牌 —— 回到第 4 步。若报 `FAIL: unparsable value for …`,说明围栏内注释里写出了「令牌名 + 冒号」形态 —— 回到第 3 步改措辞(**不要**改清单去迁就)。

    **第 6 步 —— 不触碰范围之外的一切。** 不改 `scripts/check-02-contrast.py` 一行;不改 `scripts/check-09-idi09-validation.py` / `scripts/check-05-ui-uat.py`;不改围栏外任何规则体;不改 `:670-674` 那段陈旧注释(C-10:只登记,不重归属);不改 `frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**`。
  </action>
  <verify>
    <automated>grep -nF -- 'var(--color-surface-card)' frontend/style.css; echo "rc=$?"; grep -nF -- 'var(--shadow-card)' frontend/style.css; echo "rc=$?"</automated>
    <fails_when>either grep prints a matching line (the two tokens must have zero consumers anywhere in the file after plan 01 + this task), or either `rc=` is not "1"</fails_when>
    <automated>.venv/bin/python -c "import pathlib;t=pathlib.Path('frontend/style.css').read_text(encoding='utf-8');f=t[t.index('===== DESIGN TOKENS: START ====='):t.index('===== DESIGN TOKENS: END =====')];print('card', f.count('--color-surface-card'));print('shadow', f.count('--shadow-card'));print('radius-lg', f.count('--radius-lg'))"</automated>
    <fails_when>any of the three printed counts is not "0" (the residue check is a substring count over the whole fence text INCLUDING comments — a single surviving comment that names either token fails this)</fails_when>
    <automated>.venv/bin/python scripts/check-02-contrast.py</automated>
    <fails_when>non-zero exit, or any line beginning with "FAIL", or the final line not exactly "PASS: 0 failures", or the output missing the lines for the two re-attributed pairs (`--color-marker-active on --color-surface-page` and `--color-border-strong on --color-surface-page`)</fails_when>
    <automated>grep -o '/\* PAIR' frontend/style.css | wc -l; grep -o '/\* ORDER' frontend/style.css | wc -l</automated>
    <fails_when>the two counts are not exactly "53" and "1" (re-attribution must not add or remove an entry)</fails_when>
    <automated>git diff --exit-code --stat -- scripts/check-02-contrast.py scripts/check-09-idi09-validation.py scripts/check-05-ui-uat.py</automated>
    <fails_when>exit code is not 0 — this check is intentionally about the UNCOMMITTED working tree: any listed file means the executor touched a gate script during this plan (only frontend/style.css may appear as modified)</fails_when>
    <automated>git status --porcelain frontend/ backend/</automated>
    <fails_when>output contains any path other than "frontend/style.css", or output is empty</fails_when>
  </verify>
  <acceptance_criteria>
    - 围栏内被删的卡片底色令牌名出现次数 == **0**;卡片阴影令牌名出现次数 == **0**;28px 圆角档位名出现次数仍 == **0**(Phase 10 的成果不得被本次注释改写破坏)。三条都由**子串计数、含注释**的围栏文本判据得出,不是「删了声明行」就算完。
    - 围栏外 `var(--color-surface-card)` 与 `var(--shadow-card)` 的消费者计数均为 **0**。
    - 两条 PAIR 条目的地面标签已改为统一面令牌;条目总数仍为 53;不存在两条完全相同的条目。
    - `check-02` 打印 `PASS: 0 failures`;其输出含两条重归属后的行(活动标记 TEXT 与强边界 NON-TEXT,地面均为统一面)。
    - 六个注释区已按内容锚点逐条改写:三档刻度叙事变为两级;「卡片地面」的表述一律改为「统一面」;`Tier 2 — the card container language …` 块被整块重写并显式声明「这不是通用围栏消费断言(那是 G2,不在本里程碑范围)」;`re-attribution, not recolouring` 的立场句保留。
    - 新增 / 改写的围栏内注释**不含**「令牌名 + 冒号」形态,**不含** `/* PAIR` / `/* ORDER` 字面标记,**不含**被删的两个令牌名。
    - `scripts/check-02-contrast.py` / `scripts/check-09-idi09-validation.py` / `scripts/check-05-ui-uat.py` 三个文件 `git diff` 均为空;`git status --porcelain frontend/ backend/` 仅列出 `frontend/style.css`。
    - C-10 的陈旧注释(`:670-674` 那段)被**登记**在 SUMMARY 里而**未被修改**。
  </acceptance_criteria>
  <done>两个被本次反转孤立掉的令牌声明已从围栏内删除;围栏内 6 个注释区已改写为不写令牌名的说法,围栏内两个令牌名的出现次数均为 0;两条 PAIR 条目按元素实际绘制面重归属到统一面;`check-02` 在 53 对清单上 `PASS: 0 failures`;`scripts/` 下三个门脚本零 diff;C-10 的既有陈旧注释已登记未改动。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 2: 六条页面地面 PAIR 以新统一面重算 + Phase 11 的重算登记段</name>
  <files>frontend/style.css</files>
  <reversibility rating="reversible">登记段是注释,回退是删段落;不牵连令牌层或消费者。</reversibility>
  <read_first>
    - `frontend/style.css` 围栏内 `Phase 9 page-ground RECOMPUTATION ledger` 段(**Task 1 已改写后的状态**)—— 本任务的追加锚点与格式模板
    - `frontend/style.css` 围栏内那六条页面地面 PAIR 条目(正文 TEXT / 次级正文 TEXT / 弱化正文 TEXT / 焦点环 NON-TEXT / 输入悬停边界 NON-TEXT / 活动标记 NON-TEXT)—— 本任务的**判据对象**;它们的地面标签**不变**,只有登记段里的数字要更新
    - `frontend/style.css` 围栏内 `--color-surface-page: var(--white);`(计划 01 已改)与 `--white: #ffffff;`
    - `scripts/check-02-contrast.py` 的 `resolve()` / `contrast_ratio()` / `composite()` 与输出格式(`PASS  %.2f  %s`)
    - `.planning/phases/idi-11-decard-and-hairline-dividers/11-CONTEXT.md` §D-11-15 与 §D-11-1 的三条理由
    - `.planning/ROADMAP.md` §`### Phase 11:` 的 Success Criterion 5
  </read_first>
  <action>
    **第 1 步 —— 实跑 `check-02`,把八条受影响的读数**逐行原文**抄出来。**

    `.venv/bin/python scripts/check-02-contrast.py`。在输出里找到这八行(地面是统一面或内陷面的那些),**逐字**抄进 SUMMARY:

    - 六条页面地面(地面 = 统一面):正文 TEXT / 次级正文 TEXT / 弱化正文 TEXT / 焦点环 NON-TEXT / 输入悬停边界 NON-TEXT / 活动标记 NON-TEXT
    - 两条重归属(地面 = 统一面):活动标记 TEXT / 强边界 NON-TEXT

    **⚠ 只贴本次实跑的输出行。** 规划期的估算值如下,仅作为「量级对不对」的粗筛,**不得**当作证据抄进 SUMMARY:正文 ≈ 16.29 / 次级正文 ≈ 5.92 / 弱化正文 ≈ 5.92 / 焦点环 NON-TEXT ≈ 5.87 / 输入悬停边界 NON-TEXT ≈ 5.92 / 活动标记 NON-TEXT ≈ 4.77 / 活动标记 TEXT ≈ 4.77 / 强边界 NON-TEXT ≈ 3.32。任何与实跑不符的数字一律以**实跑**为准。

    **第 2 步 —— 在清单里追加本阶段的重算登记段。**

    在 `Phase 9 page-ground RECOMPUTATION ledger` 段**之后**追加一段 `Phase 11` 的重算登记段(围栏内注释)。它必须逐条记下:

    (a) **改动的性质**:统一面由 gray-3 变为白(页面档并回卡片档的反向 —— 卡片档被并回页面档);八条配对受影响。
    (b) **六条是重算、不是刷新**:每一条给出「Phase 9 在 gray-3 上的读数 → Phase 11 在白面上的读数」两列,并写明方向(白面更亮 ⇒ 深色前景的对比度**上升**)。**不得**只写一个新数字而不写旧数字 —— 那样读不出「重算」与「刷新」的区别。
    (c) **两条是重归属**:原地面是卡片(白),新地面是统一面(也是白)⇒ **比值不变,变的是地面标签**。必须写明这一点:这两条的数字之所以不动,是因为白卡片与白统一面**同值**,不是因为「没重算」。**这是本阶段最容易被后人误读为「偷懒」的一处,注释要主动消解它。**
    (d) **两条最紧的判据点名**:活动标记 TEXT 需 4.5、强边界 NON-TEXT 需 3.0,两条都擦边通过;任何对这两个前景令牌或统一面取值的改动都会立刻打破它们。
    (e) **规模台账不变**:53 对(35 TEXT + 18 NON-TEXT)+ 1 条 ORDER;`ORDER` 的两个操作数地面都是内陷面,**不在**本阶段改动面上 ⇒ 比值不变。
    (f) **阈值未动**:`TEXT_MIN` / `NON_TEXT_MIN` 与 HEAD 逐字节相同。

    **围栏内注释禁令同样适用:** 不得出现「令牌名 + 冒号」;不得出现 `/* PAIR` / `/* ORDER` 字面标记;不得出现被删的两个令牌名(指代它们用「the former card ground」之类的概念短语)。

    **第 3 步 —— 复核规模与阈值。**

    - `grep -o '/\* PAIR' frontend/style.css | wc -l` == 53;`grep -o '/\* ORDER' frontend/style.css | wc -l` == 1。
    - `git diff --exit-code -- scripts/check-02-contrast.py` 为空(阈值与脚本逻辑逐字节不变)。
    - `check-02` 输出里的 `ORDER` 行仍为 `ORDER 0.363  --color-text-muted before --color-text on --color-surface`(数字逐字不变)。

    **第 4 步 —— 不触碰任何代码。** 本任务只追加/改写围栏内注释 + 跑命令 + 记录。任何一条不达标都按产品缺陷报回,不就地改清单、不就地改阈值、不就地改门。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-02-contrast.py</automated>
    <fails_when>non-zero exit, or any line beginning with "FAIL", or the final line not exactly "PASS: 0 failures", or the ORDER line not reading exactly "ORDER 0.363  --color-text-muted before --color-text on --color-surface"</fails_when>
    <automated>grep -cF -- 'Phase 11' frontend/style.css</automated>
    <fails_when>the count is "0" (the Phase 11 recomputation ledger must be present inside the fence)</fails_when>
    <automated>.venv/bin/python -c "import pathlib;t=pathlib.Path('frontend/style.css').read_text(encoding='utf-8');f=t[t.index('===== DESIGN TOKENS: START ====='):t.index('===== DESIGN TOKENS: END =====')];print('card',f.count('--color-surface-card'),'shadow',f.count('--shadow-card'),'pairmark',f.count('/* PAIR'),'ordermark',f.count('/* ORDER'))"</automated>
    <fails_when>the four counts are not exactly "0 0 53 1" in that order (the new ledger prose must not name the deleted tokens, and must not contain the literal PAIR/ORDER marker text)</fails_when>
    <automated>grep -o '/\* PAIR' frontend/style.css | wc -l; grep -o '/\* ORDER' frontend/style.css | wc -l</automated>
    <fails_when>the two counts are not exactly "53" and "1"</fails_when>
    <automated>git diff --exit-code -- scripts/check-02-contrast.py</automated>
    <fails_when>exit code is not 0 — this check is intentionally about the UNCOMMITTED working tree: a non-empty diff means the executor edited that gate script during this plan (this plan's edits live in frontend/style.css's fence, never in the script)</fails_when>
  </verify>
  <acceptance_criteria>
    - `check-02` 打印 `PASS: 0 failures`;八条受影响配对的**实跑输出行原文**被逐字抄进 SUMMARY(不是规划期的估算值)。
    - 围栏内存在 `Phase 11` 的重算登记段,且它逐条给出「Phase 9 的 gray-3 读数 → Phase 11 的白面读数」两列(六条),并显式写明两条重归属的比值**不变的原因**(白卡片与白统一面同值),以及两条最紧判据(4.5 / 3.0)的点名。
    - 围栏内被删的两个令牌名出现次数仍为 **0**;围栏内 `/* PAIR` 计数为 53、`/* ORDER` 计数为 1;围栏内注释不含「令牌名 + 冒号」形态。
    - `ORDER` 行的数字与 HEAD 逐字相同(`0.363`);`git diff --exit-code -- scripts/check-02-contrast.py` 为空。
    - 本任务没有编辑任何文件(除 `frontend/style.css` 的围栏内注释)。
  </acceptance_criteria>
  <done>六条页面地面 PAIR 以新统一面重算并登记(每条的旧值与新值并排),两条重归属的「比值不变但地面标签已改」被显式消解,两条最紧判据被点名,规模台账与阈值逐字不变;`check-02` `PASS: 0 failures` 且 `ORDER 0.363` 未退化。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 3: 统一面的运行时读数 + 四条静态门与「零新增 / 零放宽」逐字节证据</name>
  <files>frontend/style.css</files>
  <reversibility rating="reversible">本任务只做取证与记录,不产生产品代码改动。</reversibility>
  <read_first>
    - `scripts/check-09-idi09-validation.py` 的 `c3()` 全文 —— 逐字读它的 `info()` 行格式(`c3 body 计算 background-color 原始读数`、`c3 内陷面 --color-surface 解析值`、`c3 页面 --color-surface-page 解析值`)。**本任务一行都不改它**
    - `scripts/check-01-token-conformance.sh` / `scripts/check-03-hidden-uniqueness.sh` / `scripts/check-04-important-count.sh` 全文 —— 各自的计数逻辑(围栏外裸 `#hex` 与 tier-1 原语引用、`^\.hidden {` 计数、`!important;` **声明**计数)
    - `.planning/phases/idi-11-decard-and-hairline-dividers/11-CONTEXT.md` §D-11-3(两个「不产生新孤儿」的已核实事实)与 §D-11-1 的三条理由
    - `.planning/ROADMAP.md` §`### Phase 11:` 的 Gates 行与 Success Criterion 2
  </read_first>
  <action>
    **第 1 步 —— 统一面的真实浏览器读数。**

    跑 `.venv/bin/python scripts/check-09-idi09-validation.py --item c3`,把这三行**原文**抄进 SUMMARY:

    - `INFO c3 body 计算 background-color 原始读数` —— 要求 `rgb(255, 255, 255)`
    - `INFO c3 内陷面 --color-surface 解析值` —— 要求 `rgb(249, 249, 249)`
    - `INFO c3 页面 --color-surface-page 解析值` —— 要求 `rgb(255, 255, 255)`

    并要求 c3 打印的相对亮度诊断行满足「内陷面(≈0.947307) **严格低于** 统一面(1.000000)」。**门此时会报 FAIL / BLOCKED —— 设计预期**(它断言的仍是 gray-3 页面档的三级刻度;被删令牌那一档会让它记 BLOCKED)。**不要修改 `check-09`** —— 计划 03 拥有它。

    这一条读数是 SC2 的**运行时**证据:统一面与内陷面仍相差一档,「统一」是把卡片档并回页面档,**不是**把层次压平。

    **第 2 步 —— 两个「不产生新孤儿」事实的复核(D-11-3 已在规划期核实,本步只复核不重查)。**

    用 `grep -n` 逐行核对(不要只数个数):统一面令牌被改值后,`--radix-gray-3` 仍有 `--color-surface-sunken` 与 `--color-surface-hover` 两个消费者 ⇒ 换值**没有**造出新的零消费 primitive;`--radix-gray-2` 恰一个消费者(`--color-surface`),未受影响。把两条复核结论写进 SUMMARY。

    **第 3 步 —— 「零新增颜色值 / 零新增 primitive / 零阈值改动 / 零清单增删」的逐字节证据。**

    - `git diff --exit-code -- scripts/check-02-contrast.py` **为空** ⇒ `TEXT_MIN` / `NON_TEXT_MIN` 与 HEAD 逐字节相同。**放宽阈值是「把门改小以让结论成立」,本仓库明令禁止。**
    - `git diff -U0 -- frontend/style.css` 的输出里**不存在**任何以 `--radix-` 开头的**新增**行 ⇒ 零新增 primitive。(注意:本阶段**删除**了一行以 `--radix-gray-3` 为值的声明引用?不 —— 该 primitive 本身仍在,只是统一面令牌不再指向它。判据只禁**新增**,删除行按 Task 1 的围栏计数判据处置。)
    - `grep -o '/\* PAIR' frontend/style.css | wc -l` == **53**、`grep -o '/\* ORDER' frontend/style.css | wc -l` == **1**。
    - `frontend/style.css` 里 `@media` 出现次数仍**恰为 1**(Phase 7 的 prefers-reduced-motion 块)—— `scripts/check-05-ui-uat.py` 有一条读文件文本的静态断言锁死这个数。
    - 围栏内新增注释不含「令牌名 + 冒号」形态(`check-02` 的 `DECL_RE` 扫围栏全文含注释)。

    **第 4 步 —— 四条静态门逐条记录原始输出。** `bash scripts/check-01-token-conformance.sh` / `.venv/bin/python scripts/check-02-contrast.py` / `bash scripts/check-03-hidden-uniqueness.sh` / `bash scripts/check-04-important-count.sh`。把每条的**标准输出原文**与**退出码**抄进 SUMMARY。

    **第 5 步 —— 零改动边界。** `git status --porcelain frontend/ backend/ scripts/` 只应列出 `frontend/style.css`;`git diff --stat -- frontend/app.js frontend/index.html backend/ frontend/vendor/` 为空。

    **第 6 步 —— 不触碰任何代码。** 本任务只跑命令与记录(SUMMARY 除外)。任何一条不达标都按产品缺陷报回,不就地修。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c3 2>&1 | grep -E 'INFO c3 (body 计算 background-color 原始读数|内陷面 --color-surface 解析值|页面 --color-surface-page 解析值)|INFO c3 (内陷面|页面|卡片) 相对亮度'</automated>
    <fails_when>any of the three value INFO lines is missing, or the body background line does not read `rgb(255, 255, 255)`, or the inset-surface line does not read `rgb(249, 249, 249)`, or the page line does not read `rgb(255, 255, 255)`, or the inset luminance is not strictly below the page luminance. (check-09's FAIL/BLOCKED verdicts here are EXPECTED; do not edit check-09 in this plan)</fails_when>
    <automated>git diff --exit-code -- scripts/check-02-contrast.py</automated>
    <fails_when>exit code is not 0 — this check is intentionally about the UNCOMMITTED working tree: a non-empty diff means the executor edited the contrast gate script during this plan (its threshold constants must stay byte-identical to HEAD)</fails_when>
    <automated>git --no-pager diff -U0 -- frontend/style.css > /tmp/idi-11-style-diff.txt && grep -n '^+.*--radix-' /tmp/idi-11-style-diff.txt; echo "rc=$?"</automated>
    <fails_when>any matching line is printed, or rc is not "1" (rc 1 == no added `--radix-` line; any other rc means the git stage failed and the diff file must not be trusted)</fails_when>
    <automated>grep -o '/\* PAIR' frontend/style.css | wc -l; grep -o '/\* ORDER' frontend/style.css | wc -l; grep -nF -- '@media' frontend/style.css</automated>
    <fails_when>the first two printed numbers are not exactly "53" and "1", or the `grep -nF` output does not consist of exactly one line — the single Phase 7 prefers-reduced-motion block (a second line means a media query was added; `check-05` has a static assertion that locks this count, so read the listed line numbers and confirm the one line is that block)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>non-zero exit for any of the three, or any of the three not printing exactly "PASS"</fails_when>
    <automated>git status --porcelain frontend/ backend/ scripts/</automated>
    <fails_when>output contains any path other than "frontend/style.css", or output is empty</fails_when>
  </verify>
  <acceptance_criteria>
    - `check-09 --item c3` 的三行值 INFO 原文入册:body 计算底色 `rgb(255, 255, 255)`、内陷面令牌解析 `rgb(249, 249, 249)`、统一面令牌解析 `rgb(255, 255, 255)`;相对亮度诊断显示内陷面严格低于统一面。
    - SUMMARY 记下 D-11-3 的两条复核:统一面换值**未**造出新的零消费 primitive(`--radix-gray-3` 仍有 2 个消费者);`--radix-gray-2` 恰 1 个消费者、未受影响。
    - `git diff --exit-code -- scripts/check-02-contrast.py` 为空;SUMMARY 明确记下 `TEXT_MIN` / `NON_TEXT_MIN` 与 HEAD 逐字节相同。
    - `git diff -U0 -- frontend/style.css` 的新增行里以 `--radix-` 开头的行数为 **0**。
    - `grep -o '/\* PAIR' | wc -l` == 53;`grep -o '/\* ORDER' | wc -l` == 1;`grep -nF -- '@media' frontend/style.css` 恰列出一行(Phase 7 的 prefers-reduced-motion 块)。
    - 四条静态门的退出码与标准输出原文都抄进了 SUMMARY;`check-01` / `check-03` / `check-04` 各打印 `PASS`,`check-02` 打印 `PASS: 0 failures`。
    - `git status --porcelain frontend/ backend/ scripts/` 仅列出 `frontend/style.css`。
    - 本任务没有编辑任何文件(除 SUMMARY)。
  </acceptance_criteria>
  <done>统一面的运行时读数证明「卡片档并回页面档、内陷面仍是唯一更暗的一档」;零新增 primitive / 零阈值改动 / 零清单增删 / 零媒体查询五项逐字节取证;两个「不产生新孤儿」事实复核完毕;四条静态门全绿且原文入册。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 无外部输入边界 | 本计划只改 `frontend/style.css` 围栏内的**声明与注释**(令牌层),并读一个静态门脚本的输出:零用户输入处理、零鉴权、零数据访问、零网络调用。攻击面限于**门脚本对围栏文本的解析** |
| 本地进程边界(既有门脚本) | 运行时读数取自**既有** `check-09`(它自起/复用 `uvicorn` 并驱动无头 chromium)。本计划一行都不改它 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-11-07 | Tampering | 围栏内清单的**地面标签**(两条 PAIR 条目) | **high** | mitigate | 若重归属做成了「只改数字、不改地面标签」,清单会继续描述一块**已不存在**的面(白卡片),而数字仍达标 —— 那是本仓库明令禁止的「门绿着说谎」。缓解:(a) 重归属与删声明**同一次改动**(`check-02` 的 `resolve()` 对未声明令牌 `sys.exit(1)`,顺序倒了中间态直接红);(b) 判据是 `check-02` 实跑输出里出现 `--color-marker-active on --color-surface-page` 与 `--color-border-strong on --color-surface-page` 两行,**不是**「我觉得改了」;(c) 围栏内被删令牌名的出现次数必须为 0,故不可能留下一条仍指向卡片地面的条目 |
| T-idi-11-08 | Tampering | 围栏内注释(子串计数判据的判定面) | **high** | mitigate | 残留判据是**子串计数、含注释**,实测 HEAD 上被删令牌在围栏内出现 8 次 / 1 次 —— 只删声明行会立刻让判据失败。缓解:(a) 判据在计划里写明是「含注释的围栏全文子串计数」;(b) 六个注释区按**内容锚点**逐条列出,不是「自己找找」;(c) 指代被删令牌一律用概念短语,Phase 10 删圆角档位时已有同型先例;(d) 验收含一条独立的围栏内计数命令 |
| T-idi-11-09 | Tampering | 阈值与清单规模 | **high** | mitigate | 「把门改小以让结论成立」是本仓库最严重的错向。缓解:(a) `git diff --exit-code -- scripts/check-02-contrast.py` 必须为空;(b) 条目数 53 / 1 由两条独立计数命令判据;(c) 覆盖地板与 `raw_pairs == len(pairs)` 标记计数一致性由 `check-02` 自身在每次运行时检查 —— 本计划的注释改写**不得**引入 `/* PAIR` / `/* ORDER` 字面标记 |
| T-idi-11-10 | Repudiation | 「地面已重新归属并重算」这一结论缺少可复核的原始证据 | medium | mitigate | 八条受影响配对的**实跑输出行原文**必须抄进 SUMMARY(不是估算值);重算登记段必须并排给出旧值与新值,使「重算」与「刷新」可区分。验收:SUMMARY 含八行 `PASS  <比值>  <前景> on <地面>` 原文 |
| T-idi-11-11 | Denial of Service | 无 | low | accept | 纯声明层与注释层改动,无可用性面 |
| T-idi-11-SC | Tampering | npm / pip / cargo 安装 | low | accept | 本阶段**零安装**:零新增依赖、零构建步骤(DESIGN.md D-06 硬约束)。验收:`ls frontend/vendor/` 仅 `marked.min.js` |
</threat_model>

<verification>
**静态门(全部必须绿):**

- `bash scripts/check-01-token-conformance.sh` → `PASS`
- `.venv/bin/python scripts/check-02-contrast.py` → `PASS: 0 failures`,且 `ORDER 0.363` 逐字未变
- `bash scripts/check-03-hidden-uniqueness.sh` → `PASS`
- `bash scripts/check-04-important-count.sh` → `PASS`

**围栏内计数(源码文本级,含注释):**

- 卡片底色令牌名 == **0**;卡片阴影令牌名 == **0**;28px 圆角档位名 == **0**
- `/* PAIR` == 53;`/* ORDER` == 1

**运行时读数(经既有 `check-09`,逐行抄录 INFO 原文):**

- `.venv/bin/python scripts/check-09-idi09-validation.py --item c3` → body 底色 `rgb(255, 255, 255)`;内陷面令牌 `rgb(249, 249, 249)`;统一面令牌 `rgb(255, 255, 255)`;内陷面亮度严格低于统一面

**仓库卫生:**

- `git diff --exit-code -- scripts/check-02-contrast.py` 为空
- `git diff -U0 -- frontend/style.css` 的新增行里 `--radix-` 计数为 0
- `git status --porcelain frontend/ backend/ scripts/` 仅列出 `frontend/style.css`
- `ls frontend/vendor/` 仅 `marked.min.js`
</verification>

<success_criteria>
- 两个被本次反转孤立掉的令牌声明已删除,且**围栏内**它们的名字出现次数为 0(子串计数、含注释)。
- `check-02` 在 53 对清单上 `PASS: 0 failures`;两条卡片地面 PAIR 已按元素实际绘制面重归属到统一面;六条页面地面 PAIR 已按新统一面重算并登记(旧值与新值并排)。
- `TEXT_MIN` / `NON_TEXT_MIN` 与 HEAD 逐字节相同(`check-02` 脚本零 diff);`ORDER 0.363` 不退化;清单规模 53 + 1 逐字不变。
- 统一面与内陷面的亮度序在运行时仍成立(内陷面严格更暗),证明「统一」不是「压平」。
- 零新增颜色值 / 零新增 tier-1 primitive / 零新增 `@media`;四条静态门全绿。
- 围栏内注释不含「令牌名 + 冒号」、不含 `/* PAIR` / `/* ORDER` 字面标记、不含被删令牌名。
- `scripts/` 下三个门脚本零 diff;`frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**` 逐字节未改。
- **未**补任何通用围栏消费断言(G2 不在本里程碑范围);**未**重归属 C-10 的既有陈旧注释(只登记)。
</success_criteria>

<output>
Create `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-02-SUMMARY.md` when done
</output>

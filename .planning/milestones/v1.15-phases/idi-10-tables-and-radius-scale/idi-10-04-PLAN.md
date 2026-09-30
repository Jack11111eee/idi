---
phase: idi-10-tables-and-radius-scale
plan: 04
type: execute
wave: 4
depends_on:
  - idi-10-03
files_modified:
  - .planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md
  - .planning/phases/idi-10-tables-and-radius-scale/gate-logs/
autonomous: true
requirements:
  - REG-03

estimate:
  tokens: 55000
  raw_tokens: 55000
  tasks: 2
  confidence: low

must_haves:
  truths:
    # ---- REG-03 的「10 份覆盖,1 份可执行」口径 ----
    - "覆盖面判据锚的是**报告 frontmatter 的 `covered_files` 逐行匹配** `  - frontend/style.css`,不是全文 grep —— 全文 grep 会把只在正文里提及该文件的报告也算进来(例如 `idi-08`)。`idi-08` **不在**名单内,且这一点有独立证据(`idi-08` 的 frontmatter `covered_files` 里零 `frontend/style.css` 行)"
    - "逐份实测覆盖名单,结果恰为 **10 份** `status: passed` 报告:`.planning/milestones/v1.13-phases/` 下 3 份(idi-01 / idi-02 / idi-03)+ `.planning/milestones/v1.14-phases/` 下 5 份(idi-04 / idi-04.1 / idi-05 / idi-06 / idi-07)+ `.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md` + `.planning/quick/260925-iin-v1-14-ai-999-1/260925-iin-VERIFICATION.md`"
    - "对其中**每一份**跑 `node .claude/gsd-core/bin/gsd-tools.cjs query verification.status <该报告的 phase 目录>`,把原始 JSON 抄进 SUMMARY。**9 份**返回 `\"status\": \"stale\"`;`idi-09` 在重新验证**之前**返回 `\"status\": \"stale\"`(因为 `frontend/style.css` 确实变了),在重新验证**之后**返回 `\"status\": \"passed\"`"
    - "对**每一份**再跑 `node .claude/gsd-core/bin/gsd-tools.cjs query verification.fingerprint <该报告的 phase 目录> <它 frontmatter 里列出的 covered_files…>`,把原始输出抄进 SUMMARY。**9 份**以 `Error: could not compute fingerprint — a covered file is missing, unreadable, or escapes the project root` 失败关闭(fail-closed),`idi-09` 成功并返回一个 `v1:sha256:…` 摘要"
    - "9 份失败关闭的**成因**被逐份实测出来:`frontend/style.css` 之外的 `covered_files` 条目在归档时由 `.planning/phases/<id>/…` 移到了 `.planning/milestones/<ver>-phases/<id>/…` ⇒ 原路径不可解析 ⇒ 重算返回 `null` ⇒ fail-closed stale。每份的「缺失项数 / 总项数」都实测并记录(不沿用任何未经本次复现的数字)。这是 STATE.md 于 **2026-09-14** 登记、并在 v1.13 收口时复认的**已知限制**「归档后的报告不再被 staleness 机制消费」⇒ 它们在 Phase 10 **之前**就已是 fail-closed stale,与本次改动无关"
    - "本阶段只重新验证 `idi-09` **一份**,并在 SUMMARY 里逐条引用上述实测证据说明其余 9 份为何**不在本阶段边界内**(成因是**路径**而非内容;重验它们须先修复归档路径引用 —— 那是另一件已登记的 backlog 事项)。**不得**只写「已知限制」而不给逐份证据"
    - "本阶段**未改动** `scripts/check-05-ui-uat.py`(它在 `idi-08` 的 `covered_files` 里)⇒ 重验面被严格限制在 1 份。判据:`git diff -- scripts/check-05-ui-uat.py` 为空"
    # ---- idi-09 以 HEAD 内容重新验证(不是刷新指纹)----
    - "`.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md` 的 frontmatter `covered_files` 仍是原来的 **10** 条(逐条未变);`covered_digest` 是**重新计算**出来的新值(与旧值不同 —— 因为 `frontend/style.css` 确实变了);`status` 为 `passed`;`score` 为 `24/24 must-haves verified`"
    - "该报告的 `re_verification:` 块记录了 `previous_status: passed`、`previous_score: 24/24`、以及 `gaps_closed` / `gaps_remaining` / `regressions` 三个列表(预期三者皆为**空**;若非空,该项必须同时在正文与 SUMMARY 里逐条说明,不得静默丢弃)"
    - "该报告的正文含一节「Why this is a re-verification, and what changed」,**点名本阶段改动的那一个 `covered_file`(`frontend/style.css`)** 并说明改了什么(表格规则就地改写 + `.markdown-body th` 浅底;圆角刻度收敛为三档、`--radius-lg` 删除、两处消费者改归属)。**不得**把这份重验写成「刷新指纹」—— 刷新等于断言「自验证以来覆盖输入无变化」,那是不实陈述"
    - "idi-09 的 **24 条 must-have 逐条以 HEAD 内容重新推导**并给出结论。预期 24/24 仍成立(本阶段不改任何卡片容器的底色 / 边界 / 圆角令牌 / 阴影,也不改 `--radius-md`,而 `check-09` 的 c1…c5 在 HEAD 上仍全绿);若任何一条不再成立,它进 `gaps_remaining` 或 `regressions` 并作为**未关闭项**报回"
    - "重新验证后 `node .claude/gsd-core/bin/gsd-tools.cjs query verification.status .planning/phases/idi-09-card-containers` 返回 `\"status\": \"passed\"`(而不是 `stale`)—— 这是「重签的指纹与 HEAD 相符」的机器判据"
    # ---- 不得越界 ----
    - "只改 `idi-09-VERIFICATION.md` 一个文件。**不得**改动其余 9 份报告的任何字节(它们的 stale 成因是路径,修补它们要先修归档路径引用 —— 不在本阶段边界内);**不得**改动任何产品代码 / 门代码 / 被测样本"
    - "**不得**把某份报告从 `stale` 改成 `passed` 而不真正重跑其判据;不得删除或跳过任何 must-have;不得改动任何门脚本或阈值"

  artifacts:
    - path: ".planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md"
      provides: "以 HEAD 内容重新验证的 Phase 9 报告:`covered_digest` 重算、`status: passed`、`score: 24/24`、`re_verification:` 块(previous_status / previous_score / 三个空列表)、正文「Why this is a re-verification, and what changed」一节点名 `frontend/style.css` 被本阶段改动"
    - path: ".planning/phases/idi-10-tables-and-radius-scale/gate-logs/verification-recheck.log"
      provides: "10 份报告的 `verification.status` 与 `verification.fingerprint` 原始输出,以及逐份「缺失项数 / 总项数」的实测记录"
    - path: ".planning/phases/idi-10-tables-and-radius-scale/idi-10-04-SUMMARY.md"
      provides: "覆盖面判据(锚 frontmatter 逐行匹配,非全文 grep)、10 份报告的逐份分诊证据、idi-09 的重新验证过程与 24 条 must-have 的逐条复核结论"

  key_links:
    - from: "报告 frontmatter 的 `covered_files` 逐行匹配"
      to: "「覆盖 `frontend/style.css` 的 passed 报告有几份」这一计数"
      via: "只锚 frontmatter 的列表行 —— 全文 grep 会把只在正文提及该文件的报告也算进来(`idi-08` 就是那个假阳性)"
      pattern: "covered_files"
    - from: "`node .claude/gsd-core/bin/gsd-tools.cjs query verification.status <phase dir>`"
      to: "每份报告的 staleness 分诊结论"
      via: "归档的 9 份返回 `stale`;`idi-09` 在重签后返回 `passed`"
      pattern: "\"status\""
    - from: "`node .claude/gsd-core/bin/gsd-tools.cjs query verification.fingerprint <phase dir> <covered files…>`"
      to: "idi-09 重签所需的 `covered_digest`"
      via: "该命令做确定性哈希,且**失败关闭**(任一覆盖文件缺失即报错、不产出部分指纹)"
      pattern: "v1:sha256:"
    - from: "`frontend/style.css` 在本阶段被本阶段的两个计划改动"
      to: "`idi-09-VERIFICATION.md` 的 `covered_digest` 变 stale"
      via: "它是该报告 10 条 `covered_files` 之一 ⇒ 唯一的连带指纹债务;重验面恰为 1 份"
      pattern: "frontend/style.css"

  prohibitions:
    - statement: "**不得把重新验证写成刷新指纹。** 「以 HEAD 内容重新验证」意味着:重跑该报告的判据、逐条复核它的 must-have、在正文里点名被改动的 `covered_file` 与改动内容,然后**重新计算** `covered_digest`。刷新指纹(只更新摘要数字而不重跑判据)等于断言「自验证以来覆盖输入无变化」,那是不实陈述"
      status: active
      verification: flagged
    - statement: "**不得改动其余 9 份报告的任何字节。** 它们的 stale 成因是归档后 `covered_files` 路径不可解析,不是内容变化;修补它们要先修归档路径引用 —— 那是 STATE.md 于 2026-09-14 登记的另一件 backlog 事项,不在本阶段边界内。本计划只写 `idi-09-VERIFICATION.md`"
      status: active
      verification: flagged
    - statement: "**不得改动 `scripts/check-05-ui-uat.py`。** 它在 `idi-08` 的 `covered_files` 里(`idi-08` 不含 `frontend/style.css`)⇒ 改它会把重验面从 1 份变成 2 份(ROADMAP Deliverables 与 Pitfalls 逐字写明)。判据:`git diff -- scripts/check-05-ui-uat.py` 为空"
      status: active
      verification: flagged
    - statement: "不得删除、跳过或弱化 `idi-09-VERIFICATION.md` 的任何一条 must-have。24 条逐条以 HEAD 内容重新推导;任何一条不再成立都必须进 `gaps_remaining` / `regressions` 并作为未关闭项报回,**不得**静默丢弃,也不得通过改写判据让它成立"
      status: active
      verification: flagged
    - statement: "不得为了把 `verification.status` 跑成 `passed` 而:改 `covered_files`(删掉不可解析的条目、或把条数改小)、改 `covered_digest` 的算法输入、改 `frontend/style.css` 去迁就旧摘要、或改门脚本 / 阈值。唯一的合法路径是**真的重跑判据 + 重新计算摘要**"
      status: active
      verification: flagged
    - statement: "不得改动任何产品代码(`frontend/` 全部文件)、门代码(`scripts/` 全部文件)、被测样本(`scripts/ui-states/`)或 `.planning/` 下除 `idi-09-VERIFICATION.md` 与本阶段 `gate-logs/` 之外的任何文件"
      status: active
      verification: flagged
    - statement: "不得新增依赖、构建步骤或任何新的应用文件(DESIGN.md D-06)。本阶段**零安装**:Playwright / chromium 均已在项目 `.venv` 中就绪;`frontend/vendor/` 仍只有 `marked.min.js`"
      status: active
      verification: flagged
---

<objective>
把 `frontend/style.css` 变更所触及的连带指纹债务收口:先以**实测**证据判定真实形状是「**10 份覆盖,1 份可执行**」,再对唯一可执行的那一份(`idi-09-VERIFICATION.md`)**以 HEAD 内容重新验证**(不是刷新指纹)。

Purpose: 本阶段改的唯一产品文件 `frontend/style.css` 出现在**多份** `status: passed` 报告的 `covered_files` 里,每一份都带 `covered_digest` ⇒ 理论上都会因这次改动而 stale。但「覆盖了多少份」与「需要重验多少份」是**两个不同的问题**。规划期在磁盘上逐份实测出的真实形状是:

| 判据 | 结果 |
|---|---|
| frontmatter `covered_files` 逐行含 `  - frontend/style.css` 的 `passed` 报告 | **10 份**(v1.13 三份 + v1.14 五份 + `idi-09` + quick `260925-iin`) |
| 其中 `covered_files` 路径**仍在盘上**的 | **1 份**(`idi-09`;其余 9 份缺失数 12/41、11/26、13/31、8/13、8/12、8/11、8/10、6/9、2/7) |

9 份的 stale 成因是**路径**(归档后 `.planning/phases/<id>/…` 移到了 `.planning/milestones/<ver>-phases/<id>/…`)⇒ `verification.fingerprint` **失败关闭** ⇒ 它们在 Phase 10 **之前**就已是 fail-closed stale。这是 STATE.md 于 **2026-09-14** 登记、并在 v1.13 收口时复认的已知限制(「归档后的报告不再被 staleness 机制消费,故记为已知限制而非回填重算」)。⇒ **本阶段实际要重验的只有 1 份:`.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md`。**

处置法仍是「**以 HEAD 内容重新验证**」:`.chat-user` / `#chat-input-row input` / `.markdown-body` 的改动虽然不触碰 `idi-09` 报告断言的卡片容器语言,但 `frontend/style.css` 这个**覆盖输入**确实变了 —— 刷新指纹等于断言「自验证以来覆盖输入无变化」,那是**不实陈述**。所以本计划重跑该报告的判据、逐条复核它的 24 条 must-have、在正文里点名改了什么,然后重新计算 `covered_digest`。

**两条判据必须锚对(ROADMAP Pitfalls 的最后一条):**
- 锚 **frontmatter 的 `covered_files` 逐行匹配**,不是全文 grep —— 全文 grep 会把只在正文提及该文件的报告也算进来(`idi-08` 就是那个假阳性);
- 额外测「**路径是否还在盘上**」—— 只看覆盖名单会把 10 份都算成债务,只看路径解析又会把 `idi-09` 漏掉。

**已实测的分诊工具(规划期在本机跑通,执行器须逐份复跑):**
- `node .claude/gsd-core/bin/gsd-tools.cjs query verification.status <phase dir>` → `{"status": …}`;归档报告返回 `"status": "stale"`,HEAD 上的 `idi-09` 返回 `"status": "passed"`,未收口的 `idi-10` 返回 `"status": "missing"`
- `node .claude/gsd-core/bin/gsd-tools.cjs query verification.fingerprint <phase dir> <covered files…>` → 成功时 `{"covered_files": […], "covered_digest": "v1:sha256:…"}`;任一覆盖文件缺失时 `Error: could not compute fingerprint — a covered file is missing, unreadable, or escapes the project root`(**失败关闭**,不产出部分指纹)

**前置(执行前须复核,由 `idi-10-01` … `idi-10-03` 落地):** `frontend/style.css` 已定型(表格 + 圆角两处改动都已落地),`grep -cF -- '--radius-lg' frontend/style.css` 输出 `0`,且 `.venv/bin/python scripts/check-10-idi10-validation.py --item t1 --item t2 --item r1 --item r2` 全绿。

**本计划不触碰:** 任何产品代码(`frontend/`)、任何门代码(`scripts/`)、任何被测样本、以及 `.planning/` 下除 `idi-09-VERIFICATION.md` 与本阶段 `gate-logs/` 之外的任何文件(尤其**不得**改动其余 9 份报告)。
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
@.planning/phases/idi-10-tables-and-radius-scale/idi-10-02-SUMMARY.md
@.planning/phases/idi-10-tables-and-radius-scale/idi-10-03-SUMMARY.md
@.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md
</context>

## Artifacts this phase produces

> 本节的用途:**plan-review-convergence 的 source-grounding pass 读它,把本阶段新建的符号从漂移校验里排除**。
> 本节列出**全阶段**(四个计划)的产出;本计划只登记自己那部分。

**本计划写入的文件:**

| # | 路径 | 动作 | 备注 |
|---|---|---|---|
| 1 | `.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md` | **就地改写**(frontmatter 重签 + 正文新增一节 + 24 条 must-have 逐条复核结论) | 本阶段**唯一**允许改动的既有报告 |
| 2 | `.planning/phases/idi-10-tables-and-radius-scale/gate-logs/verification-recheck.log` | **新增** | 10 份报告的分诊原始输出(`verification.status` + `verification.fingerprint`)+ 逐份缺失项数实测 |

**本计划明确不产生的新符号:** 零新增代码文件、零新增令牌、零新增依赖;其余 9 份报告零字节改动;`frontend/` 与 `scripts/` 下全部文件零字节改动。

## 10 份报告的清单与逐份预期(规划期实测,执行器须逐份复跑并抄录原始输出)

| # | 报告 | 预期 `verification.status` | 预期 `verification.fingerprint` |
|---|---|---|---|
| 1 | `.planning/milestones/v1.13-phases/idi-01-1-2/01-VERIFICATION.md` | `stale` | 失败关闭 |
| 2 | `.planning/milestones/v1.13-phases/idi-02-g2/02-VERIFICATION.md` | `stale` | 失败关闭 |
| 3 | `.planning/milestones/v1.13-phases/idi-03-g3/03-VERIFICATION.md` | `stale` | 失败关闭 |
| 4 | `.planning/milestones/v1.14-phases/idi-04-tokens-contract/idi-04-VERIFICATION.md` | `stale` | 失败关闭 |
| 5 | `.planning/milestones/v1.14-phases/idi-04.1-radix/idi-04.1-VERIFICATION.md` | `stale` | 失败关闭 |
| 6 | `.planning/milestones/v1.14-phases/idi-05-typography-and-visual-hierarchy/idi-05-VERIFICATION.md` | `stale` | 失败关闭 |
| 7 | `.planning/milestones/v1.14-phases/idi-06-layout-robustness/idi-06-VERIFICATION.md` | `stale` | 失败关闭 |
| 8 | `.planning/milestones/v1.14-phases/idi-07-interaction-states-and-focus/idi-07-VERIFICATION.md` | `stale` | 失败关闭 |
| 9 | `.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md` | 重验前 `stale` / **重验后 `passed`** | **成功**,返回 `v1:sha256:…` |
| 10 | `.planning/quick/260925-iin-v1-14-ai-999-1/260925-iin-VERIFICATION.md` | `stale` | 失败关闭 |

**`idi-08` 不在上表**。它的报告在 `.planning/milestones/v1.14-phases/idi-08-accessibility-semantics-and-keyboard/idi-08-VERIFICATION.md`,其 `covered_files` 列的是 `frontend/app.js` / `frontend/index.html` / `scripts/check-05-ui-uat.py` / `scripts/check-07-idi08-validation.py` —— **不含** `frontend/style.css`。它正文里多次提及该文件,所以**全文 grep 会把它误算进来**。这正是「判据必须锚 frontmatter 的 `covered_files` 逐行匹配、不是全文 grep」这句话的**探测器**,本计划要给出两个并排的计数作为证据:frontmatter 段内 `^  - frontend/style.css$` 命中 **0**;全文 `frontend/style.css` 命中 **非 0**。

<tasks>

<task type="auto" tdd="false">
  <name>Task 1: 连带指纹的「10 份覆盖 / 1 份可执行」分诊 —— 逐份实测证据</name>
  <files>.planning/phases/idi-10-tables-and-radius-scale/gate-logs/</files>
  <precondition>`frontend/style.css` 的表格与圆角两处改动均已落地(`grep -cF -- '--radius-lg' frontend/style.css` 输出 `0`)</precondition>
  <reversibility rating="reversible">本任务只跑只读查询与写日志,不产生任何状态改动;失败只暴露问题、不引入问题。</reversibility>
  <read_first>
    - `.planning/phases/idi-10-tables-and-radius-scale/10-CONTEXT.md` §「连带指纹:实测「10 份覆盖,1 份可执行」」整节 —— 含 10 份报告的表格、逐份缺失数、以及 STATE.md 于 2026-09-14 登记的已知限制原文
    - `.planning/phases/idi-10-tables-and-radius-scale/idi-10-PATTERNS.md` 文末的裁定块(orchestrator 的裁定:只重验 `idi-09` 一份;配套硬约束是不得改 `scripts/check-05-ui-uat.py`)
    - `.planning/STATE.md` 的 `## Deferred Items` 里那条 `known-limitation` 行(「归档后的报告不再被 staleness 机制消费,故记为已知限制而非回填重算」)
    - `.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md` 的 **frontmatter**(`covered_files` 的 10 条、`covered_digest`、`status`、`re_verification:` 块)—— 本任务的对照物
    - `.planning/milestones/v1.14-phases/idi-08-accessibility-semantics-and-keyboard/idi-08-VERIFICATION.md` 的 **frontmatter** —— 用于证明它不在覆盖名单内(它的 `covered_files` 列的是 `frontend/app.js` / `frontend/index.html` / `scripts/check-05-ui-uat.py` / `scripts/check-07-idi08-validation.py`,**不含** `frontend/style.css`;但它正文里多次提及该文件 ⇒ 它是「全文 grep 会误报」的那个假阳性)
    - `.planning/ROADMAP.md` §`### Phase 10:` 的 Deliverables 第 5 条与 Pitfalls 最后一条(「10 vs 1」的双向错误与两条判据)
  </read_first>
  <action>
    **第 1 步 —— 用「锚 frontmatter 逐行匹配」的方式枚举覆盖面。**

    遍历 `.planning/phases/`、`.planning/milestones/*-phases/`、`.planning/quick/` 下所有 `*-VERIFICATION.md`,对每一份取它的 frontmatter(**只取两行 `---` 之间的部分**,不是全文),判定两条:该报告 `status:` 是否为 `passed`;其 `covered_files:` 列表里是否有**恰好**一行匹配 `  - frontend/style.css`。

    记录命中清单,核对是否恰为上表 10 份。**另须给出一条独立证据**证明 `idi-08` 不在名单内(例如在 `idi-08-VERIFICATION.md` 的 frontmatter 段里 grep `frontend/style.css` 的命中数为 `0`)。这条证据的意义是证明本判据**没有**被全文 grep 的假阳性污染 —— 用全文 grep 会把 `idi-08` 算进来,那是错的。

    **第 2 步 —— 逐份跑 `verification.status`。**

    对上表 10 份,逐份跑 `node .claude/gsd-core/bin/gsd-tools.cjs query verification.status <该报告的 phase 目录>`,把**原始 JSON** 抄进 SUMMARY 与 `gate-logs/verification-recheck.log`。目录取值:报告所在的那一级(例如 `idi-04` 那份是 `.planning/milestones/v1.14-phases/idi-04-tokens-contract`,quick 那份是 `.planning/quick/260925-iin-v1-14-ai-999-1`)。

    核对:9 份归档 / quick 报告返回 `"status": "stale"`;`idi-09` 在本阶段的有序性下**也应返回 `"stale"`**(因为 `frontend/style.css` 确实变了)—— 这是「重验确实是必要的」这一点的机器证据,必须抄录下来。若某一份返回了与预期不同的状态,逐份查明成因并记入 SUMMARY。

    **第 3 步 —— 逐份跑 `verification.fingerprint`,把失败关闭与成功分别取证。**

    对上表 10 份,逐份跑 `node .claude/gsd-core/bin/gsd-tools.cjs query verification.fingerprint <该报告的 phase 目录> <它 frontmatter 里列出的 covered_files,逐条照抄>`,把原始输出抄进 `gate-logs/verification-recheck.log` 与 SUMMARY。

    核对:9 份以 `Error: could not compute fingerprint — a covered file is missing, unreadable, or escapes the project root` 失败关闭;`idi-09` **成功**,返回一个 `covered_digest`(形如 `v1:sha256:<64 位十六进制>`)。

    ⚠ **注意 `idi-09` 这一步返回的摘要是「HEAD 状态下的新摘要」**,与它 frontmatter 里现存的 `covered_digest` 应当**不同**(因为 `frontend/style.css` 变了)。把两个值并排贴出来 —— 这就是「内容确实变了、所以必须重新验证而不是刷新」的直接证据。

    **第 4 步 —— 逐份实测「缺失项数 / 总项数」。**

    对 9 份失败关闭的报告,逐份实测:它 frontmatter 里列出的 `covered_files` 共几条、其中路径在盘上能解析的有几条。把「缺失数 / 总数」逐份记账(不沿用任何未经本次复现的数字 —— 10-CONTEXT 里给出的那组数字是规划期读数,本步骤以本机实跑为准;若与 10-CONTEXT 不同,记下差异并说明成因)。

    同时确认**成因**是路径而非内容:抽查至少两份,核对某一缺失路径的原位置(`.planning/phases/<id>/…`)与它的归档位置(`.planning/milestones/<ver>-phases/<id>/…`)确实一一对应。

    **第 5 步 —— 把结论写进 SUMMARY,并明确「为什么本阶段只重验 1 份」。**

    SUMMARY 必须含:(a) 覆盖面判据的定义(锚 frontmatter 逐行匹配,非全文 grep)与 `idi-08` 不在名单的独立证据;(b) 10 份的逐份原始 `verification.status` 与 `verification.fingerprint` 输出;(c) 9 份的逐份「缺失数 / 总项数」与成因;(d) 引用 STATE.md 的 2026-09-14 已知限制原文;(e) 明确写出「其余 9 份的重验须先修复归档路径引用,是另一件已登记的 backlog 事项,不在本阶段边界内」;(f) 引用 Phase 9 的先例 —— 它改同一文件时也只在 live 树内重验了 `idi-09` 一份。

    **第 6 步 —— 不触碰任何文件。** 本任务只跑只读查询与写日志 / SUMMARY。特别地:不得改动其余 9 份报告的任何字节;不得改动 `scripts/check-05-ui-uat.py`。
  </action>
  <verify>
    <automated>node .claude/gsd-core/bin/gsd-tools.cjs query verification.status .planning/phases/idi-09-card-containers</automated>
    <fails_when>the emitted JSON's "status" field is not "stale" (at this point frontend/style.css has changed, so idi-09 MUST be stale — a "passed" here would mean the change never landed or the digest was refreshed without re-verifying)</fails_when>
    <automated>node .claude/gsd-core/bin/gsd-tools.cjs query verification.fingerprint .planning/milestones/v1.14-phases/idi-04-tokens-contract frontend/style.css .planning/phases/idi-04-tokens-contract/idi-04-01-PLAN.md</automated>
    <fails_when>the command does not fail closed with "could not compute fingerprint" (a successful digest for an archived report would mean the archived covered paths actually resolve, contradicting the ruling)</fails_when>
    <automated>node .claude/gsd-core/bin/gsd-tools.cjs query verification.fingerprint .planning/phases/idi-09-card-containers .planning/phases/idi-09-card-containers/idi-09-01-PLAN.md .planning/phases/idi-09-card-containers/idi-09-01-SUMMARY.md .planning/phases/idi-09-card-containers/idi-09-02-PLAN.md .planning/phases/idi-09-card-containers/idi-09-02-SUMMARY.md .planning/phases/idi-09-card-containers/idi-09-03-PLAN.md .planning/phases/idi-09-card-containers/idi-09-03-SUMMARY.md frontend/style.css scripts/check-05-ui-uat.py scripts/check-09-idi09-validation.py scripts/probe-card-border-token.py</automated>
    <fails_when>the command errors instead of emitting a JSON object with a "covered_digest" string, or the emitted "covered_digest" equals the value currently stored in idi-09-VERIFICATION.md's frontmatter (equal would mean frontend/style.css did not actually change and the re-verification is unnecessary)</fails_when>
    <automated>awk '/^---$/{n++} n==1' .planning/milestones/v1.14-phases/idi-08-accessibility-semantics-and-keyboard/idi-08-VERIFICATION.md | grep -c '^  - frontend/style.css$'</automated>
    <fails_when>the printed count is not exactly "0" (a non-zero count would put idi-08 into the covered set and break the "which report covers style.css" criterion; the file must exist — a missing file makes awk print nothing and the count 0 for the wrong reason, so also confirm the report file is on disk)</fails_when>
    <automated>grep -c 'frontend/style.css' .planning/milestones/v1.14-phases/idi-08-accessibility-semantics-and-keyboard/idi-08-VERIFICATION.md</automated>
    <fails_when>the printed count is "0" (this full-text count is expected to be large — it is the recorded proof that full-text grep would be a FALSE POSITIVE, which is exactly why the coverage criterion must anchor on frontmatter covered_files lines instead)</fails_when>
    <automated>git diff -- scripts/check-05-ui-uat.py</automated>
    <fails_when>output is not empty (any diff to check-05-ui-uat.py would enlarge the re-verification set from 1 to 2)</fails_when>
    <automated>ls .planning/phases/idi-10-tables-and-radius-scale/gate-logs/verification-recheck.log</automated>
    <fails_when>the file does not exist</fails_when>
  </verify>
  <acceptance_criteria>
    - `gate-logs/verification-recheck.log` 存在,含 10 份报告各自的 `verification.status` 原始 JSON 与 `verification.fingerprint` 原始输出(成功或失败关闭的完整报错原文)。
    - 覆盖面判据在 SUMMARY 里被明确定义为「锚 frontmatter 的 `covered_files` 逐行匹配 `  - frontend/style.css` 且 `status: passed`」,并给出 `idi-08` 的两条并排计数作为独立证据:其 frontmatter 段内命中 **0**、其全文命中 **非 0**(后者证明全文 grep 会误报,故判据不能锚全文)。
    - 覆盖名单恰为上表 10 份,逐份路径与 SUMMARY 里的清单一致;无第 11 份、无遗漏。
    - 9 份归档 / quick 报告的 `verification.status` 为 `"stale"`,且其 `verification.fingerprint` 以 `could not compute fingerprint` 失败关闭;逐份「缺失数 / 总项数」在 SUMMARY 里实测记账,并核实成因是路径(原 `.planning/phases/<id>/…` → 归档 `.planning/milestones/<ver>-phases/<id>/…`),抽查 ≥ 2 份。
    - `idi-09` 在本任务时点的 `verification.status` 为 `"stale"`,且其 `verification.fingerprint` **成功**并返回一个与它 frontmatter 现存 `covered_digest` **不同**的新摘要;两个值并排贴进 SUMMARY。
    - SUMMARY 里引用 STATE.md 于 2026-09-14 登记的已知限制原文,并明确写出「其余 9 份的重验须先修复归档路径引用,是另一件已登记的 backlog 事项,不在本阶段边界内」,以及 Phase 9 只重验 1 份的先例。
    - `git diff -- scripts/check-05-ui-uat.py` 为空;其余 9 份报告零字节改动(`git status --porcelain .planning/milestones/ .planning/quick/` 为空)。
    - 本任务没有编辑任何报告文件(只写日志与 SUMMARY)。
  </acceptance_criteria>
  <done>连带指纹的真实形状以逐份实测证据落定:覆盖 10 份、可执行 1 份;9 份的 stale 成因(归档后路径不可解析 ⇒ fail-closed)逐份取证并引用 STATE.md 的已知限制;`idi-09` 的 stale 状态与「新旧摘要不同」一并留证,为下一任务的重验提供依据。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 2: `idi-09-VERIFICATION.md` 以 HEAD 内容重新验证(不是刷新指纹)</name>
  <files>.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md</files>
  <precondition>Task 1 已完成;`.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md` 的 `covered_files` 10 条全部在盘(`verification.fingerprint` 能成功)</precondition>
  <reversibility rating="costly">报告的重签与它所登记的产品事实成对:只回退报告不回退 `frontend/style.css`,会让重签的摘要立刻 stale;只回退产品不回退报告,则报告断言的是一个不存在的状态。两处必须成对处置,且回退后须重算摘要,故评级 costly 而非 reversible。</reversibility>
  <read_first>
    - `.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md` **全文** —— 它的 frontmatter(10 条 `covered_files`、`covered_digest`、`status`、`score`、`behavior_unverified`、`overrides_applied`、`re_verification:` 块)与正文(24 条 must-have 的逐条判据、`## Why this is a re-verification, and what changed` 那一节的**模板形态**、以及它引用的每条门命令与读数)
    - `.planning/phases/idi-09-card-containers/idi-10-01-SUMMARY.md` / `idi-10-02-SUMMARY.md` / `idi-10-03-SUMMARY.md` —— 本阶段改了什么、复跑了哪些门、各自的原始读数
    - `.planning/phases/idi-10-tables-and-radius-scale/gate-logs/` —— 本阶段的逐门原始 stdout(重验可直接引用这些已落盘的证据)
    - `scripts/check-09-idi09-validation.py` —— 该报告的核心运行时证据来源(c1…c5 + `--screenshot`),重验时要重跑它
    - `frontend/style.css` —— 本阶段改动后的 `.markdown-body table` / `th, td` / `.chat-user` / `#chat-input-row input` 四处,确认它们与 `idi-09` 断言的卡片容器语言**不相交**
    - `.planning/ROADMAP.md` §`### Phase 10:` 的 Deliverables 第 5 条(「以 HEAD 内容重新验证(不是刷新指纹 —— 内容确实变了)」)
  </read_first>
  <action>
    **第 1 步 —— 重跑该报告的判据。**

    该报告的核心运行时证据是 `scripts/check-09-idi09-validation.py` 的 `c1` … `c5` 与 `--screenshot`。逐条重跑并记录原始输出:
    - `.venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2 --item c3 --item c4 --item c5`,把 `=== 逐项结论 ===` 块与末行 `exit=` 抄进 SUMMARY(期望 `exit=0`、各项 0 FAIL / 0 BLOCKED);
    - 该报告引用的其它门命令(四个静态门、`check-05` 的相关 item、`check-06` g6 的两条 `box-shadow 恒 none` 对照组、`probe-card-border-token.py`)若已在 `idi-10-03` 的 `gate-logs/` 里有本阶段的新鲜输出,直接引用;缺失的补跑。

    **第 2 步 —— 逐条复核 24 条 must-have。**

    把该报告正文里列出的 24 条 must-have **逐条**以 HEAD 内容重新推导,每条给出:判据、本次实测读数或引用来源、结论(成立 / 不成立)。预期 **24/24 仍成立**,理由:本阶段不改任何卡片容器的 `background` / `border` / `border-radius` / `box-shadow` 令牌,也不改 `--radius-md`(它被 `check-09` 动态解析),表格规则的改动落在 `.markdown-body` 内部、与五个卡片容器不相交。

    若任何一条**不再成立**:它进 `gaps_remaining` 或 `regressions`,并作为**未关闭项**报回。**不得**通过改写判据让它成立、不得跳过、不得删除。

    **第 3 步 —— 重新计算 `covered_digest`。**

    跑 Task 1 第 3 步里给出的 `verification.fingerprint` 命令(phase 目录 + 该报告 frontmatter 的 10 条 `covered_files`),取回新的 `v1:sha256:…` 值。

    `covered_files` 的 10 条**逐条未变**(逐条照抄进新 frontmatter,顺序也保持一致)。只更新 `covered_digest`。

    **第 4 步 —— 重签 frontmatter。**

    - `verified`: 改为本次重验的时间戳(ISO-8601 UTC,与格式一致);
    - `status`: `passed`(若第 2 步出现不成立的 must-have,则按实际结论取相应状态,并在 SUMMARY 里说明);
    - `score`: `24/24 must-haves verified`(若第 2 步的结论不同则按实际写);
    - `covered_digest`: 第 3 步计算出的新值;
    - `covered_files`: 10 条逐条未变;
    - `behavior_unverified` / `overrides_applied` / `human_verification`: 保持原义(本阶段不改这些语义);
    - `re_verification:`: 更新为
      ```
      re_verification:
        previous_status: passed
        previous_score: 24/24
        gaps_closed: []
        gaps_remaining: []
        regressions: []
      ```
      (三个列表预期为空;若非空,每一项都要在正文与 SUMMARY 里逐条说明)

    **第 5 步 —— 正文新增 / 改写「Why this is a re-verification, and what changed」一节。**

    该报告已有一节同名内容(记录 2026-09-26 那次用户裁定的修正案)。本步骤要**在同一节里追加本阶段这一段**(或新开一节并在标题里写明 Phase 10),内容须含:

    - **点名**本阶段改动的 `covered_file`:`frontend/style.css`(10 条 `covered_files` 里**唯一**被本阶段改动的);
    - **改了什么**,逐条:表格规则就地改写(`.markdown-body th, .markdown-body td` 的 `border` → `border: none` + `border-bottom: 1px solid var(--color-border-subtle)`;新增 `.markdown-body th { background: var(--color-surface); }`);圆角刻度收敛为 `8 / 10 / 999` 三档(`--radius-lg` 删除,`.chat-user` → `--radius-md`,`#chat-input-row input` → `--radius-pill`);
    - **为什么不触及本报告的 must-have**:这四处改动与五个卡片容器的语言不相交,`--radius-md` 被本阶段**保留**(它是 `check-09` 动态解析的对象);
    - **本次重跑的门与读数**(引用 SUMMARY / `gate-logs/` 的原始输出,不重抄散文);
    - 一句明确的**性质声明**:这是**以 HEAD 内容重新验证**,不是刷新指纹 —— 覆盖输入确实变了,刷新等于断言「自验证以来覆盖输入无变化」,那是不实陈述。

    该节里出现的每一个数字都必须来自本次实跑或 `idi-10-03` 的 `gate-logs/`,**不得**沿用未经复现的历史读数。

    **第 6 步 —— 收口核对。**

    跑 `node .claude/gsd-core/bin/gsd-tools.cjs query verification.status .planning/phases/idi-09-card-containers`,必须返回 `"status": "passed"`。这是「重签的摘要与 HEAD 相符」的机器判据。

    **第 7 步 —— 只改这一个文件。** 不得改动其余 9 份报告、不得改动 `scripts/` 下任何文件、不得改动 `frontend/` 下任何文件、不得改动任何被测样本。
  </action>
  <verify>
    <automated>node .claude/gsd-core/bin/gsd-tools.cjs query verification.status .planning/phases/idi-09-card-containers</automated>
    <fails_when>the emitted JSON's "status" field is not "passed" (a "stale" means the re-signed covered_digest does not match HEAD, i.e. the recomputation or the frontmatter write is wrong)</fails_when>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2 --item c3 --item c4 --item c5</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or any non-zero BLOCKED count in the "=== 逐项结论 ===" block, or the trailing "exit=" line not "exit=0"</fails_when>
    <automated>awk '/^---$/{n++} n==1' .planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md | grep -c '^  - frontend/style.css$'</automated>
    <fails_when>the count is not exactly "1" (the covered_files list must still name frontend/style.css exactly once)</fails_when>
    <automated>awk '/^---$/{n++} n==1' .planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md | grep -c '^  - '</automated>
    <fails_when>the count is not exactly "10" (the covered_files list must still have all ten entries — dropping any is how a report is made to look fresh without re-verifying)</fails_when>
    <automated>node .claude/gsd-core/bin/gsd-tools.cjs query verification.fingerprint .planning/phases/idi-09-card-containers .planning/phases/idi-09-card-containers/idi-09-01-PLAN.md .planning/phases/idi-09-card-containers/idi-09-01-SUMMARY.md .planning/phases/idi-09-card-containers/idi-09-02-PLAN.md .planning/phases/idi-09-card-containers/idi-09-02-SUMMARY.md .planning/phases/idi-09-card-containers/idi-09-03-PLAN.md .planning/phases/idi-09-card-containers/idi-09-03-SUMMARY.md frontend/style.css scripts/check-05-ui-uat.py scripts/check-09-idi09-validation.py scripts/probe-card-border-token.py</automated>
    <fails_when>the emitted "covered_digest" does not equal the value now stored in the report's frontmatter (a mismatch means the frontmatter was not re-signed with the recomputed digest)</fails_when>
    <automated>git diff --stat .planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md</automated>
    <fails_when>the diff stat is empty (the report must have been rewritten) or it names more than that one file</fails_when>
    <automated>git status --porcelain .planning/milestones/ .planning/quick/ frontend/ scripts/</automated>
    <fails_when>output contains any path other than the frontend/style.css and scripts/check-10-idi10-validation.py changes already landed by earlier plans (the 9 archived reports, product code and gate code must be untouched by this plan)</fails_when>
  </verify>
  <acceptance_criteria>
    - `node .claude/gsd-core/bin/gsd-tools.cjs query verification.status .planning/phases/idi-09-card-containers` 返回 `"status": "passed"`。
    - `idi-09-VERIFICATION.md` 的 frontmatter `covered_files` 仍是**恰好 10 条**,其中 `  - frontend/style.css` 恰 1 条(条目与顺序逐条未变)。
    - 该报告 frontmatter 的 `covered_digest` 与 `verification.fingerprint` 本次计算出的值**逐字符相同**,且与 Task 1 记录的旧值**不同**。
    - `status` 为 `passed`;`score` 为 `24/24 must-haves verified`(或第 2 步实际结论);`verified` 为本阶段的时间戳。
    - `re_verification:` 块含 `previous_status: passed`、`previous_score: 24/24` 与 `gaps_closed` / `gaps_remaining` / `regressions` 三个列表;若非空,每一项在正文与 SUMMARY 里逐条说明。
    - 正文含一节「Why this is a re-verification, and what changed」,**点名 `frontend/style.css`** 为唯一被本阶段改动的 `covered_file`,并说明改了什么(表格规则 + 圆角收敛)、为什么不触及本报告的 must-have(容器语言不相交、`--radius-md` 被保留)、以及这是重新验证而非刷新指纹的性质声明。
    - SUMMARY 里**逐条**给出 24 条 must-have 的复核结论(判据 / 本次读数或引用来源 / 成立与否)。
    - `.venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2 --item c3 --item c4 --item c5` 全绿、`exit=0`、0 BLOCKED。
    - 本次只改动 `idi-09-VERIFICATION.md` 一个既有文件;其余 9 份报告、`frontend/`、`scripts/` 在本任务内零改动。
  </acceptance_criteria>
  <done>`idi-09-VERIFICATION.md` 以 HEAD 内容重新验证完成:24 条 must-have 逐条复核、`covered_files` 10 条未变、`covered_digest` 重算为新值、frontmatter 重签为 `passed` / `24/24`、`re_verification:` 块与正文「Why this is a re-verification」一节点名 `frontend/style.css` 并说明改动;`verification.status` 由 `stale` 回到 `passed`。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 无外部输入边界 | 本计划只跑**只读**的本地查询(`gsd-tools query verification.*`)、重跑既有本地门脚本、并改写**一个** Markdown 报告:零用户输入处理、零鉴权、零数据访问、零网络调用、零产品代码改动 |
| 证据边界(报告与它断言的事实之间) | 重签报告是**记录**动作,不是**证明**动作。报告里写的每个数字都必须有可追溯到本次实跑或 `gate-logs/` 的来源;把未复现的历史读数抄进去、或只改摘要不重跑判据,都会让报告变成不实陈述 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-10-01 | Repudiation | `idi-09-VERIFICATION.md` 的重新验证 | **high** | mitigate | 本计划唯一的真实风险是「**刷新指纹冒充重新验证**」:只改 `covered_digest` 而不重跑判据,等于断言「自验证以来覆盖输入无变化」——那是不实陈述。缓解:(a) 正文必须新增一节**点名**被改动的 `covered_file` 与改动内容;(b) `<verify>` 强制重跑 `check-09 --item c1…c5` 并要求 `exit=0`、0 BLOCKED;(c) 24 条 must-have 逐条以 HEAD 内容复核,结论写进 SUMMARY,不成立者进 `gaps_remaining` / `regressions`;(d) `covered_files` 的 10 条必须逐条未变(条数判据 == 10),删条目是让报告假装新鲜的典型手法;(e) 旧的 `covered_digest` 与新算出的值并排留证,证明内容确实变了 |
| T-idi-10-02 | Tampering | 连带指纹重验面的范围 | **high** | mitigate | 若误改 `scripts/check-05-ui-uat.py`(它在 `idi-08` 的 `covered_files` 里),重验面会从 1 份变成 2 份,而 `idi-08` 的报告并不覆盖 `frontend/style.css` —— 那会凭空制造一份债务。缓解:`<prohibitions>` 逐条列出该禁令;`<verify>` 要求 `git diff -- scripts/check-05-ui-uat.py` 为空;并给出 `idi-08` 的 `covered_files` 里对 `frontend/style.css` 命中数为 0 的独立证据 |
| T-idi-10-03 | Tampering | 其余 9 份报告 | medium | mitigate | 它们的 stale 成因是归档后路径不可解析,不是内容变化;就地改它们会掩盖真正的成因(路径引用未修),并可能与未来的归档路径修复冲突。缓解:`<prohibitions>` 明令只写 `idi-09-VERIFICATION.md`;`<verify>` 要求 `git status --porcelain .planning/milestones/ .planning/quick/` 输出里不含这 9 份 |
| T-idi-10-04 | Information Disclosure | 报告与日志内容 | low | accept | 报告与日志只含令牌值、几何读数与本地路径,均来自公开的样式表与本地 fixture;无用户数据、无凭据、无网络内容 |
| T-idi-10-05 | Elevation of Privilege | 无 | low | accept | 本计划不触碰鉴权、权限门、服务端路径或任何 API |
| T-idi-10-SC | Tampering | npm / pip / cargo 安装 | low | accept | 本阶段**零安装**:零新增依赖、零构建步骤(DESIGN.md D-06);`gsd-tools.cjs` 与 Playwright 均已在仓库内 / 项目 `.venv` 中。`frontend/vendor/` 仍只有 `marked.min.js` |
</threat_model>

<verification>
**分诊证据(只读查询,逐份):**

- `node .claude/gsd-core/bin/gsd-tools.cjs query verification.status <phase dir>` × 10 —— 9 份 `stale`、`idi-09` 重验前 `stale` 重验后 `passed`
- `node .claude/gsd-core/bin/gsd-tools.cjs query verification.fingerprint <phase dir> <covered files…>` × 10 —— 9 份失败关闭、`idi-09` 成功
- `idi-08` 的 frontmatter 对 `frontend/style.css` 命中数 == 0(证明判据锚对了)

**重验的判据重跑:**

- `.venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2 --item c3 --item c4 --item c5` → `exit=0`,0 FAIL / 0 BLOCKED
- 该报告引用的其它门命令引用 `idi-10-03` 的 `gate-logs/` 新鲜输出(缺失的补跑)

**重签的机器判据:**

- `node .claude/gsd-core/bin/gsd-tools.cjs query verification.status .planning/phases/idi-09-card-containers` → `"status": "passed"`
- 该报告 frontmatter 的 `covered_files` 条数 == 10、其中 `frontend/style.css` == 1
- frontmatter 的 `covered_digest` == 本次 `verification.fingerprint` 的值,且 ≠ Task 1 记录的旧值

**不得越界:**

- `git diff -- scripts/check-05-ui-uat.py` 为空
- `git status --porcelain .planning/milestones/ .planning/quick/` 为空(9 份归档 / quick 报告零改动)
- `frontend/` 与 `scripts/` 在本计划内零改动
</verification>

<success_criteria>
- 连带指纹的真实形状以逐份实测证据落定:覆盖 `frontend/style.css` 的 `passed` 报告恰 **10 份**,其中路径可解析的恰 **1 份**(`idi-09`);`idi-08` 不在名单内且有独立证据。
- 9 份归档 / quick 报告的 stale 成因(归档后 `covered_files` 路径不可解析 ⇒ `verification.fingerprint` 失败关闭)逐份取证,并引用 STATE.md 于 2026-09-14 登记的已知限制;它们被明确排除在本阶段边界之外,理由与依据都写在 SUMMARY 里。
- 本阶段**只**重新验证 `idi-09` 一份,且是「以 HEAD 内容重新验证」:24 条 must-have 逐条复核、重跑了它引用的门、正文点名 `frontend/style.css` 的改动、`covered_digest` 重算。
- `idi-09-VERIFICATION.md` 的 `covered_files` 10 条逐条未变;`status: passed`;`score: 24/24 must-haves verified`;`re_verification:` 块记录 `previous_status` / `previous_score` 与三个列表;`verification.status` 由 `stale` 回到 `passed`。
- 未被静默放宽或删除任何 must-have;未改动其余 9 份报告、`frontend/` 或 `scripts/` 下任何文件;`scripts/check-05-ui-uat.py` 零改动。
- 读者拿到 SUMMARY + `gate-logs/verification-recheck.log` 后,能独立复现「10 份覆盖 / 1 份可执行」这一结论的每一步。
</success_criteria>

<output>
Create `.planning/phases/idi-10-tables-and-radius-scale/idi-10-04-SUMMARY.md` when done
</output>

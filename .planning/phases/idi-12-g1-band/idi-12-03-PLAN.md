---
phase: idi-12-g1-band
plan: 03
type: execute
wave: 3
depends_on:
  - idi-12-01
  - idi-12-02
files_modified:
  - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-01-token-conformance.log
  - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-02-contrast.log
  - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-03-hidden-uniqueness.log
  - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-04-important-count.log
  - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-05-ui-uat.log
  - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-06-idi05-validation.log
  - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-07-idi08-validation.log
  - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-09-idi09-validation.log
  - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-10-idi10-validation.log
  - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/probe-05-resolve-color.log
  - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/probe-07-focus-composite.log
  - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/pytest.log
  - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/node-check-app-js.log
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md
autonomous: true
requirements:
  - REG-04

estimate:
  tokens: 65000
  raw_tokens: 65000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- 复跑零新增失败(ROADMAP SC3) ----
    - "五条浏览器门(`check-05` / `check-06` / `check-07` / `check-09` / `check-10`)在**最终态**上复跑,各自的 `^FAIL` 行数**均为 0**(判据取**行首** verdict 形态 `^FAIL`,**不是**子串搜索 —— 后者会命中 `check-05` 第 399 行那条标签里带 FAIL 一词的 PASS 行,在本项目恒非空、无法通过)。原始输出与退出码**逐门落盘** `.planning/phases/idi-12-g1-band/gate-logs/idi-12-03/<gate>.log`"
    - "`check-05` 走 `.venv/bin/python` 且**必须** `--browser bundled`(该机 `channel=\"chrome\"` + headless 会 CDP 挂死);全量 `exit=2` 的成因集合**仍只是 item 5 的两条 `--ai-smoke` 腿按设计 BLOCKED**(`item 5:` 汇总行的 BLOCKED 计数 == 2),不是回归"
    - "两个探针 `scripts/probe-05-resolve-color.py` / `scripts/probe-07-focus-composite.py` 复跑退出码仍为 `0`。**probe-05 输出里的 `BLOCKED [mutated] … post-fix` 是它自己的对照支,不是门失败**(该探针在同一份被变异的样式表上跑同一条断言两次,「修复前 PASS / 修复后 BLOCKED」正是它要证明的对照)"
    - "`check-09 --item c1,c2,c3,c4,c5,c6` 全 PASS、0 FAIL、0 BLOCKED、`exit=0` —— 与 Phase 11 改写后的契约一致(`c1..c5` 逐项断言计数与 Phase 11 收口读数一致,`c6` 是 Phase 12 新增)"
    # ---- 四个静态门 + pytest 基线(ROADMAP SC3) ----
    - "四个静态门全 PASS:`check-01`(围栏外零裸 `#hex`、零 tier-1 原语引用)、`check-02`(`PASS: 0 failures`;PAIR 条目数 **53**、`ORDER` 读数 **0.363**、`TEXT_MIN` / `NON_TEXT_MIN` 与 HEAD **逐字节相同**)、`check-03`(`^\\.hidden {` == 1)、`check-04`(`!important;` **声明**数 == 1)"
    - "pytest 基线不降:`.venv/bin/python -m pytest backend/tests -q --tb=short` 报 **219 passed / 6 skipped**。**必须用项目 `.venv`** —— 环境 `python3` 是 miniconda,会让 4 个 `ai_caller` 测试假失败"
    - "`node --check frontend/app.js` 通过;`git status --porcelain frontend/` 仅预期文件;`frontend/vendor/` 仍只有 `marked.min.js`"
    # ---- 连带指纹的实测形状与逐份处置(ROADMAP SC4) ----
    - "连带指纹面**磁盘实测**,判据锚报告 frontmatter 的 `covered_files` **逐行匹配**(**不是**全文 grep —— 全文 grep 会把只在正文提及的报告算进来),并**额外测每条声明的路径是否仍在盘**。筛选面 = 本次全部改动文件(`frontend/style.css` + `scripts/check-09-idi09-validation.py` + `scripts/ui-states/checking/docs/DESIGN-check-2.md`)"
    - "实测形状:**12 份**报告命中。**11 份归档报告**(v1.13 的 `01` / `02` / `03`,v1.14 的 `idi-04` / `idi-04.1` / `idi-05` / `idi-06` / `idi-07`,v1.15 的 `idi-09` / `idi-10`,quick 的 `260925-iin`)的 `covered_files` 里有 **2–13 条路径已不在盘**(`.planning/phases/...` 已移到 `.planning/milestones/v1XX-phases/...`)⇒ **fail-closed stale,属 2026-09-14 登记的已知限制**;处置 = **登记为已知限制并在 SUMMARY 里逐份列名,不重验、不修复归档路径**(「修归档」超出 G1-01 / REG-04 的范围)"
    - "**1 份在盘**:`.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md`(`status: passed`、12/12 must-haves、`covered_files` **16 条零缺失**)。它以 `covered_files` 同时覆盖 `frontend/style.css` 与 `scripts/check-09-idi09-validation.py` ⇒ 本次改动**必然作废它**"
    - "该份在盘报告**以 HEAD 内容重新验证,不是刷新指纹**:重跑它引用的判据(`check-09 --item c1,c2,c3,c4,c5`、五条浏览器门、四静态门),在报告里写入 `re_verification` 段(触发原因、上一 / 当前 `covered_digest`、逐文件变更归因、重跑的检查与其读数),并更新 `covered_digest` 与 `verified` 时间戳。**只重算 digest 而不重跑判据等于断言「自验证以来覆盖输入无变化」,而那为假**"
    - "**两份实测的零涟漪结论**(规划期已核,执行器须复核):①把 `check-09` 纳入筛选面**不新增任何报告**(`idi-09` 与 `idi-11` 已覆盖它);②`scripts/ui-states/checking/docs/DESIGN-check-2.md` **不被任何报告覆盖**(对全部 `*VERIFICATION.md` / `*VALIDATION.md` 的 `covered_files` 逐行匹配零命中)⇒ 改它不新增连带覆盖者"
    # ---- 边界 ----
    - "`scripts/check-05-ui-uat.py` / `check-06` / `check-07` / `check-10` / `check-02-contrast.py` / `check-01` / `check-03` / `check-04` / `probe-05` / `probe-07` / `frontend/**` / `backend/**` 本计划**零改动**;`files_modified` 只有 `gate-logs/idi-12-03/**` 与那份在盘报告"
    - "收口核盘的判据取 **ROADMAP 的 `## Milestones` + `## Progress`**,**不得**从 `.planning/state.json` 的 `phases` 推、**不得**采信 `state.*` 写入动词的输出(该组动词在本仓库已复现 15 次不可信:改错值 / 改分母 / 删字段 / 假报成功 + 零写入 / 部分成功 / 格式副作用;`update-progress` **不可**作为修正手段)"

  artifacts:
    - path: ".planning/phases/idi-12-g1-band/gate-logs/idi-12-03/"
      provides: "13 份原始门禁输出与退出码(五条浏览器门 + 两个探针 + 四个静态门 + pytest + `node --check`),供独立复核 —— 「门绿了」这一结论须有原始证据,摘录是选过的"
      contains: "check-09-idi09-validation.log"
    - path: ".planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md"
      provides: "以 HEAD 内容重新验证后的报告:新增 `re_verification` 段(触发原因 + 上一/当前 `covered_digest` + 逐文件变更归因 + 重跑的检查与读数),并更新 `covered_digest` 与 `verified`"
      contains: "re_verification:"

  key_links:
    - from: "`frontend/style.css` 的改动(波次 1)"
      to: "`.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md` 的 `covered_digest`"
      via: "该报告的 `covered_files` 含 `frontend/style.css` 与 `scripts/check-09-idi09-validation.py` ⇒ 本阶段必然作废它;处置 = 以 HEAD 内容重新验证而非刷新指纹"
      pattern: "covered_files:"
    - from: "11 份归档报告的 `covered_files`"
      to: "`.planning/milestones/v1XX-phases/...`(归档后的真实位置)"
      via: "逐行匹配命中 + 路径不在盘 ⇒ fail-closed stale,属 2026-09-14 登记的已知限制;登记而非修复"
      pattern: "milestones/v1"
    - from: "五条浏览器门"
      to: "本机 uvicorn(127.0.0.1:8765)"
      via: "`check-05` 的 `ensure_server()` —— 8765 上若已有残留进程则复用(不新起、结束也不关闭);读数不受影响,但若出现可疑读数先排查残留进程"
      pattern: "ensure_server"

  prohibitions:
    - statement: "不得修复归档报告的 `covered_files` 路径。那是「修归档」,超出 G1-01 / REG-04 的范围;11 份归档报告的 fail-closed stale 是 2026-09-14 就登记在案的已知限制,本阶段只登记不处置"
      status: active
      verification: flagged
    - statement: "不得用「只重算 `covered_digest`」代替「以 HEAD 内容重新验证」。内容确实变了,刷新指纹等于断言「自验证以来覆盖输入无变化」—— 那是假陈述,而指纹的价值正在于留下这个信号"
      status: active
      verification: flagged
    - statement: "不得采信 `state.*` 写入动词的输出,也不得用 `update-progress` / `sync` / `rebuild` / `record-session` 作为修正手段(它们会用坏值重算)。判据一律取 ROADMAP 的 `## Milestones` + `## Progress`"
      status: active
      verification: flagged
    - statement: "不得为了「门全绿」而删除 / 降级 / 放宽任何断言或阈值。`check-05` 全量 `exit=2` 是 item 5 两条 `--ai-smoke` 腿按设计 BLOCKED,不是回归 —— 不得为把它压成 0 而改动 `check-05`"
      status: active
      verification: flagged
    - statement: "不得在本计划改动任何产品源码(`frontend/**` / `backend/**`)或任何门脚本;`files_modified` 只有 `gate-logs/idi-12-03/**` 与 `.planning/phases/idi-11-.../idi-11-VERIFICATION.md`"
      status: active
      verification: flagged
    - statement: "不得顺手做未裁定项:v1.16 里程碑审计(走 `/gsd-audit-milestone`,不在本阶段内)、G2、`999.2`、暗色模式、Nyquist 缺口、图标与空状态、`check-10:328` 的过期注释、报告区表头 sticky(D-12-4 / D-12-12)"
      status: active
      verification: flagged
---

<objective>
在**最后一次渲染面改动落定之后**做整里程碑复跑(**REG-04**):五条浏览器门 + 两个探针 + 四个静态门 + pytest 基线逐条复跑、原始输出与退出码逐门落盘,并按既有「可执行性分诊」口径逐份处置因本次改动而作废的 `passed` 报告。

Purpose: `REG-04` 的「零新增失败」只有在**最后一次 `style.css` 改动之后**跑才成立 —— 所以它是收口阶段的需求,而不是反转阶段(ROADMAP Phase 12 Rationale)。同时,`frontend/style.css` 与 `scripts/check-09-idi09-validation.py` 的改动**必然作废**某些 `passed` 报告的指纹;处置口径是**逐份实测**(frontmatter 的 `covered_files` 逐行匹配 + 路径是否在盘),**不得凭记忆断言份数**(v1.15 Phase 10 的实测形状是「10 份覆盖,1 份可执行」,与本阶段的 12 份不同)。

**为什么判据锚 `^FAIL` 而不是子串搜索:** `check-05` 第 399 行有一条**标签里带 FAIL 一词的 PASS 行**,故计划字面的子串式判据在本项目**恒非空、无法通过**;锚行首 verdict 形态 `^FAIL` 才是可失败且非空转的判据(Phase 10 已为此付过一次代价)。

**为什么归档报告不修:** 它们的 `covered_files` 声明的是 `.planning/phases/...`,归档后移到 `.planning/milestones/v1XX-phases/...` ⇒ 重算返回 `null`(fail-closed = stale)。这是 2026-09-14 登记的已知限制:**归档后的阶段报告不再被 staleness 机制消费**,故记为已知限制而非回填重算。

**本计划关闭的需求:** REG-04。

**本计划不触碰:** `G1-01`(计划 01)、`VIS-01`(计划 02);所有产品源码与门脚本(本计划只跑不改);v1.16 里程碑审计(走 `/gsd-audit-milestone`,不在本阶段内)。

**执行前基线(规划期已在 HEAD 上实测,执行器须复核):**

| 检查 | 规划期在 HEAD 上的实测结果 |
|---|---|
| `bash scripts/check-01-token-conformance.sh` | `PASS`,`rc=0` |
| `bash scripts/check-03-hidden-uniqueness.sh` | `PASS`,`rc=0` |
| `bash scripts/check-04-important-count.sh` | `PASS`,`rc=0` |
| `.venv/bin/python scripts/check-02-contrast.py` | 以 `PASS: 0 failures` 结尾;`ORDER 0.363  --color-text-muted before --color-text on --color-surface`;`grep -c '/\* PAIR '` == 53 |
| `node --check frontend/app.js` | 通过 |
| `git status --porcelain frontend/` | 空;`frontend/vendor/` 只有 `marked.min.js` |
| `scripts/` 的门清单(磁盘现状) | `check-01`…`check-07` + `check-09` + `check-10`,外加 `probe-05-resolve-color.py` / `probe-07-focus-composite.py` / `probe-card-border-token.py` / `probe-menu-modal-reachability.py` —— **没有 `check-08`**(规划期初稿曾误列,已由路线图子代理核盘纠正) |
| `.planning/phases/idi-11-.../idi-11-VERIFICATION.md` 的 `covered_files` | **16 条,零缺失**;`status: passed`、`score: 12/12 must-haves verified` |
| `.planning/phases/idi-12-g1-band/gate-logs/` | **不存在**(本计划创建 `idi-12-03/` 子目录) |

**Flagged assumption(probe fallback,不得静默丢弃):** `REG-04` 在边界覆盖探针里返回 `{"category":"unclassified","status":"unresolved"}` —— 分类器的 cue 词汇是英文、而该需求文本是中文散文,故它**拒绝分类而不是乱猜**。按协议:`unclassified` 行**保持 `unresolved`**,**不得**用 backstop 自动消解、**不得**静默丢弃、**不得**为它发明探针派生的谓词。本计划的绑定验收判据来自 **ROADMAP 的 Success Criteria 3 / 4 与 CONTEXT 的 D-12-11 / D-12-12**,已逐条落进 `must_haves.truths`。

Output: `.planning/phases/idi-12-g1-band/gate-logs/idi-12-03/` 下的 13 份原始门禁输出;以 HEAD 内容重新验证后的 `idi-11-VERIFICATION.md`;11 份归档报告的逐份登记(写在 SUMMARY 里)。
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
@.planning/phases/idi-12-g1-band/12-CONTEXT.md
@.planning/phases/idi-12-g1-band/idi-12-PATTERNS.md
@.planning/phases/idi-12-g1-band/idi-12-01-PLAN.md
@.planning/phases/idi-12-g1-band/idi-12-02-PLAN.md
@.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md
@.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-04-SUMMARY.md
</context>

## Artifacts this phase produces

**本计划新增的符号(plan-review-convergence 的源锚定遍历须把它们排除在漂移核验之外):**

| 符号 | 类型 | 落点 |
|---|---|---|
| `.planning/phases/idi-12-g1-band/gate-logs/idi-12-03/` | 新目录(13 份 `.log`) | 文件系统 |
| `re_verification` 段 | `idi-11-VERIFICATION.md` frontmatter 的新键 | `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md` |

**本阶段前序计划已新增(此处复述以免被当作漂移):** `c6` / `"c6": c6` / `read_classlist` / fixture 的 `## 问题分级` 标题(计划 01);`--g1-snapshot DIR` / `g1_snapshot()` / `"g1-snapshot"`(计划 02);`.planning/phases/idi-12-g1-band/screenshots/**`(计划 02)。

**本计划不改动任何既有符号的源码定义。**

<tasks>

<task type="auto" tdd="false">
  <name>Task 1: 五条浏览器门 + 两个探针在最终态上复跑 —— 原始输出与退出码逐门落盘,判据锚行首 `^FAIL`</name>
  <files>.planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-05-ui-uat.log, .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-06-idi05-validation.log, .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-07-idi08-validation.log, .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-09-idi09-validation.log, .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-10-idi10-validation.log, .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/probe-05-resolve-color.log, .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/probe-07-focus-composite.log</files>
  <precondition>波次 1 与波次 2 的全部改动均已提交,`git status --porcelain frontend/ scripts/` 为空 ⇒ 复跑确实落在**最终态**上。</precondition>
  <read_first>
    - `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/`(17 份原始输出的**落盘约定与文件名先例**)
    - `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-04-PLAN.md` / `idi-11-04-SUMMARY.md`(五条浏览器门 + 两探针 + 四静态门 + pytest 的同形复跑与判据写法)
    - `scripts/check-05-ui-uat.py` 的文件头(浏览器路线与 `--browser bundled` 的实测结论)、`:4007-4013`(`parse_args`)、`:399-401` 附近那条**标签里带 FAIL 一词的 PASS 行**(计划字面式子串判据恒非空的成因)
    - `scripts/check-09-idi09-validation.py` 的 `main()`(退出码语义)、`scripts/check-06-idi05-validation.py:496-498` / `check-07-idi08-validation.py:833-835` / `check-10-idi10-validation.py:678-689`(`parse_args`)
    - `scripts/probe-05-resolve-color.py` 的文件头(「修复前 PASS / 修复后 BLOCKED」的对照支语义,退出码仍为 0)
    - `.planning/phases/idi-12-g1-band/12-CONTEXT.md` 的 D-12-11 与 ROADMAP Phase 12 的 Gates 段
  </read_first>
  <action>
    在**最终态**上逐门复跑,把**原始输出 + 退出码**落盘到 `.planning/phases/idi-12-g1-band/gate-logs/idi-12-03/<gate>.log`(先 `mkdir -p`;每份日志末尾另记一行 `rc=<退出码>`)。七条命令:

    - `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled`(**必须** `--browser bundled`;该机 `channel="chrome"` + headless 会 CDP 挂死)
    - `.venv/bin/python scripts/check-06-idi05-validation.py`
    - `.venv/bin/python scripts/check-07-idi08-validation.py`
    - `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4,c5,c6`
    - `.venv/bin/python scripts/check-10-idi10-validation.py`
    - `.venv/bin/python scripts/probe-05-resolve-color.py`
    - `.venv/bin/python scripts/probe-07-focus-composite.py`

    判据(逐门,从落盘的日志里读,**不采信「命令退 0 所以没问题」**):
    - 每份日志的 `^FAIL` 行数 == **0**(锚**行首** verdict 形态;子串式判据会命中 `check-05` 那条标签里带 FAIL 一词的 PASS 行,恒非空)。
    - `check-05` 的全量 `exit=2` 是**设计行为**:从日志里核 `item 5:` 汇总行的 BLOCKED 计数 == **2**(两条 `--ai-smoke` 腿),且成因集合里**没有别的 BLOCKED 来源**;把该结论与两条腿的名字抄进 SUMMARY。
    - `check-06` / `check-07` / `check-09` / `check-10` 的退出码均为 **0**;`check-09` 的 `=== 逐项结论 ===` 块里 `c1..c6` 全 PASS、0 FAIL、0 BLOCKED,并抄录六项各自的断言条数。
    - 两个探针退出码均为 **0**;`probe-05` 输出里的 `BLOCKED [mutated] … post-fix` 是它的**对照支**(同一份被变异的样式表上跑同一条断言两次),**不是门失败** —— 在 SUMMARY 里显式写明,免得被下游读成回归。
    - **跨阶段对照取归一化(剥临时路径)后的逐行 diff,不取「结论块看着一样」** —— 这个粒度才捞得出计划未点名的读数位移(Phase 10 / 11 都靠它捞出过 1px / 3px 级差异)。把与 Phase 11 收口日志的差异逐条登记(有位移就登记成因,没有就写「零位移」)。
  </action>
  <verify>
    <automated>for f in check-05-ui-uat check-06-idi05-validation check-07-idi08-validation check-09-idi09-validation check-10-idi10-validation probe-05-resolve-color probe-07-focus-composite; do printf '%s ' "$f"; grep -c '^FAIL' ".planning/phases/idi-12-g1-band/gate-logs/idi-12-03/$f.log"; done</automated>
    <fails_when>any of the seven printed counts is not "0"</fails_when>
    <automated>grep -n '^rc=' .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-06-idi05-validation.log .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-07-idi08-validation.log .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-09-idi09-validation.log .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-10-idi10-validation.log .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/probe-05-resolve-color.log .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/probe-07-focus-composite.log</automated>
    <fails_when>any of the six printed rc lines is not "rc=0"</fails_when>
    <automated>grep -E '^item (c1|c2|c3|c4|c5|c6): PASS' .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-09-idi09-validation.log | wc -l</automated>
    <fails_when>the count is not "6" (all six items must be present and PASS)</fails_when>
    <automated>grep -E '^item 5: ' .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-05-ui-uat.log; grep -c '^FAIL' .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-05-ui-uat.log; grep -c '^rc=' .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-05-ui-uat.log</automated>
    <fails_when>the item 5 summary line does not show exactly "2 BLOCKED", or the FAIL count is not "0", or the rc marker line count is not "1"</fails_when>
    <automated>git status --porcelain frontend/ scripts/ backend/</automated>
    <fails_when>output is not empty (this task must run gates, not edit code)</fails_when>
  </verify>
  <acceptance_criteria>
    - `.planning/phases/idi-12-g1-band/gate-logs/idi-12-03/` 下有且仅有 7 份本次浏览器/探针日志(`check-05-ui-uat.log` / `check-06-idi05-validation.log` / `check-07-idi08-validation.log` / `check-09-idi09-validation.log` / `check-10-idi10-validation.log` / `probe-05-resolve-color.log` / `probe-07-focus-composite.log`),每份末尾有一行 `rc=<退出码>`。
    - 七份日志的 `^FAIL` 行数均为 `0`。
    - `check-05-ui-uat.log` 的 `rc=2`,`item 5:` 汇总行显示恰 `2 BLOCKED`,且该 BLOCKED 的两条腿名为 `--ai-smoke` 相关的冒烟项(逐字抄进 SUMMARY);其余六份 `rc=0`。
    - `check-09-idi09-validation.log` 里 `item c1:` … `item c6:` 六行均以 `PASS` 开头且各为 `0 FAIL,0 BLOCKED`,六项断言条数被抄进 SUMMARY。
    - 与 Phase 11 收口日志的归一化逐行 diff 结果已登记(有位移则逐条给出成因)。
    - `git status --porcelain frontend/ scripts/ backend/` 为空。
  </acceptance_criteria>
  <done>五条浏览器门与两个探针在最终态上复跑完毕,原始输出与退出码逐门落盘;`^FAIL` 全为 0;`check-05` 的 `exit=2` 被证实仍只是 item 5 的两条 `--ai-smoke` 腿按设计 BLOCKED;`check-09` 的 `c1..c6` 全 PASS;`probe-05` 的 `BLOCKED [mutated]` 对照支被显式标注为非回归。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 2: 四个静态门 + pytest 基线 + `node --check` 复跑落盘</name>
  <files>.planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-01-token-conformance.log, .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-02-contrast.log, .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-03-hidden-uniqueness.log, .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-04-important-count.log, .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/pytest.log, .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/node-check-app-js.log</files>
  <read_first>
    - `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/`(同名日志文件的落盘先例,含 `check-01-token-conformance.log` … `pytest.log`)
    - `scripts/check-01-token-conformance.sh` / `check-03-hidden-uniqueness.sh` / `check-04-important-count.sh`(三条恒不变式:`!important` 数的是**声明**数、`.hidden {` 数的是**规则**条数 —— 计数门的算术陷阱本项目已红过三次)
    - `scripts/check-02-contrast.py`(围栏内 PAIR 清单、`TEXT_MIN` / `NON_TEXT_MIN`、`ORDER` 断言)
    - `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-04-SUMMARY.md`(pytest 基线的记录形态与「必须用项目 `.venv`」的成因)
    - `.planning/phases/idi-12-g1-band/12-CONTEXT.md` 的 D-12-1 ②(`--color-surface` 的 TEXT 配对仍成立、零新增对比度条目)
  </read_first>
  <action>
    在**最终态**上逐条复跑,原始输出与退出码落盘到 `.planning/phases/idi-12-g1-band/gate-logs/idi-12-03/<name>.log`(每份末尾另记一行 `rc=<退出码>`):

    - `bash scripts/check-01-token-conformance.sh` → `check-01-token-conformance.log`
    - `.venv/bin/python scripts/check-02-contrast.py` → `check-02-contrast.log`(把**完整**输出落盘,含全部 `PASS` 行与 `ORDER` 行 —— 只留结论行不足以复核「零新增条目、零阈值改动」)
    - `bash scripts/check-03-hidden-uniqueness.sh` → `check-03-hidden-uniqueness.log`
    - `bash scripts/check-04-important-count.sh` → `check-04-important-count.log`
    - `.venv/bin/python -m pytest backend/tests -q --tb=short` → `pytest.log`(**必须**用项目 `.venv` —— 环境 `python3` 是 miniconda,会让 4 个 `ai_caller` 测试假失败)
    - `node --check frontend/app.js` → `node-check-app-js.log`

    判据(从落盘日志里读):
    - `check-01` / `check-03` / `check-04` 各打印 `PASS`、`rc=0`。
    - `check-02` 以 `PASS: 0 failures` 结尾、`rc=0`;`ORDER` 行逐字仍为 `ORDER 0.363  --color-text-muted before --color-text on --color-surface`;`grep -c '/\* PAIR ' frontend/style.css` == **53**(零新增条目);`TEXT_MIN` / `NON_TEXT_MIN` 与 HEAD 逐字节相同(用 `git diff -- scripts/check-02-contrast.py` 为空来佐证「阈值未动」)。
    - pytest 报 **219 passed, 6 skipped**(规划期在 HEAD 上实测的汇总行为 `219 passed, 6 skipped, 1 warning in 7.03s`;`-m "not slow"` 下同样这 6 条会被 pytest 官方标为 `deselected` —— 同一批 6 条,两个标签都记以免被读成漂移);把该行逐字抄进 SUMMARY。
    - `node --check` 通过、`rc=0`。
    - 另核:`git status --porcelain frontend/` 仅预期文件、`frontend/vendor/` 仍只有 `marked.min.js`、`git diff --stat -- frontend/app.js frontend/index.html backend/ frontend/vendor/` 为空。
    - 与 Phase 11 收口日志的归一化逐行 diff 结果逐条登记(有位移给成因)。
  </action>
  <verify>
    <automated>for f in check-01-token-conformance check-02-contrast check-03-hidden-uniqueness check-04-important-count pytest node-check-app-js; do printf '%s ' "$f"; grep -c '^rc=' ".planning/phases/idi-12-g1-band/gate-logs/idi-12-03/$f.log"; done</automated>
    <fails_when>any of the six printed counts is not "1" (each log must carry exactly one rc marker)</fails_when>
    <automated>grep -n '^rc=0$' .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-01-token-conformance.log .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-02-contrast.log .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-03-hidden-uniqueness.log .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-04-important-count.log .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/node-check-app-js.log | wc -l</automated>
    <fails_when>the count is not "5" (all five of these must exit 0)</fails_when>
    <automated>grep -F 'PASS: 0 failures' .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-02-contrast.log; grep -F 'ORDER 0.363' .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-02-contrast.log; grep -c '/\* PAIR ' frontend/style.css</automated>
    <fails_when>either grep prints nothing, or the PAIR count is not "53"</fails_when>
    <automated>grep -E '^[0-9]+ passed' .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/pytest.log; grep -c '^rc=0$' .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/pytest.log</automated>
    <fails_when>the passed count is not "219", or the skipped count is not "6", or the rc marker is not "rc=0"</fails_when>
    <automated>git status --porcelain frontend/ scripts/ backend/; git diff --stat -- frontend/app.js frontend/index.html backend/ frontend/vendor/</automated>
    <fails_when>the first command's output is not empty, or the second command's output is not empty</fails_when>
  </verify>
  <acceptance_criteria>
    - 六份日志均在盘,各末尾一行 `rc=<退出码>`;`check-01` / `check-02` / `check-03` / `check-04` / `node-check-app-js` 的 `rc=0`,`pytest.log` 的 `rc=0`。
    - `check-02-contrast.log` 含 `PASS: 0 failures` 与逐字不变的 `ORDER 0.363  --color-text-muted before --color-text on --color-surface`;`grep -c '/\* PAIR ' frontend/style.css` 输出 `53`。
    - `pytest.log` 的汇总行为 `219 passed, 6 skipped`(或等价的 pytest 计数写法,含 225 collected),逐字抄进 SUMMARY;SUMMARY 里写明「必须用项目 `.venv`」的成因。
    - `check-01` / `check-03` / `check-04` 的日志里能看到 `PASS`;`check-04` 的判据是 `!important;` **声明**数(不是命中行数)。
    - `git status --porcelain frontend/ scripts/ backend/` 为空;`git diff --stat -- frontend/app.js frontend/index.html backend/ frontend/vendor/` 为空;`frontend/vendor/` 只有 `marked.min.js`。
    - 与 Phase 11 收口日志的归一化逐行 diff 结果已登记。
  </acceptance_criteria>
  <done>四个静态门 + pytest 基线 + `node --check` 在最终态上复跑完毕、原始输出与退出码落盘;`check-02` 零新增条目、零阈值改动、`ORDER` 不变;pytest 基线 219 passed / 6 skipped 不降;`frontend/**` 与 `backend/**` 逐字节未改。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 3: 连带指纹逐份实测与处置 —— 11 份归档报告登记为已知限制,1 份在盘报告以 HEAD 内容重新验证</name>
  <files>.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md</files>
  <read_first>
    - `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md`(将被重新验证的报告;注意其 frontmatter 里**已有**一个 `re_verification:` 段与 `bookkeeping_reverification` 子段 —— 那是 Phase 11 收口时对 `97b428f` 记账改动做的第二轮,是本任务要照抄的**留档形态**)
    - `.planning/milestones/v1.15-phases/idi-10-tables-and-radius-scale/10-CONTEXT.md`(连带指纹的**实测形状**与处置先例:10 份覆盖 / 1 份可执行 / 只重验 `idi-09` / 以 HEAD 内容重新验证而非刷新指纹)
    - `.planning/STATE.md` 的 `## Blockers/Concerns` 里 2026-09-14 登记的已知限制条目(归档后的 `covered_digest` 不可解析)
    - `.planning/phases/idi-12-g1-band/12-CONTEXT.md` 的 **D-12-11**(完整形状与逐份处置口径)
  </read_first>
  <action>
    **(a) 逐份实测,不凭记忆断言份数。** 筛选面 = 本次全部改动文件:`frontend/style.css`、`scripts/check-09-idi09-validation.py`、`scripts/ui-states/checking/docs/DESIGN-check-2.md`。对 `.planning/` 下全部 `*VERIFICATION.md` 与 `*VALIDATION.md`(含 `milestones/` 与 `quick/` 两个归档区),**解析 frontmatter 的 `covered_files` 列表并逐行匹配**(**不得**用全文 grep —— 全文 grep 会把只在正文提及该文件的报告算进来,`idi-08` 就是这种假阳性),并**额外测每一条声明的路径是否仍在盘**。把「命中 / 路径缺失条数 / 路径总数」三个数逐份记下来。

    预期形状(规划期已实测,执行器须复核并如实记录;若实测与预期不符,**以实测为准**并把差异写进 SUMMARY):共 **12 份**命中。
    - **11 份归档报告**——v1.13 的 `01` / `02` / `03`,v1.14 的 `idi-04` / `idi-04.1` / `idi-05` / `idi-06` / `idi-07`,v1.15 的 `idi-09` / `idi-10`,quick 的 `260925-iin`。它们的 `covered_files` 里有 **2–13 条路径已不在盘**(`.planning/phases/...` 归档后移到 `.planning/milestones/v1XX-phases/...`)⇒ **fail-closed stale,属 2026-09-14 登记的已知限制**。**处置 = 在 SUMMARY 里逐份列名(报告名 + 命中哪个改动文件 + 缺失路径条数)并登记为已知限制,不重验、不修复归档路径。**
    - **1 份在盘**——`.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md`(`covered_files` 16 条**零缺失**)。

    **(b) 把在盘的那一份以 HEAD 内容重新验证。** 步骤:①重跑它引用的判据(`.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4,c5`,外加本计划 Task 1 / Task 2 已落盘的五条浏览器门与四静态门读数 —— 直接复用那 13 份日志,不重复起浏览器);②逐条确认报告里的 12/12 must-haves 与它的 `checks_rerun` 记录在 HEAD 上仍成立;③在报告 frontmatter 的 `re_verification:` 段里**追加**一个新轮次(照它已有的 `bookkeeping_reverification` 形态):触发原因(本阶段改写了 `frontend/style.css` 与 `scripts/check-09-idi09-validation.py`,两者都在它的 `covered_files` 里)、`previous_digest` / `current_digest`、`commits_since_previous_report`、`changed_covered_files` 逐条变更归因、`checks_rerun` 的实际读数;④更新 `covered_digest` 与 `verified` 时间戳。

    **不得只重算 `covered_digest` 而不重跑判据** —— 内容确实变了,刷新指纹等于断言「自验证以来覆盖输入无变化」,而那是假陈述;指纹的价值正在于留下这个信号。**不得删除 / 精简 `covered_files` 条目**(删条目是让报告假装新鲜的典型手法)。

    **(c) 记下一条顺序性事实。** 本任务算出的 `covered_digest` 覆盖的 `.planning/ROADMAP.md` 会在阶段收口时被再次合法改写 ⇒ 该 digest 会再次变 stale。**这是预期内的**:按 Phase 11 的先例(`97b428f` 之后的 `bookkeeping_reverification` 第二轮),后续由记账型重新验证轮次处置,**不属本计划的缺口**。把这条事实写进 SUMMARY,供下游 `/gsd-verify-work idi-11` 或收口记账轮消费。

    **(d) 收口核盘的判据。** 全程**不得**采信 `state.*` 写入动词的输出;任何对进度 / 阶段的判断一律取 `.planning/ROADMAP.md` 的 `## Milestones` 与 `## Progress` 两节,**不得**从 `.planning/state.json` 的 `phases` 推。把这两节的现状抄进 SUMMARY(只读核对,**不在本计划里改动它们**)。
  </action>
  <verify>
    <automated>git diff --exit-code -- scripts/check-02-contrast.py scripts/check-01-token-conformance.sh scripts/check-03-hidden-uniqueness.sh scripts/check-04-important-count.sh scripts/check-05-ui-uat.py scripts/check-06-idi05-validation.py scripts/check-07-idi08-validation.py scripts/check-10-idi10-validation.py; echo "rc=$?"</automated>
    <fails_when>rc is not "0" (no gate script other than check-09 may have been touched by this phase)</fails_when>
    <automated>grep -c '^  re_verification:' .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md; grep -c '^covered_digest:' .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md; grep -c '^  - frontend/style.css$' .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md</automated>
    <fails_when>the re_verification count is not "1", or the covered_digest count is not "1", or the covered_files entry for frontend/style.css is not "1" (deleting an entry to make the report look fresh is forbidden)</fails_when>
    <automated>.venv/bin/python -c "import re,pathlib;t=pathlib.Path('.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md').read_text(encoding='utf-8');m=re.search(r'^covered_digest:\s*\"([^\"]+)\"',t,re.M);print('digest',m.group(1) if m else None);print('has_prev', 'previous_digest' in t);print('has_commits', 'commits_since_previous_report' in t)"</automated>
    <fails_when>digest is None, or has_prev is False, or has_commits is False (the re-verification round must record the previous digest and the commits that invalidated it)</fails_when>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4,c5</automated>
    <fails_when>non-zero exit, or any FAIL, or any BLOCKED (the re-verified report's cited checks must still hold on HEAD)</fails_when>
    <automated>git status --porcelain scripts/ frontend/ backend/</automated>
    <fails_when>output contains any path other than "scripts/check-09-idi09-validation.py"</fails_when>
  </verify>
  <acceptance_criteria>
    - SUMMARY 里有一张**逐份**的连带面表:12 行,每行给出报告名、命中的改动文件、`covered_files` 条数、路径缺失条数,并标出「归档 / 在盘」与处置结论。
    - 11 份归档报告被登记为**已知限制**(fail-closed stale,归档路径不可解析),**逐份列名**;SUMMARY 里显式写明「未修复任何归档报告的路径」。
    - `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md` 的 `re_verification:` 段新增了一个轮次,含触发原因、`previous_digest`、`current_digest`、`commits_since_previous_report`、`changed_covered_files` 逐条归因与 `checks_rerun` 读数;`covered_digest` 与 `verified` 已更新;`covered_files` 的 **16 条一条未删**(尤其 `frontend/style.css` 与 `scripts/check-09-idi09-validation.py` 两条仍在)。
    - `check-09 --item c1,c2,c3,c4,c5` 在 HEAD 上 `exit=0`、0 FAIL、0 BLOCKED。
    - SUMMARY 里记录了「本任务算出的 digest 会因后续 ROADMAP 记账改写再次变 stale,按 Phase 11 先例由记账型重新验证轮次处置」这条顺序性事实。
    - SUMMARY 里抄录了 ROADMAP `## Milestones` 与 `## Progress` 两节的现状(只读核对),并写明「未采信 `state.*` 写入动词的输出、未改动这两节」。
  </acceptance_criteria>
  <done>连带指纹面在磁盘上逐份实测完毕(12 份:11 份归档登记为已知限制并逐份列名、不修归档路径;1 份在盘报告以 HEAD 内容重新验证并写入新的 `re_verification` 轮次与更新后的 `covered_digest`);`covered_files` 一条未删;顺序性事实与 ROADMAP 核盘现状均已留档。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 门禁日志 → 「零新增失败」这条结论 | 摘录是选过的;结论必须有**原始输出**支撑,且判据须锚行首 `^FAIL` 而非子串 |
| 报告 frontmatter 的 `covered_files` / `covered_digest` → 阶段是否「已验证」 | 刷新指纹会抹掉 staleness 信号;删条目会让报告假装新鲜 |
| `.planning/ROADMAP.md` / `.planning/state.json` → 进度判据 | `state.*` 写入动词在本仓库已复现 15 次不可信;判据只能取 ROADMAP 的两节 |
| 本机 uvicorn(127.0.0.1:8765) | 可能存在先前遗留进程;门复用它(不新起、结束也不关闭) |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-12-11 | Repudiation | 连带指纹的处置 | high | mitigate | 判据锚 `covered_files` **逐行匹配** + **路径是否在盘**两个独立量;在盘的那份**重跑其引用的判据**后才更新 digest,并在 `re_verification` 段记录 `previous_digest` / 归因;`<verify>` 断言 `covered_files` 的 `frontend/style.css` 条目数仍为 1(删条目即红) |
| T-12-12 | Tampering | 「门全绿」的结论 | high | mitigate | 13 份原始输出与退出码逐门落盘;判据锚行首 `^FAIL`(子串式会被 `check-05` 那条带 FAIL 一词的 PASS 行命中、恒非空);跨阶段对照取归一化逐行 diff 而非「结论块看着一样」 |
| T-12-13 | Spoofing | 用 `state.*` 写入动词的输出冒充进度事实 | medium | mitigate | 判据一律取 ROADMAP 的 `## Milestones` + `## Progress`;SUMMARY 里显式声明未采信该组动词、未改动那两节 |
| T-12-14 | Tampering | 「修归档」——为让 stale 消失而回填归档报告的路径 | medium | mitigate | 明文禁止修复归档路径(那是 2026-09-14 登记的已知限制);`<verify>` 断言除 `check-09` 外**零门脚本改动**,`files_modified` 只含日志与那一份报告 |
| T-12-15 | Denial of Service | 浏览器门在 `channel="chrome"` + headless 下 CDP 挂死 | low | mitigate | 固定 `--browser bundled`(Playwright 自带 chromium + 无头);`check-09` 无 `--browser` 参数、本就固定 bundled |
| T-12-SC | Tampering | npm / pip / cargo 安装 | low | accept | 本阶段**零新增依赖**(DESIGN.md D-06);pytest 走既有 `.venv` ⇒ 无安装动作,无包合法性门可触发 |
</threat_model>

<verification>
**整体阶段检查(本计划收口时,即整里程碑收口时):**

1. 13 份日志在 `.planning/phases/idi-12-g1-band/gate-logs/idi-12-03/` 下,每份带 `rc=` 行;五条浏览器门 + 两探针的 `^FAIL` 计数全为 0。
2. `check-05` 全量 `rc=2`,成因仅 item 5 的两条 `--ai-smoke` 腿;`check-06` / `check-07` / `check-09` / `check-10` / 两探针 `rc=0`。
3. 四静态门 `rc=0`;`check-02` `PASS: 0 failures` + `ORDER 0.363` + PAIR 53;pytest `219 passed / 6 skipped`;`node --check` 通过。
4. `idi-11-VERIFICATION.md` 有新的 `re_verification` 轮次与更新后的 `covered_digest`,`covered_files` 一条未删;11 份归档报告在 SUMMARY 里逐份列名登记。
5. `git status --porcelain frontend/ scripts/ backend/` 仅含 `scripts/check-09-idi09-validation.py`(波次 1 的产物);`frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**` 逐字节未改。
6. **顺序性提醒(留给编排器,不在本计划内执行):** ROADMAP 的 Phase 12 状态翻转 / `## Progress` 行更新是**记账写入**,会再次改写 `idi-11-VERIFICATION.md` 的 `covered_files` 之一(`.planning/ROADMAP.md`)⇒ 该报告会再变 stale。核盘判据取 ROADMAP 的 `## Milestones` + `## Progress`,且**核盘必须放在收口序列的最后一个动词之后**;`state.*` 写入动词的输出不可作为判据。
</verification>

<success_criteria>
- 五条浏览器门 + 两个探针 + 四个静态门 + pytest 基线在**最终态**上复跑,零新增失败;原始输出与退出码逐门落盘。
- `check-05` 的 `exit=2` 被证实仍只因 item 5 的两条 `--ai-smoke` 腿按设计 BLOCKED。
- 连带指纹面逐份实测(12 份):11 份归档报告登记为已知限制并逐份列名、不修归档路径;1 份在盘报告以 HEAD 内容重新验证并写入新的 `re_verification` 轮次。
- `covered_files` 条目零删除;零产品源码改动;零门脚本改动(`check-09` 除外,那是波次 1 的产物)。
</success_criteria>

<output>
Create `.planning/phases/idi-12-g1-band/idi-12-03-SUMMARY.md` when done
</output>

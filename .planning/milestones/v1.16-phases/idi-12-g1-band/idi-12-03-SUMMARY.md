---
phase: idi-12-g1-band
plan: 03
subsystem: testing
tags: [gate-rerun, playwright, pytest, verification-fingerprint, mutation-testing, g1-band, reg-04]

# Dependency graph
requires:
  - phase: idi-12-g1-band
    provides: "波次 1 的 G1-01 修复:#latest-check 宿主绘制面就地改归统一面白 + check-09 新增运行时项 c6 + checking fixture 补「问题分级」表"
  - phase: idi-12-g1-band
    provides: "波次 2 的 VIS-01:5 张 1440×900 整窗截图 + check-09 新增 --g1-snapshot 局部特写"
provides:
  - "13 份原始门禁输出与退出码(gate-logs/idi-12-03/),供独立复核「零新增失败」这条结论"
  - "idi-11-VERIFICATION.md 的第三轮 content_reverification(以 HEAD 内容重新验证,非刷新指纹)+ 更新后的 covered_digest"
  - "11 份归档报告的 fail-closed stale 逐份登记(不修归档路径)"
affects: [idi-12-g1-band, phase-12-closeout, v1.16-milestone-audit]

# Actuals (#2632) — pairs with the plan's estimate to calibrate future estimates.
actuals:
  tokens: 49533
  tasks: 3
  commits: 3

# Column-0 ledger fields (verify-work extracts these with ^-anchored greps).
commits: 3
plan_head_before: 8baf330ebdd4023702108322627f23c9c95605a7

tech-stack:
  added: []
  patterns:
    - "跨阶段门禁对照取归一化(剥临时路径 + 剥 exit marker)后的逐行 diff —— 这个粒度才捞得出「结论块看着一样」看不见的读数位移"
    - "指纹位移归因:仅把 changed_covered_files 换回上一版内容复算 digest,精确复现旧值即证明位移 100% 归因于这几个文件"

key-files:
  created:
    - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-01-token-conformance.log
    - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-02-contrast.log
    - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-03-hidden-uniqueness.log
    - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-04-important-count.log
    - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-05-ui-uat.log
    - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-06-idi05-validation.log
    - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-07-idi08-validation.log
    - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-09-idi09-validation.log
    - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-10-idi10-validation.log
    - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/node-check-app-js.log
    - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/probe-05-resolve-color.log
    - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/probe-07-focus-composite.log
    - .planning/phases/idi-12-g1-band/gate-logs/idi-12-03/pytest.log
  modified:
    - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md

key-decisions:
  - "连带指纹面磁盘实测为 12 份(11 份归档 fail-closed stale + 1 份在盘),与规划期预期形状一致;11 份逐份列名登记为已知限制,不修归档路径(那是「修归档」,超出 G1-01 / REG-04 范围)"
  - "在盘的那份以 HEAD 内容重新验证而非刷新指纹:12 条真值逐条重立,并新增第三轮 content_reverification 段(触发原因 + previous/current digest + 18 笔提交 + 4 个 changed_covered_files 逐条归因 + 重跑读数)"
  - "digest 位移实测由 4 个 covered_files 造成(style.css / check-09 / ROADMAP / REQUIREMENTS),而非计划预期的 2 个;归因以「仅把这 4 份换回上一版内容即精确复现旧 digest」证明,不靠推断"
  - "Truth 10 的变异证明本轮重跑而非承前:上一轮不重跑的唯一理由是「载体哈希未变」,而本轮两个载体都真的变了,该理由失效;M1 → c4 21 FAIL、M3 → c2 2 FAIL,读数与上一轮逐字相同"
  - "check-05 的行号锚点位移 +4 分解为 +1(Phase 11 收口后的 1ec75c6 特异性注释更正)+ +3(波次 1 的围栏承重注释就地改写 39bce0b),全部为「在该行之前插入」而非重排"
  - "跨阶段对照捞出两处计划未点名的读数位移(见「跨阶段对照」段):#latest-check 新增一个 Tab 停靠点、SC1 探针首个控件身份随之变化 —— 二者均非门失败,已给实测成因"

patterns-established:
  - "「以 HEAD 内容重新验证」的完整形态:先证明 digest 位移的 100% 归因 → 再逐条重立承重真值 → 再对上一轮「承前有效」的判据逐条重跑(载体变了就不承前)→ 最后才更新 digest 与时间戳"

requirements-completed: [REG-04]

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "13 份原始门禁输出与退出码落盘;五条浏览器门 + 两探针的 ^FAIL 计数全为 0;check-05 全量 rc=2 的成因集合仍只是 item 5 的两条 --ai-smoke 腿;四静态门 rc=0;check-02 PASS: 0 failures + ORDER 0.363 + PAIR 53;pytest 219 passed / 6 skipped;node --check 通过"
    requirement: "REG-04"
    verification:
      - kind: other
        ref: "for f in check-01..check-04 check-05-ui-uat check-06 check-07 check-09 check-10 probe-05 probe-07 pytest node-check-app-js; do grep -c '^FAIL' $f.log; done → 全 0;grep '^rc=' → check-05 rc=2,其余 12 份 rc=0;grep -E '^item c[1-6]: PASS' check-09.log | wc -l → 6"
        status: pass
    human_judgment: false
  - id: D2
    description: "idi-11-VERIFICATION.md 以 HEAD 内容重新验证:新增第三轮 content_reverification 段(触发原因 + previous/current digest + 18 笔提交 + 4 个 changed_covered_files 逐条归因 + 重跑读数),covered_digest 由 9bdba54b 更新为 c5d1e338,verified 时间戳更新;covered_files 16 条一条未删;12/12 真值在 HEAD 上重立;M1/M3 两条变异在已变载体上重跑,读数逐字相同"
    requirement: "REG-04"
    verification:
      - kind: other
        ref: "gsd-tools query verification.status <phase_dir> → status passed;grep -c '^covered_digest:' → 1;covered_files 计数 → 16(含 frontend/style.css 与 scripts/check-09-idi09-validation.py);check-09 --item c1,c2,c3,c4,c5 → exit=0(59/19/6/39/5,0 FAIL 0 BLOCKED)"
        status: pass
    human_judgment: false
  - id: D3
    description: "连带指纹面逐份实测(12 行表:报告名 / 命中的改动文件 / covered_files 条数 / 路径缺失条数 / 归档或在盘 / 处置);11 份归档报告登记为已知限制并逐份列名,未修复任何归档路径;两份零涟漪结论复核(纳入 check-09 不新增报告;fixture 不被任何报告覆盖)"
    requirement: "REG-04"
    verification:
      - kind: other
        ref: "逐份解析 .planning/ 下全部 *VERIFICATION.md / *VALIDATION.md(17 份)的 frontmatter covered_files 逐行匹配三份改动文件 + 逐条测路径是否在盘 → 12 份命中;fixture 的 covered_files 命中 0、全文命中 0"
        status: pass
    human_judgment: false
  - id: D4
    description: "顺序性事实留档:本轮算出的 covered_digest 覆盖 .planning/ROADMAP.md,而阶段收口会再次合法改写它 ⇒ 该 digest 会再次变 stale,按 Phase 11 先例由记账型重新验证轮次处置,不属本计划缺口"
    verification: []
    human_judgment: true
    rationale: "这是对**尚未发生**的收口序列的预判(且收口动作不在本计划内),机器判据只能证明当前 digest 与当前内容一致,无法证明「下一次记账会再次改写它」。验证者须结合编排器的收口序列确认这条留档没有被当作「已闭合」。"

# Metrics
duration: 34min
completed: 2026-09-29
status: complete
---

# Phase 12 Plan 03: 整里程碑复跑与连带指纹处置 Summary

五条浏览器门 + 两探针 + 四静态门 + pytest 基线在**最终态**上复跑、13 份原始输出与退出码逐门落盘(零新增失败),并逐份处置因本阶段改动而作废的 `passed` 报告 —— 11 份归档报告登记为已知限制、1 份在盘报告以 HEAD 内容重新验证(第三轮 `content_reverification`,`covered_digest` `9bdba54b` → `c5d1e338`)。

## Performance

- **Duration:** 34 min
- **Started:** 2026-09-29T08:02:59Z
- **Completed:** 2026-09-29T08:36:48Z
- **Tasks:** 3 completed
- **Files modified:** 14 (13 份新日志 + 1 份报告)

## Accomplishments

- **零新增失败,且有原始证据。** 13 份门禁输出逐门落盘 `gate-logs/idi-12-03/`,每份末尾一行 `rc=<退出码>`。判据锚**行首** verdict 形态 `^FAIL`(子串式会命中 `check-05` 第 399 行那条标签里带 FAIL 一词的 PASS 行,在本项目恒非空、无法通过),七份日志的 `^FAIL` 计数**全为 0**。
- **`check-05` 的 `exit=2` 被证实仍只是设计行为。** 日志里 `item 5: BLOCKED (9 条断言,0 FAIL,2 BLOCKED)`;全日志 `^BLOCKED` 行恰 **2** 条,两条腿逐字为:
  - `BLOCKED [p3] 交互冒烟「处理本轮批注」: expected=无错误完成 actual=<未执行>  # 需要真实 AI 调用,默认不执行;加 --ai-smoke 重跑`
  - `BLOCKED [p3] 交互冒烟「发送」: expected=无错误完成 actual=<未执行>  # 需要真实 AI 调用,默认不执行;加 --ai-smoke 重跑`
  无第三个 BLOCKED 来源。**未为把它压成 0 而改动任何门脚本。**
- **`check-09` 与 Phase 11 改写后的契约一致。** `--item c1,c2,c3,c4,c5,c6` → `exit=0`,`c1..c6` 全 PASS、0 FAIL、0 BLOCKED。六项断言条数:`c1 59` / `c2 19` / `c3 6` / `c4 39` / `c5 5` / `c6 7`(共 135)。**`c1..c5` 与 Phase 11 收口读数逐项相同**(59/19/6/39/5),`c6` 是 Phase 12 新增。
- **两探针 `rc=0`。** `probe-05` 输出里的 `BLOCKED [mutated] … post-fix` 是它**自己的对照支**(同一份被变异的样式表上跑同一条断言两次,「修复前 PASS / 修复后 BLOCKED」正是它要证明的对照),**不是门失败**;`probe-07` 的 `PROBE control-verdict=PASS`、环 `rgb(31, 99, 189)` 2px、`archive` 合成地面 `rgb(255, 255, 255)` 比值 `3.54 (>= 3.0)`。
- **四静态门 + pytest 基线不降。** `check-01` / `check-03` / `check-04` 各 `PASS` `rc=0`;`check-02` 以 `PASS: 0 failures` 结尾,`ORDER 0.363  --color-text-muted before --color-text on --color-surface` **逐字不变**,`grep -c '/\* PAIR ' frontend/style.css` == **53**(零新增条目),`git diff` 对 `scripts/check-02-contrast.py` 为空(阈值未动);`node --check` 对 `frontend/app.js` 通过。
- **pytest 基线逐字:** `219 passed, 6 skipped, 1 warning in 9.03s`。**必须用项目 `.venv`** —— 环境 `python3` 是 miniconda,会让 4 个 `ai_caller` 测试假失败(本仓库已登记)。
- **连带指纹面逐份实测(12 份),不凭记忆断言份数。** 判据锚报告 frontmatter 的 `covered_files` **逐行匹配**(非全文 grep),并**额外测每条声明的路径是否仍在盘**。两份零涟漪结论复核成立:①把 `check-09` 纳入筛选面**不新增任何报告**(`idi-09` 与 `idi-11` 已覆盖它);②`scripts/ui-states/checking/docs/DESIGN-check-2.md` **不被任何报告覆盖**(`covered_files` 命中 0、**全文命中也为 0**)⇒ 改它不新增连带覆盖者。
- **在盘的那份报告以 HEAD 内容重新验证,不是刷新指纹。** 12 条承重真值在当前 HEAD 上逐条重立;`covered_files` **16 条一条未删**。

## Task Commits

Each task was committed atomically:

1. **Task 1: 五条浏览器门 + 两探针在最终态复跑落盘** - `e701062` (docs)
2. **Task 2: 四静态门 + pytest 基线 + `node --check` 复跑落盘** - `40db421` (docs)
3. **Task 3: `idi-11-VERIFICATION.md` 以 HEAD 内容重新验证(第三轮)** - `3a0b7f2` (docs)

**Plan metadata:** (this SUMMARY + STATE/ROADMAP) — see final commit.

## Files Created/Modified

- `.planning/phases/idi-12-g1-band/gate-logs/idi-12-03/*.log`(13 份)- 原始门禁输出 + 每份一行 `rc=`:`check-01-token-conformance` / `check-02-contrast` / `check-03-hidden-uniqueness` / `check-04-important-count` / `check-05-ui-uat` / `check-06-idi05-validation` / `check-07-idi08-validation` / `check-09-idi09-validation` / `check-10-idi10-validation` / `node-check-app-js` / `probe-05-resolve-color` / `probe-07-focus-composite` / `pytest`
- `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md` - 新增第三轮 `content_reverification` frontmatter 段 + 同名正文段;`covered_digest` 与 `verified` 更新

**本计划对 `frontend/**` / `backend/**` / 任何门脚本的净 diff 为零**(波次 1 的产物已提交,`git status --porcelain -- frontend/ scripts/ backend/ ':(exclude)scripts/.check09-old.py'` 为空)。

## 逐份连带指纹表(12 行,磁盘实测)

筛选面 = 本阶段全部改动文件(`frontend/style.css` + `scripts/check-09-idi09-validation.py` + `scripts/ui-states/checking/docs/DESIGN-check-2.md`)。对 `.planning/` 下全部 `*VERIFICATION.md` / `*VALIDATION.md`(**共 17 份**)解析 frontmatter 的 `covered_files` 并逐行匹配,另测每条声明路径是否在盘。

| # | 报告 | 命中的改动文件 | covered_files | 路径缺失 | 归档/在盘 | 处置 |
|---|------|----------------|---------------|----------|-----------|------|
| 1 | `.planning/milestones/v1.13-phases/idi-01-1-2/01-VERIFICATION.md` | `frontend/style.css` | 41 | 12 | 归档 | 已知限制 |
| 2 | `.planning/milestones/v1.13-phases/idi-02-g2/02-VERIFICATION.md` | `frontend/style.css` | 26 | 11 | 归档 | 已知限制 |
| 3 | `.planning/milestones/v1.13-phases/idi-03-g3/03-VERIFICATION.md` | `frontend/style.css` | 31 | 13 | 归档 | 已知限制 |
| 4 | `.planning/milestones/v1.14-phases/idi-04-tokens-contract/idi-04-VERIFICATION.md` | `frontend/style.css` | 13 | 8 | 归档 | 已知限制 |
| 5 | `.planning/milestones/v1.14-phases/idi-04.1-radix/idi-04.1-VERIFICATION.md` | `frontend/style.css` | 12 | 8 | 归档 | 已知限制 |
| 6 | `.planning/milestones/v1.14-phases/idi-05-typography-and-visual-hierarchy/idi-05-VERIFICATION.md` | `frontend/style.css` | 11 | 8 | 归档 | 已知限制 |
| 7 | `.planning/milestones/v1.14-phases/idi-06-layout-robustness/idi-06-VERIFICATION.md` | `frontend/style.css` | 10 | 8 | 归档 | 已知限制 |
| 8 | `.planning/milestones/v1.14-phases/idi-07-interaction-states-and-focus/idi-07-VERIFICATION.md` | `frontend/style.css` | 9 | 6 | 归档 | 已知限制 |
| 9 | `.planning/milestones/v1.15-phases/idi-09-card-containers/idi-09-VERIFICATION.md` | `frontend/style.css` + `scripts/check-09-idi09-validation.py` | 10 | 6 | 归档 | 已知限制 |
| 10 | `.planning/milestones/v1.15-phases/idi-10-tables-and-radius-scale/idi-10-VERIFICATION.md` | `frontend/style.css` | 11 | 9 | 归档 | 已知限制 |
| 11 | `.planning/quick/260925-iin-v1-14-ai-999-1/260925-iin-VERIFICATION.md` | `frontend/style.css` | 7 | 2 | 归档(quick) | 已知限制 |
| 12 | `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md` | `frontend/style.css` + `scripts/check-09-idi09-validation.py` | 16 | **0** | **在盘** | **以 HEAD 内容重新验证** |

**11 份归档报告逐份列名登记为已知限制**(第 1–11 行)。它们的 `covered_files` 声明的是 `.planning/phases/...`,归档后已移到 `.planning/milestones/v1XX-phases/...`(quick 那份同理)⇒ 重算返回 `null`,**fail-closed stale**。这是 **2026-09-14 登记的已知限制**:归档后的阶段报告不再被 staleness 机制消费,故记为已知限制而非回填重算。

> **未修复任何归档报告的路径。** 「修归档」超出 `G1-01` / `REG-04` 的范围;本计划对 `scripts/` 下任何门脚本与任何归档报告的净 diff 为零(`git diff --exit-code` rc=0,见下)。

## 第三轮重新验证的要点

**为什么是「重新验证」而不是「刷新指纹」:** 内容**确实变了** —— 本阶段改写了 `frontend/style.css` 与 `scripts/check-09-idi09-validation.py`,两者都在该报告的 `covered_files` 里。刷新指纹等于断言「自验证以来覆盖输入无变化」,那是假陈述;指纹的价值正在于留下这个信号。

**位移归因是实测的,不是推断的。** 以 `FINGERPRINT_VERSION=1` 算法独立复算两遍:①当前工作树 → `v1:sha256:c5d1e338…`(与 `gsd-tools query verification.fingerprint` 输出逐字相同 ⇒ 复算忠实);②**仅**把 4 个 `changed_covered_files` 换回 `fed6cab` 内容、其余 12 份不动 → `v1:sha256:9bdba54b…`,**精确复现记录中的旧 digest** ⇒ 整个位移 100% 由这 4 个文件造成,无隐藏的实质变更。

**实测的 `changed_covered_files` 是 4 个,不是计划预期的 2 个**(以实测为准):

| 文件 | 改动性质 | blob(`fed6cab` → HEAD) |
|------|----------|------------------------|
| `frontend/style.css` | **实质**(波次 1 / G1-01):`#latest-check` 的 `background` 就地改写 `var(--color-surface)` → `var(--color-surface-page)`;围栏 :126-135 承重注释就地更正(原句「controls and `#latest-check` still read as recessed」被证伪)。净 +3 行 | `b6c49280` → `6dd19801` |
| `scripts/check-09-idi09-validation.py` | **纯增量**(波次 1+2):新增 `c6`(7 条断言)+ 第四个 CLI 参数 `--g1-snapshot DIR`。`c1..c5` 的断言代码与计数逐项未变 | `c8e82ecd` → `33b7bf55` |
| `.planning/ROADMAP.md` | 记账(Phase 12 规划):Phase 12 段补 `**Plans**` 波次块 + Progress 行 `TBD \| Not started` → `2/3 \| In Progress` | `4929d1d0` → `06960869` |
| `.planning/REQUIREMENTS.md` | 记账:`G1-01` / `VIS-01` 复选框 `[ ]`→`[x]`,traceability 两行 `Pending`→`Complete` | `71387f44` → `a762e547` |

**Truth 10(变异证明)本轮重跑,不承前。** 上一轮不重跑变异的唯一理由是「判据载体 `check-09` 与 `style.css` 经哈希证明逐字节未变」。**该理由在本轮已失效** —— 两个载体都真的变了。故在**已提交的树**上重跑两条,读数与上一轮**逐字相同**:

```
变异 M1(#main-pane > section:not(:last-child) 还原为 + section { border-top })
  → item c4: FAIL  (39 条断言,21 FAIL,0 BLOCKED)   exit=1
变异 M3(#doc-panel 底色改归 var(--color-surface))
  → item c2: FAIL  (19 条断言,2 FAIL,0 BLOCKED)    exit=1
```

两次均 `git checkout -- frontend/style.css` 定向还原,`git hash-object == 6dd19801494f4f02b261884bb251247723527345`(与变异前逐字节相同);**全程未使用 `git stash`**(它跨工作树共享,本项目明令禁止)。

## 跨阶段对照(归一化后的逐行 diff)

方法:剥临时路径(`/var/folders/...` → `<TMP>`)、剥 exit marker(`[exit=N]` / `rc=N` → `<EXITMARK>`)、剥 pytest 的耗时数字,再与 Phase 11 收口日志(`gate-logs/idi-11-05/`)逐行 diff。**不取「结论块看着一样」** —— 这个粒度才捞得出计划未点名的读数位移。

| 门 | 与 Phase 11 的差异 | 处置 |
|----|-------------------|------|
| `check-06` / `check-07` / `check-10` / `probe-05` / `probe-07` | **零位移**(仅尾部空行/exit marker 形态差异) | 一致 |
| `check-01` / `check-03` / `check-04` / `pytest` / `node --check` | **零位移** | 一致 |
| `check-02` | **零位移**(57 行仅尾部空行差异)⇒ 零新增 PAIR、零阈值改动、`ORDER` 逐字不变 | 一致 |
| `check-09` | ①新增 `c6` 块(Phase 12 的产物);②`c4 [checking]` 的 `#ai-panel:top` 由 **395.91 → 429.00**(+33.09px) | 见下 |
| `check-05` | ①4 处行号锚点 +4;②`item10 [checking]` 的 Tab 序列新增 `#latest-check` 一个停靠点;③`SC1` 探针的首个控件身份由 `#btn-abort` 变为 `#btn-continue-check` | 见下 |

**(1)`check-05` 的行号位移 +4 及其分解。** `max-height: 30vh;` 1651→1655、`:focus-visible` 规则块 1847→1851、`@media` 2034→2038,三处一致 +4:

- **+1** 来自 `1ec75c6`(Phase 11 收口**之后**的一笔特异性注释更正 `1-1-2 → 1-1-1`,该日志快照时尚未发生);
- **+3** 来自 `39bce0b`(波次 1 的围栏承重注释就地改写,净 +3 行,全部位于这些锚点**之前**)。

两者都是**在其之前插入行**,不是重排 —— 规则体本身逐字未动。

**(2)`check-09 c4 [checking]` 的 `#ai-panel:top` +33.09px。** 成因实测:`#latest-check` 是 `max-height: 30vh` 的滚动区。波次 1 给 `checking` fixture 补上 `## 问题分级` 表后,其 `scrollHeight` 由 **235px(不溢出)变为 383px(> clientHeight 268px)** ⇒ 它从「收缩到内容高」变为「顶到 `max-height` 上限」,把其后的 `#ai-panel` 推下 **33.09px**(235 → 268 = +33)。**这是 fixture 忠于后端文法的直接后果**(D-12-5),不是布局缺陷。

**(3)计划未点名的读数位移:`#latest-check` 新增一个 Tab 停靠点。** `check-05 --item 10` 的**原始 Tab 驱动**在 `checking` 样本上多出 `#latest-check` 一站(`outlineWidth: 1px, outlineColor: rgb(0, 95, 204)` —— 那是 **UA 默认环**,不是本项目的 `--color-focus`)。成因已实测钉死:该元素 `overflow-y: auto` 且补表后**内容溢出**(`scrollHeight 383 > clientHeight 268`)⇒ Chrome 把可滚动容器暴露为键盘可聚焦。对照实测:注入 Phase 11 的旧报告正文后 `scrollHeight == clientHeight == 235`(**不溢出**),该站不存在。

下游效应:`_IDI07_TAB_LIMIT` 是**固定次数**的 Tab 驱动,循环体由 10 站变 11 站 ⇒ 37 次后落点由 `#btn-ping` 变为 `#latest-check`(37 mod 10 = 7 vs 37 mod 11 = 4),`SC1` 探针从该落点再 Tab 一次,故首个控件身份由 `#btn-abort` 变为 `#btn-continue-check`。**三条断言读数完全相同**(2px / 2px / `rgb(31, 99, 189)`),`item 10` **PASS(42 条,0 FAIL,0 BLOCKED)**。

> **登记(非门失败,非本计划可处置):** `item 10` 的**元素普查**是固定选择器清单(29 个元素),`#latest-check` 不在其中 ⇒ 该门对它**结构性地失明**。该站是 fixture 改动(波次 1)的连带效应,而 fixture 现在是忠于后端文法的;本计划 `files_modified` 不含任何产品源码与门脚本,故**只登记不处置**。

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] 计划 Task 3 的 verify 锚点 `^  re_verification:` 不可满足**

- **Found during:** Task 3(连带指纹处置)
- **Issue:** 计划的 `<verify>` 断言 `grep -c '^  re_verification:'` 应为 `1`,但被验证报告的 `re_verification:` 键在 frontmatter 里位于**第 0 列**(`idi-11-VERIFICATION.md:26`),不带两空格缩进 ⇒ 该锚点在**任何正确产物上都恒为 0**,是一条无法通过的门(本项目已登记的同族陷阱:判据的锚点须可满足且有判别力)。
- **Fix:** 取该断言的**意图** —— 「`re_verification` 段存在且**不被重复声明**」 —— 用与文件实际形态一致的第 0 列锚 `^re_verification:` 复核,实测 **1**(`grep -c 're_verification:'` 亦为 1 ⇒ 无重复段)。这与计划自身对 `covered_digest` 用的就是第 0 列锚 `^covered_digest:` 一致。
- **Files modified:** 无(纯判据侧更正,产物形状未迁就错误锚点)
- **Verification:** `grep -c '^re_verification:' idi-11-VERIFICATION.md` → `1`;`grep -c '^covered_digest:'` → `1`;`grep -c '^  - frontend/style.css$'` → `1`;YAML 经 `gsd-tools query verification.status` 解析 → `status: passed`
- **Committed in:** `3a0b7f2`(Task 3 提交内)

**2. [Rule 1 - Bug] 计划 Task 3 预期的作废份数是 2 个文件,实测为 4 个**

- **Found during:** Task 3
- **Issue:** 计划的 action 与 must_haves 只点名 `frontend/style.css` 与 `scripts/check-09-idi09-validation.py` 会作废该报告;磁盘实测发现 `.planning/ROADMAP.md` 与 `.planning/REQUIREMENTS.md`(都在其 `covered_files` 里)**也在 `fed6cab..HEAD` 区间内被合法改写**(Phase 12 规划记账)。计划自己写明「若实测与预期不符,**以实测为准**并把差异写进 SUMMARY」。
- **Fix:** 按实测登记 **4** 个 `changed_covered_files` 并逐条给出归因;位移归因证明以「仅把这 4 份换回 `fed6cab` 内容即精确复现旧 digest」承担,故**未漏报任何位移来源**。
- **Files modified:** `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md`
- **Verification:** `git diff --name-only fed6cab..HEAD` 与 16 条 `covered_files` 求交集 → 恰 4 个;复算 digest 两次分别得 `c5d1e338…`(当前)与 `9bdba54b…`(回退这 4 份)
- **Committed in:** `3a0b7f2`

---

**Total deviations:** 2 auto-fixed(2 × Rule 1)。
**Impact on plan:** 均为**判据/记账侧的诚实更正**,未改动任何产品源码、门脚本或断言强度;计划的交付面(13 份日志 + 1 份重新验证的报告 + 11 份登记)全部按原意交付。

## Issues Encountered

- **`git stash` 全程未使用。** 两处临时变异均以定向 `git checkout -- frontend/style.css` 还原,并以 `git hash-object` 逐字节复核(两次均 == `6dd19801494f4f02b261884bb251247723527345`)。
- **8765 端口存在先前遗留的 uvicorn 进程**(已登记)。五条浏览器门走的是 `ensure_server()` 的「复用,不新起、结束时也不关闭」分支 —— 读数不受影响(被测页面仍是本仓库的 `frontend/`),但该证据不是在全新进程上取得的。
- **`.planning/config.json` 与 `.planning/state.json` 在本计划开始时即为 modified 状态**(会话开始前的既存改动),**不属于本计划**,未纳入任何任务提交。

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

**Phase 12(本计划的收口对象)的剩余动作(留给编排器,不在本计划内执行):**

- ROADMAP 的 Phase 12 状态翻转 / `## Progress` 行更新是**记账写入**,会再次改写 `idi-11-VERIFICATION.md` 的 `covered_files` 之一(`.planning/ROADMAP.md`)⇒ 该报告会**再变 stale**。这是**预期内**的(按 Phase 11 先例,由记账型重新验证轮次处置),**不属本计划的缺口**。
- 核盘判据取 **ROADMAP 的 `## Milestones` + `## Progress`**,**不得**从 `.planning/state.json` 的 `phases` 推、**不得**采信 `state.*` 写入动词的输出(该组动词在本仓库已复现 15 次不可信)。

**本计划只读核对的 ROADMAP 现状(未改动这两节):**

```
## Milestones
- 🚧 **v1.16 界面去卡片化 —— 连续面与发丝分隔线** — Phases 11-12 (in progress) — 12 条需求(SURF 3 / DIV 3 / REG 4 / G1 1 / VIS 1);…;Phase 12 修 G1 表头 band 并以整里程碑复跑 + 5 张截图收口

## Progress
| 11. 去卡片化与发丝分隔线 | v1.16 | 5/5 | Complete    | 2026-09-29 |
| 12. G1 表头 band 与里程碑收口 | v1.16 | 2/3 | In Progress|  |
```

> **未采信 `state.*` 写入动词的输出,未改动 `## Milestones` / `## Progress` 两节。**

**v1.16 里程碑审计不在本阶段内** —— 走 `/gsd-audit-milestone`(与 v1.15 同路径),依据是 D-12-12。

## Gate Evidence

13 份门禁原始输出的关键读数(全部从落盘日志读出,**不采信「命令退 0 所以没问题」**):

| 门 | `^FAIL` | rc | 关键读数 |
|----|---------|----|----------|
| `check-01-token-conformance` | 0 | 0 | `PASS` |
| `check-02-contrast` | 0 | 0 | `PASS: 0 failures`;`ORDER 0.363  --color-text-muted before --color-text on --color-surface`;PAIR 53 |
| `check-03-hidden-uniqueness` | 0 | 0 | `PASS`(`^\.hidden {` == 1) |
| `check-04-important-count` | 0 | 0 | `PASS`(`!important;` 声明数 == 1) |
| `check-05-ui-uat` | **0** | **2** | `item 5: BLOCKED (9 条断言,0 FAIL,2 BLOCKED)`;全日志 `^BLOCKED` 恰 2 条,均为 `--ai-smoke` 腿;`item 8: PASS (13 条)`;`item 10: PASS (42 条)` |
| `check-06-idi05-validation` | 0 | 0 | `exit=0` |
| `check-07-idi08-validation` | 0 | 0 | `exit=0` |
| `check-09-idi09-validation` | 0 | 0 | `c1 59 / c2 19 / c3 6 / c4 39 / c5 5 / c6 7`,全 PASS 0 BLOCKED |
| `check-10-idi10-validation` | 0 | 0 | `exit=0` |
| `probe-05-resolve-color` | 0 | 0 | `PROBE control-verdict=PASS`(其 `BLOCKED [mutated] … post-fix` 是**对照支**) |
| `probe-07-focus-composite` | 0 | 0 | 环 `rgb(31, 99, 189)` 2px;合成地面白、比值 `3.54` |
| `pytest` | — | 0 | `219 passed, 6 skipped, 1 warning` |
| `node-check-app-js` | — | 0 | 无输出、通过 |

## Self-Check: PASSED

- 13 份门禁日志在盘(`.planning/phases/idi-12-g1-band/gate-logs/idi-12-03/`),每份恰一行 `rc=`:FOUND
- 五条浏览器门 + 两探针的行首 verdict 缺陷计数全为 `0`:FOUND
- `check-05` 的 `rc=2` 成因仅 item 5 两条 `--ai-smoke` 腿:FOUND
- 三个任务提交 `e701062` / `40db421` / `3a0b7f2`:FOUND
- `idi-11-VERIFICATION.md` 的第三轮 `content_reverification` 段与更新后的 `covered_digest`(`c5d1e338…`):FOUND
- `covered_files` 16 条一条未删(含 `frontend/style.css` 与 `scripts/check-09-idi09-validation.py`):FOUND
- 12 行连带指纹表在盘,11 份归档报告逐份列名登记为已知限制:FOUND
- 产品源码与门脚本零改动;`git status` 对 `frontend/` `scripts/` `backend/` 为空:FOUND
- 变异 M1 与 M3 各自产生非零的不通过断言计数(21 / 2),还原后 `git hash-object` 逐字节相同:FOUND

---
*Phase: idi-12-g1-band*
*Completed: 2026-09-29*

---
phase: idi-04.1-radix
plan: 02
subsystem: scripts
tags: [guard-hardening, mutation-testing, token-conformance, wcag-contrast, vacuous-guard]

# Dependency graph
requires:
  - phase: idi-04.1-radix
    plan: 01
    provides: "围栏值层 Radix 重写落地:25 个 `--radix-<family>-<step>` tier-1 名、43 对(34 TEXT + 9 NON-TEXT)+ 1 ORDER 清单、`check-02-contrast.py` 在真实树上 `PASS: 0 failures`"
provides:
  - "CHECK-01 的 tier-1 隐私半场重新可机械查:交替式含 `radix`,对 `var(--radix-…` 泄漏会 FAIL 并非零退出"
  - "「旧交替式会静默空转」的对照证据(同一份注入泄漏样本上旧守卫打印 PASS / exit 0)"
  - "check-02-contrast.py 四条硬失败路径在 43 对清单上的逐条复证(未知名 / 标记数 / 覆盖率下限 / ORDER 反转)"
affects: [idi-04.1-03, phase-5-visual, phase-6, phase-7-focus-ring]

actuals:
  tokens: 259       # chars/4 over the realized diff (1035 chars) — same scale as the plan's estimate.tokens
  tasks: 2
  commits: 1        # MEASURED: git rev-list --count f4b731b..HEAD
  plan_head_before: f4b731bbf53e6eb11b31c7f890b2125ffe85f8b5

tech-stack:
  added: []
  patterns:
    - "变异测试一律在 `mktemp -d` 临时仓库根上进行;真实工作树是被验证对象,不得被污染"
    - "守卫加固必须配「旧守卫会空转」的对照证据 —— 证明修复不是修辞"

key-files:
  created: []
  modified:
    - scripts/check-01-token-conformance.sh

key-decisions:
  - "tier-1 交替式加宽为 `(white|black|gray|green|blue|amber|red|purple|radix)`,其余各行逐字未动 —— 只改一处正则,不放宽任何断言"
  - "注释用散文说明「新增了 radix 这一支」,不逐字抄写交替式本身 —— 门按 `grep -c` 计数该交替式,抄一遍会让计数变成 2"
  - "check-02-contrast.py 代码 delta 为零,故本任务无独立提交 —— 残留扫描与四条变异复证即为验收(沿 Phase 4 idi-04-03 先例)"
  - "全部八次变异运行在 `mktemp -d` 临时根上完成;`frontend/style.css` 在变异前后逐字节一致"

patterns-established:
  - "空转对照(vacuity control):修复守卫时,用 `sed` 从新守卫重建旧守卫并对同一注入样本跑它 —— 旧守卫打印 PASS 是修复必要性的直接证据,而非自陈"

requirements-completed: [CHECK-01, TOKEN-02, CHECK-03, CHECK-04]

coverage:
  - id: D1
    description: "CHECK-01 tier-1 隐私半场在 D-03 改名后重新可机械查;对围栏外 `var(--radix-gray-11)` 泄漏非零退出并打印具名诊断"
    requirement: "TOKEN-02"
    verification:
      - kind: unit
        ref: "bash scripts/check-01-token-conformance.sh (真实树 exit=0 PASS)"
        status: pass
      - kind: mutation
        ref: "mktemp 副本 + 注入 `var(--radix-gray-11)` → FAIL: 1 tier-1 primitive reference(s) outside the fence / exit=1"
        status: pass
    human_judgment: false
  - id: D2
    description: "空转被实证:同一份注入样本上,`sed 's/|radix//'` 重建的旧守卫打印 PASS 且 exit=0"
    requirement: "CHECK-01"
    verification:
      - kind: mutation
        ref: "mktemp 副本 + sed 重建旧守卫 + 同一注入样本 → PASS / exit=0"
        status: pass
    human_judgment: false
  - id: D3
    description: "裸 hex 半场与围栏成对断言未被削弱"
    requirement: "CHECK-01"
    verification:
      - kind: mutation
        ref: "注入 `#abc` → FAIL: 1 bare hex outside the token block / exit=1;删 END 标记 → FAIL: expected exactly 1 fence START and 1 fence END, found 1/0 / exit=1"
        status: pass
    human_judgment: false
  - id: D4
    description: "check-02-contrast.py 四条硬失败路径在 43 对清单上逐一仍会失败"
    requirement: "CHECK-03"
    verification:
      - kind: mutation
        ref: "未知名 → FAIL: unknown token --color-text-typo;标记数 → FAIL: 44 '/* PAIR' markers but only 43 parsed;覆盖率 → FAIL: manifest coverage 10 pairs (10 TEXT / 0 NON-TEXT) below floor 24/20/4;ORDER 反转 → FAIL: hierarchy inverted 2.753。四条均 exit=1"
        status: pass
      - kind: unit
        ref: "无变异临时副本 → 末行 PASS: 0 failures / exit=0"
        status: pass
    human_judgment: false

# Metrics
duration: 2min
completed: 2026-09-19
status: complete
---

# Phase 04.1 Plan 02: CHECK-01 tier-1 守卫加固 + check-02 四条硬失败路径复证 Summary

**把 CHECK-01 的 tier-1 隐私不变量从「D-03 改名后会静默空转」修回「真的会失败」—— 交替式加一个 `radix` 分支(一处正则,五行注释),并用八次临时副本上的变异运行证明它,其中「旧交替式对同一泄漏样本打印 PASS」是本次修复的全部理由。**

## Performance

- **Duration:** 2 min
- **Started:** 2026-09-19T13:15:13Z
- **Completed:** 2026-09-19T13:17:22Z
- **Tasks:** 2 / 2
- **Files modified:** 1(`scripts/check-01-token-conformance.sh`)

## Accomplishments

- **T-idi041-05 消解。** `scripts/check-01-token-conformance.sh` 的 tier-1 交替式由 `(white|black|gray|green|blue|amber|red|purple)` 加宽为 `(white|black|gray|green|blue|amber|red|purple|radix)`。D-03 把 tier-1 名改成 `--radix-<family>-<step>` 之后,旧交替式对 `var(--radix-…` 不匹配,TOKEN-02 的硬不变量变成无人看守的断言而 CHECK-01 仍打印 `PASS` —— 这正是本项目有明确记忆的失败类(守卫静默空转)。
- **空转被实证,而非被假设。** 同一份注入 `var(--radix-gray-11)` 的样式表:新守卫 `FAIL … exit=1`,用 `sed 's/|radix//'` 重建的旧守卫 `PASS … exit=0`。对照成立。
- **零削弱。** 裸 hex 半场(`FAIL: 1 bare hex outside the token block`)、围栏成对断言(`FAIL: expected exactly 1 fence START and 1 fence END, found 1/0`)在变异下均仍非零退出;`set -euo pipefail`、`cd "$(dirname "$0")/.."`、`echo "PASS"; exit 0` 逐字保留。
- **check-02 四条硬失败路径在 43 对清单上全部复证。** 未知名 / 标记数与解析数不匹配 / 覆盖率低于 24/20/4 下限 / ORDER 关系反转,四条各自 exit=1 并给出具名诊断;无变异副本上末行 `PASS: 0 failures` / exit=0。
- **零依赖、只读契约未变。** `check-02-contrast.py` 的 import 集合仍恰为 `['re', 'sys']`;`check-01` 仍只用 bash 内建 + `grep`/`awk`/`wc`/`printf`(文件内 `tail` 一词只出现在 L23 的散文注释里)。

## Task Commits

1. **Task 1: CHECK-01 的 tier-1 交替式加宽到覆盖 `radix`** - `ecae6cb` (fix)
2. **Task 2: 复证 check-02 四条硬失败路径** - 无独立提交(代码 delta 为零,见下)

**Plan metadata:** (docs: complete plan — 本 SUMMARY 的提交)

## Files Created/Modified

- `scripts/check-01-token-conformance.sh` — tier-1 交替式新增 `radix` 分支(+1 行改动),其上方补 4 行散文注释说明空转机制与加宽理由(+5 / −1)

## Decisions Made

- **只改一处正则。** 计划与 `<prohibitions>` 都要求裸 hex 半场、围栏成对断言、tier-1 泄漏半场三者必须保留且必须仍会失败。本次 diff 是 `+5 / −1`:`−1` 是被替换的旧交替式行,`+5` 是 4 行注释 + 1 行新交替式。无其他行被触碰。
- **注释不逐字抄写交替式。** 门 `grep -c 'white|black|gray|green|blue|amber|red|purple|radix'` 必须等于 1;若注释里再抄一遍完整列举,计数会变成 2 而门变红。注释改以散文说明「新增了 `radix` 这一支」并点出 `--radix-<family>-<step>` 形态。
- **Task 2 无独立提交。** 它的 `<files>` 是 `scripts/check-02-contrast.py`,而计划明写「期望代码 delta 为零」。纯注入→观察→还原、净 diff 为零,故无物可提交;残留扫描(`git status --porcelain -- scripts/check-02-contrast.py` 为空)与四条变异复证即为验收。沿 `idi-04-03` 的既有先例(STATE.md:「Task 2 为纯注入→观察→还原,净 diff 为零,故无独立提交」)。

## Deviations from Plan

None - plan executed exactly as written.

两条执行期观察(不是偏离,记录以免被误读为缺陷):

1. **计划的工作树范围门在本次执行中列出 `.planning/config.json`(动手前既有状态)。** 计划给出的排除项是 `.claude/settings.local.json` 与 `idi-04.1-DISCUSS-CHECKPOINT.json`,但本会话起始的 git status 快照显示被改的是 `.claude/settings.local.json` 与 `.planning/config.json`;`idi-04.1-DISCUSS-CHECKPOINT.json` 在本次执行中是干净的(已跟踪且无改动)。`.planning/config.json` 的改动是编排器在本计划动手前写入的,与 Plan 01 SUMMARY 记录的同类既有工作树状态同源。**本计划未把任何 `.planning/*` 或 `.claude/*` 文件纳入任何一次提交**;Task 1 的提交 `ecae6cb` 的 `--numstat` 只有 `scripts/check-01-token-conformance.sh` 一个文件。
2. **一次探针误用(已自纠,非缺陷)。** 首轮跑守卫套件时把 `check-02-contrast.py` 交给了 `bash` 而不是 `python3`,于是 bash 试图执行 Python 源码并打印一串 `command not found`。这正是本项目记忆里的「先怀疑自己的探针」:逐字用正确解释器复测后,四条守卫全部 `PASS` / exit=0。真实结果见下方证据表。

## Verification Evidence

### Task 1 — CHECK-01 四次变异运行(全部在 `mktemp -d` 临时仓库根上)

| # | 变异 | 命令 | 逐字输出 | 退出码 |
|---|---|---|---|---|
| 1 | tier-1 泄漏(新守卫) | `tmp=$(mktemp -d) && mkdir -p "$tmp/scripts" "$tmp/frontend" && cp scripts/check-01-token-conformance.sh "$tmp/scripts/" && cp frontend/style.css "$tmp/frontend/" && printf '\n.leak { color: var(--radix-gray-11); }\n' >> "$tmp/frontend/style.css" && bash "$tmp/scripts/check-01-token-conformance.sh"` | `FAIL: 1 tier-1 primitive reference(s) outside the fence` | **1** |
| 2 | 空转对照(旧守卫,同一注入样本) | `tmp2=$(mktemp -d) && mkdir -p "$tmp2/scripts" "$tmp2/frontend" && sed 's/\|radix//' scripts/check-01-token-conformance.sh > "$tmp2/scripts/old.sh" && cp frontend/style.css "$tmp2/frontend/" && printf '\n.leak { color: var(--radix-gray-11); }\n' >> "$tmp2/frontend/style.css" && bash "$tmp2/scripts/old.sh"` | `PASS` | **0** |
| 3 | 裸 hex | `…cp frontend/style.css "$tmp/frontend/" && printf '\n.leak { color: #abc; }\n' >> "$tmp/frontend/style.css" && bash "$tmp/scripts/check-01-token-conformance.sh"` | `FAIL: 1 bare hex outside the token block` | **1** |
| 4 | 围栏成对 | `…grep -v '===== DESIGN TOKENS: END' frontend/style.css > "$tmp/frontend/style.css" && bash "$tmp/scripts/check-01-token-conformance.sh"` | `FAIL: expected exactly 1 fence START and 1 fence END, found 1/0` | **1** |

**第 2 行是本次修复的全部理由。** 同一份被注入泄漏的样式表,旧交替式打印 `PASS` 且退出码 0 —— D-03 改名后旧守卫确实停止守卫。这不是推论,是实测。

静态门:

| 门 | 命令 | 结果 |
|---|---|---|
| 交替式计数 | `grep -c 'white\|black\|gray\|green\|blue\|amber\|red\|purple\|radix' scripts/check-01-token-conformance.sh` | `1` |
| 新交替式匹配泄漏 | `printf 'var(--radix-gray-11' \| grep -cE 'var\(--(white\|black\|gray\|green\|blue\|amber\|red\|purple\|radix)(-[0-9]+)?'` | `1` |
| 真实树 | `bash scripts/check-01-token-conformance.sh` | `PASS` / exit 0 |
| 改动面 | `git diff --numstat HEAD~1 HEAD` | `5 1 scripts/check-01-token-conformance.sh`(单文件) |
| 删除文件 | `git diff --diff-filter=D --name-only HEAD~1 HEAD` | 空 |

### Task 2 — check-02 五次运行(全部在 `mktemp -d` 临时仓库根上,`cd "$tmp"` 后跑)

| # | 变异 | 命令 | 逐字输出 | 退出码 |
|---|---|---|---|---|
| 0 | 无(正向基线) | `cp scripts/check-02-contrast.py "$tmp/scripts/" && cp frontend/style.css "$tmp/frontend/" && (cd "$tmp" && python3 scripts/check-02-contrast.py)` | 末行 `PASS: 0 failures` | **0** |
| 1 | 未声明令牌名 | `awk '/^[[:space:]]*\/\* PAIR / && !d { sub(/--[a-z0-9-]+/, "--color-text-typo"); d=1 } { print }' frontend/style.css > "$tmp/frontend/style.css"` | `FAIL: unknown token --color-text-typo` | **1** |
| 2 | 标记数不匹配 | `awk '{ print } /^[[:space:]]*\/\* PAIR / && !d { print "  /* PAIR --color-text ON --color-surface TEXT"; d=1 }' frontend/style.css > "$tmp/frontend/style.css"` | `FAIL: 44 '/* PAIR' markers but only 43 parsed — malformed manifest entry` | **1** |
| 3 | 覆盖率下限 | `awk '/^[[:space:]]*\/\* PAIR / { n++; if (n > 10) next } { print }' frontend/style.css > "$tmp/frontend/style.css"` | `FAIL: manifest coverage 10 pairs (10 TEXT / 0 NON-TEXT) below floor 24/20/4` | **1** |
| 4 | ORDER 反转 | `sed -E 's#(/\* ORDER )([^ ]+) BEFORE ([^ ]+)#\1\3 BEFORE \2#' frontend/style.css > "$tmp/frontend/style.css"` | `FAIL: hierarchy inverted  2.753  --color-text not before --color-text-muted on --color-surface  (need < 1.000)` + `FAIL: 1 failures` | **1** |

**平台纪律已遵守:** 本机是 darwin,BSD `sed` 不支持 `0,/re/` 地址;全部变异一律用 `awk` 或 `sed -E` 完成,且不写死任何具体令牌名或清单条目 —— 变异目标由「第一条 `/* PAIR */` 条目」「ORDER 行的两个操作数」这类结构性位置确定,故与清单规模/内容无关。

**正向基线为何成立:** 因为它依赖 Plan 01。在 HEAD(`f4b731b` 之前的世界)同一命令打印 `FAIL: 14 failures`;Plan 01 把清单重算为 43 对后才是 `PASS: 0 failures`。同一个未变异的输入上守卫必须绿,四条变异才是在测那条守卫。

| 门 | 命令 | 结果 |
|---|---|---|
| 代码 delta 为零 | `git status --porcelain -- scripts/check-02-contrast.py` | 空 |
| 零依赖 | `python3 -c "import ast; …"` | `['re', 'sys']` |

### 真实工作树(未被变异污染)

| 门 | 命令 | 结果 |
|---|---|---|
| CHECK-01 | `bash scripts/check-01-token-conformance.sh` | `PASS` / exit 0 |
| CHECK-02 | `python3 scripts/check-02-contrast.py` | `PASS: 0 failures` / exit 0 |
| CHECK-03 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` / exit 0 |
| CHECK-04 | `bash scripts/check-04-important-count.sh` | `PASS` / exit 0 |
| 样式表逐字节未变 | `git diff --exit-code -- frontend/style.css` | exit 0 |
| 围栏清单规模 | `grep -c '/\* PAIR '` / `grep -c '/\* ORDER '` | `43` / `1` |
| 禁止面 | `git diff --exit-code -- frontend/app.js frontend/index.html` | 干净 |
| vendor | `ls frontend/vendor/` | `marked.min.js`(唯一文件) |
| 未跟踪 | `git status --porcelain` | 仅 `.claude/settings.local.json` / `.planning/config.json`(二者动手前既有,非本计划产出) |

## Threat Surface Scan

| Threat ID | Disposition | 处置结果 |
|---|---|---|
| T-idi041-05(篡改:tier-1 交替式) | mitigate | **已消解。** 交替式加宽到含 `radix`;并以变异测试证明「有泄漏时会 FAIL」与「旧交替式会 PASS」—— 空转被实证而非被假设 |
| T-idi041-06(篡改:变异误改真实工作树) | mitigate | **已消解。** 全部八次变异在 `mktemp -d` 临时根上进行;`git diff --exit-code -- frontend/style.css` 为空,`git status --porcelain` 无新增未跟踪文件 |
| T-idi041-07(否认:守卫被断言而非被证明) | mitigate | **已消解。** 每条守卫断言都配一条变异运行;「旧交替式打印 PASS」的对照证据即修复理由的直接证明 |
| T-idi041-08(信息泄露:守卫读取内容) | accept | 未变:两个脚本仍只读仓库内 `frontend/style.css` |
| T-idi041-SC(供应链) | accept | 未变:未安装任何包;两个守卫仍零依赖 |

## Known Stubs

None. 本计划只改一处 shell 正则 + 补四行注释,并全部以只读变异测试复证;无 UI 数据源、无占位文案、无未接线代码。

## Threat Flags

None. 未引入计划 `<threat_model>` 之外的任何新面 —— 无网络端点、无认证路径、无新文件、无新依赖、无写文件行为。改动仅为一个 `grep -oE` 的备选分支。

## Next Phase Readiness

- **Plan 03(wave 3)就绪。** 它收口 `scripts/check-05-ui-uat.py` 的其余硬编码 rgb 断言(D-14)与完整携带项 #9 运行时清单(`.hint` / `#btn-authorize` / `#ai-route-select` / `#selection-menu` / `.kind-write .event-kind` 等)。本计划未触碰 `check-05-ui-uat.py`,Plan 01 守住的那条「`rgba(0, 0, 0, 0.2)` 全文件计数 == 1」不变量原样有效。
- **TOKEN-02 的机械防线现在与它的声明同强。** Plan 01 以「围栏外 `comm -23` 未解析 var() 为空」+ 逐条人工复核作为过渡证据,并显式记明守卫尚未加固;本计划把这条过渡证据换成了一条真的会失败的守卫。后续阶段(5/6/7)若在围栏外引入 `var(--radix-…)`,CHECK-01 会立刻红。
- **留给 verify-work 的人工项未变。** UI-SPEC 的 28 条 backstop 仍由 Plan 01 的 coverage `D6` 标为 `human_judgment: true`,不得静默通过。
- **Phase 7 的注意项(沿自 UI-SPEC 携带项 #8):** 焦点环 `--color-focus: #1f63bd` 必须针对新的底色(`--color-surface` `#f9f9f9`、`--color-surface-page` `#fcfcfc`)重测,不能再对着旧的 `#fafafa`。

## Self-Check: PASSED

---
*Phase: idi-04.1-radix*
*Completed: 2026-09-19*
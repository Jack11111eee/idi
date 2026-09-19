---
phase: idi-04.1-radix
plan: 02
type: execute
wave: 1
depends_on: []
files_modified:
  - scripts/check-01-token-conformance.sh
autonomous: true
requirements:
  - CHECK-01
  - TOKEN-02
  - CHECK-03
  - CHECK-04

estimate:
  tokens: 42000
  raw_tokens: 42000
  tasks: 2
  confidence: low

must_haves:
  truths:
    - "`scripts/check-01-token-conformance.sh` 的 tier-1 隐私交替式覆盖 `radix`:`var(--radix-gray-11` 出现在围栏外时,守卫打印 `FAIL: ... tier-1 primitive reference(s) outside the fence` 并以非零码退出,而不是静默打印 `PASS` ← TOKEN-02 / D-03"
    - "空转被实证:同一份被注入泄漏的 `frontend/style.css`,在去掉 `|radix` 的旧交替式下打印 `PASS` 且退出码 0 —— 即 D-03 改名后旧守卫确实停止守卫。这条对照证据必须出现在 SUMMARY 里 ← TOKEN-02 / 本项目已记录的「守卫静默空转」失败类"
    - "裸 hex 半场未被削弱:围栏外注入 `#abc` 后守卫仍以非零码退出并打印 `FAIL: N bare hex outside the token block`"
    - "围栏标记成对断言未被削弱:删掉 END 标记后守卫仍以非零码退出(而不是把整段尾巴算作「围栏内」而空转)"
    - "`scripts/check-02-contrast.py` 在重算后的 43 对清单上仍保有全部四条硬失败路径:未声明令牌名、`/* PAIR` 标记数与解析数不匹配、覆盖率低于 24/20/4 下限、ORDER 关系反转。四条各自以非零码退出并给出具名诊断 ← CHECK-02 / 携带项 #2"
    - "两个守卫脚本仍是零依赖、只读:`check-01` 只用 bash 内建 + `grep`/`awk`/`wc`/`printf`;`check-02` 只 `import re, sys`。本计划不新增任何依赖,也不让它们写任何文件 ← 硬规则 6"
    - "`scripts/check-01-token-conformance.sh` 的改动只有交替式一处 —— 裸 hex 半场、围栏成对断言、`set -euo pipefail`、`cd \"$(dirname \"$0\")/..\"`、`echo PASS; exit 0` 全部逐字保留"

  artifacts:
    - path: "scripts/check-01-token-conformance.sh"
      provides: "CHECK-01 双守卫:围栏外裸 hex 计数 + tier-1 primitive 泄漏计数(交替式含 radix)"
      contains: "radix"

  key_links:
    - from: "scripts/check-01-token-conformance.sh 的 tier-1 交替式"
      to: "frontend/style.css 围栏内的 `--radix-<family>-<step>` 名"
      via: "D-03 改名后 `var(--radix-…` 不再匹配旧的 `(white|black|gray|green|blue|amber|red|purple)` 前缀,守卫会空转而 CHECK-01 仍打印 PASS;加宽交替式后重新匹配"
      pattern: "white\\|black\\|gray\\|green\\|blue\\|amber\\|red\\|purple\\|radix"
    - from: "scripts/check-02-contrast.py 的覆盖率下限"
      to: "frontend/style.css 围栏内的 43 条 `/* PAIR */`"
      via: "下限 24/20/4 是「清单被截断却仍然 0 failures」的唯一机械防线;重算后的 43/34/9 必须清过它"
      pattern: "below floor 24/20/4"

  prohibitions:
    - statement: "不得放宽或删除 CHECK-01 的任何断言来「让守卫通过」—— 裸 hex 半场、围栏成对断言、tier-1 泄漏半场三者都必须保留且必须仍会失败"
      status: active
      verification: flagged
    - statement: "不得在真实 `frontend/style.css` 上做变异测试 —— 同 wave 的 `idi-04.1-01-PLAN.md` 正在编辑该文件。全部变异必须在临时副本上进行,仓库工作树在变异前后逐字节一致"
      status: active
      verification: flagged
    - statement: "不得改动 `scripts/check-02-contrast.py` 的任何守卫逻辑 —— 本阶段它在代码层的期望 delta 为零或近零(它读的清单在 `style.css` 里,不在这里)"
      status: active
      verification: flagged
    - statement: "不得给两个守卫脚本引入任何新增依赖、构建步骤或写文件行为(硬规则 6:D-06 零依赖、零构建)"
      status: active
      verification: flagged
    - statement: "不得改 `frontend/app.js` / `frontend/index.html` / `frontend/vendor/`(`vendor/` 必须仍只含 `marked.min.js`)"
      status: active
      verification: flagged
---

<objective>
把 CHECK-01 的 **tier-1 隐私不变量**从「D-03 改名后会静默空转」修回「真的会失败」,并用变异测试证明它确实会失败;同时证明重算后的 43 对清单仍保留 `check-02-contrast.py` 的全部硬失败路径。

Purpose: `scripts/check-01-token-conformance.sh:37-39` 用 `grep -oE 'var\(--(white|black|gray|green|blue|amber|red|purple)(-[0-9]+)?'` 强制 TOKEN-02(tier-1 名绝不出现在围栏外)。D-03 把 tier-1 改成 `--radix-<family>-<step>` 之后,`var(--radix-gray-11` **不再匹配**这个交替式 —— 于是这条硬不变量变成**无人看守**的断言,而 CHECK-01 会继续打印 `PASS`。这正是本项目有明确记忆的失败类(守卫静默空转),也是本阶段最容易「看起来全绿但实际没守」的地方。它必须被修好并被证明。

Output: 交替式含 `radix` 的 `scripts/check-01-token-conformance.sh`;两条守卫的变异测试证据(含「旧交替式会空转」的对照证据)写入 SUMMARY;`check-02-contrast.py` 四条硬失败路径在 43 对清单上的复证。

**为什么这是本 wave 的独立计划而不是 Plan 01 的一个任务:** `scripts/` 不在 CONTEXT.md 命名的改动集里(它只列了 `check-02-contrast.py` 与 `check-05-ui-uat.py`),所以这是一处**真实的范围问题**,不是机械编辑。它与 Plan 01 的 `frontend/style.css` 零文件重叠,故可同 wave 并行;变异测试全部在临时副本上进行,不会碰到 Plan 01 正在编辑的文件。

**本计划关闭 vs 沿用:** **关闭** CHECK-01 在 D-03 改名后失效的那一半(守卫加固 + 变异证明);**沿用/复证** TOKEN-02、CHECK-03、CHECK-04。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/idi-04.1-radix/idi-04.1-CONTEXT.md
@.planning/phases/idi-04.1-radix/idi-04.1-PATTERNS.md
@.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md
@scripts/check-01-token-conformance.sh
@scripts/check-02-contrast.py
</context>

<tasks>

<task type="auto">
  <name>Task 1: CHECK-01 的 tier-1 交替式加宽到覆盖 `radix`,并证明它真的会失败</name>
  <files>scripts/check-01-token-conformance.sh</files>
  <read_first>
    - `scripts/check-01-token-conformance.sh` 全文(46 行)—— 特别是 L35-L43 的 tier-1 泄漏半场、L22-L33 的裸 hex 半场、L13-L20 的围栏成对断言、L5-L11 的 `set -euo pipefail` / `cd` / 文件存在断言
    - `.planning/phases/idi-04.1-radix/idi-04.1-PATTERNS.md` §`Tier-1 privacy — and a guard that will go vacuous (FLAG for the planner)` —— 空转的机制与「要么加宽交替式,要么记录为什么不加」的裁决要求
    - `.planning/phases/idi-04.1-radix/idi-04.1-CONTEXT.md` D-03 —— 改名到 `--radix-<family>-<step>` 的决定与「tier-1 名不得出围栏(与 TOKEN-02 硬不变量同源,机械可查)」的原文
    - `.planning/REQUIREMENTS.md` §TOKEN 的 TOKEN-02 条目 —— 「硬不变量:**primitive(tier-1)名绝不出现在 `:root` 块之外**(机械可查,与 CHECK-01 同源)」的原文
    - `.planning/phases/idi-04-tokens-contract/idi-04-UAT.md` 第 3 项的 evidence —— Phase 4 的 verifier 做过 10 次变异测试,是本仓库对「守卫必须证明会失败」的既有标准
  </read_first>
  <action>
    **唯一的改动:把 L38 的交替式加一个 `radix` 分支。** 改动后的交替式形状为
    `var\(--(white|black|gray|green|blue|amber|red|purple|radix)(-[0-9]+)?`
    —— 其余一切逐字不动:L27-L28 的裸 hex 半场、L17-L20 的围栏成对断言、L11 的文件存在断言、L5 的 `set -euo pipefail`、L6 的 `cd "$(dirname "$0")/.."`、L45 的 `echo "PASS"` / `exit 0`。

    **在 L35-L36 的既有注释里补一句说明**为什么 `radix` 在交替式里:改名前 tier-1 名是 `--gray-*` 形态,改名后是 `--radix-<family>-<step>` 形态,旧的交替式对后者不匹配,守卫会**静默空转而仍打印 PASS**;`radix` 分支正是让这条硬不变量继续可机械查的东西。注释语言沿用文件现有的英文风格。

    **变异测试(必须做,且必须在临时副本上做 —— 同 wave 的 Plan 01 正在编辑 `frontend/style.css`)。** 构造一个临时仓库根,只放守卫需要的两个路径,然后注入三种变异、每次单独跑:

    1. **tier-1 泄漏变异**:在临时副本的 `frontend/style.css` 末尾(围栏 END 之后)追加一行 `.leak { color: var(--radix-gray-11); }`。跑**新**守卫 → 必须非零退出并打印 `FAIL: 1 tier-1 primitive reference(s) outside the fence`。
    2. **空转对照**:用 `sed 's/|radix//' scripts/check-01-token-conformance.sh` 从新守卫重建一份**旧交替式**守卫,对同一份被注入泄漏的样式表跑它 → 必须打印 `PASS` 且退出码 0。这条对照证据是本次修复的全部理由,必须写进 SUMMARY。
    3. **裸 hex 变异**:另取一份干净的临时副本,在围栏 END 之后追加 `.leak { color: #abc; }`。跑新守卫 → 必须非零退出并打印 `FAIL: 1 bare hex outside the token block`。
    4. **围栏成对变异**:另取一份干净的临时副本,删掉 `/* ===== DESIGN TOKENS: END ===== */` 那一行。跑新守卫 → 必须非零退出并打印 `FAIL: expected exactly 1 fence START and 1 fence END`。

    临时副本的构造方式:守卫用 `cd "$(dirname "$0")/.."` 定位仓库根,所以只要把脚本放到 `<tmp>/scripts/`、把样式表放到 `<tmp>/frontend/` 即可从任意 cwd 运行。**每次变异后都必须确认仓库工作树逐字节未变**(`git diff --exit-code -- frontend/style.css scripts/check-01-token-conformance.sh` 之外,`git status --porcelain` 不得出现新增的未跟踪文件)。

    最后把四次运行的命令与逐字输出(含退出码)写进 SUMMARY,并明确记明「旧交替式空转」这一条。
  </action>
  <verify>
    <automated>grep -c 'white|black|gray|green|blue|amber|red|purple|radix' scripts/check-01-token-conformance.sh</automated>
    <fails_when>计数不等于 1(交替式未加宽,或被写成别的形状)</fails_when>
    <automated>printf 'var(--radix-gray-11' | grep -cE 'var\(--(white|black|gray|green|blue|amber|red|purple|radix)(-[0-9]+)?'</automated>
    <fails_when>计数不等于 1(新交替式仍然匹配不到 `--radix-*` 泄漏)</fails_when>
    <automated>tmp=$(mktemp -d) && mkdir -p "$tmp/scripts" "$tmp/frontend" && cp scripts/check-01-token-conformance.sh "$tmp/scripts/" && cp frontend/style.css "$tmp/frontend/" && printf '\n.leak { color: var(--radix-gray-11); }\n' >> "$tmp/frontend/style.css" && bash "$tmp/scripts/check-01-token-conformance.sh"; echo "exit=$?"</automated>
    <fails_when>输出不含 `FAIL: 1 tier-1 primitive reference(s) outside the fence`,或 `exit=0`(守卫在真实泄漏面前仍然空转)</fails_when>
    <automated>tmp=$(mktemp -d) && mkdir -p "$tmp/scripts" "$tmp/frontend" && sed 's/|radix//' scripts/check-01-token-conformance.sh > "$tmp/scripts/old.sh" && cp frontend/style.css "$tmp/frontend/" && printf '\n.leak { color: var(--radix-gray-11); }\n' >> "$tmp/frontend/style.css" && bash "$tmp/scripts/old.sh"; echo "exit=$?"</automated>
    <fails_when>输出不是 `PASS` 或 `exit` 不为 0 —— 若不是,说明对照不成立,本任务的修复理由未获证明</fails_when>
    <automated>tmp=$(mktemp -d) && mkdir -p "$tmp/scripts" "$tmp/frontend" && cp scripts/check-01-token-conformance.sh "$tmp/scripts/" && cp frontend/style.css "$tmp/frontend/" && printf '\n.leak { color: #abc; }\n' >> "$tmp/frontend/style.css" && bash "$tmp/scripts/check-01-token-conformance.sh"; echo "exit=$?"</automated>
    <fails_when>输出不含 `bare hex outside the token block`,或 `exit=0`(裸 hex 半场被削弱)</fails_when>
    <automated>tmp=$(mktemp -d) && mkdir -p "$tmp/scripts" "$tmp/frontend" && cp scripts/check-01-token-conformance.sh "$tmp/scripts/" && grep -v '===== DESIGN TOKENS: END' frontend/style.css > "$tmp/frontend/style.css" && bash "$tmp/scripts/check-01-token-conformance.sh"; echo "exit=$?"</automated>
    <fails_when>输出不含 `expected exactly 1 fence START and 1 fence END`,或 `exit=0`(围栏成对断言被削弱)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh</automated>
    <fails_when>任一条非零退出,或任一条 stdout 不含 `PASS`(在真实树上守卫必须仍然通过)</fails_when>
    <automated>git status --porcelain</automated>
    <fails_when>输出中出现除 `scripts/check-01-token-conformance.sh` 之外的改动路径,或出现任何未跟踪的临时文件(变异测试必须完全在 `mktemp -d` 目录内完成)</fails_when>
  </verify>
  <acceptance_criteria>
    - `scripts/check-01-token-conformance.sh` 的 tier-1 交替式恰为 `(white|black|gray|green|blue|amber|red|purple|radix)`,其余各行逐字未动
    - 对围栏外注入的 `var(--radix-gray-11)`,新守卫非零退出并打印 `FAIL: 1 tier-1 primitive reference(s) outside the fence`
    - 对**同一份**注入样本,用 `sed 's/|radix//'` 重建的旧守卫打印 `PASS` 且退出码 0 —— 空转对照成立并记入 SUMMARY
    - 围栏外注入 `#abc` 时守卫仍以非零码退出并打印裸 hex 诊断
    - 删掉 END 标记时守卫仍以非零码退出并打印围栏成对诊断
    - 在真实仓库上 `bash scripts/check-01-token-conformance.sh` 打印 `PASS` 且退出码 0
    - `git status --porcelain` 除本任务改动的脚本外无新增路径;`frontend/style.css` 的 `git diff` 为空
    - SUMMARY 中逐字记录四次变异运行的命令、输出与退出码
  </acceptance_criteria>
  <done>CHECK-01 的 tier-1 隐私半场在 D-03 改名后重新可机械查;变异测试证明它在真实泄漏面前会失败,并留下「旧交替式会空转」的对照证据;裸 hex 与围栏成对两个半场均未被削弱。</done>
</task>

<task type="auto">
  <name>Task 2: 复证 check-02-contrast.py 的四条硬失败路径在 43 对清单上仍成立</name>
  <files>scripts/check-02-contrast.py</files>
  <read_first>
    - `scripts/check-02-contrast.py` 全文(240 行)—— `read_fence` 的成对断言(L44-L69)、`resolve` 的未知名大声失败(L77-L105)、覆盖率下限(L146-L155)、raw 标记计数相等(L161-L175)、ORDER 操作数必须是已列出的普通 TEXT 对(L207-L213)、闭区间比较(L198)、退出契约(L231-L236)
    - `.planning/phases/idi-04.1-radix/idi-04.1-PATTERNS.md` §`scripts/check-02-contrast.py — the manifest parser / exit contract` —— 「期望代码 delta:零或近零」与六条必须存活的守卫
    - `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` `## Carry-Forward Obligations` 第 2 / 4 条 —— `PASS: 0 failures` 与「hex 逐字转抄,错一位就表现为一条失败配对而非静默通过」
    - `frontend/style.css` 围栏内 Task 1(Plan 01)写入的 43 条 `/* PAIR */` + 1 条 `/* ORDER */`
  </read_first>
  <action>
    **本任务对 `scripts/check-02-contrast.py` 的期望代码 delta 是零。** 它的职责是复证:在清单从 34 对重算为 43 对之后,它的四条硬失败路径**仍然各自可失败**——一条「永远返回 0」的守卫与没有守卫等价。

    全部变异在**临时仓库根**上做(脚本的 `CSS_PATH = "frontend/style.css"` 是相对路径,从 cwd 解析,所以把脚本放到 `<tmp>/scripts/`、样式表放到 `<tmp>/frontend/`、在 `<tmp>` 里跑即可)。**绝不在真实 `frontend/style.css` 上做变异**(同 wave 的 Plan 01 正在编辑它)。

    四条变异,各自单独跑并记录逐字输出与退出码:

    1. **未声明令牌名**:在临时样式表的清单块里把某一条 `/* PAIR --color-text ON --color-surface TEXT */` 的**前景**名改成一个未声明的名字(例如 `--color-text-typo`)。期望:打印 `FAIL: unknown token --color-text-typo` 并以退出码 1 结束 —— 即清单与令牌块无法漂移。
    2. **标记数不匹配**:在清单块里插入一行 `/* PAIR --color-text ON --color-surface TEXT`(**故意不闭合** `*/`)。期望:打印 `FAIL: 43 '/* PAIR' markers but only 42 parsed — malformed manifest entry`(计数以实际数字为准)并以退出码 1 结束 —— 即「条目被静默丢弃」不可能发生。
    3. **覆盖率下限**:把清单块删到只剩 10 条 `/* PAIR */`。期望:打印 `FAIL: manifest coverage 10 pairs (...) below floor 24/20/4` 并以退出码 1 结束 —— 即截断的清单不会「trivially 0 failures」。
    4. **ORDER 反转**:把 `/* ORDER --color-text-muted BEFORE --color-text ON --color-surface */` 的两个操作数对调(改成 `--color-text BEFORE --color-text-muted`)。期望:打印以 `FAIL: hierarchy inverted` 开头的行并以退出码 1 结束 —— 即层级断言不是恒真。

    另跑一条**正向基线**:在临时副本上不做任何变异,期望末行 `PASS: 0 failures` 且退出码 0(若 Plan 01 尚未落地,则如实记录当时的清单规模与结果,不得把「尚未落地」写成失败)。

    把五条运行的命令与逐字输出写进 SUMMARY,并写明 `scripts/check-02-contrast.py` 的代码 delta 为 0。
  </action>
  <verify>
    <automated>tmp=$(mktemp -d) && mkdir -p "$tmp/scripts" "$tmp/frontend" && cp scripts/check-02-contrast.py "$tmp/scripts/" && sed '0,/PAIR --color-text ON/s//PAIR --color-text-typo ON/' frontend/style.css > "$tmp/frontend/style.css" && (cd "$tmp" && python3 scripts/check-02-contrast.py); echo "exit=$?"</automated>
    <fails_when>输出不含 `FAIL: unknown token`,或 `exit=0`(未声明名不再大声失败)</fails_when>
    <automated>tmp=$(mktemp -d) && mkdir -p "$tmp/scripts" "$tmp/frontend" && cp scripts/check-02-contrast.py "$tmp/scripts/" && sed '0,/^  \/\* PAIR /s//  \/* PAIR /' frontend/style.css | sed '0,/^  \/\* PAIR --color-text ON --color-surface TEXT \*\//s//  \/* PAIR --color-text ON --color-surface TEXT/' > "$tmp/frontend/style.css" && (cd "$tmp" && python3 scripts/check-02-contrast.py); echo "exit=$?"</automated>
    <fails_when>输出不含 `markers but only`,或 `exit=0`(标记数与解析数不再比对)</fails_when>
    <automated>tmp=$(mktemp -d) && mkdir -p "$tmp/scripts" "$tmp/frontend" && cp scripts/check-02-contrast.py "$tmp/scripts/" && awk '!/^  \/\* PAIR / || n++ < 10' frontend/style.css > "$tmp/frontend/style.css" && (cd "$tmp" && python3 scripts/check-02-contrast.py); echo "exit=$?"</automated>
    <fails_when>输出不含 `below floor 24/20/4`,或 `exit=0`(覆盖率下限失效,截断的清单会 trivially 通过)</fails_when>
    <automated>tmp=$(mktemp -d) && mkdir -p "$tmp/scripts" "$tmp/frontend" && cp scripts/check-02-contrast.py "$tmp/scripts/" && sed 's/ORDER --color-text-muted BEFORE --color-text ON/ORDER --color-text BEFORE --color-text-muted ON/' frontend/style.css > "$tmp/frontend/style.css" && (cd "$tmp" && python3 scripts/check-02-contrast.py); echo "exit=$?"</automated>
    <fails_when>输出不含 `hierarchy inverted`,或 `exit=0`(ORDER 断言恒真)</fails_when>
    <automated>tmp=$(mktemp -d) && mkdir -p "$tmp/scripts" "$tmp/frontend" && cp scripts/check-02-contrast.py "$tmp/scripts/" && cp frontend/style.css "$tmp/frontend/" && (cd "$tmp" && python3 scripts/check-02-contrast.py | tail -1); echo "exit=$?"</automated>
    <fails_when>末行不是 `PASS: 0 failures`,或 `exit` 不为 0(正向基线不成立)</fails_when>
    <automated>git status --porcelain -- scripts/check-02-contrast.py; python3 -c "import ast; t=ast.parse(open('scripts/check-02-contrast.py').read()); print(sorted({n.names[0].name.split('.')[0] for n in ast.walk(t) if isinstance(n,ast.Import)} | {n.module.split('.')[0] for n in ast.walk(t) if isinstance(n,ast.ImportFrom) and n.module}))"</automated>
    <fails_when>第一条输出非空(脚本被改动,期望 delta 为零),或第二条打印的模块集合不是 `['re', 'sys']`(零依赖被破坏)</fails_when>
    <automated>git status --porcelain</automated>
    <fails_when>输出中出现除 `scripts/check-01-token-conformance.sh` 之外的改动路径,或任何未跟踪的临时文件</fails_when>
  </verify>
  <acceptance_criteria>
    - 四条变异各自以非零码退出,并分别打印 `FAIL: unknown token`、`markers but only`、`below floor 24/20/4`、`hierarchy inverted`
    - 无变异的临时副本上脚本末行 `PASS: 0 failures` 且退出码 0
    - `git status --porcelain -- scripts/check-02-contrast.py` 输出为空(代码 delta 为零)
    - `scripts/check-02-contrast.py` 的 import 集合仍恰为 `['re', 'sys']`(零依赖)
    - `git status --porcelain` 除 `scripts/check-01-token-conformance.sh` 外无改动路径,无未跟踪文件
    - SUMMARY 中逐字记录五条运行的命令、输出与退出码
  </acceptance_criteria>
  <done>check-02 的四条硬失败路径在 43 对清单上逐一被证明仍会失败;脚本代码 delta 为零;零依赖契约未变。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 守卫脚本 → 仓库工作树 | `scripts/check-01-token-conformance.sh` 与 `check-02-contrast.py` 都是**只读**的:它们不写文件、不跑 git、不联网。唯一的输入是仓库内的两个静态文件 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi041-05 | Tampering | `scripts/check-01-token-conformance.sh` 的 tier-1 交替式 | medium | mitigate | D-03 改名后旧交替式不再匹配 `var(--radix-…`,使 TOKEN-02 的硬不变量**静默空转而 CHECK-01 仍打印 PASS**。本计划加宽交替式到含 `radix`,并以变异测试证明「有泄漏时会 FAIL、旧交替式会 PASS」——空转被实证而非被假设 |
| T-idi041-06 | Tampering | 变异测试误改真实工作树 | medium | mitigate | 全部变异在 `mktemp -d` 临时仓库根上进行(脚本以 `$(dirname $0)/..` 定位根、以相对 `CSS_PATH` 解析样式表,故临时根可行);每个任务末尾以 `git status --porcelain` 断言工作树无多余改动。**不在真实 `frontend/style.css` 上变异** —— 同 wave 的 Plan 01 正在编辑它 |
| T-idi041-07 | Repudiation | 守卫被断言为「有效」而非被证明 | medium | mitigate | 每条守卫断言都配一条变异运行;「旧交替式打印 PASS」的对照证据是修复理由的直接证明,写进 SUMMARY。这正是本项目已记录的教训(变异测试是唯一能证明守卫真的会失败的手段) |
| T-idi041-08 | Information disclosure | 守卫脚本读取的内容 | none | accept | 两个脚本只读仓库内的 `frontend/style.css`,不含任何凭据、网络调用或用户数据 |
| T-idi041-SC | Tampering | npm / pip / cargo 安装 | none | accept | **本阶段不安装任何包**,且硬规则 6 要求两个守卫零依赖(`check-01` 只用 bash 内建 + `grep`/`awk`/`wc`/`printf`;`check-02` 只 `import re, sys`)。故供应链面为零 |

**诚实结论:本计划不存在 high 或 critical 级威胁。** 它只改一个 shell 脚本里的一处正则,其余全是只读的变异证明。
</threat_model>

<verification>
- `grep -c 'white|black|gray|green|blue|amber|red|purple|radix' scripts/check-01-token-conformance.sh` == 1
- 四条变异(radix 泄漏 / 裸 hex / 围栏成对 / 旧交替式对照)全部在临时副本上复现预期输出与退出码
- 四条 check-02 变异(未知名 / 标记数 / 覆盖率 / ORDER 反转)全部复现预期输出与退出码
- 真实树上 `bash scripts/check-01-token-conformance.sh` / `check-03` / `check-04` 全部 `PASS`
- `scripts/check-02-contrast.py` 的 `git status` 干净、import 集合为 `['re', 'sys']`
- `git status --porcelain` 只出现 `scripts/check-01-token-conformance.sh`
</verification>

<success_criteria>
1. CHECK-01 的 tier-1 隐私半场在 D-03 改名后重新可机械查,且被变异测试证明会失败
2. 「旧交替式会静默空转」的对照证据留档
3. 裸 hex 半场与围栏成对断言未被削弱
4. `check-02-contrast.py` 的四条硬失败路径在 43 对清单上逐一复证,代码 delta 为零
5. 两个守卫仍零依赖、只读;真实工作树未被变异污染
</success_criteria>

<artifacts_this_phase_produces>
**本计划新建的符号:**

- 交替式中的 `radix` 分支:`scripts/check-01-token-conformance.sh` 的 tier-1 正则新增一个备选(不新增文件、不新增函数、不新增依赖)
- 无新增文件、无新增脚本、无新增依赖

**删除的符号:** 无
</artifacts_this_phase_produces>

<output>
Create `.planning/phases/idi-04.1-radix/idi-04.1-02-SUMMARY.md` when done
</output>
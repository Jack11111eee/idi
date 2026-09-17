---
phase: idi-04
plan: 03
type: execute
wave: 3
depends_on:
  - idi-04-01
  - idi-04-02
files_modified:
  - frontend/style.css
  - scripts/check-02-contrast.py
autonomous: true
requirements:
  - CHECK-02
  - A11Y-04
  - A11Y-04b

estimate:
  tokens: 65000
  raw_tokens: 65000
  tasks: 2
  confidence: low

must_haves:
  truths:
    - "`scripts/check-02-contrast.py` 是零依赖的 python3(只用标准库),从 `frontend/style.css` 的 `:root` 围栏内读取**配对清单**,逐对计算 WCAG 对比度,全部达标时打印 `PASS: 0 failures` 并 `exit 0`,否则打印每个失败对与其比值并 `exit 1` ← CHECK-02 / ROADMAP Phase 4 SC5"
    - "配对清单是围栏内的一段注释清单(与令牌同处一个 diff,漂移可见),不是脚本里的硬编码 Python 字面量 —— 这是「从 :root 块派生配对」的落地形态。语法:`/* PAIR <fg-token> ON <bg-token> TEXT */`(阈值 4.5:1)与 `/* PAIR <fg-token> ON <bg-token> NON-TEXT */`(阈值 3:1);可选的 `@<alpha>` 后缀(如 `TEXT@0.8`)表示 fg 先按该 α 与 bg 合成再算比值。脚本**必须**在清单引用了不存在的令牌名时大声失败(而不是静默跳过)——这是防止清单与令牌漂移的机制"
    - "校验范围是**调和后的**范围(20 条文本对 + 4 条非文本对),不是审计报告的 4 条。文本对至少覆盖:`.hint` 的 `--color-text-muted` on `--color-surface-page`、`.badge-answered` 的 `--color-text-muted` on `--color-surface-sunken`、`.event-kind` 默认芯片的 `--color-kind-fg` on `--color-kind-default`、`#pending-count` / `.badge-pending` 的 `--color-action-warning` on `--color-surface-warning`、`.kind-command` 的 `--color-kind-fg` on `--color-kind-command`、六绿按钮的 `--color-action-*-fg` on `--color-action-*-surface`、`--color-action-primary-fg` on `--color-action-primary`、`.kind-say` 的 `--color-kind-fg` on `--color-kind-say`、`.kind-write` 的 `--color-kind-fg` on `--color-kind-write`、`.annotation-plain` 与 `.annotation-answer summary` 的 `--color-text-muted` on `--color-surface`、`.chat-user` 的 `--color-text-inverse` on `--color-surface-info-strong`、`#state-badge` 的 `--color-text-info` on `--color-surface-info`、`--color-text` / `--color-text-secondary` / `--color-text-muted` on 四个实际背景(`--gray-25` / `--white` / `--gray-50` / `--gray-100` 语义名)。非文本对 4 条:`--color-border-strong` on `--color-surface`(与 on `--gray-50`)、`--color-border-streaming` on `--gray-50`、`--color-border-success` on `--color-surface`,以及冻结轮标记 `--color-action-warning` on `--color-surface-page` ← A11Y-04 / A11Y-04b / UI-SPEC `## Contrast Verification`"
    - "`--color-text-muted` 必须在**本文件实际出现的每一个背景**上通过:`--gray-25` 5.18:1、`--white` 5.41:1、`--gray-50` 4.96:1、`--gray-100` 4.75:1 —— 四条全过。若有人把 `--gray-600` 改成 `#767676` 或 `#737373`,清单里的 `--gray-25` / `--gray-100` 两条会立刻失败(这正是脚本存在的理由)← UI-SPEC note N-1"
    - "**`opacity` 合成对被覆盖**:`.tier-desc` 的 `TEXT@0.8`(`#000` @0.8 on `--white` → 12.63:1)与归档态的 `TEXT@0.75`(`--color-text` @0.75 on `--color-surface-page` → 7.49:1)两条必须出现在清单里并通过 —— 覆盖 ≠ 失败,但**必须被覆盖**。已删除的两处(`.annotation-answered` 0.65、`.round-frozen` 0.55)不再出现在清单中,因为声明本身已消失 ← A11Y-04b / UI-SPEC `opacity` rulings 表"
    - "A11Y-04b 阈值边界(显式,脚本必须按此实现):合成逐通道在 8 位 sRGB 空间做 `round(α·fg + (1−α)·bg)`;比值 `(L_light + 0.05) / (L_dark + 0.05)`;阈值判定为**闭区间**(≥ 4.5 / ≥ 3.0 通过),**不做四舍五入到阈值** —— 4.496 判失败、4.504 判通过。此契约使 `#6a6a6a` 的 4.75 通过而 `#737373` 的 4.16 失败成为可复现的机器判定,而非人工目测 ← A11Y-04b boundary 行"
    - "A11Y-04b 精度契约(显式):WCAG 相对亮度 `L = 0.2126R + 0.7152G + 0.0722B`,通道先做 sRGB 反伽马(`c/255 ≤ 0.03928 ? c/255/12.92 : ((c/255+0.055)/1.055)^2.4`);比值报告保留 2 位小数。脚本对 `rgba()` 与 `#rgb` / `#rrggbb` 两种写法都必须解析(`--color-overlay-backdrop` 等三个 rgba 令牌虽不是配对成员,但令牌映射必须能解析它们而不崩)← A11Y-04b precision 行"
    - "四条命令(新增的 CHECK-02 与 Plan 01 的 CHECK-01 / 03 / 04)**各自可独立运行、各自给出明确的通过/失败结论**,且失败方向经过**实证**(注入违规 → 观察到 FAIL → 还原 → 观察到 PASS),不是只验了成功路径 ← ROADMAP Phase 4 SC5"
    - "四个脚本合计零新增依赖:只用 `bash` / `grep` / `awk` / `python3`(标准库)。`frontend/vendor/` 仍只有 `marked.min.js`;仓库无 `package.json`、无构建步骤 ← D-06 / ROADMAP 全局硬规则 6"
  artifacts:
    - path: "scripts/check-02-contrast.py"
      provides: "CHECK-02 对比度自动校验:从 :root 围栏读配对清单,WCAG 相对亮度引擎,4.5:1 文本 / 3:1 非文本,支持 α 合成对"
      contains: "def relative_luminance"
    - path: "frontend/style.css"
      provides: "围栏 `:root` 块内的 PAIR 配对清单(注释,与令牌同一 diff)"
      contains: "/* PAIR "
  key_links:
    - from: "scripts/check-02-contrast.py"
      to: "frontend/style.css 的 :root 围栏"
      via: "同一段注释清单既是配对的来源也是漂移的探测器;清单引用未声明令牌 → 大声失败"
      pattern: "/\\* PAIR "
    - from: "PAIR 清单中的 --color-text-muted 四条"
      to: "--gray-600"
      via: "四个实际背景上的比值构成 note N-1 的机器化守卫(改回 #767676 / #737373 立刻变红)"
      pattern: "--color-text-muted ON --gray-(25|100)"
  prohibitions:
    - "不得引入任何第三方依赖或安装步骤 —— CHECK-02 只用 python3 标准库;`pip install` / `npm install` / 任何 vendored 包都是计划偏差与停止条件 ← D-06 / ROADMAP 全局硬规则 6"
    - "不得把配对清单写成脚本内的硬编码 Python 字面量,也不得在清单引用不存在的令牌名时静默跳过 —— 两者都会让「契约可执行」退化成「一次性清理」,正是本阶段要避免的 ← CHECK-01/02 的存在理由"
    - "不得为了让脚本通过而放宽阈值(把 4.5 改 4.0 / 把 3.0 改 2.5)—— 阈值是 WCAG 的常数,不是可调参数 ← A11Y-04 / A11Y-04b"
    - "不得把已删除的两处 opacity 声明(`.annotation-answered` 的 0.65、`#round-doc.round-frozen` 的 0.55)重新引入,也不得用「提高 α」的方式让它们回到清单里 —— S-4 的裁定是删除,不是调参 ← UI-SPEC S-4 / ledger D-11·D-12"
    - "不得软化 8 处 `:disabled` 的 `opacity` 以让脚本好过 —— SC 1.4.3 豁免非活动组件,脚本不得把 `:disabled` 站点纳入失败面,更不得改样式 ← A11Y-04b 例外条款 / Pitfall M5"
    - "不得为通过 CHECK-02 而改动任何令牌的**值** —— 本阶段的值是 UI-SPEC 逐对重算并冻结的(34 个 hex 的折叠与 AA 修复);若某对失败,正确反应是核对实现是否写错,而不是调值 ← UI-SPEC `## Contrast Verification`"
    - "不得把脚本写成会修改 `frontend/style.css` 或执行 `git checkout` / `git reset` —— 四条校验命令全部是只读的 ← 威胁模型 T-idi04-15"
---

<objective>
交付第四条契约校验命令 `scripts/check-02-contrast.py`(CHECK-02):从 `:root` 围栏内的配对清单派生配对,逐对计算 WCAG 对比度,覆盖**调和后的**范围(20 条文本对 + 4 条非文本对,不是审计的 4 条),并实证四条命令的**失败方向**。

Purpose: 前三条命令是"计数守卫",只有 CHECK-02 校验**本阶段真正的主张** —— AA 达标值在声明处即选定。没有它,"契约可执行"就只是一句散文;有了它,后续四个阶段改任何一个令牌值都会被立刻判定为通过或失败。

Output: `scripts/check-02-contrast.py`;围栏 `:root` 块内的 `/* PAIR … */` 配对清单;四条命令的失败方向实证记录。

**依赖说明:** 本计划在 wave 3 —— 它要读取 Plan 01 / Plan 02 完成后的令牌集合(配对清单引用令牌名),且需要向 `frontend/style.css` 的围栏内写入清单。由于本仓库 `use_worktrees=false`(并行计划共用同一工作树),让本计划与正在写 `style.css` 的 Plan 02 并发会造成读写竞态,故串行在 02 之后。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md
@.planning/phases/idi-04-tokens-contract/idi-04-01-SUMMARY.md
@.planning/phases/idi-04-tokens-contract/idi-04-02-SUMMARY.md
@frontend/style.css
</context>

<tasks>

<task type="auto">
  <name>Task 1: CHECK-02 对比度校验脚本 + 围栏内配对清单</name>
  <files>scripts/check-02-contrast.py, frontend/style.css</files>
  <read_first>
    - frontend/style.css(读 Plan 01 / Plan 02 之后的当前状态;围栏块与全部令牌已就位)
    - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md 的 `## Contrast Verification (A11Y-04 / A11Y-04b) — the reconciled scope`(三张表全文:文本对比度表、逐背景验证矩阵、非文本对比度表)、`### opacity rulings (A11Y-04b)`、`### Hierarchy preserved, not just ratios`、`### The three computed results a naive spec gets wrong`
    - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md 的 `## The Four Contract-Check Commands (CHECK-01 … CHECK-04)` 的 CHECK-02 段
    - .planning/phases/idi-04-tokens-contract/idi-04-01-SUMMARY.md 与 idi-04-02-SUMMARY.md(实际落地的令牌清单 —— 清单里的每个名字都必须真实存在)
  </read_first>
  <action>
    1) **在 `frontend/style.css` 的 `:root` 围栏内追加一段配对清单**(注释形式,与令牌同处一个 diff)。语法逐字固定,每行一条:
    `/* PAIR <fg-token> ON <bg-token> TEXT */`(阈值 4.5:1)
    `/* PAIR <fg-token> ON <bg-token> NON-TEXT */`(阈值 3:1)
    可选 α 后缀作用于 fg:`/* PAIR <fg-token> ON <bg-token> TEXT@0.8 */`。
    清单必须以 `--` 令牌名书写,**绝不写 hex** —— 清单引用未声明的令牌名时脚本必须大声失败。

    **清单内容(调和后的范围:20 条文本对 + 4 条非文本对),逐条按 UI-SPEC 的三张表落笔:**
    - `.hint` 一族:`--color-text-muted ON --color-surface-page TEXT`(5.18)
    - `.badge-answered`:`--color-text-muted ON --color-surface-sunken TEXT`(4.96)
    - `--color-text-muted` 的另外两个实际背景:`--color-text-muted ON --white TEXT`(5.41)、`--color-text-muted ON --gray-100 TEXT`(4.75)—— **这四条构成 note N-1 的机器化守卫**
    - `--color-text` 与 `--color-text-secondary` 各自在其实际背景上的对(至少 `--color-text ON --gray-25 TEXT`、`--color-text-secondary ON --gray-25 TEXT`、`--color-text-secondary ON --amber-25 TEXT`)
    - 事件类别芯片:`--color-kind-fg ON --color-kind-default TEXT`(5.41)、`--color-kind-fg ON --color-kind-say TEXT`(5.87)、`--color-kind-fg ON --color-kind-write TEXT`(5.64)、`--color-kind-fg ON --color-kind-command TEXT`(5.32)、`--color-kind-fg ON --color-kind-error TEXT`、`--color-kind-fg ON --color-kind-read TEXT`、`--color-kind-fg ON --color-kind-done TEXT`
    - 待处理徽标:`--color-action-warning ON --color-surface-warning TEXT`(4.96)
    - 六绿按钮(Phase 4 三族同值,故三对):`--color-action-routine-fg ON --color-action-routine-surface TEXT`(5.10)、`--color-action-commit-fg ON --color-action-commit-surface TEXT`、`--color-action-irreversible-fg ON --color-action-irreversible-surface TEXT`
    - 主色按钮:`--color-action-primary-fg ON --color-action-primary TEXT`(5.87)
    - `.chat-user`:`--color-text-inverse ON --color-surface-info-strong TEXT`(5.87)
    - `#state-badge`:`--color-text-info ON --color-surface-info TEXT`(5.32)
    - 灰斜体 plain 条目与 answer summary:`--color-text-muted ON --white TEXT`(已在上面)
    - 琥珀文字:`--color-action-warning ON --amber-25 TEXT`(5.23)、`--color-action-warning ON --white TEXT`(5.32)、`--color-action-warning ON --gray-25 TEXT`(5.10)
    - 危险色:`--color-action-danger ON --white TEXT`(5.44)、`--color-action-danger ON --gray-25 TEXT`(5.21)、`--color-action-danger ON --gray-100 TEXT`(4.77)
    - **非文本 4 条**:`--color-border-strong ON --white NON-TEXT`(3.45)、`--color-border-strong ON --gray-50 NON-TEXT`(3.17)、`--color-border-streaming ON --gray-50 NON-TEXT`(5.38)、`--color-border-success ON --white NON-TEXT`(5.64)
    - **冻结轮标记(非文本)**:`--color-action-warning ON --gray-25 NON-TEXT`(5.10)—— S-4 裁定的结构性标记必须过 3:1
    - **α 合成 2 条(必须覆盖,覆盖 ≠ 失败)**:`--black ON --white TEXT@0.8`(12.63,`.tier-desc`)、`--color-text ON --gray-25 TEXT@0.75`(7.49,归档态)
    共 20 条文本对(含 2 条 α 合成)与 4 条非文本对(冻结轮标记另计,若计入则 5 条 —— 以实际落笔条数为准并在 SUMMARY 记录)。

    2) **新建 `scripts/check-02-contrast.py`**(零依赖,只用 python3 标准库)。职责:
    - 读 `frontend/style.css`;用与 CHECK-01 同源的围栏状态机(`===== DESIGN TOKENS: START` / `END`)取出围栏内文本。
    - 建令牌映射:解析 `--name: value;`,支持三种值形态 —— `#rgb` / `#rrggbb` / `rgba(r, g, b, a)`,以及 `var(--other)` 链式解析(递归到 primitive;出现环或未定义时**大声失败**并列出该名字)。
    - 解析 `/* PAIR fg ON bg KIND[@alpha] */` 清单行。
    - WCAG 相对亮度:`L = 0.2126R + 0.7152G + 0.0722B`,通道先做 sRGB 反伽马(`c/255 <= 0.03928 ? c/255/12.92 : ((c/255+0.055)/1.055)**2.4`)。
    - 比值 `(L_light + 0.05) / (L_dark + 0.05)`,保留 2 位小数。
    - α 合成:逐通道在 8 位 sRGB 空间 `round(alpha*fg + (1-alpha)*bg)`,再做反伽马。
    - 阈值:文本 4.5、非文本 3.0;**闭区间判定**(≥ 通过),**不把比值四舍五入到阈值再比较**。
    - 输出:逐对打印 `PASS  <ratio>  <fg> on <bg>` 或 `FAIL  <ratio>  <fg> on <bg>  (need >= <threshold>)`;末尾打印 `PASS: 0 failures` 并 `exit 0`,或 `FAIL: <n> failures` 并 `exit 1`。
    - **清单引用了未声明的令牌名 → 打印 `FAIL: unknown token <name>` 并 `exit 1`**(不得静默跳过)。
    - 文件头写 `#!/usr/bin/env python3`,并 `chmod +x`。

    3) 运行它:必须打印 `PASS: 0 failures` 并退出 0。若有失败,**先核对实现是否写错**(某个选择器被迁到了错误的令牌、或某个令牌值被改过),**不要**为了通过而改阈值或改令牌值 —— 值已被 UI-SPEC 逐对重算并冻结。

    **不要做:** 不要把清单写进 Python 源码;不要引入第三方依赖;不要放宽阈值;不要在脚本里写 `git` 命令或写文件;不要把已删除的两处 opacity 重新引入清单。
  </action>
  <verify>
    <automated>python3 scripts/check-02-contrast.py</automated>
    <fails_when>退出码非 0,或 stdout 不含 `PASS: 0 failures`(出现任何 `FAIL` 行即失败)</fails_when>
    <automated>grep -c '/\* PAIR ' frontend/style.css; grep -c 'PAIR .* TEXT' frontend/style.css; grep -c 'PAIR .* NON-TEXT' frontend/style.css</automated>
    <fails_when>第一行不是清单实际条数(应为 24 条及以上);第二行少于 20(文本对不足调和后的范围);第三行少于 4(非文本对不足)</fails_when>
    <automated>python3 -c "import ast,sys; src=open('scripts/check-02-contrast.py').read(); tree=ast.parse(src); mods={n.names[0].name.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.Import)} | {n.module.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.module}; print(sorted(mods))"</automated>
    <fails_when>输出的模块集合中出现任何非标准库名字(如 requests / numpy / wcag_contrast)—— 零依赖是本阶段的硬约束</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh && node --check frontend/app.js</automated>
    <fails_when>任一命令退出码非 0,或 stdout 出现 FAIL 字样(向围栏内追加清单不得破坏另外三条守卫)</fails_when>
    <human-check>在 DevTools Computed 面板抽验 CHECK-02 的三条关键结论:`#ai-route-select` 的 `border-top-color` == rgb(138, 138, 138) 且其 `background-color` == rgb(255, 255, 255)(对应 `--color-border-strong ON --white` = 3.45:1);`.hint` 的 `color` == rgb(106, 106, 106) 且其所在 `#doc-pane` 背景 == rgb(250, 250, 250)(对应 5.18:1);`#stream-banner` 的 `border-top-color` == rgb(138, 101, 8)。三者与脚本打印的比值必须互相印证。</human-check>
  </verify>
  <acceptance_criteria>
    - `python3 scripts/check-02-contrast.py` 退出 0 且 stdout 末行为 `PASS: 0 failures`
    - `scripts/check-02-contrast.py` 存在且可执行;其 import 集合只含 python3 标准库(无第三方模块)
    - `frontend/style.css` 的围栏内 `/* PAIR … */` 清单行数 ≥ 24,其中 `TEXT` 类 ≥ 20、`NON-TEXT` 类 ≥ 4
    - 清单含 `--color-text-muted ON --gray-25`、`--color-text-muted ON --white`、`--color-text-muted ON --gray-50`、`--color-text-muted ON --gray-100` 四条
    - 清单含 `--color-action-warning ON --gray-25 NON-TEXT`(冻结轮标记)
    - 清单含两条 α 合成对:一条 `TEXT@0.8` 与一条 `TEXT@0.75`
    - 清单中不出现 `.annotation-answered` 的 0.65 与 `.round-frozen` 的 0.55 对应的 α 值
    - 清单中不出现任何 `#hex`(全部以 `--` 令牌名书写)
    - 脚本对未声明令牌名的处理是 `exit 1` 且 stdout 含 `unknown token`(可用一次临时改名实证,随后还原)
    - 另外三条守卫命令仍 PASS;`node --check frontend/app.js` 退出 0
  </acceptance_criteria>
  <done>CHECK-02 脚本就位且零依赖;围栏内配对清单以令牌名书写、覆盖调和后的 20 文本 + 4 非文本(含冻结轮标记与两条 α 合成对);脚本打印 `PASS: 0 failures`;清单引用未声明令牌时大声失败;另三条守卫未被破坏。</done>
</task>

<task type="auto">
  <name>Task 2: 四条命令的失败方向实证与阶段收口</name>
  <files>frontend/style.css</files>
  <read_first>
    - frontend/style.css(读 Task 1 之后的当前状态;这是本阶段的终局状态)
    - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md 的 `## The Four Contract-Check Commands`(四条命令的原文与基线算术陷阱)与 `## Global Hard Rules`
    - .planning/ROADMAP.md 的 Phase 4 `**Gates**` 段
  </read_first>
  <action>
    本任务是本阶段的收口 gate:证明四条命令**各自独立、各自给出明确的通过/失败结论**,并跑完全部阶段门。

    **前置:先把工作树提交干净。** 下面的失败方向实证会临时篡改 `frontend/style.css` 再用 `git checkout -- frontend/style.css` 还原 —— 只有在文件已提交的前提下才安全。**若工作树有未提交的改动,先提交,不要执行 `git checkout`。**

    **失败方向实证(每条命令一次:注入违规 → 观察到 FAIL → 还原 → 观察到 PASS)。逐条记录命令、注入内容、观察到的输出与退出码:**
    - **CHECK-01**:在围栏**之外**追加一行 `#deadbe`(临时)。期望 `bash scripts/check-01-token-conformance.sh` 打印 `FAIL` 且退出 1,计数值 +1。还原后应回到 `PASS`、计数 0。
    - **CHECK-02**:临时把清单里的一条 `TEXT` 对改成一个必然失败的组合(例如把 `--color-text-muted` 那一行临时替换成 `--gray-300` on `--gray-25`,比值约 1.1)。期望 `python3 scripts/check-02-contrast.py` 打印该对的 `FAIL` 行且末行为 `FAIL: 1 failures`、退出 1。还原后应回到 `PASS: 0 failures`。
    - **CHECK-03**:临时把 `^\.hidden {` 那一行前加一个空格(破坏行首锚点)。期望 `bash scripts/check-03-hidden-uniqueness.sh` 打印 `FAIL` 且退出 1。还原后回到 `PASS`(计数 1)。
    - **CHECK-04**:临时在任意规则里追加一条 `color: red !important;`(注意:**只用于实证,必须还原**)。期望 `bash scripts/check-04-important-count.sh` 打印 `FAIL` 且退出 1(计数 2)。还原后回到 `PASS`(计数 1)。
    **每次还原后都必须重跑该命令确认回到 PASS**,并在 SUMMARY 里记录四组"注入前 / 注入后 / 还原后"的原始输出。

    **阶段收口(全部必须绿):**
    - 四条命令依次独立运行:`bash scripts/check-01-token-conformance.sh`、`python3 scripts/check-02-contrast.py`、`bash scripts/check-03-hidden-uniqueness.sh`、`bash scripts/check-04-important-count.sh` —— 各自退出 0
    - Gate 2:`comm -23 <(grep -o 'var(--[a-z0-9-]*' frontend/style.css | sed 's/var(//' | sort -u) <(grep -o '\-\-[a-z0-9-]*:' frontend/style.css | sed 's/:$//' | sort -u)` → 输出为空
    - 反向孤儿扫描 → 除 `--green-800` 外为空
    - `node --check frontend/app.js` → 退出 0
    - `.venv/bin/python -m pytest -q` → 全绿,passed 数不少于改动前实测的收集数
    - `git status --porcelain frontend/` → 只有 `frontend/style.css`;`ls frontend/vendor/` → 仅 `marked.min.js`
    - `git diff --name-only HEAD -- frontend/app.js frontend/index.html` → 输出为空
    - `git diff --name-only HEAD -- frontend/style.css` → 只有这一个文件
    - **确认没有残留的实证篡改**:`frontend/style.css` 中不得出现 `#deadbe`、不得出现清单里的 `--gray-300 on --gray-25`,`grep -c '!important;'` 必须回到 1

    **运行时收口(人工,具名):** 在运行中的应用里做一次全阶段 DevTools Computed 抽验 —— 覆盖 Plan 01 与 Plan 02 各任务列出的具名属性;重点复验两条下游门:①`#brainstorm-view h2` 仍为 14px / rgb(138, 101, 8);②冻结轮的 `box-shadow` 含 `inset 3px 0 0 rgb(138, 101, 8)` 且 `opacity` == 1。**本环境截图不可用、headless 渲染被挡 —— 不规划视觉 diff。**

    **不要做:** 不要把任何实证用的篡改留在工作树里;不要用 `git stash` / `git reset --hard`(会丢掉本阶段的成果);不要在 `app.js` / `index.html` 上做任何实证。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh && python3 scripts/check-02-contrast.py && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh</automated>
    <fails_when>任一命令退出码非 0,或 stdout 出现 FAIL 字样(四条必须各自独立通过)</fails_when>
    <automated>test "$(grep -c '#deadbe' frontend/style.css)" = "0" && test "$(grep -c -- '--gray-300 on --gray-25' frontend/style.css)" = "0" && test "$(grep -c '!important;' frontend/style.css)" = "1"</automated>
    <fails_when>任一 `test` 返回非 0 —— 即工作树里残留了实证用的篡改(`#deadbe` 或清单里的失败对),或 `!important;` 声明数不是 1(注入的那条未还原)</fails_when>
    <automated>test -z "$(comm -23 <(grep -o 'var(--[a-z0-9-]*' frontend/style.css | sed 's/var(//' | sort -u) <(grep -o '\-\-[a-z0-9-]*:' frontend/style.css | sed 's/:$//' | sort -u))" && node --check frontend/app.js && .venv/bin/python -m pytest -q</automated>
    <fails_when>第一条输出非空(存在未声明的 var() 消费);或 node 退出非 0;或 pytest 摘要行 passed 数少于改动前实测的收集数</fails_when>
    <automated>test -z "$(git ls-files --others --exclude-standard frontend/)" && test "$(ls frontend/vendor/)" = "marked.min.js" && test -z "$(git diff --name-only HEAD -- frontend/app.js frontend/index.html)"</automated>
    <fails_when>任一 `test` 返回非 0 —— 即 `frontend/` 下出现新文件、或 vendor 目录不是恰好 `marked.min.js`、或 app.js/index.html 被改动</fails_when>
    <human-check>全阶段 DevTools Computed 抽验:①`#brainstorm-view h2` 的 `font-size` == 14px 且 `color` == rgb(138, 101, 8)(ROADMAP Phase 5 SC5 / Phase 6 SC5 的下游门);②打开历史轮次,`#round-doc` 的 `box-shadow` 含 `inset 3px 0 0 rgb(138, 101, 8)`、`opacity` == 1、`filter` == `saturate(0.6)`,且文档区无横向位移;③`.hint` 的 `color` == rgb(106, 106, 106);④`#ai-route-select` 的 `border-top-color` == rgb(138, 138, 138);⑤在应用里点一次「处理本轮批注」与一次「发送」,确认交互路径未被令牌迁移破坏(五条 b9664e0 修复的回归复验在 Phase 8 的 REG-03,此处只做冒烟)。</human-check>
  </verify>
  <acceptance_criteria>
    - 四条命令依次独立运行均退出 0:CHECK-01 / CHECK-02 / CHECK-03 / CHECK-04
    - SUMMARY 里记录了四组失败方向实证的原始输出(注入前 / 注入后 / 还原后),每组都含一条可观察的 `FAIL` 与一条可观察的 `PASS`
    - `grep -c '#deadbe' frontend/style.css` 输出 0;`grep -c -- '--gray-300 on --gray-25' frontend/style.css` 输出 0;`grep -c '!important;' frontend/style.css` 输出 1(无残留篡改)
    - `comm -23 <(...var(...)...) <(...--...:...)>` 输出为空;反向孤儿扫描除 `--green-800` 外为空
    - `node --check frontend/app.js` 退出 0;pytest 全绿且 passed 数不少于改动前实测收集数
    - `git status --porcelain frontend/` 只有 `frontend/style.css`;`ls frontend/vendor/` 仅 `marked.min.js`;`git diff --name-only HEAD -- frontend/app.js frontend/index.html` 输出为空
    - `git diff --name-only HEAD -- frontend/style.css` 只列出这一个文件
  </acceptance_criteria>
  <done>四条命令的失败方向经实证(注入 → FAIL → 还原 → PASS),四组原始输出记入 SUMMARY;阶段全部自动化门绿;工作树无残留篡改;下游门(`#brainstorm-view h2` 14px / rgb(138,101,8))与冻结轮标记经人工实检。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| `frontend/style.css` → `scripts/check-02-contrast.py` | 脚本把文件内容当作**数据**解析(令牌映射 + 清单行),绝不求值、绝不执行 |
| `scripts/*` → 仓库工作树 | 四条命令全部**只读**;失败方向实证的临时篡改由执行者在已提交的工作树上手工注入并 `git checkout` 还原,不由脚本完成 |
| 配对清单 → 令牌块 | 清单引用不存在的令牌名是"契约漂移"信号,必须大声失败而非静默跳过 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi04-15 | Tampering | `scripts/check-02-contrast.py` 修改工作树或执行 git 命令 | high | mitigate | 脚本明令只读:不写文件、不调 `git`。失败方向实证由执行者在**已提交**的工作树上手工注入并还原,且由 `git diff HEAD -- frontend/style.css` 的残留扫描作为机械门。另:执行前置要求先提交,避免 `git checkout` 抹掉未提交成果。 |
| T-idi04-16 | Spoofing | 契约漂移:清单引用的令牌名不再存在,脚本静默跳过 → 假 PASS | high | mitigate | 脚本对未声明令牌名打印 `FAIL: unknown token <name>` 并 `exit 1`。这是"从 :root 块派生配对"的全部价值所在 —— 若允许静默跳过,CHECK-02 就退化成一份会腐烂的硬编码清单。 |
| T-idi04-17 | Tampering | 阈值被"为了通过"放宽 | high | mitigate | 阈值是 WCAG 常数(文本 4.5、非文本 3.0),prohibition 明令禁止调整;acceptance_criteria 要求清单中不出现被删除的 0.65 / 0.55 α 值,且禁止为通过而改令牌值。 |
| T-idi04-18 | Elevation of Privilege | 8 处 `:disabled` 的 opacity 被纳入失败面从而被"顺手"软化 | high | mitigate | SC 1.4.3 豁免非活动组件;`:disabled` 是 G3 前提条件唯一的视觉信号。Plan 02 的 verify 用四处精确计数(6 / 2 / 1 / 1)守住它,本计划的清单不得包含 `:disabled` 站点。 |
| T-idi04-19 | Repudiation | "四条命令都通过"只验了成功路径 | medium | mitigate | 本计划的 Task 2 就是这条缓解:每条命令都要实证**失败方向**(注入违规 → 观察到 FAIL → 还原 → 观察到 PASS),四组原始输出记入 SUMMARY。SC5 要求的是"各自给出明确的通过/失败结论",只有失败方向被证明才成立。 |
| T-idi04-20 | Information Disclosure | 实证用的临时篡改残留在工作树 | medium | mitigate | `git diff HEAD -- frontend/style.css` 的残留扫描(三条特征串)作为机械门;还原后必须重跑该命令确认回到 PASS。 |
| T-idi04-SC | Tampering | npm / pip / cargo 安装(供应链) | high | mitigate | **本阶段零安装**:CHECK-02 只用 python3 标准库,由 AST 扫描 import 集合证明;仓库无 `package.json`、无构建步骤。无包管理器安装任务 ⇒ 无 `[ASSUMED]` / `[SUS]` 包需要合法性检查点。 |
</threat_model>

<verification>
**自动化门(每条都可独立运行,均须给出明确 PASS/FAIL):**

1. `bash scripts/check-01-token-conformance.sh` → PASS,围栏外裸 hex = 0
2. `python3 scripts/check-02-contrast.py` → `PASS: 0 failures`
3. `bash scripts/check-03-hidden-uniqueness.sh` → PASS,`^\.hidden {` = 1
4. `bash scripts/check-04-important-count.sh` → PASS,`!important;` 声明数 = 1
5. Gate 2(`comm -23`)→ 输出为空;反向孤儿扫描 → 除 `--green-800` 外为空
6. `grep -c '#deadbe' frontend/style.css` → 0;`grep -c -- '--gray-300 on --gray-25' frontend/style.css` → 0;`grep -c '!important;' frontend/style.css` → 1(无残留篡改)
7. `node --check frontend/app.js` → 退出 0
8. `.venv/bin/python -m pytest -q` → 全绿
9. `git status --porcelain frontend/` → 只有 `frontend/style.css`;`ls frontend/vendor/` → 仅 `marked.min.js`
10. `git diff --name-only HEAD -- frontend/app.js frontend/index.html` → 输出为空

**失败方向实证(SC5 的实质):** 四条命令各做一次"注入违规 → 观察到 FAIL → 还原 → 观察到 PASS",四组原始输出记入 SUMMARY。只验成功路径不构成 SC5 的证明。

**pytest 基线说明(必须照实记录):** ROADMAP 与 REQUIREMENTS 写的基线是 **219**,但规划时对工作树实测 `pytest --collect-only -q` 收集到 **225** 条。门按"passed 数 ≥ 执行本计划前实测的收集数"判定,并在 SUMMARY 里记录实际数字 —— 照抄 219 会造出一个必然失败的假门。

**运行时验证(Pitfall M1):** 本环境截图不可用(headless 渲染被挡,且常驻 `/api/events` SSE 流使采集处理器无法终止)—— **不得规划视觉 diff**。改为 DevTools Computed 的具名属性抽验,并与 CHECK-02 打印的比值互相印证;两条下游门(`#brainstorm-view h2` 14px / rgb(138,101,8)、冻结轮标记)必须实检。
</verification>

<success_criteria>
1. CHECK-02 可独立运行,打印 `PASS: 0 failures`,零依赖(标准库 AST 扫描为证)
2. 配对清单以令牌名书写于围栏内,覆盖调和后的 20 文本对 + 4 非文本对,含冻结轮标记与两条 α 合成对
3. 清单引用未声明令牌时脚本大声失败(契约漂移可检出)
4. 四条命令的失败方向均经实证,四组原始输出记入 SUMMARY
5. 阶段全部自动化门绿;工作树无残留篡改
6. `app.js` / `index.html` 零改动;`frontend/vendor/` 仍只有 `marked.min.js`;pytest 基线不下降
7. `#brainstorm-view h2` 仍计算为 14px / rgb(138, 101, 8);冻结轮的琥珀 inset 标记可见且 `opacity` == 1
</success_criteria>

## Artifacts this phase produces (本计划产出的部分)

Plan 01 已列出本阶段的完整符号清单;本计划新增的部分如下。

**新增文件路径(1 个):**

| 路径 | 说明 |
|---|---|
| `scripts/check-02-contrast.py` | CHECK-02 对比度自动校验,零依赖 python3 标准库 |

**新增 CLI 调用(1 条,从仓库根目录运行):**

| 命令 |
|---|
| `python3 scripts/check-02-contrast.py` |

**`frontend/style.css` 围栏 `:root` 块内新增的内容(本计划产出):**

| 符号 | 形态 | 说明 |
|---|---|---|
| `/* PAIR <fg> ON <bg> TEXT */` | 注释清单行(≥ 20 行) | 文本对,阈值 4.5:1 |
| `/* PAIR <fg> ON <bg> NON-TEXT */` | 注释清单行(≥ 4 行) | 非文本对,阈值 3:1 |
| `/* PAIR <fg> ON <bg> TEXT@<alpha> */` | 注释清单行(2 行) | α 合成对(`.tier-desc` 的 0.8、归档态的 0.75) |

**新增 CSS 自定义属性:** 无。
**新增/变更的选择器:** 无。
**新增字面量例外:** 无(清单以令牌名书写,不含 hex)。
</verification>

<output>
Create `.planning/phases/idi-04-tokens-contract/idi-04-03-SUMMARY.md` when done
</output>
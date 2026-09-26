---
phase: idi-07-interaction-states-and-focus
plan: 02
subsystem: ui
tags: [css, interaction-states, hover, active, disabled, design-tokens, specificity, cascade, contrast-pairs, playwright, uat-harness, mutation-testing]

# Dependency graph
requires:
  - phase: idi-07-interaction-states-and-focus
    plan: 01
    provides: "围栏内 `--color-focus` 的声明形态与「与消费者同提交」写法、文件末尾的追加位置与注释纪律、`check-02` PAIR 清单的记账位置(`@<alpha>` 机制)、`check-05` item 10 的骨架与四处登记点、`read_style` / `resolve_color` / `resolve_token` 三个读取器 —— 本计划的 hover / active 探针全部复用它们"
  - phase: idi-04-tokens-contract
    provides: "围栏 `:root` 的 tier-1/tier-2 命名与围栏注释纪律(含 `#hex` 与 tier-1 `var()` 泄漏的机械守卫)、`check-02-contrast.py` 的 PAIR 清单机制(`PAIR_RE` / 覆盖地板 / 原始标记计数自洽)"
  - phase: idi-04.1-radix
    provides: "`--radix-gray-4` / `--radix-gray-11` / `--radix-gray-12` 三个已声明的 primitive(本计划四个新令牌零新增 primitive 的前提)、04.1-N-4 的值碰撞登记先例"
  - phase: idi-06-layout-robustness
    provides: "`check-05` 的 `CLEARANCE_MIN_PX = 4.0`、`_idi06_clearance_assert` / `_idi06_hit_assert` 的形态纪律(前提检查 ⇒ BLOCKED 而非 PASS)、06-CONTEXT D-09 的「防御性非冗余必须写注释」形态"
provides:
  - "`frontend/style.css`:围栏内四个新 tier-2 令牌 —— `--color-surface-active`(gray-4)/ `--color-border-hover`(gray-11)/ `--color-overlay-hover`(rgba 0.06)/ `--color-overlay-active`(rgba 0.12),零新增 tier-1 primitive,全部与消费者同提交"
  - "`frontend/style.css`:L627 的 `button:hover` 选择器就地改写为 `button:where(:not(:disabled)):hover:where(:not(:active))` —— 禁用按钮不再匹配(D-07 的缺陷修复)+ 按住不放时让位(D-09 的朴素按下态所必需),声明体逐字节不变、特异性逐位不变(0-1-1)"
  - "`frontend/style.css`:文件末尾三组追加规则 —— 朴素 `:where(button:not(:disabled)):active`(0-1-0)、填充按钮 hover / active 叠层组(各十条选择器,0.06 / 0.12)、输入控件 hover 边界组(八条选择器)"
  - "`frontend/style.css`:两条 `--color-border-hover` NON-TEXT 配对(`--color-surface-page` / `--color-surface`)+ 清单头部计数注释扩写为六层 `24 / 34 / 43 / 47 / 50 / 52`"
  - "`scripts/check-05-ui-uat.py`:item 10 的 SC5 / SC5-朴素按下 / SC5′ 三条运行时探针 + 动态 `.verdict-note-input` 的 hover 边界断言 + `_IDI07_INTERACTIVE_JS`(存在 ∧ 可见 ∧ 未被禁用的前提检查)"
affects: ["Phase 7 计划 03(过渡与减弱动效复用同一套追加位置、同一份 item 10 骨架与同一批前提检查)", "/gsd-verify-work idi-07", "/gsd-verify-work idi-04 / idi-04.1-radix / idi-05 / idi-06(本计划再次改动了 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`,这四份报告的 live 指纹早已被 D-19 作废 —— 重算义务归计划 03 Task 3)"]

actuals:
  tokens: 10976     # chars/4 over the realized diff of the two changed files (43906 chars)
  tasks: 3
  commits: 3        # MEASURED: git rev-list --count ed63381..HEAD
  plan_head_before: ed63381f32e311cb5decd55272f219c9340691ed

tech-stack:
  added: []
  patterns:
    - "**交互态的 gate 落在既有选择器上,不落在新增规则上**:把 gate 写成一条新规则会同时产生「修不了缺陷」(`:not(:disabled)` 不匹配禁用按钮,而旧规则仍匹配它)与「引入回归」(类列 2 > `button.primary` 的类列 1,填充族 hover 时变灰底)两个后果。就地改写选择器则特异性逐位不变,而 `:where()` 贡献 0 特异性使这件事成为可能"
    - "**特异性死结靠「让位」而非「升权」解**:「朴素 active 必须胜过 hover」要求 ≥ 0-1-1,「填充族必须保住自己的填充」要求 ≤ 0-1-0,两者在特异性上不可同时满足。解是让 hover 在按住不放时**不再匹配**(`:where(:not(:active))`),0-1-0 因而足够 —— 两半是**一对**选择器改写,改一必须改另一"
    - "**「不相等」是判据本体,不是补强**:只断言「按下读数 == `--color-surface-active`」时,让位未生效的实现会读到 hover 值而**不会变红**(该断言只要求等于期望值)。「③ != ②」这半条必须显式写出,并由变异测试证明它真的会失败"
    - "**「可见」不等于「可交互」**:一个渲染出来的禁用按钮 rect 非零,却永远不匹配 `:not(:disabled)` 的选择器 —— 前提检查必须把 `disabled` 一并断言,否则探针会 **FAIL 而非 BLOCKED**(本任务最初的探针目标正是这样写错的)"
    - "**在按钮上读「按住不放」必须先把指针移开再抬手**:原地上抬会触发 click,真的发请求并改动样本状态(`#btn-send` 会发消息、裁决按钮会 POST 一次裁决)。探针的副作用面与它的断言面同等重要"
    - "**围栏内的注释不能出现「令牌名 + 冒号」**:`check-02` 的 `DECL_RE` 按 `(--[a-z0-9-]+)\\s*:\\s*([^;]+);` 扫围栏全文(含注释),注释里写 `--radix-gray-12: ...` 会被当成一条值不可解析的声明而 FAIL。讲「不取哪一档」时必须改写措辞(本计划为此付过一次 FAIL)"
    - "**围栏外的机械判据是子串计数,注释里的「举例」同样计入**:`awk` 取围栏外后 `grep -c 'rgba('` 必须为 0 —— 连「规则体不写裸 `rgba()`」这样一句**论证性散文**都会把它顶成 1。讲这件事时写「不写颜色字面量」"

key-files:
  created: []
  modified:
    - frontend/style.css
    - scripts/check-05-ui-uat.py

key-decisions:
  - "**D-07 的 gate 落在 L627 的选择器上,不落在新增规则上。** 把 `button:not(:disabled):hover` 当新增规则追加会同时产生两个后果:①修不了缺陷(`:not(:disabled)` 不匹配禁用按钮,而 L627 仍然匹配它,`.verdict-buttons button:disabled` 只设 opacity / cursor、不钉 background,照样被上色);②引入回归(0-2-1 的类列 2 > `button.primary` / `.overlay-card button` 的类列 1,这两族填充按钮 hover 时变灰底)。就地改写后特异性逐位不变(0-1-1),`:where()` 贡献 0 特异性使这件事成立"
  - "**D-08 的 rgba 落点选「围栏内令牌」支。** CONTEXT D-08 的片段把 `rgba(0,0,0,0.06)` 写在规则体内,而 style.css 既有的 R-2 注释立下的是相反先例(「使围栏外不再出现裸 rgba()」)。`check-01` 不数裸 `rgba()` ⇒ 这条纪律**无机械守卫**。两个 alpha 收进 `--color-overlay-hover` / `--color-overlay-active` 后成为可复算的单一事实源;代价是围栏内多两个 tier-2 令牌,它们不是对比度边界,故**不进 PAIR 清单**(`--shadow-*` 同族也没有配对)"
  - "**朴素 `:active` 停在 0-1-0,由 L627 的 `:where(:not(:active))` 承担让位。** `button.primary` 与 `.overlay-card button` 都自带 `background` 声明且都是 0-1-1;朴素 active 追加在文件末尾,若取到 0-1-1 就会**靠源码顺序**夺走这两族的填充(白字落在灰底上)。两半的配套关系写进了两处注释,并在 SUMMARY 与 STATE 里各记一条 —— **后来者不得为「对齐」把它升到 0-1-1**"
  - "**两处值碰撞被显式登记。** `--color-surface-active` 与 `--color-surface-user` 同值(gray-4):注释点名 04.1-N-4 并同步扩写 L316-320 的第 3 条(否则那份注释自相矛盾,后来者会把新令牌当违规「修掉」)。`--color-border-hover` 与 `--color-text-muted` 同值(gray-11):同值不同名、不共享消费者,同样登记"
  - "**SC5 的填充半场取 `#btn-send`,不用 `#btn-process-round`。** 后者在 p1 的标记里带 `disabled`(index.html:73),`applySessionGates()` 只 `classList.remove('hidden')`、**从不清 `disabled`**,放开它的是阶段 3 路径上的 `updateFrozenPresentation()` —— 故 p1 里它可见但禁用,`#btn-process-round:not(:disabled):hover` 根本不匹配,断言会 **FAIL 而非 BLOCKED**。`#btn-send` 在 p1 可用(`applySessionGates()` 显式 `sendBtn.disabled = false`)"
  - "**SC5-朴素按下 的目标取 `renderVerdictCard()` 造出的裁决卡的首个按钮。** 它是本仓库里**在样本中稳定可达的朴素无底色按钮**;`.modal-buttons button` / `.tier-buttons button` 虽然也叫「模态按钮」,但它们都在 `.overlay-card` 内,已被 `.overlay-card button`(0-1-1)填成主色,不是朴素族。两个探针**共用同一张卡**(SC5′ 复用,不重复造第二张),故 SC5-朴素按下 必须先跑(那时按钮还没被禁用)"
  - "**两条承重断言经变异测试证明非空转。** 变异 1(从 L627 去掉 `:where(:not(:active))`)⇒ SC5-朴素按下 的 ③ 读到 ② 的值,2 条 FAIL、exit 1;变异 2(从 L627 去掉 `:where(:not(:disabled))`)⇒ SC5′ 的「禁用态 hover 背景 == 静默背景」FAIL、exit 1。两次变异后 `git checkout -- frontend/style.css` 复原,`git status --porcelain` 为空。变异测试是唯一能区分「守卫在工作」与「守卫静默空转」的手段(本项目已登记的教训)"

patterns-established:
  - "Pattern 1: 交互态的 gate 写在**既有选择器**上并用 `:where()` 保住特异性 —— 新增规则会改变特异性、进而改变级联结果,而 diff 看起来完全无辜"
  - "Pattern 2: 特异性不可同时满足的两个约束,用「让位」(`:where(:not(:active))`)而不是「升权」解;两半必须同提交,并在两侧注释里互相点名"
  - "Pattern 3: 交互态探针的前提检查是**三合一**的(存在 ∧ 可见 ∧ 未被禁用),「可见」单独一项会把禁用控件读成合格目标,使断言 FAIL 而非 BLOCKED"
  - "Pattern 4: 每条承重断言都用**变异**证明它会失败;变异在已提交的树上做,用定向 `git checkout -- <file>` 复原,复原后以 `git status --porcelain` 为空为判据"

requirements-completed: [INTERACT-01]

coverage:
  - id: D1
    description: "围栏内四个交互态 tier-2 令牌 + L627 的选择器 gate 与让位 + 朴素按钮的 `:active`(0-1-0):填充按钮 hover 时计算 `background-color` 不变而 `box-shadow` 出现 inset 叠层;禁用按钮 hover 时零反馈;朴素按钮按下态与 hover 态读数**不相等**"
    requirement: "INTERACT-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 10(SC5 #btn-send / SC5-朴素按下 / SC5′,exit 0)"
        status: pass
      - kind: other
        ref: "bash scripts/check-01-token-conformance.sh(围栏外裸 hex == 0 且 tier-1 `var()` 泄漏 == 0)"
        status: pass
      - kind: other
        ref: "git diff --numstat(本任务的删除行数恰为 2:L627 的选择器行 + 「Three values」第 3 条的扩写)"
        status: pass
    human_judgment: false
  - id: D2
    description: "填充按钮的 hover / active rgba 叠层规则组:十条 hover 选择器(0.06)+ 十条 active 选择器(0.12),逐条跨过对应既有填充规则的特异性(七条 `#btn-*` 1-2-0、`#chat-input-row button` 1-2-1、`button.primary` / `.overlay-card button` 0-3-1)"
    requirement: "INTERACT-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 10(SC5 五条断言:bg 不变 / inset 999px / hover 色 / active 色 / 按下 ≠ hover)"
        status: pass
      - kind: other
        ref: "awk 取围栏外后 `grep -c 'rgba('` == 0 且 `grep -c 'box-shadow: inset 0 0 0 999px'` == 2"
        status: pass
    human_judgment: false
  - id: D3
    description: "输入控件的 hover 边框加深:八条选择器覆盖 4 个静态 input + 3 个 select + 1 个动态 `.verdict-note-input`;两条 `--color-border-hover` NON-TEXT 配对达标;清单头部计数注释扩写为六层 `24 / 34 / 43 / 47 / 50 / 52` 且与清单实际条目数一致"
    requirement: "INTERACT-01"
    verification:
      - kind: unit
        ref: ".venv/bin/python scripts/check-02-contrast.py(末行 `PASS: 0 failures`;两条 `--color-border-hover` 配对各 PASS;`^PASS` 行数 51 → 53)"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 10(`#message-input` 与动态 `.verdict-note-input` 各两条 hover 边界断言)"
        status: pass
    human_judgment: false
  - id: D4
    description: "`check-05` 第 10 项的 SC5 / SC5-朴素按下 / SC5′ 三条运行时探针 + 三合一前提检查(存在 ∧ 可见 ∧ 未被禁用)+ 读完后先移开指针再抬手的副作用纪律;item 10 由 11 条断言增至 26 条"
    requirement: "INTERACT-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 10(item 10: PASS,26 条断言,0 FAIL,0 BLOCKED;exit 0)"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8,9(既有九项仍全绿,exit 0)"
        status: pass
      - kind: other
        ref: "变异测试两支(去掉让位 ⇒ SC5-朴素按下 2 FAIL;去掉 gate ⇒ SC5′ 1 FAIL),复原后 `git status --porcelain` 为空"
        status: pass
    human_judgment: false

duration: 14min
completed: 2026-09-23
status: complete
---

# Phase 7 Plan 02: 交互状态语言(hover / active / 禁用态)Summary

**把「有底色语义的按钮 hover 时零反馈」与「禁用按钮 hover 时变色」两个实测缺陷正面修掉:围栏内四个新 tier-2 令牌(零新增 primitive)、L627 的选择器就地 gate 在 `:not(:disabled)` 上并在按住不放时让位、三组追加规则(朴素 `:active` 停在 0-1-0 / 填充按钮的 0.06→0.12 叠层 / 输入控件的边框加深),外加两条 `--color-border-hover` 配对与 `check-05` 第 10 项的三条交互态运行时探针 —— item 10 由 11 条断言增至 26 条,两条承重断言经变异测试证明会真的失败。**

## Performance

- **Duration:** 14 min
- **Started:** 2026-09-23T06:13:55Z
- **Completed:** 2026-09-23T06:28:12Z
- **Tasks:** 3
- **Files modified:** 2(`frontend/style.css` / `scripts/check-05-ui-uat.py`,零新建)

## Accomplishments

- **两个实测缺陷被正面修掉,且修法是「就地改写选择器」而非「新增抵消规则」。** D-02 第 7 条实测的「所有有底色语义的按钮 hover 时零反馈」与第 5 条的「`.verdict-buttons button:disabled` 悬停变色」同一根因:`button:hover`(0-1-1)被九组 1-0-0 / 0-1-1 的填充规则盖掉,却照样给禁用按钮上色。把 gate 写在 L627 的选择器上后,特异性**逐位不变**(仍是 0-1-1),但匹配集收窄了两处 —— 禁用按钮不再匹配(缺陷修复,一次修掉、全局生效),按住不放中的按钮也不再匹配(D-09 的朴素按下态所必需)。
- **特异性死结用「让位」而不是「升权」解,两半同提交并互相点名。** 「朴素 active 必须胜过 hover」要求 ≥ 0-1-1,「填充族必须保住自己的填充」要求 ≤ 0-1-0 —— 不可同时满足。解是让 hover 在按住不放时不再匹配,0-1-0 因而足够;若把朴素 active 升到 0-1-1,`button.primary` 与 `.overlay-card button`(两者都自带 0-1-1 的 `background` 声明、且源码在前)会在**同特异性**下被源码顺序夺走填充。两半的配套关系写进了两处注释,`<decision_register>` 的逐族核对表也在 SUMMARY 与 STATE 各留一条。
- **D-08 的 rgba 落点选「围栏内令牌」支,R-2 的不变量被保住并升级为一条显式断言。** 两个 alpha 收进 `--color-overlay-hover` / `--color-overlay-active`,规则体只写 `var()`。`check-01` **不数裸 `rgba()`** ⇒ 这条纪律本来无机械守卫;本计划把它落成 `awk` 取围栏外 + `grep -c 'rgba('` == 0 的判据(实测 0)。代价是围栏内多两个 tier-2 令牌,它们不是对比度边界,故不进 PAIR 清单。
- **填充按钮的叠层逐条跨过既有填充规则的特异性。** 十条选择器各自写明具体特异性并逐条跨过对应既有规则:七条 `#btn-*(1-2-0)` 跨 1-0-0、`#chat-input-row button(1-2-1)` 跨 1-0-1、`button.primary` 与 `.overlay-card button(0-3-1)` 跨 0-1-1(后者也跨 `.overlay-card button.danger` 的 0-2-1)。注释里点明了那条**不带 id/族前缀的通用 gate 写法**为什么无效(1-0-0 > 0-2-1,ID 列大于类列)—— 措辞按计划的硬要求改写过,那个失效字面量**没有**进入 `frontend/style.css`(含论证性注释)。
- **输入控件的 hover 覆盖 4 个静态 input + 3 个 select + 1 个动态输入框,逐条都有服务对象。** 八条选择器按既有 ID 级规则体逐条枚举(通用 `input` 元素选择器是 0-1-1,会被所有 1-0-0 的 ID 规则盖掉);`.verdict-note-input` 的服务对象是 `app.js` 在裁决卡里动态建的那一个,由 item 10 在真实裁决卡上实测。`:not(:disabled)` 在 input / select 上是**防御性非冗余**(全站 8 条 `:disabled` 规则全部是按钮),照 06-CONTEXT D-09 的 `min-width: 0` 形态写进注释。
- **`check-05` 第 10 项从 11 条断言增至 26 条,`item 10: PASS (26 条断言,0 FAIL,0 BLOCKED)`,exit 0。** 新增 SC5(填充按钮 hover 叠层 + 按下 0.12 + `#message-input` 的边框加深)、SC5-朴素按下(静默 `rgb(249,249,249)` → 悬停 `rgb(240,240,240)` → 按住不放 `rgb(232,232,232)`,并断言 ③ != ②)、SC5′(禁用按钮 hover 背景 `rgb(249,249,249)` == 静默值,`opacity` 仍为 0.5)、以及动态 `.verdict-note-input` 的 hover 边界。
- **两条承重断言经变异测试证明非空转。** 变异 1(去掉 L627 的 `:where(:not(:active))`)⇒ ③ 读到 ② 的值,`item 10: FAIL (26 条断言,2 FAIL,0 BLOCKED)`,exit 1;变异 2(去掉 L627 的 `:where(:not(:disabled))`)⇒ SC5′ 的「禁用态 hover 背景 == 静默背景」FAIL,exit 1。两次变异都在**已提交**的树上做,用定向 `git checkout -- frontend/style.css` 复原,复原后 `git status --porcelain` 为空、四条门与 item 10 复跑仍全绿。
- **四条既有门与既有九项 UAT 全程全绿。** `check-01` / `check-03` / `check-04` 各恰一行 `PASS`;`check-02` 末行 `PASS: 0 failures`,`^PASS` 行数 51 → **53**(50 → 52 对 + 1 ORDER);`check-05 --item smoke,1,2,3,4,6,7,8,9` exit 0。`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` / `scripts/ui-states/` **零改动**(`git status --porcelain` 为空)。

## Task Commits

Each task was committed atomically:

1. **Task 1: 围栏内四个新令牌 + L587 的选择器 gate 与让位 + 朴素按钮的 `:active`** - `cd5a1a1` (feat)
2. **Task 2: 填充按钮的 hover / active rgba 叠层(按九组既有规则逐条核对特异性)** - `0b40da5` (feat)
3. **Task 3: input / select 的 hover 加深 + 两条 PAIR + 清单计数 52 + SC5 / SC5′ 运行时探针** - `aa7194b` (feat)

**Plan metadata:** 见本计划的 docs 元数据提交(SUMMARY + STATE + ROADMAP + REQUIREMENTS)

## Files Created/Modified

- `frontend/style.css` - 围栏内四个新 tier-2 令牌(`--color-surface-active` / `--color-border-hover` / `--color-overlay-hover` / `--color-overlay-active`)与它们各自的承重注释;「Three values that must NOT be 'helpfully' changed back」第 3 条的同步扩写;L627 的选择器就地改写(声明体逐字节不变);文件末尾三组追加规则(朴素 `:active` / 填充按钮 hover + active 叠层 / 输入控件 hover 边界);围栏内两条 `--color-border-hover` 配对与清单头部六层计数注释
- `scripts/check-05-ui-uat.py` - 第 10 项的 SC5 / SC5-朴素按下 / SC5′ 三条探针与三条形态纪律注释;`_IDI07_OVERLAY_SPREAD` / `_IDI07_DISABLED_OPACITY` / `_IDI07_VERDICT_PROBE_ID` 三个常量与 `_IDI07_INTERACTIVE_JS` / `_IDI07_BUILD_VERDICT_CARD_JS` / `_IDI07_DISABLE_VERDICT_BUTTONS_JS` 三段注入脚本;`_idi07_hover_border_assert` / `_idi07_sc5_filled_assert` / `_idi07_sc5_naive_press_assert` / `_idi07_sc5prime_disabled_assert` 四个断言函数;模块 docstring 新增「第 10 项的交互态半场」段

## Decisions Made

- **D-07 的 gate 落在 L627 的选择器上,不落在新增规则上**(理由见 key-decisions 第 1 条与 `<decision_register>` 的两条取证)。
- **D-08 的 rgba 落点选「围栏内令牌」支**(理由见 key-decisions 第 2 条)。
- **朴素 `:active` 停在 0-1-0,让位由 L627 的 `:where(:not(:active))` 承担**(理由见 key-decisions 第 3 条)。
- **两处值碰撞显式登记**:`--color-surface-active` ↔ `--color-surface-user`(gray-4)、`--color-border-hover` ↔ `--color-text-muted`(gray-11)。前者必须点名 04.1-N-4 并同步扩写既有注释,否则同一份注释自相矛盾。
- **SC5 的填充半场取 `#btn-send` 而非 `#btn-process-round`**(理由见 key-decisions 第 5 条:`#btn-process-round` 在 p1 可见但禁用,断言会 FAIL 而非 BLOCKED)。
- **SC5-朴素按下 的目标取 `renderVerdictCard()` 造出的裁决卡的首个按钮**,且与 SC5′ **共用同一张卡**(顺序承重:SC5-朴素按下 必须先跑)。
- **变异测试的两支都跑了**:去掉让位 ⇒ 2 FAIL;去掉 gate ⇒ 1 FAIL。没有这一步,「探针 PASS」与「探针在工作」无法区分。

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] 围栏内注释里的 `--radix-gray-12:` 被 `check-02` 当成一条声明**
- **Found during:** Task 1(`--color-border-hover` 的令牌注释)
- **Issue:** `scripts/check-02-contrast.py` 的 `DECL_RE`(`(--[a-z0-9-]+)\s*:\s*([^;]+);`)扫的是**围栏全文**,包含注释。注释里写「不取 `--radix-gray-12`: 它是高对比文字步」,该片段被解析成一条名为 `--radix-gray-12` 的声明,其「值」是后面整段散文 ⇒ `FAIL: unparsable value for --radix-gray-12`,exit 1。计划与 PATTERNS 都没有登记这条陷阱(围栏内既有的注释都恰好没有「令牌名 + 冒号」的形态)。
- **Fix:** 把该句改写为「不取那个高对比**文字**步 `--radix-gray-12` 也 —— 那一步作为边框读作近黑」,即让令牌名后面**不跟冒号**。零语义损失,注释仍完整表达「为何不取 gray-12」。
- **Files modified:** `frontend/style.css`
- **Verification:** `.venv/bin/python scripts/check-02-contrast.py` 末行回到 `PASS: 0 failures`;`check-01` / `check-03` / `check-04` 各恰一行 `PASS`。
- **Committed in:** `cd5a1a1`(Task 1 提交)

**2. [Rule 3 - Blocking] 围栏外注释里的 `rgba(` 字面量把围栏外计数从 0 顶成 1**
- **Found during:** Task 2(active 组的注释)
- **Issue:** 本任务的 `<verify>` 要求 `awk` 取围栏外后 `grep -c 'rgba('` == 0。我在 active 组的注释里写了「规则体不写裸 `rgba()`」—— 这是一句**论证性散文**,但判据是子串计数,于是围栏外计数变成 1,门红。
- **Fix:** 改写为「规则体只写 `var()`,不写颜色字面量」。同样零语义损失。
- **Files modified:** `frontend/style.css`
- **Verification:** `awk '/DESIGN TOKENS: START/{f=1} /DESIGN TOKENS: END/{f=0} !f' frontend/style.css | grep -c 'rgba('` 输出 0;`box-shadow: inset 0 0 0 999px` 的围栏外计数为 2。
- **Committed in:** `0b40da5`(Task 2 提交)

**3. [Rule 3 - Blocking] Task 1 的「扩写该分组的注释末句」(④)改为纯新增,以守住任务自己的删除行数预算**
- **Found during:** Task 1(④ 的 overlay 分组注释)
- **Issue:** 计划 ④ 要求「插入两条令牌,并扩写该分组的注释末句」;但同一任务的 `<verify>` 又把删除行数硬限制为 **≤ 2**,并逐字点名那两处就地编辑是「L587 那一行的选择器改写」与「第 3 条注释的扩写」。扩写 overlay 分组注释的末句需要改动它那一行(`rgba() appears outside the fence). */`),会把删除数顶到 3 ⇒ 任务自己的门必红。两条指令直接冲突。
- **Fix:** 把新令牌的注释写成**紧接在 `--color-overlay-backdrop` 声明之后的独立注释块**(纯新增,零删除),措辞上明确承接上面那条分组注释(R-2 的「围栏外不出现裸 rgba」不变量、`box-shadow` 的 inset 零位移、两个 alpha 不进 PAIR 清单)。**语义与计划的四条要求逐条对应,一条未少**;差别只在这段文字的开头是 `/* Tier 2 — the interaction-state scrims…` 而不是挂在原注释的末句里。
- **Files modified:** `frontend/style.css`
- **Verification:** `git diff --numstat -- frontend/style.css` 在 Task 1 提交时为 `114 2` —— 删除数**恰为计划点名的 2**(L627 选择器行 + 第 3 条注释行);`check-01` / `check-02` / `check-03` / `check-04` 与既有九项 UAT 全绿。
- **Committed in:** `cd5a1a1`(Task 1 提交)

---

**Total deviations:** 3 auto-fixed(3 blocking)
**Impact on plan:** 前两条是**同型**的机械陷阱(围栏内注释里的「令牌名 + 冒号」、围栏外注释里的「`rgba(`」子串),都是计划与 PATTERNS 未登记的;修法都只是改写措辞,零语义损失,且已在 `patterns-established` 里各留一条供后续计划复用。第三条是计划内部两条指令的直接冲突(「扩写末句」vs「删除 ≤ 2」),按机械门优先消解为纯新增。**三处均未扩大改动面**:`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` / `scripts/ui-states/` 零改动(硬规则 5),零新增运行时依赖、零构建步骤、零 `!important`、零 `@media`、零 `!important` 声明数不变(T-idi-07-SC 的 accept 面未被触及)。

**一处需要澄清的口径差异(不是偏差,是计划的措辞泛化):** 计划末尾 `<verification>` 的「`git diff --numstat -- frontend/style.css` 的删除行数只允许来自 L587 那一行的选择器改写(≤ 2)」是 **Task 1 的 `<fails_when>` 在计划层级的复述**。本计划在 style.css 上的**实际删除数为 6**,逐条为:①`--color-surface-user. */`(Task 1 ② 的扩写,计划明令)、②`button:hover { … }`(Task 1 的选择器改写,计划明令)、③④⑤⑥ 清单头部计数注释的 4 行(Task 3 明令「改写清单头部计数注释:把 `24 / 34 / 43 / 47 / 50` 改为 `24 / 34 / 43 / 47 / 50 / 52`,并把第五个值层的句子拆成两句」—— 值变了,这几行**不可能**以纯新增完成)。**Task 1 自己的预算是恰好满足的(2)**;多出的 4 行全部来自 Task 3 的具名改写。此处照实登记,不粉饰。

## Issues Encountered

- **三个一次性临时文件仍然删不掉,已按计划的要求如实上报、未采取任何绕过手段。** `.planning/.idi07-dec1.txt` / `.idi07-dec2.txt` / `.idi07-dec3.txt` 是**上一份计划**(`idi-07-01`)的执行器喂给 `gsd-tools query state.add-decision` 的输入文本,其内容已逐字进入 `STATE.md` 的 Decisions 区,不参与任何门或构建。本计划的执行器尝试 `rm -f` 被**权限系统拒绝**(与计划 01 遇到的是同一条拒绝),故它们仍留在工作区且**未提交**。**请手工 `rm` 掉这三个文件。**
- **`.claude/settings.local.json` 在本计划开始时即处于 modified 状态**(会话开始时的 git status 快照里就有),不属本计划的改动面,未提交、未触碰。
- **`timeout` 命令在本机不存在**(`zsh: command not found: timeout`)。本计划的全部 `check-05` 调用改为直接执行 + `tail`/`grep` 过滤,单项最长耗时约 90s,未出现挂死。
- **变异测试用的是「已提交的树 + 定向 `git checkout -- frontend/style.css` 复原」**,不是 `git stash`(本项目明令禁止 —— stash 列表跨工作树共享)。两次变异后 `git status --porcelain` 为空、四条门与 item 10 复跑全绿,可复跑证据完整。

## Known Stubs

无 —— 本计划新增/修改的两个文件里没有硬编码空值、占位文案、TODO/FIXME,也没有「组件没有数据源」的形态。新增的三段注入脚本与四个断言函数**全部被消费**:`_IDI07_INTERACTIVE_JS` 被 4 处调用,`_IDI07_BUILD_VERDICT_CARD_JS` / `_IDI07_DISABLE_VERDICT_BUTTONS_JS` 各被 1 处调用,四个断言函数各被 `item10` 调用一次(`_idi07_hover_border_assert` 两次)。

## Threat Flags

无 —— 本计划只新增声明式 CSS 与测试脚本,未引入任何新的网络端点、认证路径、文件访问模式或信任边界上的 schema 变更。计划 `<threat_model>` 的 T-idi-07-06…11 逐条落到实现面:T-06(填充按钮选择器特异性)由十条选择器各自写明具体特异性 + SC5 在真实浏览器里读 `box-shadow` 承担;T-07(禁用态响应交互)由 L627 的 gate + SC5′ 用真实 `renderVerdictCard` 与真实 `.disabled` 切换承担;T-08(朴素 `:active` 与 hover 的配对)由 0-1-0 的刻意取值 + 两处注释 + SC5-朴素按下 的「③ != ②」承担;T-09(围栏外裸 `rgba()`)由两个 alpha 收进围栏内令牌 + `awk` 取围栏外的显式断言承担;T-19(假 PASS:按下读数只是 hover 读数的回声)由「③ != ②」这半条 + **变异 1 的实测失败**承担;T-10(SC5 / SC5′ 的假 PASS)由三合一前提检查 + 造不出裁决卡即 `blocked` + 先移开指针再抬手承担;T-11(值碰撞被后来者「修正」)由两处登记注释 + L316-320 的同步扩写承担;T-idi-07-SC(npm / pip / cargo 安装)的 accept 面未被触及:零新增运行时依赖、零构建步骤。

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Ready for idi-07-03**(过渡与减弱动效):本计划已把三组追加规则落在文件末尾、把交互态探针的骨架与前提检查(`_IDI07_INTERACTIVE_JS`)留在 item 10 里。计划 03 只需在同一处追加过渡挂载规则与 `@media (prefers-reduced-motion: reduce)` 块 —— **注意 `check-05` 的 `EXPECTED_MEDIA_QUERIES = 0` 必须同步改成 1**(PATTERNS 已登记该冲突面),且 D-13 不得引入任何 `!important`(`check-04` 数的是 `!important;` 声明数,当前为 1)。
- **Phase 7 的交互态契约已完整落地**:hover / active / 禁用态三条语义各有一条可复跑的运行时证据;`--color-surface-active` 与 `--color-border-hover` 的值碰撞已登记,不会被后来者当违规修掉。
- **D-19 的连带复验义务仍在计划 03 Task 3**:`frontend/style.css` 与 `scripts/check-05-ui-uat.py` 的字节在本计划里**再次**变化 ⇒ `.planning/phases/` 下覆盖这两个文件的四份报告(`idi-04` / `idi-04.1-radix` / `idi-05` / `idi-06`)的 `covered_digest` 依然 stale。**本计划不重算它们**(那是计划 03 的活),**也不得**用 `gsd-tools query verification status <phase>` 判定(相位目录命名与该工具的相位令牌解析不匹配,一律返回 `missing`)。`STATE.md` 的 Operator Next Steps 第 2 条(`/gsd-verify-work idi-04.1-radix`)在本计划开始前仍未收口。
- **本计划的验收边界(不得误读)**:SC5 / SC5-朴素按下 / SC5′ 证明的是**计算样式层面的反馈成立与禁用态零反馈**,不是**感知层面**的「一眼看出不可点」—— 后者是计划 03 的具名人工验收项(SC5″),不在本计划内。`#selection-menu button` 的按下态**未被承诺**(它有自己 1-1-1 的 hover 规则,不属朴素族),这是一处有意的负空间。

---

*Phase: idi-07-interaction-states-and-focus*
*Completed: 2026-09-23*

## Self-Check: PASSED

- **Created files exist**: 本计划零新建文件;两份被修改的文件均已在盘(`frontend/style.css` / `scripts/check-05-ui-uat.py`),SUMMARY 自身路径为 `.planning/phases/idi-07-interaction-states-and-focus/idi-07-02-SUMMARY.md`。
- **Commits exist**: `cd5a1a1`(Task 1 FOUND)/ `0b40da5`(Task 2 FOUND)/ `aa7194b`(Task 3 FOUND)—— 见下方 `gsd-tools verify-summary` 的机械复核。
- **`commits` 计数口径**:`git rev-list --count ed63381..HEAD` 在写 SUMMARY 时为 **3**(三条任务提交);本计划的 docs 元数据提交另计一条(见「Task Commits」节),与 `idi-07-01-SUMMARY.md` 同一口径。
- **变异测试的复原判据**:两次变异后 `git status --porcelain` 为空,四条门与 `--item 10` 复跑全绿。

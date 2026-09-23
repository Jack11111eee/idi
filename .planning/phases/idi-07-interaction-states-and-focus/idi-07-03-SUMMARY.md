---
phase: idi-07-interaction-states-and-focus
plan: 03
subsystem: ui
tags: [css, transitions, prefers-reduced-motion, interaction-states, static-contract-guards, uat-harness, playwright, mutation-safety, verification-fingerprints]

# Dependency graph
requires:
  - phase: idi-07-interaction-states-and-focus
    plan: 01
    provides: "文件末尾的追加位置与注释纪律、`check-05` item 10 的骨架与四处登记点、`read_style` / `resolve_color` / `resolve_token` 三个读取器、`check-02` 的 PAIR 清单记账位置、`_l2_guard_shape` 的静态守卫形态"
  - phase: idi-07-interaction-states-and-focus
    plan: 02
    provides: "三组交互态追加规则与 `_IDI07_INTERACTIVE_JS` 前提检查、`_idi07_hover_border_assert` / `_idi07_sc5_naive_press_assert` 两条会被本计划的过渡影响读数的探针(本计划为它们补上终态读取器)"
  - phase: idi-06-layout-robustness
    provides: "`check-05` 的 `EXPECTED_MEDIA_QUERIES = 0` 决策常量(本计划同步为 1)、`CLEARANCE_MIN_PX = 4.0`、`_l2_guard_shape` 的三条共同纪律"
  - phase: idi-04-tokens-contract
    provides: "围栏标记(`===== DESIGN TOKENS: START/END`)与 `check-01` 的 awk 状态机形态(本计划按它切围栏内 / 围栏外两段)"
provides:
  - "`frontend/style.css`:文件末尾的过渡挂载规则 `button, input, select { transition: background-color 120ms, border-color 120ms; }`(特异性 0-0-1)+ 六条承重注释(特异性 / 与 .event-list 零竞争 / 属性列表只有两个 / D-11 的 300ms 具名例外 / `<textarea>` 两处枚举差异 / box-shadow 瞬变)"
  - "`frontend/style.css`:文件末尾的 `@media (prefers-reduced-motion: reduce)` 块(按选择器重写为 `transition: none`,枚举含 `.event-list`,零 `!important`)+ 四条承重注释(为何不采纳行业标准片段 / 为何按选择器重写 / 为何枚举写死 / 为何含 .event-list)"
  - "`scripts/check-05-ui-uat.py`:`EXPECTED_MEDIA_QUERIES` 0 → 1,决策注释 / `info()` / `ok_true` 标签三处同步说明「这是 Phase 7 的减弱动效块,不是 L-2 的窄窗口守卫」"
  - "`scripts/check-05-ui-uat.py`:`_idi07_focus_contract_guards(item)` 四条静态契约计数断言(含 `_idi07_code_only` / `_idi07_focus_rule_blocks` / `_idi07_block_declarations` / `_idi07_fence_split` 四个纯函数)"
  - "`scripts/check-05-ui-uat.py`:`_idi07_transition_motion_assert(page, item, state)` 过渡与减弱动效运行时探针(含 `_idi07_durations` 与 `page.emulate_media(reduced_motion=...)` 的读毕复位)"
  - "`scripts/check-05-ui-uat.py`:`read_settled_style` + `_IDI07_SETTLED_READ_JS` —— 读**过渡终态**的读取器(计划 02 的两条 hover 探针在过渡落地后会读到中间值)"
  - ".planning/phases/idi-07-interaction-states-and-focus/idi-07-VERIFICATION.md:阶段收口记录(status: human_needed;含人工项 5″ 与全部登记面)"
affects: ["Phase 8(A11Y-02 的 `tabindex` 承诺:`#round-doc` 的焦点环承载面必须写内嵌处理 —— 本阶段唯一跨阶段开放项)", "/gsd-verify-work idi-07(独立复核与 covered_files / covered_digest 的写回)", "/gsd-verify-work idi-04 / idi-04.1-radix / idi-05 / idi-06(四份报告的 live 指纹被本阶段作废,D-19 的连带复验义务)", "删除 `frontend/style.css` 的减弱动效媒体块的人:必须同时把 `EXPECTED_MEDIA_QUERIES` 改回 0(B1 的耦合)"]

actuals:
  tokens: 7896      # chars/4 over the realized diff of the two changed files (31584 chars)
  tasks: 3
  commits: 2        # MEASURED: git rev-list --count 346ab0f..HEAD
  plan_head_before: 346ab0f76c0adba358cbdbdd96a6819e830bf27e

tech-stack:
  added: []
  patterns:
    - "**静态契约断言的「块提取」形态**:断言「没有任何焦点规则设置 border / padding」时,必须逐行跟踪 `/* … */` 状态、从选择器行切到第一个 `}`,再只对 `{` 之后的部分数声明 —— 全文件 grep 会数到满地的 border / padding,注释里的 `:focus-visible` 提及还会被误当成规则块。形态同族于 `check-01` 的 awk 状态机,但多了注释状态这一维"
    - "**「判据取终态」:过渡落地后,交互后的一次性读数不再等于终态读数**:给 button / input / select 挂上 120ms 过渡之后,`page.hover()` 后立刻 `getComputedStyle` 会读到**过渡中间值**(实测 `rgb(112,112,112)`,而终态是 `rgb(100,100,100)`)。解不是「把断言放宽」而是「把读数推到终态」:等两帧确保过渡已注册,再 `await` 该元素上所有动画 `finished`"
    - "**「必须全为某值」的断言不得用子串包含**:`transition-duration` 对两个属性序列化成 `\"0.12s, 0.12s\"`,而 `\"0s\"` 是它的子串 —— 用 `\"0s\" in raw` 判「reduce 下全为 0s」会在**未生效**时假绿。判据先按 `,` 拆成列表再逐项比"
    - "**注释散文是机械判据的输入面**:`@media` 的全文件裸子串计数、`!important;` 的带分号声明形态、`transition:.*opacity` 的行匹配 —— 三者都要求注释**改写措辞**而不是照抄被引用的片段。本计划为此在写注释前先列出五个散文陷阱并逐条规避"
    - "**executor 的收口记录必须自陈不是独立验证**:`status: human_needed` + 刻意不声明 `covered_files` / `covered_digest`(声明其一而缺另一会 fail-closed 成 `stale`),并把指纹写回明确留给 verifier —— 因为指纹必须在**全部 PLAN/SUMMARY 都在盘之后**才能算"

key-files:
  created:
    - .planning/phases/idi-07-interaction-states-and-focus/idi-07-VERIFICATION.md
  modified:
    - frontend/style.css
    - scripts/check-05-ui-uat.py

key-decisions:
  - "**`@media` 计数与 `EXPECTED_MEDIA_QUERIES` 是一对同步量,三者(规则、media 块、常量)必须同一次提交。** 只落 media 块不改常量 ⇒ `check-05 --item 8` 的静态守卫立刻变红;只改常量不落块 ⇒ 守卫恒红。故 `frontend/style.css` 的两条追加与 `scripts/check-05-ui-uat.py` 的常量/注释/标签同步**同一次提交**落地,不留红窗"
  - "**决策注释必须把「Phase 7 的减弱动效块」与「L-2 的窄窗口守卫」明确区分开。** 两者都让 `@media` 计数变化,但 L-2 走的是「被实测推翻 ⇒ 守卫不写」支(三宽度仍无破版,该结论未变)。不区分会让后来者把「计数 == 1」读成「L-2 的守卫被写了」—— 标签是断言的一部分,`ok_true` 的 label 与 `info()` 文案一并同步"
  - "**四条契约计数断言落成 `check-05` 内的静态守卫(形态 B),不新建脚本。** `check-06` 编号已被 `scripts/check-06-idi05-validation.py` 占用;且与 Phase 6「扩在既有门」的先例一致,还少一份要连带复验的指纹。断言与运行时项同族(第 10 项),故放同处"
  - "**`prefers-reduced-motion` 与新增过渡的「同提交」断言退化为「两者同时存在」,并在 `info()` 里逐字声明该局限。** 「同提交」是 **git 维度**的事实,文件文本断言在结构上无法证明它 —— 假 PASS 的形态必须点名,不能让读者以为它证明了同提交"
  - "**`--color-focus` 的「已声明且被消费」断言扩展为五个交互态令牌的同形断言**(`--color-surface-active` / `--color-border-hover` / `--color-overlay-hover` / `--color-overlay-active`)。声明侧抓改名残留(声明了两次),消费侧抓死令牌 —— 硬规则 5「与消费者同提交」的机械形态。围栏外只认 `var()` 形态,裸令牌名不是消费"
  - "**计划 02 的两条 hover 探针改用 `read_settled_style`(终态读取器),而不是放宽断言。** 过渡让「交互后立刻读」读到中间值;正确的修法是把读数推到终态(等两帧 + `await` 动画 `finished`),而不是把期望值改成中间值或加容差。其余探针仍用 `read_style`:它们读的量要么不参与过渡(`box-shadow` / `outline`),要么未被交互改变"
  - "**时长判据先拆列表再逐项比,不用子串包含。** `\"0s\"` 是 `\"0.12s, 0.12s\"` 的子串 ⇒ `\"0s\" in raw` 判「reduce 下全为 0s」会在**未实现**时假绿 —— 这正是本项目已记录的同型陷阱(第 7 项 `all(w != \"700\")` 对 None 恒真)"
  - "**收口记录 `idi-07-VERIFICATION.md` 刻意声明 `status: human_needed` 且不声明 `covered_files` / `covered_digest`。** 前者因为本阶段有一条具名人工项(5″),后者因为 #4155 的指纹对是 fail-closed 的,且指纹必须在**本计划自己的 SUMMARY 落盘之后**才能算(`allCurrentArtifactsCovered` 会扫活目录)。指纹写回明确留给 `/gsd-verify-work idi-07`"
  - "**D-19 的四份报告全部判为「内容真变 ⇒ 重新验证」,并逐份给出以 HEAD 内容重算的 digest。** 四份的 `covered_files` 都含 `frontend/style.css`(三份另含 `scripts/check-05-ui-uat.py`),两个文件在本阶段三个计划里都变了字节。**不得**用 `gsd-tools query verification status <phase>` 判定(相位目录命名与相位令牌解析不匹配,一律返回 `missing`);判据只能是逐份比对 `covered_files` + 重算 digest"

patterns-established:
  - "Pattern 1: 静态契约断言的「块提取」必须同时处理**注释状态** —— 否则规则上方的论证散文会被当成规则块,块内计数随即失去意义"
  - "Pattern 2: 过渡落地后,交互类断言的读数必须**推到终态**(等两帧 + `await` `getAnimations()` 的 `finished`),而不是放宽期望值"
  - "Pattern 3: 「全为某值」的断言一律先拆分再逐项比;子串包含会把「未生效」读成「已生效」"
  - "Pattern 4: executor 的收口记录以 `status: human_needed` + 不声明指纹自陈「这不是独立验证」,把 `covered_files` / `covered_digest` 留给 verifier"

requirements-completed: [INTERACT-02]

coverage:
  - id: D1
    description: "过渡挂载规则 `button, input, select { transition: background-color 120ms, border-color 120ms; }`(纯追加、特异性 0-0-1、属性列表只有两个)+ `@media (prefers-reduced-motion: reduce)` 块(按选择器重写为 `transition: none`,枚举含 `.event-list`,零 `!important`)+ `EXPECTED_MEDIA_QUERIES` 0 → 1 三者同一次提交"
    requirement: "INTERACT-02"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 10(p1:button / input / select 的 transition-property 含 background-color 与 border-color、时长两项均 0.12s;.event-list 为 background-color / 0.3s;reduce 下四者全为 0s)"
        status: pass
      - kind: other
        ref: "bash scripts/check-04-important-count.sh(恰一行 PASS —— 未采纳带两个 !important 的行业标准片段)"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 8(静态守卫 `@media` 计数 == 决策 1,13 条断言全 PASS)"
        status: pass
    human_judgment: false
  - id: D2
    description: "D-15 中段的四条契约计数静态守卫(`_idi07_focus_contract_guards`):①`:focus-visible` 计数 >= 1;②没有任何含 `:focus-visible` 的规则块设置 border / padding(块提取);③`prefers-reduced-motion` 与新增过渡同时存在(并逐字声明其不证明「同提交」的局限);④五个交互态令牌围栏内声明 == 1 且围栏外被 `var()` 消费 > 0"
    requirement: "INTERACT-02"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 10(四条静态断言 + 五条逐令牌断言全部 PASS;`:focus-visible` 计数 9、焦点规则块起始行 1492、块内声明仅 outline / outline-offset)"
        status: pass
    human_judgment: false
  - id: D3
    description: "计划 02 的两条 hover 探针改用 `read_settled_style`(终态读取器):过渡落地后 `page.hover()` / `mouse.down()` 后的一次性读数会读到过渡中间值(实测 `rgb(112,112,112)` vs 终态 `rgb(100,100,100)`);修法是把读数推到终态,不是放宽期望值"
    requirement: "INTERACT-02"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 10(SC5-朴素按下 ① rgb(249,249,249) → ② rgb(240,240,240) → ③ rgb(232,232,232);两条 hover 边界断言静默 rgb(141,141,141) → hover rgb(100,100,100);0 FAIL)"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8,9(媒体模拟读毕复位,未污染其后各项;exit 0)"
        status: pass
    human_judgment: false
  - id: D4
    description: "整阶段收口:六条命令复跑全绿、D-19 的四份报告以 HEAD 内容重算 digest 并逐份处置、人工项 5″ 登记、D-11 的 UI-SPEC 修正案、`#round-doc` 的 Phase 8 指派、`EXPECTED_MEDIA_QUERIES` 的耦合、L587 的选择器改写限定、ROADMAP Gates 的 0.55 合成支作废 —— 全部落进 SUMMARY 与 VERIFICATION"
    requirement: "INTERACT-02"
    verification:
      - kind: other
        ref: "idi-07-VERIFICATION.md(六条命令的结论表 + 全部登记面)+ 本 SUMMARY 的「Task 3 收口记录」节"
        status: pass
    human_judgment: false
  - id: D5
    description: "人工验收项 5″:`#btn-authorize` 的禁用态仍一眼看出不可点(未被软化)—— 这是关于**感知**的主张,不是关于数值的主张;机器半场(SC5′)覆盖的是**另一条规则** `.verdict-buttons button:disabled`(opacity 0.5),`#btn-authorize:disabled`(opacity 0.55)今天没有任何机器断言读过它的 opacity"
    verification: []
    human_judgment: true
    rationale: "「一眼看出不可点」是感知判断,机器只能读计算样式(背景是否变化、opacity 是否仍为 0.55),读不出「是否真的没被软化」。D-17 明文:不得把它删掉换成机器代理量 —— 门绿不等于视觉上真的没被软化。逐字登记于 idi-07-VERIFICATION.md 的 Human Verification Required 节"

duration: 33 min
completed: 2026-09-23
status: complete
---

# Phase 7 Plan 03: 过渡与减弱动效 + 契约计数门(整阶段收口)Summary

**把过渡限定在 `background-color` 与 `border-color` 两个属性上(120ms),用 `@media (prefers-reduced-motion: reduce)` 把 `button` / `input` / `select` / `.event-list` 的过渡按选择器重写为 `none` —— 三条产出与 `EXPECTED_MEDIA_QUERIES` 0 → 1 同一次提交;把 D-15 中段的四条契约计数落成 `check-05` 第 10 项里的静态守卫(含必须做块提取的「焦点规则不得设 border / padding」),并为过渡落地后**会读到中间值**的两条既有 hover 探针补上终态读取器;最后完成整阶段收口:六条命令复跑全绿、四份受影响报告的指纹以 HEAD 内容重算并逐份处置、人工项 5″ 与七条登记面落进 SUMMARY 与 VERIFICATION。**

## Performance

- **Duration:** 33 min
- **Started:** 2026-09-23T06:47:04Z
- **Completed:** 2026-09-23T07:19:42Z
- **Tasks:** 3
- **Files modified:** 2(`frontend/style.css` / `scripts/check-05-ui-uat.py`,零新建代码文件;另新建 1 份 planning 产物 `idi-07-VERIFICATION.md`)

## Accomplishments

- **行业标准的减弱动效片段在本项目里被明确排除,并把这个理由写成了注释。** 通行写法(一个通配选择器 + 两个伪元素 + 把 `transition-duration` 压到 0.01ms + **两个 `!important` 声明**)会让 `check-04` 的 `!important;` 声明数从 1 变 3 而立刻变红 —— 而 `.hidden` 的隐藏机制(44 处 `classList` 依赖它)建立在「该计数恒为 1」这条不变量上。本阶段改走**按选择器重写为 `none`** 的路线:它是确定性的、可被 `getComputedStyle` 直接断言的终态,而「几乎为零」不是;枚举写死而非通配,则延续 Phase 5(`G-idi-05-1`)/ Phase 6(`overflow-wrap`)的同一口径 —— 影响面必须可枚举、可对照。
- **`@media` 计数、`EXPECTED_MEDIA_QUERIES` 与断言标签三者同一次提交。** 这是 T-idi-07-13(门恒红 / 恒绿)的缓解面:只落 media 块不改常量 ⇒ `--item 8` 立刻变红;只改常量不落块 ⇒ 守卫恒红。同时把决策注释改写成**明确区分两件事**:计数现在是 1 是因为 **Phase 7 落地了减弱动效块**,而 **L-2 的窄窗口守卫仍走「被实测推翻」支、仍未写出**(三宽度仍无破版)。`ok_true` 的 label 一并改写 —— 标签是断言的一部分,不改会让输出自相矛盾。
- **四条契约计数断言全部落成静态守卫,其中两条是「必须做块提取」的形态。** ①`:focus-visible` 计数 >= 1(判据是 `>=` 而非 `==`:七选择器枚举天然大于 1,相等判据会把「按枚举纪律扩展」误判成回归);②**没有任何含 `:focus-visible` 的规则块设置 `border` / `padding`** —— 逐行跟踪 `/* … */` 状态、从选择器行切到第一个 `}`,再只对 `{` 之后的部分数声明(全文件 grep 会数到满地的 `border` / `padding`,而规则上方那段「为什么枚举而不是裸 `:focus-visible`」的论证散文里的 `:focus-visible` 提及会被误当成规则块);③减弱动效偏好与新增过渡同时存在;④五个交互态令牌围栏内声明 == 1 且围栏外被 `var()` 消费 > 0(硬规则 5 的机械形态,用与 `check-01` 同一对围栏标记切分)。实测:焦点规则块起始行 **1492**、块内声明仅 `outline` / `outline-offset`;五个令牌全部「声明 1 / 消费 1」。
- **「同提交」这条断言的局限被逐字声明。** 「同提交」是 **git 维度**的事实,文件文本断言在结构上无法证明它 —— 故该断言退化为「两者同时存在」,并在 `info()` 里逐字写明它**不证明同提交**,同提交只能落成计划 / 评审义务(T-idi-07-15 的缓解面)。不让读者以为它证明了它没证明的事。
- **过渡与减弱动效有了真正的运行时验证(硬规则 7)。** p1 上实测:button / input / select 的 `transition-property` = `background-color, border-color`、`transition-duration` = `0.12s`(两项);`.event-list` = `background-color` / **`0.3s`** —— **D-11 的具名例外在运行时可见**,不再只是一句写在注释里的说法。随后 `page.emulate_media(reduced_motion="reduce")` 重读四者,全部为 **`0s`**(含 `.event-list`),读毕**立即复位** `reduced_motion="no-preference"`(与 `VIEWPORT_RESTORE` 同级纪律;已由 `--item smoke,1,2,3,4,6,7,8,9` 全绿证明未污染其后各项)。
- **过渡落地暴露了计划 02 两条探针的读数时刻问题,并用「推到终态」而非「放宽期望值」修掉。** 挂上 120ms 过渡后,`page.hover()` 后的一次性 `getComputedStyle` 读到的是**过渡中间值** —— 实测 `#message-input` 读到 `rgb(112, 112, 112)`,而终态是 `rgb(100, 100, 100)`;裁决按钮的悬停 / 按下读数同理(4 条 FAIL)。修法是新增 `read_settled_style`:等两帧确保过渡已注册,再 `await` 该元素上所有动画 `finished`,然后才读数。修复后 item 10 **0 FAIL**,且读数逐位等于终态:`rgb(141,141,141) → rgb(100,100,100)`、`rgb(249,249,249) → rgb(240,240,240) → rgb(232,232,232)`。
- **第 10 项由 26 条断言增至 38 条,`item 10: PASS (38 条断言,0 FAIL,0 BLOCKED)`,exit 0。** 新增 12 条(4 条静态契约 + 5 条逐令牌 + 3 条过渡读数),零 BLOCKED、零空转 PASS。
- **整阶段收口:六条命令复跑全绿。** `check-01` / `check-03` / `check-04` 各恰一行 `PASS`;`check-02` 末行 `PASS: 0 failures`(`^PASS` 行数 **53**,FAIL 0);`check-05 --item smoke,1,2,3,4,5,6,7,8,9,10` **0 FAIL**,item 5 的 2 条 BLOCKED 是需真实 AI 调用的冒烟、已由 `--item 5 --ai-smoke` 补齐为 `PASS (9 条断言,0 FAIL,0 BLOCKED)`;`probe-07-focus-composite.py` exit 0(`ratio=3.45`)。`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` / `scripts/ui-states/` **零改动**。
- **D-19 的连带复验义务被逐份落实:四份报告全部以 HEAD 内容重算 digest 并给出处置。** 四份的 `covered_files` 都含 `frontend/style.css`,其中三份另含 `scripts/check-05-ui-uat.py`;两个文件在本阶段三个计划里都变了字节 ⇒ 四份的 live 指纹全部作废,处置一律是「**内容真变 ⇒ 重新验证**」(不是补指纹)。**没有**使用 `gsd-tools query verification status <phase>` 判定(它对这些相位目录一律返回 `missing`)。
- **人工项 5″ 与七条登记面全部落进 SUMMARY 与 VERIFICATION 两处。** 尤其把 **L587 的选择器改写**写进「阶段性质」,使阶段级的「纯追加」措辞不被下游无条件复述;并把 **ROADMAP Gates 的 0.55 合成支已随 S-4 作废**显式登记,避免收口静默跳过一行 gate 文本。

## Task Commits

Each task was committed atomically:

1. **Task 1: 过渡挂载规则 + prefers-reduced-motion 块 + EXPECTED_MEDIA_QUERIES 同步(三者同一次提交)** - `4892fdf` (feat)
2. **Task 2: 契约计数的静态守卫(D-15 中段)+ 过渡与减弱动效的运行时探针** - `ce189c8` (feat)
3. **Task 3: 整阶段收口 —— 全门复跑、D-19 的指纹重算与披露、人工项 5″ 与 D-11 修正案的登记** —— **本任务零代码改动**(计划的 `<action>` 明文「不新增门,只做收口与披露;全部产出落进 SUMMARY 与 VERIFICATION」),故无独立任务提交;其产物 `idi-07-VERIFICATION.md` 与本 SUMMARY 同随本计划的 docs 元数据提交落地。

**Plan metadata:** 见本计划的 docs 元数据提交(SUMMARY + VERIFICATION + STATE + ROADMAP + REQUIREMENTS)

## Files Created/Modified

- `frontend/style.css` - 文件末尾追加两条:**过渡挂载规则** `button, input, select { transition: background-color 120ms, border-color 120ms; }`(纯追加、特异性 0-0-1,六条承重注释:特异性论证 / 与 `.event-list`(0-1-0)零竞争 / 属性列表只有两个且不含 `opacity` 与 `outline-*` / D-11 的 300ms 具名例外与「本阶段是纯追加,编辑那条声明会打破该性质」 / `<textarea>` 不进本枚举而焦点环枚举含它的有意差异 / `box-shadow` 不在列表里 ⇒ 填充按钮 hover 瞬变);**减弱动效块** `@media (prefers-reduced-motion: reduce) { button, input, select, .event-list { transition: none; } }`(四条承重注释:为何不采纳带两个 `!important` 的行业标准片段 / 为何按选择器重写而不是改时长 / 为何枚举写死而不是用通配 / 为何枚举含 `.event-list`)。本计划在 style.css 上的 diff 是 **51 增 / 0 删** —— 纯追加
- `scripts/check-05-ui-uat.py` - `EXPECTED_MEDIA_QUERIES` 0 → 1 与其决策注释 / `info()` / `ok_true` 标签三处同步;新增常量 `EXPECTED_FOCUS_VISIBLE_MIN` / `FENCE_START_MARKER` / `FENCE_END_MARKER` / `_IDI07_DECLARED_AND_CONSUMED` / `_IDI07_MOTION_TARGETS` / `_IDI07_TRANSITION_DURATION` / `_IDI07_EVENT_LIST_DURATION` / `_IDI07_REDUCED_DURATION`;新增 `_idi07_code_only` / `_idi07_focus_rule_blocks` / `_DECL_PROP_RE` / `_idi07_block_declarations` / `_idi07_fence_split` / `_idi07_durations` / `_idi07_focus_contract_guards` / `_IDI07_SETTLED_READ_JS` / `read_settled_style` / `_idi07_transition_motion_assert`;`item10` 开头调用静态守卫、p1 段插入过渡探针;两条既有探针(`_idi07_hover_border_assert` / `_idi07_sc5_naive_press_assert`)改用 `read_settled_style`;模块 docstring 新增「第 10 项的过渡与减弱动效半场」段
- `.planning/phases/idi-07-interaction-states-and-focus/idi-07-VERIFICATION.md` - **新建**。阶段收口记录(`status: human_needed`):阶段性质(带 L587 限定的措辞)、7 条 Observable Truths、3 个 Required Artifacts、4 条 Key Link、3/3 需求覆盖、ROADMAP Gates 的 0.55 合成支作废登记、**恰一条**人工项 5″(逐字写明「禁用态仍一眼看出不可点」与「门绿不等于视觉上真的没被软化」,并把两个禁用态数值各自的元素与覆盖面分开写清)、五条 Registrations、六条命令的结论表。**刻意不声明 `covered_files` / `covered_digest`** —— 指纹写回留给 `/gsd-verify-work idi-07`

## Decisions Made

- **`@media` 计数、`EXPECTED_MEDIA_QUERIES`、断言标签三者同一次提交**(理由见 key-decisions 第 1 条)。
- **决策注释必须区分「Phase 7 的减弱动效块」与「L-2 的窄窗口守卫」**(理由见 key-decisions 第 2 条)。
- **四条契约计数断言落成 `check-05` 内的静态守卫,不新建脚本**(`check-06` 编号已被占用;与 Phase 6「扩在既有门」的先例一致)。
- **「同提交」断言退化为「两者同时存在」并在 `info()` 里逐字声明局限**(理由见 key-decisions 第 4 条)。
- **「已声明且被消费」扩展为五个交互态令牌的同形断言**,围栏外只认 `var()` 形态。
- **计划 02 的两条 hover 探针改用终态读取器,而不是放宽期望值**(理由见 key-decisions 第 6 条与「Accomplishments」第 6 条)。
- **时长判据先拆列表再逐项比,不用子串包含**(理由见 key-decisions 第 7 条)。
- **收口记录声明 `status: human_needed` 且不声明指纹对**(理由见 key-decisions 第 8 条)。
- **D-19 的四份报告全部判为「重新验证」,并逐份给出以 HEAD 内容重算的 digest**(理由见 key-decisions 第 9 条)。

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] 过渡落地后,计划 02 的两条 hover 探针读到过渡中间值(4 条 FAIL)**
- **Found during:** Task 2(首次跑 `--item 10` 验收)
- **Issue:** 本计划 Task 1 给 `button` / `input` / `select` 挂了 120ms 的 `background-color` / `border-color` 过渡(D-12 的规格)。计划 02 写下的两条探针在 `page.hover()` / `page.mouse.down()` 之后**立刻**读 `getComputedStyle`,于是读到**过渡中间值**:`#message-input` 与动态 `.verdict-note-input` 的 `border-color` 读到 `rgb(112, 112, 112)`(终态 `rgb(100, 100, 100)`);SC5-朴素按下 的 ② 读到 `rgb(245, 245, 245)`(终态 `rgb(240, 240, 240)`)、③ 读到 `rgb(243, 243, 243)`(终态 `rgb(232, 232, 232)`)。**这不是 CSS 写错,是「读数时刻」早于「终态时刻」** —— 两条探针的期望值本身是对的。
- **Fix:** 新增 `_IDI07_SETTLED_READ_JS` + `read_settled_style(page, sel, prop)`:等两帧(确保过渡已被注册,否则 `getAnimations()` 可能为空)再 `await` 该元素上所有动画 `finished`,然后才读数 —— **判据取终态**。改用于 `_idi07_hover_border_assert` 与 `_idi07_sc5_naive_press_assert` 的交互后读数(含它们的「静默」基线读,以免读到上一步的**反向**过渡中间值)。**刻意不用「放宽期望值 / 加容差 / 改读中间值」** —— 那会把过渡的瞬时行为写进契约。其余探针仍用 `read_style`(它们读的量要么不参与过渡,要么未被交互改变,加等待只会拖慢 harness)。
- **Files modified:** `scripts/check-05-ui-uat.py`
- **Verification:** `--item 10` 由 `FAIL (38 条断言,4 FAIL,0 BLOCKED)` 变为 `PASS (38 条断言,0 FAIL,0 BLOCKED)`,exit 0;读数逐位等于终态(`rgb(141,141,141) → rgb(100,100,100)`、`rgb(249,249,249) → rgb(240,240,240) → rgb(232,232,232)`)。变异面已由计划 02 的两支变异测试覆盖(去掉 L728 的让位 ⇒ ③ 读到 ②;去掉 gate ⇒ SC5′ FAIL),本修复不改变那两支的判别力。
- **Committed in:** `ce189c8` (Task 2 提交)

---

**Total deviations:** 1 auto-fixed(1 bug)
**Impact on plan:** 该偏差是**跨计划耦合**的直接后果(Task 1 的过渡 + 计划 02 的探针),不是计划写错,也不扩大改动面:修法只新增一个读取器并把两处读数换成它,`frontend/app.js` / `frontend/index.html` / `frontend/vendor/` / `scripts/ui-states/` 零改动(硬规则 5),`check-01`…`check-04` 四条既有门与既有九项 UAT 全绿,零新增运行时依赖、零构建步骤、零 `!important` 新增(T-idi-07-SC 的 accept 面未被触及)。**若没有这条修复,计划 03 会以 4 条 FAIL 收尾,而失败原因会被误读成「CSS 坏了」。**

## Task 3 收口记录(本计划的收口与披露 —— 全部产出落进 SUMMARY 与 VERIFICATION,不落进代码)

### (1) 全门复跑,逐条记录原始输出

| # | 命令 | 结论(原始输出 / 判据) |
|---|------|------------------------|
| 1 | `bash scripts/check-01-token-conformance.sh` | `PASS`(围栏外裸 `#hex` 计数 0、tier-1 `var()` 泄漏 0) |
| 2 | `.venv/bin/python scripts/check-02-contrast.py` | 末行 `PASS: 0 failures`;`^PASS` 行数 **53**;`^FAIL` 行数 **0**;exit 0 |
| 3 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS`(`.hidden {` 规则计数恒为 1) |
| 4 | `bash scripts/check-04-important-count.sh` | `PASS`(`!important;` **声明**数恒为 1 —— 注意不是 `!important` 命中数,后者为 3,其中 2 处是注释散文) |
| 5 | `.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,5,6,7,8,9,10` | **0 FAIL**;逐项 `smoke PASS(9)` / `1 PASS(45)` / `2 PASS(5)` / `3 PASS(17)` / `4 PASS(65)` / **`5 BLOCKED(9 条断言,0 FAIL,2 BLOCKED)`** / `6 PASS(6)` / `7 PASS(38)` / `8 PASS(13)` / `9 PASS(16)` / `10 PASS(38)`。item 5 的 2 条 BLOCKED 是**需真实 AI 调用**的交互冒烟(默认不执行,note 写明「加 `--ai-smoke` 重跑」),已用 `.venv/bin/python scripts/check-05-ui-uat.py --item 5 --ai-smoke` 补齐 ⇒ **`item 5: PASS (9 条断言,0 FAIL,0 BLOCKED)`,exit 0** |
| 6 | `.venv/bin/python scripts/probe-07-focus-composite.py` | exit 0;`archive-state opacity=0.75`、`links-before=0 → links-after=1 (mutation-applied=yes)`、`ring outline-color=rgb(31, 99, 189) outline-width=2px`、`composited=(86, 136, 204) ratio=3.45 (>= 3.0)` |

**执行前基线对照(与 PATTERNS 的 HEAD 基线同口径):** 四条不变量门在本计划开始前即为 `PASS` / `PASS: 0 failures` / `PASS` / `PASS`;执行后逐条不变。`@media` 计数由基线 **0** 变为 **1**(Task 1 的交付物,与常量同步);`!important;` 声明数恒为 **1**;PAIR 清单恒为 **52 对 + 1 条 ORDER**(本计划不新增 PAIR);`^PASS` 行数恒为 **53**。

**其余两条 Task 3 判据:** `git status --porcelain -- frontend/app.js frontend/index.html frontend/vendor/ scripts/ui-states/` **输出为空**(硬规则 5 的零改动面);`grep -o 'inline-error' frontend/style.css | wc -l` = **1**(Phase 8 的既有回归门在本阶段结束时仍成立)。

`git diff --numstat 69dea49 HEAD -- frontend/style.css` = `354 4`(354 增 / 4 删):第 1 列非 0 ✓;**第 2 列的 4 行删除逐条核对**为 —— `--color-surface-user. */`(计划 02 Task 1 明令的注释扩写)、PAIR 清单头部计数注释的两行(计划 02 Task 3 明令的具名改写)、`button:hover { background: var(--color-surface-hover); }`(计划 02 Task 1 明令的 **L587** 选择器改写)。**本计划自身的 diff 是 51 增 / 0 删,零删除**;计划的 `<fails_when>` 期望「删除行数只来自 L587 那一行」在**阶段级**不成立(计划 02 已在其 SUMMARY 的「一处需要澄清的口径差异」节照实登记那三行),此处按实记录,不粉饰。

### (2) D-19 的指纹重算与披露(四份报告,逐份)

**判据(不得用工具代替):** 以 **HEAD 内容**重算(不看 mtime);逐份比对 `covered_files` 是否覆盖 `frontend/style.css` / `scripts/check-05-ui-uat.py`;**不得**用 `gsd-tools query verification status <phase>` 判定 —— 该命令对这四份报告一律返回 `missing`(相位目录命名与工具的相位令牌解析不匹配)。重算命令:`gsd-tools verification fingerprint <phase-dir> <covered_files…> --raw`(覆盖文件是**位置参数**,不是 `--files`)。

| 报告 | 覆盖 `frontend/style.css` | 覆盖 `scripts/check-05-ui-uat.py` | 记录的原 digest | **以 HEAD 内容重算的 digest** | 处置 |
|---|---|---|---|---|---|
| `idi-04`(`idi-04-tokens-contract`) | ✓ | ✗ | `v1:sha256:4fd8b793e5777c1fbade75b5b420e1507efb567fb09a5fc76717eae2e7e13cf0` | `v1:sha256:dc2b2ac842005352f3e3ed4464603a4167bc82fcafa05e0a55804f2a2445652d` | **重新验证**(内容真变) |
| `idi-04.1-radix` | ✓ | ✓ | `v1:sha256:25d5f1fe52eaceb48939c1bc76bcd44734bb23f035a02b22f0017724475cb5f2` | `v1:sha256:7c9f562a12ce814ba836b0d8dd1145b6a03b12e6c56de2afbc1e7f98699be01a` | **重新验证**(内容真变;**且该报告早已是 `STATE.md` Operator Next Steps 第 2 条的未收口项**) |
| `idi-05`(`idi-05-typography-and-visual-hierarchy`) | ✓ | ✓ | `v1:sha256:300abaa46994338413693e446a8b89c6cea569a3c3284ea05cd397f8c86bd718` | `v1:sha256:85f7e18f245fd3fa25c4325573ba8713c787bf0a4f3c6f6d491b3ae2b9c8295b` | **重新验证**(内容真变) |
| `idi-06`(`idi-06-layout-robustness`) | ✓ | ✓ | `v1:sha256:c07e99941c1b4faa69ee947096db982c3407eb32f7a8617cff319a8944039ae4` | `v1:sha256:043f7f11537d73c37e66cc8f930651999ba9517832e904f99288f23f3d030ef4` | **重新验证**(内容真变) |

**为什么四份全是「重新验证」而不是「重算 + 披露」:** 四份的 `covered_files` 都含 `frontend/style.css`(三份另含 `scripts/check-05-ui-uat.py`),而这两个文件在本阶段三个计划里都**真的变了字节** —— 属于「内容真变」这一支,补救方向是**重新验证**,不是补指纹。**「重算 + 披露」只适用于记账性编辑**(例如 `REQUIREMENTS.md` 的复选框翻转),本阶段确实也会产生一次那样的编辑(INTERACT-02 翻为 Complete),故本计划在末尾额外披露:该次翻转会让这四份的 digest **再次**变化,而那一支才是「重算 + 披露」。

**已收集的复验证据(供 verifier 使用,不代替它):** 四份各自的**自身门**已在 HEAD 上复跑并全绿 —— `idi-04` 的 check-01/02/03/04(见上表第 1-4 行)+ check-05 items 1-6;`idi-04.1-radix` 的 check-01/02 + `scripts/probe-05-resolve-color.py`(**exit 0**,变异证明仍成立:`mutation-applied=yes`、`pre-fix verdict=PASS` / `post-fix verdict=BLOCKED` / `control-verdict=PASS`);`idi-05` 的 `scripts/check-06-idi05-validation.py`(**exit 0**,逐项全 PASS)+ check-05 item 7(`PASS,38 条断言`);`idi-06` 的 check-05 item 8(`PASS,13 条断言`)/ item 9(`PASS,16 条断言`)。**四份报告文件本身零改动**;`covered_files` / `covered_digest` 的**写回**留给 `/gsd-verify-work`。

### (3) 人工验收项 5″ 的登记(D-17)

本阶段**只有一条**人工项:`#btn-authorize` 的禁用态**仍一眼看出不可点**。它是关于**感知**的主张,不是关于数值的主张。已逐字写进 `idi-07-VERIFICATION.md` 的 manual list,并把两个禁用态数值各自的元素与覆盖面**分开写清,不混成一个值**:

- **机器半场**(`check-05` 第 10 项的 **SC5′**)覆盖的是 **`.verdict-buttons button:disabled`**(HEAD **L1363**,**朴素**按钮),它断言 hover 时背景与静默**相同**(`rgb(249,249,249)`)且计算 `opacity` 仍为 **0.5**;
- **人工项针对的 `#btn-authorize:disabled`**(HEAD **L1247**)是**另一条规则**、`opacity` 为 **0.55**,它的 hover 零反馈由同一处 gate(HEAD **L728** 的选择器)承担,但**今天没有任何机器断言读过它的 `opacity`**。

人工半场要回答的问题正是:**门绿不等于视觉上真的没被软化**。**不得把它删掉换成机器代理量。**

### (4) D-11 的修正案(登记面因「本阶段没有 UI-SPEC」而收窄)

300ms 例外的登记面是 **CONTEXT(已由 `07-CONTEXT.md` D-11 满足)+ 新过渡规则的围栏注释(本计划 Task 1 已落)**;**UI-SPEC 那一处登记面不存在** —— 原因是本阶段没有 UI-SPEC 且 `idi-07-03-PLAN.md:71` 明文**禁止创建**它(「不得为了凑齐三处而新建 UI-SPEC 文件」)。**不得据此认为例外未登记。**

### (5) 本阶段唯一跨阶段的开放项

**`#round-doc` 的焦点环承载面指派给 Phase 8(D-06)。** Phase 7 的枚举含 `[tabindex]`(今天全站计数 0,是防御性非冗余写法);Phase 8 加 `tabindex="0"` 时那条规则会**自动**把环套到一个数千像素高的盒子上 —— 只有上下边缘可见,且落在 `.archive-mode` 的 0.75 合成里。**Phase 8 必须写内嵌处理**(`outline-offset: -2px` 或把环落在 `#doc-pane`)。已登记于本 SUMMARY 与 `idi-07-VERIFICATION.md` 两处。

### (6) B1 的耦合

`EXPECTED_MEDIA_QUERIES` 已随 media 块同步为 **1**;**若日后有人删除该 media 块,必须同时把常量改回 0**,否则 `check-05 --item 8` 会误报。

### (7) 本阶段唯一的非追加编辑(L587 的选择器改写)—— 使阶段级的「纯追加」声明不被下游无条件复述

`ROADMAP.md` Phase 7 的 Rationale 原文是「**纯追加** —— 不编辑任何既有规则」;本阶段实际有**且仅有**一处就地编辑:`frontend/style.css` 的 `button:hover` 选择器被改写为 `button:where(:not(:disabled)):hover:where(:not(:active))`(**规划期记作 L587,HEAD 上在 L728**;声明体逐字节不变,特异性改写前后逐位相同,均为 0-1-1;**匹配集收窄两处** —— 禁用按钮(D-07)与按住不放中的按钮(D-09 的朴素按下态需要 hover 让位);理由与取证见计划 02 的 `<decision_register>` 与 D-09 那张逐族核对表)。另有三行**注释**的就地改写(计划 02 明令)。

⇒ 本 SUMMARY 与 `idi-07-VERIFICATION.md` 复述「纯追加」时**都带这个限定**(写成「除 **L587** 的选择器改写与那三行注释改写外纯追加」);`07-CONTEXT.md` 的禁令面更窄(只禁「编辑既有规则的**声明**」),该改写不触犯它,但 ROADMAP 的阶段级措辞更宽,**不得无条件复述**。

### (8) ROADMAP Phase 7 Gates 里那行 0.55 / 0.75 门的作废半场

`ROADMAP.md` 的 Gates 原文含「每个环都对 **0.55** 与 **0.75** 合成背景验过」。

- **0.75 半场有门**:三条 `--color-focus` PAIR(计划 01),其中 `@0.75` 那条由 `check-02` 的 alpha 合成承担(实测 **3.45 >= 3**);归档半场的**运行时**空缺已由 D-18 显式登记,并由一次性探针 `probe-07-focus-composite.py` 补上可复跑证据。
- **0.55 半场整行作废**:那个 `opacity: 0.55` 已由 **S-4 删除**(`07-CONTEXT.md` D-02 第 1 条),`#round-doc.round-frozen`(HEAD **L1226-1229**)今天只剩 `filter: saturate(0.6)` + 琥珀 `box-shadow: inset 3px 0 0 var(--color-action-warning)`。**`filter: saturate()` 不是 alpha 合成** —— 它不做「环色与地面按比例混合」这件事 ⇒ Pitfall 5 的「被祖先 `opacity` 相乘」那一支**已不存在**,没有任何 0.55 合成背景可供验色。
- **结论与动作:不新增 PAIR、不改任何代码、也**不得**把这行 gate 当成「已满足」。** 该 gate 的 0.55 支**无服务对象,已随 S-4 作废**;存活的 `filter` 不构成合成背景。**不登记 = 阶段收口静默跳过一行 ROADMAP gate 文本**,与 D-02 的登记纪律相悖 —— 故本 SUMMARY 与 VERIFICATION 两处都写了。

## Issues Encountered

- **`verification fingerprint` 的覆盖文件是位置参数,不是 `--files`。** 首次调用 `node gsd-tools.cjs verification fingerprint <phase-dir> --files frontend/style.css` 报 `could not compute fingerprint — a covered file is missing, unreadable, or escapes the project root` —— 根因是 `--files` 被当成一个**文件名**参与了解析(路由源码是 `cmdVerificationFingerprint(cwd, args[2], args.slice(3), raw)`)。改为位置参数后四份全部算出。此处记录以免后来者重踩。
- **`check-02` 必须用 `.venv/bin/python` 调用,不能用 `bash`。** 我一次误用 `bash scripts/check-02-contrast.py` 触发了 shell 对 Python 源码的解释(一屏 `command not found`)。改用 `.venv/bin/python` 后末行 `PASS: 0 failures`。环境 `python3` 是 miniconda,故一律走 `.venv/bin/python`(本项目已记录的纪律)。
- **三个一次性临时文件仍然删不掉,已照实上报、未采取任何绕过手段。** `.planning/.idi07-dec1.txt` / `.idi07-dec2.txt` / `.idi07-dec3.txt` 是**计划 01** 的执行器喂给 `state.add-decision` 的输入文本(内容已逐字进入 `STATE.md` 的 Decisions 区),不参与任何门或构建。本执行器未再尝试 `rm`(该命令在本环境被权限系统拒绝,计划 01 与 02 都已记录)。**请手工 `rm` 掉这三个文件。**
- **`.claude/settings.local.json` 在会话开始时即处于 modified 状态**(会话起始的 git status 快照里就有),不属本计划的改动面,未提交、未触碰。
- **`git status --porcelain` 里除 `.planning/` 与 `.claude/settings.local.json`(会话起始即 modified)外无其他文件** —— 与 Task 3 的判据一致。
- **环境事实(照旧,未对抗)**:截图不可用 ⇒ 全部验收走计算样式读数;浏览器走默认 `--browser bundled`(Playwright 自带 chromium,可无头);`page.emulate_media(reduced_motion=...)` 是页面级状态,读毕立即复位(`--item smoke,1,2,3,4,6,7,8,9` 全绿即为未污染的实证)。

## Known Stubs

无 —— 本计划新增/修改的两个代码文件里没有硬编码空值、占位文案、TODO/FIXME,也没有「组件没有数据源」的形态。新增的常量与函数**全部被消费**:`EXPECTED_FOCUS_VISIBLE_MIN` 被断言与 `info()` 各用一次;`FENCE_START_MARKER` / `FENCE_END_MARKER` 被 `_idi07_fence_split` 使用;`_IDI07_DECLARED_AND_CONSUMED` 被逐令牌断言遍历;`_IDI07_MOTION_TARGETS` 被运行时探针的两段各遍历一次;`_IDI07_TRANSITION_DURATION` / `_IDI07_EVENT_LIST_DURATION` / `_IDI07_REDUCED_DURATION` 各被一条断言消费;`read_settled_style` 被两处探针共 5 次调用;`_idi07_focus_contract_guards` 被 `item10` 调用一次。

## Threat Flags

无 —— 本计划只新增声明式 CSS 与测试脚本,未引入任何新的网络端点、认证路径、文件访问模式或信任边界上的 schema 变更。计划 `<threat_model>` 的 T-idi-07-12…18 逐条落到实现面:**T-12**(采纳行业标准减弱动效片段)由围栏注释逐字点名「该片段带两个 `!important` 会让 `check-04` 从 1 变 3」+ `check-04` 作为 Task 1 的第一条 verify 承担;**T-13**(`EXPECTED_MEDIA_QUERIES` 与 `@media` 实际计数不同步 ⇒ 门恒红/恒绿)由常量 / 注释 / 断言标签三处与 media 块**同一次提交**承担,并由 Task 3 登记「删除 media 块必须同步改回 0」的耦合;**T-14**(既有的 `.event-list` 300ms 声明被改动)由 `git diff` 断言该行未出现在 diff 中 + 运行时探针读到 `.event-list` 的 `0.3s` 承担(把「例外仍在」变成可观测事实);**T-15**(假 PASS:「同提交」的静态断言)由断言退化为「两者同时存在」并**在 `info()` 里逐字声明它不证明同提交**承担;**T-16**(焦点环被加进过渡列表)由围栏注释写明「过渡焦点环是已知的无障碍反模式」+ 静态判据 `grep 'transition:.*outline'` 计数为 0 承担;**T-17**(本阶段作废的验证指纹)由以 HEAD 内容重算四份 digest + 逐份处置 + 明令禁止用 `query verification status` 判定承担;**T-18**(人工验收项 5″)由逐字写进 VERIFICATION 的 manual list 并写明机器半场覆盖了什么、人工半场要回答什么承担;**T-idi-07-SC**(npm / pip / cargo 安装)的 accept 面未被触及:零新增运行时依赖、零构建步骤。

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Phase 7 的三个计划全部交付,阶段可以收口。** 六条命令在 HEAD 上全绿;三条需求(A11Y-01 / INTERACT-01 / INTERACT-02)的机器判据全部成立;唯一的非机器项是人工项 5″。
- **`/gsd-verify-work idi-07` 是下一步**(含独立复核 + `covered_files` / `covered_digest` 的写回)。本计划已把输入备齐:收口记录 `idi-07-VERIFICATION.md`(刻意不声明指纹对)、六条命令的结论、四份受影响报告的重算 digest 与逐份处置。
- **D-19 的连带复验义务已披露但未闭合**:`idi-04` / `idi-04.1-radix` / `idi-05` / `idi-06` 四份报告的 live 指纹被本阶段作废(内容真变),各自的自身门已在 HEAD 上复跑全绿,但**指纹写回与独立复核仍欠 `/gsd-verify-work`**。其中 `idi-04.1-radix` 本就是 `STATE.md` Operator Next Steps 第 2 条的未收口项。
- **Phase 8 的接口已就位且有一条必办项**:枚举含 `[tabindex]`,Phase 8 给 `#round-doc` 加 `tabindex="0"` 时那条规则会**自动**把环套上去 —— **Phase 8 必须为 `#round-doc` 写内嵌处理**(`outline-offset: -2px` 或把环落在 `#doc-pane`)。这是本阶段唯一跨阶段的开放项,已在 `07-CONTEXT.md` 的 deferred 与 canonical_refs、本 SUMMARY、`idi-07-VERIFICATION.md` 四处登记。
- **删除 media 块的人请注意 B1 的耦合**:必须同时把 `EXPECTED_MEDIA_QUERIES` 改回 0。
- **本计划的验收边界(不得误读)**:第 10 项的四条静态契约断言证明的是**文件文本层面**的契约计数(计数 > 0、块内无 border/padding、两者同时存在、令牌声明与消费配对),**不证明**「同提交」;过渡探针证明的是**计算样式层面**的时长与属性列表,不是**视觉**上的动效观感;而 SC5″(「一眼看出不可点」的感知主张)是本阶段的具名人工项,不在机器半场内。

---
*Phase: idi-07-interaction-states-and-focus*
*Completed: 2026-09-23*

## Self-Check: PASSED

- **Created files exist**: `.planning/phases/idi-07-interaction-states-and-focus/idi-07-VERIFICATION.md` FOUND;`.planning/phases/idi-07-interaction-states-and-focus/idi-07-03-SUMMARY.md` FOUND(本文件)。两份被修改的代码文件均已在盘(`frontend/style.css` / `scripts/check-05-ui-uat.py`)。
- **Commits exist**: `4892fdf`(Task 1 FOUND)/ `ce189c8`(Task 2 FOUND)—— 见下方机械复核。Task 3 零代码改动,故无独立任务提交(计划明文「不新增门,只做收口与披露」)。
- **`commits` 计数口径**:`git rev-list --count 346ab0f76c0adba358cbdbdd96a6819e830bf27e..HEAD` 在写 SUMMARY 时为 **2**(两条任务提交);本计划的 docs 元数据提交另计一条(见「Task Commits」节),与 `idi-07-01-SUMMARY.md` / `idi-07-02-SUMMARY.md` 同一口径。
- **`actuals.tokens` 口径**:`git diff 346ab0f..HEAD -- frontend/style.css scripts/check-05-ui-uat.py | wc -c` = **31584** 字符,`/4` = **7896** —— 与计划 `estimate.tokens: 66000` 同一尺度(chars/4 over the realized diff),照实记录不向估算靠拢。
- **阶段性质的两处限定已机械复核**:`grep -c 'L587'` 在 `idi-07-03-SUMMARY.md` 与 `idi-07-VERIFICATION.md` 两份产物里各 >= 1;`grep -c '0.55'` 与 `grep -c 'saturate'` 同样两份各 >= 1。
- **VERIFICATION 的人工项计数**:`grep -c '^### 1\.'` = **1**(恰一条人工项 5″),且它逐字含「禁用态仍一眼看出不可点」与「门绿不等于视觉上真的没被软化」。

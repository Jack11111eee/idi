---
phase: idi-07-interaction-states-and-focus
plan: 03
type: execute
wave: 3
depends_on: [idi-07-02]
files_modified:
  - frontend/style.css
  - scripts/check-05-ui-uat.py
autonomous: true
requirements: [INTERACT-02]
estimate:
  tokens: 66000
  raw_tokens: 66000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "控件的过渡只声明 background-color 与 border-color 两个属性,时长 120ms,落在 INTERACT-02 的「约 120–150ms」区间内(D-12)"
    - "在 prefers-reduced-motion: reduce 下,button / input / select / .event-list 的计算 transition-duration 为 0s(D-13)"
    - "既有的 .event-list 300ms 过渡被保留、一个字节未改,并被登记为具名例外(D-11)"
    - "全站 !important 声明数仍恒为 1;.hidden 规则仍恒为 1 条;@media 出现次数恰为 1 且与 check-05 的决策常量一致"
    - ":focus-visible 计数 > 0;没有任何焦点规则设置 border 或 padding;--color-focus 已声明且被消费"
  artifacts:
    - "frontend/style.css:末尾的 button, input, select { transition: background-color 120ms, border-color 120ms; } 挂载规则 + 其 D-11 例外登记注释"
    - "frontend/style.css:末尾的 @media (prefers-reduced-motion: reduce) 块(枚举含 .event-list,无任何 !important)"
    - "scripts/check-05-ui-uat.py:EXPECTED_MEDIA_QUERIES 0 → 1 及其注释/标签同步"
    - "scripts/check-05-ui-uat.py:_idi07_focus_contract_guards(item) 静态契约计数守卫"
    - "scripts/check-05-ui-uat.py:第 10 项的过渡与减弱动效运行时探针(含 page.emulate_media(reduced_motion='reduce'))"
  key_links:
    - "新增 transition 与 @media (prefers-reduced-motion: reduce) 必须在**同一次提交**(硬规则:减弱动效偏好必须与任何新增 transition 一起落地)"
    - "@media 计数与 check-05 的 EXPECTED_MEDIA_QUERIES 是一对同步量:落一块就改常量,否则 item 8 的静态守卫立刻变红"
    - "挂载规则的特异性 0-0-1,与 .event-list(0-1-0,不同元素)零竞争"
  prohibitions:
    - "不得采用行业标准的 *, *::before, *::after { transition-duration: 0.01ms !important } 片段(两个 !important 会让 check-04 立刻变红)"
    - "不得写 * { transition: all } 或任何全局通配 transition"
    - "不得编辑既有的 .event-list { transition: background-color 0.3s } 一个字节"
    - "不得把 opacity 加进任何 transition 的属性列表(禁用态与焦点环都必须是瞬变)"
    - "不得把 outline-color / outline-width 加进 transition 的属性列表"
    - "不得新增 !important、@layer、@property、var(--x, #fallback)、任何运行时依赖或构建步骤"
    - "不得触碰 .hidden 规则、.fatal 修饰符、#selection-menu 的 DOM 位置、showInlineError、renderAnnotations、renderVerdictCard"
    - "不得编辑 frontend/app.js、frontend/index.html、frontend/vendor/"
---

<objective>
把过渡限定在明确允许的属性上、尊重减弱动效偏好,并把本阶段的契约变成可执行的门(INTERACT-02 / D-11 / D-12 / D-13 / D-14 / D-15 / D-19 / D-20)。

本计划交付四件事:①末尾追加一条**独立的挂载规则** `button, input, select { transition: background-color 120ms, border-color 120ms; }`(纯追加,不改任何既有基础规则体);②追加 `@media (prefers-reduced-motion: reduce)` 块,按选择器把 `transition` 重写为 `none`,枚举含 `.event-list`;**与①同一次提交**;③把 `check-05` 的 `EXPECTED_MEDIA_QUERIES` 从 0 同步为 1(否则 item 8 的静态守卫立刻变红);④把 D-15 中段的四条**契约计数静态断言**落成 `check-05` 第 10 项内的静态守卫,并做整阶段收口。

Purpose: `!important` 声明数必须恒为 1(硬规则 2/4),而**行业标准的减弱动效片段带两个 `!important`** —— 本项目里那条惯例根本不存在。本计划是「项目的全局硬规则会排除行业惯例」的具体实例。
Output: 一条过渡挂载规则、一个 `@media` 块、`EXPECTED_MEDIA_QUERIES` 的同步、第 10 项的静态契约守卫、以及整阶段的门禁收口与指纹披露。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/REQUIREMENTS.md
@.planning/phases/idi-07-interaction-states-and-focus/07-CONTEXT.md
@.planning/phases/idi-07-interaction-states-and-focus/idi-07-PATTERNS.md
@.planning/phases/idi-07-interaction-states-and-focus/idi-07-01-SUMMARY.md
@.planning/phases/idi-07-interaction-states-and-focus/idi-07-02-SUMMARY.md
</context>

<decision_register>
**D-11 的登记面因「本阶段没有 UI-SPEC」而收窄(必须显式记账,不得静默丢掉)。** D-11 要求 300ms 例外同时写进 CONTEXT、**UI-SPEC 的字面量/例外清单**、以及新过渡的围栏注释。本阶段的确定性门(`ui.plan-gate`)返回 `block: false`、自动链标志为 false,故**不会生成 UI-SPEC,也不得创建 UI-SPEC 文件**。因此登记面收窄为两处:**CONTEXT.md(已由 07-CONTEXT.md D-11 满足)+ 新过渡规则的围栏注释(本计划 Task 1)**。第三处(UI-SPEC)以**修正案**形式在本计划的 SUMMARY 与 VERIFICATION 里记明「该登记面不存在,原因是没有 UI-SPEC;不得据此认为例外未登记」。**不得为了凑齐三处而新建 UI-SPEC 文件。**

**D-14 派生结论(焦点环必须瞬变)。** `outline-color` / `outline-width` **不在** INTERACT-02 允许过渡的三个属性内,故环的出现与消失是硬切。**这是正确的** —— 过渡焦点环是已知的无障碍反模式(延迟的焦点反馈)。规划期不得为「让环更柔和」把它加进过渡列表。本计划的静态守卫与围栏注释都要守住这一条。

**Claude's Discretion 裁定:`<textarea>` 不进新过渡的枚举。** 全站 `<textarea>` 计数为 0;过渡枚举只列**真实存在**的控件(与 D-12 的片段一致)。焦点环枚举含 `textarea` 是另一件事 —— D-05 要求它与 `check-05` 的普查集**逐字同集**,故那里保留。两处枚举的差异必须写进注释,否则会被读成不一致。
</decision_register>

<tasks>

<task type="auto">
  <name>Task 1:过渡挂载规则 + prefers-reduced-motion 块 + EXPECTED_MEDIA_QUERIES 同步(三者同一次提交)</name>
  <files>frontend/style.css, scripts/check-05-ui-uat.py</files>
  <read_first>
    - frontend/style.css(L594-605 的 `.event-list` 及其 `transition: background-color 0.3s;` 与 `.streaming` / `.aborted` 两个状态类;L1238-1242 的 `button, input, select { color: var(--color-text); }` 及其「元素选择器特异性 0-0-1」注释 —— 这是挂载规则的**直接范本**;L1227-1324 的文件末尾追加区;L13-16 的 `!important` 注释散文)
    - scripts/check-05-ui-uat.py(L1596-1628 的 `MEDIA_QUERY_DECL` / `EXPECTED_MEDIA_QUERIES` / `_l2_guard_shape` 及其注释块,尤其 L1598-1601 的「若日后实测证成并写出守卫,把这里改成 1 并同步更新 SUMMARY 的决策记录与 UI-SPEC §L-2」;L1763 起的 `item8` 里对 `_l2_guard_shape(item)` 的调用点;L166-190 的 `ok_true` / `blocked` / `info`;L281-282 `read_style`;L392-402 `resolve_token`)
    - scripts/check-04-important-count.sh(数的是 `!important;` **声明**,不是 `!important` 命中 —— 直接数命中会得 3,其中 2 处是注释散文)
  </read_first>
  <action>
    追加过渡挂载规则。在文件末尾、`button, input, select { color: var(--color-text); }`(L1242)之后追加一条**独立的**元素选择器规则:

    `button, input, select { transition: background-color 120ms, border-color 120ms; }`

    **纯追加**:不编辑 `button { … }`(L578)/ `#ai-route-select` / `#project-path-input` 等任何既有规则体。时长取 **120ms**(在 INTERACT-02 的「约 120–150ms」区间内);**不显式声明缓动**(浏览器默认 `ease`)。

    该规则的注释必须写明六件事:

    1. **特异性 0-0-1**,所以 `button.danger`(0-1-1)、`#btn-*`(1-0-0)、`.overlay-card button`(0-1-1)全部仍然取胜 —— 与上面 L1238-1242 的同类规则同一理由,照它的论证形态写。
    2. **与 `.event-list`(0-1-0)零竞争** —— 不同元素,且 `button, input, select` 不匹配 `.event-list`。
    3. **属性列表只有两个** —— `background-color` 与 `border-color`;**不含 `opacity`**(D-14:禁用态是 G3 前提条件唯一的视觉信号,应当被立即感知;0.55 的淡入容易被读成「加载中」而非「不可点」);**不含 `outline-color` / `outline-width`**(D-14 派生结论:过渡焦点环是已知的无障碍反模式,环必须瞬变)。
    4. **D-11 的具名例外登记**:`.event-list { transition: background-color 0.3s }`(L602)保留 300ms。它服务的是 `.streaming` / `.aborted` 两个**流式状态指示类**,不是控件态过渡;INTERACT-02 的 120–150ms 规格针对的是控件反馈。**全站因此有两个时长,300ms 那个不是控件态** —— 不得静默留下两个时长。同时写明「本阶段的性质是纯追加,编辑 L602 会打破该性质」。
    5. **`<textarea>` 不进本枚举**(全站计数为 0;与 D-12 的片段一致),而**焦点环枚举含 `textarea`**(D-05 要求它与 `check-05` 的普查集逐字同集)—— 两处枚举的差异是有意的,不是不一致。
    6. **`box-shadow` 不在本列表里 ⇒ 填充按钮的 hover 是瞬变**(D-08 已登记的代价 ②,刻意保留)。

    追加减弱动效块(**与上面那条规则在同一次提交**)。在文件**最末尾**追加:

    `@media (prefers-reduced-motion: reduce) {` / `  button, input, select, .event-list { transition: none; }` / `}`

    枚举**含 `.event-list`** 是刻意的:否则减弱动效用户仍会看到流式状态的 0.3s 背景淡入。

    该块的注释必须写明三条:

    1. **为什么不采用行业标准片段** —— 通行写法是 `*, *::before, *::after { transition-duration: 0.01ms !important … }`,**带两个 `!important` 声明**;本仓库的 `!important` **声明数必须恒为 1**(硬规则 2/4;唯一一条是 `.hidden { display: none !important }`,44 处 `classList` 依赖它),`scripts/check-04-important-count.sh` 会立刻从 1 变 3 而变红。**本阶段不得采纳任何带 `!important` 的减弱动效写法。** 引用该片段时,**`!important` 之后不要跟分号** —— `check-04` 数的是 `!important;` 这个**带分号的声明形态**(裸 `!important` 的注释散文是允许的,style.css:441/444 已有先例);把片段连同分号抄进注释会让 `check-04` 从 1 变 2 并立刻变红
    2. **为什么按选择器重写而不是改时长** —— `transition: none` 是确定性的、可被 `getComputedStyle` 断言的终态;0.01ms 之类的「几乎为零」不是。
    3. **为什么枚举写死而不是用通配** —— 与 Phase 5 / Phase 6 的同一口径:影响面必须可枚举、可对照;通配会把「哪些元素受影响」重新变成不可审。

    ⚠ **注释散文里不得写出 `@media` 字面量。** `check-05` 的 `_l2_guard_shape` 数的是 `text.count("@media")` —— **全文件、裸子串**,不是锚定的规则行;本任务把 `EXPECTED_MEDIA_QUERIES` 同步为 1 之后,任何一处复述该词都会让计数变成 2,`item 8` 的静态守卫立刻 FAIL。故本块与挂载规则的注释在指代它时**必须改写措辞**(写「本块」/「减弱动效媒体块」/「该媒体块」即可),不得出现 `@media` 后跟小写词的裸形态。注意本任务验收判据里的 `grep -c '^@media (prefers-reduced-motion'` 锚在行首,**与守卫的全文件裸子串计数不是同一个判据** —— 锚定判据通过不代表守卫通过,两者必须同时为绿。

    ⚠ **同一类散文陷阱共有三个,三个都要点名。** 除上面的媒体查询字面量(甲)外:(乙)`!important` **后面不得跟分号** —— `check-04` 数的是 `!important;` 这个**带分号的声明形态**(裸 `!important` 的注释散文是允许的,style.css:441/444 已有先例);把片段连同分号抄进注释会让计数从 1 变 2 并立刻变红。(丙)**注释里不得让 `opacity` 或 `outline` 与「过渡属性的那个冒号写法」落在同一行** —— 本任务验收清单的最后三条里有两条是按行匹配的裸子串断言、且要求该计数恰为零(一条锚 `opacity`、一条锚 `outline`),它们的前缀正是「过渡属性名 + 冒号」,而 `.*` 会跨过整行散文,故「属性列表里没有某属性」这种**对照句式**会被判死(HEAD 上这两条判据实测均为零,见执行前基线)。照 (甲)(乙) 的先例**改写措辞**:讲「属性列表只有两个」时直接写「只有 `background-color` 与 `border-color`」,不要用「某属性 vs 某属性」的对照句式,或把两者拆到两行。

    同步 `check-05` 的媒体查询决策常量。`scripts/check-05-ui-uat.py` 里:

    - 把 `check-05` 的媒体查询决策常量的**值从零改为一**(变量名与位置见 `<read_first>` 指出的 `check-05` L1596-1601 那一处);
    - 它上面的决策注释块(L1596-1601)必须改写:说明计数**现在是 1**,而原因是 **Phase 7 落地了 `@media (prefers-reduced-motion: reduce)`** —— 这与 L-2「窄窗口守卫被实测推翻」是**两件不同的事**,后者仍然成立(三宽度仍无破版,该守卫仍未写出)。**不区分这两件事会让后来者把 `@media` 计数读成「L-2 的守卫被写了」。**
    - `_l2_guard_shape` 里 `ok_true(...)` 的**标签字符串**必须同步改写:从「[static] frontend/style.css 的 @media 出现次数 == 决策(被实测推翻 ⇒ 0)」改为「[static] frontend/style.css 的 @media 出现次数 == 决策(Phase 7 的 prefers-reduced-motion 块 ⇒ 1;L-2 的窄窗口守卫仍未写出)」;`info()` 的诊断文案同步。**标签是断言的一部分,不改会让输出自相矛盾。**

    这三处(规则、media 块、常量)必须在**同一个提交**里落地,否则 `check-05 --item 8` 会有一段时间是红的。
  </action>
  <verify>
    <automated>bash scripts/check-04-important-count.sh</automated>
    <fails_when>不是恰好一行 "PASS"(输出 "FAIL: expected 1 '!important;' declaration, found 3" 即为失败 —— 说明采纳了行业标准片段)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh</automated>
    <fails_when>任一条不是恰好一行 "PASS"</fails_when>
    <automated>.venv/bin/python scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>末行不是 "PASS: 0 failures"</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 8</automated>
    <fails_when>exit != 0;或 `[static] frontend/style.css 的 @media 出现次数 == 决策` 出现 FAIL(说明常量与文件实际计数不同步)</fails_when>
    <automated>grep -c '^@media (prefers-reduced-motion' frontend/style.css</automated>
    <fails_when>计数不为 1(判据锚在 `^@media` 上,不数裸子串:该块的注释必须解释「为什么尊重减弱动效」,那句散文会合法地复述 `prefers-reduced-motion` 这个词,裸子串计数会因此 > 1 而永远无法变绿)</fails_when>
    <automated>git diff -- frontend/style.css</automated>
    <fails_when>输出中出现以 `-` 开头且含 `transition: background-color 0.3s` 的行(既有的 .event-list 300ms 声明被改动 —— D-11 要求一个字节都不动)</fails_when>
  </verify>
  <done>过渡挂载规则与 `@media (prefers-reduced-motion: reduce)` 块已追加在文件末尾且在同一次提交;`.event-list` 的 300ms 声明零改动并被登记为具名例外;`EXPECTED_MEDIA_QUERIES == 1` 且其注释与断言标签已同步说明「这是 Phase 7 的 media 块,不是 L-2 的守卫」;`check-05 --item 8` 恢复 PASS;`!important` 声明数仍为 1。</done>
  <acceptance_criteria>
    - `grep -n '^button, input, select { transition: background-color 120ms, border-color 120ms; }' frontend/style.css` 有输出
    - `grep -n '^@media (prefers-reduced-motion: reduce) {' frontend/style.css` 有输出
    - `grep -n 'button, input, select, .event-list { transition: none; }' frontend/style.css` 有输出
    - `grep -n 'EXPECTED_MEDIA_QUERIES' scripts/check-05-ui-uat.py` 的输出里,赋值行的值读作 **1**(逐行核对,不数个数)
    - `grep -n 'EXPECTED_MEDIA_QUERIES' scripts/check-05-ui-uat.py | grep -c '= 0'` 输出 == 0
    - `grep -o '!important;' frontend/style.css | wc -l` 输出 == 1
    - `grep -n 'transition: background-color 0.3s;' frontend/style.css` 有输出(既有声明未被改动、也未被复制)
    - `grep -o 'transition:' frontend/style.css | wc -l` 输出 >= 3(既有 `.event-list` + 新挂载规则 + media 块内的 `transition: none`)
    - `grep -c 'transition:.*opacity' frontend/style.css` 输出 == 0
    - `grep -c 'transition:.*outline' frontend/style.css` 输出 == 0
    - `grep -c 'transition: all' frontend/style.css` 输出 == 0
    - `grep -c '^\*, \*::before, \*::after' frontend/style.css` 输出 == 0
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 2:契约计数的静态守卫(D-15 中段)+ 过渡与减弱动效的运行时探针</name>
  <files>scripts/check-05-ui-uat.py</files>
  <read_first>
    - scripts/check-05-ui-uat.py(L166-190 的 `ok_true` / `blocked` / `info`;L935-958 的 `check_render_markdown_call_sites`(脚本自己从文件文本算的范本);L1596-1628 的 `_l2_guard_shape`(静态守卫的完整形态);L2102-2122 的 `_latest_check_max_height_guard`(同族);L281-282 `read_style`;L392-402 `resolve_token`;L2425-2534 的 `parse_args` / `normalize_items` / `main`)
    - scripts/check-01-token-conformance.sh(L27 的 awk 状态机 —— 提取围栏内外文本的最接近范本)
    - .planning/phases/idi-07-interaction-states-and-focus/idi-07-PATTERNS.md 的「契约计数静态断言(D-15 中段)」一节
  </read_first>
  <action>
    在 `scripts/check-05-ui-uat.py` 新增 `_idi07_focus_contract_guards(item)`,并在 `item10` 的开头调用它。它照 `_l2_guard_shape` 的**三条共同纪律**写:**`OSError` ⇒ `blocked()`**、**打印命中行号**、**比的是「实测计数 vs 独立决策常量」不是自比**。

    四条静态断言(逐条落在职责相符的形态上):

    1. **`:focus-visible` 计数 > 0** —— 读 `STYLE_CSS` 文本,`text.count(":focus-visible")`;期望常量 `EXPECTED_FOCUS_VISIBLE_MIN = 1`(用 `>=` 比较,因为七选择器枚举天然大于 1)。`info()` 打印命中行号。这是 ROADMAP Phase 7 的 gate 原文。
    2. **没有任何焦点规则设置 `border` 或 `padding`** —— 这条需要**块提取**:用 awk 式的状态机(范本:`check-01` L27)从 `STYLE_CSS` 文本里切出所有含 `:focus-visible` 的**规则块**(从选择器行到第一个 `}`),再在块内数 `border` 与 `padding` 的**声明**出现次数;两者都必须为 0。**必须用块提取而不是全文件 grep** —— 全文件里 `border` / `padding` 到处都是。失败时的 note 要指出是哪一行、哪一个属性。
    3. **`prefers-reduced-motion` 与新增 transition 同时存在** —— 断言 `text.count("prefers-reduced-motion") >= 1` **且** `text.count("transition: background-color 120ms") >= 1`。⚠ **这条断言不证明「同一次提交」** —— 「同提交」是 git 维度的事实,文件文本断言无法证明。**必须在 `info()` 里逐字声明这个局限**,不得让读者以为它证明了同提交;同提交只能落成计划/评审义务(本计划的 Task 1 已把它写进 `<verify>` 与 `<done>`)。
    4. **`--color-focus` 已声明且被消费** —— 用 `check-01` 同款的 awk 状态机把文本切成围栏内 / 围栏外两段;断言围栏内 `--color-focus:` 的声明计数 == 1 **且** 围栏外 `var(--color-focus)` 的引用计数 > 0。这是硬规则 5「与消费者同提交」的机械形态。同样为 `--color-surface-active` / `--color-border-hover` / `--color-overlay-hover` / `--color-overlay-active` 各加一条同形断言(声明计数 == 1 且围栏外引用计数 > 0)。

    另加一条**过渡与减弱动效的运行时探针**(本计划的 style.css 改动必须有至少一项运行时验证,硬规则 7):

    - 在 `p1` 样本上读 `#btn-process-round` 的 `read_style(page, "#btn-process-round", "transition-property")` 与 `"transition-duration"`,期望属性列表包含 `background-color` 与 `border-color`、时长解析为 `0.12s`;读 `.event-list` 的同两项,期望 `background-color` 与 `0.3s`(**D-11 的具名例外在运行时可见**)。
    - 然后 `page.emulate_media(reduced_motion="reduce")`,重读四个元素的 `transition-duration`,断言全部为 `0s`(含 `.event-list`);读完立即 `page.emulate_media(reduced_motion="no-preference")` 复位,**否则会污染其后各项**。复位与 `page.set_viewport_size(VIEWPORT_RESTORE)` 同级纪律。
    - 元素读不到 ⇒ `blocked(...)`,**绝不记 PASS**。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 10</automated>
    <fails_when>exit != 0;或任一条静态契约守卫 FAIL(焦点规则里出现 border/padding、`--color-focus` 未被消费、`:focus-visible` 计数为 0);或减弱动效探针下任一元素的 `transition-duration` 不是 `0s`</fails_when>
    <automated>grep -c 'def _idi07_focus_contract_guards' scripts/check-05-ui-uat.py</automated>
    <fails_when>计数不为 1</fails_when>
    <automated>grep -c 'emulate_media' scripts/check-05-ui-uat.py</automated>
    <fails_when>计数小于 2(必须有 reduce 与复位两次调用)</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8,9</automated>
    <fails_when>exit != 0,或逐项结论里出现任一项非 PASS(尤其 item 8 —— `emulate_media` 若未复位会污染其后各项)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-02-contrast.py | tail -1; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>任一条不是 "PASS"(check-02 的判据是末行 "PASS: 0 failures")</fails_when>
  </verify>
  <done>第 10 项在跑运行时探针之前先跑四条静态契约守卫,每条都有明确的 PASS / FAIL / BLOCKED;「同提交」的局限在 `info()` 里被逐字声明;过渡与减弱动效的运行时探针在 `p1` 上读到 0.12s / 0.3s 与 reduce 下的 0s,并在读完后复位媒体模拟;既有九项 UAT 与四条既有门全绿。</done>
  <acceptance_criteria>
    - `grep -n 'def _idi07_focus_contract_guards' scripts/check-05-ui-uat.py` 有输出
    - `grep -n '_idi07_focus_contract_guards(item)' scripts/check-05-ui-uat.py` 有输出(item10 里确实调用了)
    - `grep -o 'EXPECTED_FOCUS_VISIBLE_MIN' scripts/check-05-ui-uat.py | wc -l` 输出 >= 2
    - `grep -n 'prefers-reduced-motion' scripts/check-05-ui-uat.py` 有输出
    - `grep -n '同提交' scripts/check-05-ui-uat.py` 有输出(局限被逐字声明)
    - `grep -n 'reduced_motion="reduce"' scripts/check-05-ui-uat.py` 有输出,且 `grep -n 'reduced_motion="no-preference"' scripts/check-05-ui-uat.py` 有输出
    - `grep -o 'transition-duration' scripts/check-05-ui-uat.py | wc -l` 输出 >= 2
    - `.venv/bin/python scripts/check-05-ui-uat.py --item 10` 的逐项结论行形如 `item 10: PASS  (N 条断言,0 FAIL,0 BLOCKED)` 且 N 相比计划 01 完成时**只增不减**
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 3:整阶段收口 —— 全门复跑、D-19 的指纹重算与披露、人工项 5″ 与 D-11 修正案的登记</name>
  <files>scripts/check-05-ui-uat.py</files>
  <read_first>
    - .planning/STATE.md 的 §Operator Next Steps(尤其 `/gsd-verify-work idi-04.1-radix` 这一条未收口项)
    - .planning/phases/idi-04-tokens-contract/、idi-04.1-radix/、idi-05-typography-and-visual-hierarchy/、idi-06-layout-robustness/ 各自 VERIFICATION.md 的 frontmatter `covered_files` 与 `covered_digest`
    - .planning/phases/idi-06-layout-robustness/06-CONTEXT.md 的 D-19(连带复验义务的起点)
    - scripts/check-05-ui-uat.py 的模块 docstring(L18-92:浏览器选择、禁止 `networkidle`、截图不可用、键盘文本选区无法自动化)
  </read_first>
  <action>
    这一步**不新增门**,只做收口与披露。全部产出落进 SUMMARY 与 VERIFICATION,不落进代码。

    1. **全门复跑并逐条记录原始输出**:`bash scripts/check-01-token-conformance.sh`、`.venv/bin/python scripts/check-02-contrast.py`(记录末行与 `^PASS` 计数)、`bash scripts/check-03-hidden-uniqueness.sh`、`bash scripts/check-04-important-count.sh`、`.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,5,6,7,8,9,10`、`.venv/bin/python scripts/probe-07-focus-composite.py`。任一条从执行前基线变红即为回归。

    2. **D-19 的指纹重算与披露**。本阶段作废了 `frontend/style.css` 与 `scripts/check-05-ui-uat.py` 参与的**全部 live 验证指纹**。按 `covered_files` 逐份核实,当前仍在 `.planning/phases/` 下(未归档、会被 staleness 机制消费)且覆盖这两个文件的报告有**四份**:`idi-04` / `idi-04.1-radix` / `idi-05` / `idi-06`。收口时必须:
       - **以 HEAD 内容重算指纹**,**不要看 mtime**(本项目已记录:stale 有两种成因 —— 「内容真变」走重新验证,「记账性编辑」走重算 + 披露,补救方向相反);
       - 逐份比对 `covered_files` 是否覆盖了 `frontend/style.css` / `scripts/check-05-ui-uat.py`,并记录重算后的 digest;
       - ⚠ **不得用 `gsd-tools query verification status <phase>` 判定 stale** —— 该命令对这四份报告一律返回 `missing`(相位目录命名与工具的相位令牌解析不匹配),判据只能是拿 `covered_files` 逐份比对 + 重算 digest;
       - 把「哪几份需要重新验证、哪几份只需重算 + 披露」写进 SUMMARY。

    3. **登记人工验收项 5″(D-17)**。本阶段**只有一条**人工项:「`#btn-authorize` 的禁用态**仍一眼看出不可点**」。它是关于**感知**的主张,不是关于数值的主张。必须逐字写进 VERIFICATION 的 manual list,并**把两个禁用态数值各自的元素与覆盖面分开写清,不得混成一个值**:①**机器半场**(`check-05` 第 10 项的 SC5′)覆盖的是 `.verdict-buttons button:disabled`(style.css L1222,朴素按钮),它断言 hover 时背景与静默**相同**且计算 `opacity` 仍为 **0.5**;②人工项针对的 `#btn-authorize:disabled`(style.css L1106)是**另一条规则**、`opacity` 为 **0.55**,它的 hover 零反馈由同一处 gate(L587 的选择器)承担,但**今天没有任何机器断言读过它的 `opacity`**。人工半场要回答的问题正是:**门绿不等于视觉上真的没被软化**(尤其 `#btn-authorize` 那条 0.55 的规则今天只被 gate 间接保护,未被任何探针读数)。**不得把它删掉换成机器代理量。**

    4. **登记 D-11 的修正案**。写明 300ms 例外的登记面是 **CONTEXT(已满足)+ 新过渡规则的围栏注释(计划 03 Task 1 已落)**;**UI-SPEC 那一处不存在**,原因是本阶段没有 UI-SPEC 且不得创建 —— 不得据此认为例外未登记。

    5. **登记本阶段唯一跨阶段的开放项**:`#round-doc` 的焦点环承载面指派给 Phase 8(D-06)。Phase 7 的枚举含 `[tabindex]`,Phase 8 加 `tabindex="0"` 时那条规则会自动把环套到一个数千像素高的盒子上 —— Phase 8 必须写内嵌处理(`outline-offset: -2px` 或把环落在 `#doc-pane`)。这条必须出现在 SUMMARY 与 VERIFICATION 两处。

    6. **登记 B1 的耦合**:`EXPECTED_MEDIA_QUERIES` 已随 media 块同步为 1;若日后有人删除该 media 块,必须同时把常量改回 0,否则 item 8 会误报。

    7. **登记本阶段唯一的非追加编辑(L587 的选择器改写),使阶段级的「纯追加」声明不被下游无条件复述。** `ROADMAP.md` Phase 7 的 Rationale 原文是「纯追加 —— 不编辑任何既有规则」;本阶段实际有**且仅有**一处就地编辑:`frontend/style.css` L587 的 `button:hover` 选择器被改写为 `button:where(:not(:disabled)):hover`(声明体逐字节不变,特异性改写前后逐位相同,均为 0-1-1;理由与取证见计划 02 的 `<decision_register>`)。SUMMARY 与 VERIFICATION 复述「纯追加」时**必须带这个限定**,或直接写成「除 L587 的选择器改写外纯追加」;`CONTEXT.md` 的禁令面更窄(只禁「编辑既有规则的**声明**」),该改写不触犯它,但 ROADMAP 的阶段级措辞更宽,**不得无条件复述**。这一条同时为 VERIFICATION 里「阶段性质」那一栏提供准确措辞。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>任一条不是恰好一行 "PASS"</fails_when>
    <automated>.venv/bin/python scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>末行不是 "PASS: 0 failures"</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,5,6,7,8,9,10</automated>
    <fails_when>exit != 0,或逐项结论里出现任一项 FAIL/BLOCKED</fails_when>
    <automated>.venv/bin/python scripts/probe-07-focus-composite.py</automated>
    <fails_when>exit != 0</fails_when>
    <automated>git status --porcelain -- frontend/app.js frontend/index.html frontend/vendor/ scripts/ui-states/</automated>
    <fails_when>输出非空(硬规则 5:这些路径零改动)</fails_when>
    <automated>git diff --numstat -- frontend/style.css</automated>
    <fails_when>输出的第 1 列(新增行数)为 0(本阶段必须真的落地了规则);同时人工核对第 2 列(删除行数)只来自 L587 那一行的选择器改写</fails_when>
  </verify>
  <done>四条既有门 + 第 10 项 + 既有九项 UAT + 一次性探针全部通过;四份受影响报告的 `covered_files` 比对与 HEAD 内容重算的 digest 已记录,并逐份判定「重新验证」或「重算 + 披露」;人工项 5″、D-11 修正案、`#round-doc` 的跨阶段开放项、`EXPECTED_MEDIA_QUERIES` 的耦合、以及**本阶段唯一的非追加编辑(L587 的选择器改写)**都已登记进 SUMMARY 与 VERIFICATION —— 后者确保阶段级的「纯追加」措辞不被下游无条件复述。</done>
  <acceptance_criteria>
    - SUMMARY 中逐条列出六条命令的原始输出或结论,无一条为 FAIL/BLOCKED
    - SUMMARY 中列出四份报告(`idi-04` / `idi-04.1-radix` / `idi-05` / `idi-06`)的 `covered_files` 比对结果与重算 digest,并对每份给出「重新验证」或「重算 + 披露」的处置
    - VERIFICATION 的 manual list 里恰有一条人工项(5″),且它逐字写明「禁用态仍一眼看出不可点」与「门绿不等于视觉上真的没被软化」
    - SUMMARY 与 VERIFICATION 两处都出现 `#round-doc` 的 Phase 8 指派
    - SUMMARY 中出现「UI-SPEC 那一处登记面不存在」的修正案说明
    - SUMMARY 与 VERIFICATION 复述阶段性质时**带 L587 选择器改写的限定**(两处都不得出现无条件的「纯追加」措辞):逐字核对两处,`grep -c 'L587' ` 在两份产物里各 >= 1
    - `git status --porcelain` 里除 `.planning/` 与已声明的改动面外无其他文件
    - `grep -o 'inline-error' frontend/style.css | wc -l` 输出 >= 1(Phase 8 的既有回归门在本阶段结束时仍成立)
  </acceptance_criteria>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 减弱动效偏好 → 全站过渡 | 用错写法会引入 `!important`,而 `.hidden` 的隐藏机制依赖「`!important` 声明数恒为 1」这条不变量 |
| `@media` 块 → `check-05` 的静态守卫 | 计数常量与文件实际计数是一对同步量,只改一处会让门恒红或恒绿 |
| 浏览器媒体模拟 → 其后各项 UAT | `emulate_media` 不复位会污染其后所有项 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-07-12 | Tampering | 减弱动效块采用行业标准片段 | high | mitigate | 注释逐字点名该片段带两个 `!important` 会让 `check-04` 从 1 变 3;`check-04` 在 Task 1 的 `<verify>` 里是第一条命令;围栏注释写明本项目里那条惯例不存在 |
| T-idi-07-13 | Denial of service(门恒红 / 恒绿) | `EXPECTED_MEDIA_QUERIES` 与 `@media` 实际计数 | high | mitigate | 常量、注释、断言标签三处与 media 块**同一次提交**;Task 1 的 `<verify>` 直接跑 `--item 8`;Task 3 登记删除 media 块时必须同步改回 0 |
| T-idi-07-14 | Tampering | 既有的 `.event-list` 300ms 声明 | medium | mitigate | `<verify>` 里用 `git diff` 断言该行未出现在 diff 中;运行时探针在 p1 上读到 `.event-list` 的 `0.3s`,把「例外仍在」变成可观测事实 |
| T-idi-07-15 | Spoofing(假 PASS) | 「同提交」的静态断言 | medium | mitigate | 断言退化为「两者同时存在」并**在 `info()` 里逐字声明它不证明同提交**;同提交落成计划/评审义务与 Task 1 的 `<verify>`/`<done>` |
| T-idi-07-16 | Tampering | 焦点环被加进过渡列表 | medium | mitigate | 围栏注释写明「过渡焦点环是已知的无障碍反模式」;静态断言 `grep 'transition:.*outline'` 计数为 0 |
| T-idi-07-17 | Repudiation | 本阶段作废的验证指纹 | high | mitigate | 以 HEAD 内容重算四份报告的 digest,逐份判定「重新验证 / 重算 + 披露」;明确禁止用 `query verification status` 判定 stale |
| T-idi-07-18 | Repudiation | 人工验收项 5″ | medium | mitigate | 逐字写进 VERIFICATION 的 manual list,并写明机器半场覆盖了什么、人工半场要回答什么;不得换成机器代理量 |
| T-idi-07-SC | Tampering | npm / pip / cargo 安装 | low | accept | 零新增运行时依赖、零构建步骤(硬规则 6):无包管理器调用进入范围;若执行期出现安装需求,即为计划偏差与停止条件 |
</threat_model>

<verification>
- 执行前基线:`bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh` 全 PASS;`.venv/bin/python scripts/check-02-contrast.py | tail -1` 为 `PASS: 0 failures`;`.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,5,6,7,8,9` exit 0。
- 执行后:同一命令组 + `--item 10` + `scripts/probe-07-focus-composite.py` 全部通过。
- **本计划改动 `frontend/style.css`,故硬规则 7 的运行时验证由 Task 2 的过渡/减弱动效探针与 Task 3 的 `--item 10` 共同承担。**
- 必须使用项目 venv(`.venv/bin/python`):环境 `python3` 是 miniconda,会让无关套件假失败。
- 浏览器:默认 `--browser bundled`(Playwright 自带 chromium,已缓存,可无头);**禁止 `networkidle`**;本环境**截图不可用**,一律走计算样式读数,**不得计划视觉 diff**。
- `git status --porcelain -- frontend/app.js frontend/index.html frontend/vendor/ scripts/ui-states/` 输出为空。
</verification>

<success_criteria>
1. 控件的过渡只声明 `background-color` 与 `border-color`,时长 120ms;`opacity` / `outline-*` / `all` 均不在任何过渡的属性列表里。
2. `@media (prefers-reduced-motion: reduce)` 把 `button` / `input` / `select` / `.event-list` 的过渡重写为 `none`,且**不含任何 `!important`**;运行时在 `reduced_motion="reduce"` 下读到 `0s`。
3. 既有的 `.event-list` 300ms 过渡一个字节未改,并在 CONTEXT 与新规则的围栏注释两处登记为具名例外;UI-SPEC 那一处的缺失以修正案记账。
4. `EXPECTED_MEDIA_QUERIES == 1` 且其注释/标签说明「这是 Phase 7 的 media 块,不是 L-2 的窄窗口守卫」。
5. D-15 中段的四条契约计数断言全部落成静态守卫,其中「同提交」一条明确声明其局限。
6. 四份受影响报告的指纹以 HEAD 内容重算并逐份披露;人工项 5″ 与 `#round-doc` 的跨阶段开放项已登记。
7. 四条既有门、既有九项 UAT 与第 10 项全绿;`app.js` / `index.html` / `vendor/` / `ui-states/` 零改动;`!important` 声明数仍为 1。
</success_criteria>

<output>
Create `.planning/phases/idi-07-interaction-states-and-focus/idi-07-03-SUMMARY.md` when done
</output>
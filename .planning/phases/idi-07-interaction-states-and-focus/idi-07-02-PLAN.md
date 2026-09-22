---
phase: idi-07-interaction-states-and-focus
plan: 02
type: execute
wave: 2
depends_on: [idi-07-01]
files_modified:
  - frontend/style.css
  - scripts/check-02-contrast.py
  - scripts/check-05-ui-uat.py
autonomous: true
requirements: [INTERACT-01]
estimate:
  tokens: 74000
  raw_tokens: 74000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "悬停任一有底色语义的填充按钮时,它的计算 background-color 不变,而计算 box-shadow 里出现 inset 叠层(填充变深、白字不动)(D-08)"
    - "按下任一有底色语义的填充按钮时,叠层的 alpha 从 0.06 提到 0.12(D-09)"
    - "悬停任一朴素(无底色)按钮时计算 background-color 变为 --color-surface-hover;按下时变为 --color-surface-active(D-09)"
    - "悬停一个被禁用的朴素按钮时,计算 background-color 与静默时**相同** —— 未 gate 的既有 button:hover 不再给它上色(D-07)"
    - "悬停任一 input / select 时计算 border-color 变为 --color-border-hover,且它的 7 个 ID 级规则体全部被覆盖(D-10)"
    - "所有有底色语义的按钮 hover 时,其前景文字对比度不低于静默时(D-08 的 opacity 排除理由)"
  artifacts:
    - "frontend/style.css:围栏内 --color-surface-active / --color-border-hover / --color-overlay-hover / --color-overlay-active 四个 tier-2 令牌"
    - "frontend/style.css:L587 的 button:hover 选择器就地改写为 button:where(:not(:disabled)):hover(声明一字不动)"
    - "frontend/style.css:末尾追加的 :where(button:not(:disabled)):active、填充按钮 hover/active 叠层规则组、input/select hover 规则组"
    - "scripts/check-02-contrast.py / frontend/style.css 清单:两条 --color-border-hover NON-TEXT 配对 + 头部计数注释 50 → 52"
    - "scripts/check-05-ui-uat.py:第 10 项的 SC5 / SC5′ 运行时探针"
  key_links:
    - "填充按钮 hover 的选择器特异性必须 >= 它自己的填充规则(1-0-0 的 #btn-*、0-1-1 的 button.primary / .overlay-card button、1-0-1 的 #chat-input-row button)"
    - "朴素按钮的 :active 规则特异性必须停在 0-1-0,否则会压过 0-1-1 的填充族、把它们按下时刷成灰"
    - "--color-surface-active 与 --color-surface-user 同值(--radix-gray-4);注释必须点名 04.1-N-4,否则会被后来者当成违规「修」掉"
    - "叠层的 rgba() 字面量只出现在围栏内(R-2 的不变量:围栏外无裸 rgba())"
  prohibitions:
    - "不得写 * { transition: all } 或任何全局通配 transition"
    - "不得用 opacity 实现 hover 反馈(会把白字一起变浅,三个色族跌破 AA 4.5:1)"
    - "不得用 transform: translateY(...) 做按下位移(#selection-menu 的包含块是硬规则 5 点名的雷区)"
    - "不得软化 :disabled 视觉(它是 G3 前提条件唯一的视觉信号);不得改动 8 条既有 :disabled 规则"
    - "不得编辑任何既有规则的**声明**(只有 L587 的选择器被改写)"
    - "不得新增 !important、@layer、@property、var(--x, #fallback)、任何运行时依赖或构建步骤"
    - "不得触碰 .hidden 规则、.fatal 修饰符、#selection-menu 的 DOM 位置、showInlineError、renderAnnotations、renderVerdictCard"
    - "不得编辑 frontend/app.js、frontend/index.html、frontend/vendor/"
---

<objective>
给每一个交互控件补上可辨的 hover / active 反馈,并让禁用态在悬停时**零反馈**(INTERACT-01 / D-07 / D-08 / D-09 / D-10 / D-20)。

本计划交付四件事:①围栏内四个新 tier-2 令牌(`--color-surface-active` / `--color-border-hover` / `--color-overlay-hover` / `--color-overlay-active`,零新增 tier-1 primitive);②把既有的 `button:hover` 选择器 gate 在 `:not(:disabled)` 上 —— **声明一字不动**;③按**逐条特异性核对过**的选择器组,给九个有底色语义的填充按钮规则体挂上统一 rgba 叠层(0.06 hover / 0.12 active);④给 `input` / `select` 挂上 `border-color` 加深一步的 hover。

Purpose: D-02 第 7 条已实测证明 —— **今天所有有底色语义的按钮 hover 时零反馈**(`button:hover` 是 0-1-1,被九组 1-0-0 / 0-1-1 的填充规则全部盖掉);同时 `.verdict-buttons button:disabled` 会因那条未 gate 的 hover 而变色(D-02 第 5 条)。本计划正面修掉这两个缺陷。
Output: 四个新令牌、一个既有规则的选择器改写、三组新规则、两条新 PAIR、第 10 项的 SC5 / SC5′ 探针。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/idi-07-interaction-states-and-focus/07-CONTEXT.md
@.planning/phases/idi-07-interaction-states-and-focus/idi-07-PATTERNS.md
@.planning/phases/idi-07-interaction-states-and-focus/idi-07-01-SUMMARY.md
</context>

<decision_register>
**D-07 的机制裁定(本计划唯一偏离 CONTEXT 字面的地方,已逐条取证)。** D-07 的原话是「`:hover` / `:active` 一律 gate 在 `:not(:disabled)` 上」,并明确**不选**「不 gate + 给 `:disabled` 回写背景」,理由是「那是一条专门用来抵消的规则,且每个填充色族都要跟一条」。

取证:缺陷现场是 `.verdict-buttons button:disabled`(style.css L1222),它只设 `opacity` / `cursor`,**不钉 `background`**,于是 L587 的 `button:hover`(0-1-1)照样给它上 `--color-surface-hover`。

把 D-07 的片段 `button:not(:disabled):hover`(0-2-1)当作**新增规则**追加会同时产生两个后果:
- **修不了缺陷** —— `:not(:disabled)` 不匹配禁用按钮,而 L587 仍然匹配它;
- **引入回归** —— 0-2-1 的 ID 列虽为 0,但类列 2 大于 `button.primary`(0-1-1)与 `.overlay-card button`(0-1-1)的类列 1,于是这两族填充按钮 hover 时会变成灰底,与 D-08「填充按钮用 rgba 叠层」的机制正面冲突。

因此本计划把 gate 落在 **L587 的选择器上**(`button:hover` → `button:where(:not(:disabled)):hover`):
- `:where()` 贡献 0 特异性,故改写后特异性**仍为 0-1-1,与改写前逐位相同** ⇒ 对任何元素的级联结果**可证明地不变**;
- 唯一的变化是禁用按钮不再匹配 ⇒ 缺陷被一次性、全局、面向未来地修掉(将来任何新增的朴素按钮自动继承这条 gate);
- **声明体 `background: var(--color-surface-hover);` 一字不动** —— 阶段边界禁的是「编辑既有规则的**声明**」,此处只改选择器。

`#btn-authorize` 的不可逆权重(D-07 末段)由 `#btn-authorize:not(:disabled):hover`(1-2-0)保住:它的深绿填充与 16px 字号不因叠层而改变视觉档。

**D-08 / B3 rgba() 落点裁定:选「围栏内令牌」支。** CONTEXT D-08 的片段把 `rgba(0,0,0,0.06)` 写在规则体内,而 style.css L199-204 的既有注释立下的是相反的先例:「R-2 恢复 shadow 令牌,**使围栏外不再出现裸 `rgba()`**」。`check-01` 只数裸 `#hex` 与 tier-1 `var()` 引用,**不数裸 `rgba()`** —— 这条纪律**没有机械守卫**,只能靠注释与 review 守。故本计划在围栏内声明 `--color-overlay-hover: rgba(0, 0, 0, 0.06);` 与 `--color-overlay-active: rgba(0, 0, 0, 0.12);`(紧邻既有的 `--color-overlay-backdrop`),规则体只写 `var(--color-overlay-hover)`。收益:①保住 R-2 的不变量;②两个 alpha 值成为可复算的**单一事实源**。代价:围栏内多两个 tier-2 令牌(它们不是对比度边界,故**不进 PAIR 清单** —— `--shadow-*` 同族也没有配对)。

**D-09 朴素按钮 `:active` 的特异性上限。** 朴素按钮的 `:active` 规则写成 `:where(button:not(:disabled)):active`(特异性 **0-1-0**),刻意低于 `button:primary` 族。理由:0-1-1 的 `button.primary` / `.overlay-card button` 拥有自己的按下态(D-08 的 0.12 叠层);若朴素 `:active` 取到 0-1-1 并靠源码顺序取胜,这些填充按钮按下时会被刷成灰底。0-1-0 仍高于 `button` 基础规则(0-0-1),故朴素按钮的按下反馈成立。
</decision_register>

<tasks>

<task type="auto">
  <name>Task 1:围栏内四个新令牌 + L587 选择器的 :not(:disabled) gate + 朴素按钮的 :active</name>
  <files>frontend/style.css</files>
  <read_first>
    - frontend/style.css(L180-215 的 Tier 2 surface/border 段与 overlay/shadow 段;L40-56 的 tier-1 声明,确认 `--radix-gray-4` L52 与 `--radix-gray-11` L55 都已声明;L277-297 的「Three values that must NOT be 'helpfully' changed back」注释,尤其第 3 条;L578-588 的 `button` 基础规则与唯一一条 `button:hover`;L1220-1222 的 `.verdict-buttons button:disabled`;L1227-1324 的文件末尾追加区)
    - .planning/phases/idi-07-interaction-states-and-focus/idi-07-PATTERNS.md 的「围栏内:tier-2 令牌声明」与「围栏外:hover / active 的既有形态与缺陷现场」两节
  </read_first>
  <action>
    围栏内声明四个 tier-2 令牌,全部与消费者同提交(硬规则 5),零新增 tier-1 primitive。

    ① 在 `--color-surface-hover: var(--radix-gray-3);`(L184)之后、`--color-surface-user: var(--radix-gray-4);`(L185)之前插入:
    `--color-surface-active: var(--radix-gray-4);`
    它的注释必须写明三条:①它是朴素按钮按下态,与 `--color-surface-hover`(gray-3)构成 **3 → 4 的递进**,与 hover 的 3 相邻;②**它与 `--color-surface-user` 同值** —— 这不是缺陷,两条令牌名字不同、语义不同、消费者不同(04.1 D-03「名必须说实话」);③**必须点名 04.1-N-4** —— 上面 L293-297 的第 3 条注释**逐字警告过**「gray-4 would double the hover delta and collide with `--color-surface-user`」。本令牌取 gray-4 是**刻意的**(active 是递进的终点),不是违反 04.1-N-4;不写这条说明,后来者会把同一份注释读成自相矛盾并「修」掉本令牌。

    ② 同步**扩写 L293-297 的第 3 条**注释:在「gray-4 would double the hover delta and collide with `--color-surface-user`」之后补一句,写明 gray-4 现在**还被 `--color-surface-active` 消费**,那是有意的递进终点,与 `--color-surface-user` 的「用户消息背景」语义不共享消费者。**不扩写会让同一份注释自相矛盾。**

    ③ 在 `--color-border-strong: var(--radix-gray-9);`(L192)之后插入:
    `--color-border-hover: var(--radix-gray-11);`
    注释写明:`input` / `select` 的静默边框是 `--color-border-strong`(gray-9 `#8d8d8d`),hover 加深一步取已声明的 `--radix-gray-11`(`#646464`,零新增 primitive);**不取 `--radix-gray-12`** —— 它是 Radix 的高对比**文字**步,作为边框视觉上接近 `#202020` 的近黑,过重(与 D-04 排除 `--radix-blue-12` 同一条理由);它与 `--color-text-muted` 同值(gray-11),这是值碰撞而非名不副实,注释须点名。

    ④ 在 `--color-overlay-backdrop: rgba(0, 0, 0, 0.45);`(L202)之后插入两条,并扩写该分组的注释末句:
    `--color-overlay-hover: rgba(0, 0, 0, 0.06);`
    `--color-overlay-active: rgba(0, 0, 0, 0.12);`
    注释写明:这两条是填充按钮的交互态压暗叠层,**存在的理由之一是让围栏外不出现裸 `rgba()`**(R-2 的不变量);`box-shadow` 的 inset 不参与布局 ⇒ 零位移;它们不是对比度边界,故**不进 PAIR 清单**。

    围栏外:改写 L587 的选择器(声明一字不动)。把
    `button:hover { background: var(--color-surface-hover); }`
    的选择器改为 `button:where(:not(:disabled)):hover`,声明体保持 `background: var(--color-surface-hover);` **逐字节不变**。就地改这一行,**不移动它的位置**(硬规则 3:追加,不重排)。在该行上方插入一条注释块,写明:①D-07 的 gate 落在选择器上而不是新增规则上,理由见本计划 `<decision_register>` 的两条取证(新增 `button:not(:disabled):hover` 既修不了缺陷、又会让 `button.primary` / `.overlay-card button` 变灰底);②`:where()` 贡献 0 特异性,改写后特异性**仍是 0-1-1**,对任何元素的级联结果不变,唯一变化是禁用按钮不再匹配;③**这不是硬规则 1 禁止的 `.hidden` 用法** —— 那条禁的是拿 `:where()` 给隐藏机制降特异性,本处是给交互态加 gate。

    围栏外末尾追加朴素按钮的按下态(硬规则 3:追加,不重排):
    选择器 `:where(button:not(:disabled)):active`,声明体 `background: var(--color-surface-active);`。
    注释写明:特异性 **0-1-0** 是刻意的 —— 它高于 `button` 基础规则(0-0-1)使朴素按钮的按下反馈成立,又低于 `button.primary` / `.overlay-card button`(0-1-1)使这两族填充按钮的按下态仍归 D-08 的 0.12 叠层所有;**改高即把填充按钮按下时刷成灰底**。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>exit != 0;或输出不是恰好一行 "PASS"(新规则里出现裸 `#hex` 或 `var(--radix-*)` 即为失败)</fails_when>
    <automated>bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>任一条不是恰好一行 "PASS"</fails_when>
    <automated>.venv/bin/python scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>末行不是 "PASS: 0 failures"</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8,9</automated>
    <fails_when>exit != 0,或逐项结论里出现任一项非 PASS(尤其 item 8 的静态守卫与 item 9 的 L-6 命中区普查)</fails_when>
    <automated>git diff --numstat -- frontend/style.css</automated>
    <fails_when>输出的第 2 列(删除行数)大于 2 —— 本任务只允许改写 L587 那一行的选择器,不得删除任何其他行</fails_when>
  </verify>
  <done>四个新 tier-2 令牌已在围栏内声明且各自被围栏外的规则消费;`--color-surface-active` 的值碰撞注释点名 04.1-N-4 且 L293-297 的第 3 条已同步扩写;L587 的选择器已 gate,声明体逐字节不变;朴素按钮的 `:active` 规则已追加且特异性为 0-1-0;四条既有门与既有九项 UAT 仍全绿。</done>
  <acceptance_criteria>
    - `grep -c '\-\-color-surface-active: var(--radix-gray-4);' frontend/style.css` 输出 1
    - `grep -c '\-\-color-border-hover: var(--radix-gray-11);' frontend/style.css` 输出 1
    - `grep -c '\-\-color-overlay-hover: rgba(0, 0, 0, 0.06);' frontend/style.css` 输出 1
    - `grep -c '\-\-color-overlay-active: rgba(0, 0, 0, 0.12);' frontend/style.css` 输出 1
    - `grep -c '^button:hover {' frontend/style.css` 输出 **0**,且 `grep -c '^button:where(:not(:disabled)):hover {' frontend/style.css` 输出 1
    - `grep -c '^:where(button:not(:disabled)):active {' frontend/style.css` 输出 1
    - `grep -c 'background: var(--color-surface-hover);' frontend/style.css` 输出 1(声明未被改动、也未被复制)
    - `grep -c '04.1-N-4' frontend/style.css` 输出 >= 2(原有第 3 条 + 新令牌注释)
    - `grep -c '--color-surface-user' frontend/style.css` 输出 >= 3(声明 + 原有注释 + 新令牌注释)
    - `grep -o 'var(--radix-' frontend/style.css | wc -l` 与改动前**相同**(新令牌不引入新的 tier-1 引用:gray-4 与 gray-11 均已被既有令牌消费)
    - `git diff -- frontend/style.css` 中 L587 附近只出现一行选择器的替换,`background: var(--color-surface-hover);` 那一行不在 diff 里
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 2:填充按钮的 hover / active 叠层 —— 按九组既有规则逐条核对特异性</name>
  <files>frontend/style.css</files>
  <read_first>
    - frontend/style.css(L666-675 `.overlay-card button` 与 `.overlay-card button.danger`;L771-779 `#btn-approve-draft`;L784-793 `#btn-divergence`;L883-891 `#chat-input-row button`;L900-905 `.modal-buttons button` 与 `button.primary`;L1046-1053 `#btn-process-round`;L1096-1106 `#btn-authorize`;L1111-1118 `#btn-start-writing`;L1170-1179 `#btn-continue-check, #btn-continue-repair`;L1064-1070 `#selection-menu button` 与 `#selection-menu button:hover`)
    - frontend/index.html(L159-205 的四个 `.overlay-card` 与其 `.modal-buttons`;L163 `#btn-permission-allow` 与 L177 `#btn-confirm-authorize` 的 `class="primary"`)
    - .planning/phases/idi-07-interaction-states-and-focus/idi-07-PATTERNS.md 的「Analog D — 填充按钮的既有规则体」与「⚠ D-12 与 Analog 的特异性陷阱」
  </read_first>
  <action>
    在文件末尾追加**两条**规则组(硬规则 3:追加,不重排),按「同族选择器列表」组织 —— 这与文件既有的 `#session-panel:not(.hidden) .panel-header, …` 三行枚举同族。

    hover 组(声明体只有一行 `box-shadow: inset 0 0 0 999px var(--color-overlay-hover);`),选择器逐条为:

    - `#btn-authorize:not(:disabled):hover`(1-2-0,压过 `#btn-authorize` 的 1-0-0)
    - `#btn-approve-draft:not(:disabled):hover`(1-2-0,压过 1-0-0)
    - `#btn-divergence:not(:disabled):hover`(1-2-0,压过 1-0-0)
    - `#btn-process-round:not(:disabled):hover`(1-2-0,压过 1-0-0)
    - `#btn-start-writing:not(:disabled):hover`(1-2-0,压过 1-0-0)
    - `#btn-continue-check:not(:disabled):hover`(1-2-0,压过 1-0-0)
    - `#btn-continue-repair:not(:disabled):hover`(1-2-0,压过 1-0-0)
    - `#chat-input-row button:not(:disabled):hover`(1-2-1,压过 `#chat-input-row button` 的 1-0-1)
    - `button.primary:not(:disabled):hover`(0-3-1,压过 `button.primary` 的 0-1-1)
    - `.overlay-card button:not(:disabled):hover`(0-3-1,压过 `.overlay-card button` 的 0-1-1,也压过 `.overlay-card button.danger` 的 0-2-1)

    active 组:同一份选择器列表,把 `:hover` 换成 `:active`,声明体为 `box-shadow: inset 0 0 0 999px var(--color-overlay-active);`。同特异性下靠源码顺序取胜(active 组在 hover 组之后),故按下时 0.12 覆盖 0.06。

    两条规则组的注释必须逐条写明六件事:

    1. **为什么必须逐 id / 按族枚举,不能写成 `button:not(:disabled):hover`** —— 后者是 0-2-1,ID 列为 0;而 `#btn-*` 是 1-0-0、`#chat-input-row button` 是 1-0-1、`button.primary` 与 `.overlay-card button` 是 0-1-1 且源码在本规则之前。**1-0-0 > 0-2-1**(ID 列大于类列),故那条写法对 `#btn-authorize` 完全无效 —— 这正是 D-02 第 7 条「今天所有有底色语义的按钮 hover 时零反馈」的成因,本规则必须正面跨过它。
    2. **为什么用 `box-shadow` 的 inset 而非 `opacity`** —— 实测 `opacity: 0.88` 会把白字一起变浅,primary 4.77 → 3.93、danger 5.21 → 4.42、commit 4.72 → 3.81,**三个色族跌破 AA 4.5:1**;rgba 叠层把填充变深、文字不动,对比度反而上升(5.27 / 5.75 / 5.23),irreversible 12.32 → 12.97。
    3. **为什么是 999px 的整面铺满** —— 本文件既有的 `box-shadow: inset` 只有 3px 偏移的竖条形态(`#round-doc.round-frozen`、活动面板标记);999px 大于任何按钮的盒宽,故等价于整面覆盖。`box-shadow` 不参与布局 ⇒ 零位移。
    4. **`box-shadow` 不在过渡允许列表里 ⇒ 填充按钮的 hover 是瞬变**,这是刻意的(D-14);朴素按钮仍可过渡(D-12 的挂载规则,计划 03)。
    5. **`#selection-menu button` 不进这两组** —— 它是浮层内的透明底朴素控件,已有 `#selection-menu button:hover { background: var(--color-surface-info); }`(1-1-1);D-08 的 rgba 叠层针对的是**有底色语义**的填充按钮,叠层加到透明底上不可见。
    6. **`#btn-authorize` 的不可逆权重不变** —— 叠层只改填充明度,不改它的深绿填充、白字与 `--text-md` 字号(D-07 末段)。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>exit != 0;或输出不是恰好一行 "PASS"(规则体里出现裸 `#hex` 或 `var(--radix-*)` 即为失败 —— 必须写 `var(--color-overlay-hover)` / `var(--color-overlay-active)`)</fails_when>
    <automated>bash scripts/check-04-important-count.sh</automated>
    <fails_when>不是恰好一行 "PASS"</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8,9</automated>
    <fails_when>exit != 0,或逐项结论里出现任一项非 PASS</fails_when>
    <automated>grep -v '^#' frontend/style.css | grep -c 'rgba(0, 0, 0, 0.0[0-9]*)'</automated>
    <fails_when>计数不为 0(围栏外出现裸 rgba() —— 违反了 R-2 的不变量;alpha 必须走围栏内的 --color-overlay-* 令牌)</fails_when>
    <automated>awk '/===== DESIGN TOKENS: START/{f=1} /===== DESIGN TOKENS: END/{f=0} !f' frontend/style.css | grep -c 'box-shadow: inset 0 0 0 999px'</automated>
    <fails_when>计数不为 2(hover 组与 active 组各一条)</fails_when>
  </verify>
  <done>两组规则已追加在文件末尾;填充按钮 hover 时计算 `box-shadow` 含 `inset 0 0 0 999px` 且 `background-color` 与静默时相同;按下时叠层 alpha 为 0.12;`#selection-menu button` 与透明底朴素按钮不受影响;既有九项 UAT 仍全绿。</done>
  <acceptance_criteria>
    - `grep -c 'box-shadow: inset 0 0 0 999px var(--color-overlay-hover);' frontend/style.css` 输出 1
    - `grep -c 'box-shadow: inset 0 0 0 999px var(--color-overlay-active);' frontend/style.css` 输出 1
    - 十条 hover 选择器全部在位:`grep -c ':not(:disabled):hover' frontend/style.css` 输出 10
    - 十条 active 选择器全部在位:`grep -c ':not(:disabled):active' frontend/style.css` 输出 10
    - `grep -c '#chat-input-row button:not(:disabled):hover' frontend/style.css` 输出 1
    - `grep -c 'button.primary:not(:disabled):hover' frontend/style.css` 输出 1
    - `grep -c '.overlay-card button:not(:disabled):hover' frontend/style.css` 输出 1
    - `grep -c 'selection-menu button' frontend/style.css` 输出 2(既有两条,未增未减)
    - `grep -c 'opacity' frontend/style.css` 与改动前**相同**(本任务不引入任何 opacity 用途)
    - `grep -c 'transform' frontend/style.css` 输出 0
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 3:input / select 的 hover 加深 + 两条新 PAIR + 清单计数 52 + SC5 / SC5′ 运行时探针</name>
  <files>frontend/style.css, scripts/check-02-contrast.py, scripts/check-05-ui-uat.py</files>
  <read_first>
    - frontend/style.css(围栏内 PAIR 清单的 NON-TEXT 段 L405-425 与头部计数注释 L323-343;围栏外 L561-576 `#ai-route-select` / `#project-path-input`、L684-691 `#enter-form input[type="text"]`、L874-882 `#chat-input-row input`、L918-924 `#round-switcher`、L1122-1130 `#confirmation-modal input[type="text"]`、L1152-1159 `#check-switcher`、L1212-1219 `.verdict-note-input`;L1220-1222 `.verdict-buttons button:disabled`;L1227-1324 文件末尾追加区)
    - frontend/index.html(L22 `#message-input`、L46 `#check-switcher`、L67 `#ai-route-select`、L71 `#project-path-input`、L95 `#enter-path-input`、L136 `#round-switcher`、L174 `#confirm-word-input`)
    - frontend/app.js(L700-702 的 `.verdict-note-input` 动态输入框;L718-719 与 L732-733 的 `fixBtn.disabled` / `keepBtn.disabled` 真实状态切换;L675 `renderVerdictCard(question, mode)` 的签名与它在 `#verdict-cards` 下的挂载点)
    - scripts/check-05-ui-uat.py(L166-190 的 `ok_true` / `blocked` / `info`;L281-282 `read_style`;L369-389 `resolve_color`;L405-418 `effective_bg`;L2179-2238 的 `_idi06_clearance_assert` / `_idi06_hit_assert` 形态纪律;L2333-2361 的样本循环与可见性说明)
    - scripts/check-02-contrast.py(L28-31 `PAIR_RE`、L150-167 覆盖地板与原始标记计数)
  </read_first>
  <action>
    `input` / `select` 的 hover。在文件末尾追加一条规则组(硬规则 3:追加,不重排),声明体只有一行 `border-color: var(--color-border-hover);`,选择器按**既有 ID 级规则体逐条枚举**(这是本任务的承重部分 —— 通用 `input:hover` 是 0-1-1,会被所有 1-0-0 的 ID 规则盖掉,等于不生效):

    - `#ai-route-select:where(:not(:disabled)):hover`(1-1-0,压过 `#ai-route-select` 的 1-0-0)
    - `#project-path-input:where(:not(:disabled)):hover`(1-1-0,压过 1-0-0)
    - `#round-switcher:where(:not(:disabled)):hover`(1-1-0,压过 1-0-0)
    - `#check-switcher:where(:not(:disabled)):hover`(1-1-0,压过 1-0-0)
    - `#enter-form input[type="text"]:hover`(1-1-1,与既有规则同特异性,靠源码顺序取胜)
    - `#chat-input-row input:where(:not(:disabled)):hover`(1-1-1,压过 `#chat-input-row input` 的 1-0-1)
    - `#confirmation-modal input[type="text"]:hover`(1-1-1,同特异性靠顺序取胜)
    - `.verdict-note-input:where(:not(:disabled)):hover`(0-2-0,压过 `.verdict-note-input` 的 0-1-0)

    覆盖核对:`index.html` 的 4 个静态 `<input>`(`#message-input` / `#project-path-input` / `#enter-path-input` / `#confirm-word-input`)+ 3 个 `<select>`(`#check-switcher` / `#ai-route-select` / `#round-switcher`)+ `app.js` 动态建的 `.verdict-note-input`,**逐条都有服务对象**。注释必须写明:①枚举与既有 ID 规则体一一对应,不用通用 `input:hover`(它 0-1-1 会被 ID 规则盖掉);②`:not(:disabled)` 在 `input` / `select` 上是**防御性写法** —— 全站 8 条 `:disabled` 规则**全部是按钮**,今天没有被禁用的 `input` / `select`,这条 gate 今天看似冗余;它不依赖「今天恰好没有」,将来给输入框加禁用态时仍能兜住,**不得当作冗余代码删除**(与 06-CONTEXT D-09 的 `min-width: 0` 同型,照 style.css L460-465 的注释形态写);③`border-color` 在 INTERACT-02 的过渡允许列表内,可平滑过渡;④**不加 `:active`** —— 文本框的「按下」无意义。

    加两条 PAIR。在 `frontend/style.css` 围栏内 NON-TEXT 段里,`--color-border-strong` 的两条条目之后插入一条分组注释 + 两条条目:
    - 注释写明 `--color-border-hover` 是输入控件的 hover 边界(SC 1.4.11 的 state indicator),地面与 `--color-border-strong` 同两处。
    - `/* PAIR --color-border-hover ON --color-surface-page NON-TEXT */`
    - `/* PAIR --color-border-hover ON --color-surface NON-TEXT */`
    两条必须逐字符合 `PAIR_RE`,否则 `raw_pairs != len(pairs)` 会 FAIL。

    改写清单头部计数注释:把上一计划刚写的 `24 / 34 / 43 / 47 / 50` 改为 `24 / 34 / 43 / 47 / 50 / 52`,并把第五个值层的句子拆成两句 —— 50 那层只讲三条焦点环条目,新增的 52 层讲两条 `--color-border-hover` 条目。段末方法论句子里的数字序数同步改为 `six`。
    **登记这条注释为什么是 52 而不是 50:** 规划期的模式图按「只有三条焦点环配对」预估了 50;D-10 的「加深一步」需要一个新 tier-2 令牌,而该文件自己的纪律是「枚举**实际渲染**的组合」,一个用于 UI 边界的新令牌必须有自己的 NON-TEXT 配对 —— 故实际落地是 52(35 TEXT + 17 NON-TEXT)+ 1 ordering entry。**写 50 而落 52 会让注释与清单漂移**,而 `check-02` 的 docstring 正是以「漂移必须可见」为立身之本。

    在 `check-05` 第 10 项里加 SC5 / SC5′ 两条运行时探针:

    - **SC5(hover / active 有反馈)**:在 `p1` 样本上,对 `#btn-process-round`(填充,1-0-0)与 `#message-input`(输入框)各做一次「静默读值 → `page.hover(sel)` → 再读值」的对照。填充按钮断言 `background-color` **不变**且 `box-shadow` 含 `inset 0 0 0 999px`(期望值里的 alpha 用 `resolve_color(page, "--color-overlay-hover")` 与 `resolve_token` 解析,不硬编码);输入框断言 `border-color` 从静默值变为 `resolve_color(page, "--color-border-hover")`。随后 `page.mouse.down()` 读填充按钮的 `box-shadow`,断言其中出现 `--color-overlay-active` 的 alpha。**每个探针在读值前必须先断言目标元素存在且可见**(`getBoundingClientRect()` 非全零),否则读数会让断言退化成空转 PASS —— 这是 `check-05` docstring 点名的同型陷阱。
    - **SC5′(禁用态零反馈)**:在 `checking` 样本上(`#checks-panel` / `#verdict-cards` 可见),用应用自身的 `renderVerdictCard({number: …, question: …, …}, mode)` 造出一张裁决卡(它产生 `.verdict-buttons button` —— **朴素**按钮,无 class),再用 `page.evaluate` 把这两个按钮的 `.disabled` 置为 `true`(这正是 `app.js` L718-719 的真实状态切换,不是伪造 DOM)。然后「静默读 `background-color` → `page.hover(sel)` → 再读」,断言**两者相同**。这条断言是 D-07 的 gate 生效证明 —— 它今天会 FAIL(未 gate 的 `button:hover` 会给它上 `--color-surface-hover`)。另断言该禁用按钮的计算 `opacity` 仍为 `"0.5"`(未被软化;`.verdict-buttons button:disabled` 用的是 0.5,不是 0.55)。**造不出裁决卡或按钮不可见 ⇒ `blocked(...)`,绝不记 PASS。**
    - 项末尾 `page.set_viewport_size(VIEWPORT_RESTORE)` 兜底复位(本项用 `page.hover()` / `page.mouse.down()`,可能改变滚动位置)。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>末行不是 "PASS: 0 failures";或出现 "FAIL: manifest coverage … below floor"、"FAIL: N '/* PAIR' markers but only M parsed"</fails_when>
    <automated>.venv/bin/python scripts/check-02-contrast.py | grep -c 'PASS  [0-9.]*  --color-border-hover'</automated>
    <fails_when>计数不等于 2(两条新配对未全部解析并达标)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>任一条不是恰好一行 "PASS"</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 10</automated>
    <fails_when>exit != 0;或 SC5′ 的「禁用态 hover 背景与静默相同」出现 FAIL(说明 gate 没生效);或任一条走 BLOCKED</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8,9</automated>
    <fails_when>exit != 0,或逐项结论里出现任一项非 PASS</fails_when>
  </verify>
  <done>输入控件的 hover 加深规则覆盖 4 个静态 input + 3 个 select + 1 个动态 input;两条 `--color-border-hover` 配对 PASS;清单头部计数注释为 52 且与清单实际条目数一致;SC5 在 p1 上读到填充按钮 hover 的 inset 叠层与输入框的 border-color 变化;SC5′ 在 checking 上证明禁用朴素按钮 hover 时背景与静默**相同**且 `opacity` 仍为 0.5;既有九项 UAT 与四条既有门全绿。</done>
  <acceptance_criteria>
    - `grep -c 'PAIR --color-border-hover' frontend/style.css` 输出 2
    - `grep -c '24 / 34 / 43 / 47 / 50 / 52' frontend/style.css` 输出 1
    - `grep -c 'Phase 7 lands 52 pairs (35 TEXT + 17 NON-TEXT)' frontend/style.css` 输出 1
    - `grep -c 'border-color: var(--color-border-hover);' frontend/style.css` 输出 1
    - `grep -c '#enter-form input\[type="text"\]:hover' frontend/style.css` 输出 1 且 `grep -c '#confirmation-modal input\[type="text"\]:hover' frontend/style.css` 输出 1
    - `grep -c '.verdict-note-input:where(:not(:disabled)):hover' frontend/style.css` 输出 1
    - `.venv/bin/python scripts/check-02-contrast.py | grep -c '^PASS'` 输出 >= 52
    - `grep -c 'def renderVerdictCard\|renderVerdictCard(' scripts/check-05-ui-uat.py` 输出 >= 1(SC5′ 走应用自身的渲染函数,不手工拼 DOM)
    - `grep -c 'verdict-note-input' scripts/check-05-ui-uat.py` 输出 >= 1
    - `git diff --stat -- frontend/app.js frontend/index.html frontend/vendor/` 输出为空
  </acceptance_criteria>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 新增交互态规则 → 既有填充色族的级联 | 特异性算错会让「修 hover」变成「覆盖填充色」,而源码 diff 看起来完全无辜 |
| 交互态 → 禁用态语义 | 禁用态是 G3 前提条件唯一的视觉信号;任何让它响应 hover 的路径都会削弱那个信号 |
| 围栏 → 围栏外 | `rgba()` 与 tier-1 引用一旦泄漏到围栏外,`check-01` 与 R-2 的不变量同时被打破 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-07-06 | Tampering | 填充按钮 hover 规则的选择器特异性 | high | mitigate | 十条选择器逐条列出**具体特异性数值**并要求逐条跨过对应既有规则;注释里点名「`button:not(:disabled):hover`(0-2-1)对 `#btn-authorize`(1-0-0)无效」这条具体失效模式;SC5 在真实浏览器里读 `box-shadow` 验证 |
| T-idi-07-07 | Elevation of privilege(禁用态响应交互) | L587 的 `button:hover` vs `.verdict-buttons button:disabled` | high | mitigate | gate 落在 L587 的选择器上(`:where(:not(:disabled))`),特异性逐位不变;SC5′ 用真实 `renderVerdictCard` + 真实 `.disabled` 切换断言「hover 背景 == 静默背景」;`opacity` 未被软化 |
| T-idi-07-08 | Tampering | 朴素 `:active` 规则的特异性 | medium | mitigate | 规则写成 `:where(button:not(:disabled)):active`(0-1-0),刻意低于 0-1-1 的填充族;注释写明「改高即把填充按钮按下时刷成灰底」 |
| T-idi-07-09 | Information disclosure / Repudiation | 围栏外的裸 `rgba()` | medium | mitigate | alpha 值收进围栏内的 `--color-overlay-hover` / `--color-overlay-active`;`grep -v '^#' | grep -c 'rgba(0, 0, 0, 0.0'` 必须为 0(该纪律**无机械守卫**,故本计划把它升为一条显式断言) |
| T-idi-07-10 | Spoofing(假 PASS) | SC5 / SC5′ 探针 | high | mitigate | 读值前先断言目标元素存在且可见;造不出裁决卡 ⇒ `blocked`;期望侧用 `resolve_color` 解析令牌而非硬编码 rgb |
| T-idi-07-11 | Tampering | 值碰撞被后来者「修正」 | low | mitigate | `--color-surface-active` 的注释点名 04.1-N-4 与 `--color-surface-user`,并同步扩写 L293-297 的第 3 条;`--color-border-hover` 与 `--color-text-muted` 的同值碰撞同样登记 |
| T-idi-07-SC | Tampering | npm / pip / cargo 安装 | low | accept | 零新增运行时依赖、零构建步骤(硬规则 6):无包管理器调用进入范围;若执行期出现安装需求,即为计划偏差与停止条件 |
</threat_model>

<verification>
- 执行前基线:`bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh` 全 PASS;`.venv/bin/python scripts/check-02-contrast.py | tail -1` 为 `PASS: 0 failures`;`.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8,9` exit 0。
- 执行后同一条命令组必须仍全绿;另跑 `.venv/bin/python scripts/check-05-ui-uat.py --item 10` exit 0。
- `git diff --numstat -- frontend/style.css` 的删除行数只允许来自 L587 那一行的选择器改写(≤ 2);其余改动全部是新增。
- 必须使用项目 venv(`.venv/bin/python`)。
- `git status --porcelain -- frontend/app.js frontend/index.html frontend/vendor/ scripts/ui-states/` 输出为空。
</verification>

<success_criteria>
1. 所有有底色语义的按钮 hover 时出现统一 rgba 压暗叠层(`background-color` 不变、`box-shadow` 出现 inset),按下时 alpha 提到 0.12。
2. 朴素按钮 hover 变 `--color-surface-hover`、按下变 `--color-surface-active`;填充按钮的按下态不被朴素规则抢走。
3. **禁用按钮 hover 时背景与静默时完全相同**(`.verdict-buttons button:disabled` 的缺陷被修掉),`opacity` 未被软化。
4. `input` / `select` hover 时边框加深一步,8 条既有 ID 级规则体全部被覆盖。
5. `--color-surface-active` 与 `--color-border-hover` 的值碰撞被显式登记,不会被后来者当违规修掉。
6. 四条既有门与既有九项 UAT 全绿;`app.js` / `index.html` / `vendor/` / `ui-states/` 零改动。
</success_criteria>

<output>
Create `.planning/phases/idi-07-interaction-states-and-focus/idi-07-02-SUMMARY.md` when done
</output>
---
phase: idi-07-interaction-states-and-focus
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - frontend/style.css
  - scripts/check-05-ui-uat.py
  - scripts/probe-07-focus-composite.py
autonomous: true
requirements: [A11Y-01]
estimate:
  tokens: 72000
  raw_tokens: 72000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "键盘 Tab 到任一按钮 / 输入框 / 下拉,该元素的计算 outline-width 为 2px 且 outline-color 等于运行时解析的 --color-focus(D-05 / D-17 SC1)"
    - "鼠标点击控件后该元素的计算 outline-color 不等于 --color-focus(:_focus-visible 语义成立,D-17 SC2)"
    - "枚举 button, input, select, textarea, a[href], summary, [tabindex] 的全部实例后,「未被环覆盖的可聚焦元素数」为 0(D-16)"
    - "环色对 --color-surface-page / --color-surface / --color-surface@0.75 三处的对比度 >= 3:1(D-03 / D-15)"
    - "五个状态样本的 #round-doc 内 a[href] 计数为 0 这一事实被显式登记,归档半场的运行时断言以一次性注入探针交付(D-18)"
  artifacts:
    - "frontend/style.css:围栏内 --color-focus: #1f63bd 声明 + 围栏外末尾的 7 选择器 :focus-visible 规则"
    - "frontend/style.css:PAIR 清单头部的值层计数注释(47 → 50;该注释住在 style.css:334,不在 check-02-contrast.py 里)"
    - "frontend/style.css:PAIR 清单新增三条 --color-focus 条目(含 @0.75)"
    - "scripts/check-05-ui-uat.py:第 10 项及其四处登记点 + _IDI07_* 普查 JS"
    - "scripts/probe-07-focus-composite.py(一次性注入探针,不进守卫契约)"
  key_links:
    - "--color-focus 的声明与它的 :focus-visible 消费者同一次提交(硬规则 5);围栏内计数 == 1 且围栏外 var(--color-focus) 计数 > 0"
    - ":focus-visible 的枚举集与 scripts/check-05-ui-uat.py 的可聚焦普查集逐字同集(button, input, select, textarea, a[href], summary, [tabindex])"
    - "环几何 2px + outline-offset: 2px 与 check-05 的 CLEARANCE_MIN_PX = 4.0 双向绑定"
  prohibitions:
    - "不得把 outline: none 或 outline: 0 用作焦点样式"
    - "不得在任何 :focus-visible 规则里设置 border 或 padding"
    - "不得为「让环更柔和」把 outline-color / outline-width 加进任何 transition 的属性列表"
    - "不得写针对 #round-doc 的 :focus-visible 规则(今天不可聚焦 ⇒ 死代码)"
    - "不得重排既有声明,不得触碰 .hidden 规则、.fatal 修饰符、#selection-menu 的 DOM 位置、showInlineError、renderAnnotations、renderVerdictCard"
    - "不得新增 !important、@layer、@property、var(--x, #fallback)、任何运行时依赖或构建步骤"
    - "不得编辑 frontend/app.js、frontend/index.html、frontend/vendor/"
---

<!-- planner-discipline-allow: outline: none -->
<!-- planner-discipline-allow: sed -->

<objective>
把全站作者化焦点环从「零」建成「可断言」(A11Y-01 / D-03 / D-04 / D-05 / D-06 / D-15 / D-16 / D-17 / D-18 / D-20)。

本计划交付三件事:①围栏内声明 `--color-focus: #1f63bd` 并在文件末尾追加 7 选择器的 `:focus-visible` 规则(几何固定 `outline: 2px solid` + `outline-offset: 2px`);②把环色的三处验证面落进 `check-02` 的 PAIR 清单(含 `.archive-mode` 的 0.75 合成);③在 `check-05` 新增第 10 项,按「元素普查」口径断言环覆盖全部可聚焦实例,并交付 D-18 的一次性反事实探针。

Purpose: 焦点环是本阶段唯一**新增**的样式层(HEAD 上 `:focus` / `outline` 计数均为 0),也是 Phase 8 `tabindex` 承诺的前置条件;它必须**先于**任何 tabindex 落地,否则会造出「可聚焦但焦点不可见」的中间状态。
Output: `frontend/style.css` 的新令牌与新规则、`check-02` 的三条新配对与计数注释、`check-05` 的第 10 项、`scripts/probe-07-focus-composite.py`。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/idi-07-interaction-states-and-focus/07-CONTEXT.md
@.planning/phases/idi-07-interaction-states-and-focus/idi-07-PATTERNS.md
@.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md
@.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md
</context>

<decision_register>
**D-01 基线口径:** 以磁盘 HEAD 为唯一现实基线。ROADMAP Phase 7 段与 `04-UI-SPEC.md` 的环色条款仅作意图参考。本计划执行前必须先跑四条既有门建立「执行前基线」(见 Task 2)。

**D-04 环色 = `#1f63bd`:** 选它不是因为它在 Radix 刻度上(**它不在**),而是因为 S-4 的签核算术(「删除 `opacity` 后环回到 5.62」)是拿它算的。围栏注释必须写明这是**对已签核契约的字面遵从,不是漏改**,否则会被后来者当成漂移修掉。

**D-06 `#round-doc` 负空间:** 本计划**不写**任何针对 `#round-doc` 的规则。它今天不可聚焦,那条规则是死代码,且无法被运行时验证;Phase 8 加 `tabindex="0"` 时连同它自己的内嵌处理一起落地。围栏注释须以本文件既有的「不写什么」口吻写明这条指派。
</decision_register>

<flagged_assumptions>
边缘覆盖探针对本阶段三条需求全部返回 `unclassified` / `unresolved`(探针的分类词表是英文/标记式的,读不了这三条中文需求文本)。**不得把 `unclassified` 当作「无边缘情况」,也不得自动 resolve。** 本阶段把三条逐条登记为**显式标记的假设**,说明哪些边缘情况在范围内、哪些不在、为什么:

- **A11Y-01(本计划)** — 假设:焦点环的**几何**边缘(环被裁剪容器的 padding 切掉)由 `check-05` 第 9 项的 L-5 clearance 普查(`CLEARANCE_MIN_PX = 4.0`)承担,**不在本计划内**重复实现;本计划只补一条 Tab 探针把「几何」与「实际焦点」接上(Task 3)。**不在范围内**:`#round-doc` 的环承载面(D-06,指派 Phase 8)、暗色模式下的环色(全局已裁定排除)。
- **INTERACT-01(计划 02)** — 假设:`:disabled` 的 8 条既有规则里,只有 `.verdict-buttons button:disabled` 会因未 gate 的 `button:hover` 而变色(其余 7 条是 1-0-0 填充按钮,免疫);门只对这个**真实缺陷现场**断言「禁用态 hover 时背景与静默时相同」。**不在范围内**:8 条 `:disabled` 声明的收敛重构(改特异性会翻掉 1-0-0 填充色,风险大于收益)、WCAG SC 1.4.3 对非活动组件的豁免面(不属 AA,不进 PAIR 清单)。
- **INTERACT-02(计划 03)** — 假设:过渡只覆盖 `button` / `input` / `select` 三类真实存在的控件(`<textarea>` 全站计数为 0),且「尊重减弱动效」只按**选择器重写为 `none`** 实现。**不在范围内**:动效/动画设计体系、`opacity` 作为过渡属性、行业标准的 `*, *::before, *::after { transition-duration: 0.01ms !important }` 片段(两个 `!important` 会让 `check-04` 立刻变红)。
</flagged_assumptions>

<artifacts_this_phase_produces>
本阶段(三个计划合计)新建的符号与路径 —— 每个计划重复列出同一份清单,便于逐计划对照:

**新的 CSS 自定义属性(全部在围栏 `:root` 内,零新增 tier-1 primitive):**
- `--color-focus: #1f63bd`(计划 01)
- `--color-surface-active: var(--radix-gray-4)`(计划 02)
- `--color-border-hover: var(--radix-gray-11)`(计划 02)
- `--color-overlay-hover: rgba(0, 0, 0, 0.06)`(计划 02)
- `--color-overlay-active: rgba(0, 0, 0, 0.12)`(计划 02)

**新的选择器规则(全部追加在 `frontend/style.css` 文件末尾):**
- 7 选择器 `:focus-visible` 规则(计划 01)
- `button:where(:not(:disabled)):hover`(**既有 L587 的选择器就地改写**,声明一字不动;计划 02)
- `:where(button:not(:disabled)):active`(计划 02)
- 填充按钮 hover / active 的 rgba 叠层规则组(计划 02)
- `input` / `select` hover 的 `border-color` 规则组(计划 02)
- `button, input, select { transition: ... }` 挂载规则(计划 03)
- `@media (prefers-reduced-motion: reduce)` 块(计划 03)

**新的脚本符号与路径:**
- `scripts/check-05-ui-uat.py`:`item10(page, tmp_root)`、`_idi07_focus_census_assert(...)`、`_idi07_hit_assert` 同族的 SC5 探针、`_idi07_focus_contract_guards(item)`(计划 03)、模块级 `_IDI07_*` 普查 JS 常量、`EXPECTED_MEDIA_QUERIES` 0 → 1(计划 03)
- `scripts/probe-07-focus-composite.py`(新文件,一次性注入探针,**不进守卫契约**;计划 01)
- `frontend/style.css`:仅新增 PAIR 清单条目与头部计数注释(零新脚本代码;计划 01 / 02)。**`scripts/check-02-contrast.py` 只被读、不被改** —— 它只提供 `PAIR_RE` / `composite()` / 覆盖地板,清单与计数注释都住在 `frontend/style.css:334` 的围栏注释里

**不新建:** `scripts/check-07-*.sh` 或 `check-06-*`(编号已占用,且与 Phase 6「扩在既有门」的先例相悖,D-15)。
</artifacts_this_phase_produces>

<tasks>

<task type="tracer">
  <name>Task 1 (tracer):焦点环端到端 —— 一条令牌 → 一条 CSS 规则 → 算术门 → 浏览器里读到的环</name>
  <files>frontend/style.css, scripts/check-05-ui-uat.py</files>
  <read_first>
    - frontend/style.css(围栏 `:root` 的 L182-215 surface/border 段与 L320-425 的 PAIR 清单;L578-588 的 `button` 基础规则;L1227-1324 的文件末尾追加区,尤其 L1242 的 `button, input, select { color: var(--color-text); }` 与 L1313-1324 的枚举式规则注释)
    - scripts/check-01-token-conformance.sh(围栏配对断言 + 围栏外裸 `#hex` 与 tier-1 `var()` 引用的两条守卫)
    - scripts/check-02-contrast.py(L28-31 的 `PAIR_RE` 逐字形态、L150-167 的覆盖地板与原始标记计数校验、L177-196 的 `@<alpha>` 合成实现)
    - scripts/check-05-ui-uat.py(L31-92 的 docstring 运行方式与逐项说明块、L166-190 的 `ok_true` / `blocked` / `info`、L281-282 的 `read_style`、L369-389 的 `resolve_color`、L1606-1628 的 `_l2_guard_shape` 形态、L1660-1685 的可聚焦普查集、L2248-2255 的 `item9` 骨架、L2425-2534 的 `parse_args` / `normalize_items` / `main` 的四处登记点)
    - .planning/phases/idi-07-interaction-states-and-focus/idi-07-PATTERNS.md 的「`:focus-visible`(D-05 / D-06)」与「`scripts/check-05-ui-uat.py` — 新增 item 10」两节
  </read_first>
  <action>
    围栏内声明环色令牌。在 `frontend/style.css` 的围栏 `:root` 里、`--color-text-info`(L196)之后、`/* Tier 2 — overlay backdrop and the shadow tokens */`(L199)之前,插入一个独立的 tier-2 分组:

    - 分组注释首行:`/* Tier 2 — focus ring (A11Y-01 / D-04, declared with its consumer: the
      :focus-visible rule at the end of this file — Hard Rule 5).`
    - 注释正文必须写明三条承重事实:①`#1f63bd` 是整个颜色层里**唯一不在 Radix 刻度上**的值(除 `--white` 与两个 `rgba()` 阴影),它与 04.1「值必须来自 Radix 步」的纪律相冲;②它是**对已签核契约的字面遵从,不是漏改** —— S-4 的签核算术(`04-UI-SPEC.md` §Sign-Off Items S-4:「删除 `opacity` 后环回到 5.62」)是拿它算的,**不得被「修」成 `--radix-blue-11`**;③不选 `--radix-blue-11` 的理由是它在 `.archive-mode` 的 0.75 合成下只剩 3.03:1(余量 0.03),不选 `--radix-blue-12` 的理由是它是高对比文字步、作为 2px 环视觉上接近边框。
    - 声明行:`--color-focus: #1f63bd;`

    围栏外追加焦点规则。在文件**末尾**追加一条独立规则(硬规则 3:追加,不重排),选择器**逐字**为 D-05 的七个枚举,顺序亦同:`button:focus-visible,` / `input:focus-visible,` / `select:focus-visible,` / `textarea:focus-visible,` / `a[href]:focus-visible,` / `summary:focus-visible,` / `[tabindex]:focus-visible`。声明体恰为两行:`outline: 2px solid var(--color-focus);` 与 `outline-offset: 2px;`。**绝不出现 `border` 或 `padding`**(后者会 reflow `#probe-controls`,Tab 一次按钮跳一次)。**绝不写 `outline: none`**。**绝不写针对 `#round-doc` 的规则**(D-06:它今天不可聚焦,那条是死代码,指派 Phase 8)。

    该规则的注释必须写明四条:①**为什么枚举而不是裸 `:focus-visible`** —— 与本项目 Phase 5(`G-idi-05-1`)/ Phase 6(`overflow-wrap`)建立的同一口径:影响面必须可枚举、可对照;裸通配不是「更全」而是「不可审」。②**枚举集与 `check-05` 的普查集逐字同集** —— 点名 `scripts/check-05-ui-uat.py` 的可聚焦普查集 `button, input, select, textarea, a[href], summary, [tabindex]`,并写明「新增一类可聚焦元素要**同时**改两处」。③**几何是双向绑定的** —— `2px + outline-offset: 2px` 的外伸量恰为 4px,正是 `check-05` 的 `CLEARANCE_MIN_PX = 4.0` 与 `idi-06-UI-SPEC.md` §L-5 所假设的值;改几何即改那个门的阈值。④`[tabindex]` 今天**无服务对象**(全站 `[tabindex]` 计数为 0),这是**防御性非冗余**写法 —— 照 06-CONTEXT D-09 的 `min-width: 0` 注释形态说明「它今天看似冗余,为什么不是」,并登记 Phase 8 会给 `#round-doc` 加 `tabindex="0"`、届时这条规则会自动把环套上去。

    加一条算术配对。在 `frontend/style.css` 围栏内的 PAIR 清单里,`/* PAIR --color-text ON --color-surface TEXT@0.75 */`(L394-395 的「the surviving whole-document dim」分组)**紧邻其后**插入一条新的分组注释 + 一条配对:

    - 分组注释写明:焦点环是 SC 1.4.11 的 state indicator;三处验证面 = `--color-surface-page` / `--color-surface` / `--color-surface`@0.75;`--color-surface-sunken` **不进验证面**(它只是 `.markdown-body code` 与 `.badge-answered` 的背景,不是任何可聚焦元素的相邻地面)。
    - 条目:`/* PAIR --color-focus ON --color-surface NON-TEXT */`(本任务只落这一条;另两条在 Task 2)。

    条目必须逐字符合 `check-02` 的 `PAIR_RE`(`/* PAIR --a ON --b NON-TEXT */`,大小写与空格敏感),否则 `raw_pairs != len(pairs)` 会 FAIL。

    在 `check-05` 新增第 10 项。`scripts/check-05-ui-uat.py` 有**四处登记点,漏一处即不可达或不可发现**,本任务全部补齐:

    1. 模块 docstring 的**运行方式**列表(L31-40)加一行 `.venv/bin/python scripts/check-05-ui-uat.py --item 10  # 只跑焦点环覆盖与交互态`;
    2. 模块 docstring 的**逐项说明**块(L42-92)加「第 10 项(A11Y-01 / INTERACT-01 / INTERACT-02)」段落,照「第 9 项」的形态写明:断言分「静态契约计数」与「运行时元素普查」两段;普查口径是「未被环覆盖的可聚焦元素数为 0」而非「规则被写下了」;并登记五个状态样本的 `#round-doc` 内 `a[href]` 计数为 0 这一事实;
    3. `parse_args` 的 `--item` help 字符串(L2427-2428)改为 `smoke / 1 / 2 / 3 / 4 / 5 / 6 / 7 / 8 / 9 / 10`;
    4. `normalize_items` 的默认列表(L2441)追加 `"10"`、`main()` 的 `known` 集合(L2454)追加 `"10"`(漏加会直接 `SystemExit("ERROR: 未知项 …")`),并在分发块(L2497-2498)之后加 `if "10" in items: item10(page, tmp_root)`。

    新增 `item10(page, tmp_root)`,本任务只落**最小端到端探针**:用 `make_fixture("p1", tmp_root)` + `enter_project(page, proj)` 进入样本;`page.keyboard.press("Tab")` 若干次直到 `document.activeElement` 匹配 `button`(用 `page.evaluate` 读 `document.activeElement.tagName`);读该元素的 `read_style(page, sel, "outline-width")` 与 `"outline-color"`;期望侧用 `resolve_color(page, "--color-focus")`(**不得硬编码 `rgb(31, 99, 189)`** —— 这是 `check-05` L974 立下的纪律:期望侧来自运行时解析的令牌,值的仲裁者是 `check-02-contrast.py`)。元素读不到时 `blocked(...)`,**绝不记 PASS**。项末尾 `page.set_viewport_size(VIEWPORT_RESTORE)` 兜底复位。

    本任务**不做**完整普查(Task 3)、不落另两条 PAIR、不改清单头部计数注释(Task 2)。
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>exit != 0,或输出不是恰好一行 "PASS"(出现 "FAIL: … bare hex outside the token block" 或 "FAIL: … tier-1 primitive reference(s)" 即为失败)</fails_when>
    <automated>.venv/bin/python scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>末行不是 "PASS: 0 failures"(出现 "FAIL" 行或非零 exit 即为失败)</fails_when>
    <automated>bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>任一条不是恰好一行 "PASS"(check-03 报 "expected 1 '.hidden {' rule";check-04 报 "expected 1 '!important;' declaration")</fails_when>
    <automated>grep -v '^#' frontend/style.css | grep -c ':focus-visible'</automated>
    <fails_when>计数为 0,或少于 7(七选择器枚举缺失)</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 10</automated>
    <fails_when>exit != 0(0=全 pass;1=有 FAIL 断言;2=有 BLOCKED 断言 —— 环色读不出、期望令牌解析不出、或 Tab 后 activeElement 不是按钮都会走 BLOCKED)</fails_when>
  </verify>
  <done>围栏内 `--color-focus` 已声明且被围栏外的 `:focus-visible` 规则消费;7 选择器焦点规则已追加在文件末尾,只声明 `outline` 与 `outline-offset`;`check-02` 新增的 `--color-focus ON --color-surface NON-TEXT` 条目 PASS;`check-05 --item 10` 在 p1 样本上读到环的 `outline-width == 2px` 且 `outline-color` 等于运行时解析的 `--color-focus`;四条既有门(check-01/02/03/04)仍全绿。整条链路(令牌 → 规则 → 算术门 → 浏览器读数)已在一个提交里可复跑。</done>
  <acceptance_criteria>
    - `grep -n '\-\-color-focus: #1f63bd;' frontend/style.css` 有输出,且读出的行号落在围栏 START 与 END 之间(用 `grep -n 'DESIGN TOKENS: START\|DESIGN TOKENS: END'` 的行号做区间比对)
    - `grep -n 'outline: 2px solid var(--color-focus);' frontend/style.css` 有输出
    - `grep -n 'outline-offset: 2px;' frontend/style.css` 有输出
    - `awk '/===== DESIGN TOKENS: START/{f=1} /===== DESIGN TOKENS: END/{f=0} !f' frontend/style.css | grep -n 'outline:'` 的行数恰等于 1(焦点规则只声明一处 `outline`)
    - `grep -v '^#' frontend/style.css | grep -c 'outline: none'` 输出 == 0(不得把 `outline: none` 当焦点样式)
    - `grep -n 'textarea:focus-visible\|a\[href\]:focus-visible\|\[tabindex\]:focus-visible' frontend/style.css` 的输出覆盖三行(逐行核对,不数个数)
    - `grep -c 'round-doc:focus-visible' frontend/style.css` 输出 == 0(D-06 负空间)
    - `grep -o 'var(--color-focus)' frontend/style.css | wc -l` 输出 >= 2(一处声明于围栏内、至少一处消费于围栏外)
    - `grep -n 'PAIR --color-focus ON --color-surface NON-TEXT \*/' frontend/style.css` 有输出
    - `grep -o 'PAIR --color-focus' frontend/style.css | wc -l` 输出 == 1(本任务只落这一条配对)
    - `grep -n 'def item10' scripts/check-05-ui-uat.py` 有输出;`grep -o '"10"' scripts/check-05-ui-uat.py | wc -l` 输出 >= 3(normalize_items 默认列表 / known 集合 / 分发块)
    - `git ls-files -- frontend/style.css scripts/check-05-ui-uat.py` 两条路径全部非空(全是 tracked source)
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 2:补齐环色的三处验证面 + 清单计数注释 + 归档半场的一次性反事实探针</name>
  <files>frontend/style.css, scripts/check-05-ui-uat.py, scripts/probe-07-focus-composite.py</files>
  <read_first>
    - frontend/style.css(围栏内的 PAIR 清单 L320-425,尤其 L323-343 的清单头部计数演化注释与 L394-395 的 `@0.75` 条目)
    - scripts/check-02-contrast.py(L7-12 的 docstring「漂移必须可见」立身之本、L28-31 的 `PAIR_RE`、L125-127 的 `composite()`、L150-167 的覆盖地板与原始标记计数、L177-196 的 alpha 合成分支)
    - scripts/probe-05-resolve-color.py(全文 245 行 —— L1-13 的定位声明、L29-32 的退出码语义、L63-72 的 `load_harness()`、L75-78 的 `require()`、L92-95 与 L122-131 的「变异必须真的发生」防线、L26-27 的本机 `sed` 陷阱)
    - frontend/style.css 的 L1225 `#rounds-placeholder.archive-mode #round-doc { opacity: 0.75; }`
    - scripts/check-05-ui-uat.py(L424-444 的 `make_fixture` / `enter_project`、L281-282 的 `read_style`、L369-389 的 `resolve_color`、L405-418 的 `effective_bg`)
  </read_first>
  <action>
    补另两条环色配对。在 Task 1 新增的分组注释之后、`--color-focus ON --color-surface NON-TEXT` 条目之后,追加两条(逐字符合 `PAIR_RE`):

    - `/* PAIR --color-focus ON --color-surface-page NON-TEXT */`
    - `/* PAIR --color-focus ON --color-surface NON-TEXT@0.75 */`

    第三条是 `.archive-mode` 的 `opacity: 0.75`(style.css L1225)合成整棵 `#round-doc` 子树的算术模型 —— `check-02` 已内建 alpha 合成(`composite()` + `@<alpha>` 后缀),故**零新代码**即可断言 3.45 >= 3。它必须紧邻 `--color-text ON --color-surface TEXT@0.75`,让两条「0.75 合成」在同一处可对照。

    改写清单头部的计数演化注释(style.css L323-343 的 `Manifest size across four value layers (D-15): 24 / 34 / 43 / 47 —` 那段)。**追加第五个值层**,把句子改成五层:`24 / 34 / 43 / 47 / 50`,并在段末追加:

    - 「Phase 7 lands 50 pairs (35 TEXT + 15 NON-TEXT) + 1 ordering entry — the three focus-ring entries are all NON-TEXT: the ring is a SC 1.4.11 state indicator, and its three verification surfaces are `--color-surface-page`, `--color-surface`, and `--color-surface` at the archive view's 0.75 composite (`--color-surface-sunken` is deliberately NOT among them — it is only the ground of `.markdown-body code` and `.badge-answered`, never adjacent to a focusable element).」
    - 保留原有的方法论句子(「The four numbers are not drift …」)并把其中的「four」改为「five」。

    **不改这条注释 = 清单与令牌块开始漂移**,而该文件开头的 docstring 正是以「漂移必须可见」为立身之本。

    写一次性注入探针 `scripts/probe-07-focus-composite.py`(新文件)。定位**逐字照** `scripts/probe-05-resolve-color.py`:

    - docstring 首段声明它是**反事实证据,不是门**:不进四条守卫命令契约(`check-01`…`check-04`),不被任何门禁 / CI 调用,`scripts/check-05-ui-uat.py` 也不引用它。存在的唯一目的:证明 `/* PAIR --color-focus ON --color-surface NON-TEXT@0.75 */` 这条算术断言**真的会失败/成立**,而不是静默空转。
    - 复用 harness 而不复制实现:按路径 `importlib.util.spec_from_file_location` 导入 `scripts/check-05-ui-uat.py`,复用它的 `make_fixture` / `enter_project` / `read_style` / `resolve_color` / `effective_bg`。
    - 注入内容:在 `archive` 样本里用 `page.evaluate` 向 `#round-doc` 内**合成**一个 `<a href="#">`,然后在 `#rounds-placeholder.archive-mode` 生效的态下读它的 `outline-color`,与 `resolve_color(page, "--color-focus")` 对比;并断言「注入前 `#round-doc` 内 `a[href]` 计数 == 0、注入后 == 1」—— 这是「变异必须真的发生」的防线,**空转的注入会让整条证明失去意义**。
    - **不得用 `sed` 改磁盘文件**(本机是 darwin,BSD `sed` 的 `0,/re/` 地址会静默不替换)。注入只走 `page.evaluate`;磁盘上的 `frontend/style.css` 与五个样本**逐字节不变**。
    - 退出码:`0` = 全部断言成立;`1` = 任一条不成立(哪一条写到 stderr),用 `require(cond, msg)` 辅助实现。

    在 `check-05` 第 10 项的 docstring 说明块里**显式登记**:五个状态样本(`scripts/ui-states/` 的 p1 / p12 / p3 / checking / archive)的 `#round-doc` 内 `a[href]` 计数为 **0** ⇒ 归档半场的**运行时**断言今天没有服务对象;它由常驻算术门(`check-02` 的 `@0.75` 条目)+ 一次性探针(`scripts/probe-07-focus-composite.py`,不进守卫契约)共同承担。**不登记这个事实,读者会把「没有断言」误读成「没有风险」。**
  </action>
  <verify>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>任一条不是恰好一行 "PASS"</fails_when>
    <automated>.venv/bin/python scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>末行不是 "PASS: 0 failures";或出现 "FAIL: manifest coverage … below floor"、"FAIL: N '/* PAIR' markers but only M parsed"(新条目未逐字符合 PAIR_RE)</fails_when>
    <automated>.venv/bin/python scripts/check-02-contrast.py | grep -c 'PASS  [0-9.]*  --color-focus'</automated>
    <fails_when>计数不等于 3(三条环色配对未全部解析并达标)</fails_when>
    <automated>git status --porcelain -- scripts/ui-states/</automated>
    <fails_when>输出非空(探针改动了磁盘上的样本 —— 样本必须只读)</fails_when>
  </verify>
  <done>环色的三处验证面全部进 `check-02` 的 PAIR 清单并 PASS(5.72 / 5.57 / 3.45);清单头部的值层计数注释已扩写为五层且与清单实际条目数一致;`scripts/probe-07-focus-composite.py` 可独立运行,exit 0 表示注入确实发生且归档合成下的环色读数成立,exit 1 表示任一条不成立;`check-05` 的说明块里登记了「五个样本的 `#round-doc` 内 `a[href]` 计数为 0」。</done>
  <acceptance_criteria>
    - `grep -o 'PAIR --color-focus' frontend/style.css | wc -l` 输出 == 3
    - `grep -n 'PAIR --color-focus ON --color-surface NON-TEXT@0.75' frontend/style.css` 有输出
    - `grep -n '24 / 34 / 43 / 47 / 50' frontend/style.css` 有输出
    - `grep -n 'Phase 7 lands 50 pairs (35 TEXT + 15 NON-TEXT)' frontend/style.css` 有输出
    - `.venv/bin/python scripts/check-02-contrast.py | grep -c '^PASS'` 输出 >= 50(47 原有 + 3 新增)
    - `.venv/bin/python scripts/probe-07-focus-composite.py` exit 0(全部断言成立)
    - `grep -n 'def require' scripts/probe-07-focus-composite.py` 有输出且 `grep -o 'load_harness' scripts/probe-07-focus-composite.py | wc -l` 输出 >= 2
    - `grep -cE 'subprocess|os\.system' scripts/probe-07-focus-composite.py` 输出 == 0(注入只走浏览器侧的 `page.evaluate`,不经任何子进程 —— 判据锚在「有没有子进程调用」上,不锚在字符串 `sed` 上:探针 docstring 会照 `probe-05-resolve-color.py` 的先例**解释为什么不用 sed**,那个词合法地出现在散文里)
    - `grep -o 'page.evaluate' scripts/probe-07-focus-composite.py | wc -l` 输出 >= 1(注入确实发生在浏览器侧,而不是在磁盘上)
    - `git status --porcelain -- scripts/ui-states/` 输出为空
    - `git ls-files -- scripts/probe-07-focus-composite.py` 在 `git add` 后非空(新文件,首次提交后即为 tracked source)
  </acceptance_criteria>
</task>

<task type="auto">
  <name>Task 3:焦点环覆盖的元素普查(D-16)+ SC1 / SC2 / SC4 三条运行时探针</name>
  <files>scripts/check-05-ui-uat.py</files>
  <read_first>
    - scripts/check-05-ui-uat.py(L166-190 的 `ok_true` / `ok_contains` / `blocked` / `info`;L281-282 `read_style`;L369-389 `resolve_color`;L392-402 `resolve_token`;L405-418 `effective_bg`;L1547 的「不给结论替代证据」明文;L1596-1700 的 `_IDI06_CENSUS_JS` 与可聚焦普查集;L2028-2049 的常量块;L2179-2209 的 `_idi06_clearance_assert` 五条形态纪律;L2212-2238 的 `_idi06_hit_assert` 前提检查;L2248-2366 的 `item9` 样本循环;L2333-2361 的三样本教训)
    - scripts/check-05-ui-uat.py 的 `_IDI06_SCROLLERS_JS` / `_IDI06_CENSUS_JS`(模块级 `r"""…"""` 常量形态与命名前缀族)
    - .planning/phases/idi-07-interaction-states-and-focus/idi-07-PATTERNS.md 的「Analog C — 『按元素普查 + 断言未覆盖数为 0』的完整形态」与「Analog E / F / G / H」
  </read_first>
  <action>
    在 `scripts/check-05-ui-uat.py` 的常量块(`_IDI06_CENSUS_JS` 附近)新增模块级常量:

    - `FOCUSABLE_SELECTOR = "button, input, select, textarea, a[href], summary, [tabindex]"` —— **逐字**等于 `_IDI06_CENSUS_JS` 里 `document.querySelectorAll(...)` 的那一串(顺序亦同),并加注释写明「这是 D-05 的枚举集,与 `frontend/style.css` 的 `:focus-visible` 规则逐字同集;两者必须同时改」。
    - `FOCUS_RING_WIDTH_PX = 2.0` 与 `FOCUS_RING_OFFSET_PX = 2.0`,注释写明「外伸量 4px = `check-05` 的 `CLEARANCE_MIN_PX = 4.0`;改几何即改那个门的阈值」。
    - `_IDI07_FOCUS_CENSUS_JS = r"""…"""`,命名照 `_IDI06_*` 前缀族。它按 **DOM 遍历**枚举 `FOCUSABLE_SELECTOR` 的全部实例,对每个实例返回 `{el, tag, id, cls, visible, outlineWidth, outlineColor, focusMatches}`:`visible` 取 `el.getClientRects().length > 0`(被祖先藏住的元素 rect 全零,不得把它读成「未覆盖」);`focusMatches` 取 `el.matches(':focus-visible')`(只对当前 `document.activeElement` 有意义,其余恒 false)。

    新增 `_idi07_focus_census_assert(page, item, state)`,逐条复刻 `_idi06_clearance_assert` 的**五条形态纪律**:

    1. `data is None` ⇒ `blocked(...)`,**绝不记 PASS**;
    2. 先 `info()` 落**全部原始行**(每个元素的 tag/id/class + visible + outline 读数),再判定;
    3. 若「可见的可聚焦元素」为空集,`info()` 声明「本样本无判定」并 `return`,**不记空转 PASS**;
    4. 判据是 `not bad` —— 即 **「未被环覆盖的可聚焦元素数 == 0」**,其中 `bad` 定义为 `visible and (outlineWidth != "2px" or outlineColor != focus_color)`;
    5. 失败行的 note 给出**可执行的修复动作**:「该元素不在 `:focus-visible` 的七选择器枚举里 ⇒ 到 `frontend/style.css` 文件末尾补它的选择器,并同步 `check-05` 的 `FOCUSABLE_SELECTOR`」。

    覆盖面的取得方式:**用 `page.keyboard.press("Tab")` 驱动焦点**,不得用程序化聚焦把环「点」到待测元素上(程序化聚焦在 Chrome 下不保证匹配 `:focus-visible`)。做法:先**清空焦点**复位 —— `page.evaluate("() => document.activeElement instanceof HTMLElement && document.activeElement.blur()")`(blur 把焦点交还 `document.body`,Tab 序列随即从头开始;**这不是「聚焦某个元素」,故本计划对 `scripts/check-05-ui-uat.py` 里 `.focus()` 调用的计数为 0 这条判据仍然成立**),然后循环按 Tab(上限取 `FOCUSABLE_SELECTOR` 实例数 + 8 次余量),每按一次读 `document.activeElement` 的稳定标签,累计「被 Tab 覆盖过且当时 outline 命中环」的元素集合;循环结束后把该集合与普查集比对。**已登记的边界**:Tab 序可能不覆盖被祖先藏住的元素 —— 那正是 `visible` 过滤存在的理由,过滤后的集合必须逐个被覆盖。

    SC1 探针:`page.keyboard.press("Tab")` 后读 `document.activeElement` 的 `read_style(..., "outline-width")` 与 `"outline-color"`;期望 `"2px"` 与 `resolve_color(page, "--color-focus")`。读不到元素 ⇒ `blocked`。

    SC2 探针:先 `page.keyboard.press("Tab")` 让环出现,再 `page.click(sel)`(sel 取该样本里一个可见按钮的稳定选择器,优先 `#btn-process-round`),然后读同一元素的 `outline-color`;断言它**不等于** `resolve_color(page, "--color-focus")` —— 这直接证明「鼠标点击不出现环」,比断言 UA 基线字符串稳。同时把 `outline-style` / `outline-width` 作为 `info()` 诊断落盘,不参与判定。

    SC4 探针:复用 item 9 的 L-5 clearance 普查口径。在**侧栏滚到底**之后(`#main-pane` / `#chat-messages` 视情况 `scrollTop = scrollHeight`),对每个新 Tab 聚焦的元素,用与 `_IDI06_CENSUS_JS` 相同的「到最近裁剪祖先 padding 边的最小距离」算法算 clearance,断言 `>= CLEARANCE_MIN_PX`(4.0);空集或元素不可见时 `info()` 声明「本样本无判定」,不记 PASS。几何 `2px + offset 2px` 是本探针的**前提**,注释里点名这个绑定。

    样本选择照 item 9 的教训(单样本会把「藏住」读成「不达标」):`p1`(会话流活动态:按钮、`#message-input`、`#ai-route-select`、`#project-path-input` 可见)、`checking`(`#checks-panel` / `#check-switcher` / `#btn-continue-check` / `#btn-continue-repair` 可见)、`p3`(批注面板的 `<summary>` 可见)。三个样本各跑一遍普查与 SC1;SC2 / SC4 至少跑 `p1`。

    项末尾 `page.set_viewport_size(VIEWPORT_RESTORE)` 兜底复位(本项用 `page.click()` 可能改变滚动位置)。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 10</automated>
    <fails_when>exit != 0;或输出里出现 "未覆盖" 且计数 > 0 的 FAIL 行;或任一样本走 BLOCKED(普查无返回 / 元素读不到 / `--color-focus` 解析不出)</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8,9</automated>
    <fails_when>exit != 0,或逐项结论里出现任一项非 PASS(本计划不得让既有各项从 PASS 变红)</fails_when>
    <automated>grep -c 'FOCUSABLE_SELECTOR = "button, input, select, textarea, a\[href\], summary, \[tabindex\]"' scripts/check-05-ui-uat.py</automated>
    <fails_when>计数不为 1(枚举集与 D-05 的七选择器不同集)</fails_when>
    <automated>grep -v '^#' frontend/style.css | grep -c ':focus-visible'</automated>
    <fails_when>计数 < 7</fails_when>
  </verify>
  <done>三个样本(p1 / checking / p3)上「未被环覆盖的可聚焦元素数」均为 0;SC1(Tab 出环)/ SC2(点击不出环)/ SC4(滚到底后环不被裁切)三条探针各有明确的 PASS 或 BLOCKED,无空转 PASS;既有九项(item smoke,1,2,3,4,6,7,8,9)仍全绿。</done>
  <acceptance_criteria>
    - `grep -o 'FOCUSABLE_SELECTOR' scripts/check-05-ui-uat.py | wc -l` 输出 >= 2(定义 + 至少一处消费)
    - `grep -o '_IDI07_FOCUS_CENSUS_JS' scripts/check-05-ui-uat.py | wc -l` 输出 >= 2
    - `grep -n 'def _idi07_focus_census_assert' scripts/check-05-ui-uat.py` 有输出
    - `grep -n 'FOCUS_RING_WIDTH_PX = 2.0' scripts/check-05-ui-uat.py` 有输出,且 `grep -n 'FOCUS_RING_OFFSET_PX = 2.0' scripts/check-05-ui-uat.py` 有输出
    - `.venv/bin/python scripts/check-05-ui-uat.py --item 10` 的逐项结论行形如 `item 10: PASS  (N 条断言,0 FAIL,0 BLOCKED)`
    - `grep -o 'document.activeElement' scripts/check-05-ui-uat.py | wc -l` 输出 >= 2(Tab 驱动的焦点读数确实存在)
    - `grep -c '\.focus()' scripts/check-05-ui-uat.py` 输出 == 0(不得用程序化聚焦替代 Tab;复位走 `document.activeElement.blur()`,不引入任何 `.focus()` 调用)
    - `grep -o 'keyboard.press("Tab")' scripts/check-05-ui-uat.py | wc -l` 输出 >= 1(普查确实由 Tab 驱动 —— 这是上一条「无 `.focus()`」的正向对偶,单靠反向判据会把「干脆不驱动焦点」也放过去)
    - `grep -o 'blocked(item' scripts/check-05-ui-uat.py | wc -l` 相比改动前只增不减(前提检查只增不减)
  </acceptance_criteria>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 磁盘 `frontend/style.css` → 浏览器渲染 | 本阶段唯一改动面是声明式 CSS;级联/特异性错误会静默地让一条无障碍保证失效 |
| `scripts/check-05-ui-uat.py` → 真实 Chrome 渲染树 | 探针读数即证据;元素读不到时若退化成 PASS,门就成了空转 |
| 键盘用户 → 焦点环 | 环是键盘用户唯一的「我在哪」信号;不可见即不可用 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-07-01 | Information disclosure / Denial of service(无障碍) | `:focus-visible` 规则 vs 祖先 `opacity` | medium | mitigate | 三条 PAIR 覆盖 `--color-surface-page` / `--color-surface` / `--color-surface@0.75`;`--color-surface-sunken` 明确不进验证面并在注释里说明理由 |
| T-idi-07-02 | Tampering | 焦点规则的几何(`border` / `padding`) | medium | mitigate | 规则体只声明 `outline` 与 `outline-offset`;静态守卫断言焦点规则块内 `border` / `padding` 计数为 0;几何与 `CLEARANCE_MIN_PX = 4.0` 双向绑定 |
| T-idi-07-03 | Tampering / Denial of service | 环色的「顺手修正」(`#1f63bd` → `--radix-blue-11`) | medium | mitigate | 围栏注释逐字写明这是对 S-4 已签核契约的字面遵从;`--color-surface@0.75` 的 3.45 余量是选它的实测依据 |
| T-idi-07-04 | Spoofing(假 PASS) | `item10` 的普查探针 | high | mitigate | `data is None` ⇒ `blocked`;空集 ⇒ `info` 声明「本样本无判定」并 `return`;元素读不到 ⇒ `blocked`;三样本(p1 / checking / p3)才覆盖全部「可见的可聚焦元素」组合 |
| T-idi-07-05 | Repudiation | 归档半场的运行时断言 | medium | accept | 五个样本的 `#round-doc` 内 `a[href]` 计数为 0 ⇒ 今天无服务对象。**显式登记该事实**(不假装覆盖),由常驻算术门 + 一次性反事实探针共同承担 |
| T-idi-07-SC | Tampering | npm / pip / cargo 安装 | low | accept | 本阶段**零新增运行时依赖、零构建步骤**(硬规则 6):无任何包管理器调用进入范围,故无供应链面;若执行期出现安装需求,即为计划偏差与停止条件 |
</threat_model>

<verification>
- 执行前基线(必须先跑,建立 D-20 的对照):`bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh` 三条全 PASS;`.venv/bin/python scripts/check-02-contrast.py | tail -1` 为 `PASS: 0 failures`;`.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8,9` exit 0。
- 执行后同一条命令组必须仍全绿 —— 任一条从 PASS 变红即为本计划引入的回归。
- `.venv/bin/python scripts/check-05-ui-uat.py --item 10` exit 0 且逐项结论为 `PASS (N 条断言,0 FAIL,0 BLOCKED)`。
- `.venv/bin/python scripts/probe-07-focus-composite.py` exit 0。
- 必须使用项目 venv(`.venv/bin/python`):环境 `python3` 是 miniconda,会让无关套件假失败。
- `git status --porcelain -- frontend/app.js frontend/index.html frontend/vendor/ scripts/ui-states/` 输出为空(硬规则 5)。
</verification>

<success_criteria>
1. `:focus-visible` 规则已落地且覆盖 D-05 的七个枚举,几何为 `outline: 2px solid` + `outline-offset: 2px`,规则体不含 `border` / `padding`,也不含 `outline: none`。
2. `--color-focus: #1f63bd` 在围栏内声明一次、在围栏外被消费;围栏注释写明它是刻意字面遵从、不得被「修正」。
3. 环色对 `--color-surface-page` / `--color-surface` / `--color-surface@0.75` 三处的 `check-02` 断言全部 PASS(>= 3:1)。
4. `check-05 --item 10` 在三样本上断言「未被环覆盖的可聚焦元素数为 0」;SC1 / SC2 / SC4 各有明确结论,无空转 PASS。
5. 归档半场的运行时空缺被**显式登记**,并由一次性反事实探针提供可复跑的证据。
6. 四条既有门(check-01 / 02 / 03 / 04)与既有九项 UAT 仍全绿;`app.js` / `index.html` / `vendor/` / `ui-states/` 零改动。
</success_criteria>

<output>
Create `.planning/phases/idi-07-interaction-states-and-focus/idi-07-01-SUMMARY.md` when done
</output>
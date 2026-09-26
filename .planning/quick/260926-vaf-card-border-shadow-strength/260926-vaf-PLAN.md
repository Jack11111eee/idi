---
phase: 260926-vaf-card-border-shadow-strength
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - frontend/style.css
  - scripts/check-09-idi09-validation.py
  - scripts/probe-card-border-token.py
autonomous: true
requirements:
  - CARD-01
  - CARD-02
  - D-9-3
user_setup: []

estimate:
  tokens: 30000
  raw_tokens: 30000
  tasks: 2
  confidence: low

must_haves:
  truths:
    - "五个卡片容器(#session-panel / #annotations-panel / #checks-panel / #ai-panel / #doc-panel)在真实浏览器里计算 border-top-color == 运行时解析的 --color-border(gray-7),不再是 --color-border-subtle(gray-6)"
    - "卡片计算 box-shadow 的首层是 rgba(0, 0, 0, 0.08),且首层分量的 offset-x 仍为 0px —— 两层写法没有破坏零位移判据"
    - "另外四处 --color-border-subtle 消费者(.event-list / .annotation-item / .badge-answered / #latest-check)在浏览器里仍计算为 gray-6 —— 改动面严格是两处,不是六处"
    - "check-09 --item c1,c2 全绿(0 FAIL / 0 BLOCKED):圆角、四边 1px solid、非 none、零位移、#doc-panel-header 恒 none 等既有判据零回归"
    - "四个静态门(check-01/02/03/04)全绿:零新增令牌、零围栏外裸 hex、PAIR 清单零改动(check-02 仍 PASS: 0 failures)"
    - "探针在改动前的状态下真的报 FAIL(actual=rgb(217, 217, 217))—— 判别控制成立,证明它区分得开「改了」与「没改」"
  artifacts:
    - "frontend/style.css:335 的 --shadow-card 声明为两层值,主层 0 1px 3px rgba(0, 0, 0, 0.08)"
    - "frontend/style.css 里 border: 1px solid var(--color-border); 恰好 2 处(两条卡片规则),border: 1px solid var(--color-border-subtle); 恰好 4 处(四处非卡片)"
    - "scripts/check-09-idi09-validation.py 的 SHADOW_CARD_LITERAL 与 SHADOW_CARD_COLOR 与新的裁定值逐字一致"
    - "scripts/probe-card-border-token.py 存在,复用 check-05 设施,不写盘、不进任何 check 的调用链"
  key_links:
    - "围栏 :root 的 --shadow-card → #main-pane > section / #doc-panel 的 box-shadow → check-09 c1/c2 的 computed 读数"
    - "--color-border(gray-7)→ 两条卡片规则的 border → 探针读的 computed border-top-color"
    - "check-09 的 SHADOW_CARD_LITERAL ← --shadow-card 的声明文本(字面量精确比对,期望侧不是同一个令牌)"
    - "frontend/style.css 与 scripts/check-09-idi09-validation.py 都在 idi-09-VERIFICATION.md 的 covered_files 里 ⇒ 本次改动使该报告按内容真变 stale;闭包是重跑 /gsd-verify-work idi-09,不是重算 digest"
---

<objective>
把卡片的边框与阴影各加重一档 —— 只动四处值,不动任何别的东西。

用户 2026-09-26 的裁定(逐字):「目前只需要改2.边框与阴影强度,现在太轻了,稍微重一点。其他都不需要改。保持原样即可」。这条裁定回答的正是 Phase 9 自己刻意parked的那个设计问题:`idi-09-03-PLAN.md:301` 与 `idi-09-03-SUMMARY.md:340` 都写着「卡片边界与阴影的**强度**:……是否要更强的边界 = 设计决策,本阶段不动」。本次就是那个决策的落地。

Purpose: 卡片语言本身(白底 + 四边边界 + 圆角 + 阴影)已经建好并验证通过,缺的只是强度刻度。改动是**值级**的:阴影主层不透明度 0.04 → 0.08、blur 2px → 3px 并加一层紧贴的次层;卡片边界从 gray-6 换到 gray-7(既有令牌,深一档)。零新增令牌、零新增规则、零选择器改动、零几何改动。

Output:
- `frontend/style.css`:`--shadow-card` 改为两层值;两条卡片规则的边界令牌 gray-6 → gray-7;卡片注释块的第 ① 条改写为与代码一致
- `scripts/check-09-idi09-validation.py`:两个阴影常量重新登记到新裁定值(不动任何断言、不动任何阈值)
- `scripts/probe-card-border-token.py`:边界色的运行时探针(check-09 不读边界色,这条缝由它补)
- 两次提交:守卫(RED)一条、改动(GREEN)一条
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/STATE.md
@frontend/style.css
@scripts/check-09-idi09-validation.py
@.planning/phases/idi-09-card-containers/09-CONTEXT.md
@.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md

**规划期已实测的事实(逐条核过盘,直接采信,不要重新调查):**

1. **`--color-border-subtle` 在本文件恰好 6 处消费者,只有 2 处是卡片。** 卡片两处:`frontend/style.css:745`(在 `#main-pane > section` 规则体内)与 `:763`(在 `#doc-panel` 规则体内)。非卡片四处:`:919`(`.event-list`)、`:1275`(`.annotation-item`)、`:1326`(`.badge-answered`)、`:1485`(`#latest-check`)。**六处的行文本逐字相同(都是两空格缩进 + 同一字符串)**,故**不能**用无锚点的 `replace_all` —— 必须带上下文行锚定,否则会顺手改掉四处非卡片。
2. **令牌值(围栏内,已核):** `--color-border: var(--radix-gray-7)`(`:257`)= `#cecece` = `rgb(206, 206, 206)`;`--color-border-subtle: var(--radix-gray-6)`(`:258`)= `#d9d9d9` = `rgb(217, 217, 217)`。两者不等 ⇒ 探针有可判别的期望差。**两个令牌都已存在,本次零新增令牌。**
3. **边界色改动对对比度门零影响(已核):** `scripts/check-02-contrast.py` 的 PAIR 清单是从围栏内的 `/* PAIR ... */` 注释里正则解析的(`PAIR_RE`,文件 `:28`)。实测围栏内**没有**任何 `PAIR.*--color-border` 或 `PAIR.*--color-border-subtle` 条目(现有边界类 PAIR 只有 `--color-border-strong` ×2 / `--color-border-hover` ×3 / `--color-border-streaming` / `--color-border-success`)。故本次不改清单、不动阈值,`check-02` 仍 `PASS: 0 failures`。
4. **check-09 不读边界色(已核):** c1 对四条左栏 section 读的是 `background-color` / `border-top-left-radius` / `border-top-width` / `border-top-style` / `box-shadow`;c2 对 `#doc-panel` 读的是 `background-color` / `border-top-left-radius` / `box-shadow` / `overflow-y` / 四条 `border-{side}-width` 与 `-style`。**没有任何一条读 `border-*-color`。** 故改动 ② 不需要动 check-09 一行 —— 这也是本次要新写一个探针的原因:那条缝没有门覆盖。
5. **两层阴影不会打破零位移断言(已逐字读断言,这是本次最高风险项,结论:安全)。** `check-09` 的零位移断言在 `:164-166`,形态是 `lengths = shadow_lengths(shadow)` 后只比 `lengths[0] == "0px"`。`shadow_lengths`(`:95-103`)先按 `_SHADOW_COLOR_RE` 抹掉**所有**颜色子串再 `split()`。新值在 Chrome 的 computed 序列化是 `rgba(0, 0, 0, 0.08) 0px 1px 3px 0px, rgba(0, 0, 0, 0.04) 0px 1px 2px 0px`,抹色后首 token 仍是 `0px` ⇒ **PASS**。**文件里不存在任何「分量个数 == 4」的断言**(全文件 `lengths[` 只出现在 `:166`),故 `:96-101` 的 docstring 里「剩下的就是 `[offset-x, offset-y, blur, spread]`」这句话在两层值下不再成立 —— 见下方「两处必须一并处理的散文」。
6. **`--shadow-card` 的消费者恰好 2 个**(`frontend/style.css:747` 与 `:766`),零外溢。
7. **围栏边界:** `frontend/style.css:5` 是 `===== DESIGN TOKENS: START`,`:687` 是 `END`。`--shadow-card`(`:335`)在围栏内;卡片规则与注释块(728-770)在围栏外 ⇒ 注释里**不得**出现裸 `#hex`(check-01 的 `#[0-9a-fA-F]{3,6}` 扫描)也不得出现 `var(--radix-...)`(check-01 的 tier-1 原语扫描)。用令牌名散文指代即可(如「gray-7」)。
8. **门的作用域:** `check-01` / `check-03` / `check-04` 与 `check-02` **只读 `frontend/style.css`**(check-03 数 `.hidden {`、check-04 数 `!important;`)。故在 `scripts/` 下新增一个探针文件不影响这四条门中的任何一条;也没有任何门或计划断言「`scripts/` 下恰好 N 个文件」。
9. **唯一 live 报告:** `.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md` 是仓库里唯一一份 VERIFICATION,其 `covered_files` 含 `frontend/style.css` 与 `scripts/check-09-idi09-validation.py`。该报告第 10 行 must-have 逐字钉着旧值(`--shadow-card` = `0 1px 2px rgba(0, 0, 0, 0.04)`),第 157 行记着「边界取既有 `--color-border-subtle`(#d9d9d9)、阴影 `rgba(0,0,0,0.04)`」。**本次改动使这两条陈述按内容真变失真** —— 处置见 Task 2 的登记要求。

**两处必须一并处理的散文(否则注释/文档与代码互相矛盾,本仓库明令禁止):**

- **`frontend/style.css:731-733` 的第 ① 条**现在写着「边界色取 `--color-border-subtle`……**不得顺手换成别的令牌**,也不得为卡片新声明一个边界令牌」。这条自我约束已被用户的裁定**推翻**,留着它就变成一条「代码违反了注释里的禁令」的记录。
- **`scripts/check-09-idi09-validation.py:96-101` 的 `shadow_lengths` docstring** 举的例子是 `rgba(0, 0, 0, 0.04) 0px 1px 2px 0px` 并断言「剩下的就是 `[offset-x, offset-y, blur, spread]`」。新值是两层,这两个陈述都不再成立(见事实 5)。

**不得触碰(硬规则):**

- **另外四处 `--color-border-subtle` 消费者一字不动**(`:919` / `:1275` / `:1326` / `:1485`)。它们不是卡片 —— 用户裁定是「卡片边框与阴影加重一档」,不是「全站边界加深」。
- **`#doc-panel` 的注释块(`:750-757`)不动。** 它写的「同底色令牌 / 同边界令牌 / 同圆角令牌 / 同阴影令牌(CARD-02)」在改动后**仍然为真**(两栏仍取同一组令牌),不需要改。
- **卡片规则体的第 ② / ③ 条注释(`:734-740`)不动。** 禁止属性清单与「零位移」两条与本次改动无关。
- `scripts/check-05-ui-uat.py` / `check-06` / `check-07` / `probe-05` / `probe-07` / `frontend/app.js` / `frontend/index.html` / `frontend/vendor/` **零改动**。
- **`check-09` 里除两个常量与那段 docstring 外一行不改**:不放宽任何断言、不改任何阈值、不改断言标签文本、不加容差。
- 零新增依赖、零构建步骤、零新增令牌、零新增 CSS 规则、零选择器改动。
- **不要为本 quick 跑 `phase.complete` / `advance-plan`**(本项目实测过:这两个动词会翻掉不归它管的需求、并改写被覆盖文件把刚过的门自己打破)。idi-09 已收口,本次只是值级修正。

**偏离说明(两处,已显式登记,不是静默扩权):**

1. **本次多产出一个文件 `scripts/probe-card-border-token.py`。** 理由:编排侧明令「验证必须包含真实浏览器运行时读数(computed `box-shadow` / `border-top-color`)」,而事实 4 证明 `border-top-color` 这条缝**没有任何既有门覆盖**。仓库对此有现成先例 —— `scripts/probe-menu-modal-reachability.py` 就是同形的一次性探针(其文件头自述「用后即弃,不进 check-07」)。**被否决的替代方案:** 往 `check-09` 的 c1 里加一条边界色断言。否决理由:那是改门语义(本仓库把门改动当高代价事件,上一阶段以「零处门改动」为交付亮点),而本次的裁定是纯值级修正。
2. **`check-09` 的 `shadow_lengths` docstring 一并修正一句话。** 理由:它现在描述的东西在新值下是错的(事实 5),而本仓库明令禁止注释与代码互相矛盾。**边界:** 只改那段 docstring 的示例与「4 个分量」措辞,**不重构函数、不改断言、不加分量个数检查**。
</context>

<tasks>

<task type="auto">
  <name>Task 1: 先把边界色的运行时守卫写出来,并看它红</name>
  <files>scripts/probe-card-border-token.py</files>
  <action>
新建 `scripts/probe-card-border-token.py`,一次性探针(不是门)。**照 `scripts/probe-menu-modal-reachability.py` 的形状写**,复用 check-05 的设施,不要自己另起 harness:

- 用 `importlib.util.spec_from_file_location("check05_ui_uat", ROOT / "scripts" / "check-05-ui-uat.py")` 加载 check-05,取 `c05.ensure_server` / `c05.make_fixture` / `c05.enter_project` / `c05.read_style` / `c05.resolve_color` / `c05.norm`。
- `main()`:`server = c05.ensure_server()` → `tmp_root = Path(tempfile.mkdtemp(prefix="probe-card-border-"))` → `pw.chromium.launch(headless=True)` + `new_context(viewport={"width": 1440, "height": 900})` + `page.set_default_timeout(20000)` → `proj = c05.make_fixture("p1", tmp_root)` → `c05.enter_project(page, proj)` → `page.wait_for_timeout(400)`。`finally` 里关浏览器、`server` 非 None 时 terminate。
- **为什么走 p1 且不加 `--browser`:** p1 是 check-09 c1/c2 用的同一样本(四个左栏 section 与 `#doc-panel` 都在);浏览器固定走 Playwright 自带 chromium + 无头,与 check-09 同款(本机 `channel="chrome"` + headless 会 CDP 挂死,是既有实测结论)。

**断言的形态(四条,顺序即执行序;每条都要有可判别的失败方向):**

① **令牌解析 + 可区分性(防恒真)。** 读 `border = c05.resolve_color(page, "--color-border")` 与 `subtle = c05.resolve_color(page, "--color-border-subtle")`。
   - `INFO 令牌解析: --color-border=<border> --color-border-subtle=<subtle>`
   - `PASS 令牌可区分: --color-border != --color-border-subtle` / 失败时 `FAIL 令牌可区分: --color-border == --color-border-subtle(两侧相等 ⇒ 下一条判据恒真)`。**没有这一条,②③ 两条会在「两个令牌恰好取同一个值」时静默恒绿。**

② **卡片边界(主判据)。** 对 `["#session-panel", "#annotations-panel", "#checks-panel", "#ai-panel", "#doc-panel"]` 逐个读 `c05.read_style(page, sel, "border-top-color")`,与 `border` 比(`c05.norm` 两侧都过一遍再比)。
   - 通过:`PASS 卡片边界 <sel>: expected=<border> actual=<actual>`
   - 失败:`FAIL 卡片边界 <sel>: expected=<border> actual=<actual>`
   - **元素取不到(读数 None)记 `FAIL 卡片边界 <sel>: 元素不存在`,并让脚本以 exit=2 结束** —— 前提不成立时必须报出来,绝不静默跳过。

③ **非卡片对照(证明改动面严格是两处)。** 对 `[".event-list", "#latest-check", ".annotation-item", ".badge-answered"]` 逐个读 `border-top-color`,期望是 `subtle`。
   - 通过/失败:`PASS|FAIL 非卡片边界对照 <sel>: expected=<subtle> actual=<actual>`
   - **元素在 p1 样本里不存在时记 `INFO 非卡片边界对照 <sel>: p1 样本里不存在 —— 不计入`(既不算 PASS 也不算 FAIL)。** 但要求**至少 2 个对照元素存在**;少于 2 个即 `FAIL 非卡片边界对照: p1 样本里只有 N 个可读,对照不足以证明改动面`,exit=2。**不得因为「取不到」就把对照删掉。**
   - 为什么期望侧取自 `subtle` 而不是写死 rgb:与 check-09 的 c1/c2 同口径 —— 期望侧是运行时解析值,不是硬编码;而令牌可区分性由 ① 单独守住。

④ **结果行:** 全部通过打 `PROBE RESULT: PASS(exit=0)` 并 `sys.exit(0)`;有任何 FAIL 打 `PROBE RESULT: FAIL(exit=1)` 并 `sys.exit(1)`;前提不成立打 `PROBE RESULT: BLOCKED(exit=2)` 并 `sys.exit(2)`。

**文件头 docstring 必须写明:** 这是一次性探针、不是门、不进任何 check 的调用链、不被 CI 调用;它存在的唯一理由是本仓库既有的六条门里**没有一条读卡片容器的 `border-*-color`**(check-09 读的是 width / style / radius / background / box-shadow);以及**判别控制就是改动前的状态本身** —— 改动前五条卡片规则的 `border-top-color` 实测是 `rgb(217, 217, 217)`(= subtle),正是本探针的失败方向,故 RED 输出即是「它区分得开」的实证。

**运行并留证(RED):**
```
cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python scripts/probe-card-border-token.py > /tmp/vaf-probe-red.txt 2>&1; echo "exit=$?"; grep -c 'FAIL 卡片边界' /tmp/vaf-probe-red.txt; grep -c 'FAIL 非卡片边界对照' /tmp/vaf-probe-red.txt; grep -c 'INFO 令牌解析' /tmp/vaf-probe-red.txt
```
**预期 `exit=1`、`FAIL 卡片边界` 计数 5、`FAIL 非卡片边界对照` 计数 0、`INFO 令牌解析` 计数 1,且那 5 行的 `actual=rgb(217, 217, 217)`。** 这就是本任务要的证据,不是失败 —— 它证明这条守卫真的能区分「改了」与「没改」。**若 RED 阶段 exit=0,说明守卫是废的(恒绿):停下修探针,不得继续。** 另:`INFO 非卡片边界对照 …不存在` 的行数一并抄进 SUMMARY(它是「对照读到了几个」的原始记录)。

提交:`test(260926-vaf): add a failing runtime guard for the card border token`
  </action>
  <verify>
    <automated>cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python scripts/probe-card-border-token.py > /tmp/vaf-probe-red.txt 2>&1; echo "exit=$?"; grep -c 'FAIL 卡片边界' /tmp/vaf-probe-red.txt; grep -c 'actual=rgb(217, 217, 217)' /tmp/vaf-probe-red.txt; grep -c 'PASS 令牌可区分' /tmp/vaf-probe-red.txt</automated>
  </verify>
  <done>scripts/probe-card-border-token.py 存在、语法通过、复用 check-05 设施且不写盘;`/tmp/vaf-probe-red.txt` 里 `exit=1`、`FAIL 卡片边界` 恰好 5 行且每行 `actual=rgb(217, 217, 217)`、`PASS 令牌可区分` 恰好 1 行、`FAIL 非卡片边界对照` 0 行;RED 输出留证并在 SUMMARY 里登记对照元素的命中数(含 INFO 不存在行)。</done>
</task>

<task type="auto">
  <name>Task 2: 四处值改动落地(阴影 + 两条卡片边界 + 常量)并全绿</name>
  <files>frontend/style.css, scripts/check-09-idi09-validation.py</files>
  <action>
**① `frontend/style.css:335` 的 `--shadow-card`(围栏内)。** 逐字把整行替换为:

    第 335 行原文:`  --shadow-card: 0 1px 2px rgba(0, 0, 0, 0.04);`
    第 335 行新文:`  --shadow-card: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04);`

(主层不透明度 `0.04 → 0.08`、blur `2px → 3px`,并加一层紧贴的次层;**x 偏移保持 `0`** —— 零位移是 check-09 的硬判据。行内只此一处声明,围栏内零新增令牌。)

**② `frontend/style.css` 的两条卡片规则边界(只这两处)。** 把 `border: 1px solid var(--color-border-subtle);` 改为 `border: 1px solid var(--color-border);`:

- 第 745 行(在 `#main-pane > section` 规则体内)—— 用带上下文的锚点定位,例如锚 `  background: var(--color-surface-card);\n  border: 1px solid var(--color-border-subtle);\n  border-radius: var(--radius-md);` 这一段在文件内唯一。
- 第 763 行(在 `#doc-panel` 规则体内)—— 用锚 `  overflow-y: auto;\n  border: 1px solid var(--color-border-subtle);\n  background: var(--color-surface-card);` 定位,该组合在文件内唯一。

**六处的行文本逐字相同**,故**绝对不要**用无锚点的整串替换 / `replace_all` / 全局正则 —— 那会顺手改掉 `:919` / `:1275` / `:1326` / `:1485` 四处非卡片(用户明令「其他都不需要改,保持原样即可」)。改完必须逐行核盘(见 verify)。

**③ `frontend/style.css:731-733` 的注释第 ① 条改写为与代码一致。** 现在是「边界色取 `--color-border-subtle`:它已经是 #doc-panel 与 .event-list 的容器边界色,即本文件既有的容器边界语言 ⇒ 零新增令牌。不得顺手换成别的令牌,也不得为卡片新声明一个边界令牌。」

改写成**描述现实**的版本,必须落到三点:(a) 两条卡片规则的边界色取 `--color-border`(gray-7),比 `--color-border-subtle`(gray-6)深一档;(b) 依据是用户 2026-09-26 的裁定「边框与阴影加重一档」,即 Phase 9 自己 parked 的强度决策的落地;(c) 仍然是**零新增令牌**(取的是既有令牌),且 `--color-border-subtle` 仍是 `.event-list` / `.annotation-item` / `.badge-answered` / `#latest-check` 四处的边界色 —— 那四处不是卡片,本次不动。**把原来那句「不得顺手换成别的令牌」删掉**:它已经被用户的裁定推翻,留着就是注释与代码互相矛盾。

**这条注释的硬约束(否则 check-01 会红):** 注释块在围栏**外**,故**不得出现裸 `#hex`**(连 `#cecece` / `#d9d9d9` 都不行),也**不得出现 `var(--radix-...)`**(tier-1 原语名不得外泄)。用散文写「gray-7」「gray-6」即可。**第 ② / ③ 条(`:734-740`)与 `#doc-panel` 的注释块(`:750-757`)一字不动** —— 后者的「同边界令牌」在改动后仍为真。

**④ `scripts/check-09-idi09-validation.py:88-89` 的两个常量重新登记到新裁定值。**

    原文:`SHADOW_CARD_LITERAL = "0 1px 2px rgba(0, 0, 0, 0.04)"`
    新文:`SHADOW_CARD_LITERAL = "0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04)"`
    原文:`SHADOW_CARD_COLOR = "rgba(0, 0, 0, 0.04)"`
    新文:`SHADOW_CARD_COLOR = "rgba(0, 0, 0, 0.08)"`

`SHADOW_CARD_COLOR` 取**主层**颜色(0.08)而非次层(0.04):两条断言(`:161-163` 的「非 none 且含卡片阴影」、`:214-216` 的同一形态)都在 computed 值上做子串比对,取主层能让「主层确实加深了」这件事被断言到,而不是被次层的旧色蒙过去。

**这是对用户刻意改动的那个事实的重新登记,不是放宽:** 不放宽、不删除任何断言,不改任何阈值,不改断言标签文本(`c1 [令牌] --shadow-card == 用户裁定值(D-9-3)` 保留原样)。

**⑤ 同文件 `:96-101` 的 `shadow_lengths` docstring 一并修正**(见 context 偏离说明 2)。现在是「Chrome 的 computed 序列化把颜色写在最前(如 `rgba(0, 0, 0, 0.04) 0px 1px 2px 0px`),故去掉颜色子串后剩下的就是 `[offset-x, offset-y, blur, spread]`」。新值是**两层**,该示例与「4 个分量」的说法都不再成立。改写成:Chrome 把**每层**的颜色写在层内最前,抹掉颜色子串后各层的 `[offset-x, offset-y, blur, spread]` 按层序拼接;本函数只被用来读**首层**的 offset-x(零位移判据),故多层值下 `lengths[0]` 仍是首层的 offset-x。**只改这段 docstring 的措辞,不重构函数、不改断言、不加分量个数检查。**

**运行并留证(GREEN):**
```
cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python scripts/probe-card-border-token.py > /tmp/vaf-probe-green.txt 2>&1; echo "probe_exit=$?"; grep -c 'PASS 卡片边界' /tmp/vaf-probe-green.txt; grep -c 'FAIL' /tmp/vaf-probe-green.txt; .venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2 > /tmp/vaf-c09.txt 2>&1; echo "c09_exit=$?"; grep -c 'FAIL' /tmp/vaf-c09.txt; grep -c 'BLOCKED' /tmp/vaf-c09.txt
```
预期:probe `exit=0`、`PASS 卡片边界` 5 行、`FAIL` 0 行;`check-09 --item c1,c2` `exit=0`、`FAIL` 0、`BLOCKED` 0。

**先取一次 RED 证据再改常量(证明那条字面量断言不是恒绿):** 在只改完 ①②③、**还没动常量**时跑一次
```
.venv/bin/python scripts/check-09-idi09-validation.py --item c1 > /tmp/vaf-c09-red.txt 2>&1; echo "exit=$?"; grep -c 'FAIL c1 \[令牌\] --shadow-card' /tmp/vaf-c09-red.txt
```
预期 `exit=1` 且该 FAIL 计数 1(期望侧旧字面量、实际侧新值)—— 这就是「期望侧是字面量、不是同一个令牌」这条设计的实证。**这一步是留证,不是失败**;改完常量后必须回到全绿。

**若 `c1 [令牌] --shadow-card` 在改完常量后仍 FAIL 且差异只在空白**(例如 Chrome 把逗号后的空格序列化成别的形态):**先读 `/tmp/vaf-c09.txt` 里 `INFO c1 令牌解析` 打印的实际串,再把 `SHADOW_CARD_LITERAL` 逐字对齐到那个实际串** —— 仍然是精确等值比对,仍然不接受子串匹配 / 正则 / 归一化。**不得把该断言改成包含关系来「让它过」。**

提交:`fix(260926-vaf): strengthen card border and shadow one step, re-register the pinned value`
  </action>
  <verify>
    <automated>cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && .venv/bin/python scripts/probe-card-border-token.py > /tmp/vaf-probe-green.txt 2>&1; echo "probe_exit=$?"; grep -c 'PASS 卡片边界' /tmp/vaf-probe-green.txt; grep -c 'FAIL' /tmp/vaf-probe-green.txt; .venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2 > /tmp/vaf-c09.txt 2>&1; echo "c09_exit=$?"; grep -c 'FAIL' /tmp/vaf-c09.txt; grep -c 'BLOCKED' /tmp/vaf-c09.txt; grep -c 'border: 1px solid var(--color-border);' frontend/style.css; grep -c 'border: 1px solid var(--color-border-subtle);' frontend/style.css</automated>
  </verify>
  <done>probe `exit=0` 且 `PASS 卡片边界` 5 行、`FAIL` 0 行;`check-09 --item c1,c2` `exit=0`、`FAIL` 0、`BLOCKED` 0;`border: 1px solid var(--color-border);` 计数 == 2 且 `border: 1px solid var(--color-border-subtle);` 计数 == 4(六处总数不变);`--shadow-card` 单行两层、首层 `0 1px 3px rgba(0, 0, 0, 0.08)`;注释第 ① 条已改写且注释内无裸 hex 与 `var(--radix-`;两个常量与 docstring 已更新;`/tmp/vaf-c09-red.txt` 的 RED 证据已留证。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 无新增边界 | 本次是四个 CSS 值的改动 + 一个只读本地探针 + 两个常量的重新登记。不新增输入解析面、不新增端点、不新增依赖、不新增 DOM 属性写入、不新增令牌、不新增选择器 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-vaf-01 | Tampering | `frontend/style.css` 的两处边界改动会落到错误的消费者上(六处行文本逐字相同) | medium | mitigate | 用带上下文行的锚点定位,改完以两个 grep 计数核盘(`--color-border` == 2 / `--color-border-subtle` == 4);探针的非卡片对照在浏览器侧再证一次四处未动 |
| T-vaf-02 | Tampering | `check-09` 的常量「重新登记」被当成放宽断言的借口 | medium | mitigate | 只改两个常量的字面量 + 一段 docstring 措辞;断言、阈值、标签一字不动;RED 证据(`/tmp/vaf-c09-red.txt`)证明该字面量断言在改动后、常量未更新时真的红 |
| T-vaf-03 | Repudiation | 两层阴影静默打破零位移判据而无人察觉 | low | accept | 已逐字读断言(`:164-166` 只比 `lengths[0]`,全文件无分量个数断言);探针与 check-09 双读数在 `must_haves` 里各占一条 |
| T-vaf-04 | Information Disclosure | 测试产物 `/tmp/vaf-probe-red.txt` / `/tmp/vaf-c09-red.txt` / `/tmp/vaf-probe-green.txt` / `/tmp/vaf-c09.txt` | low | accept | 只含本地 fixture 路径与计算样式读数,无凭据;探针在 `finally` 内关浏览器,不落盘到仓库 |
| T-vaf-SC | Tampering | 依赖安装(npm/pip/cargo) | high | mitigate | **本计划零新增依赖、零构建步骤**;若执行中冒出任何安装动作,即为偏离,须停下并上报 |
</threat_model>

<verification>
全部命令在 `/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration` 下用**项目 venv**(`.venv/bin/python`)跑 —— 环境 `python3` 是 miniconda,会让 4 个 `ai_caller` 测试假失败。本机是 darwin,**没有 `timeout` 命令**,不要用。

1. **主判据 ①(边界色,真实浏览器):** `.venv/bin/python scripts/probe-card-border-token.py` → `exit=0`,`PASS 卡片边界` 恰好 5 行(四个左栏 section + `#doc-panel`),`FAIL` 0 行,`PASS 令牌可区分` 1 行。**读数对象必须是 `getComputedStyle(el)['border-top-color']`** —— 「源码里写着 `var(--color-border)`」不构成证据(那正是本仓库反复付过代价的那类假绿)。
2. **主判据 ②(阴影 + 零位移,真实浏览器):** `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2` → `exit=0`,`FAIL` 0,`BLOCKED` 0;其中 `INFO c1 令牌解析` 行的 `--shadow-card` 值等于新字面量,`c1 [令牌] --shadow-card == 用户裁定值(D-9-3)` 与每条卡片的「非 none 且含卡片阴影」「水平偏移为 0px」全 PASS。
3. **RED 留证(证明两条守卫都不是恒绿):** `/tmp/vaf-probe-red.txt` 里 `FAIL 卡片边界` 5 行且 `actual=rgb(217, 217, 217)`;`/tmp/vaf-c09-red.txt` 里 `FAIL c1 [令牌] --shadow-card` 1 行(常量未更新、CSS 已改的中间态)。
4. **零回归 —— 浏览器门:** `.venv/bin/python scripts/check-05-ui-uat.py --item 1,2,3,4,6,7,8,9,10 --browser bundled`(或既有全量口径)零新增 FAIL;`.venv/bin/python scripts/check-06-idi05-validation.py` 与 `.venv/bin/python scripts/check-07-idi08-validation.py` 各自 `exit=0`。**重点看 check-05/06 的 `.panel-header` 竖条与 `#doc-panel-header` 恒 `none` 那几条** —— 阴影属于卡片容器,不该漏到表头上。
5. **零回归 —— 静态门:** `bash scripts/check-01-token-conformance.sh` → `PASS`;`.venv/bin/python scripts/check-02-contrast.py` → `PASS: 0 failures`;`bash scripts/check-03-hidden-uniqueness.sh` → `PASS`;`bash scripts/check-04-important-count.sh` → `PASS`。check-01 是注释改写的直接守卫(围栏外裸 hex / tier-1 原语名)。
6. **零回归 —— 单测基线:** `.venv/bin/python -m pytest -q` → `219 passed, 6 skipped`(改动面不含后端,此条是「没碰坏别处」的兜底)。
7. **改动面守卫(外科手术式改动):** `git diff --name-only` 只列出 `frontend/style.css`、`scripts/check-09-idi09-validation.py`、`scripts/probe-card-border-token.py`(外加本 quick 目录下的 PLAN/SUMMARY);`git status --porcelain -- frontend/app.js frontend/index.html frontend/vendor/ scripts/check-05-ui-uat.py scripts/check-06-idi05-validation.py scripts/check-07-idi08-validation.py scripts/probe-05-resolve-color.py scripts/probe-07-focus-composite.py scripts/check-01-token-conformance.sh scripts/check-02-contrast.py scripts/check-03-hidden-uniqueness.sh scripts/check-04-important-count.sh` 输出为空。
8. **`check-09` 的改动面复核:** `git diff --numstat -- scripts/check-09-idi09-validation.py` 显示的增删行数应与「2 个常量 + 1 段 docstring」相称(个位数);`grep -c 'FAIL\|assert' scripts/check-09-idi09-validation.py` 不因本次而减少 —— 断言一条都没删。
9. **可选的视觉留证(不参与判据):** `.venv/bin/python scripts/check-09-idi09-validation.py --screenshot .planning/quick/260926-vaf-card-border-shadow-strength/screenshots` 出图,供用户用眼睛裁「稍微重一点」是否到位。**它不计入本计划的 pass/fail**;若出图失败,登记事实即可,不影响交付判定。
10. **SUMMARY 里的两条登记(必须逐条写,这是本次的实质产出之一):**
    - **裁定值变更的溯源:** 用户 2026-09-26 把 D-9-3 的阴影值从 `0 1px 2px rgba(0, 0, 0, 0.04)` 改为两层值,并把卡片边界从 `--color-border-subtle`(gray-6)改到 `--color-border`(gray-7)。这回答了 Phase 9 自己 parked 的问题(`idi-09-03-PLAN.md:301` / `idi-09-03-SUMMARY.md:340` 逐字记着「是否要更强的边界 = 设计决策,本阶段不动」)。
    - **指纹义务与正确闭包:** `frontend/style.css` 与 `scripts/check-09-idi09-validation.py` 都在 **`idi-09-VERIFICATION.md`** 的 `covered_files` 里 ⇒ 该报告按**内容真变**判 stale。**正确闭包 = 重跑 `/gsd-verify-work idi-09`,不是重算 digest**(重算会断言「自验证以来无变化」,而两个文件确实变了)。同时登记:该报告第 10 行 must-have 与第 157 行设计说明**逐字钉着旧值**,故重验证时会读到这两条与新裁定值的差异 —— 那是**用户的裁定**,不是回归,重验证必须按新裁定值记录。**不要改写 `idi-09-01/02/03-PLAN.md` / `*-SUMMARY.md` / `idi-09-VERIFICATION.md`** —— 它们是「当时验证了什么」的历史记录,改写会让记录失真;登记写在本 quick 的 SUMMARY 里。**不要用 `gsd-tools query verification status <phase>` 判定 stale**(这些相位目录一律返回 `missing`)。
</verification>

<success_criteria>
- 五个卡片容器在真实浏览器里计算 `border-top-color` == `--color-border`(gray-7);四处非卡片消费者仍计算为 `--color-border-subtle`(gray-6) —— 改动面严格是两处。
- 卡片计算 `box-shadow` 的首层是 `rgba(0, 0, 0, 0.08)`,首层 offset-x 仍为 `0px`;`check-09 --item c1,c2` 全绿(0 FAIL / 0 BLOCKED)。
- 两个守卫在改动前**真的红**(探针 `actual=rgb(217, 217, 217)` 5 行;check-09 字面量断言 1 行),改动后真的绿。
- 四个静态门全绿(`check-02` 仍 `PASS: 0 failures`),五条浏览器门零新增 FAIL,pytest 仍 `219 passed, 6 skipped`。
- 零新增令牌、零新增 CSS 规则、零选择器改动、零依赖、零构建步骤;`check-09` 的断言一条未删、阈值一个未动。
- 注释块第 ① 条与 `shadow_lengths` 的 docstring 已与代码一致,且注释内无裸 hex、无 `var(--radix-`。
- 改动面严格限于三个文件;`app.js` / `index.html` / `vendor/` / `check-05` / `check-06` / `check-07` / `probe-05` / `probe-07` / `check-01…04` 零改动。
- SUMMARY 内两条登记(裁定值变更溯源、`idi-09-VERIFICATION.md` 因内容真变 stale 且正确闭包是重跑 verify-work)逐条写明。
</success_criteria>

<output>
Create `.planning/quick/260926-vaf-card-border-shadow-strength/260926-vaf-SUMMARY.md` when done
</output>

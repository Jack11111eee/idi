---
phase: idi-11-decard-and-hairline-dividers
plan: 03
type: execute
wave: 3
depends_on:
  - idi-11-01
  - idi-11-02
files_modified:
  - scripts/check-09-idi09-validation.py
autonomous: true
requirements:
  - REG-01

estimate:
  tokens: 75000
  raw_tokens: 75000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- 改写为断言新契约(不是删除、不是放宽、不是恒真) ----
    - "`check-09` 的 `c1` / `c2` / `c3` / `c4` **已改写为断言新契约**:连续面(五容器无边界)+ 统一面(面板与页面同色、内陷面仍更暗)+ 灰缝归零 + 两条发丝线。**零条断言被删除、零条降级为恒真**;`ITEMS` 仍是 `{\"c1\", \"c2\", \"c3\", \"c4\", \"c5\"}` 五项(`c5` 的滚动契约原样保留)"
    - "改写后的 `c1..c4` 断言总数 **>= 46**(HEAD 实测基线:`c1` 26 + `c2` 13 + `c3` 3 + `c4` 4 = **46**;该基线在规划期已用 `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4` 复现,`exit=0`)。**「>= 46」是本条判据的机器形态**,不是「我尽量不少写」"
    - "判据是**真实浏览器的 `getComputedStyle` 计算读数**;令牌解析降为 `info()` 诊断(D-11-12)。**这不是风格偏好** —— `ok()` 在**期望侧为 `None` 时降级成 `BLOCKED`(exit 2,本项目当良性码)**,令牌一旦被删,旧式「断言解析值」不会变红,而是静默变成「良性阻塞」。故**每一处令牌解析断言都走 `ok_true` 并显式处理 `None`**(C-4)"
    - "`c1` 断言四个 section 的计算 `box-shadow == \"none\"`、四个 `border-*-radius` 长手均 `== \"0px\"`、计算底色 == 统一面;`c2` 断言 `#doc-panel` 计算 `box-shadow == \"none\"`、四角半径 `0px`、**仅** `border-left-width == \"1px\"`、`overflow-y == \"auto\"`、`#doc-panel-header` 的 sticky 与背景仍成立;`c3` 断言两级刻度(统一面 == body 计算底色,**且**内陷面解析值亮度严格更低);`c4` 断言 `#main-pane` 计算 `gap == \"0px\"`、两条发丝线的计算宽度 `1px` 与颜色、`.panel-body` 计算 `padding == \"16px\"`、竖线宿主几何跨满"
    # ---- 异形与排除(两条最容易写错的地方) ----
    - "`c1` 的边界宽度判据是**异形的**,不是一条统一循环(C-6):`#session-panel` 是 DOM 第一个 `section`,`section + section` 永不匹配它 ⇒ 其四条 `border-*-width` **全部**为 `0px`;`#annotations-panel` / `#checks-panel` / `#ai-panel` 各自恰 `border-top-width == \"1px\"`、其余三条边 `0px`。样本 `p1` 下 `#annotations-panel` / `#checks-panel` 带 `.hidden`,但计算样式对 `display: none` 的元素同样返回解析值 ⇒ 单样本可读全四者"
    - "**`.panel-header` 不在 `c1` 的判定集与对照组里**(C-7):它合法地携带 `box-shadow: inset 3px 0 0 var(--color-marker-active)`(活动面板标记,`#session-panel:not(.hidden) .panel-header` 等三条选择器),那是去卡片后**仅存的活动态视觉线索**。任何「所有面板后代 `box-shadow === none`」的写法都会把它误判为缺陷。`c1` 反而**正面断言**该标记存活:`#session-panel .panel-header`(p1 下未隐藏)的计算 `box-shadow` 非 `none` 且含 `inset` 与 `3px 0px`"
    - "**交互控件对照组在同一份运行时读数里给出**(SC1 明文要求,否则「移除边界」可能是把整站边界一起抹掉):`button` / `#project-path-input` / `#check-switcher` / `#ai-route-select` / `.overlay-card` 各自的 `border-top-left-radius` 非 `0px` 且 `border-top-width` 非 `0px`;`.overlay-card` 另断言 `box-shadow` 非 `none`。五个选择器在 `frontend/index.html` 里都存在(`#ai-route-select` 是 `select` 族里**有显式声明**的那一个,故判据是确定的、不依赖 UA 默认样式)"
    # ---- 双断言(发丝线颜色) ----
    - "两条发丝线的颜色都带**双断言**:既等于运行时解析的 `--color-border-subtle`,又等于写死的字面量 `rgb(217, 217, 217)`(gray-6)。**字面量半条是承重的**(C-5):只跟令牌比是**自指的** —— 把该令牌换成 `--color-border`(gray-7)会让两侧一起变、恒过,而那正是 D-11-8 显式否决的备选。该形态照抄 `scripts/check-10-idi10-validation.py` 的 `TH_BORDER_LITERAL` 与其双断言(`:377-383`)"
    # ---- 两条专用残留断言(不是 G2) ----
    - "`check-09` 新增了 **`fence_text()`**(逐字照抄 `scripts/check-10-idi10-validation.py:184-189` —— `check-09` 原先没有它)与**两条专用**残留断言,判据是 `fenced.count(<令牌名>) == 0`。**这不是 G2**:G2 是「补一条**通用的**围栏消费断言 + 处置零消费的 `--radix-gray-1`」,已由用户明确排除在 v1.16 范围外;本阶段只处置**本次反转自己孤立掉的**两个令牌,照 Phase 10 删那个 28px 圆角档位时给它加一条专用残留断言的先例"
    - "残留断言的机制是**子串计数、扫围栏全文含注释**(标签若写「声明残留计数」会误导 —— 计划与 SUMMARY 都要写明它**含注释**)。配套的「被删令牌已不可解析」探测器走 `ok_true`(`resolve_token(...) is None`),因为 `ok()` 会把 `None` 降级成 BLOCKED(C-4)"
    # ---- 变异证明(唯一能证明守卫真的会失败的手段) ----
    - "**六条变异测试**逐条给出「变异 → FAIL」的**真实读数**(不得只声明做过),每条在**已提交的树上**做、用定向 `git checkout -- frontend/style.css` 还原,还原后 `git diff --exit-code -- frontend/style.css` 为空(**逐字节相同**)。**禁用 `git stash`** —— 它跨工作树共享,本项目明令禁止。六条:① 给 `#main-pane > section` 加回 `border` / `box-shadow` ⇒ `c1` 必红;② 给 `#doc-panel` 加回四边边界 ⇒ `c2` 必红;③ 删掉 `#doc-panel` 的 `overflow-y: auto` ⇒ `c2` 必红;④ 把统一面改回内陷面使两档塌成一档 ⇒ `c3` 必红;⑤ 把 `gap` 改回 12px ⇒ `c4` 必红;⑥ 删掉横线规则 ⇒ `c4` 必红"
    - "`c5` 的滚动契约在改动后复跑并确认仍成立(`#doc-panel` / `#chat-messages` 的 `overflow-y == auto`、`#doc-panel-header` 的 `position: sticky` 与 `top: 0px`、可滚前提下滚到底表头仍在面板可视带内)"
    - "`main()` 的退出码语义与 `--item` / `--screenshot` / `--keep` 三个 CLI 参数**逐字保留**(`0=全 pass / 1=有 FAIL / 2=有 BLOCKED`);`--screenshot DIR` 路径一字未动(Phase 12 的 VIS-01 要复用既有路径,**不新建 harness**)"
    - "`scripts/check-05-ui-uat.py` / `scripts/check-02-contrast.py` / `scripts/check-10-idi10-validation.py` / `scripts/check-01…04` / `scripts/check-06` / `scripts/check-07` / `scripts/probe-*` 本计划零改动;`frontend/style.css` 本计划**零改动**(它已在波次 1/2 定型)"

  artifacts:
    - path: "scripts/check-09-idi09-validation.py"
      provides: "Phase 9 卡片语言的运行时门,改写为断言 Phase 11 的新契约:连续面 + 统一面 + 灰缝归零 + 两条发丝线;新增 `fence_text()` 与两条专用残留断言;新增交互控件对照组与活动标记的正面断言;全部令牌断言改走 `ok_true` 并显式处理 None"
      contains: "def fence_text()"

  key_links:
    - from: "`scripts/check-09-idi09-validation.py` 的 `c1..c4`"
      to: "`frontend/style.css` 的五个容器规则与两条发丝线在真实浏览器里的 computed style"
      via: "Playwright `getComputedStyle` 读数 —— 容器边界是**画出来**的,文本里写着 `border: none` 不等于它真的生效"
      pattern: "read_style\\(page, sel, \"box-shadow\"\\)"
    - from: "`check-09` 的两条专用残留断言"
      to: "`frontend/style.css` 围栏内的文本(`fence_text()`)"
      via: "`fenced.count(<令牌名>) == 0` —— 子串计数、含注释;补的是「围栏里是否还留着一行没人用的声明或一句点名它的注释」这条缝"
      pattern: "def fence_text\\(\\)"
    - from: "`check-09` 的交互控件对照组"
      to: "`frontend/style.css` 的 `button` / `#project-path-input` / `#check-switcher` / `#ai-route-select` / `.overlay-card` 规则"
      via: "同一份运行时读数里的反向证据 —— 证明「移除边界」严格限于五个容器"
      pattern: "CONTROL_GROUP"

  prohibitions:
    - statement: "不得为了让门绿、或为了让结论成立,而删除 / 降级 / 放宽任何断言、阈值或判据,也不得只断言「规则被写下了」。`check-09` 反转后**必红** —— 那正是门在正确工作的证据。正解只有一条:把判据改写为断言**新契约**,并用变异测试证明它真的会失败"
      status: active
      verification: flagged
    - statement: "不得补一条**通用的**围栏消费断言(「每个声明的令牌都被消费」)。那是 G2,用户 2026-09-28 只裁定「连带 G1」,G2 **未点名**。本阶段只处置本次反转自己孤立掉的两个令牌,每个令牌一条**专用**残留断言"
      status: active
      verification: flagged
    - statement: "不得在变异测试里使用 `git stash` —— 它跨工作树共享,本项目明令禁止。还原一律用定向 `git checkout -- frontend/style.css`,并以 `git diff --exit-code -- frontend/style.css` 为空作为「逐字节相同」的判据"
      status: active
      verification: flagged
---

<objective>
把 `scripts/check-09-idi09-validation.py` 的 `c1` / `c2` / `c3` / `c4` 四条判据**改写为断言新契约**,并以**变异测试**证明改写后的四条判据会真的失败。

Purpose: 该门是 Phase 9 自建的运行时门,它断言的**正是本阶段要移除的那套卡片语言** —— 反转后 `c1..c4` 必然全红,**那正是门在正确工作的证据**(ROADMAP Rationale 的逐字表述)。判据只能改写,不得删除、不得降级为恒真、不得只断言「规则被写下了」(本仓库的方法论:一条不能失败的门比没有门更糟)。

**为什么 `REG-01` 必须与反转同阶段:** 它与反转是**同一次改动、两副面孔**;拆开会造出「改了面但没人验」的中间态(与 v1.15 把 `REG-01`/`REG-02` 与 CARD/VIS 同阶段交付的裁定同型)。

**为什么必须有变异测试:** 本项目已记录的教训 —— 只跑一次真实树**无法区分**「守卫在工作」与「守卫静默空转」。变异测试是唯一能证明守卫真的会失败的手段。

**本计划关闭的需求:** REG-01。

**本计划不触碰:** `frontend/style.css`(已在波次 1/2 定型,**本计划零 CSS 改动**);`scripts/check-05-ui-uat.py`(计划 04);`scripts/check-02-contrast.py` / `scripts/check-10-idi10-validation.py` / `scripts/check-01…04` / `check-06` / `check-07` / `probe-*`(零改动);`frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**`(零字节);`G1-01` / `REG-04` / `VIS-01`(Phase 12);G2 / `999.2` / 暗色模式 / Nyquist 缺口 / 图标与空状态 / `.overlay-card` 底色(全部 Out of Scope)。

**执行前基线(规划期已在 HEAD 上实测,执行器须复核):**

| 检查 | 规划期在 HEAD 上的实测结果 |
|---|---|
| `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4`(HEAD 上) | `exit=0`;`item c1: PASS  (26 条断言,0 FAIL,0 BLOCKED)` / `c2: PASS (13)` / `c3: PASS (3)` / `c4: PASS (4)` —— **合计 46** |
| `.venv/bin/python scripts/check-09-idi09-validation.py --item c5`(HEAD 上) | `PASS`(滚动契约) |
| `scripts/check-09-idi09-validation.py` 的 `ITEMS` | `{\"c1\": c1, \"c2\": c2, \"c3\": c3, \"c4\": c4, \"c5\": c5}` |
| `scripts/check-09-idi09-validation.py` 是否有 `fence_text()` | **没有**(`check-10` 有,`check-09` 必须新增) |

**HEAD 上 `c1..c4` 断言的四类旧契约(本计划要逐条换成新契约):**

- `c1`:四个 section 的计算底色 == 卡片令牌解析值(白)、`border-top-left-radius == var(--radius-md)`(10px)、`border-top-width == 1px` + `border-top-style == solid`、`box-shadow` 非 `none` 且含卡片阴影色、阴影首层水平偏移 `0px`
- `c2`:`#doc-panel` 的计算底色 == 卡片令牌、`border-top-left-radius == var(--radius-md)`、四边 `border-*-width == 1px` 且 `border-*-style == solid`、`box-shadow` 非 `none`、`overflow-y == auto`;`#doc-panel-header` 的 `box-shadow == none`(对照组)
- `c3`:`body` 计算底色 == `rgb(240, 240, 240)`(gray-3)、统一面令牌解析值 == `body` 计算底色、三档令牌亮度**严格递增**(页面 < 内陷面 < 卡片)
- `c4`:`#main-pane` 计算 `gap == 12px`、`.panel-body` 计算 `padding == 16px`、`#doc-panel-body` 计算 `padding == 32px 40px`(对照组)、`.panel-header` 计算 `padding-top == 6px`(对照组)

Output: 改写后的 `scripts/check-09-idi09-validation.py`(`c1..c4` 新契约 + `fence_text()` + 两条专用残留断言 + 交互控件对照组);六条变异测试的真实「变异 → FAIL」读数;`c5` 复跑证据。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/REQUIREMENTS.md
@.planning/phases/idi-11-decard-and-hairline-dividers/11-CONTEXT.md
@.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-PATTERNS.md
@.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-01-PLAN.md
@.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-02-PLAN.md
@scripts/check-09-idi09-validation.py
@scripts/check-10-idi10-validation.py
@scripts/check-05-ui-uat.py
@frontend/style.css
</context>

## Artifacts this phase produces

> 本节列出**本计划**那部分;全阶段的产出表在 `idi-11-01-PLAN.md` 的 §「Artifacts this phase produces」,不重复。

**新增符号(全部在 `scripts/check-09-idi09-validation.py`):**

| # | 符号 | 种类 | 用途 |
|---|---|---|---|
| 1 | `FENCE_START` / `FENCE_END` | 模块常量 | `"===== DESIGN TOKENS: START ====="` / `"===== DESIGN TOKENS: END ====="`,与 `check-10` 逐字相同 |
| 2 | `STYLE_CSS` | 模块常量 | `ROOT / "frontend" / "style.css"`,供源码文本级残留断言 |
| 3 | `fence_text()` | 函数 | 返回两行围栏标记之间的文本(含标记行自身)。**逐字照抄 `scripts/check-10-idi10-validation.py` 的同名函数** |
| 4 | 统一面字面量常量 | 模块常量 | `"rgb(255, 255, 255)"` —— 两侧写死,防止「令牌被改坏而消费者仍接线」时假绿 |
| 5 | 内陷面字面量常量 | 模块常量 | `"rgb(249, 249, 249)"`(gray-2) |
| 6 | 发丝线字面量常量 | 模块常量 | `"rgb(217, 217, 217)"`(gray-6)。照 `check-10` 的 `TH_BORDER_LITERAL` 同型,用于发丝线颜色的**字面量半条**断言 |
| 7 | `CONTROL_GROUP` | 模块常量 | 交互控件对照组的 `(选择器, 说明)` 元组序列:`button` / `#project-path-input` / `#check-switcher` / `#ai-route-select` / `.overlay-card`。**不含 `.panel-header`** |
| 8 | 两条专用残留断言标签 | 断言 | `fenced.count(<被删令牌名>) == 0`,每个被删令牌一条,走 `ok_true` |
| 9 | 两条「被删令牌已不可解析」断言标签 | 断言 | `resolve_token(...) is None`,走 `ok_true`(C-4:`ok()` 会把 `None` 降级成 BLOCKED) |

**删除的既有符号(同一文件):**

| # | 符号 | 动作 |
|---|---|---|
| 10 | 卡片阴影字面量常量(HEAD 上记录用户裁定阴影值的那两个) | **删除** —— 它们断言的契约已不存在 |
| 11 | 卡片白字面量常量 | **删除**,由新的统一面字面量常量取代 |
| 12 | `shadow_lengths()` | **删除**(它只服务「卡片阴影首层水平偏移为 0px」那条已不存在的断言)。若改写得当它已无调用点;删除后须确认文件里零引用 |

**保留不动:** `ITEMS`(仍是 `c1..c5`)、`parse_args()`、`main()` 的退出码语义与 `--item` / `--screenshot` / `--keep` 三个参数、`--screenshot DIR` 的输出路径与 5 个样本的逐张 1440×900 断言、`png_size()`、`load_check05()` 与它导出的全部 `c05` 助手。

## 波次与依赖形状

| 波次 | 计划 | 为什么必须在这个位置 |
|---|---|---|
| 1 | `idi-11-01` | 反转本体 |
| 2 | `idi-11-02` | 令牌删除 + 清单重归属(本计划的两条残留断言以它为**前置**:断言的是「围栏内已无该令牌名」) |
| 3 | `idi-11-03`(本计划) | 判据断言的是**改动后的**渲染状态与围栏文本,故必须在 `style.css` 定型之后改写并验证 |

<tasks>

<task type="auto" tdd="false">
  <name>Task 1: 改写 `c1` 与 `c2` —— 连续面的运行时判据 + 交互控件对照组 + 活动标记的正面断言</name>
  <files>scripts/check-09-idi09-validation.py</files>
  <reversibility rating="costly">撤销要重写两条判据并重跑六条变异(D-11-12 的 Reversibility 评级)。</reversibility>
  <read_first>
    - `scripts/check-09-idi09-validation.py` **全文**(552 行)—— 逐字读文件头 docstring(「为什么另开一个文件」的论证里点名的五条既有门与它们的盲区)、`LEFT_SECTIONS`、`SHADOW_CARD_LITERAL` / `SHADOW_CARD_COLOR` / `CARD_WHITE` / `_SHADOW_COLOR_RE` / `shadow_lengths()`、`c1()` / `c2()` / `c3()` / `c4()` / `c5()` 四个 item 函数、`ITEMS`、`parse_args()`、`main()`
    - `scripts/check-10-idi10-validation.py` 的**模块级骨架**(`STYLE_CSS` / `FENCE_START` / `FENCE_END` / `TH_BORDER_LITERAL` / `fence_text()` / `load_check05()` 的常量与助手导入块)—— 本任务要照抄的形态
    - `scripts/check-10-idi10-validation.py` 的 `r1` 的**令牌级硬 FAIL 段**(走 `ok_true` 而非 `ok()` 的那一段及其上方那条解释「`ok()` 在 expected/actual 为 `None` 时记 BLOCKED,而令牌被删正是本项要抓的回归」的注释)—— 本任务要照抄的形态
    - `scripts/check-05-ui-uat.py` 的 `ok()` / `ok_true()` / `blocked()` / `info()` / `read_style()` / `resolve_color()` / `resolve_token()` / `norm()` / `parse_rgb()` / `relative_luminance()` 的实现与语义 —— 特别是 `ok()` 的 `expected is None` → BLOCKED 那一支
    - `frontend/style.css` 的五个容器规则(Task 1 / Task 2 已改写的状态)、`#main-pane > section + section` 规则、`.panel-header` 规则、三条活动标记规则(`#session-panel:not(.hidden) .panel-header` 等)
    - `frontend/style.css` 的 `button` / `#project-path-input` / `#check-switcher` / `#ai-route-select` / `.overlay-card` 规则 —— 交互控件对照组的五个来源
    - `frontend/index.html` —— 确认五个对照组元素都在 DOM 里、四个 `section` 的 DOM 顺序、`#annotations-panel` / `#checks-panel` 在 `p1` 带 `.hidden`
    - `.planning/phases/idi-11-decard-and-hairline-dividers/11-CONTEXT.md` §D-11-12(逐条断言面)与 §D-11-13(变异集合)
    - `.planning/ROADMAP.md` §`### Phase 11:` 的 Success Criterion 1、4 与 Avoids 第 1、2、7 条
  </read_first>
  <action>
    **第 1 步 —— 更新文件头 docstring。**

    原文的「为什么另开一个文件」论证写的是 Phase 9 的卡片语言。改写为 Phase 11 的语境:本门断言的是**去卡片化之后**的渲染契约(连续面 + 统一面 + 灰缝归零 + 两条发丝线),并明确写下「本文件在 Phase 11 被**改写**而非删除 —— 它断言的旧契约反转后必然全红,那正是门在正确工作的证据」。退出码语义与浏览器路线两段**逐字保留**。

    **第 2 步 —— 模块级常量:删旧增新。**

    删除那三个只服务旧契约的常量(卡片阴影字面量、卡片阴影色、卡片白字面量)与 `_SHADOW_COLOR_RE` / `shadow_lengths()`(它们唯一的用途是「卡片阴影首层水平偏移为 0px」那条已不存在的断言;删除后确认文件里零引用)。

    新增:
    - `STYLE_CSS = ROOT / "frontend" / "style.css"`
    - `FENCE_START` / `FENCE_END`(两个围栏标记字符串,**逐字**与 `check-10` 相同)
    - 三个字面量常量:统一面 `"rgb(255, 255, 255)"`、内陷面 `"rgb(249, 249, 249)"`、发丝线 `"rgb(217, 217, 217)"`
    - `CONTROL_GROUP`:五个 `(选择器, 说明)` 元组 —— `button` / `#project-path-input` / `#check-switcher` / `#ai-route-select` / `.overlay-card`。**`.panel-header` 不得进这个序列**(它有合法的 `border-radius: 0` 与合法的 `inset` 阴影)
    - `fence_text()`:**逐字照抄** `check-10` 的同名函数(用 `STYLE_CSS.read_text(encoding="utf-8")` 与两次 `str.index`)

    **第 3 步 —— 改写 `c1`(连续面 + 对照组 + 残留断言 + 被删令牌探测器)。**

    `c1` 分两半:

    **(a) 源码文本级(浏览器之前,不需要 fixture)** —— 两条**专用**残留断言(**D-11-4**:删除两个令牌后按 Phase 10 先例各加一条专用残留断言,照 `check-10` 的 `r1` 同型),走 `ok_true`:
    - `fenced.count(<被删的卡片底色令牌名>) == 0`
    - `fenced.count(<被删的卡片阴影令牌名>) == 0`

    标签与注释里要写明判据是**围栏内的子串计数、含注释**(标签不要写「声明残留计数」那种会误导的说法),并写明依据是围栏抬头与 Hard Rule 5 / D-04「只声明被消费的令牌」、先例是 Phase 10 删除未并入刻度的圆角档位。**并在注释里显式写下「这不是通用围栏消费断言 —— 通用断言属 G2,不在 v1.16 范围」**,以免后人把它当 G2 的雏形扩写。

    **(b) 运行时(单个 `p1` fixture)** —— 对 `LEFT_SECTIONS` 的每一个:
    - 计算 `box-shadow == "none"`
    - 四个 `border-*-radius` **长手**均 `== "0px"`(**读长手,不读简写** —— 简写在多值规则体上会被 Chrome 序列化成三值,不可断言)
    - 计算底色 == **同一份读数里**读到的 `body` 计算底色,**并且**另有一条与写死字面量 `rgb(255, 255, 255)` 比对的断言(两侧都写死,防止「令牌被改坏而消费者仍接线」时假绿)
    - 边界宽度按**异形**形状断言:`#session-panel` 四条 `border-*-width` 全 `0px`;其余三个各自 `border-top-width == "1px"` 且另外三条 `0px`。**不要写成一条统一循环** —— `#session-panel` 是 DOM 第一个 `section`,`section + section` 永不匹配它

    同一份读数里给出**交互控件对照组**:对 `CONTROL_GROUP` 的每一项断言 `border-top-left-radius != "0px"` 且 `border-top-width != "0px"`;`.overlay-card` 另断言 `box-shadow != "none"`。注释写明这是 SC1 明文要求的反向证据(否则「移除边界」可能是把整站边界一起抹掉),以及 `#ai-route-select` 之所以被选为 `select` 族的代表是**因为它在样式表里有显式声明**(判据确定,不依赖 UA 默认样式)。

    另加一条**正面断言**,证明去卡片后仅存的活动态线索存活:`#session-panel .panel-header`(`p1` 下未隐藏)的计算 `box-shadow` 非 `none` 且同时含 `inset` 与 `3px 0px` 两个子串。注释写明**为什么 `.panel-header` 不进对照组也不进「`box-shadow === none`」集合**。

    另加两条**被删令牌探测器**,走 `ok_true`:`resolve_token(page, <被删的卡片底色令牌名>) is None` 与 `resolve_token(page, <被删的卡片阴影令牌名>) is None`。注释照抄 `check-10` `r1` 的那条解释:`ok()` 在期望侧为 `None` 时记 BLOCKED(exit 2,本项目当良性码),而「令牌被删」正是本项要抓的回归 —— 令牌未声明必须是**硬 FAIL**。

    **第 4 步 —— 改写 `c2`(`#doc-panel` 的新契约)。**

    同一 `p1` fixture 下:
    - 计算 `box-shadow == "none"`
    - 四个 `border-*-radius` 长手均 `== "0px"`
    - 四条边中**仅** `border-left-width == "1px"`;`border-top-width` / `border-right-width` / `border-bottom-width` 均 `== "0px"`
    - `border-left-style == "solid"`
    - `border-left-color` **双断言**:等于运行时解析的 `--color-border-subtle`,**且**等于写死字面量 `rgb(217, 217, 217)`
    - `overflow-y == "auto"`(**承重的滚动契约**,注释写明:L-1 的 sticky 表头依赖 `#doc-panel` 仍是最近的可滚祖先)。**注释里不得出现「滚动者普查期望值是 4」这一说法** —— 磁盘实测该普查是 3 个成员且 `#doc-panel` 根本不在它的遍历范围内(它是 `#main-pane` 的兄弟),保留 `overflow-y` 的理由**只有** L-1
    - `#doc-panel-header`:计算 `position == "sticky"`、`top == "0px"`、计算 `background-color` **非** `rgba(0, 0, 0, 0)` 且等于统一面的计算底色(证明 sticky 背景声明仍在盘上、且已随统一面改归属 —— 不加背景则滚动正文从标题行底下穿过)

    **所有令牌解析断言一律走 `ok_true` 并显式处理 `None`**(`resolve_color` / `resolve_token` 对未声明令牌返回 `None`)。**不得**用裸 `ok(...)` 配一个可能为 `None` 的期望侧。

    **第 5 步 —— 跑一次,确认此刻两条新判据在已定型的 `style.css` 上全绿。**

    `.venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2`。要求 `exit=0`、`0 FAIL`、`0 BLOCKED`。若出现 BLOCKED,先怀疑探针(元素/选择器读不到),不要先改期望值。

    **第 6 步 —— 不触碰范围之外的一切。** 不改 `c3` / `c4` / `c5`(Task 2 / 保留);不改 `ITEMS` / `parse_args()` / `main()`;不改 `scripts/` 下任何其它文件;不改 `frontend/style.css`。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or the "=== 逐项结论 ===" block showing a non-zero FAIL or BLOCKED count for item c1 or c2, or the trailing line not starting with "exit=0"</fails_when>
    <automated>grep -nF -- 'def fence_text()' scripts/check-09-idi09-validation.py; grep -cF -- 'ok_true' scripts/check-09-idi09-validation.py</automated>
    <fails_when>the `def fence_text()` line is not found, or the `ok_true` occurrence count is lower than it was at HEAD (the rewrite must move token assertions from `ok` to `ok_true`, never the reverse)</fails_when>
    <automated>.venv/bin/python -c "import pathlib,re;t=pathlib.Path('scripts/check-09-idi09-validation.py').read_text(encoding='utf-8');print('shadow_lengths_refs', len(re.findall(r'shadow_lengths', t)));print('card_literals', len(re.findall(r'SHADOW_CARD_LITERAL|SHADOW_CARD_COLOR|CARD_WHITE', t)))"</automated>
    <fails_when>either count is not "0" (the retired card-language constants and their only helper must have no surviving references)</fails_when>
    <automated>git status --porcelain scripts/ frontend/</automated>
    <fails_when>output contains any path other than "scripts/check-09-idi09-validation.py", or output is empty</fails_when>
  </verify>
  <acceptance_criteria>
    - `check-09 --item c1 --item c2` → `exit=0`,`0 FAIL`,`0 BLOCKED`。
    - `fence_text()` 存在且与 `check-10` 的同名函数**逐字相同**;`FENCE_START` / `FENCE_END` / `STYLE_CSS` 三个模块常量存在。
    - `c1` 含两条专用残留断言(`ok_true` + 围栏内子串计数)与两条「被删令牌已不可解析」探测器(`ok_true` + `resolve_token(...) is None`);标签与注释写明判据**含注释**、依据是围栏抬头与 Hard Rule 5 / D-04、且**明确写出「这不是通用围栏消费断言(属 G2)」**。
    - `c1` 对四个 `section` 断言 `box-shadow == "none"`、四个半径长手 `"0px"`、计算底色 == `body` 计算底色 **且** == `rgb(255, 255, 255)`;边界宽度按异形形状断言(`#session-panel` 四边 `0px`;其余三个 `border-top-width == "1px"`、另三边 `0px`)。
    - `c1` 含交互控件对照组(五项,`border-top-left-radius != "0px"` 且 `border-top-width != "0px"`;`.overlay-card` 另断言 `box-shadow != "none"`),**且 `.panel-header` 不在组内**;另含 `#session-panel .panel-header` 的活动标记正面断言(计算 `box-shadow` 含 `inset` 与 `3px 0px`)。
    - `c2` 断言 `#doc-panel` 的 `box-shadow == "none"`、四角 `0px`、仅 `border-left-width == "1px"`、`border-left-style == "solid"`、`border-left-color` 双断言(令牌 + 字面量 `rgb(217, 217, 217)`)、`overflow-y == "auto"`;`#doc-panel-header` 的 `position` / `top` / 背景三条断言在位。
    - `c2` 的注释**不出现**「滚动者普查期望值是 4」这一说法;保留 `overflow-y` 的理由只写 L-1 的 sticky 依赖。
    - 改写后的 `c1` / `c2` 里所有令牌解析断言都走 `ok_true` 并显式处理 `None`;`shadow_lengths()` 与三个卡片语言常量在全文件零引用。
    - `git status --porcelain scripts/ frontend/` 仅列出 `scripts/check-09-idi09-validation.py`。
  </acceptance_criteria>
  <done>`check-09` 的 `c1` / `c2` 已改写为断言连续面 + 统一面 + 竖线的新契约:运行时计算读数为主判据、令牌解析降为诊断、交互控件对照组在同一份读数里给出、活动标记被正面断言、`.panel-header` 被显式排除;两条专用残留断言与两条「被删令牌已不可解析」探测器就位;`c1`/`c2` 在定型后的 `style.css` 上 `exit=0` / 0 FAIL / 0 BLOCKED。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 2: 改写 `c3` 与 `c4` —— 两级刻度 + 灰缝归零 + 两条发丝线的宽度/颜色双断言 + 竖线跨满几何</name>
  <files>scripts/check-09-idi09-validation.py</files>
  <reversibility rating="costly">撤销要重写两条判据并重跑六条变异。</reversibility>
  <read_first>
    - `scripts/check-09-idi09-validation.py` 的 `c3()` 与 `c4()` 全文(**Task 1 已改写的状态**)—— 逐字读 `GRAY3_BODY` / `TIER_TOKENS` 两个模块常量、`c3` 的令牌级亮度比较与只读诊断段、`c4` 的四行 `readings` 表
    - `scripts/check-10-idi10-validation.py` 的双断言段(`t2` 里「计算 `border-bottom-color == var(--color-border-subtle)`」与「计算 `border-bottom-color == gray-6 字面量」两条相邻断言,含后者上方那条解释「只跟令牌比是自指的」的注释)—— **本任务照抄的形态**
    - `scripts/check-05-ui-uat.py` 的 `parse_rgb()` / `relative_luminance()` / `contrast_ratio()` 实现(本任务直接复用,**不另写一份**)
    - `frontend/style.css` 的 `html, body` 规则、五个容器规则、`#main-pane > section + section` 规则、`.panel-body` 规则、`#doc-panel-body` 规则、`.panel-header` 规则
    - `frontend/index.html` 的 `#app` 段(确认 `#doc-panel` 是 `#app` 的 flex 子项、默认 `align-items: stretch` ⇒ 它天然跨满视口高)
    - `scripts/check-05-ui-uat.py` 的 `[p1] sticky 把 #doc-panel-header 钉在 #doc-panel 顶部(<=1px)` 断言 —— **本任务只读它、不改它**(它是计划 04 的 REG-03 对象)
    - `.planning/phases/idi-11-decard-and-hairline-dividers/11-CONTEXT.md` §D-11-10 / §D-11-12 的 c3 / c4 两条 / §D-11-14
    - `.planning/ROADMAP.md` §`### Phase 11:` 的 Success Criterion 2、3、4
  </read_first>
  <action>
    **第 1 步 —— 改写 `c3`:三级刻度改成两级。**

    删除只服务旧契约的 `GRAY3_BODY` 常量与三档 `TIER_TOKENS` 表(卡片档的令牌已不存在)。

    新 `c3` 的断言:
    - `body` 的计算 `background-color` == 运行时解析的 `--color-surface-page`(**等值复核**:证明底色来自令牌而不是硬编码的 `rgb()`)—— 走 `ok_true`,显式处理 `None`
    - `body` 的计算 `background-color` == 写死字面量 `rgb(255, 255, 255)`(两侧都写死,防止「令牌被改坏而消费者仍接线」时假绿)
    - `body` 的计算 `background-color` **不等于** `rgb(240, 240, 240)`(旧页面档 gray-3 已退场)
    - `--color-surface`(内陷面)解析值的相对亮度**严格低于**统一面的相对亮度。**判据取令牌级读数**(`resolve_color` 分别解析后比较),**不取某元素的 `effective_bg`** —— `effective_bg` 沿祖先链找第一个非透明底色,三档里中间档不被任何元素采用时会被整个跳过,断言就在看不见的那一档上恒真(Phase 9 已为此付过代价)
    - 一条只读诊断:统一面与内陷面的对比度比值(不判定,供截图评审)

    注释里要写明**三级刻度改写成两级**这件事本身:统一面 > 内陷面,「统一」是把卡片档并回页面档,**不是**把所有层次压平。

    **第 2 步 —— 改写 `c4`:灰缝归零 + 两条发丝线 + 几何 + 三条对照组。**

    新 `c4` 的断言:
    - `#main-pane` 计算 `gap == "0px"`(HEAD 上是 `12px`)
    - **竖线**:`#doc-panel` 计算 `border-left-width == "1px"` 且 `border-left-color` **双断言**(解析的 `--color-border-subtle` + 写死字面量 `rgb(217, 217, 217)`)
    - **横线**:对 `#annotations-panel` / `#checks-panel` / `#ai-panel` 各自断言计算 `border-top-width == "1px"` 且 `border-top-color` **双断言**;并断言 `#session-panel` 的计算 `border-top-width == "0px"`(第一个面板顶部不画线)
    - **竖线跨满**:读 `#doc-panel` 的 `getBoundingClientRect()`,断言其高度**等于视口高度**(1440×900 下 `top == 0` 且 `bottom == 900`)。**这一条是承重的** —— 没有它,「跨满面板可视高度」就退化成一个恒真的「有一条 1px 边框」断言
    - 三条**对照组**(证明改动没有漏出裁定范围):`.panel-body` 计算 `padding == "16px"`(D-11-6:保持不动)、`#doc-panel-body` 计算 `padding == "32px 40px"`(右栏阅读列未受影响)、`.panel-header` 计算 `padding-top == "6px"`(表头 chrome 条的内边距未随卡片内边距改动)

    双断言的字面量半条**必须**有,注释照抄 `check-10` 的解释:「与上一条互补:只跟令牌比是**自指的**,令牌被改成 gray-7 时两侧一起变、恒过;这一条把「线是浅档」钉死在 gray-6」。**没有它,D-11-8 显式否决的那个备选(gray-7)对门是不可见的。**

    注释里还要写明**为什么发丝线不登记 NON-TEXT 对比度对**:它不标识任何控件、不标识任何状态 ⇒ SC 1.4.11 不适用;并附反证(gray-6 在白面上仅 1.412,达标需 gray-9 的 3.319,那会把发丝线变成深灰框)。依据是围栏内 role-band 段与 PAIR 清单头部注释的**两处既有登记**,注释须点名它们。

    **所有令牌解析断言一律走 `ok_true` 并显式处理 `None`。**

    **第 3 步 —— 跑四条并记录断言计数。**

    `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4`。要求 `exit=0`、`0 FAIL`、`0 BLOCKED`,并把 `=== 逐项结论 ===` 块的**原文**抄进 SUMMARY。

    统计 `c1..c4` 的断言总数,要求 **>= 46**(HEAD 实测基线)。若低于 46,说明有断言被删而未被等价替代 —— 回到第 1/2 步补齐,**不得**把 46 这个数字往下改。

    再跑 `.venv/bin/python scripts/check-09-idi09-validation.py --item c5`,要求仍 `PASS`(滚动契约原样保留、未被本次改写波及)。

    **第 4 步 —— 不触碰范围之外的一切。** 不改 `c5`;不改 `ITEMS` / `parse_args()` / `main()`;不改 `--screenshot` 路径;不改 `scripts/` 下任何其它文件;不改 `frontend/style.css`。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or the "=== 逐项结论 ===" block showing a non-zero FAIL or BLOCKED count for any of c1/c2/c3/c4, or the sum of the four assertion counts being less than 46</fails_when>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c5</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or the trailing line not starting with "exit=0", or the c5 assertion count differing from the HEAD baseline</fails_when>
    <automated>grep -cF -- 'rgb(217, 217, 217)' scripts/check-09-idi09-validation.py; grep -cF -- 'GRAY3_BODY' scripts/check-09-idi09-validation.py</automated>
    <fails_when>the first count is "0" (the hairline literal half is missing — without it a swap to gray-7 is invisible to the gate), or the second count is not "0" (the retired gray-3 page-tier constant must be gone)</fails_when>
    <automated>grep -cF -- 'getBoundingClientRect' scripts/check-09-idi09-validation.py</automated>
    <fails_when>the count is "0" (the "spans the full panel height" claim needs a real geometry reading, not just a 1px-border existence check)</fails_when>
    <automated>git status --porcelain scripts/ frontend/</automated>
    <fails_when>output contains any path other than "scripts/check-09-idi09-validation.py", or output is empty</fails_when>
  </verify>
  <acceptance_criteria>
    - `check-09 --item c1,c2,c3,c4` → `exit=0`,`0 FAIL`,`0 BLOCKED`;四项断言计数之和 **>= 46**;`=== 逐项结论 ===` 块原文入册。
    - `check-09 --item c5` → `exit=0`,`PASS`,断言计数与 HEAD 基线一致。
    - `c3` 断言两级刻度:body 计算底色 == 统一面令牌解析值 **且** == 字面量 `rgb(255, 255, 255)` **且** != `rgb(240, 240, 240)`;内陷面令牌解析值的相对亮度严格低于统一面。判据是**令牌级**读数,不是 `effective_bg`。`GRAY3_BODY` 常量已删除。
    - `c4` 断言 `#main-pane` 计算 `gap == "0px"`;竖线与横线的宽度 `1px` 与颜色**双断言**(令牌 + 字面量 `rgb(217, 217, 217)`);`#session-panel` 的 `border-top-width == "0px"`;`#doc-panel` 的 rect 高度等于视口高度;三条对照组(`.panel-body` `16px` / `#doc-panel-body` `32px 40px` / `.panel-header` `padding-top` `6px`)在位。
    - 发丝线不登记 NON-TEXT 对的论证写在 `c4` 的注释里,并点名围栏内那两处**既有**登记 + gray-6 在 1.412 的反证。
    - `c1..c4` 里所有令牌解析断言走 `ok_true` 并显式处理 `None`;`grep -cF 'rgb(217, 217, 217)'` 非 0。
    - `ITEMS` / `parse_args()` / `main()` / `--screenshot` 路径逐字未动。
    - `git status --porcelain scripts/ frontend/` 仅列出 `scripts/check-09-idi09-validation.py`。
  </acceptance_criteria>
  <done>`c3` 由三级刻度改写为两级(统一面 == body 底色、内陷面严格更暗,判据取令牌级读数);`c4` 覆盖灰缝归零、两条发丝线的宽度与颜色双断言、第一个面板顶部无线、竖线跨满视口的真实几何、三条对照组;`c1..c4` 在定型后的 `style.css` 上 `exit=0` / 0 FAIL / 0 BLOCKED 且断言总数 >= 46;`c5` 原样保留并仍 PASS。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 3: 六条变异测试 —— 逐条给出「变异 → FAIL」的真实读数,并在还原后证明逐字节相同</name>
  <files>scripts/check-09-idi09-validation.py</files>
  <reversibility rating="reversible">变异全部在已提交的树上做并定向还原;净 diff 为零,本任务只产生证据。</reversibility>
  <read_first>
    - `scripts/check-09-idi09-validation.py`(**Task 1 / 2 已改写后的状态**)—— 逐字读四条判据各自断言的是哪个属性,以便为每条变异选准**唯一**要触发的判据
    - `frontend/style.css` 的五个容器规则、`#main-pane > section + section` 规则、`html, body` 规则、围栏内 `--color-surface-page` / `--color-surface` 两行声明 —— **六条变异的落点**
    - `.planning/phases/idi-11-decard-and-hairline-dividers/11-CONTEXT.md` §D-11-13(**六条变异的逐字清单**与三条硬性要求:在已提交的树上做、定向 `git checkout --` 还原、禁用 `git stash`)
    - `.planning/ROADMAP.md` §`### Phase 11:` 的 Success Criterion 4 与 Gates 行
    - `scripts/probe-05-resolve-color.py` 与 `scripts/probe-07-focus-composite.py` 的文件头 —— 本仓库「变异测试是唯一能证明守卫真的会失败的手段」这条方法论的既有表述与对照支的写法
  </read_first>
  <action>
    **第 1 步 —— 先固定前置条件。**

    在动手前记录三件事并写进 SUMMARY:(a) `git status --porcelain` 里 `frontend/style.css` **干净**(波次 1/2 的改动已提交 —— 若未提交,先停下报回,变异必须在**已提交的树**上做);(b) 记下 `git rev-parse HEAD` 与 `git hash-object frontend/style.css`;(c) 跑一次基线 `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4`,确认 `exit=0`。

    **第 2 步 —— 逐条执行六条变异。**

    每条严格按同一个四步循环:

    1. **注入**:用 `Edit` 在 `frontend/style.css` 上做**最小**变异(只改一条声明 / 删一条声明 / 加回一条声明);
    2. **观察**:跑对应的 `check-09 --item <受影响项>`,把**完整输出里至少一条 FAIL 行的原文**(含 `expected=` / `actual=`)抄进 SUMMARY —— **不得只写「FAIL 了」**;
    3. **还原**:`git checkout -- frontend/style.css`;
    4. **证明还原**:`git diff --exit-code -- frontend/style.css` 必须为空(退出码 0);并 `git hash-object frontend/style.css` 与第 1 步记录的值**逐字符相同**。

    **⚠ 禁用 `git stash`** —— 它跨工作树共享,本项目明令禁止。

    六条变异与它们**必须**触发的判据:

    | # | 变异(最小改动) | 必须变红的判据 |
    |---|---|---|
    | 1 | 给 `#main-pane > section` 加回一条 `border: 1px solid var(--color-border);`,**或**加回一条**字面量**阴影 `box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);`(**不是** `var(--shadow-card)`) | `c1` 的 `box-shadow == "none"` / 边界宽度断言 |
    | 2 | 给 `#doc-panel` 加回四边边界(把 `border-left: 1px solid var(--color-border-subtle);` 换成 `border: 1px solid var(--color-border-subtle);`) | `c2` 的「仅 `border-left-width == "1px"`」 |
    | 3 | 删掉 `#doc-panel` 的 `overflow-y: auto;` | `c2` 的 `overflow-y == "auto"`(承重滚动契约) |
    | 4 | 把围栏内 `--color-surface-page` 的值改回 `var(--color-surface)`(统一面与内陷面塌成同一档) | `c3` 的「内陷面亮度严格低于统一面」 |
    | 5 | 把 `#main-pane` 的 `gap: 0;` 改回 `gap: var(--space-3);` | `c4` 的 `gap == "0px"` |
    | 6 | 删掉 `#main-pane > section + section { border-top: … }` 整条规则块 | `c4` 的横线宽度/颜色断言 |

    > **第 1 条为什么用字面量阴影而不是 `var(--shadow-card)`(本表唯一的改写点):** 波次 2(计划 02)已从围栏里**删掉 `--shadow-card` 声明**,而本计划(波次 3)`depends_on: [idi-11-01, idi-11-02]`。到波次 3 该令牌已不存在 ⇒ `box-shadow: var(--shadow-card)` 在 computed-value 时无效(IACVT)、解析成初始值 `none` —— **恰好等于 `c1` 断言的那个值** ⇒ 那条路线**不会变红**,是条空转的变异。加回一条**字面量**阴影才是真实回归的忠实模拟:令牌已不存在,没人能真的「重新提交一次加回令牌」;而 `box-shadow` 非 `none` ⇒ `c1` 的 `box-shadow == "none"` 断言**真的变红**。第 2–6 条的路线已逐条复核,各自的落点都指向表中指定的判据、且都能让该判据变红,无同型缺陷(它们的落点都是波次 2 **未删除**的令牌或属性:`--color-border` / `--color-border-subtle` / `overflow-y` / `--color-surface-page` / `--color-surface` / `gap`)。

    每条完成后都要确认「还原 → 基线复绿」:还原后重跑同一项,`exit=0`。**若某条变异没有让对应判据变红,那不是「变异没生效」就是「判据在空转」—— 停下判因**,把该条的原始读数写进 SUMMARY 报回,不要改判据去迁就。

    **第 3 步 —— `c5` 复跑。**

    跑 `.venv/bin/python scripts/check-09-idi09-validation.py --item c5`,确认滚动契约在改动后仍成立,把 `=== 逐项结论 ===` 里 `c5` 那一行原文抄进 SUMMARY。

    **第 4 步 —— 收口:确认树的最终状态。**

    - `git status --porcelain scripts/ frontend/` 只列出 `scripts/check-09-idi09-validation.py`(本计划的唯一改动);
    - `git diff --exit-code -- frontend/style.css` 为空;
    - `git hash-object frontend/style.css` 与第 1 步记录的值逐字符相同;
    - 重跑一次 `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4` 与 `--item c5`,全 `exit=0`。

    **第 5 步 —— 不触碰范围之外的一切。** 本任务的净改动为零(变异全部还原);除 SUMMARY 外不产出任何文件;不改 `scripts/` 下其它文件;不改 `frontend/style.css` 的最终状态。
  </action>
  <verify>
    <automated>git status --porcelain frontend/</automated>
    <fails_when>output is not empty (every mutation must have been restored; a dirty frontend/ means a mutation is still applied)</fails_when>
    <automated>git diff --exit-code -- frontend/style.css; echo "rc=$?"</automated>
    <fails_when>rc is not "0" (frontend/style.css must be byte-identical to its committed state after all six mutations)</fails_when>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4</automated>
    <fails_when>non-zero exit, or any FAIL, or any BLOCKED, or the four assertion counts summing to less than 46</fails_when>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c5</automated>
    <fails_when>non-zero exit, or any FAIL, or the trailing line not starting with "exit=0"</fails_when>
    <automated>git status --porcelain scripts/</automated>
    <fails_when>output contains any path other than "scripts/check-09-idi09-validation.py", or output is empty</fails_when>
  </verify>
  <acceptance_criteria>
    - 六条变异**逐条**给出了「变异 → FAIL」的**真实读数**:每条至少一行 FAIL 的**完整原文**(含 `expected=` / `actual=`)抄进 SUMMARY。**不得**只写「已变异,判据变红」。
    - 六条变异的落点与本计划列出的表逐条对应;每条触发的判据就是表中指定的那一项。
    - 每条变异都在**已提交的树**上做,还原用定向 `git checkout -- frontend/style.css`;**全程未使用 `git stash`**(SUMMARY 里明确记下这一点)。
    - 还原后 `git diff --exit-code -- frontend/style.css` 退出码为 **0**,且 `git hash-object frontend/style.css` 与变异前的记录值**逐字符相同** —— 即「逐字节相同」有独立证据,不是「我记得还原了」。
    - 还原后重跑 `--item c1,c2,c3,c4` 与 `--item c5` 全 `exit=0` / 0 FAIL / 0 BLOCKED。
    - 若某条变异**未**让对应判据变红,SUMMARY 里保留了该条的原始读数并报回(不得改判据迁就)。
    - `git status --porcelain frontend/` 为空;`git status --porcelain scripts/` 仅列出 `scripts/check-09-idi09-validation.py`。
  </acceptance_criteria>
  <done>六条变异各有一条真实 FAIL 读数入册;每条在已提交的树上做、定向还原、还原后 `git diff --exit-code` 为空且 `hash-object` 逐字符相同;全程未用 `git stash`;`c1..c4` 与 `c5` 在最终树上全绿。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 无外部输入边界 | 本计划只改一个**只读的本地运行时门脚本**的判据:零用户输入处理、零鉴权、零数据访问、零网络调用、零新增资源加载。攻击面限于**门脚本自起 `uvicorn` 并驱动无头浏览器**这一次本地动作 |
| 本地进程边界(门脚本) | `check-09` 会 `ensure_server()` 自起(或复用)`uvicorn`,并用 Playwright 驱动无头 chromium 访问 `localhost`。它与被测样本之间必须是**只读**关系 |
| 变异测试边界 | 六条变异会**临时修改** `frontend/style.css`。若还原不彻底,仓库会带着一条被注入的缺陷进入后续波次 —— 这是本计划最高的操作风险 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-11-12 | Tampering | 六条变异对 `frontend/style.css` 的临时修改 | **high** | mitigate | 一条未还原的变异会伪装成「产品状态」进入计划 04 的全门复跑,让后续所有证据建立在假状态上。缓解:(a) 每条变异后立刻 `git checkout -- frontend/style.css`;(b) 判据是 `git diff --exit-code -- frontend/style.css` 退出码 0 **且** `git hash-object` 与变异前记录值逐字符相同 —— 两道独立判据,不靠记忆;(c) **禁用 `git stash`**(跨工作树共享,本项目明令禁止);(d) 收口时再跑一次 `git status --porcelain frontend/` 必须为空 |
| T-idi-11-13 | Tampering | 门判据本身(「把门改小以让结论成立」) | **high** | mitigate | 删除断言 / 放宽阈值 / 降级为恒真 / 只断言「规则被写下了」都是本仓库明令禁止的错向。缓解:(a) 断言总数 **>= 46** 是机器判据;(b) 六条变异证明每条改写后的判据**真的会失败** —— 一条不能失败的门比没有门更糟;(c) 交互控件对照组与活动标记的正面断言使「移除边界」不可被过度执行;(d) 双断言的字面量半条使 gray-7 备选对门可见 |
| T-idi-11-14 | Repudiation | 「判据已改写且会失败」这一结论缺少可复核的原始证据 | **high** | mitigate | 每条变异必须给出 FAIL 行的**完整原文**(含 `expected=` / `actual=`),不得只写「变红了」;`=== 逐项结论 ===` 块与断言计数原文入册;还原后的 `git diff --exit-code` 与 `git hash-object` 值入册 |
| T-idi-11-15 | Tampering | fixture 生命周期(`c05.make_fixture`) | medium | mitigate | 门驱动真实浏览器进入**临时目录里的样本副本**。缓解:复用 `check-05` 既有的 `make_fixture` / `enter_project`(本计划一行都不重写它们);临时根目录在 `finally` 里 `shutil.rmtree`(仅 `--keep` 保留);验收:`git status --porcelain scripts/ui-states/` 为空 |
| T-idi-11-16 | Denial of Service | 无 | low | accept | 门脚本的运行时长与既有阶段一致(单次 chromium 会话);`--item` 可把范围收窄到单项 |
| T-idi-11-SC | Tampering | npm / pip / cargo 安装 | low | accept | 本阶段**零安装**:零新增依赖、零构建步骤(DESIGN.md D-06 硬约束)。验收:`ls frontend/vendor/` 仅 `marked.min.js` |
</threat_model>

<verification>
**本计划的承重证据:**

- `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4` → `exit=0`,`0 FAIL`,`0 BLOCKED`,断言总数 **>= 46**
- `.venv/bin/python scripts/check-09-idi09-validation.py --item c5` → `exit=0`(滚动契约原样保留)
- 六条变异各有一条 FAIL 行的**完整原文**入册;每条还原后 `git diff --exit-code -- frontend/style.css` 退出码 0 且 `git hash-object` 逐字符相同
- `--item` / `--screenshot` / `--keep` 三个 CLI 参数与退出码语义逐字保留;`ITEMS` 仍是 `c1..c5`

**仓库卫生:**

- `git status --porcelain frontend/` 为空(全部变异已还原)
- `git status --porcelain scripts/` 仅列出 `scripts/check-09-idi09-validation.py`
- `git diff --stat -- scripts/check-05-ui-uat.py scripts/check-02-contrast.py scripts/check-10-idi10-validation.py` 为空
- `ls frontend/vendor/` 仅 `marked.min.js`
</verification>

<success_criteria>
- `check-09` 的 `c1` / `c2` / `c3` / `c4` 已改写为断言**新契约**(连续面 + 统一面 + 灰缝归零 + 两条发丝线),**零条断言被删除、零条降级为恒真**;断言总数 **>= 46**(HEAD 实测基线)。
- 判据以真实浏览器 `getComputedStyle` 计算读数为主;令牌解析降为 `info()` 诊断;所有令牌解析断言走 `ok_true` 并显式处理 `None`(避开 `ok()` 的 BLOCKED 降级陷阱)。
- 交互控件对照组在同一份运行时读数里给出;`.panel-header` 被显式排除并另获一条活动标记的正面断言。
- 两条发丝线的颜色带**双断言**(令牌 + 字面量 `rgb(217, 217, 217)`),使 D-11-8 否决的 gray-7 备选对门可见。
- 新增 `fence_text()` 与两条**专用**残留断言(围栏内子串计数、含注释),**未**补任何通用围栏消费断言(G2 不在本里程碑范围)。
- **六条变异逐条给出真实 FAIL 读数**;全程未用 `git stash`;还原后 `frontend/style.css` 逐字节相同(`git diff --exit-code` 为空 + `git hash-object` 一致)。
- `c5` 的滚动契约原样保留并仍 PASS;`ITEMS` / `parse_args()` / `main()` / `--screenshot` 路径逐字未动。
- `frontend/style.css` 本计划零改动;`scripts/` 下其它文件零改动;`frontend/app.js` / `index.html` / `backend/**` / `vendor/**` 逐字节未改。
</success_criteria>

<output>
Create `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-03-SUMMARY.md` when done
</output>

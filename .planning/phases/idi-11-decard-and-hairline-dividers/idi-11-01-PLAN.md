---
phase: idi-11-decard-and-hairline-dividers
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - frontend/style.css
autonomous: true
requirements:
  - SURF-01
  - SURF-02
  - SURF-03
  - DIV-01
  - DIV-02
  - DIV-03

estimate:
  tokens: 70000
  raw_tokens: 70000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- SURF-01 — 五个容器不再绘制边界(运行时计算读数) ----
    - "左栏 4 个 `#main-pane > section`(`#session-panel` / `#annotations-panel` / `#checks-panel` / `#ai-panel`)与 `#doc-panel` 在真实浏览器里的计算 `box-shadow` 均为 `none`(HEAD 上四个 section 与 `#doc-panel` 都是卡片阴影 `rgba(0, 0, 0, 0.08) 0px 1px 3px 0px, rgba(0, 0, 0, 0.04) 0px 1px 2px 0px`)"
    - "五个容器的四个 `border-*-radius` **物理角长手**均为 `0px`(HEAD 上是 `10px`)。判据一律读长手,不读简写 `border-radius`"
    - "**边界宽度的形状是异形的,不是一条统一循环**(C-6):`#session-panel` 是 DOM 第一个 `section`,`section + section` 永不匹配它 ⇒ 其四条 `border-*-width` **全部**为 `0px`;`#annotations-panel` / `#checks-panel` / `#ai-panel` 各自恰 `border-top-width == \"1px\"`、其余三条边 `0px`。`#doc-panel` 四条边中恰 `border-left-width == \"1px\"`、其余三条边 `0px`"
    - "**交互控件对照组在同一份运行时读数里给出**,证明「移除边界」不是把整站边界一起抹掉:按钮 / `#project-path-input` / `select` / `#check-switcher` / `.overlay-card` 仍有各自的非零 `border-*-radius` 且 `border-*-style` 非 `none`"
    - "`.panel-header` **不在**这条断言的判定集里:它合法地携带 `box-shadow: inset 3px 0 0 var(--color-marker-active)`(`frontend/style.css` 的活动面板标记规则,`#session-panel:not(.hidden) .panel-header` 等三条选择器),那是去卡片后**仅存的活动态视觉线索**。任何「所有面板后代 `box-shadow === none`」的写法都会把它误判为缺陷(C-7)"
    # ---- SURF-02 — 统一面 ----
    - "`--color-surface-page` 的值就地改写为 `var(--white)`;`html, body` 的计算 `background-color` 与四个 section 的计算 `background-color` **同值**(都是 `rgb(255, 255, 255)`),屏幕上不再有可辨的灰底与 elevation 差"
    - "`--color-surface`(gray-2,`rgb(249, 249, 249)`,相对亮度 0.947307)**仍是唯一比统一面更暗的一档**(统一面相对亮度 1.000000)⇒ 「统一」是把卡片档并回页面档,**不是把所有层次压平**;控件与 `#latest-check` 仍读作内陷"
    - "`#doc-panel-header` 的 `background` 声明**仍在盘上**(sticky 的承重声明:`.panel-header` 规则体内没有任何 `background`,不加则滚动正文从标题行底下穿过),本阶段**只改它的归属令牌**,不删除该声明"
    # ---- SURF-03 — 灰缝与侧沟归零 ----
    - "`#main-pane` 的计算 `gap` 为 `0px`(HEAD 上是 `12px`)。`align-items: center` 与 `#main-pane > section` 的 `max-width: 768px` **两条都原地保留、逐字未动**(D-11-5):它们仍在工作(控行长 / 定位置),侧沟是被「面板与页面同色」消除的 —— 沟在几何上仍在,透出的已是同一档白,不可见。**不得把它们写成「已死声明」**"
    # ---- DIV-01 / DIV-02 / DIV-03 — 发丝线 ----
    - "主区↔文档区的竖线是 `#doc-panel` 的 `border-left: 1px solid var(--color-border-subtle)`,**零新增 DOM 元素、零位移**;其计算高度**等于面板可视高度**(`#doc-panel` 的 `getBoundingClientRect()` 在 1440×900 下 `top == 0` 且 `bottom == 900`)—— 是「跨满」而不是「内容旁的一段」"
    - "左栏面板之间的横线是 `#main-pane > section + section { border-top: 1px solid var(--color-border-subtle); }`,**只 3 条**(DOM 序 `#session-panel` → `#annotations-panel` → `#checks-panel` → `#ai-panel`,相邻选择器按 DOM 相邻判定、不按渲染相邻);第一个面板顶部**不画**"
    - "两条线的计算宽度均为 `1px`、计算颜色**同时**等于运行时解析的 `--color-border-subtle` **与**写死的字面量 `rgb(217, 217, 217)`(gray-6)。**双断言是承重的**:只跟令牌比是自指的 —— 把该令牌换成 `--color-border`(gray-7)会让两侧一起变、恒过,而那正是 D-11-8 显式否决的备选(C-5)"
    - "分隔线**不登记 NON-TEXT 对比度对**(D-11-14),理由是它不标识任何控件、不标识任何状态 ⇒ SC 1.4.11 不适用。反证必须写在计划的论证里:gray-6 在白面上仅 **1.412**,若按 NON-TEXT 阈值 3.0 判即 FAIL;要让线达标就得换 gray-9(`#8d8d8d`,3.319),那会把发丝线变成深灰框,与去卡片化的目标相反"
    - "零新增颜色值、零新增 tier-1 primitive、零新增 `!important`、零 `@layer` / `@property` / `var(--x, #fallback)` / 新增 `@media`;两条线取的是**既有**语义令牌 `--color-border-subtle`(它已是 `.event-list` / `.annotation-item` / `.badge-answered` / `#latest-check` 四处的边界色)"
    # ---- 边界(逐字节) ----
    - "`frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**` **逐字节未改**;本计划的 `files_modified` 只有 `frontend/style.css`。**偏离这个预期是一个信号** —— 例如「必须加 DOM 元素才能画出跨满高的竖线」说明实现方式选错了(应改用零 DOM 的盒内手段),须停下判因,不要顺着改下去"
    - "四条静态门在本计划结束时全绿:`check-01`(围栏外零裸 `#hex`、零 tier-1 原语引用)、`check-02`(`PASS: 0 failures`)、`check-03`(`^\\.hidden {` == 1)、`check-04`(`!important;` **声明**数 == 1)"

  artifacts:
    - path: "frontend/style.css"
      provides: "统一面(`--color-surface-page` 值改为 `var(--white)`)+ 五容器去边界(就地改写,不追加覆盖)+ 灰缝归零 + 两条发丝线;四段承重注释就地改写(规则体上方,与代码同提交)"
      contains: "#main-pane > section + section { border-top: 1px solid var(--color-border-subtle); }"
    - path: ".planning/phases/idi-11-decard-and-hairline-dividers/idi-11-01-SUMMARY.md"
      provides: "三份运行时读数的原始输出抄录(检查器 INFO 行原文)+ 两条承重注释改写前后的对照"
      contains: "INFO c1 #session-panel 原始读数"

  key_links:
    - from: "`frontend/style.css` 围栏内 `--color-surface-page` 的声明值"
      to: "`html, body` 的 `background` 与四个 `#main-pane > section` 的 `background`"
      via: "两条规则都 `var()` 引用同一个令牌 ⇒ 改一处值即可让页面与面板同色(这正是「统一面」的机械形态)"
      pattern: "--color-surface-page: var\\(--white\\);"
    - from: "`frontend/style.css` 的 `#doc-panel` 规则体"
      to: "围栏内 `--color-border-subtle: var(--radix-gray-6);`"
      via: "`border-left: 1px solid var(--color-border-subtle)` —— 盒内手段,零新增 DOM、零位移"
      pattern: "border-left: 1px solid var\\(--color-border-subtle\\);"
    - from: "`frontend/style.css` 的 `#main-pane > section + section` 规则块"
      to: "围栏内 `--color-border-subtle: var(--radix-gray-6);`"
      via: "`border-top: 1px solid var(--color-border-subtle)` —— 与竖线同令牌,零新增颜色值"
      pattern: "border-top: 1px solid var\\(--color-border-subtle\\);"
    - from: "四条承重注释(规则体上方)"
      to: "`frontend/style.css` 的规则体本身"
      via: "就地改写,注释与代码同一次提交 —— 留下一条与代码矛盾的注释正是本仓库反复付过代价的形态"
      pattern: "Phase 11"

  prohibitions:
    - statement: "不得把「去卡片」做成「删掉全站所有边界」。本阶段移除的是**五个容器**的边界,交互控件(按钮 / 输入框 / `select` / `#check-switcher` / `.overlay-card`)必须保留各自的圆角与边界,`.panel-header` 的活动标记(三条 `#…-panel:not(.hidden) .panel-header` 规则上的 `inset 3px 0 0`)必须存活 —— 它是去卡片后仅存的活动态视觉线索。验收靠**同一份运行时读数里的对照组**,不靠「我认为没动」"
      status: active
      verification: flagged
    - statement: "不得把统一面做成「压平所有层次」。SURF-02 是把卡片档并回页面档,不是把 `--color-surface`(gray-2 内陷面)一并抹掉;内陷面塌掉会让控件与 `#latest-check` 失去边界,并让下游 c3 的改写判据失去对象"
      status: active
      verification: flagged
    - statement: "不得为了让门绿、或为了让某个旧读数继续成立,而删除 / 降级 / 放宽任何断言、阈值或判据,也不得回退已裁定的产品改动。本阶段 `check-09` 的 c1..c4 反转后**必红** —— 那正是门在正确工作的证据;判据只能改写为断言新契约(计划 03),不得删除、不得降级为恒真、不得只断言「规则被写下了」。同理,`check-05 --item 8` 的 sticky 余量若因本阶段移除 1px 上边框而变化,只更新读数与成因登记,**不得为了让旧数字成立而把 1px 加回去**(D-11-16)"
      status: active
      verification: flagged

  assumptions:
    # spec-less probe fallback(§7.95,EDGE_ABSENT=1 / PROHIB_ABSENT=1):探针在 9 条阶段需求上产出
    # 11 行,全部 unresolved —— 8 条需求被英文 cue 判为 unclassified(中文散文 ⇒ 分类漏判,
    # 不是「无边界」的裁定),REG-03 另有 3 行已分类但未决(adjacency / empty / ordering)。
    # 按 §A/§C:unclassified 行**永不**用 backstop 自动消解 ⇒ 每一行在此显式登记为 flagged assumption。
    # 无静默丢弃的等式:11 = 0(authored into must_haves.truths)+ 11(此处显式登记)。
    # 编排器给出的原始行载荷是未展开的占位符,故下面的逐行枚举由它给出的摘要重建;
    # 若下游需要原始行文本,须重跑该探针,不得把本枚举当作原始输出。
    - statement: "SURF-01 的边界探针行判为 `unclassified — review manually`(英文 cue 对中文需求散文的分类漏判)。它**未**被消解:该需求的判据由本计划的 must_haves.truths 与计划 03 的 c1 改写独立承载,但那是**计划的覆盖**,不是探针对该行的分类结论"
      status: flagged
      verification: flagged
    - statement: "SURF-02 的边界探针行判为 `unclassified — review manually`(同上)。未被消解;其判据由本计划 must_haves.truths(统一面 == 面板底色、内陷面仍更暗)与计划 03 的 c3 改写承载"
      status: flagged
      verification: flagged
    - statement: "SURF-03 的边界探针行判为 `unclassified — review manually`(同上)。未被消解;其判据由本计划 must_haves.truths(灰缝归零、侧沟由同色消除)与计划 03 的 c4 改写承载"
      status: flagged
      verification: flagged
    - statement: "DIV-01 的边界探针行判为 `unclassified — review manually`(同上)。未被消解;其判据由本计划 must_haves.truths(竖线跨满面板可视高度)与计划 03 的 c4 几何断言承载"
      status: flagged
      verification: flagged
    - statement: "DIV-02 的边界探针行判为 `unclassified — review manually`(同上)。未被消解;其判据由本计划 must_haves.truths(左栏面板之间恰 3 条横线、第一个面板顶部不画)与计划 03 的 c4 承载"
      status: flagged
      verification: flagged
    - statement: "DIV-03 的边界探针行判为 `unclassified — review manually`(同上)。未被消解;其判据由本计划 must_haves.truths(线宽 1px、取既有语义令牌、零新增颜色值)与计划 03 的双断言承载"
      status: flagged
      verification: flagged
    - statement: "REG-01 的边界探针行判为 `unclassified — review manually`(同上)。未被消解;其判据由计划 03 的「断言总数 >= 46 + 六条变异各有一条真实 FAIL 读数」承载"
      status: flagged
      verification: flagged
    - statement: "REG-02 的边界探针行判为 `unclassified — review manually`(同上)。未被消解;其判据由计划 02 的「重归属而非刷新 + 53 对规模不变 + 阈值逐字节相同」承载"
      status: flagged
      verification: flagged
    - statement: "REG-03 的探针行 #1(edge kind `adjacency`,已分类但 unresolved)。未被消解:探针问的是「相邻/邻接关系」在判据里是否被穷尽,而 REG-03 的判据是单条容差断言(`abs(header.top - panel.top) <= 1.0`)加一次读数登记。计划 04 只做「复测 + 登记」,不新增邻接类断言 —— 若评审者认为需要,那是范围扩张,须先裁定"
      status: flagged
      verification: flagged
    - statement: "REG-03 的探针行 #2(edge kind `empty`,已分类但 unresolved)。未被消解:探针问的是「空集/空输入」边界,而 REG-03 的断言在 `#doc-panel` / `#doc-panel-header` 都存在时才有对象。计划 04 未新增「元素缺失时如何处置」的断言;`check-05` 既有的 `blocked()` 分支在元素缺失时记 BLOCKED(不记 PASS),这是既有行为而非本阶段新增的保证"
      status: flagged
      verification: flagged
    - statement: "REG-03 的探针行 #3(edge kind `ordering`,已分类但 unresolved)。未被消解:探针问的是「顺序关系」是否被断言,而 REG-03 不涉及任何序关系断言(`check-02` 的 `ORDER` 条目归 REG-02,且本阶段不改它)。计划 04 未新增序关系断言"
      status: flagged
      verification: flagged
---

<objective>
把 v1.15 Phase 9 落地的卡片语言**整体反转**为 ChatGPT 式的「连续白面 + 1px 发丝分隔线」—— 这是本阶段的**反转本体**,是 `frontend/style.css` 一个文件上的一次就地改写。

Purpose: 用户 2026-09-28 看过 Phase 9 的成品后逐字裁定:「分块太割裂了,完全没有联动性…chatgpt 的界面就是一根细的衬线来分割不同的分区,我们的确实很大的一块」。反转对象是**一次已 shipped 的用户裁定**(D-9-1 / D-9-2 / D-9-3),本阶段**不重开**底色关系、密度、圆角与卡片语言这四项决策,只执行反转。

为什么 SURF 与 DIV **必须同一次落地**:只去卡片不留线,等于把 4 个面板之间原本承载层次的 12px 灰缝一并抹掉、分区彻底消失 —— 那是比任一终点都差的中间态。故本计划一次交付连续面 + 统一面 + 灰缝归零 + 两条发丝线。

**本计划关闭的需求:** SURF-01、SURF-02、SURF-03、DIV-01、DIV-02、DIV-03。

**本计划不触碰:** `--color-surface-card` / `--shadow-card` 两个令牌的**删除**(属计划 02 —— 反转后它们消费者归零,按围栏自己的规则处置);`scripts/check-02-contrast.py` 的 PAIR 清单重归属与重算(计划 02);`scripts/check-09-idi09-validation.py` 的 c1..c4 承重改写(计划 03);`scripts/check-05-ui-uat.py` 的任何一行(计划 04);`G1-01` / `REG-04` / `VIS-01`(归 Phase 12);`G2`、`999.2`、暗色模式、Nyquist 缺口、图标与空状态、`.overlay-card` 底色(**全部在 Out of Scope**);`frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**`(零字节)。

**⚠ 执行本计划时 `scripts/check-09-idi09-validation.py --item c1,c2,c4` 会报 FAIL —— 这是设计预期,不是回归。** 该门断言的正是本阶段要移除的卡片语言。它的 `INFO` 行逐条打印真实浏览器里的 computed style 原始读数,故本计划**把那些 INFO 行当作运行时证据**,而不是把门的整体裁决当作证据。**不要在本计划里修改 `check-09`** —— 计划 03 拥有它。

**执行前基线(规划期已在 HEAD 上实测,执行器须复核):**

| 检查 | 规划期在 HEAD 上的实测结果 |
|---|---|
| `bash scripts/check-01-token-conformance.sh` | exit 0 |
| `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`(清单 53 对 + 1 条 `ORDER`;其中含 `PASS  4.77  --color-marker-active on --color-surface-card` 与 `PASS  3.32  --color-border-strong on --color-surface-card`) |
| `bash scripts/check-03-hidden-uniqueness.sh` | exit 0 |
| `bash scripts/check-04-important-count.sh` | exit 0 |
| `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4` | `exit=0`;`c1 PASS 26 条断言` / `c2 PASS 13` / `c3 PASS 3` / `c4 PASS 4`(**合计 46**) |
| `.venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled` | `item 8: PASS (13 条断言,0 FAIL,0 BLOCKED)`;`INFO item8 sticky 原始数值: … header={'top': 1, …} panel={'top': 0, 'bottom': 900, 'left': 1008, 'right': 1440}`;断言 `abs(header.top - panel.top) <= 1.0` 的实测值 **`1.000px`** |
| `grep -o '/\* PAIR' frontend/style.css \| wc -l` / `grep -o '/\* ORDER' …` | `53` / `1` |

**HEAD 上要被改写的规则(逐字,以选择器文本为锚 —— 行号会漂,不要按行号定位):**

- `html, body` 规则体内 `background: var(--color-surface-page);`
- `#main-pane` 规则体内:`gap: var(--space-3);` / `overflow-y: auto;` / `align-items: center;` / `min-width: 0;`(后三条**逐字保留**)
- `#main-pane > section` 规则体内:`width: 100%;` / `max-width: 768px;` / `background: var(--color-surface-card);` / `border: 1px solid var(--color-border);` / `border-radius: var(--radius-md);` / `box-shadow: var(--shadow-card);`(前两条**逐字保留**)
- `#doc-panel` 规则体内:`overflow-y: auto;` / `border: 1px solid var(--color-border);` / `background: var(--color-surface-card);` / `border-radius: var(--radius-md);` / `box-shadow: var(--shadow-card);` / `min-width: 0;`(`overflow-y` 与 `min-width` **逐字保留**)
- `#doc-panel-header` 规则体内:`position: sticky;` / `top: 0;` / `background: var(--color-surface-card);` / `border-radius: 0;`(后两条中的 `border-radius: 0` **逐字保留**)
- `.panel-header` 规则体内:`border-radius: var(--radius-md);`(**只改这一行**)

**相关令牌(围栏内,值取自磁盘):** `--color-surface-page: var(--radix-gray-3)`(HEAD 值,`#f0f0f0`)、`--white: #ffffff`、`--color-surface: var(--radix-gray-2)`(`#f9f9f9` = `rgb(249, 249, 249)`)、`--color-border: var(--radix-gray-7)`(`#cecece`)、`--color-border-subtle: var(--radix-gray-6)`(`#d9d9d9` = `rgb(217, 217, 217)`)、`--radius-md: 10px`、`--space-3: 12px`、`--space-4: 16px`。

**DOM 顺序(已核实 `frontend/index.html`):** `#main-pane` 的四个直接子 `section` 依次是 `#session-panel` → `#annotations-panel` → `#checks-panel` → `#ai-panel`;`#annotations-panel` 与 `#checks-panel` 在 p1 样本带 `.hidden`(相邻选择器按 DOM 相邻判定,与 `display` 无关)。`#doc-panel` 是 `#main-pane` 的**兄弟**(两者同为 `#app` 的子元素)⇒ `#main-pane > section + section` 永不匹配它。

Output: `frontend/style.css` 的统一面换值 + 五容器就地去边界 + 灰缝归零 + 两条发丝线 + 四段承重注释改写;三份真实浏览器运行时读数的原始输出(供计划 03 的判据改写与 SUMMARY 取证)。
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
@.planning/milestones/v1.15-phases/idi-09-card-containers/09-CONTEXT.md
@.planning/milestones/v1.15-phases/idi-10-tables-and-radius-scale/10-CONTEXT.md
@frontend/style.css
@frontend/index.html
@scripts/check-09-idi09-validation.py
@scripts/check-05-ui-uat.py
</context>

## Artifacts this phase produces

> 本节的用途:**plan-review-convergence 的 source-grounding pass 读它,把本阶段新建的符号从漂移校验里排除**。
> 本节列出**全阶段**(四个计划)的产出;每个计划的 SUMMARY 只登记自己那部分。

**新增文件:零。** 本阶段不新建任何源码文件、不新建门脚本、不新建探针 —— 改动面是 `frontend/style.css` + 三个**既有**门脚本(`check-09` / `check-02` 的清单在 style.css 内 / `check-05`)。

**新增目录:** `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/`(计划 04;一个门一个日志文件,文件名即门的名字 —— Phase 9 的同形先例)。

**新增符号:**

| # | 符号 | 种类 | 计划 | 用途 |
|---|---|---|---|---|
| 1 | `fence_text()` | 函数,`scripts/check-09-idi09-validation.py` | 03 | 返回两行 `===== DESIGN TOKENS: START/END` 之间的文本(含标记行自身)。**逐字照抄 `scripts/check-10-idi10-validation.py` 的同名函数** —— `check-09` 目前没有它 |
| 2 | `FENCE_START` / `FENCE_END` | 模块常量,`check-09` | 03 | `"===== DESIGN TOKENS: START ====="` / `"===== DESIGN TOKENS: END ====="`,与 `check-10` 逐字相同 |
| 3 | `STYLE_CSS` | 模块常量,`check-09` | 03 | `ROOT / "frontend" / "style.css"`,供源码文本级残留断言 |
| 4 | `r1 [源码] 围栏内 <被删令牌> 声明残留计数 == 0` × **2** | 断言标签,`check-09` | 03 | **两条专用**残留断言(每个被删令牌一条),照 `scripts/check-10-idi10-validation.py:402-409` 的 `r1` 同型。**不是**一条通用围栏消费断言(那才是 G2,已由用户排除在 v1.16 范围外) |
| 5 | `HAIRLINE_LITERAL` | 模块常量,`check-09` | 03 | `"rgb(217, 217, 217)"`(gray-6 字面量)。照 `check-10` 的 `TH_BORDER_LITERAL` 同型,用于发丝线颜色的**字面量半条**断言 |

**删除的既有符号(CSS 自定义属性声明,计划 02):**

| # | 符号 | 锚点 | 计划 | 动作 |
|---|---|---|---|---|
| 6 | `--color-surface-card: var(--white);` | Tier-2「card container language」注释块之后 | 02 | **删除**该行(3 处消费者 `#main-pane > section` / `#doc-panel` / `#doc-panel-header` 已在计划 01 搬走) |
| 7 | `--shadow-card: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04);` | 紧随 #6 之后 | 02 | **删除**该行(2 处消费者 `#main-pane > section` / `#doc-panel` 已在计划 01 搬走) |

**新增规则块(规则体,计划 01):**

| # | 符号 | 锚点(选择器文本) | 计划 | 动作 |
|---|---|---|---|---|
| 8 | `#main-pane > section + section` | **紧随** `#main-pane > section` 规则块之后 | 01 | **新增**规则块,规则体只一条:`border-top: 1px solid var(--color-border-subtle);`(左栏面板之间的横线,恰命中后三个 section) |

**就地改写的既有规则(规则块位置与源码顺序逐字不变,计划 01):**

| # | 符号 | 锚点(选择器文本) | 动作 |
|---|---|---|---|
| 9 | `--color-surface-page` 的**值** | 围栏内 `/* Phase 9 sinks the page one step … */` 注释之后的声明行 | `var(--radix-gray-3)` → `var(--white)`;其上方注释同步改写 |
| 10 | `#main-pane` 的 `gap` | `#main-pane` 规则体 | `var(--space-3)` → `0`;其上方注释同步改写 |
| 11 | `#main-pane > section` 的四条声明 | `#main-pane > section` 规则体 | `background` → `var(--color-surface-page)`;`border: 1px solid var(--color-border)` → `border: none`;`border-radius` → `0`;`box-shadow` → `none`;`width` / `max-width` 逐字保留;其上方 ① / ② / ③ 注释同步改写 |
| 12 | `#doc-panel` 的四条声明 | `#doc-panel` 规则体 | `border: 1px solid var(--color-border)` → `border-left: 1px solid var(--color-border-subtle)`;`background` → `var(--color-surface-page)`;**删除** `border-radius` 与 `box-shadow` 两行;`overflow-y` / `min-width` 逐字保留;其上方 Phase 9 注释同步改写 |
| 13 | `#doc-panel-header` 的 `background` | `#doc-panel-header` 规则体 | `var(--color-surface-card)` → `var(--color-surface-page)`;`position` / `top` / `border-radius: 0` 逐字保留;其上方注释同步改写 |
| 14 | `.panel-header` 的 `border-radius` | `.panel-header` 规则体 | `var(--radius-md)` → `0` |

**明确不产生的新符号:** 零新增 CSS 自定义属性、零新增颜色值、零新增 tier-1 primitive、零新增 PAIR / ORDER 条目、零新依赖、零构建步骤、零新应用文件、`frontend/app.js` / `index.html` / `vendor/` / `backend/**` 零字节改动。

## 探针未决边界的显式登记(spec-less probe fallback §7.95)

本阶段无 `*-SPEC.md`(`EDGE_ABSENT=1` / `PROHIB_ABSENT=1`),故走 §7.95 的降级协议。确定性边界探针在 9 条阶段需求上产出 **11 行,全部 unresolved**:

- **8 行**来自 8 条需求被英文 cue 判为 `unclassified — review manually`(SURF-01/02/03、DIV-01/02/03、REG-01、REG-02)。**这是分类漏判,不是「无边界」的裁定** —— 探针的 cue 是英文,而这些需求是中文散文(本项目已记录的同型失真:英文 cue 对中文散文分类不可靠)。
- **3 行**来自 `REG-03`,已分类但未决,edge kind 分别为 `adjacency` / `empty` / `ordering`。

按 §A/§C:`unclassified` 行**永不**用 backstop 自动消解。**11 行全部**已作为 `must_haves.assumptions` 的 **11 条 flagged assumption** 显式登记(descriptor-less,故各自处置为 `{status:'unverified', flagged:true}`)。**无静默丢弃的等式:11 = 0(写进 `must_haves.truths`)+ 11(显式登记为 flagged assumption)。**

**⚠ 两处诚实性声明:**

1. 编排器提供的原始行载荷是**未展开的占位符**,故 `must_haves.assumptions` 里的逐行枚举由它给出的**摘要**重建(8 条 unclassified 逐需求一条 + REG-03 三条按 edge kind)。若下游需要**原始行文本**,须重跑该探针 —— **不得**把本枚举当作原始输出。
2. 本计划与计划 03/04 的 `must_haves` **独立覆盖**了这些需求的可观测判据(那是**计划的覆盖**),但**那不是**探针对该行的分类结论 —— 两者不得混为一谈,也不得据此把任一行标为 resolved。

`PROHIB_ABSENT=1` 另触发 §B 的禁令回忆(散文通过,无引擎)。幸存项已写进各计划的 `must_haves.prohibitions`(descriptor-less,3 条):**不得把「去卡片」做成「删掉全站所有边界」**、**不得把统一面做成「压平所有层次」**、**不得为了让门绿或让旧读数成立而删除/降级/放宽判据或回退已裁定的产品改动**。按 §B 的口径,常规工程项与既定安全/合规项已被丢弃(后者只留一行面包屑:本阶段零安装、零新增依赖,`frontend/vendor/` 仍只有 `marked.min.js`)。

## 波次与依赖形状(本阶段的真实约束,不是保守)

| 波次 | 计划 | 落点 | 为什么必须在这个位置 |
|---|---|---|---|
| 1 | `idi-11-01`(本计划) | `frontend/style.css` 反转本体(连续面 + 统一面 + 灰缝 + 发丝线) | 反转本体是一切的下游:计划 02 删的令牌、计划 03 改写的判据、计划 04 复跑的门,描述的都是这次改动的**结果** |
| 2 | `idi-11-02` | 删两个被孤立的令牌 + `check-02` 清单重归属与重算 | 与计划 01 同文件 ⇒ 必须错开波次。放在波次 2 是因为**消费者必须先搬走、令牌才能删**(否则 `check-02` 的 `resolve()` 会对未声明令牌 `sys.exit(1)`) |
| 3 | `idi-11-03` | `check-09` 的 c1..c4 承重改写 + 六条变异测试 | 判据断言的是**改动后的**渲染状态,故必须在 `style.css` 定型(波次 1+2)之后才能改写并验证 |
| 4 | `idi-11-04` | `check-05` 的 `.hint` 期望侧重登记 + `--item 8` 复测 + 五条浏览器门与四静态门复跑 | 复跑必须看到**全部**改动;且 `check-05` 的改法与 `check-09` 的改写都在同一批「门禁同步」里,复跑是它们的收口证据 |

**本阶段为什么没有更多并行:** 四个计划里前两个同文件(`frontend/style.css`),后两个各自独占一个门脚本但**都以「style.css 已定型」为前提**。`execute-phase` 的同波次规则要求同波次计划的 `files_modified` 零重叠 —— 这是「纯 CSS + 门脚本阶段」的定义,不是可以优化的地方。

<tasks>

<task type="tracer">
  <name>Task 1: 统一面 + 左栏面板去边界 —— 单条路径端到端(运行时读数证明)</name>
  <files>frontend/style.css</files>
  <reversibility rating="costly">撤销要连带重算 `check-02` 的六条页面地面 PAIR 与其 Phase 9 登记账目,并重写 c3 判据(D-11-1 的 Reversibility 评级)。</reversibility>
  <read_first>
    - `frontend/style.css` 的 `html, body` 规则 —— `background: var(--color-surface-page);` 是 `--color-surface-page` 的**唯一**消费者(它是全页底色的唯一出口)
    - `frontend/style.css` 围栏内 `--color-surface-page` 声明行与其上方那段 `/* Phase 9 sinks the page one step … */` 注释(**本任务要改写的对象之一**;注意该注释在 `:126` 处点名了一个被计划 02 删除的令牌 —— 本任务**只改值与其三档叙事**,令牌名与清单归属留给计划 02)
    - `frontend/style.css` 围栏内 `--white: #ffffff;` 与 `--radix-gray-3: #f0f0f0;`、`--radix-gray-2: #f9f9f9;`、`--color-surface: var(--radix-gray-2);`
    - `frontend/style.css` 的 `#main-pane > section` 规则块**及其上方 ① / ② / ③ 三段注释**(`:736-750` 附近)—— **本任务的改写目标**。逐字读 ① 的边界色依据、② 的「`.panel-header` 自身的 border-radius 已是 `--radius-md`」前提、③ 的阴影依据
    - `frontend/style.css` 的 `#main-pane` 规则块(确认 `gap` / `overflow-y` / `align-items` / `min-width` 四行的当前形态,本任务**只动 `gap` 之外的都不动**——`gap` 属 Task 2)
    - `frontend/index.html` 的 `main#main-pane` 段 —— 确认四个 `section` 的 DOM 顺序与 id(`#session-panel` 是第一个)
    - `frontend/style.css` 的 `.panel-header` 规则块与三条活动标记规则(`#session-panel:not(.hidden) .panel-header` 等,规则体为 `box-shadow: inset 3px 0 0 var(--color-marker-active);`)及其上方注释 —— 该注释逐字记着「用 `box-shadow` 而非 `border-left`,零布局位移」,这是本阶段发丝线走盒内手段的**先例**
    - `scripts/check-09-idi09-validation.py` 的 `c1()` 函数全文 —— 逐字读它的 `info()` 行格式(`INFO c1 {sel} 原始读数 background-color=… border-top-left-radius=… border-top=… box-shadow=…`),本任务的运行时证据就取这些行。**本任务一行都不改它**
    - `.planning/phases/idi-11-decard-and-hairline-dividers/11-CONTEXT.md` §D-11-1 / §D-11-2 / §D-11-5 / §D-11-7 与 §「Claude's Discretion」
    - `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-PATTERNS.md` §"Analog A" / §"Analog C" / §"The unified-surface declaration" / §"The five container rules to rewrite, verbatim"
    - `.planning/ROADMAP.md` §`### Phase 11:` 的 Goal / Deliverables 1、2 / Success Criteria 1、2 / Avoids 第 2、4、6 条
  </read_first>
  <action>
    **第 1 步 —— 统一面换值。**

    在围栏内把 `--color-surface-page` 的声明值由 `var(--radix-gray-3)` 就地改写为 `var(--white)`。**只改值**,声明名与位置不动。

    同步改写其上方那段 `Phase 9 sinks the page one step …` 注释中**与三档 elevation 叙事直接相关**的部分:原文把页面描述成三级刻度的最低档(`gray-3 页面 < gray-2 内陷面 < 白卡片`),反转后是**两级**(统一面白 > 内陷面 gray-2)。注释要写清:(a) 这次是**就地改写值**而不是新增令牌;(b) `--radix-gray-3` 仍有 `--color-surface-sunken` 与 `--color-surface-hover` 两个消费者 ⇒ 换值**不会**造出新的零消费 primitive;(c) 反转后统一面与内陷面的亮度序仍成立(白 1.000000 > gray-2 0.947307),故控件与 `#latest-check` 仍读作内陷。

    ⚠ **围栏内注释禁令(本任务加的任何围栏内注释都适用):** 不得出现「令牌名 + 冒号」形态 —— `scripts/check-02-contrast.py` 的 `DECL_RE` 扫**围栏全文含注释**,`parse_decls` 让**最后一个**匹配胜出,写成 `--radix-gray-12: …` 会被当成一条值不可解析的声明而让 `resolve()` `exit 1`。

    **第 2 步 —— `#main-pane > section` 就地改写为「无边界」。**

    把规则体的四条声明逐条就地改写(不是追加覆盖):

    - `background: var(--color-surface-card);` → `background: var(--color-surface-page);`
    - `border: 1px solid var(--color-border);` → `border: none;`
    - `border-radius: var(--radius-md);` → `border-radius: 0;`
    - `box-shadow: var(--shadow-card);` → `box-shadow: none;`

    `width: 100%;` 与 `max-width: 768px;` 两行**逐字保留**(D-11-5:768px 居中内容列是**保留**的,只有它两侧的沟变得不可见)。

    **第 3 步 —— 改写该规则上方的 ① / ② / ③ 注释。**

    这三段是 Phase 9 的承重理由,反转后有两条前提**死掉**,必须**改写、不得删除**(留下一条与代码矛盾的注释正是本仓库反复付过代价的形态):

    - ① 边界色取 `--color-border`(gray-7)的依据 —— 随 `border: none` 一起消失;新注释要记下「反转后本容器不再绘制边界,边界色依据整段作废」;
    - ② 的 `overflow: hidden` 讨论里那句「左栏卡片**不需要**它,因为 `.panel-header` 自身的 border-radius 已是 `--radius-md`」—— **该前提在本计划 Task 2 把 `.panel-header` 的圆角归零时死掉**(C-9)。新注释不得留一条断言假前提的句子;
    - ③ 的阴影依据 —— 随 `box-shadow: none` 一起消失。

    新注释必须逐条记下:(a) 这是**就地改写**,不是追加覆盖(留下一条已死的 `border` / `box-shadow` 会让注释与代码互相矛盾 —— Phase 9 对 `#doc-panel` 的 `border-left`、Phase 10 对表格 `border` 用的是同一纪律);(b) `border: none` 与紧随 Task 3 的 `#main-pane > section + section { border-top: … }` 是**一对** —— 前者去掉四边,后者只给后三个 section 加回一条上边线;(c) ② 段中「`transform` / `filter` / `will-change` / `contain` / `perspective` / `opacity` / `position` / `z-index` / `overflow` 九项禁令」**继续有效**(`#stream-banner` 仍是 `#doc-panel` 的后代且 `position: fixed`),只是它的第二半理由换了说法;(d) `width` / `max-width` 是**保留**的声明,不是死代码 —— 它们仍在工作(定位置 / 控行长),侧沟是被同色消除的,不是被删除声明消除的。

    **第 4 步 —— 运行时读数(本 tracer 的端到端证明)。**

    跑 `.venv/bin/python scripts/check-09-idi09-validation.py --item c1`。**该门会报 FAIL —— 这是设计预期**(它断言的正是被本计划移除的卡片语言),但它逐条打印 `INFO c1 {sel} 原始读数 …`,那就是真实浏览器里的 computed style 读数。把 `#session-panel` 那一行的**原文**抄进 SUMMARY。

    要求读到的四项:`background-color=rgb(255, 255, 255)`、`border-top-left-radius=0px`、`border-top=0px none`、`box-shadow=none`。**不要为了让门变绿而修改 `check-09`** —— 计划 03 拥有它。

    同时跑 `bash scripts/check-01-token-conformance.sh` / `.venv/bin/python scripts/check-02-contrast.py` / `bash scripts/check-03-hidden-uniqueness.sh` / `bash scripts/check-04-important-count.sh`,四条都必须在**本步结束时**仍然绿(`check-02` 此刻仍应 `PASS: 0 failures` —— 两个待删令牌尚未删除,清单条目仍可解析)。

    **第 5 步 —— 不触碰范围之外的一切。** 不改 `#main-pane` 的 `gap` / `overflow-y` / `align-items` / `min-width`(Task 2 / 保留);不改 `#doc-panel` / `#doc-panel-header` / `.panel-header`(Task 2);不删任何令牌(计划 02);不改任何 PAIR / ORDER 条目(计划 02);不改 `scripts/` 下任何文件;不改 `frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**`。
  </action>
  <verify>
    <automated>grep -cF -- '--color-surface-page: var(--white);' frontend/style.css</automated>
    <fails_when>the count is not exactly "1" (the token's value was not rewritten in place)</fails_when>
    <automated>awk '/^#main-pane > section \{/{f=1} f{print} f&&/^\}/{exit}' frontend/style.css</automated>
    <fails_when>the printed rule body does not contain all of `background: var(--color-surface-page);`, `border: none;`, `border-radius: 0;`, `box-shadow: none;`, `width: 100%;`, `max-width: 768px;`, or still contains `var(--color-surface-card)`, `var(--color-border)`, `var(--radius-md)`, `var(--shadow-card)`</fails_when>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c1 2>&1 | grep -F 'INFO c1 #session-panel 原始读数'</automated>
    <fails_when>no such line is printed, or the printed line lacks any of `background-color=rgb(255, 255, 255)`, `border-top-left-radius=0px`, `border-top=0px none`, `box-shadow=none`. (check-09 exits non-zero and prints FAIL verdicts here because it still asserts the Phase 9 card contract — that is EXPECTED and is not a failure of this task; do not edit check-09 in this plan)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>non-zero exit for any of the three, or any of the three not printing exactly "PASS"</fails_when>
    <automated>.venv/bin/python scripts/check-02-contrast.py</automated>
    <fails_when>non-zero exit, or any line beginning with "FAIL", or the final line not exactly "PASS: 0 failures"</fails_when>
    <automated>git status --porcelain frontend/ backend/</automated>
    <fails_when>output contains any path other than "frontend/style.css", or output is empty</fails_when>
  </verify>
  <acceptance_criteria>
    - `--color-surface-page` 的声明值恰为 `var(--white)`,声明行位置与声明名逐字未动;其上方注释已就地改写为两级刻度叙事,且**未新增**任何「令牌名 + 冒号」形态。
    - `#main-pane > section` 规则体的选择器文本与源码位置逐字未动;声明集 = HEAD 的 6 条,其中 4 条就地改写(`background` / `border` / `border-radius` / `box-shadow`)、2 条逐字保留(`width` / `max-width`)。
    - 该规则体内**不再出现** `var(--color-surface-card)` / `var(--color-border)` / `var(--radius-md)` / `var(--shadow-card)` 任何一个 —— 四条旧声明是被改写掉的,不是被后续规则覆盖的。
    - 规则体上方的 ① / ② / ③ 注释已改写:① 与 ③ 的旧依据被显式记为「随边界/阴影移除而作废」,② 中「`.panel-header` 自身的 border-radius 已是 `--radius-md`」这句**已不存在**(该前提在 Task 2 会死掉);九项属性禁令与「`width` / `max-width` 是保留的声明,不是死代码」两段仍在。
    - `check-09 --item c1` 的输出里含一行 `INFO c1 #session-panel 原始读数`,其原文含 `background-color=rgb(255, 255, 255)`、`border-top-left-radius=0px`、`border-top=0px none`、`box-shadow=none`;该行原文被抄进 SUMMARY。
    - `bash scripts/check-01-token-conformance.sh` / `bash scripts/check-03-hidden-uniqueness.sh` / `bash scripts/check-04-important-count.sh` 各打印 `PASS`;`.venv/bin/python scripts/check-02-contrast.py` 打印 `PASS: 0 failures`(此刻两个待删令牌仍在,清单仍可解析)。
    - `git status --porcelain frontend/ backend/` 仅列出 `frontend/style.css`。
  </acceptance_criteria>
  <done>统一面已换值为 `var(--white)`,左栏四个面板共用的一条规则已就地改写为「无边界 + 统一底色」,`width` / `max-width` 逐字保留,三段承重注释已随代码改写;`check-09 --item c1` 的 INFO 行给出真实浏览器读数(`rgb(255, 255, 255)` / `0px` / `0px none` / `none`)并已入册;四条静态门全绿。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 2: `#doc-panel` / `#doc-panel-header` / `.panel-header` / `#main-pane` 四处就地改写(竖线落位 + 灰缝归零 + 圆角归零)</name>
  <files>frontend/style.css</files>
  <reversibility rating="costly">`#doc-panel` 的底色归属与令牌删除是同一笔账(计划 02 删 `--color-surface-card`);撤销要恢复两条声明、删除残留断言、并把 2 条 PAIR 的地面标签改回去。</reversibility>
  <read_first>
    - `frontend/style.css` 的 `#doc-panel` 规则块**及其上方 Phase 9 注释**(逐字读「原 `border-left: 1px` 的单边凹陷读感由四边边界 + 卡片底色取代,故这里是就地改写那条声明,不是追加一条 `border` 覆盖它」与「`overflow-y: auto` 是**承重的滚动契约**,不得删除」两段)—— **本任务的改写目标**
    - `frontend/style.css` 的 `#doc-panel.collapsed { flex-basis: …; overflow: hidden; }` 规则 —— 48px 竖条态保留左侧发丝线,**本任务不动它**
    - `frontend/style.css` 的 `#doc-panel-header` 规则块**及其上方注释**(逐字读「背景是必需的,不是可选:`.panel-header` 规则体内没有任何 background 声明」与「表头底色与卡片底色同值(都取卡片令牌)」两句;后者是 C-9 点名**必须改写**的死前提)
    - `frontend/style.css` 的 `.panel-header` 规则块与三条活动标记规则(`box-shadow: inset 3px 0 0 var(--color-marker-active);`)及其上方「用 box-shadow 而非 border-left,零布局位移」的注释
    - `frontend/style.css` 的 `#main-pane` 规则块**及其上方 Phase 9 / D-9-2 注释**(逐字读「间隙里透出的是页面底色(gray-3),这正是「白卡片浮在灰页面之上」的可见形态」)
    - `frontend/index.html` 的 `aside#doc-panel` / `header.panel-header#doc-panel-header` / `div#doc-panel-body` 段
    - `scripts/check-09-idi09-validation.py` 的 `c2()` 与 `c4()` 全文 —— 逐字读它们的 `info()` 行格式,本任务的运行时证据取这些行。**本任务一行都不改它**
    - `scripts/check-05-ui-uat.py` 的 `[p1] sticky 把 #doc-panel-header 钉在 #doc-panel 顶部(<=1px)` 断言(`abs(hp["top"] - pp["top"]) <= 1.0`)—— **本任务的改动会把它从 `1.000px` 变成 `0.000px`**;该断言是**容差**不是等值,故仍通过。本任务只读它、不改它
    - `.planning/phases/idi-11-decard-and-hairline-dividers/11-CONTEXT.md` §D-11-5 / §D-11-6 / §D-11-7 / §D-11-9 / §「连带后果」两条
    - `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-PATTERNS.md` §"The activity marker that must survive" 与 §"Analog A"
  </read_first>
  <action>
    **第 1 步 —— `#doc-panel`:四边边界收成单边竖线。**

    在 `#doc-panel` 规则体内就地改写:

    - `border: 1px solid var(--color-border);` → `border-left: 1px solid var(--color-border-subtle);`
    - `background: var(--color-surface-card);` → `background: var(--color-surface-page);`
    - **删除** `border-radius: var(--radius-md);` 这一行
    - **删除** `box-shadow: var(--shadow-card);` 这一行

    `overflow-y: auto;` 与 `min-width: 0;` **逐字保留**。`overflow-y` 是**承重的滚动契约**,不得删除:它是右列的滚动者,L-1 的 sticky 表头依赖 `#doc-panel` 仍是最近的**可滚祖先**。删除它的真实代价是打破 L-1(不是滚动者普查 —— 见下方「为什么不能写『期望值是 4』」)。

    **为什么竖线取 `border-left` 而不是别的手段:** 它零新增 DOM 元素、零位移,且天然跨满 `#doc-panel` 整高(`#app` 是 `display: flex; height: 100vh` 且默认 `align-items: stretch`)。用 `margin` 或额外元素撑高会移动既有几何,并可能打在 `check-05 --item 9` 的 L-5 clearance 普查与 `--item 8` 的 badge × banner 几何上。

    **⚠ 竖线**只能**落 `border-left`,不得留任何顶侧 border/offset**:`check-05 --item 8` 的 sticky 断言 `abs(header.top - panel.top) <= 1.0` 今天**恰好坐在容差边界上**(实测 `1.000px`,成因正是 Phase 9 给 `#doc-panel` 加的那条 1px **上**边框)。移除该上边框会让读数降到 `0.000px`(仍 `<= 1.0` ⇒ 仍 PASS);但任何残留的顶侧 border/offset 都会把读数推过 `1.0` 并让 item 8 变红。这条边界由计划 04 的 REG-03 复测登记。

    同步改写其上方注释:原文那句「原 `border-left: 1px` 的单边凹陷读感由四边边界 + 卡片底色取代」描述的是**被反转的那次改动**,新注释要记下反转后的状态(单边竖线 + 统一面)、以及「`border-left` 是盒内手段、零位移、零新增 DOM」与「`overflow-y: auto` 是承重契约,不得删除」两条。

    **第 2 步 —— `#doc-panel-header`:只改归属令牌,不删声明。**

    `background: var(--color-surface-card);` → `background: var(--color-surface-page);`。

    `position: sticky;` / `top: 0;` / `border-radius: 0;` 三行**逐字不动**。背景声明本身**必须留在盘上** —— `.panel-header` 规则体内没有任何 `background`,不加则滚动正文会从标题行底下穿过去。本阶段是**改它的归属**,不是删它。

    同步改写其上方注释:`「表头底色与卡片底色同值(都取卡片令牌)」` 这句在本阶段**变成假命题**(C-9),必须改写为新事实(表头底色与统一面同值,都取页面令牌)。`border-radius: 0` 那段理由(「`#doc-panel` 是溢出容器,其后代被裁剪到带圆角的 padding box」)也随卡片圆角的消失而失去对象 —— 新注释要记下「反转后容器不再有圆角,该理由整段作废;声明本身仍是显式零值,一字不动」。

    **第 3 步 —— `.panel-header`:圆角归零。**

    `border-radius: var(--radius-md);` → `border-radius: 0;`(**只改这一行**,规则体其余七行逐字不动)。

    理由(写进注释):活动面板标记是 `inset 3px 0 0 var(--color-marker-active)` 的竖条,10px 圆角会把竖条上下端剪成收尖的弧 —— 它今天不可见**只是因为 `.panel-header` 无背景色**,那是巧合,不是设计。

    注:`#doc-panel-header` 自身的 `border-radius: 0` 因 ID 特异性早已胜出,故本步对它零影响 —— 这正是 D-11-7 把它记为「一字不动」的原因。

    **第 4 步 —— `#main-pane`:灰缝归零。**

    `gap: var(--space-3);` → `gap: 0;`。

    `overflow-y: auto;` / `align-items: center;` / `min-width: 0;` 三行**逐字保留**。`align-items: center` 与 `#main-pane > section` 的 `max-width: 768px` 是**一对仍在工作**的声明(定位置 / 控行长),D-11-5 显式收窄了 ROADMAP Deliverable 3 的「一并处置」措辞:侧沟的判据是 SC3 原文的「主区内容列**不再露出**左右灰沟」,由**色统一**满足。**不得把它们写成「已死声明」,也不得删除。**

    同步改写其上方注释:原文「间隙里透出的是页面底色(gray-3),这正是「白卡片浮在灰页面之上」的可见形态」描述的是被反转的状态,必须改写;并写明「卡片本身不得加 margin」这条纪律**继续有效**(它会移动既有几何并可能打在 24×24 命中区门上)。

    **第 5 步 —— 运行时读数。**

    跑 `.venv/bin/python scripts/check-09-idi09-validation.py --item c2` 与 `--item c4`,把 `INFO c2 #doc-panel 原始读数`、`INFO c2 #doc-panel 四条边框宽度原始读数`、`INFO c4 #main-pane gap 原始读数`、`INFO c4 .panel-header padding-top 原始读数` 四行**原文**抄进 SUMMARY。

    要求读到:`#doc-panel` 的 `border-top-width=0px` / `border-right-width=0px` / `border-bottom-width=0px` / **`border-left-width=1px`**、`overflow-y=auto`;`#main-pane` 的 `gap=0px`;`.panel-header padding-top=6px`(对照组,未受影响)。

    **再次强调:门会报 FAIL —— 设计预期。不要修改 `check-09`。**

    顺带记录(供计划 04 的 REG-03 消费,本任务**不判定**):跑一次 `.venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled`,把 `INFO item8 sticky 原始数值` 那一行的**原文**抄进 SUMMARY。预期 `header.top` 由 `1` 变为 `0`(即 `abs(header.top - panel.top)` 由 `1.000px` 变为 `0.000px`)。**本任务不得为了让该读数保持 `1.000px` 而回退任何 1px。**

    **⚠ 一条必须留档的措辞纪律(不要写错)。** `11-CONTEXT.md` 的 D-11-9 与 `ROADMAP.md` 的 Avoids 都写着「删它会同时打破 `check-05 --item 9` 的滚动者普查,**期望值是 4 不是 3**」。**这两处都是错的,不要抄。** 磁盘实测:`scripts/check-05-ui-uat.py` 的 `PANEL_SCROLLERS` 是 `("#chat-messages", "#latest-check", "#main-pane")` —— **3 个成员**;该普查的 JS 遍历的是 `document.querySelector('#main-pane')` **及其全部后代**,而 `#doc-panel` 是 `#main-pane` 的**兄弟**(两者同为 `#app` 的子元素)⇒ `#doc-panel` **根本不在该普查的范围内**。故删 `#doc-panel` 的 `overflow-y: auto` **不会**打破 item 9。**保留它的真实理由只有一条:L-1 的 sticky 表头依赖它仍是最近的可滚祖先。** 计划、SUMMARY 与任何注释都**不得出现数字 4**,也不得把「滚动者普查」写成保留理由。

    **第 6 步 —— 不触碰范围之外的一切。** 不删任何令牌(计划 02);不改 PAIR / ORDER 清单(计划 02);不改 `#main-pane > section + section` 的横线规则(Task 3);不改 `.panel-body` 的 `padding`(D-11-6:保持 `var(--space-4)` = 16px 不动);不改 `#doc-panel-body` 的 `padding`;不改 `#doc-panel.collapsed`;不改 `scripts/` 下任何文件;不改 `frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**`。
  </action>
  <verify>
    <automated>awk '/^#doc-panel \{/{f=1} f{print} f&&/^\}/{exit}' frontend/style.css</automated>
    <fails_when>the printed rule body does not contain `border-left: 1px solid var(--color-border-subtle);`, `background: var(--color-surface-page);`, `overflow-y: auto;`, `min-width: 0;`, or still contains `border: 1px solid var(--color-border);`, `border-radius`, `box-shadow`</fails_when>
    <automated>awk '/^#doc-panel-header \{/{f=1} f{print} f&&/^\}/{exit}' frontend/style.css</automated>
    <fails_when>the printed rule body is not exactly the four declarations `position: sticky;`, `top: 0;`, `background: var(--color-surface-page);`, `border-radius: 0;` in that order (the background declaration must still exist — only its token changed)</fails_when>
    <automated>awk '/^\.panel-header \{/{f=1} f{print} f&&/^\}/{exit}' frontend/style.css</automated>
    <fails_when>the printed rule body does not contain `border-radius: 0;` or still contains `border-radius: var(--radius-md);`, or its other seven declarations (`display` / `justify-content` / `align-items` / `height` / `padding` / `cursor` / `user-select`) differ from HEAD</fails_when>
    <automated>awk '/^#main-pane \{/{f=1} f{print} f&&/^\}/{exit}' frontend/style.css</automated>
    <fails_when>the printed rule body does not contain `gap: 0;` and `align-items: center;` and `overflow-y: auto;` and `min-width: 0;`, or still contains `gap: var(--space-3);`</fails_when>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c2 --item c4 2>&1 | grep -E 'INFO c2 #doc-panel (原始读数|四条边框宽度原始读数)|INFO c4 #main-pane gap 原始读数|INFO c4 \.panel-header padding-top 原始读数'</automated>
    <fails_when>any of the four INFO lines is missing, or the `#doc-panel 四条边框宽度原始读数` line does not read `top=0px / right=0px / bottom=0px / left=1px`, or the `#doc-panel 原始读数` line does not contain `overflow-y=auto`, or the `#main-pane gap 原始读数` line does not read `0px`, or the `.panel-header padding-top 原始读数` line does not read `6px`. (check-09's FAIL verdicts against the Phase 9 card contract are EXPECTED; do not edit check-09 in this plan)</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled 2>&1 | grep -E 'INFO item8 sticky 原始数值|item 8:'</automated>
    <fails_when>the `item 8:` summary line does not read exactly "item 8: PASS  (13 条断言,0 FAIL,0 BLOCKED)" (this is a recording step for REG-03 — if the sticky assertion FAILs, stop and report the raw reading rather than reverting the border to restore the old number)</fails_when>
    <automated>grep -c '期望值是 4\|期望值 4\|== 4' frontend/style.css</automated>
    <fails_when>the count is not exactly "0" (the stale "expected 4" claim must not be written into any comment; the census has three members and does not include #doc-panel at all)</fails_when>
  </verify>
  <acceptance_criteria>
    - `#doc-panel` 规则体:选择器文本与源码位置逐字未动;声明集 = HEAD 的 6 条 − `border` − `border-radius` − `box-shadow` + `border-left`,即 `flex` / `display` / `flex-direction` / `overflow-y` / `border-left` / `background` / `min-width`。`overflow-y: auto;` 与 `min-width: 0;` 逐字保留。
    - `#doc-panel-header` 规则体逐字为四行,其中 `background` 的令牌由卡片令牌改为页面令牌;`position: sticky;` / `top: 0;` / `border-radius: 0;` 三行逐字节未动。**`background` 声明没有被删除。**
    - `.panel-header` 规则体只有 `border-radius` 一行从 `var(--radius-md)` 变为 `0`,其余声明逐字未动;三条活动标记规则(`#session-panel:not(.hidden) .panel-header` 等)的 `box-shadow: inset 3px 0 0 var(--color-marker-active);` **逐字未动**。
    - `#main-pane` 规则体的 `gap` 恰为 `0`;`overflow-y: auto;` / `align-items: center;` / `min-width: 0;` 三行逐字保留,`align-items` 与 `#main-pane > section` 的 `max-width: 768px` 都**未被删除、未被改写**。
    - 四处注释均已就地改写;`#doc-panel-header` 上方那句「表头底色与卡片底色同值(都取卡片令牌)」**已不存在**;`#main-pane` 上方那句「白卡片浮在灰页面之上」的叙事**已不存在**;`.panel-header` 与 `#doc-panel` 的新注释里写明了反转后的新事实。
    - `check-09 --item c2` 的 `INFO c2 #doc-panel 四条边框宽度原始读数` 原文为 `top=0px / right=0px / bottom=0px / left=1px`;`INFO c2 #doc-panel 原始读数` 含 `overflow-y=auto`;`INFO c4 #main-pane gap 原始读数` 为 `0px`;`INFO c4 .panel-header padding-top 原始读数` 为 `6px`。四行原文均入册。
    - `check-05 --item 8 --browser bundled` 的汇总行为 `item 8: PASS  (13 条断言,0 FAIL,0 BLOCKED)`;`INFO item8 sticky 原始数值` 那一行的原文已抄进 SUMMARY,并注明其成因(移除 Phase 9 加的那条 1px 上边框)。
    - **计划、SUMMARY 与新增注释里都不出现「期望值是 4」这一陈旧说法**;保留 `overflow-y: auto` 的理由一律写成「L-1 的 sticky 表头依赖它仍是最近的可滚祖先」。
    - `git status --porcelain frontend/ backend/` 仍仅列出 `frontend/style.css`。
  </acceptance_criteria>
  <done>右栏文档区由四边卡片边界收成单边 `border-left` 发丝线,底色改归统一面,`overflow-y: auto` 与 `min-width: 0` 逐字保留;`#doc-panel-header` 的 sticky 背景声明仍在、只改归属;`.panel-header` 圆角归零;`#main-pane` 灰缝归零而 `align-items` / `max-width` 两条仍在工作;四处承重注释随代码改写;`check-09 --item c2/c4` 的 INFO 原始读数与 `check-05 --item 8` 的新 sticky 读数均已入册;「期望值是 4」的陈旧说法未流入任何注释或计划文本。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 3: 左栏面板之间的横线 + 两条发丝线的几何与对照组运行时取证</name>
  <files>frontend/style.css</files>
  <reversibility rating="reversible">回退是删除一条新增规则块,不牵连令牌层或清单。</reversibility>
  <read_first>
    - `frontend/style.css` 的 `#main-pane > section` 规则块(**Task 1 已改写的状态**)—— 横线规则块的插入锚点就在它**正后方**
    - `frontend/style.css` 的 `#doc-panel` 规则块(Task 2 已改写的状态)—— 竖线的落点
    - `frontend/style.css` 围栏内 `--color-border-subtle: var(--radix-gray-6);` 与其所在 role-band 段(`Radix's 12 steps are read as: … 6-8 border …`)以及 `.event-list` / `.annotation-item` / `.badge-answered` / `#latest-check` 四处消费者 —— 「既有令牌、零新增颜色值」的依据
    - `frontend/style.css` 的 role-band 段里关于装饰性边界的**既有登记**(逐字:`they are decorative, and SC 1.4.11 does not apply to a border that identifies nothing`)与 PAIR 清单头部注释里的同义句(逐字:`Decorative separators are deliberately absent — SC 1.4.11 does not apply to a border that identifies nothing`)—— **本任务不登记 NON-TEXT 对的依据,注释须引用这两处原文**
    - `frontend/index.html` 的 `main#main-pane` 段 —— 确认 `#session-panel` → `#annotations-panel` → `#checks-panel` → `#ai-panel` 的 DOM 顺序,以及 `#annotations-panel` / `#checks-panel` 在 p1 带 `.hidden`
    - `frontend/index.html` 与 `frontend/style.css` 的**交互控件对照组**来源:按钮规则(`border: 1px solid var(--color-border-strong);` + `border-radius: var(--radius-sm);`)、`#project-path-input`、`select`、`#check-switcher`、`.overlay-card`(`border-radius: var(--radius-md);` + `box-shadow: var(--shadow-overlay);`)
    - `scripts/check-09-idi09-validation.py` 的 `c1()` / `c2()` / `c4()` / `c5()` 全文 —— 逐字读它们的 `info()` 行格式。**本任务一行都不改它**
    - `scripts/check-05-ui-uat.py` 的 `read_style()` 与 `resolve_color()` 实现(说明「计算样式对 `display: none` 元素同样返回解析值」这一依据 —— 四个 section 可以在单一样本里全读到)
    - `.planning/phases/idi-11-decard-and-hairline-dividers/11-CONTEXT.md` §D-11-8 / §D-11-10 / §D-11-11 / §D-11-14 / §「连带后果」两条
    - `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-PATTERNS.md` §"Analog F" / §"Dual token + literal assertion on any boundary colour" / §"Hairline carries no NON-TEXT pair, and the argument is mandatory"
  </read_first>
  <action>
    **第 1 步 —— 追加横线规则块。**

    在 `#main-pane > section` 规则块**之后**(即 `#doc-panel` 规则块之前)追加一条新规则块,选择器 `#main-pane > section + section`,规则体**只一条**声明:`border-top: 1px solid var(--color-border-subtle);`。

    为什么只 3 条:`#session-panel` 是 DOM 第一个 `section`,`section + section` 永不匹配它 ⇒ 恰命中后三个面板,第一个面板顶部不画线(顶部是窗口边缘,画了会读成多一条)。相邻选择器按 **DOM 相邻**判定、不按渲染相邻,故 `#annotations-panel` / `#checks-panel` 带 `.hidden` 时 `#ai-panel` 仍带自己的上边线 —— 两种显隐状态下都恰好 1 条可见分界。

    特异性说明(写进注释):`#main-pane > section + section`(1-0-2)高于 `#main-pane > section`(1-0-1),故它对 `border-top` 的声明稳定胜出,与源码先后无关 —— 但**仍按「追加,不重排」纪律放在其所有者正后方**(Phase 10 把 `.markdown-body th { background: … }` 放在被改写的 `th, td` 规则正后方是同一手法)。

    在规则块上方写一段承重注释,逐条记下:(a) 这是**新增**的规则块(不是就地改写),插入位置紧接其所有者;(b) 线的档位是 `--color-border-subtle`(gray-6)—— 它已是四处内陷容器的边界色,故零新增令牌、零新增颜色值;D-11-8 显式否决的备选是 `--color-border`(gray-7),理由是它更重、且其两处卡片消费者搬走后只剩 `.markdown-body blockquote` 一处,语义会从「卡片边界」漂成「引用条」;(c) 线的宽度等于**内容列宽**(受 `max-width: 768px` 约束),不是主区全宽 —— 与 ChatGPT 的分隔线随内容列等宽一致;(d) **不登记 NON-TEXT 对比度对**:线不标识任何控件、不标识任何状态 ⇒ SC 1.4.11 不适用 —— **注释必须逐字引用 role-band 段与清单头部注释里的那两处既有登记**,不得只写结论;(e) 反证:gray-6 在白面上仅 1.412,若按 NON-TEXT 阈值 3.0 判即 FAIL;要让线达标就得换 gray-9(`#8d8d8d`,3.319),那会把发丝线变成深灰框,与去卡片化的目标相反。

    在 `#doc-panel` 规则块的注释里(或竖线声明旁)补一句同款论证,覆盖**竖线**:它是装饰性分隔,不标识任何控件/状态 ⇒ SC 1.4.11 不适用、不登记 NON-TEXT 对,依据同上两处既有登记。

    **第 2 步 —— 两条线的运行时读数(宽度 + 颜色双断言)。**

    跑 `.venv/bin/python scripts/check-09-idi09-validation.py --item c2 --item c4`,抄录 `INFO c2 #doc-panel 四条边框宽度原始读数`(要求 `left=1px`,其余 `0px`)。

    颜色读数本任务需要用一次**真实浏览器**读取 —— 由于 `check-09` 此刻还没有读边界颜色的断言(那正是计划 03 要补的),本任务用一个**临时**读数命令完成取证:用项目 `.venv` 的 Python 加载 `scripts/check-05-ui-uat.py` 作为模块(`importlib.util.spec_from_file_location`,文件名含连字符不能用 `import`),起一个无头 chromium、进入 `p1` fixture,读 `#doc-panel` 的 `border-left-color` 与四个 section 中 `#annotations-panel` 的 `border-top-color`,并同时打印 `resolve_color(page, "--color-border-subtle")` 与写死字面量 `rgb(217, 217, 217)`。把三条读数**原文**抄进 SUMMARY。**临时脚本落在系统临时目录**(如 `mktemp -d` 下),**不得**落进仓库树,跑完删除。

    要求三条值一致:`border-left-color` == `border-top-color` == `resolve_color("--color-border-subtle")` == `rgb(217, 217, 217)`。

    **第 3 步 —— 几何读数(「跨满面板可视高度」)。**

    同一次浏览器会话里(或复用 `check-09 --item c5` 的 INFO 行)读 `#doc-panel` 的 `getBoundingClientRect()`,抄录 `INFO c5 滚动前 rect` 那一行的原文,要求 `panel.top=0` 且 `panel.bottom=900`(1440×900 视口下)—— 即竖线的宿主高度等于视口高度,是「跨满」而不是「内容旁的一段」。

    **第 4 步 —— 交互控件对照组的运行时读数。**

    同一次会话里读:`button`(第一个可见按钮)、`#project-path-input`、`select`、`#check-switcher`、`.overlay-card` 各自的 `border-top-left-radius` 与 `border-top-width`。要求**每一个**的圆角为非零值且 `border-top-width` 非 `0px`(证明「移除边界」严格限于五个容器,不是把整站边界一起抹掉)。把逐条读数原文抄进 SUMMARY。

    **⚠ `.panel-header` 不得进对照组**:它有 `border-radius: 0`(本计划 Task 2 的裁定结果)与合法的 `inset` box-shadow(活动标记),放进对照组会造出恒红的假判据。

    **第 5 步 —— 零改动边界取证。**

    跑 `git status --porcelain`(全仓)与 `git diff --stat -- frontend/app.js frontend/index.html backend/`,确认本计划对仓库的改动**只有** `frontend/style.css`。`frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**` 逐字节未改。

    跑四条静态门(`check-01` / `check-02` / `check-03` / `check-04`),四条都必须绿。

    **第 6 步 —— 不触碰范围之外的一切。** 不删任何令牌(计划 02);不改任何 PAIR / ORDER 条目(计划 02);不改 `scripts/` 下任何文件;不改 `.panel-body` 的 `padding`;不新增 `@media` / `@layer` / `@property` / `var(--x, #fallback)` / `!important`;不改 `frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**`。
  </action>
  <verify>
    <automated>grep -nF -- '#main-pane > section + section {' frontend/style.css</automated>
    <fails_when>the line is not found, or the matching rule body is not exactly `border-top: 1px solid var(--color-border-subtle);` (one declaration only), or the rule block does not sit after the `#main-pane > section` block and before the `#doc-panel` block</fails_when>
    <automated>grep -cF -- 'border-top: 1px solid var(--color-border-subtle);' frontend/style.css; grep -cF -- 'border-left: 1px solid var(--color-border-subtle);' frontend/style.css</automated>
    <fails_when>the two counts are not exactly "1" and "1" (each hairline declaration must exist exactly once)</fails_when>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c2 --item c5 2>&1 | grep -E 'INFO c2 #doc-panel 四条边框宽度原始读数|INFO c5 滚动前 rect'</automated>
    <fails_when>either INFO line is missing, or the border-width line does not read `top=0px / right=0px / bottom=0px / left=1px`, or the rect line does not show `panel.top=0` together with `panel.bottom=900`. (check-09's FAIL verdicts are EXPECTED; do not edit check-09 in this plan)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>non-zero exit for any of the three, or any of the three not printing exactly "PASS"</fails_when>
    <automated>.venv/bin/python scripts/check-02-contrast.py</automated>
    <fails_when>non-zero exit, or any line beginning with "FAIL", or the final line not exactly "PASS: 0 failures"</fails_when>
    <automated>git status --porcelain</automated>
    <fails_when>output contains any tracked-path change other than "frontend/style.css" (untracked files under `.planning/` are allowed and expected)</fails_when>
    <automated>git diff --stat -- frontend/app.js frontend/index.html backend/ frontend/vendor/</automated>
    <fails_when>output is not empty</fails_when>
  </verify>
  <acceptance_criteria>
    - `#main-pane > section + section` 规则块存在,规则体**只有** `border-top: 1px solid var(--color-border-subtle);` 一条声明,位置在 `#main-pane > section` 块之后、`#doc-panel` 块之前(既未前插也未后置到别处)。
    - `border-top: 1px solid var(--color-border-subtle);` 与 `border-left: 1px solid var(--color-border-subtle);` 各在全文件中恰出现 1 次。
    - **真实浏览器**读数三条一致:`#doc-panel` 计算 `border-left-color` == `#annotations-panel` 计算 `border-top-color` == `resolve_color("--color-border-subtle")` == 写死字面量 `rgb(217, 217, 217)`。三条读数的原文与「临时读数脚本未落进仓库树」的事实都记进 SUMMARY。
    - `#doc-panel` 的 `getBoundingClientRect()` 在 1440×900 下 `top == 0` 且 `bottom == 900`(竖线跨满面板可视高度);`check-09 --item c5` 的 `INFO c5 滚动前 rect` 原文入册。
    - 交互控件对照组逐条读数入册:`button` / `#project-path-input` / `select` / `#check-switcher` / `.overlay-card` 的 `border-top-left-radius` 均非 `0px` 且 `border-top-width` 均非 `0px`。`.panel-header` **不在**对照组内。
    - 注释里逐字引用了 role-band 段与 PAIR 清单头部注释那两处「装饰性边界 ⇒ SC 1.4.11 不适用」的**既有**登记,并记下 gray-6 在白面上 1.412 的反证与 gray-9(3.319)会把发丝线变成深灰框的后果。
    - 四条静态门全绿;`git status --porcelain` 的**已跟踪路径**改动只有 `frontend/style.css`;`git diff --stat -- frontend/app.js frontend/index.html backend/ frontend/vendor/` 为空。
  </acceptance_criteria>
  <done>左栏面板之间的 1px 横线以一条新增规则块落位(恰命中后三个 section);两条发丝线的计算宽度均为 1px、计算颜色同时等于运行时令牌与写死字面量 gray-6;竖线宿主 `#doc-panel` 的 rect 跨满 1440×900 视口;交互控件对照组在同一份运行时读数里证明边界未被整站抹掉;装饰性边界的 SC 1.4.11 论证以两处既有登记原文写进注释;四条静态门全绿且仓库改动严格限于 `frontend/style.css`。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 无外部输入边界 | 本计划只改 `frontend/style.css` 的**声明层**(呈现层):零用户输入处理、零鉴权、零数据访问、零网络调用、零新增资源加载。攻击面限于**浏览器对 CSS 的解析与渲染** |
| 本地进程边界(既有门脚本) | 本计划的运行时证据取自**既有**门脚本 `check-09` / `check-05`,它们会 `ensure_server()` 自起(或复用)`uvicorn` 并用 Playwright 驱动无头 chromium 访问 `localhost`。本计划一行都不改这两个脚本,也不新增脚本 |
| 临时读数脚本边界 | Task 3 用一次性临时脚本读边界颜色与几何,脚本落在系统临时目录并随即删除 —— 它不进仓库树、不被任何门引用 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-11-01 | Information Disclosure | `frontend/style.css` 的五个容器规则与两条发丝线声明 | low | accept | 声明只用既有类名 / id / 元素名,不含属性选择器、不读用户数据、不引入 `url()` / `@import` / 远程字体 —— CSS 侧不存在数据外泄面。验收:`git diff -U0 -- frontend/style.css` 的新增行不含 `url(` / `@import` |
| T-idi-11-02 | Tampering | 本计划对 `.planning/phases/idi-11-…/` 之外的文件面 | **high** | mitigate | 本阶段预期是**纯 CSS + 门脚本**改动。任何 `frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**` 的字节变化都说明实现方式选错了(例如「必须加 DOM 元素才能画出跨满高的竖线」)。缓解:(a) 每个任务的 `<verify>` 都含 `git status --porcelain` 与 `git diff --stat` 的零改动判据;(b) 竖线强制走盒内 `border-left`(零 DOM、零位移),用 `margin` / 额外元素撑高的做法被显式排除;(c) 若出现偏离,**停下判因**,不要顺着改下去 |
| T-idi-11-03 | Tampering | 一次性的浏览器读数脚本 | medium | mitigate | 读数脚本若落进仓库树或写回被测样本,会污染被检对象。缓解:(a) 临时脚本一律落在系统临时目录(`mktemp -d`)并随即删除;(b) fixture 走既有 `c05.make_fixture(name, tmp_root)`(在 `tempfile.mkdtemp()` 下 `copytree`),原始 `scripts/ui-states/` 零改动;(c) 验收:`git status --porcelain` 的已跟踪路径改动只有 `frontend/style.css` |
| T-idi-11-04 | Tampering | 自起的 `uvicorn` 进程与复用既有 8765 监听的判定 | medium | mitigate | 该机 8765 端口可能已有先前遗留的 uvicorn 进程,门走「复用,不新起」分支是既有事实。缓解:复用既有门脚本的 `ensure_server()` 逻辑(本计划一行都不重写),不对复用来的进程动手 |
| T-idi-11-05 | Repudiation | 「连续面 + 发丝线已落地」这一结论缺少可复核的原始证据 | **high** | mitigate | 全部判据走**真实浏览器** `getComputedStyle` 读数,并把门输出的 **INFO 原始读数行**逐字抄进 SUMMARY(不是只写「绿」)。本计划明确要求把 `check-09` 反转后的 **FAIL** 与 INFO 读数**一并留档** —— 只留「绿」会把「门在正确工作」误读成「门坏了」。验收:SUMMARY 含 `INFO c1 #session-panel 原始读数`、`INFO c2 #doc-panel 四条边框宽度原始读数`、`INFO c4 #main-pane gap 原始读数`、`INFO c5 滚动前 rect`、`INFO item8 sticky 原始数值` 五行原文 |
| T-idi-11-06 | Denial of Service | 无 | low | accept | 纯呈现层改动,无可用性面;门脚本的运行时长与既有阶段一致(单次 chromium 会话) |
| T-idi-11-SC | Tampering | npm / pip / cargo 安装 | low | accept | 本阶段**零安装**:零新增依赖、零构建步骤、零新增第三方包(DESIGN.md D-06 硬约束);Playwright 与 chromium 均已在项目 `.venv` 中就绪,不触发下载。`frontend/vendor/` 仍只有 `marked.min.js`,无供应链面进入。验收:`ls frontend/vendor/` 输出仅 `marked.min.js` |
</threat_model>

<verification>
**静态门(全部必须绿):**

- `bash scripts/check-01-token-conformance.sh` → `PASS`
- `.venv/bin/python scripts/check-02-contrast.py` → `PASS: 0 failures`(本计划结束时两个待删令牌仍在盘上,清单仍可解析)
- `bash scripts/check-03-hidden-uniqueness.sh` → `PASS`
- `bash scripts/check-04-important-count.sh` → `PASS`

**运行时读数(经既有门脚本,逐行抄录 INFO 原文):**

- `.venv/bin/python scripts/check-09-idi09-validation.py --item c1` → `INFO c1 #session-panel 原始读数` 含 `background-color=rgb(255, 255, 255)` / `border-top-left-radius=0px` / `border-top=0px none` / `box-shadow=none`
- `.venv/bin/python scripts/check-09-idi09-validation.py --item c2` → `INFO c2 #doc-panel 四条边框宽度原始读数` == `top=0px / right=0px / bottom=0px / left=1px`;`INFO c2 #doc-panel 原始读数` 含 `overflow-y=auto`
- `.venv/bin/python scripts/check-09-idi09-validation.py --item c4` → `INFO c4 #main-pane gap 原始读数` == `0px`;`INFO c4 .panel-header padding-top 原始读数` == `6px`
- `.venv/bin/python scripts/check-09-idi09-validation.py --item c5` → `INFO c5 滚动前 rect` 显示 `panel.top=0` 且 `panel.bottom=900`
- `.venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled` → `item 8: PASS  (13 条断言,0 FAIL,0 BLOCKED)`;`INFO item8 sticky 原始数值` 原文入册
- 一次性临时读数:两条线的计算颜色 == `resolve_color("--color-border-subtle")` == `rgb(217, 217, 217)`;交互控件对照组五个元素的圆角非 `0px` 且 `border-top-width` 非 `0px`

**`check-09` 的整体裁决在本计划结束时是 FAIL —— 这是设计预期**(它断言的是被移除的卡片语言,由计划 03 改写)。判据取它的 INFO 读数,不取它的裁决。

**仓库卫生:**

- `git status --porcelain` 的已跟踪路径改动只有 `frontend/style.css`
- `git diff --stat -- frontend/app.js frontend/index.html backend/ frontend/vendor/` 为空
- `ls frontend/vendor/` 仅 `marked.min.js`
- `grep -o '/\* PAIR' frontend/style.css | wc -l` == 53;`grep -o '/\* ORDER' frontend/style.css | wc -l` == 1(本计划零清单增删)
</verification>

<success_criteria>
- 五个容器(4 个 `section` + `#doc-panel`)在真实浏览器里不再绘制边界:计算 `box-shadow` 为 `none`、四个 `border-*-radius` 长手为 `0px`、除发丝线所在的那一条边外计算 `border-*-width` 为 `0px`。
- 面板底色与 `html, body` 底色读数相同(同一档白),屏幕上不再有可辨的灰底与 elevation 差;`--color-surface`(gray-2,亮度 0.947307)仍是唯一比统一面(白,亮度 1.000000)更暗的一档。
- `#main-pane` 的计算 `gap` 为 `0px`;`align-items: center` 与 `max-width: 768px` **仍在盘上、仍在工作**,侧沟由同色消除而非由删除声明消除。
- 两条发丝线:计算宽度均为 `1px`,计算颜色同时等于运行时令牌 `--color-border-subtle` 与写死字面量 `rgb(217, 217, 217)`;竖线宿主 `#doc-panel` 的 rect 跨满 1440×900 视口;左栏横线恰 3 条(第一个面板顶部无线)。
- 交互控件(按钮 / 输入框 / `select` / `#check-switcher` / `.overlay-card`)仍保留各自的圆角与边界;`.panel-header` 的活动标记 `inset 3px 0 0` 仍作用于三个面板。
- `#doc-panel-header` 的 `background` 声明仍在盘上(只改归属);`#doc-panel` 的 `overflow-y: auto` 仍在盘上。
- 分隔线不登记 NON-TEXT 对比度对,且该判断以两处**既有**登记原文写在注释里(D-11-14 要求论证不得省略、不得默认)。
- 零新增颜色值 / 零新增 tier-1 primitive / 零新增 `!important` / 零新增 `@media`;四条静态门全绿。
- `frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**` 逐字节未改。
- 计划、SUMMARY 与新增注释中**不出现**「滚动者普查期望值是 4」这一陈旧说法;保留 `#doc-panel` 的 `overflow-y` 的理由只写 L-1 的 sticky 依赖。
</success_criteria>

<output>
Create `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-01-SUMMARY.md` when done
</output>

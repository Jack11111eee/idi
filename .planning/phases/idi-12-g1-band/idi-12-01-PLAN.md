---
phase: idi-12-g1-band
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - frontend/style.css
  - scripts/ui-states/checking/docs/DESIGN-check-2.md
  - scripts/check-09-idi09-validation.py
autonomous: true
requirements:
  - G1-01

estimate:
  tokens: 70000
  raw_tokens: 70000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- G1-01 的本体:表头读作一条独立的 band(D-12-2 的两侧钉死) ----
    - "`#latest-check` 的计算 `background-color` **不等于** `#latest-check th` 的计算 `background-color`(同一份 `checking` 样本的运行时 `getComputedStyle` 读数)⇒ 表头在其宿主内读作**一条独立的 band**,不再「灰底压灰底」(G1-01 / ROADMAP SC1 / D-12-2)"
    - "**两侧钉死(D-12-7):** `#latest-check` 的计算底色**同时**等于 `--color-surface-page` 的运行时解析值**与**写死的字面量 `rgb(255, 255, 255)`。只钉「两者不同」的判据会被「把宿主改成 gray-4 之类」满足 —— 判别力接近「只断言规则被写下了」;「宿主 == 白」把 D-12-1 选定的「改白」这件事本身也锁住"
    - "`.markdown-body th` 的绘制面**一字未动**:其计算 `background-color` 仍等于写死的 gray-2 字面量 `rgb(249, 249, 249)`。路线 (b)(改全局 `th`)未被采用 —— `scripts/check-10-idi10-validation.py` 的 `t1` / `t2` 因此保持全绿(D-12-1 未采用路线的留档理由)"
    - "`#latest-check` 的 `max-height: 30vh`、`border: 1px solid var(--color-border-subtle)`、`border-radius: var(--radius-sm)` 三条声明**逐字节未动**(D-12-3);`scripts/probe-card-border-token.py` 读的 `border-top-color`(gray-6)因此不变"
    - "`--color-surface` 的**值**未改、令牌未删:实测它除 `#latest-check` 外仍有 8 处以上消费者(`frontend/style.css` 的 `:998` / `:1013` / `:1057` / `:1113` / `:1243` / `:1414` / `:1447` / `:1552` / `:1648`)(D-12-1 ③)。**不得顺手删它**"
    # ---- fixture 忠于后端文法(D-12-5 / D-12-8) ----
    - "`checking` 样本的报告 `scripts/ui-states/checking/docs/DESIGN-check-2.md` 现在带 `## 问题分级` 二级标题与其下的表:表头行逐字为 `| 编号 | 级别 | 位置 | 问题 | 建议修法 |`,**至少一行取 P0 或 P1**;`backend.grammar.parse_problem_grades` 返回 **>= 1 行**、`is_pure_p2` 仍为 **False**、`is_pass_conclusion` 仍为 **False**。**为什么必须带标题:** `backend/grammar.py:88` 的 `_extract_table` 只认二级标题下的表(标题文本须含「问题分级」),无标题的表根本不被解析。**为什么必须带 P0/P1:** 若全行皆 P2,`is_pure_p2` 为真 ⇒ `backend/session.py:248-261` 返回 `mode=\"p2\"` ⇒ `frontend/app.js:690-695` 隐藏 `#btn-continue-check` 并把裁决卡注入 `#checks-panel .panel-body`,在 `#latest-check` 下方多出一棵子树,涟漪波及五条浏览器门与 6 张截图(D-12-8)"
    - "该样本的 UI 模式仍是 **`running`**,在运行时被正面断言:`#btn-continue-check` 不带 `.hidden` 且 `#verdict-cards` 内 `.verdict-card` 计数为 **0**(两者是 `paused` / `p2` 分支唯一的改形动作)"
    - "fixture 的其余内容**逐字节保留**:`## 发现` 小节与其两条 bullet、`> 核查结论:FIX(问题 2 项)` 结论行、缺失的「档位头部行」(D-12-8 明文不动)"
    # ---- 围栏承重注释的就地改写(D-12-1 连带后果 ①) ----
    - "`frontend/style.css:129-130` 的围栏承重注释已**就地改写**:不再声称 `#latest-check` 仍读作内陷;按 `:140-142` 的房屋写法**陈述新事实并记录旧句为何为假**,不删除历史"
    - "改写后的围栏**声明数不变**:`DESIGN TOKENS` 围栏内 `(--[a-z0-9-]+)\\s*:\\s*([^;]+);` 的匹配数仍为 **119**(规划期 HEAD 实测基线)。这是「围栏内注释不得出现令牌名紧接冒号」这条机械约束的**可失败形态** —— `scripts/check-02-contrast.py:27` 的 `DECL_RE` 扫围栏全文**含注释**,且 `parse_decls` 让**最后一个**匹配胜出,一条写成声明形态的注释会顶掉真声明"
    - "`scripts/check-02-contrast.py` PASS(`PASS: 0 failures`);PAIR 条目数仍为 **53**、`ORDER` 读数仍为 **0.363**、`TEXT_MIN` / `NON_TEXT_MIN` 与 HEAD 逐字节相同 ⇒ **零新增对比度条目、零阈值放宽**(`--color-text ON --color-surface-page` 已在 `:620` 登记;`--color-surface` 的 TEXT 配对因另有控件消费者而仍成立)(D-12-1 ②)"
    # ---- 新判据的落位与形态(D-12-6) ----
    - "新判据落在 `scripts/check-09-idi09-validation.py` 的**新项 `c6`**:`ITEMS` 由五项变六项、模块 docstring 的映射表补一行 `c6 → G1-01`;`c1..c5` 与 `--item` / `--screenshot` / `--keep` 三个 CLI 参数、退出码语义(`0=全 pass / 1=有 FAIL / 2=有 BLOCKED`)**逐字保留**。**为什么另立一项而不并进既有项:** `c1..c5` 是 Phase 11 的 `REG-01` 契约载体;把 Phase 12 的 `G1-01` 断言塞进它们会让「哪条判据钉哪一次改动」不可分辨(D-12-6 的 Discretion 项)"
    - "`c6` 的每一处令牌解析断言都走 `ok_true` 并显式处理 `None` —— `ok()` 在期望侧为 `None` 时降级成 BLOCKED(exit 2,本项目当良性码),而「令牌缺失」必须是 FAIL(仓库既有纪律,见 `c3` 的 `ok_true` None 分支)"
    - "`c6` 里「`#latest-check th` 可读」是一条**硬 FAIL**(`ok_true(..., th_bg is not None, ...)`),不是 BLOCKED:表头消失正是本项要抓的回归(fixture 表被删 ⇒ 样本里又没有可消失的 band)"
    # ---- 变异证明(唯一能证明守卫真的会失败的手段) ----
    - "`c6` 有**两条**「变异 → FAIL」真实读数,逐条抄录 FAIL 原文(含 `expected=` / `actual=`),不得只声明做过:①把 `#latest-check` 的底色改回 `var(--color-surface)` ⇒ 两条钉死半条同时红;②把宿主底色改指 `--color-surface-sunken`(gray-3,与 `th` 的 gray-2 **不同**但**不是白**)⇒ 「两者不同」半条**保持绿**、「宿主 == 白」半条必红 —— 这一条是 D-12-7「只钉不同会被任何别的灰满足」的机械证据,证明**两侧钉死不是冗余**"
    - "两条变异都在**已提交的树**上做(前置:`git status --porcelain frontend/` 干净),用定向 `git checkout -- frontend/style.css` 还原,还原后 `git diff --exit-code -- frontend/style.css` 为 **rc=0** 且 `git hash-object frontend/style.css` 与变异前记录值**逐字符相同**。**全程禁用 `git stash`**(它跨工作树共享,本项目明令禁止)"
    # ---- 边界(逐字节) ----
    - "`frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**` **逐字节未改**;`frontend/vendor/` 仍只有 `marked.min.js`;`scripts/check-05-ui-uat.py` / `check-02-contrast.py` / `check-10-idi10-validation.py` / `check-01`…`04` / `check-06` / `check-07` / `probe-*` 本计划零改动。**偏离这个预期是一个信号**,须停下判因"
    - "四条静态门在本计划结束时全绿:`check-01`(围栏外零裸 `#hex`、零 tier-1 原语引用)、`check-02`(`PASS: 0 failures`)、`check-03`(`^\\.hidden {` == 1)、`check-04`(`!important;` **声明**数 == 1)"

  artifacts:
    - path: "frontend/style.css"
      provides: "`#latest-check` 的宿主绘制面由内陷面(gray-2)就地改写为统一面(白)—— 一条声明值改写,不是追加覆盖;外加围栏 `:129-130` 承重注释的就地改写"
      contains: "#latest-check {"
    - path: "scripts/ui-states/checking/docs/DESIGN-check-2.md"
      provides: "补上后端文法强制的「问题分级表」:`## 问题分级` 二级标题 + 逐字表头 + 含 P0/P1 的数据行,使 `checking` 样本真的渲染出 `#latest-check` 内的表头"
      contains: "| 编号 | 级别 | 位置 | 问题 | 建议修法 |"
    - path: "scripts/check-09-idi09-validation.py"
      provides: "新增运行时项 `c6`(G1 表头 band 的两侧钉死 + fixture 模式不变量)并注册进 `ITEMS` 与 docstring 映射表"
      contains: "def c6("

  key_links:
    - from: "`scripts/check-09-idi09-validation.py` 的 `c6`"
      to: "`#latest-check` 与其内 `th` 在真实浏览器里的 computed `background-color`"
      via: "`read_style(page, \"#latest-check\", \"background-color\")` / `read_style(page, \"#latest-check th\", \"background-color\")` —— band 是**画出来**的,文本里写着两个不同令牌不等于它真的生效"
      pattern: "read_style\\(page, \"#latest-check th\", \"background-color\"\\)"
    - from: "`frontend/style.css` 的 `#latest-check { background: … }`"
      to: "`--color-surface-page`(统一面,白,`:148`)"
      via: "令牌消费 —— 改归统一面后,宿主与 `.markdown-body th`(仍消费 `--color-surface`,gray-2)不再是同一档"
      pattern: "background: var\\(--color-surface-page\\);"
    - from: "`scripts/ui-states/checking/docs/DESIGN-check-2.md` 的 `## 问题分级` 标题"
      to: "`backend/grammar.py` 的 `_extract_table(md_text, \"问题分级\")` → `parse_problem_grades` → `is_pure_p2` → `backend/session.py` 的 `mode`"
      via: "二级标题定位 + 表头行丢弃 + 分隔行跳过;至少一行 P0/P1 使 `is_pure_p2` 为假 ⇒ `mode` 保持 `running`、控件区零变化"
      pattern: "## 问题分级"
    - from: "`scripts/check-09-idi09-validation.py` 的 `c6` fixture 模式不变量断言"
      to: "`frontend/app.js:684-706` 的四路 `mode` 分支"
      via: "`read_classlist(page, \"#btn-continue-check\")` 不含 `hidden` 且 `#verdict-cards` 的 `.verdict-card` 计数为 0 —— 两者同时成立即 `mode === 'running'` 的可观测形态"
      pattern: "read_classlist"

  prohibitions:
    - statement: "不得改 `--color-surface` 的**值**,也不得删该令牌。它被 6 处以上消费(`#check-switcher` / 三个 `select` / `.markdown-body th` / `.overlay-card` 等)且是既有 PAIR(`--color-text ON --color-surface`,15.48)的地面;改值会连锁影响它的**全部**配对,与 v1.15 记下的「调色」错向同型"
      status: active
      verification: flagged
    - statement: "不得采用路线 (b)(改全局 `.markdown-body th` 的底色),也不得追加 `#latest-check th` 的局部覆盖。前者会让文档区表头读感一并变深并打破 `check-10` 的 `t1` / `t2`(它们把 `th` 钉死在 gray-2 字面量);后者会引入「报告区表头与文档区不同色」的宿主特例(D-12-1 已逐条否决)"
      status: active
      verification: flagged
    - statement: "不得改 `#latest-check` 的 `border` / `border-radius` / `max-height`。G1-01 只谈 band;它是内陷可滚区、不是面板,`scripts/probe-card-border-token.py:45` 把它的 gray-6 边框当作「非卡片」对照样本。改它 = 未裁定项(D-12-3)"
      status: active
      verification: flagged
    - statement: "不得把 fixture 的 `## 问题分级` 表做成**全 P2**。全 P2 + 既有 FIX 结论行会让 `is_pure_p2` 为真 ⇒ `mode` 翻成 `p2` ⇒ 控件区改形、`#latest-check` 下方多出裁决卡子树,波及五条浏览器门与 6 张截图(D-12-8)"
      status: active
      verification: flagged
    - statement: "不得在围栏内的注释里写出「令牌名紧接冒号」的形态。`scripts/check-02-contrast.py` 的 `DECL_RE` 扫围栏全文含注释、`parse_decls` 让最后一个匹配胜出 ⇒ 一条写成声明形态的注释会顶掉真声明(本项目已为此付过 FAIL)"
      status: active
      verification: flagged
    - statement: "不得在变异测试里使用 `git stash`(它跨工作树共享,本项目明令禁止);还原一律用定向 `git checkout -- frontend/style.css`,并以 `git diff --exit-code -- frontend/style.css` 为 rc=0 **且** `git hash-object` 逐字符相同作为「逐字节还原」的判据"
      status: active
      verification: flagged
    - statement: "不得为让门绿而删除 / 降级 / 放宽任何断言。既有 `check-09` 的 `c1..c5`、`check-02` 的阈值与 PAIR 条目数、`run_screenshots` 的「恰含 5 个 PNG」断言一律逐字保留"
      status: active
      verification: flagged
    - statement: "不得顺手做未裁定项:`check-10` 的 `t1` PASS 行上那条过期注释(`scripts/check-10-idi10-validation.py:328` 的 `note=`)、报告区表头在 `#latest-check` 内 sticky、G2(`--radix-gray-1` 零消费 + 通用围栏消费断言)、`999.2`、暗色模式(`A11Y-V2` / `FLOW-V2` / `TOKEN-V2`)、Nyquist 缺口、图标与空状态 —— 全部 Out of Scope(D-12-4 / D-12-12)"
      status: active
      verification: flagged
---

<objective>
修掉 v1.15 审计登记的 **G1** —— `#latest-check` 自身声明 `background: var(--color-surface)`(gray-2)**且自身是 `.markdown-body` 宿主**,而 `.markdown-body th` 用同一令牌绘制 ⇒ 自检报告里的表头是**灰底压灰底**、band 消失。本计划让表头在 `#latest-check` 内**读作一条独立的 band**,并把这条读数落成 `scripts/check-09-idi09-validation.py` 里的永久断言 `c6`。

Purpose: G1 是**被用户点名的范围**(2026-09-28「连带 G1」),不是顺手清理。四条 `.markdown-body` 宿主里只有 `#latest-check` 自己画灰底(另三个 `#draft-content` / `#brainstorm-content` / `#round-doc` 都不声明 `background`,透明 ⇒ 继承白面板)⇒ 只有它内部的 `th` 消失。**修法是消除这处不对称,不是给表头换色。**

**路线已由用户裁定(D-12-1):** 移宿主 → 改白(`background` 由 `var(--color-surface)` 就地改写为 `var(--color-surface-page)`)。**不是**路线 (b)(改全局 `th`),**也不是**局部覆盖 `#latest-check th`。理由三条:①改白消除的是不对称本身而不只是症状;②band 因此落在 gray-2 on white = 1.053,与文档区表头今天的样子完全相同(Phase 10 已签核的读感);③它是唯一**不需要改写任何门**的路线(`check-10` 的 `t1` 把 `th` 底色钉死在 gray-2 字面量,只动宿主底色则 `t1` 全绿)。

**为什么必须先补 fixture 的表(D-12-5 / D-12-8):** `backend/prompts.py:494-499` 要求每份自检报告都带「问题分级表」,而 `checking` 与 `archive` 两个 fixture 报告**都不遵守后端文法** ⇒ **今天在任何样本上都读不到、也拍不到 G1 的 band**。`#latest-check` **只在 `checking` 样本可见**(p1 下祖先 `#checks-panel` 带 `.hidden`),故补表补在 `checking`。

**为什么必须先做本计划再做收口:** `REG-04` 的「零新增失败」必须在**最后一次 `style.css` 改动之后**跑才成立;`VIS-01` 的截图必须是**最终态**(ROADMAP Phase 12 Rationale)。

**本计划关闭的需求:** G1-01。

**本计划不触碰:** `REG-04`(计划 03)、`VIS-01`(计划 02);`scripts/check-05-ui-uat.py` / `check-02-contrast.py` / `check-10-idi10-validation.py` / `check-01`…`04` / `check-06` / `check-07` / `probe-*`(零改动);`frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**`(零字节);G2 / `999.2` / 暗色模式 / Nyquist 缺口 / 图标与空状态 / `check-10` 的过期注释 / 报告区表头 sticky(全部 Out of Scope)。

**执行前基线(规划期已在 HEAD 上实测,执行器须复核):**

| 检查 | 规划期在 HEAD 上的实测结果 |
|---|---|
| `grep -cF -- 'background: var(--color-surface-page);' frontend/style.css` | **4**(`:764` / `:828` / `:900` / `:938` = 四个并回统一面的容器)⇒ 本计划后应为 **5** |
| `grep -c '/\* PAIR ' frontend/style.css` | **53** |
| `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`,`ORDER 0.363` |
| `bash scripts/check-01-token-conformance.sh` / `check-03` / `check-04` | 三条均 `PASS`,`rc=0` |
| 围栏内 `(--[a-z0-9-]+)\s*:\s*([^;]+);` 匹配数 | **119**(去重后亦 119) |
| `.venv/bin/python -c "…g.parse_problem_grades(fixture)…"` | `rows 0` / `pure_p2 False` / `pass_conclusion False` |
| `grep -n '^#latest-check {' frontend/style.css` | **1651**(规则体 `:1651-1659`,`background` 在 `:1657`) |
| `scripts/check-09-idi09-validation.py` 的 `ITEMS` | `{"c1": c1, "c2": c2, "c3": c3, "c4": c4, "c5": c5}` —— **没有 `c6`** |
| `git status --porcelain frontend/` | 空 |

**Flagged assumption(probe fallback,不得静默丢弃):** `G1-01` 在边界覆盖探针里返回 `{"category":"unclassified","status":"unresolved"}` —— 分类器的 cue 词汇是英文、而该需求文本是中文散文,故它**拒绝分类而不是乱猜**。按协议:`unclassified` 行**保持 `unresolved`**,**不得**用 backstop 自动消解、**不得**静默丢弃、**不得**为它发明探针派生的谓词。本计划的绑定验收判据来自 **ROADMAP 的 Success Criteria 1–5 与 CONTEXT 的 D-12-1 … D-12-12**,已逐条落进 `must_haves.truths`。

Output: 改写后的 `frontend/style.css`(一条声明值 + 一段承重注释)、补过表的 `scripts/ui-states/checking/docs/DESIGN-check-2.md`、新增 `c6` 的 `scripts/check-09-idi09-validation.py`;两条变异测试的真实「变异 → FAIL」读数。
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
@.planning/phases/idi-12-g1-band/12-CONTEXT.md
@.planning/phases/idi-12-g1-band/idi-12-PATTERNS.md
@.planning/milestones/v1.15-MILESTONE-AUDIT.md
@frontend/style.css
@scripts/check-09-idi09-validation.py
@scripts/ui-states/checking/docs/DESIGN-check-2.md
@backend/grammar.py
</context>

## Artifacts this phase produces

**本计划新增的符号(plan-review-convergence 的源锚定遍历须把它们排除在漂移核验之外):**

| 符号 | 类型 | 落点 |
|---|---|---|
| `c6` | 新的 item 函数(`def c6(page, tmp_root)`) | `scripts/check-09-idi09-validation.py` |
| `"c6": c6` | `ITEMS` 字典的新条目(五项 → 六项) | 同上 |
| `c6 → G1-01` | 模块 docstring 映射表的新行 | 同上 |
| `read_classlist` | 本文件新引入的 check-05 别名(`read_classlist = c05.read_classlist`) | 同上 |
| `## 问题分级` | fixture 报告的新二级标题 | `scripts/ui-states/checking/docs/DESIGN-check-2.md` |

**本计划改动的既有符号(不是新增,漂移核验须正常覆盖):** `frontend/style.css` 的 `#latest-check` 规则体(一条声明值)、围栏 `:129-130` 的注释段。

**本阶段后续计划会新增(此处登记以免被当作漂移):** `--g1-snapshot DIR`(计划 02 的 check-09 新 CLI 参数)、`g1_snapshot()`(计划 02 的新函数)、`.planning/phases/idi-12-g1-band/screenshots/**`(计划 02)、`.planning/phases/idi-12-g1-band/gate-logs/idi-12-03/**`(计划 03)。

<tasks>

<task type="tracer">
  <name>Task 1: G1 的 band 单条路径端到端 —— fixture 补表 + 宿主绘制面改白 + `c6` 双钉判据(真实浏览器读数证明)</name>
  <files>frontend/style.css, scripts/ui-states/checking/docs/DESIGN-check-2.md, scripts/check-09-idi09-validation.py</files>
  <reversibility rating="costly">D-12-1 选定「移宿主 → 改白」,撤销要连带改写围栏 :129-130 的承重注释、重写 `c6` 的判据与其两条变异证明,并重拍 6 张截图。</reversibility>
  <read_first>
    - `frontend/style.css` —— 规则体 `:1651-1659`(`#latest-check`);围栏内 `:122-147`(Phase 11 对 `--color-surface-page` 的就地改写与其承重注释);`:148`(`--color-surface-page: var(--white);`)、`:220`(`--color-surface: var(--radix-gray-2);`);`:1236-1243`(`.markdown-body table` / `th, td` / `th { background: var(--color-surface); }`);`:620-622`(三条候选地面的既有 PAIR 登记)
    - `scripts/check-09-idi09-validation.py` —— 文件头 docstring(`:1-96`,尤其 `:40-66` 的映射表与 `:75-90` 的断言写法纪律);`:99-160`(helper 别名、`LEFT_SECTIONS`、三档字面量常量、`fence_text()`、`png_size()`);`c3`(`:591-660`)作为「令牌解析走 `ok_true` + 显式 None 分支」的样板;`ITEMS`(`:796` 附近)
    - `scripts/check-05-ui-uat.py` —— `:202-256`(`ok` / `norm` / `ok_true` / `blocked` / `info` 的签名与 `None` 语义)、`:347-348`(`read_style`)、`:424-428`(`read_classlist`)、`:435-455`(`resolve_color`)、`:485-516`(`make_fixture` / `enter_project`)、`:584`(`STATES`)
    - `scripts/ui-states/checking/docs/DESIGN-check-2.md`(将被修改的 fixture,当前 8 行);`scripts/ui-states/p3/docs/discuss-round-2.md`(仓库既有的 markdown 表格写法样板);`scripts/ui-states/archive/docs/DESIGN-check-1.md`(同族报告,**本计划不动**)
    - `backend/prompts.py:486-509`(报告文法:二级标题含「问题分级」、表头逐字、级别仅 P0/P1/P2、末行结论形态)
    - `backend/grammar.py:88-118`(`_extract_table` 只认二级标题下的表)、`:329-359`(`parse_problem_grades`)、`:362-375`(`is_pure_p2`)、`:249-260`(`is_pass_conclusion`);`backend/session.py:248-261`(`mode` 判定)
    - `frontend/app.js:684-706`(四路 `mode` 分支对 `#btn-continue-check` / `#verdict-cards` 的动作);`frontend/index.html:47`(`<div id="latest-check" class="markdown-body">`)
    - `.planning/phases/idi-12-g1-band/12-CONTEXT.md` 的 D-12-1 / D-12-2 / D-12-3 / D-12-5 / D-12-6 / D-12-7 / D-12-8
  </read_first>
  <action>
    **这是一条端到端的最小路径:fixture(markdown)→ 后端文法 → 前端渲染 → CSS 绘制面 → 运行时门。三个文件一起改,一次证明。**

    **(a) fixture 补表(`scripts/ui-states/checking/docs/DESIGN-check-2.md`)。**
    在首行 `# 核查报告 2` **之后**、`## 发现` **之前**,插入:一个二级标题,标题文本为 `问题分级`(即该行恰为井号井号 + 空格 + `问题分级`);一个空行;表头行,**逐字**为 `| 编号 | 级别 | 位置 | 问题 | 建议修法 |`(五个列头,半角竖线分隔,单元格内两侧各一个半角空格);一行分隔行(用 `backend/prompts.py:497` 的逐字形态:五列、每列三个半角连字符);随后两行数据行。两行数据行中**至少一行**的「级别」列取 `P1`(另一行取 `P2` 即可,内容与既有 `FIX(问题 2 项)` 结论自洽:一行对应「未定义划词菜单的键盘路径」、一行对应「术语表未覆盖轮次冻结」)。表放得**靠上**(紧跟标题行,即上面这个位置)是硬要求:`#latest-check` 的 `max-height: 30vh` 使它是滚动区,表放靠下就落在可视区外,整窗图与元素截图都拍不到 band(D-12-10)。
    **其余内容逐字节不动:** `## 发现` 小节与其两条 bullet、`> 核查结论:FIX(问题 2 项)` 结论行、文件末尾无换行的现状、以及缺失的「档位头部行」(D-12-8 明文不动)。
    **不要**把表做成全 P2(会让样本的 UI 模式翻成 `p2`)。

    **(b) 宿主绘制面改白(`frontend/style.css`)。**
    在 `#latest-check` 规则体(当前 `:1651-1659`)内**就地改写**那一条声明:把 `background` 的值由内陷面令牌 `var(--color-surface)` 改为统一面令牌 `var(--color-surface-page)`。规则体内其余六条声明(`max-height: 30vh` / `overflow-y: auto` / `padding` / `border: 1px solid var(--color-border-subtle)` / `border-radius: var(--radius-sm)` / `font-size`)与选择器行**逐字节不动**。**不追加**任何覆盖规则,**不重排**任何规则块,**不改** `--color-surface` 的声明值,**不改** `.markdown-body th`。

    **(c) `c6` 落进 `scripts/check-09-idi09-validation.py`。**
    新增模块级 item 函数 `c6(page, tmp_root)`,并把 `read_classlist = c05.read_classlist` 加进顶部 helper 别名区。函数体形状照 `c3` 与 `c1`:打印 `=== c6: … ===` 横幅;`proj = c05.make_fixture("checking", tmp_root)` + `c05.enter_project(page, proj)`(`checking` 是**唯一** `#latest-check` 可见的样本 —— p1 下祖先 `#checks-panel` 带 `.hidden`);先 `info()` 抄录原始读数(`#latest-check` 的计算底色、`#latest-check th` 的计算底色、`--color-surface-page` 的解析值),再逐条断言。断言一律走 `ok_true`(期望侧含令牌解析值)或 `ok()`(期望侧是硬字面量),顺序与判据如下:

    1. `#latest-check th` 的计算底色**可读**(`th_bg is not None`)—— 硬 FAIL,不是 BLOCKED:表头消失正是本项要抓的回归,fixture 的表被删会让这条红。note 写明它是 D-12-5 的前提。
    2. **钉「两者不同」**:`norm(host_bg) != norm(th_bg)`。note 写明「灰底压灰底」是 G1 的准确含义 —— `th` 的下边线一直在,消失的是表头那一档底色。
    3. **钉「宿主 == 令牌」**:`host_bg` 非 None **且** `page_token` 非 None **且** 两者 `norm()` 相等。note 写明等值复核的作用:证明底色来自令牌而不是硬编码 `rgb()`。
    4. **钉「宿主 == 白」**:`ok(item, …, SURFACE_PAGE_LITERAL, host_bg)` —— **复用既有常量** `SURFACE_PAGE_LITERAL`(`"rgb(255, 255, 255)"`,模块级已声明),不新增字面量常量。
    5. **钉 `th` 未动**:`ok(item, …, SURFACE_SUNKEN_LITERAL, th_bg)` —— **复用既有常量** `SURFACE_SUNKEN_LITERAL`(`"rgb(249, 249, 249)"`,即 gray-2)。note 写明它是路线 (a) 的反向证据:改的是宿主、不是表头。
    6. **fixture 模式不变量**:`read_classlist(page, "#btn-continue-check")` 的结果非 None **且不含** `hidden`;`page.evaluate` 读 `#verdict-cards` 内 `.verdict-card` 的元素数 **等于 0**。两者同时成立即 `mode === 'running'`(对照 `frontend/app.js:684-706` 的四路分支)。note 写明它守的是 D-12-8 的防翻转前提。

    然后:在 `ITEMS` 字典里注册 `"c6": c6`;在模块 docstring 的「断言与需求的映射」表里补一行,写明 `c6 → G1-01`,`#latest-check` 内表头读作独立 band 的两侧钉死 + fixture 模式不变量,并注明它**不是** Phase 11 的 `REG-01` 契约。**`c1..c5` 的既有断言、`parse_args` 的三个参数、`main()` 的退出码语义一律逐字保留。**

    **(d) 提交。** 三处改动一次性提交(它们是一条路径的三段,分开提交会造出「改了值但没人验」的中间态)。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c6</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or the "=== 逐项结论 ===" block showing a non-zero FAIL or BLOCKED count for item c6, or the trailing line not starting with "exit=0"</fails_when>
    <automated>.venv/bin/python -c "import sys;sys.path.insert(0,'.');import backend.grammar as g;t=open('scripts/ui-states/checking/docs/DESIGN-check-2.md',encoding='utf-8').read();r=g.parse_problem_grades(t);print('rows',len(r));print('levels',[x['level'] for x in r]);print('pure_p2',g.is_pure_p2(t));print('pass_conclusion',g.is_pass_conclusion(t))"</automated>
    <fails_when>rows is less than 1, or levels contains neither "P0" nor "P1", or pure_p2 is not False, or pass_conclusion is not False</fails_when>
    <automated>grep -cF -- 'background: var(--color-surface-page);' frontend/style.css</automated>
    <fails_when>the count is not "5" (HEAD baseline is 4; the #latest-check rewrite must add exactly one and only one)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh</automated>
    <fails_when>any of the three exits non-zero, or any of them fails to print "PASS"</fails_when>
    <automated>.venv/bin/python scripts/check-02-contrast.py</automated>
    <fails_when>non-zero exit, or the output does not end with "PASS: 0 failures"</fails_when>
    <automated>git status --porcelain frontend/ scripts/ backend/ frontend/vendor/</automated>
    <fails_when>output contains any path other than "frontend/style.css", "scripts/check-09-idi09-validation.py" and "scripts/ui-states/checking/docs/DESIGN-check-2.md"</fails_when>
  </verify>
  <acceptance_criteria>
    - `.venv/bin/python scripts/check-09-idi09-validation.py --item c6` 输出以 `exit=0` 结尾,`item c6: PASS` 且 `0 FAIL,0 BLOCKED`;stdout 里能看到 `INFO` 抄录的三条原始读数(`#latest-check` 的计算底色 = `rgb(255, 255, 255)`、`#latest-check th` 的计算底色 = `rgb(249, 249, 249)`、`--color-surface-page` 的解析值 = `rgb(255, 255, 255)`)。
    - 上一条命令的 FAIL 原文里出现的两条标签,分别是「两者不同」与「宿主 == 白」的判据标签 —— 它们在**未变异**时必须为 PASS(该行以 `PASS` 开头)。
    - fixture 的文法读数恰为:`rows >= 1`、`levels` 里至少出现一次 `P1`(或 `P0`)、`pure_p2` 为 `False`、`pass_conclusion` 为 `False`。
    - `grep -cF -- 'background: var(--color-surface-page);' frontend/style.css` 的输出是 `5`。
    - `frontend/style.css` 里 `#latest-check` 规则体的 `max-height` / `overflow-y` / `padding` / `border` / `border-radius` / `font-size` 六条声明与 HEAD 逐字节相同(`awk '/^#latest-check \{/{f=1} f{print} f&&/^\}/{exit}' frontend/style.css` 打印的块里,除 `background` 一条外逐字等于 HEAD 的同名块)。
    - `check-01` / `check-03` / `check-04` 各打印 `PASS` 且 `rc=0`;`check-02` 以 `PASS: 0 failures` 结尾且 `ORDER` 行为 `ORDER 0.363 …`。
    - `scripts/check-09-idi09-validation.py` 的 `ITEMS` 含六个键(`c1`…`c6`);`parse_args()` 仍有且仅有 `--item` / `--screenshot` / `--keep` 三个参数。
    - `git status --porcelain frontend/ scripts/ backend/ frontend/vendor/` 只列出上表三个路径。
  </acceptance_criteria>
  <done>fixture 的 `checking` 报告带上了文法强制的「问题分级」表(含至少一行 P1),`parse_problem_grades` 返回 >= 1 行而 `is_pure_p2` 仍为假;`#latest-check` 的宿主绘制面已就地改归统一面(白),其 `border` / `border-radius` / `max-height` 逐字节未动;`check-09` 的新项 `c6` 在 `checking` 样本上以真实浏览器 computed style 证明「宿主底色 != 表头底色」**且**「宿主底色 == 统一面令牌 == 白」,并顺带证明样本仍处 `running` 态;`check-01`…`check-04` 全绿。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 2: 围栏承重注释就地改写 —— 删掉被证伪的那半句,按房屋写法记下新事实与旧句为何错</name>
  <files>frontend/style.css</files>
  <read_first>
    - `frontend/style.css` —— 围栏内 `:122-147` 的整段注释(将被改写的是 `:129-130` 那两行);`:140-142` 是**房屋写法样板**(「原来写在这里的那句话声称 X,那半句是更危险的一半,现在是假的」);`:148` 的声明行(注释正下方);`:42-44`(围栏抬头关于「只声明被消费的令牌」的措辞)
    - `scripts/check-02-contrast.py` —— `:27` 的 `DECL_RE` 与 `parse_decls`(围栏全文**含注释**、最后一个匹配胜出)
    - `.planning/phases/idi-12-g1-band/12-CONTEXT.md` 的 D-12-1「连带后果」①
  </read_first>
  <action>
    就地改写 `frontend/style.css:129-130` 的那两行注释(位于 Phase 11 那段「两级 elevation」叙事里)。该从句以「The inset tier SURVIVES」起头,其后半句声称**控件与 `#latest-check` 两者**都仍读作内陷。
    - **保留**控件那半句 —— 它在改白后**仍然为真**(控件仍绘制在更暗的内陷面上)。
    - **删掉 / 改写** `#latest-check` 那半句 —— 它在本次改动后**不再成立**:`#latest-check` 现在画的是统一面(白),与它内部的表头(`.markdown-body th`,gray-2)不再是同一档。
    - **按 `:140-142` 的房屋写法记录旧句为何为假**,不删除历史:写明「这里原先声称 X;那半句现在是假的,因为 Phase 12 把该容器的宿主绘制面改归了统一面,好让报告里的 markdown 表头能读作一条独立的 band」。**不要**只把旧句抹掉而不留痕。
    - **机械约束(硬):** 改写后的**整段围栏注释**里**不得出现「令牌名紧接半角冒号」的形态**。`scripts/check-02-contrast.py:27` 的 `DECL_RE` 扫围栏全文**含注释**,`parse_decls` 让**最后一个**匹配胜出 ⇒ 一条写成声明形态的注释会顶掉真声明、让对比度读数失真。要指代令牌时用散文描述(例如「内陷面那一档」「统一面令牌」),或用反引号包裹但**后面不接冒号**。
    - 本任务**只改注释**:`frontend/style.css` 的声明体、规则块顺序、围栏边界一字不动。
  </action>
  <verify>
    <automated>grep -cF -- 'still read as recessed' frontend/style.css</automated>
    <fails_when>the count is not "0" (the falsified clause must be gone, not merely softened)</fails_when>
    <automated>.venv/bin/python -c "import re,pathlib;t=pathlib.Path('frontend/style.css').read_text(encoding='utf-8');f=t[t.index('===== DESIGN TOKENS: START ====='):t.index('===== DESIGN TOKENS: END =====')];d=re.findall(r'(--[a-z0-9-]+)\s*:\s*([^;]+);', f);print('decls',len(d));print('unique',len(set(n for n,_ in d)))"</automated>
    <fails_when>decls is not "119" (HEAD baseline; a comment written in declaration form would add a spurious match and, because parse_decls lets the last match win, silently override a real declaration)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh</automated>
    <fails_when>non-zero exit, or the output does not contain "PASS"</fails_when>
    <automated>.venv/bin/python scripts/check-02-contrast.py</automated>
    <fails_when>non-zero exit, or the output does not end with "PASS: 0 failures", or the ORDER line is no longer "ORDER 0.363  --color-text-muted before --color-text on --color-surface"</fails_when>
    <automated>grep -c '/\* PAIR ' frontend/style.css</automated>
    <fails_when>the count is not "53" (this phase adds zero contrast pairs; --color-text ON --color-surface-page is already registered)</fails_when>
    <automated>awk '/^#latest-check \{/{f=1} f{print} f&&/^\}/{exit}' frontend/style.css</automated>
    <fails_when>the printed block does not contain exactly seven declarations (max-height / overflow-y / padding / border / border-radius / background / font-size), or its background declaration is not the unified-surface token (this task must not have touched the rule body — that was Task 1)</fails_when>
  </verify>
  <acceptance_criteria>
    - `grep -cF -- 'still read as recessed' frontend/style.css` 输出 `0`。
    - 围栏内声明匹配数(`(--[a-z0-9-]+)\s*:\s*([^;]+);`)仍为 `119`,去重后仍为 `119`。
    - 改写后的注释里能看到「旧说法为何为假」的留痕(形如「这里原先声称…,那半句现在是假的」),而不是静默删除;且注释**同时**保留了控件仍读作内陷这半句(它仍为真)。
    - `check-01` 打印 `PASS`;`check-02` 以 `PASS: 0 failures` 结尾、`ORDER` 行逐字仍为 `ORDER 0.363  --color-text-muted before --color-text on --color-surface`。
    - `grep -c '/\* PAIR ' frontend/style.css` 输出 `53`。
    - `awk '/^#latest-check \{/{f=1} f{print} f&&/^\}/{exit}' frontend/style.css` 打印的规则体恰含七条声明(max-height / overflow-y / padding / border / border-radius / background / font-size),其中 `background` 一条取统一面令牌 —— 即本任务没有碰规则体(那是 Task 1 的改动面)。
    - 注释段的改写可在 `git diff HEAD -- frontend/style.css` 里看到,且改动**全部**落在围栏注释段内(`:122-147` 区间),没有任何规则体 / 声明行被这个任务改动。
  </acceptance_criteria>
  <done>围栏 `:129-130` 那句已被证伪的断言不再在盘上;新注释按房屋写法陈述新事实、保留仍为真的那半句、并记录旧句为何为假;围栏声明数不变、`check-02` 全绿、零新增对比度条目。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 3: 两条变异证明 —— `c6` 的两个钉死半条各自「变异 → FAIL」真实读数,并在还原后证明逐字节相同</name>
  <files>scripts/check-09-idi09-validation.py, .planning/phases/idi-12-g1-band/idi-12-01-SUMMARY.md</files>
  <precondition>`git status --porcelain frontend/` 为空(Task 1 / Task 2 的改动已提交)⇒ 两条变异确实做在**已提交的树**上。</precondition>
  <read_first>
    - `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-03-SUMMARY.md`(`:193-300` 的六条变异留档形态:前置条件逐条记录、FAIL 原文逐字抄录、还原判据)**与** `idi-11-05-SUMMARY.md`(同形态的第二份)
    - `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/`(原始输出落盘约定)
    - `frontend/style.css` 的 `#latest-check` 规则体与围栏内 `--color-surface-page` / `--color-surface` / `--color-surface-sunken` 三条声明
    - `.planning/phases/idi-12-g1-band/12-CONTEXT.md` 的 D-12-7(变异的三条硬性要求)
  </read_first>
  <action>
    **本任务净产出为零代码改动,交付物是两条可复跑的「变异 → FAIL」证据。** 先逐条记录前置条件:`git status --porcelain frontend/` 为空;记下 `git rev-parse HEAD`;记下 `git hash-object frontend/style.css`;跑一次基线 `.venv/bin/python scripts/check-09-idi09-validation.py --item c6` 并记下 `exit=0` 与断言条数。

    **M1 —— 钉「两者不同」与钉「宿主 == 白」两条同时红。** 用**受控的定点改写**把 `#latest-check` 规则体内的那条底色声明改回内陷面令牌 `var(--color-surface)`。**必须是定点改写**:只替换 `#latest-check` 规则体内的那一处,`--color-surface` 的另外八处以上消费者(`:998` / `:1013` / `:1057` / `:1113` / `:1243` / `:1414` / `:1447` / `:1552` / `:1648`)一律不动 —— 用一次 Python 受控替换(先定位 `#latest-check {` 到其后第一个 `}` 的块、断言块内目标子串恰出现一次、再只替换块内那一处)即可,不要用整文件级的正则替换。随后跑 `--item c6`,**逐字抄录 FAIL 原文**(含 `expected=` / `actual=` 与 note 文案)。然后 `git checkout -- frontend/style.css` 还原,并以两条判据证明**逐字节相同**:`git diff --exit-code -- frontend/style.css` 的 `rc=0`,且 `git hash-object frontend/style.css` 与前置记录值逐字符相同。

    **M2 —— 证明「两侧钉死不是冗余」(D-12-7 的机械证据)。** 把 `#latest-check` 的底色改指 `--color-surface-sunken`(gray-3,`#f0f0f0`)。此时宿主与表头(`.markdown-body th`,gray-2)的底色**仍然不同** ⇒ 「两者不同」那条判据**保持 PASS**;而「宿主 == 白」那条必 **FAIL**。这正是 D-12-7 论证「只钉不同会被任何别的灰满足、判别力接近『只断言规则被写下了』」的实证。同样逐字抄录 FAIL 原文,并用与 M1 相同的两条判据完成定向还原与逐字节核对。

    **禁令:** 全程**不得使用 `git stash`**(它跨工作树共享,本项目明令禁止);还原一律用定向 `git checkout -- frontend/style.css`。

    **留档:** 按 `idi-11-03-SUMMARY.md` / `idi-11-05-SUMMARY.md` 的形态把两条读数写进 `idi-12-01-SUMMARY.md` —— 前置条件逐条记录(干净的工作树、`HEAD`、`hash-object`、基线 `exit=0`)、每条变异「注入什么 → 观察到的 FAIL 原文 → 还原命令与两条还原判据」,并显式写明「全程未使用 `git stash`」。
  </action>
  <verify>
    <automated>git status --porcelain frontend/</automated>
    <fails_when>output is not empty (a mutation is still applied — every mutation must have been restored)</fails_when>
    <automated>git diff --exit-code -- frontend/style.css; echo "rc=$?"</automated>
    <fails_when>rc is not "0" (frontend/style.css must be byte-identical to its committed state after both mutations)</fails_when>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c6</automated>
    <fails_when>non-zero exit, or any FAIL, or any BLOCKED, or the trailing line not starting with "exit=0"</fails_when>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4,c5</automated>
    <fails_when>non-zero exit, or any FAIL, or any BLOCKED (the Phase 11 REG-01 contract must be untouched by this phase)</fails_when>
    <automated>grep -cF -- 'git stash' .planning/phases/idi-12-g1-band/idi-12-01-SUMMARY.md; grep -cF -- 'M1' .planning/phases/idi-12-g1-band/idi-12-01-SUMMARY.md; grep -cF -- 'M2' .planning/phases/idi-12-g1-band/idi-12-01-SUMMARY.md</automated>
    <fails_when>the M1 count is "0" or the M2 count is "0" (both mutation readings must be documented); the first count being non-zero is acceptable only as the explicit "git stash was never used" prohibition note</fails_when>
    <automated>git status --porcelain scripts/</automated>
    <fails_when>output contains any path other than "scripts/check-09-idi09-validation.py"</fails_when>
  </verify>
  <acceptance_criteria>
    - `idi-12-01-SUMMARY.md` 里,M1 与 M2 各有:注入内容、**逐字**的 FAIL 原文(含 `expected=` 与 `actual=` 两个字段)、还原命令、以及两条还原判据的实际输出(`git diff --exit-code -- frontend/style.css` 的 `rc=0` 与 `git hash-object` 的十六进制串)。
    - M1 的 FAIL 原文里,「两者不同」与「宿主 == 白」两条判据**都在** FAIL 行里出现。
    - M2 的 FAIL 原文里,**只有**「宿主 == 白」那条在 FAIL 行里出现;「两者不同」那条在同一次运行的 PASS 行里出现 —— 这是本任务的核心主张,缺一不可。
    - 两条变异的 `git hash-object frontend/style.css` 还原值**相同**,且与前置记录值逐字符一致。
    - 留档里显式写明「全程未使用 `git stash`」。
    - 最终树上 `check-09 --item c6` 与 `--item c1,c2,c3,c4,c5` 均 `exit=0`、0 FAIL、0 BLOCKED。
    - `git status --porcelain frontend/` 为空。
  </acceptance_criteria>
  <done>两条「变异 → FAIL」真实读数入册:M1 证明两条钉死半条都会红,M2 证明「宿主 == 白」这半条**不可省**(「两者不同」在宿主改成 gray-3 时仍绿);两次变异都在已提交的树上做、定向还原、还原后 `git diff --exit-code -- frontend/style.css` 为空且 `hash-object` 逐字符相同;全程未用 `git stash`。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 门脚本(`scripts/check-09-idi09-validation.py`)→ 仓库的验收结论 | 门是「改动是否成立」的唯一机械判据;一条被削弱的断言会让整条链路静默失真 |
| fixture(`scripts/ui-states/checking/docs/DESIGN-check-2.md`)→ 后端文法 → 前端 UI 模式 | 该文件被 `check-05` / `check-06` / `check-07` / `check-09` / `check-10` 经 `make_fixture()` 共享消费;内容改动可翻转样本的 UI 模式 |
| 本地浏览器 → 本机 uvicorn(127.0.0.1:8765) | 门通过真实浏览器读 computed style;8765 上可能存在先前遗留的进程(复用,不新起) |
| 变异测试 → 工作树 | 变异必须只在**已提交的树**上做并定向还原;`git stash` 跨工作树共享,误用会污染其它工作树 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-12-01 | Tampering | `scripts/check-09-idi09-validation.py` 的新项 `c6` | high | mitigate | 判据**两侧钉死**(「两者不同」+「宿主 == 白」),并用**两条**变异测试证明两个半条各自可失败;`ok()` 的 `None` 期望侧会降级成 BLOCKED ⇒ 令牌解析断言一律走 `ok_true` 并显式处理 `None`,且「表头可读」是硬 FAIL 而非 BLOCKED |
| T-12-02 | Tampering | `scripts/ui-states/checking/docs/DESIGN-check-2.md`(5 条门共享的 fixture) | high | mitigate | 表**必须含至少一行 P0/P1** 使 `is_pure_p2` 为假(防 `mode` 翻成 `p2`);并新增一条运行时**模式不变量**断言(`#btn-continue-check` 不带 `.hidden` ∧ `#verdict-cards` 无 `.verdict-card`);Task 1 的 `<verify>` 另以 `backend.grammar` 直读复核 `pure_p2` / `pass_conclusion` 两个布尔 |
| T-12-03 | Tampering | 围栏内注释(`frontend/style.css:122-147`) | medium | mitigate | 改写后的围栏**声明数必须仍为 119**(`check-02` 的 `DECL_RE` 扫围栏全文含注释、`parse_decls` 最后一个匹配胜出)⇒ 该判据把「注释写成声明形态」变成可失败;配套 `check-02` 的 `PASS: 0 failures` 与 `ORDER 0.363` 不变 |
| T-12-04 | Tampering | 变异测试对工作树的写入 | medium | mitigate | 变异只做在**已提交的树**上;还原用定向 `git checkout -- frontend/style.css`,并以 `git diff --exit-code -- frontend/style.css` 为 `rc=0` **且** `git hash-object` 逐字符相同作为逐字节判据;**`git stash` 全程禁用** |
| T-12-05 | Information Disclosure | 本轮无新增提交物携带本地绝对路径(截图与日志属 Phase 12 计划 02 / 03) | low | accept | 本仓库是单机单人本地仓库,且 v1.15 两个阶段已按同一口径提交过 `screenshots/` 与 `gate-logs/`;本计划不新增此类产物 |
| T-12-SC | Tampering | npm / pip / cargo 安装 | low | accept | 本阶段**零新增依赖**(DESIGN.md D-06 零构建步骤 / 零新增运行时依赖;`scripts/` 全部复用既有 `.venv` 与 Playwright 自带 chromium)⇒ 无安装动作,无包合法性门可触发 |
</threat_model>

<verification>
**整体阶段检查(本计划收口时):**

1. `bash scripts/check-01-token-conformance.sh` → `PASS`;`bash scripts/check-03-hidden-uniqueness.sh` → `PASS`;`bash scripts/check-04-important-count.sh` → `PASS`。
2. `.venv/bin/python scripts/check-02-contrast.py` → 以 `PASS: 0 failures` 结尾,`ORDER 0.363` 行逐字不变,`grep -c '/\* PAIR ' frontend/style.css` == 53。
3. `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4,c5,c6` → `exit=0`、0 FAIL、0 BLOCKED(`c1..c5` 是 Phase 11 的 `REG-01` 契约,本阶段必须保持全绿;`c6` 是新增)。
4. `git status --porcelain frontend/ scripts/ backend/ frontend/vendor/` → 只列出 `frontend/style.css`、`scripts/check-09-idi09-validation.py`、`scripts/ui-states/checking/docs/DESIGN-check-2.md`。
5. `git diff --stat -- frontend/app.js frontend/index.html backend/ frontend/vendor/` → 空。
6. `idi-12-01-SUMMARY.md` 含两条变异读数与前置条件记录。
</verification>

<success_criteria>
- `#latest-check` 内的表头在真实浏览器里读作**一条独立的 band**:宿主计算底色(`rgb(255, 255, 255)`)与表头计算底色(`rgb(249, 249, 249)`)不同,且宿主底色同时等于统一面令牌的解析值与写死的白字面量。
- `checking` 样本的 fixture 报告忠于后端文法(`## 问题分级` 标题 + 逐字表头 + 至少一行 P0/P1),样本 UI 模式仍为 `running`。
- 新判据 `c6` 就位且**经两条变异证明会失败**;既有 `c1..c5` 零删除、零降级。
- 围栏承重注释已就地改写,声明数不变,`check-02` 零新增条目、零阈值改动。
- `frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**` 逐字节未改。
</success_criteria>

<output>
Create `.planning/phases/idi-12-g1-band/idi-12-01-SUMMARY.md` when done
</output>

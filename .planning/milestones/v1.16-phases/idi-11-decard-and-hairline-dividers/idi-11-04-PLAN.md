---
phase: idi-11-decard-and-hairline-dividers
plan: 04
type: execute
wave: 4
depends_on:
  - idi-11-01
  - idi-11-02
  - idi-11-03
files_modified:
  - scripts/check-05-ui-uat.py
autonomous: true
requirements:
  - REG-03

estimate:
  tokens: 70000
  raw_tokens: 70000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- REG-03 — sticky 余量复测与登记 ----
    - "`check-05 --item 8` 在 `#doc-panel` 边界改动后**已复跑**,余量读数与成因**已登记**:HEAD 上该断言实测 `1.000px`(成因是 Phase 9 给 `#doc-panel` 加的那条 1px **上**边框 —— 滚动容器的 padding box 顶边离边框盒 `border-top-width` 那么远);本阶段把四边边框收成单边 `border-left` 后,预期读数变为 `0.000px`。该断言是**容差**(`abs(header.top - panel.top) <= 1.0`)不是等值,故 `0.000px` **仍 PASS**"
    - "**「事实是否被改变」的分诊已做,且结论写进 SUMMARY**:该断言描述的事实是「sticky 表头遮挡滚动正文」—— 本阶段只改 `#doc-panel` 的边框与底色,并给 `#main-pane` 加横线、把 `gap` 归零,但 `#doc-panel-header` 的 `position: sticky` / `top: 0` / `background` 三条逐字未动 ⇒ **该事实未被改变**。故处置是**只更新余量读数与成因登记**,**不是**改判据。**不得为了让旧数字继续成立而把那 1px 加回去**(D-11-16 的显式禁令)"
    - "`check-05 --item 8` 复跑后为 `PASS`,`0 FAIL`,`0 BLOCKED`,断言计数与 HEAD 基线**一致**(13 条);那条断言的容差字面量 `<= 1.0` 逐字未改"
    # ---- `.hint` 断言的期望侧重登记(本计划唯一的 `check-05` 代码改动) ----
    - "`check-05` 里那条「`.hint` 实际背景 == <卡片底色令牌>」的断言,其**期望侧**已改指统一面令牌(`resolve_color(page, \"--color-surface-page\")`),标签文本同步更新。**断言形式一字未变** —— 仍是「实测 computed 值 == 运行时解析的令牌值」的**精确等值**,不是放宽、不是 `ok_contains`、不是非透明判据、不是硬编码 rgb、不是 `or` 分支"
    - "**为什么必须改而不是放着**:被删的卡片底色令牌一旦不再声明,`resolve_color` 返回 `None`,而 `ok()` 在**期望侧为 `None`** 时记 **BLOCKED**(不是 FAIL)—— 该断言会**静默地从「在检查」退化成「不知道」**。`check-05` 的整体退出码本来就是 2(两条 `--ai-smoke` 腿按设计 BLOCKED),所以**门不会变红**,没人会注意到这条断言已经死了。这正是本仓库反复付过代价的「门绿着在看」形态,故必须修"
    - "**这与 Phase 9 的处置是同一条纪律、同一行代码**:Phase 9 把这条断言的期望侧由内陷面令牌换指到卡片令牌,并逐字记下「这是**重新登记**(期望侧换指到本阶段刻意改变的那条事实),断言形式一字未变 —— 仍是精确等值,不是放宽」。Phase 11 把地面**又**移动一次(卡片并回页面),故按同一条纪律再登记一次"
    # ---- 全门复跑(本阶段的收口证据) ----
    - "五条浏览器门(`check-05` 全量 / `check-06` / `check-07` / `check-09` / `check-10`)+ 两个探针(`probe-05` / `probe-07`)+ 四个静态门(`check-01`…`check-04`)+ pytest 基线 + `node --check frontend/app.js` 逐条复跑,**零新增失败**;每条门的**原始输出与退出码**落盘到 `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/`(13 个文件,一个门一个,文件名即门的名字 —— Phase 10 的同形先例)"
    - "`check-05` **全量**运行的 `exit=2` **仍只因 item 5 的两条 `--ai-smoke` 腿按设计 BLOCKED**,不是回归;item 5 的 BLOCKED 计数必须仍为 **2**(不得因为期望侧解析不出而变成 3 —— 那正是 Task 1 要消除的形态)"
    - "pytest 基线不降:`.venv/bin/python -m pytest backend/tests -q --tb=short` → **219 passed / 6 skipped**(必须用项目 `.venv`;环境 `python3` 是 miniconda,会让 4 个 `ai_caller` 测试假失败)"
    - "每一条**读数变化**都被分诊,不是被静默重述:凡某项的断言计数或读数与基线不同,SUMMARY 里给出「改前 → 改后」两列**并说明机制**(本阶段改了容器绘制面与面板间距,故几何类读数**允许**变化,但必须有机制解释;任何 FAIL 或**新增** BLOCKED 都是缺口,须停下报回)"
    # ---- 连带指纹面(实测,不凭记忆) ----
    - "连带指纹面**在磁盘上逐份实测**过,判据锚报告 frontmatter 的 `covered_files` **逐行匹配**(**不是**全文 grep —— 全文 grep 会把只在正文提及的报告算进来),并**额外测「路径是否还在盘上」**。规划期实测:`frontend/style.css` 被 **11** 份 `passed` 报告列入 `covered_files`;`scripts/check-09-idi09-validation.py` 被 **1** 份;`scripts/check-02-contrast.py` 被 **1** 份;`scripts/check-05-ui-uat.py` 被 **7** 份。**这 11 份全部已 fail-closed stale**(每份的 `covered_files` 里都有归档后不可解析的 `.planning/phases/...` 路径)⇒ 本阶段**不新制作废**任何原本可执行的报告。执行期须**重新实测**这一形状(份数可能因归档而变)"
    - "**`REG-04` 的正式处置归 Phase 12**(本阶段只**实测并登记**连带面,不做重验、不刷新任何指纹)。本阶段的连带面记录是 Phase 12 `REG-04` 的输入"

  artifacts:
    - path: "scripts/check-05-ui-uat.py"
      provides: "`.hint` 实际背景断言的期望侧重登记到统一面令牌(断言形式一字未变);注释同步改写,记下「这是重新登记、不是放宽」与「为什么必须改(ok() 的 None 期望侧降级成 BLOCKED,门不会变红)」"
      contains: "resolve_color(page, \"--color-surface-page\")"
    - path: ".planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/"
      provides: "五条浏览器门 + 两个探针 + 四个静态门 + pytest + node --check 的原始输出与退出码,一个门一个文件(13 个)"
      contains: "=== 逐项结论 ==="

  key_links:
    - from: "`scripts/check-05-ui-uat.py` 的 `.hint` 实际背景断言"
      to: "围栏内 `--color-surface-page: var(--white);`"
      via: "期望侧由 `resolve_color` 运行时解析 —— 地面从卡片令牌搬到统一面令牌后,期望侧必须同步换指,否则 `ok()` 在期望侧为 `None` 时降级成 BLOCKED(门不会变红,断言静默死亡)"
      pattern: "resolve_color\\(page, \"--color-surface-page\"\\)"
    - from: "`check-05 --item 8` 的 sticky 余量断言"
      to: "`#doc-panel` 由四边边框收成单边 `border-left` 的几何后果"
      via: "滚动容器的 padding box 顶边离边框盒 `border-top-width` 那么远 ⇒ 移除 1px 上边框把读数从 `1.000px` 带到 `0.000px`(仍 `<= 1.0`)"
      pattern: "abs\\(hp\\[\"top\"\\] - pp\\[\"top\"\\]\\) <= 1\\.0"
    - from: "本阶段的 `gate-logs/`"
      to: "Phase 10 的 `gate-logs/`(同形先例与逐项对照基线)"
      via: "逐项断言计数与退出码的并排对照 ⇒ 「零新增失败」有原始证据,不是「看着一样」"
      pattern: "item 8: PASS"

  prohibitions:
    - statement: "不得为了让门绿、或为了让某个旧读数继续成立,而删除 / 降级 / 放宽任何断言、阈值或判据,也不得回退已裁定的产品改动。`check-05 --item 8` 的余量若变为 `0.000px`,那是**事实被如实登记**,不是回归 —— **不得把 1px 上边框加回去**以恢复 `1.000px`"
      status: active
      verification: flagged
    - statement: "不得把「期望侧重登记」做成「放宽」。`.hint` 断言的期望侧只换令牌,断言形式必须仍是「实测 computed 值 == 运行时解析的令牌值」的**精确等值**;禁止改成 `ok_contains` / 非透明判据 / 硬编码 rgb / `or` 分支 / 删除该断言"
      status: active
      verification: flagged
    - statement: "不得在本阶段处置 `REG-04` 的连带指纹(以 HEAD 内容重新验证、刷新指纹等)。`REG-04` 归 Phase 12 —— 本阶段只**实测并登记**连带面。也不得改 `check-05` 的其它任何一行:本次改动的**唯一**理由是那条断言会静默死亡,且已实测其覆盖者**全部**已是 fail-closed stale ⇒ 零边际成本"
      status: active
      verification: flagged
---

<objective>
收口本阶段的三件事:把 `check-05` 里一条会**静默死亡**的断言重新登记、复测并登记 `check-05 --item 8` 的 sticky 余量(REG-03),以及把全部门在最终树上复跑一遍并把原始输出落盘。

**Purpose 一:** `check-05` 有一条断言「`.hint` 实际背景 == <卡片底色令牌>」,其期望侧走 `resolve_color` 运行时解析。本阶段删除了那个令牌 ⇒ `resolve_color` 返回 `None` ⇒ `ok()` 在**期望侧为 `None`** 时记 **BLOCKED**(不是 FAIL)。`check-05` 的整体退出码本来就是 2(两条 `--ai-smoke` 腿按设计 BLOCKED),所以**门不会变红**,这条断言会静默地从「在检查」退化成「不知道」。本仓库的立场是「一条不能失败的门比没有门更糟」,故必须按 **Phase 9 处置同一行代码的同一纪律**再登记一次。

**Purpose 二:** `REG-03` 指名处置 `check-05 --item 8` 的 sticky 余量 —— HEAD 上实测恰 `1.000px`,成因正是 Phase 9 给 `#doc-panel` 加的那条 1px 上边框,而本阶段移除该边框正是该读数变化的唯一原因。按 D-11-16 的分诊规则:**先问「事实是否被改变」** —— 该断言描述的事实(sticky 表头遮挡滚动正文)未被改变,故只更新余量读数与成因登记,**不得为了让旧数字成立而回退产品改动**。

**Purpose 三:** Phase 11 的 Gates 行要求「五条浏览器门复跑无新增失败」。本阶段改的正是容器绘制面,故复跑是**唯一**能证明回归面未破的证据;原始输出落盘使该结论可独立复核(不是「看着一样」)。

**本计划关闭的需求:** REG-03。

**本计划不触碰:** `frontend/style.css`(已在波次 1/2 定型,零改动);`scripts/check-09-idi09-validation.py`(计划 03 已收口,零改动);`scripts/check-02-contrast.py` / `check-10` / `check-01…04` / `check-06` / `check-07` / `probe-*`(零改动);`check-05` 的**其它任何一行**;`frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**`(零字节);`G1-01` / `REG-04` / `VIS-01`(Phase 12);G2 / `999.2` / 暗色模式 / Nyquist 缺口 / 图标与空状态 / `.overlay-card` 底色(全部 Out of Scope)。

## ⚠ 与编排器指令 C-2 的显式偏离(须由计划评审者裁定)

规划期收到的指令 **C-2** 写着:「`scripts/check-05-ui-uat.py` **NOT** need modification. **Do not touch it.**」并给出理由:「改它会把它自己的覆盖者拖进重验名单(**7** 份,含 `idi-08` —— Phase 10 曾以「不得改它」避免把 `idi-08` 拖进来)」。

**该指令针对的是 `--item 8` 的 sticky 断言,而那条断言确实不需要改(它是容差,`0.000px` 仍通过)。但 C-2 的覆盖面漏了一条:** `check-05` 还有一条断言(`[p1] .hint 实际背景 == var(--color-surface-card)`)的**期望侧**读的正是本阶段要删除的令牌。删除后该断言会静默退化成 BLOCKED。规划期已实测:

| 证据 | 实测结果 |
|---|---|
| HEAD 上 `.venv/bin/python scripts/check-05-ui-uat.py --item 5 --item 8 --browser bundled` | `PASS [p1] .hint 实际背景 == var(--color-surface-card): expected=rgb(255, 255, 255) actual=rgb(255, 255, 255)`;`item 5: BLOCKED  (9 条断言,0 FAIL,2 BLOCKED)`;`exit=2` |
| 删令牌后该断言的走向 | `resolve_color` 返回 `None` ⇒ `ok()` 走 `expected is None` 支 ⇒ 记 **BLOCKED** ⇒ `item 5` 变成 `0 FAIL,3 BLOCKED`,**退出码仍是 2** ⇒ 门不会变红 |
| C-2 给出的成本理由 | **已失效**。规划期逐份解析 7 份覆盖报告 frontmatter 的 `covered_files` 并逐条测「路径是否还在盘上」:`idi-04.1` 缺 8/12、`idi-05` 缺 8/11、`idi-06` 缺 8/10、`idi-07` 缺 6/9、`idi-08` 缺 6/10、`idi-09` 缺 6/10、`quick/260925-iin` 缺 2/7 —— **7 份全部已是 fail-closed stale**(归档后 `.planning/phases/...` 路径不可解析,属 2026-09-14 登记的已知限制)⇒ 改 `check-05` 的**边际重验成本为零** |
| 同文件先例 | STATE.md 记着 Phase 9 对**同一行代码**的处置:「「重新登记」≠「放宽」—— `check-05` 的 `[p1] .hint 实际背景` 断言的期望侧由 `--color-surface` 换指 `--color-surface-card`,断言形式(与运行时解析值精确等值)一字未变」 |

**结论与请求:** 本计划按 Phase 9 的同一条纪律把该断言的期望侧换指到统一面令牌(**唯一的代码改动是一处期望侧令牌名 + 相邻注释**)。若计划评审者/用户裁定 C-2 优先,替代处置是**保留该断言不动、在 SUMMARY 里登记它的静默退化**(即 item 5 的 BLOCKED 由 2 变 3),并把这条登记交给 Phase 12 的 `REG-04`。**不得**在两条路之间无声地择一 —— Task 1 的 `<done>` 要求把实际选择与理由写进 SUMMARY。

**执行前对照基线(取自 Phase 10 落盘的 `gate-logs/`;执行器须复核):**

| 门 | Phase 10 落盘的对照基线(本阶段改动前) | 本阶段预期 |
|---|---|---|
| `check-05` 全量 | `item 1: 45` / `2: 5` / `3: 17` / `4: 65` / **`5: BLOCKED (9, 2 BLOCKED)`** / `6: 6` / `7: 38` / **`8: PASS (13)`** / `9: 17` / `10: 42`;`exit=2` | 零新增 FAIL;item 5 仍 `2 BLOCKED`;item 8 仍 `PASS`;几何类读数**允许**变化但须有机制解释 |
| `check-06` | `g1: 9` / `g2: 2` / `g3: 12` / `g4: 5` / `g5: 5` / `g6: 7`;`exit=0` | `exit=0`,零新增 FAIL |
| `check-07` | `g1: 21` / `g2: 39` / `g3: 10` / `g4: 3`;`exit=0` | `exit=0`,零新增 FAIL |
| `check-10` | `t1: 58` / `t2: 51` / `r1: 11` / `r2: 10` / `shot: 7`;`exit=0` | `exit=0`,零新增 FAIL(`t1`/`t2` 断言表格表头画内陷面令牌,本阶段不动表格) |
| `probe-05` / `probe-07` | 各 `EXIT=0`;`probe-07` 的焦点环地面 `rgb(255, 255, 255)`、合成比 `3.54` | 各 `EXIT=0`;地面仍是白(统一面 = 白)⇒ 比值仍 `3.54` |
| pytest | `219 passed, 6 skipped` | 不降(必须用项目 `.venv`) |
| `check-01`…`check-04` | 全 `PASS` / exit 0 | 全 `PASS` |

**对照基线的来源(不得凭记忆):** `.planning/milestones/v1.15-phases/idi-10-tables-and-radius-scale/gate-logs/`(13 个日志文件,Phase 10 落盘)。本阶段的 `gate-logs/` 与它**同形**,使两阶段可逐项并排对照。

Output: `scripts/check-05-ui-uat.py` 的一处期望侧重登记 + 相邻注释改写;`REG-03` 的 sticky 余量新读数与成因登记;`.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/` 下 13 个日志文件;连带指纹面的实测记录。
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
@.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-03-PLAN.md
@.planning/milestones/v1.15-phases/idi-10-tables-and-radius-scale/gate-logs/check-05-full.log
@scripts/check-05-ui-uat.py
@frontend/style.css
</context>

## Artifacts this phase produces

> 本节列出**本计划**那部分;全阶段的产出表在 `idi-11-01-PLAN.md` 的 §「Artifacts this phase produces」,不重复。

**新增目录:** `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/` —— 13 个日志文件:

`check-01-token-conformance.log` / `check-02-contrast.log` / `check-03-hidden-uniqueness.log` / `check-04-important-count.log` / `check-05-full.log` / `check-06-idi05-validation.log` / `check-07-idi08-validation.log` / `check-09-idi09-validation.log` / `check-10-idi10-validation.log` / `pytest.log` / `node-check-app.log` / `probe-05-resolve-color.log` / `probe-07-focus-composite.log`。

**就地改写的既有断言(计划 04):**

| # | 符号 | 锚点 | 动作 |
|---|---|---|---|
| 1 | `[p1] .hint 实际背景 == <令牌>` 断言的**期望侧** | `scripts/check-05-ui-uat.py` 的 `item5()` 内,标签文本以 `[p1] .hint 实际背景 ==` 开头的那一条 | 期望侧由被删的卡片底色令牌改为 `resolve_color(page, "--color-surface-page")`;标签文本与相邻注释同步改写。**断言形式一字未变** |

**本计划不产生的新符号:** 零新增函数、零新增常量、零新增门、零新增探针、零新增依赖。`check-05` 的改动面**只有**上面那一处期望侧 + 相邻注释。

## 波次与依赖形状

| 波次 | 计划 | 为什么必须在这个位置 |
|---|---|---|
| 4 | `idi-11-04`(本计划) | 复跑必须看到**全部**改动(波次 1/2 的 `style.css` 与波次 3 的 `check-09`);且 `check-05` 的改动与 `check-09` 的改写同属「门禁同步」,复跑是它们的收口证据 |

<tasks>

<task type="auto" tdd="false">
  <name>Task 1: `check-05` 的 `.hint` 实际背景断言期望侧重登记(断言形式一字未变)</name>
  <files>scripts/check-05-ui-uat.py</files>
  <reversibility rating="reversible">回退是把一处期望侧的令牌名换回去(并恢复相邻注释),不牵连其它产物。</reversibility>
  <read_first>
    - `scripts/check-05-ui-uat.py` 的 `item5()` 函数全文 —— 逐字读那条标签以 `[p1] .hint 实际背景 ==` 开头的断言、它上方那段解释「`.hint` 自身无背景,沿祖先链取到的实际底色。实测:命中的是 index.html 里 `#doc-panel-body` → `#doc-panel` 内的那条。Phase 9 卡片化之后 `#doc-panel` 画的是 …(卡片白),故实际地面是卡片表面,不再是 `--color-surface`。这是**重新登记**(期望侧换指到本阶段刻意改变的那条事实),断言形式一字未变 —— 仍是「实测 computed 值 == 运行时解析的令牌值」的精确等值,不是放宽。」的注释(**本任务要改写的对象**)
    - `scripts/check-05-ui-uat.py` 的 `ok()` 实现 —— 逐字读它的 `expected is None` → **BLOCKED** 那一支及其 docstring(「expected 为 None 表示**期望值解析不出**(如令牌未声明)→ 同样记 BLOCKED」)
    - `scripts/check-05-ui-uat.py` 的 `resolve_color()` 实现 —— 逐字读它「令牌**未声明**时返回 `None`」那一支
    - `scripts/check-05-ui-uat.py` 的 `effective_bg()` 实现 —— 沿祖先链找第一个非透明 `background-color`
    - `frontend/index.html` 的 `#doc-panel-body` 段 —— 确认 `.hint` 的第一个实例(`<p class="hint">讨论文档由 AI 直接读写该目录下的 docs/ 子目录。</p>`)在 `#doc-panel-body` 内 ⇒ 其最近的不透明祖先是 `#doc-panel`
    - `frontend/style.css` 的 `#doc-panel` 规则(计划 01 已改:`background: var(--color-surface-page);`)与围栏内 `--color-surface-page: var(--white);`
    - `.planning/STATE.md` 的 `[Phase idi-09]` 决策条目里关于「「重新登记」≠「放宽」」那一条(**本任务引用的先例原文**)
    - `.planning/phases/idi-11-decard-and-hairline-dividers/11-CONTEXT.md` §D-11-2 与 §「Claude's Discretion」的 `REG-04` 连带指纹面一条
    - `.planning/ROADMAP.md` §`### Phase 11:` 的 Gates 行(「五条浏览器门复跑无新增失败」)
  </read_first>
  <action>
    **第 1 步 —— 先复现退化,再改。** 跑一次 `.venv/bin/python scripts/check-05-ui-uat.py --item 5 --browser bundled`,把 `=== 逐项结论 ===` 与那条断言的输出行原文抄进 SUMMARY。预期此刻该断言已记 **BLOCKED**(期望侧解析不出),`item 5` 变成 `0 FAIL,3 BLOCKED`。**这一步不是可选的** —— 它是「这条断言真的会静默死亡」的实测证据,而不是推断。

    **第 2 步 —— 换期望侧,断言形式一字不变。**

    在 `item5()` 里,把那条标签以 `[p1] .hint 实际背景 ==` 开头的断言的**期望侧**由被删的卡片底色令牌改为 `resolve_color(page, "--color-surface-page")`;标签文本里被删的令牌名同步改为统一面令牌名。**只改期望侧与标签文本**:

    - 断言函数仍是 `ok(...)`(**不得**改成 `ok_true` / `ok_contains` / 任何别的形态);
    - 实际侧仍是 `effective_bg(page, ".hint")`(一字不动);
    - 比较语义仍是「实测 computed 值 == 运行时解析的令牌值」的**精确等值**(**不得**改成非透明判据 / 硬编码 rgb / `or` 分支);
    - **不得**删除这条断言。

    **第 3 步 —— 改写相邻注释。**

    把注释里「Phase 9 卡片化之后 `#doc-panel` 画的是 …(卡片白)」那段历史改写为两段:Phase 9 把地面搬到卡片令牌,Phase 11 把卡片地面并回统一面 ⇒ 期望侧再次换指。**逐字保留**「这是**重新登记**……断言形式一字未变 —— 仍是精确等值,不是放宽」这句立场,并**新增**一句说明为什么必须改:`ok()` 在期望侧为 `None` 时记 BLOCKED,而 `check-05` 的退出码本来就因两条 `--ai-smoke` 腿为 2 ⇒ **门不会变红**,这条断言会静默退化。这一句是留给后人的关键线索,不得省略。

    **第 4 步 —— 复跑并确认恢复。**

    `.venv/bin/python scripts/check-05-ui-uat.py --item 5 --browser bundled`。要求:
    - 该断言恢复为 `PASS`,`expected=actual=rgb(255, 255, 255)`;
    - `item 5: BLOCKED  (9 条断言,0 FAIL,2 BLOCKED)` —— BLOCKED 计数**必须回到 2**(3 就是退化未消除);
    - `exit=2`(设计如此:两条 `--ai-smoke` 腿)。

    **第 5 步 —— 确认 `check-05` 的改动面只有这一处。** `git diff -- scripts/check-05-ui-uat.py` 人工逐行核对:只应出现「期望侧令牌名 + 标签文本 + 相邻注释」三处,不得有任何别的行被改动(其它 item、`ok()`、`resolve_color()`、`STATES`、`ITEMS` 一律逐字不动)。

    **第 6 步 —— 把实际选择写进 SUMMARY。** 若采用了本计划的主路线,写清理由与实测证据(见 objective 的偏离说明表);若裁定 C-2 优先而保留断言不动,则登记它的静默退化并把该条交 Phase 12 的 `REG-04`。**不得**在两条路之间无声择一。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 5 --browser bundled 2>&1 | grep -E '\.hint 实际背景|item 5:|^exit='</automated>
    <fails_when>the `.hint` line does not read "PASS" with `expected=rgb(255, 255, 255) actual=rgb(255, 255, 255)`, or the summary line does not read exactly "item 5: BLOCKED  (9 条断言,0 FAIL,2 BLOCKED)" (a BLOCKED count of 3 means the assertion is still degraded; a FAIL means the ground genuinely changed and needs diagnosis)</fails_when>
    <automated>grep -nF -- 'resolve_color(page, "--color-surface-page")' scripts/check-05-ui-uat.py</automated>
    <fails_when>no such line is found on the `.hint` background assertion's expected side</fails_when>
    <automated>git --no-pager diff -U0 -- scripts/check-05-ui-uat.py</automated>
    <fails_when>the diff touches any line outside the `.hint` background assertion's expected side, its label text, and its adjacent comment block — print the diff and eyeball it; a broader diff means unrelated lines were changed</fails_when>
    <automated>git diff --stat -- scripts/check-09-idi09-validation.py scripts/check-02-contrast.py scripts/check-10-idi10-validation.py frontend/style.css</automated>
    <fails_when>output is not empty (this task changes only scripts/check-05-ui-uat.py)</fails_when>
  </verify>
  <acceptance_criteria>
    - `check-05 --item 5 --browser bundled` 的该断言为 `PASS`,`expected=actual=rgb(255, 255, 255)`;`item 5` 的 BLOCKED 计数回到 **2**;`exit=2`。
    - 期望侧为 `resolve_color(page, "--color-surface-page")`;实际侧仍为 `effective_bg(page, ".hint")`;断言函数仍为 `ok(...)`;**精确等值**语义未变。
    - 相邻注释含「这是重新登记、断言形式一字未变、不是放宽」与「`ok()` 在期望侧为 `None` 时记 BLOCKED ⇒ 门不会变红 ⇒ 断言会静默退化」两句。
    - `git diff -- scripts/check-05-ui-uat.py` 的改动面只有期望侧令牌名 + 标签文本 + 相邻注释三处;其它行逐字未动。
    - `git diff --stat -- scripts/check-09-idi09-validation.py scripts/check-02-contrast.py scripts/check-10-idi10-validation.py frontend/style.css` 为空。
    - SUMMARY 里写清了实际选择(主路线或 C-2 优先路线)与其证据/理由,并附上第 1 步复现退化的原始输出。
  </acceptance_criteria>
  <done>`check-05` 那条会静默死亡的断言已按 Phase 9 的同一纪律重新登记(期望侧换指统一面令牌、断言形式一字未变);复跑后 `item 5` 的 BLOCKED 计数回到 2、`exit=2`;改动面经逐行核对只有期望侧 + 标签 + 相邻注释;实际选择与理由已写入 SUMMARY。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 2: REG-03 —— `check-05 --item 8` 的 sticky 余量复测与成因登记</name>
  <files>scripts/check-05-ui-uat.py</files>
  <reversibility rating="reversible">本任务默认零代码改动;若判据确实需要更新,回退是恢复那一处并重跑。</reversibility>
  <read_first>
    - `scripts/check-05-ui-uat.py` 的 `item8()` 全文 —— 逐字读那条标签为 `[p1] sticky 把 #doc-panel-header 钉在 #doc-panel 顶部(<=1px)` 的断言(`abs(hp["top"] - pp["top"]) <= 1.0`)、它上方的 `INFO item8 sticky 原始数值` 诊断行、以及相邻的「header.bottom > panel.top 且 header.top < panel.bottom」那条断言
    - `frontend/style.css` 的 `#doc-panel` 规则(计划 01 已改:仅 `border-left` 一条 1px 边框)与 `#doc-panel-header` 规则(`position: sticky;` / `top: 0;` / `background: …`)
    - `.planning/STATE.md` 的 `## Blockers/Concerns` 里那条「`check-05 --item 8` 的 sticky 断言余量为零(Phase 9 计划 01 引入,已实测坐实)」—— **本任务要更新的就是它描述的那个读数**
    - `.planning/phases/idi-11-decard-and-hairline-dividers/11-CONTEXT.md` §D-11-16(**分诊规则的逐字表述**)与 §D-11-9 的连带后果第 ② 条(「`#doc-panel` 由四边 border 收成单边 border-left,content box 水平 +1px、垂直 +2px —— 这正是 `REG-03` 要登记的 sticky 余量变化成因」)
    - `.planning/REQUIREMENTS.md` 的 `REG-03` 逐字
    - `.planning/ROADMAP.md` §`### Phase 11:` 的 Success Criterion 4 末句与 Gates 行
  </read_first>
  <action>
    **第 1 步 —— 复跑并抄录原始读数。**

    `.venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled`。把 `INFO item8 sticky 原始数值` 那一行与 `=== 逐项结论 ===` 的 `item 8` 行**原文**抄进 SUMMARY。

    预期:`header.top` 由 HEAD 的 `1` 变为 `0` ⇒ `abs(header.top - panel.top)` 由 `1.000px` 变为 **`0.000px`**;`item 8: PASS  (13 条断言,0 FAIL,0 BLOCKED)`。

    **第 2 步 —— 做 D-11-16 的「事实是否被改变」分诊,并把结论写死。**

    该断言描述的事实是:**sticky 表头遮挡滚动正文**。逐条回答并写进 SUMMARY:
    - 本阶段改了 `#doc-panel` 的**边框**与**底色**,并给 `#main-pane` 加了横线、把 `gap` 归零。**这些改动有没有改变「滚动正文会从表头底下穿过」这件事?** 没有 —— `#doc-panel-header` 的 `position: sticky` / `top: 0` / `background` 三条逐字未动(计划 01 Task 2)。
    - 余量读数为什么变?**机制**:滚动容器的 padding box 顶边离边框盒 `border-top-width` 那么远;移除那条 1px **上**边框把顶边对齐到边框盒顶边,故 `header.top - panel.top` 从 `1` 变为 `0`。这是**几何的如实变化**,不是回归。
    - 因此处置是:**只更新余量读数与成因登记**,判据本身不动。

    **第 3 步 —— 判据更新的条件分支(默认不触发)。**

    **默认路径:零代码改动。** 断言是**容差**(`<= 1.0`)不是等值,`0.000px` 通过,故 `check-05` 一行都不用改。

    **仅在读数不再成立(即该断言 FAIL)时才走这一支**:先按第 2 步回答「事实是否被破坏」。若事实仍成立而读数越界(例如某个 1px 级几何副作用把读数推到 `1.0` 以上),按 D-11-16 **同步更新判据并说明改了什么** —— 但**先停下判因**,把原始读数与机制写进 SUMMARY 报回,不要径直改数字。**绝不允许**为了让旧数字继续成立而把 1px 上边框加回 `#doc-panel`。

    **第 4 步 —— 确认本任务对 `check-05` 零新增改动(默认路径)。**

    `git diff --stat -- scripts/check-05-ui-uat.py` 应只反映 Task 1 的那一处。**本任务不得引入新的改动。**

    **第 5 步 —— 登记进 SUMMARY。** 内容必须包含:HEAD 读数(`1.000px`)、本阶段读数、成因机制、分诊结论(事实未变)、以及「未回退任何产品改动」的明确陈述。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled 2>&1 | grep -E 'INFO item8 sticky 原始数值|item 8:|^exit='</automated>
    <fails_when>the summary line does not read exactly "item 8: PASS  (13 条断言,0 FAIL,0 BLOCKED)", or the INFO line is missing. (If the sticky assertion FAILs, STOP: report the raw reading and the mechanism instead of reverting the border — restoring the 1px to recover the old number is explicitly forbidden)</fails_when>
    <automated>grep -nF -- 'abs(hp["top"] - pp["top"]) <= 1.0' scripts/check-05-ui-uat.py</automated>
    <fails_when>no such line is found, or its tolerance was changed from 1.0 (the tolerance must stay byte-identical; the reading changed, the criterion did not)</fails_when>
    <automated>git --no-pager diff --stat -- frontend/style.css</automated>
    <fails_when>output is not empty (no product change may be introduced by this task, least of all restoring the removed 1px top border)</fails_when>
  </verify>
  <acceptance_criteria>
    - `check-05 --item 8 --browser bundled` → `item 8: PASS  (13 条断言,0 FAIL,0 BLOCKED)`;`INFO item8 sticky 原始数值` 原文入册。
    - SUMMARY 里并排给出 HEAD 读数(`1.000px`,成因是 Phase 9 加的 1px 上边框)与本阶段读数,并写明**机制**(padding box 顶边离边框盒 `border-top-width`)。
    - SUMMARY 里写明 D-11-16 的分诊结论:**事实(sticky 表头遮挡滚动正文)未被改变** ⇒ 只更新读数与成因登记,判据不动。
    - 那条断言的容差字面量 `<= 1.0` **逐字未改**。
    - 本任务**未**改动 `frontend/style.css`(`git diff --stat -- frontend/style.css` 为空);**未**把任何 1px 边框加回去。
    - 若读数不成立,SUMMARY 里保留了原始读数与机制并报回,且未自行改判据。
  </acceptance_criteria>
  <done>`check-05 --item 8` 在 `#doc-panel` 边界改动后复跑并 PASS;余量新读数与成因机制已登记;D-11-16 的「事实是否被改变」分诊已做且结论写死(事实未变 ⇒ 只更新读数);容差与产品代码均未为迁就旧数字而回退。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 3: 全门复跑与原始日志落盘 + 连带指纹面实测登记</name>
  <files>scripts/check-05-ui-uat.py</files>
  <reversibility rating="reversible">本任务只跑命令、写日志与登记,不产生产品代码改动。</reversibility>
  <read_first>
    - `.planning/milestones/v1.15-phases/idi-10-tables-and-radius-scale/gate-logs/` 的**文件清单与命名**(13 个文件)—— 本任务的落盘格式模板
    - `.planning/milestones/v1.15-phases/idi-10-tables-and-radius-scale/gate-logs/check-05-full.log` 的 `=== 逐项结论 ===` 块与 `[gsd] EXIT=` 行 —— **逐项对照基线**
    - `scripts/` 的**磁盘清单**(以磁盘现状为准:`check-01`…`check-07` + `check-09` + `check-10`,外加 `probe-05` / `probe-07` / `probe-card-border-token` / `probe-menu-modal-reachability`)。**没有 `check-08`** —— 不得为了对上清单去造一个
    - `.planning/ROADMAP.md` §`### Phase 11:` 的 Gates 行与 Avoids 第 7 条(连带指纹的判据口径)
    - `.planning/STATE.md` 的 `## Blockers/Concerns` 里关于连带指纹面的两条 Open 条目与「`state.*` 写入动词全部不可信」那一条
    - `scripts/check-05-ui-uat.py` 的 `STATES` 常量(五个样本)与 `--browser` 参数的取值
  </read_first>
  <action>
    **第 1 步 —— 建日志目录并逐门落盘。**

    建 `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/`。逐条运行下列命令,把**标准输出 + 标准错误 + 退出码**写入同名日志文件(文件名即门的名字,照 Phase 10 的清单):

    | 日志文件 | 命令 | 预期 |
    |---|---|---|
    | `check-01-token-conformance.log` | `bash scripts/check-01-token-conformance.sh` | `PASS` / exit 0 |
    | `check-02-contrast.log` | `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures` / exit 0 |
    | `check-03-hidden-uniqueness.log` | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` / exit 0 |
    | `check-04-important-count.log` | `bash scripts/check-04-important-count.sh` | `PASS` / exit 0 |
    | `check-05-full.log` | `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` | **`exit=2`(设计如此:item 5 的两条 `--ai-smoke` 腿 BLOCKED)** |
    | `check-06-idi05-validation.log` | `.venv/bin/python scripts/check-06-idi05-validation.py` | `exit=0` |
    | `check-07-idi08-validation.log` | `.venv/bin/python scripts/check-07-idi08-validation.py` | `exit=0` |
    | `check-09-idi09-validation.log` | `.venv/bin/python scripts/check-09-idi09-validation.py` | `exit=0` |
    | `check-10-idi10-validation.log` | `.venv/bin/python scripts/check-10-idi10-validation.py` | `exit=0` |
    | `pytest.log` | `.venv/bin/python -m pytest backend/tests -q --tb=short` | `219 passed, 6 skipped` |
    | `node-check-app.log` | `node --check frontend/app.js` | 无输出 / exit 0 |
    | `probe-05-resolve-color.log` | `.venv/bin/python scripts/probe-05-resolve-color.py` | `EXIT=0` |
    | `probe-07-focus-composite.log` | `.venv/bin/python scripts/probe-07-focus-composite.py` | `EXIT=0` |

    **门环境事实(省得重探):** `check-05` / `check-09` / `check-10` / 两个探针在本机**必须**用 Playwright 自带 chromium(无头);`check-05` 必须 `--browser bundled`(`channel="chrome"` + headless 会 CDP 挂死)。pytest **必须**用项目 `.venv`(环境 `python3` 是 miniconda,会让 4 个 `ai_caller` 测试假失败)。本机**没有 `timeout` 命令**。8765 端口可能有遗留 uvicorn,门走「复用,不新起」是预期。

    **第 2 步 —— 逐项与基线对照,并把每一处差异分诊。**

    把本阶段 `gate-logs/` 的 `=== 逐项结论 ===` 块与 Phase 10 的对照基线**逐项并排**写进 SUMMARY。对每一处差异给出「改前 → 改后」两列 + **机制解释**。判据:
    - **任何 FAIL 都是缺口** —— 停下报回;
    - **任何新增 BLOCKED 都是缺口** —— 停下报回(注意 `check-05` 的 item 5 必须仍是 **2** BLOCKED);
    - 断言**计数**或**读数**变化**允许**,但必须有机制解释。已知的预期差异:本阶段改了容器绘制面与面板间距(灰缝 12px → 0、五容器由四边边框收成三条 1px 横线 + 一条 1px 竖线),故几何类读数可能整体位移 —— **由运行时读数确认,不得靠推断**(Phase 10 就出现过计划写「零布局改动」而实测矮了 3px);
    - `check-05` 全量 `exit=2` 的**成因集合必须仍是「item 5 的两条 `--ai-smoke` 腿」** —— 若成因集合扩大了,那就是缺口。

    **第 3 步 —— 连带指纹面:在磁盘上逐份实测,不凭记忆。**

    写一段一次性解析(临时脚本落系统临时目录、跑完删除),对 `.planning/**` 下**所有** `*VERIFICATION.md` / `*UAT.md`:
    - 解析 frontmatter 的 `covered_files` 列表(**逐行匹配路径**,**不是**全文 grep —— 全文 grep 会把只在正文提及的报告算进来);
    - 对每个被本阶段改动的文件统计「哪些报告的 `covered_files` 列了它」;
    - 对每份命中的报告**额外测「其 `covered_files` 里的每个路径是否还在盘上」** —— 归档后的 `.planning/phases/...` 路径不可解析 ⇒ fail-closed stale(属 2026-09-14 登记的已知限制)。

    把**实测表**写进 SUMMARY(报告路径 / 状态 / covered 条数 / 缺失条数)。规划期实测的形状(**执行期须重新实测**,份数可能因归档而变):`frontend/style.css` 被 **11** 份列出、`scripts/check-09-idi09-validation.py` 被 **1** 份、`scripts/check-02-contrast.py` 被 **1** 份、`scripts/check-05-ui-uat.py` 被 **7** 份;且这 11 份**全部已是 fail-closed stale**。

    **⚠ `REG-04` 的正式处置归 Phase 12** —— 本步只**实测并登记**,不得做「以 HEAD 内容重新验证」或刷新任何指纹。

    **第 4 步 —— 仓库卫生与最终状态。**

    - `git status --porcelain frontend/` 仅列出 `frontend/style.css`;
    - `git status --porcelain scripts/` 仅列出 `scripts/check-05-ui-uat.py`(计划 03 的 `check-09` 改动已在波次 3 提交);
    - `git diff --stat -- frontend/app.js frontend/index.html backend/ frontend/vendor/` 为空;
    - `ls frontend/vendor/` 仅 `marked.min.js`;
    - `grep -o '/\* PAIR' frontend/style.css | wc -l` == 53;`grep -o '/\* ORDER' frontend/style.css | wc -l` == 1。

    **第 5 步 —— 不触碰任何代码。** 本任务只跑命令、写日志、写 SUMMARY。任何一条不达标都按产品缺陷报回,不就地修门、不就地修产品。
  </action>
  <verify>
    <automated>ls .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/ | sort | tr '\n' ' '</automated>
    <fails_when>the listing does not contain all thirteen names: check-01-token-conformance.log, check-02-contrast.log, check-03-hidden-uniqueness.log, check-04-important-count.log, check-05-full.log, check-06-idi05-validation.log, check-07-idi08-validation.log, check-09-idi09-validation.log, check-10-idi10-validation.log, node-check-app.log, probe-05-resolve-color.log, probe-07-focus-composite.log, pytest.log</fails_when>
    <automated>grep -c '^FAIL' .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/check-05-full.log .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/check-06-idi05-validation.log .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/check-07-idi08-validation.log .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/check-09-idi09-validation.log .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/check-10-idi10-validation.log</automated>
    <fails_when>any of the five counts is non-zero (a verdict line begins at column 0 with "FAIL"; zero across all five is the "no new failures" criterion). NOTE: check-05's overall exit code is 2 BY DESIGN (item 5's two --ai-smoke legs are BLOCKED) — never read that exit code as a failure</fails_when>
    <automated>grep -E '^item (5|8|9):' .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/check-05-full.log</automated>
    <fails_when>the item 5 line does not read "item 5: BLOCKED  (9 条断言,0 FAIL,2 BLOCKED)", or the item 8 line does not read "item 8: PASS  (13 条断言,0 FAIL,0 BLOCKED)", or the item 9 line does not begin with "item 9: PASS"</fails_when>
    <automated>tail -3 .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/pytest.log; grep -E 'passed|failed' .planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/pytest.log | tail -1</automated>
    <fails_when>the pytest summary line does not report 219 passed and 6 skipped (a lower passed count, or any failed count, is a gap)</fails_when>
    <automated>git status --porcelain frontend/ scripts/ backend/; git diff --stat -- frontend/app.js frontend/index.html frontend/vendor/</automated>
    <fails_when>the status output lists any path other than "frontend/style.css" and "scripts/check-05-ui-uat.py", or the diff --stat output is not empty</fails_when>
  </verify>
  <acceptance_criteria>
    - `gate-logs/` 下恰有 13 个日志文件,名字与本计划表格逐条对应。
    - 五条浏览器门日志里 `^FAIL` 计数均为 **0**;`check-05-full.log` 的 item 5 为 `BLOCKED (9 条断言,0 FAIL,2 BLOCKED)`、item 8 为 `PASS (13 条断言,0 FAIL,0 BLOCKED)`、item 9 为 `PASS`。
    - `pytest.log` 报告 `219 passed, 6 skipped`(用项目 `.venv`);`node-check-app.log` 无输出。
    - SUMMARY 里给出本阶段与 Phase 10 基线的**逐项并排对照表**;每一处差异都有「改前 → 改后」两列 + **机制解释**;`check-05` 全量 `exit=2` 的成因集合仍只是 item 5 的两条 `--ai-smoke` 腿。
    - 连带指纹面的**实测表**入册(报告路径 / 状态 / covered 条数 / 缺失条数),并明确记为「`REG-04` 的输入,正式处置归 Phase 12」;本阶段**未**刷新任何指纹、**未**做「以 HEAD 内容重新验证」。
    - `git status --porcelain frontend/ scripts/ backend/` 只列出 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`;`git diff --stat -- frontend/app.js frontend/index.html frontend/vendor/` 为空。
    - `grep -o '/\* PAIR' frontend/style.css | wc -l` == 53;`grep -o '/\* ORDER' …` == 1;`ls frontend/vendor/` 仅 `marked.min.js`。
    - 本任务没有编辑任何代码文件(除写日志与 SUMMARY)。
  </acceptance_criteria>
  <done>13 个门的原始输出与退出码已落盘;逐项与 Phase 10 基线并排对照且每处差异有机制解释;五条浏览器门零 FAIL、`check-05` 全量的 exit=2 仍只因 item 5 的两条 `--ai-smoke` 腿;pytest 219 passed / 6 skipped;连带指纹面逐份实测并登记为 Phase 12 `REG-04` 的输入;`app.js` / `index.html` / 后端 / vendor 逐字节未改。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 无外部输入边界 | 本计划只改 `check-05` 的一处期望侧,并跑既有的门与探针:零用户输入处理、零鉴权、零数据访问、零网络调用、零新增资源加载。攻击面限于**门脚本自起 `uvicorn` 并驱动无头浏览器**这一次本地动作 |
| 本地进程边界(门与探针) | `check-05` / `check-06` / `check-07` / `check-09` / `check-10` / 两个探针都会 `ensure_server()` 自起(或复用)`uvicorn` 并用 Playwright 驱动无头 chromium 访问 `localhost`。它们与被测样本之间必须是**只读**关系 |
| 一次性解析脚本边界 | Task 3 用一次性脚本解析 `.planning/**` 的报告 frontmatter。它必须只读,且脚本落在系统临时目录、跑完删除 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi-11-17 | Repudiation | 「零新增失败」这一结论缺少可复核的原始证据 | **high** | mitigate | 五条浏览器门 + 两个探针 + 四个静态门 + pytest + `node --check` 的**原始输出与退出码**全部落盘到 `gate-logs/`(13 个文件,与 Phase 10 同形),SUMMARY 里给出与 Phase 10 基线的**逐项并排对照表**。判据是「`^FAIL` 计数为 0」与逐项计数,不是「看着一样」 |
| T-idi-11-18 | Tampering | `check-05` 的改动面(可能越界) | **high** | mitigate | 「改门以让结论成立」是本仓库最严重的错向。缓解:(a) 唯一理由已实测(那条断言会静默死亡),且其覆盖者**全部**已是 fail-closed stale ⇒ 零边际成本;(b) 改动面由 `git diff -U0` **逐行人工核对**限定为「期望侧令牌名 + 标签文本 + 相邻注释」三处;(c) 断言形式判据是「仍是 `ok(...)` 的精确等值」,禁止 `ok_contains` / 非透明 / 硬编码 rgb / `or` 分支;(d) `check-05` 的其它任何一行不得改动 |
| T-idi-11-19 | Tampering | 为迁就旧数字而回退产品改动 | **high** | mitigate | `check-05 --item 8` 的 sticky 余量从 `1.000px` 变为 `0.000px` 是**事实被如实登记**。缓解:(a) D-11-16 的分诊规则逐字写进任务;(b) 判据含 `git diff --stat -- frontend/style.css` 为空 —— 任何为恢复旧读数的产品回退都会在这里现形;(c) 容差字面量 `<= 1.0` 必须逐字未改 |
| T-idi-11-20 | Tampering | `REG-04` 越界(本阶段做重验 / 刷指纹) | medium | mitigate | `REG-04` 归 Phase 12。缓解:Task 3 只做**实测与登记**,任务文本与验收都明写「不得刷新任何指纹、不得做「以 HEAD 内容重新验证」」;连带面记录标注为「Phase 12 `REG-04` 的输入」 |
| T-idi-11-21 | Tampering | 一次性解析脚本的落点 | low | mitigate | 解析脚本落在系统临时目录(`mktemp -d`)并随即删除,不落进仓库树;验收:`git status --porcelain` 的已跟踪路径改动只有 `frontend/style.css` 与 `scripts/check-05-ui-uat.py` |
| T-idi-11-22 | Denial of Service | 无 | low | accept | 全量 `check-05` 的运行时长与既有阶段一致(单次 chromium 会话、多次导航);`--item` 可把范围收窄 |
| T-idi-11-SC | Tampering | npm / pip / cargo 安装 | low | accept | 本阶段**零安装**:零新增依赖、零构建步骤(DESIGN.md D-06 硬约束)。验收:`ls frontend/vendor/` 仅 `marked.min.js` |
</threat_model>

<verification>
**承重证据:**

- `.venv/bin/python scripts/check-05-ui-uat.py --item 5 --browser bundled` → 该 `.hint` 断言 `PASS`(`expected=actual=rgb(255, 255, 255)`);`item 5: BLOCKED  (9 条断言,0 FAIL,2 BLOCKED)`;`exit=2`
- `.venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled` → `item 8: PASS  (13 条断言,0 FAIL,0 BLOCKED)`;`INFO item8 sticky 原始数值` 原文入册
- `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/` 下恰 13 个日志;五条浏览器门日志 `^FAIL` 计数均为 0
- `check-05-full.log` 的 item 5 = `BLOCKED (9, 2 BLOCKED)`、item 8 = `PASS (13)`、item 9 = `PASS`;`exit=2` 的成因集合仍只是 item 5 的两条 `--ai-smoke` 腿
- `pytest.log` = `219 passed, 6 skipped`;`node-check-app.log` 无输出
- 连带指纹面实测表入册,并标注为 Phase 12 `REG-04` 的输入

**仓库卫生:**

- `git status --porcelain frontend/ scripts/ backend/` 仅列出 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`
- `git diff --stat -- frontend/app.js frontend/index.html frontend/vendor/` 为空
- `git diff --stat -- frontend/style.css` 为空(本计划零产品改动)
- `ls frontend/vendor/` 仅 `marked.min.js`
- `grep -o '/\* PAIR' frontend/style.css | wc -l` == 53;`grep -o '/\* ORDER' frontend/style.css | wc -l` == 1
</verification>

<success_criteria>
- `check-05` 里那条会静默死亡的 `.hint` 实际背景断言已按 Phase 9 的同一纪律重新登记:期望侧换指统一面令牌,**断言形式一字未变**;`item 5` 的 BLOCKED 计数回到 2。
- `REG-03` 关闭:`check-05 --item 8` 复跑 `PASS`,余量新读数与成因机制已登记,D-11-16 的分诊结论(事实未变 ⇒ 只更新读数)已写死;容差与产品代码均未为迁就旧数字而回退。
- 五条浏览器门 + 两个探针 + 四个静态门 + pytest + `node --check` 逐条复跑,**零新增失败**;每条门的原始输出与退出码落盘到 `gate-logs/`(13 个文件)。
- `check-05` 全量 `exit=2` 的成因集合仍**只是** item 5 的两条 `--ai-smoke` 腿;任何 FAIL 或新增 BLOCKED 都已停下报回,没有静默重述。
- pytest 基线 **219 passed / 6 skipped** 不降(用项目 `.venv`)。
- 连带指纹面在磁盘上逐份实测并登记(判据锚 frontmatter 的 `covered_files` 逐行匹配 + 路径是否在盘),**未**在本阶段处置 `REG-04`(不做重验、不刷新指纹)。
- `frontend/style.css` 本计划零改动;`check-05` 的改动面只有一处期望侧 + 相邻注释;`frontend/app.js` / `index.html` / `backend/**` / `vendor/**` 逐字节未改。
- C-2 偏离的实际选择与其证据/理由已写入 SUMMARY(不得无声择一)。
</success_criteria>

<output>
Create `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-04-SUMMARY.md` when done
</output>

---
phase: idi-12-g1-band
plan: 02
type: execute
wave: 2
depends_on:
  - idi-12-01
files_modified:
  - scripts/check-09-idi09-validation.py
  - .planning/phases/idi-12-g1-band/screenshots/p1.png
  - .planning/phases/idi-12-g1-band/screenshots/p12.png
  - .planning/phases/idi-12-g1-band/screenshots/p3.png
  - .planning/phases/idi-12-g1-band/screenshots/checking.png
  - .planning/phases/idi-12-g1-band/screenshots/archive.png
  - .planning/phases/idi-12-g1-band/screenshots/latest-check/latest-check.png
autonomous: true
requirements:
  - VIS-01

estimate:
  tokens: 45000
  raw_tokens: 45000
  tasks: 2
  confidence: low

must_haves:
  truths:
    # ---- VIS-01 的本体:5 张整窗图 ----
    - "5 张 1440×900 整窗图落盘于 `.planning/phases/idi-12-g1-band/screenshots/`,文件名**恰为** `p1.png` / `p12.png` / `p3.png` / `checking.png` / `archive.png`,每张宽高为 `1440×900` 且字节数非零 —— 与 v1.15 同规格同路径(先例:`.planning/milestones/v1.15-phases/idi-09-card-containers/screenshots/` 与 `.../idi-10-tables-and-radius-scale/screenshots/` 各含这 5 个文件名)"
    - "5 张图**复用既有 `--screenshot DIR` 路径**产出(`scripts/check-09-idi09-validation.py` 的 `run_screenshots()` 已按 `c05.STATES` 的 5 个样本迭代并断言 1440×900 落盘非空),**不新建 harness**、不新增运行时依赖、不引入构建步骤(DESIGN.md D-06)"
    - "`run_screenshots()` 里那条「`--screenshot` 输出目录**恰含 5 个 PNG**」的既有断言**逐字保留且仍 PASS**(`sorted(out_dir.glob(\"*.png\"))` == 五个 `<state>.png`)—— 这条断言**不得**被删除、改写或放宽"
    # ---- 局部特写的落位硬约束(D-12-9) ----
    - "局部特写**不落在** 5-PNG 目录的顶层:它由 `check-09` 的**专用 CLI 参数** `--g1-snapshot DIR` 产出、写入 `<DIR>/latest-check.png`,而调用时 `<DIR>` 取 `.planning/phases/idi-12-g1-band/screenshots/latest-check`(子目录)。落进顶层会让上面那条「恰含 5 个 PNG」断言变红,而放宽它属仓库明令禁止的「把门改小」"
    - "该参数照 `scripts/check-10-idi10-validation.py:682-686` 的 `--radius-snapshot LABEL DIR` 先例同形:在 `parse_args()` 里声明、在 `main()` 里与 `--screenshot` **并列且各自独立**地派发(先 `--g1-snapshot` 后 `--screenshot`,照 `check-10` 的派发顺序)、并在 `main()` 的 `summary` 列表里追加 `\"g1-snapshot\"` 使它的结论行一定被打印(取证失败必须让门红,不能静默)"
    - "局部特写走 `page.locator(\"#latest-check\").screenshot(path=...)` 的**元素截图**路径(照 `check-10:653` 的先例),并以 `png_size()` 断言宽高非零 —— `png_size()` 是 `check-09` 已有的函数(`:177-186`),不新增读图工具"
    # ---- 局部特写拍的是最终态、且真的含 band ----
    - "局部特写拍的是 `checking` 样本(唯一 `#latest-check` 可见的样本)里 `#latest-check` 这个元素,画面里含 `| 编号 | 级别 | 位置 | 问题 | 建议修法 |` 表头行与 >= 1 行数据 —— 这是 G1-01「表头读作独立 band」的**直接人眼证据**(D-12-9);故该函数必须断言 `#latest-check th` 的元素数 >= 1"
    - "该函数另断言**表头行落在 `#latest-check` 的可视区内**(`th` 的 `getBoundingClientRect()` 落在 `#latest-check` 的 `clientRect` 之内)—— 守的是 D-12-10:`max-height: 30vh` 使 `#latest-check` 是滚动区,表若落在可视区外,整窗图与元素截图**都拍不到 band**,而截图会「成功落盘」"
    - "`checking.png` 整窗图同样是**最终态**:本计划**不改** `frontend/style.css` 与 `scripts/ui-states/checking/docs/DESIGN-check-2.md`(它们在波次 1 定型),故 5 张图与局部特写拍的都是同一次最终态"
    # ---- 边界 ----
    - "`check-09` 的 `c1..c6` 既有断言、退出码语义(`0=全 pass / 1=有 FAIL / 2=有 BLOCKED`)与既有三个参数(`--item` / `--screenshot` / `--keep`)**逐字保留**;`--g1-snapshot` 是**新增的第四个**参数"
    - "`frontend/**` / `backend/**` / `scripts/check-05-ui-uat.py` / `check-10-idi10-validation.py` / `check-01`…`04` / `check-06` / `check-07` / `probe-*` 本计划**零改动**;`frontend/vendor/` 仍只有 `marked.min.js`"

  artifacts:
    - path: "scripts/check-09-idi09-validation.py"
      provides: "新增 `--g1-snapshot DIR` 参数与 `g1_snapshot()` 函数:在 `checking` 样本上对 `#latest-check` 取一张元素级特写,并断言表头存在、落在可视区内、PNG 宽高非零"
      contains: "--g1-snapshot"
    - path: ".planning/phases/idi-12-g1-band/screenshots/"
      provides: "VIS-01 的 5 张 1440×900 整窗人眼取证图(p1 / p12 / p3 / checking / archive)"
      contains: "checking.png"
    - path: ".planning/phases/idi-12-g1-band/screenshots/latest-check/latest-check.png"
      provides: "G1-01 的局部特写:补过表的 `checking` 样本里 `#latest-check` 的元素截图,band 在 1440×900 整窗图里只占几十像素,局部图才是直接证据"
      contains: "latest-check.png"

  key_links:
    - from: "`scripts/check-09-idi09-validation.py` 的 `--g1-snapshot DIR`"
      to: "`page.locator(\"#latest-check\").screenshot(...)` 的元素截图路径"
      via: "照 `scripts/check-10-idi10-validation.py:653` 的先例 —— 零新 harness、零新增依赖"
      pattern: "page\\.locator\\(\"#latest-check\"\\)\\.screenshot"
    - from: "5 张整窗图"
      to: "`c05.STATES`(`scripts/check-05-ui-uat.py:584` = `[\"p1\", \"p12\", \"p3\", \"checking\", \"archive\"]`)"
      via: "`run_screenshots()` 逐样本 `make_fixture` + `enter_project` + `page.screenshot`;文件名 = `<state>.png`"
      pattern: "for state in c05.STATES"
    - from: "`#latest-check` 的局部特写"
      to: "波次 1 补过表的 `checking` fixture 与改白后的 `#latest-check` 宿主绘制面"
      via: "`make_fixture(\"checking\")` + `enter_project` —— 截图必须是最终态,故本计划不得改动渲染面"
      pattern: "make_fixture\\(\"checking\""

  prohibitions:
    - statement: "不得删除、改写或放宽 `run_screenshots()` 里那条「`--screenshot` 输出目录恰含 5 个 PNG」的断言,也不得把局部特写写进该目录的顶层。放宽它是仓库明令禁止的「把门改小」;正确做法是给局部图**独立的落点**(专用参数 + 子目录)"
      status: active
      verification: flagged
    - statement: "不得新建 harness、不得新增运行时依赖、不得引入构建步骤。VIS-01 要求「复现既有 `--screenshot` 路径而不是新建 harness」(DESIGN.md D-06 零构建)"
      status: active
      verification: flagged
    - statement: "不得在本计划改动 `frontend/style.css` 或 `scripts/ui-states/checking/docs/DESIGN-check-2.md`。截图与局部特写必须是**最终态**;任何渲染面改动都会让本计划的产物作废(ROADMAP Phase 12 Rationale)"
      status: active
      verification: flagged
    - statement: "不得把「截图落盘成功」当作「band 拍到了」的证明。`max-height: 30vh` 使 `#latest-check` 是滚动区,表落在可视区外时截图照样落盘 ⇒ 必须断言表头存在**且**落在可视区内"
      status: active
      verification: flagged
    - statement: "不得顺手做未裁定项:G2、`999.2`、暗色模式(`A11Y-V2` / `FLOW-V2` / `TOKEN-V2`)、Nyquist 缺口、图标与空状态、`check-10:328` 的过期注释、报告区表头 sticky —— 全部 Out of Scope(D-12-4 / D-12-12)"
      status: active
      verification: flagged
---

<objective>
产出 **VIS-01** 的人眼取证:5 张 1440×900 整窗截图(p1 / p12 / p3 / checking / archive),外加**一张 `#latest-check` 的元素级局部特写**(`checking` 态,在波次 1 补过表的 fixture 上)。

Purpose: `VIS-01` 是「分块割裂感已消除」这条主张**唯一的屏幕级证据**;而 band 在 1440×900 整窗图里只占几十像素,**局部图才是 G1-01 的直接人眼证据**(D-12-9)。两张都必须拍**最终态** —— 所以本计划排在所有 `style.css` / fixture 改动落定之后,且本计划自身**不碰**渲染面。

**为什么必须给局部特写一个专用参数(D-12-9 的落位硬约束):** `scripts/check-09-idi09-validation.py` 的 `run_screenshots()` 断言 `--screenshot` 的输出目录**恰含 5 个 PNG**。把第 6 张图丢进同一个目录会让那条既有断言**变红**,而放宽它属仓库明令禁止的「把门改小」。仓库自己的先例是**独立落点**:`check-10` 的元素快照走自己的 `--radius-snapshot LABEL DIR`(声明在 `:682-686`、派发在 `:730-732`),产物落在**子目录**(`.planning/milestones/v1.15-phases/idi-10-tables-and-radius-scale/screenshots/chat-user/p1-chat-user-evidence.png`)。本计划照同形:新增 `--g1-snapshot DIR`,局部图写 `<DIR>/latest-check.png`,调用时 `<DIR>` 取 `screenshots/latest-check`。

**为什么本计划排在波次 2:** 它依赖波次 1 的两件产物 —— 补过表的 `checking` fixture(否则局部图里没有表头可看)与改白后的 `#latest-check` 宿主绘制面(否则 band 不显形)。

**本计划关闭的需求:** VIS-01。

**本计划不触碰:** `REG-04`(计划 03);`frontend/style.css` / `scripts/ui-states/checking/docs/DESIGN-check-2.md`(波次 1 已定型,本计划零改动);`frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**`(零字节);`scripts/check-05-ui-uat.py` / `check-02-contrast.py` / `check-10-idi10-validation.py` / `check-01`…`04` / `check-06` / `check-07` / `probe-*`(零改动);G2 / `999.2` / 暗色模式 / Nyquist 缺口 / 图标与空状态 / `check-10` 的过期注释 / 报告区表头 sticky(全部 Out of Scope)。

**执行前基线(规划期已在 HEAD 上实测,执行器须复核):**

| 检查 | 规划期在 HEAD 上的实测结果 |
|---|---|
| `grep -n 'def run_screenshots' scripts/check-09-idi09-validation.py` | `:774` —— 已按 `c05.STATES` 迭代、断言 1440×900、并断言输出目录**恰含 5 个 PNG**(`:791-793`) |
| `grep -n 'add_argument' scripts/check-09-idi09-validation.py` | 恰三个:`--item` / `--screenshot` / `--keep` —— **没有** `--g1-snapshot` |
| `scripts/check-10-idi10-validation.py` 的 `--radius-snapshot` | 声明在 `:682-686`(`nargs=2`,`metavar=("LABEL","DIR")`),派发在 `:730-732`,summary 追加在 `:743-744` |
| `scripts/check-10-idi10-validation.py` 的元素截图先例 | `:653` `page.locator(RADIUS_SNAPSHOT_SEL).screenshot(path=str(png_path))` |
| `c05.STATES` | `["p1", "p12", "p3", "checking", "archive"]` |
| 既有的 5-PNG 目录先例 | `.planning/milestones/v1.15-phases/idi-09-card-containers/screenshots/` 与 `.../idi-10-tables-and-radius-scale/screenshots/` 各恰含 `p1.png` / `p12.png` / `p3.png` / `checking.png` / `archive.png` |
| `.planning/phases/idi-12-g1-band/screenshots/` | **不存在**(本计划创建) |
| `git status --porcelain frontend/` | 空 |

**Flagged assumption(probe fallback,不得静默丢弃):** `VIS-01` 在边界覆盖探针里返回 `{"category":"unclassified","status":"unresolved"}` —— 分类器的 cue 词汇是英文、而该需求文本是中文散文,故它**拒绝分类而不是乱猜**。按协议:`unclassified` 行**保持 `unresolved`**,**不得**用 backstop 自动消解、**不得**静默丢弃、**不得**为它发明探针派生的谓词。本计划的绑定验收判据来自 **ROADMAP 的 Success Criteria 5 与 CONTEXT 的 D-12-9 / D-12-10**,已逐条落进 `must_haves.truths`。

Output: `.planning/phases/idi-12-g1-band/screenshots/` 下的 5 张 1440×900 整窗图、`screenshots/latest-check/latest-check.png` 局部特写,以及 `scripts/check-09-idi09-validation.py` 新增的 `--g1-snapshot` 参数与 `g1_snapshot()` 函数。
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
@.planning/phases/idi-12-g1-band/idi-12-01-PLAN.md
@scripts/check-09-idi09-validation.py
@scripts/check-10-idi10-validation.py
</context>

## Artifacts this phase produces

**本计划新增的符号(plan-review-convergence 的源锚定遍历须把它们排除在漂移核验之外):**

| 符号 | 类型 | 落点 |
|---|---|---|
| `--g1-snapshot DIR` | 新的 CLI 参数(`metavar="DIR"`) | `scripts/check-09-idi09-validation.py` 的 `parse_args()` |
| `g1_snapshot(page, out_dir, tmp_root)` | 新的函数 | 同上,紧邻 `run_screenshots()` |
| `"g1-snapshot"` | `main()` 的 `summary` 列表新条目 | 同上 |
| `g1-snapshot → VIS-01 / G1-01` | 模块 docstring 映射表的新行 + 运行方式段的新示例 | 同上 |
| `.planning/phases/idi-12-g1-band/screenshots/latest-check/latest-check.png` | 新产物 | 文件系统 |

**本阶段前序计划已新增(此处复述以免被当作漂移):** `c6`(计划 01 的 item 函数)、`"c6": c6`、`read_classlist` 别名、fixture 的 `## 问题分级` 标题。

**本阶段后续计划会新增:** `.planning/phases/idi-12-g1-band/gate-logs/idi-12-03/**`(计划 03)。

<tasks>

<task type="auto" tdd="false">
  <name>Task 1: 给 `check-09` 加专用参数 `--g1-snapshot DIR` —— 元素级局部特写走独立落点,不动「恰含 5 个 PNG」那条断言</name>
  <files>scripts/check-09-idi09-validation.py, .planning/phases/idi-12-g1-band/screenshots/latest-check/latest-check.png</files>
  <read_first>
    - `scripts/check-10-idi10-validation.py` —— `:640-676`(`radius_snapshot()` 的完整形状:进 fixture、读数、`page.locator(SEL).screenshot(path=...)`、`png_size()` 断言、`info()` 落盘路径)、`:682-689`(`parse_args` 里的参数声明)、`:726-750`(`main()` 里的派发与 `summary` 追加)
    - `scripts/check-09-idi09-validation.py` —— `:99-115`(helper 别名区,`png_size` 在 `:177-186`)、`:774-797`(`run_screenshots()`,含那条「恰含 5 个 PNG」断言)、`:799-806`(`parse_args()`)、`:808-871`(`main()`,含 `summary` 构造与 `ITEMS[name](page, tmp_root)` 派发循环)、`:1-96`(docstring,尤其 `:40-66` 的映射表与 `:26-31` 的运行方式段)
    - `scripts/check-05-ui-uat.py:485-498`(`make_fixture`)、`:510-516`(`enter_project`)、`:347-348`(`read_style`)
    - `.planning/phases/idi-12-g1-band/12-CONTEXT.md` 的 D-12-9 与 D-12-10
  </read_first>
  <action>
    在 `scripts/check-09-idi09-validation.py` 里新增一个**元素级局部特写**参数与函数,**照 `check-10` 的 `--radius-snapshot LABEL DIR` 同形但不需要标签**(只有一张图)。

    **(a) `parse_args()`:** 新增一个参数 `--g1-snapshot`, `default=None`, `metavar="DIR"`,帮助文本写明「在 `checking` 样本上对 `#latest-check` 取一张元素级特写,写 `<DIR>/latest-check.png`(独立落点:不得写进 `--screenshot` 的目录顶层)」。既有三个参数逐字保留。

    **(b) 新函数 `g1_snapshot(page, out_dir, tmp_root)`**,放在 `run_screenshots()` 附近:
    - `item = "g1-snapshot"`;打印 `=== g1-snapshot: #latest-check 元素级特写(checking)==` 横幅。
    - `out_dir.mkdir(parents=True, exist_ok=True)`。
    - `proj = c05.make_fixture("checking", tmp_root)` + `c05.enter_project(page, proj)`(`checking` 是**唯一** `#latest-check` 可见的样本)。
    - 取两条原始读数并 `info()` 抄录:`#latest-check` 的计算底色(`read_style`)与 `#latest-check th` 的计算底色。
    - **断言 1(表头存在)**:`page.locator("#latest-check th").count() >= 1`。note 写明:没有表头就没有可看的 band,这张图会拍成一张空壳。
    - **断言 2(表头落在可视区内)**:取 `page.locator("#latest-check").bounding_box()` 与 `page.locator("#latest-check th").first.bounding_box()`,断言 `th` 的矩形落在 `#latest-check` 的矩形**之内**(上下各留 0.5px 浮点容差)。note 写明:`max-height: 30vh` 使它是滚动区,表落在可视区外时截图照样落盘 —— 这条判据把「拍到了 band」变成可失败。
    - **断言 3(元素截图落盘且宽高非零)**:`page.locator("#latest-check").screenshot(path=str(out_dir / "latest-check.png"))`,再 `png_size()` 断言 `width is not None and height is not None and width > 0 and height > 0`,`note=str(path)`。**复用既有的 `png_size()`**,不新增读图工具。
    - 断言一律走 `ok_true`(期望侧是布尔条件),失败即 FAIL。

    **(c) `main()`:** 在 `for name in items: ITEMS[name](page, tmp_root)` 循环之后、`if args.screenshot:` **之前**,加 `if args.g1_snapshot: g1_snapshot(page, Path(args.g1_snapshot), tmp_root)`(照 `check-10` 的派发顺序;`args.g1_snapshot` 是字符串,须过 `Path(...)` 再交给函数)。随后在 `summary` 构造处追加:当 `args.g1_snapshot` 为真时 `summary.append("g1-snapshot")` —— 使它的结论行一定被打印(取证失败必须让门红,不能静默)。

    **(d) docstring:** 在「断言与需求的映射」表里补一行(`g1-snapshot → VIS-01 / G1-01`,写明它是元素级局部特写、独立落点、不参与 `run_screenshots` 的 5-PNG 判据),并在「运行方式」段补一条示例命令。

    **不得改动:** `run_screenshots()` 的任何一行(尤其那条「恰含 5 个 PNG」断言)、`c1..c6` 的任何断言、`ITEMS` 的既有条目、退出码语义。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --item c6 --g1-snapshot .planning/phases/idi-12-g1-band/screenshots/latest-check</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or any BLOCKED, or the trailing line not starting with "exit=0", or the "=== 逐项结论 ===" block not listing a "g1-snapshot" row</fails_when>
    <automated>.venv/bin/python -c "import struct,pathlib;p=pathlib.Path('.planning/phases/idi-12-g1-band/screenshots/latest-check/latest-check.png');h=p.open('rb').read(24);print('sig',h[:8]==b'\x89PNG\r\n\x1a\n');print('size',struct.unpack('>II',h[16:24]))"</automated>
    <fails_when>sig is not True, or the printed size tuple has a zero component, or the read raises</fails_when>
    <automated>grep -cF -- 'g1-snapshot' scripts/check-09-idi09-validation.py</automated>
    <fails_when>the count is "0" (the flag must appear in parse_args, in the main() dispatch, in the summary list, and in the docstring)</fails_when>
    <automated>grep -cF -- 'shot 输出目录恰含 5 个 PNG' scripts/check-09-idi09-validation.py</automated>
    <fails_when>the count is not "1" (the existing exactly-5-PNG assertion must be present exactly once, unmodified)</fails_when>
    <automated>git status --porcelain scripts/ frontend/</automated>
    <fails_when>output contains any path other than "scripts/check-09-idi09-validation.py", or output is empty</fails_when>
  </verify>
  <acceptance_criteria>
    - `.venv/bin/python scripts/check-09-idi09-validation.py --item c6 --g1-snapshot .planning/phases/idi-12-g1-band/screenshots/latest-check` 以 `exit=0` 结尾,`=== 逐项结论 ===` 块里同时有 `item c6: PASS` 与 `item g1-snapshot: PASS`,两者均为 `0 FAIL,0 BLOCKED`。
    - 该命令的 stdout 里能看到 `INFO` 抄录的两条底色读数,以及落盘路径。
    - `.planning/phases/idi-12-g1-band/screenshots/latest-check/latest-check.png` 存在、PNG 签名正确、宽高均 > 0。
    - `grep -cF -- 'shot 输出目录恰含 5 个 PNG' scripts/check-09-idi09-validation.py` 输出 `1` —— 那条既有断言**一字未改、未被删除、未被复制**。
    - `parse_args()` 现在有四个参数(`--item` / `--screenshot` / `--g1-snapshot` / `--keep`),既有三个的帮助文本与 `default` 逐字不变。
    - `git status --porcelain scripts/ frontend/` 只列出 `scripts/check-09-idi09-validation.py`。
  </acceptance_criteria>
  <done>`check-09` 有了独立的 `--g1-snapshot DIR` 参数与 `g1_snapshot()` 函数:它在 `checking` 样本上断言表头存在、断言表头落在 `#latest-check` 的 30vh 可视区内、再把 `#latest-check` 的元素截图写到 `<DIR>/latest-check.png` 并断言宽高非零;`run_screenshots()` 的「恰含 5 个 PNG」断言逐字保留。</done>
</task>

<task type="auto" tdd="false">
  <name>Task 2: 产出 5 张 1440×900 整窗图 + 1 张局部特写,并在盘上逐张取证</name>
  <files>.planning/phases/idi-12-g1-band/screenshots/p1.png, .planning/phases/idi-12-g1-band/screenshots/p12.png, .planning/phases/idi-12-g1-band/screenshots/p3.png, .planning/phases/idi-12-g1-band/screenshots/checking.png, .planning/phases/idi-12-g1-band/screenshots/archive.png, .planning/phases/idi-12-g1-band/screenshots/latest-check/latest-check.png</files>
  <precondition>`git status --porcelain frontend/` 为空且波次 1 的三处改动已提交 ⇒ 本次截图拍的确实是**最终态**渲染面(本计划不改 `frontend/style.css` 与 `checking` fixture)。</precondition>
  <read_first>
    - `.planning/milestones/v1.15-phases/idi-09-card-containers/screenshots/` 与 `.planning/milestones/v1.15-phases/idi-10-tables-and-radius-scale/screenshots/`(5 张图的**落盘约定与文件名先例**;后者另含 `chat-user/` 子目录,即「局部特写另置子目录」的先例)
    - `scripts/check-09-idi09-validation.py` 的 `run_screenshots()`(任务 1 之后的最新形态)与 `g1_snapshot()`(任务 1 新增)
    - `scripts/check-05-ui-uat.py:584`(`STATES`)
    - `.planning/phases/idi-12-g1-band/12-CONTEXT.md` 的 D-12-9 与 D-12-10
  </read_first>
  <action>
    一次运行同时产出两类产物:
    1. 5 张整窗图:`.venv/bin/python scripts/check-09-idi09-validation.py --screenshot .planning/phases/idi-12-g1-band/screenshots`,**复用既有 `--screenshot` 路径**,不新建 harness、不改 `run_screenshots()` 一行。它内部已逐样本断言 1440×900 落盘非空,并断言输出目录恰含 5 个 PNG。
    2. 局部特写:`.venv/bin/python scripts/check-09-idi09-validation.py --g1-snapshot .planning/phases/idi-12-g1-band/screenshots/latest-check` —— 落点在 **5-PNG 目录的子目录**里,故前者的「恰含 5 个 PNG」断言不受影响。

    两次运行可合并为一条命令(两个参数并列),也可分开跑;**合并跑时两种产物的落点仍各自独立**(`--screenshot` 的 DIR 是 `screenshots`,`--g1-snapshot` 的 DIR 是 `screenshots/latest-check`)。

    落盘后**在盘上逐张取证**(不采信「命令退 0 所以图没问题」):
    - 5-PNG 目录的顶层 `glob("*.png")` 恰为 `p1.png` / `p12.png` / `p3.png` / `checking.png` / `archive.png`(无缺项、无多余、无子目录混入顶层);
    - 5 张各为 `1440×900` 且字节数非零;
    - `screenshots/latest-check/latest-check.png` 存在、PNG 签名正确、宽高均 > 0;
    - 把两处落点的实际读数(文件名、宽高、字节数)抄进 `idi-12-02-SUMMARY.md`,并写明「5 张整窗图 + 1 张局部特写」这一分工与各自的目的(整窗图 = 分块割裂感已消除的人眼取证;局部图 = G1-01 的 band 直接证据)。

    **不得**:把局部特写写进 5-PNG 目录顶层;删除 / 改写 / 放宽任何既有断言;在本计划改动渲染面。
  </action>
  <verify>
    <automated>.venv/bin/python scripts/check-09-idi09-validation.py --screenshot .planning/phases/idi-12-g1-band/screenshots --g1-snapshot .planning/phases/idi-12-g1-band/screenshots/latest-check</automated>
    <fails_when>non-zero exit, or any verdict line beginning with "FAIL", or any BLOCKED, or the trailing line not starting with "exit=0", or the "=== 逐项结论 ===" block not listing both a "shot" and a "g1-snapshot" row with 0 FAIL and 0 BLOCKED</fails_when>
    <automated>.venv/bin/python -c "import pathlib,struct;d=pathlib.Path('.planning/phases/idi-12-g1-band/screenshots');tops=sorted(p.name for p in d.glob('*.png'));print('top',tops);[print(n,*struct.unpack('>II',(d/n).open('rb').read(24)[16:24]),(d/n).stat().st_size) for n in tops];sub=d/'latest-check'/'latest-check.png';h=sub.open('rb').read(24);print('sub',sub.name,struct.unpack('>II',h[16:24]),sub.stat().st_size)"</automated>
    <fails_when>tops is not exactly ['archive.png', 'checking.png', 'p1.png', 'p12.png', 'p3.png'], or any printed size is not (1440, 900), or any byte size is 0, or the subdirectory PNG is missing or has a zero dimension</fails_when>
    <automated>git status --porcelain frontend/</automated>
    <fails_when>output is not empty (the screenshots must be taken on the final rendering surface)</fails_when>
    <automated>git status --porcelain scripts/</automated>
    <fails_when>output contains any path other than "scripts/check-09-idi09-validation.py"</fails_when>
  </verify>
  <acceptance_criteria>
    - `.planning/phases/idi-12-g1-band/screenshots/` 顶层的 PNG 恰为 `archive.png` / `checking.png` / `p1.png` / `p12.png` / `p3.png` 五个,每张宽高为 `1440×900`、字节数 > 0。
    - `.planning/phases/idi-12-g1-band/screenshots/latest-check/latest-check.png` 存在、PNG 签名正确、宽高均 > 0 —— 它**不在**顶层,故顶层的「恰含 5 个 PNG」判据未被破坏。
    - 同一次运行的 `=== 逐项结论 ===` 块里 `item shot: PASS`(5 个样本各一条 1440×900 断言 + 样本清单 + 恰含 5 个 PNG)与 `item g1-snapshot: PASS` 均为 `0 FAIL,0 BLOCKED`,总退出码 `exit=0`。
    - `idi-12-02-SUMMARY.md` 抄录了两处落点的实际文件名 / 宽高 / 字节数,并写明整窗图与局部特写各自的目的。
    - `git status --porcelain frontend/` 为空(截图拍在最终渲染面上)。
  </acceptance_criteria>
  <done>5 张 1440×900 整窗图与 1 张 `#latest-check` 局部特写全部落盘并在盘上逐张取证;局部特写走独立子目录,既有的「恰含 5 个 PNG」断言一字未改且仍 PASS;两次运行均 `exit=0`、0 FAIL、0 BLOCKED。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 截图产物 → 「分块割裂感已消除 / band 读作独立 band」这两条主张 | 截图是这两条主张**唯一的屏幕级证据**;一张拍错状态的图会让主张看起来成立而实际未验证 |
| `check-09` 的 `--screenshot` 输出目录 → `run_screenshots()` 的「恰含 5 个 PNG」断言 | 新增第 6 张图若不换落点,会直接打破这条既有断言 —— 而放宽它属「把门改小」 |
| 新 CLI 参数 → `main()` 的 `summary` 与退出码 | 若新项不进 `summary`,它的结论行不会打印,取证失败会静默通过 |
| 本地浏览器 → 本机 uvicorn(127.0.0.1:8765) | 8765 上可能存在先前遗留的进程(复用,不新起);截图读数不受影响 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-12-06 | Tampering | `run_screenshots()` 的「恰含 5 个 PNG」断言 | high | mitigate | 局部特写走**独立参数 + 独立子目录**;`<verify>` 里用 `grep -cF` 断言该断言的原文恰出现 **1** 次(未被删、未被复制、未被改写);调用时 `--g1-snapshot` 的 DIR 指向 `screenshots/latest-check` 而非 `screenshots` |
| T-12-07 | Spoofing | 「截图落盘成功」被当作「band 拍到了」 | high | mitigate | `g1_snapshot()` 断言 `#latest-check th` 元素数 >= 1 **且** 表头矩形落在 `#latest-check` 的可视矩形内(30vh 滚动区);Task 2 的 `<verify>` 另在盘上读 PNG 头逐张核对宽高与字节数,而不是只看退出码 |
| T-12-08 | Repudiation | 新 CLI 参数的结论行不进 `summary` | medium | mitigate | `main()` 在 `args.g1_snapshot` 为真时 `summary.append("g1-snapshot")`,照 `check-10` 对 `radius-snapshot` 的同形处理;`<verify>` 断言结论块里出现 `g1-snapshot` 行且为 0 FAIL / 0 BLOCKED |
| T-12-09 | Tampering | 截图拍到非最终态(渲染面在截图后又变) | medium | mitigate | 本计划 `files_modified` 不含 `frontend/**` 与 `checking` fixture;`<precondition>` 要求工作树干净;`<verify>` 断言 `git status --porcelain frontend/` 为空 |
| T-12-10 | Information Disclosure | 截图 / 日志可能携带本地绝对路径 | low | accept | 单机单人本地仓库;v1.15 两个阶段已按同一口径提交过 `screenshots/` 与 `gate-logs/`,本计划与既有先例同级 |
| T-12-SC | Tampering | npm / pip / cargo 安装 | low | accept | 本阶段**零新增依赖**(DESIGN.md D-06);Playwright 与 `.venv` 均既有 ⇒ 无安装动作,无包合法性门可触发 |
</threat_model>

<verification>
**整体阶段检查(本计划收口时):**

1. `.venv/bin/python scripts/check-09-idi09-validation.py --screenshot .planning/phases/idi-12-g1-band/screenshots --g1-snapshot .planning/phases/idi-12-g1-band/screenshots/latest-check` → `exit=0`,`item shot: PASS` 与 `item g1-snapshot: PASS` 均 0 FAIL / 0 BLOCKED。
2. 盘上核对:`screenshots/` 顶层恰 5 个 PNG、各 1440×900、各非空;`screenshots/latest-check/latest-check.png` 非空且宽高 > 0。
3. `grep -cF -- 'shot 输出目录恰含 5 个 PNG' scripts/check-09-idi09-validation.py` → `1`。
4. `git status --porcelain frontend/` → 空;`git status --porcelain scripts/` → 只有 `scripts/check-09-idi09-validation.py`。
5. `idi-12-02-SUMMARY.md` 含两处落点的实际读数抄录。
</verification>

<success_criteria>
- VIS-01 的 5 张 1440×900 整窗图在盘,文件名与 v1.15 先例逐字相同。
- G1-01 的局部特写(`#latest-check` 元素级)在盘,且拍到的是**含表头**的 `checking` 最终态。
- 既有的「`--screenshot` 输出目录恰含 5 个 PNG」断言一字未改且仍 PASS。
- 零新 harness、零新增依赖、零构建步骤。
- 渲染面(`frontend/**` 与 `checking` fixture)本计划零改动。
</success_criteria>

<output>
Create `.planning/phases/idi-12-g1-band/idi-12-02-SUMMARY.md` when done
</output>

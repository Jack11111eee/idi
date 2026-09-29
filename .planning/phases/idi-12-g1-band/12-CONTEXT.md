# Phase 12: G1 表头 band 与里程碑收口 - Context

**Gathered:** 2026-09-29
**Status:** Ready for planning

<domain>
## Phase Boundary

修掉 v1.15 审计登记的 **G1** —— `#latest-check` 内的表格表头**读作一条独立的 band**(表头底色与其宿主绘制面不再同令牌相撞);并在**最后一次 `style.css` 改动落定后**复跑五条浏览器门 + 四个静态门 + pytest 基线、按既有口径逐份处置连带作废的 `passed` 报告、产出 5 张 1440×900 整窗截图(外加一张 G1 局部特写)作为人眼取证。

**本阶段只做**:G1 定点修复(改宿主底色)+ G1 的运行时断言与视觉取证 + REG-04 全量复跑与连带面处置 + VIS-01 截图。

**本阶段不做**:v1.16 里程碑审计(走 `/gsd-audit-milestone`,与 v1.15 同路径)、`check-10` 的「只钉令牌接线不钉视觉契约」通用加固(审计的 gate blind spot 项,路线图已列为未裁定)、报告区表头 sticky(新能力)、`#latest-check` 的边框/圆角改动(未裁定)、G2、`999.2`、暗色模式(`A11Y-V2` / `FLOW-V2` / `TOKEN-V2`)、Nyquist 缺口、图标与空状态。后端与 `frontend/app.js` / `frontend/index.html` 预期**逐字节不改**。

**本阶段的改动面(预期 3 个文件)**:`frontend/style.css`(一行底色)、`scripts/check-09-idi09-validation.py`(新增 G1 断言 + 变异证明)、`scripts/ui-states/checking/docs/DESIGN-check-2.md`(补文法要求的表)。

</domain>

<decisions>
## Implementation Decisions

> **来源:** 本文件是 `/gsd-discuss-phase 12` 的产物(2026-09-29),四个灰区由用户在 `AskUserQuestion` 中**逐项选定**。ROADMAP 的 Phase 12 段已锁定 Goal / Deliverables / Success Criteria / Avoids / Gates;本文件只补 ROADMAP 里仍是「候选 / 待定」的实现决定。**凡本文件与 ROADMAP 措辞冲突处,以本文件为准**(见 D-12-1 对 Deliverable 1 路线 (a) 的收窄)。

### band 修法路线(承载 G1-01)

- **D-12-1:** **移宿主 → 改白。** `#latest-check`(`frontend/style.css:1651-1659`)的 `background` 由 `var(--color-surface)`(gray-2)就地改写为 `var(--color-surface-page)`(白)。**这是 ROADMAP Deliverable 1 路线 (a) 的选定形态**(「移宿主:`#latest-check` 的 `background` 改归另一档 —— 波及面限于这一条规则」),**不是**路线 (b)(移表头),也**不是**局部覆盖 `#latest-check th`。
  **选它的理由三条:** ①`#latest-check` 是四个 `.markdown-body` 宿主里**唯一画灰底的**(另三个 `#draft-content` / `#brainstorm-content` / `#round-doc` 都不声明 `background`,透明 ⇒ 继承白面板)⇒ 改白消除的是这个不对称本身,而不只是症状;②band 因此落在 **gray-2 on white = 1.053**,与**文档区表头今天的样子完全相同**(Phase 10 已签核的读感),「报告区与文档区读感一致」直接成立;③它是唯一**不需要改写任何门**的路线 —— `check-10` 的 `t1` 把 `th` 底色钉死在 gray-2 字面量(`scripts/check-10-idi10-validation.py:101` `TH_BG_LITERAL`),5 个 (样本,宿主) 对里含 `("p1", "#latest-check")`,只动宿主底色则 t1 全绿。
  **未采用的路线及原因(留档,planner 不必重推):** 移宿主改 gray-3 —— `--color-surface-sunken` 同时是 `.markdown-body code`(`:1244-1249`)的底色,且 code **无边框、无等宽字体**(全文件零 `monospace`/`font-family` 声明)⇒ 报告里的行内 code 会与宿主同色撞死,是 G1 同族的新缺陷;移表头(全局 `th`)—— 文档区表头读感一并变深,且要改写 t1 的 5 对断言 + `TH_BG_LITERAL`;局部覆盖 `#latest-check th` —— 引入「报告区表头与文档区不同色」的宿主特例。
  **连带后果(须处置,不是可选项):** ①围栏注释 `frontend/style.css:129-130` 现写着「The inset tier SURVIVES — controls and `#latest-check` still read as recessed」—— 该句后半在本次改动后**不再成立**,须按仓库既有纪律**就地改写**(Phase 9 / 10 / 11 都是就地改写,并在同段记下旧说法为何错,参照 `:140-142` 的写法)。②`--color-surface` 的 TEXT 配对(`frontend/style.css:621` `/* PAIR --color-text ON --color-surface TEXT */`)**仍然成立** —— 它另有控件消费者(`#check-switcher` / 三个 `select` / `.overlay-card`),配对总数 53 不变,**零新增对比度条目**(`--color-text ON --color-surface-page` 已在 `:620` 登记)。③`--color-surface` 不因本次改动而变成零消费令牌(控件仍消费),**不触发任何令牌删除**,也不得顺手删。 — **Reversibility:** costly — 撤销要连带改写围栏 :129-130 的承重注释、重写 check-09 的新断言与其变异证明、并重拍 6 张截图。
- **D-12-2:** **G1 的验收锚「两者的计算底色不同」** —— `#latest-check` 的计算底色 != `#latest-check th` 的计算底色(不再同令牌相撞),**外加人眼截图**。与 ROADMAP SC1 与 `G1-01` 的原文措辞一致。**明确不锚**「与文档区表头读数逐字节相同」(更强但实现面更大,用户未选),**也不**因此回头去加强 band 强度(用户已看过 1.053 这个读数并接受)。 — **Reversibility:** costly — 撤销要重写新断言并重跑变异证明。
- **D-12-3:** **`#latest-check` 的边界与圆角一字不动** —— `border: 1px solid var(--color-border-subtle)`(`:1655`)与 `border-radius: var(--radius-sm)`(`:1656`)保持。理由:G1-01 只谈 band;`#latest-check` 是**内陷可滚区、不是面板**,同族的 `.event-list` / `.annotation-item` / `.badge-answered` 都保留各自边框与圆角;**且 `scripts/probe-card-border-token.py:45` 把 `#latest-check` 的 gray-6 边框当作「非卡片」对照样本**(该探针读 `border-top-color`,本次改动不触及它)。改它 = 未裁定项。
- **D-12-4:** **两条相邻项不纳入本阶段,记入 Deferred** —— ①`check-10` 的 `t1` PASS 行仍挂着**改动前的注释**「HEAD 上 th 无自身底色(透明)」(`scripts/check-10-idi10-validation.py:328` 的 `note=`),审计点名它是 supporting tell;它属审计的「gate blind spot」项(路线图已列为未裁定)。②`#doc-panel-header` 是 `position: sticky`(`frontend/style.css:936`),而报告区表头在 `#latest-check` 的 30vh 滚动区内**会滚走** —— 与文档区不同语言,但那是**新能力**。两条都**不得顺手做**。

### G1 运行时取证(承载 G1-01)

- **D-12-5:** **补 fixture 的表。** 给 `scripts/ui-states/checking/docs/DESIGN-check-2.md` 补上 `backend/prompts.py:494-499` 强制的「问题分级表」。**为什么必须补:** `#latest-check` **只在 `checking` 样本可见**(p1 下祖先 `#checks-panel` 带 `.hidden` ⇒ 审计说它是「cascade-only」正是这个意思),而该样本的报告里**没有表** —— 两个 fixture 报告(`checking` 的 `check-2`、`archive` 的 `check-1`)**都不遵守后端文法** ⇒ **今天在任何样本上都读不到、也拍不到 G1 的 band**。补表后 fixture 忠于后端文法,`checking.png` 也真的会显示表 ⇒ 读数与截图同时成立。
  **⚠ 涟漪面(改的是所有门共用的样本,必须逐门实测):** `make_fixture()`(`scripts/check-05-ui-uat.py:490-498`)把 `scripts/ui-states/<name>` 整目录复制到临时目录,`check-05` / `check-06` / `check-07` / `check-09` / `check-10` 都经它消费 `checking` 样本 ⇒ 报告变长会改变 `#latest-check` 的内容与可能的高度。**先实测再处置**,不得推断(Phase 10 曾出现计划写「零布局改动」而实测矮了 3px)。
  **已实测的两条(planner 不必重查):** ①fixture `scripts/ui-states/checking/docs/DESIGN-check-2.md` **不被任何报告覆盖**(对全部 `*VERIFICATION.md` / `*VALIDATION.md` 的 `covered_files` 逐行匹配零命中)⇒ 改它**不新增连带覆盖者**。②`check-05` 对 `#latest-check` 的既有断言都**自带内容注入**(如 `--item 9` 的可达性探针注入 60 段探针正文,`:2464-2467`),不依赖 fixture 报告正文。 — **Reversibility:** costly — 撤销要重测每一个消费 `checking` 的门,并重拍截图、撤掉新断言的前提。
- **D-12-6:** **读数落成永久断言,加进 `scripts/check-09-idi09-validation.py`。** 选它的关键优势:**零新增连带覆盖者** —— `idi-11-VERIFICATION.md` 的 `covered_files` 已**同时**含 `frontend/style.css` 与 `scripts/check-09-idi09-validation.py`,而该报告本就因 `style.css` 变更而作废 ⇒ 改 check-09 不把任何新报告拖进重验名单。(对照:改 `check-10` 会新拖入归档的 `idi-10-VERIFICATION.md`。)
  **⚠ 这超出 ROADMAP 的 Gate 清单** —— 那里只写「`check-09` 的 c1..c5 与 Phase 11 改写后的契约一致」。判为**在范围内**:`G1-01` 自己要求「以运行时读数或人眼截图取证」,而审计批评的正是「门只钉令牌接线、不钉视觉契约」;新断言是 **G1 自己的判据**,**不是**被排除的「通用 blind spot 加固」(WR-04 残项,即「check-10 里没有一条 `read_style(..., 'table', ...)`」)。planner 须在计划里显式划清这条界线。
- **D-12-7:** **新断言钉「宿主 == 白」+「两者不同」** —— 既断言 `#latest-check` 的计算底色 != `#latest-check th` 的计算底色,也断言 `#latest-check` 的计算底色 == `--color-surface-page` 的解析值(白)。**为什么必须钉宿主侧:** 只钉「两者不同」的话,将来有人把宿主改成 gray-4 之类仍然绿 —— 那条判据的判别力接近「只断言规则被写下了」。「宿主 == 白」把「改白」这件事本身也锁住。
  **须配变异证明**(仓库纪律:一条不能失败的门比没有门更糟;变异测试是唯一能证明守卫真的会失败的手段):把 `#latest-check` 的底色改回 `var(--color-surface)` ⇒ 必 FAIL。变异在**已提交的树**上做、定向 `git checkout -- frontend/style.css` 还原(**禁用 `git stash`** —— 它跨工作树共享,本项目明令禁止),还原后须逐字节相同;须给出「变异 → FAIL」的**真实读数**,不得只声明做过。判据锚定与变异方向均须双向自检(正确实现能产出该读数、变异后必然失败)。 — **Reversibility:** costly — 撤销要重写判据与变异证明。
- **D-12-8:** **fixture 只加那张表,其余部分保持原样。** 只加 `| 编号 | 级别 | 位置 | 问题 | 建议修法 |` 表头 + 分隔行 + 至少一行数据(级别取 P0/P1/P2 之一),**不动** fixture 的其余内容 —— 包括它缺失的「档位头部行」(`> 自检档位:严格` / `宽松`)与既有的 `## 发现` bullet 小节。最小改动,符合仓库 CLAUDE.md 第 3 条(只碰必须碰的)。

### G1 视觉取证形态(承载 VIS-01)

- **D-12-9:** **5 张整窗图照旧 + 追加一张 `#latest-check` 元素截图。** 5 张 1440×900 整窗图(p1 / p12 / p3 / checking / archive)按 VIS-01 原文产出,落盘 `<phase-dir>/screenshots/<state>.png`(与 v1.15 同规格同路径:`.planning/milestones/v1.15-phases/idi-09-card-containers/screenshots/` 与 `idi-10-tables-and-radius-scale/screenshots/` 都含这 5 个文件名)。**额外追加一张 `#latest-check` 的元素截图**(`checking` 态,在补过表的 fixture 上)—— 理由:band 在 1440×900 整窗图里只占几十像素,局部图才是 G1-01 的直接人眼证据。实现照 `scripts/check-10-idi10-validation.py:653` 的元素截图先例(`page.locator(...).screenshot(...)`),**零新 harness**。
  **已实测的复用点:** `scripts/check-09-idi09-validation.py`(`:774` `run_screenshots`)与 `scripts/check-10-idi10-validation.py`(`:545` `run_screenshots`)都已按 `check-05` 的 `STATES`(`scripts/check-05-ui-uat.py:584` = `["p1","p12","p3","checking","archive"]`)迭代并写出 `<state>.png`,且断言 1440×900 落盘非空。新断言进 check-09(D-12-6)⇒ 局部截图也加在 check-09 的 `run_screenshots` 里最自然。
- **D-12-10:** **补的那张表紧跟 `# 核查报告 2` 标题行之后。** 理由:`#latest-check` 的 `max-height: 30vh`(`:1652`)使它是**滚动区**(900px 视口下约 270px);表放得靠下就会落在可视区之外,整窗图与元素截图**都拍不到 band**。紧跟标题行既保证可见,又最贴 `prompts.py` 的文法顺序(档位头部行 → 问题分级表 → 结论行)。

### REG-04 连带面(承载 REG-04)

- **D-12-11:** **连带面判定口径与逐份处置。** 判据锚报告 frontmatter 的 `covered_files` **逐行匹配**(**不是**全文 grep —— 全文 grep 会把只在正文提及的报告算进来),并**额外测「路径是否还在盘上」**。
  **已实测的完整形状(planner 不必重查):** 对本次全部预期改动文件(`frontend/style.css` + `scripts/check-09-idi09-validation.py` + fixture)做逐行匹配,**共 12 份报告命中**:
  - **11 份归档报告**(v1.13 三份 `01` / `02` / `03`、v1.14 五份 `idi-04` / `idi-04.1` / `idi-05` / `idi-06` / `idi-07`、v1.15 两份 `idi-09` / `idi-10`、quick 一份 `260925-iin`):命中 `frontend/style.css`(`idi-09` 另命中 `check-09`)。它们的 `covered_files` 里有 2–13 条路径**已不在盘**(`.planning/phases/...` 已移到 `.planning/milestones/v1XX-phases/...`)⇒ **fail-closed stale,属 2026-09-14 登记的已知限制**。**处置 = 登记为已知限制并在 SUMMARY 里逐份列名,不重验**(路径不可解析,重验无从下手)。**不得**为此去修复归档报告的路径 —— 那是「修归档」,超出 G1-01 / REG-04 的范围。
  - **1 份在盘**:`.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md`(`status: passed`、12/12、covered_files 16 条**零缺失**)。它以 `covered_files` 同时覆盖 `frontend/style.css` 与 `scripts/check-09-idi09-validation.py` ⇒ **本次改动必然作废它**。按 ROADMAP SC4 的字面要求处置:**以 HEAD 内容重新验证,不是刷新指纹**(内容确实变了,刷新等于断言「自验证以来什么都没变」)。
  **两份实测的零涟漪结论:** ①把 `check-09` 纳入筛选面**不新增任何报告**(`idi-09` 与 `idi-11` 已覆盖它);②fixture **不被任何报告覆盖**。
  **⚠ 注意** `state.*` 写入动词在本仓库已复现多次不可信;**核盘必须放在收口序列的最后一个动词之后**,判据一律取 ROADMAP 的 `## Milestones` + `## Progress`,**不得**从 `state.json` 的 `phases` 推。
- **D-12-12:** **「里程碑收口」不含 v1.16 里程碑审计。** 本阶段 = G1 修复 + REG-04 全量复跑 + VIS-01 截图;v1.16 的里程碑审计走 `/gsd-audit-milestone`(与 v1.15 同路径,产出 `milestones/v1.16-MILESTONE-AUDIT.md`),**不在本阶段内**。依据:Phase 12 的 Requirements 只列 `G1-01` / `REG-04` / `VIS-01`;且审计的前提是「所有阶段已收口」,在 Phase 12 内部跑会自我指涉。

### Claude's Discretion

- **新断言在 check-09 里的落位**(新增 `c6` 还是并入既有 item)与命名 —— 由 planner 定;须在计划里说明为何这样切不把两条不同阶段的契约搅在一起(check-09 现为 Phase 11 的 REG-01 载体)。
- **元素截图的具体实现细节**(选择器、文件名、是否与 5 张同目录、是否在 check-09 的 `--screenshot` 分支里产出)—— 由 planner 定,须满足「1440×900 整窗 5 张 + 局部 1 张、复用既有路径、零新 harness」。
- **`checking` fixture 报告里那张表的具体行数与内容**(列头必须逐字为 `| 编号 | 级别 | 位置 | 问题 | 建议修法 |`,级别仅 P0/P1/P2)—— 由 planner 定;须保证落在 30vh 可视区内(D-12-10)。
- **变异测试的执行顺序与还原手法细节** —— 由 planner 定,须满足 D-12-7 的三条硬性要求(已提交的树上做、定向 `git checkout`、还原后逐字节相同、禁用 `git stash`)。
- **全量复跑与截图的时间顺序** —— 由 planner 定,硬约束只有一条:两者都必须落在**最后一次 `style.css` 改动与 fixture 改动之后**(ROADMAP:`REG-04` 的「零新增失败」必须在最后一次 `style.css` 改动之后跑才成立;截图必须是最终态)。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 权威设计与需求

- `DESIGN.md` — 唯一权威设计文档(v1.14 界面信息架构改版)。本阶段直接相关:D-04(令牌纪律:只声明被消费的令牌)、D-06(零构建步骤 / 零新增运行时依赖)、§3.8(面向用户的输出语言红线)
- `.planning/REQUIREMENTS.md` — v1.16 的 12 条需求。Phase 12 覆盖 `G1-01` / `REG-04` / `VIS-01`。**Out of Scope 表与「阶段归属的裁定理由」段必读**
- `.planning/ROADMAP.md` — Phase 12 段:Goal / Rationale / Deliverables 1-4 / Success Criteria 1-5 / Avoids / Gates。**注意 D-12-1 对 Deliverable 1 路线 (a) 的选定、D-12-6 对 Gate 清单的显式超出**
- `.planning/PROJECT.md` — v1.16 里程碑目标、候选池、已移出 Out of Scope 的项(G1)

### 上游阶段的裁定与审计(必读,不得重开)

- `.planning/milestones/v1.15-MILESTONE-AUDIT.md` — **G1 的原始判据与它的三条候选处置**(「drop `#latest-check`'s own gray-2 ground / give the checks-panel table a different header rung / explicitly accept a band-less header」)+ 「check-10 只钉令牌接线而非视觉契约,58/58 PASS 与 G1 可以共存」的 blind spot 段。**D-12-1 选的是第一条**
- `.planning/phases/idi-11-decard-and-hairline-dividers/11-CONTEXT.md` — Phase 11 的全部裁定(D-11-1 统一面 = 白、D-11-2 面板并回统一面、D-11-12 c1..c4 以 computed style 为判据、D-11-13 六条变异、D-11-14 装饰性边界不登记 NON-TEXT)。**本阶段是它的收口,不得重开它的裁定**
- `.planning/milestones/v1.15-phases/idi-10-tables-and-radius-scale/10-CONTEXT.md` — 删 `--radius-lg` 的**专用残留断言先例**、`frontend/style.css` 连带指纹的**实测形状**、编辑纪律、门禁环境事实(必读,省得重踩)
- `.planning/milestones/v1.15-phases/idi-09-card-containers/09-CONTEXT.md` — D-9-1 / D-9-2 / D-9-3(已被 Phase 11 反转);`th` 的浅底(`TABLE-01`)与「表头浅底 + 仅横向分隔线」的原始裁定

### 被改动的源码与门(行号均为当前 HEAD)

- `frontend/style.css` — 本次**唯一**改动点:`:1651-1659`(`#latest-check`,待改的是 `:1657` 的 `background`)。**承重参照**:`:148`(`--color-surface-page: var(--white)`)、`:149`(`--color-surface-sunken`)、`:220`(`--color-surface: var(--radix-gray-2)`)、`:1236-1243`(`.markdown-body table` / `th, td` / `th { background: var(--color-surface) }`)、`:1244-1249`(`.markdown-body code`,gray-3 底、无边框、无等宽字体)、`:936`(`#doc-panel-header` 的 `position: sticky`)、`:129-130`(须就地改写的围栏承重注释)、`:620-622`(三条候选地面的既有 PAIR 登记)
- `frontend/index.html` — 只读:`:47` `<div id="latest-check" class="markdown-body">`(它是 `.markdown-body` 宿主的直接证据)
- `frontend/app.js` — 只读:`:624-662`(`applyPhase5View`,`:658-662` 把 `data.latest` 经 `renderMarkdown()` 注入 `#latest-check`)。**预期逐字节不改**
- `scripts/check-09-idi09-validation.py` — **本次的改写对象**:现状 c1..c5(c1 左栏 4 个 section 连续面 + 交互控件对照组、c2 `#doc-panel` 单边竖线 + sticky 表头、c3 两级刻度、c4 灰缝归零 + 发丝线逐状态普查、c5 滚动契约)。复用 `load_check05()` / `ok()` / `ok_true()` / `info()` / `read_style()` / `resolve_color()` / `fence_text()`
- `scripts/check-10-idi10-validation.py` — **本阶段不改**(见 D-12-4)。参照:`:101` `TH_BG_LITERAL = "rgb(249, 249, 249)"`(gray-2 字面量,两侧写死)、`:117-123` `TABLE_PROBES` 5 对(含 `("p1","#latest-check")`)、`:302-353` `t1` 的断言形态、`:545-570` `run_screenshots`、`:653` 元素截图先例、`:328` 过期注释(Deferred)
- `scripts/check-02-contrast.py` — 围栏内 PAIR 清单与 `TEXT_MIN` / `NON_TEXT_MIN`。**本阶段预期零改动**(D-12-1 已核实零新增条目);**围栏内注释不得出现「令牌名 + 冒号」**(`DECL_RE` 扫围栏全文含注释)
- `scripts/probe-card-border-token.py` — `:45` 把 `#latest-check` 列为**非卡片对照样本**(读 `border-top-color` = gray-6)。本阶段不改它、也不改它读的那条声明
- `scripts/check-05-ui-uat.py` — 门环境与样本来源:`:490-498` `make_fixture`、`:584` `STATES`、`:979-994` `MARKDOWN_TARGETS` / `MARKDOWN_HOSTS`、`:2436` `PANEL_SCROLLERS`、`:2464-2467` 可达性探针正文
- `scripts/check-01-token-conformance.sh` / `scripts/check-03-hidden-uniqueness.sh` / `scripts/check-04-important-count.sh` — 三条恒不变式(令牌块外零裸 `#hex` 与零 tier-1 引用;`^\.hidden {` 恒为 1;`!important` **声明**数恒为 1)
- `backend/prompts.py` — `:486-502` 报告文法(「问题分级表」列头逐字 + 结论行形态),**D-12-5 补 fixture 的依据**

### 被改动的 fixture 与截图

- `scripts/ui-states/checking/docs/DESIGN-check-2.md` — **本次改动点**(补那张表,紧跟标题行)。`checking` 是**唯一** `#latest-check` 可见的样本
- `scripts/ui-states/archive/docs/DESIGN-check-1.md` — 只读:同族报告(结论为 `PASS`),**本阶段不动**
- `scripts/ui-states/p3/docs/discuss-round-2.md` — 只读:`#round-doc` 的表格样本(check-10 的第 5 对)
- `.planning/milestones/v1.15-phases/idi-09-card-containers/screenshots/` 与 `.../idi-10-tables-and-radius-scale/screenshots/` — 5 张截图的**落盘约定与文件名先例**(p1 / p12 / p3 / checking / archive)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `scripts/check-09-idi09-validation.py` 的 `load_check05()` 复用机制 —— `ok()` / `ok_true()` / `blocked()` / `info()` / `read_style()` / `resolve_color()` / `resolve_token()` / `norm()` 全部可直接沿用;新断言无需新辅助函数
- `scripts/check-10-idi10-validation.py:653` 的**元素截图**写法(`page.locator(SEL).screenshot(path=...)`)—— G1 局部特写直接照搬
- `scripts/check-09-idi09-validation.py:774` / `check-10:545` 的 `run_screenshots()` —— 已按 5 个样本迭代并断言 1440×900 落盘非空,VIS-01 直接复用
- `frontend/style.css` 的**单一 `:root` 令牌围栏** —— 一切改动要么在围栏内改值、要么在围栏外的规则体内改声明;零新增 primitive、零新增颜色值
- `--color-surface-page`(白)已是统一面,`#latest-check` 直接改消费它即可,**不需要任何新令牌**

### Established Patterns

- **就地改写,不追加覆盖** —— 留下已死的声明会让注释与代码互相矛盾(Phase 9 对 `#doc-panel` 的 `border-left`、Phase 10 对表格 `border`、Phase 11 对 5 个容器用的是同一手法)
- **追加,不重排** —— 至少一对等特异性规则由源码顺序决定;重排即渲染变更,而源码 diff 看起来完全无辜
- **每个 `style.css` 计划必须带至少一项运行时验证** —— 真实浏览器的 computed style 读数;`grep -c 'var(--'` 对渲染结果零证明力
- **门禁纪律** —— 一条不能失败的门比没有门更糟;删除断言 / 放宽阈值 / 降级为恒真 / 只断言「规则被写下了」全部禁止;**变异测试是唯一能证明守卫真的会失败的手段**;判据的锚点须**可满足且有判别力**(正确实现能产出该字面量,且它别处不也有)
- **计数门的算术陷阱** —— `check-04` 数的是 `!important;` **声明**数(恒为 1),不是命中行数;解释性注释的散文会把 `grep -c` 顶高(本项目已因此红过三次)。围栏外的机械判据是子串计数,连论证性散文都会把它顶高
- **装饰性边界不登记 NON-TEXT** —— `--color-border-subtle` 在多个地面上都不达 3.0,但仓库有既有论证(「分隔线不标识任何控件/状态 ⇒ SC 1.4.11 不适用」),该论证在计划里**不得省略、不得默认**

### Integration Points

- **G1 的两个碰撞面**:`#latest-check`(`:1657`)与 `.markdown-body th`(`:1243`)—— 本次只动前者
- `check-09` 是 Phase 9 自建、Phase 11 承重改写的运行时门 ⇒ 本阶段在它上面加 G1 断言;`check-10` 的 `t1` 钉的是 `th` 接线(本阶段不改 `th`,故它保持全绿)
- `#latest-check` 只在 `checking` 样本可见(`p1` 下祖先 `#checks-panel` 带 `.hidden`)—— 一切运行时取证与截图都必须落在该样本上
- `check-05` 的 `make_fixture()` 是所有浏览器门共享的样本入口 ⇒ fixture 改动的涟漪面必须逐门实测

</code_context>

<specifics>
## Specific Ideas

- **G1 的根因是一处不对称,不是一处配色失误。** 四个 `.markdown-body` 宿主里,`#draft-content` / `#brainstorm-content` / `#round-doc` 都不画底色(继承白面板),只有 `#latest-check` 自己画 gray-2 ⇒ 只有它内部的 `th`(同样 gray-2)消失。修法因此是**消除不对称**,而不是给表头换色。
- **审计给的三条候选处置**(原文,`v1.15-MILESTONE-AUDIT.md`):「drop `#latest-check`'s own gray-2 ground, give the checks-panel table a different header rung, or explicitly accept a band-less header there」—— **用户选了第一条**;第三条(接受无 band)被明确排除,因为 G1 是被点名的范围。
- **「表头 band 消失」的准确含义**:`th` 的 `border-bottom` 发丝线**一直在**(`th, td` 共享 gray-6 下边线),消失的是**表头那一档底色** —— 表头行因此与数据行读起来一样。判据要锚的正是这个,不是「有没有一条线」。
- **band 的强度被显式接受为 1.053**(gray-2 on white)。用户看过这个读数后仍选「锚「底色不同」」,即**不追求更强的 band** —— planner 不得自作主张去加深它。
- **fixture 不忠于后端文法是 G1 从未被看见的机械原因**:`backend/prompts.py:494-499` 要求每份自检报告都带「问题分级表」,而两个 fixture 报告都没有 ⇒ 样本里从来就没有可消失的 band。

</specifics>

<deferred>
## Deferred Ideas

- **`check-10` t1 的过期注释**(`scripts/check-10-idi10-validation.py:328` 的 `note="…HEAD 上 th 无自身底色(透明)"`)—— 审计点名的 supporting tell,属「gate blind spot」项;路线图已列为未裁定。改它会新拖入归档的 `idi-10-VERIFICATION.md`
- **报告区表头在 `#latest-check` 内 sticky**(与 `#doc-panel-header` 的 `position: sticky` 同语言)—— 新能力,超出 G1-01
- **`#latest-check` 的边框 / 圆角改动** —— 本阶段明确不动(D-12-3);若日后要贴合「连续面」需另开裁定
- **G2**(`--radix-gray-1` 零消费 + 补一条**通用的**围栏消费断言)—— 用户只裁定「连带 G1」,**G2 未点名**,留待下一里程碑
- **`999.2`**(Phase 7 交互态暴露的三条 affordance 缺陷)—— 未点名;执行它会作废 `idi-07` 的 `passed` 指纹
- **`A11Y-V2-01/02` / `FLOW-V2-01/02` / `TOKEN-V2-01`**(暗色模式)—— 均未点名,v1.14 已显式排除
- **Nyquist 缺口**(`idi-04` / `idi-06` / `idi-09` / `idi-10` 无 `VALIDATION.md`)—— 未点名;建议走 `/gsd-validate-phase`,不占本里程碑范围
- **图标与空状态** —— 用户 2026-09-27 与 2026-09-28 两次均未点名,仍留 Out of Scope
- **11 份归档报告的可执行性**(路径不在盘 ⇒ fail-closed stale)—— 本阶段按已知限制登记,不修复归档路径
- **v1.16 里程碑审计** —— 不在本阶段内,走 `/gsd-audit-milestone`

</deferred>

---

*Phase: 12-G1 表头 band 与里程碑收口*
*Context gathered: 2026-09-29*

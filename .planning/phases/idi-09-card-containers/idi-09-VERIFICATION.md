---
phase: idi-09-card-containers
verified: 2026-09-27T12:33:32Z
status: passed
score: 24/24 must-haves verified
covered_files:
  - .planning/phases/idi-09-card-containers/idi-09-01-PLAN.md
  - .planning/phases/idi-09-card-containers/idi-09-01-SUMMARY.md
  - .planning/phases/idi-09-card-containers/idi-09-02-PLAN.md
  - .planning/phases/idi-09-card-containers/idi-09-02-SUMMARY.md
  - .planning/phases/idi-09-card-containers/idi-09-03-PLAN.md
  - .planning/phases/idi-09-card-containers/idi-09-03-SUMMARY.md
  - frontend/style.css
  - scripts/check-05-ui-uat.py
  - scripts/check-09-idi09-validation.py
  - scripts/probe-card-border-token.py
covered_digest: "v1:sha256:7b82f8d1c2f5f6e371effbe73c5182a4ed78d49eecbea3ea76cca3e76d6a7031"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: passed
  previous_score: 24/24
  gaps_closed: []
  gaps_remaining: []
  regressions: []
human_verification: []
---

# Phase 9: 卡片容器化与页面底色下沉 Verification Report

**Phase Goal:** 左栏 4 个面板(会话流 / 本轮批注流 / 自检报告 / AI 工作面板)与右栏文档区各自成为白底卡片容器(白底 + 可见边界 + 圆角 + 极轻阴影 + 内边距),页面底色下沉至 `--radix-gray-3`(#f0f0f0) —— 界面首次拥有 elevation 层次,并与既有 `--color-surface`(gray-2,控件内陷面)接成连贯三级刻度:gray-3(页面)< gray-2(内陷面)< 白(卡片)。
**Verified:** 2026-09-27T12:33:32Z (HEAD = `35f046e`)
**Status:** passed
**Re-verification:** Yes — twice. First after the user-ruled amendment (quick `260926-vaf`); again after Phase 10 (`idi-10-tables-and-radius-scale`), which changed one `covered_file` by real content change

## Why this is a re-verification, and what changed

The previous report (`status: passed`, 21/21) was **stale by real content change**, not by a
bookkeeping edit. Two of its `covered_files` were deliberately modified after it was written:

- `frontend/style.css` (`8faa4fe`, `6ce0923`)
- `scripts/check-09-idi09-validation.py` (`6ce0923`)

The change landed the strength decision that Phase 9 itself parked as an open item, on the user's
explicit ruling (2026-09-26): 「边框与阴影强度,现在太轻了,稍微重一点」. Four value-level edits:

| # | File | Change |
|---|------|--------|
| 1 | `frontend/style.css:335` | `--shadow-card` `0 1px 2px rgba(0,0,0,0.04)` → `0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04)` (two layers) |
| 2 | `frontend/style.css:747` / `:765` | the two card borders `--color-border-subtle` (gray-6) → `--color-border` (gray-7) |
| 3 | `frontend/style.css:~728-738` | the card-rule comment rewritten (it had asserted the now-overridden "must stay `--color-border-subtle`" constraint) |
| 4 | `scripts/check-09-idi09-validation.py:89-90` + `shadow_lengths` docstring | the two pinned shadow constants re-registered to the ruled value |

Plus one new file: `scripts/probe-card-border-token.py` (a runtime probe for the card border colour,
a seam no existing gate read).

**This is a ruling, not a regression.** The old values are superseded; where this report's numbers
differ from the previous report's pinned literals, the difference IS the ruling. The phase goal was
re-derived from HEAD and the amendment was checked for whether it *holds* or *weakens* the goal —
conclusion below (it holds).

### Phase 10 re-verification (2026-09-27) — `frontend/style.css` changed again

**This is a re-verification against HEAD content, NOT a fingerprint refresh.** Of this report's ten
`covered_files`, exactly one was modified by Phase 10 (`idi-10-tables-and-radius-scale`):

- `frontend/style.css`

The other nine (`idi-09-01/02/03` PLAN+SUMMARY pairs, `scripts/check-05-ui-uat.py`,
`scripts/check-09-idi09-validation.py`, `scripts/probe-card-border-token.py`) are byte-identical to
the previous verification — `git diff --stat 27fbf20..HEAD -- frontend/app.js frontend/index.html
scripts/check-05-ui-uat.py` is empty, and `git status --porcelain frontend/ scripts/` is empty.

Because a covered input genuinely changed, refreshing the digest would have asserted "the covered
inputs are unchanged since verification" — a false statement. The digest below was **recomputed**
from HEAD; it differs from the previously stored value:

| | `covered_digest` |
|---|---|
| stored before this re-verification | `v1:sha256:6e811a1122c2e6d5c63308554a39c5d2d8dce462abef73847f0c7be39e2bb89e` |
| recomputed on HEAD | `v1:sha256:7b82f8d1c2f5f6e371effbe73c5182a4ed78d49eecbea3ea76cca3e76d6a7031` |

**What Phase 10 changed in `frontend/style.css`** (48 insertions / 5 deletions vs `27fbf20`; the
report's own line numbers above are pre-Phase-10 coordinates — the file grew, and every cited rule
resolves to the same selector text on HEAD):

| # | Change | Where (HEAD) |
|---|--------|--------------|
| 1 | Table rules rewritten **in place** (D-10-1): `.markdown-body th, .markdown-body td`'s `border: 1px solid var(--color-border)` → `border: none;` + `border-bottom: 1px solid var(--color-border-subtle);`; a new one-line rule `.markdown-body th { background: var(--color-surface); }` appended | `:1112-1118` |
| 2 | Radius scale converged to `8 / 10 / 999` (D-10-2): the `--radius-lg: 28px;` declaration **deleted**; `.chat-user` → `var(--radius-md)`; `#chat-input-row input` → `var(--radius-pill)` | `:408-410`, `:1211`, `:1245` |

**Why this does not touch any of the 24 must-haves.** The table change lands inside `.markdown-body`
and the radius change moves two consumers between existing rungs; neither intersects the card-container
language this report asserts:

- the five card containers' `background` / `border` / `border-radius` / `box-shadow` are untouched —
  the two card rules still read `border: 1px solid var(--color-border)` (`:755`, `:773`), and the card
  tokens `--color-surface-card` (`:334`) / `--shadow-card` (`:335`) are unchanged and still inside the
  fence (`:5` → `:695`);
- `--radius-md` (10px) is **preserved** — it is what `check-09-idi09-validation.py` dynamically resolves
  for its card-corner assertions, so deleting it would break c1/c2. Phase 10 kept it; only `--radius-lg`
  was removed;
- the four non-card `--color-border-subtle` consumers are the same four rules and untouched
  (`.event-list` `:929`, `.annotation-item` `:1320`, `.badge-answered` `:1371`, `#latest-check` `:1530`);
- `check-02`'s threshold constants and pair list are byte-identical (`git diff 27fbf20..HEAD --
  scripts/check-02-contrast.py` is empty; PAIR = 53, ORDER = 1).

**Gates re-run for this re-verification (raw readings, not citations):**

| Gate | Command | Reading on HEAD |
|------|---------|-----------------|
| Phase 9's own runtime gate | `.venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2 --item c3 --item c4 --item c5` | `exit=0`; c1:26 / c2:13 / c3:3 / c4:4 / c5:5, **0 FAIL / 0 BLOCKED** |
| Card border probe | `.venv/bin/python scripts/probe-card-border-token.py` | `exit=0`; 5/5 cards `rgb(206,206,206)`, 2/2 readable non-card controls `rgb(217,217,217)`, token distinguishability PASS |
| Contrast | `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`; 53 PASS + 1 ORDER; the header's drawing surface is covered by the pre-existing `PASS 15.48 --color-text on --color-surface`; the re-attributed pairs read `PASS 4.77 --color-marker-active on --color-surface-card` / `PASS 3.32 --color-border-strong on --color-surface-card` |
| Static gates | `bash scripts/check-01/03/04-*.sh` | three × `PASS`, `exit=0` |
| pytest | `.venv/bin/python -m pytest backend/tests -q --tb=short` | `219 passed, 6 skipped` |
| app.js syntax | `node --check frontend/app.js` | `exit=0`, zero output |
| Mutation probes | `scripts/probe-05-resolve-color.py` / `scripts/probe-07-focus-composite.py` | both `exit=0`; probe-07 `ratio=3.54 (>= 3.0)`; probe-05 control branch `PASS` |
| `check-05` / `check-06` / `check-07` | `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` etc. | cited from `.planning/phases/idi-10-tables-and-radius-scale/gate-logs/` (Phase 10 plan 03). Those logs are still valid for HEAD: `git diff --stat a98c788..HEAD -- frontend/ scripts/` is **empty**, so the inputs those gates read are byte-identical. `check-05` `exit=2` by design, ten items 0 FAIL, BLOCKED only on item 5's two `--ai-smoke` legs |

**Two literal readings in the table above moved, and are explained rather than silently restated:**

1. **Truth 5's `--color-border` consumer count `3 → 2`.** The third consumer was
   `.markdown-body th, .markdown-body td` — Phase 10's D-10-1 rewrote it in place. It is *not* one of
   the four non-card `--color-border-subtle` consumers that truth 5 asserts are untouched, and those
   four are still exactly four. The claim's substance (the amendment's change surface was strictly the
   two card rules; the four non-card subtle consumers were untouched) holds on HEAD.
2. **Truth 24's top-level selector count `173 → 174`.** `173 = 173` was the Phase 9 pair
   (`3ec6558` baseline vs `27fbf20` HEAD) and that pair is still identical. Today's HEAD is `174`
   because Phase 10 appended exactly one new top-level rule — `.markdown-body th` — which is Phase 10's
   own sanctioned append, not a Phase 9 reordering. The added selector is the only difference; nothing
   was removed or moved (`app.js` / `index.html` / `vendor/` remain zero-byte changed).

**The `#round-doc` −3px geometry note (carried forward from Phase 10 plan 03) does not touch any claim
here.** Phase 10 measured `#round-doc`'s height falling `778.640625 → 775.640625` on the `p3` fixture
(one collapsed table box loses its top edge per table, three tables ⇒ 3px). This report cites no
`#round-doc` absolute height. Its only geometry citation is `#doc-panel`'s `scrollHeight 2488 >
clientHeight 898` (truth 8), re-measured on HEAD as `2488 / 898` — unchanged. The other geometry
readings it relies on (`check-05 --item 8`'s sticky `header={'top':1,'bottom':35} ⊆ panel={'top':0,
'bottom':900}`, `L-2` overflow `0px` at 1440/1024/768, `docPanelWidth` 432/340/340) are on `#doc-panel`
/ `#doc-panel-header` and are byte-identical in Phase 10's `check-05-full.log` versus Phase 9's.

**Nature statement.** This section records a **re-verification against HEAD content**: the criteria
were re-run, all 24 must-haves were re-derived from HEAD, and `covered_digest` was recomputed. It is
not a fingerprint refresh — the covered input `frontend/style.css` genuinely changed, so refreshing
would have been an untrue assertion.

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | **SC1** 左栏 4 个 section 在真实浏览器里各自呈现为独立卡片:计算底色 = `--color-surface-card`(白),不再是 `rgba(0,0,0,0)` 完全透明 | ✓ VERIFIED | 我本进程重跑 `check-09 --item c1`:`#session-panel` / `#annotations-panel` / `#checks-panel` / `#ai-panel` 四条 `background-color=rgb(255, 255, 255)` 全 PASS(26 条断言 0 FAIL);截图 `p1.png` 目视:四个白卡片浮在灰页面上 |
| 2 | **SC1** 左栏 4 个 section 计算 `border-top-left-radius` = `--radius-md`(10px)、`border-top` = `1px solid`、`box-shadow` 非 `none` | ✓ VERIFIED | c1 逐 section 读数 `border-top-left-radius=10px` / `border-top=1px solid` / `box-shadow=rgba(0,0,0,0.08) 0px 1px 3px 0px, rgba(0,0,0,0.04) 0px 1px 2px 0px`,全 PASS |
| 3 | **SC1** 卡片之间有可见间隙(计算 `gap` = 12px),间隙里透出的是页面底色 gray-3 | ✓ VERIFIED | c4 `[p1] #main-pane 计算 gap == 12px` PASS;截图 `p1.png` / `p12.png` 目视:卡片间有灰色竖缝,缝隙颜色与页面底一致 |
| 4 | **SC1 / CARD-01【修正案】** 卡片边界色在真实浏览器里 = `--color-border`(gray-7,`rgb(206,206,206)`);我本进程重跑新探针 | ✓ VERIFIED | `scripts/probe-card-border-token.py` exit 0:5/5 卡片 `border-top-color=rgb(206, 206, 206)`;前置判据 `--color-border != --color-border-subtle` PASS(206 vs 217) |
| 5 | **SC1 / 改动面【修正案】** 边界改动面严格是两处卡片:四处非卡片 `--color-border-subtle` 消费者一字未动 | ✓ VERIFIED | `grep -c 'border: 1px solid var(--color-border);'` = **3**(2 卡片 + 既有 `.markdown-body th/td` @`:1083`,相位前即存在);`...--color-border-subtle);` = **4**(`:921` / `:1277` / `:1328` / `:1487`);探针的非卡片对照 `.event-list` / `#latest-check` 均 `rgb(217,217,217)` PASS(另 2 个候选在 p1 样本里不存在,INFO 不计入)。**【Phase 10 复核 2026-09-27】** 第一个计数在 HEAD 上已是 **2**(`--color-border` 消费者只剩两处卡片 `:755` / `:773`):Phase 10 的 D-10-1 把第三个消费者 `.markdown-body th, .markdown-body td` 就地改写为 `border: none` + `border-bottom`。该规则**不属于**本行主张的「四处非卡片 `--color-border-subtle` 消费者」,故本行的实质在 HEAD 上仍成立 —— 四处仍是 `.event-list`(`:929`)/ `.annotation-item`(`:1320`)/ `.badge-answered`(`:1371`)/ `#latest-check`(`:1530`),计数仍为 **4**,探针读数仍 `rgb(217,217,217)`;详见「Phase 10 re-verification」一节 |
| 6 | **SC2** `#doc-panel` 与左栏同族卡片:四边 `1px solid` / 圆角 `--radius-md` / 底色卡片白 / 阴影非 `none`;原 `border-left: 1px` 单边凹陷读感被取代 | ✓ VERIFIED | `check-09 --item c2`(13 条断言 0 FAIL):四边 width `1px` / style `solid`,圆角 `10px`,底色 `rgb(255,255,255)`,`box-shadow` 两层值;`grep -n 'border-left: 1px solid'` 无残留死声明 |
| 7 | **SC2** `#doc-panel-header` 计算底色 = 卡片白,sticky 遮挡机制保持 | ✓ VERIFIED | `frontend/style.css:808` `background: var(--color-surface-card)`;`check-05 --item 8` 我本进程重跑:`header={'top':1,'bottom':35} ⊆ panel={'top':0,'bottom':900}`,且 `|header.top - panel.top| = 1.000px` PASS;c2 对照组 `#doc-panel-header box-shadow == none` PASS |
| 8 | **SC2 / REG** `#doc-panel` 计算 `overflow-y` 仍为 `auto`(承重滚动契约,sticky 表头依赖它) | ✓ VERIFIED | c2 与 c5 各一条 `overflow-y == auto` PASS;c5 先在 `scrollHeight 2488 > clientHeight 898` 的可滚前提下再断言表头 ⊆ 面板 |
| 9 | **SC3** `body` 计算底色 = gray-3 `rgb(240,240,240)`,且底色来自令牌(不是硬编码) | ✓ VERIFIED | c3 两条互为对照:`body background-color == rgb(240, 240, 240)` 且 `--color-surface-page` 解析值 == body 计算底色;`style.css:139` `--color-surface-page: var(--radix-gray-3)` |
| 10 | **SC3** 三档亮度严格递增 gray-3 < gray-2 < 白,且屏幕级同帧共存 | ✓ VERIFIED | c3 令牌级 `0.871367 < 0.947307 < 1.000000`;我**独立算术**复算 gray-3/gray-2/白 = `0.871367 / 0.947307 / 1.000000` 逐位吻合;屏幕级由我自己的探针补证:同帧渲染 `select#ai-route-select` / `#round-switcher` / `#check-switcher` / `#btn-ping` / `#btn-abort` / `#ai-events` / `#latest-check` / `.overlay-card` 等 14 个 gray-2 `rgb(249,249,249)` 载体,与白卡片 `rgb(255,255,255)`、页面 `rgb(240,240,240)` 并存 |
| 11 | **SC3 / D-9-2** 密度紧凑档:`#main-pane` `gap` 12px、`.panel-body` `padding` 16px;`#doc-panel-body` 逐字未动 | ✓ VERIFIED | c4 四条:`gap=12px` / `.panel-body padding=16px` / 对照组 `#doc-panel-body padding=32px 40px` / 对照组 `.panel-header padding-top=6px`;`check-05 --item 4` 独立断言 `#doc-panel-body padding == "32px 40px"` PASS |
| 12 | **VIS-01** 卡片令牌(`--color-surface-card` / `--shadow-card`)落在围栏 `:root` 内;`check-01` PASS | ✓ VERIFIED | `style.css:334-335` 落在围栏 `:5`…`:687` 之间;我重跑 `bash scripts/check-01-token-conformance.sh` → `PASS` exit 0 |
| 13 | **VIS-01** 零新增 tier-1 原语(`--color-surface-card` 是既有 `--white` 的别名) | ✓ VERIFIED | `style.css:47` `--white: #ffffff` 已在;`style.css:334` `--color-surface-card: var(--white)`;相位内新增 `--radix-*:` 声明数 = 0;check-01 PASS |
| 14 | **VIS-02** 卡片圆角取自既有 `--radius-md`,零新增圆角值 | ✓ VERIFIED | 半径刻度 `--radius-sm/md/lg/pill`(`:403-406`)相位内逐字未改;相位 diff 无新增半径字面量;卡片规则只用 `var(--radius-md)` |
| 15 | **VIS-02 / D-9-3【修正案】** `--shadow-card` 零位移、不参与布局(两层值下首层 offset-x 仍 `0px`) | ✓ VERIFIED | 我读 `style.css:335` 逐字 `0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04)` —— **两层 offset-x 都是 0**;c1/c2 实测分量 `['0px','1px','3px','0px,','0px','1px','2px','0px']` ⇒ 首层 `lengths[0] == '0px'` PASS;卡片规则体内无 `margin` / `position` |
| 16 | **VIS-02** 卡片规则体内不含 `transform` / `filter` / `will-change` / `contain` / `perspective` / `opacity` / `position` / `z-index` / `overflow` 任何一项 | ✓ VERIFIED | 我按块边界提取 `#main-pane > section` 与 `#doc-panel` 的规则体(剥注释)逐属性核对:`#main-pane > section` → `width/max-width/background/border/border-radius/box-shadow`;`#doc-panel` → `flex/display/flex-direction/overflow-y/border/background/border-radius/box-shadow/min-width`;禁令属性 **NONE** |
| 17 | **REG-01** `check-02` 全部对比度对仍达标 | ✓ VERIFIED | 我重跑 `.venv/bin/python scripts/check-02-contrast.py` → `PASS: 0 failures`,53 条 `PASS` + 1 条 `ORDER` |
| 18 | **REG-01** 登记是「重算」而非「刷新」:台账旧值→新值链条与独立算术逐位一致 | ✓ VERIFIED | 我**独立算术**复算:gray-1 侧 `15.88 / 5.77 / 5.72 / 4.65 / 3.24`,gray-3 侧 `14.30 / 5.19 / 5.15 / 4.18 / 2.91`,卡片白侧 `4.77 / 3.32` —— 与台账及 check-02 运行时输出**逐位吻合**,含两条 gray-3 上跌破阈值的中间调(4.18 < 4.5、2.91 < 3.0) |
| 19 | **REG-01** 两条跌破阈值的配对按实际绘制面重新归属到卡片底色并在白底达标;全程零颜色值改动、零新增 primitive、零阈值放宽、零 PAIR 增删 | ✓ VERIFIED | `style.css:624/635` 两条 `PAIR … ON --color-surface-card`;check-02 打印 `PASS 4.77` / `PASS 3.32`;`git diff 3ec6558..HEAD -- scripts/check-02-contrast.py` **为空**;`TEXT_MIN = 4.5` / `NON_TEXT_MIN = 3.0` 逐字未动;`grep -o '/\* PAIR'` = **53**、`/\* ORDER` = **1** |
| 20 | **REG-02** `check-05` 全量:十项 FAIL 计数全 0,退出码 2,BLOCKED 只出现在 item 5 的两条 `--ai-smoke` 腿 | ✓ VERIFIED | 我本进程重跑 `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` → exit 2;`=== 逐项结论 ===` 十项 `0 FAIL`;仅有的 2 条 BLOCKED 行都带 `需要真实 AI 调用,默认不执行;加 --ai-smoke 重跑`;与 `gate-logs/check-05-full.log` 的结论块**逐字相同** |
| 21 | **REG-02** `check-06` / `check-07` / `probe-05` / `probe-07` 退出码全 0 | ✓ VERIFIED | 我本进程重跑:`check-06` exit 0(g1…g6 = 9/2/12/5/5/7 条 0 FAIL);`check-07` exit 0(g1…g4 = 21/39/10/3 条 0 FAIL);`probe-05` exit 0(`mutated-prefix=PASS` / `mutated-postfix=BLOCKED`(变异对照支)/ `control=PASS`);`probe-07` exit 0(`ground=rgb(255,255,255) ratio=3.54 >= 3.0`) |
| 22 | **REG-02** 四个静态门 PASS + pytest 基线不降 + `node --check` 通过 | ✓ VERIFIED | 我重跑 `check-01` / `check-03` / `check-04` 全部 `PASS` exit 0;`check-02` `PASS: 0 failures`;`.venv/bin/python -m pytest backend/tests -q --tb=short` = `219 passed, 6 skipped`;`node --check frontend/app.js` exit 0 |
| 23 | **REG-02** 无一条门被弱化;修正案的两条守卫都是**真守卫**(会红、断言零删除) | ✓ VERIFIED | `git diff 3ec6558..HEAD -- scripts/check-05-ui-uat.py` 仅 6 增 4 删,全在 item5 的 `.hint` 期望侧与注释,`ok(...)` 等值形式一字未变;修正案后 `check-09` 的 `ok|ok_true|blocked` 调用点数(21/6/6)与修正案前**完全相同**(断言零删除);`SHADOW_CARD_LITERAL` 以 `norm(actual) == norm(expected)` **严格等值**比较,旧值 `0 1px 2px rgba(0,0,0,0.04)` ≠ 新值 ⇒ 回退即 FAIL(我在本进程直接跑该比较函数验证判据可区分);探针的前置判据 `--color-border != --color-border-subtle`(206 vs 217)保证回退到 gray-6 时主判据会红 |
| 24 | 编辑纪律:追加不重排、`app.js` / `index.html` / `vendor/` 零字节改动、截图交付、开放项清单 | ✓ VERIFIED | 我把相位基线(`3ec6558`)与 HEAD 的顶层选择器序列逐行 diff:**173 = 173,完全相同**;`git status --porcelain frontend/` 为空;`ls frontend/vendor/` 仅 `marked.min.js`;两个截图目录各 5 张 PNG,IHDR 全部 `1440x900`,相位 9 的字节数与 HEAD blob 逐字一致(88685/123949/123449/68115/124136);4 条开放项我逐条独立复现(见下)。**【Phase 10 复核 2026-09-27】** 选择器计数在 HEAD 上是 **174** —— 相位基线 vs Phase 9 HEAD 这一对仍是 **173 = 173**(本次以顶层选择器解析复核,逐条相同);多出的 1 条是 Phase 10 自己追加的 `.markdown-body th`(唯一新增,零删除零重排),属 Phase 10 的合规追加而非 Phase 9 的重排。4 条开放项在 HEAD 上仍为开放(静态复核:`.overlay-card` 的 `background: var(--color-surface)` 仍在 `:988`;`#main-pane` 仍只有 `gap`、无 `padding` / `margin`;四个文本 input 的 `background` 声明数仍为 **0**);详见「Phase 10 re-verification」一节 |

**Score:** 24/24 truths verified (0 present-behavior-unverified)

### Required Artifacts

| Artifact | Expected | Status | Details |
| -------- | -------- | ------ | ------- |
| `frontend/style.css` | 围栏内两个卡片令牌 + 五个容器的卡片语言 + 8 条配对重算台账;修正案:两处卡片边界令牌 + 两层阴影 | ✓ VERIFIED | `:334-335` 令牌、`:743-750` 左栏卡片、`:762-771` 右栏卡片、`:808` 表头底色、`:849` 密度、`:508-553` 台账;选择器序列 173 条与相位前完全相同;修正案的 4 处编辑全部就地 |
| `scripts/check-09-idi09-validation.py` | Phase 9 运行时门 c1…c5 + `--screenshot DIR`;修正案:两个阴影常量重新登记 | ✓ VERIFIED | 552 行;我重跑 c1(26)/c2(13)/c3(3)/c4(4)/c5(5) 全 PASS exit 0;`SHADOW_CARD_LITERAL` / `SHADOW_CARD_COLOR` 已是裁定值,`shadow_lengths` docstring 按两层值修正 |
| `scripts/probe-card-border-token.py` | 【新】卡片容器 `border-*-color` 的运行时探针(既有六条门的零覆盖缝) | ✓ VERIFIED | 148 行;我重跑 exit 0:①令牌解析 + 可区分性(防恒真)②5 个卡片 `rgb(206,206,206)` ③2 个可读非卡片对照 `rgb(217,217,217)` ④结果行;不写盘、不进任何 check 调用链 |
| `scripts/check-05-ui-uat.py` | 仅 `.hint` 实际背景断言的期望侧重新登记 | ✓ VERIFIED | 相位内净 diff 仅 item5 内 6 增 4 删;断言形式(精确等值)与强度未变;修正案零触碰 |
| `.planning/phases/idi-09-card-containers/screenshots/` | 5 个状态样本 1440×900 整窗截图(修正案前) | ✓ VERIFIED | 5/5 在场,IHDR 全部 `1440x900`,字节数与 HEAD blob 逐字一致;我逐张目视:页面灰、可见容器白底带边界与圆角、卡片间灰色间隙、右栏与左栏同族 |
| `.planning/quick/260926-vaf-card-border-shadow-strength/screenshots/` | 5 个状态样本 1440×900 整窗截图(修正案后) | ✓ VERIFIED | 5/5 在场,IHDR 全部 `1440x900`;与修正案前同名的 5 张字节数均不同(p1 88685→88907 等)⇒ 确为渲染内容真变 |
| `.planning/phases/idi-09-card-containers/gate-logs/` | 原始门禁 stdout | ✓ VERIFIED | 9 份;`check-09-shot.log` 逐字记录修正案**前**的单层阴影读数(`rgba(0, 0, 0, 0.04) 0px 1px 2px 0px`),与 HEAD 的两层读数形成对照;`check-05-full.log` 的结论块与我本进程重跑逐字相同 |

### Key Link Verification

| From | To | Via | Status | Details |
| ---- | -- | --- | ------ | ------- |
| 围栏内 `--color-surface-card` | `#main-pane > section` / `#doc-panel` / `#doc-panel-header` 的 `background` | `var()` 引用(三处消费者) | ✓ WIRED | 运行时解析 `rgb(255,255,255)`,三处计算底色全部等于该值 |
| 围栏内 `--shadow-card` | 左栏 section 与 `#doc-panel` 的 `box-shadow` | 零位移普通 box-shadow(修正案后两层) | ✓ WIRED | 两处消费者;读数两层值,表头对照组恒 `none`(阴影未误加到表头) |
| 围栏内 `--color-border` | 两条卡片规则的 `border` | `var()` 引用【修正案新增的接线】 | ✓ WIRED | 探针运行时读得 5/5 卡片 `border-top-color = rgb(206,206,206)` = `--color-border` 解析值 |
| 围栏内 `--color-surface-page` | `html, body` 的 `background` | 唯一消费者 | ✓ WIRED | `grep -n "var(--color-surface-page)"` 恰 1 处(`style.css:693`);`body` 计算底色 == 令牌解析值 == `rgb(240,240,240)` |
| `#main-pane` 的 `gap: var(--space-3)` | 左栏卡片之间的可见间隙 | flex gap 透出页面底色 | ✓ WIRED | 计算 `gap` 12px;`#main-pane` 无自身背景 ⇒ 间隙透出 body 的 gray-3(截图可见) |
| `/* PAIR --color-marker-active ON --color-surface-card TEXT */` | 三个面板 `.panel-header h2` | 卡片化后标题确实画在白卡片上 | ✓ WIRED | check-02 `PASS 4.77`;NON-TEXT 半条按注释刻意留在页面地面(4.18,更严的一侧) |
| `/* PAIR --color-border-strong ON --color-surface-card NON-TEXT */` | input / select 静止边框 | input 不声明 `background` ⇒ Chrome 画 UA 白填充 | ✓ WIRED | check-02 `PASS 3.32`;我的探针实测四个文本 input 计算底色全 `rgb(255,255,255)` |
| `#doc-panel` 的 `overflow-y: auto` | `#doc-panel-header` 的 sticky 遮挡 | 滚动容器裁剪到带圆角的 padding box | ✓ WIRED | c5 在已证明可滚的前提下断言表头 ⊆ 面板;check-05 item 8 `1.000px` 对闭区间 `<= 1.0` 通过(余量为零,事实未变) |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| -------- | ------------- | ------ | ------------------ | ------ |
| 五个卡片容器的 `background` / `border` / `border-radius` / `box-shadow` | computed style | 围栏 `:root` 的 tier-2 令牌 → `var()` | 是(运行时解析值与令牌解析值等值,c3 有「硬编码会在此 FAIL」的对照断言;探针另有一条防恒真的令牌可区分判据) | ✓ FLOWING |
| `body` 的 `background` | computed `background-color` | `--color-surface-page` → `--radix-gray-3` | 是(c3 两条互为对照) | ✓ FLOWING |
| PAIR 清单 | `scripts/check-02-contrast.py` 的 54 条清单条目 | 源码里的 `/* PAIR */` 注释 → 运行时令牌解析 | 是(53 对 + 1 ORDER;登记值与运行时实测逐位一致) | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| -------- | ------- | ------ | ------ |
| 对比度门 | `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`(53 PASS + 1 ORDER) | ✓ PASS |
| 三个静态门 | `bash scripts/check-01/03/04-*.sh` | 三条全 `PASS` exit 0 | ✓ PASS |
| 卡片语言 c1/c2 | `.venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2` | exit 0;26 + 13 条断言,0 FAIL / 0 BLOCKED | ✓ PASS |
| 三层刻度 / 密度 / 滚动契约 c3/c4/c5 | `... --item c3 --item c4 --item c5` | exit 0;3 + 4 + 5 条断言,0 FAIL / 0 BLOCKED | ✓ PASS |
| 卡片边界色探针【新】 | `.venv/bin/python scripts/probe-card-border-token.py` | exit 0;5/5 卡片 `rgb(206,206,206)`,2/2 可读对照 `rgb(217,217,217)` | ✓ PASS |
| `check-05` 全量 | `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` | exit 2(按设计);十项 0 FAIL;BLOCKED 仅 item 5 两条 `--ai-smoke` 腿 | ✓ PASS(按设计非绿) |
| `check-06` / `check-07` | 各自直跑 | 各 exit 0,0 FAIL / 0 BLOCKED | ✓ PASS |
| `probe-05` / `probe-07` | 各自直跑 | 各 exit 0 | ✓ PASS |
| app.js 语法 | `node --check frontend/app.js` | exit 0 | ✓ PASS |
| pytest 基线 | `.venv/bin/python -m pytest backend/tests -q --tb=short` | `219 passed, 6 skipped` | ✓ PASS |
| 编辑纪律(追加不重排) | 相位基线 vs HEAD 顶层选择器序列 diff | 173 = 173,完全相同 | ✓ PASS |
| 截图尺寸(从 HEAD blob 直读) | `git cat-file -s HEAD:…/p*.png` + IHDR | 5/5 = `(1440, 900)`,字节数与盘上一致 | ✓ PASS |
| 截图产出机制【关键链】 | `.venv/bin/python scripts/check-09-idi09-validation.py --screenshot <tmpdir>` | exit 0;临时目录落盘 5 张 PNG,全部 1440x900,样本集合恰为 `{p1,p12,p3,checking,archive}` | ✓ PASS |
| 修正案的两条守卫可区分 | 直接跑 `c05.norm` 等值比较(旧值 vs 新值) | 严格不等 ⇒ 回退即 FAIL;探针令牌可区分 206 ≠ 217 | ✓ PASS |

### Probe Execution

| Probe | Command | Result | Status |
| ----- | ------- | ------ | ------ |
| `scripts/probe-card-border-token.py`【修正案新增】 | `.venv/bin/python scripts/probe-card-border-token.py` | EXIT=0;`PASS 令牌可区分` 1 行、`PASS 卡片边界` 5 行、`PASS 非卡片边界对照` 2 行、`INFO … 不存在` 2 行、`PROBE RESULT: PASS` | PASS |
| `scripts/probe-05-resolve-color.py` | `.venv/bin/python scripts/probe-05-resolve-color.py` | EXIT=0;`mutated-prefix-verdict=PASS` / `mutated-postfix-verdict=BLOCKED` / `control-verdict=PASS` —— 与 `gate-logs/probe-05-resolve-color.log` 逐字一致 | PASS |
| `scripts/probe-07-focus-composite.py` | `.venv/bin/python scripts/probe-07-focus-composite.py` | EXIT=0;`ring=(31,99,189) ground=rgb(255,255,255) alpha=0.75 composited=(87,138,206) ratio=3.54 (>= 3.0)`。地面已由 `--color-surface`(3.431)漂到卡片白 —— 这是**往更容易的方向**漂,SUMMARY 已写明,措辞未把它读成「仍证明 gray-2 上的算术」 | PASS |
| `scripts/check-09-idi09-validation.py` | `--item c1 … --item c5` | c1:26 / c2:13 / c3:3 / c4:4 / c5:5,0 FAIL 0 BLOCKED,exit=0 | PASS |
| `scripts/check-09-idi09-validation.py`(全量含出图) | `--screenshot /tmp/rev-shots-2` | exit=0;c1…c5 + `shot:7` 全 PASS,0 FAIL 0 BLOCKED;`shot` 断言「输出目录恰含 5 个 PNG」「样本清单一一对应」「每张 1440x900」全 PASS | PASS |
| `scripts/check-05-ui-uat.py` | `--browser bundled`(全量) | exit=2,十项 FAIL 计数全 0,BLOCKED 仅 item 5 两条 `--ai-smoke` 腿 | PASS(按设计非绿) |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
| ----------- | ----------- | ----------- | ------ | -------- |
| CARD-01 | 01, 03 | 左栏 4 个面板各自呈现为独立卡片(白底 + 可见边界 + 圆角,彼此间有明确间隙) | ✓ SATISFIED | c1 26 条读数(4 个 section 逐个)+ `gap == 12px` + 间隙透出页面底色;探针 5/5 边界色;5 张截图目视确认 |
| CARD-02 | 01, 03 | 右栏文档区呈现为独立卡片,与左栏同族(同底色 / 同边框语言 / 同圆角 / 同阴影) | ✓ SATISFIED | c2 13 条读数;两栏四条声明逐令牌相同(边界令牌在修正案后同为 `--color-border`);原 `border-left` 单边读感已由四边边界 + 卡片底色取代 |
| CARD-03 | 02, 03 | 页面底色下沉,与白卡片形成明确 elevation 层次 | ✓ SATISFIED | c3 `body == rgb(240,240,240)` + 令牌等值对照 + 亮度严格递增(我独立算术复算吻合);屏幕级 14 个 gray-2 载体与白卡片同帧共存 |
| VIS-01 | 01 | 卡片底色与阴影作为新令牌写入围栏 `:root`;围栏外零裸 `#hex`、零 tier-1 引用(check-01 绿) | ✓ SATISFIED | `style.css:334-335` 在围栏内;check-01 我重跑 `PASS` |
| VIS-02 | 01, 02 | 卡片圆角取自现有 `--radius-*` 刻度;阴影不参与布局(零位移) | ✓ SATISFIED | 半径刻度逐字未改、无新增半径值;修正案后两层阴影的 offset-x 均为 `0px`;卡片规则体无 `margin`/`position` 及九项禁令属性 |
| REG-01 | 01, 02 | 页面换值后 `check-02` 全部对比度对仍达标;受影响配对逐条重算并登记(不是刷新旧值) | ✓ SATISFIED | `PASS: 0 failures`;台账值经我的独立算术逐位复现(含两条重新归属到卡片底色的 4.77 / 3.32);零颜色值改动、零阈值放宽、53+1 清单规模不变。**此前报告曾指出该条的字面要求只有在页面值真正换掉后才完整成立 —— HEAD 上 `--color-surface-page` 已是 `var(--radix-gray-3)`、`body` 计算底色为 gray-3,故该条现在完整成立** |
| REG-02 | 03 | 五条 UI 门复跑无新增失败 —— 折叠 / 滚动容器收敛 / sticky 表头 / badge 流内机制 / 焦点环 / 24×24 命中区 / 窄窗口不破版全部保持 | ✓ SATISFIED | check-05 全量 0 FAIL;check-06 / check-07 / probe-05 / probe-07 全 exit 0(我在本进程重跑确认);四个静态门 + pytest 219/6 + `node --check` 全绿 |

**Orphaned requirements:** none —— REQUIREMENTS.md 映射到 Phase 9 的 7 个 ID(CARD-01..03 / VIS-01..02 / REG-01..02)全部出现在至少一份 PLAN 的 `requirements:` 中(CARD-01/02/03 见 01+03 与 02+03、VIS-01 见 01、VIS-02 见 01+02、REG-01 见 01+02、REG-02 见 03),且逐条有实现证据。无「映射到本阶段但无计划认领」的项。

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| ---- | ---- | ------- | -------- | ------ |
| (none) | — | 债务标记(`TBD`/`FIXME`/`XXX`) | — | 三个被修正案改动的文件(`style.css` / `check-09` / `probe-card-border-token.py`)零命中(grep exit 1) |
| (none) | — | 空实现 / 占位返回 / 硬编码空数据 | — | 卡片规则全部是真实令牌消费;`check-09` 期望侧写死字面量(防假绿),非占位;新探针是真实 `getComputedStyle` 读数,不写盘 |
| (none) | — | `!important;` 字面量进入注释 | — | 相位新增行中该字面量计数 = 0;check-04 我重跑 `PASS` |
| `frontend/style.css` | `#rounds-placeholder` 两处 | 字面 `PLACEHOLDER` 子串 | ℹ️ Info | 是元素 id(`#rounds-placeholder`),不是债务标记;grep 模式误命中,非缺陷 |

### Observations (non-blocking)

1. **开放项 2「卡片边界 / 阴影强度」已由用户裁定并落地。** Phase 9 的 plan 03 把「强度是否够」刻意 parked 为设计决策;用户 2026-09-26 裁定「稍微重一点」,quick `260926-vaf` 已把边界 gray-6→gray-7、阴影改两层值,我逐条复核为真(truths 4/5/15)。该开放项**处置完毕**;其感知层确认(`human_judgment: true`,D5)属用户的眼,已由 quick 的 coverage 登记,不是 Phase 9 的 must-have。
2. **其余三条开放项在 HEAD 仍为真实观察**(我本进程独立复现):`.overlay-card` 计算底色 `rgb(249,249,249)`(gray-2);首张左栏卡片与 `#doc-panel` 的 `top` 均为 `0`(顶到视口边缘,未加页面级留白);四个文本 input(`#project-path-input` / `#chat-input-row input` / `#enter-form input[type="text"]` / `#confirmation-modal input[type="text"]`)计算底色全 `rgb(255,255,255)`(不声明 `background`,画 UA 白填充)。三者均属后续候选的范围裁定,不在本阶段 must-have 内。
3. **`check-05` 的 item 2 INFO 诊断行仍陈旧(既有,非断言)。** 我本进程重跑的输出第 93 行仍打印「`--color-text-muted` … 在 `--color-surface-page` 上 5.77:1」,而 HEAD 的 `--color-surface-page` 已是 gray-3,该比值实为 **5.19**(我独立复算)。这**不是**断言(纯 `info()` 行,任何门都未因此假绿),且它由 quick `260925-iin` 写入时是对的(当时页面是 gray-1)。属本阶段页面换值顺带造成的文案陈旧,与 backlog 999.1 第 2 项同型;修正案未触碰该文件。
4. **修正案后 `--shadow-card` 的主层 alpha(0.08)超过 `--shadow-composer` 的主层(0.04),但仍远低于 `--shadow-overlay`(0.2 / 30px)。** 这是用户裁定「稍微重一点」的直接后果;没有任何 SC 把卡片阴影与兄弟令牌做数值约束,SC4 的可判部分(零位移、不参与布局)全部成立。**不改判据** —— 记录以供用户看图时参考。
5. **卡片边界令牌不在对比度清单内(相位前后一致)。** `--color-border` 与 `--color-border-subtle` 都没有 `/* PAIR */` 条目,故 check-02 不覆盖容器边界色。我实测边界色对其绘制面的比值:gray-7 在 gray-3 页面 **1.38**、在卡片白 **1.57**;修正案前的 gray-6 为 **1.24 / 1.41** ⇒ 修正案把容器边界**往更可见的方向**推,不是回归。这属本文件既有的容器边界语言(刻意低对比)与既有覆盖范围,**不是本阶段缺口**;修正案新增的探针覆盖的是「边界色取哪个令牌」这条缝(而非对比度)。
6. **`check-05 --item 8` 的 sticky 余量为零**(`1.000px` 对闭区间 `<= 1.0`),且它与 `#doc-panel` 的 1px 边界宽耦合。修正案只改边界**颜色**、未动宽度,故该读数与 `idi-09-03-SUMMARY` 登记的既有开放项逐字相同。属已登记的已知紧余量,非本次引入。
7. **`idi-09-03-SUMMARY.md` 对 SC3 屏幕级承载者的枚举不完整。** SUMMARY 写承载者是三个自带 `background: var(--color-surface)` 的 `<select>` 与 `.overlay-card`;我的探针实测同帧可见的 gray-2 载体还包括 `#btn-ping` / `#btn-abort`、`#ai-events`、`#latest-check`、`#selection-menu` 等(共 14 个)。**主张的实质(同帧共存 gray-2 与白卡片)成立且更强**,仅是枚举少于实际,不构成缺口。
8. **截图交付有两套,均已核对。** 相位 9 目录 5 张为修正案**前**,quick 目录 5 张为修正案**后**;两套都是 1440×900,同名文件的字节数全部不同 ⇒ 修正案确为渲染内容真变,而非仅源码文本变化。

### Human Verification Required

None. 本阶段全部 must-have 均以机器可判定的形式表述(真实浏览器 `getComputedStyle` 读数 / 对比度比值 / 门退出码 / PNG 尺寸 / 选择器序列),逐条已在代码库与渲染产物中验证;三份 PLAN 均为 `autonomous: true`,且**没有任何** `<verify><human-check>` 延迟项可收获(我 grep 了三个 PLAN,零命中)。视觉层的**主观**裁定(卡片边界与阴影强度是否够、是否加页面级留白、`.overlay-card` 是否改白、输入框是否该带 gray-2 内陷底)已由 plan 03 明确移交用户 —— 其中「强度」已由用户 2026-09-26 的裁定落地(见 Observations 1),其余三条属**后续候选的范围裁定**而非本阶段目标是否达成;我已独立复现这 4 项观察为真,故不计为需人工验证的未决项。

### Gaps Summary

**无缺口。** 五条 ROADMAP Success Criteria 逐条在代码库与渲染产物中成立,修正案**持有**而非削弱阶段目标:

- **SC1/SC2** —— 五个容器的卡片语言在真实浏览器里读得(白底 / 四边 1px solid / 10px 圆角 / 零位移阴影 / 12px 可见间隙),两栏取同一组令牌;修正案把两栏边界同时换到 `--color-border`,同族性**更强**(两栏边界令牌逐字相同);表头底色跟随且 sticky 遮挡保持。
- **SC3** —— `body` 为 gray-3、三档亮度严格递增,屏幕级 14 个 gray-2 载体与白卡片同帧共存;密度按 D-9-2 落地且未溢出裁定范围。
- **SC4(VIS-01/02)** —— 令牌全在围栏内、check-01 绿、圆角取自既有刻度、阴影两层**均**零位移。修正案的加重没有把阴影变成参与布局的东西,也没有引入任何禁令属性。
- **SC5(REG-01/02)** —— `check-02` 0 failures 且 8 条受影响配对以 HEAD 内容重算登记(我以独立算术逐位复核);五条浏览器门复跑零新增失败,零处门弱化,四静态门 + pytest 基线不降。**修正案未触碰对比度清单**(两个边界令牌都不在清单里),故 SC5 不受影响。

**修正案是否引入新缺口 —— 逐条核过,没有:** 阴影仍零位移(SC4 ✓);边界改动面严格是两处卡片,四处非卡片消费者一字未动(CARD-01/02 范围 ✓);对比度清单零改动(SC5 ✓);断言零删除、门语义零改动;新探针补上了一条此前零覆盖的缝且本身可红。

**Phase 10 重验是否引入新缺口 —— 逐条核过,没有。** 24 条 must-have 全部以 HEAD 内容重新推导,24/24 仍成立;`check-09` 的 c1…c5 在 HEAD 上复跑 `exit=0`、0 FAIL / 0 BLOCKED;四个静态门 + `check-02`(0 failures)+ pytest(219/6)+ `node --check` 全绿;`scripts/check-05-ui-uat.py` 零改动(`git diff` 为空)。两条被本阶段改动移动的历史读数(truth 5 的 `--color-border` 计数 3→2、truth 24 的顶层选择器计数 173→174)均由 Phase 10 自己的合规改动机械解释,主张的实质不受影响;`#round-doc` 的 −3px 不触及本报告任何判据。`gaps_closed` / `gaps_remaining` / `regressions` 三者皆空。

**四条开放项:** 「强度」已由用户裁定落地并复核(Observations 1);其余三条(`.overlay-card` 底色 / 页面级留白 / 输入框 UA 白填充)我逐条独立复现为真,属后续候选的范围裁定。

---

_Verified: 2026-09-27T12:33:32Z (re-verified against HEAD content; previous verification 2026-09-26T15:20:00Z)_
_Verifier: [CL] (gsd-verifier)_

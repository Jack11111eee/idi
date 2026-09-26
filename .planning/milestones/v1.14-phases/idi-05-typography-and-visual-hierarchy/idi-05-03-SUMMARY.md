---
phase: idi-05-typography-and-visual-hierarchy
plan: 03
subsystem: ui
tags: [css, design-tokens, active-panel-marker, svg-mask, data-uri, contrast, playwright, uat, visual-hierarchy, re-verification, idi-04.1]

# Dependency graph
requires:
  - phase: idi-05-typography-and-visual-hierarchy
    provides: "plan idi-05-01:7 档字号刻度、四宿主可达的 `.markdown-body` 标题、字重三档分工;plan idi-05-02:三段动作坡道、`#btn-authorize` 16px、VISUAL-03 复证与页面级层级链"
  - phase: idi-04.1-radix
    provides: "围栏 tier-1 Radix primitive 与 tier-2 语义令牌;check-02 的 `/* PAIR */` 清单机制;四条守卫命令;`--radix-blue-11` 的既有声明与消费"
provides:
  - "新 tier-2 令牌 `--color-marker-active: var(--radix-blue-11)`(诚实的名字,不复用 `--color-action-primary`;新增 tier-1 primitive = 0)"
  - "文件末尾两条追加规则:`#session-panel` / `#annotations-panel` / `#checks-panel` 的 `.panel-header` 3px inset 竖条 + 标题改用标记色,经 `:not(.hidden)` 读取既有显隐机制"
  - "围栏内两个 data-URI 令牌 `--icon-pin` / `--icon-location`(实心、12×12、恰 1 个 `<path>`、无 `fill`、**零颜色信息**)"
  - "`.annotation-quote::before` 与 `.verdict-location::before` 原地改写为 mask 盒模型(`mask-image` + `background-color: var(--color-text-secondary)`)"
  - "check-02 配对清单 45 → 47 对(35 TEXT + 12 NON-TEXT),两条新配对实测均 4.65"
  - "check-05 新增 `read_pseudo_style` / `check_active_marker` / `check_marker_control` / `check_mask_glyph`;item4 45 → 65 条断言,item_smoke 6 → 8,item6 2 → 6"
  - "D-05 连带义务:idi-04.1-radix 的四条守卫与三项人工验证项在 HEAD 上重跑,全部数值从 HEAD 重算"
affects: [idi-06, idi-07]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
# Same estimateTokens scale (chars/4 over the realized diff), never a harness token count.
actuals:
  tokens: 5140      # chars/4 over the realized diff of the two code files (20558 chars)
  tasks: 3
  commits: 2        # MEASURED: git rev-list --count 3a882de..HEAD (2 task commits; Task 3 is evidence-only, zero diff)
  plan_head_before: 3a882de

# Tech tracking
tech-stack:
  added: []        # 零新增依赖、零新增文件、零构建步骤(硬规则 6)
  patterns:
    - "机制优先于约定:mask 只看 alpha ⇒ data-URI 内零颜色信息 ⇒ 「跟文字色」由机制保证而非人工同步;这是撤掉契约字面量例外 L-3 的唯一依据"
    - "原地改写等价于追加的条件:选择器全文唯一且无竞争者时,改规则体与在末尾追加在层叠上等价,且不留被覆盖的死规则"
    - "对照组是单点断言的对偶:同一个读取器在活动面板上读到大值、在 `#ai-panel` / `#doc-panel-header` 上读到 `none`,这组差异本身就是读取器非空转的证明"
    - "复验的成因分类:covered_files 内容真变 ⇒ 重新验证并重算数值;漏项 ⇒ 补指纹。本阶段是前者"

key-files:
  created: []
  modified:
    - frontend/style.css
    - scripts/check-05-ui-uat.py

key-decisions:
  - "D-18 新开 `--color-marker-active` 而不复用 `--color-action-primary`:那个名字说的是「主要动作」,拿它做面板指示器会让名说谎(04.1 的 D-03 为同一条方法论付过代价)。颜色值不变(blue-11),只换承载它的令牌名 —— 60/30/10 的 Accent 域偏离已登记(A-7)"
  - "D-17 竖条用 `box-shadow: inset 3px 0 0` 而非 `border-left`(零布局位移),且落在 `.panel-header` 而非 `<section>`(三个 section 的子元素都带背景色,会盖住左边缘的竖条)。标题只改 `color`,不改 `font-weight`(D-09 已统一 500;flex 行改字重会移动徽标)"
  - "3px 是 `box-shadow` 的偏移分量,不是 `--space-*` 刻度值 —— L-1…L-5 从未覆盖 box-shadow,冻结轮的 `inset 3px 0 0` 已是既有先例。该理由已写进围栏外注释,以免被读成刻度外字面量"
  - "D-20/D-21/D-22 用 `mask-image` + `background-color` 而非契约的 `content: url(data-URI)`:后者经 `content` 渲染为图片、不继承页面 CSS、`currentColor` 不可用,只能把 fill 钉死为转义 hex —— 那让「跟文字色」成为人工同步的约定"
  - "两个 `--icon-*` 的 `<path>` 不带 `fill`、data-URI 内零 `%23` / `#` / `fill=`,由 Gate 5 机械钉死"
  - "图标不新增对比度配对:两个落地面已被既有 TEXT 配对覆盖(5.62 / 5.82),TEXT 阈值(4.5)严于 NON-TEXT(3.0),再加是**同义反复** —— 这是刻意的零新增"
  - "D-23 `.collapse-indicator` 零触碰(app.js 用 `textContent` 赋值,内联 `<svg>` 会被静默擦掉);mask 方案顺带消解 Pitfall 7 的第二半 —— 本阶段 DOM 里没有任何内联 `<svg>`"
  - "D-05 复验走**重新验证**而非补指纹:本次 stale 的成因是内容真变(本阶段重写了 04.1 覆盖的两个文件)。指纹写回留给编排器的 `/gsd-verify-work idi-04.1-radix`"

patterns-established:
  - "新令牌与其首个消费者同一次提交落地(Hard Rule 5):`--color-marker-active` / `--icon-pin` / `--icon-location` 三者均在各自的任务提交内声明并消费,无孤儿令牌"
  - "「名说谎」是本项目的一条可复现的失败类:04.1 的 D-03(26 个 primitive 改名)与本阶段的 D-18 是同一条方法论的两次应用"

requirements-completed: [VISUAL-04, VISUAL-05]

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "侧栏当前活动面板可辨认:3px 蓝竖条 + 标题变色。p1 → `#session-panel`、p3 → `#annotations-panel`、checking → `#checks-panel` 三态实读;`#ai-panel .panel-header` 与 `#doc-panel-header` 作为对照组必须保持 `box-shadow: none`"
    requirement: "VISUAL-04"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 4"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item smoke"
        status: pass
      - kind: unit
        ref: ".venv/bin/python scripts/check-02-contrast.py (47 pairs, both new pairs 4.65)"
        status: pass
    human_judgment: true
    rationale: "标记的**可见性**(竖条不被面板标题行内的元素盖住、不因 `border-radius` 在角落断开、标题变长时仍贴左缘)是计算样式看不见的渲染几何,已作为 E4/E5 的 backstop 陈述记录,不自动判过"
  - id: D2
    description: "两处写死的 emoji 变为跟随令牌的掩码字形:12×12、`--color-text-secondary` 上色、`mask-image` 接上围栏令牌;`.annotation-quote::before` 与 `.verdict-location::before` 各仍只出现 1 次"
    requirement: "VISUAL-05"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 4,6"
        status: pass
      - kind: other
        ref: "Gate 5: grep -oE '%23[0-9a-fA-F]{3,8}' → 0; grep -oE \"fill='\" → 0"
        status: pass
      - kind: other
        ref: "ls frontend/vendor/ → marked.min.js only; git diff --stat -- frontend/app.js frontend/index.html → 空"
        status: pass
    human_judgment: true
    rationale: "两个 12px 字形与相邻文字的**基线视觉对齐**、以及不撑高行盒,计算样式看不见,只能看渲染结果(05-N-5),已作为 E6/E7 的 backstop 陈述记录"
  - id: D3
    description: "D-05 连带义务:idi-04.1-radix 的四条守卫与三项 `human_verification` 在 HEAD 上重跑,全部数值从 HEAD 重算;tier-1 25 不变、tier-2 47 → 48、清单 43 → 47 的差值已登记;04.1 的报告文件零改动"
    requirement: "VISUAL-04, VISUAL-05"
    verification:
      - kind: integration
        ref: "bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh"
        status: pass
      - kind: integration
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 1,2,3,4,6 (全 PASS,0 FAIL / 0 BLOCKED)"
        status: pass
      - kind: other
        ref: "git status --porcelain -- .planning/phases/idi-04.1-radix/ → 空"
        status: pass
    human_judgment: false

duration: ~45min
completed: 2026-09-21
status: complete
---

# Phase 5: 排版与视觉层级 — Plan 03 Summary

**侧栏当前活动面板由 3px 蓝竖条 + 标题变色标出(纯 CSS `:not(.hidden)` 推导,`app.js` 零 diff),两处写死的 emoji 换成跟随令牌的 12px 掩码字形(data-URI 内零颜色信息);D-05 的连带义务履行完毕,`idi-04.1-radix` 的三处结论逐条从 HEAD 重算。**

## Performance
- **Duration:** ~45min
- **Tasks:** 3/3(Task 3 为证据类任务,零 diff)
- **Files modified:** 2

## Accomplishments
- **活动面板标记(VISUAL-04)。** 新开一个诚实命名的 tier-2 令牌 `--color-marker-active: var(--radix-blue-11)`,配两条追加在文件末尾的规则:活动面板的 `.panel-header` 得一条 3px inset 蓝竖条,其 `h2` 改用标记色。实现用 `box-shadow: inset`(零布局位移)而非 `border-left`;竖条落在 `.panel-header` 而非 `<section>`(section 的子元素都带背景色,会盖住左边缘的 inset 竖条)。`:not(.hidden)` 只**读取**既有的显隐机制,`.hidden` 规则本身零改动。`#ai-panel` 从不被 `.hidden`,不参与三选一推导,其可辨状态仍是既有的折叠指示器 —— 这是 D-16 对契约措辞的收窄(「三选一活动态 + AI 面板折叠态」),已登记。
- **`#ai-panel` 与 `#doc-panel-header` 对照组。** 三个样本(p1 / p3 / checking)下各断言一次:活动面板的 `box-shadow` 解析为 `inset 3px 0 0 <marker>`,`#ai-panel .panel-header` 与 `#doc-panel-header` 必须是 `none`。这组差异同时是读取器非空转的证明 —— 同一个读取器在不同元素上读出不同的值。
- **两处 emoji → 掩码字形(VISUAL-05)。** 围栏内新增两个手写 SVG data-URI 令牌,`<path>` 不带 `fill`、data-URI 内零颜色信息;两处伪元素规则**原地改写**为 mask 盒模型(`content: ''` + `display: inline-block` + 显式 12×12 + `margin-right: var(--space-1)` + `vertical-align: -2px` + `background-color: var(--color-text-secondary)` + 成对的 `-webkit-mask-*` / `mask-*`)。mask 只看 alpha,故契约的字面量例外 **L-3 可以整个撤掉**,由 Gate 5 机械钉死。
- **check-02 清单 45 → 47 对。** 新增 `--color-marker-active ON --color-surface-page` 的 TEXT(SC 1.4.5)与 NON-TEXT(SC 1.4.11)各一条,实测均 **4.65** —— 本阶段最薄的余量(0.15),不得为「更保险」而换步。图标不新增配对(TEXT 通过蕴含 NON-TEXT 通过,再加是同义反复)。
- **D-05 连带义务履行完毕。** `frontend/style.css` 与 `scripts/check-05-ui-uat.py` 都在 `idi-04.1-radix` 的 `covered_files` 里,本阶段的编辑使其 `passed` 指纹 stale。成因是**内容真变**,故走**重新验证**:四条守卫重跑全绿,04.1 的三处结论逐条从 HEAD 重算并逐字不变,三处数量差值已登记。**04.1 的报告文件零改动** —— 指纹写回由编排器的 `/gsd-verify-work idi-04.1-radix` 完成。

## Task Commits
1. **Task 1 (tracer): 活动面板标记端到端** - `afa8c0c`
2. **Task 2: 两处 emoji → 内联掩码字形** - `b90594c`
3. **Task 3: D-05 连带义务 —— 复验 `idi-04.1-radix`** - 无提交(证据类任务,`<action>` 明写「本任务不改 `frontend/style.css`,也不改任何断言逻辑」;`git status --short` 在该任务前后均为空)

## Files Created/Modified
- `frontend/style.css` — 围栏内新增 3 条声明(`--color-marker-active` / `--icon-pin` / `--icon-location`)、清单新增 2 条 PAIR;文件末尾追加 2 条活动态标记规则(含承重决定注释);`.annotation-quote::before` 与 `.verdict-location::before` 原地改写为 mask 盒模型。**围栏外的既有规则零改动、零重排**。
- `scripts/check-05-ui-uat.py` — 新增 `read_pseudo_style` 读取器、`check_active_marker` / `check_marker_control` / `check_mask_glyph` 三个断言函数;item4 新增 VISUAL-04 三态 + 对照组 12 条与 `.verdict-location::before` 探针 4 条;item6 新增 `.annotation-quote::before` 4 条;item_smoke 新增 2 条。

## Decisions & Deviations

**决策(均已登记在 `05-CONTEXT.md` / `idi-05-UI-SPEC.md`):** D-16 范围收窄为「三选一活动态 + AI 面板折叠态」;D-17 形态与四条承重决定;D-18 新开 `--color-marker-active`(不复用 `--color-action-primary`),蓝色、blue-11、60/30/10 偏离登记 A-7;D-20/D-21/D-22 mask 机制、字形路径与用色对齐;D-23 `.collapse-indicator` 零触碰。

**偏差一(计划文本缺陷,已在执行期按意图纠正):** 计划 Task 1 与 Task 3 的两条 `<verify>` 用了 `grep '^PASS  4.65  --color-marker-active ON --color-surface-page'` 与 `grep '^PASS  4.53  --color-text-info ON --color-surface-info'` —— 大写 `ON`。而 `scripts/check-02-contrast.py:192` 的标签格式是 `"%s on %s" % (fg_name, bg_name)`,输出**恒为小写 `on`**。两条命令的字面形态恒返回 0,按计划的 `<fails_when>` 会假报失败。**盘的实况**:小写形态分别返回 `2`(TEXT + NON-TEXT 各一,正是计划意图的「one TEXT, one NON-TEXT」)与 `1`(04.1 的 0.03 余量对逐字不变)。按 D-01(磁盘 HEAD 是唯一基线)取小写形态判定,并把该缺陷登记在此。

**偏差二(计划文本缺陷,同上):** 计划 Task 2 的 `<verify>` 用 `grep -o 'mask-image: var(--icon-pin);' ... | wc -l`,期望 `1`。但 `-webkit-mask-image: var(--icon-pin);` **包含**该子串,故实测为 `2`。而计划自己在同一步骤里**要求**同时书写前缀与无前缀两种形态 —— 该 `<verify>` 与自己的 `<action>` 互相矛盾。**盘的实况**:锚定行首的 `grep -cE '^[[:space:]]*mask-image: var\(--icon-pin\);'` 返回 `1`,`-location` 同为 `1`,即「每个令牌恰有一个 mask-image 消费者」的计划意图成立。

**偏差三(登记):** 计划 03 的 `<read_first>` 与 `<action>` 中的行号全部是**规划期 HEAD** 的引用,而 wave 1 与 wave 2 都修改过本计划触碰的两个文件(`check-05` item4 已由 27 长到 49 条断言)。所有编辑目标按内容重新定位、按 D-01 以磁盘 HEAD 为准;未发现计划描述与磁盘实况的**实质**冲突(两处偏差均为命令字面形态,不是内容分歧)。

**观察项(不在本计划范围,未改动):** `frontend/style.css` 围栏清单头注释(现 L332-336 附近)仍写着「Manifest size across three value layers (D-15): 24 / 34 / 43」并称「this rewrite re-enumerates 43 pairs」。该注释是**历史层记录**,但在 wave 1+2(43 → 45)与本计划(45 → 47)之后,清单实际规模已是 47。**本计划未改它** —— 它是 wave 1/2 引入的既有状态,不属本计划的 `<action>`,且改动围栏注释不在计划的授权范围内。留给 verifier 裁定是否需要登记该注释为第 4 个值层。

**未改动的四件事(有意为之):** `frontend/app.js` / `frontend/index.html` / `frontend/vendor/` 零 diff;`.collapse-indicator` 零触碰(逐字节与 HEAD 相同,见下);`REQUIREMENTS.md` / `ROADMAP.md` 零 diff;`scripts/check-02-contrast.py` 代码零改动。

## Verification (全部 `<verify>` 命令的原始输出)

```
=== Task 1 ===
$ bash scripts/check-01-token-conformance.sh
PASS                                                       (exit 0)

$ python3 scripts/check-02-contrast.py | tail -1
PASS: 0 failures

$ python3 scripts/check-02-contrast.py | grep '^PASS  ' | wc -l
47

$ python3 scripts/check-02-contrast.py | grep '^PASS  4.65  --color-marker-active on --color-surface-page' | wc -l
2        ← 计划字面用大写 ON,恒为 0;按盘实况(小写 on)判定,见偏差一

$ grep -o -- '--color-marker-active: var(--radix-blue-11);' frontend/style.css | wc -l
1

$ grep -o 'box-shadow: inset 3px 0 0 var(--color-marker-active);' frontend/style.css | wc -l
1

$ grep -o 'panel:not(.hidden) .panel-header' frontend/style.css | wc -l
6

$ bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh
PASS
PASS

$ grep -o '@media' frontend/style.css | wc -l
0

$ grep -oE '^[[:space:]]*--(white|radix-[a-z]+-[0-9]+):' frontend/style.css | wc -l
25
$ grep -oE '^[[:space:]]*--color-[a-z0-9-]+:' frontend/style.css | wc -l
48
$ grep -o '/\* PAIR' frontend/style.css | wc -l
47
$ grep -o '/\* ORDER' frontend/style.css | wc -l
1
$ grep -n -A 12 'panel:not(.hidden) .panel-header' frontend/style.css | grep -o 'border-left' | wc -l
0

$ .venv/bin/python scripts/check-05-ui-uat.py --item smoke,4
item smoke: PASS  (8 条断言,0 FAIL,0 BLOCKED)
item 4: PASS  (61 条断言,0 FAIL,0 BLOCKED)
exit=0

=== Task 2 ===
$ grep -oE '%23[0-9a-fA-F]{3,8}' frontend/style.css | wc -l
0
$ grep -oE "fill='" frontend/style.css | wc -l
0

$ grep -cE '^[[:space:]]*mask-image: var\(--icon-pin\);' frontend/style.css ; \
  grep -cE '^[[:space:]]*mask-image: var\(--icon-location\);' frontend/style.css
1
1        ← 计划字面 `grep -o 'mask-image: ...'` 因 -webkit- 前缀含同一子串而返回 2,见偏差二

$ grep -o "content: '';" frontend/style.css | wc -l
2

$ grep -o '.collapse-indicator { font-size: 20px; line-height: 1; }' frontend/style.css | wc -l
1        ← Gate 6

$ bash scripts/check-01-token-conformance.sh
PASS
$ python3 scripts/check-02-contrast.py | tail -1
PASS: 0 failures
$ python3 scripts/check-02-contrast.py | grep '^PASS  ' | wc -l
47

$ .venv/bin/python scripts/check-05-ui-uat.py --item 4,6,smoke
item 4: PASS  (65 条断言,0 FAIL,0 BLOCKED)
item 6: PASS  (6 条断言,0 FAIL,0 BLOCKED)
item smoke: PASS  (8 条断言,0 FAIL,0 BLOCKED)
exit=0

$ git diff --stat -- frontend/app.js frontend/index.html
(空)
$ ls frontend/vendor/
marked.min.js

$ 成对冗余声明(每条各 2:无前缀 + -webkit- 前缀)
mask-image=2/-webkit-mask-image=2  mask-size=2/-webkit-mask-size=2
mask-repeat=2/-webkit-mask-repeat=2  mask-position=2/-webkit-mask-position=2
$ grep -c 'margin-right: var(--space-1);' frontend/style.css
2
$ grep -c '^\.annotation-quote::before' frontend/style.css ; grep -c '^\.verdict-location::before' frontend/style.css
1
1

=== Task 3(D-05 连带义务,全部从 HEAD 重算)===
$ bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh
PASS
PASS
PASS

$ python3 scripts/check-02-contrast.py | tail -1
PASS: 0 failures                                    (exit 0)

$ python3 scripts/check-02-contrast.py | grep '^ORDER 0.363' | wc -l
1        ← 04.1 的序关系断言逐字不变

$ python3 scripts/check-02-contrast.py | grep '^PASS  4.53  --color-text-info on --color-surface-info' | wc -l
1        ← 04.1 的 0.03 余量对逐字不变(计划字面用大写 ON,见偏差一)

$ python3 scripts/check-02-contrast.py | grep 'color-border-strong'
PASS  3.24  --color-border-strong on --color-surface-page
PASS  3.15  --color-border-strong on --color-surface

$ python3 scripts/check-02-contrast.py | grep -E '^PASS  3\.(24|15)  --color-border-strong on --color-surface' | wc -l
2

$ .venv/bin/python scripts/check-05-ui-uat.py --item 1,2,3,4,6
item 1: PASS  (45 条断言,0 FAIL,0 BLOCKED)
item 2: PASS  (5 条断言,0 FAIL,0 BLOCKED)
item 3: PASS  (17 条断言,0 FAIL,0 BLOCKED)
item 4: PASS  (65 条断言,0 FAIL,0 BLOCKED)
item 6: PASS  (6 条断言,0 FAIL,0 BLOCKED)
exit=0
  冻结轮证据(item2,重复两次):opacity=1 / filter=saturate(0.6) /
  box-shadow=rgb(79, 52, 34) 3px 0px 0px 0px inset(== --color-action-warning)

$ grep -oE '^[[:space:]]*--(white|radix-[a-z]+-[0-9]+):' frontend/style.css | wc -l ; \
  grep -oE '^[[:space:]]*--color-[a-z0-9-]+:' frontend/style.css | wc -l
25
48

$ git status --porcelain -- .planning/phases/idi-04.1-radix/
(空)
```

## D-05 复验记录 —— `idi-04.1-radix` 逐条核对(全部数值从 HEAD 重算)

**指纹的义务归属。** `idi-04.1-radix` 的 `covered_digest`(`v1:sha256:25d5f1fe…`)因其两个 `covered_files`(`frontend/style.css`、`scripts/check-05-ui-uat.py`)被本阶段改写而 **stale**。成因是**内容真变**,故走**重新验证**而非补指纹。**指纹的重新写回由编排器执行 `/gsd-verify-work idi-04.1-radix`** —— 本计划提供它的输入(下表)。**本计划未改写 `idi-04.1-VERIFICATION.md` 的 frontmatter**(`git status --porcelain -- .planning/phases/idi-04.1-radix/` 为空),以保住「谁改了什么」的可追溯性。

**四条守卫:** CHECK-01 `PASS` / CHECK-02 `PASS: 0 failures` / CHECK-03 `PASS` / CHECK-04 `PASS`。

**三项 `human_verification`:**

| # | 项 | 本次复验结论 |
|---|---|---|
| ① | `## UI Considerations` 的 28 条 backstop 陈述(视觉/几何行为;其中 7 条含 CHECK-02 比值半边) | **照实记录其状态,不静默转绿。** 7 条含比值半边的陈述其比值半边由 check-02 在 HEAD 上重跑覆盖(清单 47 对全 PASS);其余裁切/换行/滚动归属/200% 缩放/菜单重定位等**渲染几何**行为无自动化证据,仍是人工项。本阶段新增的 2 对配对(4.65 ×2)已并入该证据面 |
| ② | `--color-text ON --color-surface-mark` 的比值(该对**不在**围栏清单,check-02 看不见) | **15.00**(用 `check-02` 同一模型独立算出:`--color-text` = gray-12 = `#202020`,`--color-surface-mark` = amber-3 = `#fff7c2`,ratio = 15.0017)。与 04.1 报告记载的 15.0:1 **一致** —— 本阶段未触碰这两个令牌 |
| ③ | TOKEN-07 的「断言序关系」半场 | **照实记录:仍是 manual-only,状态未变。** 复核确认代码库里仍**没有任何脚本**比较四个 `--z-*` 的值:`check-05` 断言的是「元素 `z-index` **等于**其令牌」(D-14 接线形式),不是令牌之间的大小序。`idi-04.1-VALIDATION.md:19/55/95` 已逐字记录这是**用户裁定的 manual-only 处置**(`nyquist_compliant: false`),故本复验**不单方面翻转**它 |

**三处 04.1 结论 + 数量差值(逐条从 HEAD 重算):**

| 项 | 04.1 的值 | HEAD 重算值 | 判定 |
|---|---|---|---|
| 清单规模 + `ORDER` | 43 对 + `ORDER 0.363` | **47 对 + `ORDER 0.363`** | `ORDER` **逐字不变**(两个操作数 `--color-text-muted` / `--color-text` 本阶段未改值);规模 43 → **47** 已登记 |
| `--color-text-info ON --color-surface-info` | 4.53(0.03 余量) | **4.53** | **逐字不变**,未触碰 |
| 冻结轮 `opacity` / `filter` / `box-shadow` | 1 / `saturate(0.6)` / `inset 3px 0 0 --color-action-warning` | **1 / `saturate(0.6)` / `rgb(79, 52, 34) 3px 0px 0px 0px inset`** | **逐字不变**(本阶段新增的活动态竖条是**另一个元素**上的同形声明);`--item 2` 仍 `PASS` |
| `--color-border-strong` 两行 | 3.24 / 3.15 | **3.24 / 3.15** | **逐字不变**,未触碰 |
| tier-1 primitive 数 | 25 | **25** | 不变(本阶段新增 primitive = **0**;blue-11 是既有声明) |
| tier-2 `--color-*` 名数 | 47 | **48** | +1(`--color-marker-active`)。**这是 04.1 的 `## Color` 节里「47 个 tier-2」这句在本阶段之后不再成立之处** —— 按计划要求**不改 04.1 的文件**(改它会作废它自己的其余结论),只在此登记 |
| D-15 `--color-action-irreversible*` 单消费者不变量 | 恰 1 个消费者 | **恰 1 个消费者** | 围栏外消费者仍恰 3 行,全在 `#btn-authorize` 规则体内(`style.css:1049-1051`),未变 |

**item 5 的处置:** 计划 Task 3 的 `<verify>` 不含第 5 项。本次顺带跑了 `--item 5`(不带 `--ai-smoke`)以补证据面:9 条断言 / 0 FAIL / **2 BLOCKED**,且两条 BLOCKED **恰为**需真实 AI 调用的交互冒烟(「处理本轮批注」/「发送」)。这与 `idi-04.1-03-SUMMARY.md:204` 逐字记录的形态相同(「不带 `--ai-smoke` 时 0 BLOCKED 不可达」),是 harness 的刻意设计而非回归。两条冒烟的 `--ai-smoke` 证据沿用 `260919-0h3-SUMMARY.md:173-174/262-268` 已记录的 PASS,本计划未重跑(会产生真实 AI 调用与计费)。

## Self-Check: PASSED

创建的文件与提交均已核对存在:
- `frontend/style.css` — FOUND(HEAD `b90594c`)
- `scripts/check-05-ui-uat.py` — FOUND(HEAD `b90594c`)
- 提交 `afa8c0c` — FOUND
- 提交 `b90594c` — FOUND
- `.planning/phases/idi-04.1-radix/` — 零改动(CONFIRMED,`git status --porcelain` 为空)
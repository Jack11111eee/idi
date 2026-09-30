---
phase: 260924-vb7-fix-the-tier-success-path-focus-loss-cho
plan: 01
subsystem: ui
tags: [a11y, focus-management, keyboard, playwright, nyquist-gate, tier-modal, guard-first]

# Dependency graph
requires:
  - phase: idi-08-accessibility-semantics-and-keyboard
    provides: "D-11 的 Escape 分派器 + D-14 的 syncBackgroundInert() 单点派生 + F1-d 的 Escape 分支交还(g1 已覆盖的那条路径)"
provides:
  - "chooseTier() 成功路径的焦点交还:选档后 document.activeElement 是 #btn-continue-check,不再是 <body>(F1)"
  - "check-07 item g4:真实 tier 选档路径上的行为守卫 + 判别控制(修复前后可区分)"
  - "D8-10 与 §焦点契约 情形① 的豁免收窄:只覆盖 #confirmation-modal 的放行路径"
affects: [idi-08-verification, any-future-phase-touching-chooseTier, focus-contract-F1]

# Actuals (#2632) — pairs with the plan's `estimate` (45000 tokens / 3 tasks) to calibrate.
# Same estimateTokens scale (chars/4 over the realized diff), never a harness token count.
actuals:
  tokens: 3654      # chars/4 over 14614 chars of realized diff (3 files)
  tasks: 3
  commits: 3        # MEASURED: git rev-list --count 23ca439..HEAD
plan_head_before: 23ca439bbf9bdb9916873e03af69cb40bf9e1ece

tech-stack:
  added: []          # 零新增依赖、零构建步骤(硬规则 6)
  patterns:
    - "守卫先行:先写行为断言并看它 RED,再动生产代码(本 quick 的全部价值所在)"
    - "判别控制:把待修的那一行变成 no-op,同一条真实路径必须回落到缺陷态"

key-files:
  created: []
  modified:
    - "frontend/app.js — chooseTier() 在 await refreshChecksAfterStream() 之后加 1 行交还 + 4 行围栏注释"
    - "scripts/check-07-idi08-validation.py — 新增 item g4(注册进 ITEMS)+ 文件头映射改为四条"
    - ".planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-UI-SPEC.md — D8-10 行 + §焦点契约 情形①(+6/−4)"

key-decisions:
  - "交还位置固定在 `await refreshChecksAfterStream();` **之后**:是这次刷新把 #btn-continue-check 的 disabled 复位为 false,而 Chrome 下 .focus() 对禁用按钮是 no-op —— 提前放会静默什么都不做,缺陷照旧存活而 diff 看上去是对的(比原缺陷更坏)"
  - "注释里不出现字面量 continueCheckBtn.focus():计划级计数门 grep -c 'continueCheckBtn.focus()' 按子串计数,注释散文同样计入 ⇒ 出现即把计数顶成 3。用散文指代(「上面那次刷新」「把焦点交还给下一个动作」)"
  - "判别控制必须先 page.reload():模块级 tierModalShown 在第一次进入项目后仍为 true,不 reload 时第二个项目的档位弹窗根本不会自动打开,控制会退化成空转"
  - "harness 在交还时刻**实测** disabled/rects,为禁用或不可见时记 BLOCKED 而非放行 —— 一个 no-op 的 .focus() 不得看起来像修好了"
  - "不改写 idi-08-02-PLAN.md / idi-08-02-SUMMARY.md 的旧计数 1:它们是「当时验证了什么」的历史记录;变化登记在本 SUMMARY"

# 计划的 requirements 数组另含 D8-10,但那是决策 id、不是 REQUIREMENTS.md 的行,故不列入本字段
requirements-completed: [A11Y-05, A11Y-06]

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "选档成功后焦点交还 #btn-continue-check(不再是 <body>)"
    requirement: "A11Y-05"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-07-idi08-validation.py --item g4 → PASS g4 选档成功后焦点交还 #btn-continue-check(F1-d 成功路径): expected=btn-continue-check actual=btn-continue-check"
        status: pass
      - kind: automated_ui
        ref: "同命令的判别控制 → PASS g4 判别控制:…: expected=active != btn-continue-check actual=BODY"
        status: pass
    human_judgment: false
  - id: D2
    description: "守卫真的会红:修复前同一条断言的读数是 actual=BODY"
    requirement: "A11Y-05"
    verification:
      - kind: automated_ui
        ref: "/tmp/vb7-red.txt → FAIL g4 选档成功后焦点交还 #btn-continue-check(F1-d 成功路径): expected=btn-continue-check actual=BODY(exit=1)"
        status: pass
    human_judgment: false
  - id: D3
    description: "D8-10 的豁免收窄为只覆盖 #confirmation-modal 的放行路径;情形① 保留并补 tier 的反例说明"
    requirement: "D8-10"
    verification:
      - kind: other
        ref: "git diff --numstat -- .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-UI-SPEC.md → 6/4,单文件;grep -c '选档成功路径交还' == 1;grep -c '只覆盖' == 2"
        status: pass
    human_judgment: true
    rationale: "账本措辞是否忠实反映契约,须由复验(/gsd-verify-work idi-08)与人判读;机器只能核对作用域与行数"

duration: ~14min
completed: 2026-09-24
status: complete
---

# Quick 260924-vb7: 档位选档成功路径的焦点交还(F1-d)Summary

**`chooseTier()` 选档成功后把焦点交还 `#btn-continue-check`(此前 `document.activeElement` 回落到 `<body>`),并把它落成 check-07 的一条**行为**守卫 —— 该守卫在修复前实测 RED(`actual=BODY`),修复后 GREEN,判别控制证明绿非恒绿。**

## Performance

- **Duration:** ~14 min(22:48 → 23:02 +08:00)
- **Started:** 2026-09-24T22:48+08:00
- **Completed:** 2026-09-24T23:02+08:00
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments

1. **缺陷修掉(实测,不是推断)。** `scripts/ui-states/archive` 派生的 `phase5_awaiting_tier` 样本上真实点击 `#btn-tier-loose`(真实 `POST /api/checks/tier` → 200),`document.activeElement` 由 `<body>` 变为 `btn-continue-check`。
2. **守卫先红后绿,留证。** RED(`/tmp/vb7-red.txt`,exit=1)与 GREEN(`/tmp/vb7-green.txt`,exit=0)各留一份,主断言行逐字如下 —— 这是「源码里含 `.focus()`」与「行为上真的移焦」的区分手段,也正是本缺陷第一次溜过去的原因。
3. **判别控制成立。** 把 `#btn-continue-check` 实例的 `focus` 方法置空后,同一条真实路径的 `activeElement` 回落 `BODY` ⇒ 实例 1 的绿不是恒绿。
4. **账本与代码一致。** D8-10 的豁免由「成功路径不交还」收窄为**只覆盖 `#confirmation-modal` 的放行路径**;§焦点契约 情形① 收窄并补 tier 的反例说明(情形① 本身保留 —— 它在 confirmation 弹窗上是对的)。
5. **零回归。** Escape 分支的既有 F1-d 交还(g1,21 条断言)、g2(39 条)、g3(10 条)全 PASS;pytest 219 passed / 6 skipped;check-01/02/03/04 PASS;check-05 9/10(item 5 的 2 条 AI-smoke 腿按设计 BLOCKED)。

## RED → GREEN 留证(逐字)

**RED(`/tmp/vb7-red.txt`,修复前,exit=1):**

```
FAIL g4 选档成功后焦点交还 #btn-continue-check(F1-d 成功路径): expected=btn-continue-check actual=BODY
PASS g4 判别控制:交还调用被置空后焦点不再落在 #btn-continue-check(证明实例 1 的绿非恒绿): expected=active != btn-continue-check actual=BODY
item g4: FAIL  (3 条断言,1 FAIL,0 BLOCKED)
```

**GREEN(`/tmp/vb7-green.txt`,修复后,exit=0):**

```
PASS g4 选档成功后焦点交还 #btn-continue-check(F1-d 成功路径): expected=btn-continue-check actual=btn-continue-check
PASS g4 判别控制:交还调用被置空后焦点不再落在 #btn-continue-check(证明实例 1 的绿非恒绿): expected=active != btn-continue-check actual=BODY
item g4: PASS  (3 条断言,0 FAIL,0 BLOCKED)
item g1: PASS  (21 条断言,0 FAIL,0 BLOCKED)
exit=0
```

**RED 状态下实测到的两条前提都成立**(故那次 FAIL 不是前提不成立造成的假红):`INFO g4 缺陷前提:点击前焦点在弹窗内: btn-tier-loose`,且 `PASS g4 实例 1/2 选档后 #tier-modal 已隐藏` —— 交还时刻该按钮 `disabled=false`、`rects>0`(规划期的实测事实 3 由本次 RED 运行独立复核;若为禁用,harness 会记 BLOCKED 而不是放行)。

## Task Commits

1. **Task 1: 先写守卫并看它红(扩 check-07 加 item g4)** - `5fcc7dd` (test)
2. **Task 2: 在 `chooseTier()` 的成功路径交还焦点(放在 refresh 之后)** - `40e8de9` (fix)
3. **Task 3: 收窄账本(D8-10 行 + 情形①)** - `f483eef` (docs)

**Plan metadata:** 未由本执行器提交 —— 按派发约束,SUMMARY / STATE 的 docs 提交由编排器负责。

## Files Created/Modified

- `frontend/app.js` (+5/−0) — `chooseTier()`:`await refreshChecksAfterStream();` 之后加 `continueCheckBtn.focus();` 与 4 行围栏注释(说明为什么必须在这个 await 之后、以及 D8-10 的豁免已收窄)
- `scripts/check-07-idi08-validation.py` (+101/−5) — 新增 `_active_id()` / `_g4_enter_and_choose()` / `g4()`,注册进 `ITEMS`,`--item` 帮助文本与文件头映射(三条 → 四条)同步更新
- `.planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-UI-SPEC.md` (+6/−4) — 只改两处:D8-10 行、§焦点契约 情形①

## 两条必须登记的账(本任务的实质产出)

### 1. 计数门变化:`grep -c 'continueCheckBtn.focus()' frontend/app.js` 由 **1 → 2**

- **旧门的措辞**:`idi-08-02-PLAN.md:353/420` 写 `== 1`,理由是「交还只在 Escape 分支里、不在关闭函数里」。该理由的**实质判据**(「交还逻辑不出现在关闭函数里」)仍然成立且更有价值;**失真的只是那个数字**。
- **新计数 2 的两处**:一行在 Escape 分派器(既有的 F1-d),一行在 `chooseTier()` 的成功路径(本次新增)。
- **判据改写(登记,不改写历史文件)**:判据为「**交还逻辑不出现在关闭函数(`closeConfirmModal()`)里**」,而非某个数字。**未改** `idi-08-02-PLAN.md` / `idi-08-02-SUMMARY.md` —— 它们是「当时验证了什么」的历史记录,改写会让记录失真(与 `[Phase 08]` 的「注释散文计入子串计数门」是同一条教训的第三次实例)。
- 本次实测:`continueCheckBtn.focus()` = **2**;`authorizeBtn.focus()` = **1**(未动);新注释内该字面量计数 = **0**(用散文指代)。

### 2. 指纹义务:`idi-08-VERIFICATION.md` 因**内容真变** stale,正确闭包是重跑 `/gsd-verify-work idi-08`

- 本次改动 `frontend/app.js`,而它在 **`idi-08-VERIFICATION.md`** 的 `covered_files` 里(规划期实测:**只有这一份** live 报告含 `app.js`)⇒ 该报告指纹按内容真变判 stale。
- **正确闭包 = 重跑 `/gsd-verify-work idi-08`,不是重算 digest。** 重算会断言「自验证以来覆盖输入无变化」,而 `app.js` 确实变了,那是不实陈述(与 `[Phase 08]` 对 `idi-04.1` 等的处置逐条一致)。
- **两条零代价事实(实测)**:`idi-08-UI-SPEC.md`(Task 3)与 `scripts/check-07-idi08-validation.py`(Task 1)**不在任何** live 报告的 `covered_files` 里 ⇒ 本次不新增任何指纹债务。
- **不得**用 `gsd-tools query verification status <phase>` 判定 stale —— 这些相位目录一律返回 `missing`。

## Verification(全部在项目 venv 上实跑)

| # | 命令 | 结果 |
|---|------|------|
| 1 | `.venv/bin/python scripts/check-07-idi08-validation.py --item g4` | 修复前 exit=1(主断言 FAIL,`actual=BODY`);修复后 exit=0,`actual=btn-continue-check` |
| 2 | 同上,判别控制行 | 修复前后均 PASS(它把交还调用置空,故与修复状态无关) |
| 3 | `.venv/bin/python scripts/check-07-idi08-validation.py`(全量 g1–g4) | **exit=0**;g1 21 / g2 39 / g3 10 / g4 3 条断言,0 FAIL 0 BLOCKED |
| 4 | `.venv/bin/python scripts/check-07-idi08-validation.py --item g4,g1` | exit=0;g1 一并复跑 ⇒ Escape 分支的既有 F1-d 交还零回归;g1 的 tier 断言开/关档位弹窗未受新增 focus 调用干扰 |
| 5 | `.venv/bin/python -m pytest -q` | **219 passed, 6 skipped**(1 warning,与基线一致) |
| 6 | `bash scripts/check-01-token-conformance.sh` | exit=0 PASS |
| 7 | `.venv/bin/python scripts/check-02-contrast.py` | exit=0 PASS(ORDER 0.363 逐字不变) |
| 8 | `bash scripts/check-03-hidden-uniqueness.sh` | exit=0 PASS |
| 9 | `bash scripts/check-04-important-count.sh` | exit=0 PASS |
| 10 | `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` | **exit=2 = 9/10 PASS,item 5 BLOCKED**(2 条 AI-smoke 腿,按设计 opt-in);**未传 `--ai-smoke`** |
| 11 | `node --check frontend/app.js` | 静默通过 |
| 12 | 改动面守卫 `git status --porcelain -- frontend/index.html frontend/style.css scripts/check-05-ui-uat.py frontend/vendor/` | **空** |
| 13 | `git diff --name-only 23ca439..HEAD` | 恰好三个文件(app.js / check-07 / idi-08-UI-SPEC.md) |
| 14 | `ls frontend/vendor/` | 恰好一个文件 `marked.min.js` |

## Deviations from Plan

**None — 计划按原文执行。** 三处实现细节是计划文字的直接落地,不构成偏离:

1. `_g4_enter_and_choose()` 用 `try/except` 包住 `expect_response` + 点击,请求未发出时记 **BLOCKED** 并附异常类名。理由:计划要求「前提不成立记 blocked,绝不记 PASS」,而「请求根本没发出去」正是一种前提不成立;不包住的话它会以 traceback 的形式爆掉整个 item,而不是给出可诊断的 BLOCKED。写法与本文件既有的 `_settle_cli_check()` 同款。
2. `_active_id()` 作为独立读取器抽出,供实例 1 的「点击前焦点」前提与两处主断言共用 —— 计划把读数规则(`id || tagName`)定为**固定**的,抽成一个函数让该规则只有一个落点。
3. 实例 1 的「点击前焦点在弹窗内」前提不成立时记 **BLOCKED**(计划明文),且**不 return** —— 主断言仍照跑。这样 item 判定仍为 blocked(BLOCKED 优先于 PASS),而不会因为一个前提抖动就吞掉主断言的读数。

## Issues Encountered

**1. 全量 check-07 首跑 g1 报 1 条 FAIL,复跑为绿 —— 已独立核实为既有的 `runCliCheck()` 竞态,与本改动无关。**
- 失败行:`FAIL g1 [#cli-check-overlay] Escape 后仍可见(范围锁,刻意不响应): expected=仍可见 actual=hidden=True`(注入可见态后被在途的 `runCliCheck()` 重新 `add('hidden')`)。
- **结构性排除**:`#btn-tier-loose` 在本文件中**只**在 `_g4_enter_and_choose()` 内被点击(g1 函数体内 `btn-tier-loose` / `chooseTier` 计数 = **0**)⇒ `continueCheckBtn.focus()` 在 g1 期间**不可能执行**。
- **复跑证据**:同一命令第二次全量运行 exit=0,g1/g2/g3/g4 全 PASS。
- **harness 自陈**:`_settle_cli_check()` 的文档注释早已记录该竞态(「实测竞态:同一命令连跑两次,一次绿一次红」)。**登记,不修**(不在本 quick 的范围,且修它要改 g1 的既有断言面)。

**2. 计划 verify 块里的 `grep -c 'FAIL'` 是 scope-blind 的(第三次同型)。** 修复后该计数为 **2**,而**断言级 FAIL 为 0** —— 那 2 行是 item 结论行 `item g4: PASS  (3 条断言,0 FAIL,0 BLOCKED)` 里的字面量「0 FAIL」。真实判据取 `grep -c '^FAIL '`(=0,修复前 =1)。不改计划、不改门,只登记读数。

**3. UI-SPEC `:772` 残留一处同源措辞未改(按计划刻意不动)。** 该行(§Sign-Off Items 的「已登记的两条落地约束」第 2 条)仍写「**成功路径不交还焦点**(见 §焦点契约的 F1 不覆盖情形①)」,而计划明令「只改两处」「不得触碰任何 Sign-Off 行 / §契约修正登记 A-8 行」⇒ 本次**未改**。它现在是**部分失真**的(tier 的选档成功路径已交还)。**留给 `/gsd-verify-work idi-08` 裁定**是否随账本一并收窄 —— 执行器不自裁超出授权面的改动。

## Known Stubs

None.

## Threat Flags

None — 无新增信任边界。改动是「移焦一行 + 本地测试 harness + 账本修订」;零新增依赖、零构建步骤、零端点、零 DOM 属性写入。威胁登记表 T-vb7-01/02/03 的 `accept` 处置与实测一致(g4 只在测试进程内的一次性页面会话里改写实例 `focus` 方法,生产代码零改动;每次运行从 `_awaiting_tier_fixture` 新建临时项目并在 `finally` 内关浏览器/删目录)。

## Decisions Made

见 frontmatter `key-decisions`。核心一条:**交还位置必须在 `await refreshChecksAfterStream();` 之后** —— 那里才是 `disabled` 被复位为 `false` 的时刻,而 `.focus()` 对禁用按钮是 no-op;提前放会静默失效而 diff 看上去是对的。这条已写进代码围栏注释(引 `D8-10`),不靠本文件传承。

## Next Phase Readiness

- 缺陷已修,守卫常驻(`scripts/check-07-idi08-validation.py` 的 item g4,随全量运行免费继承)。
- **待办(一条)**:`idi-08-VERIFICATION.md` 因 `frontend/app.js` 内容真变而 stale ⇒ 重跑 `/gsd-verify-work idi-08` 收口(不要重算 digest)。
- **待判(一条)**:UI-SPEC `:772` 的同源措辞是否一并收窄(见 Issues Encountered 第 3 条)。

---
*Quick: 260924-vb7-fix-the-tier-success-path-focus-loss-cho*
*Completed: 2026-09-24*

## Self-Check: PASSED

- `frontend/app.js` — FOUND(`continueCheckBtn.focus()` 计数 2、`authorizeBtn.focus()` 计数 1、新注释内该字面量计数 0)
- `scripts/check-07-idi08-validation.py` — FOUND(item g4 已注册进 `ITEMS`)
- `.planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-UI-SPEC.md` — FOUND(单文件 +6/−4)
- `260924-vb7-SUMMARY.md` — FOUND(frontmatter YAML 可解析,`status: complete`)
- 提交 `5fcc7dd` / `40e8de9` / `f483eef` — 三个全部 FOUND
- `git status --porcelain` 的代码面为空(未提交项只有本 quick 目录与执行前即存在的 `.planning/.idi07-dec*.txt` 临时文件)


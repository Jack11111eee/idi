---
phase: idi-04-tokens-contract
verified: 2026-09-25T08:01:44Z
status: passed
score: 15/15 must-haves verified
covered_files:
  - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md
  - .planning/phases/idi-04-tokens-contract/idi-04-01-PLAN.md
  - .planning/phases/idi-04-tokens-contract/idi-04-01-SUMMARY.md
  - .planning/phases/idi-04-tokens-contract/idi-04-02-PLAN.md
  - .planning/phases/idi-04-tokens-contract/idi-04-02-SUMMARY.md
  - .planning/phases/idi-04-tokens-contract/idi-04-03-PLAN.md
  - .planning/phases/idi-04-tokens-contract/idi-04-03-SUMMARY.md
  - .planning/phases/idi-04-tokens-contract/idi-04-UAT.md
  - frontend/style.css
  - scripts/check-01-token-conformance.sh
  - scripts/check-02-contrast.py
  - scripts/check-03-hidden-uniqueness.sh
  - scripts/check-04-important-count.sh
covered_digest: "v1:sha256:3d583e6d8338756718366ca76bc1f5d69ee1352bece7bbd3e4804aac9eb25e55"
behavior_unverified: 0
overrides_applied: 0
overrides:
  - must_have: "TOKEN-05 / TOKEN-06 / TOKEN-07 / TOKEN-08 — the non-colour scales are declared and consumed with zero residual literals outside the fence"
    reason: |
      SPENT — the deviation this override accepted no longer exists at HEAD, so the override carries
      no must-have and `overrides_applied` is 0. It is retained verbatim as documentation, per the
      override lifecycle ("overrides are never removed automatically; they persist as documentation").

      What was accepted on 2026-09-20: the residual `font-size: 20px` / `line-height: 1` at
      `.collapse-indicator` (then `frontend/style.css:434`), introduced AFTER the phase closed by the
      signed-off quick task 260918-qrq (`3684353`). Phase 4's own commit range was clean — the rule does
      not exist at `0c658aa` and the outside-fence `font-size: …px` count there was 0. The user ruled the
      literal out of Phase 4's scope and parked it in ROADMAP backlog `999.1`.

      What closed it (2026-09-25, quick task `260925-iin`, commit `3e50dca`): `--text-lg-plus: 20px` was
      declared as the 8th type tier (`style.css:326`) and `--lh-none: 1` as a glyph-only line height
      (`style.css:350`), and `.collapse-indicator` was rewritten to consume both
      (`style.css:686` — `.collapse-indicator { font-size: var(--text-lg-plus); line-height: var(--lh-none); }`).
      The glyph still renders at 20px. Backlog `999.1` is therefore closed.
    accepted_by: "Jack11111eee"
    accepted_at: "2026-09-20T06:18:25Z"
    resolved_at: "2026-09-25T08:01:44Z"
    resolved_by: "quick 260925-iin (3e50dca) — backlog 999.1 closed"
re_verification:
  previous_status: passed
  previous_score: 14/15 (1 accepted by user override)
  gaps_closed:
    - "TOKEN-05/06/07/08 (truth #10) — the residual bare literals at `.collapse-indicator` are gone. `frontend/style.css:686` now reads `font-size: var(--text-lg-plus); line-height: var(--lh-none);`; outside-fence `font-size: …px` declarations = 0, outside-fence non-`var()` `line-height` declarations = 0 (both were 1 at the 2026-09-20 pass). Closed by quick `260925-iin` (`3e50dca`), which also closed ROADMAP backlog `999.1`."
  gaps_remaining: []
  regressions: []
advisory:
  - finding: "The phase's own commit range is clean; the must-have that failed at the 2026-09-20 pass was introduced after the phase closed by a signed-off quick task (260918-qrq / `3684353`) and was already recorded in `idi-04.1-UI-REVIEW.md`. Phase 4's executor did not create it — and it has since been fixed by a second signed-off quick task (260925-iin / `3e50dca`)."
    category: other
    reason: "Recorded so the historical gap is attributed correctly and is not read as a Phase 4 execution defect."
    evidence_status: "deterministic — `git log -S 'font-size: 20px' -- frontend/style.css` → `3684353` (introduced); `git log --since=2026-09-20 -- frontend/style.css` → `3e50dca` (removed). The rule does not exist at the phase's close commit `0c658aa`."
---

# Phase 4: 设计契约、令牌层与契约校验 Verification Report

**Phase Goal:** `style.css` 拥有一份书面设计契约与单一令牌来源;全部字面量被替换为 `var()`,令牌块之外零裸 `#hex`;四条契约校验命令可独立运行;AA 达标值在**声明处**即选定。
**Verified:** 2026-09-25
**Status:** passed — 15/15 must-haves verified
**Re-verification:** Yes — 取代 `2026-09-20` 的报告(其 status 为 `passed`,14/15,1 条由用户裁定为范围外)

### 为什么这份报告是重算的,不是重盖戳的

本报告的 `covered_files` 覆盖的内容**确实变了**,且这是按内容判定的,不是按 mtime。用确定性工具在 HEAD(`0b6283a`)上重算**旧的 covered 集合**(含 `.planning/REQUIREMENTS.md`):

```
recomputed (old set, HEAD) = v1:sha256:cf7895c5ebf86c35508d8b7caac6cb71eaaf015d3b9b7107d4882dfd85b5fe43
recorded   (old set, 2026-09-20) = v1:sha256:4fd8b793e5777c1fbade75b5b420e1507efb567fb09a5fc76717eae2e7e13cf0
```

不匹配 ⇒ 内容真变。逐文件核对,自 2026-09-20T05:28:15Z 起被改动的 covered file 只有三个:

| Covered file | 自上次核验以来的提交数 | 变化 |
| --- | --- | --- |
| `frontend/style.css` | 21 | Phase 6 / Phase 7 的落地 + quick `260925-iin` 的 FIX 3(第 8 档字号 + `--lh-none`) |
| `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` | 1 | quick `260925-iin` 在 `## Typography` 下追加的指向行 |
| `.planning/phases/idi-04-tokens-contract/idi-04-UAT.md` | 1 | 记账性 frontmatter 归一(旧报告 Disclosed limitation #3 已披露) |

四个守卫脚本、三份 PLAN、三份 SUMMARY **零改动**。故本报告**所有来自令牌层的数值都从 HEAD 重新读出**,未从旧报告抄写。

**注意:上次核验里唯一一条失败项已经关闭。** 旧报告的 `gaps:` 条目(TOKEN-05/06/07/08 的 `.collapse-indicator` 裸字面量)在 HEAD 上不再成立 —— quick `260925-iin` 把 `20px` 与 `line-height: 1` 换成了 `var(--text-lg-plus)` / `var(--lh-none)`,并同时关闭了 ROADMAP backlog `999.1`。该 `overrides:` 条目因此**已用尽**(`overrides_applied: 0`),按 override 生命周期保留为文档。

### `covered_files` 变更(用户裁定,2026-09-25)

**本次把 `.planning/REQUIREMENTS.md` 从 `covered_files` 中移除。** 语义依据:`covered_files` 应表示「其变更足以使本报告的结论失效的**输入**」。需求索引表不是这样的输入,它是**下游记账** —— `phase.complete` 每次收口都会翻转它的行,而里程碑收口会**整个删除该文件**(`git rm .planning/REQUIREMENTS.md`,归档到 `milestones/v1.14-REQUIREMENTS.md`)。只要它留在 `covered_files` 里,每一次阶段收口、每一次里程碑收口都会**无缘无故地**把列出它的每一份报告打成 stale。`idi-04.1-radix` 的验证者已把这一点作为**结构性观察**提出并建议移出(旧报告 Disclosed limitation #3 亦记录了同一观察),用户现已采纳,适用于 v1.14 全部六份阶段报告。

`covered_digest` 因此按**移除后**的文件集合、用位置参数形式重算:

```
node .claude/gsd-core/bin/gsd-tools.cjs query verification.fingerprint \
  .planning/phases/idi-04-tokens-contract <其余 13 个 covered files…> --raw
→ v1:sha256:3d583e6d8338756718366ca76bc1f5d69ee1352bece7bbd3e4804aac9eb25e55
```

**本次未改动任何其他报告的 `covered_files`。**

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | SC1 — a single fenced `:root` block sits after `* { box-sizing }` and before `html, body`; outside it `style.css` has zero bare `#hex`, provable by CHECK-01 alone | ✓ VERIFIED | `grep -n ':root'` → exactly one hit at `style.css:6`; fence START L5, END L568; `* { box-sizing: border-box; }` L3 < L5 and `html, body {` L570 > L568. Fence-filtered `grep -o '#[0-9a-fA-F]\{3,6\}' \| wc -l` → **0**; `bash scripts/check-01-token-conformance.sh` → `PASS`, exit 0 |
| 2 | SC2 — pure value substitution: no existing selector changed position or name, and no declaration was added/removed beyond the documented deltas | ✓ VERIFIED | Comment-stripped, brace-aware selector-sequence diff `f912c1a:frontend/style.css` → `0c658aa:frontend/style.css` (Phase 4's own range): `:root` inserted at position 2, `.annotation-answered` removed (D-11), `.annotation-answered .annotation-note/.annotation-quote/.annotation-answer-body/.annotation-answer summary` + `button, input, select` appended at the end (D-11 / CR-06, N-4). The other 141 selectors' relative order is **identical**. *(At HEAD the invariant no longer holds — later signed-off work renamed/added selectors: `#sidebar`→`#doc-panel`, `#doc-pane`→`#doc-panel-body`, `--sidebar-w`→`--doc-panel-w`. That is qrq's deliberate IA swap, not a Phase 4 deviation; see Notes.)* |
| 3 | SC3 (ratio half) — every gate-hint text still reaches WCAG AA on each ground it lands on | ✓ VERIFIED | CHECK-02 at HEAD: `--color-text-muted` on `--color-surface-page` **5.77**, on `--color-surface` **5.62**, on `--color-surface-sunken` **5.19**, on `--color-surface-warning-subtle` **5.82** — all ≥ 4.5. `--color-text-muted` = `--radix-gray-11` = `#646464` (`style.css:55` / `:121`); the lightest grey passing on every ground. `.hint` (`style.css:667`) uses `--color-text-muted`; its actual ground is `--color-surface` ⇒ 5.62. `.venv/bin/python scripts/check-02-contrast.py` → `PASS: 0 failures`, exit 0 |
| 4 | SC3 (hierarchy half) — the hint stays strictly "quieter" than body text, checked as an ordering, not a re-thresholded ratio | ✓ VERIFIED | `ORDER 0.363  --color-text-muted before --color-text on --color-surface`; the assertion is strict (`q < l`). Sandbox mutation at HEAD: `--color-text-muted: var(--radix-gray-12)` → `FAIL: hierarchy inverted  1.000  --color-text-muted not before --color-text on --color-surface  (need < 1.000)`, exit 1 — correct direction. *(Constant moved 0.311 → 0.363 in 04.1; the scale widening is recorded at `04.1-UI-SPEC 04.1-N-1`.)* |
| 5 | SC4 (first half) — `.hidden` remains the site's only `!important` declaration, and `^\.hidden {` is exactly 1 | ✓ VERIFIED | `grep -nE '^[[:space:]]*\.hidden[[:space:]]*\{'` → `style.css:582` only; `style.css:582` is exactly `.hidden { display: none !important; }`; `grep -o '!important;' \| wc -l` → **1**. (`grep -c '!important'` → 5; the 4 extra hits are comment prose — not used as the gate.) CHECK-03 and CHECK-04 both PASS, exit 0 |
| 6 | SC4 (second half) — the five elements hidden only by `.hidden` are still correctly hidden **in the browser** (实检) | ✓ VERIFIED | Behavioral test at HEAD: `.venv/bin/python scripts/check-05-ui-uat.py --item 1 --browser bundled` → **PASS, 45 assertions, 0 FAIL / 0 BLOCKED**. 6 elements × 5 states force-`classList.add("hidden")` → all `display === "none"` (including the three 1-0-0 competitors `#selection-menu` / `#annotations-panel` / `#checks-panel`); reverse evidence: 6 elements become visible again when `.hidden` is removed. This is exactly the step CHECK-03 cannot see (rule text unique ≠ rule still wins the cascade) |
| 7 | SC5 — CHECK-01/02/03/04 run independently and each returns an explicit PASS/FAIL | ✓ VERIFIED | All four run standalone from the repo root and print `PASS` / exit 0 on the real tree. Each was independently mutated in a sandbox at HEAD and **failed** (all exit 1): CHECK-01 (bare hex → `FAIL: 1 bare hex outside the token block`; `var(--radix-gray-11)` outside the fence → `FAIL: 1 tier-1 primitive reference(s) outside the fence`; missing file → `FAIL: frontend/style.css not found`; END marker removed → `FAIL: expected exactly 1 fence START and 1 fence END, found 1/0`); CHECK-02 (unknown token → `FAIL: unknown token --gray-25x`; AA regression `--radix-gray-11: #8f8f8f` → `FAIL: 8 failures`; inversion → `FAIL: hierarchy inverted`; malformed entry inside the fence → `FAIL: 53 '/* PAIR' markers but only 52 parsed — malformed manifest entry`; manifest emptied → `FAIL: manifest coverage 0 pairs (0 TEXT / 0 NON-TEXT) below floor 24/20/4`; END marker removed → `FAIL: expected exactly 1 fence START and 1 fence END, found 1/0`); CHECK-03 (indented duplicate → `FAIL: expected 1 '.hidden {' rule, found 2`); CHECK-04 (second declaration → `FAIL: expected 1 '!important;' declaration, found 2`). No guard passes vacuously |
| 8 | TOKEN-02 hard invariant — tier-1 primitive names never appear outside the fence, mechanically gated | ✓ VERIFIED | Fence-filtered `grep -oE 'var\(--(white\|black\|gray\|green\|blue\|amber\|red\|purple\|radix)(-[0-9]+)?'` → **0**. CHECK-01's alternation covers `radix` (widened in 04.1-02); the mutation above proves the widened form is not vacuous |
| 9 | TOKEN-01 / TOKEN-03 — single `:root` block, two-layer taxonomy, meaning inventory precedes the tokens | ✓ VERIFIED | One `:root` (`style.css:6`) holding **120** declarations, no duplicates: 25 tier-1 (24 `--radix-*` + `--white`) + 53 `--color-*` tier-2 + 42 non-colour. Six action families present and consumed (`routine` 6 / `commit` 6 / `irreversible` 3 / `primary` 9 / `danger` 7 / `warning` 12 consumers). `04-UI-SPEC.md:357` `### Meaning inventory (produced **before** the tokens — TOKEN-03)` exists and is consumed. *(Temporal "inventory before tokens" is a process claim no command can re-verify — flagged assumption #3; the inventory exists and is consumed.)* |
| 10 | TOKEN-05 / TOKEN-06 / TOKEN-07 / TOKEN-08 — non-colour scales declared and consumed with **zero residual literals** outside the fence | ✓ VERIFIED *(was ✗ FAILED; closed by `260925-iin`)* | TOKEN-05 ✓ (12 `--space-*`: 1/2/4/6/8/10/12/14/16/24/32/40 — consumers 4/6/22/18/28/19/8/2/11/4/2/1, 0 residual `padding`/`margin`/`gap` px). TOKEN-06 ✓ (4 `--radius-*`: 8/10/28/999, consumers 15/7/2/5, 0 residual radius px; values superseded by qrq). TOKEN-07 ✓ (4 `--z-*` 10/20/100/200, ordering asserted in-fence L358-360, all four consumed at L815/868/884/1219, 0 bare z-index). **TOKEN-08 ✓** — 8 `--text-*` (12/14/16/18/20/24/22/28, all consumed incl. `--text-lg-plus` 1×) and `12.5px` = 0; **outside-fence `font-size: …px` declarations = 0** (was 1) and **outside-fence non-`var()` `line-height` declarations = 0** (was 1). The former violation at `style.css:434` is gone: `style.css:686` `.collapse-indicator { font-size: var(--text-lg-plus); line-height: var(--lh-none); }`. The two new declarations are inside the fence (`--text-lg-plus: 20px` L326, `--lh-none: 1` L350) and documented in the fence comment. *(TOKEN-07's z-index **ordering** half remains manual-only by explicit user ruling — see Requirements Coverage; it is not a literal and not a gap.)* |
| 11 | A11Y-04 — the four named text-contrast failures are fixed at declaration time | ✓ VERIFIED | CHECK-02 at HEAD: `.hint` → `--color-text-muted` on `--color-surface` **5.62** (was 2.73); `#pending-count` / `.badge-pending` → `--color-action-warning` on `--color-surface-warning` **10.93** (was 3.03); `.event-kind` → `--color-kind-fg` on `--color-kind-default` **5.92** (was 3.25); `.chat-user` → `--color-text` on `--color-surface-user` **13.30** (was 4.14). Each pair is in the fence manifest and computed by CHECK-02; the consumers are read live in the browser by UAT item 3 |
| 12 | A11Y-04b — all four non-`:disabled` opacity sites ruled, none silently changed | ✓ VERIFIED | At HEAD there is exactly **1** non-`:disabled` `opacity` declaration: `#rounds-placeholder.archive-mode #round-doc { opacity: 0.75 }` (L1387, kept). `.annotation-answered { opacity: 0.65 }` deleted → replaced by the 0-2-0 descendant rule at L852-855; `#round-doc.round-frozen` (L1247-1250) `opacity` removed → `filter: saturate(0.6)` + `box-shadow: inset 3px 0 0 var(--color-action-warning)` (S-4); `.tier-desc`'s `opacity` removed entirely by 04.1 R-3. The 8 `:disabled` opacities (6×0.55 at L941/953/1214/1268/1280/1339, 2×0.5 at L1294/1384) survive verbatim |
| 13 | `#confirm-error` keeps its 1-0-0 ID selector and danger colour; `#stream-banner.fatal` stays an independent selector | ✓ VERIFIED | `style.css:1293` `#confirm-error { color: var(--color-action-danger); }`; `style.css:886` `#stream-banner.fatal { background: var(--color-surface-danger); color: var(--color-action-danger); border-color: var(--color-border-danger-subtle); }` |
| 14 | `app.js` / `index.html` / `frontend/vendor/` untouched; pytest baseline held | ✓ VERIFIED | `git diff --name-only f912c1a 0c658aa -- frontend/app.js frontend/index.html` → **empty** (Phase 4's own range). `git status --porcelain -- frontend/` → empty; `ls frontend/vendor/` → `marked.min.js`; `.venv/bin/python -m pytest -q` → **219 passed, 6 skipped** (matches baseline); `node --check frontend/app.js` → exit 0. *(At HEAD both files differ from `f912c1a`, by later signed-off work only: `33bbd7d` qrq IA swap and `1d849b1` `#session-panel` gate fix — see Notes.)* |
| 15 | Plan 01/02 backstop — a frozen round renders with the amber inset rule, the historical switcher entry, and readable body text | ✓ VERIFIED | Behavioral test at HEAD: `.venv/bin/python scripts/check-05-ui-uat.py --item 2 --browser bundled` → **PASS, 5 assertions, 0 FAIL / 0 BLOCKED**. `#round-doc` classList contains `round-frozen`; computed `box-shadow` = `rgb(79, 52, 34) 3px 0px 0px 0px inset` (semantic parse: inset ✓ / x=3px ✓ / y=0 / blur=0 / spread=0 / colour == runtime-resolved `--color-action-warning` = `rgb(79, 52, 34)` ✓); `opacity` = `1`; `filter` = `saturate(0.6)`; body contrast **15.48:1** (threshold 4.5) |

**Score:** 15/15 truths verified (0 present-but-behavior-unverified)

### Required Artifacts

| Artifact | Expected | Status | Details |
| --- | --- | --- | --- |
| `frontend/style.css` | Fenced `:root` block + all literals → `var()` | ✓ VERIFIED | 1708 lines; fence L5-568; 120 fence declarations, no duplicates; 0 bare hex / 0 tier-1 leaks outside; 0 residual px literals for spacing / radius / z-index / font-size / line-height / font-weight |
| `scripts/check-01-token-conformance.sh` | CHECK-01 bare-hex + tier-1 gate | ✓ VERIFIED | 49 lines; asserts input exists, asserts exactly 1 START/1 END, counts occurrences; FAILs on all four mutations tested at HEAD |
| `scripts/check-02-contrast.py` | CHECK-02 WCAG checker | ✓ VERIFIED | 239 lines; stdlib only (`re`, `sys`); coverage floors 24/20/4; raw-vs-parsed marker reconciliation; α compositing; strict ORDER. FAILs on all six mutations tested at HEAD |
| `scripts/check-03-hidden-uniqueness.sh` | CHECK-03 `.hidden` uniqueness | ✓ VERIFIED | 17 lines; indentation-tolerant pattern; FAILs on an indented duplicate |
| `scripts/check-04-important-count.sh` | CHECK-04 declaration count | ✓ VERIFIED | 17 lines; counts `!important;` occurrences; FAILs on a second declaration |
| `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` | Written design contract | ✓ VERIFIED | 90399 bytes; Meaning inventory (L357), Tier 1/2 tables, Contrast Verification, Deliberate Delta Ledger, Global Hard Rules, Do-Not-Touch List, Sign-Off Items (S-1…S-4, L859), Literal exceptions (L847), the four command specs (L880), Not-in-v1.14 fence. The Typography pointer added by `260925-iin` (L317-321) is truthful and its 6-tier table is retained as Phase 4 history |

### Key Link Verification

| From | To | Via | Status | Details |
| --- | --- | --- | --- | --- |
| Every `var(--x)` outside the fence | A declared `--x` inside the fence | Gate 2 `comm -23` (consumed minus declared) | ✓ WIRED | Empty output — no silent `var()` unset. Also empty in the reverse direction (no declared-but-unconsumed token). No `var(--x, #fallback)` anywhere (`grep -cE 'var\(--[a-z0-9-]+,'` → 0) |
| `scripts/check-01-token-conformance.sh` | the two fence comments in `style.css` | awk fence state machine + START/END count assertion | ✓ WIRED | Correctly excludes in-fence literals; proven by mutation (bare hex outside → FAIL; END removed → FAIL) |
| `scripts/check-02-contrast.py` | the fenced PAIR/ORDER manifest + token declarations | regex over the fence text | ✓ WIRED | 53 pairs (35 TEXT + 18 NON-TEXT) + 1 ORDER parsed; drift fails loudly (`unknown token` / `malformed manifest entry` / `coverage below floor` / missing END all reproduced) |
| `#confirm-error` | `--color-action-danger` | 1-0-0 ID specificity over `.hint` 0-1-0 | ✓ WIRED | L1293 |
| `#round-doc.round-frozen` | `--color-action-warning` | `box-shadow: inset` (zero layout shift) | ✓ WIRED | L1249; read live in the browser by UAT item 2 |
| the four `--z-*` tokens | their four consumers | `z-index: var(--z-*)` | ✓ WIRED | L815 overlay / L868 badge / L884 banner / L1219 selection-menu; UAT item 4 reads them off the real DOM (not just the in-fence comment) |
| `--doc-panel-w` | `#doc-panel` | `flex: 0 0 var(--doc-panel-w)` | ✓ WIRED | L612 (added post-phase by qrq; recorded here because the fence now carries it) |
| `.collapse-indicator` | `--text-lg-plus` / `--lh-none` | `font-size` / `line-height` | ✓ WIRED | L686 — the closure of the previous pass's only gap |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| --- | --- | --- | --- | --- |
| `frontend/style.css` | every colour / space / type / radius / z token | `:root` fence declarations (primitives → semantic) | Yes — each `var()` resolves to a primitive declared in the fence; Gate 2 empty both directions | ✓ FLOWING |
| `scripts/check-02-contrast.py` | 53 manifest pairs + 1 ORDER | fence text, resolved through `var()` chains | Yes — 53 `PASS` lines with computed ratios; `ORDER 0.363` | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| --- | --- | --- | --- |
| CHECK-01 passes on the tree | `bash scripts/check-01-token-conformance.sh` | `PASS`, exit 0 | ✓ PASS |
| CHECK-02 passes on the tree | `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures` + `ORDER 0.363`, 53 pairs, exit 0 | ✓ PASS |
| CHECK-03 passes on the tree | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS`, exit 0 | ✓ PASS |
| CHECK-04 passes on the tree | `bash scripts/check-04-important-count.sh` | `PASS`, exit 0 | ✓ PASS |
| Guards can actually fail | sandbox mutation per guard (12 mutations at HEAD) | every guard produced exit 1 + an explicit `FAIL` line | ✓ PASS |
| SC4 second half is a real cascade outcome | `.venv/bin/python scripts/check-05-ui-uat.py --item 1 --browser bundled` | `PASS`, 45 assertions, 0 FAIL / 0 BLOCKED | ✓ PASS |
| Frozen-round backstop | `.venv/bin/python scripts/check-05-ui-uat.py --item 2 --browser bundled` | `PASS`, 5 assertions, 0 FAIL / 0 BLOCKED | ✓ PASS |
| Consumer wiring (Plan 01/02/03 spot-checks) | `.venv/bin/python scripts/check-05-ui-uat.py --item 3 --item 4 --item 6 --browser bundled` | `PASS` 17 / 65 / 6 assertions, 0 FAIL / 0 BLOCKED | ✓ PASS |
| AI-dependent interaction smokes | `.venv/bin/python scripts/check-05-ui-uat.py --item 5 --browser bundled` | `BLOCKED`, 9 assertions, 0 FAIL / 2 BLOCKED, exit 2 — by design, see Disclosed limitations | ? SKIP |
| Outside-fence bare hex | fence-filtered `grep -o '#[0-9a-fA-F]\{3,6\}' \| wc -l` | `0` | ✓ PASS |
| Fence-external tier-1 leak | fence-filtered `grep -oE 'var\(--(white\|…\|radix)(-[0-9]+)?' \| wc -l` | `0` | ✓ PASS |
| Gate 2 | `comm -23 <(var() names) <(declared names)` | empty (both directions) | ✓ PASS |
| Outside-fence `font-size: …px` declarations | fence-filtered `grep -nE 'font-size:[^;]*[0-9.]+px[^;]*;'` | **0** — was 1 at the previous pass | ✓ PASS |
| Outside-fence non-`var()` `line-height` declarations | fence-filtered `grep -nE 'line-height:[[:space:]]*[0-9.]+[[:space:]]*;'` | **0** — was 1 at the previous pass | ✓ PASS |
| Test baseline | `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped` | ✓ PASS |
| `app.js` syntax | `node --check frontend/app.js` | exit 0 | ✓ PASS |
| `app.js` / `index.html` untouched during the phase | `git diff --name-only f912c1a 0c658aa -- …` | empty | ✓ PASS |
| Ordering assertion direction | sandbox `--color-text-muted: var(--radix-gray-12)` | `FAIL: hierarchy inverted  1.000`, exit 1 | ✓ PASS |
| AA-threshold direction | sandbox `--radix-gray-11: #8f8f8f` (the qrq regression value) | `FAIL: 8 failures`, exit 1 | ✓ PASS |

### Probe Execution

Not applicable — the phase declares no `scripts/*/tests/probe-*.sh` and is not a migration/tooling phase; its four contract-check commands are exercised above. (`scripts/probe-05-resolve-color.py` exists on disk but belongs to the inserted sub-phase `idi-04.1-radix`, plan 04 — outside this phase's scope.)

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
| --- | --- | --- | --- | --- |
| TOKEN-01 | 01 | Single `:root` token block, native custom properties, zero build | ✓ SATISFIED | Exactly one `:root` at L6 inside the fence. *(04.1 carried and re-proved; the fence survived its value-layer rewrite.)* |
| TOKEN-02 | 01 | Two-layer taxonomy; tier-1 names never outside the fence | ✓ SATISFIED | 25 primitives; fence-external primitive refs = 0; gated by CHECK-01 (alternation widened to cover `radix` in 04.1-02, mutation-proven non-vacuous). *(04.1 carried and re-proved.)* |
| TOKEN-03 | 01 | Meaning inventory first, then converge the competing accents | ✓ SATISFIED *(phase evidence; not re-proved by 04.1)* | `04-UI-SPEC.md:357` `### Meaning inventory (produced before the tokens)`; six action families + kind families landed and consumed. **04.1 explicitly did not touch this requirement** — the evidence is Phase 4's own, unchanged |
| TOKEN-04 | 01 | Zero bare `#hex` outside the token block | ✓ SATISFIED | 0 outside-fence hex occurrences; CHECK-01 PASS. *(04.1 carried and re-proved.)* |
| TOKEN-05 | 02 | Spacing scale | ✓ SATISFIED (S-1) | 12 `--space-*` steps incl. the five off-base half-steps the user signed off (S-1); all 12 consumed; 0 residual px. **04.1 explicitly did not touch this requirement** |
| TOKEN-06 | 02 | 3-value radius scale | ✓ SATISFIED (S-1-class deviation, values superseded) | Scale present (4 values: `--radius-sm` 8 / `--radius-md` 10 / `--radius-lg` 28 / `--radius-pill` 999); all 4 consumed; 0 residual radius px. **The requirement's literal values (`sm` 4px / `md` 6–8px) are not the values at HEAD** — qrq's signed-off reskin moved them (and added `--radius-lg`). **04.1 did not touch this requirement**; I am reporting the value drift, not flipping it on 04.1's evidence |
| TOKEN-07 | 02 | `--z-*` tokens with an asserted ordering | ✓ SATISFIED (PARTIAL — ordering half manual-only) | 4 tokens; ordering assertion comment at L358-360 (badge 10 < banner 20 < overlay 100 < selection-menu 200); 0 bare z-index; all four consumed (L815/868/884/1219) and read live off the DOM by UAT item 4. The **ordering half has no mechanical assertion** — the user adjudicated it to manual-only acceptance (`idi-04.1-VALIDATION.md`, `REQUIREMENTS.md:176`), so this is a recorded user ruling, not an unverified gap |
| TOKEN-08 | 02 | Font-size scale; remove `12.5px` (3 sites) and `14px` | ✓ SATISFIED at HEAD *(the previous pass's residual literal is closed)* | `12.5px` = 0 ✓; outside-fence `font-size` literals = 0 ✓ (was 1); the 8-tier scale is declared and fully consumed, incl. the new `--text-lg-plus` (20px) whose sole consumer is `.collapse-indicator`. The residual `.collapse-indicator { font-size: 20px; line-height: 1 }` was closed by quick `260925-iin` (`3e50dca`) — backlog `999.1` closed. `14px` is now `--text-base`, the deliberate S-2 sign-off (keeping it preserves the Phase 5 SC5 / Phase 6 SC5 downstream gates). **04.1 explicitly did not touch this requirement** |
| CHECK-01 | 01 | Token-conformance script | ✓ SATISFIED | Present, runs standalone, PASSes on the tree, FAILs on 4 mutations at HEAD. *(04.1 substantially closed — the tier-1 alternation was widened and mutation-proved.)* |
| CHECK-02 | 03 | Contrast-check script | ✓ SATISFIED | Present, stdlib-only, PASSes on the tree (53 pairs), FAILs on 6 mutations at HEAD. *(04.1 substantially closed; Phases 5/7 grew the manifest 43 → 53 pairs — the fence comment documents each layer.)* |
| CHECK-03 | 01 | `.hidden` uniqueness guard | ✓ SATISFIED | Present, PASSes, FAILs on an indented duplicate. *(04.1 carried and re-proved.)* |
| CHECK-04 | 01 | `!important` count = 1 | ✓ SATISFIED | Present, PASSes, FAILs on a second declaration. *(04.1 carried and re-proved.)* |
| A11Y-04 | 01 (+03) | All AA text failures fixed at declaration | ✓ SATISFIED | Four named failures now 5.62 / 10.93 / 5.92 / 13.30; manifest verifies all grounds. *(04.1 substantially closed — the 3.23:1 `--color-text-muted` regression window was eliminated.)* |
| A11Y-04b | 01 + 02 (+03) | Opacity-composite failures covered | ✓ SATISFIED | Exactly 1 non-`:disabled` opacity site remains (archive 0.75); the other three ruled; 8 `:disabled` preserved. *(04.1 substantially closed — R-3 removed the `.tier-desc` opacity overreach.)* |

**Orphaned requirements:** none — `REQUIREMENTS.md` maps all 14 IDs to Phase 4, and all 14 appear in a plan's `requirements:` frontmatter (01: TOKEN-01…04, A11Y-04, CHECK-01/03/04; 02: TOKEN-05…08, A11Y-04b; 03: CHECK-02, A11Y-04, A11Y-04b).

**Note on `REQUIREMENTS.md` bookkeeping (recorded, not resolved here — and no longer a `covered_file`):** the traceability table now marks all 14 rows `Complete`, with two qualifiers: TOKEN-07 `Complete (PARTIAL — 序关系半场 manual-only …)` (correct, matches the user ruling) and **TOKEN-08 `Complete (PARTIAL — .collapse-indicator 的 20px / line-height: 1 越轨字面量经用户裁定为 Phase 4 范围外 …)` — this qualifier is now STALE**: the literal no longer exists at HEAD, and backlog `999.1` (which it cites) is closed. `REQUIREMENTS.md` is deliberately **not** in this report's `covered_files` any more, so this report's conclusions do not depend on that table; the stale qualifier is recorded here for the orchestrator/user to correct at the next `phase.complete` or milestone close. This is a bookkeeping item, not a Phase 4 execution gap.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| --- | --- | --- | --- | --- |
| — | — | No `TBD` / `FIXME` / `XXX` / `TODO` / `HACK` / `PLACEHOLDER` in `style.css` or the four scripts | — | None |
| — | — | No stubs, empty returns, or hardcoded-empty values in the deliverable (it is CSS + zero-dependency guards) | — | None |
| — | — | Prohibitions clean: 0 `@layer`, 0 `@property`, 0 tokenized `display`, 0 `var()` fallbacks, 0 `rgba(` outside the fence | — | None |

**No blocker anti-patterns.** The one blocker carried by the 2026-09-20 report (`style.css:434` bare `font-size`/`line-height`) is **gone at HEAD** — see truth #10.

### Advisory (New Scope, Unevidenced)

Re-verification ran (`is_re_verification = true`), so this section is emitted. New-scope findings from the per-file scan:

| # | Finding | Category | Why Advisory |
| --- | --- | --- | --- |
| 1 | Historical provenance of the (now-closed) gap: the failed must-have was introduced after the phase closed by signed-off quick `260918-qrq`, not by Phase 4's executor | other | Deterministic evidence exists (`git log -S`); recorded as `advisory:` in frontmatter so the gap is attributed correctly |
| 2 | The `## Typography` table in `04-UI-SPEC.md` still shows the 6-tier Phase-4 scale (11/12/13/14/15/16) while the live scale is 8 tiers | other | Deliberate — the pointer line at `04-UI-SPEC.md:317-321` declares it Phase 4 history superseded by `idi-05-UI-SPEC.md`. Recorded, not blocking |
| 3 | `04-UI-SPEC.md` L-5's literal exception still cites `#state-badge { right: 448px }` at `style.css:204`; at HEAD `#state-badge` is at L861 and no longer carries `right: 448px` | other | Deliberate — the exceptions list was left unchanged by `260925-iin`; L-5 was an accurate Phase 4-era record and Phase 6 superseded it. Not a Phase 4 defect |

None of these reverts a completed must-have or justifies a `--gaps` cycle.

### Notes on the phase's honest record (verified, not defects)

- **The (former) failed must-have was not Phase 4's work.** `.collapse-indicator { font-size: 20px; line-height: 1; }` was added by quick task `260918-qrq` (`3684353`, 2026-09-18 20:01), i.e. ~20 hours **after** the phase's close commit `0c658aa` (2026-09-18 00:11). At `0c658aa` the rule does not exist and the outside-fence `font-size: …px` count is 0. Phase 4 delivered exactly its enumerated baseline scope; the literal has since been tokenized away by `260925-iin`.
- **WR-04 resolved by `81ae6fd`.** `idi-04-REVIEW.md` (6 Critical / 4 Warning / 5 Info) and `idi-04-REVIEW-FIX.md` (9 fixed, 1 skipped) are part of the phase's record. The tree now carries the corrected `.tier-desc` rule — note that 04.1's R-3 later removed its `opacity` entirely. The UI-SPEC E6 ruling is corrected at both `04-UI-SPEC.md:689` and `:1040`. These are dated, attributed corrections, not inconsistencies.
- **The pair-count arithmetic has four numbers in circulation (24 / 34 / 43 / 53), and 53 is the landed figure.** `ROADMAP.md` Phase 4 says 24 (20 TEXT + 4 NON-TEXT) — the figure at plan-freeze time; the disk carried 34 (29 TEXT + 5 NON-TEXT) before 04.1; 04.1 recomputed to 43; Phases 5 and 7 grew it to **53 (35 TEXT + 18 NON-TEXT) + 1 ORDER**, which is what CHECK-02 parses at HEAD. D-15's ruling is "re-enumerate by what actually landed"; the earlier values are historical, not deviations. *(The ROADMAP plan-03 line still reads "20 文本 + 4 非文本" — stale prose, not a shortfall. The fence comment at `style.css:442-448` documents the 53 figure and its provenance.)*
- **`--green-800` is gone and `--fw-medium` is now legitimate.** `--green-800` no longer exists in the fence, and `--fw-medium: 500` **is** declared and consumed 8×. Hard Rule 5 ("never declare a token you are not consuming") is therefore satisfied for it. `--fw-*` is now 3 tokens, not 2.
- **`app.js` / `index.html` are changed at HEAD, but not by Phase 4.** Phase 4's own range is clean (`git diff --name-only f912c1a 0c658aa` → empty). The changes come from `33bbd7d` / `253d4d3` (qrq IA swap) and `1d849b1` (`#session-panel` gate fix). The phase's zero-touch criterion was satisfied by the phase; the file-level invariant was later superseded by signed-off work.
- **SC2's invariant is also superseded at HEAD.** qrq deliberately renamed `#sidebar`→`#doc-panel`, `#doc-pane`→`#doc-panel-body`, `--sidebar-w`→`--doc-panel-w` and added `:has()` empty-state rules. SC2 ("no existing selector changed position or name") was a Phase 4 success criterion and held for Phase 4's own change; it is not a perpetual invariant and later signed-off work is not bound by it.
- **`idi-04-01-SUMMARY.md`'s wording "exactly one added line — `:root {`"** is imprecise: against `f912c1a` the tree also adds the `.annotation-answered` descendant rule and removes `.annotation-answered`, and Plan 02 later adds `button, input, select`. All three are documented in the plans' own ledgers, so SC2 still holds — this is a SUMMARY-wording inaccuracy, not a goal failure. Recorded as info, not a gap.
- **IN-05 (Info, out of scope):** `check-02-contrast.py` exits 1 via an uncaught `FileNotFoundError` traceback when `frontend/style.css` is missing rather than a clean `FAIL` line. Non-blocking — the exit code is still non-zero and the real-tree path is guarded by CHECK-01's own input assertion.
- **Temporal assumption #3 (flagged, not re-verifiable):** TOKEN-03's "meaning inventory produced **before** the tokens" is a process claim. No command can re-verify the ordering in which a human produced two documents. The inventory exists (`04-UI-SPEC.md:357`) and is consumed by the landed tokens; the temporal half is taken on the record.
- **Recorded downstream items, not Phase 4 gaps:** (a) `#confirm-error` carries `class="hint hidden"` and computes 16px while every other `.hint` computes 14px — same class, two sizes (`.overlay-card p` 0-1-1 beats `.hint` 0-1-0); recorded in `idi-04.1-UI-REVIEW.md` Pillar 4, a typography item for Phase 5. (b) TOKEN-07's ordering half is manual-only by user ruling.

### Disclosed limitations (accepted, not silently dropped)

1. **UAT test 5's two AI-dependent interaction smokes were not re-run at HEAD.** The run gives `item 5: BLOCKED (9 assertions, 0 FAIL, 2 BLOCKED)` and `exit=2`. This is by design: the harness's exit contract is `code = 1 if any_fail else (2 if any_blocked else 0)`, and the two `blocked()` calls exist precisely so that "runtime verification claimed rather than performed" stays visible (T-idi041-09). `idi-04-UAT.md` §Test 5 records them as **run and PASSED** under `--ai-smoke` (claude CLI available), with the two real interactions described; the user has explicitly declined a re-run. This report therefore accepts the recorded UAT evidence for those two smokes and records the non-re-run as a disclosed limitation. It does **not** treat the default run's `exit=2` / 2 BLOCKED as a defect.
2. **Keyboard text selection cannot be automated** in this environment (`Shift+ArrowRight` leaves `window.getSelection()` empty in `<p>`, `tabindex` containers and `contenteditable`; `--enable-caret-browsing` does not help). None of this phase's six UAT items depends on it.
3. **`covered_files` 变更与指纹重算 —— 如实披露。** 本次核验**移除了** `.planning/REQUIREMENTS.md`(理由见上方专节),并按移除后的集合重算 `covered_digest`。这是**语义修正**,不是把一次真实内容变更盖掉:同一份报告里,内容真变(style.css / 04-UI-SPEC.md 改动)走的是**重新验证**,13 项事实全部从 HEAD 重读并逐条留证。指纹记录值为 `v1:sha256:3d583e6d…`。**注:** `idi-07-VERIFICATION.md` 记录过一次对本报告的独立重算(`v1:sha256:02a26269…`),那是**旧集合**(含 `REQUIREMENTS.md`)、且在其自身 HEAD 上算的;两者不同源,不构成矛盾。

### Carry-forward obligations (out of scope — NOT rewritten by this report)

1. **C-1 downstream-gate reference audit — measured false at HEAD, deliberately not corrected here.** Real-browser measurement (reproduced at HEAD by UAT item 4): `#brainstorm-view h2` computes to **`16px`** with colour `--color-action-warning` = **`#4f3422`**. Static basis: `frontend/style.css:679-683` uses `font-size: var(--text-md)` and `color: var(--color-action-warning)`; in-fence `--text-md: 16px` and `--radix-amber-12: #4f3422`. **Six sites still assert `14px` / `#8a6508`** (five in `.planning/ROADMAP.md` — hard-rule-3 prose, Phase 5 Pitfall 9, §Phase 5 Gates, §Phase 6 SC5, §Phase 6 Gates — plus `04-UI-SPEC.md` carry-forward #7). `idi-04-UAT.md` §Carry-Forward ① records the same six sites and the one-line correction (`14px` → `16px`, `#8a6508` → `#4f3422`). Those are **future phases' signed-off gates**; per the phase's own prohibition, this report does **not** rewrite them. User adjudication required.
2. **Carry-forward #8 — Phase 7's focus ring must be re-measured on the new grounds.** `--color-focus` (Phase 4's ring colour) was originally measured against `#fafafa`; the grounds are now `--color-surface` `#f9f9f9` and `--color-surface-page` `#fcfcfc`. *(Phase 7 has since landed its own ring and its own PAIR entries — `--color-focus` on both grounds is in the 53-pair manifest and passes. The obligation is recorded as Phase 4's hand-off, not as an open Phase 4 item.)*
3. **`idi-04.1-UI-REVIEW.md`'s own open findings** (destructive buttons painting a blue border on a red fill; no focus indicator on filled buttons; no hover feedback on filled buttons) are that sub-phase's record, outside this phase's scope.

### Human Verification Required

None outstanding. The six items the previous report routed to human verification are all resolved by `idi-04-UAT.md` (6/6 `pass`) and were reproduced at HEAD where the environment permits — items 1, 2, 3, 4 and 6 were re-run by this verification (`0 FAIL` on every one); item 5's two AI-dependent smokes carry the recorded `--ai-smoke` evidence and the disclosed non-re-run (see Disclosed limitations).

### Gaps Summary

**零失败项。** 上一次核验的唯一一条失败(TOKEN-05/06/07/08 —— `.collapse-indicator` 在围栏外的裸 `font-size: 20px` / `line-height: 1`)在 HEAD 上**已关闭**:quick `260925-iin`(`3e50dca`)在围栏内声明了第 8 档字号 `--text-lg-plus: 20px`(L326)与 glyph-only 行高 `--lh-none: 1`(L350),并把 `style.css:686` 改为消费两者;字形仍渲染 20px,ROADMAP backlog `999.1` 随之关闭。该 `overrides:` 条目因此**用尽**(`overrides_applied: 0`),按 override 生命周期保留为文档而非静默删除。

阶段其余全部目标都在树上第一手复验通过: the single fenced `:root` block is correctly placed (L5-568, `:root` at L6, between `* { box-sizing }` L3 and `html, body` L570), outside-fence bare hex and tier-1 leaks are zero, all colour / space / radius / z-index / font-size / line-height / font-weight literals are migrated, Gate 2 is empty in both directions, all four guard commands run independently and each was proven able to fail at HEAD (12 mutations), the A11Y-04 / A11Y-04b fixes are in place with the AA values chosen at declaration time, the two behavioral truths (SC4's cascade outcome; the frozen-round backstop) pass in a real browser at HEAD, `app.js` / `index.html` were untouched by the phase, and the pytest baseline held (219 passed / 6 skipped).

**判定: `passed`,15/15。** 无 `gaps:`、无 `human_verification` 项、无 `behavior_unverified` 项。本报告同时是 `.planning/REQUIREMENTS.md` 移出 `covered_files` 后的第一份指纹(用户 2026-09-25 裁定)。

---

_Verified: 2026-09-25_
_Verifier: Claude (gsd-verifier)_

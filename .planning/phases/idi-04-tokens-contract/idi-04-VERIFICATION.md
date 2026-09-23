---
phase: idi-04-tokens-contract
verified: 2026-09-20T05:28:15Z
status: passed
score: 14/15 must-haves verified (1 accepted by user override)
covered_files:
  - .planning/REQUIREMENTS.md
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
covered_digest: "v1:sha256:4fd8b793e5777c1fbade75b5b420e1507efb567fb09a5fc76717eae2e7e13cf0"
behavior_unverified: 0
overrides_applied: 1
overrides:
  - must_have: "TOKEN-05 / TOKEN-06 / TOKEN-07 / TOKEN-08 — the non-colour scales are declared and consumed with zero residual literals outside the fence"
    reason: |
      The residual `font-size: 20px` / `line-height: 1` at `frontend/style.css:434`
      (`.collapse-indicator`) was introduced AFTER the phase closed by the signed-off quick task
      260918-qrq (`3684353`, 2026-09-18 20:01; phase close `0c658aa`, 2026-09-18 00:11). Phase 4's own
      commit range is clean — the rule does not exist at `0c658aa` and the outside-fence
      `font-size: …px` count there was 0. The phase delivered its enumerated baseline scope.
      RULED OUT OF PHASE 4'S SCOPE by the user; tracked as a typography item instead (see the
      `## Backlog` entry `999.1` in `.planning/ROADMAP.md`, which also carries the stale
      item-2 diagnostic string in `scripts/check-05-ui-uat.py:588`).
      NOT silently dropped: the finding remains recorded here, in `gaps:` below, and in
      `idi-04.1-UI-REVIEW.md` Pillar 4 (3/4, "an undeclared 6th size").
    accepted_by: "Jack11111eee"
    accepted_at: "2026-09-20T06:18:25Z"
re_verification:
  previous_status: human_needed
  previous_score: 13/15
  gaps_closed:
    - "SC4 (second half) — the five `.hidden`-only elements are still correctly hidden in the browser. Was ⚠️ PRESENT_BEHAVIOR_UNVERIFIED. Now exercised by `scripts/check-05-ui-uat.py --item 1` at HEAD: PASS, 45 assertions, 0 FAIL / 0 BLOCKED (UAT test 1)."
    - "Plan 01/02 backstop — a frozen round renders with the amber inset rule, opacity 1, filter saturate(0.6) and readable body text. Was ⚠️ PRESENT_BEHAVIOR_UNVERIFIED. Now exercised by `scripts/check-05-ui-uat.py --item 2` at HEAD: PASS, 5 assertions, 0 FAIL / 0 BLOCKED (UAT test 2)."
    - "human_verification #1 — Plan 01 DevTools spot-checks (13 items) → resolved by UAT test 3; re-run at HEAD: item 3 PASS, 15 assertions, 0 FAIL / 0 BLOCKED."
    - "human_verification #2 — Plan 02 DevTools spot-checks (16 items) → resolved by UAT test 4; re-run at HEAD: item 4 PASS, 24 assertions, 0 FAIL / 0 BLOCKED."
    - "human_verification #3 — Plan 03 DevTools spot-checks (10 items) → resolved by UAT test 5; re-run at HEAD: item 5, 9 assertions, 0 FAIL / 2 BLOCKED (the 2 BLOCKED are the AI-dependent smokes, see Disclosed limitations)."
    - "human_verification #4 — CR-06 rendering outcome → resolved by UAT test 6; re-run at HEAD: item 6 PASS, 2 assertions, 0 FAIL / 0 BLOCKED."
  gaps_remaining: []
  regressions:
    - "Truth #10 (TOKEN-05/06/07/08 — non-colour scales declared and consumed with zero residual literals) no longer holds: `frontend/style.css:434` `.collapse-indicator { font-size: 20px; line-height: 1; }` is a bare literal outside the fence, in a tokenized family. Introduced AFTER the phase closed by quick task 260918-qrq (`3684353`, 2026-09-18 20:01), which specified the literal verbatim in its own plan. Deterministic evidence: outside-fence `font-size: …px` count is 1 (was 0 at `0c658aa`), non-`var()` `line-height` count is 1 (was 0)."
gaps:
  - truth: "TOKEN-05 / TOKEN-06 / TOKEN-07 / TOKEN-08 — the non-colour scales are declared and consumed with zero residual literals outside the fence"
    status: failed
    reason: |
      `frontend/style.css:434` carries `.collapse-indicator { font-size: 20px; line-height: 1; }` — a bare
      `font-size` literal and a bare `line-height` literal, both outside the fence (fence = L5-343), both in
      families the phase tokenized (`--text-*` / `--lh-*`). This violates three things at once:
      (a) the phase goal's clause 「全部字面量被替换为 `var()`」;
      (b) the phase's own delivered contract, `04-UI-SPEC.md:841` §"Literal exceptions (the complete list —
          nothing else may be a literal)" — L-1…L-5 do not include it, and L-2 covers only unitless `0`, not `1`;
      (c) plan-01's prohibition 「不得为已令牌化的值留下字面量」.
      Provenance is post-phase and signed-off: the rule was introduced by quick task 260918-qrq
      (`3684353`, 2026-09-18 20:01 — after the phase's close commit `0c658aa`, 2026-09-18 00:11), whose own
      plan wrote the literal verbatim (`260918-qrq-PLAN.md:359`). Phase 4's own commit range is clean: at
      `0c658aa` `.collapse-indicator` did not exist and the outside-fence `font-size: …px` count was 0.
      The finding is already recorded as a scored finding in `idi-04.1-UI-REVIEW.md` (Pillar 4, 3/4:
      "`20px` (`.collapse-indicator`) is an undeclared 6th size") but was never turned into a gap and is not
      covered by any later milestone phase: Phase 5's Deliverables name `.markdown-body h1/h2/h3`, `#doc-pane > h1`
      and the `code` 12.5px fold — not `.collapse-indicator`'s font-size; Phase 5 SC1 names only the four
      chrome `h2`/`h3` overrides. So this is a real, unassigned hole, not a deferral.
      The declared type scale at HEAD is 12 / 14 / 16 / 18 / 24 — `20px` is not a step on it, so the fix is a
      decision (add a step, re-map to an existing step, or amend the UI-SPEC with an explicit L-6 exception),
      not a mechanical substitution.
    artifacts:
      - path: "frontend/style.css"
        issue: "L434 `.collapse-indicator { font-size: 20px; line-height: 1; }` — two bare literals outside the token fence, in the `--text-*` / `--lh-*` families."
    missing:
      - "Replace `font-size: 20px` with a declared `--text-*` step (adding the step to the fence and to the UI-SPEC's type scale if 20px is to survive), or re-map it to an existing step — a type-scale decision, recorded in the UI-SPEC."
      - "Replace `line-height: 1` with a declared `--lh-*` step, or add it to `04-UI-SPEC.md:841` §Literal exceptions with its rationale."
      - "If the user instead judges a post-phase literal out of Phase 4's scope, record that as an `overrides:` entry (see Gaps Summary) — do not leave it unrecorded."
advisory:
  - finding: "The phase's own commit range is clean; the failed must-have was introduced after the phase closed by a signed-off quick task (260918-qrq / `3684353`) and is already recorded in `idi-04.1-UI-REVIEW.md`. Phase 4's executor did not create it."
    category: other
    reason: "Recorded so the gap is attributed correctly and is not read as a Phase 4 execution defect."
    evidence_status: "deterministic — `git log -S 'font-size: 20px' -- frontend/style.css` → `3684353`; the rule does not exist at the phase's close commit `0c658aa`."
---

# Phase 4: 设计契约、令牌层与契约校验 Verification Report

**Phase Goal:** `style.css` 拥有一份书面设计契约与单一令牌来源;全部字面量被替换为 `var()`,令牌块之外零裸 `#hex`;四条契约校验命令可独立运行;AA 达标值在**声明处**即选定。
**Verified:** 2026-09-20
**Status:** passed — 14/15 verified,1 条由用户裁定为范围外(见 frontmatter `overrides:` 与下方 Gaps Summary)
**Re-verification:** Yes — 取代 `2026-09-18` 的报告(其 status 为 `human_needed`,13/15)

### 为什么这份报告是重算的,不是重盖戳的

旧报告的 `covered_files` 覆盖的内容**确实变了**,且这是按内容判定的,不是按 mtime。用确定性工具在 HEAD 上重算**旧 covered 集合**:

```
recomputed = v1:sha256:cd9aa7610a61bf2717130a387428ac19929dc5fbb638c95554cc5af91a816239
recorded   = v1:sha256:f4dd04b61176ae0346e443ba470ff9c94228fa7c2d3b8964637421e62f7d8431
```

不匹配 ⇒ 内容真变。变化来自插入子阶段 `idi-04.1-radix`(值层 Radix 重写,改写了 `frontend/style.css` 与 `scripts/check-01-token-conformance.sh`)与更早的 quick `260918-qrq`(IA 对调 + 换肤)。故本报告**所有来自令牌层的数值都从 HEAD 重新读出**,未从旧报告抄写。

**注意:唯一一条新出现的失败,不是 04.1 造成的。** 它是 `260918-qrq`(`3684353`)留下的,04.1 的 UI 审阅已记录但从未转成缺口。逐条证据见下方 Truth #10 与 `gaps`。

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | SC1 — a single fenced `:root` block sits after `* { box-sizing }` and before `html, body`; outside it `style.css` has zero bare `#hex`, provable by CHECK-01 alone | ✓ VERIFIED | `grep -n ':root'` → exactly one hit at `style.css:6`; fence START L5, END L343; `* { box-sizing…` L3 < L5 and `html, body {` L345 > L343. Fence-filtered `grep -o '#[0-9a-fA-F]\{3,6\}' \| wc -l` → **0**; `bash scripts/check-01-token-conformance.sh` → `PASS`, exit 0. *(Fence grew L5-211 → L5-343 in 04.1; placement invariant unchanged.)* |
| 2 | SC2 — pure value substitution: no existing selector changed position or name, and no declaration was added/removed beyond the documented deltas | ✓ VERIFIED | CSS-parsed selector-sequence diff `f912c1a:frontend/style.css` → `0c658aa:frontend/style.css` (Phase 4's own range) is: `:root {` inserted at position 2, `.annotation-answered` removed (D-11), `.annotation-answered .annotation-answer summary` + `button, input, select` appended at the end (D-11 / CR-06, N-4). Relative selector order **identical**. *(At HEAD the invariant no longer holds — later signed-off work renamed/added selectors: `#sidebar`→`#doc-panel`, `#doc-pane`→`#doc-panel-body`, `--sidebar-w`→`--doc-panel-w`. That is qrq's deliberate IA swap, not a Phase 4 deviation; see Notes.)* |
| 3 | SC3 (ratio half) — every gate-hint text still reaches WCAG AA on each ground it lands on | ✓ VERIFIED | Manifest: `--color-text-muted` on `--color-surface-page` **5.77**, on `--color-surface` **5.62**, on `--color-surface-sunken` **5.19**, on `--color-surface-warning-subtle` **5.82** — all ≥ 4.5. `--color-text-muted` = `--radix-gray-11` = `#646464`; the lightest grey passing on every ground. `.hint`'s actual ground is `--color-surface` ⇒ 5.62 (was 2.73 pre-phase, 3.23 during the qrq regression window). `python3 scripts/check-02-contrast.py` → `PASS: 0 failures`, exit 0 |
| 4 | SC3 (hierarchy half) — the hint stays strictly "quieter" than body text, checked as an ordering, not a re-thresholded ratio | ✓ VERIFIED | `ORDER 0.363  --color-text-muted before --color-text on --color-surface`; the assertion is `q < l` (strict). Mutation at HEAD: `--color-text-muted: var(--radix-gray-12)` → `FAIL: hierarchy inverted  1.000  --color-text-muted not before --color-text on --color-surface  (need < 1.000)`, exit 1 — correct direction. *(Constant moved 0.311 → 0.363 in 04.1; the scale widening is recorded at `04.1-UI-SPEC 04.1-N-1`.)* |
| 5 | SC4 (first half) — `.hidden` remains the site's only `!important` declaration, and `^\.hidden {` is exactly 1 | ✓ VERIFIED | `grep -nE '^[[:space:]]*\.hidden[[:space:]]*\{'` → `style.css:357` only; `grep -o '!important;' \| wc -l` → **1**. CHECK-03 and CHECK-04 both PASS, exit 0 |
| 6 | SC4 (second half) — the five elements hidden only by `.hidden` are still correctly hidden **in the browser** (实检) | ✓ VERIFIED *(was ⚠️ PRESENT_BEHAVIOR_UNVERIFIED)* | Behavioral test at HEAD: `scripts/check-05-ui-uat.py --item 1` → **PASS, 45 assertions, 0 FAIL / 0 BLOCKED**. Matrix 6 elements × 5 states = 30 cells; 9 elements force-`classList.add("hidden")` → all `display === "none"` (including the three 1-0-0 competitors `#selection-menu` / `#annotations-panel` / `#checks-panel`); reverse evidence: 6 elements become visible again when `.hidden` is removed. This is exactly the step CHECK-03 cannot see (rule text unique ≠ rule still wins the cascade) |
| 7 | SC5 — CHECK-01/02/03/04 run independently and each returns an explicit PASS/FAIL | ✓ VERIFIED | All four run standalone from the repo root and print `PASS` / exit 0 on the real tree. Each was independently mutated in a sandbox at HEAD and **failed** (all exit 1): CHECK-01 (bare hex → `FAIL: 1 bare hex outside the token block`; `var(--radix-gray-11)` outside the fence → `FAIL: 1 tier-1 primitive reference(s) outside the fence`; missing file → `FAIL: frontend/style.css not found`); CHECK-02 (unknown token → `FAIL: unknown token --gray-25x`; AA regression `--radix-gray-11: #8f8f8f` → `FAIL: 8 failures`; inversion → `FAIL: hierarchy inverted`; malformed entry → `FAIL: 43 '/* PAIR' markers but only 42 parsed — malformed manifest entry`; empty manifest → `FAIL: manifest coverage 0 pairs (0 TEXT / 0 NON-TEXT) below floor 24/20/4`); CHECK-03 (indented duplicate → `FAIL: expected 1 '.hidden {' rule, found 2`); CHECK-04 (second declaration → `FAIL: expected 1 '!important;' declaration, found 2`). No guard passes vacuously |
| 8 | TOKEN-02 hard invariant — tier-1 primitive names never appear outside the fence, mechanically gated | ✓ VERIFIED | Fence-filtered `grep -oE 'var\(--(white\|black\|gray\|green\|blue\|amber\|red\|purple\|radix)(-[0-9]+)?'` → **0**. CHECK-01's alternation was widened to cover `radix` in 04.1-02; the mutation above proves the widened form is not vacuous |
| 9 | TOKEN-01 / TOKEN-03 — single `:root` block, two-layer taxonomy, meaning inventory precedes the tokens | ✓ VERIFIED | One `:root` (L6) holding **108** declarations, no duplicates: 25 tier-1 (24 `--radix-*` + `--white`) + 47 `--color-*` tier-2 + 37 non-colour. Six action families present and consumed (`routine` / `commit` / `irreversible` / `primary` / `danger` / `warning`, L125-142). `04-UI-SPEC.md:351` `### Meaning inventory (produced **before** the tokens — TOKEN-03)` exists and is consumed. *(Temporal "inventory before tokens" is a process claim no command can re-verify — flagged assumption #3; the inventory exists and is consumed.)* |
| 10 | TOKEN-05 / TOKEN-06 / TOKEN-07 / TOKEN-08 — non-colour scales declared and consumed with **zero residual literals** outside the fence | ✗ FAILED | TOKEN-05 ✓ (12 `--space-*`: 1/2/4/6/8/10/12/14/16/24/32/40, all consumed, 0 residual `padding`/`margin`/`gap` px). TOKEN-06 ✓ structurally (4 `--radius-*`: 8/10/28/999, 0 residual radius px; values superseded by qrq). TOKEN-07 ✓ (4 `--z-*` 10/20/100/200, ordering asserted in-fence L229-231, all four consumed at L537/590/606/889, 0 bare z-index). **TOKEN-08 ✗** — 5 `--text-*` (12/14/16/18/24) and `12.5px` = 0, but `frontend/style.css:434` `.collapse-indicator { font-size: 20px; line-height: 1; }` is a **bare literal outside the fence** in the `--text-*` / `--lh-*` families. Outside-fence `font-size: …px` count = **1** (was 0 at `0c658aa`); non-`var()` `line-height` count = **1**. Violates the goal clause 「全部字面量被替换为 `var()`」 and `04-UI-SPEC.md:841` §Literal exceptions ("the complete list — nothing else may be a literal"). See Gaps |
| 11 | A11Y-04 — the four named text-contrast failures are fixed at declaration time | ✓ VERIFIED | `.hint` 2.73 → `--color-text-muted` on `--color-surface` **5.62**; `#pending-count` / `.badge-pending` 3.03 → `--color-action-warning` on `--color-surface-warning` **10.93**; `.event-kind` 3.25 → `--color-kind-fg` on `--color-kind-default` **5.92**; `.chat-user` 4.14 → `--color-text` on `--color-surface-user` **13.30**. Each pair is in the fence manifest and computed by CHECK-02; the consumers are read live in the browser by UAT item 3 |
| 12 | A11Y-04b — all four non-`:disabled` opacity sites ruled, none silently changed | ✓ VERIFIED | At HEAD there is exactly **1** non-`:disabled` `opacity` declaration: `#rounds-placeholder.archive-mode #round-doc { opacity: 0.75 }` (L1037, kept). `.annotation-answered { opacity: 0.65 }` deleted → replaced by the 0-2-0 descendant rule at L1045-1048; `#round-doc.round-frozen` (L917-920) `opacity` removed → `filter: saturate(0.6)` + `box-shadow: inset 3px 0 0 var(--color-action-warning)` (S-4); `.tier-desc`'s `opacity` removed entirely by 04.1 R-3 (L972). The 8 `:disabled` opacities (6×0.55, 2×0.5) survive verbatim at L656/668/884/935/947/961/1005/1034 |
| 13 | `#confirm-error` keeps its 1-0-0 ID selector and danger colour; `#stream-banner.fatal` stays an independent selector | ✓ VERIFIED | `style.css:960` `#confirm-error { color: var(--color-action-danger); }`; `style.css:608` `#stream-banner.fatal { background: var(--color-surface-danger); color: var(--color-action-danger); border-color: var(--color-border-danger-subtle); }` |
| 14 | `app.js` / `index.html` / `frontend/vendor/` untouched; pytest baseline held | ✓ VERIFIED | `git diff --name-only f912c1a 0c658aa -- frontend/app.js frontend/index.html` → **empty** (Phase 4's own range). *(At HEAD both files differ from `f912c1a`, by later signed-off work only: `33bbd7d` qrq IA swap and `1d849b1` `#session-panel` gate fix — see Notes.)* `git status --porcelain -- frontend/` → empty; `ls frontend/vendor/` → `marked.min.js`; `.venv/bin/python -m pytest -q` → **219 passed, 6 skipped** (matches baseline) |
| 15 | Plan 01/02 backstop — a frozen round renders with the amber inset rule, the historical switcher entry, and readable body text | ✓ VERIFIED *(was ⚠️ PRESENT_BEHAVIOR_UNVERIFIED)* | Behavioral test at HEAD: `scripts/check-05-ui-uat.py --item 2` → **PASS, 5 assertions, 0 FAIL / 0 BLOCKED**. `#round-doc` classList contains `round-frozen`; computed `box-shadow` = `rgb(79, 52, 34) 3px 0px 0px 0px inset` (semantic parse: inset ✓ / x=3px ✓ / y=0 / blur=0 / spread=0 / colour == runtime-resolved `--color-action-warning` = `rgb(79, 52, 34)` ✓); `opacity` = `1`; `filter` = `saturate(0.6)`; body contrast **15.48:1** (threshold 4.5) |

**Score:** 14/15 truths verified (0 present-but-behavior-unverified)

### Required Artifacts

| Artifact | Expected | Status | Details |
| --- | --- | --- | --- |
| `frontend/style.css` | Fenced `:root` block + all literals → `var()` | ⚠️ HOLLOW (one site) | 1054 lines; fence L5-343; 0 bare hex / 0 tier-1 leaks outside; 0 residual px literals for spacing / radius / z-index; **1 residual `font-size` + 1 residual `line-height`** at L434 |
| `scripts/check-01-token-conformance.sh` | CHECK-01 bare-hex + tier-1 gate | ✓ VERIFIED | 49 lines; asserts input exists, asserts exactly 1 START/1 END, counts occurrences; FAILs on all three mutations tested at HEAD |
| `scripts/check-02-contrast.py` | CHECK-02 WCAG checker | ✓ VERIFIED | 239 lines; stdlib only (`re`, `sys`); coverage floors 24/20/4; raw-vs-parsed marker reconciliation; α compositing; strict ORDER. FAILs on all five mutations tested at HEAD |
| `scripts/check-03-hidden-uniqueness.sh` | CHECK-03 `.hidden` uniqueness | ✓ VERIFIED | 17 lines; indentation-tolerant pattern; FAILs on an indented duplicate |
| `scripts/check-04-important-count.sh` | CHECK-04 declaration count | ✓ VERIFIED | 17 lines; counts `!important;` occurrences; FAILs on a second declaration |
| `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` | Written design contract | ✓ VERIFIED | 89 KB; Meaning inventory (L351), Tier 1/2 tables, Contrast Verification, Deliberate Delta Ledger, Global Hard Rules, Do-Not-Touch List, Sign-Off Items (S-1…S-4), Literal exceptions (L841), the four command specs, Not-in-v1.14 fence |

### Key Link Verification

| From | To | Via | Status | Details |
| --- | --- | --- | --- | --- |
| Every `var(--x)` outside the fence | A declared `--x` inside the fence | Gate 2 `comm -23` (consumed minus declared) | ✓ WIRED | Empty output — no silent `var()` unset. No `var(--x, #fallback)` anywhere (`grep -cE 'var\(--[a-z0-9-]+,'` → 0) |
| `scripts/check-01-token-conformance.sh` | the two fence comments in `style.css` | awk fence state machine + START/END count assertion | ✓ WIRED | Correctly excludes in-fence literals; proven by mutation (bare hex outside → FAIL) |
| `scripts/check-02-contrast.py` | the fenced PAIR/ORDER manifest + token declarations | regex over the fence text | ✓ WIRED | 43 pairs (34 TEXT + 9 NON-TEXT) + 1 ORDER parsed; drift fails loudly (`unknown token` / `malformed manifest entry` / `coverage below floor` all reproduced) |
| `#confirm-error` | `--color-action-danger` | 1-0-0 ID specificity over `.hint` 0-1-0 | ✓ WIRED | L960 |
| `#round-doc.round-frozen` | `--color-action-warning` | `box-shadow: inset` (zero layout shift) | ✓ WIRED | L919; read live in the browser by UAT item 2 |
| the four `--z-*` tokens | their four consumers | `z-index: var(--z-*)` | ✓ WIRED | L537 overlay / L590 badge / L606 banner / L889 selection-menu; UAT item 4 reads badge 10 / banner 20 / selection-menu 200 off the real DOM (not just the in-fence comment) |
| `--doc-panel-w` | `#doc-panel` | `flex: 0 0 var(--doc-panel-w)` | ✓ WIRED | L381 (added post-phase by qrq; recorded here because the fence now carries it) |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| --- | --- | --- | --- | --- |
| `frontend/style.css` | every colour / space / type / radius / z token | `:root` fence declarations (primitives → semantic) | Yes — each `var()` resolves to a primitive declared in the fence; Gate 2 empty | ✓ FLOWING |
| `scripts/check-02-contrast.py` | 43 manifest pairs | fence text, resolved through `var()` chains | Yes — 43 `PASS` lines with computed ratios; `ORDER 0.363` | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| --- | --- | --- | --- |
| CHECK-01 passes on the tree | `bash scripts/check-01-token-conformance.sh` | `PASS`, exit 0 | ✓ PASS |
| CHECK-02 passes on the tree | `python3 scripts/check-02-contrast.py` | `PASS: 0 failures` + `ORDER 0.363`, 43 pairs, exit 0 | ✓ PASS |
| CHECK-03 passes on the tree | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS`, exit 0 | ✓ PASS |
| CHECK-04 passes on the tree | `bash scripts/check-04-important-count.sh` | `PASS`, exit 0 | ✓ PASS |
| Guards can actually fail | sandbox mutation per guard (10 mutations at HEAD) | every guard produced exit 1 + an explicit `FAIL` line | ✓ PASS |
| SC4 second half is a real cascade outcome | `.venv/bin/python scripts/check-05-ui-uat.py --item 1` | `PASS`, 45 assertions, 0 FAIL / 0 BLOCKED | ✓ PASS |
| Frozen-round backstop | `.venv/bin/python scripts/check-05-ui-uat.py --item 2` | `PASS`, 5 assertions, 0 FAIL / 0 BLOCKED | ✓ PASS |
| Consumer wiring (Plan 01/02/03 spot-checks) | `.venv/bin/python scripts/check-05-ui-uat.py --item 3,4,6` | `PASS` 15 / 24 / 2 assertions, 0 FAIL / 0 BLOCKED | ✓ PASS |
| Outside-fence bare hex | fence-filtered `grep -o '#[0-9a-fA-F]\{3,6\}' \| wc -l` | `0` | ✓ PASS |
| Fence-external tier-1 leak | fence-filtered `grep -oE 'var\(--(white\|…\|radix)(-[0-9]+)?' \| wc -l` | `0` | ✓ PASS |
| Gate 2 | `comm -23 <(var() names) <(declared names)` | empty | ✓ PASS |
| Outside-fence `font-size: …px` | fence-filtered `grep -nE 'font-size:[^;]*[0-9.]+px'` | **1** (`style.css:434`) — expected 0 | ✗ FAIL |
| Outside-fence non-`var()` `line-height` | fence-filtered `grep -nE 'line-height:' \| grep -v 'var(--lh'` | **1** (`style.css:434`) — expected 0 | ✗ FAIL |
| Test baseline | `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped` | ✓ PASS |
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
| TOKEN-03 | 01 | Meaning inventory first, then converge the competing accents | ✓ SATISFIED *(phase evidence; not re-proved by 04.1)* | `04-UI-SPEC.md:351` `### Meaning inventory (produced before the tokens)`; six action families + kind families landed and consumed. **04.1 explicitly did not touch this requirement** — the evidence is Phase 4's own, unchanged. `REQUIREMENTS.md` still marks it `Pending` (bookkeeping, see note below) |
| TOKEN-04 | 01 | Zero bare `#hex` outside the token block | ✓ SATISFIED | 0 outside-fence hex occurrences; CHECK-01 PASS. *(04.1 carried and re-proved.)* |
| TOKEN-05 | 02 | Spacing scale | ✓ SATISFIED (S-1) | 12 `--space-*` steps incl. the five off-base half-steps the user signed off (S-1); all consumed; 0 residual px. **04.1 explicitly did not touch this requirement** |
| TOKEN-06 | 02 | 3-value radius scale | ✓ SATISFIED (S-1-class deviation, values superseded) | Scale present (4 values: `--radius-sm` 8 / `--radius-md` 10 / `--radius-lg` 28 / `--radius-pill` 999); all 8 radii migrated incl. the 2 corner longhands; 0 residual radius px. **The requirement's literal values (`sm` 4px / `md` 6–8px) are not the values at HEAD** — qrq's signed-off reskin moved them (and added `--radius-lg`). **04.1 did not touch this requirement**; I am reporting the value drift, not flipping it on 04.1's evidence |
| TOKEN-07 | 02 | `--z-*` tokens with an asserted ordering | ✓ SATISFIED (PARTIAL — ordering half manual-only) | 4 tokens; ordering assertion comment at L229-231 (badge 10 < banner 20 < overlay 100 < selection-menu 200); 0 bare z-index; all four consumed (L537/590/606/889) and read live off the DOM by UAT item 4. The **ordering half has no mechanical assertion** — the user adjudicated it to manual-only acceptance (`idi-04.1-VALIDATION.md`, `REQUIREMENTS.md:176`), so this is a recorded user ruling, not an unverified gap |
| TOKEN-08 | 02 | Font-size scale; remove `12.5px` (3 sites) and `14px` | ✗ NOT SATISFIED at HEAD | `12.5px` = 0 ✓; but (a) the residual bare `font-size: 20px` (see Gaps) and (b) the scale at HEAD is 12/14/16/18/24 — `14px` is now `--text-base`, the deliberate S-2 sign-off (keeping it preserves the Phase 5 SC5 / Phase 6 SC5 downstream gates), and qrq moved the other steps. **04.1 explicitly did not touch this requirement**; the `20px` residual predates 04.1 |
| CHECK-01 | 01 | Token-conformance script | ✓ SATISFIED | Present, runs standalone, PASSes on the tree, FAILs on 3 mutations at HEAD. *(04.1 substantially closed — the tier-1 alternation was widened and mutation-proved.)* |
| CHECK-02 | 03 | Contrast-check script | ✓ SATISFIED | Present, stdlib-only, PASSes on the tree (43 pairs), FAILs on 5 mutations at HEAD. *(04.1 substantially closed — the 43-pair manifest was recomputed and the four hard-failure paths re-proved.)* |
| CHECK-03 | 01 | `.hidden` uniqueness guard | ✓ SATISFIED | Present, PASSes, FAILs on an indented duplicate. *(04.1 carried and re-proved.)* |
| CHECK-04 | 01 | `!important` count = 1 | ✓ SATISFIED | Present, PASSes, FAILs on a second declaration. *(04.1 carried and re-proved.)* |
| A11Y-04 | 01 (+03) | All AA text failures fixed at declaration | ✓ SATISFIED | Four named failures now 5.62 / 10.93 / 5.92 / 13.30; manifest verifies all grounds. *(04.1 substantially closed — the 3.23:1 `--color-text-muted` regression window was eliminated.)* |
| A11Y-04b | 01 + 02 (+03) | Opacity-composite failures covered | ✓ SATISFIED | Exactly 1 non-`:disabled` opacity site remains (archive 0.75); the other three ruled; 8 `:disabled` preserved. *(04.1 substantially closed — R-3 removed the `.tier-desc` opacity overreach.)* |

**Orphaned requirements:** none — `REQUIREMENTS.md` maps all 14 IDs to Phase 4, and all 14 appear in a plan's `requirements:` frontmatter (01: TOKEN-01…04, A11Y-04, CHECK-01/03/04; 02: TOKEN-05…08, A11Y-04b; 03: CHECK-02, A11Y-04, A11Y-04b).

**Note on `REQUIREMENTS.md` bookkeeping (recorded, not resolved here):** the traceability table marks TOKEN-03 / TOKEN-05 / TOKEN-06 / TOKEN-08 `Pending` while the old verification claimed all 14 `SATISFIED`. The table's `Complete` set is exactly `idi-04.1-radix`'s own requirement list (TOKEN-01/02/04/07, CHECK-01…04, A11Y-04/04b) — i.e. it reflects what 04.1's `phase.complete` flipped, not a fresh assessment of Phase 4. The four `Pending` rows were created `Pending` at `52b714b` and never changed. My own reading of the codebase is in the table above; the two documents disagree and that disagreement is itself the finding. This is a bookkeeping item for the orchestrator/user, not a Phase 4 execution gap.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| --- | --- | --- | --- | --- |
| — | — | No `TBD` / `FIXME` / `XXX` / `TODO` / `HACK` / `PLACEHOLDER` in `style.css` or the four scripts | — | None |
| — | — | No stubs, empty returns, or hardcoded-empty values in the deliverable (it is CSS + zero-dependency guards) | — | None |
| — | — | Prohibitions clean: 0 `@layer`, 0 `@property`, 0 `:where(`, 0 tokenized `display`, 0 `var()` fallbacks, 0 `rgba(` outside the fence | — | None |
| `frontend/style.css` | 434 | Bare `font-size: 20px` + bare `line-height: 1` outside the fence | 🛑 Blocker | The goal clause 「全部字面量被替换为 `var()`」 and the UI-SPEC's literal-exception contract do not hold. See Gaps |

### Notes on the phase's honest record (verified, not defects)

- **The failed must-have is not Phase 4's work.** `.collapse-indicator { font-size: 20px; line-height: 1; }` was added by quick task `260918-qrq` (`3684353`, 2026-09-18 20:01), i.e. ~20 hours **after** the phase's close commit `0c658aa` (2026-09-18 00:11). At `0c658aa` the rule does not exist and the outside-fence `font-size: …px` count is 0. The qrq plan wrote the literal verbatim (`260918-qrq-PLAN.md:359`), and `idi-04.1-UI-REVIEW.md` later scored it ("`20px` (`.collapse-indicator`) is an undeclared 6th size", Pillar 4 = 3/4) without turning it into a gap. Phase 4 delivered exactly its enumerated baseline scope.
- **WR-04 resolved by `81ae6fd`.** `idi-04-REVIEW.md` (6 Critical / 4 Warning / 5 Info) and `idi-04-REVIEW-FIX.md` (9 fixed, 1 skipped) are part of the phase's record. The tree now carries the corrected `.tier-desc` rule (L972) — note that 04.1's R-3 later removed its `opacity` entirely, so the manifest pair `--color-action-primary-fg ON --color-action-primary TEXT@0.9` = 5.08 is no longer needed and is absent from the 43-pair manifest. The UI-SPEC E6 ruling is corrected at both `04-UI-SPEC.md:689` and `:1040`. These are dated, attributed corrections, not inconsistencies.
- **The pair-count arithmetic has three numbers in circulation (24 / 34 / 43), and 43 is the landed figure.** `ROADMAP.md` Phase 4 says 24 (20 TEXT + 4 NON-TEXT) — the figure at plan-freeze time; the disk carried 34 (29 TEXT + 5 NON-TEXT) before 04.1; 04.1 recomputed to **43 (34 TEXT + 9 NON-TEXT) + 1 ORDER**, which is what CHECK-02 parses at HEAD. D-15's ruling is "re-enumerate by what actually landed"; 24 and 34 are historical values retained for comparison, not deviations. *(The ROADMAP plan-03 line still reads "20 文本 + 4 非文本" — stale prose, not a shortfall.)*
- **`--green-800` is gone and `--fw-medium` is now legitimate.** The old report noted `--green-800` as the one admitted unconsumed primitive (N-2) and `--fw-medium` as intentionally undeclared (Q4). At HEAD neither holds: `--green-800` no longer exists in the fence, and `--fw-medium: 500` **is** declared and consumed 4× (L408/432/469/766). Hard Rule 5 ("never declare a token you are not consuming") is therefore satisfied for it. `--fw-*` is now 3 tokens, not 2.
- **`app.js` / `index.html` are changed at HEAD, but not by Phase 4.** Phase 4's own range is clean (`git diff --name-only f912c1a 0c658aa` → empty). The changes come from `33bbd7d` / `253d4d3` (qrq IA swap) and `1d849b1` (`#session-panel` gate fix). The phase's zero-touch criterion was satisfied by the phase; the file-level invariant was later superseded by signed-off work.
- **SC2's invariant is also superseded at HEAD.** qrq deliberately renamed `#sidebar`→`#doc-panel`, `#doc-pane`→`#doc-panel-body`, `--sidebar-w`→`--doc-panel-w` and added `:has()` empty-state rules. SC2 ("no existing selector changed position or name") was a Phase 4 success criterion and held for Phase 4's own change; it is not a perpetual invariant and later signed-off work is not bound by it.
- **`idi-04-01-SUMMARY.md`'s wording "exactly one added line — `:root {`"** is imprecise: against `f912c1a` the tree also adds the `.annotation-answered` descendant rule and removes `.annotation-answered`, and Plan 02 later adds `button, input, select`. All three are documented in the plans' own ledgers, so SC2 still holds — this is a SUMMARY-wording inaccuracy, not a goal failure. Recorded as info, not a gap.
- **IN-05 (Info, out of scope):** `check-02-contrast.py` exits 1 via an uncaught `FileNotFoundError` traceback when `frontend/style.css` is missing rather than a clean `FAIL` line. Non-blocking — the exit code is still non-zero and the real-tree path is guarded by CHECK-01's own input assertion.
- **Stale INFO string inside the harness (cosmetic, not a defect):** `check-05-ui-uat.py`'s item-2 diagnostic still prints "`--color-text-muted` 在 260918-qrq 换肤后由 #6a6a6a 变为 #8f8f8f,低于 AA 4.5:1". At HEAD `--color-text-muted` = `rgb(100, 100, 100)` and the blockquote ratio it prints is **5.62** (passing). The line is a leftover note; the assertions around it are correct.
- **Temporal assumption #3 (flagged, not re-verifiable):** TOKEN-03's "meaning inventory produced **before** the tokens" is a process claim. No command can re-verify the ordering in which a human produced two documents. The inventory exists (`04-UI-SPEC.md:351`) and is consumed by the landed tokens; the temporal half is taken on the record.
- **Recorded downstream items, not Phase 4 gaps:** (a) `#confirm-error` carries `class="hint hidden"` and computes 16px while every other `.hint` computes 14px — same class, two sizes (`.overlay-card p` 0-1-1 beats `.hint` 0-1-0); recorded in `idi-04.1-UI-REVIEW.md` Pillar 4, a typography item for Phase 5. (b) TOKEN-07's ordering half is manual-only by user ruling.

### Disclosed limitations (accepted, not silently dropped)

1. **UAT test 5's two AI-dependent interaction smokes were not re-run at HEAD.** The default harness run gives `item 5: BLOCKED (9 assertions, 0 FAIL, 2 BLOCKED)` and overall `exit=2`. This is by design: the harness's exit contract is `code = 1 if any_fail else (2 if any_blocked else 0)`, and the two `blocked()` calls exist precisely so that "runtime verification claimed rather than performed" stays visible (T-idi041-09). `idi-04-UAT.md` §Test 5 records them as **run and PASSED** under `--ai-smoke` (claude CLI available), with the two real interactions described; the user has explicitly declined a re-run. This report therefore accepts the recorded UAT evidence for those two smokes and records the non-re-run as a disclosed limitation. It does **not** treat the default run's `exit=2` / 2 BLOCKED as a defect.
2. **Keyboard text selection cannot be automated** in this environment (`Shift+ArrowRight` leaves `window.getSelection()` empty in `<p>`, `tabindex` containers and `contenteditable`; `--enable-caret-browsing` does not help). None of this phase's six UAT items depends on it.
3. **指纹在复核之后被重算过一次 —— 如实披露。** 验证代理算 `covered_digest` 之后,编排者又做了两次**记账性**编辑:(a) `idi-04-UAT.md` 的 frontmatter `status: resolved → complete`(归一到 UAT 模板的合法取值)加一段说明;(b) `phase.complete` 依本报告的 `passed` 翻转了 `REQUIREMENTS.md` 里 **Phase 4 自己的**需求行(TOKEN-03/05/06 → `Complete`,TOKEN-08 → `Complete (PARTIAL — …)`,后者刻意不写成无保留的 `Complete`,以与本报告的 `overrides:` 一致)。这两个文件都在本报告的 `covered_files` 内,而指纹是原始字节 sha256,故记录值随之失效。**逐文件核对确认:本次唯二被改的 covered file 就是这两个**(`git status --porcelain` 显示 `frontend/style.css` 与 `scripts/` 全部未动,其余 covered 文件未动)。**没有任何被核验的事实随之移动** —— 14/15 的判定、全部数值、四条守卫、pytest 基线、`app.js`/`index.html` 零改动面均不受影响。指纹因此按**编辑后**的内容重算一次写回,而非保留一个已知过期的值。这**不是**把一次真实内容变更盖掉:`idi-04.1-radix` 改写 `style.css` 的那次内容变更走的是**重新验证**(本报告取代了旧报告),两次处置方向相反、各自留证。

   **结构性观察(留给后续阶段裁决,不在本次单方面改动):** `.planning/REQUIREMENTS.md` 同时在本报告与 `idi-04.1-VERIFICATION.md` 的 `covered_files` 里,而 `phase.complete` **每次收口都会改它**。这意味着**任何一次阶段收口都会让此前所有覆盖了该文件的报告同时转为 stale** —— 本阶段收口时就同时打掉了 idi-04 与 idi-04.1 两份。`covered_files` 的语义应是「其变更足以使本报告的结论失效的输入」,而需求索引表是**下游记账**,不是这样的输入。建议后续阶段考虑把它移出 `covered_files`(或让 `phase.complete` 的翻转不参与指纹),否则每次收口都要重算一次历史报告的指纹。

### Carry-forward obligations (out of scope — NOT rewritten by this report)

1. **C-1 downstream-gate reference audit — measured false at HEAD, deliberately not corrected here.** Real-browser measurement (reproduced at HEAD by UAT item 4): `#brainstorm-view h2` computes to **`16px`** with colour `--color-action-warning` = **`#4f3422`**. Static basis: `frontend/style.css:679-683` uses `font-size: var(--text-md)` and `color: var(--color-action-warning)`; in-fence `--text-md: 16px` (L207) and `--radix-amber-12: #4f3422` (L66). **Six sites still assert `14px` / `#8a6508`** (five in `.planning/ROADMAP.md` — hard-rule-3 prose, Phase 5 Pitfall 9, §Phase 5 Gates, §Phase 6 SC5, §Phase 6 Gates — plus `04-UI-SPEC.md` carry-forward #7). `idi-04-UAT.md` §Carry-Forward ① records the same six sites and the one-line correction (`14px` → `16px`, `#8a6508` → `#4f3422`). Those are **future phases' signed-off gates**; per the phase's own prohibition, this report does **not** rewrite them. User adjudication required.
2. **Carry-forward #8 — Phase 7's focus ring must be re-measured on the new grounds.** `--color-focus` (Phase 4's ring colour) was originally measured against `#fafafa`; the grounds are now `--color-surface` `#f9f9f9` and `--color-surface-page` `#fcfcfc`. Phase 7 must re-measure ≥ 3:1 on both. This phase neither changes the ring colour nor performs that measurement.
3. **`idi-04.1-UI-REVIEW.md`'s own open findings** (destructive buttons painting a blue border on a red fill; no focus indicator on filled buttons; no hover feedback on filled buttons) are that sub-phase's record, outside this phase's scope.

### Human Verification Required

None outstanding. The six items the previous report routed to human verification are all resolved by `idi-04-UAT.md` (6/6 `pass`) and were reproduced at HEAD where the environment permits — items 1, 2, 3, 4 and 6 were re-run by this verification and by the orchestrator (`0 FAIL` on every one); item 5's two AI-dependent smokes carry the recorded `--ai-smoke` evidence and the disclosed non-re-run (see Disclosed limitations).

### Gaps Summary

**一条失败项 —— 已由用户裁定为 Phase 4 范围外,故本报告 status 为 `passed`。** 阶段 goal 的「全部字面量被替换为 `var()`」这一条在 HEAD 上不成立:`frontend/style.css:434` 携带 `.collapse-indicator { font-size: 20px; line-height: 1; }` —— 围栏外的两个裸字面量,属阶段已令牌化的 `--text-*` / `--lh-*` 族,且在 UI-SPEC 的封闭例外清单之外。阶段其余全部目标都在树上得到验证: the single fenced `:root` block is correctly placed, outside-fence bare hex and tier-1 leaks are zero, all colour / space / radius / z-index / weight literals are migrated, Gate 2 is empty, all four guard commands run independently and each was proven able to fail at HEAD, the A11Y-04 / A11Y-04b fixes are in place with the AA values chosen at declaration time, `app.js` / `index.html` were untouched by the phase, and the pytest baseline held.

The gap is small and precisely attributable: it was introduced **after** the phase closed, by a signed-off quick task (`260918-qrq` / `3684353`), it is already recorded in `idi-04.1-UI-REVIEW.md`, and no later milestone phase claims it (Phase 5's Deliverables name `.markdown-body h1/h2/h3`, `#doc-pane > h1` and the `code` 12.5px fold — not `.collapse-indicator`'s font-size). It is nonetheless a live hole: the declared type scale is 12/14/16/18/24, so `20px` is off-scale in shipped chrome, and the phase's contract explicitly says nothing else may be a literal.

**裁定(用户,2026-09-20):记为 Phase 4 范围外,并指派去向。** 理由:该字面量由阶段**收口之后**的已签核 quick 任务引入,Phase 4 自己的提交区间干净且已交付其枚举基线范围。裁定以 frontmatter 的 `overrides:` 条目落证(`accepted_by: Jack11111eee`),**不是**静默放过 —— 该发现同时保留在本节、`gaps:` 块、以及 `idi-04.1-UI-REVIEW.md` Pillar 4。

**去向已落定,不留悬空:** 记入 `.planning/ROADMAP.md` 的 `## Backlog` 停车位 **`999.1`**,连同同一处携带的另一条 cosmetic 项 —— `scripts/check-05-ui-uat.py:588` 那条陈旧诊断文案(仍打印「`--color-text-muted` … 变为 #8f8f8f,低于 AA 4.5:1」,而 HEAD 实为 `rgb(100,100,100)` / 5.62 达标)。两项都待 `/gsd-review-backlog` 提升。

**为什么没写进 Phase 5(已核):** Phase 5 的 Pitfall 7 把触碰 `.collapse-indicator` 的范围**锁死为两处 `content:` emoji**,其 SC1 也只点名四处 chrome 覆盖。往 Phase 5 插一条新交付物等于改写一个**已签核的门** —— 正是 `idi-04-UAT.md` 携带项①刻意拒绝单方面做的事。

**为什么没有当场修掉(已核):** `20px` 不在 HEAD 的刻度上(12/14/16/18/24),修法本身是排版决策而非机械替换(加档 / 重映射 / 加 L-6 例外);且任何对 `frontend/style.css` 的编辑都会作废 `idi-04.1-radix` 的 `passed` 指纹(其 `covered_files` 含该文件,digest 为原始字节 sha256)。两条都属用户裁决面,故不在本报告内单方面执行。

---

_Verified: 2026-09-20_
_Verifier: Claude (gsd-verifier)_
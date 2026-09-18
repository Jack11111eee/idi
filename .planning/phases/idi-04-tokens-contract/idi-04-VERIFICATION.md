---
phase: idi-04-tokens-contract
verified: 2026-09-18T00:00:00Z
status: human_needed
score: 13/15 must-haves verified
covered_files:
  - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md
  - .planning/phases/idi-04-tokens-contract/idi-04-01-PLAN.md
  - .planning/phases/idi-04-tokens-contract/idi-04-01-SUMMARY.md
  - .planning/phases/idi-04-tokens-contract/idi-04-02-PLAN.md
  - .planning/phases/idi-04-tokens-contract/idi-04-02-SUMMARY.md
  - .planning/phases/idi-04-tokens-contract/idi-04-03-PLAN.md
  - .planning/phases/idi-04-tokens-contract/idi-04-03-SUMMARY.md
  - frontend/style.css
  - scripts/check-01-token-conformance.sh
  - scripts/check-02-contrast.py
  - scripts/check-03-hidden-uniqueness.sh
  - scripts/check-04-important-count.sh
covered_digest: "v1:sha256:f4dd04b61176ae0346e443ba470ff9c94228fa7c2d3b8964637421e62f7d8431"
behavior_unverified: 2
overrides_applied: 0
behavior_unverified_items:
  - truth: "ROADMAP SC4 (second half): the five elements hidden only by `.hidden` (#draft-empty / #rounds-hint / #btn-process-round / #round-switcher / #writing-hint) are still correctly hidden in the browser — 实检, not read from CSS"
    test: "Launch the app, open each of the five elements' views, and confirm the element is not rendered (display: none wins the cascade against the 1-0-0 competitors #selection-menu / #annotations-panel / #checks-panel)."
    expected: "None of the five elements is visible in any state; the three ID-specificity containers still hide when `.hidden` is applied."
    why_human: "This is a cascade/rendering outcome. CHECK-03 proves only that the rule text is unique, not that it still wins. Headless rendering is blocked in this environment and screenshots are unavailable."
  - truth: "Plan 01/02 backstop truth: in a running app, a frozen (historical) round shows an amber inset left rule, the round switcher shows the historical round, and the body text is readable (computed contrast >= 4.5:1)"
    test: "Open a historical frozen round in the running app; read `#round-doc` computed `box-shadow` / `filter` / `opacity` and the body text contrast."
    expected: "`box-shadow` contains `inset 3px 0 0 rgb(138, 101, 8)`; `opacity` is 1; `filter: saturate(0.6)`; body text >= 4.5:1."
    why_human: "`verification: backstop` truth — presence and wiring never qualify. No held-out or property test exercises it, and the environment cannot render. Per the plan, unconfirmable routes to `human_needed` (insufficient_spec), never a silent pass."
human_verification:
  - test: "DevTools Computed spot-checks carried from Plan 01 (13 pending) — `.hint` color = rgb(106,106,106); `.badge-answered` color = rgb(106,106,106); `#btn-authorize` color/border-color/background-color = rgb(38,117,74)/rgb(38,117,74)/rgb(233,247,239); `#btn-process-round` byte-identical to `#btn-authorize`; `.kind-write .event-kind` background = rgb(38,117,74); `.kind-done .event-kind` background = rgb(0,0,0); `#ai-route-select` border-top-color = rgb(138,138,138); `#selection-menu` border-top-color = rgb(138,138,138); `#stream-banner` border-top-color = rgb(138,101,8); `#state-badge` color/background = rgb(31,99,189)/rgb(238,244,255); `.chat-user` background = rgb(31,99,189); `.overlay-card` box-shadow contains rgba(0,0,0,0.2)."
    expected: "Each named property reads the value the manifest/token layer asserts."
    why_human: "DevTools computed-style readings. Screenshots unavailable and headless rendering blocked; the app's persistent /api/events SSE stream prevents capture termination."
  - test: "DevTools Computed spot-checks carried from Plan 02 (16 pending) — spacing values (.panel-header 10px/16px, #doc-pane 32px/40px, button 6px/10px, .overlay-card 24px snapped from 28px, #brainstorm-view 24px snapped from 22px); font sizes (#brainstorm-view h2 14px + rgb(138,101,8), #draft-view h2 15px, .panel-header h2 14px, .overlay-card h3 16px, .markdown-body 14px, .markdown-body code 13px folded from 12.5px); z-index (#selection-menu 200 / #state-badge 10 / #stream-banner 20); frozen-round box-shadow/opacity/filter; #rounds-placeholder.archive-mode #round-doc opacity 0.75; any button color rgb(26,26,26)."
    expected: "The snapped spacing values match the D-16 ledger; 14px survives as a first-class step so the Phase 5 SC5 / Phase 6 SC5 downstream gates stay satisfiable; z-index ordering holds."
    why_human: "Same as above — computed-style readings only; auto mode auto-approved the gates rather than performing them."
  - test: "DevTools Computed spot-checks carried from Plan 03 (10 pending) — `#ai-route-select` border-top-color/background-color = rgb(138,138,138)/rgb(255,255,255); `.hint` color rgb(106,106,106) on rgb(250,250,250); `#stream-banner` border-top-color rgb(138,101,8); `.markdown-body` color rgb(26,26,26) visibly darker than `.hint` (the observable form of ORDER 0.311); plus one 「处理本轮批注」 and one 「发送」 interaction completing without error."
    expected: "Computed values corroborate the checker's ratios; the muted grey is observably quieter than body text."
    why_human: "Computed-style + interaction smoke; not automatable here."
  - test: "Confirm the CR-06 rendering outcome: on an ordinary answered annotation, the user note and the AI answer body are both now `--color-text-muted` (the intended D-11 intra-item hierarchy)."
    expected: "Both the user note and the answer body render at the muted grey; nothing else in the item is greyed."
    why_human: "REVIEW-FIX CR-06 is a rendering-behaviour change confirmed by inspection only (`app.js:1147` sets `annotation-answer-body`); a syntax/guard check cannot see it."
---

# Phase 4: 设计契约、令牌层与契约校验 Verification Report

**Phase Goal:** `style.css` 拥有一份书面设计契约与单一令牌来源;全部字面量被替换为 `var()`,令牌块之外零裸 `#hex`;四条契约校验命令可独立运行;AA 达标值在**声明处**即选定。
**Verified:** 2026-09-18
**Status:** human_needed
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | SC1 — a single fenced `:root` block sits after `* { box-sizing }` and before `html, body`; outside it `style.css` has zero bare `#hex`, provable by CHECK-01 alone | ✓ VERIFIED | `grep -n ':root'` → exactly one hit at `style.css:6`; fence START at L5, END at L211; `* { box-sizing…` L3 < L5 and `html, body {` L213 > L211. `awk` fence-filtered `grep -o '#[0-9a-fA-F]\{3,6\}' \| wc -l` → **0**; `bash scripts/check-01-token-conformance.sh` → `PASS`, exit 0 |
| 2 | SC2 — pure value substitution: no existing selector changed position or name, and no declaration was added/removed beyond the documented deltas | ✓ VERIFIED | CSS-parsed selector→property diff of `f912c1a:frontend/style.css` vs HEAD: removed `.annotation-answered` (D-11); added `:root` (TOKEN-01), `.annotation-answered .annotation-note/.annotation-quote/.annotation-answer-body/.annotation-answer summary` (D-11 + CR-06), `input`/`select` (N-4); property-set changes only on `button` (+`color`, N-4) and `#round-doc.round-frozen` (−`opacity`, +`box-shadow`, S-4). Relative selector order **identical** |
| 3 | SC3 (ratio half) — every gate-hint text still reaches WCAG AA on each ground it lands on | ✓ VERIFIED | Manifest pair `--color-text-muted ON --gray-25` = **5.18**; on `--white` 5.41; on `--gray-50` 4.96; on `--gray-100` 4.66 — all >= 4.5. `--color-text-muted` = `--gray-600` = `#6a6a6a`, the lightest grey passing on every ground in the file |
| 4 | SC3 (hierarchy half) — the hint stays strictly "quieter" than body text, checked as an ordering, not a re-thresholded ratio | ✓ VERIFIED | `ORDER 0.311  --color-text-muted before --color-text on --gray-25`; the assertion is `q < l` (strict). Mutation `--gray-600: #000000` → all four ratio pairs still PASS (20.12/21.00/19.26/18.10) while `FAIL: hierarchy inverted  1.207 … (need < 1.000)`, exit 1 — correct direction |
| 5 | SC4 (first half) — `.hidden` remains the site's only `!important` declaration, and `^\.hidden {` is exactly 1 | ✓ VERIFIED | `grep -nE '^[[:space:]]*\.hidden[[:space:]]*\{'` → `style.css:225` only; `grep -o '!important;' \| wc -l` → **1** (`grep -c '!important'` → 3, the 2 extra being comment prose at L13-16). CHECK-03 and CHECK-04 both PASS |
| 6 | SC4 (second half) — the five elements hidden only by `.hidden` are still correctly hidden **in the browser** (实检) | ⚠️ PRESENT_BEHAVIOR_UNVERIFIED | The rule text is unique and all five elements exist (`#draft-empty`, `#rounds-hint`, `#btn-process-round`, `#round-switcher`, `#writing-hint` — all present in `index.html` + `app.js`). But cascade/rendering cannot be exercised here — see Human Verification |
| 7 | SC5 — CHECK-01/02/03/04 run independently and each returns an explicit PASS/FAIL | ✓ VERIFIED | All four run standalone from the repo root and print `PASS` / exit 0 on the real tree. Each was independently mutated in a sandbox and **failed**: CHECK-01 (bare hex → `FAIL: 1 bare hex…`; tier-1 leak → `FAIL: 2 tier-1 primitive reference(s)…`; renamed END → `FAIL: expected exactly 1 fence START and 1 fence END, found 1/0`; missing file → `FAIL: frontend/style.css not found`); CHECK-02 (empty file → fence FAIL; empty manifest → `FAIL: manifest coverage 0 pairs…`; malformed entry → `FAIL: 34 '/* PAIR' markers but only 33 parsed`; unknown token → `FAIL: unknown token --gray-25x`; hierarchy inversion → FAIL); CHECK-03 (indented duplicate → `FAIL: … found 2`); CHECK-04 (two declarations on one line → `FAIL: … found 3`). No guard passes vacuously |
| 8 | TOKEN-02 hard invariant — tier-1 primitive names never appear outside the fence, mechanically gated | ✓ VERIFIED | Fence-filtered `grep -oE 'var\(--(white\|black\|gray\|green\|blue\|amber\|red\|purple)(-[0-9]+)?'` → **0**; CHECK-01 (WR-03 fix) FAILs on any leak |
| 9 | TOKEN-01 / TOKEN-03 — single `:root` block, two-layer taxonomy, meaning inventory precedes the tokens | ✓ VERIFIED | One `:root` (L6) holding 25 tier-1 primitives + 50 tier-2 tokens (48 `--color-*` + `--shadow-overlay` / `--shadow-menu`) + 31 non-colour tokens = 106 declarations, no duplicates. `04-UI-SPEC.md:351` `### Meaning inventory (produced **before** the tokens — TOKEN-03)` exists and the six action families are present. *(Temporal "inventory before tokens" is a process claim no command can re-verify — flagged assumption #3; the inventory exists and is consumed.)* |
| 10 | TOKEN-05 / TOKEN-06 / TOKEN-07 / TOKEN-08 — non-colour scales declared and consumed with zero residual literals | ✓ VERIFIED | 12 `--space-*` (86 consumers), 6 `--text-*` (11/12/13/14/15/16), 2 `--fw-*`, 3 `--lh-*`, 3 `--radius-*`, 4 `--z-*`, `--sidebar-w`. Fence-external residual counts all **0**: `padding\|margin\|gap … px`, `font-size: …px`, `radius: …px`, `z-index: <n>`, `rgba(`. `12.5px` = 0. z-index ordering asserted in-fence: badge 10 < banner 20 < overlay 100 < selection-menu 200 (L138-143) |
| 11 | A11Y-04 — the four named text-contrast failures are fixed at declaration time | ✓ VERIFIED | `.hint` 2.73 → `--color-text-muted on --gray-25` **5.18**; `#pending-count`/`.badge-pending` 3.03 → `--color-action-warning on --color-surface-warning` **4.96**; `.event-kind` 3.25 → `--color-kind-fg on --color-kind-command` **5.32**; `.chat-user` 4.14 → `--color-text-inverse on --color-surface-info-strong` **5.87** |
| 12 | A11Y-04b — all four non-`:disabled` opacity sites ruled, none silently changed | ✓ VERIFIED | `.annotation-answered { opacity: 0.65 }` deleted, replaced by the 0-2-0 descendant rule at L852-855; `#round-doc.round-frozen` (L723-726) `opacity` removed → `filter: saturate(0.6)` + `box-shadow: inset 3px 0 0 var(--color-action-warning)` (S-4); `.tier-desc` `opacity: 0.9` (L778, corrected from 0.8 by `81ae6fd` → 5.08:1); `#rounds-placeholder.archive-mode #round-doc` `opacity: 0.75` kept (L844). The 8 `:disabled` opacities (6×0.55, 2×0.5) survive verbatim |
| 13 | `#confirm-error` keeps its 1-0-0 ID selector and danger colour; `#stream-banner.fatal` stays an independent selector | ✓ VERIFIED | `style.css:766` `#confirm-error { color: var(--color-action-danger); }`; `style.css:437` `#stream-banner.fatal { background: var(--color-surface-danger); color: var(--color-action-danger); border-color: var(--color-border-danger-subtle); }` |
| 14 | `app.js` / `index.html` / `frontend/vendor/` untouched; pytest baseline held | ✓ VERIFIED | `git diff --name-only f912c1a -- frontend/app.js frontend/index.html` → empty; `ls frontend/vendor/` → `marked.min.js`; `git status --porcelain frontend/` → empty; `.venv/bin/python -m pytest -q` → **219 passed, 6 skipped** (225 collected, matches baseline) |
| 15 | Plan 01/02 backstop — a frozen round renders with the amber inset rule, the historical switcher entry, and readable body text | ⚠️ PRESENT_BEHAVIOR_UNVERIFIED | `verification: backstop` truth. The CSS mechanism is present (`box-shadow: inset 3px 0 0 var(--color-action-warning)`, no `opacity`), but no held-out/property test exercises it and the environment cannot render — see Human Verification |

**Score:** 13/15 truths verified (2 present, behavior-unverified)

### Required Artifacts

| Artifact | Expected | Status | Details |
| --- | --- | --- | --- |
| `frontend/style.css` | Fenced `:root` block + all literals → `var()` | ✓ VERIFIED | 861 lines; fence L5-211; 0 bare hex / 0 tier-1 leaks outside; 0 residual px literals for spacing/type/radius/z-index |
| `scripts/check-01-token-conformance.sh` | CHECK-01 bare-hex + tier-1 gate | ✓ VERIFIED | 46 lines; asserts input exists, asserts exactly 1 START/1 END, counts occurrences; FAILs on all five mutations tested |
| `scripts/check-02-contrast.py` | CHECK-02 WCAG checker | ✓ VERIFIED | 240 lines; stdlib only (`re`, `sys`); coverage floors 24/20/4; raw-vs-parsed marker reconciliation; α compositing; strict ORDER. FAILs on empty file, empty manifest, malformed entry, unknown token, threshold breach, inversion |
| `scripts/check-03-hidden-uniqueness.sh` | CHECK-03 `.hidden` uniqueness | ✓ VERIFIED | 18 lines; indentation-tolerant pattern; FAILs on an indented duplicate |
| `scripts/check-04-important-count.sh` | CHECK-04 declaration count | ✓ VERIFIED | 18 lines; counts `!important;` occurrences; FAILs on a second declaration |
| `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` | Written design contract | ✓ VERIFIED | 89 KB; Meaning inventory, Tier 1/2 tables, Contrast Verification, Deliberate Delta Ledger, Global Hard Rules, Do-Not-Touch List, Sign-Off Items, the four command specs, Not-in-v1.14 fence |

### Key Link Verification

| From | To | Via | Status | Details |
| --- | --- | --- | --- | --- |
| Every `var(--x)` outside the fence | A declared `--x` inside the fence | Gate 2 `comm -23` (consumed minus declared) | ✓ WIRED | Empty output — no silent `var()` unset. No `var(--x, #fallback)` anywhere (`grep -cE 'var\(--[a-z0-9-]+,'` → 0) |
| `scripts/check-01-token-conformance.sh` | the two fence comments in `style.css` | awk fence state machine + START/END count assertion | ✓ WIRED | Correctly excludes in-fence literals; FAILs when END is renamed |
| `scripts/check-02-contrast.py` | the fenced manifest + token declarations | regex over the fence text | ✓ WIRED | 34 pairs / 29 TEXT / 5 NON-TEXT / 1 ORDER parsed; drift fails loudly |
| `#confirm-error` | `--color-action-danger` | 1-0-0 ID specificity over `.hint` 0-1-0 | ✓ WIRED | ID selector retained at L766 |
| `#round-doc.round-frozen` | `--color-action-warning` | `box-shadow: inset` (zero layout shift) | ✓ WIRED | L725 |
| `--black` | `--color-kind-done` (background only) | token chain | ✓ WIRED | `--black` has **no foreground consumer** — the reason the old manifest pair was fictional; corrected by `81ae6fd` |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| --- | --- | --- | --- | --- |
| `frontend/style.css` | every colour/space/type token | `:root` fence declarations (primitives) | Yes — each `var()` resolves to a primitive declared in the fence; Gate 2 empty | ✓ FLOWING |
| `scripts/check-02-contrast.py` | 34 manifest pairs | fence text, resolved through `var()` chains | Yes — 35 PASS lines with computed ratios; `ORDER 0.311` | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| --- | --- | --- | --- |
| CHECK-01 passes on the tree | `bash scripts/check-01-token-conformance.sh` | `PASS`, exit 0 | ✓ PASS |
| CHECK-02 passes on the tree | `python3 scripts/check-02-contrast.py` | `PASS: 0 failures` + `ORDER 0.311`, exit 0 | ✓ PASS |
| CHECK-03 passes on the tree | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS`, exit 0 | ✓ PASS |
| CHECK-04 passes on the tree | `bash scripts/check-04-important-count.sh` | `PASS`, exit 0 | ✓ PASS |
| Guards can actually fail | sandbox mutation per guard (10 mutations) | every guard produced a non-zero exit + explicit `FAIL` | ✓ PASS |
| Outside-fence bare hex | `awk … \| grep -o '#…' \| wc -l` | `0` | ✓ PASS |
| Fence-external tier-1 leak | `awk … \| grep -oE 'var\(--(white\|black\|gray\|…)…' \| wc -l` | `0` | ✓ PASS |
| Gate 2 | `comm -23 <(var() names) <(declared names)` | empty | ✓ PASS |
| Test baseline | `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped` | ✓ PASS |
| app.js / index.html untouched | `git diff --name-only f912c1a -- …` | empty | ✓ PASS |
| Ordering assertion direction | sandbox `--gray-600: #000000` | `FAIL: hierarchy inverted  1.207`, exit 1 | ✓ PASS |

### Probe Execution

Not applicable — the phase declares no `scripts/*/tests/probe-*.sh` and is not a migration/tooling phase. Its four contract-check commands are exercised above.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
| --- | --- | --- | --- | --- |
| TOKEN-01 | 01 | Single `:root` token block, native custom properties, zero build | ✓ SATISFIED | Exactly one `:root` at L6 inside the fence |
| TOKEN-02 | 01 | Two-layer taxonomy; tier-1 names never outside the fence | ✓ SATISFIED | 25 primitives; fence-external primitive refs = 0; gated by CHECK-01 |
| TOKEN-03 | 01 | Meaning inventory first, then converge the competing accents | ✓ SATISFIED | UI-SPEC `### Meaning inventory` (L351); six action families + kind families landed and consumed |
| TOKEN-04 | 01 | Zero bare `#hex` outside the token block | ✓ SATISFIED | 0 outside-fence hex occurrences; CHECK-01 PASS |
| TOKEN-05 | 02 | Spacing scale | ✓ SATISFIED (S-1) | 12 `--space-*` steps incl. the five off-base half-steps the user signed off (S-1); 86 consumers; 0 residual px |
| TOKEN-06 | 02 | 3-value radius scale | ✓ SATISFIED | `--radius-sm` 4 / `--radius-md` 8 / `--radius-pill` 999; all 8 radii migrated incl. the 2 corner longhands |
| TOKEN-07 | 02 | `--z-*` tokens with an asserted ordering | ✓ SATISFIED | 4 tokens; ordering assertion comment at L138-143 (badge 10 < banner 20 < overlay 100 < selection-menu 200); 0 bare z-index |
| TOKEN-08 | 02 | Font-size scale; remove `12.5px` (3 sites) and `14px` | ✓ SATISFIED (S-2 deviation) | 6 `--text-*` steps (11/12/13/14/15/16); `12.5px` = 0. **`14px` was deliberately kept** as a first-class step — the user-approved S-2 sign-off (keeping it preserves the Phase 5 SC5 / Phase 6 SC5 downstream gates). Not a shortfall; a signed deviation from the requirement's literal text |
| CHECK-01 | 01 | Token-conformance script | ✓ SATISFIED | Script present, runs standalone, PASSes on the tree, FAILs on 4 mutations |
| CHECK-02 | 03 | Contrast-check script | ✓ SATISFIED | Script present, stdlib-only, PASSes on the tree, FAILs on 5 mutations |
| CHECK-03 | 01 | `.hidden` uniqueness guard | ✓ SATISFIED | Script present, PASSes, FAILs on an indented duplicate |
| CHECK-04 | 01 | `!important` count = 1 | ✓ SATISFIED | Script present, PASSes, FAILs on a second declaration |
| A11Y-04 | 01 (+03) | All AA text failures fixed at declaration | ✓ SATISFIED | Four named failures now 5.18 / 4.96 / 5.32 / 5.87; manifest verifies all grounds |
| A11Y-04b | 01 + 02 (+03) | Opacity-composite failures covered | ✓ SATISFIED | All four non-`:disabled` sites ruled: 0.65 deleted, round-frozen opacity removed (S-4), `.tier-desc` 0.9 (5.08:1), archive 0.75 kept; 8 `:disabled` preserved |

**Orphaned requirements:** none — REQUIREMENTS.md maps all 14 IDs to Phase 4, and all 14 appear in a plan's `requirements:` frontmatter (01: TOKEN-01…04, A11Y-04, CHECK-01/03/04; 02: TOKEN-05…08, A11Y-04b; 03: CHECK-02, A11Y-04, A11Y-04b).

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| --- | --- | --- | --- | --- |
| — | — | No `TBD` / `FIXME` / `XXX` / `TODO` / `HACK` / `PLACEHOLDER` in `style.css` or the four scripts | — | None |
| — | — | No stubs, empty returns, or hardcoded-empty values in the deliverable (it is CSS + zero-dependency guards) | — | None |
| — | — | Prohibitions clean: 0 `@layer`, 0 `@property`, 0 `:where(`, 0 tokenized `display`, 0 `var()` fallbacks | — | None |

### Notes on the phase's honest record (verified, not defects)

- **WR-04 resolved by `81ae6fd`.** `idi-04-REVIEW.md` (6 Critical / 4 Warning / 5 Info) and `idi-04-REVIEW-FIX.md` (9 fixed, 1 skipped) are part of the phase's record. I independently confirmed the tree now carries `.tier-desc { … opacity: 0.9; }` (L778) and the manifest pair `--color-action-primary-fg ON --color-action-primary TEXT@0.9` = **5.08** — the real pair that renders (`.tier-desc` is nested inside `.overlay-card button` at `index.html:182-183`, 0-1-1). The UI-SPEC E6 ruling is corrected at both `04-UI-SPEC.md:689` and `:1040`. These are dated, attributed corrections, not inconsistencies.
- **ROADMAP plan-03 line is stale, not short.** It still reads "20 文本 + 4 非文本"; the delivered manifest is **34 pairs (29 TEXT + 5 NON-TEXT) + 1 ORDER**, exceeding the stale figure and matching `idi-04-03-PLAN.md`.
- **`--green-800` is the one admitted unconsumed primitive** (documented exception N-2) — expected, not an orphan defect.
- **`--fw-medium` intentionally undeclared** (no consumer; Q4) — correct.
- **`idi-04-01-SUMMARY.md`'s wording "exactly one added line — `:root {`"** is imprecise: against `f912c1a` the tree also adds the `.annotation-answered` descendant rule and removes `.annotation-answered`, and Plan 02 later adds `button, input, select`. All three are documented in the plans' own ledgers, so SC2 still holds — this is a SUMMARY-wording inaccuracy, not a goal failure. Recorded as info, not a gap.
- **IN-05 (Info, out of scope):** `check-02-contrast.py` exits 1 via an uncaught `FileNotFoundError` traceback when `frontend/style.css` is missing rather than a clean `FAIL` line. Non-blocking — the exit code is still non-zero and the real-tree path is guarded by CHECK-01's own input assertion.

### Human Verification Required

1. **SC4 browser 实检 — the five `.hidden`-only elements**
   **Test:** Launch the app and visit each of the five elements' views.
   **Expected:** `#draft-empty`, `#rounds-hint`, `#btn-process-round`, `#round-switcher`, `#writing-hint` are never visible in a state where they should be hidden; the three 1-0-0 containers still hide.
   **Why human:** Cascade/rendering outcome; headless rendering blocked and screenshots unavailable.

2. **Frozen-round backstop**
   **Test:** Open a historical frozen round; read `#round-doc` computed `box-shadow` / `opacity` / `filter` and the body text contrast.
   **Expected:** `inset 3px 0 0 rgb(138, 101, 8)`; `opacity` 1; `filter: saturate(0.6)`; body text >= 4.5:1.
   **Why human:** `verification: backstop` truth — presence never qualifies; the plan routes an unconfirmable result to `human_needed` (insufficient_spec).

3. **DevTools computed-style checks — Plans 01/02/03 (39 items)**
   **Test / Expected / Why human:** see the `human_verification` frontmatter list; each is a named-selector computed-style reading or interaction smoke this environment cannot automate.

4. **CR-06 rendering outcome**
   **Test:** Inspect an ordinary answered annotation.
   **Expected:** User note and AI answer body both render at `--color-text-muted` (the intended D-11 intra-item hierarchy).
   **Why human:** Rendering-behaviour change confirmed by inspection only in REVIEW-FIX.

### Gaps Summary

None. Every automated must-have is satisfied in the tree: the single fenced `:root` block is correctly placed, outside-fence bare hex and tier-1 leaks are zero, all colour/space/type/radius/z-index literals are migrated, Gate 2 is empty, all four guard commands run independently and each was proven able to fail, the A11Y-04 / A11Y-04b fixes are in place with the AA values chosen at declaration time, and `app.js` / `index.html` / vendor are untouched with the pytest baseline held.

The phase is **not `passed`** only because the plan-designated human checks were never performed: the phase ran in auto mode (`workflow.auto_advance: true`), so the tracer gate and every `<human-check>` were auto-approved rather than executed. Plan 01 records 13 pending, Plan 02 records 16, Plan 03 records 10 — all DevTools computed-style readings — and two truths (SC4's browser 实检 and the frozen-round backstop) are behaviour-dependent and unexercised by any test. They are recorded with no claimed evidence and route to `human_needed`, as the plans themselves require.

---

_Verified: 2026-09-18_
_Verifier: Claude (gsd-verifier)_
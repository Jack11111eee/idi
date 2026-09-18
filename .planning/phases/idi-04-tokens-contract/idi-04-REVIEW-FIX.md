---
phase: idi-04-tokens-contract
fixed_at: 2026-09-17T15:46:17Z
review_path: .planning/phases/idi-04-tokens-contract/idi-04-REVIEW.md
iteration: 1
findings_in_scope: 10
fixed: 9
skipped: 1
status: partial
---

# Phase idi-04: Code Review Fix Report

**Fixed at:** 2026-09-17T15:46:17Z
**Source review:** `.planning/phases/idi-04-tokens-contract/idi-04-REVIEW.md`
**Iteration:** 1

**Summary:**
- Findings in scope: 10 (CR-01…CR-06, WR-01…WR-04; Info findings IN-01…IN-05 are out of `critical_warning` scope)
- Fixed: 9
- Skipped: 1 (WR-04 — see below)

**Post-fix verification (run in the main checkout, `use_worktrees=false`):**

| Gate | Result |
|---|---|
| `bash scripts/check-01-token-conformance.sh` | `PASS`, exit 0 |
| `python3 scripts/check-02-contrast.py` | `PASS: 0 failures`, exit 0 |
| `bash scripts/check-03-hidden-uniqueness.sh` | `PASS`, exit 0 |
| `bash scripts/check-04-important-count.sh` | `PASS`, exit 0 |
| raw `^[[:space:]]*\.hidden[[:space:]]*\{` | 1 |
| raw `!important;` occurrences | 1 |
| `.venv/bin/python -m pytest -q` | **219 passed, 6 skipped** (matches baseline) |

Each guard fix was verified by **mutation** (the failure mode it exists to detect, replayed against a
sandbox copy) in addition to the green path — see the per-finding notes.

## Fixed Issues

### CR-01: CHECK-01 reported PASS when `frontend/style.css` is missing or unreadable

**Files modified:** `scripts/check-01-token-conformance.sh`
**Commit:** `62c43c7`
**Status:** fixed
**Applied fix:** Added an explicit `[ -f frontend/style.css ] || { echo "FAIL…"; exit 1; }` input
assertion, moved `awk` out of the counting pipeline so its non-zero status aborts the script under
`set -e` instead of being swallowed, and replaced `grep -c` with `grep -o … | wc -l` so the count is
occurrences (also resolving IN-03's line-vs-occurrence message mismatch).
**Mutation proof:** file removed → `FAIL: frontend/style.css not found`, exit 1; file present but
`chmod 000` → `awk: can't open file…`, exit 2 (was `PASS`, exit 0); one bare hex → `FAIL: 1 …`;
two hexes on one line → `FAIL: 3 …` (occurrence-based).

### CR-02: CHECK-01 / CHECK-02 went vacuous if the `END` fence marker was removed

**Files modified:** `scripts/check-01-token-conformance.sh`, `scripts/check-02-contrast.py`
**Commit:** `2a741f6`
**Status:** fixed
**Applied fix:** Both parsers now assert the marker pair before trusting it — CHECK-01 via
`grep -c` on each marker (must be exactly 1/1), CHECK-02 via the same count inside `read_fence()`.
**Mutation proof:** with the `END` comment rewritten and a bare `#ff00ff` appended, CHECK-01 now
prints `FAIL: expected exactly 1 fence START and 1 fence END, found 1/0` (exit 1) and CHECK-02
prints the same FAIL (exit 1); both previously stayed green.

### CR-03: CHECK-02 printed `PASS: 0 failures` for an empty file or an empty manifest

**Files modified:** `scripts/check-02-contrast.py`
**Commit:** `0aba82a`
**Status:** fixed
**Applied fix:** After parsing, assert the documented coverage floors before evaluating: `>= 24`
pairs total, `>= 20` TEXT, `>= 4` NON-TEXT (the current manifest is 34 = 29 TEXT + 5 NON-TEXT, so
the floors have headroom).
**Mutation proof:** an empty `frontend/style.css` → fence assertion FAIL, exit 1; a valid but
pair-less fence (`:root { }`) → `FAIL: manifest coverage 0 pairs (0 TEXT / 0 NON-TEXT) below floor
24/20/4`, exit 1.

### CR-04: CHECK-02 silently dropped a manifest entry it could not parse

**Files modified:** `scripts/check-02-contrast.py`
**Commit:** `9bcc244`
**Status:** fixed
**Applied fix:** Reconcile the raw marker count against the parsed count for both entry kinds
(`fence.count("/* PAIR")` vs `len(pairs)`, `fence.count("/* ORDER")` vs `len(orders)`), before
evaluation. Any dropped entry is now a loud failure, so the docstring's "never silently skipped"
promise and the behaviour agree.
**Mutation proof:** `ON` → `on` in a pair → `FAIL: 34 '/* PAIR' markers but only 33 parsed`, exit 1;
`ON` → `on` in the ORDER line → `FAIL: 1 '/* ORDER' markers but only 0 parsed`, exit 1.
**Residual (inherent):** deleting a whole pair *line* drops both counts together, so it is caught
only by the CR-03 floor (a 34→33 deletion stays above it). Catching arbitrary deletions would need a
pinned exact count, which would make every legitimate manifest addition a failure; the manifest's
stated anti-drift mechanism for that case remains "it is in the same diff as the tokens".

### CR-05: CHECK-02 measured an alpha-bearing token as fully opaque → false PASS

**Files modified:** `scripts/check-02-contrast.py`
**Commit:** `4dc5572`
**Status:** fixed
**Applied fix:** The foreground is now composited over the background whenever its alpha is below 1
— whether that alpha comes from the token's own value (`rgba(0,0,0,0.45)`) or from the entry's
`@<alpha>` suffix (the two multiply). The log label shows the token-borne alpha too.
**Mutation proof:** declaring `/* PAIR --color-overlay-backdrop ON --white TEXT */` now reports
`FAIL 3.36 --color-overlay-backdrop on --white@0.45 (need >= 4.5)` instead of the former
`PASS 21.00`. No current manifest entry carries alpha, so the green path is byte-identical
(35 PASS lines, unchanged).

### CR-06: `.annotation-answered` rewrite dropped `.annotation-answer-body`

**Files modified:** `frontend/style.css`
**Commit:** `0348ddd`
**Status:** fixed: requires human verification
**Applied fix:** Added `.annotation-answered .annotation-answer-body` to the existing 0-2-0
descendant rule at the end of the file (a selector added inside the rule — the rule is neither
inserted nor reordered, so the "绝不插入、绝不重排" constraint holds). `frontend/app.js` was not
touched.
**Verification note:** This is a rendering-behaviour change, so it cannot be confirmed by a syntax
check or by the guard scripts. Confirmed by inspection only: `app.js:1147` sets
`body.className = 'annotation-answer-body'` on the ordinary answered path, and no other rule colours
that element outside `.annotation-plain`. A human should confirm the intra-item hierarchy
(user note and AI answer now both at `--color-text-muted`) is the intended D-11 outcome.
**Guard impact:** all four guards still PASS; `#confirm-error`'s 1-0-0 ID selector and the
`.hidden` rule are untouched.

### WR-01: CHECK-03's pattern was anchored to column 0

**Files modified:** `scripts/check-03-hidden-uniqueness.sh`
**Commit:** `1839b60`
**Status:** fixed
**Applied fix:** `grep -c '^\.hidden {'` → `grep -cE '^[[:space:]]*\.hidden[[:space:]]*\{'`.
**Mutation proof:** appending `  .hidden { display: block; }` (indented) now reports
`FAIL: expected 1 '.hidden {' rule, found 2`; the real tree still reports 1 → `PASS`.

### WR-02: CHECK-04 counted matching lines, not `!important` declarations

**Files modified:** `scripts/check-04-important-count.sh`
**Commit:** `3384188`
**Status:** fixed
**Applied fix:** `grep -c '!important;'` → `grep -o '!important;' | wc -l`, so the count is
occurrences and matches the script's own "DECLARATION count" claim and FAIL wording.
**Mutation proof:** rewriting the `.hidden` line to carry two declarations on one line now reports
`FAIL: expected 1 '!important;' declaration, found 2`; the real tree still reports 1 → `PASS`.

### WR-03: The TOKEN-02 "hard invariant" had no mechanical gate

**Files modified:** `scripts/check-01-token-conformance.sh`
**Commit:** `997dac9`
**Status:** fixed
**Applied fix:** CHECK-01 now also counts tier-1 primitive references outside the fence
(`var(--white|black|gray-…|green-…|blue-…|amber-…|red-…|purple-…)`) and FAILs on any. The
`(-[0-9]+)?` suffix is optional so the suffix-less `--white` / `--black` are covered too — the
pattern suggested in REVIEW.md (`(white|black|…)-[0-9]+`) would have missed exactly those two.
**Mutation proof:** appending `.primitive-leak { color: var(--gray-700); background: var(--amber-300); }`
plus `var(--white)` and `var(--black)` uses → `FAIL: 4 tier-1 primitive reference(s) outside the
fence`, exit 1. The real tree reports 0 (verified independently before the change).

## Skipped Issues

### WR-04: The manifest's `--black ON --white TEXT@0.8` pair is stale

**File:** `frontend/style.css:195`
**Reason:** The finding is valid — `--black` has no consumer as a foreground anywhere in the file —
but **the remediation offered in REVIEW.md rests on a false premise, and the truthful correction
turns CHECK-02 red**. Skipped rather than encoding a second falsehood or silently red-lining the
phase.

**Derivation (the review's own instruction was "re-derive the real value rather than guessing"):**

1. REVIEW.md (and the orchestrator's dispatch note) state that after N-4 the tier buttons' foreground
   is `var(--color-text)`, giving `--color-text@0.8 on white = 9.15`.
2. That is not what renders. `#btn-tier-loose` / `#btn-tier-strict` sit inside
   `#tier-modal > .overlay-card > .modal-buttons`, so the rule
   `frontend/style.css:381-386` — `.overlay-card button { background: var(--color-action-primary);
   color: var(--color-action-primary-fg); }` — applies. It is specificity **0-1-1**, so it beats
   N-4's `button, input, select { color: var(--color-text); }` (**0-0-1**) regardless of source
   order. The file's own N-4 comment (L856-859) says as much: ".overlay-card button(0-1-1) 全部仍然
   取胜". This was already true pre-migration (`git show f912c1a:frontend/style.css:173-178` →
   `background: #2c7be5; color: #fff;`), so N-4 never governed this element.
3. `.tier-desc` (L778) is a `<span>` with `opacity: 0.8` inside that button, so its text composites
   over the **button's** ground: `--color-action-primary-fg` (white) @0.8 over
   `--color-action-primary` (`--blue-700`, `#1f63bd`) = `(210, 224, 242)` → **4.38:1**, not 9.15 and
   not 12.63.

**Why it was not fixed:**

- The review's proposed line, `/* PAIR --color-text ON --color-surface TEXT@0.8 */`, names a
  foreground token that never renders on that ground — it would replace one un-consumed token name
  (`--black`) with another (`--color-text`) and keep the guard green on a pair that does not exist.
- The truthful line, `/* PAIR --color-action-primary-fg ON --color-action-primary TEXT@0.8 */`,
  makes CHECK-02 print `FAIL 4.38 … (need >= 4.5)` and exit 1. That is a real AA failure at that
  site, but it is **pre-existing and outside this phase's scope**: `04-UI-SPEC.md:689` rules
  `.tier-desc { opacity: 0.8 }` **"KEEP unchanged"**, and this phase is a pure value-substitution
  refactor with no sanctioned design change. The migration actually *improved* the site (pre-migration
  `#2c7be5` gave white@0.8 = 3.24:1); it still does not reach 4.5.
- Choosing between (a) correcting the manifest and letting a phase guard go red, (b) reclassifying
  the entry as `NON-TEXT` (the UI-SPEC calls the opacity "a legitimate non-text use", and 4.38 ≥ 3.0
  would pass), or (c) adjusting the de-emphasis so the pair genuinely clears 4.5, is a design
  decision that requires a human. Option (b) in particular would weaken a WCAG text threshold on
  nothing more than my own reading of an ambiguous UI-SPEC phrase.

**Recommended follow-up (not applied):** either raise `.tier-desc`'s opacity / drop it so the real
pair clears 4.5, or explicitly reclassify the entry as NON-TEXT with a recorded rationale — and in
either case correct the manifest to name `--color-action-primary-fg ON --color-action-primary`, and
re-measure the UI-SPEC `partial` row for E6 (`04-UI-SPEC.md:689`, `:1040`), whose `#000@0.8 on #fff`
= 12.63 figure is likewise derived from the wrong ground.

---

_Fixed: 2026-09-17T15:46:17Z_
_Fixer: Claude (gsd-code-fixer)_
_Iteration: 1_
---
phase: idi-04
plan: 03
subsystem: ui
tags: [css, design-tokens, wcag, contrast, accessibility, contract-check, python3, zero-dependency, verification]

# Dependency graph
requires:
  - phase: idi-04
    plan: 01
    provides: "75 colour tokens in the fenced `:root` block + CHECK-01/03/04 guard scripts + zero bare hex outside the fence"
  - phase: idi-04
    plan: 02
    provides: "31 non-colour tokens (spacing / type / weight / line-height / radius / z-index / layout), all consumed; S-4 frozen-round marker; N-4 control foreground"
provides:
  - "scripts/check-02-contrast.py — zero-dependency WCAG contrast checker (python3 stdlib only, read-only) deriving its pairs from the :root fence"
  - "A 34-entry contrast manifest written as comments inside the fence (29 TEXT / 5 NON-TEXT), token names only, no hex"
  - "One `/* ORDER … */` hierarchy assertion (SC3) — strict ordering, metric 0.311 = 5.18 / 16.67"
  - "Loud drift failure: an undeclared token name or an unlisted ORDER operand exits 1 with `unknown token` / `unknown pair`"
  - "Failure-direction evidence for all four commands (CHECK-02 twice: threshold failure + hierarchy inversion)"
affects: [phase-5, phase-6, phase-7, phase-8]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
# Same estimateTokens scale (chars/4 over the realized diff), never a harness token count.
actuals:
  tokens: 2515      # chars/4 over the realized diff (10059 chars) across frontend/style.css + scripts/check-02-contrast.py
  tasks: 2
  commits: 1        # MEASURED: git rev-list --count 4673776..HEAD (#3968)
  plan_head_before: 4673776ca450044b7a601156545fc2fb918c2205

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "The manifest lives in the same diff as the tokens it names — drift is visible in review, not asserted in prose"
    - "A checker must be able to fail: every command's failure direction is proven by injection -> FAIL -> restore -> PASS"
    - "Contract checks are read-only: the script never writes a file and never runs git (T-idi04-15)"
    - "Thresholds are WCAG constants compared on a closed interval, never rounded to the threshold first"

key-files:
  created:
    - scripts/check-02-contrast.py
  modified:
    - frontend/style.css

key-decisions:
  - "The pair manifest is a comment block inside the :root fence, written in token names only — never a hardcoded Python list. That is the whole point: CHECK-02 derives its pairs from the token block, so it cannot rot into a one-time cleanup"
  - "The ORDER assertion is a STRICT ORDERING (`ratio(quieter) < ratio(louder)`), not a `<= 0.30` threshold gate. UI-SPEC explicitly accepts 0.311 against the `<= ~0.30` guide, so a 0.30 threshold would be a false gate that fails on HEAD; the strict ordering instead catches exactly the 'deepen the muted grey to be safe' class of edit"
  - "`--gray-100` stays `#eeeeee` — the corrected muted ratio on it is 4.66, not the pre-D-15-collapse 4.75. Re-pointing it at `#f0f0f0` to 'recover' 4.75 would violate D-15 and drag `--color-surface-hover` / `--color-border-subtle` with it"
  - "Manifest is a lower-bound enumeration: the UI-SPEC's '20 text + 4 non-text' is the AUDIT's declaration count, not the checker's scope. The three UI-SPEC tables enumerate 29 TEXT + 5 NON-TEXT = 34, and the gates are floors (>= 24 / >= 20 / >= 4)"
  - "Task 2 intentionally produces no net diff: every injection is restored, and the absence of residue is itself a mechanical gate (`#deadbe` = 0, the injected pair = 0, `!important;` = 1, `--gray-600: #6a6a6a` = 1)"

patterns-established:
  - "A contrast contract is enforced by a manifest that co-lives with the tokens; an undeclared name fails loudly rather than being skipped"
  - "SC3's 'hierarchy and ratios verified together' is machine-checkable: the ratio gates are blind to a muted grey being darkened, the ORDER assertion is not"

requirements-completed: [CHECK-02, A11Y-04, A11Y-04b]

# Coverage metadata (#1602)
coverage:
  - id: C1
    description: "scripts/check-02-contrast.py exists, is executable, is zero-dependency (stdlib only), and passes on the real tree"
    requirement: CHECK-02
    verification:
      - kind: other
        ref: "python3 scripts/check-02-contrast.py -> PASS: 0 failures, exit 0; AST import scan -> ['re', 'sys']"
        status: pass
    human_judgment: false
  - id: C2
    description: "The manifest covers the reconciled scope: 34 pairs (29 TEXT / 5 NON-TEXT) + 1 ORDER assertion, floors >= 24 / >= 20 / >= 4"
    requirement: A11Y-04
    verification:
      - kind: other
        ref: "grep -c '/\\* PAIR ' -> 34; grep -c 'PAIR .* TEXT' -> 29; grep -c 'PAIR .* NON-TEXT' -> 5; grep -c '/\\* ORDER ' -> 1"
        status: pass
    human_judgment: false
  - id: C3
    description: "Every ratio reproduces the UI-SPEC's recomputed values exactly, including the corrected --gray-100 pair (4.66) and the two alpha composites (12.63 / 7.49)"
    requirement: A11Y-04
    verification:
      - kind: other
        ref: "checker stdout: muted 5.18 / 5.41 / 4.96 / 4.66; danger 5.44 / 5.21 / 4.69; border-strong 3.45 / 3.17; alpha 12.63 / 7.49"
        status: pass
    human_judgment: false
  - id: C4
    description: "SC3's hierarchy half is machine-checked: ORDER 0.311 (5.18 / 16.67), a strict ordering, and it inverts to FAIL when the muted grey is deepened"
    requirement: A11Y-04b
    verification:
      - kind: other
        ref: "stdout contains 'ORDER 0.311  --color-text-muted before --color-text on --gray-25'; with --gray-600 -> #000000 it prints 'FAIL: hierarchy inverted  1.207 ... (need < 1.000)' and exit 1 while all four muted background pairs still PASS (20.12 / 21.00 / 19.26 / 18.10)"
        status: pass
    human_judgment: false
  - id: C5
    description: "Contract drift is detectable: an undeclared token name and an unlisted ORDER operand each exit 1 loudly instead of being skipped"
    requirement: CHECK-02
    verification:
      - kind: other
        ref: "temp-copy proof: '--gray-25' renamed -> 'FAIL: unknown token --gray-25', exit 1; the '--color-text ON --gray-25 TEXT' line deleted -> 'FAIL: unknown pair --color-text ON --gray-25', exit 1"
        status: pass
    human_judgment: false
  - id: C6
    description: "All four commands give an explicit PASS/FAIL verdict, and each failure direction is proven by injection -> FAIL -> restore -> PASS (CHECK-02 twice)"
    requirement: CHECK-02
    verification:
      - kind: other
        ref: "raw outputs recorded in the Failure-Direction Evidence section below; after all restores the four commands each exit 0"
        status: pass
    human_judgment: false
  - id: C7
    description: "No residue from the proofs; app.js / index.html / vendor untouched; pytest baseline held"
    requirement: CHECK-02
    verification:
      - kind: other
        ref: "grep -c '#deadbe' -> 0; grep -c -- '--gray-300 on --gray-25' -> 0; grep -c '!important;' -> 1; grep -c -- '--gray-600: #6a6a6a' -> 1; git status --porcelain frontend/ -> empty; ls frontend/vendor/ -> marked.min.js; git diff --name-only f912c1a -- frontend/app.js frontend/index.html -> empty"
        status: pass
      - kind: unit
        ref: ".venv/bin/python -m pytest -q -> 219 passed, 6 skipped (225 collected)"
        status: pass
    human_judgment: false
  - id: C8
    description: "DevTools Computed spot-checks corroborating the checker's ratios, plus the frozen-round backstop and the two downstream gates"
    requirement: A11Y-04
    verification: []
    human_judgment: true
    rationale: "Screenshots are unavailable in this environment (headless rendering blocked; the persistent /api/events SSE stream prevents capture termination), so no visual diff is possible. This plan ran in auto mode; none of the named DevTools Computed checks was performed by a human. Harvested at end-of-phase into idi-04-UAT.md."

# Metrics
duration: 11min
completed: 2026-09-17
status: complete
---

# Phase idi-04 Plan 03: CHECK-02 Contrast Checker + Failure-Direction Proofs Summary

**The fourth contract-check command landed: a zero-dependency WCAG checker that derives its 34 pairs from a manifest co-located with the tokens, machine-checks SC3's hierarchy half as a strict ordering (`ORDER 0.311`), fails loudly on contract drift, and had every one of its failure directions proven by injection — including the inversion that the ratio gates are blind to**

## Performance

- **Duration:** ~11 min (plan start 2026-09-17T14:45:58Z → final verification)
- **Started:** 2026-09-17T14:45:58Z
- **Completed:** 2026-09-17
- **Tasks:** 2
- **Files modified:** 2 (`frontend/style.css`, `scripts/check-02-contrast.py`)

## Accomplishments

- **`scripts/check-02-contrast.py`** — zero-dependency (python3 stdlib only: `re`, `sys`), read-only. It reads the fenced `:root` block, resolves `var()` chains to primitives, and measures every manifest pair. It never writes a file and never runs git.
- **The manifest is co-located with the tokens** — 34 comment lines inside the fence, written in token names only (no hex). This is what makes "the contract is executable" true rather than asserted: a token renamed out from under a manifest entry fails loudly, so the two cannot drift.
- **Coverage is the reconciled scope, not the audit's 4** — 29 TEXT + 5 NON-TEXT = 34 pairs (floors are ≥ 24 / ≥ 20 / ≥ 4). The four `--color-text-muted` grounds, all seven event-kind chips, the six green buttons (three families), the primary/info/danger pairs, the frozen-round marker, and the two surviving α composites are all present.
- **Every ratio reproduces the UI-SPEC exactly**, including the corrected `--gray-100` pair (**4.66**, not the pre-collapse 4.75) and the two α composites (**12.63** / **7.49**).
- **SC3's hierarchy half is machine-checked.** `ORDER 0.311  --color-text-muted before --color-text on --gray-25` turns the UI-SPEC's prose figure into executable output. It is a **strict ordering**, not a `≤ 0.30` threshold — the contract explicitly accepts 0.311 against that guide, so a threshold gate would have been false on HEAD.
- **The ratio gates are provably blind to the edit the ORDER assertion catches.** Deepening `--gray-600` to `#000000` makes all four muted background pairs *easier* to pass (20.12 / 21.00 / 19.26 / 18.10) while `ORDER` alone reports `FAIL: hierarchy inverted  1.207` and exits 1.
- **All four commands' failure directions are proven** (CHECK-02 twice), with the raw outputs recorded below.
- `frontend/app.js`, `frontend/index.html` and `frontend/vendor/` received zero changes; pytest held at 219 passed / 6 skipped.

## Task Commits

Each task was committed atomically:

1. **Task 1: CHECK-02 对比度校验脚本 + 围栏内配对清单** — `1759016` (feat)
2. **Task 2: 四条命令的失败方向实证与阶段收口** — no commit: the task is pure injection → observe → restore, so it produces **zero net diff**. Every injection was reverted, and that absence of residue is itself a mechanical gate (see the residual-tampering checks below). Its deliverable is the evidence recorded in this file.

**Plan metadata:** see the `docs(idi-04-03): complete ...` commit following this file.

## Files Created/Modified

- `scripts/check-02-contrast.py` — new. Fence state machine, token resolution with `var()` chaining and loud drift failure, `#rgb` / `#rrggbb` / `rgba()` parsing, WCAG relative luminance with sRGB inverse gamma, 8-bit α compositing, closed-interval thresholds (4.5 / 3.0), and the `ORDER` strict-ordering assertion.
- `frontend/style.css` — the 34-entry pair manifest + 1 ORDER assertion appended inside the fenced `:root` block (65 added lines, 0 removed; no token value, selector or declaration touched).

## Failure-Direction Evidence (SC5 / T-idi04-19)

Every command was made to fail on purpose, observed, then restored and observed passing again. Raw outputs:

**CHECK-01 — bare hex outside the fence**
```
before:   PASS                                        exit 0
injected: append "/* probe: #deadbe */" at end of file
          FAIL: 1 bare hex outside the token block     exit 1
restored: PASS                                        exit 0
```

**CHECK-02 injection ① — threshold failure**
```
before:   PASS: 0 failures                             exit 0
injected: the "--color-text-secondary ON --gray-25 TEXT" manifest line
          replaced with "--gray-300 ON --gray-25 TEXT"
          FAIL  1.30  --gray-300 on --gray-25  (need >= 4.5)
          FAIL: 1 failures                             exit 1
restored: PASS: 0 failures                             exit 0
```

**CHECK-02 injection ② — hierarchy inversion (SC3's failure direction)**
```
before:   ORDER 0.311  --color-text-muted before --color-text on --gray-25   exit 0
injected: --gray-600: #6a6a6a  ->  --gray-600: #000000
          PASS  20.12  --color-text-muted on --gray-25
          PASS  21.00  --color-text-muted on --white
          PASS  19.26  --color-text-muted on --gray-50
          PASS  18.10  --color-text-muted on --gray-100
          FAIL: hierarchy inverted  1.207  --color-text-muted not before --color-text on --gray-25  (need < 1.000)
          FAIL: 1 failures                             exit 1
restored: ORDER 0.311  --color-text-muted before --color-text on --gray-25
          PASS: 0 failures                             exit 0
```
This is the load-bearing proof of the plan: **the four ratio pairs all still PASS** while the hierarchy assertion alone catches the edit. A checker that could only ever print PASS would not be a checker.

**CHECK-03 — `.hidden` uniqueness**
```
before:   PASS                                        exit 0
injected: a leading space on the "^\.hidden {" line
          FAIL: expected 1 '.hidden {' rule, found 0  exit 1
restored: PASS                                        exit 0
```

**CHECK-04 — `!important;` declaration count**
```
before:   PASS                                        exit 0
injected: append ".__probe { color: red !important; }"
          FAIL: expected 1 '!important;' declaration, found 2   exit 1
restored: PASS                                        exit 0
```

**Drift detection (proven on a throwaway copy, never the real tree):**
```
--gray-25 renamed to --gray-25x        -> FAIL: unknown token --gray-25      exit 1
"--color-text ON --gray-25 TEXT" line
  deleted from the manifest            -> FAIL: unknown pair --color-text ON --gray-25   exit 1
```

## Decisions Made

- **The ORDER assertion is a strict ordering, not a 0.30 threshold.** The UI-SPEC explicitly accepts 0.311 against its `≤ ~0.30` guide; a threshold gate at 0.30 would fail immediately on HEAD and would be a false gate. The strict ordering instead catches precisely the class of edit the ratio gates cannot see — someone deepening the muted grey "to be safe".
- **`--gray-100` stays `#eeeeee`.** Its measured muted ratio is **4.66**, not the 4.75 the UI-SPEC's per-background matrix lists for `#f0f0f0` — that column predates the D-15 collapse. Re-pointing the token at `#f0f0f0` to "recover" 4.75 would violate D-15 and drag `--color-surface-hover` and `--color-border-subtle` with it.
- **The manifest enumerates more than the audit's 20 + 4.** The UI-SPEC states plainly that its count is a planning aid, not a gate input, and that CHECK-02 derives its pairs from the `:root` block. The three tables enumerate 34 pairs; the gates are floors.
- **Task 2 has no commit, by design.** Its whole content is inject → observe FAIL → restore → observe PASS. The reverted working tree *is* the acceptance criterion, and it is checked mechanically rather than asserted.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] `relative_luminance` unpacked a 4-tuple**

- **Found during:** Task 1, first run of the checker
- **Issue:** `resolve()` returns `(r, g, b, a)` (alpha carried for the compositing path), but `relative_luminance` unpacked three values — `ValueError: too many values to unpack (expected 3)` on the very first pair.
- **Fix:** `r, g, b = rgb[:3]` — the alpha channel is not part of relative luminance and is already consumed by the compositing step.
- **Files modified:** `scripts/check-02-contrast.py`
- **Verification:** the checker then printed all 34 pairs plus `ORDER 0.311` and `PASS: 0 failures`.
- **Committed in:** `1759016`

### Plan adaptations

**2. [Rule 1 - Plan defect] The plan's CHECK-02 injection ① example is an ORDER operand**

- **Found during:** Task 2, while setting up the threshold-failure injection
- **Issue:** the plan suggests temporarily replacing "`--color-text-muted` 那一行" with `--gray-300 on --gray-25`. That line — `--color-text-muted ON --gray-25 TEXT` — is one of the two operands of the `ORDER` assertion this same plan introduces. Replacing it does not produce the expected `FAIL: 1 failures`; it produces `FAIL: unknown pair --color-text-muted ON --gray-25` and exits before the summary, because the ORDER operand is now missing. Verified experimentally.
- **Fix:** injected on `--color-text-secondary ON --gray-25 TEXT` instead — a TEXT pair that is not an ORDER operand. The intent of the injection (one TEXT pair below threshold, clean `FAIL: 1 failures`) is preserved, and both of CHECK-02's assertion forms stay independently provable. The two ORDER operands are left intact.
- **Files modified:** none (the injection was reverted)
- **Verification:** `FAIL  1.30  --gray-300 on --gray-25  (need >= 4.5)` followed by `FAIL: 1 failures`, exit 1.
- **Committed in:** n/a — the evidence is in this SUMMARY.

---

**Total deviations:** 1 auto-fixed (bug), 1 plan adaptation.
**Impact on plan:** The bug fix was a one-line unpack error in new code. The adaptation changes which manifest line the injection targets; the assertion coverage is identical and the reason is recorded so an independent checker does not re-derive it as a missing proof.

## Issues Encountered

- **The plan's injection ① and the ORDER assertion interact** (see deviation 2). This is not a defect in the checker — it is the drift rule working as designed: removing an ORDER operand is itself a loud failure. The injection simply has to target a non-operand pair to isolate the threshold assertion.
- **Task 2 produces no net diff.** All injections are reverted, so there is no file to commit. Recorded rather than papered over with an empty commit.
- No package installs were needed or attempted (the phase is zero-dependency by contract). `frontend/vendor/` still contains exactly `marked.min.js`; the repo still has no `package.json` and no build step.
- The pytest baseline note is accurate: the working tree collects **225**, not the ROADMAP/REQUIREMENTS' stale 219. `.venv/bin/python -m pytest -q` → **219 passed, 6 skipped**.

## Manual / Pending Human Checks (NOT performed)

This plan ran in **auto mode**. Every `<human-check>` item is manual and **none was performed by a human.** They are recorded here as pending and are harvested at end-of-phase into `idi-04-UAT.md`. No evidence is claimed for any of them.

| Task | Selector | Property | Expected | Status |
|---|---|---|---|---|
| 1 | `#ai-route-select` | `border-top-color` / `background-color` | `rgb(138, 138, 138)` / `rgb(255, 255, 255)` (corroborates 3.45:1) | pending |
| 1 | `.hint` | `color` / its `#doc-pane` ground | `rgb(106, 106, 106)` / `rgb(250, 250, 250)` (corroborates 5.18:1) | pending |
| 1 | `#stream-banner` | `border-top-color` | `rgb(138, 101, 8)` | pending |
| 1 | `.markdown-body` | `color` | `rgb(26, 26, 26)` — body text must be **visibly darker** than `.hint`'s grey (the observable form of `ORDER 0.311`) | pending |
| 2 | `#brainstorm-view h2` | `font-size` / `color` | 14px / `rgb(138, 101, 8)` (Phase 5 SC5 / Phase 6 SC5 downstream gate) | pending |
| 2 | `#round-doc` (frozen round) | `box-shadow` / `opacity` / `filter` | contains `inset 3px 0 0 rgb(138, 101, 8)` / 1 / `saturate(0.6)` | pending |
| 2 | `#round-doc` (frozen round) | visual | amber 3px left rule visible, zero horizontal displacement | pending (`human_needed` / `insufficient_spec` if unconfirmable) |
| 2 | `.hint` | `color` | `rgb(106, 106, 106)` | pending |
| 2 | `#ai-route-select` | `border-top-color` | `rgb(138, 138, 138)` | pending |
| 2 | app interaction | smoke | one 「处理本轮批注」 and one 「发送」 complete without error | pending |

## Verification (final run, all green)

| # | Gate | Result |
|---|---|---|
| 1 | `bash scripts/check-01-token-conformance.sh` | PASS (exit 0) |
| 2 | `python3 scripts/check-02-contrast.py` | `PASS: 0 failures` + `ORDER 0.311  --color-text-muted before --color-text on --gray-25` (exit 0) |
| 3 | `bash scripts/check-03-hidden-uniqueness.sh` | PASS (`^\.hidden {` = 1) |
| 4 | `bash scripts/check-04-important-count.sh` | PASS (`!important;` = 1) |
| 5 | AST import scan of the checker | `['re', 'sys']` — stdlib only |
| 6 | Manifest counts | 34 total / 29 TEXT / 5 NON-TEXT / 1 ORDER / 1 exact ORDER |
| 7 | Gate 2 (`comm -23` consumed minus declared) | empty |
| 8 | Reverse orphan scan | `--green-800` only (N-2) |
| 9 | `node --check frontend/app.js` | exit 0 |
| 10 | `.venv/bin/python -m pytest -q` | 219 passed, 6 skipped (225 collected) |
| 11 | `grep -c '#deadbe'` / `--gray-300 on --gray-25` / `!important;` / `--gray-600: #6a6a6a` | 0 / 0 / 1 / 1 |
| 12 | `git status --porcelain frontend/` | empty |
| 13 | `ls frontend/vendor/` | `marked.min.js` |
| 14 | `git diff --name-only f912c1a -- frontend/app.js frontend/index.html` | empty |

## Known Stubs

None. The manifest is a complete enumeration of the reconciled scope, and the checker has no placeholder branch — every code path either prints a verdict or exits 1.

## Next Phase Readiness

- All four contract-check commands now exist and are independently runnable, each with a proven failure direction. Phase 4's central claim — "the contract is executable" — is a set of four commands rather than a paragraph.
- `--green-800` remains the one admitted unconsumed primitive (N-2) — Phase 5's destination for `--color-action-irreversible`.
- **Blocker for end-of-phase UAT:** the 10 manual DevTools checks above have not been performed, joining the 13 pending from Plan 01 and the 16 from Plan 02. The frozen-round backstop must route to `human_needed` (`insufficient_spec`) rather than a silent pass if it cannot be confirmed.

---
*Phase: idi-04-tokens-contract*
*Completed: 2026-09-17*

## Self-Check: PASSED

- `scripts/check-02-contrast.py` — FOUND (executable, stdlib-only)
- `.planning/phases/idi-04-tokens-contract/idi-04-03-SUMMARY.md` — FOUND
- Commits `1759016`, `6dba970`, `db3e6b3` — all FOUND in history
- Final gate run: CHECK-01 PASS · CHECK-02 `ORDER 0.311` + `PASS: 0 failures` · CHECK-03 PASS · CHECK-04 PASS
- Tamper residue: `#deadbe` = 0 · injected pair = 0 · `!important;` = 1 · `--gray-600: #6a6a6a` = 1
- `git diff --name-only f912c1a -- frontend/app.js frontend/index.html` — empty
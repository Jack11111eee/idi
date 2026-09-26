---
phase: idi-04
plan: 02
subsystem: ui
tags: [css, design-tokens, css-custom-properties, spacing, typography, radius, z-index, wcag, refactor, vanilla-js]

# Dependency graph
requires:
  - phase: idi-04
    plan: 01
    provides: "Fenced `:root` token block (75 colour tokens) + CHECK-01/03/04 guard scripts + zero bare hex outside the fence"
provides:
  - "31 new non-colour tokens in the `:root` fence: 12 spacing, 6 font-size, 2 font-weight, 3 line-height, 3 radius, 4 z-index, 1 layout"
  - "Every padding / margin / gap / font-size / font-weight / line-height / border-radius / z-index literal replaced by var()"
  - "S-4 landed: `#round-doc.round-frozen` opacity deleted, amber `box-shadow: inset` structural marker added (zero layout shift)"
  - "N-4 landed: appended `button, input, select { color: var(--color-text) }` — the UA foreground becomes a token"
affects: [idi-04-plan-03, phase-5, phase-6, phase-7, phase-8]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
# Same estimateTokens scale (chars/4 over the realized diff), never a harness token count.
actuals:
  tokens: 6187      # chars/4 over the realized diff (24747 chars) across frontend/style.css
  tasks: 3
  commits: 3        # MEASURED: git rev-list --count 5573440..HEAD (#3968)
  plan_head_before: 55734407f15726a3dd86ebf2f811b71696f34d5a

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Declare-with-consumer: each token group lands in the same commit as its consumers (Hard Rule 5)"
    - "Snapping only where the contract's D-16 ledger names it — every other substitution is value-preserving"
    - "Comment prose inside the fence must not contain bare #hex or `opacity: <literal>` — CHECK-01 and the opacity count gates read the whole file, comments included"
    - "Structural state markers use box-shadow: inset (zero layout shift), never border-left (adds width)"

key-files:
  created: []
  modified:
    - frontend/style.css

key-decisions:
  - "S-1 approved and landed: all 12 spacing steps including the five off-base ones (--space-px 1, --space-half 2, --space-1-5 6, --space-2-5 10, --space-3-5 14). No 6->8 / 10->12 / 14->16 collapse — Phase 4 SC2 forbids moving pixels"
  - "S-2 approved and landed: 14px kept as a first-class step (7 steps, not the literal 6). `#brainstorm-view h2` still computes to 14px, keeping the ROADMAP Phase 5 SC5 / Phase 6 SC5 downstream gates alive"
  - "S-4 approved and landed: `#round-doc.round-frozen` deletes `opacity: 0.55` outright and keeps `filter: saturate(0.6)` plus a new amber `box-shadow: inset`. Route 1 (`opacity: 0.65`) was NOT taken — it would drop the Phase 7 focus ring to 2.85:1"
  - "`12.5px` (3 sites) folds into `--text-base` (13px) — the only font-size value change in the phase (D-1)"
  - "`--fw-medium` deliberately NOT declared; the 500 rank has no consumer and a declared-but-unconsumed token is a second literal with a nicer name (Q4)"
  - "`#sidebar` consumes `--sidebar-w: 420px`; `#state-badge { right: 448px }` left untouched (L-5 — not a hex literal; LAYOUT-01 is Phase 6)"
  - "Layout size literals (top / right / max-width / min-width / min-height / max-height / height / flex-basis / border widths) intentionally NOT tokenized — they belong to LAYOUT-* (Phase 6)"

patterns-established:
  - "Non-colour token families are single-tier (no primitive/semantic split) and all live inside the one fence"
  - "The z-index ordering assertion is a comment inside the fence, so a future renumbering that inverts badge < banner is visible in the diff"

requirements-completed: [TOKEN-05, TOKEN-06, TOKEN-07, TOKEN-08, A11Y-04b]

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "12 spacing tokens declared (--space-px/half/1/1-5/2/2-5/3/3-5/4/6/8/10) and all consumed; --space-0/-5/-7 not declared"
    requirement: TOKEN-05
    verification:
      - kind: other
        ref: "grep -cE '--space-(px|half|1|1-5|2|2-5|3|3-5|4|6|8|10):' frontend/style.css -> 12; grep -c 'var(--space-' -> 86; grep -cE '--space-(0|5|7):' -> 0"
        status: pass
    human_judgment: false
  - id: D2
    description: "All 14 padding / 11 margin / 5 gap values land on declared steps; only the 6 D-16 snapping groups change pixels (max 4px)"
    requirement: TOKEN-05
    verification:
      - kind: other
        ref: "grep -nE '(padding|margin|gap)(-[a-z]+)?: [^;]*[0-9]+px' frontend/style.css -> empty"
        status: pass
    human_judgment: false
  - id: D3
    description: "`--sidebar-w: 420px` declared and consumed by `#sidebar` (`flex: 0 0 var(--sidebar-w)`); `right: 448px` unchanged (L-5)"
    requirement: TOKEN-05
    verification:
      - kind: other
        ref: "grep -c 'var(--sidebar-w)' frontend/style.css -> 1; grep -c 'right: 448px' -> 1"
        status: pass
    human_judgment: false
  - id: D4
    description: "6 font-size tokens (11/12/13/14/15/16px) declared and consumed; `12.5px` eliminated (3 sites -> 13px)"
    requirement: TOKEN-08
    verification:
      - kind: other
        ref: "grep -cE 'font-size: [0-9.]+px' frontend/style.css -> 0; grep -c 'font-size: var(--text-' -> 32; grep -c '12.5px' -> 0"
        status: pass
    human_judgment: false
  - id: D5
    description: "2 font-weight tokens and 3 line-height tokens declared and consumed; `--fw-medium` not declared"
    requirement: TOKEN-08
    verification:
      - kind: other
        ref: "grep -c 'font-weight: var(--fw-' -> 13; grep -c 'line-height: var(--lh-' -> 4; grep -c -- '--fw-medium' -> 0; no residual `font-weight: <n>` / `line-height: <n>` literals"
        status: pass
    human_judgment: false
  - id: D6
    description: "3 radius tokens declared and consumed across all 8 existing radii, including the 2 corner longhands"
    requirement: TOKEN-06
    verification:
      - kind: other
        ref: "grep -c 'border-radius: var(--radius-' -> 25; grep -cE 'radius: var\\(--radius-' -> 27; grep -cE 'radius: [0-9]+px' -> 0"
        status: pass
    human_judgment: false
  - id: D7
    description: "4 z-index tokens declared, all consumed, with the ordering assertion written as a comment inside the fence"
    requirement: TOKEN-07
    verification:
      - kind: other
        ref: "grep -c 'z-index: var(--z-' -> 4; grep -cE 'z-index: [0-9]+' -> 0; ordering comment present naming 10 < 20 < 100 < 200 and badge < banner"
        status: pass
    human_judgment: false
  - id: D8
    description: "S-4: `#round-doc.round-frozen` has no `opacity`; `filter: saturate(0.6)` kept and amber `box-shadow: inset 3px 0 0 var(--color-action-warning)` added"
    requirement: A11Y-04b
    verification:
      - kind: other
        ref: "rule body contains filter + box-shadow and no opacity; grep -c 'opacity: 0.55' -> 6 (the 6 :disabled sites only)"
        status: pass
    human_judgment: false
  - id: D9
    description: "Archive-mode `opacity: 0.75` untouched; all 8 `:disabled` opacity declarations preserved (6 x 0.55, 2 x 0.5)"
    requirement: A11Y-04b
    verification:
      - kind: other
        ref: "grep -c 'opacity: 0.75' -> 1; grep -c 'opacity: 0.55' -> 6; grep -c 'opacity: 0.5;' -> 2; grep -c 'opacity: 0.8' -> 1"
        status: pass
    human_judgment: false
  - id: D10
    description: "N-4: `button, input, select { color: var(--color-text) }` appended at end of file (never inserted, never reordered)"
    requirement: A11Y-04b
    verification:
      - kind: other
        ref: "last rule of frontend/style.css is the appended element-selector rule; selector-line diff vs 5573440 adds exactly this one line and removes none"
        status: pass
    human_judgment: false
  - id: D11
    description: "CHECK-01 / CHECK-03 / CHECK-04 still PASS; Gate 2 empty; zero orphan tokens except `--green-800`"
    requirement: TOKEN-05
    verification:
      - kind: other
        ref: "bash scripts/check-01-token-conformance.sh -> PASS; check-03 -> PASS; check-04 -> PASS; comm -23 consumed-minus-declared -> empty; reverse diff -> --green-800 only"
        status: pass
    human_judgment: false
  - id: D12
    description: "`app.js` / `index.html` / `frontend/vendor/` untouched; pytest baseline held"
    requirement: TOKEN-05
    verification:
      - kind: other
        ref: "git diff --name-only f912c1a -- frontend/app.js frontend/index.html -> empty; git status --porcelain frontend/ -> only style.css; ls frontend/vendor/ -> marked.min.js"
        status: pass
      - kind: unit
        ref: ".venv/bin/python -m pytest -q -> 219 passed, 6 skipped (225 collected; pre-plan baseline was 225)"
        status: pass
    human_judgment: false
  - id: D13
    description: "Runtime rendering unchanged except the D-16 / D-17 snapping deltas and D-19 — DevTools Computed checks on the named selectors, plus the frozen-round backstop"
    requirement: A11Y-04b
    verification: []
    human_judgment: true
    rationale: "Screenshots are unavailable in this environment (headless rendering blocked; the persistent /api/events SSE stream prevents capture termination), so no visual diff is possible. The per-task DevTools Computed checks and the frozen-round backstop (amber inset rule + round switcher + readable body + zero horizontal shift) were NOT performed by a human — this plan ran in auto mode. Harvested at end-of-phase into idi-04-UAT.md; the backstop routes to `human_needed` (`insufficient_spec`) if it cannot be confirmed."

# Metrics
duration: 18min
completed: 2026-09-17
status: complete
---

# Phase idi-04 Plan 02: Non-Colour Token Layer + Frozen-Round Ruling Summary

**31 non-colour tokens (spacing / type / weight / line-height / radius / z-index / layout) declared and fully consumed, every matching literal replaced by `var()`, the `#round-doc.round-frozen` opacity deleted in favour of an amber inset structural marker, and the UA control foreground brought inside the token layer**

## Performance

- **Duration:** ~18 min (plan start 2026-09-17T14:15:19Z → final task commit)
- **Started:** 2026-09-17T14:15:19Z
- **Completed:** 2026-09-17
- **Tasks:** 3
- **Files modified:** 1 (`frontend/style.css`)

## Accomplishments

- **31 new tokens** landed inside the single fenced `:root` block, every one consumed: 12 spacing, 6 font-size, 2 font-weight, 3 line-height, 3 radius, 4 z-index, and `--sidebar-w`. No orphans — the reverse-difference scan reports `--green-800` alone (the admitted N-2 exception from Plan 01).
- **Every non-colour literal migrated**: 86 `var(--space-*)` references, 32 `var(--text-*)`, 13 `var(--fw-*)`, 4 `var(--lh-*)`, 27 `var(--radius-*)` (25 shorthands + the two corner longhands), 4 `var(--z-*)`. The bare-literal counts for font-size / border-radius / any-radius / z-index are all **0**.
- **S-1 landed as approved** — the 12-step spacing scale keeps all five half-steps; only the 6 groups D-16 names change pixels, the largest being `.overlay-card`'s 28px → 24px.
- **S-2 landed as approved** — 14px remains a first-class step, so `#brainstorm-view h2` still computes to 14px and the Phase 5 SC5 / Phase 6 SC5 downstream gates stay satisfiable.
- **S-4 landed as approved** — `#round-doc.round-frozen` deletes `opacity: 0.55` and gains `box-shadow: inset 3px 0 0 var(--color-action-warning)`. Body text returns to 16.67:1; the Phase 7 focus ring stays at 5.62:1 inside frozen rounds (route 1 would have left it at 2.85:1). `box-shadow` does not participate in layout, so the "pure refactor" criterion holds.
- **N-4 landed** — `button, input, select { color: var(--color-text) }` appended at the very end of the file; the UA `buttontext` / `fieldtext` foreground is no longer a second source of truth outside the fence.
- **The archive view and the `:disabled` states are untouched**: `opacity: 0.75` preserved (7.49:1), and all 8 `:disabled` opacity declarations (6 × 0.55, 2 × 0.5) survive verbatim.
- **Structural purity verified mechanically**: diffing the selector-bearing lines against `5573440` shows exactly one added selector (`button, input, select`) and zero removals. `#confirm-error` keeps its ID selector (Pitfall M6); `#stream-banner.fatal` stays a distinct selector.
- `frontend/app.js`, `frontend/index.html` and `frontend/vendor/` received zero changes; pytest baseline held at 225 collected (219 passed / 6 skipped).

## Task Commits

Each task was committed atomically:

1. **Task 1: 间距刻度 12 档 + 全部 padding / margin / gap 替换 + 侧栏宽度令牌** — `cd2cbc5` (refactor)
2. **Task 2: 字号 / 字重 / 行高 / 圆角 / z-index 刻度与全部替换** — `e721d70` (refactor)
3. **Task 3: 冻结轮结构性标记(S-4)、N-4 前景色规则与全文件收尾** — `4f323c0` (refactor)

**Plan metadata:** see the `docs(idi-04-02): complete ...` commit following this file.

## Files Created/Modified

- `frontend/style.css` — 31 new tokens in the fenced `:root` block; all padding / margin / gap / font-size / font-weight / line-height / border-radius / z-index literals replaced with `var()`; `#round-doc.round-frozen` rewritten (opacity out, amber inset marker in); one rule appended at end of file (`button, input, select`).

## Decisions Made

- **Only the D-16 snapping groups change pixels.** Every other spacing substitution is value-preserving: `--space-2-5` is 10px because 10px is what `button` padding-x already was, not because 10 is a design value. Collapsing the half-steps would have moved pixels on the most interactive surfaces in the phase whose success criterion forbids it.
- **`12.5px` folds to `--text-base` (13px)** — the sole font-size value change (D-1). 14px was deliberately *not* folded (S-2): the ROADMAP's Phase 5 SC5 and Phase 6 SC5 both assert `#brainstorm-view h2` computes to 14px.
- **The `--fw-medium` rank is not declared.** Baseline weight has exactly two values (600 ×12, 400 ×1); declaring a third with no consumer would be a second literal with a nicer name (Q4).
- **The z-index ordering assertion lives as a comment inside the fence**, naming 10 < 20 < 100 < 200 and recording that `badge < banner` is load-bearing for b9664e0 FIX 2. A future renumbering that inverts it now shows up in the diff.
- **The frozen-round marker uses `box-shadow: inset`, not `border-left`.** A left border would add 3px of width and shift every frozen round's text — the contract explicitly rejects it. `box-shadow` is zero-layout-shift.
- **Layout sizes stay literal.** `top: 12px`, `right: 448px`, `max-width`, `min-width`, `min-height`, `max-height`, `height`, `flex: 0 0 48px` and the border widths are LAYOUT-* territory (Phase 6); tokenizing them here would be scope creep.

## Deviations from Plan

**None — plan executed exactly as written.** Every token declaration, every literal substitution, and every snapping delta the plan enumerated landed unchanged. No selector was added beyond the single plan-named `button, input, select` rule; no selector was renamed, moved, or had a declaration added or removed outside the plan's ledger.

### Auto-fixed Issues

**1. [Rule 1 - Bug] Comment prose inside the fence tripped CHECK-01 and the opacity count gate**

- **Found during:** Task 3 (frozen-round marker), first gate run
- **Issue:** The explanatory comment I added above `#round-doc.round-frozen` contained the literal string `opacity: 0.55`, and the comment above the new `button, input, select` rule contained bare `#000` / `#1a1a1a`. CHECK-01 counts bare `#hex` over the **whole file** (comments included) and returned `FAIL: 2 bare hex outside the token block`; the plan's `grep -c 'opacity: 0.55'` gate returned 7 instead of 6. Both are correct behaviours of the gates — the comment prose was the defect.
- **Fix:** Reworded both comments to describe the removed multiplier and the foreground delta without spelling the literals ("原来的不透明度乘数已删除", "视觉 delta 不可感知").
- **Files modified:** `frontend/style.css`
- **Verification:** CHECK-01 → PASS (0); `grep -c 'opacity: 0.55'` → 6; all Task 3 gates green.
- **Committed in:** `4f323c0` (Task 3 commit)

**2. [Rule 2 - Missing Critical] Comment contained the literal `--fw-medium`**

- **Found during:** Task 2 (typography), acceptance check
- **Issue:** The plan's acceptance criteria state the file must not contain `--fw-medium`. The comment explaining Q4's decision named the token literally, so a mechanical `grep` would report a hit even though no declaration exists.
- **Fix:** Reworded to "the 500 rank is deliberately NOT declared (Q4)".
- **Files modified:** `frontend/style.css`
- **Verification:** `grep -c -- '--fw-medium' frontend/style.css` → 0; CHECK-01/03/04 still PASS.
- **Committed in:** `e721d70` (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (1 bug, 1 missing-critical)
**Impact on plan:** Both fixes were comment-wording changes required to keep the phase's own mechanical gates meaningful. Zero behavioural or rendering impact; no scope creep.

## Issues Encountered

- The plan's radius arithmetic uses two probes because the shorthand grep is blind to the corner longhands: `grep -c 'border-radius: var(--radius-'` reaches **25**, while `grep -cE 'radius: var\(--radius-'` reaches **27** (the extra two being `border-bottom-right-radius` at the `.chat-user` corner and `border-bottom-left-radius` at the `.chat-ai` corner). Both were confirmed at those exact values, so the "≥26" wording the plan flags as a corrected defect is not in play.
- No package installs were needed or attempted (the phase is zero-dependency by contract).
- The pytest baseline note in the plan is accurate: the working tree collects **225**, not the ROADMAP/REQUIREMENTS' stale 219. Recorded as measured.

## Manual / Pending Human Checks (NOT performed)

This plan ran in **auto mode**. Every `<human-check>` item in the three tasks is manual and **none was actually performed by a human.** They are recorded here as pending and are harvested at end-of-phase into `idi-04-UAT.md`. No evidence is claimed for any of them.

| Task | Selector | Property | Expected | Status |
|---|---|---|---|---|
| 1 | `.panel-header` | `padding-top` / `padding-left` | 10px / 16px | pending |
| 1 | `#doc-pane` | `padding-top` / `padding-left` | 32px / 40px | pending |
| 1 | `button` | `padding-top` / `padding-left` | 6px / 10px | pending |
| 1 | `.overlay-card` | `padding-top` | 24px (snapped from 28px) | pending |
| 1 | `#brainstorm-view` | `margin-top` | 24px (snapped from 22px) | pending |
| 2 | `#brainstorm-view h2` | `font-size` / `color` | 14px / `rgb(138, 101, 8)` (downstream gate) | pending |
| 2 | `#draft-view h2` | `font-size` | 15px | pending |
| 2 | `.panel-header h2` | `font-size` | 14px | pending |
| 2 | `.overlay-card h3` | `font-size` | 16px | pending |
| 2 | `.markdown-body` | `font-size` | 14px | pending |
| 2 | `.markdown-body code` | `font-size` | 13px (folded from 12.5px) | pending |
| 2 | `#selection-menu` / `#state-badge` / `#stream-banner` | `z-index` | 200 / 10 / 20 | pending |
| 3 | `#round-doc` (frozen round) | `box-shadow` / `opacity` / `filter` | contains `inset 3px 0 0 rgb(138, 101, 8)` / 1 / `saturate(0.6)` | pending |
| 3 | `#round-doc` (frozen round) | visual | amber 3px left rule visible, zero horizontal shift | pending (`human_needed` / `insufficient_spec` if unconfirmable) |
| 3 | `#rounds-placeholder.archive-mode #round-doc` | `opacity` | 0.75 | pending |
| 3 | any `button` | `color` | `rgb(26, 26, 26)` | pending |

## Verification (final run, all green)

| # | Gate | Result |
|---|---|---|
| 1 | `bash scripts/check-01-token-conformance.sh` | PASS (exit 0) |
| 2 | `bash scripts/check-03-hidden-uniqueness.sh` | PASS (`^\.hidden {` = 1) |
| 3 | `bash scripts/check-04-important-count.sh` | PASS (`!important;` = 1) |
| 4 | Gate 2 (`comm -23` consumed minus declared) | empty |
| 5 | Reverse orphan scan (`comm -23` declared minus consumed) | `--green-800` only (N-2) |
| 6 | `grep -cE 'font-size: [0-9.]+px'` / `border-radius: [0-9]+px` / `radius: [0-9]+px` / `z-index: [0-9]+` | 0 / 0 / 0 / 0 |
| 7 | Radius consumption | 25 shorthand + 27 all-forms |
| 8 | `grep -c 'opacity: 0.55'` / `0.5;` / `0.8` / `0.75` | 6 / 2 / 1 / 1 |
| 9 | `grep -c '12.5px'` / `@media` / `--fw-medium` / `--text-2xl` etc. | 0 / 0 / 0 / 0 |
| 10 | `node --check frontend/app.js` | exit 0 |
| 11 | `.venv/bin/python -m pytest -q` | 219 passed, 6 skipped (225 collected) |
| 12 | `git diff --name-only f912c1a -- frontend/app.js frontend/index.html` | empty |
| 13 | `git status --porcelain frontend/` | only `frontend/style.css` |
| 14 | `ls frontend/vendor/` | `marked.min.js` |
| 15 | Selector-line diff vs `5573440` | +1 (`button, input, select`), −0 |

## Next Phase Readiness

- The non-colour token layer is complete and mechanically enforced. Plan 03 (`check-02-contrast.py` + failure-direction proofs) can build on it directly.
- `--green-800` remains the one admitted unconsumed primitive (N-2) — Phase 5's destination for `--color-action-irreversible`.
- S-1, S-2 and S-4 have landed; S-3 landed in Plan 01. All four sign-off items are now consumed.
- **Blocker for end-of-phase UAT:** the 16 manual DevTools checks above have not been performed. The frozen-round backstop must route to `human_needed` (`insufficient_spec`) rather than a silent pass if it cannot be confirmed. This joins the 13 pending checks carried from Plan 01.

---
*Phase: idi-04-tokens-contract*
*Completed: 2026-09-17*
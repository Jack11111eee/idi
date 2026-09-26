---
phase: idi-08-accessibility-semantics-and-keyboard
plan: 02
subsystem: ui
tags: [accessibility, aria, inert, escape, modal, focus-management, keyboard]

# Dependency graph
requires:
  - phase: idi-08-accessibility-semantics-and-keyboard
    plan: 01
    provides: "the F1 focus-hand-back already inside hideSelectionMenu() (the dispatcher's first branch calls it and inherits F1-a) and the trusted-event probe pattern reused here"
  - phase: idi-07-interaction-states-and-focus
    provides: "the z-index scale (--z-selection-menu 200 > --z-overlay 100) the dispatcher's priority table is ordered by"
provides:
  - "role=dialog + aria-modal=true + aria-labelledby on the two blocking overlays; the accessible name resolves to the modal's own <h3> (two new ids, id total 80 -> 82)"
  - "background inertness that makes the aria-modal announcement true: one derived single point (syncBackgroundInert) with 5 call sites, mounted on #app only"
  - "Escape single-point dispatcher with an explicit priority table: selection menu -> #confirmation-modal -> #tier-modal"
  - "#tier-modal focus-on-open (#btn-tier-loose) and the tierModalShown reset that removes the 'tier undecided and the entry point is gone' dead state"
  - "F1-d focus hand-back on Escape: #btn-authorize / #btn-continue-check (success paths deliberately do not hand back)"
affects: ["idi-08-03", "v2 A11Y-V2-02 (role + focus trap for the other three overlays)", "any future editor of frontend/app.js modal code"]

# Actuals (#2632) — pairs with the plan's estimate (52000 tokens) to calibrate future estimates.
actuals:
  tokens: 2969      # chars/4 over the realized diff (11876 chars) across frontend/app.js + frontend/index.html
  tasks: 3
  commits: 3        # MEASURED: git rev-list --count abfb6f3..HEAD (#3968)
  plan_head_before: abfb6f3c4dcb99158c79a0563173d74649eb14de

# Tech tracking
tech-stack:
  added: []       # zero new runtime deps, zero build steps (hard rule 6); frontend/vendor/ still exactly marked.min.js
  patterns:
    - "Derived single point over paired bookkeeping: read both modals' current .hidden status, derive one attribute — cannot desynchronize on an early-return path, idempotent by construction"
    - "Escape as one dispatcher with an explicit priority table rather than per-modal listeners, so 'who responds first' is a declared order and never a source-order fact"
    - "Announcement and its fulfilment land in the same plan: aria-modal is paired with a real background-inert mount, so the declaration is structurally checkable"
    - "Count-gate hygiene: comments describe attributes by name and never respell a counted literal, so a green count still means what it says"

key-files:
  created: []
  modified:
    - frontend/index.html   # two new ids on the modal <h3>s + the ARIA triple on two .overlay divs (22 insertions, 4 deletions)
    - frontend/app.js       # appEl handle + syncBackgroundInert() + 5 call sites + tier focus-on-open + Escape dispatcher (89 insertions, 0 deletions)

key-decisions:
  - "The ARIA triple lands on .overlay, not .overlay-card: .overlay is the node classList.toggle('hidden') acts on, so 'the announced node' and 'the node that is switched' are the same one — SC3 becomes structurally checkable instead of two things kept in sync by bookkeeping."
  - "The accessible name is aria-labelledby pointing at the modal's own <h3>, never a new literal string: the copy exists in one place only and cannot drift (a name must tell the truth)."
  - "inert is derived from the two modals' current .hidden status at a single point with 5 call sites, never paired add/remove bookkeeping — the paired form leaks the attribute on any early-return path, which is the same defect class as this project's recurring derived-counter bugs."
  - "inert mounts on #app and nowhere else. All five .overlay divs and #selection-menu are #app's siblings, so mounting there can only reach the background; mounting on document.body or any shared ancestor would inert the open modal itself and lock both the keyboard and the pointer (T-idi08-05)."
  - "Escape on #confirmation-modal closes and decides nothing (D-12). 'Escape = refuse' would run rejectAuthorization() and push the user straight into a native window.prompt, whose replacement is v2 FLOW-V2-01; a 'refuse without the prompt' variant would add a second annotation-writing path and a second source of truth."
  - "Escape on #tier-modal resets the session's shown flag (D-13) so the next self-check event re-opens it. Without the reset, 'opened sets the flag, only a successful tier choice hides it' strands the user in 'tier undecided and the entry point is gone'. selfcheck.tier is not reset and no request is sent."
  - "The F1-d hand-back lives only in the Escape branches, never in the close function: after a successful '放行' the whole view is about to switch (refreshRoundsAfterStream), so pinning focus back to the trigger would drop it on <body> a moment later."
  - "Measured, not assumed (D-16): at the instant setAttribute('inert') executes, document.activeElement is still the background trigger (btn-enter), NOT an element inside the modal — so the explicit .focus() is load-bearing, not decorative."

patterns-established:
  - "Announcement paired with fulfilment: an ARIA modal declaration ships in the same plan as the inertness that makes it true"
  - "Derived single point for a cross-cutting DOM attribute, called from every mutation site inside existing function bodies"
  - "Priority-table Escape dispatcher: one document listener, declared z-order, one preventDefault per branch"
  - "Fence comments name attributes in prose and never respell a counted literal (a comment that repeats `role=` turns a correct change into a red gate)"
  - "Mutation-style controls in the runtime probe: every inertness assertion is paired with a 'remove the attribute and the same drive now behaves differently' control, so a green assertion cannot be vacuous"

requirements-completed: [A11Y-05, A11Y-06]

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "Both blocking modals announce as modal dialogs to assistive technology, with the accessible name taken from the modal's own <h3> (no new string constant)."
    requirement: A11Y-06
    verification:
      - kind: automated_ui
        ref: "grep -c 'role=' frontend/index.html == 2 ; grep -o 'aria-modal' | wc -l == 2 ; grep -o 'aria-labelledby' | wc -l == 2 ; grep -o 'id=\"' | wc -l == 82 ; id set diff vs HEAD = two pure additions"
        status: pass
      - kind: automated_ui
        ref: "inline runtime probe (reusing check-05 helpers via importlib): #app carries the inert attribute and it reflects to the IDL .inert property on open"
        status: pass
    human_judgment: false
  - id: D2
    description: "The announcement is made true: while either modal is open, #app carries native inert; once both are closed it is removed; the value is derived from the two modals' .hidden status at one point (5 call sites), so no early-return path can desynchronize it."
    requirement: A11Y-06
    verification:
      - kind: automated_ui
        ref: "grep -c 'syncBackgroundInert' frontend/app.js == 6 (1 definition + 5 call sites) ; grep -n 'inert' frontend/app.js — both mounts are appEl.* (never document.body, never a modal, never #selection-menu)"
        status: pass
      - kind: automated_ui
        ref: "inline runtime probe A2/A3/A8/A17/A18/B2/B8/B12/B14/B17 — attribute present while a modal is open, absent after close, and absent while the other three overlays are open"
        status: pass
      - kind: automated_ui
        ref: "inline runtime probe A5/A5ctl and B5 — 8 Tab presses with a modal open never land inside #app; the control (attribute removed) lands inside #app on the same drive"
        status: pass
    human_judgment: false
  - id: D3
    description: "Escape closes #confirmation-modal and produces no decision at all: no native prompt, no new annotation, no request, and the authorize row's state is untouched."
    requirement: A11Y-05
    verification:
      - kind: automated_ui
        ref: "inline runtime probe A7/A9/A10/A11/A12 — modal hidden; window.prompt call count 0; docs/*.annotations.json unchanged on disk; fetch log empty; authorize-row hidden=false and btn-authorize disabled=false both before and after"
        status: pass
      - kind: automated_ui
        ref: "grep -c 'closeConfirmModal()' frontend/app.js == 4 (1 definition + 2 pre-existing call sites + 1 dispatcher reuse) — the dispatcher reuses the existing function instead of writing its own close path"
        status: pass
    human_judgment: false
  - id: D4
    description: "Escape closes #tier-modal, resets the session's shown flag so the next self-check event re-opens it, does not reset selfcheck.tier and sends no request."
    requirement: A11Y-05
    verification:
      - kind: automated_ui
        ref: "inline runtime probe B7/B10/B11/B13 — modal hidden; fetch log empty during the Escape; no DESIGN-check-*.md appears on disk; refreshChecksAfterStream() re-opens the modal (the flag reset is what makes it possible)"
        status: pass
      - kind: automated_ui
        ref: "grep -c 'tierModalShown' frontend/app.js == 4 (declaration + read + write + the new Escape reset)"
        status: pass
    human_judgment: false
  - id: D5
    description: "On Escape, focus returns to the trigger (#confirmation-modal -> #btn-authorize, #tier-modal -> #btn-continue-check); the success paths deliberately do not hand back."
    requirement: A11Y-05
    verification:
      - kind: automated_ui
        ref: "inline runtime probe A13 (activeElement == btn-authorize) / B9 (activeElement == btn-continue-check) / A14/A15 — after closing, Tab does not restart from the page's first focusable and Shift+Tab walks backwards from the trigger"
        status: pass
      - kind: automated_ui
        ref: "grep -c 'authorizeBtn.focus()' == 1 and grep -c 'continueCheckBtn.focus()' == 1 (each exactly once, both inside the dispatcher — neither is inside the close function)"
        status: pass
    human_judgment: false
  - id: D6
    description: "#tier-modal moves focus to #btn-tier-loose on open, with the order locked as remove('hidden') -> syncBackgroundInert() -> .focus() in both modals."
    requirement: A11Y-06
    verification:
      - kind: automated_ui
        ref: "inline runtime probe B3/B15 — activeElement == btn-tier-loose on first open and again after the flag reset re-opens it; B4 is the D-16 instant measurement"
        status: pass
      - kind: automated_ui
        ref: "grep -c 'tierLooseBtn' frontend/app.js == 3 (declaration + pre-existing click binding + the new focus call)"
        status: pass
    human_judgment: false
  - id: D7
    description: "The other three overlays deliberately do not respond to Escape, and opening them does not mount background inertness (scope lock D-11, deliberate and not an omission)."
    requirement: A11Y-05
    verification:
      - kind: automated_ui
        ref: "inline runtime probe A17 (three modals, Escape each -> still open) / A18 (no inert mounted while they are open)"
        status: pass
    human_judgment: false
  - id: D8
    description: "#permission-modal's known gap (opening it gives a keyboard user no signal, and it carries no declaration) is registered and deliberately NOT fixed."
    requirement: A11Y-05
    verification:
      - kind: automated_ui
        ref: "grep -n 'permission-modal' frontend/app.js — no focus call and no Escape branch exist for it; frontend/index.html:182 still has no ARIA triple (the other three overlays were untouched by Task 1)"
        status: pass
    human_judgment: false
  - id: D9
    description: "A human observes that the background is inert at BOTH the keyboard and the pointer level while a modal is open."
    verification:
      - kind: automated_ui
        ref: "inline runtime probe A5ctl/B5/B6/B6ctl — the keyboard half and the reflected-attribute half are machine-proven, with mutation controls"
        status: pass
    human_judgment: true
    rationale: "The pointer half is NOT discriminating in this app: .overlay is `position: fixed; inset: 0` (frontend/style.css:800), so a background click was already swallowed by the overlay before this plan, and elementFromPoint at a background element's centre returns the overlay (probe A6). Machine evidence therefore proves that the attribute is mounted on the right node and that the keyboard layer honours it; 'the background feels inert under the mouse' cannot be separated from pre-existing overlay behaviour by any reading taken here. Deferred to the end-of-phase human harvest."
  - id: D10
    description: "The keyboard-selection continuity the dispatcher is designed not to break: after Escape closes the selection menu, Shift+Arrow can keep extending the same selection."
    verification: []
    human_judgment: true
    rationale: "Keyboard text selection cannot be automated in this environment (recorded in plan 01). The dispatcher's half is machine-checkable and checked — it never clears the selection (no window.getSelection() call was added) — but the experiential half (selection highlight still visible, extension still works) is the §K-2.5 ② item and stays human."

# Metrics
duration: 12min
completed: 2026-09-24
status: complete
---

# Phase idi-08 Plan 02: Blocking-Modal Dialog Semantics, Background Inertness and Escape Dispatch Summary

**Two blocking modals now announce as modal dialogs and the announcement is made true — native `inert` derived from the modals' own `.hidden` state, plus a single Escape dispatcher that closes them with zero decisions and hands focus back to the trigger**

## Performance

- **Duration:** 12 min (700s)
- **Started:** 2026-09-24T05:29:34Z
- **Completed:** 2026-09-24T05:41:14Z
- **Tasks:** 3 (all three produced a production commit)
- **Files modified:** 2 (`frontend/index.html` +22/−4, `frontend/app.js` +89/−0)
- **Realized diff:** 11876 chars ⇒ 2969 tokens (plan estimate was 52000)

## Accomplishments

- Both blocking overlays carry the dialog semantics triple, and the accessible name resolves to the modal's own `<h3>` via two **new** ids — `id` total 80 → 82, with the id-set diff against HEAD showing **two pure additions and zero removals or renames** (hard rule 5 / G-idi01-8 intact).
- The `aria-modal` declaration is made true rather than merely asserted: `syncBackgroundInert()` derives one native `inert` attribute from the two modals' current `.hidden` status, mounted on `#app` and nowhere else. Derived, not paired — no early-return path can leak it.
- Escape is a **single** `document` listener with an explicit priority table (menu → confirmation → tier). `grep -c "key !== 'Escape'"` is exactly 1: "who responds first" is a declared order, never a source-order fact.
- `#tier-modal` gained the focus-on-open it was missing (D-16), which is the substantive half of the "keyboard user is stuck" finding — and the D-16 measurement was taken rather than assumed (see below).
- `#tier-modal`'s Escape resets the session's shown flag, so the next self-check event re-opens it. The "tier undecided and the entry point is gone" dead state is gone, proven by actually re-triggering the flow (probe B13).
- Escape on the confirmation modal decides nothing: `window.prompt` call count 0, no annotation file written, fetch log empty, authorize row unchanged.
- Both Escape branches hand focus back to their trigger, and the hand-back is provably **absent** from the close function (`authorizeBtn.focus()` and `continueCheckBtn.focus()` each appear exactly once, both inside the dispatcher).
- The other three overlays deliberately do not respond to Escape and do not mount background inertness — the scope lock holds under test, not just in prose.
- `frontend/style.css` is byte-unchanged; `check-01/03/04` still PASS; `check-05 --item 1 / 4 / 10` all PASS on the final tree; `frontend/vendor/` still holds exactly `marked.min.js`.

## Task Commits

Each task was committed atomically:

1. **Task 1: dialog semantics + accessible name on the two blocking modals** — `41f1289` (feat)
2. **Task 2: background inert derivation + tier-modal focus-on-open** — `b9f775e` (feat)
3. **Task 3: Escape single-point dispatcher + tier flag reset + F1-d hand-backs** — `2a75ba1` (feat)

**Plan metadata:** (this SUMMARY commit)

## Files Created/Modified

- `frontend/index.html` — `#confirmation-modal`'s and `#tier-modal`'s `<h3>` gain `id="confirmation-modal-title"` / `id="tier-modal-title"`; the two `.overlay` divs gain the dialog triple with attribute order `id → class → role → aria-modal → aria-labelledby`. Two fence comments record ① why the landing surface is `.overlay` and not `.overlay-card`, ② why the name points at an existing heading rather than a new literal, ③ that the announcement's fulfilment lives in `app.js`, ④ the D-11 scope lock.
- `frontend/app.js` — `const appEl` after the existing handle block; `syncBackgroundInert()` as a new banner section; five call sites (`openConfirmModal`, `closeConfirmModal`, the tier open branch, `chooseTier`'s success path, the dispatcher's tier branch); `tierLooseBtn.focus()` on tier open; the Escape dispatcher as a new top-level section after `initSelectionMenu()`; `tierModalShown = false` and the two F1-d hand-backs inside the dispatcher.

## Decisions Made

- **Landing surface is `.overlay`, not `.overlay-card`** — the announced node and the node `classList.toggle('hidden')` acts on are the same one, so SC3's "declaration matches implementation" is structurally checkable; `.overlay-card` has no id and is shared by all five modals.
- **`aria-labelledby` over `aria-label`** — a literal string would be a second source of truth for copy that already exists on screen.
- **`inert` derived at a single point, 5 call sites** — the paired form leaks the attribute on any early-return path (same class as this project's recurring derived-counter bugs); the derived form cannot desynchronize and is idempotent.
- **`inert` mounts on `#app` only** — all five `.overlay` divs and `#selection-menu` are `#app`'s siblings, so it can only reach the background. Mounting on `document.body` would inert the open modal itself.
- **Escape on the confirmation modal closes only** (D-12) — the refuse path runs `rejectAuthorization()` into a native `window.prompt`, and replacing that prompt is v2 `FLOW-V2-01`.
- **The F1-d hand-back lives only in the Escape branches** — the success path is about to switch views, so handing focus back would drop it on `<body>` a moment later.
- **Count-gate hygiene, applied deliberately:** the fence comments describe the three counted attributes in prose and never respell the literals, and no comment names `syncBackgroundInert` or `tierModalShown`. A comment that repeats a counted literal makes the count structurally blind — the same discipline plan 01 used when it refused to name the `[tabindex]` selector literal.

## Deviations from Plan

### Auto-fixed Issues

None. No production-code auto-fix was needed: the implementation matches the plan's specified code shapes exactly. The two items below are **plan-premise registrations**, deliberately not "fixed" — the same class plan 01 recorded.

### Plan-premise corrections (recorded, deliberately not "fixed")

**1. [Rule 1 - Gate arithmetic] Task 2's `syncBackgroundInert` gate (`>= 6`) is unsatisfiable at Task 2's own boundary**

- **Found during:** Task 2 (running the task's `<verify>` block)
- **Issue:** Task 2's `<verify>` requires `grep -c 'syncBackgroundInert' frontend/app.js` `>= 6` and its `<fails_when>` glosses that as "1 definition + 5 call sites", and its `<acceptance_criteria>` lists all five call sites — but the **same task's `<action>`** assigns the fifth ("Escape 分派的档位分支") to Task 3, and Task 3's `<action>` is where that branch is specified. The plan-level `<verification>` block carries the identical `>= 6` line, so the task-level gate is a copy of a plan-level gate whose intended boundary is plan completion. Measured at Task 2's boundary: **5** (1 definition + 4 call sites). Measured at plan completion: **6**.
- **Fix:** None. Following the `<action>` was the correct reading (Task 3's `<action>` corroborates it, and Task 3's `<files>` is `app.js`), so the fifth call site was landed in Task 3's commit as specified rather than pulled forward into Task 2 — pulling it forward would have left Task 3 with no production change and would have made the executor the author of a task-boundary restructuring, a larger and less reversible deviation than registering a mis-scoped gate. **No gate was edited and no expected value was changed.**
- **Files modified:** none (registration only)
- **Verification:** `grep -n 'syncBackgroundInert' frontend/app.js` after Task 2 = 5 hits (L495, L501, L521, L674, L840); after Task 3 = 6 hits (+L1541). The plan-level `<verification>` line reads 6 and is green on the final tree.
- **Committed in:** n/a (the fifth call site itself landed in `2a75ba1`)

**2. [Rule 1 - Plan premise] The plan's `index.html` line references are stale by +24 lines**

- **Found during:** Task 1 (the mandatory `read_first` gate)
- **Issue:** Task 1's `<read_first>` and `<action>` cite `frontend/index.html:170` / `:172` / `:184` / `:186` / `:207` / `:213` for the two overlays, the two `<h3>`s, `#selection-menu` and `#cli-check-overlay`. Plan 01 inserted a 24-line fence comment above `#round-doc`, so on HEAD those are at **194 / 196 / 208 / 210 / 231 / 237** (`#app` still opens at L10 and closes at L179 — the boundary claim is correct, only the offsets moved). An executor anchoring on the literal line numbers would have edited `#permission-modal` and `#mission-complete-modal`, i.e. broken the D-11 scope lock while every count gate stayed green (the counts only say "two lines carry the triple").
- **Fix:** None in the plan; elements were located by content instead of by line number, and every gate plus the id-set diff confirms the edits landed on the two intended overlays. The UI-SPEC's own baseline table has the same offsets, so this is a documented staleness rather than a one-off.
- **Files modified:** none
- **Verification:** `grep -n 'class="overlay hidden"' frontend/index.html` → attributes present at L207 / L226 only; L182 / L238 / L255 untouched; id-set diff vs HEAD = 2 additions, 0 removals.
- **Committed in:** n/a (registration only)

---

**Total deviations:** 0 auto-fixed. **2 plan-premise registrations** (1 gate-arithmetic, 1 stale line reference), both resolved without touching a gate or a stylesheet.
**Impact on plan:** None on the delivered behaviour — every plan-level gate and every `must_haves` artifact check is green on the final tree. Both registrations exist so a later reader does not read the Task 2 gate boundary or the shifted line numbers as a defect.

## The D-16 measurement (taken, not assumed)

D-16 requires recording **where focus lands at the instant background inertness takes effect**, and explicitly forbids writing it as "expected to hold". Measured by patching `Element.prototype.setAttribute` before the app's own scripts run, so the hook fires synchronously at the moment `syncBackgroundInert()` writes the attribute:

```
B0 惰性属性加/去的瞬间记录:
  [{"kind": "set", "activeId": "btn-enter", "activeInsideModal": false}, …5 条]
```

**At the instant `setAttribute('inert', '')` executes, `document.activeElement` is `btn-enter` — a background element, not an element inside the modal.** The explicit `.focus()` on the next line is therefore load-bearing: without it the modal would open with focus stranded on a now-inert background node, and the very next Tab would skip the entire background and land outside the modal — worse than not inerting at all. This is exactly the mechanism the plan predicted, now measured rather than assumed. (The pre-open focus position in this path is `#btn-enter`, the trigger the user just clicked; the plan's step-5 wording assumed `#btn-continue-check`, which is not where focus actually sits on this path.)

## The seven named manual steps — observation record

Machine evidence was collected for every step that can carry it; `workflow.human_verify_mode` is `end-of-phase`, so nothing halted mid-flight and the experiential remainder is handed to the end-of-phase harvest.

| # | Step | Result | Evidence |
|---|------|--------|----------|
| 1 | Confirmation modal Escape → closes, focus on `#btn-authorize`, **zero decisions** | **PASS (machine)** | A7 hidden; A13 `activeElement == btn-authorize`; A9 `window.prompt` calls **0**; A10 no new `*.annotations.json` on disk; A11 fetch log empty; A12 authorize-row state unchanged |
| 2 | Confirmation modal background inertness (Tab stays inside; Tab resumes after close) | **PASS (machine)** | A5: 8 Tab presses → `['btn-confirm-cancel','BODY','confirm-word-input',…]`, never inside `#app`; A5ctl control (attribute removed) → lands on `ai-route-select` and walks the background, proving A5 is not vacuous; A14/A15 after close |
| 3 | Tier modal focus-on-open, Escape → focus `#btn-continue-check`, next self-check event re-opens | **PASS (machine)** | B1/B3 modal auto-opens with focus on `btn-tier-loose`; B7/B9 Escape → hidden, focus `btn-continue-check`; B13 `refreshChecksAfterStream()` re-opens it; B10 no request; B11 no check report written |
| 4 | Tier modal background inertness | **PASS (machine)** | B5: 8 Tab presses → `['btn-tier-strict','BODY','btn-tier-loose',…]`, never inside `#app` |
| 5 | **D-16: where focus lands at the instant inertness takes effect** | **MEASURED** | `activeId = 'btn-enter'`, `activeInsideModal = false` — see the section above |
| 6 | F1-d: after closing, Tab continues from the trigger rather than from `<body>` | **PASS (machine)** | A13/B9 focus **is** the trigger immediately after Escape; A15 Shift+Tab from the trigger walks **backwards** to `round-doc`; A14 Tab does not restart at the page's first focusable (`ai-route-select`) |
| 7 | The other three modals do not respond to Escape | **PASS (machine)** | A17 ×3 — `#permission-modal`, `#mission-complete-modal`, `#cli-check-overlay` each still open after Escape; A18 no inert mounted |

**A note on step 2/4's pointer half, recorded because it changes what the evidence means:** the plan's human-check pairs the keyboard observation with "click the background — no reaction". That half is **not discriminating in this app**: `.overlay` is `position: fixed; inset: 0` (`frontend/style.css:800`), so a background click was already swallowed by the overlay *before* this plan, and `elementFromPoint` at a background element's centre returns `confirmation-modal` (probe A6). The pointer-inertness claim is therefore supported by the reflected attribute plus a discriminating pair — `enter-path-input.focus()` is a **no-op while `inert` is on** and **succeeds once it is removed** (probe B6/B6ctl) — not by the click observation. Coverage entry D9 carries this as `human_judgment: true`.

## Runtime probe (39/39 PASS, 0 FAIL)

Written to `/tmp` and never added to the repository, reusing `scripts/check-05-ui-uat.py`'s helpers via `importlib` — the pattern plan 01 and `probe-07` established. Zero new dependencies, zero new repo files.

Two samples: the `p3` fixture (phase3) and a purpose-built `phase5_awaiting_tier` fixture (the `checking` fixture with its `DESIGN-check-*.md` removed; `derive_state` confirmed as `phase5_awaiting_tier` before the browser ran).

**Mutation-style controls, without which a green inertness assertion proves nothing:** A5ctl and B6ctl remove the attribute and re-run the identical drive, showing the behaviour changes. The `inert` assertions are therefore non-vacuous.

Two initial probe failures were **my probe's faults, not the product's**, and were corrected rather than accepted (this project's "suspect your own probe first" discipline):

- **A14 first read FAIL.** `#btn-authorize` is the *last* focusable element inside `#app` in p3 (`#authorize-hint` is a `<p>`, `#writing-view` is hidden, and everything after `#app` is a hidden overlay), so Tab correctly wraps to browser chrome and `activeElement` becomes `<body>`. The assertion conflated "focus is on the trigger" with "the next Tab stays inside". Rewritten as a discriminating pair: Tab must not restart at the page's first focusable, and Shift+Tab must walk backwards from the trigger.
- **B6 first read FAIL.** The target was `#round-switcher`, but `loadChecksView`'s `awaiting_tier` branch calls `roundSwitcher.classList.add('hidden')` (`app.js:628`), so the element is unfocusable and *both* the assertion and its control were vacuous. Retargeted to `#enter-path-input`, which is visible in that state.

## Known Gaps registered (not fixed)

- **`#permission-modal` — D-17, deferred to v2 `A11Y-V2-02`.** Opening it moves focus nowhere and it carries no declaration, so a keyboard user gets no signal that it appeared. It is **deliberately not fixed in this phase**: the user adjudicated the object set to confirmation + tier (D-11), and this modal can be Tabbed out of, so it does not constitute a trap. Machine-checked as *not* touched: `frontend/index.html:182` still has no ARIA triple, and `frontend/app.js` contains no focus call or Escape branch for it.
- **The pointer half of "the background is inert" is not separately observable** — see the note under the seven-step table. The attribute is provably mounted on the right node and the keyboard layer provably honours it; the mouse observation cannot be separated from the overlay's pre-existing blocking behaviour.
- **After a successful tier choice, focus lands on `<body>`** (probe B17: `activeElement == 'BODY'`). This is per plan — A-8 scopes the hand-back to the Escape branches and states the success path must not hand back — and is recorded here as a measured consequence rather than as a defect, so a later reader does not file it as an oversight.

## Issues Encountered

- **A pre-existing dev server is already listening on `127.0.0.1:8765`.** The harness prints `INFO server: … 已在服务 —— 复用,不新起、结束时也不关闭`, so all browser evidence was collected against that reused process rather than a freshly-booted one. Same condition plan 01 recorded.
- **`check-05 --item 1` prints click-retry lines while a run is in flight.** The `cli-check-overlay` intercepts pointer events during the harness's own retry loop, which makes `tail` output look alarming mid-run. The verdict is unaffected: `item 1: PASS (45 条断言, 0 FAIL, 0 BLOCKED)`, exit 0, identical to the pre-change baseline. Recorded so a future reader does not read the retry log as a failure.
- **The `grep -c "key !== 'Escape'"` command cannot be embedded inside a nested-quoted compound shell line.** The local `grep` is ugrep and parses the embedded `!==` as a filename, printing `warning: !==: No such file or directory` and returning 0. Run standalone it returns exactly **1** (verified). This is a shell-quoting trap in composing the gate, not a gate result — the same class as the `-o | wc -l` arithmetic trap this project has recorded before.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- **Ready for plan 03.** Plan 03's only production change is one word of empty-state copy at `app.js:1121`; nothing it needs from this plan is missing, and this plan touched neither that line nor its surroundings.
- **The phase's JS half is now complete.** `frontend/app.js` carries every symbol the phase's artifact list assigns to it except plan 03's copy fix; `frontend/index.html` carries all four of its assigned changes (plan 01's attribute + this plan's two ids and two attribute groups).
- **Zero fingerprint debt holds (D-01 path):** `frontend/style.css`, `scripts/check-05-ui-uat.py` and `scripts/probe-07-focus-composite.py` are byte-identical to HEAD, and neither `frontend/app.js` nor `frontend/index.html` appears in any live report's `covered_files`. **Do not judge staleness with `gsd-tools query verification status <phase>`** — these phase directories all return `missing`.
- **End-of-phase UAT must harvest, in addition to this plan's own items:** plan 01's ring-discernibility observation (D-02 stays open), plan 01's nine-step keyboard script (whose steps 6–7 this plan unblocks), §K-2.5 ② (can the selection continue after Escape — coverage entry D10), the D-02 second half, and this plan's D9 (the pointer half).
- **Pre-existing open item, not introduced here (D-26):** `idi-04.1-radix`'s re-verification is still outstanding (`/gsd-verify-work idi-04.1-radix`). This plan adds nothing to that layer.

---

*Phase: idi-08-accessibility-semantics-and-keyboard*
*Completed: 2026-09-24*

## Self-Check: PASSED

- `frontend/index.html` — FOUND; `frontend/app.js` — FOUND; this SUMMARY — FOUND
- Commit `41f1289` (Task 1) — FOUND; commit `b9f775e` (Task 2) — FOUND; commit `2a75ba1` (Task 3) — FOUND
- `requirements-completed: [A11Y-05, A11Y-06]` matches the plan's `requirements:` verbatim
- `actuals` measured, not narrated: `commits: 3` from `git rev-list --count abfb6f3..HEAD`; `plan_head_before` = `abfb6f3c4dcb99158c79a0563173d74649eb14de`; `tokens: 2969` = 11876 chars / 4 over the realized diff
- Plan-level `<verification>` re-run on the final tree: `role=` 2 · `aria-modal` 2 · `aria-labelledby` 2 · `id="` 82 · `syncBackgroundInert` 6 · Escape guard 1 · `authorizeBtn.focus()` 1 · `continueCheckBtn.focus()` 1 · `node --check` OK · `check-01/03/04` PASS · `check-05 --item 1/4/10` PASS · `git status --porcelain -- frontend/style.css` empty · `frontend/vendor/` = exactly `marked.min.js`

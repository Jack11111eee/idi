---
phase: idi-08-accessibility-semantics-and-keyboard
plan: 01
subsystem: ui
tags: [accessibility, keyboard, focus-management, tabindex, focus-visible, selection-api, tracer]

# Dependency graph
requires:
  - phase: idi-07-interaction-states-and-focus
    provides: the `[tabindex]` member of the `:focus-visible` enumeration at frontend/style.css:1514 — the zero-CSS carrier surface this plan consumes
  - phase: idi-06-layout-robustness
    provides: `#doc-panel-body { padding: var(--space-8) var(--space-10) }` — the 32px/40px geometry the ring's clearance rests on
provides:
  - "#round-doc is a real keyboard Tab stop (tabindex=\"0\") receiving the Phase 7 whole-box focus ring with zero CSS change"
  - "Shift-only keyup submit listener inside initSelectionMenu() — release Shift to hand focus into #selection-menu's first button"
  - "F1-a / F1-b / F1-c focus hand-back at the single point hideSelectionMenu()"
  - "runtime evidence that the ring lands on the new Tab stop (check-05 --item 10 runtime reading, not the static count)"
affects: [idi-08-02, idi-08-03, "v2 A11Y-V2-02 (role + focus trap)", "any future editor of frontend/app.js selection code"]

# Actuals (#2632) — pairs with the plan's estimate.tokens (48000) to calibrate future estimates.
actuals:
  tokens: 1350      # chars/4 over the realized diff (5402 chars) across frontend/app.js + frontend/index.html
  tasks: 3
  commits: 2        # MEASURED: git rev-list --count 126646e..HEAD (#3968); Task 2 changed no file
  plan_head_before: 126646e72252184e7516e494e1d5be75b3ba345b

# Tech tracking
tech-stack:
  added: []       # zero new runtime deps, zero build steps (hard rule 6); frontend/vendor/ still exactly marked.min.js
  patterns:
    - "Zero-CSS delivery via a pre-landed enumeration rule: one HTML attribute activates a rule Phase 7 wrote for this moment"
    - "Commit gesture = modifier key release (Shift keyup) rather than a per-keystroke branch — keeps the extension loop uninterrupted"
    - "Single-point focus hand-back inside the choke function instead of at its four call sites"

key-files:
  created: []
  modified:
    - frontend/index.html   # #round-doc gains tabindex="0" + a four-point fence comment (18 insertions, 1 deletion)
    - frontend/app.js       # Shift-only keyup listener in initSelectionMenu(); F1 hand-back in hideSelectionMenu() (36 insertions, 0 deletions)

key-decisions:
  - "The submit gesture is Shift *release*, implemented as a NEW document-level listener — handleSelectionTrigger stays byte-identical. A literal ROADMAP implementation (focus-move on every keyup) would let a keyboard user select exactly one character while A11Y-03's acceptance item still passes."
  - "The focus hand-back lives inside hideSelectionMenu() alone (4 call sites ⇒ scattering necessarily misses one), and its predicate is taken BEFORE classList.add('hidden') — afterwards document.activeElement has already fallen back to <body> and the test is permanently false."
  - "#round-doc gets the attribute and nothing else: no role, no aria-label (D-18, user-adjudicated 'add none'). The bare <div> Tab stop is a knowingly accepted cost, recorded in the fence comment so it is not filed as an omission."
  - "#draft-content deliberately gets no Tab stop (D-20): handleSelectionTrigger's first substantive guard is `currentState !== 'phase3'`, so phases 1-2 have no annotation feature and a Tab stop there would be dead code, unverifiable at runtime."
  - "No D-02 escalation was taken. No machine reading triggered D-02, and the dispatch notes forbid changing frontend/style.css on the executor's own initiative; the human half of the discernibility judgment is deferred to end-of-phase."

patterns-established:
  - "Zero-CSS ring delivery: land the attribute, let the pre-existing `[tabindex]` enumeration member carry the ring; never add a :focus rule (hard rule 10 / G-idi-05-1)"
  - "Modifier-release commit gesture for keyboard text selection, fenced with the reason a per-keyup implementation would false-green"
  - "Runtime reading over static count as the Pitfall 6 evidence: counts prove the rule exists, only the runtime reading proves it landed on the new Tab stop"
  - "Reusing the check-05 harness helpers (importlib + make_fixture + enter_project) for ad-hoc verification instead of writing a new probe"

requirements-completed: [A11Y-02, A11Y-03]

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "#round-doc is a real keyboard Tab stop: tabindex=\"0\" present, reachable by Tab at position 2 (immediately after #round-switcher per §K-1.7), and it receives the Phase 7 whole-box focus ring with zero CSS change."
    requirement: A11Y-02
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 10 — [checking]/[p3] judged set includes #round-doc at ('2px','rgb(31, 99, 189)'); item 10 PASS (41 assertions, 0 FAIL, 0 BLOCKED), exit 0"
        status: pass
      - kind: automated_ui
        ref: "trusted CDP Tab drive (inline, reusing check-05 helpers): 2nd Tab lands on #round-doc with :focus-visible=true, outline-width 2px, outline-color rgb(31, 99, 189), outline-offset 2px"
        status: pass
      - kind: automated_ui
        ref: "scripts/probe-07-focus-composite.py — PROBE ring outline-color=rgb(31, 99, 189) outline-width=2px"
        status: pass
    human_judgment: false
  - id: D2
    description: "#draft-content deliberately carries no Tab stop, and the reason is recorded in code and SUMMARY so it is not read as an omission."
    requirement: A11Y-02
    verification:
      - kind: other
        ref: "grep -n draft-content frontend/index.html — L113 has class=\"markdown-body\" and no tabindex; grep -o 'id=\"[^\"]*\"' frontend/index.html | wc -l == 80 (unchanged)"
        status: pass
    human_judgment: false
  - id: D3
    description: "Releasing Shift hands focus into #btn-annotate, and all three conjunctive predicates discriminate independently (wrong key / collapsed selection / hidden menu each leave focus put)."
    requirement: A11Y-03
    verification:
      - kind: automated_ui
        ref: "inline F1 runtime check reusing check-05 helpers — 14/14 PASS: B1 Shift keyup bubbling from #round-doc ⇒ activeElement=btn-annotate; B2 key 'a' ⇒ stays; B3 collapsed selection ⇒ stays; B4 menu hidden ⇒ stays"
        status: pass
      - kind: automated_ui
        ref: "trusted CDP keyboard.down('Shift')/up('Shift') ⇒ activeElement=btn-annotate with :focus-visible=true and outline-width 2px"
        status: pass
    human_judgment: false
  - id: D4
    description: "Hiding the menu while focus rests inside it hands focus back to #round-doc (F1-a, which also covers F1-b — both menu items call it first); focus outside the menu is not hijacked."
    requirement: A11Y-03
    verification:
      - kind: automated_ui
        ref: "inline F1 runtime check — A1 focus on #btn-annotate then hideSelectionMenu() ⇒ activeElement=round-doc; A3 focus on #round-switcher then hideSelectionMenu() ⇒ activeElement stays round-switcher"
        status: pass
    human_judgment: false
  - id: D5
    description: "The whole-box focus ring is visually discernible (the D-02 question)."
    verification:
      - kind: automated_ui
        ref: "check-02 resident arithmetic gate: --color-focus on --color-surface = 5.57:1; probe-07: 3.45:1 under the archive 0.75 composite (both >= 3:1 non-text minimum)"
        status: pass
      - kind: automated_ui
        ref: "inline geometry measurement: horizontal clearance 36px per side vs the 4px the ring needs; #round-doc padding and border are all 0 so the ring's inner edge sits 2px outside the text start (it does not press on text)"
        status: pass
    human_judgment: true
    rationale: "'Discernible' is a human-eye judgment and screenshots are unavailable in this environment (headless render blocked by the resident /api/events SSE stream). The machine half is proven above; the visual half is not automatable and must be harvested from the <verify><human-check> block at end-of-phase. One machine-observed caveat to weigh: at the app's own scroll position a 3.64px sliver of the ring's bottom edge falls outside #doc-panel's scroll-clip boundary (a 4px scroll brings all four edges inside)."
  - id: D6
    description: "A keyboard user can actually select more than one character with Shift+Arrow and complete a real annotation end to end (the point of the whole plan)."
    requirement: A11Y-03
    verification: []
    human_judgment: true
    rationale: "Keyboard text selection cannot be automated in this environment (not even contenteditable can be selected) — the plan mandates a named nine-step manual script (§K-2.6). The focus-movement half is machine-proven (D3/D4); the selection-extension half and §K-2.5's two measured items are not."

# Metrics
duration: 8min
completed: 2026-09-24
status: complete
---

# Phase idi-08 Plan 01: #round-doc Tab Stop + Keyboard Selection Focus Contract Summary

**One HTML attribute activates the focus ring Phase 7 pre-wired, and a Shift-release gesture turns keyboard text selection into a working annotation path — with the false-green trap it was designed around documented in the code**

## Performance

- **Duration:** 8 min
- **Started:** 2026-09-24T03:06:49Z
- **Completed:** 2026-09-24T03:14:29Z
- **Tasks:** 3 (Task 2 changed no file by design ⇒ 2 commits)
- **Files modified:** 2 (`frontend/index.html` +18/−1, `frontend/app.js` +36/−0)
- **Realized diff:** 5402 chars ⇒ 1350 tokens (plan estimate was 48000)

## Accomplishments

- `#round-doc` is now a real keyboard Tab stop. `tabindex="0"` alone activated the `[tabindex]` member of Phase 7's `:focus-visible` enumeration at `frontend/style.css:1514` — **zero CSS change** (D-01 delivered exactly as designed).
- Under a **trusted** keyboard Tab, `#round-doc` is the **2nd** stop (immediately after `#round-switcher`) and reads `:focus-visible=true`, `outline-width: 2px`, `outline-color: rgb(31, 99, 189)`, `outline-offset: 2px`. That is the runtime reading the plan demanded — the static count (`tabindex` 0→1, `:focus-visible` 9→9) only proves the rule exists.
- Keyboard selection now has a working commit gesture: holding Shift extends the selection with focus **not moving**; releasing Shift hands focus to `#btn-annotate`. Proven with both synthetic and trusted CDP events, with negative controls on all three predicates.
- Focus never rests on a hidden element: `hideSelectionMenu()` takes its predicate **before** hiding and returns focus to `#round-doc` — the single choke point covers F1-a, F1-b and F1-c.
- `handleSelectionTrigger` is **byte-identical** to HEAD; t8g's "no key whitelist on keyup" decision still governs it. The whitelist exists only in the new Shift listener.
- `frontend/style.css`, `scripts/check-05-ui-uat.py` and `scripts/probe-07-focus-composite.py` are byte-identical to HEAD — D-01's zero-fingerprint-debt property holds.
- `scripts/probe-07-focus-composite.py` re-ran clean (D-04 obligation from STATE.md's Deferred Items) with both self-witness counts recorded verbatim.
- All four invariant guards (`check-01`…`check-04`) still PASS.

## Task Commits

1. **Task 1 (tracer): #round-doc Tab stop + fence comment** — `bbf9060` (feat)
2. **Task 2: ring discernibility measurement + probe-07 re-run + census registration** — no commit (the plan specifies zero file changes; its products are the records in this SUMMARY)
3. **Task 3: Shift submit listener + F1 focus hand-back** — `b1351d2` (feat)

**Plan metadata:** (this SUMMARY commit)

## Files Created/Modified

- `frontend/index.html` — `#round-doc` (L156) gains `tabindex="0"`; an 18-line fence comment above it records ① the ring's source is `frontend/style.css:1514`'s Phase 7 enumeration rule (deliberately not naming the selector literal, which would have introduced a second `tabindex` match), ② the ring geometry and its overturning of the upstream "only top/bottom edges" claim, ③ `#draft-content`'s deliberate D-20 asymmetry, ④ why `tabindex` 0→1 with `:focus-visible` 9→9 is not a Pitfall 6 violation.
- `frontend/app.js` — `initSelectionMenu()` gains a Shift-only `keyup` listener on `document` after the existing `roundDoc` keyup binding; `hideSelectionMenu()` gains the F1-a/b/c hand-back. Both carry fence comments stating why they live where they do.

## Decisions Made

- **Shift release, not per-keyup, is the commit gesture** — and the reason is fenced in the code: `roundDoc.addEventListener('keyup', handleSelectionTrigger)` fires on *every* keyup, so moving focus there would cap a keyboard user at one character while A11Y-03's acceptance item ("Shift+arrow → menu appears → focus already in menu") still passes, because it tests state rather than usability.
- **The hand-back predicate must be taken before the hide** — once the focused element is `display:none`, `document.activeElement` has already fallen back to `<body>` and the test is permanently false. The machine check A1 discriminates this: a post-hide predicate would leave `activeElement` at `body`.
- **One function, four call sites** — the hand-back sits inside `hideSelectionMenu()` rather than at its four call sites (two closers, two guards, two menu items); scattering it necessarily misses one.
- **`#round-doc` gets the attribute and nothing else** — no `role`, no `aria-label` (D-18, user-adjudicated "add none"); the bare `<div>` Tab stop is a knowingly accepted cost, and the fence comment says so.
- **`#draft-content` gets nothing (D-20)** — same `.markdown-body` class, but `handleSelectionTrigger`'s first substantive guard is `currentState !== 'phase3'`, so a Tab stop there would be dead code, unverifiable at runtime.
- **No D-02 escalation** — no machine reading triggered it, and the dispatch notes forbid changing `frontend/style.css` on the executor's own initiative.

## Deviations from Plan

Three plan premises were falsified by measurement. **No production-code auto-fix was needed** — the implementation matched the plan's specified code shapes exactly; all three findings are registration/measurement corrections, and none was "fixed" by touching a gate or a stylesheet.

### Plan-premise corrections (Rule 1 class — recorded, deliberately not "fixed")

**1. `check-05 --item 10`'s sample set is `p1 / checking / p3` — not `p3 / checking / archive`, and it never runs `p12`**
- **Found during:** Task 2 (running the named gate)
- **Issue:** Task 2's action says to run item 10 "在 p3 / checking / archive 三个样本上各跑一次", and Task 1's acceptance says "p1 / p12 两个样本里 `#round-doc` 因落在 `.hidden` 子视图内而不进判定集". The driver hardcodes `p1`, then `for state in ("checking", "p3")` (`scripts/check-05-ui-uat.py:3712-3760`), and the CLI exposes only `--item / --ai-smoke / --keep / --headed / --browser` — there is no `--state` flag. So the `archive` half of the instruction is unsatisfiable, and the `p12` half of the acceptance criterion is not covered by the named gate at all.
- **Fix:** None — **the gate must not be modified** (D-21: `check-05-ui-uat.py` is in the `covered_files` of five live reports). The actual coverage is registered instead. `p1` was measured directly: `#round-doc` reads `visible=False` there, so `visible ∧ focusable` filters it out exactly as D-03 predicted.
- **Files modified:** none
- **Verification:** read the driver and `--help`; ran item 10 three times (pre-change, post-change ×2), all PASS.
- **Committed in:** n/a (record-only)

**2. The plan's / D-01's geometric premise "盒高数千像素 ⇒ 视口里是左右两条贯穿全高的竖线" is not reproduced, and a new measured fact was not in the plan**
- **Found during:** Task 2 (converting the plan's geometric *argument* into a *measurement*)
- **Issue:** measured in the p3 fixture, `#round-doc` is **778.64px** tall against a **900px** viewport — the box is *shorter* than the viewport, so the ring renders as a **complete rectangle**, not "two full-height vertical lines". Cause: the p3 fixture's current round document (`scripts/ui-states/p3/docs/discuss-round-2.md`) is only **883 bytes**. The plan's claim describes a *real* phase3 project's long document; the fixture does not reproduce it. The claim's *conclusion* (not clipped, therefore discernible) survives — but its stated *evidence* does not, and per this project's "实测驱动,不采信上游文档的论断" discipline that must be registered rather than repeated.
- **Newly measured (not in the plan):** at the app's own scroll position the ring's **bottom edge** extends **3.64px** past `#doc-panel`'s scroll-clip boundary (ring bottom 903.64 vs clip bottom 900). This is a literal instance of "环的某一段被裁切", so it is surfaced rather than declared green — but it is **not** D-02's "不可辨": three of four edges plus both full-height sides are visible, and a **4px** scroll brings all four edges inside (`#doc-panel` has 201px of travel: scrollHeight 1101 vs clientHeight 900). Horizontal clearance is comfortable — **36px** measured per side against the 4px the ring needs.
- **Fix:** None. Recorded as evidence for the deferred human judgment; the D-02 escalation was not taken on the executor's own initiative, and D-01's zero-CSS path is not contradicted.
- **Files modified:** none
- **Verification:** computed-style + geometry measurement in the p3 fixture at two scroll positions, reusing the check-05 harness helpers (no new probe file, no new dependency).
- **Committed in:** n/a (record-only)

**3. The nine-step script's steps 6–7, and Task 3's `<done>` claim about Escape, belong to plan 02**
- **Found during:** Task 3
- **Issue:** Task 3's `<done>` asserts "Escape 关菜单后焦点回到 `#round-doc`", and §K-2.6's steps 6–7 exercise Escape. But this plan adds no Escape handling — `artifacts_this_phase_produces` assigns the "Escape 单点分派监听器" to **plan 02**. Pressing Escape today closes nothing (the menu's existing closers are the document mousedown and the window scroll capture). So steps 6–7 are not exercisable within this plan, and the `<done>` claim cannot hold until plan 02 lands.
- **Fix:** None in code — registered here so the end-of-phase UAT harvest does not read a failing step 6 as this plan's defect.
- **Files modified:** none
- **Verification:** read `artifacts_this_phase_produces`; confirmed the two existing closers in `initSelectionMenu()`.
- **Committed in:** n/a (record-only)

### Additional verification performed beyond the plan's `<verify>` (no production-code impact)

The plan's Task 3 automated gates are all **static** (`node --check` + three greps). Since this plan's central warning is that a literal implementation would **false-green** — all static gates passing while the feature is unusable — two runtime checks were added, reusing the check-05 harness helpers via `importlib` (the pattern `probe-07` itself uses). No repo file was created and no dependency was added.

- **F1 runtime check — 14/14 PASS.** A1: focus inside the menu, then `hideSelectionMenu()` ⇒ `activeElement` becomes `round-doc` (this is what proves the predicate is taken *before* the hide). A3 negative control: focus on `#round-switcher`, then `hideSelectionMenu()` ⇒ focus stays put. B1: Shift keyup bubbling from `#round-doc` ⇒ `activeElement` becomes `btn-annotate` (**this proves `initSelectionMenu()` is actually bound in the p3 sample** — the specific false-green this check existed to catch). B2/B3/B4: each predicate discriminates independently.
- **Trusted-keyboard check — 10/10 PASS.** `page.keyboard.press("Tab")` drives focus to `#round-doc` on the **2nd** Tab (Tab order: `round-switcher` → `round-doc`, exactly §K-1.7); the ring reads `2px / rgb(31, 99, 189)` with `:focus-visible=true`; a **trusted** `Shift` release hands focus to `#btn-annotate`, which then also reads `2px / rgb(31, 99, 189)` with `:focus-visible=true`.
  - Worth recording as a probe-hygiene note: the first, **synthetic**-event run read `#btn-annotate`'s outline as `3px / rgb(32, 32, 32)` with `focusVisible: False` — the UA default, not the ring. That was a **probe artifact** (Chrome's `:focus-visible` heuristic does not treat untrusted synthetic events as keyboard-initiated), disproven by the trusted run. Recorded because "先怀疑自己的探针" is this project's standing discipline, and because a future reader seeing only the synthetic run would wrongly conclude the menu button shows no ring.

## Issues Encountered

- **A pre-existing dev server is already listening on `127.0.0.1:8765`.** Both `probe-07` and the check-05 harness print `INFO server: 127.0.0.1:8765 已在服务 —— 复用,不新起、结束时也不关闭`. All browser evidence here was collected against that reused server. Not a problem, but it means the readings were not taken against a freshly-booted process.
- **The `#btn-annotate` ring reading required trusted events.** See the probe-hygiene note above — the synthetic-event reading was misleading and was corrected, not accepted.
- **Task 2 produces no commit by design.** The plan states "本任务不改任何文件"; its products are the records below. The atomic close-out invariant is satisfied — the two production commits both exist, and this SUMMARY is the deferred close-out.

## Ring discernibility evidence (D-02) and its branch

**Machine half — proven, and it did NOT trigger D-02:**

| Evidence | Reading | Source |
|---|---|---|
| `#round-doc` in the judged set | `checking` judged 9 (was 8), `p3` judged 10 (was 9); `#round-doc` = `(visible=True, focusable=True, '2px', 'rgb(31, 99, 189)')` | `check-05 --item 10` |
| `#round-doc` excluded where expected | `p1` = `(visible=False, focusable=True, None, None)` ⇒ filtered out by `visible ∧ focusable` | `check-05 --item 10` |
| Ring on the real Tab stop | `:focus-visible=true`, `outline-width: 2px`, `outline-color: rgb(31, 99, 189)`, `outline-offset: 2px`, at Tab position 2 | trusted CDP Tab drive |
| Ring vs panel background | `5.57:1` (`--color-focus` on `--color-surface`) — resident arithmetic gate | `check-02-contrast.py` |
| Ring vs page background | `5.72:1` (`--color-focus` on `--color-surface-page`) | `check-02-contrast.py` |
| Ring under the archive 0.75 composite | `3.45:1` (>= 3.0) | `probe-07-focus-composite.py` |
| Horizontal clearance | 36px per side measured vs 4px required | inline geometry measurement |
| Does the ring press on text? | No — `#round-doc` padding and border are all `0`, so the ring's inner edge is 2px *outside* the text start | inline geometry measurement |

**Caveat surfaced for the human:** the bottom edge's 3.64px sliver at the app's default scroll position (recoverable with a 4px scroll) — see deviation 2.

**Human half — deferred, not skipped.** `workflow.human_verify_mode` is `end-of-phase`, so the `<verify><human-check>` blocks in Task 1 and Task 2 do not halt mid-flight; they are harvested by the verifier at end-of-phase. The named steps are unchanged from UI-SPEC §K-1.2: enter p3 → Tab until focus reaches the round-document area → record ① whether the ring is left/right full-height lines, ② whether it is distinguishable at a glance from the `#doc-panel` background (`#f9f9f9`), ③ whether it presses on the first/last characters of the body. **"Not discernible" = any segment of the ring clipped ∨ adjacent-pixel contrast < 3:1 ∨ focus location cannot be determined from it — any one triggers D-02.**

**D-02 branch disposition:** **not triggered by any machine reading; escalation not performed.** Should the human observation return "not discernible", the escalation is *outside this plan's `files_modified`* — it changes `frontend/style.css` (adding a rule) and drags in ① recomputing 5 live fingerprints from **HEAD content** (not mtime — stale has two causes and the remedies are opposite), ② whether `check-05`'s static count gates are affected, ③ `§Deliberate Delta Ledger` **D8-9** moving from conditional to actual, ④ hard rule 7 (that `style.css` plan must carry runtime verification, not just static counts). The two fallback carrier surfaces (UI-SPEC §K-1.3) are **B-1 inset ring** (`outline-offset: -2px`; **not recommended** — `.markdown-body` has no padding, so the lines would press on every line's first and last characters) and **B-2 header ring** (lift the ring to the always-visible sticky `#doc-panel-header`; **recommended** — 36px compact ring, no overlap with body text, and `:has()` has a Phase 6 `:has(:empty)` precedent). **The escalation must not be silently downgraded to a known limitation** — that produces "nominally focusable, but you cannot see where focus is", which is Pitfall 6's failure form.

## probe-07-focus-composite.py re-run (D-04) — verbatim self-witness output

Re-run on the final state, exit 0. The two self-witness counts are the probe's own design promise — without them there is no way to distinguish "the probe is working" from "the probe is silently spinning":

```
PROBE archive-state opacity=0.75 visible=True
PROBE links-before=0
PROBE links-after=1 (mutation-applied=yes)
PROBE focus={'tag': 'a', 'id': 'idi07-probe-link', 'focusVisible': True}
PROBE ring outline-color=rgb(31, 99, 189) outline-width=2px
PROBE composite ring=(31, 99, 189) ground=rgb(249, 249, 249) alpha=0.75 composited=(86, 136, 204) ratio=3.45 (>= 3.0)
```

`links-before=0` / `links-after=1 (mutation-applied=yes)` confirm the injection really happened; the composite ratio 3.45 satisfies SC 1.4.11's 3:1 non-text floor. The probe's Tab drive is data-driven (limit 40, stops on hit), so the new Tab stop was absorbed with **zero probe changes** — as D-04 predicted.

## D-03 census changes and the `_idi07_tab_drive` arithmetic

Measured by running item 10 against HEAD~1's `frontend/index.html` and against the new one (temporary file swap, restored byte-identically; `git status --porcelain -- frontend/index.html` empty afterwards).

| Sample | Raw census (pre → post) | Judged set (pre → post) | `#round-doc` reading |
|---|---|---|---|
| p1 | 28 → 29 | **9 → 9** | `visible=False` ⇒ excluded (unchanged) |
| checking | 28 → 29 | **8 → 9** | `True, True, '2px', 'rgb(31, 99, 189)'` |
| p3 | 28 → 29 | **9 → 10** | `True, True, '2px', 'rgb(31, 99, 189)'` |

- **Why the raw census moves:** the census enumerates `FOCUSABLE_SELECTOR` = `button, input, select, textarea, a[href], summary, [tabindex]`. Before, `#round-doc` matched **none** of those (it had no `tabindex`), so it was absent from the raw data entirely — not merely filtered. After, `[tabindex]` matches it.
- **`_idi07_tab_drive(page, len(data) + 8)` arithmetic (D-03 ②):** the limit is data-driven on the raw census length — **36 → 37** (+1), while the Tab order also gains exactly one stop (+1). The two cancel, so **no gate change is needed**. Confirmed empirically on both sides.
- **Item 10 was PASS before *and* after** (41 assertions, 0 FAIL, 0 BLOCKED, exit 0 both times). This change therefore **did not turn a red gate green** — it added a member to the judged set which the pre-landed ring then covered. That is exactly D-03's "普查集变化", not a defect fix.
- **The `archive` half of D-03 cannot be measured** — item 10 does not run that sample (deviation 1).

## `#draft-content` anti-omission registration (D-20)

`frontend/index.html:113`'s `#draft-content` is the same `.markdown-body` class and deliberately **does not** get a Tab stop. This is **correct, not an omission**: `handleSelectionTrigger`'s first substantive guard is `if (currentState !== 'phase3') return` (`app.js:1327`), so phases 1–2 have no annotation feature at all and a Tab stop there would be **dead code** — violating this project's "don't declare what nothing consumes" discipline and unverifiable at runtime. The reason is recorded both in the `#round-doc` fence comment (point ③) and here, so a future reader cannot read "A11Y-02 only named `#round-doc`" as a gap and add it.

## Baseline reconciliation (measured on HEAD before the change)

| Probe | Expected | Measured (pre) | Post-change |
|---|---|---|---|
| `grep -c 'inline-error' frontend/style.css` | 1 | **1** | 1 |
| `grep -c 'clearInlineError();' frontend/app.js` | **9** (not 6 — D-21's "6" is a stale `b9664e0`-era figure that would build a gate which can never fail) | **9** | 9 |
| `grep -v '^#' frontend/style.css \| grep -c ':focus-visible'` | 9 | **9** | **9** (zero CSS change) |
| `grep -c '^\.hidden {' frontend/style.css` | 1 | **1** | 1 |
| `grep -c 'role=' frontend/index.html` | 0 | **0** | **0** |
| `grep -c inert frontend/app.js` | 0 | **0** | 0 |
| `grep -c 'hideSelectionMenu' frontend/app.js` | **7** (Task 3's absolute criterion) | **7** | **7** — unchanged; the hand-back is inside the function body, no new call site |
| `grep -c 'window.getSelection' frontend/app.js` | **1** pre / **2** post (Task 3's absolute criterion) | **1** | **2** |
| `grep -c 'tabindex' frontend/index.html` | 0 → **1** | **0** | **1** — the only broken baseline |
| `grep -c 'tabindex' frontend/app.js` | 0 | **0** | **0** |
| `grep -o 'id="[^"]*"' frontend/index.html \| wc -l` | 80 | **80** | **80** — no id added, renamed or deleted |
| `ls frontend/vendor/` | exactly `marked.min.js` | **1 file** | 1 file |

**Only `tabindex` moved (0 → 1); `:focus-visible` stayed 9 → 9.** That looks like "independent movement" under Pitfall 6's gate but is not — Phase 7 already landed the ring's carrier surface, which is the whole point of splitting the two phases. The mechanical evidence is not the count but the runtime reading (see the D-02 table above).

## Next Phase Readiness

- **Ready for plan 02** (modal semantics + Escape): the focus contract F1 now has its menu-side legs in place, and `hideSelectionMenu()` is the established single point for hand-backs.
- **Plan 02 unblocks three deferred items:** the nine-step script's steps 6–7 (Escape), §K-2.5 ② (can selection continue after Escape), and `#permission-modal`'s known gap stays out of scope (v2 `A11Y-V2-02`).
- **End-of-phase UAT must harvest:** Task 1's and Task 2's `<verify><human-check>` (ring discernibility — D-02 stays open until then) and Task 3's nine-step keyboard script. Also §K-2.5's two measured items: ① if the selection highlight is **not** visible after focus enters the menu, the keyboard user is annotating blind — **report immediately, do not register silently**; ② if selection cannot continue after Escape, register as a known limitation with no new mechanism.
- **Known limitation registered, not a defect (D-19):** nothing tells a keyboard user that Shift+Arrow selects text. The focus ring is the only visual signal. This makes no gate red because the manual acceptance is run by a user who knows the steps — which is exactly why it is registered explicitly rather than treated as covered.
- **Zero fingerprint debt holds** (D-01 path): `frontend/style.css`, `scripts/check-05-ui-uat.py` and `scripts/probe-07-focus-composite.py` are byte-identical to HEAD, and `frontend/app.js` / `frontend/index.html` are in no live report's `covered_files`. **Do not judge staleness with `gsd-tools query verification status <phase>`** — these phase directories all return `missing`.
- **Pre-existing open item, not introduced here (D-26):** `idi-04.1-radix`'s re-verification is still outstanding (`/gsd-verify-work idi-04.1-radix`); its `covered_digest` went stale when Phase 5 rewrote `style.css` and `check-05-ui-uat.py` (a genuine content change). This plan adds nothing to that layer.

---

*Phase: idi-08-accessibility-semantics-and-keyboard*
*Completed: 2026-09-24*

## Self-Check: PASSED

- `frontend/index.html` — FOUND; `frontend/app.js` — FOUND; this SUMMARY — FOUND
- Commit `bbf9060` (Task 1) — FOUND; commit `b1351d2` (Task 3) — FOUND
- `requirements-completed: [A11Y-02, A11Y-03]` matches the plan's `requirements:` verbatim
- `actuals` re-measured against the realized diff: 5402 chars ⇒ 1350 tokens; `commits: 2` from `git rev-list --count 126646e..HEAD`; `plan_head_before` = `126646e72252184e7516e494e1d5be75b3ba345b`
- Task 2 correctly has no commit — the plan specifies zero file changes for it

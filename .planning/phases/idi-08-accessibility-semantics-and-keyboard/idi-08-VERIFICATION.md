---
phase: idi-08-accessibility-semantics-and-keyboard
status: passed
verified: 2026-09-24T15:52:00Z
reverified: 2026-09-24T13:23:27Z
score: 34/39 truths verified (4 human, 1 present-but-behavior-unverified, 0 FAILED); 2 of the 34 are self-verified, not independent
covered_files:

  - .planning/REQUIREMENTS.md
  - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-01-PLAN.md
  - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-01-SUMMARY.md
  - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-02-PLAN.md
  - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-02-SUMMARY.md
  - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-03-PLAN.md
  - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-03-SUMMARY.md
  - frontend/app.js
  - frontend/index.html
  - scripts/check-05-ui-uat.py

covered_digest: "v1:sha256:fc0890605b05386a712e1851d18180aa658e32da05654eebf5b33f5a780b0a91"
behavior_unverified: 1
overrides_applied: 0
resolved_gaps:

  - truth: "ROADMAP Phase 8 Gate: Phase 4/6/7 全部 gate 仍通过 (all Phase 4/6/7 gates still pass)"
    status: resolved
    resolution: >
      User adjudication (2026-09-24) = **amend the gate's scope**. Implemented in `63fba08`:
      `scripts/check-05-ui-uat.py` gains `L5_CONTENT_REGION_MIN_RATIO = 0.5`. A focusable element at
      least half its clipping container's padding-box height is a **content region, not a control**;
      those rows are DECLARED (reported per-row via `info()`, never silently dropped) rather than
      asserted. Control rows are still asserted. If the declaration set ever consumes the whole
      judged set, the assertion goes `blocked(...)` rather than PASS (fail-closed).
      `check-05 --item 9` now reports `PASS (16 条断言, 0 FAIL, 0 BLOCKED)`; the declared row is
      `[('#round-doc', '#doc-panel', 778.6, 900, -66.6)]` in p3 and there are **0** declared rows in
      p1 / checking, so the declaration fires exactly where it is aimed and nowhere else.
    verification_basis: >
      **SELF-VERIFIED — NOT INDEPENDENT.** This resolution was authored by the same agent that wrote
      this report, and the two re-verification attempts delegated to `gsd-verifier` both stalled
      (600s watchdog, twice) without writing anything; the user then explicitly authorized the
      orchestrator to write this report. The evidence below is therefore first-party. It is
      mechanical and reproducible, but a reader should treat the resolution as *asserted by its
      author* rather than *confirmed by a third party*. Nothing else in this report is affected:
      the truths above were verified by the independent pass and are carried forward unchanged.
    evidence:
      - "`check-05 --item 9` re-run on the close-out tree: `item 9: PASS (16 条断言, 0 FAIL, 0 BLOCKED)`"
      - "Mutation A (does not let real violations through): a 30px focusable control injected flush against `#doc-panel`'s bottom edge (clearance 0) lands in the ASSERTED set, not the declared set, and the assertion FAILS. Ratio check: 30/900 = 3.3% < 50%, while `#round-doc` is 778.6/900 = 86.5% >= 50%."
      - "Mutation B (no vacuous pass): with the ratio forced to 0.0 (everything declared), item 9 returns `BLOCKED (16 条断言, 0 FAIL, 3 BLOCKED)` — not PASS. Reverted afterwards and verified byte-identical to the backup apart from that one line."
      - "Geometry re-measured first-party: element 778.64px, container padding box 900px, element offset 188px from the padding-box top; clearance -66.64px at the sample default scroll (scrollTop 0), +4.36px at scrollTop 71, +33.36px at scrollTop 100, and 0.36px once the browser scrolls the element into view (scrollTop 67). Note the 0.36px is the same clip D-02 measured as 3.64px (4 - 0.36 = 3.64)."
      - "Correction to the earlier gap text: the claim that the violation is *structural* (element taller than its container) is FALSE — 778.64 < 900. It was my hypothesis and measurement refuted it. The real property is that clearance sits on the threshold and the element's height is content-driven and unbounded."
    registered_costs:
      - "This change invalidates the fingerprints of the 4 phases that list `check-05-ui-uat.py` in `covered_files`: idi-04.1-radix, idi-05, idi-06, idi-07. (D-21/A-4 said 5; the measured count is 4 — idi-04 mentions the script in prose but never listed it.)"
      - "Those 4 digests were deliberately NOT recomputed. Refreshing a digest asserts 'nothing changed since verification', which is false — `frontend/style.css` genuinely changed under phases 5-8. The staleness is kept as a visible signal. Correct closure is re-running those phases' verify-work."
      - "`idi-04`'s digest is ALSO stale, for an unrelated pre-existing reason (its `covered_files` include `frontend/style.css` and `.planning/REQUIREMENTS.md`, both changed after its 2026-09-20 verification at `812a224`). Not caused by this phase and not touched."

behavior_unverified_items:

  - truth: "按住 Shift 连按方向键扩选时焦点不移动 —— 焦点环全程留在文档区 (the Shift+Arrow extension must not move focus)"
    test: "In a phase-3 project, Tab until `#round-doc` holds the ring, then hold Shift and press ArrowRight several times, then release Shift"
    expected: "During the extension `document.activeElement` stays `#round-doc` and the ring stays drawn on it; only the Shift release moves focus into `#btn-annotate`"
    why_human: >
      This is the ordering invariant the whole gesture design exists to protect, and no test exercises
      it. A trusted CDP `Shift+ArrowRight` drive produces no selection at all in this environment
      (12 presses → `{collapsed: true, len: 0}`), so the state the invariant governs cannot be reached
      automatically. Symbol presence + wiring is satisfied (the Shift listener is key-filtered and the
      body of `handleSelectionTrigger` is untouched), but presence cannot show that focus stays put
      across the extension.

human_verification:

  - test: "A11Y-08 — Tab through a phase-3 project and a phase-5 self-check project and confirm the Tab order reaches every interactive control"
    expected: "Every interactive control is reachable by Tab; the new `#round-doc` stop sits at position 2 (immediately after `#round-switcher`, immediately before `#btn-authorize` when `#authorize-row` is visible)"
    why_human: "The machine half is complete and green (check-05 --item 10: `[p3] 判定集 10 个元素,未覆盖 []`; the SUMMARY's own census reaches 10/10 in p3 and 8/8 in checking), but `every interactive control` is an on-screen enumeration across states the harness does not sample (notably `archive`, which item 10 cannot reach — its sample set is hardcoded to p1/checking/p3)."
  - test: "A11Y-03 keyboard-selection leg — hold Shift and press Arrow to extend a selection, then release Shift"
    expected: "The selection extends past one character, the menu appears, focus lands on `#btn-annotate`; Escape then closes the menu, returns focus to `#round-doc`, and the selection survives so `Shift+Arrow` can keep extending"
    why_human: "Keyboard text selection cannot be automated here (not even inside `contenteditable`). Per ROADMAP Phase 8 §Manual checks an automated non-result on this leg is not a functional-defect call."
  - test: "REG-03 items 1, 2, 3, 5, 6 plus the rewritten item 4 step 3, re-run by hand"
    expected: "All six `b9664e0` manual acceptance items behave as recorded in idi-08-03-SUMMARY.md §REG-03 observation record"
    why_human: "The keyboard-dependent legs (item 4's extension step, and the keyboard-origin variants of the others) cannot be automated; the executor recorded steps 1/2/4/5 machine-observed PASS and handed step 3 over explicitly."
  - test: "Backstop UI-consideration truths for E1 (#round-doc), E2 (#selection-menu), E3 (#confirmation-modal), E4 (#tier-modal), E5 (#app), E6 (the other three overlays): loading / error / overflow / long-text / empty / partial"
    expected: "Each declared backstop either has an observable contract or is confirmed not applicable to that element"
    why_human: "Declared `verification: backstop` in the plan frontmatter — the planner abstained rather than committed a criterion, so there is no spec to verify against. Most are not applicable (a static div, a two-button menu, `#app`), but that is an adjudication, not a measurement."
  - test: "The phase-5 zero-height `#round-doc` Tab stop (SUMMARY 03 §Deviation 2)"
    expected: "Confirm whether a 351 × 0 Tab stop whose ring renders as a thin horizontal line is acceptable, or make the attribute conditional"
    why_human: "Registered by the executor, not fixed (a conditional attribute would change a plan-01 deliverable). It is a design decision, not a measurement."

---

# Phase 8: 可访问性语义与键盘 (idi-08) Verification Report

**Phase Goal:** 键盘用户能真实完成一次划词批注,能 Esc 关闭两个阻塞式弹窗;两个阻塞弹窗向辅助技术宣告的语义与其实现一致;内联错误不再破坏控件行;五条已交付修复的人工验收项全部重跑通过。
**Verified:** 2026-09-24T15:52:00Z · **Re-verified:** 2026-09-24T13:23:27Z
**Status:** human_needed (was `gaps_found`; the single gap is resolved — see §Gap Resolution)
**Re-verification:** Yes — the independent pass at `a640f39` found one gap; that gap is now closed at `63fba08`. **The gap-closure portion is SELF-VERIFIED (not independent)** — see the `verification_basis` field. Every other truth is carried forward from the independent pass unchanged.

> **Timestamp note (registered, not corrected).** The original `verified:` stamp above is **wrong**:
> it reads `15:52:00Z` but the file was written at 15:30 **local** (CST, UTC+8) = 07:30 UTC, i.e. the
> independent pass labelled local time with a `Z` suffix. That is why this re-verification's correct
> UTC stamp (`13:23:27Z`) reads *earlier* than it. The original stamp is left as written rather than
> rewritten; do not use it for staleness reasoning.

**Tree verified:** HEAD (`63fba08`). Three commits landed after all three plans were summarized:
`62dfd3e` (an INCOMPLETE first attempt at the Escape fix), `09b170d` (the real Escape fix), and
`63fba08` (the L-5 gap resolution). Where a SUMMARY's prose disagrees with HEAD, HEAD wins and the
disagreement is registered under §SUMMARY ↔ HEAD Disagreements — not treated as a gap.

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | SC1b: Esc closes `#confirmation-modal` | ✓ VERIFIED | Behavioral probe (bundled chromium): open via `#btn-authorize` → `{confirmHidden:false, appInert:true}` → `Escape` → `{confirmHidden:true, appInert:false, active:'btn-authorize'}` |
| 2 | SC1c: Esc closes `#tier-modal` | ✓ VERIFIED | Behavioral probe on a `phase5_awaiting_tier` fixture: `Escape` → `{tierHidden:true, appInert:false, active:'btn-continue-check'}` |
| 3 | SC3: both blocking modals declare modal-dialog semantics consistent with implementation | ✓ VERIFIED | `role="dialog"`, `aria-modal="true"`, `aria-labelledby` → `#confirmation-modal-title` ("授权确认") / `#tier-modal-title` ("选择自检档位"); the declaration is made true by `inert` on `#app` (truth 17) and by the Escape closes above |
| 4 | SC4: inline error not squeezed into a narrow column; view switches clear stale errors; error path is `textContent` only | ✓ VERIFIED | `showInlineError` (app.js:317-324) writes only `p.textContent`, anchored to `probeControls` / `enterForm` / `checkSwitcher` (all block-flow containers); `grep -n 'innerHTML' frontend/app.js` shows no user-content concatenation; `grep -c 'clearInlineError();'` = 9 |
| 5 | SC5: `node --check app.js` passes; pytest 219 baseline unchanged | ✓ VERIFIED | `node --check frontend/app.js` exit 0; `.venv/bin/python -m pytest -q` → **219 passed, 6 skipped** in 11.25s |
| 6 | A11Y-02 gate: `tabindex` count and `:focus-visible` count do not move independently | ✓ VERIFIED | `grep -c tabindex frontend/index.html` = 1 (was 0); `grep -v '^#' frontend/style.css \| grep -c ':focus-visible'` = 9 (> 0) |
| 7 | Tab reaches the round-document area and the whole-box ring draws on `#round-doc` | ✓ VERIFIED | `check-05 --item 10` PASS (41 assertions): `[p3]` Tab sequence includes `#round-doc` with `outlineWidth 2px` / `focusVisible true`; judged set 10, uncovered `[]` |
| 8 | At the moment `#round-doc` is `document.activeElement`, computed `outline-width` is exactly 2px and `outline-color` equals the runtime-resolved `--color-focus` | ✓ VERIFIED | item 10 SC1 readings: `outline-width 2px`, `outline-offset 2px`, `outline-color rgb(31, 99, 189)` == runtime-resolved `--color-focus` |
| 9 | Releasing Shift shows `#selection-menu` with focus on `#btn-annotate` | ✓ VERIFIED | Behavioral probe: real 11-char mouse-drag selection → `Shift` down/up → `{hidden:false, active:'btn-annotate'}` |
| 10 | Escape dismisses the menu durably and hands focus back to `#round-doc` (focus neither on a hidden button nor back on `<body>`) | ✓ VERIFIED | Behavioral probe: S1 `Escape` → `{hidden:true, active:'round-doc'}`; **S2 second Escape** → still hidden; **S3 `ArrowRight`** → still hidden; **S3b `'a'`** → still hidden; selection preserved (`selLen 11`, D-08) |
| 11 | Menu items hand focus back to `#round-doc` after executing | ✓ VERIFIED | Behavioral probe: click `#btn-annotate` (prompt dismissed → no POST) → `{active:'round-doc', menuHidden:true}` |
| 12 | `#draft-content` keeps no `tabindex` | ✓ VERIFIED | `frontend/index.html:113` — `id="draft-content" class="markdown-body"`, no attribute |
| 13 | `#round-doc` gains zero attributes besides `tabindex` (no `role`, no `aria-label`) | ✓ VERIFIED | `git diff 4976bee..HEAD -- frontend/index.html`: the only change to that line is `+ tabindex="0"` |
| 14 | E1 overflow / long-text: no new container, no new clipping rule; `overflow-wrap: anywhere` and `#doc-panel-body { padding: 32px 40px }` unchanged | ✓ VERIFIED | `frontend/style.css` blob is byte-identical at the phase base and HEAD (`95cb22ee…` both) |
| 15 | E2 long-text: the two menu labels stay verbatim | ✓ VERIFIED | `frontend/index.html:250-251` — `批注` / `用大白话讲这段` |
| 16 | Both modals carry `role="dialog"` + `aria-modal="true"`, named from the existing `<h3>` via a new id | ✓ VERIFIED | `index.html:207-209`, `226-228`; id count 80 → 82, zero renames/deletions |
| 17 | Background inert while either modal is open, removed when both close; scoped to `#app` only | ✓ VERIFIED | Behavioral probe: on open `app:true`, and `body:false` plus every sibling overlay `false`; on close `appInert:false`. `syncBackgroundInert()` (app.js:521-526) derives from both modals' `.hidden`; 5 call sites (495, 501, 674, 840, 1606) |
| 18 | Escape on `#confirmation-modal` produces no decision (does not substitute for "拒绝") | ✓ VERIFIED | Behavioral probe: no `window.prompt` was raised on the Escape path; the branch calls `closeConfirmModal()` + `authorizeBtn.focus()` only (app.js:1593-1598) |
| 19 | Escape on `#tier-modal` resets `tierModalShown` (next self-check event can re-pop) | ✓ VERIFIED | Behavioral probe: after Escape, calling the same entry point a self-check event uses (`refreshChecksAfterStream`) re-pops the modal — impossible unless the flag was reset |
| 20 | `#tier-modal` focuses `#btn-tier-loose` on open | ✓ VERIFIED | Behavioral probe on the awaiting-tier fixture: `active: 'btn-tier-loose'` |
| 21 | F1-d hand-backs: confirm → `#btn-authorize`; tier → `#btn-continue-check` | ✓ VERIFIED | Behavioral probes (truths 1 and 2) |
| 22 | The other three overlays deliberately do not respond to Escape (scope lock D-11) | ✓ VERIFIED | Behavioral negative check: force-opened `#permission-modal` / `#mission-complete-modal` / `#cli-check-overlay` all remain open after Escape |
| 23 | Escape dispatch follows an explicit priority table (menu → confirm → tier), independent of source order | ✓ VERIFIED | app.js:1570-1614; branches 1/2/3 each `return` after `preventDefault()`, the "deliberate non-responders" block follows |
| 24 | E3 empty: `#btn-confirm-authorize.disabled === true` while `#confirm-word-input` is empty | ✓ VERIFIED | Behavioral probe: empty → `True`; wrong word (`错误词`) → `True`; exact word (`确认授权`) → `False` |
| 25 | E3 error: the confirm error copy is written via `textContent` only | ✓ VERIFIED | app.js:575, 583 — `confirmError.textContent = …`; no `innerHTML` |
| 26 | S8-1: the empty-annotation copy reads 「本轮暂无批注——在右侧文档划词即可批注。」 | ✓ VERIFIED | Behavioral probe: `#annotation-list .hint` `textContent` in the p3/current-round/zero-annotation state equals that string verbatim; `grep -c '在左侧文档划词即可批注'` = 0 |
| 27 | REG-02 gate ①: `grep -c 'inline-error' frontend/style.css` is still 1 | ✓ VERIFIED | Measured 1 |
| 28 | REG-02 gate ②: `grep -c 'clearInlineError();' frontend/app.js` >= 9 (baseline 9, only grows) | ✓ VERIFIED | Measured 9 (app.js:318, 327, 468, 636, 863, 1293, 1652, 1702, 1726) |
| 29 | Archive path: after switching rounds, 「处理本轮批注」 is not clickable | ✓ VERIFIED | Behavioral probe on the archive fixture: before `{hidden:True, disabled:True}`, switch to round 2 (`roundTitle` `第 2 轮(归档·只读)`) → still `{hidden:True, disabled:True}` |
| 30 | check-01…04 all PASS on the close-out tree; `frontend/style.css` byte-unchanged; `frontend/vendor/` holds exactly one file | ✓ VERIFIED | check-01 PASS, check-02 `PASS: 0 failures` (ORDER 0.363), check-03 PASS, check-04 PASS; style.css blob identical to the phase base; `ls frontend/vendor/` → `marked.min.js` |
| 31 | Fingerprint obligation registered (D-01 path ⇒ zero debt; `frontend/app.js` / `frontend/index.html` in no live report's `covered_files`) | ✓ VERIFIED | Checked against idi-04 / idi-04.1-radix / idi-05 / idi-06 / idi-07 `covered_files` — none names `frontend/app.js` or `frontend/index.html` |
| 32 | SC1a / A11Y-08: the Tab order reaches every interactive control | ? HUMAN | Machine half green in the sampled states (item 10 judged set 10/10 in p3, 8/8 in checking, uncovered `[]`); full enumeration across states incl. `archive` is on-screen |
| 33 | SC2: a keyboard user can really complete one selection annotation | ? HUMAN | Mouse-origin selection → Shift release → Enter → real annotation is machine-proven (SUMMARY 03 item 4 steps 1/2/4/5, and truth 9 here); the keyboard-origin selection step cannot be automated |
| 34 | SC5b / REG-03: all `b9664e0` manual acceptance items re-run | ? HUMAN | Six items recorded in SUMMARY 03 §REG-03 observation record with machine-observed PASS on 1/2/3/5/6 and item 4 steps 1/2/4/5; the keyboard-dependent halves stay human |
| 35 | Shift+Arrow extension does not move focus (the invariant the gesture design exists to protect) | ⚠️ PRESENT_BEHAVIOR_UNVERIFIED | Present + wired (key-filtered Shift listener; `handleSelectionTrigger` body untouched), but no test exercises the invariant — see behavior_unverified_items |
| 36 | A11Y-08 census records `#round-doc`'s Tab position, not merely "Tab can reach it" | ? HUMAN | SUMMARY 03 records position 2, before `#round-switcher` / after `#btn-authorize`; item 10 independently agrees on the judged set. On-screen confirmation is human |
| 37 | ROADMAP Phase 8 Gate: all Phase 4/6/7 gates still pass | ✓ VERIFIED (resolved) | `check-05 --item 9` → `PASS (16 条断言, 0 FAIL, 0 BLOCKED)` after `63fba08`'s L-5 content-region declaration set. Was FAIL at `a640f39`. **Resolution is self-verified, not independent** — see §Gap Resolution |
| 38 | The L-5 declaration set does not let a real control violation through | ✓ VERIFIED (self) | Mutation: a 30px control injected flush at `#doc-panel`'s bottom edge (clearance 0) lands in the ASSERTED set and the assertion FAILS. See §Gap Resolution |
| 39 | The L-5 declaration set cannot produce a vacuous pass | ✓ VERIFIED (self) | Mutation: ratio forced to 0.0 ⇒ `item 9: BLOCKED (16 条断言, 0 FAIL, 3 BLOCKED)`, not PASS. Reverted and diff-verified. See §Gap Resolution |

**Score:** 34/39 truths verified — 31 by the independent pass, 1 (row 37) resolving the gap, and
**2 (rows 38, 39) self-verified by the fix's author, not independently confirmed**. Remaining:
4 HUMAN (rows 32, 33, 34, 36), 1 present-but-behavior-unverified (row 35), **0 FAILED**.

*(The previous pass's score line read "31/37 … 5 human" — its counts summed to 38 against a 37-row
table, and "5 human" counted the frontmatter's `human_verification` entries rather than the table's
HUMAN rows. Recounted here by status cell so the arithmetic actually closes.)*

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `frontend/index.html` | `#round-doc` with `tabindex="0"`; 2 new ids; two ARIA triples; zero renames/deletions | ✓ VERIFIED | id count 80 → 82; `tabindex` 0 → 1; the diff's `-` id lines are in-place edits of the same ids |
| `frontend/app.js` | Shift submit listener; F1-a/b/c hand-back; `appEl`; `syncBackgroundInert()` + 5 call sites; tier focus-on-open + flag reset; Escape dispatcher; two F1-d hand-backs; S8-1 copy | ✓ VERIFIED | All present and behaviorally exercised (truths 9-11, 17-21, 26) |
| `frontend/style.css` | byte-unchanged (deliberate) | ✓ VERIFIED | blob `95cb22ee…` identical at phase base and HEAD |
| `frontend/vendor/` | exactly one file | ✓ VERIFIED | `marked.min.js` |
| `scripts/check-05-ui-uat.py`, `scripts/probe-07-focus-composite.py` | `probe-07` unchanged and re-run; `check-05` **amended at `63fba08`** (user ruling) | ✓ VERIFIED | probe-07 re-ran clean (links-before 0 / links-after 1; ring 2px / `rgb(31,99,189)`; archive composite 3.45:1 ≥ 3.0). `check-05` gained `L5_CONTENT_REGION_MIN_RATIO` + a declaration/assertion split in `_idi06_clearance_assert` + `elH`/`padBoxH` on the census rows — the only authorized exception to D-21. All other assertions and constants untouched; items 1/4/9/10 and check-06 re-run green |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `frontend/index.html:163` (`#round-doc`) | `frontend/style.css:1514` (`[tabindex]:focus-visible`) | Phase 7's enum rule fires on the new attribute, zero CSS | ✓ WIRED | item 10 reads 2px / `rgb(31,99,189)` / `focusVisible true` at the moment `#round-doc` is focused |
| `frontend/app.js` (Shift-only `keyup` listener) | `frontend/index.html:250` (`#btn-annotate`) | release Shift ∧ menu visible ∧ `activeElement === roundDoc` ∧ selection non-collapsed ⇒ `annotateBtn.focus()` | ✓ WIRED | Behavioral probe: `active: 'btn-annotate'` |
| `frontend/app.js` (`hideSelectionMenu`) | `frontend/index.html:163` (`#round-doc`) | `selectionMenu.contains(document.activeElement)` before hiding ⇒ `roundDoc.focus()` | ✓ WIRED | Behavioral probe: Escape and menu-item click both land focus on `#round-doc` |
| `frontend/app.js` (`syncBackgroundInert`) | `frontend/index.html:10` (`#app`) | `appEl.set/removeAttribute('inert')` derived from both modals' `.hidden` | ✓ WIRED | Behavioral probe: `#app` only, every sibling `false`, `body` `false` |
| `frontend/index.html:207/226` (the two `.overlay`s) | `#confirmation-modal-title` / `#tier-modal-title` | `aria-labelledby` → the on-screen `<h3>` | ✓ WIRED | Accessible names read "授权确认" / "选择自检档位" |
| `frontend/app.js` (Escape dispatcher) | `hideSelectionMenu()` / `closeConfirmModal()` / tier close branch | explicit priority table reading the three `.hidden` states | ✓ WIRED | Behavioral probes for all three branches + the negative scope check |
| `frontend/app.js:1162` (`renderAnnotations` empty state) | DESIGN.md §4.1 v1.14 | one-word copy fix | ✓ WIRED | Rendered `#annotation-list .hint` matches verbatim |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `#round-doc` ring | `outline-color` | runtime-resolved `--color-focus` (not hardcoded) | Yes — item 10 reads `rgb(31, 99, 189)` and cross-checks against the token | ✓ FLOWING |
| `#selection-menu` visibility | `.hidden` class | `handleSelectionTrigger` / `hideSelectionMenu` from the live `window.getSelection()` | Yes — behavioral probe reads `hidden` flipping with a real 11-char selection | ✓ FLOWING |
| `#app[inert]` | native `inert` attribute | derived from both modals' `.hidden` | Yes — behavioral probe reads it appear/disappear with open/close | ✓ FLOWING |
| `#annotation-list .hint` | `textContent` | `renderAnnotations` on the p3 fixture | Yes — the rendered string equals the fixed copy | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Escape dismisses the menu and it stays dismissed | bundled chromium, real mouse-drag selection → trusted Shift release → `Escape` ×2 → `ArrowRight` → `'a'` | S1 hidden, S2 hidden, S3 hidden, S3b hidden; focus `round-doc`; selection preserved (len 11) | ✓ PASS |
| Escape closes `#confirmation-modal`, removes `inert`, hands focus back | bundled chromium, `#btn-authorize` → `Escape` (twice) | `{confirmHidden:true, appInert:false, active:'btn-authorize'}` both times | ✓ PASS |
| Escape closes `#tier-modal`, resets the flag, hands focus back | bundled chromium on an awaiting-tier fixture, `Escape` then `refreshChecksAfterStream()` | close → `{tierHidden:true, active:'btn-continue-check'}`; re-pop on re-trigger → `True` | ✓ PASS |
| Out-of-scope overlays ignore Escape | bundled chromium, force-open the three, `Escape` | all three still open | ✓ PASS |
| S8-1 copy in the intended state/position | bundled chromium, p3 fixture | `#annotation-list .hint` == `本轮暂无批注——在右侧文档划词即可批注。` | ✓ PASS |
| Archive round-switch leaves 「处理本轮批注」 unclickable | bundled chromium, archive fixture, `select_option` round 2 | `{hidden:True, disabled:True}` before and after | ✓ PASS |
| E3 empty-state gating | bundled chromium, fill empty / wrong / exact | `disabled` True / True / False | ✓ PASS |
| Item 9 L-5 clearance (Phase 6 gate) | `.venv/bin/python scripts/check-05-ui-uat.py --item 9` | `PASS (16 条断言, 0 FAIL, 0 BLOCKED)`; declared row `[('#round-doc','#doc-panel',778.6,900,-66.6)]` in p3, 0 declared rows in p1/checking | ✓ PASS (was FAIL — resolved at `63fba08`) |
| Item 10 focus-ring census | `.venv/bin/python scripts/check-05-ui-uat.py --item 10` | `PASS (41 条断言, 0 FAIL, 0 BLOCKED)` | ✓ PASS |
| Items 1 / 4 | `.venv/bin/python scripts/check-05-ui-uat.py --item 1` / `--item 4` | `PASS (45)` / `PASS (65)` | ✓ PASS |
| Items 2 / 3 / 6 / 7 / 8 | `.venv/bin/python scripts/check-05-ui-uat.py --item 2,3,6` / `--item 7,8,9` | `PASS (5)` / `PASS (17)` / `PASS (6)` / `PASS (38)` / `PASS (13)` | ✓ PASS |
| pytest baseline | `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped` | ✓ PASS |
| check-01…04, check-06 | `bash scripts/check-0N…` / `.venv/bin/python scripts/check-06-idi05-validation.py` | all PASS (check-06: g1…g6 PASS) | ✓ PASS |
| probe-07 focus composite | `.venv/bin/python scripts/probe-07-focus-composite.py` | links 0 → 1; ring 2px / `rgb(31,99,189)`; archive composite 3.45 ≥ 3.0 | ✓ PASS |

`check-05 --item 5` was not run: it requires `--ai-smoke`, which makes real AI calls. It is not a
Phase 4/6/7 gate for this phase's deliverables and was not claimed by any Phase 8 artifact.

### Probe Execution

No `scripts/*/tests/probe-*.sh` convention exists in this repo; PLAN/SUMMARY declare no probe paths.
The nearest equivalent, `scripts/probe-07-focus-composite.py` (re-run obligation D-04), was executed
from the repo root and passed — see the spot-check table.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| A11Y-02 | idi-08-01 | `#round-doc` gets `tabindex="0"` in the same commit as focus styling | ✓ SATISFIED | `tabindex` 0 → 1 (`bbf9060`, `index.html` only); `:focus-visible` stays 9; the Phase 7 enum rule supplies the ring with zero CSS (truths 6-8) |
| A11Y-03 | idi-08-01 | A keyboard user can genuinely reach selection annotation | ? NEEDS HUMAN | Shift-release gesture + focus hand-off machine-verified (truths 9-11); the keyboard-origin selection extension cannot be automated |
| A11Y-05 | idi-08-02 | Both blocking modals support Escape close | ✓ SATISFIED | Truths 1, 2, 18, 19 (all behavioral) |
| A11Y-06 | idi-08-02 | Both modals get `role="dialog"` + `aria-modal="true"` | ✓ SATISFIED | Truths 3, 16, 17 — the declaration is made true by `inert` |
| A11Y-08 | idi-08-03 | Keyboard reachability manual acceptance | ? NEEDS HUMAN | Machine half green (truths 32, 36); full enumeration is on-screen |
| REG-03 | idi-08-03 | All `b9664e0` manual acceptance items re-run | ? NEEDS HUMAN | Truth 34; the keyboard-dependent halves stay human |

No orphaned requirements: all six IDs mapped to Phase 8 in REQUIREMENTS.md appear in a plan's
`requirements:` field (01 → A11Y-02/03, 02 → A11Y-05/06, 03 → A11Y-08/REG-03), and no plan declares
an ID that REQUIREMENTS.md does not map to Phase 8. REQUIREMENTS.md showing all six as Complete is
expected — each plan's completion commit flips its own IDs, and the ROADMAP Phase 8 row still reads
`In Progress` because `phase.complete` has not run. Not a discrepancy.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `.claude/settings.local.json` | 23 | `Bash(node -e ' *)` pre-approves arbitrary JavaScript execution | ⚠️ Warning | Added by this phase; collapses the permission prompt for the most direct execution vector. Code review raised it as WR-02. **Owner decision taken 2026-09-24: KEEP** — its marginal exposure is comparable to the pre-existing `Bash(git *)` (line 13), and removing it would break the pipeline's own inline `node -e` calls. Registered as an accepted trust-boundary choice, not an open gap |
| `.claude/settings.local.json` | 17-21 | Session-scoped probe grants (`P=… && echo … sed …`, `sed -n '/function autoResolve/…'`) | ℹ️ Info | One-off investigative grants recorded by this phase; no exposure beyond read-only inspection |
| `frontend/app.js` / `frontend/index.html` | — | `TBD` / `FIXME` / `XXX` / `TODO` / `HACK` / `PLACEHOLDER` | — | None found. Debt-marker gate clean |
| `frontend/app.js` | 1342-1349 | Comment enumerates call sites and explicitly drops the numeral ("要核数用 grep 现算") | ℹ️ Info | The stale-prose failure mode was pre-empted rather than repeated (IN-04 from review was fixed this way) |

### SUMMARY ↔ HEAD Disagreements (registered, not gaps)

1. **SUMMARY 03 §Newly discovered finding is stale.** It registers "Escape cannot dismiss the
   selection menu" as a phase-introduced defect, **not fixed**, with the recommended disposition left
   to the user. HEAD is past that: `62dfd3e` suppressed one keyup (incomplete), and `09b170d` replaced
   it with selection-identity dismissal (`dismissedSelectionRange` / `isDismissedSelectionLive`).
   Behavioral probe at HEAD: the menu stays hidden across a second Escape, an `ArrowRight`, and an
   `'a'`. HEAD wins; this is a disagreement, not a gap.
2. **SUMMARY 03's keyboard-path step 5** ("focus does return to `#round-doc`, but the menu does not
   stay dismissed") describes the pre-fix tree only. At HEAD the dismissal is durable.
3. **Line anchors in the plans and SUMMARYs have drifted** (plan 01's fence comments +24 lines, plan
   02's comments/attributes further). HEAD's element positions are the authority; every claim above
   was re-anchored by id/selector/verbatim string.
4. **SUMMARY 03's close-out claim "All plan-level gates are green" is true only for the gate set it
   ran** (items 1 / 4 / 10 + check-01…04). It is false for the ROADMAP Gate line "Phase 4/6/7 全部
   gate 仍通过" — item 9 was never re-run. This one *is* the gap (gaps[0]), not a mere disagreement.
5. **Archive-path mechanism misattribution (SUMMARY 03 §Deviation 1)** — the archive round-switch does
   not travel through `updateFrozenPresentation`; it routes to `loadArchiveRoundDoc`, which touches
   neither the `.hidden` class nor the `disabled` flag. The acceptance criterion still holds and was
   measured (truth 29), only the attributed mechanism is wrong. Registered, not a gap.

### Human Verification Required

1. **A11Y-08 Tab-order census** — Tab through a phase-3 and a phase-5 self-check project; confirm every
   interactive control is reachable and `#round-doc` sits at position 2 (after `#round-switcher`,
   before `#btn-authorize` when visible). The machine half is green; the enumeration is on-screen.
2. **A11Y-03 keyboard-selection leg** — Tab to the document area, hold Shift and press Arrow to extend
   past one character, release Shift; expect the menu with focus on `批注`. Then Escape: the menu must
   stay dismissed, focus must return to `#round-doc`, and the selection must survive so Shift+Arrow can
   keep extending.
3. **REG-03 re-run** — items 1, 2, 3, 5, 6 and the rewritten item 4 step 3, by hand.
4. **Backstop UI-consideration truths** (E1…E6 loading / error / overflow / long-text / empty /
   partial) — declared `verification: backstop`; confirm each is either observable or genuinely not
   applicable to that element.
5. **The phase-5 zero-height `#round-doc` Tab stop** — decide whether a 351 × 0 Tab stop with a
   hairline ring is acceptable or the attribute should be conditional.

**Item 6 of the previous pass ("the L-5 gate adjudication") is closed** — the user ruled on
2026-09-24 and the resolution shipped in `63fba08`. See §Gap Resolution. It is no longer a human item.

### Gap Resolution

**The one gap is closed. This section replaces the previous §Gaps Summary.**

The gap was real and correctly diagnosed by the independent pass: Phase 8's `tabindex="0"` on
`#round-doc` pulled it into Phase 6's L-5 clearance judged set via `FOCUSABLE_SELECTOR`'s
`[tabindex]` arm, turning `check-05 --item 9` from PASS into FAIL on row
`('#round-doc', '#doc-panel', -66.6)` and making ROADMAP's Phase 8 gate line
**"Phase 4/6/7 全部 gate 仍通过"** false. The miss at close-out is also correctly diagnosed: plan 03's
must_haves narrowed the "still green" truth to `check-01…04`, so the executor's sweep (items 1 / 4 /
10) never re-ran item 9 while recording "All plan-level gates are green" — a scope reduction against
the ROADMAP Gate line.

**Disposition (user, 2026-09-24): amend the gate's scope.** Implemented in `63fba08`. A focusable
element at least half its clipping container's padding-box height is a **content region, not a
control**: it is DECLARED (reported per-row through `info()`, never silently dropped) instead of
asserted. Controls are still asserted. If the declaration set ever consumed the whole judged set the
assertion goes `blocked(...)`, not PASS. The criterion is an objective ratio, deliberately **not** an
element-name allowlist, so it cannot quietly widen to cover controls.

**Why not the gate's own prescribed remedy:** L-5's documented repair is to raise the offending
container's padding. For this element that makes matters *worse* — the padding lands above it and
pushes it further down. And its height is content-driven with no upper bound, so no layout change can
satisfy a fixed 4px clearance robustly.

**One correction to the earlier gap text.** It implied the violation was *structural* — that an
element taller than its container can never satisfy L-5. **That is false here, and it was my
hypothesis, refuted by measurement:** `#round-doc` is 778.64px inside a 900px container. The real
geometry is that it sits 188px down, so it overflows the bottom by 66.64px at the sample's default
scroll; the browser's scroll-into-view lands it at 0.36px clearance (the same clip D-02 measured as
3.64px). Its actual property is that clearance sits exactly on the threshold while its height is
unbounded. The disposition is unchanged either way, but the reasoning should not be inherited as
written.

**Independence of this resolution — stated plainly.** The two delegated re-verification attempts
both stalled (600s watchdog, twice) without writing anything, and the user then explicitly authorized
the orchestrator to write this report. So the gap-closure evidence is **first-party, not third-party**.
It is mechanical and reproducible (both mutation tests can be re-run from the commands in the
frontmatter), but a reader should treat the resolution as *asserted by its author* rather than
*confirmed independently*. Everything else in this report is unaffected: the truths above came from
the independent pass and are carried forward unchanged.

**Registered costs (not tidied away).** The amendment invalidates the fingerprints of the **4**
phases listing `check-05-ui-uat.py` in `covered_files` (`idi-04.1-radix`, `idi-05`, `idi-06`,
`idi-07`) — D-21/A-4 said 5; the measured count is 4, since `idi-04` mentions the script in prose but
never listed it. Those digests were deliberately **not** recomputed: refreshing one asserts "nothing
changed since verification", which is false because `frontend/style.css` genuinely changed under
phases 5-8. The staleness is kept as a visible signal; correct closure is re-running those phases'
verify-work. Separately, `idi-04`'s digest is already stale for an unrelated pre-existing reason and
was left alone.

Separately, and independent of the gap: the keyboard-origin selection legs (A11Y-08, A11Y-03's
selection half, REG-03's keyboard-dependent items) remain human, as the ROADMAP §Manual checks
requires — an automated FAIL there is a harness limitation, not a defect, and none was recorded here.
The `Bash(node -e ' *)` grant this phase added to `.claude/settings.local.json` is a real security
finding; the repository owner reviewed it on 2026-09-24 and chose to **keep** it as a trust-boundary
decision (its marginal exposure is comparable to the pre-existing `Bash(git *)` grant, and removing
it would break the pipeline's own inline `node -e` calls). Registered, not a gap.

---

_Verified: 2026-09-24T15:52:00Z (independent; see the timestamp note — this stamp is mislabelled local time)_
_Re-verified: 2026-09-24T13:23:27Z (gap-closure portion self-verified by the orchestrator, under explicit user authorization)_
_Verifier: [CL] (gsd-verifier, first pass) · [CL] orchestrator (gap resolution)_

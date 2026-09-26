---
phase: idi-08-accessibility-semantics-and-keyboard
plan: 03
subsystem: ui
tags: [accessibility, keyboard, regression-verification, manual-uat, copy-fix, escape, focus-management]

# Dependency graph
requires:
  - phase: idi-08-accessibility-semantics-and-keyboard
    plan: 01
    provides: "the #round-doc Tab stop + the Shift-release submit listener + the F1-a/b/c hand-back inside hideSelectionMenu() — every A11Y-08 census reading below measures that work"
  - phase: idi-08-accessibility-semantics-and-keyboard
    plan: 02
    provides: "the Escape single-point dispatcher whose menu branch this plan's new finding is measured against"
  - phase: 260917-fqh-b9664e0-hidden-flex
    provides: "the REG-02 structural fix (inline error anchored to the block-flow container, cleared on the next action) whose two gates this plan re-runs"
provides:
  - "S8-1: the empty-annotation copy now points at the right-hand doc panel (app.js:1162, one word), aligning it with DESIGN.md §4.1 v1.14"
  - "REG-03: all six b9664e0 manual acceptance items re-run with step-by-step observations; item 4 rewritten for D-05's new gesture; the archive round-switch re-verified"
  - "A11Y-08: the full Tab-order census in two states (phase3 + phase5_checking) with #round-doc's position recorded per §K-1.7"
  - "the phase's three close-out registrations (fingerprint obligation, pre-existing D-26 todo, known gaps D-17 / D-19) plus the [v1.14 P8] Deferred Item's disposition"
  - "a measured, mechanism-isolated new defect: Escape cannot dismiss the selection menu (registered, NOT fixed — see §Newly discovered finding)"
affects:
  - "the phase-8 verifier / end-of-phase UAT harvest (the new Escape finding and the phase-5 zero-height Tab stop are handed over)"
  - "any future editor of the Escape dispatcher or of hideSelectionMenu()"
  - "v2 A11Y-V2-02 (role + focus trap for the other three overlays)"

# Actuals (#2632) — pairs with the plan's estimate (56000 tokens) to calibrate future estimates.
actuals:
  tokens: 151       # chars/4 over the realized diff (606 chars) — frontend/app.js only
  tasks: 3
  commits: 1        # MEASURED: git rev-list --count 20b99d1..HEAD (#3968); tasks 2 and 3 change no file by design
  plan_head_before: 20b99d1af81479a63f154c40a3d68b606d85910b

# Tech tracking
tech-stack:
  added: []       # zero new runtime deps, zero build steps (hard rule 6); frontend/vendor/ still exactly marked.min.js
  patterns:
    - "Verification-by-discriminating-controls: every green claim is paired with a control that changes exactly one input and shows the reading flips (the inertness-probe discipline plan 02 established, applied here to the Escape finding)"
    - "Split the key event to isolate a mechanism: pressing Escape as keydown-only vs keyup-only separates 'the dispatcher ran' from 'a later listener undid it'"
    - "Census by element with the visible+focusable filter, never by selector count (the project's standing rule since G-idi-05-1)"
    - "Register the false-green risk next to the gate it protects: the plan's own '9 not 6 / 219 not 225' arithmetic traps are recorded in the SUMMARY, not just obeyed"

key-files:
  created: []
  modified:
    - frontend/app.js   # app.js:1162 — one word of empty-state copy (1 insertion, 1 deletion); nothing else in frontend/ or scripts/ changes

key-decisions:
  - "The S8-1 edit is an authorized exception to hard rule 5, not a violation of it: it lands inside renderAnnotations (app.js:1156-1212), which ROADMAP §全局硬规则 5, the UI-SPEC Do-Not-Touch List and 08-CONTEXT §明确不含 all list as untouchable. Two authorization sources are recorded verbatim in §The S8-1 authorization below. The exception covers exactly one word at app.js:1162 — the do-not-touch list is neither overturned nor widened."
  - "REG-02 gate ②'s baseline is the MEASURED 9, not the 6 that 08-CONTEXT D-21 carries. D-21's 6 came from a b9664e0-era gate; copying it would build a gate that can never fail. Same class of error as the pytest '225' trap."
  - "pytest's criterion is '219 passed / 6 deselected / 225 collected' and the four numbers are recorded verbatim. 219 is the PASS count and 225 the COLLECT count; under -m 'not slow' the six slow-marked end-to-end tests are DESELECTED (pytest's own label), which the project's prose has always called 'skipped'. Same six tests either way."
  - "The new Escape finding is REGISTERED, not fixed, even though Task 2's action authorizes a minimal fix for phase-introduced regressions. Two reasons: (a) the plan-level <verification> states 'this plan changes only one piece of copy — apart from one word at app.js:1162 the rest of frontend/ and scripts/ is byte-unchanged', which a fix would falsify; (b) the correct fix is a design choice among at least three plausible shapes (suppress the following keyup; defer the hand-back past the keyup; move the hand-back out of the shared hideSelectionMenu choke point), and handleSelectionTrigger's body — the function the keyup lands in — is on the Do-Not-Touch list. Rule 4 applies: a design choice the user owns is not the executor's to self-author."
  - "The archive round-switch does NOT travel through updateFrozenPresentation (see §Deviation 1): the archive switcher routes to loadArchiveRoundDoc, which touches neither the hidden class nor the disabled flag. The measured outcome is stronger than the plan predicted — the button stays both hidden AND disabled after the switch."
  - "The phase-5 zero-height Tab stop is a consequence of plan 01's unconditional tabindex=\"0\" first measured here. Registered, not fixed: Task 3 is a zero-source-change task, and a conditional attribute would be a design change to a plan-01 deliverable."

patterns-established:
  - "Isolate a cross-mechanism defect by splitting the key event (keydown vs keyup) rather than by reading the final state, so 'who undid what' is a measurement instead of a hypothesis"
  - "Three controls for one finding: focus outside the menu, collapsed selection, and a bare keyup with no Escape at all — each flips exactly one input"
  - "A gate baseline is taken from disk measurement and the stale upstream figure is named in the SUMMARY, so a later reader cannot re-derive the false gate"

requirements-completed: [A11Y-08, REG-03]

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "The empty-annotation copy points at the right-hand doc panel and appears in the correct state and position (phase 3, current round, zero annotations)."
    verification:
      - kind: automated_ui
        ref: "grep -c '在右侧文档划词即可批注' frontend/app.js == 1 ; grep -c '在左侧文档划词即可批注' == 0"
        status: pass
      - kind: automated_ui
        ref: "browser, p3 fixture, round 2, 0 annotation items: #annotation-list .hint textContent == '本轮暂无批注——在右侧文档划词即可批注。' (the string appears in the intended state and position, not merely in the file)"
        status: pass
    human_judgment: true
    rationale: "The plan designates this a <human-check> ('grep can prove the string changed, not that it appears in the right state and position'). The state+position half is machine-observed above; the user-visible reading stays in the end-of-phase harvest per workflow.human_verify_mode=end-of-phase."
  - id: D2
    description: "REG-02 gate ①: .inline-error has exactly one rule in frontend/style.css (the error-rendering path was not rewritten)."
    verification:
      - kind: automated_ui
        ref: "grep -c 'inline-error' frontend/style.css == 1 (baseline measured 1 on HEAD before the change)"
        status: pass
    human_judgment: false
  - id: D3
    description: "REG-02 gate ②: the clearInlineError() call-site count never decreases (>= 9; measured baseline 9, deliberately NOT 08-CONTEXT D-21's stale 6)."
    verification:
      - kind: automated_ui
        ref: "grep -c 'clearInlineError();' frontend/app.js == 9 (>= 9 passes) ; grep -c 'clearInlineError' == 10 (9 calls + 1 definition)"
        status: pass
    human_judgment: false
  - id: D4
    description: "The pytest baseline is unchanged: the backend is untouched and the suite is green at the recorded arithmetic."
    verification:
      - kind: unit
        ref: ".venv/bin/python -m pytest -q -m 'not slow' => '219 passed, 6 deselected, 1 warning in 6.53s' ; --collect-only => '219/225 tests collected (6 deselected)' ; unfiltered --collect-only => '225 tests collected'"
        status: pass
    human_judgment: false
  - id: D5
    description: "The four invariant guards still pass on the close-out tree, and the hard-rule-2 arithmetic trap is registered (grep counts 5 hit lines, the gate counts 1 declaration)."
    verification:
      - kind: other
        ref: "check-01 PASS / check-03 PASS / check-04 PASS (all exit 0) ; check-02 => 'PASS: 0 failures' with ORDER 0.363 ; grep -c '^\\.hidden {' == 1 ; grep -c '!important' == 5 hit lines vs check-04's 1 declaration"
        status: pass
    human_judgment: false
  - id: D6
    description: "REG-03 items 1, 2, 3, 5, 6 re-run with step-by-step observations (draft-only view; no placeholder + hidden round switcher; archive read-only state; the SSE banner's three states; inline error position + replacement)."
    verification:
      - kind: automated_ui
        ref: "browser re-run over the five disk fixtures, item by item — see §REG-03 observation record for every reading (p12 draft-only; p3 rounds-hint none; checking round-switcher none; archive hidden+disabled+authorize-row hidden+switcher visible; banner none->block('事件流已断开,正在自动重连……')->none + fatal class on a deterministic non-200; error prevSibling==#enter-form, errTop 110 >= formBottom 102, re-click replaces rather than accumulates)"
        status: pass
    human_judgment: false
  - id: D7
    description: "Rewritten item 4: releasing Shift hands focus into #btn-annotate and Enter completes a real annotation end to end."
    requirement: REG-03
    verification:
      - kind: automated_ui
        ref: "real mouse-drag selection (11 chars, 'Round 2 · 检') -> menu shown (hidden=false, display flex) -> trusted Shift keyup -> activeElement == btn-annotate with ring 2px / rgb(31, 99, 189) / focusVisible true"
        status: pass
      - kind: automated_ui
        ref: "trusted Enter on #btn-annotate -> real window.prompt (type=prompt, '写批注(将绑定到划选原文)') -> accepted -> #annotation-list gains 1 item '「Round 2 · 检」探针批注:idi-08-03 待处理' ; #pending-count '本轮批注未处理 0' -> '本轮批注未处理 1' ; docs/discuss-round-2.annotations.json written {id: a2-01, quote: 'Round 2 · 检', type: 'comment', note: '探针批注:idi-08-03', status: 'pending'}"
        status: pass
    human_judgment: true
    rationale: "The rewritten step 3 (hold Shift, press Arrow repeatedly to extend the selection) cannot be automated here: a trusted CDP Shift+Arrow drive produced NO selection (collapsed, len 0) in 12 presses. The app is not blocking it — computed user-select is 'auto' on #round-doc, .markdown-body and body, and a programmatic Range selection over #round-doc yields 301 chars — so the residual explanation is environmental (Chrome's caret browsing is off by default, and Shift+Arrow needs it in a non-editable div), which is exactly what a human must settle. Per ROADMAP Phase 8 §Manual checks this automated non-result is NOT a functional-defect call. The keyboard-origin selection half therefore stays a named manual check."
  - id: D8
    description: "The archive round-switch re-verification (D-23): after switching rounds in the read-only archive state, '处理本轮批注' is still not clickable."
    requirement: REG-03
    verification:
      - kind: automated_ui
        ref: "archive fixture: title '总设计文档(只读归档)', #btn-process-round hidden + disabled=true ; select_option('2') -> title '第 2 轮(归档·只读)' (switch confirmed) -> still hidden + disabled=true"
        status: pass
    human_judgment: false
  - id: D9
    description: "A11Y-08: the full Tab-order census in two states, with #round-doc's position recorded per §K-1.7 rather than merely 'Tab can reach it'."
    requirement: A11Y-08
    verification:
      - kind: automated_ui
        ref: "p3: judged set 10 (visible AND focusable), all 10 Tab-reached, #round-doc at position 2 — immediately after #round-switcher and immediately before #btn-authorize (the #authorize-row button, visible in that state), ring 2px / rgb(31, 99, 189) / offset 2px with focusVisible true"
        status: pass
      - kind: automated_ui
        ref: "checking: judged set 8, all 8 Tab-reached, no visible control missing from the order"
        status: pass
      - kind: automated_ui
        ref: "check-05 --item 10 => PASS (41 assertions, 0 FAIL, 0 BLOCKED), [p3] judged set 10, uncovered [] — agrees with the independent census above"
        status: pass
    human_judgment: true
    rationale: "The plan mandates A11Y-08 as a named manual check: keyboard text selection cannot be automated here (not even contenteditable can be selected), and 'every interactive control is reachable' is an enumeration a human should confirm on screen. The machine half above is complete; the keyboard-selection path and the on-screen reading of the ring stay human. The phase-5 zero-height Tab stop and the Escape finding below are attached to this entry."
  - id: D10
    description: "The phase's close-out registrations: the fingerprint obligation, the pre-existing D-26 todo, the two known gaps (D-17 / D-19), and the [v1.14 P8] Deferred Item's disposition."
    verification: []
    human_judgment: true
    rationale: "Prose registrations with no machine assertion; the verifier must classify them (see the four sections under §Close-out registrations)."
  - id: D11
    description: "Newly discovered, phase-introduced defect: Escape cannot dismiss the selection menu while a live in-document selection exists — the menu re-opens on the Escape keyup. Registered, NOT fixed."
    verification:
      - kind: automated_ui
        ref: "split key event: keydown Escape (target btn-annotate) -> menu hidden + focus handed to #round-doc ; keyup Escape (target now #round-doc) -> menu visible again. Three controls: focus outside the menu -> stays hidden ; collapsed selection -> stays hidden ; bare keyup with no Escape -> re-appears"
        status: fail
    human_judgment: true
    rationale: "Measured with trusted events and three discriminating controls, and the mechanism is proven by an event log (not a text-selection failure, so the 'do not call a defect on an automated FAIL' rule does not reach it) — but the user must adjudicate, because the fix is a design choice and the plan-level verification forbids a second source change. See §Newly discovered finding."

# Metrics
duration: 16min
completed: 2026-09-24
status: complete
---

# Phase idi-08 Plan 03: Close-out Verification — S8-1 Copy Fix, REG-03 Re-run and the A11Y-08 Tab-Order Census Summary

**One word of empty-state copy corrected against the authoritative design doc, all six b9664e0 manual acceptance items re-run with per-step observations, the full Tab-order census recorded in two states — and a phase-introduced Escape defect found by the re-run, isolated with three controls, and registered rather than papered over**

## Performance

- **Duration:** 16 min (05:55:52Z → 06:12:11Z)
- **Started:** 2026-09-24T05:55:52Z
- **Completed:** 2026-09-24T06:12:11Z
- **Tasks:** 3 (Task 1 produced a production commit; Tasks 2 and 3 change no file by design)
- **Files modified:** 1 (`frontend/app.js`, +1/−1 — one word)
- **Realized diff:** 606 chars ⇒ 151 tokens (plan estimate was 56000)
- **Commits:** 1 (measured: `git rev-list --count 20b99d1..HEAD`)

## Accomplishments

- **S8-1 landed as exactly one word.** `app.js:1162` reads `本轮暂无批注——在右侧文档划词即可批注。`; the diff is 1 insertion / 1 deletion, the punctuation and the dash are byte-identical, and the historical-round string at `app.js:1164` (`该轮暂无批注。`) is untouched. `node --check` OK.
- **The string was verified in situ, not just in the file:** in the p3 fixture at round 2 with zero annotation items, `#annotation-list .hint` reads exactly `本轮暂无批注——在右侧文档划词即可批注。` — the correct state and the correct position.
- **Both REG-02 gates hold at their measured baselines:** `inline-error` in `style.css` = 1, `clearInlineError();` in `app.js` = 9. The `9` is the disk measurement; `08-CONTEXT` D-21's `6` is a `b9664e0`-era figure that would have built a gate which can never fail.
- **pytest baseline recorded as four verbatim numbers:** `219 passed, 6 deselected, 1 warning in 6.53s`; `--collect-only` = `219/225 tests collected (6 deselected)`; unfiltered = `225 tests collected`. 219 is the pass count, 225 the collect count — not interchangeable.
- **All four invariant guards green on the close-out tree:** `check-01` PASS, `check-02` `PASS: 0 failures` with `ORDER 0.363`, `check-03` PASS, `check-04` PASS. The hard-rule-2 arithmetic trap is registered: `grep -c '!important'` returns **5** hit lines (4 comment prose + 1 declaration) while the gate counts **1** declaration.
- **REG-03 items 1, 2, 3, 5, 6 re-run with step-by-step observations** over the five disk fixtures — including the SSE banner's three states, which needed a second backend instance so the resident dev server was never disturbed.
- **Item 4 executed in its rewritten form:** a real selection → menu → trusted Shift release → focus on `#btn-annotate` → trusted Enter → real `window.prompt` → an annotation actually appears in the main-pane stream and `#pending-count` increments 0 → 1, with the annotation file written to disk.
- **The archive round-switch re-verified (D-23):** after switching rounds in the read-only archive state, `#btn-process-round` stays hidden **and** `disabled === true`.
- **The A11Y-08 Tab-order census is complete for two states.** In phase 3 the judged set is 10 elements, all 10 Tab-reached, and `#round-doc` sits at **position 2 — immediately after `#round-switcher`, immediately before `#btn-authorize`** (the `#authorize-row` button, visible in that state), exactly §K-1.7's contract. In the phase-5 self-check view the judged set is 8 and all 8 are reached.
- **Wave 1 and wave 2 are not regressed:** `role=` 2, `aria-modal` 2, `aria-labelledby` 2, `id="` 82, `tabindex` 1, `:focus-visible` 9, `syncBackgroundInert` 6, `tierModalShown` reset present, both F1-d hand-backs present, and `hideSelectionMenu()` still takes its predicate (L1347) before the hide (L1348).
- **The close-out registrations are landed:** the fingerprint obligation, the pre-existing `idi-04.1-radix` todo (D-26), both known gaps (D-17 / D-19), and the `[v1.14 P8]` Deferred Item's disposition.
- **A phase-introduced Escape defect was found, isolated, and registered** rather than hidden — see §Newly discovered finding.

## Task Commits

Each task was committed atomically where it produced a change:

1. **Task 1: S8-1 copy fix + two REG-02 gates + pytest baseline + four guards** — `fa7813a` (fix)
2. **Task 2: REG-03 six-item re-run + archive round-switch re-verification** — no commit (the plan specifies zero file changes unless the re-run finds a regression; it found one, and it is registered rather than fixed — see §Deviation 1 and §Newly discovered finding)
3. **Task 3: A11Y-08 Tab-order census + close-out registrations** — no commit (the plan specifies a zero-source-change census/registration task)

**Plan metadata:** (this SUMMARY commit)

_Note: Task 2 having no commit follows the precedent plan 01 set for a zero-file-change task; the atomic close-out invariant is satisfied because the one production commit exists and this SUMMARY is the deferred close-out._

## Files Created/Modified

- `frontend/app.js` — one line: `app.js:1162`'s empty-state string changes `在左侧文档` → `在右侧文档`. Nothing else in `frontend/` or `scripts/` changes; `frontend/style.css`, `scripts/check-05-ui-uat.py`, `scripts/probe-07-focus-composite.py` and `frontend/vendor/` are byte-identical to HEAD.

## The S8-1 authorization (required registration)

**This edit lands inside a symbol hard rule 5 lists as untouchable. It is an authorized exception, not a violation — and the exception covers exactly one word.**

`frontend/app.js:1162` sits inside `renderAnnotations` (`app.js:1156-1212`), and `renderAnnotations` is listed as **do-not-touch** in three places at once: **ROADMAP §全局硬规则 5**, **`idi-08-UI-SPEC.md` §Do-Not-Touch List (inherited section)** and **`08-CONTEXT.md` §明确不含** (the stated reason being an already-accepted path).

**Registration, verbatim as the plan requires:** 本次编辑在 `renderAnnotations`(`app.js:1156-1212`)内部,由用户 2026-09-23 的 S8-1 裁定(`idi-08-UI-SPEC.md` §Sign-Off Items)与 §改动面 授权;**例外仅限 `app.js:1162` 的一个词**,硬规则 5 的不得触碰清单**未被推翻、也未扩大**。

**The two authorization sources, verbatim:**

1. **`idi-08-UI-SPEC.md` §Sign-Off Items — the S8-1 row's 「用户裁定(2026-09-23)」 column:**
   > ✅ **裁定「改」** —— `本轮暂无批注——在左侧文档划词即可批注。` → **`本轮暂无批注——在右侧文档划词即可批注。`**(`app.js:1121`,仅此一个词)

2. **`idi-08-UI-SPEC.md` §本阶段的改动面(唯一事实) — the authorizing row:**
   > | `frontend/app.js` | **`app.js:1121` 的一处用户可见字符串**:`在左侧文档` → `在右侧文档`(空态文案;**仅此一个词**,见 §Sign-Off Items S8-1) | S8-1(用户 2026-09-23 裁定) |

**The rationale S8-1 rests on** (UI-SPEC §Sign-Off Items, four points): ① it contradicts the **sole authoritative design document** — `DESIGN.md` §4.1 states 「主区(左,自适应宽度;内容列 768px 居中)」 / 「文档面板(右,可折叠)」 (v1.14 moved the session stream into the main pane and the document area to a collapsible right-hand panel); ② `06-UI-SPEC.md`'s checker had already registered this string as **known-stale and explicitly assigned it to "the phase that owns `app.js` (Phase 8)"**; ③ it is **one word**, in a file this phase already changes — zero new strings, zero new elements, zero new dependencies; ④ leaving it would **mislead the user on the very keyboard path this phase opens**.

**Line-number note (registered so the anchors do not look inconsistent):** the UI-SPEC's Sign-Off table and §Copywriting Contract still say `app.js:1121`; that is the pre-wave-1 anchor. On HEAD the target is **`app.js:1162`** — wave 1 inserted an 18-line fence comment above `#round-doc` in `index.html` and wave 3's plan re-measured `app.js` at execution time. The plan's own anchor (`app.js:1162`) is the one that matched disk. The string itself, not the number, is the identifier.

**What the exception does NOT cover (checked, all clean):**
- No other line of `renderAnnotations` was touched — `git diff` is 1 insertion / 1 deletion, both on L1162.
- `app.js:1164`'s historical-round string `该轮暂无批注。` is byte-identical (the plan's `<fails_when>` for this gate: a count of 2 would have meant this line was touched by accident; the count is 1).
- The function's write path is still `textContent`-only — `document.createElement` / `className` / `textContent` are untouched, so the XSS mitigation (T-260916-01) is intact and no HTML-parsing write was introduced.
- The exception is **not** a precedent: `renderAnnotations` remains on the do-not-touch list for every other purpose.

## Decisions Made

- **The S8-1 edit is authorized, and the authorization is recorded rather than assumed** — a reader checking the diff against hard rule 5 would otherwise read a legitimate one-word fix as a violation. Both authorizing sources are quoted verbatim above.
- **REG-02 gate ② uses the measured 9, never D-21's 6.** D-21's figure came from a `b9664e0`-era gate; adopting it would produce a gate that can never fail — the same failure class as the pytest `225` trap the plan warns about twice. The baseline was re-measured on HEAD before the change and re-measured after: 9 both times.
- **pytest's four numbers are recorded verbatim, and the `deselected`/`skipped` label difference is stated rather than smoothed over.** `-m "not slow"` makes pytest report the six `slow`-marked end-to-end tests as **deselected**; the project's prose (08-CONTEXT line 22 included) has always called the same six "skipped". Both labels are recorded so the numbers cannot be mistaken for a drift.
- **The two REG-02 gates are NOT written into `scripts/check-05-ui-uat.py` (D-21 / A-4).** That file is in the `covered_files` of five live reports; adding assertions there would destroy the phase's zero-fingerprint-debt property on the spot. The registered cost stands: these two are not resident guards, so whoever next edits `frontend/style.css` will not be stopped automatically.
- **The new Escape finding is registered, not fixed** — see the decision in the frontmatter and §Newly discovered finding for the two reasons (the plan-level verification's "only one word changes" contract, and the fix being a design choice among three shapes in code that is partly on the do-not-touch list).
- **`updateFrozenPresentation` is not the archive switch's reset path** — the plan's D-23 mechanism description does not hold for the archive switcher; the measured path is `loadArchiveRoundDoc`, which resets nothing. See §Deviation 1.
- **The phase-5 zero-height `#round-doc` Tab stop is registered, not fixed** — it is a consequence of plan 01's unconditional `tabindex="0"`, first measured here; a conditional attribute would be a design change to a plan-01 deliverable, and Task 3 is explicitly a zero-source-change task.
- **`WINDOWS.md` refused the write, as the dispatch predicted.** `gsd-tools windows append` returns: *"Ledger table in .planning/WINDOWS.md disagrees with the fenced JSON entries (the sole source of truth) for row id(s): 17."* The entry is therefore recorded here and in STATE.md instead, per the dispatch instruction not to fight the file.

## Deviations from Plan

**No production-code auto-fix was needed for Task 1** — it matched the plan exactly (one word, one commit). What follows are **plan-premise registrations** and **one newly discovered defect**, in the same class plans 01 and 02 recorded: measurements that contradict a plan statement, and a finding that is deliberately not "fixed".

### Plan-premise corrections (recorded, deliberately not "fixed")

**1. [Rule 1 - Plan premise] The archive round-switch does NOT travel through `updateFrozenPresentation`; the reset path the plan names is not on that route**

- **Found during:** Task 2 (the D-23 archive round-switch re-verification)
- **Issue:** The plan's Task 2 action and D-23 both say the switch goes 「走 `updateFrozenPresentation` 的复位路径(`app.js:1219` 会把 `applyArchiveView` 设的 `disabled = true` 复位 —— Pitfall 3 UI-6.3 的现场)」. Measured: `updateFrozenPresentation` has **exactly one call site** — `app.js:1082`, inside `loadRoundView` — and the archive switcher never reaches it. `roundSwitcher`'s change handler (`app.js:1290-1299`) branches on `currentState === 'mission_complete'` and calls **`loadArchiveRoundDoc(n)`** (`app.js:915-924`), which touches neither `processRoundBtn.classList` nor `processRoundBtn.disabled`. The `disabled = true` that `applyArchiveView` sets at `app.js:871` is therefore **never reset on this route at all**.
- **Consequence — the measured result is *stronger* than the plan predicted:** the plan expected the flag might be reset and relied on the hidden class alone; in fact the button stays **both** hidden **and** disabled after the switch. The Pitfall 3 UI-6.3 scenario the plan describes (a reset re-enabling the button) cannot occur via the archive switcher.
- **Fix:** None. The plan's acceptance criterion — "切轮之后「处理本轮批注」仍不可点" — is satisfied and was measured; only the *mechanism* attributed to it is wrong. No gate was edited and no expected value changed. `applyArchiveView`'s two lines (`app.js:870-871`, hard rule 5) were not touched: `git status` on `frontend/` is empty at Task 2's boundary.
- **Files modified:** none (registration only)
- **Verification:** `grep -n 'updateFrozenPresentation' frontend/app.js` → L1082 (call), L1215 (definition), L1287 (a comment in the switcher's section). `grep -n 'loadArchiveRoundDoc' frontend/app.js` → L915 (definition), L1295 (the archive branch's call). Browser: title `总设计文档(只读归档)` → `select_option('2')` → title `第 2 轮(归档·只读)` (switch confirmed), `#btn-process-round` `hidden=true, disabled=true` before and after.
- **Committed in:** n/a (registration only)

**2. [Rule 1 - Plan premise] A11Y-08's second census state contains a zero-height `#round-doc` Tab stop — a consequence of plan 01, first measured here**

- **Found during:** Task 3 (the phase-5 half of the Tab-order census)
- **Issue:** In the `checking` fixture (state `phase5_checking`), `#round-doc` measures **351 × 0** px with `innerHTML` length 0 — because `applyPhase5View` empties it at `app.js:629` (`roundDoc.innerHTML = ''`) — yet it is the **first** Tab stop in that state and reads `outline-width: 2px, outline-color: rgb(31, 99, 189), focusVisible: true`. Before plan 01 it had no `tabindex` and was not focusable, so this stop is **new in this phase**. The ring on a zero-height box renders as a thin horizontal line rather than a box, which is the degenerate case of D-01's "whole-box ring" — and it is adjacent to Pitfall 6's failure form ("nominally focusable, but you cannot see where focus is").
- **What is NOT claimed:** this is **not** a defect call against the app. The element is present and focusable by design, the ring *is* drawn, and `visible ∧ focusable` correctly excludes it from the harness's judged set (so `check-05 --item 10` is unaffected and stays green). A11Y-08 asks that the Tab order reach every interactive control; a phantom stop is not a missing control.
- **Fix:** None. Task 3 is explicitly a zero-source-change census/registration task, and making the attribute conditional would be a design change to a plan-01 deliverable (Rule 4 territory). Registered for the verifier and for the user.
- **Files modified:** none
- **Verification:** `page.evaluate` on the `checking` fixture: `#round-doc` rect `{w: 351, h: 0}`, `innerHTML.length = 0`, `textContent.length = 0`; first Tab lands on `round-doc` with the ring reading above. Same measurement on `p3` for contrast: rect `{w: 351, h: 778.64}`.
- **Committed in:** n/a (registration only)

### Newly discovered finding (registered, NOT fixed) — the highest-value item in this plan

**Escape cannot dismiss the selection menu: the menu re-opens on the Escape keyup. This is phase-introduced.**

**The observation.** With the selection menu open, focus on `#btn-annotate`, and a live non-collapsed selection inside `#round-doc` (11 chars, `Round 2 · 检`):

| Moment | Menu | `document.activeElement` |
|---|---|---|
| before Escape | visible (`hidden=false`, `display: flex`) | `btn-annotate` |
| after **keydown** Escape | **hidden** ✓ | `round-doc` (F1-a hand-back ran) ✓ |
| after **keyup** Escape | **visible again** ✗ | `round-doc` |

**The mechanism, proven by an event log rather than inferred.** A capture-phase probe on `document` recorded the two events of the single Escape press:

```
keydowns: [{"key": "Escape", "target": "btn-annotate"}]
keyups:   [{"key": "Escape", "target": "round-doc"}]
```

The dispatcher's menu branch runs on **keydown**, calls `hideSelectionMenu()`, which hands focus back to `#round-doc` (F1-a) — **so by the time the keyup arrives, its target is `#round-doc`**. `#round-doc` still carries the pre-existing `roundDoc.addEventListener('keyup', handleSelectionTrigger)` binding (`app.js:1350`), and `handleSelectionTrigger`'s guards all pass (state is `phase3`, the selection is non-collapsed and inside the round doc), so it calls `showSelectionMenu()` and the menu comes straight back.

**Three discriminating controls — each changes exactly one input and the reading flips:**

| Control | Change | Result |
|---|---|---|
| T2 | focus **outside** the menu before Escape (`#ai-route-select`) | menu stays hidden ✓ — keyup target is `ai-route-select`, not `round-doc` |
| T3 | collapse the selection before Escape | menu stays hidden ✓ — `handleSelectionTrigger`'s collapsed-selection guard closes it |
| T4 | no Escape at all: force-hide the menu, refocus `#round-doc`, press any key | **menu re-appears** ✓ — the re-show needs neither Escape nor the dispatcher |

T2 isolates the cause to the **hand-back**; T3 isolates it to the **live selection**; T4 shows the re-show is `handleSelectionTrigger` doing exactly what it has always done, triggered by a keyup it was never meant to see.

**Why it is phase-introduced.** Both legs are new in this phase: the Escape dispatcher is plan 02's deliverable, and the focus hand-back is plan 01's F1-a. Before this phase there was no Escape handling at all (the menu's only closers were the document `mousedown` and the window `scroll` capture), so "Escape dismisses the menu" did not exist to fail.

**Which contract it breaks.** `08-CONTEXT.md` **D-08** — 「Escape 关闭菜单并把焦点交还 `#round-doc`」; `idi-08-UI-SPEC.md` **§K-2.6 step 6** — 「按 Escape → 菜单消失,焦点回到 `#round-doc`」; and REQUIREMENTS' manual acceptance item **「A11Y-03 的键盘划词部分 — … → Escape 关闭并交还焦点」**. The hand-back half holds; the dismissal half does not.

**Why it is registered rather than fixed, even though Task 2's action authorizes a minimal fix for phase-introduced regressions:**

1. **The plan-level `<verification>` forbids a second source change**: 「**本计划只改一处文案。** 除 `frontend/app.js:1162` 的一个词之外,`frontend/` 与 `scripts/` 的其余部分逐字节不变。」 Fixing would falsify a plan-level verification statement — a larger deviation than registering a finding.
2. **The correct fix is a design choice among at least three shapes**, each with different tradeoffs: (a) suppress the following `keyup` from a new document-level capture listener in the dispatcher's section; (b) defer the F1-a hand-back past the keyup (e.g. a task/microtask), which changes timing for all four `hideSelectionMenu()` call sites; (c) move the hand-back out of the shared choke point, which plan 01 explicitly rejected for good reason ("scattering it necessarily misses one of four call sites"). Option (b) also brushes the Do-Not-Touch list indirectly, and option (a) adds a cross-cutting suppression flag. **Rule 4 applies: a design choice the user owns is not the executor's to self-author.**
3. It blocks no gate and is not one of the six REG-03 items, so the phase's close-out is not held up by it.

**How the user should confirm it (the human half).** In a real Chrome session: enter a phase-3 project → select text in the round document (mouse drag is enough) → release Shift so the menu appears with focus on `批注` → press **Escape** → observe that the menu does **not** stay dismissed. One keystroke reproduces it. The keyboard-origin variant (Tab to the document, Shift+Arrow, release Shift) is the same path.

**Recommended disposition:** a follow-up fix inside this phase's own code (it is entirely within `app.js`, touches no stylesheet, and would not disturb the zero-fingerprint-debt property), or a backlog item if the user prefers to close the phase first. It should **not** be downgraded to a known limitation: it is a live defect in a deliverable of the phase whose purpose is keyboard accessibility.

---

**Total deviations:** 0 auto-fixed. **2 plan-premise registrations** + **1 newly discovered phase-introduced defect registered for adjudication**. **Impact on plan:** none on Task 1's delivered copy fix or on any plan-level gate — every gate is green on the close-out tree. The Escape finding affects an acceptance item that the plan placed in Task 3's manual census, and it is surfaced here rather than left implying coverage.

## REG-03 observation record — the six items, step by step

Every reading below is from a browser driven with trusted events (Playwright, bundled chromium, 1440×900) against copies of `scripts/ui-states/` fixtures in a temp directory. `workflow.human_verify_mode` is `end-of-phase`, so nothing halted mid-flight; the machine-observable half is recorded here in full and the experiential remainder is handed to the end-of-phase harvest.

### Item 1 — phase 1-2 project with a draft: only the draft body shows, the "尚无草稿" hint is not visible

Fixture `p12` → derived state `phase12_in_progress`, badge 「阶段 1-2 讨论中」.

| Step | Reading |
|---|---|
| enter the project | `#draft-content` visible, `textContent` length **120** |
| look for the empty-draft hint | `#draft-empty` `display: none`, class `draft-empty hidden`, `getBoundingClientRect` zero, not visible |

**Observation:** the draft body is the only thing rendered in the doc panel; the 「尚无草稿」 hint is not on screen. **PASS.**

### Item 2 — phase 3: no placeholder above the round document; writing/self-check view: the round switcher is not visible

Fixture `p3` → `phase3`, badge 「轮次阶段(阶段 3)」:

| Step | Reading |
|---|---|
| look above the round document | `#rounds-hint` `display: none`, class `hint hidden`, not visible |
| confirm the document really rendered | `#round-doc` `textContent` length **120**, rect 351 × 778.64 |

Fixture `checking` → `phase5_checking`, badge 「自检进行中(阶段 5)」:

| Step | Reading |
|---|---|
| look for the round switcher | `#round-switcher` `display: none`, `hidden` class present, not visible |

**Observation:** in phase 3 there is no 「已进入轮次阶段(本阶段占位)。」 above the round document; in the self-check view the round switcher is gone. **PASS.**

### Item 3 — walk to `mission_complete`: the process button is invisible and `disabled === true`, the authorize row is invisible, the round switcher is still visible and switchable

Fixture `archive` → `mission_complete`, badge 「使命完成」.

| Step | Reading |
|---|---|
| `#btn-process-round` | `display: none`, `hidden` class present, **`disabled === true`** |
| `#authorize-row` | not visible, `hidden` class present |
| `#round-switcher` | **visible**, two options: `第 1 轮` / `第 2 轮` |

**Observation:** all three faces hold, and the switcher remains usable — which is deliberate (the archive must be browsable). **PASS.**

### Item 4 — REWRITTEN for D-05 (the original expectation 「菜单出现」 no longer applies)

**The original text is retired, and this is registered as required.** `260916-t8g-PLAN.md`'s item 4 read 「用 Shift+方向键在轮次文档中划选 → 菜单出现」. After D-05 the keyboard path gained a **release-Shift** step, so the previously-passing check now tests something else (Pitfall 3 / Pitfall 6's "manual check inherited rather than re-run"). **The original expectation is not applicable and was not executed.**

The rewritten five steps, with every reading:

| # | Step | Observation |
|---|---|---|
| 1 | enter a phase-3 project | `p3`, badge 「轮次阶段(阶段 3)」 |
| 2 | Tab to the round-document area | reaches `#round-doc` on the **2nd** Tab press; ring `2px / rgb(31, 99, 189)`, `outline-offset: 2px`, `:focus-visible` **true** |
| 3 | hold Shift, press → several times to extend the selection | **the selection does NOT extend under automation** — 12 trusted `Shift+ArrowRight` presses leave `window.getSelection()` `{collapsed: true, len: 0}`. The half that *is* observable passes: focus never leaves the document area (`activeElement` stays `#round-doc`, no jump), which is K-2.1's requirement. **See the honesty note below** — this is not a defect call. |
| 4 | release Shift → menu appears, focus on `#btn-annotate` | with a real selection present (produced by a real mouse drag, 11 chars `Round 2 · 检`) and a trusted Shift keyup: menu `hidden=false, display: flex`; `document.activeElement === btn-annotate`; ring `2px / rgb(31, 99, 189)`, `:focus-visible` **true** |
| 5 | press Enter on `#btn-annotate` → native `window.prompt` → type → OK → an annotation appears in the main-pane stream and `#pending-count` increases | real `prompt` dialog observed (`type: prompt`, `写批注(将绑定到划选原文)`), accepted; `#annotation-list` gains **1** item reading `「Round 2 · 检」探针批注:idi-08-03 待处理`; `#pending-count` goes `本轮批注未处理 0` → `本轮批注未处理 1`; `docs/discuss-round-2.annotations.json` written: `{id: a2-01, quote: "Round 2 · 检", before: "", type: "comment", note: "探针批注:idi-08-03", status: "pending", answer: null}` |

**Honesty note on step 3 — this is the one thing automation could not settle, and it is NOT a defect call.** A trusted `Shift+ArrowRight` drive produced no selection. The app is **not** blocking it: computed `user-select` is `auto` on `#round-doc`, on `.markdown-body` and on `body`; and a programmatic `Range` selection over `#round-doc` yields **301 characters**, so the selection machinery and the document content are both fine. The residual explanation is environmental — Chrome's **caret browsing is off by default**, and in a non-editable, non-`contenteditable` element a caret is what `Shift+Arrow` needs to anchor a selection. **That is a hypothesis, and it is stated as one.** ROADMAP Phase 8 §Manual checks is explicit that an automated FAIL here must not be turned into a functional-defect call, and this SUMMARY does not make one. It is also worth noting that if the hypothesis is right, a real keyboard user with default Chrome settings would meet the same behaviour — which is precisely why a human must settle it, and why A11Y-08's keyboard half stays a named manual check rather than something an automated pass could claim.

**PASS on steps 1, 2, 4, 5 (machine-observed); step 3's extension half handed to the human.**

### Item 5 — stop the backend → the banner appears; restore → it disappears; a fatal disconnect → a red banner

Driven against a **second** uvicorn instance on port 8799 so the resident dev server on 8765 was never disturbed (the harness reuses it and never closes it).

| Step | Reading |
|---|---|
| page loaded, backend up | `#stream-banner` `display: none`, not visible |
| **stop the backend** (SIGTERM the instance; port confirmed closed) | banner visible, `display: block`, text exactly `事件流已断开,正在自动重连……`, class list has **no** `fatal` (amber) |
| **restore the backend** (restart the instance; port confirmed open) | banner `display: none`, class `hidden` — it cleared itself via `source.onopen` |
| **fatal** | a deterministic non-200 on `/api/events` → banner visible, text exactly `事件流已断开且无法自动恢复,请刷新页面。`, class list contains **`fatal`** (red) |

**Observation:** the three states are distinguishable and the transient/fatal split works. **One registered nuance:** "stopping the backend" cannot reach the fatal state by itself — an EventSource treats a refused connection as retryable and stays in `CONNECTING`, so the amber branch is what a stopped backend produces. The `CLOSED` (red) branch was therefore reached with a deterministic non-200 response rather than by killing the process. That is a statement about EventSource semantics, not a defect.

**PASS.**

### Item 6 — a nonexistent path: the error appears directly below the input, and a second click clears the old error first

| Step | Reading |
|---|---|
| enter a nonexistent path, click 进入 | exactly **1** `.inline-error`; `previousElementSibling === #enter-form` (directly below the input+button, not in the AI work panel); error top **110** ≥ form bottom **102**; error left **1049** = form left **1049** (same column, full width of the form) |
| mark that node with `data-probe-mark="1"`, click 进入 again | still exactly **1** `.inline-error` (not 2 — replaced, not accumulated), and **the mark did not survive** ⇒ the old node was removed and a fresh one created, i.e. `clearInlineError()` ran before the new request |

**Observation:** the error is inline and positioned below the input; on re-click the stale error is cleared first rather than stacking. **PASS.**

### The mouse path (D-09) — re-run as the plan requires

| Step | Reading |
|---|---|
| plain mouse click on `#round-doc` | focused (`activeElement === #round-doc`) but `:focus-visible` **false**, computed outline `3px / rgb(32, 32, 32)` with offset `0px` — the UA default, **no ring** ⇒ **SC2's semantics still hold** |
| Shift + mouse drag to extend | selection non-collapsed, `Round 2 · 检` |
| release the mouse button | menu visible (`hidden: false`, `display: flex`) |
| **release Shift** | `activeElement` `round-doc` → **`btn-annotate`** ⇒ **the mouse path's Shift release does send focus into the menu**, exactly as D-09 registered |

**Observation: judged acceptable, as D-09 anticipated** — the focus goes precisely where the user is about to click. Recorded as measured, not as expected.

## The archive round-switch specific re-verification (D-23)

ROADMAP Phase 8's Gates list this item by name. Fixture `archive` (`mission_complete`, badge 「使命完成」).

| Step | Reading |
|---|---|
| enter the read-only archive state | `roundTitle` = `总设计文档(只读归档)`; `#btn-process-round` `hidden` class **and** `disabled === true`; not visible |
| switch rounds via `#round-switcher` (`select_option('2')`) | `roundTitle` = `第 2 轮(归档·只读)` — **the switch really happened** (`roundTitle` changed), `#round-doc` re-rendered |
| re-check 「处理本轮批注」 after the switch | `disabled === true` **still**, `hidden` class **still** present, not visible |

**Observation: 「处理本轮批注」 remains not clickable after switching rounds.** `applyArchiveView`'s two lines (`app.js:870-871`, hard rule 5) were observed only — `git status --porcelain -- frontend/` is empty at this task's boundary.

**Mechanism correction (registered as Deviation 1):** the reset path the plan attributes to this switch does not run. `updateFrozenPresentation` is called from exactly one place (`app.js:1082`, inside `loadRoundView`); the archive switcher calls `loadArchiveRoundDoc` (`app.js:1295` → `app.js:915-924`), which touches neither the class nor the flag. The button therefore stays **both** hidden and disabled — a stronger outcome than the plan predicted, and the Pitfall 3 UI-6.3 scenario it warns about cannot arise on this route.

## The t8g D4 known limitation — removed by this phase

`260916-t8g-SUMMARY.md`'s coverage entry D4 carried this rationale verbatim:

> 已知限制:`#round-doc` 是不可聚焦的普通 div,keyup 仅在焦点已落在容器内时生效(让容器可聚焦需 tabindex/role,属审计显式排除范围)。

**This limitation no longer exists, and the removal is by plan 01's work, not by plan 03:**

- **plan 01** put `tabindex="0"` on `#round-doc` (so the container is focusable at all — the 「不可聚焦」 half is gone), and
- **plan 01** added the Shift-only `keyup` listener inside `initSelectionMenu()` (so releasing Shift hands focus into the menu — the 「keyup 仅在焦点已落在容器内时生效」 half is no longer a dead end, because the document area is now itself reachable by Tab).

The measured consequence is in this SUMMARY: `#round-doc` is Tab stop **#2** in phase 3 with a live ring, and a Shift release from it lands focus on `#btn-annotate`. The limitation's own stated remedy — 「让容器可聚焦需 tabindex/role」 — was the user-adjudicated narrow slice (D-01/D-18: `tabindex` yes, `role`/`aria-label` no).

## A11Y-08 — the full Tab-order census (two states)

Census by element with the `visible ∧ focusable` filter (never by selector count). "Judged set" = the visible, non-disabled, `tabIndex >= 0` elements — i.e. the Tab-reachable ones.

### State 1 — phase 3 (`p3`)

**Judged set: 10 elements, and all 10 are reached by Tab** (`judged_not_reached: []`):

`#ai-route-select`, `#project-path-input`, `#btn-ping`, `#btn-process-round`, `#btn-abort`, `#enter-path-input`, `#btn-enter`, `#round-switcher`, `#round-doc`, `#btn-authorize`.

**`#round-doc`'s position — recorded per §K-1.7, not as 「Tab 能到」:**

| Reading | Value |
|---|---|
| position in the Tab order | **2** |
| immediately **before** it | `#round-switcher` ✓ |
| immediately **after** it | `#btn-authorize` — the `#authorize-row` button, which **is visible** in this state ✓ |
| its ring at the moment it holds focus | `outline-width: 2px`, `outline-color: rgb(31, 99, 189)`, `outline-offset: 2px`, `:focus-visible` **true** |
| geometry | 351 × 778.64 px (taller than the doc panel's visible band, so the ring traces a full box in the fixture; **the ring's vertical form is not a criterion** per A-10) |

That is exactly §K-1.7's contract: **after `#round-switcher`, before `#authorize-row`'s button (when visible)**. Cross-checked independently: `check-05 --item 10` reports `[p3] 判定集 10 个元素,未覆盖 []` — the same judged set of 10, with zero uncovered.

The remaining controls reached (all in the harness's raw census, excluded from the judged set for the right reasons): `#message-input` / `#btn-send` (phase 1-2 session panel, hidden here), `#btn-continue-check` / `#btn-continue-repair` (`display: none`), `#btn-approve-draft` / `#btn-confirm-authorize` (marked `disabled` ⇒ correctly excluded from `focusable`), and the modal/menu controls inside hidden `.overlay`s and `#selection-menu` (zero rect, not reachable by Tab while hidden — correct).

### State 2 — phase 5 self-check view (`checking`)

**Judged set: 8 elements, and all 8 are reached by Tab** (`judged_not_reached: []`):

`#check-switcher`, `#btn-continue-check`, `#ai-route-select`, `#project-path-input`, `#btn-ping`, `#btn-abort`, `#enter-path-input`, `#btn-enter`.

`#round-switcher` is correctly **not** in the judged set here (`display: none`) — which is item 2's second half, confirmed independently above.

**Registered finding in this state:** `#round-doc` is reached by Tab but has **zero height** (351 × 0, empty), because `applyPhase5View` empties it at `app.js:629`. Its ring still reads `2px / rgb(31, 99, 189)` with `:focus-visible` true — on a zero-height box. It is excluded from the judged set by the `visible` filter (correct), and the stop is new in this phase (plan 01's `tabindex`). See §Deviation 2.

### The keyboard selection path (the part automation cannot claim)

Recorded here as a **named manual check**, per the plan and ROADMAP Phase 8 §Manual checks:

1. enter a phase-3 project;
2. Tab until focus reaches the round-document area — the ring draws (`2px / rgb(31, 99, 189)`, `:focus-visible` true, 2nd Tab press);
3. **hold Shift and press → repeatedly to extend the selection** — the one step automation could not perform (see the honesty note under item 4);
4. release Shift → the menu appears and focus lands on `#btn-annotate` (machine-proven via a mouse-origin selection);
5. Escape → **focus does return to `#round-doc`, but the menu does not stay dismissed** — see §Newly discovered finding;
6. press Enter on `#btn-annotate` → a real annotation is created (machine-proven).

**No claim is made that keyboard accessibility is covered because an automated test passed.** Steps 2, 4, 5 and 6 are machine-observed; step 3 is not, and step 5 is the defect above.

## Close-out registrations (the plan's three, plus the Deferred Item)

### (a) Fingerprint obligation (D-25) — measured, and the answer is zero debt

Verified file by file against the five live reports:

| Report | `covered_files` contains `frontend/style.css` | contains `scripts/check-05-ui-uat.py` | contains `frontend/app.js` or `frontend/index.html` |
|---|---|---|---|
| `idi-04` | yes | — | **no** |
| `idi-04.1-radix` | yes | yes | **no** |
| `idi-05` | yes | yes | **no** |
| `idi-06` | yes | yes | **no** |
| `idi-07` | yes | yes | **no** |

**Conclusion: under the D-01 path this phase incurs zero fingerprint debt.** `frontend/app.js` and `frontend/index.html` appear in **no** live report's `covered_files`, and `frontend/style.css` is byte-unchanged (`git status --porcelain -- frontend/style.css` is empty). **D-02 was not triggered** — plan 01's measurement and the user's 2026-09-24 adjudication settled the ring as discernible (5.57:1), so the escalation branch was never taken and no report needs recomputing.

**Two things that must not be done, registered verbatim because both are traps:**

- **Do not judge staleness with `gsd-tools query verification status <phase>`** — for these phase directories it returns `missing` for every one of them (the phase-directory naming does not match the tool's phase-token resolution). The only valid method is comparing each report's `covered_files` and recomputing its digest from **HEAD content**.
- **If a `style.css` change ever does happen, recompute from HEAD content and do not look at mtime** — stale has two causes (a genuine content change ⇒ re-verify; a bookkeeping edit ⇒ recompute + disclose) and their remedies point in opposite directions.

### (b) Pre-existing todo (D-26) — registered as pre-existing, NOT introduced by this phase

**`/gsd-verify-work idi-04.1-radix` was still outstanding before this phase began** (STATE.md §Operator Next Steps item 2). Its `covered_digest` went stale when **Phase 5** rewrote `frontend/style.css` and `scripts/check-05-ui-uat.py` — the cause is a **genuine content change**, so the remedy is re-verification, not digest backfill. The inputs are prepared in `idi-05-03-SUMMARY.md`'s D-05 section.

**This phase adds nothing to that layer:** it does not touch `style.css` or `check-05-ui-uat.py`, so it neither deepens nor clears the staleness. Registered so it is not mistaken for something Phase 8 introduced.

### (c) Known gaps and limitations (two, both deliberately not fixed)

1. **D-17 — `#permission-modal`'s 「弹了键盘用户不知道」.** Opening it moves focus nowhere and it carries no declaration, so a keyboard user gets no signal that it appeared. Deferred to **v2 `A11Y-V2-02`**. Reason it is not fixed here: the user adjudicated the object set to `#confirmation-modal` + `#tier-modal` (D-11), and this modal can be Tabbed out of, so it is not a trap. Machine-checked as **not** touched: `frontend/index.html`'s `#permission-modal` still carries no ARIA triple, and `app.js` has no focus call and no Escape branch for it.
2. **D-19 — the keyboard selection path's discoverability.** The new path's only visual signal is the focus ring: **nothing tells a keyboard user that Shift+Arrow selects text.** No hint was added. **Registered consequence, stated plainly: this gap turns no gate red**, because A11Y-08's manual acceptance is performed by someone who already knows the steps — which is exactly why it is registered explicitly instead of being treated as covered. Adding a hint was rejected (changing `#rounds-hint` is a visible behaviour change, and a new `.hint` would be a new UI element, outside this phase's deliverable list).

### (d) STATE.md's `[v1.14 P8]` Deferred Item — relation registered, and it does NOT close

The item's verbatim text: 「五条 b9664e0 修复无自动化覆盖,而本里程碑重写其依赖的 CSS;`.hidden { display: none !important }` 是 5 路单点故障」.

This phase discharges **one pass** of both halves — Task 2's six manual re-runs cover the first half, and Task 1's `check-03` (`.hidden` uniqueness) covers the second. **But neither is a resident guard** (the six items are a human checklist, and the two REG-02 gates are plan-level greps per D-21/A-4). **The Deferred Item therefore does not close on account of this phase — it was honoured once.** Registered so a later reader does not read the re-run as closure.

### (e) The existing assertions this phase touches (Task 1's fifth registration)

1. **`check-05 --item 10`'s judged set gains one member in two samples.** Measured: `p1` 9 → 9 (unchanged — `#round-doc` reads `visible=False` there and is filtered out), `checking` 8 → 9, `p3` 9 → 10. The raw census moves 28 → 29 in each sample because before plan 01 `#round-doc` matched **none** of `FOCUSABLE_SELECTOR`'s alternatives (it had no `tabindex`), so it was absent from the raw data entirely rather than merely filtered. **`archive` cannot be measured by this gate** — item 10's sample set is hardcoded to `p1` / `checking` / `p3` and the CLI has no `--state` flag (plan 01's deviation 1); the archive half is a known uncovered item. **This is a census change, not a defect fix** — item 10 was PASS before and after (41 assertions, 0 FAIL, 0 BLOCKED, re-confirmed in this plan).
2. **`_idi07_tab_drive`'s limit is data-driven and absorbs the new stop.** The limit is `len(data) + 8`; the census +1 raises it 36 → 37, while the Tab order also gains exactly one stop (+1) — the two cancel, so **no gate change is needed**. Confirmed empirically here: the p3 drive with `len(census) + 8` reached every judged element.
3. **`scripts/probe-07-focus-composite.py`'s re-run obligation (D-04) was discharged by plan 01**, with both self-witness counts recorded verbatim in `idi-08-01-SUMMARY.md` (`links-before=0` / `links-after=1 (mutation-applied=yes)`, composite ratio 3.45 ≥ 3.0). Plan 03 does not re-run it (it is not a gate and its obligation is already met), and the file is byte-identical to HEAD.
4. **The other four invariant guards are unaffected on the D-01 path** — re-run on the close-out tree: `check-01` PASS, `check-02` `PASS: 0 failures` (47 pairs, `ORDER 0.363`), `check-03` PASS, `check-04` PASS.

### (f) The three signed-off deviations — pointer registration only

Registered as pointers for VERIFICATION / UAT to consume; the bodies live in `idi-08-UI-SPEC.md` §契约修正登记 and `08-CONTEXT.md` and are deliberately **not** copied here:

- **A-1** — the object set was re-ordered by measurement to `#confirmation-modal` + `#tier-modal`.
- **A-2** — the keyboard submit gesture is Shift **release**.
- **A-3** — PITFALLS 5 failure mode 4 was overturned geometrically ⇒ whole-box ring + zero `style.css` change.

### (g) The plan's own gate-arithmetic traps, recorded so they cannot be re-derived wrongly

- **REG-02 gate ② is `>= 9`, not `6`.** Measured on HEAD before the change: 9 (`grep -c 'clearInlineError();'`), and 10 for the unanchored `clearInlineError` (9 calls + 1 definition). `08-CONTEXT` D-21's `6` is a `b9664e0`-era figure; adopting it would have produced a gate that can never fail.
- **pytest is 「219 passed + 6 (deselected, i.e. skipped) / 225 collected」.** 219 is the **pass** count, 225 the **collect** count. Copying 225 as the pass count would build a gate that always fails.
- **Hard rule 2's arithmetic:** `grep -c '!important' frontend/style.css` returns **5** (4 lines of comment prose + 1 declaration); the gate counts **1 declaration** and is decided by `check-04`, never by counting hit lines.
- **Hard rule 1:** `grep -c '^\.hidden {' frontend/style.css` == **1**.

## Issues Encountered

- **A resident dev server was already listening on `127.0.0.1:8765`** (a detached `uvicorn backend.main:app`, PID 57542, running since a previous session). The harness reuses it and never closes it, so all readings except item 5's were taken against that reused process. **Item 5 deliberately did not touch it**: a second instance was started on **8799**, driven, killed and restarted, and torn down at the end — `lsof -ti:8799` is clean and the resident 8765 process is still alive and untouched.
- **`WINDOWS.md` refused the ledger write.** `gsd-tools windows append` returns *"Ledger table … disagrees with the fenced JSON entries (the sole source of truth) for row id(s): 17"* — the same pre-existing inconsistency the dispatch warned about. Per the dispatch instruction, the entries are recorded in this SUMMARY and in STATE.md instead, and the refusal is noted rather than fought. **The entries that would have gone there:** the Escape re-show defect (kind `deviation`), the phase-5 zero-height Tab stop (kind `deviation`), and the fact that REG-03's six items and the two REG-02 gates are not resident guards (kind `deviation`).
- **The local `grep` is ugrep and mis-parses embedded `!==`.** `grep -c "key !== 'Escape'" frontend/app.js` prints `warning: !==: No such file or directory` and returns 0 when composed inside a nested-quoted compound line. Run standalone it returns exactly **1** (verified). Same class as the `-o | wc -l` arithmetic trap this project has recorded before — a shell-quoting trap in composing a gate, not a gate result.
- **The first mouse-selection probe attempt produced no selection.** One probe's Shift+drag left `getSelection()` empty while an identically-composed probe succeeded. Rather than accept the empty reading, the working sequence was reproduced deliberately and the difference isolated to the drag's starting point/first-click focus. This is the project's "suspect your own probe first" discipline applied — the second attempt is the one reported above, and the same discipline is what produced the decisive keydown/keyup split for the Escape finding.
- **Task 2 and Task 3 produced no commit.** Both are specified as zero-file-change tasks. Plan 01 set the precedent for this (`idi-08-01`'s Task 2 has no commit), so the atomic close-out invariant is satisfied: the plan's one production commit exists and this SUMMARY is the deferred close-out.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- **Ready for the phase-8 close-out.** All plan-level gates are green on the close-out tree: `在右侧文档划词即可批注` 1, `inline-error` 1, `clearInlineError();` 9, pytest `219 passed / 6 deselected / 225 collected`, `check-01`/`check-02`/`check-03`/`check-04` PASS, `check-05 --item 1` PASS (45 assertions), `--item 4` PASS (65 assertions), `--item 10` PASS (41 assertions), `tabindex` 1, `:focus-visible` 9, `frontend/vendor/` exactly one file, `git status --porcelain -- frontend/style.css scripts/check-05-ui-uat.py` empty.
- **Wave 1 and wave 2 are not regressed** — every invariant from `idi-08-01` and `idi-08-02` was re-measured by content, not by line number.
- **The phase's deliverables are all on disk:** `frontend/index.html` carries the `tabindex` plus the two new ids and the two ARIA triples; `frontend/app.js` carries the Shift listener, the F1-a/b/c hand-back, `appEl`, `syncBackgroundInert()` with its five call sites, the tier focus-on-open and flag reset, the Escape dispatcher, both F1-d hand-backs, and now the S8-1 copy fix.
- **⚠ One item requires the user's adjudication before the phase can be called clean:** the **Escape re-show defect** (§Newly discovered finding). It is a live defect in a deliverable of this phase, it is fully measured with three controls, and the fix is a design choice the user owns. It blocks no gate; it should not be downgraded to a known limitation.
- **Two further items are handed to the end-of-phase harvest:** the phase-5 zero-height `#round-doc` Tab stop, and the keyboard-selection extension step (the caret-browsing hypothesis).
- **The manual checks this SUMMARY cannot complete** (end-of-phase UAT must harvest them): the on-screen reading of the S8-1 empty-state line, the ring's visual discernibility (plan 01's D-02 half — machine half proven at 5.57:1, user-adjudicated 2026-09-24), item 4's step-3 keyboard selection extension, A11Y-08's on-screen Tab walk in both states, and §K-2.5's two measured items (① whether the selection highlight is still visible once focus is in the menu — if not, the keyboard user annotates blind and it must be reported immediately, not registered silently; ② whether the selection can continue after Escape).
- **Pre-existing open item, not introduced here (D-26):** `/gsd-verify-work idi-04.1-radix` remains outstanding; this plan adds nothing to that layer.

---

*Phase: idi-08-accessibility-semantics-and-keyboard*
*Completed: 2026-09-24*

## Self-Check: PASSED

- `frontend/app.js` — FOUND (the only modified file); `frontend/index.html` — FOUND; `frontend/style.css` — FOUND (byte-unchanged); `scripts/check-05-ui-uat.py` — FOUND (byte-unchanged); this SUMMARY — FOUND
- Commit `fa7813a` (Task 1) — FOUND
- `requirements-completed: [A11Y-08, REG-03]` matches the plan's `requirements:` verbatim
- `actuals` measured, not narrated: `commits: 1` from `git rev-list --count 20b99d1..HEAD`; `plan_head_before` = `20b99d1af81479a63f154c40a3d68b606d85910b`; `tokens: 151` = 606 chars / 4 over the realized diff
- Plan-level `<verification>` re-run on the close-out tree: `在右侧文档划词即可批注` 1 · `inline-error` 1 · `clearInlineError();` 9 · pytest 219 passed / 6 deselected / 225 collected · `check-01`/`check-03`/`check-04` PASS · `check-02` `PASS: 0 failures` · `check-05 --item 1` PASS (45) · `--item 4` PASS (65) · `--item 10` PASS (41) · `tabindex` 1 · `:focus-visible` 9 · `git status --porcelain -- frontend/style.css scripts/check-05-ui-uat.py` empty · `frontend/vendor/` exactly one file
- Wave 1/2 invariants re-measured: `role=` 2 · `aria-modal` 2 · `aria-labelledby` 2 · `id="` 82 · `syncBackgroundInert` 6 · `tierModalShown` reset present · `authorizeBtn.focus()` 1 · `continueCheckBtn.focus()` 1 · `hideSelectionMenu`'s predicate (L1347) precedes its hide (L1348)
- Task 2 and Task 3 correctly have no commit — the plan specifies zero file changes for both; `git status --porcelain -- frontend/ scripts/` is empty at Task 3's boundary


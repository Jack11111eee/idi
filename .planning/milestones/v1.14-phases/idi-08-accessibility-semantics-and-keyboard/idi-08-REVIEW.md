---
phase: idi-08-accessibility-semantics-and-keyboard
reviewed: 2026-09-24T06:44:50Z
depth: standard
files_reviewed: 3
files_reviewed_list:
  - .claude/settings.local.json
  - frontend/app.js
  - frontend/index.html
findings:
  critical: 1
  warning: 2
  info: 5
  total: 8
status: issues
---

# Phase 8: Code Review Report

**Reviewed:** 2026-09-24T06:44:50Z
**Depth:** standard
**Files Reviewed:** 3
**Status:** issues (equivalently `issues_found`)

## Summary

Scope: the three files listed in config, diffed against `f0f0c31` (21 commits, `frontend/app.js` +142 / `frontend/index.html` +52 / `.claude/settings.local.json` +9).

What holds up:

- The **Escape-fix mechanism itself is correct**. The suppression listener is registered on `document` in the **capture** phase (app.js:1532-1534), which is the only phase that can pre-empt `#round-doc`'s own `keyup` handler (app.js:1402) — `stopPropagation()` at document-capture halts the path before the target phase, so `handleSelectionTrigger` genuinely does not run. A bubble-phase listener would have been too late; capture was necessary and is correct.
- **No collateral suppression.** The only other `keyup` consumers in the frontend are `handleSelectionTrigger` (the one being suppressed, intentionally) and the new Shift submit gesture (key-filtered to `Shift`, app.js:1422). Nothing legitimately needs an Escape `keyup`, and `stopPropagation()` does not cancel default actions, so no browser default is lost.
- **`once` does not leak unboundedly.** The listener removes itself on the first `keyup` of *any* key, so a lost keyup (window blur mid-press) leaves at most one stale listener, which is then consumed by the next keystroke. If that stale listener happens to swallow a later Escape `keyup`, the only consequence is that `handleSelectionTrigger` is not called — harmless today. No defect here.
- **The modal branches do not interact badly with `once`.** The suppressor is registered only inside branch 1, and branches 2/3 register nothing, so repeated Escape presses over a modal never accumulate listeners.
- **`syncBackgroundInert()` is genuinely derived, not bookkept.** All four places that mutate `#confirmation-modal` / `#tier-modal` visibility (app.js:494-495, 500-501, 673-674, 839-840, 1554-1556) call it, and `grep` finds no other hide path — the derived form cannot desync. `inert` is applied only to `#app` (a sibling of all five `.overlay`s and `#selection-menu`), so T-idi08-05 is respected; and the open-ordering (inert first, then `focus()`) is correct in all three open sites.
- `showInlineError` still writes via `textContent` only (app.js:317-324); no `innerHTML` was introduced anywhere in the diff. `.hidden { display: none !important }` remains the single `!important` declaration (style.css:574). `#selection-menu` is still a direct child of `<body>` (index.html:249). No existing `getElementById` id was renamed or removed — only `appEl` was added (app.js:90), which is the safe direction under G-idi01-8.
- The one-word copy fix (app.js:1162, 「在**右**侧文档划词」) is factually correct: `#main-pane` precedes `#doc-panel` in both the DOM (index.html:12 / 82) and the flex row (style.css:576-604), so the doc panel is on the right.

What does not hold up: **the Escape fix is incomplete.** It covers exactly one `keyup` — the one that immediately follows the Escape press — while the state it creates ("menu hidden, selection still live, focus handed back to `#round-doc`") persists. Any later `keyup` targeting `#round-doc` re-opens the menu, so Escape is not a durable dismissal. Details in CR-01.

One scope note the orchestrator should resolve: the binding-constraint list in my task says `renderAnnotations` must not be modified, but plan 03's authorized copy fix is *inside* `renderAnnotations` (app.js:1162). I treated the constraint as protecting its DOM construction (which is untouched) and recorded the conflict as IN-01 rather than as a violation — flagging it so the constraint text and the plan description can be reconciled.

## Narrative Findings (AI reviewer)

### Critical Issues

#### CR-01: Escape dismissal is not durable — the menu re-opens on the next `keyup` (including a second Escape)

**File:** `frontend/app.js:1518-1536` (suppression), interacting with `frontend/app.js:1350` (F1-a hand-back) and `frontend/app.js:1402` + `1375-1392` (`handleSelectionTrigger`)

**Issue:** The suppressor added in `62dfd3e` is `{ capture: true, once: true }`. `once` removes the listener after its **first invocation of any kind**, and the listener is registered without a key filter, so it is consumed by whichever `keyup` arrives first. The state the Escape branch creates, however, outlives that single keyup: `hideSelectionMenu()` deliberately does **not** clear the selection (D-08, app.js:1346), and the F1-a hand-back puts focus on `#round-doc` (app.js:1350). Focus on `#round-doc` + a live, non-collapsed selection is precisely the condition under which the *unfiltered* `handleSelectionTrigger` (bound to `#round-doc`'s `keyup`, app.js:1402) re-opens the menu. Its guards all pass (app.js:1377-1389: not a frozen round, `currentState === 'phase3'`, selection non-collapsed and non-blank, anchored inside `#round-doc`).

Three concrete failure scenarios, in increasing subtlety:

1. **Escape twice (simplest repro).** Select text in the round doc → the menu appears → press Escape → menu closes, focus returns to `#round-doc`, and the suppressor is consumed by that press's own `keyup`. Press Escape again: the dispatcher finds the menu hidden, the confirmation modal hidden and the tier modal hidden, so the `keydown` does nothing at all — but its `keyup` reaches `#round-doc` and re-opens the menu. Net effect: repeated Escape *toggles* the menu (odd presses hide, even presses show), instead of being idempotent. This is exactly the defect class `62dfd3e` set out to fix, one keypress later.
2. **Any other key after Escape.** Same setup; after Escape, press `ArrowRight` (or `Tab`, or any key) while `#round-doc` holds focus. The `keyup` targets `#round-doc` → `handleSelectionTrigger` → menu re-opens. So a user who dismisses the menu and then keeps reading with the keyboard gets the menu popping back up unprompted. Note the same state is reachable without Escape at all: mouse-select text (the click now focuses `#round-doc` because of the new `tabindex="0"`, index.html:163), then wheel-scroll — the existing capture-phase scroll listener hides the menu (app.js:1435) while the selection survives — then press any key.
3. **Release order decides.** Press Escape while Shift is held (the user is mid-extension), then release Shift *before* Escape. The Shift `keyup` arrives first, the unfiltered `once` listener fires with `key === 'Shift'`, does not call `stopPropagation`, and is removed. The Escape `keyup` then reaches `#round-doc` with no suppressor left and re-opens the menu. (The Shift `keyup` itself re-opens it first: focus is on `#round-doc` by then, so its target is `#round-doc`, and the menu is hidden — so even before the Escape keyup, the menu is back.)

The code comment at app.js:1531 ("`once:true` 让监听器在首个 keyup 后自动摘除,无需记账、不会泄漏") reasons only about *leakage*; the actual risk is the opposite — the listener is *spent too early*, leaving the state it guards unguarded. The related premise the phase relies on, recorded at app.js:1373-1374 ("不对 keyup 做按键白名单 —— 折叠/空白选区即关闭菜单已让非选择类按键成为安全 no-op"), was true only while a hidden menu could never coexist with a live selection; the Escape feature creates exactly that state, so the premise is no longer sound and non-selection keys are no longer no-ops.

**Fix (minimal, covers scenarios 1 and 3):** register the suppressor for **every** Escape `keydown` (before the priority branches, so the second press also arms it), filter by key inside, and remove it explicitly on the matching Escape `keyup` instead of relying on `once`:

```js
document.addEventListener('keydown', (e) => {
  if (e.key !== 'Escape') return;
  // 每次 Escape 都登记抑制器:① 不能被其它按键的 keyup 提前消费(如先松 Shift);
  // ② 菜单已隐藏的第二次 Escape 也必须再登记一次,否则它的 keyup 会把菜单重开。
  const suppress = (ev) => {
    if (ev.key !== 'Escape') return;            // 其它按键照常放行
    ev.stopPropagation();
    document.removeEventListener('keyup', suppress, true);
  };
  document.addEventListener('keyup', suppress, true);
  if (!selectionMenu.classList.contains('hidden')) { /* …既有分支 1… */ }
  // …既有分支 2/3…
});
```

**Fix (durable, also covers scenario 2):** scenario 2 cannot be closed from the dispatcher alone, because it is `handleSelectionTrigger`'s key-agnostic binding that re-opens the menu. The durable options are (a) add a key filter / dismissal flag to `handleSelectionTrigger` so a live selection with a hidden menu is not re-opened by unrelated keyups, or (b) keep a capture-phase suppressor armed until the selection changes (`selectionchange`) or focus leaves `#round-doc`. Note a constraint conflict for the orchestrator: the phase's own comment at app.js:1530 asserts `handleSelectionTrigger` is on the do-not-touch list (硬规则 5), while the constraint list supplied for this review does not include it. Which applies needs to be resolved before picking (a).

### Warnings

#### WR-01: The Shift submit gesture steals focus on unrelated Shift releases (e.g. Shift+Tab)

**File:** `frontend/app.js:1421-1427`

**Issue:** The gesture fires on *any* `Shift` `keyup` that finds the menu visible and the selection non-collapsed — it does not require the release to belong to an extension gesture, nor that `#round-doc` still holds focus. Concrete repro: select text in the doc (menu visible, focus on `#round-doc`), then press Shift+Tab to move focus backwards. Focus moves to `#round-switcher` (a real tab stop, index.html:136); the `Tab` `keyup` does nothing; then the `Shift` `keyup` runs the gesture and calls `annotateBtn.focus()`, yanking focus out of the control the user just navigated to and into the menu. Because `#selection-menu` is the last focusable region before the end of the document, a keyboard user yanked here has to traverse the whole tab order again to get back. Releasing Shift alone (a habitual key) does the same thing whenever the menu happens to be open.

**Fix:** require the release to be in the extension context before moving focus — the legit keyboard flow always has `#round-doc` itself focused at that moment:

```js
document.addEventListener('keyup', (e) => {
  if (e.key !== 'Shift') return;
  if (selectionMenu.classList.contains('hidden')) return;
  if (document.activeElement !== roundDoc) return; // Shift+Tab / 焦点已离开文档区 → 不夺焦
  const selection = window.getSelection();
  if (!selection || selection.isCollapsed) return;
  annotateBtn.focus();
});
```

#### WR-02: `Bash(node -e ' *)` in the local allowlist pre-approves arbitrary code execution

**File:** `.claude/settings.local.json:23`

**Issue:** This entry was added by this phase and auto-approves any `node -e '…'` command, i.e. arbitrary JavaScript executed with the user's full privileges and no permission prompt. The prompt is the only control standing between content the agent reads (file contents, web/CLI output, and — in this project — AI-generated discussion documents) and code execution, so this grant collapses that control for the most direct execution vector available. The pattern is also written with a space after the opening quote (`node -e ' *`), which is narrower than it looks: it does not match the common `node -e 'console.log(1)'` form (no space after `'`) while it does match `node -e ' <anything>'`, so the grant buys less convenience than intended while still admitting arbitrary payloads.

**Fix:** narrow to the concrete probe scripts this phase actually needed, e.g. `Bash(node -e 'require(...)/.claude/gsd-core/bin/lib/ui-consideration-probe.cjs' *)`, or drop the entry and approve the one-off commands interactively. Adjacent, pre-existing and lower priority: `Bash(git *)` (line 13) is the same class of exposure — `git -c core.pager='…' log` executes a shell command without a prompt.

### Info

#### IN-01: The copy fix is inside `renderAnnotations`, which the constraint list marks do-not-touch

**File:** `frontend/app.js:1162`

**Issue:** `renderAnnotations` is on the do-not-touch list given to this review, yet plan 03's authorized S8-1 fix changes a string literal inside it. The change itself is safe and correct (literal only; the XSS-safe DOM construction at 1157-1211 is untouched; the 「右侧」 direction matches the layout). Recorded because the constraint text and the phase description contradict each other; a later reader applying the constraint literally would flag this as a violation.

**Fix:** no code change needed — reconcile the constraint wording to "renderAnnotations' rendering logic/DOM construction" so the copy fix is unambiguously in scope.

#### IN-02: Escape branch 3 falls through instead of returning

**File:** `frontend/app.js:1553-1559`

**Issue:** Branches 1 and 2 `return`; branch 3 does not. Harmless today (nothing follows it but the comment block for the deliberate non-responders), but the asymmetry is a latent trap: any future branch appended below would run in the same keypress as the tier-modal close, and the comment block that follows reads as if branch 3 had ended the handler.

**Fix:** add `return;` after `e.preventDefault();` at app.js:1558 for symmetry with branches 1 and 2.

#### IN-03: `roundDoc.focus()` without `preventScroll` can shift the doc panel's scroll position

**File:** `frontend/app.js:1350`

**Issue:** `focus()` scrolls the target into view. `#round-doc` is a tall element inside the scrolling `#doc-panel`, so when the user has scrolled down and the hand-back runs (focus in the menu → Escape or click-outside), the browser may align the panel back to the element's top edge — a jump that discards the user's reading position. This is browser-dependent (Chrome does not scroll for a partially-visible oversized element in all cases) and was not covered by the phase's measurements, which only pinned the *focus-ring clipping* at scrollTop 67/71.

**Fix:** `roundDoc.focus({ preventScroll: true });` — the element is already in view when the menu was open, so nothing is lost.

#### IN-04: Stale derived counter in the `hideSelectionMenu` comment

**File:** `frontend/app.js:1342-1343`

**Issue:** The comment says the hand-back lives in one function "而不是它的四个调用点(两个关闭器 + handleSelectionTrigger 的两条守卫 + 两个菜单项)" — the enumeration itself lists six, and at HEAD there are seven call sites (app.js:1383, 1387, 1433, 1435, 1440, 1470, 1519 — the seventh being the Escape branch, added after this comment was written). This is the prose-counter failure mode the project has recorded repeatedly.

**Fix:** drop the count and keep the enumeration, or update it to the current seven call sites.

#### IN-05: The dispatcher closes modals on an IME-cancel Escape

**File:** `frontend/app.js:1514-1516`

**Issue:** `#confirm-word-input` takes Chinese input, so an IME composition is the normal way to type 「确认授权」. On platforms/browsers where the Escape that cancels an open IME candidate window is delivered to the page as a normal `Escape` `keydown` (with `isComposing: true`), the dispatcher's branch 2 will close the authorization modal on a keypress the user intended only as "cancel the candidate list". Platform-dependent — reported as Info, and cheap to harden.

**Fix:** ignore composition-time keydowns at the top of the handler: `if (e.isComposing) return;`.

---

_Reviewed: 2026-09-24T06:44:50Z_
_Reviewer: [CL] (gsd-code-reviewer)_
_Depth: standard_

---

## Resolution record (orchestrator, 2026-09-24 — appended, findings above left verbatim)

**CR-01 confirmed by independent reproduction, then fixed in `09b170d`.** Reproducing it against `62dfd3e` before touching anything: S2 (Escape twice), S3 (Escape then an unrelated key), S5 (release order), and S6 (wheel-scroll dismiss then a key — reachable with no Escape at all) all re-opened the menu; only S1 passed. The reviewer's mechanism was exactly right, and its "minimal" option was **not available**: `handleSelectionTrigger`'s function body is do-not-touch under D-06, and D-06 specifically forbids a key whitelist entering it. The shipped fix therefore registers the *dismissed selection* in `hideSelectionMenu()` and refuses to re-open for that same selection, self-clearing when the selection genuinely changes — selection identity, not key identity.

A **second defect the review did not see** surfaced during that work, and only when scenarios ran in sequence: `hideSelectionMenu()` is invoked on every scroll event, and its own `roundDoc.focus()` can trigger a scroll, so it runs a second time — and that second call, with `menuSelection` already nulled, overwrote the freshly recorded dismissal with `null`. Registration now happens only on a real visible→hidden transition. This is why S5 passed in isolation and failed in sequence.

**Also fixed:** WR-01 (Shift gesture focus theft — now requires focus to remain on `#round-doc`), IN-02 (missing `return` in branch 3), IN-04 (stale "four call sites" numeral — count dropped, enumeration kept), IN-05 (`e.isComposing` guard, so cancelling an IME candidate window no longer closes the authorization modal).

**Not fixed, deliberately:** WR-02 — `.claude/settings.local.json`'s `Bash(node -e ' *)` grant. It is a real finding, but removing it would also break this pipeline's own inline `node -e` calls, and its marginal exposure is comparable to the pre-existing `Bash(git *)` grant already on line 13. That is a trust-boundary decision for the repository owner, so it is surfaced rather than changed unilaterally.

**IN-01 (constraint wording):** the reviewer is right that the authorized S8-1 copy fix at `app.js:1162` sits inside `renderAnnotations`, which the inherited do-not-touch list names. The user explicitly adjudicated that one-word change, so the later explicit authorization governs; the inherited entry protects that function's rendering logic / DOM construction, which is untouched. Recorded as a wording reconciliation, no code change.

**IN-03 (focus `preventScroll`):** measured rather than assumed — `#doc-panel` scrollTop was 67 before and 67 after the hand-back, so no jump occurred in this environment. Left unchanged, as the claim could not be reproduced.

Post-fix verification: 17/17 scenarios green, guards `check-01..04` PASS, pytest 219 passed / 6 skipped, `frontend/style.css` still byte-unchanged across the phase.

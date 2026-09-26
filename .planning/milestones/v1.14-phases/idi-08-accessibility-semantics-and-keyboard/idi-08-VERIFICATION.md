---
phase: idi-08-accessibility-semantics-and-keyboard
status: passed
verified: 2026-09-25T09:31:45Z
reverified: 2026-09-24T15:31:21Z
score: 35/40 truths verified (4 human, 1 present-but-behavior-unverified, 0 FAILED); re-established first-hand at HEAD 0b6283a, but rows 38–39's mutation proofs remain self-verified in origin
covered_files:

  - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-01-PLAN.md
  - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-01-SUMMARY.md
  - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-02-PLAN.md
  - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-02-SUMMARY.md
  - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-03-PLAN.md
  - .planning/phases/idi-08-accessibility-semantics-and-keyboard/idi-08-03-SUMMARY.md
  - frontend/app.js
  - frontend/index.html
  - scripts/check-05-ui-uat.py
  - scripts/check-07-idi08-validation.py

covered_digest: "v1:sha256:9742bcd1d572f80abf6eb2d5e2f43b6c1d6c0ab10b018fe2577173a11006f6e5"
behavior_unverified: 1
overrides_applied: 0
re_verification:
  previous_status: passed
  previous_score: "35/40 truths verified (4 human, 1 present-but-behavior-unverified, 0 FAILED); 3 of the 35 are self-verified, not independent"
  previous_verified: 2026-09-24T15:31:21Z
  previous_covered_digest: "v1:sha256:f2c2e3e55e3452c814405ecc33e7c48a63aa5c9cdbc9f9a1f65f4d657a467bde"
  gaps_closed: []
  gaps_remaining: []
  regressions: []
resolved_gaps:

  - truth: "ROADMAP Phase 8 Gate: Phase 4/6/7 全部 gate 仍通过 (all Phase 4/6/7 gates still pass)"
    status: resolved
    resolution: >
      User adjudication (2026-09-24) = **amend the gate's scope**. Implemented in `63fba08`:
      `scripts/check-05-ui-uat.py` gains `L5_CONTENT_REGION_MIN_RATIO = 0.5` (now line 2445). A focusable
      element at least half its clipping container's padding-box height is a **content region, not a
      control**; those rows are DECLARED (reported per-row via `info()`, never silently dropped) rather
      than asserted. Control rows are still asserted. If the declaration set ever consumes the whole
      judged set, the assertion goes `blocked(...)` rather than PASS (fail-closed) — that branch is
      `if not asserted: blocked(...)` at `check-05:2627-2634`.
      Re-measured first-hand on 2026-09-25 at HEAD `0b6283a`: `check-05 --item 9 --browser bundled` →
      `PASS (17 条断言, 0 FAIL, 0 BLOCKED)`, exit 0. The declared row is
      `[('#round-doc', '#doc-panel', 778.6, 900, -66.6)]` in p3 and there are **0** declared rows in
      p1 / checking, so the declaration still fires exactly where it is aimed and nowhere else.
    verification_basis: >
      **Outcome independently re-measured; the two mutation proofs remain SELF-VERIFIED — NOT INDEPENDENT.**
      The resolution itself was authored by the same agent that wrote this report, and the two
      re-verification attempts delegated to `gsd-verifier` both stalled (600s watchdog, twice) without
      writing anything; the user then explicitly authorized the orchestrator to write this report. The
      original evidence is therefore first-party. **This 2026-09-25 pass re-ran `--item 9` first-hand and
      re-read the fail-closed branch in the source**, so the resolution's *outcome* now has an independent
      pass; the two mutation experiments (below) were **not** re-run — re-running them requires editing
      `scripts/check-05-ui-uat.py`, which this pass was forbidden to touch. Their *mechanisms* were
      re-confirmed by reading `_idi06_clearance_assert` (`check-05:2584-2645`): `_is_content_region()`
      returns `False` when `elH`/`padBoxH` are missing (fails toward assertion, never toward declaration),
      and an empty assertion set routes to `blocked(...)`, not PASS.
    evidence:
      - "`check-05 --item 9 --browser bundled` at HEAD `0b6283a`: `item 9: PASS (17 条断言, 0 FAIL, 0 BLOCKED)`, exit 0"
      - "Declared row in p3: `[('#round-doc', '#doc-panel', 778.6, 900, -66.6)]`; `0` declared rows in p1 and checking (read from the per-sample `L-5 声明集(内容区,不断言)` INFO lines)"
      - "Mutation A (does not let real violations through — **self-verified, not re-run this pass**): a 30px focusable control injected flush against `#doc-panel`'s bottom edge (clearance 0) lands in the ASSERTED set, not the declared set, and the assertion FAILS. Ratio check: 30/900 = 3.3% < 50%, while `#round-doc` is 778.6/900 = 86.5% >= 50%. Code-level re-confirmation this pass: `_is_content_region` (`check-05:2613-2617`) divides by the container padding box and fails closed when the readings are absent."
      - "Mutation B (no vacuous pass — **self-verified, not re-run this pass**): with the ratio forced to 0.0 (everything declared), item 9 returns `BLOCKED (16 条断言, 0 FAIL, 3 BLOCKED)` — not PASS. Reverted afterwards and verified byte-identical to the backup apart from that one line. Code-level re-confirmation this pass: `if not asserted: blocked(item, …, '判定集被声明集吃光 ⇒ 本样本对控件无判定,不记 PASS')` at `check-05:2627-2634`."
      - "Geometry re-measured first-party (2026-09-24, unchanged by the 2026-09-25 quick task): element 778.64px, container padding box 900px, element offset 188px from the padding-box top; clearance -66.64px at the sample default scroll (scrollTop 0), +4.36px at scrollTop 71, +33.36px at scrollTop 100, and 0.36px once the browser scrolls the element into view (scrollTop 67). Note the 0.36px is the same clip D-02 measured as 3.64px (4 - 0.36 = 3.64)."
      - "Correction to the earlier gap text: the claim that the violation is *structural* (element taller than its container) is FALSE — 778.64 < 900. It was my hypothesis and measurement refuted it. The real property is that clearance sits on the threshold and the element's height is content-driven and unbounded."
    registered_costs:
      - "**UPDATED 2026-09-25 — this cost is now DISCHARGED, not open.** The amendment invalidated the fingerprints of the 4 phases that listed `check-05-ui-uat.py` in `covered_files` (idi-04.1-radix, idi-05, idi-06, idi-07) — D-21/A-4 said 5; the measured count was 4, because idi-04 mentions the script in prose but never listed it. That count was correct for *that* set at the time. **All five sibling reports have since been re-verified on 2026-09-25** (`idi-04` 08:01:44Z, `idi-04.1-radix` 08:18:03Z, `idi-05` 08:36:09Z, `idi-06` 08:52:23Z, `idi-07` 09:11:00Z), each with `.planning/REQUIREMENTS.md` removed from its `covered_files`; all five read `status: passed`. The previously-prescribed closure — 're-run those phases' verify-work' — is therefore **discharged**, and the digests were recomputed at HEAD by those passes rather than refreshed blindly."
      - "**The milestone-wide picture, which is wider than the sentence above.** Quick `260925-iin` (2026-09-25, commits `11fdedb`…`0b6283a`) changed `frontend/app.js` **and** `scripts/check-05-ui-uat.py` **and** `frontend/style.css` **and** two UI-SPECs, so it invalidated **all six** v1.14 phase fingerprints: idi-04 (via `style.css` + `04-UI-SPEC.md`), idi-04.1-radix / idi-05 / idi-06 / idi-07 (via `style.css` + `check-05`), idi-08 (via `app.js` + `check-05`). Five were re-verified on 2026-09-25; **idi-08 is the sixth and is re-established by this pass**."
      - "`idi-04`'s digest had ALSO been stale for an unrelated pre-existing reason (its `covered_files` include `frontend/style.css`, changed after its 2026-09-20 verification at `812a224`). Not caused by this phase; superseded by idi-04's own 2026-09-25 re-verification."

advisory:

  - finding: "`check-05` item 10 SC4 asserts 「每个新 Tab 聚焦元素的 clearance >= 4px」 over a **fixed 12-Tab window** (`_IDI07_TAB_LIMIT = 12`, `check-05:1849`; used at `:3000` and `:3208`) rather than a window tied to the actual stop count"
    category: other
    reason: >
      Re-measured first-hand at HEAD, and the milestone audit §7 already registered it. Not raised as a
      Phase 8 blocker, for three reasons: (a) the phase's own coverage claim for A11Y-02 / A11Y-08 is
      carried by item 10's **census** assertion, which uses an **adaptive** window
      (`_idi07_tab_drive(page, len(data) + 8)`, `check-05:2945`) and passes with 「未覆盖 []」 in all three
      samples; (b) the milestone audit adjudicated this as gate *debt*, not a blocking finding — its only
      blocking finding was §5's auto-follow regression; (c) it is already parked in backlog `999.2`.
      Resolution path: tie the SC4 window to the census length, or state in the assertion's label that it
      is a fixed-window sample. Evidence status: the code reading is deterministic; there is no failing
      test and no reproducible defect.
    evidence_status: "code reading only (`check-05:1849`, `:2945`, `:3000`, `:3208`); no failing test, no reproducible defect"

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
      across the extension. **Re-checked 2026-09-25**: the quick task's one-line `renderEvent` change is
      in a disjoint function and cannot reach this path; the listener is still at `app.js:1477` and the
      gesture body is still unmodified.

human_verification:

  - test: "A11Y-08 — Tab through a phase-3 project and a phase-5 self-check project and confirm the Tab order reaches every interactive control"
    expected: "Every interactive control is reachable by Tab; the new `#round-doc` stop sits at position 2 (immediately after `#round-switcher`, immediately before `#btn-authorize` when `#authorize-row` is visible)"
    why_human: "The machine half is complete and green (check-05 --item 10: `[p3] 判定集 10 个元素,未覆盖 []`; SUMMARY 03's own census reaches 10/10 in p3 and 8/8 in checking), but `every interactive control` is an on-screen enumeration across states the harness does not sample (notably `archive`, which item 10 cannot reach — its sample set is hardcoded to p1/checking/p3). **Adjudicated pass by the user in `idi-08-UAT.md` test 1 (2026-09-24)**; retained here because it is a human item, not because it is unresolved."
  - test: "A11Y-03 keyboard-selection leg — hold Shift and press Arrow to extend a selection, then release Shift"
    expected: "The selection extends past one character, the menu appears, focus lands on `#btn-annotate`; Escape then closes the menu, returns focus to `#round-doc`, and the selection survives so `Shift+Arrow` can keep extending"
    why_human: "Keyboard text selection cannot be automated here (not even inside `contenteditable`). Per ROADMAP Phase 8 §Manual checks an automated non-result on this leg is not a functional-defect call. **Adjudicated pass in `idi-08-UAT.md` test 2 (2026-09-24).**"
  - test: "REG-03 items 1, 2, 3, 5, 6 plus the rewritten item 4 step 3, re-run by hand"
    expected: "All six `b9664e0` manual acceptance items behave as recorded in idi-08-03-SUMMARY.md §REG-03 observation record"
    why_human: "The keyboard-dependent legs (item 4's extension step, and the keyboard-origin variants of the others) cannot be automated; the executor recorded steps 1/2/4/5 machine-observed PASS and handed step 3 over explicitly. **Adjudicated pass in `idi-08-UAT.md` test 3 (2026-09-24).**"
  - test: "Backstop UI-consideration truths for E1 (#round-doc), E2 (#selection-menu), E3 (#confirmation-modal), E4 (#tier-modal), E5 (#app), E6 (the other three overlays): loading / error / overflow / long-text / empty / partial"
    expected: "Each declared backstop either has an observable contract or is confirmed not applicable to that element"
    why_human: "Declared `verification: backstop` in the plan frontmatter — the planner abstained rather than committed a criterion, so there is no spec to verify against. Most are not applicable (a static div, a two-button menu, `#app`), but that is an adjudication, not a measurement. **Adjudicated pass in `idi-08-UAT.md` test 4 (2026-09-24).**"
  - test: "The phase-5 zero-height `#round-doc` Tab stop (SUMMARY 03 §Deviation 2)"
    expected: "Confirm whether a 351 × 0 Tab stop whose ring renders as a thin horizontal line is acceptable, or make the attribute conditional"
    why_human: "Registered by the executor, not fixed (a conditional attribute would change a plan-01 deliverable). It is a design decision, not a measurement. **Adjudicated acceptable in `idi-08-UAT.md` test 5 (2026-09-24).**"

---

# Phase 8: 可访问性语义与键盘 (idi-08) Verification Report

**Phase Goal:** 键盘用户能真实完成一次划词批注,能 Esc 关闭两个阻塞式弹窗;两个阻塞弹窗向辅助技术宣告的语义与其实现一致;内联错误不再破坏控件行;五条已交付修复的人工验收项全部重跑通过。
**Verified:** 2026-09-25T09:31:45Z · **Tree:** HEAD `0b6283a` (branch `ui/baseline-and-tokens`)
**Status:** `passed` (canonical:UAT 已裁定后按仓库惯例 canonicalize —— 同型先例见 §重验证披露).
**The verifier determination for this pass is `human_needed`** — its constituents are the 4 named HUMAN
rows (32, 33, 34, 36), the 1 present-but-behavior-unverified row (35), and the 5 `human_verification`
items above. All five were adjudicated `pass` by the user in `idi-08-UAT.md` (2026-09-24), and the
frontmatter `status: passed` was set by `fbb2276` ("canonicalize verification status after UAT passed")
on that basis. Readers should not read the two halves as contradictory; they record two different things.
**Re-verification:** **Yes — 内容真变后的重验证**(not a fingerprint refresh). Two `covered_files` members
changed bytes after the 2026-09-24 re-verification at `ad43f64`. See §重验证披露.

> **Timestamp note (registered, not corrected).** The report's **original** `verified:` stamp read
> `2026-09-24T15:52:00Z`, which was **wrong**: the file was written at 15:30 **local** (CST, UTC+8) =
> 07:30 UTC, i.e. the independent pass labelled local time with a `Z` suffix. That is why the 2026-09-24
> re-verification's correct UTC stamp (`13:23:27Z`) read *earlier* than it. The original stamp was left
> as written for two rounds rather than rewritten. **On 2026-09-25 this pass replaced `verified:` with a
> fresh, correctly-computed UTC stamp**; the mislabelled original is preserved here so it is not re-used
> for staleness reasoning.

**Tree verified:** HEAD (`0b6283a`). Three commits landed after all three plans were summarized:
`62dfd3e` (an INCOMPLETE first attempt at the Escape fix), `09b170d` (the real Escape fix), and
`63fba08` (the L-5 gap resolution). Where a SUMMARY's prose disagrees with HEAD, HEAD wins and the
disagreement is registered under §SUMMARY ↔ HEAD Disagreements — not treated as a gap.

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | SC1b: Esc closes `#confirmation-modal` | ✓ VERIFIED | **Re-run 2026-09-25** via the committed harness: `check-07 --item g1` `PASS g1 [#confirmation-modal] 受信 Escape 关闭弹窗: expected=hidden=true actual=hidden=True` (with the discriminating control 「非 Escape 按键不关闭弹窗」 also PASS) |
| 2 | SC1c: Esc closes `#tier-modal` | ✓ VERIFIED | **Re-run 2026-09-25**: `check-07 --item g1` on the `phase5_awaiting_tier` fixture → `PASS … 受信 Escape 关闭弹窗: expected=hidden=true actual=hidden=True`; focus hand-back `actual=btn-continue-check` |
| 3 | SC3: both blocking modals declare modal-dialog semantics consistent with implementation | ✓ VERIFIED | **Re-run 2026-09-25**: `check-07 --item g2` → for each modal `role == dialog`, `aria-modal == true`, `aria-labelledby` resolves, accessible name non-empty and taken from a heading **inside** the modal (`授权确认` / `选择自检档位`). The declaration is made true by `inert` on `#app` (truth 17) and by the Escape closes above |
| 4 | SC4: inline error not squeezed into a narrow column; view switches clear stale errors; error path is `textContent` only | ✓ VERIFIED | `showInlineError` (`app.js:317-324`) writes only `p.textContent`, anchored to `probeControls` / `enterForm` / `checkSwitcher` (all block-flow containers); `grep -n 'innerHTML' frontend/app.js` shows no user-content concatenation; `grep -c 'clearInlineError();' frontend/app.js` = **9** (re-measured) |
| 5 | SC5: `node --check app.js` passes; pytest 219 baseline unchanged | ✓ VERIFIED | **Re-run 2026-09-25**: `node --check frontend/app.js` exit 0; `.venv/bin/python -m pytest -q` → **219 passed, 6 skipped** in 6.57s |
| 6 | A11Y-02 gate: `tabindex` count and `:focus-visible` count do not move independently | ✓ VERIFIED | **Re-measured**: `grep -c tabindex frontend/index.html` = 1 (was 0); `grep -v '^#' frontend/style.css \| grep -c ':focus-visible'` = 9 (> 0) |
| 7 | Tab reaches the round-document area and the whole-box ring draws on `#round-doc` | ✓ VERIFIED | **Re-run**: `check-05 --item 10 --browser bundled` → `PASS (42 条断言, 0 FAIL, 0 BLOCKED)`, exit 0. `[p3]` Tab sequence includes `#round-doc` (`tag: div`) with `outlineWidth 2px` / `focusVisible true`; judged set 10, uncovered `[]` |
| 8 | At the moment `#round-doc` is `document.activeElement`, computed `outline-width` is exactly 2px and `outline-color` equals the runtime-resolved `--color-focus` | ✓ VERIFIED | **Re-run**: item 10 `[p3]` reads `#round-doc` → `outlineWidth '2px'`, `outlineOffset '2px'`, `outlineColor 'rgb(31, 99, 189)'` == the harness's runtime-resolved `--color-focus=rgb(31, 99, 189)` |
| 9 | Releasing Shift shows `#selection-menu` with focus on `#btn-annotate` | ✓ VERIFIED | **Re-run**: `check-07 --item g3` `PASS g3 拖拽后菜单可见 … hidden=False` then `PASS g3 松开 Shift 把焦点送入 #btn-annotate(真实手势,非程序化移焦): expected=btn-annotate actual=btn-annotate` |
| 10 | Escape dismisses the menu durably and hands focus back to `#round-doc` (focus neither on a hidden button nor back on `<body>`) | ✓ VERIFIED | **Re-run**: `check-07 --item g3` — `Escape` → hidden; the immediately-following Escape **keyup** → still hidden; `ArrowRight` keyup → still hidden; a second `Escape` → still hidden; selection survives (`len=12`, D-08). The harness also runs the mutation control (`守卫置空后同一 keyup 重新弹开菜单`) so the green is not恒绿 |
| 11 | Menu items hand focus back to `#round-doc` after executing | ✓ VERIFIED | **Regression check 2026-09-25** (code-level, since the original behavioural probe was a one-off): both handlers call `hideSelectionMenu()` as their **first** statement (`app.js:1499-1501`, `app.js:1529-1531`), and `hideSelectionMenu` (`app.js:1348-1377`) computes `hadFocus = selectionMenu.contains(document.activeElement)` **before** `classList.add('hidden')` and then calls `roundDoc.focus()` (line 1376). g3's positive control independently reads `active: 'round-doc'` |
| 12 | `#draft-content` keeps no `tabindex` | ✓ VERIFIED | **Re-measured**: `frontend/index.html:113` — `id="draft-content" class="markdown-body"`, no attribute |
| 13 | `#round-doc` gains zero attributes besides `tabindex` (no `role`, no `aria-label`) | ✓ VERIFIED | **Re-measured**: `git diff 4976bee..HEAD -- frontend/index.html` — the only change to that line is `+ tabindex="0"` |
| 14 | E1 overflow / long-text: no new container, no new clipping rule; `overflow-wrap: anywhere` and `#doc-panel-body { padding: 32px 40px }` unchanged | ✓ VERIFIED | **Re-measured at HEAD**: `overflow-wrap: anywhere` present at `style.css:1488`; `#doc-panel-body { padding: var(--space-8) var(--space-10); }` at `style.css:665` with `--space-8: 32px` / `--space-10: 40px`; the phase's own commit range added no container and no clipping rule. ⚠ **The evidence line originally read 「style.css blob byte-identical at phase base and HEAD」 — that literal claim no longer holds at HEAD; see §重验证披露.** The substantive property above is re-measured directly and holds |
| 15 | E2 long-text: the two menu labels stay verbatim | ✓ VERIFIED | **Re-measured**: `frontend/index.html:250-251` — `批注` / `用大白话讲这段` |
| 16 | Both modals carry `role="dialog"` + `aria-modal="true"`, named from the existing `<h3>` via a new id | ✓ VERIFIED | **Re-measured**: `index.html:207-209`, `226-228`; `grep -o 'id="[^"]*"' frontend/index.html \| wc -l` = **82** (was 80); the diff's `-` id lines are in-place edits of the same ids — zero renames/deletions |
| 17 | Background inert while either modal is open, removed when both close; scoped to `#app` only | ✓ VERIFIED | **Re-run**: `check-07 --item g2` for both modals — on open `#app` carries `inert` (attr + IDL true) while `document.body`, the open modal itself, and `#selection-menu` are all `false`; on close `#app` releases it. `syncBackgroundInert()` (`app.js:521-526`) derives from both modals' `.hidden`; **5 call sites** at 495, 501, 674, 840, **1611** (the earlier report's `1606` was already stale at `ad43f64` — anchor corrected) |
| 18 | Escape on `#confirmation-modal` produces no decision (does not substitute for "拒绝") | ✓ VERIFIED | **Re-run**: `check-07 --item g1` — `PASS … Escape 零决定:未弹出任何原生对话框(不等于「拒绝」): expected=0 个 actual=0 个` and `PASS … 未发出任何写批注/授权 POST`; the branch calls `closeConfirmModal()` + `authorizeBtn.focus()` only (`app.js:1598-1603`) |
| 19 | Escape on `#tier-modal` resets `tierModalShown` (next self-check event can re-pop) | ✓ VERIFIED | **Re-run**: `check-07 --item g1` — `PASS … Escape 复位 tierModalShown(D-13 死状态的实质修复): expected=false actual=False` and `PASS … 复位生效:下一个自检事件能重新弹出(死状态已消): expected=hidden=false actual=hidden=False`. Code: `app.js:1610` |
| 20 | `#tier-modal` focuses `#btn-tier-loose` on open | ✓ VERIFIED | **Code re-verified at HEAD** (`app.js:671-680`): `remove('hidden')` → `syncBackgroundInert()` → `tierLooseBtn.focus()`, in that order. Corroborated by g2's inert reading `{'before': 'btn-tier-loose', …}` (focus is inside the modal at the moment it opens) |
| 21 | F1-d hand-backs: confirm → `#btn-authorize`; tier → `#btn-continue-check` | ✓ VERIFIED | **Re-run**: g1 reads `active=btn-authorize` after the confirm Escape, and `active=btn-continue-check` after the tier Escape |
| 22 | The other three overlays deliberately do not respond to Escape (scope lock D-11) | ✓ VERIFIED | **Re-run**: `check-07 --item g1` — force-opened `#permission-modal` / `#mission-complete-modal` / `#cli-check-overlay` all still visible after a trusted Escape; g2 also reads `role=null aria-modal=null` for all three |
| 23 | Escape dispatch follows an explicit priority table (menu → confirm → tier), independent of source order | ✓ VERIFIED | `app.js:1564-1619`; branches 1/2/3 each `preventDefault()` and `return`, the "deliberate non-responders" block follows. Gate at `app.js:1580` (`if (e.key !== 'Escape') return;`) plus the `isComposing` guard at 1579 |
| 24 | E3 empty: `#btn-confirm-authorize.disabled === true` while `#confirm-word-input` is empty | ✓ VERIFIED | **Code re-verified at HEAD**: `app.js:563-566` — `confirmAuthorizeBtn.disabled = !(confirmWordInput.value.trim() === CONFIRM_WORD)`, and `app.js:492` sets the initial `disabled = true` on open |
| 25 | E3 error: the confirm error copy is written via `textContent` only | ✓ VERIFIED | **Re-measured**: `app.js:575`, `app.js:583` — `confirmError.textContent = …`; no `innerHTML` on that path |
| 26 | S8-1: the empty-annotation copy reads 「本轮暂无批注——在右侧文档划词即可批注。」 | ✓ VERIFIED | **Code re-verified at HEAD**: `app.js:1167` inside `renderAnnotations`'s zero-item branch, guarded by `isCurrentRound`; `grep -c '在左侧文档划词即可批注'` = 0; the historical-round variant `该轮暂无批注。` is byte-identical and untouched |
| 27 | REG-02 gate ①: `grep -c 'inline-error' frontend/style.css` is still 1 | ✓ VERIFIED | **Re-measured**: 1 |
| 28 | REG-02 gate ②: `grep -c 'clearInlineError();' frontend/app.js` >= 9 (baseline 9, only grows) | ✓ VERIFIED | **Re-measured**: 9 (`app.js:318, 327, 468, 636, 868, 1298, 1657, 1707, 1731` — anchors refreshed; the earlier report's post-640 anchors were 5 lines low) |
| 29 | Archive path: after switching rounds, 「处理本轮批注」 is not clickable | ✓ VERIFIED | **Code re-verified at HEAD**: `applyArchiveView` (`app.js:867-876`) sets `processRoundBtn.classList.add('hidden')` + `disabled = true`; the round switcher routes to `loadArchiveRoundDoc(n)` (`app.js:1300`), and that function (`app.js:920-929`) never touches `processRoundBtn` — so the archive state persists across a round switch. (The original behavioural probe's reading is corroborated by the mechanism; §SUMMARY ↔ HEAD Disagreements #5 stands.) |
| 30 | check-01…04 all PASS at HEAD; `frontend/vendor/` holds exactly one file; **this phase's own commit range changed zero bytes of `frontend/style.css`** | ✓ VERIFIED | **Re-run 2026-09-25**: `check-01` PASS, `check-02` `PASS: 0 failures` (ORDER 0.363), `check-03` PASS, `check-04` PASS; `ls frontend/vendor/` → `marked.min.js`. `git rev-parse 4976bee:frontend/style.css` = `git rev-parse ad43f64:frontend/style.css` = `95cb22ee2f7946858869c41dd33a6d7fcc027d59` — the phase introduced zero CSS bytes. ⚠ **The row's original wording 「`frontend/style.css` byte-unchanged」 is FALSE as a statement about HEAD** (`HEAD:frontend/style.css` = `3ce1565a…`, edited by quick `260925-iin` after the phase closed). Re-scoped to the phase-scoped claim, which is what the row was always for; see §重验证披露 |
| 31 | Fingerprint obligation registered (D-01 path ⇒ zero debt; `frontend/app.js` / `frontend/index.html` in no live report's `covered_files`) | ✓ VERIFIED | **Re-checked 2026-09-25** against idi-04 / idi-04.1-radix / idi-05 / idi-06 / idi-07 `covered_files` — none names `frontend/app.js` or `frontend/index.html`. This phase's own two source files therefore invalidate no sibling report; the only report they invalidate is this one, which is exactly why this pass exists |
| 32 | SC1a / A11Y-08: the Tab order reaches every interactive control | ? HUMAN | Machine half green in the sampled states (**re-run**: item 10 judged set **9 / 9 / 10** across p1 / checking / p3, uncovered `[]` in all three; raw census 29 elements each); full enumeration across states incl. `archive` is on-screen. UAT test 1 = pass |
| 33 | SC2: a keyboard user can really complete one selection annotation | ? HUMAN | Mouse-origin selection → Shift release → focus in the menu is machine-proven (g3, re-run); the keyboard-origin selection extension cannot be automated. UAT test 2 = pass |
| 34 | SC5b / REG-03: all `b9664e0` manual acceptance items re-run | ? HUMAN | Six items recorded in SUMMARY 03 §REG-03 observation record with machine-observed PASS on 1/2/3/5/6 and item 4 steps 1/2/4/5; the keyboard-dependent halves stay human. UAT test 3 = pass |
| 35 | Shift+Arrow extension does not move focus (the invariant the gesture design exists to protect) | ⚠️ PRESENT_BEHAVIOR_UNVERIFIED | Present + wired (key-filtered Shift listener at `app.js:1477`; `handleSelectionTrigger` body untouched), but no test exercises the invariant — see `behavior_unverified_items` |
| 36 | A11Y-08 census records `#round-doc`'s Tab position, not merely "Tab can reach it" | ? HUMAN | SUMMARY 03 records position 2, before `#round-switcher` / after `#btn-authorize`; item 10 independently agrees on the judged set. On-screen confirmation is human. UAT test 1 = pass |
| 37 | ROADMAP Phase 8 Gate: all Phase 4/6/7 gates still pass | ✓ VERIFIED (resolved) | **Re-run 2026-09-25**: `check-05 --item 9 --browser bundled` → `PASS (17 条断言, 0 FAIL, 0 BLOCKED)`, exit 0, after `63fba08`'s L-5 content-region declaration set. Was FAIL at `a640f39`. The resolution's *outcome* is now independently re-measured; its mutation proofs remain self-verified — see §Gap Resolution |
| 38 | The L-5 declaration set does not let a real control violation through | ✓ VERIFIED (self) | Mutation: a 30px control injected flush at `#doc-panel`'s bottom edge (clearance 0) lands in the ASSERTED set and the assertion FAILS. **Not re-run this pass** (would require editing `check-05`); the mechanism was re-confirmed in code — `_is_content_region` fails closed when `elH`/`padBoxH` are absent. See §Gap Resolution |
| 39 | The L-5 declaration set cannot produce a vacuous pass | ✓ VERIFIED (self) | Mutation: ratio forced to 0.0 ⇒ `item 9: BLOCKED (16 条断言, 0 FAIL, 3 BLOCKED)`, not PASS. Reverted and diff-verified. **Not re-run this pass**; the fail-closed branch was re-read at `check-05:2627-2634`. See §Gap Resolution |
| 40 | 选档成功后焦点交还 `#btn-continue-check`(F1-d 的成功路径) | ✓ VERIFIED (**now independently re-run**) | **Re-run 2026-09-25**: `check-07 --item g4` exit 0 — `PASS g4 实例 1/2 选档后 #tier-modal 已隐藏`, `PASS g4 选档成功后焦点交还 #btn-continue-check(F1-d 成功路径): expected=btn-continue-check actual=btn-continue-check`, **and** `PASS g4 判别控制:交还调用被置空后焦点不再落在 #btn-continue-check … actual=BODY` — so the green is demonstrably not vacuous. Placement is measured, not assumed: the call sits after `await refreshChecksAfterStream()` (`app.js:842` → `app.js:847`), and `.focus()` on a disabled button is a silent no-op. The harness records `BLOCKED` (never `PASS`) if the button is not focusable at hand-back time |

**Score:** 35/40 truths verified — 4 HUMAN (rows 32, 33, 34, 36), 1 present-but-behavior-unverified
(row 35), **0 FAILED**. Rows 37–40 remain self-verified **in origin** (their author wrote them under
explicit user authorization); this pass re-measured row 37's and row 40's *outcomes* first-hand — row 40
is now fully independent, including its discriminating control — while rows 38–39's two mutation
experiments were not re-run and their mechanisms were re-confirmed by reading the source.

*(The 2026-09-24 pass's score line read "31/37 … 5 human" — its counts summed to 38 against a 37-row
table, and "5 human" counted the frontmatter's `human_verification` entries rather than the table's
HUMAN rows. Recounted by status cell so the arithmetic actually closes: 35 + 4 + 1 = 40.)*

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `frontend/index.html` | `#round-doc` with `tabindex="0"`; 2 new ids; two ARIA triples; zero renames/deletions | ✓ VERIFIED | **Re-measured**: id count 80 → 82; `tabindex` 0 → 1; the diff's `-` id lines are in-place edits of the same ids. **Unchanged by quick `260925-iin`** (`git diff bc563d7..HEAD -- frontend/index.html` is empty) |
| `frontend/app.js` | Shift submit listener; F1-a/b/c hand-back; `appEl`; `syncBackgroundInert()` + 5 call sites; tier focus-on-open + flag reset; Escape dispatcher; two F1-d hand-backs; S8-1 copy | ✓ VERIFIED | All present and behaviourally exercised (truths 9–11, 17–21, 26, 40). **One line changed since the previous verification** — `renderEvent`'s `eventsEl.scrollTop = eventsEl.scrollHeight` → `item.scrollIntoView({ block: 'nearest' })` at `app.js:253` (quick `260925-iin` F1). The change is disjoint from every deliverable in this row; see §重验证披露 |
| `frontend/style.css` | **unchanged by this phase** (deliberate, D-01 path) | ✓ VERIFIED (phase-scoped) | `git rev-parse 4976bee:frontend/style.css` == `git rev-parse ad43f64:frontend/style.css` == `95cb22ee…` — the phase's own commit range added zero CSS bytes. ⚠ **The file is no longer byte-identical at HEAD** (`3ce1565a…`) — quick `260925-iin` FIX 1 declared an 8th type tier and re-pointed `.collapse-indicator` at it. `frontend/style.css` is **not** in this report's `covered_files` (a scope decision this pass was instructed not to widen); the drift is disclosed in §重验证披露 rather than absorbed silently |
| `frontend/vendor/` | exactly one file | ✓ VERIFIED | **Re-measured**: `marked.min.js` |
| `scripts/check-05-ui-uat.py`, `scripts/probe-07-focus-composite.py` | `probe-07` unchanged and re-run; `check-05` **amended at `63fba08`** (user ruling) and **again by quick `260925-iin`** | ✓ VERIFIED | **Re-run 2026-09-25**: probe-07 exit 0 (`links-before 0` → `links-after 1`; ring 2px / `rgb(31,99,189)`; archive composite **3.45** ≥ 3.0). `check-05` gained `L5_CONTENT_REGION_MIN_RATIO` + a declaration/assertion split in `_idi06_clearance_assert` (the only authorized exception to D-21), then — via `260925-iin` — a new item-9 auto-follow assertion (**16 → 17**), a corrected `--color-text-muted` diagnostic, and a fifth static guard tying `FOCUSABLE_SELECTOR` to the CSS `:focus-visible` enumeration (**item 10: 41 → 42**). No pre-existing assertion or constant was weakened; the two additions are purely additive |
| `scripts/check-07-idi08-validation.py` | the phase's own harness | ✓ VERIFIED | **Re-run 2026-09-25**: `item g1: PASS (21)` / `g2: PASS (39)` / `g3: PASS (10)` / `g4: PASS (3)`, exit 0. Unchanged by quick `260925-iin` |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `frontend/index.html:163` (`#round-doc`) | `frontend/style.css:1519-1528` (`[tabindex]:focus-visible`) | Phase 7's enum rule fires on the new attribute, zero CSS | ✓ WIRED | **Re-run**: item 10 reads 2px / `rgb(31, 99, 189)` / `focusVisible true` at the moment `#round-doc` is focused. **New in this pass**: the enum itself is now gated — item 10's static guard ⑤ reads `CSS 侧(规则块起始行=1519)= ['button','input','select','textarea','a[href]','summary','[tabindex]']` and `Python 侧(常量定义行=1751)= [同]`, `对称差=[]` |
| `frontend/app.js:1477` (document-level Shift-only `keyup` listener) | `frontend/index.html:250` (`#btn-annotate`) | release Shift ∧ menu visible ∧ selection non-collapsed ⇒ `annotateBtn.focus()` (`app.js:1487`) | ✓ WIRED | **Re-run**: g3 `actual=btn-annotate` from a real trusted Shift release |
| `frontend/app.js` (`hideSelectionMenu`, `app.js:1348-1377`) | `frontend/index.html:163` (`#round-doc`) | `selectionMenu.contains(document.activeElement)` before hiding ⇒ `roundDoc.focus()` (line 1376) | ✓ WIRED | **Re-run**: Escape and the menu items both route through this single function; g3's Escape lands focus on `#round-doc` |
| `frontend/app.js` (`syncBackgroundInert`, `app.js:521-526`) | `frontend/index.html:10` (`#app`) | `appEl.set/removeAttribute('inert')` derived from both modals' `.hidden` | ✓ WIRED | **Re-run**: `#app` only, every sibling `false`, `body` `false`, and the inert state is behaviourally read (background focus does not move while inert, does move when not) |
| `frontend/index.html:207/226` (the two `.overlay`s) | `#confirmation-modal-title` / `#tier-modal-title` | `aria-labelledby` → the on-screen `<h3>` | ✓ WIRED | **Re-run**: accessible names read `授权确认` / `选择自检档位`, each resolved from a target **inside** its own modal; the harness mutates the id to prove the resolver is not恒真 |
| `frontend/app.js:1564-1619` (Escape dispatcher) | `hideSelectionMenu()` / `closeConfirmModal()` / tier close branch | explicit priority table reading the three `.hidden` states | ✓ WIRED | **Re-run**: behavioural probes for all three branches + the negative scope check on the other three overlays |
| `frontend/app.js:1167` (`renderAnnotations` empty state) | DESIGN.md §4.1 v1.14 | one-word copy fix | ✓ WIRED | Code-verified at HEAD; the string is written via `textContent` in the zero-item ∧ `isCurrentRound` branch |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `#round-doc` ring | `outline-color` | runtime-resolved `--color-focus` (not hardcoded) | Yes — item 10 reads `rgb(31, 99, 189)` and cross-checks against the token | ✓ FLOWING |
| `#selection-menu` visibility | `.hidden` class | `handleSelectionTrigger` / `hideSelectionMenu` from the live `window.getSelection()` | Yes — g3 reads `hidden` flipping with a real 12-char drag selection, and the mutation control flips it back | ✓ FLOWING |
| `#app[inert]` | native `inert` attribute | derived from both modals' `.hidden` | Yes — g2 reads it appear/disappear with open/close, plus the IDL boolean | ✓ FLOWING |
| `#annotation-list .hint` | `textContent` | `renderAnnotations` on the p3 fixture | Yes — the fixed copy is the literal assigned in that branch | ✓ FLOWING |
| `#main-pane` scroll position (quick `260925-iin` F1, **not** a Phase 8 deliverable) | `scrollTop` | `item.scrollIntoView({block:'nearest'})` in `renderEvent` (`app.js:253`) | Yes — item 9 reads `before=0 after=1721`, with the probe JS containing zero `scrollTop` assignments | ✓ FLOWING |

### Behavioral Spot-Checks

All rows below were **re-run first-hand on 2026-09-25 at HEAD `0b6283a`** unless marked otherwise.

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Escape closes `#confirmation-modal`, removes `inert`, hands focus back | `check-07-idi08-validation.py` item g1 (committed harness) | `hidden=True`, no prompt, no POST delta, `active=btn-authorize` | ✓ PASS |
| Escape closes `#tier-modal`, resets the flag, hands focus back | `check-07-idi08-validation.py` item g1 | `hidden=True`, `tierModalShown=False`, re-pop on re-trigger `True`, `active=btn-continue-check` | ✓ PASS |
| Escape dismisses the menu and it stays dismissed | `check-07-idi08-validation.py` item g3 | hidden across keyup / `ArrowRight` / second `Escape`; selection survives (len 12); mutation control re-opens it | ✓ PASS |
| Out-of-scope overlays ignore Escape | `check-07-idi08-validation.py` item g1 | all three still visible | ✓ PASS |
| Dialog semantics + background `inert` | `check-07-idi08-validation.py` item g2 | 39 assertions, incl. 6 mutation controls, 0 FAIL | ✓ PASS |
| F1-d tier hand-back (success path) | `check-07-idi08-validation.py` item g4 | `actual=btn-continue-check`; discriminating control `actual=BODY` | ✓ PASS |
| Item 9 L-5 clearance (Phase 6 gate) | `.venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled` | `PASS (17 条断言, 0 FAIL, 0 BLOCKED)`; declared row `[('#round-doc','#doc-panel',778.6,900,-66.6)]` in p3, **0** declared rows in p1/checking | ✓ PASS (was FAIL — resolved at `63fba08`) |
| Item 9 auto-follow assertion (quick `260925-iin` F1) | same run | `INFO … before=0 after=1721 scrollHeight=2640 clientHeight=900 pane=[0,900] last=[848,900]`; assertion PASS | ✓ PASS |
| Item 10 focus-ring census + static guard ⑤ | `.venv/bin/python scripts/check-05-ui-uat.py --item 10 --browser bundled` | `PASS (42 条断言, 0 FAIL, 0 BLOCKED)`; judged sets 9/9/10, uncovered `[]`; `对称差=[]` | ✓ PASS |
| Items 1 / 2 / 3 / 4 / 6 / 7 / 8 | `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` (one full run, saved) | `45` / `5` / `17` / `65` / `6` / `38` / `13` assertions, all PASS, 0 FAIL | ✓ PASS |
| pytest baseline | `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped` in 6.57s | ✓ PASS |
| check-01…04 | `bash scripts/check-01…` / `.venv/bin/python scripts/check-02-contrast.py` / `check-03` / `check-04` | PASS; check-02 `PASS: 0 failures` (ORDER 0.363); check-03 PASS; check-04 PASS | ✓ PASS |
| check-06 (Phase 5's harness, unchanged) | `.venv/bin/python scripts/check-06-idi05-validation.py` | g1…g6 PASS (9/2/12/5/5/7), exit 0 | ✓ PASS |
| probe-07 focus composite | `.venv/bin/python scripts/probe-07-focus-composite.py` | links 0 → 1; ring 2px / `rgb(31,99,189)`; archive composite `3.45 ≥ 3.0`; exit 0 | ✓ PASS |
| S8-1 copy in the intended state/position | code-level regression check (`app.js:1167`) | string present verbatim in the zero-item ∧ current-round branch; stale variant count 0 | ✓ PASS (code-level) |
| Archive round-switch leaves 「处理本轮批注」 unclickable | code-level regression check (`app.js:867-876`, `:920-929`, `:1300`) | archive state hides+disables the button; the round-switch path never resets it | ✓ PASS (code-level) |
| E3 empty-state gating | code-level regression check (`app.js:492`, `:563-566`) | `disabled` derives from `value.trim() === CONFIRM_WORD`; initial state disabled | ✓ PASS (code-level) |

`check-05 --item 5` was not run: it requires `--ai-smoke`, which makes real AI calls. It is not a
Phase 4/6/7 gate for this phase's deliverables and was not claimed by any Phase 8 artifact. The full
`check-05 --browser bundled` run therefore exits **2** (item 5 `BLOCKED` ×2 by design) while items
1/2/3/4/6/7/8/9/10 are all PASS — expected, not a regression.

### Probe Execution

No `scripts/*/tests/probe-*.sh` convention exists in this repo; PLAN/SUMMARY declare no probe paths.
The nearest equivalent, `scripts/probe-07-focus-composite.py` (re-run obligation D-04), was executed
from the repo root and passed — see the spot-check table. `scripts/probe-05-resolve-color.py` belongs to
Phase 4.1 and was not re-run here.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| A11Y-02 | idi-08-01 | `#round-doc` gets `tabindex="0"` in the same commit as focus styling | ✓ SATISFIED | `tabindex` 0 → 1 (`bbf9060`, `index.html` only); `:focus-visible` stays 9; the Phase 7 enum rule supplies the ring with zero CSS (truths 6-8, re-run) |
| A11Y-03 | idi-08-01 | A keyboard user can genuinely reach selection annotation | ? NEEDS HUMAN | Shift-release gesture + focus hand-off machine-verified (g3, re-run); the keyboard-origin selection extension cannot be automated. UAT test 2 = pass |
| A11Y-05 | idi-08-02 | Both blocking modals support Escape close | ✓ SATISFIED | Truths 1, 2, 18, 19 (all re-run through the committed harness) |
| A11Y-06 | idi-08-02 | Both modals get `role="dialog"` + `aria-modal="true"` | ✓ SATISFIED | Truths 3, 16, 17 — the declaration is made true by `inert`, re-run |
| A11Y-08 | idi-08-03 | Keyboard reachability manual acceptance | ? NEEDS HUMAN | Machine half green (truths 32, 36); full enumeration is on-screen. UAT test 1 = pass |
| REG-03 | idi-08-03 | All `b9664e0` manual acceptance items re-run | ? NEEDS HUMAN | Truth 34; the keyboard-dependent halves stay human. UAT test 3 = pass |

No orphaned requirements: all six IDs mapped to Phase 8 in REQUIREMENTS.md appear in a plan's
`requirements:` field (01 → A11Y-02/03, 02 → A11Y-05/06, 03 → A11Y-08/REG-03), and no plan declares
an ID that REQUIREMENTS.md does not map to Phase 8. REQUIREMENTS.md showing all six as Complete is
expected — each plan's completion commit flips its own IDs, and `phase.complete` has since run (the
ROADMAP Phase 8 row reads `Complete`, 2026-09-24). Not a discrepancy.

> **`covered_files` note.** `.planning/REQUIREMENTS.md` was **removed** from this report's `covered_files`
> on 2026-09-25 (user ruling, applied to all six v1.14 reports) and `covered_digest` was recomputed over
> the remaining 10 files. Rationale in §重验证披露. The requirement mapping above is still read from that
> file as *context*; it is simply no longer treated as an input whose change invalidates this report.

### Decision Coverage

All trackable `08-CONTEXT.md` `<decisions>` entries are honored by shipped artifacts.

`gsd-tools query check.decision-coverage-verify` → `{total: 26, honored: 26, not_honored: []}` —
"All trackable CONTEXT.md decisions are honored by shipped artifacts."

### Test Quality Audit

| Test surface | Linked Req | Active | Skipped | Circular | Assertion level | Verdict |
|--------------|-----------|--------|---------|----------|-----------------|---------|
| `scripts/check-07-idi08-validation.py` (g1/g2/g3/g4) | A11Y-05, A11Y-06, A11Y-03 | 73 assertions | 0 | none | Behavioral (live DOM + trusted key events + mutation controls) | ✓ adequate |
| `scripts/check-05-ui-uat.py` item 9 / item 10 | A11Y-02, A11Y-08, REG-03 | 17 + 42 assertions | 0 | none | Behavioral (computed style / geometry / Tab drive) + 5 static contract guards | ✓ adequate |
| `backend/tests/` (pytest) | REG-03 (baseline) | 219 | 6 | none | unit + e2e | ✓ adequate |

**Disabled tests on requirements:** 0. The 6 pytest skips are the pre-existing `@pytest.mark.slow`
e2e cases gated on `IDI_E2E` (real AI calls); none is linked to a Phase 8 requirement.
**Circular patterns detected:** 0 — no harness writes expected values, and every expected value in
`check-07`/`check-05` is either read from the live DOM or resolved at runtime from a token.
**Insufficient assertions:** 0 for the machine-covered requirements; the two genuinely
under-specified halves (keyboard-origin selection, cross-state Tab enumeration) are declared HUMAN
rather than covered by a weaker proxy.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `.claude/settings.local.json` | 24 | `Bash(node -e ' *)` pre-approves arbitrary JavaScript execution | ⚠️ Warning | Added by this phase; collapses the permission prompt for the most direct execution vector. Code review raised it as WR-02. **Owner decision taken 2026-09-24: KEEP** — its marginal exposure is comparable to the pre-existing `Bash(git *)` (line 13), and removing it would break the pipeline's own inline `node -e` calls. **Re-checked 2026-09-25: still present.** Registered as an accepted trust-boundary choice, not an open gap |
| `.claude/settings.local.json` | 17-21 | Session-scoped probe grants (`P=… && echo … sed …`, `sed -n '/function autoResolve/…'`) | ℹ️ Info | One-off investigative grants recorded by this phase; no exposure beyond read-only inspection |
| `frontend/app.js` / `frontend/index.html` / `frontend/style.css` / `scripts/check-05-ui-uat.py` / `scripts/check-07-idi08-validation.py` | — | `TBD` / `FIXME` / `XXX` | — | **None found** (re-scanned 2026-09-25, per file). Debt-marker gate clean |
| `frontend/app.js` | 1354 | Comment enumerates call sites and explicitly drops the numeral ("要核数用 grep 现算") | ℹ️ Info | The stale-prose failure mode was pre-empted rather than repeated (IN-04 from review was fixed this way) |

### Known Gate-Honesty Items (carried, not new)

Re-measured 2026-09-25. These are registered debt from the milestone audit §7 / backlog `999.2`, not
Phase 8 defects; none blocks this phase's goal.

1. **`check-05` item 10 SC4 uses a fixed 12-Tab window** (`_IDI07_TAB_LIMIT = 12`, `check-05:1849`,
   used at `:3000` / `:3208`) rather than a window tied to the actual stop count. Item 10's **census**
   assertion uses an adaptive window (`len(data) + 8`, `check-05:2945`) and is the assertion that
   actually carries the A11Y-02 / A11Y-08 coverage claim — it passes with 「未覆盖 []」. Registered in
   the frontmatter `advisory:` list.
2. **`check-05` L-5 / L-6 labels are broader than their measurement** (L-5 now exempts one row per the
   2026-09-24 ruling; L-6 judges visible rows only). Both are disclosed in-line in the `actual` field
   and per-row `info()`, so this is honest narrowing rather than a hidden gap.
3. **`check-07` g1's 「零决定」 wording reads as absolute** while measuring a delta
   (`len(posts) == posts_before`). Cosmetic; the measurement itself is correct.
4. **CLOSED 2026-09-25 — the milestone audit §7 「*(no gate)*」 row.** The audit registered that the CSS
   `:focus-visible` enumeration was never compared to the harness's `FOCUSABLE_SELECTOR`, so narrowing
   the constant would silently shrink item 10's judged set while the gate stayed green. Quick
   `260925-iin` FIX 5 added item 10's static guard ⑤, which compares the two **item by item, in order**,
   and now reports `对称差=[]`. **Re-run this pass: PASS.** The audit's last gate-honesty gap is closed.
5. **ROADMAP backlog `999.1`'s text is now stale** — it still describes `.collapse-indicator` as
   carrying `font-size: 20px; line-height: 1;` at `style.css:434`, which is false at HEAD (the rule at
   `style.css:686` consumes `var(--text-lg-plus)` / `var(--lh-none)`; both literals count 0). The
   closure is recorded in `idi-05-UI-SPEC.md` and the quick task's SUMMARY, not in ROADMAP.
   Informational only; `.planning/ROADMAP.md` is outside this pass's write scope.

### SUMMARY ↔ HEAD Disagreements (registered, not gaps)

1. **SUMMARY 03 §Newly discovered finding is stale.** It registers "Escape cannot dismiss the
   selection menu" as a phase-introduced defect, **not fixed**, with the recommended disposition left
   to the user. HEAD is past that: `62dfd3e` suppressed one keyup (incomplete), and `09b170d` replaced
   it with selection-identity dismissal (`dismissedSelectionRange` / `isDismissedSelectionLive`).
   **Re-run at HEAD**: `check-07 --item g3` shows the menu stays hidden across a second Escape, an
   `ArrowRight`, and a further Escape, with the mutation control proving the guard is load-bearing.
   HEAD wins; this is a disagreement, not a gap.
2. **SUMMARY 03's keyboard-path step 5** ("focus does return to `#round-doc`, but the menu does not
   stay dismissed") describes the pre-fix tree only. At HEAD the dismissal is durable (g3).
3. **Line anchors in the plans and SUMMARYs have drifted** (plan 01's fence comments +24 lines, plan
   02's comments/attributes further; and, within this report's own earlier version,
   `syncBackgroundInert`'s 5th call site, the `clearInlineError();` sites past line 640, the
   `showInlineError` anchor and the Escape dispatcher's extent). HEAD's element positions are the
   authority; every claim above was re-anchored by id/selector/verbatim string at HEAD `0b6283a`.
4. **SUMMARY 03's close-out claim "All plan-level gates are green"** (line 322) was true only for the
   gate set it ran (items 1 / 4 / 10 + check-01…04) and false for the ROADMAP Gate line "Phase 4/6/7
   全部 gate 仍通过" — item 9 was never re-run. This one *was* the gap (`resolved_gaps[0]`). **It is no
   longer a disagreement**: item 9 was re-run this pass and reads `PASS (17 条断言, 0 FAIL, 0 BLOCKED)`.
5. **Archive-path mechanism misattribution (SUMMARY 03 §Deviation 1)** — the archive round-switch does
   not travel through `updateFrozenPresentation`; it routes to `loadArchiveRoundDoc` (`app.js:1300`),
   which touches neither the `.hidden` class nor the `disabled` flag. **Re-confirmed first-hand at
   HEAD**: the acceptance criterion still holds (truth 29), only the attributed mechanism is wrong.
   Registered, not a gap.

### Human Verification Required

The five items below are unchanged in character from the 2026-09-24 report and remain **human**. They
are not machine proxies and were not substituted. All five were adjudicated `pass` by the user in
`idi-08-UAT.md` (2026-09-24, `status: complete`, 5/5) — that adjudication is what the frontmatter's
canonical `status: passed` rests on, and it is why the verifier determination (`human_needed`) and the
canonical status differ.

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

**Item 6 of the 2026-09-24 pass ("the L-5 gate adjudication") is closed** — the user ruled on
2026-09-24 and the resolution shipped in `63fba08`, re-measured this pass. It is no longer a human item.

Per the ROADMAP Phase 8 §Manual checks rule: an automated non-result on the keyboard-origin selection
legs is a **harness limitation, not a defect**. No automated FAIL was recorded on any of them.

### Gap Resolution

**The one gap is closed, and this pass re-measured its outcome first-hand.**

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

**Independence of this resolution — stated plainly, and updated.** The resolution was authored by the
orchestrator under explicit user authorization after two delegated `gsd-verifier` attempts stalled at
the 600s watchdog. So the gap-closure *evidence* is **first-party in origin**, and the two mutation
experiments (rows 38–39) remain so: **this pass did not re-run them** (that would require editing
`scripts/check-05-ui-uat.py`, which was out of scope). What this pass *did* do independently is re-run
`--item 9` and read the fail-closed branch in the source, so the resolution's **outcome** now has an
independent pass even though its mutation proofs do not.

**Registered costs (not tidied away).** See the frontmatter's `resolved_gaps.registered_costs` for the
full text. In short: the amendment's invalidation of four sibling fingerprints was **discharged** by
their 2026-09-25 re-verifications, and quick `260925-iin`'s wider blast radius (all six phases) is
registered there too.

Separately, and independent of the gap: the keyboard-origin selection legs (A11Y-08, A11Y-03's
selection half, REG-03's keyboard-dependent items) remain human, as the ROADMAP §Manual checks
requires — an automated FAIL there is a harness limitation, not a defect, and none was recorded here.
The `Bash(node -e ' *)` grant this phase added to `.claude/settings.local.json` is a real security
finding; the repository owner reviewed it on 2026-09-24 and chose to **keep** it as a trust-boundary
decision (its marginal exposure is comparable to the pre-existing `Bash(git *)` grant, and removing
it would break the pipeline's own inline `node -e` calls). Re-checked 2026-09-25: still present.
Registered, not a gap.

---

### Post-Close-Out Re-verification (2026-09-24T15:31:21Z, HEAD `ad43f64`)

*Preserved verbatim in substance. Its 「4 phases」 count was correct for the set it named and is
superseded by the milestone-wide picture in §重验证披露 and in the frontmatter's registered costs.*

**Why this section exists.** After the UAT pass and the three `verify:post` steps, the UI review's
priority finding 1 was adjudicated by the owner and fixed in quick task `260924-vb7`
(commits `5fcc7dd` test, `40e8de9` fix, `f483eef` docs, `cf60e4e` harness corrections). That fix
changed `frontend/app.js` — a `covered_files` member — so this report went **`stale` by content
change**, not by a bookkeeping omission. Refreshing the digest without re-establishing the
conclusions would assert "nothing changed since verification", which is false. The report is
therefore re-established here against HEAD.

**SELF-VERIFIED — NOT INDEPENDENT.** `gsd-verifier` was not re-run: it stalled twice (600s watchdog)
on this phase during the previous round and produced nothing, and the owner explicitly authorized
the orchestrator to re-verify first-party again rather than repeat that. Treat rows 38–40 and this
section as *asserted by the author of the change* rather than *confirmed by a third party*. Rows 1–37
are carried forward unchanged from the independent pass; the fix does not touch any of their subject
matter, and every gate they rest on was re-run (below).

**What changed, and what it means for the report.**

| Item | Before | After |
|------|--------|-------|
| `frontend/app.js` | pre-fix | `chooseTier()` now hands focus back to `#btn-continue-check` |
| `scripts/check-07-idi08-validation.py` | not in `covered_files` | **added** — it is now the primary evidence for the A11Y-05 / A11Y-06 / A11Y-03-Escape / tier-focus truths, exactly as `check-05` is for A11Y-01/02/08 |
| `idi-08-UI-SPEC.md` | not in `covered_files` | **still not** — the original report did not cover spec docs, and that scope is not silently widened here; its D8-10 amendment is recorded in the quick task's SUMMARY instead |
| `covered_digest` | `v1:sha256:fc089060…b0a91` | `v1:sha256:f2c2e3e5…67bde` |
| Score | 34/39 (2 self) | **35/40 (3 self)** |

**Gates re-run on HEAD `ad43f64`** (all green; these are the same instruments the independent pass used):
pytest **219 passed, 6 skipped**; check-01 PASS; check-02 `PASS: 0 failures` (ORDER 0.363); check-03 PASS;
check-04 PASS; `check-05 --browser bundled` 9/10 PASS with item 5 BLOCKED (2 AI-smoke legs, opt-in) —
exit 2 by design; check-06 g1–g6 PASS; check-07 g1 21 / g2 39 / g3 10 / g4 3, exit 0 (14 consecutive
green runs); probe-07 ring composite **3.45** ≥ 3.0; `node --check frontend/app.js` OK.

**The new truth (row 40), and why its evidence is adequate.** The defect was reproduced before the
fix (`FAIL g4 … actual=BODY`), the fix turns it green (`actual=btn-continue-check`), and a
discriminating control proves the green is not vacuous — with the focus call neutralized the same
real path yields `actual=BODY` again. The placement is **measured rather than assumed**: the call
sits after `await refreshChecksAfterStream()` because that refresh is what clears
`continueCheckBtn.disabled`, and `.focus()` on a disabled button is a silent no-op — the failure mode
that would have made the diff look correct while leaving the defect live. The harness records
`BLOCKED` (never `PASS`) if the button is not focusable at hand-back time, so a no-op cannot ship
looking green. **This pass re-ran g4 first-hand**, so row 40 is now independently verified including
its discriminating control.

**Two harness defects found and fixed while re-establishing this** (registered, not hidden):
`g4`'s "已隐藏" assertion logged the **inverse** of its own meaning (a PASS printing
`expected=hidden=true actual=hidden=False`), and `_settle_cli_check()` did not actually close the
`/api/cli-check` race it was written for — it waited for one response plus ~150ms of stability, which
a **second** in-flight round trip can outlive. That is the source of the intermittent red the executor
hit on `g1 [#cli-check-overlay] Escape 后仍可见`. Both are fixed in `cf60e4e`; the helper now gates on
zero in-flight round trips **and** a 600ms stable window. **This pass ran `check-07` three times at
HEAD with identical green results**, so the fix continues to hold.

**Residual, stated plainly.** Four truths remain HUMAN and one remains
present-but-behavior-unverified — unchanged by this re-verification, and unchanged in character:
the keyboard-origin selection legs cannot be automated in this environment, and the ROADMAP
§Manual checks explicitly forbids reading an automated non-result there as a defect. The
`Bash(node -e ' *)` grant remains a registered owner-accepted trust-boundary decision.

---

### 重验证披露(2026-09-25T09:31:45Z,HEAD `0b6283a`)— 内容真变后的重验证,非记账性刷新

**Why this section exists.** After the 2026-09-24 re-verification at `ad43f64`, quick task `260925-iin`
landed nine commits (`ed20ca6`…`0b6283a`) closing the milestone audit's one blocking finding and
backlog `999.1`. That task changed **two** of this report's `covered_files` members — `frontend/app.js`
and `scripts/check-05-ui-uat.py` — so the report went **`stale` by content change**. Recomputing the
digest alone would assert "nothing changed since verification", which is false. The conclusions are
therefore re-established below, first-hand.

**SELF-VERIFIED vs INDEPENDENT — the distinction is preserved, not laundered.** This pass was performed
by an independent verification agent, not by the author of the code under verification. That upgrades
what can honestly be upgraded and nothing more:

- **Rows 1–31 and 37**: carried forward from the earlier passes, and this pass **re-ran every gate they
  rest on** (check-01…04, check-05 items 1/2/3/4/6/7/8/9/10, check-06, check-07 g1–g4, probe-07,
  pytest, `node --check`). Their evidence rows above now cite the re-run.
- **Row 40** (tier focus hand-back): **now fully independent**, including the discriminating control
  that proves the green is not vacuous — the earlier pass could only self-verify it.
- **Rows 38–39** (the two L-5 mutation experiments): **remain self-verified in origin.** This pass did
  not re-run them — doing so requires editing `scripts/check-05-ui-uat.py`, which was explicitly out of
  scope. Their *mechanisms* were re-confirmed by reading the source (`_is_content_region` fails closed;
  `if not asserted: blocked(...)`). The earlier rows' 「(self)」 labels are therefore **kept**, not
  upgraded.
- **Row 37's resolution** (the L-5 gate amendment shipped in `63fba08`): its **outcome** is now
  independently re-measured; its mutation proofs remain self-verified, exactly as §Gap Resolution says.

**What changed, and what it means for the report.**

| Item | Before | After |
|------|--------|-------|
| `frontend/app.js:253` (`renderEvent`) | `eventsEl.scrollTop = eventsEl.scrollHeight;` (a no-op once Phase 6's L-4 removed `.event-list`'s overflow — the milestone audit's §5 blocking finding) | `item.scrollIntoView({ block: 'nearest' });` — restores auto-follow on the outer `#main-pane` |
| `scripts/check-05-ui-uat.py` | 16 assertions in item 9; 41 in item 10; a stale `--color-text-muted` diagnostic | 17 / 42; diagnostic corrected; **plus** a new static guard ⑤ tying `FOCUSABLE_SELECTOR` to the CSS `:focus-visible` enumeration |
| `frontend/style.css` | byte-identical to the phase base (`95cb22ee…`) | `3ce1565a…` — an 8th type tier (`--text-lg-plus: 20px`) + `--lh-none: 1`; `.collapse-indicator` re-pointed at both (backlog `999.1` item 1) |
| `covered_files` | included `.planning/REQUIREMENTS.md` | **that line removed** (user ruling, 2026-09-25) |
| `covered_digest` | `v1:sha256:f2c2e3e5…67bde` | `v1:sha256:9742bcd1…6f6e5` |
| Score | 35/40 (3 self) | **35/40 (2 self, 1 upgraded to independent)** |
| `verified:` | `2026-09-24T15:52:00Z` (mislabelled local time) | `2026-09-25T09:31:45Z` (correct UTC) |

**Is the change disjoint from this phase's deliverables? Yes — and here is the proof, not an
assumption.** `git diff ad43f64..HEAD -- frontend/app.js` is **exactly one line, inside `renderEvent()`**
(`numstat`: `1 1`). `renderEvent` is the AI event-stream renderer; it is not on any path this phase
touched:

| Phase 8 deliverable | Where it lives | Relation to the changed line |
|---|---|---|
| Escape single-point dispatcher | `app.js:1564-1619` | disjoint — different function |
| `hideSelectionMenu` F1-a/b/c hand-back | `app.js:1348-1377` | disjoint |
| Shift-release submit listener | `app.js:1477-1490` | disjoint |
| `syncBackgroundInert()` + 5 call sites | `app.js:521-526`; 495/501/674/840/1611 | disjoint |
| `#tier-modal` focus-on-open + flag reset | `app.js:671-680`, `:1610` | disjoint |
| F1-d hand-back (confirm / tier) | `app.js:1600`, `:847` | `chooseTier()` **does** call `renderEvent` (error/say paths), but `scrollIntoView` does not move focus, and `continueCheckBtn.focus()` runs afterwards — **re-measured green** by `check-07 --item g4`, including its discriminating control |
| S8-1 empty-state copy | `app.js:1167` | disjoint |
| `#round-doc` `tabindex` + ring | `index.html:163`; `style.css:1519-1528` | disjoint — `index.html` is byte-unchanged by the quick task, and the ring rule is untouched |
| Background `inert` derivation | `app.js:521-526` | disjoint |

**Which truths are therefore unaffected because the change is disjoint, and which were re-measured
anyway.** Truths 1–4, 6–13, 15–29, 31 are **unaffected by construction** (the changed line is not on
their call path) — but none was left on that argument alone: every one was re-measured by re-running
its gate at HEAD, and the re-run evidence is what the table above cites. Truths 5, 30 and the artifact
rows were **re-measured** because their evidence is tree-level. Truth 14's substantive property was
**re-measured directly** (`overflow-wrap: anywhere` present; `#doc-panel-body` padding unchanged).
No truth changed status.

**One evidence line that no longer holds at HEAD — disclosed, not absorbed.** Truth 14's and truth 30's
original evidence said `frontend/style.css` was byte-identical at the phase base and HEAD
(`95cb22ee…`). That was true at `ad43f64` and is **false at HEAD**: quick `260925-iin` FIX 1 edited the
file (backlog `999.1` item 1), so `HEAD:frontend/style.css` = `3ce1565a…`. The claims were therefore
re-scoped to what they were always for — **this phase introduced zero CSS bytes** — which is directly
measurable and still true (`4976bee:frontend/style.css` == `ad43f64:frontend/style.css` == `95cb22ee…`).
`frontend/style.css` is **not** in this report's `covered_files` (a scope decision from the original
report, which this pass was instructed not to widen), so the drift is disclosed here rather than
recorded as a covered-file invalidation. The quick task that made the edit was independently verified
(`260925-iin-VERIFICATION.md`, `status: passed`) and closes a backlog item, not a Phase 8 deliverable.

**The `covered_files` change (user decision, 2026-09-25).** `.planning/REQUIREMENTS.md` was removed from
this report's `covered_files`, and `covered_digest` was recomputed over the remaining **10** files with
the positional-argument form
(`gsd-tools query verification.fingerprint .planning/phases/idi-08-… <file1> … <file10> --raw` →
`v1:sha256:9742bcd1d572f80abf6eb2d5e2f43b6c1d6c0ab10b018fe2577173a11006f6e5`; re-run for determinism,
identical).

**Why.** `covered_files` means *inputs whose change invalidates this report's conclusions*. The
requirements index table is **downstream bookkeeping**: `phase.complete` flips its rows, and the
milestone close **deletes the file** (`git rm .planning/REQUIREMENTS.md`). While it was listed, every
phase completion and the milestone close silently invalidated every report that listed it — for a
reason unrelated to whether any conclusion still held. The observation was raised by the
`idi-04.1-radix` verifier and adopted by the user for all six v1.14 phase reports; this report is the
sixth and last to apply it. **No other report's `covered_files` was changed by this pass**, and this
report's list was not widened beyond that single removal.

**Blast radius of quick `260925-iin`, registered in full.** The quick task changed `frontend/app.js`,
`scripts/check-05-ui-uat.py`, `frontend/style.css`, `04-UI-SPEC.md` and `idi-05-UI-SPEC.md` — so it
invalidated **all six** v1.14 phase fingerprints: idi-04 (`style.css` + `04-UI-SPEC.md`),
idi-04.1-radix / idi-05 / idi-06 / idi-07 (`style.css` + `check-05`), idi-08 (`app.js` + `check-05`).
**All five siblings were re-verified on 2026-09-25** (`idi-04` 08:01:44Z, `idi-04.1-radix` 08:18:03Z,
`idi-05` 08:36:09Z, `idi-06` 08:52:23Z, `idi-07` 09:11:00Z) — all `status: passed`, each with
`REQUIREMENTS.md` removed from `covered_files`. **idi-08 is the sixth, and this pass is its
re-establishment.** The earlier prescription 「correct closure is re-running those phases' verify-work」
is therefore **discharged**, not outstanding.

**New coverage won in this round, registered as a closure.** Quick `260925-iin` FIX 5 closed the
milestone audit's §7 「*(no gate)*」 finding: the CSS `:focus-visible` enumeration is now mechanically
compared, item by item and in order, against the harness's `FOCUSABLE_SELECTOR`, so narrowing either
side can no longer shrink item 10's judged set silently. Re-run this pass:
`INFO item10 [static] FOCUSABLE_SELECTOR ↔ :focus-visible: CSS 侧(规则块起始行=1519)= ['button','input','select','textarea','a[href]','summary','[tabindex]']; Python 侧(常量定义行=1751)= [同]; 对称差=[]`
→ `PASS`. Item 10 is now **42** assertions (was 41); item 9 is **17** (was 16).

**Gates re-run on HEAD `0b6283a`** — every line below is verbatim output from this pass:

| Gate | Result |
|------|--------|
| `.venv/bin/python -m pytest -q` | **219 passed, 6 skipped, 1 warning in 6.57s** |
| `node --check frontend/app.js` | **OK** |
| `bash scripts/check-01-token-conformance.sh` | **PASS** |
| `.venv/bin/python scripts/check-02-contrast.py` | **PASS: 0 failures** (ORDER 0.363) |
| `bash scripts/check-03-hidden-uniqueness.sh` | **PASS** |
| `bash scripts/check-04-important-count.sh` | **PASS** |
| `.venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled` | **PASS (17 条断言, 0 FAIL, 0 BLOCKED)**, exit 0 |
| `.venv/bin/python scripts/check-05-ui-uat.py --item 10 --browser bundled` | **PASS (42 条断言, 0 FAIL, 0 BLOCKED)**, exit 0 |
| `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` (full) | items 1/2/3/4/6/7/8/9/10 **PASS**; item 5 **BLOCKED** (2 AI-smoke legs, opt-in); **exit 2 by design** |
| `.venv/bin/python scripts/check-06-idi05-validation.py` | g1–g6 **PASS** (9/2/12/5/5/7), exit 0 |
| `.venv/bin/python scripts/check-07-idi08-validation.py` | g1 **21** / g2 **39** / g3 **10** / g4 **3**, all PASS, **exit 0** (run 3× this pass, identical) |
| `.venv/bin/python scripts/probe-07-focus-composite.py` | exit 0; ring composite **3.45 ≥ 3.0** |
| `grep -c '^\.hidden {' frontend/style.css` | **1** |
| `grep -o '!important;' frontend/style.css \| wc -l` | **1** (the `grep -c '!important'` = **5** trap was NOT used as a criterion) |
| `grep -c '@layer'` / `grep -c '@property'` / `grep -E 'var\(--[a-z0-9-]+,'` | **0 / 0 / 0** |
| `grep -c tabindex frontend/index.html` | **1** |
| `grep -v '^#' frontend/style.css \| grep -c ':focus-visible'` | **9** |
| `grep -c 'inline-error' frontend/style.css` | **1** |
| `grep -c 'clearInlineError();' frontend/app.js` | **9** |
| `grep -o 'id="[^"]*"' frontend/index.html \| wc -l` | **82** |
| `ls frontend/vendor/` | `marked.min.js` (exactly one) |

**Hard-rule status at HEAD (all seven hold jointly).**

1. `grep -c '^\.hidden {' frontend/style.css` → **1**. ✓
2. `!important` **declarations** → **1** (`grep -o '!important;' | wc -l`). `grep -c '!important'` returns
   **5**; the four extras are comment prose. ✓
3. Append-not-reorder: this pass added no CSS and moved no rule; the phase's own commit range changed
   zero CSS bytes. The quick task's style.css edit appended two tokens and re-pointed one existing
   rule in place — verified independently in its own report. ✓
4. `@layer` → none; `@property` → none; `var(--x, <fallback>)` → none. ✓
5. Do-not-touch list intact at HEAD: `.fatal` distinguishable; `applyArchiveView`'s two read-only lines
   untouched (`app.js:875-876`); `#selection-menu` still a direct `<body>` child (`index.html:249`);
   `showInlineError` `textContent`-only (`app.js:317-324`); `renderAnnotations` (`app.js:1162-1174`) and
   `renderVerdictCard` not edited by quick `260925-iin` (the app.js diff is one line in `renderEvent`);
   the ~70 top-level `getElementById` handles are **71** with **zero renames or deletions**
   (`index.html` byte-unchanged by the quick task). ✓
6. Zero new runtime dependencies, zero build steps; `frontend/vendor/` = `marked.min.js` only. ✓
7. Runtime verification: check-05/06/07 are browser-driven (Playwright bundled chromium); every
   `style.css` plan carries runtime probes. ✓

**Independence summary for a reader in a hurry.** Rows 1–31 and 37: originally independent, and
re-measured this pass. Row 40: originally self-verified, **now independent**. Rows 38–39: **still
self-verified in origin** — kept labelled as such. The five human items: adjudicated by the user in
`idi-08-UAT.md`, retained as human. No `passed` verdict was preserved on a stale conclusion; the one
evidence line that stopped holding at HEAD (style.css byte-identity) is disclosed above rather than
quietly refreshed.

---

_Verified: 2026-09-25T09:31:45Z (re-established at HEAD `0b6283a`; see §重验证披露 — this stamp replaced the mislabelled `2026-09-24T15:52:00Z`)_
_Re-verified: 2026-09-24T13:23:27Z (gap-closure portion self-verified by the orchestrator, under explicit user authorization)_
_Re-verified: 2026-09-24T15:31:21Z (post-close-out re-verification at HEAD `ad43f64`; rows 38–40 and §Post-Close-Out Re-verification self-verified, under explicit user authorization)_
_Verifier: [CL] (gsd-verifier, first pass) · [CL] orchestrator (gap resolution + post-close-out re-verification, both self-verified) · [CL] (gsd-verifier, 2026-09-25 re-establishment — independent; rows 38–39's mutation proofs remain self-verified in origin)_

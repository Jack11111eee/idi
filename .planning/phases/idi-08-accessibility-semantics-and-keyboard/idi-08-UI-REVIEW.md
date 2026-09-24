# Phase 8 (idi-08) — UI Review

**Audited:** 2026-09-24
**Baseline:** `idi-08-UI-SPEC.md` (approved 2026-09-23; the phase's own interaction/state contract)
**Screenshots:** not captured — headless rendering is blocked in this environment (resident `/api/events` SSE stream prevents the capture handler from terminating; UI-SPEC §Provenance records this as an environment fact, not a choice). Audit is **code + measured-evidence only**.
**Scope note:** this is an accessibility/keyboard phase whose visible surface is deliberately tiny. The audit does **not** treat the user-ruled scope lock (D-11 / D-17 / D-18 / D-19, focus traps, full ARIA, `window.prompt` replacement) as a defect. Two of the three priority fixes below are **edge paths inside the phase's own new contract**, not scope complaints.

---

## Pillar Scores

| Pillar | Score | Key Finding |
|--------|-------|-------------|
| 1. Copywriting | 3/4 | S8-1 landed as exactly one word and every frozen string matches verbatim — but the string this phase edited still names the **mouse** gesture (`划词`) on the empty state that the new keyboard path lands on. |
| 2. Visuals | 3/4 | The whole-box ring is delivered zero-CSS and measured discernible — but in the phase-5 state the newly-added Tab stop is a **351 × 0** box, so the ring renders as a degenerate line (registered, adjudicated, unfixed). |
| 3. Color | 4/4 | Zero color delta; `check-02` `PASS: 0 failures` (47 pairs, ORDER 0.363); no hardcoded color added anywhere in the diff. |
| 4. Typography | 4/4 | Zero typography delta; no `font-size` / `font-weight` / `line-height` declaration added in the entire phase diff. |
| 5. Spacing | 4/4 | Zero spacing delta; `frontend/style.css` is byte-identical to the phase start (`git diff f0f0c31..HEAD -- frontend/style.css` empty). |
| 6. Experience Design | 3/4 | Strong derived-inert + single-point dispatcher + mutation-tested guards — but **two edge paths breach the phase's own F1 invariant / `aria-modal` claim**, and the baseline UI-SPEC no longer describes HEAD. |

**Overall: 21/24**

---

## Top 3 Priority Fixes

1. **Focus falls to `<body>` after a *successful* tier choice — an F1 breach the contract never carved out** — `chooseTier()` hides `#tier-modal` and calls `syncBackgroundInert()` (`frontend/app.js:839-840`) but moves focus nowhere; the focused `#btn-tier-loose` is now `display:none`, so `document.activeElement` collapses to `<body>` (measured by the phase's own probe B17: `activeElement == 'BODY'`, recorded in `idi-08-02-SUMMARY.md` §Known Gaps). Impact: the keyboard user loses their position immediately after the exact interaction D-11 called 「真正的卡死」, and `#btn-continue-check` ("继续自检" — the visible next action) is right there to receive it. **Concrete fix:** add `continueCheckBtn.focus();` after `syncBackgroundInert()` at `frontend/app.js:840` (mirrors the Escape branch at `:1607`). The justification the contract gives for *not* handing back — F1 不覆盖情形①, "the whole view is about to switch so the trigger will hide" — **does not transfer**: after a tier choice the view does not switch away, and the target (`#btn-continue-check`) becomes *visible* at `app.js:668`. If the owner prefers the current behaviour, the alternative is to register it as F1 exception ③ in `idi-08-UI-SPEC.md` §焦点契约, because D8-10 currently reads "两个弹窗关闭后把焦点交还触发者" without exception.

2. **`#selection-menu` escapes `inert` and paints *above* an open dialog (z 200 > z 100) — the UI-SPEC's mutual-exclusivity premise is false for `#confirmation-modal`** — `idi-08-UI-SPEC.md` §M-1.3 justifies leaving the menu outside `#app` with 「两者同时可见的场景不存在,判据是结构性的」, reasoning only about `#tier-modal` (phase5). But `#confirmation-modal` opens in **phase 3** — precisely the state where the menu lives (`app.js:1423`). Nothing hides the menu on modal open: `openConfirmModal()` (`app.js:490-497`) does not call it, and there is no `blur` / `focusout` / `selectionchange` closer anywhere (`grep` = 0 hits). Repro by code reading: keyboard-select in the round doc → menu visible with focus in it → Tab past it (it is the last tabbable before the hidden overlays, `index.html:249`) → Tab back to `#btn-authorize` → Enter. The dialog opens, `#app` becomes inert, and the **still-visible menu is a sibling of `#app`** (`index.html:179` closes `#app`, `:249` holds the menu) so it is never inerted; its buttons sit *after* `#btn-confirm-cancel` in DOM order (`index.html:215` → `:249`), so one Tab from 「拒绝」 lands outside the dialog — on an element painted over it (`--z-selection-menu: 200` vs `--z-overlay: 100`, `style.css:355-356`). This is the exact 「宣告一个实现并不兑现的契约」 class the phase was built to avoid. **Concrete fix:** call `hideSelectionMenu();` inside `openConfirmModal()` before `syncBackgroundInert()` (one line, and the mouse path already gets this for free via the document `mousedown` closer at `app.js:1486-1490`), then correct the §M-1.3 premise. Not reproduced in a browser in this audit (no browser available) — mechanism is from source reading only.

3. **The audit baseline no longer describes HEAD — four post-hoc behaviours and one new file are unregistered in `idi-08-UI-SPEC.md`** — a downstream reader auditing against the contract will read these as unauthorized deviations:
   - the Shift listener has a **4th** predicate (`document.activeElement !== roundDoc`, `app.js:1479`) where §K-2.2 specifies three conjuncts;
   - `isDismissedSelectionLive()` + `dismissedSelectionRange` (`app.js:1381-1395`, `:1450-1453`) — the durable Escape-dismissal mechanism (fixes `62dfd3e` / `09b170d`) — appear nowhere in §M-2.1's dispatcher listing;
   - `if (e.isComposing) return;` (`app.js:1574`) is not in the contract;
   - `scripts/check-07-idi08-validation.py` (**+773 lines, a new file**) falsifies the three "零新增文件" claims at `idi-08-UI-SPEC.md:27 / :96 / :735`.
   All four code changes are *improvements* and are fenced in-code; the defect is that the contract — the thing this review is scored against — was never amended. **Concrete fix:** append an 「执行后修正登记」 block to the UI-SPEC in the same style as A-10 / A-11 (which were handled correctly), covering these four items and the `check-07` file.

---

## Detailed Findings

### Pillar 1: Copywriting (3/4)

**Contract met, verified verbatim.**

| UI-SPEC Copywriting Contract row | Actual | Verdict |
|---|---|---|
| S8-1: `在左侧文档` → `在右侧文档` (one word) | `frontend/app.js:1162` = `本轮暂无批注——在右侧文档划词即可批注。`; `grep -c '在左侧文档'` = 0 | exact |
| Historical round empty state `该轮暂无批注。` | `frontend/app.js:1164` byte-identical | intact |
| 划词菜单项 `批注` / `用大白话讲这段` | `index.html:250-251` | intact |
| 弹窗标题 (= accessible name) `授权确认` / `选择自检档位` | `index.html:209` / `:228`, each referenced by `aria-labelledby` | intact, single source of truth |
| `宽松` / `严格`, `放行` / `拒绝`, `授权撰写总设计文档` | `index.html:231-232`, `:214-215`, `:167` | intact |
| 断流横幅 (both states) | `app.js:180` / `:182` | intact |
| Inline error via `showInlineError` — `textContent`-only | unchanged; no `innerHTML` introduced in the phase diff | intact (T-260916-01 holds) |

No generic labels (`确定` / `OK` / `提交` / `Submit` / `Click Here`) anywhere in `index.html`.

**Finding (justifies 3/4) — the edited string still names the mouse gesture, on the state the new keyboard path reaches.** `app.js:1162` now reads 「本轮暂无批注——在**右侧**文档**划词**即可批注。」 The phase fixed the direction word but left the gesture word pointing at a mouse drag, in the phase-3 empty state — which is exactly the state a keyboard user sees after the new Tab stop (`index.html:163`) and the Shift-release gesture put them there. D-19 deliberately declined to add a discoverability hint, so this line is the *only* instructional copy on the path and it describes the wrong input device. **Fix:** `…在右侧文档划词(或用 Shift+方向键选中)即可批注。` — but note this is a copy change the contract froze, so it needs an S8-3-style sign-off, not a silent edit.

**Registered, not scored:** D-19's known limitation (nothing tells a keyboard user Shift+Arrow selects text; the focus ring is the only signal) — explicitly ruled out of scope and honestly registered by the phase itself.

### Pillar 2: Visuals (3/4)

**The one visible addition is delivered correctly.** `frontend/index.html:163` carries `tabindex="0"`; `frontend/style.css:1508-1517`'s seven-selector enumeration includes `[tabindex]:focus-visible` (`:1514`) with `outline: 2px solid var(--color-focus)` / `outline-offset: 2px`, and `--color-focus: #1f63bd` (`style.css:259`) is pre-declared. Zero new `:focus` rules — `grep -c ':focus-visible'` = **9** (unchanged). Ring readings recorded by the phase: `2px / rgb(31, 99, 189)` at Tab position **2** (immediately after `#round-switcher`, immediately before `#btn-authorize` — §K-1.7's contract), horizontal clearance **36px** vs the 4px the ring needs, contrast **5.57:1** against the panel and **5.72:1** against the page.

**Finding (justifies 3/4) — the ring degenerates to a line on the phase-5 Tab stop.** In `phase5_checking`, `applyPhase5View` empties the element (`app.js:629`), so `#round-doc` measures **351 × 0** and is nevertheless the **first** Tab stop in that state, reading `outline-width: 2px, outline-color: rgb(31, 99, 189), focusVisible: true`. A "whole-box ring" on a zero-height box has no box: the user sees a thin horizontal rule and cannot tell what they focused. This stop is **new in this phase** (before `tabindex="0"` the element was not focusable). It is registered (`idi-08-03-SUMMARY.md` §Deviation 2) and adjudicated acceptable in `idi-08-UAT.md` item 5 — the deduction is for the unfixed degenerate rendering, not for the owner's decision. **Fix if the owner revisits it:** mount the attribute conditionally (it is dead weight in phase 5), or suppress the ring when the element has zero height.

**Registered residual (not scored):** at the app's default scroll position the ring's bottom edge is clipped **3.64px** by `#doc-panel`'s scroll boundary (a 4px scroll clears it). Owner ruled 「可辨」 on 2026-09-24 with 5.57:1 measured; the contract's own criterion (any segment clipped ∨ < 3:1 ∨ cannot locate focus) is met on the first clause but not on the second or third, and the ruling is recorded — accepted, not re-litigated here.

### Pillar 3: Color (4/4)

- `frontend/style.css` byte-identical to the phase start (`git diff f0f0c31..HEAD -- frontend/style.css` → empty); zero new tokens, `:root` untouched.
- `python3 scripts/check-02-contrast.py` → `PASS: 0 failures` (47 pairs; `ORDER 0.363`). All three `--color-focus` PAIRs unchanged.
- No hardcoded color added: `git diff … -- frontend/ | grep '^+' | grep -E '#[0-9a-fA-F]{6}|rgb\(|hsl\('` → 0 hits.
- Accent distribution unchanged: no new element consumes `--color-action-primary`; the ring uses `--color-focus`, already declared and already consumed (`style.css:259` / `:1515`) — no hard-rule-5 issue.
- **Residual note (informational):** under the archive `.archive-mode` 0.75 composite the ring reads **3.45:1** — above SC 1.4.11's 3:1 non-text floor but with only 15% headroom. `probe-07-focus-composite.py` re-ran clean with both self-witness counts (`links-before=0` / `links-after=1 (mutation-applied=yes)`), so the number is trustworthy, not a silent spin.

### Pillar 4: Typography (4/4)

- `frontend/style.css` byte-identical → the `idi-05` contract (7 sizes / 3 weights / 4 line heights) is untouched by construction.
- No `font-size` / `font-weight` / `line-height` declaration added anywhere in the phase diff (verified over `f0f0c31..HEAD`).
- `#round-doc` keeps `.markdown-body` (`style.css:891-894`) with no new class or inline style: `git diff … | grep '^+.*style="'` → 0 hits.
- The two modal `<h3>`s keep their existing `--text-xl` role; `aria-labelledby` points at them rather than duplicating a string, so the accessible name cannot drift from the on-screen title.

### Pillar 5: Spacing (4/4)

- `frontend/style.css` byte-identical → the `04-UI-SPEC` 12-step scale is untouched; **zero** new spacing literals, zero arbitrary values.
- The phase's geometric premise (`#doc-panel-body { padding: 32px 40px }`, `style.css:657`) is unchanged — which is what makes the ring's horizontal clearance argument valid.
- No spacing declaration added in `app.js` / `index.html`; the only inline styles in the file remain the pre-existing `#selection-menu` positioning math (`app.js:1413-1414`), untouched by this phase (hard rule 5 / Pitfall 8).
- `#round-doc`'s box width is unchanged at 351px; the ring draws outside the border box into the parent's 40px padding, so it consumes no layout space (outline is not in flow).

### Pillar 6: Experience Design (3/4)

**What the phase got right (and how it is proven):**

| Mechanism | Evidence |
|---|---|
| Dialog semantics on both blocking overlays | `index.html:207` / `:226` carry `role="dialog" aria-modal="true" aria-labelledby=…`; `grep -c 'role='` = 2, `aria-modal` = 2, `aria-labelledby` = 2 |
| The announcement is *made true* | `syncBackgroundInert()` (`app.js:521-526`) derives one `inert` attribute from the two modals' `.hidden` state at 6 sites (1 def + 5 calls); mounted on `#app` only, and all five `.overlay`s + `#selection-menu` are `#app`'s siblings (`index.html:179`) |
| Escape, single point, declared priority | one `document` keydown listener (`app.js:1570-1614`); `grep -c "key !== 'Escape'"` = 1; z-order table (menu 200 → confirmation 100 → tier 100) rather than source-order |
| Dismissal is durable, not one keyup | `isDismissedSelectionLive()` (`app.js:1381-1395`) keyed on **selection identity**, not key identity — the D-06-compliant shape, since `handleSelectionTrigger` stays byte-identical |
| Focus never rests on a hidden element | `hideSelectionMenu()` (`app.js:1342-1372`) takes `selectionMenu.contains(document.activeElement)` **before** `classList.add('hidden')` (`:1353` precedes `:1369`) — the ordering is load-bearing and correct |
| Tier dead-state removed | `tierModalShown = false` on Escape (`app.js:1605`) so the next `refreshChecksAfterStream` re-opens it |
| Escape closes with zero decisions | `closeConfirmModal()` only (`app.js:1594`); no `window.prompt`, no POST, no annotation — machine-asserted in plan 02 (A9/A10/A11/A12) |
| Behavioural (not text-matching) coverage | `scripts/check-07-idi08-validation.py` (new) asserts g1/g2/g3 in a real browser **with mutation controls** — including "remove the dismissal guard and the same keyup re-opens the menu" |

`check-01` / `check-02` / `check-03` / `check-04` all re-run **PASS** on the close-out tree; `node --check frontend/app.js` OK; `grep -c '^\.hidden {'` = 1; `frontend/vendor/` = exactly `marked.min.js`.

**Findings justifying 3/4:**

1. **F1 breach on the tier success path** — priority fix #1 above. `app.js:839-840` hides the modal with no hand-back; probe B17 measured `activeElement == 'BODY'`. `idi-08-UI-SPEC.md:731` (D8-10) says 「两个弹窗关闭后把焦点交还触发者」 and only references exception ① (which is written for `#confirmation-modal`'s 放行). Either the code or the ledger must move.
2. **`aria-modal` is not true in a reachable state** — priority fix #2 above. `#selection-menu` is outside the inert scope and above the dialog in z-order; the §M-1.3 exclusivity argument covers only `#tier-modal`. The machine coverage has the same hole: `check-07` g2 asserts "8 Tabs never land inside `#app`" with a modal open, but not "no focusable element outside the dialog remains reachable".
3. **Baseline drift** — priority fix #3 above.

**Deliberately not scored (user-ruled, correctly registered):** `#permission-modal`'s silent appearance (D-17 → v2 `A11Y-V2-02`); focus traps (v2 `A11Y-V2-01`); the three non-responding overlays' Escape scope lock (D-11 — deliberate, and machine-asserted in check-07 g1 with a discriminating control); `#round-doc`'s missing `role`/`aria-label` (D-18); the discoverability gap (D-19); `window.prompt` (v2 `FLOW-V2-01`); no `aria-live` anywhere (Pitfall M7 honoured — `grep` shows none added).

**Registered residual (not scored):** `#tier-modal`'s escape hatch is invisible — Escape closes it and resets the flag, but the modal still presents as a forced binary choice with no 「取消」 affordance and no copy mentioning Escape. Adding a hint would be a new UI element outside the declared deliverable list, so this is recorded as a residual, not a defect.

---

## Minor Recommendations (7)

1. `app.js:1162` — add the keyboard gesture to the empty-state line (needs sign-off; the copy is contract-frozen).
2. `index.html:163` — consider mounting `tabindex="0"` conditionally, or suppressing the ring on the zero-height phase-5 box.
3. `idi-08-UI-SPEC.md:27 / :96 / :735` — the "零新增文件" claim is false on HEAD (`scripts/check-07-idi08-validation.py`, +773).
4. `idi-08-UI-SPEC.md` §Copywriting Contract still anchors S8-1 at `app.js:1121`; HEAD is `app.js:1162` (registered in `idi-08-03-SUMMARY.md`, not in the contract).
5. `check-05 --item 10` hardcodes `p1` / `checking` / `p3` and the CLI has no `--state` flag, so the **archive**-state ring is uncovered — a real coverage hole in the phase's own headline gate, honestly registered by the executor.
6. `.claude/settings.local.json:23` — the `Bash(node -e ' *)` grant added this phase pre-approves arbitrary JS execution. Not a UI finding, surfaced because it sits in this phase's diff and the owner's WR-02 decision was "surface, don't change".
7. `#tier-modal` — Escape works but nothing on screen says so.

**Registry audit:** not applicable — no `components.json`, no `package.json`, no shadcn, no third-party registry, no design-system package (DESIGN.md D-06 forbids frameworks and build steps). Section omitted per the audit rules.

---

## Files Audited

- `frontend/index.html` (269 lines — full read; `#round-doc:163`, ARIA triples at `:207` / `:226`, new ids at `:209` / `:228`, `#selection-menu:249`)
- `frontend/app.js` (1849 lines — full read of every phase-touched region: `:90`, `:490-526`, `:671-681`, `:827-846`, `:1162`, `:1342-1395`, `:1450-1483`, `:1570-1614`)
- `frontend/style.css` (1697 lines — enumeration `:1508-1517`, `--color-focus:259`, z-scale `:350-356`, `.overlay:800-808`, `#selection-menu:1209-1211`; byte-identical to phase start)
- `scripts/check-07-idi08-validation.py` (new, 773 lines — header, assertion map, mutation controls)
- `scripts/check-05-ui-uat.py` (+48, the authorized S8-2 L-5 change)
- Phase artifacts: `idi-08-UI-SPEC.md`, `08-CONTEXT.md`, `idi-08-0{1,2,3}-PLAN.md`, `idi-08-0{1,2,3}-SUMMARY.md`, `idi-08-REVIEW.md`, `idi-08-UAT.md`
- Guards re-run: `check-01` PASS · `check-02` PASS 0 failures (ORDER 0.363) · `check-03` PASS · `check-04` PASS · `node --check frontend/app.js` OK
- Static counts re-measured on HEAD: `tabindex` (html/js) 1/0 · `:focus-visible` 9 · `role=` 2 · `aria-modal` 2 · `aria-labelledby` 2 · `id="` 82 · `inert` (js) 2 · `^\.hidden {` 1 · `inline-error` 1 · `clearInlineError();` 9 · `vendor/` = 1 file

**Not performed (environment):** browser screenshots, computed-style readings, and `check-05` / `check-07` execution — headless rendering is blocked and this session has no browser driver. All runtime numbers quoted above are the phase's own recorded measurements, cited to their source file; findings #2 (Pillar 6) and the reachability trace in priority fix #2 are **source-reading only** and are labelled as such.

---

## Orchestrator Verification Addendum (2026-09-24)

The audit above was conducted source-reading-only. Three priority fixes were therefore re-verified against the running application before being accepted. **One is disproven, one is upheld as a contract-level question (not a code defect), one is upheld as documentation drift.**

### Priority fix #2 — `#selection-menu` escaping `inert` and painting above an open dialog → **DISPROVEN (false positive)**

The claim's premise was that nothing hides the menu when `#confirmation-modal` opens, so the menu remains visible above the dialog and one Tab from 「拒绝」 reaches it. Measured against the live app (`scripts/probe-menu-modal-reachability.py`, real mouse drag then a real click):

```
STEP 1: _drag_select -> {'menuHidden': False, 'selLen': 12, 'collapsed': False}
STEP 2: 拖拽后 菜单可见=True  选区长度=12          ← premise established: the menu IS open
STEP 3: 点击 #btn-authorize
STEP 4: 确认弹窗可见=True  菜单可见=False  #app.inert=True  activeElement=confirm-word-input
```

The menu is **already hidden** by the time the dialog is visible, and focus is correctly inside it.

Two facts the source-reading pass missed:

1. **`openConfirmModal()` has exactly one call site** — `frontend/app.js:559`, inside `#btn-authorize`'s `click` handler. The claim that the menu survives into the dialog requires a path that opens the dialog while the menu is up; there is none.
2. **A document-level `mousedown` handler already closes the menu on any outside click** (`frontend/app.js:1489-1493`: `if (selectionMenu.contains(e.target)) return; hideSelectionMenu();`). `mousedown` precedes `click`, so clicking `#btn-authorize` dismisses the menu before `openConfirmModal()` runs. The z-index observation (`--z-selection-menu: 200 > --z-overlay: 100`) and the sibling relationship (`#app` at `index.html:10` vs `#selection-menu` at `:249`) are both *correct* — they are simply not reachable as a defect, because the menu is never up at that moment. Re-opening it while the dialog is open is also impossible: `#round-doc` lives inside `#app`, which is `inert`.

**No code change is warranted.** The probe is retained so this finding's resolution stays reproducible if the `mousedown` closer is ever removed — that handler is the load-bearing reason the claim does not hold.

### Priority fix #1 — focus falls to `<body>` after a successful tier choice → **UPHELD, but as a contract question, not a code defect**

Confirmed on source: `chooseTier()` (`frontend/app.js:839-840`) hides `#tier-modal` and calls `syncBackgroundInert()` with no `.focus()`, and `refreshChecksAfterStream()` contains no `focus()` either — so focus collapses to `<body>`.

**However, the code matches its plan.** `idi-08-02-SUMMARY.md:295` records this explicitly and deliberately:

> **After a successful tier choice, focus lands on `<body>`** (probe B17: `activeElement == 'BODY'`). This is per plan — A-8 scopes the hand-back to the Escape branches and states the success path must not hand back — and is recorded here as a measured consequence rather than as a defect, so a later reader does not file it as an oversight.

So this is not an implementation deviation. The real issue is in the **contract**, and the review states it correctly: D8-10's carve-out is justified by 「F1 不覆盖情形①」, whose rationale ("the whole view is about to switch") is written for `#confirmation-modal`'s 放行 path and **does not transfer** to the tier success path — where the view does not switch away and `#btn-continue-check` ("继续自检") becomes visible, which is precisely the 「继续自检流程」 D8-10's own rationale names.

**This is an owner decision, not a defect to patch**: either add `continueCheckBtn.focus();` after `app.js:840`, or register the tier success path as an explicit F1 exception ③ in `idi-08-UI-SPEC.md`. Both are legitimate; they differ in which artifact moves. **No implementation file was modified by this audit** — a code change here needs its own GSD flow.

### Priority fix #3 — the audit baseline has drifted from HEAD → **UPHELD**

Confirmed: the Shift listener's 4th predicate (`app.js:1479`), `isDismissedSelectionLive()` (`app.js:1381-1395`), the `e.isComposing` guard (`app.js:1574`), and the new `scripts/check-07-idi08-validation.py` are all absent from `idi-08-UI-SPEC.md`, and the three 「零新增文件」 claims in that spec are now false. This is documentation drift, not a behavioural defect — all four are fenced improvements. It is a consequence of the audit-time Nyquist work (`check-07` did not exist when the UI-SPEC was written), so amending the spec is a follow-up rather than a gap in the phase's delivery.


# Phase idi-07 — UI Review

**Audited:** 2026-09-23
**Baseline:** abstract 6-pillar standards (no `UI-SPEC.md` exists for this phase; `07-CONTEXT.md` + `DESIGN.md` v1.14 used as the contract of record)
**Screenshots:** not captured — no browser tooling in this session, and the project's own documented environment fact is that screenshots are unavailable (headless capture blocked by the SSE long connection). All runtime evidence below comes from computed-style readings: `.venv/bin/python scripts/check-05-ui-uat.py --item 10` → **`item 10: PASS (41 条断言, 0 FAIL, 0 BLOCKED)`**, exit 0, plus `check-01/02/03/04` all PASS.
**Phase nature:** declarative CSS only. `frontend/app.js`, `frontend/index.html`, `frontend/vendor/`, `scripts/ui-states/` are byte-unchanged (`git diff --numstat 69dea49 HEAD` on those paths is empty). The phase's diff on `frontend/style.css` is 354 added / 4 deleted; the only non-additive edit is the `button:hover` selector rewrite now at `style.css:741`.

---

## Pillar Scores

| Pillar | Score | Key Finding |
|--------|-------|-------------|
| 1. Copywriting | 3/4 | Zero copy added by the phase; the one gap is that `#btn-process-round`'s disabled rationale lives only in a mouse-only `title` while the other two disabled controls got adjacent hint paragraphs. |
| 2. Visuals | 2/4 | The focus ring is excellent and fully verified, but the interaction-state language covers buttons/inputs/selects only: `#session-panel .panel-header` shows `cursor: pointer` with no click behavior, and `.annotation-answer summary` — a `cursor: pointer` control Phase 6's own A11Y-07 gate counts as interactive — has no hover/active feedback at all. |
| 3. Color | 3/4 | No bare hex or bare `rgba()` outside the token fence (0/0); but the focus ring's PAIR manifest enumerates 3 grounds while focusable elements render on a 4th (amber-1), and that omission is silent — the sibling `--color-border-hover` token got exactly that ground added in `7b4ae18`. |
| 4. Typography | 4/4 | No-surface score: the phase added zero `font-size`/`font-weight`/`font-family` declarations (verified against the phase diff). The 7 sizes / 3 weights in the file are the signed-off Phase 5 scale. |
| 5. Spacing | 4/4 | No-surface score: the phase added zero `padding`/`margin`/`gap` declarations and zero arbitrary values; the one spacing-adjacent literal (ring geometry) is off-scale by documented precedent and its `CLEARANCE_MIN_PX` binding now has a mechanical guard. |
| 6. Experience Design | 3/4 | State coverage is thorough and mutation-tested, but `summary` sits in `FOCUSABLE_SELECTOR` with no sample that renders one (so its census coverage is nominal and the gap is unregistered), and `#btn-authorize:disabled`'s `opacity` remains machine-unread. |

**Overall: 19/24**

---

## Top 3 Priority Fixes

1. **`#session-panel .panel-header` advertises a click that does not exist** — `frontend/style.css:665` gives every `.panel-header` `cursor: pointer` and `user-select: none`; only `#ai-panel-header` and `#doc-panel-header` have click listeners (`app.js:1561`, `app.js:1567`). The file's own convention resets the cursor for the two non-collapsible headers (`#annotations-panel .panel-header { cursor: default }` at `style.css:1085`, `#checks-panel .panel-header { cursor: default }` at `style.css:1304`) — `#session-panel` was simply missed. **Impact:** the active panel's heading shows a hand cursor, carries the active-panel blue marker bar, and does nothing on click; `user-select: none` also blocks selecting the heading text. **Fix:** add `#session-panel .panel-header { cursor: default; }` alongside the two existing resets (one declaration, mirrors the established pattern), or bind the collapse handler for it.

2. **`.annotation-answer summary` is an interactive control with no interaction states and no runtime coverage** — `style.css:1189-1196` gives it `cursor: pointer` and the Phase 6 A11Y-07-mandated 24×24 hit area (i.e. the project already counts it as an interactive element), and `style.css:1513` gives it a focus ring, but there is **no** `summary:hover` / `summary:active` rule anywhere in the file, and it is absent from the 120ms transition mount rule (`style.css:1675`). Worse, no sample renders one: all five `scripts/ui-states/` fixtures contain only `.md` files (no `annotations.json`), so `item 10`'s census enumerates 28 elements per sample and never sees a `summary`. **Impact:** the phase-3 annotation-flow disclosure control — the flagship interaction of that phase — gives a mouse user zero hover/press feedback, and a future regression in `summary:focus-visible` would be invisible to the gate. **Fix:** extend the plain-button hover group's selector list (or add a `summary:not(:disabled):hover` / `:active` pair) and either add an `annotations.json` to the `p3` fixture or register the gap explicitly, as D-18 already does for the `a[href]` half.

3. **The focus ring's PAIR manifest silently omits a ground where focusable elements actually render** — `style.css:500-506` states three verification surfaces (`--color-surface-page`, `--color-surface`, `--color-surface@0.75`). But `.verdict-card` (`style.css:1341`, ground `--color-surface-warning-subtle` = amber-1) hosts the dynamically built `.verdict-note-input` and two `.verdict-buttons button` — real, visible, focusable elements in the `checking` sample (confirmed by `item 10`'s own readings: `#idi07-verdict-probe .verdict-note-input` and `#idi07-verdict-probe .verdict-buttons button` were both measured). The ring on that ground is **5.77:1** (measured, ≥3, so no contrast failure) — this is a coverage and consistency defect, not a legibility one. **Impact:** the manifest's own doctrine ("enumerate the combinations that actually render"; its docstring exists so that "drift must be visible") is unmet for the phase's headline token, on precisely the ground where the app creates focusable elements at runtime. **Fix:** add `/* PAIR --color-focus ON --color-surface-warning-subtle NON-TEXT */` and extend the group comment at `style.css:500-506`.

---

## Detailed Findings

### Pillar 1: Copywriting (3/4)

The phase added **no user-facing copy** — its entire diff is CSS declarations, comments, and test-harness code. Audited anyway, against the interaction-state affordances the phase made load-bearing.

**What is good (negative evidence, specific):**
- No generic labels. Every `<button>` in `frontend/index.html` carries a specific, contextual label: `发送` (L23), `继续自检` (L49), `继续修复` (L51), `发起测试调用` (L72), `处理本轮批注` (L73), `中止` (L74), `进入` (L96), `没想法?让 AI 发散出候选方向` (L109), `认可雏形` (L126), `授权撰写总设计文档` (L143), `撰写总设计文档` (L149), `同意`/`拒绝` (L163-164), `放行` (L177), `宽松`/`严格` with one-line descriptions (L189-190), `开始浏览归档` (L201), `批注`/`用大白话讲这段` (L208-209), `我已装好,重新检测` (L217).
- Empty states exist and are specific: `#chat-greeting` "说点什么,开始这次讨论。" (`index.html:19`), `.draft-empty` "尚无草稿——和 AI 讨论出实质进展后,它会写入 docs/draft.md。" (`index.html:115`).
- Error states exist and are specific: `第 ${n} 轮文档拉取失败。` (`app.js:878`), `轮次列表拉取失败(稍后操作会重试)。` (`app.js:1001`), `第 ${n} 轮文档拉取失败(该轮不存在或不完整)。` (`app.js:1029`), `授权失败:${data.message || resp.status}` (`app.js:542`), `授权请求失败(网络)` (`app.js:550`).
- `#authorize-hint` (`app.js:454`) explains the gate in plain language and satisfies the §3.8 language redline: "四处机械校验全部通过后按钮才会点亮(annotations 无待处理 + 未决清单清零 + 维度表全绿 + 授权标记为「是」)。"

**Finding — `#btn-process-round`'s disabled rationale is mouse-only.** `index.html:73` carries `disabled title="仅阶段 3 当前轮可用"` and has **no adjacent hint element**, unlike its two siblings: `#btn-approve-draft` has `#approve-hint` (`index.html:127`, text set at `app.js:416`) and `#btn-authorize` has `#authorize-hint` (`index.html:144`, text at `app.js:449/454`). A `title` tooltip is not reachable by keyboard or assistive tech, so for this one disabled control the "why is this unavailable" explanation exists only for mouse users. This matters more than usual here because the phase's D-07 gate made the disabled state the *sole* visual signal (zero hover feedback), so the verbal explanation carries the whole load.

### Pillar 2: Visuals (2/4)

The focus ring — the phase's headline visual artifact — is genuinely strong and I found no defect in it. The deduction is entirely about the *breadth* of the interaction-state visual language, which is the other half of the phase's stated goal ("给每个交互控件补上 hover / active / disabled 的可辨反馈").

**What is verified good (runtime, not eyeballed):**
- Ring geometry and color on real elements: `outline-width: 2px`, `outline-offset: 2px`, `outline-color: rgb(31, 99, 189)` (runtime-resolved `--color-focus`), `focusVisible: true`, measured on `#btn-ping`, `#check-switcher`, `#btn-process-round` across p1/checking/p3. Expected values are never hardcoded — the probe resolves the token at runtime.
- Mouse click does **not** draw the ring (`SC2`: post-click `outline-color` = `rgb(255, 255, 255)`, and the probe first proves the rule is live by Tab-focusing, then asserts `document.activeElement` is the clicked element — so the negative result cannot be a no-op).
- Ring is not clipped at the scroll bottom: 11 measured clearance rows, all ≥ 4px (40 / 129.5 / 130 / 252), with the scroll premise made genuinely true by first growing the containers through the app's own render path (`#main-pane` [1740, 2640, 900], `#doc-panel` [4348, 5248, 900]).
- Filled buttons: hover keeps `background-color` (`rgb(13, 116, 206)`) and adds `box-shadow: inset 0 0 0 999px rgba(0,0,0,0.06)`; press switches to `0.12`; the "press ≠ hover" half is asserted and was mutation-proven in plan 02.
- Plain buttons: `rgb(249,249,249) → rgb(240,240,240) → rgb(232,232,232)` (gray-2 → gray-3 → gray-4), with press ≠ hover asserted.
- Disabled: `.verdict-buttons button` hover background == resting (`rgb(249,249,249)`), `opacity` still `0.5` — the D-07 gate is real and verified.

**Finding 2a — misleading affordance on `#session-panel .panel-header` (BLOCKER-class defect, see Top Fix 1).** `cursor: pointer` + `user-select: none` on a heading with no click listener and no `.collapse-indicator`. The file's own convention is to reset this (two resets exist at L1085 and L1304); `#session-panel` is an inconsistency, not a design choice. It is also the panel that carries the active-panel blue marker (`style.css:1418-1426`), so it looks maximally clickable.

**Finding 2b — `<summary>` has no hover/active affordance (see Top Fix 2).** `cursor: pointer` + 24×24 hit area + focus ring, but no `:hover` and no `:active` rule, and it is excluded from the 120ms transition mount rule. Mouse users get no feedback on the annotation-flow disclosure control.

**Finding 2c — registered timing asymmetry between button families.** Filled buttons change instantly on hover/press (`box-shadow` is deliberately excluded from the transition list, D-08 cost ② / D-14) while plain buttons and inputs animate over 120ms. This is registered and deliberate (the `opacity` alternative broke AA on three color families: 4.77 → 3.93, 5.21 → 4.42, 4.72 → 3.81). I am reporting it as a **registered** inconsistency, not a defect — but two button families on the same screen do respond at visibly different speeds.

**Finding 2d — no author styling for `a[href]` at all.** The phase added `a[href]:focus-visible` to the ring enumeration (`style.css:1512`), so a focused markdown link gets a `#1f63bd` ring drawn around text that the design system does not own — Chrome's UA default `#0000EE`. That puts three near-neighbour blues on one screen (`#0000EE` UA link, `#1f63bd` ring, `#0d74ce` primary fill). Contrast is not the issue (`#0000EE` on white is ~15:1); coherence is. Marked `needs_human_review` — see below.

### Pillar 3: Color (3/4)

**Discipline holds where it is mechanically guarded:**
- Bare hex outside the token fence: **0**. Bare `rgba(` outside the fence: **0**. `check-01-token-conformance.sh` PASS. (The phase earned the second number: it hoisted both alphas into `--color-overlay-hover` / `--color-overlay-active` at `style.css:282-283` rather than writing literals in rule bodies, because `check-01` does *not* count bare `rgba()` and that invariant had no mechanical guard before.)
- `--color-focus` is consumed exactly once (`outline: 2px solid var(--color-focus)`), and each of the four new interaction tokens is declared once and consumed exactly once — the "declared with its consumer" discipline is intact and machine-asserted.
- No accent overuse: `--color-focus` appears 5 times in the file (1 declaration + 3 PAIR comments + 1 consumption); `--color-action-primary` 15; `--color-marker-active` 5.
- `--color-focus: #1f63bd` is a documented, deliberate off-Radix value with the sign-off arithmetic and the rejected alternatives (`blue-11` at 3.03 under the 0.75 composite, `blue-12` reading as a border) recorded at `style.css:238-259`. Correctly **not** flagged as a defect.

**Finding — the ring's ground set is incomplete and the omission is silent (see Top Fix 3).** Measured ratios for the ring on every ground where a focusable element can actually render:

| Ground | Ratio vs `#1f63bd` | In manifest? |
|---|---|---|
| `--color-surface-page` (gray-1 `#fcfcfc`) | 5.72 | yes |
| `--color-surface` (gray-2 `#f9f9f9`) | 5.57 | yes |
| `--color-surface@0.75` (archive composite) | 3.45 | yes |
| `--color-surface-warning-subtle` (amber-1 `#fefdfb` — `.verdict-card` L1341, `#brainstorm-view` L954) | 5.77 | **no** |
| `--color-surface-streaming` (blue-2 `#f4faff` — `.event-list.streaming` L758) | 5.58 | **no** |
| `--color-surface-danger` (red-2 `#fff7f7` — `.event-list.aborted` L759) | 5.56 | **no** |
| `--color-surface-sunken` (gray-3 `#f0f0f0`) | 5.15 | no — but the comment at `style.css:504-505` justifies this, and the justification holds (only `.markdown-body code` L919 and `.badge-answered` L1158, neither focusable) |

None fails 3:1, so this is not a contrast defect. It is an **asymmetry in the delivered artifact**: the same commit range added `--color-border-hover ON --color-surface-warning-subtle` (`style.css:536`) after the code review established that `.verdict-card` is a real ground for a token drawn there — while the ring, drawn on that same ground by the same dynamically created element, was left at three. The manifest measures only the grounds it names, and `style.css:527-533` shows the file already knows how to record such a limit explicitly; the ring's group does not.

### Pillar 4: Typography (4/4)

**This is a no-surface score, not an endorsement of the type scale.** Verified against the phase diff: `git diff 69dea49 HEAD -- frontend/style.css | grep -E '^[+-].*(font-size|font-weight|font-family)'` returns **nothing**. The phase added no type declarations, so it can neither help nor hurt this pillar.

For completeness, the file's current distribution: 7 distinct `--text-*` sizes (`xs`, `base`, `md`, `lg`, `xl`, `2xl`, `3xl`) and 3 `--fw-*` weights (`regular`, `medium`, `semibold`). That is above the abstract "≤4 sizes / ≤2 weights" heuristic, but the heuristic is the wrong yardstick here: this is the Phase 5 signed-off type contract (12/14/16/18/22/24/28, D-06/D-07), already independently verified, and the fourth weight (700) was deliberately eliminated. One raw literal exists — `.collapse-indicator { font-size: 20px; line-height: 1 }` at `style.css:678` — and it is registered backlog item `999.1`, explicitly forbidden to touch by `05-CONTEXT D-23` and by this phase's own CONTEXT. Penalising this phase for it would point the reader at the wrong actor.

### Pillar 5: Spacing (4/4)

**Also a no-surface score.** Verified against the phase diff: `git diff 69dea49 HEAD -- frontend/style.css | grep -E '^[+-].*(padding|margin|gap|space-)'` yields only two hits, both prose inside comments (a `margin of 0.03` figure and the word "gap" in the WR-02 disclosure) — **zero spacing declarations added**. Arbitrary-value search (`[Npx]` / `[Nrem]`): 0 hits.

The one spacing-adjacent decision is the ring's geometry, `2px` width + `2px` offset = 4px of outward extension. Those are intentionally off the spacing scale, matching the file's documented precedent for size literals (`min-height 160/200/52`, `min-width 96`, `height 36`, and the 24 that is the WCAG 2.5.8 constant). The binding to `CLEARANCE_MIN_PX = 4.0` is no longer prose: `scripts/check-05-ui-uat.py:1837-1838` defines `FOCUS_RING_WIDTH_PX` / `FOCUS_RING_OFFSET_PX` and SC1 asserts both halves on a real element — visible in the probe output as `PASS [p1] SC1 Tab 到 #btn-ping 的 outline-offset == 2px(= CLEARANCE_MIN_PX - 环宽)`. That closes the code review's WR-04.

Minor residual (harness, not UI): the label string `"(= CLEARANCE_MIN_PX - 环宽)"` at `check-05-ui-uat.py:2913` is a literal, so if `FOCUS_RING_OFFSET_PX` were ever changed to a value that no longer equals `CLEARANCE_MIN_PX - FOCUS_RING_WIDTH_PX`, the assertion would still pass while its own explanatory label became false. Not a UI issue; noted only because the file treats labels as part of the assertion.

### Pillar 6: Experience Design (3/4)

**State coverage is unusually thorough, and unusually well-evidenced:**
- *Focus* — complete: census judged sets of 9 / 8 / 9 elements across p1/checking/p3, uncovered count `[]` in all three; empty judged set routes to `blocked()` rather than a silent pass; disabled controls and `tabindex="-1"` are excluded and each exclusion is named with a real instance.
- *Hover* — filled buttons, plain buttons, inputs/selects all covered and measured.
- *Active* — filled buttons (0.12 overlay), plain buttons (gray-4), with `press ≠ hover` asserted (the half that a naive "== expected" assertion would miss).
- *Disabled* — 8 `:disabled` rules with `opacity` + `cursor: not-allowed`; zero hover feedback verified on a real `renderVerdictCard`-built button with a real `.disabled` toggle.
- *Reduced motion* — present, enumerated to include `.event-list`, and verified at runtime (`0s` on all four targets under `emulate_media(reduced_motion="reduce")`, then reset to `no-preference` without contaminating later items).
- *In-flight* — buttons are disabled during their requests (`app.js:1605` `pingBtn.disabled = true`, `app.js:748/769`, `app.js:1178`, `app.js:1504` with a 1500ms re-enable), so double-submit is prevented. No spinner/skeleton — correctly out of scope per REQUIREMENTS.
- *Error / empty* — see Pillar 1.

**Finding 6a — `summary`'s census coverage is nominal, and the gap is unregistered.** `FOCUSABLE_SELECTOR` (`check-05-ui-uat.py:1748`) is `"button, input, select, textarea, a[href], summary, [tabindex]"` and `style.css:1486-1492` promises this is "逐字同集" with the CSS rule and that "新增一类可聚焦元素要同时改两处". But `summary` and `a[href]` have no service object in any fixture (all five `scripts/ui-states/` samples contain only `.md` files; there is no `annotations.json`), so the census cannot exercise either. The `a[href]` half is registered and covered by a counterfactual probe (D-18, `scripts/probe-07-focus-composite.py`, `ratio=3.45`, injection proven 0 → 1). **The `summary` half is registered nowhere** — not in `07-CONTEXT.md`, not in the three plans, not in `idi-07-VERIFICATION.md`. Contrast with the negative spaces that *were* registered: `#selection-menu button`'s missing `:active`, `textarea`'s absence from the transition enumeration, `#round-doc`'s deferred ring.

**Finding 6b — `#btn-authorize:disabled`'s visual signal remains machine-unread.** Its `opacity: 0.55` (`style.css:1260`) has no assertion; the machine half (SC5′) covers a *different* rule, `.verdict-buttons button:disabled` (`style.css:1376`, `opacity: 0.5`). This is correctly registered as the phase's single human item (5″) and the verification report states plainly that "门绿不等于视觉上真的没被软化" — so it is **not** a defect of omission. It is recorded here because the core-value gate ("流程绝不进入撰写总设计文档 without explicit user authorization") rests on that one number, and a future edit to it would be caught by nothing.

**Finding 6c — two clickable headers are keyboard-unreachable.** `#ai-panel-header` and `#doc-panel-header` are click-to-collapse but are `<header>` elements with no `tabindex` and no keyboard handler, so the collapse feature has no keyboard path and no focus ring. This is a registered, explicit Phase 8 deferral (A11Y-02), so it is not this phase's contract breach — but it remains a live gap in the shipped UI, and it is why `[tabindex]:focus-visible` is a defensive (zero-service-object) selector today.

---

## Needs Human Review

These are perceptual claims I will not guess at. Each is marked `needs_human_review: true`.

| # | Claim to verify | Why a human must look | Evidence on disk |
|---|---|---|---|
| 1 | The focus ring stays legible as a *ring* when it surrounds a blue filled button (`#btn-send`, `button.primary`, `.overlay-card button`). | The ring is `2px` of `#1f63bd` separated from the button fill by a `2px` gap of page gray. WCAG 1.4.11 is satisfied against the adjacent ground (5.57:1), but the ring and the primary fill are only **1.23:1** apart in luminance, so the indicator may read as a halo of the button rather than as a separate focus marker. | `style.css:1515-1516` (geometry), `style.css:259` (`#1f63bd`), `--color-action-primary: #0d74ce` (`style.css:132`). Computed: `L(#1f63bd)=0.1289`, `L(#0d74ce)=0.1704` → 1.232:1. |
| 2 | The two button families' hover *speeds* do not read as a defect side by side (instant for filled via `box-shadow`, 120ms for plain via `background-color`). | Registered as deliberate (D-08 cost ②, D-14), and the `opacity` alternative genuinely broke AA — but whether the asymmetry is perceptible in the same viewport is a judgment about looking, not about numbers. | `style.css:1584` vs `style.css:1675`; measured `box-shadow` values in the item-10 output. |
| 3 | `#1f63bd` (ring) sitting near `#0d74ce` (primary fill) and Chrome's UA `#0000EE` (markdown links, no author rule exists) reads as one system rather than three blues. | Color-system coherence is a perceptual claim. The `#1f63bd` choice is a signed-off exception with recorded arithmetic, so this is not a "fix the token" question — it is "does the screen look coherent". | No `a` rule exists in `style.css`; `grep 'a:hover\|a:visited\|markdown-body a'` returns nothing. |
| 4 | `#btn-authorize`'s disabled state still reads as "obviously not clickable" (the phase's existing human item 5″). | Already named in `idi-07-VERIFICATION.md` as the phase's single human item; listed here so this review does not appear to have silently replaced it with the machine proxy. | `style.css:1260` (`opacity: 0.55`), `index.html:143`. |

---

## Registry Safety

Not applicable — `components.json` does not exist in this repository and no third-party shadcn registry is used. Registry audit skipped per protocol; no Registry Safety section is included.

---

## Files Audited

**Implemented artifact (this phase's edit surface):**
- `frontend/style.css` — focus ring rule (`1508-1517`), plain-button `:active` (`1519-1542`), filled-button hover group (`1544-1585`), filled-button active group (`1587-1604`), input/select hover group (`1606-1646`), transition mount rule (`1648-1675`), reduced-motion block (`1677-1697`); tokens `--color-focus` (`238-259`), `--color-surface-active` (`185-207`), `--color-border-hover` (`216-231`), `--color-overlay-hover`/`--color-overlay-active` (`265-283`); PAIR manifest (`399-540`); rewritten `button:hover` selector (`716-741`); `.event-list` (`748-759`); `.panel-header` (`665-678`), `#annotations-panel .panel-header` (`1085`), `#checks-panel .panel-header` (`1304`); `.annotation-answer summary` (`1189-1196`); `.verdict-card` / `.verdict-note-input` / `.verdict-buttons button:disabled` (`1336-1376`); `#selection-menu` (`1209-1224`); all 8 `:disabled` rules (`933`, `945`, `1206`, `1260`, `1272`, `1286`, `1330`, `1376`); active-panel marker (`1418-1426`)

**Markup and behaviour context (byte-unchanged by this phase, read for ground/affordance analysis):**
- `frontend/index.html` (all 227 lines — 21 static buttons, 4 inputs, 3 selects, 4 `disabled` attributes, `title` attributes)
- `frontend/app.js` (read-only: disabled-state toggles, panel-header click bindings at `1561`/`1567`, `renderVerdictCard`, `<summary>` creation at `1152`, `#authorize-hint` / `#approve-hint` copy)

**Contract and planning artifacts:**
- `DESIGN.md` (v1.14 — verified to contain **zero** mentions of hover / focus / transition / keyboard / disabled, confirming this phase establishes the interaction-state contract from zero)
- `.planning/phases/idi-07-interaction-states-and-focus/07-CONTEXT.md` (D-01…D-20)
- `idi-07-01-PLAN.md` / `idi-07-02-PLAN.md` / `idi-07-03-PLAN.md` and their three `SUMMARY.md` files
- `idi-07-VERIFICATION.md` (independent verification, `status: human_needed`, 8/9 + 1 named human item)
- `idi-07-REVIEW.md` (prior code review — WR-01…WR-04, IN-01…IN-04; all four fix commits `7b4ae18` / `774a79c` / `4d9cebd` / `8d08f38` verified present in the tree, with WR-03's gate fix confirmed at `style.css:1641`/`1643` and WR-04's `outline-offset` assertion confirmed in the item-10 output)

**Gates and probes re-run on HEAD for this review:**
- `scripts/check-01-token-conformance.sh` → PASS
- `scripts/check-02-contrast.py` → `PASS: 0 failures`, 54 `^PASS` lines (53 pairs + 1 ORDER; TEXT 35 / NON-TEXT 18)
- `scripts/check-03-hidden-uniqueness.sh` → PASS
- `scripts/check-04-important-count.sh` → PASS
- `scripts/check-05-ui-uat.py --item 10` → `item 10: PASS (41 条断言, 0 FAIL, 0 BLOCKED)`, exit 0
- `scripts/ui-states/` fixtures (p1 / p12 / p3 / checking / archive) — enumerated to confirm no fixture renders `<summary>` or `<a href>`

**Note on documentation drift (not a UI finding, recorded so it is not mistaken for one):** the three SUMMARYs describe the tree as it stood before the four code-review fix commits. `idi-07-03-SUMMARY.md` states the manifest is "52 对 + 1 条 ORDER" with `^PASS` = 53; HEAD has 53 pairs / 54 `^PASS` lines, because `7b4ae18` added the third `--color-border-hover` ground. `idi-07-VERIFICATION.md` already discloses this class of drift in its §B. No action needed for the UI; flagged only so the numbers in this review are not read as contradicting the SUMMARYs.

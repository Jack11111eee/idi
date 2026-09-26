# Phase 04.1 — UI Review

**Audited:** 2026-09-20
**Baseline:** `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` (Color + Contrast Verification) over `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` (everything else)
**Screenshots:** captured — `.planning/ui-reviews/idi-04.1-20260920-105951/` (20 PNGs; 5 disk states × 3 viewports + 4 modals + the chip probe). Directory is covered by `.planning/ui-reviews/.gitignore` (`git check-ignore` verified).
**Harness:** `.venv/bin/python scripts/check-05-ui-uat.py` → `0 FAIL`, `98 PASS`, `2 BLOCKED`, `exit=2` — item-by-item identical to the VERIFICATION.md P3.7 baseline. Exit 2 is by design (two AI-dependent smokes).
**Guards:** CHECK-01/02/03/04 all `PASS`, exit 0. CHECK-02 prints 43 pairs + `ORDER 0.363` + `PASS: 0 failures`.

---

## Pillar Scores

| Pillar | Score | Key Finding |
|--------|-------|-------------|
| 1. Copywriting | 4/4 | Zero generic labels; empty/error copy is specific and actionable. Phase changes zero copy — verified. |
| 2. Visuals | 3/4 | Filled `.danger` buttons render a **blue border on a red fill**; `#selection-menu` popup has no elevation. |
| 3. Color | 3/4 | Value layer is measurably correct and 100% tokenized, but the accent leaks onto the destructive border, and `mark` renders UA black, not `--color-text`. |
| 4. Typography | 3/4 | 5 token sizes + 3 weights, all consumed — but `20px` (`.collapse-indicator`) is an undeclared 6th size and `.hint` renders at two different sizes. |
| 5. Spacing | 4/4 | 12-step scale, zero arbitrary `[...]` values, zero bare px in any padding/margin/gap. |
| 6. Experience Design | 2/4 | **No keyboard focus indicator on any filled button** (UA ring measures 1.26:1 / 1.15:1) and **no hover feedback on any filled button** (measured identical to base). |

**Overall: 19/24**

---

## Top 3 Priority Fixes

1. **Destructive buttons inside overlay cards paint a blue border on a red fill** — `#btn-permission-deny` (拒绝) and `#btn-confirm-cancel` (拒绝) render `background: rgb(206,44,49)` with `border-top-color: rgb(13,116,206)`. A destructive confirmation is visually branded as the primary accent, which mis-signals the safe/default choice at the exact moment the user is asked to confirm an irreversible step (授权撰写总设计文档). Cascade cause: `.overlay-card button { border-color: var(--color-action-primary) }` (`frontend/style.css:549-555`) and `button.danger { border-color: var(--color-action-danger) }` (`:473`) are both (0,1,1); the later one wins, and `.overlay-card button.danger` (`:556-559`) overrides only `background`/`color`. **Fix:** append `border-color: var(--color-action-danger);` to the `.overlay-card button.danger` rule. One line, one declaration. Note this is a **4th** out-of-fence declaration change, beyond D-11's enumerated three — it needs the same kind of explicit record R-1/R-2/R-3 got.

2. **No keyboard focus indicator on any filled button** — there is no `:focus` / `:focus-visible` / `outline` rule anywhere in `frontend/style.css` (grep: 0 hits). Keyboard focus falls back to Chrome's UA ring `rgb(0,95,204)`, which against the new fills measures **1.26:1** on `--color-action-primary` `#0d74ce` and **1.15:1** on `--color-action-danger` `#ce2c31` (SC 2.4.11 wants ≥3:1 against adjacent colours). Measured on `#btn-send`, `.primary` and `.danger` after real `Tab` navigation. The phase moved the ground under the ring (V-4/V-5/V-6) and UI-SPEC carry-forward #8 defers the *token* to Phase 7 — but what ships today is an invisible focus ring on the app's primary action. **Fix:** declare `--color-focus` and a `:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px }` rule now, or accept and record it as a known Phase-7 blocker rather than an open deferral.

3. **No hover feedback on any filled button** — measured: `#btn-send` base `rgb(13,116,206)` → hover `rgb(13,116,206)` (identical); `#btn-permission-allow` and `#btn-permission-deny` likewise unchanged. Neutral buttons *do* respond (`#btn-enter` `#f9f9f9` → `#f0f0f0`, `#btn-abort` likewise). Cause: `button:hover` (`:472`, (0,1,1)) loses to `#chat-input-row button` (`:759`, (1,0,1)), `.overlay-card button` (`:549`, (0,1,1), later in source) and `button.primary` (`:777`, later in source). Compounding it, the hover affordance on the buttons that *do* respond got weaker: `--color-surface-hover` vs `--color-surface` is now **1.08:1** (`#f9f9f9`→`#f0f0f0`) where at HEAD it was **1.12:1** (`#ffffff`→`#f2f2f2`). **Fix:** add explicit `:hover` rules for `.primary` / `.danger` / `#chat-input-row button` (e.g. blue-12 / red-12 fills); the neutral case is fine as-is.

---

## Detailed Findings

### Pillar 1: Copywriting (4/4)

The phase changes zero copy (contract `## Copywriting Contract`), and the zero-diff gate on `frontend/app.js` + `frontend/index.html` confirms no string moved. Audited the existing strings anyway:

- **No generic labels.** Grep for `Submit|Click Here|OK|Cancel|Save|确定|提交|取消` in `frontend/index.html` returns nothing. The two `拒绝` buttons are specific to their modals' semantics.
- **Empty states are specific.** `app.js:1121` `'本轮暂无批注——在左侧文档划词即可批注。'` — names the cause *and* the remedy. `app.js:1123` `'该轮暂无批注。'`. `index.html:98` draft-empty copy explains what will happen next.
- **Error copy is honest and specific.** `app.js:550` `'授权请求失败(网络)'`; `app.js:1001` `'轮次列表拉取失败(稍后操作会重试)。'` — no "Something went wrong / try again".
- **Disabled-state reason is surfaced.** `index.html:143` `title="四处机械校验尚未全部通过"` plus the in-button label `授权撰写总设计文档`; `app.js:453` expands the title with the four check names.
- **Placeholders are concrete.** `index.html:95` `输入项目目录绝对路径(如 /Users/you/my-project)`.

No finding justifies a deduction.

### Pillar 2: Visuals (3/4)

- **Focal point per state is clear.** p1 centres the greeting + composer; p3 centres the annotation stream; checking centres the report card; archive centres the mission-complete card over a full-viewport backdrop. Verified visually across all 5 states × 3 viewports.
- **Icon-only controls: none.** All 21 buttons carry text labels. The only glyph is the `▾` collapse indicator (`style.css:434`), which is decorative and paired with a clickable header.
- **Hierarchy is carried by size + colour, per contract.** Measured: modal `h3` 24px/700, doc-panel `h2` 18px, `.panel-header h2` 14px/500, body 16px, `.hint` 14px/`--color-text-muted`.
- **Finding — the destructive/primary border collision (see Priority 1).** This is the single most visible defect in the shipped UI. In `modal-permission-modal.png` the 拒绝 button reads as a red pill with a blue outline; the 同意 button beside it is blue. Two adjacent buttons share a border colour while their fills differ, so the border stops distinguishing anything and starts contradicting the fill.
- **Finding — `#selection-menu` has no elevation.** Computed `box-shadow: none` (`style.css:887-896`) while it is `position: absolute; z-index: var(--z-selection-menu)` = 200 and floats over the document text. `.overlay-card` has `--shadow-overlay`; the other floating layer has nothing, so a popup that overlays body text reads flat and can be mistaken for inline content at a glance.
- **Observation (not scored) — the page/panel ground delta is 3/255.** `--color-surface-page` `#fcfcfc` vs `--color-surface` `#f9f9f9`. Verified by decoding screenshot pixels: under the modal backdrop the two grounds measure `(138,138,138)` and `(137,137,137)` — exactly `0.55 × #fcfcfc` and `0.55 × #f9f9f9`, so the layer is wired correctly. But the 04.1-N-7 claim that the panel now "reads as a distinct surface" is delivered almost entirely by the 1px `#d9d9d9` `border-left`, not by the fill. Recorded as V-4/V-7-intended; flagging only so the claim is not read as stronger than it measures.

### Pillar 3: Color (3/4)

**The value layer itself is correct and I verified it independently, not from the SUMMARY.**

- **CHECK-02 is the arbiter and it is green.** All 43 pairs `PASS`, `ORDER 0.363`, `PASS: 0 failures`, exit 0. Every ratio reproduces the UI-SPEC `### The measured table` verbatim, including the two thin ones: `--color-text-info ON --color-surface-info` = **4.53** and `--color-border-strong` = **3.24 / 3.15**.
- **Zero bare colour literals outside the fence.** `awk 'NR>224' frontend/style.css | grep -cE '#[0-9a-fA-F]{3,8}'` = 0; `grep -cE 'rgba?\(|hsla?\('` outside the fence = 0. **Zero hardcoded colours in `frontend/app.js` (count 0) and `frontend/index.html` (count 0)** — the token fence really is the single source of truth at runtime.
- **Accent budget measured, not eyeballed.** Area-weighted over the 1440×900 viewport: page ground (`#fcfcfc`) ≈ 60%, panel + card ground (`#f9f9f9`) ≈ 32%, control ground (`#ffffff`) ≈ 4.3%, accent fills (`#0d74ce` / amber / green) each < 0.7%. Accent is a small fraction, well inside the 10% ceiling — no overuse.
- **Accent inventory matches the declared element list.** `--color-action-primary` `#0d74ce` appears on exactly the declared consumers: `#btn-send`, `#btn-permission-allow`, `#btn-confirm-authorize`, `#btn-tier-loose`, `#btn-tier-strict`, `#btn-mission-close`, `#cli-recheck-btn`, `#state-badge` (border + text) — **plus the two undeclared `.danger` borders** (Priority 1). `--color-action-warning` `#4f3422` appears on `#pending-count`, `#check-state`, `#stream-banner`, `#btn-divergence`, `#brainstorm-view h2` — the declared amber entry. `--color-action-danger` `#ce2c31` on `#btn-abort`, `#btn-permission-deny`, `#btn-confirm-cancel`, `#confirm-error`, `.inline-error`, `.kind-error .event-content`. Green on the six gate/loop buttons plus `.overlay-card` (mission-complete, 2px border) — the two named non-action consumers.
- **Finding — the blue border on the red fill** (Priority 1). `#btn-permission-deny` and `#btn-confirm-cancel`: `background rgb(206,44,49)` / `border-top-color rgb(13,116,206)`. Not documented anywhere in `04-UI-SPEC.md` or `idi-04.1-UI-SPEC.md`; `04-UI-SPEC.md:458` names `.overlay-card button` as a `--color-action-primary` consumer but never notices it also paints the `.danger` border.
- **Finding — `mark` renders `#000000`, not `--color-text`.** Measured inside the real `#round-doc`: `background: rgb(255,247,194)` (amber-3 ✓) but `color: rgb(0,0,0)`. `style.css:905-910` sets only `background`; the foreground comes from the UA `mark { color: marktext }` rule, which beats inheritance. So the rendered ratio is **19.34:1**, while `--color-text` on that ground is **15.00:1** and the number the E16 backstop cites (**15.88**) is `--color-text on --color-surface-page`. Three different numbers for one element. This is new evidence for W-4 / H-2 — I am not re-litigating the disposition, but the attribution cannot be resolved by adding the pair alone: the pair would still describe a colour the element does not use.
- **Finding — `--color-surface-hover` got weaker.** `#f9f9f9` → `#f0f0f0` = **1.08:1** vs HEAD's `#ffffff` → `#f2f2f2` = **1.12:1**. N-4 argues gray-3 is "what makes `button:hover` perceptible"; it is measurable that the new pair is ~30% less of a delta than the one it replaced. `--color-surface-hover` has exactly one consumer (`button:hover`, `style.css:472`) and D-16 established that no text reads on it, so this is purely an affordance-strength question.
- **Accepted, not a finding:** `--color-text-info` on `--color-surface-info` = 4.53, a 0.03 margin — contract-acknowledged at 04.1-N-3, passes the checker's closed-interval rule, and the "safer" alternatives are both explicitly rejected with arithmetic.

### Pillar 4: Typography (3/4)

- **Token discipline is good.** Declared: 12/14/16/18/24px (`--text-xs` … `--text-xl`), weights 400/500/600, four line-heights. Consumption: `--text-base` ×19, `--text-xs` ×7, `--text-md` ×7, `--text-xl` ×3, `--text-lg` ×2. Weights: `--fw-semibold` ×12, `--fw-medium` ×4, `--fw-regular` ×1. Five sizes and three weights — exactly the abstract ceiling.
- **Finding — an undeclared 6th size.** `style.css:434` `.collapse-indicator { font-size: 20px; }` — a bare literal outside the 5-step scale. Pre-existing (not touched by this phase; R5/P1.13 confirm typography is untouched), but it is a real off-scale size in the shipped UI and the fence's own comment asserts "Type scale — 5 sizes … All consumed", which is true of the *tokens* and false of the *rendered type*.
- **Finding — the same class renders at two sizes.** `#confirm-error` carries `class="hint hidden"` (`index.html:180`) and computes **16px**, while every other `.hint` computes **14px**. An ID rule outranks the class. Same class, two sizes, on the same screen region (the authorization modal).
- `#brainstorm-view h2` measures 16px / `rgb(79,52,34)` — the C-1 downstream-gate discrepancy already recorded (ROADMAP says 14px / `#8a6508`); reproduced here, left as the user's call.

### Pillar 5: Spacing (4/4)

- **12-step scale intact and fully tokenized.** Every `padding` / `margin` / `gap` declaration outside the fence resolves to `var(--space-*)`. `awk 'NR>224' … | grep -oE '(padding|margin|gap|…)[^;]*' | grep -oE '[0-9]+px'` returns **nothing**.
- **Zero arbitrary values.** `grep -cE '\[[0-9.]+(px|rem|em|%|vh|vw)\]'` outside the fence = **0**.
- **S-1 untouched**, as the contract requires: no `--space-*` line appears in the phase diff; the seven spacing drifts were accepted at HEAD via updated UAT expectations (D-12).
- **Observation (not scored, not a violation): 768px squeezes the AI work panel.** No horizontal overflow at 1440/1280/1024/768 (`document.documentElement.scrollWidth == window.innerWidth` at all four). But at 768px the five controls in `#probe-controls` compress to 36px wide × 134px tall, with `发起测试调用` / `处理本轮批注` wrapping to four vertical glyphs each (`select#ai-route-select` 152×134, `input#project-path-input` 164×134, `button#btn-ping` 36×134, `#btn-process-round` 36×134, `#btn-abort` 36×134). Nothing is clipped, so the contract's "≥768px: no content occlusion" is arguably held — and `04-UI-SPEC.md` Q5 explicitly assigns the `@media` guard to **Phase 6** ("Fence (Phase 6 implements)"), with `@media` count still 0. Recorded, not deducted.

### Pillar 6: Experience Design (2/4)

**State coverage is genuinely thorough — this is why the score is 2 and not 1.**

- **Loading:** `#state-badge` streams the phase string; `.event-list.streaming`; `#btn-process-round` / `#btn-approve-draft` / `#btn-authorize` / `#btn-start-writing` / `#btn-divergence` all disable with `cursor: not-allowed` (8 `:disabled` sites, `style.css:656/668/884/935/947/961/1005/1034`).
- **Error:** `#stream-banner.fatal` (red-2 ground / red-11 text / red-7 border — the `--color-action-danger ON --color-surface-danger` pair, 4.94 ✓), `.inline-error`, `#confirm-error`, `.kind-error .event-content`.
- **Empty:** `#draft-empty`, `#rounds-hint`, the annotation-list empty paragraph.
- **Destructive confirmation:** present and strong — the permission modal, and the authorization modal which requires the literal confirmation word and defaults to refusal ("默认拒绝"). Good.
- **Finding — no focus indicator (Priority 2).** Zero `:focus` / `:focus-visible` / `outline` rules in the entire stylesheet. Measured UA ring vs fill: **1.26:1** on `#0d74ce`, **1.15:1** on `#ce2c31`. Verified via real `Tab` traversal to `#btn-send`. This is the app's primary action and its destructive action, and neither is visibly focusable. Partly the Phase-7 carry-forward (#8) — but the phase is the one that changed the ground the ring sits on, so it is fair to score the shipped state.
- **Finding — no hover feedback on filled buttons (Priority 3).** Measured identical base/hover for `#btn-send`, `#btn-permission-allow`, `#btn-permission-deny`. The interaction layer is inconsistent: neutral buttons respond, filled ones do not.
- **Known, not re-scored:** CR-02 (`wait_done("#btn-send")` predicate is dead code — pre-existing), W-2/W-3 (CHECK-01's whitespace and marker-move gaps), W-5 (`!= "none"` on an absent element), W-6 (z-index ordering has prose only), IN-01/02/03. All deferred by the plan-04 register; none newly introduced.

---

## Registry Safety

Not applicable. `components.json`, `tailwind.config.*` and `postcss.config.*` are all absent; no shadcn, no third-party registry, no design-system package, no build step (D-06). `frontend/vendor/` contains exactly `marked.min.js`. **Registry audit: 0 third-party blocks checked, no flags.** The Radix hex values are hand-transcribed into the fence — no Radix file enters the repository.

---

## Explicitly Out of Scope — Not Reported as Findings

- **375px mobile.** The layout collapses (main-pane text stacks one glyph per line, composer clipped, AI panel overflowing). `04-UI-SPEC.md` Q5 and the Deliberate Delta Ledger rule this out: "Responsive / mobile / breakpoint system … Out of scope. No `@media` below 1024px." Single-user local desktop tool. Not scored.
- **Dark mode / `prefers-color-scheme`** — excluded by the milestone charter; `@media` count = 0.
- **S-1 (12-step spacing) and S-2 (14px tier-1 size)** — signed off, untouched, verified zero-line diff on those token families.
- **`.overlay` backdrop covering the whole viewport including the doc panel** — I suspected a coverage bug from the screenshots and disproved it by decoding pixels: under the backdrop the doc panel measures `(137,137,137)` = `0.55 × #f9f9f9` and the main pane `(138,138,138)` = `0.55 × #fcfcfc`. Uniform coverage, correct compositing. Not a defect.
- **Two human-judgment items left unresolved, deliberately:** the 28 UI-SPEC backstop statements (render geometry — clipping, wrapping, scroll ownership, 200% zoom, menu repositioning) and the E16 `--color-text ON --color-surface-mark` ratio attribution. I produced new evidence bearing on E16 (above) and on E1's overflow half (all seven real chip labels measure `w == scrollWidth == 48px`, no wrap, no clip) but I am not turning either green.
- **`#doc-panel-body` `overflow-y: visible`** — looked like an E5 scroll-ownership failure, but the scroll owner is `#doc-panel` (`style.css:380-385`, `overflow-y: auto`); `documentElement.scrollHeight == innerHeight` at 1440. Not a defect.

---

## Files Audited

- `frontend/style.css` (933 lines — fence `:root` L5-L224, the 43-pair manifest, the four out-of-fence declarations L434 / L472 / L549-559 / L583-591, L887-896, L905-910)
- `frontend/index.html` (structure, ids, copy — read-only, zero diff this phase)
- `frontend/app.js` (render paths, `KIND_LABELS`, copy — read-only, zero diff this phase)
- `scripts/check-01-token-conformance.sh`, `scripts/check-02-contrast.py`, `scripts/check-03-hidden-uniqueness.sh`, `scripts/check-04-important-count.sh` (all re-run)
- `scripts/check-05-ui-uat.py` (re-run in full; item-by-item compared to the P3.7 baseline)
- `scripts/ui-states/{p1,p12,p3,checking,archive}` (driven live)
- `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md`, `idi-04.1-CONTEXT.md`, `idi-04.1-PATTERNS.md`, `idi-04.1-VERIFICATION.md`, `idi-04.1-0{1,2,3,4}-PLAN.md`, `idi-04.1-0{1,2,3,4}-SUMMARY.md`
- `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` (§Q5, §Q7, ledger L-1, accent/contrast tables)
- Screenshots: `.planning/ui-reviews/idi-04.1-20260920-105951/` (20 PNGs, gitignored)
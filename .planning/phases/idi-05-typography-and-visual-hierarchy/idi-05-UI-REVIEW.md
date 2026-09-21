# Phase 5 (idi-05) — UI Review

**Audited:** 2026-09-21
**Baseline:** `idi-05-UI-SPEC.md` (status: approved, `review_verdict: APPROVED`) — an incremental contract that rewrites `04-UI-SPEC.md` §Typography and *augments* `idi-04.1-UI-SPEC.md` §Color / §Contrast Verification
**Screenshots:** not captured — no dev server on :3000 / :5173 / :8080 (curl → `000` on all three). Code-only audit.
**Change surface:** `frontend/style.css` (220 lines changed) + `scripts/check-05-ui-uat.py` (349 lines). `frontend/app.js`, `frontend/index.html`, `frontend/vendor/`, `scripts/ui-states/` are byte-unchanged (`git status --porcelain -- frontend/` → empty; `frontend/vendor/` → `marked.min.js` only).

---

## Pillar Scores

| Pillar | Score | Key Finding |
|--------|-------|-------------|
| 1. Copywriting | 4/4 | Zero copy changes by construction; every frozen CTA/empty/error string intact and specific. |
| 2. Visuals | 3/4 | Focal point and the three-tier action ramp are genuinely established, but the "h1 is the largest text on screen" claim is falsified by unscoped markdown headings, and the Deliberate Delta Ledger omits the one mid-execution selector change. |
| 3. Color | 3/4 | All 47 PAIRs pass `check-02` (exit 0) and every value matches the contract exactly — but the phase adds three solid saturated fills with no 60/30/10 area check, and the G3 red-line pair's margin collapses from 6.5 to 0.22. |
| 4. Typography | 2/4 | Declared 7-step scale + 3 weights are exact and fully consumed, but `renderMarkdown` emits `h1/h2/h3` into five containers outside `.markdown-body` that receive UA defaults (up to **32px / weight 700**) — a 4th weight and an 8th+ size, unlisted in the contract's own off-scale enumeration. |
| 5. Spacing | 4/4 | Zero spacing-scale declarations changed; the two new declarations are in-scale (`--space-1`); the new geometry literals (`3px`, `-2px`, `12px`) are non-spacing and documented. |
| 6. Experience Design | 3/4 | New active-panel state is well-gated (3 samples + 2 controls) and all 8 `:disabled` states preserved — but the G3 control still has no hover/focus affordance, and `#session-panel .panel-header` keeps `cursor: pointer` with no click handler while the other two panels were given `cursor: default`. |

**Overall: 19/24**

---

## Top 3 Priority Fixes

1. **Unscoped markdown headings break the contract's page-level hierarchy (SC3 / E2 / UAT #3).** `renderMarkdown()` (app.js:112) returns real `<h1>/<h2>/<h3>` and is called into **five containers that are not `.markdown-body`**: `.event-content` (app.js:239), `.chat-bubble` (app.js:270), `.say-chunk p` (app.js:284), `.annotation-note` (app.js:1144), `.annotation-answer-body` (app.js:1157). No rule anywhere in `style.css` sets `font-size` or `font-weight` on an `h1/h2/h3` outside `.markdown-body` (verified: the only heading rules are `.markdown-body h1/h2/h3` :719-721, `#doc-panel-header h1` :493, `.panel-header h2` :520, `.overlay-card h3` :636, `#draft-view > h2, #round-title` :704, `#brainstorm-view > h2` :775, `.round-view-header h2` :889, marker rules :1223-1225). UA defaults therefore apply: a `#` in an AI chat bubble renders **32px / bold 700** (2em of `.chat-bubble`'s 16px), and in `.event-content` **28px** (2em of `.event-item`'s 14px); a `##` renders 24px / 21px. All three exceed `.markdown-body h2` (22px), and two of them tie or beat `.overlay-card h3` (24px) and the document h1 (28px). **User impact:** the phase's headline deliverable — "the document h1 is the largest, heaviest text on screen, 28 > 24 > 22" — is not true in any state where the AI emits a heading, and a **fourth font weight (700)** enters the app outside the contract's declared three ranks (`--fw-regular` 400 / `--fw-medium` 500 / `--fw-semibold` 600, `style.css:248-250`). **Fix:** scope the heading scale to the render targets, not just `.markdown-body` — either add `.event-content h1/h2/h3, .chat-bubble h1/h2/h3, .say-chunk h1/h2/h3, .annotation-note h1/h2/h3, .annotation-answer-body h1/h2/h3 { font-size: …; font-weight: var(--fw-semibold); }` (or a shared `.md-scope` class), and add a `check-05` assertion enumerating **all five** render targets, mirroring the `MARKDOWN_HOSTS` four-host probe that plan 01 already had to introduce after a single-host probe let the cascade defect survive to execution.

2. **The Deliberate Delta Ledger is missing the chrome selector narrowing — its own rule says unlisted changes read as regressions.** `idi-05-UI-SPEC.md:781` states: "本阶段每一项有意的视觉变化,一张表。**不在此表上的变化即回归**", and its zero-list at `:805` requires "任何既有选择器的位置 / 名字 / 声明增删" to be zero apart from P-2…P-4 and P-12/P-13. The executed diff changes **three existing selectors** — `#draft-view h2, #rounds-placeholder h2` → `#draft-view > h2, #round-title` and `#brainstorm-view h2` → `#brainstorm-view > h2` — which is a real rendering change (it is what makes 22px reachable on three of four hosts). It is registered in the contract's 订正记录 (`:323-333`) and in `WINDOWS.md` #15, but it has **no P-item in the ledger**. **User impact:** the ledger is the phase's machine-readable "everything intentional" contract; a reader auditing "is this a regression?" against it gets a false positive on the phase's single most load-bearing edit. **Fix:** add `P-19 | chrome heading selectors narrowed from descendant to child/id form | :704 :775 | 3 rules | cascade fix (WINDOWS #15)` and amend the zero-list to except it.

3. **Color: no 60/30/10 area measurement after the ramp, and the G3 red-line pair's margin collapses to 0.22.** The contract's A-7 (`:821`) discharges the 60/30/10 obligation by arguing that the marker keeps the same *element list* and the same *colour* (blue-11), so "accent 面积占比不受影响". That argument covers only the marker. The phase's **other** colour delta — three buttons flipping from a `green-3` tint to solid `green-11`/`green-12` fills (P-5…P-9) — materially enlarges the saturated-accent area, and no measurement or registration accompanies it. Separately, `--color-action-commit-fg ON --color-action-commit-surface` drops from 11.00 to **4.72** (margin 0.22) on the button whose label is the core-value red line (`05-N-3` calls it "本阶段对核心价值红线最大的一次赌注"). **User impact:** the accent distribution is now unverified, and the most safety-critical label sits 0.22 above AA — any future nudge to `--radix-green-11`, `--white`, or the surrounding surface silently breaks it. **Fix:** record the accent-area delta in the ledger (or state explicitly that only the *element list* is governed, so the area is out of scope by contract), and add a margin-regression guard — e.g. assert the ratio in `check-02` output stays `>= 4.70` so a step change fails loudly rather than passing at 4.51.

---

## Detailed Findings

### Pillar 1: Copywriting (4/4)

**No findings within scope.** The phase is copy-neutral by construction and the evidence is structural, not asserted:

- `frontend/app.js` and `frontend/index.html` are byte-identical to HEAD (`git status --porcelain -- frontend/` → empty). A pure-CSS phase **cannot** introduce or alter a user-facing string.
- Contract §Copywriting Contract (`:750-776`) freezes every string and the phase honours it. Spot-checked against the live DOM: primary CTA `进入` (index.html:96) / `发送`; routine loop `处理本轮批注` (:73) / `继续自检` / `继续修复`; commit `认可雏形` (:126); irreversible `授权撰写总设计文档` (:143) — all specific, none generic. Empty state `尚无草稿——和 AI 讨论出实质进展后,它会写入 docs/draft.md。` (:115) names the artefact and the trigger; no `No data` / `Submit` / `Click here` patterns exist in the codebase.
- The two `window.prompt` / destructive-confirmation rules are untouched; the phase adds no destructive action and no confirmation step.
- Both new glyphs are decorative and same-coloured as their adjacent text (`.annotation-quote` :931 and `.verdict-location` :1145 both carry `--color-text-secondary`, matching the `background-color` at :949 / :1154), so they carry no text-information obligation. Correct.

Score 4 — no issue found, contract met with the strongest available evidence (zero diff).

### Pillar 2: Visuals (3/4)

**What is right.** The three-tier action ramp is a genuine, mechanically-checked visual distinction and it does not rest on colour depth alone: routine = `green-3` ground + `green-12` text (:137-139), commit = `green-11` fill + `--white` text (:140-142), irreversible = `green-12` fill + `--white` text (:143-145). Fill-vs-tint is the first discriminator, which is exactly the "形态差异是第一区分手段" claim, and it survives greyscale. The active-panel marker (`box-shadow: inset 3px 0 0`, :1221) is a **shape** signal, not a colour-only signal, so it does not violate "not by colour alone".

**Finding 2.1 — BLOCKER: the "largest text on screen" claim is false.** See Top Fix #1. `.markdown-body h1` at 28px / 600 is not the ceiling: `renderMarkdown` output lands in five containers with no heading rules, so `.chat-bubble h1` renders 32px / 700 and `.event-content h1` renders 28px / 700. The contract asserts the chain only among four hand-picked selectors (`.markdown-body h1` 28 > `.overlay-card h3` 24 > `.markdown-body h2` 22 > `#doc-panel-header h1` 14) and `check-05` asserts exactly that chain — a single-point gate over a claim that is really about the whole document. This is the same failure class plan 01 already paid for (a one-host probe let the chrome-cascade defect survive to execution); the phase fixed the probe's host set for `.markdown-body` but never asked the equivalent question for the *maximum rendered size*.

**Finding 2.2 — WARNING: the Deliberate Delta Ledger omits the selector narrowing.** See Top Fix #2.

**Finding 2.3 — WARNING: chrome subview titles are inconsistent and one is indistinguishable from body text.** Three sibling subview labels sit at two sizes: `#draft-view > h2` and `#round-title` = 18px (`--text-lg`, :704-707), `#brainstorm-view > h2` = **16px** (`--text-md`, :775-779) — the same size as `.markdown-body` body copy. The contract records this as "记录,不处理" (`:317-321`, `:1021`) with the reasoning that chrome and content titles are two token families whose relative size is not this phase's to harmonise. That reasoning is sound for *chrome vs content*; it does not cover *chrome vs chrome*, and a reader sees "雏形草稿(draft.md)" and "发散候选(brainstorm.md)" rendered at different sizes inside the same `#draft-view` block. Not introduced by this phase (the 16px predates it, from `260918-qrq`), but it is visible in the shipped UI and no backlog item owns it.

**Finding 2.4 — WARNING: no fallback if `mask-image` is unsupported.** Both pseudo-elements carry `background-color: var(--color-text-secondary)` with `mask-image` as the only thing suppressing the fill (:949-955 / :1154-1160). With no `@supports (mask-image: …)` guard and no `content` fallback, an engine without mask support paints a solid 12×12 grey square in place of the pin and the location marker. Low probability (all current engines support it) but the failure mode is silent and the phase has no gate for it — Gate 5 checks only that the URI carries no colour, not that the glyph survives.

**Finding 2.5 — INFO: `#session-panel .panel-header` carries `cursor: pointer` with no click handler.** `.panel-header { cursor: pointer }` (:514) applies to all four headers; `#annotations-panel .panel-header` (:903) and `#checks-panel .panel-header` (:1104) were each given `cursor: default`, `#session-panel` was not. The only click listeners are on `#ai-panel-header` (app.js:1561) and `#doc-panel-header` (app.js:1567). This phase's marker makes the session header look *more* like a control (coloured title + left bar), which amplifies the false affordance. Pre-existing, but now co-located with a new affordance cue.

### Pillar 3: Color (3/4)

**Verified against the contract, value by value.** All 47 `/* PAIR */` entries pass `python3 scripts/check-02-contrast.py` → `PASS: 0 failures`, exit 0; 35 TEXT + 12 NON-TEXT + 1 `ORDER`. The manifest header comment has been corrected to `24 / 34 / 43 / 47` (:334-343) — the stale-comment observation plan 03 left to the verifier was resolved in `b1a9bbc`. Every declared value matches the contract exactly:

| Token | Contract (`idi-05-UI-SPEC.md`) | Disk | ✓ |
|---|---|---|---|
| `--color-action-commit-surface` | green-11 | `var(--radix-green-11)` :141 | ✓ |
| `--color-action-commit-fg` | `--white` | `var(--white)` :142 | ✓ |
| `--color-action-irreversible` | green-12 | `var(--radix-green-12)` :143 | ✓ |
| `--color-action-irreversible-surface` | green-12 | `var(--radix-green-12)` :144 | ✓ |
| `--color-action-irreversible-fg` | `--white` | `var(--white)` :145 | ✓ |
| `--color-marker-active` | `--radix-blue-11` | `var(--radix-blue-11)` :169 | ✓ |

Tier accounting matches: tier-1 primitives = **25** (new primitives = 0, as S-7 claims), tier-2 `--color-*` = **48** (47 → 48, the delta the contract registers at `:954`). Zero hardcoded colours outside the fence (`check-01` → PASS). The marker's claimed ground is correct — `#main-pane > section` declares no background (:462-465), so `html, body { background: var(--color-surface-page) }` (:437) is the ground, and the TEXT/NON-TEXT pair is measured against it. The commit/irreversible boundary pairs' ground (`--color-surface`) is also correct: `#approve-row` (:125), `#writing-view` (:148) and `#authorize-row` (:142) all sit inside `#doc-panel` (:82), which declares `background: var(--color-surface)` (:474).

**Finding 3.1 — WARNING: 60/30/10 area is unverified for the fill ramp.** See Top Fix #3. A-7 discharges the obligation for the marker only; the three solid fills are a larger accent-area change and carry no registration.

**Finding 3.2 — WARNING: the G3 red-line pair's margin is 0.22.** `--color-action-commit-fg ON --color-action-commit-surface` = white on `green-11` = **4.72** (was 11.00). `05-N-3` names this the phase's biggest bet and permits exactly one remediation ("抄进计划的验收命令"). That is honest but it is a *documentation* mitigation, not a guard: nothing fails if a later change moves the ratio to 4.51.

**Finding 3.3 — INFO: `--color-marker-active` is `--radix-blue-11`'s fifth tier-2 consumer** (`--color-action-primary`, `--color-text-info`, `--color-kind-say`, `--color-border-streaming`). The contract owns this (`:423-425`) and the naming rationale (D-18: don't reuse `--color-action-primary`, whose name says "primary action") is the correct application of the project's "names must not lie" methodology. Recorded here only so the fifth-consumer fact is not re-derived later.

### Pillar 4: Typography (2/4)

**The declared scale is exact.** 7 ranks declared (`style.css:238-244`), all consumed: `--text-base` ×19, `--text-xs` ×7, `--text-md` ×7, `--text-xl` ×2, `--text-lg` ×2, `--text-3xl` ×1, `--text-2xl` ×1. The mapping matches the contract table (`:205-210`) exactly — h1 `--text-3xl` (:719), h2 `--text-2xl` (:720), h3 `--text-lg` (:721), body `--text-md` (:709, unchanged). Weight ranks: 3 declared (:248-250), all consumed — `--fw-semibold` ×8, `--fw-medium` ×8, `--fw-regular` ×1, matching P-16's accounting (4 → 8 and 12 → 8). `#btn-authorize` correctly keeps 600 (:1058) as D-12's single registered exception, and `#btn-divergence` correctly stays 600 (:761) as the unregistered fourth tier's exclusion. No global `h1, h2, h3` rule exists (Hard Rule 9 holds).

**Finding 4.1 — BLOCKER: a fourth weight rank and at least two undeclared sizes enter through `renderMarkdown`.** See Top Fix #1. Concretely:

| Render target | Context size | `#` → | `##` → | `###` → |
|---|---|---|---|---|
| `.chat-bubble` (app.js:270) | 16px (:816) | **32px / 700** | 24px / 700 | 18.7px / 700 |
| `.event-content` (app.js:239) | 14px (:582) | **28px / 700** | 21px / 700 | 16.4px / 700 |
| `.annotation-note` (app.js:1144) | 16px (root) | **32px / 700** | 24px / 700 | 18.7px / 700 |
| `.annotation-answer-body` (app.js:1157) | 16px (root) | **32px / 700** | 24px / 700 | 18.7px / 700 |
| `.say-chunk` (app.js:284) | 16px (root) | **32px / 700** | 24px / 700 | 18.7px / 700 |

`html, body` declares no `font-size` (:433-438), so the root is the UA 16px. The contract's own enumeration of off-scale sizes (`:335-339`) lists only `.collapse-indicator`'s `20px` and the `#confirm-error` double-size `.hint` — it does **not** count this path, so the phase inherited and repeated an incomplete census. `font-weight: 700` is not among the three declared ranks, which contradicts the contract's "Weight — three ranks, all consumed" (`:246-250`) and TYPE-03's declared division of labour.

**Finding 4.2 — WARNING: h3 (18px) is only 1.125× body (16px).** The h3 step is carried almost entirely by weight (600 vs 400) rather than size. That is defensible and it is what D-06 chose, but it means the h3/h4 boundary in a rendered DESIGN.md is subtle at reading distance. No measurement or human check targets it.

**Finding 4.3 — INFO: the two deferred typographic anomalies remain.** `.collapse-indicator { font-size: 20px; line-height: 1 }` (:522) is still the only off-scale literal and still 20px — larger than every chrome label in the app. `#confirm-error` still renders at 16px while every other `.hint` renders at 14px (`:503` vs `.overlay-card p` :637). Both are explicitly assigned elsewhere (backlog `999.1`; S-8) and both are correctly untouched — `git diff` shows no change to either. Recorded so the 2/4 is not read as covering them.

### Pillar 5: Spacing (4/4)

**No findings.** The phase changes **zero** spacing-scale declarations — the contract's "本阶段的间距改动 = 0 条声明" (`:729`) holds. Both new declarations are in-scale: `margin-right: var(--space-1)` on `.annotation-quote::before` (:948) and `.verdict-location::before` (:1153), each 4px, and the contract's claim that this approximates the emoji's trailing-space footprint (`:610-612`) is plausible at 12px + 4px = 16px.

The three new geometry literals are all outside the `--space-*` family and each is documented in-line where it appears, not just in the contract: `box-shadow: inset 3px 0 0` (:1212-1213, with the frozen-round precedent at `#round-doc.round-frozen`), `vertical-align: -2px` (:946, a vertical-align value), and `width/height: 12px` + `mask-size: 12px 12px` (icon dimensions, D-22). No arbitrary bracket values anywhere in the file (`grep -E '\[[0-9.]+(px|rem|em)\]'` → empty). No `@media`, `@layer` or `@property` introduced (count still 0). `#btn-authorize` correctly takes no padding step (D-13) — only `font-size: var(--text-md)` (:1057).

The narrow-panel no-wrap arithmetic (`:743-746`) is not machine-verified by `check-05` and the contract says so; it was closed by human UAT #4.

### Pillar 6: Experience Design (3/4)

**State coverage is preserved and one state is newly afforded.**

- All 8 `:disabled` rules survive with their opacity intact (`0.55` ×6, `0.5` ×2) — verified by `grep -c 'opacity: 0.55'` and the fact that the phase diff touches none of them. D-14's "do not soften `:disabled`" holds.
- No loading/error/empty state can regress: `app.js` and `index.html` are byte-unchanged, so the structure, copy and visibility of every such state is fixed by construction. The contract states this correctly for E3/E4/E5/E6/E7/E8/E9 (`:1120-1155`).
- The new active-panel state is genuinely gated, and — notably — gated **per instance**: `check_active_marker` (check-05:626) reads `box-shadow` on `p1 → #session-panel`, `p3 → #annotations-panel`, `checking → #checks-panel`, with `check_marker_control` (:674) asserting `#ai-panel .panel-header` and `#doc-panel-header` stay `none`. A same-reader-different-element control pair is the right shape for proving the reader is not vacuous. This is the pillar's strongest evidence.

**Finding 6.1 — WARNING: the G3 control has no hover or focus affordance, and the phase made it more prominent without adding any.** `#btn-authorize` now carries four emphasis channels (solid `green-12` fill, white 16px text, weight 600, larger padding box) and is the app's single most consequential control — yet `button:hover` (:560) is 0-1-1 and loses to `#btn-authorize`'s 1-0-0, so there is no hover feedback; and there is no `:focus-visible` / `outline` rule anywhere (count 0). A keyboard user tabbing to 授权撰写总设计文档 gets no visual indication. The contract assigns focus to Phase 7 (`A11Y-01`) and hover to `INTERACT-01`, and correctly notes there is no *regression* here — but "no regression" is not the same as "covered", and this is the one control where the project's core value makes the gap load-bearing.

**Finding 6.2 — WARNING: `#session-panel .panel-header` false affordance.** See Finding 2.5. `.panel-header`'s `cursor: pointer` is applied to a header with no click handler, while the two sibling panels were each given `cursor: default`. This phase's marker makes that header look more interactive, not less.

**Finding 6.3 — INFO: the active marker is redundant with mutual exclusion.** The three panels are `display: none` when inactive, so "distinguishable" degenerates to "the one you can see is marked". The contract owns this explicitly (`:476-477`) and it is not a defect — recorded so a future reader does not read the marker as an attempt at a four-way state indicator.

---

## Files Audited

- `frontend/style.css` (1227 lines; fence `:root` :6-430, chrome headings :493 / :520 / :636 / :704 / :775 / :889, `.markdown-body` :709-741, action buttons :743-751 / :1000-1006 / :1050-1060 / :1065-1072 / :1124-1134, mask pseudo-elements :942-957 / :1147-1162, active-panel marker :1218-1227)
- `frontend/index.html` (:16 / :31 / :42 / :58 / :73 / :82-90 / :96 / :104-129 / :133-149 — DOM structure, heading placement, all frozen copy)
- `frontend/app.js` (:112-137 `renderMarkdown`, :239 / :270 / :284 / :1144 / :1157 render targets, :1561-1570 collapse listeners)
- `scripts/check-05-ui-uat.py` (:267 `check_mask_glyph`, :626 `check_active_marker`, :674 `check_marker_control`, :868 `MARKDOWN_HOSTS`, :932-942 four-host probe)
- `scripts/check-01-token-conformance.sh`, `scripts/check-03-hidden-uniqueness.sh`, `scripts/check-04-important-count.sh`, `scripts/check-02-contrast.py` (re-run: PASS / exit 0)
- `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` (full, in sections)
- `.planning/phases/idi-05-typography-and-visual-hierarchy/05-CONTEXT.md`, `idi-05-01-SUMMARY.md`, `idi-05-02-SUMMARY.md`, `idi-05-03-SUMMARY.md`, `05-UAT.md`

**Gates re-run for this audit (independently, not inherited):** `check-01` PASS, `check-02` `PASS: 0 failures` (47 pairs) exit 0, `check-03` PASS, `check-04` PASS; fence markers 1/1; Gate 2 orphan `var()` → empty; Gate 5 → `%23` count 0, `fill=` only in comment prose (:309); tier-1 = 25, tier-2 = 48; `^\.hidden {` = 1; `!important;` = 1; `@media` = 0; `frontend/` porcelain empty.

**Registry Safety:** not applicable — `components.json` does not exist, `Tool: none`, no registries, no third-party blocks, no build step. `frontend/vendor/` contains only `marked.min.js`. Registry audit: 0 third-party blocks checked, no flags.

**Note on scoring:** Pillars 1 and 5 score 4 because the phase's copy and spacing surfaces are literally unchanged and that was verified by diff, not asserted. Pillar 4 scores 2 rather than 3 because the failure is not a stray value — the phase's controlled scale does not govern a rendering path that produces larger, heavier text than the scale's top rank, which is a gap in the deliverable itself. No pillar was adjusted to make the total look better; the 19/24 reflects one BLOCKER-class contract violation and five WARNING-class gaps.
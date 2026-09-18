# Stack Research

**Domain:** Zero-dependency CSS design-token system + WCAG AA accessibility retrofit into an existing framework-free vanilla frontend
**Project:** 交互式讨论迭代系统 (Interactive Discussion Iteration) — Milestone v1.14 前端视觉与可访问性
**Researched:** 2026-09-17
**Confidence:** HIGH (platform capability data verified against MDN + MDN browser-compat-data; contrast ratios computed from the actual `frontend/style.css`)

---

## Headline

**This milestone adds zero dependencies and zero new files.** Every recommendation below is a native CSS platform feature already supported by every browser that can run this tool. The "stack decision" is therefore not *which packages* — it is **which CSS mechanisms to use and which to refuse**, because three of the obvious-sounding modern CSS features (`@layer`, `@property`, relative color syntax) actively make this retrofit worse.

**The one-line answer:** add a single `:root { … }` block at the top of `frontend/style.css`, migrate declarations by substitution, and add new additive rules for focus/state/responsive — all in the existing 622-line file, with **no `@layer`, no `@property`, no `var()` fallbacks, and no JS changes**.

---

## Recommended Stack

### Core Technologies

| Technology | Version / Support floor | Purpose | Why Recommended |
|------------|------------------------|---------|-----------------|
| **CSS custom properties** (`--token`, `var()`) | Chrome 49 / Safari 9.1 / Firefox 31 — caniuse 96.17% global | The token substrate. The only mechanism the constraints permit. | Universally supported since 2016. Cascade-neutral: substituting `var(--x)` for a literal does **not** change specificity or source order, which is precisely why the migration can be done incrementally without a rewrite. |
| **`:focus-visible`** | Chrome 86 / Safari 15.4 / Firefox 85 — caniuse 94.73% global | Keyboard-only focus ring | Satisfies WCAG 2.4.7 (Focus Visible, AA) without painting a ring on every mouse click. The `:focus`-only alternative regresses pointer UX. |
| **`@media (prefers-reduced-motion: reduce)`** | Chrome 74 / Safari 10.1 / Firefox 63 | Suppress the one existing `transition` and any new ones | WCAG 2.3.3 (Animation from Interactions, AAA). Zero cost — the file has exactly **1** `transition` today, so this is a 3-line guard. |
| **`@media (prefers-contrast: more)`** *(optional)* | Chrome 96 / Safari 14.1 / Firefox 101 | Opt-in high-contrast token overrides | Free once tokens exist: a second `:root` block re-pointing the same semantic names. **Only if the UI-SPEC wants it** — not required for AA. |
| **`@media (max-width: …)`** | Chrome 1 / Safari 3 / Firefox 2 | Narrow-window reflow | WCAG 1.4.10 Reflow (AA) **requires** no two-dimensional scrolling at 320 CSS px width. The current `#sidebar { flex: 0 0 420px }` violates this outright. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| — | — | — | **None. This is the point.** |

There is no supporting library, no dev dependency, no npm package, and no vendored file to add. `frontend/vendor/` stays exactly as it is (one JS file, `marked.min.js`, no CSS).

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| Browser DevTools (already installed) | Token inspection | Custom properties appear in the Computed pane and are live-editable. This is the entire toolchain. |
| A grep gate | Verify token integrity | See "Verification gates" below — scriptable with `grep`/`python3`, both already present. |

---

## Installation

```bash
# Nothing. Zero installs. Zero new files.
#
# The threat model for this milestone already registers:
#   "any install need is a plan deviation and a stop condition."
#
# Every recommendation in this document is achievable by editing
# the three files that already exist:
#   frontend/style.css   (the only file that MUST change)
#   frontend/index.html  (only if the UI-SPEC changes markup — see below)
#   frontend/app.js      (NOT required — see "Zero JS coupling")
```

---

## Decision 1 — Token taxonomy: two-tier for color, single-tier for everything else

**Recommendation: two-tier (primitive → semantic) for color ONLY. Single-tier for spacing, type, and radius.**

```css
:root {
  /* ── Tier 1: primitives. Raw values. No meaning. Never referenced outside this block. ── */
  --gray-900: #1a1a1a;
  --gray-700: #555555;
  --gray-500: #6a6a6a;
  --gray-400: #8a8a8a;
  --gray-200: #e0e0e0;
  --gray-100: #f5f5f5;
  --gray-050: #fafafa;

  --blue-700: #1f63bd;
  --blue-500: #2c7be5;
  --green-700: #26754a;
  --green-500: #2e8b57;
  --amber-700: #8a6508;
  --amber-500: #b8860b;
  --red-600: #c0392b;
  --purple-600: #6f42c1;

  /* ── Tier 2: semantic. Meaning. This is what every selector references. ── */
  --color-text:            var(--gray-900);
  --color-text-secondary:  var(--gray-700);
  --color-text-muted:      var(--gray-500);   /* was #999 — now AA-safe on every bg in the file */

  --color-action-primary:  var(--blue-700);
  --color-action-success:  var(--green-700);
  --color-action-warning:  var(--amber-700);
  --color-action-danger:   var(--red-600);

  --color-surface:         #ffffff;
  --color-surface-page:    var(--gray-050);
  --color-surface-sunken:  var(--gray-100);

  --color-border-strong:   var(--gray-400);   /* UI-component boundaries — 1.4.11 scope */
  --color-border-subtle:   var(--gray-200);   /* decorative dividers — NOT 1.4.11 scope */

  --color-focus:           var(--blue-700);

  /* ── Scales: single-tier. A scale step has no meaning beyond its ordinal. ── */
  --space-1: 2px;  --space-2: 4px;  --space-3: 6px;  --space-4: 8px;
  --space-5: 10px; --space-6: 12px; --space-7: 16px; --space-8: 24px; --space-9: 32px;
  --radius-1: 3px; --radius-2: 4px; --radius-3: 6px; --radius-4: 8px; --radius-pill: 999px;
  --text-xs: 11px; --text-sm: 12px; --text-base: 13px; --text-md: 14px;
  --text-lg: 16px; --text-xl: 18px; --text-2xl: 20px;
}
```

**Why two-tier for color and not the rest:**

1. **Color is where the ambiguity actually lives.** The audit's Pillar 3 finding is not "the palette is wrong" — it is that *green means seven different things* across six buttons plus an event chip. That is a **naming** failure, not a value failure. Two-tier makes the failure structurally impossible: there is no `--green-500` semantic alias for "irreversible authorization," so a selector physically cannot reach for "green" as a stand-in for "positive." It must pick `--color-action-danger` or a purpose-built `--color-action-irreversible`.
2. **It is the only way the audit's two near-identical blues (`#2c7be5`, `#2c5fb8`) get reconciled.** With primitives you see both at once, 30 lines apart, and delete one.
3. **Spacing/type/radius do not need it.** `--space-4: 8px` *is* the primitive and *is* the semantic token — there is no meaningful "meaning" layer between `8px` and "one step up from 4px." Adding `--spacing-md: var(--space-4)` is pure ceremony. The audit's complaint about spacing is "16 distinct padding values and no scale" — a **scale** fixes that; a second naming tier does not.
4. **Cost of the extra tier is 1 level of indirection for ~18 color tokens**, paid once, read in DevTools where `var()` chains resolve to final values anyway.

**Cost if you skip two-tier entirely:** you get a find-and-replace of 34 hex literals into 34 `var()` calls and the color problem is not solved at all — you have simply renamed `#2e8b57` to `--green`. The milestone's stated target "语义色分层" (semantic color layering) is not satisfied.

---

## Decision 2 — Cascade layers (`@layer`): **DO NOT USE**

This is the single most consequential "what NOT to add" call in this document, and the evidence is unambiguous.

**Support is fine.** `@layer` is Baseline *widely available* since March 2022 — Chrome 99 / Safari 15.4 / Firefox 97, 95.3% global usage. Support is not the problem.

**The cascade rule is the problem.** Per MDN (`@layer`, last modified 2026-04-20):

> "Styles that are not defined in a layer **always override** styles declared in named and anonymous layers."

Applied to this project:

1. **All 622 existing lines are unlayered.** If you wrap only the *new* token rules in `@layer tokens { … }`, every one of them **loses** to the existing unlayered rules — regardless of specificity. The layer would be inert at best.
2. **To make `@layer` do anything useful you must wrap all 622 existing lines.** That is a full-file rewrite with a hand-verified re-indentation, which is exactly the failure mode the quality gate forbids.
3. **`!important` inverts layer order** — "all important declarations within CSS layers take precedence over any important declarations declared outside of a layer." The file's one `!important` is load-bearing:
   ```css
   /* style.css:13-15 */
   /* 唯一全局显隐规则:!important 必需——.overlay/.doc-subview 等自身 display 特异性
      同为 0-1-0 且声明在后,去掉 !important 会让这些容器重新无法隐藏。 */
   .hidden { display: none !important; }
   ```
   If `.hidden` ever ends up *outside* a layer while some other `display` rule ends up *inside* one, the global show/hide contract silently inverts. `app.js` calls `classList.add('hidden')` **44 times**; a regression here is a site-wide functional break, not a cosmetic one.
4. **`@layer`'s main real-world win does not exist here.** The canonical use case is isolating third-party/reset CSS from author CSS. This project loads **zero third-party CSS** — `frontend/vendor/` contains one JS file (`marked.min.js`) and nothing else, and there is no CDN. There is no vendor layer to subordinate.

**Verdict: `@layer` offers zero benefit, requires a 622-line rewrite to offer any benefit at all, and risks breaking the global `.hidden` contract. Skip it.** Record this as a decision so a later contributor does not "modernize" the file into it.

---

## Decision 3 — Custom-property fallback strategy: **use none**

**Recommendation: declare every token exactly once in a single `:root` block at the top of `style.css`. Write `var(--x)`, never `var(--x, #fallback)`.**

Three verified reasons:

1. **Fallbacks are not a compatibility shim.** MDN is explicit: *"Fallback values aren't used to fix compatibility issues for when CSS custom properties are not supported, as the fallback value won't help in this case."* And they are unnecessary — custom properties are Chrome 49 / Safari 9.1 / Firefox 31.
2. **Fallbacks do not do what people assume.** The fallback fires only when the custom property resolves to the *guaranteed-invalid* value (never declared, or set to `initial`). If the property **is** declared but its value is invalid **for the consuming property**, the whole declaration becomes *invalid at computed-value time* and is treated as `unset` (inherit or initial) — **the fallback is NOT used**. So `color: var(--color-text, #999)` where `--color-text: 20px` yields inherited/initial color, not `#999`. The safety net people imagine does not exist.
3. **Fallbacks destroy grep-ability.** With none, `grep -o 'var(--[a-z0-9-]*'` gives a set that must be a subset of `grep -o '^\s*--[a-z0-9-]*'`. That is a one-line, zero-install integrity gate. With fallbacks sprinkled in, the same grep is noisy and the gate is worthless.

**Corollary — `@property` is also refused.** Support floor is Chrome 85 / Safari 16.4 / **Firefox 128** (July 2024) — the laggard is three years behind the other two. It buys type-checking, a guaranteed initial value, and non-inheritance. None of those are needed: no token is animated, and `:root` inheritance is exactly what you want. Adding it would raise the compatibility floor for zero functional gain.

**The real hazard this creates, and its mitigation:** because an invalid substitution resolves to `unset` rather than failing loudly, a **typo'd token name is silent**. `color: var(--color-txt)` does not error — it just inherits. Mitigation is a build-free verification gate, not a fallback (see "Verification gates").

---

## Decision 4 — Breakpoints cannot be tokenised (non-obvious, will bite)

MDN, *Using CSS custom properties*: **"Variables do not work inside media queries and container queries."** `@media (max-width: var(--bp-narrow))` is invalid CSS and will be silently dropped.

So the responsive work must use literal values:

```css
/* Breakpoints are NOT tokens (CSS custom properties are invalid in @media conditions).
   Literal values, documented here, referenced nowhere else. */
@media (max-width: 900px) { … }
@media (max-width: 640px) { … }
```

Do **not** reach for media range syntax `@media (width <= 900px)` (Chrome 104 / Safari 16.4 / Firefox 102) to work around this — it is more readable but raises the floor to Safari 16.4 for no functional gain. Classic `max-width` is supported everywhere.

---

## Decision 5 — Migration order that never leaves the UI broken

The key structural fact that makes this safe: **introducing a custom property is cascade-neutral.** `background: #fff` → `background: var(--color-surface)` has *identical* specificity, source order, and computed value. Nothing about the cascade changes. This is why the migration can be incremental in a way that a class-renaming or framework migration cannot.

| # | Step | Visual delta | Reversible? | Verification |
|---|------|--------------|-------------|--------------|
| 0 | **Baseline capture.** Screenshot the app in each of the 5 phase views before touching anything. | none | — | 5 PNGs on disk |
| 1 | **Add the `:root` block only.** Zero existing declarations change. | **none — pixel-identical** | delete the block | Page renders byte-identical to step 0 |
| 2 | **Migrate color, semantic group by semantic group** (`text` → `action` → `surface` → `border`). This is where the AA contrast fixes ride along — see Decision 6. | small, **enumerated** | git revert | Contrast table re-run; step-0 screenshots diffed |
| 3 | **Migrate spacing / type / radius.** Pure substitution *except* the deliberate 12.5px → scale-step collapse. | small, enumerated | git revert | Step-0 screenshots diffed |
| 4 | **Add the focus + interaction layer** (`:focus-visible`, `:active`, `transition`). **Purely additive — no existing rule is edited.** | additive | delete the new rules | Tab through all 21 buttons / 8 inputs / 4 selects |
| 5 | **Add `@media` reflow rules.** Purely additive, appended at end of file. | additive | delete | Resize to 320px — no horizontal scrollbar (1.4.10) |
| 6 | **Fix `#state-badge { right: 448px }`.** Isolated layout change. | isolated | git revert | Badge tracks the sidebar at every width |

**Why this order:** steps 1, 4, and 5 are *purely additive* — they cannot break anything that already works. Steps 2 and 3 are mechanical substitutions whose only visual deltas are individually enumerated (the contrast fixes and the fractional-px collapse). Step 6 is deliberately last because it is the only change that touches layout geometry, and by then the token layer makes the sidebar width itself a token (`--sidebar-width`), so the magic number can be expressed as a relationship instead of arithmetic-in-a-comment.

**Do not** reorder step 2 before step 1, and do not merge steps 2 and 3 — the contrast fixes must be reviewable separately from the spacing churn.

---

## Decision 6 — Computed contrast findings (this changes the milestone's scope)

The audit (`03-UI-REVIEW.md`, Pillar 3) reports **"four WCAG AA contrast failures."** I computed every `color`/`background` pair in the actual 622-line file. **There are 13 failing declarations across 11 distinct selectors.** The audit sampled representative cases; it did not exhaustively compute.

### Every failing pair (AA 4.5:1 for normal text)

| # | Selector(s) | Current | Ratio | Fix |
|---|-------------|---------|-------|-----|
| 1 | `.hint` (pervasive — every gate explanation) | `#999` on `#fafafa` | **2.73:1** | `--color-text-muted` |
| 2 | `.badge-answered` (已回应 badge) | `#999` on `#f5f5f5` | **2.61:1** | `--color-text-muted` |
| 3 | `.event-kind` **default** chip | `#fff` on `#999` | **2.85:1** | `--color-kind-default` |
| 4–5 | `#pending-count`, `.badge-pending` | `#b8860b` on `#fdf6ec` | **3.03:1** | `--color-action-warning` |
| 6 | `.event-kind` ochre chip (执行) | `#fff` on `#b8860b` | **3.25:1** | `--color-action-warning` |
| 7–11 | `#btn-approve-draft`, `#btn-process-round`, `#btn-authorize`, `#btn-start-writing`, `#btn-continue-check`/`#btn-continue-repair` (5 rules, **6 buttons**) | `#2e8b57` on `#e9f7ef` | **3.84:1** | `--color-action-success` |
| 12 | `.overlay-card button`, `#chat-input-row button`, `button.primary`, `.chat-user` (4 rules) | `#fff` on `#2c7be5` | **4.14:1** | `--color-action-primary` |

The audit's "four failures" named items 1, 4–5, 6, and 12. It **missed** the default `.event-kind` chip (#3), the `.badge-answered` badge (#2), and — most consequentially — the **six green buttons** (#7–11), which is the *same defect the audit independently flagged as BLOCKER 3.3* ("green overloaded across six buttons") without noticing it is also a contrast failure. That is worth telling the roadmap: **the "green button" problem and a contrast failure are the same fix.**

### Non-text contrast (SC 1.4.11, AA, 3:1)

| Element | Current | Ratio | In scope? |
|---------|---------|-------|-----------|
| Input/button borders `#ccc` on `#fff` | `#cccccc` | **1.61:1** | **YES** — the border is the only thing identifying the control. Needs ≥ `#8a8a8a` (3.45:1 on `#fff`, 3.17:1 worst-case on `#f5f5f5`). |
| `.annotation-pending-item` left border | `#e8d9a8` on `#fffdf5` | **1.38:1** | **YES** — it is a *state* indicator. |
| `.badge-pending` border | `#e8d9a8` on `#fdf6ec` | **1.31:1** | **YES** — state indicator. |
| `#eee` / `#e0e0e0` / `#f0f0f0` dividers | 1.16–1.36:1 | — | **NO.** Purely decorative separators that identify nothing. 1.4.11 does not apply; do not waste effort darkening every divider. |
| Inactive/`:disabled` controls | `opacity: .55` | — | **NO.** 1.4.11 explicitly "does not apply to inactive user interface components." |

### Proposed token values, each verified against every background it lands on

| Token | Value | Verification |
|-------|-------|--------------|
| `--color-text` | `#1a1a1a` | 16.67:1 on `#fafafa` — unchanged |
| `--color-text-secondary` | `#555555` | 7.14:1 on `#fafafa` — unchanged |
| **`--color-text-muted`** | **`#6a6a6a`** | 5.18 on `#fafafa`, 5.41 on `#fff`, 4.96 on `#f5f5f5`, **4.75 on `#f0f0f0`** (worst case). |
| **`--color-action-primary`** | **`#1f63bd`** | white on it = **5.87:1**; as text on `#fafafa` = 5.62:1 |
| **`--color-action-success`** | **`#26754a`** | white on it = 5.64:1; on `#e9f7ef` tint = **5.10:1** (was 3.84) |
| `--color-action-warning` | **`#8a6508`** | 4.96:1 on `#fdf6ec`, 4.78:1 on `#fff3c4`, 5.32:1 on `#fff` — **already present in the file**; the fix is to *delete* `#b8860b` as a text color and reuse this one |
| `--color-action-danger` | `#c0392b` | 5.44:1 white-on; 5.21:1 as text — **already passing, no change** |
| `--color-border-strong` | `#8a8a8a` | 3.45:1 on `#fff`, 3.17:1 on `#f5f5f5` — meets 1.4.11 |
| `--color-focus` | `#1f63bd` | worst case **5.15:1** across all 8 page backgrounds (needs only 3:1) |

**Three non-obvious computed results the UI-SPEC must not get wrong:**

1. **`#767676` — the value everyone reaches for as "the AA-safe grey" — FAILS here.** It is 4.54:1 on white but only **4.35:1 on `#fafafa`**, the doc-pane background where `.hint` actually lives. `#6e6e6e` also fails (4.47:1 on `#f0f0f0`). Only `#6a6a6a` passes on **every** background present in the file. Pick it and the whole class of "moved the element, broke the contrast" bugs disappears.
2. **`#8a6508` already exists in the file** (used by `#btn-divergence` and `#stream-banner`) and already passes everywhere. The amber fix is a **deletion**, not an addition: collapse `#b8860b` into `#8a6508`. Two ambers become one.
3. **One token fixes four selectors.** `#2c7be5` → `#1f63bd` simultaneously repairs `.overlay-card button`, `#chat-input-row button`, `button.primary`, and `.chat-user`. There is no reason to fix them individually.

**Note on the audit's BLOCKER 3.3 / the Core Value red line:** the irreversible G3 authorization button (`#btn-authorize`) is styled identically to the routine "继续自检" button. The token layer is the *prerequisite* for fixing this — you cannot give authorization distinct weight while both buttons share a literal `#e9f7ef`/`#2e8b57` pair. Once `--color-action-success` exists for routine positive actions, the authorization button gets a distinct semantic token (e.g. a solid `--color-action-irreversible` fill). **Solid `#26754a` fill with white text = 5.64:1, so a solid treatment is AA-safe** — the UI-SPEC is not forced into a pale tint by contrast.

---

## Decision 7 — Zero JS coupling (verified)

The token layer must not require any `app.js` change. This is verified, not assumed:

- `app.js` touches `.style` in exactly **4 places**: `pendingCount.style.display` (lines 1165, 1169) and `selectionMenu.style.left/top` (lines 1304–1305). **No color, no font, no spacing.**
- `index.html` contains **zero** `style="…"` attributes.
- `style.css` contains **zero** `outline` declarations — meaning the UA default focus ring is *currently active*. The accessibility work **adds authored focus styling**; it does not "restore a removed one." Stating this precisely matters: the audit's "grep `:focus` = 0" is a statement about *authored* styles, not about whether keyboard users can see focus today.

**Consequence: the entire milestone is a `style.css` change.** If a plan step requires editing `app.js` for a purely visual token, the plan is wrong.

---

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Native CSS custom properties | **Tailwind / SCSS / PostCSS / CSS-in-JS** | **Never here.** Locked out by D-06 and by "zero new runtime dependencies." Listed only so it is explicit that they were considered and are out of scope, not overlooked. |
| Unlayered CSS, single file | **`@layer`** | Only if this file ever starts importing third-party CSS (a reset, a component library). Today it loads none. See Decision 2. |
| Plain `var(--x)` | **`var(--x, #fallback)`** | Never as a safety net (it does not work as one). Only if a *consuming* stylesheet outside this file legitimately needs a default — not the case here. |
| Hex literals in `:root` | **`oklch()`** (Chrome 111 / Safari 15.4 / Firefox 113) | If the palette needed programmatic ramp generation. It does not — the 12 colors are inherited from the shipped UI and must stay visually recognisable. Hex keeps the diff to `style.css` readable and reviewable by a human comparing old vs new. |
| `:focus-visible` | **`:focus`** | Only if a target browser lacked `:focus-visible`. Firefox has had it since v4; Chrome 86 / Safari 15.4 are far below this tool's floor. |
| Media `max-width` literals | **Media range syntax** `(width <= 900px)` | If readability outweighed reach. Safari 16.4 floor is unnecessary here. |
| `outline` + `outline-offset` for focus | **`box-shadow` ring** | Never for focus. `outline` does not participate in layout, so it cannot cause the reflow/overflow that `box-shadow` rings can. |

---

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| **`@layer`** | Unlayered rules always beat layered rules; all 622 existing lines are unlayered, so layers would be inert or would require a full-file rewrite. Also inverts `!important` ordering, endangering the load-bearing global `.hidden` rule that 44 `classList` calls depend on. | Plain unlayered CSS. |
| **`@property`** | Firefox 128 floor (3 years behind Chrome/Safari) for benefits (type-checking, non-inheritance, animatable) that this token layer does not use. | Plain `:root` declarations. |
| **`var(--x, #fallback)`** | Does not protect against unsupported browsers (MDN says so explicitly) and does **not** fire when a declared token has a value invalid for the consuming property — that case resolves to `unset`. | Declare tokens once; add a grep integrity gate. |
| **Relative color syntax** `rgb(from var(--x) …)` | Chrome 122 / Safari 18 / Firefox 128. Newest-edge for zero benefit when the palette is 12 fixed colors. | Literal hex in the primitive tier. |
| **CSS nesting** | Changes specificity behaviour subtly and adds a compatibility floor, for a file that already has a flat, consistent, low-specificity structure. | Flat selectors, unchanged. |
| **`outline: none`** anywhere | Would remove the only visible focus indicator. There is currently no `outline` rule at all — **keep it that way** and add a ring rather than removing one. | `:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }` |
| **A CSS reset / Normalize** | Would shift the entire visual baseline of a shipped, working UI, making every screenshot diff unreadable and violating "never visually broken mid-migration." | The existing `* { box-sizing: border-box; }` is sufficient. |
| **An icon font / SVG sprite system** | The audit's finding (2.4) is that emoji (`📌`, `📍`) are *inappropriate* as iconography. The fix is to remove decorative emoji, not to introduce an icon system for a 2-icon problem. | Remove the two `content: '📌 '` / `'📍 '` rules, or replace with a text label. |
| **Dark mode / `prefers-color-scheme`** | Audit finding 4.6 is INFO-severity and explicitly out of this milestone's scope. Adding it doubles the verification surface. | Deferred. Two-tier color tokens leave the door open at zero cost. |
| **Any npm package, bundler, or build step** | Locked by D-06 and the threat model's "any install need is a plan deviation and a stop condition." | `bash run.sh`, unchanged. |

---

## Stack Patterns by Variant

**If the UI-SPEC decides `index.html` markup must change** (e.g. adding `role="dialog"`, `aria-modal`, `aria-live`, or replacing `<h1>文档区</h1>` with a visually-hidden heading):
- Make the ARIA attributes **additive** — never restructure existing elements or IDs.
- `app.js` resolves elements by ID (`getElementById`) throughout; **renaming or moving an ID breaks the app silently.** Adding attributes is safe; restructuring is not.
- Keep `<h1>文档区</h1>` in the DOM for document outline and demote it visually via a class, rather than deleting it — deleting it changes the document outline that screen readers announce.

**If the plan wants to verify contrast in CI:**
- Do not add a package (e.g. `axe-core`, `pa11y`). Write a ~40-line `python3` script that greps `style.css` for `color`/`background` pairs and computes WCAG ratios. The arithmetic is deterministic and the script is the same one used to produce Decision 6.

**If the UI-SPEC wants an opt-in high-contrast mode:**
- Add a second `:root` block inside `@media (prefers-contrast: more)` that re-points **only tier-2 semantic tokens**. Because tier-1 primitives are already there, this is ~10 lines and requires no selector changes.

**If a future milestone adds dark mode:**
- Re-point tier-2 semantic tokens inside `@media (prefers-color-scheme: dark)` and add `color-scheme: light dark` (Chrome 81 / Safari 13 / Firefox 96). Because the two-tier split already exists, this is the *only* block that changes. This is the payoff for Decision 1.

---

## Version Compatibility

| Feature | Chrome | Safari | Firefox | Global usage | Verdict for this project |
|---------|--------|--------|---------|--------------|--------------------------|
| CSS custom properties | 49 | 9.1 | 31 | 96.17% | **Use** — universal |
| `:focus-visible` | 86 | 15.4 | 85 | 94.73% | **Use** — well below floor |
| `prefers-reduced-motion` | 74 | 10.1 | 63 | (interaction mq: 96.35%) | **Use** |
| `prefers-color-scheme` | 76 | 12.1 | 67 | — | Not this milestone |
| `prefers-contrast` | 96 | 14.1 | 101 | — | Optional |
| `color-scheme` property | 81 | 13 | 96 | — | Not this milestone |
| `@layer` | 99 | 15.4 | 97 | 95.3% | **Supported — do not use** (Decision 2) |
| `@property` | 85 | 16.4 | **128** | — | **Do not use** — FF floor too high for the benefit |
| `oklch()` | 111 | 15.4 | 113 | — | Not needed |
| Relative color syntax | 119–125 | **18** | 128 | 85.67% | **Do not use** |
| Media range syntax | 104 | 16.4 | 102 | 94.01% | **Do not use** — no gain over `max-width` |
| CSS nesting | — | — | — | 90.66% | **Do not use** |

**Compatibility conclusion:** the tool runs locally in a current browser on a single machine (D-03). Every feature recommended here has a support floor at least 5 years old. **No feature is recommended at its support edge**, which is deliberate — a local tool with no polyfill pipeline should not be the reason someone has to update their browser.

---

## Verification Gates (zero-install, scriptable)

Two gates that make the token layer self-checking. Both are `grep`/`python3`, both already present.

**Gate 1 — token integrity.** Every `var(--x)` must resolve to a declared `--x`. Catches the silent-`unset` typo class from Decision 3.

```bash
# every referenced token must exist as a declaration
comm -23 \
  <(grep -o 'var(--[a-z0-9-]*' frontend/style.css | sed 's/var(//' | sort -u) \
  <(grep -o '^\s*--[a-z0-9-]*'  frontend/style.css | tr -d ' ' | sort -u)
# expected output: empty
```

**Gate 2 — no new install surface.** The threat model's stop condition, made checkable.

```bash
git status --porcelain frontend/ | grep -v 'style.css\|index.html\|app.js'   # expected: empty
ls frontend/vendor/                                                          # expected: marked.min.js only
```

**Gate 3 — contrast regression.** Re-run the pair scan after every migration step; the count of pairs below 4.5:1 must monotonically decrease to 0.

---

## Correcting a stale premise in the audit

The audit's Top Fix 1 recommends *"add a single global `.hidden { display: none !important; }` rule at the top of `style.css` (and delete the 14 per-selector duplicates)."*

**This was already done** — in commit `b9664e0` (the 5 functional BLOCKER fixes, 2026-09-16). `style.css` line 15 is now exactly:

```css
.hidden { display: none !important; }
```

and it is the **only** `.hidden` rule in the file. There are **no 14 duplicates to delete.** `grep -c "display: none" style.css` returns 2 (the `.hidden` rule and `.panel-body.collapsed`).

The quality gate's framing — "how to keep the existing 14 per-selector rules from fighting the new token layer" — rests on the audit's pre-fix text. **The real cascade constraint is the opposite and simpler:** the token layer must never introduce a rule that sets `display` on an element that can also carry `.hidden`, because `.hidden` currently wins *only* by `!important` at 0-1-0 specificity. Token rules should set custom properties, `color`, `background`, `border`, `font-size`, `padding`, `gap`, and `border-radius` — none of which touch `display`.

---

## Sources

| Source | What it verified | Confidence |
|--------|------------------|------------|
| MDN, `@layer` (last modified 2026-04-20) — Baseline "Widely available" since March 2022 | Cascade-layer ordering rules; the decisive "unlayered always overrides layered" rule; `!important` inversion | HIGH |
| MDN, `var()` (CSS Custom Properties for Cascading Variables L1/L2) | Fallback fires only on guaranteed-invalid; invalid-at-computed-value-time resolves to `unset`, not the fallback; fallbacks are not a compatibility shim | HIGH |
| MDN, *Using CSS custom properties* | `:root` inheritance; **"Variables do not work inside media queries"** | HIGH |
| MDN browser-compat-data (`css/at-rules/property`, `css/at-rules/layer`, `css/properties/custom-property`, `css/selectors/focus-visible`, `css/types/color`, `css/at-rules/media`) | Every version number in the compatibility table | HIGH |
| caniuse feature data (`css-cascade-layers`, `css-focus-visible`, `css-variables`, `css-color-function`, `css-relative-colors`, `css-media-range-syntax`, `css-nesting`) | Global usage percentages; corroborates BCD floors | HIGH |
| W3C WCAG source repo, Understanding docs: `contrast-minimum`, `non-text-contrast`, `reflow`, `text-spacing`, `focus-visible`, `focus-not-obscured-minimum`, `focus-appearance`, `target-size-minimum` | SC 1.4.3 / 1.4.11 / 1.4.10 / 1.4.12 / 2.4.7 / 2.4.11 / 2.4.13 / 2.5.8 thresholds and AA-vs-AAA levels | HIGH |
| **Own arithmetic** over the actual `frontend/style.css` (622 lines, 142 rule blocks, 120 hex occurrences, 34 distinct literals) | The 13 failing pairs; the non-text-contrast failures; every proposed token value | HIGH (deterministic) |
| `frontend/index.html` (218 lines), `frontend/app.js` (1595 lines), `.planning/milestones/v1.13-phases/idi-03-g3/03-UI-REVIEW.md` | Zero JS color coupling; zero inline styles; zero `outline` rules; the audit's findings and its stale `.hidden` premise | HIGH |

**Note on the seam's confidence tier:** `gsd_run query classify-confidence --provider websearch` returns `LOW` (unverified) / `MEDIUM` (verified). That tier is calibrated for *search-engine results*. The findings above come from primary documentation (MDN, MDN browser-compat-data — the machine-readable source caniuse itself derives from — and the W3C WCAG source repository) plus deterministic arithmetic over the project's own file. I am recording them as HIGH on that basis and flagging the divergence rather than silently adopting a tier that does not describe these sources.

---

*Stack research for: zero-dependency CSS design-token + WCAG AA retrofit into an existing vanilla frontend*
*Researched: 2026-09-17*
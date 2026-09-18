# Feature Research

**Domain:** Design-contract + accessibility capabilities for a single-user, local, framework-free web tool
**Project:** 交互式讨论迭代系统 (Interactive Discussion Iteration) — milestone v1.14 前端视觉与可访问性
**Researched:** 2026-09-17
**Confidence:** HIGH for codebase-grounded findings (measured from source); MEDIUM for external best-practice claims (network fetch to w3.org / MDN was blocked in this environment; WCAG and token-architecture guidance below is triangulated from search results + established practice, not primary-source verified)

---

## Scope Framing (read this before the tables)

This milestone adds **no product features**. Its "features" are capabilities applied to an existing surface. Two framings matter for every row below:

**1. The unit of value is not "compliance." It is "the tool stops lying about itself."**
The audit's actual complaints are not abstract standards violations. They are: the most consequential action in the product (irreversible G3 authorization — the project's stated Core Value red line) is visually identical to a routine "继续自检" button; the primary content of the tool (rendered markdown) has its type scale decided by the browser; the text carrying every gate precondition is 2.73:1 contrast; and there is no visible focus anywhere. Each of these is a *usability* defect for the one person using the tool. That is the justification that survives this project's scale.

**2. Measured current state (post-5-blocker-fix, 2026-09-16, `main@b9664e0`):**

| Metric | Measured value | Source |
|--------|----------------|--------|
| CSS custom properties | **0** | `grep -cE '^\s*--[a-z-]+\s*:'` → 0 |
| Distinct hex literal values | **34** | `#fff`×14, `#2e8b57`×12, `#ccc`×11, `#2c7be5`×9, `#c0392b`×8, … |
| `:root` block | none | grep → no match |
| `:focus` / `:focus-visible` rules | **0** | grep → 0 lines |
| `outline` declarations | **0** | grep → 0 lines |
| `@media` rules | **0** | grep → 0 |
| `:hover` / `:active` / `transition` | **2 / 0 / 1** | grep counts |
| Distinct `font-size` values | **7** (13px×15, 12px×6, 14px×5, 12.5px×3, 16px×1, 15px×1, 11px×1) | grep |
| Distinct `font-weight` values | **2** (600×12, 400×1) | grep |
| Distinct padding values | **14** (1,2,4,5,6,8,10,12,14,16,18,28,32,40 px) | grep |
| Distinct margin values | **11** | grep |
| Distinct gap values | **5** (4,6,8,10,12) | grep |
| Distinct border-radius values | **8** (2,3,4,6,8,9,10,12 px) | grep |
| `aria-*` / `role=` in HTML | **0** | grep |
| `.markdown-body h1/h2/h3` `font-size` | **absent** — falls back to UA defaults | `style.css:240` sets only margin + line-height |
| Layout magic number | `#state-badge { right: 448px }` | `style.css:202` |
| `prefers-color-scheme` / `prefers-reduced-motion` | none | grep → 0 |

Note: the earlier audit reported "32 hex literals / 16 padding values." Re-measurement after the 5-blocker fix gives 34 distinct hex values and 14 distinct padding values. Use the measured numbers above.

---

## Feature Landscape

### Table Stakes (This Milestone Must Deliver)

These are the audit's explicitly-deferred items plus the minimum needed to make them stick. Missing any of these = the milestone did not achieve its stated goal ("有设计契约、键盘可用、视觉可信").

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **Semantic color token layer** (`:root` custom properties) | Audit BLOCKER 3.1: zero tokens. Without names, the color problem is not fixable — you cannot rationalize "green means 7 things" without a vocabulary to say what each thing is. | MEDIUM | **Single tier, semantically named.** See "Token Architecture Decision" below. Target ~18–24 tokens. Zero build step (CSS custom properties are native). |
| **Collapse 4 competing accent families → primary / danger / neutral** | Audit BLOCKER 3.2: green (12 declarations) outranks nominal-primary blue (9). No dominant accent exists. | MEDIUM | Requires an explicit meaning inventory *first* (the design decision this milestone exists to make). See "Meaning Inventory" below. |
| **Irreversible-action visual weight for `#btn-authorize`** | Audit BLOCKER 3.3 + PROJECT.md Core Value. The G3 authorization is the one action the whole product is organized around; it currently shares `background:#e9f7ef; border/color:#2e8b57` with 5 routine buttons including 「继续自检」. | LOW | Highest value-per-line in the milestone. Fix: solid fill + a distinct reserved token (e.g. `--color-irreversible-*`), not the pale tint. Apply to `#btn-approve-draft` (G1, also irreversible) and `#btn-start-writing` as a second tier; leave routine actions neutral. |
| **Controlled type scale for UI chrome** | Audit 4.1/4.2: 7 flat sizes, 13px is the default for essentially everything, fractional 12.5px ×3. | LOW | 5–6 sizes, ratio 1.125–1.25. Recommended set: 11 / 12 / 13 / 15 / 18 / 22 px (ratio ~1.2 on the upper steps). Delete 12.5px and 14px. |
| **Explicit type scale for `.markdown-body` headings** | Audit BLOCKER 4.3: the primary content of the entire tool has **no** `font-size` rule; h1/h2/h3 fall back to UA defaults (28/21/16.4px against a 14px body). The most-read text in the product is styled by the browser. | LOW | `style.css:240` currently sets only `margin` + `line-height`. Add explicit `font-size` for h1/h2/h3 (+ h4 if it can appear in AI-written markdown). |
| **Page-level hierarchy** | Audit 2.1/4.5: the largest, boldest text on screen is `<h1>文档区</h1>` at UA-default ~32px — a container label outranking all actual content. | LOW | Either demote to a visually-styled small label or restyle. Also check heading order sanity (h1 → h2 → h3) since AI-generated markdown contributes headings. |
| **WCAG AA contrast compliance on the 4 known failures** | Audit 3.5, measured: `.hint` `#999`/`#fafafa` = **2.73:1** (pervasive — every gate precondition and recovery instruction); `#pending-count` + `.badge-pending` `#b8860b`/`#fdf6ec` = **3.03:1**; `.event-kind` white/`#b8860b` = **3.25:1**; `.chat-user` white/`#2c7be5` = **4.14:1**. AA requires 4.5:1 for normal text. | LOW | **The `.hint` fix is the single highest-value a11y change in this milestone** — it is legibility for the actual reader, not compliance theater. Fixing it once via a token also fixes it everywhere. |
| **Focus visibility across the whole surface** | Audit BLOCKER-adjacent 6.4: `grep :focus` = 0. Tabbing through 21 buttons / 8 inputs / 4 selects shows nothing. | LOW | `:focus-visible` rules. See "Focus Strategy" below for the two real tradeoffs. |
| **Keyboard reachability verification** | Audit 6.1 (keyboard path to the flagship annotation feature) was fixed 2026-09-16. The risk now is regression and undiscovered gaps elsewhere. | LOW | Verify tab order reaches every interactive control; verify the `#selection-menu` keyboard path still works (note: **not automatable** — PROJECT.md records that keyboard text selection cannot be driven by Playwright, even with `contenteditable`; mark as manual UAT). |
| **Interaction state coverage** (`:hover` / `:active` / `:disabled` / transition) | Audit 6.9: 2 hover rules, 0 active, 1 transition in 631 lines. Buttons give no pressed feedback. | LOW | Keep transitions to `background-color`/`border-color`/`opacity` at ~120–150ms. Do **not** build a motion system. |
| **Layout magic number removed** | Audit BLOCKER 5.1: `#state-badge { right: 448px }` is hardcoded to sidebar 420 + 28, arithmetic recorded only in a comment. The badge is `position:fixed` and does not scroll, so content scrolls underneath it. | MEDIUM | Entangled with the sidebar-width decision and the narrow-window requirement — treat as **one unit of work**, not three. Also see WCAG 2.2 2.4.11 note under Focus Strategy. |
| **Narrow-window robustness (no broken layout when the developer resizes)** | Audit 5.3: zero `@media`, `#sidebar { flex: 0 0 420px }` overflows at small widths. | MEDIUM | Scoped to "does not break", **not** "adapts". See Anti-Features: mobile/responsive system is out of scope. Concrete target: no horizontal overflow at ≥1024px; no content occlusion at ≥768px. |
| **Panel active/inactive differentiation** | Audit 2.2: four `.panel-header` blocks share one identical treatment; nothing signals which panel is live. | LOW | A left-accent or weight change on the active panel. Cheap; directly addresses "no focal point on the main screen." |
| **Markdown content typography polish** | Audit 4.x: `table th/td` at 13px vs body 14px; `code` at 12.5px fractional; blockquote at `#666`. | LOW | Falls out of the type scale + tokens; no separate design decision. |
| **Spacing scale** | Audit 5.2/5.5: 14 distinct padding values, 11 margins, 5 gaps, no scale. | MEDIUM | 4px base: 4 / 8 / 12 / 16 / 24 / 32 / 40. **Honest caveat:** this is the lowest-urgency table-stakes item. Nothing is *broken* by ad-hoc spacing; the cost is future drift. Do it because tokens make it nearly free, not because it fixes a defect. |
| **Radius scale** | Audit 2.6/5.5: 8 distinct radii (2,3,4,6,8,9,10,12). | LOW | 3 values: `--radius-sm` 4px (controls), `--radius-md` 6–8px (cards/menus), `--radius-pill` (badges). Near-zero cost once tokens exist. |

### Differentiators (What Makes the Contract Enforceable Rather Than Just Applied)

The honest reframing: at this scale the "differentiator" tier is not extra polish. It is the difference between a one-time cleanup and a contract that holds.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **A written design contract (`UI-SPEC.md`)** | The audit's root finding is that 2435 lines of UI shipped with *zero* contract — for a tool whose stated value is "无歧义对齐". Without a written contract, this milestone is a refactor and the same drift recurs. This is also literally the artifact the next step produces. | LOW | Should record: the token list, the meaning inventory, the type scale, the radius/spacing scales, and the focus/interaction state rules. Should **not** re-specify product behavior (DESIGN.md §4 owns that). |
| **Machine-checkable token conformance** | Turns "we use tokens" from an intention into a test. A ~20-line Node/Python script that greps `style.css` for raw `#hex` outside the `:root` block fails the build on regression. | LOW | This is the single cheapest mechanism that makes every other item in this document durable. Phrase as a testable requirement: "`style.css` contains zero hex literals outside the `:root` token block." |
| **Automated contrast verification for token pairs** | The 4 known AA failures will silently return the next time someone tweaks a token. A script computing contrast ratios over the declared token pairs catches it at edit time. | LOW | No dependency needed — WCAG relative-luminance is ~15 lines. Also makes the a11y claim verifiable rather than asserted. |
| **Token layer shaped for a future dark mode** | Costs nothing today, saves a rewrite later. Constraint on *how* tokens are written, not a feature: no `#fff`/`#1a1a1a` outside the token block; every background/surface expressed via a semantic name. | LOW | This is the pragmatic middle between "single tier" and "two tier" — see Token Architecture Decision. |

### Anti-Features (Commonly Requested, Explicitly Decline)

| Anti-Feature | Why Requested | Why Problematic Here | Alternative |
|--------------|---------------|----------------------|-------------|
| **Dark mode / `prefers-color-scheme`** | "Design tokens, may as well add theming"; every design-system article leads here | It is a **new feature**, and this milestone's charter is explicitly no new features. It is also the main thing that would justify the primitive token tier this project doesn't otherwise need. It doubles the contrast-verification surface (every AA fix verified twice) for a milestone whose entire point is closing 4 known failures. Zero evidence of demand: one user, short-session tool, no current `prefers-color-scheme` anywhere. | Defer to its own milestone. **But** write this milestone's tokens so dark mode is a later `@media (prefers-color-scheme: dark)` block that only reassigns existing semantic names — no structural change. |
| **Full primitive→semantic two-tier token system** | It is the canonical design-tokens architecture | The second tier earns its keep when you need to **remap raw values across contexts** — themes, brands, white-label. This project has exactly one theme and one user. Two tiers here doubles token count and adds indirection for zero remapping benefit. See Token Architecture Decision. | **Single tier of semantically-named tokens.** Migrating 1→2 tiers later is straightforward; unwinding an unnecessary 2-tier setup is the annoying direction. |
| **Component-level token tier** (`--button-primary-bg`, `--card-border`, …) | "Three-tier is the mature model" | Third tier. Requires a component system to pay off. There is no component system — there is one 631-line stylesheet and no framework. Pure bookkeeping. | Semantic tokens consumed directly by selectors. |
| **CSS framework / Tailwind / PostCSS / any build step** | Tokens + scales often arrive bundled with a toolchain | **Violates a hard project constraint** (D-06: 原生 HTML/JS + markdown 渲染库; no framework). Tokens as CSS custom properties need zero build — this is the whole point of using them here. | Hand-written `:root` block in `style.css`. |
| **Stylelint / lint pipeline** | "Enforce the token rule properly" | A toolchain, config file, and CI wiring for a 631-line stylesheet with no existing build. | The ~20-line conformance script above. Same guarantee, no dependency. |
| **Full ARIA / screen-reader conformance** (`aria-live` on streaming chat, `role="dialog"` + `aria-modal` + focus trap on all 4 modals, `aria-describedby` wiring) | It is the standard a11y checklist | **This is the item the scale question is really about.** ARIA exists to serve users who arrive without context and cannot see the screen. This app has exactly one user, who is also the author, who sees the screen. Cost is real (focus management in vanilla JS is fiddly and easy to get subtly wrong); benefit accrues to nobody who exists. | Decline wholesale, with two exceptions that survive on *safety* rather than *accessibility* grounds: (a) **Escape-to-close on the two blocking/safety modals** — the G3 confirm modal is default-deny by design, and a keyboard user who can't dismiss a modal is stuck; (b) `role="dialog"` + `aria-modal="true"` on the same two modals, because it is two attributes and zero risk. Revisit the whole category if the user ever adopts a screen reader. |
| **Focus trap implementation** | Standard modal practice | Without a trap, tabbing from a modal reaches background controls — mildly confusing, not harmful, since the background is visually occluded. Implementing a correct trap (including Shift+Tab wraparound and dynamic content) is real vanilla-JS work for a single-user mouse-driven tool. | Skip. Do Escape-to-close instead (above). |
| **Responsive / mobile layout, breakpoint system** | Audit 5.3 flags zero `@media` | The audit's finding is *technically* correct and *practically* irrelevant: this is a single-user local desktop tool, run on the developer's own machine. A breakpoint system is a feature. | **Split the finding honestly.** "Narrow window doesn't break" is table stakes (above). "Layout adapts to phone widths" is out of scope. One `@media` guard for the sidebar/`#state-badge` coupling, not a system. |
| **Icon library / SVG sprite system** | Audit 2.4: emoji (`📌`, `📍`) used as iconography via CSS `content`, renders inconsistently | Two emoji. A sprite system, an icon font, or a vendored icon set is enormous overhead for two glyphs — and vendoring a library is the only option given no CDN (no-network constraint). | Pick one: (a) accept the emoji and document it as a deliberate choice, or (b) replace each with a single inline SVG defined once and referenced. Do not build an icon system. |
| **Skeleton loaders / spinners / progress indication** | Audit 6 lists "no spinner/skeleton" as missing | This is a **new product feature**, out of charter. Also already partly addressed: buttons have text-swap states (`撰写中…`, `处理中…`). | Out of scope for v1.14. |
| **Motion / animation design system** | "Interaction states need transitions" | The app has **1** transition in 631 lines. A motion system is absurd here. | 120–150ms `background-color`/`opacity` transitions on interactive controls. That's the whole spec. |
| **Storybook / component gallery** | "How do you review the design system?" | No components, no framework, no build. | Open the app. It is a single-user local tool; the review surface *is* the product. |
| **Restyling `#probe-controls` dev scaffolding** | Audit 6.6: internal A/B route switch + duplicate path input shipped in the primary UI | Tempting because it's ugly. But removing/relocating it is a **product/behavior change**, not a design-contract change, and the two-route contract is a real feature (AI-03/D-06). | Flag to the roadmap as a candidate for a separate item. Do not fold into a visual-contract milestone — it would expand scope and touch `app.js` behavior. |

---

## Low-Value-But-Real (flag honestly, do not pad)

Items that are genuinely true findings but whose value at single-user-local scale is low. Include only if they are nearly free; do not let them displace P1 work.

| Item | Why It's Real | Why It's Low-Value Here | Recommendation |
|------|---------------|-------------------------|----------------|
| `aria-live` on the streaming chat / event panel | Audit 6.5. Screen readers get no announcement of streamed content. | The one user sees the bubbles appear. Benefit accrues to a hypothetical SR user. | Skip. |
| `prefers-reduced-motion` handling | Audit 4.6. No reduced-motion support exists. | Currently **moot** — there is exactly 1 transition. | Skip *now*. Note the dependency: if the interaction-states work adds transitions, this becomes newly relevant and should be a 3-line guard. |
| WCAG 2.2 **2.5.8 Target Size (Minimum)** — 24×24 CSS px (AA) | `.verdict-buttons button` (`font-size: 12.5px; padding: 4px 10px`, `style.css:624`) computes to roughly 21–22px tall; `#selection-menu` buttons are similarly tight. | Real for a mouse user but rarely blocking — and the verdict buttons are deliberately compact to fit 3 buttons in a 420px sidebar. | Cheap enough to fold into the interaction-states work if it doesn't fight the layout. Do not restructure the sidebar for it. |
| WCAG 2.2 **2.4.11 Focus Not Obscured (Minimum)** (AA) | `#state-badge` is `position: fixed`, `z-index: 10`, opaque background, and **does not scroll** — a focused element scrolled beneath it is obscured. This is a concrete AA failure, not a hypothetical. | Single user, and the badge sits in a corner where controls rarely land. | Fold into the magic-number fix — it's the same code path, and the criterion is satisfied for free once the badge stops being absolutely pinned over content. |
| Heading-order sanity across AI-generated markdown | AI writes `discuss-round-N.md`; nothing constrains its heading levels. | No user impact for a sighted single user; only matters for SR outline navigation. | Skip beyond the explicit `font-size` fix. |
| 8 distinct border-radii | Audit 2.6 calls them "visually coherent but ad hoc." | The audit itself says they're coherent. | Fold into the radius scale since it's near-free. |

---

## Four Decisions This Milestone Must Make Explicitly

### Decision 1: Token architecture — single tier, not two

**Recommendation: single tier of semantically-named tokens. No primitive layer.**

Grounded rationale (triangulated from Smashing Magazine, CSS-Tricks, learnwithjason.dev, thedesignsystem.guide — see Sources): two-tier earns its keep when you need to **remap raw values across contexts** — dark mode, multiple brands, white-label. This project has one theme, one brand (none), one user, one 631-line stylesheet, and a hard no-build constraint.

The decisive observation: **this project's color problem is semantic, not primitive.** The audit's complaint is "green means 7 different things," not "the same hex is written 12 times." A primitive palette (`--green-600: #2e8b57`) does not fix that. A semantic vocabulary (`--color-action-routine` vs `--color-action-irreversible`) does. The primitive tier would be pure bookkeeping.

**Target shape:**
```css
:root {
  /* surfaces & text */
  --color-bg, --color-surface, --color-border, --color-border-subtle
  --color-text, --color-text-muted, --color-text-inverse
  /* actions */
  --color-action-primary, --color-action-primary-hover
  --color-action-routine, --color-action-irreversible
  --color-danger, --color-danger-surface
  /* status */
  --color-pending, --color-success
  /* event kinds (a bounded, closed set — see note) */
  --color-kind-say, --color-kind-read, --color-kind-write,
  --color-kind-command, --color-kind-result, --color-kind-error, --color-kind-done
  /* scales */
  --space-*, --text-*, --radius-*
}
```

**Honest caveat on the event-kind palette:** audit 3.6 flags a separate 7-color ad-hoc palette for event kinds (blue/purple/green/ochre/grey/red/black) that overlaps but does not align with the UI accents — green means both "写文件 event" and "positive button." These are two genuinely different vocabularies (a categorical set vs. a semantic accent set) and should **not** be forced into one. Tokenize the event-kind set as its own named group so the overlap becomes explicit and intentional rather than accidental. Do not try to unify them.

### Decision 2: Meaning inventory before tokens

The token layer is a *symptom fix* if it isn't preceded by deciding what each color means. The audit found green carrying seven meanings. Required output: an explicit list mapping each semantic role → one token → the buttons/elements that use it. Specifically resolve:

- Is `#btn-approve-draft` (G1, irreversible) in the same tier as `#btn-authorize` (G3, irreversible)? Both are irreversible; both are gates. Recommended: yes — one `--color-action-irreversible`, both solid-fill.
- Are `#btn-process-round`, `#btn-continue-check`, `#btn-continue-repair`, `#btn-start-writing` routine? Recommended: yes — routine/neutral treatment. Note `#btn-start-writing` is arguably a gate too; decide explicitly rather than by inheritance.
- Do `#state-badge` (`#2c5fb8`) and `.primary`/`.chat-user` (`#2c7be5`) collapse to one blue? Audit 3.4 flags the two near-identical blues with no documented distinction. Recommended: collapse — the 4% difference carries no meaning.

This is the design decision the milestone defers on, and it is a **prerequisite**, not a parallel task.

### Decision 3: Focus strategy — `:focus-visible`, with two real tradeoffs

**Recommendation: `:focus-visible` as the primary mechanism.** It is broadly supported in all evergreen browsers and solves the exact dilemma that produced this project's `grep :focus` = 0: `:focus` rings on every mouse click, which is annoying, which is why people delete outlines, which is how you end up with zero focus styles.

Two tradeoffs worth naming explicitly:

1. **Never `outline: none` without a replacement.** The app currently has zero `outline` declarations, so this is a *future* risk: the first person to find a focus ring ugly will delete it. Write the rule and put it in the contract.
2. **Rings on rounded elements look broken flush.** The app uses `border-radius` 4–12px on nearly every control. Use `outline-offset: 2px` so the ring follows the element shape rather than cutting into it. This is a real, visible difference, not a nicety.
3. **Clipping is the live risk here, and it is concrete.** The app has up to four nested scroll containers (`.event-list`, `#chat-messages`, `#annotation-list`, `#latest-check`). Scroll containers clip. Focus rings on items inside them can be cut off, and `#state-badge` (fixed, opaque, `z-index: 10`, doesn't scroll) can obscure a focused element entirely — which is WCAG 2.2 **2.4.11 Focus Not Obscured (Minimum)**, an AA criterion. Both are resolved by the same layout work as the magic-number fix. Do the focus audit *after* the layout fix, not before, or you will verify a state that no longer exists.

Fallback pattern for older browsers, if wanted: `:focus { outline: 2px solid var(--color-focus); }` followed by `:focus:not(:focus-visible) { outline: none; }`. Probably unnecessary given the single-user-local context (the user's own browser is known), but it is one line.

### Decision 4: Dark mode — separate milestone, but shape the tokens for it

**Recommendation: out of scope for v1.14. Defer to its own milestone.**

Five reasons: (1) it is a new feature and the charter excludes new features; (2) it is the primary thing that would force the two-tier architecture this project doesn't otherwise need; (3) it doubles contrast-verification work — every AA fix must be verified in two contexts — for a milestone whose entire purpose is closing 4 known contrast failures; (4) there is no evidence of demand (one user, short-session daylight workflow, no existing `prefers-color-scheme`); (5) it would expand the file-touch surface of an already whole-file refactor.

**But** — this is the one place the two-tier question has a real answer. The migration 1→2 tiers is cheap *if* the single tier is written correctly. So impose this constraint on v1.14's token output: **no literal color outside the `:root` block, and every background/surface/foreground expressed through a semantic name.** Then a future dark mode is a single `@media (prefers-color-scheme: dark)` block that reassigns the same names. That is the pragmatic middle, and it costs nothing today.

---

## Feature Dependencies

```
Meaning Inventory (what each color means)
    └──requires──> Semantic Color Token Layer
                        ├──requires──> Contrast Compliance (AA)
                        │                  └──requires──> Contrast Verification Script
                        ├──requires──> Irreversible-Action Weight
                        ├──requires──> Interaction States (hover/active colors must be tokens)
                        └──shapes────> Dark Mode (future milestone; needs only a token reassignment)

Type Scale (UI chrome)
    └──enables──> Markdown Content Type Scale
    └──enables──> Page-Level Hierarchy (the <h1>文档区</h1> demotion is a type-scale decision)

Layout Unit of Work  ══ ONE UNIT, NOT THREE ══
    #state-badge magic number
    + Sidebar width decision
    + Narrow-window robustness
    + WCAG 2.2 2.4.11 Focus Not Obscured (same code path)

Focus Visibility
    ├──requires──> Layout Unit of Work  (verify AFTER layout, or you verify a stale state)
    └──requires──> Overflow/Clipping Audit of the 4 nested scroll containers

Interaction States
    ├──requires──> Semantic Color Token Layer
    └──enables────> prefers-reduced-motion guard (only becomes relevant once transitions exist)

Token Conformance Script
    └──requires──> Semantic Color Token Layer (nothing to check before it exists)

Spacing Scale ──independent──> Radius Scale
    (both are near-free once the :root block exists; neither blocks anything)
```

### Dependency Notes

- **Meaning Inventory requires nothing but is required by everything color-related.** It is a design decision, not code. Doing the token refactor before it produces a well-named version of the same confusion.
- **Contrast compliance requires tokens.** Fixing the 4 failing hex values directly works for a day; the next token tweak silently regresses them. Fix via tokens + a verification script.
- **Layout is one unit.** The magic number, the sidebar width, narrow-window behavior, and 2.4.11 all touch the same declarations. Splitting them across phases guarantees rework.
- **Focus verification must follow layout.** `#state-badge` is `position: fixed` over scrollable content; verifying focus rings before the layout fix validates a state that is about to change.
- **Interaction states enable reduced-motion.** Currently moot (1 transition). The dependency only appears if this work adds transitions.
- **Token conformance script depends on the token layer.** Trivially true, but it means the script lands in the same phase or later — never earlier.
- **Spacing and radius scales are independent and unblocking.** They can go anywhere. Honest framing: they are the lowest-urgency items in the table.

### Conflicts

- **"No hardcoded hex outside tokens" conflicts with "surgical changes."** Eliminating 34 hex literals touches nearly every rule in a 631-line stylesheet. This is a whole-file rewrite wearing a refactor's clothing. Name it as such in the roadmap — it is the milestone's main execution risk, and its review surface is the entire CSS file, not a diff.
- **Adding `@media` for narrow windows conflicts with the "no responsive system" anti-feature.** Must stay scoped to "does not break", with one guard, not a breakpoint ladder.
- **Irreversible-action weight conflicts with the existing green-family convention.** Six buttons currently share one treatment. Differentiating them is a visible change across the app; expect it to read as "different" before it reads as "better."

---

## MVP Definition

### Launch With (v1.14 — P1)

- [ ] **Meaning inventory + semantic color token layer** — the prerequisite; everything else depends on it
- [ ] **Irreversible-action visual weight** — Core Value red line; highest value-per-line
- [ ] **WCAG AA contrast fixes via tokens** — `.hint` at 2.73:1 is the worst and the most pervasive
- [ ] **`:focus-visible` across the whole surface** — "keyboard usable" is in the milestone goal
- [ ] **Markdown content type scale** — the primary content of the tool is currently browser-styled
- [ ] **Type scale for UI chrome** — kills 7 flat sizes and fractional 12.5px
- [ ] **Layout unit** (magic number + sidebar + narrow-window + 2.4.11) — one unit, or it gets redone
- [ ] **Written `UI-SPEC.md`** — without it this is a refactor, not a contract

### Add After Validation (v1.14.x)

- [ ] **Token conformance script** — trigger: the token layer exists and is stable
- [ ] **Contrast verification script** — trigger: the token set is final
- [ ] **Spacing scale** — trigger: tokens exist; near-free
- [ ] **Radius scale** — trigger: tokens exist; near-free
- [ ] **Interaction states** (`:hover`/`:active`/`transition`) — trigger: token hover/active values decided
- [ ] **Panel active/inactive differentiation** — trigger: type scale + tokens landed
- [ ] **Emoji iconography decision** (accept-and-document, or one inline SVG) — trigger: color work complete

### Future Consideration (v2+)

- [ ] **Dark mode** — defer; own milestone; only needs a token reassignment *if* v1.14's tokens are written dark-ready
- [ ] **Full ARIA / screen-reader conformance** — defer indefinitely; revisit only if the user adopts a screen reader
- [ ] **Focus trap on modals** — defer; Escape-to-close is the narrow slice that survives
- [ ] **`#probe-controls` relocation** — defer; it is a product/behavior change, not a design-contract change
- [ ] **Loading/progress indication** — defer; new product feature, out of charter

---

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Meaning inventory | HIGH (unblocks all color work) | LOW | **P1** |
| Semantic color token layer | HIGH | MEDIUM | **P1** |
| Irreversible-action visual weight | HIGH (Core Value) | LOW | **P1** |
| AA contrast fixes (via tokens) | HIGH (legibility for the actual reader) | LOW | **P1** |
| `:focus-visible` rules | HIGH (milestone goal says "键盘可用") | LOW | **P1** |
| Markdown content type scale | HIGH (primary content) | LOW | **P1** |
| UI type scale | MEDIUM-HIGH | LOW | **P1** |
| Layout unit (magic number / sidebar / narrow window / 2.4.11) | MEDIUM-HIGH | MEDIUM | **P1** |
| `UI-SPEC.md` written contract | HIGH (makes the rest durable) | LOW | **P1** |
| Page-level hierarchy (`<h1>文档区</h1>`) | MEDIUM | LOW | P2 |
| Token conformance script | MEDIUM (durability) | LOW | P2 |
| Contrast verification script | MEDIUM (durability) | LOW | P2 |
| Interaction states | MEDIUM | LOW | P2 |
| Panel active/inactive differentiation | MEDIUM | LOW | P2 |
| Spacing scale | LOW-MEDIUM | MEDIUM | P2 |
| Radius scale | LOW | LOW | P2 |
| Markdown typography polish (table/code/blockquote) | LOW-MEDIUM | LOW | P2 |
| Emoji iconography replacement | LOW | LOW | P3 |
| Escape-to-close + `role="dialog"` on 2 safety modals | LOW | LOW | P3 |
| WCAG 2.5.8 target size (verdict buttons) | LOW | LOW | P3 |
| `prefers-reduced-motion` guard | LOW (moot until transitions exist) | LOW | P3 |
| `aria-live` on streaming chat | LOW (no SR user) | LOW | **Decline** |
| Focus trap | LOW | MEDIUM | **Decline** |
| Dark mode | MEDIUM (but no demand) | HIGH | **Defer to own milestone** |
| Primitive token tier | NONE | MEDIUM | **Decline** |
| Component token tier | NONE | MEDIUM | **Decline** |
| Responsive/mobile system | NONE (desktop-local tool) | MEDIUM | **Decline** |
| Icon library | NONE (2 emoji) | MEDIUM | **Decline** |
| CSS framework / build step | NONE | HIGH | **Decline (violates D-06)** |

**Priority key:** P1 = must have for this milestone to meet its stated goal · P2 = should have, add when the P1 work is stable · P3 = nice to have · Decline/Defer = explicitly not in this milestone.

---

## How to Phrase These as Testable Requirements

The downstream UI-SPEC author and roadmap planner need requirements that can be verified, not adjectives. Concrete phrasing patterns:

| Capability | Testable requirement phrasing |
|------------|-------------------------------|
| Token layer | `style.css` declares ≥18 CSS custom properties in a single `:root` block covering color, space, type, and radius. |
| No raw values | `style.css` contains **zero** hex literals outside the `:root` block. (Machine-checkable.) |
| Meaning collapse | The number of distinct semantic action tokens is ≤3 (`primary` / `routine` / `irreversible`), and each is used by a documented set of selectors. |
| Irreversible weight | `#btn-authorize` and `#btn-approve-draft` render with a solid fill that is visually distinct from every routine action button; `#btn-continue-check` and `#btn-process-round` do **not** use the irreversible token. |
| Contrast | Every foreground/background token pair used for normal-size text meets ≥4.5:1; every UI-component boundary and graphical object meets ≥3:1. Verified by script, not by eye. |
| Type scale | The number of distinct `font-size` values in `style.css` is ≤6, all integers, all drawn from the declared scale. (Currently 7, including 12.5px.) |
| Markdown type scale | `.markdown-body h1/h2/h3` each declare an explicit `font-size` from the scale. (Currently none.) |
| Focus | Every interactive element (`button`, `input`, `select`, `summary`, `[tabindex]`) has a visible focus indicator with `outline-offset` ≥1px; zero `outline: none` declarations exist without a replacement. |
| Keyboard | All interactive controls are reachable by Tab in a DOM order matching visual order. The selection-menu keyboard path (fixed 2026-09-16) still works. **Manual UAT — not automatable.** |
| Layout | No horizontal overflow at viewport widths ≥1024px; `#state-badge` position derives from the sidebar width (no literal px offset coupled to it in a comment); no focused element is fully occluded by author content (WCAG 2.2 2.4.11). |
| Interaction states | Every `button` has distinct `:hover`, `:active`, and `:disabled` treatments; transitions are limited to `background-color`/`border-color`/`opacity` at ≤200ms. |
| Contract exists | `UI-SPEC.md` exists and enumerates the token list, the meaning inventory, the type/space/radius scales, and the focus rules. |

---

## Competitor / Reference Feature Analysis

"Competitors" here = how comparable projects handle the same decisions. Used as calibration, not as a template to copy.

| Decision | Tailwind CSS | shadcn/ui (Radix) | GitHub Primer | **Our approach** |
|----------|--------------|-------------------|---------------|------------------|
| Token tiers | Two-tier: raw palette (`blue-500`) + semantic config | Two-tier via CSS vars (`--primary`, `--background`) + Tailwind config | Three-tier: base / semantic / component | **Single semantic tier.** We have one theme; the second tier has nothing to remap. |
| Dark mode | First-class, drives the whole architecture | Built-in via CSS vars in `.dark` | First-class | **Deferred.** Tokens shaped so it's a later var reassignment, not a restructure. |
| Build step | Requires PostCSS + config | Requires React + Tailwind | Sass pipeline | **None.** Native CSS custom properties; hard constraint D-06. |
| Focus | Ships `focus-visible` ring utilities + `outline-offset` | Radix handles focus management in JS | `focus-visible` + `outline-offset` | **`:focus-visible` + `outline-offset: 2px`.** Explicitly no JS focus management. |
| A11y depth | Author's responsibility | Deep: ARIA, focus trap, roving tabindex, SR announcements | Deep | **Minimal.** One user, sighted, author. Escape-to-close + `role="dialog"` on 2 safety modals only. |
| Type scale | Configurable scale | Consumer's choice | Defined scale | **5–6 sizes, ratio 1.125–1.25.** Kills the 7 flat sizes and the fractional 12.5px. |
| Where it would be overkill here | The whole framework + build chain | The whole component + ARIA system | The Sass pipeline + 3 tiers | — |

The pattern across all three: they are built for **many users, many themes, many contributors, and a build pipeline.** This project has none of those. Take the *vocabulary* (semantic names, scales, `focus-visible`), leave the *machinery*.

---

## Sources

**Codebase (primary, HIGH confidence — measured directly):**
- `/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/frontend/style.css` (631 lines) — all counts above measured from this file
- `/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/frontend/index.html` (221 lines)
- `/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.planning/milestones/v1.13-phases/idi-03-g3/03-UI-REVIEW.md` — six-pillar audit, 13/24, 7 BLOCKERs
- `/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.planning/PROJECT.md` — Core Value, constraints, UAT environment facts
- `/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.planning/REQUIREMENTS.md` — v1.13 requirement set and Out-of-Scope table

**External (MEDIUM confidence — search-result summaries; direct fetch to w3.org and developer.mozilla.org was blocked by network policy in this environment):**
- WCAG 2.2 focus guidance, `:focus-visible` best practices, `outline-offset`, fallback patterns — via search results referencing MDN, W3C WCAG 2.2 SC 2.4.7 / 2.4.11 / 2.4.13, WebAIM, Sara Soueidan
- Design token tiering — Smashing Magazine ("Design Tokens: Primitive vs Semantic — When Two Tiers Is Over-Engineering"), CSS-Tricks ("Primitive vs Semantic Design Tokens"), learnwithjason.dev ("Stop Over-Engineering Your Design Tokens — Use One Tier"), thedesignsystem.guide ("When to Use Single-Tier vs Two-Tier Design Tokens"), Contentful ("Design Tokens 101")
- Type scale ratios — modularscale.com, typescale.com, Figma "Design Systems: Typography" best practices, UX Collective / Bootcamp on type-scale ratio selection for small apps

**Not verified in this session (treat as needing phase-specific confirmation):**
- Exact WCAG 2.2 AA criterion numbering and thresholds (2.4.11, 2.5.8, 3.2.6, 3.3.7, 3.3.8) — stated from established practice, not fetched from w3.org. The *substance* (focus not obscured; 24×24 target size; contrast 4.5:1 / 3:1) is stable and widely reported; verify exact numbering before writing it into a contract.

---

*Feature research for: design-contract and accessibility milestone on a single-user, local, framework-free web tool*
*Researched: 2026-09-17*
*Scope: v1.14 前端视觉与可访问性 — no new product features*
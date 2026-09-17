# Project Research Summary

**Project:** 交互式讨论迭代系统(Interactive Discussion Iteration)
**Domain:** 本地单机 Web 工具 — 前端设计契约 / CSS 令牌体系 / 可访问性(原生 HTML/JS,无框架、无构建步骤)
**Researched:** 2026-09-17
**Confidence:** HIGH(栈 / 架构 / 陷阱);MEDIUM(功能范围中的外部最佳实践;两处开放决策属价值观问题,非知识缺口)

## Executive Summary

This milestone adds **no product features, no dependencies, and no new frontend files.** It retrofits a design contract onto a 631-line stylesheet that grew without one. The "stack decision" is not *which packages* — it is **which CSS mechanisms to use and which to refuse.** The answer: one `:root` block of native custom properties at the top of `frontend/style.css`, mechanical literal→`var()` substitution below it, purely-additive rules for focus/interaction/reflow. Three modern-sounding features are explicitly refused because they make this retrofit worse: `@layer` (all 631 existing lines are unlayered, so layers would be inert or require a full-file rewrite, and layering inverts `!important` ordering — endangering the one global rule 44 `classList` calls depend on), `@property` (Firefox floor three years behind), and `var(--x, #fallback)` (does not work as a safety net; destroys the grep-ability that is this migration's only verification). **Four of six scope areas are a `style.css`-only change** — `app.js` writes zero color/spacing/type values, `index.html` has zero inline styles.

The real justification is not compliance. It is that **the tool currently lies about itself.** The most consequential action in the product — irreversible G3 authorization, the stated Core Value red line — is byte-identical in styling to the routine 「继续自检」 button. The primary content (rendered markdown) has its type scale decided by the browser (`.markdown-body h1/h2/h3` have no `font-size` rule at all). The text carrying every gate precondition renders at 2.73:1. There is no visible focus anywhere. Each is a usability defect for the one person who uses the tool.

**The dominant risk is not bad CSS — it is a CSS change silently reverting a JS-level guarantee.** Five functional BLOCKERs shipped 2026-09-16 (`b9664e0`), every one load-bearing on CSS this milestone rewrites, verified by grep counts plus manual checks and **not by automation**. All four researchers independently flagged the `.hidden { display: none !important }` rule as a 5-way single point of failure. The highest-value guard for the whole milestone is one command, in every plan that edits `style.css`: `grep -c '^\.hidden {' frontend/style.css` must return `1`.

---

## Key Findings

### Recommended Stack

**Zero dependencies. Zero new files. One insertion point.**

| Technology | Purpose | Why |
|---|---|---|
| CSS custom properties | The token substrate | Chrome 49 / Safari 9.1 / Firefox 31. **Cascade-neutral**: substituting `var(--x)` for a literal does not change specificity, source order, or computed value — this is why the migration is incremental-safe where a class-rename would not be. |
| `:focus-visible` | Keyboard-only focus ring | Satisfies 2.4.7 without ringing every mouse click. |
| `@media (max-width: …)` | Narrow-window reflow | 1.4.10 requires no 2-D scrolling at 320 CSS px; `#sidebar { flex: 0 0 420px }` violates this outright. |
| `@media (prefers-reduced-motion: reduce)` | Neutralize transitions | Zero cost — the file has exactly **1** `transition`. |
| `@media (prefers-contrast: more)` | Opt-in high-contrast | Optional, ~10 lines once tier-2 tokens exist. |

**Refused, with reasons:** `@layer`, `@property`, `var(--x, #fallback)`, relative color syntax, CSS nesting, media range syntax, `outline: none`, any CSS reset, any icon font/sprite system, dark mode, and any npm package / bundler / build step.

**Toolchain:** DevTools + `grep` + `python3`. Three zero-install gates carry through every `style.css` plan: (1) token integrity — every `var(--x)` resolves to a declared `--x`; (2) no new install surface — `git status --porcelain frontend/` shows only the three known files, `frontend/vendor/` still only `marked.min.js`; (3) contrast regression — failing pairs decrease monotonically to 0. Do not add `axe-core`/`pa11y`; the WCAG arithmetic is ~15 lines of `python3`.

### Expected Features

**Must have (P1):** meaning inventory; semantic color token layer; irreversible-action weight for `#btn-authorize`; AA contrast fixes via tokens; `:focus-visible` across the surface; markdown content type scale; UI-chrome type scale; the layout unit; written `UI-SPEC.md`.

**Should have (P2–P3):** page-level hierarchy (`<h1>文档区</h1>` demotion); token conformance script; contrast verification script; interaction states; panel active/inactive differentiation; spacing scale; radius scale; markdown typography polish.

**Defer / decline:** dark mode (own milestone, but shape tokens for it); full ARIA / screen-reader conformance (**contested — see Open Decision 1**); focus trap; `#probe-controls` relocation (product/behavior change); loading/progress indication; primitive tier for space/type/radius; component token tier; responsive/mobile system; icon library; any CSS framework or build step.

**Honest reframing:** at this scale the "differentiator" tier is not extra polish — it is the difference between a one-time cleanup and a contract that holds.

### Architecture Approach

Three files, one implicit contract each, no build step, no modules. `index.html` declares the DOM once; `style.css` owns every design value in one flat, source-order-load-bearing cascade; `app.js` binds ~70 element handles at module top-level (`app.js:4-75`) and derives presentation by toggling classes. **Four of six scope areas need no HTML or JS edits at all** — the strongest argument for the phase order below.

1. **`:root` token block** — inserted after `* { box-sizing }` (L3), before `html, body` (L5), fenced by `/* ===== DESIGN TOKENS: START/END ===== */`. The only place a literal color may exist. Placed first for reviewability, not function — `:root` resolution is order-independent.
2. **`.hidden { display: none !important }`** (L15) — load-bearing infrastructure, not styling. Not tokenized, not moved, not weakened. Five elements (`#draft-empty`, `#rounds-hint`, `#btn-process-round`, `#round-switcher`, `#writing-hint`) have no other rule and depend on it exclusively.
3. **`--sidebar-w` + `calc()`** — `#state-badge { right: 448px }` (420 + 28, arithmetic recorded only in a comment) becomes `calc(var(--sidebar-w) + var(--space-6))`. This is what makes the narrow-window `@media` block a token redefinition with zero extra rules; without it every breakpoint needs its own badge override and the magic number multiplies.
4. **`:focus-visible` + `outline-offset`** — one global rule, `outline` never `border` (`outline` does not participate in layout). Today `grep -c ':focus'` = **0** and `grep -c 'outline'` = **0**, so the UA default ring is *currently active*. This milestone **adds** authored focus styling; it does not restore a removed one.

### Critical Pitfalls

1. **Half-migrated token palette — two sources of truth.** 34 literals is one sitting's work; a partial pass is worse than no tokens. Migrate **totally and mechanically in one pass**, per value-family, atomically, gated by a count. Never define a token you are not consuming in that same commit; never leave a literal for a value you have tokenized.
2. **Cascade regression on `.hidden`.** Three of four competitors win by **ID specificity** (1-0-0), not source order: `#selection-menu` (L483), `#annotations-panel` (L398), `#checks-panel` (L566). `.overlay` (L155) is the only order-based competitor. Dropping `!important` makes `#annotations-panel` visible in phases 1-2 (contradicting `app.js:352`) and permanently pins the 划词 menu over the document after the first selection. `:where(.hidden)` drops to 0-0-0 → all five modals render simultaneously → total app block. **Never add `!important` to a new declaration** (arms race; concrete collision is `#stream-banner` permanently stuck showing "事件流已断开").
3. **Regressing the five shipped fixes.** Do-not-touch list: `style.css:13-15`, the `.fatal` modifier, `applyArchiveView`'s two lines (`app.js:817-818`), the `#selection-menu` DOM position (direct child of `<body>`; moving it under any `filter`/`transform`/`opacity` ancestor changes the containing block), and the `textContent`-only rule in `showInlineError` (an XSS mitigation, T-260916-01, not a style choice).
4. **Contrast fixed to the ratio, hierarchy destroyed — and `opacity` is not a color token.** (a) Fixing `.hint` with the reflexive `#666` puts hints at 5.50:1, identical to blockquotes and verdict suggestions — the least important text becomes as loud as the primary content while being *smaller*. Use the **lightest passing value**; assert hint/body ratio ≤ ~0.30. (b) `opacity` de-emphasis cannot be fixed by any palette change: `.annotation-answered { opacity: 0.65 }` composites `#999` over `#fff` to `#bdbdbd` = **1.88:1**. Ban `opacity` for text de-emphasis. A uniform `--opacity-deemphasized: 0.65` would *lighten* `.round-frozen` (0.55→0.65) and *darken* the archive view (0.75→0.65) — the terminal read-only state must not regress.
5. **Focus styles that shift layout or get clipped.** Never `border`/`padding` for focus — reflows `#probe-controls`, buttons jump on every Tab. `#chat-messages` (2px horizontal padding) and `#annotation-list` (2px) **clip** a 2px ring + 2px offset; `#sidebar` (0 padding) also clips. Ring color must be verified against the **composited** background: `#2c7be5` is 3.97:1 full but **2.05:1** inside `.round-frozen` (0.55) and **2.73:1** inside `.archive-mode` (0.75) — both fail 1.4.11. Do not ring `#round-doc` as a whole (a thousands-of-pixels-tall box shows only top and bottom edges).
6. **Reordering `style.css` is a rendering change.** `#draft-view h2` (L230, 1-0-1) and `#brainstorm-view h2` (L296, 1-0-1) both match the brainstorm heading. L296 wins today → 14px / `#8a6508`. Move L230 below it and the heading silently becomes 15px / `#555`. **Append, do not reorder.**

---

## Implications for Roadmap

### Reconciling the four researchers' build orders

The four proposals are **not in conflict at the phase level** — they describe different layers:

- **ARCHITECTURE.md** proposes the phase skeleton: `P1 tokens → {P2 typography/hierarchy, P3 interaction states, P4 layout robustness, P5 a11y-styling} → P6 a11y-semantics/keyboard`.
- **STACK.md** proposes a 6-step *intra-phase commit order* (token block alone → color by semantic group → spacing/type/radius → focus layer → `@media` → badge geometry). **Not a phase order** — steps 1–3 are all P1, steps 4–6 are P4/P5. Adopt as P1's commit sequence.
- **PITFALLS.md** proposes `A contract+tokens → B typography/hierarchy → C a11y → D layout+interaction → E regression re-verification`. A–D map 1:1 onto Architecture's P1, P2, P5/P6, P3/P4. **E is new and non-optional.**
- **FEATURES.md** contributes two ordering constraints, not a competing skeleton: *the meaning inventory is a prerequisite to the token layer*, and *layout is ONE unit, not three*.

**Where they conflict, and which wins:**

| Conflict | Winner | Why |
|---|---|---|
| PITFALLS merges interaction states + layout (D); ARCHITECTURE keeps them separate (P3, P4) | **ARCHITECTURE wins — keep separate** | Both are CSS-only, Pitfalls' only argument for merging. But regression profiles differ sharply: interaction states are *purely additive* (no existing rule edited) while layout *restructures structural rules* — Architecture names P4 "the highest-regression CSS phase." Merging buries the high-risk diff inside the low-risk one. (If phase count is constrained, merge **P3 with P5** — never P3 with P4.) |
| FEATURES says layout is one unit; ARCHITECTURE's P4 covers the same four items | **FEATURES wins on framing, ARCHITECTURE on mechanics** | Substantively identical: Architecture's P4 already contains the magic number, `--sidebar-w`, the `@media` reflow, and notes 2.4.11 is satisfied "for free once the badge stops being absolutely pinned over content." Adopt Features' hard rule — **do not split these four across phases.** But the 2.4.11 *acceptance check* is verified in P5's focus gate, not as a separate P4 task. |
| PITFALLS says focus (C) must precede/accompany layout (D) because rings depend on container padding; ARCHITECTURE says P5 depends on P4 | **Not a conflict — both say layout before focus verification.** Land the padding bumps in P4 and the ring rule in P5, same release | FEATURES states it most sharply: verifying focus rings before the layout fix "validates a state that is about to change." Do not ship a window where the ring is clipped. |
| STACK says "zero new files"; FEATURES requires `UI-SPEC.md` | **Both correct — different file sets** | Stack means zero new **frontend** files. `UI-SPEC.md` is a planning artifact under `.planning/`. State this explicitly or a planner will treat the two as contradictory. |

**One more reconciliation — the token taxonomy (2 sources vs 1).** STACK.md and ARCHITECTURE.md independently recommend **two-tier (primitive → semantic) for color**; FEATURES.md recommends **single tier of semantically-named tokens**. Genuine disagreement; it is the UI-SPEC's central decision. **Recommendation: two-tier for color only; single tier for space/type/radius; no component tier.** Both Stack and Architecture reached two-tier independently with concrete, code-grounded reasons: with primitives the two near-identical blues (`#2c7be5`, `#2c5fb8`) are visible 30 lines apart and one gets deleted; and there is no `--green-500` semantic alias for "irreversible authorization," so a selector *physically cannot* reach for "green" as a stand-in for "positive." Features' objection (no theme/brand to remap) is answered by these two within-one-context benefits. **The reconciliation satisfying all three:** PITFALLS' rule "name tokens semantically, never by literal (`--gray-500`)" applies to *consumed* tokens. Adopt as a hard invariant: **tier-1 primitive names must never appear outside the `:root` block.** Mechanically checkable, preserves Pitfalls' intent exactly. Features' deeper point survives — no third (component) tier, no primitives for space/type/radius.

### Suggested phase structure

**Six phases.** Architecture's skeleton, with Pitfalls' Phase E folded in as a mandatory milestone-closing gate on P6 rather than a seventh phase.

```
UI-SPEC + 意义清单
        │
        ▼
P1 设计契约与令牌层 ──┬──▶ P2 排版与视觉层级      (CSS-only)
   (CSS-only)         ├──▶ P3 交互状态            (CSS-only)
   hard prerequisite  ├──▶ P4 布局稳健性          (CSS-only) ──▶ P5 可访问性·样式 ──▶ P6 可访问性·语义与键盘
                      │                                          (CSS-only)          (HTML + JS)
                      └──────────────────────────────────────────────────────────────────┘
```

#### Phase 1: 设计契约与令牌层
**Rationale:** Hard prerequisite — four phases consume it, and it is the only phase whose success criterion is a *pure refactor* (zero visual change except intended AA fixes), the cheapest place to discover the migration approach is wrong. Must precede everything because every later fix is a token **value** change, unverifiable while two sources of truth exist.
**Delivers:** `UI-SPEC.md` (token list, meaning inventory, type/space/radius scales, focus rules, "not in v1.14" table); the fenced `:root` block; every literal substituted; **AA-compliant values chosen here, at declaration time — not in P5**.
**Addresses:** 设计令牌体系; the meaning inventory (Features' prerequisite); `--color-action-irreversible` **declared** (applied in P2).
**Avoids:** Pitfall 1 (half-migration), Pitfall 2 (as written constraint), Pitfall 8 (scope creep — "not in v1.14" table), Pitfall 9 ("append, do not reorder"), Pitfall 4a (ban `opacity` for text de-emphasis), Pitfall M6 (`#confirm-error` keeps its ID, or its error color set with equal-or-higher specificity than `.hint`).
**Commit order (STACK.md):** (0) baseline screenshots of all 5 phase views → (1) token block alone, pixel-identical → (2) color, one semantic group per commit (text → action → surface → border) → (3) spacing/type/radius. Do not reorder 2 before 1; do not merge 2 and 3.
**Gates:** Gate 1 (0 hex outside the fence), Gate 2 (every `var()` declared), `grep -c '^\.hidden {'` = 1, total `!important` count = 1, `node --check app.js`, pytest 219-test baseline unchanged, `app.js`/`index.html` untouched.

#### Phase 2: 排版与视觉层级
**Rationale:** Most user-visible value; carries the Core Value finding. Pure CSS — panel active state derives from `:not(.hidden)`, the `<h1>` is styled by a new `#doc-pane > h1` rule, emoji are CSS `content`.
**Delivers:** explicit `font-size` for `.markdown-body h1/h2/h3` (**scoped under `.markdown-body`** — a global `h1,h2,h3` rule collides with four chrome `<h2>` overrides: `.panel-header h2` 14px, `#draft-view h2` 15px, `#brainstorm-view h2` 14px, `.overlay-card h3` 16px); `#doc-pane > h1` demotion; **`#btn-authorize` distinct treatment** (solid `#26754a` fill + white = 5.64:1, so solid is AA-safe — not forced into a pale tint); panel active/inactive differentiation; the two `content:` emoji.
**Addresses:** 视觉层级, 排版系统.
**Avoids:** Pitfall M4 (chrome vs content `h2` collision), Pitfall 7 (emoji — **scope to 2 `content:` emoji; no icon system**; do not touch `renderAnnotations`/`renderVerdictCard`; if `.collapse-indicator` is touched, `app.js:1550` assigns `textContent` and would erase an inline `<svg>`), Pitfall M5 (do not soften `:disabled` — it is the only visual signal of the G3 precondition).

#### Phase 3: 交互状态
**Rationale:** Purely additive — no existing rule edited, minimal regression risk. Architecture sequences it before P4 deliberately: safe additive work first, so the structural diff stays isolated and reviewable.
**Delivers:** `:hover` / `:active` / `:disabled` / `transition` (currently 2/0/8/1); `@media (prefers-reduced-motion: reduce)` in the **same commit** as any new transition.
**Avoids:** Pitfall M3 (no `* { transition: all }` — `renderEvent` sets `scrollTop` on every event and the `streaming` class toggle would flash the whole panel; a transition on `opacity` cannot work against `display: none`, and the tempting `visibility`/`opacity` workaround re-opens Pitfall 2 *and* leaves hidden content tab-reachable).

#### Phase 4: 布局稳健性
**Rationale:** One indivisible unit (Features' rule, adopted). Four items touch the same declarations; splitting guarantees rework. Highest-regression CSS phase.
**Delivers:** `--sidebar-w` + `calc()` badge fix; `@media` reflow with **literal** breakpoint values; `#doc-pane { min-width: 0 }` + `overflow-wrap: anywhere`; scroll-owner reduction 5 → 2; the `#chat-messages`/`#annotation-list` padding bumps that un-clip focus rings (landed here, verified in P5).
**Scope fence:** "narrow windows do not break" — no horizontal overflow ≥1024px, no content occlusion ≥768px. A stacking/mobile layout is a **new design decision** (changes what DESIGN.md §4.1's two-column contract means) and is explicitly out of scope.
**Avoids:** Pitfall M2 (the `#state-badge`/`#stream-banner` collision — they overlap by 48px at 1280px and 90px at 1024px, and the higher-z-index banner **covers the only state readout**; the fix must not move the badge into normal flow), Pitfall 8 items 3–4 (no header restructuring, no responsive redesign).
**Gates:** resize 1440 → 1024 → 768 with no horizontal overflow; badge in the doc pane's top-right at every width; banner does not cover badge at 1024/1280; exactly one sidebar scrollbar plus `#chat-messages`; `#brainstorm-view h2` still computes to 14px / `#8a6508`.

#### Phase 5: 可访问性·样式
**Rationale:** Depends on P1 (ring color is a token) and **P4** (the layout it rings must be stable — verifying earlier validates a state about to change).
**Delivers:** one global `:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px }`; the AA verification pass over every token pair including opacity-composited values; `2.4.11 Focus Not Obscured` verified as a by-product of P4.
**Avoids:** Pitfall 5 in all four modes (layout shift, clipping, dimming, invisible-on-tall-box), Pitfall M5 (disabled must remain unambiguous and distinct from `:hover`).
**Gates:** `grep -c ':focus-visible'` > 0; every failing pair from the reconciled table passes; **no focus rule sets `border` or `padding`**; every ring verified against the 0.55 and 0.75 composited backgrounds; tab through with the sidebar scrolled to the bottom.

#### Phase 6: 可访问性·语义与键盘 (the only HTML/JS phase)
**Rationale:** Last because it is the only phase editing `app.js`/`index.html`, where the ~70 top-level `getElementById` handles (`app.js:4-75`) make every edit potentially fatal to the whole script. **All HTML/JS risk is concentrated here.**
**Delivers (contested — see Open Decision 1):** `tabindex="0"` on `#round-doc` **+ `:focus-visible` (already shipped in P5) in the same commit**; `#selection-menu` focus handoff + Escape-to-close + focus return; Escape-to-close on the blocking modals; whatever ARIA scope the user decides.
**Critical framing:** this is **not** "add attributes." `tabindex="0"` on `#round-doc` is the thing that makes b9664e0's already-shipped `keyup` listener execute **for the first time** (Known Issue 3). And `role="dialog"` without Escape-to-close is *worse* than no role: it announces a contract the implementation does not honor.
**Why the focus handoff is required, not gold-plating:** `#selection-menu` is the *last* element in `<body>` (after five modals). Tab order from `#round-doc` runs through the entire document area and the whole sidebar before reaching it — a keyboard user who successfully selects text would press Tab a dozen times to reach the menu they just triggered, and any intermediate focusable element that closes on blur defeats it.
**Milestone-closing gate (Pitfalls' Phase E, folded in):** re-run **all five manual checks** from `260916-t8g-SUMMARY.md` (including PLAN items 3, 5, 6) — none of the five shipped fixes has an automated test, so a milestone that rewrites their CSS without re-running them has no evidence it did not break them. Plus `node --check app.js`; pytest 219-test baseline unchanged; the archive path shows no clickable 「处理本轮批注」 **after switching rounds in the archive switcher** (the `updateFrozenPresentation` reset path).
**If the planner prefers a standalone 7th verification phase, that is defensible** — but do not ship without these checks.

### Phase Ordering Rationale

- **P1 first** — the only phase whose success criterion is a pure refactor; without a single source of truth P5's contrast work is literally unverifiable.
- **P2 before P3/P4** — carries the Core Value fix (the milestone's stated point), CSS-only, no structural risk.
- **P3 before P4** — additive work before structural churn, so the structural diff is attributable.
- **P4 before P5** — focus rings depend on container padding (P4) and on not being inside dimmed subtrees (a P1 palette decision); verifying focus before layout validates a state about to change.
- **P6 last** — the only phase touching HTML/JS, where the failure mode is total and silent.
- **Dependency discipline is the whole point.** P2/P3/P4 are mutually independent and *may* be reordered with a concrete reason — but P4 must not move after P5, and P1 must not move at all.
- **Three hard rules, not soft:** `tabindex` and `:focus` land in the same commit; layout is one unit; `prefers-reduced-motion` lands in the same commit as any new transition.

### Research Flags

**Needs deeper research during planning:**
- **Phase 1:** the token taxonomy and meaning inventory are *design decisions*, not research gaps — see Open Decisions. `ARCHITECTURE.md` lists 7 unresolved questions for the UI-SPEC author (token names; irreversible treatment; type-scale anchor 13px vs 14px; whether `--fw-medium: 500` is consumed at all; narrow-window scope; `#state-badge` `calc()` vs `absolute`; emoji icon mechanism). Resolve **before** P1 can be planned.
- **Phase 6:** the ARIA scope is an open user decision. Do not plan P6 until resolved.
- **Phase 4:** `calc()` vs `position: absolute` for `#state-badge` is a real behavior trade-off (fixed-and-occluding vs. scrolls-away). Architecture recommends `calc()` as the zero-behavior-change migration; confirm with the user.

**Standard patterns (skip research-phase):**
- **Phase 3** — `:hover`/`:active`/`:disabled`/`prefers-reduced-motion` are fully documented, zero-ambiguity CSS.
- **Phase 5** — `:focus-visible` + `outline-offset` is well-documented; the only project-specific work (ring color vs. composited backgrounds) is already computed.
- **Phase 2** — type scales and hierarchy are established practice; project-specific collisions are already enumerated.

### Verification Environment (do not re-derive)

- Playwright **must** use `chromium.launch({ channel: 'chrome' })` — the bundled Chromium version does not match.
- **Keyboard text selection cannot be automated** (not even on `contenteditable`). Every Shift+Arrow acceptance item must be a **MANUAL check**.
- **Screenshots are unavailable**: headless rendering was blocked (Chrome, Chrome-for-Testing, and `chrome-headless-shell` all failed) and the persistent `/api/events` SSE stream prevents the capture handler from terminating. Plan for computed-style checks in DevTools plus named manual steps, not visual diffing.
- **Every phase needs at least one runtime verification, not only static counts.** `grep -c 'var(--'` proves nothing about rendering, and the prior fix run already produced a gate arithmetic error (`showInlineError(` expected 6, actual 9) that was reported rather than fixed.

---

## Known Issues Inherited from b9664e0

Three defects in the just-shipped fixes, independently verified by the orchestrator. **The milestone's own work sits on top of them.** Recorded as facts; do not re-derive.

1. **`frontend/style.css:13-14` states the wrong reason for a correct `!important`.** The comment names `.overlay`/`.doc-subview` as the 0-1-0 competitors. `.doc-subview` has **no `display` declaration at all**, and the comment omits the decisive competitors — `#selection-menu`, `#annotations-panel`, `#checks-panel` are all **specificity 1-0-0** and beat `.hidden` regardless of source order. **The `!important` is correct; its stated rationale is not.** PITFALLS.md Pitfall 2 independently reached the same conclusion with the same enumeration. Fixing the comment is cheap and is the only defense a future reader has. Add to P1's scope.

2. **`showInlineError(processRoundBtn, ...)` renders as a squeezed wrapped column.** It inserts the error `<p>` via `insertAdjacentElement('afterend')`, but `#btn-process-round` sits inside `#probe-controls { display: flex; gap: 8px }` as the 4th of 5 horizontal flex items — the error becomes a **6th flex item**, takes its content width and shrinks. It passed both the grep gate and the manual check because it *is* literally adjacent to the button. **The other four call sites are fine** (block-flow containers: `enterForm`, `#divergence-entry`, `#approve-row`, `#checks-panel .panel-body` which is a flex *column*). Fix: `flex-wrap: wrap`, a dedicated error slot below the row, or a different anchor — **prefer the structural fix over a CSS patch.** Same fix's blast radius: `clearInlineError()` is not called on view transitions (stale error persists after switching views) and the `inlineErrorEl` singleton drops one of two concurrent errors. PITFALLS.md Pitfall 10 matches independently.

3. **The keyboard selection path added in b9664e0 is inert.** `grep -n 'tabindex' index.html app.js` returns **0**; `#round-doc` is a plain `<div>`, so focus never enters its subtree and the `keyup` listener at `app.js:1327` can never fire. **The keyboard path to 划词批注 — the flagship feature, mandated by DESIGN.md D-02 — is still mouse-only.** Do not report this "shipped fix" as delivered. P6's `tabindex="0"` is what makes it live. Note PITFALLS.md Pitfall 6 recommends considering the *alternative* of no `tabindex` + a real 「批注」button — avoids a new tab stop, but is a different product decision (Open Decision 2).

**Additionally recorded (PITFALLS.md, not orchestrator-verified but code-grounded):** the archive read-only gating has a **second entry point** — `updateFrozenPresentation(true)` (`app.js:1166`) sets `processRoundBtn.disabled = processInFlight`, resetting what `applyArchiveView` set at `app.js:818`. Recovery is one line: re-add `processRoundBtn.disabled = true` at the end of `loadArchiveView()`, after `loadChecksView`, mirroring the G-idi03-3 precedent at `app.js:844-845`.

---

## Reconciling the Contrast Undercount

**Four measurements, four numbers — because they count different things, not because they disagree about facts.**

| Source | Count | What it actually measured |
|---|---|---|
| v1.13 audit (`03-UI-REVIEW.md`, Pillar 3) | **4** | Sampled representative cases: `.hint`, `#pending-count`/`.badge-pending`, `.event-kind` ochre, `.chat-user`. |
| Orchestrator's independent sample | **7** | A sampled set of pairs, computed by hand. |
| STACK.md | **13 declarations / 11 selectors** | **Exhaustive** over all 142 rule blocks, *declared* color/background values only. Does not composite `opacity`. |
| PITFALLS.md | **"at least 9"** | Declared values **plus** opacity-composited cases; not an exhaustive block scan. |

**Reconciled picture: STACK.md's 13 is the exhaustive floor; PITFALLS.md's opacity cases are additive to it; the union is the true scope. The audit's 4 is an undercount, full stop — do not plan against it.**

**Text contrast (SC 1.4.5, 4.5:1 for normal text):**

| Pair | Ratio | Selectors |
|---|---|---|
| `#999` on `#fafafa` | **2.73:1** | `.hint` — pervasive: every gate precondition, every recovery instruction |
| `#999` on `#f5f5f5` | **2.61:1** | `.badge-answered` |
| `#fff` on `#999` | **2.85:1** | `.event-kind` **default** chip |
| `#b8860b` on `#fdf6ec` | **3.03:1** | `#pending-count`, `.badge-pending` |
| `#fff` on `#b8860b` | **3.25:1** | `.event-kind` ochre chip (执行) |
| `#2e8b57` on `#e9f7ef` | **3.84:1** | **`#btn-approve-draft`, `#btn-process-round`, `#btn-authorize`, `#btn-start-writing`, `#btn-continue-check`/`#btn-continue-repair` — 5 rules, 6 buttons** |
| `#fff` on `#2c7be5` | **4.14:1** | `.overlay-card button`, `#chat-input-row button`, `button.primary`, `.chat-user` |
| **opacity-composited:** `#999` @ 0.65 on `#fff` → `#bdbdbd` | **1.88:1** | `.annotation-answered` — §4.2's "已回应…变灰不删除" becomes "变灰到读不了" |
| **opacity-composited:** `#1a1a1a` @ 0.55 on `#fafafa` → `#7f7f7f` | **3.84:1** | `#round-doc.round-frozen` |
| `#999` on `#fff` (no opacity) | **2.85:1** | `.annotation-plain` |
| `#fff` on `#2e8b57` | **4.25:1** | `.kind-write .event-kind` |
| `#fff` on `#2c7be5` | **4.14:1** | `.kind-say .event-kind` |

The audit missed `.badge-answered`, `.annotation-answered`, `.annotation-plain`, the default `.event-kind` chip, and the `kind-*` chips.

**Non-text contrast (SC 1.4.11, 3:1) — in scope:**

| Element | Ratio | Verdict |
|---|---|---|
| Input/button borders `#ccc` on `#fff` | **1.61:1** | **In scope.** The border is the only thing identifying the control. Needs ≥ `#8a8a8a` (3.45:1 on `#fff`, 3.17:1 worst-case on `#f5f5f5`). |
| `.annotation-pending-item` left border `#e8d9a8` on `#fffdf5` | **1.38:1** | **In scope** — a *state* indicator. |
| `.badge-pending` border `#e8d9a8` on `#fdf6ec` | **1.31:1** | **In scope** — state indicator. |
| Focus ring `#2c7be5` on `#fafafa` | 3.97:1 full / **2.73:1** @ 0.75 / **2.05:1** @ 0.55 | **In scope, and failing** inside `.archive-mode` / `.round-frozen`. |
| `#eee` / `#e0e0e0` / `#f0f0f0` dividers | 1.16–1.36:1 | **Out of scope.** Purely decorative; 1.4.11 does not apply. Do not darken every divider. |
| Inactive/`:disabled` controls (`opacity: .55`) | — | **Out of scope.** 1.4.11 explicitly does not apply to inactive components. |

**The single most consequential failure:** `#btn-authorize`'s own label — `#2e8b57` on `#e9f7ef` = **3.84:1** — fails, on the project's **Core Value red-line button**, sharing the **exact palette of six routine buttons**. It is the only text on the control that gates entry into 撰写总设计文档.

**And the finding that changes the milestone's shape:** STACK.md's "green overloaded across six buttons" BLOCKER (audit 3.3) and this contrast failure are **ONE fix**. The audit flagged them as two unrelated items. They are not.

### Proposed token values — each verified against every background it lands on

| Token | Value | Verification |
|---|---|---|
| `--color-text` | `#1a1a1a` | 16.67:1 on `#fafafa` — unchanged |
| `--color-text-secondary` | `#555555` | 7.14:1 on `#fafafa` — unchanged |
| **`--color-text-muted`** | **`#6a6a6a`** | 5.18 on `#fafafa`, 5.41 on `#fff`, 4.96 on `#f5f5f5`, **4.75 on `#f0f0f0`** (worst case) |
| **`--color-action-primary`** | **`#1f63bd`** | white on it = **5.87:1**; as text on `#fafafa` = 5.62:1 |
| **`--color-action-success`** | **`#26754a`** | white on it = 5.64:1; on the `#e9f7ef` tint = **5.10:1** (was 3.84) |
| **`--color-action-warning`** | **`#8a6508`** | 4.96:1 on `#fdf6ec`, 4.78:1 on `#fff3c4`, 5.32:1 on `#fff` |
| `--color-action-danger` | `#c0392b` | 5.44:1 white-on; 5.21:1 as text — **already passing, no change** |
| `--color-border-strong` | `#8a8a8a` | 3.45:1 on `#fff`, 3.17:1 on `#f5f5f5` — meets 1.4.11 |
| `--color-focus` | `#1f63bd` | worst case **5.15:1** across all 8 page backgrounds (needs only 3:1) |

**Where the two computed proposals disagree, STACK.md wins** — it is the exhaustive scan; ARCHITECTURE.md's sample (`#1a6fd4` = 4.92:1, `#6b6b6b`) was not verified against `#f0f0f0`. Both agree on the *method*, which is the load-bearing part.

### Three computed results a naive UI-SPEC will get wrong

1. **`#767676` — the reflexive "AA-safe grey" — FAILS here.** It is 4.54:1 on white but only **4.35:1 on `#fafafa`**, the doc-pane background where `.hint` actually lives. `#6e6e6e` also fails (4.47:1 on `#f0f0f0`). **Only `#6a6a6a` passes on every background present in the file.** Pick it and the whole class of "moved the element, broke the contrast" bugs disappears.
2. **`#8a6508` already exists in the file** (used by `#btn-divergence` and `#stream-banner`) and already passes everywhere. **The amber fix is a deletion, not an addition:** collapse `#b8860b` into `#8a6508`. Two ambers become one.
3. **One token change fixes four selectors.** `#2c7be5` → `#1f63bd` simultaneously repairs `.overlay-card button`, `#chat-input-row button`, `button.primary`, and `.chat-user`. No reason to fix them individually.

**One more, from PITFALLS.md, that the value table alone would get wrong:** fix contrast by choosing the **minimum passing value, then explicitly re-checking the hierarchy**. `.hint` fixed with `#666` lands at 5.50:1 — identical to `.markdown-body blockquote` and `.verdict-suggestion`. Hints, pull-quotes, and AI repair suggestions become one visual rank, and the hint becomes *nearly as loud as the primary content while smaller*. Assert hint/body ratio stays ≤ ~0.30.

---

## Open Decisions Requiring User Input

### Open Decision 1: ARIA scope

**A genuine disagreement between researchers. Do not resolve silently — the user decides.**

**FEATURES.md argues to DECLINE most ARIA work.** ARIA exists to serve users who arrive without context and cannot see the screen. This app has exactly one user, who is also the author, who sees the screen. The cost is real — focus management in vanilla JS is fiddly and easy to get subtly wrong — and the benefit accrues to **nobody who exists**. It keeps only two exceptions, on **safety** grounds rather than accessibility grounds:
- (a) **Escape-to-close on the two blocking/safety modals.** The G3 confirm modal is default-deny by design; a keyboard user who cannot dismiss a modal is *stuck*. A usability trap for the actual user, not a compliance item.
- (b) **`role="dialog"` + `aria-modal="true"` on those same two modals** — two attributes, zero risk.

Features declines outright: `aria-live` on the streaming chat, focus traps, `aria-describedby` wiring, and `role`/`aria-*` on the other modals. It declines focus-trap implementation specifically ("without a trap, tabbing from a modal reaches background controls — mildly confusing, not harmful, since the background is visually occluded").

**ARCHITECTURE.md and PITFALLS.md assume a broader a11y phase.** Their P6 includes `role="dialog"` / `aria-modal="true"` / `aria-labelledby` on **four** `.overlay` modals; Escape-to-close; **focus trap**; initial focus; `aria-live="polite"` on `#chat-messages`; `aria-live="assertive"` on `#stream-banner`; and `role="region"` + `aria-label` (or no `tabindex`) on `#round-doc`. Today `grep -n 'aria-\|role='` over the whole frontend returns **zero matches**.

| Item | Features | Architecture / Pitfalls |
|---|---|---|
| Escape-to-close on blocking modals | **Yes** (safety) | **Yes** |
| `role="dialog"` + `aria-modal` on blocking modals | **Yes** (2 attrs, zero risk) | **Yes** |
| `role`/`aria-modal` on the other 2–3 modals | No | Yes |
| Focus trap | **Decline** | Yes |
| Initial focus / focus return | No | Yes |
| `aria-live` on `#chat-messages` | **Decline** | Yes — **but** PITFALLS.md M7 constrains it: never on the chunk container (`appendSayToChat` appends one DOM node per SSE event; a multi-minute call would make the region unusable). Announce at the *bubble* level with `aria-busy`, or use `role="log"`. |
| `aria-live="assertive"` on `#stream-banner` | Decline | Yes — makes the *same* signal b9664e0 FIX 2 already gives sighted users reach a screen reader |
| `tabindex` on `#round-doc` | Not addressed (Features scopes a11y to focus visibility + keyboard reachability verification) | Yes, **but** PITFALLS.md Pitfall 6 offers the alternative of *no* tabindex + a real 「批注」button, avoiding a new tab stop |

**What is NOT contested and must ship regardless of this decision:**
- `tabindex` and `:focus` land in the **same commit** (PROJECT.md's own rule; PITFALLS Pitfall 6).
- The keyboard path to 划词批注 must actually work — it does not today (Known Issue 3). Whether via `tabindex` on `#round-doc` or via a real button is a sub-decision (Open Decision 2).
- Escape-to-close on the blocking modals.
- `role="dialog"` + `aria-modal="true"` on those two.

**Decision criteria for the user:**
- **Choose Features' narrow slice** if the milestone's goal is read literally — "键盘可用" (keyboard *usable*), not "screen-reader conformant." The narrow slice is ~2 attributes + 1 keydown handler, all justifiable on **safety** grounds for the actual user. It also keeps P6 small, which matters because P6 is the only phase that can fatally break `app.js`.
- **Choose the broader scope** if WCAG conformance is a stated goal in its own right, or if the tool might ever be shared or demoed. Cost: a hand-written focus trap (Shift+Tab wraparound + dynamic content) in vanilla JS, which PITFALLS.md explicitly warns is "fiddly and easy to get subtly wrong" — and a wrong trap is worse than none.
- **A middle position is available and may be the best fit:** the narrow slice (Escape + 2 dialog attributes) **plus** `aria-live="assertive"` on `#stream-banner` (one attribute; extends a signal the tool already computes) **plus** `role="region"` + `aria-label` if `tabindex` is added. Skip the focus trap and skip `aria-live` on `#chat-messages`.

**Recommendation: the narrow slice.** It matches the milestone's stated goal ("键盘可用", not "无障碍合规"), is defensible on safety rather than conformance grounds, and keeps the only HTML/JS phase small. But this is the user's call — the two camps have equally good reasoning and the difference is a values question about who the tool is for.

### Open Decision 2: The keyboard annotation path — `tabindex` on `#round-doc`, or a real button?

- **`tabindex="0"` on `#round-doc`** makes the shipped `keyup` listener live with one attribute. Cost: a new tab stop on a generic `<div>`; PITFALLS Pitfall 6 warns every keystroke in the document then runs `handleSelectionTrigger`, and the menu already has three independent closers (`mousedown` at `app.js:1340`, capture-phase `scroll` at `app.js:1345`, and the handler's own empty-selection guard) with no way to *keep* it open. Needs `role="region"` + `aria-label` to not be announced as a generic container, and a ring on a thousands-of-pixels-tall box is invisible — ring `#doc-pane` instead, or use an inset treatment.
- **A visible 「批注」button operating on the current selection** adds no tab stop, is simpler, is unambiguous. Cost: a UI addition, and the trigger flow changes.
- **Do nothing and document the one-click focus requirement** is the third option, and PITFALLS.md notes it is the simplest — the previously-passed UI-6.1 manual check already covers it.
- **Whatever is chosen, the UI-6.1 manual UAT must be re-run** — the documented limitation ("先聚焦文档区这一步仍需鼠标点击一次") stops holding, so the previously-passed check is testing a different thing.

### Open Decision 3: Token taxonomy and the meaning inventory

Not a research gap — a design decision. See the taxonomy recommendation under "Reconciling the four researchers' build orders." The seven concrete questions ARCHITECTURE.md poses to the UI-SPEC author (token names and the positive/gate/irreversible split; the irreversible treatment; the 13px-vs-14px type anchor; whether `--fw-medium: 500` is consumed; narrow-window scope; `#state-badge` `calc()` vs `absolute`; the emoji icon mechanism) must be answered **before P1 can be planned**.

---

## Baseline Reconciliation (use these numbers)

The four researchers measured at slightly different times around `b9664e0`. Use these reconciled values; stale pre-fix counts appear in the audit.

| Fact | Value | Note |
|---|---|---|
| Distinct hex literals | **34** (120 occurrences) | FEATURES.md and ARCHITECTURE.md re-measured post-fix; STACK.md agrees (34). PITFALLS.md's "32" and the audit's "32" are pre-fix. |
| `style.css` lines | **631** | STACK.md says 622, PITFALLS.md says 632. The fence-gate greps do not depend on the exact count. |
| `index.html` lines | **221** | |
| `app.js` lines | **1,639** | |
| CSS custom properties | **0** | |
| `:focus` / `outline` rules | **0 / 0** | UA default focus ring is *currently active*. |
| `@media` rules | **0** | |
| Distinct `font-size` | **7** (13px ×15, 12px ×6, 14px ×5, **12.5px ×3**, 16px ×1, 15px ×1, 11px ×1) | |
| Distinct `border-radius` | **8** | |
| Distinct padding / margin / gap | **14 / 11 / 5** | |
| `aria-*` / `role=` in HTML | **0** | |
| `tabindex` in HTML or JS | **0** | |
| `.hidden` rules | **1** (global, `!important`) | There are **no 14 duplicates to delete** — the audit's Top Fix 1 was already done in `b9664e0`. |
| Total `!important` in `style.css` | **1** | Must stay 1. |
| `z-index` values | 4 — 10 badge, 20 banner, 100 overlay, 200 selection-menu | Tokenize as `--z-*` and assert the ordering. |
| Color/style writes from JS | **0** | Tokenization is a 100% CSS-only migration. |
| `index.html` inline `style=` attributes | **0** | |

---

## Confidence Assessment

| Area | Confidence | Notes |
|---|---|---|
| **Stack** | **HIGH** | Every version number verified against MDN browser-compat-data (the machine-readable source caniuse itself derives from) plus caniuse; every behavioral claim (cascade-layer ordering, `var()` fallback semantics, "variables do not work in media queries") verified against MDN primary docs; contrast values are deterministic arithmetic over the project's own file. STACK.md explicitly flags a divergence from `gsd_run query classify-confidence --provider websearch` (which returns LOW/MEDIUM for *search-engine* results) — correctly, because these are primary-source and own-arithmetic findings. |
| **Features** | **HIGH for codebase-grounded findings; MEDIUM for external best-practice claims.** | All counts measured directly from source. WCAG/token-architecture guidance is triangulated from search-result summaries — the network fetch to w3.org and developer.mozilla.org was **blocked in this environment**. FEATURES.md flags this honestly. |
| **Architecture** | **HIGH on integration points and constraints; MEDIUM on specific token values.** | Every integration point verified by reading current source and the b9664e0 commit diffs. Token values are arithmetic-verified but the final choice is a UI-SPEC decision. |
| **Pitfalls** | **HIGH for all code-level claims; MEDIUM for phase-ordering recommendations.** | All claims verified by direct source inspection + computed arithmetic. Phase-ordering and the `#probe-controls`/AI-03 inference are explicitly flagged as judgment, not verification. |

**Overall confidence: HIGH** on what to build, how to build it, what to avoid, and what is currently broken. **MEDIUM** on the two open decisions (ARIA scope, keyboard-path mechanism) — those are values questions, not knowledge gaps.

**Cross-validation worth noting:** three researchers independently computed the same contrast ratios from the same file and reproduced the audit's four reported values (2.73 / 3.03 / 3.25 / 4.14) exactly. That the audit's four are *correct but incomplete* — and that the incompleteness is systematically in the same direction (the audit sampled; the researchers scanned) — is itself a finding about how the v1.13 audit was produced.

### Gaps to Address

- **WCAG 2.2 criterion numbering is not primary-source verified.** FEATURES.md states SC 2.4.11, 2.5.8, 3.2.6, 3.3.7, 3.3.8 from established practice rather than a fetched spec. The *substance* (focus not obscured; 24×24 target size; 4.5:1 / 3:1) is stable and widely reported. **Verify exact numbering before writing it into `UI-SPEC.md`.**
- **The two `window.prompt` call sites (`app.js:486`, `app.js:1354`) are frozen.** Audit 1.3 flags them, but replacing them is a behavior change to the annotation flow (UI-01) and the G3 rejection path (FLOW-05 / D-P3-5) — both branch on `null` for cancel. Feature work with a UAT surface. Not this milestone.
- **The event-kind palette is a separate, closed vocabulary.** The 7-color ad-hoc set (blue/purple/green/ochre/grey/red/black) overlaps but does not align with the UI accents — green means both "写文件 event" and "positive button." Two genuinely different vocabularies (categorical set vs. semantic accent set). **Tokenize the event-kind set as its own named group so the overlap becomes explicit and intentional. Do not try to unify them.**
- **WCAG 2.5.8 target size** (`.verdict-buttons button` computes to ~21–22px tall; `#selection-menu` buttons similarly tight) is a real AA finding. Fold into the interaction-states work if it does not fight the layout — do **not** restructure the sidebar for it (the verdict buttons are deliberately compact to fit 3 in a 420px sidebar).
- **The `#probe-controls` inline-error fix and the `#state-badge` `calc()` decision both touch `#probe-controls`'s neighborhood.** Coordinate them; PITFALLS.md Pitfall 10 puts the row fix in the layout/interaction phase.
- **Two researchers measured slightly different file sizes and literal counts.** Reconciled numbers above; re-measure at plan time if a gate depends on an exact count.

---

## Sources

### Primary (HIGH confidence)

**Codebase — measured directly by all four researchers:**
- `frontend/style.css` (~631 lines) — read in full by three researchers; the migration target
- `frontend/index.html` (221 lines) — read in full
- `frontend/app.js` (1,639 lines) — read in full by PITFALLS.md; in part by ARCHITECTURE.md (L1-140 handles, L1230-1340 selection path, targeted greps)
- `.planning/milestones/v1.13-phases/idi-03-g3/03-UI-REVIEW.md` — six-pillar audit (13/24, 7 BLOCKERs, ~40 findings). **Treated as a starting point, not ground truth** — its contrast count of 4 is an undercount and its Top Fix 1 (`.hidden` consolidation) was already done in `b9664e0`.
- `.planning/quick/260916-t8g-ui-5-blocker-hidden-sse-onerror/260916-t8g-SUMMARY.md` — the five shipped fixes, their decisions, documented known limitations, and the manual checks to re-run
- `.planning/PROJECT.md` — v1.14 scope, six target features, Core Value, constraints, UAT environment facts
- Git: `b9664e0` (squash) and constituents `ed14c6e`, `f7eae48`, `0912429` — diffs read in full

**External platform documentation:**
- MDN, `@layer` (last modified 2026-04-20) — cascade-layer ordering; "styles not defined in a layer always override styles in layers"; `!important` inversion
- MDN, `var()` (CSS Custom Properties L1/L2) — fallback fires only on guaranteed-invalid; invalid-at-computed-value-time resolves to `unset`, **not** the fallback; fallbacks are not a compatibility shim
- MDN, *Using CSS custom properties* — `:root` inheritance; **"Variables do not work inside media queries and container queries"**
- MDN browser-compat-data — every version number in STACK.md's compatibility table
- caniuse feature data (`css-cascade-layers`, `css-focus-visible`, `css-variables`, `css-relative-colors`, `css-media-range-syntax`, `css-nesting`)
- W3C WCAG source repo, Understanding docs: `contrast-minimum`, `non-text-contrast`, `reflow`, `text-spacing`, `focus-visible`, `focus-not-obscured-minimum`, `focus-appearance`, `target-size-minimum`

**Computed arithmetic (script-verified, deterministic):** every contrast ratio in this document, including opacity-composited values and the focus-ring-under-dimming table; the `#state-badge`/`#stream-banner` overlap table; the scroll-container padding table.

### Secondary (MEDIUM confidence)

- Design-token tiering — Smashing Magazine ("Design Tokens: Primitive vs Semantic — When Two Tiers Is Over-Engineering"), CSS-Tricks, learnwithjason.dev ("Stop Over-Engineering Your Design Tokens — Use One Tier"), thedesignsystem.guide, Contentful ("Design Tokens 101")
- WCAG 2.2 focus guidance, `:focus-visible` best practices, `outline-offset`, fallback patterns — via search results referencing MDN, W3C WCAG 2.2 SC 2.4.7 / 2.4.11 / 2.4.13, WebAIM, Sara Soueidan. **Network fetch to w3.org and developer.mozilla.org was blocked in the FEATURES.md research environment.**
- Type-scale ratios — modularscale.com, typescale.com, Figma design-systems guidance

### Tertiary (LOW confidence — flag before use)

- Exact WCAG 2.2 AA criterion numbering and thresholds (2.4.11, 2.5.8, 3.2.6, 3.3.7, 3.3.8) — stated from established practice, not fetched from the spec
- PITFALLS.md's phase-ordering recommendations and the claim that removing `#probe-controls` would break AI-03's dual-route verification (inferred from DESIGN.md D-06/§9 as cited in PROJECT.md, not from reading DESIGN.md directly)

---

*Research completed: 2026-09-17*
*Ready for roadmap: yes*
*Open before P1 planning: Open Decisions 1–3*

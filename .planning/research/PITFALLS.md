# Pitfalls Research

**Domain:** Retrofitting a design-token layer and accessibility states onto a **shipped** vanilla frontend (no framework, no build step, no design contract)
**Project:** 交互式讨论迭代系统 — Milestone v1.14「前端视觉与可访问性」
**Researched:** 2026-09-17
**Confidence:** HIGH for all code-level claims (verified by direct source inspection + computed arithmetic against the actual files); MEDIUM for the phase-ordering recommendations (judgment, not verification)

## Scope Note

This milestone is **not** greenfield design-system work. The artifacts already exist and are live:

| File | Size | State |
|------|------|-------|
| `frontend/style.css` | 632 lines | 32 hardcoded hex literals, **0** CSS custom properties, **0** `:focus`, **0** `@media`, 2 `:hover`, 0 `:active`, 1 `transition` |
| `frontend/index.html` | 221 lines | **0** `aria-*`, **0** `role=`, **0** `tabindex` |
| `frontend/app.js` | 1639 lines | 78 `classList.add/remove('hidden')` call sites across ~30 elements |

Five functional BLOCKERs were fixed 2026-09-16 (`b9664e0`, tasks `ed14c6e` / `f7eae48` / `0912429`) and verified **by grep-count gates plus manual UAT**, not by automation. Those five fixes are the highest-value and highest-risk surface in this milestone: every one of them is load-bearing on CSS the visual milestone is about to rewrite.

The single most important framing: **this milestone edits CSS that other, already-verified behavior depends on.** Most of the pitfalls below are not "bad CSS" — they are "a CSS change silently reverting a JS-level guarantee."

---

## Critical Pitfalls

### Pitfall 1: The token layer duplicates the literals instead of replacing them — two sources of truth

**What goes wrong:**
A `:root` block is added with tokens, and rules are migrated **opportunistically** — only the selectors the author happens to be editing. `style.css` then holds a partial palette. Concretely, `#999` appears as a literal in four places that all mean "de-emphasized text": `.hint` (L39), `.badge-answered` (L447), `.annotation-plain .annotation-note` (L461), `.annotation-answer summary` (L464). If only `.hint` is migrated to `--color-text-muted`, the later contrast phase darkens the token, `.hint` changes, and the other three stay at `#999` — **the same semantic concept renders at two different darknesses inside the same 420px sidebar**, with no way to tell from reading the file whether a remaining literal is "not yet migrated" or "deliberately different."

**Why it happens:**
Tokens feel like a refactor you can do incrementally. But 32 literals is small enough that incremental migration produces a permanently half-migrated file, and the half-migrated state is *worse* than no tokens — it removes the ability to audit the palette by grep while providing no single point of change.

A second, sharper variant: **duplicate tokens with divergent meaning.** Green `#2e8b57` has 12 declarations covering both the `写文件` event chip and six distinct buttons. If the token pass emits both `--color-success: #2e8b57` and `--color-action-positive: #2e8b57`, the two are now coupled by value but named as if independent. Then the visual-hierarchy phase darkens the irreversible G3 button (`#btn-authorize`) — and the `写文件` event chip darkens with it, for no reason.

**How to avoid:**
- Make the migration **total and mechanical in one pass**. Define and enforce the invariant: **no hex literal outside `:root`.** 32 literals is a single sitting's work; a partial pass is not.
- Name tokens **semantically** (`--color-text-muted`, `--color-surface-sunken`), never by literal (`--gray-500`). A literal-named token re-encodes the hex and the palette still cannot be re-rationalized — which is the entire point of the milestone.
- Before writing tokens, **assign each of the 32 literals a role**, then collapse. Where two roles genuinely differ, give them two tokens; where they don't, one token and one declaration site change.
- Enforce with a test, not a convention: assert the count of `#` hex literals outside `:root` is 0 (or a pinned, decreasing number).

**Warning signs:**
- `grep -c '#[0-9a-fA-F]\{3,6\}' frontend/style.css` does not fall to ~0 after the token phase.
- A token name contains a color word or a number (`--blue-500`, `--gray-3`).
- Two token names have the same value.
- Any selector outside `:root` still uses a raw hex.

**Phase to address:** Phase A (design contract + token layer). Must be **first** — every other phase's fix (contrast, hierarchy, focus) is a token *value* change, and none of them can be verified while two sources of truth exist.

---

### Pitfall 2: Cascade regression — the `.hidden { display: none !important }` rule and its three ID-specificity competitors

**What goes wrong:**
The single global rule at `style.css:15` is the *only* mechanism keeping roughly 20 elements hidden. A "cleanup" pass that removes, weakens, or relocates it reverts the b9664e0 fix wholesale. I enumerated the exact competitors — the shipped CSS comment is **incomplete and partly wrong** about which ones matter:

| Competitor | Selector | Specificity | Declared | Elements it un-hides |
|-----------|----------|-------------|----------|---------------------|
| `.overlay { display: flex }` (L155) | 0-1-0 | **after** L15 | `#permission-modal`, `#confirmation-modal`, `#tier-modal`, `#mission-complete-modal`, `#cli-check-overlay` |
| `#selection-menu { display: flex }` (L483) | **1-0-0** | after L15 | `#selection-menu` |
| `#annotations-panel { display: flex }` (L398) | **1-0-0** | after L15 | `#annotations-panel` |
| `#checks-panel { display: flex }` (L566) | **1-0-0** | after L15 | `#checks-panel` |

Three of the four competitors win by **ID specificity**, not by source order — so `!important` is required for them regardless of where the rule sits. The existing comment (L13-14) names `.overlay/.doc-subview`; **`.doc-subview` has no `display` declaration at all** (verified: it appears only in `index.html` and in that comment), and the three ID competitors are unlisted. A refactorer who trusts the comment will conclude the ID cases are safe.

**Concrete failure scenarios:**
1. Rewrite `.hidden` as `:where(.hidden)` to "reduce specificity" → specificity drops to **0-0-0**, losing even to `.overlay`. **All five modals render simultaneously** as stacked `position: fixed; inset: 0` overlays with `rgba(0,0,0,.45)` backdrops. The last in DOM order (`#cli-check-overlay`) paints on top and `overlay.classList.add('hidden')` at `app.js:1628` becomes a no-op — **the app is permanently covered by the "启动前自检" overlay even after the CLI check passes.** Total app block.
2. Wrap the stylesheet in `@layer` → unlayered styles always beat layered ones, so `.overlay`/`#selection-menu`/`#annotations-panel`/`#checks-panel` (if unlayered, or in a later layer) win. `#checks-panel` keeps its initial `class="hidden"` from `index.html:108` and, because `applySessionGates` never touches it in the phase 1-2 branch, **the 自检报告 panel is visible from first page load** in phases 1-2.
3. Drop `!important` entirely: `#annotations-panel` becomes visible in phase 1-2, contradicting `app.js:352` (`annotationsPanel.classList.add('hidden')` — the D-P2-2 contract that phases 1-2 show 会话流, not 批注流).
4. Drop `!important` for `#selection-menu`: `hideSelectionMenu()` (`app.js:1284`) becomes a no-op **but `showSelectionMenu` has already written inline `style.left`/`style.top`** (`app.js:1304-1305`). So after the *first* text selection the 划词小菜单 stays **permanently pinned at that spot on the document**, covering content, un-dismissable (the `mousedown` closer at `app.js:1340` and the `scroll` closer at `app.js:1345` both route through `hideSelectionMenu`), and its two buttons are dead (`menuSelection` was nulled, so both handlers `return` at `app.js:1351` / `1381`).

**Why it happens:**
`!important` reads as code smell. Every styleguide says avoid it. A token-layer author with good instincts will try to remove it — and here that instinct is exactly wrong.

**How to avoid:**
- Treat `.hidden { display: none !important; }` as **load-bearing infrastructure, not styling.** Keep it unlayered, keep it `!important`, keep it a single rule.
- **Correct the comment** at L13-14 to name the real competitors: `.overlay` (order) and `#selection-menu` / `#annotations-panel` / `#checks-panel` (ID specificity). The comment is the only defense a future reader has.
- Pin it with an automated gate: `grep -c 'display: none !important' style.css` must equal `1`, and total `!important` occurrences in `style.css` must remain `1`.
- **Never add `!important` to a new tokenized declaration to win a specificity fight.** That converts a one-off into an arms race and will eventually collide with `.hidden`. Concrete collision: someone writes `#stream-banner { display: flex !important }` to beat something → `hideStreamBanner()` (`app.js:145`) can never hide the banner → **the SSE banner says "事件流已断开" while the stream is perfectly healthy, forever** — which destroys the exact distinction (disconnected vs idle) that fix UI-6.2 was built to create.
- Introduce `@layer` **only if** you also layer the entire legacy sheet in the correct order. For a 632-line stylesheet with 26 `display` declarations, the risk/benefit is not worth it. Recommend: do not introduce `@layer` in this milestone.

**Warning signs:**
- Any diff touching `style.css:13-15`.
- New `@layer`, `:where(`, or `:is(` at the top level of `style.css`.
- `!important` count rises above 1.
- Any of `#draft-empty`, `#rounds-hint`, `#btn-process-round`, `#round-switcher`, `#writing-hint` gains a `display` declaration.

**Phase to address:** Phase A (token layer) — as an explicit written constraint in UI-SPEC.md — and re-asserted as a gate in every subsequent phase.

---

### Pitfall 3: Regressing the five just-shipped functional BLOCKER fixes

**What goes wrong:**
All five fixes are CSS-coupled and were verified only by grep counts + manual checks. Each has a specific, plausible way for the visual milestone to undo it:

| Fix | Commit | What the visual phase could break | Concrete failure |
|-----|--------|-----------------------------------|------------------|
| **UI-1.1/1.2/2.5** `.hidden` no-ops | `ed14c6e` | Pitfall 2 (above) | Draft renders **and** "尚无草稿——和 AI 讨论出实质进展后,它会写入 docs/draft.md。" shows at once; the stale "已进入轮次阶段(本阶段占位)。" placeholder returns above the real round document |
| **UI-6.3** archive read-only gating | `ed14c6e` | If the archive view is made to reuse `loadRoundView` for DRY-ness | `updateFrozenPresentation(true)` (`app.js:1166`) sets `processRoundBtn.disabled = processInFlight`, **resetting the `disabled = true` that `applyArchiveView` set at `app.js:818`.** The read-only archive then shows a clickable 「处理本轮批注」, violating §7.4 / D-P3-25 |
| **UI-6.2** SSE disconnect banner | `f7eae48` | If `#stream-banner.fatal` (L227) is folded into a `--color-danger-*` token and the modifier selector is dropped or renamed | Non-fatal (`#8a6508` on `#fff3c4` = **4.78:1**, passes AA) and fatal (`#c0392b` on `#fdecea` = **4.76:1**, passes AA) collapse to the same amber. "无法自动恢复,请刷新页面" then looks identical to "正在自动重连" — **the user waits for a reconnect that will never come** |
| **UI-6.1** keyboard selection path | `0912429` | Adding `tabindex` to `#round-doc` (see Pitfall 6), or moving `#selection-menu` in the DOM (see below) | `#selection-menu` is `position: absolute` and positioned with `window.scrollX/scrollY + rect` (`app.js:1294-1295`). It is a **direct child of `<body>`** (`index.html:200`) — deliberately. If anyone moves it inside `#round-doc` or `#doc-pane` for "DOM locality", and any ancestor has `filter` or `transform`, the containing block changes and **the menu lands in the wrong place**. `#round-doc.round-frozen { filter: saturate(0.6) }` (L509) and `opacity: 0.55` (L508) both create containing blocks / stacking contexts — a `z-index: 200` menu inside them would be trapped *under* sibling content |
| **UI-1.4** inline errors | `0912429` | See Critical Pitfall 10 — this fix has a **latent defect already shipped** | — |

**Why it happens:**
The fixes are recorded as "done." Nothing in the repo prevents a later phase from editing the CSS they depend on, and the verification artifacts (`260916-t8g-SUMMARY.md`) explicitly mark every one as `human_judgment: true` — meaning **no automated test will catch a regression.**

**How to avoid:**
- Every phase plan in this milestone must carry an explicit **"do not touch" list**: `style.css:13-15`, the `.fatal` modifier, `applyArchiveView`'s two lines (`app.js:817-818`), and the `#selection-menu` DOM position.
- Re-run the five manual checks from `260916-t8g-SUMMARY.md` (PLAN 人工检查 items 3 and 5-6) **at the end of the milestone**, not just at the phase that nominally "owns" accessibility.
- Add `processRoundBtn.disabled = true` to the *end* of `loadArchiveView()` (after `loadChecksView`), mirroring the existing G-idi03-3 precedent at `app.js:844-845` where the same class of reset was already found and fixed once. This is the same bug shape; the archive path has a known second entry point.
- Keep the archive path on `loadArchiveRoundDoc`, **not** `loadRoundView`. If DRY-ing them, the archive branch must not call `updateFrozenPresentation`.

**Warning signs:**
- A diff touches `applyArchiveView`, `updateFrozenPresentation`, `loadRoundView`, or `hideStreamBanner`.
- `#stream-banner.fatal` loses its `.fatal` selector or gains a tokenized color that no longer differs from the base.
- Any refactor that makes `loadRoundView` reachable in `mission_complete`.

**Phase to address:** Constraint in Phase A's UI-SPEC; regression re-verification in Phase E.

---

### Pitfall 4: Contrast fixed to the ratio, hierarchy destroyed — and opacity is not a color token

**What goes wrong:**
Two distinct failures.

**(a) The naive AA fix flattens the visual hierarchy.** I computed the real numbers:

| Element | Current | Ratio | Minimum passing gray | Naive "safe" choice |
|---------|---------|-------|---------------------|---------------------|
| `.hint` `#999` on `#fafafa` | 2.73:1 | ✗ | `#737373` (4.54:1) | `#666666` (5.50:1) |
| Body text `#1a1a1a` on `#fafafa` | 16.67:1 | ✓ | — | — |

`.hint` is the tool's **primary explanatory text** — every gate precondition (`#authorize-hint`, `#approve-hint`, `#writing-hint`), every recovery instruction, every inline note. If it is fixed by reusing `#666` (the "obvious dark gray"), the hint lands at **5.50:1** — exactly the same as `.markdown-body blockquote` (`#666` on `#fafafa` = **5.50:1**) and `.verdict-suggestion` (`#666` on `#fffdf5` = **5.64:1**). Hints, pull-quotes, and AI repair suggestions all become the same visual rank. Worse, `.hint` is 13px while the document body is 14px `#1a1a1a` — so the hint becomes **nearly as loud as the primary content but smaller**, i.e. harder to read *and* competing with the thing it is supposed to be subordinate to.

The measured hierarchy collapse: hint/body contrast ratio goes from **0.164** (current) → **0.33** (at `#666`). At the minimum passing `#737373` it is **0.27**, which preserves separation. **The correct fix is the lightest gray that passes, not the darkest one that feels safe.**

**(b) `opacity` de-emphasis cannot be fixed by any palette change.** This is the trap that survives a "we fixed all the contrast failures" declaration:

| Element | Source | Composited color | Actual ratio |
|---------|--------|------------------|--------------|
| `.annotation-answered { opacity: 0.65 }` (L454) | `#999` over `#fff` | `#bdbdbd` | **1.88:1** |
| `.annotation-plain` (L461) | `#999` over `#fff`, no opacity | `#999999` | 2.85:1 |
| `#round-doc.round-frozen { opacity: 0.55 }` (L508) | `#1a1a1a` over `#fafafa` | `#7f7f7f` | **3.84:1** |
| `#rounds-placeholder.archive-mode #round-doc { opacity: 0.75 }` (L628) | `#1a1a1a` over `#fafafa` | `#525252` | 7.49:1 |
| `.badge-answered` `#999` on `#f5f5f5` (L447) | literal | `#999999` | **2.61:1** |

The UI audit flagged four AA failures; I verified those numbers and **found five more it missed** — including `.badge-answered` (2.61:1), `.annotation-answered` (1.88:1), and the G3 authorization button's own label:

> `#btn-authorize { color: #2e8b57; background: #e9f7ef }` → **3.84:1** — fails AA, and it is the *only* text on the project's Core-Value control. The same pair is shared by all six green buttons (`#btn-approve-draft`, `#btn-process-round`, `#btn-authorize`, `#btn-start-writing`, `#btn-continue-check`, `#btn-continue-repair`).
>
> Also failing: `.kind-say .event-kind` white on `#2c7be5` = **4.14:1**; `.kind-write .event-kind` white on `#2e8b57` = **4.25:1**; `.kind-command .event-kind` white on `#b8860b` = **3.25:1**.

So "fix the 4 contrast failures" is the wrong frame — the real count is **at least nine**, and fixing the four named ones while leaving `.annotation-answered` at 1.88:1 means §4.2's "已回应…变灰不删除" content is effectively unreadable while the milestone declares AA compliance.

**Why it happens:**
- Contrast tools output a pass/fail, not a hierarchy check. Nobody computes "what did this do to the *relationship* between elements."
- `opacity` looks like a de-emphasis *style* rather than a contrast *multiplier*. It also feels more principled than a hardcoded gray — so a token author will happily add `--opacity-deemphasized: 0.65` and apply it uniformly. That silently **lightens** `.round-frozen` (0.55 → 0.65) and **darkens** the archive view (0.75 → 0.65). The archive view is the terminal read-only state — the only way to read the finished DESIGN.md in-app — and it is the one state that must not regress.

**How to avoid:**
- Fix contrast **by choosing the minimum passing value, then explicitly re-checking the hierarchy**: after the change, `.hint` must still be visibly lighter than `.markdown-body p`. Assert hint/body ratio stays ≤ ~0.30.
- **Ban `opacity` for text de-emphasis in UI-SPEC.md.** De-emphasis must be a color token. Convert `.annotation-answered`, `.annotation-plain`, `.round-frozen`, `.badge-answered`, `.tier-desc` (`opacity: 0.8`) to explicit muted tokens. Reserve `opacity` for non-text (`.round-frozen`'s container dimming is defensible, but then it must not wrap text that must remain readable).
- Audit the **opacity-composited** values, not just the declared ones. This is the class of failure the existing audit missed entirely.
- Re-derive the failure list from scratch rather than trusting the audit's count of four. Treat the audit's numbers as a starting point that has already been shown to be incomplete.
- Give `#btn-authorize` its own token pair that satisfies AA **and** reads as irreversible (see Pitfall 8 on the green-overload problem).

**Warning signs:**
- `.hint` resolves to the same value as `.markdown-body blockquote` or `.verdict-suggestion`.
- Any `opacity` value is applied to an element containing body text.
- A "contrast fixed" claim is made without a recomputed table of composited colors.
- The count of fixed failures is exactly 4.

**Phase to address:** Phase C (accessibility). The opacity→token conversion must land in Phase A (it is a palette decision) with the value changes in Phase C.

---

### Pitfall 5: Focus styles that shift layout or get clipped in the nested-scroll sidebar

**What goes wrong:**
`:focus` count is currently **0** across all three files. There are 21 buttons, 8 inputs, and 4 selects. The naive `*:focus { outline: 2px solid var(--color-focus) }` has four failure modes here:

1. **Layout shift if implemented as `border`.** `#ai-route-select`, `#project-path-input`, `#enter-path-input`, `#chat-input-row input`, `#round-switcher`, `#check-switcher`, and `.verdict-note-input` all use `border: 1px solid #ccc`. Changing the border to 2px on focus shifts each control by 1px and **reflows `#probe-controls`** (`display: flex; gap: 8px`), making the 「发起测试调用」/「处理本轮批注」/「中止」 buttons jump on every Tab. `outline` and `box-shadow` do not affect layout — **use those.**

2. **Clipping in the nested scroll containers.** `outline` is painted outside the border box and is clipped by `overflow: auto`. The measured padding of each scroll container:

   | Container | padding | Fits 2px ring + 2px offset (needs 4px)? |
   |-----------|---------|------------------------------------------|
   | `.event-list` | 8px | yes |
   | `#latest-check` | 6px 8px | yes |
   | `#chat-messages` | 4px **2px** | **no — clipped left/right** |
   | `#annotation-list` | **2px** | **no — clipped on all sides** |
   | `#sidebar` | 0 | **no** |

   `#chat-messages` and `#annotation-list` hold focusable content (chat is read-only today, but `.annotation-answer summary` is a native focusable disclosure widget at `app.js:1140`). A clipped ring on the summary element reads as "focus lost."

3. **The ring is multiplied by ancestor `opacity`.** `#round-doc.round-frozen { opacity: 0.55 }` (L508) and `#rounds-placeholder.archive-mode #round-doc { opacity: 0.75 }` (L628) create stacking contexts that composite *everything* inside, including focus rings. Computed:

   | Ring color | No opacity | In `.archive-mode` (0.75) | In `.round-frozen` (0.55) |
   |-----------|-----------|---------------------------|---------------------------|
   | `#2c7be5` (primary) | 3.97:1 | **2.73:1** ✗ | **2.05:1** ✗ |
   | `#1f5cb0` (darkened) | 6.26:1 | 3.67:1 | **2.48:1** ✗ |
   | `#000000` | 20.12:1 | 10.25:1 | 4.74:1 |

   **`#2c7be5` as a focus ring is only 3.97:1 against `#fafafa` even at full opacity** — it barely clears the 3:1 non-text minimum (WCAG 1.4.11) before any dimming. Inside a frozen or archived document it drops to 2.05:1 / 2.73:1, i.e. **fails**. Any focusable element inside `.round-frozen` or `.archive-mode` needs either a near-black ring or an `outline` that is not inside the dimmed subtree.

4. **A ring around a very tall container is invisible.** `#round-doc` renders an entire DESIGN.md — thousands of pixels tall inside `#doc-pane { overflow-y: auto }`. If `tabindex` is added to it (Pitfall 6), the outline wraps the *whole* box, so the only visible parts are the top and bottom edges, which are almost never in the viewport. The user tabs in and sees nothing. Correct patterns: an inset `box-shadow`, a ring on a small wrapper, or a visible focus treatment on `#doc-pane` itself with `tabindex="-1"` for programmatic focus.

**Why it happens:**
`*:focus { outline: ... }` is the canonical one-liner and it looks correct in a short static page. The failure modes only appear with nested scroll containers and dimmed subtrees — both of which this app has and a demo does not.

**How to avoid:**
- Use `outline` with `outline-offset`, **never** `border`, for focus. Add `:focus-visible` for the ring and leave `:focus` available for programmatic focus.
- Choose a ring color that survives dimming: verify ≥3:1 against `#fafafa` **and** against `#fafafa` composited at 0.55.
- Bump `#chat-messages` (2px) and `#annotation-list` (2px) horizontal padding, or use `outline-offset: -2px` (inset) for elements inside those containers. Pick one rule and state it in UI-SPEC.md.
- Do **not** put a ring on `#round-doc` as a whole. If the document region needs focus affordance, ring `#doc-pane`.
- Add `prefers-reduced-motion` in the same commit as any `transition` (see Moderate Pitfall M3).

**Warning signs:**
- A focus rule that sets `border` or `padding`.
- A ring color that was not checked against the `.round-frozen` / `.archive-mode` composited background.
- `:focus` used without `:focus-visible` (rings appear on every mouse click).
- No verification step that tabs through the app with the sidebar scrolled to the bottom.

**Phase to address:** Phase C (accessibility). The padding changes to `#chat-messages` / `#annotation-list` belong to Phase D (layout) but must be coordinated — splitting them produces a window where the ring is clipped.

---

### Pitfall 6: `tabindex` without `:focus` — and the roadmap splitting them across phases

**What goes wrong:**
PROJECT.md already records the rule: "`tabindex` 与 focus 样式必须一起定". The pitfall is the roadmap *violating* it by scheduling them in different phases, plus the specific consequences of `tabindex` here.

The trigger is real and well-motivated: `260916-t8g-SUMMARY.md` documents the known limitation that "`#round-doc` 是不可聚焦的普通 div,keyup 仅在焦点已落在容器内时生效" — i.e. the keyboard annotation path (fix UI-6.1) **still requires one mouse click** to focus the document. The obvious fix is `tabindex="0"` on `#round-doc`. Doing so produces three defects at once:

1. **A new invisible tab stop.** With `:focus` count still 0, the user tabs from the sidebar into the document and focus vanishes. There is no way to tell where they are.
2. **Every keystroke in the document now runs `handleSelectionTrigger`.** `roundDoc.addEventListener('keyup', handleSelectionTrigger)` (`app.js:1337`). The handler's collapsed/empty-selection guard means any keypress with no selection calls `hideSelectionMenu()` (`app.js:1318`). Combined with the existing `document.addEventListener('mousedown', ...)` closer (`app.js:1340`) and `window.addEventListener('scroll', hideSelectionMenu, true)` (`app.js:1345`, capture phase), the menu already has **three** independent closers. Adding a focusable container adds a fourth interaction surface without adding a way to *keep* the menu open.
3. **`tabindex="0"` on a bare `div` with no `role`** is announced by screen readers as a generic container. This milestone must decide: `role="region"` + `aria-label`, or no `tabindex` at all and a different keyboard affordance (e.g. a visible 「批注」button that operates on the current selection). The latter is simpler and does not add a tab stop.

**Why it happens:**
`tabindex` is a one-attribute change that feels self-contained; `:focus` styling feels like a separate "polish" task. Splitting them is natural in a phased roadmap and always wrong.

**How to avoid:**
- **Hard rule in UI-SPEC.md:** any commit adding `tabindex` must add the corresponding `:focus`/`:focus-visible` treatment in the same commit. Enforce with a gate: `grep -c tabindex` and `grep -c ':focus'` must not be able to move independently (assert both are 0 or both are > 0).
- Prefer **not** adding `tabindex` to `#round-doc`. The simpler path is to leave the one-click focus requirement and document it, or to make the annotation action reachable from a real button.
- If `tabindex` is added, re-run the UI-6.1 manual UAT — the documented "先聚焦文档区这一步仍需鼠标点击一次" limitation no longer holds, so **the previously-passed manual check is now testing a different thing.** PROJECT.md records that keyboard text selection **cannot be automated** ("连 `contenteditable` 都选不中"), so this must be scheduled as a manual check.
- Add `role`/`aria-*` deliberately or not at all — the audit's scope note excluded them, and the milestone should either adopt them with a plan or explicitly defer them.

**Warning signs:**
- `tabindex` appears in a diff with no `:focus` rule.
- A phase plan lists "add tabindex" and "add focus styles" as separate tasks in separate phases.
- The UI-6.1 manual check is marked passed by inheritance rather than re-run.

**Phase to address:** Phase C (accessibility) — `tabindex` and `:focus` in the **same** commit; the UI-6.1 re-check in Phase E.

---

### Pitfall 7: Emoji-as-icon replacement drags in an icon dependency and breaks the collapse indicator

**What goes wrong:**
The audit flagged two `content:`-based emoji: `.annotation-quote::before { content: '📌 ' }` (L431) and `.verdict-location::before { content: '📍 ' }` (L612). There are also two text-glyph indicators: `.collapse-indicator` renders `▾` (`index.html:129`) and is mutated in JS.

Constraints that make the "obvious" fix wrong:
- **No icon system exists** — no SVG, no icon font. The only vendored asset is `vendor/marked.min.js`, explicitly commented "无 CDN 网络依赖" (`index.html:214`). **D-03 (单机单人本地) forbids a CDN icon font.**
- Adding an icon font or SVG sprite for **two glyphs** contradicts repo CLAUDE.md §2 (简单优先) and adds a vendored binary dependency.

**The concrete breakage:** the collapse indicator is driven by JS:
```js
panelHeader.querySelector('.collapse-indicator').textContent = collapsed ? '▸' : '▾';
```
(`app.js:1550`). If the glyph is replaced with an inline `<svg>` inside `.collapse-indicator`, this `textContent` assignment **erases the SVG** — `textContent = ` replaces *all* children with a text node. Result: `#ai-panel` — the **only** collapsible panel in the app (audit finding 6.10) — loses its collapse affordance entirely, silently. A blank spot where the indicator was.

Also: emoji inside `::before { content }` are **not in the DOM**. No `aria-hidden` can reach them, and screen readers announce "pushpin" / "round pushpin". Any fix that makes them accessible requires moving them into the DOM — which means editing `renderAnnotations` (`app.js:1122-1126`) and `renderVerdictCard` (`app.js:671-673`), i.e. touching the shipped annotation rendering path (UI-01/UI-02 behavior).

**How to avoid:**
- **Scope this tightly: 2 `content:` emoji + 2 indicator glyphs.** Do not introduce an icon system.
- Replace `content: '📌 '` with a **CSS-only** treatment (a tokenized left border / background tint on `.annotation-quote`, matching the existing `.annotation-pending-item { border-left: 3px solid ... }` pattern at L451). No DOM change, no dependency, no accessibility regression.
- If a glyph must stay, keep it as `content` (decorative, not announced as meaningful) rather than moving it into the DOM.
- For the collapse indicator: drive it with `classList.toggle('collapsed')` on the header and express the glyph in CSS (`::after` with `content`), **not** `textContent`. If the JS must change, change it in the same commit as the CSS.
- Do not touch `renderAnnotations` / `renderVerdictCard` in a visual milestone — they are verified paths.

**Warning signs:**
- A new file under `frontend/vendor/`, or any `<link>` to a font CDN.
- `app.js:1550` in a diff without a matching CSS change.
- A diff touching `renderAnnotations` or `renderVerdictCard`.

**Phase to address:** Phase B (visual hierarchy). Explicitly out-of-scope in UI-SPEC.md: "no icon system."

---

### Pitfall 8: Scope creep — "fix the visual debt" becomes "redesign the product"

**What goes wrong:**
The UI audit lists 7 BLOCKERs and ~40 findings. Only a subset is in v1.14's target features. The rest are **product and behavior decisions** that a visual milestone will absorb by default because they are sitting in the same document. Concrete escalation paths, each with a real cost:

1. **Removing `#probe-controls`** (audit 6.6: dev scaffolding in the primary UI — an A/B route switch, a second path input, a 「发起测试调用」button). This is *required* by DESIGN.md D-06/§9: the two AICaller routes must be switchable at runtime and the contract "两路线界面契约完全一致" must remain testable. Removing it breaks AI-03's verification surface. **Not a visual decision.**
2. **Replacing the two `window.prompt` calls** (audit 1.3, `app.js:486` and `app.js:1354`) with styled modals. This is a **behavior change** to the annotation flow (UI-01) and the G3 rejection path (FLOW-05 / D-P3-5). `window.prompt` returns `null` on cancel, and both call sites branch on that (`app.js:487`, `app.js:1355`) — a custom modal must reproduce the cancel semantics exactly. Feature work with a UAT surface.
3. **Fixing `#state-badge { right: 448px }`.** The coupling fix (derive from a `--sidebar-width` token) is in scope. **Restructuring the header is not** — the badge is `position: fixed` inside `#doc-pane` and has a deliberate z-index relationship with `#stream-banner` (`z-index: 10` vs `20`). Moving it into normal flow changes scroll behavior for a shipped element.
4. **Responsive design.** Zero `@media` rules exist today. PROJECT.md scopes this as "窄窗口不破版" — a *floor*, not a responsive redesign. D-03 says 单机单人本地; the realistic target is a desktop window (≥1024px), not 375px. A full stacking/mobile layout is a new capability.
5. **Dark mode.** `prefers-color-scheme` count is 0 and dark mode is **not** in the milestone's target features. The trap: tokens make it feel cheap. In reality it **doubles the contrast audit** — every pair must be re-verified, and the 7-color event-kind palette plus the green/amber/red semantic families all need dark variants. This is the single most likely creep vector once Phase A lands.

**Why it happens:**
Tokens create affordance. Once `--color-*` exists, "we should also…" becomes a 20-minute change. And the audit document, sitting in the same `.planning/` tree, reads as a to-do list rather than a triage output.

**How to avoid:**
- Write an explicit **"Not in v1.14"** table into UI-SPEC.md, naming each deferred audit finding and *why* (product decision / behavior change / new capability).
- Require every phase plan to cite the milestone target feature it serves. A task that cannot cite one is out of scope.
- Re-state the tech-stack constraints in UI-SPEC.md: no build step, no framework, no CDN, no new vendored dependency.
- Treat `#probe-controls` and the `window.prompt` call sites as **frozen** for this milestone.

**Warning signs:**
- A phase plan mentions dark mode, responsive breakpoints below 1024px, or replacing `window.prompt`.
- A diff removes `#probe-controls` or the `ai-route-select` element.
- `package.json` appears, or any new file appears under `frontend/vendor/`.

**Phase to address:** Phase A (UI-SPEC.md scope fence), enforced at every phase's plan review.

---

### Pitfall 9: Reordering `style.css` is a rendering change — the cascade is declaration-order-dependent

**What goes wrong:**
The natural way to introduce tokens is to **regroup** the stylesheet — all heading rules together, all color rules together. In this file, at least one pair of equal-specificity rules resolves purely by source order:

```
L230  #draft-view h2, #rounds-placeholder h2 { ... font-size: 15px; color: #555; }
L296  #brainstorm-view h2 { ... font-size: 14px; color: #8a6508; }
```

Both have specificity **1-0-1**. `#brainstorm-view` is a **descendant of `#draft-view`** (`index.html:44` inside `index.html:29`), so the `<h2>发散候选(brainstorm.md)</h2>` matches both. L296 is later, so it wins: **14px / `#8a6508`**. Move L230 below L296 and the heading becomes **15px / `#555`** — a visible size *and* color change produced by a pure reorganization.

**Why it happens:**
Regrouping is the instinct when adding tokens, and nobody expects a reorder to change rendering. Equal-specificity conflicts are invisible without tooling.

**How to avoid:**
- **Do not reorder existing rules.** Append new rules, or edit in place. If regrouping is unavoidable, do it in a **separate commit with zero value changes**, so any rendering difference is attributable.
- When converting these two rules to tokens, **also raise specificity** so the outcome no longer depends on order — e.g. scope the brainstorm rule as `#draft-view #brainstorm-view h2`. This is a genuine improvement and removes the landmine.
- Verify by diffing *computed* styles, not source: the whole point is that the source diff looks innocent.

**Warning signs:**
- A diff where `style.css` line numbers for existing selectors change without a value change.
- Any "tidy up the stylesheet" task in a phase plan.

**Phase to address:** Phase A (token layer) — as an explicit "append, do not reorder" rule. Verification in Phase E.

---

### Pitfall 10: The just-shipped inline-error fix has a latent layout defect — `.inline-error` becomes a flex item inside `#probe-controls`

**What goes wrong:**
`showInlineError(anchor, message)` inserts with `anchor.insertAdjacentElement('afterend', p)` (`app.js:309`). One of its five call sites anchors on `processRoundBtn` (`app.js:1452`, `app.js:1461`), which lives inside:

```html
<div id="probe-controls">   <!-- style.css:62-66: display: flex; gap: 8px -->
  <select id="ai-route-select">…</select>
  <input id="project-path-input">          <!-- flex: 1 -->
  <button id="btn-ping">发起测试调用</button>
  <button id="btn-process-round">处理本轮批注</button>   <!-- anchor -->
  <button id="btn-abort" class="danger">中止</button>
</div>
```

So the error `<p class="inline-error">` is inserted **as the sixth flex item in a horizontal flex row**, wedged between 「处理本轮批注」and 「中止」. `.inline-error { color: #c0392b; font-size: 13px; margin: 6px 0 0 }` (L42) has no `flex-basis`, so it takes its content width and shrinks — producing a narrow, wrapped column of red text that compresses the adjacent buttons. Inside the 420px sidebar (`#probe-controls` content width ≈ 388px) that row is already crowded before the error appears.

The other four call sites are safe because their anchors sit in block-flow containers: `enterForm` (sibling in `#doc-pane`), `divergenceBtn` (inside `#divergence-entry`, a plain div), `approveDraftBtn` (inside `#approve-row`, a plain div), `checkSwitcher` (inside `#checks-panel .panel-body`, a flex **column**).

Two secondary issues in the same fix:
- **The `inlineErrorEl` singleton** (`app.js:295`) means only one inline error can exist at a time. Two concurrent failures (e.g. `loadChecksView` failing while an approve error is displayed) silently drop one.
- **`clearInlineError()` is not called on view transitions.** It runs at the start of `enterProject`, `loadChecksView`, and the processRound/divergence/approve handlers (`app.js:314, 592, 1448, 1498, 1522`) — but not when `applySessionGates` switches views. A stale "处理发起失败:…" therefore persists in the AI work panel after the user switches to a historical round or the state advances past phase 3.
- **The `textContent`-only rule is a security mitigation.** The fix deliberately writes errors with `textContent` (never `innerHTML`) so server-returned `message` strings never enter the HTML parse path (T-260916-01). If the visual phase rewrites `.inline-error` rendering — e.g. adds an icon via `innerHTML`, or builds the node from a template literal — **that mitigation silently reverts into an XSS surface.**

**Why it happens:**
The fix was verified by grep counts (`grep -c 'clearInlineError();' == 6`, `grep -c 'inline-error' style.css == 1`) plus a manual check that "错误出现在输入框/按钮正下方而非右下 AI 工作面板". The `#probe-controls` case satisfies that manual check literally — the error *is* adjacent to the button — while being visually broken. Grep and a coarse manual check both pass.

**How to avoid:**
- Fix `#probe-controls` to `flex-wrap: wrap`, or move the error out of the row (e.g. a dedicated `#ai-panel-error` slot below `#probe-controls`), or change the `processRoundBtn` anchor. Prefer the structural fix over a CSS patch.
- Keep `textContent`. Add a written rule to UI-SPEC.md: **error text is never rendered via `innerHTML`.** Consider a gate asserting no `innerHTML` appears in the error path.
- Call `clearInlineError()` from `applySessionGates` so view transitions clear stale errors.
- This defect should be fixed in the phase that owns error/state styling, and the manual check from `260916-t8g-SUMMARY.md` (PLAN 人工检查 item 6) must be re-run with the check extended to "the error does not disturb the control row."

**Warning signs:**
- `.inline-error` appears in a diff and `#probe-controls` does not.
- Any `innerHTML` near `showInlineError`.
- `clearInlineError` call count drops below 6.

**Phase to address:** Phase D (layout / interaction states) for the row fix; Phase C for the `textContent` invariant.

---

## Moderate Pitfalls

### M1: Verification by grep count — the milestone can "pass" without rendering correctly

The five shipped fixes were verified with assertions like `grep -c 'source.onerror' == 1` and `grep -c 'var(--'`. The prior run already produced a **gate arithmetic error** (`showInlineError(` expected 6, actual 9) that was reported rather than fixed. A token/CSS milestone is *more* grep-friendly and *less* semantically verifiable than the fix it follows: `grep -c 'var(--'` proves nothing about how anything renders.

Compounding environment facts from PROJECT.md:
- **Screenshots are unavailable.** The v1.13 audit could not capture any: "headless browser rendering is blocked in this environment (Chrome, Chrome-for-Testing, and `chrome-headless-shell` all failed; the app's persistent `/api/events` SSE stream also prevents the capture handler from terminating)."
- **Playwright must use `chromium.launch({ channel: 'chrome' })`** — the bundled Chromium version does not match.
- **Keyboard text selection cannot be automated** — "连 `contenteditable` 都选不中". Shift+Arrow acceptance items must be flagged as manual.

**Prevention:** every phase needs at least one *runtime* verification, not only static counts. Where the check is manual, the plan must name the exact steps (which view, which element, which window width, what to observe). Budget manual checks explicitly; they cannot be offloaded to automation.

### M2: `#state-badge` / `#stream-banner` fixed-position collision at narrow widths

Both are `position: fixed; top: 12px`. The badge is `right: 448px` (hardcoded to sidebar 420px + 28px, `style.css:202`); the banner is `left: 50%; transform: translateX(-50%)` with `z-index: 20` against the badge's `z-index: 10`. Computed overlap:

| Viewport | Banner span | Badge span | Overlap |
|----------|-------------|-----------|---------|
| 1440px | 570–870 | 902–992 | 0px |
| 1280px | 490–790 | 742–832 | **48px** |
| 1024px | 362–662 | 486–576 | **90px** |
| 768px | 234–534 | 230–320 | **86px** |

The banner (higher z-index) **covers the badge** — and `#state-badge` is the only place the derived state is shown (`app.js:340`). During a disconnect the user loses the state readout. The layout phase's `--sidebar-width` token fix must also resolve this collision, and the fix must not move `#state-badge` into normal flow (see Pitfall 8, item 3).

### M3: A global `transition` breaks panel semantics and ignores reduced motion

Only one `transition` exists today (`.event-list { transition: background-color 0.3s }`, L107), and `renderEvent` sets `eventsEl.scrollTop = eventsEl.scrollHeight` on **every** event (`app.js:240`). A broad rule like `* { transition: all .2s }` makes `eventsEl.classList.add('streaming')` / `.remove('streaming')` animate the whole panel background on every call start and end — a full-panel flash on each operation. `@media` count is 0, so there is no `prefers-reduced-motion` guard; adding transitions without it violates WCAG 2.3.3 for motion-sensitive users. **Add `prefers-reduced-motion` in the same commit as any new transition.**

Also: a transition on `opacity` for "smooth hiding" cannot work against `.hidden { display: none !important }` — nothing transitions from `display: none`. The tempting workaround is to replace `display: none` with `visibility`/`opacity`, which re-opens Pitfall 2 **and** leaves hidden content reachable by Tab and by screen readers. Do not do this.

### M4: Chrome `h2` and content `h2` share one tag — a global type scale collides

`.markdown-body h1/h2/h3` have **no** `font-size` rule (L240-243), so rendered-document headings fall back to UA defaults relative to `.markdown-body { font-size: 14px }` → 28 / 21 / 16.4px. Meanwhile four **chrome** headings are `<h2>` with literal overrides: `.panel-header h2` 14px (L56), `#draft-view h2` / `#rounds-placeholder h2` 15px (L230), `#brainstorm-view h2` 14px (L296), `.overlay-card h3` 16px (L169). A single global `h1,h2,h3 { font-size: var(--fs-heading-N) }` will collide with all four. **Scope content typography under `.markdown-body` and treat chrome headings as a separate token family** — otherwise the panel titles and the AI-authored document headings drift against each other.

### M5: Weakening the `:disabled` token destroys the only G3 precondition signal

There are 8 `:disabled` rules using `opacity: .55` / `.5` plus `cursor: not-allowed`. `#btn-authorize` is disabled until all four mechanical checks pass (`app.js:441-446`), and the `disabled` state is the **only** visual signal of that precondition — the `title` and `#authorize-hint` are supplementary. If the disabled token is softened for "legibility" (e.g. `opacity: .55 → .8`), the button looks enabled while being unclickable, and the user clicks a dead G3 control. **The disabled treatment must remain unambiguous, and it must differ from the `:hover` state.**

### M6: `#confirm-error` carries `class="hint"` — the `.hint` rewrite can gray out the G3 failure message

`index.html:168`: `<p id="confirm-error" class="hint hidden">`. It is currently red because `#confirm-error { color: #c0392b }` (L550, specificity 1-0-0) beats `.hint` (L39, 0-1-0). If the token phase rewrites `#confirm-error` as a **class** (`.confirm-error`), both selectors become 0-1-0 and the winner is decided by source order — and `.hint` is at L39 while the modal block is at L550, so it still wins. But if the `.hint` rule is later moved or given higher specificity, **the G3 confirmation failure message reverts to gray** and reads as a hint rather than an error. Keep the ID, or explicitly set the error color with equal-or-higher specificity.

### M7: `aria-live` on a streaming region without a politeness budget

`#chat-messages` receives streamed AI output chunk-by-chunk via `appendSayToChat` (`app.js:271-281`), one DOM append per SSE event. If the a11y phase adds `aria-live="polite"` to announce streaming, every chunk triggers an announcement — on a multi-minute AI call this makes the region unusable with a screen reader. Announce at the *bubble* level (`streamingBubble`) with `aria-busy`, or use `role="log"`, and never on the chunk container.

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Migrate only the selectors you're editing to tokens | Smaller, safer-looking diffs | Permanently half-migrated file; palette can no longer be audited by grep; contrast fixes apply inconsistently | **Never** — 32 literals is one sitting's work |
| Keep `opacity` for text de-emphasis and add an `--opacity-*` token | Feels principled and tokenized | Contrast cannot be fixed by any palette change; `.annotation-answered` stays at 1.88:1 while the milestone declares AA done | Never for text. Acceptable for container dimming only if no readable text is inside |
| Add `!important` to a new declaration to win a specificity fight | Fixes the immediate conflict | Arms race; eventually collides with `.hidden` and permanently sticks a modal or the SSE banner on screen | **Never** — fix specificity instead |
| Regroup/reorder `style.css` while adding tokens | Tidier file | Changes rendering at equal-specificity conflicts (`#brainstorm-view h2` 14px→15px); the source diff looks innocent | Only as a separate commit with zero value changes |
| Introduce `@layer` for "proper cascade control" | Modern, principled | Unlayered legacy rules beat layered ones; requires layering all 632 lines correctly | Not in this milestone |
| Verify CSS changes with `grep -c` | Fast, automatable | Proves nothing about rendering; the prior fix already produced a gate arithmetic error | As a supplement only — never as the sole gate |
| Add `tabindex` now, `:focus` in the a11y phase | Lets the keyboard path land early | Ships an invisible tab stop; PROJECT.md's own rule forbids it | **Never** — same commit |
| Keep emoji icons because "it's only two glyphs" | Zero dependencies, zero risk | Inconsistent cross-platform rendering; announced as "pushpin" by screen readers | Acceptable — and *preferable* to introducing an icon system for two glyphs |

---

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| `marked` rendered output ↔ typography tokens | Styling `h1/h2/h3` globally, colliding with the four chrome `<h2>` overrides | Scope all content typography under `.markdown-body`; keep chrome headings on a separate token family |
| `.hidden` ↔ any new `display` declaration | Adding `display` to a `hidden`-carrying element's own selector, or adding `!important` elsewhere | `.hidden` stays the single unlayered `!important` rule; never add `!important` to another `display` |
| `#selection-menu` ↔ ancestor `filter`/`transform`/`opacity` | Moving the menu inside `#round-doc` / `#doc-pane` for DOM locality | Keep it a direct child of `<body>`; `filter`/`opacity` ancestors create containing blocks and stacking contexts |
| Focus rings ↔ `overflow: auto` ancestors | Assuming `outline-offset: 2px` fits everywhere | `#chat-messages` (2px horizontal) and `#annotation-list` (2px) clip it; use inset offset or add padding |
| Focus rings ↔ `opacity` ancestors | Picking a ring color against the un-dimmed background | Verify against the composited background at 0.55 and 0.75; `#2c7be5` drops to 2.05:1 / 2.73:1 |
| `EventSource` reconnect ↔ tokenized banner colors | Folding `.fatal` into a shared danger token and dropping the modifier | Keep `#stream-banner.fatal` as a distinct selector and re-verify both states meet AA (currently 4.78 / 4.76) |
| Archive read-only ↔ `updateFrozenPresentation` | DRY-ing `loadArchiveRoundDoc` into `loadRoundView` | Keep them separate; `updateFrozenPresentation(true)` resets `processRoundBtn.disabled` |
| Server error `message` ↔ error rendering | Adding an icon via `innerHTML` in `showInlineError` | `textContent` only — it is an XSS mitigation (T-260916-01), not a style choice |

---

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Hints darkened to the minimum-ratio "safe" gray (`#666`) | The least important text competes with the primary content, and is *smaller* — harder to read and louder at once | Pick the **lightest** passing value (`#737373`, 4.54:1); assert hint/body ratio stays ≤ ~0.30 |
| `opacity`-based de-emphasis on answered annotations | "已回应" content sits at 1.88:1 — §4.2's "变灰不删除" becomes "变灰到读不了" | Move de-emphasis to color tokens; keep the content readable |
| Green used for both the irreversible G3 authorization and routine 「继续自检」 | The project's Core-Value red line is visually identical to a routine action | Distinct token pair for `#btn-authorize`; AA-compliant (current `#2e8b57` on `#e9f7ef` is 3.84:1) |
| Softened `:disabled` opacity | A dead G3 button looks clickable | Keep the disabled treatment unambiguous and distinct from `:hover` |
| Focus ring invisible in a scrolled sidebar or dimmed subtree | Keyboard users lose their place; the app appears broken | Inset rings, ring color verified against composited backgrounds |
| Inline error inserted into the `#probe-controls` flex row | Error text squeezes between 「处理本轮批注」and 「中止」, compressing both | `flex-wrap` or a dedicated error slot below the row |
| Stale inline error persisting across view changes | The user reads an error for a state they have already left | Call `clearInlineError()` from `applySessionGates` |
| Emoji as the only iconography | Renders differently per platform; screen readers say "pushpin" | CSS-only decorative treatment, or keep as `content` |

---

## "Looks Done But Isn't" Checklist

- [ ] **Token layer:** `grep -c '#[0-9a-fA-F]\{3,6\}' frontend/style.css` is ~0 outside `:root` — verify no literal remains, not just that `:root` exists.
- [ ] **Token layer:** no two token names share a value, and no token name contains a color word or a number.
- [ ] **Cascade:** `grep -c 'display: none !important' frontend/style.css` == `1` and total `!important` count == `1` — verify the count did not rise.
- [ ] **Cascade:** `.overlay`, `#selection-menu`, `#annotations-panel`, `#checks-panel` are all still hidden when their `hidden` class is set — verify in a browser, not by reading CSS.
- [ ] **Cascade:** the comment at `style.css:13-14` names the real competitors (`.overlay` by order; `#selection-menu` / `#annotations-panel` / `#checks-panel` by ID specificity) — `.doc-subview` has no `display` rule and should not be cited.
- [ ] **Shipped fixes:** all five manual checks from `260916-t8g-SUMMARY.md` re-run at milestone end, including PLAN items 3, 5, and 6.
- [ ] **Archive:** `mission_complete` shows no clickable 「处理本轮批注」 — verify after switching rounds in the archive switcher (the `updateFrozenPresentation` reset path).
- [ ] **SSE banner:** fatal and non-fatal states are visually distinguishable — verify by killing the backend (fatal) vs. a transient drop.
- [ ] **Contrast:** the fixed-failure count is **≥9**, not 4 — verify `.badge-answered` (2.61:1), `.annotation-answered` (1.88:1), and `#btn-authorize` (3.84:1) are on the list.
- [ ] **Contrast:** `.hint` is still visibly lighter than `.markdown-body p` after the fix — verify the *relationship*, not just the ratio.
- [ ] **Opacity:** no `opacity` value is applied to an element containing text that must remain readable.
- [ ] **Focus:** every focus ring is verified against the `.round-frozen` (0.55) and `.archive-mode` (0.75) composited backgrounds.
- [ ] **Focus:** no focus rule sets `border` or `padding`.
- [ ] **Focus:** rings inside `#chat-messages` and `#annotation-list` are not clipped.
- [ ] **`tabindex`:** `tabindex` and `:focus` counts moved together in the same commit — verify neither is nonzero while the other is zero.
- [ ] **Icons:** no new file under `frontend/vendor/`, no CDN `<link>`; `app.js:1550`'s `textContent` assignment still works against whatever `.collapse-indicator` now contains.
- [ ] **Scope:** `#probe-controls`, `ai-route-select`, and the two `window.prompt` call sites are untouched.
- [ ] **Scope:** no `@media` breakpoint below 1024px, no `prefers-color-scheme`.
- [ ] **Inline errors:** `showInlineError` still uses `textContent` — no `innerHTML` anywhere in the error path.
- [ ] **Inline errors:** the `processRoundBtn` failure renders legibly inside `#probe-controls` (not as a squeezed flex column).
- [ ] **Ordering:** no existing selector moved position in `style.css` without a value change — verify `#brainstorm-view h2` still computes to 14px / `#8a6508`.

---

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| `.hidden` `!important` removed/weakened | LOW (if caught) / HIGH (if shipped) | Re-add the single rule at the top of `style.css`; verify all five modals, `#annotations-panel`, `#checks-panel`, `#selection-menu` hide correctly. If shipped, the app is unusable — treat as a hotfix |
| Half-migrated token palette | MEDIUM | Do a full sweep: enumerate every hex outside `:root`, assign each a role, finish the migration in one commit. Do not fix incrementally a second time |
| Contrast fixed but hierarchy flattened | LOW | Re-pick the lightest passing value per token; recompute the hint/body ratio. Pure token-value change if Phase A landed cleanly |
| `opacity` de-emphasis left in place | MEDIUM | Convert each `opacity` de-emphasis to a color token, then re-verify the composited contrast. Touches layout in `.round-frozen` / `.archive-mode` |
| Focus ring clipped or invisible | LOW | Switch to `outline-offset: -2px`, or bump the container's padding. Single-rule fix |
| `tabindex` shipped without `:focus` | LOW | Add the `:focus` rule; the tab stop is already correct |
| Archive 「处理本轮批注」 re-enabled | LOW | Re-add `processRoundBtn.disabled = true` at the end of `loadArchiveView()`, after `loadChecksView` — mirroring the G-idi03-3 precedent at `app.js:844-845` |
| `.inline-error` flex squeeze | LOW | `flex-wrap: wrap` on `#probe-controls`, or move the error to a dedicated slot |
| Stylesheet reorder changed rendering | LOW–MEDIUM | `git diff` the computed values; raise specificity on the conflicting pair (`#draft-view #brainstorm-view h2`) so order no longer decides |
| Scope crept into a product change | HIGH | Revert to the last phase boundary. `#probe-controls` removal in particular breaks AI-03's dual-route verification surface and needs a DESIGN.md-level decision |

---

## Pitfall-to-Phase Mapping

Proposed phase slots (the roadmap planner owns final numbering — these map 1:1 onto v1.14's six target features):

- **Phase A — 设计契约与令牌层** (design contract + tokens)
- **Phase B — 排版与视觉层级** (typography + visual hierarchy)
- **Phase C — 可访问性** (focus, keyboard, contrast)
- **Phase D — 布局稳健性与交互状态** (magic numbers, nested scroll, responsive floor, hover/active/disabled/transition)
- **Phase E — 回归复验与 UAT** (re-verify the five shipped fixes + manual checks)

| # | Pitfall | Prevention Phase | Verification |
|---|---------|------------------|--------------|
| 1 | Token sprawl / two sources of truth | **A** (must be first) | Hex-literal count outside `:root` is 0; no duplicate token values; no literal-named tokens |
| 2 | Cascade regression on `.hidden` | **A** (written constraint) + every phase's gate | `display: none !important` count == 1; total `!important` == 1; browser check that all 5 modals + 3 panels + selection menu hide |
| 3 | Regressing the five shipped fixes | **A** (do-not-touch list) → **E** (re-verification) | All five manual checks from `260916-t8g-SUMMARY.md` re-run; archive button unclickable after round switching |
| 4 | Contrast-to-ratio hierarchy collapse + `opacity` | **A** (palette decision) → **C** (values) | Failure count ≥ 9 including the composited values; hint/body ratio ≤ ~0.30; no `opacity` on readable text |
| 5 | Focus styles: layout shift / clipping / dimming | **C** (+ **D** for the padding bumps, same release) | Tab through with the sidebar scrolled to the bottom; ring verified at 0.55 and 0.75 composite; no focus rule sets `border`/`padding` |
| 6 | `tabindex` without `:focus` | **C** — same commit | `tabindex` and `:focus` counts moved together; UI-6.1 manual UAT re-run |
| 7 | Emoji replacement / icon dependency | **B** | No new vendored file or CDN link; collapse indicator still visible after a JS `textContent` write |
| 8 | Scope creep | **A** (UI-SPEC "not in v1.14" table) | `#probe-controls` and both `window.prompt` sites untouched; no `@media` below 1024px; no `prefers-color-scheme` |
| 9 | Stylesheet reorder changes rendering | **A** ("append, do not reorder") | `#brainstorm-view h2` still computes to 14px / `#8a6508`; no existing selector moved without a value change |
| 10 | `.inline-error` flex squeeze + `textContent` invariant | **D** (row fix) + **C** (invariant) | `processRoundBtn` failure renders legibly inside `#probe-controls`; no `innerHTML` in the error path; `clearInlineError` called from `applySessionGates` |
| M1 | Verification by grep count | every phase + **E** | At least one runtime check per phase; manual checks named step-by-step; Playwright uses `channel: 'chrome'` |
| M2 | `#state-badge` / `#stream-banner` collision | **D** | At 1024px and 1280px the banner does not cover the badge |
| M3 | Global `transition` / reduced motion | **D** | `prefers-reduced-motion` added in the same commit as any transition; no transition on `display` |
| M4 | Chrome `h2` vs content `h2` collision | **B** | Panel titles unchanged; `.markdown-body` headings use a scoped scale |
| M5 | Weakened `:disabled` token | **C**/**D** | `#btn-authorize` disabled state is unambiguous and distinct from `:hover` |
| M6 | `#confirm-error` `.hint` coupling | **A** | The G3 confirmation failure message renders red, not gray |
| M7 | `aria-live` on the streaming container | **C** | Live region is on the bubble, not the chunk container |

**Ordering rationale:** Phase A must precede everything because every later fix is a token value change; without a single source of truth, Phase C's contrast work is unverifiable. Phase C must precede or accompany Phase D, because focus rings depend on container padding (Phase D) and on not being inside dimmed subtrees (a Phase A palette decision). Phase E is non-optional: none of the five shipped fixes has an automated test, so a milestone that rewrites their CSS without re-running the manual checks has no evidence it did not break them.

---

## Sources

All code-level claims verified by direct inspection and computation against the repository at commit `eca7682`:

- `frontend/style.css` (632 lines), `frontend/index.html` (221 lines), `frontend/app.js` (1639 lines) — read in full
- `.planning/milestones/v1.13-phases/idi-03-g3/03-UI-REVIEW.md` — the 6-pillar audit (13/24, 7 BLOCKERs, ~40 findings); treated as a starting point, not ground truth (its contrast count of 4 is an undercount; see Pitfall 4)
- `.planning/quick/260916-t8g-ui-5-blocker-hidden-sse-onerror/260916-t8g-SUMMARY.md` — the five shipped fixes, their decisions, and their documented known limitations
- `git show b9664e0` — fix commit metadata and the `.hidden`/`!important` rationale
- `.planning/PROJECT.md` — v1.14 milestone scope, tech-stack constraints, UAT environment facts (Playwright `channel: 'chrome'`; keyboard selection not automatable)
- `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md` — v1.13 scope and the Out of Scope table
- `.claude/CLAUDE.md` / `CLAUDE.md` — 简单优先, 外科手术式改动, scope discipline

**Computed arithmetic (script-verified, not estimated):** all contrast ratios in Pitfalls 4 and 5, including opacity-composited values; the `#state-badge` / `#stream-banner` overlap table in M2; the scroll-container padding table in Pitfall 5.

**Not verified (flagged as judgment):** the phase-ordering recommendations, and the claim that `#probe-controls` removal would break AI-03 verification (inferred from DESIGN.md D-06/§9 as cited in PROJECT.md, not from reading DESIGN.md directly).

---

*Pitfalls research for: 交互式讨论迭代系统 — Milestone v1.14 前端视觉与可访问性*
*Researched: 2026-09-17*
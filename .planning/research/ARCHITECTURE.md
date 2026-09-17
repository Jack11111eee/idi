# Architecture Research — Retrofitting a Design System onto a No-Build Vanilla Frontend

**Domain:** Local single-user web tool (`Python + FastAPI` backend, static vanilla HTML/CSS/JS frontend, no bundler, no modules, no build step)
**Milestone:** v1.14 前端视觉与可访问性 — retrofitting design tokens, a controlled type scale, and accessibility states onto a *live* three-file frontend
**Researched:** 2026-09-17
**Confidence:** HIGH on integration points and constraints (all verified by reading the current `frontend/` source and the b9664e0 fix commits); MEDIUM on specific token values (arithmetic verified, final choice is a UI-SPEC decision)

---

## Scope of This Document

This is not "how to build a design system from scratch." It is "how to install one into a 2,491-line, three-file frontend that already works, without a build step and without ever leaving the app visually broken."

The six scope areas named in `PROJECT.md` for v1.14 are:

1. 设计令牌体系 (design tokens) — 2. 视觉层级 (visual hierarchy) — 3. 排版系统 (typography)
4. 可访问性 (accessibility) — 5. 布局稳健性 (layout robustness) — 6. 交互状态 (interaction states)

---

## Verified Baseline (as of 2026-09-17, post-b9664e0)

Every number below was measured against the working tree, not taken from the audit.

| Fact | Value | Evidence |
|---|---|---|
| `style.css` lines | 631 | `wc -l` |
| `index.html` lines | 221 | `wc -l` |
| `app.js` lines | 1,639 | `wc -l` |
| Distinct hex literals | **34** (120 occurrences) | `grep -o '#[0-9a-fA-F]\{3,6\}' \| sort -u` |
| CSS custom properties | **0** | `grep '--[a-z]'` → no matches |
| `:focus` rules | **0** | `grep -c ':focus'` → 0 |
| `@media` rules | **0** | `grep -c '@media'` → 0 |
| `.hidden` rules | **1** (global, `!important`) | `style.css:15` |
| Remaining `display: none` | **2** (`.hidden`, `.panel-body.collapsed`) | `style.css:15, 59` |
| Distinct `font-size` | 7 — `13px ×15`, `12px ×6`, `14px ×5`, `12.5px ×3`, `16px ×1`, `15px ×1`, `11px ×1` | `grep -o 'font-size: …'` |
| Distinct `border-radius` | 8 — `4px ×12`, `6px ×4`, `10px ×2`, `12px ×2`, `3px ×2`, `2px ×1`, `8px ×1`, `9px ×1` | `grep -o 'border-radius: …'` |
| Distinct `gap` | 5 — `8px ×6`, `10px ×4`, `12px ×2`, `6px ×2`, `4px ×1` | `grep -o 'gap: …'` |
| `z-index` values | 4 — `10` badge, `20` banner, `100` overlay, `200` selection-menu | `style.css:158, 209, 225, 482` |
| **Color/style writes from JS** | **0** | `grep 'style\.(background\|color\|border)'` → none |
| JS inline-style writes at all | 3 — `pendingCount.style.display` (`app.js:1165,1169`), `selectionMenu.style.left/top` (`app.js:1304-1305`) | `grep '\.style\.'` |

**The single most consequential fact for planning:** `app.js` writes **zero** color, spacing, or type values. Every design value in this product lives in `style.css`. Tokenization is therefore a **100% CSS-only** migration — no JS edit is needed to reach zero hex literals.

---

## Standard Architecture

### System Overview

The frontend has no framework, no module system, and no build step. It is three files with one implicit contract each.

```
┌───────────────────────────────────────────────────────────────────────┐
│  index.html (221 L)  —  DOM declared up front, one time               │
│                                                                       │
│  #app                                                                 │
│  ├── main#doc-pane          ── flex:1 1 auto, overflow-y:auto         │
│  │   ├── h1 "文档区"          ← UNSTYLED, UA default ~32px (audit 2.1) │
│  │   ├── #enter-form · #state-badge · #stream-banner   (fixed pos.)   │
│  │   ├── #draft-view.doc-subview       ┐                              │
│  │   └── #rounds-placeholder.doc-subview ┘ toggled by .hidden         │
│  └── aside#sidebar          ── flex:0 0 420px, overflow-y:auto        │
│      ├── #session-panel  (phase 1-2)   ┐                              │
│      ├── #annotations-panel (phase 3)  ├ exactly one visible at a time│
│      ├── #checks-panel  (phase 5)      ┘ via .hidden                  │
│      └── #ai-panel       (always)      ← never gets .hidden           │
│  + 5 × .overlay.hidden modals + #selection-menu + #cli-check-overlay  │
│  + <script marked.min.js> <script app.js>   (both at body end)        │
└───────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌───────────────────────────────────────────────────────────────────────┐
│  style.css (631 L)  —  ONE flat cascade, source order is load-bearing │
│                                                                       │
│  L3   * { box-sizing }                                                │
│  L5   html, body { … }                                                │
│  L15  .hidden { display: none !important }   ← only global mechanism  │
│  L17+ #app flex shell                                                 │
│  L39+ … 620 L of flat component rules, no layers, no @media, no vars  │
│  L631 #mission-complete-modal                                         │
└───────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌───────────────────────────────────────────────────────────────────────┐
│  app.js (1,639 L)  —  single module-scope script, no modules          │
│                                                                       │
│  L4-75   ~70 × const el = document.getElementById(...)  at top-level  │
│          (line 4 runs at parse time → script MUST stay after DOM)     │
│  L77+    module-scope state: currentState, currentRoundNumber, …      │
│  apply*View(data)  ← the 6 phase-view functions; all class toggling   │
│  SSE dispatch, fetch wrappers, showInlineError()                      │
└───────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Owns | Change surface in v1.14 |
|---|---|---|
| `index.html` | DOM shape, static text, `class` attributes, ARIA/tabindex attributes | **Small** — `tabindex` + `aria-*` only. No structural moves recommended. |
| `style.css` | All design values (color/space/type/radius) + all state presentation | **Large** — the primary target of every phase except the last. |
| `app.js` | State derivation → class toggling, SSE, error surfaces | **Near-zero** — only the accessibility-semantics phase touches it. |

### Structure Rationale

- **No build step is a hard constraint** (`PROJECT.md` Tech stack, DESIGN.md D-06/D-01). No Sass, no PostCSS, no `@custom-media`, no CSS nesting that needs transpilation, no JSX. Everything must be valid CSS that Chrome parses directly.
- **Source order is load-bearing** in exactly one place: `.hidden` needed `!important` because `.overlay { display: flex }` has the same specificity (0-1-0) and is declared later (`style.css:151`). This is documented in the code comment at `style.css:13-14` and must survive the migration.
- **`app.js` binds ~70 element handles at module top-level.** Any HTML edit that removes or renames an `id` breaks the script at parse time and silently kills every handler below it (this is the documented G-idi01-8 failure). This is why HTML edits are the highest-risk change type in this milestone and should be minimized and batched.

---

## Recommended Target Structure

No new files. No new folders. One insertion point and one discipline.

```
frontend/
├── index.html      # + tabindex="0" on #round-doc  (1 attr)
│                   # + role/aria-* on 4 .overlay modals + #chat-messages
├── style.css       # + :root token block at the TOP (the only insertion)
│                   #   … then every literal below replaced by var()
└── app.js          # + keyboard focus handoff for #selection-menu
                    # + Escape-to-close / focus trap for modals
                    # + aria-live toggling for #stream-banner
```

### The token block's placement (quality-gate item a)

**Recommendation: a single `:root` block inserted at the top of `style.css`, immediately after the `* { box-sizing }` reset (line 3) and immediately *before* `html, body` (line 5), fenced by explicit comment markers.**

```css
/* 骨架布局:左文档区 / 右侧栏(§4.1 flex 双栏)+ 面板折叠 + 事件分级颜色 */

* { box-sizing: border-box; }

/* ===== DESIGN TOKENS: START =============================================
   唯一令牌来源。本块内允许出现字面量;本块之外一律 var()。
   机械校验:块外 hex 计数必须为 0(见 ARCHITECTURE.md「迁移门禁」)。
   ========================================================================= */
:root {
  /* --- 颜色:原语层 --- */  /* --- 颜色:语义层 --- */
  /* --- 间距 --- */          /* --- 字号 / 字重 / 行高 --- */
  /* --- 圆角 --- */          /* --- 层级 / 动效 --- */
}
/* ===== DESIGN TOKENS: END ============================================== */

/* 唯一全局显隐规则:!important 必需——… (原注释逐字保留) */
.hidden { display: none !important; }

html, body { … }
```

**Why here and not at the bottom:** the block is a *declaration source*, and putting it first makes it visually the single source of truth. Functionally, order does not matter — `:root` custom properties are resolved after the cascade and are inherited by every rule in the file regardless of position. Putting it first is a *readability and reviewability* decision, and it keeps the `:root` block adjacent to `.hidden` so that any diff touching one is visible next to the other.

**Why not a separate `tokens.css`:** it would be a cleaner layer, but it costs an `index.html` edit (a second `<link>`), which (i) makes the token phase HTML-touching rather than pure-CSS and (ii) introduces a second place where `:root` custom properties can be declared, which is precisely the "second source of truth" risk we are trying to eliminate. The fence markers + mechanical check recover the reviewability benefit at zero HTML risk. Revisit only if the token count exceeds ~80.

### How the token block interacts with the existing `!important` rule (item a, continued)

**It does not, and that is by design.** Three rules of engagement:

1. **`.hidden` is a mechanism, not a design value.** It is not tokenized, not moved, not weakened. `display: none` carries no design intent. Keep it verbatim, `!important` included.
2. **`!important` makes `.hidden` position-independent.** The migration will reorder and rewrite ~620 lines of CSS. Because `.hidden` carries `!important`, it beats *any* non-important `display` declaration regardless of specificity or source order. The original failure mode (`.overlay { display: flex }` at line 151 sharing specificity 0-1-0 and coming later) cannot recur even if `.overlay` moves above `.hidden`.
3. **Never declare a tokenized `display`.** If a token phase introduces `display: var(--display-panel)` anywhere, the `!important` race is re-opened and unreadable. Colors, spacing, type, radius, z-index, and motion may be tokenized. `display` may not.

**The 14 recently-consolidated `.hidden` rules — residual coupling to watch.** The b9664e0 consolidation removed 14 per-selector `display: none` rules and left one global rule. Five elements had *no other* rule and now depend **solely** on the global rule:

| Element | JS that toggles it | Consequence if the global rule is lost |
|---|---|---|
| `#draft-empty` | `app.js:839-848` | "尚无草稿" renders on top of an existing draft — direct self-contradiction |
| `#rounds-hint` | `app.js:945`, `382`, `584`, `812` | Stale placeholder "已进入轮次阶段(本阶段占位)。" permanently above the real round doc |
| `#btn-process-round` | `app.js:344`, `817` | Read-only archive contract (§7.4 / D-P3-25) violated in the presentation layer |
| `#round-switcher` | `app.js:428`, `453`, `584`, `814` | Stale round switcher visible in writing / self-check views |
| `#writing-hint` | `app.js:463` | — |

This is a **5-way single point of failure**. The milestone should carry a one-line gate (`grep -c '^\.hidden {' style.css` must equal `1`) in every plan that edits `style.css`. Cost: one command. Payoff: it is the only thing standing between a stylesheet reorganization and a silent regression of five shipped fixes.

Note the one adjacent rule that is *not* `!important`: `.panel-body.collapsed { display: none }` (`style.css:59`), used only by `#ai-panel-body`. It survives today because nothing else declares `display` on that element. **If any phase adds an `#ai-panel-body { display: … }` ID-selector rule, collapse breaks silently** (1-0-0 beats 0-2-0). Either leave the collapse mechanism untouched, or migrate `.collapsed` → `.hidden` so the `!important` rule owns it.

---

## Architectural Patterns

### Pattern 1: Two-tier tokens (primitive → semantic) in one block

**What:** every design value is declared twice — once as a primitive (a named raw value with no meaning) and once as a semantic alias that names the *role*.

**When to use:** always, for color. Optionally for space/type/radius (a single tier is fine there).

**Trade-offs:** doubles the declaration count, but it is what lets the UI-SPEC reassign a role (`--color-action-irreversible: var(--green-700)`) without touching a single component rule. Without the primitive tier, the six semantically-distinct green buttons cannot be separated — they all currently share `#e9f7ef` / `#2e8b57`, and you cannot tell "认可雏形" from "授权撰写总设计文档" by reading the token name alone.

**Example — the color problem in concrete token form:**

```css
:root {
  /* 原语层:只描述值,不描述用途 */
  --green-700: #2e8b57;   --green-050: #e9f7ef;
  --blue-600:  #1a6fd4;   --blue-050:  #eef4ff;
  --amber-800: #8a6508;   --amber-100: #fdf6ec;  --amber-200: #e8d9a8;
  --amber-050: #fffdf5;   --amber-150: #fff3c4;
  --red-700:   #c0392b;   --red-050:   #fdecea;
  --neutral-900: #1a1a1a; --neutral-700: #444;   --neutral-600: #555;
  --neutral-500: #6b6b6b; /* 由 #999 提深以满足 AA,见下 */
  --neutral-400: #ccc;    --neutral-300: #ddd;   --neutral-200: #e0e0e0;
  --neutral-150: #eee;    --neutral-100: #f0f0f0;--neutral-050: #f5f5f5;
  --neutral-000: #fff;    --surface-page: #fafafa;

  /* 语义层:只描述用途 */
  --color-bg-page:    var(--surface-page);
  --color-surface:    var(--neutral-000);   /* 面板/卡片底 */
  --color-text:       var(--neutral-900);
  --color-text-muted: var(--neutral-500);   /* .hint —— 原 #999,AA 失败 */
  --color-border:     var(--neutral-400);
  --color-border-sub: var(--neutral-150);

  --color-action-primary:  var(--blue-600);   /* 发送 / .primary / 会话气泡 */
  --color-action-danger:   var(--red-700);    /* .danger / 中止 / 错误 */
  --color-action-positive: var(--green-700);  /* 例行正向:继续自检/继续修复/处理本轮批注 */
  --color-action-gate:     …;                 /* 门控动作:认可雏形/撰写 */
  --color-action-irreversible: …;             /* G3 授权 —— Core Value 红线,必须独立 */
}
```

**The Core-Value payoff:** `--color-action-irreversible` exists as a *token name*. The G3 authorization button's visual weight becomes a one-line contract instead of an accident. Today `#btn-authorize` (`style.css:518-525`) is byte-identical to `#btn-continue-check` (`style.css:590-595`) except for the selector.

**On the primary blue:** `#2c7be5` with white text measures **4.14:1** — an AA failure on the user's own chat bubbles and every `.primary` button. Darkening the primitive to `#1a6fd4` measures **4.92:1**. Because the value lives in `--blue-600`, that single edit fixes `.chat-user`, `button.primary`, `#chat-input-row button`, `.overlay-card button`, and `.chat-ai.streaming-ai` border in one place. This is the concrete argument for tokens over a find-and-replace.

### Pattern 2: Token-derived layout constants (`calc` instead of magic numbers)

**What:** a structural constant (sidebar width) is declared once as a token and every dependent position is *computed* from it.

**When to use:** any time two rules encode the same structural fact.

**Example — the `#state-badge { right: 448px }` fix (quality-gate item d):**

```css
:root { --sidebar-w: 420px; --space-6: 24px; }

#sidebar     { flex: 0 0 var(--sidebar-w); }
#state-badge { right: calc(var(--sidebar-w) + var(--space-6)); }  /* 420+24 = 444 */
```

`448px` was `420 + 28`, with the arithmetic recorded only in a comment. Two things change:

- **The 28px is snapped to the scale** (`--space-6: 24px`), producing 444px. A 4px shift of a badge is imperceptible; an off-scale value in the token layer is a permanent invitation to re-introduce magic numbers.
- **The coupling is now directional and enforced.** Changing `#sidebar`'s width without changing the token is no longer possible — both consumers read the same variable.

**This is the dependency that makes the responsive phase possible.** `@media` cannot use `var()` in its conditions (see Anti-Pattern 3), but it *can* redefine tokens. So the narrow-window rule becomes:

```css
@media (max-width: 900px) {
  :root { --sidebar-w: 320px; }   /* 徽标与侧栏同步收窄,零额外规则 */
}
```

Without Pattern 2, every breakpoint would need its own `#state-badge { right: … }` override — i.e. the magic number would multiply.

**Structural alternative (note for the UI-SPEC author, do not do both):** `#state-badge` is a direct child of `#doc-pane` (`index.html:23`). Adding `#doc-pane { position: relative }` + `#state-badge { position: absolute; top: 12px; right: 16px }` removes the sidebar coupling *entirely*. The trade-off: `#doc-pane` has `overflow-y: auto`, so an absolutely-positioned badge scrolls away with the content. Today it is `position: fixed` and always visible. Since audit finding 5.1 complained that the fixed badge *occludes* scrolled content, scrolling away is arguably an improvement — but it is a behavior change, so it is a UI-SPEC decision, not a refactor. **The `calc()` version is the zero-behavior-change migration step and should be what the roadmap commits to.**

### Pattern 3: CSS-only view styling via structural selectors (no JS state attribute)

**What:** derive presentation from what is already in the DOM rather than adding a JS-set attribute.

**When to use:** whenever the DOM already encodes the state.

**Example — sidebar panel active state, zero JS:**

```css
/* 三个状态面板恰好只有一个不带 .hidden;#ai-panel 常驻,排除之 */
#sidebar > section:not(.hidden):not(#ai-panel) > .panel-header {
  background: var(--color-surface);
  border-left: 3px solid var(--color-action-primary);
  color: var(--color-text);
}
```

`applyPhaseXView` already toggles `.hidden` on `#session-panel` / `#annotations-panel` / `#checks-panel` (`app.js:352, 360, 365, 370, 375, 381, 426, 434, 586, 815`). The active panel *is* the visible one; no new state is needed. This keeps the entire hierarchy/typography phase 100% CSS-only.

**Rejected alternative:** `document.body.dataset.phase = currentState` in `app.js`. It works and is arguably more explicit, but it is a JS edit in a phase that otherwise needs none — and every JS edit in this codebase carries the top-level-handle-binding risk. Reserve it for a case that genuinely cannot be derived from the DOM.

### Pattern 4: `tabindex` and `:focus` must land in the same commit (quality-gate item c)

**What:** a focusable element without a focus style is an accessibility *regression* relative to a non-focusable one — the user can reach it and cannot see where they are.

**The specific coupling in this codebase — and a finding that changes the roadmap:**

`#round-doc` currently has **no `tabindex`**, in HTML or JS (`grep -n 'tabindex' index.html app.js` → 0 matches). b9664e0's FIX 4 added `roundDoc.addEventListener('keyup', handleSelectionTrigger)` (`app.js:1327`). **That listener is inert.** `keyup` dispatches to the focused element and bubbles; `#round-doc` is a plain `<div class="markdown-body">` whose children (`h1`/`p`/`mark`/`table`) are not focusable, so focus never enters the subtree and the event never reaches the handler. The keyboard path to 划词批注 — the flagship feature, mandated by DESIGN.md D-02 — is still mouse-only today.

So the a11y phase is not "add a focus style to an existing feature." It is **"make an already-shipped-but-dead code path live,"** and it requires all three of:

| Change | File | Type |
|---|---|---|
| `tabindex="0"` on `#round-doc` | `index.html:64` | HTML, 1 attribute |
| `:focus-visible` rule with a visible ring | `style.css` | CSS |
| Focus handoff: on keyboard-triggered menu, `.focus()` the first `#selection-menu` button; Escape closes and returns focus to `#round-doc` | `app.js` (`handleSelectionTrigger`) | JS, ~8 lines |

**Why the third is required and not gold-plating:** `#selection-menu` is the *last* element in `<body>` (`index.html:200`), after five modals. Tab order from `#round-doc` runs through the whole document area and the entire sidebar before reaching it. A keyboard user who successfully selects text would have to press Tab a dozen times to reach the menu they just triggered — and any intermediate focusable element that closes the menu on blur would defeat it. Focus must be moved into the menu programmatically.

**On `:focus` vs `:focus-visible`:** use `:focus-visible`. It shows the ring for keyboard navigation and suppresses it for mouse clicks, which is exactly the desired behavior for a `tabindex="0"` document region (clicking the document to select text must not flash a focus ring). Baseline support is universal in current Chrome/Firefox/Safari. Keep `:focus-visible` as the *only* ring rule so there is one focus treatment, not two.

**Sequencing rule:** `tabindex="0"` must never be committed in a plan that does not also add the `:focus-visible` rule. If they split, the intermediate state is a focusable region with an invisible (or UA-default, inconsistent) ring — the exact failure the gate names. Bundle them in one plan, verify by keyboard in one UAT step.

### Pattern 5: Flex-driven scroll ownership (quality-gate item e)

**What:** one scroll owner per visual region, chosen deliberately; not a stack of independently-capped inner scrollers.

**The current state — five scroll owners in a 420px column:**

| # | Selector | Rule | Line |
|---|---|---|---|
| 1 | `#sidebar` | `overflow-y: auto` | 35 |
| 2 | `.event-list` | `max-height: 55vh; overflow-y: auto` | 101-102 |
| 3 | `#chat-messages` | `max-height: 40vh; overflow-y: auto` | 313-314 |
| 4 | `#annotation-list` | `max-height: 32vh; overflow-y: auto` | 416-417 |
| 5 | `#latest-check` | `max-height: 30vh; overflow-y: auto` | 581-582 |

At a 900px viewport, inner panes alone total `55vh + 40vh = 95vh` before panel headers and padding — the outer sidebar is *guaranteed* to scroll too, so the user sees nested scrollbars with no affordance for which is which.

**Target: two scroll owners, each with a stated reason.**

```css
/* 1. #sidebar —— 唯一的侧栏滚动者。面板按阶段切换,内容自然堆叠。 */
#sidebar { overflow-y: auto; }

/* 2. #chat-messages —— 唯一合理的第二个滚动者:输入行必须钉在面板底部。 */
#chat-messages { flex: 1 1 auto; min-height: 0; max-height: var(--chat-max-h); overflow-y: auto; }
```

**Concrete edits:** delete `max-height` **and** `overflow-y` from `.event-list` (101-102), `#annotation-list` (416-417), `#latest-check` (581-582). They become `overflow: visible` and grow naturally; the sidebar scrolls. Keep `#chat-messages` as the pinned-input exception.

**Two coupled fixes required for this to actually work:**

- `#session-panel { min-height: 320px }` (line 303) forces the sidebar to scroll even when every panel is empty. Replace with `flex: 0 0 auto`. Audit finding 5.4 flagged the unresolvable interaction between `#session-panel { min-height: 320px }` and `#chat-messages { flex: 1; min-height: 160px; max-height: 40vh }` — this is that resolution: the panel sizes to content, the message list owns the cap.
- `#session-panel .panel-body { min-height: 0 }` (line 308) is already present and is the flexbox `min-height: auto` fix — do not lose it during the rewrite. The same `min-height: 0` is required on any new flex container that holds a scroller.

**`max-height` in `vh` is a viewport unit in a fixed-width column.** Once `#chat-messages` is the only capped scroller, `--chat-max-h: 40vh` is defensible (it is a deliberate "don't let chat eat the whole column" cap). The other three were not caps — they were accidental layout.

**One extra robustness guard for the same phase:** `#doc-pane` is `flex: 1 1 auto` with no `min-width: 0`. A flex item's default `min-width: auto` means long unbreakable content (a URL, a wide code block in `.markdown-body`) can blow the flex container past the viewport instead of scrolling. Add `#doc-pane { min-width: 0 }` and `overflow-wrap: anywhere` on `.markdown-body`. Cheap, and it is a precondition for the narrow-window requirement.

---

## Data Flow

### Change flow for a token migration

```
UI-SPEC decision (token name + value)
        │
        ▼
style.css  :root block          ← NEW: the only place a literal may exist
        │  var()
        ▼
style.css  component rules      ← MODIFIED: literals → var() references
        │
        ▼
mechanical gate                 ← VERIFY: 0 hex outside the block; every var() defined
        │
        ▼
visual diff (browser)           ← VERIFY: rendered output matches the pre-migration
                                   screenshot except for the intended AA fixes
```

### Why the gate must be mechanical, not visual (quality-gate item f)

**The "second source of truth" failure mode is temporal, not spatial.** During migration you will have `--color-danger: #c0392b` declared *and* eight literal `#c0392b` still in component rules. Both are true simultaneously. Nothing about file layout prevents this — only the migration *granularity* does.

**The rule that prevents it: migrate one value-family per commit, atomically, and gate it with a count.**

```
Commit N (per family, e.g. --color-danger):
  1. add --red-700 / --color-action-danger to :root
  2. replace ALL 8 occurrences of #c0392b in component rules with var(--color-action-danger)
  3. gate: grep -c '#c0392b' style.css  → must equal the count inside the token block only
```

**Corollary — never define a token you are not consuming in that same commit.** A token that exists with no consumers is not a token; it is a second literal with a nicer name, and it will drift from the literals it is supposed to replace.

**Corollary — never leave a literal for a value you have tokenized.** The whole value of the invariant is that it is *checkable*. "0 hex literals outside the token block" is a one-line grep; "mostly 0, except the ones we decided to leave" is not checkable at all, and it degrades to 34 again within one milestone. This applies even to one-off values like `#e8b4ae` (the `.fatal` banner border) — give them primitive names (`--red-200`) rather than exempting them.

**The two gates to carry through every `style.css` plan in this milestone:**

```bash
# Gate 1 — no literal colors outside the token block (excluding comments)
awk '/DESIGN TOKENS: START/{f=1} /DESIGN TOKENS: END/{f=0} !f' frontend/style.css \
  | grep -c '#[0-9a-fA-F]\{3,6\}'          # must be 0

# Gate 2 — every consumed custom property is declared (catches silent var() typos)
comm -23 \
  <(grep -o 'var(--[a-z0-9-]*' frontend/style.css | sed 's/var(//' | sort -u) \
  <(grep -o '\-\-[a-z0-9-]*:' frontend/style.css | sed 's/:$//' | sort -u)   # must be empty
```

Gate 2 exists because **`var()` fails silently.** A typo'd `--color-prmary` does not error; the declaration becomes invalid at computed-value time and the property resolves to `unset` — inherited for `color`, initial for `background`. A literal `#2c7be5` typo'd to `#2c7be6` is a slightly wrong blue; a token typo is *no color at all*. This is a genuinely new failure mode that the token layer introduces, and Gate 2 is its only cheap defense. Do **not** defend against it with `var(--x, #fallback)` — the fallback re-creates the second source of truth.

---

## Migration Sequence

Six phases. Two hard dependency chains: **P1 is a prerequisite for everything**; **P5 is a prerequisite for P6**. Everything else is independent and can be reordered.

```
P1 令牌层 ──────────┬──▶ P2 排版与视觉层级        (CSS-only)
   (CSS-only)       ├──▶ P3 交互状态              (CSS-only)
   ▲                ├──▶ P4 布局稳健性            (CSS-only)
   │                └──▶ P5 可访问性·样式 ──▶ P6 可访问性·语义与键盘 (HTML+JS)
UI-SPEC
```

### P1 — 设计令牌体系 (CSS-only) — **hard prerequisite**

- Insert the fenced `:root` block at `style.css:4`; define color (primitive + semantic), space, type, radius, z-index, motion.
- Substitute every literal: 34 hex values, 3 `rgba()`, ~17 padding patterns, 5 gaps, 7 font sizes, 8 radii, 4 z-indexes.
- **AA-compliant values are chosen here, at declaration time** — not in P5. Fixing `.hint` is a *token value* decision, not a separate styling pass.
- **Gate:** Gate 1 + Gate 2 above; `grep -c '^\.hidden {'` = 1; `node --check app.js`; pytest baseline unchanged; app.js/index.html untouched.
- **Depends on:** UI-SPEC fixing the token names and values.

### P2 — 排版系统 + 视觉层级 (CSS-only)

- Consume the type tokens: `.markdown-body h1/h2/h3` get `font-size` from the scale (currently **no** `font-size` rule at all → UA defaults 28/21/16.4px — audit 4.3, the primary content's type scale is browser-controlled).
- Demote `#doc-pane > h1` from the UA-default ~32px to a scale step; it is the largest text on screen and it is a container label (audit 2.1/4.5).
- `#btn-authorize` gets `--color-action-irreversible` — the Core-Value fix.
- Panel active/inactive differentiation via Pattern 3 (pure CSS, no JS).
- Replace the two CSS-`content` emoji (`📌` at `style.css:431`, `📍` at `style.css:612`) with an icon mechanism.
- **Gate:** markdown headings no longer resolve to UA defaults (computed-style check in the browser); `#btn-authorize` computed style differs from `#btn-continue-check`; P1 gates still pass.
- **Depends on:** P1.

### P3 — 交互状态 (CSS-only)

- `:hover` / `:active` / `:disabled` / `transition` — currently 2 / 0 / 8 / 1 across 631 lines.
- Add `@media (prefers-reduced-motion: reduce)` to neutralize transitions.
- **Regression watch:** the `:disabled` treatment must not weaken `processRoundBtn.disabled = true` (b9664e0 FIX 3). Disabled controls must remain visually disabled (`cursor: not-allowed` + a reduced-opacity token), not merely non-functional.
- **Depends on:** P1. Independent of P2/P4/P5.

### P4 — 布局稳健性 (CSS-only)

- `--sidebar-w` + the `calc()` badge fix (Pattern 2).
- Scroll-owner reduction 5 → 2 (Pattern 5).
- `#doc-pane { min-width: 0 }` + `overflow-wrap`.
- `@media` breakpoints (see Anti-Pattern 3 — the values must be literals).
- **Gate:** resize 1440 → 1024 → 768 → 375 with no horizontal overflow; the badge stays in the doc pane's top-right corner at every width; no nested scrollbar except `#chat-messages`; the sidebar has exactly one scrollbar.
- **Depends on:** P1. This is the highest-regression CSS phase — it changes structural rules.

### P5 — 可访问性:样式 (CSS-only)

- One global `:focus-visible` rule + `--focus-ring` token. Today `grep -c ':focus'` = **0**.
- Re-verify every text/background token pair against WCAG AA (the arithmetic is done once, in the token block).
- **Gate:** `grep -c ':focus-visible'` > 0; all 4 named failing pairs pass AA.
- **Depends on:** P1 (the ring color is a token) and P4 (the layout it rings must be stable).

### P6 — 可访问性:语义与键盘 (HTML + JS) — **the only phase that touches HTML/JS**

- `tabindex="0"` on `#round-doc` + `:focus-visible` (already shipped in P5) **in the same commit** — completes b9664e0 FIX 4 (Pattern 4).
- `#selection-menu` focus handoff + Escape-to-close + focus return.
- `role="dialog"` / `aria-modal="true"` / `aria-labelledby` on the four `.overlay` modals; Escape-to-close; focus trap; initial focus. Today `grep -n 'aria-\|role='` over the whole frontend returns **zero matches**.
- `aria-live="polite"` on `#chat-messages`; `aria-live="assertive"` on `#stream-banner` (which already exists for sighted users from b9664e0 FIX 2 — the aria attribute makes the same signal reach screen readers).
- **Gate:** keyboard-only path from page load to a created annotation, verified manually (see the UAT constraint below); modal focus trap; `node --check app.js`; pytest 219-test baseline unchanged.
- **Depends on:** P5 (the focus style must exist before the focusable element does).

**Ordering rationale:** P1 first because four phases consume it and it is the only phase whose success criterion is a pure refactor (zero visual change except the intended AA fixes) — the cheapest possible place to discover that the migration approach is wrong. P2 second because it delivers the most user-visible value and addresses the Core-Value finding. P3 before P4 because interaction states are pure additions (low regression risk) while P4 restructures the layout. P6 last because it is the only phase that edits `app.js` and `index.html`, where the top-level element-handle bindings (`app.js:4-75`) make every edit potentially fatal to the whole script.

**Merge option for the roadmap planner:** P3 and P5 are both "state styling, CSS-only, depends only on P1" and could be one phase (状态与可访问性样式) if plan count is a constraint. They are kept separate here because their verification is different (visual feedback vs. contrast + focus).

**UAT constraint carried from `PROJECT.md`:** Playwright must use `chromium.launch({ channel: 'chrome' })`; keyboard text selection **cannot be automated** (not even on `contenteditable`). Every P6 acceptance item that depends on Shift+Arrow selection must be marked **manual check**, not automated. This is a known, documented environment fact — do not plan an automated gate for it.

---

## Which Changes Touch What (quality-gate item b)

This table is the phasing input: **four of six scope areas need no HTML or JS edits at all.**

| Scope area | `style.css` | `index.html` | `app.js` |
|---|---|---|---|
| 1. 设计令牌体系 | **YES — full** | no | no *(verified: app.js writes zero color/style values)* |
| 2. 视觉层级 | **YES — full** | no *(the `<h1>` is styled by `#doc-pane > h1`; emoji are CSS `content`)* | no *(Pattern 3 uses `:not(.hidden)`)* |
| 3. 排版系统 | **YES — full** | no | no |
| 4. 可访问性 | partial — `:focus-visible`, contrast | **YES** — `tabindex` on `#round-doc`; `role`/`aria-*` on 4 modals + `#chat-messages` + `#stream-banner` | **YES** — selection-menu focus handoff, modal Escape/trap, aria-live toggling |
| 5. 布局稳健性 | **YES — full** | no | no |
| 6. 交互状态 | **YES — full** | no | no |

**Implication:** the milestone can run five CSS-only phases with a single shared verification discipline (gates + browser visual check) and concentrate all HTML/JS risk into one final phase. That is the strongest available argument for the phase order above.

---

## Integration Points (explicit, with change type)

| # | Integration point | File : line | Change type | Consumed by |
|---|---|---|---|---|
| 1 | `:root` token block, fenced | `style.css` — insert after L3 | **NEW** | every phase |
| 2 | `.hidden { display: none !important }` | `style.css:15` | **MODIFIED — do not touch** (must survive verbatim) | 5 elements + all modals |
| 3 | `.panel-body.collapsed { display: none }` | `style.css:59` | **UNTOUCHED** (or migrate to `.hidden`) | `#ai-panel-body` |
| 4 | `.hint { color: #999; font-size: 13px }` | `style.css:39` | **MODIFIED** — token + AA value | every gate explanation |
| 5 | `.inline-error { color: #c0392b; font-size: 13px }` | `style.css:42` | **MODIFIED — values only, class name frozen** | b9664e0 FIX 5 (JS sets `className = 'inline-error'` at `app.js:307`) |
| 6 | `#sidebar { flex: 0 0 420px }` | `style.css:32` | **MODIFIED** → `var(--sidebar-w)` | #7 |
| 7 | `#state-badge { right: 448px }` | `style.css:202` | **MODIFIED** → `calc(var(--sidebar-w) + var(--space-6))` | responsive |
| 8 | `#stream-banner` + `.fatal` | `style.css:213-227` | **MODIFIED** — tokenize, preserve `z-index: 20 > 10` | b9664e0 FIX 2 |
| 9 | `.overlay { display: flex; z-index: 100 }` | `style.css:151-158` | **MODIFIED** — tokenize z, **never `!important`** | all modals + `.hidden` race |
| 10 | `#selection-menu { z-index: 200 }` | `style.css:480-490` | **MODIFIED** — tokenize z | keyboard menu |
| 11 | `.markdown-body h1/h2/h3` (no `font-size`) | `style.css:240-243` | **MODIFIED** — add scale steps | audit 4.3 |
| 12 | `#doc-pane > h1` (no rule at all) | `index.html:13` | **NEW CSS rule** | audit 2.1/4.5 |
| 13 | `.event-list { max-height: 55vh; overflow-y }` | `style.css:101-102` | **MODIFIED** — remove both | scroll owners |
| 14 | `#chat-messages { flex; min-height; max-height; overflow-y }` | `style.css:310-319` | **MODIFIED** — keep as the one pinned scroller | scroll owners |
| 15 | `#annotation-list { max-height: 32vh }` | `style.css:412-419` | **MODIFIED** — remove both | scroll owners |
| 16 | `#latest-check { max-height: 30vh }` | `style.css:580-588` | **MODIFIED** — remove both | scroll owners |
| 17 | `#session-panel { min-height: 320px }` | `style.css:303` | **MODIFIED** → `flex: 0 0 auto` | audit 5.4 |
| 18 | `#session-panel .panel-body { min-height: 0 }` | `style.css:304-309` | **UNTOUCHED — preserve** | flexbox correctness |
| 19 | `#doc-pane { flex: 1 1 auto }` (no `min-width`) | `style.css:23-28` | **MODIFIED** — add `min-width: 0` | narrow windows |
| 20 | `#btn-authorize` / `#btn-continue-check` identical | `style.css:518-525` vs `590-595` | **MODIFIED** — diverge via token | Core Value |
| 21 | 5 × `.overlay.hidden` modals | `index.html:151,163,177,189,206` | **MODIFIED** — `role`/`aria-modal`/`aria-labelledby` | P6 |
| 22 | `#round-doc` (no `tabindex`) | `index.html:64` | **NEW** — `tabindex="0"` | b9664e0 FIX 4 |
| 23 | `roundDoc.addEventListener('keyup', …)` | `app.js:1327` | **UNTOUCHED listener; add focus handoff nearby** | D-02 keyboard path |
| 24 | `handleSelectionTrigger()` | `app.js:1298-1316` | **MODIFIED** — keyboard branch focuses menu | P6 |
| 25 | `showInlineError(anchor, msg)` / `clearInlineError()` | `app.js:295-311` | **UNTOUCHED** | b9664e0 FIX 5 |
| 26 | `applyArchiveView()` — `processRoundBtn.disabled = true` | `app.js:770-774` | **UNTOUCHED** | b9664e0 FIX 3 |
| 27 | 70 × top-level `getElementById` handles | `app.js:4-75` | **UNTOUCHED — no `id` may be renamed or removed** | whole script |

---

## Anti-Patterns

### Anti-Pattern 1: Tokenizing `display`

**What people do:** add `--display-overlay: flex` / `--display-hidden: none` for "completeness."
**Why it's wrong:** it puts a `var()`-resolved value into the cascade position currently occupied by the `.hidden` `!important` rule and `.overlay { display: flex }`. The specificity/order race that b9664e0 fixed at cost of an `!important` is re-opened, and now it is also unreadable.
**Do this instead:** tokens cover color, space, type, radius, z-index, and motion. `display` stays literal. `display` is layout *mechanism*, not design *value*.

### Anti-Pattern 2: `var(--token, #fallback)`

**What people do:** defensively write fallbacks so a missing token "degrades gracefully."
**Why it's wrong:** the fallback is a literal in a component rule. It is exactly the second source of truth this migration exists to eliminate, and it is invisible to Gate 1 because it is not a bare hex — it is a hex inside a `var()`. Worse, it masks the failure: the page looks *almost* right while a token is missing.
**Do this instead:** Gate 2 (every `var()` is declared). A missing token must be a loud, greppable failure, not a silent color.

### Anti-Pattern 3: Assuming breakpoints can be tokens

**What people do:** `:root { --bp-narrow: 900px }` then `@media (max-width: var(--bp-narrow))`.
**Why it's wrong:** **it does not work.** Media queries are evaluated before custom properties are resolved, and CSS forbids `var()` in a media query condition. The rule is silently dropped — no error, no fallback, the breakpoint simply never applies. `@custom-media` would solve it, but that requires a preprocessor, and there is no build step.
**Do this instead:** accept that breakpoint values are the one documented exception to the no-literals rule. Declare them in a fenced comment block at the top of the responsive section, use them consistently (two or three values maximum), and state the exception explicitly in the UI-SPEC so it does not read as an oversight. Alternatively, put the media queries at the *end* of `style.css` in a fenced section so the exception is spatially obvious.

### Anti-Pattern 4: Reorganizing `style.css` while tokenizing

**What people do:** "while I'm in here," group rules by component, reorder sections, move `.overlay` next to the other modals.
**Why it's wrong:** the `.hidden` rule is a 5-way single point of failure (see the residual-coupling table above). A reorder cannot break it *because* of `!important` — but a reorder that also rewrites rules is exactly how a rewrite loses an `!important`, and the resulting failure is silent (five UI elements stop hiding, and the only symptom is contradictory copy in two views). It also destroys the visual-diff verification: if the layout moves, a rendered difference can no longer be attributed to a token change.
**Do this instead:** P1 is a **pure value substitution, in place**. No rule moves. No selector changes. No declarations added or removed except the `:root` block. The diff should be readable as "every literal became a `var()`" and nothing else.

### Anti-Pattern 5: `outline: none` as a focus style

**What people do:** "reset the UA outline, then style `:focus` with a border or background."
**Why it's wrong:** on `#round-doc` (a 720px-wide scrollable region) a background change is not a reliable focus indicator, and on a `tabindex="0"` region the UA outline is the only thing guaranteeing visibility across browsers. Removing it and substituting a subtle style produces a focusable region the user cannot locate — the exact failure the gate names.
**Do this instead:** keep the outline. `:focus-visible { outline: 2px solid var(--focus-ring); outline-offset: 2px }` — one rule, globally. `outline-offset` matters for the elements that sit flush against a border (the sidebar panels, the buttons in `#probe-controls`).

### Anti-Pattern 6: Treating the a11y phase as "add attributes"

**What people do:** add `tabindex` and `aria-*` in a sweep, treating it as declarative metadata.
**Why it's wrong:** in this codebase `tabindex="0"` on `#round-doc` is not metadata — it is the thing that makes b9664e0's already-shipped `keyup` listener execute for the first time. And `role="dialog"` without Escape-to-close and a focus trap is worse than no role at all: it announces a dialog contract the implementation does not honor.
**Do this instead:** treat P6 as implementing behavior, not annotating markup. Each ARIA attribute must be paired with the behavior it promises, verified by keyboard in UAT.

---

## Scaling Considerations

The scaling axis here is not users — it is viewport widths and future milestones.

| Concern | Today (1440px) | 1024px | 768px | 375px |
|---|---|---|---|---|
| Doc pane usable width | 1024 − 80 padding | 524px | 268px | fixed 420px sidebar exceeds the viewport → horizontal overflow |
| Sidebar | 420px fixed | 420px | 420px (44% of viewport) | overflows |
| `#state-badge` | `right: 448px` correct | correct | correct | off-screen / overlapping |
| Scroll owners | 5 nested | 5 nested | 5 nested | 5 nested, outer sidebar unusable |
| Breakpoints | **none declared** | — | — | — |

**What breaks first:** at ~1024px the doc pane (524px usable) is narrower than `.markdown-body { max-width: 720px }`, so every rendered document is silently constrained by the pane rather than by its own max-width — the design intent stops being expressed. At 768px the doc pane is 268px, narrower than a Chinese line of ~20 characters at 14px; reading becomes impractical. At 375px the layout overflows horizontally with no `min-width` guard or stacking fallback.

**Recommended adjustments:**
1. **≥1024px:** no change (the current design target).
2. **768–1024px:** `--sidebar-w: 320px`; doc pane padding drops one scale step. Both are token redefinitions in a media query — zero new rules (Pattern 2).
3. **<768px:** stack. `#app { flex-direction: column }`; sidebar becomes full-width and moves below the doc pane, or becomes a collapsible drawer. **This is a real design decision, not a CSS refactor** — it changes what "single interface" (DESIGN.md §3.2/§4.1) means at narrow widths, so it belongs in the UI-SPEC, not in an implementation plan. The roadmap should scope v1.14 to "narrow windows do not break" (no horizontal overflow, no unreadable text) and leave a stacked mobile layout explicitly out of scope.

**Second-order:** `#selection-menu` positioning is computed in JS from `range.getBoundingClientRect()` + `window.scrollX` with a viewport clamp (`app.js:1291-1306`). The clamp math is viewport-relative and stays correct at any width. No change needed — but do not "improve" it during the layout phase; it is working and it is on the flagship interaction path.

**Third-order (future milestones):** once `--sidebar-w` and the token block exist, dark mode becomes a bounded piece of work — a `@media (prefers-color-scheme: dark)` block redefining the *primitive* layer, with zero component rules touched. That is the real long-term return on P1, and it is worth naming in the UI-SPEC as the reason the two-tier token structure is non-negotiable.

---

## Regression Risk to the Five b9664e0 Fixes

All five shipped 2026-09-16 (`ed14c6e`, `f7eae48`, `0912429`; squashed as `b9664e0`). Each is a functional fix with a live CSS/JS coupling that this milestone will touch.

| Fix | Mechanism | Risk from v1.14 | Mitigation |
|---|---|---|---|
| **1. `.hidden` global rule** (`style.css:15`) | one `!important` rule; 5 elements depend on it exclusively | **HIGH** — a stylesheet rewrite that drops the `!important`, or a new tokenized `display`, silently un-hides 5 elements and restores 3 user-visible contradictions | Gate `grep -c '^\.hidden {'` = 1 in every `style.css` plan; Anti-Pattern 1; never move `.hidden` relative to `.overlay` *and* rewrite its declarations in the same commit |
| **2. SSE 断流横幅** (`#stream-banner`, `style.css:213-227`) | `position: fixed`, `z-index: 20`; `.fatal` variant | **MEDIUM** — tokenizing z-index can invert `20 > 10`; narrowing `--sidebar-w` can make the centred banner overlap the badge | Tokenize as `--z-badge: 10`, `--z-banner: 20`, `--z-modal: 100`, `--z-menu: 200` and assert the ordering in the token block comment; verify banner + badge at 768px in P4's gate |
| **3. 归档只读态加固** (`app.js:770-774`) | `processRoundBtn.disabled = true` + `authorizeRow.classList.add('hidden')` | **MEDIUM** — P3's `:disabled` restyling could make a disabled control look enabled; a `#authorize-row` display rule could defeat the `.hidden` | In P3, verify a disabled `#btn-process-round` is *visually* disabled, not just inert; do not add any `display` rule on `#authorize-row` |
| **4. 键盘划词路径** (`app.js:1327`) | `roundDoc` `keyup` → `handleSelectionTrigger` | **NOT A REGRESSION RISK — it is already dead.** `#round-doc` has no `tabindex`, so the listener cannot fire. | P6 must add `tabindex="0"` + `:focus-visible` + menu focus handoff together (Pattern 4). Flag in the roadmap that this "shipped fix" is currently inert — do not report it as delivered. |
| **5. 错误内联** (`.inline-error`, `style.css:42`; `showInlineError` `app.js:295-311`) | class created dynamically by JS with `className = 'inline-error'` | **MEDIUM** — P2 unifies `.hint` and `.inline-error` at 13px; if their colors converge during tokenization, error text stops being distinguishable from hint text | Freeze the class name `inline-error` (no rename); keep `--color-action-danger` distinct from `--color-text-muted` by hue, not only by lightness |

**The single highest-value guard for the whole milestone:** `grep -c '^\.hidden {' frontend/style.css` must return `1` in every plan that edits `style.css`. It costs one command and protects five shipped fixes and three user-visible contract invariants (no contradictory empty state, no stale placeholder, read-only archive honored).

---

## Open Questions for the UI-SPEC Author

These are design decisions, not research gaps — they must be resolved before P1 can be planned:

1. **Token names and the semantic split.** Specifically: what distinguishes `--color-action-positive` (例行正向) from `--color-action-gate` (门控动作) from `--color-action-irreversible` (G3)? The audit's core finding is that green currently means seven things; the token names *are* that decision.
2. **The irreversible-action treatment.** Solid fill vs. outline vs. size vs. confirmation affordance. The gate is that `#btn-authorize` must not be visually interchangeable with `#btn-continue-check`.
3. **The type scale anchor.** 13px (the current workhorse, 15 uses) or 14px (the markdown body)? This determines whether the densest UI text grows or the reading text shrinks.
4. **Whether `--fw-medium: 500` is consumed at all.** PingFang SC has a Medium weight, but 500-weight Chinese at 12–13px can render muddy. If hierarchy is expressed by scale + color instead, declare the token but do not consume it (Pattern 1's discipline) — or omit it.
5. **Narrow-window scope.** "Does not break" vs. "stacks into a mobile layout." The latter changes the meaning of DESIGN.md §4.1's two-column contract and is likely out of scope for v1.14.
6. **`#state-badge` positioning.** `calc()` (zero behavior change, badge stays fixed and may occlude scrolled content) vs. `position: absolute` inside `#doc-pane` (decouples from sidebar width entirely, badge scrolls away). The audit flagged the occlusion, so this is a real choice.
7. **Icon mechanism for the two CSS-`content` emoji.** Inline SVG data-URI in `content` is the only build-step-free option that is also platform-consistent. Confirm the approach and the two glyphs.

---

## Sources

All findings verified against the working tree at `main` @ `eca7682`, 2026-09-17.

- `/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/frontend/style.css` (631 L — read in full; the integration target)
- `/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/frontend/index.html` (221 L — read in full)
- `/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/frontend/app.js` (1,639 L — read in part: L1-140 handles/state, L1230-1340 selection path, plus targeted greps)
- `/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.planning/milestones/v1.13-phases/idi-03-g3/03-UI-REVIEW.md` (six-pillar audit, 13/24, 7 BLOCKERs — the scope source)
- `/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.planning/PROJECT.md` (v1.14 goal + six target-feature areas)
- Git: `b9664e0` (squash docs), and the three constituent fix commits `ed14c6e` (`.hidden` consolidation + archive hardening), `f7eae48` (SSE banner), `0912429` (keyboard selection + inline errors) — diffs read in full
- WCAG 2.1 SC 1.4.3 contrast arithmetic: computed independently in this research; the method reproduces all four audit-reported values (2.73 / 3.03 / 3.25 / 4.14) exactly, which validates the replacement values quoted in Pattern 1 (`#1a6fd4` = 4.92:1 white-on-blue; `#8a6508` = 4.96:1 on `#fdf6ec`; `#6b6b6b` = 5.10:1 on `#fafafa`)
- CSS Custom Properties and `var()` substitution semantics; `@media` condition evaluation ordering (`var()` not permitted in media query conditions); `:focus-visible` baseline availability — established web platform behavior, MEDIUM confidence on exact browser-version boundaries, HIGH confidence on the behavioral claims

---
*Architecture research for: retrofitting a design system onto a no-build vanilla frontend (v1.14 前端视觉与可访问性)*
*Researched: 2026-09-17*
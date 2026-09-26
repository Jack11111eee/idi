# Phase 5: 排版与视觉层级 - Pattern Map

**Mapped:** 2026-09-20
**Files analyzed:** 8 change units over 3 files (2 modified, 1 modified-but-code-frozen)
**Analogs found:** 8 / 8 (7 of them are **in-file** — this phase is a typography/hierarchy edit of an
existing single-source-of-truth stylesheet plus its two harness files, so the pattern to copy is the
file's own existing shape, not a sibling module)

> **Why the analogs are in-file.** Phase 5 adds no module, no selector family, and no file. The
> "closest existing analog" for a new `--text-*` declaration is the `--text-*` declaration already at
> `frontend/style.css:204-209`; for an appended `box-shadow: inset` state marker it is
> `#round-doc.round-frozen` at `:917-920`; for a token-wiring UAT assertion it is `item3` / `item6` /
> `item_smoke` in `scripts/check-05-ui-uat.py`. Inventing an out-of-file analog would be a false
> analog. Each entry below therefore names **exact HEAD line ranges** the executor replicates.

**Tracked-source gate (#3645):** all cited paths pass `git ls-files` (verified 2026-09-20):
`frontend/style.css`, `frontend/index.html`, `frontend/app.js`, `scripts/check-01-token-conformance.sh`,
`scripts/check-02-contrast.py`, `scripts/check-03-hidden-uniqueness.sh`,
`scripts/check-04-important-count.sh`, `scripts/check-05-ui-uat.py`. No gitignored mirror path is cited
anywhere in this document.

**HEAD line-number basis:** every range below is read from the disk HEAD of `frontend/style.css`
(1054 lines), **not** from `04-UI-SPEC.md` / `ROADMAP.md` (D-01: disk HEAD is the only reality
baseline; the contract's cited line numbers have drifted).

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `frontend/style.css` — fence `:root` declarations **L5-343** | config (design-token substrate) | transform (name → value map) | itself: tier-1 decl shape L46-70, tier-2 action families L127-142, type/weight/lh scales L204-221, `/* PAIR */` manifest L259-341 | exact (in-file) |
| `frontend/style.css` — fence comments **L42-45 / L204 / L217 / L311** | config (documentation inside the fence) | transform (prose → premise) | itself: the "role bands … and the four places it fails" block L72-115 (the in-file precedent for a comment that carries its own measurements) | exact (in-file) |
| `frontend/style.css` — `.markdown-body h1/h2/h3` **L624-626** | component style (content typography) | declarative | the sibling chrome heading overrides L405-410 / L432 / L611-615 / L548 (the four rules Hard Rule 9 fences against) | role-match |
| `frontend/style.css` — six action-button rules **L648-656 / L878-884 / L928-935 / L940-947 / L999-1008** | component style (action family) | declarative | `#btn-approve-draft` L648-656 (the family template: `background`/`border-color`/`color`/`font-weight` in one rule) | exact (in-file) |
| `frontend/style.css` — appended active-panel marker rules (end of file, after L1054) | component style (state marker) | declarative | `#round-doc.round-frozen` **L917-920** (`box-shadow: inset 3px 0 0 <token>`, the signed-off zero-layout-shift precedent) | exact |
| `frontend/style.css` — `.annotation-quote::before` **L836** / `.verdict-location::before` **L1021** | component style (decorative pseudo-element) | transform (emoji glyph → mask box) | `#chat-input-row input` L750-758 (`box-shadow: var(--shadow-composer)` — the in-file precedent for a fence token consumed by a plain declaration) | role-match |
| `scripts/check-05-ui-uat.py` | test (Playwright UAT harness) | request-response (browser → `getComputedStyle` → assert) | itself: `item3` L601-603 (token-wiring template), `item4` L742-761 (literal-px guard template), `item6` L989-1000, `item_smoke` L1014-1027, `check_frozen_marker` L499-545 (box-shadow semantic reader) | exact (in-file) |
| `scripts/check-02-contrast.py` | verifier / utility | transform (read-only, parse → measure → exit) | itself — **code frozen this phase**. Its manifest lives in the fence (L259-341), so 4 new `/* PAIR */` lines are added **in `style.css`**, and this file's bytes stay identical | exact (in-file) |

**Explicitly zero-change (do not open):** `frontend/app.js`, `frontend/index.html`,
`frontend/vendor/` (must still contain exactly `marked.min.js`), `scripts/ui-states/` (the five state
samples are read-only fixtures). Hard Rule 5 forbids renaming or deleting any of `app.js`'s ~70
top-level `getElementById` handles.

---

## Pattern Assignments

### 1. `frontend/style.css` — fence `:root` declarations (L5-343)

**Analog:** the block itself. Four sub-patterns to replicate.

**1a. Fence delimiters — must remain exactly one START and one END** (L5, L343):
```css
/* ===== DESIGN TOKENS: START ===== */
:root {
  ...
}
/* ===== DESIGN TOKENS: END ===== */
```
`scripts/check-01-token-conformance.sh:17-20` and `scripts/check-02-contrast.py:49-56` both assert the
pair is exactly `1/1` and exit non-zero otherwise. The markers are free-text comments matched by
substring; they must not be reworded, moved, or duplicated.

**1b. Tier-1 primitive declaration shape** (L46-70) — flat `--name: <literal>;`, bare literal legal
only inside the fence:
```css
  --white: #ffffff;
  --radix-gray-11: #646464;
  --radix-green-11: #218358;
  --radix-green-12: #193b2d;
  --radix-blue-11: #0d74ce;
```
**Phase 5 declares ZERO new tier-1 primitives** (S-7 / A-3): `--radix-green-11`, `--radix-green-12`
and `--radix-blue-11` are all already declared above and already consumed. Do not add `--radix-green-9`
/ `--radix-green-10` — the fence's own role-band record (L81-86) measures white-on-green-9 at 3.16 and
white-on-green-10 at 3.55, both below the 4.5:1 TEXT threshold.

**1c. Tier-2 semantic declaration shape** (L118-142) — `--color-*: var(--radix-*)`; the only names any
selector outside the fence may reference:
```css
  /* Tier 2 — action families (Q1). Phase 4: the three green families share one value pair;
     visual differentiation is Phase 5's one-line value edit. */
  --color-action-commit: var(--radix-green-11);
  --color-action-commit-surface: var(--radix-green-3);
  --color-action-commit-fg: var(--radix-green-12);
  --color-action-irreversible: var(--radix-green-11);
  --color-action-irreversible-surface: var(--radix-green-3);
  --color-action-irreversible-fg: var(--radix-green-12);
```
Note L127-128: the comment already **names this phase** as the one that performs the differentiation.
Phase 5 edits only the **values** on the right of these six lines (P-5…P-9): `-surface` green-3 →
green-11 / green-12, `-fg` green-12 → `var(--white)`. The declaration shape, the names, and the
consumers (L648-656, L940-947, L928-935) are untouched.

New tier-2 name to add alongside (D-18), following the same shape:
```css
  --color-marker-active: var(--radix-blue-11);
```

**1d. The type / weight / line-height scale block** (L204-221) — the insertion site for D-06/D-07:
```css
  /* Type scale — 5 sizes (ChatGPT 视觉语言;TOKEN-08 的字面刻度由用户决策覆盖,意图不变). All consumed. */
  --text-xs: 12px;
  --text-base: 14px;
  --text-md: 16px;
  --text-lg: 18px;
  --text-xl: 24px;

  /* Weight — three ranks, all consumed. ... */
  --fw-regular: 400;
  --fw-medium: 500;
  --fw-semibold: 600;

  /* Line height — four, paired with the size scale (24/32, 12/16, 14/20, 18/28, 16/26). */
  --lh-tight: 1.3333;
  --lh-snug: 1.4286;
  --lh-compact: 1.5556;
  --lh-reading: 1.625;
```
Two new lines insert **immediately after L209 (`--text-xl: 24px;`)**, in **name order** not numeric
order (xs → base → md → lg → xl → 2xl → 3xl), so the fence reads as "the next step up" rather than as
a mid-scale edit:
```css
  --text-2xl: 22px;
  --text-3xl: 28px;
```
The L204 comment's `5 sizes` and the L217 comment's integer-pairing list both become false the moment
these two lines land — see assignment 2. L211-215 (`--fw-*`) and L218-221 (`--lh-*`) are **not**
edited: D-10 adds zero line-height tokens.

**1e. `/* PAIR */` manifest entries** (L259-341) — the shape is a comment-only line, token names only,
never hex:
```css
  /* amber text on its three real grounds, and the six green buttons (three families, one value) */
  /* PAIR --color-action-warning ON --color-surface-warning TEXT */
  /* PAIR --color-action-routine-fg ON --color-action-routine-surface TEXT */
  /* PAIR --color-action-commit-fg ON --color-action-commit-surface TEXT */
  /* PAIR --color-action-irreversible-fg ON --color-action-irreversible-surface TEXT */
```
Four new lines append to the existing groups (TEXT group after L317; NON-TEXT group after L337). The
regex at `scripts/check-02-contrast.py:28-31` requires the exact form
`/* PAIR <fg> ON <bg> (TEXT|NON-TEXT)[@alpha] */`; a name not declared in the fence makes the checker
`sys.exit(1)` (L79-81). The L311 comment's "three families, one value" is falsified by P-5…P-9 and
must be rewritten in the same commit (see assignment 2).

**1f. The two `--icon-*` data-URI tokens** (D-20) — new declarations, fence-internal literals. Shape
contract (mechanically checkable, UI-SPEC §VISUAL-05):
```css
  --icon-pin:      url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'%3E%3Cpath d='…'/%3E%3C/svg%3E");
  --icon-location: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'%3E%3Cpath d='…'/%3E%3C/svg%3E");
```
Hard constraints: exactly 1 `<path>`, **no `fill` attribute**, **zero color information** (no `%23`,
no `#`, no `fill=`), `xmlns` present, `viewBox="0 0 12 12"`. Zero color info is the sole basis for
retiring literal exception L-3 (A-1) and is Gate 5's assertion:
`grep -oE '%23[0-9a-fA-F]{3,8}' frontend/style.css | wc -l` must print `0`.

**Hard Rule 5 accounting (must hold in one commit — no orphan token):** each new token has exactly one
consumer, in the same diff.

| New token | Its same-commit consumer |
|---|---|
| `--text-2xl` 22px | `.markdown-body h2` (`style.css:625`) |
| `--text-3xl` 28px | `.markdown-body h1` (`style.css:624`) |
| `--color-marker-active` | the appended marker rules (assignment 5) |
| `--icon-pin` | `.annotation-quote::before` (`:836`) |
| `--icon-location` | `.verdict-location::before` (`:1021`) |

---

### 2. `frontend/style.css` — four fence-comment rewrites (L42-45 / L204 / L217 / L311)

**Analog:** the fence's own role-band record at **L72-115** — the in-file precedent for a comment that
carries its own measurements and says *why* the band was left. Copy that register (numbers inline,
`scripts/check-02-contrast.py` named as the arbiter, upstream AA claims explicitly not adopted).

**2a. L42-45 — the "9/10 fill steps" forecast is now false** (A-4):
```css
     Only the steps a tier-2 token consumes in this same commit are declared
     (D-04 / Hard Rule 5 — never declare a token you are not consuming), so the
     1-12 scale is deliberately incomplete; Phase 5 declares the 9/10 fill steps
     together with their consumers. */
```
Rewrite to "Phase 5 reuses the already-declared 11/12 steps; the reason is the role-band record
below." The first three lines stay true and must be preserved verbatim.

**2b. L204 — `5 sizes` → 7** with the name-vs-value caveat (A-6 / 05-N-1). The rewritten comment must
state that the contract's `--text-2xl` means 18px while this fence's `--text-2xl` means 22px —
**same name, different value, not a typo**. Without it, a future reader reconciling against
`04-UI-SPEC.md` will "fix" 22px back to 18px and create a second name for 18px (`2xl` and `lg`), i.e.
a second source of truth.

**2c. L217 — "integer pairing" → "ratio pairing"** (D-10). Two pre-existing defects must be fixed in
the same rewrite or the new comment is self-contradictory (UI-SPEC §行高):
```css
  /* Line height — four, paired with the size scale (24/32, 12/16, 14/20, 18/28, 16/26). */
```
- `18/28` is **arithmetic error**: 18px × `--lh-tight` 1.3333 = **24**, not 28.
- The header says `four` while the size-scale pairing only lists three; `--lh-compact` (1.5556) is
  chrome-only (sole consumer `.overlay-card p`, `:549`) and is not part of the size-scale pairing.
  Either give it its own line marked "chrome-only" or drop the word `four`.

**2d. L311 — "three families, one value" is falsified** by P-5…P-9:
```css
  /* amber text on its three real grounds, and the six green buttons (three families, one value) */
```
After this phase the three green families hold three *different* value pairs. Same failure mode as
04.1-N-8: a comment that explains code must change when its premise disappears, or it starts lying.

---

### 3. `frontend/style.css` — `.markdown-body h1/h2/h3` font sizes (L616-626)

**Analog (the rule being edited):** itself.
```css
.markdown-body {
  line-height: var(--lh-reading);
  font-size: var(--text-md);
}
/* 标题字号显式化,作用域限定在 .markdown-body 内——不写全局 h1/h2/h3,
   那会与四处 chrome 覆盖(.panel-header h2 / #draft-view h2 / #brainstorm-view h2 / .overlay-card h3)碰撞。
   阅读列宽度由 #main-pane > section 的 max-width 承担,此处不再重复声明(面板内它本就不生效)。 */
.markdown-body h1, .markdown-body h2, .markdown-body h3 { margin: var(--space-4) 0 var(--space-2); line-height: var(--lh-tight); font-weight: var(--fw-semibold); }
.markdown-body h1 { font-size: var(--text-xl); }
.markdown-body h2 { font-size: var(--text-lg); }
.markdown-body h3 { font-size: var(--text-md); }
```
The comment at L620-622 **already states Hard Rule 9** and is the in-file statement of the scope
fence — preserve it. Only the three `font-size` values change (P-2…P-4): `h1` → `var(--text-3xl)`,
`h2` → `var(--text-2xl)`, `h3` → `var(--text-lg)`. The shared L623 rule (margin / `line-height:
var(--lh-tight)` / `font-weight: var(--fw-semibold)`) is already correct — D-09 and D-10 require
**zero** change to it.

**The scope fence is mechanical, not stylistic** (UI-SPEC §字号刻度的范围栅栏). None of the four
chrome headings sits inside a `.markdown-body` container, so `.markdown-body h1` (0-1-1) and the
chrome overrides never meet in the cascade. The four chrome analogs to verify unchanged:

| Chrome heading | Rule | `index.html` position |
|---|---|---|
| `.panel-header h2` | `style.css:432` | `:16` `:31` `:42` `:58` |
| `#draft-view h2` | `style.css:611-615` | `:105` (sibling of `#draft-content`, not a child) |
| `#brainstorm-view h2` | `style.css:679-683` | `:120` (sibling of `#brainstorm-content`) |
| `.overlay-card h3` | `style.css:548` | `:160` `:172` `:186` `:198` `:215` |

**The `.markdown-body` hosts (the blast radius, name them in the plan):** `#draft-content`
(`index.html:113`), `#brainstorm-content` (`:121`), `#round-doc` (`:139`), `#latest-check` (`:47`).

---

### 4. `frontend/style.css` — six action-button rules (L648-656 / L878-884 / L928-935 / L940-947 / L999-1008)

**Analog:** `#btn-approve-draft` (L648-656) — the family template. Every green button rule in the file
is the same four-declaration shape:
```css
#btn-approve-draft {
  margin-top: var(--space-4);
  padding: var(--space-2) var(--space-4);
  background: var(--color-action-commit-surface);
  border-color: var(--color-action-commit);
  color: var(--color-action-commit-fg);
  font-weight: var(--fw-semibold);
}
#btn-approve-draft:disabled { opacity: 0.55; cursor: not-allowed; }
```
Sibling instances of the identical shape: `#btn-process-round` L878-884, `#btn-authorize` L928-935,
`#btn-start-writing` L940-947, `#btn-continue-check, #btn-continue-repair` L999-1008.
`#btn-divergence` L661-668 has the shape but belongs to the amber family and is **not** one of the six
(UI-SPEC §TYPE-03: pulling it in would create an unregistered fourth tier).

**Phase 5 edits (P-12 / P-13), by line:**

| Rule line | Selector | HEAD | Phase 5 |
|---|---|---|---|
| `:654` | `#btn-approve-draft` | `--fw-semibold` | → `--fw-medium` |
| `:666` | `#btn-divergence` | `--fw-semibold` | **unchanged** |
| `:882` | `#btn-process-round` | `--fw-semibold` | → `--fw-medium` |
| `:933` | `#btn-authorize` | `--fw-semibold` | **stays 600** (D-12, the sole registered exception) |
| `:945` | `#btn-start-writing` | `--fw-semibold` | → `--fw-medium` |
| `:1003` | `#btn-continue-check, #btn-continue-repair` | `--fw-semibold` | → `--fw-medium` |

Plus **one added declaration** inside `#btn-authorize` (L928-934): `font-size: var(--text-md);`
(16px, an existing step — zero new tokens). **No padding step** (D-13); the padding stays
`var(--space-2) var(--space-4)`.

**`:disabled` is untouched (D-14):** all six `opacity: 0.55` lines (L656, L668, L884, L935, L947, L1006)
stay byte-identical. Pitfall M5 forbids softening them; on a solid fill 0.55 is a *stronger* fade.

**Selector structure is untouched (D-11):** the three family rules already declare
`background` / `border-color` / `color` from the three `-surface` / base / `-fg` tokens. The whole
three-tier ramp is a pure value edit in the fence plus the two weight edits above — no selector moves,
no declaration added or removed. `--color-action-irreversible*` keeps exactly one consumer
(`#btn-authorize`) forever (D-15).

---

### 5. `frontend/style.css` — appended active-panel marker rules (after L1054)

**Analog:** `#round-doc.round-frozen` (L917-920) — the signed-off precedent for the exact mechanism,
including its comment, which is the argument the plan must reproduce:
```css
/* 冻结轮只读信号(D-P2-21:轮 < 当前轮的呈现服务端 409 是防线)。
   只读 = 去饱和(不动亮度,因而正文对比度不受影响)+ 左侧 3px 琥珀 inset 竖线。
   原来的不透明度乘数已删除:它合成整棵子树(含 Phase 7 的焦点环),
   使正文降到 3.84:1、焦点环降到 2.85:1;删除后正文回到 16.67:1、环回到 5.62:1。
   box-shadow 不参与布局 ⇒ 零位移,纯重构判据成立(绝不用 border-left —— 它会加 3px 宽度)。 */
#round-doc.round-frozen {
  filter: saturate(0.6);
  box-shadow: inset 3px 0 0 var(--color-action-warning);
}
```
Copy the mechanism (`box-shadow: inset 3px 0 0 <token>`, never `border-left`) and copy the comment
register. New rules **append at the end of the file**, after L1054 — Hard Rule 3 ("append, do not
reorder"); the file already has three append-at-end blocks (L1042-1048, L1050-1054) as precedent.
The UI-SPEC supplies the rule bodies verbatim (§VISUAL-04 落地规格):

```css
#session-panel:not(.hidden) .panel-header,
#annotations-panel:not(.hidden) .panel-header,
#checks-panel:not(.hidden) .panel-header {
  box-shadow: inset 3px 0 0 var(--color-marker-active);
}
#session-panel:not(.hidden) .panel-header h2,
#annotations-panel:not(.hidden) .panel-header h2,
#checks-panel:not(.hidden) .panel-header h2 {
  color: var(--color-marker-active);
}
```

**Four load-bearing choices, each with its in-file evidence:**
1. `box-shadow: inset` on `.panel-header`, not `<section>` — the three sections' children carry their
   own backgrounds (`.chat-bubble` L716-723, `.annotation-item` L827-833 `background:
   var(--color-surface)`, `.event-list` L476-487, `.panel-body` L436), and an inset shadow is painted
   on the element's own background layer, so those children would cover it (05-N-4).
2. Title changes `color` only, not `font-weight` — `.panel-header` is `height: 36px` +
   `justify-content: space-between` (L421-430), so a weight change would shift `#pending-count` /
   `#check-state`; and D-09 already fixes chrome headings at 500.
3. `3px` matches `.markdown-body blockquote`'s `border-left: 3px` (L630). It is a `box-shadow` offset
   component, not a `--space-*` value; L-1…L-5 never covered it and L919 is the precedent.
4. `#doc-panel-header` is a `.panel-header` (`index.html:84`) but is matched by none of the three ID
   selectors — no accidental coverage.

**Cascade accounting** (`.hidden { display: none !important }` at L357 is a mechanism and is not
touched; `:not(.hidden)` *reads* that state):
`:not(.hidden)` contributes 0-1-0; each new selector is 1-2-0 (or 1-2-1 for the `h2` form), beating
`.panel-header` (0-1-0, no `box-shadow` declared) and `#annotations-panel .panel-header { cursor:
default }` (1-1-0, L807) / `#checks-panel .panel-header { cursor: default }` (1-1-0, L979) on a
different property. The IDs win on the 1-0-0 component regardless of source order — but append
anyway, because someone may later add `box-shadow` to `.panel-header`.

---

### 6. `frontend/style.css` — two `::before` emoji → mask (L836 / L1021)

**Analog (the rules being rewritten in place):**
```css
.annotation-quote::before { content: '📌 '; }   /* L836 */
.verdict-location::before { content: '📍 '; }   /* L1021 */
```
Both selectors occur **exactly once in the file, with no competitor**, so an in-place rewrite is
cascade-equivalent to appending and avoids leaving a dead overridden `content: '📌 '` at the tail.
That is why Hard Rule 3 is not violated (UI-SPEC §两条伪元素规则).

Target shape (UI-SPEC §VISUAL-05, per D-20/D-21/D-22):
```css
.annotation-quote::before {
  content: '';
  display: inline-block;
  width: 12px;
  height: 12px;
  margin-right: var(--space-1);
  vertical-align: -2px;
  background-color: var(--color-text-secondary);
  -webkit-mask-image: var(--icon-pin);
  mask-image: var(--icon-pin);
  -webkit-mask-size: 12px 12px;
  mask-size: 12px 12px;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
}
```
Three details, each missing one is a bug: (1) `margin-right: var(--space-1)` — the old
`content: '📌 '` carried a trailing space that a 12px box does not; (2) **both** `-webkit-mask-*` and
`mask-*` — the only permitted redundancy, unprefixed for modern Chrome / prefixed for WebKit;
(3) `mask-repeat: no-repeat` and `mask-size` must be explicit (default is `repeat`; an SVG has a
viewBox but no intrinsic size, so `auto` is engine-dependent).

**Color contrast needs no new pairs** — the two grounds already have TEXT entries: `.annotation-item`
is `background: var(--color-surface)` (L831) and `.verdict-card` is `background:
var(--color-surface-warning-subtle)` (L1016); the manifest already lists
`--color-text-secondary ON --color-surface` (5.62) and `--color-text-secondary ON
--color-surface-warning-subtle` (5.82) at L290-291. TEXT (4.5) is stricter than NON-TEXT (3.0), so a
NON-TEXT pair would be a tautology.

**`.collapse-indicator` (L434) is untouchable (D-23):** `app.js:1563` / `:1569` assign it via
`textContent`, so an inline `<svg>` would be erased. Its `font-size: 20px; line-height: 1;` stays
byte-identical — Gate 6 asserts the selector line is unchanged.

---

### 7. `scripts/check-05-ui-uat.py` — assertion updates (D-02 / D-03 / D-04)

**Analog A — the token-wiring assertion template (D-14's product).** `item3` L601-603 states the rule
in-file; every wiring assertion in the file follows it:
```python
    # D-14:期望侧一律来自运行时解析出的令牌,不再硬编码 rgb。
    # 每条断言旁的 info() 打印解析值 —— 这是「接线对但值错」留下的人工核对痕迹;
    # 值本身的仲裁者是 scripts/check-02-contrast.py,不是本 harness。
    muted = resolve_color(page, "--color-text-muted")
    ...
    ok(item, "[p1] .hint color == var(--color-text-muted)", muted,
       read_style(page, ".hint", "color"))
```
Same template at `item4` L766-776 (via `resolve_token`) and `item_smoke` L1014-1027. Helpers:
`resolve_color` L258-278 (returns `None` when the token is undeclared — never a false PASS),
`resolve_token` L281-291, `read_style` L247-248, `ok` L102-122 (a `None` on either side emits
**BLOCKED**, never PASS), `ok_true` L132-133, `info` L154-156.

**Analog B — the literal-px guard template.** `item4` L742-761 is the pattern for the assertions that
must **keep** their hard-coded pixels (D-03 second class):
```python
    ok(item, "[p1] #brainstorm-view h2 font-size", "16px", read_style(page, "#brainstorm-view h2", "font-size"))
    ok(item, "[p1] #draft-view h2 font-size", "18px", read_style(page, "#draft-view h2", "font-size"))
    ok(item, "[p1] .panel-header h2 font-size", "14px", read_style(page, ".panel-header h2", "font-size"))
    ok(item, "[p1] .overlay-card h3 font-size", "24px", read_style(page, ".overlay-card h3", "font-size"))
```
and the S-2 dependency guard L797-807 (`--text-base == "14px"` via `ok_true`) — also stays literal.
The in-file rationale for the split is already written at L716-717 and L740-741.

**Analog C — the box-shadow semantic reader.** `parse_box_shadow` L479-490 + `check_frozen_marker`
L499-545 is the exact reader to reuse for the active-panel marker assertion. Note the idiom: parse
into `{inset, color, x, y, blur, spread}`, then assert each component with `ok_true` and a
**runtime-resolved** color expectation, with `blocked(...)` when the shadow is missing or
unparsable:
```python
    raw = read_style(page, "#round-doc", "box-shadow")
    frozen_amber = resolve_color(page, "--color-action-warning")
    expected_shadow = f"inset 3px 0 0 {frozen_amber}"
    parsed = parse_box_shadow(raw) if raw else None
    ... parsed["inset"] and parsed["x"] == "3px" and parsed["y"] == "0px"
        and parsed["blur"] == "0px" and parsed["spread"] == "0px"
        and norm(parsed["color"]) == norm(frozen_amber)
```

**The object of the D-04 inversion** — L683-695, currently asserting the three attributes are
byte-identical between the routine and irreversible buttons:
```python
    proc_color = read_style(page, "#btn-process-round", "color")
    proc_border = read_style(page, "#btn-process-round", "border-top-color")
    proc_bg = read_style(page, "#btn-process-round", "background-color")
    auth_color = read_style(page, "#btn-authorize", "color")
    ...
    ok_true(
        item,
        "[p3] #btn-process-round 与 #btn-authorize 三属性逐字节相同",
        (proc_color, proc_border, proc_bg) == (auth_color, auth_border, auth_bg),
        ...
    )
```
Invert to "within-tier identical + across-tier pairwise distinct" using the UI-SPEC's snippet
(§The Four Contract-Check Commands) and the existing `trio` shape. **Why one state suffices:** all six
buttons are permanently in the DOM; `getComputedStyle` returns resolved computed values even for
`display: none` subtrees (`color` / `background-color` / `border-color` are layout-independent), and
the file already reads `#btn-authorize` in `p3` without a visibility check (L677-682).

**Placement:** new assertions go in `item4` (p1 + p3 samples already entered at L710-711 and L779-780)
and `item1`/`item3` as appropriate; `item_smoke` L1006-1038 is the cheap end-to-end slice to extend
first for fast feedback. Item dispatch is `main()` L1098-1111; `--item` values are validated against
`known` at L1073-1076.

**D-03 classification (the easiest thing to get wrong — copy this table into the plan):**

| Class | Assertion | Handling |
|---|---|---|
| Phase-5-changed value | `#brainstorm-view h2` font-size (`:742`), `.markdown-body h1/h2/h3` font-size (**new**), button font-size / font-weight (**new**) | rewrite as token wiring — expectation from `resolve_token` / `resolve_color`, no hard-coded px |
| Guard for a value that must NOT move | `.panel-header h2` 14px (`:746`), `#draft-view h2` 18px (`:745`), `.overlay-card h3` 24px (`:747`), `.markdown-body` 16px (`:751`), `.markdown-body code` 14px (`:760`), `--text-base == 14px` (`:800-807`) | **keep literal px** |

The literal-px guards are a **feature, not a defect**: they are the only shape that catches "the
heading change leaked into chrome". Converting `.panel-header h2` to token wiring would degrade it to
a tautology. `#brainstorm-view h2` is different — the 14px it guards was already overturned by
`260918-qrq`, so continuing to hard-code it only keeps a false FAIL alive (D-02).

**New assertions required** (UI-SPEC §The Four Contract-Check Commands, full table):
`.markdown-body h1/h2/h3` == `--text-3xl` / `--text-2xl` / `--text-lg`; `#btn-authorize` font-size ==
`--text-md` and font-weight == `600`; the five other buttons' font-weight == `500`;
`#doc-panel-header h1` font-size `14px` + font-weight `500` (literal — VISUAL-03's guard);
active-panel marker on `p1` / `p3` / `checking` with `#ai-panel .panel-header` `box-shadow == none`;
active-panel `h2` color == `--color-marker-active`; both `::before` `width` / `height` == `12px`,
`background-color` == `--color-text-secondary`, `mask-image != none`.

**In-file note about the stale diagnostics string at `:588`:** it stays (backlog `999.1`, see 05-N-6).

---

### 8. `scripts/check-02-contrast.py` — zero code change

**Analog:** itself, and the point is that **nothing in it is edited.** The manifest it reads lives in
the fence (`style.css:259-341`); the file's own docstring states the design:
```python
"""CHECK-02 — WCAG contrast verification for the design-token layer.
Pairs are derived from the contrast manifest written as comments inside the
fenced `:root` block of frontend/style.css — the same diff that declares the
tokens, so a drift between the manifest and the tokens is visible in review.
A manifest entry naming a token that is not declared in the fence (or an
ordering entry naming a pair that is not listed) is a contract-drift signal
and fails loudly; it is never silently skipped.
"""
```
Guards the phase must keep satisfied, all in-file and all unmodified:
- fence pair exactly 1/1 — L49-56;
- coverage floor `>=24 pairs, >=20 TEXT, >=4 NON-TEXT` — L150-155 (43 → 47 keeps this green);
- every `/* PAIR` / `/* ORDER` marker must parse — L161-175 (a malformed new manifest line fails here);
- closed-interval comparison, no rounding to the threshold — L198-202 (4.496 fails, 4.504 passes);
- the `ORDER` entry (L341) resolves against TEXT pairs — L207-226.

**Phase 5 expected result:** `PASS: 0 failures` over **47 pairs (35 TEXT + 12 NON-TEXT) + 1 ORDER**,
exit 0. The three pairs whose *values* move without their manifest line changing are L315-317.

---

## Shared Patterns

### Token wiring is the assertion form (not hard-coded values)
**Source:** `scripts/check-05-ui-uat.py:258-291` (`resolve_color` / `resolve_token`) + `:601-603` (the
D-14 comment) + `:1014-1027` (the smoke slice).
**Apply to:** every **new** assertion in assignment 7, and the reclassified `#brainstorm-view h2`
assertion.
**Why:** the expectation side comes from the running page, so a future value-layer change produces no
false FAIL. The literal-px form is reserved for the guards in D-03's second class. Value arbitration
belongs to `scripts/check-02-contrast.py`, never to this harness.

### Fence pair is asserted before it is trusted
**Source:** `scripts/check-01-token-conformance.sh:11-20` and `scripts/check-02-contrast.py:49-56`.
**Apply to:** every change that touches `style.css` (i.e. all of assignments 1-6).
Both scripts refuse to run unless there is exactly one START and one END marker — a removed END marker
would otherwise make the guard vacuous. Do not reword the markers.

### Count occurrences, not lines
**Source:** `scripts/check-01-token-conformance.sh:27-28` (`grep -o | wc -l`), `check-04` L11 (same
idiom, with the L1-4 comment explaining that `grep -c '!important'` returns 3 while the declaration
count is 1), `check-03` L11 (`^[[:space:]]*\.hidden[[:space:]]*\{`, deliberately not anchored to
column 0).
**Apply to:** Gate 5 (`grep -oE '%23…' | wc -l` must print 0) and any new counting gate.

### Append at the end; never reorder
**Source:** `frontend/style.css:1042-1048` and `:1050-1054` — two existing append-at-end blocks whose
comments state the reason (`0-2-0` descendant selectors that must win on source order).
**Apply to:** the two active-panel marker rules (assignment 5).
**Why:** `#draft-view h2` (L611, 1-0-1) and `#brainstorm-view h2` (L679, 1-0-1) are separated by source
order — the latter wins, giving `--color-action-warning`. Reordering is a render change whose diff
looks innocent.

### A new token ships with its consumer in the same commit
**Source:** `frontend/style.css:42-44` (the rule stated in the fence) and the existing
`--color-kind-fg` / `--color-border-danger-subtle` pair at L179-181, commented
`/* Tier 2 — declared with their consumers (Hard Rule 5): .event-kind / .fatal. */`.
**Apply to:** all five new tokens in assignment 1 — see the Hard Rule 5 table there. A new comment
following the L179 shape is the in-file precedent for recording the consumer next to the declaration.

### `:disabled` opacity 0.55 is a deliberate exemption, not a defect
**Source:** `frontend/style.css:656` `:884` `:935` `:947` `:1005-1008`.
**Apply to:** assignment 4 — zero changes. Pitfall M5; D-14.

### The `.hidden` mechanism is not styling
**Source:** `frontend/style.css:353-357` — the comment already spells out why `!important` is required
(three 1-0-0 competitors declare `display: flex`).
**Apply to:** assignment 5 — `:not(.hidden)` reads that state and does not modify it; the rule itself
is untouched, and `check-03` (`^\.hidden {` == 1) / `check-04` (`!important;` == 1) must stay green.

---

## No Analog Found

| File | Role | Data Flow | Reason |
|---|---|---|---|
| (none) | — | — | Every change unit in this phase has an in-file analog. This is the expected shape of a phase whose entire change surface is one existing stylesheet plus its two harness files. |

**Genuinely novel artifacts, with no code analog anywhere (planner should take these from the UI-SPEC
directly, not from a codebase search):**

| Artifact | Where | Source of truth |
|---|---|---|
| The two `<path d='…'>` data values | `style.css` fence, `--icon-pin` / `--icon-location` | UI-SPEC §VISUAL-05 shape contract + D-22 (a solid pin and a solid map marker, `viewBox="0 0 12 12"`, no `fill`). No icon asset exists in the repo and none may be added |
| Gate 5 / Gate 6 (the two new phase-specific gates) | run ad hoc, not new files | UI-SPEC §The Four Contract-Check Commands |
| The `--color-marker-active` / green-11 / green-12 step assignment | fence | UI-SPEC §Color + S-7; arbitrated by `check-02`, not by upstream AA claims |

---

## Metadata

**Analog search scope:** `frontend/` (style.css, index.html, app.js), `scripts/` (check-01…05,
probe-05-resolve-color.py, ui-states/). No other directory in the repo holds renderable or verifiable
surface for this phase.
**Files scanned:** 8 (5 check scripts, 3 frontend files); `frontend/style.css` read in full (1054
lines, single pass), `scripts/check-05-ui-uat.py` read in 5 non-overlapping targeted ranges
(1-175, 240-320, 370-535, 594-833, 928-1147).
**Tracked-source gate:** all 8 cited paths verified with `git ls-files` on 2026-09-20; no gitignored
mirror path is cited.
**Pattern extraction date:** 2026-09-20
**Baseline:** disk HEAD of `frontend/style.css` (1054 lines) — D-01. HEAD counts confirmed by direct
measurement: `/* PAIR` = 43, `/* ORDER` = 1, `--text-*` scale = 5, fence delimiters = 1/1.
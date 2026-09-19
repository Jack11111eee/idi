# Phase 04.1: Radix 颜色族重写 - Pattern Map

**Mapped:** 2026-09-19
**Files analyzed:** 4 (2 code files modified in place, 1 script rewritten, 1 script whose contract is consumed)
**Analogs found:** 4 / 4 (every analog is **in-file** — this phase is a value-layer rewrite of an existing single-source-of-truth, so the pattern to copy is the file's own existing shape, not a sibling module)

> **Why the analogs are in-file.** Phase 04.1 changes no selector and adds no module. The
> "closest existing analog" for a tier-1 declaration is the tier-1 declaration already in
> `style.css:8-33`; for a token-wiring UAT assertion it is `item6`/`item_smoke` in
> `scripts/check-05-ui-uat.py`. There is no other file in the repo that does these things —
> inventing one would be a false analog. Each entry below therefore names **exact line ranges**
> the executor replicates.

**Tracked-source gate (#3645):** all four cited paths pass `git ls-files` (verified 2026-09-19):
`frontend/style.css`, `scripts/check-02-contrast.py`, `scripts/check-05-ui-uat.py`,
`frontend/index.html`, `frontend/app.js`, `frontend/vendor/marked.min.js`. No gitignored mirror
path is cited anywhere in this document.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `frontend/style.css` — fence `:root`, **L5-L224** | config (design-token substrate) | transform (name → value map) | itself: fence delimiters L5/L224, decl shape L8-33 + L36-103, manifest block L159-222 | exact (in-file) |
| `frontend/style.css` — `#state-badge` rule **L463-470** (R-1 restore `z-index`) | component style | declarative | `#stream-banner` rule L473-486 (the ordering partner, already consumes a z-index token) | role-match |
| `frontend/style.css` — `.overlay-card` rule **L421-427** (R-2 restore `box-shadow`) | component style | declarative | `#chat-input-row input` L629-637 (`box-shadow: var(--shadow-composer)`) + token decl L96 | exact for the declaration shape |
| `frontend/style.css` — `.tier-desc` rule **L851** (R-3 delete `opacity: 0.9`) | component style | declarative | the sibling `:disabled` opacity sites L840 (kept) — R-3 is a **deletion**, so the pattern is "remove the declaration, touch nothing else" | partial |
| `scripts/check-02-contrast.py` | verifier / utility | transform (read-only, parse → measure → exit) | itself: fence reader L44-69, manifest regexes L27-41, loud-fail contract L79-81/L104 | exact (in-file) |
| `scripts/check-05-ui-uat.py` | test | request-response (Playwright → `getComputedStyle`) | itself: `item6` L860-905 and `item_smoke` L911-932 (the token-wiring template D-14 names) | exact (in-file) |

**Explicitly zero-change (do not open):** `frontend/app.js`, `frontend/index.html`,
`frontend/vendor/marked.min.js`. Hard Rule 5 forbids renaming or deleting any of `app.js`'s ~70
top-level `getElementById` handles; D-13's `#doc-pane` → `#doc-panel-body` correction is a change
to the **UAT expectation string**, never to an id.

---

## Pattern Assignments

### `frontend/style.css` — the fenced `:root` block (L5-L224)

**Analog:** the block itself. Four sub-patterns to replicate.

**1. Fence delimiters — must remain exactly one START and one END** (L5, L224):
```css
/* ===== DESIGN TOKENS: START ===== */
:root {
  ...
}
/* ===== DESIGN TOKENS: END ===== */
```
Both `scripts/check-01-token-conformance.sh:17-20` and `scripts/check-02-contrast.py:49-56`
assert the pair is exactly `1/1` and `sys.exit(1)` / `exit 1` otherwise. The markers are free-text
comments matched by substring (`===== DESIGN TOKENS: START`); they must not be reworded.

**2. Tier-1 primitive declaration shape** (existing, L10-11) — flat `--name: <literal>;`, bare
literal legal only here:
```css
  --gray-900: #0d0d0d;
  --gray-700: #8f8f8f;
```
New shape per D-03 (UI-SPEC `### Tier 1`, 25 primitives):
```css
  --radix-gray-11: #646464;
  --radix-gray-12: #202020;
```
Every tier-1 line is `<2 spaces>--<name>: <literal>;` — no `var()`, no shorthand. `--white`
(L8) keeps its name and its `#ffffff` literal (04.1-N-6). The existing same-value comment
convention (`--gray-600: #8f8f8f; /* ... */`, L12) is the in-file precedent for the mapping-table
comments V-12 requires; L12's comment itself must go with the value it excuses.

**3. Tier-2 semantic declaration shape** (existing, L36-38, L74) — always `var(--tier-1)`:
```css
  --color-text: var(--gray-900);
  --color-text-muted: var(--gray-600);
  --color-surface: var(--white);
```
New shape (UI-SPEC `### Tier 2`): `--color-text-muted: var(--radix-gray-11);` — the tier-2
**name is frozen verbatim** (D-02), only the right-hand `var()` target changes. The two deleted
names (R-4: `--color-text-inverse` L101, `--color-surface-info-strong` L91) are removed **together
with their explanatory comments** at L88-90 and L99-100 — 04.1-N-8: leaving the comment would be
a comment that lies about the code.

**4. The `/* PAIR */` and `/* ORDER */` comment grammar** — the exact strings the checker's
regexes match. Existing exemplars (L169, L196, L222):
```css
  /* PAIR --color-text-muted ON --gray-25 TEXT */
  /* PAIR --color-text-inverse ON --color-surface-info-strong TEXT */
  /* ORDER --color-text-muted BEFORE --color-text ON --gray-25 */
```
The authoritative grammar (from `scripts/check-02-contrast.py:28-35`):
```
/* PAIR  <fg-token>  ON  <bg-token>  TEXT|NON-TEXT [@<alpha>] */
/* ORDER <quieter-token>  BEFORE  <louder-token>  ON  <bg-token> */
```
Hard constraints the regexes impose — a partial or reformatted edit fails loudly, not silently:
- tokens are `--[a-z0-9-]+` only; **names, never hex** (L166's own rule).
- the `/* PAIR` and `/* ORDER` marker prefixes are counted raw and must equal the parsed count
  (`check-02-contrast.py:161-175`) — so **no stray `/* PAIR` in prose**.
- `@<alpha>` is `[0-9.]+` and only legal on `TEXT` entries (L28-31).
- an `ORDER` operand must be a listed **plain TEXT** pair on the same ground (L207-213).
The replacement manifest is written verbatim in UI-SPEC `### The manifest, verbatim` (43 pairs +
1 ORDER) — copy it as-is, same order, same comments.

**The manifest block header comment** (existing L159-166) is the shape to extend; V-12 requires it
to also carry the name↔step mapping table and the four override notes.

---

### `frontend/style.css` — `#state-badge` (L463-470), R-1

**Analog:** `#stream-banner` (L473-486) — the load-bearing ordering partner and the only other
rule that both declares `position` context and consumes a `z-index` token.

Existing `#state-badge` (L463-470) — note the **missing** `z-index`:
```css
#state-badge {
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-pill);
  background: var(--color-surface-info);
  color: var(--color-text-info);
  font-size: var(--text-xs);
  font-weight: var(--fw-semibold);
}
```
Analog declaration to replicate (L485, inside `#stream-banner`):
```css
  z-index: var(--z-banner);
```
Restoration is one line inside the existing rule: `z-index: var(--z-badge);`. **Do not add
`position:`** — `#state-badge` is documented as deliberately *not* a `position: fixed` overlay
(L460-462); `z-index` on a non-positioned element is inert, but its presence is what gives
`--z-badge` a consumer and makes the `badge < banner` assertion (L151-153, TOKEN-07) have two
consumed ends. Other z-index consumers for reference: `.overlay` L418 (`var(--z-overlay)`),
`#selection-menu` L768 (`var(--z-selection-menu)`).

---

### `frontend/style.css` — `.overlay-card` (L421-427), R-2

**Analog:** `#chat-input-row input` (L629-637) is the only existing consumer of a shadow token;
`--shadow-composer` (L96) is the only existing shadow-token declaration.

Existing `.overlay-card` (L421-427) — note the **missing** `box-shadow`:
```css
.overlay-card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: var(--space-6) var(--space-8);
  max-width: 420px;
  text-align: center;
}
```
Analog consumer declaration (L635):
```css
  box-shadow: var(--shadow-composer);
```
Analog token declaration (L96) — the shape a new shadow token must match (a single flat
declaration inside the fence, `rgba(...)` allowed here and **only** here):
```css
  --shadow-composer: rgba(0, 0, 0, 0.04) 0 0 0 1px, rgba(0, 0, 0, 0.04) 0 2px 8px 0, rgba(0, 0, 0, 0.024) 0 4px 80px 8px;
```
New token + consumer (UI-SPEC R-2):
```css
  /* in the fence, beside --shadow-composer */
  --shadow-overlay: 0 8px 30px rgba(0, 0, 0, 0.2);
  /* in the .overlay-card rule */
  box-shadow: var(--shadow-overlay);
```
The token exists so that **no bare `rgba()` appears outside the fence** — the same reason
`--shadow-composer` exists. CHECK-01 counts only `#hex` outside the fence (L28), so `rgba` is not
its concern, but the fence is where the literal must live. The only other `box-shadow` in the
file (L798, `inset 3px 0 0 var(--color-action-warning)`) is a token-valued inset with no `rgba`
and is **not** a shadow-token analog.

---

### `frontend/style.css` — `.tier-desc` (L851), R-3

**Analog:** the sibling `:disabled` opacity sites (L840) are the ones that must be **left alone**;
R-3 is a pure deletion, so the pattern is "remove exactly the one declaration, touch nothing else."

Existing (L851) — delete only the trailing `opacity: 0.9;`:
```css
.tier-desc { font-size: var(--text-xs); font-weight: var(--fw-regular); opacity: 0.9; }
```
Result:
```css
.tier-desc { font-size: var(--text-xs); font-weight: var(--fw-regular); }
```
Do **not** touch `font-size`/`font-weight` (S-2 / C-1 territory) and do **not** touch the
`:disabled` `opacity: 0.5` at L840 or the archive dim at L703-704 — UI-SPEC `### opacity rulings`
marks all of those EXEMPT.

---

### `scripts/check-02-contrast.py` — the manifest parser / exit contract

**Analog:** itself. **Expected code delta: zero or near-zero** — the manifest it reads is
rewritten inside `style.css`, not here. This entry exists so the plan preserves the contract.

Contract that must survive (exact, from the file):
- fence reader asserts `starts == 1 and ends == 1`, else `sys.exit(1)` (L49-56).
- unknown token name → `print("FAIL: unknown token %s"); sys.exit(1)` (L79-81). This is why the
  manifest and the token block cannot drift.
- unparsable value → loud fail (L104).
- **coverage floor** (L146-155): `len(pairs) >= 24 and text_n >= 20 and nontext_n >= 4`, else
  exit 1. The new manifest is 43 pairs / 34 TEXT / 9 NON-TEXT — clears all three floors.
- raw-marker-count equality (L161-175): `fence.count("/* PAIR")` must equal the parsed count.
- closed-interval comparison (L198): `value >= threshold` — **4.496 fails, 4.504 passes**.
- alpha compositing (L185-188) uses the token's own alpha **and** the `@<alpha>` suffix.
- exit contract: `0` when `failures == 0` (`PASS: 0 failures`, L235), else `1`.
- The `VAR_RE` (L41) and `DECL_RE` (L27) both accept the new `--radix-*` names unchanged.

**Verification target:** `python3 scripts/check-02-contrast.py` must print `PASS: 0 failures` over
43 pairs + `ORDER 0.363`. If a code edit is proposed here, it must not weaken any of the six
guards above.

---

### `scripts/check-05-ui-uat.py` — assertions move to token-wiring form (D-14)

**Analog:** `item6` (L860-905) and `item_smoke` (L911-932). `item6` is the template the UI-SPEC
names; `item_smoke` is the second in-file exemplar of the same idea.

The two helpers that make token-wiring possible (already present, L250-262 and L239-240):
```python
def resolve_color(page, token):
    """把令牌解析成归一化的 computed rgb —— 挂一个探针元素读它的 color。"""
    return page.evaluate(
        """(t) => {
            const p = document.createElement('div');
            p.style.color = `var(${t})`;
            document.body.appendChild(p);
            const c = getComputedStyle(p).color;
            p.remove();
            return c;
        }""",
        token,
    )

def read_style(page, selector, prop):
    return page.evaluate(_READ_JS, [selector, prop])
```
The `item6` pattern to copy (L894-905) — resolve the token, read the consumer's computed value,
assert equality:
```python
    muted = resolve_color(page, "--color-text-muted")
    info("item6 --color-text-muted 解析值", muted)
    note_color = read_style(page, ".annotation-note", "color")
    body_color = read_style(page, ".annotation-answer-body", "color")
    if muted is None or note_color is None or body_color is None:
        blocked(item, "CR-06 用户批注以 --color-text-muted 渲染", muted, note_color,
                "元素缺失或令牌解析失败")
        ...
    ok(item, "CR-06 用户批注 .annotation-note color", muted, note_color)
    ok(item, "CR-06 AI 回应正文 .annotation-answer-body color", muted, body_color)
```
The `item_smoke` variant (L920-926) — the same wiring, with the token name in the label:
```python
    color_token = resolve_color(page, "--color-text-info")
    bg_token = resolve_color(page, "--color-surface-info")
    ok(item, "smoke #state-badge color == var(--color-text-info)",
       color_token, read_style(page, "#state-badge", "color"))
    ok(item, "smoke #state-badge background == var(--color-surface-info)",
       bg_token, read_style(page, "#state-badge", "background-color"))
```
**The hardcoded literals to replace** are the `ok(item, ..., "rgb(r,g,b)", read_style(...))` calls
in `item3` (L566-632), `item4` (L670, L707), `item5` (L733-747) and the module constant
`FROZEN_AMBER = "rgb(138, 101, 8)"` (L445) plus its three uses in `check_frozen_marker`
(L484, L501, L507). Each becomes `resolve_color(page, "--<token>")` for the expected side.

Notes on the rewrite:
- `ok()` normalises rgb whitespace before comparing (L111, L117-121), so `rgb(106,106,106)` and
  `rgb(106, 106, 106)` already compare equal — the change is about **which side is dynamic**, not
  about whitespace.
- `ok_contains` (L128-139) is the form for substrings such as the box-shadow check at L573-574;
  keep it, but source the needle from `resolve_color`/a token where possible.
- `read_style`/`resolve_color` return `None` for a missing selector; `ok()` turns `None` into
  `BLOCKED`, never a pass (L109-110) — preserve that.
- D-13: the `#doc-pane` expectation string becomes `#doc-panel-body` (padding 32px/40px already
  matches; only the name was wrong). This is a label/selector-string fix, not an id change.
- D-12: the 7 spacing/font-size drifts are accepted at HEAD — update the **expected** strings
  (`.panel-header` padding `6px 10px`, the five font sizes), do not change the CSS.

---

## Shared Patterns

### The fence is the single source of truth — two guards read it
**Source:** `frontend/style.css:5` / `:224`
**Apply to:** every edit in this phase.
Two independent scripts assert the fence delimiter pair is exactly 1 START / 1 END:
`scripts/check-01-token-conformance.sh:17-20` and `scripts/check-02-contrast.py:49-56`. Both
`exit 1` on mismatch. Never reword the markers; never add a second `:root` block.

### Tier-1 privacy — and a guard that will go vacuous (FLAG for the planner)
**Source:** `scripts/check-01-token-conformance.sh:37-39`
**Apply to:** the D-03 rename to `--radix-<family>-<step>`.
The guard's regex is:
```bash
prim=$(printf '%s\n' "$outside" \
  | grep -oE 'var\(--(white|black|gray|green|blue|amber|red|purple)(-[0-9]+)?' \
  | wc -l | tr -d ' ' || true)
```
After D-03 the tier-1 names are `--radix-gray-11`, `--radix-blue-11`, … — the pattern requires
`var(--` immediately followed by `gray`/`blue`/…, which `var(--radix-gray-11` does **not** match.
**Consequence:** TOKEN-02 ("tier-1 names must never appear outside the fence", restated in
UI-SPEC `### Tier 1`) becomes unenforced for the new names, and CHECK-01 would still print
`PASS`. This is a guard that silently stops guarding — the exact failure class the file's own
comments (L8-16) were written to prevent. `scripts/` is not in CONTEXT's named two-script change
set, so the plan must **either** widen the alternation to include `radix` **or** record explicitly
why it does not. The bare-hex half of CHECK-01 (L27-33) is unaffected and still holds.

### Contrast is arbitrated, never asserted
**Source:** `scripts/check-02-contrast.py` (whole file)
**Apply to:** every Radix hex transcribed into the fence.
No ratio in the UI-SPEC is evidence on its own; the checker recomputes from the fence. A wrong
transcribed digit surfaces as a failing pair, never as a silent pass (UI-SPEC carry-forward #4).
Radix's own AA documentation is deliberately not adopted.

### Manifest and tokens travel in one diff
**Source:** `frontend/style.css:159-222` (manifest) alongside `:8-157` (declarations)
**Apply to:** the manifest rewrite (V-11).
The manifest names tokens, never hex (L166), and lives inside the same fence so drift is visible
in review. `check-02-contrast.py:161-175` makes a malformed entry a hard failure.

### Declarations are restored/deleted individually, outside the fence
**Source:** `#stream-banner` L485, `#chat-input-row input` L635
**Apply to:** R-1, R-2, R-3.
Each out-of-fence change is a **single declaration** added to or removed from an existing rule —
no rule is reordered, no selector is added or removed (Hard Rule 3: 追加不重排). R-2 additionally
requires the token to be declared in the fence, because a bare `rgba()` may not live outside it.

---

## No Analog Found

| File | Role | Data Flow | Reason |
|---|---|---|---|
| — | — | — | None. Every file in scope has an in-file analog; no new file is created in this phase (D-01: zero new files). |

---

## Metadata

**Analog search scope:** `frontend/` (style.css, app.js, index.html, vendor/), `scripts/`
(check-01…check-05, ui-states/). Confirmed absent: `components.json`, `tailwind.config.*`,
`postcss.config.*`, any `.scss`/`.ts`/`.jsx` source.
**Files scanned:** 6 tracked source files + directory listings for `frontend/vendor/`.
**Tracking verified:** all cited paths pass `git ls-files`; `frontend/vendor/` contains exactly
`marked.min.js`.
**Baselines (re-measured 2026-09-19):** `frontend/style.css` = 933 lines; fence `:root` at
L5-224; tier-1 = 26 primitives (L8-33), tier-2 = 49 `--color-*` (L36-103); 34 `/* PAIR */` +
1 `/* ORDER */` markers (L169-222); `scripts/check-05-ui-uat.py` = 1041 lines;
`scripts/check-02-contrast.py` = 239 lines.
**Pattern extraction date:** 2026-09-19
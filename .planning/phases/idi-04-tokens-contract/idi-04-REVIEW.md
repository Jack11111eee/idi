---
phase: idi-04-tokens-contract
reviewed: 2026-09-17T15:16:26Z
depth: standard
files_reviewed: 5
files_reviewed_list:
  - frontend/style.css
  - scripts/check-01-token-conformance.sh
  - scripts/check-02-contrast.py
  - scripts/check-03-hidden-uniqueness.sh
  - scripts/check-04-important-count.sh
findings:
  critical: 6
  warning: 4
  info: 5
  total: 15
status: issues_found
---

# Phase idi-04: Code Review Report

**Reviewed:** 2026-09-17T15:16:26Z
**Depth:** standard
**Files Reviewed:** 5
**Status:** issues_found

## Summary

The `style.css` migration itself is in good shape. I re-derived the phase's headline claims
from the working tree and they hold: **106 tokens** in the fence (25 tier-1 primitives, 50
tier-2 including the two shadows, 31 non-colour); **0 bare `#hex` outside the fence**; 0
`font-size: <n>px`, 0 `border-radius: <n>px`, 0 `z-index: <n>`, 0 `12.5px`, 0 `@media`; the
orphan scan returns `--green-800` alone; Gate 2 (`consumed − declared`) is empty; `app.js`,
`index.html` and `frontend/vendor/` (exactly `marked.min.js`) are untouched. `#confirm-error`
is indeed `class="hint hidden"` at `index.html:168` and keeps its 1-0-0 ID selector, so it
still beats `.hint`. Every substitution I traced matches the Deliberate Delta Ledger — I found
no colour, spacing, radius or type value change that the ledger does not enumerate, and no
`var()` substitution changes specificity or source order.

**The four guard commands are where this phase actually fails.** All four are green on HEAD,
but three of them can report PASS while the condition they exist to detect is present, and the
contrast checker has three independent silent-pass paths. I proved each of the following by
mutation, not by reading:

| Guard | Mutation | Guard says |
|---|---|---|
| CHECK-01 | delete `frontend/style.css` | **PASS, exit 0** |
| CHECK-01 | remove the `DESIGN TOKENS: END` comment | **PASS** with a bare `#ff00ff` in the file |
| CHECK-02 | empty `style.css` / empty manifest | **`PASS: 0 failures`, exit 0** |
| CHECK-02 | misspell `ON` → `on`, or `TEXT` → `TEXTX`, or delete a non-ORDER pair line | **`PASS: 0 failures`, exit 0** |
| CHECK-02 | declare `--color-overlay-backdrop` (rgba, α 0.45) as a pair | reports **21.00**, real value **3.36** |
| CHECK-03 | add an indented second `.hidden { … }` | **PASS** with two rules present |
| CHECK-04 | one line carrying two `!important` declarations | **PASS** with two declarations present |

A guard that cannot fail is not a guard, and this phase's central claim is that the contract is
*executable* rather than asserted. Separately, the `.annotation-answered` rewrite silently
drops `.annotation-answer-body`, producing an undisclosed rendering change on the product's
core annotation surface.

---

## Narrative Findings (AI reviewer)

### Critical Issues

#### CR-01: CHECK-01 reports PASS when `frontend/style.css` is missing or unreadable

**File:** `scripts/check-01-token-conformance.sh:10-16`

**Issue:** The count is taken through a pipeline whose failure mode produces a *passing* value:

```bash
n=$(awk '…' frontend/style.css | grep -c '#[0-9a-fA-F]\{3,6\}' || true)
if [ "$n" = "0" ]; then echo "PASS"; exit 0; fi
```

When `awk` cannot open the file it writes the diagnostic to **stderr** and emits **no stdout**.
`grep -c` therefore reads empty input, prints `0`, and exits 1; the `|| true` — added to handle
exactly the "grep -c exits 1 on a zero count" case documented at L9 — swallows that status too.
`n` is `"0"` and the guard prints `PASS` with exit 0. Proven on a repo copy with the file absent
and again with it present but `chmod 000`:

```
$ bash scripts/check-01-token-conformance.sh      # frontend/style.css missing
awk: can't open file frontend/style.css
 source line number 1
PASS
exit=0
```

CHECK-03 and CHECK-04 do **not** have this bug (their `n` is empty, which is `!= "1"`, so they
FAIL loudly). CHECK-01 is the outlier, and it is the guard that certifies the phase's headline
claim.

**Fix:** Assert the input before counting, and do not let a pipeline status masquerade as a
count:

```bash
[ -f frontend/style.css ] || { echo "FAIL: frontend/style.css not found"; exit 1; }

hex=$(awk '/===== DESIGN TOKENS: START/{f=1} /===== DESIGN TOKENS: END/{f=0} !f' frontend/style.css \
  | grep -o '#[0-9a-fA-F]\{3,6\}' | wc -l | tr -d ' ')
```

(`grep -o | wc -l` also fixes the line-vs-occurrence mismatch with the message text — see IN-03.)

---

#### CR-02: CHECK-01 and CHECK-02 go vacuous if the `END` fence marker is removed

**File:** `scripts/check-01-token-conformance.sh:10`, `scripts/check-02-contrast.py:44-59`

**Issue:** Both parsers define the fence solely by the presence of a marker line; neither
asserts that the marker exists, nor that it appears exactly once. Remove or rename the
`/* ===== DESIGN TOKENS: END ===== */` comment and `f` (awk) / `inside` (Python) stays `1` /
`True` to EOF — the entire remainder of the stylesheet is treated as "inside the fence".
CHECK-01 then reports PASS for a file containing a bare hex:

```
$ sed -i '' 's|/\* ===== DESIGN TOKENS: END ===== \*/|/* fence marker gone */|' /tmp/t2.css
$ printf '\n.bogus { color: #ff00ff; }\n' >> /tmp/t2.css
$ awk '/START/{f=1} /END/{f=0} !f' /tmp/t2.css | grep -c '#[0-9a-fA-F]\{3,6\}'
0                      # ← PASS, with #ff00ff in the file
```

CHECK-02 is unaffected numerically (it re-reads the same declarations), so **both guards stay
green simultaneously** — there is no cross-check that catches the drift.

Note this is *not* the attack surface the phase context anticipated. Neither parser matches
braces at all, so nested braces, `{`/`}` inside comments, strings and `@media` are all
irrelevant. The real fragility is that the fence is a pair of free-text line markers with no
cardinality assertion.

**Fix:** In CHECK-01, before counting:

```bash
starts=$(grep -c '===== DESIGN TOKENS: START' frontend/style.css)
ends=$(grep -c '===== DESIGN TOKENS: END' frontend/style.css)
[ "$starts" = "1" ] && [ "$ends" = "1" ] \
  || { echo "FAIL: expected exactly 1 fence START and 1 fence END, found $starts/$ends"; exit 1; }
```

Mirror the same assertion in `check-02-contrast.py:read_fence` (raise/`sys.exit(1)` when the
marker count is not exactly 1) so the two parsers cannot disagree about where the fence ends.

---

#### CR-03: CHECK-02 prints `PASS: 0 failures` for an empty file or an empty manifest

**File:** `scripts/check-02-contrast.py:126-185`

**Issue:** `main()` counts failures over whatever `PAIR_RE.finditer` happens to match and
exits 0 when `failures == 0`. With zero matches that is trivially true. Proven:

```
$ : > frontend/style.css
$ python3 scripts/check-02-contrast.py
PASS: 0 failures
exit=0

$ printf '/* ===== DESIGN TOKENS: START ===== */\n:root { }\n/* ===== DESIGN TOKENS: END ===== */\n' > frontend/style.css
$ python3 scripts/check-02-contrast.py
PASS: 0 failures
exit=0
```

There is no lower bound on the pair count anywhere in the script. The SUMMARY (coverage C2)
claims floors of `>= 24 / >= 20 / >= 4` — those floors exist only in the prose; nothing in
`check-02-contrast.py` enforces them.

**Fix:** After parsing, assert coverage before evaluating:

```python
pairs = list(PAIR_RE.finditer(fence))
text_n = sum(1 for m in pairs if m.group(3) == "TEXT")
nontext_n = len(pairs) - text_n
if len(pairs) < 24 or text_n < 20 or nontext_n < 4:
    print("FAIL: manifest coverage %d pairs (%d TEXT / %d NON-TEXT) below floor 24/20/4"
          % (len(pairs), text_n, nontext_n))
    sys.exit(1)
```

---

#### CR-04: CHECK-02 silently drops a manifest entry it cannot parse

**File:** `scripts/check-02-contrast.py:28-35`, `134`, `156`

**Issue:** The module docstring states (L10-12): *"A manifest entry naming a token that is not
declared in the fence (or an ordering entry naming a pair that is not listed) is a
contract-drift signal and fails loudly; it is never silently skipped."* That is true only for
entries that **match** `PAIR_RE`. An entry that fails to parse is not reported at all — the
`finditer` simply produces nothing for it. Three proven variants, all yielding
`PASS: 0 failures`, exit 0:

```
/* PAIR --color-action-danger on --white TEXT */     # lowercase "on"
/* PAIR --color-action-danger ON --white TEXTX */    # typo in the kind
                                                     # (or: delete the line entirely)
```

Deleting a non-ORDER pair line outright is the most damaging case: it is undetectable for 33 of
the 34 pairs. Only the two `ORDER` operands are protected, because `ORDER_RE` re-checks them
(L158-162). The checker's own stated anti-rot property — "the manifest and the token block
cannot drift apart" — therefore does not hold in the direction that matters.

**Fix:** Reconcile the raw marker count against the parsed count:

```python
raw = fence.count("/* PAIR")
parsed = len(PAIR_RE.findall(fence))
if raw != parsed:
    print("FAIL: %d '/* PAIR' markers but only %d parsed — malformed manifest entry" % (raw, parsed))
    sys.exit(1)
```

(and the same for `/* ORDER`). This turns every dropped entry into a loud failure.

---

#### CR-05: CHECK-02 measures an alpha-bearing token as fully opaque → false PASS

**File:** `scripts/check-02-contrast.py:67-95`, `106-112`, `115-117`

**Issue:** `resolve()` returns `(r, g, b, a)`, but `relative_luminance()` reads only `rgb[:3]`
(L107) and the alpha is consulted *only* when a manifest entry carries an explicit `@<alpha>`
suffix. A token whose own declared value carries alpha is therefore measured at full opacity.
`--color-overlay-backdrop: rgba(0, 0, 0, 0.45)` is exactly such a token:

```
overlay measured opaque : 21.0        # what the checker would report
overlay truly composited: (140, 140, 140) -> 3.36
```

Because 3.36 < 4.5, declaring that token as a `TEXT` pair produces a **false PASS** on a pair
that genuinely fails:

```
$ # added: /* PAIR --color-overlay-backdrop ON --white TEXT */
PASS  21.00  --color-overlay-backdrop on --white
exit=0
```

The current manifest does not name it, so HEAD is not wrong — but the checker advertises alpha
handling and silently does the wrong thing for the one token in the file that carries alpha.

**Fix:** Composite the foreground over the background using the *foreground's own* alpha when
it is below 1, and reject the combination rather than ignoring it:

```python
fg = resolve(fg_name, decls)
bg = resolve(bg_name, decls)
fg_alpha = fg[3]
if alpha is not None:
    fg_alpha *= float(alpha)
if fg_alpha < 1.0:
    fg = composite(fg, bg, fg_alpha)
```

---

#### CR-06: `.annotation-answered` rewrite drops `.annotation-answer-body` — undisclosed rendering change

**File:** `frontend/style.css:849-854` (and the removed rule, `frontend/style.css` pre-migration L456)

**Issue:** The migration deleted `.annotation-answered { opacity: 0.65 }` and re-expressed the
dimming as a 0-2-0 descendant rule:

```css
.annotation-answered .annotation-note,
.annotation-answered .annotation-quote,
.annotation-answered .annotation-answer summary { color: var(--color-text-muted); }
```

`.annotation-answer-body` is **not** in that list, and no other rule colours it for non-plain
items (`.annotation-plain .annotation-answer-body` at L669 requires `.annotation-plain`).
`frontend/app.js` renders that element on exactly this path — `renderAnnotations` sets
`li.className = '… annotation-answered'` for `item.status === 'answered'` (`app.js:1121`) and
independently appends `body.className = 'annotation-answer-body'` whenever `item.answer` is
non-empty (`app.js:1147`). So for the ordinary "user annotates → AI answers → answered" item,
the answer body now inherits `--color-text` (#1a1a1a, 16.67:1) while the user's own note is
muted (#6a6a6a, 5.18:1).

Measured delta at that site: ~5.1:1 (the old 0.65 composite of `#1a1a1a` on white) → 16.67:1.
The intra-item hierarchy inverts — the AI's answer becomes the loudest text in an item that is
supposed to read as 已回应. The CSS comment at L849 states the rule's purpose as
「已回应条目:文字弱化」, and the UI-SPEC's D-11 states the mechanism as "apply
`--color-text-muted` to the text inside"; the implementation covers three of the four text
carriers. This is not on the Deliberate Delta Ledger, whose own rule is "Anything not on this
list is a regression."

**Fix:** Add the missing selector (one line):

```css
.annotation-answered .annotation-note,
.annotation-answered .annotation-quote,
.annotation-answered .annotation-answer-body,
.annotation-answered .annotation-answer summary { color: var(--color-text-muted); }
```

---

### Warnings

#### WR-01: CHECK-03's pattern is anchored to column 0, so an indented duplicate is invisible

**File:** `scripts/check-03-hidden-uniqueness.sh:8`

**Issue:** `grep -c '^\.hidden {'` only counts a `.hidden {` that begins at column 0. The
guard's stated purpose is "exactly one global `.hidden {` rule". A second rule that is indented
— the natural formatting for any rule nested inside a future `@media` or `@layer`, both of
which the UI-SPEC anticipates in later phases — is not counted. Proven:

```
$ printf '\n  .hidden { display: block; }\n' >> style.css
$ grep -c '^\.hidden {' style.css
1                      # ← CHECK-03 PASSES with two .hidden rules present
```

The phase context's own phrasing ("a 5-way single point of failure") is the reason this matters:
`.hidden` is a mechanism, and a duplicate that wins the cascade would silently un-hide
`#draft-empty` / `#rounds-hint` / `#btn-process-round` / `#round-switcher` / `#writing-hint`.

**Fix:** Match the selector anywhere on a line and tolerate whitespace/brace placement:

```bash
n=$(grep -cE '^[[:space:]]*\.hidden[[:space:]]*\{' frontend/style.css || true)
```

---

#### WR-02: CHECK-04 counts matching lines, not `!important` declarations

**File:** `scripts/check-04-important-count.sh:9-11`

**Issue:** The script's own header and its FAIL message both say "declaration count", and
`docs`/SUMMARY justify the `;` in the pattern as the way to exclude the two comment-prose hits.
But `grep -c` counts **lines**, so N declarations on one line count as 1. Proven:

```
$ # single .hidden line rewritten to carry two !important declarations
$ grep -c '!important;' style.css
1                      # ← CHECK-04 PASSES, but the file now has 2 declarations
$ grep -o '!important;' style.css | wc -l
2
```

The guard also still fails on comment prose that happens to contain `!important;` (a false FAIL,
the safe direction, but noise the `;` trick was supposed to remove).

**Fix:** Count occurrences, not lines:

```bash
n=$(grep -o '!important;' frontend/style.css | wc -l | tr -d ' ')
```

---

#### WR-03: The "hard invariant" has no mechanical gate, contrary to the contract

**File:** `scripts/check-01-token-conformance.sh:1-18`; claim at `04-UI-SPEC.md:63-65`

**Issue:** The UI-SPEC states the phase's hard invariant — *"tier-1 primitive names must never
appear outside the `:root` block. This is mechanically checkable and **becomes part of
CHECK-01**"* — and the phase context repeats it as a hard invariant. CHECK-01 as implemented
counts only `#[0-9a-fA-F]{3,6}`; its sole mention of "primitives" is the prose comment at L8.
A selector that reaches for a primitive name passes **every** gate in the phase. Proven by
appending `.primitive-leak { color: var(--gray-700); background: var(--amber-300); }` to a copy:

```
CHECK-01          -> 0 bare hex  => PASS
Gate 2 (consumed − declared)      => empty (both names are declared)
reverse orphan scan               => --green-800 only, unchanged
```

The invariant does hold on HEAD (I verified: no `--gray-*` / `--white` / `--black` /
`--amber-*` / `--green-*` / `--blue-*` / `--red-*` / `--purple-*` reference appears outside the
fence), so this is a verification gap, not a live defect — but the claim that CHECK-01 covers it
is false.

**Fix:** Extend CHECK-01 to also count primitive references outside the fence:

```bash
prim=$(awk '/===== DESIGN TOKENS: START/{f=1} /===== DESIGN TOKENS: END/{f=0} !f' frontend/style.css \
  | grep -oE 'var\(--(white|black|gray|green|blue|amber|red|purple)-[0-9]+' | wc -l | tr -d ' ')
[ "$prim" = "0" ] || { echo "FAIL: $prim tier-1 primitive reference(s) outside the fence"; exit 1; }
```

---

#### WR-04: The manifest's `--black ON --white TEXT@0.8` pair is stale — it models a value the site no longer uses

**File:** `frontend/style.css:194-195`

**Issue:** The comment above these entries claims *"the two surviving whole-subtree dims —
covered, and both pass"*. The `@0.75` entry (`--color-text ON --gray-25`) correctly models
`#rounds-placeholder.archive-mode #round-doc` (L844). The `@0.8` entry models `.tier-desc`
(L778), which is a `<span>` inside `<button id="btn-tier-loose">` (`index.html:182-183`) and
therefore inherits its foreground from the button. **N-4 landed in plan 02 (`4f323c0`) and the
manifest was written in plan 03 (`1759016`)** — so at manifest-authoring time the button
foreground was already `var(--color-text)` (#1a1a1a), not `#000000`:

```
MANIFEST entry models --black@0.8 on white : 12.63   (what the checker prints)
REAL tier-desc: --color-text@0.8 on white  :  9.15   (what renders)
```

Both clear 4.5, so this is not a false PASS — but the manifest is asserted to name the tokens
that are actually in play, and this entry names one (`--black`) that has no consumer as a
foreground anywhere in the file. It is exactly the class of drift the checker's design claims to
prevent.

**Fix:**

```css
/* PAIR --color-text ON --color-surface TEXT@0.8 */
```

---

### Info

#### IN-01: `--color-text-muted ON --gray-100` is not a ground the token lands on

**File:** `frontend/style.css:155-159`

**Issue:** The comment says "the four grounds `--color-text-muted` actually lands on (note
N-1)". `--gray-100` (`#eeeeee`) is `--color-surface-hover` (`button:hover`) and
`--color-border-subtle`; the muted-text sites sit on `--gray-25` (`.hint` in `#doc-pane`),
`--white` (`.annotation-plain`, `.annotation-answer summary`), `--gray-50`
(`--color-surface-sunken`: `.badge-answered`, `.chat-ai`, `.markdown-body code`) and
`--amber-25` (`.verdict-suggestion`, via `.verdict-card`). No element renders muted text on
`#eeeeee`. The entry is harmless (4.66 is the tightest of the four, so it over-constrains
rather than under-constrains), but the comment overstates it.

**Fix:** Either drop the `--gray-100` pair, or reword the comment to "the four grounds the muted
rank must clear" rather than "actually lands on".

---

#### IN-02: Two manifest entries emit byte-identical log lines

**File:** `frontend/style.css:189` and `frontend/style.css:205`

**Issue:** `--color-action-warning ON --gray-25` is listed twice — once as `TEXT` (L189, amber
text on the page ground) and once as `NON-TEXT` (L205, the S-4 frozen-round marker). The label
built at `check-02-contrast.py:143-145` is `"%s on %s"`, which is identical for both, so stdout
shows two indistinguishable `PASS 5.10  --color-action-warning on --gray-25` lines and the
threshold actually applied (4.5 vs 3.0) is not visible.

**Fix:** Include the kind in the label: `label = "%s on %s %s" % (fg_name, bg_name, kind)`.

---

#### IN-03: CHECK-01's message reports lines but calls them hexes

**File:** `scripts/check-01-token-conformance.sh:11`, `17`

**Issue:** `grep -c` counts lines; the FAIL message reads `"FAIL: $n bare hex outside the token
block"`. The UI-SPEC and SUMMARY are explicit that the baseline was 117 *lines* / 120
*occurrences*, so the discrepancy is understood — but a file with two hexes on one line reports
"1 bare hex", which will mislead whoever reads the failure. Using `grep -o … | wc -l` (as in the
CR-01 fix) makes the message true and also matches TOKEN-04's occurrence-based wording.

---

#### IN-04: A failing ratio can print as `4.50 (need >= 4.5)`

**File:** `scripts/check-02-contrast.py:150`

**Issue:** The comparison is correctly closed-interval and unrounded (`4.496 >= 4.5` is `False`),
but the FAIL line renders the value with `%.2f`, so `4.496` prints as `4.50` next to
`(need >= 4.5)` — a log line that reads like a bug in the checker. Widen the display precision
(`%.3f`) so a boundary failure is legible.

---

#### IN-05: CHECK-02 exits via an uncaught traceback when the stylesheet is missing

**File:** `scripts/check-02-contrast.py:46`

**Issue:** `open(CSS_PATH)` on a missing file raises `FileNotFoundError`; the process exits 1
(correct direction, so this is not a false PASS) but with a raw traceback rather than the
command's own `FAIL:` line, unlike the other three guards which print a readable message.
Wrapping `read_fence` in a `try/except OSError` with `print("FAIL: cannot read %s" % path);
sys.exit(1)` keeps the four commands' output contract uniform.

---

_Reviewed: 2026-09-17T15:16:26Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
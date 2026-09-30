---
phase: idi-10-tables-and-radius-scale
reviewed: 2026-09-27T13:33:35Z
depth: standard
files_reviewed: 2
files_reviewed_list:
  - frontend/style.css
  - scripts/check-10-idi10-validation.py
findings:
  critical: 1
  warning: 5
  info: 7
  total: 13
status: issues_found
---

# Phase idi-10: Code Review Report

**Reviewed:** 2026-09-27T13:33:35Z
**Depth:** standard
**Files Reviewed:** 2
**Status:** issues_found

## Summary

The **product change is correct**. The diff against `1a5ec558^` is exactly what the phase description
claims and nothing else: the table rule is rewritten in place (`border: 1px solid var(--color-border)` →
`border: none` + `border-bottom: 1px solid var(--color-border-subtle)`), `.markdown-body th
{ background: var(--color-surface); }` is appended immediately after it, `--radius-lg: 28px;` is deleted
from the token fence, and its two consumers go to different steps (`.chat-user` → `--radius-md`,
`#chat-input-row input` → `--radius-pill`). Source order inside both radius rules is correct (the
`border-bottom-right-radius` longhand still follows the shorthand), no later rule targets `th` or
`border-radius` on those two selectors, and `--radius-lg` has zero residual occurrences anywhere in the
file (verified by grep; the fence comment correctly avoids naming the deleted token, which would have
broken the two `grep == 0` criteria).

The `t1` / `t2` assertion sets are **not** vacuous for the table change: reverting either half of the
change (dropping the `th` background, or restoring `border: 1px solid`) turns the item red — the
header background is pinned to a literal (`TH_BG_LITERAL`, `check-10:101`) and the left/right/top
widths are pinned to `0px`. The runtime evidence is genuine: the `after` snapshot's `style_css_sha256`
(`4e783086…5783e8`) matches the current `frontend/style.css` byte-for-byte, and the two element PNGs are
in fact byte-identical (`sha256 190d7d7d…4a35`), so the "zero visual change" claim for
`#chat-input-row input` is supported by measurement, not by the arithmetic the CSS comment disclaims.

The defects are all in the **instrument**, and they are of two kinds: (1) a failure-honesty hole that
reports a hard regression of this phase's own requirement as `BLOCKED`/`exit=2` — the code this project
documents as the *expected* code; and (2) several assertions that are weaker than their own labels and
notes claim, plus coverage gaps at the table level. Details below.

## Critical Issues

### CR-01: A destroyed radius scale is reported as `BLOCKED` (exit 2), not `FAIL` (exit 1) — and with a wrong reason

**File:** `scripts/check-10-idi10-validation.py:402-410`, `:450-460`, `:471-500` (mechanism in the shared helper at `scripts/check-05-ui-uat.py:215-222`)

**Issue:** `r1` / `r2` are the *only* assertions in the whole gate that pin the three surviving radius
tokens to their declared scale literals, and `RADIUS-01`'s requirement is precisely that the scale stays
`8 / 10 / 胶囊`. Both items feed the tokens straight into `ok()` as an **expected** value:

```python
tokens = {name: resolve_token(page, name) for name in RADIUS_LITERALS}
for name, literal in RADIUS_LITERALS.items():
    ok(item, f"r1 [令牌] {name} 解析值 == 刻度声明字面量", literal, tokens[name], ...)
```

`resolve_token` returns `None` for an undeclared custom property. Delete `--radius-md: 10px;` from the
`:root` fence — the exact regression this phase guards — and:

- the three token-literal assertions (`:404-406`) take `ok()`'s `actual is None` branch
  (`check-05:217-218`) → **BLOCKED**, with the printed reason 「元素/选择器不存在」 ("element/selector
  does not exist"), which points the fixer at the DOM instead of at the token fence;
- the corner assertions (`:452-460`) take the `expected is None` branch → BLOCKED;
- everything else in `r1` still **PASSES** — the fence check (`:392-396`) counts only `--radius-lg`, and
  the "四角并非统一" inequality still holds because `border-bottom-right-radius: var(--radius-sm)` is a
  separate, still-valid longhand.

`item_verdict("r1")` therefore returns `"blocked"`, `any_fail` is `False`, and `main()` exits **2**
(`:726-728`). `ROADMAP.md`'s Gates section documents exit 2 as the benign code for this project
(「全量 exit=2 是 item 5 两条 `--ai-smoke` 腿按设计 BLOCKED」), so the gate reports *"the radius scale was
destroyed"* in the same channel as *"an optional AI smoke leg was unavailable"*. `r2` has the identical
shape for `--radius-pill`. This is the one failure mode the reviewer brief asks about explicitly, and it
is the one the script gets wrong — notably in the same file whose author already recognised the trap for
`.chat-user` (`:439-446`: "BLOCKED 不适用 … 这是 FAIL 而不是 BLOCKED") and did not apply the same
reasoning to token resolution.

*Mitigation, stated for honesty:* the plan designates `check-09-idi09-validation.py --item c1 --item c2`
as the "不得删 `--radius-md`" detector, so this regression is caught elsewhere. That does not remove the
defect — within `check-10`'s own verdict, a hard FAIL is downgraded to a BLOCKED.

**Fix:** make the token expectations hard assertions, and stop routing them through `ok()`'s
`actual is None` branch:

```python
for name, literal in RADIUS_LITERALS.items():
    ok_true(item, f"r1 [令牌] {name} 解析值 == 刻度声明字面量", tokens[name] == literal,
            literal, str(tokens[name]),
            note="令牌缺失(None)是硬失败,不是 BLOCKED —— 本阶段的核心要求就是这三档存在且值不变")
md, sm = resolve_token(page, "--radius-md"), resolve_token(page, "--radius-sm")
ok_true(item, "r1 [令牌] --radius-md / --radius-sm 均可解析", md is not None and sm is not None,
        "两者非 None", f"md={md} sm={sm}")
```

and the same treatment for `r2`'s `pill`. (`r1`'s `gone is None` check at `:407-410` is already the
right shape — mirror it.)

## Warnings

### WR-01: The `shot` sample-list assertion is tautological — it compares a list to itself

**File:** `scripts/check-10-idi10-validation.py:529-530`

**Issue:**

```python
made = []
for state in c05.STATES:
    ...
    made.append(state)
ok(item, "shot 样本清单逐项一一对应(无缺项、无多余样本)", list(c05.STATES), made, ...)
```

`made` is built by iterating `c05.STATES`, so the two operands are equal by construction whenever the
loop completes; if a state's fixture were missing, `c05.make_fixture` raises `SystemExit` and aborts the
whole run rather than failing this assertion. The "无缺项" intent is not guarded by this line (it is
partially covered by the per-state `ok_true` at `:527-528`).

**Fix:** delete the line, or make it compare against a literal expectation that does not derive from the
loop, e.g. assert `made == ["p1", "p12", "p3", "checking", "archive"]` — or, better, assert
`set(made) == set(c05.STATES) and len(made) == len(set(made))` outside the loop.

### WR-02: The `border-bottom-color` assertions are wiring-only; their own note claims a value-level fact that is not enforced

**File:** `scripts/check-10-idi10-validation.py:328-330` and `:368-370`

**Issue:** Both sides of these assertions are resolved from the same token:

```python
ok(item, f"{pair} .markdown-body th 计算 border-bottom-color == var(--color-border-subtle)",
   tokens["subtle"], read_style(page, f"{host} th", "border-bottom-color"),
   note="表头下边线与行间分隔线同档,不再是原 --color-border(gray-7)的深线")
```

The note asserts a *step* fact ("no longer the deeper gray-7 line"). If `--color-border-subtle` were
changed to `var(--radix-gray-7)` — making it identical to the token the phase deliberately moved away
from — both sides move together and all four assertions still pass. The `ok_true` guard at `:315-318`
compares `--color-border-subtle` against `--color-surface`, not against `--color-border`, so it does not
close the hole either. This directly contradicts the script's own stated discipline
(`:99-101`): "若两侧都从同一个令牌解析,令牌被改坏(而消费者仍接着线)也照样 PASS" — a principle that *is*
applied to `TH_BG_LITERAL`, `TH_TD_PADDING` and `RADIUS_LITERALS`, and is skipped only here (and for
`--text-base` in the two font-size control groups, where the note 「改它就红」 is likewise only true of
the declaration, not of the token value — `check-05:1122/1126` resolves `--text-base` too).

**Fix:** pin the separator to the gray-6 literal, as the header background already is:

```python
BORDER_SUBTLE_LITERAL = "rgb(217, 217, 217)"   # --radix-gray-6
...
ok(item, f"{pair} .markdown-body th 计算 border-bottom-color == gray-6 字面量",
   BORDER_SUBTLE_LITERAL, read_style(page, f"{host} th", "border-bottom-color"),
   note="分隔线档位是值级判据:两侧都写死,防「令牌被改成 gray-7 而消费者仍接线」时假绿")
```

and add `ok_true(..., resolve_color(page, "--color-border-subtle") != resolve_color(page, "--color-border"))`.

### WR-03: `r1` / `r2` have no rendered-evidence guard, although `r1`'s claim is explicitly about appearance

**File:** `scripts/check-10-idi10-validation.py:385-465`, `:471-508` (contrast with `:279-293`)

**Issue:** `t1` / `t2` were (correctly) given an aggregate assertion that at least one `(sample, host)`
pair sits in a rendered subtree, precisely so that a `display:none` subtree cannot supply the evidence.
`r1` and `r2` have no equivalent: `r1` creates its `.chat-user` probe with the app's own
`appendChatMessage` and then reads it without ever checking that the element is in a rendered subtree,
even though `r1`'s central claim is 「本阶段**唯一外观真变**的消费者」 — an appearance claim. Today the
`p1` fixture does render `#session-panel`, so the readings are real; but a future change that hides the
session panel in `p1` would leave `r1` green on cascade-only evidence while its own label still asserts a
visual change.

**Fix:** reuse the display walk from `_PROBE_JS` for the probe bubble and assert `rendered is True` with
`ok_true`, or call a shared `render_evidence_assertion`-style helper for `r1` / `r2`.

### WR-04: Table-level properties are unasserted, so "no outer frame" and "no double lines" are unguarded

**File:** `scripts/check-10-idi10-validation.py:320-339` / `:359-376`; `frontend/style.css:1111`

**Issue:** Every table assertion reads a **cell** (`th` / `td`). Nothing reads the `<table>` element
itself, so:

- Adding `border: 1px solid var(--color-border)` (or any single-side border) to
  `.markdown-body table` — the most direct way to re-introduce the outer frame that `ROADMAP` SC1
  requires to be gone — leaves `t1` and `t2` fully green.
- Removing or changing `.markdown-body table { border-collapse: collapse; }` also leaves them green,
  even though the file's own comment declares that rule load-bearing for the "行间不与相邻行画双线"
  property (`style.css:1110`, restated in the gate's note at `:370`). With `border-collapse: separate`
  the UA's `border-spacing: 2px` re-appears and rows gain gaps; the cell reads do not change.
- `td`'s `background-color` is never asserted (only `th`'s), so a cell fill that would break
  「表头浅底」's implicit "only the header is shaded" is invisible to the gate.

No other gate covers any of this — `grep -rn "border-collapse" scripts/` matches only a note string in
this file, which is exactly the situation the file header (`:4-19`) was written to document.

**Fix:** add to each pair's assertion block:

```python
ok(item, f"{pair} .markdown-body table 计算 border-collapse == collapse", "collapse",
   read_style(page, f"{host} table", "border-collapse"),
   note="行间不画双线依赖这条既有折叠规则 —— 它此前零断言")
for side in ("top", "right", "bottom", "left"):
    ok(item, f"{pair} .markdown-body table 计算 border-{side}-width == 0px", "0px",
       read_style(page, f"{host} table", f"border-{side}-width"),
       note="外框必须消失(ROADMAP SC1);此前只断言了单元格,表格自身的边框是可达的回归路径")
ok(item, f"{pair} .markdown-body td 计算 background-color == transparent", "rgba(0, 0, 0, 0)",
   read_style(page, f"{host} td", "background-color"))
```

### WR-05: The "zero visual change" diff is not implemented in code, and the plan's allow-list is provably wrong

**File:** `scripts/check-10-idi10-validation.py:558-632` (and the criterion it defers to, `.planning/phases/idi-10-tables-and-radius-scale/idi-10-02-PLAN.md` Task 2 `<verify>`)

**Issue:** `radius_snapshot()` writes the computed dump, the rect, the element PNG and the source
sha256, but performs **no comparison at all**; nothing else in the repository consumes the artifacts
(`grep -rn "input-radius-before"` outside `radius-snapshots/` matches only the plan and the summary). The
「外观零变化」 claim for `#chat-input-row input` therefore rests entirely on a hand-typed command, and
that command is wrong. Running the plan's `<verify>` python one-liner verbatim against the committed
snapshots prints:

```
['--radius-lg', 'border-bottom-left-radius', 'border-bottom-right-radius',
 'border-end-end-radius', 'border-end-start-radius', 'border-start-end-radius',
 'border-start-start-radius', 'border-top-left-radius', 'border-top-right-radius']
rect_equal True
subset False corners True sha_changed True
```

`subset False` is the plan's own `<fails_when>` trigger (`"subset" is not True`). The diff set is **9**
keys, not the 8 the criterion names: deleting a custom property from `:root` also removes that property's
own inherited key from the element's computed-style dump (`599 → 598` keys; `--radius-lg` is the only
key present in `before` and absent in `after`). The deviation is registered in
`idi-10-02-SUMMARY.md`, but the plan's criterion was never corrected, so the phase's verification record
contains a command that fails as written — and the completeness/tightness of the allow-list is asserted
nowhere mechanically.

**Fix:** mechanize it in the script (the two labels are already both on disk), and/or correct the plan's
key set to 9:

```python
def radius_snapshot_diff(before_dir, after_dir):
    b = json.loads((before_dir / "input-radius-before.json").read_text(encoding="utf-8"))
    a = json.loads((after_dir / "input-radius-after.json").read_text(encoding="utf-8"))
    allowed = set(RADIUS_CORNER_PROPS) | {   # 4 physical + 4 logical aliases + the deleted token's own key
        "border-start-start-radius", "border-start-end-radius",
        "border-end-start-radius", "border-end-end-radius", "--radius-lg",
    }
    diff = {k for k in set(b["computed"]) | set(a["computed"])
            if b["computed"].get(k) != a["computed"].get(k)}
    ok_true("radius-snapshot", "键级 diff ⊆ 允许集合且四角全在",
            diff <= allowed and set(RADIUS_CORNER_PROPS) <= diff,
            f"⊆ {sorted(allowed)}", str(sorted(diff)))
    ok_true("radius-snapshot", "rect 前后逐值相同", b["rect"] == a["rect"], "相等", f"{b['rect']} vs {a['rect']}")
```

## Info

### IN-01: `--radius-snapshot before DIR` can silently overwrite pre-change evidence with post-change data

**File:** `scripts/check-10-idi10-validation.py:558-632`, `:665-669`

**Issue:** The label is validated only against the tuple `("before", "after")` (`:665-669`); nothing ties
it to the CSS state. Re-running `--radius-snapshot before …` at HEAD overwrites the genuine "before"
artifacts with post-change readings. The recorded `style_css_sha256` lets a human notice, but the gate
itself never fails — and the downstream plan check only compares the two shas for *inequality*, which a
double re-run would break in a way that looks like "the change was never made".
**Fix:** have `radius_snapshot` refuse to write a label whose recorded sha collides with an existing
sibling file of the other label, or assert `before_sha != after_sha` in the diff helper above.

### IN-02: `r2`'s "four corners equal" assertion can pass vacuously

**File:** `scripts/check-10-idi10-validation.py:498-500`

**Issue:** `ok_true(..., len(set(corners.values())) == 1, ...)`. If `#chat-input-row input` is missing,
all four reads are `None`, the set has one element, and this assertion PASSES. The item verdict is still
`blocked` because the sibling `ok()` calls read `None`, so no false green escapes today — but the
assertion is weaker than it reads.
**Fix:** `ok_true(..., len(set(corners.values())) == 1 and corners["border-top-left-radius"] is not None, ...)`.

### IN-03: Stale count in the `_SNAPSHOT_JS` header comment

**File:** `scripts/check-10-idi10-validation.py:539-542`

**Issue:** The comment says the iteration list holds 「恰 599 个长手名」. That is the **before** count;
after this phase's change it is 598, and the list's 121 custom-property entries are not longhands at all.
The script asserts only `len(computed) > 100` (`:598-600`), so nothing breaks — but a reader comparing
the comment to a fresh `after` snapshot will conclude the dump is wrong.
**Fix:** 「实测在收敛前 599 / 收敛后 598 个属性名(含 121 个从 `:root` 继承的自定义属性,不含
`border-radius` 简写)」.

### IN-04: `fence_text()` does not verify that END follows START

**File:** `scripts/check-10-idi10-validation.py:179-184`

**Issue:** `text[start:end]` is computed from two independent `str.index` calls. If the END marker ever
appeared before the START marker, the slice would be empty and `fenced.count("--radius-lg") == 0`
(`:392-396`) would pass vacuously — the one assertion in `r1` that reads source text rather than the
rendered cascade.
**Fix:** `assert end > start` (or slice from `start` to the first END occurrence after `start`).

### IN-05: `th` renders at the UA's `font-weight: bold` (700), outside this file's declared three weight ranks

**File:** `frontend/style.css:1112-1118`

**Issue:** The phase gave `th` a background surface but no weight, so the header inherits the HTML
rendering default `th { font-weight: bold }` — weight 700, which is exactly the "fourth weight rank" the
file's own comment calls a contract violation when it eliminated 700 from the embedded heading rules
(`style.css:1649`: 「字重 700 更是一个契约只声明三档(400 / 500 / 600)之外的**第四档**」). This is
pre-existing and strictly outside the phase's mandate, but the new background now makes the header the
most visually prominent cell in the table, and neither `t1` nor any other gate asserts the weight.
**Fix (optional, likely a follow-up phase):** decide the header's rank explicitly
(`font-weight: var(--fw-semibold)`) and assert it; do not change it silently inside this phase.

### IN-06: The restyle does not reach tables rendered into the five non-`.markdown-body` embed targets

**File:** `frontend/style.css:1111-1118` (scope), `:1641-1680` (the enumerated embed targets)

**Issue:** `renderMarkdown()` also injects into `.event-content` / `.chat-bubble` / `.say-chunk` /
`.annotation-note` / `.annotation-answer-body`, none of which carries `.markdown-body`. A table inside an
AI message therefore gets no `border-collapse`, no cell padding and no separator at all. This is
**pre-existing scope**, not introduced here (the old `border: 1px solid` rule was equally scoped), and the
gate's probe set correctly matches the CSS scope — recorded so that the asymmetry is a known fact rather
than an oversight discovered later.

### IN-07: The gate cannot distinguish "row separators only" from "row separators plus a bottom edge"

**File:** `frontend/style.css:1112-1117`; `scripts/check-10-idi10-validation.py:364-367`

**Issue:** Under `border-collapse: collapse` with `border: none` + `border-bottom: 1px`, the left/right/
top edges are gone but the **last row's** `td` still paints its bottom border, so the table keeps a 1px
rule along its bottom edge — the bottom of what SC1 calls 「外框」. `t2` asserts `border-bottom-width ==
1px` on a generic `td` (which includes the last row) and therefore *codifies* that line rather than
distinguishing it. If the signed-off intent is "horizontal separators between rows, no bottom edge",
`tr:last-child td { border-bottom: none; }` is missing and no assertion would notice either way.
**Fix:** decide the intent explicitly and assert it (e.g. assert the last row's `border-bottom-width`
equals `0px`), so the reading is recorded rather than left to the reader of a screenshot.

---

_Reviewed: 2026-09-27T13:33:35Z_
_Reviewer: [CL] (gsd-code-reviewer)_
_Depth: standard_

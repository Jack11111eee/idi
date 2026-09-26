---
phase: idi-05-typography-and-visual-hierarchy
reviewed: 2026-09-21T20:55:00Z
depth: standard
files_reviewed: 3
files_reviewed_list:
  - frontend/style.css
  - scripts/check-05-ui-uat.py
  - scripts/check-06-idi05-validation.py
findings:
  critical: 0
  warning: 7
  info: 5
  total: 12
status: issues_found
---

# Phase idi-05: Code Review Report

**Reviewed:** 2026-09-21T20:55:00Z
**Depth:** standard
**Files Reviewed:** 3
**Status:** issues_found

## Summary

Scope: `frontend/style.css` (the typography/visual-hierarchy contract), `scripts/check-05-ui-uat.py` (item 7 + the render-target census guard), `scripts/check-06-idi05-validation.py` (the six Nyquist behaviour assertions). Depth `standard`; the phase is frontend-only, so the review concentrated on (a) whether the gate scripts actually verify what their labels claim, and (b) whether the CSS declarations hold across all enumerated render targets.

**Verification I performed (not just reading):**

- Ran both gates against the live app. `scripts/check-05-ui-uat.py --item 7` → `exit=0`, 38 assertions, 0 FAIL, 0 BLOCKED. `scripts/check-06-idi05-validation.py` (all six items) → `exit=0`, 40 assertions, 0 FAIL, 0 BLOCKED. The phase's deliverable works.
- **Enumeration is exhaustive today.** I independently mapped all 11 `renderMarkdown(` occurrences in `frontend/app.js` (line 112 definition + 10 call sites at 239/270/284/627/848/905/917/1047/1144/1157) onto `MARKDOWN_TARGETS`. The 9 enumerated selectors are exactly the 9 distinct injection targets, and the `doc`/`embedded` split is correct. No target is missing.
- **Frozen-file claim holds.** `git diff --name-only <base>..HEAD -- frontend/` returns only `frontend/style.css`; `frontend/app.js`, `frontend/index.html` and `frontend/vendor/` have byte-empty diffs.
- **Style invariants hold.** `^\.hidden {` appears exactly once (`style.css:445`); exactly one `!important` (same line); zero `@media` blocks; the only hex literal outside the token fence is inside a comment (`style.css:94`). The contrast manifest is 47 PAIR entries = 35 TEXT + 12 NON-TEXT + 1 ORDER, matching the comment's claim.
- **Measurements taken in the browser** to substantiate WR-05, WR-06, WR-07 and WR-02 rather than reasoning from source.

**No BLOCKER-class defect found.** Every finding below is either a gate that under-verifies relative to its own label (the defect class this phase exists to eliminate) or a CSS consistency gap that no gate covers. I did not find a crash, security hole, or data-loss path.

**One thing I checked hard and it held:** the `renderMarkdown(` census guard is *not* vacuous today — 11 really is 11, and the 9 entries really do cover every target. The residual weakness (WR-03) is that the guard anchors on a *count* rather than on the target selectors, so it can go stale without the count changing.

## Narrative Findings (AI reviewer)

## Warnings

### WR-01: `check_mask_glyph`'s `icon_token` parameter is never asserted — the two icons can be swapped and every gate stays green

**File:** `scripts/check-05-ui-uat.py:278-314`

**Issue:** `check_mask_glyph(page, item, label_prefix, selector, icon_token)` takes the expected token name and uses it **only in the assertion label string**. The actual assertion is:

```python
ok_true(
    item,
    f"{label_prefix} {selector}{pseudo} mask-image 接上 var({icon_token})",
    mask != "none",
    "!=none",
    mask,
)
```

So the label claims "mask-image is wired to `var(--icon-pin)`" while the check only proves the mask is *some* image. Swapping `--icon-pin` for `--icon-location` in `.annotation-quote::before` (and vice versa in `.verdict-location::before`) produces a pin glyph on verdict rows and a teardrop on annotation quotes — and `check-05` item 6, `check-05` item 4, and `check-06` g4 all still PASS. Nothing anywhere asserts the two shapes are distinguishable, even though `style.css:312-319` declares "the two shapes must be distinguishable from each other" as part of a "mechanically checkable" shape contract.

I confirmed the data-URIs themselves are valid (both load as images; my first probe reported `imgOk: false` because my URL slicing was wrong, not because the SVG is broken).

**Fix:** resolve the token and compare, and add a distinctness assertion:

```python
expected = resolve_token(page, icon_token)
if expected is None:
    blocked(item, f"{label_prefix} {selector}{pseudo} mask-image", f"var({icon_token})", mask,
            f"{icon_token} 未声明")
else:
    ok(item, f"{label_prefix} {selector}{pseudo} mask-image == var({icon_token})", expected, mask)
```

plus one assertion that `resolve_token(page, "--icon-pin") != resolve_token(page, "--icon-location")`.

---

### WR-02: "exactly one active panel marker" is unguarded — two panels can show the blue bar with all gates green

**File:** `scripts/check-05-ui-uat.py:685-695` (control group), consumed at `:1129-1130`, `:1159-1160`, `:1165-1166`

**Issue:** `check_marker_control` asserts `box-shadow == "none"` for only two elements: `#ai-panel .panel-header` and `#doc-panel-header`. Those are the two `.panel-header`s that can never match the three ID selectors — so the control group tests the *selector* logic, but never the *mutual-exclusivity* premise the design rests on (`style.css:1198-1200`: "三个互斥面板里恰有一个可见,那一个就是「活动态」"). In the `[p3]` state nothing asserts `#checks-panel .panel-header` is unmarked; in `[checking]` nothing asserts `#annotations-panel .panel-header` is unmarked; in no state is `#session-panel`'s header checked as unmarked.

I proved this escapes: in the real `checking` state I removed `.hidden` from `#annotations-panel` (simulating a regression that makes two sidebar panels visible). Result:

```
checks: 'rgb(13, 116, 206) 3px 0px 0px 0px inset'
annot:  'rgb(13, 116, 206) 3px 0px 0px 0px inset'   <- second active marker
aiPanel: 'none'   docPanel: 'none'
```

`check_active_marker("[checking]", "#checks-panel")` PASSes; `check_marker_control("[checking]")` PASSes (its two selectors are still `none`); `check-06` g3 only measures `#checks-panel`. Two "active" panels render simultaneously and the run is green.

**Fix:** assert the invariant directly instead of sampling it — in each state, read all three panels' header `box-shadow` and require exactly one non-`none`:

```python
def check_marker_exclusivity(page, item, label_prefix, active):
    PANELS = ("#session-panel", "#annotations-panel", "#checks-panel")
    shadows = {p: read_style(page, f"{p} .panel-header", "box-shadow") for p in PANELS}
    marked = [p for p, s in shadows.items() if s and s != "none"]
    ok_true(item, f"{label_prefix} 恰有一个活动面板竖条", marked == [active],
            f"[{active}]", str(marked), str(shadows))
```

---

### WR-03: the census guard anchors on a call-site *count*, not on the target selectors — it can go stale without changing

**File:** `scripts/check-05-ui-uat.py:906-935`

**Issue:** `check_render_markdown_call_sites` does two things: `APP_JS.read_text().count("renderMarkdown(") == 11`, and `len(MARKDOWN_TARGETS) == 9`. Neither ties the enumerated **selectors** to the call sites. A change that removes one call site and adds another (or repurposes an existing call site to a new container) keeps the count at 11 and `MARKDOWN_TARGETS` at 9 entries, so both assertions stay green while the enumeration is silently wrong — precisely the "enumeration by class name went stale" failure mode this phase exists to kill. Two smaller issues in the same function: the assertion *label* hardcodes `"== 11"` and `"== 9"` while the expected values come from constants (`:922`, `:930`), so changing the constant makes the label lie; and the token count would also fire on a comment or string containing `renderMarkdown(`.

To be fair to the implementation: I verified the enumeration is **not** stale today, and the two most likely rename scenarios fail closed (renaming a container in `index.html` makes `hit.get(sel)` false → BLOCKED, not PASS). The hole is the count-preserving swap.

**Fix:** anchor on the selector set, not the count. Parse the receiver of each call and require its class/id to appear in `MARKDOWN_TARGETS`:

```python
import re
src = APP_JS.read_text(encoding="utf-8")
receivers = re.findall(r"(\w+)\.appendChild\(\s*renderMarkdown\(", src)
# each receiver is assigned via getElementById / className / id= ...; assert the
# resulting selector set == {sel for sel, _fn, _fam in MARKDOWN_TARGETS}
```

A cheaper, still-non-vacuous alternative: assert that every selector in `MARKDOWN_TARGETS` literally occurs in `frontend/app.js` or `frontend/index.html` text, so a rename cannot leave the enumeration pointing at a dead selector.

---

### WR-04: `check-06` g1 crashes with a `TypeError` instead of recording BLOCKED when `.panel-header h2` is absent

**File:** `scripts/check-06-idi05-validation.py:127-129`

**Issue:**

```python
chrome = px(read_style(page, ".panel-header h2", "font-size"))
ok_true(item, f"[p1] {host} h3 > chrome 标题(.panel-header h2)",
        sizes[2] > chrome, f">{chrome}px", f"{sizes[2]:g}px")
```

`px()` returns `None` when `read_style` returns `None` (element/selector missing). `sizes[2] > None` raises `TypeError: '>' not supported between instances of 'float' and 'NoneType'`. That propagates out of `g1` → out of `ITEMS[name](page, tmp_root)` → past the `finally` → traceback and a non-documented exit code, **aborting the whole run before the summary table is printed** (so the other five items report nothing). This directly violates the file's own stated contract ("绝不静默判过...读不到的记 BLOCKED"). Same shape as the guard `item7` in check-05 got right at `check-05-ui-uat.py:1500-1503`.

**Fix:**

```python
chrome = px(read_style(page, ".panel-header h2", "font-size"))
if chrome is None:
    blocked(item, f"[p1] {host} h3 > chrome 标题", ">chrome", None, ".panel-header h2 未渲染")
else:
    ok_true(item, f"[p1] {host} h3 > chrome 标题(.panel-header h2)",
            sizes[2] > chrome, f">{chrome}px", f"{sizes[2]:g}px")
```

---

### WR-05: g5's "button fits the panel content width" assertion measures the padding box, ~80px looser than its label

**File:** `scripts/check-06-idi05-validation.py:406-408` (measured value from `:386`)

**Issue:** `bodyClientW` is `#doc-panel-body.clientWidth`, which is the **padding box** (content + padding), not the content width. Observed in my run:

```
'bodyClientW': 339, 'btnWidth': 178, 'panelWidth': 340
```

`#doc-panel-body { padding: var(--space-8) var(--space-10); }` = 32px/40px, so the real content width is `339 - 80 = 259`. The assertion

```python
ok_true(item, "g5 按钮宽度不超出面板内容宽",
        res["btnWidth"] <= res["bodyClientW"], f"<={res['bodyClientW']}px", ...)
```

therefore permits a button up to 339px wide while claiming to guard 259px. The D-13 acceptance arithmetic this assertion exists to mechanise (`check-05-ui-uat.py:1057-1060`) uses exactly 260px. A label like `#btn-authorize` growing to ~300px wide (a real D-13 failure) would still PASS.

**Fix:**

```python
padding = page.evaluate("""() => {
  const cs = getComputedStyle(document.querySelector('#doc-panel-body'));
  return parseFloat(cs.paddingLeft) + parseFloat(cs.paddingRight);
}""")
content_w = res["bodyClientW"] - padding
ok_true(item, "g5 按钮宽度不超出面板内容宽",
        res["btnWidth"] <= content_w, f"<={content_w}px", f"{res['btnWidth']}px")
```

---

### WR-06: the embedded heading scale is not uniform — the same h1 renders a 39px line box in `.chat-bubble`/`.say-chunk` and 33px elsewhere, and the chat bubble's is taller than the document h1

**File:** `frontend/style.css:1263-1265`

**Issue:** the three appended rules set `font-size` and `font-weight` only, so line-height is inherited from each container. The five enumerated embedded targets do not inherit the same value:

| container | `h1` font-size | computed `line-height` | line box (measured) |
|---|---|---|---|
| `#draft-content` (doc reference) | 28px | 37.3324px (`--lh-tight`) | 37.33px |
| `.chat-bubble` | 24px | 39px (`--lh-reading` = 1.625) | **39px** |
| `.say-chunk` (inside `.chat-bubble`) | 24px | 39px | **39px** |
| `.event-content` | 24px | `normal` | 33px |
| `.annotation-note` | 24px | `normal` | (panel hidden in probe state) |
| `.annotation-answer-body` | 24px | `normal` | (panel hidden in probe state) |

Two consequences: (1) the "embedded scale" is not one scale — the same level occupies 39px or 33px of vertical space depending on which of the five enumerated containers it lands in; (2) an embedded `h1` in the chat stream has a **taller line box (39px) than the document's own `h1` (37.33px)**, which cuts against the SC3 statement this phase is built on ("文档自己的标题是全屏最大最重的文字"). No gate covers this: `check-05` item 7 and `check-06` g1/g2 assert `font-size` and `font-weight` only.

This is a deliberate decision (`style.css:1257-1258` explicitly declines to add margin/line-height, citing "本缺陷的判据只有字号与字重" and D-10's "零新增行高令牌"), so the fix is a judgement call rather than a clear-cut bug — but the decision's stated reason addresses *margins/rhythm*, not the 39px-vs-33px divergence, and `--lh-tight` is not a new token.

**Fix (if the divergence is accepted as a defect):**

```css
.event-content h1, .chat-bubble h1, .say-chunk h1, .annotation-note h1, .annotation-answer-body h1 { font-size: var(--text-xl); font-weight: var(--fw-semibold); line-height: var(--lh-tight); }
```

and likewise for the h2/h3 rules. That makes the embedded line box 32px uniformly and re-establishes 28px/37.33px > 24px/32px for the document-vs-embedded `h1` pair. If instead the divergence is intended, `check-06` should assert the *chosen* per-container line-height so the choice is pinned rather than incidental.

---

### WR-07: the "fourth weight rank" the phase declares out of contract survives on four chrome headings, and no gate scans them

**File:** `frontend/style.css:1263-1265` (rationale), `:704-708`, `:775-779`, `:636`

**Issue:** the embedded rules' stated rationale is that `font-weight: 700` is "契约只声明三档(400 / 500 / 600)之外的**第四档**". That fix was applied only to the five embedded containers. Measured in the real app:

```
#draft-view > h2        => 18px / 700
#round-title            => 18px / 700
#brainstorm-view > h2   => 16px / 700
.overlay-card h3        => 24px / 700
.panel-header h2        => 14px / 500
#doc-panel-header h1    => 14px / 500
```

Four headings still compute 700 (they inherit the UA `h1..h6 { font-weight: bold }` because their rules declare no `font-weight`). Two consequences: the weight contract is three ranks in one place and four in another; and because this phase raised `.markdown-body h3` from 16px to 18px, a document `h3` is now the *same size* as `#draft-view > h2` (18px) while being *lighter* (600 vs 700) — an inversion of the intended content-over-chrome hierarchy at that pair. No gate covers it: `check-05` item 7's "no 700" scan iterates only the five embedded targets, and `check-06` g2 explicitly declines to assert "最重" (`check-06-idi05-validation.py:138-139`).

**Fix:** decide which contract holds. If three ranks: add `font-weight: var(--fw-medium)` (or `--fw-semibold`) to `#draft-view > h2, #round-title`, `#brainstorm-view > h2`, and `.overlay-card h3`, and extend the "no 700" scan in `check-05` item 7 from the five embedded targets to every heading on the page (the `body *` sweep already exists in `check-06` g2 — reuse it). If four ranks are intended, correct the embedded rules' rationale so it no longer claims 700 is out of contract.

## Info

### IN-01: g5 hardcodes `"16px"` where the file's methodology resolves the token at runtime

**File:** `scripts/check-06-idi05-validation.py:399-400`

**Issue:** `ok(item, "g5 #btn-authorize 字号为 var(--text-md) 的解析值(16px)", "16px", res["fontSize"])` — the label says "解析值" but the expectation is a literal. `check-05-ui-uat.py:1063-1064` asserts the same property as `resolve_token(page, "--text-md")`. A legitimate value-layer change to `--text-md` makes g5 FAIL while item 4 PASSes on the same element.
**Fix:** `ok(item, "g5 #btn-authorize 字号 == var(--text-md)", resolve_token(page, "--text-md"), res["fontSize"])`.

### IN-02: `chain_px` uses `int()` where the rest of the harness uses `float`

**File:** `scripts/check-05-ui-uat.py:1099-1100`

**Issue:** `int(v[:-2])` raises `ValueError` (uncaught → aborts the run) on any non-integer px value, whereas `px_of` (`:1401-1408`) and `check-06`'s `px` both use `float` and return `None` on failure. The harness's contract is BLOCKED-on-unreadable, not crash.
**Fix:** reuse `px_of` and route `None` into the existing `if None in chain_px:` BLOCKED branch.

### IN-03: g2 does not assert the document h1 is *visible*

**File:** `scripts/check-06-idi05-validation.py:155-183`

**Issue:** `doc_h1` is read with `getComputedStyle`, which resolves for hidden elements. If `#draft-content` were hidden, `doc_h1` would still read 28px and `doc_h1 > worst["size"]` would still pass while the claim ("全屏最大字号的文字是文档自己的 h1") is unobservable — a near-vacuous pass of the kind the empty-`others` guard at `:175-177` was written to prevent.
**Fix:** add `ok_true(..., page.evaluate("() => { const e = document.querySelector('#draft-content h1'); return !!e && e.getClientRects().length > 0; }"), True, ...)`.

### IN-04: `ensure_server()` adopts any listener on 127.0.0.1:8765

**File:** `scripts/check-05-ui-uat.py:226-232`

**Issue:** if the port is open, the harness reuses it without confirming it is `backend.main:app`. Observed in my runs: `INFO server: 127.0.0.1:8765 已在服务 —— 复用`. A stale or unrelated process on that port would silently make every assertion meaningless (all reads would be BLOCKED, so it fails closed — but the diagnosis would point at the app rather than at the wrong server).
**Fix:** before reusing, `GET /api/session` (or any known endpoint) and confirm the expected shape; otherwise start a private instance on an ephemeral port.

### IN-05: g3's long-title box-shadow comparison cannot fail

**File:** `scripts/check-06-idi05-validation.py:265-266`

**Issue:** `long["shadow"] == base["shadow"]` compares a `box-shadow` that is a static CSS declaration — title length cannot influence it, so the assertion is a tautology. It is the same class of vacuous guard the phase set out to remove (contrast with the neighbouring `h2Delta`/`scrollW` assertions, which do carry signal).
**Fix:** drop it, or replace it with a mutation that *can* differ — e.g. assert `long["shadow"] != "none"` (i.e. the bar survived the long title) rather than equality with a value that cannot change.

---

_Reviewed: 2026-09-21T20:55:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
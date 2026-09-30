---
phase: idi-11-decard-and-hairline-dividers
reviewed: 2026-09-29T02:00:13Z
depth: standard
files_reviewed: 2
files_reviewed_list:
  - frontend/style.css
  - scripts/check-09-idi09-validation.py
findings:
  critical: 0
  warning: 1
  info: 1
  total: 2
status: issues_found
---

# Phase 11: Code Review Report (incremental — gap-closure plan 05)

**Reviewed:** 2026-09-29T02:00:13Z
**Depth:** standard
**Files Reviewed:** 2
**Status:** issues_found
**Scope:** the two files changed by `764d55c` (style.css) and `bc33cc4` (check-09). This is a
re-review of a phase whose earlier review produced CR-01 / WR-01 / WR-02 / WR-03 / IN-01 / IN-02.

## Summary

The gap-closure rewrote the horizontal hairline **in place** from
`#main-pane > section + section { border-top: … }` to
`#main-pane > section:not(:last-child) { border-bottom: … }`, and re-pointed `check-09`'s c1/c4
assertions to the new edge, added a five-state census (`HAIRLINE_CENSUS_JS`), and added the two
`#doc-panel` ground assertions c2 was missing.

**I could not break it.** I attacked the four load-bearing claims directly and each survived:

1. **The registered premise is true today.** `frontend/index.html:56-78` has `#ai-panel` as
   `#main-pane`'s DOM-last element child (nothing follows it before `</main>`), and `frontend/app.js`
   contains **no** reference to `#ai-panel` other than `#ai-panel-header` / `#ai-panel-body`
   (lines 10-11); `grep -n "ai-panel"` over the whole `frontend/` tree returns nothing else, there is
   no `.hidden =` / `setAttribute('hidden')` anywhere in `app.js`, and no `body`/`#app` class hook
   exists. `.hidden` is `display: none !important` (`style.css:772`) and only ever lands on
   `#session-panel` / `#annotations-panel` / `#checks-panel`. So `:not(:last-child)` really is
   equivalent to "every section except the last **visible** one", for **any** visibility pattern of
   the first three — the rule is state-independent, not just correct in the five fixtures.
2. **The census can fail, and it fails on the right thing.** I reproduced the mutation arithmetic
   from the recorded M1/M2 readings: reverting the rule re-introduces a `border-top` on the first
   visible panel in p3/checking/archive, which trips criterion (i) *and* (iii) (top `0.00 <= 0.5`)
   *and* inflates the line count; adding a `border-top` on top of the new rule trips c1/c4's
   `border-top == 0px` and the census's (i)/(iii). Nothing in the census is a tautology.
3. **The reorientation lost no discriminating power.** Top-border absence on **all four** sections is
   still asserted (c1 lines 264-274 and c4 lines 487-494, both on p1), and the hairline **count** is
   still pinned (c1/c4 pin the exact per-section shape on p1; the census asserts
   `len(lines) == len(visible) - 1`, i.e. exactly *n−1*, never "at least one").
4. **The corrected fence numbers are right.** I re-derived them by hand and they match `check-02`:
   blue-11 `#0d74ce` on white = **4.77** (margin **0.27**); gray-9 `#8d8d8d` = **3.32** on white /
   **3.15** on gray-2; `--color-surface-page` has exactly **four** `background:` consumers
   (style.css:764 `html, body`, :828 `#main-pane > section`, :899 `#doc-panel`, :937
   `#doc-panel-header`). The historical paragraphs (S-3 `#8a8a8a 3.45:1`; the `--color-marker-active`
   "Phase 11 update … the value itself was never touched" block) are preserved. No new fence comment
   contains "token name + colon" (checked against `check-02`'s `DECL_RE`, which also passes).

**Independently reproduced on the current tree** (not taken from the SUMMARY or `gate-logs/`):
`.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4,c5` → `exit=0`,
c1 **59** / c2 **19** / c3 **6** / c4 **39** / c5 **5**, 0 FAIL 0 BLOCKED; the c4 census prints the
expected readings for all five states (`p1`/`p12` first-visible `#session-panel`; `p3`
`#annotations-panel`; `checking`/`archive` `#checks-panel` — all `top=0.00`, `bt=0px`);
`check-01` / `check-03` / `check-04` PASS; `check-02` `PASS: 0 failures`.

**Dispositions of the prior findings** (all re-checked against the current tree): **CR-01 fixed** —
no visible section carries a `border-top` in any of the five states, and the premise it rests on is
true. **WR-02 fixed** — the three statements are numerically correct now. **WR-03 fixed** — c2
consumes `#doc-panel`'s `bg` in two falsifiable assertions. **WR-01** stays out of scope (see
carried-forward debt). **IN-01 / IN-02** stay out of scope.

Two new, non-blocking findings follow. This is a thin report by design: a fabricated finding is
worse than none, and I found no correctness, security, or data-loss defect in either file.

## Critical Issues

None. No BLOCKER was found, and I could not construct one: the rule's only failure modes are
"`#ai-panel` becomes `.hidden`" or "an element is appended after `#ai-panel`", and neither exists in
the tree — and both would be caught by the new census (`len(lines) != len(visible) - 1`) rather than
passing silently.

## Warnings

### WR-04: The specificity registration the rewrite introduced states the wrong number (says `1-1-2`; the selector is `1-1-1`)

**File:** `frontend/style.css:855` (the `⚠ 机制前提` comment block, rewritten by `764d55c`)

**Issue:** The comment reads:

> 特异性:本选择器现在是 **1-1-2**(`:not(:last-child)` 的参数是一个伪类,贡献 0-1-0),
> 仍高于 #main-pane > section(1-0-1),故它对下边框的声明稳定胜出,与源码先后无关

`#main-pane > section:not(:last-child)` has **one** ID (`#main-pane`), **one** class-level
contribution (`:last-child` inside `:not()`, which is `0-1-0` — the comment itself says so), and
**one** type selector (`section`). That is **`1-1-1`**, not `1-1-2`. The same arithmetic slip is in
the plan (`idi-11-05-PLAN.md:198,232`), which is why it landed here; this commit is the one that
wrote the sentence, so the fix belongs here.

**Falsified empirically, not argued:** with `#a:not(:last-child) { color: rgb(1,2,3) }` followed by
`div#a.x { color: rgb(9,9,9) }` (specificity `1-1-1`, later in source), Chromium resolves to
`rgb(9, 9, 9)` — i.e. the target rule does **not** outrank `1-1-1`. A `1-1-2` rule would have won.

**Why it matters / why it is not a style nit:** this is the sentence that registers *why* the rule
beats `#main-pane > section`'s `border: none`, in a comment block the same commit rewrote
specifically to stop the file from carrying claims that contradict its code. A future maintainer
relying on "1-1-2" would mis-budget headroom for a competing rule. **Impact is documentation-only
today:** the stated conclusion ("仍高于 `#main-pane > section`(1-0-1)") is still true, the rule is
also later in source order, and no gate consumes the number (`grep -rn "1-1-2" scripts/` → no hits).

**Fix:**
```css
   特异性:本选择器现在是 **1-1-1**(`:not(:last-child)` 的参数是一个伪类,贡献 0-1-0),
   仍高于 #main-pane > section(1-0-1),故它对下边框的声明稳定胜出,与源码先后无关 ——
```

(Do **not** "fix" this by raising the selector's specificity — the number is what is wrong, not the
rule. Also worth correcting at its source in `idi-11-05-PLAN.md:198,232` so the next plan does not
copy it forward; that file is outside this review's scope.)

## Info

### IN-03: The census never verifies that the state it is census-ing actually took effect

**File:** `scripts/check-09-idi09-validation.py:544-579`

**Issue:** The loop claims five-state coverage, but nothing in it pins the *expected* visibility of
each state. It asserts only (i) the first visible panel's `border-top`, (ii)
`len(lines) == len(visible) - 1`, (iii) no top line at `top <= 0.5`. All three are **satisfied by a
page that never entered the fixture at all**: pre-entry, `#session-panel` is visible and `#ai-panel`
is visible, so `visible = [#session-panel, #ai-panel]`, `lines = 1 = len(visible) - 1`, first
`border-top == 0px` → three PASSes. `c05.enter_project()` (check-05:510) asserts nothing about
whether entry succeeded, so a fixture that fails to load (backend error, app-side exception) yields a
green `[p3]`/`[checking]`/`[archive]` iteration while covering p1 three more times. The defect this
census exists to catch lived precisely in those states.

This is a *robustness* gap, not a demonstrated defect: on the current tree the readings are correct
(verified above), and `check-05 --item 1`'s `HIDDEN_MATRIX` (`check-05-ui-uat.py:569-577`) pins
`#session-panel` per state — but `check-09` is runnable standalone (`--item c4`), and then nothing in
the run pins it.

**Fix (strengthen, do not remove or relax anything):** assert the expected visible set per state
alongside the existing three criteria — the probe already returns everything needed, so it is a
lookup, not new plumbing. For example, right after `visible` is computed:

```python
        # 状态真的生效了吗:每态的预期可视集(与 check-05 HIDDEN_MATRIX:569-577 同口径)
        EXPECT_VISIBLE = {
            "p1":       ["#session-panel", "#ai-panel"],
            "p12":      ["#session-panel", "#ai-panel"],
            "p3":       ["#annotations-panel", "#ai-panel"],
            "checking": ["#checks-panel", "#ai-panel"],
            "archive":  ["#checks-panel", "#ai-panel"],
        }
        ok_true(item, f"[{state}] 该样本状态已生效(可视集 == 预期)",
                [r["sel"] for r in visible] == EXPECT_VISIBLE[state],
                str(EXPECT_VISIBLE[state]), str([r["sel"] for r in visible]),
                note="少了这条,进入 fixture 失败时三条判据在「p1 被读了 5 次」上全绿")
```

## Carried-forward debt (not in scope, recorded once)

- **WR-01** — `scripts/check-05-ui-uat.py:1315-1317`'s `.hint` ground assertion remains a tautology.
  Explicitly out of scope by user ruling; `check-05-ui-uat.py` was not reviewed in this cycle.

## Review-focus answers (for the orchestrator)

1. **Premise true? Recorded?** True today (evidence in Summary §1); recorded as load-bearing in
   `style.css:842-847`, `check-09:111-115`, `check-09:259-263`, `check-09:490-494`, and
   `check-05-ui-uat.py:777`. Adequately registered. One precision nit, not raised as a finding: the
   comment enumerates the failure mode as "在其后插入新的 **section**" — appending *any* element
   child (not just a `<section>`) after `#ai-panel` breaks it the same way.
2. **Can the census fail?** Yes — (a) non-list/unreadable → `blocked`, element-missing → `blocked`
   (a JS *throw* crashes the run, which is fail-loud, not fail-green); (b) the count is computed from
   `visible` only, so a hidden panel's border cannot be miscounted; (c) the `0.5` tolerance bounds
   *position*, not width — a real 1px top border at `top == 0.00` is caught, and a panel at
   `top <= 0.5` is by construction at the window edge; (d) the archive overlay is `position: fixed`
   (`style.css:1101-1109`) and cannot perturb computed borders or `getBoundingClientRect`, and the
   run's archive readings are the expected ones. Residual gap (not raised): the count criterion is a
   proxy for "one line *between* each adjacent pair", so a defect that simultaneously removes one
   interior line and adds one elsewhere in the same state would keep the count equal; the p1 shape
   assertions in c1/c4 are what close that.
3. **Reorientation preserved discriminating power?** Yes — top-border absence on all four sections
   is still asserted (c1:264-274, c4:487-494), and the count is constrained to exactly `n−1`, not
   "≥1". Assertion counts confirm no deletion: c1 59 (unchanged), c2 17→19, c4 20→39, c3/c5
   unchanged.
4. **Fence prose correct?** All three corrected numbers verified (hand-derived + `check-02` PASS);
   history preserved; no new token-name-colon in the fence (`check-02` `DECL_RE` clean). Note for the
   record: the old `--color-surface-page` single-consumer sentence was **replaced by a paraphrase**
   rather than kept verbatim (the two other hunks kept their history verbatim) — the information is
   retained and the claim was false, so this is fine, but the SUMMARY's blanket "历史账目段逐字保留"
   is slightly loose for that one hunk.
5. **New defects?** WR-04 and IN-03 above; nothing else in either file.

---

_Reviewed: 2026-09-29T02:00:13Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_

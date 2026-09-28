---
phase: idi-11-decard-and-hairline-dividers
reviewed: 2026-09-28T08:12:39Z
depth: standard
files_reviewed: 3
files_reviewed_list:
  - frontend/style.css
  - scripts/check-05-ui-uat.py
  - scripts/check-09-idi09-validation.py
findings:
  critical: 1
  warning: 3
  info: 2
  total: 6
status: issues_found
---

# Phase 11: Code Review Report

**Reviewed:** 2026-09-28T08:12:39Z
**Depth:** standard
**Files Reviewed:** 3
**Status:** issues_found

## Summary

Phase 11 reverses the Phase 9 card language across three artifacts: `frontend/style.css`
(five containers de-carded, page ground unified to white, two hairlines added),
`scripts/check-09-idi09-validation.py` (criteria c1..c4 rewritten to the new contract,
plus two dedicated residue assertions for the two deleted tokens), and
`scripts/check-05-ui-uat.py` (one `.hint` assertion re-pointed from the deleted
`--color-surface-card` to `--color-surface-page`).

Verified during review:

- `check-01`, `check-02`, `check-03`, `check-04` all PASS on the current tree.
- `check-09 --item c1,c2,c3,c4,c5` runs green in a real browser: 107 assertions,
  0 FAIL, 0 BLOCKED, `exit=0`. (The phase context says "46 → 102 assertions"; the
  measured count is **107** = c1 59 + c2 17 + c3 6 + c4 20 + c5 5. Not a code defect,
  but downstream consumers should not treat "102" as a checked-in fact.)
- No non-`.planning` file references the two deleted tokens any more (`frontend/` has
  zero hits; the only remaining occurrences repo-wide are the literal name list in
  `check-09` itself). The two residue assertions therefore pass legitimately, and no
  new instance of the "literal inside a comment breaks a substring gate" class was
  introduced by the new fence prose.
- The Phase 11 contrast ledger in the fence was spot-checked against `check-02`'s
  output and is arithmetically correct (white ground: text 16.29, secondary/muted 5.92,
  focus 5.87, marker 4.77, border-strong 3.32, ordering 0.363).

The substantive problems are: one behavioural contradiction of the ratified
D-11-10 hairline contract that reproduces in 3 of the 5 sample states (CR-01), one
gate assertion in `check-05` that this phase silently turned into a tautology
(WR-01), and stale prose in the token fence that this phase's own ledger contradicts
(WR-02).

## Critical Issues

### CR-01: The horizontal hairline is drawn at the window edge whenever `#session-panel` is hidden

**File:** `frontend/style.css:856` (rule), rationale/claim at `frontend/style.css:833-836`

**Issue:** `#main-pane > section + section { border-top: 1px solid var(--color-border-subtle); }`
uses **DOM** adjacency. `#session-panel` is the DOM-first `<section>`, so it never
receives a line — which is exactly the intent the comment states: "第一个面板顶部不画线
(顶部是窗口边缘,画了会读成多一条)". But `#session-panel` is `display: none` in every
state that is not phase 1/2 (`frontend/app.js:363`,
`sessionPanel.classList.toggle('hidden', !isSessionPhase)`). In those states the first
**rendered** panel is `#annotations-panel` (p3) or `#checks-panel` (checking, archive),
and it carries the 1px border at `#main-pane`'s top edge — i.e. a hairline pinned to the
top of the window, the precise artefact D-11-10 exists to prevent. The comment's own
claim ("两种显隐状态下都恰好 1 条可见分界", lines 835-836) is therefore false.

Measured in a real browser (Playwright bundled chromium, 1440×900, one fixture per
state, read-only probe over `check-05`'s harness):

```
state=p1        #main-pane.top=0
  session-panel     display=flex  top=  0.0  border-top=0px
  ai-panel          display=block top=767.0  border-top=1px   (separator)
state=p3        #main-pane.top=0
  session-panel     display=none  top=  0.0  border-top=0px
  annotations-panel display=flex  top=  0.0  border-top=1px   <== HAIRLINE AT WINDOW EDGE
  ai-panel          display=block top=121.0  border-top=1px   (separator)
state=checking  #main-pane.top=0
  checks-panel      display=flex  top=  0.0  border-top=1px   <== HAIRLINE AT WINDOW EDGE
  ai-panel          display=block top=395.9  border-top=1px   (separator)
state=archive   #main-pane.top=0
  checks-panel      display=flex  top=  0.0  border-top=1px   <== HAIRLINE AT WINDOW EDGE
  ai-panel          display=block top=331.2  border-top=1px   (separator)
```

3 of the 5 sample states ship an extra line the design forbids. The gate cannot see it:
`check-09` c4 (`scripts/check-09-idi09-validation.py:443-446`) asserts
`#session-panel`'s `border-top-width == 0px` **only in p1**, where `#session-panel` is
the rendered-first panel — the assertion is true and irrelevant in exactly the state
where the defect cannot occur.

**Fix:** There is no pure-CSS sibling-combinator form that expresses "first *visible*
section": `section.hidden + section:not(.hidden) { border-top: none }` suppresses the
line correctly in p3 but also suppresses the `#checks-panel → #ai-panel` separator in
p3 (checks is `.hidden`, so `checks.hidden + ai` matches). Pick one of:

1. Have `app.js` toggle a class alongside the existing `.hidden` toggles (the same place
   `sessionPanel.classList.toggle('hidden', ...)` already lives) and key the rule off it,
   e.g. `#main-pane > section.is-first-visible { border-top: none; }`; or
2. Draw the separator as a **bottom** border on all but the last *visible* section under
   the same JS-assisted scheme; or
3. If the team decides the window-edge line is acceptable, re-ratify D-11-10 and correct
   the comment at `frontend/style.css:833-836` — but do not leave the code and its
   ratified rationale contradicting each other.

Whichever is chosen, extend `check-09` c4 so the assertion runs in a state where
`#session-panel` is hidden (the `checking` fixture already exists in the file), otherwise
the regression is unobservable to the gate.

## Warnings

### WR-01: `check-05` item5's `.hint` ground assertion became a tautology after the expected side was re-pointed

**File:** `scripts/check-05-ui-uat.py:1315-1317` (assertion), `scripts/check-05-ui-uat.py:471-484` (`effective_bg`)

**Issue:** The assertion is `ok("[p1] .hint 实际背景 == var(--color-surface-page)",
resolve_color(page, "--color-surface-page"), effective_bg(page, ".hint"))`. `effective_bg`
walks up the ancestor chain and, when nothing paints a background, **falls back to
`getComputedStyle(document.documentElement).backgroundColor`** — and after Phase 11 the
root's background *is* `--color-surface-page` (white). The expected value and the
fallback value are now the same token, so the assertion can no longer fail for the
failure mode it was written to catch ("the `.hint` really sits on the panel's paint").

Demonstrated at runtime (read-only; `#doc-panel`'s background stripped in-page):

```
BASELINE  expected=rgb(255,255,255)  effective_bg('.hint')=rgb(255,255,255)  #doc-panel=rgb(255,255,255)
AFTER stripping #doc-panel background:
          #doc-panel bg=rgba(0, 0, 0, 0)
          effective_bg('.hint')=rgb(255,255,255)   -> assertion would still PASS
```

Before this phase the expected side was `--color-surface-card` (white) while the fallback
was the page ground `gray-3` (`rgb(240,240,240)`), so the same mutation **would have
FAILED**. The re-pointing in this phase removed the discriminating power — a textbook
"门绿着在看" regression of the kind this repo has repeatedly paid for. Note the comment
block at lines 1303-1314 reasons carefully about the `ok()`-returns-BLOCKED hazard but
does not consider the fallback.

**Fix:** Assert the *paint path*, not the resolved value. Either assert the panel's own
declaration, e.g. add to the same item

```python
ok(item, "[p1] #doc-panel 计算 background-color == var(--color-surface-page)",
   resolve_color(page, "--color-surface-page"),
   read_style(page, "#doc-panel", "background-color"),
   note=".hint 的实际地面由 #doc-panel 绘制;只比 effective_bg 会沿祖先链落到 <html>,"
        "而 <html> 用的是同一个令牌 ⇒ 断言恒真")
```

or make the ground assertion two-sided by pinning the literal as well
(`effective_bg(page, ".hint") == "rgb(255, 255, 255)"` does **not** help — same value);
the panel-level declaration assertion is the one that restores discrimination.

### WR-02: Retained fence prose is now false and is contradicted by this phase's own ledger

**File:** `frontend/style.css:136-137`, `frontend/style.css:189-191`, `frontend/style.css:93`

**Issue:** Phase 11 rewrote the neighbouring sentences and added a Phase 11 ledger, but
left three present-tense claims that the value rewrite invalidated. Each is now
contradicted by the file itself, and this fence is the project's authoritative token
record.

1. `frontend/style.css:136-137` — *"This token has exactly ONE consumer (`html, body`'s
   background), so changing the value here re-colours the whole page and nothing else
   needs synchronising."* `--color-surface-page` now has **four** consumers:
   `frontend/style.css:759` (`html, body`), `:822` (`#main-pane > section`), `:880`
   (`#doc-panel`), `:918` (`#doc-panel-header`). The follow-on claim ("nothing else needs
   synchronising") is the more dangerous half: a reader changing this value would not
   expect the panels and the sticky header to move with it — which is precisely what this
   phase made them do.

2. `frontend/style.css:189-191` — *"Measured 4.65 on `--color-surface-page` … and is this
   phase's thinnest margin (0.15)."* On the current (white) page ground `--color-marker-active`
   measures **4.77** (confirmed by `check-02` and by the Phase 11 ledger at
   `frontend/style.css:598-606`, which states "measures 4.77 (margin 0.27)"). The retained
   sentence and the ledger the same commit added disagree with each other.

3. `frontend/style.css:93` — *"gray-9 = 3.24 / 3.15"*. The `3.24` was the page-ground
   reading on `gray-1`; on the unified white ground `--color-border-strong` measures
   **3.32** (`check-02` output and the Phase 11 ledger at `frontend/style.css:600`).
   Only the `3.15` half (on `--color-surface`) is still correct. (This number was already
   stale after Phase 9; Phase 11 changed the page ground again without correcting it, so
   it is now wrong in a third direction.)

**Fix:** Rewrite the three retained sentences to the post-Phase-11 facts — e.g. "this token
has FOUR consumers (`html, body`, `#main-pane > section`, `#doc-panel`,
`#doc-panel-header`), so changing it re-colours the page, the four left panels and the
sticky header together"; "measured 4.77 on the unified surface (margin 0.27)"; "gray-9 =
3.32 / 3.15". Do not delete the historical paragraphs — only the present-tense
measurements are wrong.

### WR-03: `check-09` c2 collects `#doc-panel`'s background but never asserts it

**File:** `scripts/check-09-idi09-validation.py:322` (read), `scripts/check-09-idi09-validation.py:342-369` (assertions)

**Issue:** The file's own opening contract is "连续面(五个容器不再绘制边界)+ 统一面
(**面板与页面同色**、内陷面仍更暗)" (`scripts/check-09-idi09-validation.py:20-21`).
c1 asserts page-equality for the four left sections (`:248-252`), and c2 asserts it for
`#doc-panel-header` (`:385-387`) — but `#doc-panel` itself, the fifth container named in
the phase's own scope, is only *read* into `bg` (`:322`) and then used solely in `info()`
and in the BLOCKED message. No assertion consumes it.

Consequence: `#doc-panel` could be repainted to any colour (e.g. back to a gray) and
`check-09` would stay green — the header paints its own background, so the c2 header
assertion would still pass, and `check-05` does not assert `#doc-panel`'s background
either. That is one fifth of the phase's headline deliverable with no gate.

**Fix:** Add, next to the other c2 assertions (and using the already-computed `body_bg`
from line 376):

```python
ok(item, "[p1] #doc-panel 计算底色 == body 计算底色(统一面)",
   body_bg, bg,
   note="五个容器统一面的一部分;c2 原先只读了 bg 未断言 ⇒ 面板被重新上色时本门看不见")
```

and optionally the literal half (`SURFACE_PAGE_LITERAL`) for the same
"token-drift-but-still-wired" reason c1 uses it.

## Info

### IN-01: `fence_text()` is unguarded — a missing fence marker crashes instead of recording BLOCKED

**File:** `scripts/check-09-idi09-validation.py:159-168`

**Issue:** `text.index(FENCE_START)` / `text.index(FENCE_END)` raise `ValueError` (and
`read_text` raises `OSError`) if the fence markers are renamed or removed. The exception
escapes `c1` and terminates the process with a traceback before any assertion is
recorded, so `item_verdict` never runs and the exit code carries no diagnosis. It is
fail-loud rather than fail-green, so this is not a correctness hole — but the file
elsewhere goes to some length to convert unreadable state into an explicit BLOCKED with a
reason (`:3646-3651` in `check-05` is the same pattern done properly).

**Fix:** Wrap the body of `fence_text()` and return `None` on `OSError`/`ValueError`, then
have the c1 residue block emit `blocked(item, "...", "围栏标记各出现一次", ..., "围栏标记
不成对 ⇒ 子串计数不可信")` and skip the two residue assertions. Note this function is
copied verbatim from `check-10-idi10-validation.py:184`, so the same fix should be applied
there or explicitly registered as accepted.

### IN-02: Stale `argparse` description in `check-09`

**File:** `scripts/check-09-idi09-validation.py:711`

**Issue:** `description="Phase 9 卡片语言的运行时门"` no longer describes what the file
asserts; the module docstring was rewritten for Phase 11 but the `--help` text was not.

**Fix:** `description="Phase 9 卡片语言 / Phase 11 去卡片化与发丝分隔线的运行时门"`.

---

_Reviewed: 2026-09-28T08:12:39Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_

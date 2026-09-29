---
phase: idi-12-g1-band
reviewed: 2026-09-29T09:08:08Z
depth: standard
files_reviewed: 3
files_reviewed_list:
  - frontend/style.css
  - scripts/check-09-idi09-validation.py
  - scripts/ui-states/checking/docs/DESIGN-check-2.md
findings:
  critical: 0
  warning: 1
  info: 6
  total: 7
status: issues_found
---

# Phase 12: Code Review Report

**Reviewed:** 2026-09-29T09:08:08Z
**Depth:** standard
**Files Reviewed:** 3
**Status:** issues_found

## Summary

Scope was the three source files changed in `f4603ef9^..HEAD`: one declaration rewrite + a fence-comment rewrite in `frontend/style.css`, the new `c6` runtime item + `--g1-snapshot` CLI parameter in `scripts/check-09-idi09-validation.py`, and a `## 问题分级` table added to the `checking` fixture report `scripts/ui-states/checking/docs/DESIGN-check-2.md`.

The core change is correct and the new gate is sound. I verified the substance rather than assuming it:

- **`c6` is two-sided and genuinely independent.** I traced every assertion. The three colour readings come from three different sources (host element rule, `th` element rule, `documentElement` token declaration via `resolve_color`'s probe div) — none is self-referential, and each can fail independently: reverting `#latest-check` to `var(--color-surface)` fails the `host != th` assertion; deleting the declaration makes the host transparent (fails the token-equality assertion); hardcoding `#ffffff` and deleting the token fails the same assertion because `resolve_color` returns `None` for an undeclared token and the assertion uses `ok_true` with an explicit `is not None` guard. Helper choice is correct throughout — no token-resolution assertion was written with `ok()`. The two literal assertions that *do* use `ok()` have non-`None` expected sides, and their only `actual is None` path (element missing) is already hard-FAILed by the preceding `ok_true`, so there is no silent BLOCKED degradation.
- **`g1-snapshot`'s geometry assertion is not vacuous.** I empirically confirmed with Playwright that `locator.bounding_box()` does **not** scroll the element into view (a target inside an `overflow:auto` container stays at its off-screen `y`), so assertion 2 can genuinely fail when the table falls below the `max-height: 30vh` fold. I re-ran the item end-to-end (`--item c6 --g1-snapshot /tmp/g1snap-review`): `c6 PASS (7 条断言)`, `g1-snapshot PASS (3 条断言)`, host box `736x270`, `th` at `y=203.66..234.9` — inside the host with ~125px of slack, so it is satisfiable but still has a failure margin.
- **The fixture is grammar-faithful and does not flip `mode`.** I ran the backend parser against the fixture directly: `parse_problem_grades` yields 2 rows (`P1`, `P2`), `is_pure_p2` → `False`, `is_pass_conclusion` → `False`, `unpaired_verdicts` → `[]`. Per `backend/session.py:225-262` the derived mode is therefore `running`, so `#btn-continue-check` keeps no `.hidden` (it starts `.hidden` in `index.html:48` and is only un-hidden by the `running`/`awaiting_tier` branches) and `#verdict-cards` stays empty. `c6`'s fixture invariant is real, not decorative.
- **The change is purely additive on the gate side.** Every `-` line in the `check-09` diff is either the `ITEMS` literal (now carrying `c6`) or the `summary` construction; no existing assertion was deleted, relaxed, or turned into a tautology. `c1..c5` counts are unchanged, matching the phase's claim.

The defects found are documentation/evidence-accuracy and gate-robustness issues, not correctness or security bugs. The most consequential one is that the fence comment the phase rewrote to remove one stale half still contains a *different* stale half — the consumer ledger — that this same change falsified.

## Narrative Findings (AI reviewer)

### Warnings

#### WR-01: Fence comment's consumer ledger is now false — the change added a fifth consumer and left the count at four

**File:** `frontend/style.css:139-143` (changed region: the same comment block, `:130-133`)

**Issue:** This phase's stated job for the fence comment was to delete the half that its change falsified ("the sentence that used to stand here claimed `#latest-check` was recessed as well; that half is now false"). The edit fixed that half but left the very next paragraph asserting:

> `This token now has FOUR consumers, not one: `html, body`'s background, plus the three panels Phase 11 merged into this surface — `#main-pane > section`, `#doc-panel` and `#doc-panel-header` all paint it. Changing the value here therefore re-colours the page, all four left-column panels and the sticky document header at once; none of them follows along on its own.`

Rewriting `#latest-check`'s `background` from `var(--color-surface)` to `var(--color-surface-page)` makes `#latest-check` a **fifth** consumer of this token. Verified mechanically: `grep -n 'var(--color-surface-page)' frontend/style.css` returns 4 hits at `f4603ef^` (764, 828, 900, 938) and 5 at `HEAD` (767, 831, 903, 941, 1660). The paragraph's own warning ("stale consumer counts were *the more dangerous half*") is now violated by the paragraph itself.

**Realistic failure scenario:** a later phase re-values `--color-surface-page` (Phase 11 already did exactly this once, gray-3 → white) and trusts the ledger: it re-checks `html, body`, `#main-pane > section`, `#doc-panel`, `#doc-panel-header`, concludes "none of them follows along on its own" is satisfied, and never re-derives the contrast pairs drawn on `#latest-check`'s new white ground. The comment is the only place in the file that enumerates this token's blast radius, so an undercount here silently narrows the next change's impact analysis.

**Fix:** rewrite the sentence to five consumers and name the new one, e.g.

```
     This token now has FIVE consumers, not one: `html, body`'s background, plus the
     three panels Phase 11 merged into this surface — `#main-pane > section`,
     `#doc-panel` and `#doc-panel-header` — plus `#latest-check`, which Phase 12 lifted
     onto this ground (G1-01). Changing the value here therefore re-colours the page,
     all four left-column panels, the sticky document header and the check-report
     container at once; none of them follows along on its own.
```

### Info

#### IN-01: `checking` is described as the only sample where `#latest-check` is visible; `archive` also shows it

**File:** `scripts/check-09-idi09-validation.py:794-795` and `:904-905`

**Issue:** Both new comments justify the sample choice with "`#latest-check` **只在该样本可见**" / "`checking` 是**唯一** `#latest-check` 可见的样本(p1 下祖先 `#checks-panel` 带 `.hidden`)". The parenthetical is true for `p1` only. In the `archive` sample `applyArchiveView` runs `checksPanel.classList.remove('hidden')` (`frontend/app.js:873`) and then `loadArchiveView` → `loadChecksView(null)` (`frontend/app.js:899`) renders the archive report into `#latest-check` — so `#latest-check` is visible there too. The actual reason `checking` is required is narrower: only `checking`'s report carries a `## 问题分级` table, so only there does `#latest-check th` exist (`archive/docs/DESIGN-check-1.md` has no table).

**Fix:** state the real premise, e.g. "`checking` 是唯一报告里带「问题分级」表的样本(故唯一有 `th` 可读的样本);`archive` 也显示 `#latest-check`,但其报告无表。" No behaviour change needed.

#### IN-02: `--item` help string still advertises only `c1`–`c5`

**File:** `scripts/check-09-idi09-validation.py:960`

**Issue:** `help="只跑指定项:c1 / c2 / c3 / c4 / c5(可重复,或逗号分隔)"` omits the newly added `c6`, even though `ITEMS` now contains it and the module docstring documents it. A user following the help text will not discover the new item.

**Fix:** `help="只跑指定项:c1 / c2 / c3 / c4 / c5 / c6(可重复,或逗号分隔)"`.

#### IN-03: `g1-snapshot` assertion 3 cannot fail in the situation it is documented to cover

**File:** `scripts/check-09-idi09-validation.py:946-951`

**Issue:** The item's comment claims "三条断言把「拍到了 band」变成**可失败**的 … ③PNG 宽高非零". But `page.locator("#latest-check").screenshot(path=...)` on line 947 either writes a valid PNG (in which case `png_size()` reads a valid IHDR and both dimensions are necessarily `> 0`) or raises — and an exception propagates out of `g1_snapshot`, through `main()`'s `finally`, and aborts the process with a traceback rather than emitting a FAIL row. So assertion 3 contributes no failability of its own; it is a "the file landed" check dressed as a band check. (I re-ran the item: `actual=736x270`.)

**Fix:** make it discriminating by pinning the capture against the host geometry already read on line 928, e.g.

```python
ok_true(item, "[checking] #latest-check 元素截图尺寸 == 宿主矩形(拍到的是该容器)",
        host_rect is not None
        and abs(width - round(host_rect["width"])) <= 1
        and abs(height - round(host_rect["height"])) <= 1,
        f"≈ {host_rect['width']}x{host_rect['height']}", f"{width}x{height}",
        note=str(png_path))
```

#### IN-04: `c6`'s `cards == 0` assertion is vacuously satisfied if `#verdict-cards` is removed from the DOM

**File:** `scripts/check-09-idi09-validation.py:857-860`

**Issue:** `cards = page.evaluate("() => document.querySelectorAll('#verdict-cards .verdict-card').length")` returns `0` both when the container exists and is empty *and* when the container is absent entirely (`index.html:50`). Deleting `#verdict-cards` — which is exactly what the mode-flip regression would also involve touching — keeps this assertion green. The companion assertion on line 852 covers the mode flip via `#btn-continue-check`, so this is a robustness gap rather than a hole in the invariant.

**Fix:** assert the container exists as part of the same condition, e.g. evaluate `document.querySelectorAll('#verdict-cards').length` alongside and require `== 1 and cards == 0`.

#### IN-05: `c6` asserts computed colours with no rendering premise

**File:** `scripts/check-09-idi09-validation.py:796-841`

**Issue:** Every `c6` assertion reads `getComputedStyle` values, and this file itself documents (`:204-207`, `:257`) that `getComputedStyle` resolves normally inside a `display:none` subtree. `#latest-check` is a descendant of `#checks-panel` (`frontend/index.html:39-52`), so if the panel (or any ancestor) were hidden while `loadChecksView` still ran its `running` branch, `c6` would report `PASS` for a band no user can see. This repo has an explicit precedent against that shape: `check-10`'s `t1` added `render_evidence_assertion` precisely because "隐藏子树上的层叠读数会被读成渲染证据". Mitigating factor: assertion 6 requires `#btn-continue-check` to be free of `.hidden`, and that class is only removed inside `loadChecksView`'s `running` branch, which runs after `checksPanel.classList.remove('hidden')` (`frontend/app.js:630-631`) — so `c6` carries an *indirect* visibility premise today, and `g1-snapshot` asserts visibility directly via `bounding_box()`.

**Fix (optional, low priority):** add one explicit premise assertion mirroring `check-10`'s pattern, e.g. `ok_true(item, "[checking] #latest-check 处于被渲染子树(rect 非零)", ...)` using `page.evaluate` on `getBoundingClientRect().height > 0`.

#### IN-06: The recorded `check-09` gate log contains no `g1-snapshot` section

**File:** `.planning/phases/idi-12-g1-band/gate-logs/idi-12-03/check-09-idi09-validation.log:184-204`

**Issue:** The phase's recorded evidence for `check-09` shows the `c6` block (`item c6: PASS (7 条断言,0 FAIL,0 BLOCKED)`) but stops at `逐项结论` with only `c1..c6` — there is no `g1-snapshot` section, so the three new `--g1-snapshot` assertions have no captured run in the phase evidence (the PNG at `screenshots/latest-check/latest-check.png` is timestamped 15:51, the logged run 16:09). I independently re-ran the item and it passes (`item g1-snapshot: PASS (3 条断言,0 FAIL,0 BLOCKED)`, `736x270`), so this is an evidence-capture gap rather than a failing gate.

**Fix:** re-run `--g1-snapshot` into the recorded log path so the phase's gate evidence contains the run it cites.

---

_Reviewed: 2026-09-29T09:08:08Z_
_Reviewer: [CL] (gsd-code-reviewer)_
_Depth: standard_

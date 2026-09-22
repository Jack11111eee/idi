---
phase: idi-06-layout-robustness
reviewed: 2026-09-22T05:42:50Z
depth: standard
files_reviewed: 2
files_reviewed_list:
  - frontend/style.css
  - scripts/check-05-ui-uat.py
critical: 1
warning: 3
info: 2
total: 6
status: findings
---

# Phase idi-06: Code Review Report

**Reviewed:** 2026-09-22T05:42:50Z
**Depth:** standard
**Files Reviewed:** 2
**Status:** findings

## Summary

The CSS half of this phase is sound. I traced every changed declaration in `frontend/style.css` and could not falsify any of them:

- `#doc-panel-header { position: sticky; top: 0 }` works. Its containing block is `#doc-panel` (a direct parent, `display: flex; flex-direction: column`), and `#doc-panel { overflow-y: auto }` makes the panel itself the scrollport, so the header sticks to the panel's padding-box top. Measured live at 1440×900 with `#doc-panel` scrolled to the bottom (`scrollTop=4348`, `scrollHeight=5248`): `header.top = 0`, `panel.top = 0` — the header does not travel with the content.
- `background: var(--color-surface)` resolves (`style.css:183`, `--radix-gray-2: #f9f9f9`, opaque), so content scrolling under the header cannot show through. Matching the underlying surface colour is irrelevant because the paint is opaque.
- `border-radius: 0` wins over `.panel-header`'s `var(--radius-md)` on specificity (`#doc-panel-header` 1-0-0 beats `.panel-header` 0-1-0), independent of the append/in-place placement. No later rule in the file declares `position` / `top` / `background` / `border-radius` on this element, so the mid-file insertion at `style.css:512` breaks no cascade.
- `min-width: 0` on `#doc-panel` is genuinely load-bearing, not redundant: `flex: 0 0 <clamp>` fixes the flex base size but `min-width: auto` resolves to the content-based minimum, so an unbreakable token inside the panel would set the hypothetical main size *above* `clamp()` (measured min-content of the L-2 probe content is ≈1680px). The comment on `style.css:481-485` is accurate.
- Removing `max-height`/`overflow-y` from `.event-list` and `#annotation-list` leaves exactly the intended scroller set; the census confirms `{#main-pane, #chat-messages, #latest-check}` and nothing else.
- `min-height: 24px` on `.annotation-answer summary` is honoured (measured 722 × 24, up from 722 × 17).

The harness half has real problems. I ran both new items (`.venv/bin/python scripts/check-05-ui-uat.py --item 8` and `--item 9`) and read the raw INFO lines rather than trusting the SUMMARY. `item 8: PASS (13 条断言, 0 FAIL, 0 BLOCKED)` and `item 9: PASS (16 条断言, 0 FAIL, 0 BLOCKED)` reproduce — but one of those PASSes is on a criterion that is measurably violated at the very width the criterion names, and three of the new assertions are weaker than their labels claim. `CR-01` is the one that matters; the others are latent false-PASS / false-FAIL holes rather than active failures.

No security issues: the diff adds no input handling, no injection surface, no secrets. `page.evaluate` arguments are passed as arguments (`_IDI06_REACH_JS(sel)`), never interpolated, so the new JS templates carry no injection risk.

## Critical Issues

### CR-01: LAYOUT-02's 768px "无内容遮挡" criterion is measurably violated, and the new comment claims the badge×banner assertion covers it

**File:** `scripts/check-05-ui-uat.py:1931-1933` and `scripts/check-05-ui-uat.py:1944-1946`

**Issue:** The new comment asserts a coverage that does not exist:

```python
# LAYOUT-02 的字面承诺「≥1024px 无横向溢出」—— 1440 与 1024 两处升为硬断言。
# 768 处保持只读诊断:它在 LAYOUT-02 里的承诺是「无内容遮挡」,已由本项前面的
# badge × banner 不相交断言覆盖(UI-SPEC §L-2 的判据表)。
```

and again:

```python
info(f"item8 L-2 @{width}px",
     "保持只读诊断(768px 处的承诺是「无内容遮挡」,"
     "已由 badge × banner 不相交断言覆盖)")
```

The only 768px geometry assertion in item 8 is `#state-badge × #stream-banner` (`check-05-ui-uat.py:1832-1839`). LAYOUT-02's criterion is the broader "关键元素 rect 两两不相交" (`idi-06-UI-SPEC.md:192`). The badge is not the occluded element.

**Measured failure scenario (reproduced on HEAD, not inferred).** The harness's own INFO line prints the banner rect that proves it:

```
INFO item8 [768px] badge × banner 原始 rect: badge={'left': 638.97, 'right': 739.89, 'top': 7, 'bottom': 32, ...} | banner={'left': 285.34, 'right': 482.66, 'top': 12, 'bottom': 39, ...}
```

At a 768px viewport `--doc-panel-w: clamp(340px, 30vw, 480px)` (`frontend/style.css:228`) resolves to its **floor**, 340px, so `#doc-panel` starts at x=428. The banner is centred (`#stream-banner { position: fixed; top: 12px; left: 50%; transform: translateX(-50%) }`, `frontend/style.css:710-723`) and is 197px wide, so it reaches x=482.7 — 54.7px into the panel. A direct measurement of the panel title:

```
h1     = {l: 439.0, t: 8.0,  r: 481.0, b: 28.0}   # #doc-panel-header h1 ("文档区")
header = {l: 429.0, t: 0.0,  r: 768.0, b: 36.0}
banner = {l: 285.3, t: 12.0, r: 482.7, b: 39.0}
h1_vs_banner = True ; header_vs_banner = True
bannerZ = 20 ; bannerPos = fixed ; bannerBg = rgb(255, 247, 194)
```

The banner's x-span (285.3–482.7) fully contains the h1's x-span (439–481), and vertically covers y 12–28 of the h1's 8–28. The banner is `position: fixed` with `z-index: 20` and an opaque amber-3 background, while the sticky header is a positioned element with `z-index: auto`, so the banner paints on top: whenever SSE disconnects at the promised minimum window width, the panel's title label is entirely hidden. `item 8` reports PASS for this viewport.

The geometry predates this phase (the banner and the clamp are untouched by the diff, and the header occupied the same 36px band before it became sticky), so this is not a regression. It is nonetheless the criterion the phase declares itself to satisfy at 768px, and the new gate reports PASS on it while a probe that takes ten lines would falsify it — the exact "假 PASS" failure this phase registered as `T-idi-06-04`.

**Fix:** pick one and record it, but do not leave the comment as written.

1. Actually assert the criterion. Extend `_IDI06_BADGE_BANNER_JS` (`check-05-ui-uat.py:1652-1668`) to also return `#doc-panel-header` and its `h1` rect, then add a 768px-only assertion:

```python
ok_true(item,
        f"[@{width}px] #stream-banner 不遮挡 #doc-panel-header(h1)",
        not _rects_intersect(banner, geo["docHeader"])
        and not _rects_intersect(banner, geo["docHeaderH1"]),
        "不相交", f"banner={banner} header={geo['docHeader']} h1={geo['docHeaderH1']}",
        "LAYOUT-02 的 768px 承诺:无内容被遮挡")
```

It will FAIL today, which is the correct signal; the underlying fix is either to un-centre the banner (e.g. `left: auto; right: 12px` on narrow viewports) or to raise the clamp floor so the panel starts right of x=482.7 at 768px.
2. If the project instead decides this pair is out of LAYOUT-02's scope, say so explicitly in `idi-06-UI-SPEC.md` §L-2 and replace both comment sites with the measured numbers and an explicit "not covered" statement — the current wording inverts the truth, which is worse than no wording because it stops the next reader from looking.

## Warnings

### WR-01: `_idi06_reach` records a vacuous PASS for "末条内容可达" when the probe content fails to make the container scroll

**File:** `scripts/check-05-ui-uat.py:2125-2167`

**Issue:** The precondition chain rejects only `injected is None`:

```python
if injected is None:
    blocked(item, label, "内容经应用自身的渲染路径注入", "<MISSING>", inject_error)
    return
```

Both call sites pass an integer count, and `0` is not `None`. `item9`'s `#main-pane` probe (`check-05-ui-uat.py:2292-2299`) returns `document.querySelectorAll('#ai-events .event-item').length`; if `renderEvent` ever stops appending (renamed internal, a state guard, a silent exception path), that is `0`, the precondition passes, and then:

```python
if geo["scrollHeight"] <= geo["clientHeight"]:
    info(f"item9 {label}",
         "容器无需滚动,可达性平凡成立(不记断言,避免空转 PASS)")
else:
    ok_true(item, f"[{sample}] {sel} 滚到底(...)", ...)
```

only the *scroll* half is downgraded to `info()`. The last-child half at `check-05-ui-uat.py:2161-2167` still runs:

```python
ok_true(item, f"[{sample}] {sel} 末条子元素落在容器可视区内",
        geo["last"]["bottom"] <= geo["container"]["bottom"] + 1
        and geo["last"]["bottom"] >= geo["container"]["top"], ...)
```

When nothing was injected the container does not overflow, so the last child is trivially inside it and this records **PASS** for a claim that was never exercised. The same hole exists on the `#latest-check` side (`check-05-ui-uat.py:2309-2315` returns `c.childElementCount`, which is `0` if `window.marked` is missing — `renderMarkdown` then returns a bare Text node, `app.js:113`). Note the inconsistency: the sticky-header assertion in item 8 (`check-05-ui-uat.py:1861-1868`) *does* treat "container cannot scroll" as `blocked()`. The project's own doctrine (stated in this item's comment at `check-05-ui-uat.py:2119-2122`) is that a missing precondition is BLOCKED, never PASS.

**Fix:** require a positive injection count and treat a non-scrolling container as a failed precondition for the last-child assertion:

```python
if not isinstance(injected, int) or injected <= 0:
    blocked(item, label, "注入计数 > 0", injected, "注入未生效 ⇒ 可达性判定是空转,不记 PASS")
    return
...
if geo["scrollHeight"] <= geo["clientHeight"]:
    blocked(item, label, "scrollHeight > clientHeight(容器真的可滚)",
            f"scrollHeight={geo['scrollHeight']} clientHeight={geo['clientHeight']}",
            "容器无需滚动 ⇒ 末条可达性平凡成立,不记 PASS")
    return
```

### WR-02: the L-5 clearance assertion fails on partially-scrolled-out elements, which is normal scroll behaviour, not clipping

**File:** `scripts/check-05-ui-uat.py:2186-2192` (judgement) and `scripts/check-05-ui-uat.py:1707-1709` (`intersects`)

**Issue:** `judged` keeps rows where the element is visible *and* intersects the container's padding box:

```python
judged = [r for r in rows if r["visible"] and r["intersects"]]
...
bad = [r for r in judged if r["clearance"] < CLEARANCE_MIN_PX]
```

`intersects` only excludes elements that are **completely** outside the padding box. An element that is *partially* scrolled out of a scroll container has `intersects == True` and a negative clearance (the offending term is `padBottom - r.bottom`), so it lands in `bad` and FAILs — even though partial visibility is the normal, unavoidable behaviour of every scroll container, and the browser scrolls the element into view when it receives focus. The assertion therefore measures scroll position, not clipping.

The margin is thin and is printed by the harness itself. From the p3 sample:

```
('#round-switcher', '#doc-panel', 110.8, True, True)
('#btn-authorize',  '#doc-panel', -122.6, True, False)   # excluded only because intersects=False
```

`#btn-authorize` is already at clearance −122.6px against `#doc-panel`; it is excluded solely because it sits 122.6px past the bottom edge. Any change that moves it (or scrolls the panel) by ~123px flips `intersects` to `True` and turns the item red with a negative clearance that is not a defect. The three samples happen to be deterministic today only because `enter_project` reloads the page and every panel starts at `scrollTop = 0` — a property nothing asserts.

**Fix:** judge clipping against the scrollport-visible band rather than the padding box alone, e.g. only assert on rows that are fully inside vertically and record the rest as `info`:

```python
judged = [r for r in rows if r["visible"] and r["intersects"]]
straddling = [r for r in judged if r["clearance"] < CLEARANCE_MIN_PX
              and r["rect"]["top"] < r["padTop"]]   # partially scrolled out, not clipped
```

or simply skip any row whose rect crosses the container's top/bottom padding edge and say so in the label. Whatever the mechanism, the label should not claim to measure clipping when it measures scroll position.

### WR-03: the `#doc-panel` clamp probe hard-codes the CSS clamp with no binding, so a *narrowed* clamp makes it vacuous

**File:** `scripts/check-05-ui-uat.py:1586-1595` (constants + `_doc_panel_declared_width`) and `scripts/check-05-ui-uat.py:1955-1963` (assertion)

**Issue:** The probe's bound is a hand-copied mirror of `frontend/style.css:228`:

```python
DOC_PANEL_W_MIN_PX = 340.0
DOC_PANEL_W_VW = 0.30
DOC_PANEL_W_MAX_PX = 480.0

def _doc_panel_declared_width(viewport_width):
    """`clamp(340px, 30vw, 480px)` 在给定视口宽下的解析值(= 面板宽的声明上界)。"""
    return min(DOC_PANEL_W_MAX_PX, max(DOC_PANEL_W_MIN_PX, DOC_PANEL_W_VW * viewport_width))
```

Nothing binds these to the stylesheet — `_l2_guard_shape` only counts `@media`. Widening the clamp (`clamp(500px, 30vw, 600px)`) fails loudly, which is fine. **Narrowing** it does not: with `clamp(300px, 24vw, 400px)` the probe still compares against 432px at 1440 while the panel is 345.6px, and the assertion passes without ever exercising the L-3 protection it exists to guard. The failure mode is silent and in the direction that loses coverage, which is the same class of defect as `T-idi-06-04`.

**Fix:** derive the triple from the file instead of duplicating it — this repo already has the pattern (`scripts/check-02-contrast.py` reads the token fence). Parse `--doc-panel-w: clamp(<a>, <b>vw, <c>)` out of `STYLE_CSS` and assert the parsed values equal the constants, so drift is a FAIL:

```python
m = re.search(r"--doc-panel-w:\s*clamp\((\d+)px,\s*([\d.]+)vw,\s*(\d+)px\)", text)
ok_true(item, "[static] --doc-panel-w 的 clamp() 参数 == 探针常量",
        m is not None and (float(m.group(1)), float(m.group(2)), float(m.group(3)))
        == (DOC_PANEL_W_MIN_PX, DOC_PANEL_W_VW, DOC_PANEL_W_MAX_PX),
        f"({DOC_PANEL_W_MIN_PX}, {DOC_PANEL_W_VW}, {DOC_PANEL_W_MAX_PX})",
        m.groups() if m else "<MISSING>",
        "本常量是 style.css:228 的镜像;不绑死它,收窄 clamp 会让探针静默失去判别力")
```

## Info

### IN-01: `_idi06_census`'s documented contract is false and its return value has no consumer

**File:** `scripts/check-05-ui-uat.py:1738-1760` (`return data` at 1760; claim at 1741-1742), call site at `scripts/check-05-ui-uat.py:1988`

**Issue:** The docstring states "波次 1 / 2 里调用方一律 info()、不判定(判据属计划 03);波次 3 起 item 9 消费同一份返回值做断言(`clearance` / `hits` 两个数组)" and the function ends with `return data`. Neither is true: item 9 never calls `_idi06_census` — `_idi06_clearance_assert` (`check-05-ui-uat.py:2177`) and `_idi06_hit_assert` (`check-05-ui-uat.py:2211`) each `page.evaluate(_IDI06_CENSUS_JS)` themselves. The only call site (`check-05-ui-uat.py:1988`, inside item 8) discards the return value. Each census evaluation computes both arrays, so item 9 evaluates the same DOM survey six times per run to use one array at a time.

**Fix:** either delete `return data` and correct the docstring to "item 9 自行调用 `_IDI06_CENSUS_JS`", or have `_idi06_clearance_assert` / `_idi06_hit_assert` accept a pre-computed `data` argument and have item 9 call `_idi06_census` once per sample. The second option makes the comment true and removes the duplicated survey.

### IN-02: the `@media` guard's label overstates what it counts

**File:** `scripts/check-05-ui-uat.py:1602-1630`

**Issue:** `count = text.count(MEDIA_QUERY_DECL)` counts the substring `@media` anywhere in `frontend/style.css`, including inside comments, and the assertion label is `"[static] frontend/style.css 的 @media 出现次数 == 决策(被实测推翻 ⇒ 0)"`. The decision it encodes is narrow — "the L-2 narrow-window guard was not written" — but the guard fires on *any* media query. A future `@media (prefers-reduced-motion: reduce)` (an accessibility improvement, unrelated to layout) or a print stylesheet turns this FAIL with a note that sends the fixer to the L-2 decision record in `idi-06-03-SUMMARY.md`. The count is currently 0 (`命中行=[]`), so this is latent.

**Fix:** either narrow the match to the guard's actual shape (e.g. only count `@media` blocks whose condition contains `max-width`), or reword the label to "无任何 @media 声明(本阶段 L-2 决策)" so the failure message describes what is being counted. Prefer the former: the decision is about the narrow-window guard, not about media queries in general.

---

_Reviewed: 2026-09-22T05:42:50Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
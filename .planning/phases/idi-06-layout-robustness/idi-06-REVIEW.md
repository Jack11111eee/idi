---
phase: idi-06-layout-robustness
reviewed: 2026-09-22T07:53:32Z
depth: standard
files_reviewed: 2
files_reviewed_list:
  - frontend/style.css
  - scripts/check-05-ui-uat.py
critical: 0
warning: 4
info: 3
total: 7
status: issues_found
---

# Phase idi-06: Code Review Report (incremental re-review)

**Reviewed:** 2026-09-22T07:53:32Z
**Depth:** standard
**Files Reviewed:** 2
**Status:** issues_found

## Summary

This is a re-review of the current tree (`HEAD` = `f0d7132`), superseding the review at `d6c375c`. Only `scripts/check-05-ui-uat.py` changed since then (`git diff d6c375c..HEAD --stat`: 15 lines, comment/`info()` text only). `frontend/style.css` is byte-identical to the prior review's base — I confirmed with `git diff d6c375c..HEAD -- frontend/style.css` returning empty — so every CSS observation in the prior review still holds verbatim, and the phase's scope lock on `#stream-banner` (:709-723) and `--doc-panel-w` (:224-227) is intact.

**CR-01 is resolved, and I verified the replacement text is true rather than merely less wrong.** The two sites (`scripts/check-05-ui-uat.py:1931-1938` comment, `:1949-1955` `info()`) now say the 768px "无内容遮挡" promise is **not covered** and is a registered known gap. I re-measured the numbers the new text asserts, with a live probe at 768px on a `p1` fixture:

```
h1     = {l: 439, t: 8,  r: 481, b: 28}
header = {l: 429, t: 0,  r: 768, b: 36}
banner = {l: 285.34375, t: 12, r: 482.65625, b: 39}
badge  = {l: 638.96875, t: 7, r: 739.890625, b: 32}
```

Overlap = 42 × 16px, exactly as the comment states, and the band is real and closed at both ends: I swept 768/855/856/857/877/878 and `#stream-banner × #doc-panel-header h1` intersects at 768 **and** 855 but not at 856 — so "相交带 768–855px" is correct, not approximate. The same numbers are registered at `idi-06-UI-SPEC.md:585` (A-10 row), which the comment cites and which does exist. `--item 8` still reports `PASS (13 条断言, 0 FAIL, 0 BLOCKED)`, exit 0. The residual gap itself is **not** re-raised as a finding: it is registered, user-adjudicated (A-10, remediation (b)), and both of its fixes are excluded by the phase's own scope lock.

**WR-01 / WR-02 / WR-03 and IN-01 / IN-02 all still apply unchanged.** They are not fixed, not softened, and not inflated; I re-derived each against the current file and give the current line numbers below (each drifted by a handful of lines). All five are on `scripts/check-05-ui-uat.py`.

**One new finding (WR-04) and one new info item (IN-03).** Chasing WR-03's "the probe loses discriminating power" concern to its root, I found a stronger version of it that WR-03 did not reach: the `#doc-panel` width probe cannot fail on the failure mode it is labelled as catching, because the failure mode is structurally impossible for a scroll container. I proved this by measurement, not inference (details in WR-04). The product behaviour is correct — nothing is broken on screen — so this is a WARNING, not a critical: the gate and two load-bearing CSS comments attribute the correct outcome to a declaration (`min-width: 0`) that is not doing the work.

No security issues in either file. No injection surface is added: every `page.evaluate` argument is passed as an argument (`_IDI06_REACH_JS(sel)`, `WIDE_MD`, `LONG_DOC_MD`, `BANNER_TEXT`), never interpolated into the JS template; the harness has no network listener beyond localhost, no secrets, and no deserialisation.

## Critical Issues

None open. `CR-01` from the prior review is resolved (verified by re-measurement, see Summary). No new critical findings: neither file's current state contains an incorrect product behaviour, a security vulnerability, or a data-loss path.

## Warnings

### WR-01: `_idi06_reach` records a vacuous PASS for "末条内容可达" when the probe content fails to make the container scroll

**File:** `scripts/check-05-ui-uat.py:2134` (precondition) and `scripts/check-05-ui-uat.py:2158-2176` (last-child assertion)

**Issue:** Unchanged from the prior review; line numbers have drifted. The precondition chain rejects only `injected is None`:

```python
if injected is None:
    blocked(item, label, "内容经应用自身的渲染路径注入", "<MISSING>", inject_error)
    return
```

Both call sites pass an integer count, and `0` is not `None`. `item9`'s `#main-pane` probe (`check-05-ui-uat.py:2301-2308`) returns `document.querySelectorAll('#ai-events .event-item').length`; if `renderEvent` ever stops appending (renamed internal, a state guard, a silent exception path) that is `0`, the precondition passes, and then only the *scroll* half is downgraded:

```python
if geo["scrollHeight"] <= geo["clientHeight"]:
    info(f"item9 {label}",
         "容器无需滚动,可达性平凡成立(不记断言,避免空转 PASS)")
```

The last-child half at `:2170-2176` still runs and records **PASS** for a claim that was never exercised: with nothing injected the container does not overflow, so the last child is trivially inside it. The `#latest-check` side (`check-05-ui-uat.py:2318-2324` returning `c.childElementCount`) has the same shape. Note the inconsistency: the sticky-header assertion in item 8 (`check-05-ui-uat.py:1861-1868`) *does* treat "container cannot scroll" as `blocked()`, and the project's own doctrine (stated in this item's comment at `:2119-2122`) is that a missing precondition is BLOCKED, never PASS.

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

**File:** `scripts/check-05-ui-uat.py:2195` and `:2201` (judgement); `scripts/check-05-ui-uat.py:1707-1708` (`intersects`)

**Issue:** Unchanged. `judged` keeps rows where the element is visible *and* intersects the container's padding box:

```python
judged = [r for r in rows if r["visible"] and r["intersects"]]
...
bad = [r for r in judged if r["clearance"] < CLEARANCE_MIN_PX]
```

`intersects` only excludes elements that are **completely** outside the padding box. An element *partially* scrolled out of a scroll container has `intersects == True` and a negative clearance (the offending term is `padBottom - r.bottom`), so it lands in `bad` and FAILs — even though partial visibility is the normal, unavoidable behaviour of every scroll container, and the browser scrolls the element into view when it receives focus. The assertion measures scroll position, not clipping. The margin is thin and the harness prints it: in the current `p3` run, `#btn-authorize × #doc-panel = -122.6px` with `intersects=False` — excluded solely because it sits 122.6px past the bottom edge. Any change that moves it (or scrolls the panel) by ~123px flips `intersects` to `True` and turns the item red with a negative clearance that is not a defect. The three samples are deterministic today only because `enter_project` reloads the page and every panel starts at `scrollTop = 0` — a property nothing asserts.

**Fix:** judge clipping against the scrollport-visible band rather than the padding box alone, e.g. only assert on rows that are fully inside vertically and record the rest as `info`:

```python
judged = [r for r in rows if r["visible"] and r["intersects"]]
straddling = [r for r in judged if r["clearance"] < CLEARANCE_MIN_PX
              and r["rect"]["top"] < r["padTop"]]   # partially scrolled out, not clipped
```

or skip any row whose rect crosses the container's top/bottom padding edge and say so in the label. Whatever the mechanism, the label should not claim to measure clipping when it measures scroll position.

### WR-03: the `#doc-panel` clamp probe hard-codes the CSS clamp with no binding, so a *narrowed* clamp makes it vacuous

**File:** `scripts/check-05-ui-uat.py:1588-1595` (constants + `_doc_panel_declared_width`) and `scripts/check-05-ui-uat.py:1959-1973` (assertion)

**Issue:** Unchanged. The probe's bound is a hand-copied mirror of `frontend/style.css:228`:

```python
DOC_PANEL_W_MIN_PX = 340.0
DOC_PANEL_W_VW = 0.30
DOC_PANEL_W_MAX_PX = 480.0
```

Nothing binds these to the stylesheet — `_l2_guard_shape` only counts `@media`. Widening the clamp (`clamp(500px, 30vw, 600px)`) fails loudly, which is fine. **Narrowing** it does not: with `clamp(300px, 24vw, 400px)` the probe still compares against 432px at 1440 while the panel is 345.6px, and the assertion passes without ever exercising the L-3 protection it exists to guard. The failure mode is silent and in the direction that loses coverage — the same class of defect as `T-idi-06-04`. (WR-04 below shows the probe has a second, independent discriminating-power hole.)

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

### WR-04: the `#doc-panel` width probe is labelled "判别性" but cannot fail on the failure mode it names — `min-width: 0` is inert on a scroll container

**File:** `scripts/check-05-ui-uat.py:1964-1973` (assertion) and `scripts/check-05-ui-uat.py:1568-1576` (the comment that claims discriminating power)

**Issue:** The probe is presented as the L-3 detector, on the stated reasoning that the document-level `scrollWidth` is "结构性失明" to the "flex item pushed wider by long unbreakable content" failure mode while the panel-width read is not:

```python
ok_true(item, f"[@{width}px] #doc-panel 实测宽 <= clamp(340px, 30vw, 480px) 上界",
        m["panelWidth"] <= expected_w + 1.0, ...,
        "L-2 的判别性探针:长不可断内容不得把面板顶得比它声明的宽还宽"
        "(文档级 scrollWidth 对该失效模式结构性失明)")
```

It is not discriminative. `#doc-panel` declares `overflow-y: auto` (`frontend/style.css:478`), so its computed `overflow-x` is also `auto` (`frontend/style.css:1560-1561` already documents this) — the box is a **scroll container**, and per CSS Flexbox §4.5 the automatic minimum size of a scroll container is **zero**. `min-width: 0` (`frontend/style.css:486`) therefore cannot change the used width, and the failure mode the probe names cannot occur. Measured live at 768px on a `p1` fixture with the harness's own `WIDE_MD` injected into `#doc-panel-body` (the probe div carries no `.markdown-body` class, so the six-target `overflow-wrap: anywhere` rule at `frontend/style.css:1322` does not apply — the content really is unbreakable):

| configuration | `#doc-panel` width | computed `min-width` | computed `overflow-x` | doc `scrollWidth`/`clientWidth` |
|---|---|---|---|---|
| as shipped | 340 | `0px` | `auto` | 768 / 768 |
| runtime override `minWidth: auto` | 340 | `auto` | `auto` | 768 / 768 |
| as shipped + a further 4000-char unbreakable token | 340 | `0px` | `auto` | 768 / 768 |
| runtime override `minWidth: auto` + 4000-char token | 340 | `auto` | `auto` | 768 / 768 |

The width is identical in all four rows. The assertion passes for a reason unrelated to the declaration it guards, so a change that removed `min-width: 0` — or one that broke the real mechanism (e.g. flipping `#doc-panel` to `overflow: visible`) while keeping `min-width: 0` — would not be distinguished by it. This is the same shape as the `T-idi-06-04` false-PASS class the phase registered, one level down: not a false PASS on a violated product criterion (the panel really is 340px, and nothing is broken on screen), but a gate that cannot fail for the reason its label gives.

**Fix:** make the probe measure the actual mechanism instead of asserting an invariant that is true for a different reason. Add a positive control that overrides the declaration at runtime (no source edit needed) and asserts the width is *unchanged*, which is what proves the scroll container is doing the work:

```python
control = page.evaluate("""() => {
  const p = document.querySelector('#doc-panel');
  const before = p.getBoundingClientRect().width;
  p.style.minWidth = 'auto';          // 撤掉 L-3 的声明,只在本探针内
  const after = p.getBoundingClientRect().width;
  const ovX = getComputedStyle(p).overflowX;
  p.style.minWidth = '';
  return {before, after, ovX};
}""")
ok_true(item, f"[@{width}px] 撤掉 #doc-panel 的 min-width: 0 后实测宽不变(真正承重的是滚动容器)",
        control["after"] <= expected_w + 1.0 and control["ovX"] != "visible",
        f"<= {expected_w:.1f}px 且 overflow-x != visible",
        f"before={control['before']:.1f} after={control['after']:.1f} overflowX={control['ovX']}",
        "CSS Flexbox §4.5:滚动容器的自动最小尺寸为 0 ⇒ min-width: 0 是惰性声明,"
        "判别力来自 overflow 而非它。本控制组把这条机制变成可证伪的断言")
```

Alternatively, if the declaration is to be kept and defended on its own terms, assert `getComputedStyle(panel).minWidth == '0px'` and reword the label so it no longer claims to catch a failure mode that cannot occur.

## Info

### IN-01: `_idi06_census`'s documented contract is false and its return value has no consumer

**File:** `scripts/check-05-ui-uat.py:1738-1760` (`return data` at `:1760`; claim at `:1741-1742`), call site at `scripts/check-05-ui-uat.py:1997`

**Issue:** Unchanged. The docstring states "波次 1 / 2 里调用方一律 info()、不判定(判据属计划 03);波次 3 起 item 9 消费同一份返回值做断言(`clearance` / `hits` 两个数组)" and the function ends with `return data`. Neither is true: item 9 never calls `_idi06_census` — `_idi06_clearance_assert` (`:2186`) and `_idi06_hit_assert` (`:2220`) each `page.evaluate(_IDI06_CENSUS_JS)` themselves. The only call site (`:1997`, inside item 8) discards the return value. Each census evaluation computes both arrays, so item 9 evaluates the same DOM survey six times per run to use one array at a time.

**Fix:** either delete `return data` and correct the docstring to "item 9 自行调用 `_IDI06_CENSUS_JS`", or have `_idi06_clearance_assert` / `_idi06_hit_assert` accept a pre-computed `data` argument and have item 9 call `_idi06_census` once per sample. The second option makes the comment true and removes the duplicated survey.

### IN-02: the `@media` guard's label overstates what it counts

**File:** `scripts/check-05-ui-uat.py:1602-1628`

**Issue:** Unchanged. `count = text.count(MEDIA_QUERY_DECL)` (`:1619`) counts the substring `@media` anywhere in `frontend/style.css`, including inside comments, and the assertion label is `"[static] frontend/style.css 的 @media 出现次数 == 决策(被实测推翻 ⇒ 0)"`. The decision it encodes is narrow — "the L-2 narrow-window guard was not written" — but the guard fires on *any* media query. A future `@media (prefers-reduced-motion: reduce)` (an accessibility improvement, unrelated to layout) or a print stylesheet turns this FAIL with a note that sends the fixer to the L-2 decision record. I confirmed the count is currently 0 (`grep -n "@media" frontend/style.css` returns nothing; the harness prints `计数=0 命中行=[]`), so this is latent.

**Fix:** narrow the match to the guard's actual shape (e.g. only count `@media` blocks whose condition contains `max-width`), or reword the label to "无任何 @media 声明(本阶段 L-2 决策)" so the failure message describes what is being counted. Prefer the former: the decision is about the narrow-window guard, not about media queries in general.

### IN-03: the two `min-width: 0` comments in `style.css` assert a mechanism that cannot occur on a scroll container

**File:** `frontend/style.css:460-465` (`#main-pane`) and `frontend/style.css:481-486` (`#doc-panel`)

**Issue:** Both comments make the same claim: "`#app` 的两个 flex 子项都是 `min-width: auto` ⇒ flex-basis 不是硬约束,min-width: auto 胜出,长不可断内容能把 `#doc-panel` 顶得比它的 `clamp()` 还宽". That is false for both elements as shipped, because both declare `overflow-y: auto` (`frontend/style.css:458` and `:478`) and are therefore scroll containers whose automatic minimum size is zero (CSS Flexbox §4.5) — the same fact the harness comment at `check-05-ui-uat.py:1571-1573` already states. Measured: with `min-width` overridden to `auto` at runtime, `#doc-panel` stays 340px and `#main-pane` stays 428px at 768px, including with a 4000-char unbreakable token in the panel (see WR-04's table). So the declarations at `:465` and `:486` are inert today, and the comment's conclusion — "看似冗余 …… 不得当作冗余代码删除" — rests on a premise that does not hold; the real reason the declarations are harmless is that they are currently no-ops.

This is Info rather than Warning because there is no product defect and the comment is a deliberate belt-and-suspenders record; the declarations become load-bearing the moment either element stops being a scroll container. It is reported because `frontend/style.css` is scope-locked for this phase, so the only available action is a comment correction, and because a false mechanism in a comment is what stops the next reader from checking.

**Fix:** reword both comment blocks to state the measured position, e.g. "滚动容器的自动最小尺寸为 0(实测:把本行改成 `auto` 后 `#doc-panel` 在 768px 仍是 340px),故本行当前是惰性声明;它保留为防御 —— 一旦 `overflow-y: auto` 被移除,它才成为承重行。" Do not change the declarations (out of scope per the phase's UI-SPEC scope lock).

---

_Reviewed: 2026-09-22T07:53:32Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
---
phase: idi-07-interaction-states-and-focus
reviewed: 2026-09-23T07:46:07Z
depth: standard
files_reviewed: 3
files_reviewed_list:
  - frontend/style.css
  - scripts/check-05-ui-uat.py
  - scripts/probe-07-focus-composite.py
findings:
  critical: 0
  warning: 4
  info: 4
  total: 8
status: issues_found
---

# Phase idi-07: Code Review Report

**Reviewed:** 2026-09-23T07:46:07Z
**Depth:** standard
**Files Reviewed:** 3
**Status:** issues_found

## Summary

Scope was the phase diff only (`git diff d03019842c8d9bb3f41a416e8cf4c94e477a7b64^..HEAD`):
the additive CSS layer in `frontend/style.css` (5 new tier-2 tokens, the rewritten
`button:hover` gate, the 7-selector `:focus-visible` rule, the filled-button
hover/active overlay groups, the input hover-border group, the transition mount rule
and the `prefers-reduced-motion` block), the new UAT item 10 in
`scripts/check-05-ui-uat.py`, and the one-shot `scripts/probe-07-focus-composite.py`.

**No Critical findings.** I found no product-behaviour defect, no security issue and no
data-loss risk. I traced the specificity arithmetic of every new selector, re-derived the
PAIR-manifest counts (52 = 35 TEXT + 17 NON-TEXT + 1 ORDER — the header comment is
accurate), confirmed the `button:hover` rewrite is specificity-neutral (0-1-1 before and
after), confirmed the naive-active / gated-hover pair is a matched pair (runtime:
hover `rgb(240,240,240)` != pressed `rgb(232,232,232)`), and confirmed every filled rule
body in the file is enumerated in the new overlay groups (no recurrence of the D-02
"filled button has no hover feedback" defect). I also re-ran the phase's own probe and
`--item 10` end to end: `item 10: PASS (38 条断言, 0 FAIL, 0 BLOCKED)`, exit 0.

All four Warnings are **gate-integrity** defects rather than product defects, which is
where this phase's risk actually lives: three of them are assertions that cannot fail for
the reason they exist, and one is a manifest-enumeration claim the phase's own new
selector contradicts. Each is backed below by a measured runtime value or a computed
contrast ratio, not by inspection alone.

Method note: everything below was verified against the running application, not read off
the source. I ran `scripts/check-05-ui-uat.py --item 10` (exit 0, 38 assertions) and two
throwaway Playwright sessions that reuse the harness's own helpers (`effective_bg`,
`read_style`, `make_fixture`, `enter_project`) to measure the values quoted in WR-01,
WR-02 and WR-04. No file other than this report was written.

## Narrative Findings (AI reviewer)

### Warnings

#### WR-01: SC4's "scroll to the bottom" premise is a no-op in the only state where SC4 runs

**File:** `scripts/check-05-ui-uat.py:2933-2967` (scroll step 2933-2946; judged set 2958-2967)
**Issue:** SC4 is documented as *"侧栏滚到底再 Tab,环不被裁切"* and its judgement set is
defined as *"滚到底之后每个新 Tab 聚焦到的可见元素"*. The scroll step writes
`el.scrollTop = el.scrollHeight` for `#main-pane` and `#chat-messages` and then records the
triple as `info()` only — it never asserts that either container can actually scroll. SC4 is
invoked exactly once, for the `p1` sample (`item10`, line 3563), and in `p1` **neither
container is scrollable**. Measured (throwaway session, p1, viewport 1440×900):

```
#main-pane      scrollHeight 900  clientHeight 900  overflowY auto
#chat-messages  scrollHeight   8  clientHeight   8  overflowY auto
#doc-panel      scrollHeight 900  clientHeight 900  overflowY auto
```

The harness's own INFO line agrees (`{'#main-pane': [0, 900, 900], '#chat-messages': [0, 8, 8]}`,
`scrollTop` stayed 0 after being set to `scrollHeight`). So the assertion degenerates into a
plain clearance check over the first 12 Tab targets and can never fail for the reason it
exists. This is the same class the file already knows how to catch: `item8` (lines 2165-2172)
blocks with *"内容不足一屏,不可滚 ⇒「滚到底后仍可见」是空转断言,不记 PASS"* on precisely this
condition.

A second gap compounds it: the scroll list is `['#main-pane', '#chat-messages']`, but
`#doc-panel` is the nearest clipping ancestor for 4 of the 11 judged rows in the SC4 run
(three distinct elements — `#enter-path-input` appears twice, plus `#btn-enter` and
`#btn-divergence`) and is itself `overflow-y: auto`. The container that clips those elements
is never scrolled, so "侧栏滚到底" is not achieved for them even in principle.

**Failure scenario:** `#main-pane`'s padding is changed from 40px to 0 (or an element is
added flush against the container edge) *and* the sample is long enough to scroll. SC4's
scroll step still no-ops in `p1`, the newly-Tabbed elements still clear the threshold, and
SC4 reports PASS — while the exact situation the probe is named for (a focused ring clipped
after scrolling to the bottom) goes untested. Today the probe is green because the
containers are not scrollable at all, not because the clearance survives scrolling.

**Fix:** mirror `item8`'s pattern — treat "could not scroll" as no judgement, and add
`#doc-panel` to the scroll list:

```python
scrolled = page.evaluate(
    """() => {
        const out = {};
        for (const sel of ['#main-pane', '#chat-messages', '#doc-panel']) {
          const el = document.querySelector(sel);
          if (!el) continue;
          el.scrollTop = el.scrollHeight;
          out[sel] = [el.scrollTop, el.scrollHeight, el.clientHeight];
        }
        return out;
    }"""
)
scrollable = [s for s, (_top, sh, ch) in scrolled.items() if sh > ch]
if not scrollable:
    blocked(item,
            f"[{state}] SC4 滚到底后每个新 Tab 聚焦元素的 clearance >= {CLEARANCE_MIN_PX:.0f}px",
            "至少一个裁剪容器真的可滚(scrollHeight > clientHeight)",
            f"{scrolled}",
            "容器均不可滚 ⇒「滚到底」是 no-op,本断言退化成普通 clearance 检查,"
            "不记 PASS(item8 对 sticky 表头用的是同一条判据)")
    return
```

### WR-02: the new `--color-border-hover` ground enumeration misses the ground the phase's own eighth selector renders on

**File:** `frontend/style.css:517-523` (new PAIR comment) and `frontend/style.css:1600-1605`
(the rule's own coverage check)
**Issue:** the new pair is justified with *"every input / select sits either on
`--color-surface-page` (the page itself) or on `--color-surface` (inside #doc-panel /
#checks-panel / a .overlay-card)"*, and only those two grounds are enumerated. The same
rule's coverage check names the eighth selector's service object as the `.verdict-note-input`
that `app.js` creates dynamically — and that input is appended to `.verdict-card`
(`frontend/app.js:705`), whose background is `var(--color-surface-warning-subtle)`
(`frontend/style.css:1328`). That is a third, opaque ground, and it is not in the manifest.

Measured ground of the eighth selector's service object (throwaway session, `checking` sample,
card built via the harness's own `_IDI07_BUILD_VERDICT_CARD_JS`):

```
.verdict-card                            background-color = rgb(254, 253, 251)   # amber-1
#idi07-verdict-probe .verdict-note-input  own bg           = rgb(255, 255, 255)
```

Computed with `check-02`'s own resolver/ratio code (no new implementation):

```
--color-border-hover  on --color-surface-warning-subtle : 5.82   (missing from the manifest)
--color-border-hover  on --color-surface                : 5.62   (present)
--color-border-hover  on --color-surface-page           : 5.77   (present)
--color-border-strong on --color-surface-warning-subtle : 3.26   (missing — pre-existing gap, same shape)
```

5.82 clears the 3:1 floor comfortably, so **this is not a live accessibility failure** — it is
an enumeration-completeness defect in a manifest whose stated contract is *"enumerate the
combinations that actually render"* (the exact sentence the phase's new 52-entry header
comment re-asserts). Because `check-02` only measures what the manifest names, the divergence
is invisible to every gate.

Secondary, larger discrepancy on the same claim: five of the eight selectors in the new hover
group draw that border against a **white** field fill, not against the container surface,
because no `input` in this app declares a `background` and Chrome's UA `field` colour is
`rgb(255,255,255)`. Measured own-backgrounds: `#project-path-input`, `#enter-path-input`,
`#message-input`, `#confirm-word-input`, `.verdict-note-input` = `rgb(255, 255, 255)`;
`#check-switcher`, `#round-switcher`, `#ai-route-select` = `rgb(249, 249, 249)` (they declare
`background: var(--color-surface)`). `--color-border-hover` on white is 5.92 and
`--color-border-strong` on white is 3.32, so both still pass — again a modelling gap, not a
contrast failure.

**Failure scenario:** a later change moves `--color-surface-warning-subtle` (amber-1) toward
`--color-surface` or darkens the card, or the white UA field fill is replaced by a token. The
manifest has no entry on either ground, so `check-02` stays green while the control boundary
that identifies the note input drops below 3:1.

**Fix:** add the missing ground (and either add the field-fill ground or register it as a known
deviation, which is this file's established way of handling an enumeration it does not model):

```css
  /* the input controls' hover boundary (INTERACT-01 / D-10): … three grounds —
     --color-surface-page, --color-surface, and --color-surface-warning-subtle
     (.verdict-card, the ground of app.js's dynamic .verdict-note-input). */
  /* PAIR --color-border-hover ON --color-surface-page NON-TEXT */
  /* PAIR --color-border-hover ON --color-surface NON-TEXT */
  /* PAIR --color-border-hover ON --color-surface-warning-subtle NON-TEXT */
```

#### WR-03: two of the eight selectors in the new input hover group omit the `:where(:not(:disabled))` gate the group's own docstring declares mandatory

**File:** `frontend/style.css:1618` and `frontend/style.css:1620` (group at 1614-1623;
docstring claim at 1607-1610)
**Issue:** the group's docstring states that `:not(:disabled)` on the input / select family is
*"**防御性写法** … 它不依赖「今天恰好没有」,将来给输入框加禁用态时仍能兜住,**不得当作冗余代码删除**"*.
Six of the eight selectors carry the gate; `#enter-form input[type="text"]:hover` and
`#confirmation-modal input[type="text"]:hover` do not:

```css
#enter-form input[type="text"]:hover,             /* 1618 — no gate */
#confirmation-modal input[type="text"]:hover {    /* 1620 — no gate */
  border-color: var(--color-border-hover);
}
```

So the future-proofing the comment claims exists for "input / select" holds for 6 of 8, and the
two exceptions are the two controls a disabled-state feature is most likely to touch
(`#enter-path-input` gates the whole entry flow; `#confirm-word-input` is already manipulated
programmatically by `app.js:530`). Today no input is ever disabled (`confirmWordInput.disabled`
is never set anywhere), so this is latent, not live.

**Failure scenario:** a later phase adds `disabled` to `#enter-path-input` while the app is
busy. `#project-path-input` and the other six controls correctly keep their resting border;
`#enter-path-input` still paints `--color-border-hover` on hover, i.e. the D-07-class defect
(a disabled control that still responds to hover) survives on exactly the two selectors the
group forgot. Conversely, a future reader who trusts the docstring may delete the six gates as
redundant, restoring the defect on all eight.

**Fix:**

```css
#enter-form input[type="text"]:where(:not(:disabled)):hover,
#confirmation-modal input[type="text"]:where(:not(:disabled)):hover,
```

#### WR-04: nothing asserts `outline-offset`, so the "geometry is bidirectionally bound to `CLEARANCE_MIN_PX`" contract has no mechanical guard

**File:** `scripts/check-05-ui-uat.py:1809-1812` (`FOCUS_RING_WIDTH_PX` / `FOCUS_RING_OFFSET_PX`),
`scripts/check-05-ui-uat.py:2816-2820`, `scripts/check-05-ui-uat.py:2920-2921`,
`scripts/check-05-ui-uat.py:2968-2977`; `frontend/style.css:1478-1480` and `1499-1500`
**Issue:** both the CSS comment (*"几何是双向绑定的:… 改几何即改那个门的阈值,两者不是两件事"*) and
the SC4 docstring (*"几何 `2px` + `outline-offset: 2px` 是本探针的**前提**:环的外伸量恰为 4px,
故判据取 `CLEARANCE_MIN_PX`"*) state that the ring geometry and the clearance threshold are one
fact. The width half is asserted at runtime (`FOCUS_RING_WIDTH_CSS == "2px"`, SC1 and the
census). The offset half is asserted **nowhere**: `outline-offset` is never read from the
browser — `FOCUS_RING_OFFSET_PX` occurs only inside two failure-note f-strings (lines 2819 and
2976), and `_IDI07_TAB_READ_JS` / `_IDI07_TAB_CLEARANCE_JS` return only `outlineWidth` /
`outlineColor`.

**Failure scenario:** change `frontend/style.css:1500` from `outline-offset: 2px` to
`outline-offset: 0`. Every assertion in item 10 still passes — the census and SC1 read
`outline-width == "2px"` (unchanged), and SC4 measures `40px >= CLEARANCE_MIN_PX 4.0` (the
measured clearances are 40 and 130, so a 2px change in the true overhang cannot move them).
The ring's real overhang is now 2px while `CLEARANCE_MIN_PX` still encodes 4px, so the gate's
threshold no longer describes the geometry it claims to protect, and the next tightening of any
container padding will be judged against the wrong constant. The reverse mutation (widening the
ring) *is* caught by SC1 — only the offset is unguarded.

**Fix:** assert the offset alongside the width, in SC1 (the moment the ring is actually read):

```python
    ok(item,
       f"[{state}] SC1 Tab 到 {hit['label']} 的 outline-offset == "
       f"{FOCUS_RING_OFFSET_PX:.0f}px(= CLEARANCE_MIN_PX - 环宽)",
       f"{FOCUS_RING_OFFSET_PX:.0f}px", hit["outlineOffset"],
       "改几何即改 CLEARANCE_MIN_PX 的阈值 —— 两者不是两件事")
```

with `outlineOffset: s.outlineOffset` added to the `_IDI07_TAB_READ_JS` payload (the payload is
the single source of the focus reading; do not add a second `read_style` path).

### Info

#### IN-01: static guard 1 (`:focus-visible` count >= 1) counts comment mentions, so it cannot fail while the prose survives

**File:** `scripts/check-05-ui-uat.py:3379-3389`
**Issue:** `fv_count = text.count(":focus-visible")` is taken over the whole file including
comments. Verified on the current file: `计数=9(含注释提及)命中行=[239, 1469, 1492, 1493, 1494,
1495, 1496, 1497, 1498]` — lines 239 and 1469 are comment prose, so **2 of the 9** occurrences are
not code. Deleting the entire rule (lines 1492-1501) leaves `fv_count == 2 >= 1` → still PASS.
The INFO line discloses "含注释提及", but the assertion's label does not, and the phase's own
discipline (guard 3, lines 3419-3427) is to write such limitations into the assertion.
**Mitigation that keeps this at Info:** deleting the rule also empties `_idi07_focus_rule_blocks`,
so guard 2 turns BLOCKED (`一条规则块都切不出来 ⇒ 本断言无判定对象`) and item 10 is not green.
**Fix:** count only code occurrences — the helper already exists:
`fv_count = sum(1 for _, buf in _idi07_focus_rule_blocks(text) for _, code in buf if ":focus-visible" in code)`
or simply `len(_idi07_focus_rule_blocks(text)) >= 1`.

#### IN-02: `FOCUSABLE_SELECTOR` is declared but never used — the "single sync point" it documents does not exist

**File:** `scripts/check-05-ui-uat.py:1806` (declaration; the only other mentions are comments at
1909 and 2779)
**Issue:** the constant is introduced with *"焦点规则的枚举集。**逐字**等于上面 `_IDI06_CENSUS_JS` 里
`document.querySelectorAll(...)` 的那一串"* and the CSS comment (`frontend/style.css:1473-1476`)
promises the two sides "必须**同时**改". In fact the selector list is written out as a literal in
three places that are mechanically independent: `frontend/style.css:1492-1498`,
`_IDI06_CENSUS_JS` (lines 1756-1758) and `_IDI07_FOCUS_CENSUS_JS` (lines 1950-1951). The constant
consumes none of them, so editing it changes nothing — a maintainer who follows the comment's
instruction and adds a selector to `FOCUSABLE_SELECTOR` will believe the gate is in sync while
the census still enumerates the old set. (The three literals do agree today; I verified them
character by character.)
**Fix:** build the JS strings from the constant, e.g. interpolate `repr(FOCUSABLE_SELECTOR)` into
both census scripts' `document.querySelectorAll(...)` call, so the constant is the one place the
JS side is written down.

#### IN-03: the specificity arithmetic for the two `input[type="text"]` hover selectors is wrong in the load-bearing comment

**File:** `frontend/style.css:1594-1598`
**Issue:** the comment says *"`#enter-form input[type="text"]` 与 `#confirmation-modal
input[type="text"]` 各 1-1-1,与既有规则**同特异性**,靠源码顺序取胜(本规则在文件末尾)"*. Both
selectors actually compute to **(1,2,1)** — one ID, two class-level components
(`[type="text"]` + `:hover`), one type — while the rules they override
(`frontend/style.css:825-832`, `1263-1271`) are (1,1,1). They win on specificity, not on source
order, so the stated mechanism is false. The other six entries in the same list are computed
correctly (`1-1-0` for the four ID+`:hover` pairs, `1-1-1` for `#chat-input-row input`,
`0-2-0` for `.verdict-note-input`).
**Fix:** correct the two entries to `1-2-1` and drop the "靠源码顺序取胜" clause for them. The
rendered behaviour is correct either way (verified: `#message-input` hover border
`rgb(141,141,141)` → `rgb(100,100,100)`); only the comment is wrong — which matters in a file
whose comments are treated as the contract.

#### IN-04: `probe-07` swallows non-`require` failures, contradicting its own "which one is written to stderr" promise

**File:** `scripts/probe-07-focus-composite.py:237-238` and `252-254`
**Issue:** the docstring promises *"1 = 任一条不成立(哪一条写到 stderr)"*, but the only thing that
writes to stderr is `require()` (line 92). Every other `SystemExit` raised inside the `try` block
is caught by `except SystemExit as e: failures.append(str(e))` and `str(e)` is **never printed** —
`if failures: return 1` produces exit code 1 with an empty stderr. Concretely, a missing sample
(`make_fixture("archive", tmp_root)` → `SystemExit("ERROR: 状态样本不存在: …")`, raised from the
imported harness) exits 1 silently, and the operator cannot tell a failed assertion from a
missing fixture. `ensure_server()` (line 146) is called outside the `try`, so its `SystemExit`
leaks the temp directory before propagating.
**Fix:**

```python
    except SystemExit as e:
        print(f"PROBE FAILED: {e}", file=sys.stderr, flush=True)
        failures.append(str(e))
```

---

_Reviewed: 2026-09-23T07:46:07Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
---
phase: idi-04.1-radix
reviewed: 2026-09-19T13:40:00Z
depth: standard
files_reviewed: 3
files_reviewed_list:
  - frontend/style.css
  - scripts/check-01-token-conformance.sh
  - scripts/check-05-ui-uat.py
findings:
  critical: 2
  warning: 4
  info: 3
  total: 9
status: issues_found
---

# Phase idi-04.1: Code Review Report

**Reviewed:** 2026-09-19T13:40:00Z
**Depth:** standard
**Files Reviewed:** 3
**Status:** issues_found

## Summary

The value layer itself is in good shape. I verified the phase's structural claims
mechanically rather than by reading the diff:

- **No reordering.** Extracting every rule-opener outside the token fence from
  `a1a237c^` and from `HEAD` yields 158 selectors on both sides and `diff` is
  empty. The append-only rule (Hard Rule 3) holds — `.chat-ai` still follows
  `.chat-bubble`, and `.annotation-answered .annotation-note` is still last.
- **No broken or dead tokens.** Every `var(--x)` referenced outside the fence
  resolves to a token declared inside it, and every declared token has at least
  one consumer. Zero drift in both directions.
- **Manifest is self-consistent.** 43 `PAIR` + 1 `ORDER`; every name in the
  manifest is declared in the fence. `check-02-contrast.py` passes 43/43.
- **Scope discipline holds.** `frontend/app.js`, `frontend/index.html` and
  `frontend/vendor/` are untouched in the range; `frontend/vendor/` still holds
  only `marked.min.js`. No bare `#hex` or `rgba()` outside the fence.
  `--shadow-overlay` and its `.overlay-card` consumer landed in the same commit
  (`00c6073`), satisfying Hard Rule 5.
- **`check-01`'s radix repair is real.** Mutation-tested: `var(--radix-gray-11)`
  outside the fence now fails the guard, and a deleted `END` marker fails the
  fence-pair assertion.

The problems are all in the **guard layer**, and two of them are the exact
failure class this project has on record: a guard that keeps printing PASS while
checking nothing. `check-05-ui-uat.py` replaced ~25 hard-coded `rgb()` literals
with `resolve_color(page, "--token")` (D-14). That removes the false-FAIL risk
the phase set out to remove, but it silently removes the guard's ability to fail
at all: when a token is renamed, **both** sides of the comparison degrade to the
same inherited value. I confirmed this in a real Chromium, not by reasoning.

## Critical Issues

### CR-01: `resolve_color()` makes ~25 `check-05` assertions vacuous under a token rename

**File:** `scripts/check-05-ui-uat.py:250-262` (definition), consumed at
`:600-685` (item 3), `:727-728` / `:777-778` (item 4), `:803-826` (item 5),
`:983-984` (item 6), `:1002-1005` (`item_smoke`)

**Issue:** `resolve_color` resolves a token by setting `color: var(--t)` on a
probe div appended to `<body>`. If `--t` is **not declared**, that declaration is
invalid at computed-value time, so the probe inherits its parent's `color` — and
so does the real consumer, which is `var(--t)` too. Both sides of
`ok(expected=resolve_color(...), actual=read_style(...))` become the same
inherited value and the assertion **PASSES**.

This is the "guard goes silently vacuous after a rename" failure class that plan
02 existed to repair, reintroduced into `check-05` by this phase's own D-14 edit.
Before D-14 the literal form (`"rgb(106,106,106)"`) failed loudly on a rename;
after D-14 it cannot.

Empirically reproduced in Chromium (`.venv/bin/python`, bundled revision 1243),
with `--color-text-muted` deliberately undeclared:

```
body color          : rgb(32, 32, 32)
.hint computed      : rgb(32, 32, 32)
resolve_color probe : rgb(32, 32, 32)
=> assertion (hint == probe) would: PASS
=> literal 'rgb(106,106,106)' would: FAIL
```

Also reproduced for the `border-top-color` form (`#ai-route-select`'s
`border: 1px solid var(--color-border-strong)` falls back to `currentColor`,
which is `var(--color-text)` from the `button, input, select` rule — identical to
the probe's inherited value → PASS) and for the `color` form on `#state-badge`.

Affected assertions (a rename/removal of the named token makes each of these
report PASS while rendering is broken):

| item | assertion | token |
|---|---|---|
| 3 | `.hint color` | `--color-text-muted` |
| 3 | `#ai-route-select` / `#selection-menu` `border-top-color` | `--color-border-strong` |
| 3 | `#stream-banner border-top-color` | `--color-action-warning` |
| 3 | `.kind-write` / `.kind-done` `.event-kind background-color` | `--color-kind-write` / `--color-kind-done` |
| 3 | `.chat-user background-color` | `--color-surface-user` |
| 3 | `#btn-authorize color` / `border-top-color` | `--color-action-irreversible-fg` / `--color-action-irreversible` |
| 3 | `#state-badge color` | `--color-text-info` |
| 3 | `.badge-answered color` | `--color-text-muted` |
| 4 | `#brainstorm-view h2 color` | `--color-action-warning` |
| 4 | `[archive] #btn-enter color` | `--color-text` |
| 5 | `#ai-route-select` border / background, `.hint` color, `#stream-banner` border, `.markdown-body color` | 5 tokens |
| 6 | `.annotation-note` / `.annotation-answer-body color` | `--color-text-muted` |
| smoke | `#state-badge color` | `--color-text-info` |

(For the record, `background-color` assertions still have teeth — an undeclared
token makes `background-color` fall back to `rgba(0,0,0,0)` while the probe
returns the inherited text colour, so those correctly FAIL. `resolve_token()` is
also safe: it returns `None` for an undeclared token, which `ok()` records as
BLOCKED. `resolve_color` is the only unsafe resolver.)

**Fix:** Make `resolve_color` return `None` when the token is not declared, so
`ok()` records BLOCKED instead of a false PASS. Validated in the same browser:

```python
def resolve_color(page, token):
    """把令牌解析成归一化的 computed rgb —— 挂一个探针元素读它的 color。

    令牌未声明时返回 None(而非继承色):否则探针与消费者会退化成同一个
    继承值,断言恒真。ok() 对 None 记 BLOCKED,绝不记 pass。
    """
    return page.evaluate(
        """(t) => {
            const v = getComputedStyle(document.documentElement).getPropertyValue(t);
            if (!v || !v.trim()) return null;
            const p = document.createElement('div');
            p.style.color = `var(${t})`;
            document.body.appendChild(p);
            const c = getComputedStyle(p).color;
            p.remove();
            return c;
        }""",
        token,
    )
```

Verified: declared token → `rgb(100, 100, 100)`; undeclared token → `None`.

### CR-02: the "发送" AI smoke assertion passes without waiting for the AI call

**File:** `scripts/check-05-ui-uat.py:873-883` (`wait_done`), `:917-933` (send
branch of `run_ai_smoke`)

**Issue:** `wait_done(selector)` returns `True` as soon as
`el.disabled === false`. That is the correct predicate for
`#btn-process-round` (`app.js:1178` drives it from `processInFlight`), but
`#btn-send` is **never disabled during streaming** — `app.js` only ever sets
`sendBtn.disabled = true` in `applyArchiveView` (`app.js:834`), i.e. in the
read-only archive state, and never around `sendMessage()`.

So on the send branch `wait_done("#btn-send")` returns `True` on the first poll,
microseconds after `page.click`. The subsequent `ok_true(..., not errors, ...)`
then evaluates an `errors` list that has not had time to collect anything, and
records **PASS**. The 90 s deadline is dead code on this path; the assertion
reports success even when the AI call 4xx/5xx's or the page throws. It is a
false-PASS guard, which is the same class as CR-01.

**Fix:** Don't use `disabled` as the completion signal for a button the app never
disables. Either poll for the observable outcome, or make the wait explicit:

```python
# 发送没有 disabled 生命周期(app.js 只在归档态 disable #btn-send),
# 故不能用 wait_done;改为等待本轮流结束的可见信号 + 固定观察窗。
page.click("#btn-send", timeout=15000)
deadline = time.time() + 90
while time.time() < deadline:
    if not page.evaluate("() => document.querySelector('#btn-send').disabled") \
       and page.evaluate("() => !!document.querySelector('.chat-ai.streaming-ai')") is False \
       and page.evaluate("() => !!document.querySelector('#chat-messages .chat-ai')"):
        break
    time.sleep(1.0)
else:
    blocked(item, "[p12] 交互冒烟「发送」", "无错误完成", "超时(90s)",
            "claude CLI 不可用或超时")
```

At minimum, the current code should assert that the wait actually waited
(`if done and elapsed < 2: blocked(..., "wait_done 立即返回 —— 该选择器没有 disabled 生命周期")`),
so the next reader cannot mistake this for a real wait.

## Warnings

### WR-01: `check-01` tier-1 alternation misses `var( --radix-… )` with whitespace

**File:** `scripts/check-01-token-conformance.sh:41-43`

**Issue:** The pattern requires `var(--` with no space. CSS allows whitespace
after `var(`, so `var( --radix-gray-11 )` is a valid tier-1 leak that the guard
does not see. Mutation-tested against a copy of the repo:

```
=== M3 var( --radix-gray-11 ) spaced ===
PASS
```

(The unspaced form is correctly caught — `M2 var(--radix-gray-11)` → FAIL. So the
radix repair itself works; this is a residual gap in the same regex.)

**Fix:** Allow optional whitespace and use a word boundary so the family name
cannot be matched as a prefix of an unrelated token:

```bash
prim=$(printf '%s\n' "$outside" \
  | grep -oE 'var\(\s*--(white|black|gray|green|blue|amber|red|purple|radix)(-[0-9]+)?' \
  | wc -l | tr -d ' ' || true)
```

### WR-02: `check-01`'s fence assertion guards the marker *pair*, not its *position*

**File:** `scripts/check-01-token-conformance.sh:17-27`

**Issue:** The script asserts exactly one `START` and one `END` and its comment
claims this protects against a marker going missing. It does not protect against
the marker being **relocated**: if `END` is moved to EOF, `awk`'s `f` stays `1`
for the whole file, `$outside` becomes empty, and both scans report `0`. The
guard prints PASS for a file containing an obvious violation. Mutation-tested:

```
=== M4b: leak before relocated END ===
PASS
```

(The genuine removal case is caught — `M6 deleted END` → `FAIL: expected exactly
1 fence START and 1 fence END, found 1/0` — so this is narrower than "the fence
check is broken", but the guard's own comment overstates its coverage, and the
project's recorded failure class is exactly "vacuously green".)

**Fix:** Assert the fence encloses only the `:root` block, so a relocated marker
cannot make the scan vacuous:

```bash
# 围栏必须紧贴 :root —— 否则 END 被挪到文件末尾会让两次扫描都退化成 0。
[ "$(sed -n "$(( $(grep -n '===== DESIGN TOKENS: START' frontend/style.css | cut -d: -f1 ) + 1 ))p" \
       frontend/style.css)" = ":root {" ] \
  || { echo "FAIL: fence START is not immediately followed by ':root {'"; exit 1; }
```

### WR-03: contrast manifest is missing `--color-text ON --color-surface-mark`

**File:** `frontend/style.css:279-341` (manifest), `:904-910` (the consumer)

**Issue:** The manifest header states the contract as "enumerate the combinations
that actually render" (D-15). `#round-doc mark` and `.markdown-body mark` set
`background: var(--color-surface-mark)` and inherit `color: var(--color-text)`
from `.markdown-body` — so body text on the amber-3 mark ground is a combination
that renders, and no `PAIR --color-text ON --color-surface-mark` entry exists.
Only the two `--color-action-warning ON --color-surface-mark` entries are present.
The ratio is high (~15:1, so nothing fails today), but the manifest's stated
completeness is what `check-02` is built on, and this is the one ground in the
file where body text is neither enumerated nor covered.

**Fix:** Add next to the other `--color-text` grounds (after
`/* PAIR --color-text ON --color-surface-warning-subtle TEXT */`):

```css
  /* mark 高亮底:正文落在 amber-3 上(§4.1「高亮 = 有批注」) */
  /* PAIR --color-text ON --color-surface-mark TEXT */
```

### WR-04: `item_smoke` "可见" assertion passes when the element is absent

**File:** `scripts/check-05-ui-uat.py:996-997`

**Issue:** `ok_true(item, "smoke #state-badge 可见", read_style(page, "#state-badge", "display") != "none", ...)`.
`read_style` returns `None` when the selector does not match, and `None != "none"`
is `True`, so a missing `#state-badge` is reported as **visible**. This is the
only assertion in the file with this shape — `item1` does it correctly
(`own_visible = disp is not None and disp != "none"`, `:404-405`) — so it is an
inconsistency as well as a hole, and it sits in the harness self-check whose job
is to prove the wiring works at all.

**Fix:**

```python
disp = read_style(page, "#state-badge", "display")
ok_true(item, "smoke #state-badge 可见", disp is not None and disp != "none",
        "display!=none", disp)
```

## Info

### IN-01: `goto_frozen_round` takes an `item` parameter it never uses

**File:** `scripts/check-05-ui-uat.py:477-480`

**Issue:** `def goto_frozen_round(page, item):` never references `item`; both call
sites (`:538`, `:765`) pass it. Dead parameter.

**Fix:** `def goto_frozen_round(page):` and drop the argument at both call sites.

### IN-02: the send-smoke row is labelled `[p3]` on one path and `[p12]` on the other

**File:** `scripts/check-05-ui-uat.py:845` vs `:926-930`

**Issue:** Without `--ai-smoke` the placeholder row is
`"[p3] 交互冒烟「发送」"`; with `--ai-smoke` the real row is
`"[p12] 交互冒烟「发送」"`. Same acceptance item, two labels — grepping the log
for either string silently misses the other run mode.

**Fix:** Use `"[p12] 交互冒烟「发送」"` at `:845` (p12 is where the smoke actually
runs, per the comment at `:917`).

### IN-03: a default `check-05` run can never exit 0

**File:** `scripts/check-05-ui-uat.py:842-847`, `:1124-1127`

**Issue:** Item 5 unconditionally emits two BLOCKED rows unless `--ai-smoke` is
passed, and `main()` maps any BLOCKED to exit 2. A default run therefore always
reports `exit=2`, so "all six items green" is not an expressible outcome and any
CI gate keyed on `exit == 0` is permanently red. Documented behaviour, but it
means the exit code cannot be used as a pass/fail signal for the default run.

**Fix:** Either treat the two skipped AI smokes as a distinct `SKIPPED` verdict
that does not force exit 2, or gate them behind `--item 5` so a plain run of
items 1-4/6 can exit 0.

---

_Reviewed: 2026-09-19T13:40:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
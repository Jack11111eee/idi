---
phase: idi-04.1-radix
reviewed: 2026-09-20T02:35:38Z
depth: standard
files_reviewed: 2
files_reviewed_list:
  - scripts/check-05-ui-uat.py
  - scripts/probe-05-resolve-color.py
findings:
  critical: 0
  warning: 2
  info: 3
  total: 5
status: issues_found
---

# Phase idi-04.1 (incremental re-review): Code Review Report

**Reviewed:** 2026-09-20T02:35:38Z
**Depth:** standard
**Files Reviewed:** 2
**Status:** issues_found

## Summary

Incremental review scoped to gap-closure plan `idi-04.1-04` (commits `f06b1d8` +
`ff0e95c`). Prior plans 01–03 were reviewed in the previous revision of this file
(`git show 7cc1d17:…`); the deferred set W-2…W-6 / CR-02 / IN-01…IN-03 was treated
as out of scope and is not re-reported.

**No Critical finding. CR-01 is genuinely closed.** I re-derived the fix from the
diff rather than from the SUMMARY:

- `resolve_color` (`:258-278`) now reads
  `getComputedStyle(document.documentElement).getPropertyValue(t)` and returns
  `null` before building the probe div. The probe body below the two added lines
  is byte-identical to `68309d0`, so the declared-token path is unchanged, and
  appending/removing a `<div>` on `<body>` cannot alter `:root`'s computed custom
  properties — moving the read earlier is behaviour-neutral for declared tokens.
- `ok()` (`:115-122`) puts `expected is None` **before** `actual is None`, so a
  `None` expectation can no longer reach `norm(actual) == norm(None)` and be
  recorded FAIL. `_emit`'s 6-argument call shape is correct; `ok_contains` /
  `ok_true` / `item_verdict` are untouched and unaffected.
- `PREFIX_PROBE_JS` (`probe:50-57`) is **byte-identical** to `68309d0`'s probe
  body (checked with `git show 68309d0:scripts/check-05-ui-uat.py`), so the
  counterfactual is a faithful counterfactual. Computing the pre-fix verdict with
  the post-fix `ok()` is sound: `pre_fix_expected` is a string, so the new branch
  cannot fire on that path.
- Importing the harness has **no** top-level side effects (`ROWS = []` and path
  constants only; `main()` is `__main__`-guarded), so the probe's
  `spec_from_file_location` reuse is safe. The only import-time write is a
  gitignored `scripts/__pycache__/*.pyc`.

**Verified sound — claims I tried to falsify and could not:**

- *"No call site passes `None` expected for a reason other than an unresolvable
  token."* True. Every `None`-capable expected argument comes from `resolve_color`
  or `resolve_token` (harness `:604-608`, `:660-665`, `:713`, `:766-768`,
  `:791`, `:819-835`, `:842`, `:989`, `:1015-1016`, `:1024`); the remaining
  expected arguments are string literals (`"none"`, `"6px"`, `"1"`,
  `"saturate(0.6)"`, …). No call site passes a literal `None`.
- *"`resolve_color`'s empty check ≡ token undeclared."* Not literally equivalent —
  a declared-but-empty (`--x: ;`, `--x: initial`) token also returns `null` — but
  that is the correct call, because such a token is invalid at computed-value time
  and would otherwise re-enter the very degeneration CR-01 fixed. The BLOCKED note
  ("令牌未声明或期望值解析失败") covers both. Dismissed.
- *Both-`None` call sites now get a misleading note.* Where expected **and** actual
  are `None`, the note flips from "元素/选择器不存在" to "令牌未声明"; the **verdict
  stays BLOCKED** either way, so no verdict changed. Message-only, not a finding.
- *"24 call sites and all expected values unchanged."* Confirmed by `git show
  f06b1d8`; only `ok()`, `resolve_color` and the docstring's exit-code-2 gloss
  (`:42`) moved.
- *Scope:* the probe is referenced by nothing else in the tree (grep over
  `scripts/`, `.planning/`, config); it does not enter the four guard commands'
  contract. Its mutation never touches the working tree — `frontend/style.css:120`
  is the only `--color-text-muted:` declaration (`grep -c` = 1), and it sits alone
  on its line.

What the happy-path runs do **not** prove is where I found the two warnings: the
proof's own self-validation (WR-01) and the verdict-tier change that CR-01's fix
carries into `resolve_token` call sites (WR-02).

## Critical Issues

None. The fix does what VERIFICATION.md's CR-01 gap required, and I could not
construct a mutation of the token layer under which the repaired assertions return
to PASS *without* another guard in the suite failing (see IN-01).

## Warnings

### WR-01: the probe cannot tell its own mutation apart from "the stylesheet never loaded"

**File:** `scripts/probe-05-resolve-color.py:81-97` (handler), `:95` (`fulfill`),
`:114-193` (PASS A)

**Issue:** `route.fulfill(response=resp, body=mutated)` reuses the *original*
response's headers, including `content-length`. In Playwright's client,
`_inner_fulfill` copies `response.headers` when no `headers` argument is given
(`.venv/lib/python3.13/site-packages/playwright/_impl/_network.py:430-437`) and
then only fills `content-length` **if it is absent** (`:471`). The mutated body is
shorter than the original stylesheet, so the fulfilled response advertises a
length it does not deliver. Two consequences:

1. A mismatched `content-length` is a load-rejection trigger in Chromium
   (`ERR_CONTENT_LENGTH_MISMATCH`). Today it is tolerated — see the evidence
   below — but nothing in the probe would notice if a future Chromium/Playwright
   combination started rejecting it.
2. **More importantly, the probe would still print all four `PROBE …` lines and
   exit 0 in that world.** If the stylesheet never applied, `.hint` has no colour
   rule and inherits `<body>`'s colour, and so does the pre-fix probe div
   (`PREFIX_PROBE_JS`), so `require(pre_fix_expected == hint_computed)` passes →
   `mutated-prefix-verdict=PASS`; `resolve_color` then finds the token undeclared →
   `mutated-postfix-verdict=BLOCKED`; and PASS B runs without a route → `PASS`.
   The three-line "proof" is byte-identical for the intended mechanism and for
   "the mutated stylesheet failed to load at all", i.e. the probe cannot
   distinguish "the token was deleted" from "the CSS was not applied".

**Evidence that it works today** (so this is a robustness/diagnostic gap, not a
current failure): the recorded PASS A values are
`pre_fix_expected=rgb(32, 32, 32)` / `hint_computed=rgb(32, 32, 32)`. `rgb(32, 32,
32)` is `#202020` = `--radix-gray-12` = `--color-text`, applied by
`frontend/style.css:345-351` (`html, body { color: var(--color-text) }`). An
unstyled page would inherit Chromium's UA default `rgb(0, 0, 0)`, not
`rgb(32, 32, 32)`; so the mutated stylesheet did load and did apply. The proof
stands — it is the *future* silence that is unguarded.

**Fix:** (a) drop the stale header, and (b) add a positive control in PASS A that
the mutated stylesheet is otherwise intact:

```python
    def handler(route):
        resp = route.fetch()
        original = resp.body().decode("utf-8")
        mutated = "".join(
            ln for ln in original.splitlines(keepends=True) if f"{TOKEN}:" not in ln
        )
        seen["original"] = original
        seen["mutated"] = mutated
        # 复用原响应头会带上原 content-length(Playwright 只在缺该头时才回填),
        # 而变异后的 body 更短 —— 显式去掉,避免把「长度不符」交给浏览器裁决。
        headers = {k: v for k, v in resp.headers.items() if k.lower() != "content-length"}
        route.fulfill(response=resp, headers=headers, body=mutated)
```

```python
        # PASS A 的正对照:变异只删了一个声明,样式表其余部分必须仍在生效。
        # 没有它,「样式表根本没加载」这一世界会产出同样的三行 PROBE。
        require(
            h5.resolve_color(page, "--color-text") is not None,
            "变异页上 --color-text 未声明 —— 样式表可能根本没加载,"
            "本条证明无法区分「删了令牌」与「CSS 没生效」",
        )
```

### WR-02: `ok()`'s new branch also re-buckets `resolve_token` expectations from FAIL to BLOCKED

**File:** `scripts/check-05-ui-uat.py:115-116` (new branch), affected sites
`:766-776` (item 4) and `:1024-1026` (`item_smoke`)

**Issue:** the new branch is keyed on `expected is None` **regardless of which
resolver produced it**. `resolve_color` never returned `None` before, so for its
24 call sites the change is PASS→BLOCKED (the intended repair). But
`resolve_token` already returned `None` for an undeclared/empty token, and those
expectations previously fell through to the comparison branch and were recorded
**FAIL** (`norm("10") == norm(None)` → `False`). After this commit a deleted
`--z-badge` / `--z-selection-menu` / `--z-banner` yields **BLOCKED** at four call
sites, i.e. a genuine wiring defect moves from the "值不相等" bucket (exit 1) to
the same bucket as the two by-design AI-smoke skips (exit 2), and the per-item
headline `item 4: BLOCKED (24,0,1)` reads like an environment gap rather than a
broken token.

The docstring at `:105-109` argues the FAIL→BLOCKED reframing explicitly for the
`resolve_color` case, but the four `resolve_token` sites are collateral: the
plan's mandate ("使 `ok()` 记 BLOCKED 而非假 PASS") is about the *false PASS*, not
about re-bucketing a pre-existing FAIL. Scope is narrow and BLOCKED is not a false
PASS, so this is not Critical — but it is an unregistered behaviour change to an
existing verdict, and it is the one place where this commit makes a guard *less*
loud rather than more.

**Fix:** keep BLOCKED (it is the mandated verdict) but make the two kinds
distinguishable in the aggregate, e.g. carry the reason tag into the summary:

```python
    # _emit 已把 reason 存进 ROWS["note"],汇总时按 reason 分开计数
    expected_side = len([r for r in ROWS if r["item"] == i
                         and r["verdict"] == "BLOCKED"
                         and r["note"] == "令牌未声明或期望值解析失败"])
    print(f"item {i}: {v.upper()}  ({n} 条断言,{fails} FAIL,{blocks} BLOCKED"
          f"{f',其中期望侧 {expected_side}' if expected_side else ''})", flush=True)
```

Alternatively, split the branch by resolver (have `resolve_token`'s callers use a
distinct sentinel) if the intent really is "unresolvable expectation is an
environment state, a broken token wiring is a product defect".

## Info

### IN-01: the declaration check is "non-empty", not "resolves to a colour"

**File:** `scripts/check-05-ui-uat.py:268-269`

**Issue:** `if (!declared || !declared.trim()) return null;` catches undeclared and
declared-but-empty tokens, but not a token whose value is non-empty and yet
invalid as a colour — e.g. the classic `--color-text-muted: --radix-gray-11;`
(`var()` dropped). That value is a valid custom-property token stream, so
`declared` is `"--radix-gray-11"`, the probe's `color: var(--t)` is invalid at
computed-value time and inherits, the consumer `.hint` does the same, and the
assertion is **PASS again** — the residual half of CR-01's vacuity class.

I traced the blast radius rather than assuming it is covered: of the 13 tokens
passed to `resolve_color`, 12 appear in check-02's `/* PAIR */` manifest and
check-02 fails loudly on an unparsable value (`check-02-contrast.py:104`), so
the mutation is caught there. The exception is `--color-action-irreversible`,
which has **zero** manifest references (`grep -c` on `PAIR --color-action-irreversible `
/ `ON --color-action-irreversible ` = 0; only `-fg`/`-surface` are listed at
`style.css:317`), so check-02 never resolves it. At its single assertion
(`check-05:679`, `#btn-authorize border-top-color`) the degenerate case happens to
fail loudly anyway (`border-color` falls back to `currentColor` = the button's
`--color-action-irreversible-fg`, which differs from the inherited body colour) —
so this is a boundary observation, not a live hole. Note that the manifest gap is
the same family as **deferred W-4**; do not double-count it as a new item.

**Fix:** make the check validate the value, not just its presence:

```javascript
            const declared = getComputedStyle(document.documentElement).getPropertyValue(t);
            if (!declared || !declared.trim()) return null;
            // 非空 ≠ 是颜色:`--x: --radix-gray-11`(漏了 var())非空却无效,
            // 探针与消费者会一起退化成同一个继承值 —— CR-01 的残余半边。
            if (!CSS.supports('color', declared.trim())) return null;
```

### IN-02: the mutation's *minimality* is not asserted

**File:** `scripts/probe-05-resolve-color.py:87-95`, `:123-130`

**Issue:** the filter deletes every line containing `--color-text-muted:`, and the
only self-check is "the token string is gone from the mutated body". If
`frontend/style.css` is ever reformatted so that the declaration shares a line
with other declarations or with a closing brace (e.g.
`--color-text-muted: var(--radix-gray-11); }`), the whole line — and therefore
more than the intended declaration — disappears, and the probe would still print
`mutation-applied=yes` and the same four `PROBE` lines while claiming "只删掉
`--color-text-muted` 那一行声明". Today the mutation is provably minimal:
`style.css:120` is `  --color-text-muted: var(--radix-gray-11);`, a lone
declaration, and `grep -c -- '--color-text-muted:'` over the file is 1.

**Fix:** assert the delta is exactly one declaration-shaped line:

```python
        removed = [ln for ln in lines if f"{TOKEN}:" in ln]
        require(
            len(removed) == 1 and "{" not in removed[0] and "}" not in removed[0],
            f"变异不最小:命中 {len(removed)} 行,或该行含块结构 —— 删掉的不止一个声明",
        )
```

### IN-03: the probe swallows the harness helpers' `SystemExit` messages

**File:** `scripts/probe-05-resolve-color.py:225-226`

**Issue:** `except SystemExit as e: failures.append(str(e))` discards the message.
`require()` has already printed to stderr before raising, so probe failures are
fine — but `h5.make_fixture` (`check-05:317`) raises
`SystemExit("ERROR: 状态样本不存在:…")`, and inside this `try` that becomes a bare
`exit 1` with **no output at all**. The harness itself does not catch `SystemExit`
and therefore does print the reason, so the probe is strictly worse at diagnosis
here. The catch is also unnecessary: an uncaught `SystemExit(1)` already exits 1
and still runs the `finally` cleanup.

**Fix:** delete the `except` clause (keep `try/finally`), or at minimum
`print(str(e), file=sys.stderr)` before appending.

---

_Reviewed: 2026-09-20T02:35:38Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
---
phase: idi-10-tables-and-radius-scale
verified: 2026-09-27T14:45:00Z
status: passed
score: 62/62 must-haves verified
covered_files:
  - .planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md
  - .planning/phases/idi-10-tables-and-radius-scale/idi-10-01-PLAN.md
  - .planning/phases/idi-10-tables-and-radius-scale/idi-10-01-SUMMARY.md
  - .planning/phases/idi-10-tables-and-radius-scale/idi-10-02-PLAN.md
  - .planning/phases/idi-10-tables-and-radius-scale/idi-10-02-SUMMARY.md
  - .planning/phases/idi-10-tables-and-radius-scale/idi-10-03-PLAN.md
  - .planning/phases/idi-10-tables-and-radius-scale/idi-10-03-SUMMARY.md
  - .planning/phases/idi-10-tables-and-radius-scale/idi-10-04-PLAN.md
  - .planning/phases/idi-10-tables-and-radius-scale/idi-10-04-SUMMARY.md
  - frontend/style.css
  - scripts/check-10-idi10-validation.py
covered_digest: "v1:sha256:76e09b08a85e93a4adf5c9e8b340e9de562bcf32f48ce30785fb7c5198aec89b"
behavior_unverified: 0
overrides_applied: 0
coincidental_reliance_items: []
human_verification: []
---

# Phase 10: 表格重做与圆角刻度收敛 Verification Report

**Phase Goal:** 把 Phase 9 之后**读起来最重**的两处构图残留收掉 —— 文档区表格由「每格 1px 全边框的电子表格式网格」改为「表头浅底 + 仅横向分隔线」;圆角刻度由 `8 / 10 / 28 / 999` 收敛为 `8 / 10 / 999` 三档(删掉从未并入刻度的 `--radius-lg: 28px`)。两项都是**纯构图**改动:零新增颜色值、零新令牌(`--radius-lg` 是**删除**不是新增)、零阈值放宽、零新增 `!important`。
**Verified:** 2026-09-27T14:45:00Z (HEAD = `7170fa5`)
**Status:** passed
**Re-verification:** No — initial verification (no prior `idi-10-VERIFICATION.md` existed)

## Verification Posture

SUMMARY claims were treated as hypotheses, not evidence. Every product-level claim below was
re-derived from the live working tree; the four `check-10` assertion sets were **re-executed in this
process against a real browser** (r2, t1+t2, r1 — all reproduced byte-for-byte in assertion counts and
readings), the before/after radius snapshots were diffed by hand, and the 10/1 fingerprint triage was
recomputed from the report frontmatter rather than read out of the SUMMARY.

Two notes on the review aftermath, per the phase-state brief:

- **CR-01 is genuinely fixed** in `7170fa5`, and I confirmed the fix is *effective*, not cosmetic: the
  token assertions now route through `ok_true()` (lines 423-427, 475-478, 507-509), so a deleted
  `--radius-md` / `--radius-pill` is a hard FAIL rather than a `BLOCKED`/exit-2. `frontend/style.css`
  was **not** touched by that commit — `git diff --stat a98c788..HEAD -- frontend/` is empty.
- **WR-01 / WR-02 are fixed** (tautological sample-list comparison replaced with an on-disk
  existence + exact-5-PNG check, `check-10:558-571`; gray-6 literal guards added at `:336` / `:380`).
  **WR-03 / WR-04 / WR-05 remain** and are new-coverage gaps in the gate script, deliberately deferred.
  I judged each against the must_have list: none undermines a must-have (details in Anti-Patterns).

## Goal Achievement

### Observable Truths — Plan 01 (TABLE-01 / TABLE-02)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | `.markdown-body td` computed `border-left/right/top-width` == `0px` in a real browser | ✓ VERIFIED | I re-ran `check-10 --item t1 --item t2`: **t1 PASS 58 assertions / t2 PASS 51 assertions, 0 FAIL 0 BLOCKED, exit=0**. Raw readings for all 5 (sample, host) pairs: left/right/top all `0px` (HEAD was `1px`). Two pairs sit in a rendered subtree (`(p1,#draft-content)`, `(p3,#round-doc)`) ⇒ render evidence, not just cascade resolution |
| 2 | `.markdown-body th` computed `background-color` == runtime `--color-surface` **and** == literal `rgb(249, 249, 249)` | ✓ VERIFIED | Reproduced: `PASS ... expected=rgb(249, 249, 249) actual=rgb(249, 249, 249)` on all 5 pairs; token-level guard `--color-surface 解析值 == gray-2 字面量` PASS |
| 3 | `th`/`td` computed `border-bottom` = 1px / solid / == runtime `--color-border-subtle` | ✓ VERIFIED | Reproduced: `border-bottom-width=1px`, `border-bottom-style=solid`, `border-bottom-color=rgb(217, 217, 217)` on all pairs; plus the WR-02 gray-6 literal guard (`== gray-6 字面量`) PASS — so the "no longer gray-7" claim is value-level, not self-referential |
| 4 | `th, td` `padding` / `font-size` verbatim unchanged; `table` `border-collapse` unchanged | ✓ VERIFIED | `frontend/style.css:1115-1116` = `padding: var(--space-1) var(--space-2-5);` / `font-size: var(--text-base);`; `:1111` = `.markdown-body table { border-collapse: collapse; }`. Control-group assertions PASS (`padding=4px 10px`, `font-size=14px`). Phase diff touches none of these three lines |
| 5 | Original `border: 1px solid var(--color-border);` rewritten **in place**; no dead overridden `border` remains | ✓ VERIFIED | `git diff 6ce0923 HEAD -- frontend/style.css` shows the single line replaced by `border: none;` + `border-bottom: 1px solid var(--color-border-subtle);` inside the same rule body. No later rule targets `th`/`td` borders (`grep` for competing selectors returns only `:1112` / `:1118`) |
| 6 | `.markdown-body th { background: var(--color-surface); }` is an **appended** block immediately after the union rule; existing source order verbatim unchanged | ✓ VERIFIED | File order is `:1111 table` → `:1112-1117 th, td` → `:1118 .markdown-body th` → `:1119 .markdown-body code`. The selector `.markdown-body th` did not exist at HEAD, so no equal-specificity pair is disturbed; the phase diff is pure append + one in-place rewrite, zero reorder |
| 7 | Header text-on-gray-2 pair already registered ⇒ zero new PAIR entries; `check-02` prints the covering line | ✓ VERIFIED | My own `check-02` run prints `PASS  15.48  --color-text on --color-surface`. `grep -o '/\* PAIR' frontend/style.css \| wc -l` = **53** (unchanged); `/* ORDER` = **1** |
| 8 | Separators add **no** NON-TEXT entry, on the strength of two *existing* registrations | ✓ VERIFIED | `check-02` exits 0 with `PASS: 0 failures`; the 53-entry manifest is byte-unchanged (`git diff HEAD -- scripts/check-02-contrast.py` empty) — nothing was added or removed, so the "no new NON-TEXT entry" claim is confirmed by the manifest's own immutability |
| 9 | Zero new colour values / primitives / threshold changes | ✓ VERIFIED | `git diff 6ce0923 HEAD -- frontend/style.css` contains no `--radix-` line and no `#hex`; `TEXT_MIN = 4.5` / `NON_TEXT_MIN = 3.0` at `check-02:24-25` with `git diff HEAD -- scripts/check-02-contrast.py` empty |
| 10 | No new "token-name + colon" inside the fence; no bare `#hex` / `var(--radix-` outside | ✓ VERIFIED | `bash scripts/check-01-token-conformance.sh` → PASS, exit 0 (scans outside-fence text); `.venv/bin/python scripts/check-02-contrast.py` → PASS (its `DECL_RE` scans the fence incl. comments) |
| 11 | Four static gates PASS (`check-01` / `check-02` / `check-03` / `check-04`) | ✓ VERIFIED | Re-ran all four in this process: `check-01` PASS, `check-02` `PASS: 0 failures`, `check-03` PASS, `check-04` PASS — all exit 0 |
| 12 | `scripts/check-10-idi10-validation.py` exists, runs under `.venv/bin/python`, exit semantics 0/1/2, accepts `--item` / `--screenshot` / `--keep` | ✓ VERIFIED | `--help` lists `--item` (repeatable / comma-separated), `--screenshot DIR`, `--radius-snapshot`, `--json`, `--keep`; `:766` `code = 1 if any_fail else (2 if any_blocked else 0)` — same vocabulary as `check-05` |
| 13 | `--item t1` and `--item t2` each exit=0, 0 FAIL, **0 BLOCKED**; INFO reports two independent facts per pair | ✓ VERIFIED | Reproduced in this process: t1 `PASS (58 assertions, 0 FAIL, 0 BLOCKED)`, t2 `PASS (51 assertions, 0 FAIL, 0 BLOCKED)`, `exit=0`. Each pair logs injected `th=3 td=6` **and** a rendered-ness reading (`处于被渲染子树=True/False` + hiding ancestor) |
| 14 | Evidence-strength classification comes from runtime measurement (≥1 rendered pair), and the property is **fail-able** via an aggregate assertion | ✓ VERIFIED | Reproduced: `渲染证据 2 个对 / 层叠解析证据 3 个对`; aggregate line `PASS t1 [聚合] 至少 1 个 (样本, 宿主) 对处于被渲染子树 ... rendered 2/5` (same for t2). The gate does not assume 5 equivalent pairs |
| 15 | `--screenshot DIR` produces exactly 5 PNGs matching `STATES`, each 1440×900 | ✓ VERIFIED | Reproduced: `shot` PASS (7 assertions); directory holds exactly `['archive.png','checking.png','p1.png','p12.png','p3.png']`, IHDR-verified 1440×900 by my own decoder |

### Observable Truths — Plan 02 (RADIUS-01 / RADIUS-02)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 16 | Radius scale has three steps: full-text `--radius-lg` count == 0, fence declaration count == 0, `var(--radius-lg)` reference count == 0 | ✓ VERIFIED | Three independent quantities measured on the live file: `grep -c -F -- '--radius-lg' frontend/style.css` = **0**; fence slice (`:5`–`:695`) count = **0**; `grep -o -F 'var(--radius-lg)' \| wc -l` = **0** |
| 17 | Fence `--radius-sm: 8px` / `--radius-md: 10px` / `--radius-pill: 999px` verbatim unchanged; no unconsumed declaration remains | ✓ VERIFIED | `frontend/style.css:412-414` reads exactly those three lines. Every `--radius-*` declared in the fence has consumers (31 `border-radius` sites, all three tokens used) |
| 18 | `--radius-md` **not** deleted — `check-09` still green | ✓ VERIFIED | I re-ran `.venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2`: `c1 PASS (26, 0 FAIL, 0 BLOCKED)` / `c2 PASS (13, 0 FAIL, 0 BLOCKED)`, exit=0. `--radius-md: 10px;` present at `:413` |
| 19 | Fence comment changed `four values` → `three values`, records the deleted step + both destinations, and does **not** contain the literal token name | ✓ VERIFIED | `:402-411` reads "Radius — three values. The former fourth step (28px) ..." and names both consumers; the literal `--radius-lg` appears nowhere in the file (truth 16's zero-count is the proof) |
| 20 | `.chat-user`: TL/TR/BL == runtime `--radius-md`, BR == runtime `--radius-sm` (sharp tail kept) | ✓ VERIFIED | Reproduced in-browser: `border-top-left-radius=10px / top-right=10px / bottom-left=10px / bottom-right=8px`; per-corner assertions PASS; the "四角并非统一" inequality PASS (so "keep the sharp corner" cannot be silently eaten by a uniform assertion). Probe bubble built via the app's own `appendChatMessage('user', …)` — no hand-built DOM |
| 21 | `#chat-input-row input` computed `border-radius` == runtime `--radius-pill`; four corners equal; `min-height` still 52px | ✓ VERIFIED | Reproduced: `r2 PASS (10 assertions, 0 FAIL, 0 BLOCKED)`, exit=0; all four corners `999px`, `min-height=52px`, `border-top=1px solid` |
| 22 | Input appearance unchanged, proven by before/after runtime readings (not arithmetic) | ✓ VERIFIED | I diffed the two committed snapshots myself: `rect` **identical** (`{x:137, y:406.5, w:664, h:52}`); element PNGs **byte-identical** (`shasum -a 256` = `190d7d7d…4a35` for both); computed-style diff = **9** keys, all radius-related (4 physical corner longhands + 4 logical aliases + the deleted token's own key). Nothing else moved. See Anti-Patterns INFO-1 for the criterion-count correction |
| 23 | Both rule blocks keep their position and selector text; each carries a comment explaining its destination | ✓ VERIFIED | `.chat-user` block `:1209-1215` with comment `:1203-1208`; `#chat-input-row input` block `:1240-1248` with comment `:1235-1239`. Both are in-place re-attributions (phase diff shows one changed line each) |
| 24 | `#doc-panel-header` `border-radius: 0;` untouched | ✓ VERIFIED | `frontend/style.css:817` = `border-radius: 0;` — outside the phase diff entirely |
| 25 | Zero new colour values / primitives / `!important` / `@media` / `@layer` / `@property` / `var(--x, #fallback)`; PAIR 53 and ORDER 1 unchanged | ✓ VERIFIED | PAIR = 53, ORDER = 1; `!important;` declaration count = **1** (`check-04` PASS); `grep -c '@media'` = **1**; phase diff contains no `@layer` / `@property` / fallback var / `--radix-` line |
| 26 | Four static gates green | ✓ VERIFIED | Same run as truth 11 |
| 27 | `--item r1` / `--item r2` exit=0, 0 FAIL / 0 BLOCKED; `t1`/`t2` still green | ✓ VERIFIED | Reproduced: `r1 PASS (11, 0 FAIL, 0 BLOCKED)`, `r2 PASS (10, 0 FAIL, 0 BLOCKED)`, both exit=0; t1/t2 green (truth 13) |
| 28 | `radius-snapshots/` holds `input-radius-before.{png,json}` + `input-radius-after.{png,json}`, each JSON carrying the captured `frontend/style.css` sha256 | ✓ VERIFIED | All four files present. Shas differ and are genuine: before `c6c06436f77271b5…`, after `4e7830863522f7b5…` ⇒ two real readings, not one copied twice |

### Observable Truths — Plan 03 (REG-03, regression surface)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 29 | `check-05 --browser bundled`: no FAIL, exit 2, BLOCKED only on item 5's two `--ai-smoke` legs | ✓ VERIFIED | Committed raw log: item conclusions 1-4, 6-10 all `0 FAIL, 0 BLOCKED`; item 5 `BLOCKED (9 assertions, 0 FAIL, 2 BLOCKED)`; `exit=2`. My anchored scan for lines beginning `FAIL `/`BLOCKED ` finds exactly 2, both the documented ai-smoke legs |
| 30 | `check-06` exit 0; `check-07` exit 0 | ✓ VERIFIED | Logs: `check-06` g1-g6 all PASS, `exit=0`; `check-07` g1-g4 all PASS, `exit=0` |
| 31 | `probe-05` exit 0; `probe-07` exit 0 | ✓ VERIFIED | `probe-05` `[gsd] EXIT=0` (its one `BLOCKED` is the probe's *mutated post-fix* leg — the mutation removing the token, i.e. the probe proving it can go red); `probe-07` `[gsd] EXIT=0` with `ratio=3.54 (>= 3.0)` |
| 32 | Item-by-item identical to the Phase 9 `check-05-full.log` conclusion block | ✓ VERIFIED | `diff` of the two `^item [0-9]+:` blocks returns **IDENTICAL** (10 items, same assertion counts, same FAIL/BLOCKED distribution) |
| 33 | `check-05` `[p1] .markdown-body td font-size == var(--text-base)` PASS (not BLOCKED) | ✓ VERIFIED | Log line 152: `PASS [p1] .markdown-body td font-size == var(--text-base): expected=14px actual=14px` |
| 34 | `check-05` item 8's three `badge × banner` and three `#doc-panel` width assertions still PASS, readings value-identical to Phase 9 | ✓ VERIFIED | Phase 9 vs Phase 10 item-8 INFO readings are **character-identical**: `@1440 scrollWidth=1440 clientWidth=1440 docPanelWidth=432`; `@1024 1024/1024/340`; `@768 768/768/340`. Removing vertical lines only narrows tables — direction-safe, and measured |
| 35 | `check-05` item 4's four geometry assertions still PASS | ✓ VERIFIED | Log line 124: `PASS [p1] #doc-panel-body padding: expected=32px 40px actual=32px 40px`; the sibling `.panel-header` / `button` / `.overlay-card` padding-top assertions PASS in item 4's 65-assertion block |
| 36 | `check-05` item 9's scroll-census (exactly `{#main-pane, #chat-messages, #latest-check}`) and item 2's `#round-doc` contrast ≥ 4.5 still PASS | ✓ VERIFIED | Log line 399: scroll census PASS with the exact three-element set; line 92: `PASS [p3→round1] 正文对比度: ratio=16.29` |
| 37 | `check-06` g3 / g5 / g6 all pass, incl. g6's two `box-shadow 恒 none` controls and g5's 340px no-wrap/no-clip | ✓ VERIFIED | `check-06` log: g3 PASS (12), g5 PASS (5) with `panelWidth=340, lineBoxes=1, scrollW<=clientW`, g6 PASS (7) with `headerShadow='none'` across all three toggle states |
| 38 | `check-10 --item t1 --item t2 --item r1 --item r2` still exit=0, 0 FAIL / 0 BLOCKED | ✓ VERIFIED | Reproduced individually in this process (truths 13, 27); no assertion set was broken by the other plan's edits |
| 39 | Any "gate assertion whose fact the phase deliberately changed" is handled by **re-registration** only; expected count zero | ✓ VERIFIED | `git diff 6ce0923 HEAD -- scripts/` names exactly one file: `scripts/check-10-idi10-validation.py` (this phase's own new gate). `git diff HEAD -- scripts/check-05-ui-uat.py` is **empty**; `check-01…04` / `check-06` / `check-07` / `check-09` / `probe-*` untouched. Zero assertions weakened/skipped/deleted |
| 40 | Four static gates PASS | ✓ VERIFIED | Same run as truth 11 |
| 41 | `.venv/bin/python -m pytest backend/tests -q --tb=short` == `219 passed, 6 skipped` | ✓ VERIFIED | Re-ran in this process with the project venv: `219 passed, 6 skipped, 1 warning in 6.44s`, exit 0 — matches baseline verbatim |
| 42 | `node --check frontend/app.js` exit 0 | ✓ VERIFIED | Re-ran: exit 0 (app.js has zero byte changes this phase — `git diff HEAD -- frontend/app.js` empty) |
| 43 | `git status --porcelain frontend/` lists only `frontend/style.css`; `frontend/vendor/` holds only `marked.min.js` | ✓ VERIFIED | Working tree is clean and `git status --porcelain frontend/` is empty (the phase's frontend change is committed); `ls frontend/vendor/` = `marked.min.js` |
| 44 | `scripts/check-05-ui-uat.py` unmodified | ✓ VERIFIED | `git diff HEAD -- scripts/check-05-ui-uat.py` empty; last commit touching it is `3bc9660` (Phase 9) |
| 45 | `screenshots/` holds PNGs for all 5 states, each 1440×900 | ✓ VERIFIED | 5 PNGs present; I decoded each IHDR myself: `p1 1440x900`, `p12 1440x900`, `p3 1440x900`, `checking 1440x900`, `archive 1440x900` |
| 46 | Screenshots show the table's mechanical consequences; `p3` shows the three machine-parsable tables | ✓ VERIFIED | I viewed `screenshots/p3.png`: §1 批注回应 / §2 覆盖维度表 / §3 未决问题清单 are all visible, each with a shaded header band, **no vertical lines and no outer frame**, and horizontal-only separators. The fixture doc has 15 `^\|` lines across exactly those three tables (`scripts/ui-states/p3/docs/discuss-round-2.md`) — "at least two" is satisfied with all three |
| 47 | Screenshots show the radius consequences (10px bubble + sharp tail; input unchanged) | ✓ VERIFIED | I viewed `screenshots/chat-user/p1-chat-user-evidence.png`: the user bubble has a small card-radius with a visibly sharp bottom-right corner, and the input renders as an unchanged pill |
| 48 | `gate-logs/` holds one file per gate with the gate's **full** raw output | ✓ VERIFIED | 13 logs present, named after their gates, none truncated (e.g. `check-05-full.log` is 96,665 bytes ending in the full conclusion block + `[gsd] EXIT=2`) |

### Observable Truths — Plan 04 (REG-03 fingerprint triage + idi-09 re-verification)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 49 | Coverage criterion anchors **frontmatter `covered_files` line-match**, not full-text grep; `idi-08` is not in the list | ✓ VERIFIED | I recomputed the criterion myself over all `**/*VERIFICATION.md`: exactly **10** reports carry a `  - frontend/style.css` line in frontmatter. `idi-08` has **0** such lines while its body mentions `frontend/style.css` **27** times — precisely the full-text false positive the criterion exists to exclude |
| 50 | The list is exactly 10 `status: passed` reports (v1.13 ×3, v1.14 ×5, `idi-09`, quick `260925-iin`) | ✓ VERIFIED | My recomputation returns exactly those 10, all `status: passed`, matching the SUMMARY's enumeration one-for-one |
| 51 | Per-report `verification.status` raw JSON: 9 `stale`; `idi-09` stale before re-verification, `passed` after | ✓ VERIFIED | `verification-recheck.log` holds the raw JSON per report (9 × `{"status":"stale",...}`). I queried `idi-09` at HEAD myself: `{"status":"passed","next_action":"Verification passed — continue."}` |
| 52 | Per-report `verification.fingerprint`: 9 fail closed with the missing-file error; `idi-09` succeeds with a `v1:sha256:…` digest | ✓ VERIFIED | Log shows 9 × `Error: could not compute fingerprint — a covered file is missing, unreadable, or escapes the project root` with `rc=1`. I recomputed `idi-09`'s fingerprint over its 10 `covered_files` and got `v1:sha256:7b82f8d1c2f5f6e371effbe73c5182a4ed78d49eecbea3ea76cca3e76d6a7031` — **byte-identical** to the digest in its frontmatter |
| 53 | The 9 fail-closed causes measured per report (archived path relocation), with per-report missing/total counts | ✓ VERIFIED | Log records each report's `present= / total= / missing=` plus the missing path list; e.g. `idi-01` 29/41 missing 12, `idi-02` 15/26 missing 11. All missing paths are of the form `.planning/phases/<id>/…` after archival to `.planning/milestones/<ver>-phases/<id>/…` — a path cause, not a content cause, predating this phase |
| 54 | Only `idi-09` re-verified, with per-report evidence for why the other 9 are out of scope | ✓ VERIFIED | `idi-10-04-SUMMARY.md` carries the per-report triage table; the recheck log carries the raw command output for all 10. The scope argument is evidence-backed, not a bare "known limitation" |
| 55 | `scripts/check-05-ui-uat.py` unchanged ⇒ re-verification surface strictly 1 report | ✓ VERIFIED | `git diff HEAD -- scripts/check-05-ui-uat.py` empty (truth 44); among all `*VERIFICATION.md`, the only one modified in this phase's range is `idi-09-VERIFICATION.md` |
| 56 | `idi-09-VERIFICATION.md`: `covered_files` still the original 10; `covered_digest` **recomputed** (differs from old); `status: passed`; `score: 24/24` | ✓ VERIFIED | Frontmatter: 10 `covered_files` verbatim; `covered_digest: "v1:sha256:7b82f8d1…7031"` vs the previously recorded `6e811a11…` — genuinely different, and my independent recomputation reproduces `7b82f8d1…` exactly; `status: passed`; `score: 24/24 must-haves verified` |
| 57 | `re_verification:` block records `previous_status` / `previous_score` and the three lists | ✓ VERIFIED | Frontmatter `re_verification: {previous_status: passed, previous_score: 24/24, gaps_closed: [], gaps_remaining: [], regressions: []}` |
| 58 | Body has a "Why this is a re-verification, and what changed" section naming `frontend/style.css` and what changed | ✓ VERIFIED | §"Phase 10 re-verification (2026-09-27) — `frontend/style.css` changed again" names the table rule rewrite + `.markdown-body th` background (with line refs `:1112-1118`) and the radius convergence + `--radius-lg` deletion + the two re-attributions (`:408-410`, `:1211`, `:1245`). It is written as a re-verification, not a fingerprint refresh |
| 59 | idi-09's 24 must-haves re-derived against HEAD; `check-09` c1…c5 green | ✓ VERIFIED | Report's truth table shows 24 rows all ✓ VERIFIED with the two moved historical readings (border count 3→2, selector count 173→174) explicitly annotated with mechanism. I re-ran `check-09 --item c1 --item c2`: both PASS, exit 0 (truth 18) |
| 60 | `verification.status .planning/phases/idi-09-card-containers` returns `passed` | ✓ VERIFIED | Queried directly: `{"status":"passed","next_action":"Verification passed — continue."}` |
| 61 | Only `idi-09-VERIFICATION.md` changed; no product / gate / fixture / other-report bytes touched | ✓ VERIFIED | `git diff --name-only 6ce0923 HEAD \| grep -i verification` → only `idi-09-VERIFICATION.md` (+ this phase's own `gate-logs/verification-recheck.log`); `git diff --stat 6ce0923 HEAD -- scripts/ui-states/` empty; `scripts/` diff names only `check-10` |
| 62 | No `stale`→`passed` flip without re-running the criteria; no must-have deleted/skipped; no gate or threshold edited | ✓ VERIFIED | Digest genuinely recomputed and matches my independent recomputation (truth 56); 24/24 with three empty lists; the only `scripts/` change is this phase's new gate; `check-02` / `check-09` thresholds unchanged (`git diff HEAD` empty for both) |

**Score:** 62/62 truths verified (0 present-but-behavior-unverified)

### Prohibitions (must-NOT) Check

All **33** plan prohibitions are `verification: flagged` (judgment-tier). I checked each against the
codebase rather than leaving them to human resolution — every one resolves to **not violated** on
deterministic evidence, grouped here by concern:

| Concern | Plans | Status | Evidence |
|---|---|---|---|
| Union selector text / rule-block positions preserved; no block moved | 01, 02 | ✓ NOT VIOLATED | `.markdown-body th, .markdown-body td` intact at `:1112`; phase diff is one in-place rewrite + one append; both radius edits are in-place (one line each) |
| `td` `font-size` / `padding` untouched; `table` `border-collapse` untouched | 01 | ✓ NOT VIOLATED | `:1111`, `:1115-1116` byte-unchanged; `check-05`'s live `td font-size` assertion PASS |
| No `--radix-*` value change, no new primitive/colour token, no threshold relaxation, no `check-02` edit, no PAIR/ORDER deletion; header surface must be `--color-surface` | 01 | ✓ NOT VIOLATED | `git diff HEAD -- scripts/check-02-contrast.py` empty; PAIR 53 / ORDER 1; phase diff has no `--radix-` line; `:1118` uses `var(--color-surface)` |
| No new `!important`, no tokenized `display`, no `@layer`/`@property`/fallback `var()`, no new `@media` | 01, 02 | ✓ NOT VIOLATED | `check-04` PASS (`!important;` declarations = 1); `@media` count = 1; diff contains none of the banned constructs |
| No "token + colon" in fence comments; no bare `#hex` / `var(--radix-` outside | 01, 02 | ✓ NOT VIOLATED | `check-01` PASS; `check-02` PASS (its `DECL_RE` scans the fence) |
| `scripts/check-05-ui-uat.py` untouched; `check-01…04`/`06`/`07`/`09`/`probe-*` untouched | 01, 02, 03, 04 | ✓ NOT VIOLATED | `git diff 6ce0923 HEAD -- scripts/` names only `check-10-idi10-validation.py` |
| `frontend/app.js` / `index.html` / `vendor/` zero-byte changes; no new dependency or build step | 01, 02, 03, 04 | ✓ NOT VIOLATED | `git diff HEAD` empty for all three; `vendor/` holds only `marked.min.js` |
| No scope creep (icons/empty-states, dark mode, `.overlay-card` fill, page-level whitespace, input UA white fill); no radius work in plan 01 | 01, 02, 03 | ✓ NOT VIOLATED | Phase diff is confined to the table rules + the two radius consumers + comments; none of the five unnamed open items appear |
| Do **not** unify the two radius consumers | 02 | ✓ NOT VIOLATED | `.chat-user` → `var(--radius-md)`; `#chat-input-row input` → `var(--radius-pill)` — deliberately different |
| Do not delete/rewrite `--radius-md`; do not touch `#doc-panel-header`'s `border-radius: 0` | 02 | ✓ NOT VIOLATED | `:413` intact and `check-09` green; `:817` untouched |
| Do not substitute arithmetic for measurement; do not fake a "before" reading | 02 | ✓ NOT VIOLATED | Two real snapshots with different `style_css_sha256`; rect identical; PNGs byte-identical (truth 22) |
| Do not relax any gate criterion to go green; do not treat `BLOCKED` as `PASS`; do not use bare `grep -c 'FAIL'` | 03 | ✓ NOT VIOLATED | Zero gate edits; the only `BLOCKED` are item 5's two ai-smoke legs; my own scan was anchored to line-start `FAIL `/`BLOCKED ` rather than a bare count |
| pytest must use the project `.venv`; `check-05` must not use `channel="chrome"` | 03 | ✓ NOT VIOLATED | I re-ran pytest with `.venv/bin/python` → 219/6; logs show `--browser bundled` usage and `browser.version 153.0.8010.12` |
| Do not write screenshots/logs into `frontend/`; do not hand-fabricate DOM or modify `scripts/ui-states/` | 02, 03 | ✓ NOT VIOLATED | Artifacts live under `.planning/phases/idi-10-…`; `git diff --stat 6ce0923 HEAD -- scripts/ui-states/` empty; probes use the app's own `appendChatMessage` / `renderMarkdown` |
| Do not write the idi-09 re-verification as a fingerprint refresh; do not change the other 9 reports; do not game `verification.status` | 04 | ✓ NOT VIOLATED | Report has a substantive "what changed" section; only `idi-09-VERIFICATION.md` modified; digest genuinely recomputed and independently reproduced |
| Do not delete/skip/weaken any idi-09 must-have | 04 | ✓ NOT VIOLATED | 24/24 with `gaps_remaining: []` / `regressions: []` |

## Required Artifacts

| Artifact | Expected | Status | Details |
| -------- | -------- | ------ | ------- |
| `frontend/style.css` | Table rules rewritten in place + `.markdown-body th` background appended; `--radius-lg` deleted; two consumers re-attributed | ✓ VERIFIED | Exists, substantive, wired, data flowing. Diff vs pre-phase `6ce0923`: 48 insertions / 5 deletions, all accounted for. Live-browser readings confirm the rules actually paint |
| `scripts/check-10-idi10-validation.py` | New runtime gate: `t1` / `t2` / `r1` / `r2` + `--screenshot` + `--radius-snapshot` + `--json` | ✓ VERIFIED | 776 lines; all four item sets reproduced exit=0 in this process; `--help` confirms the CLI surface |
| `.planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/` | `input-radius-{before,after}.{png,json}` | ✓ VERIFIED | 4 files; before/after shas differ; PNGs byte-identical; rects identical |
| `.planning/phases/idi-10-tables-and-radius-scale/screenshots/` | 5 state PNGs at 1440×900 | ✓ VERIFIED | 5/5 present, IHDR-verified, inspected |
| `.planning/phases/idi-10-tables-and-radius-scale/gate-logs/` | One full raw log per gate | ✓ VERIFIED | 13 logs, none truncated |
| `.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md` | Re-verified against HEAD content | ✓ VERIFIED | `status: passed`, `24/24`, digest recomputed to `7b82f8d1…` (independently reproduced) |

## Key Link Verification

| From | To | Via | Status | Details |
| ---- | -- | --- | ------ | ------- |
| `.markdown-body th { background: var(--color-surface); }` | fence `--color-surface: var(--radix-gray-2)` | `var()` reference | ✓ WIRED | Runtime `getComputedStyle` returns `rgb(249, 249, 249)` = gray-2, on both a rendered host and hidden hosts |
| `border-bottom: 1px solid var(--color-border-subtle);` | fence `--color-border-subtle: var(--radix-gray-6)` | `var()` reference | ✓ WIRED | Runtime `border-bottom-color` = `rgb(217, 217, 217)` = gray-6, pinned by literal too |
| `check-10` `t1`/`t2` | `.markdown-body` table rules in a real browser | Playwright `getComputedStyle` | ✓ WIRED | 109 assertions across the two sets, all reading live computed style; 2/5 pairs proven in a rendered subtree |
| Header text on its new gray-2 ground | existing `/* PAIR --color-text ON --color-surface TEXT */` | registered pair, `check-02` output line | ✓ WIRED | `PASS 15.48 --color-text on --color-surface`; manifest unchanged at 53 entries |
| `.chat-user { border-radius: var(--radius-md); }` | fence `--radius-md: 10px` | `var()` reference | ✓ WIRED | Computed TL/TR/BL = `10px` |
| `#chat-input-row input { border-radius: var(--radius-pill); }` | fence `--radius-pill: 999px` | `var()` reference | ✓ WIRED | Computed corners all `999px` |
| `.chat-user { border-bottom-right-radius: var(--radius-sm); }` | fence `--radius-sm: 8px` | `var()` reference | ✓ WIRED | Computed BR = `8px` (longhand after shorthand, source order correct) |
| `check-09`'s dynamic `resolve_token("--radius-md")` | fence `--radius-md: 10px` | token resolution | ✓ WIRED | `check-09 --item c1 --item c2` exit=0 — the "must not delete `--radius-md`" detector is live |
| `check-10 --screenshot DIR` | `screenshots/*.png` | Playwright `page.screenshot()` | ✓ WIRED | Exactly 5 PNGs, each asserted 1440×900 |
| `--radius-snapshot` JSONs | the "input appearance unchanged" conclusion | key-level diff + rect + PNG byte compare | ⚠️ PARTIAL (documentation) | The four artifacts are genuine and mutually consistent (I diffed them myself), but the *comparison* is not mechanized in the script — see Anti-Patterns INFO-1 |
| Report frontmatter `covered_files` line-match | the "10 reports cover `frontend/style.css`" count | anchored line match | ✓ WIRED | Independently recomputed: exactly 10, `idi-08` correctly excluded |
| `query verification.fingerprint` | `idi-09`'s `covered_digest` | deterministic hash, fail-closed | ✓ WIRED | My recomputation reproduces the report's digest byte-for-byte |

## Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
| -------- | ------------- | ------ | ------------------ | ------ |
| `frontend/style.css` table rules | `th` `background-color`, `th`/`td` `border-bottom-*`, `td` `border-{left,right,top}-width` | Browser cascade over the real stylesheet, read via `getComputedStyle` on elements injected by the app's own `renderMarkdown()` | Yes — readings are `rgb(249,249,249)` / `1px solid rgb(217,217,217)` / `0px`, i.e. the real computed values, not fixtures | ✓ FLOWING |
| `frontend/style.css` radius rules | `.chat-user` corner radii, `#chat-input-row input` corner radii | Browser cascade; `.chat-user` element built through the app's `appendChatMessage('user', …)` | Yes — `10px / 10px / 10px / 8px` and `999px`×4 on the real `#message-input` | ✓ FLOWING |
| `screenshots/*.png` | full-window render | Playwright over the live app against `scripts/ui-states/` fixtures | Yes — I viewed `p3.png` and `p1-chat-user-evidence.png`; the table and bubble render as described | ✓ FLOWING |

No value's chain terminates in a static return, hardcoded literal, or mock. The two literal constants in
the gate (`TH_BG_LITERAL`, gray-6) are *independent second sides* of two-sided assertions, not the data
source — they exist precisely to catch a token being changed while the consumer stays wired.

## Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| -------- | ------- | ------ | ------ |
| Table restyle paints in a real browser (th background, no side/top borders, gray-6 bottom) | `.venv/bin/python scripts/check-10-idi10-validation.py --item t1 --item t2` | t1 PASS 58 / t2 PASS 51, 0 FAIL 0 BLOCKED, exit=0 | ✓ PASS |
| `.chat-user` is 10px with an 8px sharp tail | `.venv/bin/python scripts/check-10-idi10-validation.py --item r1` | PASS 11 assertions, exit=0; corners `10/10/10/8` | ✓ PASS |
| Input is a pill at unchanged geometry | `.venv/bin/python scripts/check-10-idi10-validation.py --item r2` | PASS 10 assertions, exit=0; corners `999px`×4, `min-height=52px` | ✓ PASS |
| Phase 9's card gate still detects a deleted `--radius-md` | `.venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2` | c1 PASS 26 / c2 PASS 13, exit=0 | ✓ PASS |
| Static gates | `bash scripts/check-01…03.sh`; `.venv/bin/python scripts/check-02-contrast.py`; `bash scripts/check-04-important-count.sh` | PASS / PASS / PASS / `PASS: 0 failures` / PASS — all exit 0 | ✓ PASS |
| Backend suite baseline | `.venv/bin/python -m pytest backend/tests -q --tb=short` | `219 passed, 6 skipped` | ✓ PASS |
| JS syntax | `node --check frontend/app.js` | exit 0 | ✓ PASS |
| idi-09 fingerprint still matches HEAD | `node .claude/gsd-core/bin/gsd-tools.cjs query verification.status .planning/phases/idi-09-card-containers` | `{"status":"passed"}` | ✓ PASS |
| Table renders with header band + horizontal-only separators | direct inspection of `screenshots/p3.png` | Three machine-parsable tables visible, no vertical lines, no outer frame, shaded headers | ✓ PASS |

**Not re-run in this process:** `check-05` / `check-06` / `check-07` / `probe-05` / `probe-07` (browser
launches were flagged as intermittently hanging in this environment). Their committed `gate-logs/` raw
output was used instead, and I confirmed the fallback is sound rather than assumed: the only input they
read is `frontend/`, and `git diff --stat a98c788..HEAD -- frontend/` is **empty**, so those logs are
still valid for HEAD. I *did* launch browsers successfully four times in this process (check-10 t1/t2/r1/r2
and check-09), which independently confirms the environment can run the gates and that HEAD's
`frontend/style.css` produces the expected computed styles.

## Probe Execution

| Probe | Command | Result | Status |
| ----- | ------- | ------ | ------ |
| `scripts/probe-05-resolve-color.py` | committed log (not re-run) | `[gsd] EXIT=0`; its single `BLOCKED` is the probe's own mutated post-fix leg (the mutation removes the token), i.e. the probe proving it can go red | ✓ PASS |
| `scripts/probe-07-focus-composite.py` | committed log (not re-run) | `[gsd] EXIT=0`; `ratio=3.54 (>= 3.0)` | ✓ PASS |

No phase-declared `scripts/*/tests/probe-*.sh` exists; the two Python probes are the project's probe
surface and both are archived with exit 0.

## Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
| ----------- | ----------- | ----------- | ------ | -------- |
| TABLE-01 | 01, 03 | Table: header ground + horizontal-only separators; verticals/frame gone; in-place rewrite | ✓ SATISFIED | Truths 1-6; runtime readings on 5 pairs; in-place diff verified; `p3.png` visual |
| TABLE-02 | 01, 03 | All table colours on existing tokens; header ground pair confirmed by `check-02`; zero new values/primitives/thresholds | ✓ SATISFIED | Truths 7-10; `PASS 15.48 --color-text on --color-surface`; manifest still 53; `check-02` diff empty |
| RADIUS-01 | 02, 03 | Scale converged to 8 / 10 / pill; `--radius-lg` deleted (fence + full text zero); two consumers re-attributed | ✓ SATISFIED | Truths 16-19; three independent zero-counts; both destinations differ as required |
| RADIUS-02 | 02, 03 | Zero visual regression; input equals `--radius-pill` and is unchanged; `.chat-user` 10px with 8px sharp tail | ✓ SATISFIED | Truths 20-23; before/after rect identical, PNGs byte-identical, only radius keys differ |
| REG-03 | 03, 04 | Five browser gates no new failures; four static gates PASS; pytest baseline held; fingerprint debt triaged per-report with `idi-09` re-verified | ✓ SATISFIED | Truths 29-48, 49-62; item blocks IDENTICAL to Phase 9; 219/6; 10/1 triage independently recomputed; `idi-09` digest reproduced |

**Orphaned requirements:** none. All five phase requirement IDs appear in at least one plan's
`requirements:` frontmatter (01: TABLE-01/02; 02: RADIUS-01/02; 03: all five; 04: REG-03).

**REQUIREMENTS.md status column:** all five read `Complete`. Per the repo's recorded false positive,
this column reflects `phase.complete`, not this verifier — but in this instance my independent
verification agrees, so there is no discrepancy to report.

## Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| ---- | ---- | ------- | -------- | ------ |
| — | — | `TBD` / `FIXME` / `XXX` in any phase-modified file | — | **None found.** `grep -n -E 'TBD\|FIXME\|XXX' frontend/style.css scripts/check-10-idi10-validation.py` returns nothing (exit 1). The two `placeholder` hits are selector names (`#rounds-placeholder`), not stub markers |
| `frontend/style.css` | 1112-1118 | Stub patterns (`return null`, empty handlers, hardcoded empty data) | — | **None.** Not applicable to CSS; the rules are real declarations verified live |
| — | — | Unresolved debt markers (the Step 7 gate) | — | **No blocker.** No unreferenced `TBD`/`FIXME`/`XXX` exists, so the debt-marker gate does not fire |

### Findings carried from `idi-10-REVIEW.md` (none blocks a must-have)

| # | Finding | Severity | Why it is not a blocker |
|---|---------|----------|------------------------|
| INFO-1 | **WR-05 residual.** `radius_snapshot()` writes the artifacts but performs no comparison; the "appearance unchanged" claim rests on a hand-typed command, and the plan's literal criterion ("diff ⊆ the **eight** radius keys") evaluates `subset False` because the measured diff is **9** keys — the eighth-plus-one being the deleted token's own inherited key. | ℹ️ Info | The **substance is verified by measurement, not arithmetic**: I diffed the snapshots myself — `rect` identical, element PNGs byte-identical (`190d7d7d…4a35` both), and the only computed-style differences are the 4 physical corner longhands + 4 logical aliases + `--radius-lg` itself. Nothing outside the radius surface moved (`outside_radius == []`). The deviation is registered in `idi-10-02-SUMMARY.md` with raw output, and it **does not weaken the invariant** (the plan's own stated principle — "the allowed set must cover every property the expected change can touch, including the deleted token's own key" — requires 9). The defect is a stale criterion count in the plan text, not a codebase gap. Worth correcting the plan's `<verify>` line in a follow-up so the record contains no command that fails as written |
| INFO-2 | **WR-03 residual.** `r1` / `r2` have no "at least one rendered pair" guard, unlike `t1`/`t2`, although `r1`'s claim is explicitly about appearance. | ℹ️ Info | A new-coverage gap in the gate, not a product defect. I confirmed the readings are real: `r1` builds `.chat-user` through the app's own `appendChatMessage` inside the rendered `#chat-messages`, and the readings (`10/10/10/8`) are live computed values corroborated by the delivered screenshot. No must-have requires the guard |
| INFO-3 | **WR-04 residual.** Every table assertion reads a **cell**; nothing reads the `<table>` element, so a re-added table-level border, a changed `border-collapse`, or a `td` background would not be caught. | ℹ️ Info | ROADMAP SC1 defines "no verticals and no outer frame" **operationally on `td`** (`border-left/right/top-width == 0px`), which is asserted and passing. I additionally verified the visual outcome directly in `p3.png` (no vertical lines, no outer frame). A hardening opportunity for the gate, not a criterion failure |
| INFO-4 | **IN-05.** `th` renders at the UA default `font-weight: 700`, outside the file's declared three weight ranks (400/500/600). | ℹ️ Info | Pre-existing (HEAD's `th` had the same weight) and explicitly outside this phase's mandate. The phase changed `th`'s background only. Recorded so it is a known fact rather than a later surprise |
| INFO-5 | **IN-06.** The restyle does not reach tables injected into the five non-`.markdown-body` embed targets (`.event-content` / `.chat-bubble` / `.say-chunk` / `.annotation-note` / `.annotation-answer-body`). | ℹ️ Info | Pre-existing scope: the old `border: 1px solid` rule was equally scoped to `.markdown-body`. The gate's probe hosts correctly match the CSS scope |
| INFO-6 | **IN-07.** Under `border-collapse: collapse`, the last row's `td` still paints its `border-bottom`, so the table keeps a 1px bottom edge. | ℹ️ Info | Not a violation: the plan explicitly designates the surviving `border-bottom` (row separators + header underline) as SC1-permitted, and the user's chosen option was 「仅横向分隔线」 — a bottom rule is a horizontal separator. `p3.png` reads consistently with the signed-off intent |
| INFO-7 | A stray file `.planning/phases/idi-10-tables-and-radius-scale/.musthaves_rest.txt` was created by **my own** verification tooling while extracting plan frontmatter; `rm` was denied by the permission system. | ℹ️ Info | Not a phase artifact and not part of `covered_files`; harmless, but should be deleted by the orchestrator |

No `🛑 BLOCKER` and no `⚠️ WARNING` anti-pattern was found. The three residual review findings
(WR-03/04/05) are new-coverage gaps in the gate script, deliberately deferred by the phase and, as
checked above, none of them undermines a must-have.

## Deferred Items

No gaps were identified that later phases address; the milestone's Phase 10 is its last phase, so
Step 9b filtering produced nothing to defer.

## Human Verification Required

None. Every must-have in all four plans is expressed in machine-decidable form (real-browser
`getComputedStyle` readings, contrast ratios, gate exit codes, PNG IHDR dimensions, source-text counts,
fingerprint digests) and was verified in this process or from committed raw gate output whose inputs are
byte-identical to HEAD. I grepped all four PLANs for `<verify><human-check>` blocks: **zero** hits, so
there are no planner-deferred human items to harvest.

The subjective visual sign-off (does the table now read as "a sunken block inside a white card"; does the
bubble read as a card?) is framed by the ROADMAP's own Deliverables as the **delivered screenshot
artifact** — 「供用户评审的截图」 — not as a pending verification gap. The five 1440×900 state screenshots
plus the dedicated `.chat-user` evidence shot are on disk, and I inspected them: the table has a shaded
header band, no vertical lines, no outer frame and horizontal-only separators; the user bubble has a card
radius with a visibly sharp bottom-right tail. This matches the Phase 9 precedent, where a purely visual
phase was verified `passed` with `human_verification: []`.

## Gaps Summary

**No gaps.** All five ROADMAP Success Criteria hold in the codebase, and both product changes are exactly
as scoped — nothing more, nothing less:

- **SC1 (table)** — `td` computed `border-left/right/top-width` are all `0px` and `th`'s computed
  `background-color` is gray-2 with a 1px `--color-border-subtle` underline, read live from a real
  browser on five (sample, host) pairs, two of which are in a rendered subtree. The rewrite is in place
  (no dead overridden declaration). The three machine-parsable tables share the single rule and are all
  visible in `p3.png`.
- **SC2 (contrast)** — `check-02` exits 0 with `PASS: 0 failures`, including `PASS 15.48
  --color-text on --color-surface` for the header's new ground; `TEXT_MIN`/`NON_TEXT_MIN` and the whole
  script are byte-identical to HEAD; the manifest is unchanged at 53 PAIR + 1 ORDER.
- **SC3 (radius scale)** — three independent zero-counts for `--radius-lg` (full text, fence, `var()`
  references); the three surviving declarations are verbatim unchanged; no unconsumed declaration
  remains.
- **SC4 (zero visual regression)** — `#chat-input-row input` equals the resolved `--radius-pill`, all
  four corners `999px`, `min-height` 52px, and its appearance is proven unchanged by measurement: rect
  identical, element PNG byte-identical, and the only computed-style diffs are the radius surface
  (4 physical + 4 logical aliases + the deleted token's own key). `.chat-user` is 10px on three corners
  with the 8px sharp tail retained, and it is the only consumer whose appearance actually changed —
  visible in the evidence screenshot.
- **SC5 (regression + fingerprint)** — five browser gates show no new failures (the `check-05` item block
  is **IDENTICAL** to Phase 9's, exit 2 by design on item 5's two ai-smoke legs), four static gates PASS,
  pytest holds at 219/6, `node --check` passes, `.hidden` uniqueness = 1 and `!important` **declarations**
  = 1, and the fingerprint debt is triaged at 10 reports / 1 executable with `idi-09` genuinely
  re-verified against HEAD (its digest `7b82f8d1…` independently reproduced, `verification.status`
  `passed`).

**Did the post-review fix introduce a gap? No.** `7170fa5` touched only
`scripts/check-10-idi10-validation.py` and its log; `frontend/style.css` is untouched by it. The fix is
effective (token assertions now hard-FAIL via `ok_true`), and the regenerated log's counts (t1 58, t2 51,
r1 11, r2 10) are exactly what I reproduced. The other wave-3 logs remain valid because the only input
they read — `frontend/` — is byte-identical to HEAD.

**Scope fences honored:** no new colour values, no new tokens (`--radius-lg` is a deletion), no threshold
relaxation, no new `!important`, no new `@media`/`@layer`/`@property`, no reordering, no new
dependency or build step, `check-05-ui-uat.py` untouched, and none of the five unnamed Phase 9 open items
(icons/empty-states, dark mode, `.overlay-card` fill, page-level whitespace, input UA white fill) was
touched.

---

_Verified: 2026-09-27T14:45:00Z (HEAD = `7170fa5`)_
_Verifier: [CL] (gsd-verifier)_

---
phase: idi-06-layout-robustness
plan: 04
subsystem: testing
tags: [ui-uat, playwright, harness-honesty, verification-override, layout-robustness, gap-closure]

# Dependency graph
requires:
  - phase: idi-06-layout-robustness
    provides: "plans 01-03 delivered the phase artifacts; plan 03 wrote the false 768px coverage claim this plan corrects"
provides:
  - "scripts/check-05-ui-uat.py's 768px branch states explicit 未覆盖 + measured values (no longer claims coverage it lacks)"
  - "idi-06-UI-SPEC.md A-10 narrowing registration + in-place L-2 判据表 annotation"
  - "idi-06-VERIFICATION.md frontmatter override entry for the narrowed LAYOUT-02 promise (accepted_by/accepted_at filled, overrides_applied left 0)"
  - "in-place 【更正 2026-09-22】 notes in idi-06-03-PLAN.md / idi-06-03-SUMMARY.md"
affects: [idi-06-verify-work, phase-7, phase-8]

# Actuals (#2632) — same estimateTokens scale as the plan's `estimate` (chars/4 over the realized diff)
actuals:
  tokens: 4585
  tasks: 3
  commits: 3
  plan_head_before: 3c3db94f07cf0cba3e61bf34e96dd5daa6981335

tech-stack:
  added: []
  patterns:
    - "A gate that claims coverage it does not have is worse than no gate — correct the claim to the measured truth rather than widen the assertion"
    - "Wording narrowing follows the A-5 precedent: register in the plan + verification record only; never edit REQUIREMENTS.md / ROADMAP.md (editing them invalidates the passing verification digest)"
    - "Override entries live in VERIFICATION.md frontmatter only — the verifier never reads a same-named YAML block in the body"

key-files:
  created: []
  modified:
    - scripts/check-05-ui-uat.py
    - .planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md
    - .planning/phases/idi-06-layout-robustness/idi-06-VERIFICATION.md
    - .planning/phases/idi-06-layout-robustness/idi-06-03-PLAN.md
    - .planning/phases/idi-06-layout-robustness/idi-06-03-SUMMARY.md

key-decisions:
  - "Remediation (b) implemented, (a) explicitly not attempted: no layout change, no new assertion, no @media guard, #stream-banner and --doc-panel-w untouched"
  - "768px branch stays read-only info(); the 1440/1024 hard assertions and the :1834 badge x banner assertion are untouched verbatim, pinned by two text-identity gates (each == 2) that a count gate (>=13) cannot catch"
  - "The correction notes paraphrase the stale claim rather than reproducing it, so the occurrence count stays at 2 (neither dropped nor raised) — a note that echoed the literal would fail the gate on a correct correction"
  - "overrides_applied deliberately left at 0 so re-verification walks the apply path and yields PASSED (override)"
  - "ROADMAP.md / REQUIREMENTS.md left untouched by this plan (A-5 precedent); ROADMAP progress bookkeeping is the orchestrator's"

patterns-established:
  - "Text-identity gates complement count gates: assert the exact literal count (==2) so renaming a label or rewriting a reason string — a weakening that assertion counts cannot see — fails immediately"

requirements-completed: [LAYOUT-01, LAYOUT-02, LAYOUT-03, LAYOUT-04, A11Y-07]

coverage:
  - id: D1
    description: "scripts/check-05-ui-uat.py's 768px branch no longer claims the badge x banner assertion covers LAYOUT-02's 768px 'no content occlusion' promise; it states explicit 未覆盖 with the falsifying measurements and points at the §L-2 / A-10 registration"
    requirement: "LAYOUT-02"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 8 -> PASS, 13 assertions, 0 FAIL, 0 BLOCKED"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 9 -> PASS, 16 assertions, 0 FAIL, 0 BLOCKED"
        status: pass
      - kind: unit
        ref: "grep -c '不相交断言覆盖' scripts/check-05-ui-uat.py -> 0; grep -c 'LAYOUT-02 的字面承诺' -> 2; grep -c '#state-badge 与 #stream-banner 不相交' -> 2"
        status: pass
    human_judgment: false
  - id: D2
    description: "idi-06-UI-SPEC.md registers the narrowing: an A-10 row in the 契约修正登记 table (A-1..A-9 not renumbered) plus an in-place annotation on the §L-2 判据表 row"
    requirement: "LAYOUT-02"
    verification:
      - kind: unit
        ref: "grep -c 'A-10' idi-06-UI-SPEC.md -> 3; grep -n 'badge 不被横幅遮挡' -> hits; grep -c '表头 × 正文' -> 2 (row annotated, not deleted)"
        status: pass
    human_judgment: false
  - id: D3
    description: "idi-06-VERIFICATION.md frontmatter carries the LAYOUT-02 override with accepted_by/accepted_at filled; the verifier's body YAML template with the two {待人工填写} placeholders is removed and replaced by a prose provenance note"
    requirement: "LAYOUT-02"
    verification:
      - kind: unit
        ref: "awk '/^---$/{n++; next} n==1' <VERIFICATION.md> | grep -c 'accepted_by: \"Jack11111eee\"' -> 1; same scope 'overrides_applied: 0' -> 1; whole-file grep -c '待人工填写' -> 0; python3 yaml.safe_load parses frontmatter"
        status: pass
    human_judgment: false
  - id: D4
    description: "idi-06-03-PLAN.md (:37, :212) and idi-06-03-SUMMARY.md (:150) carry in-place 【更正 2026-09-22】 notes; the original sentences remain visible"
    requirement: "LAYOUT-02"
    verification:
      - kind: unit
        ref: "grep -c '【更正 2026-09-22】' -> 2 and 1; grep -c '不相交断言覆盖' idi-06-03-PLAN.md -> 2 (neither dropped nor raised)"
        status: pass
    human_judgment: false
  - id: D5
    description: "The zero-diff invariants hold: frontend/style.css, frontend/index.html, frontend/app.js, frontend/vendor/, .planning/REQUIREMENTS.md, .planning/ROADMAP.md all unchanged by this plan"
    requirement: "LAYOUT-01"
    verification:
      - kind: unit
        ref: "git status --porcelain -- frontend/ .planning/REQUIREMENTS.md .planning/ROADMAP.md -> empty"
        status: pass
    human_judgment: false
  - id: D6
    description: "The reader test: anyone opening scripts/check-05-ui-uat.py's 768px region can read (1) what LAYOUT-02's 768px promise was, (2) that it was narrowed, (3) the exact falsifying measurements, (4) where the narrowing is registered"
    verification: []
    human_judgment: true
    rationale: "This is the plan's stated single success criterion and it is a judgment about what a human reader can extract from prose. No automated check can decide whether the wording is legible to a reader who has never seen the gap; the machine gates only prove the required facts and literals are present."

duration: 16min
completed: 2026-09-22
status: complete
---

# Phase 6 Plan 04: LAYOUT-02 768px Promise Narrowing Summary

**Narrowed LAYOUT-02's 768px promise to "badge not occluded by the banner", made check-05's 768px branch say explicitly that it does NOT cover the occlusion, and registered the deviation as an A-10 entry plus a frontmatter override — with zero layout change.**

## Performance

- **Duration:** 16 min
- **Started:** 2026-09-22T07:19:08Z
- **Completed:** 2026-09-22T07:35:18Z
- **Tasks:** 3
- **Files modified:** 5

## Accomplishments

- **The gate now tells the truth about itself.** `scripts/check-05-ui-uat.py`'s 768px branch (:1933 comment, :1945-1946 `info()` string) previously claimed LAYOUT-02's "no content occlusion" promise was covered by the badge × banner assertion at :1834. That assertion only tests `#state-badge`, and it passes cleanly at exactly the widths where the real occlusion occurs. Both claims now read as an explicit **未覆盖**, carrying the falsifying measurements (h1 = 439.0–481.0 × 8–28 vs banner = 285.3–482.7 × 12–39, overlap 42×16px, intersection band 768–855px) and pointing at the registration site (`idi-06-UI-SPEC.md` §L-2 / A-10). A reader no longer has to re-measure, and can no longer mistake this for a PASS.
- **The narrowing is visibly registered, not silently applied.** `idi-06-UI-SPEC.md` gains an **A-10** row in the 契约修正登记 table (A-1…A-9 untouched and not renumbered) recording the narrowed object, the scope-lock basis (`#stream-banner` declarations locked at :665, `--doc-panel-w` value reserved to the user at `frontend/style.css:224-227`, and the only legal `@media` form being geometrically impossible — it would need a panel ≤285.3px against a 340px clamp floor), the measured values, and that it follows the A-5 precedent as a **registered deviation**. The §L-2 判据表 row is annotated in place: of the three named pairs, only `badge × banner` was ever measured; `表头 × 正文` and `按钮 × 视口` were never measured and the narrowed promise does not claim them. The table row is kept, not deleted or reordered.
- **The override is real and in the only place that counts.** `idi-06-VERIFICATION.md` frontmatter now carries the `overrides:` entry with `accepted_by: "Jack11111eee"` (the repo git identity) and `accepted_at: "2026-09-22T06:43:50Z"`, while `overrides_applied` stays **0** so re-verification walks the apply path and produces `PASSED (override)`. The verifier's body template (a fenced `yaml` block holding two `{待人工填写}` placeholders) was removed and replaced by a prose provenance note — copying that YAML into the body would have put `accepted_by` in the file twice, broken the "exactly one" frontmatter gate, and created an override that is never read.
- **The stale claim is corrected in the record, not erased from it.** `idi-06-03-PLAN.md` (:37, :212) and `idi-06-03-SUMMARY.md` (:150) each get an in-place `【更正 2026-09-22】` note. The original sentences remain visible, so each file shows both what was claimed at the time and what is actually true. The notes **paraphrase** the stale phrase rather than reproducing it, so the literal count stays at 2 — a note that echoed it would have tripped the gate on a correct correction.

### Override provenance (restated as the plan's `<output>` requires)

The acceptance came from the **project owner's explicit selection of remediation (b) in this session** — "Narrow the promise, fix the claim" — **not** from an executor's unilateral call. `accepted_by` is the repo's git identity (`Jack11111eee`, the only identifier available to the accepting party); `accepted_at` is this session's decision timestamp. `overrides_applied` was left at **0 deliberately**, so that re-verification applies the override itself and records `PASSED (override)` rather than inheriting a pre-applied count. The prose provenance line in the report body states the same, and contains no `accepted_by:` / `accepted_at:` keys.

### Re-verification note (for the next reader)

Editing `idi-06-03-PLAN.md`, `idi-06-03-SUMMARY.md` and `idi-06-VERIFICATION.md` changes files listed in the verification's `covered_files`, so `covered_digest` **will** differ at the next verification. **That is the expected result of a gap-closure round, not a drift failure.** The follow-up verification is a fresh re-verification (`re_verification.previous_status` records the prior status); do not read the digest change as a defect.

## Task Commits

Each task was committed atomically:

1. **Task 1: 让 768px 分支说出实测真相(检查门自身诚实)** - `b15bd89` (fix)
2. **Task 2: 在 UI-SPEC 登记收窄(A-10 行 + §L-2 判据表注解)** - `62efa70` (docs)
3. **Task 3: 填实 override 条目 + 更正历史记录里的失效主张** - `24be8d8` (docs)

**Plan metadata:** `pending` (docs: complete plan)

_All gates for each task were run BEFORE that task's commit — the scope-lock gates observe `git status --porcelain`, which would pass vacuously on a clean tree._

## Files Created/Modified

- `scripts/check-05-ui-uat.py` — the :1933 comment and the :1945-1946 `info()` string rewritten to explicit 未覆盖 + measured values. The only diff in this file is those two claim rewrites; **no assertion was touched**.
- `.planning/phases/idi-06-layout-robustness/idi-06-UI-SPEC.md` — A-10 row appended to the 契约修正登记 table; §L-2 判据表 row annotated in place.
- `.planning/phases/idi-06-layout-robustness/idi-06-VERIFICATION.md` — frontmatter `overrides:` entry added; body YAML template removed and replaced with prose provenance.
- `.planning/phases/idi-06-layout-robustness/idi-06-03-PLAN.md` — two `【更正 2026-09-22】` notes appended in place.
- `.planning/phases/idi-06-layout-robustness/idi-06-03-SUMMARY.md` — one `【更正 2026-09-22】` note appended in place.

## Decisions Made

- **Remediation (b) only.** No layout change, no new assertion, no `@media` guard, no touch to `#stream-banner`'s declarations or to the value of `--doc-panel-w`. The 768px branch stays a read-only `info()`.
- **Pinned the surviving literals with text-identity gates.** `LAYOUT-02 的字面承诺` must stay at exactly 2 occurrences (:1931 comment + :1941 `ok_true` reason string) and `#state-badge 与 #stream-banner 不相交` at exactly 2 (:1825 + :1834 labels). The assertion-count gates (≥13 / ≥16) cannot see a label widened or a reason string made vague; these two gates can.
- **The correction notes paraphrase, never reproduce, the stale literal** — so the count neither drops (which would mean the original sentence was deleted) nor rises (which would mean the note echoed it).
- **`overrides_applied` stays 0**; the re-verifier owns that count.
- **`ROADMAP.md` / `REQUIREMENTS.md` deliberately not edited** (A-5 precedent: editing them invalidates the passing verification digest). ROADMAP progress bookkeeping belongs to the orchestrator, so `roadmap update-plan-progress` and `requirements mark-complete` were **not** run by this plan.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Repaired the STATE.md progress rollup clobbered by the state.* tooling**

- **Found during:** the post-execution STATE.md update step
- **Issue:** As the orchestrator's briefing predicted (`.planning/STATE.md` line ~211 tracks this as acknowledged tech debt), `state.advance-plan` and `state.update-progress` clobbered the rollup: `progress.completed_phases` 3 → **0**, `progress.percent` 50 → **0**, the body line `Progress: [█████░░░░░] 50%` → `[░░░░░░░░░░] 0%`. `state.advance-plan` also reported `previous_plan: 1, current_plan: 2` because the orchestrator's `state.begin-phase` had reset the counter to 1 of 4. `state.add-decision` clobbered the same three fields **a second time** after the first repair.
- **Fix:** Restored the four values by hand to their authoritative levels (`completed_phases: 3`, `percent: 50`, body line `[█████░░░░░] 50%`, `current_phase_name: 布局稳健性` — the last was never clobbered). Also set `Current Position` to the truthful `Plan: 4 of 4 (all plans executed; awaiting /gsd-verify-work idi-06)`, since leaving the tool-written `Plan: 2 of 4` would have been plainly false after all four plans gained SUMMARYs. Fixed the matching `next.reason` in `state.json` (`· 0% ·` → `· 50% ·`). Repaired **after** all `state.*` calls, so nothing re-clobbered it.
- **Files modified:** `.planning/STATE.md`, `.planning/state.json`
- **Verification:** re-grepped all four fields; `completed_phases: 3`, `percent: 50`, `Progress: [█████░░░░░] 50%`, `current_phase_name: 布局稳健性`; the decision line from this plan is present exactly once.
- **Committed in:** plan metadata commit

---

**Total deviations:** 1 auto-fixed (1 bug — tooling clobber of shared state, not a plan-intent deviation)
**Impact on plan:** None on deliverables. The repair is confined to STATE.md / state.json bookkeeping and restores the values that were correct before the tooling ran.

## Issues Encountered

- **`--item 5` reports 2 BLOCKED in the full `check-05` run, and that is pre-existing by design.** The two blocked rows are the real-AI smoke assertions, which the harness skips unless `--ai-smoke` is passed ("需要真实 AI 调用,默认不执行"). Verified pre-existing rather than assumed: the same block strings occur twice in `git show HEAD~3:scripts/check-05-ui-uat.py`, and `git diff HEAD~3 HEAD -- scripts/check-05-ui-uat.py` contains **only** the two claim rewrites — no assertion line is touched. So the full run's `exit=2` is baseline-equivalent, not a regression.
- **Plan verification item 5 names `check-03` / `check-04` without a suffix**; the actual files are `check-03-hidden-uniqueness.sh` and `check-04-important-count.sh`. All four static gates (`check-01`, `check-02`, `check-03`, `check-04`) plus `check-06` were run and all PASS.
- **`roadmap update-plan-progress` and `requirements mark-complete` were intentionally not run** — both edit files this plan's prohibitions and zero-diff invariant protect (see Decisions Made).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- All four `idi-06` plans now have SUMMARYs. The phase awaits `/gsd-verify-work idi-06`, which should now yield `PASSED (override)` for the LAYOUT-02 768px truth once the frontmatter override is applied.
- The `covered_digest` for `idi-06` will differ on the next verification because this plan edited three of its `covered_files`. This is the expected gap-closure outcome (see the Re-verification note above).
- Five advisory findings (WR-01, WR-02, WR-03, IN-01, IN-02) remain registered as non-blocking in the verification. This plan planned no work for them and did not investigate or fix them, per its scope boundary. Note that `idi-06-REVIEW.md`'s **WR-02 is refuted** — the `judged` filter excludes exactly the rows the reviewer claimed it mishandles — and was left alone.

---

*Phase: idi-06-layout-robustness*
*Completed: 2026-09-22*
---
phase: "idi-04.1"
slug: "radix"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: false
wave_0_complete: true
created: "2026-09-20"
---

# Phase idi-04.1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

**Phase:** Radix 颜色族重写 (INSERTED) — 值层重写,4 个 plan(含 gap-closure plan 04)
**Reconstructed** from artifacts (State B): no VALIDATION.md was seeded at plan time; this file was built from the four PLAN/SUMMARY pairs plus the live guard commands, all of which the orchestrator re-ran.

**Verdict: VALIDATED (PARTIAL).** 9 of 10 requirements have automated verification. One requirement — **TOKEN-07** — has a *stated* invariant with no mechanized assertion; the user elected to record it manual-only rather than add a new test after the phase was already verified. `nyquist_compliant: false`.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x (`.venv`), plus four standalone zero-dependency guard commands |
| **Config file** | `pytest.ini` |
| **Quick run command** | `.venv/bin/python -m pytest -q` |
| **Full suite command** | `.venv/bin/python -m pytest -q` **and** `bash scripts/check-01-token-conformance.sh` **and** `.venv/bin/python scripts/check-02-contrast.py` **and** `bash scripts/check-03-hidden-uniqueness.sh` **and** `bash scripts/check-04-important-count.sh` **and** `.venv/bin/python scripts/check-05-ui-uat.py` |
| **Estimated runtime** | ~6s (pytest) + ~90s (check-05, needs a browser) |

**Important:** the guard scripts are the phase's real verification surface. They are *not* invoked by the pytest suite — `backend/tests/` tests the application's own modules (`checks`, sessions, routes, e2e), and no test file references `check-01`…`check-05`. Each guard is a standalone executable with its own PASS/FAIL exit code and must be run separately.

**pytest baseline:** `219 passed, 6 skipped`. (Use the project `.venv` — the environment `python3` is a miniconda install and produces 4 spurious `ai_caller` failures.)

---

## Sampling Rate

- **After every task commit:** Run the affected guard command only
- **After every plan wave:** Run `check-01`…`check-04` plus `.venv/bin/python -m pytest -q`
- **Before `/gsd-verify-work`:** All four guards green **and** `check-05` at 0 FAIL **and** pytest green
- **Max feedback latency:** ~90 seconds (dominated by `check-05`'s browser run)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 04.1-01-01…03 | 01 | 1 | TOKEN-01 | T-idi041-03 | 围栏内 tier-1 隐私不变量成立(围栏外不得直接引用 primitive) | integration | `bash scripts/check-01-token-conformance.sh` | ✅ | ✅ green |
| 04.1-01-01…03 | 01 | 1 | TOKEN-02 | — | 围栏内无裸 hex,全部走 `var(--…)` | integration | `bash scripts/check-01-token-conformance.sh` | ✅ | ✅ green |
| 04.1-01-01…03 | 01 | 1 | TOKEN-04 | — | 令牌层结构契约(单一围栏、无裸 hex/rgba) | integration | `bash scripts/check-01-token-conformance.sh` | ✅ | ✅ green |
| 04.1-01-01…03 | 01 | 1 | **TOKEN-07** | — | z-index 四个令牌的**序关系** `--z-badge < --z-banner < --z-overlay < --z-selection-menu` | — | **无机械断言**(见 Manual-Only) | ❌ | ⚠️ PARTIAL |
| 04.1-02-01…02 | 02 | 2 | CHECK-01 | T-idi041-05 | tier-1 交替式覆盖 `radix`,泄漏时真的会 FAIL(附变异证明) | integration | `bash scripts/check-01-token-conformance.sh` | ✅ | ✅ green |
| 04.1-01/03/04 | 01,03,04 | 1,3,4 | CHECK-02 | T-idi041-15 | 43 对对比度配对全部达标,含 `ORDER` 序断言 | integration | `.venv/bin/python scripts/check-02-contrast.py` | ✅ | ✅ green |
| 04.1-01/02/03 | 01,02,03 | 1,2,3 | CHECK-03 | — | `hidden` 类唯一性不变量 | integration | `bash scripts/check-03-hidden-uniqueness.sh` | ✅ | ✅ green |
| 04.1-01/02/03 | 01,02,03 | 1,2,3 | CHECK-04 | — | `!important` 计数不超过契约上限 | integration | `bash scripts/check-04-important-count.sh` | ✅ | ✅ green |
| 04.1-01/03/04 | 01,03,04 | 1,3,4 | A11Y-04 | T-idi041-15 | AA 对比度无倒退(`--color-text-muted` 3.23:1 → 达标) | integration | `.venv/bin/python scripts/check-02-contrast.py` | ✅ | ✅ green |
| 04.1-01/03 | 01,03 | 1,3 | A11Y-04b | — | `.tier-desc` 的 opacity 越轨已消除 | e2e | `.venv/bin/python scripts/check-05-ui-uat.py` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

**Orchestrator re-run evidence (2026-09-20, not taken from any SUMMARY):**

| Command | Result |
|---------|--------|
| `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped` |
| `bash scripts/check-01-token-conformance.sh` | `PASS`, exit 0 |
| `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures` (incl. `ORDER 0.363 --color-text-muted before --color-text on --color-surface`), exit 0 |
| `bash scripts/check-03-hidden-uniqueness.sh` | `PASS`, exit 0 |
| `bash scripts/check-04-important-count.sh` | `PASS`, exit 0 |
| `.venv/bin/python scripts/check-05-ui-uat.py` | 0 FAIL; `item 1 PASS (45,0,0)` / `2 PASS (5,0,0)` / `3 PASS (15,0,0)` / `4 PASS (24,0,0)` / `5 BLOCKED (9,0,2)` / `6 PASS (2,0,0)`; `exit=2` — item-by-item identical to VERIFICATION.md P3.7 |
| `.venv/bin/python scripts/probe-05-resolve-color.py` | `mutated-prefix-verdict=PASS` / `mutated-postfix-verdict=BLOCKED` / `control-verdict=PASS`, exit 0 |

`check-05`'s exit code 2 is by design (`code = 1 if any_fail else (2 if any_blocked else 0)`); the two BLOCKED items are exactly the two recorded AI-smoke items that require a real AI call. **Any CI gate keyed on `exit == 0` for the default run is permanently red** — already documented as IN-03 in VERIFICATION.md.

---

## Wave 0 Requirements

- [x] No framework install needed — pytest 8.x and the four guards were already in place before this phase
- [x] `pytest.ini` present
- [x] `.venv` provisioned with Playwright 1.63.0 + bundled chromium-1243

*Existing infrastructure covers all phase requirements except TOKEN-07's ordering half (see below).*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| z-index 四令牌的**序关系** `--z-badge (10) < --z-banner (20) < --z-overlay (100) < --z-selection-menu (200)` 成立,且 `badge < banner` 这条**承重**关系不被反转 | TOKEN-07 | 该不变量只在 `frontend/style.css:229-231` 的散文注释里陈述,**没有任何机械断言**。`check-05-ui-uat.py:771-776` 断言的是「元素 `z-index` **等于**其令牌」(D-14 接线形式),不是「令牌之间的大小序」。把四个值重新排序后,`check-01`…`check-05` **全部仍会通过** —— 这正是本阶段反复出现的失败类(陈述了却守不住的不变量)。代码库里已有同型模式:`check-02-contrast.py` 对颜色输出 `ORDER 0.363 …`,z-index 只是缺这一条。 | 1. `grep -nE '^\s*--z-' frontend/style.css` 读出四个值<br>2. 人工核对 `badge < banner < overlay < selection-menu`<br>3. `grep -n 'z-index: var(--z-' frontend/style.css` 确认四个令牌各有消费者(`:537` overlay / `:590` badge / `:606` banner / `:889` selection-menu)<br>4. 若要机械覆盖:按 `check-02-contrast.py` 的 `ORDER` 形式加一条断言(用户已裁定本 run 不加) |
| `--z-overlay` 的运行时消费者断言 | TOKEN-07 | 四个 z-index 令牌中,`item4` 只对 `--z-selection-menu` / `--z-badge` / `--z-banner` 做了接线断言;`--z-overlay` 有消费者(`style.css:537`)但无运行时断言 | 同上的第 3 步覆盖静态侧;运行时侧需人工在 `item4` 观察 |

*除 TOKEN-07 的序关系半场外,其余全部相位行为均有自动化验证。*

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 120s
- [ ] `nyquist_compliant: true` set in frontmatter — **not set; TOKEN-07 remains PARTIAL**

**Approval:** validated 2026-09-20 — PARTIAL (9/10 requirements automated)

---

## Validation Audit 2026-09-20

| Metric | Count |
|--------|-------|
| Gaps found | 1 |
| Resolved | 0 |
| Escalated | 1 (TOKEN-07 → Manual-Only, per user decision) |

**Note on scope:** this audit ran *after* the phase had already been verified and its sole blocker (CR-01) closed. The TOKEN-07 gap is pre-existing and was already visible as **W-6** in VERIFICATION.md's warnings table — it is not a regression introduced by plan 04. `REQUIREMENTS.md` marks TOKEN-07 `Complete` on the strength of its "ordering assertion regained a consumer" half; this file records that the *mechanization* half remains uncovered, so the two documents should not be read as disagreeing silently.
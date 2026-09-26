---
phase: "idi-05"
slug: "typography-and-visual-hierarchy"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: "2026-09-21"
---

# Phase idi-05 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

**Phase:** 排版与视觉层级 — 字号刻度 / 字重分工 / 不可逆动作视觉处理 / 活动面板标记 / 掩码字形,3 个 plan
**Reconstructed** from artifacts (State B): no VALIDATION.md was seeded at plan time; this file was built from the three PLAN/SUMMARY pairs plus the live guard commands, all of which the orchestrator re-ran on 2026-09-21.

**Verdict: VALIDATED (COMPLIANT).** All 8 requirements have automated behavioral verification. The audit found a **systematic blind spot** in the phase's automated surface and closed it with one new harness — see below.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x (`.venv`), plus six standalone zero-dependency guard commands |
| **Config file** | `pytest.ini` |
| **Quick run command** | `.venv/bin/python -m pytest -q` |
| **Full suite command** | `.venv/bin/python -m pytest -q` **and** `bash scripts/check-01-token-conformance.sh` **and** `.venv/bin/python scripts/check-02-contrast.py` **and** `bash scripts/check-03-hidden-uniqueness.sh` **and** `bash scripts/check-04-important-count.sh` **and** `.venv/bin/python scripts/check-05-ui-uat.py --item 1,2,3,4,6` **and** `.venv/bin/python scripts/check-06-idi05-validation.py` |
| **Estimated runtime** | ~8s (pytest) + ~90s (check-05, needs a browser) + ~90s (check-06, needs a browser) |

**Important:** the guard scripts are the phase's real verification surface. They are *not* invoked by the pytest suite — `backend/tests/` tests the application's own modules (`checks`, sessions, routes, e2e), and no test file references `check-01`…`check-06`. Each guard is a standalone executable with its own PASS/FAIL exit code and must be run separately.

**pytest baseline:** `219 passed, 6 skipped`. (Use the project `.venv` — the environment `python3` is a miniconda install and produces 4 spurious `ai_caller` failures.)

**`check-06-idi05-validation.py` is new in this audit.** It reuses `check-05`'s module facilities (server lifecycle, fixture isolation, `ok`/`read_style`/`resolve_token`) via `importlib` and does not modify `check-05`. It adds behavioral (not wiring) assertions — see "Why a sixth harness exists" below.

---

## Sampling Rate

- **After every task commit:** Run the affected guard command only
- **After every plan wave:** Run `check-01`…`check-06` plus `.venv/bin/python -m pytest -q`
- **Before `/gsd-verify-work`:** All six guards green **and** pytest green
- **Max feedback latency:** ~90 seconds (dominated by the two browser-driven harnesses)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| idi-05-01-01 (tracer) | 01 | 1 | TYPE-01 | T-idi-05-03, T-idi-05-04 | 无全局 `h1, h2, h3` 规则泄漏到 chrome | integration | `.venv/bin/python scripts/check-05-ui-uat.py --item 4` (65) + `check-06 --item g1` (9) | ✅ | ✅ green |
| idi-05-01-02 | 01 | 1 | TYPE-02, TYPE-01 | T-idi-05-02 | 围栏注释与代码一致(档数 7、行高比率配对) | integration | `.venv/bin/python scripts/check-05-ui-uat.py --item 4` | ✅ | ✅ green |
| idi-05-01-03 | 01 | 1 | TYPE-03 | T-idi-05-01 | 字重三档分工显式化,`--fw-*` 无孤儿档 | integration | `.venv/bin/python scripts/check-05-ui-uat.py --item 4` (6 条字重断言) | ✅ | ✅ green |
| idi-05-02-01 (tracer) | 02 | 2 | VISUAL-01, VISUAL-02 | T-idi-05-01 | 三档坡道两两不同、档内相同;AA 无倒退 | integration | `.venv/bin/python scripts/check-05-ui-uat.py --item 3` (17) + `check-02-contrast.py` (47 pairs) | ✅ | ✅ green |
| idi-05-02-02 | 02 | 2 | VISUAL-01 | T-idi-05-01 | `--color-action-irreversible*` 保持单消费者(D-15) | integration | `.venv/bin/python scripts/check-05-ui-uat.py --item 3` + `check-06 --item g5` (5) | ✅ | ✅ green |
| idi-05-02-03 | 02 | 2 | VISUAL-03 | T-idi-05-03 | chrome 标题未被文档标题改动带偏 | integration | `.venv/bin/python scripts/check-05-ui-uat.py --item 4` + `check-06 --item g2` (2) | ✅ | ✅ green |
| idi-05-03-01 (tracer) | 03 | 3 | VISUAL-04 | T-idi-05-01, T-idi-05-04 | 活动标记仅命中三选一面板;`#ai-panel` 对照恒 `none` | integration | `.venv/bin/python scripts/check-05-ui-uat.py --item 4` / `--item smoke` + `check-06 --item g3` (12), `--item g6` (7) | ✅ | ✅ green |
| idi-05-03-02 | 03 | 3 | VISUAL-05 | T-idi-05-05 | data-URI 零颜色信息,不引入外部资源 | integration | `.venv/bin/python scripts/check-05-ui-uat.py --item 4,6` + `check-06 --item g4` (5) | ✅ | ✅ green |
| idi-05-03-03 | 03 | 3 | VISUAL-04, VISUAL-05 | T-idi-05-02, T-idi-05-SC | 本阶段零安装;`frontend/vendor/` 仍只含 `marked.min.js` | integration | `bash scripts/check-01-token-conformance.sh` && `check-03` && `check-04` + `check-05 --item 1,2,3,4,6` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

### Why a sixth harness exists (the blind spot this audit closed)

Every `check-05` assertion derives its **expected** value from `resolve_token()` at runtime. That makes the assertions **agnostic to the value itself**: they prove a declaration is *wired* to a token, never that the token's value is *correct*. Six genuine gaps followed from this, all confirmed by reading the assertion code rather than the summaries:

| Gap | Blind to | Closed by |
|-----|----------|-----------|
| TYPE-01 | **ordering** — `--text-2xl: 30px` passes all 12 wiring assertions while destroying "三级标题层级分明" | `g1` — strict `h1>h2>h3` per host + token ordering |
| VISUAL-01 | the "不换行" half was **arithmetic only**; `check-05` never pressed the panel to 340px | `g5` — presses to 340px, counts line boxes via `Range.getClientRects()` |
| VISUAL-03 | the chain compares only 4 **named** elements; any 5th could be enlarged unnoticed | `g2` — scans every visible element on the page |
| VISUAL-04 | (a) computed `box-shadow` says nothing about a descendant with an opaque background painting over the 3px band — the exact reason D-17 moved the bar onto `.panel-header`; (b) **no test executed the collapse toggle** | `g3` — occlusion/edge/overflow geometry; `g6` — clicks the indicator through a full round-trip |
| VISUAL-05 | "不撑高行盒" was **inferred** from `12px < line-height`, never measured | `g4` — differential measurement (host height with `::before` visible vs suppressed via injected `display:none`) |

**Falsifiability proof (mutation testing).** Each CSS-mutable guard was mutated at runtime via `page.add_init_script` (survives navigation, touches no repo file) and the real `check-06` item functions were re-run:

| Guard | Mutation | Result |
|-------|----------|--------|
| g1 | `.markdown-body h2 { font-size: 30px }` | **FAIL** — `28px > 30px > 18px` ×4 hosts |
| g2 | `#chat-greeting { font-size: 40px }` | **FAIL** — `max_other=40px` |
| g3 | `.panel-header { padding-left: 0 }` + opaque h2 bg | **FAIL** — occluder detected `H2. rgb(255,0,0) left=120 w=42`, `h2Delta=0px` ×7 |
| g4 | `::before { height: 40px }` | **FAIL** — `with=43 without=20` |
| g5 | `#btn-authorize { font-size: 40px }` | **FAIL** — `lineBoxes=2` (wrapped) |
| g6 | negative control: click a header with no handler | no toggle; same-page handled header toggles — proves the observation is non-vacuous |

**Orchestrator re-run evidence (2026-09-21, not taken from any SUMMARY):**

| Command | Result |
|---------|--------|
| `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped` |
| `bash scripts/check-01-token-conformance.sh` | `PASS`, exit 0 |
| `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures` (47 pairs), exit 0 |
| `bash scripts/check-03-hidden-uniqueness.sh` | `PASS`, exit 0 |
| `bash scripts/check-04-important-count.sh` | `PASS`, exit 0 |
| `.venv/bin/python scripts/check-05-ui-uat.py --item 1,2,3,4,6` | `item 1 PASS (45)` / `2 PASS (5)` / `3 PASS (17)` / `4 PASS (65)` / `6 PASS (6)`; `exit=0` |
| `.venv/bin/python scripts/check-05-ui-uat.py --item smoke` | `PASS (8)`, exit 0 |
| `.venv/bin/python scripts/check-06-idi05-validation.py` | `g1 PASS (9)` / `g2 PASS (2)` / `g3 PASS (12)` / `g4 PASS (5)` / `g5 PASS (5)` / `g6 PASS (7)`; `exit=0` |

---

## Wave 0 Requirements

- [x] No framework install needed — pytest 8.x and the four original guards were already in place before this phase
- [x] `pytest.ini` present
- [x] `.venv` provisioned with Playwright + bundled chromium
- [x] `scripts/check-06-idi05-validation.py` added by this audit (the phase's Wave-0 equivalent for the six closed gaps)

*Existing infrastructure covers all phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| D-16 口径裁决:「侧栏四个面板…可区分」按「**三选一活动态 + AI 面板折叠态**」收窄被接受 | VISUAL-04 | 这是**需求措辞的裁决**,不是行为。没有任何可执行的东西,也没有测试能失败。`REQUIREMENTS.md` 的 VISUAL-04 原文写「四个面板」,而 ROADMAP SC4 只列三个面板 + 「`#ai-panel` 的折叠行为不变」;D-16 已登记该收窄且明写「本阶段不改 `REQUIREMENTS.md`(改它会作废指纹)」。行为半边已由 `check-06 --item g3` / `g6` 机器化覆盖 —— 缺的只是口径确认 | 人工确认该收窄被接受。若要求给 AI 面板也加活动标记,那是**新的范围**,应另开阶段而非在此补测 |

*除 VISUAL-04 的口径裁决半场外,其余全部相位行为均有自动化验证。*

**Note:** this item was carried as UAT test #5 and **passed** on 2026-09-21 — the adjudication is accepted.

---

## Observations (reported, not escalated)

1. **`.panel-header` has `border-top-left-radius: 10px`** (measured). The `inset 3px 0 0` marker is clipped along the rounded border box, so the bar tapers over the top ~10px of the 36px header. This is precisely the "不因 border-radius 在角落断开" backstop (E4/E5). Human UAT #1 passed it, so `check-06` does **not** assert `radius == 0px` — that would over-strictly assert an adjudicated design judgment. Printed as INFO in `g3`.
2. **The strict "最重" reading of VISUAL-03/E8 is false and is deliberately not asserted.** `#draft-view > h2` computes to `font-weight: 700` (browser default — no rule sets it) vs the document h1's 600. The requirement's actual claim is about the container label 「文档区」 (14px/500), which `g2` does assert. Asserting "doc h1 is globally heaviest" would fail for a non-requirement. Human UAT #3 (E8「读起来是否分明」) **passed**, which is the judgment that actually governs.
3. `g5` and `g4`'s `.verdict-location` half are **state-dependent**: `#authorize-row` is hidden in `checking`, and `#verdict-cards` is hidden in `p3`. Both are guarded to emit **BLOCKED** rather than silently pass, so a state drift cannot turn them vacuous.

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 180s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** validated 2026-09-21 — COMPLIANT (8/8 requirements automated)

---

## Validation Audit 2026-09-21

| Metric | Count |
|--------|-------|
| Gaps found | 6 |
| Resolved | 6 |
| Escalated | 0 |
| Explicit skips | 1 (VISUAL-04 D-16 口径裁决 — decision, not behavior) |

**Debug iterations:** 1/3. The single iteration was a **test bug, not an implementation bug**: `g6`'s helper guessed that the collapse toggle target was the header, but `#doc-panel`'s handler puts `.collapsed` on the `aside`. Observed behavior was already correct (display `none`↔`block`, indicator `▸`↔`▾`); fixed by passing an explicit toggle-target selector.

**Note on scope:** this audit ran *after* the phase had been verified (`8/8 must-haves verified`) and after human UAT completed 6/6. The phase's `8/8` claim holds for *value-level* evidence; what this audit adds is that the automated surface previously could not distinguish "correct value" from "any value wired to a token". `REQUIREMENTS.md` and this file should therefore not be read as disagreeing silently — the requirements were already met; the *mechanization* of their invariants is what this file newly records.
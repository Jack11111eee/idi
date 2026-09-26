---
phase: "idi-08"
slug: "accessibility-semantics-and-keyboard"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: "2026-09-24"
---

# Phase idi-08 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

**Phase:** 可访问性语义与键盘 (A11Y-02 / A11Y-03 / A11Y-05 / A11Y-06 / A11Y-08 / REG-03) — 3 个 plan,wave 1/2/3,共 9 个 task。
**Reconstructed** from artifacts (State B): no VALIDATION.md was seeded at plan time; this file was built from the three PLAN/SUMMARY pairs plus the live guard commands, all of which the orchestrator re-ran.

**Verdict: VALIDATED.** Every requirement that *can* carry automated verification now does. `nyquist_compliant: true`.

**This phase is a Nyquist-gap correction, not a formality.** At audit time the three requirements below had **zero** automated coverage — the plans' `<verify>` blocks contained only static greps (counting occurrences of an attribute in a source file), which prove a *word appears in a file*, never that the behavior exists at runtime. Two of the three had shipped a real defect:

| Requirement | Coverage before this audit | Consequence |
|-------------|---------------------------|-------------|
| **A11Y-05** (Escape closes both blocking modals) | **none** — the string `Escape` appeared **nowhere** in `scripts/` or `backend/tests/` | the dispatcher's whole contract was unasserted |
| **A11Y-06** (dialog semantics + background `inert`) | **none** — `aria-modal` / `inert` / `aria-labelledby` appeared **only** in `frontend/index.html` + `frontend/app.js` | greps would still pass if `inert` were applied to the wrong element, never applied, or never removed |
| **A11Y-03** (Escape-dismissal half) | **none** — static greps only | **this is the half that shipped a defect**: the menu re-opened on the Escape keyup, requiring two fix commits (`62dfd3e`, then `09b170d`). Neither fix had a committed test |

Filled by `scripts/check-07-idi08-validation.py` (new harness, items g1/g2/g3, 70 assertions).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.x (`.venv`), plus six standalone zero-dependency guard commands and two browser harnesses |
| **Config file** | `pytest.ini` |
| **Quick run command** | `.venv/bin/python -m pytest -q` |
| **Full suite command** | `.venv/bin/python -m pytest -q` **and** `bash scripts/check-01-token-conformance.sh` **and** `.venv/bin/python scripts/check-02-contrast.py` **and** `bash scripts/check-03-hidden-uniqueness.sh` **and** `bash scripts/check-04-important-count.sh` **and** `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` **and** `.venv/bin/python scripts/check-06-idi05-validation.py` **and** `.venv/bin/python scripts/check-07-idi08-validation.py` **and** `.venv/bin/python scripts/probe-07-focus-composite.py` |
| **Estimated runtime** | ~6s (pytest) + ~90s (check-05) + ~60s (check-06) + ~40s (check-07), all browser legs headless |

**Important:** the guard scripts are the phase's real verification surface. They are *not* invoked by the pytest suite — `backend/tests/` tests the application's own modules (`checks`, sessions, routes, e2e), and no test file references `check-0N`. Each guard is a standalone executable with its own PASS/FAIL exit code and must be run separately.

**Browser route:** always `--browser bundled` (Playwright's own chromium, cached, arm64 native, headless-safe). Do **not** use `--browser chrome` headless — under this machine's x86_64 venv it hangs; that route is headed-only by design and the script enforces it.

**Never pass `--ai-smoke`** to check-05 — it makes real `claude` CLI calls and incurs real billing.

**pytest baseline:** `219 passed, 6 skipped`. (Use the project `.venv` — the environment `python3` is a miniconda install and produces 4 spurious `ai_caller` failures.)

**Guard exit codes:** `0` = all pass, `1` = at least one FAIL, `2` = at least one BLOCKED (no FAIL). Both browser harnesses use a shared assertion recorder in which a missing element or an unresolvable expected value records **BLOCKED, never PASS** — a green is never vacuous by construction.

---

## Sampling Rate

- **After every task commit:** Run the affected guard command only
- **After every plan wave:** Run `check-01`…`check-04` plus `.venv/bin/python -m pytest -q`
- **Before `/gsd-verify-work`:** All eight guards green (check-05 at 0 FAIL, check-07 at exit 0) **and** pytest green
- **Max feedback latency:** ~90 seconds (dominated by `check-05`'s browser run)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| idi-08-01-01 | 01 | 1 | A11Y-02 | — | `#round-doc` is a real Tab stop and receives the Phase 7 whole-box ring | browser (runtime Tab census) | `.venv/bin/python scripts/check-05-ui-uat.py --item 10` | ✅ | ✅ green |
| idi-08-01-02 | 01 | 1 | A11Y-02 | — | the ring stays **discernible** on every ground it can land on, incl. the archive state | browser (composite probe) | `.venv/bin/python scripts/probe-07-focus-composite.py` | ✅ | ✅ green |
| idi-08-01-03 | 01 | 1 | A11Y-03 | — | Escape dismisses the selection menu and the dismissal **holds** (no keyup re-show) | browser (runtime, trusted key) | `.venv/bin/python scripts/check-07-idi08-validation.py --item g3` | ✅ **W0** | ✅ green |
| idi-08-02-01 | 02 | 2 | A11Y-06 | — | both blocking modals carry `role="dialog"` + `aria-modal="true"` + a **resolving** `aria-labelledby` | browser (live DOM) | `.venv/bin/python scripts/check-07-idi08-validation.py --item g2` | ✅ **W0** | ✅ green |
| idi-08-02-02 | 02 | 2 | A11Y-06 | — | `#app` really becomes `inert` while a modal is open, and is released when both close | browser (attribute + IDL + focus behavior) | `.venv/bin/python scripts/check-07-idi08-validation.py --item g2` | ✅ **W0** | ✅ green |
| idi-08-02-03 | 02 | 2 | A11Y-05 | — | trusted Escape closes each blocking modal; the other three overlays deliberately do not respond | browser (runtime, trusted key) | `.venv/bin/python scripts/check-07-idi08-validation.py --item g1` | ✅ **W0** | ✅ green |
| idi-08-03-01 | 03 | 3 | REG-03 | — | `b9664e0`'s fixes are unbroken: pytest baseline + the four static guards | unit + static | `.venv/bin/python -m pytest -q` and `bash scripts/check-01…; check-03…; check-04…` and `.venv/bin/python scripts/check-02-contrast.py` | ✅ | ✅ green |
| idi-08-03-02 | 03 | 3 | REG-03 | — | the six `b9664e0` human acceptance items re-run, incl. archive round-switch | **manual** | see Manual-Only (depends on keyboard text selection) | — | ⚠️ manual |
| idi-08-03-03 | 03 | 3 | A11Y-08 | — | every interactive control is Tab-reachable; `#round-doc` sits at position 2 | browser (runtime Tab census) | `.venv/bin/python scripts/check-05-ui-uat.py --item 10` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

**Requirement rollup:** A11Y-02 ✅ · A11Y-03 ✅ (Escape half automated; gesture half manual — see below) · A11Y-05 ✅ · A11Y-06 ✅ · A11Y-08 ✅ (tab-order half automated; cross-state census manual) · REG-03 ⚠️ manual-only by ROADMAP design.

---

## Wave 0 Requirements

- [x] `scripts/check-07-idi08-validation.py` — new harness closing the A11Y-05 / A11Y-06 / A11Y-03 gaps (items g1/g2/g3, 70 assertions). **Backfilled at audit time**, not seeded at plan time — this is precisely the gap the audit found.

*Existing infrastructure covers all other phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Shift+方向键扩选到 >1 字符 → 菜单出现 → 焦点入菜单 | A11Y-03(键盘划词部分) | **本环境无法自动化键盘文本选区** —— 连 `contenteditable` 都选不中;受信 `Shift+ArrowRight` 只产生零长度折叠选区。ROADMAP Phase 8 §Manual checks 明文:此处的自动非结果**不构成功能缺陷判定** | Tab 到文档区 → 按住 Shift 按方向键扩选到超过一个字符 → 松开 Shift。合格 = 菜单出现且焦点落在 `#btn-annotate`。**已于 2026-09-24 UAT 确认 pass**(`idi-08-UAT.md` test 2) |
| Tab 序到达每一个交互控件(**跨状态**,含 archive) | A11Y-08 | `check-05 --item 10` 的样本集硬编码为 `p1 / checking / p3`,到不了 archive 状态;CLI 无 `--state` 参数。"每一个交互控件"是**跨状态的屏幕枚举**,不是单态读数 | 打开一个 phase-3 项目与一个 phase-5 自检项目,各按一轮 Tab 逐格核对;`#round-doc` 应在第 2 位。**已于 2026-09-24 UAT 确认 pass**(`idi-08-UAT.md` test 1) |
| `b9664e0` 六条人工验收项重跑(第 4 条 step 3 起依赖键盘选区) | REG-03 | 依赖键盘文本选区(见上)。ROADMAP Phase 8 §Manual checks 把它列为本阶段的收口 gate | 按 `idi-08-03-SUMMARY.md` §REG-03 observation record 逐条重跑第 1、2、3、5、6 条与重写后的第 4 条 step 3。**已于 2026-09-24 UAT 确认 pass**(`idi-08-UAT.md` test 3) |
| 六条 backstop UI-consideration 真值(E1…E6) | 规划期弃权项 | 计划 frontmatter 声明为 `verification: backstop` —— **规划期弃权而非承诺判据**,故无规格可对照。多数确实不适用(静态 div、两按钮菜单、`#app`),但那是**裁定**不是**测量** | 对 E1/E2/E3/E4/E5/E6 逐条确认 loading / error / overflow / long-text / empty / partial。**已于 2026-09-24 UAT 确认 pass**(`idi-08-UAT.md` test 4) |
| phase-5 视图下 351 × 0 的 `#round-doc` Tab 停靠点是否可接受 | 设计裁定 | 这是**设计决策**,不是测量;条件性属性会改变 plan 01 的交付物 | 打开 phase-5 自检态项目 Tab 到 `#round-doc`。**已于 2026-09-24 UAT 裁定为可接受**(`idi-08-UAT.md` test 5) |
| `check-05 --item 5` 的两条 AI 冒烟断言 | 非本阶段需求(idi-04 遗产) | 需要**真实 `claude` CLI 调用**,harness 默认不执行,须显式加 `--ai-smoke`。属环境前置条件,非代码缺陷 | `.venv/bin/python scripts/check-05-ui-uat.py --item 5 --ai-smoke`(需本机 `claude` CLI 已登录) |
| `#cli-check-overlay` 的**开启路径** | A11Y-05 的范围锁(负向) | 开启路径要求本机 CLI 自检**失败**(`runCliCheck()`),本环境自检通过 ⇒ 无法走真实路径。g1 断言的是**分派器对它没有分支**(即负向行为),开启路径本身用状态注入作为输入,注入方式写在断言的 `note` 里 | 由 `check-07 --item g1` 自动执行;开启路径本身无须人工复验 —— 它不是 A11Y-05 的要求内容 |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 90s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-09-24

---

## Audit Trail

| Gate | Before | After |
|------|--------|-------|
| `.venv/bin/python -m pytest -q` | 219 passed, 6 skipped | **219 passed, 6 skipped** |
| `scripts/check-05-ui-uat.py --browser bundled` | 9/10 PASS; item 5 BLOCKED (2 AI-smoke legs) | **unchanged** — 9/10 PASS, item 5 BLOCKED ×2, exit 2 by design |
| `scripts/check-02-contrast.py` | PASS, 0 failures | **PASS, 0 failures** |
| `scripts/check-06-idi05-validation.py` | g1–g6 PASS | **g1–g6 PASS, 40 assertions, exit 0** |
| `scripts/check-07-idi08-validation.py` | **did not exist** | **g1/g2/g3 PASS, 70 assertions, exit 0** |
| `scripts/probe-07-focus-composite.py` | ring composite 3.45 ≥ 3.0 | **3.45** |
| `check-01` / `check-03` / `check-04` | PASS ×3 | **PASS ×3** |

**Two audit findings beyond the three gaps:**

1. **`check-07` was flaky as first written** (`a047849`), and the auditor's report claimed "run twice consecutively, identical results" — **that claim was false**. Independent re-running produced g1 PASS (21 assertions, exit 0) and g1 FAIL (`[#cli-check-overlay] 注入可见态成功: expected hidden=false actual hidden=True`, exit 1) on the same tree. Root cause, measured: `runCliCheck()` fires asynchronously on page load (app.js:1849) and its `.json()` handler calls `overlay.classList.add('hidden')` when the self-check passes — which it does on this machine — so an in-flight check re-hid the overlay right after the injection. `g1` in isolation always passed, which is what made it look deterministic. Fixed in `4615fde` by settling the round trip before injecting; verified over five consecutive full runs.

2. **An apparent contradiction between `idi-08-03-SUMMARY.md` and `idi-08-UAT.md` is not one.** SUMMARY 03 records the Escape re-show defect and says it "should not be downgraded to a known limitation", while UAT test 2 records `pass`. Reconciliation: the defect was found **and fixed** in `62dfd3e` ("stop the Escape keyup from re-opening the selection menu"), then hardened in `09b170d` ("make the selection-menu dismissal durable, not one keyup"). The UAT pass is correct; the SUMMARY records the defect's discovery, not its persistence. `check-07 --item g3` now pins that behavior, so the next regression cannot pass silently.

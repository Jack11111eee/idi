---
phase: "idi-07"
slug: "interaction-states-and-focus"
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: "2026-09-23"
---

# Phase idi-07 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest(后端)+ Playwright 驱动的浏览器 harness(`scripts/check-05-ui-uat.py`)+ shell / python 守卫脚本(check-01 ~ check-04) |
| **Config file** | `pytest.ini` |
| **Quick run command** | `bash scripts/check-01-token-conformance.sh; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh; .venv/bin/python scripts/check-02-contrast.py \| tail -1` |
| **Full suite command** | `.venv/bin/python -m pytest -m "not slow" -q; bash scripts/check-01-token-conformance.sh; .venv/bin/python scripts/check-02-contrast.py; bash scripts/check-03-hidden-uniqueness.sh; bash scripts/check-04-important-count.sh; .venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8,9,10; .venv/bin/python scripts/probe-07-focus-composite.py` |
| **Estimated runtime** | ~10 秒(pytest)+ ~2 分钟(check-05 全项,需拉起 8765 上的浏览器) |

**必须使用项目 venv(`.venv/bin/python`)。** 环境 `python3` 是 miniconda,会让无关套件假失败。

**check-05 的服务生命周期:** 先探测 `127.0.0.1:8765`;已在服务则复用,结束时不动它;未服务才自己 `Popen` uvicorn 并在结束时只关掉自己起的那个进程。

---

## Sampling Rate

- **After every task commit:** Run `{Quick run command}`(四条静态守卫,秒级)
- **After every plan wave:** Run `{Full suite command}`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** ~120 秒(受 check-05 浏览器会话主导)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| idi-07-01-01 | 01 | 1 | A11Y-01 | T-idi-07-01 / -02 / -03 | 环色对三处表面的对比度 >= 3:1;焦点规则体不含 `border` / `padding`;环色不被「顺手修正」 | unit + automated_ui | `.venv/bin/python scripts/check-05-ui-uat.py --item 10` + `bash scripts/check-01-token-conformance.sh` | ✅ | ✅ green |
| idi-07-01-02 | 01 | 1 | A11Y-01 | T-idi-07-01 / -05 | 三条环色 PAIR 全部达标;归档半场的反事实探针以一次性注入交付 | unit + integration | `.venv/bin/python scripts/check-02-contrast.py \| grep -c 'PASS  [0-9.]*  --color-focus'`(== 3)+ `.venv/bin/python scripts/probe-07-focus-composite.py` | ✅ | ✅ green |
| idi-07-01-03 | 01 | 1 | A11Y-01 | T-idi-07-04 | 普查判定集非空且未覆盖数为 0;空集走 `blocked` 而非静默 PASS | automated_ui | `.venv/bin/python scripts/check-05-ui-uat.py --item 10` + `--item smoke,1,2,3,4,6,7,8,9` | ✅ | ✅ green |
| idi-07-02-01 | 02 | 2 | INTERACT-01 | T-idi-07-07 / -08 | 禁用按钮 hover 零反馈;朴素 active 与 L587 让位成对,缺一即按下态不可达 | automated_ui | `.venv/bin/python scripts/check-05-ui-uat.py --item 10` | ✅ | ✅ green |
| idi-07-02-02 | 02 | 2 | INTERACT-01 | T-idi-07-06 / -09 | 填充按钮 hover 时 `background-color` 不变、`box-shadow` 出 inset 叠层;围栏外裸 `rgba()` 计数为 0 | automated_ui + static | `.venv/bin/python scripts/check-05-ui-uat.py --item 10` + `awk` 围栏外取样断言 | ✅ | ✅ green |
| idi-07-02-03 | 02 | 2 | INTERACT-01 | T-idi-07-10 | input / select hover 边框加深到 `--color-border-hover`;SC5 / SC5′ 读值前先断言元素存在且可见 | unit + automated_ui | `.venv/bin/python scripts/check-02-contrast.py \| grep -c -- '--color-border-hover'` + `.venv/bin/python scripts/check-05-ui-uat.py --item 10` | ✅ | ✅ green |
| idi-07-03-01 | 03 | 3 | INTERACT-02 | T-idi-07-12 / -13 / -14 / -16 | 减弱动效块零 `!important`;`EXPECTED_MEDIA_QUERIES` 与 `@media` 实际计数一致;`.event-list` 例外未被动;焦点环不进过渡列表 | static + automated_ui | `bash scripts/check-04-important-count.sh` + `.venv/bin/python scripts/check-05-ui-uat.py --item 8` + `grep -c '^@media (prefers-reduced-motion' frontend/style.css` | ✅ | ✅ green |
| idi-07-03-02 | 03 | 3 | INTERACT-02 | T-idi-07-15 / -16 | 四条契约计数静态守卫成立;过渡与减弱动效运行时读数正确 | automated_ui + static | `.venv/bin/python scripts/check-05-ui-uat.py --item 10` + `grep -c 'def _idi07_focus_contract_guards' scripts/check-05-ui-uat.py` | ✅ | ✅ green |
| idi-07-03-03 | 03 | 3 | INTERACT-02 | T-idi-07-17 | 整阶段收口:全门复跑、D-19 指纹以 HEAD 重算并逐份处置 | integration | `bash scripts/check-01…04` + `.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8,9,10` + `.venv/bin/python scripts/probe-07-focus-composite.py` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] 既有基础设施覆盖本阶段全部需求 —— 本阶段零新增测试框架、零新增运行时依赖、零构建步骤(硬规则 6)

*Existing infrastructure covers all phase requirements.* 复用:`pytest.ini` + `scripts/check-01…05` + `scripts/probe-07-focus-composite.py`。

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| `#btn-authorize` 的禁用态仍「一眼看出不可点」,未被 hover / 按下点亮(D-17 的 5″) | A11Y-01(G3 前提条件) | 这是关于**感知**的主张,不是关于数值的主张。机器半场(SC5′)覆盖的是**另一条规则** `.verdict-buttons button:disabled`(opacity 0.5);`#btn-authorize:disabled`(opacity 0.55)今天没有任何机器断言读过它的 opacity,只被 L741 那条 gate 间接保护。D-17 明文:不得把它删掉换成机器代理量 | 进入阶段 3(p3 样本)后把鼠标移到 `#btn-authorize` 上并停留 / 按下,观察它是否仍一眼看出不可点。合格 = 禁用态一眼可辨,且悬停 / 按下时零视觉反馈;0.55 淡化不被削弱 |
| `check-05` item 5 的两条 AI 冒烟断言(「处理本轮批注」/「发送」) | 非本阶段需求(idi-04 遗产) | 需要**真实 claude CLI 调用**,harness 默认不执行,须显式加 `--ai-smoke`。属环境前置条件,非代码缺陷 | `.venv/bin/python scripts/check-05-ui-uat.py --item 5 --ai-smoke`(需本机 claude CLI 已登录) |

**人工项 5″ 的处置:** 已于 2026-09-23 由用户在 UAT 会话中确认 **pass**(`idi-07-UAT.md`,1/1 passed,0 issues)。

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references(无 MISSING —— 基础设施先于本阶段存在)
- [x] No watch-mode flags
- [x] Feedback latency < 120s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-09-23

---

## Validation Audit 2026-09-23

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

**审计方式:** State B(无既有 VALIDATION.md,由 PLAN / SUMMARY 重建)。逐条在 HEAD 上重跑全部自动化面,未采信 SUMMARY 的自述:

| 命令 | 结果 |
|------|------|
| `.venv/bin/python -m pytest -m "not slow" -q` | `219 passed, 6 deselected`(与既有基线一致) |
| `bash scripts/check-01-token-conformance.sh` | `PASS` |
| `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`;`--color-focus` 配对 3 条 |
| `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` |
| `bash scripts/check-04-important-count.sh` | `PASS` |
| `.venv/bin/python scripts/check-05-ui-uat.py --item 10` | `PASS (41 条断言, 0 FAIL, 0 BLOCKED)`,exit 0 |
| `.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,2,3,4,6,7,8,9` | 9/9 PASS,0 FAIL / 0 BLOCKED |
| `.venv/bin/python scripts/probe-07-focus-composite.py` | exit 0,`ratio=3.45 (>= 3.0)` |
| `awk` 围栏外取样:`grep -c 'rgba('` | `0` |
| `awk` 围栏外取样:`grep -c 'box-shadow: inset 0 0 0 999px'` | `2` |
| `grep -c '^@media (prefers-reduced-motion' frontend/style.css` | `1` |
| `grep -c 'def _idi07_focus_contract_guards' scripts/check-05-ui-uat.py` | `1` |
| `grep -v '^#' frontend/style.css \| grep -c ':focus-visible'` | `9` |
| `git status --porcelain -- scripts/ui-states/` | 空(样本只读) |

**唯一非绿项:** `--item 5` 的两条 AI 冒烟断言为 `BLOCKED`(需 `--ai-smoke`,真实 AI 调用)。经 `git log -S` 溯源,该 gate 由 `6f52602`(idi-04 的 harness 首版)引入,**早于本阶段**,非 idi-07 引入的回归,亦非本阶段的覆盖缺口 —— 已登记于上表 Manual-Only。

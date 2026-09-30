---
phase: idi-12-g1-band
verified: 2026-09-29T12:52:00Z
status: passed
score: 15/15 must-haves verified
covered_files:

  - .planning/REQUIREMENTS.md
  - .planning/ROADMAP.md
  - .planning/phases/idi-12-g1-band/12-CONTEXT.md
  - .planning/phases/idi-12-g1-band/idi-12-01-PLAN.md
  - .planning/phases/idi-12-g1-band/idi-12-01-SUMMARY.md
  - .planning/phases/idi-12-g1-band/idi-12-02-PLAN.md
  - .planning/phases/idi-12-g1-band/idi-12-02-SUMMARY.md
  - .planning/phases/idi-12-g1-band/idi-12-03-PLAN.md
  - .planning/phases/idi-12-g1-band/idi-12-03-SUMMARY.md
  - .planning/phases/idi-12-g1-band/idi-12-REVIEW.md
  - frontend/style.css
  - scripts/check-09-idi09-validation.py
  - scripts/ui-states/checking/docs/DESIGN-check-2.md

covered_digest: "v1:sha256:d2377864406b200ade063f1ed6adea81af18e09eee0345f8e50039811a67af47"
content_reverification:
  round: 1
  kind: "bookkeeping"
  trigger: "Phase 12 的**收口动词**改写了 .planning/ROADMAP.md(Phase 12 行 `2/3 | In Progress` → `3/3 | Complete | 2026-09-29`),该文件在 covered_files 内 ⇒ digest 必然作废。这是**记账型 stale**(非缺陷):收口序列合法改写被覆盖文件,信号按设计工作。按 Phase 11 先例处置 —— 在收口序列的**最后一个动词之后**复算,以 HEAD 内容重新验证,不是刷新指纹"
  previous_digest: "v1:sha256:7590cdfe099573da8f6235ec20850bea0cfe6406ff90afef92d46b097df8a001"
  current_digest: "v1:sha256:d2377864406b200ade063f1ed6adea81af18e09eee0345f8e50039811a67af47"
  verified_head: "23a8efc"
  changed_files_total: 1
  changed_covered_files:
    - path: ".planning/ROADMAP.md"
      change: "记账(phase.complete 12):Phase 12 行 `2/3 | In Progress` → `3/3 | Complete | 2026-09-29`;Phase 12 段的三条计划复选框置 [x]。`## Milestones` 的 v1.16 行仍为 🚧(里程碑审计走 /gsd-audit-milestone,不在本阶段内 —— D-12-12)。Goal / Success Criteria / Deliverables 零改动"
  digest_delta_attribution: "以 FINGERPRINT_VERSION=1 算法独立复算两遍:①当前工作树(13 个 covered 文件)→ `d2377864…`(与 `gsd-tools query verification.fingerprint` 输出逐字相同);②**仅**把 `.planning/ROADMAP.md` 换回 `21d4267` 内容、其余 12 份不动 → `7590cdfe…`,**精确复现记录值** ⇒ 整个 digest 位移 100% 由这一份记账文件造成,无任何隐藏的实质变更。**本轮未删除、未放宽、未改写任何断言或阈值**"
  truth_reestablishment: "15 条 must-have 真值**逐条仍成立** —— 本轮唯一变动是记账(Phase 12 状态翻转),它不触及任何一条判据的载体:`frontend/style.css`(band 的两条计算底色)、`scripts/check-09-idi09-validation.py`(`c6` 7 条断言 + `--g1-snapshot` 3 条)、fixture 表、5 张截图与局部特写、13 份门日志,全部逐字节未动。门禁证据在 `gate-logs/idi-12-03/` 且 `^FAIL` 全为 0"
  note: "**人类验收已由用户完成**:`idi-12-UAT.md` 两项(局部特写的 band 观感、5 张整窗图的「分块割裂感已消除」)均 `result: pass`;`status` 由 `human_needed` 规范化为 `passed` 是本轮之前的合法动作(见 `phase uat-passed` 谓词 → `passed: true`)"
behavior_unverified: 0
overrides_applied: 0
gaps: []
deferred: []
human_verification:

  - test: "打开 .planning/phases/idi-12-g1-band/screenshots/latest-check/latest-check.png,确认表头行(`编号 | 级别 | 位置 | 问题 | 建议修法`)在其宿主内读作一条**独立的 band**"
    expected: "表头行呈现为一档浅灰底,与周围白色报告面可辨;不再与数据行读感相同"
    why_human: "「读作一条独立 band」是屏幕级观感判断。机械判据只证明两者的计算底色不同(rgb(255,255,255) vs rgb(249,249,249)),证明不了 1.053 的色差在真实显示条件下**看得出**"
  - test: "打开 screenshots/ 下 5 张 1440×900 整窗图(p1 / p12 / p3 / checking / archive),确认「分块割裂感已消除」"
    expected: "整站读作一张连续白面 + 发丝分隔线,无卡片边界或灰缝残留"
    why_human: "VIS-01 的主张本身是屏幕级人眼判断,自动化只能覆盖机械半边(文件名齐全、各 1440×900、字节非零)"
---

# Phase 12: G1 表头 band 与里程碑收口 Verification Report

**Phase Goal:** 修掉 v1.15 里程碑审计登记的 **G1** —— `#latest-check` 自身声明 `background: var(--color-surface)`(gray-2)**且自身是 `.markdown-body` 宿主**,而 `th` 用同一令牌绘制 ⇒ 自检报告里的表头是**灰底压灰底**、band 消失。目标是让表头在 `#latest-check` 内**读作一条独立的 band**。**同时收口**:在全部 `style.css` 改动落定后复跑五条浏览器门 + 四个静态门 + pytest 基线,处置连带作废的 `passed` 报告,并产出 5 张 1440×900 整窗截图作为人眼取证。
**Verified:** 2026-09-29T12:52:00Z
**Status:** human_needed
**Re-verification:** No — initial verification (no prior `idi-12-VERIFICATION.md` existed)

**Verified at HEAD:** `707f023` (`docs(idi-12): correct the surface-page ledger's layout descriptor (left/right columns)`) — `frontend/style.css` blob `34f47ed862aee52ed2ad2598f6d3ecf5abdc3042`.

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | `#latest-check` 的计算底色 **!=** `#latest-check th` 的计算底色(同一 `checking` 样本的运行时 `getComputedStyle`)⇒ 表头读作独立 band (G1-01 / SC1) | ✓ VERIFIED | 门日志 `check-09-idi09-validation.log`:host `rgb(255, 255, 255)` vs th `rgb(249, 249, 249)`。**本人独立复跑** `.venv/bin/python scripts/check-09-idi09-validation.py --item c6` → `item c6: PASS (7 条断言,0 FAIL,0 BLOCKED)`。两值来自不同来源(宿主规则 / `th` 规则),非自指 |
| 2 | 两侧钉死(D-12-7):宿主底色 == `--color-surface-page` 运行时解析值 **且** == 写死字面量 `rgb(255,255,255)` | ✓ VERIFIED | 源码 `scripts/check-09-idi09-validation.py:826-837` 三条断言齐备;运行读数三者一致。**M2 变异**下「两者不同」半条保持 PASS 而这两条 FAIL ⇒ 两侧非冗余(见 Truth 11) |
| 3 | `.markdown-body th` 的绘制面一字未动(仍 gray-2)⇒ 路线 (b) 未被采用 | ✓ VERIFIED | `frontend/style.css:1250` `.markdown-body th { background: var(--color-surface); }` 在 `f4603ef^..HEAD` 区间**零 diff**;`check-10` 的 `t1` 五对(含 `#latest-check`)全 PASS(日志 `:11,:23,:35,:47,:59`) |
| 4 | `#latest-check` 的 `max-height: 30vh` / `border` / `border-radius` 三条声明逐字节未动(D-12-3) | ✓ VERIFIED | 整阶段 `style.css` diff 只有两处 hunk:围栏注释段 + `background` 一行。规则体现读为 `max-height: 30vh; overflow-y: auto; border: 1px solid var(--color-border-subtle); border-radius: var(--radius-sm);` |
| 5 | `--color-surface` 的值未改、令牌未删(D-12-1 ③) | ✓ VERIFIED | 该令牌仍有 10 处消费者(`style.css:1005/1020/1064/1120/1250/1421/1454/1559/1655` + `:741` 注释);围栏声明数 119(去重 119)不变 |
| 6 | `checking` fixture 忠于后端文法:`## 问题分级` + 逐字表头 + 至少一行 P0/P1 | ✓ VERIFIED | `scripts/ui-states/checking/docs/DESIGN-check-2.md` 读盘确认;`.venv/bin/python` 直调 `backend.grammar` → `parse_problem_grades` **2 行**(P1/P2)、`is_pure_p2 False`、`is_pass_conclusion False`。diff 为纯插入(+7 行),其余逐字节保留 |
| 7 | 该样本 UI 模式仍是 `running`(运行时正面断言) | ✓ VERIFIED | `c6` 两条 fixture 不变量 PASS:`#btn-continue-check` classList `[]`(不含 `hidden`)、`#verdict-cards` 内 `.verdict-card` == 0。本人复跑读数一致 |
| 8 | 围栏 `:129-133` 承重注释就地改写;改写后围栏**声明数不变**(119) | ✓ VERIFIED | `style.css:130-133` 读盘:旧句「controls and `#latest-check` still read as recessed」已就地更正并记录旧句为何为假;注释内无「令牌名紧接冒号」形态。`.venv/bin/python` 正则复算 → `119 / unique 119` |
| 9 | `check-02` PASS:零新增对比度条目、零阈值放宽(SC2) | ✓ VERIFIED | `check-02-contrast.log` 54 PASS / `ORDER 0.363  --color-text-muted before --color-text on --color-surface` / `PASS: 0 failures`;`grep -c '/\* PAIR '` == **53**;`scripts/check-02-contrast.py` 本阶段零改动。**本人于 HEAD 复跑 → 逐字相同** |
| 10 | 新判据落在新项 `c6`,`c1..c5` 逐字保留(D-12-6) | ✓ VERIFIED | `ITEMS = {"c1".."c6"}`;日志六项计数 `c1 59 / c2 19 / c3 6 / c4 39 / c5 5 / c6 7` —— `c1..c5` 与 Phase 11 收口读数逐项相同;`check-09` 的 diff 中每条 `-` 行仅为 `ITEMS` 字面量与 `summary` 构造,零断言删除/降级 |
| 11 | `c6` 经**两条真实变异**证明会失败(M1 / M2),且还原后逐字节相同 | ✓ VERIFIED | **本人独立复现**:M1(宿主改回 `var(--color-surface)`)→ `item c6: FAIL (7 条断言,3 FAIL,0 BLOCKED)` exit=1,逐字复现 SUMMARY 记录的 3 条 FAIL 文本;M2(改指 `--color-surface-sunken`)→ `FAIL (7 条,2 FAIL)`,**「两者不同」半条保持 PASS** 而「宿主 == 白」两条 FAIL。两次均 `git checkout -- frontend/style.css` 还原,`git diff --exit-code` rc=0,`git hash-object` == `ecd5fb0d…`(变异前值)。全程未用 `git stash` |
| 12 | 边界:`frontend/app.js` / `index.html` / `backend/**` / `frontend/vendor/**` 逐字节未改;未顺手做任何未裁定项 | ✓ VERIFIED | `git diff --stat f4603ef^..HEAD -- frontend/app.js frontend/index.html backend/ frontend/vendor/` **为空**;`ls frontend/vendor/` 仅 `marked.min.js`;整阶段只动 3 个源文件。未裁定项核实**未动**:`check-10-idi10-validation.py:328` 的过期注释原样在盘、`position: sticky` 全文仅 `:943`(`#doc-panel-header`)一处、无 G2 / `999.2` / 暗色模式 / Nyquist / 图标空状态改动 |
| 13 | 五条浏览器门 + 两探针 + 四静态门 + pytest 基线复跑零新增失败(SC3 / REG-04) | ✓ VERIFIED | 13 份日志 `^FAIL` 计数**全为 0**(**行首锚定**,非子串 —— 实测 `check-05` 日志含 11 处 FAIL **子串**,全部落在 PASS 行的标签里,子串判据在本项目恒非空)。rc:`check-05` = 2,其余 12 份 = 0。**本人于 HEAD 复跑四静态门**:`check-01/03/04` PASS rc=0,`check-02` `PASS: 0 failures`;`.venv/bin/python -m pytest backend/tests -q` → **219 passed, 6 skipped** |
| 14 | `check-05` 的 `exit=2` 成因**仍只是** item 5 两条 `--ai-smoke` 腿按设计 BLOCKED;`check-09` 的 `c1..c5` 与 Phase 11 契约一致 | ✓ VERIFIED | 全日志 `^BLOCKED` 恰 **2** 条(`:215` `:216`),逐字为两条 `--ai-smoke` 腿;`item 5: BLOCKED (9 条断言,0 FAIL,2 BLOCKED)`,其余九项全 PASS。`check-09 --item c1..c6` exit=0 |
| 15 | 连带指纹逐份处置 + 5 张 1440×900 截图落盘且「恰含 5 个 PNG」断言未放宽(SC4 / SC5 / VIS-01) | ✓ VERIFIED | 指纹:本人独立按 `covered_files` **逐行匹配**扫全部 17 份报告 → **命中 12 份**(11 归档 + 1 在盘),与 SUMMARY 表格逐行一致;fixture 零命中。截图:顶层恰 5 个 PNG,各 1440×900 且字节非零;局部特写 736×270 落在**独立子目录** `screenshots/latest-check/`;`grep -cF 'shot 输出目录恰含 5 个 PNG'` == **1**(逐字保留) |

**Score:** 15/15 truths verified (0 present-behavior-unverified)

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `frontend/style.css` | `#latest-check` 宿主绘制面就地改归统一面白 + 围栏注释就地改写 | ✓ VERIFIED | `:1664` `background: var(--color-surface-page);`(blob `b6c4928 → 34f47ed`)。单条声明换值 + 注释段改写,**无追加覆盖** |
| `scripts/check-09-idi09-validation.py` | 新项 `c6` + 专用参数 `--g1-snapshot DIR` + `g1_snapshot()` | ✓ VERIFIED | `ITEMS` 六键;`add_argument` 恰 4 个;`g1_snapshot()` 3 条断言;`summary` 追加 `"g1-snapshot"`;模块 docstring 映射表补 `c6`/`g1-snapshot` 两行 |
| `scripts/ui-states/checking/docs/DESIGN-check-2.md` | 后端文法强制的「问题分级」表 | ✓ VERIFIED | `## 问题分级` + 逐字表头 + P1/P2 两行;纯插入 |
| `screenshots/{p1,p12,p3,checking,archive}.png` | 5 张 1440×900 整窗图 | ✓ VERIFIED | 逐张读盘:1440×900,86,609 / 121,583 / 124,205 / 75,024 / 122,876 字节 |
| `screenshots/latest-check/latest-check.png` | G1 局部特写(独立落点) | ✓ VERIFIED | 736×270,25,737 字节,PNG 签名正确 |
| `gate-logs/idi-12-03/*.log` | 13 份原始门禁输出 + 退出码 | ✓ VERIFIED | 13 份在盘,每份末尾恰一行 `rc=` |
| `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-VERIFICATION.md` | 以 HEAD 内容重新验证(第三轮) | ✓ VERIFIED | `content_reverification` round 3 段在盘(触发原因 + previous/current digest + 18 笔提交 + 4 个 `changed_covered_files` 逐条归因 + 重跑读数);`covered_files` 16 条零缺失;`gaps: []`。**见 W-02** |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `style.css` 的 `#latest-check { background }` | `--color-surface-page`(`:155`) | 令牌消费 | ✓ WIRED | `grep -cF 'var(--color-surface-page)'` == 5(基线 4 + 本阶段 1);运行时解析值 `rgb(255,255,255)` 与宿主计算底色相等(Truth 2) |
| `check-09` 的 `c6` | 真实浏览器 computed `background-color` | `read_style(page, "#latest-check th", "background-color")` | ✓ WIRED | `:804`;实测非 None 且为 `rgb(249, 249, 249)` —— band 是**画出来**的,非文本匹配 |
| fixture 的 `## 问题分级` 标题 | `backend/grammar._extract_table` → `parse_problem_grades` → `session.mode` | 二级标题定位 + 表头丢弃 + P1 行防 `is_pure_p2` | ✓ WIRED | 直调后端:2 行 / `pure_p2 False` / `pass_conclusion False` ⇒ mode `running` |
| `c6` 的 fixture 模式不变量 | `frontend/app.js` 的四路 `mode` 分支 | `read_classlist("#btn-continue-check")` 不含 `hidden` + `#verdict-cards` 计数 0 | ✓ WIRED | 运行时读数 `[]` / `0`,与 `c6` 的 mode 前提一致 |
| `--g1-snapshot DIR` | `page.locator("#latest-check").screenshot(...)` | 照 `check-10:653` 元素截图先例 | ✓ WIRED | 实测写出 736×270;断言 3 把尺寸钉到宿主矩形(`736x270 vs host=736x270`) |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `c6` 的 `host_bg` / `th_bg` | 浏览器 `getComputedStyle` | 真实 Chromium(153.0.8010.12)渲染 `checking` fixture 后的计算值 | Yes | ✓ FLOWING |
| `c6` 的 `page_token` | `resolve_color(page, "--color-surface-page")` | `documentElement` 上的令牌声明(经 probe div 解析) | Yes | ✓ FLOWING |
| fixture 表头 | `backend.grammar.parse_problem_grades` | fixture 文件正文 → 后端解析器 | Yes(2 行) | ✓ FLOWING |
| `g1-snapshot` 的 `host_rect` / `th_rect` | Playwright `bounding_box()` | 真实布局几何(非滚动入视) | Yes | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| `c6` 在正确实现上通过 | `.venv/bin/python scripts/check-09-idi09-validation.py --item c6` | `item c6: PASS (7 条断言,0 FAIL,0 BLOCKED)` | ✓ PASS |
| `c6` 在 M1(还原为内陷面)下失败 | 注入 `background: var(--color-surface)` → 同上 | `FAIL (7 条,3 FAIL)`,exit=1 | ✓ PASS(守卫可失败) |
| `c6` 在 M2(gray-3)下失败而「不同」半条仍绿 | 注入 `var(--color-surface-sunken)` → 同上 | `FAIL (7 条,2 FAIL)`,「两者不同」PASS | ✓ PASS(两侧非冗余) |
| fixture 忠于后端文法 | `.venv/bin/python -c "from backend import grammar; ..."` | rows 2 / pure_p2 False / pass_conclusion False | ✓ PASS |
| 四静态门在最终树 | `bash scripts/check-0{1,3,4}-*.sh` + `check-02-contrast.py` | 全 PASS rc=0 / `PASS: 0 failures` | ✓ PASS |
| pytest 基线 | `.venv/bin/python -m pytest backend/tests -q --tb=short` | `219 passed, 6 skipped, 1 warning` | ✓ PASS |

### Probe Execution

| Probe | Command | Result | Status |
|-------|---------|--------|--------|
| `scripts/probe-05-resolve-color.py` | 日志 `probe-05-resolve-color.log`(rc=0) | `PROBE control-verdict=PASS`;其 `BLOCKED [mutated] … post-fix` 是**该探针自己的对照支**(同表两跑),非门失败 | ✓ PASS |
| `scripts/probe-07-focus-composite.py` | 日志 `probe-07-focus-composite.log`(rc=0) | 环 `rgb(31, 99, 189)` 2px;合成地面白、比值 `3.54 (>= 3.0)` | ✓ PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| **G1-01** | idi-12-01, idi-12-02 | `#latest-check` 内表头读作独立 band;运行时读数或人眼截图取证 | ✓ SATISFIED | Truths 1-11;`check-09 c6` + `g1-snapshot` 全 PASS;局部特写落盘 |
| **REG-04** | idi-12-03 | 五浏览器门 + 四静态门 + pytest 复跑零新增失败;连带作废报告逐份处置 | ✓ SATISFIED | Truths 13-15;13 份日志 `^FAIL` 全 0;12 份连带报告逐份处置。**W-02 记录 re-staling** |
| **VIS-01** | idi-12-02 | 5 张 1440×900 整窗截图落盘 | ✓ SATISFIED(机械半边) | 5 张在盘、各 1440×900;观感半边见 Human Verification |

**Orphaned requirements:** none — `REQUIREMENTS.md` 将 Phase 12 映射的恰为上述三条,与三份 PLAN 的 `requirements:` 字段完全一致(12/12 决策 honored,见下)。

**Decision Coverage (gate):** `check.decision-coverage-verify` → `{skipped: false, blocking: false, total: 12, honored: 12, not_honored: []}` — "All trackable CONTEXT.md decisions are honored by shipped artifacts."

### Test Quality Audit

| Test File | Linked Req | Active | Skipped | Circular | Assertion Level | Verdict |
|-----------|-----------|--------|---------|----------|-----------------|---------|
| `scripts/check-09-idi09-validation.py` (`c6` / `g1-snapshot`) | G1-01, VIS-01 | yes | 0 | no | Value + Behavioral | PASS |
| `backend/tests/**`(pytest 基线) | REG-04 | 219 | 6 | no | Value | PASS |

**Disabled tests on requirements:** 0 → no BLOCKER. The 6 skips are pre-existing `IDI_E2E`-gated E2E tests (`test_e2e_g3.py:174,253`, `test_e2e_rounds.py:179`), unrelated to this phase's requirements and part of the declared 219/6 baseline.
**Circular patterns detected:** 0 → no BLOCKER. `c6` reads the system under test but asserts against **externally written literals** (`rgb(255,255,255)` / `rgb(249,249,249)`) plus an independently-resolved token, not against values generated by the same run.
**Insufficient assertions:** 0.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| — | — | `TBD` / `FIXME` / `XXX` in any phase-modified file | — | **None found** — 三个改动源文件零债务标记 |
| — | — | 空实现 / 占位文案 / 硬编码空值 | — | **None found** |

### Warnings (registered, non-blocking)

**W-01 — 静态门日志早于最后一次 `style.css` 改动(注释级)。** `check-01` / `check-02` / `check-03` / `check-04` / `pytest` 五份日志最后提交于 `40db421` / `cecfe9c`;其后 `707f023` 又改了一次 `style.css`(纯注释文本:更正 `--color-surface-page` 消费者台账的布局描述,零声明改动)。**本人已在最终 HEAD 上复跑** `check-01/02/03/04` → 全 PASS(`check-02` `PASS: 0 failures`、围栏声明 119/119、PAIR 53),且浏览器门读的是渲染结果而非注释文本 ⇒ 实质结论成立。仅证据新鲜度上存在一处注释级错位,非门失败。

**W-02 — 在盘报告 `idi-11-VERIFICATION.md` 在最终 HEAD 上再次变 stale。** 该报告的 `covered_files` 同时含 `frontend/style.css` 与 `scripts/check-09-idi09-validation.py`。第三轮重新验证提交于 `3a0b7f2`(当时 HEAD = `40db421`),此后**同阶段的评审整改提交** `cecfe9c` 又改动了这两个文件(check-09 的 `g1-snapshot` 断言 3 由「宽高非零」加强为「== 宿主矩形」;style.css 围栏注释),`707f023` 再改一次注释。**本人复算**:记录值 `c5d1e338…` vs 最终 HEAD 值 `64e0be48…` ⇒ `verification.status` 报 `stale`。
**为何不判为 BLOCKER:** SC4 的**操作性要求**是「以 HEAD 内容重新验证而非刷新指纹」—— 该行为已可证地执行(报告内含第三轮 `content_reverification` 段:4 个 `changed_covered_files` 逐条归因、12 条真值在 HEAD 上重立、M1/M3 变异在已变载体上重跑);stale 是**信号按设计工作**的结果,不是被掩盖的假陈述。且后续两次改动均不使该报告的任何一条真值失效(注释文本 + 一条本阶段新增的断言)。`idi-12-03-SUMMARY.md` 的 D4 已登记「收口序列会再次合法改写 `covered_digest` 覆盖面 ⇒ 再次 stale,按 Phase 11 先例由记账型重新验证轮次处置」。**建议:** 在阶段收口序列的最后一步之后补一轮 re-verification(或按 D4 登记为已知限制),勿在收口前用 `verification.fingerprint` 直接覆盖 —— 那正是 SC4 禁止的「刷新指纹」。

### Human Verification Required

#### 1. G1 band 的观感确认(局部特写)

**Test:** 打开 `/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.planning/phases/idi-12-g1-band/screenshots/latest-check/latest-check.png`。
**Expected:** `核查报告 2` 下方的表头行(`编号 | 级别 | 位置 | 问题 | 建议修法`)呈现为一档**浅灰底**,与周围白色报告面可辨;表头行不再与数据行读感相同。
**Why human:** 机械判据只证明两者计算底色不同(`rgb(255,255,255)` vs `rgb(249,249,249)`);band 强度被显式接受为 1.053,「看得出」这一条只能人眼判。**验证者本人的读图观察:** 该 PNG 中表头行确呈一档浅灰横带、数据行落白底,band 可辨 —— 但这不替代用户确认。

#### 2. VIS-01 整窗观感确认(5 张)

**Test:** 逐张打开 `screenshots/{p1,p12,p3,checking,archive}.png`。
**Expected:** 整站读作一张连续白面 + 发丝分隔线,无卡片边界、无灰缝残留 —— 「分块割裂感已消除」。
**Why human:** VIS-01 是屏幕级主张,自动化只覆盖机械半边。

### Gaps Summary

**无 BLOCKER 级缺口。** 15 条真值全部 VERIFIED,含最关键的 G1-01 本体(两条计算底色不同)、D-12-7 的两侧钉死、以及**本人独立复现**的两条变异证明(M1 → 3 FAIL;M2 → 2 FAIL 且「两者不同」半条保持 PASS)。REG-04 的 13 份门禁证据在盘且 `^FAIL` 全为 0;VIS-01 的 5 张整窗图与 1 张局部特写落盘,「恰含 5 个 PNG」断言逐字保留。范围栅栏成立(3 个源文件;`app.js` / `index.html` / `backend/` / `vendor/` 逐字节未改;未裁定项零触碰)。

状态为 `human_needed` 而非 `passed`,唯一原因是 VIS-01 与 SC1 明文要求**人眼取证** —— 屏幕级观感判断无法由机器替代。两条 WARNING 均已登记且经本人复核不构成门失败。

---

_Verified: 2026-09-29T12:52:00Z_
_Verifier: [CL] (gsd-verifier)_

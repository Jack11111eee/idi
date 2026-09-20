---
phase: idi-04.1-radix
verified: 2026-09-20T03:24:39Z
status: passed
score: 37/38 must-haves verified
covered_files:

  - .planning/REQUIREMENTS.md
  - .planning/phases/idi-04.1-radix/idi-04.1-01-PLAN.md
  - .planning/phases/idi-04.1-radix/idi-04.1-01-SUMMARY.md
  - .planning/phases/idi-04.1-radix/idi-04.1-02-PLAN.md
  - .planning/phases/idi-04.1-radix/idi-04.1-02-SUMMARY.md
  - .planning/phases/idi-04.1-radix/idi-04.1-03-PLAN.md
  - .planning/phases/idi-04.1-radix/idi-04.1-03-SUMMARY.md
  - .planning/phases/idi-04.1-radix/idi-04.1-04-PLAN.md
  - .planning/phases/idi-04.1-radix/idi-04.1-04-SUMMARY.md
  - frontend/style.css
  - scripts/check-01-token-conformance.sh
  - scripts/check-05-ui-uat.py
  - scripts/probe-05-resolve-color.py

covered_digest: "v1:sha256:a8b5147e616dd7c798906f69bb20dfa8c6319bbe372a05b455c482997719fe41"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: 33/36
  gaps_closed:
    - "P3.1 / CR-01 — `scripts/check-05-ui-uat.py` 的颜色断言在令牌改名/删除下恒真(假 PASS)。`resolve_color` 现在区分「令牌已声明 / 未声明」,`ok()` 把 `None` 期望值记 BLOCKED;变异证明钉死「修复前 PASS / 修复后 BLOCKED」"
  gaps_remaining: []
  regressions: []
human_verification:

  - test: "UI-SPEC `## UI Considerations` 的 28 条 backstop 陈述(plan 01 must_haves 中 `verification: backstop` 的 28 条)——E1 七芯片不换行/200% 缩放、E2 六按钮行换行与最长闸门标签不裁切、E3 窄面板实心标签不裁切、E4 最长 streaming 串不裁切、E5 文档面板滚动与 #f9f9f9/#fcfcfc 可区分、E6 折行 .hint 与长引用不裁切、E7 冻结轮滚动与琥珀竖线钉边、E8 长致命错误折行、E9 不可断消息撑高与 --shadow-composer 边缘、E10 模态适配视口、E11 大量长批注滚动列表、E12 大量检查项滚动面板、E13 长归档文档不裁切、E14 选区菜单重定位与长菜单项不截断、E15 最长路由标签不截断、E16 跨行 mark 连续段与长 mark 文字可读"
    expected: "每条陈述在其描述的极端输入下成立;其中 7 条只含 CHECK-02 比值的一半已由 check-02 实测证据覆盖(E1 芯片 4.61–16.29 / E2 闸门标签 11.00 / E4 徽标 4.53 / E6 弱化灰 5.19–5.82 / E7 冻结标记 10.80 / E13 归档 0.75 压暗 6.97 / E10 .tier-desc 满不透明度 4.77),其余裁切/滚动/换行/缩放行为无自动化证据"
    why_human: "这些是渲染几何与极端输入下的视觉行为(裁切、换行、滚动归属、200% 缩放、菜单重定位),grep 与 computed-style 读数都看不见。plan 01 的 coverage D6 与 plan 02/03 的 Next-Phase-Readiness 均自行标为 `human_judgment: true`,本报告不把它们静默转绿。"
  - test: "E16 的 `--color-text ON --color-surface-mark` 比值"
    expected: "≥ 4.5:1(本报告实测 15.0:1,通过)"
    why_human: "该配对**不在**围栏清单里(check-02 因此看不见它),而 plan 01 的 E16 backstop 陈述引用『CHECK-02: --color-text on --color-surface-mark = 15.88』—— 15.88 实为 `--color-text on --color-surface-page` 的数,该引用在 check-02 输出里不存在(见 W-4)。人工须决定是否把该对补进清单,以及该引用如何修正。"
  - test: "TOKEN-07 的『断言序关系』半场:`REQUIREMENTS.md` 把它标为 `Complete`,但代码库里没有任何脚本比较四个 `--z-*` 的值"
    expected: "人工决定其一:(a) 接受 `VALIDATION.md` 已记录的 manual-only 处置,并把 `REQUIREMENTS.md` 的 `Complete` 降级/加注,使两文档不再表面一致;或 (b) 按 `check-02-contrast.py` 的 `ORDER` 形式补一条机械断言,把 `--z-badge (10) < --z-banner (20) < --z-overlay (100) < --z-selection-menu (200)` 钉死"
    why_human: "本报告已实测:把四个值重新排序后 `check-01`…`check-05` 全部仍会通过。该不变量只存在于 `frontend/style.css:229-231` 的散文注释里(该注释自称 `z-index ordering assertion (TOKEN-07)`,但断言并不存在);`check-05-ui-uat.py:771-776` 断言的是「元素 `z-index` **等于**其令牌」,不是「令牌之间的大小序」。用户已在 `VALIDATION.md` 里裁定本阶段不加断言,故这是裁决项而非本报告单方面翻转的缺口 —— 但 `Complete` 的标记在机械层面**不成立**,不得静默调和。"
behavior_unverified_items: []
coincidental_reliance_items: []
advisory:

  - finding: "WR-01 —— `scripts/probe-05-resolve-color.py:95` 的 `route.fulfill(response=resp, body=mutated)` 继承原响应的 `content-length`,而变异后的 body 更短;探针自身无法区分「令牌被删」与「样式表根本没加载」(两种世界产出逐字相同的四行 `PROBE`)"
    category: other
    reason: "本报告已在真实 chromium-1243 上独立证伪这一疑虑:变异页上 `.hint` 的 `font-size` 仍为 `14px`(来自 `var(--text-base)`),证明样式表确实加载并生效、只少了那一行声明;`rgb(32, 32, 32)` 也确为 `--color-text` 经 `html, body` 规则应用后的值(UA 默认是 `rgb(0, 0, 0)`)。故这是未来静默的健壮性缺口,不是当下的假证明。"
    evidence_status: "independently verified as a robustness gap only — not a current failure"
---

# Phase 04.1: Radix 颜色族重写 Verification Report

**Phase Goal:** 把颜色族从手调 hex 换成 Radix Colors 的 12 步语义刻度(1-2 底 / 3-5 组件底 / 6-8 边框 / 9-10 实心填充 / 11-12 文字),并据此重算 UI-SPEC 令牌清单与 CHECK-02 的 34 对对比度配对。
**Verified:** 2026-09-20T03:24:39Z
**Status:** human_needed
**Re-verification:** Yes — after gap closure (plan 04, CR-01)

**Mode:** 非 MVP(ROADMAP §Phase 04.1 无 `mode: mvp`);goal 非 User Story 形式,MVP 验证段落休眠。

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| R1 | 颜色族换成 Radix 12 步语义刻度(1-2/3-5/6-8/9-10/11-12) | ✓ VERIFIED | 围栏内 tier-1 恰 25 条 = `--white` + 24 个 `--radix-<family>-<step>`;47 个 `--color-*` 全部 `var(--radix-…)` 或 `var(--white)` |
| R2 | UI-SPEC 令牌清单据此重算 | ✓ VERIFIED | 围栏内 `/* PAIR */` 恰 43 条 + `/* ORDER */` 1 条;与 UI-SPEC `### The measured table — all 43 pairs` 同规模 |
| R3 | CHECK-02 对比度配对重算并实测 | ✓ VERIFIED | 自跑 `python3 scripts/check-02-contrast.py` → 44 行 PASS(43 对 + 1 `ORDER`)+ 末行 `PASS: 0 failures`,含 `ORDER 0.363`;exit 0 |
| R4 | 结构产出不动(单一围栏 `:root`、四条守卫命令) | ✓ VERIFIED | `^:root` 计数 1、START/END 各 1;四条守卫全部 `PASS`/exit 0;围栏外**规则名集**与 `e530ead` 逐名相同(`diff` 空) |
| R5 | 不含暗色模式;S-1 间距 12 档与 S-2 14px 一级字号档不改 | ✓ VERIFIED | `git diff e530ead..HEAD -- frontend/style.css` 对 `--space-*` / `--text-*` / `--fw-*` / `--lh-*` / `--radius-*` / `--z-*` 的**声明**零行(唯二命中是 `z-index: var(--z-badge)` 消费者行与 `.tier-desc` 的 opacity 删除行) |
| R6 | 吸收 idi-04 UAT 的 3 项 FAIL 与 `--color-text-muted` 3.23:1 的 AA 倒退 | ✓ VERIFIED | UAT 6 项全 `[pass]`;`--color-text-muted: var(--radix-gray-11)` = `#646464`;check-02 实测 `5.62 --color-text-muted on --color-surface`(旧值 3.23) |
| P1.1 | 围栏内 tier-1 恰 25 条、`--color-*` 恰 47 条 | ✓ VERIFIED | 实测 24 个 `--radix-*` + `--white` = 25;`--color-*` 声明 47 |
| P1.2 | 围栏外 CHECK-01 `PASS`(裸 hex 计数 0) | ✓ VERIFIED | 自跑 `bash scripts/check-01-token-conformance.sh` → `PASS` / exit 0 |
| P1.3 | tier-1 名不再说谎:Tailwind 式名消失 | ✓ VERIFIED | `grep -cE '^\s+--(gray\|green\|blue\|amber\|red\|purple\|black)-'` = 0;唯一非 `--radix-` 的 tier-1 是 `--white` |
| P1.4 | check-02 打印 `PASS: 0 failures` + 43 条配对 + `ORDER 0.363` | ✓ VERIFIED | 自跑原文一致(见 R3) |
| P1.5 | `--color-text-muted` / `--color-text` 成为同族相邻两步 | ✓ VERIFIED | `frontend/style.css:120` `--color-text-muted: var(--radix-gray-11)`;`:118` `--color-text: var(--radix-gray-12)` |
| P1.6 | `--color-border-strong` 由 `#d9d9d9` 变 `--radix-gray-9`(3.24 / 3.15) | ✓ VERIFIED | check-02 实测 `3.24 … on --color-surface-page` / `3.15 … on --color-surface` |
| P1.7 | `#state-badge { z-index: var(--z-badge) }` 恢复,`--z-badge` 重新有消费者 | ✓ VERIFIED(带注记) | `frontend/style.css:590` ↔ `--z-badge: 10`(:232)。**注记:** 本 truth 预设「围栏内有一条 `badge < banner` 序断言」——**该断言不存在**,只有散文注释(:229-231)。详见 W-6 / TOKEN-07 / 人工项 3 |
| P1.8 | `.overlay-card { box-shadow: var(--shadow-overlay) }` 与令牌同次提交落地,围栏外无裸 `rgba()` | ✓ VERIFIED | `:546`(消费);围栏外 `grep -E 'rgba?\('` 为空 |
| P1.9 | `.tier-desc` 的 `opacity: 0.9` 删除,`font-size` / `font-weight` 一字未动 | ✓ VERIFIED | `git diff e530ead..HEAD` 该行:仅 `opacity: 0.9;` 被删;UAT `smoke .tier-desc opacity == 1` PASS |
| P1.10 | `grep -c '^\.hidden {'` == 1 且 `grep -c '!important;'` == 1 | ✓ VERIFIED | 1 / 1 |
| P1.11 | Gate 2 双向为空 | ✓ VERIFIED | 围栏外 `var(--…)` 名集 − 围栏内声明集 = 空;围栏内 `--color-*` 声明集 − 围栏外使用集 = 空(本报告自跑两个 `comm -23`,均空) |
| P1.12 | 运行时:`#state-badge` z-index == `--z-badge`;`.overlay-card` box-shadow ≠ `none`;`.tier-desc` opacity == `1` | ✓ VERIFIED | UAT `smoke` 项三条断言全 PASS(本报告复跑) |
| P1.13 | 30 条「loading/error/empty/partial 态内容与结构未被本阶段改动」 | ✓ VERIFIED | 折叠为一条:围栏外**规则名集**与 `e530ead` 相同;`frontend/app.js` / `frontend/index.html` 在 `e530ead..HEAD` 上 **零 diff** |
| P1.14 | 28 条 UI-SPEC backstop 陈述(`verification: backstop`) | ⚠️ INSUFFICIENT_SPEC | 7 条的比值半边由 check-02 实测覆盖;其余约 21 条的裁切/换行/滚动/缩放/重定位行为无任何自动化证据 → 人工项 1 |
| P2.1 | 围栏外 `var(--radix-gray-11` 使 CHECK-01 非零退出并具名诊断 | ✓ VERIFIED | 本报告独立复跑:`FAIL: 1 tier-1 primitive reference(s) outside the fence` / exit 1(临时树变异) |
| P2.2 | 空转对照证据(旧交替式对同一泄漏样本 `PASS` / exit 0)出现在 SUMMARY 里 | ✓ VERIFIED | SUMMARY 表第 2 行逐字给出;上一轮验证已在临时副本上复现 |
| P2.3 | 裸 hex 半场未被削弱 | ✓ VERIFIED | 本报告独立复跑:注入 `#abc` → `FAIL: 1 bare hex outside the token block` / exit 1 |
| P2.4 | 围栏标记成对断言未被削弱 | ✓ VERIFIED | 上一轮验证自跑:删 END → `FAIL: expected exactly 1 fence START and 1 fence END, found 1/0` / exit 1 |
| P2.5 | check-02 四条硬失败路径在 43 对清单上逐一仍会失败 | ✓ VERIFIED | 上一轮验证自跑四次变异,四条均 exit 1 且具名;本报告复证覆盖率下限代码在 `check-02-contrast.py:150-153` |
| P2.6 | 两个守卫仍零依赖、只读 | ✓ VERIFIED | `check-02` import 集合 = `['re','sys']`;`check-01` 只用 `grep`/`awk`/`wc`/`printf`;均无写文件 |
| P2.7 | `check-01` 的改动只有交替式一处 | ✓ VERIFIED | 上一轮验证 `git diff --numstat` = `+5 / −1` 单文件 |
| P3.1 | check-05 全部颜色断言改为令牌接线,**且该形式不得以失去证伪能力为代价** | ✓ VERIFIED | **CR-01 已关闭。** 结构半边:`grep -c FROZEN_AMBER` = 0、`"rgb(` 字面 = 0、`resolve_color(` 24 处调用点。证伪半边:`resolve_color`(`:258-278`)先读 `documentElement` 上该令牌的声明,空即返回 `null`;`ok()`(`:115-116`)把 `None` 期望值记 BLOCKED(置于 `actual is None` 之前)。变异证明 B-1 自跑成立 |
| P3.2 | 携带项 #9 的具名运行时清单逐条覆盖 | ✓ VERIFIED | 11 项逐条定位到断言(`.hint` :604/:826、`.badge-answered`、`#btn-authorize` :660-662、`.kind-write .event-kind`、`#state-badge` :767/:773、`#ai-route-select`、`#selection-menu` :766/:771、`.overlay-card` box-shadow、`.tier-desc` opacity)。**注记:** 其中 8 项颜色断言的证伪能力本轮由 CR-01 修复恢复 |
| P3.3 | `#doc-pane` → `#doc-panel-body`(D-13),item4 由 BLOCKED 转 ok,期望 `32px 40px` | ✓ VERIFIED | item4 = 24 PASS / 0 FAIL / 0 BLOCKED(本报告复跑) |
| P3.4 | D-12 七条间距/字号漂移以更新期望值接受 HEAD 现状,`style.css` 一字未动 | ✓ VERIFIED | item4 的 6px/10px/16px/18px/24px/14px 各条 PASS |
| P3.5 | z-index 三条断言走 `resolve_token`,承重序关系在渲染层两端被读到 | ✓ VERIFIED(带注记) | `#selection-menu` / `#state-badge` / `#stream-banner` 三条 PASS(`:766-776`)。**注记:** 本 truth 的尾句「使 `badge < banner` 的承重序关系在**渲染层**被断言(而不只在围栏注释里被声明)」**为假** —— 三条断言比较的是「元素 z-index == 其令牌」,没有任何断言比较令牌之间的大小序;该关系**确实只在**围栏注释里被声明。详见 W-6 / TOKEN-07 / 人工项 3 |
| P3.6 | 每条接线断言旁的 `info()` 打印运行时令牌解析值 | ✓ VERIFIED | item3 4 条 INFO 覆盖 12 个令牌;item4 3 条(`:769-770`、`:792`);item5 以 `resolve_color` 内联调用 |
| P3.7 | 全量运行 0 FAIL、item 1/2/3/4/6 PASS 且 0 BLOCKED、item 5 BLOCKED 恰两条、退出码 2、`smoke` 项 PASS | ✓ VERIFIED | 本报告自跑原文:`item 1: PASS (45,0,0)` / `2: PASS (5,0,0)` / `3: PASS (15,0,0)` / `4: PASS (24,0,0)` / `5: BLOCKED (9,0,2)` / `6: PASS (2,0,0)`;`exit=2`;两条 BLOCKED 逐字为 `[p3] 交互冒烟「处理本轮批注」` 与 `[p3] 交互冒烟「发送」` |
| P3.8 | `idi-04-UAT.md` 三条 gap 消解、Summary 计数更新 | ✓ VERIFIED | `result: [pass]` = 6 / `[fail]` = 0;`## Gaps` 三块均 `status: resolved` |
| P3.9 | C-1 下游门引用复核留证(16px / `#4f3422`,五站点) | ✓ VERIFIED | item4 `#brainstorm-view h2 font-size: expected=16px actual=16px`;`grep -cE '#brainstorm-view h2.*8a6508' .planning/ROADMAP.md` = 5 |
| P3.10 | 携带项 #8 被记录而非执行 | ✓ VERIFIED | UAT `## Carry-Forward ②` 明写 Phase 7 须在 `--color-surface` `#f9f9f9` 与 `--color-surface-page` `#fcfcfc` 上重测焦点环;本阶段未改环色 |
| P3.11 | `app.js` / `index.html` / `vendor/` 零改动,`vendor/` 仍只含 `marked.min.js` | ✓ VERIFIED | `git diff --stat e530ead..HEAD -- frontend/app.js frontend/index.html frontend/vendor/` 为空;`ls frontend/vendor/` = `marked.min.js` |

**Score:** 37/38 truths verified (1 abstained: P1.14 `insufficient_spec` → 人工项 1)

> **计分口径与上一轮的一处更正。** 本表沿用上一轮的 38 行(6 Roadmap + 14 Plan 01 + 7 Plan 02 + 11 Plan 03),但上一轮的分母写作 `36` 而它自己的表列了 38 行 —— `6+14+7+11 = 38`,`33/36` 与之不自洽。本报告按 38 行重新计分:CR-01 关闭使 P3.1 翻绿,故 37 绿 / 1 `insufficient_spec`。
>
> **P1.7 与 P3.5 的处理。** 两条都保留了「带注记的 VERIFIED」:它们的**交付物半边**(消费者恢复;三条断言走令牌接线)经本报告独立复核成立,而它们各自携带的**因果尾句**(「围栏内断言的序关系」「序关系在渲染层被断言」)为假。该假尾句不另计为一条 FAILED truth,而是作为 **W-6 / TOKEN-07** 这一条具名发现登记,并升级为人工裁决项 3 —— 避免同一事实被重复扣分,同时不把它静默吸收进绿。

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `frontend/style.css` | 围栏 `:root`:25 tier-1 / 47 `--color-*` / `--shadow-overlay` / 43 `/* PAIR */` + 1 `/* ORDER */` / V-12 注释 / R-1·R-2·R-3 | ✓ VERIFIED | 全部实测命中;单一围栏;围栏外规则名集与 `e530ead` 相同;无裸 hex / rgba;Gate 2 双向空 |
| `scripts/check-01-token-conformance.sh` | 双守卫:tier-1 泄漏(交替式含 `radix`)+ 裸 hex | ✓ VERIFIED | 三半场(tier-1 泄漏 / 裸 hex / 未变异对照)经本报告独立复跑,行为正确 |
| `scripts/check-05-ui-uat.py` | `resolve_color` 的「令牌未声明 → None」分支 + `ok()` 的「期望值为 None → BLOCKED」分支 | ✓ VERIFIED | `:268` 新增 `getPropertyValue` 前置检查(全文件恰 3 处);`:115` `expected is None` 分支恰 1 处;24 处调用点与全部期望值未动(`git diff f5adfa4..HEAD` = `+19/−3` 单文件) |
| `scripts/probe-05-resolve-color.py` | CR-01 的变异证明,不是门 | ✓ VERIFIED | 246 行新文件;`importlib` 按路径复用 harness helper;`PREFIX_PROBE_JS` 与 `68309d0` 的探针体逐字一致;四行 `PROBE …` 输出契约成立;exit 0 |
| `.planning/phases/idi-04-tokens-contract/idi-04-UAT.md` | D-10/D-12/D-13 更新后的期望值与已消解的 `## Gaps` | ✓ VERIFIED | 6 pass / 0 fail;三条 gap `resolved` |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| 围栏 43 条 `/* PAIR */` | 围栏内令牌声明 | check-02 对未声明名 `sys.exit(1)` | ✓ WIRED | 原始标记数 43 == 解析数 43;上一轮变异注入第 44 条 → `FAIL: 44 markers but only 43 parsed` |
| `--color-text-muted` | `--radix-gray-11` | tier-2 → tier-1 `var()` 链 | ✓ WIRED | `frontend/style.css:120` |
| `#state-badge` z-index | `--z-badge` | R-1 恢复的唯一消费者 | ✓ WIRED | `:590` ↔ `:232`;UAT 两条(z-index == 10) |
| `.overlay-card` box-shadow | `--shadow-overlay` | R-2:令牌与消费者同次提交,围栏外无裸 rgba | ✓ WIRED | `:546`;围栏外 `rgba?(` 为空 |
| `check-05.item_smoke` / item3/4/5 颜色断言 | `style.css` 令牌值层 | `resolve_color` / `resolve_token` 运行时解析后与 computed 比对 | ✓ WIRED | **本轮由 CR-01 修复恢复证伪能力**:令牌未声明 → `resolve_color` 返回 `None` → `ok()` 记 BLOCKED(绝不记 PASS)。见 B-1 |
| `check-05.item4` z-index 断言 | `--z-selection-menu` / `--z-badge` / `--z-banner` | `resolve_token` 读 `documentElement` 的 `getPropertyValue` | ✓ WIRED(带缺口) | 链路成立且四条断言 PASS。**缺口:** 没有任何断言比较四个 `--z-*` 之间的大小序 —— 见 W-6 |
| `check-01` tier-1 交替式 | 围栏内 `--radix-<family>-<step>` 名 | 加宽后重新匹配 | ✓ WIRED | 本报告复跑:泄漏样本 → exit 1;未变异 → exit 0。残余缺口 W-2(带空格的 `var( … )`)仍在 |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `scripts/check-05-ui-uat.py` item3 `.hint color` | `muted = resolve_color(page, "--color-text-muted")` | 浏览器 `getComputedStyle` 探针(真实 chromium-1243 无头) | 是(`rgb(100, 100, 100)` = `#646464`,与 `documentElement` 声明一致) | ✓ FLOWING |
| `scripts/check-05-ui-uat.py` item4 z-index 三条 | `resolve_token(page, "--z-…")` | `getComputedStyle(document.documentElement).getPropertyValue` | 是(`200` / `10` / `20`) | ✓ FLOWING |
| `scripts/check-05-ui-uat.py` 颜色断言(未声明令牌分支) | `resolve_color(page, "--t")` | 先读 `documentElement` 声明;空即 `null` | **是 —— 不再退化**。修复前此处返回父级继承色(与真实消费者同值 → 断言恒真);现返回 `null` → BLOCKED。**CR-01 已消解** | ✓ FLOWING(修复后) |
| `frontend/style.css` 围栏令牌 | 静态声明 | 手写 Radix hex | 是(25 tier-1 / 47 tier-2) | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| 四条守卫在真实树上全绿 | `bash scripts/check-01-token-conformance.sh` / `python3 scripts/check-02-contrast.py` / `bash scripts/check-03-hidden-uniqueness.sh` / `bash scripts/check-04-important-count.sh` | `PASS` / `PASS: 0 failures`(44 PASS 行 + `ORDER 0.363`)/ `PASS` / `PASS`,四个 exit 0 | ✓ PASS |
| 全量 UAT | `.venv/bin/python scripts/check-05-ui-uat.py` | 0 条 `^FAIL `;item 1/2/3/4/6 PASS 0 BLOCKED,item 5 BLOCKED(9,0,2);`exit=2` | ✓ PASS(与 P3.7 基线逐项一致) |
| pytest 基线 | `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped, 1 warning in 5.68s` | ✓ PASS |
| **B-1** CR-01 的变异证明(修复前 PASS / 修复后 BLOCKED) | `.venv/bin/python scripts/probe-05-resolve-color.py` | `mutation-applied=yes` / `mutated-prefix-verdict=PASS`(pre_fix_expected=rgb(32,32,32) == hint_computed=rgb(32,32,32))/ `mutated-postfix-verdict=BLOCKED`(expected=`<UNRESOLVED>`)/ `control-verdict=PASS`(rgb(100,100,100));`exit=0` | ✓ PASS |
| **B-2** 变异是否真的发生(独立证伪 WR-01:排除「样式表根本没加载」) | 本报告自写探针:拦截 `/style.css` 只删 `--color-text-muted:` 行,再读 `.hint` 的 `font-size`(来自 `var(--text-base)`,与所删令牌无关) | `style.css` 39068 → 39024 字节(−44,恰一行声明);`.hint` `color` = `rgb(32, 32, 32)` 但 `font-size` = **`14px`** → 样式表确实加载并生效;`resolve_color("--color-text-muted")` = `None` | ✓ PASS(变异真实且非空转) |
| **B-3** `PREFIX_PROBE_JS` 是否忠实反事实 | `git show 68309d0:scripts/check-05-ui-uat.py` 与探针常量逐字比对 | 探针体逐字相同(仅缩进层级不同);`68309d0` 是 plan 04 动手前的树 | ✓ PASS |
| **B-4** check-01 是否真的会失败 | 临时树变异:`var(--radix-gray-11)` 泄漏 → exit 1 `FAIL: 1 tier-1 primitive reference(s) outside the fence`;注入 `#abc` → exit 1 `FAIL: 1 bare hex outside the token block`;未变异 → exit 0 `PASS` | 三例全部符合预期 | ✓ PASS |
| **B-5** 被验证对象未被污染 | `git diff --exit-code -- frontend/style.css`(对 `f5adfa4..HEAD`) | 空;`git status --porcelain -- frontend/` 空;`git diff --diff-filter=D --name-only f5adfa4..HEAD` 空 | ✓ PASS |
| **B-6** 围栏外规则名集不变 | `diff <(e530ead 的 `^[^ ].*\{` 行取 `{` 前) <(HEAD 的)` | `RULE-NAME-SET-IDENTICAL`;围栏外文本仅三处声明 delta(R-1 `+ z-index: var(--z-badge)` / R-2 `+ box-shadow: var(--shadow-overlay)` / R-3 `− opacity: 0.9`) | ✓ PASS |
| **B-7** Gate 2 双向 | 围栏外 `var()` 名集 vs 围栏内声明集,双向 `comm -23` | 两个方向均为空 | ✓ PASS |
| **B-8** TOKEN-07 序关系是否被任何脚本守卫 | `grep -rn -- '--z-badge\|--z-banner\|--z-overlay\|--z-selection-menu' scripts/`(排除 check-05) | **零命中**;`check-05:771-776` 只断言「元素 z-index == 其令牌」 | ✗ **FAIL**(序关系无机械断言 —— W-6 / 人工项 3) |

**B-1 / B-2 是 CR-01 关闭的承重证据,均为本验证会话自跑,非引用 SUMMARY 或 REVIEW。**

### Probe Execution

| Probe | Command | Result | Status |
|-------|---------|--------|--------|
| `scripts/probe-05-resolve-color.py` | `.venv/bin/python scripts/probe-05-resolve-color.py` | 四行 `PROBE …` 齐备,`exit=0` | ✓ PASS |

Step 7c 的常规发现流程(迁移/CLI 阶段的 `scripts/*/tests/probe-*.sh`)在本仓库无对应目录;本阶段声明并交付的探针只有上表这一条,已按其 PLAN 的输出契约逐字复跑。

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| TOKEN-01 | 01, 04 | 单一 `:root` 令牌块、零构建零依赖 | ✓ SATISFIED | `^:root` == 1;无 package.json/build 变更 |
| TOKEN-02 | 01, 02 | 两层分类学;tier-1 名绝不出现在围栏外(机械可查) | ✓ SATISFIED(带残余缺口) | 围栏外 `var(--radix-…)` 被 CHECK-01 抓住(B-4);**带空格的 `var( --radix-… )` 漏网**(W-2) |
| TOKEN-04 | 01 | 令牌块之外零裸 `#hex` | ✓ SATISFIED | CHECK-01 `PASS`;B-4 复证裸 hex 半场会失败 |
| TOKEN-07 | 01, 03 | `--z-*` 令牌化**并断言序关系** | ⚠️ **PARTIAL —— `Complete` 标记不成立** | 令牌化 + 四个消费者(537/590/606/889)成立;三条 UAT 断言证明两端 computed 值。但**序关系本身没有任何机械断言**:唯一载体是 `frontend/style.css:229-231` 的散文注释(该注释自称 `z-index ordering assertion (TOKEN-07)`),`check-05-ui-uat.py:771-776` 断言的是「元素 z-index **等于**其令牌」。**B-8 实测:把四个值重新排序后 `check-01`…`check-05` 全部仍会通过。** `REQUIREMENTS.md:127` 与 `:20` 标 `Complete`,`ROADMAP.md` §04.1 亦写「实质关闭 TOKEN-07(…z-index 序断言重新有消费者…)」—— 两者的前提(存在一条序断言)在代码里**不成立**。`VALIDATION.md` 已诚实地记录该半场为 manual-only(`nyquist_compliant: false`),故这不是静默分歧;但 `Complete` 在机械层面**不被支持**。见 W-6 / 人工项 3 |
| CHECK-01 | 01, 02 | 围栏外裸 hex 即失败 | ✓ SATISFIED | B-4 |
| CHECK-02 | 01, 02, 03, 04 | 对所有声明的令牌配色算 WCAG 对比度 | ✓ SATISFIED | `PASS: 0 failures`;四条硬失败路径经上一轮复证;本轮交付其**验收仪器侧**的证伪修复(CR-01) |
| CHECK-03 | 01, 02, 03 | `.hidden` 唯一性守卫 == 1 | ✓ SATISFIED | 1 / `PASS` |
| CHECK-04 | 01, 02, 03 | `!important` 计数 == 1 | ✓ SATISFIED | 1 / `PASS` |
| A11Y-04 | 01, 03, 04 | WCAG AA 文本对比度失败全部修复 | ✓ SATISFIED | check-02 43 对全 PASS,最低文本对 `--color-text-info on --color-surface-info` 4.53 ≥ 4.5;`.hint` 由 2.73 → 5.62 |
| A11Y-04b | 01, 03 | opacity 合成导致的失败一并覆盖 | ✓ SATISFIED(带残余缺口) | `.tier-desc` `opacity: 0.9` 删除(满不透明度 4.77 ✓);归档 0.75 压暗 6.97 ✓;冻结轮 `opacity: 1` + `saturate(0.6)` 保留且断言 PASS。**残余:** E16 mark 上的正文(`--color-text on --color-surface-mark`)不在清单里(实测 15.0:1 通过,未被 check-02 覆盖 —— W-4 / 人工项 2) |

**无 ORPHANED 需求。** ROADMAP §Phase 04.1 列出的 10 个 ID 全部被至少一份 PLAN 的 `requirements:` 字段认领(01: TOKEN-01/02/04/07, CHECK-02/03/04, A11Y-04/04b;02: CHECK-01, TOKEN-02, CHECK-03, CHECK-04;03: A11Y-04, A11Y-04b, TOKEN-07, CHECK-02/03/04;04: CHECK-02, A11Y-04)。ROADMAP 明确「不触碰 TOKEN-03/05/06/08」,与 4 份 PLAN 的认领一致。

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `frontend/style.css` | 229-231 | **W-6 / TOKEN-07** z-index 序关系只有散文注释,且该注释自称 `z-index ordering assertion (TOKEN-07)` —— 一条**自述为断言却并不存在**的断言 | ⚠️ WARNING | 四个值重新排序后全部守卫仍绿(B-8)。TOKEN-07 的「断言序关系」半场未覆盖;`REQUIREMENTS.md` 的 `Complete` 与 `ROADMAP` 的「实质关闭」在机械层面不成立。预先存在(非 plan 04 引入),用户已在 `VALIDATION.md` 裁定 manual-only → 升级为人工项 3 |
| `scripts/probe-05-resolve-color.py` | 87-95, 123-130 | **IN-02** 变异的**最小性**未被断言:过滤器删掉所有含 `--color-text-muted:` 的行,自检只验「令牌串已消失」。若将来该声明与其它声明/右花括号共行,删掉的不止一个声明而探针仍打印同样的四行 | ℹ️ INFO | 今天可证最小:`style.css:120` 是独占一行的单一声明,`grep -c -- '--color-text-muted:'` = 1。未来重构下的静默风险 |
| `scripts/probe-05-resolve-color.py` | 95 | **WR-01** `route.fulfill(response=resp, body=mutated)` 继承原 `content-length` 而 body 更短;探针无法区分「令牌被删」与「样式表没加载」 | ⚠️ WARNING(本轮已独立证伪为「非当下故障」) | 本报告 B-2 用 `.hint` 的 `font-size` 仍为 `14px` 证明样式表确实加载、只少一行声明;`rgb(32,32,32)` 亦确为 `--color-text` 经 `html, body` 规则应用后的值(UA 默认是 `rgb(0,0,0)`)。故是未来静默的健壮性缺口,非当下的假证明。见 `advisory` |
| `scripts/check-05-ui-uat.py` | 115-116 | **WR-02** `ok()` 的 `expected is None` 分支按**期望值**分桶,不区分解析器:`resolve_token` 的 4 处调用点(`:766-776`、`:1024-1026`)在令牌被删时由 **FAIL 变 BLOCKED**,与两条 by-design 的 AI 冒烟 BLOCKED 同桶 | ⚠️ WARNING | 真实的 z 令牌接线缺陷由「值不相等」(exit 1)降级到「环境状态」(exit 2),`item 4: BLOCKED (24,0,1)` 读起来像环境缺口而非坏令牌。**这是本 commit 唯一一处让守卫「更不响」而非更响的地方**;BLOCKED 仍不是假 PASS,故非阻断 |
| `scripts/check-05-ui-uat.py` | 268-269 | **IN-01** 声明检查是「非空」而非「解析成颜色」:`--color-text-muted: --radix-gray-11;`(漏 `var()`)非空却无效 → 探针与消费者一起退化 → 断言又可 PASS(CR-01 的残余半边) | ℹ️ INFO | 审查者已追查爆散半径:13 个传给 `resolve_color` 的令牌中 12 个在 check-02 清单里且 check-02 对不可解析值 `exit(1)`;唯一的例外 `--color-action-irreversible` 在其单条断言上恰好仍会响亮失败。**边界观察,非活洞**;其清单缺口与已 deferred 的 W-4 同源,不重复计 |
| `scripts/check-05-ui-uat.py` | 873-883, 923-930 | **CR-02** `wait_done("#btn-send")` 谓词是 `el.disabled === false`,而 `app.js` 只在归档态 disable `#btn-send` → 90s 截止是死代码 | ⚠️ WARNING | 预先存在于 `6f52602`,本阶段未触碰 `run_ai_smoke`;默认运行下该行本就 BLOCKED,不影响 P3.7。用户裁定 deferred |
| `scripts/check-01-token-conformance.sh` | 41-43 | **W-2** 交替式要求 `var(--` 无空格,CSS 允许 `var( --radix-gray-11 )` | ⚠️ WARNING | TOKEN-02 的硬不变量仍有机械缺口;用户裁定 deferred |
| `scripts/check-01-token-conformance.sh` | 17-27 | **W-3** 成对断言只数 START/END 的**数量**,不管位置;标记被搬移时 `$outside` 退化为空而 `PASS` | ⚠️ WARNING | 用户裁定 deferred |
| `frontend/style.css` | 279-341 清单 + plan 01 的 E16 backstop | **W-4** 清单缺 `--color-text ON --color-surface-mark`;引用的 `15.88` 实为 `on --color-surface-page` 的数 | ⚠️ WARNING | 实测 text-on-mark = 15.0:1 通过但未被 check-02 覆盖。与人工项 2 同源 |
| `scripts/check-05-ui-uat.py` | 996-997 | **W-5** `read_style(...) != "none"` 在元素缺席时返回 `None`,`None != "none"` 为真 → `smoke #state-badge 可见` 记 PASS | ⚠️ WARNING | 用户裁定 deferred |
| `scripts/check-05-ui-uat.py` | 477-480 / 845 vs 926 / 842-847,1124-1127 | **IN-01·IN-02·IN-03**(上一轮编号)死参数 / 双模式标签不一致 / 默认运行必然 exit 2 | ℹ️ INFO | 用户裁定 deferred |
| `.planning/ui-reviews/` 证据(`idi-04.1-UI-REVIEW.md`) | — | 三条新发现的视觉缺陷:① `.overlay-card` 内 `.danger` 实心按钮画出**蓝边红底**(`:549-555` 与 `:473` 同特异性,后者胜出);② 全站**无任何焦点指示**(grep `:focus`/`outline` = 0),UA 环在新填充上仅 1.26:1 / 1.15:1;③ 实心按钮**无 hover 反馈** | ⚠️ WARNING(新范围,非本阶段目标) | 均为 plan 04 范围之外的新发现;焦点环的**令牌**按携带项 #8 已排给 Phase 7。①需要一条围栏外声明改动(`.overlay-card button.danger { border-color: … }`),UI 审查指出它会是 R-1/R-2/R-3 之后的**第四处**围栏外声明变更,须同样显式记账 —— 交后续阶段裁决,不阻断本阶段 |

**债务标记门:** plan 04 改动的两个源文件中 `TBD` / `FIXME` / `XXX` 计数均为 **0**。无未决债务标记。

**再验证证据门(#3304):** 本轮无 BLOCKER。W-6 是上一轮即已登记的 WARNING(不在上一轮 `gaps:` 里),且 `frontend/style.css` 与 `scripts/check-05-ui-uat.py` 自上一轮验证以来未被改动以引入它 —— 它是预先存在、用户已裁定的项。`advisory` 里的 WR-01 是本轮新范围发现且已由 B-2 独立证伪为「非当下故障」。

### Human Verification Required

1. **28 条 UI-SPEC backstop 陈述** —— 7 条的比值半边已由 check-02 实测覆盖(E1 4.61–16.29 / E2 11.00 / E4 4.53 / E6 5.19–5.82 / E7 10.80 / E13 6.97 / E10 4.77),其余约 21 条是裁切/换行/滚动归属/200% 缩放/菜单重定位这类渲染几何行为,`grep` 与 computed-style 都看不见。plan 01 的 coverage D6 与 plan 02/03 的 Next-Phase-Readiness 均自标 `human_judgment: true`,本报告照录,不静默转绿。

2. **E16 的 `--color-text ON --color-surface-mark`** —— 该对不在清单里(所以 check-02 看不见),而计划引用的 `15.88` 是另一个配对的数。实测 15.0:1 通过,但需人工决定是否补进清单并修正引用。

3. **TOKEN-07 的「断言序关系」半场** —— `REQUIREMENTS.md` 标 `Complete`、`ROADMAP.md` 写「实质关闭」,但代码库里没有任何脚本比较四个 `--z-*` 的值(B-8:重新排序后全部守卫仍绿)。唯一载体是 `frontend/style.css:229-231` 的散文注释,而该注释自称是一条 `z-index ordering assertion (TOKEN-07)`。请人工裁决:(a) 接受 `VALIDATION.md` 已记录的 manual-only 处置并把 `Complete` 降级/加注,或 (b) 按 `check-02-contrast.py` 的 `ORDER` 形式补一条机械断言。本报告不代其裁决,也不把它静默调和进绿。

### Gaps Summary

**CR-01 已真正关闭,而且我按 plan 04 自己的尺子独立复证过它。**

- 修复的形状正确:`resolve_color`(`:258-278`)在创建探针 `div` **之前**先读 `documentElement` 上该令牌的声明,`trim()` 后为空即返回 `null`;已声明令牌的探针体与 `68309d0` 逐字相同。`ok()`(`:115-122`)把 `expected is None` 置于 `actual is None` **之前**,记 BLOCKED —— 不加这一支会落进 `normal(actual) == norm(None)` 恒假分支而记 FAIL。全文件 `getPropertyValue` 恰 3 处、`expected is None` 恰 1 处,与计划的静态门一致。
- 修复**被证明而非被断言**:`scripts/probe-05-resolve-color.py` 自跑 exit 0,四行 `PROBE …` 齐备 —— 同一份被删掉 `--color-text-muted:` 声明的浏览器侧副本上,修复前 `expected=rgb(32,32,32) == actual=rgb(32,32,32)` → **PASS**(提示灰已变成正文黑,渲染是坏的,而 harness 记 PASS),修复后 `expected=<UNRESOLVED>` → **BLOCKED**;未变异对照 `rgb(100,100,100)` → **PASS**。
- **反事实是忠实的**:`PREFIX_PROBE_JS` 与 `git show 68309d0:scripts/check-05-ui-uat.py` 的探针体逐字相同(B-3),所以「修复前会记 PASS」不是自陈。
- **变异真实且非空转**:我没有采信 SUMMARY 或审查者的转述,而是自写探针独立复现(B-2)—— 变异后 `style.css` 由 39068 字节降到 39024(−44,恰一行声明),而 `.hint` 的 `font-size` 仍为 `14px`(来自与所删令牌无关的 `var(--text-base)`),证明样式表确实加载并生效、只少了一行声明;`rgb(32, 32, 32)` 也确为 `--color-text` 经 `html, body` 规则应用后的值(UA 默认是 `rgb(0, 0, 0)`)。这一条同时独立证伪了 WR-01 所担心的「无法区分『删了令牌』与『CSS 没生效』」在**当下**并不成立。
- **修复没有引入另一种空转**:未变异对照仍 PASS;全量 harness 逐项与 P3.7 基线**逐项一致**(0 FAIL;item 1/2/3/4/6 为 PASS 且 0 BLOCKED;item 5 `BLOCKED (9,0,2)`;`exit=2`);pytest `219 passed, 6 skipped`。被验证对象未被污染:`frontend/` 零改动,`frontend/style.css` 在 `f5adfa4..HEAD` 上零 diff。

**值层本身仍然好,而且我复证过它。** 25 tier-1 / 47 tier-2、43 对清单与 `PASS: 0 failures` + `ORDER 0.363`、单一围栏、围栏外**规则名集**与 `e530ead` 相同(仅 R-1/R-2/R-3 三处声明 delta)、Gate 2 双向为空、`app.js`/`index.html`/`vendor/` 零 diff、四条守卫全绿、check-01 的三半场我独立复跑过会失败/会通过。上一轮的 9 条 B-* 证据本轮没有一条出现回归。

**为什么不是 `passed`:** 两条必须保持人工判断的项(28 条 backstop 陈述、E16 的比值归属)仍在 —— 这是本阶段自己声明的 `human_judgment: true`,不是新发现。

**为什么要显式说出 TOKEN-07:** `REQUIREMENTS.md:127` 把 TOKEN-07 标为 `Complete`,`ROADMAP.md` §04.1 也写「实质关闭 TOKEN-07(…z-index 序断言重新有消费者…)」。我按指令自己判:`Complete` 在机械层面**不被支持**。该阶段唯一触及 TOKEN-07 的动作是 R-1 恢复了 `--z-badge` 的消费者,而「序断言」本身**在代码里从未存在** —— 只有 `frontend/style.css:229-231` 一条自称是它的散文注释;`check-05-ui-uat.py:771-776` 断言的是「元素 z-index **等于**其令牌」,不是「令牌之间的大小序」。我实测把四个值重新排序后 `check-01`…`check-05` **全部仍会通过**(B-8)。`VALIDATION.md` 已诚实地把它记为 manual-only(`nyquist_compliant: false`),所以两份文档并非静默分歧 —— 但结论是:**`Complete` 标记应被降级或加注,或补一条机械断言。** 用户已裁定本阶段不加断言,故我把它升级为人工项 3,而不单方面翻成 BLOCKER。

**其余为警告,不阻断:** W-2 / W-3(`check-01` 两处残余缺口)、W-4(清单缺 `--color-text ON --color-surface-mark`)、W-5(`smoke #state-badge 可见` 在元素缺席时记 PASS)、CR-02(发送冒烟不等 AI 调用,预先存在)、IN-01·IN-02·IN-03(上一轮编号)、本轮审查新出的 WR-01(已被 B-2 证伪为当下非故障)与 WR-02(`resolve_token` 的 4 处期望值由 FAIL 变 BLOCKED),以及 UI 审查的三条新范围视觉发现(蓝边红底 / 无焦点指示 / 无 hover 反馈)。全部为用户已裁定或新范围项,均未修、均未静默丢弃。

**需求侧结论:** 10 个需求 ID 全部有认领、无孤儿。TOKEN-01/04、CHECK-01/02/03/04、A11Y-04 完全满足;TOKEN-02 与 A11Y-04b 有机械缺口(见上);**TOKEN-07 的「令牌化 + 消费者恢复」满足,但「断言序关系」半场仍只有散文 —— `Complete` 标记不被支持。**

---

_Verified: 2026-09-20T03:24:39Z_
_Verifier: Claude (gsd-verifier)_

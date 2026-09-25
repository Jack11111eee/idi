---
phase: idi-04.1-radix
verified: 2026-09-25T08:18:03Z
status: passed
score: 37/38 must-haves verified
covered_files:

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

covered_digest: "v1:sha256:27957ceaceab0075d094ffc5f2125301a7ec2060d2a15a2a24450650766c1a4b"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: passed
  previous_score: 37/38
  previous_verified: "2026-09-20T03:24:39Z"
  gaps_closed: []
  gaps_remaining: []
  regressions: []
  reason: "内容真变后的重验证 —— frontend/style.css 与 scripts/check-05-ui-uat.py 在 2026-09-20 之后被 Phase 5/7/8 与 quick 260925-iin 改动,故重跑复核而非重算指纹。详见 §重验证披露"
human_verification:

  - test: "UI-SPEC `## UI Considerations` 的 28 条 backstop 陈述(plan 01 must_haves 中 `verification: backstop` 的 28 条)——E1 七芯片不换行/200% 缩放、E2 六按钮行换行与最长闸门标签不裁切、E3 窄面板实心标签不裁切、E4 最长 streaming 串不裁切、E5 文档面板滚动与 #f9f9f9/#fcfcfc 可区分、E6 折行 .hint 与长引用不裁切、E7 冻结轮滚动与琥珀竖线钉边、E8 长致命错误折行、E9 不可断消息撑高与 --shadow-composer 边缘、E10 模态适配视口、E11 大量长批注滚动列表、E12 大量检查项滚动面板、E13 长归档文档不裁切、E14 选区菜单重定位与长菜单项不截断、E15 最长路由标签不截断、E16 跨行 mark 连续段与长 mark 文字可读"
    expected: "每条陈述在其描述的极端输入下成立;其中 7 条只含 CHECK-02 比值的一半已由 check-02 实测证据覆盖(E1 芯片 4.61–16.29 / E2 闸门标签 11.00 / E4 徽标 4.53 / E6 弱化灰 5.19–5.82 / E7 冻结标记 10.80 / E13 归档 0.75 压暗 6.97 / E10 .tier-desc 满不透明度 4.77),其余裁切/滚动/换行/缩放行为无自动化证据"
    why_human: "这些是渲染几何与极端输入下的视觉行为(裁切、换行、滚动归属、200% 缩放、菜单重定位),grep 与 computed-style 读数都看不见。plan 01 的 coverage D6 与 plan 02/03 的 Next-Phase-Readiness 均自行标为 `human_judgment: true`,本报告不把它们静默转绿。**2026-09-20 的 UAT 第 1 项已裁定 `pass`;但此后 Phase 5/6/7/8 确实改动了排版/布局/焦点渲染面,故本轮复核把该项作为「对当前内容仍待人工确认」保留,而非援引旧裁定。**"
  - test: "E16 的 `--color-text ON --color-surface-mark` 比值"
    expected: "≥ 4.5:1(本报告 2026-09-25 复测 **15.00:1**,通过;与 2026-09-20 的 15.0:1 一致)"
    why_human: "该配对**不在**围栏清单里(check-02 因此看不见它),而 plan 01 的 E16 backstop 陈述引用『CHECK-02: --color-text on --color-surface-mark = 15.88』—— 15.88 实为 `--color-text on --color-surface-page` 的数,该引用在 check-02 输出里不存在(见 W-4)。人工须决定是否把该对补进清单,以及该引用如何修正。"
known_accepted:

  - item: "TOKEN-07 的『断言序关系』半场"
    disposition: "**用户已裁定**(2026-09-20,UAT 第 3 项 resolution (a)):接受 `VALIDATION.md` 记录的 manual-only 处置、不补机械断言;`REQUIREMENTS.md:127` 已由无保留的 `Complete` 改注为 `Complete (PARTIAL — 序关系半场 manual-only,见文末人工验收项)`,该半场移入 `REQUIREMENTS.md:176` 的「人工验收项」段落。本报告照录为已知/已接受项,**不作为缺口**。`nyquist_compliant: false` 因此仍然正确。"
  - item: "LAYOUT-02 的 768–855px 横幅×标题重叠(Phase 6)"
    disposition: "user-accepted override(UI-SPEC A-10)。**不属本阶段**,登记在此仅为避免读者把它读成 04.1 的遗漏。"
  - item: "`.claude/settings.local.json` 的 `Bash(node -e ' *)` 授权(Phase 8)"
    disposition: "owner-accepted trust-boundary decision(2026-09-24)。**不属本阶段**,同上仅作登记。"
behavior_unverified_items: []
coincidental_reliance_items: []
advisory:

  - finding: "WR-01 —— `scripts/probe-05-resolve-color.py:95` 的 `route.fulfill(response=resp, body=mutated)` 继承原响应的 `content-length`,而变异后的 body 更短;探针自身无法区分「令牌被删」与「样式表根本没加载」(两种世界产出逐字相同的四行 `PROBE`)"
    category: other
    reason: "本轮(B-2,2026-09-25)在真实 chromium-1243 上独立复现并证伪这一疑虑:变异页上 `.hint` 的 `font-size` 仍为 `14px`(来自 `var(--text-base)`,与被删令牌无关),证明样式表确实加载并生效、只少了那一行声明;`resolve_color(\"--color-text\")` 仍解析为 `rgb(32, 32, 32)`,证明该读数确为 `--color-text` 经 `html, body` 规则应用后的值(UA 默认是 `rgb(0, 0, 0)`)。故这是未来静默的健壮性缺口,不是当下的假证明。"
    evidence_status: "independently re-verified as a robustness gap only — not a current failure (2026-09-25, B-2)"
---

# Phase 04.1: Radix 颜色族重写 Verification Report

**Phase Goal:** 把颜色族从手调 hex 换成 Radix Colors 的 12 步语义刻度(1-2 底 / 3-5 组件底 / 6-8 边框 / 9-10 实心填充 / 11-12 文字),并据此重算 UI-SPEC 令牌清单与 CHECK-02 的 34 对对比度配对。
**Verified:** 2026-09-25T08:18:03Z(HEAD `0b6283a`,分支 `ui/baseline-and-tokens`)
**Status:** passed(仓库既有惯例:UAT 裁定后 canonicalize;同型先例 `idi-07` 的 `f0f0c31`,本阶段为 `41440e3`)。**本轮复核的验证代理判定仍为 `human_needed`** —— 3 项人工项中 TOKEN-07 的半场已由用户裁定为 manual-only(→ `known_accepted`),另 2 项(28 条 backstop、E16)保留为 UAT 已裁定但需对**当前内容**再确认的记录。两字段的分工见 §重验证披露。
**Re-verification:** Yes —— **内容真变后的重验证**(非记账性指纹刷新)。上一轮为 CR-01 缺口闭合后的重验证(`cc4fdab`);本轮因 `covered_files` 中的两个文件被后续阶段改动而重跑复核面。

**Mode:** 非 MVP(ROADMAP §Phase 04.1 无 `mode: mvp`);goal 非 User Story 形式,MVP 验证段落休眠。

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| R1 | 颜色族换成 Radix 12 步语义刻度(1-2/3-5/6-8/9-10/11-12) | ✓ VERIFIED | 围栏内 tier-1 恰 **25** 条 = `--white` + 24 个 `--radix-<family>-<step>`;围栏内 `--color-*` 声明 **53** 条,其中 **49** 条为 `var(--radix-…)` / `var(--white)`。**更正:** 上一版此格写「47 个 `--color-*` 全部 `var(--radix-…)` 或 `var(--white)`」—— 即使在 2026-09-20 也不成立(当时 47 条里有 1 条 `--color-overlay-backdrop: rgba(0,0,0,0.45)` 是字面量,即 46/47);本阶段自身交付的 47 条**至今一条未少**(逐名比对,`comm -23` 空) |
| R2 | UI-SPEC 令牌清单据此重算 | ✓ VERIFIED | 围栏内 `/* PAIR */` 在 2026-09-20 恰 **43** 条 + `/* ORDER */` 1 条,与 UI-SPEC `### The measured table — all 43 pairs` 同规模。**HEAD 现状:** 清单已增至 **53** 条(`/* PAIR */` 53 + `/* ORDER */` 1),本阶段的 43 条**全部仍在**(逐条比对,0 缺失),新增 10 条来自 Phase 5/7;围栏自带出处注释(`frontend/style.css:427-448`,「Manifest size across six value layers (D-15): 24 / 34 / 43 / 47 / 50 / 53」)。UI-SPEC 仍写 43(阶段时文档,非 covered file) |
| R3 | CHECK-02 对比度配对重算并实测 | ✓ VERIFIED | 本轮自跑 `.venv/bin/python scripts/check-02-contrast.py` → **54 行 PASS(53 对 + 1 `ORDER`)** + 末行 `PASS: 0 failures`,含 `ORDER 0.363  --color-text-muted before --color-text on --color-surface`;exit 0。**计数已变:** 上一版记录 44 行(43 对 + ORDER),现为 54 行,原因同 R2 |
| R4 | 结构产出不动(单一围栏 `:root`、四条守卫命令) | ✓ VERIFIED | `^:root` 计数 **1**;`===== DESIGN TOKENS: START/END` 各 **1**(位于 `:5` / `:568`);四条守卫本轮全部 `PASS`/exit 0;**围栏外规则名集在阶段区间 `e530ead..f5adfa4` 上与基线逐名相同**(`diff` 空,`RULE-NAME-SET-IDENTICAL`)。HEAD 上该集合已被 Phase 5-8 追加(追加、非重排),故本 truth 的证据按**阶段区间**给出 |
| R5 | 不含暗色模式;S-1 间距 12 档与 S-2 14px 一级字号档不改 | ✓ VERIFIED | 阶段区间内 `--space-*` / `--text-*` / `--fw-*` / `--lh-*` / `--radius-*` / `--z-*` 的**声明行**逐前缀 `diff` 全部 `IDENTICAL`(六组);围栏外文本 delta 恰三处(R-1/R-2/R-3)。围栏内无 `prefers-color-scheme` / 暗色块 |
| R6 | 吸收 idi-04 UAT 的 3 项 FAIL 与 `--color-text-muted` 3.23:1 的 AA 倒退 | ✓ VERIFIED | `idi-04-UAT.md` 6 项全 `result: [pass]`,`## Gaps` 三块 `status: resolved`;`--color-text-muted: var(--radix-gray-11)`(`frontend/style.css:117`) = `#646464`;本轮复测 check-02 `5.62 --color-text-muted on --color-surface`(旧值 3.23) |
| P1.1 | 围栏内 tier-1 恰 25 条、`--color-*` 恰 47 条 | ✓ VERIFIED(计数已变) | tier-1 实测 24 个 `--radix-*` + `--white` = **25**(不变)。`--color-*` 声明 **HEAD = 53**;阶段时 47。本阶段交付的 47 条**逐名全在**,新增 6 条(`--color-border-hover` / `--color-focus` / `--color-marker-active` / `--color-overlay-active` / `--color-overlay-hover` / `--color-surface-active`)来自 Phase 7 |
| P1.2 | 围栏外 CHECK-01 `PASS`(裸 hex 计数 0) | ✓ VERIFIED | 本轮自跑 `bash scripts/check-01-token-conformance.sh` → `PASS` / exit 0;直接计数:围栏外裸 hex **0**、围栏外 tier-1 泄漏 **0**、围栏外 `rgba?(` **0** |
| P1.3 | tier-1 名不再说谎:Tailwind 式名消失 | ✓ VERIFIED | `grep -cE '^\s+--(gray\|green\|blue\|amber\|red\|purple\|black)-'` = 0;唯一非 `--radix-` 的 tier-1 是 `--white` |
| P1.4 | check-02 打印 `PASS: 0 failures` + 配对清单 + `ORDER 0.363` | ✓ VERIFIED | 本轮自跑原文一致(见 R3);**配对计数由 43 变 53**,`ORDER 0.363` 逐字不变 |
| P1.5 | `--color-text-muted` / `--color-text` 成为同族相邻两步 | ✓ VERIFIED | `frontend/style.css:117` `--color-text-muted: var(--radix-gray-11)`;`:115` `--color-text: var(--radix-gray-12)`(行号相对 2026-09-20 的 `:120`/`:118` 前移 3 行,因围栏前部被后续阶段追加) |
| P1.6 | `--color-border-strong` 由 `#d9d9d9` 变 `--radix-gray-9`(3.24 / 3.15) | ✓ VERIFIED | 本轮复测 check-02 `3.24 --color-border-strong on --color-surface-page` / `3.15 --color-border-strong on --color-surface` |
| P1.7 | `#state-badge { z-index: var(--z-badge) }` 恢复,`--z-badge` 重新有消费者 | ✓ VERIFIED(带注记) | `frontend/style.css:868` ↔ `--z-badge: 10`(:361)。**注记:** 本 truth 预设「围栏内有一条 `badge < banner` 序断言」——**该断言不存在**,只有散文注释(:358-360)。详见 W-6 / TOKEN-07 / `known_accepted` |
| P1.8 | `.overlay-card { box-shadow: var(--shadow-overlay) }` 与令牌同次提交落地,围栏外无裸 `rgba()` | ✓ VERIFIED | `--shadow-overlay` 声明 `:285`,消费 `:824`;围栏外 `grep -E 'rgba?\('` 为空(本轮直接计数 0) |
| P1.9 | `.tier-desc` 的 `opacity: 0.9` 删除,`font-size` / `font-weight` 一字未动 | ✓ VERIFIED | 阶段区间围栏外 diff 该行:`-.tier-desc { … opacity: 0.9; }` → `+.tier-desc { … }`,仅 `opacity: 0.9;` 被删;UAT `smoke .tier-desc opacity == 1` PASS(本轮 check-05 复跑) |
| P1.10 | `grep -c '^\.hidden {'` == 1 且 `!important` 声明数 == 1 | ✓ VERIFIED | 本轮实测 **1 / 1**(`grep -o '!important;' \| wc -l` = 1)。算术陷阱仍在:`grep -c '!important'` 返回 **5**(4 处为注释散文),不得用作判据 |
| P1.11 | Gate 2 双向为空 | ✓ VERIFIED | 本轮自跑两个 `comm -23`:围栏外 `var(--…)` 名集 − 围栏内声明集 = **空**(367 个围栏外 `var()` 引用全部有声明);围栏内 `--color-*` 声明集 − 围栏外使用集 = **空** |
| P1.12 | 运行时:`#state-badge` z-index == `--z-badge`;`.overlay-card` box-shadow ≠ `none`;`.tier-desc` opacity == `1` | ✓ VERIFIED | 本轮 check-05 `smoke` 项三条断言全 PASS(harness 自跑原文) |
| P1.13 | 30 条「loading/error/empty/partial 态内容与结构未被本阶段改动」 | ✓ VERIFIED | 折叠为一条,证据按**阶段区间**给出:围栏外**规则名集**与 `e530ead` 相同;`git diff --stat e530ead..f5adfa4 -- frontend/app.js frontend/index.html frontend/vendor/` 为空。HEAD 上 `app.js` 已被 Phase 8 改动(那不在本阶段区间内) |
| P1.14 | 28 条 UI-SPEC backstop 陈述(`verification: backstop`) | ⚠️ INSUFFICIENT_SPEC | 7 条的比值半边由 check-02 实测覆盖;其余约 21 条的裁切/换行/滚动/缩放/重定位行为无任何自动化证据 → 人工项 1 |
| P2.1 | 围栏外 `var(--radix-gray-11` 使 CHECK-01 非零退出并具名诊断 | ✓ VERIFIED | 本轮独立复跑(临时树变异):`FAIL: 1 tier-1 primitive reference(s) outside the fence` / exit 1 |
| P2.2 | 空转对照证据(旧交替式对同一泄漏样本 `PASS` / exit 0)出现在 SUMMARY 里 | ✓ VERIFIED | `idi-04.1-02-SUMMARY.md:59-63` 逐字给出「mktemp 副本 + sed 重建旧守卫 + 同一注入样本 → PASS / exit=0」;`:106-107` 复述。本轮未重跑该对照(它是对历史提交 `ecae6cb` 的一次性证明),但其结论与 P2.1 的本轮复跑一致 |
| P2.3 | 裸 hex 半场未被削弱 | ✓ VERIFIED | 本轮独立复跑:注入 `#abc` → `FAIL: 1 bare hex outside the token block` / exit 1 |
| P2.4 | 围栏标记成对断言未被削弱 | ✓ VERIFIED | 本轮独立复跑:删 END → `FAIL: expected exactly 1 fence START and 1 fence END, found 1/0` / exit 1 |
| P2.5 | check-02 四条硬失败路径在清单上逐一仍会失败 | ✓ VERIFIED | 本轮独立复跑四次变异,四条均 exit 1 且具名:① 清空全部 `/* PAIR */` → `FAIL: manifest coverage 0 pairs (0 TEXT / 0 NON-TEXT) below floor 24/20/4`;② 清单写未声明令牌 → `FAIL: unknown token --color-nonexistent-page`;③ 注入畸形 `/* PAIR` → `FAIL: 54 '/* PAIR' markers but only 53 parsed`;④ 注入畸形 `/* ORDER` → `FAIL: 2 '/* ORDER' markers but only 1 parsed` |
| P2.6 | 两个守卫仍零依赖、只读 | ✓ VERIFIED | `check-02` import 集合 = `['re','sys']`;`check-01` 只用 `grep`/`awk`/`wc`/`printf`;均无写文件 |
| P2.7 | `check-01` 的改动只有交替式一处 | ✓ VERIFIED | 阶段区间 `git diff --numstat e530ead..f5adfa4` = `+5 / −1` 单文件;该脚本自 `ecae6cb` 后**未再被任何阶段触碰**(`git log` 全历史仅 5 次提交,最后一次即 `ecae6cb`) |
| P3.1 | check-05 全部颜色断言改为令牌接线,**且该形式不得以失去证伪能力为代价** | ✓ VERIFIED | **CR-01 仍闭合。** 结构半边:`grep -c FROZEN_AMBER` = **0**、`"rgb("` 字面 = **0**、`resolve_color(` 调用点 **40** 处(阶段时 24,新增来自 Phase 7/8 的同型接线)。证伪半边:`resolve_color`(`:435-455`)先读 `documentElement` 上该令牌的声明,空即返回 `null`;`ok()`(`:215-216`)把 `None` 期望值记 BLOCKED(置于 `actual is None` 之前);`expected is None` 全文件 **2** 处(`:215` = CR-01 本体,`:3283` = Phase 7 的 item10 同型守卫)。变异证明 B-1 本轮自跑成立 |
| P3.2 | 携带项 #9 的具名运行时清单逐条覆盖 | ✓ VERIFIED | 11 项逐条定位到断言(`.hint`、`.badge-answered`、`#btn-authorize`、`.kind-write .event-kind`、`#state-badge`、`#ai-route-select`、`#selection-menu`、`.overlay-card` box-shadow、`.tier-desc` opacity 等;HEAD 行号见 §Key Link Verification 与 §Anti-Patterns)。**注记:** 其中 8 项颜色断言的证伪能力由 CR-01 修复恢复 |
| P3.3 | `#doc-pane` → `#doc-panel-body`(D-13),item4 由 BLOCKED 转 ok,期望 `32px 40px` | ✓ VERIFIED(计数已变) | 本轮 check-05 全量复跑:**item 4 = 65 条断言 / 0 FAIL / 0 BLOCKED**(阶段时 24 条,新增来自 Phase 6/7/8 的普查断言)。`#doc-panel-body` 的 `32px 40px` 期望值仍在其中且 PASS |
| P3.4 | D-12 七条间距/字号漂移以更新期望值接受 HEAD 现状,`style.css` 一字未动 | ✓ VERIFIED | item4 的 6px/10px/16px/18px/24px/14px 各条随 item 4 全 PASS;本阶段区间内 `style.css` 仅 R-1/R-2/R-3 三处围栏外 delta |
| P3.5 | z-index 三条断言走 `resolve_token`,承重序关系在渲染层两端被读到 | ✓ VERIFIED(带注记) | `#selection-menu` / `#state-badge` / `#stream-banner` 三条 PASS(`check-05-ui-uat.py:1208-1212`)。**注记:** 本 truth 的尾句「使 `badge < banner` 的承重序关系在**渲染层**被断言(而不只在围栏注释里被声明)」**为假** —— 三条断言比较的是「元素 z-index == 其令牌」,没有任何断言比较令牌之间的大小序;该关系**确实只在**围栏注释里被声明。详见 W-6 / TOKEN-07 / `known_accepted` |
| P3.6 | 每条接线断言旁的 `info()` 打印运行时令牌解析值 | ✓ VERIFIED | 本轮全量输出中 item3 的 4 条 INFO 覆盖 12 个令牌;item4 三条;item5 以 `resolve_color` 内联调用。逐行可见 |
| P3.7 | 全量运行 0 FAIL、item 1/2/3/4/6 PASS 且 0 BLOCKED、item 5 BLOCKED 恰两条、退出码 2、`smoke` 项 PASS | ✓ VERIFIED(计数已变) | 本轮自跑原文:`item 1: PASS (45,0,0)` / `2: PASS (5,0,0)` / `3: PASS (17,0,0)` / `4: PASS (65,0,0)` / `5: BLOCKED (9,0,2)` / `6: PASS (6,0,0)` / `7: PASS (38,0,0)` / `8: PASS (13,0,0)` / `9: PASS (17,0,0)` / `10: PASS (42,0,0)`;`exit=2`。两条 BLOCKED 逐字为 `[p3] 交互冒烟「处理本轮批注」` 与 `[p3] 交互冒烟「发送」`(均 `# 需要真实 AI 调用,默认不执行`)。**注:** 阶段时 item 3/4/6 为 15/24/2,item 7-10 尚不存在 |
| P3.8 | `idi-04-UAT.md` 三条 gap 消解、Summary 计数更新 | ✓ VERIFIED | `result: [pass]` = 6 / `[fail]` = 0;`## Gaps` 三块均 `status: resolved` |
| P3.9 | C-1 下游门引用复核留证(16px / `#4f3422`,五站点) | ✓ VERIFIED(站点数已变) | item4 `#brainstorm-view h2 font-size == var(--text-md)`(=`16px`,`frontend/style.css:324`)PASS;`--color-action-warning` = `var(--radix-amber-12)`(`:135`)。**站点数已变:** `grep -cE '#brainstorm-view h2.*8a6508' .planning/ROADMAP.md` 在阶段时为 5,HEAD 为 **4** —— 少的那处是 Phase 6 执行时改写的 SC 行。失真引用作为下游义务保留(本阶段按 D-12 只记录、不单方面改写未来阶段的门) |
| P3.10 | 携带项 #8 被记录而非执行 | ✓ VERIFIED | `idi-04-UAT.md` `## Carry-Forward ②`(`:311-314`)明写 Phase 7 须在 `--color-surface` `#f9f9f9` 与 `--color-surface-page` `#fcfcfc` 上重测焦点环;本阶段未改环色 |
| P3.11 | `app.js` / `index.html` / `vendor/` 零改动,`vendor/` 仍只含 `marked.min.js` | ✓ VERIFIED | 阶段区间 `git diff --stat e530ead..f5adfa4 -- frontend/app.js frontend/index.html frontend/vendor/` 为空;`ls frontend/vendor/` = `marked.min.js` |

**Score:** 37/38 truths verified (1 abstained: P1.14 `insufficient_spec` → 人工项 1)

> **计分口径。** 本表沿用 38 行(6 Roadmap + 14 Plan 01 + 7 Plan 02 + 11 Plan 03);`6+14+7+11 = 38`。CR-01 闭合使 P3.1 翻绿,故 **37 绿 / 1 `insufficient_spec`**。
>
> **P1.7 与 P3.5 的处理。** 两条都保留「带注记的 VERIFIED」:它们的**交付物半边**(消费者恢复;三条断言走令牌接线)成立,而它们各自携带的**因果尾句**(「围栏内断言的序关系」「序关系在渲染层被断言」)为假。该假尾句不另计为一条 FAILED truth,而是作为 **W-6 / TOKEN-07** 这一条具名发现登记(现为 `known_accepted`)。
>
> **计数变化的三处已逐条标注。** 对比度配对 43 → 53(R2/R3/P1.4)、`--color-*` 47 → 53(P1.1)、check-05 item 3/4/6 的断言数增长并新增 item 7-10(P3.3/P3.7)。三处**均非本阶段结论失效**:本阶段交付的 43 对与 47 条逐项逐名至今全部在位,增长来自 Phase 5/7/8。

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `frontend/style.css` | 围栏 `:root`:25 tier-1 / `--color-*` / `--shadow-overlay` / `/* PAIR */` 清单 + 1 `/* ORDER */` / V-12 注释 / R-1·R-2·R-3 | ✓ VERIFIED | 全部实测命中;单一围栏(`:5` / `:568`,`^:root` == 1);围栏外**规则名集**在阶段区间与 `e530ead` 相同;围栏外无裸 hex / rgba;Gate 2 双向空。**HEAD 计数:** tier-2 53(本阶段 47 全在)、清单 53(本阶段 43 全在) |
| `scripts/check-01-token-conformance.sh` | 双守卫:tier-1 泄漏(交替式含 `radix`)+ 裸 hex | ✓ VERIFIED | 三半场(tier-1 泄漏 / 裸 hex / 未变异对照)本轮独立复跑,行为正确;阶段区间 numstat `+5/−1` |
| `scripts/check-05-ui-uat.py` | `resolve_color` 的「令牌未声明 → None」分支 + `ok()` 的「期望值为 None → BLOCKED」分支 | ✓ VERIFIED | `:437-441` 的 `getPropertyValue` 前置检查(全文件恰 3 处);`:215` `expected is None` 分支在位;40 处调用点与全部期望值未动。该文件此后被 Phase 7/8 与 quick `260925-iin` 改动(新增 item 7-10、item 9 自动跟随断言、item 10 的 `FOCUSABLE_SELECTOR` ↔ `:focus-visible` 同步门),但**未触碰 CR-01 的两处分支** |
| `scripts/probe-05-resolve-color.py` | CR-01 的变异证明,不是门 | ✓ VERIFIED | 246 行;`importlib` 按路径复用 harness helper;`PREFIX_PROBE_JS` 与 `68309d0` 的探针体逐字一致;四行 `PROBE …` 输出契约成立;exit 0。自 `ff0e95c` 后未再被改动 |
| `.planning/phases/idi-04-tokens-contract/idi-04-UAT.md` | D-10/D-12/D-13 更新后的期望值与已消解的 `## Gaps` | ✓ VERIFIED | 6 pass / 0 fail;三条 gap `resolved` |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| 围栏 `/* PAIR */` 清单 | 围栏内令牌声明 | check-02 对未声明名 `sys.exit(1)` | ✓ WIRED | 本轮复跑:标记数 == 解析数(53 == 53);注入第 54 条畸形标记 → `FAIL: 54 markers but only 53 parsed`;写未声明名 → `FAIL: unknown token` |
| `--color-text-muted` | `--radix-gray-11` | tier-2 → tier-1 `var()` 链 | ✓ WIRED | `frontend/style.css:117` |
| `#state-badge` z-index | `--z-badge` | R-1 恢复的唯一消费者 | ✓ WIRED | `:868` ↔ `:361`;check-05 两条断言(smoke 与 item4)均 PASS |
| `.overlay-card` box-shadow | `--shadow-overlay` | R-2:令牌与消费者同次提交,围栏外无裸 rgba | ✓ WIRED | `:824` ↔ `:285`;围栏外 `rgba?(` 为空 |
| `check-05.item_smoke` / item3/4/5 颜色断言 | `style.css` 令牌值层 | `resolve_color` / `resolve_token` 运行时解析后与 computed 比对 | ✓ WIRED | **CR-01 修复的证伪能力在位**:令牌未声明 → `resolve_color` 返回 `None` → `ok()` 记 BLOCKED(绝不记 PASS)。见 B-1 / B-2 |
| `check-05.item4` z-index 断言 | `--z-selection-menu` / `--z-badge` / `--z-banner` | `resolve_token` 读 `documentElement` 的 `getPropertyValue` | ✓ WIRED(带缺口) | 链路成立且三条断言 PASS(`:1208-1212`)。**缺口:** 没有任何断言比较四个 `--z-*` 之间的大小序 —— 见 W-6(已裁定 `known_accepted`) |
| `check-01` tier-1 交替式 | 围栏内 `--radix-<family>-<step>` 名 | 加宽后重新匹配 | ✓ WIRED | 本轮复跑:泄漏样本 → exit 1;未变异 → exit 0。残余缺口 W-2(带空格的 `var( … )`)仍在,已由本轮变异复现 |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `scripts/check-05-ui-uat.py` item3 `.hint color` | `muted = resolve_color(page, "--color-text-muted")` | 浏览器 `getComputedStyle` 探针(真实 chromium-1243 无头) | 是(本轮 B-2 实测 `rgb(100, 100, 100)` = `#646464`,与 `documentElement` 声明一致) | ✓ FLOWING |
| `scripts/check-05-ui-uat.py` item4 z-index 三条 | `resolve_token(page, "--z-…")` | `getComputedStyle(document.documentElement).getPropertyValue` | 是(`200` / `10` / `20`) | ✓ FLOWING |
| `scripts/check-05-ui-uat.py` 颜色断言(未声明令牌分支) | `resolve_color(page, "--t")` | 先读 `documentElement` 声明;空即 `null` | **是 —— 不再退化**。本轮 B-2 复现:删掉 `--color-text-muted:` 后该函数返回 `None`(修复前此处返回父级继承色 `rgb(32,32,32)`,与真实消费者同值 → 断言恒真) | ✓ FLOWING(修复后) |
| `frontend/style.css` 围栏令牌 | 静态声明 | 手写 Radix hex | 是(tier-1 25 / tier-2 53) | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| 四条守卫在真实树上全绿 | `bash scripts/check-01-token-conformance.sh` / `.venv/bin/python scripts/check-02-contrast.py` / `bash scripts/check-03-hidden-uniqueness.sh` / `bash scripts/check-04-important-count.sh` | `PASS` / `PASS: 0 failures`(54 PASS 行 + `ORDER 0.363`)/ `PASS` / `PASS`,四个 exit 0 | ✓ PASS |
| 全量 UAT | `.venv/bin/python scripts/check-05-ui-uat.py --browser bundled` | 0 条 `^FAIL`;item 1/2/3/4/6/7/8/9/10 PASS 且 0 BLOCKED,item 5 `BLOCKED (9,0,2)`;`exit=2` | ✓ PASS(0 FAIL 与 item5 设计性 BLOCKED 与基线一致;逐项断言数已增长,见 P3.7) |
| pytest 基线 | `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped, 1 warning in 8.68s` | ✓ PASS |
| `app.js` 语法 | `node --check frontend/app.js` | 无输出 / exit 0 | ✓ PASS |
| **B-1** CR-01 的变异证明(修复前 PASS / 修复后 BLOCKED) | `.venv/bin/python scripts/probe-05-resolve-color.py` | `mutation-applied=yes` / `mutated-prefix-verdict=PASS`(pre_fix_expected=rgb(32,32,32) == hint_computed=rgb(32,32,32))/ `mutated-postfix-verdict=BLOCKED`(expected=`<UNRESOLVED>`)/ `control-verdict=PASS`(rgb(100,100,100));`exit=0` | ✓ PASS |
| **B-2** 变异是否真的发生(独立证伪 WR-01:排除「样式表根本没加载」) | 本报告自写探针(本轮,真实 chromium-1243):拦截 `/style.css` 只删 `--color-text-muted:` 行,再读 `.hint` 的 `font-size`(来自 `var(--text-base)`,与所删令牌无关) | `orig_bytes=72778 mutated_bytes=72734 delta=44` / `decl_removed_count=1`;`.hint` `color` = `rgb(32, 32, 32)` 而 `font-size` = **`14px`** → 样式表确实加载并生效;`resolve_color("--color-text-muted")` = `None`;`resolve_color("--color-text")` = `rgb(32, 32, 32)`(证明该读数非 UA 默认 `rgb(0,0,0)`)。`exit=0` | ✓ PASS(变异真实且非空转) |
| **B-3** `PREFIX_PROBE_JS` 是否忠实反事实 | `git show 68309d0:scripts/check-05-ui-uat.py` 与探针常量逐字比对 | 探针体逐字相同(仅缩进层级不同);`68309d0` 是 plan 04 动手前的树 | ✓ PASS(承自上一轮;该常量自 `ff0e95c` 未改) |
| **B-4** check-01 是否真的会失败 | 临时树变异(本轮复跑):`var(--radix-gray-11)` 泄漏 → exit 1 `FAIL: 1 tier-1 primitive reference(s) outside the fence`;注入 `#abc` → exit 1 `FAIL: 1 bare hex outside the token block`;删 END 标记 → exit 1 `FAIL: expected exactly 1 fence START and 1 fence END, found 1/0`;未变异 → exit 0 `PASS` | 四例全部符合预期 | ✓ PASS |
| **B-5** 被验证对象未被污染 | `git status --porcelain -- frontend/`;`git diff --diff-filter=D --name-only e530ead..f5adfa4` | 本轮 `frontend/` 工作树干净;阶段区间无删除文件 | ✓ PASS |
| **B-6** 围栏外规则名集不变 | `diff <(e530ead 的 `^[^ ].*\{` 行取 `{` 前) <(f5adfa4 的)` | `RULE-NAME-SET-IDENTICAL`;围栏外文本仅三处声明 delta(R-1 `+ z-index: var(--z-badge)` / R-2 `+ box-shadow: var(--shadow-overlay)` / R-3 `− opacity: 0.9`) | ✓ PASS |
| **B-7** Gate 2 双向 | 围栏外 `var()` 名集 vs 围栏内声明集,双向 `comm -23` | 两个方向均为空 | ✓ PASS |
| **B-8** TOKEN-07 序关系是否被任何脚本守卫 | `grep -rn -- '--z-badge\|--z-banner\|--z-overlay\|--z-selection-menu' scripts/`(排除 check-05) | 命中 **2** 行,均在 `scripts/probe-menu-modal-reachability.py:4-5` 的**注释散文**里(该探针测的是菜单可达性,不比较四个令牌的值);`check-05-ui-uat.py:1208-1212` 只断言「元素 z-index == 其令牌」。**无任何机械断言比较令牌之间的大小序** | ✗ **FAIL**(序关系无机械断言 —— W-6 / `known_accepted`;用户已裁定 manual-only) |
| **B-9** check-01 两处残余缺口是否仍在 | 临时树变异(本轮新增) | ① `var( --radix-gray-11 )`(var 内带空格)→ `PASS` / exit 0(**W-2 复现**);② 把 END 标记搬到 START 之前(数量仍 1/1、位置互换)→ `PASS` / exit 0(**W-3 复现**) | ✗ **FAIL**(两处缺口均仍在;用户裁定 deferred,不阻断) |

**B-1 / B-2 是 CR-01 闭合的承重证据,均为本验证会话自跑,非引用 SUMMARY 或 REVIEW。B-4 / B-9 为本轮新跑的变异证据。**

### Probe Execution

| Probe | Command | Result | Status |
|-------|---------|--------|--------|
| `scripts/probe-05-resolve-color.py` | `.venv/bin/python scripts/probe-05-resolve-color.py` | 四行 `PROBE …` 齐备,`exit=0` | ✓ PASS |

Step 7c 的常规发现流程(迁移/CLI 阶段的 `scripts/*/tests/probe-*.sh`)在本仓库无对应目录;本阶段声明并交付的探针只有上表这一条,已按其 PLAN 的输出契约逐字复跑。

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| TOKEN-01 | 01, 04 | 单一 `:root` 令牌块、零构建零依赖 | ✓ SATISFIED | `^:root` == 1;无 package.json/build 变更 |
| TOKEN-02 | 01, 02 | 两层分类学;tier-1 名绝不出现在围栏外(机械可查) | ✓ SATISFIED(带残余缺口) | 围栏外 `var(--radix-…)` 被 CHECK-01 抓住(B-4);**带空格的 `var( --radix-… )` 漏网**(W-2,本轮 B-9 复现) |
| TOKEN-04 | 01 | 令牌块之外零裸 `#hex` | ✓ SATISFIED | CHECK-01 `PASS`;B-4 复证裸 hex 半场会失败 |
| TOKEN-07 | 01, 03 | `--z-*` 令牌化**并断言序关系** | ⚠️ **PARTIAL —— 序关系半场 manual-only(用户已裁定)** | 令牌化 + 四个消费者成立(`:815` overlay / `:868` badge / `:884` banner / `:1219` selection-menu);check-05 三条断言证明两端 computed 值。但**序关系本身没有任何机械断言**:唯一载体是 `frontend/style.css:358-360` 的散文注释(该注释自称 `z-index ordering assertion (TOKEN-07)`),`check-05-ui-uat.py:1208-1212` 断言的是「元素 z-index **等于**其令牌」。**B-8 实测:没有任何脚本比较四个值。** `REQUIREMENTS.md:127` 现标 `Complete (PARTIAL — 序关系半场 manual-only,见文末人工验收项)`,与 `:176` 的人工验收项段落一致;`VALIDATION.md` 记为 `nyquist_compliant: false`。用户 2026-09-20 裁定 (a)(不补断言),故这是**已裁定的 manual-only**,非静默分歧 |
| CHECK-01 | 01, 02 | 围栏外裸 hex 即失败 | ✓ SATISFIED | B-4 |
| CHECK-02 | 01, 02, 03, 04 | 对所有声明的令牌配色算 WCAG 对比度 | ✓ SATISFIED | `PASS: 0 failures`(53 对 + ORDER);四条硬失败路径本轮逐一复证(P2.5);交付了验收仪器侧的证伪修复(CR-01) |
| CHECK-03 | 01, 02, 03 | `.hidden` 唯一性守卫 == 1 | ✓ SATISFIED | 1 / `PASS` |
| CHECK-04 | 01, 02, 03 | `!important` 计数 == 1 | ✓ SATISFIED | 1 / `PASS` |
| A11Y-04 | 01, 03, 04 | WCAG AA 文本对比度失败全部修复 | ✓ SATISFIED | check-02 53 对全 PASS,最低文本对仍为 `--color-text-info on --color-surface-info` **4.53** ≥ 4.5;`.hint` 由 2.73 → 5.62 |
| A11Y-04b | 01, 03 | opacity 合成导致的失败一并覆盖 | ✓ SATISFIED(带残余缺口) | `.tier-desc` `opacity: 0.9` 删除(满不透明度 4.77 ✓);归档 0.75 压暗 6.97 ✓;冻结轮 `opacity: 1` + `saturate(0.6)` 保留且断言 PASS。**残余:** E16 mark 上的正文(`--color-text on --color-surface-mark`)不在清单里(本轮实测 **15.00:1** 通过,未被 check-02 覆盖 —— W-4 / 人工项 2) |

**无 ORPHANED 需求。** ROADMAP §Phase 04.1 列出的 10 个 ID 全部被至少一份 PLAN 的 `requirements:` 字段认领(01: TOKEN-01/02/04/07, CHECK-02/03/04, A11Y-04/04b;02: CHECK-01, TOKEN-02, CHECK-03, CHECK-04;03: A11Y-04, A11Y-04b, TOKEN-07, CHECK-02/03/04;04: CHECK-02, A11Y-04)。ROADMAP 明确「不触碰 TOKEN-03/05/06/08」,与 4 份 PLAN 的认领一致。**TOKEN-08 的 `.collapse-indicator` 字面量**(上一轮尚在 backlog `999.1` 的已知项)**已由 quick `260925-iin` FIX 3 关闭** —— 围栏新增 `--text-lg-plus: 20px` 与 `--lh-none: 1`,该规则改写为消费这两个令牌。本报告此前只把 TOKEN-08 记为「不触碰」,未把它登记为开放项,故无需改判。

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `frontend/style.css` | 358-360 | **W-6 / TOKEN-07** z-index 序关系只有散文注释,且该注释自称 `z-index ordering assertion (TOKEN-07)` —— 一条**自述为断言却并不存在**的断言 | ⚠️ WARNING | 四个值重新排序后全部守卫仍绿(B-8:无任何脚本比较它们)。TOKEN-07 的「断言序关系」半场未覆盖。**预先存在**(非 plan 04 引入),用户已裁定 manual-only → 登记为 `known_accepted`,不作为缺口 |
| `scripts/probe-05-resolve-color.py` | 87-95, 123-130 | **IN-02** 变异的**最小性**未被断言:过滤器删掉所有含 `--color-text-muted:` 的行,自检只验「令牌串已消失」。若将来该声明与其它声明/右花括号共行,删掉的不止一个声明而探针仍打印同样的四行 | ℹ️ INFO | 今天可证最小:本轮 `grep -c -- '--color-text-muted:' frontend/style.css` = **1**,B-2 实测删掉恰 44 字节 / 1 条声明。未来重构下的静默风险 |
| `scripts/probe-05-resolve-color.py` | 95 | **WR-01** `route.fulfill(response=resp, body=mutated)` 继承原 `content-length` 而 body 更短;探针无法区分「令牌被删」与「样式表没加载」 | ⚠️ WARNING(本轮已独立证伪为「非当下故障」) | 本轮 B-2 用 `.hint` 的 `font-size` 仍为 `14px` 证明样式表确实加载、只少一行声明;`resolve_color("--color-text")` 仍为 `rgb(32,32,32)`。故是未来静默的健壮性缺口,非当下的假证明。见 `advisory` |
| `scripts/check-05-ui-uat.py` | 215-216 | **WR-02** `ok()` 的 `expected is None` 分支按**期望值**分桶,不区分解析器:`resolve_token` 的调用点(如 `:1203-1212`、`:3959-3961`)在令牌被删时由 **FAIL 变 BLOCKED**,与两条 by-design 的 AI 冒烟 BLOCKED 同桶 | ⚠️ WARNING | 真实的 z 令牌接线缺陷由「值不相等」(exit 1)降级到「环境状态」(exit 2),`item 4: BLOCKED (…,0,1)` 读起来像环境缺口而非坏令牌。**这仍是让守卫「更不响」而非更响的一处**;BLOCKED 仍不是假 PASS,故非阻断 |
| `scripts/check-05-ui-uat.py` | 437-441 | **IN-01** 声明检查是「非空」而非「解析成颜色」:`--color-text-muted: --radix-gray-11;`(漏 `var()`)非空却无效 → 探针与消费者一起退化 → 断言又可 PASS(CR-01 的残余半边) | ℹ️ INFO | 13 个传给 `resolve_color` 的令牌中 12 个在 check-02 清单里且 check-02 对不可解析值 `exit(1)`;唯一例外 `--color-action-irreversible` 在其单条断言上恰好仍会响亮失败。**边界观察,非活洞**;与已 deferred 的 W-4 同源 |
| `scripts/check-05-ui-uat.py` | 873-883, 923-930 | **CR-02** `wait_done("#btn-send")` 谓词是 `el.disabled === false`,而 `app.js` 只在归档态 disable `#btn-send` → 90s 截止是死代码 | ⚠️ WARNING | 预先存在于 `6f52602`,本阶段未触碰 `run_ai_smoke`;默认运行下该行本就 BLOCKED,不影响 P3.7。用户裁定 deferred |
| `scripts/check-01-token-conformance.sh` | 41-43 | **W-2** 交替式要求 `var(--` 无空格,CSS 允许 `var( --radix-gray-11 )` | ⚠️ WARNING | TOKEN-02 的硬不变量仍有机械缺口。**本轮 B-9 复现**:带空格的泄漏样本 → `PASS` / exit 0。用户裁定 deferred |
| `scripts/check-01-token-conformance.sh` | 17-20 | **W-3** 成对断言只数 START/END 的**数量**,不管位置;标记被搬移时 `$outside` 退化为空而 `PASS` | ⚠️ WARNING | **本轮 B-9 复现**:END 搬到 START 之前(数量仍 1/1)→ `PASS` / exit 0。用户裁定 deferred |
| `frontend/style.css` | 455-567 清单 + plan 01 的 E16 backstop | **W-4** 清单缺 `--color-text ON --color-surface-mark`;引用的 `15.88` 实为 `on --color-surface-page` 的数 | ⚠️ WARNING | 本轮实测 text-on-mark = **15.00:1** 通过但未被 check-02 覆盖;text-on-page = 15.88 逐字复现。与人工项 2 同源 |
| `scripts/check-05-ui-uat.py` | 3947-3949 | **W-5** `read_style(...) != "none"` 在元素缺席时返回 `None`,`None != "none"` 为真 → `smoke #state-badge 可见` 记 PASS | ⚠️ WARNING | 用户裁定 deferred |
| `scripts/check-05-ui-uat.py` | 477-480 / 845 vs 926 / 842-847,1124-1127 | **IN-01·IN-02·IN-03**(上一轮编号)死参数 / 双模式标签不一致 / 默认运行必然 exit 2 | ℹ️ INFO | 用户裁定 deferred |
| `.planning/ui-reviews/` 证据(`idi-04.1-UI-REVIEW.md`) | — | 三条新发现的视觉缺陷:① `.overlay-card` 内 `.danger` 实心按钮画出**蓝边红底**;② 全站**无任何焦点指示**(当时 grep `:focus`/`outline` = 0);③ 实心按钮**无 hover 反馈** | ℹ️ INFO(新范围,非本阶段目标;②③ 已由 Phase 7 处置) | ①需要一条围栏外声明改动,UI 审查指出它会是 R-1/R-2/R-3 之后的**第四处**围栏外声明变更,须同样显式记账 —— 交后续阶段裁决,不阻断本阶段。②③ 已由 Phase 7 的 `:focus-visible` 规则与 hover/active 叠层落地(本轮 check-05 item 10 与 SC5/SC5′ 全 PASS) |

**债务标记门:** 本阶段改动的四个源文件中 `TBD` / `FIXME` / `XXX` 计数均为 **0**(本轮复核)。无未决债务标记。

**再验证证据门(#3304):** 本轮无 BLOCKER。W-6 是上一轮即已登记的 WARNING(不在上一轮 `gaps:` 里),且其载体 `frontend/style.css` 虽自上一轮以来被改动(Phase 5/7/8),但该改动**追加**令牌与规则,并未引入或加剧 W-6;用户已裁定 manual-only。`advisory` 里的 WR-01 是本报告上一轮的新范围发现且已由 B-2 独立证伪为「非当下故障」。B-9 复现的 W-2/W-3 是上一轮已登记、用户已裁定 deferred 的项。

### Human Verification Required

1. **28 条 UI-SPEC backstop 陈述** —— 7 条的比值半边已由 check-02 实测覆盖(E1 4.61–16.29 / E2 11.00 / E4 4.53 / E6 5.19–5.82 / E7 10.80 / E13 6.97 / E10 4.77),其余约 21 条是裁切/换行/滚动归属/200% 缩放/菜单重定位这类渲染几何行为,`grep` 与 computed-style 都看不见。plan 01 的 coverage D6 与 plan 02/03 的 Next-Phase-Readiness 均自标 `human_judgment: true`,本报告照录,不静默转绿。**注:** `idi-04.1-UAT.md` 第 1 项已于 2026-09-20 裁定 `pass`,但此后 Phase 5/6/7/8 确实改动了排版/布局/焦点渲染面;本轮复核保留该项为「对当前内容仍待人工确认」,不援引旧裁定代替。

2. **E16 的 `--color-text ON --color-surface-mark`** —— 该对不在清单里(所以 check-02 看不见),而计划引用的 `15.88` 是另一个配对的数。本轮实测 **15.00:1** 通过,但需人工决定是否补进清单并修正引用。

### Known / Accepted(已裁定,非缺口)

1. **TOKEN-07 的「断言序关系」半场** —— 用户 2026-09-20 裁定 (a):接受 `VALIDATION.md` 记录的 manual-only 处置、**不补**机械断言;`REQUIREMENTS.md:127` 已由无保留的 `Complete` 改注为 `Complete (PARTIAL — 序关系半场 manual-only,见文末人工验收项)`,该半场移入 `:176` 的人工验收项段落。`nyquist_compliant: false` 因此**仍然正确**。本报告不代其裁决,也不把它静默调和进绿 —— 它被登记为已知/已接受。
2. **LAYOUT-02 的 768–855px 横幅×标题重叠** —— user-accepted override(UI-SPEC A-10)。属 Phase 6,登记于此仅为避免误读为 04.1 的遗漏。
3. **`.claude/settings.local.json` 的 `Bash(node -e ' *)` 授权** —— owner-accepted(2026-09-24)。属 Phase 8,同上仅作登记。
4. **TOKEN-08 的 `.collapse-indicator` 字面量** —— 曾是 backlog `999.1` 的已知开放项,**已由 quick `260925-iin` FIX 3 关闭**(围栏新增 `--text-lg-plus: 20px` / `--lh-none: 1`,规则改写为消费这两个令牌)。本报告此前未把它登记为开放项,故无改判。

### Gaps Summary

**本轮无缺口。CR-01 的修复在 HEAD 上仍然完好,而且我按 plan 04 自己的尺子重新独立复证过它。**

- 修复的形状正确:`resolve_color`(`:435-455`)在创建探针 `div` **之前**先读 `documentElement` 上该令牌的声明,`trim()` 后为空即返回 `null`;已声明令牌的探针体与 `68309d0` 逐字相同。`ok()`(`:215-216`)把 `expected is None` 置于 `actual is None` **之前**,记 BLOCKED。全文件 `getPropertyValue` 恰 3 处、`expected is None` 恰 2 处(第 2 处 `:3283` 是 Phase 7 的同型守卫)。
- 修复**被证明而非被断言**:`scripts/probe-05-resolve-color.py` 本轮自跑 exit 0,四行 `PROBE …` 齐备 —— 同一份被删掉 `--color-text-muted:` 声明的浏览器侧副本上,修复前 `expected=rgb(32,32,32) == actual=rgb(32,32,32)` → **PASS**,修复后 `expected=<UNRESOLVED>` → **BLOCKED**;未变异对照 `rgb(100,100,100)` → **PASS**。
- **变异真实且非空转**:本轮 B-2 自写探针独立复现 —— 变异后 body 由 72778 字节降到 72734(−44,`decl_removed_count=1`),而 `.hint` 的 `font-size` 仍为 `14px`(来自与所删令牌无关的 `var(--text-base)`),证明样式表确实加载并生效、只少了一行声明;`resolve_color("--color-text")` = `rgb(32, 32, 32)` 也确为 `--color-text` 经 `html, body` 规则应用后的值(UA 默认是 `rgb(0, 0, 0)`)。这一条同时独立证伪了 WR-01 所担心的「无法区分『删了令牌』与『CSS 没生效』」在**当下**并不成立。
- **修复没有引入另一种空转**:全量 harness 0 FAIL、item 5 为设计性 `BLOCKED (9,0,2)`、`exit=2`;pytest `219 passed, 6 skipped`;`node --check frontend/app.js` OK。

**值层本身仍然好,而且我在 HEAD 上逐项复证过它。** 25 tier-1(24 `--radix-*` + `--white`);本阶段交付的 47 条 `--color-*` **逐名全在**;本阶段交付的 43 对清单 **逐条全在**;单一围栏(`:5`/`:568`,`^:root` == 1);围栏外**规则名集**在阶段区间与 `e530ead` 相同(仅 R-1/R-2/R-3 三处声明 delta);围栏外裸 hex / tier-1 泄漏 / `rgba?(` 均为 0;Gate 2 双向为空;六组非颜色刻度声明在阶段区间逐前缀 `IDENTICAL`;`app.js`/`index.html`/`vendor/` 在阶段区间零 diff;四条守卫全绿;check-01 的三半场与 check-02 的四条硬失败路径我独立复跑过会失败/会通过。上一轮的 9 条 B-* 证据本轮没有一条出现回归。

**为什么要说清计数变化:** 本报告上一版记录的是 2026-09-20 的计数(43 对 / 47 条 tier-2 / check-05 item 3/4/6 = 15/24/2)。这些数字在 HEAD 上**都已变大**(53 对 / 53 条 / 17/65/6,并新增 item 7-10),原因全部是 Phase 5/7/8 在同一份 `style.css` 与 `check-05-ui-uat.py` 上**追加**。本阶段自身交付的每一条都逐名逐条在位,故这是「计数变了、结论没变」,不是缺口。围栏自带出处注释(`frontend/style.css:427-448`)逐层记录 24 / 34 / 43 / 47 / 50 / 53,与实测一致。

**为什么不是 `human_needed`(本轮):** 上一轮验证代理的判定是 `human_needed`(3 项人工项);`idi-04.1-UAT.md` 随后对三项全部裁定 `pass`,TOKEN-07 的半场被移入 `known_accepted`,状态按仓库既有惯例 canonicalize 为 `passed`(同型先例:`idi-07` 的 `f0f0c31`「canonicalize verification status to passed after UAT」;本阶段为 `41440e3`)。本轮复核未发现任何结论失效,故维持 `passed`;§Human Verification Required 保留的 2 项是对**当前内容**仍待人工确认的记录,不是未裁决的缺口。详见下节。

### 重验证披露(内容真变,非记账性刷新)

**为什么重跑复核而不是只重算指纹。** 本报告的 `covered_digest` 是 `covered_files` 的原始字节 sha256,而其中两个文件在 2026-09-20 的验证之后**确实被改动**:

- `frontend/style.css` —— 被 Phase 5/6/7/8 改动(新增 tier-2 令牌与围栏外规则),最近又被 quick `260925-iin` FIX 3 改动:在 `:root` 围栏内**追加**两条声明(`--text-lg-plus: 20px` 作为 `--text-lg` 之后的第 8 档、`--lh-none: 1`),并把 `.collapse-indicator` 改写为消费这两条(原为 `font-size: 20px; line-height: 1`),另有三处围栏注释同步(字号档数 7→8、行高条数 4→5、嵌入刻度数字梯)。
- `scripts/check-05-ui-uat.py` —— 被 Phase 7/8 改动,最近被 quick `260925-iin` FIX 2(item9 新增自动跟随断言,16→17)、FIX 4(修正 `:824` 附近的陈旧散文串)、FIX 5(新增静态 `FOCUSABLE_SELECTOR` ↔ `:focus-visible` 枚举同步门,item 10 41→42)。

**本阶段自己的值层没有被 `260925-iin` 触碰:** 25 条 tier-1、本阶段的 47 条 tier-2、本阶段的 43 对清单、四条守卫命令,逐名逐条比对全部在位(0 缺失)。故本轮是「重跑复核面」,不是「重算指纹了事」—— 所有 gate 都在 HEAD 上第一手重跑,所有结论都在 HEAD 上重新落定。

**`covered_files` 的变更(用户 2026-09-25 裁定)。** 删除了 `.planning/REQUIREMENTS.md`。理由是本报告上一版 §Gaps Summary 已提出的结构性观察:该文件同时出现在 `idi-04` 与本报告的 `covered_files` 里,而每次 `phase.complete` 都会改它 —— 于是**任何一次阶段收口都会同时打掉此前所有覆盖该文件的报告**。`covered_files` 的语义应是「其变更足以使本报告结论失效的输入」,需求索引表属**下游记账**,不满足该语义。用户已采纳该建议并适用于全部六份 v1.14 阶段报告(本报告之外的五份另行处理)。`covered_digest` 随之按**剩余文件集**用位置参数形式重算为 `v1:sha256:27957cea…1a4b`。

**上一版指纹重算的记账性历史(保留,供追溯)。** 2026-09-20 `phase.complete` 依 `idi-04` 的 `passed` 翻转了 `REQUIREMENTS.md` 里 **Phase 4 自己的**需求行(TOKEN-03/05/06 → `Complete`,TOKEN-08 → `Complete (PARTIAL — …)`),当时该文件仍在 `covered_files` 内,故指纹被重算过一次并写有披露。那一次是**记账性**的;本轮不同 —— 本轮是**内容真变**。

**状态字段的两半,以及它们的来历。** 本报告 frontmatter 的 `status: passed` 与正文 `**Status:**` 在上一版里不一致(前者 `passed`、后者 `human_needed`),这不是笔误:

- 2026-09-20 `cc4fdab`(CR-01 缺口闭合后的重验证)把两者都写成 `human_needed`,并列出 3 项人工项。
- 2026-09-20 `idi-04.1-UAT.md` 对 3 项全部裁定 `pass`(第 3 项 resolution (a):接受 manual-only 并把 `REQUIREMENTS.md` 的 TOKEN-07 加注)。
- 2026-09-20 `41440e3` 的提交信息逐字写「**status: stale -> human_needed -> passed.**」—— 即 UAT 裁定后按仓库惯例 canonicalize frontmatter 为 `passed`,**但未同步正文那一行**。同型先例:`idi-07` 的 `f0f0c31`「canonicalize verification status to passed after UAT」只改 frontmatter、正文同样保留 `human_needed`。

本轮据此把两半写清而非继续留一个无解释的矛盾:frontmatter `status: passed` 是 canonical 状态(UAT 已裁定);正文明确标出「本轮复核的验证代理判定仍为 `human_needed`」并说明其构成(TOKEN-07 半场已移入 `known_accepted`,另 2 项保留为对当前内容待人工确认的记录)。读者不应再把两半读成互相矛盾。

**本轮未改动任何其他产物。** 未改 `REQUIREMENTS.md`、`ROADMAP.md`、`idi-04.1-VALIDATION.md`、`frontend/`、`scripts/`,也未触碰其他五份阶段报告;唯一的写入是本文件。

**一处需读者知晓的文档漂移(非本阶段缺口):** `idi-04.1-UI-SPEC.md` 仍写「43 pairs」(阶段时文档),而围栏清单在 HEAD 已是 53 条 —— 增长由 Phase 5/7 追加,围栏自带出处注释(`frontend/style.css:427-448`)已逐层记录。UI-SPEC 不是本报告的 covered file,故不参与指纹,也不改判本阶段结论。

---

_Verified: 2026-09-25T08:18:03Z_
_Verifier: Claude (gsd-verifier)_
_重验证: 2026-09-25 —— 内容真变后的重跑复核(见上节)_
_covered_files 变更: 2026-09-25 —— 移除 `.planning/REQUIREMENTS.md`,指纹按剩余文件集重算(用户裁定)_

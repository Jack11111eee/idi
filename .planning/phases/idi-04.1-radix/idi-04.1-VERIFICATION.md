---
phase: idi-04.1-radix
verified: 2026-09-19T14:41:02Z
status: gaps_found
score: 33/36 must-haves verified
covered_files:
  - .planning/REQUIREMENTS.md
  - .planning/phases/idi-04-tokens-contract/idi-04-UAT.md
  - .planning/phases/idi-04.1-radix/idi-04.1-01-SUMMARY.md
  - .planning/phases/idi-04.1-radix/idi-04.1-02-PLAN.md
  - .planning/phases/idi-04.1-radix/idi-04.1-02-SUMMARY.md
  - .planning/phases/idi-04.1-radix/idi-04.1-03-PLAN.md
  - .planning/phases/idi-04.1-radix/idi-04.1-03-SUMMARY.md
  - frontend/style.css
  - scripts/check-01-token-conformance.sh
  - scripts/check-05-ui-uat.py
covered_digest: "v1:sha256:c4a9f8880b030b57f9c16ccfeb88a46850fb07292eadfc17d621270f3da13ce4"
behavior_unverified: 0
overrides_applied: 0
gaps:
  - truth: "`scripts/check-05-ui-uat.py` 的全部颜色断言改为令牌接线形式(D-14):期望侧来自运行时解析出的 `--token`(`resolve_color`),不再硬编码 `rgb(...)`;且该形式不得以失去证伪能力为代价(plan 01 key_link 的『值层改动不产生假 FAIL』与本阶段『守卫静默空转』的既有失败类)"
    status: failed
    reason: "结构条款成立(22 条 `rgb(...)` 字面已全部改为 `resolve_color(page, \"--token\")`,见 33/36 表中的 P3.1),但『仍能证伪』条款被 CR-01 破坏:`resolve_color` 对未声明的令牌返回**继承色**而非 `None`,而真实消费者用的是同一个 `var(--token)`,两侧同时退化成同一个继承值 → 断言恒真。这是本阶段自己引入的回归:D-14 之前 `.hint color` 断言字面 `rgb(106,106,106)`,改名/删除令牌时会响亮 FAIL;本阶段把它换成 `resolve_color` 之后不能再 FAIL。独立复现见 `## Behavioral Spot-Checks` B-1。"
    artifacts:
      - path: "scripts/check-05-ui-uat.py"
        issue: "`resolve_color`(L250-262)不区分『令牌已声明』与『令牌未声明』;未声明时 `p.style.color = \"var(--t)\"` 在 computed-value 阶段失效 → 探针继承 `body` 的 `color`。27 处调用点(L600-685 item3 / L727-728·L777-778 item4 / L803-826 item5 / L983-984 item6 / L1002-1005 item_smoke)中的颜色断言因此全部失去改名/删除证伪能力。`resolve_token`(L265-275)不受影响(未声明返回 `None`,`ok()` 记 BLOCKED)。"
    missing:
      - "让 `resolve_color` 在令牌未声明时返回 `None`(先读 `getComputedStyle(document.documentElement).getPropertyValue(t)`,空串即返回 `None`),使 `ok()` 记 BLOCKED 而非假 PASS"
      - "为 D-14 补一条与 plan 02 同规格的变异证明:在临时副本上删除 `--color-text-muted` 声明后,该断言必须不再记 PASS(对照证据需进 SUMMARY)"
advisory: []
human_verification:
  - test: "UI-SPEC `## UI Considerations` 的 28 条 backstop 陈述(plan 01 must_haves 中 `verification: backstop` 的 28 条)——E1 七芯片不换行/200% 缩放、E2 六按钮行换行与最长闸门标签不裁切、E3 窄面板实心标签不裁切、E4 最长 streaming 串不裁切、E5 文档面板滚动与 #f9f9f9/#fcfcfc 可区分、E6 折行 .hint 与长引用不裁切、E7 冻结轮滚动与琥珀竖线钉边、E8 长致命错误折行、E9 不可断消息撑高与 --shadow-composer 边缘、E10 模态适配视口、E11 大量长批注滚动列表、E12 大量检查项滚动面板、E13 长归档文档不裁切、E14 选区菜单重定位与长菜单项不截断、E15 最长路由标签不截断、E16 跨行 mark 连续段与长 mark 文字可读"
    expected: "每条陈述在其描述的极端输入下成立;其中 7 条只含 CHECK-02 比值的一半已由 check-02 实测证据覆盖(E1 芯片 4.61–16.29 / E2 闸门标签 11.00 / E4 徽标 4.53 / E6 弱化灰 5.19–5.82 / E7 冻结标记 10.80 / E13 归档 0.75 压暗 6.97 / E10 .tier-desc 满不透明度 4.77),其余裁切/滚动/换行/缩放行为无自动化证据"
    why_human: "这些是渲染几何与极端输入下的视觉行为(裁切、换行、滚动归属、200% 缩放、菜单重定位),grep 与 computed-style 读数都看不见。plan 01 的 coverage D6 与 plan 02/03 的 Next-Phase-Readiness 均自行标为 `human_judgment: true`,本报告不把它们静默转绿。"
  - test: "E16 的 `--color-text ON --color-surface-mark` 比值"
    expected: "≥ 4.5:1(本报告实测 15.0:1,通过)"
    why_human: "该配对**不在**围栏清单里(check-02 因此看不见它),而 plan 01 的 E16 backstop 陈述引用『CHECK-02: --color-text on --color-surface-mark = 15.88』—— 15.88 实为 `--color-text on --color-surface-page` 的数,该引用在 check-02 输出里不存在(见 W-4)。人工须决定是否把该对补进清单,以及该引用如何修正。"
---

# Phase 04.1: Radix 颜色族重写 Verification Report

**Phase Goal:** 把颜色族从手调 hex 换成 Radix Colors 的 12 步语义刻度(1-2 底 / 3-5 组件底 / 6-8 边框 / 9-10 实心填充 / 11-12 文字),并据此重算 UI-SPEC 令牌清单与 CHECK-02 的 34 对对比度配对。
**Verified:** 2026-09-19T14:41:02Z
**Status:** gaps_found
**Re-verification:** No — initial verification

**Mode:** 非 MVP(ROADMAP §Phase 04.1 无 `mode: mvp`);goal 非 User Story 形式,MVP 验证段落休眠。

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| R1 | 颜色族换成 Radix 12 步语义刻度(1-2/3-5/6-8/9-10/11-12) | ✓ VERIFIED | 围栏内 tier-1 恰 25 条 = `--white` + 24 个 `--radix-<family>-<step>`;47 个 `--color-*` 全部 `var(--radix-…)` 或 `var(--white)`;名↔步映射表与四处越轨记账在 `frontend/style.css:8-111` |
| R2 | UI-SPEC 令牌清单据此重算 | ✓ VERIFIED | 围栏内 `/* PAIR */` 恰 43 条 + `/* ORDER */` 1 条;与 UI-SPEC `### The measured table — all 43 pairs` 同规模;三数差异(24/34/43)在围栏注释与 UAT `## Carry-Forward ③` 双处留档 |
| R3 | CHECK-02 对比度配对重算并实测 | ✓ VERIFIED | `python3 scripts/check-02-contrast.py` → 44 行 PASS + 末行 `PASS: 0 failures`,含 `ORDER 0.363`;43 对 = 34 TEXT + 9 NON-TEXT(脚本自报) |
| R4 | 结构产出不动(单一围栏 `:root`、四条守卫命令) | ✓ VERIFIED | `^:root` 计数 1、START/END 各 1;四条守卫全部 `PASS`/exit 0;围栏外规则开集与 `e530ead` **逐字节相同**(`diff` 空,无追加/删除/重排) |
| R5 | 不含暗色模式;S-1 间距 12 档与 S-2 14px 一级字号档不改 | ✓ VERIFIED | `git diff e530ead..HEAD -- frontend/style.css` 对 `--space-*` / `--text-*` / `--fw-*` / `--lh-*` / `--radius-*` / `--z-*` 的声明**零行**;UAT item4 `S-2 DEPENDENCY --text-base 存活为 14px` PASS |
| R6 | 吸收 idi-04 UAT 的 3 项 FAIL 与 `--color-text-muted` 3.23:1 的 AA 倒退 | ✓ VERIFIED | UAT 6 项全 `[pass]`;`--color-text-muted: var(--radix-gray-11)` = `#646464`,check-02 实测 `5.62 --color-text-muted on --color-surface`(旧值 3.23 → 现 5.62) |
| P1.1 | 围栏内 tier-1 恰 25 条、`--color-*` 恰 47 条 | ✓ VERIFIED | 逐名枚举:25 条(9 gray + 2 blue + 3 green + 6 amber + 3 red + 1 violet + `--white`)/ 47 条 |
| P1.2 | 围栏外 CHECK-01 `PASS`(裸 hex 计数 0) | ✓ VERIFIED | `bash scripts/check-01-token-conformance.sh` → `PASS` / exit 0 |
| P1.3 | tier-1 名不再说谎:Tailwind 式名消失 | ✓ VERIFIED | `grep -cE '^\s+--(gray\|green\|blue\|amber\|red\|purple\|black)-'` = 0;唯一非 `--radix-` 的 tier-1 是 `--white`(无对应 Radix 步,名字不说谎) |
| P1.4 | check-02 打印 `PASS: 0 failures` + 43 条配对 + `ORDER 0.363` | ✓ VERIFIED | 复跑原文一致(见上 R3) |
| P1.5 | `--color-text-muted` / `--color-text` 成为同族相邻两步 | ✓ VERIFIED | `frontend/style.css:120` `--color-text-muted: var(--radix-gray-11)`;`--color-text: var(--radix-gray-12)` |
| P1.6 | `--color-border-strong` 由 `#d9d9d9` 变 `--radix-gray-9` `#8d8d8d`(3.24 / 3.15) | ✓ VERIFIED | `frontend/style.css:165`;check-02 实测 `3.24 … on --color-surface-page` / `3.15 … on --color-surface` |
| P1.7 | `#state-badge { z-index: var(--z-badge) }` 恢复,`--z-badge` 重新有消费者 | ✓ VERIFIED | `frontend/style.css:590`;`--z-badge: 10`(:232);UAT item4 `#state-badge z-index == var(--z-badge)` PASS。**注意:** `badge < banner` 的**序关系**在代码里只有散文注释(:229-231),没有任何脚本比较两个值 —— 见 W-6 |
| P1.8 | `.overlay-card { box-shadow: var(--shadow-overlay) }` 与令牌同次提交落地,围栏外无裸 `rgba()` | ✓ VERIFIED | `frontend/style.css:177`(声明)/ `:546`(消费);围栏外 `grep -E 'rgba?\('` 为空;`--shadow-overlay` 与消费者同在 `00c6073` |
| P1.9 | `.tier-desc` 的 `opacity: 0.9` 删除,`font-size` / `font-weight` 一字未动 | ✓ VERIFIED | `git diff e530ead..HEAD` 该行:仅 `opacity: 0.9;` 被删,两属性原样保留;UAT `smoke .tier-desc opacity == 1` PASS |
| P1.10 | `grep -c '^\.hidden {'` == 1 且 `grep -c '!important;'` == 1 | ✓ VERIFIED | 1 / 1 |
| P1.11 | Gate 2 双向为空(每个 `var(--x)` 可解析;每个颜色令牌有消费者) | ✓ VERIFIED | 围栏外 `var(--…)` 名集 − 围栏内声明集 = 空;围栏内 `--color-*` 声明集 − 围栏外使用集 = 空 |
| P1.12 | 运行时:`#state-badge` z-index == `--z-badge`;`.overlay-card` box-shadow ≠ `none`;`.tier-desc` opacity == `1` | ✓ VERIFIED | UAT `smoke` 项三条断言全 PASS(本报告复跑) |
| P1.13 | 30 条「loading/error/empty/partial 态内容与结构未被本阶段改动」 | ✓ VERIFIED | 折叠为一条:围栏外规则开集与 `e530ead` 逐字节相同;`frontend/app.js` / `frontend/index.html` 在 `e530ead..HEAD` 上 **零 diff**;文案零改动 |
| P1.14 | 28 条 UI-SPEC backstop 陈述(`verification: backstop`) | ⚠️ INSUFFICIENT_SPEC | 7 条的比值半边由 check-02 实测覆盖;其余约 21 条的裁切/换行/滚动/缩放/重定位行为无任何自动化证据 → 人工项(见 Human Verification) |
| P2.1 | 围栏外 `var(--radix-gray-11` 使 CHECK-01 非零退出并具名诊断 | ✓ VERIFIED | 自跑变异:`FAIL: 1 tier-1 primitive reference(s) outside the fence` / exit 1 |
| P2.2 | 空转对照证据(旧交替式对同一泄漏样本 `PASS` / exit 0)出现在 SUMMARY 里 | ✓ VERIFIED | SUMMARY 表第 2 行逐字给出;本报告在临时副本上复现:`sed 's/\|radix//'` 重建的旧守卫 → `PASS` / exit 0 |
| P2.3 | 裸 hex 半场未被削弱 | ✓ VERIFIED | 注入 `#abc` → `FAIL: 1 bare hex outside the token block` / exit 1 |
| P2.4 | 围栏标记成对断言未被削弱 | ✓ VERIFIED | 删 END → `FAIL: expected exactly 1 fence START and 1 fence END, found 1/0` / exit 1 |
| P2.5 | check-02 四条硬失败路径在 43 对清单上逐一仍会失败 | ✓ VERIFIED | 自跑四次变异,四条均 exit 1 且具名:未知名 / `44 markers but only 43 parsed` / `coverage 10 pairs … below floor 24/20/4` / `hierarchy inverted 2.753` |
| P2.6 | 两个守卫仍零依赖、只读 | ✓ VERIFIED | `check-02` import 集合 = `['re','sys']`;`check-01` 只用 `grep`/`awk`/`wc`/`printf`(`tail` 仅出现在注释散文);均无写文件 |
| P2.7 | `check-01` 的改动只有交替式一处 | ✓ VERIFIED | `git diff --numstat` = `+5 / −1` 单文件;裸 hex 半场、围栏成对断言、`set -euo pipefail`、`cd "$(dirname "$0")/.."`、`echo PASS; exit 0` 逐字保留 |
| P3.1 | check-05 全部颜色断言改为令牌接线,`FROZEN_AMBER` 与三处字面删除 | ✗ FAILED | 结构半边成立(`grep -c FROZEN_AMBER` = 0;`"rgb(` 字面由 22 条降为 0;`resolve_color` 调用点由 4 增至 27),但**证伪能力半边被 CR-01 破坏** —— 详见 `## Gaps Summary` 与 B-1 |
| P3.2 | 携带项 #9 的具名运行时清单逐条覆盖 | ✓ VERIFIED(带注记) | 11 项逐条定位到断言(`.hint` L600/809、`.badge-answered` L684、`#btn-authorize` color/border/bg L661-666、`.kind-write .event-kind` L617、`#state-badge` color/bg/z-index L680-682·L757、`#ai-route-select`/`#selection-menu` border-top-color L602-605、`.overlay-card` box-shadow L610/L1013、`.tier-desc` opacity L1015)。**注记:** 其中 8 项是颜色断言,其证伪能力受 CR-01 影响 |
| P3.3 | `#doc-pane` → `#doc-panel-body`(D-13),item4 由 BLOCKED 转 ok,期望 `32px 40px` | ✓ VERIFIED | `grep -cE 'read_style\(page, .#doc-pane\b'` = 0 / `…#doc-panel-body\b` = 1;UAT item4 = 24 PASS / 0 FAIL / 0 BLOCKED |
| P3.4 | D-12 七条间距/字号漂移以更新期望值接受 HEAD 现状,`style.css` 一字未动 | ✓ VERIFIED | item4 的 6px/10px/16px/18px/24px/14px 各条 PASS;`git diff e530ead..HEAD -- frontend/style.css` 中无这些规则 |
| P3.5 | z-index 三条断言走 `resolve_token`,承重序关系在渲染层两端被读到 | ✓ VERIFIED(带注记) | `#selection-menu`/`#state-badge`/`#stream-banner` 三条 PASS,两端 computed 值(200/10/20)确在渲染层读出。**注记:** 无任何断言比较 `badge < banner`;`--z-overlay` 无运行时断言 —— 见 W-6 |
| P3.6 | 每条接线断言旁的 `info()` 打印运行时令牌解析值 | ✓ VERIFIED | item3 4 条 INFO 覆盖 12 个令牌;item4 3 条;item5 0 条(以 `resolve_color` 内联调用,无 INFO —— 与陈述的「每条」有轻微落差,但解析值可从上文 INFO 与断言 `expected=` 列读出) |
| P3.7 | 全量运行 0 FAIL、item 1/2/3/4/6 PASS 且 0 BLOCKED、item 5 BLOCKED 恰为两条交互冒烟、退出码 2、`smoke` 项 PASS | ✓ VERIFIED | 自跑原文:`item 1: PASS (45,0,0)` / `2: PASS (5,0,0)` / `3: PASS (15,0,0)` / `4: PASS (24,0,0)` / `5: BLOCKED (9,0,2)` / `6: PASS (2,0,0)`;`exit=2`;两条 BLOCKED 逐字为 `[p3] 交互冒烟「处理本轮批注」` 与 `[p3] 交互冒烟「发送」` |
| P3.8 | `idi-04-UAT.md` 三条 gap 消解、Summary 计数更新 | ✓ VERIFIED | `result: [pass]` = 6 / `[fail]` = 0;`expected:.*#doc-panel-body` = 1 / `…#doc-pane\b` = 0;`## Gaps` 三块均 `status: resolved` 且原文保留为历史对照 |
| P3.9 | C-1 下游门引用复核留证(16px / `#4f3422`,五站点) | ✓ VERIFIED | 自跑 item4:`#brainstorm-view h2 font-size: expected=16px actual=16px`;`color == var(--color-action-warning): expected=rgb(79, 52, 34) actual=rgb(79, 52, 34)`;`grep -cE '#brainstorm-view h2.*8a6508' .planning/ROADMAP.md` = 5(内容锚未失效);UAT `## Carry-Forward ①` 逐站点枚举 |
| P3.10 | 携带项 #8 被记录而非执行 | ✓ VERIFIED | UAT `## Carry-Forward ②` 明写 Phase 7 须在 `--color-surface` `#f9f9f9` 与 `--color-surface-page` `#fcfcfc` 上重测焦点环;本阶段未改环色 |
| P3.11 | `app.js` / `index.html` / `vendor/` 零改动,`vendor/` 仍只含 `marked.min.js` | ✓ VERIFIED | `git diff --stat e530ead..HEAD -- frontend/app.js frontend/index.html frontend/vendor/` 为空;`ls frontend/vendor/` = `marked.min.js` |

**Score:** 33/36 truths verified (1 failed, 1 insufficient_spec/abstained, 1 counted as VERIFIED-with-caveat not double-counted)

> 计分口径:上表 36 行 = 6(Roadmap)+ 14(Plan 01)+ 7(Plan 02)+ 11(Plan 03)。已核实 33 行;1 行 FAILED(P3.1);1 行 ⚠️ INSUFFICIENT_SPEC(P1.14,28 条 backstop);1 行因 CR-01 的注记不计入绿(P3.2 仍计为 VERIFIED,其证伪力削弱记在 P3.1 的 gap 下,不重复扣分)。

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `frontend/style.css` | 围栏 `:root`:25 tier-1 / 47 `--color-*` / `--shadow-overlay` / 43 `/* PAIR */` + 1 `/* ORDER */` / V-12 注释 / R-1·R-2·R-3 | ✓ VERIFIED | 全部实测命中;单一围栏;围栏外规则集逐字节未变;无裸 hex / rgba;Gate 2 双向空 |
| `scripts/check-01-token-conformance.sh` | 双守卫:tier-1 泄漏(交替式含 `radix`)+ 裸 hex | ✓ VERIFIED | 含 `radix` 分支;三半场(radix 泄漏 / 裸 hex / 围栏成对)均自跑变异证明会失败 |
| `scripts/check-05-ui-uat.py` | `item_smoke` 三条令牌接线断言;item2-5 期望侧改 `resolve_color` / `resolve_token` | ⚠️ PARTIAL | 断言与助手均在位且可运行;`resolve_color` 的未声明分支缺失使其颜色断言在改名/删除下恒真(CR-01) |
| `.planning/phases/idi-04-tokens-contract/idi-04-UAT.md` | D-10/D-12/D-13 更新后的期望值与已消解的 `## Gaps` | ✓ VERIFIED | 6 pass / 0 fail;三条 gap `resolved`;`## Carry-Forward` 四节齐备 |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| 围栏 43 条 `/* PAIR */` | 围栏内令牌声明 | check-02 对未声明名 `sys.exit(1)` | ✓ WIRED | 原始标记数 43 == 解析数 43;变异注入第 44 条 → `FAIL: 44 markers but only 43 parsed` |
| `--color-text-muted` | `--radix-gray-11` | tier-2 → tier-1 `var()` 链 | ✓ WIRED | `frontend/style.css:120` |
| `#state-badge` z-index | `--z-badge` | R-1 恢复的唯一消费者 | ✓ WIRED | `:590` ↔ `:232`;UAT 两条(z-index == 10) |
| `.overlay-card` box-shadow | `--shadow-overlay` | R-2:令牌与消费者同次提交,围栏外无裸 rgba | ✓ WIRED | `:177` ↔ `:546`;围栏外 `rgba?(` 为空 |
| `check-05.item_smoke` | `style.css` 令牌值层 | `resolve_color` / `resolve_token` 运行时解析后与 computed 比对 | ⚠️ PARTIAL | 链路存在且跑通,但 `resolve_color` 的退化分支使颜色一侧在令牌未声明时两端同值 —— 见 CR-01 |
| `check-05.item3/4/5` 颜色断言 | 47 个 `--color-*` 令牌 | `resolve_color(page, "--color-…")` | ⚠️ PARTIAL | 同上;`resolve_token` 一侧(`--z-*`)安全 |
| `check-01` tier-1 交替式 | 围栏内 `--radix-<family>-<step>` 名 | 加宽后重新匹配 | ✓ WIRED | 自跑变异:未加宽的空格写法 `var( --radix-gray-11 )` **不**匹配 → 见 W-2 |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `scripts/check-05-ui-uat.py` item3 `.hint color` | `muted = resolve_color(page, "--color-text-muted")` | 浏览器 `getComputedStyle` 探针(真实 chromium-1243 无头) | 是(`rgb(100, 100, 100)`,与 `documentElement` 的 `#646464` 一致) | ✓ FLOWING |
| `scripts/check-05-ui-uat.py` item4 z-index 三条 | `resolve_token(page, "--z-…")` | `getComputedStyle(document.documentElement).getPropertyValue` | 是(`200` / `10` / `20`) | ✓ FLOWING |
| `scripts/check-05-ui-uat.py` 颜色断言(未声明令牌分支) | `resolve_color(page, "--t")` | 探针 `color` → **父级继承值** | 否 —— 未声明时不反映任何令牌 | ✗ DISCONNECTED(CR-01) |
| `frontend/style.css` 围栏令牌 | 静态声明 | 手写 Radix hex | 是(25 tier-1 / 47 tier-2) | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| 四条守卫在真实树上全绿 | `bash scripts/check-01-token-conformance.sh` / `python3 scripts/check-02-contrast.py` / `bash scripts/check-03-hidden-uniqueness.sh` / `bash scripts/check-04-important-count.sh` | `PASS` / `PASS: 0 failures`(44 PASS 行)/ `PASS` / `PASS`,四个 exit 0 | ✓ PASS |
| 全量 UAT | `.venv/bin/python scripts/check-05-ui-uat.py` | 98 PASS / **0 FAIL** / 2 BLOCKED;item 1/2/3/4/6 PASS 0 BLOCKED,item 5 BLOCKED(9,0,2);`exit=2` | ✓ PASS(与 SUMMARY 逐项一致) |
| **B-1** check-05 能否在令牌改名后失败(CR-01) | 拦截 `/style.css` 注入删掉 `--color-text-muted` 声明的副本,再问 `.hint` 与 `resolve_color` 各算出什么 | `expected (resolve_color) = 'rgb(32, 32, 32)'` / `actual (.hint computed) = 'rgb(32, 32, 32)'` → `harness ok() would record: PASS`(渲染已坏:提示灰变成正文黑);仓库 `style.css` 未被触碰 | ✗ **FAIL**(守卫在改名下恒真) |
| **B-2** `wait_done("#btn-send")` 是否真的等待(CR-02) | 进入 p12 样本后读 `#btn-send` 状态并复现 `wait_done` 的谓词 | `{'disabled': False, 'hidden': False}`;首次轮询 `disabled = False` → 返回 `True`,耗时 **0.157s**(90s 截止在发送分支上是死代码) | ✗ **FAIL**(断言未等待 AI 调用) |
| **B-3** check-01 radix 分支 | `mktemp` 副本注入 `var(--radix-gray-11)` | `FAIL: 1 tier-1 primitive reference(s) outside the fence` / exit 1 | ✓ PASS |
| **B-4** check-01 空转对照 | 同一副本 + `sed 's/\|radix//'` 重建的旧守卫 | `PASS` / exit 0 —— 修复必要性被实证 | ✓ PASS |
| **B-5** check-01 裸 hex / 围栏成对 | 注入 `#abc`;删 END | `FAIL: 1 bare hex …` exit 1;`FAIL: expected exactly 1 fence START and 1 fence END, found 1/0` exit 1 | ✓ PASS |
| **B-6** check-02 四条硬失败路径 | 未知名 / 标记数 / 覆盖率下限 / ORDER 反转,四次 `mktemp` 副本 | 四条均 exit 1 且具名 | ✓ PASS |
| **B-7** 围栏外规则集不变 | `diff <(e530ead 的围栏外规则开集) <(HEAD 的)` | `IDENTICAL` | ✓ PASS |
| **B-8** Gate 2 双向 | 围栏外 `var()` 名集 vs 围栏内声明集,双向 `comm -23` | 两个方向均为空 | ✓ PASS |
| **B-9** 变更面 | `git diff --stat e530ead..HEAD -- frontend/app.js frontend/index.html frontend/vendor/` | 空;`ls frontend/vendor/` = `marked.min.js` | ✓ PASS |

**B-1 / B-2 是本报告结论的承重证据**,均为本验证会话自跑,非引用 SUMMARY 或 REVIEW。

### Probe Execution

Step 7c: SKIPPED —— 本阶段不是迁移/CLI/tooling 阶段,PLAN/SUMMARY/成功判据均未声明任何 `scripts/*/tests/probe-*.sh`,仓库内也无该约定目录。

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| TOKEN-01 | 01 | 单一 `:root` 令牌块、零构建零依赖 | ✓ SATISFIED | `^:root` == 1;无 package.json/build 变更 |
| TOKEN-02 | 01, 02 | 两层分类学;tier-1 名绝不出现在围栏外(机械可查) | ✓ SATISFIED(带残余缺口) | 围栏外 `var(--radix-…)` 被 CHECK-01 抓住(B-3);但**带空格的 `var( --radix-… )` 漏网**(W-2),不变量未 100% 机械覆盖 |
| TOKEN-04 | 01 | 令牌块之外零裸 `#hex` | ✓ SATISFIED | CHECK-01 `PASS`;`grep -o '#[0-9a-fA-F]\{3,6\}'` 在围栏外计数 0 |
| TOKEN-07 | 01, 03 | `--z-*` 令牌化**并断言序关系** | ⚠️ PARTIAL | 四个令牌已声明、四个消费者都在(`:537`/`:590`/`:606`/`:889`);三条 UAT 断言证明两端 computed 值。但**序关系本身没有任何机械断言** —— 只有 `:229-231` 的散文注释;`--z-overlay` 无运行时断言(W-6) |
| CHECK-01 | 01, 02 | 围栏外裸 hex 即失败 | ✓ SATISFIED | 见 B-3 / B-5 |
| CHECK-02 | 01, 02, 03 | 对所有声明的令牌配对算 WCAG 对比度 | ✓ SATISFIED | `PASS: 0 failures`;四条硬失败路径经 B-6 复证 |
| CHECK-03 | 01, 02, 03 | `.hidden` 唯一性守卫 == 1 | ✓ SATISFIED | 1 / `PASS` |
| CHECK-04 | 01, 02, 03 | `!important` 计数 == 1 | ✓ SATISFIED | 1 / `PASS` |
| A11Y-04 | 01, 03 | WCAG AA 文本对比度失败全部修复 | ✓ SATISFIED | check-02 43 对全 PASS,最低文本对 `--color-text-info on --color-surface-info` 4.53 ≥ 4.5;`.hint` 由 2.73 → 5.62 |
| A11Y-04b | 01, 03 | opacity 合成导致的失败一并覆盖 | ✓ SATISFIED(带残余缺口) | `.tier-desc` `opacity: 0.9` 删除(满不透明度 4.77 ✓);归档 0.75 压暗 6.97 ✓;冻结轮 `opacity: 1` + `saturate(0.6)` 保留且断言 PASS。**残余:** E16 mark 上的正文(`--color-text on --color-surface-mark`)不在清单里 —— 实测 15.0:1 通过,但未被 check-02 覆盖(W-4) |

**无 ORPHANED 需求。** ROADMAP §Phase 04.1 列出的 10 个 ID 全部被至少一份 PLAN 的 `requirements:` 字段认领(01: TOKEN-01/02/04/07, CHECK-02/03/04, A11Y-04/04b;02: CHECK-01, TOKEN-02, CHECK-03, CHECK-04;03: A11Y-04, A11Y-04b, TOKEN-07, CHECK-02/03/04)。ROADMAP 明确「不触碰 TOKEN-03/05/06/08」,与 3 份 PLAN 的认领一致。

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `scripts/check-05-ui-uat.py` | 250-262(定义)、600-685 / 727-728 / 777-778 / 803-826 / 983-984 / 1002-1005(消费) | **CR-01** `resolve_color` 对未声明令牌返回继承色 → 探针与消费者同值,断言恒真 | 🛑 BLOCKER | 本阶段自己引入的回归(22 条 `rgb()` 字面 → `resolve_color`)。约 25 条颜色断言在令牌改名/删除下记 PASS 而渲染已坏 —— 正是本项目记录的「守卫静默空转」失败类,也正是 plan 02 在同一阶段内刚修掉的那一类。独立复现:B-1 |
| `scripts/check-05-ui-uat.py` | 873-883(`wait_done`)、923-930(发送分支) | **CR-02** `wait_done("#btn-send")` 谓词是 `el.disabled === false`,而 `app.js` 只在归档态 disable `#btn-send`(L834),发送期间从不 disable | ⚠️ WARNING | `[p12] 交互冒烟「发送」` 在点击后约 0.16s 即记 PASS(B-2),`errors` 尚未收集到任何东西;90s 截止是死代码。**预先存在**(`6f52602`),本阶段未触碰 `run_ai_smoke`;默认运行下该行本就 BLOCKED,不影响 P3.7 |
| `scripts/check-01-token-conformance.sh` | 41-43 | **W-2(WR-01)** 交替式要求 `var(--` 无空格,CSS 允许 `var( --radix-gray-11 )` | ⚠️ WARNING | 自跑:`var( --radix-gray-11 )` → `PASS` / exit 0。TOKEN-02 的硬不变量仍有机械缺口 |
| `scripts/check-01-token-conformance.sh` | 17-27 | **W-3(WR-02)** 成对断言只数 START/END 的**数量**,不管位置 | ⚠️ WARNING | 自跑:把泄漏放在原 END 之前、再把 END 挪到 EOF → `PASS` / exit 0(`$outside` 退化为空)。注释声称覆盖「标记丢失」,实际只覆盖删除、不覆盖搬移 |
| `frontend/style.css` | 279-341(清单)、601 / 907(消费) | **W-4(WR-03)** 清单缺 `--color-text ON --color-surface-mark`;plan 01 的 E16 backstop 引用「CHECK-02: … = 15.88」 | ⚠️ WARNING | `grep -c 'PAIR --color-text ON --color-surface-mark'` = 0;15.88 实为 `on --color-surface-page` 的数,该引用在 check-02 输出里不存在;实测 text-on-mark = **15.0:1**(通过,但未被 check-02 覆盖)。清单自述的「枚举所有真实渲染的组合」因此不成立 |
| `scripts/check-05-ui-uat.py` | 996-997 | **W-5(WR-04)** `read_style(...) != "none"` 在元素缺席时返回 `None`,`None != "none"` 为真 | ⚠️ WARNING | `smoke #state-badge 可见` 在元素不存在时也记 PASS;同文件 item1 写法正确(L404-405),此处不一致 |
| `frontend/style.css` | 229-231 | **W-6** z-index 序关系只有散文注释,无机械断言 | ⚠️ WARNING | `grep -rn` 全部 `scripts/` 无任何比较 `--z-badge` 与 `--z-banner` 的断言;`--z-overlay` 无运行时断言。TOKEN-07 的「断言序关系」半场未被机械覆盖(消费者恢复这一半场已达成) |
| `scripts/check-05-ui-uat.py` | 477-480 | **IN-01** `goto_frozen_round(page, item)` 的 `item` 参数从未使用 | ℹ️ INFO | 死参数;两处调用都传了 |
| `scripts/check-05-ui-uat.py` | 845 vs 926 | **IN-02** 同一验收项在两个运行模式下标签不同(`[p3]` / `[p12]`) | ℹ️ INFO | grep 日志时两种模式会互相漏掉 |
| `scripts/check-05-ui-uat.py` | 842-847 / 1124-1127 | **IN-03** 默认运行必然 exit 2 | ℹ️ INFO | `code = 1 if any_fail else (2 if any_blocked else 0)`;任何以 `exit == 0` 为判据的 CI 门会永久红。文档已记明,但退出码不能当默认运行的通过信号 |

**债务标记门:** 三个改动源文件中 `TBD` / `FIXME` / `XXX` 计数均为 **0**。无未决债务标记。

### Human Verification Required

见 frontmatter `human_verification`。两条:

1. **28 条 UI-SPEC backstop 陈述**(plan 01 must_haves 的 `verification: backstop` 层)——7 条的比值半边已由 check-02 实测覆盖(E1 4.61–16.29 / E2 11.00 / E4 4.53 / E6 5.19–5.82 / E7 10.80 / E13 6.97 / E10 4.77),其余约 21 条是裁切/换行/滚动归属/200% 缩放/菜单重定位这类渲染几何行为,`grep` 与 computed-style 都看不见。plan 01 的 coverage D6 与 plan 02/03 的 Next-Phase-Readiness 均自标 `human_judgment: true`,本报告照录,不静默转绿。
2. **E16 的 `--color-text ON --color-surface-mark`** —— 该对不在清单里(所以 check-02 看不见),而计划引用的 `15.88` 是另一个配对的数。实测 15.0:1 通过,但需人工决定是否补进清单并修正引用。

### Gaps Summary

**值层本身是好的,而且我按计划自己的判据复证过它。** Radix 12 步刻度落地(25 tier-1 / 47 tier-2)、43 对清单与 check-02 的 `PASS: 0 failures` / `ORDER 0.363`、单一围栏、围栏外规则集与 `e530ead` 逐字节相同、Gate 2 双向为空、`app.js`/`index.html`/`vendor/` 零 diff —— 这些我都自己跑过,不是抄 SUMMARY。四条守卫全绿,plan 02 对 check-01 的加固我按它自己的方法(临时副本变异 + 旧守卫空转对照)独立复现过,成立。全量 UAT 我也复跑出 `0 FAIL` / `exit=2` / item5 恰两条交互冒烟,与 SUMMARY 逐项一致。

**唯一阻断项在守卫层,而且是本阶段自己引入的。**

`resolve_color()` 对**未声明**的令牌不做区分:它把 `color: var(--t)` 挂到探针元素上,而 CSS 在 computed-value 阶段让这条声明失效 → 探针继承父级颜色。真实消费者用的是同一个 `var(--t)`,于是**两侧同时退化成同一个继承值,断言恒真**。我在真实 chromium-1243 上拦截 `/style.css`、删掉 `--color-text-muted` 的声明后复现:`.hint` computed 与 `resolve_color` 都变成 `rgb(32, 32, 32)`,harness 记 **PASS** —— 而此时提示灰已经变成正文黑,渲染明显是坏的(证据 B-1)。

这为什么是阻断项而不是提醒:

- **它是本阶段引入的回归。** D-14 之前 `.hint color` 断言的是字面 `rgb(106,106,106)`,令牌被改名或删除时会响亮 FAIL。本阶段把 22 条这样的字面换成 `resolve_color` 调用(`git show e530ead:… | grep -c '"rgb('` = 22 → HEAD = 0),代价正是这个 FAIL 能力。计划与 SUMMARY 都只写了 D-14 的收益(移除假 FAIL)与「值由 check-02 仲裁」的补偿条款,**没有披露证伪能力的损失**。
- **它是本项目有明确记忆的失败类。** 计划 02 在同一阶段内刚修掉一个同类的空转守卫(`check-01` 的 tier-1 交替式),并且**专门要求**用变异证明修复不是修辞。本阶段用 D-14 在 `check-05` 里重新引入同类问题时,没有配任何变异证明。
- **它削弱的是本阶段的验收仪器。** `0 FAIL` 是本阶段的头条证据。在今天这棵树上,每条断言确实在做一次真实的两值相等比较(所有令牌都已声明),所以 `0 FAIL` 本身不是假的。但值层重写正是本阶段在做的事,也是 Phase 5/6/7 会继续做的事:未来任何一次令牌改名/删除都会让 check-05 继续打印 PASS,而 `check-02` 只兜住清单里出现过的名字(16 个被断言令牌中 12 个在清单里,`--color-action-irreversible` 不在)。

**修复面很小且有验证过的形态:** 让 `resolve_color` 在 `getComputedStyle(document.documentElement).getPropertyValue(t)` 为空时返回 `None`(`ok()` 对 `None` 记 BLOCKED,绝不记 PASS),再按 plan 02 的规格补一条「删掉 `--color-text-muted` 后该断言不再 PASS」的变异对照。`resolve_token` 已经是对的,可作为参照。

**其余为警告,不阻断:** CR-02(发送冒烟不等 AI 调用,预先存在、本阶段未触碰该函数)、W-2/W-3(`check-01` 两处残余缺口:带空格的 `var( … )`、标记搬移)、W-4(清单缺 `--color-text ON --color-surface-mark`,且计划引用了不存在的 15.88)、W-5(`smoke #state-badge 可见` 在元素缺席时记 PASS)、W-6(z-index 序关系只有散文,无机械断言)。

**人工项:** 28 条 backstop 陈述(约 21 条无自动化证据)+ E16 的比值归属。这是本阶段自己声明的 `human_judgment: true`,不是新发现。

**需求侧结论:** 10 个需求 ID 全部有认领、无孤儿。TOKEN-01/04、CHECK-01/02/03/04、A11Y-04 完全满足;TOKEN-02 与 A11Y-04b 有机械缺口(见上);TOKEN-07 的「令牌化 + 消费者恢复」满足,但「断言序关系」半场仍只有散文。

---

_Verified: 2026-09-19T14:41:02Z_
_Verifier: Claude (gsd-verifier)_
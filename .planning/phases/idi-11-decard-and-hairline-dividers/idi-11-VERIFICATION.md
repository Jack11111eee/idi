---
phase: idi-11-decard-and-hairline-dividers
verified: 2026-09-29T02:41:48Z
status: passed
score: 12/12 must-haves verified
covered_files:
  - .planning/REQUIREMENTS.md
  - .planning/ROADMAP.md
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-01-PLAN.md
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-01-SUMMARY.md
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-02-PLAN.md
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-02-SUMMARY.md
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-03-PLAN.md
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-03-SUMMARY.md
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-04-PLAN.md
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-04-SUMMARY.md
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-05-PLAN.md
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-05-SUMMARY.md
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-REVIEW.md
  - frontend/style.css
  - scripts/check-05-ui-uat.py
  - scripts/check-09-idi09-validation.py
covered_digest: "v1:sha256:9bdba54b0ca74f730d9810492aa04543a110eaa9bbc14793fe4c369a32f6d550"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: 11/12
  gaps_closed:
    - "DIV-02 / D-11-10 —— 窗口边缘发丝线(p3 / checking / archive 三态的可视首个面板带 border-top 且 rect.top == 0.00)"
  gaps_remaining: []
  regressions: []
  bookkeeping_reverification:
    round: 2
    trigger: "covered_digest 变 stale —— phase-completion 动词(97b428f)合法改写了 covered_files 中的 .planning/ROADMAP.md"
    previous_report_commit: "2a917ad"
    verified_head: "97b428f33800f6fa23cb4a3b7d2d839b5892ede7"
    previous_digest: "v1:sha256:e6988102bda07fab2893ad82c30b2500b66538d013d1f533e39e0550c4f2e206"
    current_digest: "v1:sha256:9bdba54b0ca74f730d9810492aa04543a110eaa9bbc14793fe4c369a32f6d550"
    commits_since_previous_report:
      - "97b428f docs(phase-11): complete phase execution"
    changed_files_total: 3
    changed_covered_files:
      - path: ".planning/ROADMAP.md"
        change: "bookkeeping only —— 阶段行 [ ]→[x] + 追加 (completed 2026-09-29);Progress 表行 In Progress → Complete | 2026-09-29。Goal / Success Criteria / Phase Details 三节零改动(全文件仅 2 个 hunk)"
    changed_uncovered_files:
      - path: ".planning/STATE.md"
        change: "bookkeeping only —— current_phase 11→12、status executing→planning、completed_phases 0→1、percent 100→50、velocity 表补 idi-11 行"
      - path: ".planning/state.json"
        change: "bookkeeping only —— phase 11 status in_progress→complete、next.reason、updated_at"
    claim_bearing_artifacts_byte_identical:
      - "frontend/style.css @ b6c492808757ad8be35fe23d4ab887d8c1e8d8d6"
      - "scripts/check-09-idi09-validation.py @ c8e82ecdf000f490791f0d80a36c05ffbce36785"
      - "scripts/check-05-ui-uat.py @ d6f8265b2b4c4774445a9df5c120207f35618a20"
      - ".planning/REQUIREMENTS.md @ 71387f44bac0cf2394342650ed48ad26e020d04f"
      - "idi-11-01..05 PLAN + SUMMARY + REVIEW @ 2a917ad==HEAD(11 份逐字节相同)"
      - "frontend/app.js @ 4ff062599ef157a09fdc7877df101b6988bb6ad3 / frontend/index.html @ 936ffb7e30376919e97e7125e0290558f6df7ae4"
    digest_delta_attribution: "以 FINGERPRINT_VERSION=1 算法(verification.cjs:266-273)独立复算:仅把 .planning/ROADMAP.md 换回 2a917ad 内容即精确复现记录的旧 digest e6988102… ⇒ 整个 digest 位移 100% 由 ROADMAP.md 的记账改动造成,无隐藏实质变更"
    checks_rerun:
      - "check-09 --item c1,c2,c3,c4,c5 → exit=0(c1 59 / c2 19 / c3 6 / c4 39 / c5 5,0 FAIL 0 BLOCKED)"
      - "check-01 / check-03 / check-04(bash)→ PASS rc=0"
      - "check-02(.venv python)→ PASS: 0 failures(53 PASS / ORDER 1)"
      - "check-05 --item 8 --browser bundled → PASS(13 条,0 FAIL,0 BLOCKED)exit=0"
      - "承重前提:#ai-panel 为 #main-pane DOM 末元素子(index.html:56-78,</main> 在 :79);frontend/app.js 无 ai-panel 隐藏路径(仅 :10-11 引用 header/body)"
      - "node --check frontend/app.js OK;git status --porcelain frontend/ 为空;frontend/vendor/ 仅 marked.min.js"
gaps: []
deferred: []
advisory: []
behavior_unverified_items: []
coincidental_reliance_items: []
---

# Phase 11: 去卡片化与发丝分隔线 Verification Report

**Phase Goal:** 把 v1.15 Phase 9 落地的卡片语言**整体反转** —— 左栏 4 个 section 与右栏 `#doc-panel` 不再绘制容器边界,面板底色与页面底色统一为同一档,12px 灰缝与 768px 居中侧沟归零;分区改由 1px 发丝线承担(主区↔文档区一条竖线跨满可视高度、左栏面板之间 1px 横线);界面读作一张连续的平面。
**Verified:** 2026-09-29T02:41:48Z
**Status:** passed
**Re-verification:** Yes — 第二轮:gap closure(plan `idi-11-05`)之后的 **post-completion-bookkeeping 复核**

## Post-Completion Bookkeeping Re-Verification(第二轮)

上一版报告提交于 `2a917ad`(`status: passed`,12/12)。此后 phase-completion 动词运行并**合法改写**了 `.planning/ROADMAP.md`(Phase 11 复选框置 `[x]`、追加 `(completed 2026-09-29)`、Progress 表行 `In Progress` → `Complete | 2026-09-29`)以及 `.planning/STATE.md` / `.planning/state.json`。`ROADMAP.md` 在 `covered_files` 内 ⇒ digest 位移,`verification.status` 报 `stale`。本轮**不复用旧结论**,在**当前 HEAD(`97b428f`)**上重立全部 12 条承重真值。

### (1) Delta 逐文件测量(不采信口头描述)

`git log 2a917ad..HEAD` 恰 **1 个提交**(`97b428f`);`git diff --name-status 2a917ad..HEAD` 恰 **3 个文件**:

| 文件 | 在 covered_files | 改动性质 |
| ---- | ---------------- | -------- |
| `.planning/ROADMAP.md` | 是 | **纯记账**:阶段行 `[ ]`→`[x]` + `(completed 2026-09-29)`;Progress 表行 `In Progress|`→`Complete    | 2026-09-29`。全文件仅 2 个 hunk,**Goal / Success Criteria / Phase Details 三节零改动** |
| `.planning/STATE.md` | 否 | 纯记账:`current_phase` 11→12、`status` executing→planning、`completed_phases` 0→1、`percent` 100→50、velocity 表补 `idi-11` 行 |
| `.planning/state.json` | 否 | 纯记账:phase 11 `in_progress`→`complete`、`next.reason`、`updated_at` |

三者**均不含任何 CSS、门脚本、需求或计划内容**。工作树对全部 covered_files 与 HEAD **逐字节干净**(`git status --untracked-files=no` 为空)。

### (2) 承重产物的哈希核对(逐字节)

`git rev-parse 2a917ad:<path>` vs `HEAD:<path>`:

```
SAME  frontend/style.css                     b6c492808757ad8be35fe23d4ab887d8c1e8d8d6
SAME  scripts/check-09-idi09-validation.py   c8e82ecdf000f490791f0d80a36c05ffbce36785
SAME  scripts/check-05-ui-uat.py             d6f8265b2b4c4774445a9df5c120207f35618a20
SAME  .planning/REQUIREMENTS.md              71387f44bac0cf2394342650ed48ad26e020d04f
SAME  frontend/app.js                        4ff062599ef157a09fdc7877df101b6988bb6ad3
SAME  frontend/index.html                    936ffb7e30376919e97e7125e0290558f6df7ae4
SAME  scripts/check-02-contrast.py           c3615209ce8acdc28c506069db9c8714029e7f01
SAME  idi-11-01..05 PLAN ×5 / SUMMARY ×5 / REVIEW(11 份逐字节相同)
```

**结论:无一条承重产物改动。** 12 条真值所依赖的 CSS 规则、门脚本、需求表、计划/摘要全部与已核验状态逐字节一致。

### (3) Digest 位移的归因证明

以 `verification.cjs:266-273` 的 `FINGERPRINT_VERSION=1` 算法(path 排序 → 逐文件 `sha256(bytes)` → `sha256("v1\n" + Σ"path\nhash\n")`)独立复算:

- 当前 HEAD 内容 → `v1:sha256:9bdba54b0ca74f730d9810492aa04543a110eaa9bbc14793fe4c369a32f6d550`(与 `gsd_run query verification.fingerprint` 输出逐字相同 ⇒ 复算忠实);
- **仅**把 `.planning/ROADMAP.md` 换回 `2a917ad` 内容、其余 15 份不动 → `v1:sha256:e6988102bda07fab2893ad82c30b2500b66538d013d1f533e39e0550c4f2e206`,**精确复现记录中的旧 digest**。

⇒ **整个 digest 位移 100% 由 `ROADMAP.md` 的记账改动造成**,不存在任何隐藏的实质变更。这就是「stale = 记账」的确定性证据,而非推断。

### (4) 在当前 HEAD 上重立 12/12(自跑读数,非采信旧报告)

| 检查 | 命令 | 读数 |
| ---- | ---- | ---- |
| `check-09` c1..c5 | `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4,c5` | **exit=0**;c1 59 / c2 19 / c3 6 / c4 39 / c5 5,**0 FAIL 0 BLOCKED** |
| 静态门 check-01 / 03 / 04 | `bash scripts/check-0{1,3,4}-*.sh` | 全部 **PASS** rc=0 |
| `check-02` 对比度 | `.venv/bin/python scripts/check-02-contrast.py` | **PASS: 0 failures**(53 PASS / ORDER 1) |
| `check-05 --item 8` | `.venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled` | **PASS(13 条,0 FAIL,0 BLOCKED)** exit=0 |
| 承重前提 | `grep frontend/index.html` / `grep frontend/app.js` | `#ai-panel` 为 `#main-pane` DOM 末**元素**子(:56-78,`</main>` 在 :79);`app.js` 全文仅 `#ai-panel-header` / `#ai-panel-body` 两处引用,**无 `#ai-panel` 自身隐藏路径**;`index.html:56` 无 `hidden` 属性 ⇒ 前提为真 |
| `style.css` 关键锚点 | 逐行读盘 | :764 `background: var(--color-surface-page)`;:792 `gap: 0`;:794 `align-items: center`;:827 `max-width: 768px`;:828 `background:…page` + `border: none` + `border-radius: 0`;:876 `#main-pane > section:not(:last-child){border-bottom:1px solid var(--color-border-subtle)}`;:899 `#doc-panel{border-left:1px solid var(--color-border-subtle)}`;:900 底;:938 表头底。`--color-surface-card` / `--shadow-card` 全文 **0** 次;`1-1-2` **0** 次 / `1-1-1` 5 次 |
| 前端卫生 | `node --check frontend/app.js` / `git status --porcelain frontend/` / `ls frontend/vendor/` | OK;空;仅 `marked.min.js` |

**12 条真值在当前 HEAD 上全部重新成立,且读数与上一版登记逐字一致(无漂移)。** 变异读数(M1 → c4 21 FAIL / M3 → c2 2 FAIL)未在本轮重跑:其判据载体 `scripts/check-09-idi09-validation.py` 与 `frontend/style.css` 均经哈希证明逐字节未变,故承前有效(见下 Truth 10 行)。

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | SURF-01 — 五个容器计算 `box-shadow == none`、四角 `== 0px`、除发丝线所在边外 `border-*-width == 0px` | ✓ VERIFIED | 自建 Playwright 探针(自带 chromium 153.0.8010.12,headless,1440×900)逐容器实测:四个 section + `#doc-panel` 全部 `bs=none r=0px`;`#doc-panel` 仅 `bl=1px`,其余三边 0。本轮重跑 `check-09 --item c1,c2` PASS(c1 59 / c2 19,0 FAIL 0 BLOCKED) |
| 2 | SURF-01 — 交互控件对照组在同一份读数里保留圆角与边界 | ✓ VERIFIED | c1 对照组 `button` / `#project-path-input` / `#check-switcher` / `#ai-route-select` / `.overlay-card` 全部 PASS(实测 `border-top-left-radius=10px`、`.overlay-card` `box-shadow != none`);本轮 c1 重跑 PASS |
| 3 | SURF-02 — 面板与页面底色统一为同一档白;`--color-surface`(gray-2)仍是唯一更暗的一档 | ✓ VERIFIED | 探针实测五个容器 `bg=rgb(255,255,255)` == body;本轮重跑 c3 PASS(内陷面 0.947307 < 统一面 1.000000);`check-02` 本轮重跑 PASS |
| 4 | SURF-03 — `#main-pane` 计算 `gap == 0px`;`align-items: center` / `max-width: 768px` 原地保留仍在工作 | ✓ VERIFIED | 探针实测 `#main-pane gap=0px`;本轮逐行读盘确认 style.css:792 `gap: 0`、:794 `align-items: center`、:827 `max-width: 768px` 逐字在盘 |
| 5 | DIV-01 — 主区↔文档区竖线 = `#doc-panel` 的 `border-left`,跨满面板可视高度 | ✓ VERIFIED | 探针实测 `#doc-panel` rect `top=0 bottom=900`(视口高 900),`border-left` 像素在 x=1008 为 `rgb(217,217,217)`、邻列白;本轮 c4 rect 断言重跑 PASS;:899 规则体逐字在盘 |
| 6 | DIV-02 — 左栏面板之间的横线由 `:not(:last-child)` 的下边线承担,恰 3 条(DOM 非末位) | ✓ VERIFIED | c4 三条前段 section 的 `border-bottom-width==1px` + 颜色双断言 PASS;`#ai-panel` 四边全 0px;本轮 c4 重跑 PASS;:876 规则体逐字在盘 |
| 7 | DIV-02 / D-11-10 — **可视的第一个**面板顶部不画线;5 个样本状态无一条线落在窗口边缘 | ✓ VERIFIED | **独立复现(非采信 SUMMARY)**:自建探针逐状态读 computed style —— p1/p12 首个可视 `#session-panel`、p3 `#annotations-panel`、checking/archive `#checks-panel`,五态均 `bt=0px`、`top=0.00`;像素级复核 y=0 内容列为白(p1/p12/p3/checking)/ 遮罩白 `rgb(140,140,140)`(archive),**无一处为线色**。恰一条可见发丝线落在两可视面板交界(767 / 120 / 395 / 330 行,`rgb(217,217,217)`)= 可见面板数 − 1。本轮 c4 五状态普查重跑逐态 PASS(`[checking]`/`[archive]` 原始读数:首个可视 `#checks-panel` `bt=0px`、`top=0.00`;可见线数 1 == 可见面板数 − 1;窗口边缘线 0 条) |
| 8 | DIV-03 — 两条线取既有语义令牌 `--color-border-subtle`(gray-6)、1px、零新增颜色值 | ✓ VERIFIED | c2/c4 双断言(令牌 + 字面量 `rgb(217,217,217)`)PASS;本轮 `check-01` 重跑 PASS(围栏外零裸 hex / 零 tier-1);:876/:899 规则体逐字在盘 |
| 9 | REG-01 — `check-09` 的 c1..c4 已改写为断言新契约,零条删除、零条降级为恒真 | ✓ VERIFIED | 实跑旧版(`315af14`)与 HEAD 并排:旧 c1 59 / c2 17 / c3 6 / c4 20 / c5 5;HEAD c1 59 / c2 19 / c3 6 / c4 39 / c5 5。**零项下降**;plan-05 diff 中 7 条被删断言行均为**就地换向**(上边线→下边线),计数逐项证实等价替换。本轮 HEAD 计数重跑逐项复现(59/19/6/39/5);`check-09` 脚本哈希与已核验态逐字节相同 |
| 10 | REG-01 — 以变异测试证明改写后的判据会真的失败 | ✓ VERIFIED | **上一轮独立复跑两条**:M1(规则还原为相邻兄弟 + `border-top`)→ `c4` **21 FAIL**, exit=1;M3(`#doc-panel` 底色改归 `--color-surface`)→ `c2` **2 FAIL**, exit=1。两次均 `git checkout -- frontend/style.css` 还原,`git diff --exit-code` rc=0 且 `git hash-object == b6c492808757ad8be35fe23d4ab887d8c1e8d8d6`。**本轮未重跑**:判据载体 `check-09-idi09-validation.py`(c8e82ecd…)与 `frontend/style.css`(b6c49280…)经哈希证明逐字节未变 ⇒ 变异读数承前有效 |
| 11 | REG-02 — `check-02` 两条卡片地面 PAIR 重新归属并重算;阈值与清单规模逐字不变 | ✓ VERIFIED | 本轮重跑 `check-02` → `PASS: 0 failures`;`PAIR 53 / ORDER 1`(与上一版逐数相同);`TEXT_MIN=4.5` / `NON_TEXT_MIN=3.0` 与 base 逐字相同;两条 PAIR 由 `--color-surface-card` 改记 `--color-surface-page`;`check-02-contrast.py` 零 diff(哈希 c3615209…) |
| 12 | REG-03 — `check-05 --item 8` 的 sticky 余量在 `#doc-panel` 边界改动后复测并登记 | ✓ VERIFIED | 本轮重跑 `.venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled` → `item 8: PASS (13 条,0 FAIL,0 BLOCKED)`,exit=0;容差字面量 `abs(...) <= 1.0` 与 base 逐字节相同(check-05 本阶段仅 plan 04 改 `.hint`,未触本项,哈希 d6f8265b… 与已核验态相同);余量 `1.000 → 0.000` 已登记 |

**Score:** 12/12 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
| -------- | -------- | ------ | ------- |
| `frontend/style.css` | 统一面换值 + 五容器去边界 + 灰缝归零 + 两条发丝线 + 规则换向 | ✓ VERIFIED | 逐条在盘:764(`html,body` 底)、828(`#main-pane > section`)、876(`:not(:last-child)` 下边线)、899(`#doc-panel` `border-left`)、900(底)、938(表头底);`--color-surface-card` / `--shadow-card` 全文出现 0 次;注释特异性数已更正为 `1-1-1`(全文无 `1-1-2`)。哈希 b6c49280… 与已核验态逐字节相同 |
| `scripts/check-09-idi09-validation.py` | c1..c4 换向 + c4 五状态普查 + c2 补 `#doc-panel` 底色断言 | ✓ VERIFIED | 本轮实跑 c1..c5 exit=0;`HAIRLINE_CENSUS_JS`、五状态循环、`#doc-panel` 底色双断言、对照组在盘;哈希 c8e82ecd… 与已核验态逐字节相同 |
| `scripts/check-05-ui-uat.py` | `.hint` 断言期望侧重登记(plan 04) | ✓ VERIFIED(有警告) | 本阶段唯一改动为 `.hint` 期望侧换指统一面令牌(747d5ff,21 行);sticky 断言未动;哈希 d6f8265b… 与已核验态逐字节相同。见 WR-01(范围外) |
| `.planning/…/gate-logs/idi-11-05/` | 17 份门原始输出与退出码 | ✓ VERIFIED | 目录实含 17 个 `.log`(14 门 + geometry-before/after + pytest),与 SUMMARY 一致 |

### Key Link Verification

| From | To | Via | Status | Details |
| ---- | -- | --- | ------ | ------- |
| `--color-surface-page` 声明值 | `html, body` / 四 section / `#doc-panel` / `#doc-panel-header` 的 background | `var()` 引用同一令牌 | ✓ WIRED | 本轮 c1/c2/c3 重跑 PASS;消费者 4 处 |
| `#doc-panel` 规则体 | `--color-border-subtle` | `border-left: 1px solid var(…)` | ✓ WIRED | c2/c4 双断言 + 像素实测 PASS;:899 在盘 |
| `#main-pane > section:not(:last-child)` | `--color-border-subtle` | `border-bottom: 1px solid var(…)` | ✓ WIRED | c4 双断言 + 五状态普查 + 自建探针 PASS;:876 在盘 |
| 横线规则的**机制前提** | `#ai-panel` 恒为 `#main-pane` DOM 末子元素且不被 `.hidden` 隐藏 | `frontend/index.html:56-79` + `frontend/app.js` 零 `#ai-panel` 隐藏路径 | ✓ WIRED | 本轮重新逐条在盘核实(index.html `#ai-panel` :56-78 / `</main>` :79;app.js 仅 :10-11 引用 header/body;全文无 `#ai-panel` classList 切换;:56 无 `hidden` 属性)⇒ 前提为真 |

### Data-Flow Trace (Level 4)

本阶段交付物为 CSS 绘制与门脚本,不渲染动态数据;Level 4 不适用。等价检查(令牌 → 消费者接线)由 Key Link 表覆盖:4 个 `--color-surface-page` 消费者与 2 条发丝线的令牌引用均由 check-09 的 computed-style 断言在真实浏览器中实测,并由自建探针独立复核。

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| -------- | ------- | ------ | ------ |
| 五状态发丝线普查(自建探针,非 check-09) | `.venv/bin/python /tmp/idi11_probe.py`(自带 chromium,1440×900) | 五态首个可视面板 `bt=0px` `top=0.00`;y=0 内容列白/遮罩白;恰一条线在两可视面板交界 | ✓ PASS |
| 窗口边缘像素取样 | 同上(PNG 手工解码) | p3/checking/p1/p12 y=0 = `(255,255,255)`;archive y=0 = `(140,140,140)`(= 遮罩白,非线色) | ✓ PASS |
| `check-09` c1..c5 | `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4,c5` | **本轮重跑** exit=0(c1 59 / c2 19 / c3 6 / c4 39 / c5 5,0 FAIL 0 BLOCKED) | ✓ PASS |
| 静态门 check-01/03/04 | `bash scripts/check-0{1,3,4}-…` | **本轮重跑** 全部 `PASS` rc=0 | ✓ PASS |
| check-02 对比度 | `.venv/bin/python scripts/check-02-contrast.py` | **本轮重跑** `PASS: 0 failures`(53 PASS / ORDER 1,含 4.77 / 3.32 / 3.15) | ✓ PASS |
| check-05 item 8 | `.venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled` | **本轮重跑** `PASS (13 条,0 FAIL,0 BLOCKED)` exit=0 | ✓ PASS |
| 变异 M1 | 规则还原为 `+ section { border-top }` → `check-09 --item c4` | 上一轮:`c4 FAIL (39 条,21 FAIL)` exit=1;还原后 hash 逐字节相同。本轮承前(载体哈希未变) | ✓ PASS(判据可失败) |
| 变异 M3 | `#doc-panel` 底色改 `--color-surface` → `check-09 --item c2` | 上一轮:`c2 FAIL (19 条,2 FAIL)` exit=1;还原后 hash 逐字节相同。本轮承前(载体哈希未变) | ✓ PASS(新断言可失败) |
| pytest 基线 | `.venv/bin/python -m pytest backend/tests -q --tb=short` | `219 passed, 6 skipped`(上一轮读数;本轮未重跑 —— 无后端/`app.js` 改动,`git status --porcelain frontend/` 空) | ✓ PASS |
| 前端卫生 | `node --check frontend/app.js` / `git status --porcelain frontend/` / `ls frontend/vendor/` | **本轮重跑** OK / 空 / 仅 `marked.min.js` | ✓ PASS |

### Probe Execution

本阶段未声明或约定 `scripts/*/tests/probe-*.sh` 形式的探针(项目探针为 `probe-05` / `probe-07`,非本阶段交付物);不适用。

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
| ----------- | ----------- | ----------- | ------ | -------- |
| SURF-01 | 01, 05 | 五容器不再绘制边界;交互控件保留 | ✓ SATISFIED | c1/c2 本轮 PASS + 自建探针;CSS 就地改写 |
| SURF-02 | 01, 05 | 面板与页面同色;内陷面仍更暗 | ✓ SATISFIED | c1/c2/c3 本轮 PASS + 探针;token:143 |
| SURF-03 | 01, 05 | 灰缝与侧沟归零 | ✓ SATISFIED | c4 gap PASS;保留声明在盘(本轮逐行复核) |
| DIV-01 | 01, 05 | 主区↔文档区 1px 竖线跨满高 | ✓ SATISFIED | c4 rect PASS + 像素实测 |
| DIV-02 | 01, 05 | 左栏面板间 1px 横线 | ✓ SATISFIED | c4 + 五状态普查 + 自建探针;窗口边缘线已消除 |
| DIV-03 | 01, 05 | 取既有语义令牌、1px | ✓ SATISFIED | 双断言 PASS;check-01 本轮 PASS |
| REG-01 | 03, 05 | c1..c4 改写为断言新契约 + 变异证明 | ✓ SATISFIED | 计数只增不减;M1/M3 各 FAIL(载体哈希未变,承前) |
| REG-02 | 02, 05 | check-02 地面重归属并重算 | ✓ SATISFIED | check-02 本轮 PASS;PAIR 53/ORDER 1 不变 |
| REG-03 | 04, 05 | check-05 item 8 余量复测登记 | ✓ SATISFIED | item 8 本轮 PASS;容差未回退;读数变化已登记 |
| REG-04 / G1-01 / VIS-01 | — | 归 Phase 12 | N/A(正确未声明) | 三个 PLAN 的 `requirements` 未含它们,与 ROADMAP 归属一致 |

**Orphaned requirements:** 无。REQUIREMENTS.md 映射 Phase 11 的 9 条 ID 全部出现在 PLAN frontmatter(01: SURF×3+DIV×3,02: REG-02,03: REG-01,04: REG-03,05: 全 9 条收口),无未声明的孤儿;`REG-04` / `G1-01` / `VIS-01` 按 ROADMAP 归 Phase 12。

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| ---- | ---- | ------- | -------- | ------ |
| — | — | 无 `TBD` / `FIXME` / `XXX` 债务标记(实扫 `frontend/style.css` + `check-09`,零命中) | — | 债务门通过 |
| `frontend/style.css` | 846 | 承重注释把失效条件写成「在其后插入新的 section」;实为「在其后追加**任何**元素子元素」 | ℹ️ Info | 注释精度,非代码缺陷(review 已登记);前提当前为真 |
| `scripts/check-09-idi09-validation.py` | 544-579 | 五状态普查未校验「该状态确实生效」(IN-03) | ℹ️ Info | **范围外**(用户已登记);自建探针已独立证明五态确实生效 |
| `scripts/check-05-ui-uat.py` | 1315-1317 | `.hint` 背景断言期望侧与 `<html>` 回退同值 ⇒ 判别力被抹(WR-01) | ℹ️ Info | **范围外**(用户裁定排除);本阶段已显式登记为承继债 |

### Human Verification Required

无。本阶段全部契约(五容器去边界、统一面、灰缝归零、两条发丝线的宽度/颜色/几何、窗口边缘无线的五状态普查)均由真实浏览器 `getComputedStyle` 计算读数 + 像素级取样覆盖,不存在仅凭 presence 无法判定的行为依赖真值。ROADMAP 的 `VIS-01`(5 张整窗截图的人眼取证)显式归 Phase 12,不在本阶段范围。

### Gaps Summary

**无缺口。** 上一轮的 1 个 BLOCKER(`DIV-02 / D-11-10` 窗口边缘发丝线)已由独立复现证明消除;本轮的 post-completion-bookkeeping 复核进一步证明 digest 位移纯属记账,12 条承重真值在当前 HEAD 上逐条重新成立。

**1. 上一轮失败的承重真值 —— 窗口边缘线:已消除(独立复现,不采信 SUMMARY)。**

自建 Playwright 探针(复用 check-05 的 `make_fixture` / `enter_project`,但读数与像素解码全为自写),使用 **Playwright 自带 chromium + headless + 1440×900**,逐状态读四个 section 的 computed `border-top-width` 与 `getBoundingClientRect().top`,并对整窗截图做 PNG 解码取像素:

```
state=p1       首个可视=#session-panel      bt=0px  top=0.00   y=0 内容列=(255,255,255)
state=p12      首个可视=#session-panel      bt=0px  top=0.00   y=0 内容列=(255,255,255)
state=p3       首个可视=#annotations-panel  bt=0px  top=0.00   y=0 内容列=(255,255,255)
state=checking 首个可视=#checks-panel       bt=0px  top=0.00   y=0 内容列=(255,255,255)
state=archive  首个可视=#checks-panel       bt=0px  top=0.00   y=0 内容列=(140,140,140)=遮罩白
```

每个状态恰有 **一条** 可见发丝线,落在两个可视面板的交界(p1/p12 y=767、p3 y=120、checking y=395、archive y=330,色 `rgb(217,217,217)`;archive 被遮罩压为 `rgb(119,119,119)`),即 **可见线数 == 可见面板数 − 1**。对照上一轮的读数(p3/checking/archive 首个可视面板 `bt=1px`、y=0 = `rgb(217,217,217)`),缺陷确已消除。`#doc-panel` 竖线在 x=1008 全程 `rgb(217,217,217)`、邻列白,跨满 0→900。本轮 c4 五状态普查重跑逐态复现该读数。

**2. 新规则的承重前提 —— 逐条在盘核实,前提为真(本轮重新核实)。**

`#main-pane > section:not(:last-child)` 等价于「除最后一个**可见** section 外」,当且仅当 `#ai-panel` 恒为 `#main-pane` 的 DOM 末**元素**子元素且不被隐藏。本轮核实结果:

- `frontend/index.html`:`#ai-panel` 于 :56 开始,`</main>` 于 :79,两者之间无任何元素 ⇒ 它是 `#main-pane` 的最后一个子元素;
- `frontend/app.js` 全文对 `#ai-panel` 的引用只有 `#ai-panel-header` / `#ai-panel-body`(:10-11);`.hidden` 只落在 `#session-panel`(:363 toggle)/ `#annotations-panel` / `#checks-panel`;全文无对 `#ai-panel` 自身的 `classList` 切换、无 `style.display='none'`、无向其父追加元素的路径;
- `frontend/index.html:56` 无 `hidden` 属性;`frontend/style.css` 中 `#ai-panel` 只出现在注释里,无规则体。

故规则**状态无关**地正确 —— 不只是在这 5 个 fixture 上。若日后给 `#ai-panel` 加隐藏切换或在 `#main-pane` 末尾追加元素,规则即失效(末位可视面板会多画一条下边线),该前提已显式登记在 `style.css:842-847` 与 `check-09` 的 c1/c4 注释中。

**3. 五容器契约与对照组同在一份读数里。** 探针实测五容器 `box-shadow=none`、四角 `0px`、底色全为 `rgb(255,255,255)` == body;`#doc-panel` 仅 `border-left:1px`。同一探针/同一门读数里,交互控件(`button` / 输入框 / 两个 `select` / `#check-switcher` / `.overlay-card`)保留各自圆角与边界 —— 「移除边界」未波及全站。

**4. REG-01 的判据改写确实零删除、零降级,且变异可失败。** 旧版与 HEAD 的断言计数并排:旧 59/17/6/20/5 → 新 59/19/6/39/5,零项下降;plan-05 diff 中 7 条被删断言行均为**就地换向**(上边线 → 下边线,`#ai-panel` 末位形态),计数逐项证实是等价替换而非删除。变异读数 M1 → c4 **21 FAIL** exit=1、M3 → c2 **2 FAIL** exit=1(上一轮独立复跑,还原后 `git hash-object == b6c492808757ad8be35fe23d4ab887d8c1e8d8d6` 逐字节相同,未用 `git stash`)。本轮未重跑变异,但判据载体(`check-09` c8e82ecd… / `style.css` b6c49280…)经哈希证明未变,且 HEAD 断言计数 59/19/6/39/5 逐项复现。

**5. 记录诚实性。** SUMMARY 披露三处偏差(子代理卡死 ×3 的收尾代写、`state.begin-phase` 把 `percent` 80→0 的覆写、复核发现 WR-04 特异性数字写错),与产物一致。跨阶段字节核对:仅 `frontend/style.css`、`scripts/check-05-ui-uat.py`、`scripts/check-09-idi09-validation.py` 三个非规划文件被改动;`frontend/app.js` / `frontend/index.html` / `scripts/check-02-contrast.py` / `backend/` 自阶段基址(`4e3afe4`)至 HEAD **逐字节相同**。

**6. 本轮新增的证据(记账复核)。** 见上方「Post-Completion Bookkeeping Re-Verification」四节:delta 逐文件测量、承重产物哈希核对、digest 位移归因证明、当前 HEAD 上的 12/12 重立读数。结论:digest 由 `e6988102…` 位移至 `9bdba54b…` 系 `ROADMAP.md` 的 phase-completion 记账所致,**无任何实质变更**,故本轮重写报告为 `status: passed` 并刷新 digest —— 这是**重新核验后**的结论,不是「刷新指纹」。

**范围外项(已登记,不构成缺口):** WR-01(`check-05` 的 `.hint` 恒真断言,用户裁定排除)、IN-01 / IN-02 / IN-03、G1-01 / REG-04 / VIS-01(归 Phase 12)、G2 / 999.2 / 暗色模式 / Nyquist 缺口 / 图标空态 / `.overlay-card` 地面 —— 均按用户裁定留在范围外。

---

_Verified: 2026-09-29T02:41:48Z_
_Verifier: Claude (gsd-verifier)_

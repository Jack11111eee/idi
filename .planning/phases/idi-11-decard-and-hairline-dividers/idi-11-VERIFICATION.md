---
phase: idi-11-decard-and-hairline-dividers
verified: 2026-09-29T02:30:18Z
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
covered_digest: "v1:sha256:e6988102bda07fab2893ad82c30b2500b66538d013d1f533e39e0550c4f2e206"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: 11/12
  gaps_closed:
    - "DIV-02 / D-11-10 —— 窗口边缘发丝线(p3 / checking / archive 三态的可视首个面板带 border-top 且 rect.top == 0.00)"
  gaps_remaining: []
  regressions: []
gaps: []
deferred: []
advisory: []
behavior_unverified_items: []
coincidental_reliance_items: []
---

# Phase 11: 去卡片化与发丝分隔线 Verification Report

**Phase Goal:** 把 v1.15 Phase 9 落地的卡片语言**整体反转** —— 左栏 4 个 section 与右栏 `#doc-panel` 不再绘制容器边界,面板底色与页面底色统一为同一档,12px 灰缝与 768px 居中侧沟归零;分区改由 1px 发丝线承担(主区↔文档区一条竖线跨满可视高度、左栏面板之间 1px 横线);界面读作一张连续的平面。
**Verified:** 2026-09-29T02:30:18Z
**Status:** passed
**Re-verification:** Yes — after gap closure (plan `idi-11-05`)

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | SURF-01 — 五个容器计算 `box-shadow == none`、四角 `== 0px`、除发丝线所在边外 `border-*-width == 0px` | ✓ VERIFIED | 自建 Playwright 探针(自带 chromium 153.0.8010.12,headless,1440×900)逐容器实测:四个 section + `#doc-panel` 全部 `bs=none r=0px`;`#doc-panel` 仅 `bl=1px`,其余三边 0。`check-09 --item c1,c2` 实跑 PASS(c1 59 / c2 19,0 FAIL 0 BLOCKED) |
| 2 | SURF-01 — 交互控件对照组在同一份读数里保留圆角与边界 | ✓ VERIFIED | c1 对照组 `button` / `#project-path-input` / `#check-switcher` / `#ai-route-select` / `.overlay-card` 全部 PASS(实测 `border-top-left-radius=10px`、`.overlay-card` `box-shadow != none`) |
| 3 | SURF-02 — 面板与页面底色统一为同一档白;`--color-surface`(gray-2)仍是唯一更暗的一档 | ✓ VERIFIED | 探针实测五个容器 `bg=rgb(255,255,255)` == body;c3 PASS(内陷面 0.947307 < 统一面 1.000000);`check-02` PASS |
| 4 | SURF-03 — `#main-pane` 计算 `gap == 0px`;`align-items: center` / `max-width: 768px` 原地保留仍在工作 | ✓ VERIFIED | 探针实测 `#main-pane gap=0px`;style.css:792 `gap: 0`、:794 `align-items: center`、:827 `max-width: 768px` 逐字在盘 |
| 5 | DIV-01 — 主区↔文档区竖线 = `#doc-panel` 的 `border-left`,跨满面板可视高度 | ✓ VERIFIED | 探针实测 `#doc-panel` rect `top=0 bottom=900`(视口高 900),`border-left` 像素在 x=1008 为 `rgb(217,217,217)`、邻列白;c4 rect 断言 PASS |
| 6 | DIV-02 — 左栏面板之间的横线由 `:not(:last-child)` 的下边线承担,恰 3 条(DOM 非末位) | ✓ VERIFIED | c4 三条前段 section 的 `border-bottom-width==1px` + 颜色双断言 PASS;`#ai-panel` 四边全 0px |
| 7 | DIV-02 / D-11-10 — **可视的第一个**面板顶部不画线;5 个样本状态无一条线落在窗口边缘 | ✓ VERIFIED | **独立复现(非采信 SUMMARY)**:自建探针逐状态读 computed style —— p1/p12 首个可视 `#session-panel`、p3 `#annotations-panel`、checking/archive `#checks-panel`,五态均 `bt=0px`、`top=0.00`;像素级复核 y=0 内容列为白(p1/p12/p3/checking)/ 遮罩白 `rgb(140,140,140)`(archive),**无一处为线色**。恰一条可见发丝线落在两可视面板交界(767 / 120 / 395 / 330 行,`rgb(217,217,217)`)= 可见面板数 − 1 |
| 8 | DIV-03 — 两条线取既有语义令牌 `--color-border-subtle`(gray-6)、1px、零新增颜色值 | ✓ VERIFIED | c2/c4 双断言(令牌 + 字面量 `rgb(217,217,217)`)PASS;`check-01` PASS(围栏外零裸 hex / 零 tier-1) |
| 9 | REG-01 — `check-09` 的 c1..c4 已改写为断言新契约,零条删除、零条降级为恒真 | ✓ VERIFIED | 实跑旧版(`315af14`)与 HEAD 并排:旧 c1 59 / c2 17 / c3 6 / c4 20 / c5 5;HEAD c1 59 / c2 19 / c3 6 / c4 39 / c5 5。**零项下降**;plan-05 diff 中 7 条被删断言行均为**就地换向**(上边线→下边线),计数逐项证实等价替换 |
| 10 | REG-01 — 以变异测试证明改写后的判据会真的失败 | ✓ VERIFIED | **本次独立复跑两条**:M1(规则还原为相邻兄弟 + `border-top`)→ `c4` **21 FAIL**, exit=1;M3(`#doc-panel` 底色改归 `--color-surface`)→ `c2` **2 FAIL**, exit=1。两次均 `git checkout -- frontend/style.css` 还原,`git diff --exit-code` rc=0 且 `git hash-object == b6c492808757ad8be35fe23d4ab887d8c1e8d8d6`(逐字节相同,未用 `git stash`) |
| 11 | REG-02 — `check-02` 两条卡片地面 PAIR 重新归属并重算;阈值与清单规模逐字不变 | ✓ VERIFIED | 实跑 `check-02` → `PASS: 0 failures`;`PAIR 53 / ORDER 1`(base 与 HEAD 逐数相同);`TEXT_MIN=4.5` / `NON_TEXT_MIN=3.0` 与 base 逐字相同;两条 PAIR 由 `--color-surface-card` 改记 `--color-surface-page`;`check-02-contrast.py` 零 diff |
| 12 | REG-03 — `check-05 --item 8` 的 sticky 余量在 `#doc-panel` 边界改动后复测并登记 | ✓ VERIFIED | 实跑 `.venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled` → `item 8: PASS (13 条,0 FAIL,0 BLOCKED)`,exit=0;容差字面量 `abs(...) <= 1.0` 与 base 逐字节相同(check-05 本阶段仅 plan 04 改 `.hint`,未触本项);余量 `1.000 → 0.000` 已登记 |

**Score:** 12/12 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
| -------- | -------- | ------ | ------- |
| `frontend/style.css` | 统一面换值 + 五容器去边界 + 灰缝归零 + 两条发丝线 + 规则换向 | ✓ VERIFIED | 逐条在盘:764(`html,body` 底)、828(`#main-pane > section`)、876(`:not(:last-child)` 下边线)、899(`#doc-panel` `border-left`)、900(底)、938(表头底);`--color-surface-card` / `--shadow-card` 全文出现 0 次;注释特异性数已更正为 `1-1-1`(全文无 `1-1-2`) |
| `scripts/check-09-idi09-validation.py` | c1..c4 换向 + c4 五状态普查 + c2 补 `#doc-panel` 底色断言 | ✓ VERIFIED | 实跑 c1..c5 exit=0;`HAIRLINE_CENSUS_JS`(:429)、五状态循环(:544)、`#doc-panel` 底色双断言、对照组(:156)在盘 |
| `scripts/check-05-ui-uat.py` | `.hint` 断言期望侧重登记(plan 04) | ✓ VERIFIED(有警告) | 本阶段唯一改动为 `.hint` 期望侧换指统一面令牌(747d5ff,21 行);sticky 断言未动。见 WR-01(范围外) |
| `.planning/…/gate-logs/idi-11-05/` | 17 份门原始输出与退出码 | ✓ VERIFIED | 目录实含 17 个 `.log`(14 门 + geometry-before/after + pytest),与 SUMMARY 一致 |

### Key Link Verification

| From | To | Via | Status | Details |
| ---- | -- | --- | ------ | ------- |
| `--color-surface-page` 声明值 | `html, body` / 四 section / `#doc-panel` / `#doc-panel-header` 的 background | `var()` 引用同一令牌 | ✓ WIRED | c1/c2/c3 实跑 PASS;消费者 4 处 |
| `#doc-panel` 规则体 | `--color-border-subtle` | `border-left: 1px solid var(…)` | ✓ WIRED | c2/c4 双断言 + 像素实测 PASS |
| `#main-pane > section:not(:last-child)` | `--color-border-subtle` | `border-bottom: 1px solid var(…)` | ✓ WIRED | c4 双断言 + 五状态普查 + 自建探针 PASS |
| 横线规则的**机制前提** | `#ai-panel` 恒为 `#main-pane` DOM 末子元素且不被 `.hidden` 隐藏 | `frontend/index.html:56-79` + `frontend/app.js` 零 `#ai-panel` 隐藏路径 | ✓ WIRED | 见下方「机制前提」段:逐条在盘核实,前提为真 |

### Data-Flow Trace (Level 4)

本阶段交付物为 CSS 绘制与门脚本,不渲染动态数据;Level 4 不适用。等价检查(令牌 → 消费者接线)由 Key Link 表覆盖:4 个 `--color-surface-page` 消费者与 2 条发丝线的令牌引用均由 check-09 的 computed-style 断言在真实浏览器中实测,并由本次自建探针独立复核。

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| -------- | ------- | ------ | ------ |
| 五状态发丝线普查(自建探针,非 check-09) | `.venv/bin/python /tmp/idi11_probe.py`(自带 chromium,1440×900) | 五态首个可视面板 `bt=0px` `top=0.00`;y=0 内容列白/遮罩白;恰一条线在两可视面板交界 | ✓ PASS |
| 窗口边缘像素取样 | 同上(PNG 手工解码) | p3/checking/p1/p12 y=0 = `(255,255,255)`;archive y=0 = `(140,140,140)`(= 遮罩白,非线色) | ✓ PASS |
| `check-09` c1..c5 | `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4,c5` | exit=0(c1 59 / c2 19 / c3 6 / c4 39 / c5 5,0 FAIL 0 BLOCKED) | ✓ PASS |
| 静态门 check-01/03/04 | `bash scripts/check-0{1,3,4}-…` | 全部 `PASS` rc=0 | ✓ PASS |
| check-02 对比度 | `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`(含 4.77 / 3.32 / 3.15) | ✓ PASS |
| check-05 item 8 | `.venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled` | `PASS (13 条,0 FAIL,0 BLOCKED)` exit=0 | ✓ PASS |
| 变异 M1 | 规则还原为 `+ section { border-top }` → `check-09 --item c4` | `c4 FAIL (39 条,21 FAIL)` exit=1;还原后 hash 逐字节相同 | ✓ PASS(判据可失败) |
| 变异 M3 | `#doc-panel` 底色改 `--color-surface` → `check-09 --item c2` | `c2 FAIL (19 条,2 FAIL)` exit=1;还原后 hash 逐字节相同 | ✓ PASS(新断言可失败) |
| pytest 基线 | `.venv/bin/python -m pytest backend/tests -q --tb=short` | `219 passed, 6 skipped` | ✓ PASS |

### Probe Execution

本阶段未声明或约定 `scripts/*/tests/probe-*.sh` 形式的探针(项目探针为 `probe-05` / `probe-07`,非本阶段交付物);不适用。

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
| ----------- | ----------- | ----------- | ------ | -------- |
| SURF-01 | 01, 05 | 五容器不再绘制边界;交互控件保留 | ✓ SATISFIED | c1/c2 PASS + 自建探针;CSS 就地改写 |
| SURF-02 | 01, 05 | 面板与页面同色;内陷面仍更暗 | ✓ SATISFIED | c1/c2/c3 PASS + 探针;token:143 |
| SURF-03 | 01, 05 | 灰缝与侧沟归零 | ✓ SATISFIED | c4 gap PASS;保留声明在盘 |
| DIV-01 | 01, 05 | 主区↔文档区 1px 竖线跨满高 | ✓ SATISFIED | c4 rect PASS + 像素实测 |
| DIV-02 | 01, 05 | 左栏面板间 1px 横线 | ✓ SATISFIED | c4 + 五状态普查 + 自建探针;窗口边缘线已消除 |
| DIV-03 | 01, 05 | 取既有语义令牌、1px | ✓ SATISFIED | 双断言 PASS;check-01 PASS |
| REG-01 | 03, 05 | c1..c4 改写为断言新契约 + 变异证明 | ✓ SATISFIED | 计数只增不减;独立复跑 M1/M3 各 FAIL |
| REG-02 | 02, 05 | check-02 地面重归属并重算 | ✓ SATISFIED | check-02 PASS;PAIR 53/ORDER 1 不变 |
| REG-03 | 04, 05 | check-05 item 8 余量复测登记 | ✓ SATISFIED | item 8 PASS;容差未回退;读数变化已登记 |
| REG-04 / G1-01 / VIS-01 | — | 归 Phase 12 | N/A(正确未声明) | 三个 PLAN 的 `requirements` 未含它们,与 ROADMAP 归属一致 |

**Orphaned requirements:** 无。REQUIREMENTS.md 映射 Phase 11 的 9 条 ID 全部出现在 PLAN frontmatter(01: SURF×3+DIV×3,02: REG-02,03: REG-01,04: REG-03,05: 全 9 条收口),无未声明的孤儿;`REG-04` / `G1-01` / `VIS-01` 按 ROADMAP 归 Phase 12。

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| ---- | ---- | ------- | -------- | ------ |
| — | — | 无 `TBD` / `FIXME` / `XXX` 债务标记(实扫 `frontend/style.css` + `check-09`,零命中) | — | 债务门通过 |
| `frontend/style.css` | 846 | 承重注释把失效条件写成「在其后插入新的 section」;实为「在其后追加**任何**元素子元素」 | ℹ️ Info | 注释精度,非代码缺陷(review 已登记);前提当前为真 |
| `scripts/check-09-idi09-validation.py` | 544-579 | 五状态普查未校验「该状态确实生效」(IN-03) | ℹ️ Info | **范围外**(用户已登记);本次自建探针已独立证明五态确实生效 |
| `scripts/check-05-ui-uat.py` | 1315-1317 | `.hint` 背景断言期望侧与 `<html>` 回退同值 ⇒ 判别力被抹(WR-01) | ℹ️ Info | **范围外**(用户裁定排除);本阶段已显式登记为承继债 |

### Human Verification Required

无。本阶段全部契约(五容器去边界、统一面、灰缝归零、两条发丝线的宽度/颜色/几何、窗口边缘无线的五状态普查)均由真实浏览器 `getComputedStyle` 计算读数 + 像素级取样覆盖,不存在仅凭 presence 无法判定的行为依赖真值。ROADMAP 的 `VIS-01`(5 张整窗截图的人眼取证)显式归 Phase 12,不在本阶段范围。

### Gaps Summary

**无缺口。上一轮的 1 个 BLOCKER(`DIV-02 / D-11-10` 窗口边缘发丝线)已由独立复现证明消除。**

**1. 上一轮失败的承重真值 —— 窗口边缘线:已消除(本次独立复现,不采信 SUMMARY)。**

我不接受 SUMMARY 的结论,自建 Playwright 探针(复用 check-05 的 `make_fixture` / `enter_project`,但读数与像素解码全为自写),使用 **Playwright 自带 chromium + headless + 1440×900**,逐状态读四个 section 的 computed `border-top-width` 与 `getBoundingClientRect().top`,并对整窗截图做 PNG 解码取像素:

```
state=p1       首个可视=#session-panel      bt=0px  top=0.00   y=0 内容列=(255,255,255)
state=p12      首个可视=#session-panel      bt=0px  top=0.00   y=0 内容列=(255,255,255)
state=p3       首个可视=#annotations-panel  bt=0px  top=0.00   y=0 内容列=(255,255,255)
state=checking 首个可视=#checks-panel       bt=0px  top=0.00   y=0 内容列=(255,255,255)
state=archive  首个可视=#checks-panel       bt=0px  top=0.00   y=0 内容列=(140,140,140)=遮罩白
```

每个状态恰有 **一条** 可见发丝线,落在两个可视面板的交界(p1/p12 y=767、p3 y=120、checking y=395、archive y=330,色 `rgb(217,217,217)`;archive 被遮罩压为 `rgb(119,119,119)`),即 **可见线数 == 可见面板数 − 1**。对照上一轮的读数(p3/checking/archive 首个可视面板 `bt=1px`、y=0 = `rgb(217,217,217)`),缺陷确已消除。`#doc-panel` 竖线在 x=1008 全程 `rgb(217,217,217)`、邻列白,跨满 0→900。

**2. 新规则的承重前提 —— 本次逐条在盘核实,前提为真。**

`#main-pane > section:not(:last-child)` 等价于「除最后一个**可见** section 外」,当且仅当 `#ai-panel` 恒为 `#main-pane` 的 DOM 末**元素**子元素且不被隐藏。核实结果:

- `frontend/index.html:56-79`:`#ai-panel` 是 `#main-pane` 的最后一个子元素,`</section>` 与 `</main>` 之间无任何元素;
- `frontend/app.js` 全文对 `#ai-panel` 的引用只有 `#ai-panel-header` / `#ai-panel-body`(第 10-11 行);`.hidden` 只落在 `#session-panel`(app.js:363 toggle)/ `#annotations-panel` / `#checks-panel`;全文无对 `#ai-panel` 自身的 `classList` 切换、无 `style.display='none'`、无向其父追加元素的路径;
- `frontend/style.css` 中 `#ai-panel` 只出现在注释里,无规则体;`index.html:56` 无 `hidden` 属性。

故规则**状态无关**地正确 —— 不只是在这 5 个 fixture 上。若日后给 `#ai-panel` 加隐藏切换或在 `#main-pane` 末尾追加元素,规则即失效(末位可视面板会多画一条下边线),该前提已显式登记在 `style.css:842-847` 与 `check-09` 的 c1/c4 注释中。

**3. 五容器契约与对照组同在一份读数里。** 探针实测五容器 `box-shadow=none`、四角 `0px`、底色全为 `rgb(255,255,255)` == body;`#doc-panel` 仅 `border-left:1px`。同一探针/同一门读数里,交互控件(`button` / 输入框 / 两个 `select` / `#check-switcher` / `.overlay-card`)保留各自圆角与边界 —— 「移除边界」未波及全站。

**4. REG-01 的判据改写确实零删除、零降级,且变异可失败。** 旧版与 HEAD 的断言计数并排:旧 59/17/6/20/5 → 新 59/19/6/39/5,零项下降;plan-05 diff 中 7 条被删断言行均为**就地换向**(上边线 → 下边线,`#ai-panel` 末位形态),计数逐项证实是等价替换而非删除。本次**独立复跑**两条变异:M1 → c4 **21 FAIL** exit=1(普查在 p3/checking/archive 上正确触发 (i)/(ii)/(iii) 三条判据),M3 → c2 **2 FAIL** exit=1;两次均 `git checkout -- frontend/style.css` 还原,`git diff --exit-code` rc=0 且 `git hash-object == b6c492808757ad8be35fe23d4ab887d8c1e8d8d6`(逐字节相同,未用 `git stash`)。这三条读数与 SUMMARY 登记逐字一致。

**5. 记录诚实性。** SUMMARY 披露三处偏差(子代理卡死 ×3 的收尾代写、`state.begin-phase` 把 `percent` 80→0 的覆写、复核发现 WR-04 特异性数字写错),与产物一致。跨阶段字节核对:仅 `frontend/style.css`、`scripts/check-05-ui-uat.py`、`scripts/check-09-idi09-validation.py` 三个非规划文件被改动;`frontend/app.js` / `frontend/index.html` / `scripts/check-02-contrast.py` / `backend/` 自阶段基址(`4e3afe4`)至 HEAD **逐字节相同**。

**一处需要指出的措辞不精确(非缺口):** 本次任务的说明把 `scripts/check-05-ui-uat.py` 列为「跨阶段逐字节未改」,但该文件实际被 **plan 04**(`747d5ff`)改动过(21 行,`.hint` 期望侧重新登记 —— 即范围外的 WR-01)。plan 05 **没有**改它,plan-05 SUMMARY 的「亦逐字节未改」在该语境下为真;但若读成「整个阶段未改」则不准确。属记录措辞,不影响任何承重真值。

**范围外项(已登记,不构成缺口):** WR-01(`check-05` 的 `.hint` 恒真断言,用户裁定排除)、IN-01 / IN-02 / IN-03、G1-01 / REG-04 / VIS-01(归 Phase 12)、G2 / 999.2 / 暗色模式 / Nyquist 缺口 / 图标空态 / `.overlay-card` 地面 —— 均按用户裁定留在范围外。

---

_Verified: 2026-09-29T02:30:18Z_
_Verifier: Claude (gsd-verifier)_

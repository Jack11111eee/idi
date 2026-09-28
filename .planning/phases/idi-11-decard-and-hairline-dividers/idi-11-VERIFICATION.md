---
phase: idi-11-decard-and-hairline-dividers
verified: 2026-09-28T16:40:00Z
status: gaps_found
score: 11/12 must-haves verified
covered_files:
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-01-PLAN.md
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-01-SUMMARY.md
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-02-PLAN.md
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-02-SUMMARY.md
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-03-PLAN.md
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-03-SUMMARY.md
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-04-PLAN.md
  - .planning/phases/idi-11-decard-and-hairline-dividers/idi-11-04-SUMMARY.md
  - frontend/style.css
  - scripts/check-05-ui-uat.py
  - scripts/check-09-idi09-validation.py
covered_digest: "v1:sha256:383cce0d173dd7da75e43c44a4215b2f353dfbd1732f0acd26809f91e7982ae5"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: none
  previous_score: 0/0
  gaps_closed: []
  gaps_remaining: []
  regressions: []
gaps:
  - truth: "DIV-02 / D-11-10 —— 左栏面板之间的横线只在面板之间,第一个(可视)面板顶部不画线(顶部是窗口边缘,画了会读成多一条);计划注释自述『两种显隐状态下都恰好 1 条可见分界』"
    status: failed
    reason: "`#main-pane > section + section { border-top: … }`(frontend/style.css:856)按 **DOM 相邻** 判定,`#session-panel` 是 DOM 第一个 section 故永不带线 —— 但 app.js:363 在非 phase1/phase12 状态给它加 `.hidden`(display:none)。在这些状态下可视的第一个面板是 `#annotations-panel`(p3)或 `#checks-panel`(checking/archive),而它们各自带 border-top ⇒ 一条 1px 发丝线被画在 y=0 的窗口边缘。独立复现(Playwright 自带 chromium + check-05 harness,1440×900):p3 `#annotations-panel` display=flex top=0.00 border-top=1px;checking / archive `#checks-panel` display=flex top=0.00 border-top=1px。像素级复核:p3 与 checking 在 y=0 的内容列像素为 rgb(217,217,217)(= gray-6 线色),p1 / p12 为 rgb(255,255,255)。即 5 个样本里 3 个 ships 一条设计明令禁止的窗口边缘线。style.css:833-835 的注释断言『两种显隐状态下都恰好 1 条可见分界』与实测矛盾。"
    artifacts:
      - path: "frontend/style.css"
        issue: "第 856 行的相邻兄弟选择器按 DOM 相邻判定,无法表达『第一个**可见** section』;第 833-835 行的注释断言与实测矛盾"
      - path: "scripts/check-09-idi09-validation.py"
        issue: "c4 的『第一个面板顶部不画线』判据(第 443-446 行)只在 p1 fixture 上运行 —— p1 下 `#session-panel` 恰是可视的第一个面板,该断言在唯一不可能出缺陷的状态里恒真;c4 在 p3/checking/archive 从不运行 ⇒ 对本缺陷结构性失明(实测:缺陷存在的当前树上 `check-09 --item c1,c2,c3,c4` 仍 exit=0、0 FAIL)"
    missing:
      - "让横线规则表达『第一个可见 section』:例如 app.js 在既有 `.hidden` toggle 旁同步加一个类(如 `is-first-visible`),规则键控于它;或改用『除最后一个可见 section 外都加下边线』。**不得**用 `section.hidden + section:not(.hidden) { border-top: none }` —— 那会同时抹掉 p3 下 `#checks-panel → #ai-panel` 的分隔线(checks 带 .hidden)"
      - "扩写 check-09 c4:把『第一个面板顶部不画线』的断言至少跑在一个 `#session-panel` 被隐藏的状态上(check-05 的 `checking` fixture 已存在),否则该回归对门不可观测"
      - "或(替代路线)重新裁定 D-11-10 并改正 style.css:833-835 的注释 —— 但不得让代码与已裁定的理由互相矛盾"
deferred: []
advisory: []
behavior_unverified_items: []
coincidental_reliance_items: []
---

# Phase 11: 去卡片化与发丝分隔线 Verification Report

**Phase Goal:** 去卡片化与发丝分隔线 — reverse v1.15 Phase 9's card language: the five containers (`#main-pane > section` ×4 + `#doc-panel`) stop drawing a boundary, page and panel ground unify to one step, the 12px gutter and centering gutters go to zero, and partitioning moves to 1px hairlines.
**Verified:** 2026-09-28T16:40:00Z
**Status:** gaps_found
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
| --- | --- | --- | --- |
| 1 | SURF-01 — 五个容器(`#session-panel` / `#annotations-panel` / `#checks-panel` / `#ai-panel` / `#doc-panel`)计算 `box-shadow == none`、四个物理角长手 `== 0px`、除发丝线所在边外 `border-*-width == 0px` | ✓ VERIFIED | `check-09 --item c1,c2` 实跑 PASS(c1 59 条 / c2 17 条,0 FAIL 0 BLOCKED);CSS 就地改写:`#main-pane > section`(style.css:819-826)`border:none;border-radius:0;box-shadow:none`、`#doc-panel`(:874-887)仅 `border-left` |
| 2 | SURF-01 — 交互控件对照组在同一份读数里保留圆角与边界(去卡片未波及全站) | ✓ VERIFIED | c1 对照组 `button` / `#project-path-input` / `#check-switcher` / `#ai-route-select` / `.overlay-card` 全部 PASS |
| 3 | SURF-02 — 面板与页面底色统一为同一档白;`--color-surface`(gray-2)仍是唯一更暗的一档 | ✓ VERIFIED | `--color-surface-page: var(--white)`(style.css:143);c1 四个 section 底色 `== body 底色 == rgb(255,255,255)`;c3 实跑 PASS(内陷面 0.947307 < 统一面 1.000000);`check-02` PASS |
| 4 | SURF-03 — `#main-pane` 计算 `gap == 0px`;`align-items: center` 与 `max-width: 768px` 原地保留仍在工作,侧沟由同色消除 | ✓ VERIFIED | c4 `gap == 0px` PASS;style.css:787 `gap: 0`、:789 `align-items: center`、:821 `max-width: 768px` 逐字在盘 |
| 5 | DIV-01 — 主区↔文档区竖线 = `#doc-panel` 的 `border-left`,零新增 DOM、跨满面板可视高度 | ✓ VERIFIED | c4 rect 断言 PASS(`#doc-panel` rect.top≈0、rect.bottom≈视口高、height≈视口高);style.css:879 |
| 6 | DIV-02 — 左栏面板之间的横线由 `#main-pane > section + section` 承担,恰 3 条(DOM 相邻) | ✓ VERIFIED | c4 三条 HAIRLINE_SECTIONS 的 border-top 宽度与颜色(令牌 + gray-6 字面量)双断言 PASS;style.css:856 |
| 7 | DIV-02 / D-11-10 — 第一个(**可视**)面板顶部不画线(顶部是窗口边缘);注释自述『两种显隐状态下都恰好 1 条可见分界』 | ✗ FAILED | 独立浏览器复现:p3 / checking / archive 下可视第一个面板(`#annotations-panel` / `#checks-panel`)带 border-top 且 top=0.00 ⇒ 窗口边缘线;像素级 y=0 = rgb(217,217,217)。见 Gaps Summary |
| 8 | DIV-03 — 两条线取既有语义令牌 `--color-border-subtle`(gray-6)、1px、零新增颜色值 / tier-1 primitive | ✓ VERIFIED | c2/c4 双断言(令牌 + 字面量 `rgb(217,217,217)`)PASS;`check-01` PASS(围栏外零裸 hex / 零 tier-1);`--color-border-subtle: var(--radix-gray-6)`(style.css:265) |
| 9 | REG-01 — `check-09` 的 c1..c4 已改写为断言新契约,零条删除、零条降级为恒真 | ✓ VERIFIED | 实跑 c1 59 / c2 17 / c3 6 / c4 20(HEAD 基线 26/13/3/4,断言数只增不减);判据为真实浏览器 `getComputedStyle` 读数;令牌解析断言改走 `ok_true` |
| 10 | REG-01 — 以变异测试证明改写后的判据会真的失败 | ✓ VERIFIED | SUMMARY 逐条登记 6 条变异(含 FAIL 原文与 hash 还原);**本次独立复跑变异 5**(`gap` 改回 `var(--space-3)`)→ `c4` FAIL(1 FAIL, exit=1);`git checkout -- frontend/style.css` 还原后 `git diff --exit-code` rc=0、hash 回到 `cfcaef098d957abc885413793cd8b1a9dc12193f`(逐字节相同,未用 git stash) |
| 11 | REG-02 — `check-02` 两条卡片地面 PAIR 按实际绘制面重新归属并重算;阈值与清单规模逐字不变 | ✓ VERIFIED | 实跑 `check-02` → `PASS: 0 failures`;style.css:686 `PAIR --color-marker-active ON --color-surface-page TEXT`、:700 `PAIR --color-border-strong ON --color-surface-page NON-TEXT`;PAIR 53 / ORDER 1;`scripts/check-02-contrast.py` 零 diff |
| 12 | REG-03 — `check-05 --item 8` 的 sticky 余量在 `#doc-panel` 边界改动后复测并登记,判据与产品代码未回退 | ✓ VERIFIED | 实跑 `.venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled` → `item 8: PASS (13 条断言,0 FAIL,0 BLOCKED)`,exit=0;容差字面量 `<= 1.0` 与 `#doc-panel` 上边框均未回退(余量 1.000→0.000 是事实变化,已登记) |

**Score:** 11/12 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
| -------- | -------- | ------ | ------- |
| `frontend/style.css` | 统一面换值 + 五容器去边界 + 灰缝归零 + 两条发丝线 | ✓ VERIFIED | 实盘逐条核对:143 / 787 / 819-826 / 856 / 874-887;`--color-surface-card` / `--shadow-card` 全文出现 0 次 |
| `scripts/check-09-idi09-validation.py` | c1..c4 改写为断言新契约 + `fence_text()` + 两条专用残留断言 | ✓ VERIFIED | 实跑 c1..c4 exit=0;`fence_text()`(:159)、两条 `RETIRED_CARD_TOKENS` 残留断言(:202-208)、交互控件对照组(:150-156)在盘 |
| `scripts/check-05-ui-uat.py` | `.hint` 断言期望侧重登记到统一面令牌 | ✓ VERIFIED(有警告) | `resolve_color(page, "--color-surface-page")`(:1316)在盘;断言形式仍是 `ok()` 精确等值。但见 WR-01 |
| `.planning/phases/idi-11-…/gate-logs/` | 13 份门原始输出与退出码 | ✓ VERIFIED | 目录实含 13 个 `.log`(check-01…07/09/10 + probe-05/07 + pytest + node-check),内容与本次复跑一致 |

### Key Link Verification

| From | To | Via | Status | Details |
| ---- | -- | --- | ------ | ------- |
| `--color-surface-page` 声明值 | `html, body` / 四个 section / `#doc-panel` / `#doc-panel-header` 的 background | `var()` 引用同一令牌 | ✓ WIRED | c1/c2/c3 实跑 PASS;消费者 4 处 |
| `#doc-panel` 规则体 | `--color-border-subtle` | `border-left: 1px solid var(…)` | ✓ WIRED | c2/c4 双断言 PASS |
| `#main-pane > section + section` | `--color-border-subtle` | `border-top: 1px solid var(…)` | ✓ WIRED | c4 双断言 PASS |
| 横线规则 / 其注释 | 渲染出的可见分界数 | 相邻选择器按 DOM 相邻判定 | ✗ BROKEN | 注释断言『两种显隐状态下都恰好 1 条可见分界』与实测矛盾(3/5 状态下为 2 条可见线) |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
| -------- | ------- | ------ | ------ |
| 四个 section 的 border-top 与 rect.top 逐状态实测 | 自建 Playwright 探针(自带 chromium,1440×900,复用 check-05 harness) | p3/checking/archive 可视首个面板 border-top=1px 且 top=0 | ✗ FAIL(见 Gap) |
| 窗口边缘像素取样 | 自建 PNG 解码探针 | p3/checking y=0 = rgb(217,217,217);p1/p12 = 白 | ✗ FAIL(见 Gap) |
| 静态门 check-01/03/04 | `bash scripts/check-0{1,3,4}…` | PASS(与 gate-logs 一致) | ✓ PASS |
| check-02 对比度 | `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures` | ✓ PASS |
| check-09 c1..c4 | `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4` | exit=0(c1 59 / c2 17 / c3 6 / c4 20) | ✓ PASS |
| check-05 item 8 | `.venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled` | PASS(13 条,0 FAIL,0 BLOCKED) | ✓ PASS |
| 变异 5(gap→12px) | 定向注入 + `check-09 --item c4` | c4 FAIL(1 FAIL, exit=1);还原后逐字节相同 | ✓ PASS |
| pytest 基线 | `.venv/bin/python -m pytest backend/tests -q --tb=short` | `219 passed, 6 skipped` | ✓ PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
| ----------- | ----------- | ----------- | ------ | -------- |
| SURF-01 | 01 | 五容器不再绘制边界;交互控件保留 | ✓ SATISFIED | c1/c2 PASS;CSS 就地改写 |
| SURF-02 | 01 | 面板与页面同色;内陷面仍更暗 | ✓ SATISFIED | c1/c3 PASS;token:143 |
| SURF-03 | 01 | 灰缝与侧沟归零 | ✓ SATISFIED | c4 gap PASS;保留声明在盘 |
| DIV-01 | 01 | 主区↔文档区 1px 竖线跨满高 | ✓ SATISFIED | c4 rect PASS |
| DIV-02 | 01 | 左栏面板间 1px 横线 | ✗ BLOCKED | 面板间线存在,但 3/5 状态在窗口边缘多画一条(见 Gap) |
| DIV-03 | 01 | 取既有语义令牌、1px | ✓ SATISFIED | 双断言 PASS;check-01 PASS |
| REG-01 | 03 | c1..c4 改写为断言新契约 + 变异证明 | ✓ SATISFIED(判据覆盖面有缺口) | 实跑 + 独立复跑变异;但 c4 对 DIV-02 的窗口边缘缺陷失明 |
| REG-02 | 02 | check-02 地面重归属并重算 | ✓ SATISFIED | check-02 PASS;两条 PAIR 在盘 |
| REG-03 | 04 | check-05 item 8 余量复测登记 | ✓ SATISFIED | item 8 PASS;判据未回退 |
| REG-04 / G1-01 / VIS-01 | — | 归 Phase 12 | N/A(正确未声明) | 三个 PLAN 的 `requirements` 未含它们,与 ROADMAP 归属一致 |

**Orphaned requirements:** 无。REQUIREMENTS.md 映射 Phase 11 的 9 条 ID 全部出现在 PLAN frontmatter(01: SURF×3+DIV×3,02: REG-02,03: REG-01,04: REG-03),无未声明的孤儿。

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
| ---- | ---- | ------- | -------- | ------ |
| `frontend/style.css` | 833-835 | 注释断言与实测矛盾(『两种显隐状态下都恰好 1 条可见分界』实为 2 条) | 🛑 Blocker | 已并入上方 Gap |
| `scripts/check-09-idi09-validation.py` | 443-446 | 判据仅在 p1 运行,在唯一不可能出缺陷的状态里恒真 | 🛑 Blocker | 已并入上方 Gap |
| `scripts/check-05-ui-uat.py` | 1315-1317 | `.hint` 背景断言的期望侧与 `effective_bg` 的 `<html>` 回退同值 ⇒ 对『面板被重新上色』失明(WR-01) | ⚠️ Warning | 计划明令要求的换指;形式仍是精确等值(合规),但判别力被抹掉 |
| `frontend/style.css` | 136-137 / 189-191 / 93 | 三处现在时陈述被本阶段自己的账目推翻(WR-02) | ⚠️ Warning | 围栏是权威令牌记录;`--color-surface-page` 现有 4 个消费者而非 1 个;marker-active 实测 4.77 而非 4.65;gray-9 白面 3.32 而非 3.24 |
| `scripts/check-09-idi09-validation.py` | 322 / 342-369 | c2 读了 `#doc-panel` 的 background 却从不断言(WR-03) | ⚠️ Warning | 五个容器里的第五个被重新上色时本门看不见(header 自带背景,c2 的 header 断言仍会过) |
| `scripts/check-09-idi09-validation.py` | 159-168 | `fence_text()` 未防护,围栏标记缺失时抛异常而非记 BLOCKED(IN-01) | ℹ️ Info | fail-loud 非 fail-green |
| `scripts/check-09-idi09-validation.py` | 711 | `argparse` description 仍写『Phase 9 卡片语言的运行时门』(IN-02) | ℹ️ Info | `--help` 文本过期 |

无 `TBD` / `FIXME` / `XXX` 债务标记(实扫 `frontend/style.css` + 两个门脚本,零命中)。

### Data-Flow Trace (Level 4)

本阶段交付物为 CSS 绘制与门脚本,不渲染动态数据;Level 4 不适用。等价检查(令牌 → 消费者接线)由 Key Link 表覆盖:4 个 `--color-surface-page` 消费者与 2 条发丝线的令牌引用均由 check-09 的 computed-style 断言在真实浏览器中实测。

### Human Verification Required

无(状态为 `gaps_found`,按判定树优先级)。注:ROADMAP 的 `VIS-01`(5 张整窗截图的人眼取证)显式归 Phase 12,不在本阶段范围。

### Gaps Summary

**一个 BLOCKER:`DIV-02 / D-11-10` 的窗口边缘发丝线(CR-01)—— 独立复现成立。**

我不接受 review 的结论,自行在真实浏览器里复现。使用 check-05 的 harness(`make_fixture` / `enter_project`)、Playwright **自带 chromium** + headless(不用 `channel="chrome"`,该组合在本机会挂死),1440×900,逐状态读四个 section 的 computed `border-top-width` 与 `getBoundingClientRect().top`:

```
state=p1        #main-pane.top=0  firstVisible=#session-panel
  #session-panel      display=flex   top=  0.00  border-top=0px
  #ai-panel           display=block  top=767.00  border-top=1px   (separator)
state=p3        #main-pane.top=0  firstVisible=#annotations-panel
  #session-panel      display=none   top=  0.00  border-top=0px
  #annotations-panel  display=flex   top=  0.00  border-top=1px   <== 窗口边缘线
  #ai-panel           display=block  top=121.00  border-top=1px   (separator)
state=checking  #main-pane.top=0  firstVisible=#checks-panel
  #checks-panel       display=flex   top=  0.00  border-top=1px   <== 窗口边缘线
  #ai-panel           display=block  top=395.91  border-top=1px   (separator)
state=archive   #main-pane.top=0  firstVisible=#checks-panel
  #checks-panel       display=flex   top=  0.00  border-top=1px   <== 窗口边缘线
  #ai-panel           display=block  top=331.16  border-top=1px   (separator)
```

像素级复核(自带 PNG 解码)进一步证明这条线**真的被画出来**:p3 与 checking 在 `y=0` 的内容列像素为 `rgb(217,217,217)`(= gray-6 线色),而 p1 / p12 同一位置为 `rgb(255,255,255)`。archive 有半透明遮罩,`y=0` 为 `rgb(119,119,119)`(白地 `rgb(140,140,140)` 被压暗后的线色)——线同样在。

**结论:claim 成立。** 5 个样本状态里 **3 个**(p3 / checking / archive)在窗口边缘多画一条设计明令禁止的线。成因是 `#main-pane > section + section` 按 **DOM** 相邻判定,而 `#session-panel`(DOM 首个)在非 phase1/phase12 状态被 `app.js:363` 加 `.hidden`;此时可视的第一个面板带着 border-top,落在 `#main-pane` 的 `top == 0`(窗口边缘,`#app` 是 `height:100vh` 的 flex 行,`#main-pane` 之上无任何 chrome)。style.css:833-835 的注释断言『两种显隐状态下都恰好 1 条可见分界』与实测**直接矛盾** —— 而本计划自己把『留下一条与代码矛盾的注释』列为反复付过代价的形态。

**是否击败 DIV-02 / D-11-10:** 击败 **D-11-10**(用户裁定的绑定决定,「第一个面板顶部不画,顶部是窗口边缘,画了会读成多一条」)与计划的承重注释;它**不**击败 DIV-02 的字面要求(面板之间的横线确实存在、确实取代了 12px 灰缝)。即:去卡片化的核心交付物成立,但发丝线的**契约**被违反 —— 这正是 ROADMAP 明令禁止的「门绿着在看」形态。

**`check-09` 的 c4 能否检测到它:不能,且是结构性的。** c4 的『第一个面板顶部不画线』判据(`scripts/check-09-idi09-validation.py:443-446`)断言 `#session-panel` 的 `border-top-width == 0px`,而 c4 只在 `make_fixture("p1", …)` 上运行。p1 下 `#session-panel` 恰是**可视的第一个面板**(我的探针实测 `firstVisible=#session-panel`)—— 该断言在唯一不可能出缺陷的状态里恒真,而在 p3 / checking / archive(缺陷唯一可能出现处)c4 **从不运行**。实测佐证:在缺陷存在的当前树上 `check-09 --item c1,c2,c3,c4` 仍 **exit=0、0 FAIL**。6 条变异也没有一条模拟「`#session-panel` 被隐藏」这一路径,故变异证明**不覆盖**这条契约。这使 REG-01 的『判据已改写为断言新契约』对本条契约只做到一半 —— 判据写下了,但抓不到违反它的回归。

**其余 11 条 must-have 全部 VERIFIED**(见上表):五容器去边界、统一面、灰缝归零、竖线跨满、三条横线、令牌纪律、c1..c4 改写、变异可失败(独立复跑变异 5 证实)、check-02 重归属、check-05 item 8 复测。`app.js` / `index.html` / 后端逐字节未改(与计划预期一致);静态门、check-02、check-09、check-05 item 8、pytest(219/6)全部与 SUMMARY 一致。

---

_Verified: 2026-09-28T16:40:00Z_
_Verifier: Claude (gsd-verifier)_

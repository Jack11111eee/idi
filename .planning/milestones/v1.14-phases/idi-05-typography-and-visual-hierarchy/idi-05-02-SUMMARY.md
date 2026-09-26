---
phase: idi-05-typography-and-visual-hierarchy
plan: 02
subsystem: ui
tags: [css, design-tokens, action-ramp, irreversible-action, contrast, playwright, uat, visual-hierarchy, core-value]

# Dependency graph
requires:
  - phase: idi-05-typography-and-visual-hierarchy
    provides: "plan idi-05-01:7 档字号刻度(28 / 22 / 18px)、四宿主可达的 `.markdown-body` 标题、五只按钮 500 / `#btn-authorize` 600 的字重分工、check-05 item4 的四宿主探针与六条字重断言"
  - phase: idi-04.1-radix
    provides: "围栏 tier-1 Radix primitive 与 tier-2 语义令牌;check-02 的 `/* PAIR */` 清单机制与「不采信上游 AA 论断」的方法论"
provides:
  - "三段坡道落地:`--color-action-commit-*` 改为实心(green-11 底 / 白字),`--color-action-irreversible-*` 改为更深实心(green-12 底 / 白字),routine 族逐字节不变"
  - "`#btn-authorize` 的第四个强调通道:字号步进 14 → 16px(`--text-md`,零新增令牌,D-13),padding 零步进"
  - "check-02 配对清单 43 → 45 对(+2 条白字对实心填充的 NON-TEXT 配对:commit 4.48 / irreversible 11.70)"
  - "D-04 断言反转:原「routine 与 irreversible 三属性逐字节相同」改为「档内相同 ×2 + 三档两两不同 ×1」,一个断言同时覆盖 VISUAL-01 与 VISUAL-02"
  - "VISUAL-03 复证 + 页面级层级链运行时断言:文档 h1 28 > `.overlay-card h3` 24 > 文档 h2 22 > `#doc-panel-header h1` 14"
  - "check-05 item4 的断言数 45 → 49;item3 由 14 → 17"
affects: [idi-05-03, idi-06, idi-07]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
# Same estimateTokens scale (chars/4 over the realized diff), never a harness token count.
actuals:
  tokens: 3234      # chars/4 over the realized diff of the two code files (12934 chars)
  tasks: 3
  commits: 3        # MEASURED: git rev-list --count 5bd9ba8..HEAD (3 task commits); plan_head_before = 5bd9ba8
  plan_head_before: 5bd9ba8

# Tech tracking
tech-stack:
  added: []        # 零新增依赖、零新增文件、零构建步骤(硬规则 6)
  patterns:
    - "「形态差异是第一区分手段」:三段坡道靠淡底 vs 实心 vs 实心更深分离,不依赖色深对比 —— 色深只是第二手段"
    - "断言反转而非现实反转:阶段目标是让旧断言必然 FAIL 时,反转的是断言(并说明为什么),不是把现实改回去"
    - "档内相同 + 档间不同成对出现:前者抓「改错了一只」,后者守卫核心价值红线;单有其一都不足以定位失败"
    - "字号层级链用整数比较而非字符串比较(避免 \"14px\" < \"9px\" 的序陷阱)"

key-files:
  created: []
  modified:
    - frontend/style.css
    - scripts/check-05-ui-uat.py

key-decisions:
  - "D-11 三段坡道的取值:commit 用 green-11 实心、irreversible 用 green-12 实心 —— 两者都是「白字在其上通过 AA 的最浅/更深步」,由 check-02 实算仲裁而非采信 Radix 的 band 论断"
  - "D-13 `#btn-authorize` 字号步进 14 → 16px,零新增令牌;不加 padding 步进(算术:标签 16px 下约 144px + padding-x 32px ≈ 176px < 最窄内容宽 260px,不换行)"
  - "D-12 `#btn-authorize` 保持 600 —— D-09「按钮统一 500」的唯一已登记例外,四个强调通道(形态 / 色深 / 字号 / 字重)此处用满"
  - "D-15 `--color-action-irreversible*` 仍恰有一个消费者 `#btn-authorize`:本计划改的是它的**值**,不是它的**消费者集合** —— 两件事分别核对"
  - "D-19 VISUAL-03 零 CSS 改动,只做复证;门的选择器名由契约文本的 `#doc-pane > h1` 更正为 HEAD 实况 `#doc-panel-header h1`,并断言 `#doc-pane` 不存在"

patterns-established:
  - "斜坡类交付物的门必须成对断言:档内相同 + 档间不同 —— 只断言档间不同会漏掉「某一档内部不一致」"
  - "契约漂移的机械登记:契约文本引用的选择器在 HEAD 上不存在时,断言其不存在,而不是新建元素让契约成立"

requirements-completed: [VISUAL-01, VISUAL-02, VISUAL-03]

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "三段坡道在**形态**上分离:`#btn-authorize` 实心更深 + 白字 + 16px + 600;commit 两只实心 + 白字;routine 三只淡底绿字逐字节不变。三档两两不同且档内各自相同"
    requirement: "VISUAL-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 3"
        status: pass
      - kind: unit
        ref: ".venv/bin/python scripts/check-02-contrast.py"
        status: pass
    human_judgment: false
  - id: D2
    description: "commit 两只(`#btn-approve-draft` / `#btn-start-writing`)实心填充 + 白字,与 routine 三只形态不同、与 irreversible 深浅不同"
    requirement: "VISUAL-02"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 3"
        status: pass
    human_judgment: false
  - id: D3
    description: "VISUAL-03 复证成立且零 CSS 改动:`#doc-panel-header h1` 为 14px / 500;页面级层级链 文档 h1 28 > `.overlay-card h3` 24 > 文档 h2 22 > `#doc-panel-header h1` 14"
    requirement: "VISUAL-03"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 4"
        status: pass
      - kind: other
        ref: "git diff --stat -- frontend/style.css → 空(Task 3 零 CSS 改动)"
        status: pass
    human_judgment: true
    rationale: "字号半边由运行时断言钉死;剩余的「视觉层级是否真的立住」是人的判断,已作为 E8 的 backstop 陈述记录,不自动判过"

duration: ~35min
completed: 2026-09-21
status: complete
---

# Phase 5: 排版与视觉层级 — Plan 02 Summary

**不可逆的 G3 授权在**形态**上与五只例行/承诺按钮分离(淡底 vs 实心 vs 实心更深),页面级层级链 28 > 24 > 22 > 14 由运行时断言钉死。**

## Performance
- **Duration:** ~35min(跨两次子代理失败:一次静默交付失败,一次 API 503)
- **Tasks:** 3/3
- **Files modified:** 2

## Accomplishments
- **三段坡道落地。** `--color-action-commit-*` 由淡底改为实心(green-11 底 / 白字),`--color-action-irreversible-*` 改为更深实心(green-12 底 / 白字),routine 族逐字节不变。形态是第一区分手段,色深是第二 —— 授权按钮在**不依赖色深对比**的前提下就与例行按钮不同。
- **`#btn-authorize` 用满四个强调通道**:实心更深 / 白字 / 字号步进 16px(D-13)/ 字重 600(D-12 唯一例外)。
- **D-04 断言反转。** 原「`#btn-process-round` 与 `#btn-authorize` 三属性逐字节相同」在本阶段之后必然 FAIL —— 那正是本阶段要做的事。反转成「档内相同 ×2 + 三档两两不同 ×1」,一个断言同时覆盖 VISUAL-01 与 VISUAL-02。档内相同那一半同样承重:它能抓到「改错了一只」。
- **check-02 配对 43 → 45。** 新增两条白字对实心填充的 NON-TEXT 配对(commit 4.48 / irreversible 11.70 on `--color-surface`),由脚本实算仲裁。
- **VISUAL-03 复证 + 页面级层级链。** 零 CSS 改动;门的选择器名由契约文本的 `#doc-pane > h1` 更正为 HEAD 实况 `#doc-panel-header h1`,并断言 `#doc-pane` 不存在 —— 把 D-01 的契约漂移登记成机械可核的事实。

## Task Commits
1. **Task 1 (tracer): 三段坡道端到端** - `49b1364`
2. **Task 2: D-04 断言反转 + `#btn-authorize` 字号步进与字重例外** - `05c29b6`
3. **Task 3: VISUAL-03 复证 + 页面级层级链(SC3)** - `0071a22`

> Task 2 与 Task 3 的提交由 orchestrator 代写:执行 Task 2 的子代理在**第 4 步(实跑验证)之前**死于一次 API 503,Task 3 因连续两次子代理失败(一次静默交付失败、一次 503)由 orchestrator 内联执行。两个任务的**编辑内容**均由子代理/内联完成,所有 `<verify>` 命令由 orchestrator 独立复跑,原始输出见下。

## Files Created/Modified
- `frontend/style.css` — 围栏内五个令牌值改动(commit 族改实心、irreversible 族改更深实心)+ `#btn-authorize` 新增一条 `font-size: var(--text-md)`;围栏头注释的 9/10 fill-step 预告与「三族一值」注记改写。**围栏外消费者规则零改动**。
- `scripts/check-05-ui-uat.py` — item3 新增 `trio()` 读取器与 `ROUTINE` / `COMMIT` / `IRREVERSIBLE` 常量、三条坡道断言替换原逐字节相同断言;item4 新增 `#btn-authorize` 字号断言、两条 `#doc-panel-header h1` 字面断言、`#doc-pane` 不存在断言、页面级层级链断言。

## Decisions & Deviations

**决策(均已登记在 05-CONTEXT.md):** D-11 三段坡道取值由 check-02 实算仲裁;D-12 授权按钮字重保持 600;D-13 字号步进 16px 且不加 padding 步进;D-15 `--color-action-irreversible*` 仍单消费者;D-19 VISUAL-03 只复证。

**偏差一(流程):** 执行 Task 2 的子代理在编辑完成后、实跑验证前死于 API 503(`503 No available providers`)。工作树中的编辑完整且正确,orchestrator 独立复跑了该任务的全部 `<verify>` 命令后代为提交。**没有重跑该任务** —— 依据是先核提交与门禁再决定是否重跑。

**偏差二(流程):** Task 3 由 orchestrator 内联执行而非派发子代理 —— 连续两次子代理失败后选择风险更低的内联路径。任务的编辑、验证、提交均按计划原文执行。

**偏差三(登记):** 计划 02 的 `<read_first>` 与 `<action>` 中的行号全部是**规划期 HEAD** 的引用,而 wave 1 已修改过本计划触碰的两个文件。所有编辑目标按内容定位、按 D-01 以磁盘 HEAD 为准;未发现计划文本与磁盘的实质冲突。

**未改动的三件事(有意为之):** `frontend/app.js` / `index.html` / `vendor/` 零 diff;`REQUIREMENTS.md` 与 `ROADMAP.md` 零 diff(改它们会作废已通过的验证指纹);`.collapse-indicator` 未触碰。

## Verification (orchestrator 独立复跑)

```
CHECK-01  PASS
CHECK-02  PASS: 0 failures · 45 pairs(+2 相对 wave 1)· ORDER 0.363 不变
item 3    PASS  (17 条断言,0 FAIL,0 BLOCKED)
item 4    PASS  (49 条断言,0 FAIL,0 BLOCKED)
item smoke PASS (6 条断言,0 FAIL,0 BLOCKED)

三档读数(p3):routine=(rgb(25,59,45), green-11, green-3)
              commit=(white, green-11, green-11)
              irreversible=(white, green-12, green-12)
层级链:文档 h1=28px > .overlay-card h3=24px > 文档 h2=22px > #doc-panel-header h1=14px
--text-md 消费者 6 → 7(与 UI-SPEC:200 的「7 处 → 7 处,净不变」一致)
--color-action-irreversible* 围栏外消费者:恰 3 行,全在 #btn-authorize 规则体内(D-15)
frontend/ porcelain 空;REQUIREMENTS.md / ROADMAP.md 零 diff
```

## Next Phase Readiness
- **Wave 3(`idi-05-03`)可开始**:它依赖 `[idi-05-01, idi-05-02]`,两者均已完成并有 SUMMARY。它触碰 `frontend/style.css`(标记体系 / SVG mask)与 `scripts/check-05-ui-uat.py`,**且其计划同样写于 wave 1 之前** —— 行号需按内容重新定位。
- **已知的连带义务**:本计划两次改动 `frontend/style.css`,与 wave 1 合并为同一批,`idi-04.1-radix` 的 `passed` 指纹仍作废,**须在阶段收口时一次性连带复验**(D-05)。
- **未完成的验证动作**:无。本计划的三条需求 VISUAL-01 / VISUAL-02 / VISUAL-03 均已有运行时证据。
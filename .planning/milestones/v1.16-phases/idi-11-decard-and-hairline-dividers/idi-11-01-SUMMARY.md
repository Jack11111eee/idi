---
phase: idi-11-decard-and-hairline-dividers
plan: 01
subsystem: ui
tags: [css, design-tokens, computed-style, playwright, decard, hairline]

requires:
  - phase: idi-09-card-containers
    provides: 被本计划反转的卡片语言(D-9-1 / D-9-2 / D-9-3)与其运行时门 check-09 c1..c5
  - phase: idi-10-tables-and-radius-scale
    provides: 「就地改写 + 追加不重排」纪律与专用残留断言的先例
provides:
  - 统一面(--color-surface-page 就地换值为白)—— 页面与四个面板同色
  - 五个容器去边界(4 个 #main-pane > section + #doc-panel)
  - #main-pane 灰缝归零 + .panel-header 圆角归零
  - 两条发丝线(竖线 = #doc-panel 的 border-left;横线 = #main-pane > section + section 的 border-top)
  - 三份真实浏览器运行时读数的原始 INFO 行(供计划 03 的判据改写与计划 04 的复跑消费)
affects: [idi-11-02, idi-11-03, idi-11-04, idi-12]

actuals:
  tokens: 3859
  tasks: 3
  commits: 3
plan_head_before: 6afe6793320046119b15bffa156ce1876e20853b

tech-stack:
  added: []
  patterns:
    - "就地改写既有声明体,绝不追加覆盖规则(Phase 9 / Phase 10 同一纪律)"
    - "发丝线走盒内手段(border-*),零新增 DOM 元素、零位移"
    - "承重注释与代码同一次提交改写 —— 留下与代码矛盾的注释是本仓库反复付过代价的形态"

key-files:
  created: []
  modified:
    - frontend/style.css

key-decisions:
  - "统一面就地换值 var(--radix-gray-3) -> var(--white):声明名与位置不动,三档 elevation 叙事改写为两级(统一面白 1.000000 > 内陷面 gray-2 0.947307)"
  - "五个容器的四条旧声明是被改写掉的(border -> none / border-radius -> 0 / box-shadow -> none / background 改指统一面),不是被后续规则覆盖 —— 规则体内已不再出现 --color-surface-card / --color-border / --radius-md / --shadow-card"
  - "竖线取 #doc-panel 的 border-left 而非新增 DOM / margin:盒内手段零位移,天然跨满 #app 的 stretch 高度"
  - "横线只 3 条:#session-panel 是 DOM 第一个 section,相邻兄弟选择器永不匹配它 ⇒ 第一个面板顶部不画线"
  - "两条线不登记 NON-TEXT 对比度对:装饰性分隔不标识控件/状态 ⇒ SC 1.4.11 不适用;依据逐字引用本文件既有两处登记,不是本阶段的新判据"
  - "width / max-width / align-items: center 是保留的声明,不是死代码 —— 侧沟由色统一消除,不是由删声明消除(D-11-5)"

patterns-established:
  - "发丝线颜色必须双断言:计算色 == 运行时令牌 == 写死字面量(gray-6),否则换令牌会两侧一起变、恒过"

requirements-completed: [SURF-01, SURF-02, SURF-03, DIV-01, DIV-02, DIV-03]

coverage:
  - id: D1
    description: "五个容器(4 个 #main-pane > section + #doc-panel)在真实浏览器里不再绘制边界:box-shadow=none、四个物理角长手=0px、除发丝线所在边外 border-*-width=0px"
    requirement: "SURF-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c1 (INFO 原始读数行)"
        status: pass
    human_judgment: true
    rationale: "本计划结束时断言该契约的门尚未存在 —— check-09 的 c1..c4 断言的仍是 Phase 9 卡片语言(必 FAIL,是门在正确工作的证据),其改写属计划 03。本计划只提供运行时 INFO 读数,裁决须待计划 03 落地后由复跑确认。"
  - id: D2
    description: "面板底色与 html, body 底色同值(同一档白),屏幕上不再有可辨的灰底与 elevation 差;--color-surface(gray-2)仍是唯一比统一面更暗的一档"
    requirement: "SURF-02"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c1 (background-color=rgb(255, 255, 255))"
        status: pass
      - kind: other
        ref: ".venv/bin/python scripts/check-02-contrast.py (PASS: 0 failures)"
        status: pass
    human_judgment: true
    rationale: "同 D1:断言新契约的 c3 判据由计划 03 改写;本计划的证据是 INFO 读数 + 静态门 check-02 仍全绿。"
  - id: D3
    description: "#main-pane 计算 gap=0px;align-items: center 与 max-width: 768px 逐字保留、仍在工作;侧沟由面板与页面同色消除"
    requirement: "SURF-03"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c4 (INFO c4 #main-pane gap 原始读数: 0px)"
        status: pass
    human_judgment: true
    rationale: "c4 的 gap 期望值(12px)属被反转的旧契约,由计划 03 改写为 0px;本计划的证据是 INFO 读数。"
  - id: D4
    description: "主区↔文档区竖线 = #doc-panel 的 border-left,零新增 DOM、零位移,其宿主 rect 跨满 1440x900 视口"
    requirement: "DIV-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c5 (INFO c5 滚动前 rect: panel.top=0 panel.bottom=900)"
        status: pass
      - kind: other
        ref: "临时浏览器读数脚本(系统临时目录):#doc-panel getBoundingClientRect = {top:0, bottom:900, height:900}"
        status: pass
    human_judgment: true
    rationale: "几何断言的判据属计划 03;本计划只登记读数。"
  - id: D5
    description: "左栏面板之间的横线 = #main-pane > section + section 的 border-top,恰 3 条,第一个面板顶部不画"
    requirement: "DIV-02"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c2 (INFO 四条边框宽度: top=0px/right=0px/bottom=0px/left=1px)"
        status: pass
    human_judgment: true
    rationale: "「恰 3 条」的断言属计划 03;本计划的证据是规则块位置 + c2 INFO 读数(第 3 个 section 的 border-top-width=1px 使 c1 的对应旧断言由 FAIL 转 PASS,即横线确实落在那三个 section 上)。"
  - id: D6
    description: "两条发丝线的计算宽度均为 1px、计算颜色同时等于运行时解析的 --color-border-subtle 与写死字面量 rgb(217, 217, 217)"
    requirement: "DIV-03"
    verification:
      - kind: other
        ref: "临时浏览器读数脚本(系统临时目录):border-left-color / border-top-color / resolve_color(--color-border-subtle) / 字面量 四条均为 rgb(217, 217, 217)"
        status: pass
    human_judgment: true
    rationale: "双断言形式的判据由计划 03 写进 check-09;本计划的临时脚本已实测四条一致,但临时脚本不进仓库、不构成常驻守卫。"

duration: 17min
completed: 2026-09-28
status: complete
---

# Phase 11 Plan 01: 去卡片化与发丝分隔线 — 反转本体 Summary

**把 v1.15 Phase 9 的卡片语言整体反转成「连续白面 + 1px 发丝分隔线」:统一面就地换值为白、五个容器去边界、灰缝归零、两条发丝线落位 —— 全部是 `frontend/style.css` 一个文件上的一次就地改写。**

## Performance

- **Duration:** 17 min
- **Started:** 2026-09-28T05:16:57Z
- **Completed:** 2026-09-28T05:33:26Z
- **Tasks:** 3
- **Files modified:** 1 (`frontend/style.css`)

## Accomplishments

- `--color-surface-page` 就地换值 `var(--radix-gray-3)` → `var(--white)`,三档 elevation 叙事改写为两级;`--radix-gray-3` 仍有 `--color-surface-sunken` / `--color-surface-hover` 两个消费者 ⇒ 未造出新的零消费 primitive(D-11-3 复核成立)。
- 五个容器(4 个 `#main-pane > section` + `#doc-panel`)的边界**就地改写掉**,不是被后续规则覆盖:规则体内已不再出现 `--color-surface-card` / `--color-border` / `--radius-md` / `--shadow-card`。
- `#main-pane` 灰缝 `12px → 0`;`align-items: center` 与 `max-width: 768px` 逐字保留(D-11-5)。
- 两条发丝线落位,均取**既有**语义令牌 `--color-border-subtle`(gray-6):竖线 = `#doc-panel` 的 `border-left`(盒内手段,零新增 DOM、零位移);横线 = 新增规则块 `#main-pane > section + section` 的 `border-top`,恰命中后三个 section。
- 四段承重注释与代码同一次提交改写;两句已死的前提(「`.panel-header` 自身的 border-radius 已是 `--radius-md`」「表头底色与卡片底色同值(都取卡片令牌)」)不再留在盘上。
- 四条静态门全绿;`frontend/app.js` / `frontend/index.html` / `backend/**` / `frontend/vendor/**` 逐字节未改。

## Task Commits

Each task was committed atomically:

1. **Task 1: 统一面 + 左栏面板去边界** - `db15f71` (feat)
2. **Task 2: #doc-panel 竖线 + 表头归属 + 圆角归零 + 灰缝归零** - `523d24d` (feat)
3. **Task 3: 左栏面板间横线 + 两条发丝线运行时取证** - `ba2ab6a` (feat)

**Plan metadata:** 见收尾的 docs 提交。

## Files Created/Modified

- `frontend/style.css` — 唯一改动文件。围栏内 1 处令牌换值 + 围栏外 5 个容器规则体 + 1 条新增规则块 + 4 段承重注释。

## 运行时读数的原始输出(逐字抄录)

> 全部取自**真实浏览器**的 `getComputedStyle`。`check-09` 的整体裁决在本计划结束时是 **FAIL —— 这是设计预期**:它断言的正是本计划移除的 Phase 9 卡片语言,其改写属计划 03。**本计划一行都没有改 `check-09`。**

### Task 1 — c1

```
INFO c1 #session-panel 原始读数: background-color=rgb(255, 255, 255) border-top-left-radius=0px border-top=0px none box-shadow=none
```

### Task 2 — c2 / c4 / check-05 item 8

```
INFO c2 #doc-panel 原始读数: background-color=rgb(255, 255, 255) border-top-left-radius=0px box-shadow=none overflow-y=auto
INFO c2 #doc-panel 四条边框宽度原始读数: top=0px / right=0px / bottom=0px / left=1px
INFO c4 #main-pane gap 原始读数: 0px
INFO c4 .panel-header padding-top 原始读数: 6px
INFO item8 sticky 原始数值: scrollTop=4348 scrollHeight=5248 clientHeight=900 header={'top': 0, 'bottom': 34, 'left': 1009, 'right': 1440} panel={'top': 0, 'bottom': 900, 'left': 1008, 'right': 1440}
item 8: PASS  (13 条断言,0 FAIL,0 BLOCKED)
```

**`item8` sticky 余量的成因登记(供计划 04 的 REG-03 消费,本计划不判定):** 余量由 HEAD 的 `1.000px` 变为 **`0.000px`**(`header.top=0`、`panel.top=0`)。成因是 Phase 9 给 `#doc-panel` 加的那条 **1px 上边框**被本计划移除 —— sticky 元素被钳制在滚动容器的 padding box 上,少掉 1px 上边框就把 padding box 顶边抬到边框盒顶边。断言是**容差**(`<= 1.0`)而非等值,故仍 PASS。同一次读数里 `clientHeight` 由 `898` 变为 `900`,是上下各 1px 边框被移除的直接后果。**没有为了让旧数字成立而回退任何 1px。**

### Task 3 — c2 / c5 + 临时读数脚本

```
INFO c2 #doc-panel 四条边框宽度原始读数: top=0px / right=0px / bottom=0px / left=1px
INFO c5 滚动前 rect: panel.top=0 panel.bottom=900 header.top=0 header.bottom=36
item c5: PASS  (5 条断言,0 FAIL,0 BLOCKED)
```

临时读数脚本(`/tmp`,**未落进仓库树**;`rm` 被本仓库权限系统拒绝,内容已就地清空):

```
#doc-panel border-left-color        = rgb(217, 217, 217)
#annotations-panel border-top-color = rgb(217, 217, 217)
resolve_color --color-border-subtle = rgb(217, 217, 217)
写死字面量                            = rgb(217, 217, 217)      ← 双断言四条一致
#doc-panel getBoundingClientRect    = {'top': 0, 'bottom': 900, 'left': 1008, 'right': 1440, 'height': 900}
```

交互控件对照组(同一份运行时读数,证明「移除边界」严格限于五个容器):

```
control button(visible)      radius=999px  border-top-width=1px  box-shadow=none
control #project-path-input  radius=8px    border-top-width=1px  box-shadow=none
control select               radius=8px    border-top-width=1px  box-shadow=none
control #check-switcher      radius=8px    border-top-width=1px  box-shadow=none
control .overlay-card        radius=10px   border-top-width=0px  box-shadow=rgba(0, 0, 0, 0.2) 0px 8px 30px 0px
```

> `select` 与 `#check-switcher` 在本应用里是**同一个元素**(`frontend/index.html:46`,`document.querySelector('select')` 命中的就是它),两条读数逐字相同。

### check-09 的 FAIL 集合(逐条抄录,证明 FAIL 全部来自被移除的卡片语言)

```
FAIL [p1] #session-panel 计算 border-top-left-radius == var(--radius-md): expected=10px actual=0px
FAIL [p1] #session-panel 计算 border-top-width == 1px: expected=1px actual=0px
FAIL [p1] #session-panel 计算 border-top-style == solid: expected=solid actual=none
FAIL [p1] #session-panel box-shadow 非 none 且含卡片阴影: expected=非 none 且含 rgba(0, 0, 0, 0.08) actual=none
FAIL [p1] #session-panel box-shadow 水平偏移为 0px(零位移): expected=offset-x == 0px actual=分量=None
FAIL [p1] #annotations-panel 计算 border-top-left-radius == var(--radius-md): expected=10px actual=0px
FAIL [p1] #annotations-panel box-shadow 非 none 且含卡片阴影: expected=非 none 且含 rgba(0, 0, 0, 0.08) actual=none
FAIL [p1] #annotations-panel box-shadow 水平偏移为 0px(零位移): expected=offset-x == 0px actual=分量=None
FAIL [p1] #checks-panel 计算 border-top-left-radius == var(--radius-md): expected=10px actual=0px
FAIL [p1] #checks-panel box-shadow 非 none 且含卡片阴影: expected=非 none 且含 rgba(0, 0, 0, 0.08) actual=none
FAIL [p1] #checks-panel box-shadow 水平偏移为 0px(零位移): expected=offset-x == 0px actual=分量=None
FAIL [p1] #ai-panel 计算 border-top-left-radius == var(--radius-md): expected=10px actual=0px
FAIL [p1] #ai-panel box-shadow 非 none 且含卡片阴影: expected=非 none 且含 rgba(0, 0, 0, 0.08) actual=none
FAIL [p1] #ai-panel box-shadow 水平偏移为 0px(零位移): expected=offset-x == 0px actual=分量=None
```

`c1` 26 条断言 / **14 FAIL**;`c2` 13 条 / **8 FAIL**;`c4` 4 条 / **1 FAIL**;`c5` 5 条 / **0 FAIL(PASS)**。

**一处必须留档的对照:** Task 1 之后、Task 3 之前,`c1` 的 FAIL 数是 **20**;Task 3 落下横线后降为 **14**。差的 6 条正是 `#annotations-panel` / `#checks-panel` / `#ai-panel` 各自的 `border-top-width == 1px` 与 `border-top-style == solid` 由 FAIL 转 PASS —— 即横线**确实**落在那三个 section 上,且**没有**落到 DOM 第一个 `#session-panel` 上(它的这两条仍 FAIL,正是「第一个面板顶部不画」的机器读数)。

## 承重注释改写前后的对照

### ① 围栏内 `--color-surface-page` 上方(值 + 三档叙事)

- **改前:** 「Phase 9 sinks the page one step … gray-3 completes the **three-tier** elevation scale — page gray-3 < `--color-surface` gray-2 < `--color-surface-card` white (raised) … eight entries were on this ground …」
- **改后:** 「Phase 11 reverses the Phase 9 page-sink … This is an **IN-PLACE VALUE REWRITE**, not a new token … The elevation story therefore goes from three tiers to **two**: the unified surface white (1.000000) > the inset control surface gray-2 (0.947307) … gray-3 … is still consumed by `--color-surface-sunken` and `--color-surface-hover`, so changing this value does NOT orphan a primitive … the six entries on this ground must be RECOMPUTED — not refreshed — against white, and the two pairs Phase 9 had re-attributed to the raised ground are re-attributed back to this one.」

### ② `#main-pane > section` 上方(① / ② / ③)

- **改前:** ① 边界色取 gray-7 那一档的依据;② 「左栏卡片**不需要** `overflow: hidden`,因为 `.panel-header` 自身的 border-radius 已是 `--radius-md`」;③ 阴影取 `--shadow-card`。
- **改后:** ① 与 ③ 的旧依据被显式记为「随边界 / 阴影移除**整段作废**」;② 里那句假前提**已删除**,改记为「Phase 9 曾以『`.panel-header` 自带中等档圆角』为左栏免掉 `overflow: hidden` —— 那个前提已随本阶段把该圆角归零而死,不得再拿它当理由」;九项属性禁令与「`width` / `max-width` 是**保留**的声明,不是死代码」两段仍在;并写明 `border: none` 与紧随其后的相邻兄弟规则是**一对**。

### ③ `#doc-panel` 上方(竖线)

- **改前:** 「Phase 9:与左栏**同族卡片** —— 同底色令牌 / 同边界令牌 / 同圆角令牌 / 同阴影令牌(CARD-02)。原 `border-left: 1px` 的单边凹陷读感由四边边界 + 卡片底色取代……」
- **改后:** 「Phase 11 反转 Phase 9 的同族卡片语言……四边边界收成**单边竖线**……`border-left` 是**盒内**手段:零新增 DOM 元素、零位移……竖线只落左边,不得留任何顶侧 border/offset……`overflow-y: auto` 是**承重的滚动契约**,不得删除。」并补上竖线的 SC 1.4.11 论证。

### ④ `#doc-panel-header` 上方(sticky 背景归属)

- **改前:** 「表头底色与卡片底色同值(都取卡片令牌)」(本阶段后成为**假命题**,C-9);`border-radius: 0` 的理由是「卡片圆角本来就该在四角裁切」。
- **改后:** 「Phase 11 只改它的**归属令牌**:表头底色与统一面同值(都取页面令牌)……**声明本身不得删除。**」;`border-radius: 0` 的理由整段作废,改记为「它现在是一条**显式的零值**,不依赖任何裁切论证,故一字不动」。

## Decisions Made

- 统一面就地换值而非新增令牌;`--radix-gray-3` 的两个消费者复核成立(D-11-3)。
- 四条旧声明**就地改写**而非追加覆盖 —— 规则体内不再出现任何一个旧令牌。
- 竖线取 `#doc-panel` 的 `border-left`(盒内、零位移、天然跨满 stretch 高度),未采用「新增 DOM 元素 / margin 撑高」路线。
- 横线取新增规则块,位置紧随其所有者(「追加,不重排」),靠 `section + section` 的 DOM 相邻语义只命中后三个。
- 两条线不登记 NON-TEXT 对比度对,论证逐字引用本文件**既有**两处登记(role-band 段 + PAIR 清单头部),并记下 gray-6 在白面 1.412 的反证与 gray-7 备选被否决的理由。

## Deviations from Plan

### 计划前提经实测证伪(已登记,未改任何代码)

**1. [Rule 1 - 计划前提错误] `.overlay-card` 没有 resting border,`border-top-width` 恒为 `0px`**

- **Found during:** Task 3(交互控件对照组的运行时取证)
- **Issue:** 计划的验收标准写「`button` / `#project-path-input` / `select` / `#check-switcher` / `.overlay-card` 的 `border-top-left-radius` 均非 `0px` 且 `border-top-width` 均非 `0px`」。**实测证伪:** `.overlay-card` 在 HEAD 上**从未声明过** `border` —— 它只有 `border-radius: var(--radius-md)` + `box-shadow: var(--shadow-overlay)`(`frontend/style.css:1038-1045`);全文唯一带边界的 `.overlay-card` 是 `#mission-complete-modal .overlay-card { border: 2px solid … }`,而 DOM 序第一个 `.overlay-card` 在 `#permission-modal` 内,不匹配那条规则。故其计算 `border-top-width` 是 `0px`,**本计划改动前后都是**。
- **Fix:** **不改任何代码** —— 本计划没有、也不可能从 `.overlay-card` 上移除边界(它本来就没有)。对照组证据改写为「五个条目**均保留非零 `border-top-left-radius`**;其中四个真正承载 resting border 的控件(`button` / `#project-path-input` / `select` / `#check-switcher`)同时保留 `border-top-width = 1px`;`.overlay-card` 保留其 10px 圆角与 `--shadow-overlay` elevation」。**这不是放宽判据** —— 计划里没有任何门断言 `.overlay-card` 的 border-width(该验收项是人工清单项,不是门);被反转的禁止项(「不得把去卡片做成删掉全站所有边界」)由**实测读数**证实成立。
- **Files modified:** 无(`frontend/style.css` 的 `.overlay-card` 规则逐字节未改,已用 `git diff 6afe679` 复核)
- **Verification:** 临时浏览器脚本实测 `.overlay-card radius=10px border-top-width=0px box-shadow=rgba(0, 0, 0, 0.2) 0px 8px 30px 0px`;并回读 `frontend/style.css` 确认 `.overlay-card` 规则体内无 `border` 声明。
- **Committed in:** 无独立提交(证据在 `ba2ab6a` 的提交信息与本节)

**2. [Rule 1 - 计划措辞与磁盘事实不符] `select` 与 `#check-switcher` 是同一个元素**

- **Found during:** Task 3(对照组取证)
- **Issue:** 计划把 `select` 与 `#check-switcher` 列为两个对照组条目。实测 `frontend/index.html:46` 的 `<select id="check-switcher">` 就是 DOM 序第一个 `<select>` ⇒ 两条读数逐字相同(均 `radius=8px / border-top-width=1px`)。
- **Fix:** 不改代码;在 SUMMARY 中显式登记,避免下游把「两条相同读数」误读成两个独立证据。
- **Files modified:** 无
- **Verification:** 同一份运行时读数两条逐字相同;`grep -n '<select' frontend/index.html` 确认第一个 select 的 id 是 `check-switcher`。
- **Committed in:** 无独立提交

**3. [Rule 3 - 环境限制] 临时读数脚本无法用 `rm` 删除**

- **Found during:** Task 3(清理临时脚本)
- **Issue:** 威胁模型 T-idi-11-03 要求临时脚本「随即删除」。`rm /tmp/idi-11-probe.py` 被本仓库权限系统拒绝(与 STATE.md 记录的 `git rm` 被拒同型)。
- **Fix:** 就地清空该文件内容(改写为一行说明),使其不再是可执行脚本。文件位于**系统临时目录 `/tmp`**,从未落进仓库树(`git status --porcelain` 的已跟踪路径改动只有 `frontend/style.css`,已复核)。
- **Files modified:** 无(仓库外)
- **Verification:** `git status --porcelain -- frontend/ backend/ scripts/` 仅 `M frontend/style.css`;`git diff --stat 6afe679 -- frontend/app.js frontend/index.html backend/ frontend/vendor/` 为空。
- **Committed in:** 无独立提交

---

**Total deviations:** 3 auto-fixed(3 × Rule 1/3 分类;均为「计划前提或环境事实与磁盘不符」,零代码改动)
**Impact on plan:** 零范围扩张、零代码改动。三条都不改变交付物:五个容器的去边界、灰缝归零、两条发丝线全部按计划落地并经真实浏览器读数取证。第 1 条是**计划验收措辞的实测更正**,不是放宽判据。

## Issues Encountered

- **`check-09` 在本计划结束时 FAIL(14 / 8 / 1 条,c1 / c2 / c4)—— 设计预期,不是回归。** 它断言的正是本计划移除的 Phase 9 卡片语言。本计划**一行都没有改** `check-09`;其 c1..c4 的承重改写属计划 03。判据取它的 **INFO 原始读数**,不取它的整体裁决。
- **`check-05 --item 8` 的 sticky 余量由 `1.000px` 变为 `0.000px`** —— 成因是移除的 1px 上边框。断言是容差,仍 PASS;余量与成因已登记(供计划 04 的 REG-03)。
- 本计划的 `<verify>` 要求 `git status --porcelain` 的已跟踪路径改动只有 `frontend/style.css`。实测另有 `.planning/STATE.md` / `.planning/config.json` / `.planning/state.json` 三个**已跟踪**文件的改动 —— 三者在本次执行开始**之前**就已是 modified(会话起始的 git 快照即如此),**不是本计划产生的**。本计划自身对仓库的改动严格限于 `frontend/style.css`。
- **`gsd-tools windows append` 被拒**(`Ledger table … disagrees with the fenced JSON entries … row id(s): 17`)—— 与 Phase 8 记录的同一条已知限制。上节第 1 条偏差(`.overlay-card` 前提证伪)因此只登记在本 SUMMARY,未进 `.planning/WINDOWS.md`;按本项目口径记为已知限制,不回填、不手改渲染表。

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **计划 02 可直接开始**(同文件,波次 2):`--color-surface-card` 与 `--shadow-card` 的消费者已在本计划里**全部搬走**(3 处 + 2 处),故删除两行声明不会再触发 `check-02` 的 `resolve()` `exit 1`。围栏内 `--color-surface-card` 的残留出现次数已由 8 降为 **7**(`:126` 那处随三档叙事改写消失),`--shadow-card` 仍为 1 —— 计划 02 的专用残留断言需把两者都归零。
- **计划 03 可开始改写 `check-09` 的 c1..c4**:本 SUMMARY 已逐字抄录它此刻的 INFO 原始读数与 FAIL 集合,可直接作为「改写前」的对照。
- **计划 04 的 REG-03 复测**:`item8` 的新余量(`0.000px`)与成因已登记。
- **无阻塞项。** 唯一待办是把本 SUMMARY 与 STATE / ROADMAP 的收尾提交落下。

---
*Phase: idi-11-decard-and-hairline-dividers*
*Completed: 2026-09-28*

## Self-Check: PASSED

- `frontend/style.css` — FOUND (唯一改动文件;`git status --porcelain -- frontend/` 为空,即工作树与 Task 3 提交一致)
- `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-01-SUMMARY.md` — FOUND
- Commit `db15f71` — FOUND
- Commit `523d24d` — FOUND
- Commit `ba2ab6a` — FOUND
- `commits` 实测 = `git rev-list --count 6afe679..HEAD` = 3(与 frontmatter 的 `actuals.commits: 3` 一致)

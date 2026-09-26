---
phase: idi-09-card-containers
plan: 02
subsystem: ui
tags: [css, design-tokens, elevation, contrast-manifest, page-ground, density, playwright, computed-style, wcag, mutation-testing]

# Dependency graph
requires:
  - phase: idi-09-card-containers
    plan: 01
    provides: "卡片地面(--color-surface-card / --shadow-card 两个令牌 + 五个容器的卡片语言 + 2 条中间调 PAIR 已重新归属到卡片底色)"
  - phase: idi-04.1-radix
    provides: "单一围栏 :root 令牌层(--radix-gray-3 已声明且已被 surface-sunken / surface-hover 消费)+ 间距刻度 --space-3 / --space-4"
provides:
  - "页面底色下沉:--color-surface-page 的声明值 gray-1 → gray-3(#f0f0f0),body 计算底色 rgb(240, 240, 240)"
  - "三层 elevation 刻度在真实浏览器里成立且可机器判定:页面 gray-3 < --color-surface gray-2(控件内陷面)< 卡片白"
  - "画在页面地面上的 6 条 PAIR 以 gray-3 逐条**重算并登记**(14.30 / 5.19 / 5.19 / 5.15 / 5.19 / 4.18),登记值与 check-02 运行时实测逐位一致"
  - "清单历史段的 Phase 9 重算台账:8 条配对的「gray-1 旧值 → gray-3 新值 → 卡片白」完整链条,含 2 条 FAIL 的重新归属链路(4.65→4.18 FAIL→4.77 / 3.24→2.91 FAIL→3.32)"
  - "左栏密度收到用户裁定紧凑档(D-9-2):卡片间距 12px(--space-3)、面板内边距 16px(--space-4)"
  - "scripts/check-09-idi09-validation.py 的 c3(三层刻度 + body 底色)/ c4(密度几何 + 两条对照组)/ c5(滚动契约 + sticky 可滚前提)"
affects: [idi-09-03]

# Actuals (#2632) — chars/4 over the realized diff, same scale as the plan's `estimate`.
actuals:
  tokens: 5280
  tasks: 3
  commits: 3
plan_head_before: 1f9f8471e7b2c21a6cded1995dfc98a9eae38159

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "「重算」≠「刷新」的机器形态:登记段逐条写出旧值→新值,且新值必须与 check-02 的运行时实测输出逐位一致 —— 刷新旧值等于断言「自验证以来什么都没变」,在这里是假的"
    - "运行时门复用 check-05 的模块级设施(resolve_color / relative_luminance / contrast_ratio / read_style / ok / blocked),不重复实现、不改 check-05 一行"
    - "反空转前提必须**正面证明**后才断言:sticky 的几何断言先证明容器真的可滚(scrollHeight > clientHeight),前提不足走 blocked() 而非在不可滚的容器上空转记 PASS"
    - "密度几何断言取字面量 px 而不是令牌名 —— 两侧都从同一个令牌解析会让「令牌改坏但声明仍接线」假绿;对照组(未在裁定范围内的邻近元素)与受断言元素同批落盘"
    - "承载门的断言集必须用变异证明会失败:本项目口径「只有变异测试能证明守卫真的会失败」"

key-files:
  created: []
  modified:
    - frontend/style.css
    - scripts/check-09-idi09-validation.py

key-decisions:
  - "c3 的亮度比较取**令牌级**读数(resolve_color 三档分别解析)而不是某个元素的 effective_bg —— effective_bg 沿祖先链找第一个非透明底色,而三档里恰好有中间档不被任何元素采用时会被整个跳过,断言就在看不见的那一档上恒真"
  - "c5 的 sticky 断言落点必须取**当前可见**的 .doc-subview 的 .markdown-body:首跑把填充内容追加进了 p1 下被 display:none 藏住的 #round-doc,scrollHeight 纹丝不动(898 == 898)⇒ BLOCKED。改判据后实测 scrollHeight 2488 > clientHeight 898"
  - "密度改动只落 .panel-body(左栏 4 个面板),不碰 #doc-panel-body —— 后者是 id 选择器且元素不带 .panel-body 类,且 check-05 item 4 有活断言 padding == '32px 40px';c4 把这条重列了一遍作为回归护栏(防后来者把 .panel-body 的选择器扩成同时命中它)"
  - "Phase 9 的重算登记以**独立段落**追加在既有六个规模数字之后,六个数字(24 / 34 / 43 / 47 / 50 / 53)逐字保留 —— 本阶段清单规模不变(53 对 + 1 ORDER),变的是地面归属与实测值;把 Phase 9 混进那串数字会让「规模台账」与「值台账」不可区分"
  - "两条变异测试证明新断言非空转,且都在已提交的树上做、用定向 git checkout -- frontend/style.css 还原(不用 git stash —— 它跨工作树共享,本项目明令禁止):①position sticky→static ⇒ c5 报 2 FAIL(几何断言实测 header.top = -1589,落在面板外);②--color-surface-page gray-3→gray-2(页面与内陷面塌成一档)⇒ c3 报 2 FAIL。两次变异后均按 diff 逐字节还原"

patterns-established:
  - "「页面换值作废地面配对」的处置形态:先由前一计划把必然跌破阈值的条目重新归属,再在换值计划里逐条重算登记 —— 顺序反了会让 check-02 在中间态红着"
  - "对照组(counter-group)作为密度/几何断言的标配:受断言元素 + 一个**明确不在裁定范围内**的邻近元素同批断言,使「改动漏出范围」当场变红而不是等下游门"

requirements-completed: [CARD-03, REG-01, VIS-02]

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "页面底色下沉到 gray-3:围栏内 --color-surface-page 的声明值改为 var(--radix-gray-3),真实浏览器实测 body 计算 background-color == rgb(240, 240, 240),且令牌解析值与 body 计算底色等值(证明底色来自令牌而非硬编码)"
    requirement: "CARD-03"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c3#[p1] body 计算 background-color == rgb(240, 240, 240) + [p1] --color-surface-page 解析值 == body 计算底色"
        status: pass
      - kind: other
        ref: "bash scripts/check-01-token-conformance.sh"
        status: pass
    human_judgment: false
  - id: D2
    description: "三档 elevation 刻度在真实浏览器里严格递增:页面 0.871367 < 内陷面(--color-surface)0.947307 < 卡片(--color-surface-card)1.000000,两两对比度比值作为只读诊断打印"
    requirement: "CARD-03"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c3#[p1] 三档亮度严格递增:页面 < 内陷面 < 卡片(变异 gray-3→gray-2 时 2 FAIL)"
        status: pass
    human_judgment: false
  - id: D3
    description: "画在页面地面上的 6 条 PAIR 以 gray-3 重算并登记(14.30 / 5.19 / 5.19 / 5.15 / 5.19 / 4.18),2 条已在计划 01 重新归属的配对写出完整链条(4.65→4.18 FAIL→卡片 4.77 / 3.24→2.91 FAIL→卡片 3.32);清单规模与阈值零改动"
    requirement: "REG-01"
    verification:
      - kind: other
        ref: ".venv/bin/python scripts/check-02-contrast.py(8 条目标行逐行 grep -x 命中,ORDER 仍 0.363,PASS: 0 failures)"
        status: pass
      - kind: other
        ref: "git diff scripts/check-02-contrast.py(空)+ grep -o '/\\* PAIR' frontend/style.css | wc -l == 53 + '/\\* ORDER' == 1"
        status: pass
    human_judgment: false
  - id: D4
    description: "左栏密度收到用户裁定紧凑档(D-9-2):#main-pane 计算 gap == 12px、.panel-body 计算 padding == 16px;两条对照组证明改动没有漏出裁定范围(#doc-panel-body padding == 32px 40px、.panel-header padding-top == 6px)"
    requirement: "CARD-03"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c4#4 条断言 0 FAIL 0 BLOCKED"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-06-idi05-validation.py#g5(340px 最窄面板单行/不裁切)9/2/12/5/5/7 条断言全 PASS"
        status: pass
    human_judgment: false
  - id: D5
    description: "零新增令牌 / 零新增 tier-1 原语 / 零颜色值改动 / 零阈值放宽 / 零 PAIR 条目增删:围栏内仅 --color-surface-page 一行换值,check-02 的 TEXT_MIN / NON_TEXT_MIN 与脚本本体逐字节未动"
    requirement: "VIS-02"
    verification:
      - kind: other
        ref: "git diff -U0 frontend/style.css | grep -- '--radix-' ⇒ 仅 1 增 1 删(同一行)"
        status: pass
      - kind: other
        ref: "git status --porcelain frontend/ ⇒ 仅 frontend/style.css;ls frontend/vendor/ ⇒ 仅 marked.min.js"
        status: pass
    human_judgment: false
  - id: D6
    description: "滚动契约在运行时保持:#doc-panel 与 #chat-messages 计算 overflow-y == auto,#doc-panel-header position == sticky / top == 0px,且在**已证明可滚**的前提下滚到底时表头仍落在面板可视带内"
    requirement: "REG-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c5#[p1] #doc-panel 可滚前提下,滚到底时 #doc-panel-header 仍在面板可视区内(scrollHeight 2488 > clientHeight 898;变异 sticky→static 时 2 FAIL)"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled#17 条断言 0 FAIL 0 BLOCKED(面板区滚动者集合恰好 + 末条可达 + 24×24 命中区)"
        status: pass
    human_judgment: false

# Metrics
duration: 20min
completed: 2026-09-26
status: complete
---

# Phase 9 Plan 02: 页面底色下沉与密度收档 Summary

**页面底色从 gray-1(#fcfcfc,全场最亮)下沉到 gray-3(#f0f0f0),使「白卡片浮在灰页面之上」在屏幕上真的成立 —— 三档 elevation(gray-3 页面 < gray-2 控件内陷面 < 白卡片)由真实浏览器读数证明严格递增;同时把左栏密度收到用户裁定的紧凑档(间距 12px / 内边距 16px),并把页面换值作废的 6 条对比度配对以 gray-3 逐条重算登记(不是刷新旧值)。**

## Performance

- **Duration:** 20 min
- **Started:** 2026-09-26T13:18:47Z
- **Completed:** 2026-09-26T13:40Z
- **Tasks:** 3
- **Files modified:** 2(均为既有文件,零新建)

## Accomplishments

- **页面下沉一档,整页换色只动一行。** `--color-surface-page` 的声明值由 `var(--radix-gray-1)` 改为 `var(--radix-gray-3)`。该令牌唯一消费者是 `html, body` 的 `background`,故换值即整页换色、无第二处需要同步;`--radix-gray-3` 早已声明且已被 `--color-surface-sunken` / `--color-surface-hover` 消费 ⇒ **零新增令牌、零新增 tier-1 原语**。实测 `body` 计算底色 `rgb(240, 240, 240)`,且令牌解析值与 body 计算底色等值(证明底色来自令牌而非硬编码字面量)。
- **三档刻度由运行时门证明,且严格递增。** 页面 `0.871367` < 内陷面(`--color-surface` gray-2)`0.947307` < 卡片(`--color-surface-card` 白)`1.000000`。两两对比度比值(1.0824 / 1.1396 / 1.0528)作为只读诊断打印 —— 这是给用户看「ΔL 到底有多小」的锚点(层次主要靠边框与这点的底色差,不是靠阴影)。
- **页面换值作废的 8 条配对全部逐条结清,一条不落地登记。** 其中 6 条以 gray-3 重算后**本来就达标**(深色前景在更暗的地面上对比度上升):`--color-text` 15.88→**14.30**、`--color-text-secondary` 5.77→**5.19**、`--color-text-muted` 5.77→**5.19**、`--color-focus` 5.72→**5.15**、`--color-border-hover` 5.77→**5.19**、`--color-marker-active` NON-TEXT 4.65→**4.18**。另 2 条(中间调 blue-11 / gray-9)在 gray-3 上**跌破**阈值(`--color-marker-active` TEXT 4.18 < 4.5、`--color-border-strong` NON-TEXT 2.91 < 3.0),已在计划 01 重新归属到卡片底色并达标(4.77 / 3.32)—— 本计划把「页面旧值(达标)→ 页面新值(不达标)→ 卡片值(达标)」的完整链条写进清单历史段。8 条登记值与 `check-02` 的运行时实测输出**逐位一致**。
- **登记是「重算」而不是「刷新」。** 清单历史段新增独立段落,写明反直觉之处(页面变暗**不**让所有配对变好:深色前景上升、**中间调**下降,两条 FAIL 都是中间调)、正解是重新归属而不是调色或放宽阈值、以及本阶段全程零颜色值改动 / 零新增 primitive / 零阈值放宽。既有六个规模数字(`24 / 34 / 43 / 47 / 50 / 53`)逐字保留 —— Phase 9 清单规模不变(53 对 + 1 ORDER = 54 条清单条目),变的是地面归属与实测值。
- **密度收到用户裁定的紧凑档。** `#main-pane` 的 `gap` 就地由 `var(--space-1-5)`(6px)改为 `var(--space-3)`(12px);`.panel-body` 的 `padding` 就地由 `var(--space-2-5)`(10px)改为 `var(--space-4)`(16px)。间隙里透出的是页面底色,这正是「卡片浮在页面之上」的可见形态。右栏 `#doc-panel-body` 与 `.panel-header` 的内边距**逐字未动**,并由 c4 的两条对照组在运行时证明。
- **运行时门扩到 c1…c5 五组,全绿。** 新增 `c3`(三层刻度 + body 底色)/ `c4`(密度几何 + 两条对照组)/ `c5`(滚动契约 + sticky 可滚前提)。`--item c1,c2,c3,c4,c5` 一起跑:`exit=0`,0 FAIL / 0 BLOCKED(26 + 13 + 3 + 4 + 5 = 51 条断言)。模块 docstring 的断言映射表与 `--item` help 文本已同步列出 c1…c5。

## Task Commits

Each task was committed atomically:

1. **Task 1: 密度收档 —— `#main-pane` 的卡片间距 6px → 12px,`.panel-body` 的内边距 10px → 16px** - `e7ffa36` (feat)
2. **Task 2: 页面底色下沉到 gray-3 + 画在页面上的 6 条 PAIR 逐条重算并登记** - `7930c35` (feat)
3. **Task 3: 三层刻度的运行时门 c3 + 滚动契约门 c5** - `c4357c2` (feat)

**Plan metadata:** (本提交,docs: complete plan)

## Files Created/Modified

- `frontend/style.css` — 三处改动,全部落在既有规则体/声明内部,无新增规则块、无规则移动:
  - 围栏内 `--color-surface-page` 的声明值 `var(--radix-gray-1)` → `var(--radix-gray-3)`,并附承重注释(为什么下沉、三级刻度、唯一消费者、换值作废了哪 8 条配对以及它们各自的处置)
  - `#main-pane` 规则体内 `gap` 就地改值(`--space-1-5` → `--space-3`)+ 注释(间距是卡片层次的载体;卡片不得加 margin、页面级留白是未裁定项)
  - `.panel-body` 规则体 `padding` 就地改值(`--space-2-5` → `--space-4`)+ 注释(四个面板一致生效;`#doc-panel-body` 逐字不受影响且它有 check-05 item 4 的活断言)
  - 清单历史段追加 Phase 9 重算台账(独立段落,含 8 行表格与三条论证)
- `scripts/check-09-idi09-validation.py` — 追加 `c3` / `c4` / `c5` 三组断言集,同步模块 docstring 的断言映射表与 `--item` help 文本;复用 check-05 的 `relative_luminance` / `contrast_ratio` / `resolve_color` / `read_style` / `parse_rgb`,未另写一份,未改 check-05 一行。

**零改动的文件(计划明令):** `frontend/app.js` / `frontend/index.html` / `frontend/vendor/`(仅 `marked.min.js`)/ `scripts/check-01…07` / `scripts/check-02-contrast.py` / `scripts/check-05-ui-uat.py` / `scripts/probe-05-resolve-color.py` / `scripts/probe-07-focus-composite.py`。

## Decisions Made

- **`c3` 的亮度比较取令牌级读数,不取元素的 `effective_bg`。** 三档本身就是三个令牌;`effective_bg` 沿祖先链找第一个非透明底色,若三档里恰好有中间档不被任何元素采用,它会被整个跳过 —— 断言就在看不见的那一档上恒真。故用 `resolve_color` 分别解析后比较亮度。
- **`c5` 的 sticky 断言落点必须取当前**可见**的 `.doc-subview` 的 `.markdown-body`。** 首跑把填充内容追加进了 p1 下被 `display:none` 藏住的 `#round-doc`,`scrollHeight` 纹丝不动(898 == 898)⇒ BLOCKED。改判据后实测 `scrollHeight 2488 > clientHeight 898`、`scrollTop 1590`,表头滚动后仍在面板可视带内(`header=[1.00, 35.00]` ⊆ `panel=[0.00, 900.00]`)。**这条首跑的 BLOCKED 是门在正确工作**,不是缺陷。
- **密度改动只落 `.panel-body`,不碰 `#doc-panel-body`。** 后者是 id 选择器且元素不带 `.panel-body` 类,`check-05` item 4 有活断言 `padding == "32px 40px"`。`c4` 把这条重列了一遍作为**回归护栏** —— 防后来者把 `.panel-body` 的选择器扩成同时命中它,那时本文件会当场变红而不必等 check-05。
- **`.panel-header` 的 `padding-top` 刻意**未**随卡片内边距一起改。** 表头是 36px 固定高的 chrome 条,它的内边距不在 D-9-2 的裁定范围内;`c4` 把它作为第二条对照组断言 `== 6px`。
- **Phase 9 的重算登记以独立段落追加在既有六个规模数字之后。** 六个数字是**规模**台账,本阶段规模不变(53 对 + 1 ORDER);把 Phase 9 混进那串数字会让「规模台账」与「值台账」不可区分。登记格式为「配对 | 需要 | gray-1 | gray-3 | 卡片白 | 处置」。
- **两条变异测试证明新断言非空转(本项目口径:只有变异测试能证明守卫真的会失败)。** 均在已提交的树上做,用定向 `git checkout -- frontend/style.css` 还原(**不用 `git stash`** —— 它跨工作树共享,本项目明令禁止),还原后 `diff -q` 与备份逐字节相同:
  1. `#doc-panel-header` 的 `position: sticky` → `static` ⇒ **c5 报 2 FAIL**:直接断言 `expected=sticky actual=static`,且几何断言实测 `header.top = -1589.00`(滚到底时表头被滚出面板外)—— 证明几何断言不是恒真。
  2. `--color-surface-page` 的 `gray-3` → `gray-2`(页面与内陷面塌成一档)⇒ **c3 报 2 FAIL**:`body` 底色不再是 `rgb(240, 240, 240)`,且三档亮度序 `0.947307 < 0.947307 < 1.000000` 违反严格递增。

## Deviations from Plan

None - plan executed exactly as written.

(一处**执行期自纠**,发生在任何提交之前,净结果与计划逐条一致,不构成偏差:`c5` 首跑把滚动前提的填充内容追加进了 p1 下隐藏的 `#round-doc`,门正确地记 BLOCKED;随即把落点改为「当前可见的 `.doc-subview` 的 `.markdown-body`」并重跑至 PASS。计划的 `<action>` 只写了「先经应用自身的渲染路径把文档内容加长」,未指定宿主选择规则 —— 这正是首跑撞上的那一条,已作为 key-decision 登记。)

## Issues Encountered

- **计划里所有行号都是波次 1 之前的旧锚点**(计划写 `#main-pane` 的 `gap` 在 `:594`、`.panel-body` 在 `:688`、清单头在 `:427-452`,HEAD 实测分别为 `:657` / `:782` / `:449-494`)。全部按**选择器文本与源码内容**定位,未按行号定位;`git diff -U0` 逐行复核改动全部落在既有规则体内部。
- **`check-05 --item 8` 的 sticky 零余量断言(计划 01 引入)本计划未触碰。** 本计划对 `#doc-panel` 的边框零改动,故该读数仍是 `1.000px`(闭区间 `<= 1.0` 仍通过、余量为零)。事实未变故不重新登记 —— 与计划 01 的处置一致。
- **本机 8765 端口上有一个先前遗留的 uvicorn 在服务**,所有浏览器门本次都走了「复用,不新起、结束时也不关闭」的分支。这不影响任何断言(被测页面仍是本仓库的 `frontend/`),但意味着门的读数不是在全新进程上取得的。
- **`state.*` 动词本次的实测行为已逐条核盘**(详见 STATE.md 的 Blockers/Concerns)。与波次 1 的第 9 次复现一致:增量型写入可信、比值型不可信、回显不可作为判据;本次还新增了「格式被改坏」的两处,已手工修正。

## Known Stubs

None — 本计划零新增代码路径,零占位值。三组新断言的期望值全部是实测得到的确定值(几何 px 字面量 / 用户裁定值),没有一条走 `TODO` / 占位 / 空值渲染路径。

## Threat Flags

None — 本计划的改动面与 `<threat_model>` 逐条一致:新增行不含 `url(` / `@import`(T-idi-09-01),未新增任何定位 / 层叠属性且两处 `position: fixed` 元素仍自带底色(T-idi-09-02),密度位移的两条缓解(`#session-panel` 的 `flex: 1 1 auto` 与 `min-height: 200px`)逐字未动(T-idi-09-03),零安装(T-idi-09-SC)。未发现计划威胁模型之外的任何新安全相关面。

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **计划 03 可以开工,且本计划已替它预跑了三条最受威胁的浏览器门。** 计划 03 的职责是「五条浏览器门复跑 + pytest 基线 + 截图」;本计划在执行中额外复跑了其中三条(计划 02 的 `<verification>` 未要求,属额外确认),全部在 HEAD `c4357c2` 上绿:
  - `check-05 --item 2`(5 条断言,0 FAIL,0 BLOCKED,`exit=0`)—— `#round-doc` 正文对比度由 gray-1 上的 15.88 升至白底上的 **16.29**,与「地面变白 ⇒ 比值上升」的预判一致。
  - `check-05 --item 9`(**17 条断言**,0 FAIL,0 BLOCKED,`exit=0`)—— 面板区滚动者集合仍恰好 `{#main-pane, #chat-messages, #latest-check}`,末条可达,24×24 命中区全达标(这一条是密度改动最直接的风险面,threat T-idi-09-03)。
  - `check-06`(g1…g6 = 9/2/12/5/5/7 条断言,0 FAIL,0 BLOCKED,`exit=0`)—— 含 g5「340px 最窄面板 `#btn-authorize` 单行、不裁切」,即密度改动的窄窗口风险面。
  - `probe-07-focus-composite.py` `exit=0` —— 焦点环的地面已由 `--color-surface`(3.431)漂到卡片白(**3.54**),仍 `>= 3.0`。这是**已登记的预期效应**,不是缺陷。
- **计划 03 尚需自行完成的:** 折叠行为 / badge 流内机制两条门、`pytest` 基线(必须 `.venv/bin/python -m pytest`,环境 `python3` 是 miniconda 会造 4 个假失败;基线 **219 passed / 6 skipped**)、以及供用户评审的 5 张 1440×900 截图(`.venv/bin/python scripts/check-09-idi09-validation.py --screenshot <DIR>`)。
- **无阻塞项。** `frontend/app.js` / `frontend/index.html` / `frontend/vendor/` 零字节改动;`scripts/check-02-contrast.py` 零改动;`scripts/check-05-ui-uat.py` 本计划零改动。
- **留给用户的未裁定项(不在本阶段范围,截图时提请裁定):** `.overlay-card` 的底色(页面下沉后它会显得比主界面卡片「内陷一档」)、页面级留白(本计划明令未加 `#main-pane` padding、未给卡片加 margin)。

## Gate Evidence (HEAD = c4357c2)

| 门 | 命令 | 结果 |
|---|---|---|
| CHECK-01 | `bash scripts/check-01-token-conformance.sh` | `PASS` / exit 0 |
| CHECK-02 | `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures`;6 条页面地面重算值 14.30 / 5.19 / 5.19 / 5.15 / 5.19 / 4.18 与登记值逐位一致;2 条卡片地面 4.77 / 3.32;`ORDER 0.363` 不变;53 对 + 1 ORDER |
| CHECK-03 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` / `grep -c '^\.hidden {'` == 1 |
| CHECK-04 | `bash scripts/check-04-important-count.sh` | `PASS` / `!important` 声明数 == 1 |
| check-09 c1 | `.venv/bin/python scripts/check-09-idi09-validation.py --item c1` | 26 条断言,0 FAIL / 0 BLOCKED,`exit=0` |
| check-09 c2 | 同上 `--item c2` | 13 条断言,0 FAIL / 0 BLOCKED,`exit=0` |
| check-09 c3 | 同上 `--item c3` | 3 条断言,0 FAIL / 0 BLOCKED,`exit=0` |
| check-09 c4 | 同上 `--item c4` | 4 条断言,0 FAIL / 0 BLOCKED,`exit=0` |
| check-09 c5 | 同上 `--item c5` | 5 条断言,0 FAIL / 0 BLOCKED,`exit=0` |
| check-09 合并 | 同上 `--item c1,c2,c3,c4,c5` | 51 条断言,**`exit=0`** |
| 变异 1 | `position: sticky` → `static` 后 `--item c5` | **2 FAIL**(`exit=1`);几何断言 `header.top = -1589.00` ⇒ 非空转;`git checkout --` 还原后逐字节相同 |
| 变异 2 | `--color-surface-page: gray-3` → `gray-2` 后 `--item c3` | **2 FAIL**(`exit=1`);亮度序 `0.947307 < 0.947307 < 1.000000` ⇒ 非空转;还原后逐字节相同 |
| 额外门 1 | `.venv/bin/python scripts/check-05-ui-uat.py --item 2 --browser bundled` | 5 条断言,0 FAIL / 0 BLOCKED,`exit=0`(`#round-doc` 正文 16.29) |
| 额外门 2 | 同上 `--item 9` | 17 条断言,0 FAIL / 0 BLOCKED,`exit=0` |
| 额外门 3 | `.venv/bin/python scripts/check-06-idi05-validation.py` | g1…g6 全 PASS,`exit=0` |
| 额外探针 | `.venv/bin/python scripts/probe-07-focus-composite.py` | `exit=0`;环在卡片白上 3.54 `>= 3.0`(已登记的预期漂移) |
| 仓库卫生 | `git status --porcelain frontend/` / `ls frontend/vendor/` / `git diff scripts/check-02-contrast.py` / `git diff -U0 frontend/style.css \| grep -- '--radix-'` | 仅 `M frontend/style.css` / 仅 `marked.min.js` / 空 / 仅 1 增 1 删(同一行) |

## Self-Check: PASSED

- 修改的文件:`frontend/style.css` — FOUND;`scripts/check-09-idi09-validation.py` — FOUND
- 提交:`e7ffa36` / `7930c35` / `c4357c2` — 三条均在 `git log` 中 — FOUND
- `commits` 由磁盘 ledger 量得:`git rev-list --count 1f9f847..HEAD` == 3(在 SUMMARY 写入时量得,不含本次 docs 元数据提交)
- `actuals.tokens` 由同一把尺量得:`git diff 1f9f847..HEAD | wc -c` == 21122 → chars/4 = **5280**(计划 `estimate.tokens` 为 34000,故本计划实际消耗约估算的 15.5%)
- 工作树:执行结束时 `git status --porcelain` 仅剩本 SUMMARY 与后续状态文件(无未提交的代码改动)

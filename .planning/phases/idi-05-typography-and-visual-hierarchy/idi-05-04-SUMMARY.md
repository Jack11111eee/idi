---
phase: idi-05-typography-and-visual-hierarchy
plan: 04
subsystem: ui
tags: [css, typography, heading-scale, playwright, uat-harness, gap-closure]

# Dependency graph
requires:
  - phase: idi-05-typography-and-visual-hierarchy
    provides: "plan 01 的七档字号刻度 / `.markdown-body` 四条宿主的标题规则与 `MARKDOWN_HOSTS` 探针;plan 02 的三段坡道与页面级层级链;plan 03 的活动面板标记与两处掩码字形"
  - phase: idi-04.1-radix
    provides: "Radix 颜色族、四条守卫命令、check-02 的 47 对清单与 ORDER 断言(D-05 的连带义务对象)"
provides:
  - "`frontend/style.css` 末尾三条嵌入刻度规则(5 个选择器 × 3 档),使 `renderMarkdown()` 的全部九个注入目标都拿到契约内的字号档与 `--fw-semibold`"
  - "`scripts/check-05-ui-uat.py` 的单一事实源枚举 `MARKDOWN_TARGETS`(9 条,按调用点)+ 派生视图 + 调用点普查守卫 + `item7` 逐目标断言 + smoke 切片"
  - "`idi-05-UI-SPEC.md` 的 P-19 / P-20 / A-9 / 硬规则 9 改写 / 渲染目标影响面表(9 行)/ 05-N-7"
  - "D-05 连带义务的复验证据(04.1 四条守卫 + 三项 human_verification + 三处结论从 HEAD 重算)"
affects: ["idi-05 的收口验证(指纹 stale)", "idi-04.1-radix 的指纹重写", "Phase 8(唯一触碰 app.js 的阶段 —— 调用点普查守卫会挡住枚举漂移)"]

actuals:
  tokens: 9177
  tasks: 3
  commits: 3
  plan_head_before: 4be21b16bf712c814d72e50af01f802b8b2b536e

tech-stack:
  added: []
  patterns:
    - "影响面枚举按**调用点**而非按类名,并配一条会失败的静态普查守卫"
    - "嵌入刻度由文档刻度沿契约的**数值**阶梯下移一档推出(可复算,不是逐容器手调)"
    - "门先红后绿 + 变异测试证明守卫非空转(项目已记录的方法论)"

key-files:
  created: []
  modified:
    - frontend/style.css
    - scripts/check-05-ui-uat.py
    - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md

key-decisions:
  - "嵌入刻度取 24 / 18 / 16(下移一档),不是 28 / 22 / 18(同档)也不是 22 / 18 / 16(下移两档) —— 同档会让 SC3 的「文档 h1 是全屏最大」为假,下移两档会让嵌入 h1 与文档 h2 撞档"
  - "修法是逐容器列举而非一条全局标题规则 —— 全局规则对四处 chrome 覆盖与 `.markdown-body` 都是惰性的,于是只命中这五个容器,却把影响面重新变成不可枚举(那正是本缺陷的成因)"
  - "枚举按调用点而非按类名:九个目标里 `#round-doc` 有两个调用点,故 `renderMarkdown(` 计数是 11 而非 9;只枚举四个 `.markdown-body` 宿主正是 G-idi-05-1 存活的直接原因"
  - "item7 先造容器再断言,容器造不出记 BLOCKED;`all(w != \"700\")` 对 None 恒真,故读不到的字重必须与缺失同处置(变异探针发现并修掉的静默 PASS 洞)"
  - "SC3 的机械依据在 item7 自己的 5 条严格不等式里,不在 check-06 的 g2 —— g2 对五个嵌入容器状态盲(RED 状态下 g2 仍 PASS)"

patterns-established:
  - "影响面枚举必须问反向问题:plan 01 把探针从 1 个宿主扩到 4 个,只回答了「四个 .markdown-body 宿主都探到了吗」,没问「renderMarkdown() 到底注入到哪些容器」—— 同一错误类型的第二次发作"
  - "枚举要有会失败的守卫:静态普查守卫断言调用点数 == 11 且枚举条数 == 9,新增渲染目标而不更新枚举即 FAIL 并给出可执行动作"
  - "「读不到」必须与「不相等」分开:任何 `all(...)` 形式的否定断言都要显式处理 None,否则在元素未渲染时静默 PASS"

requirements-completed: [TYPE-01, TYPE-03, VISUAL-03]

coverage:
  - id: D1
    description: "`renderMarkdown()` 的全部九个注入目标上,h1/h2/h3 解析为契约内的字号档(文档 28/22/18、嵌入 24/18/16)与 `--fw-semibold`(600);UA 默认值(32px / 28px)与第四字重档 700 双双消失"
    requirement: TYPE-01
    verification:
      - kind: e2e
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 7 (38 条断言 / 0 FAIL / 0 BLOCKED / exit 0);RED 同命令 36 FAIL 存证"
        status: pass
    human_judgment: false
  - id: D2
    description: "字重三档分工在嵌入目标上成立:五个容器渲染的是内容,故取内容标题档 `--fw-semibold`(600),第四档 700 退出应用"
    requirement: TYPE-03
    verification:
      - kind: e2e
        ref: "check-05 --item 7 的 15 条 font-weight 令牌接线断言 + 1 条「无 700」断言"
        status: pass
    human_judgment: false
  - id: D3
    description: "页面级层级:文档 h1 严格大于每一个嵌入目标自己的 h1(28 > 24),在 AI 吐出发散标题时仍成立"
    requirement: VISUAL-03
    verification:
      - kind: e2e
        ref: "check-05 --item 7 的 5 条「文档 h1 严格大于该目标 h1」严格不等式(先造容器再断言)"
        status: pass
      - kind: e2e
        ref: ".venv/bin/python scripts/check-06-idi05-validation.py --item g1,g2 (回归守卫,9 + 2 条断言 / exit 0)"
        status: pass
    human_judgment: false
  - id: D4
    description: "check-05 的渲染目标枚举按 `renderMarkdown()` 的调用点而非按类名,并有会失败的静态普查守卫"
    requirement: TYPE-01
    verification:
      - kind: unit
        ref: "变异测试:删掉 MARKDOWN_TARGETS 一条 -> FAIL(8 vs 9);给 app.js 加一个调用点 -> FAIL(12 vs 11);未变异对照 PASS"
        status: pass
    human_judgment: false
  - id: D5
    description: "契约不再自相矛盾:P-19 / P-20 入账、零列表同步除外、A-9 收窄硬规则 9 与 TYPE-01 的措辞、影响面表点名九个目标"
    verification:
      - kind: manual_procedural
        ref: "grep 门:P-19 / P-20 各 1 行且各在零列表被点名、A-9 已登记、九个选择器与八个注入函数全部在契约里"
        status: pass
    human_judgment: true
    rationale: "「契约措辞是否真的不再自相矛盾」是判读,不是可机械核的事实;grep 门只能证明登记项在位,不能证明读者不会再被误导。这是 plan 03 同类交付物的既定处置。"
  - id: D6
    description: "D-05 连带义务:idi-04.1-radix 的四条守卫与三项 human_verification 在 HEAD 上重跑通过,三处结论与三处数量口径逐字不变"
    verification:
      - kind: manual_procedural
        ref: "check-01/02/03/04 全绿;check-05 --item 1,2,3,4,6,7 全 PASS(45/5/17/65/6/38 条断言,exit 0);ORDER 0.363、4.53、3.24+3.15、冻结轮三属性逐字不变;tier-1 25 / tier-2 48 / 清单 47 对"
        status: pass
    human_judgment: false

duration: 17 min
completed: 2026-09-21
status: complete
---

# Phase idi-05 Plan 04: 九个渲染目标的标题刻度(G-idi-05-1 闭合)Summary

**把标题刻度从 `.markdown-body` 作用域扩展到 `renderMarkdown()` 的全部九个注入目标:五个非 `.markdown-body` 容器里的 h1/h2/h3 从 UA 默认值(32px / 28px、字重 700)改为 24 / 18 / 16px 与 `--fw-semibold`,第四字重档 700 退出应用;门从 36 FAIL 转 0 FAIL,枚举改按调用点并配会失败的普查守卫。**

## Performance

- **Duration:** 17 min
- **Started:** 2026-09-21T12:02:27Z
- **Completed:** 2026-09-21T12:19:42Z
- **Tasks:** 3(Task 1 = tracer + TDD;Task 3 = 纯证据、零 diff)
- **Files modified:** 3

## Accomplishments

- **`G-idi-05-1`(BLOCKER)闭合。** `renderMarkdown()` 的九个注入目标上,标题字号与字重全部落入契约内的档位;UA 默认值(`.chat-bubble` 上下文 32px、`.event-content` 上下文 28px)与第四字重档 **700** 双双消失。
- **文档 h1 仍是全屏最大最重的文字。** 嵌入 h1 取 24px 而非 28px,`28 > 24` 由 `item7` 自己的 5 条**严格不等式**担保(先造容器再断言,不依赖 fixture 恰好有内容)。
- **枚举从「按类名」改成「按调用点」,并配一条会失败的普查守卫。** 只枚举四个 `.markdown-body` 宿主正是本缺陷存活到验证后的直接原因;普查守卫(`renderMarkdown(` == 11 且 `MARKDOWN_TARGETS` == 9)使枚举无法悄悄过期。
- **契约不再自相矛盾。** 硬规则 9 的原字面把本缺陷唯一的 CSS 侧修法也一并禁掉(A-9 收窄);P-19 把 plan 01 执行期那次未入账的选择器收窄补记进 ledger;影响面表把九个目标逐行点名。
- **D-05 连带义务履行。** 04.1 的四条守卫与三项人工验证项在 HEAD 上重跑,三处结论与三处数量口径逐字不变;两份报告文件零改动。

## Task Commits

Each task was committed atomically:

1. **Task 1 (tracer, TDD RED): 门先写、先红** - `3dfdf8e` (test)
2. **Task 1 (tracer, TDD GREEN): 三条嵌入刻度规则,门转绿** - `417b1e3` (feat)
3. **Task 2: 契约补齐 P-19 / P-20 / A-9 / 硬规则 9 / 影响面表 / 05-N-7** - `01ce2ed` (docs)
4. **Task 3: D-05 连带复验** - 无独立提交(纯证据、零 diff,沿 `idi-05-03` Task 3 的先例)

**Plan metadata:** (本提交, docs: complete plan)

_Note: Task 1 是 TDD 任务,按 RED → GREEN 两次提交;REFACTOR 无改动,故无第三次提交。_

## Files Created/Modified

- `frontend/style.css` — 文件末尾追加 3 条嵌入刻度规则(每条 5 个选择器),配一条多行注释写明取值规则、为什么不用全局标题规则、为什么不加 `margin` / `line-height`。**+38 行,零删除。**
- `scripts/check-05-ui-uat.py` — `MARKDOWN_TARGETS`(单一事实源,9 条)+ 派生 `MARKDOWN_HOSTS` / `RENDER_TARGETS` + `check_render_markdown_call_sites` 静态普查守卫 + `item7`(逐目标断言)+ `item_smoke` 切片 + 注册(`normalize_items` / `known` / `main` / 模块 docstring)。**+215 −5 行。**
- `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` — P-19 / P-20 入 ledger、零列表同步除外并分类、A-9 入契约修正登记、硬规则 9 正文改写、§字号刻度的范围栅栏 增九行影响面表、§未在 HEAD 上受控的字号 补记五个目标并标注已闭合、Notes 增 05-N-7。**+90 −11 行。**

## 先红后绿证据(逐字)

**RED —— CSS 未改,同一条命令(`--item 7`):**

```
INFO item7 渲染目标枚举: doc=['#draft-content', '#brainstorm-content', '#round-doc', '#latest-check'] embedded=['.event-content', '.chat-bubble', '.say-chunk', '.annotation-note', '.annotation-answer-body']
INFO item7 容器创建: {'created': {'.event-content': True, '.chat-bubble': True, '.say-chunk': True, '.annotation-note': True, '.annotation-answer-body': True}}
INFO item7 令牌解析: --text-xl=24px --text-lg=18px --text-md=16px --fw-semibold=600
FAIL [p1] .event-content h1 font-size == var(--text-xl): expected=24px actual=28px
FAIL [p1] .event-content h1 font-weight == var(--fw-semibold): expected=600 actual=700
FAIL [p1] .event-content h2 font-size == var(--text-lg): expected=18px actual=21px
FAIL [p1] .event-content h2 font-weight == var(--fw-semibold): expected=600 actual=700
FAIL [p1] .event-content h3 font-size == var(--text-md): expected=16px actual=16.38px
FAIL [p1] .event-content h3 font-weight == var(--fw-semibold): expected=600 actual=700
FAIL [p1] .chat-bubble h1 font-size == var(--text-xl): expected=24px actual=32px
FAIL [p1] .chat-bubble h1 font-weight == var(--fw-semibold): expected=600 actual=700
FAIL [p1] .chat-bubble h2 font-size == var(--text-lg): expected=18px actual=24px
FAIL [p1] .chat-bubble h3 font-size == var(--text-md): expected=16px actual=18.72px
...
INFO item7 文档 h1: #draft-content h1 = 28.0px
FAIL [p1] 文档 h1 严格大于 .event-content h1(SC3): expected=>28px actual=28px
FAIL [p1] 文档 h1 严格大于 .chat-bubble h1(SC3): expected=>32px actual=28px
FAIL [p1] 文档 h1 严格大于 .say-chunk h1(SC3): expected=>32px actual=28px
FAIL [p1] 文档 h1 严格大于 .annotation-note h1(SC3): expected=>28px actual=28px
FAIL [p1] 文档 h1 严格大于 .annotation-answer-body h1(SC3): expected=>28px actual=28px
FAIL [p1] 五个渲染目标无第四字重档 700(契约只声明 400/500/600): expected=无 700 actual=700,700,700,700,700,700,700,700,700,700,700,700,700,700,700
PASS app.js 的 renderMarkdown( 计数 == 11(1 定义 + 10 调用点): expected=11 actual=11
PASS MARKDOWN_TARGETS 条数 == 9(与调用点枚举一一对应): expected=9 actual=9

=== 逐项结论 ===
item 7: FAIL  (38 条断言,36 FAIL,0 BLOCKED)

exit=1  (0=全 pass,1=有 fail,2=有 blocked)
```

**GREEN —— 加完 CSS,同一条命令(`--item 7,4,smoke`):**

```
PASS [p1] .chat-bubble h1 font-size == var(--text-xl): expected=24px actual=24px
PASS [p1] .chat-bubble h1 font-weight == var(--fw-semibold): expected=600 actual=600
PASS [p1] 文档 h1 严格大于 .chat-bubble h1(SC3): expected=>24px actual=28px
PASS [p1] 五个渲染目标无第四字重档 700(契约只声明 400/500/600): expected=无 700 actual=600,600,600,600,600,600,600,600,600,600,600,600,600,600,600
PASS app.js 的 renderMarkdown( 计数 == 11(1 定义 + 10 调用点): expected=11 actual=11
PASS MARKDOWN_TARGETS 条数 == 9(与调用点枚举一一对应): expected=9 actual=9

=== 逐项结论 ===
item 7: PASS  (38 条断言,0 FAIL,0 BLOCKED)
item 4: PASS  (65 条断言,0 FAIL,0 BLOCKED)
item smoke: PASS  (9 条断言,0 FAIL,0 BLOCKED)

exit=0  (0=全 pass,1=有 fail,2=有 blocked)
```

**`item 7` 的断言条数两次相同(38),不是两个门。** RED 与 GREEN 是同一条命令的两次运行。

## 变异测试(证明守卫真的会失败,不是空转)

项目已记录的方法论:**变异测试是唯一能证明守卫真的会失败的手段。**

**1. 调用点普查守卫(静态,两次变异 + 一次未变异对照):**

```
--- 未变异对照 ---
PASS app.js 的 renderMarkdown( 计数 == 11 ...: expected=11 actual=11
PASS MARKDOWN_TARGETS 条数 == 9 ...: expected=9 actual=9
--- 变异:从 MARKDOWN_TARGETS 删掉一条 ---
PASS app.js 的 renderMarkdown( 计数 == 11 ...: expected=11 actual=11
FAIL MARKDOWN_TARGETS 条数 == 9 ...: expected=9 actual=8
--- 变异:给 app.js 加一个 renderMarkdown 调用点 ---
FAIL app.js 的 renderMarkdown( 计数 == 11 ...: expected=11 actual=12
PASS MARKDOWN_TARGETS 条数 == 9 ...: expected=9 actual=9
```

两条断言各能独立失败 —— 比的是「调用点数 vs 枚举条数」两个独立量,不是自比。

**2. 容器造不出时必须记 BLOCKED 而非 PASS(浏览器侧拦截 `/app.js`,把 `renderMarkdown` 的返回值换成空 fragment):**

```
item 7: 34 条断言,0 FAIL,32 BLOCKED  → verdict=blocked
```

容器仍被创建、标题不存在,故 30 条字号/字重断言全部退化为 `BLOCKED ... actual=<MISSING>`。**这一跑当场抓到一个真实缺陷并已修**:「无第四字重档 700」那条最初写成 `all(w != "700" for w in weights)`,而 `weights` 在标题读不到时是 15 个 `None` —— `all(None != "700")` 恒真,该断言会**静默 PASS**。已改为 `any(w is None ...)` 与缺失同处置(见 Deviations)。修复后同一次变异复跑:`32 BLOCKED`,无任何标题断言记 PASS。

## 契约补齐(Task 2)

| 登记项 | 内容 |
|---|---|
| **P-19** | chrome 标题选择器由后代形态收窄为子组合器 / id 形态(**补记**):`:704` `:775`,2 条规则 / 3 个选择器名。写明它发生在 plan 01 执行期、已登记在订正记录与 `WINDOWS.md` 第 15 条,但此前**没有 P-item** —— 按 ledger 自己的规则会让审计者拿到假阳性。这正是 `G-idi-05-1` 的 `missing` 第 3 项 |
| **P-20** | 五个非 `.markdown-body` 渲染目标的嵌入标题刻度:含 `.chat-bubble` 上下文 32 → 24 / 24 → 18 / 18.7 → 16、`.event-content` 上下文 28 → 24 / 21 → 18 / 16.4 → 16、字重一律 700 → 600,与「下移一档」的取值规则 |
| **零列表** | 例外项改为「P-2…P-4、P-12 / P-13、**P-19** 与 **P-20**」,并**分开写明各自属哪一类**:P-19 = 既有选择器改名(零列表原本要拦的那一类),P-20 = 新增规则(不在零列表字面范围内,但必须一并点名) |
| **A-9** | 硬规则 9 与 TYPE-01 的「作用域限定在 `.markdown-body` 内」收窄为「不得写全局标题规则 + 渲染目标必须逐个列举」。写明**收窄的是措辞不是意图**;TYPE-01 的需求行**不改**(与 A-5 同型:改 `REQUIREMENTS.md` 会作废指纹) |
| **硬规则 9 正文** | (a) 禁止裸类型选择器的全局标题规则并给出理由;(b) 要求逐容器列举、把 `renderMarkdown()` 的全部注入目标列进选择器表并与 check-05 的枚举一一对应;(c) 写出可机械核的负向门正则与「五个容器各 3 次」;原第三段理由保留并**追加一句**:那半句已经点出暴露面,却没有把暴露面枚举出来 —— `G-idi-05-1` 就是只读这半句、没做枚举的结果 |
| **影响面表** | §字号刻度的范围栅栏 的「`.markdown-body` 的四个宿主」那一句改为「改动的影响面 = 下表九行」,并列出 9 行(选择器 / 注入它的 `app.js` 函数 / 刻度族);表下三条:按调用点不按类名(`#round-doc` 两个调用点 ⇒ 计数 11)、`MARKDOWN_TARGETS` 是本表的机器可核形态、函数名是给人核对的锚点 |
| **05-N-7** | check-06 的 g2 对五个嵌入容器**状态盲**(只把探针注入四个 `MARKDOWN_HOSTS`,从不造 `.chat-bubble`,`p1` fixture 也是空的)—— 故「`p1` 下 g2 仍 PASS」推不出「五个容器的标题受控」;实测佐证:RED 状态下 g2 依然 PASS 而 item7 报 36 FAIL。严格不等式已搬进 item7;g2 自身加固不在本阶段 |

**`REQUIREMENTS.md` / `ROADMAP.md` / 两份旧 UI-SPEC 零改动**(`git status --porcelain` 为空)。

## D-05 复验记录(Task 3,纯证据、零 diff)

**第 1 步 —— 四条守卫(从 HEAD 重跑):**

| 命令 | 结果 |
|---|---|
| `bash scripts/check-01-token-conformance.sh` | `PASS` / exit 0 |
| `python3 scripts/check-02-contrast.py` | `PASS: 0 failures` / **47 对**(35 TEXT + 12 NON-TEXT)/ `ORDER 0.363` 行恰 1 / exit 0 |
| `bash scripts/check-03-hidden-uniqueness.sh` | `PASS`(`^\.hidden {` == 1) |
| `bash scripts/check-04-important-count.sh` | `PASS`(`!important;` 声明数 == 1) |

**第 2 步 —— 04.1 的三项 `human_verification` 逐条复核:**

1. **UI-SPEC `## UI Considerations` 的 backstop 陈述**(16 条 E1…E16;04.1 记的是 28 条):照实记录 —— 其中 7 条只含 CHECK-02 比值的一半,已由 `check-02` 实测覆盖;其余裁切 / 滚动 / 换行 / 缩放行为**无自动化证据**,属渲染几何,本计划的复验不改变这一状态。
2. **`--color-text ON --color-surface-mark` 的比值**(该对**不在**围栏清单里,`check-02` 看不见它):用与 `check-02` 同一模型(同一 WCAG 相对亮度公式、同一 `var()` 链解析)独立算出 —— `--color-text = #202020`、`--color-surface-mark = #fff7c2`、**ratio = 15.00**(≥ 4.5,通过)。与 04.1 报告的实测 15.0 一致。
3. **TOKEN-07 的「断言序关系」半场:照实记录其状态,不单方面翻转。** 复核确认:代码库里**没有任何脚本**比较四个 `--z-*` 的值(`grep -rn '--z-' scripts/` 除 `check-05` 外零命中);`check-05` 断言的是「元素 `z-index` **等于**其令牌」(`--z-selection-menu` / `--z-badge` / `--z-banner` 三条等值断言),**不是**「令牌之间的大小序」。四个声明为 `--z-badge: 10` / `--z-banner: 20` / `--z-overlay: 100` / `--z-selection-menu: 200`。**状态 = `REQUIREMENTS.md` 标 `Complete`,但该半场在机械层面不成立;用户在 `VALIDATION.md` 已裁定为 manual-only,本计划不改判。**

第 5 项(两条真实 AI 冒烟)沿用已记录的 `--ai-smoke` 证据,本计划不重跑。

**第 3 步 —— 04.1 的三处结论逐条核对(全部逐字不变):**

| 结论 | 本计划实测 | 判定 |
|---|---|---|
| 清单全 PASS + `ORDER 0.363` | `PASS: 0 failures`;`grep '^ORDER 0.363'` 恰 **1** 行 | 不变 |
| `--color-text-info ON --color-surface-info` = 4.53(0.03 余量) | `grep '^PASS  4.53  --color-text-info on --color-surface-info'` 恰 **1** 行 | 逐字不变 |
| `--color-border-strong` = `--radix-gray-9`,实测 3.24 / 3.15 | `grep -E '^PASS  3\.(24\|15)  --color-border-strong on --color-surface'` 恰 **2** 行 | 逐字不变 |
| 冻结轮:`opacity 1` + `filter saturate(0.6)` + `inset 3px 0 0` 琥珀 | `--item 2` PASS:`opacity: expected=1 actual=1` / `filter: expected=saturate(0.6) actual=saturate(0.6)` / box-shadow 语义 `inset 3px 0 0 rgb(79, 52, 34)` | 逐字不变 |
| 数量口径 | tier-1 **25** 不变;tier-2 **48** 不变(04.1 记的是 47,plan 03 已登记 47 → 48);清单 **47 对**不变 | 本计划新增令牌 **0** 个、新增 PAIR **0** 条 |

**逐条理由:** 本计划只追加了 3 条**没有声明任何新令牌**的 CSS 规则,与一组 `check-05` 的断言 / 枚举代码 —— 故 04.1 的每一处结论都应逐字不变。**实测全部不变,无一处是 04.1 的过期。**

**第 2 步的运行时批次 —— `.venv/bin/python scripts/check-05-ui-uat.py --item 1,2,3,4,6,7`:**

```
item 1: PASS  (45 条断言,0 FAIL,0 BLOCKED)
item 2: PASS  (5 条断言,0 FAIL,0 BLOCKED)
item 3: PASS  (17 条断言,0 FAIL,0 BLOCKED)
item 4: PASS  (65 条断言,0 FAIL,0 BLOCKED)
item 6: PASS  (6 条断言,0 FAIL,0 BLOCKED)
item 7: PASS  (38 条断言,0 FAIL,0 BLOCKED)
exit=0  (0=全 pass,1=有 fail,2=有 blocked)
```

`item 7` 是本计划新增的门,与 04.1 的复验批次同跑通过 —— **缺口闭合后的门与 04.1 的复验互不干扰。**

**第 4 步 —— 两条指纹义务的归属(都不得自行改写报告文件):**

- **(a) `idi-04.1-radix` 的 `covered_digest`(`v1:sha256:25d5f1fe…`)因本计划改动了它的两个 `covered_files`(`frontend/style.css` 与 `scripts/check-05-ui-uat.py`)而 stale。** 成因是内容真变,故走**重新验证**而非补指纹。指纹写回由编排器执行 **`/gsd-verify-work idi-04.1-radix`**。
- **(b) `idi-05` 自己的 `covered_digest`(`v1:sha256:b34a2d19…`)同样因本计划而 stale** —— 它的 `covered_files` 也含 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`。缺口闭合后必须重跑 **`/gsd-verify-work idi-05`**。**本计划不改 `idi-05-VERIFICATION.md`**(`git status --porcelain --` 该文件为空)。

## Decisions Made

- **嵌入刻度取 24 / 18 / 16(下移一档)。** 两个候选被否决并记入契约:28 / 22 / 18(同档)—— SC3 的措辞是「最大」,同档即不再是最大,且 D-19 的层级链 28 > 24 > 22 > 14 会在顶端失去区分;22 / 18 / 16(下移两档)—— 嵌入 h1 与文档 h2 撞档,且它不再是「下移一档」这条可复算规则的产物。
- **修法是逐容器列举,不是一条全局标题规则。** 全局规则的特异性 0-0-1 对四处 chrome 覆盖与 `.markdown-body` 都是惰性的,于是**只**命中这五个容器 —— 看起来更省事,但它无法表达三档各不相同,而三条全局规则会把任何将来的标题一并捕获(那正是本缺陷的成因),且无法把枚举逐条对照 `app.js` 的调用点。
- **枚举按调用点,不按类名。** 九个目标里 `#round-doc` 有两个调用点,故 `renderMarkdown(` 计数是 **11** 而不是 9 —— 这条差值正是普查守卫的判据来源。
- **SC3 的机械依据在 `item7`,不在 check-06 的 g2。** g2 对五个嵌入容器状态盲(05-N-7);本计划的 RED 实测就是佐证:g2 在 CSS 未改时依然 PASS,而 item7 报 36 FAIL。
- **字重取内容标题档 `--fw-semibold`(600)。** D-09 的分工里这五个容器渲染的是内容(AI 输出 / 用户批注),不是 chrome 标题 —— 这也正是消除第四字重档 700 的方式。
- **不加 `margin` / `line-height`。** 本缺陷的判据只有字号与字重;给标题加边距或行高而同一容器里的段落仍走 UA 边距,只会造成半套节奏(与 D-10 的「零新增行高令牌」一致)。

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] 修掉「无第四字重档 700」断言里的静默 PASS 洞**

- **Found during:** Task 1(tracer)的第 3 步 —— 变异探针(浏览器侧拦截 `/app.js`,把 `renderMarkdown` 的返回值换成空 fragment)
- **Issue:** 该断言原写作 `all(w != "700" for w in weights)`。当五个容器的标题**一个都读不到**时,`weights` 是 15 个 `None`,而 `all(None != "700")` 恒真 ⇒ 断言记 **PASS**。这正好违反了本计划的硬性约定「容器造不出时记 BLOCKED,绝不记 PASS」—— 一个从未红过的守卫无法证明它能看见本缺陷。
- **Fix:** 改为 `if not weights or any(w is None for w in weights): blocked(...)` —— 读不到的字重与缺失同处置。变异复跑后 `32 BLOCKED` / 0 FAIL / verdict=blocked,无任何标题断言记 PASS。
- **Files modified:** `scripts/check-05-ui-uat.py`
- **Verification:** 变异探针复跑(`/tmp/probe-idi0504-blocked.py`,不进仓库、不进守卫契约);未变异对照支仍 38 条全 PASS
- **Committed in:** `3dfdf8e`(RED 提交,修复发生在门定稿前)

---

**Total deviations:** 1 auto-fixed(1 bug)
**Impact on plan:** 该修复是**必需的** —— 不加它,计划自己声明的「绝不静默判过」约定在本计划新增的断言上就是假的。无范围蔓延:改动只有一处条件分支,断言条数不变。

## Issues Encountered

- **工作树里三处非本计划的改动:** `.claude/settings.local.json`、`.planning/STATE.md`、`.planning/state.json` 在本计划开始**之前**即为 modified(会话起始的 git status 快照已如此)。按范围边界不触碰、不还原;它们不出现在任何任务提交里。
- **Task 2 的 `git status --porcelain` 判据**要求输出「只列出本计划的三个改动面」;上述三处预存改动使该判据的字面读数多出三项。已逐项核对:**三处都不是本计划产生的**,本计划的改动面恰为 `frontend/style.css` / `scripts/check-05-ui-uat.py` / `idi-05-UI-SPEC.md`(+ 本计划自己的 PLAN / SUMMARY)。其余判据(两份旧 UI-SPEC、`idi-04.1-radix/`、`REQUIREMENTS.md`、`ROADMAP.md` 零 diff)全部字面通过。
- **Task 3 无独立提交。** 计划的 Task 3 明写「本任务不改 `frontend/style.css`,也不改任何断言逻辑;产物是复验证据,零 diff」,故沿 `idi-05-03` Task 3 的先例以「纯证据、零 diff」交付,证据在本 SUMMARY 的「D-05 复验记录」节。

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

**Phase idi-05 的缺口闭合,但阶段尚未收口。** 收口前必须按序履行两条指纹义务:

1. **`/gsd-verify-work idi-05`** —— `idi-05` 的 `covered_digest` 因本计划而 stale(它的 `covered_files` 含 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`)。
2. **`/gsd-verify-work idi-04.1-radix`** —— D-05 的连带义务;本计划已把复验输入备齐(见上「D-05 复验记录」)但**未写指纹**。

**给 Phase 8 的交接项:** `frontend/app.js` 是唯一由 Phase 8 触碰的文件。若那时新增 `renderMarkdown()` 的调用点或渲染目标,`check-05` 的调用点普查守卫会立刻 FAIL 并指明「按调用点更新 `MARKDOWN_TARGETS`,再跑本项」—— 枚举不会悄悄过期。`MARKDOWN_TARGETS` 的「注入函数名」一栏就是为此准备的锚点(比行号稳)。

**本计划不触碰、且已验证零 diff 的面:** `frontend/app.js` / `frontend/index.html` / `frontend/vendor/`(仍只含 `marked.min.js`)/ `scripts/ui-states/` / `scripts/check-02-contrast.py` / `scripts/check-06-idi05-validation.py` / plan 01 / 02 / 03 的全部交付物。

---

## Self-Check

**Created files exist:**
- `[ -f frontend/style.css ]` → FOUND
- `[ -f scripts/check-05-ui-uat.py ]` → FOUND
- `[ -f .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md ]` → FOUND

**Commits exist:**
- `git log --oneline --all | grep -q "3dfdf8e"` → FOUND
- `git log --oneline --all | grep -q "417b1e3"` → FOUND
- `git log --oneline --all | grep -q "01ce2ed"` → FOUND

**Plan invariants re-verified on HEAD:**

| 不变量 | 期望 | 实测 |
|---|---|---|
| `^\\.hidden {` | 1 | 1 |
| `!important;` 声明数 | 1 | 1 |
| `@media` | 0 | 0 |
| 围栏外裸 hex | 0 | `check-01` PASS |
| `renderMarkdown(` 计数 | 11 | 11 |
| `MARKDOWN_TARGETS` 条数 | 9 | 9 |
| 五容器 `h[123]` 各 | 3 | 3 / 3 / 3 / 3 / 3 |
| 裸类型选择器负向门 | 0 | 0 |
| 三档声明各 | 1 | 1 / 1 / 1 |
| `frontend/app.js` / `index.html` / `vendor/` diff | 空 | 空 |

**Verification results:** `.venv/bin/python scripts/check-05-ui-uat.py --item 7,4,smoke` → exit 0(38 / 65 / 9 条断言,0 FAIL / 0 BLOCKED);`.venv/bin/python scripts/check-06-idi05-validation.py --item g1,g2` → exit 0;`check-01` / `03` / `04` PASS;`check-02` 47 对 + `PASS: 0 failures`;`--item 1,2,3,4,6,7` → exit 0。

## Self-Check: PASSED

---

*Phase: idi-05-typography-and-visual-hierarchy*
*Completed: 2026-09-21*
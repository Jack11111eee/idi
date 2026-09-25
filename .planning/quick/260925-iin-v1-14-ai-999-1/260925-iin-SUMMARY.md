---
phase: 260925-iin-v1-14-ai-999-1
plan: 01
subsystem: ui
tags: [css, playwright, uat-harness, design-tokens, accessibility, mutation-testing]

# Dependency graph
requires:
  - phase: idi-06-layout-robustness
    provides: L-4 面板区滚动容器收敛(6adcaa3)—— 删掉 `.event-list` 的 max-height/overflow-y,本任务修它遗留的自动跟随回归
  - phase: idi-07-interaction-states-and-focus
    provides: FOCUSABLE_SELECTOR 与 `:focus-visible` 枚举(两条手抄副本,FIX 5 为它们补门)
  - phase: idi-05-typography-and-visual-hierarchy
    provides: 7 档字号刻度与 `--lh-*` 族(FIX 3 在此加第 8 档)
provides:
  - "AI 事件自动跟随恢复:renderEvent 追加条目后经 item.scrollIntoView({block:'nearest'}) 滚入外层 #main-pane"
  - "check-05 --item 9 新增一条经变异证明的自动跟随断言(16 → 17 条)"
  - "check-05 --item 10 新增一条静态枚举对齐断言 FOCUSABLE_SELECTOR ↔ :focus-visible(41 → 42 条),双向变异证明"
  - "第 8 档字号令牌 --text-lg-plus(20px)与 glyph-only 行高令牌 --lh-none(1),各恰一个消费者"
  - "两份 UI-SPEC 的刻度表 7 → 8 档同步 + backlog 999.1 两项关闭"
affects: [idi-04-tokens-contract, idi-04.1-radix, idi-05-typography-and-visual-hierarchy, idi-06-layout-robustness, idi-07-interaction-states-and-focus, idi-08-accessibility-semantics-and-keyboard, milestone-close-v1.14]

actuals:
  tokens: 6415      # chars/4 over the realized diff (25658 chars)
  tasks: 4
  commits: 5        # MEASURED: git rev-list --count 48e8b34..HEAD
  plan_head_before: 48e8b34057f61efbcbe3b2acfdb5c19bc7273629

tech-stack:
  added: []          # 零新增运行时依赖、零构建步骤(硬规则 6)
  patterns:
    - "变异证明作为门的一部分:新增断言必须先在「被中和的实现」上 FAIL,否则不提交"
    - "反空转前提链:前提不成立记 blocked() 而非 PASS,与 _idi06_reach / item 10 已有四条同型"
    - "两侧手抄副本(JS/CSS 常量 ↔ CSS 枚举)用静态断言同步,注释承诺不算门"

key-files:
  created: []
  modified:
    - frontend/app.js
    - scripts/check-05-ui-uat.py
    - frontend/style.css
    - .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md
    - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md

key-decisions:
  - "FIX 1 不恢复内滚动(那会回退 L-4 并打破 item 9 的滚动者普查),改为把刚追加的条目滚入外层 #main-pane"
  - "FIX 2 的新断言必须排在 item9() 内第一个 _idi06_reach() 之前 —— 后者自己设 scrollTop,排在其后「before==0」前提恒假,门会退化成空转"
  - "FIX 3 加一档字号(--text-lg-plus 20px)而非重映射到 18px / 加 L-6 例外 —— 用户已拍定,保持字形渲染尺寸不变"
  - "FIX 3 的改动面逐字限定为该规则的两个值声明;idi-05-UI-SPEC.md:677 的绝对禁令就地收窄为 textContent 赋值路径并登记唯一例外"
  - "FIX 5 的判据取有序比较而非集合比较 —— 常量上方的注释已声明「顺序亦同」,那条不变量此前无门;有序比较蕴含集合相等,零假 FAIL 风险"
  - "FIX 5 的项数不进 blocked() 前提 —— 项数不符必须流入逐项比较记 FAIL,否则变异 B 会得到 BLOCKED 而非 FAIL"

requirements-completed: [LAYOUT-04, TOKEN-08, CHECK-01, CHECK-02, CHECK-03, CHECK-04, A11Y-01]

coverage:
  - id: D1
    description: "AI 事件自动跟随恢复:应用自身的 renderEvent 追加条目后,最新条目落入外层 #main-pane 的可见盒"
    requirement: LAYOUT-04
    verification:
      - kind: e2e
        ref: ".venv/bin/python /tmp/idi-iin-260925/probe-follow.py (exit 0; before=0 after=1721 last=[848,900] pane=[0,900])"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled (PASS, 17 条断言)"
        status: pass
    human_judgment: false
  - id: D2
    description: "自动跟随门非空转:中和 FIX 1 后该断言变 FAIL(exit 1),还原后回到 PASS"
    verification:
      - kind: automated_ui
        ref: "check-05 --item 9 on the neutralized tree (FAIL, 1 FAIL, exit 1) → git checkout -- frontend/app.js → PASS (17)"
        status: pass
    human_judgment: false
  - id: D3
    description: ".collapse-indicator 的 20px 从裸字面量变为第 8 档令牌 --text-lg-plus,字形渲染尺寸不变"
    requirement: TOKEN-08
    verification:
      - kind: e2e
        ref: ".venv/bin/python /tmp/idi-iin-260925/probe-font.py (exit 0; 两个实例均 font-size=20px line-height=20px)"
        status: pass
      - kind: integration
        ref: "bash scripts/check-01-token-conformance.sh && check-02 && check-03 && check-04 (all PASS)"
        status: pass
    human_judgment: false
  - id: D4
    description: "check-05 的 --color-text-muted 诊断串陈述真实值(#646464 / 5.62:1 / 5.77:1,均达标),断言零改动"
    requirement: CHECK-02
    verification:
      - kind: automated_ui
        ref: "check-05 --item 2 --browser bundled (PASS, 5 条断言) + grep 8f8f8f=0 / 5.62:1=1"
        status: pass
    human_judgment: false
  - id: D5
    description: "FOCUSABLE_SELECTOR 与 frontend/style.css 的 :focus-visible 枚举由一条静态门守住,双向变异都能失败"
    requirement: A11Y-01
    verification:
      - kind: automated_ui
        ref: "check-05 --item 10 --browser bundled (PASS, 42 条断言); mutation A/B both FAIL (42, 1 FAIL, exit 1)"
        status: pass
      - kind: unit
        ref: ".venv/bin/python /tmp/idi-iin-260925/probe-fix5-nobrowser.py (exit 0; 9 行 item 10 记录,零浏览器)"
        status: pass
    human_judgment: false
  - id: D6
    description: "idi-05-UI-SPEC.md 的刻度表 7 → 8 档、999.1 第 1 项关闭、hard rule 9 引用登记;04-UI-SPEC.md 加如实指向行"
    verification:
      - kind: other
        ref: "grep 判据全套(见 §门基线对照表 文档块)"
        status: pass
    human_judgment: false

duration: 22min
completed: 2026-09-25
status: complete
---

# Phase 260925-iin Plan 01: v1.14 收口前五修一票 Summary

**恢复 AI 事件自动跟随(Phase 6 的 L-4 改动遗留的零门覆盖回归),并用两条带双向变异证明的门补上「标签读起来像覆盖了某行为、实际没测」这一在本里程碑已出现三次的弱点;同时把 backlog 999.1 的两项(第 8 档字号令牌化、陈旧诊断串订正)收口。**

## Performance

- **Duration:** 22 min
- **Started:** 2026-09-25T06:16:16Z
- **Completed:** 2026-09-25T06:38:29Z
- **Tasks:** 4
- **Files modified:** 5

## Accomplishments

- **FIX 1(最重要)**:`renderEvent()` 追加条目后经 `item.scrollIntoView({ block: 'nearest' })` 把该条目滚入外层 `#main-pane` —— 恢复「看 AI 干活」这条核心流程。原 `eventsEl.scrollTop = eventsEl.scrollHeight` 在 Phase 6 L-4 删掉 `.event-list` 的 `max-height`/`overflow-y` 后按 CSS 规范恒为空操作。
- **FIX 2**:check-05 `--item 9` 新增一条判定性质为**自动跟随**的断言(经应用自身的 `renderEvent` 驱动、探针 JS 内零 `scrollTop` 赋值),16 → 17 条;变异证明它在中和 FIX 1 后 FAIL。
- **FIX 3**:`.collapse-indicator` 的 `font-size: 20px` / `line-height: 1` 两个围栏外裸字面量换成第 8 档令牌 `--text-lg-plus`(20px)与 glyph-only 行高令牌 `--lh-none`(1);浏览器实读两个实例的 computed `font-size` 仍为 `20px`。
- **FIX 4**:check-05 那条称 `--color-text-muted` 变为 `#8f8f8f`、低于 AA 的陈旧诊断串订正为真值(`#646464` / 5.62:1 / 5.77:1,均达标);`item2()` 的断言一字未动。
- **FIX 5**:`_idi07_focus_contract_guards()` 新增第 ⑤ 条**静态**断言(零浏览器、零 `--ai-smoke`),逐项(含顺序)比对 `FOCUSABLE_SELECTOR` 与 `frontend/style.css` 的 `:focus-visible` 枚举;item 10 41 → 42 条;**双向**变异证明都能失败;FIX 5 对 `style.css` 的净改动为 **0**。

## Task Commits

Each task was committed atomically (5 commits across 4 tasks; Task 3 carries two):

1. **Task 1: FIX 1 — 恢复 AI 事件自动跟随** - `11fdedb` (fix)
2. **Task 2: FIX 2 — 补一条能失败的自动跟随门** - `1560bd6` (test)
3. **Task 3a: FIX 3 — 第 8 档字号与契约同步** - `3e50dca` (fix)
4. **Task 3b: FIX 4 — 订正陈旧诊断文案** - `7c991d8` (docs)
5. **Task 4: FIX 5 — 枚举对齐静态门** - `eb01a3a` (test)

`plan_head_before` = `48e8b34057f61efbcbe3b2acfdb5c19bc7273629`;`commits` 由 `git rev-list --count 48e8b34..HEAD` **实测**为 5。

## Files Created/Modified

- `frontend/app.js` — `renderEvent()` 内一条 `item.scrollIntoView({ block: 'nearest' })` 替换 no-op 的 `eventsEl.scrollTop = eventsEl.scrollHeight`(+1/−1)
- `scripts/check-05-ui-uat.py` — item9() 新增自动跟随断言(含反空转前提链);`item2()` 陈旧诊断串订正;`_idi07_focus_contract_guards()` 新增第 ⑤ 条静态断言 + 模块/函数 docstring 同步
- `frontend/style.css` — 围栏内 `--text-lg-plus: 20px;` / `--lh-none: 1;`;`.collapse-indicator` 规则值替换;三处围栏注释同步
- `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` — 刻度表 7 → 8 档、L367 改写、`:677-679` 禁令收窄、Do-Not-Touch 行更新、hard rule 9 引用登记
- `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` — 仅加一条如实指向行(6 档历史表与 L-1…L-5 清单未改)

## 门基线对照表(逐条命令 + 改动后实测值)

| 命令 | 基线(bc563d7) | 改动后实测 |
|---|---|---|
| `bash scripts/check-01-token-conformance.sh` | PASS | **PASS** |
| `.venv/bin/python scripts/check-02-contrast.py` | `PASS: 0 failures` | **`PASS: 0 failures`**(53 PASS + 1 ORDER 0.363) |
| `bash scripts/check-03-hidden-uniqueness.sh` | PASS | **PASS** |
| `bash scripts/check-04-important-count.sh` | PASS | **PASS** |
| `check-05 --item 9 --browser bundled` | `PASS (16 条断言, 0 FAIL, 0 BLOCKED)` | **`PASS (17 条断言, 0 FAIL, 0 BLOCKED)`** |
| `check-05 --item 10 --browser bundled` | `PASS (41 条断言, 0 FAIL, 0 BLOCKED)` | **`PASS (42 条断言, 0 FAIL, 0 BLOCKED)`** |
| `check-05 --item 2 --browser bundled` | PASS | **`PASS (5 条断言, 0 FAIL, 0 BLOCKED)`** |
| `check-05 --item 7 --browser bundled` | PASS | **`PASS (38 条断言, 0 FAIL, 0 BLOCKED)`**(嵌入刻度未受影响) |
| `.venv/bin/python -m pytest -q` | `219 passed, 6 skipped` | **`219 passed, 6 skipped`** |
| `node --check frontend/app.js` | OK | **OK** |
| `grep -c '^\.hidden {' frontend/style.css` | 1 | **1** |
| `grep -o '!important;' frontend/style.css \| wc -l` | 1 | **1** |
| `grep -c -- '^  --text-' frontend/style.css` | 7 | **8** |
| `grep -c -- '^  --lh-' frontend/style.css` | 4 | **5** |
| `ls frontend/vendor/` | `marked.min.js` | **`marked.min.js`**(零新依赖) |
| `git status --porcelain frontend/` | — | **空**(全部已提交) |

### 硬规则 3 / 4 的机械复核(计划未要求脚本,执行期自跑)

- **硬规则 3(追加不重排):** 用脚本提取 `HEAD:frontend/style.css` 与工作树的顶层选择器行(84 个),逐项比较 —— **selectors moved earlier = 0**,added = `[]`,removed = `[]`。围栏内新增两条声明行不是选择器块移动。
- **硬规则 4:** `@layer` = 0、`@property` = 0、`var(--x,` fallback 形态 = 0、`display: var(` = 0、`!important;` 声明数 = 1。

## FIX 1 端到端探针原始读数

`/tmp/idi-iin-260925/probe-follow.py`(临时,未提交;复用 check-05 的 `load_check05()` 同型设施 + `ensure_server()` + `make_fixture("p1")` + `enter_project()` + 捆绑 chromium headless):

```
INFO server: 127.0.0.1:8765 已在服务 —— 复用,不新起、结束时也不关闭
[probe] browser.version = 153.0.8010.12
[probe] 原始读数:
    before = 0
    after = 1721
    paneRect = {'top': 0, 'bottom': 900, 'height': 900}
    scrollHeight = 2640
    clientHeight = 900
    itemCount = 40
    lastRect = {'top': 848, 'bottom': 900, 'height': 52}
    lastText = 说话第 39 条自动跟随探针:把面板撑到可滚。

    paneOverflowY = auto
    aiEventsOverflowY = visible

[probe] 四个条件:
    PASS  (a) before == 0(harness 从未滚过)  [before=0]
    PASS  (b) after > 0(应用自己滚的)  [after=1721]
    PASS  (c) scrollHeight > clientHeight(非平凡)  [scrollHeight=2640 clientHeight=900]
    PASS  (d) 末条 .event-item rect 完全落在 #main-pane 可见盒内  [last={'top': 848, 'bottom': 900, 'height': 52} pane={'top': 0, 'bottom': 900, 'height': 900}]

[probe] exit 0 —— 自动跟随成立
PROBE_EXIT=0
```

`aiEventsOverflowY = visible` 同时把回归前提实测钉死:`#ai-events` 已不是滚动容器,真正滚的是 `paneOverflowY = auto` 的 `#main-pane`。

## FIX 2 变异证明(逐字记录)

**中和方式:** 把 `frontend/app.js` 的 `item.scrollIntoView({ block: 'nearest' });` 那一行临时改为注释 `// MUTATION (temporary): item.scrollIntoView(...)`。

**变异树 `--item 9` 输出(逐字):**

```
INFO item9 [p1] 自动跟随原始读数: before=0 after=0 scrollHeight=2640 clientHeight=900 pane=[0,900] last=[2569,2621] 末条='说话第 39 条自动跟随探针:把面板撑到可滚。\n'
FAIL [p1] 自动跟随:#main-pane 随应用自身的 renderEvent 滚到最新条目: expected=before=0 ∧ after>0 ∧ 末条 rect ⊆ #main-pane 可见盒 actual=after=0 last=[2569,2621] pane=[0,900]  # 与 (b)「末条内容可达」的区别:(b) 先自设 c.scrollTop = scrollHeight 再读 rect,测显式滚动后可达;本条 JS 内零 scrollTop 赋值,测应用自身把新条目滚入视野
=== 逐项结论 ===
item 9: FAIL  (17 条断言,1 FAIL,0 BLOCKED)

exit=1  (0=全 pass,1=有 fail,2=有 blocked)
REAL_EXIT=1
```

`after=0` 且 `last=[2569,2621]` 完全落在 `pane=[0,900]` **之外** —— 门真的报错,不是空转。

**还原证据:**

```
$ git checkout -- frontend/app.js
$ git diff -- frontend/app.js
(空)
$ grep -n "scrollIntoView" frontend/app.js
253:  item.scrollIntoView({ block: 'nearest' }); // 把最新条目滚入外层 #main-pane 视野(自动跟随)
$ node --check frontend/app.js
OK
$ .venv/bin/python scripts/check-05-ui-uat.py --item 9 --browser bundled
item 9: PASS  (17 条断言,0 FAIL,0 BLOCKED)
exit=0
```

**另记(零门覆盖的活体演示):** 提交 1 之后、Task 2 之前,`--item 9` 仍为 `PASS (16 条断言, 0 FAIL, 0 BLOCKED)` —— 修复已生效而门毫无察觉,这正是审计 §5 判「ZERO, and worse than zero」的实测形态。

## FIX 3 浏览器 computed 读数与声明计数

`/tmp/idi-iin-260925/probe-font.py`(临时,未提交):

```
[probe] .collapse-indicator 实例数 = 2
    PASS  owner=ai-panel font-size=20px line-height=20px textContent='▾'
    PASS  owner=doc-panel font-size=20px line-height=20px textContent='▾'

[probe] exit 0 —— 字形渲染尺寸仍为 20px
PROBE_EXIT=0
```

`line-height: 1` 对 20px 字号解析为 `20px`(浏览器返回**使用值**),故两个实例的 `line-height` 也必须是 `20px`。

**围栏外裸字面量清零 + 声明计数:**

```
grep -c 'font-size: 20px' frontend/style.css        # 0(基线 1)
grep -c 'line-height: 1;' frontend/style.css        # 0(基线 1)
grep -c -- '^  --text-' frontend/style.css          # 8(基线 7)
grep -c -- '^  --lh-' frontend/style.css            # 5(基线 4)
grep -c 'var(--text-lg-plus)' frontend/style.css    # 1(.collapse-indicator)
grep -c 'var(--lh-none)' frontend/style.css         # 1(.collapse-indicator)
```

**围栏注释同步(基线为 0 / 旧串为 1,才证明非空转):**

```
grep -c '8 sizes' frontend/style.css                # 1(基线 0)
grep -c '7 sizes' frontend/style.css                # 0(基线 1)
grep -c 'Line height — 五条' frontend/style.css      # 1(基线 0)
grep -c 'Line height — 四条' frontend/style.css      # 0(基线 1)
grep -c '与 8 档字号刻度' frontend/style.css         # 1(基线 0)
grep -c '18 / 20 / 22' frontend/style.css           # 1(基线 0)
grep -c '18 / 22 / 24 / 28' frontend/style.css      # 0(基线 1)
```

## FIX 4 证据

```
grep -c '8f8f8f' scripts/check-05-ui-uat.py         # 0(基线 1)
grep -c '5.62:1' scripts/check-05-ui-uat.py         # 1(基线 0)
```

`--item 2 --browser bundled` → `PASS (5 条断言, 0 FAIL, 0 BLOCKED)`,exit 0。运行时打印的诊断行与串内数字一致:

```
INFO [p3→round1] blockquote 比值(诊断,非正文): ratio=5.62 (color=rgb(100, 100, 100) on bg=rgb(249, 249, 249)) —— --color-text-muted = --radix-gray-11 = #646464(即 rgb(100,100,100)),在 --color-surface 上 5.62:1、在 --color-surface-page 上 5.77:1,两者均达标 AA
```

`git diff` 只显示那一条字符串(2 insertions / 1 deletion),`item2()` 的断言零改动。

## FIX 5 无浏览器探针 + 双向变异证明(逐字记录)

**无浏览器自证(`/tmp/idi-iin-260925/probe-fix5-nobrowser.py`,全程不启服务器、不启浏览器):**

```
[probe] _idi07_focus_contract_guards 发出 9 行 item 10 记录(无浏览器)
[probe] 本条 verdict=PASS
    label    = [static] FOCUSABLE_SELECTOR 与 :focus-visible 枚举逐项(含顺序)一致
    expected = ['button', 'input', 'select', 'textarea', 'a[href]', 'summary', '[tabindex]']
    actual   = ['button', 'input', 'select', 'textarea', 'a[href]', 'summary', '[tabindex]']
PROBE_EXIT=0
```

计划期基线为 8 行;第 ⑤ 条无条件恰发 1 条 ⇒ 9 行。`info()` 行另落盘:规则块起始行=1519、常量定义行=1751、对称差=`[]`。

### 变异 A —— 常量侧收窄一项(临时删掉 `summary`)

```
--- [A1] no-browser probe ---
PROBE_EXIT=1
FAIL [static] FOCUSABLE_SELECTOR 与 :focus-visible 枚举逐项(含顺序)一致: expected=['button', 'input', 'select', 'textarea', 'a[href]', '[tabindex]'] actual=['button', 'input', 'select', 'textarea', 'a[href]', 'summary', '[tabindex]']
[probe] 本条 verdict=FAIL

--- [A2] --item 10 --browser bundled ---
REAL_EXIT=1
item 10: FAIL  (42 条断言,1 FAIL,0 BLOCKED)
exit=1  (0=全 pass,1=有 fail,2=有 blocked)
```

还原:`git checkout -- scripts/check-05-ui-uat.py` → `git diff -- scripts/check-05-ui-uat.py` **为空**;`grep -n 'FOCUSABLE_SELECTOR = '` 回到七项原文。

### 变异 B —— CSS 侧收窄一项(临时删掉 `summary:focus-visible,` 那一行)

```
--- [B1] no-browser probe ---
PROBE_EXIT=1
FAIL [static] FOCUSABLE_SELECTOR 与 :focus-visible 枚举逐项(含顺序)一致: expected=['button', 'input', 'select', 'textarea', 'a[href]', 'summary', '[tabindex]'] actual=['button', 'input', 'select', 'textarea', 'a[href]', '[tabindex]']
[probe] 本条 verdict=FAIL

--- [B2] --item 10 --browser bundled ---
REAL_EXIT=1
item 10: FAIL  (42 条断言,1 FAIL,0 BLOCKED)
exit=1  (0=全 pass,1=有 fail,2=有 blocked)
```

两个方向的 expected/actual 恰好互换 —— 门报的是**真实的不一致**,不是「两侧都读了同一个源」的空转。

还原:`git checkout -- frontend/style.css` → `git diff -- frontend/style.css` **为空**;`git diff --stat HEAD -- frontend/style.css` **为空** ⇒ **FIX 5 对 style.css 的净改动 == 0**。

### 还原后复跑

```
check-05 --item 10 --browser bundled  → item 10: PASS  (42 条断言,0 FAIL,0 BLOCKED)  exit=0
check-05 --item 9  --browser bundled  → item 9:  PASS  (17 条断言,0 FAIL,0 BLOCKED)  exit=0
node --check frontend/app.js          → OK
grep -n 'FOCUSABLE_SELECTOR = ' scripts/check-05-ui-uat.py
1751:FOCUSABLE_SELECTOR = "button, input, select, textarea, a[href], summary, [tabindex]"
```

第 ⑤ 条对 item 9 **零影响**。

## 文档契约门(grep)

```
F5=.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md
F4=.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md

grep -c '8 档\|八档' "$F5"                 # 2   (基线 0;期望 >= 1)
grep -c -- '--text-lg-plus' "$F5"          # 6   (基线 0;期望 >= 2)
grep -c -- '--text-lg-plus' "$F4"          # 1   (基线 0;期望 == 1)
grep -c '260925-iin' "$F5"                 # 6   (基线 0;期望 >= 2)
grep -c '260925-iin' "$F4"                 # 1   (基线 0;期望 == 1)
grep -c '第 8 档' "$F5"                     # 1   (基线 0;期望 >= 1)
grep -c '20px.*刻度外\|刻度外.*20px' "$F5"  # 0   (基线 1)
grep -c '赋值路径' "$F5"                    # 3   (基线 0;期望 >= 1)
```

> 注:首次落地时 `260925-iin` 在 `$F4` 计数为 **2**(指向行里写了两处),与 `<verify>` 的「期望 == 1」不符 —— 已按判据把第二处改为「截至本指向行」,复测为 1。这是 verify 与初稿的差异,不是 verify 的问题。

## Decisions Made

- **FIX 1 的修法是 `scrollIntoView({block:'nearest'})` 而非 `mainPane.scrollTop = mainPane.scrollHeight`。** 前者不打断用户阅读上方内容(条目已在视野内时不产生位移),且是旧行为「列表底边与容器底边齐平」的忠实等价物;`inline` 用默认值。
- **FIX 2 的落点由 `_idi06_reach` 的副作用决定。** `_IDI06_REACH_JS` 自己设 `c.scrollTop = scrollHeight`(L2483),新断言排在其后则「before == 0」恒假、门恒绿 —— 故必须排在 item9() 内第一个 `_idi06_reach()` 调用之前。
- **FIX 2 把 `before == 0` 放进前提链而非判据。** 起始滚动位非 0 是「被测前提不成立」,记 `blocked()`;判据不满足才记 `FAIL`。两者不是同一件事。
- **FIX 3 加档而非重映射**(用户已拍定):值序插在 `--text-lg`(18)与 `--text-2xl`(22)之间;命名阶梯非单调的依据是已登记的 D-07 冲突(`--text-xl` 24 > `--text-2xl` 22),**不是笔误**。
- **FIX 3 对 style.css:1440-1442 嵌入刻度注释的同步是加档的直接后果。** 嵌入档**钉在已出货的三对上**(28 → 24 / 22 → 18 / 18 → 16),**不**从数值阶梯重新推导 —— 否则插入 20 后 22 的「下一档」会变成 20,而 `.markdown-body h2` 的嵌入档由 check-05 `--item 7` 断言为 `--text-lg`(18px)。注释不改就自相矛盾。
- **FIX 5 归属 item 10 而非 item 9。** 被守的性质是焦点环的覆盖集,item 10 是「A11Y-01 焦点环」项;塞进 item 9 是错误标签。
- **FIX 5 的项数不进 `blocked()` 前提。** 项数不符必须流入逐项比较记 `FAIL` —— 把项数写进前提会让变异 B 得到 `BLOCKED` 而非 `FAIL`,与 `<done>` 要求的证据互斥。
- **FIX 5 的有序比较是机制选择。** `FOCUSABLE_SELECTOR` 上方的注释已声明「顺序亦同」,而那条不变量此前**没有任何门在守**;有序比较蕴含集合相等(故完全覆盖「集合不等即 FAIL」),且今天两侧逐字同序 ⇒ 零假 FAIL 风险。

## Deviations from Plan

### 1. brief 写名的 `04-UI-SPEC.md` 不含 7 档字号表,也不含 hard rule 9(计划期已核实,处置照计划)

brief 的 FIX 3 末条写「更新 `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md`:字号刻度表(7 档 → 8 档)与其 "hard rule 9" 引用」。**该描述在 HEAD 上不成立:**

- `04-UI-SPEC.md` 的 `## Typography` 是 **Phase 4 的 6 档历史表**(11 / 12 / 13 / 14 / 15 / 16),其值已被 `idi-04.1-radix` 的 Radix 重写与 Phase 5 推翻。
- `04-UI-SPEC.md` 的 `## Global Hard Rules` 只有 1-7 条,**没有第 9 条**。
- 7 档字号刻度表与 hard rule 9 都在 `idi-05-UI-SPEC.md`。

**处置(照计划的 §已核实的偏差):** 实质同步落在 `idi-05-UI-SPEC.md`;`04-UI-SPEC.md` 只加一条**如实的指向行**(声明本节是历史声明、现行刻度为 8 档),**那张 6 档表与 L-1…L-5 §Literal exceptions 清单一字未改**(加例外是用户已否决的替代修法)。

### 2. Task 3 对 `style.css:1440-1442` 嵌入刻度注释的同步(加档的直接后果,计划已登记)

见上 §Decisions Made 第 5 条。数值序由 `12 / 14 / 16 / 18 / 22 / 24 / 28` 改为 `12 / 14 / 16 / 18 / 20 / 22 / 24 / 28`,并补一句说明嵌入档钉在已出货三对上、不从数值阶梯重推。

### 3. 函数 docstring 的「四条 → 五条」也在 `_idi07_focus_contract_guards` 自身(计划只点名模块 docstring L85)

计划 Task 4 步骤 8 只点名模块 docstring(L85)的清单句。该函数**自己的** docstring 首行同样写着「D-15 中段的四条**契约计数静态断言**」—— 只改一处会留下文件内部自相矛盾(正是本项目反复被咬的形态),故两处同提交一并改为「五条」。

### 4. `04-UI-SPEC.md` 指向行里 `260925-iin` 的首稿计数为 2,已收为 1

见上 §文档契约门 的注。判据是 `<verify>` 明写的「期望 == 1」。

**Total deviations:** 4(均为计划内已核实项或判据驱动的措辞收敛,无 Rule 1-4 意义上的自动修复)
**Impact on plan:** 无范围扩张。brief 写名的文件已按其**实质意图**满足(有指向行、不误导),7 档表的实质同步落在真正承载它的文件上。

## FIX 3 落地后会变假的散文 —— 逐条分类(读起来是决定,不是疏漏)

分类规则:**带显式时间/阶段限定的陈述 ⇒ 刻意保留为历史记录;裸的、无时间限定的绝对禁令 ⇒ 就地收窄措辞。**

### A. 就地收窄的一处(已改)

**`idi-05-UI-SPEC.md:677-679`** —— 原为「**`.collapse-indicator` 不得触碰。** …它的 `font-size: 20px` / `line-height: 1` 越轨字面量属 backlog `999.1`,**本阶段不修**。」

- **为什么必须改**(两条,缺一不可):(a) 它的第一句是**无时间限定的绝对禁令**,FIX 3 确实触碰了该元素 ⇒ 字面上为假;(b) 它的**规范登记行**(Do-Not-Touch List)在**同一次提交**里被更新为「已令牌化」—— 登记行说「已改」而段级陈述说「不得触碰」,是**文档内部自相矛盾**。
- **改法:** 禁令主体收窄为「`.collapse-indicator` 的 **`textContent` 赋值路径**不得触碰」,并登记**唯一例外**(quick `260925-iin`:两个**声明值**换成令牌,`textContent` 赋值路径与「不得内联 `<svg>`」一字未动)。
- **这不是扩大范围** —— 它就是 FIX 3 正在触碰的那条禁令本身。

### B. 刻意保留的三处(未改,历史记录)

| 位置 | 内容 | 保留理由 |
|---|---|---|
| `idi-05-UI-SPEC.md:555-556` | `#ai-panel` 零 CSS 改动段里对 `.collapse-indicator` 说「**不得触碰**」+「本阶段对 `.collapse-indicator` 的规则数改动 = **0**」 | 带「本阶段」(Phase 5)限定;末句对 Phase 5 **仍为真**。属 Phase 5 的 D-16/D-23 决定记录 |
| `idi-05-UI-SPEC.md:913` | Gate 6 的期望串 `# PASS: 恰好 1 行,内容为 { font-size: 20px; line-height: 1; }` | 写在「**本阶段**新增的两条专用门」标题之下,是 **Phase 5 的门规格**(带「本阶段」限定) |
| `idi-05-UI-SPEC.md:1329-1330` | 「字号刻度 = **5**(`12/14/16/18/24`);围栏外 `font-size: …px` 裸字面量 = **1**(`.collapse-indicator` 的 `20px`,L434,属 backlog `999.1`)」 | 写在「**基线(2026-09-20 对 HEAD 实测,非引用上游文档)**」之下,是**带日期**的历史测量 |

**三处均声明:刻意保留,非疏漏。** 它们没有对应的门 —— 由本节登记为决定,而不是由脚本断言。这是**记录在案**的覆盖缺口。

### C. `.collapse-indicator` do-not-touch 调和(计划要求显式记录)

- **FIX 3 的改动面逐字限定为该规则的两个「值」声明**:`font-size: 20px` → `var(--text-lg-plus)`、`line-height: 1` → `var(--lh-none)`。同一选择器、同一位置、同一规则块,只换值;未改选择器、未改规则块起止行、未新增/删除声明、未动该元素的 DOM 结构、行为、折叠逻辑或其他任何属性。
- **`idi-05-UI-SPEC.md:677` 的「理由」未被违反,且仍然成立**:该条给出的理由是「`app.js` 用 `textContent` 赋值,内联 `<svg>` 会被擦掉」。FIX 3 **不碰** `app.js:1759` / `:1765` 的 `textContent` 赋值路径、**不引入**内联 `<svg>`。
- **结论:`:677` 在实质上仍然为真** —— 该条要守的东西一字未动。措辞收窄的理由见上 A。
- **实证:** `git diff -- frontend/app.js` 在提交 3 内**为空**(该文件只被提交 1 改过)。

### D. 硬规则 3 / 4 的覆盖是人工核对,不是机械门(记录缺口,不新造脚本)

`check-01` 只覆盖围栏标记 / 裸 hex / tier-1 泄漏 —— 硬规则 3(追加不重排)与硬规则 4(`@layer` / `@property` / `var(--x, fallback)` / 不令牌化 `display`)**没有常驻机械门**。本次编辑在结构上不可能引入规则块移动(只换两个声明值、只在围栏内新增声明行、只改文件文本断言),故风险为零;执行期自跑了一次性机械复核(见 §硬规则 3/4 的机械复核),但**未把它固化成脚本**。该覆盖缺口**记录在此**,不新造脚本。

### E. 一处**未**按计划处置、但需登记的相邻散文(报告,不擅自改)

`idi-05-UI-SPEC.md:378`(现约 L378)仍写「本节剩余的 `.collapse-indicator` 20px 与 `#confirm-error` 16px 两条**仍然存在**,不因 P-20 而消失」。计划明写「同段的 `#confirm-error` 16px 一条(**L378**)**仍然存在**,不要顺手改它」,故**一字未动**。如实登记两点:(a) 该句的 `.collapse-indicator` 半场在**现在时**读法下已陈旧(第 1 项已关闭);(b) 但整句的主题是 **P-20 的闭合范围**(「不因 P-20 而消失」),作为 P-20 那次工作的记录仍然成立。**这是报告,不是遗漏** —— 若里程碑收口希望它一并收窄,那是一处独立的一行改动。

## Issues Encountered

- **计划期遗留的探针文件在 `/tmp/idi-iin-260925/` 内**:`probe-fix5-nobrowser.py`、`proof-fix5.py`、`proof-fix5-mutation.py`(mtime 13:38-13:42,计划期产物)。执行期重写了 `probe-fix5-nobrowser.py`(加入 label 查找与 exit code 语义),另新建 `probe-follow.py` / `probe-font.py`。`proof-fix5*.py` 未动。全部为临时文件,**未提交**。
- **`git checkout --` 的时序陷阱(计划已正确排序)**:变异 A 的还原若在提交 5 之前用 `git checkout -- scripts/check-05-ui-uat.py`,会一并丢掉尚未提交的 FIX 5 与 FIX 4 工作。计划把提交 5 排在变异之前(步骤 13 → 14),执行期照此顺序;提交前的首轮变异用 Edit 手工还原。
- **check-05 全量跑 exit 2 是预期的**(item 5 的两条 opt-in `--ai-smoke` 腿按设计 BLOCKED),本计划不依赖 `--ai-smoke`,未触发。
- **无其他问题。** 全部命令使用项目 venv `.venv/bin/python` 与 `--browser bundled`。
- **`gsd-tools windows append` 被拒(既有不一致,非本任务引入)。** 尝试把 §Deviations E 那条陈旧散文登记进 `.planning/WINDOWS.md` 时返回:`Ledger table … disagrees with the fenced JSON entries … for row id(s): 17` —— 与 STATE.md 已登记的同类事件逐字同型(`idi-08-03` 收口时也遇到同一 row 17)。按计划「该账本为 best-effort、绝不阻塞执行」的口径**未与该文件相争**:应入账的一条(§Deviations E)已改记于本 SUMMARY 的 §Deviations from Plan 与 §FIX 3 落地后会变假的散文 E 两节。**未编辑 `.planning/WINDOWS.md`。**

## 指纹影响声明(刻意保留,未重算 digest)

`frontend/style.css` / `frontend/app.js` / `scripts/check-05-ui-uat.py` 的改动按「**内容真变**」使 **idi-04 / 04.1 / 05 / 06 / 07 / 08** 六个阶段的指纹 stale。

- **刻意保留:** 未重跑那六个阶段的验证、**未重算任何 `covered_digest`**。刷新 digest 等于断言「验证之后什么都没变」,而这里是假的 —— 陈旧性作为可见信号留给里程碑收口统一处理。
- 本任务的两条新增/改动断言(**FIX 2 / FIX 5**)本身即对该类「指纹与内容脱钩」缺陷的补偿:它们把此前只由注释承诺承担的不变量(自动跟随、枚举同步)变成了能失败的门。

## Next Phase Readiness

- **审计 §5 的唯一阻断项已闭合**:AI 事件直播的自动跟随恢复,且有一条经变异证明的门守着它。
- **backlog `999.1` 两项关闭**:第 1 项(`.collapse-indicator` 的 20px 字面量)已令牌化为第 8 档;第 2 项(check-05 陈旧诊断串)已订正。
- **本里程碑第三次出现的门弱点类型已补上两处**(item 9 的自动跟随判定集、item 10 的枚举同步),各带双向/单向变异证明。
- **未闭合、交给里程碑收口的项:** 六个阶段的 stale 指纹;`idi-05-UI-SPEC.md:378` 的相邻散文(见 §Deviations E);`ROADMAP.md` 硬规则 3 的具名源码序例子与 `style.css:1498-1502` 的围栏注释(已登记的 tech debt,不在本任务范围)。
- **本 SUMMARY 之外的工作树状态:** 代码与文档契约改动已全部提交(5 个提交);`SUMMARY.md` / `STATE.md` / `ROADMAP.md` 的 docs 提交由编排器处理。`.claude/settings.local.json` 与 `.planning/.idi07-dec*.txt` / `.planning/v1.14-MILESTONE-AUDIT.md` 按约束未动、未提交。

---

*Phase: 260925-iin-v1-14-ai-999-1*
*Completed: 2026-09-25*

## Self-Check: PASSED

- **Files exist:** frontend/app.js / scripts/check-05-ui-uat.py / frontend/style.css / idi-05-UI-SPEC.md / 04-UI-SPEC.md / 260925-iin-SUMMARY.md —— 全部 FOUND
- **Commits exist:** `11fdedb` / `1560bd6` / `3e50dca` / `7c991d8` / `eb01a3a` —— 全部 FOUND
- **Measured commit count:** `git rev-list --count 48e8b34057f61efbcbe3b2acfdb5c19bc7273629..HEAD` == **5**(与 frontmatter `actuals.commits` 一致)
- **No uncommitted code changes:** `git status --porcelain frontend/ scripts/` 为空


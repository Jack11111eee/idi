---
phase: idi-10-tables-and-radius-scale
plan: 01
subsystem: ui
tags: [css, tables, design-tokens, contrast, playwright, runtime-gate]

# Dependency graph
requires:
  - phase: idi-09-card-containers
    provides: 三级 elevation 刻度(gray-3 页面 < gray-2 内陷面 < 白卡片)与既有容器边界令牌 --color-border-subtle
provides:
  - 文档区表格规则:表头取 --color-surface(gray-2)浅底,四条边里 left / right / top 归零,只剩一条 border-bottom 取 --color-border-subtle(gray-6)
  - 运行时门骨架 scripts/check-10-idi10-validation.py —— t1 / t2 两个断言集 + --screenshot / --json / --keep,复用 check-05 的模块级设施且 check-05 零改动
  - 计划 02 / 03 复用的符号:fence_text() / png_size() / load_check05() / TABLE_PROBES / TABLE_PROBE_MD / TH_BG_LITERAL / ITEMS / run_screenshots()
affects: [idi-10-02, idi-10-03, idi-10-04]

# Actuals (#2632) —— 同一 estimateTokens 口径(chars/4 over the realized diff)。
actuals:
  tokens: 6686
  tasks: 3
  commits: 2
plan_head_before: ac5dcd37c8f193266a7475e32b8ff86156440cd0

tech-stack:
  added: []
  patterns:
    - "造出容器再断言:读数前用应用自身的 renderMarkdown 注入含表格的探针 markdown,不依赖 fixture 自然渲染"
    - "两个独立读数:注入成功(元素存在)与显示性读数(宿主是否处于被渲染子树)分开采集、分开陈述"
    - "渲染证据 vs 层叠解析证据:证据强度由运行时实测分类,聚合断言使「零渲染证据」可失败"

key-files:
  created:
    - scripts/check-10-idi10-validation.py
  modified:
    - frontend/style.css

key-decisions:
  - "表格语言 = 就地改写 + 追加一条 th 规则块:并集选择器逐字未动,原 border 声明就地改写成 border: none + border-bottom,新增 .markdown-body th { background: var(--color-surface); } 紧随其后"
  - "表头新绘制面的配对零新增:check-02 本次实跑输出含 PASS  15.48  --color-text on --color-surface;PAIR / ORDER 计数仍为 53 / 1"
  - "行间与表头下的分隔线不新增 NON-TEXT 条目 —— 依据是本文件 role-band 段与清单头部两处既有登记,不是本阶段的新判据"
  - "证据分两类且由运行时实测决定:5 个对里 2 个处于被渲染子树(渲染证据),3 个被祖先 display:none 藏住(层叠解析证据);t1 / t2 各自的聚合断言使零渲染证据可失败"
  - "探针首跑暴露的两个缺陷都是探针自身的(令牌在进入 fixture 前解析;读数跨过 enter_project 的重新导航),不是产品缺陷 —— 已就地修掉"

patterns-established:
  - "表格的运行时判据只能用 getComputedStyle:文本里写着 background 不等于浏览器里真的生效"
  - "隐藏子树上的计算样式照常返回解析值 ⇒ 「注入成功」推不出「被渲染」,两个事实必须各自断言"

requirements-completed: [TABLE-01, TABLE-02]

coverage:
  - id: D1
    description: "文档区表格在真实浏览器里不再有竖线与外框(td 的 left / right / top border-width 为 0px),表头拿到 --color-surface(gray-2)浅底,行间与表头下是一条 1px solid 的 --color-border-subtle(gray-6)细线"
    requirement: "TABLE-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-10-idi10-validation.py --item t1"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-10-idi10-validation.py --item t2"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-02-contrast.py"
        status: pass
    human_judgment: false
  - id: D2
    description: "表格的渲染判据首次有自动化运行时覆盖:新门 scripts/check-10-idi10-validation.py 的骨架(t1 / t2 / --screenshot / --json),计划 02 扩展、计划 03 直接消费 --screenshot"
    requirement: "TABLE-02"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-10-idi10-validation.py --screenshot <DIR> ⇒ 恰 5 张 1440x900 PNG"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-10-idi10-validation.py --item t1 --item t2 --json ⇒ json.load 解析出 99 条记录"
        status: pass
    human_judgment: false
  - id: D3
    description: "表头的 gray-2 浅底是否真的把表格读作「白卡片内的一个内陷块」,而不是换了一种网格"
    verification: []
    human_judgment: true
    rationale: "计算样式能证明「底色 == gray-2 且只剩一条横向分隔线」,不能证明它读起来是白卡片内的内陷块而非另一种网格 —— 这是 D-10-1 的视觉主张,只有人眼能判。计划 03 的 5 张 1440×900 截图是本条的评审入口。"

duration: 25 min
completed: 2026-09-27
status: complete
---

# Phase 10 Plan 01: 表格重做(表头浅底 + 仅横向分隔线)与运行时门骨架 Summary

**文档区表格从「每格 1px 全边框的电子表格式网格」改为「gray-2 表头浅底 + 仅横向分隔线」,并新建运行时门 `scripts/check-10-idi10-validation.py`,在真实浏览器里以 computed style 读出 99 条断言、0 FAIL / 0 BLOCKED**

## Performance

- **Duration:** 25 min
- **Started:** 2026-09-27T10:58:05Z(规划收口提交 `ac5dcd3` 的时刻)
- **Completed:** 2026-09-27T11:24Z
- **Tasks:** 3
- **Files modified:** 2(1 新建 + 1 就地改写)

## Accomplishments

- `frontend/style.css` 的 `.markdown-body th, .markdown-body td` 里那条 `border: 1px solid var(--color-border);` 被**就地改写**成 `border: none;` + `border-bottom: 1px solid var(--color-border-subtle);`;并集选择器文本、规则块位置、`padding` 与 `font-size` 两行、`.markdown-body table` 的 `border-collapse` **逐字未动**
- 紧随其后**追加**一条 `.markdown-body th { background: var(--color-surface); }` —— 该选择器在 HEAD 上不存在,故不参与任何既有等特异性对,既有规则块的相对源码顺序逐字未变;三个机器可解析表(批注回应表 / 覆盖维度表 / 未决问题清单)共用这一条规则,该一致性是结构性的
- 表头新绘制面上的配对**零新增**:`check-02` 本次实跑输出含 `PASS  15.48  --color-text on --color-surface`(既有条目),PAIR / ORDER 计数仍为 **53 / 1**
- 新建 `scripts/check-10-idi10-validation.py`:复用 check-05 的模块级设施(服务生命周期 / fixture 隔离 / 断言记录器 / 读数器 / 令牌解析 / 样本清单),**check-05 一行未改**;`t1`(表头)/ `t2`(数据格)两个断言集在真实浏览器里全 PASS;`--screenshot DIR` 出 5 张 1440×900;`--json` 可机器消费
- 表格的渲染判据**首次**有了自动化运行时覆盖 —— 在此之前,TABLE-01 / TABLE-02 的渲染判据零自动化覆盖(唯一接触点 `check-05:1126` 断言的是 `td font-size`,不是本阶段改的属性)

## Task Commits

Each task was committed atomically:

1. **Task 1: 表格规则就地改写 —— 表头 gray-2 浅底 + 仅横向分隔线** - `8bfe4f9` (feat)
2. **Task 2: 新建运行时门 scripts/check-10-idi10-validation.py** - `b4fe65d` (feat)
3. **Task 3: 表头新绘制面的对比度登记核实 + 四个静态门逐字节证据(D-10-3)** - **无独立提交**(只跑命令与记录,零文件改动;沿 `idi-09-02` 的零净 diff 先例)

**Plan metadata:** `b94e976` (docs: complete plan) + `5cf6a73` (fix: 校正派生计数)

_Note: TDD tasks may have multiple commits (test → feat → refactor)_

## Files Created/Modified

- `scripts/check-10-idi10-validation.py`(新建,454 行)- Phase 10 的运行时门:`t1` / `t2` 两个断言集、`--item` / `--screenshot` / `--json` / `--keep`;`TABLE_PROBES` 5 个 (样本, 宿主) 对;每个对读数前用应用自身的 `renderMarkdown` 注入 `TABLE_PROBE_MD`,并当场采集「注入成功」与「是否被渲染」两个独立读数
- `frontend/style.css`(+25 / −1)- 表格规则改造(就地改写一条 `border` 声明 + 追加一条 `.markdown-body th` 规则块 + 一段承重注释)

## Gate Evidence(原始输出,不是摘录)

```
$ bash scripts/check-01-token-conformance.sh
PASS            # rc=0
$ bash scripts/check-03-hidden-uniqueness.sh
PASS            # rc=0
$ bash scripts/check-04-important-count.sh
PASS            # rc=0
$ .venv/bin/python scripts/check-02-contrast.py
PASS  15.48  --color-text on --color-surface      # ← 表头新绘制面的配对(既有条目),本次实跑原文
ORDER 0.363  --color-text-muted before --color-text on --color-surface
PASS: 0 failures                                  # rc=0
```

```
$ .venv/bin/python scripts/check-10-idi10-validation.py --item t1
item t1: PASS  (53 条断言,0 FAIL,0 BLOCKED)
exit=0  (0=全 pass,1=有 fail,2=有 blocked)

$ .venv/bin/python scripts/check-10-idi10-validation.py --item t2
item t2: PASS  (46 条断言,0 FAIL,0 BLOCKED)
exit=0  (0=全 pass,1=有 fail,2=有 blocked)

$ .venv/bin/python scripts/check-10-idi10-validation.py --screenshot /tmp/idi-10-shot-selfcheck
item t1: PASS  (53 条断言,0 FAIL,0 BLOCKED)
item t2: PASS  (46 条断言,0 FAIL,0 BLOCKED)
item shot: PASS  (7 条断言,0 FAIL,0 BLOCKED)
exit=0
# 目录内容:archive.png checking.png p1.png p12.png p3.png —— 恰 5 个,逐张 1440x900

$ .venv/bin/python scripts/check-10-idi10-validation.py --item t1 --item t2 --json
# stdout 为纯 JSON(json.loads 成功),99 条记录 = 人类可读模式的 53 + 46
```

`--color-text on --color-surface` 那一行是**本次实跑**的输出原文。规划期 Pattern Map 里出现过的比值**未被本机复现**,故未沿用任何历史数字(唯一写入摘要的数值即上行的 `15.48`)。

## 证据强度:渲染证据 vs 层叠解析证据(不得写成等价证据)

门输出的分类行原文:

```
INFO t1 证据分类: 渲染证据 2 个对 / 层叠解析证据 3 个对 ——
  rendered=(p1, #draft-content), (p3, #round-doc) /
  hidden=(p1, #brainstorm-content)<-#brainstorm-view, (p1, #round-doc)<-#rounds-placeholder, (p1, #latest-check)<-#checks-panel
```

| 对 | 注入后 th / td | 处于被渲染子树 | 藏住它的祖先 | 证据类别 |
|---|---|---|---|---|
| `(p1, #draft-content)` | 3 / 6 | **是** | — | **渲染证据** |
| `(p3, #round-doc)` | 3 / 6 | **是** | — | **渲染证据** |
| `(p1, #brainstorm-content)` | 3 / 6 | 否 | `#brainstorm-view`(.hidden) | 层叠解析证据 |
| `(p1, #round-doc)` | 3 / 6 | 否 | `#rounds-placeholder`(.doc-subview.hidden) | 层叠解析证据 |
| `(p1, #latest-check)` | 3 / 6 | 否 | `#checks-panel`(.hidden) | 层叠解析证据 |

5 个对**全部注入成功**(注入后 `td` 计数均为 6 ⇒ 无一为 0,不触发「停下报回」处置),且**至少 1 个对处于被渲染子树**(实测 2 个)⇒ 聚合断言 PASS,渲染判据成立。隐藏子树上的读数只证明**层叠解析**(规则选对了元素、声明按预期解析) —— 计算样式与 `display` 无关,故「注入成功」推不出「被渲染」。

## D-10-3 的零新增 / 零放宽逐字节证据

| 判据 | 实测 | 命令 |
|---|---|---|
| `check-02` 阈值与 HEAD 逐字节相同 | `git diff -- scripts/check-02-contrast.py` 输出 **0 行**;常量仍为 `TEXT_MIN = 4.5` / `NON_TEXT_MIN = 3.0` | `git diff -- scripts/check-02-contrast.py` |
| 零 tier-1 primitive 改动 | 增删行里以 `--radix-` 开头的行 **0 条**(`grep` rc=1) | `git --no-pager diff -U0 8bfe4f9^ 8bfe4f9 -- frontend/style.css \| grep '^[+-].*--radix-'` |
| 零 PAIR / ORDER 条目增删 | `/\* PAIR` = **53**、`/\* ORDER` = **1**(与改动前逐字相同) | `grep -o '/\* PAIR' frontend/style.css \| wc -l` |
| 零新增媒体查询 | `@media` 计数 = **1**(Phase 7 的 prefers-reduced-motion 块) | `grep -c '@media' frontend/style.css` |
| 新增注释不含围栏外禁字 | 新增行里 `#hex` / `var(--radix-` / `var(--white)` / `!important;` / `@media` / `@layer` / `@property` 命中 **0 条**(`grep` rc=1);注释全部落在围栏**外**(围栏为 `style.css:5` → `:687`,改动在 `:1080` 之后) | `git --no-pager diff -U0 8bfe4f9^ 8bfe4f9 -- frontend/style.css \| grep '^+' \| grep -E '#[0-9a-fA-F]{3,6}\|var\(--radix-\|…'` |
| `td` 的 `font-size` / `padding` 一字未动 | 两个属性在**每个**探针对上都是 PASS(`td font-size == 14px`、`padding == 4px 10px`) | `--item t2` 的 10 条对照组断言 |

## 装饰性边界 ⇒ 零新增 NON-TEXT 条目:依据是两处**既有**登记

表头下边线与行间分隔线**不标识任何东西**(它们是视觉分组的装饰,不是控件的边界),故 SC 1.4.11 不适用。本阶段**不新发明判据**,引用本文件两处既有原文:

- `frontend/style.css` 围栏内 role-band 段:`The other three borders stay in band 6-8: they are decorative, and SC 1.4.11 does not apply to a border that identifies nothing.`
- `frontend/style.css` 围栏内对比度配对清单头部:`Decorative separators are deliberately absent — SC 1.4.11 does not apply to a border that identifies nothing.`

新增的承重注释(围栏外,写在 `.markdown-body table` 规则块上方)逐条记下五件事:档位依据(gray-2 是三级刻度的「内陷面」档)、就地改写的理由、分隔线的档位与上述两处既有登记、零新增配对的依据、以及 `padding` / `font-size` 不得触碰。

## 源码级验收(报告体域内计数,不是全文裸计数)

`awk` 取 `.markdown-body th, .markdown-body td {` 到其闭合 `}` 之间的行域后计数:

| 域内计数的模式 | 计数 | 期望 |
|---|---|---|
| `border: none;` | 1 | 1 |
| `border-bottom: 1px solid var(--color-border-subtle);` | 1 | 1 |
| `border: 1px solid var(--color-border);` | **0** | 0(已就地改写,不是被覆盖) |
| `padding: var(--space-1) var(--space-2-5);` | 1 | 1 |
| `font-size: var(--text-base);` | 1 | 1 |

全文计数另记(HEAD 现状会让全文裸计数误报,故两条判据分开写):`border: none;` 全文 **2**(本任务 1 + `#selection-menu button` 既有 1);`border: 1px solid var(--color-border);` 全文 **2**(`#main-pane > section` 与 `#doc-panel` 两处容器规则,均不在 `.markdown-body` 内;HEAD 上是 3);`border-bottom: 1px solid var(--color-border-subtle);` 全文 **1**(HEAD 上是 0)。`grep -nF '.markdown-body th { background: var(--color-surface); }'` 命中**恰 1** 行(`style.css:1110`)。

## Decisions Made

- **就地改写而非追加覆盖规则** —— 留下一条已死的 `border` 声明会让注释与代码互相矛盾(与 Phase 9 对 `#doc-panel` 的 `border-left` 同一纪律)。并集选择器 `.markdown-body th, .markdown-body td` **逐字未动**:拆分 `th` 与 `td` 是重排风险区(至少一对等特异性规则由源码顺序决定)。新增的 `.markdown-body th` 必须插在其所有者正后方。
- **分隔线取 `--color-border-subtle`(gray-6)而非 `--color-border`(gray-7)** —— 后者是「深」的那一档,正是本次要去掉的观感;`--color-border-subtle` 是**既有**的容器边界令牌(`#doc-panel` / `.event-list` 在用)⇒ 零新增令牌。
- **`t1` / `t2` 的期望侧取自 `resolve_color`,另加一条令牌级「两侧都写死」断言**(`--color-surface` == `rgb(249, 249, 249)`)—— 若两侧都从同一个令牌解析,令牌被改坏而消费者仍接线时也照样 PASS。
- **断言与注入必须就地成对**,不能「先收集全部读数、再统一断言」—— `enter_project` 会 `page.goto` 重新导航,滞后读会读到已清空的宿主。这条在首跑时以满屏 `<MISSING>` 的形态真实发生过(见 Deviations)。
- **`--json` 时把人类可读输出改道 stderr**,使 stdout 是一份可被 `json.loads` 解析的纯 JSON。

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] 令牌在进入 fixture **之前**解析,全部返回 `None`**
- **Found during:** Task 2(新建运行时门)首跑 `--item t1`
- **Issue:** 原实现把 `resolve_color("--color-surface")` / `resolve_token("--text-base")` 放在 `enter_project` **之前**。页面仍是 `about:blank` 时 `documentElement` 上没有任何 CSS 自定义属性 ⇒ 全部返回 `None` ⇒ `ok()` 的 expected 侧为 `None` 时落进 BLOCKED 分支,首跑 `t1` 报 **53 条断言 / 0 FAIL / 35 BLOCKED / exit=2**。一次真实的 PASS 被读成了大面积 BLOCKED。
- **Fix:** 新增 `on_entered(page)` 钩子,由 `run_probe_pairs` 在**第一次** `enter_project` 之后、任何读数之前调用一次;令牌解析与该批令牌级断言挂在这个时点。
- **Files modified:** `scripts/check-10-idi10-validation.py`
- **Verification:** 复跑 `--item t1` ⇒ BLOCKED 由 35 归 **0**,exit=2 → **0**;令牌解析 INFO 行变为 `--color-surface=rgb(249, 249, 249) --color-border-subtle=rgb(217, 217, 217) --text-base=14px`(与预期字面量逐字相符)
- **Committed in:** `b4fe65d`(Task 2 提交;首跑的两个缺陷都在该提交落盘之前修掉,git 历史里只有修好的形态)

**2. [Rule 1 - Bug] 读数与注入跨过了 `enter_project` 的重新导航,注入的 DOM 被丢掉**
- **Found during:** Task 2 首跑(与上条同一次运行)
- **Issue:** 原实现先遍历全部 5 个对做注入并把读数收进一个列表,遍历结束后才统一跑断言。但 `(p3, #round-doc)` 的注入会调用 `enter_project("p3")` ⇒ `page.goto` 重新导航 ⇒ **`p1` fixture 里注入的 DOM 全部消失**。断言阶段读 `#draft-content th` / `#latest-check th` 时元素已不存在 ⇒ `read_style` 返回 `None`,大量 `<MISSING>`。这是**探针缺陷**,不是产品缺陷。
- **Fix:** 把注入、两条读数与断言合并进同一次遍历 —— `run_probe_pairs(page, tmp_root, item, assert_pair, on_entered)`,同一 `样本` 只 `make_fixture` + `enter_project` 一次,每个宿主**各注入一次后立即断言**,再进入下一个宿主。
- **Files modified:** `scripts/check-10-idi10-validation.py`
- **Verification:** 复跑 `--item t1` / `--item t2` ⇒ 两个项均 0 FAIL / 0 BLOCKED / exit=0,且每个对的两个读数都打印出非空的原始值
- **Committed in:** `b4fe65d`

**3. [Rule 1 - Bug] 「两档不塌」写成等值断言,恒 FAIL**
- **Found during:** Task 2 第二次运行 `--item t1`
- **Issue:** 「`--color-border-subtle` 解析值 != `--color-surface`」这条不等式判据被误用了 `ok()`(等值比较)⇒ 实测值 `rgb(217, 217, 217)` 与期望串 `!= rgb(249, 249, 249)` 永不相等,报 1 条 FAIL。
- **Fix:** 改用 `ok_true()` 并显式写出条件 `tokens["subtle"] != tokens["surface"] and tokens["subtle"] is not None`。
- **Files modified:** `scripts/check-10-idi10-validation.py`
- **Verification:** 复跑 ⇒ `t1: PASS (53 条断言,0 FAIL,0 BLOCKED)`,exit=0
- **Committed in:** `b4fe65d`

---

**Total deviations:** 3 auto-fixed(3 Rule 1 —— 全部是**本次新建的探针脚本自身**的缺陷,零产品代码改动)
**Impact on plan:** 三条都发生在 Task 2 的首次运行与第二次运行之间,未改变任何交付物的形态或范围 —— 产品侧只有 `frontend/style.css` 的三处改动(一条声明就地改写、一条规则块追加、一段注释),与计划逐字一致。三条的共同教训:**探针自身的缺陷会让一次真实的 PASS 退化成 BLOCKED 或 FAIL**;本项目已登记的「先怀疑自己的探针」在这里第三次生效。

## Issues Encountered

- **`gsd-tools windows append` 被拒**(与 STATE.md 已登记的既有不一致相同):`Error: Ledger table in .planning/WINDOWS.md disagrees with the fenced JSON entries … for row id(s): 17`。三条探针缺陷因此**未入账到 WINDOWS.md**(该命令退出码为 0 且 `.planning/WINDOWS.md` **零字节改动**,已用 `git status --porcelain` 核实),改记于本 SUMMARY 与 STATE.md,沿 `idi-08-03` 先例记为已知限制而非回填。
- **`state.add-blocker` 的 `--text-file` 入参被路径守卫拒绝**(`Path escapes allowed directory: /private/tmp/…`)—— 改用内联 `--text`。**新增事实:凡 `--*-file` 入参,文件必须落在仓库内。**
- **`state.*` 动词第十二次复现**,本次 `advance-plan` 把 `completed_phases` 1 → 0、`percent` 43 → 0,并把 `state.json` 的 `next.reason` 从 `43%` 改成 `0%`;`update-progress` 仍然零写入。已按 ROADMAP 的 `## Milestones` + `## Progress` 手工校正回 `completed_phases: 1` / `percent: 43` 与 `state.json` 的 `43%`。**随后发现新的失效顺序**:手工校正之后,`state.record-session` **又把它压回 `0` / `0`** ⇒ 该字段的破坏是累加式的、且能跨越一次人工校正。第二次校正落在 `5cf6a73`。⇒ **核盘必须放在收口序列的最后一个动词之后,不能插在中间**;判据仍取 ROADMAP,不采信任何 `state.*` 动词的回显。两次形态都已逐条登记进 STATE.md 的 Blockers 段(`advance-plan` 也会打坏派生计数,此前该症状只记在 `update-progress` / `record-session` / `phase.complete` 名下)。
- **`roadmap.update-plan-progress idi-10` 的两处确定性格式副作用**已按既有登记手工修复:Progress 行尾格 `| In Progress|  |` → `| In Progress | - |`;`**Plans**: 4 plans` 被改写成 `**Plans**: 0/4 plans executed` ⇒ 改回。该动词本身已按流程运行,其输出结果(Phase 10 表格行 = `1/4 | In Progress`)与磁盘现状一致。
- **`requirements.mark-complete TABLE-01 TABLE-02` 被共享-ID 门(#2388)按设计拦下**:`requirements.ready-ids` 实测返回 `0/2 ready` —— `idi-10-03-PLAN.md` 的 frontmatter 也声明了这两条。故本计划**不写** REQUIREMENTS.md,勾选由计划 03 的 SUMMARY 触发。这不是缺口。

## Known Stubs

None —— 本计划未引入任何 stub、占位文案或硬编码空值。新增脚本的每个断言都有真实的读数来源;`TABLE_PROBES` 的 5 个对全部实测注入成功(`td` 计数均为 6),无一对因「凑绿」被删减。

## Threat Flags

None —— 本计划的改动面是 `frontend/style.css` 的**呈现层**声明加一个**只读**的本地运行时门。新增声明只有 `background: var(--color-surface);` 与 `border-bottom`,`git diff -U0 8bfe4f9^ 8bfe4f9` 的新增行里不含 `url(` / `@import` / 任何网络引用;门脚本走 `c05.make_fixture`(在 `tempfile.mkdtemp()` 下 `copytree` 出副本,原 `scripts/ui-states/` 零改动,已用 `git status --porcelain scripts/ui-states/` 核实为空),临时根目录在 `finally` 里 `shutil.rmtree`。零新增依赖、零构建步骤、零新增第三方包(`frontend/vendor/` 仍只有 `marked.min.js`)。

## Next Phase Readiness

- **计划 02(圆角刻度收敛)可以开工**:它要复用的门骨架已就位 —— `ITEMS` 派发表、`parse_args()`、`main()` 的服务生命周期 + Playwright 启动 + `=== 逐项结论 ===` 汇总 + 退出码语义、`run_screenshots()`、`load_check05()` / `png_size()` / `fence_text()` 都已落地且经实跑验证;计划 02 只需追加 `r1` / `r2` / `radius_snapshot()` / `--radius-snapshot {before,after}` 并扩展 `RADIUS_LITERALS`。
- **计划 03 可直接消费 `--screenshot <DIR>`**:实测输出恰 5 张 1440×900 PNG,与 `c05.STATES` 逐项一一对应,逐张断言宽高。
- **`t1` / `t2` 是计划 02 的回归护栏**:圆角改动落地后须复跑 `--item t1 --item t2`,证明表格的两处改动未被顺手带偏(尤其 `td` 的 `font-size`,它被 `check-05:1126` 的活断言锁死)。
- **待决出口**:D3(视觉档位是否真读作「白卡片内的一个内陷块」)是唯一的人工判断项,入口是计划 03 的 5 张截图;本计划不代其收口。

## Self-Check: PASSED

- `frontend/style.css` 存在于盘,`git log --oneline --all` 含 `8bfe4f9`(Task 1)与 `b4fe65d`(Task 2)
- `scripts/check-10-idi10-validation.py` 存在于盘并可被 `.venv/bin/python` 直接运行
- 四个静态门 + 新门的四条 verify 命令全部实跑通过(原始输出见上)
- `git status --porcelain frontend/` 仅 `frontend/style.css`;`git status --porcelain scripts/` 仅新增 `scripts/check-10-idi10-validation.py`;`git status --porcelain scripts/ui-states/` 为空

---

*Phase: idi-10-tables-and-radius-scale*
*Completed: 2026-09-27*

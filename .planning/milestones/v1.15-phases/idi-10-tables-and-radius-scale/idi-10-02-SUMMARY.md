---
phase: idi-10-tables-and-radius-scale
plan: 02
subsystem: ui
tags: [css, design-tokens, radius, visual-regression, playwright, runtime-gate]

# Dependency graph
requires:
  - phase: idi-10-tables-and-radius-scale
    provides: 运行时门骨架 scripts/check-10-idi10-validation.py(t1 / t2 + --screenshot / --json / --keep)、表格规则改造(表头 gray-2 浅底 + 仅横向分隔线)
provides:
  - 圆角刻度收敛为三档 8 / 10 / 999 —— 围栏内 --radius-lg 一行被删除,全文零出现、零 var() 引用
  - .chat-user → var(--radius-md)(卡片档,本阶段唯一外观真变的消费者;border-bottom-right-radius: var(--radius-sm) 尖角逐字保留)
  - "#chat-input-row input → var(--radius-pill)(胶囊档,如实登记;外观零变化)"
  - 运行时门新增 r1 / r2 两个断言集(10 + 9 条断言)与 RADIUS_LITERALS / RADIUS_CORNER_PROPS 常量
  - "--radius-snapshot {before,after} DIR 单元素取证模式 + radius_snapshot();产出四份并排取证(computed style dump / rect / 元素 PNG / 源码 sha256)"
affects: [idi-10-03, idi-10-04]

# Actuals (#2632) —— 同一 estimateTokens 口径(chars/4 over the realized diff)。
# 方法经波次 1 校准:git diff <plan_head_before>..<末个任务提交> -- frontend/style.css
# scripts/check-10-idi10-validation.py | wc -c,再除 4(波次 1 同法得 26746/4 = 6686,
# 与其 actuals.tokens 逐字相符)。仅计**手写**的两个文件,不含自动生成的 JSON / PNG 取证产物。
actuals:
  tokens: 6003
  tasks: 3
  commits: 3
plan_head_before: 26b4f60cb0ee8fa92b1619a794f20bf89bb65e6c

tech-stack:
  added: []
  patterns:
    - "外观零变化必须**测量**而非推断:收敛前后各取一次真实读数(整份 computed style dump + getBoundingClientRect() + 元素级 PNG + 捕获时源码 sha256),再做键级 diff / 矩形逐值 / PNG 逐字节三项并排比对"
    - "两份取证的源码 sha256 必须不同 —— 这是「两次真实读数,不是同一次复制两份」的可复核凭据"
    - "逐角读物理长手而非简写:同一批圆角判据要覆盖带 border-bottom-right-radius 的规则体时,Chrome 会把简写序列化成三值,`== \"10px\"` 这类断言不可满足"
    - "造出容器再断言 + 每次读数前重建:探针节点不在 fixture 里时,任何重新导航都会清掉它,只在开头造一次会让后续读数落空"

key-files:
  created:
    - .planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/input-radius-before.json
    - .planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/input-radius-before.png
    - .planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/input-radius-after.json
    - .planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/input-radius-after.png
  modified:
    - frontend/style.css
    - scripts/check-10-idi10-validation.py

key-decisions:
  - "删令牌而非保留 --radius-lg:围栏的 D-04 / Hard Rule 5 明写 never declare a token you are not consuming —— 消费者搬走后不得留下未消费的声明"
  - "两处消费者去向**不同**是承重点,不得统一:.chat-user → var(--radius-md)(它真的是大圆角气泡,28px → 10px 外观真变);#chat-input-row input → var(--radius-pill)(min-height: 52px 下 28px 早已被 UA 钳制,它实际就是一个胶囊,改记是如实登记)"
  - "围栏内注释以「28px 那一档 / the former fourth step」指代被删档位,**不写**字面量令牌名 —— 那是「围栏内计数 == 0」与「全文计数 == 0」两条判据的共同锚点"
  - "r1 的 .chat-user 读数一律取四个**物理角长手**并逐角独立断言,不读简写:该规则体带 border-bottom-right-radius,Chrome 把简写序列化成三值(实测收敛后为 '10px 10px 8px'),「简写 == 卡片档」这条断言永远不可满足"
  - "r1 另立一条「四角并非统一」断言,使「保留尖角」这条判据可失败 —— 否则它会被三条等值断言悄悄吃掉"
  - "「输入框外观零变化」的判据是 radius-snapshots/ 里收敛前后的三份并排读数(测量),不是「28px 会被钳成胶囊」这条算术(ROADMAP Pitfalls 第 2 条明令)"
  - "compute-style 的允许差异键集合必须按计划自己写下的原则扩到 9 个:8 个圆角键 **加上**被删令牌自身的键 —— 实测该迭代名单包含 121 个继承来的自定义属性键,被删的 --radius-lg 正是其中之一(见 Deviations)"

patterns-established:
  - "「外观零变化」的机器化形态 = 键级 computed style diff 的允许集合 + 矩形逐值 + 元素 PNG 逐字节;三者缺一不可,且允许集合必须覆盖预期改动能改到的**每一个**属性(含被删令牌自身)"
  - "被删令牌自身的 computed style 键会随令牌一起消失,故它必须出现在允许差异键集合里 —— 用合成 page.set_content 探针页测不出这件事(那里没有 :root 继承),只有真实 fixture 才看得见"

requirements-completed: [RADIUS-01, RADIUS-02]

coverage:
  - id: D1
    description: "圆角刻度收敛为三档 8 / 10 / 999:围栏内 --radius-lg 声明被删除、全文零出现、零 var() 引用;--radius-sm / --radius-md / --radius-pill 三行值逐字未变;围栏内无未消费的令牌声明"
    requirement: "RADIUS-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-10-idi10-validation.py --item r1"
        status: pass
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2"
        status: pass
      - kind: other
        ref: "grep -cF -- '--radius-lg' frontend/style.css == 0;awk <fence> | grep -cF == 0;grep -o -- 'var(--radius-lg)' | wc -l == 0(三条独立判据)"
        status: pass
    human_judgment: false
  - id: D2
    description: ".chat-user 的四个物理角长手中 TL / TR / BL == 解析后的 --radius-md(卡片档)、BR == 解析后的 --radius-sm(8px 尖角保留);选择器文本与其余四行声明逐字未变,且规则体上方带承重注释写明「不得与输入框统一」"
    requirement: "RADIUS-02"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-10-idi10-validation.py --item r1(.chat-user 探针气泡由应用自身的 appendChatMessage('user', …) 造出)"
        status: pass
    human_judgment: false
  - id: D3
    description: "#chat-input-row input 的计算 border-radius == 解析后的 --radius-pill(999px)、四角长手等值,min-height 仍为 52px、border-top 仍为 1px solid;且其**外观与收敛前一致**"
    requirement: "RADIUS-02"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-10-idi10-validation.py --item r2"
        status: pass
      - kind: automated_ui
        ref: "radius-snapshots/input-radius-before.{json,png} vs input-radius-after.{json,png}:键级 diff ⊆ 8 圆角键 ∪ {--radius-lg}、rect 逐值相同、cmp -s 两张 PNG 返回 0"
        status: pass
    human_judgment: false
  - id: D4
    description: "运行时门的圆角覆盖:r1 / r2 两个断言集在真实浏览器里全 PASS、0 BLOCKED,且波次 1 的 t1 / t2 未被打破"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-10-idi10-validation.py --item r1 / --item r2 / --item t1 --item t2"
        status: pass
    human_judgment: false
  - id: D5
    description: ".chat-user 由 28px 大圆角气泡变为 10px 卡片圆角 —— 这是本阶段唯一**外观真的变了**的消费者,它的观感是否与 Phase 9 的卡片语言同族,只有人眼能判"
    verification: []
    human_judgment: true
    rationale: "计算样式能证明「TL/TR/BL == 10px 且 BR == 8px」,不能证明那个形态读起来是卡片档气泡而不是被削平了一块。计划 03 的 5 张 1440×900 截图是本条的评审入口(ROADMAP SC4 点名「须在截图里可见」)。"

duration: 9 min
completed: 2026-09-27
status: complete
---

# Phase 10 Plan 02: 圆角刻度收敛(8 / 10 / 999)与前后并排运行时取证 Summary

**圆角刻度由 8 / 10 / 28 / 999 收敛为 8 / 10 / 999:删掉从未并入刻度的 `--radius-lg: 28px`,两处消费者按各自真实形态就地改归属(`.chat-user` → 卡片档 10px、`#chat-input-row input` → 胶囊档 999px),并以收敛前后的真实运行时读数(键级 computed style diff + 矩形逐值 + 元素 PNG 逐字节)证明输入框外观零变化**

## Performance

- **Duration:** 9 min
- **Started:** 2026-09-27T11:34:05Z
- **Completed:** 2026-09-27T11:43:04Z
- **Tasks:** 3
- **Files modified:** 2 手写(`frontend/style.css` +12 / −4、`scripts/check-10-idi10-validation.py` +147 / −3)+ 4 份新取证产物

## Accomplishments

- `frontend/style.css` 围栏内**删掉整行** `--radius-lg: 28px;`,并把上方注释由 `four values` 改写为 `three values` 且逐条记下三件事:被删的是 28px 那一档、它由 quick `260918-qrq` 的临时视觉 pass 手调引入且从未并入任何刻度声明(`04-UI-SPEC.md` 的圆角账本至今写着 `4px / 8px / 999px`)、它的两处消费者去向不同、以及删而非留的依据(Hard Rule 5)。注释里**不出现**字面量令牌名 —— 那会让两条 `grep == 0` 判据同时红
- `.chat-user` 的 `border-radius` 由 `var(--radius-lg)` **就地**改为 `var(--radius-md)`(卡片档,10px);`border-bottom-right-radius: var(--radius-sm)`(8px 气泡尾巴尖角)逐字保留;规则体上方新增一段承重注释写明「本元素是本阶段唯一外观真变的消费者」且**不得**与输入框统一
- `#chat-input-row input` 的 `border-radius` 由 `var(--radius-lg)` **就地**改为 `var(--radius-pill)`(胶囊档,999px);其余六行声明(含 `min-height: 52px`)逐字未变;上方新增一段承重注释,明确「外观零变化」的判据是 `radius-snapshots/` 的三份并排读数而不是那条钳制算术
- 两处改动都是**就地改归属**:选择器文本与规则块位置逐字未变,零规则块搬迁、零追加覆盖规则、零 `--radix-` 增删行
- `scripts/check-10-idi10-validation.py` 新增 `r1` / `r2` 两个断言集(实跑 10 条 / 9 条断言,均 0 FAIL / 0 BLOCKED)与 `--radius-snapshot {before,after} DIR` 单元素取证模式;`ITEMS` 增为四键;`--item` 帮助文本与文件头的需求映射同步更新
- 圆角刻度的渲染判据**首次**有了自动化运行时覆盖 —— 在此之前,`check-06-idi05-validation.py:224` 读 `borderTopLeftRadius` 但**只经 `info()` 打印、不断言**,其余门与探针零圆角断言
- 四份并排取证落盘于 `.planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/`,两份 JSON 各带捕获时 `frontend/style.css` 的 sha256(`c6c06436…` vs `4e783086…`,**不同**)

## Task Commits

Each task was committed atomically:

1. **Task 1: 给门追加 `--radius-snapshot {before,after} DIR` 取证模式,并在 HEAD 状态取「收敛前」读数** - `37207ac` (feat)
2. **Task 2: 删除 `--radius-lg` + 两处消费者按各自真实形态就地改归属 + 取「收敛后」读数并做三项并排比对** - `6349b2e` (feat)
3. **Task 3: 给门追加 `r1` / `r2` 断言集** - `4239717` (feat)

**Plan metadata:** 见本次收口的 docs 提交

## Files Created/Modified

- `frontend/style.css`(+12 / −4)- 围栏内删 1 行声明 + 改写 1 段围栏内注释;`.chat-user` 与 `#chat-input-row input` 各就地改 1 处 `border-radius` 值 + 各新增 1 段围栏外承重注释
- `scripts/check-10-idi10-validation.py`(+147 / −3)- 新增 `RADIUS_SNAPSHOT_SEL` / `RADIUS_SNAPSHOT_LABELS` / `RADIUS_TOKENS` / `RADIUS_CORNER_PROPS` / `RADIUS_LITERALS` / `_SNAPSHOT_JS` / `radius_snapshot()` / `r1()` / `r2()`;`parse_args()` 增 `--radius-snapshot`;`main()` 增派发与汇总项
- `.planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/input-radius-before.{json,png}`(21480 / 5255 字节)
- `.planning/phases/idi-10-tables-and-radius-scale/radius-snapshots/input-radius-after.{json,png}`(21480 / 5255 字节)

## Gate Evidence(原始输出,不是摘录)

```
$ grep -cF -- '--radius-lg' frontend/style.css
0        # rc=1(grep 恰在零命中时退 1)
$ awk '/===== DESIGN TOKENS: START/{f=1} f{print} /===== DESIGN TOKENS: END/{f=0}' frontend/style.css | grep -cF -- '--radius-lg'
0        # rc=1;同一条 awk 管道不加 grep 时输出 691 行(围栏确实被取到,不是空管道假绿)
$ grep -o -- 'var(--radius-lg)' frontend/style.css | wc -l
0
$ grep -nF -- '--radius-sm: 8px;' frontend/style.css; grep -nF -- '--radius-md: 10px;' frontend/style.css; grep -nF -- '--radius-pill: 999px;' frontend/style.css
412:  --radius-sm: 8px;
413:  --radius-md: 10px;
414:  --radius-pill: 999px;
$ grep -nF -- 'Radius — four values' frontend/style.css
# rc=1(零命中 —— 注释已改写为 three values)
```

```
$ bash scripts/check-01-token-conformance.sh
PASS
$ bash scripts/check-03-hidden-uniqueness.sh
PASS
$ bash scripts/check-04-important-count.sh
PASS
$ .venv/bin/python scripts/check-02-contrast.py   # 末行
PASS: 0 failures
# 表头新绘制面的既有条目本次实跑原文:PASS  15.48  --color-text on --color-surface
# 圆角收敛不涉色 ⇒ PAIR / ORDER 计数仍为 53 / 1(与改动前逐字相同)
```

```
$ .venv/bin/python scripts/check-09-idi09-validation.py --item c1 --item c2
item c1: PASS  (26 条断言,0 FAIL,0 BLOCKED)
item c2: PASS  (13 条断言,0 FAIL,0 BLOCKED)
exit=0
# 该门动态解析 --radius-md 做卡片圆角断言 ⇒ 它是「不得删 --radius-md」这条禁令的探测器
```

```
$ .venv/bin/python scripts/check-10-idi10-validation.py --item r1
INFO r1 令牌解析: --radius-sm=8px --radius-md=10px --radius-pill=999px
INFO r1 .chat-user 四个物理角长手原始读数(诊断): border-top-left-radius=10px / border-top-right-radius=10px / border-bottom-left-radius=10px / border-bottom-right-radius=8px
INFO r1 .chat-user 简写 border-radius(显式 getPropertyValue,仅诊断、不断言): '10px 10px 8px'
item r1: PASS  (10 条断言,0 FAIL,0 BLOCKED)
exit=0

$ .venv/bin/python scripts/check-10-idi10-validation.py --item r2
INFO r2 原始读数: border-top-left-radius=999px / border-top-right-radius=999px / border-bottom-left-radius=999px / border-bottom-right-radius=999px / 简写 border-radius=999px / min-height=52px / border-top=1px solid
item r2: PASS  (9 条断言,0 FAIL,0 BLOCKED)
exit=0

$ .venv/bin/python scripts/check-10-idi10-validation.py --item t1 --item t2
item t1: PASS  (53 条断言,0 FAIL,0 BLOCKED)
item t2: PASS  (46 条断言,0 FAIL,0 BLOCKED)
exit=0        # 波次 1 的表格判据未被本阶段打破
```

## 前后并排取证:四份产物与三项比对

两份 JSON 的顶层键为 `label` / `selector` / `computed` / `rect` / `tokens` / `style_css_sha256`。

| 读数 | before(HEAD 状态) | after(收敛后) |
|---|---|---|
| `tokens["--radius-sm"]` | `8px` | `8px` |
| `tokens["--radius-md"]` | `10px` | `10px` |
| `tokens["--radius-lg"]` | **`28px`** | **`None`**(令牌已不存在) |
| `tokens["--radius-pill"]` | `999px` | `999px` |
| `computed` 的四个物理角长手 | 均 `28px` | 均 `999px` |
| `computed` 键数 | **599** | **598** |
| `rect` | `x=137 y=406.5 w=664 h=52` | 逐值相同 |
| 元素 PNG | 664×53,sha256 `190d7d7d…` | 664×53,sha256 `190d7d7d…` |
| `style_css_sha256` | `c6c06436f77271b5265c4071b6b560f534b090416027e00d30d363ef9a6f6afd` | `4e7830863522f7b5437942eb8f0d03e7b9962b59022b05dd0d8038c9725783e8` |

**三项并排比对(全部通过):**

| # | 判据 | 命令 | 实测 |
|---|---|---|---|
| (a) | computed style 键级 diff | 见下「允许集合」段 | 差异键恰 **9** 个:8 个圆角键 + 被删令牌自身的键;集合外 **0** 个键变化 |
| (b) | 矩形逐值相同 | `b['rect'] == a['rect']` | `True`(布局零变化) |
| (c) | 元素截图逐字节相同 | `cmp -s input-radius-before.png input-radius-after.png` | `rc=0`,两张 PNG 的 sha256 均为 `190d7d7d0299e38d0dd915dc941beafccf43f9ebd5a3721c979a13f9921d4a35` |

**两条必须先读的口径说明(否则会误读上面的数字):**

1. **`getComputedStyle` 返回的是计算值,不是被钳制后的使用值。** 四个物理角长手读到的 `28px`(before)/ `999px`(after)是**声明解析结果**;「外观零变化」这件事**不是**从这个数字读出来的,而是由 (b)(c) 两项测量承担 —— (c) 的逐字节相同才是直接证据。ROADMAP Pitfalls 第 2 条明令不得用「28px 会被钳成胶囊」这条算术替代测量,本计划即按此执行。
2. **「收敛前」快照取自波次 1 落地之后。** 计划 01 改过 `frontend/style.css`(表格规则),但它不碰圆角层 ⇒ 该元素的计算圆角在计划 01 前后逐值相同。故 before / after 这一对**干净地隔离了本计划的圆角改动**。

### (a) 的允许差异键集合:9 个,而不是计划字面的 8 个

计划 Task-2 第 6 步把允许集合写成「八个圆角相关键」(四个物理角长手 + 四个逻辑别名)。实测差异键是**九个** —— 那八个**加上被删令牌自身的键**:

```
$ python3 -c "... 计划原文的比较式 ..."
['--radius-lg', 'border-bottom-left-radius', 'border-bottom-right-radius', 'border-end-end-radius', 'border-end-start-radius', 'border-start-end-radius', 'border-start-start-radius', 'border-top-left-radius', 'border-top-right-radius']
rect_equal True
subset False          # ← 字面判据在此为 False,原因只有一个:--radius-lg
corners True
sha_changed True
```

```
$ python3 -c "... 允许集合 = 8 个圆角键 ∪ {--radius-lg} ..."
subset(9) True   corners True   rect_equal True   sha_changed True
outside_radius []        # 集合之外**零个**键发生变化
```

根因是**测量面的事实**,不是实现缺陷:`for (const name of cs)` 走的是 `CSSStyleDeclaration` 的迭代名单,在真实 `p1` fixture 上它**包含 121 个继承来的自定义属性键**(`--color-action-commit`、`--radius-*` 等),而 `#chat-input-row input` 从 `:root` 继承 `--radius-lg`。令牌被删除 ⇒ 该键随之消失 ⇒ 键数 599 → 598。这是**预期改动本身**,不是「改动溢出」。

判据取计划**自己写下的原则**(Task-2 第 6 步 (a) 的说明句):「允许差异键集合**必须覆盖预期改动能改到的每一个属性**」。按该原则,被删令牌自身的键必须在集合内。故这是**按计划的原则修正集合的枚举**,不是放宽不变量:集合之外仍然一个键都不许变(实测 `outside_radius == []`)。

⚠ **这条事实用合成 `page.set_content` 探针页测不出来**(那里没有 `:root` 继承,故没有自定义属性键),只有真实 fixture 才看得见 —— 计划里那句「实测恰 477 个长手名」也是同一个合成页的产物(真实 fixture 实测 **599**)。两处偏差同源。

## Decisions Made

- **`--radius-md` 不得删,且用一道门把它钉住** —— `scripts/check-09-idi09-validation.py` 动态解析该令牌做卡片圆角断言(令牌相对 ⇒ 改值不破;**删该令牌会破**)。本计划把该门显式纳入 Task 2 与 Task 3 的 `<verify>`,实跑 `c1/c2` 仍 `exit=0`。
- **r1 逐角独立断言而不是「四角等值」一条带过** —— 标签里写清哪一个角是尖角,并另立一条「四角并非统一」断言。否则「保留 8px 尖角」这条判据会被三条等值断言悄悄吃掉。
- **r1 的简写读数只作诊断** —— 用 `getPropertyValue('border-radius')` 显式取,写进 `info()` 而不作断言(实测 `'10px 10px 8px'`,三值形态正是 `border-bottom-right-radius` 的序列化结果)。
- **`--radius-snapshot` 作为一项进入 `=== 逐项结论 ===`** —— 取证失败必须让门红,不能静默;标签校验放在 `main()` 开头(起浏览器之前),使非法标签 fail-fast。
- **before / after 的快照由**同一次运行语义**下取得** —— 同一个脚本、同一个选择器、同一段「先失焦再读」的代码路径;两份 JSON 的 `style_css_sha256` 不同即证明是两次真实读数。
- **未把三项比对写进门脚本** —— 计划把 (a)(b)(c) 定为**取证协议**(由产物 + 独立复核承担),没有要求新增 `--radius-compare` 模式;本计划不加(避免越出计划的交付面)。

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] 计划的允许差异键集合在真实 fixture 上少枚举了 1 个键(被删令牌自身的键)**
- **Found during:** Task 2 第 6 步(三项并排比对)
- **Issue:** 计划把允许集合写成「八个圆角相关键」。实测差异键是九个 —— 那八个**加上 `--radius-lg`**:`CSSStyleDeclaration` 的迭代名单包含**继承来的自定义属性键**(真实 `p1` fixture 上实测 121 个),而该元素从 `:root` 继承 `--radius-lg`;令牌被删 ⇒ 该键消失 ⇒ `computed` 键数 599 → 598。计划字面的 `subset` 判据因此为 `False`。
- **Fix:** 按计划**自己写下的原则**(「允许差异键集合必须覆盖预期改动能改到的**每一个**属性」)把集合扩到 9 个。**不变量未被放宽**:集合之外仍然一个键都不许变,实测 `outside_radius == []`。同时把「简写/迭代名单」这条事实的注释写进 `_SNAPSHOT_JS` 上方(按 orchestrator 的实测口径记 **599**,不记计划里那个来自合成探针页的 477 —— 两者差 122,差值恰是继承来的自定义属性键数)。
- **Files modified:** 无(这是一条**取证协议**的判据修正;产品代码与门脚本都未因它改动)
- **Verification:** 计划字面式输出 `subset False`(唯一超集外键即 `--radius-lg`);修正式输出 `subset(9) True / corners True / rect_equal True / sha_changed True / outside_radius []`
- **Committed in:** 不适用(零文件改动;证据在 `radius-snapshots/` 的两份 JSON 里,已随 `6349b2e` 落盘)

**2. [Rule 1 - Bug] 计划的两处「工作树里应有未提交改动」前提与逐任务提交的执行方式冲突**
- **Found during:** Task 1 第 5 步与 Task 3 第 5 步
- **Issue:** 两处判据的字面 `fails_when` 建立在「波次 1 的 `style.css` 改动仍在工作树里」这个前提上:(a) Task 1 的 `git status --porcelain frontend/` 要求「输出非空且只含 `frontend/style.css`」;(b) Task 3 的 `git diff -- frontend/style.css` 要求「不得为空」。但波次 1 的三处改动**已提交**(`8bfe4f9`),而本计划按 `<task_commit_protocol>` 逐任务提交 ⇒ 工作树在这两处判据运行时不可能是脏的。两条字面判据因此**不可满足**。
- **Fix:** 按**判据的意图**取证,不为了凑非空而制造改动:(a) 取 `git diff -- frontend/style.css` 为空(证明本任务零 CSS 改动)+ `git status --porcelain frontend/` 为空(工作树干净 ⇒ 更严格);(b) 取 `git diff --stat 26b4f60 -- frontend/style.css`(相对**计划基线**)为 `+23 / −4`,证明 `style.css` 确实带着本计划的圆角收敛。
- **Files modified:** 无(取证方式修正,零代码改动)
- **Verification:** (a) `git diff -- frontend/style.css` 输出 0 行;(b) `git diff --stat 26b4f60 -- frontend/style.css` → `1 file changed, 23 insertions(+), 4 deletions(-)`,且 `-U0` 的行级 diff 恰为「删 1 行声明 + 改 1 段围栏内注释 + 改 2 处 `border-radius` 值 + 新增 2 段围栏外注释」,无任何规则块搬迁、零 `--radix-` 增删行
- **Committed in:** 不适用(零文件改动)

---

**Total deviations:** 2 auto-fixed(2 Rule 1 —— 均为**计划文本的判据与磁盘现实不符**,零产品代码改动、零范围变化)
**Impact on plan:** 两条都不改变任何交付物的形态或范围。第 1 条修正的是取证协议的允许集合(不变量强度不变);第 2 条修正的是取证方式(判据意图不变)。两条的共同成因:**计划里的若干「实测」数字取自合成 `page.set_content` 探针页或「改动尚未提交」的假设**,与真实 fixture / 逐任务提交的执行方式不符 —— orchestrator 已在派发说明里预警 477→599 这一处,本计划实测确认并补齐了其余同源处。

## Issues Encountered

- **`state.*` 动词第十三次复现,已逐条核盘修正(完整形态见 STATE.md 的 Blockers 段本次新增条目)。** ①`advance-plan` 正确写 `Plan: 2 of 4 → 3 of 4` 与 `completed_plans: 4 → 5`,但**再次把派生计数打坏**(`completed_phases` 1 → 0、`percent` 50 → 0),已按 ROADMAP 的 `## Milestones` + `## Progress` 手工校正回 `1` / `50`;②`update-progress` 仍然**零写入**,回显不可作为判据;③`record-metric` 正确追加,但计划号写法漂成 `Phase 10 P02`(既有惯例是 `Phase idi-10 P01`),已手工对齐;④`add-decision` **七条里只落盘六条** —— 第七条以 `--radius-snapshot` 开头被 flag 解析器拒绝,**新增事实:决策正文以 `-` 开头时必须改写首词(或用 `--summary-file`),否则该动词「部分成功」(退出码 1 但先前的条目已落盘)**;⑤`record-session` 正确写三行(丰富正文被压成一行,已手工补回);⑥`roadmap.update-plan-progress` 正确写 `2/4` 与两个 `[x]`,但**两处格式副作用**再现(Progress 行尾格掉内容、`**Plans**: 4 plans` 被改写),均已手工修回;⑦`state.json` 的 `next.reason` 同源打坏(`50%` → `0%`),已改回。**核盘放在收口序列的最后一个动词之后** —— 这条纪律本次再次生效。
- **`gsd-tools windows append` 被拒**(与 STATE.md 已登记的既有不一致逐字相同:`Ledger table in .planning/WINDOWS.md disagrees with the fenced JSON entries … for row id(s): 17`)。本计划的两条 deviation 因此**未入账到 `.planning/WINDOWS.md`**(该命令两次都返回上述错误、退出码 0,且该文件**零字节改动**,已用 `git status --porcelain .planning/WINDOWS.md` 核实),改记于本 SUMMARY 与 STATE.md,沿 `idi-08-03` / `idi-10-01` 先例记为**已知限制而非回填**。
- **RADIUS-01 / RADIUS-02 的勾选被共享-ID 门(#2388)按设计拦下** —— `idi-10-03-PLAN.md` 的 frontmatter 也声明了这两条,故 `requirements.ready-ids` 实测返回 **`0/2 requirement(s) ready to mark complete`**。⇒ 本计划**不写** REQUIREMENTS.md,勾选由计划 03 的 SUMMARY 触发。这不是缺口,是门前置行为(与波次 1 的 TABLE-01 / TABLE-02 逐字同形)。
- **未跑 pytest / check-05** —— 计划 02 的 `<verification>` 与 `<success_criteria>` 未要求它们(五条浏览器门复跑 + pytest 基线 + `node --check` 是**计划 03** 的收口 gate),且本计划对后端零改动、对 `scripts/check-05-ui-uat.py` 零改动。`td` 的 `font-size`(被 `check-05:1126` 活断言锁死的属性)由 `t2` 的对照组逐对断言覆盖。

## Known Stubs

None —— 本计划未引入任何 stub、占位文案或硬编码空值。新增的 `r1` / `r2` / `radius_snapshot` 每个断言都有真实的读数来源;`.chat-user` 的探针气泡由**应用自身的** `appendChatMessage('user', …)` 造出(真实渲染路径、零网络、零 AI 调用),`r1` 的 FAIL / BLOCKED 计数为 0 即证明每一次读数都读到了真实元素而非 `None`。取证产物里的 `computed` 是整份 dump(599 / 598 个键),不是抽样。

## Threat Flags

None —— 本计划的改动面是 `frontend/style.css` 的两处**呈现层**声明改归属 + 一个**只读**的本地运行时门。`git diff -U0` 的新增行里不含 `url(` / `@import` / 任何网络引用;`--radius-snapshot` 只**读** `frontend/style.css`(sha256)并只**写**调用方显式给定的产物目录(实测 `git status --porcelain frontend/` 为空、`git status --porcelain scripts/ui-states/` 为空、四份产物全部落在 `.planning/` 下);fixture 走 `c05.make_fixture`(`tempfile.mkdtemp()` 下 `copytree` 出副本,原 `scripts/ui-states/` 零改动),临时根在 `finally` 里 `rmtree`。零新增依赖、零构建步骤、`frontend/vendor/` 仍只有 `marked.min.js`。威胁 T-idi-10-03(不得删 `--radius-md`)与 T-idi-10-04(外观零变化须有可复核原始证据)两条 `mitigate` 项均已按其缓解计划落地并实跑验证。

## Next Phase Readiness

- **计划 03(门禁复跑 + 截图)可以开工**:`--screenshot <DIR>` 未被本计划改动(仍出 5 张 1440×900),`--item` 现支持四个取值;`check-10` 的四个断言集在真实浏览器里全 PASS、0 BLOCKED。
- **本计划给计划 03 留下一条**人工判断出口**(coverage 的 D5)**:`.chat-user` 由 28px 大圆角气泡变为 10px 卡片圆角是本阶段唯一外观真的变了的消费者,其观感只有人眼能判 —— 入口是计划 03 的 5 张截图(ROADMAP SC4 点名「须在截图里可见」)。
- **RADIUS-01 / RADIUS-02 的 REQUIREMENTS.md 勾选仍待计划 03 触发**(共享-ID 门)。
- **`radius-snapshots/` 的四份产物是本计划的独立复核入口**:任何复查者都可以用 `python3 -c` 重跑三项比对,不需要重跑浏览器。
- **待决出口**:计划 03 / 04 的收口 gate 与 `idi-09-VERIFICATION.md` 的连带重验(计划 04)。本计划不代其收口。

## Self-Check: PASSED

- `frontend/style.css` / `scripts/check-10-idi10-validation.py` / `radius-snapshots/` 的四份产物均存在于盘
- `git log --oneline --all` 含 `37207ac`(Task 1)/ `6349b2e`(Task 2)/ `4239717`(Task 3)
- 四个静态门 + `check-09 c1/c2` + `check-10` 的 `r1` / `r2` / `t1` / `t2` 全部实跑通过(原始输出见上)
- `git status --porcelain frontend/` 为空、`git status --porcelain scripts/ui-states/` 为空、`git diff -- scripts/check-05-ui-uat.py` 为空
- `commits: 3` 由 `git rev-list --count 26b4f60…HEAD` **实测**(非叙述)

---

*Phase: idi-10-tables-and-radius-scale*
*Completed: 2026-09-27*

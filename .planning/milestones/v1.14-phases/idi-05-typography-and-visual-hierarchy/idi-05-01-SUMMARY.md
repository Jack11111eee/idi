---
phase: idi-05-typography-and-visual-hierarchy
plan: 01
subsystem: ui
tags: [css, design-tokens, typography, font-scale, font-weight, line-height, playwright, uat, specificity]

# Dependency graph
requires:
  - phase: idi-04-tokens-contract
    provides: "围栏 `:root` 令牌层与 CHECK-01/02 四条守卫;`.markdown-body` 作用域规则(quick 260918-qrq);check-05 的 `ok()` BLOCKED 语义与 `resolve_token`/`resolve_color` 读取器"
provides:
  - "7 档字号刻度(`--text-2xl: 22px` / `--text-3xl: 28px`,插在 `--text-xl: 24px` 之后按名字序)"
  - "`.markdown-body h1/h2/h3` = `var(--text-3xl)` / `var(--text-2xl)` / `var(--text-lg)`(28 / 22 / 18px),四个宿主全部可达"
  - "三条 chrome 标题规则的选择器由后代形态收窄为 `#draft-view > h2` / `#round-title` / `#brainstorm-view > h2`"
  - "字重三档分工显式化:五只动作按钮 500,`#btn-authorize` / `#btn-divergence` 保持 600"
  - "check-05 item4 的 markdown 探针扩为四宿主 × 三档 + TYPE-02 两条运行时断言 + 六条字重断言(27 → 44 条)"
  - "围栏两处注释改写:字号档数 5 → 7(名同值不同警示)、行高整数配对 → 比率配对(`18/28` → `18/24`)"
affects: [idi-05-02, idi-05-03, idi-06, idi-07]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
# Same estimateTokens scale (chars/4 over the realized diff), never a harness token count.
actuals:
  tokens: 3601      # chars/4 over the realized diff of the two code files (14403 chars)
  tasks: 3
  commits: 3        # MEASURED: git rev-list --count 7f4f589..HEAD (2 task commits + 1 plan-metadata commit); base = executor-start HEAD, so Task 1's orchestrator commit 7f4f589 is not counted — see the note under Task Commits
  plan_head_before: 7f4f58982179793f500cb9b6027300abc6816da8

# Tech tracking
tech-stack:
  added: []        # 零新增依赖、零新增文件、零构建步骤(硬规则 6)
  patterns:
    - "CSS 层叠缺陷的机器化形态:chrome 侧选择器形态必须与 `.markdown-body` 侧一起被断言 —— 只守一侧时 1-0-1 后代选择器会反向压掉 0-1-1 的类规则"
    - "D-03 双类断言分类:本阶段主动改动的值走令牌接线(resolve_token 运行时解析),既有 chrome 字面 px 守卫保持字面(它们是唯一能抓到标题改动溢出到 chrome 的形态)"
    - "探针宿主集合必须覆盖影响面的全部实例 —— 只探一个宿主正是本阶段层叠缺陷存活到执行期的原因"

key-files:
  created: []
  modified:
    - frontend/style.css
    - scripts/check-05-ui-uat.py

key-decisions:
  - "D-07 命名冲突:`--text-2xl` 取 22px 而非契约 04-UI-SPEC 写的 18px —— 18px 已被 `--text-lg` 占用,改回会让 18px 有两个令牌名(第二事实源);围栏注释写明「名同值不同,不是笔误」"
  - "D-10 行高复用 `--lh-tight`,零新增令牌;整数配对在数学上不可得(28k 与 22k 同时为整数要求 k 是 0.5 的倍数,k = 1.5 太松),故改写为比率配对并单列 `--lh-compact` 为 chrome-only"
  - "D-08 TYPE-02 只复证、零 CSS 改动 —— 三处已由 quick 260918-qrq 归入刻度与令牌,为「有交付物」而重写会把正确状态改坏并使 `--text-base` 消费者计数漂移"
  - "D-12 `#btn-authorize` 是字重分工的唯一已登记例外(600):授权绝不与例行混同,四个强调通道此处用满"
  - "执行期新增(用户裁决):收窄三条 chrome 规则的选择器而非改用 id 作用域覆盖或重定 h2 目标 —— 这是「收窄既有规则的可达范围」,不是新增字号规则,且是 SC1 成立的前提"

patterns-established:
  - "层叠可达性断言:凡本阶段改动的字号,必须在**全部**受影响宿主上断言,而非规范宿主一处"
  - "探针串扩展优于新增探针:同一次 renderMarkdown 渲染出标题 / 代码跨度 / 表格 / 引用块,四条证据共用一条真实渲染路径"

requirements-completed: [TYPE-01, TYPE-02, TYPE-03]

# Coverage metadata (#1602)
coverage:
  - id: D1
    description: "7 档字号刻度落地,`.markdown-body h1/h2/h3` 在四个宿主(`#draft-content` / `#brainstorm-content` / `#round-doc` / `#latest-check`)上分别解析为 28 / 22 / 18px"
    requirement: "TYPE-01"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 4"
        status: pass
      - kind: unit
        ref: "bash scripts/check-01-token-conformance.sh"
        status: pass
    human_judgment: false
  - id: D2
    description: "围栏两处注释改写为真:字号档数 5 → 7(含「名同值不同」警示);行高整数配对 → 比率配对,既有算术错误 `18/28` 修正为 `18/24`,`four` 与三档配对的不自洽消解"
    requirement: "TYPE-01"
    verification:
      - kind: other
        ref: "grep -o '18/28' frontend/style.css | wc -l  →  0;grep -c '22/29.33' / '28/37.33' / '18/24' → 各 1;四条 --lh-* 声明逐字未变"
        status: pass
    human_judgment: false
  - id: D3
    description: "TYPE-02 复证成立且零 CSS 改动:`.markdown-body th/td` 与 `code` 仍为 `var(--text-base)`、`blockquote` 仍为 `var(--color-text-muted)`,由源断言 + 两条运行时令牌接线断言共同举证"
    requirement: "TYPE-02"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 4  →  td font-size / blockquote color 两条 PASS"
        status: pass
    human_judgment: false
  - id: D4
    description: "字重三档分工显式化:五只动作按钮 computed `font-weight` = 500,`#btn-authorize` = 600,`#btn-divergence` 保持 600;`--fw-medium` 消费者 4 → 8、`--fw-semibold` 12 → 8(无孤儿档)"
    requirement: "TYPE-03"
    verification:
      - kind: automated_ui
        ref: ".venv/bin/python scripts/check-05-ui-uat.py --item 4  →  六条 font-weight 断言全 PASS"
        status: pass
    human_judgment: false
  - id: D5
    description: "视觉层级判断:h1 > h2 > h3 三级标题可辨且不互相淹没(h1 28px 是全屏最大文字,> `.overlay-card h3` 的 24px > h2 的 22px);四处 chrome 标题在改动后仍不溢出各自容器、字号与色值未漂移"
    verification: []
    human_judgment: true
    rationale: "字号半边已由 check-05 的令牌接线断言与四条字面 px 守卫机器化覆盖,但「三级标题读起来层级分明、chrome 标题未被文档标题改动带偏」是视觉判断,不可由 computed style 数值还原;计划 must_haves 亦将其列为 backstop truth。"

# Metrics
duration: 20min
completed: 2026-09-21
status: complete
---

# Phase 5 Plan 01: 排版刻度 7 档 + 字重三档分工 Summary

**字号刻度 5 → 7 档(`--text-2xl` 22px / `--text-3xl` 28px),`.markdown-body` 的 h1/h2/h3 在全部四个宿主上落为 28/22/18px;三条 chrome 标题规则的选择器由 1-0-1 后代形态收窄为子组合器/自有 id,解开压掉文档 h2 的层叠缺陷;五只动作按钮字重 600 → 500,`#btn-authorize` 按 D-12 保持 600;围栏两处注释改写为真,`18/28` 算术错误修正为 `18/24`。**

## Performance

- **Duration:** 20min(含 Task 1 的停机与续跑;本次续跑从 `7f4f589` 起)
- **Started:** 2026-09-21T10:03:58+08:00(Task 1 提交时刻)
- **Completed:** 2026-09-21T10:26:00+08:00
- **Tasks:** 3/3
- **Files modified:** 2(`frontend/style.css`、`scripts/check-05-ui-uat.py`)

## Accomplishments

- **7 档字号刻度端到端落地**:围栏内 `--text-2xl: 22px;` / `--text-3xl: 28px;` 紧随 `--text-xl: 24px;` 之后按名字序插入;`.markdown-body h1/h2/h3` 三条 `font-size` 改为 `var(--text-3xl)` / `var(--text-2xl)` / `var(--text-lg)`。围栏标记仍恰为 1/1,围栏内 `--text-*` 声明数为 7,`--text-xl` 仍有 2 个消费者(无孤儿档)。
- **层叠缺陷修复(执行期用户裁决)**:`#draft-view h2, #rounds-placeholder h2` → `#draft-view > h2, #round-title`;`#brainstorm-view h2` → `#brainstorm-view > h2`。三条规则的**声明体逐字未动**,只有选择器行变化;`#rounds-placeholder > h2` 不可用(chrome 标题嵌在 `.round-view-header` 里,子组合器匹配不到),改用元素自有 id(1-0-0,仍胜过 `.round-view-header h2` 的 0-1-1)。
- **四个宿主全部达标**:`#draft-content` / `#brainstorm-content` / `#round-doc` / `#latest-check` 的 h1/h2/h3 在 `--item 4` 下逐条解析为 28 / 22 / 18px(12 条断言)。
- **字重三档分工显式化**:四行声明改动覆盖五只按钮(`#btn-approve-draft` / `#btn-process-round` / `#btn-start-writing` / `#btn-continue-check, #btn-continue-repair`)600 → 500。`--fw-medium` 消费者 4 → 8、`--fw-semibold` 12 → 8。`#btn-authorize`(D-12 唯一例外)与 `#btn-divergence`(琥珀族,不在六只之列)保持 600;八处 `:disabled` 的 `opacity`(0.55 × 6、0.5 × 2)逐字节未动。
- **TYPE-02 复证(零 CSS 改动)**:`.markdown-body th, .markdown-body td` 与 `.markdown-body code` 仍逐字为 `var(--text-base)`(L659 / L665),`.markdown-body blockquote` 的 `color` 仍逐字为 `var(--color-text-muted)`(L653);`--text-base` 消费者计数 19 保持不变。
- **围栏两处注释改写为真**:字号头注释 5 → 7 档并写明「契约的 `--text-2xl` 指 18px、本围栏指 22px —— 名同值不同,不是笔误」及数值序在 `xl(24) → 2xl(22)` 处不单调;行高头注释由「整数配对」改为「比率配对」,7 行配对表写全,既有算术错误 `18/28` 修正为 `18/24`(18 × 1.3333 = 24),`--lh-compact` 单列并注明 chrome-only。四条 `--lh-*` 声明逐字节未变。
- **断言面扩张**:check-05 item4 由 27 条(1 FAIL)扩为 **44 条**(0 FAIL / 0 BLOCKED)—— 四宿主 × 三档字号 12 条、TYPE-02 运行时 2 条、字重 6 条,其余为既有断言。

## Task Commits

Each task was committed atomically:

1. **Task 1 (tracer): 字号刻度两档端到端** - `7f4f589` (fix) — **由编排者在 blocking-human 门禁解除后提交,非执行器提交**
2. **Task 2: 行高注释改写 + TYPE-02 复证证据** - `b77b2f1` (docs)
3. **Task 3: 字重三档分工显式化** - `a0845bb` (feat)

**Plan metadata:** (docs: complete plan) — 本 SUMMARY 与 STATE/ROADMAP 的收口提交

### 关于 Task 1 的提交归属(不虚构任务提交)

Task 1 首次执行时 `--item 4` 报 `FAIL [p1] .markdown-body h2 font-size == var(--text-2xl): expected=22px actual=18px`,执行器按协议停在 `checkpoint:human-verify`(`gate="blocking-human"`)。根因由独立复测确认:三条 chrome 标题规则用**后代**选择器(1-0-1),会伸进 `.markdown-body` 容器把 `.markdown-body h2`(0-1-1)无条件压回 chrome 字号(ID 列胜过类列,与源码顺序无关)。实测 `#draft-content h2` 与 `#round-doc h2` 渲染 18px、`#brainstorm-content h2` 渲染 16px,只有 `#latest-check` 拿到 22px。

用户裁决「收窄 chrome 选择器」并授权修订 UI-SPEC 后,**由编排者提交了 `7f4f589`**,因此 Task 1 没有执行器侧的原子提交,本 SUMMARY 不为其虚构一条。本次续跑对 Task 1 只做验证、未重做:其 `<verify>` 与 `<acceptance_criteria>` 逐条复跑全绿(见下「验证证据」)。

`commits:` 的度量基点是执行器启动时的 HEAD(`7f4f589`),故计数为 2(仅本次续跑的两个任务提交);计划代码面的总改动量另见 `actuals.tokens`(以 `7f4f589^..HEAD` 的两个代码文件实现 diff 计)。

## Files Created/Modified

- `frontend/style.css` — 围栏内新增两档字号 + L204 字号头注释改写 + L217 行高头注释改写;`.markdown-body h1/h2/h3` 三条 `font-size` 改值;三条 chrome 规则选择器收窄(声明体逐字不动);四行动作按钮 `font-weight` 改值。**零新增文件、零依赖、零构建步骤。**
- `scripts/check-05-ui-uat.py` — item4 的 `MARKDOWN_HOSTS` 四宿主探针、`renderMarkdown` 探针串扩为「三级标题 + 代码跨度 + 表格 + 引用块」、十二条字号令牌接线断言、两条 TYPE-02 运行时断言、六条字重断言;`:742` 的 `#brainstorm-view h2` 断言按 D-02 改为令牌接线。六条 D-03 第二类字面 px 守卫保持不动。

## 验证证据(本次续跑逐条复跑,原始输出)

| 门 | 命令 | 结果 |
|---|---|---|
| CHECK-01 | `bash scripts/check-01-token-conformance.sh` | `PASS` / exit 0 |
| CHECK-02 | `python3 scripts/check-02-contrast.py \| tail -1` | `PASS: 0 failures` |
| CHECK-02 清单规模 | `… \| grep '^PASS  ' \| wc -l` | `43` |
| CHECK-02 序关系 | `… \| grep '^ORDER 0.363  --color-text-muted before --color-text on --color-surface' \| wc -l` | `1`(未变) |
| CHECK-03 | `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` |
| CHECK-04 | `bash scripts/check-04-important-count.sh` | `PASS` |
| UAT item 4 | `.venv/bin/python scripts/check-05-ui-uat.py --item 4` | `item 4: PASS (44 条断言,0 FAIL,0 BLOCKED)` / exit 0 |
| UAT smoke | `.venv/bin/python scripts/check-05-ui-uat.py --item smoke` | `item smoke: PASS (6 条断言,0 FAIL,0 BLOCKED)` / exit 0 |
| Gate 2 孤儿令牌 | `comm -23 <(var(--…) <(声明…)` | 输出为空 |
| Gate 3 改动面 | `git status --porcelain -- frontend/` | 只有 `frontend/style.css` |
| Gate 3 vendor | `ls frontend/vendor/` | 只有 `marked.min.js` |
| 零 diff 面 | `git diff --stat -- frontend/app.js frontend/index.html frontend/vendor/` | 空 |

Task 1 验收 grep 逐条复跑:`--text-2xl: 22px;` × 1、`--text-3xl: 28px;` × 1;`font-size: var(--text-3xl);` × 1、`var(--text-2xl);` × 1、`var(--text-lg);` × 2;后代形态 `^#draft-view h2|^#rounds-placeholder h2|^#brainstorm-view h2` **× 0**;`^#draft-view > h2, #round-title` × 1、`^#brainstorm-view > h2` × 1;`--text-*` 声明 × 7;围栏标记 1/1;全局 `h1, h2` 规则 **× 0**;`var(--text-xl)` × 2。

## Decisions Made

- **D-07 命名冲突按已锁决策执行**:`--text-2xl` 保持 22px,不「修正」回契约写的 18px —— 18px 已被 `--text-lg` 占用,改回会让 18px 有两个令牌名(第二事实源)。围栏注释写明名同值不同的理由与数值序不单调之处。
- **D-10 行高复用既有令牌、零新增**:整数配对在数学上不可得(28k 与 22k 同时为整数要求 k 是 0.5 的倍数,而 k = 1.5 太松:28 × 1.5 = 42px),故注释改为比率配对;`--lh-compact` 单列并注明 chrome-only(唯一消费者 `.overlay-card p`),消解 `four` 与三档配对的不自洽。
- **D-08 TYPE-02 零 CSS 改动**:只出证据。为「有交付物」而重写三处会把一个已经正确的状态改坏,并让 `--text-base` 的消费者计数漂移。
- **D-03 双类断言分类严格执行**:本阶段主动改动的值走令牌接线(`resolve_token` 运行时解析);`.panel-header h2` 14px / `#draft-view h2` 18px / `.overlay-card h3` 24px / `#draft-content` 16px / `.markdown-body code` 14px / `--text-base == "14px"` 六条保持字面 px —— 它们是唯一能抓到「标题改动溢出到 chrome」的形态。
- **字重断言写成对字面档值(500 / 600)的断言**:Chrome 把 `font-weight` 序列化为无单位数字串,与 `resolve_token` 读到的自定义属性值同形;实跑 `info()` 记录 `--fw-medium=500 --fw-semibold=600` 以供核对。
- **执行期新增(用户裁决,非执行器自选)**:收窄三条 chrome 规则的选择器形态。这是本阶段唯一被允许的选择器形态变更,且是 SC1 成立的前提 —— 不收窄则四个宿主里三个拿不到 D-06 的 22px。**未据此改动任何规则的先后位置**(硬规则 3)。

## Deviations from Plan

### Auto-fixed Issues

无。Task 2 与 Task 3 按计划原文执行,零自动修正。

### 计划执行期的停机(已登记的偏差,非自动修正)

**1. Task 1 `--item 4` FAIL → `checkpoint:human-verify`(blocking-human)**
- **发现于:** Task 1(字号刻度两档端到端)
- **问题:** 三条 chrome 标题规则用后代选择器(1-0-1)伸进 `.markdown-body`,无条件压掉 `.markdown-body h2`(0-1-1),四个宿主里三个拿不到 22px。缺陷在 HEAD 上早已存在,只是在 `.markdown-body h2` 也是 18px 时不可见。
- **处置:** 执行器按协议停机返回 checkpoint,不自行「修」。用户裁决收窄选择器并授权修订 UI-SPEC。修复由编排者提交为 `7f4f589`。
- **连带修订:** `idi-05-UI-SPEC.md` 的范围栅栏论证与「已知不一致」注记原文均被该缺陷证伪,已改写并附订正记录;`idi-05-01-PLAN.md` 新增 Task 1 第 3b 步、prohibition 1 加范围化豁免、prohibition 5 更新、step 4(a) 改为要求四个宿主、验收 grep 加 `^` 行首锚定。
- **登记:** `.planning/WINDOWS.md` #15(kind `deviation`,status `fixed`)
- **验证:** 本次续跑复跑 Task 1 全部 `<verify>` 与 `<acceptance_criteria>`,逐条通过(见「验证证据」)。

---

**Total deviations:** 0 auto-fixed;1 计划执行期停机(blocking-human,已由用户裁决并登记为 WINDOWS #15)
**Impact on plan:** 收窄选择器是 SC1 成立的前提,不是范围蔓延 —— 它收窄既有规则的可达范围而非新增规则。计划的三条需求(TYPE-01/02/03)全部关闭,无需求降级。

## Issues Encountered

- **单宿主探针是缺陷存活的直接原因。** item4 原只探 `#draft-content` 一个宿主,`#brainstorm-content`(16px)与 `#round-doc`(18px)的同类压制整片溜过。已把宿主集合提为模块常量 `MARKDOWN_HOSTS` 并作为 `page.evaluate` 的**参数**传入(不能在 JS 字符串里引用 Python 常量 —— 那段代码跑在浏览器里,引用会直接抛 `ReferenceError`),四个宿主逐个断言。
- **注释正文会让未锚定的 grep 多数。** 收窄后的规则注释里出现 `#draft-view > h2` / `#brainstorm-view > h2` 的散文引用,未加 `^` 时第三项得 2 而非 1。这是探针的错,不是 CSS 的错;验收命令已改为行首锚定。
- **无其他阻塞。**

## User Setup Required

None - no external service configuration required.

## Known Stubs

无。本次续跑未引入任何硬编码空值、占位文案或未接线的数据源。

## Threat Flags

无。本次改动只涉及 `frontend/style.css` 的声明值与 `scripts/check-05-ui-uat.py` 的断言,零新增网络面、零新增输入面、零新增依赖、零新增文件;未引入计划 `<threat_model>` 之外的信任边界。

计划 `<threat_model>` 的四条 mitigate 均已落地:T-idi-05-01(`#btn-authorize` 保持 600 + 六条字重断言)、T-idi-05-02(每任务复跑 CHECK-01/02,围栏标记 1/1,43 对与 `ORDER 0.363` 逐字不变)、T-idi-05-03(全局 `h1, h2` 规则 × 0,六条 chrome 字面守卫未动)、T-idi-05-04(`--item 4` + `--item smoke` 在 p1/p3 真实样本上读 computed style)。T-idi-05-SC:零安装,vendor 仍只含 `marked.min.js`。

## Next Phase Readiness

- **idi-05-02 可以开始。** 它需要的两条既有正确形态已就位:`.markdown-body h1/h2/h3` 的 `font-weight: var(--fw-semibold)`(L643)与 `.panel-header h2` 的 `var(--fw-medium)`(L445)构成 D-04 断言反转的三档参照;`#btn-authorize` 的 600 是 D-12 例外,Plan 02 会改它的字号步进(14 → 16px)但**不得**动它的字重。
- **注意 Plan 02 的迁移核账口径**:本计划之后 `--text-md` 失去 `.markdown-body h3` 消费者(改由 `--text-lg` 承接),`--text-lg` 的消费者从 1 升到 2(`.markdown-body h3` 与 `#draft-view > h2, #round-title`)。`--text-md` 仍有 5 处消费者,不产生孤儿档。
- **注意 `--fw-medium` 消费者已从 4 升到 8**,Plan 02 若再改动字重需重新核账。
- **无阻塞项。** `frontend/app.js` / `index.html` / `vendor/` / `scripts/ui-states/` 仍零 diff;`scripts/check-02-contrast.py` 代码零改动。

---
*Phase: idi-05-typography-and-visual-hierarchy*
*Completed: 2026-09-21*

## Self-Check: PASSED

**Created files exist:**
- FOUND: frontend/style.css
- FOUND: scripts/check-05-ui-uat.py
- FOUND: .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-01-SUMMARY.md

**Commits exist:**
- FOUND: 7f4f589 (Task 1 — 编排者提交)
- FOUND: b77b2f1 (Task 2)
- FOUND: a0845bb (Task 3)

**Content assertions re-verified at self-check time:**
- `grep -o -- '--text-2xl: 22px;' frontend/style.css | wc -l` == 1
- `grep -o -- '--text-3xl: 28px;' frontend/style.css | wc -l` == 1
- `grep -o -- '--lh-tight: 1.3333;' frontend/style.css | wc -l` == 1
- `grep -c '^#draft-view > h2, #round-title' frontend/style.css` == 1
- `grep -c '18/28' frontend/style.css` == 0
- `grep -o 'var(--fw-medium)' frontend/style.css | wc -l` == 8
# Phase 7: 交互状态与焦点样式 - Pattern Map

**Mapped:** 2026-09-22
**Files analyzed:** 5 (2 modify-in-place gates, 1 append-only stylesheet, 2 new/extended assertion surfaces)
**Analogs found:** 5 / 5 (every target has a tracked-source analog in this repo)

> **Baseline note (D-20 的「执行前基线」).** 四条不变量门在 HEAD 上**全绿**,已实跑:
> `check-01` PASS / `check-02` PASS(0 failures, 47 pairs + 1 ORDER)/ `check-03` PASS /
> `check-04` PASS。这是 Phase 7 改动前的基线 —— 任何一条从 PASS 变红即为本阶段引入的回归。
>
> **实测人口普查(HEAD, 2026-09-22):**
> - `grep -n ":focus\|:active\|@media\|transition\|prefers-reduced" frontend/style.css`
>   → **唯一命中是 `:602 transition: background-color 0.3s;`**。全站 `:focus` / `:focus-visible` /
>   `:active` / `@media` / `prefers-reduced-motion` **计数均为 0** —— D-05 是**新增**作者化焦点样式,
>   不是恢复被移除的。
> - `grep -o '!important;' | wc -l` = **1**;`grep -cE '^[[:space:]]*\.hidden[[:space:]]*\{'` = **1**。
> - `scripts/ui-states/` 五个样本(p1 / p12 / p3 / checking / archive)内 `href` 出现次数 = **0**
>   ⇒ D-18 的前提「`#round-doc` 内 `a[href]` 计数为 0」**已独立复核成立**。

## File Classification

| New/Modified File | Action | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|---|
| `frontend/style.css` | MODIFY (append-only) | config (token layer + stylesheet) | transform (declarative cascade) | 自身既有段落 — 见下方五组逐条 analog | exact (same file, same house style) |
| `scripts/check-02-contrast.py` | MODIFY (PAIR 清单) | test (static arithmetic gate) | transform | 自身 L394-395 的 `@0.75` 条目 + L405-425 的 NON-TEXT 段 | exact |
| `scripts/check-05-ui-uat.py` | MODIFY (新增 item 10) | test (runtime browser UAT gate) | request-response | 自身 `item9` (L2248-2366) + `_idi06_clearance_assert` (L2179-2209) | exact |
| 契约计数静态断言(D-15 中段;落点未定 — 新零依赖脚本 **或** `check-05` 内静态守卫) | CREATE or MODIFY | test (static text census) | transform | `scripts/check-01-token-conformance.sh`(独立脚本形态)**或** `_l2_guard_shape` (L1606-1628) / `_latest_check_max_height_guard` (L2102-2122)(脚本内静态守卫形态) | exact (两种形态都有现成先例) |
| 归档合成一次性注入探针(D-18;建议名 `scripts/probe-07-focus-composite.py`) | CREATE | test (one-off counterfactual probe — **不是门**) | request-response | `scripts/probe-05-resolve-color.py`(整个文件) | exact |

**零改动(硬规则 5 / Phase 8 的活,已核实不在本阶段):** `frontend/app.js`、`frontend/index.html`、`frontend/vendor/`(保持只有 `marked.min.js`)。

**Analog 追踪性核验(gate #3645):** 上表全部 analog 路径均由
`git ls-files -- <path>` 确认是 **tracked source**(`frontend/style.css`、`scripts/check-02-contrast.py`、
`scripts/check-05-ui-uat.py`、`scripts/probe-05-resolve-color.py` 四份全部非空)。**无一条是 gitignored
镜像路径**;`scripts/check-01/03/04*.sh` 同为 tracked。

---

## Pattern Assignments

### `frontend/style.css` — 围栏内:tier-2 令牌声明

**Analog:** 同一文件 §Tier 2 — surface / border(L182-197)

**分组声明形态** — 新令牌按**语义族**落在同族相邻行,不另起区块(L182-197 逐字):
```css
  /* Tier 2 — surface / border */
  --color-surface: var(--radix-gray-2);
  --color-surface-hover: var(--radix-gray-3);
  --color-surface-user: var(--radix-gray-4);
  --color-surface-info: var(--radix-blue-2);
```
⇒ `--color-surface-active: var(--radix-gray-4);` 的落点是紧邻 L184/L185 的 surface 族内。

**「与消费者同提交」的围栏注释形态**(L206-208)——这是硬规则 5 在本文件里的**具名写法**,新令牌必须复制它:
```css
  /* Tier 2 — declared with their consumers (Hard Rule 5): .event-kind / .fatal. */
  --color-kind-fg: var(--white);
  --color-border-danger-subtle: var(--radix-red-7);
```

**⚠ 值碰撞必须显式登记(本阶段最容易踩的注释陷阱)。** `--radix-gray-4` 已被 `--color-surface-user`
消费(L185),而 L293-297 的围栏注释**逐字警告过**「不要为 hover 用 gray-4」:
```
     3. --color-surface-hover and --color-surface-sunken deliberately share
        --radix-gray-3 (04.1-N-4). gray-3 is the canonical next step above the
        default component surface (gray-2), which is what makes button:hover
        perceptible; gray-4 would double the hover delta and collide with
        --color-surface-user. */
```
⇒ `--color-surface-active` 取 gray-4 会与 `--color-surface-user` **同值**。这不是缺陷(名字不同、语义不同 ——
04.1 D-03「名必须说实话」),但**不写注释就会被后来者读成违反 04.1-N-4 并「修」掉**。新令牌的注释必须
点名 04.1-N-4 并说明「active 是 3→4 的**递进**终点,与 hover 的 3 相邻;值碰撞对象是 `--color-surface-user`,
其语义是『用户消息背景』,与本令牌不共享消费者」。**建议同时扩写 L277-297 那条「三个不得改回的值」的
第 3 条**,否则同一份注释会自相矛盾。

**围栏内 `rgba()` 字面量的唯一先例**(L199-204)——D-08 的 alpha 叠层的合法性依据:
```css
  /* Tier 2 — overlay backdrop and the shadow tokens (composer: three layers;
     overlay: the modal card's elevation, restored by R-2 so that no bare
     rgba() appears outside the fence). */
  --color-overlay-backdrop: rgba(0, 0, 0, 0.45);
  --shadow-composer: rgba(0, 0, 0, 0.04) 0 0 0 1px, ...;
  --shadow-overlay: 0 8px 30px rgba(0, 0, 0, 0.2);
```

**⚠ D-08 的落点决定点(必须由 planner 裁定并写明理由)。** D-08 的片段把
`rgba(0,0,0,0.06)` 写在**规则体内**(围栏外),而 L200-201 的注释立下的是相反的先例 ——
「R-2 恢复 shadow 令牌,**使围栏外不再出现裸 `rgba()`**」。`check-01` 只数裸 `#hex` 与 tier-1 `var()`
引用,**不数裸 `rgba()`**,所以这条纪律**没有机械守卫**——正因如此它只能靠注释与 review 守。
两条路都站得住,但**必须选一条并登记**:
- (a) 围栏内新增一个 rgba 值令牌(如 `--overlay-hover` / `--overlay-active`),规则体只写 `var(...)`
  —— 与 R-2 先例一致,且 alpha 的 0.06 / 0.12 两个取值变成可复算的单一事实源;
- (b) 规则体内直写 `rgba()`,并在注释里说明「R-2 的『围栏外无裸 rgba』是 shadow 令牌的收敛结果,
  不是全局不变量;本处 alpha 是交互态参数,不入语义层」。
CONTEXT D-08 的「已登记代价 ①」措辞是「**围栏内合法**」,倾向 (a),但 D-08 的代码片段是 (b)。

---

### `frontend/style.css` — 围栏外:hover / active 的既有形态与缺陷现场

**Analog A — 唯一的既有 `:hover`(L578-588,逐字):**
```css
button {
  padding: var(--space-1-5) var(--space-2-5);
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  font-size: var(--text-base);
  font-weight: var(--fw-medium);
  cursor: pointer;
}
button:hover { background: var(--color-surface-hover); }
button.danger { color: var(--color-action-danger); border-color: var(--color-action-danger); }
```
⇒ D-07 的 gate 形态必须写成 `button:not(:disabled):hover`(0-2-1),**不改 L587 本体**;新规则追加在文件末尾。

**Analog B — D-02 第 5 条实测缺陷的现场(L1220-1222,逐字):**
```css
.verdict-buttons { display: flex; gap: var(--space-2); }
.verdict-buttons button { font-size: var(--text-base); padding: var(--space-1) var(--space-2-5); }
.verdict-buttons button:disabled { opacity: 0.5; cursor: not-allowed; }
```
⇒ 该规则**只设 `opacity` / `cursor`,不钉 `background`**,故 `button:hover`(L587,0-1-1)在
`.verdict-buttons button:disabled`(0-2-1)之后仍然生效于 `background` —— 禁用态悬停时背景变色。
**这是 D-07 要修的真实缺陷**;`#btn-authorize`(L1096,1-0-0 钉住填充色)反而是**免疫**的,与路线图点名的对象相反。

**Analog C — 8 条 `:disabled` 规则的统一形态**(全部为 `opacity` + `cursor`,逐条):
| 行 | 规则 | opacity |
|---|---|---|
| L779 | `#btn-approve-draft:disabled` | 0.55 |
| L791 | `#btn-divergence:disabled` | 0.55 |
| L1052 | `#btn-process-round:disabled` | 0.55 |
| L1106 | `#btn-authorize:disabled` | 0.55 |
| L1118 | `#btn-start-writing:disabled` | 0.55 |
| L1132 | `.overlay-card .modal-buttons button:disabled` | 0.5 |
| L1176-1179 | `#btn-continue-check, #btn-continue-repair:disabled` | 0.55 |
| L1222 | `.verdict-buttons button:disabled` | 0.5 |

形态逐字(L779 为范本):`#btn-approve-draft:disabled { opacity: 0.55; cursor: not-allowed; }`
⇒ 本阶段**不改这 8 条**(D-07 选 gate 而非回写,收敛是 backlog 项);它们进 `check-02` 的豁免面
(WCAG 1.4.3 非活动组件豁免,A11Y-04b 已登记)。

**Analog D — 填充按钮的既有规则体(D-08 的覆盖对象,`background` + `color` + `border-color` 三件套):**
```css
/* L666-671 */  .overlay-card button { margin-top: ...; background: var(--color-action-primary); color: var(--color-action-primary-fg); border-color: var(--color-action-primary); }
/* L672-675 */  .overlay-card button.danger { background: var(--color-action-danger); color: var(--color-action-danger-fg); }
/* L883-891 */  #chat-input-row button { padding: ...; border-radius: var(--radius-pill); background: var(--color-action-primary); color: var(--color-action-primary-fg); border-color: var(--color-action-primary); ... }
/* L901-905 */  button.primary { background: var(--color-action-primary); color: var(--color-action-primary-fg); border-color: var(--color-action-primary); }
/* L771-778 */  #btn-approve-draft { ... background: var(--color-action-commit-surface); border-color: var(--color-action-commit); color: var(--color-action-commit-fg); ... }
/* L784-790 */  #btn-divergence { ... background: var(--color-action-warning-surface); border-color: var(--color-action-warning); color: var(--color-action-warning); ... }
/* L1046-1051 */ #btn-process-round { background: var(--color-action-routine-surface); border-color: var(--color-action-routine); color: var(--color-action-routine-fg); ... }
/* L1096-1105 */ #btn-authorize { padding: ...; background: var(--color-action-irreversible-surface); border-color: var(--color-action-irreversible); color: var(--color-action-irreversible-fg); font-size: var(--text-md); font-weight: var(--fw-semibold); }
/* L1111-1117 */ #btn-start-writing { ... background: var(--color-action-commit-surface); border-color: var(--color-action-commit); color: var(--color-action-commit-fg); ... }
/* L1170-1175 */ #btn-continue-check, #btn-continue-repair { background: var(--color-action-routine-surface); border-color: var(--color-action-routine); color: var(--color-action-routine-fg); ... }
```
⇒ **这是 D-02 第 7 条的实测证据面**:九组规则的特异性(1-0-0 或 0-1-1 且源码在 L587 之后)全部盖过
`button:hover`(0-1-1),故它们**今天 hover 时零反馈**。D-08 的 rgba 叠层必须用
**特异性 ≥ 上述每条**的选择器覆盖它们 —— 这是本阶段**唯一需要超过 0-1-1 的地方**,
`button:not(:disabled):hover`(0-2-1)对 1-0-0 的 `#btn-authorize` **不够**,必须逐 id 或按族枚举。

**Analog E — 浮层内控件的 hover 先例(L1065-1070,逐字):**
```css
#selection-menu button {
  border: none;
  background: transparent;
  white-space: nowrap;
}
#selection-menu button:hover { background: var(--color-surface-info); }
```
⇒ 这是**朴素(透明底)按钮 hover 变浅蓝**的既有先例,也是 Claude's Discretion 里
「`#selection-menu button` 的态是否并入统一一套」的对象。它**不是**填充按钮(D-08 的 rgba 叠层不适用)。

**Analog F — `input` / `select` 的既有规则体(D-10 的 hover 加深对象):**
```css
/* L561-568 */ #ai-route-select { flex: 0 0 auto; padding: ...; border: 1px solid var(--color-border-strong); border-radius: var(--radius-sm); font-size: var(--text-base); background: var(--color-surface); }
/* L570-576 */ #project-path-input { flex: 1; padding: ...; border: 1px solid var(--color-border-strong); ... }
/* L918-924 */ #round-switcher { padding: ...; border: 1px solid var(--color-border-strong); ... }
/* L1152-1159 */ #check-switcher { ... border: 1px solid var(--color-border-strong); ... }
/* L684-691 */ #enter-form input[type="text"] { ... border: 1px solid var(--color-border-strong); ... }
/* L874-882 */ #chat-input-row input { ... border: 1px solid var(--color-border-strong); ... }
/* L1122-1130 */ #confirmation-modal input[type="text"] { ... border: 1px solid var(--color-border-strong); ... }
/* L1212-1219 */ .verdict-note-input { ... border: 1px solid var(--color-border-strong); ... }
```
⇒ 全部 `input` / `select` 的边框都是 `--color-border-strong`(= `--radix-gray-9` `#8d8d8d`,L54/L192)。
D-10 的「加深一步」候选档 `--radix-gray-11` `#646464`(L55)/ `--radix-gray-12` `#202020`(L56)**都已声明**,
故取哪一档都是**零新增 primitive**;两档都要新配对进 `check-02`。

---

### `frontend/style.css` — 围栏外:`transition` 与 `prefers-reduced-motion`

**Analog — D-12 的**直接**范本(L1238-1242,逐字)。** 这是本文件里「追加在末尾的元素选择器规则」的
唯一同类:相同的选择器三元组 `button, input, select`、相同的 0-0-1 特异性、相同的「元素选择器不越权」理由。
```css
/* 控件前景色(N-4 / D-19,追加在文件末尾):今天每个按钮与输入框的前景色来自 UA
   (buttontext / fieldtext),那是令牌块之外的第二个事实源。
   元素选择器特异性 0-0-1,所以 button.danger(0-1-1)、#btn-*(1-0-0)、
   .overlay-card button(0-1-1)全部仍然取胜。视觉 delta 不可感知。 */
button, input, select { color: var(--color-text); }
```
⇒ D-12 的 `button, input, select { transition: background-color 120ms, border-color 120ms; }`
应**紧随这一条之后**(或与之相邻)追加,注释须说明「0-0-1,与 `.event-list`(0-1-0)零竞争 —— 不同元素」。

**⚠ D-12 与 Analog 的特异性陷阱。** L1242 是 0-0-1;D-08 的填充按钮 hover 若写成 `#btn-*:not(:disabled):hover`(1-1-0)
则**稳胜**;但若写成 `button:not(:disabled):hover`(0-2-1),它对 `#btn-authorize`(1-0-0)**无效** ——
因为 1-0-0 > 0-2-1(ID 列 > 类列)。**D-08 的 selector 组织方式是本阶段最容易出错的一处**,必须在计划里
按 Analog D 的九组规则逐条核对特异性,或统一用「同族选择器列表」并逐个验证计算样式。

**Analog — 唯一的既有 `transition`(D-11 的保留对象,L594-605,逐字):**
```css
.event-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-1-5);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-sm);
  padding: var(--space-2);
  background: var(--color-surface);
  transition: background-color 0.3s;
}
.event-list.streaming { background: var(--color-surface-streaming); } /* 流式进行中 */
.event-list.aborted { background: var(--color-surface-danger); }   /* 已中止标记 */
```
⇒ **不改 L602 一个字节**(D-11);新过渡是**独立挂载规则**。D-13 的减弱动效枚举**含 `.event-list`**
(否则 reduce 用户仍会看到 0.3s 的流式状态淡入)。

**⚠ `@media` 在 HEAD 上的计数是 0,且已有一条「决策登记」断言在看着它。**
`check-05` L1598-1628 有:
```python
MEDIA_QUERY_DECL = "@media"
EXPECTED_MEDIA_QUERIES = 0
...
def _l2_guard_shape(item):
    count = text.count(MEDIA_QUERY_DECL)
    ...
    ok_true(item,
            "[static] frontend/style.css 的 @media 出现次数 == 决策(被实测推翻 ⇒ 0)",
            count == EXPECTED_MEDIA_QUERIES, EXPECTED_MEDIA_QUERIES, count, ...)
```
⇒ **D-13 一旦落地 `@media (prefers-reduced-motion: reduce)`,`EXPECTED_MEDIA_QUERIES` 必须同步改成 1**,
否则 `check-05 --item 8` 立刻 FAIL。这是 D-20「本阶段会打破的既有断言」清单里**尚未登记的一条**,
必须在计划里显式补上(L1598-1601 的注释本身就要求「若日后写出守卫,把这里改成 1 并同步更新
SUMMARY 的决策记录与 UI-SPEC §L-2」)。

**Analog — 追加规则的长注释形态(D-13 的注释范本)。** 本文件对每条追加规则都写「为什么是这个形态 +
为什么不选那个替代」:L1244-1273(活动面板标记,四条承重决定)、L1313-1324(六目标换行保护)、
L1275-1308(嵌入标题刻度)。D-13 的注释须照此写明「**为什么不采用行业标准的
`*, *::before, *::after { transition-duration: 0.01ms !important }`**」——
该片段带**两个 `!important`**,会让 `check-04` 立刻从 1 变 3(硬规则 2/4)。

---

### `frontend/style.css` — 围栏外:`:focus-visible`(D-05 / D-06)

**无既有 analog —— HEAD 上 `:focus` / `:focus-visible` / `outline` 计数全为 0。** 这是**新增**,
不是恢复(路线图 L269 已明文)。

**形态范本一:枚举式选择器 + 逐条对齐注释(L1313-1324,逐字节选)。** D-05 的「为什么枚举而不是裸通配」
必须复刻这套论证形态:
```css
/* 六目标换行保护(L-3 / D-07,追加在文件末尾 —— 硬规则 3:追加,不重排)。
   六目标枚举 —— 与 renderMarkdown() 的调用点一一对应(Phase 5 idi-05-04 已建立该枚举,
   见 `:1229-1262` 的注释与 check-05 的 MARKDOWN_TARGETS)。
   不写通配规则:那会波及已裁定的 `.event-content { word-break: break-all }`(L598-601),
   并把「哪些容器受影响」重新变成不可枚举 —— 那正是 G-idi-05-1 的成因。 */
.markdown-body, .event-content, .chat-bubble, .say-chunk, .annotation-note, .annotation-answer-body {
  overflow-wrap: anywhere;
}
```

**形态范本二:枚举集必须与门的普查脚本**同集**(D-05 的核心杠杆)。** `check-05` L1683-1685 逐字:
```js
  document.querySelectorAll(
    'button, input, select, textarea, a[href], summary, [tabindex]'
  ).forEach((el) => {
```
⇒ D-05 的七个选择器与这一行**逐字同集**(顺序亦同:`button, input, select, textarea, a[href], summary, [tabindex]`)。
注释必须点名「枚举集 = `check-05` 的普查集,两者可逐条对照;新增一类可聚焦元素要**同时**改两处」。

**形态范本三:几何绑定必须在注释里写明(D-05 的 `2px + outline-offset: 2px`)。**
`check-05` L2202-2209 的 note 逐字:
```python
    ok_true(item,
            f"[{state}] L-5 每个裁剪容器 × 可聚焦后代的 clearance >= {CLEARANCE_MIN_PX:.0f}px",
            not bad, f"全部 >= {CLEARANCE_MIN_PX:.0f}px",
            f"共 {len(judged)} 行,未达标 "
            f"{[(r['el'], r['container'], round(r['clearance'], 1)) for r in bad]}",
            "4px = Phase 7 的 outline: 2px + outline-offset: 2px 的环外伸量。"
            "实测未达标时**只改那一个容器**的 padding 为 var(--space-1),"
            "禁止「为确定性四个全抬」(UI-SPEC §L-5 的决策规则)")
```
⇒ CSS 侧的注释必须**反向引用** `CLEARANCE_MIN_PX = 4.0`(`check-05` L2040)与 `idi-06-UI-SPEC.md` §L-5。
**改几何即改那个门的阈值** —— 这是双向绑定的文字证据。

**`--color-focus: #1f63bd` 的「刻意字面遵从」注释(D-04 的登记要求)。** 本文件已有**同类**的
「这不是漏改,不得修掉」注释(L231-237 的字号表、L277-297 的三个值、L299-319 的图标机制)。
D-04 的注释须照此写明「`#1f63bd` 是整个颜色层里**唯一不在 Radix 刻度上**的值(除 `--white` 与两个 `rgba()` 阴影);
它与 04.1『值必须来自 Radix 步』的纪律相冲,但 S-4 的签核算术是拿它算的 ⇒ 这是**对已签核契约的字面遵从**,
不是漏改」。

**`#round-doc` 的负空间声明(D-06)。** Phase 7 **不写** `#round-doc:focus-visible`。本文件对
「不写什么」有既成写法(L1013-1014 的「规则体见文件末尾」+ L1229-1232 的「绝不插入、绝不重排」),
D-06 的注释须以同样口吻写明「`#round-doc` 今天不可聚焦,任何针对它的规则都是**死代码**,
违反『不声明不被消费的东西』;指派给 Phase 8」。**这条必须同时出现在 CONTEXT 的 deferred 与 canonical_refs 里**
(已满足:`07-CONTEXT.md` L357 与 L335)。

---

### `scripts/check-02-contrast.py` — 新增三条 `--color-focus` PAIR

**Analog A — `@<alpha>` 后缀的唯一既有用例(D-15/D-18 的**零新代码**依据)。** L394-395 逐字:
```python
  /* the surviving whole-document dim — the archive view (A11Y-04b) */
  /* PAIR --color-text ON --color-surface TEXT@0.75 */
```
⇒ D-15 的第三条 `/* PAIR --color-focus ON --color-surface NON-TEXT@0.75 */` 与它**同族同机制**:
`.archive-mode` 的 `opacity: 0.75`(style.css L1225)合成整棵子树。**新增条目应紧邻 L394-395 摆放**,
让两条「0.75 合成」在同一处可对照。

**Alpha 合成的实现(D-15 引用的零新代码证据,L177-196 逐字):**
```python
    for match in pairs:
        fg_name, bg_name, kind, alpha = match.groups()
        fg = resolve(fg_name, decls)
        bg = resolve(bg_name, decls)
        # Composite whenever the foreground carries alpha — either from the
        # token's own value or from the entry's @<alpha> suffix. contrast_ratio
        # reads only rgb[:3], so skipping this would score rgba(0,0,0,0.45) as
        # fully opaque (21.00 instead of the true 3.36).
        token_alpha = fg[3]
        fg_alpha = token_alpha * float(alpha) if alpha is not None else token_alpha
        if fg_alpha < 1.0:
            fg = composite(fg, bg, fg_alpha)
```
配合 `composite()`(L125-127):
```python
def composite(fg, bg, alpha):
    """Composite fg over bg per channel in 8-bit sRGB."""
    return tuple(int(round(alpha * fg[i] + (1.0 - alpha) * bg[i])) for i in range(3))
```
⇒ `--color-focus` 是 opaque hex(`#1f63bd`,alpha 1.0),`@0.75` 使 `fg_alpha = 1.0 × 0.75 = 0.75`
⇒ 环色以 75% 合成到 `--color-surface` 上再测 —— 与 `.archive-mode` 的实际渲染模型一致。

**Analog B — NON-TEXT 段的摆放与注释分组(L405-425,逐字节选):**
```python
  /* non-text boundaries and state indicators (SC 1.4.11, 3:1) */
  /* PAIR --color-border-strong ON --color-surface-page NON-TEXT */
  /* PAIR --color-border-strong ON --color-surface NON-TEXT */
  ...
  /* the active sidebar panel marker, non-text half: the 3px inset bar is a state
     indicator (SC 1.4.11), on the same --color-surface-page ground as its TEXT
     half above. */
  /* PAIR --color-marker-active ON --color-surface-page NON-TEXT */
```
⇒ 三条新条目落在此段,带一条分组注释说明「焦点环是 SC 1.4.11 的 state indicator,
三处验证面 = `--color-surface-page` / `--color-surface` / `--color-surface`@0.75;
`--color-surface-sunken` **不进验证面**(它只是 `.markdown-body code` L765 与 `.badge-answered` L1004
的背景,不是任何可聚焦元素的相邻地面)」。

**必须同提交的记账性编辑 — 清单头部的计数演化注释(L323-343 逐字节选):**
```python
     Manifest size across four value layers (D-15): 24 / 34 / 43 / 47 — ROADMAP
     Phase 4 wrote 24 pairs (20 text + 4 non-text); the disk state Phase 4
     actually landed was 34 pairs (29 TEXT + 5 NON-TEXT) + 1 ordering entry; the
     04.1 rewrite re-enumerated 43 pairs (34 TEXT + 9 NON-TEXT) + 1 ordering entry;
     Phase 5 lands 47 pairs (35 TEXT + 12 NON-TEXT) + 1 ordering entry — the
     three-step action ramp needs a white-on-fill TEXT pair and a non-text
     boundary pair for each solid tier, and the active-panel marker needs one of
     each on its ground. The four numbers are not drift: the contract is
     "enumerate the combinations that actually render", and each successive value
     layer changes which combinations occur. */
```
⇒ 加三条 NON-TEXT 后是 **50 pairs(35 TEXT + 15 NON-TEXT)+ 1 ordering**,且必须**追加第五个值层**
「Phase 7 lands 50 pairs …」并说明焦点环的验证面。**不改这条注释 = 清单与令牌块开始漂移**,
而该文件的开头 docstring(L7-12)正是以「漂移必须可见」为立身之本。

**机制性护栏(改动不会误伤,已核实):** 覆盖地板是 `len(pairs) < 24 or text_n < 20 or nontext_n < 4`(L150-155),
50/35/15 全部远高于地板;`raw_pairs != len(pairs)` 的原始标记计数校验(L161-167)要求新条目的注释
**逐字符合 `PAIR_RE`**(L28-31)—— 写法必须是 `/* PAIR --a ON --b NON-TEXT@0.75 */`,大小写与空格敏感。

---

### `scripts/check-05-ui-uat.py` — 新增 item 10

**Analog A — 项的四处登记点(全部要改,漏一处即不可达或不可发现):**

1. 模块 docstring 的**运行方式**列表(L31-40)—— 加一行 `--item 10`;
2. 模块 docstring 的**逐项说明**块(L42-92)—— 加「第 10 项」段落(现有形态见 L42-51 的「第 9 项」);
3. `parse_args` 的 `--item` help(L2427-2428):
   ```python
   ap.add_argument("--item", action="append", default=None,
                   help="只跑指定项:smoke / 1 / 2 / 3 / 4 / 5 / 6 / 7 / 8 / 9(可重复,或逗号分隔)")
   ```
4. `normalize_items` 的默认列表(L2441)与 `main()` 的 `known` 集合(L2454)+ 分发块(L2497-2498):
   ```python
   known = {"smoke", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
   ...
           if "9" in items:
               item9(page, tmp_root)
   ```
   ⚠ `known` 漏加 "10" 会直接 `SystemExit("ERROR: 未知项 …")`。

**Analog B — 项函数的骨架(L2248-2255,逐字):**
```python
def item9(page, tmp_root):
    item = "9"
    print("\n=== UAT 9: L-4 面板区滚动容器收敛(D-14)===", flush=True)

    # ---- (a) 滚动者 DOM 普查 + (c) 两处限高消失 + (d) 保留项护栏 ---------------
    proj = make_fixture("p1", tmp_root)
    enter_project(page, proj)
    info("item9 样本", f"p1(会话流活动态,#session-panel / #ai-events 可见)→ {proj}")
```

**Analog C — 「按元素普查 + 断言未覆盖数为 0」的完整形态(D-16 的直接范本,L2179-2209)。**
这是本阶段 item 10 最重要的一条 analog —— **断言的是「全部实例」而不是「规则被写下」**:
```python
def _idi06_clearance_assert(page, item, state):
    """L-5 的 clearance 普查断言(D-13):每个裁剪容器 × 其可聚焦后代的实测 clearance >= 4px。

    按 **DOM 遍历**算出,不硬编码选择器列表。只判定**当前落在容器可视滚动区内**的行:
    与 padding 盒完全不相交的元素被滚动到视口之外,当前不渲染,其负 clearance 是噪声
    (见 `_IDI06_CENSUS_JS` 里 `intersects` 的注释);相交却越界才是真裁切,clearance 为负。
    """
    data = page.evaluate(_IDI06_CENSUS_JS)
    if data is None:
        blocked(item, f"[{state}] L-5 ...",
                "普查脚本返回数据", "<MISSING>", "普查无返回 ⇒ 不记 PASS")
        return
    rows = data["clearance"]
    info(f"item9 [{state}] L-5 clearance 普查(全部原始行)",
         f"{len(rows)} 对:"
         f"{[(r['el'], r['container'], round(r['clearance'], 1), r['visible'], r['intersects']) for r in rows]}")
    judged = [r for r in rows if r["visible"] and r["intersects"]]
    if not judged:
        info(f"item9 [{state}] L-5 clearance",
             "无「裁剪容器 × 可聚焦后代」组合落在可视滚动区内 ⇒ 本样本无判定"
             "(不记断言,避免空转 PASS)")
        return
    bad = [r for r in judged if r["clearance"] < CLEARANCE_MIN_PX]
    ok_true(item, ..., not bad, f"全部 >= {CLEARANCE_MIN_PX:.0f}px",
            f"共 {len(judged)} 行,未达标 {[(r['el'], r['container'], round(r['clearance'], 1)) for r in bad]}",
            ...)
```
**五条形态纪律**(item 10 必须逐条复刻):
1. `data is None` ⇒ `blocked(...)`(**绝不记 PASS**);
2. 先 `info()` 落**全部原始行**,再判定(「不给结论替代证据」,L1547 明文);
3. 空集时 `info()` 声明「本样本无判定」并 `return`,**不记空转 PASS**(L2196-2200);
4. 判据是 `not bad`(即**未覆盖数 == 0**),D-16 的「未被覆盖的可聚焦元素数为 0」照此写;
5. 失败行的 note 要给出**可执行的修复动作**。

**Analog D — 枚举集常量与普查 JS 的存放形态(L1660-1685,L2032-2049)。** 普查 JS 是模块级
`r"""..."""` 常量(带中文注释解释每个字段为什么承重),常量与阈值集中在一处:
```python
CLEARANCE_MIN_PX = 4.0
...
PANEL_SCROLLERS = ("#chat-messages", "#latest-check", "#main-pane")
PANEL_SCROLLERS_EXEMPT = ("#chat-messages",)
STYLE_CSS = ROOT / "frontend" / "style.css"
TARGET_MIN_PX = 24.0
SUMMARY_TAG = "summary"
```
⇒ item 10 的普查 JS 命名照 `_IDI06_CENSUS_JS` 的 `_IDI06_*` 前缀族,命名为 `_IDI07_*`。

**Analog E — 读计算样式 / 令牌 / 有效背景的三个读取器(D-17 的机器半场全靠它们):**
```python
_READ_JS = """([sel, prop]) => {
  const el = document.querySelector(sel);
  if (!el) return null;
  return getComputedStyle(el)[prop];
}"""
def read_style(page, selector, prop): ...              # L281-282

def resolve_color(page, token): ...                    # L369-389,未声明 ⇒ None(记 BLOCKED)
def resolve_token(page, name): ...                     # L392-402,非颜色令牌
def effective_bg(page, selector): ...                  # L405-418,沿祖先链找第一个非透明背景
```
⇒ D-17 的 SC1(读 `outline-width` / `outline-color`)/ SC2(点击后读 `outline`)/ SC5(读 hover 后
`background-color` / `border-color`)**全部复用 `read_style`**;环色期望值用 `resolve_color(page, "--color-focus")`
而不是硬编码 `rgb(31, 99, 189)` —— 这正是 L974 立下的纪律(「期望侧来自运行时解析的令牌,不再硬编码 rgb;
值的仲裁者是 `check-02-contrast.py`」)。

**Analog F — 「元素读不到 ⇒ BLOCKED,绝不记 PASS」的前提检查(L2212-2238,逐字节选):**
```python
def _idi06_hit_assert(page, item, state, require_summary):
    ...
    if require_summary:
        summary_rows = [r for r in rows if r["el"].split(".")[0] == SUMMARY_TAG]
        if not summary_rows:
            blocked(item, f"[{state}] .annotation-answer summary 已由 renderAnnotations 造出且可见",
                    ">= 1 个可见的 <summary>", "<MISSING>",
                    "本断言的主要对象不存在 ⇒ 命中区断言失去证明力,不记 PASS")
            return
```
⇒ item 10 的每个探针都必须在读值前断言「目标元素存在且可见」,否则 `getBoundingClientRect()` /
`getComputedStyle()` 的返回值会让断言退化成**空转 PASS**。**这正是 `check-05` docstring L58
点名的同型陷阱**(「第 7 项 `all(w != "700")` 对 None 恒真」)。

**Analog G — 样本循环形态(D-16 的「三样本才覆盖全部组合」教训,L2333-2361):**
```python
    for state in ("p1", "checking"):
        proj_c = make_fixture(state, tmp_root)
        enter_project(page, proj_c)
        _idi06_clearance_assert(page, item, state)
        _idi06_hit_assert(page, item, state, require_summary=False)
```
配套的**样本可见性说明**(L2328-2332 注释)是承重的:「单样本会把『藏住』读成『不达标』」。
⇒ item 10 的 hover/active 探针必须在**控件可见的样本**上跑(p1 有会话流与探针行;`#checks-panel`
只在 checking 可见;批注面板只在 p3 可见)。

**Analog H — viewport 纪律(L1551 / L2363-2366):**
```python
    # 本项不变更 viewport;此处是兜底复位(若调试期用过 set_viewport_size),
    # 与 item 8 同一纪律:VIEWPORT_RESTORE 是 harness 的基准视口,不复位会污染其后各项。
    page.set_viewport_size(VIEWPORT_RESTORE)
```
⇒ item 10 若用 `page.hover()` / `page.click()` 改变滚动位置,**结束前必须复位**。

**⚠ 环境事实(不得对抗,`check-05` docstring L18-29 是权威):**
- **浏览器选择:** 默认 `--browser bundled`(Playwright 自带 chromium,已缓存,**可无头**);
  `--browser chrome` 强制有头。本机 x86_64 venv 下 `channel="chrome"` + `headless=True`
  **CDP 永不连上,180s 挂死**(L26-28)。`probe-05` 也是 `pw.chromium.launch(headless=True)`(L112)。
- **禁止 `networkidle`**(SSE 长连接永不返回,L84);
- **截图不可用** ⇒ SC1–SC5 全部走**计算样式读数**,**不要计划视觉 diff**;
- **键盘文本选区无法自动化**(L88-92)—— **但 `page.keyboard.press("Tab")` 不受此限**,SC1 可自动化。
- **人工项 5″ 必须留在 VERIFICATION 的 manual list**(D-17),不得换成机器代理量。

---

### 契约计数静态断言(D-15 中段)

**落点未定 —— 两条 house 形态都有现成先例,planner 须二选一并写明理由(D-15 头部说「不新建脚本」,
中段说「新的零依赖静态断言」,两者张力须由计划消解;`check-06` 编号已被
`scripts/check-06-idi05-validation.py` 占用)。**

**形态 A — 独立零依赖 shell 守卫(`scripts/check-01-token-conformance.sh` 逐字,L1-33 节选):**
```bash
#!/usr/bin/env bash
# CHECK-01 — token conformance: zero bare #hex AND zero tier-1 primitive
# references outside the fenced :root block.
# Zero-dependency (awk + grep). Read-only. PASS: prints "PASS" and exits 0.
set -euo pipefail
cd "$(dirname "$0")/.."

# Assert the input before counting: a missing/unreadable file must FAIL loudly.
[ -f frontend/style.css ] || { echo "FAIL: frontend/style.css not found"; exit 1; }

starts=$(grep -c '===== DESIGN TOKENS: START' frontend/style.css || true)
ends=$(grep -c '===== DESIGN TOKENS: END' frontend/style.css || true)
[ "$starts" = "1" ] && [ "$ends" = "1" ] \
  || { echo "FAIL: expected exactly 1 fence START and 1 fence END, found $starts/$ends"; exit 1; }

n=$(printf '%s\n' "$outside" | grep -o '#[0-9a-fA-F]\{3,6\}' | wc -l | tr -d ' ' || true)
if [ "$n" != "0" ]; then
  echo "FAIL: $n bare hex outside the token block"
  exit 1
fi
echo "PASS"
exit 0
```
三条纪律(逐字见 `check-03` L8-11 / `check-04` L9-11):**先断言输入存在**、**数 occurrence 不数命中行**
(`grep -o | wc -l`,`|| true` 兜住 `grep` 的 exit 1)、**PASS 打印 "PASS" 且 exit 0**。

**形态 B — 脚本内静态守卫(`_l2_guard_shape`,L1606-1628 逐字)。** 适用于「断言与某个运行时项同族」时:
```python
def _l2_guard_shape(item):
    """L-2 守卫形态(静态):`frontend/style.css` 里 `@media` 出现次数与本次决策一致。

    读的是**文件文本**而非渲染结果 —— 与几何断言互补:它抓「守卫被悄悄删掉 / 悄悄多写
    一条」。读法与 `check_render_markdown_call_sites` 同族:脚本自己从文件文本算,不依赖
    shell 管道;比的是「实测计数 vs 决策」两个独立量,不是自比。
    """
    try:
        text = STYLE_CSS.read_text(encoding="utf-8")
    except OSError as exc:
        blocked(item, "[static] ...", EXPECTED_MEDIA_QUERIES, "<MISSING>", f"{STYLE_CSS} 读不到:{exc}")
        return
    count = text.count(MEDIA_QUERY_DECL)
    lines = [i for i, ln in enumerate(text.splitlines(), 1) if MEDIA_QUERY_DECL in ln]
    info("item8 [static] L-2 守卫形态", f"...计数={count} 命中行={lines};...")
    ok_true(item, "...", count == EXPECTED_MEDIA_QUERIES, EXPECTED_MEDIA_QUERIES, count, "...")
```
同族还有 `_latest_check_max_height_guard`(L2102-2122)与 `check_render_markdown_call_sites`(L935-958)。
共同纪律:**`OSError` ⇒ `blocked()`**、**打印命中行号**、**比的是「实测计数 vs 独立决策常量」不是自比**。

**D-15 中段的四条断言逐条落点建议:**

| 断言 | 形态 | 依据 |
|---|---|---|
| `:focus-visible` 计数 > 0 | 形态 A 或 B(`grep -c ':focus-visible'`) | ROADMAP L289 的 gate 原文 |
| **没有任何焦点规则设置 `border` 或 `padding`** | 形态 A(awk 状态机提取 `:focus-visible` 规则块后 grep `border`/`padding`)| 需要**块提取**,`check-01` L27 的 awk 状态机是最接近的范本 |
| `prefers-reduced-motion` 与新增 transition 同提交 | ⚠ **无法用文件文本断言** —— 「同提交」是 git 维度的事实 | 只能落成**计划/评审义务**;或退化为「两者同时存在」的弱断言并**在 note 里声明它不证明同提交** |
| `--color-focus` 已声明且被消费 | 形态 B(围栏内计数 == 1 + 围栏外 `var(--color-focus)` 计数 > 0)| 硬规则 5「与消费者同提交」的机械形态 |

**⚠ 与 `_l2_guard_shape` 的冲突面(已登记):** D-13 落地后 `EXPECTED_MEDIA_QUERIES` 必须从 0 改成 1
(见上文)。若形态 A/B 也断言 `@media` 计数,两处会同时变红 —— **两处必须一起改**。

---

### 归档合成一次性注入探针(D-18)—— `scripts/probe-07-focus-composite.py`

**Analog:整个 `scripts/probe-05-resolve-color.py`(245 行,tracked)。** 它的**定位**是本阶段必须逐字复刻的:

**定位声明(L1-13 逐字):**
```python
"""probe-05-resolve-color.py — CR-01 的**变异证明**,不是门。

它不进四条守卫命令契约(`check-01`…`check-04`),不被任何门禁 / CI 调用,
`scripts/check-05-ui-uat.py` 也不引用它。存在的唯一目的:把「修复前 PASS /
修复后 BLOCKED」这一对照变成可复跑的证据 —— 变异测试是唯一能证明守卫真的
会失败的手段。
```
⇒ D-18 的探针同样**不进守卫契约**、不被任何门引用。它的价值是「反事实证据」:
证明 `--color-focus ON --color-surface@0.75` 这条算术断言**真的会失败/成立**,而不是静默空转。

**复用 harness 而不复制实现(L63-72 逐字):**
```python
def load_harness():
    """按路径导入 harness(文件名带连字符,不能走普通 import)。

    该文件末尾是 `if __name__ == "__main__": sys.exit(main())`,导入无副作用。
    复用它的 helper 而不是复制实现 —— 否则探针测的就不是真实 helper。
    """
    spec = importlib.util.spec_from_file_location("check05_ui_uat", HARNESS_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
```

**断言辅助 + 退出码(L75-78 逐字):**
```python
def require(cond, msg):
    if not cond:
        print(f"PROBE FAILED: {msg}", file=sys.stderr, flush=True)
        raise SystemExit(1)
```
运行方式与退出码写在 docstring 尾部(L29-32):`0 = 全部断言成立;1 = 任一条不成立(哪一条写到 stderr)`。

**变异必须真的发生的防线(L92-95 / L122-131 逐字)** —— 这是「空转变异」的守卫,D-18 的 DOM 注入同理:
```python
        mutated = "".join(ln for ln in lines if f"{TOKEN}:" not in ln)
        # 空转变异的防线:变异必须真的发生。
        seen["original"] = original
        seen["mutated"] = mutated
        route.fulfill(response=resp, body=mutated)
...
        mutation_applied = bool(seen.get("mutated")) and seen["mutated"] != seen.get("original")
        require(mutation_applied, "变异未发生:mutated 与原始 body 相等")
```

**⚠ 本机 `sed` 陷阱(不得用 sed 做注入,L26-27 逐字):**
```
不用 `sed`:本机是 darwin,BSD `sed` 的 `0,/re/` 地址会**静默不替换**,那会让
变异变成空转、整条证明失去意义(plan 02 已实测并写成纪律)。
```
⇒ D-18 的 DOM 注入必须走 `page.evaluate(...)`(如 item9 的 `renderEvent` / `renderAnnotations` 注入形态,L2301-2324),
**绝不用 `sed` 改磁盘文件**;磁盘上的 `frontend/style.css` 与五个样本**逐字节不变**。

**D-18 的注入内容:** 在 `#round-doc` 内合成一个 `<a href>`(样本里为 0 个,已独立复核),
实测其在 `.archive-mode` 的 `opacity: 0.75`(style.css L1225)合成下的环色渲染值。

---

## Shared Patterns

### 硬规则 3 — 追加,不重排(适用:**每一个** `style.css` 计划)
**Source:** `.planning/ROADMAP.md` L37 + `frontend/style.css` L1230-1232 / L1244 / L1313
本文件所有 Phase 5/6 的追加规则都带同一条尾注(L1230-1232 逐字):
```css
/* 已回应条目:文字弱化(A11Y-04b / D-11 的落地形态)。
   追加在文件末尾 —— 0-2-0 后代选择器,靠源码顺序压过 .annotation-plain .annotation-note(0-2-0)。
   绝不插入、绝不重排(Global Hard Rule 3)。 */
```
⇒ Phase 7 的**每一条**新规则(焦点环、hover、active、过渡、media 块)都必须:① 追加在**文件末尾**;
② 注释里写明「硬规则 3:追加,不重排」;③ 若依赖源码顺序取胜,**必须说明它压过谁**。
**唯一的「不追加」例外是 D-11 的 `.event-list` 300ms —— 那条本来就存在,一个字节都不动。**

### 硬规则 5 — 「与消费者同提交」+ 不得触碰清单
**Source:** `.planning/ROADMAP.md` L39 + `frontend/style.css` L42-46 / L206-208
- 围栏内**不得**声明不被消费的令牌(L42-46 逐字:「Only the steps a tier-2 token consumes in this
  same commit are declared (D-04 / Hard Rule 5 — never declare a token you are not consuming)」)。
  ⇒ `--color-focus` 必须与 `:focus-visible` 规则**同一次提交**;`--color-surface-active` 必须与
  `:active` 规则**同一次提交**。**零新增 tier-1 primitive**(`--radix-gray-4` L51 / `--radix-gray-9` L54
  / `--radix-gray-11` L55 / `--radix-gray-12` L56 全部已声明)。
- 不得触碰(ROADMAP L39):`.fatal` 修饰符、`applyArchiveView` 的两行、`#selection-menu` 的 DOM 位置、
  `showInlineError` 的 `textContent`-only、`renderAnnotations` / `renderVerdictCard`、
  `app.js:4-75` 的约 70 个 `getElementById` 句柄。**本阶段零 JS/HTML 改动,故该清单天然满足。**

### 不变量守卫(适用:任何 `style.css` 改动)—— 执行前后都必须跑
**Source:** `scripts/check-01-token-conformance.sh` / `check-03-hidden-uniqueness.sh` / `check-04-important-count.sh`
```bash
bash scripts/check-01-token-conformance.sh   # 围栏外裸 #hex == 0 且 tier-1 var() 引用 == 0
bash scripts/check-03-hidden-uniqueness.sh   # ^\s*\.hidden\s*\{ 计数 == 1
bash scripts/check-04-important-count.sh     # '!important;' occurrence 计数 == 1
python3 scripts/check-02-contrast.py         # 全部 PAIR 达标 + 清单覆盖地板 + 标记计数自洽
```
**HEAD 基线(已实跑):四条全绿。** 本阶段的具体风险面:
- `check-01`:新的 `#1f63bd` **必须在围栏内**(围栏外裸 hex 会立刻 FAIL);新增规则只能 `var(--color-*)`,
  **不得出现 `var(--radix-*)`**(该脚本 L41-47 的 tier-1 泄漏守卫会抓到)。
- `check-03`:`#selection-menu` 等三个 1-0-0 竞争者的 `display: flex` 规则**不得触碰**(`.hidden` 靠
  `!important` 压它们;L441-445 的注释逐字说明了机制)。
- `check-04`:**D-13 不得引入任何 `!important`**;行业标准的减弱动效片段带两个,会立刻从 1 变 3。
  `check-04` 数的是 **`!important;`(声明)**,不是 `!important`(命中)—— L3-4 逐字说明了这个算术陷阱
  (直接数命中会得 3,其中 2 处是 L13-16 的注释散文)。
- `check-02`:三条新 PAIR 必须逐字符合 `PAIR_RE`(L28-31);清单头部的计数注释必须同步扩写。

### 「防御性非冗余必须写注释」(06-CONTEXT D-09 → D-10 的同型要求)
**Source:** `frontend/style.css` L460-465 与 L481-486(同一段注释写了两遍)
```css
  /* L-3 / D-09:#app 的两个 flex 子项都是 min-width: auto ⇒ flex-basis 不是硬约束,
     min-width: auto 胜出,长不可断内容能把 #doc-panel 顶得比它的 clamp() 还宽。
     上面的 anywhere 落地后 min-content 会塌缩,本行看似冗余 —— 它不依赖「六个目标
     长期全覆盖」,将来新增一个未被 overflow-wrap 覆盖的渲染容器时仍能兜住,
     不得当作冗余代码删除。 */
  min-width: 0;
```
⇒ D-10 的 `input:not(:disabled)`(全站无被禁用的 input/select)与 D-06 的 `[tabindex]` 枚举
(今天无 `[tabindex]` 元素)**都必须照这个形态写注释**:说明「它今天看似冗余,为什么不是」。

### 「名必须说实话」(04.1 D-03 / Phase 5 D-18)
**Source:** `frontend/style.css` L147-168(活动面板标记拒绝复用 `--color-action-primary`)+ L138(Phase 5 不复用)
```css
  /* Tier 2 — the active sidebar panel marker (VISUAL-04 / D-18).

     Deliberately NOT --color-action-primary. That name says "the primary
     action"; reusing it for a panel indicator would make the name lie — the
     same methodology this project already paid for once, when 04.1's D-03
     renamed all 26 primitives for exactly this reason. ... */
  --color-marker-active: var(--radix-blue-11);
```
⇒ D-09 拒绝复用 `--color-surface-user` 承载 active、D-04 拒绝复用 `--color-action-primary` 承载环色
—— 两处注释都必须复刻这段论证形态。

### 「实测驱动,不采信上游文档的论断」
**Source:** `frontend/style.css` L73-116(角色带的四个失效处,逐条给实测数字)+ `check-05` L1598-1601
⇒ D-02 的六项登记、D-03 的比值重算、D-08 的 `opacity` 排除,全部以 HEAD 实测为准。
**规划期已完成的实测:见本文件顶部的「实测人口普查」块。**

---

## No Analog Found

| 文件/片段 | Role | Data Flow | Reason |
|---|---|---|---|
| `:focus-visible` 规则本身 | config | transform | HEAD 上 `:focus` / `:focus-visible` / `outline` 计数**全为 0** —— 全站首次引入作者化焦点样式。形态从 L1313-1324 的枚举纪律与 `check-05` L1683-1685 的普查集推得,无直接先例 |
| `@media (prefers-reduced-motion: reduce)` 块 | config | transform | HEAD 上 `@media` 计数为 **0**(且有一条 `EXPECTED_MEDIA_QUERIES = 0` 的断言在看着它)。**无任何既有 media 块可参照缩进/形态** |
| `:active` 规则 | config | transform | HEAD 上 `:active` 计数为 **0**;D-09 的「同机制加深」是新语汇 |
| D-08 的 `box-shadow: inset 0 0 0 999px rgba(...)` 压暗叠层 | config | transform | 本文件既有的 `box-shadow: inset` 只有 **3px 偏移的竖条**形态(L1087 冻结轮、L1267 活动面板标记),**没有「整面铺满」的 999px 形态**。机制本身无先例,须在注释里自证(「box-shadow 不参与布局 ⇒ 零位移」这条理由有先例,L1084 / L1249-1251) |
| 「`prefers-reduced-motion` 与新增 transition 同提交」的机械断言 | test | transform | 「同提交」是 **git 维度**的事实,文件文本断言无法证明。只能落成计划/评审义务,或退化为弱断言并在 note 里声明其局限 |

---

## Metadata

**Analog search scope:** `frontend/`(style.css / app.js / index.html / vendor)、`scripts/`(check-01…check-06、
probe-05、ui-states/)、`.planning/ROADMAP.md`(全局硬规则 + Phase 7/8 段)、`07-CONTEXT.md`
**Files scanned:** 11(其中 5 份完整读取:`frontend/style.css` 1324 行、`scripts/check-02-contrast.py` 239 行、
`scripts/check-05-ui-uat.py` 定点读 8 段、`scripts/probe-05-resolve-color.py` 2 段、
三条 shell 守卫全文)
**Analog 追踪性:** 全部 analog 路径经 `git ls-files --` 确认 tracked;**零 gitignored 镜像路径**
**Pattern extraction date:** 2026-09-22
**Baseline gate run:** 2026-09-22(HEAD `fcff7e4` 工作树)— check-01/02/03/04 全绿

**遗留待 planner 裁定的三处(本文件已给出先例,但选择本身是计划的活):**
1. **D-08 的 `rgba()` 落点** —— 围栏内令牌(合 R-2 先例)还是规则体内直写(CONTEXT D-08 片段)?见上文「⚠ D-08 的落点决定点」。
2. **D-15 中段契约计数断言的落点** —— 独立零依赖脚本(形态 A)还是 `check-05` 内静态守卫(形态 B)?
   D-15 头部「不新建脚本」与中段「新的零依赖静态断言」的张力须消解;`check-06` 编号已占用。
3. **D-08 的 selector 组织方式** —— 统一选择器列表 vs 按族分组;**必须逐个验证对 Analog D 的九组
   1-0-0 / 0-1-1 规则的特异性**,`button:not(:disabled):hover`(0-2-1)对 1-0-0 无效。
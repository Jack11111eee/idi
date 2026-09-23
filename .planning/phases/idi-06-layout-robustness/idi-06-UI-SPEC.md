---
phase: "6"
slug: "idi-06-layout-robustness"
status: approved
reviewed_at: "2026-09-22"
shadcn_initialized: false
preset: none
created: "2026-09-22"
supersedes_decisions:
  - "04-UI-SPEC Q6(#state-badge:`calc()` vs `position: absolute`)—— 两条分支都被 qrq 的第三种实现取代,见 D-03"
  - "04-UI-SPEC Pitfall 8 的「the fix must not move the badge into normal flow」—— badge 已在正常流,该禁令失去对象"
  - "ROADMAP Phase 6 交付物清单的六项(逐条登记于 §基线与契约漂移口径)"
  - "ROADMAP Phase 6 Success Criterion #3(「只剩一个滚动条」)与 #5(「14px / #8a6508」)"
---

# Phase 6 — UI Design Contract(布局稳健性)

> 前端阶段的视觉与交互契约。由 `gsd-ui-researcher` 生成,由 `gsd-ui-checker` 验证。

## 权威声明 —— 用本文件之前先读这一节

**本文件是增量契约,刻意不是全量契约。** Phase 6 只改 `frontend/style.css` 的布局/换行/定位规则,
不重写已签核的设计系统。与上游契约的关系如下:

| 节 | 权威来源 |
|---|---|
| `## 布局契约`(本文件) | **本文件** —— 它是全新的;上游没有任何一份契约覆盖 Phase 6 的落点(04-UI-SPEC 的 Q5/Q6 只写了**意图**,且其前提已被 HEAD 推翻) |
| `## Spacing Scale` | `04-UI-SPEC.md`(S-1,12 档,已签核)—— **本阶段一字不动**;本文件只登记本阶段的**消费面**与**例外** |
| `## Typography` | `idi-05-UI-SPEC.md`(7 档字号 / 3 档字重 / 4 档行高)—— **本阶段零改动**,只复证 SC5 |
| `## Color` / `## Contrast Verification` | `idi-04.1-UI-SPEC.md`(25 tier-1 / 47 tier-2 / 47 对清单)—— **本阶段零改动**;本阶段**零新增令牌** |
| Design Decisions Q1–Q4 / Q7 | `04-UI-SPEC.md` —— 本阶段不触碰 |
| Design Decisions **Q5 / Q6** | **本文件 §契约修正登记 是它们的最终读法** —— Q5 的围栏仍然有效,但其 `--sidebar-w` 部分失效;Q6 整条被撤销 |
| Global Hard Rules 1–7 | `04-UI-SPEC.md` + `ROADMAP.md` §全局硬规则 —— 本文件 §Global Hard Rules 逐条复述,不改动 |
| Do-Not-Touch List | `04-UI-SPEC.md` + `05-UI-SPEC.md` —— 本文件只**追加** Phase 6 的四条 |

**用本文件之前必须知道的五件事:**

1. **ROADMAP Phase 6 的交付物清单几乎全部需要重新表述** —— 六项已被 HEAD 推翻或前提失效(§基线与契约漂移口径)。
   以那张表为起点读,不要以路线图的清单为起点读。
2. **本阶段零新增令牌。** 围栏 `:root` 内**零改动**;所有取值来自已声明且已被消费的令牌,或已登记的尺寸字面量族。
3. **本阶段是结构性 diff,不是新增规则。** 它改动既有布局规则的**声明**。每个计划必须显式登记它打破的既有断言(D-20)。
4. **`app.js` / `index.html` / `frontend/vendor/` 零改动。** 本里程碑只有 Phase 8 触碰前两者。
5. **`#state-badge` 不回到 `position: fixed`。** 契约 Q6 的 `calc()` 分支与 Pitfall 8 的禁令都已被撤销(D-03);
   本阶段接受 HEAD 的流内机制,并用 `position: sticky` 把「恒可见」补回来。

---

## Design System

| Property | Value |
|----------|-------|
| Tool | none |
| Preset | not applicable |
| Component library | none — native HTML/JS, no framework(DESIGN.md D-06) |
| Icon library | none. 两个内联 `mask-image` 数据 URI 字形(Phase 5 / VISUAL-05)—— 无图标字体、无 sprite 体系、无 vendored 图标集 |
| Font | `-apple-system, "PingFang SC", "Helvetica Neue", sans-serif`(未变) |
| Token substrate | 原生 CSS 自定义属性(单一围栏 `:root`,L5-431)。零构建步骤、零依赖、零新文件 |
| Build step | none(D-06)。无 Tailwind / PostCSS / Sass / lint 流水线 |

**Design-system gate:** `components.json` 与 `tailwind.config.*` 不存在;技术栈是 Python + FastAPI + 原生 HTML/JS。
shadcn **不适用**且未被提议 —— 硬约束 D-06 禁止框架与构建步骤,CSS 自定义属性两者都不需要。无 registry 门适用。

**Component Inventory:本节整节省略** —— `Tool: none`,项目没有设计系统包可枚举(UI-SPEC 模板明令:
`Tool: none` 时省略该节)。本阶段的「组件」是 `style.css` 里既有的选择器,其清单以 `frontend/style.css` 磁盘现状为唯一事实。

---

## 本阶段的改动面(唯一事实)

| 文件 | 改动 | 依据 |
|---|---|---|
| `frontend/style.css` | 围栏外**新增 3 条规则** + **原地修改 5 处既有规则**(删声明 / 加声明) | L-1…L-6 |
| `scripts/check-05-ui-uat.py` | 按 D-06 / D-14 扩写断言 | L-1 / L-4 的门 |
| `frontend/style.css` 围栏 `:root`(L5-431) | **零改动** | 零新增令牌(D-05 / 硬规则 5) |
| `frontend/app.js` / `frontend/index.html` / `frontend/vendor/` | **零改动** | 硬规则 5;`vendor/` 保持只有 `marked.min.js` |
| `scripts/check-01…04` | **零改动**;四条守卫必须仍然通过 | §契约校验命令 |

**新增的 3 条规则(全部为「追加,不重排」,硬规则 3):**

1. `#doc-panel-header { position: sticky; top: 0; background: var(--color-surface); border-radius: 0; }`(L-1)
2. 六目标换行规则 `.markdown-body, .event-content, .chat-bubble, .say-chunk, .annotation-note, .annotation-answer-body { overflow-wrap: anywhere; }`(L-3)
3. `@media` 窄窗口守卫 —— **条件交付物**,仅在实测出破版时落地(L-2)

**原地修改的 5 处(删/加声明,规则块不移动):**

| # | 选择器 | 动作 |
|---|---|---|
| 1 | `.event-list`(`:564-575`) | 删 `max-height: 55vh;` 与 `overflow-y: auto;` |
| 2 | `#annotation-list`(`:913-920`) | 删 `max-height: 32vh;` 与 `overflow-y: auto;` |
| 3 | `#main-pane`(`:453-460`) | 加 `min-width: 0;` |
| 4 | `#doc-panel`(`:468-475`) | 加 `min-width: 0;` |
| 5 | `.annotation-answer summary`(`:991-996`) | 加 `min-height: 24px;` 与 `min-width: 24px;` |

**`#session-panel` 族(`:783-811`)零改动** —— 路线图「改 `flex: 0 0 auto`」被登记为「执行会造成回归」(D-12)。

---

## 基线与契约漂移口径(D-01 / D-02 / D-03)

**D-01:以磁盘 HEAD 为唯一现实基线。** 规划与执行一律以 `frontend/style.css` 的磁盘现状 +
`scripts/check-05-ui-uat.py` 的断言为准;`ROADMAP.md` Phase 6 段、`04-UI-SPEC.md` 的 Q5/Q6 与
`## UI Considerations` **仅作意图参考**。**不动 `04-UI-SPEC.md` / `ROADMAP.md` 正文**(改 ROADMAP 会作废已通过的验证指纹)。

### 六项路线图交付物被 HEAD 推翻 —— 逐条登记

| # | 路线图/契约声称 | HEAD 实况 | 本阶段处置 |
|---|---|---|---|
| 1 | `#state-badge { right: 448px }`(LAYOUT-01 的对象) | **该声明不存在**;badge 是 `#doc-panel-header` 内的流内元素(`:671-679`),无 `position`、无 `right` | **已由 qrq 实现**。LAYOUT-01 的实质(魔法数消除)已达成;本阶段只补「恒可见」(L-1) |
| 2 | LAYOUT-03:「badge 是 `position: fixed` + 不透明背景,正文从其底下穿过被挡」 | badge 不再是 fixed ⇒ **结构上不可能遮挡正文** | **已由 qrq 实现**。本阶段**不得**把它改回 fixed(L-1 的禁令) |
| 3 | Pitfall M2:1280px 重叠 48px / 1024px 重叠 90px | 该算术基于 fixed badge;横幅仍是 `position: fixed; top: 12px; left: 50%` 居中 | **已由 qrq 实现**。残余碰撞实测不存在:相交条件是视口 < 490px,远低于 768px 下限(L-1 的门仍按 768/1024/1280 三处实检) |
| 4 | 「`#session-panel { min-height: 320px }` 改 `flex: 0 0 auto`」 | HEAD 是 `min-height: 200px` + `flex: 1 1 auto`;执行该交付物**会让输入行落到视口之外**,与路线图自己的「输入行必须钉底」矛盾 | **已由 qrq 推翻 + 执行会造成回归**。零改动(D-12) |
| 5 | A11Y-07 边界:「裁决按钮实测约 **21–22px** 高」 | 按 `font-size: 14px` + `padding: 4px 10px` + `border: 1px` + `line-height: normal` 算,盒高约 **26–30px**;21–22px 需 line-height ≈ 0.8×14,不可得 | **数字陈旧,走实测**(L-6) |
| 6 | A11Y-07 边界:「裁决按钮是为在 **420px 侧栏**塞下 **3 个**而故意紧凑」 | 420px 侧栏不存在(`--doc-panel-w: clamp(340px,30vw,480px)`);按钮现为 **2 个**(`app.js:709-711`) | **fence 随前提失效**。实质保留为一般原则,不再构成对本阶段的具体约束(D-18) |

### 两条前提值漂移(不构成推翻,但规划期必须用 HEAD 值)

- `--sidebar-w: 420px` 与 `#sidebar` **均不存在**;实际是 `--doc-panel-w`(`:228`)与 `#doc-panel`。
- `#doc-pane` **不存在**;04.1 D-13 已登记改名为 `#doc-panel-body`。**路线图 LAYOUT-02 的 `#doc-pane { min-width: 0 }` 指向一个不存在的选择器** —— 真正的落点是 `#main-pane` 与 `#doc-panel`(L-3)。

### 契约侧被推翻的文本(逐条撤销,不留悬空引用)

| 被推翻的文本 | 出处 | 撤销依据 |
|---|---|---|
| 「**`calc()`. Committed.**」 | `04-UI-SPEC.md` Q6 | qrq 的第三种实现已在 HEAD 上消掉魔法数、遮挡与碰撞主因;`style.css:668-669` 留有逐字反驳注释。**两条分支(calc / absolute)都不采** |
| 「the fix must not move the badge into normal flow」 | `04-UI-SPEC.md` Pitfall 8 | badge **已在**正常流;禁令失去对象 |
| 「Phase 6 replaces it with `calc(var(--sidebar-w) + var(--space-6))`」 | `04-UI-SPEC.md` Q5 尾段 + L-5 例外行 | 同上;L-5 的豁免对象已消失(剩余例外 L-1 / L-2 / L-4 不变) |
| 「`#sidebar` 的 padding 为 0,会裁切焦点环」 | `ROADMAP.md` Phase 7 段 | `#sidebar` 不存在;真正 0 padding 且 `overflow-y: auto` 的是 `#main-pane` 与 `#doc-panel`(L-5 的普查口径) |
| 「窄窗口的 `@media` 块退化为重赋令牌而零额外规则」 | `ROADMAP.md` Phase 6 交付物第 2 条 | 该形态以 calc() 分支为前提(badge 恒可见需要与面板宽同步)。撤销 calc() 后守卫不再有「必须同步的对象」;若写,其形态是**消费者侧声明或媒体作用域内的 `:root` 重赋**(L-2) |

---

## 布局契约(本阶段核心)

### L-1 徽标收口:流内 badge + sticky 表头

**LAYOUT-01 / LAYOUT-03 / Pitfall M2 三者在 HEAD 上已由流内机制一次性解决。** 本阶段补的是 HEAD 引入的**非自愿丢失**:
`#doc-panel { overflow-y: auto }` 且全文件 `position: sticky` 计数为 **0**,故标题行(含 badge 与折叠指示符)
会随面板内容滚走 —— 这正是 `04-UI-SPEC` Q6 反对 `absolute` 时给出的理由原话,该理由对 HEAD 同样成立。

**落地(新增 1 条规则,插在 `:487-490` 的 `#doc-panel.collapsed #doc-panel-header` 之后):**

```css
/* D-03 / D-05:sticky 表头 —— 把「恒可见」补回来,不改 badge 的流内机制。
   背景是必需的,不是可选:`.panel-header` 规则体内没有任何 background 声明,
   sticky 之后正文会从标题行底下穿过去。`--color-surface` 与 `#doc-panel` 自身背景
   同值且已被消费(`:474`)⇒ 零新增令牌。
   不加 z-index:sticky 元素是 positioned,默认画在静态内容之上;实测若有穿透再补,
   届时须连带登记 `--z-*` 的序关系断言(badge 10 < banner 20 < overlay 100 < selection-menu 200)。
   border-radius: 0:半径在本元素上是加背景之后才**首次可见**的新视觉物,而 10px 圆角
   会让滚动正文从四角露出;全宽条带没有卡片边缘需要圆角。 */
#doc-panel-header {
  position: sticky;
  top: 0;
  background: var(--color-surface);
  border-radius: 0;
}
```

**四条承重约束(缺一即错):**

1. **`#state-badge` 的流内机制一字不动。** 不得给它加 `position`、不得加 `right`、不得移出 `#doc-panel-header`。
   其 `z-index: var(--z-badge)`(`:678`)**必须保留** —— 它在静态元素上是惰性的,但 `check-05` item4
   有活断言 `#state-badge z-index == var(--z-badge)`,删掉会打破既有门。
2. **不加 `z-index`。** 见上;若实测出现穿透,补 `z-index` 时必须同时登记 `--z-*` 序关系(TOKEN-07 的四个令牌各需消费者)。
3. **折叠态零改动。** `#doc-panel.collapsed #state-badge { display: none }`(`:485`)保持;登记为**有意设计**
   (D-04):可折叠面板的语义就是用户主动让出空间,48px 竖条放不下 pill 形态。**与 M2 性质不同** ——
   横幅盖住 badge 是非自愿丢失读数(路线图判为缺陷),折叠是用户主动选择。
4. **特异性核账:** `#doc-panel-header` 是 1-0-0,`.panel-header` 是 0-1-0 ⇒ ID 分量取胜,与源码顺序无关。
   `#doc-panel.collapsed #doc-panel-header`(1-1-0)只声明 `justify-content` / `padding-inline`,与本规则的三条声明无交集 ⇒ **无竞争**。

**已接受的行为(明确声明,不当作缺陷):** sticky 表头在滚动时会覆盖经过其下的正文 —— 这是 sticky 的定义,
不是 LAYOUT-03 的遮挡。判据区别:**覆盖只在滚动过程中发生且内容仍可达**(滚到底后表头停止覆盖,内容全部可达),
而 LAYOUT-03 是浮层永久压住正文。表头高 36px、背景不透明,不产生视觉糊化。

**门(D-06,扩进 `scripts/check-05-ui-uat.py`,三件事):**

1. `#state-badge` 是流内元素(计算 `position` 为 `static`,且无 `right` 声明);
2. **768 / 1024 / 1280 三处** `#state-badge` 与 `#stream-banner` 的 `getBoundingClientRect()` 不相交;
3. 滚动 `#doc-panel` 到底后 `#doc-panel-header` 仍可见(sticky 生效)。

**第 2 条必须补上 768px** —— 路线图 Success Criterion #2 原本只在 1024/1280 两处实检,而 768 是承诺的窄窗口下限。

---

### L-2 窄窗口守卫(条件交付物 —— 实测驱动)

**LAYOUT-02 的范围是「不破版」,不是「适配」。** 判据只有两条,**且都在文档级测量**:

| 判据 | 精确公式 | 承诺边界 |
|---|---|---|
| 无横向溢出 | `document.documentElement.scrollWidth <= document.documentElement.clientWidth` | ≥1024px |
| 无内容被遮挡 | 关键元素 rect 两两不相交(badge × banner、表头 × 正文、按钮 × 视口) | ≥768px |

> **就地注解(2026-09-22,A-10 登记)。** 上表「无内容被遮挡」一行点了三对关键元素,
> 但本阶段**只测量过 `badge × banner` 这一对**(`scripts/check-05-ui-uat.py` 的 badge × banner
> 不相交断言)。**「表头 × 正文」与「按钮 × 视口」两对在本阶段从未被测量过一次**
> (harness / SUMMARY / 任何探针均零命中),且收窄后的承诺**不主张**它们 ——
> 因为 768px 的承诺已按项目所有者本次会话的显式裁定收窄为「badge 不被横幅遮挡」
> (见下方「契约修正登记」表的 A-10 行)。
>
> 原承诺「≥768px 无内容遮挡」在 768–855px 区间**被实测证伪**:`#stream-banner`(fixed、
> 不透明)压住 `#doc-panel-header` 的 h1 —— h1 = 439.0–481.0 × 8–28 vs banner =
> 285.3–482.7 × 12–39,重叠 42×16px。收窄由项目所有者授权(remediation (b)),同时登记在
> `idi-06-VERIFICATION.md` 的 override 条目里。**本表行未被删除、未被重排。**

**三宽度实测:1440 / 1024 / 768。** 工具与「遮挡」的精确判据属 Claude's Discretion,
但**必须产出可复核的原始数值**(三个宽度各一行 `scrollWidth / clientWidth`),不能只给结论。

**面板内部的横向滚动条不算破版,明确不计入:** `#doc-panel { overflow-y: auto }` 会把
`overflow-x` 的 used value 一并算成 `auto`,故一张宽 markdown 表会在**面板内部**产生横向滚动条。
它是**可达内容**,不是文档级溢出,也不是遮挡。**判据一律取文档级 `scrollWidth`。**

**决策规则(条件交付物,必须逐字照做):**

- 实测**在 ≥768px 区间内无破版** ⇒ **不写 `@media`**;把路线图这条交付物登记为「被实测推翻」,
  并附三个宽度的原始数值作为证据。
- 实测**在 768–1023px 之间破版** ⇒ 写**恰好一条** `@media (max-width: 1023px)`。
- 实测**只在 <768px 破版** ⇒ 落在 LAYOUT-02 承诺之外,**登记,不修**(承诺下限是 768px)。

**若写出守卫,其形态被锁死为:**

```css
/* ===== 窄窗口守卫(LAYOUT-02)=====
   字面量例外 L-1,在此显式声明(非疏漏):CSS 禁止在媒体查询条件中使用 var(),
   带 var() 的 @media 会被静默丢弃。1023px 是 Q5 承诺边界(≥1024px 无横向溢出)
   的唯一合法字面量。本块是全文件唯一的 @media。
   范围是「不破版」而非「适配」:无 flex-direction: column、无堆叠布局、无断点阶梯。 */
@media (max-width: 1023px) {
  /* 只放实测证成的声明;取值全部来自已声明令牌,或媒体作用域内 :root 的重赋(L-4 族) */
}
```

| 允许的守卫体 | 禁止 |
|---|---|
| 媒体作用域内 `:root { --doc-panel-w: <字面量> }`(继承例外 L-4:字面量在令牌声明内是合法的,`--doc-panel-w` 现值本就是 `clamp(340px,30vw,480px)`) | `#app { flex-direction: column }` 或任何堆叠布局(Q5 明文 Out of scope) |
| `#doc-panel` / `#doc-panel-body` 上使用**已声明令牌**的声明(如收窄 `#doc-panel-body` 的 `padding: var(--space-8) var(--space-10)`) | 第二条断点、断点阶梯、任何响应式系统 |
| —— | 在媒体查询条件里使用 `var()`(规则会被静默丢弃) |
| —— | 任何 `!important`、任何新令牌、任何 `#hex` |

**断点字面量的门面事实(已核实):** 断点是**非 hex 字面量**,`scripts/check-01-token-conformance.sh` 只统计裸 `#hex`,
不会触发;硬规则 4 禁止 `var(--x, #fallback)`,故「用带 fallback 的 var 绕过」这条路本就被堵死。

---

### L-3 换行与 flex 最小尺寸

**两个声明是一件事的两半,必须同一次落地:**

```css
/* 六目标枚举 —— 与 renderMarkdown() 的调用点一一对应(Phase 5 idi-05-04 已建立该枚举,
   见 `:1229-1262` 的注释与 check-05 的 MARKDOWN_TARGETS)。
   不写通配规则:那会波及已裁定的 `.event-content { word-break: break-all }`(L598-601),
   并把「哪些容器受影响」重新变成不可枚举 —— 那正是 G-idi-05-1 的成因。
   必须用 anywhere 而非 break-word:按 CSS Text 3,只有 anywhere 参与 min-content 内在尺寸计算,
   break-word 不参与 —— 这是下面 min-width: 0 能生效的前提,注释必须写明。
   `.event-content` 已在 `break-all` 之下(break-all 同样影响 min-content),故此处的 anywhere
   对它渲染零影响 —— 仍列入六目标,因为枚举必须与渲染目标一一对应(部分枚举正是缺陷存活的原因)。 */
.markdown-body, .event-content, .chat-bubble, .say-chunk, .annotation-note, .annotation-answer-body {
  overflow-wrap: anywhere;
}
```

```css
/* 加在 #main-pane(`:453-460`)与 #doc-panel(`:468-475`)两条**既有规则体内**,原地加一行。
   #app 的两个 flex 子项都是 min-width: auto ⇒ flex-basis 不是硬约束,min-width: auto 胜出,
   长不可断内容能把 #doc-panel 顶得比它的 clamp() 还宽,不只是撑破主区。
   上面的 anywhere 落地后 min-content 会塌缩,本行看似冗余 —— 它不依赖「六个目标长期全覆盖」,
   将来新增一个未被 overflow-wrap 覆盖的渲染容器时仍能兜住。不得当作冗余代码删除。 */
min-width: 0;
```

**六目标的 HEAD 换行保护现状(已逐条核实):**

| 目标 | HEAD 现状 | 本阶段 |
|---|---|---|
| `.markdown-body` | 零保护 | 加 `anywhere` |
| `.event-content` | `word-break: break-all` + `white-space: pre-wrap`(**已裁定,不动**) | 加 `anywhere`(渲染零影响,枚举完整性) |
| `.chat-bubble` | `word-break: break-word` | 加 `anywhere`(min-content 行为变化) |
| `.say-chunk` | 零保护 | 加 `anywhere` |
| `.annotation-note` | 零保护 | 加 `anywhere` |
| `.annotation-answer-body` | 零保护 | 加 `anywhere` |

**声明组织方式(Claude's Discretion 的裁定):合并为一条六选择器列表**,与 Phase 5 的
「逐容器列举而非一条全局规则」同一口径 —— 它既让影响面机械可枚举,又不误伤 `.event-content` 的既有裁定。
规则**追加在文件末尾**(`:1265` 之后,紧邻 Phase 5 的注入目标枚举注释),不重排任何既有规则。

---

### L-4 滚动容器收敛(LAYOUT-04)

**目标状态:面板区内恰好两个滚动容器 —— `#main-pane`(外层)+ `#latest-check`。**
基线修正:路线图写的 40vh 那只**已不存在**,故基线从「4 个」修正为「3 个嵌套 + 1 个外层」。

| 容器 | HEAD | 动作 | 理由 |
|---|---|---|---|
| `#main-pane`(`:458`) | `overflow-y: auto` | **保留** | 唯一外层滚动者 |
| `#ai-events`(即 `.event-list`,`:568-569`) | `max-height: 55vh` + `overflow-y: auto` | **删两条声明(原地)** | 套娃的第一层 |
| `#annotation-list`(`:917-918`) | `max-height: 32vh` + `overflow-y: auto` | **删两条声明(原地)** | 套娃的第二层 |
| `#latest-check`(`:1115-1116`) | `max-height: 30vh` + `overflow-y: auto` | **保留** | 见下方保留理由 |
| `#chat-messages`(`:791-793`) | `flex: 1` + `min-height: 160px` + `overflow-y: auto` | **保留** | 唯一合理的第二滚动者;输入行必须钉底 |
| `#session-panel`(`:783`) | `flex: 1 1 auto` + `min-height: 200px` | **零改动** | D-12:执行路线图的 `flex: 0 0 auto` 会让输入行落到视口之外 |

**保留 `#latest-check` 的理由(不可省):** 它下方就是 `#check-controls`,而**裁决按钮是交互面**。
去掉限高后,长自检报告会把按钮推到视口之外,必须滚动才能操作 —— 那是**把交互面推到折叠线以下**。

**已接受的代价 —— Success Criterion #3 必须登记偏离:** 路线图写「侧栏内只剩一个滚动条(`#chat-messages` 除外)」;
本阶段的实际目标状态是**面板区内恰好两个滚动者**(`#main-pane` + `#latest-check`)。

**删除时必须原地改声明,不得移动规则块(硬规则 3)。** `.event-list` 的其余声明
(`display` / `flex-direction` / `gap` / `border` / `border-radius` / `padding` / `background` /
`transition: background-color 0.3s` / `.streaming` / `.aborted` 三条)一字不动;
`#annotation-list` 的 `display` / `flex-direction` / `gap` / `padding` 一字不动。

**门(D-14,扩进 `scripts/check-05-ui-uat.py`,三件事):**

1. 面板区内计算 `overflow != visible` 的滚动容器**恰好两个**(`#main-pane` + `#latest-check`)—— 按 **DOM 普查**而非硬编码选择器;
2. 两者都能滚到底(内容可达性);
3. `#ai-events` / `#annotation-list` 的计算 `max-height` 为 `none`。

口径取「**恰好两个**」而非「至多两个」,以便抓到「意外新增第三个滚动者」这类回归。

---

### L-5 焦点环解裁切(普查口径 —— 本阶段不写任何 `:focus` 规则)

**本阶段的义务是「解裁切」,不是焦点样式本身**(A11Y-01 归 Phase 7)。**零 `:focus` / `:focus-visible` 规则。**

**普查口径(Claude's Discretion 的裁定):按可聚焦元素枚举,不按容器名。** 判据:

> 一个**裁剪容器**(计算 `overflow != visible`)必须让它的每一个可聚焦后代距离其 **padding 边**至少 **4px**,
> 否则该容器需要抬 padding。4px = Phase 7 的 `outline: 2px solid` + `outline-offset: 2px` 的环外伸量。

**静态分析的预期结论(必须由实测确认或推翻,不得直接采信):**

| 容器 | HEAD padding | 可聚焦后代 | 预期 |
|---|---|---|---|
| `#annotation-list` | `var(--space-half)` = **2px** | 有 —— `app.js:1150-1156` 的 `<details>` + `<summary>`(`<summary>` 默认可聚焦) | **无裁切**:该 `<summary>` 嵌在 `.annotation-item` 内,距列表 padding 边 = 2px(列表)+ 1px(卡片 border)+ 10px(卡片 padding)= **13px** ≥ 4px |
| `#chat-messages` | `var(--space-1) var(--space-half)` = 4px 2px | **无** —— 气泡是 `div`(`app.js:260-262`)与 `p`/`div`(`app.js:282`),无 `button`、无 `details`/`summary` | **空动作**,零改动 |
| `#latest-check` | `var(--space-1-5) var(--space-2)` = 6px 8px | 无(只渲染 markdown 元素) | 零改动 |
| `#main-pane` | **0** | 有 | **无裁切**:可聚焦元素的最浅祖先链含 `.panel-body { padding: 10px }`(`:524`),故距 `#main-pane` 的 padding 边 ≥10px |
| `#doc-panel` | **0** | 有 | **无裁切**:`#doc-panel-body { padding: 32px 40px }`(`:501`) |

**即:预期结论是「零 padding 改动」—— 路线图点名的两个容器都是空动作。**
`#annotation-list` 的 2px 看似危险,但其唯一可聚焦后代嵌在自带 padding 的卡片里;
`#chat-messages` 的 2px 则根本没有服务对象。

**决策规则:**

- 实测与上表一致 ⇒ **不改任何 padding**;把这条交付物登记为「被实测推翻」,附普查原始数据(元素 × 最近裁剪祖先 × 实测 clearance)。
- 实测发现某个容器 clearance < 4px ⇒ **只改那一个容器**,取值 `var(--space-1)`(4px),并在
  §Deliberate Delta Ledger 登记为**视觉变更**。
- **禁止「为确定性四个全抬」** —— 它会移动 `#main-pane` 居中布局下的 section 位置,并与
  `#doc-panel-body` 的既有 padding 叠加;这类「顺手统一」正是 Pitfall 8 的范围蔓延。

**为什么这个口径与 Phase 5 的 G-idi-05-1 同构:** 按容器名/点名枚举会漏掉没被点名的那个
(A11Y-07 的实例见 L-6);按元素普查能抓到。本阶段两处普查(可聚焦元素 / 可交互元素)采用同一口径。

---

### L-6 紧凑控件命中区(A11Y-07)

**判据:** 每个**可交互元素**的计算盒 `getBoundingClientRect()` 的宽与高均 ≥ **24px**(WCAG 2.5.8 Target Size Minimum, AA)。
**按字面走尺寸,不走 2.5.8 的间距例外** —— A11Y-07 明文要求「达到 24×24」。

**机制(已锁定,不再讨论):** `min-height: 24px` + `min-width: 24px`。**不动现有 `padding`**
(改 padding 改的是外观而非命中区,且连锁影响行高与相邻间距观感);**不用 `::after` 撑开**
(`.verdict-buttons { gap: var(--space-2) }` = 8px,扩展后的相邻命中区会**互相重叠**,反而可能违反
2.5.8 的「不与他者相交」要求)。

**落地(原地加两行到 `.annotation-answer summary`,`:991-996`):**

```css
/* A11Y-07(WCAG 2.5.8 目标尺寸):24×24。
   24 是**目标尺寸常数**,刻意不耦合 `--space-6`:把 WCAG 下限挂在间距刻度上,会让一次间距
   改动静默地把命中区压到下限之下 —— 这是「名必须说实话」的同一条方法论(D-17 拒绝把 3px
   box-shadow 偏移塞进 --space-* 刻度是同一判断)。
   本文件已有同一族的未令牌化**尺寸**字面量:`min-height: 160px/200px/52px`、`min-width: 96px`、
   `height: 36px` —— `--space-*` 刻度覆盖的是 padding / margin / gap,不覆盖尺寸。 */
min-height: 24px;
min-width: 24px;
```

**普查表(已逐条核实;`✓` = 预计已达标,`✗` = 确定不达标):**

| 控件 | 盒高估算 | 判定 |
|---|---|---|
| 所有 `<button>`(`button { padding: 6px 10px }` + 1px border,`:551-559`) | ≈ line-height + 14 ≈ **30–34px** | ✓ |
| `#selection-menu button`(`#btn-annotate` / `#btn-plain-ask`) | 同上 ≈ **30px** | ✓ |
| `.verdict-buttons button`(padding 覆盖为 4px 10px,`:1175`) | ≈ **26–30px** | 待实测;**很可能已达标** |
| **`.annotation-answer summary`**(`font-size: var(--text-xs)` = 12px,无 padding、无 min-height) | ≈ **14–17px** | ✗ **确定不达标** |
| `.collapse-indicator` | `<span>`,属**不得触碰**(硬规则 5 / 05-CONTEXT D-23);其可点父级 `.panel-header` 为 36px | ✓(父级达标) |

**即:REQUIREMENTS 点名的裁决按钮很可能本来就达标,而唯一确定不达标的是 `.annotation-answer summary`**
(`<details>` 的展开控件)—— 它正是「等紧凑控件」里那个「等」所指,却未被点名。

**决策规则:**

- 实测已 ≥24×24 的控件 ⇒ **零 CSS 改动**,登记为「被 HEAD 推翻」并附实测 rect。
- 实测不足 ⇒ **只对未达标者**施加 `min-height` / `min-width`,形式是**原地加两行到该控件的既有规则体**
  (选择器全文唯一时原地改写与追加在层叠上等价,且不留重复选择器 —— 05-UI-SPEC D-21 先例);
  若某控件没有既有规则,则以一条新规则追加在文件末尾。**任何这类改动都是视觉变更,必须进 §Deliberate Delta Ledger。**

**已登记的视觉变更(由机制直接推出,不是副作用):** `.annotation-answer summary` 从 ≈14–17px 抬到 24px,
**会改变 `.annotation-item` 的高度**(每个带 AI 回复的批注条目 +7…10px)。这是 D-17 明文要求显式登记的变更。

**fence 状态(D-18):**「若与布局冲突,不得为此重构侧栏」的**前提两处都已不成立**(420px 侧栏不存在;
按钮已从 3 个变 2 个)。其**实质**(不为命中区去重构侧栏)保留为一般原则,但**不再构成对本阶段的具体约束**。

---

### 交互状态契约(本阶段零新增)

| 交互面 | 本阶段 | 约束 |
|---|---|---|
| `:hover` / `:active` / `:disabled` | **零新增规则** | INTERACT-01 / INTERACT-02 归 Phase 7。既有 `button:hover`(`:560`)与八处 `:disabled` 一字不动 |
| `:focus` / `:focus-visible` | **零新增规则** | A11Y-01 归 Phase 7。本阶段只为它解裁切(L-5) |
| transition | **零新增** | 既有的 `.event-list { transition: background-color 0.3s }`(`:574`)保留,不改不删 |
| `#doc-panel-header` | 可点(折叠开关),高 36px | 已 ≥24×24;**不新增任何 hover / cursor 变化**(`cursor: pointer` 来自 `.panel-header`) |
| `.annotation-answer summary` | 可点,命中区 24×24 | 既有 `cursor: pointer`(`:992`)保留;不新增 hover |
| `#state-badge` / `#stream-banner` | **非交互** | 不得为它们加任何交互态 |

**软化的禁令重申:** `:disabled` 是 G3 前提条件唯一的视觉信号,**不得软化**(Pitfall M5)。
本阶段不新增、不修改任何 `:disabled` 规则。

---

## Spacing Scale —— 已签核,本阶段只登记消费面与例外

**`04-UI-SPEC.md` 的 12 档刻度(S-1)本阶段一字不动。** 本节只登记两件事:本阶段**消费**哪几档,以及**例外**。

| Token | Value | 本阶段的消费 |
|-------|-------|-------------|
| `--space-1` | 4px | **条件**:L-5 的 padding 解裁切(仅在实测 clearance < 4px 时) |
| `--space-6` | 24px | **条件**:L-2 的守卫体内收窄 `#doc-panel-body` padding(若写出守卫) |
| (无) | 0 | L-1 的 `top: 0` —— 单位less `0`,例外 L-2(复位不是设计值) |

**本阶段不新增任何间距字面量,也不新增例外行。** 理由:

- L-1 的 `top: 0` 命中已有例外 **L-2**(unitless `0`)。
- L-2 的断点字面量命中已有例外 **L-1**(条件声明:仅在写出 `@media` 时于该段首的围栏注释里声明,
  理由:CSS 禁止在媒体查询条件中使用 `var()`,该规则会被静默丢弃)。**实测无破版则不声明、不落地。**
- L-2 守卫体内若重赋 `--doc-panel-w`,其字面量在**令牌声明内**,命中已有例外 **L-4**
  (「`--sidebar-w: 420px` 是字面量**在围栏内**;它是令牌,围栏就是字面量该在的地方」)。
- L-6 的 `24px` 是**尺寸**字面量,不是间距字面量 —— 见下方声明。

**A11Y-07 的 `24px` 为什么不是间距刻度的违规(显式声明,防被读成疏漏):**
`--space-*` 刻度覆盖 padding / margin / gap(04-UI-SPEC 的「14 个 padding / 11 个 margin / 5 个 gap」即其全量)。
`min-height` / `min-width` 是**尺寸**族,HEAD 上本就未被令牌化且从不入刻度:
`min-height: 160px`(`#chat-messages`)、`min-height: 200px`(`#session-panel`)、`min-height: 52px`(`#chat-input-row input`)、
`min-width: 96px`(`.modal-buttons button`)、`height: 36px`(`.panel-header`)、`width/height: 12px`(两处 `::before` 字形)。
**故 `24px` 落在这个既有族里,不产生新的例外行,也不触发 CHECK-01(它只统计裸 `#hex`)。**
**刻意不写成 `var(--space-6)`** —— 见 §Sign-Off Items S-3。

**例外清单(本阶段结束时的完整状态):** L-1(条件)/ L-2 / L-3(**已被 Phase 5 整个撤掉**)/ L-4 / L-5(**豁免对象已消失,行本身留证**)。

---

## Typography —— 本阶段零改动,只复证 SC5

**`idi-05-UI-SPEC.md` 的排版契约全部继续有效:7 档字号(12 / 14 / 16 / 18 / 22 / 24 / 28)、
3 档字重(400 / 500 / 600)、4 档行高。本阶段一个字号、一个字重、一行行高都不动。**

| Role | Size | Weight | Line Height |
|------|------|--------|-------------|
| 文档正文(本体) | `--text-md` 16px | `--fw-regular` 400 | `--lh-reading` 1.625 |
| chrome 标题 / 标签 | `--text-base` 14px | `--fw-medium` 500 | 继承 |
| 批注 / 事件条目 | `--text-base` 14px | `--fw-regular` 400 | `--lh-snug` 1.4286 |
| 文档 h1 | `--text-3xl` 28px | `--fw-semibold` 600 | `--lh-tight` 1.3333 |
| 嵌入目标 h1(五容器) | `--text-xl` 24px | `--fw-semibold` 600 | 继承 |
| 徽标 / 说明 | `--text-xs` 12px | `--fw-semibold` 600 | 继承 |

**SC5 的读法(必须按这个读,ROADMAP 的字面值是陈旧的):**
ROADMAP Phase 6 Success Criterion #5 写「`#brainstorm-view h2` 仍计算为 14px / `#8a6508`」——
**两个值都已失真**(实测 `var(--text-md)` = 16px / `var(--color-action-warning)` = `--radix-amber-12` = `#4f3422`;
`#8a6508` 在围栏里根本不存在)。SC5 的**实质**是「结构改动没有把 chrome 覆盖带偏」,其机械形态是
**`check-05-ui-uat.py` item4 的两条令牌接线断言仍然通过**:

```
[p1] #brainstorm-view h2 font-size == var(--text-md)          ← resolve_token 期望侧
[p1] #brainstorm-view h2 color      == var(--color-action-warning)
```

**本阶段对排版的两条硬约束:**

1. **不得新增/修改任何 `font-size` / `font-weight` / `line-height` 声明。** L-6 的 `min-height`/`min-width` 不是排版声明。
2. **不得触碰 `.collapse-indicator`**(`font-size: 20px; line-height: 1`)—— backlog `999.1` 第 1 项,
   硬规则 5 / 05-CONTEXT D-23 明文禁止。它是围栏外**唯一**的越轨排版字面量,本阶段**留证不修**。

---

## Color —— 本阶段零改动

**`idi-04.1-UI-SPEC.md` 的 25 个 tier-1 / 47 个 tier-2 / 47 对清单全部继续有效。本阶段零颜色改动、零新增令牌。**

| Role | Value | Usage |
|------|-------|-------|
| Dominant (60%) | `--color-surface-page` `#fcfcfc` / `--color-surface` `#f9f9f9` | 页面与面板底、卡片、控件 |
| Secondary (30%) | `--color-surface-sunken` `#f0f0f0` + `--color-border*` | 面板 chrome、分隔线、徽标、事件列表 |
| Accent (10%) | `--color-action-primary` `#0d74ce` / `--color-action-warning` `#4f3422` | 见下方「Accent reserved for」 |
| Destructive | `--color-action-danger` `#ce2c31` | 仅破坏性动作 |

**Accent reserved for:** 主要动作按钮(发送 / 进入 / 同意 / 放行)、`#btn-divergence`、`#state-badge`、
`mark` 高亮、活动面板标记(Phase 5)。**绝不含「所有交互元素」。** 绿色三档是**动作族**而非 accent。

**本阶段唯一涉色的地方(且不是颜色改动):** L-1 的 sticky 表头背景复用 `var(--color-surface)` ——
该令牌**已被 `#doc-panel` 消费**(`:474`),故不违反硬规则 5(不得声明一个在同一次提交中不被消费的令牌)。

**两条不得触碰的对比度不变量:**

1. **`#stream-banner` 的 `.fatal` 修饰符必须保留为独立选择器**(`:696`)—— 两态 4.78:1 / 4.76:1 继续达 AA。
   L-1 的门断言的是 badge 与 banner 的**几何不相交**,不得以「弱化横幅」或「移动横幅」来通过。
2. **`--color-marker-active` 的 inset 竖条只在 `#session-panel` / `#annotations-panel` / `#checks-panel` 三条
   ID 选择器上**(`:1218-1227`),`#doc-panel-header` 刻意**不被**匹配。L-1 给 `#doc-panel-header` 加背景
   **不得**顺带给它加竖条或改它的 h1 颜色。

---

## Copywriting Contract —— 本阶段改动零文案

**本阶段不改任何面向用户的字符串。** 它不新增元素、不改按钮、不改提示、不改空态与错误态。
下表**冻结既有文案**,使后续阶段有参照且不能静默漂移(与 `04-UI-SPEC.md` / `idi-05-UI-SPEC.md` 一致)。

| Element | Copy(frozen —— 逐字来自 `index.html`) |
|---|---|
| Primary CTA(进入) | `进入` |
| Primary CTA(会话) | `发送` |
| 例行循环动作 | `处理本轮批注` |
| 继续动作 | `继续自检` / `继续修复` |
| 提交动作(G1) | `认可雏形` |
| **不可逆动作(G3 —— 核心价值红线)** | `授权撰写总设计文档` |
| 闸门确认 | `放行` / `拒绝` |
| 空态(会话流) | 居中问候语由 `#chat-greeting` 承担(纯 CSS 空态,`app.js` 零改动) |
| 空态(批注流) | `本轮暂无批注——在左侧文档划词即可批注。` / `该轮暂无批注。` |
| 错误态(内联) | `showInlineError(anchor, message)` —— 服务端消息,`textContent`-only |
| 错误态(G3 确认) | `#confirm-error` —— 必须渲染为**红色**而非灰色(Pitfall M6) |
| 破坏性确认 | 本阶段无。`拒绝` / `中止` 是破坏性控件,两者都不增减确认步骤 |
| 断流横幅 | `事件流已断开,正在自动重连……`(L-1 的 768px 碰撞实检用的就是这个字符串) |

**文案规则(后续阶段适用,记录在此以防被重新发明):**
- 面向用户的输出遵守 DESIGN.md §3.8 语言红线 —— 简洁精准、大白话定义术语;讨论文档以中文为主。
- **错误文本绝不经 `innerHTML` 渲染**(T-260916-01)。
- G3 授权按钮的标签是核心价值红线唯一的文字,其对比度是唯一不得为美观让路的配对。

**本阶段的文案相关面(说明为什么本表是冻结而非新增):** L-6 让 `.annotation-answer summary` 的**命中区**变大,
其**文本**(`AI 回应` / `大白话回答`,来自 `app.js:1150-1152`)一字不动;
L-1 让表头**恒可见**,其**文本**(`文档区`)一字不动。**本阶段没有任何一处新增或改写字符串。**

---

## Deliberate Delta Ledger(本阶段)

**每一项都是刻意的视觉/行为变更。没有列的就不是变更。**

| # | 变更 | 视觉/行为 delta | 依据 | 门 |
|---|---|---|---|---|
| D6-1 | `#doc-panel-header` 获得 `background: var(--color-surface)` | 文档面板标题行**首次可见为一条 36px 条带**(此前无背景,不可见)。同色于面板底 ⇒ 仅在与正文重叠时才可辨(即滚动时,这正是目的) | L-1 | check-05:滚动后表头仍可见 |
| D6-2 | `#doc-panel-header { border-radius: 0 }` | 半径在加背景之前**不可见**,故此项的净 delta 是「不让圆角在滚动时从四角露出正文」。**不移动任何像素**(半径不参与布局) | L-1 / S-1 | 无(与 HEAD 的折叠态布局等价) |
| D6-3 | `.annotation-answer summary` 从 ≈14–17px 抬到 ≥24px | **`.annotation-item` 高度 +7…10px**(每个带 AI 回复的批注条目) | L-6 / D-17 | check-05:实测 rect ≥24×24 |
| D6-4 | `.event-list` 删 `max-height: 55vh` + `overflow-y: auto` | AI 面板不再内部滚动,随事件增长 ⇒ 由 `#main-pane` 滚动。**行为变更,不是纯视觉** | L-4 / D-11 | check-05:`max-height` 计算为 `none`;滚动者恰好两个 |
| D6-5 | `#annotation-list` 删 `max-height: 32vh` + `overflow-y: auto` | 批注面板同上 | L-4 / D-11 | 同上 |
| D6-6 | 六目标加 `overflow-wrap: anywhere` | 四个**零保护**容器(`.say-chunk` / `.annotation-note` / `.annotation-answer-body` / `.markdown-body`)里不可断长内容**由溢出改为折行**;`.chat-bubble` 的 min-content 行为变化(视觉近似,`break-word` → `anywhere`) | L-3 / D-07 | 运行时:768px 无横向溢出 |
| D6-7 | `#main-pane` / `#doc-panel` 加 `min-width: 0` | **正常情况下零 delta**;仅在长不可断内容存在时阻止 flex 项被顶宽(即它是 D6-6 的兜底,不是独立视觉变更) | L-3 / D-09 | 同上 |
| D6-8 | `#state-badge` 随 sticky 表头恒可见 | **行为修正**(非视觉变更):面板滚动时状态读数不再丢失 | L-1 / D-03 | check-05:三宽度不相交 + 滚动后可见 |
| D6-9 | **(条件)** `@media` 守卫体内的声明 | 仅在 768–1023px 区间;内容见 L-2。**实测无破版则本项不存在** | L-2 / D-08 | 三宽度原始数值 |
| D6-10 | **(条件)** L-5 的 padding 解裁切 | 仅在实测 clearance < 4px 的容器上,+2px(2px → `--space-1` 4px),会移动该容器内的条目位置 | L-5 / D-13 | 普查原始数据 |

**本阶段明确不产生的 delta:** 零颜色改动、零字号/字重/行高改动、零新增令牌、零新依赖、
零新文件、`app.js` / `index.html` / `vendor/` 零字节改动。

---

## 契约修正登记(全部由已锁定决策产生,不是新问题)

| # | 修正 | 依据 | 影响 |
|---|---|---|---|
| **A-1** | `04-UI-SPEC.md` **Q6 整条撤销**(calc() / absolute 两条分支都不采) | D-03 | 本文件的 L-1 是该问题的最终读法;`04-UI-SPEC.md` 正文**不改**(改它会作废已通过的验证指纹) |
| **A-2** | `04-UI-SPEC.md` **Pitfall 8 的「must not move the badge into normal flow」撤销** | D-03 | 禁令失去对象(badge 已在正常流)。**其余 Pitfall 8 条款(不重构 header、不重设计响应式、不动 `#selection-menu` 定位数学)全部继续有效** |
| **A-3** | `04-UI-SPEC.md` **L-5 例外行**的豁免对象消失(原:`#state-badge { right: 448px }`) | D-02 第 1 项 | 剩余例外 **L-1 / L-2 / L-4** 不变;**L-3 已由 Phase 5 撤掉** |
| **A-4** | **`#doc-pane { min-width: 0 }` 更正为 `#main-pane` + `#doc-panel`** | D-09 | 原选择器在 HEAD 上不存在;落点是 `#app` 的两个 flex 子项 |
| **A-5** | **SC#3 措辞收窄为「面板区内恰好两个滚动者(`#main-pane` + `#latest-check`)」** | D-11 | **不改 `REQUIREMENTS.md` / `ROADMAP.md`**(改会作废指纹),只在计划与验证记录里登记 |
| **A-6** | **SC#5 措辞更正为令牌接线表述**(`var(--text-md)` / `var(--color-action-warning)`),不是 `14px / #8a6508` | 04.1 C-1 + Phase 5 D-02 | 同上,只登记不改文件 |
| **A-7** | **A11Y-07 的两处边界前提失效**(21–22px 数字 / 420px 侧栏 3 个按钮) | D-02 第 5/6 项 + D-18 | fence 不再构成本阶段的具体约束 |
| **A-8** | **LAYOUT-04 基线从「4 个滚动容器」更正为「3 个嵌套 + 1 个外层」** | D-11 | 路线图写的 40vh 那只已不存在 |
| **A-9** | **`ROADMAP.md` Phase 7 段的「`#sidebar` 的 padding 为 0」更正为 `#main-pane` / `#doc-panel`** | D-13 | 路线图内部不一致;本阶段只登记,不改文件 |
| **A-10** | **LAYOUT-02 的 768px 承诺收窄为「badge 不被横幅遮挡」**(原为「无内容遮挡」) | **用户本次会话显式裁定 remediation (b)** | 该遮挡是**既有几何**,且被本阶段自己的范围锁排除在可修范围之外:`#stream-banner` 的任何声明不得触碰(`:665`)、`--doc-panel-w` 的值由用户裁决(`frontend/style.css:224-227`)、唯一合法的 `@media` 形态在几何上不可能(需面板 ≤285.3px,而 clamp 下限是 340px)。实测证伪:h1 = 439.0–481.0 × 8–28 vs banner = 285.3–482.7 × 12–39,重叠 42×16px,相交带 768–855px。**跟随 A-5 先例**:只登记在计划与验证记录里,`REQUIREMENTS.md` / `ROADMAP.md` 不改(改会作废指纹)。这是**已登记的偏离,不是静默通过**;同时见 `idi-06-04-PLAN.md` / `idi-06-04-SUMMARY.md` 与 `idi-06-VERIFICATION.md` 的 override 条目 |

---

## Sign-Off Items(S-1 / S-2 / S-3 —— 需要用户裁定,不是 checker 裁定)

三项都是 Claude's Discretion 或本次研究得出的、**会改变一个已签核交付物存在与否**的判断。
规划期须把三项呈给用户**逐项裁定**;任一项被否决即按替代方案执行。

| # | 裁定项 | 本文件的建议 | 一行式替代方案 | 若不裁定的后果 |
|---|---|---|---|---|
| **S-1** | **sticky 表头的 `border-radius` 取哪个** | **`border-radius: 0`**(仅 `#doc-panel-header`)。理由:半径在加背景后才首次可见,10px 圆角会让滚动正文从四角露出;全宽条带没有卡片边缘需要圆角;`0` 不移动任何像素 | 保留 `var(--radius-md)`,接受四角露出(或改只圆下缘 `border-radius: 0 0 var(--radius-md) var(--radius-md)`) | 规划期会把它当成一个未决的美术细节反复讨论 |
| **S-2** | **L-5 的预期结论是「零 padding 改动」** —— 路线图点名的两个容器在 HEAD 上都是空动作(静态分析:唯一可聚焦后代嵌在自带 10px padding 的卡片里,clearance 13px)。是否接受「登记为被实测推翻」而非「为确定性抬两个容器」? | **接受**:只在实测 clearance < 4px 时改,且只改那一个容器。理由:`#main-pane` 的 padding 抬升会移动其居中布局下的 section 位置,并与 `#doc-panel-body` 的 32/40px 叠加 —— 是真实的视觉变更,不是免费的保险 | 「四个全抬,以 padding 换确定性」—— 代价是两处计划外视觉位移 + 与 L-4 的滚动容器数统计相互干扰 | 执行器可能「顺手统一」抬四个容器(Pitfall 8 的范围蔓延) |
| **S-3** | **A11Y-07 的 `24px` 写法** | **裸字面量 `24px`**(尺寸族,非间距族)。理由:24 是 WCAG 2.5.8 的目标尺寸常数;写成 `var(--space-6)` 会把 a11y 下限**耦合**到间距刻度上 —— 一次间距改动静默地把命中区压到下限之下,而本阶段的全部方法论都反对这种耦合(D-03 撤销 calc() 的理由就是「把一个魔法数换成另一个耦合」) | `min-height: var(--space-6); min-width: var(--space-6);` —— 值相同、单源更强,代价是引入了上述耦合 | 规划期会把它当成 spacing-scale 的违规去处理,或反过来把它令牌化后留下耦合 |

---

## 契约校验命令

**四条既有守卫本阶段必须全部仍然通过(零改动):**

```bash
bash scripts/check-01-token-conformance.sh   # 围栏外裸 #hex = 0(断点字面量不触发:它非 hex)
python3 scripts/check-02-contrast.py         # 47 对清单全部达 AA(本阶段零颜色改动 ⇒ 必须逐字不变)
bash scripts/check-03-hidden-uniqueness.sh   # ^\.hidden { 计数 == 1
bash scripts/check-04-important-count.sh     # !important **声明**数 == 1(注意:grep -c 会数到 L13-14 的注释散文)
```

**本阶段扩写的两条门(D-06 / D-14 —— 扩进 `scripts/check-05-ui-uat.py`,不新建脚本):**

```bash
python3 scripts/check-05-ui-uat.py --item 8   # L-1 的门:流内 badge + 768/1024/1280 不相交 + 滚动后表头可见
python3 scripts/check-05-ui-uat.py --item 9   # L-4 的门:面板区滚动者恰好两个 + 两者可滚到底 + 两处 max-height == none
```

**必须保留的既有门(本阶段会打破它们的表面形态,但不得打破断言本身):**

```bash
python3 scripts/check-05-ui-uat.py --item 4   # 含 SC5 的两条令牌接线断言 + #state-badge z-index == var(--z-badge)
python3 scripts/check-05-ui-uat.py --item 7   # 九个 renderMarkdown 目标的标题刻度
python3 scripts/check-05-ui-uat.py --item 1   # 五态显隐(.hidden 的层叠证据)
```

**执行前基线(硬要求,D-20):** 规划期必须先跑一遍 HEAD 上的全部门,建立「执行前基线」,
再逐条登记本阶段会打破的既有断言。至少包含:`check-05` 中与 `#chat-messages` / `#annotation-list` /
`#latest-check` 的 `max-height` / `overflow` 相关的条目(若存在)、与 `#session-panel` 相关的条目、
以及 Success Criterion #3 的表述。

**运行时验证不可省(硬规则 7):** 每个 `style.css` 计划都必须带**至少一项运行时验证**。
`grep -c 'var(--'` 对渲染结果零证明力。本阶段的三项运行时判据:三宽度文档级 `scrollWidth`、
滚动者 DOM 普查、可交互元素 `getBoundingClientRect()`。

---

## Global Hard Rules(每个 Phase 6 计划都适用)

1. `grep -c '^\.hidden {' frontend/style.css` 必须等于 **1**。`.hidden { display: none !important }` 是**机制而非样式**:
   不得令牌化、不得移动、不得弱化、不得用 `:where()` 降特异性。三个 ID 特异性竞争者
   (`#selection-menu` / `#annotations-panel` / `#checks-panel`,均 1-0-0)靠它压制。
2. `style.css` 中含 `!important` 的**声明行**数为 **1**。算术陷阱:直接 `grep -c '!important'` 返回 3(两行是注释散文)。
3. **追加,不重排。** 至少一对等特异性规则由源码顺序决定(`#draft-view > h2` 与 `#brainstorm-view > h2`,同为 1-0-1)。
   **本阶段是结构性 diff,重排风险比 Phase 5 更高** —— 任何删除 `max-height` / `overflow-y` 的操作都必须**原地改声明**,
   不得移动规则块。源码 diff 看起来无辜,渲染会变。
4. 不得新增 `!important`;不得令牌化 `display`;不得引入 `@layer` / `@property` / `var(--x, #fallback)`。
5. **不得触碰:** `.fatal` 修饰符;`applyArchiveView` 的两行(`app.js:817-818`);`#selection-menu` 的 DOM 位置与定位数学;
   `showInlineError` 的 `textContent`-only 规则(XSS 缓解 T-260916-01);`renderAnnotations` / `renderVerdictCard`;
   `app.js:4-75` 的约 70 个顶层 `getElementById` 句柄(id 不得改名或删除);`.collapse-indicator`;
   `#state-badge` 的 `z-index: var(--z-badge)` 声明;`#session-panel` 族的任何声明。
6. 零新增运行时依赖、零构建步骤(D-06)。CHECK-01/02 必须保持零依赖。
7. 每个 `style.css` 计划都必须带**至少一项运行时验证**。
8. **本阶段零新增令牌**(围栏 `:root` 内零改动)。不得顺手声明任何 `--x`。
9. **不得声明任何 `:focus` / `:focus-visible` / `:hover` / `:active` / `transition` 规则**(Phase 7)。

---

## Do-Not-Touch List(继承 + 本阶段追加)

**继承(逐条复述,来源:`04-UI-SPEC.md` + `05-UI-SPEC.md`):**
`.hidden` 唯一性与其注释 · `!important` 声明数 = 1 · `.fatal` 两态 · `#selection-menu` 的 DOM 位置与定位数学 ·
`showInlineError` 的 `textContent`-only · `renderAnnotations` / `renderVerdictCard` · `app.js:4-75` 的约 70 个 id ·
`applyArchiveView` 两行 · `#round-doc.round-frozen` 的 `filter: saturate(0.6)` + 琥珀 inset ·
`.annotation-answered` 的 `--color-text-muted` 弱化 · 五处 `.panel-header` 的活动标记 ·
嵌入目标的标题刻度规则(`:1263-1265`)· `#round-switcher` / `#check-switcher` 的 token 接线。

**本阶段追加:**

| 不得触碰 | 理由 |
|---|---|
| `#state-badge` 的 `z-index: var(--z-badge)`(`:678`) | 惰性但对 `check-05` item4 有活断言;删掉即打破既有门 |
| `#session-panel { flex: 1 1 auto; min-height: 200px }` 与 `:has(:empty)` 两条空态规则 | D-12;`min-height: 200px` **不是死代码** —— 空态下它是居中问候语唯一的空间来源 |
| `.event-list` 的 `transition: background-color 0.3s` 与 `.streaming` / `.aborted` 两条 | INTERACT-02 归 Phase 7;`.aborted` 是已交付的 SSE 修复(REG-03 复验对象) |
| `.collapse-indicator`(`:522`) | backlog `999.1` 第 1 项;硬规则 5 / 05-CONTEXT D-23 |
| `#latest-check` 的 `max-height: 30vh` + `overflow-y: auto` | D-11:去掉它会把裁决按钮推到折叠线以下 |
| `#stream-banner` 的任何声明(含 `position: fixed` / `top: 12px` / `left: 50%`) | L-1 的门断言几何不相交,不得靠移动横幅来通过 |
| `#doc-panel.collapsed` 的三条规则(含 `#state-badge { display: none }`) | D-04:登记为有意设计 |
| `#doc-panel-body { padding: 32px 40px }` | 除非 L-2 的守卫实测证成(那属于 §Deliberate Delta Ledger D6-9) |
| `.annotation-answer summary` 的 `font-size` / `color` / `cursor` / `margin-top` | L-6 只加两行尺寸声明,不动既有四条 |

---

## 不在本阶段(范围锁 —— Pitfall 8)

| 项 | 理由 | 状态 |
|---|---|---|
| 焦点样式本身(`:focus` / `:focus-visible` / `outline`) | A11Y-01,Phase 7。本阶段只为它解裁切 | 不在本阶段 |
| `:hover` / `:active` / `:disabled` / transition | INTERACT-01 / INTERACT-02,Phase 7 | 不在本阶段 |
| `tabindex` / ARIA / 键盘语义 / 划词焦点交接 | Phase 8;本阶段不触碰 `app.js` / `index.html` | 不在本阶段 |
| 响应式 / 移动端断点系统、`#app { flex-direction: column }`、任何堆叠布局 | UI-SPEC Q5 明文 Out of scope:它们改变 DESIGN.md §4.1 两栏契约的**含义**,是新设计决策而非 CSS 重构 | 不在本阶段 |
| `.collapse-indicator` 的 `font-size: 20px` / `line-height: 1` 越轨字面量 | backlog `999.1` 第 1 项(与 `check-05-ui-uat.py:588` 的陈旧文案合并为同一批处理) | 留证不修 |
| 折叠态的状态读数(48px 竖条内的紧凑 badge) | D-04 保持隐藏并登记为有意设计;若日后恢复属独立候选 | 不在本阶段 |
| `#latest-check` 的长报告折叠机制 | D-11 明确不引入;若裁决按钮可达性成为实际问题,属独立候选 | 不在本阶段 |
| UI Considerations 的 13 条 `overflow` 延后项(E2–E14) | 04.1 的 probe 已**取代**而非继承这些处置;本阶段只按 L-2 / L-3 / L-4 处理实际换行与溢出 | 不在本阶段 |
| `#probe-controls` 的移除或重定位 | 产品行为变更,v1.14 全局已裁定不进任何阶段 | 不在本阶段 |
| 暗色模式 / `prefers-color-scheme` | v2 `TOKEN-V2-01` | 不在本阶段 |
| `#selection-menu` 的定位数学 | Pitfall 8:它在旗舰交互路径上且工作正常,**不得「顺手改进」** | 不在本阶段 |
| `#main-pane` / `#doc-panel` 的 padding 抬升 | 若 L-5 普查判定需要,须登记为视觉变更并单独裁定(§Sign-Off S-2) | 条件项 |

---

## UI Considerations

> 本节由 ui-phase 的 **UI-consideration probe(Step 9.5)** 在 checker 通过之后生成,由
> plan-phase 的 `## UI Considerations` lift 规则提升。**整节替换,不追加**(幂等)。
> 空态 / 错误态 / 加载态的**文案**不在本节重复 —— 见 `## Copywriting Contract` 的冻结表(去重)。

**probe 运行记录(2026-09-22,checker APPROVED 之后):**

| 项 | 值 |
|---|---|
| 引擎 | `.claude/gsd-core/bin/lib/ui-consideration-probe.cjs` |
| 元素 | 10(E1–E10,见下表) |
| 覆盖 | applicable 43 / resolved 43 / unresolved 0 |
| 验证档 | explicit 24 / backstop 19 |
| 首跑(裸中文散文,无 override) | applicable 22;10 个元素中 **8 个 unclassified**;本阶段主题 `overflow` / `long-text` 中,`long-text` **全部漏检(0 条)** |
| 重跑(作者逐条裁定 kind 覆盖) | applicable 43;unclassified 0;`long-text` 10 条 |
| 差异 | 首跑漏掉 21 条,全部由作者裁定补回 |

> **首跑的数字不是覆盖率,是分类失真。** 引擎的 cue 是**英文匹配**:中文散文会被大量判为
> `unclassified`,而 `overflow` / `long-text` 这类本阶段的核心类别只在选择器里恰好含英文 `list`
> 时才被 `list-collection` 顺带命中。两行必须一起读 —— 只引「applicable 43」会把**作者裁定的成分**
> 误读成**引擎的认同**(沿用 Phase 5 的记录)。首跑 → 重跑的差异已逐条登记,可复核。

**元素面(10 个)与作者裁定的 kind:**

| id | 界面面 | 作者裁定的 kind |
|---|---|---|
| E1 | `#doc-panel-header`(sticky 表头) | `nav, static-content` |
| E2 | `#state-badge` | `static-content` |
| E3 | `#stream-banner` | `nav` |
| E4 | `#ai-events` / `.event-list` | `list-collection, static-content` |
| E5 | `#annotation-list` | `list-collection, static-content` |
| E6 | `#chat-messages` | `list-collection, static-content` |
| E7 | `#latest-check` | `static-content` |
| E8 | `.annotation-answer summary` | `interactive-control` |
| E9 | `#doc-panel-body` | `static-content` |
| E10 | `#main-pane` | `static-content` |

### explicit(24)—— 可直接提升为验收判据

| id | 界面面 | 类别 | 判据(truth) |
|---|---|---|---|
| E1 | `#doc-panel-header`(sticky 表头) | `overflow` | `#doc-panel` 是滚动容器、`#doc-panel-header` 是其直接 flex 子项,故 `position: sticky; top: 0` 生效:滚动面板正文时表头钉在面板顶部,正文首行不被遮住。门:`check-05 --item 8`(D-06/D-14 扩写的 sticky 断言)。 |
| E1 | `#doc-panel-header`(sticky 表头) | `long-text` | sticky 条在 `--doc-panel-w` 最小宽 340px 下仍单行:最宽文案是 `#state-badge` 的 9 字 + `文档区` h1,不折断、不换行。门:768/1024/1280 三处实检(L-1 的门)。 |
| E2 | `#state-badge` | `overflow` | `#state-badge` 是流内元素(无 `position`、无 `right`,HEAD `style.css:671-679`),结构上不可能遮挡正文;本阶段**不得**把它改回 fixed。徽标随 sticky 条钉住,滚动时恒可见。 |
| E2 | `#state-badge` | `long-text` | 最宽 badge 文案(阶段 1-12 / 自检档,9 字)在 340px 面板最小宽下不溢出、不换行,不把 `#doc-panel-header` 撑破。该文案是 L-1 碰撞实检的输入。 |
| E3 | `#stream-banner` | `loading` | 重连中态由 `#stream-banner` 的非 `.fatal` 形态承载,对比度 4.78:1 保持 AA;本阶段零改动。 |
| E3 | `#stream-banner` | `error` | 致命态由 `.fatal` 修饰符承载,`.fatal` 必须保留为**独立选择器**,对比度 4.76:1 保持 AA;门:`check-02-contrast.py` 两态实测。 |
| E3 | `#stream-banner` | `overflow` | `#stream-banner` 与 `#state-badge` 的相交条件是视口 < 490px,低于本阶段 768px 下限 ⇒ 残余碰撞不存在;门:768 / 1024 / 1280 三处实检横幅不盖 badge(L-1 的门)。 |
| E3 | `#stream-banner` | `long-text` | 横幅文案「事件流已断开,正在自动重连……」在 768px 下不折断、不换行溢出,且不因换行而增高到遮挡 badge。 |
| E4 | `#ai-events` / `.event-list` | `overflow` | 删掉 `.event-list` 的 `max-height: 55vh` 与 `overflow-y: auto` 后不再内部滚动,条目随外层容器滚动,滚到侧栏底部时内容可达(L-4:侧栏只剩两个滚动者)。门:`check-05 --item 9`。 |
| E4 | `#ai-events` / `.event-list` | `zero-one-many` | 0 / 1 / 多条目下高度随内容自然增长,无固定高度截断、无空白占位塌陷(本阶段删除了固定高度)。 |
| E4 | `#ai-events` / `.event-list` | `long-text` | `.event-content` 在 L-3 的六目标 `overflow-wrap: anywhere` 之列,不可断长串换行而不撑破视口。 |
| E5 | `#annotation-list` | `overflow` | 删掉 `#annotation-list` 的 `max-height: 32vh` 与 `overflow-y: auto` 后不再内部滚动,条目随外层容器滚动,滚到侧栏底部时内容可达(L-4)。门:`check-05 --item 9`。 |
| E5 | `#annotation-list` | `zero-one-many` | 0 / 1 / 多条目下高度随内容自然增长;展开某条 `<details>` 后不把后续条目挤出不可达区域(不再内部滚动即达成)。 |
| E5 | `#annotation-list` | `long-text` | `.annotation-note` 与 `.annotation-answer-body` 在 L-3 的六目标 `overflow-wrap: anywhere` 之列,引用摘录与批注正文的长串换行不撑破视口。 |
| E6 | `#chat-messages` | `overflow` | `#chat-messages` **保留**为侧栏内唯一合理的第二滚动者(输入行必须钉底),本阶段不动其 `overflow`;门:`check-05 --item 9` 断言侧栏恰好两个滚动者。 |
| E6 | `#chat-messages` | `zero-one-many` | 0 / 1 / 多条消息下 `#chat-messages` 的滚动行为一致;流式追加时新内容进入既有滚动区,不改变输入行的钉底位置。 |
| E6 | `#chat-messages` | `long-text` | `.chat-bubble` 与 `.say-chunk` 在 L-3 的六目标 `overflow-wrap: anywhere` 之列,长 markdown 与不可断长串换行不撑破视口。 |
| E7 | `#latest-check` | `overflow` | `#latest-check` **保留** 30vh 内部滚动(自检报告是本阶段唯一除 `#chat-messages` 外被显式允许保留的内部滚动者);L-4 只收敛 `.event-list` 与 `#annotation-list`。 |
| E7 | `#latest-check` | `long-text` | 报告 markdown 的不可断长串(路径、长 token)在 30vh 滚动区内换行,不产生横向滚动条。 |
| E8 | `.annotation-answer summary` | `long-text` | `.annotation-answer summary` 加 `min-height: 24px; min-width: 24px;` 后命中区 ≥24×24,而标签文案(`AI 回应` / `大白话回答`)不折断、不溢出该命中区。 |
| E9 | `#doc-panel-body` | `overflow` | `#doc-panel { min-width: 0 }` 生效,flex 项默认 `min-width: auto` 不再让面板被不可断长内容撑破视口;门:1440 → 1024 → 768 无横向溢出。 |
| E9 | `#doc-panel-body` | `long-text` | `.markdown-body` 在 L-3 的六目标 `overflow-wrap: anywhere` 之列,草稿 / 轮次文档 / 归档视图三态共用同一换行契约,长串换行不产生横向滚动。 |
| E10 | `#main-pane` | `overflow` | `#main-pane { min-width: 0 }` 生效,四个居中 section 的列不再被长内容撑破;门:1440 → 1024 → 768 三档无横向溢出(L-2 的判据:文档级 `scrollWidth`,面板内部横向滚动条不计)。 |
| E10 | `#main-pane` | `long-text` | 主区内不可断长内容(代码块、长路径)换行或在其自身容器内滚动,不把 `#main-pane` 的 `scrollWidth` 推过视口宽。 |

### backstop(19)—— 本阶段未改动该状态维度

每行是一个扁平标量 `{ statement, verification: backstop }`。**本阶段对空态 / 加载 / 错误 /
正常 / 局部这五类状态零改动** —— 文案与显隐机制一字不动,已由上游契约签核(见
`## Copywriting Contract`)。verify 时若无 wired 证据,这些行按 `insufficient_spec → human_needed`
上报,**不是静默通过**(#1154)。

| id | 界面面 | 类别 | statement | verification |
|---|---|---|---|---|
| E1 | `#doc-panel-header`(sticky 表头) | `loading` | What is shown while data or content is still loading (skeleton, spinner, progressive reveal)? | `backstop` |
| E1 | `#doc-panel-header`(sticky 表头) | `error` | What is shown when the load or submit fails (message, retry affordance, partial fallback)? | `backstop` |
| E4 | `#ai-events` / `.event-list` | `empty` | What is shown when there is no data — zero items, an unfilled form, or absent media? | `backstop` |
| E4 | `#ai-events` / `.event-list` | `loading` | What is shown while data or content is still loading (skeleton, spinner, progressive reveal)? | `backstop` |
| E4 | `#ai-events` / `.event-list` | `error` | What is shown when the load or submit fails (message, retry affordance, partial fallback)? | `backstop` |
| E4 | `#ai-events` / `.event-list` | `populated` | What does the normal populated (happy-path) state look like at a typical volume of content? | `backstop` |
| E4 | `#ai-events` / `.event-list` | `partial` | What is shown for partial or incomplete data — some fields or rows present, others missing? | `backstop` |
| E5 | `#annotation-list` | `empty` | What is shown when there is no data — zero items, an unfilled form, or absent media? | `backstop` |
| E5 | `#annotation-list` | `loading` | What is shown while data or content is still loading (skeleton, spinner, progressive reveal)? | `backstop` |
| E5 | `#annotation-list` | `error` | What is shown when the load or submit fails (message, retry affordance, partial fallback)? | `backstop` |
| E5 | `#annotation-list` | `populated` | What does the normal populated (happy-path) state look like at a typical volume of content? | `backstop` |
| E5 | `#annotation-list` | `partial` | What is shown for partial or incomplete data — some fields or rows present, others missing? | `backstop` |
| E6 | `#chat-messages` | `empty` | What is shown when there is no data — zero items, an unfilled form, or absent media? | `backstop` |
| E6 | `#chat-messages` | `loading` | What is shown while data or content is still loading (skeleton, spinner, progressive reveal)? | `backstop` |
| E6 | `#chat-messages` | `error` | What is shown when the load or submit fails (message, retry affordance, partial fallback)? | `backstop` |
| E6 | `#chat-messages` | `populated` | What does the normal populated (happy-path) state look like at a typical volume of content? | `backstop` |
| E6 | `#chat-messages` | `partial` | What is shown for partial or incomplete data — some fields or rows present, others missing? | `backstop` |
| E8 | `.annotation-answer summary` | `loading` | What is shown while data or content is still loading (skeleton, spinner, progressive reveal)? | `backstop` |
| E8 | `.annotation-answer summary` | `error` | What is shown when the load or submit fails (message, retry affordance, partial fallback)? | `backstop` |

---

## Registry Safety

Not applicable —— 无 shadcn、无 registry、无第三方 block。项目没有设计系统包,也没有构建步骤(D-06)。
`frontend/vendor/` 含**恰好一个文件**(`marked.min.js`),本阶段每个计划之后都必须仍是恰好一个文件。

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| none | none | not applicable — 无 registry 可及,也未被使用 |

---

## Checker Sign-Off

- [x] Dimension 1 Copywriting: FLAG(非阻塞)
- [x] Dimension 2 Visuals: PASS
- [x] Dimension 3 Color: PASS
- [x] Dimension 4 Typography: PASS
- [x] Dimension 5 Spacing: FLAG(非阻塞)
- [x] Dimension 6 Registry Safety: PASS
- [x] Dimension 7 Inventory Provenance: PASS

**Approval:** approved(7/7 通过,0 个 BLOCK,2 个非阻塞 FLAG)—— 2026-09-22

**两条非阻塞 FLAG(不阻塞规划,均为文档层、且都在本阶段的编辑面之外):**

1. **D1 · 冻结文案表记录了一条与权威设计文档矛盾的字符串。** 表中 `空态(批注流)` 行冻结
   `本轮暂无批注——在左侧文档划词即可批注。`(实为 `frontend/app.js:1121`),但 `DESIGN.md`(v1.14)
   §4.1 把文档面板放在**右侧**,v1.14 changelog 明写「会话流移入主区、文档区改为可折叠的右侧面板」。
   该串相对权威文档是**过期**的。次要点:表的来源行称文案「逐字来自 index.html」,而该串在 `app.js`。
   **处置:记为本阶段的已知过期串,交给拥有 `app.js` 的阶段(Phase 8)修 —— 本阶段零文案改动,
   硬规则 5 禁止动 `app.js`,不得为此扩张范围。**
2. **D5 · 签核 ID 命名空间碰撞。** `## Spacing Scale` 写 `04-UI-SPEC.md 的 12 档刻度(S-1)`,
   而本文件的 `## Sign-Off Items` 定义了**另一个** `S-1`(sticky 表头 `border-radius`);`06-CONTEXT.md`
   记录的锁定命名空间是 `S-1(间距 12 档)/ S-2(14px 为一级字号档)/ S-3(#ccc→#8a8a8a)/ S-4`。
   规划者读到裸 `S-2` / `S-3` 时可能解析到 04/04.1 的锁定签核。
   **处置(建议,未在本轮应用 —— FLAG 不阻塞规划):本文件的 `## Sign-Off Items` 三项宜写全
   `06-S-1` / `06-S-2` / `06-S-3`,与 04/04.1 的 `S-1…S-6` 区分。规划者读到本文件的裸 `S-2` / `S-3`
   时,按本节即可解析到**本阶段**的签核项,不是 04/04.1 的锁定签核。**

---

## Provenance

**本文件的输入(全部读自磁盘,无外部来源):**

| 来源 | 用途 |
|---|---|
| `.planning/phases/idi-06-layout-robustness/06-CONTEXT.md` | D-01…D-20 全部决策;本文件的 §布局契约 是它们的规格化形态 |
| `.planning/phases/idi-06-layout-robustness/06-DISCUSSION-LOG.md` | 四个讨论区的备选项与被否方案(用于写清「为什么不选 X」) |
| `.planning/ROADMAP.md` §Phase 6 / §Phase 7 / §全局硬规则 | 意图、承诺边界、硬规则;交付物清单经 D-02 逐条核对后登记 |
| `.planning/REQUIREMENTS.md` §LAYOUT / §A11Y-07 / §Out of Scope | 五条需求的原文与边界;两处失效前提登记于 A-7 |
| `.planning/STATE.md` §Operator Next Steps / §Blockers | S-1…S-4 签核原文(不得重开);D-19 的连带复验义务 |
| `frontend/style.css`(1265 行,磁盘 HEAD) | **唯一事实来源。** 每条断言的行号均取自该文件:L445 `.hidden` / L453-460 `#main-pane` / L468-475 `#doc-panel` / L477-490 `#doc-panel.collapsed` / L509-518 `.panel-header` / L551-559 `button` / L564-575 `.event-list` / L671-679 `#state-badge` / L682-696 `#stream-banner` / L783-811 `#session-panel` 族 / L913-920 `#annotation-list` / L991-996 `.annotation-answer summary` / L1114-1122 `#latest-check` / L1174-1176 `.verdict-buttons` / L1218-1227 活动面板标记 / L1263-1265 嵌入标题刻度 |
| `frontend/index.html` | DOM 结构:`#app` > `main#main-pane`(四个 section)+ `aside#doc-panel`;`#doc-panel-header` 的 badge 宿主;`#stream-banner` 位置 |
| `frontend/app.js`(`renderAnnotations:1150-1156` / `renderVerdictCard:676-717` / `appendSayToChat:260-285`) | L-5 与 L-6 的普查依据 |
| `scripts/check-05-ui-uat.py`(1672 行) | D-06 / D-14 的扩写对象;`MARKDOWN_TARGETS`(L889-904)是 L-3 的枚举范本;item4 的 SC5 断言(L983-986)是 A-6 的依据 |
| `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` | Q5 / Q6 / 例外清单 L-1…L-5 / 硬规则 / Do-Not-Touch / Copywriting |
| `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` | 25 tier-1 / 47 tier-2 / 47 对清单 / 60-30-10 预算(本阶段零改动) |
| `.planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-UI-SPEC.md` | 7 档字号 / 3 档字重 / 4 档行高;「按调用点枚举 + 普查守卫」方法论 |

**外部规范依赖:** 仅 **WCAG 2.5.8 Target Size Minimum(AA)**。其**间距例外**存在,但 A11Y-07 明文要求「达到 24×24」,
故按字面走尺寸而非例外(L-6)。无其他外部来源。

**环境事实(不得重新推导、不得对抗):** 截图不可用(headless 渲染被阻,且常驻 `/api/events` SSE 流让 capture handler 无法退出)
⇒ **计划用计算样式检查 + 命名人工步骤,不要计划视觉 diff**;若用 Playwright **必须**
`chromium.launch({ channel: 'chrome' })`(或按 `check-05-ui-uat.py` 头部的 `--browser` 策略);
**键盘文本选区无法自动化**,不得因自动测试 FAIL 判定功能缺陷。

*Phase: 6 — 布局稳健性 · UI-SPEC generated: 2026-09-22*
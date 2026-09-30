# Phase 11: 去卡片化与发丝分隔线 - Pattern Map

**Mapped:** 2026-09-28
**Files analyzed:** 4 (3 to modify, 1 verified as NOT needing modification)
**Analogs found:** 4 / 4

> **Scope note.** This phase is an **in-place reversal** of a shipped decision (v1.15 Phase 9's
> D-9-1 / D-9-2 / D-9-3), not new construction. Every analog below is therefore a **precedent for
> how this repo reverses a shipped decision**, and every line number was re-read against HEAD
> before quoting (nothing here is inferred from the CONTEXT/ROADMAP prose).

---

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `frontend/style.css` | config (single-tier design-token layer + rule bodies) | transform (declaration rewrite) | `frontend/style.css` @ `3bc9660` (Phase 9 `#doc-panel` rewrite) + `8bfe4f9` (Phase 10 table `border` rewrite) + `6349b2e` (Phase 10 token deletion) | exact (same file, same idiom) |
| `scripts/check-09-idi09-validation.py` | test (runtime gate, Playwright `getComputedStyle`) | request-response (browser probe) | `scripts/check-10-idi10-validation.py` `r1` (`:398-431`) + `t1` (`:337-389`) | exact (same repo, same gate family, same rewrite shape) |
| `scripts/check-02-contrast.py` | test (static token-contrast gate) | batch (fence scan → pair manifest) | itself at HEAD — only the **manifest inside `frontend/style.css`** changes, not the script | exact (script body byte-identical) |
| `scripts/check-05-ui-uat.py` | test (runtime UAT gate) | request-response | n/a — **no change needed**; see §"check-05 does NOT change" | verified by execution |

**Divergence from the brief's expected file set:** the brief listed `scripts/check-05-ui-uat.py` as
"possibly modified". It is **not** modified. Evidence in §"check-05 does NOT change".

---

## Repo conventions that constrain every excerpt below

These are not style preferences — each one has already cost this repo a red gate.

1. **追加,不重排 (append, never reorder).** At least four pairs of equal-specificity rules are
   decided by source order. Reordering is a rendering change that looks innocent in a diff.
   Documented in-file at `frontend/style.css:1216-1217` (`.chat-user` vs `.chat-bubble`, both
   0-1-0, "靠源码顺序取胜——不得移到 .chat-bubble 之前"), `:1376-1377` (`.annotation-answered`
   descendant rules, 0-2-0 vs 0-2-0), `:1597` ("追加在文件末尾 …… 靠源码顺序压过
   `.annotation-plain .annotation-note`(0-2-0)"), `:1805`.
   → **Rewrite an existing declaration in place; never move a rule.**
2. **零新增 tier-1 原语、零新增颜色值、零新增 `!important`、无 `@layer` / `@property` /
   `var(--x, #fallback)`.** `check-01-token-conformance.sh:42-48` mechanically enforces the first
   two **outside** the fence (it drops the fenced region with an awk state machine, then counts
   `#hex` occurrences and `var(--(white|black|gray|green|blue|amber|red|purple|radix)(-[0-9]+)?`
   references). `check-04-important-count.sh` counts `!important;` **declarations** (≡ 1) — prose
   in comments inflates a naive `grep -c`, which this repo has already tripped on three times.
3. **`* { box-sizing: border-box; }` is global** (`style.css:3`), so adding a `border-*` to a
   container changes its **border-box** height. Every 1px geometry claim in this phase must come
   from a runtime reading, never from arithmetic on paper.
4. **Every `style.css` plan needs ≥1 RUNTIME verification** (real-browser computed style).
   `grep -c 'var(--'` proves nothing about rendering — this is the milestone's stated Avoids entry.
5. **删除令牌必配专用残留断言** (Phase 10's `--radius-lg` precedent), and **never** a *generic*
   fence-consumption assertion — that is G2, explicitly out of scope for v1.16.
6. **Inside the fence, never write「令牌名 + 冒号」in a comment.** `check-02-contrast.py`'s
   `DECL_RE = re.compile(r"(--[a-z0-9-]+)\s*:\s*([^;]+);")` (`:27`) scans the **whole fence text,
   comments included**, and `parse_decls` (`:72-74`) lets the **last** match win. A comment reading
   `` `--color-border-subtle`: gray-6 已四处消费; `` is parsed as a declaration and
   `resolve()` exits 1 with `unparsable value`.

---

## Pattern Assignments

### `frontend/style.css` (config, in-place declaration rewrite)

**Analog A (in-place rewrite of a container's boundary — the exact template):**
`git show 3bc9660 -- frontend/style.css` (Phase 9, `#doc-panel`). The hunk:

```diff
-  border-left: 1px solid var(--color-border-subtle);
-  background: var(--color-surface);
+  border: 1px solid var(--color-border-subtle);
+  background: var(--color-surface-card);
+  border-radius: var(--radius-md);
+  box-shadow: var(--shadow-card);
```

with the commit message stating the rule verbatim:
> `#doc-panel 就地改写:border-left → border(四边同族)、background 改指 --color-surface-card`

and the surviving comment (`style.css:760-767`) recording *why*:

```css
/* 右:文档面板(基准宽由 --doc-panel-w 控制;收起态为 48px 竖条)

   Phase 9:与左栏**同族卡片** —— 同底色令牌 / 同边界令牌 / 同圆角令牌 / 同阴影令牌
   (CARD-02)。原 `border-left: 1px` 的单边凹陷读感由四边边界 + 卡片底色取代,故这里
   是就地改写那条声明,不是追加一条 `border` 覆盖它(留下一条已死的 border-left 会让
   注释与代码互相矛盾)。
   `overflow-y: auto` 是**承重的滚动契约**,不得删除:它是右列的滚动者,L-1 的 sticky
   表头依赖 #doc-panel 仍是最近的可滚祖先。 */
```

**Phase 11 reverses exactly this hunk** (the value `--color-border-subtle` on `border-left` is
restored byte-for-byte; the ground moves to the unified surface). **Do not append an override
rule** — rewrite `:773-776` in place.

**Analog B (in-place rewrite of a boundary + append of the rule that consumes the freed token):**
`git show 8bfe4f9 -- frontend/style.css` (Phase 10, tables). Its own comment records the idiom:

```css
   (b) 就地改写:原「四条边取 --color-border」那条声明是就地改写成「四边零宽度 + 一条下边线」,
   不是追加一条覆盖规则 —— 留下一条已死的声明会让注释与代码互相矛盾(与 Phase 9 对
   #doc-panel 的左边框同一纪律)。
```

The shape to copy: **rewrite the existing declaration to the "no boundary" state, then place the
new hairline rule immediately after it** (Phase 10 put `.markdown-body th { background: … }`
directly below the rewritten `th, td` rule at `style.css:1112-1118`).

**Analog C (token deletion + comment rewrite that never names the deleted token):**
`git show 6349b2e -- frontend/style.css` (Phase 10, `--radius-lg`):

```diff
-  /* Radius — four values. */
+  /* Radius — three values. The former fourth step (28px) was hand-tuned in by the
+     temporary visual pass of quick `260918-qrq` and never joined any scale
+     declaration: …
+     Deleted rather than kept: Hard Rule 5 — never declare a token you are not consuming. */
   --radius-sm: 8px;
   --radius-md: 10px;
-  --radius-lg: 28px;
   --radius-pill: 999px;
```

Note the deleted token's **name appears nowhere** in the replacement comment — that is forced by
the residue assertion in Analog D, which is a **substring count over the whole fence text**.

#### The five container rules to rewrite, verbatim

**1. `#main-pane` (`:717-734`)** — rewrite `gap: var(--space-3)` (`:725`) to `0`; `align-items:
center` (`:727`) and `overflow-y: auto` (`:726`) stay **byte-identical** (D-11-5). The comment
block `:721-724` is load-bearing rationale that dies with the gap:

```css
  /* Phase 9 / D-9-2:卡片间距取紧凑档 12px(HEAD 是 6px)。间隙里透出的是页面底色
     (gray-3),这正是「白卡片浮在灰页面之上」的可见形态 —— 间距不只是留白,它是
     卡片层次的载体。卡片本身不得加 margin:那会移动既有几何并可能打在 24x24 命中区
     门上,而页面级留白是未裁定项(见 STATE 的开放清单)。 */
  gap: var(--space-3);
```

**2. `#main-pane > section` (`:751-758`)** with its comment `:736-750`:

```css
/* 左栏四个面板的卡片语言(Phase 9 / CARD-01 / CARD-02)。就地扩写既有规则体,
   选择器文本与源码顺序逐字不变 —— 硬规则 3「追加,不重排」的落地形态。

   ① 边界色取 --color-border(gray-7),比 --color-border-subtle(gray-6)深一档 ——
      依据是用户 2026-09-26 的裁定「边框与阴影强度:现在太轻了,稍微重一点」,即
      Phase 9 自己 parked 的强度决策的落地。取的是既有令牌 ⇒ 仍是零新增令牌;
      --color-border-subtle 仍是 .event-list / .annotation-item / .badge-answered /
      #latest-check 四处的边界色 —— 那四处不是卡片,本次不动。
   ② 本规则体内**禁止**出现 transform / filter / will-change / contain / perspective /
      opacity / position / z-index / overflow 任何一项。#stream-banner 是 #doc-panel 的
      后代且 position: fixed,前六个属性会建立「fixed 定位包含块」或新层叠上下文,把它
      钉到卡片上而不是视口;overflow: hidden 会裁剪 :focus-visible 的 2px 焦点环 ——
      左栏卡片**不需要**它,因为 .panel-header 自身的 border-radius 已是 --radius-md,
      不会把卡片四角顶成方角。
   ③ 阴影取 --shadow-card,零位移,不参与布局。 */
#main-pane > section {
  width: 100%;
  max-width: 768px;
  background: var(--color-surface-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
}
```

Rewrite: `background` → `var(--color-surface-page)`, `border` → `none`, `border-radius` → `0`,
`box-shadow` → `none`. `width` / `max-width` **stay byte-identical** (D-11-5 — the 768px centred
column is *kept*; only its side gutters become invisible). Clause ②'s premise ("`.panel-header`
自身的 border-radius 已是 --radius-md") **dies** when D-11-7 zeroes it at `:843`; clause ① and ③
die with the boundary tokens. The comment must be **rewritten, not deleted** — and clause ② must
not be left asserting a false premise. Add the hairline immediately after this rule:

```css
#main-pane > section + section { border-top: 1px solid var(--color-border-subtle); }
```

**3. `#doc-panel` (`:768-783`)** — see Analog A's comment above. Rewrite `:773-776`:
`border: 1px solid var(--color-border)` → `border-left: 1px solid var(--color-border-subtle)`;
`background: var(--color-surface-card)` → `var(--color-surface-page)`; drop `border-radius` and
`box-shadow`. `overflow-y: auto` (`:772`) and `min-width: 0` (`:782`) **stay byte-identical**.
`#doc-panel.collapsed { overflow: hidden }` (`:785-788`) is untouched (the 48px bar keeps its
left hairline).

**4. `#doc-panel-header` (`:813-818`)** with comment `:800-812`:

```css
#doc-panel-header {
  position: sticky;
  top: 0;
  background: var(--color-surface-card);
  border-radius: 0;
}
```

Change **only** `:816`'s token to `var(--color-surface-page)`. `position: sticky` / `top: 0` /
`border-radius: 0` are load-bearing and **一字不动** (D-11-7). The comment's sentence
「表头底色与卡片底色同值(都取卡片令牌)」 becomes false and must be rewritten.

**5. `.panel-header` (`:837-846`)** — zero `:843`'s radius in place:

```css
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 36px;
  padding: var(--space-1-5) var(--space-2-5);
  border-radius: var(--radius-md);
  cursor: pointer;
  user-select: none;
}
```

`border-radius: var(--radius-md)` → `0` (D-11-7). `#doc-panel-header`'s own `border-radius: 0`
(`:817`) already wins by ID specificity, so it is unaffected — which is exactly why it is recorded
as "一字不动".

#### The activity marker that must survive (`.panel-header` inset bar, `:1630-1634`)

```css
#session-panel:not(.hidden) .panel-header,
#annotations-panel:not(.hidden) .panel-header,
#checks-panel:not(.hidden) .panel-header {
  box-shadow: inset 3px 0 0 var(--color-marker-active);
}
```

This is the **only surviving activity affordance** after de-carding. Two consequences the planner
must encode:
- **`.panel-header` is NOT one of the 5 containers.** c1's `box-shadow === "none"` assertion must
  be scoped to the four `section` elements (and `#doc-panel`), **never** to `.panel-header` or to
  "all descendants".
- The rationale comment above it (`:1611-1629`) explains it uses `box-shadow` instead of
  `border-left` precisely so it costs **zero layout** (`:1615-1617`) — this is the precedent to
  cite for the hairline being box-internal (D-11-9's "零位移、零新增 DOM").

#### The unified-surface declaration (`--color-surface-page`, `:139`)

The value change is one line, but its comment (`:122-138`) is a Phase-9 ledger that names the
deleted token at `:126`:

```css
  /* Phase 9 sinks the page one step (CARD-03 / user decision D-9-1): gray-1 #fcfcfc ->
     gray-3 #f0f0f0. Reason: gray-1 was the LIGHTEST value on the whole screen, so the
     white cards Phase 9 plan 01 introduced had almost nothing to sit against. gray-3
     completes the three-tier elevation scale — page gray-3 < --color-surface gray-2
     (the inset control surface) < --color-surface-card white (raised) — which is
     shadcn's canvas / inset / raised ladder. …
     This token has exactly ONE consumer (`html, body`'s background), so changing the
     value here re-colours the whole page and nothing else needs synchronising. What it
     DOES invalidate is every contrast pair drawn on it: eight entries were on this
     ground. … */
  --color-surface-page: var(--radix-gray-3);
```

Verified against HEAD: `var(--color-surface-page)` has **exactly one consumer** (`style.css:701`,
`html, body { background: … }`), and `var(--radix-gray-3)` has **three** consumers (`:139`
page, `:140` sunken, `:209` hover) ⇒ changing the page value creates **no new orphan** (D-11-3
holds). `var(--radix-gray-1)` has **zero** consumers at HEAD (`:48` is a bare declaration) ⇒ the
G2 fact base is untouched.

#### The two tokens to delete (`:312-335`)

```css
  /* Tier 2 — the card container language (Phase 9 / VIS-01 / VIS-02 / CARD-01 /
     CARD-02). Five load-bearing facts, so that a later reader does not "fix"
     either token away.

     1. The SURFACE RELATIONSHIP is a three-step ladder the user adjudicated
        (D-9-1, PROJECT.md Key Decisions — do NOT reopen it): page
        (--radix-gray-3 after Phase 9 plan 02) < --color-surface (gray-2, the
        inset ground of controls) < white (the card). It is the shadcn
        canvas / inset / raised trio.
     …
     5. --color-surface-card is an alias of --white, which is already declared
        at the top of this fence => Phase 9 adds ZERO tier-1 primitives. */
  --color-surface-card: var(--white);
  --shadow-card: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04);
```

Verified consumers at HEAD: `var(--color-surface-card)` → `:754`, `:774`, `:816` (exactly the 3
claimed); `var(--shadow-card)` → `:757`, `:776` (exactly the 2 claimed); `var(--white)` → 5 other
consumers (`:150`, `:151`, `:159`, `:162`, `:338`) ⇒ deleting the card token does **not** orphan
`--white`. `var(--color-border)` → `:755`, `:773`, `:1084`; after the rewrite only `:1084`
(`.markdown-body blockquote { border-left: 3px solid … }`) survives — matching D-11-8's note about
its semantic drift.

**The fence-wide residue list (this is the forcing function).** `fenced.count("--color-surface-card")`
is a **substring count over the whole fence text, comments included**. At HEAD the token occurs
**8 times** inside the fence (`:126`, `:189`, `:332`, `:334`, `:515`, `:542`, `:632`, `:643`); all
eight must reach zero. `--shadow-card` occurs **once** (`:335`). Two of the eight are **PAIR
entries**, so they must be re-attributed (not merely reworded) or `check-02`'s `resolve()` exits 1
with `FAIL: unknown token`.

#### The Phase-9 manifest ledger inside the fence (`:474-693`)

The whole PAIR manifest lives **inside** `:root` (`:6`-`:694`). Relevant lines, re-read at HEAD:

```css
  /* PAIR --color-text ON --color-surface-page TEXT */                        /* :561 */
  /* PAIR --color-text-secondary ON --color-surface-page TEXT */              /* :571 */
  /* PAIR --color-text-muted ON --color-surface-page TEXT */                  /* :576 */
  /* PAIR --color-focus ON --color-surface-page NON-TEXT */                   /* :620 */
  /* PAIR --color-marker-active ON --color-surface-card TEXT */               /* :632 */
  /* PAIR --color-border-strong ON --color-surface-card NON-TEXT */           /* :643 */
  /* PAIR --color-border-hover ON --color-surface-page NON-TEXT */            /* :659 */
  /* PAIR --color-marker-active ON --color-surface-page NON-TEXT */           /* :689 */
```

The exact syntax is `/* PAIR <fg-token> ON <bg-token> TEXT|NON-TEXT[@alpha] */`, matched by
`check-02-contrast.py:28-31`; the single ordering entry is
`/* ORDER --color-text-muted BEFORE --color-text ON --color-surface */` (`:693`), matched by
`:32-35`. Only `:632` and `:643` change (ground → `--color-surface-page`); the other six
page-ground entries keep their **name** and only their **number** is recomputed.

**Thresholds are not touched:** `TEXT_MIN = 4.5` / `NON_TEXT_MIN = 3.0` (`check-02-contrast.py:24-25`)
stay byte-identical, as does the coverage floor (`:150`, `>=24 pairs / >=20 TEXT / >=4 NON-TEXT`)
and the raw-marker-count guard (`:161-175`). Re-attribution changes **ground labels only**, so the
pair count stays **53 (35 TEXT + 18 NON-TEXT) + 1 ordering entry**.

**Recomputed numbers (computed here with `check-02`'s own `resolve` / `contrast_ratio` /
`composite`, page simulated as `var(--white)`):**

| pair | ground | HEAD | after | need | verdict |
|---|---|---|---|---|---|
| `--color-text` TEXT | page | 14.30 (gray-3) | **16.293** | 4.5 | PASS |
| `--color-text-secondary` TEXT | page | 5.19 | **5.918** | 4.5 | PASS |
| `--color-text-muted` TEXT | page | 5.19 | **5.918** | 4.5 | PASS |
| `--color-focus` NON-TEXT | page | 5.15 | **5.869** | 3.0 | PASS |
| `--color-border-hover` NON-TEXT | page | 5.19 | **5.918** | 3.0 | PASS |
| `--color-marker-active` NON-TEXT | page | 4.18 | **4.766** | 3.0 | PASS |
| `--color-marker-active` TEXT | card → page | 4.77 | **4.766** | 4.5 | PASS |
| `--color-border-strong` NON-TEXT | card → page | 3.32 | **3.319** | 3.0 | PASS |

`--color-surface` (gray-2) luminance **0.947307** < unified surface **1.000000** ⇒ SURF-02's
"inset stays the only darker tier" holds. The `ORDER` entry's ground is `--color-surface`, not the
page ⇒ unaffected.

**⚠ Discovered pre-existing staleness (report, do not silently fold in).** `style.css:670-674`
reads:

```css
  /* the two solid-fill steps are boundaries in their own right (SC 1.4.11). Each fill
     sits on --color-surface: #approve-row / #writing-view / #authorize-row all live in
     #doc-panel-body → #doc-panel, and #doc-panel declares background: var(--color-surface). */
  /* PAIR --color-action-commit ON --color-surface NON-TEXT */
  /* PAIR --color-action-irreversible ON --color-surface NON-TEXT */
```

`#doc-panel` declares `background: var(--color-surface-card)` at HEAD (white) — **not**
`--color-surface` (gray-2). Phase 9 broke this sentence and Phase 11 breaks it again. The label is
the **conservative** one (gray-2 is darker than white, so the recorded ratio is the lower of the
two), which is why nothing went red. These two pairs are **not** among the 2 + 6 enumerated by
D-11-15 / SC5. Whether to re-attribute them is a **scope decision for the planner** — flag it, do
not expand scope unilaterally.

---

### `scripts/check-09-idi09-validation.py` (test, runtime gate rewrite)

**Analog D (the dedicated residue assertion — quote in full):**
`scripts/check-10-idi10-validation.py:402-409`

```python
    # (a) 源码文本级:围栏内零声明残留。读的是**文件文本**,不是渲染结果 ——
    #     与下面的运行时断言互补(文本级看不见「消费者是否真的接上了」,运行时看不见
    #     「围栏里是否还留着一行没人用的声明」)。
    fenced = fence_text()
    ok_true(item, "r1 [源码] 围栏内 --radius-lg 声明残留计数 == 0",
            fenced.count("--radius-lg") == 0, "== 0", str(fenced.count("--radius-lg")),
            note="读 DESIGN TOKENS 围栏内的文本;围栏内不得留下未消费的令牌声明"
                 "(D-04 / Hard Rule 5)")
```

with the helper it calls (`scripts/check-10-idi10-validation.py:184-189`):

```python
def fence_text():
    """返回两行 `===== DESIGN TOKENS: START/END` 之间的文本(含标记行自身)。"""
    text = STYLE_CSS.read_text(encoding="utf-8")
    start = text.index(FENCE_START)
    end = text.index(FENCE_END)
    return text[start:end]
```

(`STYLE_CSS` / `FENCE_START` / `FENCE_END` at `:94-97`.) **`check-09` has no `fence_text()` — it
must add one**, copied verbatim. Note the mechanism is a **substring count**, while the label says
「声明残留计数」: the replacement comment for the two deleted tokens must therefore **not name
them** (exactly as Phase 10's `--radius-lg` comment does not).

**Analog E (the "token deleted" hard-FAIL detector — the `ok()` None-degradation trap):**
`scripts/check-10-idi10-validation.py:417-431`

```python
    for name, literal in RADIUS_LITERALS.items():
        got = tokens[name]
        # ⚠ 走 ok_true 而**不是** ok():ok() 在 expected/actual 为 None 时记 BLOCKED,
        # 而「令牌被删」正是本项要抓的回归 —— 记 BLOCKED 会把它降级成 exit 2(本项目
        # 把 2 当作「按设计」的良性码)。令牌未声明必须是硬 FAIL,否则删掉 --radius-md
        # 这条回归在本门里无人拦(实测:check-01/03/04 对此也全 PASS)。
        ok_true(item, f"r1 [令牌] {name} 解析值 == 刻度声明字面量",
                got is not None and norm(got) == norm(literal),
                literal, "<未声明>" if got is None else got, …)
    gone = resolve_token(page, "--radius-lg")
    ok_true(item, "r1 [令牌] 被删档位已不可解析(解析值 None)",
            gone is None, "None", str(gone),
            note="被删档位的探测器:它若还能解析出值,说明删漏了或消费者没搬完")
```

This is the **exact** shape Phase 11 needs for `--color-surface-card` / `--shadow-card`. The
mechanism it defends against is confirmed in `check-05-ui-uat.py:215-222`: `ok()` emits `BLOCKED`
(not `FAIL`) when `expected is None`, and `check-09`'s `main()` maps BLOCKED to exit code **2**
(`:544-547`), which this project treats as a benign code.

**Analog F (dual token+literal assertion on a hairline colour):**
`scripts/check-10-idi10-validation.py:377-383`

```python
        ok(item, f"{pair} .markdown-body td 计算 border-bottom-color == var(--color-border-subtle)",
           tokens["subtle"], read_style(page, f"{pair} .markdown-body td", "border-bottom-color"),
           note="行间极浅分隔线(gray-6);border-collapse 把它与上一行折成一条,不出现双线")
        ok(item, f"{pair} .markdown-body td 计算 border-bottom-color == gray-6 字面量",
           TH_BORDER_LITERAL, read_style(page, f"{pair} .markdown-body td", "border-bottom-color"),
           note="与上一条互补:只跟令牌比是自指的,令牌被改成 gray-7 时两侧一起变、恒过;"
                "这一条把「行间线是浅档」钉死在 gray-6")
```

`TH_BORDER_LITERAL = "rgb(217, 217, 217)"` (`:106`). **Phase 11's hairline assertions must carry
this pair of complementary assertions** — otherwise swapping `--color-border-subtle` for
`--color-border` (gray-7) passes by self-reference. That swap is exactly the D-11-8 alternative the
phase rejected, so the gate must be able to see it.

**Analog G (the machinery the rewrite must keep).** `check-09`'s module-level wiring at `:62-81`:

```python
ROOT = Path(__file__).resolve().parent.parent
CHECK05 = ROOT / "scripts" / "check-05-ui-uat.py"

def load_check05():
    """把 check-05 当模块加载(文件名含连字符,不能用 import)。"""
    spec = importlib.util.spec_from_file_location("check05_ui_uat", CHECK05)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

c05 = load_check05()
ok = c05.ok
ok_true = c05.ok_true
blocked = c05.blocked
info = c05.info
read_style = c05.read_style
resolve_color = c05.resolve_color
resolve_token = c05.resolve_token
```

Dispatch and exit-code semantics to keep: `ITEMS = {"c1": c1, "c2": c2, "c3": c3, "c4": c4, "c5": c5}`
(`:477`), `main()` `:490-548`, and the `--screenshot DIR` path `:455-474` (Phase 12's VIS-01 reuses
it verbatim: *"复用既有 `--screenshot` 路径 … 不新建 harness"*).

Helper behaviours the rewrite depends on (all in `check-05-ui-uat.py`):
- `read_style(page, sel, prop)` (`:340-348`) = `document.querySelector(sel)` + `getComputedStyle(el)[prop]`,
  returns `None` when the element is absent. It works on `display: none` elements — that is the
  stated basis for reading all four sections from the single `p1` sample (`check-09:126-128`).
- `resolve_color(page, token)` (`:435-455`) returns **`None` for an undeclared token** (it probes
  `documentElement` first).
- `resolve_token(page, name)` (`:458-468`) returns `None` for an undeclared token.
- `norm(value)` (`:225-229`) flattens whitespace inside `rgb()`/`rgba()`.
- `c05.STATES = ["p1", "p12", "p3", "checking", "archive"]` (`:584`).

**HEAD baseline (measured by running the gate, not inferred).**
`.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4` → **exit=0**,
`c1 PASS 26 条断言`, `c2 PASS 13`, `c3 PASS 3`, `c4 PASS 4`. The readings the rewrite must invert:

- c1, each of the four sections: `background-color=rgb(255, 255, 255)`, `border-top-left-radius=10px`,
  `border-top=1px solid`, `box-shadow=rgba(0, 0, 0, 0.08) 0px 1px 3px 0px, rgba(0, 0, 0, 0.04) 0px 1px 2px 0px`.
- c2 `#doc-panel`: all four `border-*-width=1px`, all four `border-*-style=solid`, radius `10px`,
  `overflow-y=auto`; `#doc-panel-header box-shadow=none`.
- c3: `body=rgb(240, 240, 240)`; luminances page **0.871367** < inset **0.947307** < card **1.000000**.
- c4: `#main-pane gap=12px`; `.panel-body padding=16px`; `#doc-panel-body padding=32px 40px`;
  `.panel-header padding-top=6px`.

Assertion-count delta (context for "零条断言被删除"): the rewrite should land **≥** 46 assertions
across c1..c4. c1 grows (4 sections × more properties + the new control group), c3's third tier
disappears but is replaced by the "body == panel ground, same value" equality + the "inset still
darker" assertion.

**Assertion shapes the rewrite needs, with the concrete selectors verified present in `p1`:**

- c1 control group (D-11-12 / SC1: "该对照组须在同一份运行时读数里给出"). All of these are in
  `frontend/index.html` and readable via `getComputedStyle` even when their ancestor is `.hidden`:
  `button` (`:884-892`: `border: 1px solid var(--color-border-strong)`, `border-radius: var(--radius-sm)`),
  `#check-switcher` (`:1518-1525`: 1px border + `--radius-sm`),
  `#project-path-input` (`:876-882`: 1px border + `--radius-sm`),
  `.overlay-card` (`:987-994`: `border-radius: var(--radius-md)` + `box-shadow: var(--shadow-overlay)`).
  ⚠ Do **not** put `.panel-header` in the control group (it legitimately has radius 0 after D-11-7
  and a legitimate `inset` box-shadow when active).
- c1 border-width shape is **heterogeneous**, not a uniform loop: `#session-panel` is the DOM-first
  `section` so `section + section` never matches it ⇒ all four widths `0px`; the other three each
  have `border-top-width == "1px"` and the other three sides `0px`. `#annotations-panel` and
  `#checks-panel` carry `.hidden` in `p1` — `getComputedStyle` still resolves them, but this is
  precisely the kind of claim that must be confirmed by a real run, not asserted on paper.
- c4 vertical hairline "跨满面板可视高度": `#doc-panel` is stretched by `#app { display: flex;
  height: 100vh }` (default `align-items: stretch`); the item-8 reading confirms
  `panel={top: 0, bottom: 900}` at 1440×900. A geometry assertion (e.g. the element's rect height
  equals the viewport height, or `#doc-panel` rect `top == 0 ∧ bottom == 900`) is what makes "跨满"
  observable rather than merely "a 1px border exists".

---

### `scripts/check-02-contrast.py` (test, static gate — script body unchanged)

**No line of this script changes.** What changes is the manifest it reads (inside `frontend/style.css`).
Its invariants that the phase must not disturb:

- `TEXT_MIN = 4.5` / `NON_TEXT_MIN = 3.0` (`:24-25`) — byte-identical.
- `DECL_RE` (`:27`) scans the **fence text including comments**; `PAIR_RE` (`:28-31`) and
  `ORDER_RE` (`:32-35`) define the entry syntax.
- Coverage floor `:150`; raw-marker-count guards `:161-175` (`fence.count("/* PAIR")` must equal the
  parsed count — so a comment that *mentions* `/* PAIR` breaks the gate).
- `resolve()` (`:77-105`) `sys.exit(1)`s on an unknown token name — this is why the two re-attributed
  PAIR entries cannot be left naming `--color-surface-card`.
- `ORDER` handling `:207-226` — the single ordering entry's operands are both TEXT pairs on
  `--color-surface`, so it does not degenerate.

---

### `scripts/check-05-ui-uat.py` — **does NOT change** (verified by execution, not by reading)

The brief flagged this as "possibly modified"; the CONTEXT/ROADMAP warn against changing it. The
gate as written already tolerates the phase's geometry change, because the sticky assertion is a
**tolerance**, not an equality — `scripts/check-05-ui-uat.py:2282-2288`:

```python
            ok_true(
                item,
                "[p1] sticky 把 #doc-panel-header 钉在 #doc-panel 顶部(<=1px)",
                abs(hp["top"] - pp["top"]) <= 1.0,
                "|header.top - panel.top| <= 1px",
                f"{abs(hp['top'] - pp['top']):.3f}px",
            )
```

Measured at HEAD by running `.venv/bin/python scripts/check-05-ui-uat.py --item 8 --browser bundled`:

```
INFO item8 sticky 原始数值: scrollTop=4350 scrollHeight=5248 clientHeight=898
  header={'top': 1, 'bottom': 35, ...} panel={'top': 0, 'bottom': 900, ...}
PASS [p1] sticky 把 #doc-panel-header 钉在 #doc-panel 顶部(<=1px): … actual=1.000px
item 8: PASS  (13 条断言,0 FAIL,0 BLOCKED)   exit=0
```

So the "余量恰 `1.000px`" claim is confirmed, and its cause is the 1px **top** border on
`#doc-panel` (the padding-box top of a scroll container is `border-top-width` away from the border
box). Removing that border moves the reading to `0.000px` — **still `<= 1.0` ⇒ still PASS**.

Consequences for the plan:
- `check-05` needs a **re-run + reading registration** (REG-03), **not** a code change. Changing it
  would drag its **7** covering reports into re-verification (measured below), which is the exact
  cost Phase 10 avoided.
- ⚠ **The assertion is sitting exactly on its tolerance boundary today.** `1.000 <= 1.0` is true
  only by the stated float tolerance. Any implementation that leaves *any* top-side border/offset on
  `#doc-panel` (or that uses a `margin`/extra element for the vertical hairline) pushes the reading
  above 1.0 and turns item 8 red. `border-left` only — no `border-top` — keeps it at 0.000.
- D-11-16's triage rule applies if the reading's *fact* changes: the fact (sticky header occludes
  scrolled body) is unchanged, so only the margin reading and its cause are re-registered.

**Item 9 scroll-census discrepancy (report).** CONTEXT D-11-9 and ROADMAP's Avoids both say the
census "期望值是 4 不是 3". On disk it is neither: `scripts/check-05-ui-uat.py:2427` defines
`PANEL_SCROLLERS = ("#chat-messages", "#latest-check", "#main-pane")` — **3** members — and
`:2708-2718` asserts the set is **exactly** those 3, then **exactly 2** after excluding
`#chat-messages` (`PANEL_SCROLLERS_EXEMPT`, `:2429`). No `4` appears in item 9's scroll census.
The load-bearing point survives (deleting `#doc-panel`'s `overflow-y: auto` breaks the census), but
the planner must **not** write "expected 4" into a plan.

---

## Shared Patterns

### In-place rewrite, never an appended override
**Source:** `git show 3bc9660` (Phase 9 `#doc-panel`) and `git show 8bfe4f9` (Phase 10 tables).
**Apply to:** all five container rules + `#main-pane`'s `gap` + `.panel-header`'s radius in
`frontend/style.css`. The rule body's old declaration is replaced; the comment above it is rewritten
to match the new fact. The only *added* rule is the hairline, placed immediately after the rule it
completes (Phase 10's `.markdown-body th` placement precedent, `:1118`).

### Rewrite the rationale comment in the same commit
**Source:** `frontend/style.css:736-750` (① / ② / ③), `:760-767`, `:800-812`, `:122-138`,
`:312-335`, `:474-558`, `:623-631`, `:634-643`.
**Apply to:** every rule/token touched. These comments carry the *reason* the old state existed and
are the only thing standing between a future reader and a "helpful" revert. Two of them assert
premises that this phase **kills**: `:748-749` ("`.panel-header` 自身的 border-radius 已是
`--radius-md`") and `:802` ("表头底色与卡片底色同值(都取卡片令牌)"). Rewriting is mandatory;
deleting is forbidden.

### Dedicated residue assertion for each deleted token
**Source:** `scripts/check-10-idi10-validation.py:402-409` (`fenced.count("--radius-lg") == 0`) +
`:184-189` (`fence_text()`).
**Apply to:** `--color-surface-card` and `--shadow-card` — one assertion each, in `check-09` (the
phase's own gate, mirroring Phase 10 putting `r1` in `check-10`). **Never** a generic
fence-consumption assertion (that is G2).

### Hard-FAIL on token absence (`ok_true`, never `ok`)
**Source:** `scripts/check-10-idi10-validation.py:417-431`; mechanism confirmed in
`check-05-ui-uat.py:215-222` + `check-09:544-547` (BLOCKED → exit 2, a benign code here).
**Apply to:** every token-resolution assertion in the rewritten c1/c2/c3 — `resolve_color` /
`resolve_token` return `None` for a deleted token, and `ok()` would silently downgrade that to
BLOCKED with a DOM-pointing message.

### Dual token + literal assertion on any boundary colour
**Source:** `scripts/check-10-idi10-validation.py:377-383` + `TH_BORDER_LITERAL` (`:106`).
**Apply to:** the horizontal hairline (`#main-pane > section + section` `border-top-color`) and the
vertical hairline (`#doc-panel` `border-left-color`). Without the literal half, a swap from
`--color-border-subtle` (gray-6, `#d9d9d9`, `rgb(217, 217, 217)`) to `--color-border` (gray-7) is
invisible to the gate.

### Hairline carries no NON-TEXT pair, and the argument is mandatory
**Source:** the existing registration of decorative boundaries — `frontend/style.css:484`
("Decorative separators are deliberately absent — SC 1.4.11 does not apply to a border that
identifies nothing") and Phase 10's clause (c) (`:1099-1104`, re-affirming the "border band 6-8"
reasoning).
**Apply to:** both hairlines. D-11-14 requires the plan to state, per line, that it identifies no
control and no state. The counter-fact to record: gray-6 on white measures **1.412**; reaching the
3.0 NON-TEXT floor would require gray-9 (`#8d8d8d`, 3.319) and would turn the hairline into a dark
grey frame — the opposite of the phase's goal.

### Mutation testing is the only proof a rewritten assertion fails
**Source:** the milestone's stated methodology; the phase's own mutation set is D-11-13's six cases.
**Apply to:** all four rewritten criteria, done on the committed tree, restored with
`git checkout -- frontend/style.css` (**never** `git stash` — this repo forbids it: it is shared
across worktrees), then verified byte-identical.

---

## No Analog Found

None. Every file in scope has a same-file or same-family precedent from Phase 9 / Phase 10.

---

## Measured ancillary fact — `covered_files` blast radius (input to REG-04, owned by Phase 12)

Measured by parsing every report's frontmatter `covered_files` list line-by-line (not a full-text
grep) across `.planning/**/*.md`:

| file touched by this phase | reports whose `covered_files` names it |
|---|---|
| `frontend/style.css` | **11** — `v1.13/{01,02,03}-VERIFICATION.md`, `v1.14/idi-04`, `idi-04.1`, `idi-05`, `idi-06`, `idi-07`, `v1.15/idi-09`, `idi-10`, `quick/260925-iin` |
| `scripts/check-09-idi09-validation.py` | **1** — `v1.15/idi-09-card-containers/idi-09-VERIFICATION.md` |
| `scripts/check-02-contrast.py` | **1** — `v1.14/idi-04-tokens-contract/idi-04-VERIFICATION.md` |
| `scripts/check-05-ui-uat.py` (if touched) | **7** — `idi-04.1`, `idi-05`, `idi-06`, `idi-07`, `idi-08`, `idi-09`, `quick/260925-iin` |

So the phase's own two script edits pull in `idi-09` and `idi-04` respectively; leaving
`check-05-ui-uat.py` alone keeps `idi-08` out. This confirms the "先实测再处置" instruction
quantitatively. `idi-09-VERIFICATION.md`'s frontmatter also lists
`.planning/phases/idi-09-card-containers/*` paths that no longer exist (the phase dir moved to
`.planning/milestones/v1.15-phases/`) — the known fail-closed stale limitation (2026-09-14), which
the planner must account for when triaging.

---

## Metadata

**Analog search scope:** `frontend/style.css` (whole file, targeted reads), `frontend/index.html`
(DOM order + control-group presence), `frontend/app.js` (presence checks only),
`scripts/check-{01,02,05,09,10}*`, `scripts/probe-card-border-token.py`, `git log`/`git show` for
`3bc9660` / `8bfe4f9` / `6349b2e`, `.planning/**/*.md` frontmatter.
**Files scanned:** 5 source/script files in depth + 3 git diffs + 12 report frontmatters.
**Tracked-source gate:** every analog path was checked with `git ls-files -- <path>` (all non-empty).
No gitignored capability mirror (`.gsd/capabilities/**`) was used or named.
**Runtime evidence gathered:** `check-09 --item c1,c2,c3,c4` (exit 0, 46 assertions) and
`check-05 --item 8 --browser bundled` (exit 0, margin `1.000px`) were actually executed at HEAD.
**Pattern extraction date:** 2026-09-28

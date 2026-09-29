# Phase 12: G1 表头 band 与里程碑收口 - Pattern Map

**Mapped:** 2026-09-29
**Files analyzed:** 3 (all to modify)
**Analogs found:** 3 / 3

> **Scope note.** This phase is a **three-line-surface surgical fix**: one CSS declaration
> (`frontend/style.css:1657`), one new runtime item in an existing gate
> (`scripts/check-09-idi09-validation.py`), and one markdown table in a UI fixture
> (`scripts/ui-states/checking/docs/DESIGN-check-2.md`). Every line number below was re-read
> against HEAD before quoting — nothing is inferred from CONTEXT/ROADMAP prose.
>
> **No RESEARCH.md exists for this phase** (research disabled in project config). All patterns
> below come from the real codebase.

---

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `frontend/style.css` | config (design-token layer + rule body) | transform (one declaration value rewrite) | `frontend/style.css:122-147` (Phase 11 in-place fence rewrite) + `:875` / `:781` (Phase 11 in-place rule-body rewrite) | exact (same file, same idiom) |
| `scripts/check-09-idi09-validation.py` | test (runtime gate, Playwright `getComputedStyle`) | request-response (browser probe) | same file's `c1`/`c3` (computed-vs-token + literal-pinning shape) + `scripts/check-10-idi10-validation.py:304-351` (`t1`, reads a computed `background-color`) | exact (same gate family, same assertion idiom) |
| `scripts/ui-states/checking/docs/DESIGN-check-2.md` | fixture (markdown content consumed by `make_fixture`) | file-I/O (copied verbatim into every browser gate's tmp dir) | `scripts/ui-states/p3/docs/discuss-round-2.md` (markdown tables already in the repo) | role-match (both are markdown fixtures; no fixture currently carries the 问题分级 table) |

---

## Repo conventions that constrain every excerpt below

Each of these has already cost this repo a red gate. They are load-bearing, not style.

1. **就地改写,不追加覆盖 (rewrite in place, never append an override).** Phase 9 (`#doc-panel`
   `border-left`), Phase 10 (table `border`), Phase 11 (5 containers, fence values) all used the
   same idiom. Leaving a dead declaration makes comment and code contradict each other.
2. **追加,不重排 (append, never reorder).** At least one pair of equal-specificity rules is
   decided by source order; reordering is a rendering change that looks innocent in a diff.
3. **Every `style.css` plan needs ≥1 RUNTIME verification** — a real-browser computed-style
   reading. `grep -c 'var(--'` proves nothing about rendering.
4. **门禁纪律:** a gate that cannot fail is worse than no gate. Deleting assertions, loosening
   thresholds, degrading to always-true, or asserting only "the rule was written" are all
   forbidden. **Mutation testing is the only way to prove a guard really fails.**
5. **Inside the fence, never write「令牌名 + 冒号」in a comment.** `scripts/check-02-contrast.py:27`
   `DECL_RE = re.compile(r"(--[a-z0-9-]+)\s*:\s*([^;]+);")` scans the **whole fence text,
   comments included**, and `parse_decls` (`:72-74`) lets the **last** match win. A comment reading
   `` `--color-surface`: gray-2 已被控件消费; `` is parsed as a declaration. **This binds the
   `style.css:129-130` rewrite directly.**
6. **`ok()` degrades a `None` expected side to BLOCKED** (exit 2, which this project treats as a
   benign code). Every token-resolution assertion in `check-09` therefore goes through `ok_true`
   with an explicit `None` branch — see `check-09:604-609`.

---

## Pattern Assignments

### `frontend/style.css` (config, one declaration value rewrite)

**Analog:** the file's own Phase 11 rewrite of `--color-surface-page` (`:122-147`) — the exact
template for "rewrite a declaration in place and correct the load-bearing comment that the
rewrite falsifies".

**The declaration to change** (`frontend/style.css:1651-1659`, re-read at HEAD):

```css
#latest-check {
  max-height: 30vh;
  overflow-y: auto;
  padding: var(--space-1-5) var(--space-2);
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  font-size: var(--text-base);
}
```

Target: `:1657` `background: var(--color-surface);` → `background: var(--color-surface-page);`
(lines `:1652` `:1655` `:1656` stay byte-identical — D-12-3).

**The two tokens involved** (both already declared, zero new tokens):

```css
/* style.css:148 — 统一面(白) */
--color-surface-page: var(--white);
/* style.css:220 — 内陷面(gray-2) */
--color-surface: var(--radix-gray-2);
/* style.css:47 / :49 — 两个 tier-1 原语 */
--white: #ffffff;
--radix-gray-2: #f9f9f9;
```

**The colliding header declaration that stays untouched** (the other half of G1):

```css
/* style.css:1236-1243 */
.markdown-body table { border-collapse: collapse; }
.markdown-body th, .markdown-body td {
  border: none;
  border-bottom: 1px solid var(--color-border-subtle);
  padding: var(--space-1) var(--space-2-5);
  font-size: var(--text-base);
}
.markdown-body th { background: var(--color-surface); }
```

**The load-bearing comment that must be rewritten in place** (`style.css:122-147`; the falsified
sentence is at `:129-130`):

```css
  /* Phase 11 reverses the Phase 9 page-sink (SURF-02 / user decision D-11-1):
     gray-3 #f0f0f0 -> white #ffffff. This is an IN-PLACE VALUE REWRITE, not a new
     token — the declaration name and its position in the fence are unchanged. Reason:
     Phase 9 pushed the page one step DOWN so the white cards it introduced had
     something to sit against; Phase 11 removes those cards, so the page and the panels
     must read as ONE continuous white surface. The elevation story therefore goes from
     three tiers to two: the unified surface white (relative luminance 1.000000) > the
     inset control surface gray-2 (0.947307). The inset tier SURVIVES — controls and
     #latest-check still read as recessed.
                                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                    :129-130 — this half becomes FALSE
     ... */
  --color-surface-page: var(--white);
```

**The in-place correction idiom to copy** — `style.css:140-142` shows how this repo records why
the old sentence was wrong, without deleting the history:

```css
     ... (The sentence that used to stand here
     claimed a single consumer and concluded that nothing else needed synchronising —
     that half was the more dangerous half, and it is now false.) What the change also
     invalidates is every contrast pair drawn on it: the six entries on this ground
     must be RECOMPUTED — not refreshed — against white, ...
```

**Why `--color-surface` does NOT become orphaned** (D-12-1 ③ — verified at HEAD, do not re-derive).
`grep -n "var(--color-surface)" frontend/style.css` returns these consumers besides `:1657`:

```
998  #check-switcher          1013  (select 族)      1057  (select 族)
1113 (select 族)              1243  .markdown-body th
1414                          1447                   1552   .overlay-card
1648 #check-switcher (邻近规则)
```

⇒ zero token deletions, zero new contrast pairs. The PAIR ledger entry that stays valid:

```css
/* style.css:620-621 */
/* PAIR --color-text ON --color-surface-page TEXT */
/* PAIR --color-text ON --color-surface TEXT */
```

**Negative precedent (do NOT copy):** the alternatives D-12-1 rejected. `--color-surface-sunken`
(`:149` = gray-3) is also `.markdown-body code`'s ground (`:1244-1249`) and `code` has **no border
and no monospace font** (zero `monospace` / `font-family` declarations in the whole file) ⇒ moving
the host to gray-3 makes inline code collide with its own host — a new defect of the G1 family.

---

### `scripts/check-09-idi09-validation.py` (test, runtime gate — new item + element screenshot)

**Analog A — the item-function shape (`c1`..`c5`).** Every item is `def cN(page, tmp_root) -> None`,
prints a `=== cN: ... ===` banner, calls `c05.make_fixture(state, tmp_root)` + `c05.enter_project`,
then emits assertions through the shared recorders. Template (`check-09:591-602`):

```python
def c3(page, tmp_root):
    item = "c3"
    print("\n=== c3: 两级刻度 —— 统一面 == body 底色,内陷面严格更暗 ===", flush=True)
    proj = c05.make_fixture("p1", tmp_root)
    c05.enter_project(page, proj)

    body_bg = read_style(page, "body", "background-color")
    page_token = resolve_color(page, "--color-surface-page")
    sunken_token = resolve_color(page, "--color-surface")
    info("c3 body 计算 background-color 原始读数", f"{body_bg}")
    info("c3 统一面 --color-surface-page 解析值", f"{page_token}")
```

**Registration** (`check-09:796`) — one dict, item name → callable:

```python
ITEMS = {"c1": c1, "c2": c2, "c3": c3, "c4": c4, "c5": c5}
```

**The shared helpers** (imported at `check-09:99-106` from `check-05`; definitions re-read):

| Helper | Definition | Signature / behaviour |
|---|---|---|
| `ok` | `check-05:202-222` | `ok(item, label, expected, actual, note="")` — `expected is None` → BLOCKED, `actual is None` → BLOCKED, else `norm(actual) == norm(expected)` → PASS/FAIL |
| `ok_true` | `check-05:232-233` | `ok_true(item, label, cond, expected, actual, note="")` — PASS iff `cond`. **Use this for token-resolution assertions** (D-11-12 machine form) |
| `blocked` | `check-05:250-251` | `blocked(item, label, expected, actual, reason)` |
| `info` | `check-05:254-256` | `info(label, text)` — diagnostic line, never judged |
| `read_style` | `check-05:347-348` | `read_style(page, selector, prop)` → `getComputedStyle(el)[prop]`, `None` if selector missing |
| `resolve_color` | `check-05:435-455` | token → computed `rgb(...)`; returns `None` when the token is **undeclared** |
| `norm` | `check-05:225-229` | collapses whitespace inside `rgb()/rgba()` |
| `parse_rgb` / `relative_luminance` / `contrast_ratio` | `check-05:298`, `:280`, `:289` | used by `c3` for the two-tier luminance order |

**Analog B — an existing runtime assertion that reads a computed `background-color`.** This is the
exact shape the new G1 assertion copies. Two-sided pinning (token side + hard literal side), from
`c1` (`check-09:254-258`):

```python
        ok(item, f"[p1] {sel} 计算底色 == body 计算底色(同一份读数)", body_bg, bg,
           note="连续面:面板与页面同色,屏幕上不再有可辨的灰底与 elevation 差(SURF-02)")
        ok(item, f"[p1] {sel} 计算底色 == rgb(255, 255, 255)(写死字面量)",
           SURFACE_PAGE_LITERAL, bg,
           note="与上一条互补:只跟 body 比会跟着令牌一起变;这一条把统一面钉死在白")
```

**Analog C — "computed value == token's resolved value" with the `None` branch** (`c3:606-614`).
This is the pattern for D-12-7's "宿主 == 白" half:

```python
    ok_true(item, "[p1] --color-surface-page 已声明且可解析(堵住 ok() 的 None-期望侧降级)",
            page_token is not None, "非 None", str(page_token),
            note="ok() 在期望侧为 None 时记 BLOCKED(exit 2,本项目当良性码)—— 令牌缺失"
                 "必须是 FAIL,不是 BLOCKED")
    ok_true(item, "[p1] body 计算底色 == --color-surface-page 解析值(底色来自令牌)",
            page_token is not None and c05.norm(body_bg) == c05.norm(page_token),
            f"== {page_token}", str(body_bg),
            note="等值复核:证明底色来自令牌而不是硬编码的 rgb()。少了这条,把 body 写成"
                 "字面量再删掉令牌声明也能全绿")
```

**Analog D — literal constants declared module-level, both sides written down** (`check-09:137-139`).
`SURFACE_PAGE_LITERAL` already exists and is exactly the white the new assertion needs:

```python
SURFACE_PAGE_LITERAL = "rgb(255, 255, 255)"
SURFACE_SUNKEN_LITERAL = "rgb(249, 249, 249)"
HAIRLINE_LITERAL = "rgb(217, 217, 217)"
```

**Analog E — the cross-file precedent for reading a computed `background-color` on a markdown
table** (`scripts/check-10-idi10-validation.py:304-351`, `t1`). **This file is NOT modified this
phase (D-12-4)** — it is a read-only style reference:

```python
    def assert_pair(pair, host):
        ok(item, f"{pair} .markdown-body th 计算 background-color == var(--color-surface)",
           tokens["surface"], read_style(page, f"{host} th", "background-color"),
           note="表头浅底落三级刻度的「内陷面」档(D-10-1);HEAD 上 th 无自身底色(透明)")
```

```python
# check-10:101 — gray-2 字面量,两侧写死
TH_BG_LITERAL = "rgb(249, 249, 249)"
# check-10:117-123 — 5 个 (样本, 宿主) 对,含 ("p1", "#latest-check")
TABLE_PROBES = (
    ("p1", "#draft-content"), ("p1", "#brainstorm-content"), ("p1", "#round-doc"),
    ("p1", "#latest-check"), ("p3", "#round-doc"),
)
```

**Consequence for this phase:** `t1` pins `th`'s background to the gray-2 literal and never reads
the host's background ⇒ changing `#latest-check`'s host ground leaves `t1` fully green (D-12-1 ②).

**Analog F — the element screenshot precedent** (`check-10:652-657`, the code CONTEXT cites as
`:653`):

```python
    png_path = out_dir / f"input-radius-{label}.png"
    page.locator(RADIUS_SNAPSHOT_SEL).screenshot(path=str(png_path))
    width, height = png_size(png_path)
    ok_true(item, f"[{label}] 元素级截图落盘且宽高非零",
            width is not None and height is not None and width > 0 and height > 0,
            "width > 0 and height > 0", f"{width}x{height}", note=str(png_path))
```

with `RADIUS_SNAPSHOT_SEL = "#chat-input-row input"` (`check-10:141`) and `png_size`
(`check-09:177-186`, byte-identical copy of check-10's).

**Analog G — `run_screenshots` in check-09** (`:774-793`), which already iterates `c05.STATES`
(`check-05:584` = `["p1","p12","p3","checking","archive"]`):

```python
def run_screenshots(page, out_dir, tmp_root):
    item = "shot"
    print("\n=== shot: 逐样本整窗截图(1440x900)===", flush=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    made = []
    for state in c05.STATES:
        proj = c05.make_fixture(state, tmp_root)
        c05.enter_project(page, proj)
        path = out_dir / f"{state}.png"
        page.screenshot(path=str(path))
        width, height = png_size(path)
        made.append(state)
        info(f"shot {state}", f"{path} {width}x{height}")
        ok_true(item, f"shot [{state}] 截图落盘且为 1440x900",
                width == 1440 and height == 900, "1440x900", f"{width}x{height}")
    ok(item, "shot 样本清单逐项一一对应(无缺项、无多余样本)",
       list(c05.STATES), made, note=f"来源 check-05 的 STATES={c05.STATES}")
    pngs = sorted(p.name for p in out_dir.glob("*.png"))
    ok(item, "shot 输出目录恰含 5 个 PNG",
       sorted(f"{s}.png" for s in c05.STATES), pngs)
```

**⚠ Hard constraint on the new element screenshot (see Ripple Risks §R1):** the last assertion
asserts the output directory contains **exactly 5** PNGs. Dropping `latest-check.png` into that
same directory makes the existing assertion **FAIL**. The repo's own precedent is a **separate
destination**: `check-10`'s element snapshot takes its own `--radius-snapshot LABEL DIR`
(`check-10:682-686`, dispatched at `:730-732`), and the artifact on disk lives in a
**subdirectory** — `.planning/milestones/v1.15-phases/idi-10-tables-and-radius-scale/screenshots/chat-user/p1-chat-user-evidence.png`.

**Mutation-proof documentation convention** (the repo requires "mutation → FAIL real reading").
Precedent: `.planning/phases/idi-11-decard-and-hairline-dividers/idi-11-03-SUMMARY.md:193-300`
and `idi-11-05-SUMMARY.md`. The shape, verbatim from the repo:

```markdown
## 六条变异测试 —— 逐条「变异 → FAIL」真实读数

> **前置条件(第 1 步,逐条记录):**
> - `git status --porcelain frontend/` **干净**(波次 1/2 的改动已提交)⇒ 变异确实做在**已提交的树**上
> - `git rev-parse HEAD` = `315af14e53b58ee7ca8ccda3bc68620edef1dfe0`
> - `git hash-object frontend/style.css` = `cfcaef098d957abc885413793cd8b1a9dc12193f`
> - 基线 `.venv/bin/python scripts/check-09-idi09-validation.py --item c1,c2,c3,c4` → `exit=0`
>
> **⚠ 全程未使用 `git stash`**(它跨工作树共享,本项目明令禁止)。还原一律 `git checkout -- frontend/style.css`。

### 变异 N — <一句话说清注入什么> → `cN` 必红

- **注入:** `<旧值>` → `<新值>`
- **观察(FAIL 原文,N 条,含 `expected=` / `actual=`):**

```
FAIL <label>: expected=<...> actual=<...>  # <note>
item cN: FAIL  (M 条断言,K FAIL,0 BLOCKED)
exit=1  (0=全 pass,1=有 fail,2=有 blocked)
```

- **还原:** `git checkout -- frontend/style.css` → `git diff --exit-code -- frontend/style.css` **rc=0**;
  `git hash-object` = `<同一个 sha>`(逐字符相同)
```

The binding rules (D-12-7 + repo discipline, all already enforced in Phase 11):
mutation done **on the committed tree**; restore via **targeted `git checkout --`**; **`git stash` is
banned**; byte-identical restore proven by `git diff --exit-code` rc=0 **and** `git hash-object`;
the FAIL reading must be quoted **raw**, never merely asserted.

Gate logs land in `<phase-dir>/gate-logs/<plan-id>/` (see
`.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/`, 17 files including
`check-01-token-conformance.log` … `check-10-idi10-validation.log`, `pytest.log`).

**Also update the module docstring's mapping table** (`check-09:40-66`), which enumerates
`c1 → REG-01 / SURF-01 / SURF-02`, … `shot → 逐样本整窗截图`. A new item with no line there is
the same class of doc/code divergence this repo keeps correcting.

---

### `scripts/ui-states/checking/docs/DESIGN-check-2.md` (fixture, markdown content)

**Current content, verbatim and complete (7 lines, re-read at HEAD):**

```markdown
# 核查报告 2

## 发现

- 术语表未覆盖「轮次冻结」。
- §4.2 未定义划词菜单的键盘路径。

> 核查结论:FIX(问题 2 项)
```

**Sibling that DOES carry tables** (formatting analog — column widths, separator style, heading
levels): `scripts/ui-states/p3/docs/discuss-round-2.md`:

```markdown
## 1. 批注回应(2/2)

| 批注id | 原文摘录 | 回应 |
|--------|---------|------|
| a1 | 先做全文检索就够 | 采纳,标签降级为可选 |
| a2 | 不要引入数据库 | 采纳,检索走内存索引 |
```

Note the repo's actual separator idiom is `|--------|---------|------|` (no spaces), **not** the
`|---|---|---|` the prompt grammar shows at `backend/prompts.py:497`. The grammar's requirement is
about the **header row being byte-exact**, not the separator.

**The grammar the fixture must satisfy** (`backend/prompts.py:486-509`, verbatim):

```python
_CHECK_GRAMMAR_EXAMPLES = (
    "报告文法(逐字遵守,工具按此解析):",
    "",
    "报告首行为档位头部行(恰为以下两串之一,「档位」由任务方给定):",
    "",
    "> 自检档位:严格",
    "> 自检档位:宽松",
    "",
    "问题分级表(二级标题含「问题分级」,表格列头逐字如下,级别仅 P0/P1/P2):",
    "",
    "| 编号 | 级别 | 位置 | 问题 | 建议修法 |",
    "|---|---|---|---|---|",
    "",
    "末行结论(报告最后一个非空行,恰为以下两形态之一;零问题时必须 PASS):",
    "",
    "> 核查结论:FIX(P1×2,P2×1 …)",
    "> 核查结论:PASS",
    ...
```

**⚠ Grammar-faithfulness gap the planner must resolve (see Ripple Risks §R2).** The parser is
`backend/grammar.py:329-359` `parse_problem_grades` → `_extract_table(md_text, "问题分级")`, and
`_extract_table` (`grammar.py:88-118`) locates the table **only under a `## ` heading whose text
contains「问题分级」**:

```python
def _extract_table(md_text: str, heading_keyword: str) -> list[list[str]]:
    """共通表格解析:定位首个标题含关键词的二级标题,取其下连续表格行。"""
    ...
        if line.startswith(_HEADING_PREFIX):
            if in_target:
                break
            in_target = heading_keyword in line
            continue
```

D-12-8's literal "只加 `| 编号 | 级别 | 位置 | 问题 | 建议修法 |` 表头 + 分隔行 + 至少一行数据"
therefore yields a table that **renders** (marked ⇒ `<thead><th>`, which is all G1's screenshot
needs) but that `parse_problem_grades` returns `[]` for — i.e. it would **not** be "忠于后端文法",
which is D-12-5's stated rationale. Adding the `## 问题分级` heading closes that gap, but is a
strictly larger change than D-12-8's wording.

---

## Ripple Risks (measured at HEAD — the planner must decide these explicitly)

### R1 — The element screenshot breaks an existing assertion if dropped into the same directory

`check-09:791-793` asserts the screenshot output directory contains **exactly** the 5 state PNGs.
D-12-9 adds a 6th. Two viable routes, both with repo precedent:

- **Route (a) — subdirectory (the repo's own precedent).** Phase 10's element snapshot landed in
  `.../idi-10-tables-and-radius-scale/screenshots/chat-user/p1-chat-user-evidence.png`, i.e. a
  child directory, leaving the parent's "exactly 5 PNGs" assertion untouched.
- **Route (b) — a second CLI flag with its own DIR**, exactly as `check-10`'s
  `--radius-snapshot LABEL DIR` (`check-10:682-686`) is separate from `--screenshot DIR`
  (`:680-682`), dispatched independently at `:730-732`.

Route (b) requires editing `parse_args` (`check-09:799-806`) and the `summary` list
(`:852`) plus the `if args.screenshot:` dispatch (`:835-836`). Route (a) requires only that the new
code write into a subdirectory. **Neither route may delete or weaken the existing
"恰含 5 个 PNG" assertion.**

### R2 — The added table can flip the `checking` sample's UI mode from `running` to `p2`

`checking` is the **only** sample where `#latest-check` is visible (its ancestor `#checks-panel`
carries `.hidden` elsewhere). The sample's UI mode is derived from the fixture report at runtime by
`backend/session.py:228-263` `_selfcheck_substate`:

```python
    if st == STATE_PHASE5_CHECKING:
        latest = latest_check_content_mod(project / "docs") or ""
        tier = grammar_mod.parse_tier_line(latest) or checks_mod.read_tier(project)
        ...
        # 纯 P2 残余:末行非 PASS + is_pure_p2(半份 fail-closed 回落 running)
        if not grammar_mod.is_pass_conclusion(latest) and grammar_mod.is_pure_p2(latest):
            return {"tier": tier, "mode": "p2", "questions": [ ... ]}
        return {"tier": tier, "mode": "running", "questions": []}
```

`is_pure_p2` (`backend/grammar.py:362-375`) is true iff **every row's `level == "P2"`** and the
report has a conclusion line. The fixture's conclusion is `> 核查结论:FIX(问题 2 项)` — non-PASS.

⇒ **A `## 问题分级` heading + an all-P2 table flips the mode to `p2`.** The front-end then changes
the whole control area (`frontend/app.js:684-693`):

```javascript
  } else if (mode === 'p2') {
    // 纯 P2 残余态:隐藏继续自检;呈现残余裁决卡({number, location, issue, suggestion})
    continueCheckBtn.classList.add('hidden');
    continueRepairBtn.classList.add('hidden');
    (selfcheck.questions || []).forEach((q) => {
      verdictCards.appendChild(renderVerdictCard(q, 'p2'));
    });
```

i.e. `#btn-continue-check` disappears and `.verdict-card`s appear — a **new sibling subtree inside
`#checks-panel .panel-body`**, right below `#latest-check`. That is a ripple across all five
browser gates (`check-05` / `06` / `07` / `09` / `10` all consume the `checking` sample through
`make_fixture`) plus the 6 screenshots.

**Two safe shapes, both keeping `mode == running`:**
- **(i)** add the table **without** the `## 问题分级` heading → `parse_problem_grades` → `[]` →
  `is_pure_p2` False. Minimal (matches D-12-8 literally), but not grammar-faithful.
- **(ii)** add `## 问题分级` + a table whose rows include **at least one P0/P1** →
  `is_pure_p2` False (any non-P2 row short-circuits it). Grammar-faithful (D-12-5's rationale) and
  the UI mode is unchanged. The single all-P2 shape is the one to avoid.

Also note the fixture has **no** `> 自检档位:` line, so `parse_tier_line` returns `None` and
`tier` falls back to `checks_mod.read_tier(project)` — D-12-8 deliberately leaves that alone.

### R3 — Verified-zero ripples (measured; do not re-derive)

- **`check-05`'s scroll-container census is declaration-based, not content-based.**
  `PANEL_SCROLLERS = ("#chat-messages", "#latest-check", "#main-pane")` (`check-05:2436`) is read
  from computed `overflow-y` in `{auto, scroll}`, and `check-05:2717-2727` asserts the set is
  *exactly* those three. `#latest-check` declares `overflow-y: auto` (`style.css:1653`) ⇒ it stays
  in the set no matter how long the fixture report becomes.
- **`check-05`'s `#latest-check` reachability probe injects its own content** (`check-05:2464-2467`,
  60 paragraphs via `renderMarkdown`), so it does not depend on the fixture report body.
- **`check-05`'s `max-height: 30vh` guardrail counts source text** (`check-05:2519-2537`), not
  rendered height.
- **`probe-card-border-token.py:45`** lists `#latest-check` among `NON_CARD_SELECTORS` and reads
  its **`border-top-color`** — the change touches only `background`, so it stays green (D-12-3).
- **`check-01` / `check-03` / `check-04`** count bare hex outside the fence, `^.hidden {` rules,
  and `!important;` declarations respectively — none is affected by a declaration *value* rewrite
  or a fixture edit. `check-02`'s `DECL_RE` scans the fence: see convention 5 above for the
  comment-rewrite constraint.
- **`check-10`'s `t1`** reads `th`'s background against the gray-2 literal, never the host's ⇒
  stays green (see Analog E).

---

## Shared Patterns

### Two-sided literal pinning (every color assertion in `check-09`)
**Source:** `check-09:137-139` + `:254-258`, `:364-371`, `:403-405`
**Apply to:** the new G1 assertion

```python
# 两侧都写死:只跟令牌比会跟着令牌一起变,只跟字面量比会漏掉「令牌被改坏而消费者仍接线」。
ok(item, "... == rgb(255, 255, 255)(写死字面量)", SURFACE_PAGE_LITERAL, bg, note="...")
```

### Token-resolution assertions go through `ok_true`, never `ok`
**Source:** `check-09:604-609` (the rule), `:606-609` / `:610-614` (the shape)
**Apply to:** every assertion whose expected side comes from `resolve_color` / `resolve_token`

```python
ok_true(item, "... 已声明且可解析(堵住 ok() 的 None-期望侧降级)",
        token is not None, "非 None", str(token),
        note="ok() 在期望侧为 None 时记 BLOCKED(exit 2,本项目当良性码)—— 令牌缺失必须是 FAIL")
```

### Fixture entry point (shared by every browser gate)
**Source:** `check-05:490-498` `make_fixture` + `:510-516` `enter_project`
**Apply to:** any new item that needs a browser sample

```python
def make_fixture(name, tmp_root):
    """把 scripts/ui-states/<name> 复制到临时目录的新副本,返回其绝对路径。"""
    src = STATES_SRC / name
    if not src.is_dir():
        raise SystemExit(f"ERROR: 状态样本不存在:{src}")
    dest = Path(tempfile.mkdtemp(dir=str(tmp_root), prefix=f"{name}-"))
    dest = dest / name
    shutil.copytree(src, dest)
    return dest
```

`STATES = ["p1", "p12", "p3", "checking", "archive"]` (`check-05:584`).

### Gate-log + screenshot artifact convention
**Source:** `.planning/phases/idi-11-decard-and-hairline-dividers/gate-logs/idi-11-05/` (17 logs)
**Apply to:** REG-04's full re-run and VIS-01's screenshots

- Gate logs → `<phase-dir>/gate-logs/<plan-id>/<gate-name>.log`, one file per gate, raw output.
- Whole-window screenshots → `<phase-dir>/screenshots/<state>.png`, five files named exactly
  `p1.png` / `p12.png` / `p3.png` / `checking.png` / `archive.png` (both v1.15 screenshot dirs
  contain exactly these five names).
- Element close-ups → a **subdirectory** (see R1), e.g. `screenshots/latest-check/<name>.png`.

---

## No Analog Found

| File | Role | Data Flow | Reason |
|---|---|---|---|
| — | — | — | All three targets have close analogs. The **`## 问题分级` heading in a UI fixture** has no precedent — neither `checking/docs/DESIGN-check-2.md` nor `archive/docs/DESIGN-check-1.md` carries one, and no other `ui-states` markdown uses that heading. Its grammar is specified only by `backend/prompts.py:486-509` + `backend/grammar.py:88-118`. |

---

## Metadata

**Analog search scope:** `frontend/` (`style.css`, `index.html`, `app.js`), `scripts/` (all gates,
fixtures, probes), `backend/` (`prompts.py`, `grammar.py`, `session.py`), `.planning/phases/idi-11-*`
and `.planning/milestones/v1.15-phases/*` (precedent documentation)
**Files scanned:** 16 read in full or in targeted non-overlapping ranges; 3 additional greps
**All named analogs verified git-tracked** via `git ls-files --` (no gitignored mirror paths used):
`frontend/style.css`, `frontend/index.html`, `frontend/app.js`, `backend/prompts.py`,
`scripts/check-02-contrast.py`, `scripts/check-05-ui-uat.py`, `scripts/check-09-idi09-validation.py`,
`scripts/check-10-idi10-validation.py`, `scripts/probe-card-border-token.py`,
`scripts/ui-states/checking/docs/DESIGN-check-2.md`,
`scripts/ui-states/archive/docs/DESIGN-check-1.md`,
`scripts/ui-states/p3/docs/discuss-round-2.md`
**Pattern extraction date:** 2026-09-29

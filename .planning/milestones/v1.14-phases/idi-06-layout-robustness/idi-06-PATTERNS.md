# Phase 6: 布局稳健性 - Pattern Map

**Mapped:** 2026-09-22
**Files analyzed:** 2 (both modified, neither created)
**Analogs found:** 2 / 2 (both are the files themselves — this is a structural-diff phase; every pattern is an *existing convention inside the file being edited*)

**Phase character:** This is NOT a "new files" phase. There is exactly one source file to edit (`frontend/style.css`) plus one harness to extend (`scripts/check-05-ui-uat.py`). The analogs below are therefore (a) the *existing rules this phase mutates in place*, and (b) the *existing conventions in the same file that the new rules must imitate*. Every path below is git-tracked (verified via `git ls-files`).

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `frontend/style.css` (5 in-place edits) | config (stylesheet) | transform (declaration-level structural diff) | itself — the 5 target rule bodies | exact (self-analog) |
| `frontend/style.css` (3 appended rules) | config (stylesheet) | transform | `style.css:1192-1265` (Phase 5 tail append block) | exact |
| `scripts/check-05-ui-uat.py` (item 8) | test | request-response (Playwright runtime assertion) | `item7` (`:1411-1508`) + `item5` rect diagnostic (`:1305-1312`) | role-match |
| `scripts/check-05-ui-uat.py` (item 9) | test | request-response + batch (DOM census) | `check_render_markdown_call_sites` (`:912-935`) + `MARKDOWN_TARGETS` (`:889-904`) | role-match |
| `scripts/check-05-ui-uat.py` (dispatch wiring) | config | event-driven | `main()` dispatch (`:1593-1636`) + `normalize_items` (`:1581-1599`) | exact |
| `frontend/style.css` `@media` guard (**conditional**) | config | transform | **none — no `@media` exists in the file** | no analog |

**Zero-change files (confirmed, do not open for edit):** `frontend/app.js`, `frontend/index.html`, `frontend/vendor/`, `scripts/check-01…04`.

---

## Pattern Assignments

### A. `frontend/style.css` — in-place declaration edits (5 sites)

**Analog:** the target rule bodies themselves. The load-bearing convention is **Hard Rule 3「追加,不重排」: delete/add declarations *inside* the existing rule body; never move the rule block.** The UI-SPEC line numbers match the disk exactly (verified by read).

**A-1 · `.event-list` delete two declarations** (`style.css:564-575`):

```css
/* 事件列表与条目 */
.event-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-1-5);
  max-height: 55vh;      /* ← DELETE this line */
  overflow-y: auto;      /* ← DELETE this line */
  border: 1px solid var(--color-border-subtle);
  border-radius: var(--radius-sm);
  padding: var(--space-2);
  background: var(--color-surface);
  transition: background-color 0.3s;   /* ← KEEP (INTERACT-02, Phase 7) */
}
.event-list.streaming { background: var(--color-surface-streaming); } /* KEEP */
.event-list.aborted { background: var(--color-surface-danger); }      /* KEEP */
```

**A-2 · `#annotation-list` delete two declarations** (`style.css:913-920`):

```css
#annotation-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2-5);
  max-height: 32vh;      /* ← DELETE */
  overflow-y: auto;      /* ← DELETE */
  padding: var(--space-half);   /* ← KEEP (L-5 census input) */
}
```

**A-3 · `#main-pane` add one declaration** (`style.css:453-460`):

```css
#main-pane {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-1-5);
  overflow-y: auto;      /* ← KEEP (L-4: the one outer scroller) */
  align-items: center;
  min-width: 0;          /* ← ADD (L-3 / D-09) */
}
```

**A-4 · `#doc-panel` add one declaration** (`style.css:468-475`):

```css
#doc-panel {
  flex: 0 0 var(--doc-panel-w);
  display: flex;
  flex-direction: column;
  overflow-y: auto;      /* ← KEEP */
  border-left: 1px solid var(--color-border-subtle);
  background: var(--color-surface);   /* ← the token D-05's sticky bg reuses */
  min-width: 0;          /* ← ADD (L-3 / D-09) */
}
```

**A-5 · `.annotation-answer summary` add two declarations** (`style.css:991-996`):

```css
.annotation-answer summary {
  cursor: pointer;                 /* KEEP */
  color: var(--color-text-muted);  /* KEEP */
  font-size: var(--text-xs);       /* KEEP (12px — the reason it fails 24×24) */
  margin-top: var(--space-1);      /* KEEP */
  min-height: 24px;                /* ← ADD (L-6 / D-16) */
  min-width: 24px;                 /* ← ADD (L-6 / D-16) */
}
```

**Precedent for "edit a selector in place rather than append a duplicate":** `style.css:932-941` (`.annotation-quote::before`, VISUAL-05 / D-20/D-21/D-22) — the comment explicitly argues that when a selector is file-unique and uncontested, in-place rewrite is cascade-equivalent to append **and** avoids leaving a dead overridden declaration. 05-UI-SPEC D-21 is the cited precedent. Use this same justification form for A-1…A-5.

---

### B. `frontend/style.css` — appended new rules (append at end, never reorder)

**Analog:** `style.css:1192-1265` — the Phase 5 tail block. Three consecutive appended rules, each preceded by a long rationale comment, each explicitly tagged `追加在文件末尾 —— 硬规则 3:追加,不重排`.

**B-1 · `#doc-panel-header` sticky header (L-1)** — target insertion point per UI-SPEC: **after `:487-490`** (`#doc-panel.collapsed #doc-panel-header`).

**Precedent comment style** (from `style.css:1198-1217`, the active-panel marker — same "four load-bearing decisions" shape the L-1 comment needs):

```css
/* 活动面板标记(VISUAL-04 / D-17,追加在文件末尾 —— 硬规则 3:追加,不重排)。
   ...
   四条承重决定:
   (1) 用 box-shadow 的 inset 竖条而非 border-left —— box-shadow 不参与布局、零位移,
   ...
   #doc-panel-header 虽是 .panel-header,但不被下面三条 ID 选择器匹配,故无意外覆盖。
   特异性 1-2-0 / 1-2-1,靠 ID 分量取胜,与源码顺序无关;仍追加在末尾,以防日后有人给
   .panel-header 补 box-shadow。 */
```

The L-1 rule must mirror this shape (UI-SPEC §L-1 supplies the exact comment text and the **四条承重约束**):

```css
#doc-panel-header {
  position: sticky;
  top: 0;
  background: var(--color-surface);   /* required: .panel-header has NO background (see :509-518) */
  border-radius: 0;                   /* S-1 sign-off item */
}
```

**Specificity accounting precedent** — the file already writes these out. `#doc-panel-header` = 1-0-0 beats `.panel-header` = 0-1-0 regardless of source order; `#doc-panel.collapsed #doc-panel-header` (`:487-490`, 1-1-0) declares only `justify-content` / `padding-inline` ⇒ no competing declaration. Cite this in the comment (UI-SPEC §L-1 constraint 4).

**B-2 · Six-target `overflow-wrap` rule (L-3)** — append at **`:1265` (file end)**, adjacent to the Phase 5 injection-target enumeration comment.

**Analog for the enumeration discipline:** `style.css:1229-1265` (the embedded-heading-scale block). Its comment explicitly rejects a global type selector because *"它无法表达三档各不相同… 把「哪些容器受影响」这件事重新变成不可枚举 —— 那正是本缺陷的成因"*. L-3's rule must reuse this exact argument for rejecting a wildcard `overflow-wrap` rule (which would also hit the already-adjudicated `.event-content { word-break: break-all }` at `:598-601`).

```css
/* 六目标枚举 —— 与 renderMarkdown() 的调用点一一对应(Phase 5 idi-05-04 已建立该枚举)…
   必须用 anywhere 而非 break-word:按 CSS Text 3,只有 anywhere 参与 min-content 内在尺寸计算,
   break-word 不参与 —— 这是下面 min-width: 0 能生效的前提,注释必须写明。 */
.markdown-body, .event-content, .chat-bubble, .say-chunk, .annotation-note, .annotation-answer-body {
  overflow-wrap: anywhere;
}
```

**Six-target HEAD state (verified by read):**

| Target | HEAD line | Current protection |
|---|---|---|
| `.markdown-body` | `:709-712` | none |
| `.event-content` | `:598-602` | `word-break: break-all` + `white-space: pre-wrap` |
| `.chat-bubble` | `:812-819` | `word-break: break-word` |
| `.say-chunk` | (no rule block) | none |
| `.annotation-note` | `:959` | none |
| `.annotation-answer-body` | `:997` | none |

**`min-width: 0` is NOT part of B-2** — per UI-SPEC §L-3 it goes into the two **existing** rule bodies (A-3 / A-4), not a new rule. Its comment must state why it is not redundant once `anywhere` lands (D-09), or it will be deleted as dead code.

---

### C. `frontend/style.css` — comment conventions (applies to every edit above)

**Analog:** the token fence and tail comments. These are the *load-bearing* conventions in this repo — comments carry arithmetic, rejected alternatives, and specificity proofs, because the file has no build step and no test that can read intent.

| Convention | Source excerpt |
|---|---|
| Fence header/footer markers | `style.css:5` `/* ===== DESIGN TOKENS: START ===== */` |
| Arithmetic written out | `:252-257` (line-height ratio pairing: `28k 与 22k 同时为整数要求 k 是 0.5 的倍数…`) |
| "why not the alternative" is mandatory | `:1250-1258` (why not a global selector; why no margin/line-height) |
| Specificity proof inline | `:1260-1262` (`五组选择器全部是 0-1-1,与既有规则无竞争 —— …已逐条核过`) |
| Cross-reference to the guard that enforces it | `:1247-1248` (`该不等式由 check-05 的 item7 先造容器再断言`) |
| Token-declaration comment names its consumer | `:206` (`Tier 2 — declared with their consumers (Hard Rule 5)`) |
| Layout token rationale | `:224-227` (`--doc-panel-w` — 「值交由用户裁决,执行器不得自行改动」) |

**Zero-new-token rule:** the fence `:root` block spans `:6` … (closes after `:343`). This phase adds **nothing** inside it. The only token reference the new rules introduce is `var(--color-surface)` — already consumed by `#doc-panel` at `:474`, so Hard Rule 5 is satisfied without a new declaration.

**Unitless-`0` exception:** `top: 0` and `border-radius: 0` are unitless zeros, which hit existing exception **L-2** (UI-SPEC §Spacing Scale). No new exception row is created.

---

### D. `frontend/style.css` — conditional `@media` guard (L-2)

**No analog exists.** `grep -n "@media" frontend/style.css` → **zero hits**. `grep -n "position: sticky"` → **zero hits**. This is the one genuinely novel construct in the phase.

**Consequence for the planner:** the guard is a **conditional deliverable**. Per UI-SPEC §L-2 decision rule, it lands *only* if the three-width measurement (1440 / 1024 / 768) shows breakage in the 768–1023px band. If measurement shows none, the deliverable is registered as "被实测推翻" and **no `@media` is written**. The planner must sequence the measurement *before* the plan that would write it (CONTEXT D-08: "这是**计划之前的步骤**,不是计划里的一步").

**If written, its form is locked** (UI-SPEC §L-2 supplies the verbatim comment header). The literal `1023px` is a non-hex literal, so `scripts/check-01-token-conformance.sh` (which counts bare `#hex` only) does not fire.

---

### E. `scripts/check-05-ui-uat.py` — item 8 (L-1's gate) and item 9 (L-4's gate)

**Analog:** `item7` (`:1411-1508`) for new-item shape; `item5`'s rect diagnostic (`:1305-1312`) for the only existing `getBoundingClientRect()` usage; `check_render_markdown_call_sites` (`:912-935`) for the DOM-census guard.

**E-1 · Assertion recorder API — every assertion goes through one of these** (`:96-167`). Nothing may be silently skipped:

```python
_emit(item, verdict, label, expected, actual, note="")   # :96
ok(item, label, expected, actual, note="")               # :113 — equality; None ⇒ BLOCKED
ok_true(item, label, cond, expected, actual, note="")    # :143 — boolean
ok_contains(item, label, needle, actual, note="")        # :147
blocked(item, label, expected, actual, reason)           # :161 — element/selector missing
info(label, text)                                        # :165 — diagnostic, not judged
```

**Two BLOCKED directions are load-bearing** (`:126-131`): `expected is None` ⇒ "token undeclared / expected unresolved"; `actual is None` ⇒ "element/selector missing". Both must be used in the new items — a missing `#state-badge` or an unresolvable token must be BLOCKED, never PASS.

**E-2 · Runtime rect read pattern** — the only existing `getBoundingClientRect()` call (`:1305-1312`):

```python
clickable = page.evaluate("""() => {
    const el = document.querySelector('#btn-send');
    if (!el) return null;
    const r = el.getBoundingClientRect();
    const top = document.elementFromPoint(r.left + r.width/2, r.top + r.height/2);
    return { top: top ? (top.id || top.className || top.tagName) : null,
             is_send: top === el || (top && el.contains(top)) };
}""")
```

Item 8 must reuse this shape for: (a) badge × banner intersection at 768/1024/1280; (b) sticky header still visible after scrolling `#doc-panel` to bottom. Item 9 needs the same shape for "both scrollers reach bottom". **Always return `null` for a missing element and convert to `blocked()`, never to a false PASS** — item7's comment at `:1498-1499` documents exactly this trap (`all(w != "700")` is vacuously true on `None`).

**E-3 · Viewport resize for the three-width assertion** — the context is created once at `:1617`:

```python
ctx = browser.new_context(viewport={"width": 1440, "height": 900})
```

There is **no existing `set_viewport_size` call**. The planner must add one (or use `page.set_viewport_size`) inside item 8, and must restore 1440×900 before returning so item 9 (or any later item) is not affected by leftover state. Document the restore in the comment — this is the first stateful viewport mutation in the harness.

**E-4 · New-item skeleton** — mirror `item7`'s structure (`:1411-1517`):

```python
def item7(page, tmp_root):
    item = "7"
    print("\n=== UAT 7: … ===", flush=True)
    proj = make_fixture("p1", tmp_root)   # :401 — idempotent copy; repo samples stay read-only
    enter_project(page, proj)             # :421
    info("item7 …", f"…")
    …                                     # assertions
    check_render_markdown_call_sites(item)  # static guard appended last
```

**E-5 · DOM-census guard (item 9's core)** — analog `check_render_markdown_call_sites` (`:912-935`):

```python
def check_render_markdown_call_sites(item):
    count = APP_JS.read_text(encoding="utf-8").count("renderMarkdown(")
    ok_true(item, "app.js 的 renderMarkdown( 计数 == 11(1 定义 + 10 调用点)",
             count == RENDER_MARKDOWN_CALL_SITES, RENDER_MARKDOWN_CALL_SITES, count,
             "调用点数变了 ⇒ 按调用点更新 MARKDOWN_TARGETS,再跑本项")
```

Two disciplines to copy verbatim:
1. **Count two independent quantities, never self-compare** (`:917` — *"比的是「调用点数 vs 枚举条数」两个独立量 —— 不是自比"*). Item 9's "exactly two scrollers" must be a DOM census computed in-page (`overflow != visible` walk), compared against the expected set `{#main-pane, #latest-check}` — not against a hardcoded selector list.
2. **The FAIL message tells the reader the executable next action.**

**E-6 · Enumeration table precedent** — `MARKDOWN_TARGETS` (`:889-904`) is the structural model for any enumeration the new items need (e.g. the scroller whitelist):

```python
MARKDOWN_TARGETS = (
    ("#draft-content", "renderDraft", "doc"),
    …
)
MARKDOWN_HOSTS = tuple(sel for sel, _fn, fam in MARKDOWN_TARGETS if fam == "doc")
RENDER_TARGETS = tuple(sel for sel, _fn, fam in MARKDOWN_TARGETS if fam == "embedded")
```

Note the "给人核对的锚点(它比行号稳)" convention at `:886-888` — function names, not line numbers, as human anchors.

**E-7 · Wiring a new item** — three coordinated edits (`:1581-1599`, `:1593-1636`):

```python
def normalize_items(raw):
    if not raw:
        return ["1", "2", "3", "4", "5", "6", "7"]        # ← add "8", "9"
    …

def main():
    …
    known = {"smoke", "1", "2", "3", "4", "5", "6", "7"}   # ← add "8", "9"
    …
    if "7" in items:
        item7(page, tmp_root)
    if "8" in items:                                        # ← new dispatch
        item8(page, tmp_root)
    if "9" in items:                                        # ← new dispatch
        item9(page, tmp_root)
```

Also update: the docstring usage block (`:31-38`), the `--item` help string (`:1569-1570`), and the module docstring's item list. The verdict summary at `:1654-1668` is **automatic** — it iterates `ROWS` filtered by item, so no change is needed there.

**E-8 · Environment constraints that the new items must not fight** (`:18-29`, `:64-69`):
- Default `--browser bundled`; `--browser chrome` forces `headless=False` because `channel="chrome"` + headless deadlocks on this machine (x86_64 venv under Rosetta).
- Never use `wait_until="networkidle"` — the app holds a permanent `/api/events` SSE connection (`:60-61`).
- **Screenshots are unavailable** (headless capture blocked by the SSE stream) ⇒ plan computed-style + rect assertions and named manual steps, never visual diff.

---

## Shared Patterns

### Hard Rule 3 — 追加,不重排 (applies to every `style.css` edit)
**Source:** `style.css:1186` (`绝不插入、绝不重排(Global Hard Rule 3)`), `:1198`, `:1229`.
At least one pair of equal-specificity rules is decided by source order (`#draft-view > h2` at `:704` and `#brainstorm-view > h2`). Deleting `max-height`/`overflow-y` **must** happen in place (A-1/A-2); new rules **must** be appended at the end (B-1/B-2). A source diff that looks innocent changes rendering.

### Hard Rule 5 — 不得触碰 / with-consumer discipline
**Source:** UI-SPEC §Global Hard Rules 5; `style.css:206`, `:660-663` (`.verdict-buttons`' two disabled rules).
Do-not-touch for this phase (UI-SPEC §Do-Not-Touch List, appended table): `#state-badge { z-index: var(--z-badge) }` (`:678`) · `#session-panel { flex: 1 1 auto; min-height: 200px }` + `:has(:empty)` (`:783`, `:802-803`) · `.event-list { transition }` + `.streaming` / `.aborted` (`:574-577`) · `.collapse-indicator` (`:522`) · `#latest-check { max-height: 30vh; overflow-y: auto }` (`:1114-1116`) · `#stream-banner` (`:682-696`) · `#doc-panel.collapsed` (`:477-490`) · `.annotation-answer summary`'s existing four declarations.

### Zero-new-token discipline (Hard Rule 8)
**Source:** token fence `:6`…`:343`; `--color-surface` already consumed at `:474`.
Every value the new rules use is either an already-consumed token (`var(--color-surface)`) or an already-established **dimension** literal family — `min-height: 160px` (`:792`) / `200px` (`:783`) / `52px`, `min-width: 96px`, `height: 36px` (`:513`), `width/height: 12px` (`:945-946`). The `24px` of L-6 belongs to that family (UI-SPEC §Spacing Scale explicit declaration). No `--space-*` coupling for `24px` (S-3).

### Runtime verification (Hard Rule 7) — applies to every `style.css` plan
**Source:** UI-SPEC §契约校验命令.
`grep -c 'var(--'` proves nothing about rendering. Every plan touching `style.css` must carry at least one runtime judgement: three-width document-level `scrollWidth`, scroller DOM census, or interactive-element `getBoundingClientRect()`.

### Pre-existing gates that must still pass unchanged
```bash
bash scripts/check-01-token-conformance.sh   # bare #hex outside fence == 0
python3 scripts/check-02-contrast.py         # 47 pairs AA (zero color changes ⇒ byte-identical)
bash scripts/check-03-hidden-uniqueness.sh   # ^\.hidden { count == 1
bash scripts/check-04-important-count.sh     # !important declaration lines == 1
```
Note the arithmetic trap at `:597` in the UI-SPEC: `grep -c '!important'` returns 3 because two hits are comment prose.

---

## No Analog Found

| File / Construct | Role | Data Flow | Reason |
|---|---|---|---|
| `frontend/style.css` `@media (max-width: 1023px)` guard (L-2) | config | transform | No `@media` block exists anywhere in the file (grep: 0 hits). Conditional deliverable — written only if the 768–1023px measurement shows breakage. Planner should treat UI-SPEC §L-2's verbatim comment header + locked body form as the substitute pattern. |
| `frontend/style.css` `position: sticky` (L-1) | config | transform | No sticky element exists in the file (grep: 0 hits). Substitute precedent: the specificity-proof comment shape at `:1198-1217`. |
| `page.set_viewport_size(...)` in `check-05-ui-uat.py` | test | request-response | The harness sets viewport once at context creation (`:1617`) and never resizes. Item 8's three-width assertion is the first viewport mutation — must restore 1440×900 before returning. |

---

## Metadata

**Analog search scope:** `frontend/` (style.css, index.html, app.js), `scripts/` (check-05-ui-uat.py, check-01…04, ui-states/), `.planning/phases/idi-06-layout-robustness/`.
**Files scanned:** 6 read in full or in targeted ranges; all named analogs verified git-tracked via `git ls-files`.
**Line numbers:** taken from disk HEAD (`frontend/style.css` 1265 lines, `scripts/check-05-ui-uat.py` 1672 lines). Where 06-CONTEXT.md's line refs drifted from disk, the disk value is used and noted (e.g. `.panel-header` is at `:509-518`, not `:529-537`; `#chat-messages` at `:790-798`, not `:791-799`).
**Pattern extraction date:** 2026-09-22
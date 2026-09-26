# Phase 8: 可访问性语义与键盘 - Pattern Map

**Mapped:** 2026-09-24
**Files analyzed:** 2 modified (`frontend/index.html` / `frontend/app.js`) + 6 gate scripts asserted-but-unmodified
**Analogs found:** 2 / 2 modified files have in-file analogs (10 / 11 code shapes matched)

> **This phase has no RESEARCH.md by design (research disabled in config).** Inputs were
> `08-CONTEXT.md` (D-01…D-26, all LOCKED) + `idi-08-UI-SPEC.md` (approved, 0 BLOCKER / 2 FLAG).
>
> **Read this before using the tables.** There is no framework, no build step, no component
> library. The only two files that change are `frontend/app.js` (1658 lines) and
> `frontend/index.html` (227 lines). `frontend/style.css` gets **zero** changes (D-01).
> The valuable analog for nearly every new code shape is therefore **inside `app.js` itself** —
> that file has strong internal conventions and new code must match them, not invent new ones.
> This document is organized as: file-level classification → per-code-shape analog assignments
> (with verbatim excerpts) → shared cross-cutting patterns → gate-script assertion shapes the
> plan must reuse verbatim rather than reinvent.

---

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `frontend/index.html` | markup / static DOM | declarative attributes | itself (the five `.overlay` divs + `#round-doc` / `#draft-content` pair) | exact (same file, same element family) |
| `frontend/app.js` | frontend controller (single monolithic module, 57 top-level functions) | event-driven + request-response + DOM mutation | itself (its own established idioms) | exact (same file) |
| `frontend/style.css` | — | — | **not touched (D-01)** | n/a |
| `scripts/check-05-ui-uat.py` | gate / Playwright harness | browser-driven assertions | **not touched (D-21)**; asserted against | n/a |
| `scripts/check-01…04` | invariant guards | static text assertions | **not touched**; asserted against | n/a |
| `scripts/probe-07-focus-composite.py` | one-shot probe (not a gate) | browser-driven counterfactual | **not touched (D-04)**; re-run obligation | n/a |

### Code-shape classification (the unit that actually matters here)

| # | Code shape | File /落点 | Role | Data Flow |
|---|---|---|---|---|
| H-1 | `tabindex="0"` on `#round-doc` | `index.html:139` | markup attribute | declarative |
| H-2 | 2 new ids on the modal `<h3>`s | `index.html:172` / `:186` | markup attribute | declarative |
| H-3 | `role` / `aria-modal` / `aria-labelledby` on 2 `.overlay` | `index.html:170` / `:184` | markup attribute | declarative |
| J-1 | new top-level handle `appEl` | `app.js` after `:83` | module init | one-shot bind |
| J-2 | Shift-keyup submit listener | `app.js` inside `initSelectionMenu()` after `:1350` | event listener | event-driven |
| J-3 | Escape single-point dispatcher | `app.js` after `:1423` | event listener (document-level) | event-driven |
| J-4 | focus hand-back inside `hideSelectionMenu()` | `app.js:1296-1299` | DOM/focus management | event-driven |
| J-5 | `syncBackgroundInert()` derived single-point fn | `app.js` new | state derivation | transform (state → attribute) |
| J-6 | 5 `syncBackgroundInert()` call sites | `app.js:487/492/640/799` + J-3 | wiring | one-shot |
| J-7 | `#tier-modal` open: focus + inert | `app.js:638-641` | DOM/focus management | event-driven |
| J-8 | `app.js:1121` copy fix (`左侧`→`右侧`) | `app.js:1121` | string literal | n/a |
| J-9 | one-time-bind guard idiom | `app.js:1343-1346` | module init | one-shot bind |

---

## Pattern Assignments

### H-1 — `#round-doc` gets `tabindex="0"` (markup attribute)

**Analog:** `frontend/index.html:139` (itself) + the deliberate non-analog `frontend/index.html:113`

**Current shape** (L139 — verbatim, no attribute today):
```html
          <div id="round-doc" class="markdown-body"><!-- 当前轮文档 markdown 渲染区 --></div>
```

**Target:** `<div id="round-doc" class="markdown-body" tabindex="0">` — add the attribute,
change nothing else. Existing attribute order in this file is `id` → `class` → (new attribute).

**The deliberate non-analog** (L113 — same `.markdown-body` class, **must NOT get `tabindex`**):
```html
          <div id="draft-content" class="markdown-body"><!-- markdown 渲染区 --></div>
```
Reason to record in the plan (D-20): `handleSelectionTrigger`'s first substantive guard is
`if (currentState !== 'phase3') return` (`app.js:1327`) ⇒ phases 1-2 have no annotation feature
at all, so a Tab stop on `#draft-content` would be dead code — unverifiable at runtime and a
violation of this project's "don't declare what nothing consumes" discipline. **A reader who
does not see this reason will file it as an omission and add it.**

**The reason this one attribute is the whole delivery (K-1.1):** the ring rule already exists and
already enumerates `[tabindex]` — see Shared Patterns § Focus ring.

---

### H-2 — two new ids on the modal `<h3>`s

**Analog:** `frontend/index.html:184` + `:174` (the kebab-case id naming convention on sibling
elements inside the very same `.overlay-card`)

**Current shapes** (verbatim):
```html
  <!-- confirmation-modal card, L172 -->
      <h3>授权确认</h3>
  <!-- tier-modal card, L186 -->
      <h3>选择自检档位</h3>
```

**Naming convention to match** (from the same card bodies and the same file):
```html
      <input type="text" id="confirm-word-input" placeholder="请输入确认词:确认授权" autocomplete="off">
      <div id="tier-modal" class="overlay hidden">
        <button id="btn-tier-loose">宽松<span class="tier-desc">…</span></button>
```
⇒ kebab-case, `<concept>-<qualifier>`. The adjudicated names (UI-SPEC §属性级规格, Claude's
Discretion under D-15) are `confirmation-modal-title` / `tier-modal-title`, measured to have
zero collision across `index.html` / `app.js` / `style.css`.

**Hard rule 5 note the plan must carry:** renaming or deleting an existing id silently kills
every handler beneath it at parse time (recorded failure mode G-idi01-8); **adding** ids is safe.
`index.html` currently has exactly 80 ids — this phase takes it to 82.

---

### H-3 — `role` / `aria-modal` / `aria-labelledby` on two `.overlay` divs

**Analog:** the five `.overlay` divs themselves — all five share one attribute shape today

**Current shapes** (verbatim; note all five are byte-identical in shape):
```html
  <div id="permission-modal" class="overlay hidden">       <!-- L158 -->
  <div id="confirmation-modal" class="overlay hidden">     <!-- L170 -->
  <div id="tier-modal" class="overlay hidden">             <!-- L184 -->
  <div id="mission-complete-modal" class="overlay hidden"> <!-- L196 -->
  <div id="cli-check-overlay" class="overlay hidden">      <!-- L213 -->
```

**Target** (L170 / L184 only — the other three are locked out by D-11):
```html
  <div id="confirmation-modal" class="overlay hidden" role="dialog" aria-modal="true" aria-labelledby="confirmation-modal-title">
  <div id="tier-modal" class="overlay hidden" role="dialog" aria-modal="true" aria-labelledby="tier-modal-title">
```

**Adjudicated landing surface = `.overlay`, not `.overlay-card`** (UI-SPEC M-1.2). The reason the
plan must state: `.overlay` **is** the node `classList.toggle('hidden')` acts on, so
"declaration matches implementation" (SC3) is structurally checkable rather than two things kept
in sync by bookkeeping; `.overlay-card` has no id and is shared by all five modals.

**Structural boundary that makes `inert` cheap (D-14, verified):** `#app` opens at `index.html:10`
and closes at `:155`. All five `.overlay` divs and `#selection-menu` are **siblings** of `#app`,
so mounting `inert` on `#app` can only affect the background. Excerpt of the boundary:
```html
    </aside>
  </div>                                  <!-- L155: #app closes here -->

  <!-- 权限确认弹窗(AI-04:confirm 处置征求用户) -->
  <div id="permission-modal" class="overlay hidden">   <!-- L158: sibling -->
```

---

### J-1 — new top-level handle `const appEl = document.getElementById('app')`

**Analog:** `frontend/app.js:81-83` — the last handle block in the file

**Imports/handles pattern** (L81-83, verbatim):
```js
// 文档面板句柄(260918-qrq:面板可折叠)
const docPanel = document.getElementById('doc-panel');
const docPanelHeader = document.getElementById('doc-panel-header');
```

The file's convention: handles are grouped under a Chinese comment naming the feature that
needs them, all as top-level `const`, all between L4 and L83. The new handle goes **after L83**
with its own comment naming D-14 as the consumer. `app.js:4-75` holds ~70 of these — **add,
never rename or delete** (hard rule 5 / G-idi01-8).

---

### J-2 — Shift-keyup submit listener (inside `initSelectionMenu()`)

**Analog:** `frontend/app.js:1353-1358` — the two closers already bound inside the same function

**Existing event-delegation pattern** (L1352-1358, verbatim):
```js
  // 点文档其他位置/滚动 → 菜单消失(菜单自身点击不冒泡关闭)
  document.addEventListener('mousedown', (e) => {
    if (selectionMenu.classList.contains('hidden')) return;
    if (selectionMenu.contains(e.target)) return;
    hideSelectionMenu();
  });
  window.addEventListener('scroll', hideSelectionMenu, true);
```
This is **the** shape to copy: guard-first early-returns reading `classList.contains('hidden')`,
arrow function, no named handler. The new listener is inserted immediately after L1350
(`roundDoc.addEventListener('keyup', handleSelectionTrigger);`) and matches this shape exactly.
Note the third binding variant (`window.addEventListener('scroll', hideSelectionMenu, true)`)
shows the file passes named functions directly when there is no guard — the new listener has
guards, so it takes the inline-arrow form.

**The guard chain the listener must use** (D-06, three conjunctive predicates):
`e.key === 'Shift'` ∧ menu not hidden ∧ selection non-collapsed. Excerpt from the same file
showing the exact `window.getSelection()` predicate idiom to reuse (L1329-1330):
```js
  const selection = window.getSelection();
  if (!selection || selection.isCollapsed || !String(selection.toString()).trim()) {
```

**Hard fence the plan must write down (D-06 / Do-Not-Touch):** `handleSelectionTrigger`
(`app.js:1323-1340`) stays **byte-identical**. Its existing decision is recorded at L1321-1322:
```js
// 划词触发(D-P2-2 / D-02):mouseup 与 keyup(键盘 Shift+方向键划选)共用同一份守卫。
// 不对 keyup 做按键白名单——「折叠/空白选区即关闭菜单」已让非选择类按键成为安全 no-op。
```
That comment is a record of an existing decision; **the new listener departs from it, it does not
overturn it.** Without the fence comment, a later reader deletes the new listener as a violation.

**The mechanism fact the plan must register (this is the phase's most important one, §K-2.1):**
implementing ROADMAP's literal "the keyup branch moves focus into the menu's first button" yields
a **false green** — `roundDoc.addEventListener('keyup', handleSelectionTrigger)` fires on *every*
keyup, so Shift+→ selecting one character would move focus to `#btn-annotate`, the next Shift+→
would target the menu button instead of `roundDoc`, and the keyboard user could **never select
more than one character** — while A11Y-03's acceptance item ("Shift+arrow → menu appears → focus
already in menu") **passes anyway**, because it tests state, not usability.

---

### J-3 — Escape single-point dispatcher (new block after `initSelectionMenu()`)

**Analog (binding shape):** `frontend/app.js:1353-1358` (document-level listener, guard-first)
**Analog (placement shape):** `frontend/app.js:524` / `:807-808` — top-level column-0 bindings

**Existing top-level binding convention** (verbatim, L807-808):
```js
tierLooseBtn.addEventListener('click', () => chooseTier('宽松'));
tierStrictBtn.addEventListener('click', () => chooseTier('严格'));
```
All 24 top-level bindings sit at column 0 with a `//` comment above naming the feature. The
dispatcher is a **new section** inserted after `initSelectionMenu()`'s closing brace at L1423
(next existing code is `refreshPendingCount` at L1425) — bound at top level, so it is one-shot
and decoupled from the menu's init path (UI-SPEC M-2.1).

**The three `classList.contains('hidden')` probes it needs** — this idiom is already used at
L1354, and `showSelectionMenu()` shows the inverse (L1305):
```js
    if (selectionMenu.classList.contains('hidden')) return;   // L1354
    selectionMenu.classList.remove('hidden');                  // L1305
```

**The functions it dispatches to (all pre-existing, zero new functions for the closing half):**
```js
function closeConfirmModal() {                 // L491-493, verbatim
  confirmationModal.classList.add('hidden');
}
```
`hideSelectionMenu()` (L1296) and the tier branch's `tierModal.classList.add('hidden')` (L799)
are the other two. The dispatcher adds only: the tier branch's `tierModalShown = false`
(D-13), `syncBackgroundInert()` calls, and the two `F1-d` focus hand-backs.

**The two return targets, verified present:** `#btn-authorize` at `index.html:143`,
`#btn-continue-check` at `index.html:49`. Handles already exist: `authorizeBtn` (`app.js:58`),
`continueCheckBtn` (`app.js:76`).

**Adjudicated shape (Claude's Discretion, resolved):** one `document` listener + explicit
priority table (menu → confirmation → tier), **not** per-modal listeners. Recorded reasons: the
menu already lives in `initSelectionMenu`, so the dispatcher adjacent to it makes "Escape's whole
semantics readable in one screen"; per-modal listeners would turn "who responds first" into a
**source-order fact** (hard rule 3's same risk class); a single point is enumerable.

**Explicit non-response the plan must register:** the other three modals
(`#permission-modal` / `#mission-complete-modal` / `#cli-check-overlay`) **deliberately do not
respond to Escape** — scope locked to D-11's two objects. This is deliberate, not an omission.

---

### J-4 — focus hand-back inside `hideSelectionMenu()`

**Analog:** `frontend/app.js:1296-1299` (the function itself — four call sites, one choke point)

**Current body** (verbatim):
```js
// 隐藏菜单并清空选区快照
function hideSelectionMenu() {
  selectionMenu.classList.add('hidden');
  menuSelection = null;
}
```

**Its four call sites** (verified) — this is why the change goes here and nowhere else
(scattering it across four sites would necessarily miss one):
- `app.js:1356` — `document` mousedown closer
- `app.js:1358` — `window` scroll capture closer (passed as the handler directly)
- `app.js:1331` / `:1335` — `handleSelectionTrigger`'s two guards
- `app.js:1363` / `:1393` — the two menu-item click handlers

**The predicate has no precedent in this file** (it is the phase's one genuinely new idiom):
`selectionMenu.contains(document.activeElement)`. The nearest existing "contains" usage is
`selectionInRoundDoc()` at L1292:
```js
  return !!(el && roundDoc.contains(el));
```

**Two hard constraints the plan must carry (UI-SPEC K-2.4):**
1. The predicate must be taken **before** `classList.add('hidden')` — once the focused element is
   `display:none`, `document.activeElement` immediately falls back to `body` and the test is
   permanently false.
2. **Must not clear `window.getSelection()`** — doing so destroys the "after Escape, keep
   extending with Shift+→" path (D-08).

---

### J-5 — `syncBackgroundInert()` — derived single point, not paired bookkeeping

**Analog (derivation-from-state idiom):** `frontend/app.js:1174-1184` `updateFrozenPresentation(isCurrent)`

**Existing derived single-point function** (verbatim):
```js
// 冻结轮三面呈现(D-P2-21):容器灰化 + 计数徽标隐藏 + 处理按钮禁用
function updateFrozenPresentation(isCurrent) {
  if (isCurrent) {
    roundDoc.classList.remove('round-frozen');
    pendingCount.style.display = '';
    processRoundBtn.disabled = processInFlight;
  } else {
    roundDoc.classList.add('round-frozen');
    pendingCount.style.display = 'none'; // 历史轮不显示本轮计数(D-P2-21)
    processRoundBtn.disabled = true;
  }
}
```
This is the file's established shape for "one function reads current state and derives N
presentation effects, called from every mutation site." The `inert` sync is the same shape:
read the two modals' `.hidden` status, derive one attribute. **The reason recorded in the plan
(UI-SPEC M-1.4):** paired add/remove bookkeeping leaks on any early-return path (the same class
of defect as this project's recurring derived-counter bugs); a derivation cannot desynchronize
and is inherently idempotent.

**`inert` has zero occurrences today** in both `index.html` and `app.js` (measured 0 / 0), so
there is no in-file `setAttribute`/`removeAttribute` precedent — the nearest attribute mutation
idiom is the `style.display` / `classList` writes above.

**Hard rule 12 the plan must carry:** `inert` and `.hidden` are **orthogonal mechanisms** —
`.hidden` governs visibility, `inert` governs background inertness. Do not substitute one for
the other. `inert` mounts on `#app` only, never on a modal or on `#selection-menu`.

---

### J-6 — the 5 `syncBackgroundInert()` call sites

**Analog:** the existing "one derived function, called from every mutation site" pattern — same
as `updateFrozenPresentation` (see J-5), and as `applySessionGates()` invoked from the session
refresh paths.

**Verbatim landing points** (all inside existing function bodies; **no new functions**):

| Site | Line | Existing code to insert after |
|---|---|---|
| `openConfirmModal()` | after `:487` | `confirmationModal.classList.remove('hidden');` |
| `closeConfirmModal()` | after `:492` | `confirmationModal.classList.add('hidden');` |
| tier open branch | after `:640` | `tierModal.classList.remove('hidden');` |
| `chooseTier()` success | after `:799` | `tierModal.classList.add('hidden');` |
| Escape dispatcher tier branch | J-3 | after `tierModal.classList.add('hidden');` |

**The tier open branch in context** (L638-641, verbatim — this is also the D-13 dead-state site):
```js
    if (!selfcheck.tier && !tierModalShown) {
      tierModalShown = true;
      tierModal.classList.remove('hidden');
    }
```
**D-13's dead state, verbatim mechanism:** the flag is set to `true` the instant the modal opens,
but only `chooseTier()` success (`:799`) hides it. Close it without choosing ⇒ `selfcheck.tier`
is still empty while `tierModalShown` is already `true` ⇒ **it never re-appears** and the user
lands in "tier undecided and the entry point is gone." Resetting the flag on Escape lets the next
self-check event (`refreshChecksAfterStream`) re-open it. **Do not reset `selfcheck.tier`; do not
POST anything.**

---

### J-7 — `#tier-modal` focus-on-open

**Analog:** `frontend/app.js:483-489` `openConfirmModal()` — the **only** `.focus()` call in the
entire 1658-line file (verified: `grep -n '\.focus()' frontend/app.js` returns exactly one hit)

**Verbatim analog:**
```js
function openConfirmModal() {
  confirmWordInput.value = '';
  confirmAuthorizeBtn.disabled = true; // 初始 disabled(未输入即不可放行)
  confirmError.classList.add('hidden');
  confirmationModal.classList.remove('hidden');
  confirmWordInput.focus();          // ← L488, the file's sole .focus() call
}
```
**Order to copy exactly (UI-SPEC M-1.5, locked):** `classList.remove('hidden')` →
`syncBackgroundInert()` → `.focus()`. Target for tier is `#btn-tier-loose` (first operable
control), mirroring `confirmWordInput.focus()` being the first operable control in its modal.

**Why the plan must state this is the substantive fix (D-11):** `#tier-modal`'s trap is not
"no Escape" but "focus isn't inside it"; once `inert` lands the background is unfocusable, so
focus left outside the modal falls to `<body>` and the next Tab **skips the whole background** —
worse than not inerting at all.

**Measured-open item the plan must schedule (D-16):** verify at runtime where focus lands at the
instant `inert` takes effect, and decide from that whether an explicit `.focus()` is needed.
Do not write this as "expected to work."

---

### J-8 — `app.js:1121` copy fix

**Analog:** the surrounding empty-state rendering in the same function (L1118-1124)

**Verbatim current state:**
```js
  if (!items.length) {
    const empty = document.createElement('p');
    empty.className = 'hint';
    empty.textContent = '本轮暂无批注——在左侧文档划词即可批注。';
    annotationList.appendChild(empty);
    if (!isCurrentRound) empty.textContent = '该轮暂无批注。';
    return;
  }
```
Change `在左侧文档` → `在右侧文档`, one word (S8-1, user-adjudicated 2026-09-23). Note the
`textContent`-only rule that governs this whole function (`showInlineError`'s
`textContent`-only rule is an XSS mitigation, T-260916-01, **not** a style choice) — the fix
must not introduce `innerHTML`.

---

### J-9 — one-time-bind guard idiom

**Analog:** `frontend/app.js:1342-1346` — the file's **only** instance

**Verbatim:**
```js
// 一次性绑定入口(menu 单例,handler 内部动态读当前显示轮判定冻结)
let selectionMenuBound = false;
function initSelectionMenu() {
  if (selectionMenuBound) return;
  selectionMenuBound = true;
```
`initSelectionMenu()` is called from exactly one place — `app.js:1019`, at the tail of the
rounds refresh path — and may run many times per session, hence the guard. The new Shift
listener goes **inside** this function (so it inherits the guard for free). The Escape dispatcher
does **not** need it: it is bound at top level once at parse time.

---

## Shared Patterns

### Focus ring — inherited, zero CSS (D-01)
**Source:** `frontend/style.css:1508-1517` (verbatim):
```css
button:focus-visible,
input:focus-visible,
select:focus-visible,
textarea:focus-visible,
a[href]:focus-visible,
summary:focus-visible,
[tabindex]:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}
```
**Apply to:** `#round-doc` (via H-1) and the two menu buttons. Ring color is
`--color-focus: #1f63bd` (`style.css:259`).

**This is the phase's central lever:** dropping `tabindex="0"` makes the ring take effect with
**zero new CSS** — Phase 7 D-05 deliberately wrote `[tabindex]` into this enumeration so this
phase could deliver with no CSS. **Hard rule 10 / Do-Not-Touch:** adding any `:focus` /
`:focus-visible` rule, or any `#round-doc`-specific focus rule, is forbidden — it would fork
"what the rule covers" from "what the gate checks" (the cause of G-idi-05-1).

**The geometric evidence the plan must carry (D-01, overturns PITFALLS 5 failure mode 4):**
`#round-doc`'s parent is `#doc-panel-body { padding: var(--space-8) var(--space-10); }`
(`style.css:657` = `32px 40px`). The ring is drawn 2–4px **outside** the border box, landing
inside that 40px horizontal padding ⇒ **not clipped**; the box is thousands of pixels tall ⇒ what
the viewport shows is **two full-height vertical lines**, not "only the top and bottom edges."

**Pitfall 6's gate is satisfied by construction (K-1.6), and the plan must explain why:**
`tabindex` moves 0 → 1 while `:focus-visible` stays 9 → 9. That looks like "independent movement"
but is not — Phase 7 already landed the ring's carrier surface. **The mechanical evidence is not
the count, it is the runtime reading:** `check-05 --item 10` reading `2px` /
`rgb(31, 99, 189)` at the moment `#round-doc` becomes `document.activeElement`. Counts prove the
rule exists; only the runtime reading proves it landed on the new Tab stop.

**A-9, must be registered:** the fence comment at `style.css:1499-1503` promising "Phase 8 lands
`#round-doc`'s own inset handling together with the `tabindex`" **no longer holds**. The comment
stays unchanged as a record (zero CSS changes); downstream must not read it as this phase's
contract.

### Focus invariant F1 — the single predicate for all focus behaviour
**Source:** `idi-08-UI-SPEC.md` §焦点契约 (contract, not code)

> **F1: focus never rests on an invisible element, and never falls back to `<body>` because of a
> hide.**

Four landing points, three of which are the same one-function mechanism:

| # | Landing point | Mechanism | Decision |
|---|---|---|---|
| F1-a | menu hidden while focus is inside it ⇒ hand back to `#round-doc` | `hideSelectionMenu()` **single point** | D-08 |
| F1-b | after a menu item executes ⇒ hand back to `#round-doc` | same (both items call `hideSelectionMenu()` first) | D-07 |
| F1-c | Escape closes menu ⇒ hand back to `#round-doc` | same | D-08 |
| F1-d | after a modal closes ⇒ hand back to the trigger (`#btn-authorize` / `#btn-continue-check`) | inside the Escape branch only | **A-8, user-adopted** |

**Two explicit non-coverage cases (registered, not omissions):** ① the success path does **not**
hand back — after `#confirmation-modal`'s "放行" succeeds the whole view is about to switch
(`refreshRoundsAfterStream()`), so pinning focus to `#btn-authorize` is wrong; hand-back lives in
the Escape branch, **not** inside `closeConfirmModal()`; ② if the target is unfocusable, degrade
silently (Chrome's `.focus()` on a disabled button is a no-op) — **add no fallback logic.**

### In-file comment conventions (new code must match)
**Source:** the whole of `frontend/app.js`

- **Section banners** are a 75-column triple-line block; verified 16 of them (L108, 139, 255,
  295, 427, 477, 956, 1217, 1245, 1260, 1438, 1495, 1525, 1557, 1572, 1635):
```js
// ---------------------------------------------------------------------------
// G3 确认词模态(FLOW-05 / D-P3-3):strip 后全等「确认授权」才放行;默认拒绝
// ---------------------------------------------------------------------------
```
- **All comments are Chinese** (stated at `app.js:2`: `注释一律中文,遵守简单优先`), and they
  state **why**, not what. Decision IDs are cited inline (`D-P2-21`, `D-P3-25`, `G-idi01-7`,
  `T-260916-01`) — the new code should cite `D-05` / `D-06` / `D-08` / `D-13` / `D-14` / `D-16`
  the same way.
- **Append, never reorder** (hard rule 3): new code is appended inside existing function bodies
  or after existing logic blocks; **no existing statement may be moved.**

### `.hidden` is a mechanism, not styling
**Source:** `frontend/style.css` (`grep -c '^\.hidden {'` == 1, measured)

`display: none !important` must not be tokenized, moved, or weakened. All modal/menu visibility
in this phase goes through `classList.add/remove/contains('hidden')` — see the verified toggle
sites at `app.js:487, 492, 640, 799, 1297, 1305, 1354`.

---

## Gate Scripts — reuse these assertion shapes verbatim (do not invent new commands)

These six scripts are **not modified this phase**. The plan must assert against them using the
already-proven command and predicate shapes below, so the phase's `<verify>` steps are copies of
working gates rather than newly invented ones.

### `scripts/check-05-ui-uat.py` — item 10 focus-ring element census
**Invocation (proven, from the file's own docstring at L39):**
```bash
.venv/bin/python scripts/check-05-ui-uat.py --item 10
```

**The enumeration constant** (`check-05-ui-uat.py:1748`, verbatim):
```python
FOCUSABLE_SELECTOR = "button, input, select, textarea, a[href], summary, [tabindex]"
```
It is injected into two JS census scripts via `_focusable_census_js()` (L1751-1759), which uses
`json.dumps` rather than bare quoting.

**The adjudication set** (`_idi07_focus_census_assert`, L2830-2831 and L2847-2854, verbatim):
```python
    order, samples = _idi07_tab_drive(page, len(data) + 8)
    judged = [r for r in data if r["visible"] and r["focusable"]]
```
```python
    bad = [
        r for r in judged
        if r["label"] not in samples
        or (
            samples[r["label"]]["outlineWidth"],
            norm(samples[r["label"]]["outlineColor"]),
        ) != (FOCUS_RING_WIDTH_CSS, norm(focus_color))
    ]
```
The per-element `focusable` predicate (`_IDI07_FOCUS_CENSUS_JS`, L1988, verbatim):
```js
      focusable: !el.matches(':disabled') && el.getAttribute('tabindex') !== '-1',
```

**The two registered changes (D-03) the plan must log, not "fix":**
1. The adjudication set gains one member (`#round-doc`) in the **p3 / checking / archive** samples
   only — in p1 / p12 it sits inside a `.hidden` subview, so `visible` filters it out.
2. `_idi07_tab_drive(page, len(data) + 8)`'s limit is **data-driven**: the set grows by 1 ⇒ the
   limit grows by 1, while the Tab order also gains exactly one stop (+1) — the two cancel.
   **No gate change needed, but the arithmetic must be logged.**
3. **If the item goes red in some sample, first judge whether it is a real defect or a census-set
   change — do not edit the gate.** (Also: the two sample drivers at L3718 and L3743 call
   `_idi07_focus_census_assert` for p1, then checking + p3.)

**Also required to stay green:** `--item 1` (five-state `.hidden` layering) and `--item 4`
(SC5 token wiring + `#state-badge` z-index). Neither is touched by this phase.

### `scripts/probe-07-focus-composite.py` — D-04 re-run obligation
**Invocation:** `.venv/bin/python scripts/probe-07-focus-composite.py`

**Why (verbatim from its own docstring, L10-14):** the five state samples have **0** `a[href]`
inside `#round-doc` ⇒ the `.archive-mode` 0.75-composite **runtime** ring assertion has no
service object today; it is carried by the resident arithmetic gate (`check-02`'s
`--color-focus ON --color-surface NON-TEXT@0.75`) plus this one-shot probe. It is **not** in the
guard contract (same standing as `scripts/probe-05-resolve-color.py`).

**The counter-assertion the plan must require (L177-191, verbatim intent):** the probe asserts
its own mutation actually happened — `before == 0` and `after == 1`. **The re-run must log these
two counts verbatim**, otherwise there is no way to distinguish "the probe is working" from "the
probe is silently spinning." Its Tab drive is data-driven (limit 40, stops on hit) so the new Tab
stop is absorbed naturally.

### `scripts/check-01…04` — four invariant guards (must stay PASS)
**Proven commands (verbatim, from UI-SPEC §契约校验命令):**
```bash
bash scripts/check-01-token-conformance.sh   # PASS: 围栏外裸 hex = 0 且 tier-1 primitive 引用 = 0
python3 scripts/check-02-contrast.py         # PASS: 0 failures(47 对 + ORDER 0.363)
bash scripts/check-03-hidden-uniqueness.sh   # PASS: ^[[:space:]]*\.hidden[[:space:]]*\{ 计数 == 1
bash scripts/check-04-important-count.sh     # PASS: grep -o '!important;' 计数 == 1
```
Each guard's own failure-mode discipline is worth copying into the plan's reasoning:
- `check-01` asserts the fence **pair** exists before trusting it (L17-20), and counts
  **occurrences** via `grep -o | wc -l`, not lines.
- `check-03` matches the selector **anywhere on the line** (L11) so a future indented duplicate
  inside an `@media` is still caught.
- `check-04` counts `!important;` **declarations**, not `!important` hits — a line-based `grep -c`
  would report 1 and pass even with two declarations sharing a line.
- `check-02` floors the manifest before trusting `failures == 0` (L146-153: `>= 24` pairs,
  `>= 20` TEXT, `>= 4` NON-TEXT; FAIL message printed at L152) and asserts raw marker count ==
  parsed count (`raw_pairs` L161-167, `raw_orders` L169-174). `NON_TEXT_MIN = 3.0` (L25).

### Static count gates (each written by declaration/occurrence, never by matching line)
```bash
grep -c tabindex frontend/index.html                   # 0 → 1   (and app.js must stay 0)
grep -c ':focus-visible' frontend/style.css            # 9 → 9   (zero CSS change)
grep -c 'role=' frontend/index.html                    # 0 → 2
grep -o 'aria-modal' frontend/index.html | wc -l       # 0 → 2
grep -o 'aria-labelledby' frontend/index.html | wc -l  # 0 → 2
grep -c inert frontend/app.js                          # 0 → >0  (index.html stays 0: attribute is JS-mounted)
```
**Arithmetic trap to carry forward:** `grep -c 'aria-' frontend/index.html` counts **lines**, not
occurrences ⇒ write the gate with `grep -o … | wc -l`. This project has a documented history of
gate-arithmetic errors; every count above was re-measured on HEAD this session and matches the
UI-SPEC's baseline table.

### The two REG-02 gates — plan-level `<verify>` + manual UAT only (D-21 / A-4 / A-5)
```bash
grep -c 'inline-error' frontend/style.css        # == 1
grep -c 'clearInlineError();' frontend/app.js    # >= 9
```
**Measured on HEAD this session: `1` and `9`** (the 9 call sites are L311 / 320 / 461 / 603 /
822 / 1252 / 1461 / 1511 / 1535; `grep -c 'clearInlineError'` returns 10 = 9 calls + the L303
definition). **A-5: `08-CONTEXT.md` D-21's "baseline 6" is wrong — writing 6 produces a gate that
can never fail.** These do **not** go into `check-05-ui-uat.py`: that file is in the
`covered_files` of five live reports, so writing an assertion into it would instantly destroy
D-01's zero-fingerprint-debt property. Registered cost: they are not resident guards, so the next
person to edit `style.css` will not be automatically stopped.

### Baseline gate (run before touching anything)
```bash
cd frontend && node --check app.js                    # OK
.venv/bin/python -m pytest -q -m "not slow"           # 219 passed + 6 skipped / 225 collected
```
**A-6 / D-24:** the criterion is "219 passed + 6 skipped"; 219 is the **pass** count and 225 the
**collection** count — they are not the same thing, and copying "225" creates a false gate. The
project venv is mandatory: the environment's `python3` is miniconda and makes 4 `ai_caller` tests
fail spuriously.

---

## No Analog Found

| Code shape | Role | Data Flow | Reason | Planner should use |
|---|---|---|---|---|
| `syncBackgroundInert()`'s `setAttribute('inert')` / `removeAttribute` | DOM attribute mutation | transform | `inert` appears **0 times** in both `index.html` and `app.js` (measured) — no in-file precedent | UI-SPEC §M-1.4's given implementation shape + `updateFrozenPresentation` (J-5) for the *derivation* structure |
| `selectionMenu.contains(document.activeElement)` | focus predicate | event-driven | No `.contains(document.activeElement)` anywhere in the file; nearest is `roundDoc.contains(el)` at `app.js:1292` | UI-SPEC §K-2.4's given body; take the predicate **before** `classList.add('hidden')` |
| Escape single-point dispatcher with a priority table | event listener | event-driven | No keydown dispatcher exists; the only `document` listener is a single-purpose mousedown closer (`app.js:1353`) | Copy `app.js:1353-1358`'s binding shape; priority order from UI-SPEC §M-2.1 |
| `role` / `aria-modal` / `aria-labelledby` | markup attribute | declarative | `grep -c 'role=' index.html` == 0 and `grep -c 'aria-'` == 0 (measured) — the project has **zero** accessibility attributes today | UI-SPEC §属性级规格 table (the exact literal targets) |

---

## Metadata

**Analog search scope:** `frontend/` (`app.js`, `index.html`, `style.css`), `scripts/`
(`check-01…04`, `check-05-ui-uat.py`, `probe-07-focus-composite.py`), `frontend/vendor/`
**Files read this session:** `08-CONTEXT.md`, `idi-08-UI-SPEC.md`, `frontend/index.html` (full),
`frontend/app.js` (targeted non-overlapping ranges: 1-100, 290-330, 470-570, 618-663, 780-858,
1005-1034, 1100-1149, 1150-1190, 1195-1225, 1280-1424, 1635-1658), `frontend/style.css`
(1500-1525 + targeted greps), `scripts/check-05-ui-uat.py` (30-110, 1740-1810, 1930-2000,
2755-2874, 3700-3775), `scripts/check-02-contrast.py` (136-200), `scripts/check-01/03/04`
(full), `scripts/probe-07-focus-composite.py` (full)
**Tracked-source gate (#3645):** every analog path named above was verified with
`git ls-files -- <path>` → all TRACKED. `.gsd/` exists but is gitignored and contains only
`dispatch-isolation-sentinel.json` — **no mirror copies of `frontend/` or `scripts/`**, so no
mirror path is emitted anywhere in this document.
**Baselines re-measured on HEAD this session (2026-09-24):** `inline-error`(css)=1 ·
`clearInlineError();`(js)=9 · `tabindex`(html/js)=0/0 · `:focus-visible`(css)=9 · `role=`(html)=0 ·
`aria-`(html)=0 · `inert`(js)=0 · `.focus()`(js)=1 hit at L488 · `index.html` ids=80 ·
`vendor/`= exactly one file (`marked.min.js`) · all four invariant guards + `check-02` PASS
**Pattern extraction date:** 2026-09-24

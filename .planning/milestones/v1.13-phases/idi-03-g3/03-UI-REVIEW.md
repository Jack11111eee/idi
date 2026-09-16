# Phase 3 — UI Review

**Audited:** 2026-09-16
**Baseline:** Abstract 6-pillar standards (NO UI-SPEC.md exists — see Scope Note)
**Screenshots:** NOT captured — dev server detected and live at `http://localhost:8765` (HTTP 200), but headless browser rendering is blocked in this environment (Chrome, Chrome-for-Testing, and `chrome-headless-shell` all failed; the app's persistent `/api/events` SSE stream also prevents the capture handler from terminating). Audit is code-only: CSS/HTML/JS source analysis plus computed contrast arithmetic.

---

## Scope Note

This project's entire frontend is three shared files spanning all three phases (`frontend/index.html` 218 lines, `frontend/style.css` 622 lines, `frontend/app.js` 1595 lines). There is no phase-specific frontend, so this review covers the whole frontend surface. The phase-3 artifacts were used as intent baseline only.

**Finding: no UI-SPEC.md exists anywhere in the project.** The only `UI-SPEC.md` on disk is the GSD template at `.claude/gsd-core/templates/UI-SPEC.md` — not a project artifact. The design contract therefore exists only as `DESIGN.md` §4 prose, which specifies layout regions (§4.1), selection interaction (§4.2), work-panel semantics (§4.3), and the three gate interactions (§4.4). It specifies **no** spacing scale, type scale, color tokens, component library, breakpoint set, or copy contract. Every pillar below is therefore scored against abstract standards, and there is no declared contract to hold the implementation to. For a tool whose stated value is "unambiguous alignment," shipping 2435 lines of UI with zero design contract is itself a structural gap.

---

## Pillar Scores

| Pillar | Score | Key Finding |
|--------|-------|-------------|
| 1. Copywriting | 3/4 | Domain-specific Chinese copy throughout, zero generic labels — but `#draft-empty` renders its "尚无草稿" message on top of an existing draft, and the stale placeholder `#rounds-hint` is permanently visible in phase 3 |
| 2. Visuals | 2/4 | The largest, boldest text on screen is an unstyled UA-default `<h1>文档区</h1>` (~32px container label); rendered-document headings fall back to browser defaults; four sidebar panels share one undifferentiated header treatment; emoji used as iconography |
| 3. Color | 2/4 | 32 hardcoded hex literals, **zero** CSS custom properties; four accent families with no hierarchy (green 12 declarations outnumbers nominal-primary blue 9); green overloaded as generic "positive action" across 6 semantically distinct buttons including the irreversible G3 authorization; four WCAG AA contrast failures |
| 4. Typography | 2/4 | 7 flat sizes (13px used 14×), fractional 12.5px, only 2 weights; markdown headings have **no** font-size rule and fall back to UA defaults (28/21/16.4px) — the primary content's type scale is uncontrolled |
| 5. Spacing | 2/4 | No spacing scale (16 distinct padding values, 8 distinct gap values); `right: 448px` hardcoded to sidebar 420+28; up to 4 nested scroll containers in a 420px column; **zero** responsive rules; 8 distinct border-radii |
| 6. Experience Design | 2/4 | SSE stream has no `onerror`/reconnect — a dropped connection is silent; zero `:focus` styles and no keyboard path to the flagship selection-annotation feature; errors surface in the AI work panel instead of inline; archive read-only contract violated in the presentation layer |

**Overall: 13/24**

---

## Top 3 Priority Fixes

1. **Five `classList.toggle('hidden')` calls are silent no-ops — there is no global `.hidden` rule and no rule for these five selectors.** `#draft-empty` (`.draft-empty.hidden` undefined), `#rounds-hint`, `#btn-process-round`, `#round-switcher`, `#writing-hint` all receive the `hidden` class from `app.js` but have no matching CSS rule, so they never hide. Concretely: (a) in phase 1-2 with a draft present, the user sees the rendered draft **and** the message "尚无草稿——和 AI 讨论出实质进展后,它会写入 docs/draft.md。" at the same time — directly contradictory information about tool state (`app.js:839-848`); (b) the stale placeholder "已进入轮次阶段(本阶段占位)。" stays pinned above the real round document in every phase-3 screen (`app.js:945`, defeating the explicit intent recorded in `idi-02-03-SUMMARY.md` key-decision "roundsHint 在 phase3 时隐藏"); (c) in `mission_complete` the "处理本轮批注" button is neither hidden nor disabled, so the read-only archive state (§7.4 / D-P3-25: "「处理本轮批注」… 均不可用") is visibly violated and the user can click a control that should not exist. — **User impact:** the tool displays self-contradictory state in its two most-used views, and a core design contract (read-only archive) is broken at the presentation layer. — **Fix:** add a single global `.hidden { display: none !important; }` rule at the top of `style.css` (and delete the 14 per-selector duplicates), or add the five missing selector rules. Then add `processRoundBtn.disabled = true` in `applyArchiveView` (`app.js:764-781`) as defense in depth.

2. **The AI work panel and the sidebar have no error surface, and the SSE stream fails silently.** 17 `try` blocks cover 39 async functions; failures in `enterProject`, `divergenceBtn`, `approveDraftBtn`, `processRoundBtn`, `loadChecksView` are all rendered via `renderEvent()` into `#ai-events` — the bottom-right AI work panel — so a failed "进入" (typed in the top-left form) reports its error far from the control that failed. Worse, `initEventSource()` (`app.js:136-148`) sets only `source.onmessage` with **no** `onerror`/`onopen`/`onclose` handler, so if the stream drops the UI silently stops updating with no indication — and SSE is the sole feedback channel for every long-running operation in this tool. — **User impact:** users cannot tell a failed action from a slow one, and cannot tell a dead event stream from an idle system. — **Fix:** render errors inline adjacent to the initiating control (the `sendMessage` pattern at `app.js:1138` is the correct one — extend it); add `source.onerror` that surfaces a visible "事件流已断开,正在重连" banner and re-instantiates the EventSource.

3. **Establish a design token layer before adding any more UI.** Zero CSS custom properties exist; 32 hex literals and 16 padding values are inlined. Without tokens, the four accent families cannot be rationalized (green currently means "写文件", "认可雏形", "处理本轮批注", "授权撰写总设计文档", "撰写总设计文档", "继续自检", and "继续修复" — seven meanings, one color), and the irreversible Core-Value G3 authorization button is styled identically to a routine "继续自检" button (`style.css:504-511` vs `581-586`). — **User impact:** the single most consequential action in the product (irreversible authorization, the project's Core Value red line) has no visual weight distinguishing it from routine actions. — **Fix:** introduce `:root` custom properties for color/spacing/type/radius, collapse the palette to one primary + one danger + one neutral scale, and give `#btn-authorize` a distinct irreversible-action treatment (solid fill, not the pale `#e9f7ef` tint shared with six other buttons). This is a prerequisite for fixes 1 and 2 being maintainable.

---

## Detailed Findings

### Pillar 1: Copywriting (3/4)

**Strengths (verified, not assumed):**
- Generic-label grep (`Submit|Click Here|>OK<|>Cancel<|>Save<`) returns **zero** matches. Every control has a specific Chinese label.
- Gate copy states preconditions rather than just disabling: `#authorize-hint` enumerates all four mechanical checks (`app.js:399`), `#approve-hint` warns about irreversibility (`app.js:361`), `#writing-hint` explains the tmp-overwrite recovery (`app.js:413`).
- Error copy is specific and state-named: 13 distinct messages, e.g. `授权失败:${...}`, `大白话调用失败:${...}`, `仅当前轮可批注`, `轮次列表拉取失败(稍后操作会重试)。` — no "something went wrong."
- Domain terminology is used correctly and consistently (轮次/批注/雏形/未决清单/档位/使命完成), matching DESIGN.md §10.

**Findings:**

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 1.1 | BLOCKER | `#draft-empty` copy is displayed simultaneously with rendered draft content. The empty-state string is never actually hidden because `.draft-empty.hidden` has no CSS rule. | `app.js:839-848` toggles the class; `style.css` has no `.draft-empty` rule at all |
| 1.2 | WARNING | Stale placeholder copy "已进入轮次阶段(本阶段占位)。" is permanently visible above the real round document in phase 3. | `index.html:60`; `app.js:945` (`roundsHint.classList.add('hidden')`) is a no-op |
| 1.3 | WARNING | Two user-facing text inputs use native `window.prompt` (`写批注(将绑定到划选原文)` at `app.js:1301`, `拒绝原因…` at `app.js:441`), bypassing the five styled `.overlay-card` modals built for exactly this purpose. Browser-native prompt chrome is unstyled, unbranded, and blocks the event loop. | `app.js:441`, `app.js:1301` |
| 1.4 | WARNING | Error copy is delivered into the wrong region. `进入失败:…` renders into `#ai-events` (AI work panel, bottom-right) while the input that caused it sits top-left. Same for divergence, approve, process-round failures. | `app.js:277`, `1453`, `1479`, `1399` |
| 1.5 | WARNING | No empty state for the chat panel or the AI event panel — both render as blank regions on first entry. Only 5 empty states exist in the whole app (`index.html:37`, `app.js:572`, `790`, `1061`, `1063`). | grep `暂无\|尚无\|未找到` |
| 1.6 | INFO | No copy contract exists to audit against (no UI-SPEC). Copy quality is therefore a judgment call rather than a conformance check. | — |

### Pillar 2: Visuals (2/4)

**Findings:**

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 2.1 | WARNING | No visual hierarchy at the page level. `<h1>文档区</h1>` has **no CSS rule**, so it renders at the browser default 2em ≈ 32px bold — the largest and heaviest text on the screen is a generic container label, outranking all actual content. | `index.html:13`; grep for `h1` in `style.css` matches only `.markdown-body h1` (line 220) |
| 2.2 | WARNING | No focal point on the main screen. The doc pane and the 420px sidebar are visually co-equal; within the sidebar four `.panel-header` blocks (`会话流` / `本轮批注流` / `自检报告` / `AI 工作面板`) share one identical treatment (`#f5f5f5` fill, 14px/600 title, same border) with no active/inactive differentiation — panels are shown and hidden by state, but nothing signals which is live. | `style.css:38-52`; `index.html:80-143` |
| 2.3 | WARNING | The tool's primary explanatory text is the least legible element. `.hint` (used for every gate explanation, every precondition, every recovery instruction) is 13px `#999` on `#fafafa` = **2.73:1** contrast. | `style.css:35`; computed |
| 2.4 | WARNING | Emoji used as iconography via CSS `content`: `📌` for annotation quotes (`style.css:415`), `📍` for verdict locations (`style.css:603`). Renders inconsistently across platforms and is not an icon system; there is no iconography anywhere else in the app (no SVG, no icon font). | `style.css:415`, `603` |
| 2.5 | WARNING | Stale chrome in phase 4/5: `#round-switcher` (a `<select>` titled "切换轮次(历史轮只读)") receives `hidden` in `applyWritingView` and `applyPhase5View` but has no CSS rule, so it remains visible in the writing and self-check views. | `app.js:408`, `539`; no `#round-switcher.hidden` rule |
| 2.6 | INFO | 8 distinct border-radii (2/3/4/6/8/9/10/12px) with no scale — the pill-shaped badges (9-12px) and the square-ish controls (4px) are visually coherent but arrived at ad hoc. | grep `border-radius` |

### Pillar 3: Color (2/4)

**Verified usage counts (`style.css`):**

| Color | Declarations | Semantic role assigned |
|-------|--------------|------------------------|
| `#2e8b57` green | 12 | "写文件" event + **6 distinct buttons** + mission-complete modal border |
| `#2c7be5` blue | 9 | "说话" event + user chat bubble + send button + `.primary` + streaming border |
| `#b8860b`/`#8a6508`/`#fdf6ec`/`#e8d9a8`/`#d9c58a`/`#fffdf5`/`#fff3c4` amber | 18 | "执行" event + divergence button + pending badges + verdict cards + brainstorm panel + `<mark>` highlight |
| `#c0392b`/`#fdecea` red | 6 | `.danger` buttons + "错误" event + `#confirm-error` |
| `#6f42c1` purple | 1 | "读文件" event |
| `#555` grey | 1 | "结果" event |
| `#000` black | 1 | "结束" event |
| `#2c5fb8` blue | 1 | `#state-badge` text — a second blue 4% off the primary |

**Findings:**

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 3.1 | BLOCKER | Zero design tokens. 32 hardcoded hex literals, **0** CSS custom properties. No token layer exists to correct any of the below. | grep `^\s*--[a-z-]+\s*:` in `style.css` → no matches |
| 3.2 | BLOCKER | The 60/30/10 distribution is absent and the nominal primary is outranked. Green (12 declarations) is used more than the primary blue (9). There is no dominant accent — four families compete at roughly equal weight against the neutral base. | counts above |
| 3.3 | BLOCKER | Green is overloaded as a generic "positive action" across six semantically unrelated buttons: `#btn-approve-draft` (irreversible G1), `#btn-process-round`, `#btn-authorize` (**irreversible G3, the Core Value red line**), `#btn-start-writing`, `#btn-continue-check`, `#btn-continue-repair`. All share the identical pale treatment (`background: #e9f7ef; border/color: #2e8b57`). The project's most consequential and least reversible action is visually indistinguishable from a routine "继续自检". | `style.css:245-252`, `455-460`, `504-511`, `518-525`, `581-586` |
| 3.4 | WARNING | Two near-identical blues (`#2c7be5`, `#2c5fb8`) with no documented distinction. | `style.css:167`, `200` |
| 3.5 | WARNING | Four WCAG AA contrast failures on normal-size text (AA requires 4.5:1): `.hint` `#999`/`#fafafa` = **2.73:1** (pervasive — every gate explanation); `#pending-count` and `.badge-pending` `#b8860b`/`#fdf6ec` = **3.03:1**; `.event-kind` white on `#b8860b` = **3.25:1**; `.chat-user` white on `#2c7be5` = **4.14:1** (the user's own messages). | computed from `style.css:35`, `387-395`, `136`, `311-316` |
| 3.6 | WARNING | A separate 7-color ad-hoc palette for event kinds (blue/purple/green/ochre/grey/red/black) that overlaps but does not align with the UI accent palette — e.g. green means both "写文件 event" and "positive button". | `style.css:133-139` |

### Pillar 4: Typography (2/4)

**Verified distribution (`style.css`):** 7 distinct sizes — 13px ×14, 12px ×5, 14px ×5, 12.5px ×3, 15px ×1, 16px ×1, 11px ×1. Weights: only `600` ×11 and `400` ×1. Family: one stack (`-apple-system, "PingFang SC", …`) applied to `html, body` only. Line-heights: 1.35 / 1.6 / 1.75.

**Findings:**

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 4.1 | WARNING | The type scale is flat and has no ratio. 13px is the default for essentially everything (buttons, inputs, bubbles, events, annotations, verdict cards, table cells); headings differ by 1-2px (14px panel titles, 15px `#draft-view h2`). There is no step between body and heading. | grep `font-size` |
| 4.2 | WARNING | Fractional sizes (12.5px ×3, `font-size: 12.5px` on `.markdown-body code` and `.verdict-*`) indicate values chosen per-component rather than from a scale. | `style.css:242`, `612`, `615` |
| 4.3 | BLOCKER | The rendered document — the primary content of the entire tool — has **no** type scale. `.markdown-body h1, h2, h3` set only margin and line-height, never `font-size`, so headings fall back to UA defaults (2em/1.5em/1.17em relative to the 14px body → 28/21/16.4px). The most-read text in the product is styled by the browser, not the system, and `h1` vs `h2` vs `h3` hierarchy is whatever Chrome/WebKit ships. | `style.css:215-223` |
| 4.4 | WARNING | Only two weights exist (600 and 400). No 500/700 step, so hierarchy cannot be expressed by weight — which is why 13px body text and 14px headings read as the same rank. | grep `font-weight` |
| 4.5 | WARNING | `<h1>文档区</h1>` unstyled at UA default (~32px) — see 2.1. The single largest type on screen is a container label. | `index.html:13` |
| 4.6 | INFO | No `prefers-color-scheme`, no dark mode, no reduced-motion handling. | grep `@media` → none |

### Pillar 5: Spacing (2/4)

**Verified distribution:** 16 distinct `padding` values (2px → 40px), 8 distinct `gap` values (4/6/8/10/12px), 13 distinct `margin` values. No scale, no tokens.

**Findings:**

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 5.1 | BLOCKER | Layout magic number coupling: `#state-badge { right: 448px; }` is hardcoded to sidebar width 420px + 28px, with the arithmetic only recorded in a comment. The badge is `position: fixed` and does not scroll with the doc pane, so scrolled content passes underneath it and is occluded (`z-index: 10`, opaque background). Any change to `#sidebar { flex: 0 0 420px }` silently misplaces the badge. | `style.css:28`, `193-204` |
| 5.2 | WARNING | Up to **four nested scroll containers** inside a 420px-wide column: `#sidebar` (`overflow-y:auto`) contains `#chat-messages` (`max-height:40vh`), `.event-list` (`max-height:55vh`), `#annotation-list` (`max-height:32vh`), and `#latest-check` (`max-height:30vh`), each independently scrollable. At a 900px viewport the inner panes alone total 55vh+40vh = 95vh before panel headers and padding, guaranteeing the outer sidebar also scrolls — nested scrollbars with no visual affordance for which one is which. | `style.css:31`, `94`, `296`, `400`, `571` |
| 5.3 | WARNING | Zero responsive rules (`@media` count = 0) despite `<meta name="viewport" content="width=device-width">` declaring responsiveness. `#app { display:flex; height:100vh }` with `#sidebar { flex: 0 0 420px }` and `#doc-pane { padding: 32px 40px }` means at a 1024px window the doc pane has 604px minus 80px padding = 524px; at 768px it has 268px; at 375px the fixed 420px sidebar exceeds the viewport and the layout overflows horizontally with no `min-width` guard or stacking fallback. | `style.css:13-33`; grep `@media` → none |
| 5.4 | WARNING | Conflicting sizing on one element: `#chat-messages` sets `flex: 1`, `min-height: 160px`, **and** `max-height: 40vh` simultaneously; `#session-panel` sets `min-height: 320px` and `flex-direction: column` with `overflow-y:auto` inherited from the sidebar. The interaction between these is not resolvable by inspection. | `style.css:286-302` |
| 5.5 | INFO | 8 distinct border-radii (2/3/4/6/8/9/10/12px), no radius scale. | grep `border-radius` |
| 5.6 | INFO | Non-token one-offs: `flex: 0 0 48px` (event chip), `min-width: 96px` (modal buttons), `max-width: 720px` (markdown body), `max-width: 420px` (overlay card), `min-height: 320px`/`160px`. | `style.css:114`, `353`, `216`, `159`, `286`, `295` |

### Pillar 6: Experience Design (2/4)

**Verified state coverage:**

| State type | Present | Missing |
|-----------|---------|---------|
| Loading | 3 text-swap states (`撰写中…` `app.js:511`, `处理中…` `app.js:1387`, `disabled` on 8 buttons) | No spinner/skeleton; no initial page-load state; no progress indication for calls that run for minutes |
| Error | 13 specific messages; 17 `try` blocks | 22 async functions without try/catch; no inline error placement; **no `EventSource.onerror`** |
| Empty | 5 (`#draft-empty`, `#brainstorm-view`, `#annotation-list`, `#latest-check`, `#round-doc`) | `#chat-messages`, `#ai-events`, `#verdict-cards`, `#check-switcher`, `#round-doc` error path |
| Disabled | 8 `:disabled` rules with `opacity: .55/.5` + `cursor: not-allowed` | No `:disabled` distinction beyond opacity; no `aria-disabled` |
| Confirmation | G3 confirmation-word modal; tier modal; permission modal | No confirmation on 中止 (acceptable per D-13 self-healing); no confirmation on 拒绝雏形/授权 rejection (uses native prompt) |

**Findings:**

| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| 6.1 | BLOCKER | **No keyboard path to the flagship feature.** `#selection-menu` is triggered exclusively by `roundDoc.addEventListener('mouseup')` (`app.js:1267`). A keyboard user who selects text with Shift+Arrow never fires `mouseup`, so the menu never appears and **no annotation can ever be created**. DESIGN.md D-02 makes 划词批注 a mandatory feature; it is mouse-only. | `app.js:1267-1284` |
| 6.2 | BLOCKER | **The SSE stream fails silently.** `initEventSource()` registers only `onmessage`. No `onerror`, `onopen`, or `onclose`. If the connection drops, the UI stops updating with no warning — and SSE is the sole feedback channel for every long-running AI operation in the product. | `app.js:136-148` |
| 6.3 | BLOCKER | **Read-only archive contract violated in the presentation layer.** In `mission_complete`, `applyArchiveView` calls `processRoundBtn.classList.add('hidden')` — a no-op (see Top Fix 1) — and never sets `disabled`. The button remains visible and clickable, contradicting §7.4 / D-P3-25 ("「处理本轮批注」… 均不可用"). The server 409s, so no data is corrupted, but the UI asserts a capability the design says does not exist. | `app.js:764-781`; no `#btn-process-round.hidden` rule |
| 6.4 | WARNING | **No `:focus` styles anywhere** (grep `:focus` = 0). Keyboard navigation is invisible — a user tabbing through the 21 buttons, 8 inputs, and 4 selects cannot see where focus is. | grep `:focus` → 0 |
| 6.5 | WARNING | **Modals are not dialogs.** Zero `role`, `aria-modal`, `aria-labelledby`, or `aria-live` attributes exist in the entire HTML. No Escape-to-close, no focus trap, and only one `.focus()` call in the whole app (`confirmWordInput`, `app.js:432`). The blocking permission modal — which gates filesystem access — receives no focus at all. The streaming chat has no `aria-live`, so screen readers get no announcement. | grep `aria-\|role=` → none |
| 6.6 | WARNING | **Dev scaffolding shipped in the primary UI.** `#probe-controls` sits permanently at the top of the AI work panel and contains an internal A/B route switch (`Claude Agent SDK` / `子进程兜底`), a *second* project-path text input, and a 「发起测试调用」 button. DESIGN.md §4.3 defines the work panel as an event display; none of this is in the design. It also presents two competing "enter a path" inputs on the same screen (top-left `#enter-path-input` vs. work-panel `#project-path-input`) with no indication of which is authoritative. | `index.html:131-140` |
| 6.7 | WARNING | No error boundary of any kind (vanilla JS). 22 of 39 async functions have no `try`/`catch`; e.g. the send button handler calls `sendMessage(text)` without awaiting or catching, and `sendMessage` (`app.js:1126-1140`) has no try/catch around its `fetch` — a network failure becomes an unhandled rejection with no user-visible effect. | `app.js:1167-1173`, `1126-1140` |
| 6.8 | WARNING | Abort has no confirmation and no undo affordance. `#btn-abort` immediately POSTs `/api/abort` and kills the in-flight call. Acceptable per D-13 (self-healing by re-run), but combined with 6.2 there is no way for the user to tell whether an abort succeeded or the stream merely died. | `app.js:1558-1567` |
| 6.9 | WARNING | Interaction states are almost entirely absent: 2 `:hover` rules, 1 `transition` in 622 lines, 0 `:active`. Buttons give no pressed feedback. | grep `:hover`/`:active`/`transition` |
| 6.10 | INFO | Panel collapse is implemented on only one panel (`#ai-panel-header`, `app.js:1504-1507`) while the other three sidebar panels have `cursor: pointer` styling that implies interactivity they do not have (`#annotations-panel .panel-header { cursor: default }` and `#checks-panel .panel-header { cursor: default }` override it correctly, but `#session-panel`'s header retains the pointer cursor with no handler). | `style.css:45`, `386`, `560`; `index.html:81` |

---

## Files Audited

- `/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/frontend/index.html` (218 lines)
- `/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/frontend/style.css` (622 lines)
- `/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/frontend/app.js` (1595 lines)
- `/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/DESIGN.md` (§4 layout/interaction contract, §7.4 archive state, §8.2 self-check)
- Phase intent baseline: `01-CONTEXT.md`, `idi-01-01..04-SUMMARY.md`, `02-CONTEXT.md`, `idi-02-03-SUMMARY.md`, `03-CONTEXT.md`, `idi-03-03-SUMMARY.md`, `idi-03-04-SUMMARY.md`

**Registry audit:** skipped — `components.json` absent (`NO_SHADCN`), and no UI-SPEC lists third-party registries.

**Screenshot artifacts:** `.planning/ui-reviews/` created with a `.gitignore` blocking `*.png`, `*.webp`, `*.jpg`, `*.jpeg`, `*.gif`, `*.bmp`, `*.tiff` (gate executed before any capture attempt). No binary files were produced or written.
# Interactive Discussion Iteration

English | [中文](README.md)

A **local** web tool that turns "discussing, refining, and aligning before an AI project starts" into a fixed process:

> **An idea goes in; an unambiguous master design document comes out.**

Single machine, single user, runs locally. Discussion documents are primarily in Chinese.

---

## The Problem It Solves

When you build a project with AI, the biggest waste isn't writing the wrong code — it's **not being aligned before you start**: the AI picks a direction on its own, or both sides assume they understood each other.

This tool turns "align before acting" into a process with a visual interface that supports annotation and full traceability, ending at a master design document. It stops at the design document — **writing code is outside this tool's scope**.

## Core Mechanics

### Five phases, three gates

| # | Phase | Output | Passing condition (gate) |
|---|-------|--------|--------------------------|
| 1 | Requirements & goals | Requirement/goal statement | Phases 1–2 are one continuous session; the only formal exit is G1 |
| 2 | Prototype | `docs/draft.md` | **G1**: user clicks "Approve prototype" |
| 2.5 | Divergence mode (optional) | Candidate directions → prototype | Same as G1 |
| 3 | N rounds of iterative convergence | One `discuss-round-N.md` per round | **G2** (per round): all annotations of that round answered; phase exit = open-questions list cleared + dimension table all green |
| 4 | Writing the master design document | `DESIGN.md` | **G3**: user gives **explicit authorization** (denied by default) |
| 5 | Self-check (lenient/strict) | Revised version + check report | Lenient: check + fix + report is enough; strict: one consecutive round with zero issues |

**G3 is the central constraint of the whole flow:** without the user's explicit authorization, the process never enters the "write the master design document" step. The authorization button lights up only when four mechanical checks all pass (no pending annotations, open-questions list cleared, coverage dimension table all green, and the AI's request marker is "yes"); after clicking, a confirmation word must still be typed in for a second confirmation.

### Key design points

- **A single interface for all five phases** — document pane on the left, annotation stream and AI work panel on the right. No separate pages;
- **Dual-track annotation** — select text and ask "explain this in plain words" for an answer within seconds (doesn't count toward convergence progress); once substantive annotations have piled up, click "Process this round's annotations" and the AI answers them all at once;
- **Round freezing** — once the next round exists, a round's document becomes read-only. Annotations always stay attached to the round they were born in, so they never drift;
- **Objective convergence criteria** — seven fixed coverage dimensions; the AI only becomes eligible to request authorization when all are green;
- **Permission gate** — reading files inside the project, and writing inside `docs/` or to `DESIGN.md.tmp`, are auto-approved; writing `DESIGN.md` directly or writing `AUTHORIZATION.md` is backend-only (the AI doing so is treated as out-of-bounds); all other reads/writes outside the project and executing any command require your approval in the UI;
- **Files are the state** — the tool keeps no separate process state; everything is derived from what's on disk. Reopen after a restart, crash, or shutdown and the state is intact;
- **Live event stream** — every sentence the AI says and every file it reads or writes is streamed to the work panel in real time. No black-box waiting.

## Quick Start

### Prerequisites

- The [claude CLI](https://docs.claude.com/en/docs/claude-code) installed and logged in on this machine (checked at startup);
- Python 3 (developed on 3.13).

### Run

```bash
./run.sh
```

The script bootstraps a virtual environment (creating `.venv` and installing dependencies if missing), then starts the server at:

```
http://127.0.0.1:8765
```

Open that address in your browser.

### Typical flow

1. Enter the **absolute path of the project directory** you want to discuss (discussion documents are written to `docs/` under it);
2. No idea yet? Click "Let the AI brainstorm candidate directions". Have one? Just start chatting in the session stream;
3. Once a prototype draft takes shape, click "Approve prototype" (G1) to enter round-based iteration;
4. Discuss round by round: select text to ask or annotate, then click "Process this round's annotations" to advance;
5. When the open-questions list is cleared and the dimension table is all green, the AI requests authorization — type the confirmation word, and the AI writes the master design document;
6. Choose a self-check level (lenient/strict). Once the check passes, the UI shows "Mission complete"; the flow ends and enters a read-only archived state.

## Project Structure

```
backend/          # Python + FastAPI backend
  main.py         #   app and routes (session / SSE / abort / permissions)
  session.py      #   session and flow orchestration
  ai_caller.py    #   dual AI call routes (SDK preferred / claude CLI subprocess fallback)
  grammar.py      #   §6.4 machine-parsable grammar
  prompts.py      #   per-phase prompts
  tests/          #   pytest tests
frontend/         # vanilla HTML/JS + markdown rendering library
  index.html
  app.js
  style.css
docs/             # this project's own discussion history and check reports
DESIGN.md         # this project's own master design document — the single authority
run.sh            # one-shot launch script
config.json       # runtime configuration
```

## Configuration

`config.json` at the repo root is the single source of configuration:

| Field | Value | Description |
|-------|-------|-------------|
| `ai_caller` | `"sdk"` / `"subprocess"` | AI call route. `sdk` = Claude Agent SDK (preferred); `subprocess` = `claude -p --output-format stream-json` subprocess fallback. Both routes share the same UI contract and can be swapped at will |
| `ai_model` | model name or `null` | Pin an AI model; `null` uses the CLI default |

## Tests

```bash
.venv/bin/python -m pytest -m "not slow"   # fast unit/integration tests
.venv/bin/python -m pytest                 # includes slow: end-to-end tests needing a real logged-in claude CLI
```

## Documentation

- **`DESIGN.md`** — this project's single authoritative design document (v1.13, closed). If anything else conflicts with it, it wins;
- `docs/discuss-round-0~4.md` — this project's own discussion history;
- `docs/DESIGN-check-1~14.md` — this project's own self-check reports;
- `.planning/` — implementation-side supporting views (roadmap, requirements, phase verification records); not authoritative.

## License

[AGPL-3.0](LICENSE)
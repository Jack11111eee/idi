---
schema_version: 1
open_count: 2
waived_count: 0
fixed_count: 1
total_count: 3
last_updated: 2026-09-09T07:54:54.087Z
---

# Broken Windows Ledger

> Cross-phase defect register. With `workflow.windows_enforce` enabled, `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | idi-01 | deviation | backend/transcript.py |  | append_message 父目录自举:计划称 a 模式不存在会建,但新讨论首条消息时 docs/ 尚不存在,已补 mkdir(parents=True) | open |  | 2026-09-09T03:35:41.900Z |  |
| 2 | 1 | deviation | frontend/index.html |  | D4/AI-05: claude CLI 未装/未登录两分支浮层交互需浏览器人检(本机已装已登录无法真实触发失败分支) | open |  | 2026-09-09T05:29:43.842Z |  |
| 3 | idi-01 | deviation | backend/ai_caller.py | 608 | 子进程路线 init 设置(若连不上 CLI 文档形态降级)与 stderr 噪声在 result-line 收尾后不再进事件流 | fixed |  | 2026-09-09T07:54:23.719Z | 2026-09-09T07:54:54.087Z |

````json
[
  {
    "id": 1,
    "kind": "deviation",
    "phase": "idi-01",
    "file": "backend/transcript.py",
    "line": null,
    "description": "append_message 父目录自举:计划称 a 模式不存在会建,但新讨论首条消息时 docs/ 尚不存在,已补 mkdir(parents=True)",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-09T03:35:41.900Z",
    "resolved_at": null
  },
  {
    "id": 2,
    "kind": "deviation",
    "phase": "1",
    "file": "frontend/index.html",
    "line": null,
    "description": "D4/AI-05: claude CLI 未装/未登录两分支浮层交互需浏览器人检(本机已装已登录无法真实触发失败分支)",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-09T05:29:43.842Z",
    "resolved_at": null
  },
  {
    "id": 3,
    "kind": "deviation",
    "phase": "idi-01",
    "file": "backend/ai_caller.py",
    "line": 608,
    "description": "子进程路线 init 设置(若连不上 CLI 文档形态降级)与 stderr 噪声在 result-line 收尾后不再进事件流",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-09T07:54:23.719Z",
    "resolved_at": "2026-09-09T07:54:54.087Z"
  }
]
````

---
schema_version: 1
open_count: 1
waived_count: 0
fixed_count: 0
total_count: 1
last_updated: 2026-09-09T03:35:41.900Z
---

# Broken Windows Ledger

> Cross-phase defect register. With `workflow.windows_enforce` enabled, `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | idi-01 | deviation | backend/transcript.py |  | append_message 父目录自举:计划称 a 模式不存在会建,但新讨论首条消息时 docs/ 尚不存在,已补 mkdir(parents=True) | open |  | 2026-09-09T03:35:41.900Z |  |

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
  }
]
````

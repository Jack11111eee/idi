---
schema_version: 1
open_count: 5
waived_count: 0
fixed_count: 1
total_count: 6
last_updated: 2026-09-10T02:42:58.000Z
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
| 4 | idi-01 | deviation | backend/tests/test_session.py |  | TDD RED 证据未按 test/feat 两段提交(实测输出保全,功能切片 a9d8a90/5ec5b9b) | open |  | 2026-09-09T08:41:30.596Z |  |
| 5 | idi-01 | unrun-verify | frontend/index.html |  | UAT 人检批次待办:浏览器走 没想法→brainstorm→发方向→认可雏形→轮次占位(PLAN verification 第 5 条) | open |  | 2026-09-09T08:41:30.704Z |  |
| 6 | 2 | deviation | frontend/app.js |  | ui.safety-gate(wave3/idi-02-03)blocking 结果为项目级配置缺口而非本波缺陷:对 Phase 1 回跑同一 gate 同样 block:true(前端文件已改+无 UI-SPEC.md)而 Phase 1 verification passed——本项目从未生成 UI-SPEC(规划期 ui-phase 步骤未执行)。本项目唯一权威设计文档为根 DESIGN.md,.planning 皆为辅助视图;UI 契约即 DESIGN.md §4.1/§4.2,idi-02-03 must_haves 逐字复述该两节。处置:编排者接受 gate 报告为已记录偏差(Phase 1 同构先例+DESIGN.md 为契约权威+浏览器 UAT 六点清单为实际验证工具,UAT 结果落 02-VERIFICATION.md),不回滚不中途重构;gate 处方 /gsd-ui-phase 属规划期动作留给用户裁量。 | open |  | 2026-09-10T02:42:58.000Z |  |

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
  },
  {
    "id": 4,
    "kind": "deviation",
    "phase": "idi-01",
    "file": "backend/tests/test_session.py",
    "line": null,
    "description": "TDD RED 证据未按 test/feat 两段提交(实测输出保全,功能切片 a9d8a90/5ec5b9b)",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-09T08:41:30.596Z",
    "resolved_at": null
  },
  {
    "id": 5,
    "kind": "unrun-verify",
    "phase": "idi-01",
    "file": "frontend/index.html",
    "line": null,
    "description": "UAT 人检批次待办:浏览器走 没想法→brainstorm→发方向→认可雏形→轮次占位(PLAN verification 第 5 条)",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-09T08:41:30.704Z",
    "resolved_at": null
  },
  {
    "id": 6,
    "kind": "deviation",
    "phase": "2",
    "file": "frontend/app.js",
    "line": null,
    "description": "ui.safety-gate(wave3/idi-02-03)blocking 结果为项目级配置缺口而非本波缺陷:对 Phase 1 回跑同一 gate 同样 block:true(前端文件已改+无 UI-SPEC.md)而 Phase 1 verification passed——本项目从未生成 UI-SPEC(规划期 ui-phase 步骤未执行)。本项目唯一权威设计文档为根 DESIGN.md,.planning 皆为辅助视图;UI 契约即 DESIGN.md §4.1/§4.2,idi-02-03 must_haves 逐字复述该两节。处置:编排者接受 gate 报告为已记录偏差(Phase 1 同构先例+DESIGN.md 为契约权威+浏览器 UAT 六点清单为实际验证工具,UAT 结果落 02-VERIFICATION.md),不回滚不中途重构;gate 处方 /gsd-ui-phase 属规划期动作留给用户裁量。",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-10T02:42:58.000Z",
    "resolved_at": null
  }
]
````

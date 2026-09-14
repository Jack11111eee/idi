---
schema_version: 1
open_count: 0
waived_count: 3
fixed_count: 5
total_count: 8
last_updated: 2026-09-14T06:22:46.362Z
---

# Broken Windows Ledger

> Cross-phase defect register. With `workflow.windows_enforce` enabled, `/gsd-ship` blocks while `open_count > 0`.
> Waive with `gsd-tools windows waive <id> "<reason>"` (reason required).
> Mark fixed with `gsd-tools windows fixed <id>`.

| id | phase | kind | file | line | description | status | reason | recorded_at | resolved_at |
|----|-------|------|------|------|-------------|--------|--------|-------------|-------------|
| 1 | idi-01 | deviation | backend/transcript.py |  | append_message 父目录自举:计划称 a 模式不存在会建,但新讨论首条消息时 docs/ 尚不存在,已补 mkdir(parents=True) | fixed |  | 2026-09-09T03:35:41.900Z | 2026-09-14T06:21:08.614Z |
| 2 | 1 | deviation | frontend/index.html |  | D4/AI-05: claude CLI 未装/未登录两分支浮层交互需浏览器人检(本机已装已登录无法真实触发失败分支) | waived | 环境不可触发:本机 claude CLI 恒已装已登录(2.1.266),未装/未登录两分支无法真实触发;浮层机制本体(加载即检/通过放行/重检再检)已由 01-UAT.md 检查点 4 在修复 31deefb 后实证为活代码,仅两失败分支留待换机或卸载场景人检 | 2026-09-09T05:29:43.842Z | 2026-09-14T06:22:46.139Z |
| 3 | idi-01 | deviation | backend/ai_caller.py | 608 | 子进程路线 init 设置(若连不上 CLI 文档形态降级)与 stderr 噪声在 result-line 收尾后不再进事件流 | fixed |  | 2026-09-09T07:54:23.719Z | 2026-09-09T07:54:54.087Z |
| 4 | idi-01 | deviation | backend/tests/test_session.py |  | TDD RED 证据未按 test/feat 两段提交(实测输出保全,功能切片 a9d8a90/5ec5b9b) | waived | 纯过程留痕非代码缺陷:实测输出与功能切片(a9d8a90/5ec5b9b)均已保全,TDD RED 两段式提交纪律属一次性执行瑕疵,不构成需修复的制品,不追溯改写历史 | 2026-09-09T08:41:30.596Z | 2026-09-14T06:22:46.247Z |
| 5 | idi-01 | unrun-verify | frontend/index.html |  | UAT 人检批次待办:浏览器走 没想法→brainstorm→发方向→认可雏形→轮次占位(PLAN verification 第 5 条) | fixed |  | 2026-09-09T08:41:30.704Z | 2026-09-14T06:21:08.724Z |
| 6 | 2 | deviation | frontend/app.js |  | ui.safety-gate(wave3/idi-02-03)blocking 结果为项目级配置缺口而非本波缺陷:对 Phase 1 回跑同一 gate 同样 block:true(前端文件已改+无 UI-SPEC.md)而 Phase 1 verification passed——本项目从未生成 UI-SPEC(规划期 ui-phase 步骤未执行)。本项目唯一权威设计文档为根 DESIGN.md,.planning 皆为辅助视图;UI 契约即 DESIGN.md §4.1/§4.2,idi-02-03 must_haves 逐字复述该两节。处置:编排者接受 gate 报告为已记录偏差(Phase 1 同构先例+DESIGN.md 为契约权威+浏览器 UAT 六点清单为实际验证工具,UAT 结果落 02-VERIFICATION.md),不回滚不中途重构;gate 处方 /gsd-ui-phase 属规划期动作留给用户裁量。 | waived | 项目级配置缺口非本波缺陷:本项目唯一权威设计文档为根 DESIGN.md,UI 契约即 §4.1/§4.2,从未生成 UI-SPEC(规划期 ui-phase 步骤未执行);Phase 1 回跑同一 gate 亦 block:true 而 Phase 1 verification passed,属同构先例;实际验证工具为真浏览器 UAT(02-VERIFICATION.md) | 2026-09-10T02:42:58.000Z | 2026-09-14T06:22:46.362Z |
| 7 | 2 | unrun-verify | backend/tests/test_e2e_rounds.py |  | UAT 六点浏览器人检待办(PHASE2 收口):划词菜单/批注流/高亮/大白话灰斜体/处理直播+冻结/反向划选——交接表在 idi-02-04-SUMMARY,造盘项目 /tmp/idi-02-04-uat-project;后端全链已由 IDI_E2E 真跑 2 passed 证明,浏览器视觉面 pending | fixed |  | 2026-09-09T22:49:11.296Z | 2026-09-14T06:21:08.828Z |
| 8 | 2 | deviation | backend/prompts.py |  | idi-02-04 修复留痕:_ROUND_INSTRUCTIONS 补资料完备性段(AI 幻觉读不存在路径触发项目外读→confirm 无限挂;已修复,E2E 真跑复验通过)——记录 CLI 失眠窗口环境事实(约 05:00-06:00 CST 启动即挂死)与 answer_plain 一次 121.7s 高负载例外,供 Phase 3 真调用 E2E 预算参考 | fixed |  | 2026-09-09T22:49:33.210Z | 2026-09-14T06:22:46.025Z |

````json
[
  {
    "id": 1,
    "kind": "deviation",
    "phase": "idi-01",
    "file": "backend/transcript.py",
    "line": null,
    "description": "append_message 父目录自举:计划称 a 模式不存在会建,但新讨论首条消息时 docs/ 尚不存在,已补 mkdir(parents=True)",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-09T03:35:41.900Z",
    "resolved_at": "2026-09-14T06:21:08.614Z"
  },
  {
    "id": 2,
    "kind": "deviation",
    "phase": "1",
    "file": "frontend/index.html",
    "line": null,
    "description": "D4/AI-05: claude CLI 未装/未登录两分支浮层交互需浏览器人检(本机已装已登录无法真实触发失败分支)",
    "status": "waived",
    "reason": "环境不可触发:本机 claude CLI 恒已装已登录(2.1.266),未装/未登录两分支无法真实触发;浮层机制本体(加载即检/通过放行/重检再检)已由 01-UAT.md 检查点 4 在修复 31deefb 后实证为活代码,仅两失败分支留待换机或卸载场景人检",
    "recorded_at": "2026-09-09T05:29:43.842Z",
    "resolved_at": "2026-09-14T06:22:46.139Z"
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
    "status": "waived",
    "reason": "纯过程留痕非代码缺陷:实测输出与功能切片(a9d8a90/5ec5b9b)均已保全,TDD RED 两段式提交纪律属一次性执行瑕疵,不构成需修复的制品,不追溯改写历史",
    "recorded_at": "2026-09-09T08:41:30.596Z",
    "resolved_at": "2026-09-14T06:22:46.247Z"
  },
  {
    "id": 5,
    "kind": "unrun-verify",
    "phase": "idi-01",
    "file": "frontend/index.html",
    "line": null,
    "description": "UAT 人检批次待办:浏览器走 没想法→brainstorm→发方向→认可雏形→轮次占位(PLAN verification 第 5 条)",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-09T08:41:30.704Z",
    "resolved_at": "2026-09-14T06:21:08.724Z"
  },
  {
    "id": 6,
    "kind": "deviation",
    "phase": "2",
    "file": "frontend/app.js",
    "line": null,
    "description": "ui.safety-gate(wave3/idi-02-03)blocking 结果为项目级配置缺口而非本波缺陷:对 Phase 1 回跑同一 gate 同样 block:true(前端文件已改+无 UI-SPEC.md)而 Phase 1 verification passed——本项目从未生成 UI-SPEC(规划期 ui-phase 步骤未执行)。本项目唯一权威设计文档为根 DESIGN.md,.planning 皆为辅助视图;UI 契约即 DESIGN.md §4.1/§4.2,idi-02-03 must_haves 逐字复述该两节。处置:编排者接受 gate 报告为已记录偏差(Phase 1 同构先例+DESIGN.md 为契约权威+浏览器 UAT 六点清单为实际验证工具,UAT 结果落 02-VERIFICATION.md),不回滚不中途重构;gate 处方 /gsd-ui-phase 属规划期动作留给用户裁量。",
    "status": "waived",
    "reason": "项目级配置缺口非本波缺陷:本项目唯一权威设计文档为根 DESIGN.md,UI 契约即 §4.1/§4.2,从未生成 UI-SPEC(规划期 ui-phase 步骤未执行);Phase 1 回跑同一 gate 亦 block:true 而 Phase 1 verification passed,属同构先例;实际验证工具为真浏览器 UAT(02-VERIFICATION.md)",
    "recorded_at": "2026-09-10T02:42:58.000Z",
    "resolved_at": "2026-09-14T06:22:46.362Z"
  },
  {
    "id": 7,
    "kind": "unrun-verify",
    "phase": "2",
    "file": "backend/tests/test_e2e_rounds.py",
    "line": null,
    "description": "UAT 六点浏览器人检待办(PHASE2 收口):划词菜单/批注流/高亮/大白话灰斜体/处理直播+冻结/反向划选——交接表在 idi-02-04-SUMMARY,造盘项目 /tmp/idi-02-04-uat-project;后端全链已由 IDI_E2E 真跑 2 passed 证明,浏览器视觉面 pending",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-09T22:49:11.296Z",
    "resolved_at": "2026-09-14T06:21:08.828Z"
  },
  {
    "id": 8,
    "kind": "deviation",
    "phase": "2",
    "file": "backend/prompts.py",
    "line": null,
    "description": "idi-02-04 修复留痕:_ROUND_INSTRUCTIONS 补资料完备性段(AI 幻觉读不存在路径触发项目外读→confirm 无限挂;已修复,E2E 真跑复验通过)——记录 CLI 失眠窗口环境事实(约 05:00-06:00 CST 启动即挂死)与 answer_plain 一次 121.7s 高负载例外,供 Phase 3 真调用 E2E 预算参考",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-09T22:49:33.210Z",
    "resolved_at": "2026-09-14T06:22:46.025Z"
  }
]
````

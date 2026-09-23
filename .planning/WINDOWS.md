---
schema_version: 1
open_count: 5
waived_count: 3
fixed_count: 9
total_count: 17
last_updated: 2026-09-21T06:44:50.930Z
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
| 9 | idi-04 | unrun-verify | .planning/phases/idi-04-tokens-contract/idi-04-03-SUMMARY.md |  | CHECK-02 DevTools Computed spot-checks (4 named items) not performed — auto mode, screenshots unavailable | open |  | 2026-09-17T14:58:05.360Z |  |
| 10 | idi-04 | unrun-verify | .planning/phases/idi-04-tokens-contract/idi-04-03-SUMMARY.md |  | Stage close-out DevTools checks (6 named items incl. #brainstorm-view h2 14px/rgb(138,101,8) and frozen-round marker) not performed — auto mode | open |  | 2026-09-17T14:58:05.467Z |  |
| 11 | 260919-0h3 | unmet-truth | .planning/phases/idi-04-tokens-contract/idi-04-UAT.md |  | UAT 第 3/4/5 项 fail(7+9+4 条 FAIL 断言):期望值定稿于 0c658aa,被 448686b 令牌值层换肤作废;待裁:更新期望值或回退令牌值 | open |  | 2026-09-18T17:09:49.959Z |  |
| 12 | 260919-0h3 | unrun-verify | .planning/phases/idi-04-tokens-contract/idi-04-UAT.md |  | UAT 第 4 项 #doc-pane 选择器不存在(index.html 实际为 #doc-panel-body),该格如实记 blocked | open |  | 2026-09-18T17:09:50.074Z |  |
| 13 | 260919-0h3 | deviation | scripts/check-05-ui-uat.py |  | 浏览器由 channel=chrome 改为 Playwright 自带 chromium:计划的两条理由均失效(1243 已缓存;x86_64 venv 下 chrome 无头走 Rosetta 会 CDP 挂死) | open |  | 2026-09-18T17:09:50.180Z |  |
| 14 | 04.1 | deviation | frontend/style.css |  | Rule 2 自动修正:--shadow-overlay 紧邻的分节注释原文写 'the single shadow token',Task 3 新增第二个 shadow 令牌后成为假陈述;已在 Task 3 内改为 'the shadow tokens' 并与声明同提交落地 (00c6073) | fixed |  | 2026-09-19T13:08:41.612Z | 2026-09-19T13:10:43.199Z |
| 15 | 05 | deviation | frontend/style.css | 619 | plan idi-05-01 Task1 halt: .markdown-body h2 fails to reach --text-2xl in 3 of 4 hosts | fixed | 根因:三条 chrome 规则用后代选择器(#draft-view h2 / #rounds-placeholder h2 / #brainstorm-view h2,均 1-0-1)伸进 .markdown-body,把 .markdown-body h2(0-1-1)无条件压回 chrome 字号,四个宿主里三个拿不到 D-06 的 22px。已收窄为 #draft-view > h2 / #round-title / #brainstorm-view > h2,三条规则的声明体逐字不动。check-05 item4 由 27 条(1 FAIL)扩为 36 条(四宿主 × 三档,0 FAIL),smoke PASS,CHECK-01..04 PASS。UI-SPEC 范围栅栏与 plan idi-05-01 Task1 第 3b 步已同步订正 | 2026-09-20T15:57:55.903Z | 2026-09-21T01:59:49.454Z |
| 16 | idi-05 | deviation | .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-03-PLAN.md |  | Task 1/3 verify commands grep check-02 output with uppercase 'ON' but check-02 emits lowercase 'on' (label format '%s on %s') -> literal form always returns 0; disk-truth form returns the intended 2 and 1 | fixed | 计划文本缺陷,非产品缺陷:check-02 的标签恒为小写 'on',三处 grep 的 'ON' 字面永不匹配(各返回 0,在 <fails_when> 下会报假失败)。已把 plan 03 的 L245 / L377 / L379 三处改为小写 'on',改正后实测 2 / 1 / 2,与计划意图一致。代码零改动 | 2026-09-21T06:38:07.346Z | 2026-09-21T06:44:50.794Z |
| 17 | idi-05 | deviation | .planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-03-PLAN.md |  | Task 2 verify greps 'mask-image: var(--icon-pin);' expecting 1, but '-webkit-mask-image: ...' contains that substring so it returns 2; plan's own action mandates both prefixed and unprefixed forms. Anchored grep returns 1 | fixed | 计划文本缺陷,非产品缺陷:该 grep 未锚定,`-webkit-mask-image: var(--icon-pin);` 含目标子串故返回 2;而同一任务的 <action> 明令前缀与非前缀两种写法都要写 —— 计划自相矛盾。已改为行首锚定的 `grep -cE '^[[:space:]]*mask-image: var\(--icon-pin\);'`,改正后实测 1 / 1,与「每个令牌恰一个 mask-image 消费者」的意图一致。代码零改动 | 2026-09-21T06:38:07.459Z | 2026-09-21T06:44:50.930Z |

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
  },
  {
    "id": 9,
    "kind": "unrun-verify",
    "phase": "idi-04",
    "file": ".planning/phases/idi-04-tokens-contract/idi-04-03-SUMMARY.md",
    "line": null,
    "description": "CHECK-02 DevTools Computed spot-checks (4 named items) not performed — auto mode, screenshots unavailable",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-17T14:58:05.360Z",
    "resolved_at": null
  },
  {
    "id": 10,
    "kind": "unrun-verify",
    "phase": "idi-04",
    "file": ".planning/phases/idi-04-tokens-contract/idi-04-03-SUMMARY.md",
    "line": null,
    "description": "Stage close-out DevTools checks (6 named items incl. #brainstorm-view h2 14px/rgb(138,101,8) and frozen-round marker) not performed — auto mode",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-17T14:58:05.467Z",
    "resolved_at": null
  },
  {
    "id": 11,
    "kind": "unmet-truth",
    "phase": "260919-0h3",
    "file": ".planning/phases/idi-04-tokens-contract/idi-04-UAT.md",
    "line": null,
    "description": "UAT 第 3/4/5 项 fail(7+9+4 条 FAIL 断言):期望值定稿于 0c658aa,被 448686b 令牌值层换肤作废;待裁:更新期望值或回退令牌值",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-18T17:09:49.959Z",
    "resolved_at": null
  },
  {
    "id": 12,
    "kind": "unrun-verify",
    "phase": "260919-0h3",
    "file": ".planning/phases/idi-04-tokens-contract/idi-04-UAT.md",
    "line": null,
    "description": "UAT 第 4 项 #doc-pane 选择器不存在(index.html 实际为 #doc-panel-body),该格如实记 blocked",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-18T17:09:50.074Z",
    "resolved_at": null
  },
  {
    "id": 13,
    "kind": "deviation",
    "phase": "260919-0h3",
    "file": "scripts/check-05-ui-uat.py",
    "line": null,
    "description": "浏览器由 channel=chrome 改为 Playwright 自带 chromium:计划的两条理由均失效(1243 已缓存;x86_64 venv 下 chrome 无头走 Rosetta 会 CDP 挂死)",
    "status": "open",
    "reason": "",
    "recorded_at": "2026-09-18T17:09:50.180Z",
    "resolved_at": null
  },
  {
    "id": 14,
    "kind": "deviation",
    "phase": "04.1",
    "file": "frontend/style.css",
    "line": null,
    "description": "Rule 2 自动修正:--shadow-overlay 紧邻的分节注释原文写 'the single shadow token',Task 3 新增第二个 shadow 令牌后成为假陈述;已在 Task 3 内改为 'the shadow tokens' 并与声明同提交落地 (00c6073)",
    "status": "fixed",
    "reason": "",
    "recorded_at": "2026-09-19T13:08:41.612Z",
    "resolved_at": "2026-09-19T13:10:43.199Z"
  },
  {
    "id": 15,
    "kind": "deviation",
    "phase": "05",
    "file": "frontend/style.css",
    "line": 619,
    "description": "plan idi-05-01 Task1 halt: .markdown-body h2 fails to reach --text-2xl in 3 of 4 hosts",
    "status": "fixed",
    "reason": "根因:三条 chrome 规则用后代选择器(#draft-view h2 / #rounds-placeholder h2 / #brainstorm-view h2,均 1-0-1)伸进 .markdown-body,把 .markdown-body h2(0-1-1)无条件压回 chrome 字号,四个宿主里三个拿不到 D-06 的 22px。已收窄为 #draft-view > h2 / #round-title / #brainstorm-view > h2,三条规则的声明体逐字不动。check-05 item4 由 27 条(1 FAIL)扩为 36 条(四宿主 × 三档,0 FAIL),smoke PASS,CHECK-01..04 PASS。UI-SPEC 范围栅栏与 plan idi-05-01 Task1 第 3b 步已同步订正",
    "recorded_at": "2026-09-20T15:57:55.903Z",
    "resolved_at": "2026-09-21T01:59:49.454Z"
  },
  {
    "id": 16,
    "kind": "deviation",
    "phase": "idi-05",
    "file": ".planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-03-PLAN.md",
    "line": null,
    "description": "Task 1/3 verify commands grep check-02 output with uppercase 'ON' but check-02 emits lowercase 'on' (label format '%s on %s') -> literal form always returns 0; disk-truth form returns the intended 2 and 1",
    "status": "fixed",
    "reason": "计划文本缺陷,非产品缺陷:check-02 的标签恒为小写 'on',三处 grep 的 'ON' 字面永不匹配(各返回 0,在 <fails_when> 下会报假失败)。已把 plan 03 的 L245 / L377 / L379 三处改为小写 'on',改正后实测 2 / 1 / 2,与计划意图一致。代码零改动",
    "recorded_at": "2026-09-21T06:38:07.346Z",
    "resolved_at": "2026-09-21T06:44:50.794Z"
  },
  {
    "id": 17,
    "kind": "deviation",
    "phase": "idi-05",
    "file": ".planning/phases/idi-05-typography-and-visual-hierarchy/idi-05-03-PLAN.md",
    "line": null,
    "description": "Task 2 verify greps 'mask-image: var(--icon-pin);' expecting 1, but '-webkit-mask-image: ...' contains that substring so it returns 2; plan's own action mandates both prefixed and unprefixed forms. Anchored grep returns 1",
    "status": "fixed",
    "reason": "计划文本缺陷,非产品缺陷:该 grep 未锚定,`-webkit-mask-image: var(--icon-pin);` 含目标子串故返回 2;而同一任务的 <action> 明令前缀与非前缀两种写法都要写 —— 计划自相矛盾。已改为行首锚定的 `grep -cE '^[[:space:]]*mask-image: var\\(--icon-pin\\);'`,改正后实测 1 / 1,与「每个令牌恰一个 mask-image 消费者」的意图一致。代码零改动",
    "recorded_at": "2026-09-21T06:38:07.459Z",
    "resolved_at": "2026-09-21T06:44:50.930Z"
  }
]
````

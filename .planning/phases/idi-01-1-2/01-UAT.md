---
status: complete
phase: idi-01-1-2
source: [idi-01-01-SUMMARY.md, idi-01-02-SUMMARY.md, idi-01-03-SUMMARY.md, idi-01-04-SUMMARY.md]
started: 2026-09-09T09:50:00Z
updated: 2026-09-09T11:00:00Z
---

## Current Test

[testing complete]

## 测试方式说明

按 orchestrator 授权,本会话以自动化浏览器 UAT 替代逐条人工问答(verify-work workflow 的 `automated-ui-verification` 步骤):真实启动 `bash run.sh`(uvicorn:8765),经 CDP 驱动一个隔离 Chrome 实例(独立 user-data-dir,非用户常用浏览器),对 6 项人检条逐条实测并截图取证(/tmp/idi-uat-artifacts/shots/,共 8 张:01-initial/02-entered-phase1/03-permission-modal/04-brainstorm/05-draft-and-session/07-rounds-placeholder/08-permission-modal-deny/09-recovery-proj1)。涉及 AI 的两条链路(发散、会话轮)均走真实 claude CLI 调用(每轮数分钟),磁盘文件(transcript.md/brainstorm.md/draft.md/discuss-round-1.md)作为 ground truth 逐项核对。

## Tests

### 1. 浏览器端到端用户流(空目录 → 没想法 → 发散 → 发方向 → 草稿 → 认可雏形 → 轮次占位)
expected: 每步按 DESIGN.md §3.2/§4.1/§4.4 呈现;brainstorm.md/draft.md/discuss-round-1.md 落盘;最终界面切「已进入轮次阶段(本阶段占位)。当前轮:第 1 轮。」
result: issue
reported: "主链各步全部真实跑通且落盘正确:① 空目录进入 → 徽标「新讨论(阶段 1)」、draft-empty、发散按钮在场;② 点「没想法」→ 发散直播、brainstorm.md 落盘(5 候选)、brainstorm 区渲染;③ 会话发方向 A → transcript.md 落 [user]/[ai] 对、draft.md 落盘并在草稿区渲染(markdown);⑤ 点「认可雏形」→ discuss-round-1.md 落盘且末行恰为「> 申请授权:否」、draft.md 字节保留、界面切「轮次阶段(阶段 3)」+「当前轮:第 1 轮」。但第④步断链:草稿出来后,「认可雏形」按钮在当前页面仍保持 disabled(title 仍为「先要有雏形草稿才能认可」)、发散入口仍可见——`refreshDraftAfterStream()`(app.js:292)只拉新 draft/brainstorm 重渲染,不调 `applySessionView`,故 `g1_available`/`divergence_available` 门控在当前页面上永不更新;用户手动重进(重新 POST /api/enter)后按钮才解禁。用户若不知道需「重新进入」,会认为无法认可雏形——goal 全句「草稿出来 → 认可雏形」在无人工干预的浏览器操作里走不通。"
severity: major

### 2. SSE 事件逐条渲染进工作面板(say 走 markdown、read/write/command 显示路径,面板可折叠)
expected: 事件分级标签与颜色正确(kind-say/command/write/done 等类名与标签),say 走 markdown,面板可折叠
result: pass
evidence: 实测两轮 AI 调用共 15 条事件逐条流进 #ai-events,类名分级正确(kind-say/kind-command/kind-permission_request/kind-permission_resolved/kind-write/kind-read/kind-done);say 内容经 marked 渲染(innerHTML 含 <p>/<strong>);write 事件显示完整落盘路径;点面板标题折叠/展开往返生效(collapsed 类切换 + ▾ 指示器)。

### 3. 权限弹窗闭环(AI confirm 时弹模态框,同意/拒绝两按钮回传生效)
expected: 模态框出现并说明工具与目标;同意放行/拒绝驳回,面板出现权限确认事件
result: pass
evidence: 发散轮(工具 Bash:pwd && ls -la ...)与越权写轮(Bash:echo "hello" > notes-test.txt)均真实弹出模态框(permission-modal 显示,文案含工具名+命令全文);第一次点「同意」→ 面板出现 permission_resolved、命令继续执行;第二次对越权写点「拒绝」→ permission_resolved、notes-test.txt 未被创建(transcript 与目录双重核实),AI 在后续回复中明确说明「写入命令被驳回」。会话轮结束 transcript.md 仅落 [user] + [ai] 一对。

### 4. CLI 自检失败分支视觉(未装/未登录指引浮层 + 重新检测放行)
expected: 浮层显示对应中文指引;点击「已装好,重新检测」通过后浮层消失且不再出现(只挡第一次)
result: issue
reported: "本机 CLI 已装已登录(2.1.266),'未装/未登录'两分支本就无法真实触发,这部分按原计划记为环境不可触发;但实测发现更根本的问题:任何页面加载时 /api/cli-check 根本从未被请求(服务端日志三轮加载均无该请求,performance resource 仅 /api/config),原因是 index.html 中 app.js(script 标签,行 115)先于 cli-check-overlay DOM(行 118-124)执行,app.js:534 `recheckBtn.addEventListener` 对 null 调 addEventListener 抛 Uncaught TypeError(经注入 error listener 捕获:'Cannot read properties of null (reading addEventListener) @line 534 col 12',在干净无注入的页面复现同一行为),脚本在此中止,行 535 的 `runCliCheck()` 永不执行。即 CLI 自检浮层(通过分支和失败分支)在正常页面加载时整体失效,「只挡第一次」「重检放行」的接线在浏览器里全部是死代码。此前 VERIFICATION 报告判定'接线完整(app.js:519-535)'是基于源码通读,未覆盖脚本执行时序。"
severity: major

### 5. 视觉样式目检(会话气泡左右对齐、模态布局、草稿排版、发散候选虚线)
expected: 样式与 §4.1/§4.2 布局一致,无排版破损
result: pass
evidence: 8 张截图目检:用户气泡 alignSelf:flex-end(蓝底 #2c7be5 右对齐)、AI 气泡 flex-start(灰底 #f1f3f5 左对齐);模态框居中遮罩布局正常(rgba 黑 45% 背景 + 卡片居中);草稿区 markdown 渲染正常(H2/H3/列表/引用块,截图 05);brainstorm 候选区 1px dashed 边框(computed style 核实);三区布局(左文档+右会话流/工作面板)无破损。附注(非缺陷判定):AI 会话气泡在流结束后保留 streaming-ai 类的蓝色左边框(app.js:186 添加后从不移除,done 只置 null 引用)——视觉上是轻微残留,DESIGN 未规定流式标记样式,记为观察项不单独立 gap。

### 6. 重启浏览器恢复体验(关页重开重进同目录,会话流与草稿完整恢复)
expected: 会话流与草稿从磁盘全量恢复,无需任何恢复操作
result: pass
evidence: 关闭整个浏览器页面并新开空 target(全新页面生命周期,无 BFCache),重进 proj2 → transcript 两条消息([user] 越权写请求 + [ai] 驳回说明)完整恢复、徽标「阶段 1-2 讨论中」、AI 气泡 markdown 重新渲染;重进 proj1 → 徽标「轮次阶段(阶段 3)」、rounds 占位「当前轮:第 1 轮」、transcript+draft+discuss-round-1 全部按磁盘现状呈现、发散入口正确关闭、认可按钮正确 disabled(title「已定稿——项目已在轮次阶段」)。全部从磁盘推导,零恢复操作。

## Summary

total: 6
passed: 3
issues: 2
pending: 0
skipped: 0
blocked: 0

## Gaps

<!-- YAML format for plan-phase --gaps consumption -->
- gap_id: G-idi01-7
  truth: "会话轮产出雏形草稿后,「认可雏形」按钮应在当前页面解禁可点(goal 链:草稿出来 → 认可雏形,§4.4 常驻按钮)"
  status: failed
  reason: "User reported: 草稿出来后按钮仍 disabled、发散入口仍开着;refreshDraftAfterStream() 只重渲染 draft/brainstorm 内容,不刷新 g1_available/divergence_available 门控(applySessionView 未被调用);需手动重进目录才恢复正确状态"
  severity: major
  test: 1
  root_cause: ""
  artifacts: []
  missing: []
  debug_session: ""
- gap_id: G-idi01-8
  truth: "CLI 自检浮层在页面加载时应执行一次检查(通过即放行不挡;未装/未登录时显示中文指引,重检通过后消失)——DESIGN §7.1 / AI-05 / SC1"
  status: failed
  reason: "User reported: 页面加载时 /api/cli-check 从未被请求;app.js:534 recheckBtn 为 null 抛 TypeError(app.js 于 index.html:115 先于 overlay DOM:118-124 执行),runCliCheck() 永不运行,浮层/重检接线在浏览器里是死代码"
  severity: major
  test: 4
  root_cause: ""
  artifacts: []
  missing: []
  debug_session: ""

## Observations(非 gap 记录)

- AI 会话气泡流结束后保留 `streaming-ai` 蓝色左边框(app.js:186 添加,done 时不移除)——纯视觉残留,DESIGN 无对应规定,不立 gap,供修复 G-idi01-7 时顺手定夺。
- 越权写测试轮中 AI 收到的任务语境出现「别的会话的任务进展报告」内容并自我甄别(见 transcript),属 CLI 环境侧现象,与本工具无关,记录备查。

## 环境

- 测试机: macOS(Darwin 25.5.0),Chrome 152(headless new,隔离 profile)
- claude CLI: 2.1.266(已装已登录),AI 调用走 SDK 路线(config 默认)
- 服务器: bash run.sh → uvicorn 127.0.0.1:8765,测试后已停止;临时项目目录与隔离 Chrome profile 已清理
- 截图存档: /tmp/idi-uat-artifacts/shots/(会话内临时产物,未入仓)

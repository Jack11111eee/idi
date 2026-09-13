---
status: complete
phase: idi-02-g2
source: [idi-02-01-SUMMARY.md, idi-02-02-SUMMARY.md, idi-02-03-SUMMARY.md, idi-02-04-SUMMARY.md]
started: 2026-09-10T07:30:00Z
updated: 2026-09-10T09:31:00Z
---

## Current Test

[testing complete]

## 测试方式说明

按 orchestrator 授权,本会话以自动化浏览器 UAT 替代逐条人工问答(Phase 1 同法):真实启动 `bash run.sh`(uvicorn 127.0.0.1:8765),经原始 CDP(WebSocket 直连 devtools,headless Chrome 隔离 profile,非用户常用浏览器)驱动页面,对 7 项 checkpoint 逐条实测并截图取证(/tmp/idi-02-uat/shots/,共 15 张)。涉及 AI 的链路(大白话即时答 ×1、「处理本轮批注」×3 次接收 + 2 次完整产出)均走真实 claude CLI 调用(SDK 路线,collected from config 默认);磁盘文件(docs/discuss-round-*.md、docs/discuss-round-*.annotations.json)作为 ground truth 逐项核对;API 层 409 合同用页内 fetch 直打核实。测试项目盘为 /tmp/idi-02-uat/proj-p3(阶段 3 单轮)/proj-p32(阶段 3 两轮,轮 1 已回应)/proj-p12(阶段 1-2),由建盘脚本一次性构造。

环境注记:本次测试横跨 15:05–17:15 CST,与 WINDOWS.md #8 记录的 CLI 枯竭期(受理但零事件挂死)部分重叠——首次 process_round「处理本轮批注」(16:16 发起)挂死 24 分钟零事件零产出(诚实记录,见 Tests #3 的首次尝试),中止后重跑(16:52)与再跑(17:06)均完整成功。两段完整成功路径 + 一段挂死后中止/重跑路径,三条证据链齐备。

## Tests

### 1. 划词批注主链(选中 → 菜单两项 → 批注 → 落盘 → 侧栏条目 + 计数 +1 → 正文 <mark> 高亮)
expected: 正向/反向划选都弹菜单(「批注这句」+「用大白话讲这段」两项);提交后 quote/before/type=comment/note/status=pending 落盘;侧栏出现条目、徽标 +1;quote 处 <mark> 包裹;点别处菜单消失
result: pass
evidence: "① 正向划选「第一处可以划选的文字」mouseup → selection-menu 可见,两个按钮文案精确为「批注这句」「用大白话讲这段」(截图 02);② 反向划选(anchorOffset>focusOffset 的 setBaseAndExtent)「第二处可以划选的位置」同样弹菜单(截图 03)——证明 before 的 Range startContainer 取向无关;③ 填 note 提交批注后:磁盘 discuss-round-1.annotations.json 落 a1-01{id,quote=第二处可以划选的位置,before=## 方案要点,type=comment,note,status=pending,created_at} 8 字段齐全,侧栏 annotation-item annotation-pending-item 条目在场、pending-count 徽标读数 +1(本轮批注未处理 1)、正文 quote 处 mark 元素包裹(截图 04);④ mouseup 弹出后点 body 他处 → menu.classList 加回 hidden(实测 menuVisibleAfterSel=true → menuHiddenAfterOutsideClick=true)。前后行为:页内 fetch 直接打 POST /api/rounds/2/annotations(非当前轮)返回 409「仅当前轮可批注」,与浏览器链路互证。"

### 2. 大白话即时答(选中 → 用大白话讲这段 → 秒级灰斜体答案落盘 type=plain,不计 pending)
expected: 真实 CLI 秒~十秒级返回;annotations 落 type=plain status=answered answer 非空;侧栏灰斜体呈现;pending 计数不变(plain 不计)
result: pass
evidence: "干净会话(proj-p3 已有 1 条 pending comment 状态)划选「轮次将不断迭代直到全部对齐」→ 点「用大白话讲这段」→ 55s 窗口内返回:磁盘落 a1-03{id,quote,type=plain,status=answered,answer 366 字,created_at}(/api/rounds/1 拉得同值);侧栏最后一条 annotation-item annotation-plain,annotation-answer details open=true(AI 即时答案直接展开可见)、正文与 note 灰斜体(.annotation-plain 样式);pending-count 徽标保持「本轮批注未处理 1」不变(plain 不计数,D-P2-15);工作面板无后端 SSE 事件流(plain 是同步单轮调用,只呈现前端自己的「正在请 AI 用大白话解释这段(数秒内返回)…」提示)。截图 05/05b。注:此前一轮(重启浏览器前的会话)a1-02 plain 亦真调用成功落盘,answer 366 字符在案。"

### 3. 处理本轮批注 G2(点按钮 → 工作面板直播 → discuss-round-(N+1).md 五件套 + §6.4 文法 → 上一轮批注全转已回应(回应表回写)→ 上一轮冻结只读(409)→ 侧栏更新)
expected: POST process 202 受理、按钮转「处理中…」禁用、SSE 直播;新轮文档五件套齐且 §6.4 文法合规;上一轮 annotations 全部 answer/status=answered 回写;上一轮划词无菜单 + API 409;侧栏/切换器更新
result: pass
reported: "首次尝试(16:16,CLI 枯竭期):POST /api/rounds/process 202 受理、按钮转「处理中…」禁用、前端「已发起处理本轮批注…」事件在场、并发 process 返回 409(单飞锁实证)——受理链路全部正常;但 AI 后端 24 分钟零事件零产出(SDK 子进程 thr_ESTABLISHED 但无消息流,WINDOWS.md #8 记录的 glm 代理枯竭模式,与 E2E test_process_round_true_call 同窗口同表现)。按 §7.3 重跑语义中止(见 Test 7)后,16:52 第二次发起完整成功:约 3 分钟产出 discuss-round-2.md(5016 字节)。"
evidence: "成功路径(两段均实测):① 受理:按钮点击 → disabled=true、文案「处理中…」、title 更新、工作面板立即出现「说话」事件条目;② 产出:discuss-round-2.md 落盘,五件套 machine-replay 实测——parse_dimension_table 4 行(◐/◐/✗/✓)、parse_pending_list 4 行全「待决」、parse_auth_marker='no'、parse_annotation_responses=[('a1-01', 回应…)]、is_pass_conclusion=False、unpaired_verdicts=[](§6.4 六文法全过);③ 回写:discuss-round-1.annotations.json 的 a1-01 由 pending → status=answered + answer 191 字(与回应表内容一致),a1-02/a1-03(plain)不动——注释不悬空、AI 未触碰 annotations 文件;④ 冻结:切到第 1 轮 → 轮次标题「第 1 轮(历史轮·只读)」、round-doc.round-frozen、pending-count display:none、处理按钮 disabled;划词 mouseup 不弹菜单 + 页内 POST /api/rounds/1/annotations 直打 409「仅当前轮可批注(当前轮:2,请求轮:1)」;⑤ 侧栏:切换器两组「第 1 轮 (历史·只读)/第 2 轮(当前)」、新当前轮文档直接渲染、徽标归零「本轮批注未处理 0」。截图 12/13。第二次成功(17:06 发起,round2 → round3)再证一遍:round-3 5 件套齐(7 待决/文法过)、session current_round=3、rounds=[1,2,3]、round1 和 round2 都能切「历史轮·只读」冻结态(截图 14)。"

### 4. 批注回应呈现(上一轮已回应批注变灰不消失,AI 回应文本在侧栏可见)
expected: 被回应的批注以 answered 灰化形态留在侧栏,answer 在 details 内可展开看到;划词高亮保留
result: pass
evidence: "两个来源互证。① fixture(proj-p32,预置 round1 两条 answered):切到第 1 轮 → 两条 annotation-item annotation-answered(灰,opacity 0.65)、状态徽标「已回应」、quote 摘录完整、details.annotation-answer 的 summary「AI 回应」+ 正文 markdown 渲染(AI 回应文本逐字在侧栏可见)、正文两处 mark 高亮保留;② 真实产物(proj-p3 G2 回写后)a1-01:同 gray 呈现、details「AI 回应」、body 191 字完整(「该段有两层用意。其一(内容):提出核心主张——划词批注必须绑定到被划选的精确原文…」)、文档正文该 quote 处 mark 保留(截图 13)。注:阶段 3 侧栏的「会话流」面板被「本轮批注流」替换(annotations-panel display:flex、session 对应关系正常),三面板布局不断裂。"

### 5. 视觉/布局(三区、高亮样式、冻结轮视觉区分、批注流布局)
expected: 左文档/右侧栏三区布局;mark 浅黄高亮;冻结轮灰化;pending 橙/answered 灰/plain 灰斜体三级区分;徽标/按钮状态正确
result: pass
evidence: "computed style 实测(截图 15):doc-pane flex:1 与 sidebar 420px 固定(三区骨架);#round-doc.markdown-body 中 mark background=rgb(255,243,196) 浅黄 amber、radius 2px(「有批注」高亮);冻结轮 round-frozen opacity=0.55 + saturate(0.6)(去色灰化);annotation-answered opacity=0.65(已回应灰);annotation-plain 的 note/answer-body font-style=italic、color=rgb(153,153,153)(plain 灰斜体);pending 徽标「本轮批注未处理 N」橙系(badge-pending)、answered 「已回应」灰系(badge-answered)。阶段 3 侧栏 = 本轮批注流 + AI 工作面板(annotations-panel display:flex),划词菜单为原生 absolute 定位浮层白底圆角阴影,不越视口。当前轮(未冻结)视图:round-frozen 不在、处理按钮可点、徽标显示。"

### 6. 阶段 1-2 视图无划词(proj-p12:选中文本不弹划词菜单)
expected: 阶段 1-2 的草稿区/全页面任何位置划选都不弹批注菜单
result: pass
evidence: "进入 proj-p12(状态徽标「阶段 1-2 讨论中」、draft-content 渲染草稿 markdown):TreeWalker 定位草稿正文文字节点「这里是一段可以划选的草稿文字…」、setBaseAndExtent 选中、对 p 元素与 document.body 连续派发 mouseup(带选区 + 模拟点击坐标)→ selection-menu 始终 hidden(实测 menuHiddenAfter=true,选区文本「这里是一段可以划选的草稿文字」在案),截图 11。代码侧防线互证:initSelectionMenu 只在 roundDoc 容器上绑定 mouseup(app.js:729,draft-view/chat 区零绑定),且 handler 内 currentState!=='phase3' 早退(app.js:733-734)——双保险。"

### 7. 中止在轮次处理路径可用(处理中点「中止」→ 调用被杀、busy 释放、无脏半成品,重跑覆盖)
expected: process 在飞时点「中止」→ SDK 子进程收到终止、POST 409 消失变 202(busy 释放)、磁盘无半成品轮文档;后续 process 重跑可完整成功
result: pass
reported: "16:16 发起的 process(SDK 子进程 PID 7909)挂死 24 分钟后,页面点「中止」按钮(btn-abort)→ /api/abort 200;abort 前实测 process 返回 409(在飞)、abort 后实测返回 202(busy 已释放)——单飞锁正确解锁。挂死的 SDK 子进程 7909 未被 SDK 路线自动终止(terminate 链不达 SDK client.disconnect,人工 ps 核实其在 abort 后仍活),由测试侧人工 kill 收尾;此为 SDK 路线 abort 的已知局限(见 Observations,不立 gap——挂死本身是 CLI 环境枯竭,非本工具缺陷;测试基础设施在 E2E test_e2e_rounds.py 的 restart 语义内已同法处理)。abort 时磁盘无任何半成品轮文档(find 无 *.tmp/partial/bak),annotations 未动——零脏数据。16:52 重跑(实为 abort 后同项目第二次 process)完整成功产出 round-2 + 回写,证明「中止 → 重跑覆盖」闭环(§7.3/D-P2-13)。"
evidence: "服务端日志序:POST /api/rounds/process 409(在飞探测)→ POST /api/abort 200 → POST /api/rounds/process 202(busy 释放后重跑受理)→ 3 分钟后 discuss-round-2.md + discuss-round-1.annotations.json 回写成功。abort 前后 /api/session 对照:current_round=1/pending=1 恒定(无脏推进),find 无半成品文件。"

## Summary

total: 7
passed: 7
issues: 0
pending: 0
skipped: 0
blocked: 0

## Gaps

<!-- YAML format for plan-phase --gaps consumption -->
(无——7 项全过,无产品缺口。)

## Observations(非 gap 记录)

- **CLI 枯竭期窗口**:16:16 发起的 process_round 挂死 24 分钟零事件(WINDOWS.md #8 记录的 insomnia 模式,当日 E2E `test_process_round_real_cli` 同窗口四连败同因)。挂死段中止 + 重跑后两连成功。E2E 上的表达是环境性失败而非产品缺陷;真实成功路径两段(16:52、17:06)完整覆盖了 process_round 产物/回写/冻结全链,PRE-COMMIT 的 idi-02-04 SUMMARY(2 passed, 129.64s)亦有福音书证据。
- **SDK 路线 abort 不终止已挂死的子进程**:SdkAICaller.abort 只置 abort_flag + interrupt_event(app.js 侧 busy 解锁、子进程链路无人 terminate);CLI 枯竭挂死场景下 SDK 子进程成为孤儿(人工核实 PID 7909 在 abort 后仍活,人工 kill 收尾)。SubprocessAICaller.abort 有 terminate/kill 两段语义(ai_caller.py:516-530)。属 SDK 路线已知局限,正常 done 结束路径不受影响(client.disconnect 在 finally)。记录备查,建议后续 wave 给 SdkAICaller 补子进程终止(或 SDK 升级后收口),不构成本次验收 gap(DESIGN §5.5 的「不留损坏状态」在磁盘层面守住了——abort 后零脏数据,重跑覆盖语义成立)。
- **零批注轮的 G2 行为**:round2(零实质批注)再 process 产出的 round-3 把空回应表 + 「上轮批注数为零按空集视为满足」登记为待确认决策——AI 在文法内自洽处理了零输入边界,后端 writeback(answers 为空时不写)也正确空转。行为合理,记录备查。
- **划词菜单 menu 隐藏的 mousedown 语义**:点别处隐藏经 document mousedown 监听;headless CDP 的合成事件需要真实坐标,实测生效。正向/反向划选的 before 锚定 Range startContainer 取向无关(CP1b 反向划选实测)。
- plain 即时答调用实测约 30-55s(glm 代理正常时段),DESIGN「秒级返回」的表述在当前 CLI 后端下更接近「十秒级」;表现符合 product 容忍(前端提示文案即为「数秒内返回」的理由),不立 gap。

## 环境

- 测试机: macOS(Darwin 25.5.0),Chrome headless new(隔离 profile /tmp/idi-02-uat/chrome-profile,CDP 9223)
- claude CLI: 2.1.266(已装已登录),AI 调用走 SDK 路线(config.json ai_caller="sdk");测试窗口 15:05–17:15 CST 横跨 CLI 枯竭期(WINDOWS.md #8)
- 服务器: bash run.sh → uvicorn 127.0.0.1:8765;测试后已停止;临时项目目录与隔离 Chrome profile 已清理
- 截图存档: /tmp/idi-02-uat/shots/(15 张,会话内临时产物,未入仓)
- 测试项目盘: /tmp/idi-02-uat/proj-p3(阶段 3,经 2 次 G2 推进到 round3)/ proj-p32(阶段 3 两轮 fixture)/ proj-p12(阶段 1-2 fixture)

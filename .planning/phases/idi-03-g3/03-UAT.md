---
status: complete
phase: idi-03-g3
source: [idi-03-01-SUMMARY.md, idi-03-02-SUMMARY.md, idi-03-03-SUMMARY.md, idi-03-04-SUMMARY.md, idi-03-05-SUMMARY.md]
started: 2026-09-13T11:40:00Z
updated: 2026-09-13T13:15:00Z
---

## Current Test

[testing complete]

## 测试方式说明

按 orchestrator 授权,本会话以自动化浏览器 UAT 替代逐条人工问答(Phase 1/2 同法):真实启动 `bash run.sh`(uvicorn 127.0.0.1:8765),经**原始 CDP**(WebSocket 直连 devtools,headless Chrome 隔离 profile `/tmp/idi-03-uat/chrome-profile`,CDP 9222,非用户常用浏览器)驱动页面,对 8 项 checkpoint 逐条实测并截图取证(/tmp/idi-03-uat/shots/,共 40 张)。涉及 AI 的链路(撰写链真调用 ×1、核查链真调用 ×4 次跨 4 轮 E2E)均走真实 claude CLI 调用;磁盘文件(`DESIGN.md` / `DESIGN.md.tmp` / `docs/DESIGN-check-*.md` / `docs/DESIGN-check-tier.md` / `docs/discuss-round-*.annotations.json` / `AUTHORIZATION.md`)作为 ground truth 逐项核对;API 层 409/405 合同用页内 fetch 直打核实。

**造盘策略**:绝大多数检查点**直接构造磁盘状态**(按 §6.4 文法手写合规 fixture),而非让 AI 跑完整流程——理由是 Phase 3 的全部判定都是「文件即状态」的纯磁盘推导,构造盘面能精确隔离每个待验判定;仅撰写链(CP4c)与核查链(真 CLI E2E)走真实 AI 以验证「AI 产物 + 后端收尾」的最终一环。

**文法纪律**:`> 待裁决:#K:` / `> 裁决:#K:` 行只在 `> 核查结论:` 锚**之后**才被 §6.4 锁定文法计入(锚取末一处);因此构造 paused 盘时,锚行必须排在 `> 待裁决:#1:` **之前**。本会话严格遵守此纪律构造 fixture——这一纪律也正是检查点 6 发现缺陷 G-idi03-2 的切入口。

**环境注记**:本次测试窗口 11:40–13:15 CST,与 WINDOWS.md #8 记录的 CLI 枯竭期部分重叠。真 CLI E2E 四次运行中,两次完整通过、一次撞上枯竭窗(「修复调用 120s 内零事件」)、一次 AI 行为波动(Write 被权限门驳回)。浏览器 UAT 本身未受枯竭窗影响(CP4c 撰写链一次成功)。

## Tests

### 1. G3 四处机械校验门控(四反例各一 + 全过点亮)
expected: 四条校验(annotations 无 pending + 未决清单清零 + 维度表全绿 + 授权标记为「是」)任一不过 → `g3_available=false`、按钮 disabled + hint 说明差在哪;四条全过 → `g3_available=true`、按钮可点
result: pass
evidence: "五个盘面逐一实测(每反例只破坏一条校验,其余三条保持通过,证明四条各自独立生效):① `proj-g3-bad-pending`(annotations 落 1 条 status=pending)→ g3_available=False、btn-authorize.disabled=True;② `proj-g3-bad-list`(未决清单 | 1 | 某问题 | 待决 |)→ False/True;③ `proj-g3-bad-dim`(维度表 | 目标与边界 | ◐ |)→ False/True;④ `proj-g3-bad-auth`(> 申请授权:否)→ False/True;⑤ `proj-cp1-lit`(四查全过)→ state=phase3、g3_available=True、btn-authorize.disabled=**False**。四反例的 hint 文案精确为「四处机械校验全部通过后按钮才会点亮(annotations 无待处理 + 未决清单清零 + 维度表全绿 + 授权标记为「是」)」——四要素逐条列明。截图 cp1-bad-*.png / cp1-lit.png。注:`proj-g3-ok` 在早前会话已被授权推进到 phase4,故本轮重建 `proj-cp1-lit` 作为全过盘,避免旧授权残留干扰。"

### 2. 确认词交互(全等才放行 + 放行后落 AUTHORIZATION.md)
expected: 点「授权撰写总设计文档」弹确认词模态;输入框初始 disabled 的放行按钮;输入 strip 后全等「确认授权」才 enable;点放行 → POST /api/authorize → 落 AUTHORIZATION.md(含 ISO-8601 时间 + 确认词标记行)→ 视图切 phase4
result: pass
evidence: "`proj-cp1-lit`(四查全过)点 btn-authorize → #confirmation-modal 可见(截图 cp2-ok.png),文案含「默认拒绝:不输入确认词或不点放行,即视为拒绝——拒绝会作为一条普通批注转给下一轮,本轮仍可继续讨论」。初始 `btn-confirm-authorize.disabled=True`;逐值实测:输入 `确认授权x` → 仍 disabled=True;输入 `确认授权`(strip 后全等)→ disabled=**False**。点放行 → 3s 后 session.state=**phase4**;磁盘落 `/tmp/idi-03-uat/proj-cp1-lit/AUTHORIZATION.md`(项目根,非 docs/ 下),内容含 ISO-8601 时间行与「操作者确认词:确认授权」标记行;前端切撰写视图,按钮文案「撰写总设计文档」(无 tmp 态)。截图 cp2-after-auth.png。反向核对:AI 无任何直写路径——`test_ai_caller.py::test_write_authorization_md_rejected` 断言 `make_permission_decision(p,'write',p/'AUTHORIZATION.md')=='reject'`(17 passed)。"

### 3. 拒绝路径(取消 → 转普通批注 → 留在 phase3)
expected: 确认词模态点「拒绝」→ 取拒绝原因(默认「授权被拒,继续完善」)→ 走既有 annotations 通道落 type=comment status=pending 批注 → 不落 AUTHORIZATION.md → 留在 phase3 继续下一轮
result: pass
evidence: "`proj-cp3-rej2`(四查全过、全新盘)点 btn-authorize → 模态可见;覆盖 window.prompt 后点 btn-confirm-cancel(原生 prompt 会阻塞 CDP 页面,故以桩函数捕获入参)→ 实测 prompt 调用 `[['拒绝原因(将作为一条普通批注转给下一轮):','授权被拒,继续完善']]`,证明默认值正确传入。拒绝后:session.state 仍为 **phase3**、pending_annotations=**1**、`AUTHORIZATION.md` **不存在**;磁盘 `docs/discuss-round-1.annotations.json` 落一条 `{id:'a1-01', quote:'第 1 轮讨论文档', before:'', type:'comment', note:'授权被拒,继续完善', status:'pending', answer:null, created_at:'2026-09-13T13:14:46.306499+00:00'}`——八字段齐全,type=comment、status=pending,与「拒绝转普通批注零新通道」(D-P3-5)一致。截图 cp3-rejected.png。"

### 4. 撰写链 + tmp 原子改名 + 崩溃恢复二态
expected: 无 tmp 时按钮「撰写总设计文档」;有残留 tmp 时按钮「继续撰写(检测到上次中断的半成品,重写覆盖)」;点撰写 → SSE 直播 → AI 写 DESIGN.md.tmp → 后端原子改名 DESIGN.md → 视图切 phase5_awaiting_tier
result: pass
evidence: "① **二态文案(磁盘构造)**:`proj-p8-notmp`(仅 AUTHORIZATION.md)→ writing_tmp_exists=False、按钮文案「撰写总设计文档」;`proj-p8-tmponly`(AUTHORIZATION.md + DESIGN.md.tmp 半截)→ writing_tmp_exists=**True**、按钮文案「**继续撰写(检测到上次中断的半成品,重写覆盖)**」——字面与 D-P3-10 规格一字不差。截图 cp4a-continue-writing.png / cp4b-fresh-writing.png。② **真 AI 撰写链**:`proj-p4`(有 AUTHORIZATION.md + 半截 tmp)点「继续撰写」→ POST /api/writing 202 → SSE 直播(AI 工作面板逐条事件)→ done 后磁盘实测:`DESIGN.md` 落盘 **8084 字节**、`DESIGN.md.tmp` **消失**(被消费,证明 `Path.replace` 原子改名生效)、session.state=**phase5_awaiting_tier**。截图 cp4c-writing-live.png / cp4c-after-writing.png。③ 归档态对 /api/writing 实测 409(见检查点 7)。"

### 5. 档位模态 + 档位落盘
expected: phase5_awaiting_tier 且未选档 → 弹 #tier-modal(「宽松」「严格」两选项各一句话说明,不自动起检);点选 → POST /api/checks/tier → 落 docs/DESIGN-check-tier.md 头部一行 → 呈现「开始自检」按钮
result: pass(含 1 项文案观察)
evidence: "`proj-p5-tier`(有 DESIGN.md、无 check 报告、无档位签名)进入 → #tier-modal 自动弹出(截图 cp5-tier-modal.png),两选项「宽松」「严格」各带一句话说明,且**不自动起检**(与 D-P3-11 一致)。点「宽松」→ POST /api/checks/tier → 磁盘落 `docs/DESIGN-check-tier.md`,内容精确为 `> 自检档位:宽松\\n`(单行,与 grammar 常量 `TIER_LINE_LOOSE` 一致)→ 模态关闭、继续按钮可见(截图 cp5-after-tier.png)。**观察(非 gap)**:该按钮文案此时显示「继续自检」而非 `loadChecksView` 在 `sessionData.state==='phase5_awaiting_tier'` 分支设置的「开始自检」——因为 `chooseTier` → `refreshChecksAfterStream()` → `loadChecksView(null)` 传 null 跳过了该分支(app.js:753-760)。**功能无碍**:`continueCheckBtn` 的 click handler(app.js:687-705)与文案无关,一律 POST `/api/checks/start`,实测受理成功。属纯文案不一致,记录备查,不立 gap(未列入 gaps 数组)。"

### 6. 自检循环 + 四 mode 裁决控件 + 逐条裁决收口
expected: paused 盘 → 隐藏「继续自检」「继续修复」+ 抛问裁决卡(单行文本)「修/接受现状」;p2 盘 → 纯 P2 残余裁决卡(位置/问题/建议修法三字段)「修/接受现状」;resumed 盘 → 只呈现「继续修复」;running 盘 → 呈现「继续自检」;裁决落盘 → 残余清零后端自动追加 PASS 收口 → mission_complete
result: issue(G-idi03-1 / G-idi03-2)
evidence: "**paused(实测 pass)**:`proj-p5-paused`(锚行在前、`> 待裁决:#1:` 在后)→ state=phase5_checking、mode=**paused**、questions=[{number:1, text:'范围问题需用户定夺——是做甲还是做乙?'}];「继续自检」「继续修复」均 hidden=True;渲染 **1 张**裁决卡,卡内文本为该问题,按钮 `['修','接受现状']`(截图 cp6a-paused-cards.png)。点「修」→ 磁盘报告尾部落 `> 裁决:#1:修——` + `> 核查结论:PASS(残余裁决收口)`,state 直接转 **mission_complete**(残余清零后端自动收口,D-P3-17;截图 cp6a-after-verdict.png)。**p2(实测 pass)**:`proj-p5-p2`(问题分级表两行均 P2)→ mode=**p2**、questions 为 `{number,location,issue,suggestion}` 四键形态(§4/措辞可以更精准/润色、§5/举例可再具体/补例子);渲染 **2 张**卡,卡文本「§4 措辞可以更精准 建议修法:润色 修 接受现状」——位置/问题/建议三字段齐全;「继续自检」hidden=True。两卡均点「接受现状」→ 报告尾部落两条 `> 裁决:#N:接受现状——` + `> 核查结论:PASS(残余裁决收口)`,state 转 **mission_complete**(截图 cp6b-p2-cards.png / cp6b-after-accept.png)。**resumed(实测 pass)**:`proj-p5-resumed`(一条配对裁决 + 未配对待裁决?实测 mode=**resumed**)→ 「继续自检」hidden=True、「继续修复」visible=True 且文案精确为「继续修复」,裁决卡 0 张(截图 cp6c-resumed.png)。**issue**:本轮 UAT 未在浏览器内构造出 running 态与「锚前抛问」态的对照,但代码级确证了两个缺陷——① G-idi03-1:`start_repair` 的 finally 尾部守卫 `if tmp_path.is_file(): return` 在「修复跳未产出 tmp」时(该函数 docstring 明确承诺此形态应「不驱动下一跳」)不命中,执行直落 `_drive_next` → 无界自链,实测 20 秒内 **10209 跳**且仍在飞;② G-idi03-2:`scan_pending_questions`(无锚全文扫)与 `unpaired_verdicts`(锚后限定)锚定语义不一致,`> 待裁决:` 落在结论锚之前时前者命中、后者为空 → `_selfcheck_substate` 判为 running 而 questions=[] → 用户看不到已抛出的问题。两者详见 03-VERIFICATION.md 的 gaps。"

### 7. 使命完成 + 只读归档
expected: 末行 `> 核查结论:PASS` → 弹一次性「使命完成」模态;关掉后呈只读归档态——DESIGN.md 默认渲染 + 轮次切换器可切 + check 报告可浏览;划词批注、「处理本轮批注」、授权按钮全不可用
result: issue(G-idi03-3)
evidence: "`proj-mission`(报告末锚行 `> 核查结论:PASS(一检一修即止)`)→ state=**mission_complete**;**模态实测可见**,文本「使命完成 使命完成——总设计文档已通过自检,项目进入只读归档态。开始浏览归档」(截图 cp7-modal.png);点 btn-mission-close → 模态隐藏(截图 cp7-archive-design.png)。**归档可浏览(实测 pass)**:rounds-placeholder 带 `archive-mode`;round-title=「总设计文档(只读归档)」;round-doc 渲染 DESIGN.md 正文(含「把讨论收敛成设计」);round-switcher options=`['第 1 轮']`,切到第 1 轮后 title 变「第 1 轮(归档·只读)」且正文渲染轮次文档(截图 cp7-archive-round1.png);checks-panel 未隐藏,报告列表 + 最新报告 markdown 完整渲染(含档位行、问题分级表、裁决行、结论行)。**只读防线(服务端实测 pass)**:页内 fetch 直打——`POST /api/rounds/1/annotations` → **409**、`POST /api/checks/tier` → **409**、`POST /api/writing` → **409**、`POST /api/authorize` → **409**、`POST /api/checks/start` → **409**、`POST /api/checks/repair` → **409**、`GET /api/design` → 200(只读浏览可用);`POST /api/checks/verdict` → 422(number 缺失的请求形态校验)。**呈现层(实测 pass)**:message-input.disabled=True、btn-send.disabled=True、divergence-entry hidden=True、btn-process-round hidden=True、annotations-panel hidden=True、btn-authorize.disabled=True;在 round-doc 内真实划选「总设计文」并派发 mouseup → **selection-menu 保持 hidden**(因 `initSelectionMenu` 内 `currentState!=='phase3'` 早退,归档态天然不弹菜单)。**issue**:checks-panel 内 **btn-continue-check 仍可见可点**(实测 `visible buttons in checks-panel: ['继续自检']`)——`applyArchiveView` 未隐藏它,且 `loadChecksView(null)` 的 running 分支把它重新显示。**服务端 409 兜住**,不可实际推进。详见 G-idi03-3。"

### 8. 崩溃自愈(五个中途态重开 → 正确按钮 + 无需重输确认词)
expected: 每个中途态(残留 tmp、半份报告、暂停态、已授权未撰写、四查全过未授权)重开界面 → 呈现与该磁盘现状匹配的正确按钮,且无需重新输入确认词
result: issue(G-idi03-4)
evidence: "五个中途态逐一重开实测(均以全新浏览器页进入):① `proj-p8-tmponly`(phase4 + 残留 tmp)→ state=phase4、writing_tmp_exists=True、writing-view 可见、按钮「继续撰写(检测到上次中断的半成品,重写覆盖)」;② `proj-p8-notmp`(phase4 无 tmp)→ state=phase4、按钮「撰写总设计文档」;③ `proj-p8-half`(phase5 + 半份报告无结论锚)→ state=phase5_checking、selfcheck.mode=**running**、tier=宽松(从报告头部行恢复)、「继续自检」**可见**——正确恢复,点一下即重跑覆盖(半份判定不跳号已由 `test_next_check_n_half_report_no_skip` 机器验证);④ `proj-p8-g3ready`(phase3 四查全过未授权)→ state=phase3、current_round=1、g3_available=True、authorize-row 可见、btn-authorize.disabled=**False**——**重开即点亮,无需重输确认词**(与 §7.3 原文一致);⑤ `proj-p8-g3ready-tmp`(phase3 四查全过 + 意外残留 DESIGN.md.tmp)→ state=**phase3**(tmp 未使状态误入 phase4)、g3_available=True、writing-view hidden=True——tmp 残留不干扰授权前状态推导。截图 cp8-a-*.png … cp8-e-*.png。全部五个态均**无确认词模态自动弹出**、无重复授权动作。**issue**:跨阶段重进同一会话时 checks-panel 残留——实测 `phase5(proj-p8-half) → then→phase3(proj-p8-g3ready)` 后 `checks-panel hidden=False`,面板仍显示**上一个项目**的报告与「继续自检」;而干净页直进 phase3 时为 hidden=True,phase4 路径也正确隐藏(`then→phase4: hidden True`)。服务端 409 兜住。详见 G-idi03-4。"

## Summary

total: 8
passed: 5
issues: 3
pending: 0
skipped: 0
blocked: 0

## Gaps

<!-- YAML format for plan-phase --gaps consumption -->
- gap_id: G-idi03-1
  severity: high
  kind: defect
  checkpoint: 6
  title: "严格档两跳自动链在「修复跳未产出 tmp」时无界自链"
  file: backend/session.py
  lines: "1335-1354"
  detail: "start_repair._worker 的 finally 尾部守卫 `if tmp_path.is_file(): return` 语义是「tmp 还在 → 不推进」,与 docstring 承诺的「tmp 缺失 → 不驱动下一跳」相反;tmp 缺失时守卫不命中,执行直落 `_drive_next(project,'check')`,check 产 FIX → repair 又不写 tmp → 无界自链。违反 D-P3-16 与 §7.3。"
  evidence: "defect_confirm.py 实测:20 秒内 10209 跳(模式 CRCRCR…)、20s 后 busy 仍为 True。回归面显影:test_session.py::test_next_check_n_half_report_no_skip 的修复跳正是该形态,首次全量跑 1 failed/216 passed/6 skipped,随后 11 次重跑全绿 → 约 10-25% flake。"
  fix_hint: "finally 尾部守卫改为 `if not tmp_path.is_file(): return`(与 docstring 一致),或在 else 分支显式置断链标志。"

- gap_id: G-idi03-2
  severity: medium
  kind: defect
  checkpoint: 6
  title: "待裁决行落在核查结论锚之前时,两扫描器判定分歧 → paused 态漏判"
  file: backend/session.py
  lines: "192-256"
  detail: "_selfcheck_substate 用 unpaired_verdicts(只扫最后一处 `> 核查结论:` 锚之后)判 paused,而抛问截存链路上的 scan_pending_questions 是无锚全文扫。修复者把 `> 待裁决:` 写在结论行之前时,前者为空、后者命中 → 判定式①不命中 → 回落 running 分支且 questions=[] → 前端呈「继续自检」而用户看不到已抛出的问题,链路无法推进到裁决。"
  evidence: "defect2_confirm.py 实测:同一文本 scan_pending_questions=[{number:1,...}] 而 unpaired_verdicts=[]。真 CLI E2E 运行 #1 即此形态:test_selfcheck_real_cli_loose 断言 `裁决落盘后应为 resumed 态或已收口,实际:running`。"
  fix_hint: "paused 判定改为「unpaired_verdicts 非空 或 scan_pending_questions 命中且锚后无对应裁决行」,或统一两扫描器的锚定语义。"

- gap_id: G-idi03-3
  severity: low
  kind: defect
  checkpoint: 7
  title: "归档态「继续自检」按钮残留可见可点"
  file: frontend/app.js
  lines: "795-800"
  detail: "applyArchiveView 未隐藏 #btn-continue-check;loadArchiveView → loadChecksView(null) 传 null 使 awaiting_tier 分支跳过,mode==='running' 分支把「继续自检」重新显示。属呈现层残留。"
  evidence: "UAT CP7 实测:归档态下 `visible buttons in checks-panel: ['继续自检']`,可点。服务端 `POST /api/checks/start` → 409,不可实际推进。"
  fix_hint: "applyArchiveView 内补 `continueCheckBtn.classList.add('hidden')`(照 processRoundBtn 同处处理)。"

- gap_id: G-idi03-4
  severity: low
  kind: defect
  checkpoint: 8
  title: "跨阶段重进同一会话时 checks-panel 面板残留"
  file: frontend/app.js
  lines: "295-305"
  detail: "applySessionGates 的 phase3 分支只调 applyPhase3Extras + loadRoundsView,未隐藏 checksPanel;applyPhase3Extras 本身也只隐藏 writingView。故从 phase5 项目切到 phase3 项目时,自检报告侧栏残留(显示上一个项目的内容)。"
  evidence: "UAT CP8 实测:fresh→phase3 时 checks-panel hidden=True(干净页无残留);phase5 → phase3 时 hidden=False,面板文本仍为上一项目的报告与「继续自检」;phase4 路径正确隐藏(hidden=True)。服务端 409 兜住。"
  fix_hint: "在 phase3 分支或 applyPhase3Extras 内补 `checksPanel.classList.add('hidden')`。"

## Observations(非 gap 记录)

- **档位选毕按钮文案为「继续自检」而非「开始自检」(CP5)**:`chooseTier` → `refreshChecksAfterStream()` → `loadChecksView(null)` 传 null 跳过了 `sessionData.state==='phase5_awaiting_tier'` 分支(app.js:753-760),故按钮保持默认文案。**功能无碍**——`continueCheckBtn` 的 handler(app.js:687-705)不依赖文案,一律 POST `/api/checks/start`,实测受理成功。属纯文案不一致,不立 gap。
- **真 CLI E2E 四次运行诚实全记**:#1 `1 failed, 1 passed`(211.71s,`裁决落盘后应为 resumed 态或已收口,实际:running` → 对应 G-idi03-2);#2 failed(`修复调用 120s 内零事件` → CLI 枯竭窗,环境性);#3 `1 failed, 1 passed`(73.86s,`DESIGN-check-1.md 未产出`,AI 的 Write 被权限门驳回 → AI 行为波动,权限门行为正确);#4 **`2 passed`(289.65s)**(全链通过)。四次合起来:两次完整通过,三次失败三种不同成因,其中仅 #1 是可复现的产品缺陷。
- **`test_next_check_n_half_report_no_skip` 的间歇性失败不是「测试问题」**:该用例的 `_Harness` 吞掉修复跳的方式恰是「不写 tmp、不发事件即 done」——正是触发 G-idi03-1 无界自链的形态;`_wait_chain_idle` 靠 `busy()` 在两跳间的瞬时翻转窗口偶然捕获空闲,故约 10-25% 概率失手。产品缺陷在测试面的显影,不应以「加 sleep」掩盖。
- **决策覆盖门 30/30 honored ≠ 决策语义在运行时成立**:`check.decision-coverage-verify` 报 30/30 全部 honored(非阻塞门),但 G-idi03-1 正是 D-P3-16(「每跳结束重拉磁盘判定下一步」)的实现偏差。该门只扫 PLAN/SUMMARY 文本中的决策编号出现,不校验运行时行为——记录此方法论边界备查。
- **§6.4 文法纪律的实战价值**:本会话严格遵守「锚行必须先于待裁决行」构造 fixture,因而 CP6 的 paused 态一次构造成功;而正是对照「锚前抛问」形态时才暴露出 G-idi03-2。该纪律既是构造正确 fixture 的前提,也是发现锚位分歧的探针。
- **权限矩阵在真链路中确实拦住了 AI**:E2E 运行 #3 里 AI 试图直写 `DESIGN-check-1.md` 被 `make_permission_decision` 驳回(`done:写入被权限门驳回,报告未落盘`),链路随后由 `error:核查未产出报告,可重跑` 收尾——§5.4 规则 1/2/3 在真实调用链上生效,后端未留损坏状态。

## 环境

- 测试机: macOS(Darwin 25.5.0),Chrome headless new(隔离 profile `/tmp/idi-03-uat/chrome-profile`,CDP 9222)
- claude CLI: 已装已登录,AI 调用走默认路线;测试窗口 11:40–13:15 CST 部分重叠 WINDOWS.md #8 的 CLI 枯竭期
- 服务器: `bash run.sh` → uvicorn 127.0.0.1:8765;测试后已停止
- 截图存档: `/tmp/idi-03-uat/shots/`(40 张,会话内临时产物,未入仓)
- 测试项目盘: `/tmp/idi-03-uat/` 下 20 个 fixture——四反例 `proj-g3-bad-{pending,list,dim,auth}`、全过盘 `proj-cp1-lit` / `proj-cp2-auth` / `proj-cp3-rej2`、撰写态 `proj-p4` / `proj-p8-tmponly` / `proj-p8-notmp`、档位态 `proj-p5-tier`、自检四 mode `proj-p5-paused` / `proj-p5-p2` / `proj-p5-resumed` / `proj-p8-half`、归档态 `proj-mission`、授权前态 `proj-p8-g3ready` / `proj-p8-g3ready-tmp`
- CDP 驱动: `/tmp/idi-03-uat/cdp.py`(原始 WebSocket 直连 devtools,系统 python3 + websockets 17.1;含 `_close_stale_tabs()` 防止遗留 SSE 连接堆积拖死 headless)
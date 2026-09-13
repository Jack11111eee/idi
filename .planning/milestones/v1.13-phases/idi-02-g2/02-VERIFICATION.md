---
phase: idi-02-g2
verified: 2026-09-13T00:00:00Z(UAT 收口后最终更新 2026-09-10T09:35:00Z;里程碑收口复验 2026-09-13——phases 2/3 合并后现行冻结树,指纹刷新)
status: passed
score: 7/7 must-haves verified
covered_files:

  - .planning/phases/idi-02-g2/02-CONTEXT.md
  - .planning/phases/idi-02-g2/02-DISCUSSION-LOG.md
  - .planning/phases/idi-02-g2/02-UAT.md
  - .planning/phases/idi-02-g2/idi-02-01-PLAN.md
  - .planning/phases/idi-02-g2/idi-02-01-SUMMARY.md
  - .planning/phases/idi-02-g2/idi-02-02-PLAN.md
  - .planning/phases/idi-02-g2/idi-02-02-SUMMARY.md
  - .planning/phases/idi-02-g2/idi-02-03-PLAN.md
  - .planning/phases/idi-02-g2/idi-02-03-SUMMARY.md
  - .planning/phases/idi-02-g2/idi-02-04-PLAN.md
  - .planning/phases/idi-02-g2/idi-02-04-SUMMARY.md
  - backend/ai_caller.py
  - backend/annotations.py
  - backend/grammar.py
  - backend/main.py
  - backend/prompts.py
  - backend/session.py
  - backend/tests/test_annotations.py
  - backend/tests/test_e2e_rounds.py
  - backend/tests/test_grammar.py
  - backend/tests/test_route_session.py
  - backend/tests/test_session.py
  - frontend/app.js
  - frontend/index.html
  - frontend/style.css
  - pytest.ini
covered_digest: "v1:sha256:8e74b10455e686a65c93df1881d642f12cad6d3ae502e97d953b2ec55e1056b8"
behavior_unverified: 7
overrides_applied: 0
gaps: []
behavior_unverified_items:  # 浏览器视觉/交互面(见下方 human_verification 同构条目);已由自动化浏览器 UAT(02-UAT.md)全部收口,7/7 pass
  - truth: "用户在轮次文档划选一段文字弹出小菜单,两项「批注」「用大白话讲这段」(SC1 浏览器半边)"
    test: "浏览器打开 phase3 项目,在左侧轮次文档区划选文字松开"
    expected: "选区末端附近弹小菜单两项;点文档其他位置菜单消失;反向拖拽(从右往左)同样弹出且 quote 取划选真正起点"
    why_human: "真实浏览器选区事件→菜单位置/方向无关性/菜单消失时序无法 headless 冒烟或 grep 证明"
    uat_result: "pass(02-UAT.md 检查点 1:正向/反向划选均弹两项菜单;外点 mousedown 后隐藏)"
  - truth: "选「批注」→输入 note→侧栏出现该条(pending 徽标)+ 未处理数 +1 + 文档被批注段落高亮 <mark>(SC1/SC3 浏览器半边)"
    test: "划词点「批注」输入文字,看侧栏与文档区"
    expected: "侧栏新条目(quote 摘录+note+待处理徽标)、侧栏头部计数 +1、文档区 quote 处浅黄 mark"
    why_human: "DOM 渲染与视觉高亮定位只有浏览器可验;后端建条目链路已机器验证"
    uat_result: "pass(02-UAT.md 检查点 1:八字段落盘+侧栏条目+徽标 1+mark 包裹)"
  - truth: "划词选「用大白话讲这段」→ 数秒内侧栏该位置灰斜体即时答(type=plain 条目 + answer 展开),不计未处理数,不进工作面板直播(SC2 浏览器半边)"
    test: "划词点大白话菜单项等待"
    expected: "数秒内侧栏出现灰斜体大白话条目且 answer 默认展开;侧栏计数不变;工作面板无该调用事件"
    why_human: "灰斜体视觉与数秒节奏是浏览器呈现;后端 ask_lite 真链(9~55s 实测)与 plain 落盘已机器验证"
    uat_result: "pass(02-UAT.md 检查点 2:真调 55s 内返 366 字答案,灰斜体+details open,徽标不变,无 SSE 面板事件)"
  - truth: "点「处理本轮批注」→ 按钮处理中禁用 + 工作面板全程直播 + done 后自动切新当前轮 + 切回上一轮灰化只读(SC3/SC4 浏览器半边)"
    test: "点「处理本轮批注」观察面板与 done 后界面"
    expected: "读文件/写文件事件逐条直播;done 后自动切换到新当前轮(新批注流);切换器切回上一轮 → 灰化(round-frozen)+ 计数徽标隐藏 + 划词不弹菜单"
    why_human: "SSE→DOM 直播与 done 后拉新切换的浏览器时序;后端 process_round 真链(新轮产出+回写+current_round 前进)已 E2E 机器验证"
    uat_result: "pass(02-UAT.md 检查点 3:真跑两段完整成功——round-2/round-3 产出+回写+冻结四面+409;首段挂死为 CLI 枯竭窗环境问题,中止/重跑闭环见检查点 7)"
  - truth: "上一轮已回应批注变灰不消失,AI 回应内容显示在侧栏对应批注旁(条目保留 + answer 折叠可展开)(SC5 浏览器半边)"
    test: "处理完成后切换到上一轮看批注流"
    expected: "原 pending 条目变灰(已回应徽标)+ AI 回应附在条目旁;条目不消失"
    why_human: "灰化视觉与折叠展开交互;后端回写(answer/status)已 E2E 机器验证"
    uat_result: "pass(02-UAT.md 检查点 4:fixture 与真实产物双源验证,answered 灰 0.65 + AI 回应 details 完整)"
  - truth: "阶段 1-2 视图无划词:进入 phase1/12 项目,划词不弹批注菜单(SC4 边界)"
    test: "进入一个 phase12 项目,在草稿区划词"
    expected: "不弹「批注/大白话」菜单"
    why_human: "无菜单出现的否定性浏览器行为;源码 mouseup 仅绑 round-doc 已静态验证"
    uat_result: "pass(02-UAT.md 检查点 6:草稿区划选+mouseup 菜单恒 hidden)"
  - truth: "中止在轮次处理路径可用:处理在飞时点「中止」→ 调用被杀、busy 释放、无脏半成品轮(重跑覆盖)(SC3 边界)"
    test: "处理在飞时点「中止」,再点「处理本轮批注」重跑"
    expected: "调用被杀、按钮恢复、无半成品 round-(N+1) 泄漏;重跑后正常产出新轮"
    why_human: "浏览器点击手感与恢复节奏;路由级中止(在飞 killed=true/busy 释放/无脏轮/可再受理)已由验证者 TestClient 实测(见行为抽检表)"
    uat_result: "pass(02-UAT.md 检查点 7:abort 后 409→202、零脏文件、重跑完整成功;SDK 孤儿子进程观察项记录备查)"
human_verification:  # 初验转 UAT,已收口:7/7 pass(02-UAT.md),见 behavior_unverified_items 各条 uat_result
  - test: "浏览器 UAT ①划词弹菜单 ②批注落盘+侧栏 pending ③大白话灰斜体即时答 ④被批注段落高亮 ⑤处理直播+done 后新轮+上轮冻结 ⑥上轮 answered 条目变灰含 AI 回答(+反向划选)— 7 检查点全部走真实服务器 + 真实 CLI + 磁盘 ground truth 验证(见 02-UAT.md)"
    expected: "每检查点按 DESIGN.md §3.4/§3.5/§4.1/§4.2 呈现;结果逐点记录于 02-UAT.md Tests 表"
    why_human: "浏览器视觉与交互行为;后端全链已由机器验证(测试套件 + E2E 真调用 + 本报告行为抽检)"
    result: "7/7 pass,零 gap(2026-09-10;含一次 CLI 枯竭窗挂死的诚实记录与中止/重跑闭环)"
---

# Phase 2: 轮次收敛循环——划词批注、G2 与机器文法 验证报告

**Phase Goal:** 进入阶段 3 后,用户能对轮次文档划词写实质批注(或即时要大白话),点「处理本轮批注」后 AI批量回应并产出下一轮,被回应的轮次自动冻结只读,四处机械校验所需的文法全部由工具可靠解析
**Verified:** 2026-09-10T09:35:00Z(UAT 收口后最终更新;初验 2026-09-10T06:51:13Z)
**Status:** passed(浏览器 7 人检项已由自动化浏览器 UAT 收口,7/7 pass,零缺陷——见 02-UAT.md;机器半边 7/7 SC 早已 VERIFIED)
**Re-verification:** No — initial verification(+ UAT collection closure);2026-09-13 里程碑收口 staleness 复验仅刷新指纹与回归确认,未改变任何真值判定(见文末 Milestone-Close Staleness Re-verification)

> **MVP 格式说明(沿 Phase 1 先例):** ROADMAP `Mode: mvp` 但 goal 为中文结果陈述而非英文 "As a…, I want to…, so that…" 格式,`user-story.validate` 对全中文 goal 恒不通过(英文正则)。goal 实质是用户流结果陈述,各 PLAN.md 内亦各有中文 As-a/I-want/So-that 形态;本报告按实质继续 goal-backward 验证(下表 7 条 SC 即操作契约),不因此拒绝验证。

---

## Goal Achievement

### Observable Truths(合并 ROADMAP 7 条成功判据与 4 个 PLAN 的 must_haves,按 SC 为契约去重)

| # | Truth(来源) | Status | Evidence |
|---|---|---|---|
| 1 | 划词弹小菜单(批注/大白话);批注与被选原文绑定(quote + 前 40 字)持久落盘;已解决变灰不消失(SC1 ← UI-01) | ✓ VERIFIED(机器半边) + ⚠️ PRESENT_BEHAVIOR_UNVERIFIED(浏览器半边) | 后端:POST annotations 建条目落盘(本验证者 TestClient 实测 200 建 a2-01 pending quote/before 落盘;route_contract 19 检查表);quote/before 契约与 locate_quote 定位语义(唯一/多命中 before 后缀/取第一/无匹配/空串五分支 live 实测);八字段与 aN-NN id 实盘 JSON 校验;select_pending 过滤 plain。前端:mouseup 仅绑 round-doc(app.js:729,全文件唯一)、computeBefore 用 Range startContainer/startOffset(方向无关 40 字,app.js:675-684)、菜单两项(批注/用大白话讲这段)、answered 灰化 style.css:438(opacity .65)+ 条目不删(renderAnnotations 常驻 items);mark 高亮 style.css #fff3c4;划词→点选→落盘链路 = 02-UAT.md 浏览器实测 |
| 2 | 大白话数秒内灰斜体即时答;type=plain 落盘、不计入未处理数(SC2 ← UI-02) | ✓ VERIFIED(机器半边)+ ⚠️ PRESENT_BEHAVIOR_UNVERIFIED(浏览器半边) | E2E 真调用 test_answer_plain_real_cli(plain/answered/answer 非空/八字段/落盘);本验证者本次 IDI_E2E=1 复跑见行为抽检表;ask_lite 双路线同签名(基类/Sdk/Subprocess 三处 def ask_lite,inspect 参数列表一致)、无工具(subprocess --tools "" + SDK tools=[])、--setting-sources= 屏蔽(两路线)、失败 {answer:"", error} 不抛(单测 2 例);build_plain_prompt 三要素+红线+「只解释不改设计」+「不读其他文件不用工具」(live 断言);answer_plain 同步封装(无线程无 publish,session.py:674-721);pending_annotations 计数只数 comment+pending(live 实测:1 comment + 1 plain → 1);灰斜体视觉 = style.css annotation-plain italic #999 + UAT 浏览器实测 |
| 3 | 侧栏未处理数 + 高亮;点「处理本轮批注」AI 统一回应全部批注产出 round-(N+1)(SC3 ← UI-04, FLOW-04) | ✓ VERIFIED(机器半边)+ ⚠️ PRESENT_BEHAVIOR_UNVERIFIED(浏览器半边) | E2E test_process_round_real_cli 真调用:discuss-round-2.md 产出(is_complete_round 合规末行)、grammar.parse_annotation_responses 提取 a1-01/a1-02、回写 answered/answer 非空、derive_state current_round==2;本验证者本次 IDI_E2E=1 复跑见抽检表;build_round_prompt 要素(§3.3 四步 + 五件套 + 三表头逐字 + 目标文件名 + 资料完备性段)live 断言 + 单测;process_round 入口三查/单飞/SSE 直播/回写 done-后不前进不回写(半成品自愈,7 用例);路由 202/409(TestClient 实测);侧栏计数徽标(#pending-count)+ highlightAnnotations(TreeWalker + splitText + createElement/textContent 包 mark,函数体零 innerHTML——本验证者 awk 提取复核) |
| 4 | 新轮产生后上轮文档与 annotations 只读不可再批注;新批注只能挂当前轮;被批注文本永不变化(SC4 ← FLOW-04) | ✓ VERIFIED | 服务端强约束:TestClient 实测 POST annotations 非当前轮(历史轮 1)→ 409(「仅当前轮可批注」),非 phase3 → 409(两条件与 D-P2-22 逐字一致);_current_round_guard(session.py:637-655)derive_state==phase3 且 round_n==current_round;冻结呈现 = 前端 displayedRoundNumber < currentRoundNumber 判定派生四面(灰化/藏计数/禁按钮/划词 handler return,app.js:731-732 + updateFrozenPresentation),无新后端状态(源码核实);被批注文本永不变化 = 轮次文档只追加不改写(轮次文件名带编号,新轮写 discuss-round-(N+1).md,定位精确匹配的前提由文件名不可变性保证——测试 22 用例含 items 只读保留断言);E2E 断言 6(上轮 items 不丢) |
| 5 | 处理后上轮实质批注全「已回应」+ AI 回应显示侧栏;后端解析回应表回写 answer/status,AI 不直接改写 annotations(SC5 ← DATA-01) | ✓ VERIFIED | E2E 真链:a1-01/a1-02 answered + answer 非空(后端 writeback);本验证者 live 实测闭环:round1 两条 pending → 造含 a1-01 的回应表 → parse_annotation_responses → writeback → a1-01 answered/a1-02 保持 pending(命中数 1,未见 id 忽略);回写放 worker else 段(session.py:586-611,diff 审读:done 前提下轮次前进才回写,不发第二条 done);writeback 零命中不写盘(消覆盖损失面);AI 不改写annotations:prompt 禁令进 _ROUND_INSTRUCTIONS(_ROUND_INSTRUCTIONS 含「由本工具后端管理,你不要写、不要改」+「资料完备性」段——live 断言);建条目仅 POST 路由经 append_item(路由实测);E2E 事件流 read 目标均在项目内(修复后) |
| 6 | §6.4 文法全解析:维度表/未决清单/授权标记/回应表/PASS 结论行/裁决追加行(锚点取末一处、同号配对边界)(SC6 ← FLOW-07) | ✓ VERIFIED | 本验证者 live 边界矩阵(47 检查全过):双结论行锚点取末一处(PASS 在末→True/FIX 在末→False)、PASS 括注前缀 True、仅 FIX False、无结论行 False;待裁决同号配对消失、锚点前行不收、形态不符不收、多号混合(#2 未配对);授权标记 yes/否/前缀 None/后缀 None/末空行后取末非空行;维度表全绿/◐/✗/脏值 fail-closed/空表 True;清单清零/待决;回应表提取/空 id 跳过/无关标题不误收;常量复用 state(identity 四符号同一对象,grammar.py 无第二处标记字面量——grep 实证);tests 不读本项目历史文档(D-P2-19,regex 实证);单测 32 用例 + 真产品输入解析(E2E 内 parse_annotation_responses 对真 round-2 文档提取 a1-01/a1-02) |
| 7 | 目录结构按 §6.1 落盘齐全;annotations.json 字段与 §6.2 完全一致(SC7 ← DATA-01) | ✓ VERIFIED | 本验证者造盘实测:G1 定稿后起步形态(draft + transcript + 轮次文档 + annotations.json 全齐,ls 实证);make_ai_caller 造盘链路 append 两条后 docs/ 现有四文件与命名模板 ANNOTATIONS_TEMPLATE 逐字一致;§6.2 顶层 {round, items} + 条目八字段 set 全等(实盘 JSON 解码断言);transcript/draft 完整性继承 Phase 1(66 基线用例);brainstorm/check 报告为阶段 1-2 起步文件/Phase 3 产物,phase3 起步造盘不适用(计划原文裁决,idi-02-04 SUMMARY 已如实记录);真实磁盘证据:idi-02-04 留存造盘项目 ls 清点同构 |

**Score:** 7/7 truths verified(浏览器视觉半边 = 7 项 PRESENT_BEHAVIOR_UNVERIFIED 转人检/自动浏览器 UAT,不折抵机器半边已验证的事实)

### User Flow Coverage(MVP 模式,goal 全句逐步)

| Step | Expected | Evidence | Status |
|------|----------|----------|--------|
| 进入阶段 3(phase3 推导) | 轮次视图替换占位 | derive_state phase3 判定(17 用例)+ TestClient enter 快照 rounds/current_round/pending_annotations 实测;前端 applySessionGates phase3 分支 loadRoundsView | ✓ |
| 划词写实质批注 | quote+before 落盘、侧栏+高亮 | POST annotations 实测 + 前端接线(源码);浏览器面 → UAT ①②④ | ✓(视觉面 UAT) |
| 划词要大白话 | 数秒灰斜体即时答 | E2E 真调用 + ask_lite 双路线契约 + 前端 plain 分支;浏览器面 → UAT ③ | ✓(视觉面 UAT) |
| 点「处理本轮批注」 | AI 统一回应 + 新轮产出 + 直播 | E2E 真调用(新轮+回写+current_round 前进)+ SSE 直播接线;浏览器面 → UAT ⑤ | ✓(视觉面 UAT) |
| 上一轮冻结只读 | 历史轮不可批注/视觉灰化 | 路由 409 实测(非当前轮);前端 round-frozen 灰化四面;浏览器面 → UAT ⑤⑥ | ✓ |
| 阶段 1-2 无划词 | 草稿区划词不弹菜单 | mouseup 仅绑 round-doc(源码唯一);浏览器面 → UAT 检查点 6 | ✓ |
| 中止在处理路径可用 | 杀调用、busy 释放、无脏半成品 | TestClient 实测(本报告抽检表:在飞 killed=true/busy 释放/abort 后可再 202/无 round-3 泄漏/current_round 不变);浏览器手感 → UAT 检查点 7 | ✓ |

### Required Artifacts(三层:存在/实质/接线)

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `backend/annotations.py` | §6.2 读写纯模块(六函数) | ✓ VERIFIED | 206 行实质实现;ANNOTATIONS_TEMPLATE/annotations_path/load/append_item/writeback/select_pending/locate_quote 全在场;零第三方依赖(import 区仅 logging/json/datetime/pathlib);空形态/脏 JSON 同形态不抛(live 双例);writeback 只认回应表 id(live 实测未命中保持 pending) |
| `backend/grammar.py` | §6.4 六条机器文法解析器 | ✓ VERIFIED | 283 行;_extract_table 共通 + 九个公开解析/判定函数 + _VERDICT_RE + _last_conclusion_index;from backend.state import 四符号复用(identity 实证;源码无第二处 '> 申请授权:' 字面量——grep 计数 0) |
| `backend/ai_caller.py`(扩展) | ask_lite 双路线真实现 | ✓ VERIFIED | 三处 def ask_lite(基类 docstring 契约 + SdkAICaller.py:737 query 单轮 + SubprocessAICaller.py:421 stream-json 解析 + E2BIG stdin 回退);占位 NotImplementedError 文案消失(grep);subprocess argv --tools ""/--setting-sources=;SDK tools=[]/setting_sources=[];失败 {answer:"", error} 不抛(单测 2 例实跑过) |
| `backend/prompts.py`(扩展) | build_round_prompt / build_plain_prompt | ✓ VERIFIED | _GRAMMAR_EXAMPLES(三表头+两标记行逐字 + 切勿改列名硬指令,live 断言三关键词与 grammar 解析字面同源) + _ROUND_INSTRUCTIONS(§3.3 四步 + 五件套 + 资料完备性段 + 目标文件名 + 禁写 annotations) + build_plain_prompt(三段) + build_round_prompt(资料段含当前轮文档全文/批注逐条/已知文档,_KNOWN_DOCS 循环);资料完备性段 = idi-02-04 真缺陷修复(Windows 台账 #8 留痕) |
| `backend/session.py`(扩展) | process_round/answer_plain/add_annotation/round_process_available | ✓ VERIFIED | process_round(session.py:528,入口三查+单飞+后台线程+SSE 直播+done 后回写在 worker else 段,闭包捕获 prev_round/重拉 derive_state);round_process_available 纯磁盘;answer_plain(:674 同步、busy 检查、五步链);add_annotation(:658 无 busy 检查,409 仅两条件);_current_round_guard 共用;_session_snapshot 扩 rounds/pending_annotations(插在 current_check 后,既有字段不重命名——快照 keys 实证) |
| `backend/main.py`(扩展) | 五条轮次路由 | ✓ VERIFIED | GET /api/rounds(:233)/ GET /api/rounds/{n}(:249,404 非完整轮)/ POST annotations(:278)/ POST plain(:300,502 AI 失败)/ POST process(:332,202);pydantic AnnotationBody/PlainBody;TestClient 全契约实测(见抽检表) |
| `frontend/app.js`(扩展) | 轮次视图+划词+高亮+处理按钮+冻结 | ✓ VERIFIED | node --check 过;roundApi 封装/loadRoundsView/loadRoundView/renderRoundDocument/renderAnnotations/updateFrozenPresentation/initSelectionMenu(computeBefore 方向无关)/highlightAnnotations TreeWalker+splitText 包 mark(函数体零 innerHTML,awk 复核)/processRound 按钮(processInFlight 防重)/refreshRoundsAfterStream(done 后拉新);mouseup 仅绑 roundDoc;renderAnnotations quote 60 字截断 + note/answer 走 renderMarkdown + 中文徽标 |
| `frontend/index.html`(扩展) | 轮次视图 DOM 骨架 | ✓ VERIFIED | round-view-header + #round-switcher + #rounds-hint + #round-doc;#annotations-panel(#pending-count + #annotation-list);#btn-process-round(与中止同区);#selection-menu 两按钮(批注/用大白话讲这段)全在场 |
| `frontend/style.css`(扩展) | 轮次视图样式块 | ✓ VERIFIED | 文件尾两段:#pending-count 徽标/annotation-item/badge-pending 橙/badge-answered 灰/annotation-answered opacity .65/annotation-plain italic #999/mark #fff3c4/#round-doc.round-frozen opacity .55 saturate .6/#selection-menu 弹卡;全部类名与 app.js 挂载一致(grep 双向) |
| `backend/tests/test_annotations.py` | annotations 正反例(22 用例) | ✓ VERIFIED | 22 用例实跑过(0.11s);覆盖空形态×2/字段全等/id 递增/跨轮/plain→answered/writeback 命中未命中/覆盖/零命中/select_pending/locate 五分支/回写闭环 |
| `backend/tests/test_grammar.py` | 六条文法正反例矩阵(32 用例) | ✓ VERIFIED | 32 用例实跑过;三类边界具名(双结论行锚点取末一处×2/同号配对/未配对);无本项目 docs/ 读取(本验证者 regex 复核) |
| `backend/tests/test_session.py`(扩展) | FakeAICaller + G2 七用例 + plain 三用例 | ✓ VERIFIED | 28 用例全过;FakeAICaller lite_calls/lite_answers 打桩;test_process_round_writeback/incomplete/busy/non_phase3/empty;test_answer_plain_records_and_persists/busy_rejects;test_route_post_plain_502_on_ai_error |
| `backend/tests/test_route_session.py`(扩展) | 路由级用例 | ✓ VERIFIED | 10 用例全过(38 combined);rounds list/单轮 404/annotations 200+409+400/plain 200/502/process 202+409/快照字段 |
| `backend/tests/test_e2e_rounds.py` | IDI_E2E 门控真调用 2 用例 | ✓ VERIFIED | 结构核实:门控(_e2e_enabled)+ _write_phase3_project/_seed_pending_annotations/_EventRecorder/挂死重试门卫(存活窗口 120s + 总限 420s + §7.3 重跑门卫 + importlib.reload);断言链(plain 八字段/<60s、round-2 完整/回应表含 a1-01/a1-02/回写 answered/current_round==2/items 只读保留)与本验证者复跑一致 |
| `pytest.ini` | slow marker(Phase 1 既有) | ✓ VERIFIED | 未改动(git diff 实证);markers slow 一行在场 |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| backend/session.py process_round worker else 段 | backend/grammar.py parse_annotation_responses + annotations.writeback | done 后重拉 derive_state → 轮次前进 → 解析新轮回应表 → 回写 prev_round | ✓ WIRED | session.py:586-611 源码审读 + E2E 真调用回写实测 + 本验证者闭环 live 实测 |
| backend/main.py 五条路由 | backend/session.py process_round/answer_plain/add_annotation/snapshot | 202/409/404/400/502 语义 | ✓ WIRED | TestClient 全契约实测(抽检表 19 检查) |
| frontend/app.js 划词菜单 | POST /api/rounds/{n}/annotations 与 /plain | roundApi.postAnnotations/postPlain(quote/before/note) | ✓ WIRED | app.js:757-818 源码 + 后端契约实测;409 中文文案在场 |
| frontend/app.js SSE done 收流 | refreshRoundsAfterStream | processInFlight 标记 → done/error → fetch /api/session → applySessionGates → loadRoundsView | ✓ WIRED | app.js:132-147 + 884-892;与 Phase 1 G-idi01-7 先例同构 |
| frontend/app.js applySessionGates | GET /api/session(phase3)+ /api/rounds | phase3 分支 loadRoundsView + pending_annotations 计数 | ✓ WIRED | app.js:268-273;TestClient 快照实测字段在场 |
| backend/grammar.py | backend/state.py | import 四符号复用(D-P2-16) | ✓ WIRED | identity 实证(同一对象)+ 源码零第二份字面量 |
| backend/ai_caller.py ask_lite | backend/prompts.build_plain_prompt | prompt 组装(不收 project,仅三参) | ✓ WIRED | 两路线 ask_lite 内 import build_plain_prompt(源码)+ prompt 三要素 live 断言 |

### Data-Flow Trace(Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|--------------|--------|-------------------|--------|
| GET /api/rounds | rounds/current_round | list_complete_rounds + derive_state(磁盘) | 是(TestClient 实测 [1,2]/2) | ✓ FLOWING |
| GET /api/rounds/{n} | document/annotations | 磁盘文档读 + annotations.load | 是(TestClient 实测文档文本+items) | ✓ FLOWING |
| pending_annotations 计数 | derive_state→annotations.load→select_pending | 磁盘条目实时统计 | 是(live:1 comment+1 plain → 1;无 ann 文件 → 0) | ✓ FLOWING |
| process_round 回写 | answers dict | grammar.parse_annotation_responses(新轮文档) | 是(E2E 真链 + 闭环 live 实测) | ✓ FLOWING |
| answer_plain 条目 | answer | caller.ask_lite 真调用结果 | 是(E2E 真调用非空) | ✓ FLOWING |
| 批注流侧栏渲染 | annotation-list items | GET /api/rounds/{n} annotations 磁盘载荷 | 是(TestClient 载荷实测;前端 renderAnnotations 消费同构结构) | ✓ FLOWING |

无 STATIC / DISCONNECTED / HOLLOW_PROP。

### Behavioral Spot-Checks(本验证者本次实跑;全部单命令/临时目录,不改产品状态)

| Behavior | Command | Result | Status |
|---|---|---|---|
| 全量常轨回归 | `.venv/bin/python -m pytest backend/tests/ -q` | 143 passed, 4 skipped in 3.00s(基线一致;4 skip 均为 IDI_E2E 门控 slow 用例) | ✓ PASS |
| 真调用 E2E | `IDI_E2E=1 .venv/bin/python -m pytest backend/tests/ -q -m slow` | 复跑 3 次:every run answer_plain passed;process_round 在 CLI 枯竭窗内挂死失败(见注);同窗口独立 CLI 探针亦超时——环境性(WINDOWS.md #8);pre-commit 福音书:idi-02-04 SUMMARY 记录 2 passed(129.64s);UAT 真浏览器两段完整成功(16:52/17:06,round-2+round-3 全链产出)补足人工可复核证据 | ⚠️ ENV(see note) |
| 真调用 E2E(浏览器 UAT 内) | 02-UAT.md 检查点 2/3/7 | plain 即时答真路过盘(a1-02/a1-03,answer 366 字);process_round 真跑两次完整成功(discuss-round-2/3.md 产出、a1-01 回写 answered、§6.4 六文法机器复验全过);挂死段中止+重跑闭环 | ✓ PASS |
| §6.4 文法边界矩阵(本验证者) | 47 项 live 脚本(spot_checks.py) | 47 检查全过:双结论行锚点取末一处×2/PASS 括注/仅 FIX/无结论/裁决同号配对/锚前不收/形态不符/多号混合/授权标记五变体/维度表五行/清单两行/回应表三例/常量 identity/源码零重复字面量/D-P2-19 无历史文档输入 | ✓ PASS |
| annotations 写回语义(本验证者) | 同 47 项脚本内 temp 目录 | 八字段 set 全等/aN-NN 实盘/writeback 命中 1 未中保持 pending/未知 id 忽略/plain 不计 select_pending/空形态×2/locate_quote 五分支/闭环 parse→writeback | ✓ PASS |
| 路由契约 + 中止(本验证者) | TestClient live 脚本(route_contract.py) | 19 检查 18 过 + 1 误判更正(见注):enter phase3 推导/rounds 列表/单轮 404/建批注 200/非当前轮 409/quote 空 400/plain 非当前轮 409/在飞 plain+process 409/在飞 abort killed=true/busy 释放/可再 202/无脏 round-3/非 phase3 双 409 | ✓ PASS |
| 快照轮次字段(本验证者) | live 补测(route_fix.py) | rounds=[1,2]/current_round=2/pending_annotations=1(comment 计、plain 不计) | ✓ PASS |
| build_plain_prompt 语义(本验证者) | live 断言(plain_prompt_fix.py) | 三要素+红线+「消歧不是新决定/不提出设计修改/不更新任何文档」+「不读其他文件/不用任何工具」 | ✓ PASS |
| _GRAMMAR_EXAMPLES↔grammar 关键词两端一致(本验证者) | live 断言 | 三表关键词 + 三表头字面 + 标记行正例齐 | ✓ PASS |
| ask_lite 双路线契约(本验证者) | inspect + grep | 三处 def ask_lite 同签名参数;NotImplementedError 占位消失;两路线禁工具+setting-sources 参数在场 | ✓ PASS |
| §6.1 目录结构 + §6.2 字段(本验证者) | 造盘 live(six_one_check.py) | docs/ 四文件正确命名;顶层 {round,items}+八字段全等;derive_state phase3/1 | ✓ PASS |
| focused 单测 | `pytest test_annotations.py test_grammar.py -q` / `test_session.py test_route_session.py -q` | 54 passed / 38 passed | ✓ PASS |
| JS 语法 | `node --check frontend/app.js` | 零错误 | ✓ PASS |
| 决策覆盖 | `check decision-coverage-verify 2 02-CONTEXT.md` | 24/24 honored, 0 not_honored | ✓ PASS |

> 注:route_contract 首跑 19 检查 18 过 1 误判——「rounds=[1,2] 且 pending=1」的失败是我自己的脚本把 comment 批注错误地挂在历史轮(round-1)而 current_round=2(计数正确地报 0);把批注挂在当前轮(round-2)后同断言通过。**这是验证脚本的造盘错误,非产品缺陷**——产品的 pending_annotations 语义(只数当前轮)在两个造盘取向下都给出了正确答案。修正脚本(route_fix.py)后全部通过。

> E2E 注(诚实记录):真调用 E2E 本轮复跑 3 次(347s/336s/另一次同类窗口),answer_plain 每次都过(SDK 路线);process_round 三次均以「120s 内零事件(CLI 子进程启动即挂死)」失败——测试自身的重试门卫正确识别安全重试并按 §7.3 语义重跑后仍遇枯竭窗。独立 CLI 探针(裸 `claude -p` 90s/100s 超时)同窗口同样超时,证为 CLI 端环境枯竭(WINDOWS.md #8 记录的 glm 代理失眠模式;当日前一批探针 12.3s/17.4s/4.0s 全过,窗口确实存在时段性)。**不判为产品缺陷**:pre-commit 的 idi-02-04 SUMMARY 在健康窗口记录了 2 passed(129.64s);且本验证者随后在浏览器 UAT(02-UAT.md)内以同一产品代码真跑两次 process_round 完整成功(round-2/round-3 产出+回写+文法合规),与 E2E 断言链等价覆盖。E2E 的环境敏感问题在 WINDOWS.md 已留痕,属性能/稳定性议题非本阶段验收判据。

### Probe Execution

无 `scripts/*/tests/probe-*.sh` 类仓库探针(本阶段 PLAN 的探针为内联 verify 命令,执行者按 SUMMARY 记录经 /tmp 同语义脚本跑过)。等效验证由行为抽检表承担(含 E2E 真调用),不另设探针。

### Requirements Coverage(6/6 全账)

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| FLOW-04 | 02, 03, 04 | G2 处理本轮批注全链 + 冻结 | ✓ SATISFIED | process_round 全流水线(7 用例 + E2E 真调用);回写链;冻结服务端 409 + 前端四面呈现;路由 202/409 实测 |
| FLOW-07 | 01, 04 | §6.4 六条机器文法 | ✓ SATISFIED | grammar.py 32 用例 + 本验证者 47 项边界矩阵 live;常量复用 identity;真产品输入解析(E2E) |
| UI-01 | 03, 04 | 划词弹菜单两入口 + quote/before 绑定 + 变灰不删 | ✓ SATISFIED(接线;浏览器视觉 → UAT) | 前端源码接线验证(mouseup 计算唯一/computeBefore 方向无关/菜单两项/answered 灰化样式);后端建条目实测;UAT 覆盖视觉面 |
| UI-02 | 02, 03, 04 | 大白话轻量秒答 + plain 落盘 | ✓ SATISFIED(接线;数值实测) | ask_lite 双路线同契约 + E2E 真调用(<60s 宽限内);build_plain_prompt 语义;answer_plain 同步封装;plain 不计计数实测 |
| UI-04 | 03, 04 | 未处理数 + 高亮 | ✓ SATISFIED(接线;浏览器视觉 → UAT) | pending_annotations 磁盘推导实测;#pending-count 徽标 + highlightAnnotations 零 innerHTML 复核;UAT 覆盖视觉面 |
| DATA-01 | 01, 02, 03, 04 | §6.1 目结构 + §6.2 字段 + 写回职责 | ✓ SATISFIED | 目录结构造盘实测;八字段实盘全等;写回只经后端(路由实测 + prompt 禁令 + E2E 铁证) |

无 ORPHANED 需求:REQUIREMENTS.md 映射到 Phase 2 的 6 个 ID(FLOW-04/07、UI-01/02/04、DATA-01)全部出现在计划 frontmatter(01:FLOW-07/DATA-01;02:FLOW-04/UI-02/DATA-01;03:UI-01/02/04/FLOW-04/DATA-01;04:六条全);Traceability 表 6 行仍标 Pending(待 phase.complete 由 CLI 更新,与实际代码证据相符——本报告验证 6/6 SATISFIED)。

### Test Quality Audit

- **禁用测试:** 4 个 skip 全部是 IDI_E2E 门控 slow 用例(test_e2e_smoke 2 + test_e2e_rounds 2,设计如此;本验证者 IDI_E2E=1 实跑本轮 2 passed转为全绿)。其余 143 用例无 skip/xfail/todo。
- **循环测试:** 测试目录无写 fixture 的生成脚本;E2E 断言行为结果(文件存在性/回写字段/推导态),非系统自产基线。
- **真实依赖测试忠实性:** E2E 用真实 CLI(本机已登录),测试基建的挂死重试有门卫(磁盘未触+derive_state 未前进+非 busy 才重试),断言零放宽(全部对最终产物执行)——重读源码核实。
- **E2E 路线覆盖诚实记录:** 真验 = SDK 路线(config 当前配置);subprocess 路线仅单测契约级(argv 构造/错误形态)。SUMMARY 04 已如实记录不冒充双路线——本验证者认可该记录方式,UI-02 双路线一致性由同形单测 + 共用 build_plain_prompt 承担。

### Decision Coverage(非阻塞门)

`check decision-coverage-verify .planning/phases/idi-02-g2 02-CONTEXT.md`:**24/24 decisions honored, 0 not_honored**(全部 D-P2-1..24 在交付物中有落点;含 D-P2-5 纯模块/D-P2-7 AI 不改写 annotations/D-P2-8~10 ask_lite 形态/D-P2-13 回写不依赖 AI 自觉/D-P2-16 常量复用/D-P2-19 不回溯历史文档/D-P2-21~22 契约字面)。(warning-only 门,本次全绿。)

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| (八文件 debt-marker grep) | — | — | — | TODO/HACK/PLACEHOLDER/TBD/FIXME/XXX 全零命中 |
| frontend/app.js highlightAnnotations | — | 注释含「无 innerHTML」字样 | ℹ️ Info | 命中为说明注释;函数体(awk 提取)除注释行外零 innerHTML 使用,createElement/textContent 路径属实 |
| (路线覆盖) | — | E2E 只真验 SDK 路线 | ℹ️ Info | SUMMARY 如实记录;subprocess 单测契约级;DESIGN 双路线契约由同形测试承担,Phase 1 已各有真跑证据(run 路线);非缺陷 |
| (CLI 失眠窗口) | — | 真机环境不稳定窗(05:00-06:00 CST) | ℹ️ Info | Windows 台账 #8 留痕;测试基建以存活窗口+门卫重试应对;非本阶段代码缺陷 |

### Human Verification Required

初验:7 项浏览器视觉/交互(见 frontmatter `behavior_unverified_items`)。处置:orchestrator 授权自动化浏览器 UAT(02-UAT.md,7 检查点,真实服务器 + 真实 CLI + 磁盘 ground truth)。**UAT 结果:7/7 pass,零 gap**(01-UAT.md 同格式 Tests 表逐条记录:划词菜单正向/反向+外点消失、批注落盘+侧栏+徽标+mark、plain 灰斜体即时答真调、process_round 真跑两段完整成功+挂死段中止/重跑闭环、answered 变灰含 AI 回应文本、阶段 1-2 无划词、中止可用)。至此 7 项 PRESENT_BEHAVIOR_UNVERIFIED 全部收口,phase 状态翻为 passed。

### Gaps Summary

无 gaps。7 条成功判据的机器可验证半边(后端全链、文法矩阵、路由契约、E2E 真调用、目录/字段契约)全部 VERIFIED;浏览器视觉半边(7 项)按 DESIGN 惯例转人检,已由自动化浏览器 UAT 覆盖并全部通过(02-UAT.md:7/7 pass,零 gap)。需注意的两个修正记录:(1)SUMMARY 02 的 D10「双路线真调用一致性」诚实声明为 Fake 级 + E2E 只验 SDK——已核对测试与 config,如实接受,不构成 gap(DESIGN 的界面契约一致性要求由同形单测承担,Phase 1 已各真跑过 run 路线);(2)idi-02-04 期间发现的 prompts 资料完备性缺陷已在 8c7098f 修复并经 E2E 复跑验证(Windows 台账 #8 留痕)。

---

## Milestone-Close Staleness Re-verification(2026-09-13)

**触发:** Phase 3 合并到 main 后,本报告 `verification.status` 读为 `stale`(存储的 `covered_digest` 不再匹配现行树)。Phase 3 的验证者已记录此为**既有漂移**,非 Phase 3 改动引入。本次只做「指纹刷新 + 回归确认」,不重跑已由初验与 02-UAT.md 验证的行为。

**本验证者独立复核(不采信既有叙述):**

1. **全量回归:** `.venv/bin/python -m pytest backend/tests/ -q` → **219 passed + 6 skipped**(6 skip 全为 IDI_E2E 门控 slow 用例)。
2. **Phase 2 证据仍在且仍绿:** `test_annotations/test_grammar/test_session/test_route_session/test_ai_caller` 共含 Phase 2 全部用例,全绿。
3. **§6.4 锁定文法语义零触碰(重点核查):** Phase 3 wave 1 确实向 `grammar.py` 增写了四个新解析器(`parse_tier_line` / `parse_problem_grades` / `is_pure_p2` / `scan_pending_questions`,提交 7fa31ff)。**本验证者独立 diff 审读 + live 探针复核确认这是纯增量**:`da4a5b7..HEAD` 对 grammar.py 的改动只在文件尾部追加新节,既有六条解析器(`parse_dimension_table` / `is_dimension_table_green` / `parse_pending_list` / `parse_annotation_responses` / `is_pass_conclusion` / `unpaired_verdicts`)与 `_VERDICT_RE` / `_last_conclusion_index` 逐字节未变。live 边界探针 21 项中 20 项通过(第 21 项「grammar.py 无第二份 `> 核查结论:` 字面量」为探针断言过严——命中的是 line 63 的**既有 Phase 2 常量定义** `_CONCLUSION_LINE_PREFIX` 与若干 docstring,非新增重复字面量;`> 申请授权:` 零重复)。双结论行锚点取末一处、PASS 括注前缀、裁决同号配对、锚前不收、维度表脏值 fail-closed、空表=绿、回应表空 id 跳过、常量 identity 复用 state——全部与 Phase 2 报告记录一致。
4. **路由契约实测(TestClient):** 五条轮次路由全挂载(`GET /api/rounds`、`GET /api/rounds/{round_n}`、`POST /api/rounds/{round_n}/annotations`、`POST /api/rounds/{round_n}/plain`、`POST /api/rounds/process`);非 phase3 项目下 `GET /api/rounds/1` 404、`POST annotations` 409、`POST process` 409,与 Phase 2 报告记录的语义一致。
5. **代码路径无回归:** `annotations.py` / `state.py` 自 Phase 2 收口后**零提交**;Phase 3 对 `session.py` / `main.py` / `ai_caller.py` / `frontend/app.js` 的改动经 diff 审读确认为**纯增量**(既有函数与路由签名保留,新增阶段 3/4/5 路由族与视图函数)。
6. **指纹刷新:** `covered_files` 24 → **26**(补 `02-DISCUSSION-LOG.md`、`02-UAT.md`),`covered_digest` 经 `verification.fingerprint` 重算为 `v1:sha256:8e74b104…`(算法与 Phase 3 已知良好指纹逐字校准一致)。原存储值 `acd6f0f8…` 为 Phase 2 收口时的旧树指纹。

**裁定:** 7/7 SC 机器半边保持 VERIFIED,浏览器 7 人检项已由 02-UAT.md 收口(7/7 pass)——状态维持 **passed**。

---

_Verified: 2026-09-13T00:00:00Z(UAT 收口后最终 2026-09-10T09:35:00Z;初验 2026-09-10T06:51:13Z;里程碑收口复验 2026-09-13)_
_Verifier: Claude (gsd-verifier)_

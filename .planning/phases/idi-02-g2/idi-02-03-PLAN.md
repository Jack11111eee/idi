---
phase: idi-02
plan: 03
type: execute
wave: 3
depends_on: ["idi-02-02"]
files_modified:
  - frontend/index.html
  - frontend/app.js
  - frontend/style.css
autonomous: false
requirements:
  - UI-01
  - UI-02
  - UI-04
  - FLOW-04
  - DATA-01

estimate:
  tokens: 95000
  raw_tokens: 95000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "阶段 3 的轮次文档视图替换 rounds-placeholder:左文档区渲染当前轮 discuss-round-N.md(markdown,renderMarkdown + stripUnsafeNodes 管线),侧栏切换为轮次批注流;阶段 1-2 视图(draft 渲染区)不绑划词事件(D-P2-1/D-P2-2/D-P2-20)← UI-04 / FLOW-04 呈现端"
    - "用户在轮次文档划选文字 → mouseup 检测 → 原生 Selection API 取选区 → 选区附近弹原生 DOM 小菜单,两项:「批注」「用大白话讲这段」;不引任何前端框架/第三方库(D-P2-1)← UI-01(浏览器面,人检为主)"
    - "划词后前端算好 quote = 精确选中文本、before = 选中起点往前 40 字(字符串切片,中文按字符计,不截断半字无妨),随 POST /api/rounds/{n}/annotations 发给后端(D-P2-3)← UI-01 before=40 字(边界:恰好 40 与超 40 两种输入同语义,仅前 40 进入字段)"
    - "选「批注」→ 输入 note → 后端建 pending 条目落盘;侧栏出现该条(quote 摘录 + note + status 徽标);文档区有批注的段落高亮(按 annotations 的 quote + locate 同语义重新定位包 <mark>,createElement/textContent,不用 innerHTML 拼接)(D-P2-4/D-P2-23)← UI-01 时(浏览器高亮为人检)"
    - "选「用大白话讲这段」→ 同步 POST /api/rounds/{n}/plain → 数秒内灰色斜体即时答气泡显示在侧栏该条目位置(type=plain 条目,answer 折叠展示),不进工作面板直播(D-P2-8/D-P2-10)← UI-02 时(浏览器面,人检)numbers-in-seconds"
    - "侧栏实时显示「本轮批注未处理数」(snapshot 的 pending_annotations;plain 不计),文档区有批注段落高亮至每条批注的 quote 处 ← UI-04(时序:建批注/处理完成后前端拉新 /api/session + /api/rounds 刷计数与视图——G-idi01-7 done 后拉新先例)← UI-04"
    - "点「处理本轮批注」→ POST /api/rounds/process(202)→ 工作面板全程直播这次调用(SSE 事件照常渲染);done 后拉新:新当前轮文档 + 上一轮视图变只读(轮次 < current_round → 划词菜单不绑 + 侧栏计数不显示 + 视觉灰化)← FLOW-04 / ROADMAP 成功判据 3、4"
    - "上一轮的 annotations 只读不可再批注:轮次切换器可浏览历史轮(docs 列表);历史轮视图只读(冻结 = 「下一轮存在」推导出的呈现,无独立状态,D-P2-20/D-P2-21);新批注 POST 被服务端 409 拦截(前端配合隐藏菜单)← FLOW-04"
    - "已解决批注变灰但不消失:answered 条目留在侧栏列表(CSS 灰化样式,不删条目)(D-P2-4/§4.2)← UI-01(浏览器面,人检)"
    - "批注内容(note/answer/quote)渲染一律走 renderMarkdown→stripUnsafeNodes 或 textContent,零 raw HTML 注入(D-P2-23/T-idi03-02 平移)← DATA-01 的 XSS 面"
  artifacts:
    - path: "frontend/index.html(扩展)"
      provides: "轮次视图骨架(前一轮被替代:文档区子视图 rounds-view = 轮次切换器 + markdown 渲染区;侧栏「本轮批注流」区;工作面板区「处理本轮批注」按钮)"
    - path: "frontend/app.js(扩展)"
      provides: "划词交互(initSelectionMenu:Selection API + mouseup + 原生弹菜单)、renderRoundView(轮次渲染 + 高亮)、renderAnnotations(批注流条目 + 灰化 plain 斜体)、processRound 触发与 done 后拉新、applySessionGates phase3 分支替换"
    - path: "frontend/style.css(扩展)"
      provides: "annotation 条目样式(pending 徽标 / answered 灰化 / plain 斜体灰 / mark 高亮 / 冻结轮只读灰化 / 弹菜单位置)"
  key_links:
    - from: "frontend/app.js applySessionGates"
      to: "GET /api/session(state=phase3)与 GET /api/rounds"
      via: "phase3 分支挂真轮次视图(替换 rounds-placeholder),pending_annotations 驱动计数徽标"
      pattern: "applySessionGates"
    - from: "frontend/app.js 划词菜单"
      to: "POST /api/rounds/{n}/annotations 与 POST /api/rounds/{n}/plain"
      via: "前端算好 quote/before(40 字)随 body 发送;409 响应给中文提示(非当前轮)"
      pattern: "quote/before"
    - from: "frontend/app.js SSE done 收流"
      to: "refreshGatesAfterStream 拉新链"
      via: "process_round done 后拉 /api/session + /api/rounds → 新当前轮 + 上轮冻结灰化(G-idi01-7 先例)"
      pattern: "done 后拉新"
  prohibitions:
    - statement: "划词交互不得引入前端框架/第三方库(浏览器原生 Selection API + 原生 DOM,D-P2-1/§9)"
      status: unverified
      flagged: true
    - statement: "阶段 1-2 视图(draft 渲染区)不得绑定划词事件(D-P2-2:§4.2 阶段 1-2 无划词批注)"
      status: unverified
      flagged: true
    - statement: "划词高亮与批注内容渲染不得用 innerHTML 拼接用户/AI 内容(必须 createElement/textContent 或 renderMarkdown→stripUnsafeNodes,D-P2-23)"
      status: unverified
      flagged: true
    - statement: "冻结只读不得引入新后端状态或标记(冻结 = 「下一轮存在」的纯前端呈现,权威在 derive_state,CODEX D-P2-20/D-P2-21 注:前端只是显示;服务端 409 是防线)"
      status: unverified
      flagged: true
    - statement: "「处理本轮批注」不得在非 phase3 状态可点(按钮可用性由 snapshot state 判定,服务端 409 兜底防绕过)"
      status: unverified
      flagged: true
    - statement: "phase4/phase5/mission_complete 的视图分支不得在本计划触碰(本阶段只覆盖 phase3 分支,placeholder 维持现状,CODEX 边界裁决③)"
      status: unverified
      flagged: true
---

## Phase Goal

**As a** 批注讨论中的用户,**I want to** 对当前轮文档划词写实质批注或即时要大白话,在侧栏看到未处理数和高亮,点「处理本轮批注」看到全程直播,然后上一轮自动冻结只读,**so that** DESIGN.md §4.2 的划词批注交互完整落地,轮次收敛循环在浏览器里可用。

<objective>
Wave 3 前端收口:把 Wave 2 定形的五条路由契约渲染成完整轮次交互——切片 1 替换 rounds-placeholder 为真轮次视图(文档渲染 + 批注流侧栏 + 未处理数);切片 2 划词弹菜单(原生 Selection API)与批注/大白话两入口;切片 3 高亮(quote 定位包 mark)、「处理本轮批注」按钮(done 后拉新 + 冻结灰化 + 轮次切换器)。全部用原生前端(无框架、无构建、无新依赖),XSS 管线全程复用 Phase 1 的 renderMarkdown + stripUnsafeNodes。

Purpose: UI-01/UI-02/UI-04 三条 REQ 的交互端全部落地;FLOW-04 的用户可见侧(点击 → 直播 → 冻结)收口;DATA-01 的渲染约束(不 raw HTML)平移到所有新数据入口。
Output: 浏览器可完整走一段「划词批注 → 处理本轮批注 → 下一轮产生 → 上一轮冻结」的界面(真实 AI 链在 idi-02-04 验证)。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/phases/idi-02-g2/02-CONTEXT.md
@.planning/phases/idi-02-g2/idi-02-PATTERNS.md
@.planning/phases/idi-02-g2/idi-02-02-SUMMARY.md

依赖接口(来自 Wave 2,前端只消费不重定义):
- GET /api/session → {state, current_round, rounds: [n,...], pending_annotations: 计数, ...}(已扩字段)
- GET /api/rounds → {rounds, current_round};GET /api/rounds/{n} → {round: n, document: 文本, annotations: {round, items}}
- POST /api/rounds/{n}/annotations {quote, before, note} → 200 {annotation} 或 409(非当前轮/非 phase3)
- POST /api/rounds/{n}/plain {quote, before, question} → 200 {annotation}(answer 在 annotation.answer)或 409/502
- POST /api/rounds/process → 202 accepted / 409
- SSE /api/events 事件流照旧(工作面板渲染 AI 处理过程)

DESIGN.md 权威依据:
- §4.1(布局:左文档区划词→弹菜单、高亮 = 有批注、侧栏批注流 #3 已回应/#4 待处理、工作面板区「中止」+「处理本轮批注」按钮)
- §4.2(划词交互全条:小菜单两项、批注与被选原文绑定、AI 回复附在旁边、已解决变灰不删、每轮侧栏未处理数、阶段 1-2 无划词)
- §3.4(D-05:划选→提问→数秒内出解释不打断阅读)
- §3.5(D-07 冻结 = 只读归档呈现)
- §9(原生选区接口,引框架收益低)
- §3.8(界面中文文案)

分支纪律(per 仓库 CLAUDE.md §5):前端三文件大改动——执行者从当前分支 HEAD 切出 phase-02/idi-02-03 工作分支,plan 完成后合回原分支(工作分支生命周期与 plan 对齐,不引入 worktree)。
</context>

<tasks>

<task type="auto">
  <name>Task 1: 轮次视图骨架——替换 rounds-placeholder,文档渲染 + 批注流侧栏 + 未处理数</name>
  <reversibility rating="costly">applySessionGates 的 phase3 分支从占位切到真视图后,DOM 结构(容器 id 体系)成为后续两个任务与 Phase 3(只读归档态)的挂点;轮次视图的 DOM 骨架一旦被多任务引用,改动需协调三处。</reversibility>
  <files>frontend/index.html, frontend/app.js, frontend/style.css</files>
  <read_first>
  - frontend/index.html(40-97 行:doc-subview 结构、rounds-placeholder 53-57 行、session-panel / ai-panel 侧栏分区、approve-row 形态)
  - frontend/app.js(18-37 行 DOM 句柄区;59-71 行 renderMarkdown + stripUnsafeNodes;229-246 行 applySessionGates phase3 分支;312-320 行 refreshGatesAfterStream)
  - frontend/style.css(45-53 行灰色 hint;143-153 行 overlay;262-281 行 brainstorm 视图区样式先例)
  - .planning/phases/idi-02-g2/idi-02-PATTERNS.md(Modified Files #9:替换策略 extend-not-rewrite)
  - .planning/phases/idi-02-g2/02-CONTEXT.md(D-P2-20/D-P2-15)
  </read_first>
  <behavior>
    - phase3 快照进入:applySessionGates 的 phase3 分支显示新 rounds-view(轮次切换器 + 轮次文档 markdown 渲染),隐藏 draft-view;phase1_new/phase12_in_progress 分支行为不变(仍显示 draft-view)
    - phase4/phase5/mission_complete:并入现有 else 分支照旧显示(placeholder 语义保留,不触碰其内容)
    - GET /api/rounds 数据就绪后:侧栏「本轮批注流」区渲染 annotations 条目列表(quote 摘录 + note + status 徽标 + answer 折叠展示;plain 条目灰斜体)
    - 侧栏头部常驻计数:「本轮批注未处理数 N」(仅当前轮视图显示;历史轮不显示)
    - 轮次切换器(下拉或按钮组):列出 rounds,当前轮默认选中,切换时拉 GET /api/rounds/{n} 重渲染文档与批注
    </behavior>
  <action>(1)frontend/index.html:rounds-placeholder 容器内改造为真视图骨架(容器 id 保留 rounds-placeholder 或更名为 rounds-view——执行者取改动最小者并在 SUMMARY 记录;结构:轮次切换器 select#round-switcher + 轮次标题 + div#round-doc.markdown-body(轮次文档渲染)+ 冻结提示位)#;侧栏 session-panel 之后新增 section#annotations-panel(照 session-panel section 结构:「本轮批注流」header + span#pending-count 徽标 + div#annotation-list);ai-panel 的 probe-controls 区追加 button#btn-process-round(「处理本轮批注」,与既有「中止」同区——§4.1 布局图中两按钮同在工作面板区)。阶段 1-2 会话流区不动(进入轮次后 session-panel 由 applySessionGates 隐藏——照 phase 分支控制,D-P2-20 侧栏切换为批注流)。

(2)frontend/app.js:(a)DOM 句柄区追加新句柄(round-switcher/pending-count/annotation-list/btn-process-round/round-doc);(b)applySessionGates 的 else(非 phase1/phase12)分支扩:state === 'phase3' 时仍走同一容器但填充真数据——调 loadRoundsView()(新函数:async 拉 GET /api/rounds → 渲染切换器选项 → 默认选当前轮 → 拉 GET /api/rounds/{n} → renderRoundDocument + renderAnnotations);pending_annotations 计数写入 pending-count;非 phase3 的 else 态(phase4/5/mission_complete)保持现有 placeholder 文案行为(改用现在的 rounds-hint 更新文案,不删功能);(c)fetch 封装 roundApi(照 sendMessage 的 fetch JSON 形态);(d)切换器 change 事件 → 拉对应轮重渲染。**注意 extend-not-rewrite:applySessionGates 其余门控(divergence_available/g1_available 按钮态等)一行不动。**

(3)frontend/style.css:文件尾追加新样式块(#annotations-panel / .annotation-item / .annotation-pending 徽标橙色 / .annotation-answered 灰化(opacity 或 color:#999)/ .annotation-plain 灰斜体(font-style: italic; color:#999)/ .round-frozen 冻结灰化 / mark 引用高亮背景色 / 切换器样式)。

(4)renderAnnotations(annotations, is_current_round):条目循环 createElement——每条:quote 摘录(textContent 截断显示前 60 字)、note(renderMarkdown 渲染)、status 徽标(中文「已回应」/「待处理」)、answer 有值时折叠展示(details/summary 或 div 切换——实现取简,type=plain 条目直接灰斜体显示 answer)。**零 innerHTML 拼接**(D-P2-23)。历史轮(is_current_round=false):列表照渲染但侧栏不显示计数徽标 + 容器加 round-frozen 类(视觉灰化)。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && node --check frontend/app.js && (.venv/bin/uvicorn backend.main:app --port 8766 &) && n=0 && until curl -sf http://127.0.0.1:8766/api/health >/dev/null 2>&1; do n=$((n+1)); if [ $n -gt 120 ]; then lsof -ti:8766 | xargs kill 2>/dev/null; exit 1; fi; sleep 0.5; done && D=$(mktemp -d) && mkdir -p $D/docs && printf "# 第 1 轮\n\n第一段批注目标文字。\n\n> 申请授权:否\n" > $D/docs/discuss-round-1.md && printf "{\"round\":1,\"items\":[{\"id\":\"a1-01\",\"quote\":\"批注目标\",\"before\":\"第一段\",\"type\":\"comment\",\"note\":\"这里不清楚\",\"status\":\"pending\",\"answer\":null,\"created_at\":\"2026-09-09T00:00:00Z\"},{\"id\":\"a1-02\",\"quote\":\"批注目标\",\"before\":\"第一段\",\"type\":\"plain\",\"note\":\"什么是?\",\"status\":\"answered\",\"answer\":\"就是字面意思\",\"created_at\":\"2026-09-09T00:00:01Z\"}]}" > $D/docs/discuss-round-1.annotations.json && curl -sf -X POST http://127.0.0.1:8766/api/enter -H "Content-Type: application/json" -d "{\"path\": \"$D\"}" >/dev/null && curl -sf http://127.0.0.1:8766/api/session | grep -q "pending_annotations" && curl -sf http://127.0.0.1:8766/api/rounds/1 | grep -q "status" && curl -sf http://127.0.0.1:8766/ | grep -q "annotations-panel" && curl -sf http://127.0.0.1:8766/ | grep -q "btn-process-round"; rc=$?; lsof -ti:8766 | xargs kill 2>/dev/null; [ $rc -eq 0 ] && echo "rounds-view-ok"'</automated>
    <fails_when>node --check 报语法错误(退出非零——app.js 被改坏);uvicorn 起不来;assistantpending_annotations 响应缺失(grep 失败——快照字段未扩或服务未起);首页 HTML 不含 annotations-panel 与 btn-process-round(grep 失败——骨架未建);无 rounds-view-ok。</fails_when>
  </verify>
  <acceptance_criteria>
  - frontend/index.html 含 grep -q "annotations-panel"、grep -q "btn-process-round"、grep -q "round-switcher"(或执行者所选切换器控件 id,记入 SUMMARY)
  - frontend/app.js node --check 通过;grep -c "rounds-placeholder\|rounds-view" ≥ 1(真视图挂点替换占位)
  - /api/session 响应含 pending_annotations 键(curl 证明,值为造盘的 1——server 端字段已在 Wave 2 就绪,此处验证消费链路)
  - GET /api/rounds/1 返回 annotations 合并视图(curl grep status 命中)
  - app.js 中 applySessionGates 的 phase1_new/phase12_in_progress 分支行为未被破坏(grep "draft-view" 仍在)
  </acceptance_criteria>
  <done>轮次视图骨架就绪且造盘冒烟通过:phase3 目录进入后返回快照带轮次字段、单轮文档 + annotations 可拉、首页含批注流面板与处理按钮;JS 语法零错误。已 commit。</done>
</task>

<task type="auto">
  <name>Task 2: 划词弹菜单 + 批注/大白话两入口(原生 Selection API,零新依赖)</name>
  <reversibility rating="costly">划词菜单的交互形态(菜单两项、选区结束即弹、before=40 字)是 UI-01/UI-02 的用户直接触点,样式可调但事件流(mouseup → Selection → 菜单 → 分支动作)是批注入口的骨架。</reversibility>
  <files>frontend/app.js, frontend/index.html, frontend/style.css</files>
  <read_first>
  - frontend/app.js(Task 1 已建:roundApi 封装、renderAnnotations;347-360 行 showPermissionModal 原生 modal 先例;331-345 行 sendMessage fetch 形态)
  - frontend/style.css(143-153 行 .overlay 定位先例)
  - DESIGN.md §4.2(118-123 行:划词→弹小菜单→两项;批注与被选原文绑定)
  - .planning/phases/idi-02-g2/02-CONTEXT.md(D-P2-1/D-P2-2/D-P2-3/D-P2-8)
  </read_first>
  <behavior>
    - 鼠标在轮次文档区(round-doc 容器内)划选后松开:取 window.getSelection() → 选区非空且锚定在 round-doc 内 → 在选区末端附近(offset 定位)显示小菜单;点文档其他位置菜单消失
    - 选「批注」:弹轻量输入框(原生 prompt 或小 modal,实现取简)收 note → POST annotations {quote, before, note} → 成功后拉新侧栏(新条目 pending 徽标)→ 菜单消失;409(非当前轮) → toast/中文提示
    - 选「用大白话讲这段」:同样收 question(或直接「用大白话讲这段」就是 question 本身——形态:菜单第二项直接发送固定 question「用大白话讲讲这段」;实现取简并可加输入,记 SUMMARY)→ POST plain → 期待数秒返回 → 新 plain 条目灰斜体插入侧栏(answer 显示)→ 菜单消失
    - quote = 选区 toString() 精确文本;before = 选区起点在其文本节点中的前文字取末尾 40 字(String.prototype.slice(-40),字符计数)
    - 阶段 1-2 的 draft 渲染区划选无菜单弹(not-round-doc 容器不绑事件——D-P2-2)
    </behavior>
  <action>(1)frontend/app.js 新增 initSelectionMenu():(a)round-doc 容器 mouseup 监听:event 后 200ms 内读 window.getSelection();selection.isCollapsed(空选区)或 selection.toString() trim 为空 → 清除菜单返回;(b)判定选区是否落在 round-doc 内(selection.anchorNode 用 compareDocumentPosition 或 contains 判定——实现取简:menu 只在 round-doc mouseup 时出现);(c)菜单元素 = 预建 div#selection-menu(两个 button:「批注」「用大白话讲这段」),绝对定位在选区 getBoundingClientRect 附近(向右下偏移若干像素,不越视口边界——简单 clamp);document click 空白处隐藏;(d)分支动作:「批注」→ 收 note(原生 prompt(title「写批注」)——零依赖形态;若用小 modal 则照 permission-modal 结构建,实现者取简并记录)→ roundApi.postAnnotations(currentRound, {quote, before, note}) → 200 成功 → loadRoundView 刷新侧栏;409 → alertWarn(中文文案「仅当前轮可批注」;照既有错误提示形态);「用大白话讲这段」→ roundApi.postPlain(currentRound, {quote, before, question: "用大白话讲讲这段"}) → 200 → 把返回条目插入侧栏(灰斜体 answer);502 → 中文错误提示。(e)before 计算:定位选区起点的文本节点(anchorNode 为 text node 时取 anchorOffset 前的 data;取 .slice(-40);anchorNode 非文本(元素节点)时取空串 before=""(配对靠 quote 唯一性,合法降级,注释说明);(f)**冻结轮禁用**:当前视图的轮 < 当前轮(round_frozen)→ mouseup 不绑/直接返回(D-P2-21:历史轮不可批注)。

(2)frontend/index.html:body 尾(permission-modal 旁)加 div#selection-menu.hidden(两个按钮,结构照 modal-buttons)。

(3)frontend/style.css:#selection-menu 绝对定位小卡片(背景、阴影、圆角、z-index)、菜单按钮 hover 态。菜单移动端不优化(单机桌面,明细记录)。

(4)入口绑定:loadRoundsView 渲染当前轮文档后调 initSelectionMenu 的一次性绑定(menu 单例,handler 内部动态读当前显示轮判定)。**schema 反面确认:draft-view 容器与 chat 消息区绝不绑 mouseup 到此菜单**(验收 grep)。完成后自查:round-doc 渲染走 renderMarkdown→stripUnsafeNodes(既有函数直接复用);所有 quote/note/answer 出现处 textContent;无 .innerHTML = 拼接变量。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && node --check frontend/app.js && (.venv/bin/uvicorn backend.main:app --port 8766 &) && n=0 && until curl -sf http://127.0.0.1:8766/api/health >/dev/null 2>&1; do n=$((n+1)); if [ $n -gt 120 ]; then lsof -ti:8766 | xargs kill 2>/dev/null; exit 1; fi; sleep 0.5; done && D=$(mktemp -d) && mkdir -p $D/docs && printf "# 第 1 轮\n\n一段可划选的文字。\n\n> 申请授权:否\n" > $D/docs/discuss-round-1.md && curl -sf -X POST http://127.0.0.1:8766/api/enter -H "Content-Type: application/json" -d "{\"path\": \"$D\"}" >/dev/null && curl -sf -X POST http://127.0.0.1:8766/api/rounds/1/annotations -H "Content-Type: application/json" -d "{\"quote\": \"一段可划选的文字\", \"before\": \"# 第 1 轮 \", \"note\": \"看不懂这里\"}" | grep -q "a1-01"; rc=$?; lsof -ti:8766 | xargs kill 2>/dev/null; [ $rc -eq 0 ] && echo "annotation-post-ok"'</automated>
    <fails_when>node --check 语法错误;uvicorn 上限超时;POST annotations 返回非 2xx(curl -sf 失败——路由 409/400/500,服务链断);grep -q a1-01 失败(建条目未返回 id;响应长短或字段异常);无 annotation-post-ok——失败路径杀进程后无对账 echo。</fails_when>
  </verify>
  <acceptance_criteria>
  - frontend/app.js 含 `grep -c "getSelection\|selection-menu" frontend/app.js` ≥ 2(划词交互就位)
  - frontend/index.html 含 id="selection-menu" 元素与两个菜单按钮文案「批注」「用大白话讲这段」(grep -q 命中两中文按钮文案)
  - app.js 中无 draft-view/消息区容器的 mouseup 绑定引用 selection-menu(验收:grep 范围内 selection-menu 的引用仅出现于 round-doc 相关函数——代码审阅级)
  - POST annotations 端到端造盘冒烟成功(返回条目含 id a1-01——服务端建条目链路已被前端同一 API 验证)
  - CSS 含 #selection-menu 定位样式与 .annotation-plain 灰斜体样式(grep -q italic 命中)
  </acceptance_criteria>
  <done>划词弹菜单交互链就绪:划选→菜单→批注落盘(409 拦非当前轮)/大白话 plain 落盘灰斜体;阶段 1-2 视图无划词绑定;菜单纯原生 DOM 零新依赖。真浏览器划词视觉行为留人检(见 verification)。</done>
</task>

<task type="auto">
  <name>Task 3: 处理本轮批注按钮 + 高亮 + done 后拉新冻结 + 已回应变灰</name>
  <reversibility rating="costly">done 后拉新的刷新链(SSE done → refreshGatesAfterStream → 重进 phase3 视图拉新)沿 G-idi01-7 先例但扩到双端点(/api/session + /api/rounds),形成本工具的固定刷新模式,后续 Phase 3 按此扩展。</reversibility>
  <files>frontend/app.js, frontend/style.css, frontend/index.html</files>
  <read_first>
  - frontend/app.js(Task 1/2 已建:loadRoundsView/renderAnnotations/initSelectionMenu;312-320 行 refreshGatesAfterStream;SSE initEventSource 的 done 分发处)
  - frontend/style.css(Task 1 样式块;mark 标签默认样式)
  - DESIGN.md §4.2(高亮 = 有批注)、§4.4 G2(下一轮产生 = 本轮自动冻结)、§3.5(D-07)
  - backend/annotations.py(Wave 1:locate_quote 语义——前端高亮定位的同一语义参考:D-P2-6 前后端共用)
  - .planning/phases/idi-02-g2/02-CONTEXT.md(D-P2-4/D-P2-12/D-P2-20/D-P2-21/D-P2-22)
  </read_first>
  <behavior>
    - 「处理本轮批注」按钮:state == phase3 时可用(点击 POST /api/rounds/process;busy 时禁用防重复);非 phase3 禁用;202 后按钮进入处理中禁用态,直到 SSE done
    - SSE done 事件到达且在飞为 process_round 时:拉新 GET /api/session + GET /api/rounds → current_round 前进 → 重渲染新当前轮文档与空批注流,上一轮自动只读(通过切换器切回可见灰化态)
    - 高亮:当前轮文档渲染后,对该轮全部 annotations(含 answered 与 plain)的 quote 逐条在渲染后 DOM 的段落文本中定位并包 <mark>(按 quote 精确匹配 + before 优先语义,与 locate_quote 同思路的前端实现);找不到(冻结的文档理论上不会,但防呆)跳过不报错
    - 已回应批注(answered)条目灰化显示但保留在列表;处理完成后拉新侧栏可见 a1-01 状态从「待处理」变「已回应」+ answer 展示(后端回写的结果)
    - 历史轮视图(< 当前轮):不亮「处理本轮批注」、计数徽标隐藏、容器灰化(round-frozen 类)
    </behavior>
  <action>(1)「处理本轮批注」接线:btn-process-round click → busy 判定(照既有 btn-abort 逻辑风格读快照/全局态)→ POST /api/rounds/process;202 成功 → startProcessing UI(按钮禁用 + 文字「处理中…」,工作面板照常直播——SSE 事件已由 Phase 1 面板渲染,零新面板逻辑);409 → 中文提示;**SSE done 事件到达时**(initEventSource 既有 done 分支扩一小步:若 process_in_flight 标记为真 → 调 refreshRoundsAfterStream())结束恢复按钮。refreshRoundsAfterStream = 串行 fetch /api/session → applySessionGates(快照含新 current_round/rounds/pending_annotations)→ loadRoundsView()(拉新当前轮文档+annotations;拉新动作本身已经覆盖「上一轮冻结」——文档轮 < current_round 即渲染只读态,G-idi01-7 同型)。

(2)高亮 highlightAnnotations(roundDocEl, annotations):renderMarkdown 后的 fragment 已插入 DOM → 遍历段落文本节点(TreeWalker 或 querySelectorAll('p, li, td') 取 textContent 含 quote 的节点——实现取简)→ 用 quote 在节点全文 indexOf 定位 → 创建 range 或拆分文本节点包 mark 元素(createTextNode + surroundContents 或手工拆节点;**不重写 innerHTML**)→ 每条 annotation 一个 mark;answered/descendant 条目统一使用同一 mark 样式(区分靠侧栏,文档区 quote 高亮不区分状态——§4.1 仅「高亮 = 有批注」);多 annotations 同 quote 场景:首个命中位置即可(定位精度由 before 辅助的要求在侧栏条目,文档区重定位取简化,记录 SUMMARY)。异常防呆:quote 为空或找不到匹配 → 跳过该条继续(不抛)。

(3)冻结呈现(documented in summary):loadRoundsView(n) 渲染轮 n 时判定 n < current_round → 容器加 round-frozen 类(CSS 灰化 filter/opacity)→ 计数徽标 display:none、btn-process-round 禁用(仅当前轮可用)、initSelectionMenu 的 handler 读 same 条件直接 return(不弹菜单);n == current_round → 正常交互。

(4)frontend/style.css:补 mark 高亮背景(浅黄 amber 系)、round-frozen 灰化(opacity .55 或 saturate(0))、处理中按钮态。

(5)人检准备:真实浏览器 UAT 在 verification 步骤 3 记录清单(划词弹菜单/批注落盘侧栏/plain 灰斜体秒级回/处理直播/新旧轮冻结只读/已回应灰化不消失——六个观察点)。完成后自查:done 拉新链无轮询(纯事件驱动一拉);btn-process-round 在 phase4+ 状态被 applySessionGates 禁用(boundary:仅 phase3 开);高亮不产生页面重排循环(单次)。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && node --check frontend/app.js && (.venv/bin/uvicorn backend.main:app --port 8766 &) && n=0 && until curl -sf http://127.0.0.1:8766/api/health >/dev/null 2>&1; do n=$((n+1)); if [ $n -gt 120 ]; then lsof -ti:8766 | xargs kill 2>/dev/null; exit 1; fi; sleep 0.5; done && D=$(mktemp -d) && mkdir -p $D/docs && printf "# 第 1 轮\n\n目标文字甲。\n\n> 申请授权:否\n" > $D/docs/discuss-round-1.md && printf "{\"round\":1,\"items\":[{\"id\":\"a1-01\",\"quote\":\"目标文字甲\",\"before\":\"\",\"type\":\"comment\",\"note\":\"问\",\"status\":\"pending\",\"answer\":null,\"created_at\":\"2026-09-09T00:00:00Z\"}]}" > $D/docs/discuss-round-1.annotations.json && printf "# 第 2 轮\n\n新内容。\n\n## 批注回应表\n\n| 批注id | 原文摘录 | 回应 |\n|------|------|------|\n| a1-01 | 目标文字甲 | 已解释 |\n\n> 申请授权:否\n" > $D/docs/discuss-round-2.md && curl -sf -X POST http://127.0.0.1:8766/api/enter -H "Content-Type: application/json" -d "{\"path\": \"$D\"}" >/dev/null && curl -sf http://127.0.0.1:8766/api/session | grep -o "current_round[^,}]*" | grep -q 2 && curl -sf http://127.0.0.1:8766/api/rounds/1 | grep -q "a1-01"; rc=$?; lsof -ti:8766 | xargs kill 2>/dev/null; [ $rc -eq 0 ] && echo "freeze-view-ok"'</automated>
    <fails_when>node --check 语法错误;uvicorn 超时;session 快照的 current_round 不是 2(grep 失败——双轮造盘后推导态未前进,检查服务端链但更常是造盘文件末行标记不合规);rounds/1 合并视图拉不到(grep a1-01 失败——上一轮 annotations 冻结但可读的实现断链);无 freeze-view-ok。</fails_when>
  </verify>
  <acceptance_criteria>
  - frontend/app.js 含 `grep -q "btn-process-round"` 接线、`grep -c "refreshRoundsAfterStream\|refreshGatesAfterStream"` ≥ 2(done 后拉新链)
  - app.js 含高亮函数名(grep -q "highlightAnnotations" 或所选等名,记 SUMMARY);其实现中无 innerHTML 赋值拼接(源级别:高亮函数体内 grep "innerHTML" 为 0)
  - CSS 含 mark 元素高亮样式与 round-frozen 灰化样式(grep -q "round-frozen" style.css)
  - 双轮造盘冒烟:current_round=2 推导正确、rounds/1 上一轮 annotations 可读(curl 双验证)
  - node --check 全绿;全量后端回归不下降(本任务纯前端,后端测试应保持 Wave 2 完成时全绿——验证命令含 node --check 而后端无改动)
  </acceptance_criteria>
  <done>按钮链(点击→202→直播→done→拉新→新轮+冻结)闭合;高亮对渲染后文档段落包 mark;answered 灰化保留;历史轮只读三面(不弹菜单/隐藏计数/灰化容器);浏览器真实交互六点人检就绪。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 划选文本/批注 note/answer → 前端 DOM | 用户与 AI 产出的不可信文本经渲染进入 DOM——必须走 renderMarkdown→stripUnsafeNodes 或 textContent(D-P2-23) |
| 浏览器 → POST annotations/plain/process/rounds | 用户触发,round 参数可被绕过(冻结轮直写试探已被服务端 409 拦——纵深防御在此依赖 Wave 2) |
| GET /api/rounds/{n} 拉取 → renderMarkdown | AI 书写的轮次文档是最大 XSS 面(document 全文直接渲染) |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi02-12 | Tampering | note/answer/quote 注入 HTML/XSS(T-idi03-02 同族,新数据入口) | high | mitigate | 渲染齐走 renderMarkdown→stripUnsafeNodes 或 textContent;高亮 mark 构造 createElement;D-P2-23 全条;acceptance criteria 含高亮函数体内 innerHTML=0 |
| T-idi02-13 | Tampering | 前端解锁绕过(改 DOM 删除 disabled 让冻结轮可批注) | medium | mitigate | 前端禁用仅为呈现(纵深防御的逻辑记录),服务端 409 硬拦(Wave 2 已实现并已测);本层不新做防护 |
| T-idi02-14 | Denial of Service | 划词菜单重复触发(mouseup 高频弹叠) | low | mitigate | 菜单单例(pre 建 hidden 元素显隐),重复 mouseup 只改位置不重建 |
| T-idi02-15 | Information Disclosure | 大白话即时答含未消毒内容直接显示 | medium | mitigate | 灰斜体气泡内 answer 渲染经 renderMarkdown(textContent 或同一 strip 管线);与 chat 气泡同一防线 |
| T-idi02-16 | Tampering | 高亮定位错段(mark 包错文本误导用户以为批注挂别处) | low | mitigate | 前端定位用 quote 精确匹配 + before 辅助语义(与 locate_quote 同思路,D-P2-6 共用);找不到跳过不误标 |

执行说明:纯前端计划,无新包安装,无供应链项。
</threat_model>

<verification>
1. Task 1-3 automated:node --check + uvicorn 造盘冒烟(rounds-view-ok / annotation-post-ok / freeze-view-ok 三条对账输出)
2. 全量后端回归在 idi-02-02 完成后的基线上不变(本计划零后端改动;若执行者动了后端文件属越权)
3. 人检(UAT,浏览器一次走完六点):进入 phase3 项目 → ①划选弹两菜单项 ②点批注写 note 落盘、侧栏出现 pending ③点大白话拿到灰斜体即时答(数秒)④文档区被批注段落高亮 ⑤点处理本轮批注看直播、done 后新轮出现、上一轮灰化只读(切换器切回验证)⑥上一轮 answered 条目变灰含 AI 回答(answer 展示)。真 CLI 链(⑤ 的 AI 真实产出)在 idi-02-04 的 IDI_E2E 用例验证,人检可 Faker 造盘(挖空:⑤ 的 done 由收流模拟或下次真跑)
4. 浏览器人检 checklist 落 .planning/phases/idi-02-g2/idi-02-03-SUMMARY.md(UAT 结果逐项打钩)
</verification>

<success_criteria>
- UI-01:划词弹菜单两项、quote+before(40 字)绑定落盘、已解决灰化不删(高亮+灰化经人检)
- UI-02:大白话秒级灰斜体回、落盘 plain 条目、不进工作面板直播
- UI-04:侧栏未处理数(不含 plain)、文档区高亮
- FLOW-04 呈现端:处理按钮→直播→下一轮→上一轮只读(407 数据 409 拦截 + 前端冻结灰化)
- 零新前端依赖(node --check + 无 import/新 script 标签)
- 三条冒烟对账输出全绿
</success_criteria>

## Artifacts this phase produces(本计划新增符号清单)

- frontend/index.html:#selection-menu(划词菜单容器)、#annotations-panel(本轮批注流侧栏)、#pending-count(计数徽标)、#annotation-list、#round-switcher(轮次切换器)、#round-doc(轮次文档渲染区)、#btn-process-round(处理本轮批注按钮)
- frontend/app.js:loadRoundsView()、renderRoundDocument(text)、renderAnnotations(annotations, is_current_round)、initSelectionMenu()、computeBefore(selection) 或等名 before 计算辅助、highlightAnnotations(roundDocEl, annotations)、processRound()/refreshRoundsAfterStream()(done 后拉新链)、roundApi fetch 封装(postAnnotations/postPlain/getRound/process)、applySessionGates phase3 分支真视图化
- frontend/style.css:#annotations-panel、.annotation-item、.annotation-pending、.annotation-answered、.annotation-plain、.round-frozen、#selection-menu、mark 高亮规则块

<output>
Create `.planning/phases/idi-02-g2/idi-02-03-SUMMARY.md` when done
</output>

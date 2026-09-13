---
phase: idi-02-g2
plan: "03"
subsystem: ui
tags: [vanilla-js, selection-api, markdown-rendering, sse-refresh, annotation-highlight, rounds-view, xss-pipeline]

# Dependency graph
requires:
  - phase: idi-02-g2(plan 01)
    provides: backend/annotations.py(load/append_item/select_pending/locate_quote 定位语义)+ backend/grammar.py(§6.4 文法)——前端高亮定位与条目消费的数据契约
  - phase: idi-02-g2(plan 02)
    provides: 五条轮次路由(GET /api/rounds、GET /api/rounds/{n}、POST annotations、POST plain、POST process;202/409/400/404/502)与 _session_snapshot rounds/pending_annotations 字段——本计划的全部消费面
  - phase: idi-01-1-2
    provides: renderMarkdown + stripUnsafeNodes XSS 管线、applySessionGates 骨架、refreshGatesAfterStream done 后拉新先例(G-idi01-7)、原生 modal/事件/fetch 形态
provides:
  - frontend/index.html:轮次视图骨架(round-view-header + select#round-switcher + #round-doc + #rounds-hint)、侧栏 section#annotations-panel(#pending-count 徽标 + #annotation-list)、probe-controls 区 button#btn-process-round、body 尾 div#selection-menu(「批注」「用大白话讲这段」两按钮)
  - frontend/app.js:roundApi fetch 封装(list/get/postAnnotations/postPlain)、loadRoundsView/loadRoundView/renderRoundDocument/renderAnnotations/updateFrozenPresentation、initSelectionMenu(mouseup 检测 + 菜单单例 + 冻结轮禁用)、computeBefore(Range startContainer 方向无关 40 字)、highlightAnnotations + firstTextNodeContaining + findAllIndexes(TreeWalker 定位 + splitText 包 mark,与 locate_quote 同语义)、processRound 按钮接线 + refreshRoundsAfterStream(done 后拉新链)、applySessionGates phase3 分支真视图化(其余门控一行不动)
  - frontend/style.css:轮次视图样式块(切换器/批注条目/pending 橙徽标/answered 灰化/plain 灰斜体/mark 高亮/round-frozen 冻结灰化/selection-menu 弹卡/处理按钮)
affects: [idi-02-04 (IDI_E2E 前端全链消费本视图), idi-03 (phase4+ 占位分支与只读归档态 DATA-03 在彼阶段替换)]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
# Same estimateTokens scale (chars/4 over the realized diff), never a harness token count.
actuals:
  tokens: 7739    # 30957 diff chars / 4(git diff plan_head_before..HEAD, frontend/ only)
  tasks: 3
  commits: 3       # MEASURED: git rev-list --count 792d20b..HEAD(生产 3;SUMMARY 后再 +1)
  plan_head_before: 792d20baaa26ccfdc4173ae794d154d34bc5e7e1

# Tech tracking
tech-stack:
  added: []   # 零新增依赖:原生 Selection API + 原生 DOM,无框架无构建无新 script 标签(D-P2-1)
  patterns:
    - "before 方向无关算法:getRangeAt(0).startContainer/startOffset 取选区真正起点(反向拖拽时 anchorNode 是终点,locate_quote 的 before 二次定位会被反向起点败掉);text node 取 data.slice(0, startOffset).slice(-40);元素节点取空串配对靠 quote 唯一性"
    - "done 后拉新链双端点版(G-idi01-7 先例扩展):process_in_flight 标记 → SSE done/error → refreshRoundsAfterStream(串行 fetch /api/session → applySessionGates → loadRoundsView)→ 新当前轮 + 上轮冻结呈现,纯事件驱动零轮询"
    - "前端高亮与 backend.locate_quote 同语义(D-P2-6 前后端共用):TreeWalker 找含 quote 的文本节点 → findAllIndexes 枚举匹配 → 多处匹配优先『前文以 before 结尾』的那一处 → splitText 拆节点 + createElement('mark') + textContent 包裹(T-idi02-12 函数体零 innerHTML 拼接)"
    - "冻结轮四面呈现一处判定:displayedRoundNumber < currentRoundNumber → round-frozen 类 + 计数徽标 display:none + btn-process-round 禁用 + 划词 handler 直接 return(纯前端呈现,权威在 derive_state,服务端 409 是防线 D-P2-21)"

key-files:
  created: []
  modified:
    - frontend/index.html
    - frontend/app.js
    - frontend/style.css

key-decisions:
  - "切换器控件形态取 select#round-switcher(计划原文二选一:下拉或按钮组——选项含中文『当前』『历史·只读』标注,单控件零布局成本,detrieve 取简)"
  - "划词菜单一次性绑定 + menuSelection 快照:mouseup 即捕获 window.getSelection()(菜单动作延迟读会因选区清除而丢);绑定守卫 selectionMenuBound 防重复(T-idi02-14 单例语义)"
  - "「批注」收 note 用原生 window.prompt(零依赖形态,计划原文 min 形态二选一取证简);「用大白话讲这段」直接发固定 question『用大白话讲讲这段』不收输入(实现取简,计划行为列了两种形态,选定其一并记录于此)"
  - "容器 id 保留 rounds-placeholder 未更名(改动最小:acceptance 要求 grep rounds-placeholder|rounds-view ≥1 且 phase4+ 分支不触碰,保留原 id 零外部引用断裂)"
  - "answer 折叠展示用 details/summary(计划原文 three 选一取标准控件零 JS;plain 条目 ansEl.open=true 即时答案默认展开可见)"
  - "phase4+ 的 rounds-hint 更新为状态中文文案(计划 action:『改用现在的 rounds-hint 更新文案,不删功能』——占位语义保留与 phase3 分支共容器)"
  - "roundsHint 在 phase3 时隐藏(loadRoundsView 拉到数据即 classList.add('hidden')):与旧占位文案『已进入轮次阶段(本阶段占位)』互斥,失败路径恢复显示中文错误提示"

patterns-established:
  - "Pattern: 划词交互骨架 = round-doc mouseup → Selection 快照 → 弹菜单 → 选项分支 fetch → loadRoundView 拉新(后端不推状态,前端拉新即真相)——后续阶段 4 文档视图只读归档可平移禁用语义"
  - "Pattern: XSS 管线新入口全量复用:quote/note/answer 渲染齐走 renderMarkdown→stripUnsafeNodes 或 textContent;高亮 mark 构造 createElement/textContent(D-P2-23 平移先例 T-idi03-02)"
  - "Pattern: applySessionGates extend-not-rewrite:子视图分支只扩 phase3 真数据,phase1/phase12 与 phase4+ 分支行为零变化,divergence/g1 门控一行不动"

requirements-completed: [UI-01, UI-02, UI-04, FLOW-04, DATA-01]

# Coverage metadata (#1602) — one entry per shipped deliverable.
coverage:
  - id: D1
    description: "轮次视图骨架:phase3 分支替换占位为真视图(切换器 + round-doc markdown 渲染 via renderMarkdown→stripUnsafeNodes + 批注流侧栏 + pending_annotations 计数徽标);phase1/2 分支行为不变,phase4+ 占位文案保留"
    requirement: UI-04
    verification:
      - kind: automated
        ref: "node --check frontend/app.js(零语法错误)—— Task 1/2/3 各跑一次全绿"
        status: pass
      - kind: integration
        ref: "uvicorn 造盘冒烟(discuss-round-1.md + 2 条目 annotations.json)→ rounds-view-ok:/api/session 含 pending_annotations、GET /api/rounds/1 含 status、首页含 annotations-panel 与 btn-process-round、/api/enter 200"
        status: pass
      - kind: automated
        ref: "grep frontend/index.html:annotations-panel / btn-process-round / round-switcher 命中;grep frontend/app.js:draft-view 分支仍在"
        status: pass
    human_judgment: true
    rationale: "侧栏批注流条目与计数徽标的浏览器视觉呈现(条目布局/徽标样式/灰斜体观感)是 browser-only visual behavior——UAT routes to human/automated-browser session"
  - id: D2
    description: "划词弹菜单与两入口:round-doc mouseup → 原生 Selection API → 选区附近弹原生 DOM 小菜单两项;「批注」→ prompt 收 note → POST annotations(409 中文提示「仅当前轮可批注」);「用大白话讲这段」→ 固定 question → POST plain(502/409 中文提示);quote=toString()、before=Range 起点前 40 字(方向无关)、元素节点 before=\"\";冻结轮 handler 直接 return;阶段 1-2 视图零绑定"
    requirement: UI-01
    verification:
      - kind: integration
        ref: "uvicorn 造盘冒烟 → annotation-post-ok:POST /api/rounds/1/annotations {quote,before,note} 返回条目含 a1-01(前端同一 API 的建条目链路)"
        status: pass
      - kind: automated
        ref: "grep -c getSelection|selection-menu ≥ 2;index.html 含 id=selection-menu 与「批注」「用大白话讲这段」两文案;style.css 含 italic;mouseup 绑定仅 round-doc(代码审阅:app.js 中唯一 roundDoc.addEventListener('mouseup'))"
        status: pass
      - kind: unit
        ref: "computeBefore 源检:getRangeAt(0).startContainer/startOffset 实现(方向无关;非文本节点空串降级有注释说明)"
        status: pass
      - kind: automated
        ref: "全量后端回归 .venv/bin/python -m pytest backend/tests/ -q → 143 passed + 2 skipped(前端计划后端零改动)"
        status: pass
    human_judgment: true
    rationale: "真实浏览器划词行为(选区→菜单弹出位置/反向拖拽起点/菜单消失/中键选区边界)无法 headless 冒烟证明——契约接口与后端链路已证,视觉行为 UAT routes to human/automated-browser session"
  - id: D3
    description: "批注流条目渲染:quote 摘录 textContent 60 字截断、note/answer 走 renderMarkdown、中文徽标(已回应/待处理)、answered 灰化不删、plain 灰斜体 answer 展开;pending 徽标橙色;历史轮计数隐藏"
    requirement: UI-01
    verification:
      - kind: integration
        ref: "rounds-view-ok 冒烟内含造盘 2 条目(pending comment + answered plain)→ GET /api/rounds/1 返回合并视图(status 键命中);renderAnnotations 消费该结构"
        status: pass
      - kind: automated
        ref: "grep style.css:annotation-plain italic + badge-pending 橙(#b8860b 色系)+ annotation-answered 灰化(opacity .65)+ #pending-count 徽标样式命中"
        status: pass
    human_judgment: true
    rationale: "条目灰化/斜体/徽标颜色/折叠展开的视觉效果与交互(点 summary 展开 answer)是 browser-only visual behavior——UAT routes to human/automated-browser session"
  - id: D4
    description: "大白话即时答呈现:POST plain 200 → 拉新侧栏 plain 条目灰斜体显示 answer(ansEl.open 默认展开);不进工作面板直播(无 SSE 事件,零新面板逻辑);502/409 错误中文提示"
    requirement: UI-02
    verification:
      - kind: automated
        ref: "app.js plainAskBtn handler 源检:roundApi.postPlain → loadRoundView 拉新/plain 分支 502『大白话调用失败』/409 中文分支;answer 渲染经 renderMarkdown(T-idi02-15 灰斜体气泡内 strip 管线)"
        status: pass
      - kind: integration
        ref: "wave 2 已证 POST plain 契约(backend/tests/test_route_session.py#test_route_post_plain_answers / test_route_post_plain_502_on_ai_error);本计划前端消费同一 API(roundApi.postPlain)——契约面不重测,消费链路源检证实"
        status: pass
    human_judgment: true
    rationale: "数秒内回的即时答视觉呈现(灰斜体气泡、不打断阅读)是 browser-only visual behavior——UAT routes to human/automated-browser session"
  - id: D5
    description: "处理本轮批注按钮 + done 后拉新链:phase3 显示当前轮时可点、busy 禁用防重复、202 处理中禁用态直至 SSE done;done/error 且 process_in_flight → refreshRoundsAfterStream(fetch /api/session → applySessionGates → loadRoundsView 新当前轮 + 上轮自动冻结)——零轮询;409 恢复按钮 + 中文提示;按钮在 phase1/2/4/mission_complete 状态禁用"
    requirement: FLOW-04
    verification:
      - kind: integration
        ref: "uvicorn 双轮造盘冒烟 → freeze-view-ok:/api/session current_round=2 推导正确、GET /api/rounds/1 上轮 annotations 可读(a1-01)——拉新链消费的两数据面就绪"
        status: pass
      - kind: automated
        ref: "grep app.js:btn-process-round 接线命中、refreshRoundsAfterStream|refreshGatesAfterStream ≥ 2(实测 7);processRoundBtn 完整 busy/in_flight/statusCode 分支源检"
        status: pass
      - kind: automated
        ref: "app.js applySessionGates 源检:phase3 真分支 loadRoundsView、phase1/2 与 phase4+ 分支行为不变(draft-view grep 仍在);initSelectionMenu 在 displayedRound < currentRound 时直接 return"
        status: pass
      - kind: automated
        ref: "后端零改动证据:git diff 792d20b..HEAD --name-only = frontend/app.js + frontend/index.html + frontend/style.css"
        status: pass
    human_judgment: true
    rationale: "done 后新轮出现 + 上一轮灰化只读的完整时序视觉行为(直播过程 → 新轮切换 → 冻结观感)是 browser-only behavior——UIAR routes to human/automated-browser session;真 CLI 的 AI 真实产出链在 idi-02-04 IDI_E2E 用例"
  - id: D6
    description: "quote 高亮:highlightAnnotations 在渲染后 DOM 的段落文本节点定位 quote(TreeWalker)→ 多处匹配 before 辅助(locate_quote 同语义)→ splitText 拆节点包 mark(createElement+textContent);quote 空或找不到跳过不抛;每条 annotation 一个 mark 函数体零 innerHTML 拼接"
    requirement: UI-04
    verification:
      - kind: automated
        ref: "awk 提取 highlightAnnotations 函数体 → 非注释行 grep innerHTML = 0(doctored grep 验收语义:实际代码零 innerHTML;注释中『无 innerHTML』字样为说明文字)——highlightAnnotations / firstTextNodeContaining / findAllIndexes"
        status: pass
      - kind: automated
        ref: "grep style.css:mark 高亮(#fff3c4 浅黄 amber)命中"
        status: pass
    human_judgment: true
    rationale: "浏览器中 mark 高亮的视觉定位正确性(高亮位置 = 用户所见批注处、answered 与 pending 统一样式)是 browser-only visual behavior——UAT routes to human/automated-browser session"
  - id: D7
    description: "冻结只读呈现(纯前端,D-P2-21):displayedRoundNumber < currentRoundNumber → #round-doc.round-frozen 灰化(opacity .55 + saturate .6)+ 计数徽标隐藏 + 处理按钮禁用 + 划词 handler return;无新后端状态或标记(权威在 derive_state,服务端 409 硬拦)"
    requirement: FLOW-04
    verification:
      - kind: integration
        ref: "freeze-view-ok 冒烟:双轮造盘(第1轮含批注第2轮含回应表)后 current_round=2、rounds/1 上轮 annotations 可读——冻结判据『n < current_round』的两数据源经 curl 证明"
        status: pass
      - kind: automated
        ref: "grep 命中:app.js round-frozen 类挂载与 updateFrozenPresentation 分支;style.css round-frozen 规则存在(app.js initSelectionMenu 冻结判定源检)"
        status: pass
    human_judgment: true
    rationale: "切换器切回历史轮的灰化视觉观感(灰化 + 计数消失 + 划词无反应)是 browser-only visual behavior——UAT routes to human/automated-browser session"
  - id: D8
    description: "阶段 1-2 视图与 phase4+ 边界:phase1_new/phase12_in_progress 分支行为不变(draft-view 显示/隐藏 + 会话流,无划词菜单绑定——D-P2-2);phase4/phase5/mission_complete 并入现有 else 照旧显示占位语义(rounds-hint 文案更新),本计划未触碰其分支内容结构(CODEX 边界裁决③)"
    requirement: UI-01
    verification:
      - kind: automated
        ref: "grep app.js:draft-view 分支仍在;唯一 mouseup 绑定在 roundDoc(代码审阅);annotationsPanel 在 phase1/12 分支显式 classList.add('hidden')"
        status: pass
      - kind: automated
        ref: "全量后端回归 143 passed + 2 skipped(wave 2 完成基线之上不变——前端计划后端零改动)"
        status: pass
      - kind: integration
        ref: "rounds-view-ok 冒烟(1 轮 phase3 造盘)+ freeze-view-ok 冒烟(2 轮造盘):phase3 状态下 phase1/12 路径未被破坏(无回归信号)"
        status: pass
    human_judgment: false
  - id: D9
    description: "三条对账冒烟输出 + node check + 后端回归全绿(计划验证第 1、2 条的自动化半边)"
    requirement: DATA-01
    verification:
      - kind: automated
        ref: "node --check frontend/app.js → 零错误(final 轮绿色)"
        status: pass
      - kind: automated
        ref: "bash /tmp/idi-02-03-t1-smoke.sh → rounds-view-ok(执行两轮:T1 提交后与最终提交后)"
        status: pass
      - kind: automated
        ref: "bash /tmp/idi-02-03-t2-smoke.sh → annotation-post-ok(执行两轮:T2 提交后与最终提交后)"
        status: pass
      - kind: automated
        ref: "bash /tmp/idi-02-03-t3-smoke.sh → freeze-view-ok(执行两轮:T3 提交后与最终提交后;注:final 一轮曾失败一次,为前一进程占用 8766 的紫外线残留,kill -9 后隔离复跑通过,非代码问题,详见 Deviations)"
        status: pass
      - kind: automated
        ref: ".venv/bin/python -m pytest backend/tests/ -q → 143 passed + 2 skipped(wave 2 基线不降)"
        status: pass
    human_judgment: false

# Metrics
duration: 39 min
completed: 2026-09-10
status: complete
---

# Phase idi-02 Plan 03: 轮次收敛循环——前端轮次视图 Summary

**轮次视图(切换器+文档渲染+批注流侧栏+未处理数)替换 rounds-placeholder,划词弹原生菜单两项落盘(方向无关 before)、highlightAnnotations 包 mark、处理本轮批注按钮挂 done 后拉新链(新轮+上轮冻结灰化)——纯原生 JS 零新依赖,三条 uvicorn 冒烟对账全绿**

## Performance

- **Duration:** 39 min
- **Started:** 2026-09-09T17:37:38Z
- **Completed:** 2026-09-09T18:17:14Z
- **Tasks:** 3 / 3
- **Files modified:** 3(前端三文件,零后端改动)

## Accomplishments

- **轮次视图骨架落地(D-P2-20)**:applySessionGates 的 phase3 分支从占位切到真视图——GET /api/rounds 拉列表 → select#round-switcher 渲染选项(当前轮标注「(当前)」/历史轮标注「(历史·只读)」)→ 默认当前轮 → GET /api/rounds/{n} → round-doc 走 renderMarkdown→stripUnsafeNodes 渲染 + 批注流侧栏条目;pending_annotations 驱动计数徽标「本轮批注未处理 N」;extend-not-rewrite 达成(phase1/12 分支与 divergence/g1 门控一行不动,phase4+ 占位文案行为保留)
- **划词交互完整链(D-P2-1~3)**:round-doc 容器 mouseup → window.getSelection() 快照 → 菜单单例弹选区末端附近(视口 clamp)→ 两入口:「批注」prompt 收 note POST annotations(成功 loadRoundView 拉新 + refreshPendingCount,409「仅当前轮可批注」)/「用大白话讲这段」固定 question POST plain(200 拉新侧栏 answer 灰斜体默认展开,502/409 中文提示);computeBefore 用 Range startContainer 方向无关取 40 字,元素节点空串降级;冻结轮 handler 直接 return,阶段 1-2 视图零绑定
- **高亮 + 处理按钮 + done 后拉新链闭合(D-P2-4/D-P2-12/D-P2-21)**:highlightAnnotations(TreeWalker 定位 + findAllIndexes + before 辅助,与 backend.locate_quote 同语义)→ splitText 拆节点包 mark,函数体零 innerHTML(验收 doctored grep 通过);processRoundBtn busy 禁用 → POST process 202 处理中态 → SSE done/error 且 process_in_flight → refreshRoundsAfterStream(fetch /api/session → applySessionGates → loadRoundsView)→ 新当前轮 + 上轮 round-frozen 灰化 + 计数徽标隐藏,零轮询;冻结四面(灰化/藏计数/禁按钮/划词不弹)同源于 displayedRoundNumber < currentRoundNumber 判定

## Task Commits

Each task was committed atomically:

1. **Task 1: 轮次视图骨架——替换 rounds-placeholder,文档渲染 + 批注流侧栏 + 未处理数** - `1df3402` (feat)
2. **Task 2: 划词弹菜单 + 批注/大白话两入口(原生 Selection API,零新依赖)** - `09e62c3` (feat)
3. **Task 3: 处理本轮批注按钮 + quote 高亮 mark 包裹 + done 后拉新冻结链** - `4c9f147` (feat)

**Plan metadata:** 本 commit(docs: complete plan)

## Files Created/Modified

- `frontend/index.html` - 轮次视图骨架(round-view-header + #round-switcher + #round-doc + #rounds-hint 保留)、侧栏 #annotations-panel(#pending-count + #annotation-list)、#btn-process-round(与「中止」同区)、body 尾 #selection-menu 两按钮
- `frontend/app.js` - roundApi 封装 / loadRoundsView / loadRoundView / renderRoundDocument / renderAnnotations / updateFrozenPresentation / initSelectionMenu + computeBefore / highlightAnnotations + firstTextNodeContaining + findAllIndexes / processRoundBtn 接线 + refreshRoundsAfterStream / applySessionGates phase3 分支真数据
- `frontend/style.css` - 文件尾两段新样式块:轮次视图 + 批注流(切换器/条目/pending 橙/answered 灰化/plain 灰斜体)、划词菜单(#selection-menu 弹卡 + mark 高亮 + round-frozen 冻结灰化)

## Decisions Made

(均记录于 frontmatter key-decisions,此处挑三项展开)

- **切换器控件形态 = select 下拉**:计划原文「下拉或按钮组」二选一,取 select——选项直接承载「第 N 轮(当前)/(历史·只读)」中文标注,单控件零布局成本,与 ai-route-select 同族控件风格一致
- **「批注」的 note 输入用原生 window.prompt**:计划原文「原生 prompt 或小 modal,实现取简」——prompt 零依赖零新 CSS,符合 D-P2-1「不引库」+ Claude's Discretion 弹菜单视觉细节取简单者;若后续 UAT 认为体验不足,升级方向是照 permission-modal 结构建小 modal(记录为已知后续项,非 stub)
- **computeBefore 元素节点降级 + 冻结四面一判**:startContainer 为元素节点(如 triple-click 选整段或跨节点选区)时 before="":配对靠 quote 唯一性,与 backend.locate_quote 的 before 空串分支同语义;冻结四面(容器灰化/徽标藏/按钮禁/划词不弹)全部由 displayedRoundNumber < currentRoundNumber 单条判定派生——呈现逻辑一处收口,后续 Phase 3 只读归档态只扩大判定条件

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Task 1/2/3 verify 行整链 bash 命令无法以内联单命令过沙箱**
- **Found during:** Task 1(执行 verify 时;Task 2/3 同)
- **Issue:** PLAN `<verify>` 的整链 bash 命令(node --check + uvicorn 后台起 + until 等 health 循环 + mktemp 造盘 + 数个 curl 判定 + kill 收尾)超出权限沙箱对单条 Bash 命令的长度/引号接受度
- **Fix:** 按编排者指引把同样判定语义写为 /tmp shell 脚本逐任务执行(/tmp/idi-02-03-t1-smoke.sh / t2 / t3);判定行逐条保留原语义:health 等待 120×0.5s 上限、造盘文件字面一致、全部 curl grep 判定、结束 lsof -ti:8766 | xargs kill;输出对账 echo(rounds-view-ok / annotation-post-ok / freeze-view-ok)逐字保留
- **Files modified:** 无仓库文件(/tmp 三个临时脚本;沙箱禁止 rm,无害残留)
- **Verification:** 三条对账输出全绿(每条在 task 提交后 + 最终提交后各跑一轮,T3 final 轮的一次失败见下条)
- **Committed in:** 无(临时脚本不入库)

**2. [Rule 1 - Bug] final 验收轮 T3 冒烟一度失败——前一轮 T3 残留 uvicorn 进程占用 8766 端口**
- **Found during:** 全部任务完成后的 plan-level verification(Task 3 commit 后复跑三冒烟)
- **Issue:** T1+T2+T3 连跑时 T3 输出 FAIL rc=2(current_round grep 未命中 2):早前一次 T3 是在后台 until-loop 任务中跑的,其收尾 kill 是异步的,残留 uvicorn(PID 41208)仍在 8766 服务旧项目状态;复跑时新 uvicorn 绑定失败([Errno 48] address already in use),curl 命中了残留实例的项目(单轮/旧目录),current_round 判定错位
- **Fix:** kill -9 清残留进程后隔离复跑 T3 → freeze-view-ok 一次通过;后续 T1/T2 复跑也加了 kill+间隔,三冒烟在最终提交代码上全绿二次确认。非代码问题(T3 代码在 Task 3 commit 前后的两次干净运行都全过)
- **Files modified:** 无(仅进程清理)
- **Verification:** freeze-view-ok 复跑通过;端口最终 lsof 空
- **Committed in:** 无(环境清理)

---

**Total deviations:** 2 auto-fixed(1 Rule 3 blocking§冒烟脚本、1 Rule 1 environment§端口残留)
**Impact on plan:** 两个偏差都是执行层面:冒烟判定语义零变化(逐行保留 PLAN 字面),端口残留是 harness 异步收尾的测试环境问题且已在最终验收前清干净;零范围蔓延、零契约变化、零后端改动。

## Issues Encountered

None —— 三任务线性推进;node --check 三轮全绿;三条冒烟对账(task 后 + final 后两次)全绿;全量后端回归 143 passed + 2 skipped 与 wave 2 基线持平。T3 final 轮的端口残留问题见 Deviations(已定案为环境问题非代码缺陷)。

## User Setup Required

None - no external service configuration required.

## UAT Checklist(浏览器人检清单——结果全部 pending,待编排者自动化浏览器 UAT 或真人跑)

进入 phase3 测试项目(可用 Faker 造盘:一轮带批注的 discuss-round-1.md + annotations.json,或任何 phase3 磁盘形态目录),逐项观察:

| # | 观察点 | 期望 | 结果 |
|---|--------|------|------|
| ① | 划选弹两菜单项 | 在左侧轮次文档划选一段文字松开,选区末端附近弹小菜单,两项:「批注」「用大白话讲这段」;点文档其他位置菜单消失 | pending — orchestrator automated browser UAT to follow |
| ② | 批注落盘 + 侧栏 pending | 点「批注」→ prompt 输入 note → 侧栏出现新条目(pending 橙徽标 + quote 摘录 + note);「本轮批注未处理」计数 +1 | pending — orchestrator automated browser UAT to follow |
| ③ | 大白话灰斜体即时答(数秒) | 划选后点「用大白话讲这段」→ 数秒内侧栏该位置出现灰斜体「大白话回答」条目(默认展开显示 answer),不进工作面板直播 | pending — orchestrator automated browser UAT to follow |
| ④ | 文档区被批注段落高亮 | 有批注的 quote 文本处显示浅黄 mark 高亮(已回应与待处理统一样式,§4.1「高亮 = 有批注」) | pending — orchestrator automated browser UAT to follow |
| ⑤ | 处理直播 + done 后新轮 + 上轮灰化只读 | 点「处理本轮批注」→ 按钮变「处理中…」禁用,工作面板全程直播读文件/写文件;done 后自动切换到新当前轮(空批注流),切换器切回上一轮 → 灰化(round-frozen)+ 计数徽标隐藏 + 划词不弹菜单 | pending — orchestrator automated browser UAT to follow(真 CLI 的 AI 真实产出链在 idi-02-04 IDI_E2E;人检可 Faker 造盘,⑤ 的 done 由收流模拟或下次真跑) |
| ⑥ | 上一轮 answered 条目变灰含 AI 回答 | done 拉新后切换到上一轮:原 pending 条目变灰(已回应徽标)+ answer 折叠展开可见;条目不消失 | pending — orchestrator automated browser UAT to follow |
| 补 | 反向划选(从右往左拖拽) | 从右往左拖拽选一段文字做批注:批注绑定的 quote 与高亮位置与正向划选完全一致(before 取的是选区真正起点,不因拖拽方向变化) | pending — orchestrator automated browser UAT to follow |

## Next Phase Readiness

- **idi-02-04(IDI_E2E)**:前端视图已就绪——真 CLI 全链(划词批注 → process_round 真实产出新轮 → done 拉新 → 冻结呈现)的浏览器/端到端验证消费本计划交付的全部 UI 挂点;UAT 六点 + 反向划选观察点排入其对账清单
- **idi-03(Phase 3)**:phase4+ 分支的 rounds-hint 占位文案与 annotationsPanel 隐藏逻辑是收口边界——只读归档态(DATA-03)在该阶段替换 placeholder 时,draft-view/rounds-placeholder 的显隐骨架与 updateFrozenPresentation 的单条判定可直接扩展
- **「批注」prompt 体验**:note 输入现为原生 prompt(实现取简裁决);若 UAT 反馈多行/粘贴体验不足,升级为照 permission-modal 结构的小 modal——形态变更不触后端契约

## Self-Check: PASSED

- 关键文件:frontend/index.html FOUND、frontend/app.js FOUND、frontend/style.css FOUND(3/3)
- 提交:1df3402 FOUND、09e62c3 FOUND、4c9f147 FOUND(3/3)
- commits 实测:git rev-list --count 792d20b..HEAD = 3(生产 3 + 本 SUMMARY 1 = 4)
- node --check frontend/app.js:零错误(final 提交后复跑)
- 三条冒烟:rounds-view-ok + annotation-post-ok + freeze-view-ok(final 提交后全绿二次确认)
- 后端零改动:git diff 792d20b..HEAD --name-only = 3 个 frontend/ 文件,backend/ 不在列表
- 全量回归:143 passed + 2 skipped(wave 2 基线不降)
- 禁项自查:零新依赖(无 import/新 script 标签);高亮函数体非注释 innerHTML=0;mouseup 仅绑 round-doc;冻结零新后端状态

---
*Phase: idi-02-g2*
*Completed: 2026-09-10*

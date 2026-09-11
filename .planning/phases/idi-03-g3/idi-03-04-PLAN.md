---
phase: idi-03
plan: 04
type: execute
wave: 4
depends_on: ["idi-03-02", "idi-03-03"]
files_modified:
  - frontend/index.html
  - frontend/app.js
  - frontend/style.css
autonomous: false
requirements:
  - FLOW-05
  - DATA-02
  - DATA-03
  - DATA-04

estimate:
  tokens: 100000
  raw_tokens: 100000
  tasks: 3
  confidence: low

must_haves:
  truths:
    - "phase3 视图新增 #authorize-row(G3「授权撰写总设计文档」按钮 + hint,挂 rounds-placeholder 内照 approve-row 模式):按钮仅在 snapshot.g3_available 为 true 时可点(disabled + title 说明差在哪,照 g1_available 三态先例);点击 → 弹 #confirmation-modal 确认词模态 ← FLOW-05 / D-P3-26 / ROADMAP 判据 1"
    - "确认词模态(D-P3-3):输入框 + 放行按钮初始 disabled;输入值 strip 后全等「确认授权」才 enable(纯 textContent 比较,不进渲染管线);点放行 → POST /api/authorize → 200 则拉新 /api/session(state=phase4 视图);拒绝路径 = 关闭/取消/输入不符 → 不 POST 授权,弹拒绝批注入口(复用 window.prompt 或模态内 textarea 取拒绝原因,缺省「授权被拒,继续完善」)→ 走既有 POST /api/rounds/{n}/annotations 通道落 type=comment pending 批注(D-P3-5 拒绝转普通批注零新通道)→ 留在 phase3 继续下一轮 ← FLOW-05 / ROADMAP 判据 1"
    - "phase4 视图:撰写按钮常驻二态文案(无 tmp = 「撰写总设计文档」,有 tmp 无 DESIGN.md = 「继续撰写(检测到上次中断的半成品,重写覆盖)」——D-P3-10 字面);tmp 可见性 = snapshot 扩字段 writing_tmp_exists(bool,idi-03-02 Task 3 在 _session_snapshot 内伪层组装:state==phase4 时 (project/DESIGN.md.tmp).is_file() 一行,不碰 derive_state)——前端纯消费 s.writing_tmp_exists 切换按钮文案与 hint(崩溃恢复指引的判定源;点 → POST /api/writing 202 → AI 面板 SSE 直播 → done 拉新 → phase5_awaiting_tier)/ 模态文案点明「默认拒绝;拒绝后本轮仍可继续批注讨论」← DATA-02 / D-P3-10 / ROADMAP 判据 2"
    - "phase5_awaiting_tier 视图:#tier-modal 档位模态弹出(两选项「宽松」「严格」+ 各一句话说明,§8.2 口径);选择 → POST /api/checks/tier → 拉新(session 拉新后 state 仍 awaiting_tier 但已有 tier 签名 → 用户点「开始自检」按钮 POST /api/checks/start 或选档后直接起——按 D-P3-11 不自动起检,呈现「开始自检」按钮);已有 check 报告时打开项目 → 不弹模态照报告头部档位恢复 ← DATA-04 / D-P3-11 / ROADMAP 判据 3"
    - "phase5_checking 视图:#checks-panel 阶段 5 侧栏(报告列表 + 最新报告 markdown 渲染 + selfcheck.mode 控件区):mode='running' → 呈现「继续自检」按钮(意外中断恢复)+ 报告流直播照旧;mode='paused' → 隐藏继续自检、呈现抛问裁决卡列表 + 输入控件(questions 键 = {number, text}——修复者抛问文本)与输入控件;mode='p2' → 隐藏继续自检、呈现残余裁决卡(questions 键 = {number, location, issue, suggestion}——D-P3-17 卡三字段 位置/描述/建议修法 + number,来自问题分级表,与后端 snapshot 组装形状一字不差);mode='resumed' → 只呈现「继续修复」按钮;裁决卡(纯 P2 残余)每问题一卡两按钮「修」「接受现状」+ 输入 note → POST /api/checks/verdict;「继续修复」→ POST /api/checks/repair ← DATA-04 / D-P3-17 / D-P3-20 / D-P3-26 / ROADMAP 判据 4"
    - "mission_complete 视图:一次性欢呼模态 #mission-complete-modal(「使命完成——总设计文档已通过自检,项目进入只读归档态」;判定 = 本次会话首次见到 state==mission_complete,会话内存标记不落盘,重开重现弹一次)+ 只读归档态(D-P3-25:DESIGN.md 默认渲染 + 轮次切换器复用 + check 报告列表可浏览;划词菜单不绑(currentState!=='phase3' 防线天然生效)、「处理本轮批注」隐藏、G3 按钮隐藏、发散/发送输入面隐藏或禁用)← DATA-03 / D-P3-24 / D-P3-25 / ROADMAP 判据 5"
    - "XSS:阶段 5 全新数据(check 报告/DESIGN.md/裁决问题文本/AI 回复)一律 renderMarkdown→stripUnsafeNodes 或 textContent 渲染,零 innerHTML 拼接(D-P3-28/T-idi03-02);确认词输入靠 textContent 全等比较不进渲染管线 ← DATA-03/DATA-04 的 XSS 面"
    - "done 后拉新链:撰写/核查/修复调用 done → fetch /api/session + /api/design + /api/checks → 视图重取(照 refreshRoundsAfterStream 模式,D-idi01-7 先例;不新增专用收尾事件)← D-P3-27/D-P3-28"
    - "「继续撰写/继续自检/继续修复」按钮族与崩溃恢复:重开项目按 derive_state + selfcheck.mode 自动呈现对应恢复按钮(无需重新确认词,§7.3 原文);文案区分「撰写总设计文档」vs「继续撰写」← DATA-02 / ROADMAP 判据 2"
  artifacts:
    - path: "frontend/index.html(扩展)"
      provides: "#authorize-row、#confirmation-modal、#tier-modal、#mission-complete-modal、#checks-panel、#design-view 骨架元素(照 permission-modal overlay 与 annotations-panel section 形态)"
    - path: "frontend/app.js(扩展)"
      provides: "applySessionGates else 分支的 phase4/phase5/mission_complete 真视图替换(占位文案退场)+ 确认词模态逻辑 + 档位模态 + 欢呼模态 + 裁决卡渲染 + 继续按钮族 + done 拉新链"
    - path: "frontend/style.css(扩展)"
      provides: "G3 按钮样式(#btn-authorize 照 #btn-approve-draft)、verdict-card 卡片、灰化只读态、报告切换器、declare 灰斜体、三模态共用 overlay 外壳复用"
  key_links:
    - from: "frontend/app.js applySessionGates else 分支"
      to: "GET /api/session(state=phase4/5/mission_complete + g3_available + selfcheck)+ GET /api/design + GET /api/checks"
      via: "phase4 → 撰写按钮;phase5_awaiting_tier → 档位模态 + 开始自检;phase5_checking → 报告视图 + mode 控件;mission_complete → 归档视图 + 一次性欢呼模态"
      pattern: "applySessionGates"
    - from: "frontend #confirmation-modal 放行按钮"
      to: "POST /api/authorize"
      via: "确认词 strip 全等「确认授权」才 enable;后端四查再查是安全边界(前端只是呈现)"
      pattern: "confirm-word"
    - from: "frontend 裁决卡按钮 + 「继续修复」"
      to: "POST /api/checks/verdict 与 POST /api/checks/repair"
      via: "逐条裁决落盘(单飞)→ 残余清零后端自动收口 → 拉新呈 mission_complete"
      pattern: "verdict-append"
  prohibitions:
    - statement: "确认词校验不得放行到后端解析(后端不重复解析自然语言;唯一防线 = 四查 + 后端写 AUTHORIZATION.md 动作;前端全等比较纯展示层防呆,D-P3-3)"
      status: unverified
      flagged: true
    - statement: "phase3 已定版式不得重排(轮次视图/批注流/划词交互零修改;新视图只在 else 分支与新增容器内);子视图切换沿用现有 DOM 结构,不新增路由(D-P1-14 单页原则)"
      status: unverified
      flagged: true
    - statement: "mission_complete 只读归档不得新增归档标志文件或后端状态(呈现 = 推导态;关闭动作全部是入口判定不满足,服务端 409 是防线,D-P3-25)"
      status: unverified
      flagged: true
    - statement: "欢呼模态标记不得落盘(会话内存标记;重开项目重现弹一次符合「重开即弹」语义,D-P3-24)"
      status: unverified
      flagged: true
    - statement: "「继续自检」不得用于正常流程推进(正常推进是自动两跳;它仅担任意外中断恢复——报告未完整/调用挂死时重跑当前核查轮,D-P3-20/§7.3②);不得在 paused/resumed 两态呈现"
      status: unverified
      flagged: true
    - statement: "阶段 5 新数据渲染不得用 innerHTML 拼接用户/AI 内容(renderMarkdown→stripUnsafeNodes 或 textContent,D-P3-28/T-idi03-02)"
      status: unverified
      flagged: true
    - statement: "不引入前端框架/第三方库(原生 Selection API + 原生 DOM);不新增第三方依赖"
      status: unverified
      flagged: true
---

## Phase Goal

**As a** 走到后半程的用户,**I want to** 在浏览器里走完「G3 授权确认 → 撰写直播 → 选档 → 自动循环核查修复 → 残余裁决/继续修复 → 使命完成欢呼 → 只读归档」的完整可视化旅程,**so that** Phase 3 的四个 REQ 在界面上全部可用,任何崩溃中断后重开即看到正确的「继续」按钮。

<objective>
Wave 4 前端收口:applySessionGates 的 else 分支占位文案(274-279 行)替换为阶段 4/5/完成态真视图。切片 1 = G3 授权交互(按钮显隐 + 确认词模态 + 拒绝转批注)+ phase4 撰写视图;切片 2 = 档位模态 + phase5_checking 报告视图与裁决控件(四 mode:running/paused/p2/resumed)+ 残余裁决卡;切片 3 = mission_complete 欢呼模态 + 只读归档视图。全部原生 DOM(无框架无新依赖),XSS 管线全程复用 renderMarkdown→stripUnsafeNodes。

Purpose: FLOW-05 的用户可见侧(按钮点亮→确认词→拒绝即批注)、DATA-02 的三个继续按钮、DATA-04 的档位与裁决交互、DATA-03 的使命完成与归档呈现收口;真正的浏览器人检 UAT 在 idi-03-05。
Output: 浏览器可完整走「确认词授权 → 撰写 → 选档 → 循环 → PASS 欢呼 → 归档浏览」的界面(真 AI 链在 idi-03-05 E2E + 人检)。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/phases/idi-03-g3/03-CONTEXT.md
@.planning/phases/idi-03-g3/idi-03-PATTERNS.md
@.planning/phases/idi-03-g3/idi-03-02-SUMMARY.md
@.planning/phases/idi-03-g3/idi-03-03-SUMMARY.md

依赖接口(来自 Wave 2/3 后端契约,前端只消费不重定义):
- GET /api/session → {state, g3_available, selfcheck: {tier, mode, questions}, ...}(既有字段照旧)
- POST /api/authorize(无请求体)→ 200 {state: 新推导} / 409
- POST /api/writing → 202 / 409;POST /api/checks/tier {tier} → 200 / 400 / 409;POST /api/checks/start → 202/409;POST /api/checks/repair → 202/409;POST /api/checks/verdict {number, decision, note} → 200 / 409 / 400
- GET /api/design → {design: 文本|null};GET /api/checks → {checks: [...], latest: 报告全文, selfcheck}
- SSE /api/events 事件流照旧(撰写/核查/修复循环全程直播)
- POST /api/rounds/{n}/annotations(拒绝路径复用,零新通道)

DESIGN.md 权威依据:
- §4.4(G3 交互:确认词 + 默认拒绝 + 拒绝=普通批注)、§4.1/§4.2(布局与划词,归档态不可用的依据)、§7.3①②(继续按钮语义)、§7.4(只读归档态:可浏览/不可改)、§8.1(G3)、§8.2(档位选择时机与两态界面规格:暂停态/裁决待续跑态的控件清单——check-14 锁定版)、§3.8(界面中文文案)
- D-21(只读归档)、D-22(逐条裁决卡)

分支纪律(per 仓库 CLAUDE.md §5):前端三文件大改动——执行者从当前分支 HEAD 切出 phase-03/idi-03-04 工作分支,plan 完成后合回原分支(不引入 worktree)。

预算边界说明(checker advisory,本计划 estimate 处 100k/100k 满额):切片 1/2/3 即天然收口边界(Task 间边界);若任一 Task 中途 context 压力接近 70%,收口当前 Task(冒烟 sentinel 必须先跑通)并把剩余 UI 细化项记 SUMMARY「未竟清单」交 idi-03-05 人检时核对——禁止为省 context 而砍 behavior 列表的按钮/控件承诺(三 mode+p2 控件清单是锁定版,不可删)。
</context>

<tasks>

<task type="auto">
  <name>Task 1: G3 授权交互——#authorize-row 按钮显隐 + 确认词模态 + 拒绝转批注 + phase4 撰写视图</name>
  <reversibility rating="costly">确认词模态的放行语义(输入「确认授权」strip 全等才 POST)与拒绝转批注通道复用是 FLOW-05 的字面契约;phase4 视图的按钮文案(撰写 vs 继续撰写)配合磁盘 tmp 判定,改动即破坏崩溃恢复指引。</reversibility>
  <files>frontend/index.html, frontend/app.js, frontend/style.css</files>
  <read_first>
  - frontend/app.js(260-320 applySessionGates 完整函数——else 分支即挂点;608-621 showPermissionModal 模态模子;295-307 approve-row 按钮三态消费;840-878 processRoundBtn click→POST→SSE→refresh 完整模子;880-892 refreshRoundsAfterStream 拉新链)
  - frontend/index.html(47-53 approve-row 结构;119-129 permission-modal overlay;53-62 rounds-placeholder;81-90 annotations-panel section 形态)
  - frontend/style.css(143-174 .overlay/.overlay-card;245-254 #btn-approve-draft 绿色按钮 + disabled opacity 形态)
  - backend/session.py(Wave 2:g3_available/snapshot 字段语义与 authorize 三查)
  - DESIGN.md §4.4、§7.4 行 4(「继续撰写」文案)、§8.1
  - .planning/phases/idi-03-g3/03-CONTEXT.md(D-P3-3 / D-P3-5 / D-P3-10 / D-P3-26)
  - .planning/phases/idi-03-g3/idi-03-PATTERNS.md(Modified Files 6-7:index.html 新元素清单与 G3 按钮显隐先例详注)
  </read_first>
  <behavior>
    - phase3 四查合规(session g3_available=true):#authorize-row 显示、按钮可点;不合规(g3_available=false):按钮显示但 disabled + title 列出差哪条(照 g1_available 三态 title 先例)
    - 点「授权撰写总设计文档」→ #confirmation-modal 弹出:文案默认拒绝声明 + 输入框 + 放行按钮初始 disabled
    - 输入「确认授权」(前后空格容忍,strip 后全等)→ 放行按钮 enable;其他任何输入 → 保持 disabled
    - 点放行 → POST /api/authorize → 200 → 关模态拉新 /api/session(state=phase4 视图出现);409 → 错误提示留在模态内
    - 点取消/关闭/输入不符放弃 → 拒绝路径:弹出拒绝原因输入(默认文案「授权被拒,继续完善」)→ POST /api/rounds/{current_round}/annotations(type=comment pending 一条)→ 侧栏批注流出现该条 → 界面留在 phase3
    - phase4 视图:按钮文案二态(纯磁盘消费 snapshot.writing_tmp_exists——后端 snapshot 已在 phase4 态组装该字段):无 tmp = 「撰写总设计文档」+ hint「AI 将撰写总设计文档并整体落盘」;有 tmp 无 DESIGN.md = 「继续撰写(检测到上次中断的半成品,重写覆盖)」+ hint「残留的半份 tmp 将被整体覆盖重写」(D-P3-10 字面二态,检测到中断恢复时明确指引)+ 点击 POST /api/writing → 202 → SSE 直播照旧 → done 拉新
    - 非可用态点按钮 → 409 → 界面提示(按钮 disabled 防呆为主)
  </behavior>
  <action>(1)frontend/index.html:rounds-placeholder 内 Phase3 视图底部加 #authorize-row(照 #approve-row 结构:button#btn-authorize + p.hint#authorize-hint);permission-modal 之后新增 #confirmation-modal(overlay + overlay-card:标题「授权确认」+ 默认拒绝说明文案 + input#confirm-word-input + 按钮组:btn-confirm-authorize.primary(disabled) + btn-confirm-cancel.danger);style.css 加 G3 按钮样式(#btn-authorize 照 #btn-approve-draft 绿色系)+ 模态内 input 样式(新增分节注释「阶段 3/4/5 视图(PLAN idi-03-04)」)。

(2)frontend/app.js:(a)applySessionGates 的 phase3 分支内(authorize 显隐属 phase3 视图):按 data.g3_available 设 #btn-authorize disabled 与 title(三态文案:可点「四处机械校验已全部通过」;不可点列出四查哪条未过——后端快照未细分时统一 title「四处机械校验尚未全部通过:annotations/清单/维度表/授权标记」,简单优先);(b)新增 openConfirmModal / 绑定 #btn-authorize click → showConfirm;#confirm-word-input 的 input 事件 → strip 全等「确认授权」→ toggle #btn-confirm-authorize.disabled;(c)#btn-confirm-authorize click → fetch POST /api/authorize → 成功关模态 + refreshSession()(照既有拉新函数形态);失败 409 → 模态内错误文案;(d)拒绝路径:#btn-confirm-cancel 与 overlay 点击/ESC → 关闭确认模态并打开拒绝原因输入(择简实现:window.prompt('拒绝原因(将作为一条普通批注转给下一轮):', '授权被拒,继续完善')——app.js 763 行 window.prompt 先例;输入含文字则组 {quote: 当前轮文档标题或空串, before: '', note: 拒绝原因} POST /api/rounds/{data.current_round}/annotations;quote 择简取当前轮文档第一行标题文本(前端已知);完成后拉新(批注流出现新条));(e)applySessionGates else 分支新增 phase4 分支:rounds-placeholder 内呈现撰写视图区(照 PATTERNS「归 planner 择简」建议复用 rounds-placeholder 容器 + rounds-hint 文案 + 按钮 #btn-start-writing)+ **按钮文案二态按 snapshot.writing_tmp_exists 切换**(false = 「撰写总设计文档」,true = 「继续撰写(检测到上次中断的半成品,重写覆盖)」+ hint 明示覆盖语义——D-P3-10 逐字;纯消费后端快照字段,前端不自判 tmp 文件)+ done 拉新链(writingInFlight 模式照 processInFlight);(f)XSS:确认词输入 textContent 比较,拒绝批注走既有 annotations 渲染管线(零新面)。

(3)node --check 全量自检照旧。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && node --check frontend/app.js && (.venv/bin/uvicorn backend.main:app --port 8766 &) && n=0 && until curl -sf http://127.0.0.1:8766/api/health >/dev/null 2>&1; do n=$((n+1)); if [ $n -gt 120 ]; then lsof -ti:8766 | xargs kill 2>/dev/null; exit 1; fi; sleep 0.5; done && D=$(mktemp -d) && mkdir -p $D/docs && printf "## 覆盖维度表\n\n| 维度 | 状态 | 说明 |\n|---|---|---|\n| 目标与边界 | ✓ | ok |\n| 非目标 | ✓ | ok |\n\n## 未决问题清单\n\n| 编号 | 问题 | 状态 |\n|---|---|---|\n| 1 | 无 | 已决 |\n\n> 申请授权:是\n" > $D/docs/discuss-round-1.md && curl -sf -X POST http://127.0.0.1:8766/api/enter -H "Content-Type: application/json" -d "{\"path\": \"$D\"}" >/dev/null && curl -sf http://127.0.0.1:8766/api/session | grep -q "g3_available" && curl -sf -X POST http://127.0.0.1:8766/api/authorize >/dev/null && printf "# 设计\n\n内容\n" > $D/docs/../DESIGN.md.tmp && mv $D/DESIGN.md.tmp $D/DESIGN.md && printf "\n> 自检档位:宽松\n" > $D/docs/DESIGN-check-1.md && curl -sf -X POST http://127.0.0.1:8766/api/enter -H "Content-Type: application/json" -d "{\"path\": \"$D\"}" >/dev/null && curl -sf http://127.0.0.1:8766/api/session | grep -q "selfcheck" && curl -sf http://127.0.0.1:8766/ | grep -q "confirmation-modal" && curl -sf http://127.0.0.1:8766/ | grep -q "btn-authorize" && curl -sf http://127.0.0.1:8766/ | grep -q "btn-start-writing"; rc=$?; lsof -ti:8766 | xargs kill 2>/dev/null; [ $rc -eq 0 ] && echo "g3-frontend-ok"'</automated>
    <fails_when>node --check 语法错误(退出非零);uvicorn 起不来(等待循环 120 次后退出非零);任一 curl -sf 失败(enter/authorize/g3_available 或 selfcheck 的 grep 未命中);GET / 未含三元素 id 确认(confirmation-modal/btn-authorize/btn-start-writing 任一 grep 失败);无 g3-frontend-ok 输出(rc 在 kill 前捕获)。</fails_when>
  </verify>
  <acceptance_criteria>
  - frontend/index.html 含四个元素 id:逐名 grep -n 各命中(confirmation-modal / btn-authorize / btn-start-writing / authorize-row)
  - frontend/app.js 含 `grep -n "确认授权" frontend/app.js` 命中(确认词字面)且确认模态逻辑含 strip 比较(源码可见 trim/strip 形态),放行按钮初始 disabled
  - 拒绝路径调用 POST /api/rounds(源码 grep.app.js 可见 annotations fetch 分支与默认文案「授权被拒,继续完善」)
  - GET /api/session 响应含 g3_available 与 selfcheck 字段(冒烟已证);GET / 静态页含三元素
  - phase4 按钮二态:app.js 源码 grep 可见 writing_tmp_exists 消费分支与两段按钮文案字面(「撰写总设计文档」/「继续撰写(检测到上次中断的半成品,重写覆盖)」——D-P3-10 逐字,无合并文案变体)
  - phase3 既有视图(轮次渲染/批注流/划词)token 零变化(app.js 260-273 行 phase1/2/phase3 分支不动,git diff 零触碰)
  - node --check 通过
  </acceptance_criteria>
  <done>G3 交互浏览器可用:按钮四查驱动的三态、确认词模态 strip 全等放行、拒绝转普通批注走既有通道、phase4 撰写按钮与 done 拉新链就位;静态页与 API 冒烟证明元素在位。</done>
</task>

<task type="auto">
  <name>Task 2: 档位模态 + phase5_checking 报告视图与四 mode 控件 + 残余裁决卡</name>
  <reversibility rating="costly">selfcheck.mode 四态的控件清单(暂停/纯 P2 态隐藏继续自检 + 裁决落盘前不呈现继续修复;resumed 态只呈现继续修复)是 §8.2/check-14/D-22 锁定版界面规格——呈现错一个按钮就破坏「防误点重跑」承诺;questions 键集按 mode 二分(p2 四键 / paused 两键)是与后端 snapshot 的共享数据契约。</reversibility>
  <files>frontend/index.html, frontend/app.js, frontend/style.css</files>
  <read_first>
  - frontend/app.js(Task 1 已挂的 else 分支骨架;521-577 renderAnnotations 的 createElement 卡片模子——裁决卡照此;451-455 renderRoundDocument 的 innerHTML='' 清旧 + renderMarkdown 模式——报告渲染同款;131-148 dispatchEvent_ 的 done/error 收尾链)
  - frontend/index.html(annotations-panel 81-90 section 形态——#checks-panel 照抄结构)
  - backend/session.py(Wave 2:selfcheck 组装语义——mode: running/paused/resumed/p2/done;questions 两形态按 mode 区分:p2 = {number, location, issue, suggestion}(残余裁决卡,parse_problem_grades 映射)、paused = {number, text}(修复者抛问卡,scan_pending_questions 输出))
  - DESIGN.md §8.2(两态界面规格原文:暂停态 = 隐藏继续自检 + 呈现问题与输入框、裁决前不呈现继续修复;裁决待续跑态 = 只呈现继续修复)、§6.1(DESIGN-check-N)
  - .planning/phases/idi-03-g3/03-CONTEXT.md(D-P3-11 / D-P3-17 / D-P3-20 / D-P3-26 / D-P3-28)
  </read_first>
  <behavior>
    - phase5_awaiting_tier + 无 check 报告(选档未落或已落未起检):#tier-modal 弹出,两选项各一句话说明(宽松 = 一次核查+修复+追加 PASS 即止;严格 = 循环核查至零问题轮 PASS,纯 P2 轮交用户裁决);点选 → POST /api/checks/tier → 200 → 拉新后呈「开始自检」按钮(不自动起验,D-P3-11)
    - 重开 phase5_awaiting_tier 且已有 check 报告:不弹模态(照报告头部档位恢复——后端 selfcheck.tier 已从报告/签名文件组装,前端只呈现)
    - phase5_checking mode='running':报告视图(最新报告 markdown 渲染 + 报告列表切换)+ 「继续自检」按钮(POST /api/checks/start)+ SSE 直播照旧
    - mode='paused':继续自检隐藏;questions 每条一张抛问裁决卡(键 = {number, text}:抛问文本 + 输入 note + 两按钮「修」「接受现状」)→ POST /api/checks/verdict {number, decision: "修"|"接受现状", note};落盘后拉新(mode → resumed)
    - mode='p2':继续自检隐藏;questions 每条一张残余裁决卡(键 = {number, location, issue, suggestion}——D-P3-17 卡三字段:位置/描述/建议修法,number 供 POST;形状与后端 snapshot 组装一字不差)+ 两按钮「修」「接受现状」+ 输入 note → POST /api/checks/verdict;全部处理完 → 后端自动收口 PASS → 前端拉新见 mission_complete(Task 3 视图)
    - mode='resumed':只呈现「继续修复」按钮(POST /api/checks/repair);继续自检隐藏
    - 裁决卡落盘后后端自动收口(全部配对 → PASS 追加):前端拉新见 mission_complete(Task 3 视图)
    - 报告/DESIGN.md/AI 回复渲染经 renderMarkdown→stripUnsafeNodes;裁决卡问题文本 textContent(零 innerHTML 拼接)
  </behavior>
  <action>(1)frontend/index.html:permission-modal 之后加 #tier-modal(overlay-card:标题「选择自检档位」+ 两按钮 btn-tier-loose / btn-tier-strict 各带一句话说明文案);sidebar 的 annotations-panel 之后加 section#checks-panel hidden(header:待「自检报告」+ badge#check-state)+ 内部:#checks-list(报告切换器,select 或列表照 round-switcher 模式)+ #latest-check(.markdown-body)+ #check-controls(三个控件区:btn-continue-check「继续自检」/ 裁决卡容器 #verdict-cards / btn-continue-repair「继续修复」)。style.css 分节追加:verdict-card 卡片样式(照 .annotation-item 形态:位置/描述/建议修法三行 + 按钮组)、check 报告灰化样式、badge。

(2)frontend/app.js:(a)applySessionGates else 分支 phase5_awaiting_tier:呈现 rounds-placeholder 内档位引导 + 弹 #tier-modal(判定「无 check 报告」= snapshot.current_check 为 null 或 GET /api/checks 的 checks 列表空;会话内存防重复弹标记——同会话选过不再弹);已选档(checks.tier 非 null)不弹只呈现「开始自检」按钮(POST /api/checks/start);(b)phase5_checking:annotationsPanel 隐藏、#checks-panel 显示 + loadChecksView()(fetch GET /api/checks:渲染 checks 列表(切换器)+ latest 报告 renderMarkdown + 按 snapshot.selfcheck.mode 切控件区——running:btn-continue-check 显示;paused:#verdict-cards 渲染 questions 每条一张抛问裁决卡(位置行显示问题文本 q.text、number 记 data 属性)+ btn-continue-check 隐藏 + btn-continue-repair 隐藏;p2:#verdict-cards 渲染 questions 每条一张残余裁决卡(number/location/issue/suggestion 四字段:位置行 = q.location、描述 = q.issue、建议修法 = q.suggestion)+ 两按钮「修」「接受现状」+ note 输入框 → POST /api/checks/verdict {number: q.number, decision, note},两按钮隐藏与 paused 同;resumed:btn-continue-repair 显示其余两隐藏);(c)裁决卡:renderVerdictCard(question, mode) createElement 模式(textContent 填字段;**按 mode 取键**——mode == "p2" 用 q.location/q.issue/q.suggestion 三行渲染(D-P3-17 卡字段:位置/描述/建议修法),mode == "paused" 用 q.text 单行渲染(修复者抛问文本),q.number 两者都记到卡片的 data-number 供 POST)+ note 输入框 + 两按钮(「修」decision="修"、「接受现状」decision="接受现状")→ POST /api/checks/verdict → 拉新 loadChecksView + refreshSession;(d)#btn-continue-check → POST /api/checks/start(202/409 处理照 processRoundBtn 模子:disabled busy 防重复 + SSE 直播);#btn-continue-repair → POST /api/checks/repair 同模;(e)#btn-tier-loose/#btn-tier-strict click → POST /api/checks/tier {tier: "宽松"|"严格"} → 关模态拉新;(f)done/error 事件收尾:writing/checkInFlight 模式的 dispatched done → fetch /api/session + /api/checks 拉新(照 refreshRoundsAfterStream 拉新链;自动链起跳时 SSE 照直播)。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && node --check frontend/app.js && (.venv/bin/uvicorn backend.main:app --port 8766 &) && n=0 && until curl -sf http://127.0.0.1:8766/api/health >/dev/null 2>&1; do n=$((n+1)); if [ $n -gt 120 ]; then lsof -ti:8766 | xargs kill 2>/dev/null; exit 1; fi; sleep 0.5; done && D=$(mktemp -d) && mkdir -p $D/docs && printf "# 设计\n\n正文内容。\n" > $D/DESIGN.md && printf "# 第 1 轮\n\n内容\n\n> 申请授权:是\n" > $D/docs/discuss-round-1.md && printf "\n> 自检档位:严格\n\n## 问题分级\n\n| 编号 | 级别 | 位置 | 问题 | 建议修法 |\n|---|---|---|---|---|\n| 1 | P2 | §2 | 范围问题 | 明确边界 |\n\n> 待裁决:#1:范围问题\n" > $D/docs/DESIGN-check-1.md && curl -sf -X POST http://127.0.0.1:8766/api/enter -H "Content-Type: application/json" -d "{\"path\": \"$D\"}" >/dev/null && curl -sf http://127.0.0.1:8766/api/session | grep -q "paused" && curl -sf http://127.0.0.1:8766/api/checks | grep -q "问题分级" && curl -sf http://127.0.0.1:8766/ | grep -q "checks-panel" && curl -sf http://127.0.0.1:8766/ | grep -q "tier-modal" && curl -sf http://127.0.0.1:8766/ | grep -q "verdict-cards" && curl -sf -X POST http://127.0.0.1:8766/api/checks/verdict -H "Content-Type: application/json" -d "{\"number\": 1, \"decision\": \"修\", \"note\": \"按建议\"}" >/dev/null && curl -sf http://127.0.0.1:8766/api/session | grep -q "mission_complete" && E=$(mktemp -d) && mkdir -p $E/docs && printf "# 设计\n\n正文。\n" > $E/DESIGN.md && printf "# 第 1 轮\n\n内容\n\n> 申请授权:是\n" > $E/docs/discuss-round-1.md && printf "\n> 自检档位:严格\n\n## 问题分级\n\n| 编号 | 级别 | 位置 | 问题 | 建议修法 |\n|---|---|---|---|---|\n| 1 | P2 | §2 | 范围问题 | 明确边界 |\n\n> 核查结论:FIX(P2×1)\n" > $E/docs/DESIGN-check-1.md && curl -sf -X POST http://127.0.0.1:8766/api/enter -H "Content-Type: application/json" -d "{\"path\": \"$E\"}" >/dev/null && curl -sf http://127.0.0.1:8766/api/session | grep -q "\"p2\"" && curl -sf http://127.0.0.1:8766/api/session | grep -q "范围问题" && curl -sf -X POST http://127.0.0.1:8766/api/checks/verdict -H "Content-Type: application/json" -d "{\"number\": 1, \"decision\": \"接受现状\", \"note\": \"维持边界\"}" >/dev/null && curl -sf http://127.0.0.1:8766/api/session | grep -q "mission_complete"; rc=$?; lsof -ti:8766 | xargs kill 2>/dev/null; [ $rc -eq 0 ] && echo "selfcheck-frontend-ok"'</automated>
    <fails_when>node --check 语法错误;uvicorn 起不来;任一 curl/grep 失败:paused 未命中(报告待裁决未被 snapshot 判 paused)、纯 P2 盘(结论行 FIX·无待裁决行)未判 mode=p2 或 questions 未含问题表文本(残余裁决卡数据断链)、问题分级未入 GET /api/checks、静态页三元素(checks-panel/tier-modal/verdict-cards)任一缺失、verdict POST 失败或落盘后 mission_complete 未出现(残余收口链断)、无 selfcheck-frontend-ok 输出。</fails_when>  </verify>
  <acceptance_criteria>
  - frontend/index.html 五个元素逐一 grep -n 命中(tier-modal / checks-panel / verdict-cards / btn-continue-check / btn-continue-repair)
  - 暂停态/纯 P2 残余态/裁决待续跑态/running 四态的控件显隐逻辑在 app.js 可 grep(mode === 'paused' / mode === 'p2' / 'resumed' 分支)
  - 裁决卡取键与后端 snapshot 形状一字不差:mode='p2' 读 q.number/q.location/q.issue/q.suggestion、mode='paused' 读 q.number/q.text(源码 grep 可见两组键名;无读不存在键的 undefined 渲染——与 idi-03-02 Task 3 组装面的共享数据契约)
  - 裁决卡渲染无 innerHTML 拼接用户内容(createElement/textContent 模式;grep 裁决卡函数体内无模板字符串拼 innerHTML)
  - 冒烟:paused 判定 + verdict 落盘 + mission_complete 出现三步 API 链全通(抛问裁决收口);**纯 P2 盘(结论行 FIX、无待裁决行)判 mode=p2 + questions 含问题表文本 + 逐条 verdict(接受现状)→ 自动收口 mission_complete 第二链全通(D-22 残余裁决制端到端冒烟)**
  - phase4/phase3 既有视图零破坏(前端 phase1-3 分支零 diff)
  - node --check 通过
  </acceptance_criteria>
  <done>档位选择与报告视图浏览器可用;四 mode 控件清单与 §8.2/D-22 锁定版逐字一致(暂停与纯 P2 各呈对应裁决卡、resumed 只呈继续修复);纯 P2 残余裁决逐条交互闭环(冒烟:裁决落盘 → 后端收口 PASS → mission_complete)——判定→呈现→逐条 POST verdict→收口→mission_complete 整链经 mode='p2' 承载。</done>
</task>

<task type="auto">
  <name>Task 3: mission_complete 欢呼模态 + 只读归档视图</name>
  <reversibility rating="costly">只读归档态的「关闭实现 = 入口判定不满足」承诺(D-P3-25)意味着本任务不得引入任何归档标志/后端状态——呈现层一旦引入了状态文件,回退即破坏文件即状态原则。</reversibility>
  <files>frontend/index.html, frontend/app.js, frontend/style.css</files>
  <read_first>
  - frontend/app.js(Task 2 的 phase5 分支与 loadChecksView;renderRoundDocument 451-455;轮次切换器 round-switcher 消费模式)
  - frontend/index.html(permission-modal overlay 结构——#mission-complete-modal 照抄)
  - frontend/style.css(491-495 .round-frozen 灰化形态——归档态整体 opacity 参考)
  - backend/state.py(STATE_MISSION_COMPLETE 推导:最新 check 末行 PASS;零新增)
  - DESIGN.md §7.4(完成态段:可浏览全部轮次、批注、DESIGN.md 与核查报告;划词批注/处理本轮批注/授权按钮均不可用;不再追加轮次)、§8.2(终点:PASS → 弹「使命完成」提示)
  - .planning/phases/idi-03-g3/03-CONTEXT.md(D-P3-24 / D-P3-25)
  </read_first>
  <behavior>
    - state=mission_complete 首见(会话内存标记)→ #mission-complete-modal 弹出(「使命完成——总设计文档已通过自检,项目进入只读归档态」+ 关闭按钮);再次拉新不再弹(同会话);重开项目(新会话)重现弹一次
    - 关闭模态后进入归档视图:DESIGN.md 默认渲染(GET /api/design)+ 轮次切换器复用(浏览任一历史轮文档)+ check 报告列表可浏览(GET /api/checks latest 渲染)
    - 只读防线的呈现层:划词菜单不绑(既有 currentState !== 'phase3' 防线天然生效——验证即可,无新代码)、「处理本轮批注」隐藏(process-f 入口 409 服务端双防线)、「授权撰写总设计文档」隐藏(非 phase3 无处安放)、发散/发送消息输入面隐藏
    - API 冒烟:mission_complete 造盘下 GET /api/design 返回设计全文;GET /api/checks 返回报告与 done mode
  </behavior>
  <action>(1)frontend/index.html:#mission-complete-modal(overlay-card:欢呼标题 + 说明 + btn-mission-close「开始浏览归档」);app.js:(a)applySessionGates else 分支 mission_complete:呈现归档视图(复用 rounds-placeholder:round-switcher 切换轮次 + roundDoc 渲染 DESIGN.md 默认文→ 首次进入拉 GET /api/design 渲染,轮次切换时渲染所选轮文档;#checks-panel 保持可见——报告列表 + latest 渲染);(b)欢呼模态:会话级 let missionCelebrated = false(模块内存,不落盘);applySessionGates 见 state==mission_complete && !missionCelebrated → 去除 hidden → missionCelebrated = true;关闭按钮 → 加 hidden;(c)只读防线呈现层:归档视图下 btn-process-round.hidden、authorize-row.hidden、divergence-entry.hidden、message-input 禁用(disabled)——全部条件呈现,零后端改动(D-P3-25:服务端 409 是真防线,UI 只是呈现);(d)style.css:归档整体灰化容器样式(照 .round-frozen 模式 opacity 0.7 之类)+ 欢呼模态样式。

(2)自查:不新增任何归档标志文件/路由/状态(git diff 后端零变更——本任务只动前端三文件)。
  </action>
  <verify>
    <automated>bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && node --check frontend/app.js && (.venv/bin/uvicorn backend.main:app --port 8766 &) && n=0 && until curl -sf http://127.0.0.1:8766/api/health >/dev/null 2>&1; do n=$((n+1)); if [ $n -gt 120 ]; then lsof -ti:8766 | xargs kill 2>/dev/null; exit 1; fi; sleep 0.5; done && D=$(mktemp -d) && mkdir -p $D/docs && printf "# 设计\n\n这是归档的正文。\n" > $D/DESIGN.md && printf "# 第 1 轮\n\n内容\n\n> 申请授权:否\n" > $D/docs/discuss-round-1.md && printf "\n> 自检档位:宽松\n\n> 核查结论:PASS(一检一修即止)\n" > $D/docs/DESIGN-check-1.md && curl -sf -X POST http://127.0.0.1:8766/api/enter -H "Content-Type: application/json" -d "{\"path\": \"$D\"}" >/dev/null && curl -sf http://127.0.0.1:8766/api/session | grep -q "mission_complete" && curl -sf http://127.0.0.1:8766/api/design | grep -q "归档的正文" && curl -sf http://127.0.0.1:8766/ | grep -q "mission-complete-modal" && [ "$(curl -s -o /dev/null -w '%{http_code}' -X POST http://127.0.0.1:8766/api/rounds/process)" = "409" ]; rc=$?; lsof -ti:8766 | xargs kill 2>/dev/null; [ $rc -eq 0 ] && echo "archive-frontend-ok"'</automated>
    <fails_when>node --check 语法错误;uvicorn 起不来;mission_complete 造盘下 /api/session 未含 mission_complete(PASS 判定或造盘问题);/api/design 未含设计正文;/api/rounds/process POST 未返回 409(归档只读防线失效);静态页无 mission-complete-modal;无 archive-frontend-ok。</fails_when>
  </verify>
  <acceptance_criteria>
  - frontend/index.html 含 grep -n "mission-complete-modal" 命中;app.js 含 missionCelebrated 会话内存标记(grep 命中)且无落盘动作
  - git diff --stat 本任务零后端文件变更(backend/ 无 diff——只读归档零后端动作证明)
  - 归档造盘下:state=mission_complete + GET /api/design 全文 + POST /api/rounds/process 409 三断言过(冒烟)
  - 归档视图可浏览三源(DESIGN.md/轮次/check 报告——渲染函数复用既有管线,源码可见三处 renderMarkdown 调用)
  - 划词/处理本轮批注/授权按钮的隐藏在归档分支源码可见(三处 hidden 类操作)
  </acceptance_criteria>
  <done>「使命完成」欢呼模态(一次性、会话内存判定)+ 只读归档视图(DESIGN.md/轮次/报告三源可浏览,三交互面隐藏)就位;归档防线零后端改动、服务端 409 冒烟证明;浏览器人检 UAT 清单交 idi-03-05。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 浏览器 → 授权/自检 POST 系 | 确认词是呈现层防呆(前端 strip 全等),安全边界 = 服务端四查 + 后端写 AUTHORIZATION.md;自检按钮非法态点击由服务端 409 拦 |
| 阶段 5 新数据(报告/DESIGN/裁决文本)→ DOM | 全部不可信 AI/用户输入,渲染必须走 stripUnsafeNodes/textContent |
| 会话内存标记(欢呼模态)→ 重放 | 不落盘(重开重现弹出是设计语义),无安全面 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi03-15 | Tampering | 阶段 5 报告/DESIGN.md/AI 回复含恶意 HTML/脚本注入 DOM | high | mitigate | 全部经 renderMarkdown→stripUnsafeNodes 或 textContent(D-P3-28/T-idi03-02);裁决卡 createElement 模式;acceptance criteria 禁 innerHTML 拼接(grep) |
| T-idi03-16 | Elevation of Privilege | 确认词绕过(直接 POST /api/authorize) | critical | mitigate | 前端全等比较仅防呆;服务端 authorize() 四查 + phase3 再查(零绕过路径,D-P3-3/4);Wave 2 已测,本计划冒烟链复核 |
| T-idi03-17 | Tampering | paused 态误呈现「继续修复」导致重跑丢裁决 | high | mitigate | 控件清单照 §8.2 锁定版逐字实现(mode 三分支互斥);GET /api/checks/verdict 同号 409 二道防线;后端 repair_available 的 unpaired 检查(Wave 2 已交付)为服务端强制 |
| T-idi03-18 | Denial of Service | 「开始自检/继续修复」连续点击导致重复起跳 | medium | mitigate | 点击后 disabled + inFlight 标记(照 processRoundBtn 模子);202/409 分支恢复按钮 |

执行说明:纯前端三文件 + 零包安装(原生 DOM),无供应链项。
</threat_model>

<verification>
1. Task 1 automated:node --check + uvicorn 冒烟(G3 四查盘 → authorize → 设计落盘链 + 静态页三元素)
2. Task 2 automated:node --check + uvicorn 冒烟(paused 判定 + 问题分级报告 + verdict 落盘自动收口 mission_complete 全链)
3. Task 3 automated:node --check + uvicorn 冒烟(mission_complete + design 全文 + process 409)
4. 浏览器人检 UAT(确认词弹窗、模态文案、裁决卡布局、欢呼模态、归档浏览)在 idi-03-05 由用户执行,本计划只交付可冒烟的功能面
</verification>

<success_criteria>
- G3 交互三件(按钮三态/确认词模态/拒绝转批注)静态+API 冒烟通过;phase3 既有视图零破坏
- 档位模态 + 四 mode 控件 + 残余裁决卡全部就位,冒烟证明「裁决落盘 → 自动收口 → mission_complete」全链
- 欢呼模态一次性语义 + 只读归档三源可浏览三交互隐藏;零后端改动
- XSS 管线全程复用,零 innerHTML 拼接新数据
- 全部 verify 冒烟 sentinel(g3-frontend-ok / selfcheck-frontend-ok / archive-frontend-ok)可复现
</success_criteria>

## Artifacts this phase produces(本计划新增符号清单)

- frontend/index.html:#authorize-row、#btn-authorize、#authorize-hint、#confirmation-modal、#confirm-word-input、#btn-confirm-authorize、#btn-confirm-cancel、#tier-modal、#btn-tier-loose、#btn-tier-strict、#mission-complete-modal、#btn-mission-close、#checks-panel、#checks-list、#latest-check、#check-controls、#verdict-cards、#btn-continue-check、#btn-continue-repair、#btn-start-writing
- frontend/app.js:applySessionGates 的 phase4/phase5_awaiting_tier/phase5_checking/mission_complete 真视图分支、openConfirmModal/确认词全等放行/拒绝转批注链、chooseTier、loadChecksView、renderVerdictCard、verdict POST 链、btn-continue-check/repair 点击链、missionCelebrated 会话标记 + 归档视图渲染、done 拉新链扩展(writing/check 维度)
- frontend/style.css:「阶段 3/4/5 视图」分节(G3 按钮、确认词/档位/欢呼三模态共用外壳、verdict-card、checks-panel、归档灰化只读态)

<output>
Create `.planning/phases/idi-03-g3/idi-03-04-SUMMARY.md` when done
</output>

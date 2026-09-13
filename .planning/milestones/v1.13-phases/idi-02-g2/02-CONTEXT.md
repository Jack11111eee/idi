# Phase 2: 轮次收敛循环——划词批注、G2 与机器文法 - Context

**Gathered:** 2026-09-09
**Status:** Ready for planning
**Mode:** --auto(discuss-phase 单遍完成;决策源 = DESIGN.md v1.13,冲突处一律以 DESIGN.md 为准)

<domain>
## Phase Boundary

交付 DESIGN.md 范围内的"轮次收敛主循环":进入阶段 3(phase3 推导态)后,用户能对当前轮次文档划词写实质批注(或划词要一段大白话即时答),点「处理本轮批注」后 AI 按无状态调用量回应全部批注、产出 discuss-round-(N+1).md,上一轮(文档 + annotations)自动冻结只读,§6.4 机器文法的全部解析(维度表 / 未决清单 / 授权申请标记 / 批注回应表 / PASS 结论行 / 裁决追加 / 完整轮判据)由工具可靠实现并经正反例验证。

**In(本阶段做):** 划词弹菜单(UI-01)、大白话轻量无头调用与 plain 落盘(UI-02)、未处理数与高亮(UI-04)、G2「处理本轮批注」全流水线(FLOW-04)、§6.4 文法解析器 + 完整轮判据收口(FLOW-07)、annotations.json 字段与写回职责(DATA-01)、阶段 3 轮次视图(阶段 1-2 视图的既有占位被真视图替换)。

**Out(本阶段不做 → Phase 3):** G3 四处校验与确认词、AUTHORIZATION.md、DESIGN.md.tmp 原子落盘、G3 拒绝转普通批注(FLOW-05 / DATA-02 的撰写半边);宽松/严格自检档位、待裁决/裁决行落盘配对、继续撰写/继续自检/继续修复按钮、崩溃自愈的 Phase 4-5 侧(DATA-02 / DATA-04);使命完成提示与只读归档态(DATA-03;§6.4 中仅"PASS 结论行解析 + 裁决追加行判定式"两条文法属本阶段——它们是 FLOW-07 的机械校验部分,自检流程本身在 Phase 3)。

边界模糊处的裁决:①§6.4 的 PASS 行与裁决行**解析判定**归本阶段(FLOW-07 要求"文法全部由工具可靠解析",且 state.py 已实现 PASS 前缀判定——零成本收口),其**消费场景**(报告按钮逻辑)归 Phase 3;②冻结只读是纯前端呈现约束(后端按磁盘判),不需新后端状态;③中途接手(阶段 1-2 于 phase3 磁盘形态)无需任何新机制——derive_state 已把它判为 phase3,天然进入轮次视图。

</domain>

<decisions>
## Implementation Decisions

(auto 模式:全部承袭 DESIGN.md v1.13 既有决策/章节,无新造决策;每条标注 DESIGN.md 出处)

### 划词批注前端实现(UI-01 / UI-04 / §4.2 / §9)
- **D-P2-1:** 划词交互用浏览器原生 Selection API + mouseup 检测选区,划词后在选区附近弹原生 DOM 小菜单,两个菜单项:「批注」「用大白话讲这段」。不引任何前端框架/库,与 app.js 既有原生风格一致。理由:§9 技术栈表明确"划词高亮用浏览器原生选区接口,引框架收益低";D-P1-1 原生前端已锁定。
- **D-P2-2:** 划词菜单仅在**阶段 3 的轮次文档视图**内可用:阶段 1-2 视图(draft 渲染区)不绑划词事件——§4.2"阶段 1-2……此时无划词批注";阶段 4+ 本阶段不触达(placeholder 维持)。已完成 mission_complete 只读化属 Phase 3(DATA-03),本阶段不预留。
- **D-P2-3:** 批注选中时前端就把 quote/before 算好随 POST 发给后端:quote = 精确选中文本,before = 选中起点往前 40 字(按字符串切片,不截半个字也无所谓——中文按字符数计)。渲染层从选区两侧文本节点取内容。理由:§6.2 字段定义;"前 40 字"是 DESIGN.md 原文。
- **D-P2-4:** 有批注的文本做高亮(§4.1 文档区"高亮 = 有批注"):前端把渲染后的段落文本按 annotations 的 quote(+before 辅助)重新定位并包 `<mark>`。qa 定位逻辑共享一份(见 D-P2-6 的配对函数)。已解决批注(answered)变灰但不消失:CSS 灰化样式 + annotation 条目常驻,不删条目。理由:§4.2"AI 回复附在旁边;已解决批注变灰但不删除";UI-01 原文。

### annotations 数据层(DATA-01 / §6.2 D-18)
- **D-P2-5:** annotations 读写是独立纯模块 `backend/annotations.py`(与 state.py / transcript.py / g1.py 同级的零依赖 pathlib 模块),职责:parse(读 json)、append_item(建条目)、writeback(批量处理后回写 answer/status)、load(返回对象,不存在时返回空形态)。格式严格照 §6.2:`{"round": N, "items": [...]}`,字段 id/quote/before/type/note/status/answer/created_at 一字不差,不用 pydantic 存盘(存盘是 DESIGN.md 字面契约,pydantic 仅做 API 入口校验可选)。id 方案:`aN-NN`(如 a3-01)——N=轮次,NN=该轮条目递增序号——与 DESIGN.md §6.2 示例同构。理由:§6.2 字段写回职责(后端建条目、AI 不直接改写)——模块必须纯,才能在 AI 写乱轮次文档时不被连带污染。
- **D-P2-6:** quote+before 定位算法(纯函数,前端渲染与后端校验共用同一语义):在文档全文中找 quote 的精确匹配;多个匹配时用 before 做二次定位(找"before+quote"拼接的匹配,或匹配点前文以 before 结尾的那一处);仍不唯一取第一处。冻结保证被批注文本永不变化,所以精确匹配足够,不引入模糊匹配。理由:§6.2"定位靠精确文本匹配(quote + before 辅助);轮次冻结(D-07)保证被批注文本永不变化,无需更复杂算法"——DESIGN.md 直接否决了更复杂算法。
- **D-P2-7:** 批注条目仅由后端经 API 创建(status=pending 落盘);轻量即时答同样由后端落盘(type=plain,answer 即时写回,status 直接落 answered)。AI 子进程不直接改写 annotations 文件(权限上写 docs/ 虽放行,但 prompt 明确禁止 + 后端回写不依赖 AI 遵守)。理由:§6.2"字段写回职责"原文;D-18。

### 大白话轻量调用(UI-02 / §3.4 D-05 / D-12)
- **D-P2-8:** ask_lite 在 AICaller 基类双路线各自实现(SdkAICaller 与 SubprocessAICaller 均实现),同一签名 `ask_lite(document_text, quoted_text, question) -> dict`(Phase 1 D-P1-6 已预定义,返回 dict 含 answer 文本)。调用形态:全新轻量无头调用,**只携带当前文档 + 划选原文**——不读全量 docs/、不走逐轮四步、不给工具能力(纯问答,无文件读写)、事件不进工作面板直播(不代表用户主动任务,§4.3 面板是"AI 工作过程"直播)。理由:§3.4"轻量无头调用,仅携带当前打开的文档与划选原文……保证秒级响应";D-05 双轨批注;双路线都要做是 D-01/§5.3"两路线界面契约完全一致"的硬要求。
- **D-P2-9:** 轻量调用的 prompt 模板同样注入 §3.8 语言红线,并要求"只解释,不改设计"(大白话是消歧不是新决定)。回答由后端落盘为 type=plain 条目(answer 即时写回),**不计入未决清单 / 未处理数**。理由:D-12"大白话问答落盘、不入清单";§3.8 注入每个阶段的 prompt;§3.3"大白话请求在产生时已即时回答,不进入轮次循环"。
- **D-P2-10:** 轻量调用与主调用共用"单飞"锁语义(进行中再发起被拒),但轻量调用通常秒级,请求本身是同步的(同 apps 不再走后台线程 + done 收流;若实现简单性要求,同步阻塞在 FastAPI worker 上实现即可——单机单人,秒级响应,无并发压力)。前端把即时答渲染为灰色斜体气泡并落盘。理由:§3.4"数秒内出解释,不打断阅读"——同步化是最简实现;session.py 单飞锁先例(D-P1 send/abort/divergence 同语义)。

### G2 处理流水线(FLOW-04 / §3.3 / §3.5 / §4.4 / §5.1)
- **D-P2-11:** 「处理本轮批注」的服务端 prompt 由新函数 `build_round_prompt(project, current_round)` 组装(加进 backend/prompts.py,与 build_phase12_prompt 同族四段结构:角色 + 语言红线 → 资料段 → 任务段):**资料段读全量 docs/**——当前轮文档全文 + 当前轮全部 annotations(逐条 id/quote/note)+ transcript/draft(§5.1"AI 启动时自磁盘读取 docs/ 下全部文档与批注"字面);**任务段**注入 §3.3 固定四步(逐条回应上轮全部实质批注 → 更新文档(本轮版次)并标注"已对齐" → 追问新的更深层细节问题进清单 → 文末公开当前未决清单)+ §6.3 五件套模板 + §6.4 文法模板(逐字遵守)。理由:§3.3 四步是原文;§6.3 每轮固定五件套(批注回应表 / 决策登记 / 维度表 / 未决清单 / 授权申请标记);§5.1 无状态。
- **D-P2-12:** 新一轮文档由 AI 的 Write 工具直接产出到 docs/discuss-round-(N+1).md(权限门规则 3:写 docs/ 内放行——现有实现已满足,零改动)。产出后**后端**做三件事:①解析新文档的批注回应表(§6.4 文法,批注id 对应上一轮 annotations 的 id),②按回应表回写上一轮 annotations.json 的 answer/status(status pending→answered),③拉新 derive_state——下一轮出现即上一轮自动冻结(冻结 = "下一轮文档存在" 推导出的呈现,无独立状态)。理由:§4.4 G2"本轮批注全部转为已回应、下一轮文档产生,本轮即自动冻结";§6.2 字段写回职责;§6.3 批注回应表与 N-1 轮 annotations 一一对应。
- **D-P2-13:** 回写后端动作**不依赖 AI 自觉**:回应表解析按"批注id"配对,凡出现在回应表中的 id 才回写;未在表中出现的批注保持 pending(下次「处理」重跑覆盖同轮,§7.3 自愈路径)。若 AI 写出格式不合规的新文档(末行非合规授权标记),is_complete_round 判半成品 → 当前轮仍为原轮 → 处理流程等同可重跑——现有 derive_state 已给足自愈语义,不新增判错分支。理由:D-13/§7.3"半成品判据……视为不存在……重跑产物覆盖原编号落盘"。
- **D-P2-14:** 触发入口在 session 层加 `process_round()`(与 trigger_divergence 同族:入口校验 phase3 + 单飞锁 + 后台线程 caller.run + 事件照常 SSE 直播——§4.1 布局图中「处理本轮批注」按钮就在工作面板区)。入口判定纯靠磁盘:derive_state == phase3 才受理(409 否则)。工作面板全程直播这次调用(§5.2"从用户点『处理本轮批注』起全程可见")。理由:§3.4"实质批注 → 批量处理";§5.2 原文;session.py 的 divergence 先例。
- **D-P2-15:** 侧栏"本轮批注未处理数" = 当前轮 annotations 中 type=comment 且 status=pending 的条数(plain 不计:它即时答且不入清单)。前端在侧栏批注流区常驻显示计数;「处理本轮批注」按钮的可用条件 = phase3 且未处理数 ≥ 0(DESIGN.md 不设"有批注才可处理"的门槛——第 3.3 收敛判据允许新批注不存在时回应完毕即申请授权,空批注轮也是合法处理轮)。理由:§4.2"每轮侧栏显式'本轮批注未处理数'";D-12;§3.3"新批注的存在不阻碍申请授权"。

### §6.4 机器文法解析器(FLOW-07)
- **D-P2-16:** 解析器为独立纯模块 `backend/grammar.py`(与 state.py 同级;state.py 已有的 PASS 前缀判定 / 授权标记判定迁移或复用,不重复实现两套)。覆盖六条:维度表(二级标题含「覆盖维度表」,列 = 维度/状态/说明,状态 ∈ {✓, ◐, ✗},全绿判定)、未决清单(二级标题含「未决问题清单」,列 = 编号/问题/状态,状态 ∈ {待决, 已决},清零判定)、授权申请标记(末非空行 strip 后恰为两串之一)、批注回应表(二级标题含「批注回应」,列 = 批注id/原文摘录/回应,供回写)、PASS 结论行(末非空行前缀匹配 + 结论行锚点取**最后一处** `> 核查结论:` 行)、裁决追加行(`> (待裁决|裁决):#数字:` 形态、仅统计结论行之后、同号配对)。**判定式自上而下首条命中**照 §6.4 原文。理由:§6.4 表格逐行;锚点取末一处、配对同号是 §6.4 原文对双结论行/多组问答边界的裁决。
- **D-P2-17:** 每条文法都要有正反例单元测试(构造合规轮次文档样本做解析与判定验证):合规表全绿/非全绿、清单清零/有待决、标记"是/否/脏变体(前后缀、空格)"、回应表 id 配对(命中/未命中/多余 id)、末行锚点取最后、同号配对与未配对、PASS 前缀带括注。ROADMAP 成功判据 6(含"结论行锚点取末一处、配对同号等边界")落在这里。理由:Phase 2 成功判据 6。
- **D-P2-18:** AI 生成模板逐字遵守文法:build_round_prompt 的任务段把 §6.4 的表格形态直接贴进 prompt(标记行/表头行逐字给出正例,并给出"切勿改列名/标记行"的硬指令);不解析成功也不修补 AI 的产物——靠重跑覆盖(§7.3)。理由:FLOW-07"AI 生成模板逐字遵守";§6.4"AI 生成轮次文档的模板必须逐字遵守"。
- **D-P2-19:** 解析不兼容历史文档:本工具只解析实施后新生成的轮次文档,本项目自身的 discuss-round-0~4(文法不完全合规,如 round-1 的清单状态列是"待批注")不要求能解析、不据此做按钮判定(不回溯改造)。理由:§6.4 适用范围原文(ROADMAP Out of Scope 已记)。

### 阶段 3 轮次视图(§4.1 / §4.2)
- **D-P2-20:** 轮次视图替换现有 rounds-placeholder:左文档区渲染当前轮 discuss-round-N.md(markdown,复用 renderMarkdown + stripUnsafeNodes);侧栏切换为批注流(annotations 条目列表:quote 摘录 + note + status 徽标 + answer 折叠展示,plain 条目灰斜体)+ 面板常驻「处理本轮批注」与现有「中止」。上一轮视图通过轮次切换器(dropdown / 左右切换)可浏览,**只读**:划词菜单不绑 + 侧栏计数不显示 + 视觉弱化(灰化)。理由:§4.2"进入轮次后切换为轮次文档 + 批注流";§3.5 冻结 = 只读归档;Phase 1 D-P1-15 占位即为此预留。
- **D-P2-21:** 冻结判据纯前端(权威在后端 derive_state):文档轮 < current_round → 该轮视图只读。新批注只能挂当前轮(API 层校验:POST 批注带 round 参数,非当前轮 → 409)。理由:成功判据 4"新批注只能挂在当前轮上,被批注文本永不变化"。

### 路由与契约(与 Phase 1 同族)
- **D-P2-22:** 新增路由(命名跟既有 api 风格):`GET /api/rounds`(轮次列表 + 当前轮号)、`GET /api/rounds/{n}`(轮次文档 + annotations 合并视图)、`POST /api/rounds/{n}/annotations`(建批注:quote/before/type=pending 条目落盘;非当前轮 409、非 phase3 409)、`POST /api/rounds/{n}/plain`(大白话:同步 ask_lite + 落盘 plain 条目,返回 answer)、`POST /api/rounds/process`(= 处理本轮批注:session.process_round,202)。「处理」完成(done 事件)后前端拉新 /api/session + /api/rounds 得到新当前轮与冻结视图——沿用 Phase 1 的"done 后拉新"门控刷新模式(REFRESH precedent:G-idi01-7 / applySessionGates)。理由:main.py 既有路由族;session.busy 409 先例;"文件即状态"拉新即可。
- **D-P2-23:** 批注内容(note/answer/quote)渲染一律走既有 renderMarkdown→stripUnsafeNodes 管线或 textContent,同样不做 raw HTML 注入;quote 高亮的 DOM 包装用 createElement/textContent,不用 innerHTML 拼接用户内容。理由:Phase 1 XSS 防护先例(T-idi03-02)平移到新数据入口——AI 回应与用户批注都是不可信输入。
- **D-P2-24:** 双路线(SDK/子进程)的 ask_lite 行为一致、run 行为照旧——本阶段不新增路线开关,config.ai_caller 沿用;测试用 FakeAICaller 平移(ask_lite 打桩)。理由:D-01/§5.3;test_session.py 的 FakeAICaller 先例。

### Claude's Discretion
- 弹菜单的视觉细节(位置偏移、样式)、选区跨段落时的截断策略(只取首段 / 选区必须单段落内)——DESIGN.md 无规定,实现取简单者(单要求:quote 必须落盘为合法字符串)
- 轮次切换器的具体控件形态(下拉 / 按钮组)
- annotations.py / grammar.py 的函数签名与内部结构(planner 自定,只要纯函数 + 零 FastAPI 依赖)
- 类型校验是否用 pydantic 模型(仅 API 边界;存盘 JSON 字面即 §6.2)
- batch 处理的 SSE 事件字段扩展(如 kind=round_started 等)——本阶段内自洽即可

</decisions>

<specifics>
## Specific Ideas

- 「处理本轮批注」点击起,处理过程(读文件、写 round-(N+1))要在工作面板全程直播,不是黑箱等结果(§5.2 原文)。
- 大白话即时答数秒内返回,"不打断阅读"(§3.4)——不在工作面板直播,answer 直接附在批注条目形态里显示(灰色斜体)。
- 侧栏批注流要能看到每个批注的完整链路:quote 摘录 → 用户批注 → AI 回应"附在旁边"(§4.2)。
- before 字段固定取"原文前 40 字"(§6.2 字面)。
- 批注回应表的 id 必须与上一轮 annotations 的 id 一一对应(§6.3)——后端回写据此配对;未出现的 id 保持 pending。
- 本项目自身的 docs/discuss-round-0~4 是文法不合规的历史样本(如 round-1 清单状态列是"待批注"而非"待决"),不能作为解析正例输入(§6.4 不回溯)。

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 设计权威(唯一)
- `DESIGN.md`(项目根,v1.13)— 唯一权威设计文档。本阶段重点节:§3.3(未决清单四步)、§3.4(双轨批注)、§3.5(轮次冻结)、§3.8(语言红线,轻量 prompt 也要注入)、§4.1/§4.2(布局/划词交互/未处理数/冻结)、§4.4(G2 语义)、§5.1(无状态调用)、§5.2(事件直播)、§5.4(权限门——写 docs/ 放行)、§6.1(目录结构含 annotations 命名)、§6.2(annotations 数据结构 + 字段写回职责,D-18)、§6.3(轮次文档五件套 + 批注回应表)、§6.4(机器可解析文法全部,含锚点取末一处/配对同号/判定式)、§7.3(半成品判据与覆盖自愈)、§7.4(推导表——current_round 消费)、§9(原生选区接口)
- `DESIGN.md` §11 决策表 — D-02(批注必做)、D-05(双轨)、D-07(冻结)、D-12(大白话落盘不入清单)、D-13(重跑覆盖)、D-18(批注结构)溯源

### 需求与规划
- `.planning/REQUIREMENTS.md` — FLOW-04/07、UI-01/02/04、DATA-01 六条需求原文(均标注 DESIGN.md 章节)
- `.planning/ROADMAP.md` — Phase 2 目标与 7 条成功判据(边界锚)
- `.planning/phases/idi-01-1-2/01-CONTEXT.md` — Phase 1 实现决策(D-P1-1~15),本阶段大量承接(ask_lite 签名、AICaller 双轨、done 后拉新刷新模式)

### 讨论上下文(理解意图参考)
- `docs/discuss-round-2.md` — D-05(双轨批注)/D-07(冻结制)定案轮,原始讨论上下文
- `docs/discuss-round-4.md` — D-18(annotations 数据结构)定案轮

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets(Phase 1 交付物,全部可平移复用)
- `backend/state.py`(164 行)— derive_state 已全量实现 §7.4 八行表:`STATE_PHASE3` / `current_round`(最大完整轮)正是本阶段所有按钮逻辑的判定源;`is_complete_round` / `list_complete_rounds` / `AUTH_MARKER_YES/NO` / `PASS_PREFIX` 已就位——授权标记与 PASS 行的 strip-末行判定先例,新 grammar.py 直接复用这些常量与语义,**不重复造两套**
- `backend/transcript.py`(121 行)— `[user]`/`[ai]` 文法的 parse/append 先例:annotations.py 照它的"纯 pathlib + 零依赖 + 不存在返回空形态 + 父目录自举"模式写
- `backend/g1.py`(52 行)— "后端动作写受控产物"(draft→round-1 + 追加标记行)先例:G2 的 annotations 回写在结构上同构(后端改写文件,AI 不碰)
- `backend/session.py`(484 行)— 单飞锁(_inflight Event)、后台线程 _worker + SSE 直播、入口校验(available 判定防绕过)、_reset_for_tests / _set_caller_for_tests 测试 seam——process_round() 直接照 trigger_divergence(433-484 行)的模子写
- `backend/ai_caller.py`(641 行)— AICaller.ask_lite 签名已预定义(222-227 行,NotImplementedError 占位);make_permission_decision 规则 3(写 docs/ 内放行)已生效——AI 写 discuss-round-(N+1).md 零改动放行;set_request_permission 依赖注入模式照用;双路线 setting_sources=[] 硬约束已就位
- `backend/prompts.py`(157 行)— 四段结构(角色+语言红线/资料/任务)+ _LANGUAGE_RULES 常量:build_round_prompt 照 build_phase12_prompt(104-157 行)的模子写,资料段扩到轮次文档 + annotations 全量
- `backend/main.py`(316 行)/ `backend/events.py`(48 行)— 路由族(202 受理/409 忙、JSONResponse、SSE /api/events、broker 单例):新路由照抄风格;done 后前端拉新已是惯例
- `frontend/app.js`(553 行)— renderMarkdown + stripUnsafeNodes(XSS 管线,新数据入口必须走)、applySessionGates 的 phase1/phase12 → draft-view / phase3+ → rounds-placeholder 分支(236-245 行)是轮次视图替换的挂点;done 后 GET /api/session 拉新(G-idi01-7 修复先例);STATE_LABELS 已含全部状态中文名
- `frontend/index.html` — rounds-placeholder(53-57 行)即被替换占位;vendor/marked.min.js 已 vendored
- `backend/tests/`(10 文件)— FakeAICaller(script 事件 + run_calls 记录)、fresh_session 夹具(_reset_for_tests)、wait_idle 收流辅助;68 用例 + 2 个 @slow E2E(IDI_E2E 门控)——新功能按同族加文件

### Established Patterns
- 纯函数模块(零 FastAPI / 零 AI 依赖)承载文法与磁盘判定:state / transcript / g1 三模块已确立——annotations.py 与 grammar.py 照此
- 入口校验"纯靠磁盘推导"防绕过:divergence_available / g1_available 先例——批注与处理入口照此(derive_state == phase3 且轮次为当前轮)
- 后台线程 + SSE 广播 + done 收流 + 前端拉新:send_message / trigger_divergence 已两次复制该模式,G2 是第三次
- SSE 事件 kind 枚举前端可见且双路线一致:ask_lite 不产直播事件(它是用户查询,非 AI 任务过程)

### Integration Points
- `session._session_snapshot()` — 扩展轮次字段(rounds 列表 / 当前轮 annotations 计数)供 /api/session 前端拉新
- `trigger_divergence` 模子 → `process_round()`:差异 = prompt 组装源(build_round_prompt)+ done 后回写动作(解析回应表 → annotations 回写 answer/status)
- `app.js` applySessionGates 的 phase3+ 分支 → 挂轮次视图与侧栏批注流(替换占位)
- config.json `ai_caller` 开关不动;ask_lite 双路线各自实现但同一契约

</code_context>

<deferred>
## Deferred Ideas

- G3:四处机械校验、确认词「确认授权」、AUTHORIZATION.md 后端写入、DESIGN.md.tmp 原子改名、拒绝转普通批注 → Phase 3(FLOW-05 / DATA-02)
- 自检档位(宽松/严格)、核查/修复双角色循环、纯 P2 残余裁决的**流程侧**(报告按钮、暂停态、继续修复)→ Phase 3(DATA-04;六条文法的**解析判定**本阶段已实现,Phase 3 只做消费)
- 「继续撰写」「继续自检」「继续修复」按钮 → Phase 3(§7.3②)
- 使命完成提示与只读归档态(划词/处理/授权按钮全部不可用)→ Phase 3(DATA-03)
- 阶段 4/5 推导态的界面呈现 → Phase 3(D-P1-11 已全量实现推导;本阶段轮次视图只覆盖 phase3 分支)
- AI 生成中途插话(v2 再议,D-20)与历史文档回溯改造(§6.4 不回溯)为 DESIGN.md 明确非目标,永不做

</deferred>

---

*Phase: idi-02-g2*
*Context gathered: 2026-09-09*

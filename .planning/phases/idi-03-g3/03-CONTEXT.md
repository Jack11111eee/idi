# Phase 3: 授权、自检与终点——G3、档位、使命完成归档 - Context

**Gathered:** 2026-09-10
**Status:** Ready for planning
**Mode:** --auto(discuss-phase 单遍完成;决策源 = DESIGN.md v1.13,冲突处一律以 DESIGN.md 为准)

<domain>
## Phase Boundary

交付 DESIGN.md 范围内的"三道门后半程与终点":收敛达标后用户走完 **G3 授权**(四处机械校验点亮按钮、确认词「确认授权」、后端写 AUTHORIZATION.md、拒绝转普通批注),授权后走完**阶段 4 撰写**(AI 写 DESIGN.md.tmp → 后端原子改名落盘),接着**阶段 5 自检全链**(宽松/严格档位选择与报告头部落盘、核查者/修复者两角色自动循环、纯 P2 轮 D-22 残余裁决、待裁决/裁决行后端截存追加与配对),直至最新 check 报告末行 `> 核查结论:PASS` 前缀命中 → **「使命完成」提示 + 只读归档态**(D-21)。全程任何崩溃中断,重开界面按磁盘现状出现「继续撰写」/「继续自检」/「继续修复」按钮,点一下重跑覆盖即自愈。

**In(本阶段做):** G3 四处校验组合判定、确认词模态交互、AUTHORIZATION.md 后端写入、拒绝转一条普通批注(FLOW-05);撰写流水线 + DESIGN.md.tmp 原子改名 + 「继续撰写」(DATA-02 撰写侧);宽松/严格档位选择 UI + 报告头部记录 + 重开恢复(DATA-04 交互侧);严格档两角色自动循环引擎、抛问 `> 待裁决:` 事件截存、裁决落盘与「继续修复」、D-22 纯 P2 残余裁决、宽松档修复者追加 PASS(DATA-04 流程侧);报告判定式状态机(暂停态/裁决待续跑态,消费 Phase 2 已交付的 grammar 判定);"继续自检"意外中断恢复;mission_complete 提示弹窗 + 只读归档态呈现(DATA-03);新 AI prompt 四族(授权拒绝批注引导、撰写、核查、修复);以上全部的前端路由挂载(阶段 4/5/完成态视图)。

**Out(本阶段不做):** 新增任何轮次/批注能力(Phase 2 已全量交付——完成态只把它关掉);阶段 1-2 与发散模式的任何改动;§6.4 文法的解析本体(grammar.py 六条已交付,本阶段只作消费方);权限门矩阵改动(DESIGN.md/AUTHORIZATION.md 拒绝、tmp 放行均已实现);本项目自身 docs/(14 份 check 报告)的回溯改造——工具运行时操作的是另一个项目目录(D-P1-4 仓库/目标分离铁律);AI 生成中途插话与直播回放(D-20/D-13 永久非目标)。

**本 phase = milestone 收尾:** Phase 3 是 v1.13 milestone 的最后一个 phase。本 phase 完成(verification 通过)后即走 `/gsd-complete-milestone` 归档整个 milestone,不再有 Phase 4。任何超出 DESIGN.md v1.13 范围的想法一律记 Deferred(后续 milestone),不得塞进本 phase。

</domain>

<decisions>
## Implementation Decisions

(auto 模式:全部承袭 DESIGN.md v1.13 既有章节/决策 D-04/D-09/D-13/D-14/D-17/D-19/D-21/D-22 及 Phase 1/2 实施决策 D-P1-*/D-P2-*,无新造决策;每条标注出处)

### G3 四处校验与按钮(FLOW-05 / §4.4 / §8.1 / D-17)

- **D-P3-1:** G3「授权撰写总设计文档」按钮的点亮判定 = 新组合函数 `g3_available(project)`,四条机械校验全部命中才 True:①当前轮 annotations 无 status=pending 的 comment 条目(复用 annotations.select_pending);②当前轮文档未决清单清零(grammar.is_pending_list_clear);③维度表全绿(grammar.is_dimension_table_green);④授权申请标记为「是」(grammar.parse_auth_marker == "yes")。前两条已各有现成函数,组合判定放 backend(独立小函数或并入 g1.py 同族的门文件),session/_session_snapshot 与前端按同一来源取(phase3 时按钮显隐挂 snapshot 字段,照 g1_available/divergence_available 先例)。四条必须在同一份当前轮文档快照上判定(读一次文档文本复用),不跨轮。理由:§4.4 权威定义"四处机械校验全部通过";ROADMAP 判据 1 字面;D-17「机械校验而非采信 AI 自评」。
- **D-P3-2:** 「当前轮」在 G3 语境 = derive_state 的 current_round(最大完整轮;半成品轮视为不存在,§7.3)。四处校验只对当前轮做;G3 按钮也只在 derive_state == phase3 时呈现。理由:§7.4 行 3"当前轮 = 最大完整 N"一切按钮逻辑的判定源是 derive_state 的既有约定。
- **D-P3-3:** 确认词交互 = 前端模态 + 文本输入框:点「授权撰写总设计文档」→ 弹确认框 → 用户输入恰为「确认授权」(strip 后全等)才放行 POST;任何其他输入/关闭/取消 = 拒绝路径,不 POST 授权,不写任何落盘物。确认词校验在前端模态内完成(输入框未通过不给放行按钮)——**后端不重复解析自然语言,后端防线是"仅确认词通过瞬间写 AUTHORIZATION.md"的动作本身**。模态文案点明"默认拒绝;拒绝后本轮仍可继续批注讨论"。理由:§4.4"点击 → 确认框 → 输入确认词『确认授权』二次确认,防误触;默认拒绝";§8.1 同;后端不二次解词是简单优先——唯一凭证是 AUTHORIZATION.md,不存在绕过确认词的 API 路径。
- **D-P3-4:** 授权通过(POST 受理)= 后端动作两件套:①在项目根写 AUTHORIZATION.md(内容 = 后端生成的明文:授权时间 ISO-8601 + 操作者确认词标记行,格式照 §7.4 授权痕迹"授权时间 + 操作者确认词标记"),②返回新 derive_state(state=phase4)。幂等防护照 g1.py 形态:AUTHORIZATION.md 已存在 → FileExistsError(路由层 409,G3 只走一次——重开已授权项目按 §7.4 行 4 显示「继续撰写」而非重新授权)。写入前四处校验后端**再查一遍**(防绕过:按钮亮否是前端呈现,POST /api/authorize 入口处后端独立重判四条 + phase3,任一不过 → 409)。理由:§7.4 行 3/行 4 + 授权痕迹段"后端(非 AI)在项目根写入 AUTHORIZATION.md……存在 = 用户确已授权";g1.py FileExistsError 幂等先例;divergence_available/g1_available/round_process_available 的"入口校验纯靠磁盘防绕过"三先例。
- **D-P3-5:** 拒绝路径 = 前端把用户在确认框里写明的原因(或"授权被拒,继续完善")作为一条普通批注提交——走既有 annotations 通道(type=comment,pending),quote 可取当前轮文档标题或维度表行、note 写明还差什么/用户要求(实现细节归 planner),然后入口留在 phase3 继续下一轮「处理本轮批注」。**不在 CONEXT 层发明独立拒绝文件。**理由:§4.4"拒绝 = 一条普通批注(写明还差什么),继续下一轮";§8.1"拒绝形式:普通批注,写明还差什么,继续追加轮"——"普通批注"原文即复用批注通道。

### 阶段 4 撰写流水线与 tmp 原子落盘(FLOW-05 / DATA-02 / §7.3① / §7.4 行 4)

- **D-P3-6:** 「撰写总设计文档」入口(阶段 4 视图常驻按钮):session 层新函数 `start_writing()`,照 process_round 模子三查(未进项目 400 / 在飞 409 / 入口判定不过 409)。入口判定 `writing_available(project)` = derive_state == phase4(有 AUTHORIZATION.md、无 DESIGN.md)。后台线程跑 caller.run + oAuth 事件 SSE 直播(“授权撰写”到 AI 需要专人传令——见 D-P3-7)。理由:trigger_divergence/process_round 两次同模复制是第三次;§7.3①"撰写调用中断 → §7.4 对应行提供「继续撰写」按钮,重跑重新写 DESIGN.md.tmp、由后端原子落盘"。
- **D-P3-7:** 撰写调用的 prompt = 新函数 `build_writing_prompt(project)`(backend/prompts.py,与 build_round_prompt 同族四段:角色(总设计文档撰写引擎)+ 语言红线 → 资料段(全量 docs/:全部完整轮文档 + 全部 annotations 逐条 + transcript/draft/brainstorm——授权后的产物是整段讨论的收敛,§5.1 无状态全量读)→ 任务段:产出一份无歧义的总设计文档——覆盖维度表七个维度全部内容、吸收决策登记与已对齐结论、不含未决问题;落盘指令:**用 Write 工具写 `DESIGN.md.tmp`(项目根,整体覆盖式写入)后即结束**,绝不直接写 DESIGN.md 或 AUTHORIZATION.md(权限门会拒绝,提示语写明目的与格式)。理由:§5.4 tmp 放行行"它是 DESIGN.md 唯一合法的落盘路径";§8.1 授权语义;build_round_prompt 先例(prompt 里目标文件名显式给出)。
- **D-P3-8:** tmp 原子改名落盘 = done 后端动作:worker 的 else 分支(照 process_round 回写分支的位置先例)拉 derive_state——有 AUTHORIZATION.md 且无 DESIGN.md 而 DESIGN.md.tmp 存在 → `(tmp_path).replace(design_path)`(os.rename/Path.replace 同 inode 原子操作,覆盖语义)。改名前不校验 tmp 内容完整性(半份 tmp 是崩溃残留重跑场景,DB 无"半份 DESIGN.md"状态——见 D-P3-9);改名成功 → publish 完成 say/done。若 done 后 tmp 不存在(AI 没写)→ error 事件("撰写未产出 tmp,可重跑")不改名,状态留在 phase4 可重跑。理由:§7.4 行 4"半份 DESIGN.md 不可能存在:撰写调用以 DESIGN.md.tmp 写入、完成后原子改名为 DESIGN.md";D-13 重跑覆盖在阶段 4 的推广。
- **D-P3-9:** 半份 tmp 残留的崩溃自愈:AI 写 tmp 中途崩溃/被杀 → tmp 留在盘上但 DESIGN.md 未出现 → derive_state 照 §7.4 行 4 = phase4 → 界面显示「继续撰写」(同一入口的文案变体,判定式有 tmp 存在即显示"继续")→ 点击重跑,**重跑 prompt 的资料段照读磁盘(tmp 的半份内容不入资料、不参考——它是被覆盖物,见 D-P3-7 资料段不含 tmp)**,AI 重新整体写 tmp 覆盖旧残件,再走改名。无需重新确认词(AUTHORIZATION.md 已存在,凭证不受影响)。理由:§7.3① 原文"中断残留的 tmp 文件随重跑覆盖,自愈成立;无需重新确认词"。
- **D-P3-10:** 「继续撰写」/「撰写总设计文档」按钮判定式:phase4 态常驻(文案:无 tmp = "撰写总设计文档";有 tmp 但无 DESIGN.md = "继续撰写(检测到上次中断的半成品,重写覆盖)")。判定纯磁盘:derive_state == phase4 + (project/DESIGN.md.tmp).is_file()。理由:DATA-02/§7.3①;三个"继续"按钮族的共通判定模式——一切状态从磁盘推导。

### 档位选择(DATA-04 / §8.2 / §7.4 行 5)

- **D-P3-11:** 档位选择 = 阶段 5 待选档(phase5_awaiting_tier)界面弹模态:两个选项「宽松」「严格」+ 各自一句话说明(宽松 = 一次核查+修复+追加 PASS 即止;严格 = 循环核查至零问题轮 PASS,纯 P2 轮交用户裁决)。选择 POST /api/checks/tier 后在后端记录:**落盘为一份未编号的档位签名文件,不落 docs/**——定 `docs/DESIGN-check-tier.md` 与 §6.1 目录树相符(头部一行 `> 自检档位:严格|宽松`,内容给状态机读写)。**不**采用"选档后立刻起 check-1"方案(tier 留文件等首次核查按它产出 check-N 头部,见 D-P3-14)。模态的弹出判定 = derive_state == phase5_awaiting_tier 且无废档文件(见 D-P3-25)弹;选档幂等:重开项目在 phase5_awaiting_tier(尚无 check 报告)→ 重新弹选(DESIGN.md 字面"重新弹选,幂等");已有报告 → 档位照最新报告头部,不弹。理由:§8.2"选择结果记录于每份核查报告头部(落盘),重开据此恢复档位(尚未产生首份报告时重开 → 重新弹选,幂等)";档位必须落盘是"文件即状态"的硬要求——不落盘的选档违反 D-19。
- **D-P3-12:** 档位签名文件的内容 = 单行 `> 自检档位:严格`(或宽松)。check 报告产出时后端把该值注入 prompt 文法模板(D-P3-15 报告头部行),报告头部行格式:`> 自检档位:严格`。derive_state 路线 B(见 D-P3-23)与"重开恢复档位"都读**最新 check 报告头部**的该行——tier 文件只在"选档已落、报告未出"的窗口期作为中间态凭证。理由:§8.2 字面"记录于每份核查报告头部……重开据此恢复档位"。

### 阶段 5 两角色循环引擎(DATA-04 / §8.2 全节)

- **D-P3-13:** 核查执行者调用 = `start_check()`(session 层,照 start_writing 模子):入口判定 `check_available(project)` = phase5_awaiting_tier 或 phase5_checking(无在飞)。prompt = `build_check_prompt(project, check_n)`:角色段——「干净的眼睛:独立核查引擎,无讨论立场,只依据磁盘文件」+ 语言红线;资料段——DESIGN.md 全文 + 全部轮次文档 + 全部 annotations + 已有全部 DESIGN-check 报告(严格档多轮的趋势/沿用 §8.2"以磁盘为唯一输入"字面)→ 任务段——按五维(内部一致性/历史批注符合度/决策无歧义/可实施性/结论覆盖)核查 DESIGN.md,问题按 **P0/P1/P2 分级列示**(表头:编号/级别/位置/问题/建议修法——**表列名文法逐字贴入 prompt,照 D-P2-18 先例**),产出报告全文用 Write 写 `docs/DESIGN-check-{n}.md`(n = 现有最大 check 编号 + 1,后端算好注入 prompt,防 AI 编错号);报告**末行**写结论行(`> 核查结论:FIX(P1×2 …)` 或零问题时 `> 核查结论:PASS`,供 strengthen §7.4 全局判定)。**核查执行者绝不修改 DESIGN.md——prompt 明禁**(它只写自家报告)。理由:§8.2 多方角色①"全新无头调用,以磁盘文件为唯一输入,产出该轮核查报告,并在零问题时于报告末行写 PASS;它不修改 DESIGN.md";§6.1 "DESIGN-check-N.md 自检报告(宽松 1 份;严格每轮 1 份)";§6.4 PASS 结论行文法(报告最后一个非空行前缀)。
- **D-P3-14:** 修复者调用 = `start_repair()`(同模子):入口判定 = 最新 check 报告末行非 PASS 前缀(有可修的问题)且处于 phase5_checking/裁决待续跑。prompt = `build_repair_prompt(project, check_n)`:资料段 = DESIGN.md 全文 + 最新一份(第 n 轮)核查报告全文(问题清单 + 用户裁决,见 D-P3-19)+ 其他既有报告 + 轮次文档/批注;任务段——报告问题按裁决逐条修复,修订**用 Write 工具整体写 `DESIGN.md.tmp` 后结束**(修复同样走 tmp 单次整体落盘纪律);**报告问题属用户职权**(如范围与非目标类)时**不得替用户决定**——在输出里发 `> 待裁决:` 前缀事件停下(见 D-P3-18)。宽松档特例:唯一一轮核查+修复后,修复者**在报告末追加 PASS 结论行**(用 Write 整体重写报告含原内容 + 末行 PASS,或 Edit 追加——实现归 planner,落盘物必须仍是末行前缀合规)。理由:§8.2②"修复者——另一个全新无头调用(同样以磁盘为唯一输入,含刚落盘的核查报告),按报告执行修复、修订 DESIGN.md";§7.3②"修复者对 DESIGN.md 的修订同样走'单次整体落盘'纪律——tmp 一次写全、后端改名";§8.2"宽松档即由修复者追加 PASS 收尾"。
- **D-P3-15:** 报告头部固定行(文法,逐字贴入 prompt):首头部行 `> 自检档位:<严格|宽松>`(照 tier 签名)。**本工具对报告其余正文只消费三样:头部档位行、问题分级表(可选——D-22 残余裁决需要从中提取逐条 P2 给 UI;表头文法待 planner 逐字定死)、末行结论行前缀判定 + 裁决行扫描。**正文风格归 AI(§3.8 语言红线约束)。理由:§8.2 档位记录于头部;§6.4「报告最后一个非空行以 `> 核查结论:PASS` 开头(前缀匹配)」;D-22 残余裁决需要"问题逐条"可数——中庸做法:问题表按固定表头落,便于后端把纯 P2 轮的剩余问题逐条抛给用户。
- **D-P3-16:** 严格档自动循环 = 后端的循环驱动器(不新增独立状态机状态——见 D-P3-23 磁盘推导原则):核查调用 done 后:①拉 derive_state + 读最新报告——末行 PASS 前缀 → 结束(mission_complete 弹窗链);②报告末行非 PASS:后端判定**该轮是否纯 P2**(从报告问题表解析级别列——见 D-P3-15 表文法):纯 P2 → 不自动修复,转 D-22 残余裁决流程(D-P3-17);含 P0/P1 → 自动启动修复调用;③修复调用 done 且全程无 `> 待裁决:` 标记 → 判定修复者是否已写 tmp(照 D-P3-8 改名 DESIGN.md)→ 自动开启下一轮核查(check_n+1 回到 ①)。**两跳均后端自动,无需用户点击;每一步结束都拉磁盘判定下一步。**循环驱动实现形态归 planner(session 层一个驱动函数串两跳,或每 done 事件的回调链——**不得**引入常驻后台 scheduler;推荐 done-回调和 done-回调的直排形态)。理由:§8.2"循环的两跳均为后端自动:核查报告落盘且末行非 PASS 时,后端自动启动修复调用;修复正常完成后,后端自动开启下一轮核查(严格档),无需用户点击"。
- **D-P3-17:** D-22 残余裁决(纯 P2 轮)判定 = 核查报告问题分级表全部问题级别 = P2(零 P0/P1)。触发后**不启动修复调用**;界面进入残余裁决呈现:每个残余问题一条裁决卡(问题位置 + 描述 + 建议修法 + 两个按钮「修」「接受现状」)。逐条用户点击 → 逐条落盘(见 D-P3-19 同一裁决通道)——**用户裁决本身落盘沿用 D-P3-19 的 `> 裁决:#K:` 追加到最新报告;「接受现状」也是一条裁决,note 文案如"接受现状"**。全部残余问题处理完 = "全部处理完即视为收敛收口"→ 后端**立即**在最新报告末追加 PASS 结论行(后端动作,这里不是 AI——收口瞬间在全部裁决落盘后,机器可判定"残余清零":配对数 == 问题数)。收口后进 mission_complete。**P2 分级本身不进 derive_state 判定**——它是循环驱动的内部判定,从报告文法解析,落盘签名仍是"裁决行配对 + 追加 PASS"。理由:§8.2 D-22 修订补充"当某轮核查结果为纯 P2(无 P0/P1)时,不再自动进入下一轮循环,剩余问题逐条交用户裁决「修」或「接受现状」,全部处理完即视为收敛收口,裁决记录补录为正式决策";「逐条在界面抛给用户裁决」ROADMAP 判据 4 字面;后端追加 PASS 是"收口"语义的实现方式——唯一备选"再起一轮修复调 check 落实'修'"违反"不再自动进入下一轮循环"字面,弃。
- **D-P3-18:** 抛问识别契约:修复者抛问时,在**调用输出**发一条以 `> 待裁决:` 前缀开头的 say 事件消息(协议形态:AI 在其最终回复文本里包含一行以 `> 待裁决:#K:<问题>` 开头的消息——prompt 写明该协议)。后端扫描本次调用的 say 事件流/最终文本:发现该前缀 → 截存(提取 #K 与问题文本)→ **立即暂停**:①把问题本身追加落盘到当轮核查报告末尾(`> 待裁决:#K:…`,后端写,幂等=内容级——同一问题已存在同内容待裁决行则不重复追加,§6.4);②不启动后续跳;③不发"继续修复"按钮。**自动推进仅在「调用正常结束且全程无该标记」时触发;识别不到该标记不得当作正常完成**——本条设计为 D-13 自愈兜底:识别失败时,循环停在当前跳,该轮报告无裁决行签名 → 判定式照旧行,不误推进。理由:§8.2 抛问识别契约段字面。
- **D-P3-19:** 用户裁决落盘:用户在暂停态界面回答(输入框)→ POST /api/checks/verdict {number, decision, note} → 后端把裁决追加落盘到同一报告末尾(`> 裁决:#K:<用户裁决文本>`),同号即与原待裁决行配对。幂等照 §6.4 内容级:**后端仅当同内容裁决行不存在时追加**(同号不同内容 = 更新不了——判定式只看同号配对,多写一行不影响判定,但 prompt/UI 引导一次一答;实现择拒绝重复 POST 同号)。落盘后状态自动变为裁决待续跑态(判定式②,§6.4)→ 界面只呈现「继续修复」。「继续修复」重跑修复调用:prompt 资料段**含问题与裁决的报告**(以磁盘为输入,不引入其他通道——裁决行就在最新报告里,天然满足)。理由:§8.2"用户在界面回答后,后端将其裁决追加落盘到同一报告末尾,「继续修复」按钮重跑修复调用(续跑以含问题与裁决的报告为磁盘输入,不引入其他通道)"。

### 判定式与三个继续按钮(DATA-02 / §6.4 判定式)

- **D-P3-20:** 自检侧两个暂停态与「继续自检」/「继续修复」按钮判定式,严格照 §6.4 判定式(自上而下,首条命中即取),消费 grammar.py 已交付函数:
  - **判定式①(暂停态):** 最新报告 unpaired_verdicts 非空 → 暂停态:隐藏「继续自检」、呈现问题与输入框(**裁决落盘前不呈现「继续修复」**——防误点重跑,check-10 已记)。前端读 snapshot 的 `selfcheck_mode: "paused"` 字段(见 D-P3-23 状态机从推导层取)。
  - **判定式②(裁决待续跑态):** 存在配对问答行 + 无未配对待裁决行 + 无更新编号报告 + 末行非 PASS 前缀 → 隐藏「继续自检」、**只呈现「继续修复」**。退出 = 更新编号报告出现。
  - **「继续自检」按钮:** 仅担任**意外中断恢复**——报告未完整(挂死的核查/修复调用,盘上无当轮报告或半份)时点击重跑当前核查轮,覆盖半份。判定 = phase5_checking 态(最新报告存在但是半成品/调用挂死)且非①②两态。「继续自检」**不**用于正常流程推进(正常推进是自动两跳);也不在暂停态/裁决待续跑态呈现(两态各自隐藏)。宽松档「继续自检」同样适用(核查 or 修复中挂了都能重跑当前轮)。理由:§8.2 两态呈现规格原文 + §6.4 判定式①②(check-14 修订后的互斥版, grammar 已按其锁定);§7.3②「继续自检」仅担任意外中断恢复。
- **D-P3-21:** 半份 check 报告自愈 = 重跑覆盖("半份"判据照 state.py max_check_number 现状:**只要文件在就计入最大编号,不校验内容完整性**——半份重跑覆盖即可,derive_state 注释原文"半成品报告同样落此行,重跑覆盖")。「继续自检」重跑的目标轮 = max_check_number(若当轮报告半份)或被中断前的下一轮;实现择:*重跑 = 重新起核查调用,check_n 取 max+1 若最新报告完整、取 max 若判定为半份*(判定细节归 planner,原则:重跑同轮覆盖、不跳号、不重算确认词)。理由:§7.3②"半份 DESIGN-check-N.md 重跑覆盖";state.py 既有注释。
- **D-P3-22:** 修复者写 tmp 中断(修复半途被杀)自愈:tmp 残留、DESIGN.md 未变(旧版完整有效——权限门只放行 tmp 写入,DESIGN.md 不可能半份)→ derive_state 仍 phase5_checking(DESIGN.md 存在 + 最新报告非 PASS)→ 重开按判定式(若报告无裁决行签名,靠「继续自检」重跑核查轮;若裁决已配对,判定式②给「继续修复」)恢复。**不新增第三个"继续"按钮**——「继续修复」重跑对 tmp 残留同样覆盖。理由:§7.3②"超时或失败时已落盘的 DESIGN.md 保持旧版完整有效,未完成的修复项会在下一轮核查报告中重现,循环自身兜底"。

### mission_complete 与只读归档(DATA-03 / §7.4 / D-21)

- **D-P3-23:** 自检状态机**不新增 derive_state 状态值**:state.py 七常量已全量覆盖(phase5_awaiting_tier / phase5_checking / mission_complete 就绪)。derive_state 需扩展的只有一处:**路线 B 的 tier 与两态细节**——session._session_snapshot 在 state=phase5_checking 时读最新报告文本,运行 grammar 判定式(unpaired/coupled/is_pass_conclusion + tier 头部行),组装自检子状态字段:`selfcheck: {tier, mode: "running"|"paused"|"resumed"|"done"(=mission_complete 用 state 表达)}` + 暂停态问题列表(裁决卡数据)。**推导函数本身只认磁盘,不缓存**——UI 呈现的全部判据(say按钮显隐、报告可读、输入框)都从 /api/session snapshot 来。理由:§7.4 "工具不维护独立的流程状态,一切由磁盘现状推导";Phase 1 D-P1-11 推导脊柱先例(状态值已全部预定义,本字段扩展仅 snapshot 层组装)。
- **D-P3-24:** 「使命完成」提示:前端感知 state == mission_complete(design PASS 后拉新 /api/session,或进入项目时)弹一次性欢呼模态("使命完成——总设计文档已通过自检,项目进入只读归档态"),关闭后进入只读归档视图。弹窗判定 = 「本次会话首次见到 mission_complete」(会话内存标记,不落盘——重开项目重现弹一次,符合"重开即弹"语义且无状态);只读归档本身是持久态。理由:§8.2"PASS 结论行出现(判定规则见 §7.4)→ 界面弹「使命完成」提示,流程正式结束,此后为只读归档态";DATA-03/ROADMAP 判据 5 字面"界面弹出「使命完成」"。
- **D-P3-25:** 只读归档态呈现 = mission_complete 分支的完整视图:左侧文档区可浏览 DESIGN.md(默认渲染)+ 全部轮次(切换器)+ 全部 check 报告(新报告切换/折叠列表,归 planner 定形态);划词菜单不绑(round-doc mouseup 的 `currentState !== 'phase3'` 防线已天然生效)、「处理本轮批注」禁用/隐藏(process_round 入口判定 409 双防线)、「授权撰写总设计文档」按钮隐藏(非 phase3 无处安放)、发散/发消息等输入面全部隐藏或禁用——**本质是现有 phase4+ 占位文案分支替换为真视图**。后端不新增"归档标志"——mission_complete 本身即推导态,一切关闭动作都是"入口判定不满足"(服务端 409 是防线)。理由:§7.4 完成态段"可浏览全部轮次、批注、DESIGN.md 与核查报告;划词批注、「处理本轮批注」、授权按钮均不可用;不再追加轮次"——可用性即推导态的呈现,零新增状态。
- **D-P3-26:** session gates 双向补全:phase3 下新「授权」按钮、G3 拒绝转批注交互;phase5_awaiting_tier 弹档位;phase5_checking 呈报告 + 继续/裁决控件;mission_complete 归档视图。**确认与修复/核查入口均带单飞锁**(照 process_round 五先例),互相 409——多窗口同时点只有一个被受理。裁决卡逐条 POST /api/checks/verdict 不起 AI 调用但同样单飞校验(避免两个裁决同时 pending 写报告竞态——追加动作短暂同步,单飞即可)。理由:session.py _inflight 单飞锁五先例;§7.4 文件即状态不新增锁机制。

### 路由契约(与 Phase 1/2 同族)

- **D-P3-27:** 新增路由(照 main.py 风格):`GET /api/design`(DESIGN.md 内容,前端阶段 5/完成态渲染)+ `GET /api/checks`(check 报告列表 + 最新报告全文 + selfcheck 子状态) + `POST /api/authorize`(G3:四查+确认词已在前端完成,落 AUTHORIZATION.md,409 幂等)+ `POST /api/writing`(起撰写,202)+ `POST /api/checks/tier`(宽松/严格落盘)+ `POST /api/checks/start`(「继续自检」/首轮核查入口,202)+ `POST /api/checks/repair`(「继续修复」/自动修复入口,202)+ `POST /api/checks/verdict`(用户裁决追加落盘)。照既有惯例:202 受理/409 忙或不可/400 未进项目;done 后前端拉 /api/session+自我查看链(不新增专用收尾事件,kind 面向 SSE 照旧)。幂等防护:endpoint 判 derive_state 过滤(如 POST /api/authorize 要求 phase3)已在 D-P3-4/D-P3-6/D-P3-13 各入口。理由:main.py 路由族先例;done 后拉新 G-idi01-7 惯例。
- **D-P3-28:** 前端阶段 4/5/完成态视图挂点 = applySessionGates 的 else 分支(现占位文案"当前状态:xxx(轮次阶段之后的视图在本工具后续版本呈现)"被真视图替换):phase4 → 撰写按钮 + AI 面板照旧;phase5_awaiting_tier → 档位模态;phase5_checking → 报告视图 + 继续/裁决控件;mission_complete → 归档视图。**子视图切换沿用现有 DOM 结构**(rounds-placeholder 容器复用或新增 doc-subview 均可,归 planner,原则:不重排阶段 1-3 已定版式,不新增路由)。XSS 不变:报告/DESIGN.md/AI 回复渲染一律走 renderMarkdown→stripUnsafeNodes 或 textContent(T-idi03-02)——阶段 5 新数据全部是不可信 AI/用户输入。理由:app.js applySessionGates 236-245 行现挂点;D-P1-14 单页原则;D-P2-23 同管线先例。
- **D-P3-29:** prompt 四族与 §3.8/语言红线 + 报告文法模板逐字注入:build_writing_prompt / build_check_prompt / build_repair_prompt 全部照 build_round_prompt 四段结构,报告文法(头部档位行、问题分级表头、结论行、裁决追加形态)在 prompt 里逐字给出正例 + 切勿改列名硬指令(D-P2-18 先例)。**对 AI 产物不解析成功也不修补——靠重跑覆盖**(§7.3)。新 prompt 若要求特定表格才可解析的处,必须配构造正反例测试(照 D-P2-17 先例——新问题分级表是新文法,配若干正反例)。理由:FLOW-07 延续;§6.4"AI 生成轮次文档的模板必须逐字遵守";D-13。
- **D-P3-30:** 测试延续既有模式:纯函数层用例(四查、判定式组合、报告头部/问题表解析、裁决幂等) + session 单飞/入口判定用例(FakeAICaller 打桩撰写/核查/修复 run,验证 done 后端动作链:改名、自动下一跳、截存暂停) + E2E 真调门控(照 IDI_E2E 现有形态,造真实 tmp 项目走 part of G3→PASS 全链)。**本阶段不引入新的测试基建**;旨在守住"143 passed + 4 skipped"基线上扩量。落地时确认 SDK 测试须在项目 venv 下跑(系统 Python 无 claude_agent_sdk 时 4 个 SDK 归一化用例会失败——执行 agent 注意)。理由:测试三族先例(test_state/test_grammar/test_session/FakeAICaller);Phase 2 E2E 门控先例。

### Claude's Discretion
- AUTHORIZATION.md 的具体文案排版(只要含"授权时间 + 操作者确认词标记"两要素、明文、UTF-8)
- 拒绝批注的 quote 默认取点(标题/空串核准)与前端确认框文案细节(确认词输入框防呆样式等)
- 档位模态的两个选项说明文案(照 §8.2 口径即可)
- check 报告视图的具体形态(折叠列表 vs 切换器,归档视图复用 rounds-placeholder 容器或新建 subview)
- 问题分级表的具体列名定案(建议:编号/级别/位置/问题/建议修法——需配正反例测试)
- 循环驱动的实现形态(done 回调直排 vs 显式 driver 函数;无 scheduler)
- 「待裁决」事件截存的具体扫描层(say 事件流 vs 最终 result 文本;建议两者都扫——先流后文本,命中即停)
- selfcheck 子状态的字段命名与 snapshot 组装形态

</decisions>

<specifics>
## Specific Ideas

- 四处机械校验是"机械校验而非采信 AI 自评"(D-17)——按钮点亮是**机器可复核**的,四处任何一条不过就不亮,不存在 AI 哄骗通道;最终否决权仍在用户(确认词)。
- AUTHORIZATION.md 的写入者是**后端且仅后端**——权限矩阵对 AI 拒绝**无任何批准路径**(§5.4 原文"不能容 AI 以任何形式绕过 D-17 防误触")。这是本工具的 Core Value 红线,测试须覆盖"AI 尝试写 AUTHORIZATION.md 被拒"。
- DESIGN.md 的唯一合法落盘路径 = tmp + 后端原子改名——权限矩阵已实现(AI 写 tmp 放行、直写 DESIGN.md 一律拒绝);撰写调用 A/B 双线权限测试已在 Phase 1 完成矩阵,本阶段是消费侧。
- 半份 tmp 不可能产生半份 DESIGN.md:rename 是原子操作(§7.4 行 4 字面"半份 DESIGN.md 不可能存在")。
- 撰写与自检的中断恢复**一律无需重新确认词**(§7.3 原文);AUTHORIZATION.md 存在即凭证,后续 Phase 4-5 的"继续"按钮都直接重跑。
- 严格档循环的两跳**自动到 PASS 为止**——用户点击只发生在异常恢复(「继续自检」「继续修复」)与纯 P2 残余裁决(「修」/「接受现状」),正常路径用户零点击。
- 判定式①②已由 check-14 钉死互斥(②补"且无未配对的待裁决行" + "且末行非 PASS 开头"),grammar.py v1.13 版已按该锁定实现——本阶段**只消费不再修判定式**。
- D-22 残余裁决逐条交用户的 UI 形态是"每问题一张裁决卡:位置+描述+建议修法+〔修/接受现状〕",不是一次性批量表单(§8.2"逐条")。
- 本 phase 完成 = v1.13 milestone 收口:验证通过后走 `/gsd-complete-milestone`,不再有 Phase 4。

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 设计权威(唯一)
- `DESIGN.md`(项目根,v1.13)— 唯一权威设计文档。本阶段重点节:§3.3(未决清单四步与收敛判据,G3 门四处)、§3.8(语言红线,全部新 prompt 注入)、§4.4(三道门交互——G3 权威定义)、§5.1(无状态全量读)、§5.2(事件直播)、§5.4(权限门:DESIGN.md/AUTHORIZATION.md 拒绝、tmp 放行——已实现,本阶段消费)、§5.5(中止)、§6.1(目录结构:AUTHORIZATION.md/docs 下 DESIGN-check-N.md 与 tier 签名落点)、§6.4(**判定式①② + 裁决追加文法 + 幂等内容级——锁定版,grammar.py 已实现,只消费**)、§7.3(崩溃与中断自愈全节——①撰写②核查修复)、§7.4(推导表行 4/5/6/7 + 授权痕迹 + 完成标记 + 只读归档)、§8.1(G3)、§8.2(自检全节:档位、两跳自动、抛问契约、裁决落盘续跑、D-22 残余裁决)、§9(技术栈)
- `DESIGN.md` §11 决策表 — D-04(命名)、D-09(维度表)、D-13(重跑覆盖)、D-14(五阶段三道门)、D-17(授权门槛)、D-19(启动/恢复)、D-21(只读归档)、D-22(纯 P2 残余裁决制)溯源

### 需求与规划
- `.planning/REQUIREMENTS.md` — FLOW-05、DATA-02/03/04 四条需求原文(均标注 DESIGN.md 章节)
- `.planning/ROADMAP.md` — Phase 3 目标与 5 条成功判据(边界锚)
- `.planning/phases/idi-01-1-2/01-CONTEXT.md` — Phase 1 实现决策 D-P1-1~15(单飞锁、权限门、纯函数模块族、推导脊柱、XSS 管线)
- `.planning/phases/idi-02-g2/02-CONTEXT.md` — Phase 2 实现决策 D-P1/2-1~24(annotations/grammar 全族、process_round 模子、done 后回写分支、路由族、窗口刷新);本阶段大规模承接其模子

### 讨论上下文(理解意图参考)
- `docs/discuss-round-4.md` — D-17(授权门槛)/D-18 定案轮
- `docs/DESIGN-check-13.md` — D-22 残余裁决制诞生轮(纯 P2 末轮的裁决实例,问题卡形态参考)
- `docs/DESIGN-check-14.md` — 判定式①②互斥修订收口轮(本阶段消费的判定式即其定稿形态)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets(Phase 1+2 交付物,全部可平移复用)
- `backend/state.py`(164 行)— §7.4 八行推导表**已全量实现**:STATE_PHASE4 / STATE_PHASE5_AWAITING_TIER / STATE_PHASE5_CHECKING / STATE_MISSION_COMPLETE 四常量就绪;`max_check_number`(半份不校验)/`latest_check_content` 直接供判定式消费;PASS_PREFIX / AUTH_MARKER_YES / _CHECK_TEMPLATE 复用。**本阶段对 state.py 的改动 ≈ 0**(.snapshot 层组装 selfcheck 子状态在 session.py)
- `backend/grammar.py`(283 行)— 六条文法全族已锁:`is_pending_list_clear` / `is_dimension_table_green` / `parse_auth_marker`(G3 四查的三条解析现成)+ `is_pass_conclusion` / `parse_verdict_lines` / `unpaired_verdicts`(判定式①②的核心)。**禁改判定式语义**(check-14 锁定版);新增解析仅允许:报告头部档位行、问题分级表(可选)
- `backend/annotations.py`(206 行)— select_pending(G3 四查之一)/append_item(拒绝转普通批注通道,D-P3-5 零新代码)/writeback 模子
- `backend/g1.py`(52 行)— "后端写受控产物 + FileExistsError 幂等防护"形态:AUTHORIZATION.md 写入(D-P3-4)照 finalize_g1 的模子抄
- `backend/session.py`(721 行)— **三种后台流水线模子**(send_message / trigger_divergence / process_round):入口三查 + _ensure_caller + 后台 _worker + SSE 直播 + done 后 else 分支后端动作 + finally 解锁。start_writing / start_check / start_repair 照 process_round(530-629 行)的模子复制;`_session_snapshot` 的字段扩展点(selfcheck / g3_available)在此
- `backend/prompts.py`(352 行)— build_round_prompt 四段结构 + _GRAMMAR_EXAMPLES 逐字模板先例:build_writing/check/repair_prompt 三族照抄形态;_LANGUAGE_RULES 照注入
- `backend/ai_caller.py`(791 行)— 权限矩阵规则 1/2(DESIGN.md/AUTHORIZATION.md 拒绝、tmp 放行)**已生效零改动**;make_permission_decision / 双路线 ask settting_sources 先例;修复/核查调用只走既有 run()
- `backend/main.py`(453 行)— 路由风格(202/409/400 JSONResponse)+ StaticFiles 挂载:八个新端点照旧;`getCurrentProject` 模式
- `frontend/app.js`(1057 行)— applySessionGates 的 **else 分支即 phase4/5/mission_complete 挂点**(274-279 行占位文案);STATE_LABELS 七状态中文名已全含;renderMarkdown→stripUnsafeNodes XSS 管线(新视图全走);权限模态 + CLI 自检浮层是现存的两种 modal 形态(确认词模态/档位模态照抄模子);cilck→POST→SSE→refresh 链(refreshRoundsAfterStream)
- `frontend/index.html`(152 行)— permission-modal / cli-check-overlay 的 overlay-card 结构可复制;rounds-placeholder 容器;selection-menu
- `backend/tests/`(11 文件,143 passed + 4 skipped 于项目 venv)— FakeAICaller(打桩 run 的 script 事件)、fresh_session 夹具、wait_idle;E2E IDI_E2E 门控先例(test_e2e_rounds.py)——新用例照族加
- `.venv/` 是权威运行时(系统 Python 无 claude_agent_sdk,SDK 用例需 venv 内跑)

### Established Patterns(强约束)
- 纯函数模块族(零 FastAPI/AI 依赖):state/transcript/annotations/grammar 四模块既定——新门判定(g3_available 等)同样纯函数
- 入口判定"纯靠磁盘推导,防绕过":divergence/g1/round_process 四先例——G3 与自检入口照抄;前端只是呈现约束,服务端 409 是防线
- 后台线程 + 单飞 _inflight + SSE 直播 + done 后端动作 + 解锁:start_writing/start_check/start_repair 是第四五六次复制
- "文件即状态"绝对律:不新增任何非磁盘状态(选档落盘、裁决落盘、暂停签名落盘)——本阶段的一切按钮显隐判定最终都回落到 derive_state + 报告文法
- AI 产物不修补,重跑覆盖:prompt 逐字给文法模板,解析失败不救(D-P2-18/D-13)

### Integration Points
- `session._session_snapshot()` — 扩展 `g3_available` / `selfcheck`(tier + mode + 暂停问题清单)字段,/api/session 前端拉新
- `process_round` 模子 → start_writing(done 后 tmp→rename)/ start_check(done 后判定下一跳)/ start_repair(done 后判定 next/收口)——三函数的 done-else 分支是本阶段后端动作链的主战场
- `app.js applySessionGates` else 分支(274-279 行)→ 阶段 4/5/归档视图;新增两个模态(确认词/档位)照 permission-modal 结构
- `make_permission_decision` — 零改动消费(AUTHORIZATION.md 拒绝路径已在矩阵)
- 测试:新文法正反例入 test_grammar.py 同族;session 链路入 test_session.py 同族;E2E 入 test_e2e_*(IDI_E2E 门控)

</code_context>

<deferred>
## Deferred Ideas

- AI 生成中途插话/双向流(v2 再议,D-20)与直播回放(D-13)——DESIGN.md 明确永久非目标,永不做
- 历史文档(本项目 docs/DISCUS-round-0~4、check-1~14)回溯改造为文法(§6.4 不回溯)
- 多项目并行、多人协作、云端部署(§1.5 非目标)
- 重新讨论入口(完成态后"另起新目录"是用户手动操作,不做重置功能——D-21 字面)
- 分模块文档拆分(DESIGN.md 头注:可选后续,不得与总设计文档冲突)
- 若 Phase 3 执行中出现超出 v1.13 范围的能力性想法 → 记入本表,由 **下一个 milestone**(complete-milestone 后 /gsd-new-milestone)承接,不塞进本 phase

</deferred>

---

*Phase: idi-03-g3*
*Context gathered: 2026-09-10*

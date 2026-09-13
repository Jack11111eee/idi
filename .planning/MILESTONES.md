# Milestones

## v1.13 交互式讨论迭代系统 MVP (Shipped: 2026-09-13)

**Phases completed:** 3 phases, 13 plans, 28 tasks

**Key accomplishments:**

- FastAPI + 原生前端单页 + AICaller 双轨(SDK 首选/子进程兜底,事件枚举同构)+ §5.4 权限矩阵 + SSE 事件直播 + 中止——`bash run.sh` 一键可用的端到端骨架
- derive_state() 按 §7.4 八行表自上而下首条命中实现"文件即状态"脊柱(含完整轮判据、半成品轮视为不存在、tmp 残留免疫),transcript.md 按 §6.1 `[user]`/`[ai]` 起始行文法实现 parse/append 幂等读写——两纯后端模块零框架依赖,28 用例全绿
- 会话流水线(enter→send_message→[ai] 落盘)+ AI-04 权限弹窗闭环(SDK can_use_tool 与 CLI 控制协议双路线,setting_sources 屏蔽全局 allow 绕过)+ 前端阶段 1-2 视图与重启恢复——真实 claude 链路端到端走通
- 发散模式(无想法冷启动,brainstorm.md 覆盖式落盘、雏形诞生即关闭)+ G1 后端定稿(draft.md→discuss-round-1.md + `> 申请授权:否` 末行标记,direct-through 交互)——Phase 1 十个 REQ 全收口
- annotations.json 读写纯模块(§6.2 八字段/aN-NN id/空形态/回写只认 id)与六条 §6.4 机器文法解析器(维度表/未决清单/授权标记/回应表/PASS 锚点取末一处/裁决同号配对),54 个正反例用例 + 回写闭环全绿,基线 66→120 不降
- G2 全流水线(process_round 入口三查+单飞+SSE 直播+done 后回应表解析回写上一轮 annotations)与大白话 ask_lite 双路线同步调用、五条轮次路由(202/409/404/400/502)落下,23 新用例 + uvicorn 冒烟全绿,基线 120→143 不降
- 轮次视图(切换器+文档渲染+批注流侧栏+未处理数)替换 rounds-placeholder,划词弹原生菜单两项落盘(方向无关 before)、highlightAnnotations 包 mark、处理本轮批注按钮挂 done 后拉新链(新轮+上轮冻结灰化)——纯原生 JS 零新依赖,三条 uvicorn 冒烟对账全绿
- 真 CLI 全链 E2E(SDK 路线)证明 answer_plain 秒级回 + process_round 产文法合规新轮 + 回写 + 推导态前进;发现的 AI 越界读缺陷以 prompts 资料完备性段修复;真机观测驱动的挂退避重试测试基建;Phase 2 六 REQ 以 7 判据对账表收口
- G3 四查组合判定 + AUTHORIZATION.md 后端写入、tier 档位签名与报告尾部追加族(待裁决/裁决/PASS)、grammar 四新解析器(tier 行/问题分级表/纯 P2/待裁决扫描)——Phase 3 全部上层的纯函数 import 基座,143→176 passed 零失败
- G3 授权入口(四查服务端再查→AUTHORIZATION.md)与撰写 tmp 原子改名流水线、检查者/修复者两角色 prompt 族、严格档两跳自动循环引擎(done-回调直排 + 抛问截存暂停 + 半份不跳号)、选档/裁决同步落盘与残余收口、快照 selfcheck 子状态 + 5 条新路由(authorize/tier/verdict 三 POST + design/checks 两 GET)——176→209 passed 零失败
- D-P3-27 八条路由族收口:POST /api/writing、/api/checks/start、/api/checks/repair 三条 202 受理路由照 /api/rounds/process 模子接线(路由层零判定透传 session)+ 7 条 route 级全分支用例——209→216 passed 零失败,prompts.py 零改动确认

---

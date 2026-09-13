# Phase 3: 授权、自检与终点——G3、档位、使命完成归档 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in 03-CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-10
**Phase:** 3-授权、自检与终点——G3、档位、使命完成归档
**Areas discussed:** 阶段边界与 milestone 收口、G3 门与授权流水线、撰写与 tmp 原子落盘、档位选择与磁盘签名、两角色自检循环引擎、D-22 残余裁决、判定式与三个继续按钮、mission_complete 与只读归档、路由与契约、测试基线
**Mode:** --auto(Claude 按推荐项自动选择;决策源 = DESIGN.md v1.13 既有章节/决策,非新造)

---

## 阶段边界与 milestone 收口

| Option | Description | Selected |
|--------|-------------|----------|
| G3 + 撰写 + 自检 + 归档 + 崩溃自愈全链(ROADMAP Phase 3 字面) | FLOW-05/DATA-02/03/04 全部及其界面/路由/prompt 配套 | ✓ |
| 把 PASS/裁决行文法解析也拉进本阶段 | Phase 2 已交付(grammar.py 六条),D-P2 判定式①②为 check-14 锁定版,只消费 | |
| 顺手改阶段 1-3 的既有交互 | Phase 1/2 已定版验收,越界 | |

**User's choice:** [auto] 按 ROADMAP 字面;解析归 P2、消费归 P3(D-P2 边界裁定沿用)
**Notes:** 本 phase = v1.13 milestone 最后一个 phase,完成即 complete-milestone;超出 v1.13 的想法记 Deferred 交下一 milestone。

## G3 门与授权流水线(FLOW-05)

| Option | Description | Selected |
|--------|-------------|----------|
| 四处校验组合成新纯函数 g3_available(复用 annotations/grammar 现成函数) | §4.4 "四处机械校验"字面;D-17 机械校验非采信 AI 自评 | ✓ |
| 每条校验散在前端各处拼 | 防绕过失效(前端只是呈现),且与四先例"入口判定纯靠磁盘"冲突 | |
| derive_state 里加 G3 状态 | derive 只做阶段推导(行 3 即 phase3),G3 是行内门——不混层 | |

**User's choice:** [auto] 组合函数 + 后端入口重判
**Notes:** 确认词「确认授权」strip 全等;模态在前端;后端防线 = "四查通过瞬间才写 AUTHORIZATION.md" 动作本身(不重复解词,§7.4 凭证语义)。幂等照 g1(FileExistsError→409)。
[auto] 拒绝路径子问题:拒绝转"一条普通批注" → 选中复用 annotations 通道(type=comment),quote 取当前轮文档锚点、note 写明还差什么(§4.4/§8.1 "普通批注"原文)。备选"独立拒绝文件"被否——§8.1 字面即批注。

## 撰写与 tmp 原子落盘(FLOW-05/Data-02 / §7.3①)

| Option | Description | Selected |
|--------|-------------|----------|
| AI 写 DESIGN.md.tmp + done 后后端 Path.rename 原子改名(照 process_round done-else 模子) | §5.4 tmp 是唯一合法路径;D-13 重跑覆盖推广 | ✓ |
| AI 直接写 DESIGN.md | 权限矩阵规则 1 一律拒绝(§5.4 明文) | |
| 后端拼 DESIGN.md(不靠 AI) | 与 §5.1 "产出写回磁盘"、D-10 无头调用哲学冲突 | |

**User's choice:** [auto] AI 写 tmp + 后端改名
[auto] 中断续跑子问题:半份 tmp 残留 → derive_state 照行 4 = phase4 → 「继续撰写」重跑覆盖,无需确认词;重跑资料段**不含 tmp 内容**(tmp 是被覆盖物)——若 AI 拿半份当参考会产生"在烂稿上续写"路径,与"整体覆盖"语义冲突。§7.3① 字面。

## 档位选择与磁盘签名(DATA-04 / §8.2)

| Option | Description | Selected |
|--------|-------------|----------|
| 档位落盘 = docs/ 下 tier 签名文件(选档即写);报告头部行是 tier 的拷贝,已有报告后一切照最新报告头部 | D-19 "文件即状态"硬要求 + §8.2 字面"记录于每份核查报告头部" | ✓ |
| 档位只存内存/前端 local | 违反 D-19;重开丢档 | |
| 档位作为 check-1 报告内字段(首报告前无档) | "尚未产生首份报告时重开重新弹选"仍需磁盘凭证,首报告前窗口期无态 | |

**User's choice:** [auto] tier 签名文件 + 报告头部行双轨
**Notes:** 选档幂等(重开 phase5_awaiting_tier 无报告 → 重新弹,§8.2 字面);已有报告 → 从最新报告头部恢复,不弹。

## 两角色自检循环引擎(DATA-04 / §8.2)

| Option | Description | Selected |
|--------|-------------|----------|
| 后端循环驱动:check done → 判末行(PASS→终点 / 纯 P2→裁决 / P0P1→自动修复);修复 done 无待裁决 → 改名 + 自动下一轮 check;恢复入口 = 三个按钮 | §8.2 "循环的两跳均为后端自动……无需用户点击" | ✓ |
| 每跳要用户点「下一步」 | 直接违反"无需用户点击"字面 | |
| 常驻后台 scheduler 轮询磁盘 | 引入新进程机制,违反 done-事件驱动既有惯例 | |

**User's choice:** [auto] done-回调和直排驱动形态
[auto] 抛问识别子问题:`> 待裁决:` 前缀事件截存 → 复用 D-20「不做中途插话」哲学,定为 **协议约定**(prompt 里写明输出协议)而非新增交互流;幂等 = 内容级(§6.4 同字不重复追加)。备选"识别 AI 特定 tool call 停下"更复杂且无新信息。
[auto] 全部裁决收口子问题:纯 P2 残余全部处理完 = **后端立即在最新报告末追加 PASS**(后端动作,机器判"残余清零" = 配对数==问题数)——不唤起 AI。备选"再起一轮 check 落实『修』"被否:违反"不再自动进入下一轮循环"字面(D-22)。

## D-22 残余裁决(check-13 后)

| Option | Description | Selected |
|--------|-------------|----------|
| 残余逐条裁决卡:位置+描述+建议修法 +〔修 / 接受现状〕;裁决与 D-P3-19 同一落盘通道(`> 裁决:#K:`) | §8.2 D-22 字面"逐条交用户裁决「修」或「接受现状」" + ROADMAP 判据 4 | ✓ |
| 一次性呈现全部问题批量选 | "逐条"字面冲突 | |
| 「接受现状」不落盘 | 裁决记录补录为正式决策(D-22 字面),必须落盘 | |

**User's choice:** [auto] 逐条卡 + 同一裁决通道
**Notes:** 纯 P2 判定来源:报告问题分级表(P0/P1/P2 列解析,表头文法待 planner 逐字定死)——新增 Mini 文法须配正反例测试(见 D-P3-29 测试注意)。

## 判定式与三个继续按钮(DATA-02 / §6.4)

| Option | Description | Selected |
|--------|-------------|----------|
| 暂停态 / 裁决待续跑态 / 意外中断三态,严格照 §6.4 判定式①②(check-14 互斥锁定版),consume grammar 已有函数 | 文法已交付;判定式勿再自造或重复实现,语义冲突以 DESIGN.md 为准 | ✓ |
| 把三态做成 derive_state 新状态值 | state.py 七常量已覆盖;snapshot 层组装 selfcheck 子状态即可(推导表不动) | |

**User's choice:** [auto] 三态 = 判定式 + derive 层组装(D-P3-20/D-P3-23)
**Notes:** 「继续自检」仅意外中断恢复,两暂停态各自隐藏(§8.2/§7.3②);"继续修复"在裁决落盘前不呈现(防误点重跑,check-10 已记)。半份报告/半份 tmp 自愈均走重跑覆盖(§7.3②/§6.1 注),不新增恢复机制。

## mission_complete 与只读归档(DATA-03 / D-21)

| Option | Description | Selected |
|--------|-------------|----------|
| state == mission_complete(最新 check 末行 PASS 前缀,derive_state 已实现)→ 前端拉新感知 → 一次性欢呼模态 → 只读归档视图(浏览 DESIGN.md/全部轮/全部报告;划词/处理/授权/发散/消息面全关) | §7.4 + §8.2 终点定义、D-21 只读归档 | ✓ |
| 后端新增"归档标志文件" | mission_complete 本身是推导态(§7.4 行 7),新增冗余 | |

**User's choice:** [auto] 零新增状态,呈现即推导
**Notes:** 划词菜单 currentState!=='phase3' 防线已天然生效;process_round 入口 409 双防线;授权按钮只在 phase3 分支安放——天然不可达。「使命完成」重开重现弹一次属合符语义(会话内存标记)。

## 路由与契约

| Option | Description | Selected |
|--------|-------------|----------|
| 八新端点(照 202/409/400 先例)+ /api/session snapshot 扩展(g3_available / selfcheck)+ done 后拉新链复用 | main.py 路由族先例 + G-idi01-7 刷新惯例 | ✓ |
| 自检驱动过程新增专用事件类型驱动前端刷新 | 现有 done 事件收尾后拉新已够,事件枚举扩新会破坏双路线一致性负担 | |

**User's choice:** [auto] 路由族 + 拉新链复用
**Notes:** 阶段 4/5/归档视图挂点 = applySessionGates else 分支(现占位);确认词/档位模态照 permission-modal 结构复制;XSS 管线(stripUnsafeNodes)覆盖全部新数据入口(AI 报告/DESIGN.md/裁决文本都不可信)。

## 测试基线(实施前提)

| Option | Description | Selected |
|--------|-------------|----------|
| 纯函数正反例 + session/FakeAICaller 链路用例 + E2E 真调门控;不在本阶段引入新基建 | 三族先例 | ✓ |

**User's choice:** [auto] 三族照旧
**Notes:** 本环境权威运行时 = **项目 `.venv/`**(系统 Python 无 claude_agent_sdk,4 个 SDK 归一化用例在系统 Python 下会失败——勿误判为回归;`143 passed + 4 skipped` 基线在 venv 内确认)。

---

## Claude's Discretion

- AUTHORIZATION.md 文案排版、拒绝批注 quote 取点、档位选项文案、归档视图/报告视图控件形态、循环驱动实现形态(done 回调 vs 显式 driver)、待裁决事件扫描层(say 流 + result 文本双扫)、selfcheck 子状态字段命名(见 03-CONTEXT.md Claude's Discretion 八项)

## Deferred Ideas

- 超出 v1.13 范围的能力性想法 → 下一 milestone(complete-milestone 后 /gsd-new-milestone)
- D-20 中途插话、D-13 直播回放、§6.4 历史回溯、多项目/多人/云端、重置已归档项目、分模块文档 → 永久非目标或 v2(见 DESIGN.md §1.5)

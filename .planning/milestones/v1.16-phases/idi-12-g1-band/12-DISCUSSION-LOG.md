# Phase 12: G1 表头 band 与里程碑收口 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-29
**Phase:** 12-G1 表头 band 与里程碑收口
**Areas discussed:** band 修法路线, G1 运行时取证, G1 视觉取证形态, REG-04 连带面

---

## band 修法路线

| Option | Description | Selected |
|--------|-------------|----------|
| 移宿主 → 改白 | `#latest-check` 的 background 改 `--color-surface-page`(白)。四个宿主读感一致,band = gray-2 on white(1.053)—— 文档区表头已签核的读感。零新增对比度条目、check-10 t1 全绿、零门改写。代价:Phase 11 SC2 点名「`#latest-check` 仍读作内陷」不再成立,围栏 :129-130 须改写 | ✓ |
| 移宿主 → gray-3 | `#latest-check` 改 `--color-surface-sunken`。内陷更深,band = 1.082。但 `.markdown-body code` 的底也是 gray-3、无边框、无等宽字体 ⇒ 行内 code 与宿主撞死 | |
| 移表头 → 全局 th | `.markdown-body th` 换到 gray-3,band 最强(1.140)。但文档区表头读感一并变深,且 check-10 t1 的 5 对断言 + `TH_BG_LITERAL` 全部要改写 | |
| 局部覆盖 th | 追加 `#latest-check th { background: gray-3 }`。最外科,但引入宿主特例,且 check-10 的 `("p1","#latest-check")` 那一对要改写 | |

**User's choice:** 移宿主 → 改白
**Notes:** 选它同时满足三条:消除「四个宿主里唯一画灰底」这个不对称本身;band 读数与文档区表头完全一致;唯一不需要改写任何门的路线。

| Option | Description | Selected |
|--------|-------------|----------|
| 锚「底色不同」 | 判据 = `#latest-check` 计算底色 != `th` 计算底色 + 截图人眼确认。与 G1-01 原文一致 | ✓ |
| 锚「与文档区同值」 | 再把「报告区 th 读数 == 文档区 th 读数」写成可失败判据 | |
| 1.053 不够强 | 回头改全局 `th` 或加局部覆盖 | |

**User's choice:** 锚「底色不同」
**Notes:** 用户看过 1.053 这个读数后仍选最小锚 —— **不追求更强的 band**,planner 不得自作主张加深。

| Option | Description | Selected |
|--------|-------------|----------|
| 不动(推荐) | G1-01 只谈 band;`#latest-check` 是内陷可滚区、不是面板;`probe-card-border-token.py` 把它的 gray-6 边框当作「非卡片」对照样本 | ✓ |
| 圆角归零 | 与 Phase 11 把 `.panel-header` 圆角归零同向,但会造出与 `.event-list` 等内陷容器不一致的特例 | |
| 去掉四边边框 | 报告与面板彻底连成一片,但可滚区 affordance 丢失 | |

**User's choice:** 不动
**Notes:** 边界与圆角保持 1px gray-6 + `--radius-sm`。

| Option | Description | Selected |
|--------|-------------|----------|
| 都不纳入(推荐) | 过期注释属审计的「gate blind spot」项(已列未裁定);sticky 是新能力 | ✓ |
| 只修过期注释 | 改 `check-10:328` 的 note 字符串,但会拖入归档的 `idi-10-VERIFICATION.md` | |
| 两条都纳入 | 同时把「报告区表头 sticky」做成新能力 | |

**User's choice:** 都不纳入
**Notes:** 两条记入 Deferred。

---

## G1 运行时取证

| Option | Description | Selected |
|--------|-------------|----------|
| 补 fixture 的表(推荐) | 给 `checking` 的报告补上 `prompts.py:494-499` 要求的「问题分级表」。fixture 忠于后端文法,`checking.png` 也真的会显示表 ⇒ 读数与截图同时成立 | ✓ |
| 注入探针表 | 照 check-10 的 `_PROBE_JS` 注入,样本零改动,但截图仍看不到表 | |
| 两者都做 | 补 fixture + 注入探针,证据最齐但两套机制并存 | |

**User's choice:** 补 fixture 的表
**Notes:** `#latest-check` 只在 `checking` 可见,而该样本的报告里没有表 —— 这是 G1 从未被看见的机械原因。

| Option | Description | Selected |
|--------|-------------|----------|
| 落成永久断言(进 check-09) | 加进 `scripts/check-09-idi09-validation.py`;零新增连带覆盖者(idi-11 的 covered_files 已同时含 style.css 与 check-09)。超出 ROADMAP 的 Gate 清单,但判为在范围内(G1 自己的判据,非通用 blind spot 加固) | ✓ |
| 一次性探针 | 照 `probe-card-border-token.py` 先例,零门改动但无回归保护 | |
| 只记 SUMMARY + 截图 | 最轻,但审计刚批评过「只靠截图/接线不够」 | |

**User's choice:** 落成永久断言(进 check-09)
**Notes:** 须配变异证明(底色改回 gray-2 ⇒ 必 FAIL)。

| Option | Description | Selected |
|--------|-------------|----------|
| 钉「宿主==白」+「不同」(推荐) | 既断言两者底色不同,也断言 `#latest-check` 底色 == `--color-surface-page` 解析值。可满足且有判别力 | ✓ |
| 只钉「两者不同」 | 宿主改成任何别的档(含 gray-4)都绿,判别力弱 | |
| 再钉「两区 th 同值」 | 最强,但需一个能同时读到两个区 th 的读数面 | |

**User's choice:** 钉「宿主==白」+「不同」
**Notes:** 把「改白」这件事本身也锁住。

| Option | Description | Selected |
|--------|-------------|----------|
| 只加那张表 | 只加 `| 编号 | 级别 | 位置 | 问题 | 建议修法 |` 表;fixture 其余部分(缺档位头部行、`## 发现` 小节)保持原样 | ✓ |
| 对齐完整文法 | 把 `check-2` 改写成与 `prompts.py:486-502` 逐字一致 | |
| 加表 + 档位行 | 折中 | |

**User's choice:** 只加那张表
**Notes:** 最小改动,符合 CLAUDE.md 第 3 条。

---

## G1 视觉取证形态

| Option | Description | Selected |
|--------|-------------|----------|
| 追加局部特写(推荐) | 5 张整窗图照旧,额外加一张 `#latest-check` 元素截图(照 `check-10:653` 先例) | ✓ |
| 只用 5 张整窗图 | 最贴 VIS-01 原文,但 band 在 1440×900 里可能小到看不出 | |
| 不加图，只调滚动位 | 解决「拍到了但没拍到 band」的风险,产物仍只 5 张 | |

**User's choice:** 追加局部特写
**Notes:** 局部图才是 G1-01 的直接人眼证据。

| Option | Description | Selected |
|--------|-------------|----------|
| 紧跟标题行(推荐) | 表紧跟 `# 核查报告 2` 之后,保证落在 30vh 可视区内,且最贴文法顺序 | ✓ |
| 放在发现之后 | 更接近现有叙述顺序,但有落在 30vh 以下的风险 | |
| 替掉发现列表 | 最像真实报告,但与「只加那张表」相悖 | |

**User's choice:** 紧跟标题行
**Notes:** `max-height: 30vh` 是滚动区,位置直接决定截图能否拍到 band。

---

## REG-04 连带面

| Option | Description | Selected |
|--------|-------------|----------|
| 登记为已知限制(推荐) | 归档报告的 covered_files 路径不可解析 ⇒ fail-closed stale(2026-09-14 已登记),不重验但**逐份列名**进 SUMMARY | ✓ |
| 修复路径后重验 | 先把路径修到 `milestones/` 下再逐份重验 —— 属「修归档」,超出范围 | |
| 只处置在盘那份 | 11 份归档连名单都不列 | |

**User's choice:** 登记为已知限制
**Notes:** 磁盘实测共 **12 份**报告命中(11 归档 + 1 在盘);`idi-11-VERIFICATION.md` 以 HEAD 内容重新验证。⚠ 讨论中 Claude 一度把份数说成 14/13,已当场更正为 12/11。

| Option | Description | Selected |
|--------|-------------|----------|
| 不含里程碑审计(推荐) | Phase 12 = G1 + REG-04 复跑 + VIS-01 截图;v1.16 审计走 `/gsd-audit-milestone`(与 v1.15 同路径) | ✓ |
| 含里程碑审计 | 并入本阶段 —— 但审计的前提是「所有阶段已收口」,在 Phase 12 内跑会自我指涉 | |

**User's choice:** 不含里程碑审计
**Notes:** Phase 12 的 Requirements 只列 G1-01 / REG-04 / VIS-01。

---

## Claude's Discretion

- 新断言在 check-09 里的落位(新增 `c6` 还是并入既有 item)与命名
- 元素截图的具体实现细节(选择器、文件名、是否与 5 张同目录、是否在 check-09 的 `--screenshot` 分支里产出)
- `checking` fixture 报告里那张表的具体行数与内容(列头必须逐字,级别仅 P0/P1/P2;须落在 30vh 可视区内)
- 变异测试的执行顺序与还原手法细节(须满足:已提交的树上做、定向 `git checkout`、还原后逐字节相同、禁用 `git stash`)
- 全量复跑与截图的时间顺序(硬约束只有一条:都落在最后一次 `style.css` 与 fixture 改动之后)

## Deferred Ideas

- `check-10` t1 的过期注释(`scripts/check-10-idi10-validation.py:328`)—— 属审计的「gate blind spot」项
- 报告区表头在 `#latest-check` 内 sticky(与 `#doc-panel-header` 同语言)—— 新能力
- `#latest-check` 的边框 / 圆角改动 —— 本阶段明确不动
- G2(`--radix-gray-1` 零消费 + 通用围栏消费断言)—— 用户未点名
- `999.2`、暗色模式(`A11Y-V2` / `FLOW-V2` / `TOKEN-V2`)、Nyquist 缺口、图标与空状态
- 11 份归档报告的可执行性(路径不在盘)—— 按已知限制登记,不修复归档路径
- v1.16 里程碑审计 —— 走 `/gsd-audit-milestone`

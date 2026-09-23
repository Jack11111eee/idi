# Phase 04.1: Radix 颜色族重写 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-19
**Phase:** 04.1-radix
**Areas discussed:** Radix 交付方式, 令牌名与契约归属, 色族选型与 AA 步骤, UAT 3 项消解口径, 两个补讨论的空白

---

## Radix 交付方式

| Option | Description | Selected |
|--------|-------------|----------|
| 手工转抄 hex 进 :root | 把每族用到的 12 步 hex 值直接写成围栏内的 tier-1 primitive。零新文件、vendor gate 不动、依赖为零,颜色值仍只有围栏一个事实源 | ✓ |
| vendor Radix 的 CSS 文件 | 放进 `frontend/vendor/` 并在 index.html 引入。上游更新可整体替换、日后暗色模式现成;代价:颜色值出现第二个事实源(围栏外),需修正 Phase 4 的 vendor gate 断言,126 个文件里绝大多数本阶段不用 | |
| 只借刻度结构不借值 | 只采用 12 步语义结构,hex 自己调。完全可控;代价:严格说这不是「换成 Radix Colors」,与 ROADMAP 的 goal 字面有出入 | |

**User's choice:** 手工转抄 hex 进 :root
**Notes:** 无额外说明。理由记录于 CONTEXT.md D-01。

---

## 令牌名与契约归属

### Q1 — tier-2 的 49 个语义令牌名是否逐字冻结?

| Option | Description | Selected |
|--------|-------------|----------|
| 逐字冻结 | 全部选择器 / CHECK-02 按名配对清单 / Phase 5 的 VISUAL-01/02 都引用这些名;冻结后是真正的纯值替换(SC2) | ✓ |
| 随 Radix 重命名 | 名与刻度一一对应,自文档化;代价:所有 `var()` 引用要改、清单重写、Phase 5 计划引用的名失效,diff 巨大 | |

**User's choice:** 逐字冻结

### Q2 — tier-1 的 26 个 primitive 名怎么处理?

| Option | Description | Selected |
|--------|-------------|----------|
| 换成 Radix 刻度名 | `--gray-600` 现在指「中灰」,Radix 的 `gray-6` 指「细边框」,名实不符。改成 `--radix-<family>-<step>` | ✓ |
| 保留原 26 名、只换值 | diff 最小;代价:名会说谎 | |
| 两套并存(旧名作别名) | 同一值两个名 = 第二事实源,与 CHECK-01/02 按名机制冲突 | |

**User's choice:** 换成 Radix 刻度名

### Q3 — 每族声明完整 12 步,还是只声明消费到的步?

| Option | Description | Selected |
|--------|-------------|----------|
| 只声明消费到的步 | 遵守 Phase 4 已立的 Pitfall 1 / Hard Rule 5。代价:刻度不完整,Phase 5 取新步时要改围栏 | ✓ |
| 每族完整 12 步 | 刻度即产物,序关系完整,Phase 5-7 免改围栏;代价:约 84 个 primitive 中约半数无消费者,与 Pitfall 1 字面冲突 | |

**User's choice:** 只声明消费到的步

### Q4 — 04.1 的 UI-SPEC 与 04-UI-SPEC.md 是什么关系?

| Option | Description | Selected |
|--------|-------------|----------|
| 04.1 只重写颜色两节 | 新建 04.1-UI-SPEC.md 只含 Color + Contrast Verification;其余节声明 04-UI-SPEC.md 仍为权威并在 canonical_refs 指向它。零重复、零漂移 | ✓ |
| 04.1 完整重发一份 | 单一入口;代价:1179 行重复,两份必然漂移 | |
| 就地改 04-UI-SPEC.md | 与已定路线(跑 `/gsd-ui-phase 04.1`)冲突,且 Phase 5-8 读的是 04.1 的目录 | |

**User's choice:** 04.1 只重写颜色两节

---

## 色族选型与 AA 步骤

### Q1 — 中性族选 Radix 的哪一支?

| Option | Description | Selected |
|--------|-------------|----------|
| Radix gray | 纯中性无色偏;现有 gray 值全是 r=g=b,是字面对应,视觉变化最小 | ✓ |
| Radix slate | 冷偏蓝,现代 SaaS 观感;代价:全部中性色带蓝调,是可见的换肤 | |
| Radix sand | 暖偏黄,与琥珀强调色同温;代价:与现有冷白底相比暖得明显 | |

**User's choice:** Radix gray

### Q2 — 强调色族的取法

| Option | Description | Selected |
|--------|-------------|----------|
| 逐族取最接近的现有色相 | blue→blue / green→green / amber→amber / red→red / purple→violet。关键:AA 保证来自**步的选择**而非族的归属,不必为对比度牺牲色相 | ✓ |
| 采用 Radix 规范色相 | 后续跟上游同步时无需再判断;代价:每个颜色都肉眼可见地变,与刚定下的 ChatGPT 视觉语言脱钩 | |

**User's choice:** 逐族取最接近的现有色相

### Q3 — 第 11 步在最深的那个底上过不了 4.5:1 时怎么办?

| Option | Description | Selected |
|--------|-------------|----------|
| 换背景步,保住 muted = 11 | 把该背景提到更浅的步;保住同族层级结构。代价:`--color-surface-hover` 变浅会削弱 hover 可见性 | ✓ |
| muted 提到 12 步 | 背景不动;代价:12 步是刻度顶端,ORDER「muted 比正文安静」失去同族内的序依据 | |
| 逐对交 CHECK-02 裁定 | 沿用 Pitfall 4a「最浅的通过值」;规划器拿不到结论时停下来问 | |

**User's choice:** 换背景步,保住 muted = 11
**Notes:** 该选项的代价(hover 可见性)在补讨论中被单独拿出来核实,见下。

### Q4 — 重映射的范围

| Option | Description | Selected |
|--------|-------------|----------|
| 全部角色都重映射 | 底 / 组件底 / 边框 / 实心填充 / 文字 —— 即 goal 的字面。代价:边框与实心填充也换值,本阶段最大视觉面 | ✓ |
| 只重映射文字角色 | 边框/实心填充保持现有 hex;代价:围栏里 Radix 值与手调 hex 并存 = 半迁移状态(Pitfall 1) | |

**User's choice:** 全部角色都重映射

---

## UAT 3 项消解口径

（本节先由 Claude 把 20 条失败按性质分为四类:①颜色值漂移 ②被删除的声明 ③间距/字号漂移 ④选择器不存在 —— 四类的答案不同,故分四问。）

### Q1 — 被 260918-qrq 删除的两条声明怎么处理?

| Option | Description | Selected |
|--------|-------------|----------|
| 两条都恢复 | `#state-badge` 的 z-index(让 TOKEN-07 的承重序重新有消费者)+ `.overlay-card` 的 box-shadow(需新立 shadow 令牌)。依据:SC2 要求无增删声明,这两条是 260918-qrq 遗留的 SC2 偏差 | ✓ |
| 只恢复 z-index | `.overlay-card` box-shadow 判为有意简化,改 UAT 期望值为 none;代价:该删除仍无记录决策依据 | |
| 都不恢复,改 UAT | 04.1 严格只做颜色值;代价:TOKEN-07 的序继续无消费者,SC2 偏差被永久接受 | |

**User's choice:** 两条都恢复

### Q2 — 间距 / 字号的 7 条漂移怎么处理?

| Option | Description | Selected |
|--------|-------------|----------|
| 更新 UAT 接受现状 | 接受 6/10px 与 14/16/18/24;附带必做:复核 Phase 5 SC5 / Phase 6 SC5 下游门引用的字号 | ✓ |
| 回退到 D-16 账本值 | 恢复账本一致性;代价:直接违反 04.1 goal「不改 S-1/S-2」,且打破已签核的 S-2 | |

**User's choice:** 更新 UAT 接受现状

### Q3 — `#doc-pane` 选择器不存在这条 BLOCKED 怎么收?

| Option | Description | Selected |
|--------|-------------|----------|
| 改 UAT 为 `#doc-panel-body` | 硬规则 5 明写 id 不得改名或删除;实测该元素 padding 与期望一致,只是名对不上 | ✓ |
| 恢复 `#doc-pane` 这个 id | 代价:直接违反硬规则 5,且要同步改 app.js 句柄 | |

**User's choice:** 改 UAT 为 `#doc-panel-body`

### Q4 — UAT 期望值的表述方式

| Option | Description | Selected |
|--------|-------------|----------|
| 全部改为令牌接线表述 | 运行时读 `getComputedStyle` 解析出的 `--token` 值比对,不再硬编码 rgb。test 6 已用此写法并 PASS。这是根因的结构性修复 | ✓ |
| 保持硬编码 hex | 断言更硬(能抓令牌接错线);代价:令牌值层改动必然产生一批假 FAIL —— 本次就是 | |

**User's choice:** 全部改为令牌接线表述

---

## 补讨论的空白（用户主动要求继续讨论）

### Q1 — CHECK-02 配对清单重算后是多大?

| Option | Description | Selected |
|--------|-------------|----------|
| 按实际落地对重新枚举 | 围栏 L160-166 的契约是「枚举真实发生的组合」,不是覆盖面指标;附带记档 24 / 34 / 34 三个数字的差异 | ✓ |
| 固定维持 34 对 | 与 goal 字面一致;代价:落地对若有增减,清单会带假对或漏对 —— 而清单的全部价值就在于不漏 | |
| 扩成完整矩阵 | 覆盖面最大;代价:生成大量实际不落地的组合,与契约相反 | |

**User's choice:** 按实际落地对重新枚举

### Q2 — `--color-surface-hover` 变浅的代价怎么处理?

| Option | Description | Selected |
|--------|-------------|----------|
| 先核实该对是否真实 | 把「第 4 个底是否真实」当待核事实;若不成立就从清单删掉该对,hover 底保持可见步,代价归零 | ✓ |
| 保留该对,hover 改靠边框 | hover 底提到更浅步,靠 border-color 变化维持可见性;需新增一条 border-color 声明 | |
| 保留该对,记为已知例外 | hover 底保持可见步,该对接受 < 4.5:1;代价:与本阶段中心目标直接矛盾 | |

**User's choice:** 先核实该对是否真实
**Notes:** Claude 在本轮核实了静态证据并当场报告:`--color-surface-hover` 只有 `button:hover`(L353)一个消费者;`--color-text-muted` 的消费者全是 `<p>`/`<span>`/`<summary>`/`<div>`;扫过 `index.html` 全部 `<button>` 块无任何 muted-text 类元素。故该对**很可能是 Phase 4 的保守过度收录**,Claude 先前标出的「hover 变浅」代价可能是假的。保留项:`app.js` 动态渲染的节点需一并核实。

---

## Claude's Discretion

- 每族具体取哪个 Radix 族与哪几个步(在 D-06/D-07/D-08 的原则下),由规划期按现有 hex 逐族比对后定。
- 恢复 `.overlay-card` box-shadow 所新立的 shadow 令牌的命名与形状。
- 围栏内注释的措辞与粒度。

## Deferred Ideas

讨论中未出现范围蔓延。以下为 Claude 主动排除并记档的项:

- 暗色模式 / `prefers-color-scheme` —— v2 `TOKEN-V2-01`,本阶段与 v1.14 全局均已排除。
- `#state-badge { right: 448px }` 魔法数消除 —— `LAYOUT-01`,Phase 6。
- `.overlay-card` box-shadow 令牌的最终形状 —— 本阶段只要求「新立一个令牌」使其不成为围栏外裸 `rgba`。
- `#probe-controls` 的移除或重定位 —— 产品行为变更,v1.14 全局已裁定不进任何阶段。
- Phase 5 的实心填充分化 —— 本阶段保持三族共享值不动。

## 附:方法论文档化的两条观察

- **本阶段最重要的立场是不采信上游的 AA 论断。** 本次会话 web 访问被阻断,未能核对 Radix 官方文档;即便能核对,也应一律以 `scripts/check-02-contrast.py` 算出的**真实比值**为准 —— 上游的保证是在上游的背景组合上成立的,而 CHECK-02 存在的全部理由就是回答「在**我们的**组合上成立吗」。
- **UAT 的 20 条假 FAIL 是一条可复用的教训。** 根因不是产品缺陷,而是「期望值定稿于值层改动之前」。D-14 的令牌接线表述把这个失效模式从根上关掉。
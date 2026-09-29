# Roadmap: 交互式讨论迭代系统

## Milestones

- ✅ **v1.13 交互式讨论迭代系统 MVP** — Phases 1-3 (shipped 2026-09-13) — 20 条需求(FLOW 7 / UI 4 / AI 5 / DATA 4)全部交付 — 详见 `milestones/v1.13-ROADMAP.md`
- ✅ **v1.14 前端视觉与可访问性** — Phases 4-8 (shipped 2026-09-26) — 38 条需求(TOKEN 8 / VISUAL 5 / TYPE 3 / A11Y 9 / LAYOUT 4 / INTERACT 2 / CHECK 4 / REG 3)全部交付 — 详见 `milestones/v1.14-ROADMAP.md`
- ✅ **v1.15 视觉构图升级** — Phases 9-10 (shipped 2026-09-28) — 12 条需求(CARD 3 / VIS 2 / REG 2 / TABLE 2 / RADIUS 2 / REG-03)全部交付 — 详见 `milestones/v1.15-ROADMAP.md`
- 🚧 **v1.16 界面去卡片化 —— 连续面与发丝分隔线** — Phases 11-12 (in progress) — 12 条需求(SURF 3 / DIV 3 / REG 4 / G1 1 / VIS 1);Phase 11 反转 v1.15 Phase 9 的卡片语言(连续白面 + 1px 发丝线)并同步改写 `check-09` 的 c1..c4(承重);Phase 12 修 G1 表头 band 并以整里程碑复跑 + 5 张截图收口

## Phases

<details>
<summary>✅ v1.13 交互式讨论迭代系统 MVP (Phases 1-3) — SHIPPED 2026-09-13</summary>

- [x] **Phase 1: 行走骨架——服务器、单界面与阶段 1-2 会话** (4/4 plans) — completed 2026-09-09
  启动自检 CLI、选目录进入单界面、状态由磁盘推导、阶段 1-2 连续会话(transcript 恢复)、AI 双轨调用与事件直播、发散模式、G1 认可雏形
- [x] **Phase 2: 轮次收敛循环——划词批注、G2 与机器文法** (4/4 plans) — completed 2026-09-10
  划词批注与大白话双轨、处理本轮批注产出下一轮、上轮冻结只读、§6.4 文法机械校验、annotations 字段写回
- [x] **Phase 3: 授权、自检与终点——G3、档位、使命完成归档** (5/5 plans) — completed 2026-09-13
  G3 四处校验与确认词、DESIGN.md.tmp 原子落盘、宽松/严格自检循环与 D-22 残余裁决、崩溃自愈、完成态只读归档

**Milestone scope:** DESIGN.md v1.13 全部 20 条需求(FLOW 7 + UI 4 + AI 5 + DATA 4)交付并验证。
验证记录:各阶段 `*-VERIFICATION.md`(Phase 1: 8/8 真值、Phase 2: 7/7 SC、Phase 3: 5/5 ROADMAP 判据)与 `*-UAT.md`(6/6、7/7、8 检查点)均 passed。

</details>

<details>
<summary>✅ v1.14 前端视觉与可访问性 (Phases 4-8) — SHIPPED 2026-09-26</summary>

- [x] **Phase 4: 设计契约、令牌层与契约校验** (3/3 plans) — completed 2026-09-20
  书面 UI-SPEC(含含义清单)+ 单一 `:root` 令牌块 + 全部字面量替换 + 四条契约校验命令
- [x] **Phase 4.1: Radix 颜色族重写** (4/4 plans) — completed 2026-09-20
  颜色族从手调 hex 换成 Radix Colors 12 步语义刻度(25 primitive / 47 `--color-*`),CHECK-02 清单重算为 43 对
- [x] **Phase 5: 排版与视觉层级** (4/4 plans) — completed 2026-09-21
  markdown 正文字号受控、不可逆动作权重、页面级层级、面板活动态、两处内联 SVG
- [x] **Phase 6: 布局稳健性** (4/4 plans) — completed 2026-09-22
  魔法数消除、窄窗口不破版、滚动容器收敛、24×24 命中区
- [x] **Phase 7: 交互状态与焦点样式** (3/3 plans) — completed 2026-09-23
  hover/active/disabled/transition + 全站 `:focus-visible`
- [x] **Phase 8: 可访问性语义与键盘** (3/3 plans) — completed 2026-09-24
  唯一触碰 `app.js`/`index.html` 的阶段:tabindex、划词焦点交接、Escape、dialog 语义、内联错误结构修复、五条修复回归复验

**Milestone scope:** 六支柱 UI 审计 13/24 的 13 项**显式延后项**——延后理由一致:修法本身就是设计决策,必须先定契约再落地。38 条需求全部交付;6/6 阶段在 `0b6283a` 复验 `passed`。
**回归面(本里程碑最高风险):** 5 条功能性 BLOCKER 的修复(`b9664e0`)全部依赖本里程碑重写的 CSS 且无自动化覆盖 —— 已由 Phase 8 的 REG-03 全量人工重跑收口。
**收口期发现的跨阶段回归:** Phase 6 的 L-4 滚动容器收敛静默杀掉了 AI 事件自动跟随(`app.js:253` 的 `scrollTop` 赋值按 CSS 规范成为 no-op),而当时的 `check-05 --item 9` 不但零覆盖该回归,还正面断言了它的前提。已修复(追加节点上 `scrollIntoView({ block: 'nearest' })`,不回退 L-4)并新增一条经变异证明会失败的门。
**验证记录:** `milestones/v1.14-phases/` 各阶段 `*-VERIFICATION.md` 与 `*-UAT.md`;里程碑审计 `milestones/v1.14-MILESTONE-AUDIT.md`(`status: passed`,`remediated: 2026-09-25`)。

</details>

<details>
<summary>✅ v1.15 视觉构图升级 (Phases 9-10) — SHIPPED 2026-09-28</summary>

- [x] **Phase 9: 卡片容器化与页面底色下沉** (3/3 plans) — completed 2026-09-26
  左栏 4 个面板与右栏文档区成为白底卡片;页面底色下沉至 gray-3,形成 gray-3 < gray-2 < 白 三级 elevation 刻度;受影响的对比度对重算并登记;五条 UI 门复跑无新增失败
- [x] **Phase 10: 表格重做与圆角刻度收敛** (4/4 plans) — completed 2026-09-27
  文档表格由「每格 1px 全边框」改为「表头浅底 + 仅横向分隔线」;圆角刻度收敛为 8 / 10 / 胶囊三档,删掉未并入刻度的 `--radius-lg: 28px`;两项均不引入新颜色值、不放宽阈值、不新增 `!important`

**Milestone scope:** 12 条需求(CARD 3 / VIS 2 / REG 2 / TABLE 2 / RADIUS 2 / REG-03)全部交付并验证。范围裁定两次均由用户逐项作出:Phase 9 先只做卡片化(「开一个 phase,先看看效果吧」),用户看过截图后裁定「表格重做, 圆角刻度收敛。做这两个」⇒ 另开 Phase 10;第三项候选(图标与空状态)**未点名,仍留 Out of Scope**。
**验证记录:** Phase 9 `passed` 24/24(收口前经用户裁定追加一次强度微调 quick `260926-vaf`,已按「以 HEAD 内容重新验证」处置,非刷新指纹);Phase 10 `passed` 62/62。里程碑审计 `milestones/v1.15-MILESTONE-AUDIT.md`(`status: tech_debt` —— 12/12 需求满足、无 critical blocker,14 项已登记 tech debt 待用户裁定)。
**产品面:** 仅 `frontend/style.css`(+258)与 `scripts/`(新 `check-09` / `check-10` / `probe-card-border-token.py`,`check-05` +10);后端与 `app.js` / `index.html` 逐字节未改。
**v1.16 与本里程碑的关系:** v1.16 **反转** Phase 9 的卡片语言(D-9-1 / D-9-2 / D-9-3 是一次已 shipped 的用户裁定,用户 2026-09-28 看过成品后逐项裁定反转);本里程碑审计登记的 **G1**(`#latest-check` 表头 band 消失)由用户裁定「连带」纳入 v1.16 的 `G1-01`。Phase 9 引入的 **sticky 余量为零**由 v1.16 的 `REG-03` 处置。

</details>

### 🚧 v1.16 界面去卡片化 —— 连续面与发丝分隔线 (In Progress)

**Milestone Goal:** 消除分块割裂感。把 v1.15 Phase 9 引入的「独立白卡片 + 12px 灰缝 + 768px 居中侧沟」整体反转为 ChatGPT 式的「**连续白面 + 1px 发丝分隔线**」,并连带修掉 v1.15 审计登记的 G1(自检报告表头 band 消失)。

**本里程碑的性质:反转,不是新增。** 反转对象是**一次已 shipped 的用户裁定**(D-9-1 / D-9-2 / D-9-3)。用户 2026-09-28 看过成品后逐字裁定:「分块太割裂了,完全没有联动性…chatgpt 的界面就是一根细的衬线来分割不同的分区,我们的确实很大的一块」。因此**门禁同步是承重需求而非附属工作**:`scripts/check-09-idi09-validation.py` 的 c1 / c2 / c3 / c4 逐条断言卡片语言,**反转后必然全红 —— 那正是门在正确工作的证据**。判据必须**改写为断言新契约**,不得删除、不得降级为恒真、不得只断言「规则被写下了」(仓库方法论:一条不能失败的门比没有门更糟),而唯一能证明改写后的判据真的会失败的手段是**变异测试**。

**范围裁定(用户,2026-09-28,逐项):** 视觉方向 = **全站去卡片**;落地方式 = 走 GSD 新阶段;范围 = 去卡片化 **连带 G1**(`#latest-check` 表头 band 消失,从 v1.15 审计的候选池移入本里程碑);跳过领域研究。

**明令排除(Out of Scope,不得为其预建阶段):** G2(`--radix-gray-1` 零消费 + 通用围栏消费断言 —— 用户只裁定「连带 G1」,**G2 未点名**)、`999.2`(Phase 7 三条既有 affordance 缺陷)、`A11Y-V2-01/02` / `FLOW-V2-01/02` / `TOKEN-V2-01`(暗色模式)、Nyquist 缺口(`idi-04` / `idi-06` / `idi-09` / `idi-10` 无 `VALIDATION.md`)、图标与空状态(用户 2026-09-27 与 2026-09-28 两次均未点名)。

**硬约束(每个阶段都适用):** `scripts/check-01-token-conformance.sh`(令牌块外零裸 `#hex`、零 tier-1 原语引用;primitive 名私有于围栏)、`scripts/check-02-contrast.py`(围栏内 PAIR 清单)、`scripts/check-03-hidden-uniqueness.sh`(`^\.hidden {` 恒为 1)、`scripts/check-04-important-count.sh`(`!important` **声明**数恒为 1);**复用现有 `--color-*` 语义令牌,不新增 tier-1 原语、不新增颜色值**;**追加,不重排**(至少一对等特异性规则由源码顺序决定;需要改写既有声明时就地改写,不搬迁);不得新增 `!important`、不得令牌化 `display`、不得引入 `@layer` / `@property` / `var(--x, #fallback)`;零新增运行时依赖、零构建步骤(DESIGN.md D-06);**每个 `style.css` 计划必须带至少一项运行时验证**(真实浏览器的 computed style 读数 —— `grep -c 'var(--'` 对渲染结果零证明力)。

**回归面(本里程碑最高风险):** 五条浏览器门大量断言绑死具体 DOM 与 computed style(焦点环 2px 与其解析后的 `--color-focus`、sticky 表头、badge 流内机制、滚动容器收敛、命中区 24×24、窄窗口不破版、表格令牌接线),而本里程碑改的正是容器绘制面 ⇒ 每次改动必须复跑。**门环境事实(省得重探):** `check-05` 走 `.venv/bin/python` 且**必须** `--browser bundled`(该机 `channel="chrome"` + headless 会挂死);`check-05` 全量 exit=2 是 item 5 两条 `--ai-smoke` 腿按设计 BLOCKED,不是回归;pytest 基线 **219 passed / 6 skipped**,必须用项目 `.venv`(环境 `python3` 是 miniconda,会让 4 个 `ai_caller` 测试假失败)。**`check-05 --item 8` 的 sticky 断言余量实测恰 `1.000px`**(由 Phase 9 给 `#doc-panel` 加的 1px 上边框引入)⇒ 任何 1px 级改动都会顶破,由 `REG-03` 指名处置。

- [x] **Phase 11: 去卡片化与发丝分隔线** - 左栏 4 个 section 与 `#doc-panel` 移除边框/阴影/圆角、面板与页面统一为同一档底色、12px 灰缝与 768px 居中侧沟归零;分区改由 1px 发丝线承担(主区↔文档区竖线跨满高、左栏面板间横线);同步改写 `check-09` 的 c1..c4 并以变异证明其会失败、重新归属 `check-02` 的卡片地面配对、复测 `check-05 --item 8` 的 sticky 余量 (completed 2026-09-29)
- [ ] **Phase 12: G1 表头 band 与里程碑收口** - `#latest-check` 内表头读作独立 band(宿主绘制面与表头底色不再同令牌相撞,以运行时读数 + 截图取证);五条浏览器门 + 四个静态门 + pytest 基线复跑零新增失败;连带作废的 `passed` 报告按既有口径逐份处置;5 张 1440×900 整窗截图

## Phase Details

### Phase 11: 去卡片化与发丝分隔线

**Goal**: 把 v1.15 Phase 9 落地的卡片语言**整体反转** —— 左栏 4 个 section(会话流 / 本轮批注流 / 自检报告 / AI 工作面板)与右栏 `#doc-panel` 不再绘制容器边界(`border` / `box-shadow` / `border-radius` 三者从这 5 个容器上移除),面板底色与页面底色**统一为同一档**(不再有「白卡片浮在灰页面之上」的 elevation 差),12px 灰缝与 768px 居中侧沟**归零**;分区改由 **1px 发丝线**承担 —— 主区↔文档区一条竖线**跨满面板可视高度**,左栏面板之间 1px 横线。界面读作**一张连续的平面**。**同步(承重):** `check-09` 的 c1/c2/c3/c4 逐条断言卡片语言、反转后必红,须改写为断言新契约并以变异测试证明会失败;`check-02` 中归属 `--color-surface-card` 的 2 条 PAIR 按元素实际绘制面重新归属并重算;`check-05 --item 8` 的 sticky 余量在 `#doc-panel` 边界改动后复测并登记成因。
**Depends on**: Nothing(v1.15 的 Phase 9 / 10 已 shipped 并归档于 2026-09-28;本阶段直接改写 Phase 9 落地的卡片规则所在的 `frontend/style.css`)
**Requirements**: SURF-01, SURF-02, SURF-03, DIV-01, DIV-02, DIV-03, REG-01, REG-02, REG-03

**Rationale**: 本阶段是**反转,不是新增** —— 底色关系、密度、圆角与卡片语言四者都是 Phase 9 / 10 已签核的落地形态,用户 2026-09-28 逐项裁定反转,**本阶段不重开该决策**。难点**不在选色,而在门禁同步**:`check-09` 的 c1/c2/c3/c4 是 Phase 9 自己建的运行时门,它们断言的正是本阶段要移除的那套语言。三条「同一次改动、两副面孔」的承重义务拆开会造出「改了值但没人验」的中间态(与 v1.15 把 REG-01/REG-02 与 CARD/VIS 同阶段交付的裁定同型),而且这三条门在本阶段之后**都会绿着说谎**:

- `check-09` c1..c4 → `REG-01`:门断言的正是本次改动;
- `check-02` 的 2 条卡片地面 PAIR(`style.css:632` / `:643`)→ `REG-02`:卡片地面**因本次改动而消失**,配对若不重新归属就只是数字仍然达标、而它描述的那块面已不存在;
- `check-05 --item 8` 的 sticky 余量 → `REG-03`:余量恰 `1.000px`,而它的成因就是 Phase 9 给 `#doc-panel` 加的那 1px 上边框 —— 本阶段移除该边框正是该读数变化的唯一原因。

SURF 与 DIV **必须同阶段落地**:只去卡片不留线,等于把 4 个面板之间的 12px 灰缝一并抹掉、分区彻底消失 —— 那是比任一终点都差的中间态。且 `check-09` 的 c4 同时断言「间距几何」与「面板内边距」,一次改写覆盖 SURF-03 与 DIV-02 两侧的契约。

**Deliverables**:

1. **连续面(SURF-01 / SURF-02)** —— `#main-pane > section`(`style.css:751-758`)与 `#doc-panel`(`:768-776`)按新契约**就地改写**那四条声明(`background` / `border` / `border-radius` / `box-shadow`),**不是追加覆盖** —— 留下已死的声明会让注释与代码互相矛盾(Phase 9 对 `#doc-panel` 的 `border-left`、Phase 10 对表格 `border` 用的是同一手法)。5 个容器的计算 `box-shadow` 为 `none`、计算 `border-radius` 为 `0px`。**交互控件不受影响**:按钮 / 输入框 / `select` / `#check-switcher` / `.overlay-card` 仍保留各自的圆角与边界。
2. **底色统一(SURF-02)** —— 面板底色与页面底色**同一档**:`--color-surface-page`(`:139`,现值 `--radix-gray-3`)与面板所取的地面统一,页面不再有可辨的灰色底。**`#doc-panel-header`(`:813-818`)的 sticky 底色是承重声明,不是装饰**(不加背景则滚动正文从标题行底下穿过)—— 它必须**跟随统一后的地面改归属,不得删除**。
3. **灰缝与侧沟归零(SURF-03)** —— `#main-pane` 的 `gap`(`:725`,现值 `var(--space-3)` = 12px)归零;`#main-pane > section` 的 `max-width: 768px`(`:753`)与 `#main-pane` 的 `align-items: center`(`:727`)一并处置 —— 侧沟的机械成因就是这两条(内容列被居中,左右露出页面底色)。面板区与文档区**直接相邻**。
4. **发丝分隔线(DIV-01 / DIV-02 / DIV-03)** —— 主区↔文档区 **1px 竖线、跨满面板可视高度**(不是只画在内容旁的一段);左栏面板之间 **1px 横线**,替代原 12px 灰缝。线取**既有语义令牌**(候选 `--color-border-subtle`,gray-6 —— 它已是 `.event-list` / `.annotation-item` / `.badge-answered` / `#latest-check` 四处的边界色),**零新增颜色值、零新增 tier-1 primitive**;线宽 1px。竖线的实现须**零位移、零新增 DOM 元素**(优先 `border-left` 之类的盒内手段)。
5. **门禁同步(承重,REG-01 / REG-02 / REG-03)** —— 判据见 Success Criteria 4 / 5 与 Gates。三条各自带「改写/重新归属」与「变异/重算取证」两半,缺一不可。
6. **被本次反转孤立的令牌** —— `--color-surface-card`(`:334`)与 `--shadow-card`(`:335`)在本阶段之后**消费者归零**(前者原 3 处消费者 `:754` / `:774` / `:816`,后者 2 处 `:757` / `:776`)。围栏自己的抬头(`:42-44`)与 Hard Rule 5 / D-04 逐字要求「只声明被消费的令牌」—— Phase 10 正是援引这条规则删掉了 `--radius-lg`,并只给它加了一条**专用**的残留断言。故本阶段按同一条规则处置这两个令牌(删除,或在计划里显式论证保留的理由)。**⚠ 这不是 G2:** G2 是「补一条**通用的**围栏消费断言」,已由用户明确排除在 v1.16 范围外;本阶段只处置**本次改动自己孤立掉的**两个令牌,不得顺手补通用断言。

**Success Criteria** (what must be TRUE):

1. 左栏 4 个 section 与 `#doc-panel` 在浏览器里**不再绘制容器边界**:五者的计算 `box-shadow` 为 `none`、计算 `border-radius` 为 `0px`、除发丝线所在的那一条边外计算 `border-*-width` 为 `0px`;界面读作**一张连续的平面**,不再是"一块块浮起的卡片"。**交互控件仍保留各自的圆角与边界** —— 该对照组须在同一份运行时读数里给出(否则"移除边界"可能是把整站边界一起抹掉)。(SURF-01)
2. **面板底色与页面底色读数相同**,屏幕上不再有可辨的灰色底与 elevation 差;`--color-surface`(gray-2,控件内陷面)仍是唯一比统一面更暗的一档,控件与 `#latest-check` 仍读作内陷 —— 即「统一」是把**卡片档并回页面档**,不是把所有层次压平。(SURF-02)
3. **灰缝与侧沟归零、分区由线承担**:`#main-pane` 的计算 `gap` 为 `0px`,面板之间不再透出页面底色,主区内容列不再露出左右灰沟,面板区与文档区**直接相邻**;主区↔文档区一条 1px 竖线的计算高度**等于面板可视高度**(跨满,不是一段),左栏面板之间 1px 横线;线宽 1px、取既有语义令牌,`check-01` PASS(令牌块外零裸 `#hex`、零 tier-1 原语引用)。(SURF-03 + DIV-01 / DIV-02 / DIV-03)
4. **`check-09` 的 c1 / c2 / c3 / c4 已改写为断言新契约**,**零条断言被删除、零条降级为恒真**(不得只断言「规则被写下了」),并**以变异测试证明改写后的四条判据会真的失败** —— 逐条给出「变异 → FAIL」的真实读数(候选变异:给 `#main-pane > section` 重新加回 `border` / `box-shadow` ⇒ c1 必红;给 `#doc-panel` 加回四边边界或删掉 `overflow-y: auto` ⇒ c2 必红;把统一面改回 `--color-surface` 使内陷档塌掉 ⇒ c3 必红;把 `gap` 改回 12px 或删掉发丝线规则 ⇒ c4 必红)。变异在已提交的树上做、定向 `git checkout -- frontend/style.css` 还原(**不用 `git stash`** —— 它跨工作树共享,本项目明令禁止),还原后逐字节相同。c5 的滚动契约在改动后复跑并确认仍成立。**`check-05 --item 8` 的 sticky 断言在 `#doc-panel` 边界改动后复测**,余量读数与成因已登记(不成立时按「事实是否被改变」分诊并同步更新判据、说明改了什么)。(REG-01 + REG-03)
5. **`check-02` 全部对比度对达标,且地面归属如实**:归属 `--color-surface-card` 的 2 条 PAIR(`:632` `--color-marker-active` TEXT / `:643` `--color-border-strong` NON-TEXT)已按元素**实际绘制面**重新归属并重算 —— **非刷新旧值、非调色、非放宽阈值**;因统一面换值而受影响的页面地面 PAIR(`:561` / `:571` / `:576` / `:620` / `:659` / `:689` 六条)逐条以 HEAD 内容重算并登记;四个静态门(`check-01`…`check-04`)全 PASS,`ORDER` 断言不退化,`TEXT_MIN` / `NON_TEXT_MIN` 与改动前逐字节相同。(REG-02)

**Avoids** (Pitfalls):

- **把门改小以让结论成立** —— 反转后 `check-09` c1..c4 必红,那是门在正确工作。**删除断言 / 放宽阈值 / 降级为恒真 / 只断言「规则被写下了」** 都是本仓库明令禁止的「门绿但没在看」。正解只有一条:把判据改写为断言**新契约**,并用变异测试证明它真的会失败。
- **只在静态 grep 上验收** —— 每个 `style.css` 计划必须带至少一项运行时验证(真实浏览器的 computed style 读数);`grep -c 'var(--'` 对渲染结果零证明力。
- **重排规则** —— 至少一对等特异性规则由源码顺序决定;重排即渲染变更,而源码 diff 看起来完全无辜。只追加,需要改写既有声明时就地改写、不搬迁。
- **计数门的算术陷阱** —— `check-04` 数的是 `!important;` **声明**数(恒为 1),不是命中行数;解释性注释的散文会把 `grep -c` 顶高(本项目已因此红过三次)。`check-03` 数 `^\.hidden {` 恒为 1。围栏内注释不得出现「令牌名 + 冒号」(`check-02` 的 `DECL_RE` 扫围栏全文含注释);围栏外的机械判据是子串计数,连论证性散文都会把它顶高。
- **删掉 `#doc-panel` 的 `overflow-y: auto`** —— 它是右列的滚动者,L-1 的 sticky 表头依赖它仍是**最近的可滚祖先**;删它会打破 L-1。**保留它的理由只有这一条。** 原文此处曾写「删它会同时打破 L-1 与 `check-05 --item 9` 的滚动者普查(期望值是 4 不是 3)」—— **该说法有误,已纠正**:磁盘实测 `scripts/check-05-ui-uat.py:2436` 的 `PANEL_SCROLLERS` 是 **3** 个成员(`#chat-messages` / `#latest-check` / `#main-pane`),普查遍历的是 `#main-pane` **及其后代**,而 `#doc-panel` 是 `#main-pane` 的**兄弟**(两者同为 `#app` 的子元素)⇒ 它根本不在该普查范围内,删它的 `overflow-y` **不会**打破 item 9。该错误已由 `idi-11-01` 与 `idi-11-05` 两份计划各自核盘并显式禁止抄录。
- **删掉 `#doc-panel-header` 的背景** —— 它是 sticky 的承重声明,不是装饰(`.panel-header` 规则体内没有 `background`,不加则滚动正文从标题行底下穿过去)。本阶段是**改它的归属**,不是删它。
- **把发丝线做成参与布局的东西** —— 竖线若用 `margin` 或额外元素撑高,会移动既有几何并可能打在 `check-05 --item 9` 的 L-5 clearance 普查与 `--item 8` 的 badge × banner 几何上;`#main-pane > section` 上加一条 `border-top` 会给每个面板加 1px 盒高。**这类 1px 级几何变化必须由运行时读数确认,不能靠推断**(Phase 10 就出现过计划写「零布局改动」而实测矮了 3px)。
- **把统一面做成「压平所有层次」** —— SURF-02 是把卡片档并回页面档,不是把 `--color-surface`(内陷面)也一并抹掉;内陷面塌掉会让 c3 的改写判据失去对象,也会让控件与 `#latest-check` 失去边界。
- **以为改 `style.css` 只作废一份指纹** —— 真实形状须在磁盘上逐份读 `covered_files` 实测,判据锚 frontmatter 的 `covered_files` **逐行匹配**(**不是**全文 grep,全文 grep 会把只在正文提及的报告算进来),并**额外测「路径是否还在盘上」**(归档后的报告路径不可解析 ⇒ fail-closed stale,属 2026-09-14 登记的已知限制)。**本阶段的连带面与 v1.15 不同**:改写 `scripts/check-09-idi09-validation.py` 会把该脚本的覆盖者拖进名单,`scripts/check-05-ui-uat.py` 若被改动同理(Phase 10 曾以「不得改 `check-05`」避免把 `idi-08` 拖进来)—— 须在计划里**先实测再处置**,不得凭记忆断言份数。
- **顺手做未裁定项** —— G2(`--radix-gray-1` 零消费 + 通用围栏消费断言)、`999.2`、`A11Y-V2` / `FLOW-V2` / `TOKEN-V2`、Nyquist 缺口、图标与空状态**全部在 Out of Scope**;本阶段只处置本次反转自己孤立掉的令牌。
- **以为后端 / `app.js` 会需要改动** —— 预期本阶段是**纯 CSS + 门脚本**改动,`frontend/app.js` 与 `frontend/index.html` 逐字节不改、后端零改动(v1.15 两个阶段都是这样,且两处都以此为证据)。**偏离这个预期是一个信号** —— 例如「必须加 DOM 元素才能画出跨满高的竖线」说明选的实现方式错了(应改用零 DOM 的盒内手段),须先停下来判因,不要顺着改下去。

**Gates**: `scripts/check-01-token-conformance.sh` PASS(令牌块外零裸 `#hex`、零 tier-1 原语引用);`scripts/check-02-contrast.py` PASS(2 条卡片地面 PAIR 已重新归属并重算、六条页面地面 PAIR 已重算、`ORDER` 不退化、阈值与 HEAD 逐字节相同);`scripts/check-03-hidden-uniqueness.sh`(`^\.hidden {` = 1);`scripts/check-04-important-count.sh`(`!important` **声明**数 = 1);`scripts/check-09-idi09-validation.py` 改写后 c1..c5 全 PASS **且四条改写判据各有一条变异 FAIL 的读数**;`scripts/check-05-ui-uat.py --item 8` 复跑(sticky 余量读数已登记);五条浏览器门复跑无新增失败(`check-05` 走 `.venv/bin/python` + `--browser bundled`;全量 exit=2 是 item 5 两条 `--ai-smoke` 腿按设计 BLOCKED,不是回归);`.venv/bin/python -m pytest backend/tests -q --tb=short` 基线不降(**219 passed / 6 skipped** —— 必须用项目 `.venv`);`node --check frontend/app.js`;`git status --porcelain frontend/` 仅预期文件、`frontend/vendor/` 仍只有 `marked.min.js`。
**Plans**: 5/5 plans executed (4 executed + 1 gap-closure pending)

Plans:
**Wave 1**

- [x] idi-11-01-PLAN.md — 反转本体(纯 CSS):统一面 `--color-surface-page` 换值为 `var(--white)` + 左栏 4 个 `section` 与 `#doc-panel` 就地去掉 `border` / `border-radius` / `box-shadow` + `#main-pane` 灰缝归零 + 两条 1px 发丝线(竖线 = `#doc-panel` 的 `border-left`、横线 = `#main-pane > section + section`)+ 四段承重注释改写;三份真实浏览器运行时读数取证

**Wave 2** *(blocked on Wave 1 completion)*

- [x] idi-11-02-PLAN.md — 处置被反转孤立的两个令牌(`--color-surface-card` / `--shadow-card` 删除)+ 围栏内 6 个注释区改写为不写令牌名的说法 + `check-02` 的 2 条卡片地面 PAIR 重新归属到统一面、6 条页面地面 PAIR 以 HEAD 内容重算并登记(REG-02)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] idi-11-03-PLAN.md — `check-09` 承重改写:c1..c4 换为断言新契约(连续面 + 统一面 + 灰缝归零 + 两条发丝线,判据走真实浏览器 computed style)+ 新增 `fence_text()` 与两条专用残留断言 + 交互控件对照组与活动标记的正面断言;**六条变异测试**逐条给出「变异 → FAIL」真实读数并证明还原后逐字节相同(REG-01)

**Wave 4** *(blocked on Wave 3 completion)*

- [x] idi-11-04-PLAN.md — 门禁收口:`check-05` 的 `.hint` 期望侧重登记到统一面令牌(断言形式一字未变,消除「期望侧为 `None` → BLOCKED」的静默退化)+ `--item 8` 的 sticky 余量复测与成因登记(REG-03)+ 五条浏览器门 / 两探针 / 四静态门 / pytest 基线复跑并把原始输出落盘 `gate-logs/` + 连带指纹面逐份实测登记

**Wave 5** *(gap closure — blocked on Wave 4 completion)*

- [x] idi-11-05-PLAN.md — 收口独立验证报出的 1 个 BLOCKER 与 2 条 Warning:发丝线规则就地改写为「除 DOM 末个外都加下边线」(窗口边缘线缺陷,DIV-02 / D-11-10)+ 承重注释如实改写并登记机制前提 + `check-09` 的 c1/c4 断言换向与 c4 逐状态发丝线普查(5 个样本状态)+ c2 补 `#doc-panel` 底色断言 + 三条变异证明 + 围栏内三处现在时陈述改写 + 全门复跑落盘 `gate-logs/idi-11-05/`

**UI hint**: yes

### Phase 12: G1 表头 band 与里程碑收口

**Goal**: 修掉 v1.15 审计登记的 **G1** —— `#latest-check`(`style.css:1526-1534`)自身声明 `background: var(--color-surface)`(gray-2)**且自身是 `.markdown-body` 宿主**,而 `th`(`:1118`)用同一令牌绘制 ⇒ 自检报告里的表头是**灰底压灰底**、band 消失(不是假想:`backend/prompts.py:494-499` 要求每份自检报告都带这张表)。目标是让表头在 `#latest-check` 内**读作一条独立的 band**。**同时收口**:在全部 `style.css` 改动落定后复跑五条浏览器门 + 四个静态门 + pytest 基线,处置连带作废的 `passed` 报告,并产出 5 张 1440×900 整窗截图作为「分块割裂感已消除」的人眼取证。
**Depends on**: Phase 11(表头的**宿主绘制面**正是 Phase 11 改的那一面 —— 在 Phase 11 的统一面落定之前修 G1,等于把 band 修在一个马上要变的底上;`REG-04` 的「零新增失败」也必须在最后一次 `style.css` 改动之后跑才成立)
**Requirements**: G1-01, REG-04, VIS-01

**Rationale**: G1 是 v1.15 里程碑审计的 WARNING 级结构发现,用户 2026-09-28 裁定「连带 G1」纳入本里程碑,故它是**被点名的范围**,不是顺手清理。它与 Phase 11 的反转**机制独立**(不在同一区域、不共享规则)但**有依赖**(宿主绘制面在 Phase 11 变),故排在 Phase 11 之后并单独成阶段:反转是一次大而耦合的绘制模型改动,G1 是一次小而独立的定点修复,混在一阶段会让「反转需要按截图微调」时把 G1 一并卷进去。本阶段同时是里程碑的收口阶段 —— `REG-04` 的复跑与 `VIS-01` 的截图都只有落在**最终态**上才有意义。

**Deliverables**:

1. **G1 的 band 修复** —— 让 `#latest-check` 内的表头底色与其**宿主绘制面**不再同令牌相撞。**两条候选路线须在计划里显式择一并说明涟漪面**(这是设计决策,不是机械替换):
   - (a) **移宿主**:`#latest-check` 的 `background`(`:1532`)改归另一档 —— 波及面限于这一条规则;
   - (b) **移表头**:`th` 的 `background`(`:1118`)改归另一档 —— 但 `th` 是**全局**规则(`.markdown-body` 的 9 个宿主里 4 个覆盖,`IN-06`),改它同时改变文档区表格的表头读感,并可能打破 `check-10` 的 `t1` / `t2`(它们断言 `th` 画的是 `--color-surface`)。
   **同形先例**:仓库上一阶段刚为 `#doc-panel-header`(`:800-812`)处置过同一族问题 —— 那里的机制是**让元素的底色与其宿主同值**、使 sticky 表头不显形;G1 要的是**相反的结果**(band 必须显形),可复用的是「重新归属绘制面」这一手法,不是它的方向。**不得改 `--color-surface` 的值**:它被多处消费(`:1523` `#check-switcher` / `:1532` `#latest-check` / `:1118` `th` / 三个 `select` / `.overlay-card`),且是既有 PAIR(`--color-text ON --color-surface` 15.48)的地面 —— 改值会连锁影响它的全部配对,与 v1.15 记下的「调色」错向同型。
2. **表头新绘制面的对比度登记** —— 以 `check-02` **实际输出**证实:新地面上表头文字(`--color-text`,继承自 `.markdown-body`)的配对已登记,或已按元素实际绘制面重新归属;**零新增颜色值、零放宽阈值**;若 `check-10` 的 `t1` / `t2` 因路线 (b) 而不再成立,判据**同步改写而非删除**。
3. **整里程碑复跑(REG-04)** —— 磁盘上的浏览器门(`check-05` / `check-06` / `check-07` / `check-09` / `check-10`,外加两个探针 `probe-05` / `probe-07`)+ 四个静态门(`check-01`…`check-04`)+ pytest 基线(**219 passed / 6 skipped**)逐条复跑并落原始输出;因 `frontend/style.css` 变更而作废的 `passed` 报告按既有「可执行性分诊」口径逐份处置。**门清单以磁盘现状为准:** `scripts/` 实为 `check-01`…`check-07` + `check-09` + `check-10`,**没有 `check-08`**(规划期初稿曾误列,已由路线图子代理核盘纠正,`REQUIREMENTS.md` 的 REG-04 已同步修正)。
4. **截图取证(VIS-01)** —— 5 张 1440×900 整窗截图(p1 / p12 / p3 / checking / archive),**复用既有 `--screenshot` 路径**(`scripts/check-09-idi09-validation.py --screenshot <DIR>` 与 `scripts/check-10-idi10-validation.py --screenshot <DIR>` 已按 `scripts/ui-states/` 的 5 个样本迭代并写出 `<state>.png`),**不新建 harness**。

**Success Criteria** (what must be TRUE):

1. **`#latest-check` 内的表头读作一条独立的 band**:表头底色与其宿主绘制面**不再同令牌相撞** —— 以运行时读数(两者的计算底色不同)与**人眼截图**共同取证,**不是**只断言「`th` 画了某个令牌」(那正是 `check-10` 的 58/58 PASS 与 G1 可以共存的原因)。(G1-01)
2. 表头文字在其**新绘制面**上的对比度已登记且达标(`check-02` PASS,零新增颜色值、零放宽阈值);文档区表格的表头读感若因本阶段而改变,须在 SUMMARY 里显式说明(路线 (b) 的涟漪面)。(G1-01)
3. 浏览器门 + 四个静态门 + pytest 基线**复跑零新增失败**;`check-05` 全量 exit=2 仍只因 item 5 两条 `--ai-smoke` 腿按设计 BLOCKED;`check-09` 的 c1..c5 与 Phase 11 改写后的契约一致。(REG-04)
4. **连带指纹已按既有口径逐份处置**:判据锚报告 frontmatter 的 `covered_files` **逐行匹配**(不是全文 grep)并**额外测路径是否仍在盘**;受影响且在盘的报告以 HEAD 内容**重新验证**而非刷新指纹(内容确实变了,刷新等于断言「自验证以来什么都没变」)。(REG-04)
5. **5 张 1440×900 整窗截图落盘**(p1 / p12 / p3 / checking / archive),作为「分块割裂感已消除」的人眼取证 —— 与 v1.15 同规格、同路径。(VIS-01)

**Avoids** (Pitfalls):

- **把 G1 修成「门绿但没在看」** —— `check-10` 的 `t1` / `t2` 回答的是「`th` 是否画了 `--color-surface`」(是),从不回答「表头是否读作独立 band」;它们 58/58 PASS 与 G1 完全相容。本条的判据必须是**视觉契约**(两条计算底色不同 + 截图),不是令牌接线。
- **只改一侧却不同步另一侧的门** —— 若路线 (b) 改了 `th` 的令牌,`check-10` 的 `t1` / `t2` 会红:那是门在正确工作,须**改写判据为断言新契约**,不得删除、不得降级为恒真。
- **在 Phase 11 之前修 G1** —— 宿主绘制面即将变化,先修等于把 band 修在一个马上要变的底上,并会让 `REG-04` 的复跑落在最后一次 `style.css` 改动之前。
- **为修 band 去动 `--color-surface` 的值** —— 它被 6 处以上消费且是既有 PAIR 的地面;改值会连锁影响它的**全部**配对。
- **把截图当成"跑一下就好"的副产品** —— `VIS-01` 是**人眼取证**,是「分块割裂感已消除」这条主张唯一的屏幕级证据;截图必须是最终态、1440×900、5 个样本齐全,并复现既有 `--screenshot` 路径而不是新建 harness。
- **以为改 `style.css` 只作废一份指纹 —— 或者以为作废十份** —— 两个方向都错;判据锚 frontmatter 的 `covered_files` 逐行匹配 + 路径是否在盘,并在计划里先实测再处置。
- **采信 `state.*` 写入动词的输出** —— 该组动词在本仓库已复现 15 次不可信(改错值 / 改分母 / 删字段 / 假报成功 + 零写入 / 部分成功 / 格式副作用),`update-progress` **不可作为修正手段**(它会用坏值重算)。判据一律取 ROADMAP 的 `## Milestones` + `## Progress`,且**核盘必须放在收口序列的最后一个动词之后**。
- **顺手做未裁定项** —— G2、`999.2`、`A11Y-V2` / `FLOW-V2` / `TOKEN-V2`、Nyquist 缺口、图标与空状态全部在 Out of Scope。

**Gates**: `scripts/check-01-token-conformance.sh` PASS;`scripts/check-02-contrast.py` PASS(表头新绘制面已登记,零阈值改动);`scripts/check-03-hidden-uniqueness.sh`(`^\.hidden {` = 1);`scripts/check-04-important-count.sh`(`!important` 声明 = 1);`scripts/check-05-ui-uat.py`(全量,`.venv/bin/python` + `--browser bundled`)/ `check-06` / `check-07` / `check-09` / `check-10` / `probe-05` / `probe-07` 复跑无新增失败;`.venv/bin/python -m pytest backend/tests -q --tb=short` 基线不降(219 passed / 6 skipped);`node --check frontend/app.js`;5 张 `<state>.png` 在盘(1440×900);连带指纹逐份处置的记录。
**Plans**: 3 plans

Plans:
**Wave 1**

- [ ] idi-12-01-PLAN.md — G1 定点修复(fixture 补 `## 问题分级` 表含 P0/P1 + `#latest-check` 宿主绘制面就地改归统一面白 + 围栏 `:129-130` 承重注释就地改写)+ `check-09` 新增运行时项 `c6`(「两者不同」与「宿主 == 白」两侧钉死 + fixture 模式不变量)+ 两条变异证明(M1 改回内陷面 / M2 改 gray-3 证明两侧钉死不冗余)

**Wave 2** *(blocked on Wave 1 completion)*

- [ ] idi-12-02-PLAN.md — `check-09` 新增专用参数 `--g1-snapshot DIR`(照 `check-10` 的 `--radius-snapshot` 先例)+ 产出 5 张 1440×900 整窗截图(p1 / p12 / p3 / checking / archive)与 1 张 `#latest-check` 元素级局部特写(独立子目录,不动「恰含 5 个 PNG」断言)(VIS-01)

**Wave 3** *(blocked on Wave 2 completion)*

- [ ] idi-12-03-PLAN.md — 整里程碑复跑(五条浏览器门 + 两探针 + 四静态门 + pytest 基线)原始输出与退出码逐门落盘 `gate-logs/idi-12-03/` + 连带指纹面逐份实测处置(11 份归档登记为已知限制、1 份在盘报告以 HEAD 内容重新验证)(REG-04)

**UI hint**: yes

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. 行走骨架 | v1.13 | 4/4 | Complete | 2026-09-09 |
| 2. 轮次收敛循环 | v1.13 | 4/4 | Complete | 2026-09-10 |
| 3. 授权、自检与终点 | v1.13 | 5/5 | Complete | 2026-09-13 |
| 4. 设计契约、令牌层与契约校验 | v1.14 | 3/3 | Complete | 2026-09-20 |
| 4.1. Radix 颜色族重写 | v1.14 | 4/4 | Complete | 2026-09-20 |
| 5. 排版与视觉层级 | v1.14 | 4/4 | Complete | 2026-09-21 |
| 6. 布局稳健性 | v1.14 | 4/4 | Complete | 2026-09-22 |
| 7. 交互状态与焦点样式 | v1.14 | 3/3 | Complete | 2026-09-23 |
| 8. 可访问性语义与键盘 | v1.14 | 3/3 | Complete | 2026-09-24 |
| 9. 卡片容器化与页面底色下沉 | v1.15 | 3/3 | Complete | 2026-09-26 |
| 10. 表格重做与圆角刻度收敛 | v1.15 | 4/4 | Complete | 2026-09-27 |
| 11. 去卡片化与发丝分隔线 | v1.16 | 5/5 | Complete    | 2026-09-29 |
| 12. G1 表头 band 与里程碑收口 | v1.16 | TBD | Not started | - |

**三个里程碑共 11 个阶段全部收口。** v1.15(视觉构图升级)已 shipped 并归档于 2026-09-28 —— Phase 9 交付卡片容器化与页面底色下沉(7 条需求 CARD 3 / VIS 2 / REG 2),Phase 10 交付表格重做与圆角刻度收敛(5 条需求 TABLE 2 / RADIUS 2 / REG-03);12/12 需求满足,里程碑审计 `status: tech_debt`(无 critical blocker,14 项 tech debt 已登记待裁定)。

**v1.16 已规划(2026-09-28),2 个阶段、12 条需求 100% 映射:** Phase 11 承载反转本体与其**三条门禁同步义务**(`REG-01` 改写 `check-09` 的 c1..c4 并以变异证明其会失败、`REG-02` 重新归属 `check-02` 的卡片地面配对、`REG-03` 复测 `check-05 --item 8` 的 sticky 余量)—— 三条与反转是同一次改动、两副面孔,拆开会造出「改了面但没人验」的中间态;Phase 12 承载 **G1**(用户裁定「连带」纳入)与**里程碑收口**(`REG-04` 全量复跑 + `VIS-01` 5 张截图),`REG-04` 必须在最后一次 `style.css` 改动之后跑,故归收口阶段。**`REG-01` 归 Phase 11,`REG-04` 归 Phase 12** —— 这是本路线图对「哪一阶段拥有哪条承重义务」的显式裁定。

**v1.15 审计登记的其余待裁定项仍未点名,留在 Out of Scope:** ①**G2** —— `--radix-gray-1` 已声明但零消费,围栏的「每个声明的令牌都被消费」性质现已不成立,而 `check-01` 结构上看不见(它只扫围栏外);②`check-10` 只钉令牌接线而非视觉契约(`WR-04` 残项同源);③`WR-03`/`WR-05` 两条加固残项;④`IN-05`/`IN-06` 两条字重与作用域残项;⑤Nyquist 缺口(`idi-09` / `idi-10` 无 `VALIDATION.md`,连同 v1.14 的 `idi-04` / `idi-06`)。另:`999.2`(Phase 7 三条既有 affordance 缺陷)仍在 Backlog,执行它会作废 `idi-07` 的 `passed` 指纹,须连带重新验证。

## Backlog

### Phase 999.1: Phase 4 残留的两条卫生项 (BACKLOG)

**Goal:** 清掉 Phase 4 收口后遗留、已由用户裁定为 Phase 4 范围外的两条小项。二者都是「已记录但无人认领」的真项,不是延期项。

1. **`.collapse-indicator` 的越轨字面量** —— `frontend/style.css:434` 为
   `.collapse-indicator { font-size: 20px; line-height: 1; }`,围栏外两个裸字面量,属 Phase 4 已令牌化的
   `--text-*` / `--lh-*` 族,且在 `04-UI-SPEC.md:841` 的封闭例外清单(L-1…L-5)之外。
   由 quick 任务 `260918-qrq`(`3684353`,2026-09-18 20:01)在 Phase 4 收口(`0c658aa`)之后引入;
   Phase 4 自己的提交区间干净。已在 `idi-04.1-UI-REVIEW.md` Pillar 4 记分(3/4,「undeclared 6th size」)。
   **HEAD 字号刻度为 12 / 14 / 16 / 18 / 24 —— `20px` 不在刻度上,故修法是排版决策而非机械替换**:
   加一档(改刻度,牵动 UI-SPEC 的「5 sizes」声明与 S-2 `--text-base = 14px` 的下游门)、重映射到 `18px`/`24px`
   (改已出货的 ▾/▸ 视觉),或加一条 L-6 例外(不改 `style.css`,但 `20px` 永久留在出货 chrome 里)。
   **注意:** 任何对 `frontend/style.css` 的编辑都会作废 `idi-04.1-radix` 的 `passed` 指纹(其 `covered_files`
   含该文件,digest 为原始字节 sha256),需连带复验 04.1。另见 Phase 5 Pitfall 7:`app.js:1550` 用 `textContent`
   赋值 `.collapse-indicator`,触碰它时不得引入内联 `<svg>`。
2. **`scripts/check-05-ui-uat.py:588` 的陈旧诊断文案** —— 仍打印「`--color-text-muted` … 变为 #8f8f8f,
   低于 AA 4.5:1」,而 HEAD 实为 `rgb(100,100,100)`、在 `--color-surface` 上 5.62 达标。周围断言正确,
   仅该 INFO 行陈旧。**改它同样会作废 04.1 的指纹**(该脚本也在 04.1 的 `covered_files` 里),
   故与第 1 项合并为同一批处理,一次性连带复验 04.1。

**裁定记录:** `idi-04-VERIFICATION.md` frontmatter `overrides:`(`accepted_by: Jack11111eee`,2026-09-20)与
其 Gaps Summary。未写进 Phase 5 的理由:Phase 5 的 Pitfall 7 把触碰 `.collapse-indicator` 的范围锁死为
两处 `content:` emoji,其 SC1 只点名四处 chrome 覆盖 —— 插入新交付物等于改写已签核的门。

> ✅ **已于 2026-09-25 关闭** —— quick `260925-iin` 同时处置了两项:第 1 项按用户裁定**加第 8 档字号**
> (`--text-lg-plus: 20px` + `--lh-none: 1`,字形渲染尺寸不变);第 2 项把陈旧 INFO 串更正为
> `rgb(100,100,100)` / 5.62:1 达标,未改任何断言。该 quick 同时新增一条经变异证明的自动跟随门
> (`check-05 --item 9`)与一条 `FOCUSABLE_SELECTOR` ↔ `:focus-visible` 对齐门(`check-07` 静态守卫 ⑤)。
> 连带复验:因 `frontend/style.css` 与 `scripts/check-05-ui-uat.py` 变更,`idi-04.1-radix` 与 `idi-07` 的
> 指纹作废 —— 六个阶段的指纹最终全部作废,并在收口前逐份以 HEAD 内容重新验证通过。见
> `.planning/milestones/v1.14-phases/idi-04-tokens-contract/idi-04-VERIFICATION.md` 与 `idi-05-*/idi-05-UI-SPEC.md`。

**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /gsd-review-backlog when ready)

### Phase 999.2: Phase 7 交互态契约暴露的三条既有 affordance 缺陷 (BACKLOG)

**Goal:** 清掉 `idi-07-UI-REVIEW.md`(2026-09-23,19/24)在建立「每个交互控件对 hover / active / disabled
有可辨反馈」这条契约时**暴露出来**的三条缺陷。三者都不是本阶段改动引入的(第 1、2 条是 Phase 7 之前就在的
affordance 谎报;第 3 条虽属 Phase 7 自己那份 PAIR 清单,但补它要动 `style.css` ⇒ 作废刚过的指纹),
但都只有在 Phase 7 的契约下才成为可判定的项。

1. **`#session-panel .panel-header` 宣称了一个不存在的点击** —— `frontend/style.css:665-674` 的基类
   `.panel-header` 规则体带 `cursor: pointer` + `user-select: none`,但只有 `#ai-panel-header` 与
   `#doc-panel-header` 有监听(`frontend/app.js:1561` / `1567`)。文件自己的惯例是对不可点的两个面板显式复位:
   `#annotations-panel .panel-header { cursor: default; }`(`style.css:1085`)与
   `#checks-panel .panel-header { cursor: default; }`(`style.css:1304`)。
   `#session-panel .panel-header`(`frontend/index.html:15`,该 header 无 id)两者皆无 ⇒ 鼠标移到「会话流」
   标题上会得到可点的指针。**修法:** 按既有惯例补一条 `#session-panel .panel-header { cursor: default; }`
   (一条声明,零重排)。
2. **`.annotation-answer summary` 没有任何交互态,也没有运行时覆盖** —— `style.css:1189` 定义了它;它带
   `cursor: pointer`、受 Phase 6 的 A11Y-07 门约束(24×24 命中区)、并被 Phase 7 的焦点环覆盖
   (`style.css:1513` 的七选择器含 `summary`),但**没有任何 `:hover` / `:active` 规则**,也不在过渡挂载规则里
   (`style.css:1675` 只覆盖 `button, input, select`)。更关键的是:**三个样本里没有任何 fixture 会渲染出
   `<summary>`**,故 item 10 的焦点环普查(每样本 28 个元素)从未见过它 —— 它的「已覆盖」是名义上的。
   **修法(两半,缺一不可):** 把 `summary` 并入朴素按钮的 hover 组;**并且**在 `p3` fixture 里加一个
   `summary`,或按 D-18 对 `a[href]` 的先例把该缺口**显式登记**。只做前半场会让「已覆盖」继续是名义的。
3. **焦点环的 PAIR 清单漏掉一处它真实渲染其上的底色** —— `style.css:498-507` 的清单列三处验证面
   (`--color-surface` / `--color-surface-page` / `--color-surface@0.75`),并**显式论证**为何排除
   `--color-surface-sunken`,却对 `--color-surface-warning-subtle`(amber-1)只字未提。而
   `.verdict-card`(`style.css:1341`,底色即该令牌)正是 item 10 在 `checking` 样本里实测
   `.verdict-note-input` 与两个 `.verdict-buttons button` 的宿主 —— 焦点环在这处底色上确实渲染。
   这是**与本文件自订纪律的直接冲突**:`style.css:435-437` 逐字写明「a token drawn as a UI boundary must
   have its own NON-TEXT pair on each ground it is drawn on」,而兄弟令牌 `--color-border-hover` 正是按这条
   纪律补上了这一处底色(`7b4ae18`,+3 ⇒ 53 对);`--color-focus` 同为 UI 边界却漏了同一处。
   实测环色在其上为 **5.77:1(达标)** ⇒ 这是**覆盖一致性缺陷,不是可辨性缺陷**。
   **修法:** 补一条 `/* PAIR --color-focus ON --color-surface-warning-subtle NON-TEXT */`,与 `7b4ae18` 对齐。

**指纹影响(执行前必读):** `frontend/style.css` 与 `scripts/check-05-ui-uat.py` **同时**在
`idi-07-VERIFICATION.md` 的 `covered_files` 里(digest `v1:sha256:5964d53c…`)。第 1、2、3 条的修法都要动
`frontend/style.css`,第 2 条的后半场还要动 `scripts/check-05-ui-uat.py` —— 故本项一旦执行,`idi-07` 的
`passed` 指纹即失效,须**连带重新验证 idi-07**(与 999.1 对 `idi-04.1-radix` 的关系同型)。
建议三条合并为同一批处理,一次性连带复验。

**裁定记录:** `idi-07-UI-REVIEW.md`(19/24;Pillar 2 Visuals 2/4、Pillar 3 Color 3/4、Pillar 6 Experience
Design 3/4 的扣分主因即此三条)与 `idi-07-VERIFICATION.md`。未写进 Phase 7 的理由:第 1、2 条是**既有**
affordance —— Phase 7 只改了声明式 CSS 的交互态与焦点环,`frontend/app.js` / `frontend/index.html` 逐字节未改,
按外科手术式改动纪律不在本阶段边界内;第 3 条虽属 Phase 7 自己的清单,但补它要动 `style.css` ⇒ 作废刚过的
指纹,而 UAT 已 1/1 通过、阶段收口在即,故由用户裁定转为 backlog 而非当场展开。
**用户裁定:`2026-09-23`(本 backlog 条目的建立即该裁定)。**

**Requirements:** TBD
**Plans:** 0 plans

Plans:

- [ ] TBD (promote with /gsd-review-backlog when ready)

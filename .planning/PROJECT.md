# 交互式讨论迭代系统(Interactive Discussion Iteration)

## What This Is

一个本地运行的 Web 工具,把"AI 项目开工前的讨论、细化、对齐"做成固定流程:想法进、无歧义的总设计文档出。单机、单人、本地运行,讨论文档以中文为主。**唯一权威设计文档为项目根 `DESIGN.md`(v1.13 收口版),本文件及 `.planning/` 全部为实施辅助视图,冲突时以 DESIGN.md 为准。**

## Core Value

未经用户明确授权,流程绝不进入"撰写总设计文档"步骤——总设计文档通过自检、界面提示「使命完成」即为终点(只读归档态)。

## Next Milestone Goals: v1.16 (未启动)

**状态:** v1.15 已 shipped 并归档(2026-09-28)。下一个里程碑尚未定义 —— 由 `/gsd-new-milestone` 走 提问 → 研究 → 需求 → 路线图 定义。

**候选池(本次未纳入,待用户裁定):**

- **v1.15 审计登记的待裁定项**(`milestones/v1.15-MILESTONE-AUDIT.md`,14 项):
  - **G1(WARNING)** —— `#latest-check` 自身声明 `background: var(--color-surface)` **且自身是 `.markdown-body` 宿主**(`style.css:1532`),而 Phase 10 用同一令牌画 `th`(`:1118`)⇒ 自检报告里的表头是**灰底压灰底**、band 消失。不是假想:`backend/prompts.py:494-499` 要求每份自检报告都带这张表。仓库上一阶段刚为 `#doc-panel-header` 修过**同形**问题(`style.css:802-803`),Phase 10 又为 `th` 造了一次。仅视觉层级破坏(文字在 gray-2 上 15.48:1,无 a11y 失败)。需要一次决策:去掉 `#latest-check` 自己的灰底 / 给 checks-panel 的表头换一档 / 显式接受那里无 band。
  - **G2(WARNING)** —— `frontend/style.css:48` 的 `--radix-gray-1: #fcfcfc` 已声明但**全仓库零消费**(Phase 9 把唯一消费者 `--color-surface-page` 改指 gray-3)。围栏自己的抬头(`style.css:42-44`)逐字写着「只声明被消费的令牌」—— Phase 10 正是援引这条规则删掉了 `--radius-lg`,却只给它加了一条**专用**的残留断言,没有一般化。`check-01` 结构上看不见它(它只扫围栏外)。⇒ 应删该 primitive 或重新消费,并补一条**通用的**围栏消费断言。
  - 其余:连带指纹「10 份覆盖 / 1 份可执行」的口径、`check-10` t1/t2 只钉令牌接线而非视觉契约、`WR-03/04/05` 三条加固残项、`IN-05`(`th` 仍渲染 UA 默认字重 700,在文件声明的三档 400/500/600 之外)、`IN-06`(表格语言只到 `.markdown-body`,9 个 markdown 宿主里 4 个覆盖)、`check-05` 一条陈旧 INFO、`check-05 --item 8` 的 sticky 断言余量为零、Nyquist 缺口(`idi-09` / `idi-10` 无 `VALIDATION.md`)。
- **`999.2`** —— Phase 7 交互态契约暴露的三条既有 affordance 缺陷(仍在 Backlog;执行它会作废 `idi-07` 的 `passed` 指纹,须连带重新验证)。
- **`A11Y-V2-01/02`**(焦点陷阱、其余非阻塞弹窗的 `role` / `aria-modal`)、**`FLOW-V2-01`**(替换两处 `window.prompt`)、**`TOKEN-V2-01`**(暗色模式)、**`FLOW-V2-02`**(`#probe-controls` 的移除或重定位)。
- **构图轴上的其余候选(用户 2026-09-27 未点名,仍留 Out of Scope):** 图标与空状态。

**硬约束(任何后续 phase 都适用):** 遵守 `scripts/check-01-token-conformance.sh`(令牌块外零裸 `#hex`、零 tier-1 原语引用)与 `check-02` 对比度门禁;复用现有 `--color-*` 语义令牌,**不新增 tier-1 原语**;零新增运行时依赖、零构建步骤(DESIGN.md D-06);`frontend/style.css` 的编辑纪律见下方 Constraints 末条。

## Current State

**v1.15 视觉构图升级 — ✅ SHIPPED 2026-09-28**(归档 2026-09-28)

把界面的**构图层次**补齐。v1.14 的设计纪律全部花在**正确性**(颜色 / 对比度 / 焦点环),**构图**(容器层次、视觉重量、组件变体)从未被任何阶段覆盖 —— 界面因此仍然"丑"。本里程碑按 shadcn/ui 的**配方**(不引入其依赖,见 Context 的可行性结论)逐层收敛。2 个阶段(9 / 10)、7 个计划、20 个任务,12 条需求全部交付。**零新增运行时依赖、零构建步骤**(DESIGN.md D-06 守住):两个阶段都是纯 `frontend/style.css` 改动,**后端与 `app.js` / `index.html` 逐字节未改**。

**界面首次拥有 elevation 层次:** 左栏 4 个面板与右栏文档区从「完全透明 / 比页面更暗的 gray-2」变为同族白卡片(白底 + 1px 既有容器边界 + 10px 既有圆角 + 零位移极轻阴影),页面底色从 gray-1(全场最亮)下沉到 gray-3,三档刻度 `gray-3 页面 < gray-2 内陷面 < 白卡片` 由真实浏览器读数证明严格递增 —— 这正是 shadcn 的 canvas / inset / raised 三档。

**第二次交付:** 文档区表格由「每格 1px 全边框的电子表格式网格」改为「gray-2 表头浅底 + 仅横向分隔线」;圆角刻度由 `8 / 10 / 28 / 999` 收敛为 `8 / 10 / 999`(删掉从未并入刻度的 `--radius-lg: 28px`,两处消费者按各自真实形态就地改归属)。两项均零新增颜色值、零新增 primitive、零阈值放宽、零新增 `!important`。

**两次范围裁定均由用户逐项作出:** Phase 9 先只做卡片化(「开一个 phase,先看看效果吧」),用户看过 5 张截图后裁定「表格重做, 圆角刻度收敛。做这两个」⇒ 另开 Phase 10;第三项候选(图标与空状态)**未点名,仍留 Out of Scope**。

**里程碑审计:** `status: tech_debt` —— 12/12 需求满足、无 critical blocker,14 项 tech debt 已登记(其中 3 项 WARNING 级结构发现:上方的 G1 / G2 与伴随 G1 的门盲区)。

<details>
<summary>历史:已 shipped 的里程碑</summary>

**v1.14 前端视觉与可访问性 — ✅ SHIPPED 2026-09-25**(归档 2026-09-26)

把前端从"零设计契约下长出来的功能骨架"变成有设计契约、键盘可用、视觉可信的工具界面。6 个阶段(4 / 4.1 / 5 / 6 / 7 / 8)、21 个计划、81 个任务,38 条需求全部交付。**零新增运行时依赖、零构建步骤**(DESIGN.md D-06 守住):六个范围域中五个是纯 `style.css` 改动,只有 Phase 8 触碰 `app.js` / `index.html`。

**核心价值首次被前端兑现:** 不可逆的 G3 授权动作现在有独立的视觉处理(实心填充 + 白字 + 16px + 600,四个强调通道用满),不再与例行「继续自检」逐字节相同——工具此前在对自己说谎,现在不再。

**v1.13 交互式讨论迭代系统 MVP — ✅ SHIPPED 2026-09-13**

DESIGN.md v1.13 全范围 20 条需求(FLOW 7 + UI 4 + AI 5 + DATA 4)交付并验证。3 个阶段、13 个计划、28 个任务。详见 `.planning/milestones/v1.13-ROADMAP.md`。

</details>

## Requirements

### Validated

**v1.13 交互式讨论迭代系统 MVP**(DESIGN.md v1.13 全范围,20 条):

- ✓ 行走骨架(阶段 1-2 全链路:进入/会话/发散/G1/恢复/权限门/双轨 AICaller/中止)— Phase 1
- ✓ FLOW-01/02/03/06、UI-03、AI-01~05 共 10 条需求 — Phase 1(见 `.planning/milestones/v1.13-phases/idi-01-1-2/01-VERIFICATION.md`,8/8 真值 + UAT 6/6)
- ✓ 轮次收敛循环(划词批注/大白话即时答/处理本轮批注 G2/轮次冻结/批注回应回写/§6.4 机器文法全解析)— Phase 2
- ✓ FLOW-04/07、UI-01/02/04、DATA-01 共 6 条需求 — Phase 2(见 `.planning/milestones/v1.13-phases/idi-02-g2/02-VERIFICATION.md`,7/7 SC + UAT 7/7 零 gap)
- ✓ 授权、自检与终点(G3 四处机械校验 + 确认词、DESIGN.md.tmp 原子落盘、宽松/严格自检两角色自动循环、D-22 残余裁决、崩溃自愈、使命完成只读归档)— Phase 3
- ✓ FLOW-05、DATA-02/03/04 共 4 条需求 — Phase 3(见 `.planning/milestones/v1.13-phases/idi-03-g3/03-VERIFICATION.md`,5/5 ROADMAP 判据 + UAT 8 检查点,4 处运行时缺陷修复后复验 passed)

**v1.14 前端视觉与可访问性**(38 条,2026-09-25 收口;逐条状态与验证记录见 `.planning/milestones/v1.14-REQUIREMENTS.md`):

- ✓ **TOKEN 8 条** — 单一围栏 `:root` 令牌块 + 颜色两层(primitive → semantic)/ 间距 / 字号 / 行高 / 字重 / 圆角 / `z-index` 单层;令牌块外零裸 `#hex`(117 → 0);primitive 名绝不出围栏 — Phase 4 + 4.1
- ✓ **VISUAL 5 条** — `#btn-authorize` 的不可逆独立处理(实心 green-12 / 白字 / 16px / 600)、G1 两只第二档、页面级层级、侧栏活动面板标记、两处 emoji 改内联掩码字形 — Phase 5
- ✓ **TYPE 3 条** — 字号刻度 5 → 7 → 8 档;`.markdown-body` 与 `renderMarkdown()` 全部 9 个注入目标获得显式 `font-size`(UA 默认与第四字重档 700 退出应用);字重三档分工 — Phase 5
- ✓ **A11Y 9 条** — 全站 `:focus-visible`(七选择器,`--color-focus` 三条 PAIR 全达标)、`#round-doc` 的 Tab 停靠点、键盘划词路径、AA 对比度全量修复(含 opacity 合成面)、两个阻塞弹窗的 Escape + `role="dialog"` / `aria-modal` — Phase 4/7/8
- ✓ **LAYOUT 4 条** — `#state-badge` 魔法数消除、窄窗口不破版(768px 承诺按实测收窄并登记 A-10)、badge 不再被横幅遮挡、侧栏滚动容器套娃收敛 — Phase 6
- ✓ **INTERACT 2 条** — hover / active / disabled 覆盖(禁用态**未被软化**)、过渡限定 `background-color` / `border-color` 120ms + `prefers-reduced-motion` — Phase 7
- ✓ **CHECK 4 条** — 四条零依赖契约校验命令(`check-01`…`check-04`),每条失败方向经变异证明 — Phase 4 + 4.1
- ✓ **REG 3 条** — `.hidden` 注释的错误理由修正、`showInlineError` 结构性修复、`b9664e0` 五条修复人工验收项全量重跑 — quick `260917-fqh` + Phase 8

**v1.15 视觉构图升级**(12 条,2026-09-28 收口;逐条状态与验证记录见 `.planning/milestones/v1.15-REQUIREMENTS.md`):

- ✓ **CARD 3 条** — 左栏 4 个面板与右栏文档区各自成为独立卡片(白底 + 可见边界 + 圆角);页面底色下沉,与卡片形成明确 elevation 层次 — Phase 9
- ✓ **VIS 2 条** — 卡片底色与阴影作为新令牌进围栏 `:root`(`check-01` 绿);圆角取现有刻度,阴影零位移 — Phase 9
- ✓ **REG 2 条** — 页面换值后对比度对**重算并登记**(非刷新旧值);五条 UI 门复跑无新增失败 — Phase 9
- ✓ **TABLE 2 条** — 文档表格改为「表头浅底 + 仅横向分隔线」,就地改写原 `border` 声明;表头新绘制面的配对经 `check-02` 实际输出证实已登记,零新增颜色值 / primitive / 阈值改动 — Phase 10
- ✓ **RADIUS 2 条** — 圆角刻度收敛为 8 / 10 / 胶囊三档(删 `--radius-lg`,两处消费者按各自真实形态改归属);收敛零视觉回归,以收敛前后运行时读数并排为证 — Phase 10
- ✓ **REG-03** — 五条浏览器门 + 四个静态门 + pytest 基线复跑无新增失败;连带指纹按「可执行性」分诊(实测 10 份覆盖 / 1 份可执行),唯一可执行的 `idi-09` 以 HEAD 内容**重新验证** — Phase 10

### Active

**无。** 下一个里程碑(v1.16)尚未定义 —— 由 `/gsd-new-milestone` 走 提问 → 研究 → 需求 → 路线图 定义。候选池见上方 `## Next Milestone Goals`。

### Out of Scope

见 DESIGN.md §1.5 与 `.planning/milestones/v1.14-REQUIREMENTS.md` 的 Out of Scope 表——写代码实施本工具之外的功能、多项目并行、多人协作、云端部署、批注以外的文档编辑、AI 生成中途插话(v2 再议);v1.14 另显式排除暗色模式、组件级令牌层、CSS 框架 / 构建步骤、lint 流水线、完整 ARIA / 屏幕阅读器合规、焦点陷阱、图标库、骨架屏、动效体系、Storybook、移动端适配。

## Context

- **设计已完成:** DESIGN.md v1.13,由 22 条已确认决策(D-01~D-22)、4 轮讨论(docs/discuss-round-0~4.md)、14 轮自检核查(docs/DESIGN-check-1~14.md)收敛而来。第 14 轮为 PASS 收口。
- **为什么存在:** 用 AI 做项目最大的浪费是"开工前没对齐"。本工具把对齐流程产品化。
- **唯一权威:** 一切入 implement 细节以 DESIGN.md 为准;`.planning/` 文档若与 DESIGN.md 冲突,DESIGN.md 胜出。
- **当前代码状态(v1.15 shipped, 2026-09-28):** 后端 10,887 LOC(含测试;15 个测试文件,219 passed / 6 skipped;**v1.15 零后端改动**)、前端 4,035 LOC(`style.css` 1912 / `app.js` 1854 / `index.html` 269);Python + FastAPI,原生 HTML/JS,仅 vendored `marked.min.js`。纯模块 `grammar.py` / `annotations.py` / `g3.py` / `checks.py` 承载全部 §6.4 文法与磁盘签名逻辑。
- **设计契约面(v1.14 建立,v1.15 扩展):** `frontend/style.css` 顶部单一围栏 `:root` 令牌块(8 档字号 / 5 条行高 / 4 个 `z-index` / 25 个 Radix primitive / 47+ 个 `--color-*`,含 v1.15 新增的 `--color-surface-card` 与 `--shadow-card`),外加 7 条零依赖校验命令(`scripts/check-01`…`check-07`)与 v1.15 新增的两条运行时门(`check-09-idi09-validation.py` / `check-10-idi10-validation.py`)+ 1 个探针(`probe-card-border-token.py`)。**设计契约现在是可执行的,不是文档承诺。**
- **v1.15 范围裁定依据(shadcn/ui 可行性结论,2026-09-26 实地核查):** 已克隆 `shadcn-ui/ui` 并逐层核对,结论是**不能引入,但可借鉴配方**。
  ①**不能引入:** 组件是 `.tsx`(React + Tailwind + Radix primitives,`apps/v4/registry/new-york-v4/ui/` 共 61 个),与「原生 HTML/JS、零构建」(D-06)直接冲突;`npx shadcn init` 会装 npm 依赖并改写 tsconfig。
  ②**但配色层面本项目并不落后** —— `frontend/style.css` 已在用 Radix Colors 12 步语义刻度(`--radix-gray-1` 等,Phase 4.1 的成果),与 shadcn 同源。**缺的是构图,不是颜色。**
  ③**可借鉴:** Card / Table / Badge / Button 的视觉配方数值;单一 `--radius` + `calc()` 派生的圆角刻度(天然不会像现有 `--radius-sm:8 / md:10 / lg:28` 那样漂);语义 token **别名**层(以新增别名方式加在现有 token 之后、不动现有名 ⇒ 门禁不受影响);lucide 图标可 vendored 成 SVG(与 `vendor/marked.min.js` 同路子,无构建)。
  ④**最大风险:** `check-05-ui-uat.py` / `check-06` / `check-07` / `probe-05` / `probe-07` 五条门大量断言绑死具体 DOM 与 computed style(焦点环 2px、`--color-focus` 解析值、sticky 表头、badge 流内机制、滚动容器收敛、命中区 24×24),**改样式极易打破,每次改动必须复跑**。
  ⑤**影响面已实测收窄:** `--radius-lg`(28px)只被 2 处消费(聊天气泡、`#chat-input-row input`),`--radius-pill` 被 5 处消费 ⇒ 圆角收敛的风险面很小。
- **已知技术债:**
  ①`SdkAICaller.abort` 在 CLI 已挂死时无法杀掉孤儿 SDK 子进程(磁盘侧"无脏状态"语义仍成立);
  ②`annotations` append 与 writeback 存在毫秒级交错窗口(模块级锁可收口);
  ③**`state.*` 写入动词全部不可信**(已复现 **15 次**,不自愈)。失效形态不止一种:改错值(`completed_phases` → 1 或 0)、改分母(数阶段编号)、删字段、**假报成功 + 零写入**、**部分成功**(`add-decision` 遇以 `-` 开头的正文会少写一条)、以及**格式副作用**(`add-decision` 双前缀 / `roadmap.update-plan-progress` 掉空格与插入重复复选框列表 / `mark-complete` 在 `**Coverage:**` 后插空行 —— 后三处**连续六次复现**,是确定性的)。判据一律取 ROADMAP 的 `## Milestones` + `## Progress`(或 `gsd_run query progress.bar --raw`),不得从 `state.json` 推;**核盘必须放在收口序列的最后一个动词之后**(`record-session` 会把人工校正过的值再次压回 0);**`update-progress` 会用坏值重算,不可作为修正手段**。第十五次(2026-09-27)首次未观察到派生计数损坏 —— 因为 `advance-plan` 走了 `last_plan` 的 fail-closed 零写入分支,损坏只发生在它真的推进位置的那一支;
  ④**4 条门标签宽于实测**(v1.14 审计 §7):L-5 称「每个」实为 9/10 行、L-6 只测可见行、`check-05` item 10 的 SC4 用固定 12 次 Tab 窗口、`check-07` g1 措辞与实测不符。四条都**不影响已通过的结论**,但门文本与其真实覆盖面不一致,是同一类「门绿但没在看」缺陷的温床;
  ⑤`idi-04` 与 `idi-06` 缺 `VALIDATION.md`(Nyquist 覆盖缺口),已登记待补。**v1.15 新增两处同型缺口:`idi-09` / `idi-10` 也无 `VALIDATION.md`**(Nyquist 能力是开着的,只是 `validate-phase` 从未对它们跑过);
  ⑥**v1.15 审计登记的 G1 / G2**(详见上方 `## Next Milestone Goals`):G1 = `#latest-check` 的灰底与 Phase 10 的表头灰底同令牌相撞、band 消失;G2 = `--radix-gray-1` 已声明零消费,围栏的「每个声明的令牌都被消费」性质已不成立而 `check-01` 结构上看不见。两者都是 WARNING,无 a11y 失败、无需求不满足;
  ⑦**`check-10` t1/t2 只钉令牌接线,不钉视觉契约** —— 58/58 PASS 与 G1 可以共存:它回答「`th` 是不是画了 `--color-surface`?」(是),从不回答「表头读起来是不是一条独立的 band?」(在 `#latest-check` 里不是)。`WR-04` 残项同源:`check-10` 里没有任何 `read_style(..., 'table', ...)`,重新加回表级边框或改 `border-collapse` 都会让 t1/t2 保持绿。
- **方法论教训:** 真浏览器 UAT 抓出了机器级验证漏掉的真实缺陷(v1.13 六处、v1.14 一处跨阶段回归)。**文本级 gate 通过不等于运行时语义成立**,且**一条不能失败的门比没有门更糟**——v1.14 的 `check-05 --item 9` 不但漏掉 AI 事件自动跟随的回归,还正面断言了该回归的前提。变异测试是唯一能证明门真的会失败的手段。
- **UAT 环境事实(省得重踩):** `check-05-ui-uat.py` 走 `.venv/bin/python` 且**必须** `--browser bundled`(该路线的 `channel="chrome"` + headless 会挂死);Node 路线才用 `channel: 'chrome'`。键盘文本选区**无法自动化**(连 `contenteditable` 都选不中),依赖 Shift+方向键的验收项必须标注为人工检查。`check-05` 全量跑 exit=2 是因为 item 5 的两条 `--ai-smoke` 腿按设计 BLOCKED,不是回归。

## Constraints

- **Tech stack**: Python + FastAPI 后端,原生 HTML/JS + markdown 渲染库前端,Claude Agent SDK 首选(子进程 `claude -p --output-format stream-json` 兜底,两路线界面契约一致) — DESIGN.md D-06/D-01/§9,不得更换
- **Runtime**: 单机单人本地运行,无云端 — D-03
- **AI 调用前提**: 本机已装 claude CLI 并登录,启动时自检 — D-19
- **数据**: 纯 Markdown + JSON 落盘,"文件即状态",工具不维护独立流程状态,一切由磁盘现状推导(§7) — D-19
- **语言**: 讨论文档以中文为主;面向用户的输出遵守 DESIGN.md §3.8 语言红线(简洁精准、大白话定义术语)
- **Scope**: 代码实施不在本工具职责范围内(工具产出设计文档后归档;本仓库的"实施"是把这个工具本身建起来)
- **Git**: 实施分支活动按仓库 CLAUDE.md 第 5 条纪律执行
- **`style.css` / `app.js` 的编辑纪律(v1.14 建立,v1.15 沿用,每个改动都必须遵守)** — 来源 `.planning/milestones/v1.14-ROADMAP.md` §全局硬规则:`grep -c '^\.hidden {' frontend/style.css` 恒为 1;`!important` **声明**数恒为 1(按声明计数,不能数命中行);**追加,不重排**(至少一对等特异性规则由源码顺序决定;需要改写既有声明时就地改写,不搬迁);不得新增 `!important`、不得令牌化 `display`、不得引入 `@layer` / `@property` / `var(--x, #fallback)`;零新增运行时依赖、零构建步骤;每个 `style.css` 计划必须带至少一项运行时验证(真实浏览器的 computed style 读数 —— `grep -c 'var(--'` 对渲染结果零证明力)

## Key Decisions

既有 22 条决策(D-01~D-22)已定案于 DESIGN.md §11 附录,此处不重复维护。实施期新增决策追加于下表:

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| 实施框架选用 GSD Core 1.13.0(open-gsd) | 五步循环 Discuss→Plan→Execute→Verify→Ship 与本项目"先讨论后动手"哲学同构;DESIGN.md 22 条决策直接充当 Discuss 阶段输入 | ✓ Good |
| GSD 安装为 local 模式(.claude/ 入库) | 项目自含,依赖可追溯;用户全局 gitignore 对 `**/.claude/` 有忽略,已 `git add -f` 破例入库 | ✓ Good |
| Phase 1:SDK/子进程两路线均强制 setting_sources=[](SDK)/--setting-sources=(CLI) | 用户全局 ~/.claude/settings.json 的 Write(*)/Bash(*) allow 规则会在权限回调前自动放行、绕过 §5.4 权限门;屏蔽来源不掩蔽 auth(环境变量级) | ✓ Good(实测双路线权限矩阵 9/9) |
| Phase 1:/api/abort 会话接线 = session.busy() 时优先 session.abort() | Plan 03 把 caller 挪进 session 后路由需跟随;dev/ping 探针的 _current_caller 路径保留 | ✓ Good(路由级测试 + UAT 实证) |
| Phase 1:会话后门控刷新走 GET /api/session 端点 + applySessionGates/renderTranscript 拆分 | done 后原地刷新 g1_available/divergence_available 门控,不重渲染 transcript(避免清掉刚流完的气泡,且 [ai] 落盘晚于 done) | ✓ Good(UAT G-idi01-7 复测) |
| Phase 1:app.js 脚本移到 body 末尾(#cli-check-overlay 之后) | DOM 先于脚本执行,CLI 自检浮层才能真跑(原顺序 recheckBtn 为 null 抛 TypeError) | ✓ Good(UAT G-idi01-8 复测) |
| Phase 2:PASS/裁决行文法解析归 P2、消费归 P3 | FLOW-07 措辞"文法全部由工具可靠解析" + ROADMAP 判据 6 明确 P2 验期;解析器(backend/grammar.py)P2 交付,Phase 3 按钮逻辑消费 | ✓ Good(47 live 边界抽检) |
| Phase 2:ask_lite 同步调用、事件不进工作面板 | §3.4"数秒内…"不打断阅读 + 单机单人;走 SSE 直播面板的是用户驱动的批处理任务(§4.3),轻量问答不属此列 | ✓ Good(UAT 真调 55s 灰斜体秒级感) |
| Phase 2:冻结 = 纯磁盘推导(轮号 < current_round 即只读),非当前轮批注 API 层拒绝 409 | 不新增后端状态;§7.4 文件即状态的直接推论 | ✓ Good(路由 19 契约 + UAT 冻结检查点) |
| Phase 2:annotations 写回(AI 不碰 JSON)与标记脏变体免疫 | §6.2 字段写回职责——后端解析响应表统一回写 answer/status,格式漂移归零 | ✓ Good(UAT a1-01 回写 answered) |
| Phase 3:裁决行锚点取末一处 `> 核查结论:` + 同号配对 | 宽松档裁决轮报告可含双结论行,锚点取末一处才能让尾部追加段进配对空间;配对与呈现必须共用同一编号空间 | ⚠️ Revisit(G-idi03-2 暴露:anchor 受限扫描与锚点无关扫描曾口径不一,已修) |
| Phase 3:自检自动推进以 hop-local 标志(而非"tmp 在盘")守卫 | 原 `finally` 守卫写反导致严格档无界自动链(实测 84 跳/1.5s);仅当 `tmp_path.replace` 实际执行处置 `tmp_consumed=True` | ✓ Good(修复后恰 1 跳,复验 passed) |
| Phase 3:prompt 契约必须由测试锁死参数注入 | `build_check_prompt` 接受 `tier` 却未注入,AI 写出非法档位行导致 `parse_tier_line` 返回 None——靠真 CLI E2E 才暴露 | ✓ Good(已补 `test_build_check_prompt_injects_tier_line`) |
| Phase 04.1:颜色族换成 Radix Colors 12 步语义刻度(25 primitive / 47 `--color-*` / 43 对清单) | 吸收 idi-04 UAT 的 3 项 FAIL 与 `--color-text-muted` 3.23:1 的 AA 倒退;结构产出(围栏 `:root`、四条守卫)不动,只重写值层 | ✓ Good(`check-01`…`05` 全 PASS;`--color-text-muted` 实测 5.62:1) |
| Phase 04.1:TOKEN-07 的「断言序关系」半场裁定 **manual-only**,不补机械断言 | 实测把四个 `--z-*` 值重排后 `check-01`…`check-05` **全部仍会通过** —— 该不变量只存在于 `style.css:229-231` 的散文注释。用户裁定本阶段不加断言,但 `REQUIREMENTS.md` 的 `Complete` 在机械层面不成立,故降级为 `Complete (PARTIAL)` 并把序关系核对移入人工验收项,不静默调和 | ⚠️ Revisit(Phase 5+ 可补一条 `ORDER` 式断言收口) |
| Phase 04.1:验证报告的 `covered_files` 必须覆盖相位目录内**全部** `*-PLAN.md` / `*-SUMMARY.md` | `verification.cjs:716` 的 `allCurrentArtifactsCovered` 要求逐一声明;idi-04.1-VERIFICATION.md 漏了 `01-PLAN.md`,仅此一项即令 `status=stale`,而指纹本身与记录值逐字节一致 | ✓ Good(补声明 + 重算指纹后 stale→human_needed→passed) |
| Phase 4:阶段**收口后**引入的字面量不算该阶段的偏差,以 `overrides:` 落证而非静默放过 | `style.css:434` `.collapse-indicator { font-size: 20px; line-height: 1; }` 由 quick `260918-qrq`(`3684353`)在 Phase 4 收口(`0c658aa`)后约 20 小时引入;Phase 4 自己的提交区间干净、已交付枚举基线范围。用户裁定为范围外,但**必须留证并指派去向**,否则就是「无人认领的洞」 | ✓ Good(记入 `idi-04-VERIFICATION.md` 的 `overrides:` + `REQUIREMENTS.md` 标 `Complete (PARTIAL)` + backlog `999.1`) |
| Phase 4:stale 的两种成因走**方向相反**的补救,不得混用 | 「内容真变」→ 重新验证(idi-04 的旧报告被取代,全部数值从 HEAD 重算);「记账性编辑」(UAT 状态归一、`phase.complete` 翻需求行)→ 重算指纹并**在报告内披露改了什么、为何不移动任何被核验的事实**。判据是拿 HEAD 内容重算指纹比对,不是看 mtime | ✓ Good(两条路径各自留证,未出现「重新盖章」掩盖内容变更) |
| Phase 4:`REQUIREMENTS.md` 不该进 `covered_files`(待后续裁决) | 它同时存在于 `idi-04` 与 `idi-04.1` 的报告里,而 `phase.complete` **每次收口都会改它** → 任何一次阶段收口都会同时打掉此前所有覆盖该文件的报告(本次收口即打掉两份)。`covered_files` 的语义应是「其变更足以使本报告结论失效的输入」,需求索引表属**下游记账**,不满足该语义 | ✓ Good(**v1.14 收口时采纳**:6 份报告全部移出 `REQUIREMENTS.md`,否则收口的 `git rm` 会二次打掉刚完成的 6 次复验) |
| Phase 5:嵌入标题刻度 = 文档档沿**数值**阶梯下移一档(28→24 / 22→18 / 18→16),逐容器列举而非写全局 `h1,h2,h3` 规则 | 全局裸类型选择器特异性 0-0-1,对四处 chrome 覆盖与 `.markdown-body` 规则都是惰性的,于是「恰好只命中这五个失控容器」——看起来更省事,但无法表达三档各不相同,且会把**任何将来的标题**一并捕获,正是本缺陷(影响面不透明)的成因;枚举还能逐条对照 `app.js` 的调用点 | ✓ Good(G-idi-05-1 关闭;文档 h1 28 > 嵌入 h1 24 由 5 条严格不等式保证,不依赖 fixture 恰好有内容) |
| Phase 5:渲染目标枚举**按 `renderMarkdown()` 调用点**而非按类名,并配一条会失败的静态普查守卫 | 同一类错误在本阶段发作了两次:plan 01 只探一个 `.markdown-body` 宿主,让 chrome 后代选择器的层叠缺陷活到执行期;修法把探针扩到 4 个宿主,但没问等价的反向问题「`renderMarkdown()` 到底注入到哪些容器」——`app.js` 有 10 个调用点 / 9 个目标,只枚举了 4 个 | ✓ Good(守卫比的是两个独立量:app.js 的 token 计数 vs `MARKDOWN_TARGETS` 条数,非自比) |
| Phase 5:`phase.complete` 又一次把 `progress.completed_phases` / `percent` 往回改(2→1 / 33→17),收口后由编排器按 ROADMAP `## Progress` 校正 | 与 `advance-plan` 同一族缺陷(既往已有复现记录)。本次未越权翻需求(`requirements_updated: false`),但进度计数器仍不可信;`state.json` 的 phases 也不是判据来源 | ⚠️ Revisit(已四次复现,编排器每次收口后必须自己核盘并校正) |
| Phase 7:焦点环环色取字面值 `#1f63bd`,**不**采纳同族的 `--radix-blue-11` | 这是对已签核契约 S-4 的**字面遵从**,不是疏漏:S-4 的签核算术(`04-UI-SPEC.md`)就是用这个值算的。`blue-11` 在归档态 0.75 合成下实测 **3.03:1** —— 余量仅 0.03,任何后续微调都会把它推回线下;`blue-12` 是高对比**文本**档,作 2px 环会被读成边框而非焦点指示。环色因此进围栏并带「不得修正」注释 | ✓ Good(三条 PAIR 实测 5.72 / 5.57 / 3.45 全达标;围栏注释逐字禁止「顺手修正」) |
| Phase 7:禁用态的 hover 闸门**落在既有 `button:hover` 规则的选择器上**(就地改写为 `:where(:not(:disabled))`),而非给每个禁用控件补一条反向规则 | 就地改写让特异性**逐位不变**(`:where()` 计 0),从而不会与九组既有填充规则发生层叠竞速;补反向规则则会新增一个需要与既有规则比特异性的竞争者。同样的推理让朴素 `:active` **刻意停在 0-1-0** —— 升到 0-1-1 就会靠源码顺序夺走 `button.primary` / `.overlay-card button` 的填充底色 | ✓ Good(SC5′ 用真实 `renderVerdictCard` + 真实 `.disabled` 断言「hover 背景 == 静默背景」;变异测试证明去掉 gate 或让位即变红) |
| Phase 8:选档成功后的焦点交还必须放在 `await refreshChecksAfterStream()` **之后**,不能紧跟 `syncBackgroundInert()` | `continueCheckBtn.disabled` 在检查在途时为 `true`,而 Chrome 的 `.focus()` 对**禁用按钮是 no-op**;`disabled` 的复位恰在 `refreshChecksAfterStream()` 内。提前放会静默失效——diff 看起来是对的、缺陷却仍然存活,比原缺陷更糟(读起来像已修)。UI 审计把它列为优先级 1,用户裁定「先修焦点,再收口」 | ✓ Good(先写出守卫看它红 `expected=btn-continue-check actual=BODY`,再修至绿;判别控制证明绿非恒绿) |
| Phase 8:`chooseTier()` 的成功路径**交还焦点**,而 `#confirmation-modal` 的「放行」路径**不交还** —— D8-10 的豁免收窄为只覆盖后者 | 豁免援引的「F1 不覆盖情形①」(整个视图即将切换)是为确认弹窗写的:放行后视图确实切换、触发者随之隐藏,钉回焦点是错的。选档成功**不切换视图**,反而让 `#btn-continue-check`(「继续自检」)变得可见 —— 正是 D8-10 自己所说的「可继续自检流程」那个位置,故豁免不适用 | ✓ Good(D8-10 + §焦点契约情形① 同步收窄;check-07 item g4 钉死该行为) |
| **v1.14 收口:预收口审计发现一处跨阶段回归(Phase 6 的 L-4 静默杀掉 AI 事件自动跟随),用户裁定「先修回归,再收口」** | Phase 6 的滚动容器收敛从 `.event-list`(= `#ai-events`)原地删掉 `max-height` / `overflow-y`,使其计算为 `overflow-y: visible`;`app.js:253` 的 `eventsEl.scrollTop = scrollHeight` 按 CSS 规范成为 no-op(非滚动元素的 `scrollTop` 恒为 0)。**没有任何东西替代它**,而本里程碑的其他五个范围域都动过 `style.css` | ✓ Good(修法:追加节点上 `item.scrollIntoView({ block: 'nearest' })`,把最新条目滚入外层 `#main-pane`;**不回退 L-4**——恢复内滚动会打破 `check-05 --item 9` 的滚动者普查) |
| **v1.14 收口:一条不能失败的门比没有门更糟 —— 新门必须用变异证明会 FAIL** | `check-05 --item 9` 不但零覆盖该回归,**还正面断言了回归的前提**(`#ai-events 计算 max-height == none # L-4:套娃第一层(55vh 限高 + 内滚动)已原地删除`),其唯一的滚动行为断言「末条内容可达」自己设 `c.scrollTop = scrollHeight` —— 那是「显式滚动下的可达性」,与「自动跟随」是两个性质 | ✓ Good(新断言驱动 app 自己的 `renderEvent` 路径追加 N 条,断言最新条目落在 `#main-pane` 可视盒内且**不动 `scrollTop`**;变异证明 `after=0 last=[2569,2621] pane=[0,900]` 转 FAIL。**本里程碑反复出现的缺陷类就是这一类**) |
| **v1.14 收口:`.collapse-indicator` 的 20px 走「加第 8 档」而非重映射** | backlog `999.1` 的三条候选(加档 / 重映射到 18-24 / 加 L-6 例外)中,加档是唯一**保持字形渲染尺寸不变**的;重映射会改已出货的 ▾/▸ 视觉,加例外则让 `20px` 永久留在出货 chrome 里 | ⚠️ Revisit(新增 `--text-lg-plus: 20px` + `--lh-none: 1`,字号刻度 7 → 8 档;**命名阶梯因此非单调**(xl=24 > 2xl=22),属已登记的 D-07 冲突,不得"顺手修正") |
| **v1.14 收口:收口类型 = `verified_closeout`** | 6/6 阶段在 `0b6283a` 全部复验 `passed`,`all_phases_verified = true`;不再需要 `override_closeout`。前提是先把被本次修复作废的 6 份指纹**全部重算并重新验证**,而不是刷新旧指纹(刷新等于断言"自验证以来什么都没变",而这里是假的) | ✓ Good(6 份报告逐份以 HEAD 内容重算 digest;`REQUIREMENTS.md` 同时移出全部 `covered_files` 以吸收收口自身的 `git rm`) |
| **v1.15:卡片化的底色关系取「页面下沉 + 白卡片」**(用户裁定 2026-09-26) | 实测发现现有层次是**反的**:页面 `#fcfcfc`(gray-1)是全场最亮,左栏 3 个面板**完全透明**,`#doc-panel` 是更暗的 gray-2(读起来像"凹陷")且**零圆角零阴影** —— 这是"平 / 丑"的机械成因,不是配色问题。三选项中此项层次最强(ΔL≈6%),且顺带把现有三层接成连贯刻度:gray-3(页面)< gray-2(`--color-surface`,控件内陷面)< 白(卡片),正好是 shadcn 的 canvas / inset / raised 三档 | ✓ Good(Phase 9 落地;页面换值作废的 8 条 PAIR 逐条以 HEAD 内容重算登记,其中 2 条按**元素实际绘制面**重新归属到卡片底色 —— 不是调色、不是放宽阈值) |
| **v1.15:两条中间调 PAIR 的解法是「重新归属」而非调色或放宽阈值** | 页面变暗会让深色前景对比度**上升**、中间调**下降**(与直觉相反):`--color-marker-active` TEXT 重算后 4.18 < 4.5、`--color-border-strong` NON-TEXT 2.91 < 3.0,双双 FAIL。但这两族的元素**全部画在面板内部**,卡片化本身确实改变了它们的绘制面 ⇒ 改记为卡片底色后在白底实测 4.77 / 3.32 双双达标 | ✓ Good(**全程未改动任何颜色值、未新增 primitive、未放宽阈值**;`marker-active` 的 NON-TEXT 半条刻意保留在页面地面 —— 4.18 < 4.77,那是更严的一侧) |
| **v1.15:表格改「表头浅底 + 仅横向分隔线」,表头底色落 `--color-surface`(gray-2)** | gray-2 正是 Phase 9 建立的三级刻度里的「内陷面」档,于是表格从「与卡片无关的网格」变成「卡片内的一个内陷块」;且它的既有 PAIR(`--color-text ON --color-surface` 15.48)已登记 ⇒ 零新增配对 | ✓ Good(`check-02` 实跑输出含该条为证;零新增颜色值 / primitive / 阈值改动) |
| **v1.15:圆角收敛 = 删令牌而非改值,两处消费者去向**不同** | `--radius-lg: 28px` 是 quick `260918-qrq` 临时视觉 pass 手调进来的,连 UI-SPEC 的圆角账本都没同步。两处消费者**形态不同**:`.chat-user` 真的是"大圆角气泡"(→ `--radius-md`,外观真变)、`#chat-input-row input`(`min-height: 52px`)在 28px 下早已被 UA 钳到 26px,它**实际就是一个胶囊**(→ `--radius-pill`,如实登记、外观零变化) | ✓ Good(一律改成 `--radius-md` 会让输入框外观真的变化 —— 那是用户没选的档位;"零变化"的判据是**测量**不是算术:收敛前后整份 computed style dump + 矩形逐值 + 元素 PNG **逐字节相同**三项并排) |
| **v1.15:连带指纹的真实形状是「10 份覆盖,1 份可执行」** | `frontend/style.css` 出现在 10 份 `passed` 报告的 `covered_files` 里,但其中 9 份的路径因归档而**不可解析**(`.planning/phases/<id>/…` → `.planning/milestones/<ver>-phases/…`),属 2026-09-14 登记的已知限制 ⇒ 它们在本次改动**之前**就已是 fail-closed stale。规划期初稿写「6 份」是错的(只扫了两个 phases 目录,漏了 `v1.13-phases/` 与 `quick/`) | ✓ Good(逐份读 frontmatter 实测校正;判据锚 `covered_files` 逐行匹配**而非**全文 grep —— 全文 grep 会把只在正文提及的 `idi-08` 算进来。`idi-09` 以 HEAD 内容**重新验证**而非刷新指纹) |
| **v1.15:门的创建动机是「七个门里零条断言覆盖表格的边框/底色」** | `check-10` 的抬头逐字记录了这条 grep 结果。它的存在本身是诚实工程 —— 但它的判据是**令牌接线**,不是视觉契约 | ⚠️ Revisit(58/58 PASS 与 G1 共存:它回答「`th` 画了 `--color-surface` 吗」(是),从不回答「表头读起来是一条独立的 band 吗」(在 `#latest-check` 里不是)。下一里程碑应决定 G1 的处置) |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-09-28 after v1.15 milestone — 2 阶段 / 7 计划 / 20 任务 / 12 需求全部交付并归档。界面首次拥有 elevation 层次(白卡片 + 页面下沉 + 三级刻度);表格重做与圆角刻度收敛。**后端与 `app.js` / `index.html` 逐字节未改。** 里程碑审计 `status: tech_debt`(12/12 需求满足、无 critical blocker,14 项 tech debt 已登记,其中 G1/G2 两条 WARNING 待下一里程碑裁定)。范围裁定两次均由用户逐项作出。本次同时把 `## Current State` 的旧里程碑内容归档进 `<details>`,并把 `## Next Milestone Goals` 从 v1.15 改写为 v1.16 的候选池。*

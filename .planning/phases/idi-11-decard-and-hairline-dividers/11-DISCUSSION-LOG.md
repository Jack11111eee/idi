# Phase 11: 去卡片化与发丝分隔线 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-28
**Phase:** 11-去卡片化与发丝分隔线
**Areas discussed:** 统一面档位, 几何与密度, 发丝线规格, 门禁改写口径

---

## 讨论范围(灰区选择)

| Option | Description | Selected |
|--------|-------------|----------|
| 统一面档位 | 面板与页面统一到哪一档;连带两个孤立令牌的去向 | ✓ |
| 几何与密度 | 768px 上限 / 居中 / `.panel-body` 内边距 / `.panel-header` 圆角 | ✓ |
| 发丝线规格 | 线取哪个令牌 / 横线覆盖范围 / sticky 表头是否收口 | ✓ |
| 门禁改写口径 | c1..c4 的断言形态 / 变异规模 / 线是否登记对比度对 | ✓ |

**User's choice:** 四项全选。
**Notes:** 讨论前已核实并排除的范围:5 个容器清单、`#doc-panel` 的 `overflow-y: auto`、`#doc-panel-header` 的 sticky 背景(三者均不得删)、交互控件与内陷面保留边界、`check-01`…`check-04` 恒不变式、G2 / `999.2` / 暗色模式 / Nyquist 缺口 / 图标与空状态全部 Out of Scope。

---

## ① 统一面档位

### Q1 — 面板与页面统一到哪一档?

| Option | Description | Selected |
|--------|-------------|----------|
| 白面 #ffffff(推荐) | `--color-surface-page` 由 gray-3 改指 `--white`;面板 / `#doc-panel` / `#doc-panel-header` 改消费它 ⇒ `--color-surface-card` 与 `--shadow-card` 归零删除;gray-1 保持零消费(G2 不动);最贴 ChatGPT | ✓ |
| gray-1 #fcfcfc | 页面改指 `--radix-gray-1`;会把 gray-1 从「零消费」变成「有消费」—— 而那是 G2 的事实基底,后续裁定 G2 时账目对不上 | |
| 保留 gray-3 + 内陷面下沉 | 内陷面改指 gray-4 保住三档方向;需消费新 primitive,`--color-surface` 的 11 处消费者全部变暗 ⇒ 多条 PAIR 重算,风险最大 | |

**User's choice:** 白面 #ffffff
**Notes:** 规划期实测的关键约束:gray-3(`#f0f0f0`)**比**内陷面 gray-2(`#f9f9f9`)**更暗**,所以"统一"必须换值,否则已裁定的 SC2(「gray-2 仍是唯一比统一面更暗的一档」)直接不成立。白面比 gray-1 对中间调前景更安全(白面更亮 ⇒ 对比度更高)。

### Q2 — 统一面由哪个令牌承载?两个孤立令牌怎么处置?

| Option | Description | Selected |
|--------|-------------|----------|
| 面板改消费页面令牌 + 删两个(推荐) | 面板 / `#doc-panel` / `#doc-panel-header` 改消费 `--color-surface-page`;`--color-surface-card`(3 处)与 `--shadow-card`(2 处)删除;与 ROADMAP Deliverable 6 一致,与 SC2 措辞同向 | ✓ |
| 反向:页面改消费卡片令牌 | `html, body` 改用 `--color-surface-card`,面板一字不动 ⇒ 零删除;但与 SC2 方向措辞相反,且「页面令牌指向卡片令牌」的语义错位会被后人读成历史遗留 | |
| 删三个,直接用 `--white` | 「地面」这层语义从令牌表消失,`check-02` 的地面标签无从挂靠,六条 PAIR 要重写标签 | |

**User's choice:** 面板改消费页面令牌 + 删两个
**Notes:** 规划期实测并核实:①`--radix-gray-1` 保持零消费 ⇒ G2 的事实基底一字不动;②`--radix-gray-3` 除页面外还有 `--color-surface-sunken`(`:140`)与 `--color-surface-hover`(`:209`)两个消费者 ⇒ 页面换值**不会**造出新的零消费 primitive;③`--radix-gray-2` 恰一个消费者(`--color-surface`,`:208`)。

### Q3 — 删除两个令牌后,要不要按 Phase 10 先例加专用残留断言?

| Option | Description | Selected |
|--------|-------------|----------|
| 加两条专用残留断言(推荐) | 参照 `scripts/check-10-idi10-validation.py:406` 的 `r1`(`fenced.count("--radius-lg") == 0`);这不是 G2 —— G2 是「通用的围栏消费断言」,仍然不做 | ✓ |
| 不加,靠 `check-01` | 只靠删除本身 + 既有围栏扫描;但 `check-01` 结构上看不见「已删令牌是否被重新声明」 | |

**User's choice:** 加两条专用残留断言

---

## ② 几何与密度

### Q1 — `#main-pane > section` 的 768px 上限与 `#main-pane` 的居中怎么处置?

| Option | Description | Selected |
|--------|-------------|----------|
| 两条保留不动(推荐) | 侧沟由「面板与页面同色」消除 —— 沟在几何上仍在但透出同一档白、不可见;零水平位移、零回归风险;居中列仍是 ChatGPT 式 | ✓ |
| 只删居中 | 保留 `max-width: 768px`,删 `align-items: center` ⇒ 内容贴左、右侧留大片白;有水平位移,可能触及命中区 / 窄窗口断言 | |
| 两条都删(铺满) | 沟真的归零,但行长变长(1440 视口下主区约 860px),`.markdown-body` 长段落与表格可读性下降 | |

**User's choice:** 两条保留不动
**Notes:** **这是对 ROADMAP Deliverable 3「一并处置」措辞的显式收窄。** 已裁定的判据是 SC3 原文「主区内容列**不再露出**左右灰沟」—— 由色统一满足,不是由删除声明满足。CONTEXT.md 已记录「下游 verifier 不得按 Deliverable 3 的旧措辞判失败」,并要求 planner 显式论证这两条仍在工作(控行长 / 定位置)、不得写成「已死声明」。

### Q2 — `.panel-body` 的 16px 内边距(Phase 9 / D-9-2)是否随卡片语言一并反转?

| Option | Description | Selected |
|--------|-------------|----------|
| 保持 16px(推荐) | 去卡片化删的是「容器边界」,不是「内容呼吸」;c4 的「面板内边距」断言可原值保留;竖向预算净多出约 41px | ✓ |
| 回到 HEAD 的 10px | 把 D-9-2 的两半一并反转;更彻底,但 c4 的断言要改,且面板内容更贴边 | |

**User's choice:** 保持 16px
**Notes:** Phase 9 的 D-9-2 只反转**间距那一半**(`gap` → 0)。

### Q3 — `.panel-header` 自己的 `border-radius: var(--radius-md)` 怎么处置?

| Option | Description | Selected |
|--------|-------------|----------|
| 归零(推荐) | 活动面板标记是 `inset 3px 0 0` 竖条,10px 圆角会把竖条上下端剪成收尖的弧;它今天不可见只是因为表头无底色 —— 那是巧合,不是设计 | ✓ |
| 不动 | 圆角不可见,改它是「没有被迫的编辑」(与 Phase 10 对 `#doc-panel-header { border-radius: 0 }` 的口径一致) | |

**User's choice:** 归零

---

## ③ 发丝线规格

### Q1 — 发丝线取哪个令牌?

| Option | Description | Selected |
|--------|-------------|----------|
| gray-6(推荐) | `--color-border-subtle` `#d9d9d9`,白面上 NON-TEXT 1.412;已是四处内陷容器的边界色 ⇒ 零新增令牌;最轻,最贴 ChatGPT 的 hairline | ✓ |
| gray-7(更重一档) | `--color-border` `#cecece`,1.574;用户 2026-09-26 裁定「稍微重一点」的那档;副作用:两处卡片消费者搬走后只剩 `:1084` 一个,语义从「卡片边界」漂成「引用条」 | |
| gray-4(更浅) | `#e8e8e8`,1.225;不是现有 `--color-*` 语义令牌 ⇒ 要新增语义别名或直引 primitive,与硬约束相冲 | |

**User's choice:** gray-6
**Notes:** 实测值(白面上):gray-4 = 1.225 / gray-6 = 1.412 / gray-7 = 1.574 / gray-9 = 3.319。primitive 表里**没有 gray-5 / gray-8 / gray-10**,可选档位就是这四级。

### Q2 — 左栏横线画在哪几条边上?

| Option | Description | Selected |
|--------|-------------|----------|
| 只画面板之间 3 条(推荐) | `#main-pane > section + section { border-top: 1px }`;第一个面板顶部不画(顶部是窗口边缘,画了会读成多一条);代价 3 条 × 1px 盒高 | ✓ |
| 每个面板顶部 4 条 | `#main-pane > section { border-top: 1px }`;实现更短,但顶部多一条贴着窗口上缘的线 | |

**User's choice:** 只画面板之间 3 条
**Notes:** DOM 顺序已核实(`frontend/index.html`):`#session-panel` → `#annotations-panel` → `#checks-panel` → `#ai-panel`。`section + section` 恰命中后三个;当中间两个带 `.hidden` 时 `#ai-panel` 仍带自己的上边线 ⇒ **两种显隐状态下都恰好 1 条可见分界**(相邻选择器按 DOM 相邻判定,不按渲染相邻)。

### Q3 — sticky 的 `#doc-panel-header` 下缘要不要一条线收口?

| Option | Description | Selected |
|--------|-------------|----------|
| 不加(推荐) | SURF / DIV 只枚举了两种线,表头下缘是第三种、超出枚举范围;且「白表头压在白面板上、滚动正文凭空消失」是 Phase 9 起就存在的行为,不是本次引入的 | ✓ |
| 加一条下边线 | 必须用 id 选择器(否则会给左栏四个表头也加上线);`height: 36px` 是 definite ⇒ 外高不变但内部少 1px 垂直空间,须运行时读数确认没移动行内徽标 | |

**User's choice:** 不加

---

## ④ 门禁改写口径

### Q1 — c1..c4 改写后以什么为判据?

| Option | Description | Selected |
|--------|-------------|----------|
| 计算读数为主(推荐) | c1/c2 断言 `getComputedStyle`(`box-shadow === "none"` / `border-radius === "0px"` / `border-*-width`);c3 断言 `body` 与面板计算底色同值且 gray-2 仍更暗(三级刻度改写成**两级**故事);c4 断言 `gap === "0px"` + 发丝线宽 `1px` + padding `16px`;令牌解析降为 `info()` 诊断 | ✓ |
| 保留令牌解析为判据 | 继续断言 `resolve_token(...)` 的解析值 —— 正是 ROADMAP 明禁的「只断言规则被写下了」:令牌改对而元素没接线也会绿 | |
| 两者都断言 | 计算读数 + 令牌解析双保险;代价:令牌被删后 `resolve_token` 返回 `None`,期望侧 `None` 会把 `ok()` 降级成 BLOCKED(exit 2)—— 门会「绿着说谎」而不是变红 | |

**User's choice:** 计算读数为主
**Notes:** 本项目实测过的静默陷阱:`ok()` 在**期望侧为 `None` 时降级成 BLOCKED(exit 2,本项目当良性码)**,文案还指向 DOM。这是选择计算读数为主而非双保险的直接理由。

### Q2 — 变异测试做多少条?

| Option | Description | Selected |
|--------|-------------|----------|
| 每条判据双向变异(推荐,6 条) | c1 加回 border/box-shadow;c2 加回四边边界;c2 删 `overflow-y: auto`;c3 统一面改回 `--color-surface`;c4 `gap` 改回 12px;c4 删掉发丝线规则 —— c2/c4 各覆盖两个方向(加回旧语言 + 删掉新契约) | ✓ |
| 每判据一条(4 条) | 每判据一条代表变异;工作量小,但「删掉新契约」这个方向没被覆盖 | |
| 只变异 c1 | 其余三条靠「复跑无新增失败」代替 —— 无法证明 c2/c3/c4 真的会失败 | |

**User's choice:** 每条判据双向变异(6 条)
**Notes:** 变异在已提交的树上做、定向 `git checkout -- frontend/style.css` 还原(**禁用 `git stash`** —— 它跨工作树共享,本项目明令禁止),还原后须逐字节相同。每条须给出「变异 → FAIL」的真实读数。

### Q3 — 发丝线要不要在 `check-02` 里登记 NON-TEXT 对比度对?

| Option | Description | Selected |
|--------|-------------|----------|
| 不登记,显式论证(推荐) | 按 Phase 10 就「装饰性边界」已写明的判据,在计划里**逐条论证**「分隔线不标识任何控件 / 状态 ⇒ SC 1.4.11 不适用」;该论证不得省略、不得默认 | ✓ |
| 登记 NON-TEXT 对 | gray-6 在白面上仅 1.412,远低于 3.0 阈值 ⇒ FAIL;要达标就得换 gray-9 `#8d8d8d`(3.319)—— 线会从 hairline 变成深灰框,与去卡片化目标相反 | |

**User's choice:** 不登记,显式论证

---

## 收口

| Option | Description | Selected |
|--------|-------------|----------|
| 我准备好写 context 了(推荐) | 四个灰区都已落定,写 `11-CONTEXT.md` | ✓ |
| 再挖灰区 | 候选:`REG-04` 的连带指纹面份数 / `check-05` 其余 item 的复跑范围 / `#doc-panel.collapsed` 的形态 / 截图取景 | |

**User's choice:** 我准备好写 context 了

---

## Claude's Discretion

- **竖线承载盒** —— CONTEXT 定为 `#doc-panel` 的 `border-left`;若运行时读数显示它顶破某条门,可在保持四条不变式(零新增 DOM、零位移、跨满高、取既有语义令牌)的前提下改用 `#main-pane` 的 `border-right`,偏离须说明判因
- **`--color-border`(gray-7)的语义注释** —— 卡片消费者搬走后只剩 `:1084` 一个消费者,是否补注释说明语义漂移
- **`#doc-panel-header { border-radius: 0 }` 的论证注释措辞**(其「卡片四角」前提已消失)—— **声明本身一字不动**
- **变异测试的执行顺序与还原手法细节**
- **`REG-04` 的连带指纹面份数** —— 须在磁盘上逐份读 `covered_files` 实测(逐行匹配,不是全文 grep;并额外测「路径是否还在盘上」);本阶段先实测再处置,不得凭记忆断言份数

## Deferred Ideas

- **`.overlay-card` 的底色** —— Phase 9 停放的开放项,用户 2026-09-27 与 2026-09-28 两次均未点名;页面变白后它会读作「内陷一档」,是否改白底同族仍待裁定
- **G2**(`--radix-gray-1` 零消费 + 通用围栏消费断言)—— 用户只裁定「连带 G1」,G2 未点名
- **`999.2`**(Phase 7 三条 affordance 缺陷)—— 未点名;执行会作废 `idi-07` 的 `passed` 指纹
- **`A11Y-V2-01/02` / `FLOW-V2-01/02` / `TOKEN-V2-01`**(暗色模式)—— 均未点名
- **Nyquist 缺口**(`idi-04` / `idi-06` / `idi-09` / `idi-10` 无 `VALIDATION.md`)—— 未点名;建议走 `/gsd-validate-phase`
- **图标与空状态** —— 两次均未点名,仍留 Out of Scope
- **`check-05` 其余 item 在 1px 几何变化下的复跑范围** —— 本次未展开;`REG-04`(Phase 12)会以「复跑零新增失败」覆盖,但本阶段就须对受 1px 几何影响的 item 做实测
- **`REG-04` 的连带指纹面份数** —— 改 `check-09` 会把该脚本的覆盖者拖进重验名单;`REG-04` 本身归 Phase 12

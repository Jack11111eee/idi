# Phase 10 Context — 表格重做与圆角刻度收敛

> **来源说明:** 本文件**不是** `/gsd-discuss-phase` 的产物 —— 与 `09-CONTEXT.md` 同例
> (Phase 9 用户裁定「直接规划」)。本阶段的两个视觉档位由用户 2026-09-27 在
> `AskUserQuestion` 中**逐项选定**,本文件把那些答复与**规划期实测的事实**如实存档,
> 使 planner 不必自行发明数值。所有条目均为**已裁定**,不重开。

## 已裁定的设计决策(用户,2026-09-27)

<decisions>
- **D-10-1:** 表格重做 = 表头 gray-2(`--color-surface`)浅底 + 仅横向分隔线 —— 去掉全部竖线、外框与表行之间的深色线;`.markdown-body th` 获得浅底 + 1px 下边线;`.markdown-body td` 保留行间极浅分隔线;就地改写原 `border` 声明,不追加覆盖规则
- **D-10-2:** 圆角刻度收敛 = 8 / 10 / 胶囊 —— 删除 `--radius-lg: 28px`;`.chat-user` → `var(--radius-md)`(外观真变 28px→10px),`#chat-input-row input` → `var(--radius-pill)`(外观零变化,52px 高下 28px 早已被 UA 钳成 26px);两处去向不同,不得「统一」
- **D-10-3:** 两项都不引入新颜色值、不新增 tier-1 primitive、不放宽 `check-02` 阈值(`TEXT_MIN` / `NON_TEXT_MIN` 与 HEAD 逐字节相同);`--radius-lg` 是删除不是新增
</decisions>

### D-10-1:表格重做 = 表头浅底 + 仅横向分隔线

用户选定档位:「**表头浅底 + 仅横向分隔(推荐)**」。具体形态:

- **去掉**:全部竖线、外框、表行之间的深色线
- **表头** `.markdown-body th`:新增 `background: var(--color-surface)`(gray-2 浅底)
  + 保留 1px 下边线
- **数据格** `.markdown-body td`:保留行间 1px **极浅**分隔线(色取 `--color-border-subtle`,gray-6)
- **动机**:表头底色落 **gray-2** 不是随便挑的 —— 那正是 Phase 9 建立的三级 elevation
  刻度里的「**内陷面**」档(`gray-3 页面 < gray-2 内陷面 < 白卡片`)。于是表格从
  「与卡片语言无关的电子表格式网格」变成「白卡片内的一个内陷块」。
- **就地改写**原 `border: 1px solid var(--color-border)` 那条声明,**不追加覆盖规则**
  (Phase 9 对 `#doc-panel` 的 `border-left` 用的是同一手法;留下一条已死的 border
  会让注释与代码互相矛盾)
- **不重开此项决策。**

### D-10-2:圆角刻度收敛 = 8 / 10 / 胶囊(删除 `--radius-lg`)

用户选定档位:「**严格收敛: 8 / 10 / 胶囊(推荐)**」。具体形态:

| 令牌 | 值 | 语义 | 处置 |
|---|---|---|---|
| `--radius-sm` | 8px | 控件(输入框 / 按钮 / 事件条目 / 代码片段) | **一字不动** |
| `--radius-md` | 10px | 卡片(面板 / 文档区 / 气泡 / 弹窗 / 裁决卡) | **一字不动** |
| `--radius-lg` | 28px | —— | **删除** |
| `--radius-pill` | 999px | 胶囊(徽标 / 发送按钮 / 输入框) | **一字不动** |

`--radius-lg` 的 **2 处消费者去向不同**,这是本阶段的承重点:

| 消费者 | 行 | 现值 | 改为 | 外观后果 |
|---|---|---|---|---|
| `.chat-user` | ~1173 | `var(--radius-lg)` | `var(--radius-md)` | **真的变了**:28px 大圆角气泡 → 10px 卡片圆角 |
| `#chat-input-row input` | ~1202 | `var(--radius-lg)` | `var(--radius-pill)` | **零变化**:52px 高的输入框在 28px 下早已被 UA 钳到 26px,本就是一个胶囊 |

- `.chat-user` 另有 `border-bottom-right-radius: var(--radius-sm)`(8px 尖角,气泡尾巴),
  **保留不动**。
- **删令牌而非保留**:围栏的 D-04 / Hard Rule 5 明写「never declare a token you are
  not consuming」⇒ 消费者搬走后不得留下未消费的 `--radius-lg` 声明。
- **`--radius-md` 不得删**:`scripts/check-09-idi09-validation.py` 动态解析它做卡片断言。
- **不重开此项决策。**

### D-10-3:两项都不引入新颜色值、不放宽阈值

与 Phase 9 逐条一致。表格表头底色取**既有令牌** `--color-surface`;圆角收敛**只改归属**、
不改任何颜色。`check-02` 的 `TEXT_MIN` / `NON_TEXT_MIN` 必须与 HEAD **逐字节相同**。

## 规划期实测的现状(硬数据)

### 表格

**规则位置** `frontend/style.css`(注释剥离后的真实行号):

```css
.markdown-body table { border-collapse: collapse; }
.markdown-body th, .markdown-body td {
  border: 1px solid var(--color-border);
  padding: var(--space-1) var(--space-2-5);   /* 4px 10px */
  font-size: var(--text-base);
}
```

**影响面**:文档区右栏占比最大的内容 —— `docs/discuss-round-N.md` 几乎全是表格,
且其中三个是 **DESIGN.md §6.4 明文规定的机器可解析表**(批注回应表 / 覆盖维度表 /
未决问题清单)。三张表共用**同一条** CSS 规则,该一致性是结构性的。

**语义耦合检查(已核实,结论:无耦合)**:后端解析的是**原始 markdown 文件**,
渲染是前端 `app.js:119` 的 `renderMarkdown()` 经 marked 转 HTML 注入 `.markdown-body`。
改 CSS 只影响呈现,不触碰任何解析路径。

### 圆角

**消费者全量清点(注释剥离后,按选择器真实归属;共 31 处)**:

| 令牌 | 处数 | 消费者 |
|---|---|---|
| `--radius-sm` 8px | 15 | `#ai-route-select` / `#project-path-input` / `button` / `.event-list` / `.event-item` / `.event-kind` / `#enter-form input[type="text"]` / `.markdown-body code` / `#round-switcher` / `.markdown-body mark` / `#confirmation-modal input[type="text"]` / `#check-switcher` / `#latest-check` / `.verdict-note-input` / `.chat-user` 的尖角 |
| `--radius-md` 10px | 9 | `#main-pane > section` / `#doc-panel` / `.panel-header` / `.overlay-card` / `#brainstorm-view` / `.chat-bubble` / `.annotation-item` / `#selection-menu` / `.verdict-card` |
| `--radius-lg` 28px | **2** | `.chat-user` / `#chat-input-row input` |
| `--radius-pill` 999px | 5 | `#state-badge` / `#stream-banner` / `#chat-input-row button` / `#pending-count` / `.annotation-badge` |

**`--radius-lg` 的来历(已用 `git log -S` 核实)**:由 quick `260918-qrq` 的
「令牌值层换血」提交(`448686b`)引入,**从未并入任何刻度声明** ——
`04-UI-SPEC.md` 的圆角账本至今还写着 `4px / 8px / 999px`(早已被那次 quick 悄悄绕过),
连 `--radius-lg` 这个名字都没出现过。⇒ 它是「临时视觉 pass 的手调值」,
与后来由 `260925-iin` 清掉的 `20px` 字号越轨值是**同一次 quick 的同型产物**。

**`#doc-panel-header` 的 `border-radius: 0` 不在本阶段范围**:它是就地改写过的**显式零值**,
带一段 2026-09-26 的论证(「溢出容器把后代裁到带圆角的 padding box,表头方角因此不可能
把卡片四角顶成方角」)。它不消费任何 `--radius-*` 令牌 ⇒ 与本阶段的收敛无关,**一字不动**。

## 已核实的门禁暴露面(规划期实测,防执行期撞墙)

### 表格:无门断言

`grep` 全部 7 个门脚本 + 2 个探针,**没有任何一条断言表格的边框 / 底色 / 布局**。
唯一的接触点是 **`scripts/check-05-ui-uat.py:1126`**:

```
ok(item, "[p1] .markdown-body td font-size == var(--text-base)", base_size,
   read_style(page, "#draft-content td", "font-size"))
```

它断言的**不是**本阶段要改的属性(`font-size` / `padding` 的 `font-size` 半场),
且期望侧由 `resolve_token` 运行时解析 ⇒ **值层不改就恒过**。
本阶段**不得碰 `td` 的 `font-size`**。

同一函数(`item4`)另用 `WIDE_MD`(一张 12 列表)做 L-2 的三宽度溢出诊断,
但那些断言测的是**文档级 `scrollWidth`** 与 `#doc-panel` 的**实测宽 vs 声明上界**。
**去掉竖线只会让表更窄** ⇒ 方向安全,但仍必须复跑(不是推断,是实测)。

### 表格:对比度

表头文字色是 `.markdown-body th` 从 `.markdown-body` 继承的 `--color-text`。
表头新绘制面 gray-2 = `--color-surface`,而

```
/* PAIR --color-text ON --color-surface TEXT */    （style.css:554，早已登记）
```

**⇒ 预期零新增 PAIR 条目**。但**必须**以 `check-02` 的实际输出证实,
不得以「我认为已覆盖」结案。行间与表头下的分隔线是**装饰性**边界 ——
SC 1.4.11 不适用于「不标识任何东西的边框」,围栏注释(`style.css` 的 role-bands 段)
已就「装饰性边框」写明这条判据 ⇒ 不需 NON-TEXT 条目,**但该判断须在计划里显式论证**。

### 圆角:门禁几乎不设防

- `check-09-idi09-validation.py:136` / `:186` **动态解析** `--radius-md` 再与卡片的
  计算 `border-top-left-radius` 比对 ⇒ **令牌相对,改值不破;但删该令牌会破**。
- `check-06-idi05-validation.py:224` 读 `borderTopLeftRadius`,但只经 `info()`
  打印,**不断言**。
- 其余门与探针:零圆角断言。
- 无任何门引用 `--radius-lg` ⇒ 删除它是安全的。

### 连带指纹:实测「10 份覆盖,1 份可执行」

> **⚠ 本节数字为规划期实测校正值。** 初稿(含 ROADMAP 与 STATE.md 的初稿)写的是「6 份」,
> 那是**只扫了 `.planning/phases/` 与 `.planning/milestones/v1.14-phases/`** 得出的 ——
> 漏了 `v1.13-phases/` 与 `quick/`。规划期(pattern-mapper 独立发现,orchestrator 逐份读盘复核)
> 实测的真实形状如下。**planner 不得沿用「6」。**

`frontend/style.css` 出现在 **10 份** `status: passed` 报告的 `covered_files` 里
(判据:锚 frontmatter 的 `covered_files` **逐行**匹配,不是全文 grep —— 全文 grep 会把只在
正文提及该文件的报告也算进来,例如 `idi-08`):

| # | 报告 | `covered_files` 路径在盘? |
|---|---|---|
| 1 | `milestones/v1.13-phases/idi-01-1-2/01-VERIFICATION.md` | ❌ 12/41 缺失 |
| 2 | `milestones/v1.13-phases/idi-02-g2/02-VERIFICATION.md` | ❌ 11/26 缺失 |
| 3 | `milestones/v1.13-phases/idi-03-g3/03-VERIFICATION.md` | ❌ 13/31 缺失 |
| 4 | `milestones/v1.14-phases/idi-04-tokens-contract/idi-04-VERIFICATION.md` | ❌ 8/13 缺失 |
| 5 | `milestones/v1.14-phases/idi-04.1-radix/idi-04.1-VERIFICATION.md` | ❌ 8/12 缺失 |
| 6 | `milestones/v1.14-phases/idi-05-typography-and-visual-hierarchy/idi-05-VERIFICATION.md` | ❌ 8/11 缺失 |
| 7 | `milestones/v1.14-phases/idi-06-layout-robustness/idi-06-VERIFICATION.md` | ❌ 8/10 缺失 |
| 8 | `milestones/v1.14-phases/idi-07-interaction-states-and-focus/idi-07-VERIFICATION.md` | ❌ 6/9 缺失 |
| 9 | **`.planning/phases/idi-09-card-containers/idi-09-VERIFICATION.md`** | ✅ **0/10 缺失 —— 全部在盘** |
| 10 | `.planning/quick/260925-iin-v1-14-ai-999-1/260925-iin-VERIFICATION.md` | ❌ 2/7 缺失(两个 UI-SPEC 指向已归档路径) |

第 1–8 与第 10 份的路径在归档时从 `.planning/phases/<id>/…` 移到了
`.planning/milestones/<ver>-phases/<id>/…`,其 `covered_files` 因此**不可解析** ⇒
重算返回 `null` ⇒ **fail-closed stale**。这是 STATE.md 于 **2026-09-14** 登记、
并在 v1.13 收口时复认的**已知限制**(`## Deferred Items` 的
`known-limitation` 行:「归档后的报告不再被 staleness 机制消费,故记为已知限制而非回填重算」)。
⇒ **它们在 Phase 10 之前就已是 stale,与本次改动无关。**

**本阶段的裁定:实际要重新验证的只有第 9 份(`idi-09`)。**
理由:①它是唯一「覆盖该文件 **且** 路径可解析」的报告;②其余 9 份的 stale 成因是**路径**,
不是内容,重验它们须先修复归档路径引用 —— 那是另一件已登记的 backlog 事项,不是本阶段的活儿。
③Phase 9 改同一文件时也只在 live 树内重验了 `idi-09` 一份。

**处置法仍是「以 HEAD 内容重新验证」,不是「刷新指纹」** —— 对 `idi-09` 而言内容确实变了,
刷新等于断言「自验证以来覆盖输入无变化」,那是不实陈述。参照
`idi-09-VERIFICATION.md` 自己的 `re_verification:` 块与正文的
「Why this is a re-verification, and what changed」段作为模板。

**本阶段不得改动 `scripts/check-05-ui-uat.py`** —— 该文件在 `idi-08` 的 `covered_files` 里
(`idi-08` 不含 `style.css`)。改它会把 `idi-08` 也拖进重验名单,**把 1 份变成 2 份**。

## 范围边界

本阶段**只做**:表格规则改造 + 圆角刻度收敛 + 门禁复跑 + `idi-09` 的连带指纹重验 + 供用户评审的截图。

**不做**(用户未点名 / 已裁定排除):图标与空状态、暗色模式、`.overlay-card` 底色、
页面级留白、输入框的 UA 白填充 —— 这四条 Phase 9 的开放项**用户本次未点名**,
仍为开放项,不得顺手一起改。

## 编辑纪律(来自 v1.14,每个改动必须遵守)

- `grep -c '^\.hidden {' frontend/style.css` 恒为 **1**
- `!important` **声明**数恒为 **1**(按 `!important;` 计数,不是命中行数 ——
  散文注释会把 `grep -c` 顶高,本项目已因此红过三次)
- **追加,不重排**(至少一对等特异性规则由源码顺序决定);需要改写既有声明时**就地改写**,不搬迁
- 不得新增 `!important`、不得令牌化 `display`、不得引入 `@layer` / `@property` /
  `var(--x, #fallback)`
- 零新增运行时依赖、零构建步骤(DESIGN.md D-06)
- 每个 `style.css` 计划必须带至少一项**运行时**验证(真实浏览器 `getComputedStyle` 读数)
- **围栏内注释不得出现「令牌名 + 冒号」** —— `check-02` 的 `DECL_RE` 扫围栏全文
  (含注释),写 `--radix-gray-12: ...` 会被当成一条值不可解析的声明而 FAIL
- 凡有 `grep -c 'X'` 门的地方,`X` 的字面量不得出现在解释性注释里

## 门禁环境事实(省得重踩)

- `check-05` **必须**走 `.venv/bin/python` + `--browser bundled`;该机
  `channel="chrome"` + headless 会**挂死**
- `check-05` 全量跑 exit=2 是**设计如此**(item 5 两条 `--ai-smoke` 腿 BLOCKED),不是回归
- pytest 必须用项目 `.venv`(环境 `python3` 是 miniconda,会让 4 个 `ai_caller` 测试假失败);
  基线 **219 passed / 6 skipped**
- macOS **没有 `timeout` 命令**
- 本机 `grep` 是 **ugrep**,`-` 算词字符 ⇒ `\b` 对含连字符的令牌名不可靠;
  改名判据要锚内容、逐行核对,别只数个数
- 8765 端口可能存在先前遗留的 uvicorn 进程;浏览器门走「复用,不新起」分支是既有事实
- `check-02` 的既有条目 `--color-text ON --color-surface` 的**实测比值**须由执行器当场跑出来贴进
  SUMMARY(pattern-mapper 报的是 `PASS  15.48`,**orchestrator 未复现该读数** —— Bash 分类器
  当时不可用)。**不得把未经复现的数字写进计划或摘要。**

---
phase: "5"
slug: "idi-05-typography-and-visual-hierarchy"
status: approved
shadcn_initialized: false
preset: none
created: "2026-09-20"
reviewed_at: "2026-09-20T12:05:36Z"
review_verdict: APPROVED
review_note: "Dimension 4 FLAG — 3 non-blocking evidence defects (the --text-md consumer count missing :626; the line-height fence comment leaving --lh-compact unpaired while the head still said four, plus the pre-existing 18/28 arithmetic error; a wrong specificity parenthetical in Hard Rule 9). All three corrected in place after independent re-verification against disk. No BLOCK."
supersedes_sections: ["Typography"]
---

# Phase 5 — UI Design Contract(排版与视觉层级)

> 前端阶段的视觉与交互契约。由 `gsd-ui-researcher` 生成,由 `gsd-ui-checker` 验证。

## 权威声明 —— 用本文件之前先读这一节

**本文件是增量契约,刻意不是全量契约。** Phase 5 只改 `frontend/style.css` 的排版与视觉层级,
不重写已经签核的设计系统。与上游三份契约的关系如下:

| 节 | 权威来源 |
|---|---|
| `## Typography`(本文件) | **本文件** —— 它重写 `04-UI-SPEC.md` 的 `## Typography` 节(5 档 → 7 档;后由 quick `260925-iin` 增至 **8 档**,见 §最终字号阶梯) |
| `## Color` / `## Contrast Verification` | `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` —— **本文件不重写它们**;本文件只**增补** Phase 5 新增的 4 条 PAIR 与 4 条令牌值改动,并逐条标明增补点 |
| Spacing Scale(S-1,12 档) | `04-UI-SPEC.md` —— **已签核,本阶段一字不动** |
| Design Decisions Q1–Q7 | `04-UI-SPEC.md`(Q2 的「Phase 5 applies」由本文件兑现;Q7 的机制被 D-20 刻意替换,见 §契约修正登记) |
| Global Hard Rules 1–7 | `04-UI-SPEC.md` + `ROADMAP.md` §全局硬规则 —— 本文件 §Global Hard Rules 逐条复述,不改动 |
| Do-Not-Touch List | `04-UI-SPEC.md` —— 本文件只**追加** Phase 5 的四条 |
| 四条契约校验命令 | `04-UI-SPEC.md` —— 本文件追加两条 Phase 5 专用门 |
| Copywriting Contract | `04-UI-SPEC.md` —— **本阶段改动零文案**,该节原样有效 |
| Literal exceptions L-1…L-5 | `04-UI-SPEC.md` —— **L-3 被本阶段整个撤掉**,见 §契约修正登记 |
| Sign-Off Items | `04-UI-SPEC.md` 的 S-1…S-4 与 `idi-04.1-UI-SPEC.md` 的 S-5/S-6 **均已签核,不得重开,任何一行式替代方案不得执行**;本阶段新增 **S-7 / S-8** |
| Notes | **按前缀分家。** `04-UI-SPEC.md` 的 `N-1…N-5` 与 `idi-04.1-UI-SPEC.md` 的 `04.1-N-1…04.1-N-8` 各自有效;**本文件的注释编号为 `05-N-1…05-N-6`** |
| 不在 v1.14 | `04-UI-SPEC.md` —— 本文件 §不在本阶段 只追加 Phase 5 自己的范围锁 |

**禁止复制上游全文。** 复制 `04-UI-SPEC.md`(1179 行)或 `idi-04.1-UI-SPEC.md`(864 行)会造出本项目
反复付代价的**第二事实源** —— 正是 Phase 4 存在的理由。凡本文件与上游冲突,**只有本文件显式重写的
那一节以本文件为准**;其余冲突一律以对应上游为准。

```yaml
canonical_refs:
  # 本阶段的直接上游
  - .planning/phases/idi-05-typography-and-visual-hierarchy/05-CONTEXT.md   # D-01…D-23,已锁定
  - .planning/ROADMAP.md                                                     # §Phase 5 + §全局硬规则 1-7 + §Backlog 999.1
  - .planning/REQUIREMENTS.md                                                # §VISUAL 01-05 / §TYPE 01-03 / §Out of Scope
  - .planning/STATE.md                                                       # §Operator Next Steps(S-1…S-4 签核原文)
  # 上游契约(本文件不重写它们)
  - .planning/phases/idi-04-tokens-contract/04-UI-SPEC.md                    # 除 Color / Contrast / Typography 外全部
  - .planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md                      # Color + Contrast Verification 的权威
  - .planning/phases/idi-04.1-radix/idi-04.1-CONTEXT.md                      # D-02 / D-04 / D-14 / D-15
  - .planning/phases/idi-04.1-radix/idi-04.1-UI-REVIEW.md                    # :75 Pillar 4 / :77 C-1
  - .planning/phases/idi-04.1-radix/idi-04.1-VERIFICATION.md                 # covered_files(D-05 的复验对象)
  - .planning/phases/idi-04-tokens-contract/idi-04-VERIFICATION.md           # frontmatter overrides:
  # 代码面
  - frontend/style.css                                                       # 围栏 L5-343;L405-434 / L463-472 / L611-626 / L648-667 / L878-946 / L999-1004 / L836 / L1021
  - frontend/index.html                                                      # L12-70 四个 section;L61 / L88 两处 .collapse-indicator
  - frontend/app.js                                                          # L344-397 applySessionGates;L1561-1570 .collapsed 切换
  - scripts/check-01-token-conformance.sh
  - scripts/check-02-contrast.py                                             # 比值的仲裁者
  - scripts/check-03-hidden-uniqueness.sh
  - scripts/check-04-important-count.sh
  - scripts/check-05-ui-uat.py                                               # :689-695(D-04 反转对象)/ :742(D-03 改法)
  - scripts/ui-states/                                                       # p1 / p12 / p3 / checking / archive
```

---

## Design System

| Property | Value |
|----------|-------|
| Tool | none |
| Preset | not applicable |
| Component library | none —— 原生 HTML/JS,无框架(DESIGN.md D-06) |
| Icon library | **none。** 两个内联字形,以 `mask-image` + `background-color` 实现,零新文件、零依赖、零 CDN |
| Font | `-apple-system, "PingFang SC", "Helvetica Neue", sans-serif`(不变,`style.css:348`) |
| Token substrate | 原生 CSS 自定义属性,单一围栏 `:root`(`style.css:5-343`)。零构建、零依赖、零新文件 |
| Build step | none(D-06) |

**设计系统门 —— 已执行,无发现。** `components.json` / `tailwind.config.*` / `postcss.config.*`
三者皆不存在(已核)。技术栈是 Python + FastAPI + 原生 HTML/JS;这里的「设计系统」是一段手写的
CSS 令牌围栏,不是一个可安装的包。shadcn **不适用**,也不曾提供:硬约束 D-06 禁止框架与构建步骤,
而 CSS 自定义属性两者都不需要。

**`## Component Inventory` 整节省略。** 按其自身的门,`Tool: none` 时该节整节省略 —— 没有可枚举的包,
凭记忆编一份会是对一个不存在的已安装依赖的**虚假事实陈述**。

**无 registry 门适用。** `frontend/vendor/` 只含一个文件(`marked.min.js`),本阶段每个计划跑完之后
仍须只含一个文件(D-01 / 硬规则 6)。

---

## 本阶段的改动面(唯一事实)

**唯一改动的文件:`frontend/style.css`。**

| 区域 | 改动 |
|---|---|
| 围栏 `:root`(L5-343) | 新增 2 个字号令牌 + 1 个 tier-2 标记色 + 2 个 `--icon-*`;改动 4 个 tier-2 绿色令牌的**值**;新增 4 条 `/* PAIR */`;重写 4 处围栏注释 |
| 围栏外 | **恰 6 处**:3 条 `.markdown-body h1/h2/h3` 的 `font-size` 值;4 条规则的字重;1 条 `#btn-authorize` 的 `font-size` 新增;2 条 `::before` 的机制替换;追加 2 条活动态标记规则 |

**零改动(硬约束):** `frontend/app.js`、`frontend/index.html`、`frontend/vendor/`、`scripts/ui-states/`。

**会改的脚本(与 `style.css` 同批处理):** `scripts/check-05-ui-uat.py` 的断言按 D-03 分类更新、
按 D-04 反转。**`scripts/check-02-contrast.py` 的代码零改动** —— 它从围栏读清单,清单变而代码不变,
这是它设计上最关键的一条。

**明确不含:** 暗色模式 / `prefers-color-scheme`、图标库 / sprite 体系 / 图标字体、`.collapse-indicator`
的越轨字面量(backlog `999.1`)、hover / active / transition(Phase 7)、布局结构常量 / 窄窗口 /
滚动容器 / 命中区(Phase 6)、焦点样式(Phase 7)。详见 §不在本阶段。

---

## 基线与契约漂移口径(D-01 / D-02 / D-03)

**D-01:磁盘 HEAD 是唯一现实基线。** 本契约的每一个「现状」值都取自 `frontend/style.css` 的磁盘内容
与 `scripts/check-05-ui-uat.py` 的断言;两份上游 UI-SPEC / `ROADMAP.md` §Phase 5 / `REQUIREMENTS.md`
的具体数值**只作意图参考**。**不改 `04-UI-SPEC.md` / `ROADMAP.md` 正文**(改 ROADMAP 会作废已通过的
验证指纹)。

**契约漂移登记 —— 每一条都是「契约文本 ≠ HEAD」,已由 quick `260918-qrq` 实现或推翻:**

| 契约文本声称 | HEAD 实况 | 性质 | 本阶段动作 |
|---|---|---|---|
| `.markdown-body h1/h2/h3` **无** `font-size` | **已有**作用域规则 → 24/18/16px(`style.css:624-626`) | 已实现 | **改值**:28/22/18 |
| `#doc-pane > h1` 是约 32px 粗体 | 该选择器**不存在**;实际是 `#doc-panel-header h1` = 14px / 500 / `#646464`(`:405-410`) | 已实现 | **只复证**(D-19),选择器名更正 |
| `#brainstorm-view h2` = 14px / `#8a6508` | 16px / `--color-action-warning`(`:679-683`);`#8a6508` **在围栏里不存在** | 已推翻 | **D-02**:门改写为令牌接线表述 |
| TYPE-02:`code` 现 12.5px 分数值 | 已是 `var(--text-base)` = 14px(`:645`) | 已实现 | 只复证(D-08) |
| TYPE-02:blockquote 现 `#666` | 已是 `var(--color-text-muted)`(`:633`) | 已实现 | 只复证 |
| TYPE-02:`table th/td` 现 13px vs 正文 14px | 已是 `var(--text-base)` 14px vs 本体 16px(`:639`) | 已实现 | 只复证 |
| TYPE-03 基线「仅 600 / 400 两档」 | 三档:400×1 / 500×4 / 600×12 | 已推翻 | 本阶段**改分工**(D-09) |
| 字号锚点 13px | 14px(`--text-base`);刻度 5 档 `12/14/16/18/24` | 已推翻 | D-06 扩到 7 档 |
| 契约字号表 `--text-2xl: 18px` / `--text-3xl: 22px` | 18px 已被 `--text-lg` 占用;22 / 28 均不存在 | 已推翻 | **D-07**:同名不同值,围栏注释必须写明 |
| 契约行高 `1.35 / 1.6 / 1.75` | `1.3333 / 1.5556 / 1.625`,另有 `--lh-snug 1.4286` | 已推翻 | D-10 只改注释措辞 |
| 契约圆角三值 `4 / 8 / 999` | 四值 `8 / 10 / 28 / 999` | 已推翻 | 本阶段不动 |
| 契约 `--color-action-*` 候选 hex `#e9f7ef` / `#26754a` / `#1f5c3a` | `--green-800` 已被 04.1 V-13 删除;三族共用 green-3 / green-11 / green-12 | 已推翻 | 本阶段重挑步,见 §Color |
| 契约 `--sidebar-w: 420px` | 已改名改值为 `--doc-panel-w: clamp(340px, 30vw, 480px)`(`:201`) | 已推翻 | 本阶段不动(Phase 6) |
| 契约 L-5:`#state-badge { right: 448px }` | 该声明已消失,`#state-badge` 现在是流内元素(`:583-591`) | 已推翻 | 本阶段不动 |
| 契约 `--fw-medium`「**No. Do not declare it.**」 | 已声明且消费 4 处 | 已推翻 | 本阶段把消费数提到 8 |
| 「五个元素只靠 `.hidden` 隐藏」清单 | 已过期;`#session-panel` 现也由 `.hidden` 控制(`app.js:356`) | 已推翻 | 见 §VISUAL-04 |
| ROADMAP / 04-UI-SPEC 引用的 `app.js:1550` | 已漂移到 `app.js:1563` / `1569` | 行号漂移 | 本契约按 HEAD 行号书写 |

**D-03 —— `check-05-ui-uat.py` 的字面 px 断言分两类处理。** 这是本阶段最容易做错的一处:

| 类别 | 断言 | 处理 |
|---|---|---|
| **Phase 5 主动改动的值** | `#brainstorm-view h2` 字号(`:742`)、`.markdown-body h1/h2/h3` 字号(新增)、按钮字号 / 字重(新增) | **改成令牌接线表述** —— 期望侧来自 `resolve_token(page, "--…")`,不再硬编码 px |
| **守卫「不该变」的值** | `.panel-header h2` 14px(`:746`)、`#draft-view h2` 18px(`:745`)、`.overlay-card h3` 24px(`:747`)、`.markdown-body` 16px(`:751`)、`--text-base == 14px`(`:800-807`)、`.markdown-body code` 14px(`:760`) | **保持字面 px** |

**理由(必须照抄进计划):** 字面值在守卫上是**特性而非缺陷**。它是唯一能抓到「误伤 chrome」的形态 ——
把 `.panel-header h2` 改成令牌接线表述会让该断言退化为同义反复,而它存在的全部理由恰恰是**保证
Phase 5 的标题改动没有溢出到 chrome**。D-02 之所以能把 `#brainstorm-view h2` 改成接线表述,是因为
那条**本来就不是守卫**:它守卫的那个 14px 值已由 qrq 推翻,继续硬编码只会继续假 FAIL。

**已接受的代价:** 牺牲「硬编码值能抓令牌接错线」的那部分检测力。补偿:接线断言旁保留 `info()` 打印
运行时解析值(`check-05` 既有形态),值的仲裁者始终是 `scripts/check-02-contrast.py`。

---

## Typography —— 本文件重写 `04-UI-SPEC.md` 的同名节

### 最终字号阶梯(D-06 / D-07,定稿)

**8 档。** 5 → 7 新增两档(Phase 5);7 → 8 新增一档(quick `260925-iin`,`--text-lg-plus` 20px)。**正文本体保持 16px**(`--text-md`)不变 —— DESIGN.md 的阅读尺寸不动。

| 档 | Token | 值 | 与契约(`04-UI-SPEC.md`)的关系 |
|---|---|---|---|
| 1 | `--text-xs` | 12px | 同 |
| 2 | `--text-base` | 14px | 同(**S-2 已签核的一级字号档,不得删**) |
| 3 | `--text-md` | 16px | 同 |
| 4 | `--text-lg` | 18px | 同 |
| 5 | `--text-lg-plus` | **20px** | **新**(quick `260925-iin`)—— 值序在 `--text-lg`(18)与 `--text-2xl`(22)之间;命名阶梯非单调,依据是已登记的 D-07 冲突(`--text-xl` 24 > `--text-2xl` 22)。唯一消费者 `.collapse-indicator` |
| 6 | `--text-xl` | 24px | 同 |
| 7 | `--text-2xl` | **22px** | **新** —— 契约里同名令牌指 18px,现指 22px。**名同值不同,不是笔误** |
| 8 | `--text-3xl` | **28px** | **新** —— 契约里同名令牌指 22px,现指 28px |

**`--text-2xl` 的命名冲突必须写进围栏注释(D-07)。** 04-UI-SPEC 的字号表写
`--text-2xl: 18px` / `--text-3xl: 22px`,而 HEAD 上 18px 已被 `--text-lg` 占用、22px 不存在。
本阶段继续跟随 `xs / base / md / lg / xl` 的**尺寸递进命名法**(2xl 是 xl 之上的下一档),于是
`--text-2xl` 是 22px、`--text-3xl` 是 28px —— **数值序与名字序在 `xl`(24)→`2xl`(22)这一处不单调**。
围栏注释必须写明这一点,否则日后对照契约必然困惑。

**围栏声明位置:** 紧接 `--text-xl`(`style.css:209`)之后插入两行,**按名字序**(xs → base → md → lg →
xl → 2xl → 3xl),不按数值序。理由:名字序让「下一档是 2xl」这件事在文件里可读;数值序会把两行插到
`--text-lg` 与 `--text-xl` 之间,读起来像既有档被改动。

**Hard Rule 5 核账:** 两个新令牌**与消费者同提交**。消费者恰好各一个,都在同一批:

| 新令牌 | 消费者(同一提交) |
|---|---|
| `--text-2xl` 22px | `.markdown-body h2`(`style.css:625`) |
| `--text-3xl` 28px | `.markdown-body h1`(`style.css:624`) |

**既有档的消费者迁移核账(不得出现孤儿档):**

| 档 | HEAD 消费者 | 本阶段后 | 迁移 |
|---|---|---|---|
| `--text-lg` 18px | `#draft-view h2, #rounds-placeholder h2`(`:613`)、`.markdown-body h2`(`:625`) | 2 处 | 失去 `.markdown-body h2`,**获得** `.markdown-body h3` → 净不变 |
| `--text-md` 16px | 7 处(`:549` `:618` `:626` `:681` `:720` `:757` `:957`) | 7 处 | 失去 `.markdown-body h3`,**获得** `#btn-authorize` → 净不变 |
| `--text-xl` 24px | 3 处(`:548` `.overlay-card h3`、`:624` `.markdown-body h1`、`:712` `#chat-greeting`) | **2 处** | 失去 `.markdown-body h1` → **仍 ≥1,不孤儿** |

### 标题映射(D-06,定稿)

| 元素 | 选择器 | 值 | 字重 | 行高 |
|---|---|---|---|---|
| 文档 h1 | `.markdown-body h1` | `--text-3xl` 28px | `--fw-semibold` 600 | `--lh-tight` 1.3333 |
| 文档 h2 | `.markdown-body h2` | `--text-2xl` 22px | `--fw-semibold` 600 | `--lh-tight` |
| 文档 h3 | `.markdown-body h3` | `--text-lg` 18px | `--fw-semibold` 600 | `--lh-tight` |
| 文档本体 | `.markdown-body` | `--text-md` 16px(**不变**) | `--fw-regular` | `--lh-reading` 1.625(**不变**) |

**改动只有三条 `font-size` 值。** 字重与行高**已经正确**:`.markdown-body h1, h2, h3`(`:623`)已声明
`line-height: var(--lh-tight)` 与 `font-weight: var(--fw-semibold)`,D-10 与 D-09 对这两项**要求零改动**。

### 行高:D-10 —— 复用 `--lh-tight`,零新增令牌

**新开两档不引入任何行高令牌。** h1/h2/h3 统一 `--lh-tight`(1.3333),因为该规则已存在。

围栏注释(L217-221)的措辞从「**整数配对**」改为「**比率配对**」:

| 档 | 比值配对 | 整数? |
|---|---|---|
| `--text-xs` 12 | 12 / 16.00(`--lh-tight`) | 是 |
| `--text-base` 14 | 14 / 20.00(`--lh-snug` 1.4286) | 是 |
| `--text-md` 16 | 16 / 26.00(`--lh-reading` 1.625) | 是 |
| `--text-lg` 18 | 18 / 24.00(`--lh-tight`) | 是 |
| `--text-xl` 24 | 24 / 32.00(`--lh-tight`) | 是 |
| **`--text-2xl` 22** | **22 / 29.33**(`--lh-tight`) | **否** |
| **`--text-3xl` 28** | **28 / 37.33**(`--lh-tight`) | **否** |

**为什么必须改措辞:** 28k 与 22k 同时为整数要求 k 是 0.5 的倍数,而 k = 1.5 太松(28 × 1.5 = 42px,
标题会散开)。**整数配对在数学上不可得**,不是没试。

**改写该注释时另有两处必须一并修正(否则新注释仍自相矛盾):**

- **既有算术错误:`18/28` 是错的。** `--text-lg` 18px 配 `--lh-tight` 1.3333 得 **24**,不是 28。
  改写后的注释须写 `18/24`(上表已按正确值书写)。
- **`four` 与上表的三档不自洽。** `--lh-compact`(1.5556)是**纯 chrome** 行高,唯一消费者是
  `.overlay-card p`(`:549`),**不属字号刻度配对**。改写后的注释要么给它单列一行并注明
  「chrome-only」,要么删掉 `four` 这个词 —— 不能像现状那样,头部说「four」而刻度配对只列三档。

### TYPE-02 —— 认定已由 qrq 实现,本阶段只做复证(D-08)

| 项 | HEAD 实况 | 判定 |
|---|---|---|
| `table th/td` | `var(--text-base)` 14px(`:639`),本体 16px | 比正文低一档的相对关系**已与契约意图一致**(契约时代是 13 vs 14,同样低一档) |
| 行内 `code` | `var(--text-base)` 14px(`:645`);12.5px 已消失 | 已归入刻度与令牌 |
| `blockquote` | `color: var(--color-text-muted)`(`:633`) | 已归入令牌 |

**结论:TYPE-02 作为「复证项」收口,零 CSS 改动。** 计划必须给出可核证据(见 §四条命令的扩展),
**不得**为了「有交付物」而重写这三处的值 —— 那会把一个已经正确的状态改坏,并让 `--text-base` 的
消费者计数漂移。

### TYPE-03 —— 字重三档分工显式化(D-09)

**分工规则(定稿):**

| 用途 | 字重 | 选择器 |
|---|---|---|
| 内容标题 | `--fw-semibold` 600 | `.markdown-body h1, .markdown-body h2, .markdown-body h3`(**已正确,不动**) |
| chrome 标题 | `--fw-medium` 500 | `.panel-header h2`、`#doc-panel-header h1`(**已正确,不动**) |
| **按钮** | **`--fw-medium` 500** | 见下表 —— **本阶段改动** |
| 徽标 / 事件 chip | `--fw-semibold` 600 | `.event-kind` / `#state-badge` / `#stream-banner` / `#pending-count` / `.annotation-badge`(**不动**) |
| 唯一例外 | **`--fw-semibold` 600** | **`#btn-authorize`(D-12,见下)** |
| 次级说明 | `--fw-regular` 400 | `.tier-desc`(**不动**) |

**六个动作按钮的字重从 600 改为 500 —— 它们现在与内容标题同重,这是分工的由来。**

| 规则行 | 选择器 | HEAD | 本阶段 |
|---|---|---|---|
| `:654` | `#btn-approve-draft` | `--fw-semibold` | → `--fw-medium` |
| `:666` | `#btn-divergence` | `--fw-semibold` | **不动**(它不在六个动作按钮之列;它是发散入口,琥珀族) |
| `:882` | `#btn-process-round` | `--fw-semibold` | → `--fw-medium` |
| `:933` | `#btn-authorize` | `--fw-semibold` | **保持 600**(D-12 的唯一已登记例外) |
| `:945` | `#btn-start-writing` | `--fw-semibold` | → `--fw-medium` |
| `:1003` | `#btn-continue-check, #btn-continue-repair` | `--fw-semibold` | → `--fw-medium` |

**`--fw-medium` 的消费数 4 → 8,`--fw-semibold` 的 12 → 8。** 两档都远 ≥1,不产生孤儿令牌。

**`#btn-divergence` 为什么不在六个之列:** D-11 的三段坡道只定义 routine / commit / irreversible 三族,
`#btn-divergence` 不属于任何一族(它是 `--color-action-warning` 族)。把它拉进「按钮统一 500」会让
三段坡道之外出现一个未登记的第四档。**它保持 600 是本契约的显式决定,不是遗漏。**

### 字号刻度的范围栅栏(Pitfall M4 / TYPE-01)

**绝不写全局 `h1, h2, h3` 规则。** 它会与四处 chrome 覆盖碰撞。

**栅栏成立的机械理由(计划必须核这条,不是核措辞):** 栅栏成立与否,**不能只看 chrome 标题元素落在
哪里,必须看 chrome 选择器能匹配到哪些元素**。这两件事在本项目里不等价 —— 本阶段执行期抓到的正是
二者之差(见下方「订正记录」)。

| chrome 标题 | `index.html` 位置 | 选择器形态(收窄后) | 能匹配到的元素 |
|---|---|---|---|
| `.panel-header h2` | `:16` `:31` `:42` `:58` | 后代,0-1-1 | 仅四个面板头;其容器不含 `.markdown-body` |
| `#draft-view > h2` | `:105` | **子组合器**,1-0-1 | 仅 `:105` |
| `#brainstorm-view > h2` | `:120` | **子组合器**,1-0-1 | 仅 `:120` |
| `#round-title` | `:135` | id,1-0-0 | 仅 `:135` |
| `.overlay-card h3` | `:160` `:172` `:186` `:198` `:215` | 后代,0-1-1 | 仅五个弹窗卡 |

**后三条是 Phase 5 在执行期从后代形态收窄而来的。** 原形态 `#draft-view h2` / `#rounds-placeholder h2` /
`#brainstorm-view h2`(均 1-0-1)是**后代**选择器,会伸进 `.markdown-body` 容器内部,把
`.markdown-body h2`(0-1-1)**无条件**压回 chrome 字号 —— ID 列胜过类列,与源码顺序无关。实测:
`#draft-content h2` 与 `#round-doc h2` 渲染 18px、`#brainstorm-content h2` 渲染 16px,三者都拿不到
D-06 要求的 22px(只有 `#latest-check` 是对的 —— 它嵌在 `#checks-panel > .panel-body`(`:45`)里,
没有任何 chrome 选择器够得到它,`.markdown-body h2` 是唯一匹配的规则)。**`#rounds-placeholder > h2`
不可用**:chrome 标题嵌在 `.round-view-header`(`:134`)里,子组合器会匹配不到任何元素,
故改用该元素自带的 id `#round-title`。

因此 `.markdown-body h1/h2/h3`(0-1-1)与四处 chrome 覆盖**在层叠上永不相遇**,改值不可能带偏它们。
**SC1 的实检因此是两件事,不是「看起来没变」:**(a) 四条 chrome 断言仍绿;(b) `.markdown-body` 的
**四个宿主各自的 h1/h2/h3 都到达 D-06 的目标档**。只探一个宿主会让缺陷从另外两个溜过去 ——
那正是它此前存活到执行期的原因。

**改动的影响面 = 下表九行,计划必须逐行点名。** `renderMarkdown()` 的**全部九个**注入目标:

| 渲染目标(选择器) | 注入它的 `app.js` 函数 | 刻度族 | 三档字号 |
|---|---|---|---|
| `#draft-content` | `renderDraft` | `doc` | 28 / 22 / 18 |
| `#brainstorm-content` | `renderBrainstorm` | `doc` | 28 / 22 / 18 |
| `#round-doc` | `loadArchiveView` | `doc` | 28 / 22 / 18 |
| `#latest-check` | `applyPhase5View` | `doc` | 28 / 22 / 18 |
| `.event-content` | `renderEvent` | `embedded` | 24 / 18 / 16 |
| `.chat-bubble` | `appendChatMessage` | `embedded` | 24 / 18 / 16 |
| `.say-chunk` | `appendSayToChat` | `embedded` | 24 / 18 / 16 |
| `.annotation-note` | `renderAnnotations` | `embedded` | 24 / 18 / 16 |
| `.annotation-answer-body` | `renderAnnotations` | `embedded` | 24 / 18 / 16 |

表里的取值规则只有一条,四个决策各出半边,不得写出第三种说法:**刻度族** —— 嵌入档 = 文档档
沿契约的**数值**阶梯下移一档(**D-06** 的文档刻度 28 / 22 / 18 / 本体 16,按 **D-07** 登记的
「数值序与名字序在 `--text-xl`(24) → `--text-2xl`(22) 处不单调」故**按数值序**下移:
28 → 24 = `--text-xl`、22 → 18 = `--text-lg`、18 → 16 = `--text-md`);**字重** —— 按 **D-09** 取
内容标题档 `--fw-semibold`(600),这五个容器渲染的是内容(AI 输出 / 用户批注)而不是 chrome 标题;
**行高** —— 本组规则不加 `line-height`,与 **D-10** 的「零新增行高令牌」一致;**影响面** —— 按
**D-19** 的层级链 28 > 24 > 22 > 14,嵌入 h1 取 24 而非 28 正是为了让这条链在会话流里真有标题时
仍成立(文档 h1 **严格大于**每一个嵌入目标自己的 h1)。

表下三条,计划必须一起核:

1. **枚举按调用点,不按类名。** `#round-doc` 有**两个**调用点(`loadArchiveView` 与冻结轮路径
   `app.js:1047`),故 `app.js` 的 `renderMarkdown(` 计数是 **11**(1 处定义 + 10 个调用点),
   比目标数(9)多 1。只枚举四个 `.markdown-body` 宿主正是 `G-idi-05-1` 存活到验证后的直接原因。
2. **check-05 的 `MARKDOWN_TARGETS` 是本表的机器可核形态**,`MARKDOWN_HOSTS`(4 个文档宿主)与
   `RENDER_TARGETS`(5 个嵌入目标)都由它派生;调用点普查守卫(`renderMarkdown(` 计数 == 11 且
   枚举条数 == 9)使两者无法漂移 —— 新增一个渲染目标而不更新枚举,门立刻 FAIL。
3. 表里的**函数名**是给人核对的锚点(它比行号稳 —— Phase 8 改 `app.js` 时行号会漂),不参与断言。

**一处已知且刻意不处理的不一致(记录,不是交付物):** `#brainstorm-content` 是 `.markdown-body`,
它内部的 markdown h2 是 22px,而同一容器自己的标签 `#brainstorm-view > h2` 是 16px ——
内容标题大于容器标签。**不改。** 理由与 CONTEXT 对 `.overlay-card h3` 24px vs `.markdown-body h2`
22px 的处置同源(模态高于正文标题是合理的):chrome 标题与内容标题是**两个令牌族**,它们的相对
大小不由本阶段调和。若要调和,那是排版刻度的再平衡,属独立阶段。

> **订正记录(2026-09-21,执行期)。** 本节此前有两处事实错误,均由执行期 `check-05` 的 item 4 失败暴露:
>
> 1. 「四处 chrome 覆盖**在层叠上永不相遇**」的论证核的是 **chrome 标题元素**是否落在
>    `.markdown-body` 之内(结论:都不在),却没有核 **chrome 选择器**是否够得到 `.markdown-body`
>    之内的元素(结论:三个够得到)。元素位置与选择器可达性不等价,前者成立推不出后者。已按上表重写。
> 2. 「`#brainstorm-content` 内部的 markdown h2 **会是** 22px」在当时是**错的** —— 实际渲染 16px
>    (不是 18px,更不是 22px)。22px 只有在收窄 chrome 选择器之后才成立。该条「**不改**」的结论不变
>    (收窄是修层叠缺陷,不是调和这两个令牌族),事实描述已按实测改写。
>
> 收窄本身登记为 `.planning/WINDOWS.md` 第 15 条的处置结果。`04-UI-SPEC.md` / `ROADMAP.md` 正文未动
> (D-01:改 ROADMAP 会作废已通过的验证指纹)。

### 未在 HEAD 上受控的字号(不属本阶段,见 §不在本阶段)

`.collapse-indicator` 的字号**已不再是刻度外字号** —— 已由 quick `260925-iin` 落为第 8 档
`--text-lg-plus`(20px),backlog `999.1` 第 1 项由此关闭;`#confirm-error` 因 `.overlay-card p`(0-1-1)
压过 `.hint`(0-1-0)而渲染 16px,是全站唯一以两个
不同字号渲染的 `.hint`。后者**仍不在本阶段**,理由与一行式替代方案见 §不在本阶段。

**本节此前的普查漏了五个渲染目标(已由 P-20 闭合)。** `renderMarkdown()` 的返回值还被注入
`.event-content` / `.chat-bubble` / `.say-chunk` / `.annotation-note` / `.annotation-answer-body`
这五个**不是** `.markdown-body` 的容器,它们在本阶段之前一直回落 UA 默认值:`.chat-bubble` 上下文
32 / 24 / 18.7px、`.event-content` 上下文 28 / 21 / 16.4px,字重一律 **700**。**这条漏项使本节
「刻度外的第 6 个渲染字号」这个计数本身不成立** —— 实际刻度外字号至少有 8 个,且其中含一个
契约只声明三档之外的**第四个字重档**。**闭合状态:** 已由 **P-20** 与 `G-idi-05-1` 的修法消除
(五个目标改取 24 / 18 / 16px 与 `--fw-semibold`,由 check-05 的 `--item 7` 逐目标断言);
P-20 闭合后本节剩余的两条中,`.collapse-indicator` 的 20px 已由 quick `260925-iin` 落为第 8 档
(见本节开头);**`#confirm-error` 16px 仍然存在**,不因 P-20 而消失。
**这条漏项的类型(枚举不全)与本阶段 plan 01 的层叠缺陷同型** —— 两次都是「只枚举了影响面的一部分」。

---

## Color —— 不重写 04.1,只增补 Phase 5 的四处值改动

**本节不重写 `idi-04.1-UI-SPEC.md` 的 `## Color`。** 那份文件的 25 个 tier-1、47 个 tier-2、
43 对清单、以及「role bands 在三处被算术推翻」的记录**全部继续有效**。本节只做三件事:
兑现 `04-UI-SPEC.md` Q2 的「Phase 5 applies」、落地 VISUAL-01/02 的三段坡道、落地 VISUAL-04 的标记色。

### 三段坡道(D-11 定稿)—— 形态差异是第一区分手段

| 档 | 选择器 | 形态 | 三个令牌的取值 |
|---|---|---|---|
| **routine** | `#btn-process-round` / `#btn-continue-check` / `#btn-continue-repair` | **淡底 + 绿字**(不变) | bg `--color-action-routine-surface`(green-3)/ border `--color-action-routine`(green-11)/ color `--color-action-routine-fg`(green-12) |
| **commit** | `#btn-approve-draft` / `#btn-start-writing` | **实心填充 + 白字** | bg `--color-action-commit-surface`(**green-11**)/ border `--color-action-commit`(green-11)/ color `--color-action-commit-fg`(**`--white`**) |
| **irreversible** | `#btn-authorize` | **实心更深 + 白字 + 字号步进 + 600** | bg `--color-action-irreversible-surface`(**green-12**)/ border `--color-action-irreversible`(**green-12**)/ color `--color-action-irreversible-fg`(**`--white`**) |

**语义读法:** 淡底 = 「例行」/ 实心 = 「这一步会留下东西」/ 实心更深 + 更大 + 更重 = 「这一步不可逆」。
**形态是第一区分手段,色深是第二。**

**这是一次纯值改动,选择器结构一字未动。** 三族的消费者规则(`:648-655` `:940-946` `:928-934`)
已经按 `background / border-color / color` 三条声明写成,本阶段只改**令牌的值**:
`-surface` 从 green-3 提到填充步、`-fg` 从 green-12 改为 `--white`。这正是 `04-UI-SPEC.md` Q2 承诺的
「Phase 5 的差异化是一次一行式的值改动」,也是 Phase 4 把契约放在最前面的全部理由。

**`-surface` 因此没有失去消费者(Hard Rule 5 核账)。** 三个 `-surface` 令牌都仍是各自规则的
`background` —— 只是值从淡底变成实心。**没有令牌被删、没有令牌变孤儿。**

### 两个填充步:green-11 / green-12 —— 不是契约预告的 9/10(见 S-7)

**契约与围栏注释都预告 Phase 5 会声明 green-9 / green-10 作为实心填充步**(`style.css:42-45`:
「Phase 5 declares the 9/10 fill steps together with their consumers」;**`04-UI-SPEC.md` Q2 的表**
写 commit `#26754a`、irreversible `#1f5c3a`)。**这个预告被 04.1 自己的算术推翻,本阶段按算术走。**

围栏内已记录的实测(`style.css:81-86`,与 `idi-04.1-UI-SPEC.md` Finding 1 同源):

| 族 | 9 步白字 | 10 步白字 | 11 步白字 | 12 步白字 |
|---|---|---|---|---|
| green | **3.16 ✗** | **3.55 ✗** | **4.72 ✓** | **12.32 ✓** |

**「step 9 = 实心填充 + 白字」是 Radix 的规范用法,但在本项目的每一族上都过不了 4.5:1。**
`--radix-green-11` 是**最浅的通过步**(项目已签核的 Pitfall 4a 规则应用在填充上而非文字上),
`--radix-green-12` 是该族最深的步。两者**都已声明、都已消费** —— 于是:

> **Phase 5 声明的新 tier-1 primitive 数量 = 0。**

围栏注释 `style.css:42-45` 的那句预告**因此变成一句假话,必须重写**(与 04.1-N-8 同源:一条解释代码
的注释在前提消失后必须改,否则它会开始说谎)。

**`#btn-authorize` 的字号步进(D-13):** `font-size: var(--text-md)` = 16px,**现有档,零新增令牌**。
契约原本写的 `--text-xl` 16px 是 13px 锚点世界的 1.23×;现锚点 14px,16px 即 1.14×。**不加 padding 步进。**

**`#btn-authorize` 的字重例外(D-12):** 保持 `--fw-semibold` 600。这是 D-09「按钮统一 500」的**唯一
已登记例外**。理由:核心价值要求授权绝不与例行混同,而它有四个可用强调通道(形态 / 色深 / 字号 / 字重),
此处用满。

**硬规则不变量继续成立(D-15):** `--color-action-irreversible*` **只被 `#btn-authorize` 消费,永不出现
第二个消费者**;三族名不得改(`commit` 而非 `gate` —— 「gate」在本代码库已指决策门)。

**`:disabled` 态零改动(D-14):** 实心按钮沿用 `opacity: 0.55`。对实心按钮而言 0.55 是**更强的**淡化
(实心 → 淡绿是明显的去饱和),区分度反而上升;与 Pitfall M5「不得软化 `:disabled`」字面一致。
**不得为了让实心按钮的禁用态"更好看"而调这个值。**

### 活动面板标记色(VISUAL-04 / D-18)

**新开一个诚实命名的 tier-2 令牌,不复用 `--color-action-primary`:**

```css
/* 围栏内,紧随 --color-action-* 族之后 */
--color-marker-active: var(--radix-blue-11);
```

**为什么必须新开而不是复用(D-18):** `--color-action-primary` 这个名字说的是「主要动作」,拿它做
面板指示器会让**名说谎** —— 而本项目为此付过代价:04.1 的 D-03 把 26 个 primitive 全部改名,理由正是
「保留旧名会让名说谎」。这是同一条方法论的第二次应用。

**为什么是蓝而不是契约划定的琥珀:** 琥珀在本系统已承载**警告**(`--color-action-warning` /
`#pending-count` / `#state-badge` 系)与**冻结轮**(`#round-doc.round-frozen` 的琥珀 inset 竖线)
两重含义,再加「活动面板」即三重撞车。蓝在本系统已是「信息 / 流式」色(`--color-surface-info` /
`--color-text-info` / `--color-border-streaming`),与琥珀**明确分离** —— 这正是 D-18 选蓝的全部理由。

**为什么是 blue-11 而不是更浅的蓝步:** blue-2/3 对 3px 竖条与 14px 标题都太浅。blue-11 是本族的
指示 / 文字步,且已声明、已消费(它已承载 `--color-action-primary` / `--color-text-info` /
`--color-kind-say` / `--color-border-streaming` 四个 tier-2 名)。**本阶段把它变成第五个 —— 这是刻意的,
不是重复。** 实测:blue-11 在 `--color-surface-page` 上 **4.65:1**,同时满足 TEXT(≥4.5)与
NON-TEXT(≥3)。**这是本阶段最薄的一处余量(0.15),不得"为了更保险"而换步**(Pitfall 4a)。

**60/30/10 的登记(D-18 要求):** 这是对契约 Accent 域的**刻意偏离并已登记** —— 契约的 Accent 行把
「active-panel marker (Phase 5)」列在 `--color-action-primary` / `--color-action-warning` 之下。
本阶段保留了 Accent 行的**元素清单**(活动面板标记仍是 accent 域元素),只把承载它的**令牌名**换成一个
说实话的新名字。**颜色本身没变**(blue-11 就是 `--color-action-primary` 的值),所以 accent 预算的
面积占比不受影响。

### VISUAL-03 —— 认定已由 qrq 实现,本阶段只做复证(D-19)

| 项 | HEAD 实况 | 判定 |
|---|---|---|
| `#doc-panel-header h1` | `font-size: var(--text-base)` 14px、`font-weight: var(--fw-medium)` 500、`color: var(--color-text-secondary)`(`:405-410`) | 源码注释即「安静的容器标签,不是全屏最大最重的文字」 |
| `#doc-pane > h1` | **该选择器不存在** | 契约文本的漂移,已在 §基线与契约漂移口径 登记 |

**零 CSS 改动。** 计划只需把 gate / 交付物里的选择器名从 `#doc-pane > h1` 更正为 `#doc-panel-header h1`。

**连带效果(D-06 之后页面级层级已立住),这是 SC3 的证据链:**

| 排名 | 元素 | 字号 |
|---|---|---|
| 1 | 文档自己的 `.markdown-body h1` | **28px** |
| 2 | `.overlay-card h3`(模态标题) | 24px |
| 3 | `.markdown-body h2` | 22px |
| … | `#doc-panel-header h1`(容器标签) | **14px / 500** |

**全屏最大最重的文字不再是容器标签「文档区」。** SC3 由「28 > 24 > 22 且容器标签 14/500」这一条链证明,
由运行时断言核(见 §四条命令的扩展)。

---

## VISUAL-04 落地规格 —— 侧栏活动面板标记

### 范围修正(D-16,契约措辞需登记)

**REQUIREMENTS.md 的 VISUAL-04 写「侧栏四个面板的活动/非活动态可区分」。实测该措辞**不能**按字面实现:**

| 面板 | 显隐机制 | 依据 |
|---|---|---|
| `#session-panel` | `app.js:356` `classList.toggle('hidden', !isSessionPhase)` | 阶段 1-2 可见;阶段 3+ / checking / archive 隐藏 |
| `#annotations-panel` | `app.js:362/370/375/380/385/390` | 仅 `phase3` 且有 `current_round` 时可见 |
| `#checks-panel` | `app.js:436/444/597/827` | 仅 `phase5_checking` 与 `mission_complete` 可见 |
| `#ai-panel` | **从不被 `.hidden`** | `grep -n "aiPanel" frontend/app.js` **零命中**;它的折叠是 `#ai-panel-body` 上的 `.collapsed`(`app.js:1562-1565`) |

**结论:`:not(.hidden)` 只能表达前三个的互斥,表达不了 `#ai-panel`。** 前三个面板在任一状态里
**恰有一个**可见(实测:`p1`/`p12` → session;`p3` → annotations;`checking`/`archive` → checks),
所以「活动态」= 那个可见的。`#ai-panel` 用**它自己的**展开/折叠态(既有 `▾`/`▸` 指示器)作为可辨状态。

**REQUIREMENTS.md 的 VISUAL-04 措辞需登记为:「三选一活动态 + AI 面板折叠态」。** 本阶段不改
`REQUIREMENTS.md`(改它会作废指纹),只在计划与验证记录里登记该口径。

**非活动面板是 `display: none`(看不见),所以「可区分」实际退化为「当前活动的那一个看得出是活动的」。**
这是 D-17 已承认的实情,不是缺陷 —— 三个面板是**切换**而非**叠加**(DESIGN.md §4.1/§4.2)。

### 形态与实现(D-17,定稿)

**左侧一条 3px 竖条 + 面板标题文字改用标记色。**

```css
/* 追加在文件末尾(硬规则 3:追加,不重排)。 */
#session-panel:not(.hidden) .panel-header,
#annotations-panel:not(.hidden) .panel-header,
#checks-panel:not(.hidden) .panel-header {
  box-shadow: inset 3px 0 0 var(--color-marker-active);
}
#session-panel:not(.hidden) .panel-header h2,
#annotations-panel:not(.hidden) .panel-header h2,
#checks-panel:not(.hidden) .panel-header h2 {
  color: var(--color-marker-active);
}
```

**四条承重决定,每条都要写进计划:**

1. **`box-shadow: inset` 而非 `border-left`。** `box-shadow` 不参与布局 ⇒ **零位移**;`border-left`
   会给标题行加 3px 宽度,把 `#pending-count` / `#check-state` 往右推。**冻结轮已经是这个写法**
   (`:917-920`),有现成先例可抄。
2. **竖条落在 `.panel-header`,不落在 `<section>` 上。** 三个 section 的子元素都带背景色
   (`.chat-bubble` / `.annotation-item` / `.event-list` / `.panel-body`),它们会在自身背景层盖住
   左边缘的 inset 竖条;标题行**没有**带背景的左边缘子元素,竖条因此可见。
3. **标题只改 `color`,不改 `font-weight`。** 两条理由:(a) D-09 已把 chrome 标题统一为 500,
   在这里改成 600 会与 D-09 直接冲突;(b) `.panel-header` 是 `height: 36px` +
   `justify-content: space-between` 的 flex 行,改字重会移动行内的 `#pending-count` / `#check-state`。
   **两个理由都指向「只改 color」。**
4. **3px 与 `.markdown-body blockquote` 的 `border-left: 3px` 一致**(`:630`)。刻度外的字面量?
   **不是** —— 它落在 `--space-*` 刻度上吗?不落。**它是本阶段新增的第 7 个刻度外字面量吗?**
   也不是:`box-shadow` 的偏移/模糊/扩展不是设计令牌,04-UI-SPEC 的 L-1…L-5 从未覆盖它们,
   且冻结轮的 `inset 3px 0 0` 已是既有先例。**这一点必须写明,否则会被读成疏漏。**

**`#ai-panel` 零 CSS 改动(D-16 / D-23)。** 它的 `▾`/`▸` 指示器(`.collapse-indicator`)是它
唯一的可辨状态,**不得触碰** —— `app.js:1563` / `:1569` 用 `textContent` 赋值,内联 `<svg>` 会被擦掉。
本阶段对 `.collapse-indicator` 的规则数改动 = **0**。

**`#doc-panel-header` 不受影响。** 它是 `.panel-header` 但不被上面三条 ID 选择器匹配 ✓
(`#doc-panel` 是文档面板的容器标签行,不是「活动面板」概念的一部分)。

### 层叠核账(计划必须逐条核)

| 新规则 | 特异性 | 竞争对手 | 竞争规则的特异性 | 结果 |
|---|---|---|---|---|
| `#session-panel:not(.hidden) .panel-header` | 1-2-0 | 无(`.panel-header` 未声明 `box-shadow`) | 0-1-0 | ✓ 无竞争 |
| `#annotations-panel:not(.hidden) .panel-header` | 1-2-0 | `#annotations-panel .panel-header { cursor: default }`(`:807`) | 1-1-0 | ✓ 不同属性 |
| `#checks-panel:not(.hidden) .panel-header` | 1-2-0 | `#checks-panel .panel-header { cursor: default }`(`:979`) | 1-1-0 | ✓ 不同属性 |
| `… .panel-header h2`(三条) | 1-2-1 | `.panel-header h2`(`:432`,未声明 `color`) | 0-1-1 | ✓ 无竞争 |

**`:not(.hidden)` 的特异性贡献 = 0-1-0**(取参数的特异性)。三处 ID 选择器都靠 1-0-0 的 ID 分量取胜,
与源码顺序无关 —— 但**仍须追加在末尾**(硬规则 3),因为日后可能有人往 `.panel-header` 上加 `box-shadow`。

**与 `.hidden` 机制的关系:** `.hidden { display: none !important }` 是机制而非样式,**不得触碰**
(硬规则 1)。`:not(.hidden)` 是**读取**该状态,不是修改它;隐藏时选择器根本不匹配,两者不冲突。

---

## VISUAL-05 落地规格 —— 两处内联字形(D-20 / D-21 / D-22)

### 机制:mask-image + background-color(刻意偏离契约的 `content: url(data-URI)`)

**契约(`04-UI-SPEC.md` Q7)写死的机制是 `content: var(--icon-*)` + data-URI 内转义 hex。本阶段
刻意改用 mask。** 理由(D-20):

| 机制 | 颜色如何跟随文字 | 结论 |
|---|---|---|
| `content: url(data-URI)` | data-URI 经 `content` 渲染为**图片**,**不继承页面 CSS**,`currentColor` 不可用 ⇒ fill 只能钉死为转义 hex | 「跟文字色」是**人工同步的约定**,值层一变就静默漂移 |
| **`mask-image` + `background-color`** | `background-color` 是普通 CSS 声明 ⇒ **真正跟随令牌** | **采用** |

**附带收益(这是撤掉 L-3 的依据):** mask 只看 **alpha**,所以 `<path>` **不带 `fill` 属性**即可
(默认黑 = 不透明)。**data-URI 里因此零颜色信息**,契约的字面量例外 **L-3 可以整个撤掉**。

**代价(已接受,D-20 明写):** 伪元素从「内联字形」变成**盒模型**,需要 `display: inline-block` +
显式尺寸 + 间距,对齐需实测。**这是本阶段唯一需要实测微调的视觉项。**

### 围栏内的两个令牌

```css
/* 围栏内。形状为实心(D-22):mask 只看 alpha,实心形状在 12px 下比轮廓线清晰得多。
   <path> 不带 fill 属性 ⇒ 本 data-URI 内零颜色信息 ⇒ 契约例外 L-3 整个撤掉。
   具体 d='…' 由规划期定(D-22);形状契约见下表。 */
--icon-pin:      url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'%3E%3Cpath d='…'/%3E%3C/svg%3E");
--icon-location: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'%3E%3Cpath d='…'/%3E%3C/svg%3E");
```

**令牌形状契约(可机械核):**

| 约束 | 值 | 理由 |
|---|---|---|
| `viewBox` | `0 0 12 12` | 渲染尺寸 12×12(D-22),viewBox 与渲染尺寸一致可省一次缩放 |
| `<path>` 数量 | 恰 1 | 两个字形各一条路径 |
| `fill` 属性 | **禁止出现** | mask 只看 alpha;带 fill 会重新引入颜色信息,并使 L-3 无法撤掉 |
| 颜色信息 | **零** —— data-URI 内不得出现 `%23`、`#`、`fill=` | 这是 L-3 撤掉的**唯一依据**,必须机械可核 |
| `xmlns` | 必须带 | 无命名空间的 SVG 在部分引擎下不渲染 |
| 形状风格 | **实心**(D-22) | 12px 下轮廓线不可辨 |
| 两形状 | **必须彼此可辨**(图钉 vs 地图标记) | 它们在同一界面里承载两个不同语义(批注引用 / 裁决位置) |

### 两条伪元素规则 —— 原地改写,不追加

**改 `style.css:836` 与 `:1021` 的规则体本身,不在文件末尾追加重复选择器。**

```css
.annotation-quote::before {
  content: '';
  display: inline-block;
  width: 12px;
  height: 12px;
  margin-right: var(--space-1);
  vertical-align: -2px;
  background-color: var(--color-text-secondary);
  -webkit-mask-image: var(--icon-pin);
  mask-image: var(--icon-pin);
  -webkit-mask-size: 12px 12px;
  mask-size: 12px 12px;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-position: center;
}

.verdict-location::before { /* 同上,换成 --icon-location */ }
```

**为什么原地改写不违反硬规则 3:** 硬规则 3 的实质是「**重排即渲染变更**」—— 它防的是把一条规则
移到另一条**等特异性**规则之后。这里的两个选择器**没有任何竞争者**(全文各只出现一次,已核),
原地改写在层叠上等价于追加。**原地改写还避免了在文件末尾留一条被覆盖的死 `content: '📌 '`。**

**三条实现细节,缺一即错:**

1. **`margin-right: var(--space-1)`(4px)是必需的。** 原来的 `content: '📌 '` **自带一个尾随空格**;
   `content: ''` 的 12px 盒没有尾随空格,不加间距图标会贴住文字。4px 是刻度内档,且与
   「12px 图标 + 4px 间距 = 16px」的 emoji 占位宽度相当。
2. **`-webkit-mask-*` 与 `mask-*` 都要写。** 无前缀 `mask-image` 是现代 Chrome 的写法,
   `-webkit-` 前缀是 WebKit 系的写法。这是**唯一的冗余声明**,理由具体、零依赖、零构建。
3. **`mask-repeat: no-repeat` 必须显式声明**(默认值是 `repeat`),`mask-size` 也必须显式声明
   (SVG 有 viewBox 但无内在尺寸,`auto` 的落点依赖引擎)。

### 用色与对齐(D-21 / D-22)

| 项 | 值 | 理由 |
|---|---|---|
| 用色 | `background-color: var(--color-text-secondary)` | 图标在正文流里,不该抢眼;与相邻文字**同色**(D-21)。**不再是转义 hex。** |
| 渲染尺寸 | 12×12 | 与 14px 文字并排的常规图标尺寸(D-22) |
| `vertical-align` | `-2px` | 契约原值(D-22),保持不变 |
| 对齐验收 | 图标与相邻文字**基线视觉对齐**,不撑高行盒 | 该 12px 盒在 14px / `--lh-snug`(20px)的行里不得改变行高 |

**图标的颜色对比度已由既有 PAIR 覆盖,不需要新配对:** `.annotation-quote` 在 `.annotation-item`
内(`background: var(--color-surface)`,`:831`),`.verdict-location` 在 `.verdict-card` 内
(`background: var(--color-surface-warning-subtle)`,`:1016`)。清单里已有
`--color-text-secondary ON --color-surface`(**5.62**)与
`--color-text-secondary ON --color-surface-warning-subtle`(**5.82**)。**TEXT 阈值(4.5)严于
NON-TEXT 阈值(3.0),同一对 fg/bg 的 TEXT 通过即蕴含 NON-TEXT 通过** —— 再加一条 NON-TEXT 配对
是同义反复。**这是刻意的零新增,不是遗漏。**

### 与 `.collapse-indicator` 的关系(D-23,零交互)

**`.collapse-indicator` 的 `textContent` 赋值路径不得触碰。** `app.js:1563` / `:1569` 用 `textContent`
赋值,内联 `<svg>` 会被擦掉(`#ai-panel` 与 `#doc-panel` 是两个可折叠面板,各有自己的指示器)。
**唯一例外(quick `260925-iin`):** 该规则的 `font-size` / `line-height` 两个**声明值**已换成令牌
(`--text-lg-plus` / `--lh-none`)—— 只改值,`textContent` 赋值路径与「不得内联 `<svg>`」一字未动,
故本条禁令**在实质上仍然成立**;backlog `999.1` 第 1 项由此关闭。

**mask 方案的一个附带简化(值得写进计划):** 本阶段**不在 DOM 里放任何内联 `<svg>`** ——
图标是伪元素上的 CSS 掩码。所以即便日后有人给 `.collapse-indicator` 换成图标,也不存在「`textContent`
擦掉内联 SVG」这一类问题。**Pitfall 7 的第二半被机制本身消解。**

---

## Contrast Verification —— 增补,不重写

**`idi-04.1-UI-SPEC.md` 的 `## Contrast Verification` 继续有效。** `scripts/check-02-contrast.py`
是**唯一仲裁者**,上游文档的 AA 论断**不采信**。本节只登记 Phase 5 造成的清单变化与实测值。

### 清单变化:43 对 → 47 对(35 TEXT + 12 NON-TEXT)+ 1 ORDER

**四条新增(全部落在围栏内 `/* PAIR */` 清单里,与令牌同一 diff):**

```css
  /* 活动面板标记:3px 竖条是非文本状态指示器(SC 1.4.11),面板标题是文本(SC 1.4.5);
     两者都落在 --color-surface-page 上(三个面板都在 #main-pane 内,其祖先无背景声明,
     故底色是 body 的 --color-surface-page)。 */
  /* PAIR --color-marker-active ON --color-surface-page TEXT */
  /* PAIR --color-marker-active ON --color-surface-page NON-TEXT */

  /* 两个实心填充作为控件边界对底色(SC 1.4.11)。两者的落地面都是 --color-surface:
     #approve-row / #writing-view / #authorize-row 都在 #doc-panel-body → #doc-panel 内,
     而 #doc-panel { background: var(--color-surface) }。
     routine 三只按钮落在 --color-surface-page 而非 --color-surface,但它们本阶段未改动,
     且其既有的 --color-action-routine ON --color-action-routine-surface 配对已覆盖其边界。 */
  /* PAIR --color-action-commit ON --color-surface NON-TEXT */
  /* PAIR --color-action-irreversible ON --color-surface NON-TEXT */
```

**三条既有配对的值会变(行不改,值随令牌变):**

| 清单行 | HEAD 实测 | 本阶段实测 | 说明 |
|---|---|---|---|
| `--color-action-routine-fg ON --color-action-routine-surface` | 11.00 | **11.00**(不变) | routine 族值未动 |
| `--color-action-commit-fg ON --color-action-commit-surface` | 11.00(green-12 on green-3) | **4.72**(white on green-11) | 淡底 → 实心 |
| `--color-action-irreversible-fg ON --color-action-irreversible-surface` | 11.00(green-12 on green-3) | **12.32**(white on green-12) | 淡底 → 实心更深 |

**一条既有的注释行变成假话,必须重写:** 清单里那行
`/* amber text on its three real grounds, and the six green buttons (three families, one value) */`
中的「**three families, one value**」在本阶段之后**不再成立** —— 三族从此有三个不同的值对。
与 04.1-N-8 同源:一条解释清单的注释在前提消失后必须改。

### 实测表(Phase 5 新增与变化的部分,全部由 check-02 仲裁)

**TEXT(阈值 4.5:1):**

| 配对 | 比值 | 判定 |
|---|---|---|
| `--color-marker-active ON --color-surface-page` | **4.65** | ✓ **本阶段最薄的余量(0.15)** —— 见 05-N-2 |
| `--color-action-commit-fg ON --color-action-commit-surface` | **4.72** | ✓ white on green-11 |
| `--color-action-irreversible-fg ON --color-action-irreversible-surface` | **12.32** | ✓ white on green-12 |
| `--color-action-routine-fg ON --color-action-routine-surface` | 11.00 | ✓ 不变 |

**NON-TEXT(阈值 3:1):**

| 配对 | 比值 | 判定 |
|---|---|---|
| `--color-marker-active ON --color-surface-page` | **4.65** | ✓ |
| `--color-action-commit ON --color-surface` | **4.48** | ✓ green-11 on `#f9f9f9` |
| `--color-action-irreversible ON --color-surface` | **11.70** | ✓ green-12 on `#f9f9f9` |

**被否决的候选(记录以防被"好心改回"):**

| 候选 | 实测 | 为什么否决 |
|---|---|---|
| green-9 作填充(`#30a46c`) | white = **3.16 ✗** | 契约与围栏注释的预告;Radix 的规范用法,但过不了 AA |
| green-10 作填充 | white = **3.55 ✗** | 同上 |
| green-11 作**不可逆**档(把 11 给 authorize) | white = 4.72 ✓ | 会**反转**两档的深浅关系:commit 只能退到 green-12(更深),「实心更深 = 不可逆」的语义当场失效 |
| `--color-marker-active` = `--radix-blue-2` / `blue-3` | 远低于 4.5 | 3px 竖条与 14px 标题都不可辨 |
| `--color-marker-active` = `--radix-blue-12` | 高 | 会把面板标题变成深海军蓝,与 `--color-text` 抢重;且放弃「最浅通过值」规则 |

### 不新增配对的三处,及理由

| 未新增 | 理由 |
|---|---|
| 图标(fg `--color-text-secondary`)的两个落地面 | 同一 fg/bg 的 **TEXT** 配对已在清单里(5.62 / 5.82);TEXT 阈值严于 NON-TEXT,再加是**同义反复** |
| `--color-action-commit` 与 `--color-action-irreversible` **互为背景**的配对 | 两者**永不并排渲染**(p3 里 `#btn-approve-draft` 所在的 `#draft-view` 是 `display: none`)。SC 1.4.11 的「相邻颜色」规则在此不适用;两档的**可区分性**由 D-04 的运行时不等断言保证 |
| routine 三只按钮对 `--color-surface-page` 的边界配对 | routine 族本阶段**未改动**,其既有配对(`ON --color-action-routine-surface`,4.21)已覆盖其边界 |

---

## Spacing Scale —— 已签核,本阶段一字不动

**`04-UI-SPEC.md` 的 `## Spacing Scale`(S-1,12 档,含 5 个非 4px 倍数档)继续有效。**
S-1 已由用户在 2026-09-17 签核,**不得重新讨论,不得执行任何一行式替代方案**。

**本阶段的间距改动 = 0 条声明。** 唯一涉及间距的是两处**新增**声明,两者都取刻度内档:

| 新增声明 | 值 | 刻度归属 |
|---|---|---|
| `.annotation-quote::before` 的 `margin-right` | `var(--space-1)` 4px | ✓ 刻度内 |
| `.verdict-location::before` 的 `margin-right` | `var(--space-1)` 4px | ✓ 刻度内 |

**`box-shadow: inset 3px 0 0` 的 `3px` 不是间距值。** 它是 box-shadow 的偏移分量,不属
`--space-*` 族,04-UI-SPEC 的 L-1…L-5 也从未覆盖它。**冻结轮的同一形态(`:919`)已是先例。**
这一句必须写进计划,否则会被读成「新增了一个刻度外字面量」。

**`#btn-authorize` 不加 padding 步进(D-13 明写)。** 它的 padding 保持
`var(--space-2) var(--space-4)`,只有 `font-size` 变。

**窄面板下的不换行核账(计划必须实测):** `#btn-authorize` 的文本「授权撰写总设计文档」9 字,
14px ≈ 126px → 16px ≈ 144px,加 `padding-x` 32px = **约 176px**。`--doc-panel-w` 的最小值是 340px,
`#doc-panel-body` 的 padding 是 `var(--space-8) var(--space-10)`(32/40),故最窄内容宽 = 340 − 80 =
**260px > 176px** ✓ **不换行**。这是 D-13 的验收条件之一。

---

## Copywriting Contract —— 本阶段改动零文案

**`04-UI-SPEC.md` 的 `## Copywriting Contract` 继续有效,其冻结原样成立。** 本阶段是纯 CSS 改动,
`app.js` / `index.html` 零改动,因此**不可能**引入或修改任何面向用户的字符串。

| Element | 本阶段状态 |
|---|---|
| Primary CTA | 冻结(`进入` / `发送`)—— 不变 |
| Routine loop action | 冻结(`处理本轮批注` / `继续自检` / `继续修复`)—— 不变 |
| Commit action(G1) | 冻结(`认可雏形`)—— **视觉形态变为实心填充**,文案不变 |
| Irreversible action(G3,核心价值红线) | 冻结(`授权撰写总设计文档`)—— **视觉形态变为实心更深 + 16px + 600**,文案不变 |
| Empty state | 冻结 —— 本阶段不新增、不修改任何空态 |
| Error state | 冻结 —— `showInlineError` 的 `textContent`-only 规则在 Do-Not-Touch 清单上 |
| Destructive confirmation | 本阶段**不新增**任何破坏性动作,也不给现有动作增加或移除确认步骤 |

**两条必须继续成立的文案规则(不得在本阶段被削弱):**

1. **错误文本永不通过 `innerHTML` 渲染。**(T-260916-01,安全缓解措施,不是风格选择)
2. **G3 授权按钮的标签是核心价值红线唯一的文字。** 它的对比度是**唯一一对不得为美观让步的配对** ——
   本阶段把它从 11.00(淡底绿字)改成 4.72(实心白字),**仍然通过,但余量从 6.5 降到 0.22**。
   计划必须把 `--color-action-commit-fg ON --color-action-commit-surface` 与
   `--color-action-irreversible-fg ON --color-action-irreversible-surface` 两条配对**逐字抄进计划的验收命令**。

**两个新字形是纯装饰性的、与相邻文字同色,不承载文字信息**(`.annotation-quote` 的引用文本与
`.verdict-location` 的位置文本本身完整)。因此不产生替代文本 / `aria-label` 义务 —— 它们不是
`<img>`,也不在 DOM 里。

---

## Deliberate Delta Ledger(本阶段)

**本阶段每一项有意的视觉变化,一张表。不在此表上的变化即回归。** 这是把「纯 CSS 排版与层级阶段」
变成可核而非可断言的东西。

| # | Delta | 站点 | 幅度 | 为什么 |
|---|---|---|---|---|
| **P-1** | `--text-2xl` / `--text-3xl` 两个新档(22 / 28) | 围栏 | 新令牌 | D-06 / D-07。**各有一个消费者,同提交** |
| **P-2** | `.markdown-body h1` 24 → 28px | `:624` | +4px | D-06 —— 文档 h1 成为全屏最大文字(SC3) |
| **P-3** | `.markdown-body h2` 18 → 22px | `:625` | +4px | D-06 |
| **P-4** | `.markdown-body h3` 16 → 18px | `:626` | +2px | D-06 |
| **P-5** | `--color-action-commit-surface` green-3 → **green-11** | 围栏 | 淡底 → 实心 | D-11 commit 档 |
| **P-6** | `--color-action-commit-fg` green-12 → **`--white`** | 围栏 | 绿字 → 白字 | D-11 |
| **P-7** | `--color-action-irreversible-surface` green-3 → **green-12** | 围栏 | 淡底 → 实心更深 | D-11 irreversible 档 |
| **P-8** | `--color-action-irreversible` green-11 → **green-12** | 围栏 | 边框随填充 | D-11「实心更深」的边界与填充同色 |
| **P-9** | `--color-action-irreversible-fg` green-12 → **`--white`** | 围栏 | 绿字 → 白字 | D-11 |
| **P-10** | `--color-marker-active` 新 tier-2 令牌 → `--radix-blue-11` | 围栏 | 新令牌 | D-18。**已声明、已消费的 primitive,零新增 primitive** |
| **P-11** | 活动面板:左侧 3px 蓝竖条 + 标题变蓝 | 3 条追加规则 | 新增 | D-16 / D-17 |
| **P-12** | `#btn-authorize` `font-size` 14 → 16px(`--text-md`) | `:928-934` | +2px | D-13 |
| **P-13** | 五条动作按钮规则的字重 600 → 500 | `:654` `:882` `:945` `:1003` | 字重 | D-09 |
| **P-14** | 两处 `::before` 的 emoji → mask 字形 | `:836` `:1021` | 机制 | D-20 / D-21 / D-22 |
| **P-15** | `--icon-pin` / `--icon-location` 两个新令牌 | 围栏 | 新令牌 | D-20。**各有一个消费者,同提交** |
| **P-16** | `--text-*` 刻度 5 → 7;`--fw-medium` 消费 4 → 8、`--fw-semibold` 12 → 8 | 围栏 | 记账 | D-06 / D-09 |
| **P-17** | 围栏注释重写 4 处 + 清单注释重写 1 处 | 围栏 | 零渲染 | `style.css:42-45`(9/10 预告)、`:204`(5 档)、`:217`(整数配对)、`:311`(三族一值) |
| **P-18** | `check-05-ui-uat.py` 断言按 D-03 分类、按 D-04 反转 | `scripts/` | 零渲染 | D-02 / D-03 / D-04 |
| **P-19** | chrome 标题选择器由**后代形态**收窄为**子组合器 / id 形态**(**补记**) | `:704` `:775` | 2 条规则 / 3 个选择器名 | 层叠修复。原形态 `#draft-view h2, #rounds-placeholder h2` 与 `#brainstorm-view h2` 是 1-0-1 **后代**选择器,会伸进 `.markdown-body` 容器把 `.markdown-body h2`(0-1-1)**无条件**压回 chrome 字号(ID 列胜过类列,与源码顺序无关);改用子组合器 / id 形态(`#draft-view > h2, #round-title` 一条,`#brainstorm-view > h2` 一条)后两者在层叠上永不相遇,22px 才在三个宿主上可达。原形态的三个选择器名里,`#rounds-placeholder h2` 被换成 `#round-title`。**必须写明这是「补记」**:该改动发生在 plan 01 的执行期(已登记在 §字号刻度的范围栅栏 的订正记录、`.planning/WINDOWS.md` 第 15 条与 `idi-05-01-SUMMARY.md`),但此前**没有 P-item** —— 按本 ledger 自己的规则(「不在此表上的变化即回归」),未登记的改动会让审计者在全阶段最承重的一次编辑上拿到**假阳性**。这正是 `G-idi-05-1` 的 `missing` 第 3 项 |
| **P-20** | 五个非 `.markdown-body` 渲染目标的**嵌入标题刻度** | 文件末尾追加的 3 条规则 | `.chat-bubble` 上下文 h1 32 → 24、h2 24 → 18、h3 18.7 → 16;`.event-content` 上下文 h1 28 → 24、h2 21 → 18、h3 16.4 → 16;字重一律 700 → 600 | `G-idi-05-1` —— `renderMarkdown()`(`app.js:112`)的返回值被注入这五个容器(`.event-content` / `.chat-bubble` / `.say-chunk` / `.annotation-note` / `.annotation-answer-body`),而它们**不是** `.markdown-body`,故标题回落 UA 默认值:既超过 `.markdown-body h2`(22px)又与文档 h1(28px)持平或反超,使 SC3 的「文档 h1 是全屏最大最重的文字」为假,并把第四个字号档与**第四个字重档 700** 带进只声明三档(400 / 500 / 600)的应用。取值规则是「沿契约**数值**阶梯下移一档」(`--text-3xl` 28 → `--text-xl` 24、`--text-2xl` 22 → `--text-lg` 18、`--text-lg` 18 → `--text-md` 16,**按数值序不按名字序**),三档全在既有七档内,**零新增令牌** |

**不在本 ledger、且必须是零的:** 任何既有选择器的位置 / 名字 / 声明增删(除 P-2…P-4、P-12 / P-13、
**P-19** 与 **P-20** 点名的那些);任何 `--space-*` / `--radius-*` / `--lh-*` / `--z-*` 的声明改动;`.hidden` 规则;
`!important` 声明数;任何 `@media`;`app.js` / `index.html` / `frontend/vendor/` 的任何字节。

**P-19 与 P-20 各属零列表的哪一类(两者必须分开写,否则读者会以为 P-20 越过了零列表):**
**P-19 是「既有选择器的名字改动」** —— 正是零列表原本要拦的那一类(它改的是 `:704` / `:775` 两条既有规则的
选择器形态,声明体一字未动),故必须在这里点名除外。**P-20 是「新增规则」** —— 它不在零列表的字面范围内
(零列表管的是既有选择器的增删改名,而 P-20 是文件末尾的三条追加规则),但必须一并点名,否则读者会以为
它越过了零列表。两者的共同点是:都只由 `G-idi-05-1` 产生,不是顺手做的其他事。

---

## 契约修正登记(全部由已锁定决策产生,不是新问题)

| # | 修正 | 依据 | 影响 |
|---|---|---|---|
| **A-1** | **字面量例外 L-3 整个撤掉**(原:「两个 `--icon-*` data-URI 内的转义 hex」) | D-20 | mask 只看 alpha ⇒ `<path>` 不带 `fill` ⇒ data-URI 内**零颜色信息**。L-3 不再有需要豁免的对象。**撤掉后剩余例外 L-1 / L-2 / L-4 / L-5 不变** |
| **A-2** | **`04-UI-SPEC.md` Q7 的机制被替换**:`content: var(--icon-*)` → `mask-image` + `background-color` | D-20 | Q7 的三条约束中,第 1 条(为什么不是 DOM `<svg><use>`)与第 3 条(为什么不是 `.collapse-indicator`)**继续成立**;第 2 条(为什么是 `%23555555` 而非 `currentColor`)**整条作废** |
| **A-3** | **`04-UI-SPEC.md` Q2 的填充步从契约候选改为 green-11 / green-12** | D-11 的委派 + 04.1 的算术 | 见 §Color 与 S-7。**Phase 5 新增 tier-1 primitive = 0** |
| **A-4** | **围栏注释 `style.css:42-45`「Phase 5 declares the 9/10 fill steps」作废** | 同上 | 该注释必须重写为「Phase 5 复用已声明的 11/12 步,理由见本围栏的 role-band 记录」 |
| **A-5** | **REQUIREMENTS.md 的 VISUAL-04 措辞收窄为「三选一活动态 + AI 面板折叠态」** | D-16 | **不改 `REQUIREMENTS.md`**(改它会作废指纹),只在计划与验证记录里登记 |
| **A-6** | **`--text-2xl` 名同值不同**(契约 18px,现 22px) | D-07 | 围栏注释必须写明,否则日后对照契约必然困惑 |
| **A-7** | **60/30/10 的 Accent 域**:活动面板标记的**承载令牌**从 `--color-action-primary` 改为新令牌 `--color-marker-active` | D-18 | **元素清单与颜色值都不变**(blue-11 就是 `--color-action-primary` 的值),只有名字变。accent 面积占比不受影响 |
| **A-8** | **D-05 的连带义务**:本阶段编辑 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`,两者都在 `idi-04.1-radix` 的 `covered_files` 里 | D-05 | **必须在同一批内复验 04.1** —— 见 §四条命令的扩展 |
| **A-9** | **硬规则 9 与 REQUIREMENTS 的 TYPE-01 里「作用域限定在 `.markdown-body` 内」这一句,按 `G-idi-05-1` 收窄为「不得写全局标题规则;`renderMarkdown()` 的每个渲染目标必须在 style.css 侧逐个列举」** | `G-idi-05-1` 的 truth 与 `missing` 第 1 项 | 硬规则 9 的**原字面**禁止了本缺陷唯一的 CSS 侧修法 —— 它把「不得写全局规则」这条**正确的意图**,写成了「不得给 `.markdown-body` 容器之外的任何 `h1` / `h2` / `h3` 写字号规则」这条**会自相矛盾**的措辞:缺陷本身正是「`.markdown-body` 之外的标题无人管」。**A-9 收窄的是措辞,不是意图** —— 全局规则仍然禁止,禁止的理由仍是原第 9 条自己写的那半句(它对四处 chrome 覆盖与 `.markdown-body` 都惰性,只会命中「落在 `.markdown-body` 之外又没有更具体规则兜底的标题」,而那正是这五个容器)。**TYPE-01 的需求行不改**(改 `REQUIREMENTS.md` 会作废指纹,与 **A-5** 同型处置),只在计划与验证记录里登记 |

---

## Sign-Off Items(S-7 / S-8 —— 需要用户裁定,不是 checker 裁定)

`04-UI-SPEC.md` 的 **S-1…S-4** 与 `idi-04.1-UI-SPEC.md` 的 **S-5 / S-6** **均已签核**;
**不得重开,任何一行式替代方案不得执行。** 下面两条是**新的**,各自附一行式替代方案与代价。

| # | 项 | 偏离了什么 | 为什么这样取 | 一行式替代方案 |
|---|---|---|---|---|
| **S-7** | **两个实心填充步落在 green-11 / green-12,不是契约与围栏注释预告的 green-9 / green-10。** 连带:**Phase 5 新增 tier-1 primitive = 0** | `04-UI-SPEC.md` Q2 的候选 hex 表;`style.css:42-45` 的「Phase 5 declares the 9/10 fill steps」预告;D-11 的括注 | **D-11 明文把「具体取哪两个步」委派给规划期**(「具体取哪两个步由规划期定(契约候选 hex 已被 04.1 V-13 删除)」)。而 04.1 的算术已经把 9/10 排除:white on green-9 = **3.16 ✗**、green-10 = **3.55 ✗**,green-11 = **4.72 ✓** 是**最浅的通过步**(Pitfall 4a 应用在填充上),green-12 = 12.32 是最深步。「实心更深」的语义要求 commit 取较浅的通过步、irreversible 取最深步 —— 11 与 12 是唯一满足两条约束的分配 | 改用 green-9 / green-10 作填充 —— **代价:`scripts/check-02-contrast.py` 立即报两条 TEXT 失败(3.16 / 3.55),即两个按钮的白字低于 AA。** 若同时把文字改成深色以救回比值,则「实心填充 + 白字」的形态契约当场失效,且两档之间只剩色深差异 |
| **S-8** | **`.hint` 以两个不同字号渲染(`#confirm-error` 16px,其余 `.hint` 14px),本阶段不修** | 无 —— 这是一条**未登记的既有不一致**,由 `idi-04.1-UI-REVIEW.md` Pillar 4 记分时发现(3/4) | **它不在 TYPE-01/02/03 的任何一条字面范围内**,也不在 05-CONTEXT 的 22 条决策里。ROADMAP §Backlog `999.1` 明确警告过:**向 Phase 5 插入新交付物等于改写已签核的门**。根因是层叠而非排版:`.overlay-card p`(0-1-1)压过 `.hint`(0-1-0),`#confirm-error` 因此拿到 `--text-md` | 给 `#confirm-error` 补一条显式 `font-size: var(--text-base)`(1-0-0,压过 `.overlay-card p`),或把 `.hint` 提到 0-1-1。**代价:本阶段多一条围栏外声明、多一条必须复验的断言,且它触碰的是 G3 授权确认弹窗的错误路径 —— Pitfall M6 点名的那条路径。** 本契约**建议不在本阶段动它**,而把它与 backlog `999.1` 的第 2 项(陈旧诊断文案)合并为同一批 |

**两条都不阻断执行。** 它们被呈上是因为各自收窄或绕开了一条已锁输入,而那是**用户**的裁定权,不是
checker 的。**S-7 是必须让用户看到的** —— 它是本阶段唯一一处「契约写的步被算术推翻」的落地决策。

---

## The Four Contract-Check Commands —— 复述 + 本阶段的扩展

四条命令的规格见 `04-UI-SPEC.md`(§The Four Contract-Check Commands)。**本阶段不改它们的行为,
只增加对它们的调用点。** 四条都是**补充而非替代** —— 每个 `style.css` 计划仍须带**至少一项运行时验证**
(硬规则 7:`grep -c 'var(--'` 对渲染结果零证明力)。

| 命令 | Phase 5 的期望 |
|---|---|
| `bash scripts/check-01-token-conformance.sh` | `PASS` / exit 0 —— **围栏外裸 hex 仍为 0;tier-1 名仍不出围栏**(新令牌 `--color-marker-active` 是 tier-2,不触发 tier-1 泄漏;两个 `--icon-*` 是围栏内的字面量,合法) |
| `python3 scripts/check-02-contrast.py` | `PASS: 0 failures` over **47 对(35 TEXT + 12 NON-TEXT)+ `ORDER`**,exit 0。**清单规模 43 → 47** |
| `bash scripts/check-03-hidden-uniqueness.sh` | `PASS` —— `^\.hidden {` 仍为 **1** |
| `bash scripts/check-04-important-count.sh` | `PASS` —— `!important;` **声明**数仍为 **1**(算术陷阱:`grep -c '!important'` 返回 3,其中 2 行是 L13-14 的注释散文) |

**本阶段新增的两条专用门(零依赖、可独立运行):**

```bash
# Gate 5 —— mask 数据 URI 内零颜色信息(A-1 撤掉 L-3 的唯一依据)
# PASS: 打印 0
grep -oE '%23[0-9a-fA-F]{3,8}' frontend/style.css | wc -l

# Gate 6 —— .collapse-indicator 零改动(D-23 / 硬规则 5 的不得触碰清单)
# PASS: 该选择器的规则行与 HEAD 逐字节相同
git diff --exit-code HEAD -- frontend/style.css >/dev/null || true
grep -n '^\.collapse-indicator' frontend/style.css   # PASS: 恰好 1 行,内容为 { font-size: 20px; line-height: 1; }
```

**两条既有门继续逐计划跑(`04-UI-SPEC.md` 的 Gate 2 / Gate 3):**

```bash
# Gate 2 —— 每个被消费的自定义属性都已声明(抓 var() 静默失效的拼写错误)。PASS: 空
comm -23 \
  <(grep -o 'var(--[a-z0-9-]*' frontend/style.css | sed 's/var(//' | sort -u) \
  <(grep -o '\-\-[a-z0-9-]*:' frontend/style.css | sed 's/:$//' | sort -u)

# Gate 3 —— 零新增安装面。PASS: 空 / marked.min.js only
git status --porcelain frontend/ | grep -v 'style.css\|index.html\|app.js'
ls frontend/vendor/
```

**`check-05-ui-uat.py` 的断言变更清单(D-02 / D-03 / D-04)—— 计划必须逐条落:**

| 位置 | 变更 | 类别 |
|---|---|---|
| `:689-695` | **反转**为「三档两两不同 + 档内相同」 | D-04 |
| `:742` | `#brainstorm-view h2 font-size` → 令牌接线(`--text-md`) | D-02 / D-03 |
| `:746` `:745` `:747` `:751` `:760` `:800-807` | **保持字面 px**(四处 chrome + `.markdown-body` 16px + `--text-base` 14px + `.markdown-body code` 14px) | D-03 |
| 新增 | `.markdown-body h1/h2/h3` font-size == `--text-3xl` / `--text-2xl` / `--text-lg`(令牌接线) | P-2…P-4 |
| 新增 | `#btn-authorize` font-size == `--text-md`、font-weight == `600` | P-12 / D-12 |
| 新增 | 五只按钮 font-weight == `500`(`#btn-approve-draft` / `#btn-process-round` / `#btn-start-writing` / `#btn-continue-check` / `#btn-continue-repair`) | P-13 / D-09 |
| 新增 | `#doc-panel-header h1` font-size == `14px` 且 font-weight == `500`(**VISUAL-03 的守卫,保持字面**) | D-19 |
| 新增 | 活动态标记:`p1` → `#session-panel .panel-header` 的 `box-shadow` 含 `inset 3px 0 0` + `--color-marker-active`;`p3` → `#annotations-panel`;`checking` → `#checks-panel`;且 `#ai-panel .panel-header` 的 `box-shadow == none` | P-11 / D-16 |
| 新增 | 活动面板标题 color == `--color-marker-active`(三条) | P-11 |
| 新增 | 两处 `::before` 的 `width` / `height` == `12px`、`background-color` == `--color-text-secondary`、`mask-image != none` | P-14 |

**D-04 的反转形态(计划照抄):**

```python
# 三档两两不同 + 档内相同。一个断言同时覆盖 VISUAL-01 与 VISUAL-02。
# 档内相同那一半同样承重 —— 它能抓到「改错了一只」。
ROUTINE = ("#btn-process-round", "#btn-continue-check", "#btn-continue-repair")
COMMIT = ("#btn-approve-draft", "#btn-start-writing")
IRREVERSIBLE = ("#btn-authorize",)

def trio(page, sel):
    return (read_style(page, sel, "color"),
            read_style(page, sel, "border-top-color"),
            read_style(page, sel, "background-color"))

# 档内相同
ok_true(item, "routine 三只三属性逐字节相同", len({trio(page, s) for s in ROUTINE}) == 1, ...)
ok_true(item, "commit 两只三属性逐字节相同", len({trio(page, s) for s in COMMIT}) == 1, ...)
# 三档两两不同
r, c, i = trio(page, ROUTINE[0]), trio(page, COMMIT[0]), trio(page, IRREVERSIBLE[0])
ok_true(item, "routine / commit / irreversible 三档两两不同",
        len({r, c, i}) == 3, "3 distinct triples", f"{len({r, c, i})}")
```

**为什么这个断言在 `p3` 一个状态里就成立:** 六只按钮**全部常驻 DOM**(`index.html` 里都存在,
只是各自的祖先被 `.hidden` 藏住),而 `getComputedStyle` 对 `display: none` 的元素**仍返回解析后的
computed 值**(`color` / `background-color` / `border-color` 不依赖布局)。`check-05` 现在就已经在 `p3`
里读 `#btn-authorize` 而不检查其可见性 ✓

---

### D-05 连带义务 —— 本阶段必须复验 `idi-04.1-radix`

**`frontend/style.css` 的任何编辑都会作废 `idi-04.1-radix` 的 `passed` 指纹。** 其 `covered_files`
(见 `idi-04.1-VERIFICATION.md` frontmatter)含:

| covered file | 本阶段是否改动 |
|---|---|
| `frontend/style.css` | **改**(围栏内 + 围栏外) |
| `scripts/check-05-ui-uat.py` | **改**(D-02 / D-03 / D-04) |
| `scripts/check-01-token-conformance.sh` | 不改 |
| `scripts/probe-05-resolve-color.py` | 不改 |
| `.planning/REQUIREMENTS.md` | 不改 |
| 四对 `idi-04.1-0N-PLAN.md` / `-SUMMARY.md` | 不改 |

`covered_digest` 是**原始字节 sha256**,因此两个文件一改,指纹即 stale。

**义务(不是建议):** 本阶段必须**在同一批内**复验 `idi-04.1-radix` —— 逐条重跑其
`human_verification` 的三项与四条守卫,并**从 HEAD 重算全部数值**(而不是补指纹)。理由与
`idi-04` 复验收口的先例一致:本次 stale 的成因是**内容真变**(本阶段重写了 04.1 覆盖的文件),
故走**重新验证**而非补指纹。

**复验时必须逐条确认的三处 04.1 结论未因本阶段的值改动而失效:**

| 04.1 的结论 | 本阶段是否触碰 | 复验动作 |
|---|---|---|
| 43 对清单全 PASS + `ORDER 0.363` | **清单规模变 43 → 47**;`ORDER` 的两个操作数(`--color-text-muted` / `--color-text`)本阶段未改值 ⇒ `ORDER` 应仍为 **0.363** | 重跑 check-02,核对 47 对与 `ORDER` 数值 |
| `--color-text-info ON --color-surface-info` = **4.53**(0.03 余量) | 未触碰 | 重跑 check-02,该行须逐字不变 |
| 冻结轮:`opacity 1` + `filter saturate(0.6)` + `inset 3px 0 0 --color-action-warning` | 未触碰(本阶段新增的活动态竖条是**另一个**元素上的同形声明) | `check-05 --item 2` 须仍 PASS |
| `--color-border-strong` = `--radix-gray-9`,实测 3.24 / 3.15 | 未触碰 | check-02 两行须逐字不变 |
| 25 tier-1 / 47 tier-2 的**数量** | **tier-1 仍 25**(新增 primitive = 0);**tier-2 47 → 48**(新增 `--color-marker-active`) | 重数并记录 |

**注意 `--color-*` 的数量从 47 变 48** —— 这是 04.1 的 `## Color` 节里「47 个 tier-2」这一句在
本阶段之后不再成立的地方。**不改 04.1 的文件**(改它会作废它自己的其余结论),在复验报告里登记该差值。

---

## Global Hard Rules(每个 Phase 5 计划都适用,来源:`04-UI-SPEC.md` + `ROADMAP.md`)

1. `grep -c '^\.hidden {' frontend/style.css` **必须等于 1**。`.hidden { display: none !important }`
   是**机制而非样式**:不得令牌化、不得移动、不得弱化、不得用 `:where()` 降特异性。它现在承载
   **六个**元素(`#draft-empty` / `#rounds-hint` / `#btn-process-round` / `#round-switcher` /
   `#writing-hint` / **`#session-panel`**),三个竞争者(`#selection-menu` / `#annotations-panel` /
   `#checks-panel`)靠 **ID 特异性 1-0-0** 取胜。
2. `style.css` 中含 `!important` 的**声明行**数为 1。**算术陷阱:**`grep -c '!important'` 返回 **3**,
   其中 2 行是 L13-14 的注释散文。写 gate 时按「声明」计数(`!important;`)。
3. **追加,不重排。** `#draft-view h2`(`:611`)与 `#brainstorm-view h2`(`:679`)同为 1-0-1,后者
   靠源码顺序取胜 → 16px / `--color-action-warning`。**重排即渲染变更,而源码 diff 看起来完全无辜。**
   本阶段的三条活动态标记规则与两处 `::before` 改写都不得改变任何既有规则的相对顺序。
4. 不得新增 `!important`;不得令牌化 `display`;不得引入 `@layer` / `@property` /
   `var(--x, #fallback)`(前三者都会重新打开 `.hidden` 的特异性竞速,第四者会重建第二事实源)。
   **本阶段新增 0 条 `!important`。**
5. **不得触碰:** `.fatal` 修饰符(`#stream-banner` 的两态必须仍可区分)、`applyArchiveView` 的两行
   (`app.js:817-818`)、`#selection-menu` 的 DOM 位置(必须是 `<body>` 直接子元素)、
   `showInlineError` 的 `textContent`-only 规则、`renderAnnotations` / `renderVerdictCard`、
   `app.js:4-75` 的约 70 个顶层 `getElementById` 句柄(id 不得改名或删除)、
   **`.collapse-indicator`(本阶段新增,见 D-23)**。
6. 零新增运行时依赖、零构建步骤(D-06)。**本阶段新增 0 个依赖、0 个文件。**
7. 每个 `style.css` 计划都必须带**至少一项运行时验证**,不能只有静态计数。
8. **【本阶段新增】不得引入 `@media`。** 窄窗口与断点是 Phase 6 的交付物(`@media` 计数须保持 **0**)。
9. **【本阶段新增,按 `G-idi-05-1` / A-9 收窄措辞】** 不得写**裸类型选择器**的全局标题规则
   (三个标题类型选择器各自单独成条,或合并成一条;特异性 0-0-1)。凡给 `.markdown-body` 之外的
   标题写字号规则,**必须在同一次提交里把 `renderMarkdown()` 的全部注入目标列进选择器表**,
   并让 check-05 的枚举(按调用点)与之一一对应。原字面写的是「不得给 `.markdown-body` 容器之外的
   任何标题写字号规则」—— 那条措辞**自相矛盾**:本缺陷正是「`.markdown-body` 之外的标题无人管」,
   照字面读会把唯一的 CSS 侧修法也一并禁掉(见 A-9)。**收窄的是措辞,不是意图。**
   - **(a) 为什么禁止全局规则。** 它的特异性 0-0-1,严格弱于四处 chrome 覆盖(`#draft-view > h2` /
     `#brainstorm-view > h2` 为 1-0-1,`.panel-header h2` / `.overlay-card h3` 为 0-1-1)与
     `.markdown-body` 的标题规则(0-1-1),所以在 `font-size` 上它对那五处**是惰性的** ——
     于是它**只会**命中「落在 `.markdown-body` 之外、又没有更具体规则兜底的标题」,
     而**那正是 `G-idi-05-1` 的五个容器**。一条全局规则会让它们暂时变对,却把「哪些容器受影响」
     这件事重新变成**不可枚举**;而且它无法表达三档各不相同(那要写成三条全局规则),
     三条全局规则会把**任何将来的标题**一并捕获 —— 那正是本缺陷的成因。
   - **(b) 因此本阶段的形态是逐容器列举。** 给 `.markdown-body` 之外的标题写字号规则时,
     选择器表必须列全 `renderMarkdown()` 的注入目标(本阶段为 9 个:四个 `.markdown-body` 宿主 +
      §字号刻度的范围栅栏 的「渲染目标影响面」表所列五者),并让 check-05 的 `MARKDOWN_TARGETS`
      (按调用点枚举,附调用点普查守卫)与之一一对应 —— 枚举才是可核的:门能把枚举逐条对照
     `app.js` 的调用点,全局规则不能。
   - **(c) 可机械核的形态(门必须写成这两条,不能只写措辞)。**
     `grep -oE '(^|,)[[:space:]]*h[123][[:space:]]*[,{]' frontend/style.css` 必须为 **0**;
     五个嵌入容器的 `h1` / `h2` / `h3` 各恰出现 **3** 次。
   - **原来的第三段理由保留并追加一句:** 真正的暴露面是四处 chrome 规则**未声明的那些属性**
     (`line-height` / `margin-bottom` / `letter-spacing`),以及**任何落在 `.markdown-body` 之外、
     又没有更具体规则兜底的标题**。**那半句已经点出了暴露面,却没有把暴露面枚举出来** ——
     `G-idi-05-1` 就是只读这半句、没做枚举的结果。
   - **引用登记(quick `260925-iin`):** 本次新增的 `--text-lg-plus`(20px)与 `--lh-none`(1)
     **只被 `.collapse-indicator` 消费** —— 未新增任何标题字号规则、未新增任何 `.markdown-body`
     之外的目标,故**本条(第 9 条)不受影响**。

---

## Do-Not-Touch List(继承 + 本阶段追加)

`04-UI-SPEC.md` 的整张清单**原样有效**。本阶段追加四条:

| Artifact | Rule |
|---|---|
| **`.collapse-indicator`(`style.css:434`)** | **已由 quick `260925-iin` 令牌化(值不变,仍 20px):** `font-size` / `line-height` 两个声明值改为 `--text-lg-plus` / `--lh-none`。`textContent` 赋值路径与「不得内联 `<svg>`」**仍不得触碰**。backlog `999.1` 第 1 项由此关闭 |
| **`scripts/check-02-contrast.py`** | **本阶段零代码改动。** 它从围栏读清单;清单变而代码不变正是它的设计。改它会破坏「值层改动不产生假 FAIL」这条 04.1 已立的性质 |
| **`#ai-panel` 与 `#doc-panel` 的折叠行为** | `app.js:1561-1570` 的两处 `classList.toggle('collapsed')` 与两处 `textContent` 赋值**零改动**。VISUAL-04 对 `#ai-panel` 的处置是「承认既有 `▾`/`▸` 指示器已构成可辨状态」,与该元素**零交互** |
| **`--color-action-irreversible*` 的消费者集合** | **只被 `#btn-authorize` 消费,永不出现第二个消费者**(D-15)。本阶段改了它的**值**,没改它的**消费者** —— 这两件事必须分别核对 |

---

## 不在本阶段(范围锁 —— Pitfall 8)

**一个不能引用里程碑目标特性的任务就是范围外。**

| 项 | 理由 | 状态 |
|---|---|---|
| **`.collapse-indicator` 的 `font-size: 20px` / `line-height: 1`** | backlog `999.1` 第 1 项。ROADMAP Phase 5 的 Pitfall 7 把触碰该元素的范围锁死为两处 `content:` emoji;插入新交付物等于改写已签核的门。**规划时二者不得互相覆盖**(D-23) | 不在本阶段 |
| **`scripts/check-05-ui-uat.py:588` 的陈旧诊断文案** | backlog `999.1` 第 2 项,与上一项合并为同一批处理。**注意:** 本阶段会编辑该脚本(D-03 / D-04),因此 999.1 原定的「合并以省一次 04.1 复验」理由已不再成立 —— **但已锁决策不改**,本阶段仍不修它。**这是给用户的观察,不是本阶段的交付物** | 不在本阶段(见 05-N-6) |
| **`.hint` 的双字号不一致(`#confirm-error` 16px)** | 见 **S-8**。不在 TYPE-01/02/03 的字面范围内;修它会触碰 G3 授权确认弹窗的错误路径(Pitfall M6 点名) | 不在本阶段(S-8) |
| **hover / active / transition** | `INTERACT-01` / `INTERACT-02`,Phase 7。**本阶段不新增任何 hover 规则** —— 六只按钮因 ID 特异性本就无 hover 反馈(`button:hover` 是 0-1-1,输给 `#btn-*` 的 1-0-0),**不存在回归** | Phase 7 |
| **`:focus-visible` / 焦点环** | `A11Y-01`,Phase 7。04.1 的携带项 #8 要求环色在新地面(`--color-surface` `#f9f9f9` / `--color-surface-page` `#fcfcfc`)上重测。**本阶段不声明 `--color-focus`** | Phase 7 |
| **布局结构常量 / 窄窗口 / 滚动容器 / 24×24 命中区** | `LAYOUT-01…04` / `A11Y-07`,Phase 6。**本阶段不引入 `@media`**(硬规则 8) | Phase 6 |
| **暗色模式 / `prefers-color-scheme`** | v2 `TOKEN-V2-01`,v1.14 全局已裁定排除 | 不在 v1.14 |
| **图标库 / SVG sprite 体系 / 图标字体 / 任何第三方包** | REQUIREMENTS §Out of Scope。VISUAL-05 用两个 `mask-image` 数据 URI,零新文件 | 不在 v1.14 |
| **`.overlay-card h3` 的 24px 与 `.markdown-body h2` 的 22px 的相对关系** | 模态高于正文标题是合理的;若要调,属排版刻度的再平衡,是独立阶段 | 不在本阶段 |
| **`#brainstorm-content` 内 h2(22px)大于其容器标签(16px)** | chrome 标题与内容标题是**两个令牌族**,其相对大小不由本阶段调和(与上一条同源) | 记录,不处理 |
| **`#probe-controls` 的移除 / 重定位** | 产品行为变更;双路线界面契约(AI-03 / D-06)是真功能。v1.14 全局已裁定不进任何阶段 | 独立未来候选 |
| **两处 `window.prompt` 替换 / 响应式断点系统 / 骨架屏 / 动效体系 / Storybook / lint 工具链** | `04-UI-SPEC.md` §Not in v1.14 表 | 不在 v1.14 |

---

## Notes(05-N-1 … 05-N-7)

- **05-N-1 —— `--text-2xl` 名同值不同,是本契约最容易被"修正"回去的一处。** 契约表写
  `--text-2xl: 18px`,本契约写 22px。**这不是笔误**:18px 在 HEAD 上已被 `--text-lg` 占用,而
  D-07 要求继续跟随尺寸递进命名法,于是 2xl 只能是 xl(24)之上的下一档 22px。**任何把 2xl 改回
  18px 的"修正"都会让 18px 有两个令牌名(2xl 与 lg),即第二事实源。** 围栏注释必须写明这一点。

- **05-N-2 —— `--color-marker-active` 的 4.65 余量只有 0.15,不得"为了更保险"而换步。**
  blue-11 在 `--color-surface-page` 上实测 4.65,同时满足 TEXT(≥4.5)与 NON-TEXT(≥3)。它是本族
  唯一同时满足两条阈值的可用步:blue-2/3 太浅(竖条与标题都不可辨),blue-12 会把标题变成深海军蓝
  并放弃「最浅通过值」规则。**这与 04.1-N-3(`--color-text-info` 的 0.03 余量)是同一类陷阱的
  第二次出现** —— 项目已记录的方法论是:**薄的余量不是缺陷,是「最浅通过值」规则的代价;加深它
  才是违反规则。** `check-02` 是仲裁者,4.65 ≥ 4.5 通过。

- **05-N-3 —— `--color-action-commit-fg` 的余量从 6.5 掉到 0.22,这是本阶段对核心价值红线最大的
  一次赌注。** 淡底绿字时代该配对是 11.00;实心白字时代是 4.72。**它仍然通过,但余量只剩 0.22。**
  这是 D-11「实心填充 + 白字」形态的**必然代价**:Radix 的 green 族在 11 步上对白字给的就是 4.72。
  **不得为了拉大余量而把填充退到 green-12**(那会让 commit 与 irreversible 两档同色,
  「实心更深」的语义当场失效),**也不得把白字改成绿字**(那会退回淡底形态)。**唯一允许的动作是
  把这两条配对逐字抄进计划的验收命令。**

- **05-N-4 —— 活动态标记落在 `.panel-header` 而不是 `<section>` 上,这条决定有实测依据。**
  三个 section 的子元素都带背景色(`.chat-bubble` / `.annotation-item` / `.event-list` /
  `.panel-body`),`box-shadow: inset` 画在元素自身的背景层上,**带背景的子元素会盖住左边缘的竖条**;
  标题行没有带背景的左边缘子元素。**这不是审美偏好,是层叠事实。** 若计划改成给 section 加竖条,
  必须先用运行时检查证明竖条在真实渲染里可见(而不是被 `#chat-messages` 或 `#annotation-list` 盖住)。

- **05-N-5 —— mask 方案的唯一实测风险是对齐,不是渲染。** `content: '📌 '` 是一个字形(由字体引擎
  决定基线),`mask-image` 是一个 12×12 的行内盒(由 `vertical-align` 决定基线)。**两者的基线行为
  不同**,所以 `vertical-align: -2px` 是从契约继承的**起点而非结论**。计划必须把「图标与相邻文字
  视觉基线对齐、且不撑高行盒」列为**实测项**(计算样式看不到这一项 —— 它需要看渲染结果)。
  **`-2px` 落在刻度外,但它是 `vertical-align` 的值而不是间距值**,不在 `--space-*` 族的覆盖范围内。

- **05-N-6 —— backlog `999.1` 的第 2 项其合并理由已消失,但已锁决策不改(给用户的观察)。**
  `999.1` 把「`.collapse-indicator` 的越轨字面量」与「`check-05-ui-uat.py:588` 的陈旧诊断文案」
  合并为一批,理由是**改后者也会作废 04.1 的指纹,故合并以省一次复验**。**本阶段已经会编辑
  `scripts/check-05-ui-uat.py`(D-02 / D-03 / D-04)并连带复验 04.1** —— 于是该理由不再成立,
  现在顺手修那行陈旧文案的边际成本是**零**(同文件、同一次复验)。**但 05-CONTEXT 的 `deferred`
  明写该项不在本阶段**,故本契约**不把它列为交付物**,只把这条观察呈给用户(S-8 的同一批)。
  **这不是范围蔓延的入口,是一条给用户的、成本已归零的选项。**

- **05-N-7 —— check-06 的 g2 对 `G-idi-05-1` 的五个容器是状态盲的,故它**不是**SC3 的机械依据。**
  g2 的判据是「可见元素里不存在比文档 h1 更大的字号」,而它的扫描面是**当前状态里已存在的可见
  元素**(`body *` 且有非零 client rect)。它只把探针注入四个 `MARKDOWN_HOSTS`(check-06:145-153),
  **从不造 `.chat-bubble` / `.say-chunk` / `.annotation-note` / `.annotation-answer-body`**,
  且 `p1` 的 fixture 里本来就没有 `.chat-bubble` —— 故「`p1` 下 g2 仍 PASS」**推不出**「五个嵌入容器
  的标题受控」。实测佐证:在 CSS 未改的 RED 状态下,g2 依然 PASS,而 item7 报 36 条 FAIL。
  **因此「嵌入 h1 不得取 28px」这条约束的机械形态在本阶段自己的 `item7` 里** —— 那里**先造容器
  再断言**(5 条「文档 h1 严格大于该目标 h1」的严格不等式),不依赖「fixture 恰好有内容」。
  g2 在本阶段的角色是**回归守卫**(必须仍 PASS),不是本条判据的担保者。
  **g2 自身扫描面的加固不在本阶段** —— 记录在此,以防日后被误读为「g2 已覆盖」。

---

## UI Considerations

> 由 ui-phase 的 UI-consideration probe(Step 9.5)填充,并由 plan-phase 的
> `## UI Considerations` lift 规则按与 SPEC `## Edge Coverage` 相同的规则提升。
> **本节由 probe 引擎在 checker 通过之后重算并整节替换**(幂等,不追加);元素集与 kind 由本契约
> 作者在 auto 模式下按分类法裁定(引擎检测到的 ∪ 作者判定被漏掉的)。

**适用状态考量已裁定:40 条(22 条 explicit、18 条 backstop、0 条 unresolved)。**

**probe 运行记录(可复核):**

```bash
node .claude/gsd-core/bin/lib/ui-consideration-probe.cjs <elements.json> <resolutions.json>
# → coverage: {"applicable":40,"resolved":40,"unresolved":0,"byVerification":{"explicit":22,"backstop":18}}
```

**首跑的分类失真(必须记录,否则会被误读成「引擎认同本表」):** 直接喂元素散文时,引擎把
**5/9 判为 `unclassified`**(E1–E5、E8)、把 E6/E7 判成 `media`(数据态,对一个静态字形无意义)、
把 E9 判成 `list-collection`;并且 `overflow` / `long-text` **一条都没提出** —— 而那恰恰是本阶段
(排版与层级)真正相关的两类。故按工作流的 propose-then-confirm,在 auto 模式下由作者逐条裁定
kind 后重跑。**上表 40 条是重跑结果,不是首跑结果。**

**本阶段的元素集与 kind(9 个):**

| # | 元素 | kind(engine) | 依据 |
|---|---|---|---|
| E1 | `.markdown-body` 的四个宿主(`#draft-content` / `#brainstorm-content` / `#round-doc` / `#latest-check`) | `static-content` | 渲染的 markdown 内容 |
| E2 | 文档 h1/h2/h3(`.markdown-body h1/h2/h3`) | `static-content` | 本阶段主动改字号 |
| E3 | 六个动作按钮(`#btn-approve-draft` / `#btn-process-round` / `#btn-authorize` / `#btn-start-writing` / `#btn-continue-check` / `#btn-continue-repair`) | `interactive-control`, `static-content` | 本阶段主动改形态 / 字重 / 字号 |
| E4 | 侧栏三面板标题行(`#session-panel` / `#annotations-panel` / `#checks-panel` 的 `.panel-header`) | `static-content`, `nav` | 本阶段新增活动态标记 |
| E5 | `#ai-panel` 的标题行与折叠指示器 | `interactive-control`, `static-content`, `nav` | 本阶段**零改动**,但它是 E4 的对照组 |
| E6 | `.annotation-quote` 的引用行(含 `::before` 图标) | `static-content`, `media` | 本阶段替换图标机制 |
| E7 | `.verdict-location` 的位置行(含 `::before` 图标) | `static-content`, `media` | 同上 |
| E8 | `#doc-panel-header h1`(容器标签) | `static-content`, `nav` | VISUAL-03 的复证对象 |
| E9 | 四处 chrome 标题(`.panel-header h2` / `#draft-view h2` / `#brainstorm-view h2` / `.overlay-card h3`) | `static-content`, `list-collection` | SC1 的守卫对象 |

**explicit 与 backstop 的分界线:** 本阶段改的是**排版与层级**,不新增元素、不新增状态、不改文案
(§Copywriting Contract 已冻结)。一个字号或一个 `box-shadow` 的值**不可能**改变某个状态的**内容、
结构或显隐** —— 那些一律 `explicit`,由接线证据钉住;但它**可以**改变某个状态下的**文字适配**
(换行、裁切、行盒高度),那些只能 `backstop`。空态 / 错误态的**文案**归 `## Copywriting Contract`,
本节只覆盖**形状根因的状态适配**并**引用**该节,不复述其文案。

**考量表(40 条):**

| Element | Category | Status | Resolution |
|---|---|---|---|
| E1 | `overflow` | ✅ `resolved` / backstop | 长文档在 `#draft-content` 内滚动而非撑破容器;本阶段只改标题字号,不新增滚动容器(布局归 Phase 6),此处只断言不回归。 |
| E1 | `long-text` | ✅ `resolved` / backstop | 超长 DESIGN.md 渲染后 `#doc-pane` 无横向滚动条,28px h1 不撑破内容宽。 |
| E2 | `overflow` | ✅ `resolved` / backstop | 28px h1 / 22px h2 在 `--doc-panel-w` 最窄值(340px)下不溢出容器。 |
| E2 | `long-text` | ✅ `resolved` / backstop | 含 h1/h2/h3 的长文档渲染后三级标题层级可辨且不互相淹没;h1 是全屏最大文字(28 > `.overlay-card h3` 的 24 > 22)。字号半边由 `check-05` 的令牌接线断言覆盖,剩余的是视觉层级判断。 |
| E3 | `loading` | ✅ `resolved` / explicit | 六只按钮的 loading 关联态由 `app.js` 既有句柄驱动;本阶段 `app.js` / `index.html` 零 diff,故态的结构、文案与显隐不可能改变 —— 本阶段只改 `font-weight` / `font-size` / 填充形态。 |
| E3 | `error` | ✅ `resolved` / explicit | 同上:`:disabled` 是 G3 前提条件唯一的视觉信号(Pitfall M5),D-14 裁定沿用 `opacity: 0.55` 零改动,错误态不可被本阶段改动。 |
| E3 | `overflow` | ✅ `resolved` / backstop | `#btn-continue-check` 与 `#btn-continue-repair` 在 `#check-controls`(`flex-direction: column`)里各占一行,不溢出。 |
| E3 | `long-text` | ✅ `resolved` / backstop | `#btn-authorize` 文本「授权撰写总设计文档」在 `--doc-panel-w` 最窄值 340px(内容宽 260px)下不换行、不裁切,且 16px 白字在 green-12 上可读(12.32)。换行半边无自动化证据,需实测。 |
| E4 | `loading` | ✅ `resolved` / explicit | 三面板的显隐由 `.hidden` 驱动(`app.js` 既有句柄);本阶段 `app.js` / `index.html` 零 diff,活动态由纯 CSS `:not(.hidden)` 推导,不引入新状态。 |
| E4 | `error` | ✅ `resolved` / explicit | 同上。CHECK-03(`^\.hidden {` = 1)与 CHECK-04(`!important;` = 1)钉住 `.hidden` 的唯一性,任何面板态的显隐结构不可能移动。 |
| E4 | `overflow` | ✅ `resolved` / backstop | 3px 竖条在**每个**活动面板上真实可见 —— 既不被该面板标题行内的元素盖住,也不因 `border-radius: var(--radius-md)` 在角落断开。这是 05-N-4 的实测验收。 |
| E4 | `long-text` | ✅ `resolved` / backstop | 面板标题文本变长时竖条仍贴左缘,标题变色(标记色)不溢出标题行。 |
| E5 | `loading` | ✅ `resolved` / explicit | `#ai-panel` 的折叠态由 `#ai-panel-body` 上的 `.collapsed` 驱动(`app.js:1563-1569`),本阶段零改动;它从不被 `.hidden`,故不参与三选一活动态推导(D-16)。 |
| E5 | `error` | ✅ `resolved` / explicit | 同上 —— `#ai-panel` 的折叠行为按 SC4 要求保持不变。 |
| E5 | `overflow` | ✅ `resolved` / backstop | `#ai-panel` 折叠/展开两态下,3px 竖条(若适用)与既有 `▾`/`▸` 指示器并存且不重叠。 |
| E5 | `long-text` | ✅ `resolved` / backstop | 折叠指示器不因标题变长而漂移;`.collapse-indicator` 本阶段零触碰(D-23)。 |
| E6 | `empty` | ✅ `resolved` / explicit | 该行的存在与否由 `app.js` 的 `renderAnnotations` 驱动(已验收路径,硬规则 5 不得触碰);本阶段零 diff,故空态结构不变。 |
| E6 | `loading` | ✅ `resolved` / explicit | 同上。本阶段只把 `::before` 的 emoji 机制换成 mask 字形,不触碰渲染函数。 |
| E6 | `error` | ✅ `resolved` / explicit | 同上。 |
| E6 | `populated` | ✅ `resolved` / explicit | 同上 —— 批注列表的正常填充态结构与文案均不变。 |
| E6 | `overflow` | ✅ `resolved` / backstop | 两个 12px mask 字形与相邻文字基线视觉对齐,且不撑高行盒(行高仍由 `--lh-snug` / `--lh-reading` 决定)。计算样式看不见这一项,只能看渲染结果。 |
| E6 | `long-text` | ✅ `resolved` / backstop | 图标在折行的引用文本里仍与首行文字对齐,不在换行处漂移;`--color-text-secondary` 在 `.annotation-item`(`--color-surface` 5.62)地面上可辨。 |
| E7 | `empty` | ✅ `resolved` / explicit | 该行的存在与否由 `app.js` 的 `renderVerdictCard` 驱动(已验收路径,不得触碰);本阶段零 diff,故空态结构不变。 |
| E7 | `loading` | ✅ `resolved` / explicit | 同上。 |
| E7 | `error` | ✅ `resolved` / explicit | 同上。 |
| E7 | `populated` | ✅ `resolved` / explicit | 同上 —— 裁决卡片的正常填充态结构与文案均不变。 |
| E7 | `overflow` | ✅ `resolved` / backstop | 两个 12px mask 字形与相邻文字基线视觉对齐,且不撑高行盒。 |
| E7 | `long-text` | ✅ `resolved` / backstop | 图标在折行的位置文本里仍与首行文字对齐;`--color-text-secondary` 在 `.verdict-card`(`--color-surface-warning-subtle` 5.82)地面上可辨。 |
| E8 | `loading` | ✅ `resolved` / explicit | 容器标签的显隐由 `#doc-panel` 的既有折叠行为驱动,本阶段零改动;VISUAL-03 只做复证(D-19,零 CSS 改动)。 |
| E8 | `error` | ✅ `resolved` / explicit | 同上。 |
| E8 | `overflow` | ✅ `resolved` / backstop | 「文档区」在面板收起态(48px 竖条)下不裁切、不换行。 |
| E8 | `long-text` | ✅ `resolved` / backstop | 其 14px / 500 的「安静标签」定位在实测中成立,不因本阶段标题改动而变成全屏最大最重的文字(SC3)。 |
| E9 | `empty` | ✅ `resolved` / explicit | 四处 chrome 标题的显隐由 `app.js` / `index.html` 既有结构决定,本阶段两者零 diff,故空态结构不变。 |
| E9 | `loading` | ✅ `resolved` / explicit | 同上。 |
| E9 | `error` | ✅ `resolved` / explicit | 同上。 |
| E9 | `populated` | ✅ `resolved` / explicit | 同上 —— 四处 chrome 标题的正常态由 `check-05` 的字面 px 断言守卫(D-03:守卫项保持字面值,不得改成令牌接线表述)。 |
| E9 | `partial` | ✅ `resolved` / explicit | 同上。 |
| E9 | `zero-one-many` | ✅ `resolved` / explicit | 同上 —— 四处 chrome 标题的个数与位置由 DOM 决定,本阶段零 diff。 |
| E9 | `overflow` | ✅ `resolved` / backstop | 四处 chrome 标题在两栏布局下均不溢出各自容器(SC1 的守卫对象,本阶段不得被带偏)。 |
| E9 | `long-text` | ✅ `resolved` / backstop | 四处 chrome 标题文本变长时各自保持既有字号与色值(`.panel-header h2` 14px / `#draft-view h2` 18px / `.overlay-card h3` 24px),不因本阶段标题改动而漂移。 |

### Backstop 陈述(18 条 —— 每条都是 held-out 视觉检查)

`verification: backstop` —— 只由显式证据确认,否则路由到 `human_needed`,**绝不静默判过**。

| Element | Category | Statement |
|---|---|---|
| E1 | `overflow` | 长文档在 `#draft-content` 内滚动而非撑破容器;本阶段不新增滚动容器(布局归 Phase 6),只断言不回归。 |
| E1 | `long-text` | 超长 DESIGN.md 渲染后 `#doc-pane` 无横向滚动条,28px h1 不撑破内容宽。 |
| E2 | `overflow` | 28px h1 / 22px h2 在 `--doc-panel-w` 最窄值(340px)下不溢出容器。 |
| E2 | `long-text` | 三级标题层级可辨且不互相淹没;h1 是全屏最大文字(28 > 24 > 22)。**字号半边已由 `check-05` 的令牌接线断言覆盖**,剩余的是视觉层级判断。 |
| E3 | `overflow` | `#btn-continue-check` 与 `#btn-continue-repair` 在 `#check-controls`(column)里各占一行,不溢出。 |
| E3 | `long-text` | 「授权撰写总设计文档」在 340px 面板(内容宽 260px)下不换行不裁切;16px 白字在 green-12 上可读(12.32)。**换行半边无自动化证据** —— 需实测。 |
| E4 | `overflow` | 3px 竖条在每个活动面板上真实可见,不被标题行内元素盖住,也不因 `border-radius` 在角落断开(**05-N-4 的实测验收**)。 |
| E4 | `long-text` | 面板标题文本变长时竖条仍贴左缘,标题变色不溢出标题行。 |
| E5 | `overflow` | `#ai-panel` 折叠/展开两态下,竖条与既有 `▾`/`▸` 指示器并存且不重叠。 |
| E5 | `long-text` | 折叠指示器不因标题变长而漂移;`.collapse-indicator` 本阶段零触碰(D-23)。 |
| E6 | `overflow` | 两个 12px mask 字形与相邻文字基线视觉对齐,且不撑高行盒(行高仍由 `--lh-snug` / `--lh-reading` 决定)。**计算样式看不见这一项,只能看渲染结果** |
| E6 | `long-text` | 图标在折行的引用文本里仍与首行文字对齐,不在换行处漂移;`--color-text-secondary` 在 `.annotation-item`(`--color-surface` 5.62)地面上可辨。 |
| E7 | `overflow` | 两个 12px mask 字形与相邻文字基线视觉对齐,且不撑高行盒。 |
| E7 | `long-text` | 图标在折行的位置文本里仍与首行文字对齐;`--color-text-secondary` 在 `.verdict-card`(`--color-surface-warning-subtle` 5.82)地面上可辨。 |
| E8 | `overflow` | `#doc-panel-header h1`「文档区」在面板收起态(48px 竖条)下不裁切、不换行。 |
| E8 | `long-text` | 其 14px / 500 的「安静标签」定位在实测中成立(VISUAL-03 / SC3)。 |
| E9 | `overflow` | 四处 chrome 标题在两栏布局下均不溢出各自容器。 |
| E9 | `long-text` | 四处 chrome 标题文本变长时各自保持既有字号与色值(14 / 18 / 24px),不因本阶段标题改动而漂移。 |

**已知且不试图绕过的环境限制(不得重新推导、不得对抗):**

- **截图不可用** —— 无头渲染被阻,且常驻 `/api/events` SSE 流使采集处理器无法终止。
  **计划用计算样式检查 + 具名人工步骤,不要计划视觉 diff。**
- Playwright 若使用,**必须** `chromium.launch({ channel: 'chrome' })`;`.venv` / check-05 路线
  必须用捆绑 chromium(`channel` + `headless` 会挂死)。
- **键盘文本选区无法自动化。** 本阶段的 18 条 backstop 里没有一条依赖键盘选区 ✓

**probe 未覆盖、且刻意不覆盖的东西(写明以免被读成缺口):** 分类法的轴是**元素 × 状态**。
本阶段三条承重不变量**不是**状态考量,故刻意不在上表:**(1)** 新增令牌必须有同提交消费者 —— 由
Hard Rule 5 + §Typography / §Color 的两张消费者核账表覆盖;**(2)** 三档两两不同 —— 由 D-04 的
运行时断言覆盖;**(3)** 围栏外零裸 hex / tier-1 名不出围栏 —— 由 CHECK-01 覆盖。按
`references/ui-consideration-probe.md`,开放的领域/UX 考量(深度 WCAG 广度、实时/离线、i18n)
归 prose 所有,不塞进这个封闭分类法。

---

## Registry Safety

不适用 —— 无 shadcn、无 registry、无第三方 block、无设计系统包、无构建步骤(D-06)。
`frontend/vendor/` 只含一个文件(`marked.min.js`),本阶段每个计划跑完之后**仍须只含一个文件**。

| Registry | Blocks Used | Safety Gate |
|----------|-------------|-------------|
| none | none | 不适用 —— 没有任何 registry 可达,也没有任何 registry 被使用 |

**两个图标是手写的 data-URI,不是 vendored 资源。** 没有任何图标文件进入仓库:
`frontend/vendor/` 未被触碰,依赖数仍为零,且两个字形仍只有**一个事实源**(围栏内的
`--icon-pin` / `--icon-location`)。**`<path>` 的 `d` 数据由规划期手写**(D-22),因此不引入任何
外部来源、许可证或供应链面。**Registry 审计:0 个第三方 block,无 flag。**

---

## Checker Sign-Off

- [x] Dimension 1 Copywriting: PASS
- [x] Dimension 2 Visuals: PASS
- [x] Dimension 3 Color: PASS
- [x] Dimension 4 Typography: FLAG(非阻塞 —— 3 处证据性缺陷,已在下方登记并就地修正)
- [x] Dimension 5 Spacing: PASS
- [x] Dimension 6 Registry Safety: PASS
- [x] Dimension 7 Inventory Provenance: PASS(N/A —— `Tool: none`,无设计系统可枚举)

**Approval:** approved(2026-09-20;checker 独立复算了全部对比度比值、层叠栅栏与 Hard Rule 5 消费者核账,均成立)

**Dimension 4 的三处非阻塞缺陷(已就地修正,记录以备追溯):**

1. **`--text-md` 消费者行少数一处** —— 原写 6 处且未列 `:626`(`.markdown-body h3`),却声称「失去
   `.markdown-body h3` → 净不变」,自相矛盾。磁盘实为 **7 处**。已改为 7 → 7 并补入 `:626`。
2. **行高配对注释会留下不自洽** —— 重写的比率配对表有 7 行但只用到 4 个 `--lh-*` 中的 3 个,
   `--lh-compact`(唯一消费者 `.overlay-card p`)无行,而注释头部仍写 `four`;且既有注释的
   `18/28` 本身是**算术错误**(18 × 1.3333 = 24)。已在 §行高 追加两条修正要求。
3. **Hard Rule 9 的特异性括注写反** —— 全局 `h1, h2, h3` 是 **0-0-1**,并非「与 1-0-1 等特异性」;
   它在 `font-size` 上对四处 chrome 覆盖是惰性的。规则本身(不得给 `.markdown-body` 之外的标题写
   字号规则)正确且与已锁定的 TYPE-01 一致,只有该括注的解释错了。已改写为真实暴露面。

---

## Provenance

- **Phase:** 5 — 排版与视觉层级(v1.14 前端视觉与可访问性里程碑)。
- **契约范围:** 本文件**只重写 `04-UI-SPEC.md` 的 `## Typography` 节**;`## Color` 与
  `## Contrast Verification` 的权威是 `idi-04.1-UI-SPEC.md`,本文件只做增补并逐条标明增补点。
  **不存在、也不得创建上游任何一份契约的第二份全文副本。**
- **基线(2026-09-20 对 HEAD 实测,非引用上游文档):**
  - 围栏 `:root` 在 `style.css:5-343`;`frontend/style.css` = **1055** 行。
  - tier-1 = **25**(`--white` + 24 个 `--radix-<family>-<step>`);`--color-*` = **47**;
    `/* PAIR */` = **43** + `/* ORDER */` = **1**。
  - 字号刻度 = **5**(`12/14/16/18/24`);围栏外 `font-size: …px` 裸字面量 = **1**(`.collapse-indicator` 的
    `20px`,L434,属 backlog `999.1`)。
  - `font-weight` 消费:`--fw-regular` ×1、`--fw-medium` ×4、`--fw-semibold` ×12。
  - `^\.hidden {` = **1**;`!important;` 声明 = **1**(`grep -c '!important'` = 3,含 L13-14 注释散文);
    `@media` = **0**;`:focus` / `:focus-visible` / `outline` = **0**;`:disabled` = 8。
  - `#ai-panel` 从不被 `.hidden`(`grep -n "aiPanel" frontend/app.js` 零命中);`#session-panel` 由
    `app.js:356` 单点 toggle。
  - `.annotation-quote::before`(`:836`)与 `.verdict-location::before`(`:1021`)各只出现一次,
    **无竞争者**。
- **本文件里的每一个比值都是本次为这份契约从**本契约写入的值**算出的**,使用 WCAG 2.x 相对亮度,
  并按 `scripts/check-02-contrast.py` 的同一模型(8-bit sRGB 合成、闭区间判定:4.496 失败、4.504 通过)。
  **`scripts/check-02-contrast.py` 是唯一仲裁者;Radix 与上游文档的 AA 论断一律不采信**
  —— 04.1 已立此方法论,并在自己的五个 band 里被推翻四次。
- **上游:** `05-CONTEXT.md`(D-01…D-23)、`.planning/ROADMAP.md`(§Phase 5 + §全局硬规则 1-7 +
  §Backlog 999.1)、`.planning/REQUIREMENTS.md`、`.planning/STATE.md`(§Operator Next Steps)、
  `04-UI-SPEC.md`、`idi-04.1-UI-SPEC.md`、`idi-04.1-CONTEXT.md`、`idi-04.1-UI-REVIEW.md`、
  `idi-04.1-VERIFICATION.md`、`idi-04-VERIFICATION.md`、`frontend/{style.css,index.html,app.js}`、
  `scripts/check-0{1,2,3,4}*`、`scripts/check-05-ui-uat.py`、`scripts/ui-states/`。
- **标记待规划期确认的事项:**
  1. 两处 `::before` 的 `d='…'` 路径数据(D-22 明写交规划期)。
  2. `05-N-5` 的基线对齐是**实测项**,`vertical-align: -2px` 是起点而非结论。
  3. WCAG 2.2 的准则编号(SC 1.4.3 / 1.4.5 / 1.4.11 / 2.5.8)按既有实践陈述,本环境无法抓取
     `w3.org`;其**实质**(4.5:1 / 3:1 / 24×24)稳定,且本文件每一个数都是对着它量的。
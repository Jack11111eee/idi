# Phase 5: 排版与视觉层级 - Context

**Gathered:** 2026-09-20
**Status:** Ready for planning

<domain>
## Phase Boundary

给渲染出的 DESIGN.md 与界面 chrome 各一套受控的排版刻度;把不可逆的 G3 授权从例行按钮里在视觉上分离出来;页面级层级正确;侧栏面板活动态可辨;两处内容标记换成内联 SVG。

**改动面:纯 `frontend/style.css`** —— 围栏 `:root` 块内的新增声明 + 围栏外的排版/层级规则。**`app.js` / `index.html` / `frontend/vendor/` 零改动**(本里程碑只有 Phase 8 触碰前两者)。

**明确不含:**
- 新功能、新依赖、新前端文件、构建步骤(ROADMAP 里程碑章程)
- 暗色模式 / `prefers-color-scheme`(v1.14 全局已裁定排除)
- 图标库 / SVG sprite 体系 / 图标字体(REQUIREMENTS Out of Scope 表)
- `.collapse-indicator` 的越轨字面量(`font-size: 20px` / `line-height: 1`)—— 已裁定为 backlog `999.1`,**不在本阶段**
- hover / active / transition 态(`INTERACT-01`,Phase 7)
- 布局结构常量、窄窗口、滚动容器、命中区(`LAYOUT-01…04` / `A11Y-07`,Phase 6)
- 焦点样式(`A11Y-01`,Phase 7)

**已签核、不得重开:** S-1(间距 12 档)、S-2(14px 为一级字号档)、S-3(`#ccc`→`#8a8a8a`)、S-4(冻结轮 route 2)、04.1 的 S-5/S-6。04.1 原话:「all four signed off 2026-09-17; **none may be re-opened, and no one-line alternative may be executed**」。

</domain>

<decisions>
## Implementation Decisions

### 基线与契约漂移(最优先 —— 决定后面所有取值)

- **D-01:** **以磁盘 HEAD 为唯一现实基线。** 规划与执行一律以 `frontend/style.css` 的磁盘值 + `scripts/check-05-ui-uat.py` 的断言为准;两份 UI-SPEC / ROADMAP Phase 5 段 / REQUIREMENTS 的四处 chrome 值**仅作意图参考**。规划期必须把下面「契约漂移清单」逐条登记为「已由 qrq 实现」或「已由 qrq 推翻」。**不动 `04-UI-SPEC.md` / `ROADMAP.md` 正文**(改 ROADMAP 会作废已通过的验证指纹)。 — **Reversibility:** reversible — 基线口径是读取约定,不改任何文件。
- **D-02:** ROADMAP Phase 5 `Gates` 行中「`#brainstorm-view h2` 仍计算为 14px / `#8a6508`」**改写为令牌接线表述**:「`#brainstorm-view h2` 仍解析为 `--text-md` 与 `--color-action-warning`」。与 04.1 的 D-14 同构。已接受的代价:牺牲「硬编码值能抓令牌接错线」的那部分检测力。 — **Reversibility:** reversible。
- **D-03:** `scripts/check-05-ui-uat.py` 的字面 px 断言**分类处理**:Phase 5 主动改动的断言改成令牌接线表述;守卫「不该变」的四处 chrome 覆盖(`.panel-header h2` 14px / `#draft-view h2` 18px / `.overlay-card h3` 24px / `.markdown-body` 16px)与 `--text-base == 14px`(S-2 依赖)**保持字面 px**。理由:字面值在守卫上是**特性而非缺陷**——它才能抓到「误伤 chrome」;改成令牌接线会退化为同义反复。 — **Reversibility:** reversible。
- **D-04:** `check-05-ui-uat.py:689-695` 那条「`#btn-process-round` 与 `#btn-authorize` 三属性**逐字节相同**」断言**反转为三档两两不同 + 档内相同**:routine 三只(`#btn-process-round` / `#btn-continue-check` / `#btn-continue-repair`)互相相同;commit 两只(`#btn-approve-draft` / `#btn-start-writing`)互相相同;irreversible(`#btn-authorize`)独立;三档**两两不同**。一个断言同时覆盖 VISUAL-01 与 VISUAL-02。档内相同那一半同样承重——它能抓到「改错了一只」。 — **Reversibility:** reversible。
- **D-05:** **`frontend/style.css` 的任何编辑都会作废 `idi-04.1-radix` 的 `passed` 指纹**(其 `covered_files` 含该文件,digest 为原始字节 sha256),`scripts/check-05-ui-uat.py` 也在其 `covered_files` 里。本阶段必须**连带复验 04.1**。 — **Reversibility:** reversible — 复验是流程义务。

### 契约漂移清单(规划期必须逐条登记)

值层已被 quick 任务 `260918-qrq`(2026-09-18,commits `33bbd7d` / `448686b` / `3684353` / `253d4d3`)整体换成「ChatGPT 视觉语言」,契约未同步。以下每一条都是**契约文本 ≠ HEAD**:

| 契约文本声称 | HEAD 实况 | 性质 |
|---|---|---|
| `.markdown-body h1/h2/h3` **无** `font-size` 规则,落 UA 默认 28/21/16.4px | **已有**作用域规则 → 24/18/16px | 已由 qrq 实现 |
| `#doc-pane > h1` 是约 32px 粗体 | 该选择器**不存在**;实际是 `#doc-panel-header h1` = 14px / 500 / `#646464` | 已由 qrq 实现 |
| `#brainstorm-view h2` = 14px / `#8a6508` | 16px / `#4f3422`;`#8a6508` **在围栏里不存在** | 已由 qrq 推翻 |
| TYPE-02:`code` 现 12.5px 分数值 | 已是 `var(--text-base)` = 14px | 已由 qrq 实现 |
| TYPE-02:blockquote 现 `#666` | 已是 `var(--color-text-muted)` = `#646464` | 已由 qrq 实现 |
| TYPE-02:`table th/td` 现 13px vs 正文 14px | 已是 `var(--text-base)` = 14px,vs 本体 16px | 已由 qrq 实现 |
| TYPE-03 基线「仅 600 / 400 两档」 | 三档:`--fw-regular` 400 ×1 / `--fw-medium` 500 ×4 / `--fw-semibold` 600 ×12 | 已由 qrq 推翻 |
| 字号锚点 13px | 14px(`--text-base`);刻度 5 档 `12/14/16/18/24` | 已由 qrq 推翻 |
| 契约字号表 `--text-2xl: 18px` / `--text-3xl: 22px` | 18px 已被 `--text-lg` 占用;22 / 28 均不存在 | 已由 qrq 推翻 |
| 契约行高 `--lh-tight 1.35 / --lh-compact 1.6 / --lh-reading 1.75` | `1.3333 / 1.5556 / 1.625`,另有新增 `--lh-snug 1.4286` | 已由 qrq 推翻 |
| 契约圆角三值 `4 / 8 / 999px` | 四值 `8 / 10 / 28 / 999px` | 已由 qrq 推翻 |
| 契约 `--color-action-*` 候选 hex `#e9f7ef` / `#26754a` / `#1f5c3a` | `--green-800: #1f5c3a` 已被 04.1 V-13 删除;三族共用 green-3 / green-11 / green-12 | 已由 qrq + 04.1 推翻 |
| 契约 `--sidebar-w: 420px` | 已改名改值为 `--doc-panel-w: clamp(340px, 30vw, 480px)` | 已由 qrq 推翻 |
| 契约 L-5:`#state-badge { right: 448px }` | 该声明已消失,`#state-badge` 现在是流内元素 | 已由 qrq 推翻 |
| 契约 `--fw-medium` 「**No. Do not declare it.**」 | 已声明且消费 4 处 | 已由 qrq 推翻 |
| 「五个元素只靠 `.hidden` 隐藏」清单 | 已过期:`#rounds-hint` / `#btn-process-round` / `#round-switcher` / `#writing-hint` 已不在清单;`#btn-process-round` 改用 `disabled` | 已由 qrq 推翻 |
| ROADMAP / 04-UI-SPEC 引用的 `app.js:1550` | 已漂移到 `app.js:1563` / `1569` | 行号漂移 |

### 排版刻度(TYPE-01 / TYPE-02 / TYPE-03)

- **D-06:** 正文本体**保持 16px**(`--text-md`),**新开两档 22px / 28px**。最终阶梯:**h1 28 / h2 22 / h3 18 / 本体 16**。刻度 5 → 7 档:`12 / 14 / 16 / 18 / 22 / 24 / 28`。两个新令牌**与消费者同提交**(不违反 Pitfall 1 / Hard Rule 5)。DESIGN.md 的阅读尺寸不变。理由:本体拉回 14px 会让整篇文档小一档,而 16px 是 qrq 刻意选定的阅读尺寸;h1 的 24px 已是旧刻度上限,不开档无法建立三级标题层级。 — **Reversibility:** costly — 回退要同时改围栏声明、`.markdown-body h1/h2/h3` 三条规则、`check-05` 的 `.markdown-body` 断言与围栏注释里的配对表。
- **D-07:** 新开两档的令牌名为 **`--text-2xl: 22px`** / **`--text-3xl: 28px`**,继续跟随 `xs/base/md/lg/xl` 的尺寸递进命名法。**围栏注释必须写明**:契约里的 `--text-2xl` 指 18px,现指 22px(名同值不同,否则日后对照契约会困惑)。 — **Reversibility:** costly — 改名要同时改围栏与 `.markdown-body h1/h2` 两处消费者。
- **D-08:** **`table th/td` 与行内 `code` 保持 14px(`--text-base`),零改动。** 比正文低一档的相对关系**已与契约意图一致**(契约时代是 13 vs 14,同样低一档)。TYPE-02 因此作为**「复证项」**收口——其字面要求「归入刻度与令牌」已全部由 qrq 实现。`blockquote` 的 `--color-text-muted` 同样只复证。 — **Reversibility:** reversible。
- **D-09:** **字重三档分工显式化**:内容标题(`.markdown-body h1/h2/h3`)全 600;chrome 标题(`.panel-header h2` / `#doc-panel-header h1`)与**按钮**统一 500。即六个动作按钮的 `font-weight` 从 600 改为 500(它们现在与内容标题同重)。 — **Reversibility:** reversible。
- **D-10:** 新开两档**复用 `--lh-tight`(1.3333)**,h1/h2/h3 行高统一,**零新增行高令牌**。围栏注释从「整数配对」改为「**比率配对**」表述(28→37.33 / 22→29.33)。理由:28k 与 22k 同时为整数要求 k 是 0.5 的倍数,k=1.5 又太松——整数配对在数学上不可得。 — **Reversibility:** reversible。

### 不可逆动作权重(VISUAL-01 / VISUAL-02)

- **D-11:** **三段坡道**(契约原设计):

  | 档 | 选择器 | 形态 |
  |---|---|---|
  | routine | `#btn-process-round` / `#btn-continue-check` / `#btn-continue-repair` | 淡底 + 绿字(**不变**) |
  | commit | `#btn-approve-draft` / `#btn-start-writing` | **实心填充 + 白字** |
  | irreversible | `#btn-authorize` | **实心更深 + 白字 + 字号步进 + 600** |

  三档在**形态**上就不同(淡底 vs 实心),不依赖色深对比。Phase 5 必须**声明 Radix `green-9` / `green-10` 两个 primitive**(围栏注释已预告:「Phase 5 declares the 9/10 fill steps together with their consumers」),并给 `CHECK-02` 加白字对实心填充的配对。**具体取哪两个步由规划期定**(契约候选 hex 已被 04.1 V-13 删除)。 — **Reversibility:** costly — 回退要重挑 Radix 步、重算 CHECK-02 配对、并复跑三档两两不同的 gate。
- **D-12:** **不可逆按钮的字重例外 600** —— `#btn-authorize` 保持 600,其余五只按钮 500。这是 D-09「按钮统一 500」的**唯一已登记例外**,理由:核心价值要求授权绝不与例行混同,而它有四个可用强调通道(形态 / 色深 / 字号 / 字重),此处用满。 — **Reversibility:** reversible。
- **D-13:** 不可逆按钮的**字号步进 14 → 16px**(`--text-md`,现有档,零新增令牌)。契约原本写的 `--text-xl` 16px 是 13px 锚点世界的 1.23×;现锚点 14px,16px 即 1.14×。**不加 padding 步进。** — **Reversibility:** reversible。
- **D-14:** 实心按钮的 `:disabled` 态**沿用 `opacity: 0.55`,零改动**。理由:0.55 对实心按钮是**更强的**淡化(实心→淡绿是明显的去饱和),区分度反而上升;与硬规则 Pitfall M5「不得软化」字面一致。 — **Reversibility:** reversible。
- **D-15:** 硬规则不变量继续成立:`--color-action-irreversible*` **只被 `#btn-authorize` 消费,永不出现第二个消费者**;三族名不得改(`commit` 而非 `gate`——「gate」在本代码库已指决策门)。

### 标记体系(VISUAL-03 / VISUAL-04 / VISUAL-05)

- **D-16:** **VISUAL-04 的范围修正为「三选一活动态 + AI 面板折叠态」。** 依据:`#ai-panel` **从不被 `.hidden`**(`grep -n "aiPanel" app.js` 零命中),它的折叠是 `#ai-panel-body` 上的 `.collapsed`(`app.js:1562-1565`),所以 `:not(.hidden)` 只能表达 `#session-panel` / `#annotations-panel` / `#checks-panel` 三者互斥。前三个用 `:not(.hidden)` 表达活动态;`#ai-panel` 用它**自己的**展开/折叠态(既有 `▾`/`▸` 指示器)作为可辨状态——**该指示器不得触碰**(见 D-20)。REQUIREMENTS 的 VISUAL-04 措辞需登记修正。 — **Reversibility:** reversible。
- **D-17:** 活动态标记的**形态**:面板**左侧一条竖条** + 面板标题文字改用标记色。实现**必须用 `box-shadow: inset`(而非 `border-left`)**以避免布局位移——冻结轮已经是这个写法。注意非活动面板是 `display: none`(看不见),所以「可区分」实际退化为「当前活动的那一个看得出是活动的」。 — **Reversibility:** reversible。
- **D-18:** 竖条用**蓝**,并**新开一个诚实命名的 tier-2 令牌**承载它(与消费者同提交,不违反 Hard Rule 5),**不复用 `--color-action-primary`**。理由:该名字说的是「主要动作」,拿它做面板指示器会让**名说谎**——而本项目为此付过代价(04.1 D-03 把 26 个 primitive 全部改名,理由正是「保留旧名会让名说谎」)。**具体令牌名由规划期定**(建议形如 `--color-marker-active`,指向 `--radix-blue-11`)。选蓝而非契约划定的琥珀 accent,是因为琥珀在本系统已承载**警告**(`--color-action-warning`)与**冻结轮**(`#round-doc.round-frozen` 的琥珀 inset 竖线)两重含义,再加「活动面板」即三重撞车。**这是对契约 60/30/10 表 Accent 域的刻意偏离,需登记。** — **Reversibility:** costly — 令牌名一旦落地即与 04.1 的 D-02 一样被下游引用冻结。
- **D-19:** **VISUAL-03 认定已由 qrq 实现,Phase 5 只做复证。** `#doc-panel-header h1` 已是 14px / `--fw-medium` 500 / `--color-text-secondary` `#646464`,源码注释即「安静的容器标签,不是全屏最大最重的文字」。**零 CSS 改动**;只需把 gate / 交付物里的选择器名从 `#doc-pane > h1` 更正为 `#doc-panel-header h1`(D-05 的契约漂移登记)。连带效果:D-06 之后全屏最大文字是文档自己的 h1(28px) > `.overlay-card h3`(24px,模态) > 文档 h2(22px),页面级层级已立住。 — **Reversibility:** reversible。
- **D-20:** 两处图标**改用 `mask-image` + `background-color`**,**刻意偏离契约已写死的 `content: url(data-URI)` 机制**。理由:data-URI 经 `content` 渲染为**图片**,不继承页面 CSS,`currentColor` 不可用,契约只能把 fill 钉死为转义 hex——那让「跟文字色」成为**人工同步的约定而非机制**(值层一变就静默漂移)。mask 方案让图标**真正跟随令牌**。附带收益:**`<path>` 不带 `fill` 属性即可**(mask 只看 alpha,默认黑=不透明),data-URI 里**零颜色信息**,于是契约的**字面量例外 L-3 可以整个撤掉**。代价:伪元素从「内联字形」变盒模型,需 `display: inline-block` + 显式尺寸,对齐需实测。 — **Reversibility:** costly — 回退要恢复 `content: url()`、重新引入 L-3、重调对齐。
- **D-21:** 两处图标的**用色 = `--color-text-secondary`**(经 `background-color` 上色,不再是转义 hex)。图标在正文流里,不该抢眼;与相邻文字同色。 — **Reversibility:** reversible。
- **D-22:** 两处图标的**形状风格 = 实心**(图钉 / 地图标记),**渲染尺寸 12×12**,**`vertical-align: -2px`**(契约原值)。理由:mask 只看 alpha,实心形状在 12px 下比轮廓线清晰得多;12px 是与 14px 文字并排的常规图标尺寸。**具体 `d='…'` path 数据由规划期定。** — **Reversibility:** reversible。
- **D-23:** **`.collapse-indicator` 不得触碰**(`app.js:1563` / `1569` 用 `textContent` 赋值,内联 `<svg>` 会被擦掉)。其 `font-size: 20px` / `line-height: 1` 越轨字面量属 backlog `999.1`,**本阶段不修**。D-16 对 `#ai-panel` 的处置正是「承认既有 `▾`/`▸` 指示器已构成可辨状态」,与该元素零交互。 — **Reversibility:** reversible。

### Claude's Discretion

- 竖条令牌的**具体名字**(建议 `--color-marker-active`)与它指向的 Radix 步。
- 三段坡道中 commit 与 irreversible **具体取哪两个 Radix 步**(green-9 / green-10 的分配)。
- 两处图标的 **`d='…'` path 数据**(实心图钉 / 实心地图标记的常规形状)。
- 竖条宽度(建议 3px,与 `.markdown-body blockquote` 的 `border-left: 3px` 一致)、标题变色改的是 `color` 还是 `color` + `font-weight`。
- 围栏内注释的措辞与粒度(尤其 D-07 的「契约 2xl=18px vs 现 22px」与 D-10 的比率配对表)。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 本阶段的直接上游(必须读)
- `.planning/ROADMAP.md` §Phase 5 — 本阶段的 goal / 交付物 / Success Criteria / Pitfalls M4 / 7 / M5 / 3 / 9
- `.planning/ROADMAP.md` §全局硬规则 1-7 — **每个计划都适用**;尤其规则 1(`.hidden` 唯一性)、规则 3(追加不重排)、规则 5(不得触碰清单)、规则 6(零新增依赖)
- `.planning/ROADMAP.md` §Backlog §Phase 999.1 — `.collapse-indicator` 的越轨字面量 + `check-05-ui-uat.py:588` 陈旧文案,**明确不在本阶段**;且记录了「任何 `frontend/style.css` 编辑都作废 04.1 指纹」的连带义务
- `.planning/REQUIREMENTS.md` §VISUAL(01-05)/ §TYPE(01-03)/ §Out of Scope 表 — 本阶段 8 条需求的原文;**注意其引用的具体值多已过期,以 D-01 的基线口径读**
- `.planning/STATE.md` §Operator Next Steps — S-1…S-4 签核原文(不得重开),以及 04.1 的 S-5/S-6
- `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` — **颜色两节之外仍为权威**(Color 与 Contrast Verification 两节以 04.1 为准)。重点节:`## Design Decisions` Q1/Q2/Q3/Q4/Q7、`## Typography`、`## Global Hard Rules`、`## Do-Not-Touch List`、`## Sign-Off Items`、`## The Four Contract-Check Commands`、60/30/10 表(Accent 域与 active-panel marker 的归属)
- `.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md` §Notes N-1…N-5 — 值层决策的来由
- `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` — **Color 与 Contrast Verification 两节的权威**(tier-1 Radix 名、47 个 tier-2 名、43 对清单);§C-1 记录了 `--text-base` 14px vs 契约 13px 的已知差异
- `.planning/phases/idi-04.1-radix/idi-04.1-CONTEXT.md` — D-02(tier-2 名冻结)/ D-04(只声明消费到的步)/ D-14(断言改令牌接线表述)/ D-15(配对清单按实际落地枚举)
- `.planning/phases/idi-04.1-radix/idi-04.1-UI-REVIEW.md` — `:75`(Pillar 4,undeclared 6th size)、`:77`(C-1 downstream-gate discrepancy,`#brainstorm-view h2` 的 14px 门与 HEAD 不符,「left as the user's call」—— 本阶段 D-02 即对该条的裁定)
- `.planning/phases/idi-04.1-radix/idi-04.1-VERIFICATION.md` — `covered_files` 指纹清单(D-05 的复验对象)
- `.planning/phases/idi-04-tokens-contract/idi-04-VERIFICATION.md` — frontmatter `overrides:`(用户裁定把 `.collapse-indicator` 越轨项指派到 backlog 999.1)

### 代码面
- `frontend/style.css` §围栏 `:root`(`L5-343`,含 `/* ===== DESIGN TOKENS: START/END ===== */`、tier-1 Radix primitive、tier-2 语义令牌、`/* PAIR */` 对比度清单、以及 `L42-45` 的「Phase 5 declares the 9/10 fill steps」预告)
- `frontend/style.css` §字号/字重/行高/圆角刻度(`L204-227`)
- `frontend/style.css` §`.markdown-body h1/h2/h3` 规则(已由 qrq 加显式 `font-size`)
- `frontend/style.css` §六个动作按钮规则(`#btn-approve-draft` / `#btn-process-round` / `#btn-authorize` / `#btn-start-writing` / `#btn-continue-check` / `#btn-continue-repair`)
- `frontend/style.css` §`L353` `button:hover`(唯一消费 `--color-surface-hover` 的规则;**ID 特异性 1-0-0 使其对六只按钮无效**——本阶段无需处理 hover)
- `frontend/style.css` §`.annotation-quote::before`(现 `content: '📌 '`)与 `.verdict-location::before`(现 `content: '📍 '`)
- `frontend/style.css` §`.markdown-body table / th / td / code / blockquote`
- `frontend/style.css` §`L611` `#draft-view h2, #rounds-placeholder h2` 与 §`L679` `#brainstorm-view h2`(**同为 1-0-1,后者靠源码顺序取胜** —— 硬规则 3 的活证据)
- `frontend/style.css` §`L357` `.hidden { display: none !important }`(机制而非样式,不得触碰)
- `frontend/style.css` §`L434` `.collapse-indicator`(**不得触碰**,D-23)
- `frontend/index.html` §`L12-70` 四个 `<section>` 面板 DOM;§`L61` / `L88` 两处 `.collapse-indicator`
- `frontend/app.js` §`L1562-1569`(`#ai-panel-body` 的 `.collapsed` 切换与两处 `.collapse-indicator` 的 `textContent` 赋值)
- `scripts/check-01-token-conformance.sh` — 围栏外裸 `#hex` 必须为 0
- `scripts/check-02-contrast.py` — 从围栏读 `/* PAIR */` 清单算真实 WCAG 比值;零依赖、只读、对未声明令牌名大声失败(D-11 要给它加白字对实心填充的配对)
- `scripts/check-03-hidden-uniqueness.sh` / `scripts/check-04-important-count.sh` — 两条不变量守卫
- `scripts/check-05-ui-uat.py` — Playwright UAT harness(`--item N` 单跑);`:689-695`(D-04 的反转对象)、`:720`(`#doc-pane` 不存在的那句注释)、`:742-747` / `:751` / `:760` / `:802`(D-03 的分类对象)
- `scripts/ui-states/` — p1 / p12 / p3 / checking / archive 五个磁盘状态样本

### 需求与状态
- `DESIGN.md` — 项目唯一权威设计文档;§3.8 语言红线
- `.planning/REQUIREMENTS.md` §Traceability — VISUAL-01…05 / TYPE-01…03 均为 Phase 5、状态 Pending

### 外部
- 无。本阶段为纯 CSS 改动,**无外部规范依赖**;Radix 步的选取以 `scripts/check-02-contrast.py` 算出的真实比值为仲裁(不采信上游文档的 AA 论断 —— 04.1 已立的方法论立场)。

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **围栏 `:root` 令牌块**(`frontend/style.css` L5-343):单一事实源。本阶段的新增声明(2 个字号档、green-9/10 两个 primitive、1 个标记色 tier-2、2 个 `--icon-*`)全部落在这里。
- **`scripts/check-02-contrast.py`**:从围栏读 `/* PAIR --fg ON --bg TEXT|NON-TEXT[@alpha] */` 清单算真实 WCAG 比值。零依赖、只读、对未声明令牌名 exit 1 —— 所以清单与令牌块无法漂移。D-11 的白字对实心填充配对直接复用它验证。
- **`scripts/check-05-ui-uat.py`**:Playwright harness,5 个磁盘状态样本,支持 `--item N` 单跑。**test 6 是「令牌接线表述」的范本**(04.1 D-14 的产物),D-03 的分类处理直接照它写。
- **`scripts/ui-states/`**:五个状态样本,幂等、仓库样本只读 —— 活动态与按钮三档的运行时验证直接跑在这里。
- **冻结轮的琥珀 inset 竖线**(`#round-doc.round-frozen`):D-17 的 `box-shadow: inset` 实现有现成先例可抄。

### Established Patterns
- **「与消费者同提交」纪律(Hard Rule 5)**:绝不声明一个在同一次提交中不消费的令牌 —— 直接约束 D-06 / D-11 / D-18 / D-20 的新增声明。
- **「最浅的通过值」原则(Pitfall 4a)**:对比度修到比值却毁掉层级是本项目已记录的失败模式;取最浅的通过值,并断言层级关系。
- **ORDER 断言取严格序关系而非阈值门**(04.1)。
- **追加,不重排**(硬规则 3):`#draft-view h2`(L611)与 `#brainstorm-view h2`(L679)同为 1-0-1,后者靠源码顺序取胜 —— 重排即渲染变更而 diff 看起来完全无辜。
- **`.hidden` 是机制而非样式**:`.hidden { display: none !important }` 不得令牌化、移动、弱化或用 `:where()` 降特异性;三个 ID 特异性竞争者(`#selection-menu` / `#annotations-panel` / `#checks-panel`,均 1-0-0)靠它压制。
- **不采信上游文档的 AA 论断**:一律以 `check-02-contrast.py` 算出的真实比值为准。
- **`opacity` 不得用于文字弱化**(04.1 裁决),但 `:disabled` 的 8 处是**刻意的豁免**,不得软化(Pitfall M5)。
- **环境事实(不得重新推导、不得对抗)**:截图不可用(headless 渲染被阻,SSE 长连接让 capture handler 无法退出)→ **计划用 DevTools 计算样式检查 + 命名人工步骤,不要计划视觉 diff**;若用 Playwright **必须** `chromium.launch({ channel: 'chrome' })`;键盘划词无法自动化。

### Integration Points
- **唯一改动面** = `frontend/style.css`:围栏 `:root` 内的新增声明 + 围栏外的排版/层级规则。
- **`scripts/check-05-ui-uat.py`** 的断言按 D-03 / D-04 分类更新(改它同样作废 04.1 指纹,与 `style.css` 合并为同一批处理,一次性连带复验)。
- **`scripts/check-02-contrast.py`** 的配对清单随 D-11 增加白字对实心填充的配对。
- **`app.js` / `index.html` / `frontend/vendor/` 零改动** —— 硬规则 5 的约 70 个顶层 `getElementById` 句柄 id 不得改名或删除;`frontend/vendor/` 保持只有 `marked.min.js`(Phase 4 gate 原样成立)。
- **本阶段会打破的既有断言(必须在计划里显式登记)**:`check-05-ui-uat.py:689-695`(D-04 反转)、`:742`(`#brainstorm-view h2`)、以及 D-06 会碰到的字号断言。

</code_context>

<specifics>
## Specific Ideas

- **最终字号阶梯(定稿)**:`--text-xs 12 / --text-base 14 / --text-md 16 / --text-lg 18 / --text-2xl 22 / --text-xl 24 / --text-3xl 28`,7 档。标题映射:h1 → `--text-3xl`(28)、h2 → `--text-2xl`(22)、h3 → `--text-lg`(18)、本体 → `--text-md`(16)。
- **三段坡道的语义读法**:淡底 = 「例行」/ 实心 = 「这一步会留下东西」/ 实心更深 + 更大 + 更重 = 「这一步不可逆」。形态是第一区分手段,色深是第二。
- **活动态标记的语义读法**:左侧蓝竖条 = 「你正在看这个面板」。蓝在本系统已是「信息 / 流式」色,与警告琥珀、冻结琥珀**明确分离** —— 这正是 D-18 选蓝的全部理由。
- **mask 方案的一个附带简化**:`<path>` 不带 `fill` 属性,mask 只看 alpha,data-URI 里**零颜色信息**,契约的字面量例外 L-3 可以整个撤掉。
- **两条方法论立场(沿用 04.1)**:不采信上游文档的 AA 论断(以 `check-02` 的实算比值为准);名必须说实话(D-18 为此新开令牌而非复用 `--color-action-primary`)。

</specifics>

<deferred>
## Deferred Ideas

- **`.collapse-indicator` 的 `font-size: 20px` / `line-height: 1` 越轨字面量** —— backlog `999.1` 第 1 项。本阶段不修:Phase 5 的 Pitfall 7 把触碰该元素的范围锁死为两处 `content:` emoji,插入新交付物等于改写已签核的门。**规划时二者不得互相覆盖**(D-23)。
- **`scripts/check-05-ui-uat.py:588` 的陈旧诊断文案** —— backlog `999.1` 第 2 项,与上一项合并为同一批处理。
- **`--color-surface-success` 的声明** —— 04.1 刻意不声明;其假想消费者各自已持 `-surface` 令牌。D-11 之后仍不需要。
- **`#probe-controls` 的移除或重定位** —— 产品行为变更,v1.14 全局已裁定不进任何阶段。
- **暗色模式 / `prefers-color-scheme`** —— v2 `TOKEN-V2-01`。
- **hover / active / transition 态** —— `INTERACT-01` / `INTERACT-02`,Phase 7。**本阶段不新增任何 hover 规则**(六只按钮因 ID 特异性本就无 hover 反馈,不存在回归)。
- **`.overlay-card h3` 的 24px 与 `.markdown-body h2` 的 22px 的相对关系** —— 模态高于正文标题是合理的;若日后要调,属排版刻度的再平衡,不在本阶段。
- **UI Considerations 的 13 条 `overflow` 延后项** —— Phase 6(LAYOUT-02/03);04.1 的 probe 已**取代**而非继承这些处置。

### Reviewed Todos (not folded)
无 —— `gsd-tools query todo.match-phase 5` 返回 `todo_count: 0`,本阶段无待办匹配。

</deferred>

---

*Phase: 05-typography-and-visual-hierarchy*
*Context gathered: 2026-09-20*
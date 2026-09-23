# Phase 5: 排版与视觉层级 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-20
**Phase:** 5-排版与视觉层级
**Areas discussed:** 基线裁定与矛盾门, 标题与正文字号阶梯, 不可逆动作三档, 标记体系, (收尾) 竖条令牌 / SVG 机制 / 新档命名 / 图标尺寸

---

## 基线裁定与矛盾门

### Q1 — Phase 5 的规划基线以谁为准?

| Option | Description | Selected |
|--------|-------------|----------|
| 以 HEAD 为唯一基线 | `style.css` 磁盘值 + `check-05-ui-uat.py` 断言为现实基线;契约文本仅作意图参考;逐条登记漂移;不动契约正文 | ✓ |
| 先同步契约文本 | 先修 `04-UI-SPEC` 与 `ROADMAP` 的过期条目再规划 | |
| 只改会误导的条目 | 只改会误导下游代理写出错代码的那几条 | |

**User's choice:** 以 HEAD 为唯一基线
**Notes:** 起因:quick 任务 `260918-qrq`(2026-09-18)把值层整体换成「ChatGPT 视觉语言」,两份 UI-SPEC 明确知道却选择不改(原话「S-1/S-2 are signed off and this phase does not touch them」)。改 ROADMAP 会作废已通过的验证指纹,故不动契约正文。

### Q2 — `#brainstorm-view h2` 那段 gate 怎么处置?

| Option | Description | Selected |
|--------|-------------|----------|
| 改成令牌接线表述 | gate 改为「仍解析为 `--text-md` 与 `--color-action-warning`」,与 04.1 D-14 同构 | ✓ |
| 改写为 HEAD 实际值 | 写死「16px / `#4f3422`」 | |
| 拉回 14px | 保留契约意图,把元素拉回 14px | |

**User's choice:** 改成令牌接线表述
**Notes:** 契约断言的 `14px / #8a6508` 已不可能满足——`#8a6508` 在围栏里根本不存在,且拉回 14px 会同时打破 `check-05-ui-uat.py:742` 与硬规则 3(该元素靠**源码顺序**胜过同为 1-0-1 的 `#draft-view h2`)。`idi-04.1-UI-REVIEW.md:77` 早已把它记为「left as the user's call」,本次即对该条的裁定。已接受代价:牺牲「硬编码值能抓令牌接错线」的检测力。

### Q3 — `check-05-ui-uat.py` 的字面 px 断言怎么处理?

| Option | Description | Selected |
|--------|-------------|----------|
| 分类处理 | 会变的改令牌接线;守卫「不该变」的四处 chrome 覆盖保持字面 px | ✓ |
| 全部令牌接线 | 全局统一,但守卫退化为同义反复 | |
| 只改字面值 | 改动面最小,但值层下次变动会再漂一次 | |

**User's choice:** 分类处理
**Notes:** 判别依据是**断言的性质**:守卫(Phase 5 SC1 要求「未被带偏」的四处 chrome 覆盖)的字面值在这里是**特性而非缺陷**——它才能抓到「误伤 chrome」;改成令牌接线后会变成「读 `--text-base` 再断言它等于 `--text-base`」的循环。会变的则是 `:742`(brainstorm h2)与 `:689`(逐字节相同)。

### Q4 — 那条「逐字节相同」断言反转成什么形式?

| Option | Description | Selected |
|--------|-------------|----------|
| 三档两两不同 + 档内相同 | routine 三只互相相同 / commit 两只互相相同 / irreversible 独立 / 三档两两不同 | ✓ |
| 只反转那一条 | 只断言 `#btn-authorize` ≠ `#btn-continue-check` | |
| 删除该断言 | 由 Phase 5 新 gate 承担 | |

**User's choice:** 三档两两不同 + 档内相同
**Notes:** ROADMAP 只写了最弱的形式(「授权 ≠ 例行」),会漏掉「第二档是否真的独立于第一档」。档内相同那一半同样承重——能抓到「改错了一只」。

---

## 标题与正文字号阶梯

### Q1 — 正文本体字号与标题阶梯怎么定?

| Option | Description | Selected |
|--------|-------------|----------|
| 本体 16px + 新开两档 | h1 28 / h2 22 / h3 18 / 本体 16;刻度 5→7 档 | ✓ |
| 本体 16px + 新开一档 | h1 24 / h2 20 / h3 18;但 h2/h3 只差 2px | |
| 本体拉回 14px | 零新增令牌,但整篇文档小一档 | |
| 不开档,h3 靠字重区分 | 零字号改动,但标题层级实质没做 | |

**User's choice:** 本体 16px + 新开两档(22 / 28)
**Notes:** 现状 `.markdown-body` 本体 16px 而 h3 也是 16px,只差字重与行高——层级实质断裂;h1 的 24px 已是旧刻度上限,不开档无法建立三级标题。契约原本就打算开档(「Phase 5 declares them with their consumers」),但其值(18/22)是在 13px 锚点世界取的,18px 现已被 `--text-lg` 占用。

### Q2 — `table th/td` 与行内 `code` 的字号怎么定?

| Option | Description | Selected |
|--------|-------------|----------|
| 两者保持 14px | 零改动;相对关系已与契约意图一致 | ✓ |
| 只升 code 到 16px | 行内代码与所在正文齐平 | |
| 两者都升到 16px | 字面满足「内容排版一致」 | |

**User's choice:** 两者保持 14px(零改动)
**Notes:** 发现 TYPE-02 的三个「现」值全部已过期(`code` 不再是 12.5px、blockquote 不再是 `#666`、`table th/td` 不再是 13px),其字面要求「归入刻度与令牌」**已全部满足**。契约时代是 13 vs 14(同样低一档),**相对关系其实是一致的**。故 TYPE-02 转为「复证项」收口。

### Q3 — 字重层级(TYPE-03)怎么定?

| Option | Description | Selected |
|--------|-------------|----------|
| 三档分工显式化 | 内容标题全 600;chrome 标题与按钮统一 500 | ✓ |
| 保持现状,仅复证 | 零改动,但「同为按钮两种字重」的不一致留在出货版 | |
| h1/h2 600、h3 500 | 用字重补足 h3 与本体仅差 2px 的弱层级 | |

**User's choice:** 三档分工显式化
**Notes:** TYPE-03 的前提「仅 600 / 400 两档」也已过期——HEAD 是三档且全部有消费者(`--fw-regular` 400 ×1 / `--fw-medium` 500 ×4 / `--fw-semibold` 600 ×12)。当前的不一致是「六个动作按钮 600,而 chrome 标题与通用按钮 500」——同为按钮却两种字重。本决定要求把六个动作按钮改为 500(后由不可逆按钮的字重例外补回一只)。

### Q4 — 新增的 28px / 22px 两档怎么配行高?

| Option | Description | Selected |
|--------|-------------|----------|
| 复用 `--lh-tight`(零新增) | h1/h2/h3 统一 1.3333;围栏注释改比率配对表述 | ✓ |
| 新开 `--lh-display` 给 h1/h2 | 大标题更紧凑(1.2) | |
| h3 改用 `--lh-compact` | h3 常带多行,接近正文行高 | |

**User's choice:** 复用 `--lh-tight`(零新增)
**Notes:** 围栏自述「Line height — four, paired with the size scale」,配对全是整数 px。但 28k 与 22k 同时为整数要求 k 是 0.5 的倍数,k=1.5 又太松——整数配对在数学上不可得,故把注释改为比率配对表述(28→37.33 / 22→29.33)。排版上 1.3333 对 28px 偏松(大字号通常配 1.1–1.2),此项作为已知取舍接受。

---

## 不可逆动作三档

### Q1 — 三档的形态怎么定?

| Option | Description | Selected |
|--------|-------------|----------|
| 三段坡道(契约原设计) | routine 淡底(不变)/ commit 实心 + 白字 / irreversible 实心更深 + 白字 + 字号步进 | ✓ |
| 只动 `#btn-authorize` | 改动最小,但 VISUAL-02 未满足 | |
| commit 与 irreversible 同实心 | 靠字号区分两档 | |

**User's choice:** 三段坡道
**Notes:** 现状六只按钮解析结果**逐字节相同**(`bg #e6f6eb` / `border #218358` / `fg #193b2d` / 600,差异只在 padding)——这就是「工具在对自己说谎」。三档在**形态**上就不同(淡底 vs 实心),不依赖色深对比。契约的候选 hex(`#26754a` / `#1f5c3a`)已被 04.1 V-13 删除,Phase 5 必须自己挑 Radix 步;围栏注释已预告「Phase 5 declares the 9/10 fill steps together with their consumers」。

### Q2 — 不可逆按钮的字重怎么定?

| Option | Description | Selected |
|--------|-------------|----------|
| 不可逆例外 600 | `#btn-authorize` 保持 600,其余五只 500(四重强调) | ✓ |
| 全部 500,无例外 | 形态已是强区分,字重边际收益最低 | |
| 字重随档位递进 | routine 500 / commit 600 / irreversible 600 | |

**User's choice:** 不可逆例外 600
**Notes:** 与灰区 2 的「按钮统一 500」直接冲突——契约原话是 irreversible「additionally carries a size step **and `--fw-semibold`**」。作为唯一已登记例外,理由:核心价值要求授权绝不与例行混同,而它有四个可用强调通道,此处用满。

### Q3 — 不可逆按钮的字号步进幅度怎么定?

| Option | Description | Selected |
|--------|-------------|----------|
| 14 → 16px(现有档) | `--text-md`,零新增令牌 | ✓ |
| 14 → 18px | 更近契约的 1.23× 比例,但按钮文字偏大 | |
| 不加字号,改加 padding | 按钮体量感来自 padding | |

**User's choice:** 14 → 16px
**Notes:** 契约写的是「`--text-xl` 16px vs `--text-base` 13px」,那是 13px 锚点世界的 1.23×;现锚点 14px,16px 即 1.14×,恰好是正文本体大小,不夸张。

### Q4 — 实心按钮的 `:disabled` 态怎么处置?

| Option | Description | Selected |
|--------|-------------|----------|
| 沿用 0.55,零改动 | 0.55 对实心是更强的淡化,区分度反而上升 | ✓ |
| 实心按钮用更低值(如 0.4) | 补偿实心填充的视觉重量 | |
| disabled 退回淡底形态 | 语义最清晰,但最远于 Pitfall M5 | |

**User's choice:** 沿用 0.55
**Notes:** Pitfall M5 明写「`:disabled` 是 G3 前提条件**唯一**的视觉信号,不得软化」,而 `#btn-authorize` 的 disabled 态正是「四处机械校验尚未全部通过」的唯一视觉表达。同一档 0.55 作用在实心绿底+白字上得到的是明显的去饱和,作用在淡底上则是几乎消失的浅灰——对实心按钮是**更强**的淡化。

---

## 标记体系

### Q1 — VISUAL-04 的活动态范围怎么定?

| Option | Description | Selected |
|--------|-------------|----------|
| 三选一活动 + AI 面板折叠态 | 前三个用 `:not(.hidden)`;`#ai-panel` 用自身的展开/折叠态 | ✓ |
| 只做三个互斥面板 | `#ai-panel` 完全不碰 | |
| 给 AI 面板引入 JS 状态 | 需改 `app.js`,属范围外 | |

**User's choice:** 三选一活动 + AI 面板折叠态
**Notes:** `#ai-panel` **从不被 `.hidden`**(`grep -n "aiPanel" app.js` 零命中),它的折叠是 `#ai-panel-body` 上的 `.collapsed`(`app.js:1562-1565`),所以 `:not(.hidden)` 只能表达三者互斥。VISUAL-04 字面的「四个面板的活动/非活动态可区分」在纯 CSS 推导下**无法照做**,而 ROADMAP 的 Rationale 明确要求「无需 JS 状态属性」。需登记对 REQUIREMENTS 措辞的修正。

### Q2 — 活动态的标记形态怎么定?

| Option | Description | Selected |
|--------|-------------|----------|
| 左侧 accent 竖条 + 标题变色 | 实现用 `box-shadow: inset` 避免布局位移 | ✓ |
| 只改标题颜色/字重 | 最轻,但区分度很弱 | |
| 整块背景换底 | 最显眼,但侧栏多一块色块 | |

**User's choice:** 左侧 accent 竖条 + 标题变色
**Notes:** 冻结轮的琥珀 inset 竖线已是现成先例。另注意到:非活动面板是 `display: none`(**根本看不见**),所以「可区分」实际退化为「当前活动的那一个看得出是活动的」。

### Q3 — VISUAL-03 怎么收口?

| Option | Description | Selected |
|--------|-------------|----------|
| 认定已实现,仅复证 | qrq 已把 `#doc-panel-header h1` 降到 14px/500/muted;只更正 gate 里的选择器名 | ✓ |
| 再降到 12px | 更像纯标签,但 12px 是全站最小档 | |
| 去掉字重档(500→400) | 更安静,但差异极弱 | |

**User's choice:** 认定已实现,仅复证
**Notes:** `#doc-pane` 这个选择器**在代码库里不存在**(唯一命中是 `check-05-ui-uat.py:720` 的一句注释)。实际元素 `#doc-panel-header h1` 已是 14px / 500 / `#646464`,源码注释即「安静的容器标签,不是全屏最大最重的文字」。连带效果:灰区 2 定下 `.markdown-body h1` = 28px 后,全屏最大文字是文档自己的 h1(28) > `.overlay-card h3`(24,模态) > 文档 h2(22)——页面级层级已立住。

### Q4 — 活动态竖条与两处 SVG 的用色怎么定?

| Option | Description | Selected |
|--------|-------------|----------|
| 竖条用蓝,图标跟文字色 | 与警告琥珀、冻结琥珀明确分离 | ✓ |
| 竖条用琥珀(契约原意) | 最贴已签核的 60/30/10 表 | |
| 竖条用中性灰 | 零语义撞车,但可见度最低 | |

**User's choice:** 竖条用蓝,图标跟文字色
**Notes:** 契约把 active-panel marker 划进 Accent(10%)保留域(与 `#state-badge`、`mark` 同组),而该系统的 accent 是琥珀——但琥珀同时是**警告色**(`--color-action-warning`)与**冻结轮标记色**,加「活动面板」即三重撞车。选蓝是对契约 60/30/10 表的**刻意偏离**,需登记。

---

## 收尾:三处未裁定的细节

### Q1 — 蓝色竖条用哪个令牌?

| Option | Description | Selected |
|--------|-------------|----------|
| 新开诚实命名的令牌 | 与消费者同提交;不复用名不副实的令牌 | ✓ |
| 复用 `--color-action-primary` | 零新增令牌,但「主要动作」的名被用于面板指示器 | |
| 放弃蓝色,改用中性令牌 | 零命名问题,但可见度最低 | |

**User's choice:** 新开诚实命名的令牌
**Notes:** 项目为「名必须说实话」付过代价——04.1 D-03 把 26 个 primitive 全部改名,理由正是「保留旧名会让名说谎」。现有令牌里**没有一个**的名字说的是「活动标记」。具体名由规划期定(建议 `--color-marker-active`)。

### Q2 — 两处图标的实现机制用哪个?

| Option | Description | Selected |
|--------|-------------|----------|
| 改用 `mask-image` | 图标真正跟随令牌;L-3 例外可撤掉 | ✓ |
| 照契约用 `content: url()` | 最贴契约,但「跟文字色」只是人工同步的约定 | |
| 搬到 DOM SVG | 需改 `renderAnnotations` / `renderVerdictCard`(不得触碰) | |

**User's choice:** 改用 `mask-image`
**Notes:** 与上一条选择**直接冲突**的技术事实:data-URI 经 `content` 渲染为**图片**,不继承页面 CSS,`currentColor` 不可用,契约只能把 fill 钉死为转义 hex(`%23555555`,旧 gray-700 的值,与当前 `--color-text-secondary` `#646464` **有色差**)——那让「跟文字色」成为人工同步的约定而非机制。mask 方案用令牌上色、SVG 当蒙版,附带收益是 `<path>` 不带 `fill` 即可(mask 只看 alpha),data-URI 里零颜色信息,**契约的字面量例外 L-3 可以整个撤掉**。代价:伪元素从内联字形变盒模型,对齐需实测。这是对契约已写死机制的刻意偏离。

### Q3 — 新开两档的令牌名怎么定?

| Option | Description | Selected |
|--------|-------------|----------|
| `--text-2xl` / `--text-3xl` | 跟随 `xs/base/md/lg/xl` 递进 | ✓ |
| 用途名 `--text-h1` / `--text-h2` | 名直接说出用在哪,但刻度混用两套命名法 | |
| 重排现有档位 | 违反硬规则 3,且静默改变 `--text-xl` 的 3 处消费者 | |

**User's choice:** `--text-2xl` / `--text-3xl`
**Notes:** 契约里的 `--text-2xl` 指 18px、`--text-3xl` 指 22px(在旧的六档刻度上取的),现在 18px 已被 `--text-lg` 占用,照契约名会得到**名同值不同**的 `--text-2xl = 22px`。此差异必须在围栏注释里写清楚。

### Q4 — 两处图标的形状风格与尺寸怎么定?

| Option | Description | Selected |
|--------|-------------|----------|
| 实心 12×12,`vertical-align: -2px` | mask 下实心在 12px 不糊 | ✓ |
| 实心 14×14 | 与文字同高,但显重 | |
| 轮廓线 16×16 | 最轻,但细线可能断 | |

**User's choice:** 实心 12×12,`vertical-align: -2px`
**Notes:** 契约只给了骨架(`viewBox='0 0 16 16'` + `<path d='…'/>`),`d` 与渲染尺寸都没给。mask 只看 alpha,实心形状在 12px 下比轮廓线清晰得多;`vertical-align: -2px` 是契约原值。具体 path 数据由规划期定。

---

## Claude's Discretion

- 竖条令牌的**具体名字**(建议 `--color-marker-active`)与它指向的 Radix 步。
- 三段坡道中 commit 与 irreversible **具体取哪两个 Radix 步**(green-9 / green-10 的分配)。
- 两处图标的 **`d='…'` path 数据**(实心图钉 / 实心地图标记的常规形状)。
- 竖条宽度(建议 3px)、标题变色改的是 `color` 还是 `color` + `font-weight`。
- 围栏内注释的措辞与粒度(尤其「契约 `--text-2xl`=18px vs 现 22px」与比率配对表)。

## Deferred Ideas

- `.collapse-indicator` 的越轨字面量与 `check-05-ui-uat.py:588` 的陈旧文案 —— backlog `999.1`,本阶段不修(Pitfall 7 把触碰该元素的范围锁死为两处 `content:` emoji)。
- hover / active / transition 态 —— Phase 7(`INTERACT-01` / `INTERACT-02`)。
- 布局结构常量 / 窄窗口 / 滚动容器 / 命中区 —— Phase 6。
- 暗色模式 —— v2 `TOKEN-V2-01`。
- `#probe-controls` 的移除或重定位 —— 产品行为变更,不进本里程碑。
- 本阶段无 todo 匹配(`todo.match-phase 5` 返回 0),无折叠或审阅项。
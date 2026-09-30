# Phase 11: 去卡片化与发丝分隔线 - Context

**Gathered:** 2026-09-28
**Status:** Ready for planning

<domain>
## Phase Boundary

把 v1.15 Phase 9 落地的**卡片语言整体反转**:左栏 4 个 section(`#session-panel` / `#annotations-panel` / `#checks-panel` / `#ai-panel`)与右栏 `#doc-panel` 不再绘制容器边界(`border` / `box-shadow` / `border-radius` 从这 5 个容器上移除),面板底色与页面底色统一为同一档,12px 灰缝归零,分区改由 1px 发丝线承担。界面读作**一张连续的平面**。

**同步(承重,与反转是同一次改动):** `check-09` 的 c1..c4 逐条断言卡片语言、反转后必红,须改写为断言新契约并以变异测试证明会失败;`check-02` 的 2 条卡片地面 PAIR 按实际绘制面重新归属;`check-05 --item 8` 的 sticky 余量在 `#doc-panel` 边界改动后复测登记。

**本阶段只做**:连续面 + 底色统一 + 灰缝归零 + 发丝线 + 三条门禁同步义务 + 处置本次反转自己孤立掉的令牌。

**本阶段不做**:G2、`999.2`、暗色模式(`A11Y-V2` / `FLOW-V2` / `TOKEN-V2`)、Nyquist 缺口、图标与空状态、`.overlay-card` 底色、`G1-01`(归 Phase 12)、`REG-04` / `VIS-01`(归 Phase 12)。后端与 `frontend/app.js` / `frontend/index.html` 预期**逐字节不改**。

</domain>

<decisions>
## Implementation Decisions

> **来源:** 本文件是 `/gsd-discuss-phase 11` 的产物(2026-09-28),四个灰区由用户在 `AskUserQuestion` 中**逐项选定**。ROADMAP 的 Phase 11 段已锁定范围、Deliverables 与 Success Criteria;本文件只补 ROADMAP 里仍是「候选 / 待定」的实现决定。**凡本文件与 ROADMAP 措辞冲突处,以本文件为准**(见 D-11-4)。

### 统一面(承载 SURF-02 + Deliverable 6)

- **D-11-1:** 统一面 = **白 `#ffffff`**。`--color-surface-page`(`frontend/style.css:139`)的值由 `var(--radix-gray-3)` 就地改写为 `var(--white)`。理由三条:①gray-3(`#f0f0f0`)**比内陷面 gray-2(`#f9f9f9`)更暗**,保留现值即违反已裁定的 SC2(「gray-2 仍是唯一比统一面更暗的一档」);②白面最贴用户点名的参照物(ChatGPT);③白面比 gray-1 对中间调前景更安全 —— 实测 gray-1 上 `--color-marker-active` 4.65 / `--color-border-strong` 3.24,而白面更高。 — **Reversibility:** costly — 撤销要连带重算 `check-02` 的六条页面地面 PAIR(`style.css:561` / `:571` / `:576` / `:620` / `:659` / `:689`)与其 Phase 9 登记账目,并重写 c3 判据。
- **D-11-2:** **面板 / `#doc-panel` / `#doc-panel-header` 改消费 `--color-surface-page`**;`--color-surface-card`(`:334`,3 处消费者 `:754` / `:774` / `:816`)与 `--shadow-card`(`:335`,2 处 `:757` / `:776`)**双双删除**。**方向说明:** 是把卡片档并回页面档,不是反向(页面去消费卡片令牌)—— 与 SC2 措辞同向,也避免「页面令牌指向卡片令牌」的语义错位。 — **Reversibility:** costly — 撤销要恢复两条声明、删除残留断言、并把 2 条 PAIR 的地面标签改回去。
- **D-11-3:** **已核实的两个「不产生新孤儿」事实**(planning 期实测,planner 不必重查):`--radix-gray-1` 保持零消费 ⇒ G2 的事实基底**一字不动**;`--radix-gray-3` 除 `--color-surface-page` 外还有 `--color-surface-sunken`(`:140`)与 `--color-surface-hover`(`:209`)两个消费者 ⇒ 页面换值**不会**造出新的零消费 primitive。`--radix-gray-2` 恰一个消费者(`--color-surface`,`:208`),不动。
- **D-11-4:** 删除两个令牌后,**按 Phase 10 先例各加一条专用残留断言**(参照 `scripts/check-10-idi10-validation.py:406` 的 `r1`:`fenced.count("--radius-lg") == 0` 同型,即断言围栏内不再出现 `--color-surface-card` / `--shadow-card` 的声明)。**不得**顺手补一条**通用的**围栏消费断言 —— 那正是 G2,已由用户明确排除在 v1.16 范围外。

### 几何与密度(承载 SURF-03)

- **D-11-5:** **`#main-pane > section { max-width: 768px }`(`:753`)与 `#main-pane { align-items: center }`(`:727`)两条都保留不动。** 侧沟由「面板与页面同色」消除 —— 沟在几何上仍在,但透出的已是同一档白,**不可见**。
  **⚠ 这是对 ROADMAP Deliverable 3「一并处置」措辞的显式收窄。** 已裁定的判据是 **SC3 的原文**「主区内容列**不再露出**左右灰沟」—— 由色统一满足,不是由删除声明满足。**下游 verifier 不得按 Deliverable 3 的旧措辞判失败**;planner 须在计划里显式论证「这两条仍在工作(控行长 / 定位置),只是不可见」,不得把它们写成「已死声明」。
  **用户裁定的理由:** 保留两条 = 零水平位移、零回归风险,且居中列仍是 ChatGPT 式;去掉居中会让内容贴左、右侧留大片白;两条都删会让行长变长、`.markdown-body` 长段落与表格可读性下降。 — **Reversibility:** reversible — 两条声明原地未动,若日后要改只是删/改声明。
- **D-11-6:** **`.panel-body { padding: var(--space-4) }`(`:857`)保持 16px 不动。** 去卡片化删的是「容器边界」,不是「内容呼吸」;且 c4 的「面板内边距」断言可原值保留(少一处改写)。Phase 9 的 D-9-2 只反转**间距那一半**(gap → 0)。 — **Reversibility:** reversible。
- **D-11-7:** **`.panel-header { border-radius: var(--radius-md) }`(`:841`)归零**(就地改写为 `0`)。理由:活动面板标记是 `inset 3px 0 0 var(--color-marker-active)` 的竖条(`:1630-1633`),10px 圆角会把竖条上下端剪成收尖的弧 —— 它今天不可见**只是因为 `.panel-header` 无背景色**,那是巧合,不是设计。`#doc-panel-header { border-radius: 0 }`(`:816`)本就已是显式零值,**一字不动**。
- **连带后果(事实,非决定,须由运行时读数确认):** 灰缝归零 + 卡片四边 border 收成横线,竖向预算**净多出约 41px**(`gap` 12px→0 省 36px;5 个容器由 2px/个的上下 border 变成 3 条 1px 横线,省 5px)。这是 1px 级几何变化,**不得靠推断**,须由真实浏览器的 computed style / 几何读数确认没顶破命中区与滚动普查。

### 发丝线(承载 DIV-01 / DIV-02 / DIV-03)

- **D-11-8:** 线取 **`--color-border-subtle`(gray-6 `#d9d9d9`)**。实测白面上 NON-TEXT 1.412;它已是 `.event-list` / `.annotation-item` / `.badge-answered` / `#latest-check` 四处的边界色 ⇒ **零新增令牌、零新增颜色值**。备选 `--color-border`(gray-7 `#cecece`,1.574)未采用:它更重,且其两处卡片消费者搬走后只剩 `:1084`(blockquote 左竖条)一个,语义会从「卡片边界」漂成「引用条」。 — **Reversibility:** reversible — 换令牌是一处字面量替换。
- **D-11-9:** **竖线 = `#doc-panel` 的 `border-left: 1px solid var(--color-border-subtle)`。** 零新增 DOM 元素、零位移,天然跨满 `#doc-panel` 整高(`#app` 是 `align-items: stretch` 的 flex 行),`.collapsed` 的 48px 竖条态也仍在。**`#doc-panel` 的 `overflow-y: auto` 保留**(它是右列的滚动者,L-1 的 sticky 表头依赖它仍是最近的可滚祖先;删它会同时打破 `check-05 --item 9` 的滚动者普查,期望值是 4 不是 3)。**`#doc-panel-header` 的 `background` 保留、只改归属**(不加背景则滚动正文从标题行底下穿过)。
- **D-11-10:** **横线 = `#main-pane > section + section { border-top: 1px solid var(--color-border-subtle) }`,只 3 条**(面板之间);第一个面板顶部**不画**(顶部是窗口边缘,画了会读成多一条)。
  **DOM 顺序已核实**(`frontend/index.html`):`#session-panel` → `#annotations-panel` → `#checks-panel` → `#ai-panel`。`section + section` 恰命中后三个;且当中间两个带 `.hidden` 时,`#ai-panel` 仍带自己的上边线 ⇒ **两种显隐状态下都恰好 1 条可见分界**,不依赖可见性(相邻选择器按 DOM 相邻判定,不按渲染相邻)。
- **D-11-11:** **`#doc-panel-header` 下缘不加线。** SURF / DIV 只枚举了两种线(主区↔文档区竖线 + 面板间横线),表头下缘是第三种,超出本阶段枚举范围;且「白表头压在白面板上、滚动正文凭空消失」是 **Phase 9 起就存在**的行为,不是本次引入的。
- **连带后果(事实,非决定):** ①横线的宽度 = **内容列宽(768px、居中)**,不是主区全宽 —— 因为 `#main-pane > section` 的宽度受 `max-width: 768px` 约束(见 D-11-5),这与 ChatGPT 的分隔线随内容列等宽是一致的。②`#doc-panel` 由四边 `border` 收成单边 `border-left`,content box **水平 +1px、垂直 +2px** —— 这正是 `REG-03` 要登记的 sticky 余量变化成因。

### 门禁改写口径(承载 REG-01 / REG-02 / REG-03)

- **D-11-12:** **c1..c4 以真实浏览器的 `getComputedStyle` 计算读数为判据;令牌解析降为 `info()` 诊断。** 逐条断言面:
  - **c1** — 4 个 section 的 `box-shadow === "none"`、`border-radius === "0px"`、除发丝线所在边外 `border-*-width === "0px"`;**同一份读数里给出交互控件对照组**(按钮 / 输入框 / `select` / `#check-switcher` / `.overlay-card` 仍有各自圆角与边界)—— 否则「移除边界」可能是把整站边界一起抹掉。**注意:`.panel-header` 不是这 5 个容器之一,它有 `inset 3px 0 0` 的活动标记 box-shadow,断言不得波及它。**
  - **c2** — `#doc-panel` 的计算 `box-shadow === "none"`、`border-radius === "0px"`、四边中仅 `border-left-width === "1px"`;`overflow-y` 仍为 `auto`;`#doc-panel-header` 的 sticky 与背景仍成立。
  - **c3** — `body` 的计算底色 **== 面板的计算底色**(同值),且 `--color-surface`(gray-2)解析值**仍比统一面更暗**。**三级刻度的故事改写成两级**(统一面 > 内陷面),不得保留 gray-3 页面档的旧断言。
  - **c4** — `#main-pane` 计算 `gap === "0px"`;发丝线的计算宽度 `=== "1px"` 且色为 `--color-border-subtle`;`.panel-body` 计算 `padding === "16px"`。
  **为何以此为准:** REQ 的可观测判据就是「屏幕上不再有边界」,计算读数直接证明它;而**令牌解析有一个本项目实测过的静默陷阱** —— `ok()` 在**期望侧为 `None` 时降级成 BLOCKED(exit 2,本项目当良性码)**,文案还指向 DOM。令牌一旦删除,旧式「断言解析值」不会变红,而是静默变成「良性阻塞」。 — **Reversibility:** costly — 撤销要重写四条判据并重跑六条变异。
- **D-11-13:** **变异测试做 6 条,每条判据双向覆盖**(在已提交的树上做,定向 `git checkout -- frontend/style.css` 还原 —— **禁用 `git stash`**,它跨工作树共享、本项目明令禁止;还原后须逐字节相同):
  1. c1 — 给 `#main-pane > section` 加回 `border` / `box-shadow` ⇒ 必 FAIL
  2. c2 — 给 `#doc-panel` 加回四边边界 ⇒ 必 FAIL
  3. c2 — 删掉 `#doc-panel` 的 `overflow-y: auto` ⇒ 必 FAIL
  4. c3 — 把统一面改回 `--color-surface`,使内陷档塌掉 ⇒ 必 FAIL
  5. c4 — 把 `gap` 改回 12px ⇒ 必 FAIL
  6. c4 — 删掉发丝线规则 ⇒ 必 FAIL
  c5 的滚动契约在改动后复跑并确认仍成立。**每条须给出「变异 → FAIL」的真实读数**,不得只声明做过。
- **D-11-14:** **发丝线不登记 NON-TEXT 对比度对**,但**必须在计划里逐条论证**「分隔线不标识任何控件 / 状态 ⇒ SC 1.4.11 不适用」(沿用 Phase 10 就「装饰性边界」已写明的判据)。**该论证不得省略、不得默认。** 反证:gray-6 在白面上仅 1.412,若按 NON-TEXT 阈值 3.0 判即 FAIL;要让线达标就得换 gray-9(`#8d8d8d`,3.319),那会把 hairline 变成深灰框,与去卡片化的目标相反。
- **D-11-15:** **`check-02` 的地面记账**:2 条卡片地面 PAIR(`:632` `--color-marker-active` TEXT / `:643` `--color-border-strong` NON-TEXT)改记为**统一面** `--color-surface-page` 并重算;六条页面地面 PAIR(`:561` / `:571` / `:576` / `:620` / `:659` / `:689`)以 HEAD 内容逐条重算并登记。**非刷新旧值、非调色、非放宽阈值**;`TEXT_MIN` / `NON_TEXT_MIN` 与改动前**逐字节相同**,`ORDER` 断言不退化。
- **D-11-16:** **`check-05 --item 8` 的 sticky 余量**(实测恰 `1.000px`,成因是 Phase 9 给 `#doc-panel` 加的 1px 上边框)在本阶段移除该边框后**复测**;余量读数与成因须登记。**不成立时按「事实是否被改变」分诊**:若判据描述的事实(sticky 表头遮挡)仍成立 ⇒ 只更新余量读数与成因登记;若事实被破坏 ⇒ 同步更新判据并说明改了什么。**不得为了让旧数字继续成立而回退那 1px。**

### Claude's Discretion

- **竖线承载盒**:D-11-9 定为 `#doc-panel` 的 `border-left`。若运行时读数显示它顶破了某条门(例如 `check-05` 对 `#doc-panel` 实测宽的断言),可在**保持四条不变式**(零新增 DOM、零位移、跨满高、取既有语义令牌)的前提下改用 `#main-pane` 的 `border-right`;偏离须在计划里说明判因。
- **`--color-border`(gray-7)的语义注释**:卡片消费者搬走后它只剩 `:1084` 一个消费者,是否补注释说明语义漂移,由 planner 定。
- **`#doc-panel-header { border-radius: 0 }` 的论证注释**(其「卡片四角」前提已随本阶段消失)是否更新措辞,由 planner 定 —— **声明本身一字不动**。
- **变异测试的执行顺序与还原手法细节**(须满足 D-11-13 的三条硬性要求)。
- **`REG-04` 的连带指纹面份数**:改写 `check-09` 会把该脚本的覆盖者拖进重验名单,**份数须在磁盘上逐份读 `covered_files` 实测**(判据锚 frontmatter 的 `covered_files` **逐行匹配**,不是全文 grep;并额外测「路径是否还在盘上」)。Phase 10 曾以「不得改 `check-05-ui-uat.py`」避免把 `idi-08` 拖进来 —— 本阶段**先实测再处置,不得凭记忆断言份数**。`REG-04` 本身归 Phase 12。

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 权威设计与需求

- `DESIGN.md` — 唯一权威设计文档(v1.14 界面信息架构改版)。本阶段直接相关:D-04(令牌纪律:只声明被消费的令牌)、D-06(零构建步骤 / 零新增运行时依赖)、§3.8(面向用户的输出语言红线)
- `.planning/REQUIREMENTS.md` — v1.16 的 12 条需求。Phase 11 覆盖 SURF-01 / SURF-02 / SURF-03 / DIV-01 / DIV-02 / DIV-03 / REG-01 / REG-02 / REG-03;`REG-04` / `G1-01` / `VIS-01` 归 Phase 12。**Out of Scope 表与「阶段归属的裁定理由」段必读**
- `.planning/ROADMAP.md` — Phase 11 段:Goal / Rationale / Deliverables 1-6 / Success Criteria 1-5 / Avoids / Gates。**注意 D-11-5 对 Deliverable 3 措辞的收窄**
- `.planning/PROJECT.md` — v1.16 里程碑目标、候选池、已移出 Out of Scope 的项(G1)

### 被反转的既有裁定(必读,不得重开)

- `.planning/milestones/v1.15-phases/idi-09-card-containers/09-CONTEXT.md` — **D-9-1 / D-9-2 / D-9-3 正是本阶段反转的对象**。含规划期实测的容器底色读数表、8 条页面地面 PAIR 在 gray-3 上的重算表、以及「重新归属配对而非调色」的论证模板
- `.planning/milestones/v1.15-phases/idi-10-tables-and-radius-scale/10-CONTEXT.md` — 删 `--radius-lg` 的**专用残留断言先例**、`frontend/style.css` 连带指纹的**实测形状**(10 份覆盖 / 1 份可执行)、编辑纪律、门禁环境事实(必读,省得重踩)
- `.planning/milestones/v1.15-MILESTONE-AUDIT.md` — G1 的原始判据与 14 项待裁定项清单。Phase 11 只需知道 `#latest-check` 的**宿主绘制面在本阶段变**(G1-01 归 Phase 12)

### 被改写的门与探针

- `scripts/check-09-idi09-validation.py` — **本阶段的承重改写对象**(552 行)。现状:c1 断言 `--color-surface-card` 解析为白 + `--shadow-card == 用户裁定值`;c2 断言 `#doc-panel` 卡片语言 + `#doc-panel-header` 对照组;c3 断言 `body` 计算底色 gray-3 + 三级亮度严格递增;c4 断言 `gap 12px` + `.panel-body` 16px;c5 断言滚动契约。`ITEMS` 表在 `:477`
- `scripts/check-02-contrast.py` — 围栏内 PAIR 清单与 `TEXT_MIN` / `NON_TEXT_MIN` 阈值。2 条卡片地面 PAIR 在 `frontend/style.css:632` / `:643`;六条页面地面 PAIR 在 `:561` / `:571` / `:576` / `:620` / `:659` / `:689`。**围栏内注释不得出现「令牌名 + 冒号」**(`DECL_RE` 扫围栏全文含注释)
- `scripts/check-05-ui-uat.py` — `--item 8`(sticky 余量恰 1.000px)与 `--item 9`(滚动者普查,期望 4)。**改它会把它自己的覆盖者拖进重验名单**(Phase 10 曾以「不得改它」避免把 `idi-08` 拖进来)
- `scripts/check-10-idi10-validation.py` — `:406` 的 `r1` 是**专用残留断言**的先例(`fenced.count("--radius-lg") == 0`);`:428` / `:649` 是「令牌解析为 None」的登记手法
- `scripts/check-01-token-conformance.sh` / `scripts/check-03-hidden-uniqueness.sh` / `scripts/check-04-important-count.sh` — 三条恒不变式(令牌块外零裸 `#hex` 与零 tier-1 引用;`^\.hidden {` 恒为 1;`!important` **声明**数恒为 1)

### 被改动的源码(行号均为当前 HEAD)

- `frontend/style.css` — `:139`(`--color-surface-page`,换值)、`:334-335`(两个待删令牌)、`:725`(`#main-pane` 的 `gap`)、`:727`(`align-items: center`,保留)、`:751-758`(`#main-pane > section`)、`:768-776`(`#doc-panel`)、`:813-818`(`#doc-panel-header`)、`:837-846`(`.panel-header`)、`:857`(`.panel-body`)、`:925-935`(`.event-list`,内陷面,不动)、`:1084`(`--color-border` 的剩余消费者)、`:1630-1633`(活动面板标记的 `inset 3px 0 0`)
- `frontend/index.html` — 只读:`#main-pane` 的 4 个 section 的 DOM 顺序(相邻选择器的判据)
- `frontend/app.js` / 后端 — **预期逐字节不改**。偏离此预期是选错实现方式的信号

### 截图取证(Phase 12 消费,本阶段只需知道样本存在)

- `scripts/ui-states/` — p1 / p12 / p3 / checking / archive 五个样本(VIS-01 的 5 张 1440×900 整窗截图)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets

- `frontend/style.css` 的**单一 `:root` 令牌围栏** — 一切改动要么在围栏内改值、要么在围栏外的规则体内改声明;零新增 primitive、零新增颜色值
- `--color-border-subtle`(gray-6)已是四处内陷容器的边界色 ⇒ 发丝线直接复用,无需新令牌
- `check-05` 的 `read_style()` / `resolve_token()` / `ok()` / `info()` 辅助函数与 `check-09` 既有的 `load_check05()` 复用机制可直接沿用
- `check-10` 的 `r1`(`:406`)是**专用残留断言**的现成写法

### Established Patterns

- **就地改写,不追加覆盖** — Phase 9 对 `#doc-panel` 的 `border-left`、Phase 10 对表格 `border` 用的是同一手法。留下已死的声明会让注释与代码互相矛盾
- **追加,不重排** — 至少一对等特异性规则由源码顺序决定;重排即渲染变更,而源码 diff 看起来完全无辜
- **每个 `style.css` 计划必须带至少一项运行时验证** — 真实浏览器的 computed style 读数;`grep -c 'var(--'` 对渲染结果零证明力
- **门禁纪律** — 一条不能失败的门比没有门更糟;删除断言 / 放宽阈值 / 降级为恒真 / 只断言「规则被写下了」全部禁止;**变异测试是唯一能证明守卫真的会失败的手段**
- **删除令牌必配专用残留断言**(Phase 10 删 `--radius-lg` 的先例)
- **计数门的算术陷阱** — `check-04` 数的是 `!important;` **声明**数(恒为 1),不是命中行数;解释性注释的散文会把 `grep -c` 顶高(本项目已因此红过三次)。围栏外的机械判据是子串计数,连论证性散文都会把它顶高

### Integration Points

- `scripts/check-09-idi09-validation.py` 是 Phase 9 自建的运行时门,**断言的正是本阶段要移除的语言** ⇒ 承重改写点;反转后 c1..c4 必红,那正是门在正确工作的证据
- `scripts/check-02-contrast.py` 的地面标签与 `scripts/check-01-token-conformance.sh` 的围栏扫描是静态面
- `#doc-panel` 的 `overflow-y: auto` 同时是 L-1 sticky 表头与 `check-05 --item 9` 滚动者普查的依赖 ⇒ 承重声明
- 活动面板标记(`inset 3px 0 0` on `.panel-header`)是去卡片后**仅存的活动态视觉线索**,不得被本次改动波及

</code_context>

<specifics>
## Specific Ideas

- **参照物:ChatGPT 界面。** 用户 2026-09-28 原话:「分块太割裂了,完全没有联动性…chatgpt 的界面就是一根细的衬线来分割不同的分区,我们的确实很大的一块」。**一根细线**是本次的核心隐喻 —— 不是靠留白分区,是靠线。
- **范围裁定(用户,2026-09-28,逐项):** 视觉方向 = 全站去卡片;落地方式 = 走 GSD 新阶段;范围 = 去卡片化**连带 G1**;跳过领域研究。
- **反转而非新增:** 反转对象是一次**已 shipped 的用户裁定**(D-9-1 / D-9-2 / D-9-3)。本阶段**不重开**底色关系、密度、圆角与卡片语言这四项决策,只执行反转与门禁同步。
- **中间态不可接受:** 只去卡片不留线 = 把 4 个面板之间承载层次的 12px 灰缝一并抹掉、分区彻底消失 —— 比任一终点都差。故 SURF 与 DIV 必须同阶段落地。

</specifics>

<deferred>
## Deferred Ideas

- **`.overlay-card` 的底色**(Phase 9 停放的开放项,用户 2026-09-27 与 2026-09-28 两次均未点名)—— 页面变白后它会读作「内陷一档」;是否改白底同族仍待裁定。**不得顺手一起改**
- **G2**(`--radix-gray-1` 零消费 + 补一条**通用的**围栏消费断言)—— 用户只裁定「连带 G1」,**G2 未点名**,留待下一里程碑。本阶段只处置本次反转自己孤立掉的两个令牌
- **`999.2`**(Phase 7 交互态暴露的三条 affordance 缺陷)—— 未点名;执行它会作废 `idi-07` 的 `passed` 指纹
- **`A11Y-V2-01/02` / `FLOW-V2-01/02` / `TOKEN-V2-01`**(暗色模式)—— 均未点名,v1.14 已显式排除
- **Nyquist 缺口**(`idi-04` / `idi-06` / `idi-09` / `idi-10` 无 `VALIDATION.md`)—— 未点名;建议走 `/gsd-validate-phase`,不占本里程碑范围
- **图标与空状态** —— 用户 2026-09-27 与 2026-09-28 两次均未点名,仍留 Out of Scope
- **`check-05` 其余 item 在 1px 几何变化下的复跑范围** —— 本次讨论未展开;`REG-04`(Phase 12)会以「复跑零新增失败」覆盖,但**本阶段就须对受 1px 几何影响的 item 做实测**(不得推断)
- **`REG-04` 的连带指纹面份数** —— 改 `check-09` 会把该脚本的覆盖者拖进重验名单,份数须实测;`REG-04` 本身归 Phase 12

</deferred>

---

*Phase: 11-去卡片化与发丝分隔线*
*Context gathered: 2026-09-28*

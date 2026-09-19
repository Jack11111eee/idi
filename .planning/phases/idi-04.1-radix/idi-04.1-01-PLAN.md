---
phase: idi-04.1-radix
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - frontend/style.css
  - scripts/check-05-ui-uat.py
autonomous: true
requirements:
  - TOKEN-01
  - TOKEN-02
  - TOKEN-04
  - TOKEN-07
  - CHECK-02
  - CHECK-03
  - CHECK-04
  - A11Y-04
  - A11Y-04b

estimate:
  tokens: 95000
  raw_tokens: 95000
  tasks: 3
  confidence: low

must_haves:
  truths:
    # ---- lifted from idi-04.1-UI-SPEC.md `## UI Considerations` — explicit tier (30) ----
    - "E2 闸门/循环动作按钮的 loading 态内容与结构未被本阶段改动(本阶段只改颜色值,不改任何选择器与文案;由 app.js/index.html 零 diff 门 + CHECK-03/CHECK-04 守住)← UI-SPEC UI-Considerations E2 `loading`(explicit)"
    - "E2 闸门/循环动作按钮的 error 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E2 `error`(explicit)"
    - "E3 主/危险实心按钮的 loading 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E3 `loading`(explicit)"
    - "E3 主/危险实心按钮的 error 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E3 `error`(explicit)"
    - "E9 输入区(composer)的 empty 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E9 `empty`(explicit)"
    - "E9 输入区的 loading 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E9 `loading`(explicit)"
    - "E9 输入区的 error 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E9 `error`(explicit)"
    - "E9 输入区的 partial 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E9 `partial`(explicit)"
    - "E10 .overlay-card 的 empty 态内容与结构未被本阶段改动(本阶段只恢复其 box-shadow 声明)← UI-SPEC UI-Considerations E10 `empty`(explicit)"
    - "E10 .overlay-card 的 loading 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E10 `loading`(explicit)"
    - "E10 .overlay-card 的 error 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E10 `error`(explicit)"
    - "E10 .overlay-card 的 populated 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E10 `populated`(explicit)"
    - "E10 .overlay-card 的 partial 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E10 `partial`(explicit)"
    - "E10 .overlay-card 的 zero-one-many 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E10 `zero-one-many`(explicit)"
    - "E11 #annotation-listed 的 empty 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E11 `empty`(explicit)"
    - "E11 #annotation-listed 的 loading 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E11 `loading`(explicit)"
    - "E11 #annotation-listed 的 error 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E11 `error`(explicit)"
    - "E11 #annotation-listed 的 populated 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E11 `populated`(explicit)"
    - "E11 #annotation-listed 的 partial 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E11 `partial`(explicit)"
    - "E11 #annotation-listed 的 zero-one-many 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E11 `zero-one-many`(explicit)"
    - "E12 #checks-panel 的 empty 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E12 `empty`(explicit)"
    - "E12 #checks-panel 的 loading 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E12 `loading`(explicit)"
    - "E12 #checks-panel 的 error 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E12 `error`(explicit)"
    - "E12 #checks-panel 的 populated 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E12 `populated`(explicit)"
    - "E12 #checks-panel 的 partial 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E12 `partial`(explicit)"
    - "E12 #checks-panel 的 zero-one-many 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E12 `zero-one-many`(explicit)"
    - "E14 #selection-menu 的 loading 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E14 `loading`(explicit)"
    - "E14 #selection-menu 的 error 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E14 `error`(explicit)"
    - "E15 #ai-route-select 的 loading 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E15 `loading`(explicit)"
    - "E15 #ai-route-select 的 error 态内容与结构未被本阶段改动 ← UI-SPEC UI-Considerations E15 `error`(explicit)"
    # ---- lifted from idi-04.1-UI-SPEC.md `## UI Considerations` — backstop tier (28) ----
    - statement: "E1 事件类别芯片:在窄事件行内渲染全部七个芯片,无标签换行或裁切。"
      verification: backstop
    - statement: "E1 事件类别芯片:200% 缩放下每个芯片标签保持单行,且 --color-kind-fg 在七个底色上均可读(CHECK-02: 4.61–16.29)。"
      verification: backstop
    - statement: "E2 闸门/循环动作按钮:在最窄支持面板宽度下,六按钮行换行而非溢出面板。"
      verification: backstop
    - statement: "E2 闸门/循环动作按钮:最长的闸门标签(授权撰写总设计文档)不裁切,其 green-12-on-green-3 标签保持可读(CHECK-02: 11.00)。"
      verification: backstop
    - statement: "E3 主/危险实心按钮:最窄面板下「认可雏形」/「重新检测」的 white-on-blue / white-on-red 实心标签不裁切。"
      verification: backstop
    - statement: "E4 #state-badge:最长 streaming 状态串不裁切其胶囊。"
      verification: backstop
    - statement: "E4 #state-badge:其 --color-text-info 在 --color-surface-info 上保持 ≥4.5:1(4.53),且恢复的 z-index 使其仍在横幅之上。"
      verification: backstop
    - statement: "E5 #doc-panel / #doc-panel-body:长到需要滚动的文档滚动面板体,而非页面。"
      verification: backstop
    - statement: "E5 #doc-panel / #doc-panel-body:面板底(#f9f9f9)与页面底(#fcfcfc)读起来可区分 —— 04.1-N-7 的 delta 正是要看的东西。"
      verification: backstop
    - statement: "E6 提示/弱化文字面:折行后的多行 .hint 与长引用块不裁切。"
      verification: backstop
    - statement: "E6 提示/弱化文字面:折行后弱化灰在四个底色上均保持 ≥4.5:1(CHECK-02: 5.19–5.82)。"
      verification: backstop
    - statement: "E7 #round-doc.round-frozen:长到需要滚动的历史轮次,其琥珀色 inset 竖线仍钉在块边缘。"
      verification: backstop
    - statement: "E7 #round-doc.round-frozen:冻结轮标记在新值 #4f3422 下读作清晰的琥珀褐色竖线(CHECK-02: 10.80),且轮次切换器显示历史轮次。"
      verification: backstop
    - statement: "E8 #stream-banner:长的致命错误信息在横幅内折行,而不是溢出它。"
      verification: backstop
    - statement: "E8 #stream-banner:琥珀警告底与红色致命底在长信息下都保持其前景 ≥4.5:1。"
      verification: backstop
    - statement: "E9 输入区:极长的不可断消息撑高或滚动输入区,而不是溢出它。"
      verification: backstop
    - statement: "E9 输入区:长草稿下 --shadow-composer 仍读作一条清晰边缘,且 placeholder 保持可读。"
      verification: backstop
    - statement: "E10 .overlay-card:档位模态与确认对话框在其最长内容下仍适配视口。"
      verification: backstop
    - statement: "E10 .overlay-card:.tier-desc 在满不透明度下(R-3)在 blue-11 上保持可读(4.77),且 --shadow-overlay 可读。"
      verification: backstop
    - statement: "E11 #annotation-listed:大量长批注滚动该列表,而不是面板。"
      verification: backstop
    - statement: "E12 #checks-panel:大量检查项滚动该面板,而不是页面。"
      verification: backstop
    - statement: "E13 归档视图:长归档文档在归档态压暗下不裁切。"
      verification: backstop
    - statement: "E13 归档视图:0.75 压暗下的正文保持 ≥4.5:1(CHECK-02: 6.97)。"
      verification: backstop
    - statement: "E14 #selection-menu:在面板边缘附近打开的选区菜单重新定位而非裁切。"
      verification: backstop
    - statement: "E14 #selection-menu:长菜单项不截断其标签。"
      verification: backstop
    - statement: "E15 #ai-route-select:带最长路由标签时不截断该标签。"
      verification: backstop
    - statement: "E16 mark:跨行断点的 mark 连续段在两行上都保持其 amber-3 底色。"
      verification: backstop
    - statement: "E16 mark:长 mark 连续段上的文字保持 ≥4.5:1(CHECK-02: --color-text on --color-surface-mark = 15.88)。"
      verification: backstop
    # ---- phase-specific truths ----
    - "`frontend/style.css` 仍只有**一个** `:root` 块,由 `/* ===== DESIGN TOKENS: START ===== */` 与 `/* ===== DESIGN TOKENS: END ===== */` 界定;围栏内 tier-1 恰为 25 条、`--color-*` 恰为 47 条(HEAD: 26 / 49)← TOKEN-01 / D-02 收窄 / R-4"
    - "围栏内零裸 `#hex` 之外的东西不变:围栏外 `bash scripts/check-01-token-conformance.sh` 打印 `PASS`(裸 hex 计数 0)← TOKEN-04 / CHECK-01"
    - "tier-1 名不再说谎:`--gray-600` 这一族 Tailwind 式名全部消失,取而代之的是 `--radix-<family>-<step>`(唯一例外 `--white`,它没有 Radix 步对应且名字不说谎)← D-03 / 04.1-N-6"
    - "`python3 scripts/check-02-contrast.py` 打印 `PASS: 0 failures`,并逐行给出 43 条配对(34 TEXT / 9 NON-TEXT)+ 一行 `ORDER 0.363` ← CHECK-02 / D-15 / UI-SPEC `### The measured table`"
    - "`--color-text-muted` 与 `--color-text` 成为同一族的相邻两步(`--radix-gray-11` / `--radix-gray-12`),AA 倒退在**声明处**被刻度消解,而不是靠手调更深的灰 ← A11Y-04 / V-6 / 04.1-N-1"
    - "`--color-border-strong` 由 `#d9d9d9`(1.41:1,SC 1.4.11 失败)变为 `--radix-gray-9` `#8d8d8d`(3.24 / 3.15),把用户签核的 S-3 意图以 Radix 步恢复 ← A11Y-04 / V-5"
    - "`#state-badge { z-index: var(--z-badge) }` 恢复后,`--z-badge` 重新有消费者,围栏内断言的 `badge < banner` 序关系两端都被真实消费(TOKEN-07 的断言不再空转)← TOKEN-07 / R-1 / D-11"
    - "`.overlay-card { box-shadow: var(--shadow-overlay) }` 恢复,且 `--shadow-overlay` 在同一次提交内于围栏中声明并消费 —— 围栏外无裸 `rgba()` ← R-2 / Hard Rule 5"
    - "`.tier-desc` 的 `opacity: 0.9` 被删除(白字@0.9 on blue-11 = 4.17 ✗;满不透明度 = 4.77 ✓),而其 `font-size` / `font-weight` 一字未动 ← R-3 / S-6 / A11Y-04b"
    - "`grep -c '^\\.hidden {' frontend/style.css` == 1 且 `grep -c '!important;' frontend/style.css` == 1 ← CHECK-03 / CHECK-04"
    - "围栏内每个 `var(--x)` 都能解析到围栏内已声明的 `--x`,且每个已声明的颜色令牌都有一个消费者(Gate 2 双向为空)← Hard Rule 5 / Pitfall 1"
    - "运行时:`#state-badge` 的 computed `z-index` 等于运行时解析出的 `--z-badge`;`.overlay-card` 的 computed `box-shadow` 不为 `none`;`.tier-desc` 的 computed `opacity` 为 `1` ← 硬规则 7 / R-1 / R-2 / R-3"

  artifacts:
    - path: "frontend/style.css"
      provides: "围栏 `:root`:25 个 tier-1 Radix primitive(24 个 `--radix-*` + `--white`)、47 个 `--color-*` 语义令牌、新增 `--shadow-overlay`、43 条 `/* PAIR */` + 1 条 `/* ORDER */` 清单、重写的围栏注释;围栏外三处声明变更(R-1/R-2/R-3)"
      contains: "===== DESIGN TOKENS: START ====="
    - path: "scripts/check-05-ui-uat.py"
      provides: "item_smoke 新增三条令牌接线的运行时断言(R-1 z-index / R-2 box-shadow / R-3 opacity)"
      contains: "def item_smoke"

  key_links:
    - from: "frontend/style.css 的 43 条 `/* PAIR */` 清单"
      to: "frontend/style.css 围栏内的令牌声明"
      via: "check-02-contrast.py 对未声明名 `sys.exit(1)`,故清单与令牌块无法漂移;raw `/* PAIR` 标记数必须等于解析数"
      pattern: "/\\* PAIR --color-"
    - from: "--color-text-muted"
      to: "--radix-gray-11"
      via: "tier-2 → tier-1 的 var() 链(AA 倒退在声明处被刻度消解)"
      pattern: "--color-text-muted: var\\(--radix-gray-11\\)"
    - from: "#state-badge 的 z-index"
      to: "--z-badge"
      via: "R-1 恢复的唯一消费者,使围栏内 `badge < banner` 的序断言两端都被消费"
      pattern: "z-index: var\\(--z-badge\\)"
    - from: ".overlay-card 的 box-shadow"
      to: "--shadow-overlay"
      via: "R-2:令牌与消费者同一次提交落地,围栏外不留裸 rgba()"
      pattern: "box-shadow: var\\(--shadow-overlay\\)"
    - from: "scripts/check-05-ui-uat.py 的 item_smoke"
      to: "frontend/style.css 的令牌值层"
      via: "resolve_color / resolve_token 在运行时解析令牌,再与消费者的 computed 值比对(值层改动不产生假 FAIL)"
      pattern: "resolve_(color|token)"

  prohibitions:
    - statement: "不得改动 `frontend/app.js` 与 `frontend/index.html` 的任何一个字节 —— 硬规则 5 明写 `app.js` 约 70 个顶层 `getElementById` 句柄的 id 不得改名或删除"
      status: active
      verification: flagged
    - statement: "`frontend/vendor/` 必须仍只含 `marked.min.js`;不得 vendor Radix 的 CSS、不得新增任何文件、依赖或构建步骤(D-01 / 硬规则 6)"
      status: active
      verification: flagged
    - statement: "不得重排 `style.css` 的任何规则或声明,只允许原位追加/删除(硬规则 3「追加不重排」:至少一对等特异性规则由源码顺序决定,重排即渲染变更而 diff 看起来完全无辜)"
      status: active
      verification: flagged
    - statement: "不得改 S-1 间距 12 档、S-2 字号档(含 `--text-base` = 14px)、圆角刻度、`--z-*` 的四个值、`.hidden` 规则与 `!important` 声明数(D-12 / 硬规则 1·2·4;S-1…S-4 已签核,不得重开)"
      status: active
      verification: flagged
    - statement: "不得软化 8 处 `:disabled` 的 `opacity: 0.55 / 0.5` —— SC 1.4.3 豁免非活动组件,且它是 G3 前提条件唯一的视觉信号(Pitfall M5)"
      status: active
      verification: flagged
    - statement: "不得改 `--color-action-irreversible*` 的消费者 —— 仍只有 `#btn-authorize`,且不得执行三族差异化(那是 Phase 5 的一行式值编辑)"
      status: active
      verification: flagged
    - statement: "不得为改善比值而 round / 改写任何 Radix hex,也不得采信 Radix 自己的 AA 论断替代 `check-02-contrast.py` 的实测仲裁(携带项 #4 / 04.1-N-2)"
      status: active
      verification: flagged
    - statement: "不得为「恢复层级」把 `--color-text-muted` 调得比 `--radix-gray-11` 更深 —— 那是 04-UI-SPEC N-1 的陷阱换新衣,且会打破 AA 配对(04.1-N-1)"
      status: active
      verification: flagged
    - statement: "不得在围栏外留下裸 `rgba()`;`.overlay-card` 的影子必须经 `--shadow-overlay`,且该令牌必须与消费者同一次提交落地(Hard Rule 5)"
      status: active
      verification: flagged
    - statement: "不得给 `#state-badge` 添加 `position:` —— 它被刻意设计为不是 `position: fixed` 浮层(style.css:460-462),R-1 只恢复 `z-index` 这一条声明"
      status: active
      verification: flagged
    - statement: "不得改 `.tier-desc` 的 `font-size` / `font-weight` —— R-3 只删除 `opacity: 0.9` 一条声明"
      status: active
      verification: flagged
    - statement: "不得改动任何用户可见文案 —— 本阶段 copy 零改动"
      status: active
      verification: flagged
    - statement: "不得改任何 tier-2 `--color-*` 名(唯一例外是 R-4 删除的 `--color-text-inverse` 与 `--color-surface-info-strong`);D-02 的 49 名冻结收窄为 47,且该收窄已由用户于 2026-09-19 签核(S-5)"
      status: active
      verification: flagged
    - statement: "不得重开 S-5 / S-6 或执行 S-1…S-4 的任何一行式替代方案 —— 六项均已签核,是输入而非待议问题"
      status: active
      verification: flagged
---

<!-- planner-discipline-allow: opacity: 0.9 -->
<!-- 本计划正文必须写出字面量 `opacity: 0.9`,因为 R-3 的任务就是删除 `.tier-desc` 上这一条
     精确声明(执行器需要知道删哪一条),而 Task 3 的验收对源文件做 `grep -c 'opacity: 0.9' == 0`
     来证明删净。字面量在此是承重的,不是散漫的散文引用。 -->

<objective>
把 `frontend/style.css` 的颜色**值层**从手调 hex 换成 Radix Colors 的 12 步语义刻度,并据此重算围栏内的 `/* PAIR */` 对比度清单;同时恢复 `260918-qrq` 删掉的两条声明并删除一条由算术强制的声明。

Purpose: 这是 Phase 4 **结构产出**之上的值层重写。结构不动 —— 围栏位置与标记、75 个令牌的分层结构、四条守卫命令、`.hidden` 唯一性、`!important` 声明数 = 1。改的只是值,但值承载着三件事:①`--color-text-muted` 3.23:1 的 AA 倒退(`.hint` / `.badge-answered` / 批注正文全站受影响);②idi-04 UAT 的 3 项 FAIL 中属于颜色漂移的那一批;③`--color-border-strong` 1.41:1 的 SC 1.4.11 失败(用户签核的 S-3 意图被 `260918-qrq` 的值层换血抹掉)。三件事都靠**刻度**而不是靠再手调一次灰来解决。

Output: 值层已换成 Radix 的 `frontend/style.css`;`check-02-contrast.py` 在 43 条重算配对上 `PASS: 0 failures`;围栏外三处声明变更(R-1 / R-2 / R-3)落地并带运行时证据;`scripts/check-05-ui-uat.py` 的 `item_smoke` 新增三条令牌接线断言。

**D-15 的三数差异(必须在围栏注释中说明,见 Task 2):** ROADMAP Phase 4 写 **24** 对(20 文本 + 4 非文本),那是 Phase 4 规划期的目标数;磁盘现状是 **34** 对(29 TEXT + 5 NON-TEXT)+ 1 ORDER,那是 Phase 4 执行期实际落地的数;本阶段 goal 与重算结果都是 **43** 对(34 TEXT + 9 NON-TEXT)+ 1 ORDER。三个数字的差异不是漂移,而是「清单枚举真实发生的组合」这条契约在三代值层上各算了一次 —— 每次值层改动都会改变哪些组合真实发生。

**本阶段关闭 vs 沿用的需求口径:** 本阶段**真正关闭**的是 A11Y-04(AA 倒退在声明处消解)、A11Y-04b(四处 opacity 裁定中 `.tier-desc` 一处被算术强制删除、另三处复核后不变)、TOKEN-07(z-index 序断言重新有消费者)、CHECK-02(清单按新值层重算并实测通过);**沿用/重验**的是 TOKEN-01(单一围栏、零依赖)、TOKEN-02(改名后仍不出围栏,并由 Plan 02 补上守卫)、TOKEN-04、CHECK-03、CHECK-04。**本阶段不触碰** TOKEN-03、TOKEN-05、TOKEN-06、TOKEN-08(含义清单、间距、圆角、字号刻度 —— D-12 明令不动)。
</objective>

<execution_context>
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/workflows/execute-plan.md
@/Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/idi-04.1-radix/idi-04.1-CONTEXT.md
@.planning/phases/idi-04.1-radix/idi-04.1-PATTERNS.md
@.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md
@.planning/phases/idi-04-tokens-contract/04-UI-SPEC.md
@.planning/phases/idi-04-tokens-contract/idi-04-UAT.md
@frontend/style.css
@scripts/check-02-contrast.py
</context>

<tasks>

<task type="tracer">
  <name>Task 1 (tracer): 围栏值层与对比度清单的原子重写 —— Radix 步 + 43 对清单</name>
  <files>frontend/style.css</files>
  <read_first>
    - `frontend/style.css` L1-L230 —— 围栏现状:26 个 tier-1 primitive(L8-L33)、49 个 `--color-*`(L36-L103)、34 条 `/* PAIR */` + 1 条 `/* ORDER */`(L159-L222)、两条 `:root` 围栏标记(L5 / L224)
    - `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` `### Tier 1 — primitives` —— **25 条的完整名/步/hex/消费者表,逐字转抄的唯一来源**
    - `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` `### Tier 2 — semantic` —— 47 个 `--color-*` 的 Radix 值映射表(名冻结、只改右侧 `var()` 目标)
    - `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` `### The manifest, verbatim — ready to write into the fence` —— **43 条 `/* PAIR */` + 1 条 `/* ORDER */` 连同其分节注释的逐字清单**
    - `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` `### The role bands, and the three places the arithmetic overrides them` 与 `### The four computed results a naive Radix port gets wrong` —— 四步越轨的算术依据
    - `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` `### opacity rulings` —— `.tier-desc` 与 8 处 `:disabled` 的裁定
    - `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` `## Carry-Forward Obligations` 第 1/2/3/4 条 —— 清单替换、`PASS: 0 failures`、CHECK-01 仍为 0、hex 逐字转抄
    - `.planning/phases/idi-04.1-radix/idi-04.1-CONTEXT.md` D-02 / D-03 / D-04 / D-06…D-09 / D-15 / D-16
    - `scripts/check-02-contrast.py` —— 解析契约:`DECL_RE` / `PAIR_RE` / `ORDER_RE` / `VAR_RE`、未声明名 `sys.exit(1)`、raw `/* PAIR` 标记数必须等于解析数、覆盖率下限 24/20/4、闭区间比较
    - `frontend/app.js` —— **D-16 的核实对象**:所有动态构建 `<button>` 的路径(重点 `renderVerdictCard`,约 `app.js:709-713`)与所有 muted-text 类(`.hint` / `.badge-answered` / `.annotation-note` / `.annotation-answer-body` / `.verdict-suggestion`)的使用点
  </read_first>
  <action>
    **第 0 步 —— D-16 前置核实(必须先做,结论写进 SUMMARY)。** 在 `frontend/app.js` 中穷举所有创建 `<button>` 的路径(至少覆盖 `renderVerdictCard` 的「修」/「接受现状」两处、`renderEvent`、`appendChatMessage`、以及任何 `createElement("button")` / `innerHTML` 含 `<button` 的写法),并穷举五个 muted-text 类在 `app.js` 与 `frontend/index.html` 中的全部使用点。判定:是否存在任何 muted-text 类元素落在 `<button>` 内部。把逐条 `文件:行号` 证据与结论写进 SUMMARY。**若结论为「不成立」**(即确实存在 muted-text 类元素落在 `<button>` 内部,与 UI-SPEC 04.1-N-4 / D-16 的记载相反):**停止并上报,不得自行把该对写回清单。** 本任务的全部闸门、UI-SPEC `### The manifest, verbatim` 的逐字清单、以及 `### The measured table` 都是 **43 对**(34 TEXT + 9 NON-TEXT)+ 1 ORDER;写回该对会变成 44 对,与它们全部冲突 —— 那不是执行器的裁量范围,而是与已签核事实的冲突。把逐条 `文件:行号` 证据写进 SUMMARY,并在返回中标记该冲突交由用户裁决,不要静默偏离。若结论为「成立」(与 UI-SPEC 的记载一致):该对不进清单,`--color-surface-hover` 继续与 `--color-sunken` 共享 `--radix-gray-3`。

    **第 1 步 —— tier-1:26 → 25 条,改名 + 换值。** 严格按 UI-SPEC `### Tier 1 — primitives` 表执行,逐字转抄 hex(不得 round、不得「顺手」调整)。具体:
    - 删除 `--black: #000000;`(L9)—— `--color-kind-done` 改指 `--radix-gray-12` 后它没有消费者,而 Hard Rule 5 禁止声明不消费的 primitive。
    - 删除 `--green-800: #1f5c3a;`(L19)—— 它是 Phase 5 的脚手架,本轮整体改名换值后其前提消失(V-13 / 04.1-N-2 取代前作 N-2)。
    - 删除 L12 那条解释「与 --gray-700 同值:AA 倒退为用户知情决策」的注释 —— 它解释的值本身被换掉,留着就是说谎。
    - 其余 24 个 primitive 名改为 `--radix-<family>-<step>` 并写入表中的 hex。锚点示例(完整 25 条以 UI-SPEC 表为准):`--radix-gray-1: #fcfcfc`、`--radix-gray-3: #f0f0f0`、`--radix-gray-9: #8d8d8d`、`--radix-gray-11: #646464`、`--radix-gray-12: #202020`、`--radix-blue-11: #0d74ce`、`--radix-green-11: #218358`、`--radix-green-12: #193b2d`、`--radix-amber-12: #4f3422`、`--radix-red-11: #ce2c31`、`--radix-violet-11: #6550b9`。
    - `--white: #ffffff;` **保留原名原值**(04.1-N-6:Radix 亮色刻度里没有白色,它的名字不说谎)。
    - 只声明本阶段真正消费的步(D-04):**不得**补齐完整的 1-12 步。

    **第 2 步 —— tier-2:49 → 47 条,名逐字冻结,只改右侧目标。** 按 UI-SPEC `### Tier 2 — semantic` 表逐个重定向。锚点:`--color-text: var(--radix-gray-12)`、`--color-text-muted: var(--radix-gray-11)`、`--color-text-secondary: var(--radix-gray-11)`、`--color-surface-page: var(--radix-gray-1)`、`--color-surface: var(--radix-gray-2)`、`--color-surface-hover: var(--radix-gray-3)`、`--color-surface-sunken: var(--radix-gray-3)`、`--color-surface-user: var(--radix-gray-4)`、`--color-border-strong: var(--radix-gray-9)`、`--color-border: var(--radix-gray-7)`、`--color-border-subtle: var(--radix-gray-6)`、`--color-action-primary: var(--radix-blue-11)`、`--color-action-warning: var(--radix-amber-12)`、`--color-action-warning-surface: var(--radix-amber-2)`、`--color-surface-warning-subtle: var(--radix-amber-1)`、`--color-surface-mark: var(--radix-amber-3)`、`--color-border-warning-subtle: var(--radix-amber-6)`、`--color-kind-command: var(--radix-amber-11)`、`--color-action-{routine,commit,irreversible}: var(--radix-green-11)`、`--color-action-{routine,commit,irreversible}-surface: var(--radix-green-3)`、`--color-action-{routine,commit,irreversible}-fg: var(--radix-green-12)`、`--color-kind-done: var(--radix-gray-12)`、`--color-kind-read: var(--radix-violet-11)`、`--color-border-success: var(--radix-green-11)`、`--color-border-streaming: var(--radix-blue-11)`、`--color-surface-danger: var(--radix-red-2)`、`--color-border-danger-subtle: var(--radix-red-7)`、`--color-surface-info: var(--radix-blue-2)`、`--color-text-info: var(--radix-blue-11)`、`--color-surface-streaming: var(--radix-blue-2)`。
    - **删除两条声明连同它们的注释**(R-4 / 04.1-N-8):`--color-surface-info-strong`(L91)与 `--color-text-inverse`(L101),以及 L88-L90 与 L99-L100 那两段「保留它是因为 check-02 清单按名引用它」的注释 —— 清单重算后该理由变成假的,留着就是「一条对代码说谎的注释」。
    - `--color-overlay-backdrop: rgba(0, 0, 0, 0.45)` 与 `--shadow-composer` **值一字不改**(它们不是 Radix 值)。
    - **不得**在此任务新增 `--shadow-overlay` —— 它必须与 `.overlay-card` 的消费者同一次提交落地(Hard Rule 5),那在 Task 3。

    **第 3 步 —— 清单整块替换。** 把 L159-L222 的清单块(含其分节注释)**整块替换**为 UI-SPEC `### The manifest, verbatim` 的逐字内容:43 条 `/* PAIR ... */` + 1 条 `/* ORDER --color-text-muted BEFORE --color-text ON --color-surface */`,顺序、注释、缩进与 UI-SPEC 一致。硬约束:`/* PAIR` 与 `/* ORDER` 标记前缀被 `check-02-contrast.py` 原样计数并必须等于解析数,故**任何散文注释里都不得出现 `/* PAIR` 或 `/* ORDER` 字样**;清单条目只写令牌名,绝不写 hex;`@<alpha>` 只允许出现在 `TEXT` 条目上;`ORDER` 的两个操作数必须是同底上的**普通 TEXT** 条目(新清单里是 `--color-text-muted ON --color-surface` 与 `--color-text ON --color-surface`)。

    **贯穿三条纪律:** ①全部改动都在围栏内**原位**替换,只追加/删除行,绝不移动任何规则或声明(硬规则 3);②每一步之后 `bash scripts/check-01-token-conformance.sh` 与 `bash scripts/check-03-hidden-uniqueness.sh` / `bash scripts/check-04-important-count.sh` 都必须仍 PASS;③本任务结束时 `check-02-contrast.py` 必须绿 —— 它是本阶段的仲裁者,不是「稍后再修」的东西。
  </action>
  <verify>
    <automated>python3 scripts/check-02-contrast.py</automated>
    <fails_when>非零退出,或任一行以 `FAIL` 开头,或末行不是 `PASS: 0 failures`</fails_when>
    <automated>python3 scripts/check-02-contrast.py | grep -c '^PASS  '</automated>
    <fails_when>计数不等于 43,或输出中出现 `FAIL: unknown token`</fails_when>
    <automated>python3 scripts/check-02-contrast.py | grep -c '^ORDER 0.363'</automated>
    <fails_when>计数不等于 1</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh</automated>
    <fails_when>任一条非零退出,或任一条的 stdout 不含 `PASS`</fails_when>
    <automated>awk '/===== DESIGN TOKENS: START/{f=1} /===== DESIGN TOKENS: END/{f=0} f' frontend/style.css | grep -cE '^  --(white|radix-[a-z]+-[0-9]+): #'</automated>
    <fails_when>计数不等于 25</fails_when>
    <automated>awk '/===== DESIGN TOKENS: START/{f=1} /===== DESIGN TOKENS: END/{f=0} f' frontend/style.css | grep -cE '^  --color-[a-z0-9-]+:'</automated>
    <fails_when>计数不等于 47</fails_when>
    <automated>grep -c '/\* PAIR ' frontend/style.css; grep -c '/\* ORDER ' frontend/style.css</automated>
    <fails_when>两个计数不是 43 与 1</fails_when>
    <automated>comm -23 <(grep -o 'var(--[a-z0-9-]*' frontend/style.css | sed 's/var(//' | sort -u) <(grep -o '\-\-[a-z0-9-]*:' frontend/style.css | sed 's/:$//' | sort -u)</automated>
    <fails_when>输出非空(存在引用了未声明令牌的 var())</fails_when>
    <automated>comm -23 <(grep -oE '^[[:space:]]*--color-[a-z0-9-]+:' frontend/style.css | tr -d ' :' | sort -u) <(grep -o 'var(--[a-z0-9-]*' frontend/style.css | sed 's/var(//' | sort -u)</automated>
    <fails_when>输出非空(存在已声明但零消费者的 `--color-*` 令牌 —— Hard Rule 5 禁止)。范围**刻意**限定在 `--color-*` 声明:非颜色的 tier-2 令牌在本任务结束时本就还没有消费者 —— `--z-badge` 的消费者是 Task 3 的 R-1,`--shadow-overlay` 由 Task 3 与消费者同一次提交落地 —— 把整个声明集纳入会让闸门在一个正确的中间态上失败。Phase 级 `<verification>` 里的反向 comm 覆盖全部声明,那一条在所有任务之后运行</fails_when>
    <automated>awk '/===== DESIGN TOKENS: START/{f=1} /===== DESIGN TOKENS: END/{f=0} !f' frontend/style.css | grep -c '#[0-9a-fA-F]\{3,6\}'</automated>
    <fails_when>计数不为 0(围栏外出现裸 hex)</fails_when>
    <automated>grep -cE '^  --(gray|green|blue|amber|red|purple)-[0-9]+:|^  --black:' frontend/style.css; grep -c -- '--color-text-inverse\|--color-surface-info-strong' frontend/style.css</automated>
    <fails_when>第一个计数不为 0(Tailwind 式 tier-1 名或 --black 仍在),或第二个计数不为 0(两条待删声明或其注释仍在)</fails_when>
  </verify>
  <acceptance_criteria>
    - `python3 scripts/check-02-contrast.py` 退出码 0,stdout 含 43 行 `PASS  `、0 行 `FAIL`,末行为 `PASS: 0 failures`,且含 `ORDER 0.363` —— 逐条比值与 UI-SPEC `### The measured table — all 43 pairs` 一致
    - 围栏内 tier-1 颜色 primitive 恰 25 条(24 个 `--radix-<family>-<step>` + `--white`);`--black` 与 `--green-800` 均不存在
    - 围栏内 `--color-*` 声明恰 47 条;`--color-text-inverse` 与 `--color-surface-info-strong` 及其注释均已删除
    - 围栏内 `/* PAIR ` 标记恰 43 个、`/* ORDER ` 恰 1 个,且与解析数相等(check-02 的 raw-count 守卫为证)
    - `--color-text-muted: var(--radix-gray-11)` 与 `--color-text: var(--radix-gray-12)` 逐字成立
    - `--color-border-strong: var(--radix-gray-9)` 逐字成立
    - 围栏外裸 hex 计数为 0;每个 `var(--x)` 都能解析到围栏内声明的 `--x`
    - `grep -c '^\.hidden {'` == 1 且 `grep -c '!important;'` == 1
    - SUMMARY 中写有 D-16 的逐条 `文件:行号` 核实证据与结论(成立 → 该对不进清单,清单为 43 对;不成立 → 停手上报冲突,不得自行写回该对)
    - `git diff --name-only HEAD -- frontend/app.js frontend/index.html` 输出为空
  </acceptance_criteria>
  <done>围栏的值层已整体换成 Radix 步,43 条清单在 `check-02-contrast.py` 上 `PASS: 0 failures`(含 `ORDER 0.363`),三条结构守卫仍 PASS,围栏外零裸 hex、零未解析 `var()`;D-16 已按 `app.js` 的动态渲染核实并留证。</done>
</task>

<task type="auto">
  <name>Task 2: 围栏注释 V-12 —— 步语义、名↔步映射、四处越轨说明与 D-15 的三数差异</name>
  <files>frontend/style.css</files>
  <read_first>
    - `frontend/style.css` L1-L230 —— Task 1 之后的围栏现状(注释现状是 L8、L13、L15-L19、L35、L45-L46、L62、L70、L73、L94、L98、L105、L119-L122、L126、L133-L134、L139、L145、L151-L153,以及 Task 1 写入的清单头注释)
    - `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` `### The role bands, and the three places the arithmetic overrides them` —— 四条越轨的**算术**依据(实心填充 9-10→11;边框 6-8→9;绿色 -fg 11-12→12;`--color-action-warning` 11-12→12)
    - `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` `### The four computed results a naive Radix port gets wrong` —— 上面四条逐条展开的测量值
    - `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` `## Notes` 04.1-N-1…04.1-N-8 —— 其中 N-1(ORDER 残差 0.363 不可修)、N-3(4.53 的 0.03 余量不得「改进」)、N-5(`--color-surface` 一名两用)、N-6(`--white` 是唯一非 `--radix-*` 名)、N-7(面板现在比页面略深是刻意的)是注释必须承载的内容
    - `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` `## Value-Layer Delta Ledger` —— V-1…V-13 / R-1…R-4 / C-1 的变更账本
    - `.planning/phases/idi-04.1-radix/idi-04.1-CONTEXT.md` D-03 / D-15 与 `### Claude's Discretion` 第三条(注释的措辞与粒度由执行器裁量)
    - `.planning/ROADMAP.md` §Phase 04.1 —— goal 原文与「非紧急插入」说明
  </read_first>
  <action>
    重写围栏内**块级注释**(不改任何声明、不改清单条目、不改围栏标记):

    1. **名↔步映射表。** 在 tier-1 区块上方写一段注释,给出「旧名 → `--radix-<family>-<step>` → 语义步带」的对照,使上游 Radix 更新时可机械同步(D-03 明写「映射关系靠围栏内注释记录」)。必须让 25 条 primitive 的族与步都可从注释中读出。

    2. **12 步语义与四处越轨。** 写一段注释说明 D-09 的角色步带(1-2 底 / 3-5 组件底 / 6-8 边框 / 9-10 实心填充 / 11-12 文字)是**工作假设**,并逐条记录它在**本项目的真实背景组合**上失效的四处:实心填充的每个载白字的填充面移到**第 11 步**(9/10 步在各族都过不了白字 4.5:1:blue-9 3.26 / blue-10 3.63 / green-9 3.16 / green-10 3.55 / red-10 4.37 / amber-9 1.58;第 11 步是各族**最浅的通过值**);`--color-border-strong` 移到**第 9 步**(6-8 步在 `--color-surface` 上最好也只有 gray-8 1.82,过不了 SC 1.4.11 的 3:1);三个绿色 `-fg` 移到**第 12 步**(green-11 在 green-3 上 4.21 ✗);`--color-action-warning` 移到**第 12 步**(amber-11 在 amber-2 上 4.43 ✗、在 gray-1 上 4.49 ✗)。

    3. **D-15 的三数差异。** 在清单块头注释里补一句说明:ROADMAP Phase 4 写 24 对、Phase 4 落地时磁盘上是 34 对、本阶段重算后是 43 对(34 TEXT + 9 NON-TEXT)+ 1 ORDER;差异来源是「清单枚举**真实发生**的组合」这条契约在三代值层上各算了一次,不是漂移。

    4. **三处不得被「好心改回」的地方。** ①`--color-text-muted` 不得取更深的值 —— 它是第 11 步,第 10 步在 `--color-surface` 上只有 3.79(失败),而第 12 步被正文占用,所以 ORDER 比值 0.363 是刻度强制的,不是判断失误(04.1-N-1);②`--color-text-info` 在 `--color-surface-info` 上 4.53 只有 0.03 余量,它是**最浅的通过组合**,「更安全」的 `blue-12` 会毁掉 Pitfall-4a 规则,把底挪到 `blue-3` 反而掉到 4.25(04.1-N-3);③`--color-surface-hover` 与 `--color-sunken` 刻意共享 `--radix-gray-3`(04.1-N-4)。

    5. **围栏内必须出现的四个可 grep 锚点字符串**(措辞可自定,锚点不可省):`band 9-10`、`band 6-8`、`band 11-12`、`24 / 34 / 43`。它们分别锚定「越轨发生在哪个步带」与「D-15 的三数差异」。

    **硬约束:** 注释里**绝不得出现** `/* PAIR` 或 `/* ORDER` 字样(它们会被原样计数并与解析数比对,多一个就 FAIL);不得改围栏标记 `/* ===== DESIGN TOKENS: START/END ===== */` 的措辞;不得移动任何声明或规则(硬规则 3)。注释语言沿用围栏现状的混排风格:分节标题用英文,解释用中文。
  </action>
  <verify>
    <automated>python3 scripts/check-02-contrast.py</automated>
    <fails_when>非零退出,或末行不是 `PASS: 0 failures`(证明注释改动没有破坏标记计数)</fails_when>
    <automated>grep -c '/\* PAIR ' frontend/style.css; grep -c '/\* ORDER ' frontend/style.css; python3 scripts/check-02-contrast.py | grep -c '^PASS  '</automated>
    <fails_when>三个计数不是 43 / 1 / 43(注释里混进了标记字样,或清单被改动)</fails_when>
    <automated>grep -c -- 'band 9-10' frontend/style.css; grep -c -- 'band 6-8' frontend/style.css; grep -c -- 'band 11-12' frontend/style.css; grep -c -- '24 / 34 / 43' frontend/style.css</automated>
    <fails_when>四个锚点中任何一个的计数为 0</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh</automated>
    <fails_when>任一条非零退出,或任一条 stdout 不含 `PASS`</fails_when>
    <automated>grep -nE '^\s*--(white|radix-[a-z]+-[0-9]+):' frontend/style.css | wc -l; grep -nE '^\s*--color-[a-z0-9-]+:' frontend/style.css | wc -l</automated>
    <fails_when>两个计数不是 25 与 47(注释任务不得增删声明)</fails_when>
  </verify>
  <acceptance_criteria>
    - 围栏内含 `band 9-10` / `band 6-8` / `band 11-12` / `24 / 34 / 43` 四个锚点字符串各至少一次
    - 围栏内存在一段把 25 条 primitive 的族与 Radix 步对应起来的注释(可从注释中读出 `--radix-gray-11` 对应 gray 第 11 步、`--radix-amber-12` 对应 amber 第 12 步)
    - 围栏注释明确记录四条越轨及其算术,以及 `--color-text-muted` / `--color-text-info` / `--color-surface-hover` 三处「不得好心改回」的理由
    - `check-02-contrast.py` 仍 `PASS: 0 failures`,`/* PAIR ` 仍为 43、`/* ORDER ` 仍为 1
    - 围栏标记 `/* ===== DESIGN TOKENS: START ===== */` 与 `/* ===== DESIGN TOKENS: END ===== */` 各恰一行且措辞未变
    - 围栏内声明数未变(25 个 tier-1 颜色 primitive / 47 个 `--color-*`)
    - `git diff --numstat -- frontend/style.css` 的本任务增量中不含对任何 `--*: ...;` 声明行的增删
  </acceptance_criteria>
  <done>围栏注释承载了名↔步映射、12 步语义与四处越轨的算术、D-15 的三数差异、以及三处「不得好心改回」的警告;四个锚点字符串可 grep;`check-02-contrast.py` 仍 `PASS: 0 failures`。</done>
</task>

<task type="auto">
  <name>Task 3: 围栏外三处声明(R-1 / R-2 / R-3)与运行时接线证据</name>
  <files>frontend/style.css, scripts/check-05-ui-uat.py</files>
  <read_first>
    - `frontend/style.css` `.overlay-card` 规则(约 L421-L427)与 `#state-badge` 规则(约 L463-L470)与 `.tier-desc`(约 L851)与 `#stream-banner`(约 L473-L486)
    - `frontend/style.css` 围栏内 `--shadow-composer` 声明(约 L96)与 `#chat-input-row input` 的 `box-shadow: var(--shadow-composer)`(约 L635)—— 新 shadow 令牌要照抄的形状
    - `.planning/phases/idi-04.1-radix/idi-04.1-PATTERNS.md` §`frontend/style.css — #state-badge (L463-470), R-1` / §`.overlay-card (L421-427), R-2` / §`.tier-desc (L851), R-3` —— 三处的 analog 与「只动这一条声明」的纪律
    - `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` `## Value-Layer Delta Ledger` R-1 / R-2 / R-3 与 `### opacity rulings` 表
    - `.planning/phases/idi-04.1-radix/idi-04.1-UI-SPEC.md` `## Carry-Forward Obligations` 第 9 条 —— 运行时验证的具名清单
    - `scripts/check-05-ui-uat.py` `item_smoke`(约 L911-L937)、`resolve_color`(约 L250-L262)、`read_style`(约 L239-L241)、`ok` / `ok_true` / `ok_contains` / `blocked` / `info`(约 L85-L149)
  </read_first>
  <action>
    **围栏内(1 条新增声明):** 在 `--shadow-composer` 紧邻处新增 `--shadow-overlay: 0 8px 30px rgba(0, 0, 0, 0.2);`(R-2 的令牌形状,取自 UI-SPEC `### Tier 2` 表末行)。它必须与下面的消费者在**同一次提交**落地(Hard Rule 5);`--shadow-composer` 的值一字不改。

    **围栏外(恰好三处,均只动一条声明):**
    - **R-1** —— 在 `#state-badge` 规则内追加 `z-index: var(--z-badge);`。**不得**添加 `position:`:`#state-badge` 被刻意设计为不是 `position: fixed` 浮层(`style.css:460-462` 的注释已写明理由),`z-index` 在非定位元素上是惰性的,它的价值在于让 `--z-badge` 重新**有消费者**,从而让围栏 L151-L153 断言的 `badge < banner` 序关系两端都被真实消费(b9664e0 FIX 2 的承重关系)。
    - **R-2** —— 在 `.overlay-card` 规则内追加 `box-shadow: var(--shadow-overlay);`(形状照 `#chat-input-row input` 的 `box-shadow: var(--shadow-composer)`)。理由:令牌存在是为了让围栏外不出现裸 `rgba()`。
    - **R-3** —— 从 `.tier-desc` 规则中**删除** `opacity: 0.9;` 一条声明,规则其余部分(`font-size: var(--text-xs); font-weight: var(--fw-regular);`)逐字保留。理由:`.tier-desc` 位于 `.overlay-card button` 内,底色是 `--color-action-primary`(`#0d74ce`),白字@0.9 合成为 4.17 ✗;满不透明度 4.77 ✓;而把整个主 CTA 族压到 `blue-12` 是 Pitfall 4a 明令禁止的「为安全而过暗」。
    - 三处**都只追加/删除单条声明**,不重排、不改选择器、不改相邻规则(硬规则 3)。

    **运行时接线证据(硬规则 7 / 携带项 #9)。** 在 `scripts/check-05-ui-uat.py` 的 `item_smoke` 中**追加**三条令牌接线断言(不改动该函数已有的断言与 `info` 记录):
    - 新增一个小助手 `resolve_token(page, name)`:用 `page.evaluate` 读 `getComputedStyle(document.documentElement).getPropertyValue(name).strip()`,返回令牌的**运行时**值(与既有的 `resolve_color` 并列 —— 后者只能解析颜色,`--z-badge` 是数字)。
    - 断言 `#state-badge` 的 computed `z-index` 等于 `resolve_token(page, "--z-badge")`(R-1)。
    - 断言 `.overlay-card` 的 computed `box-shadow` 不为 `"none"` 且含 `0.2`(R-2)。
    - 断言 `.tier-desc` 的 computed `opacity` 等于 `"1"`(R-3)。
    - 元素缺失或令牌解析失败时,沿用既有 `blocked()` 语义(绝不记为 pass)。`.overlay-card` 与 `.tier-desc` 在 `index.html` 中静态存在,但若其 computed 值为 `None` 必须走 `blocked`。
    - 断言标签沿用该文件的中文风格,并在标签里写明令牌名(照 `item_smoke` 现有写法)。
  </action>
  <verify>
    <automated>grep -c 'z-index: var(--z-badge);' frontend/style.css</automated>
    <fails_when>计数不等于 1</fails_when>
    <automated>grep -c 'box-shadow: var(--shadow-overlay);' frontend/style.css; grep -c '^  --shadow-overlay: 0 8px 30px rgba(0, 0, 0, 0.2);' frontend/style.css</automated>
    <fails_when>两个计数不是 1 与 1</fails_when>
    <automated>grep -c 'opacity: 0.9' frontend/style.css; grep -c 'opacity: 0.55' frontend/style.css; grep -c 'opacity: 0.5;' frontend/style.css</automated>
    <fails_when>第一个计数不为 0(未删净),或第二/三个计数发生变化(误动了 :disabled 的豁免站点)</fails_when>
    <automated>grep -c 'position:' frontend/style.css; grep -n -A 8 '^#state-badge {' frontend/style.css | grep -c 'position'</automated>
    <fails_when>第二个计数不为 0(给 #state-badge 加了 position,违反 R-1 的边界)</fails_when>
    <automated>bash scripts/check-01-token-conformance.sh && bash scripts/check-03-hidden-uniqueness.sh && bash scripts/check-04-important-count.sh && python3 scripts/check-02-contrast.py | tail -1</automated>
    <fails_when>任一条非零退出,或末行不是 `PASS: 0 failures`</fails_when>
    <automated>.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,6</automated>
    <fails_when>退出码不为 0,或输出中出现 `FAIL`,或 `item smoke` 结论不是 `PASS`</fails_when>
    <automated>test -z "$(git diff --name-only HEAD -- frontend/app.js frontend/index.html)" && test -z "$(git ls-files --others --exclude-standard frontend/)" && test "$(ls frontend/vendor/)" = "marked.min.js"</automated>
    <fails_when>任一 test 非零退出(app.js/index.html 被改动、frontend/ 出现未跟踪文件、或 vendor/ 不再只有 marked.min.js)</fails_when>
    <automated>git diff --name-only HEAD -- . ':!.claude/settings.local.json'</automated>
    <fails_when>输出的文件清单超出 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`。**范围刻意排除 `.claude/settings.local.json`**:它是长期跟踪的会话本地文件,在本计划动手之前就已是 modified,不是本计划的产出、也不得被本计划提交;裸 `git diff --name-only HEAD` 会把它算成本计划的改动,那不是关于本计划的信号</fails_when>
  </verify>
  <acceptance_criteria>
    - `#state-badge` 规则内恰有一条 `z-index: var(--z-badge);`,且该规则内**无** `position` 声明
    - 围栏内恰有一条 `--shadow-overlay: 0 8px 30px rgba(0, 0, 0, 0.2);`,`.overlay-card` 规则内恰有一条 `box-shadow: var(--shadow-overlay);`
    - `grep -c 'opacity: 0.9' frontend/style.css` == 0,而 `opacity: 0.55` 与 `opacity: 0.5;` 的计数与本任务前一致(8 处 `:disabled` 未被软化)
    - `.tier-desc` 规则仍含 `font-size: var(--text-xs)` 与 `font-weight: var(--fw-regular)`
    - `.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,6` 退出码 0;`item smoke` 结论为 `PASS`(其中含新增的三条接线断言)
    - 四条守卫命令全部 PASS,`check-02-contrast.py` 仍 `PASS: 0 failures`
    - `git diff --name-only HEAD -- . ':!.claude/settings.local.json'` 只列出 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`(排除项是本计划动手前既有的工作树状态);`frontend/vendor/` 仍只有 `marked.min.js`
    - 本次改动全部为原位追加/删除,无任何规则重排(`git diff -- frontend/style.css` 中不出现被移动的既有规则块)
  </acceptance_criteria>
  <done>R-1 / R-2 / R-3 三处声明落地并各带一条运行时接线断言;`item smoke` 在真实浏览器里确认 `#state-badge` 的 z-index 接线、`.overlay-card` 的 box-shadow 存在、`.tier-desc` 的 opacity 为 1;四条守卫与 `check-02` 仍全绿。</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| 无新增边界 | 本阶段不引入网络面、不解析用户输入、不新增依赖、不新增文件。唯一的输入是**仓库内静态文本**(`frontend/style.css` 的围栏),唯一的消费者是本地浏览器与两个只读脚本 |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-idi041-01 | Tampering | `frontend/style.css` 围栏内的令牌值 | low | accept | 令牌值是仓库内静态文本,无运行时注入路径(应用不写 CSS 变量、不拼接 style 属性)。篡改者需要写权限,而写权限已经等于完全控制。不制造虚假的高危项 |
| T-idi041-02 | Tampering | 令牌值流向 `url()` / `content:` 汇点 | none | accept | 本阶段新增的 `--shadow-overlay` 与全部 Radix hex 只流向 `background` / `color` / `border-*` / `box-shadow`;`url()` 在本文件中只出现在两处 data-URI 图标(Phase 5),`content:` 只出现在 emoji 图标(Phase 5)。本阶段**不新增任何** `url()` / `content:` 汇点,故 CSS 值注入无可达汇点 |
| T-idi041-03 | Spoofing | tier-1 名改名为 `--radix-*` 后,围栏外可冒充 primitive | low | mitigate | D-03 的改名会让 `check-01-token-conformance.sh:37-39` 的交替式(`white\|black\|gray\|green\|blue\|amber\|red\|purple`)不再匹配 `var(--radix-…`,使 TOKEN-02 的守卫**静默空转而仍打印 PASS**。本计划以「围栏外 `comm -23` 未解析 var() 为空」+ 人工 diff 复核作为过渡证据;守卫本身的加固与变异证明在 `idi-04.1-02-PLAN.md`(wave 2,依赖本计划,不同文件) |
| T-idi041-04 | Repudiation | 「渲染未变」被断言而非证明 | low | mitigate | 本计划不为值层改动主张「渲染未变」—— 它主张的是**刻意的渲染变更**(V-4…V-11 的 Delta Ledger)。逐条运行时证据由 `item_smoke` 的三条新断言给出;完整的携带项 #9 运行时清单(含 `.hint` / `#btn-authorize` / `#ai-route-select` / `#selection-menu` 等)在 `idi-04.1-03-PLAN.md` 收口 |
| T-idi041-SC | Tampering | npm / pip / cargo 安装 | none | accept | **本阶段不安装任何包。** D-01 明确禁止 vendor Radix 的 CSS,色值以手工转抄 hex 落地;`frontend/vendor/` 必须仍只含 `marked.min.js`(硬规则 6)。故供应链面为零,无需包合法性门与人工 checkpoint |

**诚实结论:本阶段不存在 high 或 critical 级威胁。** 它是单文件 CSS 自定义属性的值层重写,没有网络面、没有输入解析、没有新依赖、没有新文件。唯一真实的可利用点是 T-idi041-03 —— 它不是安全漏洞,而是一条**守卫会静默空转**的完整性缺陷,故列为 mitigate 并交给 Plan 02。
</threat_model>

<verification>
- `python3 scripts/check-02-contrast.py` → `PASS: 0 failures`,43 条配对 + `ORDER 0.363`
- `bash scripts/check-01-token-conformance.sh` / `check-03-hidden-uniqueness.sh` / `check-04-important-count.sh` → 各自 `PASS`
- 围栏结构计数:tier-1 颜色 primitive = 25、`--color-*` = 47、`/* PAIR ` = 43、`/* ORDER ` = 1
- `comm -23 <(var 引用) <(声明)` 输出为空;反向 `comm -23 <(声明) <(var 引用)` 亦为空(无声明未消费的令牌)
- `.venv/bin/python scripts/check-05-ui-uat.py --item smoke,1,6` → 退出码 0
- `node --check frontend/app.js` 与 `.venv/bin/python -m pytest -q`(基线 225 collected / 219 passed / 6 skipped)不变
- `git diff --name-only HEAD -- . ':!.claude/settings.local.json'` 只列出 `frontend/style.css` 与 `scripts/check-05-ui-uat.py`
- `frontend/vendor/` 仍只含 `marked.min.js`
</verification>

<success_criteria>
1. 围栏内颜色值层全部换成 Radix 步,25 个 tier-1 / 47 个 `--color-*`,两条无消费者的 tier-2 名被删除
2. `check-02-contrast.py` 在 43 条重算配对上 `PASS: 0 failures` 并给出 `ORDER 0.363`
3. `--color-text-muted` 的 AA 倒退(3.23:1)在声明处被刻度消解(5.62 on `--color-surface`)
4. `--color-border-strong` 恢复 SC 1.4.11 达标(3.24 / 3.15),S-3 的签核意图以 Radix 步恢复
5. R-1 / R-2 / R-3 三处围栏外声明落地,各带一条真实浏览器的运行时接线断言
6. `--z-badge` 重新有消费者,TOKEN-07 的 `badge < banner` 序断言不再空转
7. `frontend/app.js` / `frontend/index.html` / `frontend/vendor/` 零改动
</success_criteria>

<artifacts_this_phase_produces>
**本阶段新建的符号(供 plan-review-convergence 的 source-grounding 排除漂移误报):**

- **新增 tier-1 令牌名(24 个,全部在 `frontend/style.css` 围栏内)**:`--radix-gray-1`、`--radix-gray-2`、`--radix-gray-3`、`--radix-gray-4`、`--radix-gray-6`、`--radix-gray-7`、`--radix-gray-9`、`--radix-gray-11`、`--radix-gray-12`、`--radix-blue-2`、`--radix-blue-11`、`--radix-green-3`、`--radix-green-11`、`--radix-green-12`、`--radix-amber-1`、`--radix-amber-2`、`--radix-amber-3`、`--radix-amber-6`、`--radix-amber-11`、`--radix-amber-12`、`--radix-red-2`、`--radix-red-7`、`--radix-red-11`、`--radix-violet-11`
- **新增 tier-2 令牌(1 个)**:`--shadow-overlay`
- **新增 Python 助手(1 个)**:`scripts/check-05-ui-uat.py` 的 `resolve_token(page, name)`
- **新增清单标记**:43 条 `/* PAIR ... */` + 1 条 `/* ORDER ... */`(整块替换,数量由 34+1 变为 43+1)
- **删除的令牌名**:tier-1 `--black`、`--green-800`、`--gray-900`、`--gray-700`、`--gray-600`、`--gray-500`、`--gray-300`、`--gray-200`、`--gray-100`、`--gray-50`、`--gray-25`、`--green-700`、`--green-100`、`--blue-700`、`--blue-100`、`--blue-50`、`--amber-800`、`--amber-300`、`--amber-100`、`--amber-50`、`--amber-25`、`--red-600`、`--red-200`、`--red-50`、`--purple-600`;tier-2 `--color-text-inverse`、`--color-surface-info-strong`
</artifacts_this_phase_produces>

<output>
Create `.planning/phases/idi-04.1-radix/idi-04.1-01-SUMMARY.md` when done
</output>
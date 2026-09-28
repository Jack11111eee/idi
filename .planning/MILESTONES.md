# Milestones

## v1.15 视觉构图升级 (Shipped: 2026-09-28)

**Phases completed:** 2 phases, 7 plans, 20 tasks

**Key accomplishments:**

- 界面首次拥有 elevation 层次 —— 左栏 4 个 section 与右栏 #doc-panel 由「完全透明 / 比页面更暗的 gray-2」变为同族白卡片(白底 + 1px 既有容器边界 + 10px 既有圆角 + 零位移极轻阴影),并接进一个真实浏览器 computed-style 运行时门(c1/c2),两条中间调 PAIR 的地面重新归属到卡片底色(4.77 / 3.32)。
- 页面底色从 gray-1(#fcfcfc,全场最亮)下沉到 gray-3(#f0f0f0),使「白卡片浮在灰页面之上」在屏幕上真的成立 —— 三档 elevation(gray-3 页面 < gray-2 控件内陷面 < 白卡片)由真实浏览器读数证明严格递增;同时把左栏密度收到用户裁定的紧凑档(间距 12px / 内边距 16px),并把页面换值作废的 6 条对比度配对以 gray-3 逐条重算登记(不是刷新旧值)。
- 本阶段是纯 CSS 的构图改动,本计划用本仓库唯一能证明「渲染语义仍然成立」的机器复核它:五条真实浏览器门 + 四个静态门 + pytest 基线全部复跑,零 FAIL、零处门改动、断言强度零降低;并产出 5 张 1440×900 整窗截图,补上 SC3 一直缺的「屏幕级」半边证据(gray-2 内陷面与白卡片在 5/5 样本里同帧共存)。
- 文档区表格从「每格 1px 全边框的电子表格式网格」改为「gray-2 表头浅底 + 仅横向分隔线」,并新建运行时门 `scripts/check-10-idi10-validation.py`,在真实浏览器里以 computed style 读出 99 条断言、0 FAIL / 0 BLOCKED
- 圆角刻度由 8 / 10 / 28 / 999 收敛为 8 / 10 / 999:删掉从未并入刻度的 `--radius-lg: 28px`,两处消费者按各自真实形态就地改归属(`.chat-user` → 卡片档 10px、`#chat-input-row input` → 胶囊档 999px),并以收敛前后的真实运行时读数(键级 computed style diff + 矩形逐值 + 元素 PNG 逐字节)证明输入框外观零变化
- 本阶段两处纯 CSS 改动(表格重做 + 圆角收敛)在五条真实浏览器门上复跑零 FAIL、与 phase 9 基线逐项结论块逐项同形、门改动实测零处;5 张 1440×900 整窗截图落盘(p3 一张同时可见三个机器可解析表),另出一张 `.chat-user` 10px 圆角的人眼取证图
- 实测落定连带指纹的真实形状是「10 份覆盖 `frontend/style.css`,1 份可执行」—— 9 份归档/quick 报告因 `covered_files` 路径归档后不可解析而 fail-closed stale(与本次改动无关,属 2026-09-14 登记的已知限制),唯一可执行的 `idi-09` 以 HEAD 内容重新验证(非刷新指纹):24 条 must-have 逐条复核 24/24 成立,`covered_digest` 由 `6e811a11…` 重算为 `7b82f8d1…`,`verification.status` 由 `stale` 回到 `passed`

---

## v1.14 前端视觉与可访问性 (Shipped: 2026-09-26)

**Phases completed:** 6 phases, 21 plans, 60 tasks

**Key accomplishments:**

- Fenced `:root` token block with 75 colour tokens, every colour literal in `frontend/style.css` replaced by `var()`, CHECK-01 driven from 117 to 0 bare hex outside the fence, plus three zero-dependency guard commands
- 31 non-colour tokens (spacing / type / weight / line-height / radius / z-index / layout) declared and fully consumed, every matching literal replaced by `var()`, the `#round-doc.round-frozen` opacity deleted in favour of an amber inset structural marker, and the UA control foreground brought inside the token layer
- The fourth contract-check command landed: a zero-dependency WCAG checker that derives its 34 pairs from a manifest co-located with the tokens, machine-checks SC3's hierarchy half as a strict ordering (`ORDER 0.311`), fails loudly on contract drift, and had every one of its failure directions proven by injection — including the inversion that the ratio gates are blind to
- `frontend/style.css` 的颜色值层整体换成 Radix Colors 12 步刻度(tier-1 25 条 / tier-2 47 条),CHECK-02 清单重算为 43 对并实测 `PASS: 0 failures` + `ORDER 0.363`;同时恢复 `#state-badge` 的 `z-index` 与 `.overlay-card` 的 `box-shadow`、删除由算术强制的 `.tier-desc { opacity: 0.9 }`,三处各带一条真实浏览器的运行时接线断言。
- 把 CHECK-01 的 tier-1 隐私不变量从「D-03 改名后会静默空转」修回「真的会失败」—— 交替式加一个 `radix` 分支(一处正则,五行注释),并用八次临时副本上的变异运行证明它,其中「旧交替式对同一泄漏样本打印 PASS」是本次修复的全部理由。
- `scripts/check-05-ui-uat.py` 的全部颜色断言改为令牌接线形式(D-14),`FROZEN_AMBER` 删除、`#doc-pane` → `#doc-panel-body`;全量 harness 由「20 条假 FAIL」变为 0 FAIL(item 1/2/3/4/6 全 PASS 0 BLOCKED,item 5 仅剩两条按设计记 BLOCKED 的交互冒烟,exit=2);`idi-04-UAT.md` 六项全 pass、三条 gap 消解、AA 倒退记为已修复,并补上 C-1 下游门复核与携带项 #8 的留档。
- 把 `check-05-ui-uat.py` 的颜色断言从「令牌改名/删除下恒真」修回「真的会失败」—— `resolve_color` 未声明即返回 `None`、`ok()` 把 `None` 期望值记 BLOCKED(两处 helper),并用一份只删掉 `--color-text-muted` 声明的浏览器侧副本证明:同一条断言修复前记 PASS(渲染已坏)、修复后记 BLOCKED,未变异对照仍记 PASS。
- 字号刻度 5 → 7 档(`--text-2xl` 22px / `--text-3xl` 28px),`.markdown-body` 的 h1/h2/h3 在全部四个宿主上落为 28/22/18px;三条 chrome 标题规则的选择器由 1-0-1 后代形态收窄为子组合器/自有 id,解开压掉文档 h2 的层叠缺陷;五只动作按钮字重 600 → 500,`#btn-authorize` 按 D-12 保持 600;围栏两处注释改写为真,`18/28` 算术错误修正为 `18/24`。
- 不可逆的 G3 授权在**形态**上与五只例行/承诺按钮分离(淡底 vs 实心 vs 实心更深),页面级层级链 28 > 24 > 22 > 14 由运行时断言钉死。
- 侧栏当前活动面板由 3px 蓝竖条 + 标题变色标出(纯 CSS `:not(.hidden)` 推导,`app.js` 零 diff),两处写死的 emoji 换成跟随令牌的 12px 掩码字形(data-URI 内零颜色信息);D-05 的连带义务履行完毕,`idi-04.1-radix` 的三处结论逐条从 HEAD 重算。
- 把标题刻度从 `.markdown-body` 作用域扩展到 `renderMarkdown()` 的全部九个注入目标:五个非 `.markdown-body` 容器里的 h1/h2/h3 从 UA 默认值(32px / 28px、字重 700)改为 24 / 18 / 16px 与 `--fw-semibold`,第四字重档 700 退出应用;门从 36 FAIL 转 0 FAIL,枚举改按调用点并配会失败的普查守卫。
- 文档面板标题行由 `position: sticky; top: 0` 钉在面板顶部(自带 `var(--color-surface)` 背景、零新增令牌),配 check-05 `item8` 的三条 L-1 运行时门(流内 badge / 三宽度几何不相交 / 滚到底后表头仍可见),并把三宽度溢出、L-5 clearance、L-6 命中区三项原始数值落盘为计划 03 的输入契约
- 六目标 `overflow-wrap: anywhere` 把不可断长内容的横向撑破从根上堵死(配 `#main-pane` / `#doc-panel` 两处 `min-width: 0` 兜底),`.event-list` 与 `#annotation-list` 的限高与内滚动原地删除后面板区滚动者收敛为「1 个外层 + 1 个保留的内层 + 1 个明文豁免的会话流」,并由 check-05 `item9` 的 DOM 普查 + 末条可达性 + 两条保留项护栏机械复核
- 窄窗口守卫被实测推翻(三宽度文档级溢出 0px,并另立 `#doc-panel` 实测宽 vs `clamp()` 上界的判别性探针,实测 432/340/340 逐位等于上界),`.annotation-answer summary` 由 722 × 17 抬到 722 × 24(唯一实测不达标的可交互元素,需求点名的裁决按钮本来就达标),L-5 的 clearance 普查最小 40px 故零 padding 改动,并把两条普查写成门后经反向验证证明会失败
- Narrowed LAYOUT-02's 768px promise to "badge not occluded by the banner", made check-05's 768px branch say explicitly that it does NOT cover the occlusion, and registered the deviation as an A-10 entry plus a frontmatter override — with zero layout change.
- `--color-focus: #1f63bd` 从零建成可断言:围栏内一条令牌 + 文件末尾一条七选择器 `:focus-visible` 规则 + `check-02` 的三条配对(5.72 / 5.57 / 3.45)+ `check-05` 新增 item 10 的**元素普查**(三个样本的判定集,未被环覆盖数均为 0)与 SC1 / SC2 / SC4 三条运行时探针,外加一条不进守卫契约的归档合成反事实探针。
- 把「有底色语义的按钮 hover 时零反馈」与「禁用按钮 hover 时变色」两个实测缺陷正面修掉:围栏内四个新 tier-2 令牌(零新增 primitive)、L627 的选择器就地 gate 在 `:not(:disabled)` 上并在按住不放时让位、三组追加规则(朴素 `:active` 停在 0-1-0 / 填充按钮的 0.06→0.12 叠层 / 输入控件的边框加深),外加两条 `--color-border-hover` 配对与 `check-05` 第 10 项的三条交互态运行时探针 —— item 10 由 11 条断言增至 26 条,两条承重断言经变异测试证明会真的失败。
- 把过渡限定在 `background-color` 与 `border-color` 两个属性上(120ms),用 `@media (prefers-reduced-motion: reduce)` 把 `button` / `input` / `select` / `.event-list` 的过渡按选择器重写为 `none` —— 三条产出与 `EXPECTED_MEDIA_QUERIES` 0 → 1 同一次提交;把 D-15 中段的四条契约计数落成 `check-05` 第 10 项里的静态守卫(含必须做块提取的「焦点规则不得设 border / padding」),并为过渡落地后**会读到中间值**的两条既有 hover 探针补上终态读取器;最后完成整阶段收口:六条命令复跑全绿、四份受影响报告的指纹以 HEAD 内容重算并逐份处置、人工项 5″ 与七条登记面落进 SUMMARY 与 VERIFICATION。
- One HTML attribute activates the focus ring Phase 7 pre-wired, and a Shift-release gesture turns keyboard text selection into a working annotation path — with the false-green trap it was designed around documented in the code
- Two blocking modals now announce as modal dialogs and the announcement is made true — native `inert` derived from the modals' own `.hidden` state, plus a single Escape dispatcher that closes them with zero decisions and hands focus back to the trigger
- One word of empty-state copy corrected against the authoritative design doc, all six b9664e0 manual acceptance items re-run with per-step observations, the full Tab-order census recorded in two states — and a phase-introduced Escape defect found by the re-run, isolated with three controls, and registered rather than papered over

**Range:** `52b714b` (2026-09-17 11:07) → `428e96d` (2026-09-26 12:46) — 296 commits, 8 days
**Product surface:** 23 files, +8490 / −401 (`frontend/` + `scripts/`). Frontend at close: `style.css` 1708 / `app.js` 1854 / `index.html` 269 = 3,831 LOC. Backend unchanged by this milestone (219 passed / 6 skipped).
**Closeout type:** `verified_closeout` — 6/6 phases `phase_complete === true` and `verification_status === 'passed'` at `0b6283a`.
**Known verification overrides:** 2 newly acknowledged, 0 carried forward from a prior close (see STATE.md Deferred Items). Both are ledger-lag artifacts rather than verdict overrides: `uat_gaps idi-05/05-UAT.md` (a `status: failed` never written back after plan 04 fixed it) and `quick_tasks 260917-fqh` (its SUMMARY has no `status:` field, so the scanner reads `unknown`).

**Pre-close audit finding — one genuine cross-phase regression, fixed before closing:**

Phase 6's L-4 scroll-container convergence (`6adcaa3`) deleted `max-height: 55vh; overflow-y: auto` from `.event-list` (= `#ai-events`), which made `app.js:253`'s `eventsEl.scrollTop = eventsEl.scrollHeight` a **no-op by CSS spec** (a non-scrollable element's `scrollTop` is always 0). AI event auto-follow was silently dead, and nothing replaced it. `check-05 --item 9` did not merely miss it — it *affirmatively asserted the regression's precondition*. Fixed by `item.scrollIntoView({ block: 'nearest' })` on the appended node (no revert of L-4), with a new assertion driven through the app's own `renderEvent` path and proven non-vacuous by mutation. `check-07` also gained a static gate that pins `FOCUSABLE_SELECTOR` to `style.css`'s `:focus-visible` enumeration.

**Deferred to the next milestone:**

- **Nyquist gaps** — `idi-04` and `idi-06` have no `VALIDATION.md`. Registered, not closed. Recommend `/gsd-validate-phase 4` and `/gsd-validate-phase 6`.
- **Four gate labels are wider than what they measure** (audit §7). None changes a passed verdict, but each is a "green gate that isn't looking" — the defect class this milestone hit hardest: `04-UI-SPEC.md` L-5 says "every" while measuring 9 of 10 lines; L-6 measures only visible rows; `check-05 --item 10`'s SC4 uses a fixed 12-Tab window; `check-07` g1's wording does not match what it measures.
- **`check-05 --item 10`'s own docstring is stale** — it claims p3's judged set necessarily contains `summary`, but the measured p3 census at HEAD is 29 elements / **10 judged** and `summary` is not among them (the annotation that would produce it is rendered by item 9, not item 10). Backlog `999.2` item 2 depends on exactly this gap, and its premise is therefore **verified accurate at HEAD**.
- **`idi-07` human item 5″** cites an unreachable sample: `#btn-authorize` is enabled in p3, and `#authorize-row` is `.hidden` in the four samples where it is disabled — so the disabled button is never visible in any shipped fixture, and the recorded UAT `pass` is not evidence for the perception claim as worded. The verifier rewrote the Test to a reachable scenario; **nobody has re-run it**. Accepted as-is at close (user adjudication 2026-09-26).
- **`WINDOWS.md` append rejected** — the append was refused over a pre-existing ledger inconsistency (row id 17). Recorded as a known limitation, not fixed.
- **Backlog `999.1` is closed** (quick `260925-iin` handled both of its items); `999.2` remains open.

---

## v1.13 交互式讨论迭代系统 MVP (Shipped: 2026-09-13)

**Phases completed:** 3 phases, 13 plans, 28 tasks

**Key accomplishments:**

- FastAPI + 原生前端单页 + AICaller 双轨(SDK 首选/子进程兜底,事件枚举同构)+ §5.4 权限矩阵 + SSE 事件直播 + 中止——`bash run.sh` 一键可用的端到端骨架
- derive_state() 按 §7.4 八行表自上而下首条命中实现"文件即状态"脊柱(含完整轮判据、半成品轮视为不存在、tmp 残留免疫),transcript.md 按 §6.1 `[user]`/`[ai]` 起始行文法实现 parse/append 幂等读写——两纯后端模块零框架依赖,28 用例全绿
- 会话流水线(enter→send_message→[ai] 落盘)+ AI-04 权限弹窗闭环(SDK can_use_tool 与 CLI 控制协议双路线,setting_sources 屏蔽全局 allow 绕过)+ 前端阶段 1-2 视图与重启恢复——真实 claude 链路端到端走通
- 发散模式(无想法冷启动,brainstorm.md 覆盖式落盘、雏形诞生即关闭)+ G1 后端定稿(draft.md→discuss-round-1.md + `> 申请授权:否` 末行标记,direct-through 交互)——Phase 1 十个 REQ 全收口
- annotations.json 读写纯模块(§6.2 八字段/aN-NN id/空形态/回写只认 id)与六条 §6.4 机器文法解析器(维度表/未决清单/授权标记/回应表/PASS 锚点取末一处/裁决同号配对),54 个正反例用例 + 回写闭环全绿,基线 66→120 不降
- G2 全流水线(process_round 入口三查+单飞+SSE 直播+done 后回应表解析回写上一轮 annotations)与大白话 ask_lite 双路线同步调用、五条轮次路由(202/409/404/400/502)落下,23 新用例 + uvicorn 冒烟全绿,基线 120→143 不降
- 轮次视图(切换器+文档渲染+批注流侧栏+未处理数)替换 rounds-placeholder,划词弹原生菜单两项落盘(方向无关 before)、highlightAnnotations 包 mark、处理本轮批注按钮挂 done 后拉新链(新轮+上轮冻结灰化)——纯原生 JS 零新依赖,三条 uvicorn 冒烟对账全绿
- 真 CLI 全链 E2E(SDK 路线)证明 answer_plain 秒级回 + process_round 产文法合规新轮 + 回写 + 推导态前进;发现的 AI 越界读缺陷以 prompts 资料完备性段修复;真机观测驱动的挂退避重试测试基建;Phase 2 六 REQ 以 7 判据对账表收口
- G3 四查组合判定 + AUTHORIZATION.md 后端写入、tier 档位签名与报告尾部追加族(待裁决/裁决/PASS)、grammar 四新解析器(tier 行/问题分级表/纯 P2/待裁决扫描)——Phase 3 全部上层的纯函数 import 基座,143→176 passed 零失败
- G3 授权入口(四查服务端再查→AUTHORIZATION.md)与撰写 tmp 原子改名流水线、检查者/修复者两角色 prompt 族、严格档两跳自动循环引擎(done-回调直排 + 抛问截存暂停 + 半份不跳号)、选档/裁决同步落盘与残余收口、快照 selfcheck 子状态 + 5 条新路由(authorize/tier/verdict 三 POST + design/checks 两 GET)——176→209 passed 零失败
- D-P3-27 八条路由族收口:POST /api/writing、/api/checks/start、/api/checks/repair 三条 202 受理路由照 /api/rounds/process 模子接线(路由层零判定透传 session)+ 7 条 route 级全分支用例——209→216 passed 零失败,prompts.py 零改动确认

---

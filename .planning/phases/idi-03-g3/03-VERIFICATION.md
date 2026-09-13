---
phase: idi-03-g3
verified: 2026-09-13T23:40:00Z(初验 13:10:00Z;复审 23:40:00Z——缺口修复 503f374 后 staleness 复验,指纹刷新至现行树)
status: passed
score: 5/5 ROADMAP 判据代码级达成;4/4 缺口已关闭(初验 2 运行时缺陷 + 2 呈现层残留,修复于 503f374)
re_verification:
  previous_status: gaps_found
  previous_score: "5/5 ROADMAP 判据代码级达成;2 项运行时缺陷(见 gaps)"
  gaps_closed:
    - "G-idi03-1(high,无界自链)— 修复于 503f374:start_repair 的 finally 守卫由「tmp 是否仍在」改为本跳局部 tmp_consumed 标志(仅在 tmp_path.replace(design_path) 真跑过时置 True),守卫 = `if _aborted or tier == '宽松' or not tmp_consumed: return`。本验证者独立探针复验:同一形态(严格档 + 修复跳不写 tmp)修复前 20 秒内 10209 跳且仍在飞 → 修复后 20 秒窗口内恰好 2 跳(C/R)、busy=False。RED 用例 test_repair_no_tmp_stops_chain 通过;命名 flake test_next_check_n_half_report_no_skip 连跑 10/10 全绿(修复前约 10-25% 失败)。"
    - "G-idi03-2(medium,锚位分歧)— 修复于 503f374:新增 session 层 _unpaired_pending_questions,按 unpaired_verdicts 的未配对编号从 scan_pending_questions 全扫结果取文本,判定式与呈现层共用同一配对空间。本验证者独立探针复验三形态:锚前 unpaired=[]/scan=[1] → mode=running questions=[](不再端出文法不认的问题);混合(锚前 #7 + 锚后 #1)→ unpaired=[1] → mode=paused questions=[#1](修复前会端出 #7);锚后 → mode=paused questions=[#1]。grammar.py 锁定语义零触碰(与 9c824bc 同 blob)。"
    - "G-idi03-3(low,归档态按钮残留)— 修复于 503f374:loadArchiveView 在 loadChecksView(null) 之后复位两个推进按钮。本验证者 CDP 复验:归档态 continue-check/continue-repair 均 hidden=True,checks-panel 内可见按钮数 = **0**(修复前为 ['继续自检']),报告仍可浏览(D-P3-25 不回归),服务端 POST /api/checks/start → 409 不变。"
    - "G-idi03-4(low,跨阶段面板残留)— 修复于 503f374:applyPhase3Extras 补 checksPanel.classList.add('hidden')。本验证者 CDP 复验:同页 phase5(checks-panel hidden=False)→ phase3(checks-panel hidden=**True**,continue-check hidden=True),且 authorize-row 可见 + 四查全过按钮点亮(无回归)。"
  gaps_remaining: []
  regressions: []
  post_gap_fix_passes:
    - "复审(503f374 + 49b5eb7,本次 staleness 复验):diff 审读(仅 3 文件:backend/session.py +35/-5、backend/tests/test_session.py +117、frontend/app.js +5;grammar.py / state.py / checks.py / g3.py / main.py / prompts.py 零改动,无新文件,无新 derive_state 值,无归档标志文件)→ 四缺口逐条独立复验(见 gaps_closed,均用本验证者自己的探针而非新测试)→ 全量 219 passed + 6 skipped(5.82s,较修复前 12.27s 显著下降,与无界自链消失一致)→ 命名 flake 10/10 → 真 CLI E2E 2 passed(170.28s)→ 浏览器 CDP 复验 CP7/CP8 两缺口。结果:gaps_found → passed。"
    - "复审中真 CLI E2E 共 2 次运行:运行 #5 `1 failed, 1 passed`(176.45s,`核查调用 120s 内零事件` — WINDOWS.md #8 记录的 CLI 枯竭窗,环境性,与产品缺陷无关);运行 #6 **`2 passed`(170.28s)**——即初验运行 #1 失败的那条断言区(test_selfcheck_real_cli_loose)本次通过。"
covered_files:
  - .planning/phases/idi-03-g3/03-CONTEXT.md
  - .planning/phases/idi-03-g3/03-DISCUSSION-LOG.md
  - .planning/phases/idi-03-g3/idi-03-01-PLAN.md
  - .planning/phases/idi-03-g3/idi-03-01-SUMMARY.md
  - .planning/phases/idi-03-g3/idi-03-02-PLAN.md
  - .planning/phases/idi-03-g3/idi-03-02-SUMMARY.md
  - .planning/phases/idi-03-g3/idi-03-03-PLAN.md
  - .planning/phases/idi-03-g3/idi-03-03-SUMMARY.md
  - .planning/phases/idi-03-g3/idi-03-04-PLAN.md
  - .planning/phases/idi-03-g3/idi-03-04-SUMMARY.md
  - .planning/phases/idi-03-g3/idi-03-05-PLAN.md
  - .planning/phases/idi-03-g3/idi-03-05-SUMMARY.md
  - .planning/phases/idi-03-g3/idi-03-PATTERNS.md
  - backend/ai_caller.py
  - backend/checks.py
  - backend/g3.py
  - backend/grammar.py
  - backend/main.py
  - backend/prompts.py
  - backend/session.py
  - backend/tests/test_ai_caller.py
  - backend/tests/test_checks.py
  - backend/tests/test_e2e_g3.py
  - backend/tests/test_g3.py
  - backend/tests/test_grammar.py
  - backend/tests/test_route_session.py
  - backend/tests/test_session.py
  - frontend/app.js
  - frontend/index.html
  - frontend/style.css
  - pytest.ini
covered_digest: "v1:sha256:12555c9b1fd05f02abdd63d88a73c0c8763e6ce3bfb8e82351ac2c46c2513ecb"
behavior_unverified: 0
overrides_applied: 0
gaps:
  - gap_id: G-idi03-1
    severity: high
    kind: defect
    title: "严格档两跳自动链在「修复跳未产出 tmp」时无界自链(违反 D-P3-16 与 start_repair docstring)"
    file: backend/session.py
    lines: "1335-1354"
    status: resolved
    resolved_by: 503f374
    resolved_at: 2026-09-13
  - gap_id: G-idi03-2
    severity: medium
    kind: defect
    title: "待裁决行落在核查结论锚之前时,scan_pending_questions(无锚)与 unpaired_verdicts(锚后限定)判定分歧 → 呈现 running 态而问题已抛"
    file: backend/session.py
    lines: "192-256"
    status: resolved
    resolved_by: 503f374
    resolved_at: 2026-09-13
  - gap_id: G-idi03-3
    severity: low
    kind: defect
    title: "归档态「继续自检」按钮仍可见可点(服务端 409 兜住,属呈现层残留)"
    file: frontend/app.js
    lines: "795-800"
    status: resolved
    resolved_by: 503f374
    resolved_at: 2026-09-13
  - gap_id: G-idi03-4
    severity: low
    kind: defect
    title: "跨阶段重进同一会话时 checks-panel 面板残留(phase5 → phase3 切换后自检报告侧栏不消失)"
    file: frontend/app.js
    lines: "295-305"
    status: resolved
    resolved_by: 503f374
    resolved_at: 2026-09-13
human_verification:  # 已由自动化浏览器 UAT(03-UAT.md)全部收口:8 检查点 8 pass / 0 issue(初验 5 pass/3 issue,缺口修复后重验转 8 pass)
  - truth: "真实浏览器中 G3 四查门控、确认词交互、拒绝转批注的完整交互面(ROADMAP 判据 1 浏览器半边)"
    uat_result: "pass(03-UAT.md 检查点 1/2/3:四反例按钮全灰 + 全过点亮;确认词 strip 全等才放行;拒绝落 type=comment pending 批注)"
  - truth: "撰写 tmp 原子改名 + 崩溃恢复按钮文案(ROADMAP 判据 2 浏览器半边)"
    uat_result: "pass(03-UAT.md 检查点 4/8:真 AI 产出 8084 字节 DESIGN.md,tmp 被消费;残留 tmp 盘重开呈「继续撰写(检测到上次中断的半成品,重写覆盖)」)"
  - truth: "档位模态与档位落盘恢复(ROADMAP 判据 3 浏览器半边)"
    uat_result: "pass(03-UAT.md 检查点 5:模态两选项;点「宽松」落 docs/DESIGN-check-tier.md)"
  - truth: "四 mode 裁决控件(paused/p2/resumed/running)+ 逐条裁决落盘收口(ROADMAP 判据 4 浏览器半边)"
    uat_result: "pass(03-UAT.md 检查点 6:裁决卡「修/接受现状」、纯 P2 三字段卡、resumed「继续修复」;全裁决后落 PASS 收口)"
  - truth: "使命完成欢呼模态 + 只读归档可浏览不可改(ROADMAP 判据 5 浏览器半边)"
    uat_result: "pass(03-UAT.md 检查点 7:模态一次性;三源可浏览;annotations/tier 409、design GET-only、划词菜单不弹)"
---

# Phase 3: 授权、自检与终点——G3、档位、使命完成归档 验证报告

**验证者立场**:本报告按 goal-backward 方法执行——先假设目标未达成,再逐条找证据推翻该假设。凡未能找到可复现证据的判据,一律不勾通过。

**验证时间**:2026-09-13(代码级全量 + 真 CLI E2E + 浏览器 UAT 三线并行;初验 13:10 CST,缺口修复后复审 23:40 CST)
**HEAD**:a82a6c9(phase 3 全部 5 plan + 缺口修复 503f374 已合并 main;初验时为 bdb7672)

**Re-verification: Yes** — after gap closure(初验 4 缺口,修复于 503f374,复审确认全部关闭,详见 Gap Remediation 与 frontmatter `re_verification`)

---

## Goal Achievement

### Observable Truths(ROADMAP 5 条成功判据)

| # | 判据 | 状态 | 证据 |
|---|---|---|---|
| 1 | 「授权撰写总设计文档」按钮仅当四处机械校验全过才点亮;点击后须输入「确认授权」才通过;默认拒绝,拒绝记为一条普通批注进入下一轮 | ✅ 代码级达成 | `backend/g3.py:g3_available` 四查组合(单快照复用,不跨轮);`authorize_write` 写 `AUTHORIZATION.md` 含 ISO-8601 时间 + 确认词标记行,已存在 → `FileExistsError`(幂等)。测试 `test_g3.py` 8 passed(四条各一「AI 产物污染」反例);`test_session.py::test_authorize_accepts_and_persists` / `test_authorize_rejects_on_four_checks`;`test_ai_caller.py::test_write_authorization_md_rejected`(AI 无任何批准路径)。浏览器面见 03-UAT.md CP1/CP2/CP3。 |
| 2 | 授权后 AI 写 `DESIGN.md.tmp`,后端原子改名;中途崩溃重开出现「继续撰写」/「继续自检」,点一下重跑覆盖,无需重新确认词 | ✅ 代码级达成 | `session.start_writing` done-else 分支 `tmp_path.replace(design_path)`(`Path.replace` 同 inode 原子);`writing_tmp_exists` 纯磁盘判定驱动前端二态文案;`_next_check_n` 半份报告同轮覆盖不跳号。测试 `test_start_writing_closes_loop` / `test_start_writing_error_when_no_tmp` / `test_next_check_n_half_report_no_skip`。真 CLI 实测产出 8084 字节 DESIGN.md、tmp 被消费(UAT CP4c)。 |
| 3 | DESIGN.md 初稿写完弹宽松/严格档位选择,结果记在每份核查报告头部,重开据此恢复 | ✅ 代码级达成 | `checks.write_tier` / `read_tier` 落盘 `docs/DESIGN-check-tier.md`(白名单外 → `ValueError`,脏/缺 → None);`build_check_prompt` 注入 `TIER_LINE_STRICT` / `TIER_LINE_LOOSE` 常量(非手搓字符串);`_selfcheck_substate` 先读报告头部行、回落签名文件。测试 `test_build_check_prompt_injects_tier_line` 等 4 passed;`test_checks.py` 11 passed。UAT CP5 实测落盘。 |
| 4 | 宽松档一检一修一 PASS 即止;严格档两角色自动循环至零问题轮 PASS;纯 P2 轮进残余裁决制,抛问截存暂停,裁决落盘后续跑「继续修复」,全部处理完收口 | ✅ 代码级达成(缺口已关闭) | 宽松档:`test_start_check_pass_stops`。严格档两跳链:`test_start_check_two_hop_chain`(check-1 P1 → repair → check-2 纯 P2 停)。抛问截存:`test_start_check_pending_question_intercepts` / `test_resume_after_verdict`。判定式①②③:`test_repair_available_three_states`。**初验发现的 G-idi03-1(修复跳未产出 tmp 时无界自链)与 G-idi03-2(锚位分歧)均修复于 503f374,本验证者独立探针复验关闭**(见 Gap Remediation)。 |
| 5 | 最新 check 报告末行以 `> 核查结论:PASS` 开头时弹「使命完成」;此后只读归档态,轮次/批注/DESIGN.md/报告全可浏览,划词批注/「处理本轮批注」/授权按钮均不可用 | ✅ 代码级达成 | `state.py:139` 行 7 末行 `PASS_PREFIX` → `mission_complete`;`applyArchiveView` 三源浏览 + 三交互面隐藏;服务端 409 真防线实测(UAT CP7:`/api/rounds/1/annotations` 409、`/api/checks/tier` 409、`/api/writing` 409、`/api/authorize` 409、`/api/checks/start` 409)。 |

### User Flow Coverage(goal 全句逐步)

「授权 → 撰写 → 选档 → 自检 → 残余裁决 → 使命完成 → 只读归档」七步全链:

1. **授权**:`derive_state==phase3` + `g3_available` 后端再查 → `authorize_write` → `phase4` ✅
2. **撰写**:`start_writing` 三查 → 真 AI 写 tmp → 后端原子改名 → `phase5_awaiting_tier` ✅(真 CLI 实测)
3. **选档**:`set_tier` 白名单 → 落盘签名 → 呈现「开始自检」✅
4. **自检**:`start_check` → 真 AI 产报告 → 宽松档修复者追加 PASS ✅(真 CLI 实测 2 passed/289.65s)
5. **残余裁决**:抛问截存 → paused 卡 → 逐条裁决 → resumed → 「继续修复」✅(UAT CP6 实测;但见 G-idi03-2 的锚位分歧)
6. **使命完成**:末行 PASS → 模态 + `mission_complete` ✅
7. **只读归档**:三源可浏览 + 五路 409 ✅

### Required Artifacts(三层:存在/实质/接线)

| 产物 | 存在 | 实质 | 接线 | 证据 |
|---|---|---|---|---|
| `backend/g3.py`(119 行) | ✅ | ✅ 四查组合单快照 + fail-closed OSError | ✅ `/api/authorize` 369 行消费 | `test_g3.py` 8 passed |
| `backend/checks.py`(158 行) | ✅ | ✅ tier 读写 + 抛问/裁决/收口三件套(内容级幂等、同号拒绝) | ✅ session 六函数消费 | `test_checks.py` 11 passed |
| `backend/grammar.py`(397 行) | ✅ | ✅ 六条锁定文法零改动 + 四个纯增量解析器 | ✅ g3/checks/session 三处消费 | `test_grammar.py` 全绿 |
| `backend/session.py`(1357 行) | ✅ | ✅ 六函数 + snapshot 三新字段 | ✅ 八路由族消费 | `test_session.py` 全绿(除 flake) |
| `backend/main.py`(643 行) | ✅ | ✅ 八路由族齐(authorize/tier/verdict/design/checks/writing/checks-start/checks-repair) | ✅ 前端全挂接 | `test_route_session.py` 全绿 |
| `backend/prompts.py`(795 行) | ✅ | ✅ 三族四段 prompt + tier_line 注入(f81d24c) | ✅ session 三 start 消费 | 4 passed(tier_line) |
| `frontend/app.js`(1590 行) | ✅ | ✅ 阶段 3/4/5/归档四视图 + 四 mode 控件 | ✅ applySessionGates else 分支 | 浏览器 UAT CP1-CP8 |

**Anti-pattern 扫描**:9 个 Phase 3 产品文件(TODO/FIXME/XXX/TBD/HACK/PLACEHOLDER)零命中。

### Key Link Verification

| 链路 | 验证 |
|---|---|
| `session.start_writing` done-else → `Path.replace` 原子改名 | ✅ 代码 + 真 CLI 实测(tmp 消失、DESIGN.md 落盘) |
| `session.start_check` done-else → `_drive_next` 串调 `start_repair` | ⚠️ 正常路径 ✅(`test_start_check_two_hop_chain`);**tmp 缺失路径 ❌ 无界自链**(G-idi03-1) |
| `session.verdict_append` → `append_pass_conclusion` 收口 | ✅ `test_verdict_append_persists_and_closes`;UAT CP6a/CP6b 实测末行落 PASS |
| `main.py` 八路由 → session 六函数 | ✅ `test_route_session.py` 全分支 |
| `frontend/app.js` applySessionGates → 四视图 | ✅ UAT CP1-CP8 逐态实测 |

### Data-Flow Trace(Level 4)

磁盘 → 解析器 → snapshot → 路由 → 前端 的完整链在本 Phase 全部落在「文件即状态」上,无独立流程状态:

- `derive_state`(§7.4 八行表)读 `docs/` 现状推导,八行条件互斥化覆盖全形态 ✅
- `_selfcheck_substate` 只认磁盘不缓存 ✅
- `writing_tmp_exists` / `g3_available` 均为纯磁盘判定 ✅
- 前端按钮文案纯消费 snapshot 字段,不自行推演 ✅(UAT CP8 五个中途态逐一核对)

### Behavioral Spot-Checks(本验证者本次实跑)

**初验(HEAD bdb7672)**:

| 命令 | 结果 |
|---|---|
| `.venv/bin/python -m pytest backend/tests/ -q` | **217 passed, 6 skipped**(10.34s) |
| `IDI_E2E=1 .venv/bin/python -m pytest backend/tests/test_e2e_g3.py -q -m slow` | **2 passed in 289.65s**(真 claude CLI) |
| `pytest backend/tests/test_g3.py -q` | 8 passed |
| `pytest backend/tests/test_checks.py -q` | 11 passed |
| `pytest backend/tests/test_ai_caller.py -q` | 17 passed |
| `pytest backend/tests/ -q -k tier_line` | 4 passed |
| `defect_confirm.py`(两跳链无界性有界观察) | 20s 内 **10209 跳**、仍在飞 → 缺陷确证 |
| `defect2_confirm.py`(锚位分歧) | 锚前抛问:`scan=[{1,...}]` 而 `unpaired=[]` → 分歧确证 |

**复审(HEAD a82a6c9,缺口修复后)**:

| 命令 | 结果 |
|---|---|
| `.venv/bin/python -m pytest backend/tests/ -q` | **219 passed, 6 skipped**(5.82s;+2 新用例、零回归,耗时较初验 12.27s 显著下降) |
| `IDI_E2E=1 .venv/bin/python -m pytest backend/tests/test_e2e_g3.py -q -m slow` | **2 passed in 170.28s**(真 claude CLI) |
| `pytest ...::test_next_check_n_half_report_no_skip ...::test_repair_no_tmp_stops_chain` ×10 | **10 passed / 0 failed**(确定性) |
| `reverify_probe.py`(G-idi03-1 无界性,本验证者独立探针) | 20s 窗口内 **2 跳**(C/R)、busy=False(修复前 10209 跳) |
| `reverify_probe.py`(G-idi03-2 锚位三形态,独立探针) | 锚前 running/[] · 混合 paused/[#1] · 锚后 paused/[#1] |
| CDP 复验 CP7(归档态推进按钮) | checks-panel 可见按钮 **0** 个(修复前 `['继续自检']`);报告仍可浏览;start → 409 |
| CDP 复验 CP8(phase5 → phase3) | checks-panel hidden=**True**;authorize-row 可见 + 按钮点亮(无回归) |
| `git diff 9c824bc..HEAD --stat -- backend/{grammar,state,checks,g3,main,prompts}.py` | **空** — 锁定模块零改动 |

**真 CLI E2E 六次运行记录(诚实全记,不挑选)**:

| 运行 | 阶段 | 结果 | 现象 |
|---|---|---|---|
| #1 | 初验 | 1 failed, 1 passed(211.71s) | `test_selfcheck_real_cli_loose`:`裁决落盘后应为 resumed 态或已收口,实际:running` → 对应 G-idi03-2 |
| #2 | 初验 | failed | `修复调用 120s 内零事件` — CLI 枯竭窗(环境性,非产品缺陷) |
| #3 | 初验 | 1 failed, 1 passed(73.86s) | `DESIGN-check-1.md 未产出`,AI 的 Write 被权限门驳回 → AI 行为波动(权限门行为正确) |
| #4 | 初验 | **2 passed(289.65s)** | 全链通过(宽松档一检一修一 PASS 收口) |
| #5 | 复审 | 1 failed, 1 passed(176.45s) | `核查调用 120s 内零事件` — 同一 CLI 枯竭窗(环境性) |
| #6 | 复审 | **2 passed(170.28s)** | **初验 #1 失败的那条断言区本次通过**;产物完整链:check-1 抛 3 条锚后 `> 待裁决:` → 3 条 `> 裁决:#N:修` → `> 核查结论:PASS(残余裁决收口)` → `derive_state=mission_complete` |

六次运行合起来:三次完整通过,三次失败三种不同成因——其中仅 #1 是可复现的产品缺陷(已修复),另两次为 CLI 环境枯竭窗、一次为 AI 行为波动。复审的 #6 通过即初验 #1 断言区的正面反证。

**复审对 #6 真产物的独立推导复验**(直接对 basetemp 落盘报告跑解析器):末锚行 `> 核查结论:PASS(残余裁决收口)`;`unpaired_verdicts=[]`、`parse_verdict_lines=[]`、`scan_pending_questions` 编号 `[1,2,3]`、`is_pass_conclusion=True`、`derive_state=mission_complete`、`tier=宽松`。注意此形态正是 G-idi03-2 的关键切面:三条待裁决行**全部在锚之前**、裁决行在锚之后 —— 若沿用修复前的无锚扫描,`questions` 会端出 3 条而判定式不计;修复后 `unpaired=[]` 与 `questions=[]` 一致,PASS 收口正确判定。

### Requirements Coverage(4/4)

| REQ | 状态 | 证据 |
|---|---|---|
| FLOW-05(G3 授权门控 + 确认词 + 拒绝转批注) | ✅ | `g3_available` 四查 + `authorize_write` + `/api/authorize` 三态;UAT CP1/CP2/CP3 |
| DATA-02(撰写 tmp 原子改名 + 崩溃恢复) | ✅ | `Path.replace` + `writing_tmp_exists` 二态;真 CLI 实测 + UAT CP4/CP8 |
| DATA-03(使命完成 + 只读归档) | ✅ | `state.py` 行 7 + `applyArchiveView` + 五路 409;UAT CP7 |
| DATA-04(档位 + 两角色循环 + 残余裁决) | ✅ | 档位签名落盘/读回 + 两跳自动链 + 抛问截存 + 残余裁决收口;初验缺陷 G-idi03-1/G-idi03-2 修复于 503f374 并复验关闭 |

### Test Quality Audit

- 新增用例均为**先红后绿**(`test(idi-03-01): ... 先红` 等提交可查),非事后补测 ✅
- 四查反例为「AI 产物污染」形态(非空值),针对性强 ✅
- 边界覆盖:半份报告重跑不跳号、同号裁决拒绝、抛问内容级幂等、三态 repair_available ✅
- **初验发现的覆盖缺口已随缺陷修复关闭**:`test_next_check_n_half_report_no_skip` 的修复跳恰好「不写 tmp、不发事件即 done」,正是触发 G-idi03-1 无界自链的形态,用例靠 `busy()` 在两跳间的瞬时翻转窗口偶然通过(初验实测约 10-25% 失败)。503f374 新增 RED 用例 `test_repair_no_tmp_stops_chain` 正面覆盖该形态(断言恰好 1 次修复、1 次核查、无 check-2、发「修复未产出 tmp,可重跑」error、链停不 busy),同时消除原 flake——复审连跑 **10/10 全绿**。

### Decision Coverage(非阻塞门)

`node .claude/gsd-core/bin/gsd-tools.cjs check.decision-coverage-verify .planning/phases/idi-03-g3 .planning/phases/idi-03-g3/03-CONTEXT.md`:

```json
{ "skipped": false, "blocking": false, "total": 30, "honored": 30,
  "not_honored": [], "message": "All trackable CONTEXT.md decisions are honored by shipped artifacts." }
```

30/30 全部 honored。⚠️ **方法论边界(初验发现,修复后仍成立)**:决策覆盖门只扫 PLAN/SUMMARY 文本中的决策编号出现,不校验运行时行为——初验时 G-idi03-1 正是 D-P3-16(「无常驻 scheduler,每跳结束重拉磁盘判定下一步」)的实现偏差,而该门当时即报 30/30 通过。此项说明:决策覆盖通过 ≠ 决策语义在运行时成立。

### Anti-Patterns Found

零 TODO/FIXME/XXX/TBD/HACK/PLACEHOLDER(9 个产品文件)。

### Human Verification Required

无(本 Phase 的浏览器面已由自动化浏览器 UAT 全部收口,见 03-UAT.md;`behavior_unverified: 0`)。

---

## Gaps Summary

**4 项缺口(1 high / 1 medium / 2 low),初验时全部未修复**(按 orchestrator 指令:issues > 0 时记录不修);**复审时全部已关闭**(修复于 503f374,本验证者独立复验,详见下方各条 `状态` 与 `复审结论`)。

---

## Gap Remediation(复审新增)

**修复提交**:503f374 `fix(idi-03): 收口 Phase 3 四处 UAT 缺口(G-idi03-1~4)`,经 49b5eb7(UAT 对账)合并入 main(a82a6c9)。

**修复范围审读(本验证者 `git show 503f374` 实读,非采信摘要)**:

| 文件 | 变更量 | 内容 |
|---|---|---|
| `backend/session.py` | +35 / −5 | `_unpaired_pending_questions` 新增;`_selfcheck_substate` paused 分支改用它;`start_repair._worker` 新增 `tmp_consumed` 局部标志 + finally 守卫替换 |
| `backend/tests/test_session.py` | +117 | 两个 RED 用例:`test_repair_no_tmp_stops_chain`、`test_selfcheck_paused_questions_anchor_consistent` |
| `frontend/app.js` | +5 | `applyPhase3Extras` 补 `checksPanel` hidden;`loadArchiveView` 尾部复位两推进按钮 |

**外科性核验(全部通过)**:

- `git diff 9c824bc..HEAD --stat -- backend/{grammar,state,checks,g3,main,prompts}.py` → **空**。§6.4 锁定文法(`grammar.py`,check-14 锁定版)零触碰;`derive_state` 状态值集合零新增;无归档标志文件新增。
- `git show 503f374 --diff-filter=A --name-only` → 空,无新文件、无新依赖、无新测试基建(D-P3-30)。
- 无「为过 E2E 而改锁定语义」的痕迹:两处后端改动均只改 session 层**消费者**,不改解析器或回写逻辑(D-P3-20..22 边界内)。

### G-idi03-1(high,缺陷):严格档两跳自动链在「修复跳未产出 tmp」时无界自链 — **status: resolved(503f374)**

**位置(初验)**:`backend/session.py:1335-1354`(`start_repair._worker` 的 `finally` 尾部驱动判定)

**初验问题**:`finally` 尾部的断链判定为:

```python
if _aborted or tier == "宽松":
    return
...
if not latest or grammar_mod.unpaired_verdicts(latest):
    return  # 抛问截存盘:不再自动推进
if tmp_path.is_file():
    return  # tmp 未消费(异常形态,不推进;重跑覆盖)
_drive_next(project, "check")
```

`if tmp_path.is_file(): return` 的语义是「tmp **还在** → 未消费 → 不推进」。而该函数自己的 docstring 承诺的形态是「tmp **缺失**(AI 没写)→ error 事件『修复未产出 tmp,可重跑』,**不驱动下一跳**」——tmp 缺失时 `tmp_path.is_file()` 为 False,该守卫不命中,执行直落 `_drive_next(project, "check")`,于是 check 产 FIX 报告 → repair 又不写 tmp → 再 check……**无界自链**。

**初验实测确证**(`/tmp/defect_confirm.py`,严格档 + 修复跳「不写 tmp、不发事件即 done」):
```
20s 内跳数=10209  模式(前40)=CRCRCRCRCRCRCRCRCRCRCRCRCRCRCRCRCRCRCRCR
20s 后仍在飞(busy)=True  ← True 表示链未自停(无限自链)
```

**初验影响**:
1. **违反 D-P3-16**(每跳结束重拉磁盘判定下一步)与 §7.3「不留损坏状态」——链路不收敛,后台线程持续空转。
2. **回归套件间歇性失败**:`test_session.py::test_next_check_n_half_report_no_skip` 的修复跳正是该形态,靠 `_wait_chain_idle` 的 `busy()` 瞬时翻转窗口偶然通过。本验证者首次全量跑得 **1 failed, 216 passed, 6 skipped**;随后 11 次重跑全绿,判定为约 **10-25% 的 flake**。这不是「偶发测试问题」,而是产品缺陷在测试面的显影。
3. **真 CLI 场景下会烧 token**:AI 若连续两次不写 tmp,链路将持续真调用。

**根因**:断链判据用「tmp 文件是否仍在」推断「修复是否产出」,把两种形态混为一谈——(a) 修复成功 → 后端已把 tmp 改名 DESIGN.md → tmp 不在(应链);(b) 修复根本没产出 tmp → tmp 也不在(不应链)。两者在守卫眼里同形,故 (b) 被当成 (a) 放行。

**修复做法(503f374)**:`_worker` 内新增本跳局部变量 `tmp_consumed = False`,**仅在 `tmp_path.replace(design_path)` 真跑过的分支置 True**;finally 守卫改为:

```python
if _aborted or tier == "宽松" or not tmp_consumed:
    return
```

即判据从「tmp 是否仍在」改为「**本跳是否真的改名落成 DESIGN.md**」,与 docstring 承诺一致;原「修复未产出 tmp,可重跑」error 事件仍照发,用户可重跑恢复。原先那条反向守卫 `if tmp_path.is_file(): return` 随之删除(被 `not tmp_consumed` 覆盖)。

**复审结论(本验证者独立探针,非采信新测试)**:同一形态复跑 `/tmp/reverify_probe.py` → 20 秒窗口内跳数 **2**(模式 `CR`)、`busy=False`。修复前 10209 跳 → 修复后 2 跳,链路正常终止(1 次核查 + 1 次修复即断,符合 docstring)。RED 用例 `test_repair_no_tmp_stops_chain` 通过;命名 flake `test_next_check_n_half_report_no_skip` 连跑 **10/10 全绿**;正常改名路径 `test_start_check_two_hop_chain` 仍通过(无回归)。

### G-idi03-2(medium,缺陷):待裁决行锚位分歧导致 paused 态漏判 — **status: resolved(503f374)**

**位置**:`backend/session.py:192-256`(`_selfcheck_substate`)+ `backend/grammar.py`(`scan_pending_questions` 无锚 vs `unpaired_verdicts` 锚后限定)

**问题**:两个扫描器的锚定语义不一致——
- `scan_pending_questions(text)`:**无锚全文扫** `> 待裁决:#K:`(设计如此,供修复者输出扫描复用)
- `unpaired_verdicts(text)`:**只扫最后一处 `> 核查结论:` 锚之后**

`_selfcheck_substate` 用 `unpaired_verdicts` 判 paused。当修复者把 `> 待裁决:` 写在结论行**之前**时:

```
scan_pending_questions (无锚全文扫): [{'number': 1, 'text': '...'}]
unpaired_verdicts      (锚后限定): []
```

→ 判定式①不命中 → 落到 running 分支 → `questions: []`,前端呈「继续自检」而**用户看不到那条已抛出的问题**。

**实测确证**:`/tmp/defect2_confirm.py` 输出如上;**真 CLI E2E 运行 #1 即此形态**:`裁决落盘后应为 resumed 态或已收口,实际:running`。

**影响**:用户可能反复点「继续自检」而 AI 的问题始终不可见,链路无法推进到裁决;属 D-P3-18「先流后文本两处均可复用」的语义边界未对齐。

**根因**:同一份报告上并存两个配对空间——判定式用锚后限定空间(`unpaired_verdicts`),呈现层却用无锚全文空间(`scan_pending_questions`)。§6.4 明文规定配对空间只统计末一处结论行之后,故锚前正文行本就不该计入;而呈现层全扫会把锚前行端成裁决卡——判定式不计、界面端出,两处对同一文本给不同答案。

**修复做法(503f374)**:session 层新增 `_unpaired_pending_questions(md_text)`——先取 `unpaired_verdicts` 的未配对编号(判定式的权威配对空间),再按这些编号从 `scan_pending_questions` 的全扫结果里取文本,按 unpaired 顺序组装 `{number, text}`;`_selfcheck_substate` 的 paused 分支改用它。判定式计入几条,界面就呈现几条。**`grammar.py` 锁定语义零触碰**,只改 session 层消费者(D-P3-20..22 边界内)。

**复审结论(本验证者独立探针,非采信新测试)**:`/tmp/reverify_probe.py` 三形态实测——

| 形态 | `unpaired_verdicts` | `scan_pending_questions` | 修复后 mode / questions | 修复前 |
|---|---|---|---|---|
| 锚前抛问(单行 #1 在锚前) | `[]` | `[1]` | `running` / `[]` | `running` / **`[#1]`**(端出文法不认的问题) |
| 混合(锚前 #7 + 锚后 #1) | `[1]` | `[7, 1]` | `paused` / `[#1]` | `paused` / **`[#7, #1]`**(多一条) |
| 锚后抛问(单行 #1 在锚后) | `[1]` | `[1]` | `paused` / `[#1]` | `paused` / `[#1]`(一致,无变化) |

混合形态是分歧的正面显影:修复后 questions 与 `unpaired_verdicts` 严格同空间。RED 用例 `test_selfcheck_paused_questions_anchor_consistent` 通过(含混合形态断言);真 CLI E2E 运行 #6 的产物(3 条待裁决**全在锚前**、裁决行在锚后)独立推导复验:`unpaired=[]`、`questions=[]`、`is_pass_conclusion=True`、`derive_state=mission_complete`——即修复前会误判为「3 条待裁决未处理」的形态,现已正确收口。

### G-idi03-3(low,缺陷):归档态「继续自检」按钮残留可见

**位置**:`frontend/app.js:795-800`(`applyArchiveView`)

**问题**:`applyArchiveView` 未隐藏 `#btn-continue-check`;`loadArchiveView` → `loadChecksView(null)` 传 `null` 使 `sessionData` 分支跳过,`mode==='running'` 分支(报告为宽松档一检一修即 PASS 的形态)把「继续自检」重新显示。

**实测**:UAT CP7 归档态下 `btn-continue-check` 可见且可点,`visible buttons in checks-panel: ["继续自检"]`。

**缓解**:服务端 409 真防线成立(`POST /api/checks/start` → 409),不可实际推进。属呈现层残留,与 `processRoundBtn.classList.add('hidden')` 同处未覆盖到该按钮。

**复审结论(503f374)**:`loadArchiveView` 在 `await loadChecksView(null)` **之后**补 `continueCheckBtn.classList.add('hidden')` + `continueRepairBtn.classList.add('hidden')`(复位必须放在拉新之后,否则被 `loadChecksView` 的 running 兜底分支覆盖——修复注释已点明)。本验证者 CDP 复验:归档态 `checks-panel` 内可见按钮数 = **0**(修复前 `['继续自检']`);`continue-check`/`continue-repair` 均 hidden=True;报告仍可浏览(`checks-panel` 未隐藏、文本含「核查报告」,D-P3-25 不回归);服务端 `POST /api/checks/start` → 409 不变。

### G-idi03-4(low,缺陷):跨阶段重进时 checks-panel 残留

**位置**:`frontend/app.js:295-305`(`applySessionGates` 的 phase3 分支)

**问题**:phase3 分支只调 `applyPhase3Extras(data)` + `loadRoundsView(...)`,未隐藏 `checksPanel`。`applyPhase3Extras` 本身也不隐藏它(只隐藏 `writingView`)。因此从 phase5 项目切到 phase3 项目时,自检报告侧栏残留。

**实测**(UAT CP8):`fresh→phase3: checks-panel hidden: True`(干净页无残留),但 `phase5 → then→phase3: checks-panel hidden: False`,面板文本仍显示上一个项目的报告与「继续自检」。

**缓解**:服务端 409 兜住(`POST /api/checks/start` → 409),且 `hidePhase3Extras` 在 phase4 路径上正确隐藏(实测 `then→phase4: hidden True`)。属跨阶段切换的呈现层残留。

**复审结论(503f374)**:`applyPhase3Extras` 补一行 `checksPanel.classList.add('hidden')`。本验证者 CDP 复验同页切换:phase5(`checks-panel hidden=False`、「继续自检」可见)→ phase3(**`checks-panel hidden=True`**、`continue-check hidden=True`),且 phase3 自身功能无回归——`authorize-row` 可见、`writing-view` hidden、四查全过盘 `btn-authorize.disabled=False`。

---

## 结论(复审更新)

**Phase 3 的 5 条 ROADMAP 成功判据在代码级全部找到可复现证据**;4 条 REQ 全部达成(初验时 DATA-04 因 G-idi03-1 标为「达成但有缺陷」,缺口修复后转 ✅);真 CLI E2E 三次完整通过(初验两次 + 复审一次,复审那次正覆盖初验失败的断言区);30 项 D-P3 决策经权威门校验 30/30 honored;浏览器 UAT 8 检查点全部 pass(初验 5 pass/3 issue,缺口修复后重验转 8 pass)。

**初验发现的 4 项缺口已全部关闭**(修复于 503f374,本验证者以**自己的独立探针**逐条复验,非采信新测试或修复者摘要):

| 缺口 | 严重度 | 修复前实测 | 复审实测 | 状态 |
|---|---|---|---|---|
| G-idi03-1 | high | 20s 内 **10209 跳**、仍在飞 | 20s 内 **2 跳**、busy=False | resolved |
| G-idi03-2 | medium | 锚前 `scan=[1]` vs `unpaired=[]` 分歧 | 锚前 running/[] · 混合 paused/[#1] · 锚后 paused/[#1] | resolved |
| G-idi03-3 | low | 归档态可见按钮 `['继续自检']` | 可见按钮 **0** 个 | resolved |
| G-idi03-4 | low | phase5→phase3 `checks-panel hidden=False` | `checks-panel hidden=**True**` | resolved |

**修复外科性**:仅 3 文件(backend/session.py +35/−5、backend/tests/test_session.py +117、frontend/app.js +5);§6.4 锁定文法(grammar.py)零改动、`derive_state` 状态值零新增、无归档标志文件、无新依赖/新测试基建。后端两处均只改 session 层消费者,未触碰锁定语义。

**回归面**:全量 **219 passed + 6 skipped**(较初验 +2 新用例、零回归;耗时 12.27s → 5.82s,与无界自链消失一致);命名 flake 10/10 全绿;正常两跳链用例仍通过。

**遗留事项(非本 Phase 缺口,报告备查)**:
- **Phase 2 的 `covered_digest` 已与现行树不符**(`.planning/phases/idi-02-g2/02-VERIFICATION.md` 存 `acd6f0f8…`,按现行文件重算为 `20a4297f…`)。属**既有漂移**,非本次改动引入;按 orchestrator 指示**不修**,由其在 milestone close 时决定处理方式。
- **决策覆盖门的方法论边界**:该门 30/30 通过不蕴含运行时语义成立(初验 G-idi03-1 即反例),已在 Decision Coverage 段落记录。
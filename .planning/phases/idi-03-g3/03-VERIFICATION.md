---
phase: idi-03-g3
verified: 2026-09-13T13:10:00Z
status: gaps_found
score: 5/5 ROADMAP 判据代码级达成;2 项运行时缺陷(见 gaps)
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
covered_digest: "v1:sha256:375c84ad40b2f45150fad16a19fcc0c77e01ce2eeb98e10b6e3e77e88a0f20be"
behavior_unverified: 0
overrides_applied: 0
gaps:
  - gap_id: G-idi03-1
    severity: high
    kind: defect
    title: "严格档两跳自动链在「修复跳未产出 tmp」时无界自链(违反 D-P3-16 与 start_repair docstring)"
    file: backend/session.py
    lines: "1335-1354"
    status: open
  - gap_id: G-idi03-2
    severity: medium
    kind: defect
    title: "待裁决行落在核查结论锚之前时,scan_pending_questions(无锚)与 unpaired_verdicts(锚后限定)判定分歧 → 呈现 running 态而问题已抛"
    file: backend/session.py
    lines: "192-256"
    status: open
  - gap_id: G-idi03-3
    severity: low
    kind: defect
    title: "归档态「继续自检」按钮仍可见可点(服务端 409 兜住,属呈现层残留)"
    file: frontend/app.js
    lines: "795-800"
    status: open
  - gap_id: G-idi03-4
    severity: low
    kind: defect
    title: "跨阶段重进同一会话时 checks-panel 面板残留(phase5 → phase3 切换后自检报告侧栏不消失)"
    file: frontend/app.js
    lines: "295-305"
    status: open
human_verification:  # 已由自动化浏览器 UAT(03-UAT.md)全部收口:8 检查点 6 pass / 3 issue(见 gaps)
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

**验证时间**:2026-09-13(代码级全量 + 真 CLI E2E + 浏览器 UAT 三线并行)
**HEAD**:bdb7672(phase 3 全部 5 plan 已合并 main)

---

## Goal Achievement

### Observable Truths(ROADMAP 5 条成功判据)

| # | 判据 | 状态 | 证据 |
|---|---|---|---|
| 1 | 「授权撰写总设计文档」按钮仅当四处机械校验全过才点亮;点击后须输入「确认授权」才通过;默认拒绝,拒绝记为一条普通批注进入下一轮 | ✅ 代码级达成 | `backend/g3.py:g3_available` 四查组合(单快照复用,不跨轮);`authorize_write` 写 `AUTHORIZATION.md` 含 ISO-8601 时间 + 确认词标记行,已存在 → `FileExistsError`(幂等)。测试 `test_g3.py` 8 passed(四条各一「AI 产物污染」反例);`test_session.py::test_authorize_accepts_and_persists` / `test_authorize_rejects_on_four_checks`;`test_ai_caller.py::test_write_authorization_md_rejected`(AI 无任何批准路径)。浏览器面见 03-UAT.md CP1/CP2/CP3。 |
| 2 | 授权后 AI 写 `DESIGN.md.tmp`,后端原子改名;中途崩溃重开出现「继续撰写」/「继续自检」,点一下重跑覆盖,无需重新确认词 | ✅ 代码级达成 | `session.start_writing` done-else 分支 `tmp_path.replace(design_path)`(`Path.replace` 同 inode 原子);`writing_tmp_exists` 纯磁盘判定驱动前端二态文案;`_next_check_n` 半份报告同轮覆盖不跳号。测试 `test_start_writing_closes_loop` / `test_start_writing_error_when_no_tmp` / `test_next_check_n_half_report_no_skip`。真 CLI 实测产出 8084 字节 DESIGN.md、tmp 被消费(UAT CP4c)。 |
| 3 | DESIGN.md 初稿写完弹宽松/严格档位选择,结果记在每份核查报告头部,重开据此恢复 | ✅ 代码级达成 | `checks.write_tier` / `read_tier` 落盘 `docs/DESIGN-check-tier.md`(白名单外 → `ValueError`,脏/缺 → None);`build_check_prompt` 注入 `TIER_LINE_STRICT` / `TIER_LINE_LOOSE` 常量(非手搓字符串);`_selfcheck_substate` 先读报告头部行、回落签名文件。测试 `test_build_check_prompt_injects_tier_line` 等 4 passed;`test_checks.py` 11 passed。UAT CP5 实测落盘。 |
| 4 | 宽松档一检一修一 PASS 即止;严格档两角色自动循环至零问题轮 PASS;纯 P2 轮进残余裁决制,抛问截存暂停,裁决落盘后续跑「继续修复」,全部处理完收口 | ⚠️ 部分达成(见 G-idi03-1) | 宽松档:`test_start_check_pass_stops`。严格档两跳链:`test_start_check_two_hop_chain`(check-1 P1 → repair → check-2 纯 P2 停)。抛问截存:`test_start_check_pending_question_intercepts` / `test_resume_after_verdict`。判定式①②③:`test_repair_available_three_states`。**但**:修复跳未产出 tmp 时 finally 尾部的驱动判定放行 `_drive_next`,链路无界自链——本验证者实测 20 秒内 10209 跳且仍在飞(见 G-idi03-1)。 |
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

**真 CLI E2E 四次运行记录(诚实全记,不挑选)**:

| 运行 | 结果 | 现象 |
|---|---|---|
| #1 | 1 failed, 1 passed(211.71s) | `test_selfcheck_real_cli_loose`:`裁决落盘后应为 resumed 态或已收口,实际:running` → 对应 G-idi03-2 |
| #2 | failed | `修复调用 120s 内零事件` — CLI 枯竭窗(环境性,非产品缺陷) |
| #3 | 1 failed, 1 passed(73.86s) | `DESIGN-check-1.md 未产出`,AI 的 Write 被权限门驳回 → AI 行为波动(权限门行为正确) |
| #4 | **2 passed(289.65s)** | 全链通过(宽松档一检一修一 PASS 收口) |

四次运行合起来:两次完整通过(含本验证者本次),失败三次三种不同成因——其中 #1 是可复现的产品缺陷,另两次为环境/AI 行为波动。

### Requirements Coverage(4/4)

| REQ | 状态 | 证据 |
|---|---|---|
| FLOW-05(G3 授权门控 + 确认词 + 拒绝转批注) | ✅ | `g3_available` 四查 + `authorize_write` + `/api/authorize` 三态;UAT CP1/CP2/CP3 |
| DATA-02(撰写 tmp 原子改名 + 崩溃恢复) | ✅ | `Path.replace` + `writing_tmp_exists` 二态;真 CLI 实测 + UAT CP4/CP8 |
| DATA-03(使命完成 + 只读归档) | ✅ | `state.py` 行 7 + `applyArchiveView` + 五路 409;UAT CP7 |
| DATA-04(档位 + 两角色循环 + 残余裁决) | ⚠️ | 功能面齐备并有测试;但严格档自链无界(G-idi03-1),标为「达成但有缺陷」 |

### Test Quality Audit

- 新增用例均为**先红后绿**(`test(idi-03-01): ... 先红` 等提交可查),非事后补测 ✅
- 四查反例为「AI 产物污染」形态(非空值),针对性强 ✅
- 边界覆盖:半份报告重跑不跳号、同号裁决拒绝、抛问内容级幂等、三态 repair_available ✅
- **覆盖缺口**:`test_next_check_n_half_report_no_skip` 所依赖的 `_wait_chain_idle` 与产品缺陷 G-idi03-1 正面冲突——该用例的修复跳恰好「不写 tmp、不发事件即 done」,正是触发无界自链的形态;用例靠 `busy()` 在两跳间的瞬时翻转窗口偶然通过,实测 11 次重跑中约 10-25% 失败(见下)。

### Decision Coverage(非阻塞门)

`node .claude/gsd-core/bin/gsd-tools.cjs check.decision-coverage-verify .planning/phases/idi-03-g3 .planning/phases/idi-03-g3/03-CONTEXT.md`:

```json
{ "skipped": false, "blocking": false, "total": 30, "honored": 30,
  "not_honored": [], "message": "All trackable CONTEXT.md decisions are honored by shipped artifacts." }
```

30/30 全部 honored。⚠️ **但决策覆盖门只扫 PLAN/SUMMARY 文本中的决策编号出现,不校验运行时行为**——G-idi03-1 正是 D-P3-16(「无常驻 scheduler,每跳结束重拉磁盘判定下一步」)的实现偏差,而该门报 30/30 通过。此项说明:决策覆盖通过 ≠ 决策语义在运行时成立。

### Anti-Patterns Found

零 TODO/FIXME/XXX/TBD/HACK/PLACEHOLDER(9 个产品文件)。

### Human Verification Required

无(本 Phase 的浏览器面已由自动化浏览器 UAT 全部收口,见 03-UAT.md;`behavior_unverified: 0`)。

---

## Gaps Summary

**4 项缺口(1 high / 1 medium / 2 low),全部未修复**(按 orchestrator 指令:issues > 0 时记录不修)。

### G-idi03-1(high,缺陷):严格档两跳自动链在「修复跳未产出 tmp」时无界自链

**位置**:`backend/session.py:1335-1354`(`start_repair._worker` 的 `finally` 尾部驱动判定)

**问题**:`finally` 尾部的断链判定为:

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

**实测确证**(`/tmp/defect_confirm.py`,严格档 + 修复跳「不写 tmp、不发事件即 done」):
```
20s 内跳数=10209  模式(前40)=CRCRCRCRCRCRCRCRCRCRCRCRCRCRCRCRCRCRCRCR
20s 后仍在飞(busy)=True  ← True 表示链未自停(无限自链)
```

**影响**:
1. **违反 D-P3-16**(每跳结束重拉磁盘判定下一步)与 §7.3「不留损坏状态」——链路不收敛,后台线程持续空转。
2. **回归套件间歇性失败**:`test_session.py::test_next_check_n_half_report_no_skip` 的修复跳正是该形态,靠 `_wait_chain_idle` 的 `busy()` 瞬时翻转窗口偶然通过。本验证者首次全量跑得 **1 failed, 216 passed, 6 skipped**;随后 11 次重跑全绿,判定为约 **10-25% 的 flake**。这不是「偶发测试问题」,而是产品缺陷在测试面的显影。
3. **真 CLI 场景下会烧 token**:AI 若连续两次不写 tmp,链路将持续真调用。

**修复方向(不在本次职责内,仅记录)**:`finally` 尾部的守卫应改为「tmp 缺失 → return」,即 `if not tmp_path.is_file(): return`(与 docstring 一致),或在 `except`/`else` 分支显式置断链标志。

### G-idi03-2(medium,缺陷):待裁决行锚位分歧导致 paused 态漏判

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

**修复方向(仅记录)**:`_selfcheck_substate` 的 paused 判定改为「`unpaired_verdicts` 非空 **或** `scan_pending_questions` 命中且锚后无对应裁决行」,或统一两扫描器的锚定语义。

### G-idi03-3(low,缺陷):归档态「继续自检」按钮残留可见

**位置**:`frontend/app.js:795-800`(`applyArchiveView`)

**问题**:`applyArchiveView` 未隐藏 `#btn-continue-check`;`loadArchiveView` → `loadChecksView(null)` 传 `null` 使 `sessionData` 分支跳过,`mode==='running'` 分支(报告为宽松档一检一修即 PASS 的形态)把「继续自检」重新显示。

**实测**:UAT CP7 归档态下 `btn-continue-check` 可见且可点,`visible buttons in checks-panel: ["继续自检"]`。

**缓解**:服务端 409 真防线成立(`POST /api/checks/start` → 409),不可实际推进。属呈现层残留,与 `processRoundBtn.classList.add('hidden')` 同处未覆盖到该按钮。

### G-idi03-4(low,缺陷):跨阶段重进时 checks-panel 残留

**位置**:`frontend/app.js:295-305`(`applySessionGates` 的 phase3 分支)

**问题**:phase3 分支只调 `applyPhase3Extras(data)` + `loadRoundsView(...)`,未隐藏 `checksPanel`。`applyPhase3Extras` 本身也不隐藏它(只隐藏 `writingView`)。因此从 phase5 项目切到 phase3 项目时,自检报告侧栏残留。

**实测**(UAT CP8):`fresh→phase3: checks-panel hidden: True`(干净页无残留),但 `phase5 → then→phase3: checks-panel hidden: False`,面板文本仍显示上一个项目的报告与「继续自检」。

**缓解**:服务端 409 兜住(`POST /api/checks/start` → 409),且 `hidePhase3Extras` 在 phase4 路径上正确隐藏(实测 `then→phase4: hidden True`)。属跨阶段切换的呈现层残留。

---

## 结论

**Phase 3 的 5 条 ROADMAP 成功判据在代码级全部找到可复现证据**,4 条 REQ 中 3 条完全达成、DATA-04 达成但有运行时缺陷;真 CLI E2E 有两次完整通过记录;30 项 D-P3 决策经权威门校验 30/30 honored;浏览器 UAT 8 检查点中 6 项 pass、3 项 issue(对应上述 G-idi03-1/3/4 的浏览器面表现)。

**但本 Phase 带缺陷收口**:G-idi03-1 是一处可稳定复现的产品缺陷,使严格档自链在特定形态下无界空转,并使回归套件间歇性失败(约 10-25% flake)。按 orchestrator 指令,本次验证**记录不修复**;`status: gaps_found`。

**后续动作建议**(交 orchestrator / 用户决策):
1. 修 G-idi03-1(finally 尾部守卫改 `if not tmp_path.is_file(): return`)——一行改动即可消除无界自链与测试 flake。
2. 修 G-idi03-2(统一两扫描器锚定语义或改 paused 判定)。
3. G-idi03-3 / G-idi03-4 为呈现层残留,有服务端 409 兜底,可择机修。
---
phase: idi-03-g3
plan: "04"
subsystem: frontend
tags: [g3-authorization, confirm-word-modal, reject-to-annotation, writing-view, tier-modal, selfcheck-report, verdict-cards, mission-complete, read-only-archive, xss-pipeline]

# Dependency graph
requires:
  - phase: idi-03-g3(plan 02)
    provides: backend/session.py 阶段 3/4/5 六函数(authorize/set_tier/start_writing/start_check/start_repair/verdict_append)+ snapshot 扩展(g3_available/writing_tmp_exists/selfcheck)+ 五路由
  - phase: idi-03-g3(plan 03)
    provides: POST /api/writing、/api/checks/start、/api/checks/repair 三条 202 受理路由(八路由族收口)
  - phase: idi-02-g2(plan 03)
    provides: 轮次视图/批注流/划词交互既有挂点(applySessionGates else 分支即本计划替换点)
provides:
  - frontend/index.html:#authorize-row/#btn-authorize/#authorize-hint、#confirmation-modal/#confirm-word-input/#btn-confirm-authorize/#btn-confirm-cancel、#writing-view/#btn-start-writing、#tier-modal/#btn-tier-loose/#btn-tier-strict、#checks-panel/#check-switcher/#latest-check/#check-controls/#verdict-cards/#btn-continue-check/#btn-continue-repair、#mission-complete-modal/#btn-mission-close
  - frontend/app.js:applySessionGates else 分支 phase4/phase5/mission_complete 真视图;applyPhase3Extras/applyWritingView/applyPhase5View/applyArchiveView;确认词 strip 全等放行链 + 拒绝转批注链;loadChecksView + renderVerdictCard(四 mode 控件清单)+ 裁决 POST 链;missionCelebrated 会话标记 + 归档视图渲染;done 拉新链 writing/check 维度扩展
  - frontend/style.css:「阶段 3/4/5 视图」分节(G3 按钮 / 撰写视图 / 模态输入框 / verdict-card / checks-panel / 归档灰化 / 欢呼模态)
affects: [idi-03-05(E2E 与浏览器人检 UAT 的对象面)]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
# Same estimateTokens scale (chars/4 over the realized diff), never a harness token count.
actuals:
  tokens: 8550     # ~34196 diff chars / 4(前端三文件;含注释)
  tasks: 3
  commits: 3       # MEASURED: git rev-list --count 2d4316b..HEAD
  plan_head_before: 2d4316b06b22efb4c8e8c48d13eada7aed33284e

# Tech tracking
tech-stack:
  added: []   # 零新依赖:原生 DOM + 原生 Selection API + 既有 renderMarkdown 管线
  patterns:
    - "阶段视图替换模式:applySessionGates 的 else 分支按 data.state 四路分派(phase3/phase4/phase5/mission_complete),共用 hidePhase3Extras 复位各容器显隐——避免状态间容器泄漏"
    - "按钮文案二态纯消费后端快照字段(writing_tmp_exists):前端不自判磁盘(文件即状态的呈现层纪律)"
    - "裁决卡按 mode 取键(共享数据契约):p2 → {number,location,issue,suggestion} 四键,paused → {number,text} 两键——与后端 _selfcheck_substate 组装面一字不差"
    - "会话内存标记(missionCelebrated/tierModalShown)控制一次性模态:不落盘,重开重现符合设计语义(D-P3-24)"

key-files:
  created: []
  modified:
    - frontend/index.html   # 三模态 + G3 授权行 + 撰写视图 + checks-panel
    - frontend/app.js       # 四路视图分派 + 五组交互链
    - frontend/style.css    # 「阶段 3/4/5 视图」分节
  pytest.ini: 未改动

key-decisions:
  - "确认词校验纯前端 strip 全等「确认授权」(textContent 比较不进渲染管线)——后端不重复解析自然语言,唯一防线 = 四查再查 + authorize_write 动作本身(D-P3-3/D-P3-4)"
  - "拒绝路径复用 window.prompt 取原因(照 app.js 既有 763 行先例)并走既有 POST /api/rounds/{n}/annotations 通道落 type=comment pending 批注——零新通道(D-P3-5)"
  - "phase5 的 awaiting_tier 与 checking 共用 applyPhase5View 入口,以 sessionData.state 分流:awaiting_tier 未选档弹模态且呈现「开始自检」,checking 按 selfcheck.mode 四分支切控件——避免同一容器两套渲染路径"
  - "归档只读防线全部为呈现层条件(processRoundBtn/divergenceEntry 隐藏、messageInput/sendBtn 禁用),零后端改动——服务端 409 是真防线(D-P3-25);applySessionGates 顶部统一复位,防跨状态容器泄漏"
  - "「继续自检」在 awaiting_tier 态文案切为「开始自检」但复用同一按钮与 POST /api/checks/start(后端 check_available 已覆盖两态判定,D-P3-11 不自动起检)"

requirements-completed: [FLOW-05, DATA-02, DATA-03, DATA-04]

# Coverage metadata (#1602) — one entry per shipped deliverable.
coverage:
  - deliverable: "G3 授权交互(按钮三态 + 确认词模态 + 拒绝转批注)"
    verification:
      kind: smoke
      ref: "bash /tmp/idi0304_t1.sh → g3-frontend-ok(四查盘 authorize 200 + 静态页三元素 grep)"
      status: pass
    human_judgment: false
  - deliverable: "phase4 撰写视图与按钮二态文案"
    verification:
      kind: source-assertion
      ref: "grep writing_tmp_exists + 两段按钮文案字面(D-P3-10 逐字)"
      status: pass
    human_judgment: false
  - deliverable: "档位模态 + 四 mode 裁决控件 + 残余裁决卡(含纯 P2 收口链)"
    verification:
      kind: smoke
      ref: "bash /tmp/idi0304_t2.sh → selfcheck-frontend-ok(paused 判定 + verdict 落盘 + mission_complete 两链)"
      status: pass
    human_judgment: false
  - deliverable: "mission_complete 欢呼模态 + 只读归档视图"
    verification:
      kind: smoke
      ref: "bash /tmp/idi0304_t3.sh → archive-frontend-ok(mission_complete + design 全文 + process 409)"
      status: pass
    human_judgment: false
  - deliverable: "浏览器视觉呈现(模态文案/裁决卡布局/归档灰化的实际观感)"
    human_judgment: true
    rationale: "冒烟只证元素在位与 API 链通;视觉/交互观感需真浏览器人检——交 idi-03-05 UAT 五点"
---

# Phase 3 Plan 04: 前端阶段 3-5 视图 Summary

前端阶段 3-5 三切片收口:applySessionGates 的 else 分支占位文案替换为阶段 4/5/完成态真视图——G3 授权确认词模态 + 拒绝转普通批注、phase4 撰写按钮二态、档位模态 + 四 mode 裁决控件 + 残余裁决卡、使命完成欢呼模态 + 只读归档视图,全部原生 DOM(零框架零新依赖),XSS 管线全程复用 renderMarkdown→stripUnsafeNodes。

## Accomplishments

- **切片 1(G3 授权 + phase4 撰写)**:`#authorize-row` 三态由 `snapshot.g3_available` 驱动(可点/disabled + title 列出四查差哪条);`#confirmation-modal` 确认词输入 strip 全等「确认授权」才 enable 放行按钮,放行 POST `/api/authorize` → 关模态拉新进入 phase4;拒绝路径(取消/关闭)→ `window.prompt` 取原因(缺省「授权被拒,继续完善」)→ 复用既有 annotations 通道落 type=comment pending 批注 → 留在 phase3;phase4 撰写按钮文案二态纯消费 `snapshot.writing_tmp_exists`(「撰写总设计文档」/「继续撰写(检测到上次中断的半成品,重写覆盖)」——D-P3-10 逐字)→ POST `/api/writing` 202 → SSE 直播 → done 拉新。
- **切片 2(档位 + 报告视图 + 裁决控件)**:`#tier-modal` 两选项各带一句话说明(宽松/严格)→ POST `/api/checks/tier` → 拉新呈「开始自检」(不自动起检,D-P3-11);`#checks-panel` 报告切换器 + 最新报告 markdown 渲染 + 按 `selfcheck.mode` 四分支切控件区(running=继续自检 / paused=抛问裁决卡 / p2=残余裁决卡 / resumed=只呈继续修复——§8.2 锁定版互斥);`renderVerdictCard` 按 mode 取键(p2 读 number/location/issue/suggestion 四键,paused 读 number/text 两键,与后端 snapshot 组装面一字不差),两按钮「修」「接受现状」+ note → POST `/api/checks/verdict` → 拉新(残余清零后端自动收口 → mission_complete)。
- **切片 3(欢呼 + 归档)**:`#mission-complete-modal` 由会话内存标记 `missionCelebrated` 控制首见弹一次(不落盘,重开重现,D-P3-24);归档视图三源可浏览(DESIGN.md 默认渲染 + 轮次切换器 + check 报告列表);只读防线呈现层三面隐藏(处理本轮批注/发散入口/授权按钮 + 消息输入禁用),零后端改动——服务端 409 是真防线(D-P3-25)。

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - 阻塞] 内联 verify 命令改由 /tmp 脚本承载**
- **Found during:** Task 1
- **Issue:** plan 的三条 `<automated>` verify 均为长内联 bash(含多段 printf 造盘与 heredoc 风格引号),经工具通道提交时被 sandbox 以长度/引号拒绝。
- **Fix:** 把每条 verify 的语义逐字写入 `/tmp/idi0304_t1.sh` / `_t2.sh` / `_t3.sh`(judgment 行 `grep -q` 与 sentinel echo 保持原文不变)后 `bash` 执行。
- **Files modified:** 无仓库文件(脚本在 /tmp)
- **Verification:** 三个 sentinel 全部复现(g3-frontend-ok / selfcheck-frontend-ok / archive-frontend-ok)。
- **Commit:** 不适用(执行方式偏差)

**2. [Rule 1 - 缺陷] 提交账本(plan-head ledger)基线被陈旧值污染**
- **Found during:** SUMMARY 阶段
- **Issue:** `phase-03/idi-03-04` 分支此前已存在(指向 a8d7294),其遗留的 `gsd-plan-head-before-idi-03-04` 账本值为 a8d7294——按它测 `rev-list --count` 会得 4,而真实 plan head 是 2d4316b(3 commits)。
- **Fix:** 分支从 main 的 2d4316b 重建(`git checkout -B`),账本改写为 `git rev-parse 2d4316b`,SUMMARY 的 `plan_head_before`/`commits` 按修正后的基线实测。
- **Files modified:** 无仓库文件(git dir 内账本)
- **Verification:** `git rev-list --count 2d4316b..HEAD` = 3,与 `git log --oneline main..HEAD` 三条一致。
- **Commit:** 不适用(测量基线偏差)

**3. [Rule 2 - 缺失关键功能] applySessionGates 顶部补只读防线复位**
- **Found during:** Task 3
- **Issue:** 归档视图会隐藏「处理本轮批注」并禁用消息输入;若用户随后拉新到非归档态(如造盘变更后重进),这些容器不会自动恢复,形成跨状态容器泄漏。
- **Fix:** 在 `applySessionGates` 顶部统一复位(`processRoundBtn` 取消 hidden、`messageInput`/`sendBtn` 解除 disabled),归档分支内再逐面隐藏。
- **Files modified:** frontend/app.js
- **Verification:** 全量回归 216 passed + 4 skipped 无回归;三条冒烟 sentinel 复现。
- **Commit:** f26c8e2

**Total deviations:** 3 auto-fixed(1 阻塞 / 1 缺陷 / 1 缺失关键功能)。**Impact:** 均为执行方式与健壮性修正,未改变任何 behavior 承诺;三切片交付面与 plan 逐字一致。

## Known Stubs

无。前端三文件无硬编码空值流向渲染、无占位文案残留(原 else 分支占位文案已被真视图替换)。

## Issues Encountered

无。三次 verify 冒烟与全量回归均一次通过。

## Self-Check: PASSED

- 三文件在盘:frontend/index.html、frontend/app.js、frontend/style.css — FOUND
- 三提交在盘:241aa76 / b249cd8 / f26c8e2 — FOUND
- 三条 sentinel 复现:g3-frontend-ok / selfcheck-frontend-ok / archive-frontend-ok — PASS
- 全量回归:216 passed, 4 skipped(与 Wave 3 基线持平,零回归)— PASS
- 零后端改动:`git diff --stat 2d4316b..HEAD -- backend/` 为空 — PASS

## Next Phase Readiness

Wave 5(idi-03-05)依赖本计划完成:`backend/tests/test_e2e_g3.py` 真 CLI E2E + 五判据对账 + 浏览器人检 UAT 五点(模态文案、裁决卡布局、欢呼模态、归档浏览的视觉面由人检覆盖——见 coverage 第 5 项)。
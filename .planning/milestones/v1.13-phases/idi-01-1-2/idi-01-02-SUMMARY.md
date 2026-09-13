---
phase: idi-01-1-2
plan: '02'
subsystem: testing
tags: [python, pytest, pure-functions, pathlib, state-derivation, markdown-grammar, file-as-state]

requires:
  - phase: idi-01-1-2
    provides: 无(本计划零依赖,可与 Plan 01 并行;不假设脚手架已就绪,verify 自带 venv 自举)
provides:
  - derive_state(project_path) 纯函数——§7.4 八行推导表全量实现(Phase 2/3 全部按钮逻辑的脊柱)
  - 完整轮判据(§7.3/§6.4):is_complete_round / last_nonempty_line / list_complete_rounds
  - check 编号辅助:max_check_number / latest_check_content(最新报告定位 + PASS 前缀判定)
  - transcript.md 文法(§6.1)读写:parse_transcript / append_message / transcript_exists(FLOW-02 恢复数据源)
affects: [idi-01-03(会话恢复读 transcript), idi-01-04(前端按推导状态渲染), Phase 2 轮次批注按钮逻辑, Phase 3 G3/自检授权链]

actuals:
  tokens: 6562
  tasks: 2
  commits: 3

tech-stack:
  added: []  # 零第三方依赖(纯 pathlib + 标准库);pytest 为既有 venv 测试基建
  patterns:
    - "文件即状态(D-19):状态纯函数从磁盘现状推导,无任何持久化/全局状态"
    - "表格驱动推导:§7.4 八行表自上而下首条命中,行条件互斥化,照抄表条件不改写"
    - "exact-match 判据 vs prefix-match 判据:授权标记 strip 后全等(前缀后缀均不算),PASS 结论行 startswith 前缀(尾注仍算)"
    - "末字符二进制探测的无尾换行容错追加(a 模式 + 先补换行)"

key-files:
  created:
    - backend/state.py
    - backend/transcript.py
    - backend/tests/__init__.py
    - backend/state.py#derive_state
  modified: []

key-decisions:
  - "derive_state 返回结构固定为 {state, current_round, current_check},current_round 仅 phase3、current_check 仅 phase5_checking 有值——形状被 Phase 2/3 按钮逻辑消费,本阶段内锁定"
  - "行 4/5 的 AUTHORIZATION.md/DESIGN.md 用例必须先建 docs/:表自上而下首条命中,行 1「无 docs/」先于一切;正常运行中授权前 docs/ 早已存在,无 docs/ 的构造是超表形态"
  - "行 2 兜底:磁盘形态超出 §7.4 表(如 docs/ 存在但为空目录)回退 phase12_in_progress,保证任意目录形态给确定判定"
  - "append_message 自建父目录:新讨论第一条消息时 docs/ 尚不存在,a 模式建文件需先有目录(计划只说'不存在会建',父目录自举是实现该承诺的必要补全)"
  - "防御性兜底不扩表:表条件已互斥化,超出表的形态只回退行 2,不自行发明新状态"

patterns-established:
  - "纯模块可直接导入:backend.state / backend.transcript 零框架依赖,其他计划(含 FastAPI 层)直接 import,无配置面"
  - "磁盘输入不受信:非 UTF-8 以 errors=replace 读、读失败按空文档处理并 warning(T-idi02-01:不崩、给确定判定)"
  - "文法判定三态:整行精确匹配(起始行)、strip 后全等(授权标记)、前缀匹配(PASS 结论行)——§6.4 各结构的匹配语义不同"

requirements-completed: [FLOW-01]

coverage:
  - id: D1
    description: "derive_state 按 DESIGN.md §7.4 八行推导表自上而下首条命中,覆盖全部 8 行(空目录→phase1_new、无完整轮→phase12_in_progress、完整轮→phase3、已授权→phase4、设计完成→phase5_awaiting_tier、自检中→phase5_checking、PASS→mission_complete),含半成品轮视为不存在、非连续轮编号取实际最大完整、tmp 残留不影响、多 check 取最大编号四个边界"
    requirement: FLOW-01
    verification:
      - kind: unit
        ref: "backend/tests/test_state.py#test_row1_empty_dir_is_phase1_new .. test_row7_multiple_checks_take_max_number (17 用例)"
        status: pass
    human_judgment: false
  - id: D2
    description: "完整轮判据:轮次文档最后一个非空行恰为 `> 申请授权:是|否`(strip 后全等,前缀/后缀均不算)才算完整轮,否则视为不存在;当前轮取最大完整轮编号"
    requirement: FLOW-01
    verification:
      - kind: unit
        ref: "backend/tests/test_state.py#test_is_complete_round_exact_match_no_prefix_suffix_tolerance"
        status: pass
    human_judgment: false
  - id: D3
    description: "transcript.md 文法 parse/append:起始行 [user]/[ai] 整行精确匹配(strip 后),消息体首尾 strip、内部空行保留;append 幂等可重入(只追加新条目、既有消息不变)、无尾换行先补、文件不存在则建、role 非 user/ai 抛 ValueError"
    requirement: FLOW-01
    verification:
      - kind: unit
        ref: "backend/tests/test_transcript.py#test_parse_basic_three_messages .. test_parse_only_starters_no_body (11 用例)"
        status: pass
    human_judgment: false
  - id: D4
    description: "PASS 结论行前缀判定:最新 DESIGN-check-N.md 末行以 `> 核查结论:PASS` 开头(尾注如「(问题 3 项修复完毕)」仍算 PASS)即 mission_complete"
    requirement: FLOW-01
    verification:
      - kind: unit
        ref: "backend/tests/test_state.py#test_row7_latest_check_pass_line_is_mission_complete"
        status: pass
    human_judgment: false

duration: 10min
completed: 2026-09-09
status: complete
---

# Phase idi-01 Plan 02: 状态推导 + transcript 文法 Summary

**derive_state() 按 §7.4 八行表自上而下首条命中实现"文件即状态"脊柱(含完整轮判据、半成品轮视为不存在、tmp 残留免疫),transcript.md 按 §6.1 `[user]`/`[ai]` 起始行文法实现 parse/append 幂等读写——两纯后端模块零框架依赖,28 用例全绿**

## Performance

- **Duration:** ~10 min
- **Started:** 2026-09-09T03:24:10Z
- **Completed:** 2026-09-09T03:34:59Z
- **Tasks:** 2/2
- **Files modified:** 5 created(全部为本计划 files_modified 清单内)

## Accomplishments
- derive_state(project_path) 纯函数:§7.4 八行表全量实现,严格自上而下首条命中——Phase 2/3 所有按钮逻辑的脊柱(D-P1-11)
- 完整轮判据(§7.3 + §6.4):末行授权标记 strip 后全等判定,半成品轮视为不存在、当前轮取最大完整轮;PASS 结论行 startswith 前缀匹配(尾注仍算)
- transcript.md 文法(§6.1)parse/append:起始行整行精确匹配、多行消息体不需转义、脏头丢弃 + warning、无尾换行容错、幂等可重入——FLOW-02(Plan 03)会话恢复的数据源
- 磁盘输入不受信(T-idi02-01):全部读取 errors=replace、读失败给确定判定不崩

## Task Commits

Each task was committed atomically:

1. **Task 1: derive_state()——§7.4 八行推导表 + 完整轮判据** - `5b3aff6` (feat,RED→GREEN:先 17 用例跑红再实现转绿)
2. **Task 2: transcript.md 文法——parse 与 append** - `c967789` (feat,RED→GREEN:先 11 用例跑红再实现转绿)

**Plan metadata:** `b2208fe` (merge: 工作分支 phase-01/idi-01-02 合回 main,per 仓库 CLAUDE.md §5 分支纪律)

## Files Created/Modified
- `backend/state.py` - derive_state 纯函数 + §7.4 八行表 + 完整轮判据辅助函数(is_complete_round/last_nonempty_line/list_complete_rounds/max_check_number/latest_check_content)
- `backend/transcript.py` - §6.1 文法 parse_transcript/append_message/transcript_exists
- `backend/tests/__init__.py` - 空包标记(单仓 pytest 根导入)
- `backend/tests/test_state.py` - 17 用例:八行表每行 + 边界(半成品轮/非连续编号/tmp 残留/末行空行/行尾空白/多 check 取最大/PASS 行内前缀 vs 整行)
- `backend/tests/test_transcript.py` - 11 用例:基础 3 条解析、多行体、追加、空文件、建文件、无尾换行、脏头丢弃、未知角色 ValueError

## Decisions Made
- 返回结构锁定 `{state, current_round, current_check}`;current_round 仅 phase3、current_check 仅 phase5_checking 有值——reversibility "costly",形状变更需协调 Phase 2/3 全部调用点
- 兜底行:磁盘形态超出 §7.4 表(如 docs/ 存在但为空目录、且无轮/无 DESIGN/无 AUTHORIZATION——正落行 2)之外的超表形态回退 phase12_in_progress,不发明新状态
- `_ends_without_newline` 用二进制读末字符而非文本 read_text(避免整读大文件;T-idi02-01 缓解)
- 零第三方依赖兑现:两 module 仅 import logging/re/pathlib(计划工程约定)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] 行 4/5 测试目录构造与 §7.4 表冲突**
- **Found during:** Task 1(首次 GREEN 运行)
- **Issue:** 初版 test_row4/test_row5 用例只建 AUTHORIZATION.md/DESIGN.md 不建 docs/,被行 1「无 docs/ → phase1_new」自上而下首条命中(权限授予前 docs/ 必已存在——G1 定稿先落轮次文档),2 用例失败
- **Fix:** 用例改为先构造 docs/(含合法完整轮),既符合推导表也贴合真实到达路径
- **Files modified:** backend/tests/test_state.py
- **Verification:** 17 用例全绿(derive_state 实现未变——实现本就严格照抄表)
- **Committed in:** 5b3aff6(Task 1 commit 内)

**2. [Rule 2 - Missing Critical] append_message 父目录自举**
- **Found during:** Task 2(用例 5 追加建文件)
- **Issue:** 计划说「a 模式打开(不存在会建)」,但新讨论第一条消息时 docs/ 目录尚不存在——Path.open("a") 在父目录缺失时抛 FileNotFoundError,「文件被创建」承诺不成立
- **Fix:** append_message 先 mkdir(parents=True) 再追加(一行 if);属完成计划所述行为所必需的关键补全
- **Files modified:** backend/transcript.py
- **Verification:** test_append_creates_file 由红转绿;全部 11 用例过
- **Committed in:** c967789(Task 2 commit 内)

---

**Total deviations:** 2 auto-fixed(1 bug / 1 missing critical)
**Impact on plan:** 均为实现计划所述行为的最小补全,无范围蔓延;§7.4 表条件未被改写。

## Issues Encountered
None —— 计划的 verify 命令(含 venv 自举)逐步按原样跑通;.venv 已由并行执行的 Plan 01 创建符合预期(self-bootstrap 未触发)。

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Plan 03(FLOW-02 会话恢复)可直接 `from backend.transcript import parse_transcript, append_message, transcript_exists` 重建消息流
- Plan 04(前端)与 Phase 2/3 按钮逻辑可直接 `from backend.state import derive_state` 取 {state, current_round, current_check} 驱动 UI
- 两模块零框架依赖、无配置面,导入即可用;blocking 无

---
*Phase: idi-01-1-2*
*Completed: 2026-09-09*

## Self-Check: PASSED

全部 6 个产出文件存在;全部 3 个 commit(5b3aff6 / c967789 / b2208fe)在 git 历史;28 用例(17 state + 11 transcript)全绿;无未落盒 stub(两模块零 TODO/FIXME/占位)。

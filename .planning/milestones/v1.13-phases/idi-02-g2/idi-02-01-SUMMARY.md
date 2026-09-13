---
phase: idi-02-g2
plan: "01"
subsystem: database
tags: [annotations, json-storage, markdown-parsing, regex, pure-functions, tdd]

# Dependency graph
requires:
  - phase: idi-01-1-2
    provides: backend/state.py 常量(AUTH_MARKER_YES/NO、PASS_PREFIX、last_nonempty_line)、transcript.py 形态模子(空形态+父目录自举)、g1.py 读-改-写先例
provides:
  - backend/annotations.py 纯存储模块:load / append_item / writeback / select_pending / locate_quote / annotations_path(§6.2 八字段字面契约、aN-NN id、空形态、回写只认 id)
  - backend/grammar.py 六条 §6.4 机器文法解析器:维度表/未决清单/授权标记/批注回应表/PASS 结论行(锚点取末一处)/裁决追加行(同号配对)
  - Wave 2 process_round 与 Wave 3 前端批注流的唯一数据契约(grammar 回应表 → annotations.writeback 已闭环证明)
affects: [idi-02 (Wave 2 process_round 回写、ask_lite 落盘), idi-02 (Wave 3 前端批注流渲染/高亮定位), idi-03 (G3 四处机械校验消费 grammar 判定)]

# Actuals (#2632) — pairs with the plan's `estimate` to calibrate future estimates.
# Same estimateTokens scale (chars/4 over the realized diff), never a harness token count.
actuals:
  tokens: 12305    # 49219 diff chars / 4(git diff over plan_head_before..HEAD)
  tasks: 3
  commits: 4        # MEASURED: git rev-list --count 653f6cd..HEAD
  plan_head_before: 653f6cd0a64bfff2bcfa4667ab4b38219d0e4d14

# Tech tracking
tech-stack:
  added: []   # 零新增依赖(纯标准库 logging/json/pathlib/datetime/re)
  patterns:
    - "解析/判定分离:parse_* 返回行结构、is_* 返回 bool(state.py 先例平移)"
    - "空形态统一返回:文件不存在与 JSON 损坏同形态 {round, items: []}(transcript.py 先例平移)"
    - "读-改-写整文件重写:writeback/append_item 均 load→改→json.dumps 整体落盘(g1.py 先例平移)"
    - "常量复用禁止复制:grammar.py from backend.state import 四符号(identity 校验同一对象)"
    - "RED 骨架模式:函数组 NotImplementedError 占位使测试可收集、失败在目标断言点"

key-files:
  created:
    - backend/annotations.py
    - backend/grammar.py
    - backend/tests/test_annotations.py
    - backend/tests/test_grammar.py
  modified: []

key-decisions:
  - "维度表状态列脏值 fail-closed:值不在 {✓,◐,✗}(如「待定」)判非绿——刻意偏离 §6.4 字面(无◐无✗即绿)取保守,已写进 is_dimension_table_green docstring(计划 action 原文要求)"
  - "未决清单照 §6.4 字面仅找「待决」:脏值行(如「已解决」)不算待决即清零——与维度表 fail-closed 刻意不同(判定式原文如此)"
  - "locate_quote 在 Task 1 一并交付(计划 action 第 6 点明示可选):闭环用例集中在 Task 3 补"
  - "writeback 零命中不写盘:读失败路径(load 返回空形态)不会走到写,无覆盖损失面(T-idi02-02 缓解)"
  - "annotations 模块 docstring 避免出现框架/校验库名:防全文件 grep 误报(acceptance criteria 字面合规)"

patterns-established:
  - "Pattern: 共通表格解析 _extract_table(标题关键词定位 + 空行容 markdown 惯例 + 分隔行不收 + 表头丢弃)——后续表格型文法扩展复用"
  - "Pattern: 回应表→回写闭环 = parse_annotation_responses 组 answers dict → writeback(同 id 配对为唯一依据,D-P2-13)"

requirements-completed: [FLOW-07, DATA-01]

# Coverage metadata (#1602) — one entry per shipped deliverable.
coverage:
  - id: D1
    description: "annotations.json 纯存储模块:load 空形态(不存在/脏 JSON 同形态)、append_item §6.2 八字段 + aN-NN id、writeback 命中/未命中语义、select_pending 过滤 plain"
    requirement: DATA-01
    verification:
      - kind: unit
        ref: backend/tests/test_annotations.py#test_load_missing_file_returns_empty_shape
        status: pass
      - kind: unit
        ref: backend/tests/test_annotations.py#test_load_corrupt_json_returns_empty_shape
        status: pass
      - kind: unit
        ref: backend/tests/test_annotations.py#test_append_item_first_entry_full_fields
        status: pass
      - kind: unit
        ref: backend/tests/test_annotations.py#test_append_item_ids_increment_same_round
        status: pass
      - kind: unit
        ref: backend/tests/test_annotations.py#test_append_item_round_three_starts_a3_01
        status: pass
      - kind: unit
        ref: backend/tests/text_annotations 模块全量(22 passed,含 writeback 命中/未命中混合、select_pending)
        status: pass
    human_judgment: false
  - id: D2
    description: "locate_quote 定位算法四分支 + 防呆:唯一命中起点 / 多命中 before 后缀二次定位 / 仍不唯一取第一处 / 无匹配 None / 空 quote None(精确匹配,无模糊算法)"
    requirement: DATA-01
    verification:
      - kind: unit
        ref: backend/tests/test_annotations.py#test_locate_quote_unique_match
        status: pass
      - kind: unit
        ref: backend/tests/test_annotations.py#test_locate_quote_multiple_uses_before_suffix
        status: pass
      - kind: unit
        ref: backend/tests/test_annotations.py#test_locate_quote_multiple_no_before_match_takes_first
        status: pass
      - kind: unit
        ref: backend/tests/test_annotations.py#test_locate_quote_no_match_returns_none
        status: pass
      - kind: unit
        ref: backend/tests/test_annotations.py#test_locate_quote_empty_quote_returns_none
        status: pass
    human_judgment: false
  - id: D3
    description: "grammar.py 六条 §6.4 文法解析器 + 判定函数(维度表/未决清单/授权标记/批注回应表/PASS 结论行/裁决追加行),复用 state.py 常量(identity 同一对象)"
    requirement: FLOW-07
    verification:
      - kind: unit
        ref: backend/tests/test_grammar.py 全量 32 passed(正反例矩阵:全绿/◐/✗/空表/脏值 fail-closed/清零/待决/是/否/前缀/后缀/末行后空行/提取/空 id 跳过/空表/PASS/仅FIX/括注/双结论行锚点取末一处×2/未配对/同号配对/多号部分配对/锚前行不收/形态不符)
        status: pass
      - kind: automated
        ref: "identity 校验:grammar.AUTH_MARKER_YES is state.AUTH_MARKER_YES 等 4 符号(命令行 python -c 断言通过)"
        status: pass
    human_judgment: false
  - id: D4
    description: "grammar 回应表 → annotations 回写闭环:手造第 1 轮两条 pending + 第 2 轮回应表(只含 a1-01)→ writeback 后 a1-01 answered、a1-02 保持 pending、返回 1(D-P2-12/D-P2-13 纯函数级证明)"
    requirement: FLOW-07
    verification:
      - kind: unit
        ref: backend/tests/test_annotations.py#test_grammar_response_table_to_writeback_closure
        status: pass
    human_judgment: false
  - id: D5
    description: "全量 pytest 回归基线不降:66 passed + 2 skipped 之上叠加 54 新用例零失败"
    requirement: FLOW-07
    verification:
      - kind: automated
        ref: ".venv/bin/python -m pytest backend/tests/ -q → 120 passed, 2 skipped(66 基线 + 54 新增)"
        status: pass
    human_judgment: false

# Metrics
duration: 28 min
completed: 2026-09-09
status: complete
---

# Phase idi-02 Plan 01: 轮次收敛循环数据脊柱(annotations 存储 + §6.4 机器文法) Summary

**annotations.json 读写纯模块(§6.2 八字段/aN-NN id/空形态/回写只认 id)与六条 §6.4 机器文法解析器(维度表/未决清单/授权标记/回应表/PASS 锚点取末一处/裁决同号配对),54 个正反例用例 + 回写闭环全绿,基线 66→120 不降**

## Performance

- **Duration:** 28 min
- **Started:** 2026-09-09T16:04:15Z
- **Completed:** 2026-09-09T16:32:17Z
- **Tasks:** 3 / 3
- **Files modified:** 4(全部新建)

## Accomplishments
- backend/annotations.py:§6.2 字面契约的纯 pathlib 存储模块——load(文件不存在/JSON 脏文件同返回 {round, items: []} 空形态,D-P2-5)、append_item(八字段一字不差、id=aN-NN 递增、plain 即时 answered)、writeback(只认回应表 id、未提及保持 pending、返回命中数,D-P2-13)、select_pending(plain 不计,D-P2-15)、locate_quote(quote+before 精确匹配四分支 + 空 quote 防呆,D-P2-6)
- backend/grammar.py:六条 §6.4 文法全部解析 + 判定就位,复用 state.py 四符号(identity 校验同一对象,源码零第二份标记字面量);维度表状态脏值 fail-closed、未决清单照字面、PASS 锚点取末一处(双结论行正反两例)、裁决同号配对/未配对/锚前行不收/形态不符全覆盖
- 闭环证明:手造上一轮 annotations(两条 pending)+ 新轮回应表(只含 a1-01)→ parse_annotation_responses → writeback → 命中回写/未命中保持 pending/返回 1——Wave 2 process_round 只需把这条链挂到 done 后执行
- 测试矩阵:22 + 32 = 54 新用例全绿,全量回归 120 passed + 2 skipped(基线 66 passed + 2 skipped 不降)

## Task Commits

Each task was committed atomically:

1. **Task 1: annotations.py 纯存储模块(load/append_item/writeback/select_pending/locate_quote)+ 16 用例** - `b857f36` (feat)
2. **Task 2 RED: 六条 §6.4 文法正反例矩阵(先红)** - `2159c8c` (test)
3. **Task 2 GREEN: 六条文法解析器转绿** - `da4a5b7` (feat)
4. **Task 3: locate_quote 五分支用例 + grammar×annotations 回写闭环** - `a5445ae` (test)

**Plan metadata:** 本 commit(docs: complete plan)

_Note: Task 2 为 tdd="true":RED(2159c8c)先于 GREEN(da4a5b7);locate_quote 已在 Task 1 随模块交付(计划明示可选),其专属用例 + 闭环在 Task 3 补齐。_

## Files Created/Modified
- `backend/annotations.py` - annotations.json 读写纯模块:ANNOTATIONS_TEMPLATE / annotations_path / load / append_item / writeback / select_pending / locate_quote(零第三方依赖,206 行)
- `backend/grammar.py` - §6.4 六条机器文法解析器:_extract_table 共通解析 + parse/is 分离九个公开函数 + _VERDICT_RE / _last_conclusion_index(复用 state 四符号,283 行)
- `backend/tests/test_annotations.py` - 22 用例:空形态×2、建条目八字段全等、id 递增、跨轮、plain 即答、回写命中/未命中/覆盖/零命中、select_pending、locate_quote 五分支、回写闭环
- `backend/tests/test_grammar.py` - 32 用例正反例矩阵:六条文法 × 合规/非合规/脏变体/空形态 + 三类边界具名具例(双结论行锚点取末一处、同号裁决配对、未配对)+ 无关标题不误收 + 五件套混合判定

## Decisions Made
- 维度表状态列脏值 fail-closed(计划 action 原文要求的显式设计选择):值不在 {✓,◐,✗} 的行(如「待定」)判非绿——比 §6.4 字面「无 ◐ 与 ✗」更保守,docstring 一行注明 deliberate deviation
- 未决清单与维度表刻意不同:清单照 §6.4 判定式原文仅找「待决」字样(脏值不算待决),因「清零 ⇔ 无待决」是 DESIGN.md 原文;两处语义差异均写入各自 docstring
- locate_quote 随 Task 1 模块一并交付、用例留 Task 3(计划 action 第 6 点明示此选项;保持函数与模块同 commit 的内聚性)
- writeback 零命中不写盘(命中数为 0 时跳过落盘)——读失败路径(load 返回空形态)不会走到写,消解 T-idi02-02「坏 JSON 被静默当空形态后覆盖丢失旧批注」的损失面
- _extract_table 容 markdown 空行惯例(标题与表间的空行跳过)但不容表内空行(表格开始后遇非 | 行即终止)——比"连续 | 行"字面更贴真实 AI 产物形态,反例(标题后直接正文、无关标题表格)有专属用例

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] _extract_table 初版三个解析缺陷(GREEN 首轮 8 用例失败)**
- **Found during:** Task 2(GREEN 阶段首跑)
- **Issue:** 初版表格解析:①标题与表格之间的空行(markdown 惯例)被当"表格结束";②markdown 分隔行 `|---|---|` 被当数据行收进结果;③离开目标标题后继续扫(非表格行仅重置 in_target)
- **Fix:** 重写循环:表格首行未出现时空行跳过、分隔行(`_is_separator_row`:非空 cell 全部只由 -/: 构成)不收、目标表定位后遇新标题 break
- **Files modified:** backend/grammar.py(_extract_table)
- **Verification:** 32 用例全绿(含空 id 跳过、无关标题不误收、空表)
- **Committed in:** da4a5b7(Task 2 GREEN commit)

**2. [Rule 1 - Bug] locate_quote before 二次定位测试首次手算索引错误**
- **Found during:** Task 3(locate_quote 用例编写)
- **Issue:** 手算中文字符串索引偏移(「先说一遍甲乙丙」的「甲」起点是 4 非 3)
- **Fix:** 以 python 实算(start 4 与 17)重写期望值,并复核唯一命中用例索引 10 亦实算无误
- **Files modified:** backend/tests/test_annotations.py
- **Verification:** 22 用例全绿
- **Committed in:** a5445ae(Task 3 commit)

**3. [Rule 1 - Consistency] annotations.py docstring 措辞调整**
- **Found during:** Task 1(acceptance criteria 自检)
- **Issue:** 模块 docstring 提及框架/校验库名(以说明「不使用」),全文件 grep 会误报"import 区含框架关键词"字面检查
- **Fix:** 措辞改为「不在本模块重定义字段模型」「不碰 Web 框架层」,语义不变
- **Files modified:** backend/annotations.py(仅 docstring 两行)
- **Verification:** grep 干净 + 16 用例仍绿
- **Committed in:** b857f36(Task 1 commit)

---

**Total deviations:** 3 auto-fixed(2 Rule 1 bug、1 Rule 1 consistency)
**Impact on plan:** 全部为字面/索引/解析边界层的实现级修正,零范围蔓延;三个修正各自有绿色用例锁定。

## TDD Gate Compliance (Task 2)

- **RED commit:** `2159c8c`(test(idi-02-01): 六条 §6.4 文法正反例矩阵(先红))— 32 用例全部收集并在目标函数断言点抛 NotImplementedError(非 ImportError,模块骨架已建;Phase 1 idi-01-03 RED 先例同构)
- **GREEN commit:** `da4a5b7`(feat(idi-02-01): 六条 §6.4 文法解析器转绿)— 32 passed
- **REFACTOR:** 无(实现一次成型,无需清理)→ 无 refactor commit,符合"REFACTOR commits only on change"
- **门序校验:** git log 顺序 RED(2159c8c)→ GREEN(da4a5b7),先红后绿成立

## Issues Encountered
None —— 计划的三任务按 store → parse → verify 顺序一次走通;两个 GREEN 首轮的实现级 bug 均按 tdd 红绿循环在 GREEN 迭代内即时修复(见 Deviations)。

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Wave 2(process_round / ask_lite 落盘)可直接 import 本计划契约:parse_annotation_responses → writeback 的闭环链已用例锁定,process_round 只需在 done 后把它挂到「下一轮文档存在」判定后执行
- Wave 3(前端)消费 annotations.load + locate_quote 做批注流渲染与高亮;select_pending 供侧栏未处理数
- state.py 常量单一来源已被 identity 断言锁定——Phase 3 的 G3 消费同一组判定无漂移风险

## Self-Check: PASSED

- 关键文件:backend/annotations.py FOUND、backend/grammar.py FOUND、backend/tests/test_annotations.py FOUND、backend/tests/test_grammar.py FOUND(4/4)
- 提交:b857f36 FOUND、2159c8c FOUND、da4a5b7 FOUND、a5445ae FOUND(4/4)
- commits 实测:git rev-list --count 653f6cd..HEAD = 4(生产 4 + 本 SUMMARY 1 = 5)
- 全量:.venv/bin/python -m pytest backend/tests/ -q → 120 passed, 2 skipped

---
*Phase: idi-02-g2*
*Completed: 2026-09-09*

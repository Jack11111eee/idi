# Phase 3 Pattern Map

**Phase:** idi-03 (授权、自检与终点——G3、档位、使命完成归档;v1.13 milestone FINAL phase)
**Mapped:** 2026-09-10
**Files classified:** 11(1 new + 10 modified;测试族单独列)
**Analogs found:** 11 / 11(全部有仓库内 analog;零 "no analog" 文件)

All excerpt line numbers below refer to the current git-tracked source under `backend/` and `frontend/`. All analog paths verified tracked via `git ls-files backend/ frontend/`(zustand:全数在列,见文末 Metadata)。DESIGN.md 符号:**§4.4**(G3 门)、**§5.4**(权限矩阵)、**§6.1**(目录结构)、**§6.4**(判定式①② + 报告文法——锁定版,只消费)、**§7.3**(自愈)、**§7.4**(行 4-7)、**§8.1/§8.2**(G3 与自检全节)。

**本阶段零改动面(消费侧,防 planner 误触):**
- `backend/state.py`(≈0 改动,D-P3-23):七状态常量(lines 21-27)、`max_check_number`(lines 75-84,半份报告不校验直接计入)、`latest_check_content`(lines 87-92)、`derive_state` 行 4/5/6/7(lines 122-143)全部就绪
- `backend/ai_caller.py`(零改动):权限矩阵规则 1/2 已拒绝 DESIGN.md/AUTHORIZATION.md、放行 tmp(make_permission_decision,lines 60-69);system prompt 已告知 tmp 纪律(build_system_prompt,lines 105-108)
- `backend/annotations.py`(零改动,D-P3-5):拒绝批注走 append_item 现成通道
- `backend/grammar.py` 六条文法已锁——**判定式①②语义禁改**;本阶段 grammar 仅允许纯增量(见 Modified Files 4)
- `backend/transcript.py` / `cli_check.py` / `config.py` / `events.py` 零改动

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `backend/g3.py`(NEW,模块名归 planner) | model/storage (pure) | file-I/O | `backend/g1.py` | exact(后端写受控产物 + FileExistsError 幂等) |
| `backend/prompts.py` (MOD,+3 build 函数族) | utility | transform | self(`build_round_prompt` lines 259-352) | exact(四五六次同模复制) |
| `backend/session.py` (MOD,+3 流水线 + 3 入口判定 + snapshot 扩展) | service | event-driven/background | self(`process_round` lines 528-629) | exact |
| `backend/grammar.py` (MOD,+2 解析器) | utility (pure parser) | transform | self(`parse_auth_marker` lines 183-197 / `parse_dimension_table` lines 120-132) | extend(纯增量,既有六条禁改) |
| `backend/main.py` (MOD,+8 路由) | route/controller | request-response | self(`/api/g1` lines 194-215 + `/api/rounds/*` lines 233-350) | extend |
| `frontend/app.js` (MOD) | component | request-response + SSE | self(`applySessionGates` else 分支 lines 274-279 + `showPermissionModal` lines 608-621) | extend |
| `frontend/index.html` (MOD) | component (markup) | — | self(permission-modal lines 118-128) | extend |
| `frontend/style.css` (MOD) | component (style) | — | self(`.overlay`/`.overlay-card` lines 143-174) | extend |
| `backend/tests/test_session.py`(MOD 或新同族文件) | test | event-driven | self(RoundWritingFake lines 744-762 + HangingFake lines 940-961) | extend |
| `backend/tests/test_grammar.py` (MOD) | test | transform | self(is_pass_conclusion / unpaired 正反例族) | extend |
| `backend/tests/test_e2e_rounds.py`(MOD 或族内新文件) | test (E2E) | real-call | self(test_e2e_rounds.py 全形态) | extend |

---

## New Files

### 1. `backend/g3.py` — G3 四查 + AUTHORIZATION.md 写入纯函数 (D-P3-1 / D-P3-4)

**Role:** 纯 pathlib 模块,零 FastAPI / 零 AI 依赖(与 g1.py 同级同风格)。命名归 planner(CONTEXT 原文 "may be a new module or g1.py-family file — planner decides")。
**Data Flow:** file-I/O;AUTHORIZATION.md 内容 = 后端生成明文,两要素必备:授权时间 ISO-8601 + 操作者确认词标记行(§7.4 授权痕迹)。
**Closest analog:** `backend/g1.py`(全文件 52 行,结构完全同构——照抄模子)。

**模块头 docstring 形态** — 照 `g1.py` lines 1-15:

```python
# -*- coding: utf-8 -*-
"""G1 定稿纯函数(PLAN idi-01-04 Task 2 / FLOW-03 / DESIGN.md §4.4 / D-P1-12)。

G1 是后端动作,不涉及 AI:把 docs/draft.md 定稿为 docs/discuss-round-1.md,
并在文档末尾追加合规的 `> 申请授权:否` 标记行(§6.4 文法:strip 后全等)。

规则:
  - draft.md 不存在 → FileNotFoundError(先有雏形才能定稿)
  - discuss-round-1.md 已存在 → FileExistsError(G1 只走一次,幂等防护;
    重开即 phase3,重入合法路径不存在)
  ...
零第三方依赖、纯 pathlib,不碰 FastAPI/AI 层。
"""
from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)
```

g3.py 对应:文件名常量 `AUTHORIZATION_FILENAME = "AUTHORIZATION.md"`(**项目根,不在 docs/ 下**,§7.4 行 3);docstring 引用 §4.4/§7.4/D-P3-4。

**前置校验 + FileExistsError 幂等双查** — 照 `g1.py` lines 37-43 的"先缺前置、再防重复"顺序:

```python
    if not draft_path.is_file():
        raise FileNotFoundError(f"尚无雏形草稿({DRAFT_FILENAME})——先在阶段 1-2 讨论出雏形再认可")

    if round_path.is_file():
        raise FileExistsError(
            f"已定稿({ROUND_1_FILENAME} 已存在)——G1 只走一次,项目已在轮次阶段"
        )
```

g3.py 对应(AUTHORIZATION.md 已存在 → FileExistsError,路由层 409):**写入前四条机械校验由调用方(session 层)完成后端再查**(D-P3-4 防绕过——POST /api/authorize 入口后端独立重判四条 + phase3,任一不过 → 409,语义同 process_round 入口判定 False → 409 先例,session.py lines 560-561)。四查不过用 409 而非 FileNotFoundError。

**写入形态** — 照 `g1.py` lines 45-51("构造文本 → mkdir 防御 → write_text"):

```python
    draft_text = draft_path.read_text(encoding="utf-8", errors="replace")
    # draft 全文(尾部空白 rstrip)换行接标记行换行:标记行是最后的非空行
    finalized = f"{draft_text.rstrip()}\n\n{AUTH_MARKER_NO}\n"

    round_path.parent.mkdir(parents=True, exist_ok=True)  # docs/ 理论上已存在(draft 在其中),防御
    round_path.write_text(finalized, encoding="utf-8")
    logger.info("G1 定稿完成:%s(draft.md 保留)", round_path)
    return round_path
```

g3.py 对应(具体文案 Claude's Discretion,两要素必备):

```python
    # 授权痕迹(§7.4):授权时间 ISO-8601 + 操作者确认词标记行——后端生成,非 AI
    from datetime import datetime, timezone
    authorized_at = datetime.now(timezone.utc).isoformat()
    content = (
        "# 授权记录\n\n"
        f"- 授权时间:{authorized_at}\n"
        "- 操作者确认词:确认授权\n"
        "- 说明:用户在 G3 门输入确认词「确认授权」,由后端写入本文件。\n"
    )
    auth_path.write_text(content, encoding="utf-8")
    logger.info("G3 授权落盘:%s", auth_path)
```

注:AUTHORIZATION.md 写项目根(enter_project 已保证目录存在),无 g1 那样的 docs/ 父目录自举需求,可省 mkdir 或仅防御性保留。

**组合判定 g3_available(同文件或挂 session.py——planner 定)** — D-P3-1 四条:①当前轮 annotations 无 pending comment(`annotations.select_pending` 空)②未决清单清零(`grammar.is_pending_list_clear`)③维度表全绿(`grammar.is_dimension_table_green`)④授权申请标记为「是」(`grammar.parse_auth_marker == "yes"`)。前 3/4 条解析器全部现成(grammar.py lines 170-178 / 135-150 / 183-197);④的快照消费模式照 session.py lines 146-151:

```python
    # 轮次字段(仅 phase3/current_round 有 pending 计数,其余 0;plain 不计 D-P2-15)
    if state["state"] == STATE_PHASE3 and state["current_round"] is not None:
        ann = annotations_mod.load(project, state["current_round"])
        pending_count = len(annotations_mod.select_pending(ann))
    else:
        pending_count = 0
```

四条必须在**同一份当前轮文档快照**上判定(D-P3-1:读一次 `docs/discuss-round-{N}.md` 文本,N = derive_state 的 current_round,复用该文本跑 ②③④)。入口判定纯函数形态照 `round_process_available`(session.py lines 517-525):

```python
def round_process_available(project_path) -> bool:
    """入口判定(纯靠磁盘,防绕过):derive_state == phase3 且当前轮非空。

    ...
    """
    state = derive_state(Path(project_path))
    return state["state"] == STATE_PHASE3 and state["current_round"] is not None
```

g3_available 对应签名建议 `g3_available(project_path) -> dict`(返回 `{available: bool, reasons: [...]}` 供前端 title 与后端 409 消息共用;或纯 bool——planner 择简)。

**路由层消费:** POST /api/authorize 调 session 层封装(照 finalize_g1 in session.py lines 415-439 的"校验已进项目 + busy 拒绝 + 委托纯函数 + 返回新 derive_state"形态);成功返回 state=phase4(D-P3-4 两件套之二)。

**Deviations from analog (g1.py):**
- g1 重组磁盘既有内容(draft 追加标记行);g3 产物是后端纯生成(时间戳 + 确认词),除四查读当前轮文档外无 AI 输入面。
- g1 的 FileNotFoundError(缺前置)分支在 G3 不适用:四查不过 = 入口判定失败 → 409(非 400)。
- **AI 写 AUTHORIZATION.md 被拒是 CONTEX Specific Ideas 红线要求测试覆盖**——权限矩阵规则 1 已生效(ai_caller.py lines 60-66),新增 test_ai_caller.py 矩阵族断言即可(照既有矩阵用例形态)。

---

## Modified Files

### 2. `backend/prompts.py` — build_writing_prompt / build_check_prompt / build_repair_prompt (D-P3-7 / D-P3-13 / D-P3-14 / D-P3-29)

**What exists today — the exact mold:** `build_round_prompt`(lines 259-352,四段结构 + 三模块级常量 + {target_filename} 占位替换)。

**模块头 docstring 函数卡片先例** — 照 prompts.py lines 11-14(每个 build 函数在模块头有一张"卡片",新三函数照加):

```python
build_round_prompt(project_path, current_round) -> str(G2 / §4.4 / D-P2-11):
「处理本轮批注」的服务端提示词——资料段读全量 docs/(当前轮文档全文 +
当前轮 annotations 逐条 + transcript/draft),任务段注入 §3.3 四步 +
§6.3 五件套 + §6.4 文法模板逐字。
```

**文法模板逐字注入先例(D-P2-18 → D-P3-29 延续)** — `_GRAMMAR_EXAMPLES`(lines 210-232,元组逐行 + "切勿改列名"硬指令收尾):

```python
_GRAMMAR_EXAMPLES = (
    "批注回应表(二级标题含「批注回应」,表格列头逐字如下):",
    "",
    "| 批注id | 原文摘录 | 回应 |",
    "|---|---|---|",
    ...
    "切勿改列名、切勿改标记行格式——工具按此逐字解析,改动即解析失败。",
)
```

check 族对应新增 `_CHECK_GRAMMAR_EXAMPLES` 同构常量,报告文法三件逐字:
- 头部档位行:`> 自检档位:严格`(或宽松;与 tier 签名文件同字面,D-P3-12)
- 问题分级表头:`| 编号 | 级别 | 位置 | 问题 | 建议修法 |`(列名定案归 planner,Claude's Discretion 有建议列名)
- 末行结论行正例:`> 核查结论:FIX(P1×2 …)` / `> 核查结论:PASS`(`_CONCLUSION` 前缀与 state.PASS_PREFIX 同字面——复用 import,不复制第二份字符串,D-P2-16 同纪律)

repair 族另注入抛问协议(`> 待裁决:#K:<问题>` 输出形态,D-P3-18)与宽松档追加 PASS 指令。

**资料段拼装模式** — build_round_prompt lines 281-334 三小节(读盘 → is_file 检查 → OSError 容错 → "文件名标题 + 全文" Section,不存在/空给显式说明):

```python
    # ---- 资料段①:当前轮文档全文(半成品原文照读——重跑覆盖场景) ----
    current_doc_path = docs_dir / current_doc_name
    if current_doc_path.is_file():
        try:
            current_doc_text = current_doc_path.read_text(
                encoding="utf-8", errors="replace"
            )
        except OSError:
            current_doc_text = ""
```

三个新函数的资料段差异:
- **build_writing_prompt(project)**(D-P3-7):全部完整轮文档(`list_complete_rounds` 现成,循环注入全文)+ 全部 annotations 逐条(各轮 load 拼接,照 lines 300-316 的逐条格式)+ transcript/draft/brainstorm(`_KNOWN_DOCS` 循环,lines 318-334)。**资料段绝不读 DESIGN.md.tmp / AUTHORIZATION.md**(D-P3-9:半份 tmp 是被覆盖物,不入资料、不参考)。
- **build_check_prompt(project, check_n, tier)**(D-P3-13):DESIGN.md 全文 + 全部轮次文档 + 全部 annotations + **已有全部 DESIGN-check 报告**(严格档多轮趋势照读,§8.2"以磁盘文件为唯一输入"字面)。check_n 后端算好注入 prompt 防编错号(n = max_check_number + 1,照 lines 277-279 的 target 计算先例:`target_round = current_round + 1` 在函数体开头算好再格式化目标文件名)。
- **build_repair_prompt(project, check_n)**(D-P3-14):DESIGN.md 全文 + **最新一份(第 n 轮)核查报告全文**(问题清单 + 已落盘的用户裁决行天然在其中,D-P3-19 续跑语义)+ 其他既有报告 + 轮次文档/批注。

**任务段常量 + 落盘指令先例** — `_ROUND_INSTRUCTIONS`(lines 235-256,含 `{target_filename}` 占位)+ 替换模式(lines 337):

```python
    instructions = _ROUND_INSTRUCTIONS.replace("{target_filename}", target_filename)
```

三函数的落盘指令(全部逐字明示目标文件名,照 build_round_prompt 先例):
- writing:用 Write 工具写 `DESIGN.md.tmp`(项目根,整体覆盖式)后即结束;**绝不直接写 DESIGN.md 或 AUTHORIZATION.md**(权限门将拒绝——prompt 写明目的与格式)
- check:产出报告全文用 Write 写 `docs/DESIGN-check-{n}.md`;**核查执行者绝不修改 DESIGN.md——prompt 明禁**;报告末行写结论行(零问题 PASS)
- repair:按裁决逐条修复,**修订用 Write 整体写 `DESIGN.md.tmp` 后结束**(tmp 单次整体落盘纪律,§7.3②);属于用户职权的问题不得替用户决定——在输出里发 `> 待裁决:#K:` 行停下;宽松档特例:修复后在报告末追加 PASS 结论行(Write 整体重写含原内容 + 末行 PASS,或 Edit 追加——归 planner,落盘物必须仍是末行前缀合规)

**角色段差异**(每函数头部一句 + `_LANGUAGE_RULES` lines 29-33 注入,照 lines 340-343 接句先例):
- writing = "总设计文档撰写引擎"(覆盖七维度、吸收决策登记、不含未决问题)
- check = "干净的眼睛:独立核查引擎,无讨论立场,只依据磁盘文件"
- repair = 修复引擎,按报告与裁决逐条修

**WHERE:** 三个新函数放 `build_round_prompt` 之后;各自的任务段常量与文法常量照 `_ROUND_INSTRUCTIONS` / `_GRAMMAR_EXAMPLES` 的模块级常量先例放函数定义上方,分节注释照 lines 202-204 的 `# ---` 包裹形态,新起一轮次分节注释"阶段 4/5(G3 撰写与自检,idi-03)"。不修改既有三个 build 函数(extend-not-rewrite)。

### 3. `backend/session.py` — start_writing / start_check / start_repair + 入口判定 + snapshot 扩展 (D-P3-6 / D-P3-13 / D-P3-14 / D-P3-16 ~ D-P3-23 / D-P3-26)

**What exists today — the exact mold to copy ×3:** `process_round`(lines 528-629)。四段拆解引用:

**段 1:入口三查** — lines 550-565(照抄三遍,只换入口判定函数与延迟导入):

```python
    global _inflight, _ai_texts, _aborted
    from backend.grammar import parse_annotation_responses
    from backend.prompts import build_round_prompt

    with _lock:
        project = _current_project
        if project is None:
            raise RuntimeError("尚未进入任何项目(先调 enter_project)")
        if _inflight is not None and _inflight.is_set() is False:
            return False  # 在飞调用未结束:并发拒绝
        if not round_process_available(project):
            return False  # 非 phase3 或无完整轮:入口关闭(防绕过)
        caller = _ensure_caller()
        _inflight = threading.Event()  # set = 未结束
        _ai_texts = []
        _aborted = False
```

变体:
- `start_writing()` 换 `writing_available`(= derive_state == STATE_PHASE4;import STATE_PHASE4 照 line 31 的 STATE_PHASE3 import 形态加)
- `start_check()` 换 `check_available`(= phase5_awaiting_tier 或 phase5_checking 且判定式①不命中;check_n 取 max+1 首轮 / 重跑同轮半份覆盖——半份判定细节归 planner,D-P3-21)
- `start_repair()` 换 repair 入口(最新报告末行非 PASS + 判定式②或首启动,D-P3-14)

`_ai_texts` 需求按函数定:writing/check 不需要;**start_repair 保留 say 累积**(照 send_message lines 305-306 的 collect 形态)供 `> 待裁决:` 抛问扫描——D-P3-18:先扫 say 事件流、后扫最终文本,两者都扫。

**段 2:闭包外 state 捕获** — lines 567-569:

```python
    state = derive_state(project)
    prev_round = state["current_round"]
    prompt = build_round_prompt(project, prev_round)
```

对应:`prompt = build_writing_prompt(project)` / `build_check_prompt(project, check_n, tier)` / `build_repair_prompt(project, check_n)`。

**段 3:done 后端动作(else 分支——主战场)** — process_round lines 585-619 完整结构(else 在 try/except 之后、finally 之前;try 正常收流才执行):

```python
        else:
            # ---- done 后回写(prev_round 在线程外闭包捕获,build 前的值)----
            try:
                new_state = derive_state(project)
                new_round = new_state["current_round"]
                if new_round is not None and new_round > prev_round:
                    round_doc_path = (
                        project / "docs" / f"discuss-round-{new_round}.md"
                    )
                    try:
                        new_doc_text = round_doc_path.read_text(
                            encoding="utf-8", errors="replace"
                        )
                    except OSError:
                        new_doc_text = ""
                    responses = parse_annotation_responses(new_doc_text)
                    answers = {r["id"]: r["response"] for r in responses}
                    if answers:
                        hits = annotations_mod.writeback(
                            project, prev_round, answers
                        )
                        logger.info(
                            "G2 回写:第 %d 轮批注命中 %d 条(回应表 %d 条)",
                            prev_round, hits, len(responses),
                        )
            except Exception as exc:  # 回写失败:发 error 事件,不悬空进度
                _publish_for_tests(
                    {
                        "kind": "error",
                        "content": f"批注回写异常:{exc}",
                        "raw": None,
                    }
                )
```

三个 else 对应:
- **start_writing 的 else**(D-P3-8):derive_state 重拉 + 磁盘三判——有 AUTHORIZATION.md 且无 DESIGN.md 且 DESIGN.md.tmp 存在 → `tmp_path.replace(design_path)`(Path.replace / os.rename 同 inode 原子操作,覆盖语义)→ 改名成功 publish 完成 say;done 后 tmp 不存在(AI 没写)→ error 事件("撰写未产出 tmp,可重跑")不改名,状态留 phase4 可重跑。改名前**不**校验 tmp 内容完整性(D-P3-8:半份 tmp 是崩溃残留重跑场景,且 rename 原子保证不可能出现半份 DESIGN.md)。
- **start_check 的 else**(D-P3-16 循环驱动——纯逻辑,可提私有子函数便于单测):derive_state 重拉 → 读最新报告文本(`latest_check_content` 现成或 derive 后读 state["current_check"] 对应文件)→ ①末行 PASS 前缀(`grammar.is_pass_conclusion`)→ 结束,mission_complete 链(D-P3-24,前端拉新感知);②报告末行非 PASS → 解析问题分级表判**纯 P2**(全部级别 == "P2",零 P0/P1,D-P3-17):纯 P2 → 不自动修复,转 D-22 残余裁决呈现(snapshot 自组装 selfcheck 数据,用户逐条裁决);含 P0/P1 → **自动调修复跳**;③每跳结束拉磁盘判定下一步,不依赖内存传递(D-P3-16 字面)。
- **start_repair 的 else**(D-P3-14 / D-P3-18):扫描 `> 待裁决:` 前缀(say 累积 + 最终文本)——命中 → **立即暂停**:把问题行 `> 待裁决:#K:<问题>` 追加落盘到当轮核查报告末尾(读-改-写,幂等内容级——同内容已存在不重复追加)、不启动下一跳、不发继续修复;**核对不到该标记不得当作正常完成**(D-13 自愈兜底:识别失败停当前跳,报告无裁决行签名,判定式照旧行不误推进)。无标记 + 修复者已写 tmp → 照 writing 的改名分支原子落盘 → 自动调下一轮核查(check_n+1)。宽松档特例:唯一一轮修复后修复者已在报告末追加 PASS → mission_complete。

**段 4:finally 解锁** — lines 620-628(照抄,换 content 文案):

```python
        finally:
            # done 收尾事件:本流水线唯一一条 kind=done(回写动作不发第二条)
            _publish_for_tests({"kind": "done", "content": "本轮处理结束", "raw": None})
            with _lock:
                inflight_local = _inflight
            if inflight_local is not None:
                inflight_local.set()
```

**自动链条的单飞锁实现要点(必读,直接影响代码形态):** else 分支运行时 finally **尚未解锁**(`_inflight` 未 set)——若在 else 里直接调公共入口 `start_repair()`,会被自己的单飞检查(lines 558-559)拒绝。两个可行形态归 planner:
1. **内部 helper 直排(推荐)**:把"build prompt → caller.run → 事件流消费 → done 动作"提为私有 `_run_call(project, prompt, on_done)`;公共入口(start_check/start_repair)带三查 + 单飞后调它,else 分支续跳**直接调 helper 不再过单飞**(同一 worker 线程内串行,天然无并发);
2. else 分支判定下一跳后**先 `inflight_local.set()` 解锁再调公共入口**(锁内安全窗口:三查会通过)。
不得引入常驻 scheduler / 后台轮询(D-P3-16 字面;推荐 done-回调直排形态)。裁决卡 POST /api/checks/verdict 不起 AI 调用但同样写报告——同步追加(短临界区),防两个裁决并发写用同一 `_lock` 或 busy 校验(D-P3-26)。

**入口判定三函数(新,照 round_process_available 模子)** — session.py lines 517-525:

```python
def round_process_available(project_path) -> bool:
    """入口判定(纯靠磁盘,防绕过):derive_state == phase3 且当前轮非空。
    ...
    """
    state = derive_state(Path(project_path))
    return state["state"] == STATE_PHASE3 and state["current_round"] is not None
```

1. `writing_available(project)` = derive_state == STATE_PHASE4(有 AUTHORIZATION.md 无 DESIGN.md,state 行 4 现成)
2. `check_available(project)` = derive_state ∈ {phase5_awaiting_tier, phase5_checking} 且判定式①不命中(unpaired_verdicts 为空——判定式①是暂停态,「继续自检」不呈现)
3. `repair_available(project)` = 最新报告末行非 PASS 前缀 + 判定式②或首启动(存在配对问答行 + 无未配对 + 无更新编号报告 + 末行非 PASS)

三函数 docstring 照 lines 517-523 风格(中文语义 + DESIGN.md 章节 + "纯靠磁盘防绕过")。

**_session_snapshot 扩展** — 当前形态(lines 135-164,return dict 是 D-P3-23 的字段扩展点):

```python
    return {
        "state": state["state"],
        "current_round": state["current_round"],
        "current_check": state["current_check"],
        "rounds": list_complete_rounds(project / "docs"),
        "pending_annotations": pending_count,
        "transcript": parse_transcript(transcript_path),
        "draft": _read_text(project / DRAFT_FILENAME),
        "brainstorm": _read_text(project / BRAINSTORM_FILENAME),
        "divergence_available": divergence_available(project),
        "g1_available": g1_available(project),
    }
```

新增字段(不动既有键;插在 g1_available 之后):
- `g3_available: dict | bool`(phase3 分支加观察流量——照 lines 146-151 的 STATE_PHASE3 分支形态;四查照 New Files 1 的组合)
- `selfcheck` 子状态字段(D-P3-23;字段命名归 planner,Claude's Discretion):

```python
    "selfcheck": {
        "tier": None | "严格" | "宽松",
        "mode": "running" | "paused" | "resumed" | "done",
        "resume_available": bool,   # 「继续自检」意外中断恢复(非①②态)
        "repair_available": bool,   # 判定式② → 「继续修复」
        "unpaired": [...],          # 判定式①:待裁决问题(裁决卡数据)
        "p2_residue": [...],        # D-22 残余裁决卡:逐条 P2 问题
    }
```

组装逻辑(只认磁盘不缓存):STATE_PHASE5_AWAITING_TIER → tier 读签名文件(或 None);STATE_PHASE5_CHECKING → 读最新报告文本(`latest_check_content`)→ 跑新 parse_tier_line + **既有** unpaired_verdicts / is_pass_conclusion(判定式①②消费,D-P3-20)|纯 P2 残余判定(新问题表解析);STATE_MISSION_COMPLETE → mode "done"。**不新增 derive_state 状态值**(state.py 七常量已全量覆盖,D-P3-23)。

**verdict 落盘函数(新,同步)** — 照 answer_plain(lines 674-721)的"lock 取 project → busy 检查 → 入口校验 → 落盘"同步模子:

```python
    with _lock:
        project = _current_project
        caller = _ensure_caller()
    if project is None:
        raise RuntimeError("尚未进入任何项目(先调 enter_project)")
    if busy():
        raise RuntimeError("当前有调用进行中,请等它结束或先中止")
```

对应 `append_verdict(number, decision, note)`:读最新报告 → 组 `> 裁决:#K:<用户裁决文本>` 行 → 内容级幂等(同号已存在同内容裁决 → 拒绝重复 POST;§6.4)→ 追加落盘;**D-22 残余裁决收口检测**:全部残余问题已配对(配对数 == 问题数)→ 后端立即在最新报告末追加 PASS 结论行(后端动作非 AI,D-P3-17)→ derive_state 自动变 mission_complete。

### 4. `backend/grammar.py` — 报告头部档位行 + 问题分级表解析(纯增量) (D-P3-15)

**What exists today:** 六条文法已锁(§6.4 check-14 锁定版)——**禁改语义**;允许新增:①报告头部档位行解析 ②问题分级表解析。

**类比先例 1:三态解析** — `parse_auth_marker`(lines 183-197):

```python
def parse_auth_marker(md_text: str) -> str | None:
    """授权申请标记三态解析:"yes" / "no" / None。
    ...
    """
    last = last_nonempty_line(md_text)
    if last == AUTH_MARKER_YES:
        return "yes"
    if last == AUTH_MARKER_NO:
        return "no"
    return None
```

`parse_tier_line(md_text) -> str | None` 对应:`"严格"` / `"宽松"` / None。定位建议:扫首部以 `> 自检档位:` 开头的行(报告可能带 H1 标题,不假定首行);脏值/缺失 → None(畸形输入给确定判定不抛,照模块 docstring lines 22-23 纪律)。**tier 字符串字面建议进模块级常量**——py 与 prompts.py 的注入字面必须逐字一致(同一关键词纪律,或 prompts.py import grammar 常量——照 state/grammar 的常量复用先例,不复制第二份)。

**类比先例 2:关键词表格解析** — `parse_dimension_table`(lines 120-132)+ 共通 `_extract_table`(lines 73-109):

```python
def parse_dimension_table(md_text: str) -> list[dict]:
    """解析维度表为 [{"dimension", "status", "note"}] 行列表。

    列 = 维度/状态/说明(§6.4 字面);表头丢弃、各列 strip;无表返回 []。
    """
    rows = _extract_table(md_text, "覆盖维度表")
    result: list[dict] = []
    for columns in rows:
        dimension = columns[0] if len(columns) > 0 else ""
        status = columns[1] if len(columns) > 1 else ""
        note = columns[2] if len(columns) > 2 else ""
        result.append({"dimension": dimension, "status": status, "note": note})
    return result
```

`parse_problem_grades(md_text) -> list[dict]` 对应:`_extract_table(md_text, <与 prompt 注入一致的关键词>)` → `[{"number", "level", "location", "issue", "suggestion"}]`(列 = 编号/级别/位置/问题/建议修法)。纯 P2 判定 helper `is_pure_p2(md_text) -> bool` = 全部 level 恰为 "P2"(零 P0/P1,D-P3-17);空表 → False(零问题报告走 PASS 路径,不以纯 P2 处理——planner 按此语义)。

**__all__ 登记** — lines 37-47 数组同步扩(新函数照加)。

**Deviations / 硬约束:**
- 六条既有函数**只消费不改**(判定式①②是 check-14 锁定版,CONTEXT domain 铁律)。
- 表格关键词与 prompts.py 注入的文法字面**严格对齐**(prompt 模板、解析器、tier 签名文件三处同一字符串)。
- 新文法**必配构造正反例测试**(D-P3-29 字面,照 D-P2-17 先例——见 Modified Files 8.a)。
- 无磁盘 IO(纯文本函数,保持模块零 IO 纪律)。

### 5. `backend/main.py` — 八个新路由 (D-P3-27)

**What exists today:** 三类现成 route 模板:
- **受控产物写盘路由**(完整错误分支):`POST /api/g1` lines 194-215
- **202 受理路由**:`POST /api/rounds/process` lines 332-350(或 `/api/divergence` lines 163-181)
- **GET 组装路由**:`GET /api/rounds/{round_n}` lines 249-275 与 `GET /api/rounds` lines 233-246

八条新路由逐条对应(全部照既有错误分支形态:RuntimeError 消息关键字分流 409/400、FileNotFoundError→400、FileExistsError→409):

1. **`GET /api/design`** → 照 `GET /api/draft`(lines 137-144):`session.current_project_path()`(session.py lines 172-182 网关;未进入项目 → 照 lines 142-143 的 ok:null 形态或 400,planner 择一,GET /api/brainstorm lines 184-191 亦有 null 形态)→ 读 DESIGN.md 全文返回 `{"status": "ok", "design": content}`。
2. **`GET /api/checks`** → 照 `GET /api/rounds`(lines 233-246):check 报告编号列表 + 最新报告全文 + selfcheck 子状态字段(snapshot 已组装,透传即可);未进入项目 400。
3. **`POST /api/authorize`** → 照 `/api/g1`(lines 194-215)完整错误分支:四查/phase 不过 → 409、busy → 409、FileExistsError(已授权幂等)→ 409;成功返回新 derive_state(state=phase4)。
4. **`POST /api/writing`** → 照 `/api/rounds/process`(lines 332-350):session.start_writing() 三查,202 受理 / 409 / 400。
5. **`POST /api/checks/tier`** → 照 pydantic body + 白名单路由:body 类 `TierBody(BaseModel){ tier: str }`(照 lines 84-87 PlainBody 形态);白名单校验照 set_config lines 364-368(`("严格", "宽松")`,非法 400);写 tier 签名文件;phase5_awaiting_tier / 已有报告头部不一致 → 409;幂等:同档重选跳过。
6. **`POST /api/checks/start`** → 形态同 4:session.start_check(),202/409/400。
7. **`POST /api/checks/repair`** → 形态同 4:session.start_repair(),202/409/400。
8. **`POST /api/checks/verdict`** → **同步路由**(不起线程不调 AI,照 answer_plain 的 session 同步模子 + route 消费形态 lines 300-329):body `VerdictBody(BaseModel){ number: int, decision: str, note: str }`;session.append_verdict(...):busy → 409、同号重复 → 409、成功 200;后端收口(残余清零)时同次返回新 derive_state(mission_complete)供前端弹欢呼模态。

**pydantic Body 类位置:** TierBody / VerdictBody 追加在 PlainBody 之后(lines 84-87 后)。
**路由块位置:** 轮次路由族之后、"Plan 01 骨架路由"分节注释(lines 353-355)之前,新起分节注释块(照 lines 228-231 `# 轮次路由族(PLAN ...)` 形态,写 "阶段 4/5/归档路由族(PLAN idi-03-xx,D-P3-27)")。
**done 后前端拉链:** writing/check/repair 202 后,前端照既有 refresh 链(app.js lines 880-892)在 SSE done 收尾拉新 `/api/session` + `/api/design` + `/api/checks`;**不新增专用收尾事件**(D-P3-27,kind 面向 SSE 照旧)。

### 6-7. `frontend/app.js` + `frontend/index.html` + `frontend/style.css` — 阶段 4/5/完成态视图 + 确认词/档位/欢呼模态 (D-P3-3 / D-P3-11 / D-P3-24 ~ D-P3-26 / D-P3-28)

**What exists today — 挂点:** `applySessionGates` 的 phase4/5/mission_complete else 分支(app.js lines 260-280;**274-279 为占位文案 D-P3-28 指名的挂点**):

```javascript
  // 子视图切换:阶段 1-2 → draft-view;阶段 3+ → rounds-placeholder
  if (data.state === 'phase1_new' || data.state === 'phase12_in_progress') {
    draftView.classList.remove('hidden');
    roundsPlaceholder.classList.add('hidden');
    annotationsPanel.classList.add('hidden'); // 阶段 1-2 侧栏是会话流(D-P2-2)
  } else {
    draftView.classList.add('hidden');
    roundsPlaceholder.classList.remove('hidden');
    if (data.state === 'phase3' && data.current_round) {
      // phase3:真轮次视图(文档渲染 + 批注流侧栏 + 计数);D-P2-20
      currentRoundNumber = data.current_round;
      pendingCount.textContent = `本轮批注未处理 ${data.pending_annotations}`;
      annotationsPanel.classList.remove('hidden');
      loadRoundsView(data.current_round);
    } else {
      // phase4/5/mission_complete:占位文案维持现状(CODEX 边界裁决③,不触碰内容)
      annotationsPanel.classList.add('hidden');
      roundsHint.textContent = `当前状态:${STATE_LABELS[data.state] || data.state}(轮次阶段之后的视图在本工具后续版本呈现)。`;
      roundDoc.innerHTML = '';
    }
  }
```

**替换策略(D-P3-28):** 只改 else 分支内部(274-279),按 state 细分;phase1-3 分支零修改:
- `phase4` → 撰写按钮 + AI 面板照旧(按钮文案二态:无 tmp = "撰写总设计文档";有 tmp 无 DESIGN.md = "继续撰写(检测到上次中断的半成品,重写覆盖)",D-P3-10)
- `phase5_awaiting_tier` → 档位模态触发(D-P3-11:无 tier 文件且无 check 报告 → 弹;有报告 → 照头部行)
- `phase5_checking` → 报告视图 + 继续/裁决控件(selfcheck.mode 驱动按钮显隐,D-P3-20:①paused → 隐藏「继续自检」、呈现问题 + 输入框、**不呈现「继续修复」**;②resumed → 隐藏「继续自检」、**只呈现「继续修复」**;其余 running → 「继续自检」做中断恢复;D-22 p2_residue → 逐条裁决卡)
- `mission_complete` → 归档视图(DESIGN.md 默认渲染 + 全轮次切换器 + check 报告列表;划词菜单不绑——round-doc mouseup 的 `currentState !== 'phase3'` 防线已天然生效,D-P3-25)+ 一次性欢呼模态(D-P3-24:会话内存标记,不落盘;判定 = 本次会话首次见到 mission_complete)

**模态先例 ×2** — index.html permission-modal(lines 118-128)+ app.js showPermissionModal(lines 608-621):

```html
  <!-- 权限确认弹窗(AI-04:confirm 处置征求用户) -->
  <div id="permission-modal" class="overlay hidden">
    <div class="overlay-card">
      <h3>权限确认</h3>
      <p id="permission-message"></p>
      <div class="modal-buttons">
        <button id="btn-permission-allow" class="primary">同意</button>
        <button id="btn-permission-deny" class="danger">拒绝</button>
      </div>
    </div>
  </div>
```

```javascript
function showPermissionModal(event) {
  permissionMessage.textContent = event.summary || `AI 请求使用工具 ${event.tool}`;
  permissionModal.classList.remove('hidden');
  const respond = async (approved) => {
    permissionModal.classList.add('hidden');
    await fetch('/api/permission', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: event.id, approved }),
    }).catch(() => { /* 网络失败:后端 abort 时会强制释放 */ });
  };
  permissionAllowBtn.onclick = () => respond(true);
  permissionDenyBtn.onclick = () => respond(false);
}
```

- **确认词模态**(D-P3-3)照抄 overlay 结构 + 加 `<input type="text">`:放行按钮初始 disabled,`input` 事件里 `value.trim() === '确认授权'` 全等才 enable(前端完成校验,后端不重复解词——后端防线是"仅确认词通过瞬间写 AUTHORIZATION.md"的动作本身);任何其他输入/关闭/取消 = 拒绝路径 → 走 annotations 通道转普通批注(window.prompt 先例 app.js lines 756-767 的 note 收集;或模态内 textarea——planner 择简)
- **档位模态**(D-P3-11)同结构,两个选项按钮 + 各一句话说明(文案照 §8.2 口径,Claude's Discretion)
- **欢呼模态**(D-P3-24)一次性,overlay 结构照 cli-check-overlay(lines 136-143)

**XSS 管线** — renderMarkdown → stripUnsafeNodes(app.js lines 76-101),阶段 5 全新数据(check 报告 / DESIGN.md / 裁决问题文本——全部不可信 AI 输入)一律走此管线或 textContent,**零 innerHTML 拼接**(D-P3-28 = T-idi03-02 延续):

```javascript
function renderMarkdown(text) {
  if (!window.marked) return document.createTextNode(text || '');
  marked.setOptions({ mangle: false, headerIds: false });
  const html = marked.parse(String(text || ''));
  const tpl = document.createElement('template');
  tpl.innerHTML = html;
  stripUnsafeNodes(tpl.content);
  ...
}
```

报告/DESIGN 渲染照 renderRoundDocument(lines 451-455:清旧节点 + appendChild(renderMarkdown(text)));条目级 DOM 构建照 renderAnnotations(lines 521-577 的 createElement 模式)。

**「继续」按钮族点击 → POST → SSE → refresh 链** — 照 processRoundBtn handler(lines 840-878)完整模子:busy 防重复(disabled + inFlight 标记)→ renderEvent say 提示 → fetch POST(202 检查)→ 202 未受理恢复按钮(done 链不会来)→ 受理后保持禁用直至 SSE done。**done/error 收尾挂点**(dispatchEvent_ lines 131-148)已有 processInFlight 先例:

```javascript
    if (processInFlight) {
      processInFlight = false;
      processRoundBtn.textContent = '处理本轮批注';
      processRoundBtn.title = '仅阶段 3 当前轮可用';
      refreshRoundsAfterStream();
    }
```

新族照加 writingInFlight / checkInFlight 变量(或统一 Map——planner 择简);拉新链扩 `/api/design` + `/api/checks`(照 refreshRoundsAfterStream lines 884-892 的 fetch + applySessionGates 模式)。

**G3 按钮显隐** — 照 g1_available 按钮消费先例(applySessionGates lines 295-307):snapshot 新字段 g3_available → 授权按钮 hidden/disabled + title 三态;点击走确认词模态。

**index.html 新元素清单**(照 rounds-placeholder lines 53-62 与 annotations-panel lines 81-90 的 section 形态;全部新 id 照 `btn-`/`-panel`/`-modal` 既有命名):
- `#authorize-row`(G3「授权撰写总设计文档」按钮 + hint,挂 rounds-placeholder 内 phase3 视图底部——同 approve-row 在 draft-view 末尾的模式 lines 46-50)
- 三个模态:`#confirmation-modal`(确认词)/ `#tier-modal`(档位)/ `#mission-complete-modal`(欢呼)——overlay 结构照 permission-modal
- phase5 侧栏 `#checks-panel`(报告列表 + 继续按钮 + 裁决控件)——照 annotations-panel 的 section 结构形态
- mission_complete 归档视图:复用 rounds-placeholder 容器或新建 doc-subview(Claude's Discretion 已开放;原则 = 不重排阶段 1-3 已定版式、不新增路由)

**style.css 追加块** — 照 idi-02-03 末尾分节注释先例(style.css lines 360-362 的 `/* ===== */` 包裹格式),新起"阶段 4/5/归档视图"分节:
- G3 按钮样式照 `#btn-approve-draft`(lines 245-254:绿色系 + disabled opacity 0.55)
- 裁决卡 `.verdict-card` 照 `.annotation-item`(lines 405-435:卡片边框 + 徽标形态;含 location/issue/suggestion 文本 + 「修」/「接受现状」两按钮)
- 报告列表/档位模态选项样式照 `.overlay-card button`(lines 165-174)
- 归档只读灰化照 `#round-doc.round-frozen`(lines 491-495:opacity + saturate)

### 8. `backend/tests/` — 新测试族 (D-P3-30)

**What exists today — 测试基建(全部复用,本阶段不引入新基建):** FakeAICaller(test_session.py lines 29-77)、fresh_session fixture(lines 84-89)、wait_idle(lines 92-97)、RoundWritingFake(lines 744-762)、_round_doc_text(lines 719-741)、HangingFake + gate/release(lines 940-961)、_enter_phase3(lines 765-772)、route_env(test_route_session.py lines 23-29)、E2E IDI_E2E 门控(test_e2e_rounds.py:lines 65-66 门检查 + lines 69-75 造盘 + lines 115-124 wait_idle + lines 127-168 _EventRecorder + lines 276-289 无人值守 denier 线程 + lines 291-370 挂死重试门卫)。

**写盘 fake 模子** — RoundWritingFake(lines 744-762,阶段 4/5 的三个新 fake 同构):

```python
class RoundWritingFake(FakeAICaller):
    """AI 在调用中写盘新轮文档(Write 工具语义:整体覆盖)。
    ...
    """

    def __init__(self, events, content: str):
        super().__init__(events=events)
        self.content = content

    def run(self, project_path, prompt: str):
        self.run_calls.append((str(project_path), prompt))
        docs_dir = Path(project_path) / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)
        (docs_dir / "discuss-round-2.md").write_text(self.content, encoding="utf-8")
        for ev in list(self.events):
            yield dict(ev)
        yield {"kind": "done", "content": "调用结束", "raw": None}
```

对应:TmpWritingFake(写项目根 DESIGN.md.tmp)、CheckReportWritingFake(写 docs/DESIGN-check-{n}.md,报告文法内嵌)、RepairWritingFake(写 tmp;可注入 `> 待裁决:` say 事件)。

**新测试族分布:**

a) **test_grammar.py 增量** — parse_tier_line / parse_problem_grades / is_pure_p2 正反例族(照 test_grammar.py 现有 style:手造报告样本 helper + 用例分节注释)。反例必含:脏头部行、空报告、无表、双结论行(锚点取末一处)、非 P2 混级、空表 is_pure_p2=False。D-P3-29 字面要求:新文法必配构造正反例。

b) **test_session.py(或新 test_writing.py / test_check.py 同族)增量** — 照 process_round 六用例模式(尤其 test_process_round_writeback lines 849-888 的"受理 → wait_idle → 磁盘断言 → snapshot 断言"骨架):
   - start_writing:tmp 写盘 → done 后 tmp 改名 DESIGN.md、derive_state phase4→phase5_awaiting_tier;AI 不产 tmp → error 事件、状态留 phase4、重跑覆盖
   - start_check:纯 P0/P1 报告 → 自动续修复跳(fake 二连调);纯 P2 报告 → 不修复、p2_residue 进 snapshot;PASS 报告 → mission_complete;零报告/畸形 → error 不崩溃
   - start_repair:tmp 改名 → 自动下一轮核查(check_n+1);`> 待裁决:` say 事件 → 截存追加到报告、不续跳;verdict 落盘 → resumed;D-22 残余全部裁决 → 后端追加 PASS → mission_complete
   - 单飞互斥:三入口在飞互相拒绝 + verdict 与在飞 AI 调用互斥(HangingFake + gate/release,照 lines 936-961)
   - 入口判定:非 phase4/phase5 各 reject(照 test_process_round_non_phase3_rejects lines 964-973)
   - G3 四查 + 幂等:合规文档四查全过;各条不过的反例(pending 批注/维度 ◐/清单待决/标记"否");已授权再 POST → FileExistsError → 409

c) **test_route_session.py 增量** — route_env + 造盘 helper 模子:八路由全分支(authorize 四查不过 409 / tier 白名单 400 / verdict 同号重复 409 / checks 列表字段形状)

d) **test_e2e_*(新文件或增量)** — 照 test_e2e_rounds.py 全形态:IDI_E2E 门控 + mktemp 造真实 tmp 项目走 **part-of-G3 → PASS 全链**(造盘:完整轮 + 四查合规文档(维度全绿/清单清零/申请授权"是"/无 pending 批注)+ 手造 AUTHORIZATION.md → start_writing → tier POST → start_check 自动链 → mission_complete);真路线权限 denier 线程与挂死重试门卫复用先例。**不引入新测试基建**(D-P3-30):不新增 fixture、不引插件、FakeAICaller 原位扩展不迁移。基线:守住 "143 passed + 4 skipped" 只增不减。venv 纪律:SDK 用例必须在 `.venv/bin/python -m pytest` 下跑(系统 Python 无 claude_agent_sdk 时 4 个 SDK 归一化用例会失败——执行 agent 注意)。

e) **test_g1.py 同族新 g3 单测** — 四查组合、FileExistsError 幂等、授权时间/确认词两要素落盘;AI 写 AUTHORIZATION.md 被拒断言放 test_ai_caller.py 矩阵族(Specific Ideas 红线要求)。

---

## Shared Patterns

### 单飞锁 + 入口三查(全部新入口复用)
**Source:** `backend/session.py` lines 277-286(在飞检查)+ lines 517-525(纯磁盘入口判定)+ lines 550-565(入口三查模子)
**Apply to:** start_writing / start_check / start_repair 三函数全部照抄;verdict 同步函数(busy → 409 防双写竞态,D-P3-26)
[完整摘录见 Modified Files 3 段 1]

### 后台线程 + SSE 直播 + done 后端动作 + finally 解锁(process_round 模子)
**Source:** `backend/session.py` lines 528-629
**Apply to:** 三个 else 分支各接各的 done 动作(tmp 改名 / 循环驱动 / 待裁决截存);每跳结束重拉 derive_state 判定下一步,不依赖闭包内存传递(D-P3-16)
[完整摘录见 Modified Files 3 段 1-4;**自动链单飞锁要点必读**]

### FileExistsError 幂等防护(受控产物写盘)
**Source:** `backend/g1.py` lines 40-43 + `backend/main.py` lines 213-214
**Apply to:** AUTHORIZATION.md 写入(已授权 → 409)/ tier 签名重复选档 / verdict 同号重复 POST

```python
    if round_path.is_file():
        raise FileExistsError(
            f"已定稿({ROUND_1_FILENAME} 已存在)——G1 只走一次,项目已在轮次阶段"
        )
```

```python
    except FileExistsError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=409)
```

### 文件即状态 · derive_state 派生(一切按钮显隐的最终权威)
**Source:** `backend/state.py` lines 21-27(七常量,本阶段全量消费) + lines 95-147(八行推导表,行 4/5/6/7 lines 122-143)
**Apply to:** 全部新按钮(撰写/继续撰写/继续自检/继续修复/裁决卡)判定最终回落 derive_state + 报告文法;mission_complete 不新增归档标志——推导态即呈现,关闭动作 = 入口判定不满足(服务端 409 是防线,D-P3-25);**snapshot 的 selfcheck 子状态只是组装,不是新状态值**(D-P3-23)

### 判定式①②消费(禁改,check-14 锁定版)
**Source:** `backend/grammar.py` lines 234-245(is_pass_conclusion)+ lines 266-283(unpaired_verdicts)
**Apply to:** snapshot 的 selfcheck.mode 组装 / 继续按钮显隐(D-P3-20)/ start_repair 入口判定 / start_check else 推进决策
[代码见 grammar.py 原文,不在此重复——只消费不改]

### XSS 管线(阶段 5 新数据全走)
**Source:** `frontend/app.js` lines 76-101(renderMarkdown + stripUnsafeNodes)
**Apply to:** check 报告 / DESIGN.md / 裁决卡问题文本渲染(AI 产物不可信;renderMarkdown 或 textContent,零 innerHTML 拼接,D-P3-28)

### Prompt 四段结构 + 文法模板逐字注入(D-P2-18 → D-P3-29)
**Source:** `backend/prompts.py` lines 210-232(_GRAMMAR_EXAMPLES)+ lines 235-256(_ROUND_INSTRUCTIONS)+ lines 259-352(build_round_prompt)
**Apply to:** 三族新 build 函数;报告文法(头部档位行、问题分级表头、结论行、裁决追加形态)prompt 内逐字正例 + 切勿改列名硬指令;解析器关键词与 prompt 字面严格对齐;AI 产物不解析成功不修补——靠重跑覆盖(§7.3/D-13)

### done 后前端拉新链(不新增专用收尾事件)
**Source:** `frontend/app.js` lines 131-148(dispatchEvent_ done/error 收尾 + processInFlight 链)+ lines 884-892(refreshRoundsAfterStream)
**Apply to:** writing/check/repair 的 202 受理后,SSE done 收尾拉新 /api/session + /api/design + /api/checks;phase 切换(如 phase4→awaiting_tier)由 applySessionGates 的 else 分支重进相应视图

---

## No Analog Found

(none — 全部 11 文件有仓库内 analog。三个「新形态」能力各有最接近的仿写基础,不构成 no-analog 文件:
1. **确认词模态文本输入** — permission-modal 结构 + 字符串 strip 全等比较(无新依赖,输入不进渲染管线)
2. **严格档两跳自动循环** — process_round done-else 分支的直排扩展(无 scheduler;单飞锁要点见 Modified Files 3)
3. **D-22 逐条裁决卡** — annotation-item 条目卡片形态 + createElement 模式(纯 DOM)
以上三源在执行 plan 时引用既有代码即可,planner 无需外部 pattern 来源。)

## Metadata

**Analog search scope:** backend/(12 源文件)、backend/tests/(11)、frontend/(3)、.planning/phases/idi-01-1-2/ 与 idi-02-g2/(模子与验证命令先例)、DESIGN.md §4.4/§5.4/§6.1/§6.4/§7.3/§7.4/§8.1/§8.2(协议权威)
**Files scanned:** 26 tracked source files + 3 planning artifacts(直接 Read 校验行号:session.py 722 行 / g1.py 52 / state.py 165 / main.py 454 / prompts.py 353 / grammar.py 284 / annotations.py 207 / app.js 1058 / index.html 153 / style.css 496 / test_session.py ~1090 / test_e2e_rounds.py 446)
**Pattern extraction date:** 2026-09-10
**Git-tracked check:** all analog paths confirmed tracked(`git ls-files backend/ frontend/` 输出与引用文件一一对应;无 .gsd/capabilities 镜像路径参与)

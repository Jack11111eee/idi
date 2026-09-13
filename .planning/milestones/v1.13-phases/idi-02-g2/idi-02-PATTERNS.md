# Phase 2 Pattern Map

**Phase:** idi-02 (轮次收敛循环——划词批注、G2 与机器文法)
**Mapped:** 2026-09-09
**Files classified:** 8 (+2 test files = 10)
**Analogs found:** 10 / 10(every file has an in-repo analog; zero "no analog" files)

All excerpt line numbers below refer to the current git-tracked source under `backend/` and `frontend/`. All analog paths are git-tracked (verified via `git ls-files`). DESIGN.md symbols: **§6.2** (annotations JSON contract), **§6.3** (五件套), **§6.4** (six grammar rules), **§7.4** (derive_state).

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `backend/annotations.py` (NEW) | model/storage (pure) | file-I/O | `backend/transcript.py` | exact role+flow |
| `backend/grammar.py` (NEW) | utility (pure parser) | transform | `backend/state.py` | exact role+flow |
| `backend/tests/test_annotations.py` (NEW) | test | file-I/O | `backend/tests/test_transcript.py` | exact |
| `backend/tests/test_grammar.py` (NEW) | test | transform | `backend/tests/test_state.py` | exact |
| `backend/ai_caller.py` (MOD) | provider | request-response | self (run 双路线先例) | extend |
| `backend/prompts.py` (MOD) | utility | transform | self (`build_phase12_prompt`) | extend |
| `backend/session.py` (MOD) | service | event-driven/background | self (`trigger_divergence`) | extend |
| `backend/main.py` (MOD) | route/controller | request-response | self (`/api/g1`, `/api/divergence`) | extend |
| `frontend/app.js` / `index.html` / `style.css` (MOD) | component | request-response + SSE | self (`applySessionGates` / permission modal) | extend |
| `backend/tests/test_session.py` (MOD) | test | event-driven | self (`FakeAICaller`) | extend |

---

## New Files

### 1. `backend/annotations.py` — annotations 纯存储模块 (D-P2-5, D-P2-6, DATA-01)

**Role:** 纯 pathlib 模块,零 FastAPI/零 AI 依赖(与 state.py / transcript.py / g1.py 同级同风格)。
**Data Flow:** file-I/O,无状态,"文件即状态"。
**Closest analog:** `backend/transcript.py`(parse/append + 不存在返回空形态 + 父目录自举);次级 analog `backend/g1.py`(后端受控写产物)。

**模块头模式** — 照 `backend/transcript.py` lines 1-17:

```python
# -*- coding: utf-8 -*-
"""transcript.md 的 parse / append 读写函数——DESIGN.md §6.1 文法。
...
零第三方依赖、纯 pathlib 无状态。
"""
from __future__ import annotations

import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)
```

注:annotaions 是 JSON 不是 md,故补 `import json`(仍是标准库,零第三方)。

**"不存在返回空形态"模式** — 文件不存在 → 空结构而非异常,照 `transcript.py` lines 34-39:

```python
    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:  # 读不到(权限/竞态)→ 按无转录处理
        logger.warning("读取 %s 失败,按空转录处理: %s", path, exc)
        return []
```

annotations.py 的对应:<br>
`if not path.is_file(): return {"round": N, "items": []}`(空形态带 round 号,依据 §6.2 顶层结构);JSON 解析失败(`json.JSONDecodeError`)同样 warning + 返回空形态,不抛(AI 写乱轮次文档时 annotations 不被连带污染,D-P2-5)。JSON 写盘用 `json.dumps(obj, ensure_ascii=False, indent=2)`,读用 `path.read_text(encoding="utf-8")`。

**父目录自举模式** — 照 `transcript.py` lines 81-84:

```python
    # 父目录不存在则建(新讨论的第一条消息:docs/ 尚未建立)
    parent = path.parent
    if not parent.is_dir():
        parent.mkdir(parents=True, exist_ok=True)
```

annotations 落盘(append_item / writeback)每次都先做这一步——新轮的第一条批注到来时 `docs/` 已存在,但防御性 mkdir 与 transcript 同风格。

**文件名形态** — 照 `state.py` lines 38-42 的编号named 模板常量:

```python
_ROUND_RE = re.compile(r"^discuss-round-(\d+)\.md$")
_ROUND_TEMPLATE = "discuss-round-{n}.md"
```

annotations.py 对应 `ANNOTATIONS_TEMPLATE = "discuss-round-{n}.annotations.json"`(§6.1 / §6.2 字面)。函数边界建议(planner 可调):`load_annotations(project_path, round_n) -> dict`、`append_item(project_path, round_n, *, quote, before, type, note, status, answer, created_at) -> dict`(内部生成 `id = f"a{round_n}-{seq:02d}"`,seq = 现有 items 长度 + 1)、`writeback(project_path, round_n, answers: dict[str, str]) -> int`(批量回写 answer 与 status pending→answered,返回命中数;未在回应表出现的 id 保持 pending,D-P2-13)。

**quote+before 定位纯函数** — 前端与后端共用语义的配对函数,签名建议 `locate_quote(full_text: str, quote: str, before: str) -> int | None`(返回匹配起点;精确匹配,多个匹配时优先"前文以 before 结尾"的那一处,否则第一处;无匹配 None)。这是纯字符串函数,不落盘——单测直接 string-in/position-out,照 `state.py` `last_nonempty_line` 的纯函数形态(state.py lines 45-52)。

**id 方案校验**(D-P2-5):`aN-NN`(如 `a3-01`),N=轮次,NN=该轮条目递增序号——与 DESIGN.md §6.2 示例 `"id": "a3-01"` 同构。

**Deviations from analog (transcript.py):**
- transcript 是 append-only 文本;annotations 建条目(append)与批量回答(writeback,重写整文件)两种写路径。writeback 需"读全量 → 改字段 → 整体重写"(json 文件无法追加写),这更像 `g1.finalize_g1` 的"后端动作改写文档"语义——照 g1.py lines 45-51 的"读-改-写"形态:

```python
    draft_text = draft_path.read_text(encoding="utf-8", errors="replace")
    finalized = f"{draft_text.rstrip()}\n\n{AUTH_MARKER_NO}\n"
    round_path.parent.mkdir(parents=True, exist_ok=True)  # docs/ 理论上已存在(draft 在其中),防御
    round_path.write_text(finalized, encoding="utf-8")
```

- 字段集一字不差:`/quote/before/type/note/status/answer/created_at` + 顶层 `round`(ISEDIGN.md §6.2 JSON 字面),不用 pydantic 存盘。
- 不删条目:answered 条目留在 items(§4.2"变灰但不删除")。

---

### 2. `backend/grammar.py` — §6.4 机器文法解析器 (D-P2-16 ~ D-P2-19, FLOW-07)

**Role:** 纯解析 utility,零依赖,与 state.py 同级。
**Data Flow:** transform(文本 in → 判定/结构化 out)。
**Closest analog:** `backend/state.py`。**硬要求:复用 state.py 常量,不重复实现两套**(CONTEXT D-P2-16 原文)。

**必复用的 state.py 既有资产**(lines 29-52)——直接 `from backend.state import AUTH_MARKER_YES, AUTH_MARKER_NO, PASS_PREFIX, last_nonempty_line`:

```python
# §6.4 授权申请标记:恰为这两个字符串之一(exact match after strip——前缀不算,后缀不算)
AUTH_MARKER_YES = "> 申请授权:是"
AUTH_MARKER_NO = "> 申请授权:否"
_AUTH_MARKERS = (AUTH_MARKER_YES, AUTH_MARKER_NO)

# §7.4 PASS 结论行:前缀匹配(其后可附括注,如 "> 核查结论:PASS(问题 N 项修复完毕)")
PASS_PREFIX = "> 核查结论:PASS"

def last_nonempty_line(md_text: str) -> str | None:
    """返回文档最后一个非空行(行 strip 后取末一个非空);全空返回 None。"""
    last: str | None = None
    for line in md_text.splitlines():
        stripped = line.strip()
        if stripped:
            last = stripped
    return last
```

授权标记判定照 `is_complete_round`(state.py lines 55-58)的语义(末非空行 strip 全等):

```python
def is_complete_round(md_text: str) -> bool:
    """§7.3 完整轮判据 + §6.4 授权申请标记:最后一个非空行恰为合规标记(exact,strip 后全等)。"""
    last = last_nonempty_line(md_text)
    return last in _AUTH_MARKERS
```

grammar.py 的授权申请标记解析 = 同语义(glue:复用或 re-export,planner 择一;决策已定"迁移或复用,不重复实现两套")。

**模块头(docstring 判定式自上而下先例)** — 照 state.py lines 1-11:

```python
# -*- coding: utf-8 -*-
"""derive_state(project_path) 纯函数——DESIGN.md v1.13 §7.4 八行推导表的完整实现。

「文件即状态」(D-19/D-P1-11):工具不维护独立流程状态,一切由磁盘现状推导。
...
零第三方依赖、零全局状态:纯 pathlib + 标准库,不碰 FastAPI 层。
"""
```

**正则形态先例** — state.py lines 38-39 的文件名正则带编号有界防护:

```python
_ROUND_RE = re.compile(r"^discuss-round-(\d+)\.md$")
_CHECK_RE = re.compile(r"^DESIGN-check-(\d+)\.md$")
```

grammar.py 的二维表/清单解析建议同风格预编译正则,例如裁决行形态(D-P2-16):`_VERDICT_RE = re.compile(r"^>\s*(待裁决|裁决):#(\d+):")`(strip 后匹配;§6.4 原文形态 `> (待裁决|裁决):#数字:`;同号即配对,锚点 = 最后一处 `> 核查结论:` 行)。

**表格解析思路**(六条文法共用):`for line in md_text.splitlines()` 扫描,定位二级标题行(`line.startswith("## ")` 且标题含关键词「覆盖维度表」/「未决问题清单」/「批注回应」),其后连续以 `|` 开头的行即表格行,第一行表头、其余数据行按 `|` split 后 strip 各列。每条解析器返回结构化结果 + 判定函数(全绿/清零/matching ids),照 state.py "解析函数与判定函数分离"的风格(`list_complete_rounds` 解析、`is_complete_round` 判定)。

**六条覆盖**(逐字对应 DESIGN.md §6.4 表 + PASS/裁决段):
1. 维度表:二级标题含「覆盖维度表」;列 = 维度/状态/说明;状态 ∈ {✓, ◐, ✗};全绿 ⇔ 无 ◐ 与 ✗
2. 未决清单:二级标题含「未决问题清单」;列 = 编号/问题/状态;状态 ∈ {待决, 已决};清零 ⇔ 无待决
3. 授权申请标记:末非空行 strip 后恰为两串之一(复用 state 常量)
4. 批注回应表:二级标题含「批注回应」;列 = 批注id/原文摘录/回应;供 D-P2-12 回写配对
5. PASS 结论行:末非空行前缀匹配 `PASS_PREFIX`(复用);结论行锚点取最后一处 `> 核查结论:` 行
6. 裁决追加行:`> (待裁决|裁决):#K:` 形态;仅统计结论行之后;同号配对(D-P2-16 原文)

**Deviations from analog (state.py):**
- state.py 判定的是磁盘目录形态(传 project_path);grammar.py 的六条解析全是**文本级纯函数**(传 md_text 字符串)——除批注回应表回写场景外无磁盘 IO。这使得 grammar.py 比 state.py 更纯。
- 5/6 两条(PASS 行 + 裁决行)本阶段只做**解析判定**,消费场景(报告按钮逻辑)在 Phase 3(CONTEXT `domain` 边界裁决①)。
- 不解析历史文档(D-P2-19):不要求兼容本项目自身 discuss-round-0~4(如 round-1 清单状态列是"待批注"不是"待决")——单测正例全部手造合规样本。

---

### 3. `backend/tests/test_annotations.py`(NEW)

**Closest analog:** `backend/tests/test_transcript.py`。
**Pattern to copy:** 模块头 docstring 列文法 → `tmp_path` 直接写盘 → 逐 case 命名行为。文件头(test_transcript.py lines 1-15):

```python
# -*- coding: utf-8 -*-
"""transcript.md 文法(DESIGN.md §6.1)单元测试:parse 与 append。
...
"""
from pathlib import Path

import pytest

from backend.transcript import (
    append_message,
    parse_transcript,
    transcript_exists,
)
```

目录自举 helper 先例(test_transcript.py lines 21-24):

```python
def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
```

必覆盖用例(照 test_transcript 的"基础解析/多行体/追加/空文件/边界反例"编排骨架):不存在的 annotations 文件 → 空形态;建条目(字段齐全 + id 递增 a3-01 → a3-02);writeback 命中 id 回写 answer + status=answered、未命中 id 保持 pending;quote+before 定位(唯一命中/多命中取 before 辅助/无命中 None);JSON 脏文件容错返回空形态。

### 4. `backend/tests/test_grammar.py`(NEW)

**Closest analog:** `backend/tests/test_state.py`。
**Pattern to copy:** 正反例编排骨架 + 手造文档样本 helper(test_state.py lines 21-33):

```python
def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def valid_round_text(marker: str = AUTH_NO) -> str:
    return f"# 第 N 轮讨论\n\n正文……\n\n{marker}\n"
```

条目用 `# ---------- 用例 N(行 N):形态描述 ----------` 分节注释;直接函数级断言先例(test_state.py lines 183-197):

```python
def test_is_complete_round_exact_match_no_prefix_suffix_tolerance():
    # 前缀不算、后缀不算——exact match after strip
    assert is_complete_round(f"{AUTH_NO}\n") is True
    assert is_complete_round(f"> 申请授权:是的\n") is False  # 后缀不算
    assert is_complete_round(f"前缀 {AUTH_NO}\n") is False  # 前缀不算
```

正反例矩阵(D-P2-17 原文,ROADMAP 成功判据 6):维度表全绿/非全绿(◐/✗)、清单清零/有"待决"、标记"是/否/脏变体(前后缀、空格、末行之后空行)"、回应表 id 配对(命中/未命中/多余 id)、结论行锚点取**最后一处**双结论行样本、裁决同号配对与未配对、PASS 前缀带括注(`> 核查结论:PASS(问题 N 项修复完毕)`)。

---

## Modified Files

### 5. `backend/ai_caller.py` — ask_lite 双路线实现 (D-P2-8)

**What exists today:** 基类签名已预定义(lines 218-227),当前 `raise NotImplementedError`:

```python
    @abstractmethod
    def run(self, project_path, prompt: str) -> Iterator[dict]:
        """在 project_path 目录上执行一次无头调用,逐条产出统一事件。"""

    def ask_lite(self, document_text: str, quoted_text: str, question: str) -> dict:
        """大白话轻量调用(§3.4,Phase 2 的 UI-02 实现)。

        只定义签名不实现逻辑(D-P1-6)——避免 Phase 2 改接口。
        """
        raise NotImplementedError("ask_lite 将在 Phase 2 实现(D-P1-6 接口预定义)")
```

**Where the new code goes:** 基类保留此 docstring/签名(或改为统一的轻量 prompt 组装说明);`SdkAICaller` 与 `SubprocessAICaller` 各自 override `ask_lite`。返回 dict 含 `answer` 文本键(同一契约,两路线一致,D-P2-8)。

**SubprocessAICaller 实现模式** — 复用现有 `run()` 的子进程骨架但**禁工具、非流式**。最小实现照 run() lines 313-332 的 Popen 形态裁剪:去 **input-format stream-json**(改单向 `-p prompt`),去 `--permission-prompt-tool stdio`(不起 control_request 回环),保留 `--setting-sources=`(屏蔽全局 allow 规则——两路线同因,line 243-245 docstring 语)与 `--append-system-prompt`(§3.8 红线 + "只解释,不改设计",D-P2-9):

```python
        argv = [
            self._cli_path,
            "-p",
            "--input-format", "stream-json",
            "--output-format", "stream-json",
            "--verbose",
            "--permission-prompt-tool", "stdio",
            "--setting-sources=",
            "--append-system-prompt",
            build_system_prompt(),
        ]
```

简单版:`subprocess.run([cli, "-p", lite_prompt, "--setting-sources=", "--append-system-prompt", ...], capture_output=True, text=True, cwd=project)` + 复用 `normalize_stream_line`/result 行逻辑取最终 answer。可参考 `normalize_stream_line` 里 result 行解析(ai_caller.py lines 182-187):

```python
    if msg_type == "result":
        # CLI 收尾行 → done(is_error 时 error;content = 最终结果文本)
        is_error = bool(obj.get("is_error"))
        kind = "error" if is_error else "done"
        content = str(obj.get("result") or ("调用结束" if not is_error else "调用出错"))
        return {"kind": kind, "content": content, "raw": obj}
```

**SdkAICaller 实现模式** — 照 `_build_options`(lines 506-552)建 `ClaudeAgentOptions` 但 `can_use_tool` 一律 False(disallow tools:纯问答,无文件读写,D-P2-8)、`setting_sources=[]`;调用走 `asyncio.run(...)` 包同步(照 run() lines 597-610 的 `asyncio.run(_consume())` 形态),收 `ResultMessage.result` 为 answer。

**ask_lite prompt** 建议进 `prompts.py`(见下),ai_caller 只组装调用——但注意 ask_lite 文件签名不收 project_path;document_text/quoted_text 由调用方(session)传入。**ask_lite 不产 SSE 直播事件**(D-P2-8:事件不进工作面板,不代表用户主动任务)。
**Integration point:** session 层同步调 `caller.ask_lite(...)`(D-P2-10),回写落盘走 backend(D-P2-7)。

### 6. `backend/prompts.py` — build_round_prompt (D-P2-11, D-P2-18)

**What exists today:** `_LANGUAGE_RULES` 常量(lines 21-25)与四段结构先例 `build_phase12_prompt`(lines 104-157):

```python
_LANGUAGE_RULES = (
    "语言红线:输出必须简洁、精准,不用晦涩词语。但解释必须清晰、完整——简洁不等于省略,"
    "不许因追求简短而含糊带过。未定义的术语不用;必须用术语时,先用一句大白话定义。"
    "一次讲一个小点,讲透。面向单人开发者读者,讨论文档以中文为主。"
)
```

```python
def build_phase12_prompt(project_path, user_message: str) -> str:
    """拼装阶段 1-2 的完整调用提示词(§5.1:磁盘现状 + 本次消息,四段结构)。"""
    project = Path(project_path)
    docs_dir = project / "docs"

    # ---- 资料段:docs/ 下已知文档逐个注入(文件名标题 + 全文) ----
    doc_sections: list[str] = []
    for name in _KNOWN_DOCS:
        path = docs_dir / name
        if path.is_file():
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                text = ""
```

返回段结构(lines 145-157)= "一、你的角色" + `_LANGUAGE_RULES` + "二、项目资料" + "三、本次任务" + "四、用户消息"。

**Where the new code goes:** 新增模块级任务段常量(照 `_PHASE12_INSTRUCTIONS` / `_DIVERGENCE_PERSPECTIVES` 的括号元组常量风格,lines 31-44)+ 新函数 `build_round_prompt(project_path) -> str` 放在 `build_divergence_prompt` 之后。签名建议 `build_round_prompt(project_path, current_round: int) -> str`——当前轮号由调用方传入(session 已从 derive_state 拿到)。

**资料段差异**(D-P2-11):读全量 docs/——当前轮文档全文(`discuss-round-{N}.md`,is_complete_round 不过时的原始文本也照读,半成品重跑场景)+ 当前轮全部 annotations(逐条 `id: … quote: … note: …` 行,直接消费 annotations.load)+ transcript/draft(照 `_KNOWN_DOCS` 循环注入既有形态)。annotations 无条目也要显式说明("当前轮暂无待处理批注",与 §3.3 空批注轮合法呼应,D-P2-15)。

**任务段注入**(D-P2-11/D-P2-18):§3.3 四步原文 + §6.3 五件套(批注回应表/决策登记/维度表/未决清单/授权申请标记)+ §6.4 文法模板**逐字**贴入(维度表表头 `| 维度 | 状态 | 说明 |`、清单表头 `| 编号 | 问题 | 状态 |`、回应表头 `| 批注id | 原文摘录 | 回应 |`、标记行 `> 申请授权:是|否`,并给"切勿改列名/标记行"硬指令);结果文件名 `docs/discuss-round-(N+1).md` 明示(权限门规则 3 已放行,零改动)。
**Integration point:** session.process_round() 内组装,替代 build_phase12_prompt 的角色;不修改既有两个 build 函数。

### 7. `backend/session.py` — process_round() + ask_lite 封装 + 快照扩展 (D-P2-10, D-P2-14, D-P2-15)

**What exists today — the exact mold to copy:** `trigger_divergence`(lines 434-484):

```python
def trigger_divergence() -> bool:
    """触发发散:走既有 AI 调用链(build_divergence_prompt → caller.run,事件照常出 SSE)。

    入口校验(防绕过):divergence_available(current_project) 为 True 才受理,
    否则返回 False(路由层转 4xx)。并发限制沿用会话锁(在飞中再触发 → False)。
    ...
    """
    global _inflight, _ai_texts, _aborted
    with _lock:
        project = _current_project
        if project is None:
            raise RuntimeError("尚未进入任何项目(先调 enter_project)")
        if _inflight is not None and _inflight.is_set() is False:
            return False  # 在飞调用未结束:并发拒绝
        if not divergence_available(project):
            return False  # 雏形已存在/已定稿:发散入口关闭(防绕过)
        caller = _ensure_caller()
        _inflight = threading.Event()  # set = 未结束
        _ai_texts = []
        _aborted = False

    prompt = build_divergence_prompt(project)

    def _worker():
        global _aborted
        try:
            _wire_permission_callback(caller)
            for event in caller.run(project, prompt):
                if _aborted:
                    break
                if event.get("kind") == "say":
                    _ai_texts.append(event.get("content", ""))
                _publish_for_tests(event)
                if event.get("kind") == "done":
                    break
        except Exception as exc:  # 线程内兜底:流不悬空
            _publish_for_tests(
                {"kind": "error", "content": f"调用线程异常:{exc}", "raw": None}
            )
        finally:
            _publish_for_tests({"kind": "done", "content": "发散结束", "raw": None})
            with _lock:
                inflight_local = _inflight
            if inflight_local is not None:
                inflight_local.set()

    threading.Thread(target=_worker, daemon=True).start()
    return True
```

**process_round() 模子**:同结构照抄。入口判定 `round_process_available(project)`(照 `divergence_available`/`g1_available` 的"纯靠磁盘"先例,lines 377-387 与 420-431):

```python
def divergence_available(project_path) -> bool:
    """入口判定(纯靠磁盘):无 draft.md 且无完整轮 → True(发散开放)。"""
    project = Path(project_path)
    if (project / DRAFT_FILENAME).is_file():
        return False
    if list_complete_rounds(project / "docs"):
        return False
    return True
```

G2 对应:`derive_state(project) == STATE_PHASE3`(from backend.state,session.py 已 import derive_state,line 30)且 `current_round is not None` → True。差异(vs trigger_divergence):
- prompt 源 = `build_round_prompt(project, current_round)`(planner:import 进顶部 line 29 的既有 prompts import 行,不新增 import 块结构)。
- **finally 段加 done 后回写动作**(D-P2-12):①derive_state 重拉(新轮出现 = 下一轮文档存在);②若 current_round 前进:用 grammar.py 的批注回应表解析器解析新轮文档 → `annotations.writeback(project, prev_round, answers)`(仅命中表中的 id;未命中保持 pending);③不依赖 AI 自觉(D-P2-13)——responding table 缺失/AI 格式不合规 → is_complete_round 判半成品 → derive_state 仍回原轮,process_round 可重跑(现有自愈语义,零新分支)。
- 事件照常 SSE 直播(工作面板全程可见,§5.2)+ done 收尾照旧;不落 transcript(同 divergence 先例,line 43-44 docstring)。_ai_texts 不需要(G2 无 say 落盘需求)——保持 worker 情况按 planner 判断,最终 done 事件照常。

**ask_lite 同步封装**(D-P2-10):新函数如 `answer_plain(document_text, quoted_text, question) -> dict`(同步,不走后台线程,worker 语义不需要):单飞锁照 busy()(lines 364-367):

```python
def busy() -> bool:
    """当前是否有在飞调用(路由层 409 判据)。"""
    with _lock:
        return _inflight is not None and not _inflight.is_set()
```

进行中再发起 → 拒绝(False/RuntimeError,planner 按路由层既有 409 风格统一)。

**_session_snapshot 扩展**(CONTEXT Integration Points):`_session_snapshot()`(lines 134-152)currently:

```python
    state = derive_state(project)
    transcript_path = project / TRANSCRIPT_FILENAME
    return {
        "state": state["state"],
        "current_round": state["current_round"],
        "current_check": state["current_check"],
        "transcript": parse_transcript(transcript_path),
        "draft": _read_text(project / DRAFT_FILENAME),
        "brainstorm": _read_text(project / BRAINSTORM_FILENAME),
        "divergence_available": divergence_available(project),
        "g1_available": g1_available(project),
    }
```

新增轮次字段(rounds 列表:来自 list_complete_rounds(dataset 来源相同)→ 前端渲染轮次切换器 D-P2-20;当前轮 annotations 计数:loaded → count type=comment 且 status=pending,D-P2-15)。
**Integration point:** process_round / answer_plain 放 trigger_divergence 之后同区;rounds 字段插在 current_check 之后(不做字段重命名)。

### 8. `backend/main.py` — 轮次路由族 (D-P2-22)

**What exists today:** 路由模板先例 POST /api/g1(lines 182-203,覆盖 FileNotFound→400 / FileExists→409 / RuntimeError 在飞→409 完整错误分支):

```python
@app.post("/api/g1")
def finalize_g1() -> JSONResponse:
    """G1 认可雏形(FLOW-03 / §4.4):后端定稿 draft.md → docs/discuss-round-1.md。
    ...
    """
    try:
        result = session.finalize_g1()
    except RuntimeError as exc:
        message = str(exc)
        if "在飞" in message or "进行中" in message:
            return JSONResponse(
                {"status": "error", "message": message}, status_code=409
            )
        return JSONResponse({"status": "error", "message": message}, status_code=400)
    except FileNotFoundError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=400)
    except FileExistsError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=409)
    return JSONResponse({"status": "ok", **result})
```

202 受理 + 未受理 409 先例 POST /api/divergence(lines 151-169):

```python
    try:
        accepted = session.trigger_divergence()
    except RuntimeError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=400)
    if not accepted:
        return JSONResponse(
            {
                "status": "error",
                "message": "发散入口已关闭(雏形已存在或已定稿)或当前有调用进行中",
            },
            status_code=409,
        )
    return JSONResponse({"status": "accepted"}, status_code=202)
```

**Pydantic 请求体**先例(lines 65-75,可选批注路由用):

```python
class EnterBody(BaseModel):
    path: str

class MessageBody(BaseModel):
    text: str
```

**Where the new code goes:** 新路由块放 get_transcript(lines 206-213)之后、"Plan 01 骨架路由"分节之前(保持现有分节注释);新 pydantic 模型(AnnotationBody / PlainBody)追加在 PermissionBody 之后。五个路由:

1. `GET /api/rounds`(轮次列表 + 当前轮号——session snapshot 已有的 rounds 字段)→ JSONResponse 形态,RuntimeError→400
2. `GET /api/rounds/{n}`(单轮文档 + annotations 合并视图;非完整轮 404)→ 对应 file get 形态(参考 get_draft lines 125-132 的"失败返回 ok:null"模式,但本路由 404 更贴语义,planner 择一)
3. `POST /api/rounds/{n}/annotations`(注解建条目:非当前轮 / 非 phase3 → 409;busy → 409)→ 照 409 分支先例
4. `POST /api/rounds/{n}/plain`(同步 ask_lite + 落盘 plain 条目;返回 answer)→ 错误分支含 busy 409 同上
5. `POST /api/rounds/process`(triggers session.process_round,202)
**Integration point:** 前端 done 后会拉新(G-idi01-7 修复先例)——refresh 流沿用既有 GET /api/session + 新 GET /api/rounds。

### 9. `frontend/index.html` + `frontend/app.js` + `frontend/style.css` (D-P2-1~4, D-P2-20~23)

**What exists today — rounds-placeholder(被替换物)** index.html lines 53-57:

```html
      <!-- 子视图:rounds-placeholder(阶段 3+:最小轮次占位) -->
      <div id="rounds-placeholder" class="doc-subview hidden">
        <h2>轮次视图</h2>
        <p class="hint" id="rounds-hint">已进入轮次阶段(本阶段占位)。</p>
      </div>
```

**侧栏既有分区** index.html lines 61-97(session-panel + ai-panel;AI 工作面板含 probe-controls + ai-events)。**Phase 1 D-P1-15 占位即为此预留**(CONTEXT code_context)。

**app.js 的挂点 — applySessionGates**(lines 229-244):

```javascript
  // 子视图切换:阶段 1-2 → draft-view;阶段 3+ → rounds-placeholder
  if (data.state === 'phase1_new' || data.state === 'phase12_in_progress') {
    draftView.classList.remove('hidden');
    roundsPlaceholder.classList.add('hidden');
  } else {
    draftView.classList.add('hidden');
    roundsPlaceholder.classList.remove('hidden');
    if (data.state === 'phase3' && data.current_round) {
      roundsHint.textContent = `已进入轮次阶段(本阶段占位)。当前轮:第 ${data.current_round} 轮。`;
    }
  }
```

**替换策略**:phase3 分支改为挂真轮次视图(show/hide 圆整为 `roundsView.classList.remove('hidden')`;placeholder 可整体改为 rounds-view 骨架或新建 sibling div——planner 决定,原则"extend-not-rewrite":保留 `applySessionGates` 其余门控不动)。phase4+ 分支本阶段不触达(CONTEXT 边界裁决③,D-P2-20)。

**渲染 + XSS 管线 — 复用点** app.js lines 59-71:

```javascript
function renderMarkdown(text) {
  if (!window.marked) return document.createTextNode(text || '');
  // marked v12:配置禁用原始 HTML 注入(sanitize 双保险)
  marked.setOptions({ mangle: false, headerIds: false });
  const html = marked.parse(String(text || ''));
  // 解析后仍剥离 script/style/iframe/on* 属性(AI 内容不可信)
  const tpl = document.createElement('template');
  tpl.innerHTML = html;
  stripUnsafeNodes(tpl.content);
  ...
```

注:renderMarkdown 返回 fragment 不是 string(D-P2-23 要求 note/answer/quote 走此管线 createElement/textContent,不是 innerHTML 拼接,不受链式前既定插件影响)。

**done 后拉新先例**(G-idi01-7,lines 312-320):

```javascript
async function refreshGatesAfterStream() {
  if (currentProject == null) return;
  try {
    const resp = await fetch('/api/session');
    if (!resp.ok) return;
    const data = await resp.json();
    if (data.status === 'ok') applySessionGates(data);
  } catch { /* 拉不到保持现状 */ }
}
```

轮次直播 done 后:同拍 `fetch('/api/rounds')` 拉新当前轮与冻结视图,挂同一个 refresh 链。

**弹窗(原生 modal)先例** showPermissionModal app.js lines 347-360(showPermissionModal 相关;permission-modal HTML lines 101-111)+ style.css .overlay(lines 143-153)——划词小菜单可以复用/模仿同样 native DOM 建法,菜单项点击后即 pop front-end event。划词交互 D-P2-1:浏览器原生 Selection API + mouseup 检测选区,不引库。

**事件处理与前端 fetch 先例**(POST body JSON 形态照 sendMessage lines 331-345)。
**Where the new code goes:** DOM 句柄区追加 roundsView 相关 getElementByIds(照 lines 18-37 句柄区);新分区注释块 style 照 app.js 既有 section 注释(`// --- ... ---`)。

**index.html**:侧栏新增「本轮批注流」区(照 session-panel 的 section 结构,即 BOARDType lines 62-74 形态);"处理本轮批注" + 已有「中止」常驻(work 面板区 D-P2-20)。批注流(plain 灰斜体) / status 徽标 / quote 折叠展示这些条目级呈现用 app.js 动态构建(照 chat bubble lines 165-198 的 createElement 模式,禁 innerHTML)。

**style.css**:新样式块追加文件尾,照 §4.2 语义给 annotation 条目(pending 徽标颜色、answered+plain 灰化斜体 `font-style: italic; color:#999;`、mark 高亮 `mark { background: …; }`)。字面先例:style.css lines 45-53(灰色 hint),lines 262-281(brainstorm 视图区)。

### 10. `backend/tests/test_session.py`(and/or 新文件)(D-P2-24)

**What exists today:** `FakeAICaller`(lines 29-61,含 script events + run_calls 记录 + permission script),`fresh_session` fixture(lines 68-73),`wait_idle` helper(lines 76-81):

```python
class FakeAICaller:
    """测试替身:按脚本产出事件;可注入 confirm 权限场景与挂起行为。"""

    def __init__(self, events=None, permission_script=None, before_done=None):
        self.events = events or []
        self.permission_script = permission_script or {}
        self.before_done = before_done
        self.run_calls: list[tuple[str, str]] = []
        self.aborted = False
        self.permission_requests: list[dict] = []
        self.request_permission = None
```

```python
@pytest.fixture()
def fresh_session(tmp_path, monkeypatch):
    """重置 session 全局状态(当前项目、在飞锁、pending 权限队列)。"""
    session._reset_for_tests()
    yield session
    session._reset_for_tests()

def wait_idle(sess, timeout: float = 10.0) -> bool:
    """等在飞调用结束(后台线程是异步的;断言前必须先收流)。"""
    deadline = time.time() + timeout
    while sess.busy() and time.time() < deadline:
        time.sleep(0.05)
    return not sess.busy()
```

**Required change:** FakeAICaller 类内新增 `ask_lite` 打桩(照 run 方法风格;含 `lite_calls` 记录列表,模拟真实 caller 的可观测模式):

```python
class FakeAICaller:
    def __init__(...):
        ...
        self.lite_calls: list[tuple[str, str, str]] = []  # (document_text, quoted_text, question)
        self.lite_answers = {"default": "测试即时答"}

    def ask_lite(self, document_text, quoted_text, question) -> dict:
        self.lite_calls.append((document_text, quoted_text, question))
        return {"answer": ...}
```

注意 FakeAICaller 不继承 AICaller(duck-typed),原样扩展即可——不加 `set_request_permission`,session._wire_permission_callback(lines 315-335)已有 duck-type fallback(`caller.request_permission = fn`),同形兼容。

**process_round 测试**照 test_trigger_divergence_writes_and_overwrites(lines 426-488)的 Fake subclass 模式(写盘 fake,RoundWritingFake 同构于 BrainstormWritingFake);**在飞拒绝测试**照 test_session_finalize_g1_rejects_when_busy(lines 552-579)的 HangingFake + gate/release Event 模式。

**route-level 测试**如需,照 test_route_session.py 的 route_env fixture(lines 23-29):

```python
@pytest.fixture()
def route_env(tmp_path):
    """路由级测试环境:重置 session 状态 + 独立项目目录 + TestClient。"""
    session._reset_for_tests()
    client = TestClient(main.app)
    yield {"project": tmp_path, "docs": tmp_path / "docs", "client": client}
    session._reset_for_tests()
```

标准 phase3 场景 setup(照 test_route_session.py lines 72-74 的完整轮文件直写法):

```python
    # G1 定稿后(完整轮存在)再拉:phase3、当前轮 1、两门全关
    (docs / "discuss-round-1.md").write_text(
        "# 第 1 轮\n\n> 申请授权:否\n", encoding="utf-8"
    )
```

---

## Conventions

### 语言约定
- **用户可见文案中文**(错误消息、注释、SSE content、前端 UI 文案——全部按 DESIGN.md §3.8 简洁精准红线);**标识符/函数名/变量英文**(如 ask_lite、process_round、writeback)。docstring 模块头一律 `# -*- coding: utf-8 -*-` + 中文 docstring。
- 公开函数、常量命名依既有 precedent:常量全大写下划线(`AUTH_MARKER_NO`、`_KNOWN_DOCS` 私有前缀下划线)、module-level 常量注释引用 DESIGN.md 章节/决策号。

### 模块风格约定
- 新纯模块(annotations.py / grammar.py)aurally:零第三方依赖,legacy `{from __future__ import annotations}` 头;`logging.getLogger(__name__)`;失败路径 warning 日志 + 确定性返回(不抛不悬空,照 transcript.py lines 37-39 / state.py lines 158-164 的"读不到给确定判定"模式)。
- 函数先 docstring 中文语义说明(含 DESIGN.md 章节引用);私有 helper 前缀下划线(transcript `_flush` / state `_read_text`)。

### SSE 事件约定
- batch 处理的事件 kind 沿用统一枚举前端可见形态("kind": "say" | "read" | "write" | "command" | "result" | "error" | "done"),读取权限确认等已见先例;本阶段 kind=round_started 等扩展自定(Context Claude's Discretion)。

### 测试文件命名与执行
- 新测试文件命名 `test_{module}.py` 同族;手工 sys.path 注入头(照 test_session.py lines 9-21 / test_route_session.py lines 11-20):

```python
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
```

- 带 session 状态的用例必带 `fresh_session` fixture(每 case 前后 `_reset_for_tests`);后台线程用例 meta-barrier LoadEvent 等同步原语照 test_session.py 现 style(用 `threading.Event()`,前置 wait(timeout=5));

### 验证命令约定(Phase 1 plan artifacts 既有形态)

```bash
bash -c 'set -o pipefail; cd /Users/huaxinzhang/Desktop/trifles/interactive-discuss-iteration && (.venv/bin/pip install -q pytest; true) && .venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1'
```

- 单模块先跑:`.venv/bin/python -m pytest backend/tests/test_annotations.py -q 2>&1 | tail -2` 然后**全量回归**:`.venv/bin/python -m pytest backend/tests/ -q 2>&1 | tail -1`。
- 既有 E2E 门控:`IDI_E2E` 未设时 slow 用例 skip(常轨不跑真 AI);真实 E2E 仅在需要时 `IDI_E2E=1 .venv/bin/python -m pytest backend/tests/test_e2e_smoke.py -q -m slow`。

### GSD / Git 纪律
- 计划任务内的 file-changing 动作全走 GSD(`\`/gsd-plan-phase` 产物由 gsd-planner 消费);实施后按仓库 CLAUDE.md 第 5 条:小改提交于工作分支,批量新功能视规模走分支。
- 本仓库自身 docs/discuss-round-0~4 不能进 grammar 单测正例(D-P2-19 不回溯);测试样本全部手造合规文档。

---

## No Analog Found

(none — all 10 files have direct in-repo analogs; frontend selection-popup interaction is the only genuinely new UI pattern, its base primitives(selection API + modal positioning)可照既有 permission-modal/native DOM 风格仿写)

## Metadata

**Analog search scope:** backend/ (11 源文件)、backend/tests/(10)、frontend/(3)、.planning/phases/idi-01-1-2/(verify 命令惯例)、DESIGN.md §6.2-6.4/§7.4(数据契约)
**Files scanned:** 26 tracked source files + 4 planning artifacts
**Pattern extraction date:** 2026-09-09
**Git-tracked check:** all analog paths confirmed tracked (`git ls-files backend/ frontend/`)

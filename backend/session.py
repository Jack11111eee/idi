# -*- coding: utf-8 -*-
"""模块级会话管理(D-P1-10 / PLAN idi-01-03 Task 1):单机单人,一个当前项目。

职责与流水线:
  - enter_project(path):校验目录存在 → 设当前项目 → 返回 derive_state 结果 + transcript/draft
  - send_message(user_text):完整流水线(在后台线程中跑,send 立即返回):
      ① append_message(transcript, "user", text)  —— 用户消息先落盘
      ② build_phase12_prompt —— 从磁盘读 docs/ 全部文档组装载荷(§5.1 无状态)
      ③ 后台线程起 caller.run(project, prompt) —— 事件逐条 publish 到 broker(SSE 直播)
      ④ 调用期间累积 say 文本;done 且非 abort 时把累积文本 append_message(transcript, "ai", ...)(多段合一条)
  - abort():委托 caller.abort() 并强制释放全部挂起权限为 False
  - 权限确认队列:pending {id: _PendingPermission};request_permission(tool, params) 发布
    permission_request 事件并阻塞等待用户决定(无超时——用户慢慢看;abort 强制释放为 False);
    resolve_permission(id, approved) 设置 Event,函数返回决定给 AICaller。

依赖注入:ai_caller 不 import session(依赖倒置)——AICaller 的 confirm 分支经构造函数/
属性注入的 request_permission 回调回到本模块。session 通过 events.broker 广播事件。
"""

from __future__ import annotations

import logging
import threading
import uuid
from pathlib import Path

from backend import annotations as annotations_mod
from backend import checks as checks_mod
from backend import config as cfg
from backend import g3 as g3_mod
from backend import grammar as grammar_mod
from backend.events import broker
from backend.prompts import build_divergence_prompt, build_phase12_prompt
from backend.state import (
    STATE_PHASE3,
    STATE_PHASE4,
    STATE_PHASE5_AWAITING_TIER,
    STATE_PHASE5_CHECKING,
    STATE_MISSION_COMPLETE,
    derive_state,
    list_complete_rounds,
)
from backend.state import latest_check_content as latest_check_content_mod
from backend.state import max_check_number as max_check_number_mod
from backend.transcript import append_message, parse_transcript

logger = logging.getLogger(__name__)

TRANSCRIPT_FILENAME = "docs/transcript.md"
DRAFT_FILENAME = "docs/draft.md"
BRAINSTORM_FILENAME = "docs/brainstorm.md"


class _PendingPermission:
    """一条挂起的权限确认:Event 置位 = 用户已决定,decision 为最终答复。"""

    def __init__(self, permission_id: str, tool: str, summary: str):
        self.id = permission_id
        self.tool = tool
        self.summary = summary
        self.event = threading.Event()
        self.decision: bool | None = None


# ---------------------------------------------------------------------------
# 模块级单例状态(单机单人;tests 用 _reset_for_tests 复位)
# ---------------------------------------------------------------------------

_lock = threading.Lock()
_current_project: Path | None = None
_caller = None  # 当前会话使用的 AICaller(真实工厂产物或测试注入的 FakeAICaller)
_caller_maker = cfg.make_ai_caller  # 可注入工厂(默认按 config.json)
_inflight: threading.Event | None = None  # 在飞调用标志(None = 空闲)
_ai_texts: list[str] = []  # 本次调用的 say 累积(事件线程内部缓冲)
_aborted = False
_pending: dict[str, _PendingPermission] = {}


def _reset_for_tests() -> None:
    """复位模块级状态(仅测试用:避免用例间状态泄漏)。"""
    global _current_project, _caller, _inflight, _ai_texts, _aborted, _pending
    with _lock:
        _current_project = None
        _caller = None
        _inflight = None
        _ai_texts = []
        _aborted = False
        _pending = {}


def _set_caller_for_tests(caller) -> None:
    """测试注入 FakeAICaller(绕过 config 工厂)。"""
    global _caller, _caller_maker
    with _lock:
        _caller = caller


def _publish_for_tests(event: dict) -> None:
    """事件发布 seam(默认直发 broker;测试可包装观察)。"""
    broker.publish(event)


def _register_pending_for_tests(tool: str, summary: str) -> str:
    """登记挂起权限并发布事件(实现细节暴露给 seam)。"""
    return _register_pending(tool, summary)


def _wait_for_pending_for_tests(timeout: float = 5):
    """等待出现第一个挂起权限,返回其 id(超时 None)。"""
    deadline = threading.Event()
    import time

    t0 = time.time()
    while time.time() - t0 < timeout:
        with _lock:
            if _pending:
                return next(iter(_pending))
        time.sleep(0.02)
    return None


def send_message_with_permission_for_tests(permission_fn) -> None:
    """测试驱动:send_message 全流水线,但权限回调用注入的 permission_fn。"""
    global _caller
    caller = _caller
    if caller is not None:
        _wire_permission_callback(caller, permission_fn)
    send_message("测试消息", _permission_impl=permission_fn)


# ---------------------------------------------------------------------------
# 进入项目 / 会话读取
# ---------------------------------------------------------------------------


def enter_project(path) -> dict:
    """校验目录存在后设当前项目;返回 derive_state 结果与文档读取视图。"""
    global _current_project
    project = Path(path)
    if not project.is_dir():
        raise FileNotFoundError(f"项目目录不存在:{project}")
    with _lock:
        _current_project = project.resolve()
        _caller = None  # 重进项目,清掉旧 caller(下次 send_message 重建)
    return _session_snapshot()


def _session_snapshot() -> dict:
    """当前项目的推导状态 + transcript 历史 + draft/brainstorm 内容 + 发散入口判定
    + 轮次字段(rounds 完整轮列表 / pending_annotations 当前轮待处理数,D-P2-15)。"""
    global _current_project
    with _lock:
        project = _current_project
    if project is None:
        raise RuntimeError("尚未进入任何项目(先调 enter_project)")
    state = derive_state(project)
    transcript_path = project / TRANSCRIPT_FILENAME

    # 轮次字段(仅 phase3/current_round 有 pending 计数,其余 0;plain 不计 D-P2-15)
    if state["state"] == STATE_PHASE3 and state["current_round"] is not None:
        ann = annotations_mod.load(project, state["current_round"])
        pending_count = len(annotations_mod.select_pending(ann))
    else:
        pending_count = 0

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


def snapshot() -> dict:
    """对外只读视图(main.py /api/enter 复用 enter_project 内部同一组装)。"""
    return _session_snapshot()


def current_project_path() -> Path:
    """当前项目路径只读访问器(未进入项目时 RuntimeError,路由层转 4xx)。

    供 main.py 轮次路由读当前轮文档/annotations 用——不加新全局,
    从 session 既有对外函数就近取(D-P2-22)。
    """
    with _lock:
        project = _current_project
    if project is None:
        raise RuntimeError("尚未进入任何项目(先调 enter_project)")
    return project


def _read_text(path: Path) -> str | None:
    """读文本;不存在返回 None(前端区分「无草稿」与「空草稿」)。"""
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        logger.warning("读取 %s 失败:%s", path, exc)
        return None


# ---------------------------------------------------------------------------
# 权限确认队列
# ---------------------------------------------------------------------------


def _register_pending(tool: str, summary: str) -> str:
    """登记一条挂起权限并广播 permission_request 事件(SSE → 前端弹窗)。"""
    permission_id = uuid.uuid4().hex
    pending = _PendingPermission(permission_id, tool, summary)
    with _lock:
        _pending[permission_id] = pending
    _publish_for_tests(
        {
            "kind": "permission_request",
            "id": permission_id,
            "tool": tool,
            "summary": summary,
        }
    )
    return permission_id


def _request_permission_impl(tool: str, tool_input: dict) -> bool:
    """AICaller 的 confirm 分支回环:发布事件 → 阻塞等待用户决定(无超时)。

    返回 True = 用户同意放行;False = 用户拒绝(或 abort 强制释放)。
    """
    target = (
        tool_input.get("file_path")
        or tool_input.get("notebook_path")
        or tool_input.get("path")
        or tool_input.get("command")
        or ""
    )
    summary = f"AI 请求使用工具 {tool} 操作:{target}"
    permission_id = _register_pending(tool, summary)
    with _lock:
        pending = _pending.get(permission_id)
    if pending is None:  # 竞态兜底(abort 刚清空)
        return False
    pending.event.wait()  # 无超时:用户慢慢看;abort 会强制置位
    return pending.decision is True


def request_permission(tool: str, tool_input: dict) -> bool:
    """对外回环入口(注入给 AICaller 的回调形状)。"""
    return _request_permission_impl(tool, tool_input)


def resolve_permission(permission_id: str, approved: bool) -> bool | None:
    """用户回答挂起权限:放行/驳回;返回回传给 AICaller 的决定。

    未知 id(非后端生成的挂起队列)返回 None → 路由层 404(T-idi03-01)。
    """
    with _lock:
        pending = _pending.pop(permission_id, None)
    if pending is None:
        return None
    pending.decision = bool(approved)
    pending.event.set()
    _publish_for_tests(
        {
            "kind": "permission_resolved",
            "id": permission_id,
            "approved": bool(approved),
        }
    )
    return pending.decision


# ---------------------------------------------------------------------------
# 发消息流水线
# ---------------------------------------------------------------------------


def send_message(user_text: str, _permission_impl=None) -> bool:
    """发消息:同步落盘 [user] + 校验,后台线程跑 AI 流水线。返回是否受理。

    同一时刻只允许一个在飞调用(T-idi03-04):进行中再 send 返回 False(busy)。
    """
    global _inflight, _ai_texts, _aborted
    with _lock:
        project = _current_project
        if project is None:
            raise RuntimeError("尚未进入任何项目(先调 enter_project)")
        if _inflight is not None and _inflight.is_set() is False:
            return False  # 在飞调用未结束:409 语义,由路由层转
        caller = _ensure_caller()
        _inflight = threading.Event()  # set = 未结束
        _ai_texts = []
        _aborted = False

    # ① 用户消息先落盘(含目录自举:新讨论 docs/ 尚不存在)
    transcript_path = project / TRANSCRIPT_FILENAME
    append_message(transcript_path, "user", user_text)

    # ② 组装提示词(§5.1:磁盘现状 + 本次消息)
    prompt = build_phase12_prompt(project, user_text)

    # ③ 后台线程起调用
    permission_fn = _permission_impl if _permission_impl is not None else request_permission

    def _worker():
        global _aborted
        try:
            _wire_permission_callback(caller, permission_fn)
            for event in caller.run(project, prompt):
                if _aborted:
                    break
                if event.get("kind") == "say":
                    _ai_texts.append(event.get("content", ""))
                _publish_for_tests(event)
                if event.get("kind") == "done":
                    break  # 终止事件:收流
        except Exception as exc:  # 线程内兜底:流不悬空
            _publish_for_tests(
                {"kind": "error", "content": f"调用线程异常:{exc}", "raw": None}
            )
        finally:
            # ④ done 且非 abort → [ai] 落盘(多段合一条,多行体)
            if not _aborted:
                combined = "\n\n".join(t for t in _ai_texts if t and t.strip())
                if combined.strip():
                    append_message(transcript_path, "ai", combined)
            _publish_for_tests({"kind": "done", "content": "会话轮结束", "raw": None})
            with _lock:
                inflight_local = _inflight
            if inflight_local is not None:
                inflight_local.set()  # 解锁:允许下一次 send

    threading.Thread(target=_worker, daemon=True).start()
    return True


def _ensure_caller():
    """取/建当前 caller;已在 F 计算内则复用(含权限回调注入)。"""
    global _caller
    if _caller is None:
        maker = _caller_maker
        _caller = maker(cfg.read_config())
        _wire_permission_callback(_caller)
    return _caller


def _wire_permission_callback(caller, permission_fn=None) -> None:
    """把 request_permission 回环接到 caller。

    依赖倒置:ai_caller 不 import session;session 单向注入回调。
    两条路线的 confirm 分支都经此回环(SdkAICaller 用 can_use_tool 的 confirm 分支;
    SubprocessAICaller 用 CLI 控制协议)。

    注入优先级:
      1. caller.set_request_permission(fn) —— 路线类原生注入口(真实 AICaller)
      2. caller.request_permission 属性 —— duck-typed 基本注入(测试替身等)
    """
    if permission_fn is None:
        permission_fn = request_permission
    setter = getattr(caller, "set_request_permission", None)
    if callable(setter):
        setter(permission_fn)
        return
    try:
        caller.request_permission = permission_fn
    except (AttributeError, TypeError):  # 只读属性等:无法注入时保持默认(真路线均有注入口)
        logger.warning("caller 不支持权限回调注入:%s", type(caller).__name__)


def abort() -> dict:
    """中止当前调用:caller.abort + 强制释放全部挂起权限为 False。

    未完成的 AI 回复不落盘(§5.5:不留损坏状态;孤儿半成品由重跑覆盖)。
    """
    global _aborted, _inflight
    with _lock:
        _aborted = True
        caller = _caller
        pendings = list(_pending.values())
        _pending.clear()
        inflight = _inflight
    for p in pendings:
        p.decision = False
        p.event.set()
    killed = False
    if caller is not None:
        try:
            killed = bool(caller.abort())
        except Exception as exc:
            logger.warning("abort 调用异常:%s", exc)
    if inflight is not None:
        inflight.set()
    return {"status": "aborted", "killed": killed}


def busy() -> bool:
    """当前是否有在飞调用(路由层 409 判据)。"""
    with _lock:
        return _inflight is not None and not _inflight.is_set()


# ---------------------------------------------------------------------------
# G1 定稿(FLOW-03 / D-P1-12 / §4.4)
# ---------------------------------------------------------------------------

G1_MARKER_LINE = "> 申请授权:否"  # §6.4 授权申请标记(后端追加,strip 后全等)


def g1_available(project_path) -> bool:
    """G1 入口判定(纯靠磁盘):有 draft.md 且尚无完整轮 → True。

    已有完整轮(已经定稿过)→ False——G1 只走一次,重开即 phase3。
    """
    project = Path(project_path)
    if not (project / DRAFT_FILENAME).is_file():
        return False
    if list_complete_rounds(project / "docs"):
        return False
    return True


def finalize_g1():
    """G1 认可雏形:后端动作(不涉及 AI,D-P1-12)把 draft.md 定稿为 discuss-round-1.md。

    委托 backend.g1.finalize_g1(project) 纯函数;当前层的职责:
      - 校验已进入项目(RuntimeError → 路由层 400)
      - AI 调用在飞时拒绝(锁语义同 send_message)
      - 返回 {state, current_round, current_check}(调用方拿新 derive_state 结果)
    """
    from backend.g1 import finalize_g1 as _finalize  # 延迟导入避免环(置底)

    with _lock:
        project = _current_project
        inflight_busy = _inflight is not None and not _inflight.is_set()
    if project is None:
        raise RuntimeError("尚未进入任何项目(先调 enter_project)")
    if inflight_busy:
        raise RuntimeError("当前有 AI 调用进行中,请等它结束或先中止")
    new_path = _finalize(project)
    state = derive_state(project)
    return {
        "path": str(new_path),
        "state": state["state"],
        "current_round": state["current_round"],
        "current_check": state["current_check"],
    }





def divergence_available(project_path) -> bool:
    """入口判定(纯靠磁盘):无 draft.md 且无完整轮 → True(发散开放)。

    §3.7:入口仅限阶段 1-2(雏形诞生前)——雏形(draft.md)存在或已有
    完整轮(雏形已定稿)时发散模式关闭,后续分歧一律走批注。
    """
    project = Path(project_path)
    if (project / DRAFT_FILENAME).is_file():
        return False
    if list_complete_rounds(project / "docs"):
        return False
    return True


def trigger_divergence() -> bool:
    """触发发散:走既有 AI 调用链(build_divergence_prompt → caller.run,事件照常出 SSE)。

    入口校验(防绕过):divergence_available(current_project) 为 True 才受理,
    否则返回 False(路由层转 4xx)。并发限制沿用会话锁(在飞中再触发 → False)。
    与 send_message 不同:发散不落 [user] 消息——它是后台一条自主发散指令,
    AI 说的话与写盘事件照常直播到工作面板。
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
            # 发散产物(brainstorm.md)由 AI 的 Write 工具落盘(权限门:docs/ 内放行),
            # 不落 transcript——发散不是会话消息。
            _publish_for_tests({"kind": "done", "content": "发散结束", "raw": None})
            with _lock:
                inflight_local = _inflight
            if inflight_local is not None:
                inflight_local.set()

    threading.Thread(target=_worker, daemon=True).start()
    return True


# ---------------------------------------------------------------------------
# G2 轮次收敛:「处理本轮批注」(FLOW-04 / §4.4 / D-P2-12~15,idi-02-02 Task 2)
# ---------------------------------------------------------------------------


def round_process_available(project_path) -> bool:
    """入口判定(纯靠磁盘,防绕过):derive_state == phase3 且当前轮非空。

    照 divergence_available/g1_available 的"纯磁盘"先例——只在推导结果为
    phase3 且存在完整轮(current_round 非 None)时受理「处理本轮批注」;
    其余(phase12_in_progress / phase1_new / 阶段 4+)一律关闭。
    """
    state = derive_state(Path(project_path))
    return state["state"] == STATE_PHASE3 and state["current_round"] is not None


def process_round() -> bool:
    """处理本轮批注(FLOW-04 / §4.4 G2):build_round_prompt → 后台线程 caller.run
    → AI 产出 docs/discuss-round-(N+1).md(权限门:写 docs/ 内放行)→ done 后
    后端回写上一轮 annotations(answer/status)。

    入口三查(照 trigger_divergence 模子):
      ① 未进入项目 → RuntimeError(路由层 400)
      ② 在飞调用中 → False(单飞锁,路由层 409)
      ③ round_process_available 为 False(非 phase3 / 无完整轮)→ False(409)
    事件照常 SSE 直播(§5.2:从用户点「处理本轮批注」起全程可见);
    不落 transcript(G2 不是会话消息,与 divergence 同)。

    done 后回写(D-P2-12/D-P2-13,重拉磁盘不依赖内存):
      - 重拉 derive_state:current_round 前进(新轮文档存在)→ 读新轮文档文本
        → grammar.parse_annotation_responses 解析批注回应表 → 组 answers dict
        {id: response} → annotations.writeback 回写上一轮(prev_round)条目的
        answer/status。回写异常发 error 事件,不悬空进度;不发第二条 done
        (本流水线的 done 收尾事件仍由 finally 常规发,唯一一条);
      - current_round 未前进(AI 写废/中止的半成品)→ 不回写、不报错——
        derive_state 已按完整轮判据把它视作不存在,process_round 可重跑
        (§7.3 重跑覆盖自愈,D-P2-13,零新增判错分支)。
    """
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

    state = derive_state(project)
    prev_round = state["current_round"]
    prompt = build_round_prompt(project, prev_round)

    def _worker():
        global _aborted
        try:
            _wire_permission_callback(caller)
            for event in caller.run(project, prompt):
                if _aborted:
                    break
                _publish_for_tests(event)
                if event.get("kind") == "done":
                    break
        except Exception as exc:  # 线程内兜底:流不悬空
            _publish_for_tests(
                {"kind": "error", "content": f"调用线程异常:{exc}", "raw": None}
            )
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
                            prev_round,
                            hits,
                            len(responses),
                        )
            except Exception as exc:  # 回写失败:发 error 事件,不悬空进度
                _publish_for_tests(
                    {
                        "kind": "error",
                        "content": f"批注回写异常:{exc}",
                        "raw": None,
                    }
                )
        finally:
            # done 收尾事件:本流水线唯一一条 kind=done(回写动作不发第二条)
            _publish_for_tests({"kind": "done", "content": "本轮处理结束", "raw": None})
            with _lock:
                inflight_local = _inflight
            if inflight_local is not None:
                inflight_local.set()

    threading.Thread(target=_worker, daemon=True).start()
    return True


# ---------------------------------------------------------------------------
# 批注建条目 + 大白话即时答(D-P2-7/D-P2-10/D-P2-22,idi-02-02 Task 3)
# ---------------------------------------------------------------------------


def _current_round_guard(round_n: int) -> Path:
    """建条目/大白话共用的入口校验:当前项目 + phase3 + round_n 为当前轮。

    通过 → 返回当前项目路径(调用方继续读文档/落盘);
    未进入项目 → RuntimeError(路由层 400);非当前轮或非 phase3 →
    RuntimeError「仅当前轮可批注」(路由层 409,T-idi02-06 服务端强制)。
    """
    with _lock:
        project = _current_project
    if project is None:
        raise RuntimeError("尚未进入任何项目(先调 enter_project)")
    state = derive_state(project)
    if not (
        state["state"] == STATE_PHASE3
        and state["current_round"] is not None
        and round_n == state["current_round"]
    ):
        raise RuntimeError(f"仅当前轮可批注(当前轮:{state['current_round']},请求轮:{round_n})")
    return project


def add_annotation(round_n: int, quote: str, before: str, note: str) -> dict:
    """建一条实质批注:type=comment,pending 落盘(D-P2-7:仅后端经 API 创建)。

    校验 = _current_round_guard(未进项目 400 / 非当前轮或非 phase3 → 409)。
    **不加 busy 检查**:annotations 的写入目标是当前轮文件,与 AI 回写的
    上一轮文件不同对象,无竞态(D-P2-22:409 仅「非当前轮/非 phase3」两条件,
    与 answer_plain 不同——AI 实时读文件不会写 annotations,busy 不构成冲突)。
    quote 由前端划词算好精确文本(APPLE);空 quote 由 append_item 语义兜底。
    返回新建条目 dict。
    """
    project = _current_round_guard(round_n)
    return annotations_mod.append_item(
        project, round_n, quote=quote, before=before, type="comment", note=note
    )


def answer_plain(round_n: int, quote: str, before: str, question: str) -> dict:
    """大白话即时答(§3.4 D-05 / D-P2-10):同步 caller.ask_lite → plain 落盘。

    同步执行(不起后台线程:单机单人,秒级响应无并发压力);
    单飞检查(busy → RuntimeError「当前有调用进行中」供路由层 409);
    不产 SSE 事件(轻量调用是用户查询,不代表用户主动任务,D-P2-8);
    结果 append_item(type=plain, answer=即时答, status=answered)落盘
    (D-P2-7:后端落盘;plain 不计未处理数 D-P2-15)。
    """
    with _lock:
        project = _current_project
        caller = _ensure_caller()
    if project is None:
        raise RuntimeError("尚未进入任何项目(先调 enter_project)")
    if busy():
        raise RuntimeError("当前有调用进行中,请等它结束或先中止")

    state = derive_state(project)
    if not (
        state["state"] == STATE_PHASE3
        and state["current_round"] is not None
        and round_n == state["current_round"]
    ):
        raise RuntimeError(f"仅当前轮可批注(当前轮:{state['current_round']},请求轮:{round_n})")

    # 读当前轮文档全文(不存在 FileNotFoundError → 路由层 400)
    round_doc_path = project / "docs" / f"discuss-round-{round_n}.md"
    if not round_doc_path.is_file():
        raise FileNotFoundError(f"当前轮文档不存在:{round_doc_path}")
    document_text = _read_text(round_doc_path) or ""

    result = caller.ask_lite(
        document_text=document_text, quoted_text=quote, question=question
    )
    answer = result.get("answer", "")
    if not answer:
        # AI 调用失败(answer 空 + error 键):落盘缺答案无意义,交路由层 502
        raise RuntimeError(f"大白话调用失败:{result.get('error', '未知原因')}")

    return annotations_mod.append_item(
        project,
        round_n,
        quote=quote,
        before=before,
        type="plain",
        note=question,
        answer=answer,
    )


# ---------------------------------------------------------------------------
# G3 授权 + 阶段 4 撰写 + 选档/裁决同步三件(FLOW-05 / DATA-02 / DATA-04,
# PLAN idi-03-02 Task 1 / §4.4 / §7.3① / §7.4 行 4 / D-P3-4 / D-P3-5 ~ D-P3-11)
# ---------------------------------------------------------------------------


def authorize() -> bool:
    """G3 授权:后端四查再查后写 AUTHORIZATION.md(§4.4 / §7.4 行 3→4,D-P3-4)。

    入口三查(照 answer_plain 同步风格,不起线程):
      ① 未进入项目 → RuntimeError(路由层 400)
      ② 在飞调用中 → False(拒绝瞬时写授权,防在飞期间状态漂移;路由层 409)
      ③ derive_state != phase3 或 g3_available 四查不过 → False(路由层 409)

    D-P3-4 防绕过语义:前端按钮亮否只是呈现,服务端在本入口独立重判四条
    机械校验(机械校验而非采信 AI 自评,D-17)——不存在绕过确认词的 API 路径
    (确认词在前端模态完成,D-P3-3;后端防线 = 四查再查 + 写入动作本身)。
    通过 → g3.authorize_write 落 AUTHORIZATION.md(AI 不可写,§5.4)→ True;
    FileExistsError(已授权)上抛——理论不可达(已授权后 derive_state 为
    phase4+ != phase3),保留防御供路由层 409 幂等。
    """
    with _lock:
        project = _current_project
        inflight_busy = _inflight is not None and not _inflight.is_set()
    if project is None:
        raise RuntimeError("尚未进入任何项目(先调 enter_project)")
    if inflight_busy:
        return False  # 在飞调用未结束:拒绝瞬时写授权
    state = derive_state(project)
    if state["state"] != STATE_PHASE3 or not g3_mod.g3_available(project):
        return False  # 四查不过 / 非 phase3:入口关闭(路由层 409)
    g3_mod.authorize_write(project)  # FileExistsError 上抛供路由层 409(防御)
    return True


def set_tier(tier: str) -> bool:
    """选档落盘:checks.write_tier 写 docs/DESIGN-check-tier.md(§8.2 / D-P3-11)。

    入口:未进入项目 → RuntimeError(400);derive_state !=
    phase5_awaiting_tier(有 DESIGN.md、无 check 报告)→ RuntimeError
    「仅待选档阶段可选(当前:…)」供路由层 409。tier 白名单外值由
    checks.write_tier 抛 ValueError 冒出(路由层 400)。覆盖式写入幂等
    合法:同值重选覆盖,重选改档亦覆盖(D-P3-11)。
    """
    with _lock:
        project = _current_project
    if project is None:
        raise RuntimeError("尚未进入任何项目(先调 enter_project)")
    state = derive_state(project)
    if state["state"] != STATE_PHASE5_AWAITING_TIER:
        raise RuntimeError(f"仅待选档阶段可选(当前:{state['state']})")
    checks_mod.write_tier(project, tier)  # ValueError 冒出供路由层 400
    return True


def _residue_cleared(report_text: str) -> bool:
    """残余清零判定(D-P3-17「全部处理完即视为收敛收口」,机器可判定)。

    两源问题同一配对判定式收口:
      ① 纯 P2 残余(mode=p2):问题来自问题分级表,`> 裁决:#K:` 同号配对;
      ② 修复者抛问暂停(paused):问题来自 `> 待裁决:#K:` 截存行,同号配对。
    清零 ⇔ 问题集(表编号 ∪ 待裁决编号)全部有同号裁决行 且
    unpaired_verdicts 为空;复用 grammar 锁定函数,不重实现第二套判定。
    """
    problems = {row["number"] for row in grammar_mod.parse_problem_grades(report_text)}
    verdicts = grammar_mod.parse_verdict_lines(report_text)
    problems.update(v["number"] for v in verdicts if v["kind"] == "待裁决")
    answered = {v["number"] for v in verdicts if v["kind"] == "裁决"}
    if grammar_mod.unpaired_verdicts(report_text):
        return False
    return problems <= answered


def verdict_append(number: int, decision: str, note: str) -> bool:
    """用户裁决落盘:checks.append_user_verdict 追加 `> 裁决:#K:<decision>——<note>`
    到当前核查报告(§8.2 / §6.4 / D-P3-19);残余全部配对 → 后端立即追加 PASS
    收口(D-P3-17)。

    入口:未进入项目 → RuntimeError(400);busy → False(单飞防双写竞态,
    D-P3-26);derive_state != phase5_checking → RuntimeError
    「仅自检进行中可裁决(当前:…)」供路由层 409。
    同号裁决已存在 → FileExistsError 冒出供路由层 409(一问一答)。
    追加后重读报告:_residue_cleared 判定残余清零 → append_pass_conclusion
    立即收口(derive_state 自行翻 mission_complete,§7.4 行 7)。
    """
    with _lock:
        project = _current_project
        inflight_busy = _inflight is not None and not _inflight.is_set()
    if project is None:
        raise RuntimeError("尚未进入任何项目(先调 enter_project)")
    if inflight_busy:
        return False  # 在飞调用未结束:409 语义,由路由层转
    state = derive_state(project)
    if state["state"] != STATE_PHASE5_CHECKING or state["current_check"] is None:
        raise RuntimeError(f"仅自检进行中可裁决(当前:{state['state']})")
    report_path = project / "docs" / f"DESIGN-check-{state['current_check']}.md"
    verdict_text = f"{decision}——{note}"
    checks_mod.append_user_verdict(report_path, number, verdict_text)  # FileExistsError 冒出
    # 残余清零判定(追加后重读报告,磁盘现状):
    try:
        report_text = report_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        report_text = ""
    if _residue_cleared(report_text):
        checks_mod.append_pass_conclusion(report_path, "残余裁决收口")
    return True


def writing_available(project_path) -> bool:
    """撰写入口判定(纯靠磁盘,防绕过):derive_state == phase4(§7.4 行 4)。

    有 AUTHORIZATION.md、无 DESIGN.md → True(「撰写总设计文档」/
    「继续撰写」同一入口,tmp 残留由文案二态区分,D-P3-10);
    其余态一律 False。
    """
    state = derive_state(Path(project_path))
    return state["state"] == STATE_PHASE4


def start_writing() -> bool:
    """撰写总设计文档(§7.3① / §7.4 行 4 / D-P3-6 / D-P3-8):后台线程跑
    build_writing_prompt → caller.run(AI 用 Write 写 DESIGN.md.tmp,权限门
    放行)→ done 后端原子改名 tmp → DESIGN.md(同 inode,半份 DESIGN.md
    不可能存在)。

    入口三查(照 process_round 模子):
      ① 未进入项目 → RuntimeError(路由层 400)
      ② 在飞调用中 → False(单飞锁,路由层 409)
      ③ writing_available 为 False(非 phase4)→ False(409,防绕过)
    事件照常 SSE 直播(§5.2);改名前不校验 tmp 内容完整性(D-P3-8:
    AI 产物不修补,靠重跑覆盖)。
    done 后端动作(重拉磁盘,不依赖内存):
      - tmp 存在且 DESIGN.md 未出现 → tmp.replace(design) 原子改名 →
        信息性 say 事件「总设计文档已落盘」(state 自然翻 phase5_awaiting_tier)
      - tmp 不存在(AI 没写)→ error 事件「撰写未产出 tmp,可重跑」,
        状态留 phase4(重开入口,重跑覆盖,D-P3-9)
    """
    global _inflight, _ai_texts, _aborted
    from backend.prompts import build_writing_prompt

    with _lock:
        project = _current_project
        if project is None:
            raise RuntimeError("尚未进入任何项目(先调 enter_project)")
        if _inflight is not None and _inflight.is_set() is False:
            return False  # 在飞调用未结束:并发拒绝
        if not writing_available(project):
            return False  # 非 phase4:入口关闭(防绕过)
        caller = _ensure_caller()
        _inflight = threading.Event()  # set = 未结束
        _ai_texts = []
        _aborted = False

    prompt = build_writing_prompt(project)
    tmp_path = project / "DESIGN.md.tmp"
    design_path = project / "DESIGN.md"

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
        else:
            # ---- done 后端动作:原子改名 / error 可重跑(D-P3-8) ----
            try:
                if tmp_path.is_file() and not design_path.is_file():
                    tmp_path.replace(design_path)  # 同 inode 原子改名,不校验内容
                    _publish_for_tests(
                        {
                            "kind": "say",
                            "content": "总设计文档已落盘",
                            "raw": None,
                        }
                    )
                else:
                    _publish_for_tests(
                        {
                            "kind": "error",
                            "content": "撰写未产出 tmp,可重跑",
                            "raw": None,
                        }
                    )
            except Exception as exc:  # 改名失败:发 error 事件,不悬空进度
                _publish_for_tests(
                    {"kind": "error", "content": f"总设计文档落盘异常:{exc}", "raw": None}
                )
        finally:
            # done 收尾事件:本流水线唯一一条 kind=done(改名动作不发第二条)
            _publish_for_tests({"kind": "done", "content": "撰写结束", "raw": None})
            with _lock:
                inflight_local = _inflight
            if inflight_local is not None:
                inflight_local.set()

    threading.Thread(target=_worker, daemon=True).start()
    return True


# ---------------------------------------------------------------------------
# 阶段 5 两角色循环引擎(PLAN idi-03-02 Task 2 / DATA-04 / §8.2 全节 /
# D-P3-13 ~ D-P3-22;done-回调直排,无 scheduler——每跳结束重拉磁盘判定)
# ---------------------------------------------------------------------------


def _next_check_n(project) -> int:
    """「继续自检」重跑的目标轮编号(D-P3-21 半份自愈的实现点)。

    读 max_check_number(docs):None → 1(首轮);有报告 → 读
    latest_check_content——**半份判定 = 报告缺结论行**(全文无
    `> 核查结论:` 行;AI 产物必含结论行,缺即崩在半途)→ 返回 max
    (同轮覆盖重跑,不跳号,D-P3-21 字面);报告完整(有结论行)→ 返回
    max + 1。不重排已落盘报告编号。
    """
    docs_dir = Path(project) / "docs"
    max_check = max_check_number_mod(docs_dir)
    if max_check is None:
        return 1
    latest = latest_check_content_mod(docs_dir) or ""
    if "> 核查结论:" not in latest:
        return max_check  # 半份:同轮覆盖重跑
    return max_check + 1


def check_available(project_path) -> bool:
    """自检入口判定(纯靠磁盘,防绕过;D-P3-20 与「继续修复」互斥单一路径):
    derive_state == phase5_checking → True(「继续自检」= 意外中断恢复,
    §7.3②,重跑当前核查轮覆盖半份;paused/resumed 态由 repair_available
    互斥拒绝修复跳,check 重跑覆盖是恢复通道)。

    STATE_PHASE5_AWAITING_TIER 且 tier 签名文件存在(read_tier 非 None)
    → True(选档是起检前置,D-P3-11);未选档 → False(先选档)。
    其余态 False。
    """
    state = derive_state(Path(project_path))
    if state["state"] == STATE_PHASE5_CHECKING:
        return True
    if state["state"] == STATE_PHASE5_AWAITING_TIER:
        return checks_mod.read_tier(Path(project_path)) is not None
    return False


def repair_available(project_path) -> bool:
    """修复入口判定(纯靠磁盘,双条件恰一放行——D-P3-20 判定式①②互斥的
    服务端强制,「继续自检」/「继续修复」单一路径放行):

      ① 判定式①命中(最新报告 unpaired_verdicts 非空 = 抛问待裁决,
         paused 态)→ False(裁决落盘前不得重跑修复,check-10;
         T-idi03 对应的 route 409 防线);
      ② 判定式②命中(unpaired_verdicts 为空 且 报告含 `> 裁决:#K:` 配对
         问答行 且 末行非 PASS)→ True(裁决已落盘「继续修复」唯一放行口);
      ③ 其余态 → False:
         - running 态(报告刚落盘未跑修复,无裁决行无待裁决行)→ False
           ——否则与 check_available 的「继续自检」同时可用,违反 D-P3-20;
         - 纯 P2 残余(p2 态)→ False(残余走裁决卡通道,不修复);
         - PASS 尾(mission_complete)→ False。
    """
    state = derive_state(Path(project_path))
    if state["state"] != STATE_PHASE5_CHECKING:
        return False
    docs_dir = Path(project_path) / "docs"
    latest = latest_check_content_mod(docs_dir)
    if not latest:
        return False  # 无报告(防御:phase5_checking 必有报告)
    if grammar_mod.unpaired_verdicts(latest):
        return False  # ① 暂停态:先裁决,不修复
    verdicts = grammar_mod.parse_verdict_lines(latest)
    has_answered = any(v["kind"] == "裁决" for v in verdicts)
    if has_answered and not grammar_mod.is_pass_conclusion(latest):
        return True  # ② 配对裁决 + 末行非 PASS:「继续修复」唯一放行
    return False  # ③ running(无裁决无待裁决)/ p2 / PASS


def _drive_next(project, kind: str) -> None:
    """循环驱动器外层 wrapper(D-P3-16 定案形态)。

    在 start_check/start_repair 的 finally 解锁**之后**由驱动函数串调
    (else 分支不直接自调——单飞锁未释放会自我拒绝);每跳结束重拉磁盘
    判定下一步,无 scheduler / 无 threading.Timer / 无 while True 轮询。
    abort 语义:_aborted 置位后驱动链条断(else 不排下一跳),
    「继续自检/继续修复」恢复。

    repair 跳走 start_repair(auto=True) 自动链入口:报告刚落盘
    (running 态)无裁决行,判定式②用户门不适用(那是「继续修复」
    按钮的放行条件,D-P3-20);自动链的守卫在 start_repair 的
    auto 分支重验(phase5_checking + 无未配对待裁决)。
    """
    if _aborted:
        return
    if kind == "repair":
        start_repair(auto=True)
    elif kind == "check":
        start_check()


def start_check() -> bool:
    """起一轮核查(§8.2 多方角色① / D-P3-13):后台线程 caller.run
    (build_check_prompt(project, check_n, tier))→ AI 用 Write 写
    docs/DESIGN-check-{n}.md → done-else = 循环驱动判定头部(D-P3-16):
      ① 最新报告末行 PASS → 自然结束(mission_complete 由 derive_state
         推导,§7.4 行 7;Wave 4 弹窗);
      ② 报告纯 P2(问题表全 P2,非 PASS)→ 不修复,结束(残余裁决态,
         D-22 / D-P3-17,Wave 4 呈现裁决卡);
      ③ 其余(含 P0/P1)→ 自动链入 start_repair(finally 解锁后由
         外层 wrapper _drive_next 串调,无 scheduler)。

    check_n = _next_check_n(project)(半份报告同轮覆盖重跑不跳号,D-P3-21);
    tier = 最新报告头部 parse_tier_line 或 read_tier 兜底(check_available
    在 awaiting_tier 已要求 tier 存在;两者皆无 → 严格兜底)。两跳事件
    照常 SSE 直播(§5.2)。
    """
    global _inflight, _ai_texts, _aborted
    from backend.prompts import build_check_prompt

    with _lock:
        project = _current_project
        if project is None:
            raise RuntimeError("尚未进入任何项目(先调 enter_project)")
        if _inflight is not None and _inflight.is_set() is False:
            return False  # 在飞调用未结束:并发拒绝
        if not check_available(project):
            return False  # 非 phase5 / 未选档 / 在飞:入口关闭(防绕过)
        caller = _ensure_caller()
        _inflight = threading.Event()  # set = 未结束
        _ai_texts = []
        _aborted = False

    check_n = _next_check_n(project)
    docs_dir = project / "docs"
    latest_before = latest_check_content_mod(docs_dir) or ""
    tier = grammar_mod.parse_tier_line(latest_before) or checks_mod.read_tier(project) or "严格"
    prompt = build_check_prompt(project, check_n, tier)
    tmp_path = project / "DESIGN.md.tmp"
    design_path = project / "DESIGN.md"

    def _worker():
        global _aborted
        try:
            _wire_permission_callback(caller)
            for event in caller.run(project, prompt):
                if _aborted:
                    break
                _publish_for_tests(event)
                if event.get("kind") == "done":
                    break
        except Exception as exc:  # 线程内兜底:流不悬空
            _publish_for_tests(
                {"kind": "error", "content": f"调用线程异常:{exc}", "raw": None}
            )
        else:
            # ---- 循环驱动判定头部(D-P3-16;每跳重拉磁盘)----
            try:
                latest = latest_check_content_mod(docs_dir) or ""
                if not latest:
                    _publish_for_tests(
                        {
                            "kind": "error",
                            "content": "核查未产出报告,可重跑",
                            "raw": None,
                        }
                    )
                elif grammar_mod.is_pass_conclusion(latest):
                    pass  # ① PASS:自然结束(mission_complete 由 derive_state 推导)
                elif grammar_mod.is_pure_p2(latest):
                    pass  # ② 纯 P2 残余:不修复,结束(Wave 4 呈现裁决卡)
                else:
                    pass  # ③ 含 P0/P1:finally 解锁后 _drive_next 串调修复
            except Exception as exc:
                _publish_for_tests(
                    {"kind": "error", "content": f"自检驱动判定异常:{exc}", "raw": None}
                )
        finally:
            _publish_for_tests({"kind": "done", "content": "本轮核查结束", "raw": None})
            with _lock:
                inflight_local = _inflight
            if inflight_local is not None:
                inflight_local.set()
            # finally 解锁后串调下一跳(D-P3-16 外层 wrapper;_aborted 断链;
            # PASS / 纯 P2 / 无报告 → 不驱动)
            latest = ""
            try:
                latest = latest_check_content_mod(docs_dir) or ""
            except Exception:
                pass
            if (
                not _aborted
                and latest
                and not grammar_mod.is_pass_conclusion(latest)
                and not grammar_mod.is_pure_p2(latest)
            ):
                _drive_next(project, "repair")

    threading.Thread(target=_worker, daemon=True).start()
    return True


def start_repair(auto: bool = False) -> bool:
    """起修复跳(§8.2 多方角色② / D-P3-14 / D-P3-18):后台线程 caller.run
    (build_repair_prompt;最新报告 + DESIGN.md 全文)→ done-else:
      - 全文本扫描 `> 待裁决:`(say 事件流 + 最终报告文本,先流后文本;
        scan_pending_questions 取命中清单,D-P3-18 幂等截存)→ 有命中 →
        checks.append_pending_question 逐条截存到当轮报告尾部 + error 事件
        「修复者抛问,已截存暂停,等待用户裁决」,**不驱动下一跳**(循环
        停在当前跳;识别到标记一律暂停,误暂停代价 = 用户看一眼,比误
        推进安全);
      - 无命中且 tmp 已写 → tmp 原子改名 DESIGN.md(同 writing,D-P3-22)
        → 驱动判定:宽松档(tier == 宽松)→ 结束(PASS 由修复者已追加
        或残余收口动作处理);严格档 → start_check(check_n+1,同轮驱动器);
      - 无命中且 tmp 不存在(AI 没写)→ error 事件「修复未产出 tmp,可
        重跑」,不驱动下一跳(重跑覆盖自愈)。

    入口判定(D-P3-20):
      - auto=False(用户「继续修复」按钮):repair_available 双条件恰一
        放行——判定式②(配对裁决 + 无未配对 + 末行非 PASS)才 True;
        running 态(报告刚落盘未跑修复)与 unpaired 非空(paused 态)
        均拒绝 409。
      - auto=True(严格档自动链,check-done 后由 _drive_next 串调):
        只重验 phase5_checking + 无未配对待裁决(报告刚落盘的 running
        形态正是自动修复的目标盘,判定式②的用户门不适用)。
    两者同样受单飞锁(在飞 409)与未进项目(400)约束。
    """
    global _inflight, _ai_texts, _aborted
    from backend.prompts import build_repair_prompt

    with _lock:
        project = _current_project
        if project is None:
            raise RuntimeError("尚未进入任何项目(先调 enter_project)")
        if _inflight is not None and _inflight.is_set() is False:
            return False  # 在飞调用未结束:并发拒绝
        if not repair_available(project):
            if not auto:
                return False  # 判定式②未命中:用户入口关闭(D-P3-20 互斥)
            # 自动链:重验 phase5_checking + 无未配对待裁决(§8.2 两跳自动)
            state_auto = derive_state(project)
            if state_auto["state"] != STATE_PHASE5_CHECKING:
                return False
            latest = latest_check_content_mod(project / "docs") or ""
            if grammar_mod.unpaired_verdicts(latest):
                return False  # 暂停态(待裁决):自动链也停,等用户
        caller = _ensure_caller()
        _inflight = threading.Event()  # set = 未结束
        _ai_texts = []
        _aborted = False

    state = derive_state(project)
    check_n = state["current_check"]
    docs_dir = project / "docs"
    latest_before = latest_check_content_mod(docs_dir) or ""
    tier = grammar_mod.parse_tier_line(latest_before) or checks_mod.read_tier(project) or "严格"
    prompt = build_repair_prompt(project, check_n, tier)
    tmp_path = project / "DESIGN.md.tmp"
    design_path = project / "DESIGN.md"

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
        else:
            # ---- done 后端动作:抛问扫描 → 截存暂停 / 改名 → 下一跳 ----
            try:
                # 先流后文本(D-P3-18:say 事件流 + 报告文本都扫;
                # 报告文本兜底覆盖修复者把抛问写进报告正文的形态)
                combined_text = "\n".join(t for t in _ai_texts if t)
                try:
                    report_text = (
                        docs_dir / f"DESIGN-check-{check_n}.md"
                    ).read_text(encoding="utf-8", errors="replace")
                except OSError:
                    report_text = ""
                scanned = grammar_mod.scan_pending_questions(
                    combined_text + "\n" + report_text
                )
                if scanned:
                    for q in scanned:
                        checks_mod.append_pending_question(
                            docs_dir / f"DESIGN-check-{check_n}.md",
                            q["number"],
                            q["text"],
                        )
                    _publish_for_tests(
                        {
                            "kind": "error",
                            "content": "修复者抛问,已截存暂停,等待用户裁决",
                            "raw": None,
                        }
                    )
                    # 不驱动下一跳:循环停在当前跳;finally 尾部的驱动判定
                    # 由 unpaired_verdicts 非空拦截(截存后报告必含未配对待裁决)
                else:
                    # 无命中:tmp 存在 → 原子改名(D-P3-8/D-P3-22 同 writing)
                    if tmp_path.is_file() and design_path.is_file():
                        tmp_path.replace(design_path)
                    elif not tmp_path.is_file():
                        _publish_for_tests(
                            {
                                "kind": "error",
                                "content": "修复未产出 tmp,可重跑",
                                "raw": None,
                            }
                        )
            except Exception as exc:
                _publish_for_tests(
                    {"kind": "error", "content": f"修复收尾异常:{exc}", "raw": None}
                )
        finally:
            _publish_for_tests({"kind": "done", "content": "修复结束", "raw": None})
            with _lock:
                inflight_local = _inflight
            if inflight_local is not None:
                inflight_local.set()
            # 每跳结束重拉磁盘判定下一步(finally 解锁后外层 wrapper 串调;
            # 抛问截存 → unpaired 非空断链;宽松档不链;tmp 缺失不链)
            if _aborted or tier == "宽松":
                return
            latest = ""
            try:
                latest = latest_check_content_mod(docs_dir) or ""
            except Exception:
                pass
            if not latest or grammar_mod.unpaired_verdicts(latest):
                return  # 抛问截存盘:不再自动推进
            if tmp_path.is_file():
                return  # tmp 未消费(异常形态,不推进;重跑覆盖)
            _drive_next(project, "check")

    threading.Thread(target=_worker, daemon=True).start()
    return True

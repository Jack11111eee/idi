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

from backend import config as cfg
from backend.events import broker
from backend.prompts import build_divergence_prompt, build_phase12_prompt
from backend.state import STATE_PHASE3, derive_state, list_complete_rounds
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
    """当前项目的推导状态 + transcript 历史 + draft/brainstorm 内容 + 发散入口判定。"""
    global _current_project
    with _lock:
        project = _current_project
    if project is None:
        raise RuntimeError("尚未进入任何项目(先调 enter_project)")
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


def snapshot() -> dict:
    """对外只读视图(main.py /api/enter 复用 enter_project 内部同一组装)。"""
    return _session_snapshot()


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
    from backend import annotations as annotations_mod

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

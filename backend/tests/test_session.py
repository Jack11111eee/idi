# -*- coding: utf-8 -*-
"""session 会话层测试(PLAN idi-01-03 Task 1,TDD RED 先行)。

六个 behavior 用例全部用 FakeAICaller(伪造 caller,产固定事件序列,
含可注入的 confirm 场景)——所有用例不起真 claude 进程。
send_message 全流水线用直接调(不 via FastAPI)。
"""

import sys
import threading
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend import prompts as prompts_mod  # noqa: E402
from backend import session  # noqa: E402
from backend.ai_caller import make_permission_decision  # noqa: E402
from backend.transcript import parse_transcript  # noqa: E402


# ---------------------------------------------------------------------------
# FakeAICaller:伪造 caller(不起真进程)
# ---------------------------------------------------------------------------


class FakeAICaller:
    """测试替身:按脚本产出事件;可注入 confirm 权限场景与挂起行为。"""

    def __init__(self, events=None, permission_script=None, before_done=None):
        self.events = events or []
        self.permission_script = permission_script or {}
        self.before_done = before_done
        self.run_calls: list[tuple[str, str]] = []
        self.aborted = False
        self.permission_requests: list[dict] = []
        # request_permission 回调由 session 在 send_message 时注入
        self.request_permission = None

    def run(self, project_path, prompt: str):
        self.run_calls.append((str(project_path), prompt))
        for ev in list(self.events):
            yield dict(ev)
        # confirm 场景:模拟 AICaller 需要权限判定(经注入的回调回环)
        if self.permission_script:
            tool_name, tool_input = self.permission_script["tool"]
            if self.request_permission is not None:
                decision = self.request_permission(tool_name, tool_input)
                self.permission_requests.append(
                    {"tool": tool_name, "input": tool_input, "decision": decision}
                )
        if self.before_done is not None:
            self.before_done()
        yield {"kind": "done", "content": "调用结束", "raw": None}

    def abort(self) -> bool:
        self.aborted = True
        return True


# ---------------------------------------------------------------------------
# fixture:每个用例独立重置 session 模块级状态(单机单人,模块即单例)
# ---------------------------------------------------------------------------


@pytest.fixture()
def fresh_session(tmp_path, monkeypatch):
    """重置 session 全局状态(当前项目、在飞锁、pending 权限队列)。"""
    session._reset_for_tests()
    yield session
    session._reset_for_tests()


# ---------------------------------------------------------------------------
# 用例 1:send_message 流水线——[user] 先落盘、prompt 含 docs/ 全部文档、[ai] 收尾
# ---------------------------------------------------------------------------


def test_send_message_pipeline(tmp_path, fresh_session):
    """用例 1:send_message 依次产生 [user] 落盘 → 含 docs/ 内容的 prompt → [ai] 落盘。"""
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "transcript.md").write_text("", encoding="utf-8")
    (docs / "draft.md").write_text("# 草稿\n\n现有雏形说明。\n", encoding="utf-8")
    (docs / "brainstorm.md").write_text("风暴记录。\n", encoding="utf-8")

    fake = FakeAICaller(
        events=[
            {"kind": "say", "content": "我看看你说的。", "raw": None},
            {"kind": "read", "content": str(docs / "draft.md"), "raw": None},
        ]
    )
    fresh_session.enter_project(tmp_path)
    fresh_session._set_caller_for_tests(fake)

    ok = fresh_session.send_message("帮我把目标写清楚一点")
    assert ok is True or ok is None  # 返回形状:不抛异常即可

    transcript_path = docs / "transcript.md"
    messages = parse_transcript(transcript_path)
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "帮我把目标写清楚一点"
    assert messages[1]["role"] == "ai"
    assert "我看看你说的" in messages[1]["content"]

    # prompt 组装:含用户消息、draft 内容(§5.1 从磁盘读全部文档)
    assert len(fake.run_calls) == 1
    proj_path, prompt = fake.run_calls[0]
    assert str(tmp_path) in proj_path
    assert "帮我把目标写清楚一点" in prompt
    assert "现有雏形说明" in prompt  # draft.md 内容注入
    assert "风暴记录" in prompt  # brainstorm.md 内容注入
    # §3.8 语言红线注入
    assert "简洁" in prompt
    assert "大白话" in prompt


# ---------------------------------------------------------------------------
# 用例 2:多段 say 合一条 [ai](多行消息体,不拆条)
# ---------------------------------------------------------------------------


def test_multi_segment_say_single_ai_entry(tmp_path, fresh_session):
    """用例 2:AI 输出多段时,[ai] 作为一条多行消息落盘(不是多条)。"""
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "transcript.md").write_text("", encoding="utf-8")

    fake = FakeAICaller(
        events=[
            {"kind": "say", "content": "第一段:先看目标。", "raw": None},
            {"kind": "read", "content": "/tmp/x.md", "raw": None},
            {"kind": "say", "content": "第二段:再补充维度。", "raw": None},
        ]
    )
    fresh_session.enter_project(tmp_path)
    fresh_session._set_caller_for_tests(fake)
    fresh_session.send_message("继续")

    messages = parse_transcript(docs / "transcript.md")
    assert len(messages) == 2
    ai_msg = messages[1]
    assert ai_msg["role"] == "ai"
    # 两段合进同一条,多行体
    assert "第一段:先看目标" in ai_msg["content"]
    assert "第二段:再补充维度" in ai_msg["content"]
    assert "\n" in ai_msg["content"]


# ---------------------------------------------------------------------------
# 用例 3:权限确认队列——confirm 判定挂起任务、登记 pending、阻塞等决定
# ---------------------------------------------------------------------------


class _PendingProbe:
    """记录 confirm 挂起行为的探针。"""

    def __init__(self):
        self.hang_started = threading.Event()
        self.hang_released = threading.Event()
        self.saw_pending_ids = []

    def fake_request_permission(self, tool_name, tool_input):
        return False  # 默认不允许,等主线程 resolve


def test_confirm_pends_until_resolved(tmp_path, fresh_session):
    """用例 3:confirm 判定 → 任务挂起、pending 登记,AI 线程阻塞等待用户决定。"""
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "transcript.md").write_text("", encoding="utf-8")

    proj = tmp_path / "proj"
    proj.mkdir()
    target = proj / "outside.md"
    # §5.4:写项目内 docs/ 外 → confirm
    assert make_permission_decision(proj, "write", target) == "confirm"

    released = threading.Event()

    def slow_permission(tool_name, tool_input):
        # 模拟用户未決:阻塞直到 resolve
        released.wait(timeout=10)
        return True

    fake = FakeAICaller(
        events=[{"kind": "say", "content": "我要写项目根的文件了。", "raw": None}],
        permission_script={
            "tool": ("Write", {"file_path": str(target), "content": "x"})
        },
    )
    fresh_session.enter_project(tmp_path)
    fresh_session._set_caller_for_tests(fake)

    # 挂一个 permission_request 事件观察器
    published = []
    orig_publish = fresh_session._publish_for_tests
    fresh_session._publish_for_tests = lambda ev: (published.append(ev), orig_publish(ev))

    # send_message 在后台线程跑;权限回调先挂起
    send_thread = threading.Thread(target=lambda: fresh_session.send_message("写个文件"))
    send_thread.start()

    # 等 permission_request 事件出现(带 id 与工具参数)
    deadline = time.time() + 5
    perm_event = None
    while time.time() < deadline:
        for ev in published:
            if ev.get("kind") == "permission_request":
                perm_event = ev
                break
        if perm_event:
            break
        time.sleep(0.05)
    assert perm_event is not None, "未发布 permission_request 事件"
    assert "id" in perm_event and perm_event["id"]
    assert perm_event.get("tool") == "Write"
    assert str(target) in str(perm_event.get("summary", ""))

    # AI 调用线程此刻仍被阻塞(未收到决定)
    assert send_thread.is_alive()

    # 放行:resolve_permission(id, True)
    released.set()
    fresh_session.resolve_permission(perm_event["id"], True)
    send_thread.join(timeout=10)
    assert not send_thread.is_alive()

    # 放行后 AI 回复正常落盘
    messages = parse_transcript(docs / "transcript.md")
    assert len(messages) == 2
    assert messages[1]["role"] == "ai"


# ---------------------------------------------------------------------------
# 用例 4:approve=True 放行;approve=False 时 AICaller 收到拒绝
# ---------------------------------------------------------------------------


def test_resolve_permission_deny_reaches_caller(tmp_path, fresh_session):
    """用例 4:resolve_permission(id, False) 让 AICaller 权限回调收到 False。"""
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "transcript.md").write_text("", encoding="utf-8")

    fake = FakeAICaller(
        events=[{"kind": "say", "content": "试试写文件。", "raw": None}],
        permission_script={
            "tool": ("Write", {"file_path": "/anywhere/outside.md", "content": "y"})
        },
    )
    fresh_session.enter_project(tmp_path)
    fresh_session._set_caller_for_tests(fake)

    pending_perm = {}

    def hanging_permission(tool_name, tool_input):
        pid = fresh_session._wait_for_pending_for_tests(timeout=5)
        assert pid is not None, "5 秒内未出现挂起权限"
        pending_perm["id"] = pid
        decision = fresh_session.resolve_permission(pid, False)
        return decision

    # 直接驱动:用注入的回调路径(fake.request_permission 在 run 内被调)
    fake.request_permission = None

    # 简化路径:monkeypatch session.request_permission 内部等待逻辑由线程驱动
    # 这里测 resolve 的直接语义:伪造一个挂起,然后拒绝
    registered = {}

    orig_register = fresh_session._register_pending_for_tests
    fresh_session._register_pending_for_tests = lambda tool, summary: registered.setdefault(
        "id", orig_register(tool, summary)
    )

    send_thread = threading.Thread(
        target=lambda: fresh_session.send_message_with_permission_for_tests(
            hanging_permission
        )
    )
    try:
        send_thread.start()
        deadline = time.time() + 5
        while "id" not in registered and time.time() < deadline:
            time.sleep(0.05)
        assert "id" in registered, "未登记 pending 权限"
        # 拒绝路径:decision 传回 False
        pid = registered["id"]
        decision = fresh_session.resolve_permission(pid, False)
        assert decision is False
        send_thread.join(timeout=10)
        assert fake.permission_requests, "AICaller 权限回环未被调用"
        assert fake.permission_requests[-1]["decision"] is False
    finally:
        send_thread.join(timeout=5)


# ---------------------------------------------------------------------------
# 用例 5:abort 后无半条脏 [ai]
# ---------------------------------------------------------------------------


def test_abort_leaves_no_dirty_ai_entry(tmp_path, fresh_session):
    """用例 5:abort 中止时,未完成的 AI 回复不落盘(transcript 无半条脏 [ai])。"""
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "transcript.md").write_text("", encoding="utf-8")

    mid_stream = threading.Event()

    def before_done_hook():
        # 在 done 之前模拟用户点了中止
        mid_stream.set()

    fake = FakeAICaller(
        events=[
            {"kind": "say", "content": "开头说了几句,但还没说完。", "raw": None},
        ],
        before_done=before_done_hook,
    )
    fresh_session.enter_project(tmp_path)
    fresh_session._set_caller_for_tests(fake)

    send_thread = threading.Thread(target=lambda: fresh_session.send_message("长回答"))
    send_thread.start()
    mid_stream.wait(timeout=5)
    fresh_session.abort()
    send_thread.join(timeout=10)

    messages = parse_transcript(docs / "transcript.md")
    # [user] 在;[ai] 不在(中止,未完成的回复不落盘)
    assert len(messages) == 1
    assert messages[0]["role"] == "user"


# ---------------------------------------------------------------------------
# 用例 6:build_phase12_prompt 四段结构
# ---------------------------------------------------------------------------


def test_build_phase12_prompt_sections(tmp_path, monkeypatch):
    """用例 6:注入用户消息、历史 transcript、draft 现状、docs/ 文档与语言红线。"""
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "transcript.md").write_text(
        "[user]\n之前聊过目标。\n\n[ai]\n好的,收到。\n", encoding="utf-8"
    )
    (docs / "draft.md").write_text("# 雏形草稿\n\n目标:做一个本地讨论工具。\n", encoding="utf-8")

    prompt = prompts_mod.build_phase12_prompt(tmp_path, "本次的新消息")
    # 系统段:角色 + §3.8 语言红线
    assert "讨论" in prompt
    assert "简洁" in prompt and "大白话" in prompt
    # 资料段:transcript 历史 + draft 现状
    assert "之前聊过目标" in prompt
    assert "做一个本地讨论工具" in prompt
    # 任务段:用户本次消息
    assert "本次的新消息" in prompt
    assert "draft.md" in prompt


def test_build_phase12_prompt_fresh_project(tmp_path):
    """用例 6b:docs/ 为空/不存在时说明「全新讨论」。"""
    empty_dir = tmp_path / "fresh"
    empty_dir.mkdir()
    prompt = prompts_mod.build_phase12_prompt(empty_dir, "你好")
    assert "全新讨论" in prompt
    assert "你好" in prompt

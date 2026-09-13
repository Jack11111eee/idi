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
    """测试替身:按脚本产出事件;可注入 confirm 权限场景与挂起行为。

    Phase 2 扩展(D-P2-24):ask_lite 打桩——lite_calls 记录三元组
    (document_text, quoted_text, question),lite_answers 可注入固定答案
    (None 时返回固定「测试即时答」)。run/abort 形态不变(duck-type 兼容)。
    """

    def __init__(self, events=None, permission_script=None, before_done=None,
                 lite_answers=None):
        self.events = events or []
        self.permission_script = permission_script or {}
        self.before_done = before_done
        self.run_calls: list[tuple[str, str]] = []
        self.aborted = False
        self.permission_requests: list[dict] = []
        # request_permission 回调由 session 在 send_message 时注入
        self.request_permission = None
        # 轻量调用观测与应答注入(D-P2-8 同一契约;记录三元组,可注入固定答案)
        self.lite_calls: list[tuple[str, str, str]] = []
        self.lite_answers: dict[str, str] | None = lite_answers

    def ask_lite(self, document_text: str, quoted_text: str, question: str) -> dict:
        """打桩 ask_lite:记录三元组,返回注入答案或固定值。"""
        self.lite_calls.append((document_text, quoted_text, question))
        if self.lite_answers is not None:
            return {"answer": self.lite_answers.get(question, "测试即时答")}
        return {"answer": "测试即时答"}

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


def wait_idle(sess, timeout: float = 10.0) -> bool:
    """等在飞调用结束(后台线程是异步的;断言前必须先收流)。"""
    deadline = time.time() + timeout
    while sess.busy() and time.time() < deadline:
        time.sleep(0.05)
    return not sess.busy()


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
    assert wait_idle(fresh_session), "后台调用未在时限内结束"

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
    assert wait_idle(fresh_session), "后台调用未在时限内结束"

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

    # send_message 在后台线程跑;权限回调由 session 注入 fake,先挂起等用户
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

    # AI 调用线程仍在跑(worker 还阻塞在权限等待,send 的外层线程也还在)
    assert fresh_session.busy(), "权限未决时调用应仍被阻塞(busy)"

    # 放行:resolve_permission(id, True)
    fresh_session.resolve_permission(perm_event["id"], True)
    deadline = time.time() + 10
    while fresh_session.busy() and time.time() < deadline:
        time.sleep(0.05)
    assert not fresh_session.busy(), "放行后调用未在时限内结束"

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

    # send_message 注入 session.request_permission 给 fake(worker 内 wiring);
    # fake 脚本触发真实回环 → pending 登记 → 阻塞。主线程等登记后拒绝。
    send_thread = threading.Thread(target=lambda: fresh_session.send_message("写个文件"))
    send_thread.start()

    pid = fresh_session._wait_for_pending_for_tests(timeout=5)
    assert pid is not None, "5 秒内未出现挂起权限"
    # 拒绝路径:决定传回 False 给 AICaller 的回环
    decision = fresh_session.resolve_permission(pid, False)
    assert decision is False

    deadline = time.time() + 10
    while fresh_session.busy() and time.time() < deadline:
        time.sleep(0.05)
    assert not fresh_session.busy(), "拒绝后调用未在时限内结束"

    assert fake.permission_requests, "AICaller 权限回环未被调用"
    assert fake.permission_requests[-1]["decision"] is False
    # 拒绝后 pending 队列清空;未知 id 二次 resolve 返回 None(T-idi03-01)
    assert fresh_session.resolve_permission(pid, False) is None
    assert not fresh_session._pending


# ---------------------------------------------------------------------------
# 用例 5:abort 后无半条脏 [ai]
# ---------------------------------------------------------------------------


def test_abort_leaves_no_dirty_ai_entry(tmp_path, fresh_session):
    """用例 5:abort 中止时,未完成的 AI 回复不落盘(transcript 无半条脏 [ai])。"""
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "transcript.md").write_text("", encoding="utf-8")

    mid_stream = threading.Event()
    resume_stream = threading.Event()

    class AbortingFakeAICaller(FakeAICaller):
        """say 已产出但 AI 仍在生成(done 未到)的形态;abort 后收流。"""

        def run(self, project_path, prompt):
            self.run_calls.append((str(project_path), prompt))
            for ev in list(self.events):
                yield dict(ev)
            mid_stream.set()  # say 全部产出,AI 仍在生成
            resume_stream.wait(timeout=5)  # 等 abort(或超时自续)
            if not self.aborted:
                yield {"kind": "done", "content": "调用结束", "raw": None}
            else:
                # 被杀:流被切断,不再产 done(abort 语义:未完成的回复不落盘)
                return

        def abort(self):
            self.aborted = True
            resume_stream.set()
            return True

    fake = AbortingFakeAICaller(
        events=[
            {"kind": "say", "content": "开头说了几句,但还没说完。", "raw": None},
        ],
    )
    fresh_session.enter_project(tmp_path)
    fresh_session._set_caller_for_tests(fake)

    send_thread = threading.Thread(target=lambda: fresh_session.send_message("长回答"))
    send_thread.start()
    assert mid_stream.wait(timeout=5), "未到达 AI 生成中时刻"
    fresh_session.abort()
    deadline = time.time() + 10
    while fresh_session.busy() and time.time() < deadline:
        time.sleep(0.05)
    assert not fresh_session.busy(), "abort 后调用未收尾"
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


# ---------------------------------------------------------------------------
# 发散模式(PLAN idi-01-04 Task 1,FLOW-06)——四用例
# ---------------------------------------------------------------------------


def test_build_divergence_prompt_three_steps(tmp_path):
    """用例 1:发散模板三段结构(多视角风暴 N≥4 固定视角 / 收敛 3~5 候选 / 挑选引导)+ §3.8 红线 + 落盘指令。"""
    from backend.prompts import build_divergence_prompt

    empty_dir = tmp_path / "fresh"
    empty_dir.mkdir()
    prompt = build_divergence_prompt(empty_dir)

    # 三步走指令逐项在场
    assert "多视角风暴" in prompt       # ①风暴指令
    assert "收敛" in prompt             # ②收敛指令
    assert "挑选" in prompt or "委托" in prompt  # ③挑选引导
    # 固定视角清单(N ≥ 4)
    assert "解决谁的什么痛点" in prompt
    assert "最省事的版本" in prompt
    assert "最贵的版本" in prompt
    assert "没人做但该有人做的" in prompt
    # 每视角 2~3 个方向、鼓励离谱
    assert "2" in prompt and "3" in prompt
    assert "离谱" in prompt
    # 收敛规格:3~5 候选 + 一句话说明 + 为什么值得做
    assert "3" in prompt and "5" in prompt
    assert "一句话说明" in prompt
    assert "为什么值得做" in prompt
    # §3.8 语言红线
    assert "简洁" in prompt and "大白话" in prompt
    # 落盘指令:整体覆盖写 docs/brainstorm.md
    assert "docs/brainstorm.md" in prompt
    assert "覆盖" in prompt


def test_divergence_prompt_includes_existing_brainstorm(tmp_path):
    """用例 4:prompt 含既有 brainstorm.md 内容(再次发散时看得见上一轮候选)。"""
    from backend.prompts import build_divergence_prompt

    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "brainstorm.md").write_text("# 上一轮候选\n\n候选 A:做 XX。\n", encoding="utf-8")
    prompt = build_divergence_prompt(tmp_path)
    assert "上一轮候选" in prompt
    assert "候选 A" in prompt


def test_trigger_divergence_writes_and_overwrites(tmp_path, fresh_session):
    """用例 2:触发发散 → brainstorm.md 创建;再次触发 → 整体覆盖(无 -2 编号新文件)。

    写盘者是 AI 的 Write 工具(权限门:docs/ 内自动放行)——伪造 caller 用
    BrainstormWritingFake 模拟"AI 在调用中写盘"这一行为;session 层职责是
    把发散 prompt 交给同一条 AICaller 链路并让事件照常出 SSE。
    """
    import os

    class BrainstormWritingFake(FakeAICaller):
        """run 时把风暴产物写入 docs/brainstorm.md(Write 工具语义:整体覆盖)。"""

        def __init__(self, events, content):
            super().__init__(events=events)
            self.content = content

        def run(self, project_path, prompt: str):
            self.run_calls.append((str(project_path), prompt))
            docs_dir = Path(project_path) / "docs"
            docs_dir.mkdir(parents=True, exist_ok=True)
            (docs_dir / "brainstorm.md").write_text(self.content, encoding="utf-8")
            for ev in list(self.events):
                yield dict(ev)
            yield {"kind": "done", "content": "调用结束", "raw": None}

    fresh_session.enter_project(tmp_path)

    fake1 = BrainstormWritingFake(
        events=[{"kind": "say", "content": "开始发散。", "raw": None}],
        content="# 第一轮风暴\n\n候选 1:做 XX。\n",
    )
    fresh_session._set_caller_for_tests(fake1)
    ok = fresh_session.trigger_divergence()
    assert ok is True, "入口开放时发散应被受理"
    assert wait_idle(fresh_session), "第一次发散未在时限内结束"

    brainstorm = tmp_path / "docs" / "brainstorm.md"
    assert brainstorm.is_file(), "发散后 brainstorm.md 应被创建"
    assert "第一轮风暴" in brainstorm.read_text(encoding="utf-8")
    mtime_first = os.path.getmtime(brainstorm)

    time.sleep(0.02)  # 保证 mtime 分辨(文件系统秒级截断的兜底)

    fake2 = BrainstormWritingFake(
        events=[{"kind": "say", "content": "再发散一轮。", "raw": None}],
        content="# 第二轮风暴\n\n候选 A:完全不同的方向。\n",
    )
    fresh_session._set_caller_for_tests(fake2)
    ok = fresh_session.trigger_divergence()
    assert ok is True, "入口仍开放(无 draft/无轮次)时再次发散应被受理"
    assert wait_idle(fresh_session), "第二次发散未在时限内结束"

    assert "第二轮风暴" in brainstorm.read_text(encoding="utf-8")
    assert "第一轮风暴" not in brainstorm.read_text(encoding="utf-8"), \
        "再发散应整体覆盖旧文件,而不是追加"
    assert os.path.getmtime(brainstorm) > mtime_first, "覆盖后 mtime 应变化"

    # 无编号变体文件(brainstorm-2.md 等)
    docs_files = [p.name for p in brainstorm.parent.iterdir()]
    assert "brainstorm.md" in docs_files
    assert not any(
        n != "brainstorm.md" and n.startswith("brainstorm") for n in docs_files
    ), f"发散产物出现编号变体: {docs_files}"

    # 走的是同一 AICaller 链路:写入 caller 的 prompt 是发散模板(不是会话模板)
    assert len(fake2.run_calls) == 1
    _, diverge_prompt = fake2.run_calls[0]
    assert "多视角风暴" in diverge_prompt, "发散触发的 prompt 应为发散指令模板"


def test_divergence_available_gating(tmp_path, fresh_session):
    """用例 3:入口判定——无 draft 且无完整轮 → True;draft.md 存在 → False;有完整轮 → False。"""
    from backend.state import AUTH_MARKER_NO

    empty_project = tmp_path / "empty"
    empty_project.mkdir()
    assert fresh_session.divergence_available(empty_project) is True

    with_draft = tmp_path / "withdraft"
    (with_draft / "docs").mkdir(parents=True)
    (with_draft / "docs" / "draft.md").write_text("# 雏形\n", encoding="utf-8")
    assert fresh_session.divergence_available(with_draft) is False

    with_round = tmp_path / "withround"
    (with_round / "docs").mkdir(parents=True)
    (with_round / "docs" / "discuss-round-1.md").write_text(
        "# 轮次\n\n正文。\n\n> 申请授权:否\n", encoding="utf-8"
    )
    assert fresh_session.divergence_available(with_round) is False

    # 触发侧防绕过:雏形存在时 trigger_divergence 拒绝(不发起调用)
    fresh_session.enter_project(with_draft)
    rejected = fresh_session.trigger_divergence()
    assert rejected is False, "draft.md 存在时发散应被拒绝"


# ---------------------------------------------------------------------------
# G1 session 层(PLAN idi-01-04 Task 2):finalize_g1 会话封装 + 在飞拒绝 + 快照字段
# ---------------------------------------------------------------------------


def test_session_finalize_g1_and_gating(tmp_path, fresh_session):
    """G1 会话封装:定稿成功返回 phase3 形状;在飞调用时拒绝;重复定稿抛 FileExistsError。"""
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "draft.md").write_text("# 雏形\n\n已谈妥。\n", encoding="utf-8")

    # 空闲时定稿:返回 {path, state, current_round, current_check}
    fresh_session.enter_project(tmp_path)
    result = fresh_session.finalize_g1()
    assert result["state"] == "phase3"
    assert result["current_round"] == 1
    assert result["current_check"] is None
    assert result["path"].endswith("discuss-round-1.md")

    # 重复定稿:幂等防护(后端 409 语义)
    with pytest.raises(FileExistsError):
        fresh_session.finalize_g1()

    # 定稿后快照:divergence/g1 双入口均关闭(雏形已定稿)
    snap = fresh_session.snapshot()
    assert snap["state"] == "phase3"
    assert snap["divergence_available"] is False
    assert snap["g1_available"] is False


def test_session_finalize_g1_rejects_when_busy(tmp_path, fresh_session):
    """G1 在飞拒绝(锁语义同 send_message):AI 调用进行中定稿被驳回。"""
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "draft.md").write_text("# 雏形\n", encoding="utf-8")
    (docs / "transcript.md").write_text("", encoding="utf-8")

    gate = threading.Event()
    release = threading.Event()

    class HangingFake(FakeAICaller):
        def run(self, project_path, prompt):
            self.run_calls.append((str(project_path), prompt))
            gate.set()
            release.wait(timeout=5)  # 模拟调用在飞
            yield {"kind": "done", "content": "调用结束", "raw": None}

    fake = HangingFake(events=[])
    fresh_session.enter_project(tmp_path)
    fresh_session._set_caller_for_tests(fake)
    threading.Thread(target=lambda: fresh_session.send_message("先聊"), daemon=True).start()
    assert gate.wait(timeout=5), "在飞调用未启动"

    with pytest.raises(RuntimeError, match="在飞|进行中"):
        fresh_session.finalize_g1()

    release.set()
    assert wait_idle(fresh_session), "调用未收尾"


# ---------------------------------------------------------------------------
# 大白话轻量调用(PLAN idi-02-02 Task 1,D-P2-8/D-P2-9/UI-02)
# ---------------------------------------------------------------------------


def test_build_plain_prompt_three_materials_and_rules():
    """用例 1:build_plain_prompt 三要素(当前文档全文、划选原文、用户问题)+ 红线 + 只解释不改设计。"""
    from backend.prompts import build_plain_prompt

    prompt = build_plain_prompt(
        "# 第 1 轮\n\n这里讲目标与边界。\n",
        "目标与边界",
        "这句到底什么意思?",
    )
    # 三要素齐备
    assert "这里讲目标与边界" in prompt          # ① 当前文档全文
    assert "目标与边界" in prompt                # ② 划选原文
    assert "这句到底什么意思" in prompt            # ③ 用户问题
    # §3.8 语言红线注入(引用 _LANGUAGE_RULES,非复制字面量)
    assert "简洁" in prompt and "大白话" in prompt
    # 「只解释,不改设计」指令
    assert "只解释" in prompt or "消歧" in prompt


def test_fake_ai_caller_ask_lite_records_and_returns():
    """用例 2:FakeAICaller.ask_lite 记录三元组;lite_answers 注入固定答;None 时默认固定答。"""
    fake = FakeAICaller()
    result = fake.ask_lite("文档全文A", "划选B", "问题C")
    assert result == {"answer": "测试即时答"}
    assert fake.lite_calls == [("文档全文A", "划选B", "问题C")]

    injected = FakeAICaller(lite_answers={"问题C": "注入的回答"})
    assert injected.ask_lite("文档全文A", "划选B", "问题C") == {"answer": "注入的回答"}
    # 未命中 question 键 → 默认固定答
    assert injected.ask_lite("x", "y", "别的问题") == {"answer": "测试即时答"}


def test_subprocess_ask_lite_argv_construction(monkeypatch):
    """用例 3a:SubprocessAICaller.ask_lite 参数组装级单测(不起真 CLI)。

    断言:argv 含 --setting-sources=、--tools ""(禁工具)、--append-system-prompt;
    prompt 来自 build_plain_prompt(三要素);产物不含文档读取/文件写指令。
    真 CLI 的 ask_lite 全链验证在 idi-02-04 的 IDI_E2E 门控用例(不在本计划)。
    """
    from backend.ai_caller import SubprocessAICaller

    captured_argv = []
    captured_input = []

    class FakeCompleted:
        returncode = 0
        stdout = (
            '{"type":"assistant","message":{"role":"assistant",'
            '"content":[{"type":"text","text":"我先看看。"}]}}\n'
            '{"type":"result","result":"大白话答案:这就是字面意思。"}\n'
        )
        stderr = ""

    def fake_run(argv, **kwargs):
        captured_argv.append(list(argv))
        captured_input.append(kwargs.get("input"))
        return FakeCompleted()

    monkeypatch.setattr("backend.ai_caller.subprocess.run", fake_run)
    caller = SubprocessAICaller()
    result = caller.ask_lite("文档全文A", "划选B", "问题C")

    assert result == {"answer": "大白话答案:这就是字面意思。"}
    argv = captured_argv[0]
    assert "--setting-sources=" in argv        # 屏蔽全局 allow(与 run() 同因)
    assert "--tools" in argv and "" in argv     # 禁全部内置工具(纯问答)
    assert "--append-system-prompt" in argv     # §3.8 红线注入
    # prompt 走 argv(captured_input None = 未触发 stdin 回退)
    assert captured_input[0] is None
    prompt_text = argv[argv.index("-p") + 1]
    assert "文档全文A" in prompt_text and "划选B" in prompt_text and "问题C" in prompt_text
    # 用例 4:纯问答——prompt 不含 docs/ 读取指令、不要求 AI 写任何文件
    assert "docs/" not in prompt_text
    assert "Write" not in prompt_text
    assert "不要读取其他文件" in prompt_text


def test_subprocess_ask_lite_error_no_result(monkeypatch):
    """用例 3b:stdout 无 result 行 → {"answer": "", "error": ...} 不抛。"""
    from backend.ai_caller import SubprocessAICaller

    class FakeCompleted:
        returncode = 0
        stdout = "不是 JSON 的普通输出\n"
        stderr = ""

    monkeypatch.setattr(
        "backend.ai_caller.subprocess.run",
        lambda argv, **kwargs: FakeCompleted(),
    )
    result = SubprocessAICaller().ask_lite("a", "b", "c")
    assert result["answer"] == ""
    assert "error" in result and result["error"]


def test_sdk_ask_lite_options_construction():
    """用例 3c:SdkAICaller ask_lite 的参数构造级单测(options 组装纯断言,不起真调用)。

    断言 SdkAICaller.ask_lite 存在且为同步方法(契约形态);对 4xx 路径的
    行为一致性(answer 空 + error)由 Task 3 路由用例经 Fake 打桩覆盖。
    """
    from backend.ai_caller import SdkAICaller

    caller = SdkAICaller()
    # 方法存在且同步(不是生成器/协程:双路线同契约,session.answer_plain 同步调)
    import inspect

    assert callable(caller.ask_lite)
    assert not inspect.iscoroutinefunction(caller.ask_lite)


# ---------------------------------------------------------------------------
# G2 处理流水线(PLAN idi-02-02 Task 2,FLOW-04)——七用例
# ---------------------------------------------------------------------------

# 合规第 N 轮文档样本(五件套齐;末行 = 合规授权申请标记)
def _round_doc_text(round_n: int, marker: str = "> 申请授权:否") -> str:
    return (
        f"# 第 {round_n} 轮讨论\n\n"
        "## 批注回应\n\n"
        "| 批注id | 原文摘录 | 回应 |\n"
        "|---|---|---|\n"
        "| a1-01 | 目标与边界 | 已补充说明边界范围。 |\n"
        "\n"
        "## 决策登记\n\n"
        "- D1:边界按补充后的版本执行。\n"
        "\n"
        "## 覆盖维度表\n\n"
        "| 维度 | 状态 | 说明 |\n"
        "|---|---|---|\n"
        "| 目标与边界 | ✓ | 已对齐 |\n"
        "\n"
        "## 未决问题清单\n\n"
        "| 编号 | 问题 | 状态 |\n"
        "|---|---|---|\n"
        "| 1 | 用户画像是否需要细化 | 待决 |\n"
        "\n"
        f"{marker}\n"
    )


class RoundWritingFake(FakeAICaller):
    """AI 在调用中写盘新轮文档(Write 工具语义:整体覆盖)。

    照 BrainstormWritingFake 同构;content 末行不合规时即"半成品"形态
    (is_complete_round 判不存在,derive_state 仍回原轮)。
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


def _enter_phase3(sess, tmp_path, round_text: str | None = "# 第 1 轮\n\n正文。\n\n> 申请授权:否\n"):
    """直造 phase3 目录:完整第 1 轮 + 进入项目;round_text=None 时不写轮文档。"""
    docs = tmp_path / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    if round_text is not None:
        (docs / "discuss-round-1.md").write_text(round_text, encoding="utf-8")
    sess.enter_project(tmp_path)
    return docs


def test_round_process_available(tmp_path, fresh_session):
    """用例 1:入口判定三态——phase3+完整轮 True;phase12_in_progress / phase1_new False。"""
    from backend.state import STATE_PHASE12_IN_PROGRESS, STATE_PHASE1_NEW, STATE_PHASE3

    # phase3:完整第 1 轮存在
    phase3_dir = tmp_path / "p3"
    (phase3_dir / "docs").mkdir(parents=True)
    (phase3_dir / "docs" / "discuss-round-1.md").write_text(
        "# 第 1 轮\n\n正文。\n\n> 申请授权:否\n", encoding="utf-8"
    )
    assert fresh_session.round_process_available(phase3_dir) is True

    # phase12_in_progress:有 docs/ 无完整轮
    phase12_dir = tmp_path / "p12"
    (phase12_dir / "docs").mkdir(parents=True)
    (phase12_dir / "docs" / "draft.md").write_text("# 雏形\n", encoding="utf-8")
    assert fresh_session.round_process_available(phase12_dir) is False

    # phase1_new:无 docs/
    phase1_dir = tmp_path / "p1"
    phase1_dir.mkdir()
    assert fresh_session.round_process_available(phase1_dir) is False

    # 半成品轮(末行非合规标记)→ 无完整轮 → False(derive_state 已判)
    half_dir = tmp_path / "half"
    (half_dir / "docs").mkdir(parents=True)
    (half_dir / "docs" / "discuss-round-1.md").write_text(
        "# 第 1 轮\n\n半成品,没写完\n", encoding="utf-8"
    )
    assert fresh_session.round_process_available(half_dir) is False


def test_process_round_prompt_contains(tmp_path, fresh_session):
    """用例 2:prompt 组装——当前轮文档全文、批注行、§3.3 四步、三表头原文、目标文件名。"""
    from backend import annotations as annotations_mod

    docs = _enter_phase3(fresh_session, tmp_path)
    annotations_mod.append_item(
        tmp_path, 1,
        quote="目标与边界", before="", type="comment", note="这里没看懂",
    )

    fake = RoundWritingFake(
        events=[{"kind": "say", "content": "我来处理批注。", "raw": None}],
        content=_round_doc_text(2),
    )
    fresh_session._set_caller_for_tests(fake)
    ok = fresh_session.process_round()
    assert ok is True, "phase3 当前轮应受理"
    assert wait_idle(fresh_session), "处理未在时限内结束"

    assert len(fake.run_calls) == 1
    _, prompt = fake.run_calls[0]
    # 当前轮文档全文
    assert "第 1 轮" in prompt and "正文" in prompt
    # 批注逐条(id/quote/note)
    assert "a1-01" in prompt
    assert "目标与边界" in prompt
    assert "这里没看懂" in prompt
    # §3.3 四步关键词
    assert "逐条回应" in prompt
    assert "已对齐" in prompt
    assert "未决清单" in prompt or "清单" in prompt
    # §6.4 三表头行原文(逐字)
    assert "| 批注id | 原文摘录 | 回应 |" in prompt
    assert "| 维度 | 状态 | 说明 |" in prompt
    assert "| 编号 | 问题 | 状态 |" in prompt
    # 标记行正例
    assert "> 申请授权:是" in prompt
    assert "> 申请授权:否" in prompt
    # 目标文件名(N+1:当前轮 1 → discuss-round-2.md)
    assert "docs/discuss-round-2.md" in prompt


def test_process_round_writeback(tmp_path, fresh_session):
    """用例 3:回写闭环——新轮文档含回应表(a1-01)→ a1-01 answered、a1-02 保持 pending、current_round 前进。"""
    from backend import annotations as annotations_mod

    docs = _enter_phase3(fresh_session, tmp_path)
    annotations_mod.append_item(
        tmp_path, 1,
        quote="目标与边界", before="", type="comment", note="这里没看懂",
    )
    annotations_mod.append_item(
        tmp_path, 1,
        quote="另一段", before="", type="comment", note="这里也没懂",
    )

    fake = RoundWritingFake(
        events=[{"kind": "say", "content": "处理批注中。", "raw": None}],
        content=_round_doc_text(2),  # 回应表只含 a1-01
    )
    fresh_session._set_caller_for_tests(fake)
    ok = fresh_session.process_round()
    assert ok is True
    assert wait_idle(fresh_session), "处理未在时限内结束"

    # 轮次前进:current_round 1 → 2
    state = fresh_session.snapshot()
    assert state["state"] == "phase3"
    assert state["current_round"] == 2

    # 回写:a1-01 answered + answer 有值;a1-02 保持 pending(answer None)
    obj = annotations_mod.load(tmp_path, 1)
    items = {item["id"]: item for item in obj["items"]}
    assert items["a1-01"]["status"] == "answered"
    assert items["a1-01"]["answer"]
    assert "边界" in items["a1-01"]["answer"]
    assert items["a1-02"]["status"] == "pending"
    assert items["a1-02"]["answer"] is None

    # done 收尾事件只有一条 kind=done 进 broker(事件照常直播;回写不发第二条)
    # (此处只验证流水线正常收尾——事件数断言在 published 观察器版本)
    assert not fresh_session.busy()


def test_process_round_incomplete_new_round(tmp_path, fresh_session):
    """用例 4:半成品——新文档末行非合规标记 → current_round 不变、批注未动、可重跑。"""
    from backend import annotations as annotations_mod

    docs = _enter_phase3(fresh_session, tmp_path)
    annotations_mod.append_item(
        tmp_path, 1,
        quote="目标与边界", before="", type="comment", note="这里没看懂",
    )

    # 新文档末行不合规(缺授权申请标记)→ 半成品
    fake = RoundWritingFake(
        events=[{"kind": "say", "content": "写废了。", "raw": None}],
        content=(_round_doc_text(2) + "后面还没写完\n"),
    )
    fresh_session._set_caller_for_tests(fake)
    ok = fresh_session.process_round()
    assert ok is True
    assert wait_idle(fresh_session), "处理未在时限内结束"

    # current_round 仍为 1(半成品视为不存在)
    state = fresh_session.snapshot()
    assert state["state"] == "phase3"
    assert state["current_round"] == 1

    # 上一轮批注未被回写(a1-01 保持 pending)
    obj = annotations_mod.load(tmp_path, 1)
    assert obj["items"][0]["status"] == "pending"
    assert obj["items"][0]["answer"] is None

    # 可重跑受理(重跑覆盖语义:入口仍开)
    fake2 = RoundWritingFake(
        events=[{"kind": "say", "content": "重来。", "raw": None}],
        content=_round_doc_text(2),
    )
    fresh_session._set_caller_for_tests(fake2)
    ok2 = fresh_session.process_round()
    assert ok2 is True, "半成品后重跑应被受理"
    assert wait_idle(fresh_session), "重跑未在时限内结束"
    state2 = fresh_session.snapshot()
    assert state2["current_round"] == 2, "重跑产物合规后轮次前进"
    obj2 = annotations_mod.load(tmp_path, 1)
    assert obj2["items"][0]["status"] == "answered", "重跑后批注被回写"


def test_process_round_busy_rejects(tmp_path, fresh_session):
    """用例 5:在飞拒绝——HangingFake 挂住在飞主调用 → process_round 返回 False。"""
    docs = _enter_phase3(fresh_session, tmp_path)

    gate = threading.Event()
    release = threading.Event()

    class HangingFake(FakeAICaller):
        def run(self, project_path, prompt):
            self.run_calls.append((str(project_path), prompt))
            gate.set()
            release.wait(timeout=10)  # 模拟调用在飞
            yield {"kind": "done", "content": "调用结束", "raw": None}

    fake = HangingFake(events=[])
    fresh_session._set_caller_for_tests(fake)
    threading.Thread(target=lambda: fresh_session.send_message("先聊"), daemon=True).start()
    assert gate.wait(timeout=5), "在飞调用未启动"

    # 在飞中触发处理本轮批注 → 单飞锁拒绝
    accepted = fresh_session.process_round()
    assert accepted is False, "在飞中 process_round 应被拒绝(单飞)"

    release.set()
    assert wait_idle(fresh_session), "调用未收尾"
    assert len(fake.run_calls) == 1, "process_round 不应另起调用"


def test_process_round_non_phase3_rejects(tmp_path, fresh_session):
    """用例 6:非 phase3 拒绝——phase12 目录直接调 process_round → False(入口校验)。"""
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "transcript.md").write_text("", encoding="utf-8")
    (docs / "draft.md").write_text("# 雏形\n", encoding="utf-8")
    fresh_session.enter_project(tmp_path)

    accepted = fresh_session.process_round()
    assert accepted is False, "非 phase3 时 process_round 应被拒绝"


def test_process_round_empty_annotations_ok(tmp_path, fresh_session):
    """用例 7:空批注轮合法——零 annotations 时照常受理 + prompt 含「当前轮暂无待处理批注」。"""
    docs = _enter_phase3(fresh_session, tmp_path)  # 不建任何批注

    fake = RoundWritingFake(
        events=[{"kind": "say", "content": "本轮无批注,直接更新文档。", "raw": None}],
        content=_round_doc_text(2),
    )
    fresh_session._set_caller_for_tests(fake)
    ok = fresh_session.process_round()
    assert ok is True, "空批注轮也应受理(D-P2-15:不设「有批注才可处理」门槛)"
    assert wait_idle(fresh_session), "处理未在时限内结束"

    _, prompt = fake.run_calls[0]
    assert "当前轮暂无待处理批注" in prompt
    # 轮次照常前进 + done 正常收尾
    state = fresh_session.snapshot()
    assert state["current_round"] == 2


# ---------------------------------------------------------------------------
# answer_plain 同步封装 / add_annotation(PLAN idi-02-02 Task 3,D-P2-7/D-P2-10)
# ---------------------------------------------------------------------------


def test_answer_plain_records_and_persists(tmp_path, fresh_session):
    """用例 1:answer_plain 同步调 ask_lite → lite_calls 记录三元组 → plain 落盘 answered。"""
    from backend import annotations as annotations_mod

    docs = _enter_phase3(fresh_session, tmp_path)

    fake = FakeAICaller(lite_answers={"这段什么意思": "即时答:字面意思即可。"})
    fresh_session._set_caller_for_tests(fake)

    # 观察事件:answer_plain 不 publish 任何 SSE 事件(D-P2-8:不进工作面板)
    published = []
    orig_publish = fresh_session._publish_for_tests
    fresh_session._publish_for_tests = lambda ev: published.append(ev)

    entry = fresh_session.answer_plain(
        1, quote="目标与边界", before="第 1 轮", question="这段什么意思"
    )

    #FakeAICaller 未走 run → 不 publish;直接断言无事件
    assert published == [], "answer_plain 不应发 SSE 事件"

    # ask_lite 记录了三元组(当前文档全文 / 划选原文 / 用户问题)
    assert len(fake.lite_calls) == 1
    document_text, quoted_text, question = fake.lite_calls[0]
    assert "第 1 轮" in document_text  # 当前轮文档全文进 payload
    assert quoted_text == "目标与边界"
    assert question == "这段什么意思"

    # 落盘条目:type=plain、status=answered、answer 有值
    assert entry["type"] == "plain"
    assert entry["status"] == "answered"
    assert entry["answer"] == "即时答:字面意思即可。"
    persisted = annotations_mod.load(tmp_path, 1)
    assert persisted["items"], "plain 条目应已落盘"
    assert persisted["items"][-1]["id"] == entry["id"]

    # plain 不计 pending(快照 pending_annotations 只数 comment+pending,D-P2-15)
    snap = fresh_session.snapshot()
    assert snap["pending_annotations"] == 0


def test_answer_plain_busy_rejects(tmp_path, fresh_session):
    """在飞主调用进行中再发起大白话 → 拒绝(RuntimeError,路由层 409 语义)。"""
    docs = _enter_phase3(fresh_session, tmp_path)

    gate = threading.Event()
    release = threading.Event()

    class HangingFake(FakeAICaller):
        def run(self, project_path, prompt):
            self.run_calls.append((str(project_path), prompt))
            gate.set()
            release.wait(timeout=10)
            yield {"kind": "done", "content": "调用结束", "raw": None}

    fake = HangingFake(events=[])
    fresh_session._set_caller_for_tests(fake)
    threading.Thread(target=lambda: fresh_session.send_message("先聊"), daemon=True).start()
    assert gate.wait(timeout=5), "在飞调用未启动"

    with pytest.raises(RuntimeError, match="在飞|进行中"):
        fresh_session.answer_plain(1, quote="x", before="", question="y")

    release.set()
    assert wait_idle(fresh_session), "调用未收尾"


def test_add_annotation_creates_pending_comment(tmp_path, fresh_session):
    """用例 2(session 侧):add_annotation 建条目落盘(pending + comment)。"""
    from backend import annotations as annotations_mod

    docs = _enter_phase3(fresh_session, tmp_path)

    entry = fresh_session.add_annotation(1, "目标与边界", "第 1 轮", "这里没看懂")
    assert entry["type"] == "comment"
    assert entry["status"] == "pending"
    assert entry["answer"] is None

    # 非当前轮 → RuntimeError(路由层 409)
    with pytest.raises(RuntimeError, match="仅当前轮可批注"):
        fresh_session.add_annotation(2, "x", "", "y")

    # 计数:1 条 pending comment → snapshot pending_annotations == 1
    snap = fresh_session.snapshot()
    assert snap["pending_annotations"] == 1


# ---------------------------------------------------------------------------
# G3 授权 + 选档/裁决同步三件 + 撰写流水线(PLAN idi-03-02 Task 1,
# FLOW-05 / DATA-02 / DATA-04 / D-P3-4 ~ D-P3-11)
# ---------------------------------------------------------------------------


def _compliant_round_doc(marker: str = "> 申请授权:是") -> str:
    """四查合规轮文档样本:维度全绿 + 清单清零 + 申请授权「是」+ 末行标记。"""
    return (
        "# 第 1 轮讨论\n\n"
        "## 批注回应\n\n"
        "| 批注id | 原文摘录 | 回应 |\n"
        "|---|---|---|\n"
        "| a1-01 | 目标与边界 | 已补充说明。 |\n"
        "\n"
        "## 决策登记\n\n"
        "- D1:目标与边界已对齐。\n"
        "\n"
        "## 覆盖维度表\n\n"
        "| 维度 | 状态 | 说明 |\n"
        "|---|---|---|\n"
        "| 目标与边界 | ✓ | 已对齐 |\n"
        "\n"
        "## 未决问题清单\n\n"
        "| 编号 | 问题 | 状态 |\n"
        "|---|---|---|\n"
        "| 1 | 用户画像是否细化 | 已决 |\n"
        "\n"
        f"{marker}\n"
    )


def _enter_phase3_compliant(sess, tmp_path, marker: str = "> 申请授权:是"):
    """直造四查合规 phase3 目录:完整合规第 1 轮 + 进入项目(无 pending 批注)。"""
    docs = tmp_path / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "discuss-round-1.md").write_text(
        _compliant_round_doc(marker), encoding="utf-8"
    )
    sess.enter_project(tmp_path)
    return docs


def _enter_phase4(sess, tmp_path, tmp_text: str | None = None):
    """直造 phase4 目录:完整轮 + AUTHORIZATION.md(无 DESIGN.md)+ 进入项目。

    tmp_text 非 None 时同时写 DESIGN.md.tmp(半份残留形态,D-P3-9)。"""
    docs = _enter_phase3_compliant(sess, tmp_path)
    (tmp_path / "AUTHORIZATION.md").write_text(
        "# 授权记录\n\n- 操作者确认词:确认授权\n", encoding="utf-8"
    )
    if tmp_text is not None:
        (tmp_path / "DESIGN.md.tmp").write_text(tmp_text, encoding="utf-8")
    return docs


def _enter_phase5(sess, tmp_path, design_text: str = "# 总设计文档\n\n正文。\n",
                  check_reports: dict | None = None, tier: str | None = None):
    """直造阶段 5 目录:完整轮 + AUTHORIZATION.md + DESIGN.md + 可选 check 报告族。"""
    docs = _enter_phase4(sess, tmp_path)
    (tmp_path / "DESIGN.md").write_text(design_text, encoding="utf-8")
    for n, text in (check_reports or {}).items():
        (docs / f"DESIGN-check-{n}.md").write_text(text, encoding="utf-8")
    if tier is not None:
        (docs / "DESIGN-check-tier.md").write_text(
            f"> 自检档位:{tier}\n", encoding="utf-8"
        )
    return docs


class WritingFake(FakeAICaller):
    """AI 在撰写调用中写盘 DESIGN.md.tmp(Write 工具语义:整体覆盖)。

    照 RoundWritingFake 同构;content=None 时模拟 AI 没写 tmp 的失败形态。
    """

    def __init__(self, events, content: str | None):
        super().__init__(events=events)
        self.content = content

    def run(self, project_path, prompt: str):
        self.run_calls.append((str(project_path), prompt))
        if self.content is not None:
            (Path(project_path) / "DESIGN.md.tmp").write_text(
                self.content, encoding="utf-8"
            )
        for ev in list(self.events):
            yield dict(ev)
        yield {"kind": "done", "content": "调用结束", "raw": None}


def test_authorize_accepts_and_persists(tmp_path, fresh_session):
    """用例 1:authorize 受理——四查合规 phase3 → AUTHORIZATION.md 落盘 → 幂等 False。"""
    from backend.g3 import AUTHORIZATION_FILENAME

    _enter_phase3_compliant(fresh_session, tmp_path)
    assert fresh_session.authorize() is True
    auth_path = tmp_path / AUTHORIZATION_FILENAME
    assert auth_path.is_file(), "AUTHORIZATION.md 应已落盘"
    assert "确认授权" in auth_path.read_text(encoding="utf-8")
    # 落盘后 derive_state → phase4(授权链走通)
    assert fresh_session.snapshot()["state"] == "phase4"

    # 再次 authorize → False(已授权,幂等;derive_state 已 != phase3)
    assert fresh_session.authorize() is False


def test_authorize_rejects_on_four_checks(tmp_path, fresh_session):
    """用例 2:四查防绕过——维度表含 ◐ → False;未进项目 → RuntimeError。"""
    # 维度污染:◐ 行 → g3_available False → authorize False
    docs = tmp_path / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    polluted = _compliant_round_doc().replace(
        "| 目标与边界 | ✓ | 已对齐 |", "| 目标与边界 | ◐ | 未对齐 |"
    )
    (docs / "discuss-round-1.md").write_text(polluted, encoding="utf-8")
    fresh_session.enter_project(tmp_path)
    assert fresh_session.authorize() is False, "维度 ◐ 污染盘应拒绝授权"
    assert not (tmp_path / "AUTHORIZATION.md").exists()

    # 未进入项目 → RuntimeError(路由层 400)
    session._reset_for_tests()
    with pytest.raises(RuntimeError, match="尚未进入任何项目"):
        fresh_session.authorize()


def test_set_tier_accepts_and_rejects(tmp_path, fresh_session):
    """用例 3:set_tier——phase5_awaiting_tier 落盘签名;非该态 RuntimeError;白名单外 ValueError。"""
    from backend.checks import TIER_FILENAME

    # phase5_awaiting_tier:有 DESIGN.md 无 check 报告
    _enter_phase5(fresh_session, tmp_path)
    assert fresh_session.set_tier("严格") is True
    tier_path = tmp_path / "docs" / TIER_FILENAME
    assert tier_path.is_file()
    assert "> 自检档位:严格" in tier_path.read_text(encoding="utf-8")
    # 同值覆盖幂等合法
    assert fresh_session.set_tier("严格") is True

    # 白名单外 → ValueError(路由层 400)
    with pytest.raises(ValueError, match="档位"):
        fresh_session.set_tier("超严格")

    # 非 phase5_awaiting_tier(全新 phase3 目录)→ RuntimeError(路由层 409)
    session._reset_for_tests()
    _other = tmp_path / "other-project"
    _enter_phase3_compliant(fresh_session, _other)
    with pytest.raises(RuntimeError, match="仅待选档阶段可选"):
        fresh_session.set_tier("宽松")


def test_verdict_append_persists_and_closes(tmp_path, fresh_session):
    """用例 4:verdict_append——追加 `> 裁决:#1:修——按建议`;残余清零 → PASS 收口;同号 FileExistsError。"""
    # phase5_checking:check-1 报告含待裁决 #1(结论行之后)无配对
    report = (
        "# 核查报告 1\n\n"
        "> 自检档位:严格\n\n"
        "## 问题分级\n\n"
        "| 编号 | 级别 | 位置 | 问题 | 建议修法 |\n"
        "|---|---|---|---|---|\n"
        "| 1 | P1 | §2 | 范围含糊 | 写清边界 |\n"
        "\n"
        "> 核查结论:FIX(P1×1)\n\n"
        "> 待裁决:#1:范围要不要收紧?\n"
    )
    _enter_phase5(
        fresh_session, tmp_path,
        check_reports={1: report}, tier="严格",
    )
    assert fresh_session.verdict_append(1, "修", "按建议") is True
    text = (tmp_path / "docs" / "DESIGN-check-1.md").read_text(encoding="utf-8")
    assert "> 裁决:#1:修——按建议" in text

    # 残余清零(问题表 #1 已有同号裁决 + 无未配对)→ PASS 收口 → mission_complete
    assert "> 核查结论:PASS(残余裁决收口)" in text
    assert fresh_session.snapshot()["state"] == "mission_complete"

    # 收口后再裁决(非 phase5_checking)→ RuntimeError「仅自检进行中可裁决」
    # (路由层 409:同号拒绝被入口门先拦,同样是 409)
    with pytest.raises(RuntimeError, match="仅自检进行中可裁决"):
        fresh_session.verdict_append(1, "又修", "重复")


def test_verdict_append_same_number_rejects(tmp_path, fresh_session):
    """用例 4b:同号 FileExistsError——双待裁决盘,#1 裁决后 #2 仍配对缺口(不收口),
    状态留 phase5_checking;重复裁决 #1 → FileExistsError 冒出供路由 409。"""
    report = (
        "# 核查报告 1\n\n"
        "> 自检档位:严格\n\n"
        "## 问题分级\n\n"
        "| 编号 | 级别 | 位置 | 问题 | 建议修法 |\n"
        "|---|---|---|---|---|\n"
        "| 1 | P1 | §2 | 范围含糊 | 写清边界 |\n"
        "| 2 | P1 | §4 | 措辞歧义 | 直说 |\n"
        "\n"
        "> 核查结论:FIX(P1×2)\n\n"
        "> 待裁决:#1:范围要不要收紧?\n"
        "> 待裁决:#2:第 4 节是否重写?\n"
    )
    _enter_phase5(
        fresh_session, tmp_path,
        check_reports={1: report}, tier="严格",
    )
    # 裁决 #1:#2 仍无同号裁决 → _residue_cleared False → 不收口
    assert fresh_session.verdict_append(1, "修", "按建议") is True
    text = (tmp_path / "docs" / "DESIGN-check-1.md").read_text(encoding="utf-8")
    assert "> 裁决:#1:修——按建议" in text
    assert "> 核查结论:PASS" not in text.split("> 核查结论:FIX")[1].split("\n")[0], \
        "PASS 收口行不应出现(#2 仍未配对)"
    assert fresh_session.snapshot()["state"] == "phase5_checking"

    # 同号重复裁决 → FileExistsError(checks.append_user_verdict 冒出,路由层 409)
    with pytest.raises(FileExistsError):
        fresh_session.verdict_append(1, "再修", "重复")


def test_start_writing_closes_loop(tmp_path, fresh_session):
    """用例 5:撰写闭环——WritingFake 写 tmp → done 后 tmp 消失、DESIGN.md 出现、state=phase5_awaiting_tier。"""
    _enter_phase4(fresh_session, tmp_path)
    fake = WritingFake(
        events=[{"kind": "say", "content": "开始撰写。", "raw": None}],
        content="# 总设计文档\n\n七维度全覆盖。\n",
    )
    fresh_session._set_caller_for_tests(fake)
    assert fresh_session.start_writing() is True
    assert wait_idle(fresh_session), "撰写未在时限内结束"

    assert (tmp_path / "DESIGN.md").is_file(), "tmp 应已改名为 DESIGN.md"
    assert not (tmp_path / "DESIGN.md.tmp").exists(), "tmp 应消失"
    assert "# 总设计文档" in (tmp_path / "DESIGN.md").read_text(encoding="utf-8")
    snap = fresh_session.snapshot()
    assert snap["state"] == "phase5_awaiting_tier"


def test_start_writing_error_when_no_tmp(tmp_path, fresh_session):
    """用例 6:tmp 缺失——error 事件含「撰写未产出 tmp」、状态留 phase4、可重跑。"""
    _enter_phase4(fresh_session, tmp_path)

    published = []
    orig_publish = fresh_session._publish_for_tests
    fresh_session._publish_for_tests = lambda ev: published.append(ev)

    fake = WritingFake(events=[], content=None)  # AI 没写 tmp
    fresh_session._set_caller_for_tests(fake)
    assert fresh_session.start_writing() is True
    assert wait_idle(fresh_session), "撰写未在时限内结束"

    errors = [ev for ev in published if ev.get("kind") == "error"]
    assert any("撰写未产出 tmp" in ev.get("content", "") for ev in errors), \
        "应发「撰写未产出 tmp,可重跑」error 事件"
    assert not (tmp_path / "DESIGN.md").exists()
    assert fresh_session.snapshot()["state"] == "phase4"

    # 可重跑:重进 fake 写 tmp → 闭环成功
    fresh_session._publish_for_tests = orig_publish
    fake2 = WritingFake(events=[], content="# 总设计文档\n\n重跑产物。\n")
    fresh_session._set_caller_for_tests(fake2)
    assert fresh_session.start_writing() is True, "phase4 应可重跑"
    assert wait_idle(fresh_session)
    assert (tmp_path / "DESIGN.md").is_file()


def test_start_writing_entry_rejects(tmp_path, fresh_session):
    """用例 7:入口拒绝——phase3 → False;busy 在飞 → False。"""
    _enter_phase3_compliant(fresh_session, tmp_path)
    assert fresh_session.writing_available(tmp_path) is False
    assert fresh_session.start_writing() is False, "phase3 不应受理撰写"

    # busy:挂住在飞主调用 → start_writing False
    _enter_phase4(fresh_session, tmp_path)

    gate = threading.Event()
    release = threading.Event()

    class HangingFake(FakeAICaller):
        def run(self, project_path, prompt):
            self.run_calls.append((str(project_path), prompt))
            gate.set()
            release.wait(timeout=10)
            yield {"kind": "done", "content": "调用结束", "raw": None}

    fake = HangingFake(events=[])
    fresh_session._set_caller_for_tests(fake)
    threading.Thread(target=lambda: fresh_session.send_message("先聊"), daemon=True).start()
    assert gate.wait(timeout=5), "在飞调用未启动"

    assert fresh_session.start_writing() is False, "在飞中不应受理撰写"
    assert len(fake.run_calls) == 1, "start_writing 不应另起调用"

    release.set()
    assert wait_idle(fresh_session), "调用未收尾"


def test_build_writing_prompt_contains_materials(tmp_path, fresh_session):
    """用例 8:build_writing_prompt 产物——完整轮文档正文 + 批注逐条 + transcript 片段
    + DESIGN.md.tmp 落盘指令 + 明禁直写语句 + 语言红线。"""
    from backend.prompts import build_writing_prompt

    docs = _enter_phase3_compliant(fresh_session, tmp_path)
    from backend import annotations as annotations_mod

    annotations_mod.append_item(
        tmp_path, 1,
        quote="目标与边界", before="", type="comment", note="写清边界",
    )
    (docs / "transcript.md").write_text(
        "[user] 帮我把目标写清楚\n[ai] 已经写清\n", encoding="utf-8"
    )
    (tmp_path / "DESIGN.md.tmp").write_text(
        "半份残留不该进资料段", encoding="utf-8"
    )
    (tmp_path / "AUTHORIZATION.md").write_text(
        "# 授权记录\n", encoding="utf-8"
    )

    prompt = build_writing_prompt(tmp_path)
    # 全部完整轮文档正文片段
    assert "第 1 轮讨论" in prompt
    # annotations 逐条(id/quote/note)
    assert "目标与边界" in prompt
    assert "写清边界" in prompt
    # transcript 片段
    assert "帮我把目标写清楚" in prompt
    # DESIGN.md.tmp 落盘指令
    assert "DESIGN.md.tmp" in prompt
    # 明禁直写 DESIGN.md / AUTHORIZATION.md
    assert "绝不直接写 DESIGN.md 或 AUTHORIZATION.md" in prompt
    # 语言红线
    assert "简洁" in prompt and "大白话" in prompt


def test_build_writing_prompt_excludes_tmp_and_auth(tmp_path, fresh_session):
    """用例 9:资料隔离——半份 DESIGN.md.tmp 与 AUTHORIZATION.md 内容不入资料段。"""
    from backend.prompts import build_writing_prompt

    docs = _enter_phase3_compliant(fresh_session, tmp_path)
    (tmp_path / "DESIGN.md.tmp").write_text(
        "HALF-TMP-MARKER 半份内容不应出现", encoding="utf-8"
    )
    (tmp_path / "AUTHORIZATION.md").write_text(
        "AUTH-MARKER 授权记录不应出现", encoding="utf-8"
    )

    prompt = build_writing_prompt(tmp_path)
    assert "HALF-TMP-MARKER" not in prompt, "半份 tmp 内容不得进资料段(D-P3-9)"
    assert "AUTH-MARKER" not in prompt, "AUTHORIZATION.md 内容不得进资料段"


# ---------------------------------------------------------------------------
# 阶段 5 两角色循环引擎(PLAN idi-03-02 Task 2 / DATA-04 / §8.2 /
# D-P3-13 ~ D-P3-22:check→repair→check-2 两跳自动驱动 Fake 级全链)
# ---------------------------------------------------------------------------


def _check_report(tier: str = "严格", problems: list[tuple] | None = None,
                  conclusion: str = "> 核查结论:FIX(P1×1)",
                  pending_questions: list[tuple] | None = None,
                  verdict_lines: list[tuple] | None = None) -> str:
    """手造核查报告样本(文法与 grammar 解析器一字不差)。

    problems = [(number, level, location, issue, suggestion)];
    pending_questions = [(number, text)] → `> 待裁决:#K:…`;
    verdict_lines = [(number, decision_text)] → `> 裁决:#K:…`(结论行之后)。
    """
    lines = [f"# 核查报告\n\n> 自检档位:{tier}\n\n## 问题分级\n\n"]
    if problems:
        lines.append("| 编号 | 级别 | 位置 | 问题 | 建议修法 |\n")
        lines.append("|---|---|---|---|---|\n")
        for n, level, loc, issue, sug in problems:
            lines.append(f"| {n} | {level} | {loc} | {issue} | {sug} |\n")
    lines.append(f"\n{conclusion}\n")
    if pending_questions or verdict_lines:
        lines.append("\n")
        for n, text in pending_questions or []:
            lines.append(f"> 待裁决:#{n}:{text}\n")
        for n, text in verdict_lines or []:
            lines.append(f"> 裁决:#{n}:{text}\n")
    return "".join(lines)


def _target_check_n(prompt: str) -> int:
    """从 check prompt 的落盘指令解析目标报告编号(docs/DESIGN-check-N.md,
    编号由任务方给出,勿自定)——取「写入 docs/DESIGN-check-」而非资料段的
    既有报告标题,防把资料段文件名误当目标。"""
    import re as _re

    m = _re.search(r"写入 docs/DESIGN-check-(\d+)\.md", prompt)
    return int(m.group(1)) if m else 0


class CheckWritingFake(FakeAICaller):
    """核查执行者 fake:per-call 脚本(每次 run 消费一个 spec)写 check 报告。

    specs = [report_text_1, report_text_2, ...](报告文法样本——含/不含
    结论行、P1/P2 分级由样本控制);调用次数超脚本 → AssertionError。
    """

    def __init__(self, specs: list[str]):
        super().__init__(events=[])
        self.specs = list(specs)
        self.reports_written: list[int] = []

    def run(self, project_path, prompt: str):
        self.run_calls.append((str(project_path), prompt))
        if not self.specs:
            raise AssertionError("CheckWritingFake 脚本耗尽(超出预期的核查跳数)")
        report = self.specs.pop(0)
        n = _target_check_n(prompt) or len(self.reports_written) + 1
        docs_dir = Path(project_path) / "docs"
        docs_dir.mkdir(parents=True, exist_ok=True)
        (docs_dir / f"DESIGN-check-{n}.md").write_text(report, encoding="utf-8")
        self.reports_written.append(n)
        yield {"kind": "say", "content": f"核查第 {n} 轮完成。", "raw": None}
        yield {"kind": "done", "content": "调用结束", "raw": None}


class RepairWritingFake(FakeAICaller):
    """修复者 fake:per-call 脚本写 DESIGN.md.tmp(tmp_prefill 先置盘);

    pending_lines 非 None 时在 say 事件流文本含 `> 待裁决:#K:…` 行
    (抛问形态,D-P3-18);say_texts 可额外注入。计数 repair_calls。
    """

    def __init__(self, tmp_content: str | None = "# 总设计文档\n\n修复后版本。\n",
                 pending_lines: list[str] | None = None):
        super().__init__(events=[])
        self.tmp_content = tmp_content
        self.pending_lines = pending_lines
        self.repair_calls: list[tuple[str, str]] = []

    def run(self, project_path, prompt: str):
        self.repair_calls.append((str(project_path), prompt))
        if self.tmp_content is not None:
            (Path(project_path) / "DESIGN.md.tmp").write_text(
                self.tmp_content, encoding="utf-8"
            )
        if self.pending_lines:
            for line in self.pending_lines:
                yield {"kind": "say", "content": line, "raw": None}
        yield {"kind": "done", "content": "调用结束", "raw": None}


class DualRoleFake:
    """单 caller 两角色双队列 fake:session._ensure_caller 复用同一 caller,
    check 与 repair 按调用顺序分别从 check_specs / repair_specs 消费
    (谁先被调谁出队;真实链路 check 先 repair 后,由 prompt 内容区分)。

    分派依据:prompt 含「核查执行者」→ check 脚本;含「修复引擎」→ repair 脚本。
    """

    def __init__(self, check_specs: list[str], repair_specs: list["RepairWritingFake"]):
        self.check_specs = list(check_specs)
        self.repair_specs = list(repair_specs)
        self.check_calls: list[str] = []
        self.repair_calls: list[str] = []
        self.request_permission = None

    def run(self, project_path, prompt: str):
        if "核查执行者" in prompt:
            self.check_calls.append(prompt)
            report = self.check_specs.pop(0)
            n = _target_check_n(prompt) or len(self.check_calls)
            docs_dir = Path(project_path) / "docs"
            docs_dir.mkdir(parents=True, exist_ok=True)
            (docs_dir / f"DESIGN-check-{n}.md").write_text(report, encoding="utf-8")
            yield {"kind": "say", "content": f"核查第 {n} 轮完成。", "raw": None}
        else:
            repair = self.repair_specs.pop(0)
            self.repair_calls.append(prompt)
            repair.repair_calls.append((str(project_path), prompt))
            if repair.tmp_content is not None:
                (Path(project_path) / "DESIGN.md.tmp").write_text(
                    repair.tmp_content, encoding="utf-8"
                )
            if repair.pending_lines:
                for line in repair.pending_lines:
                    yield {"kind": "say", "content": line, "raw": None}
            yield {"kind": "say", "content": "修复完成。", "raw": None}
        yield {"kind": "done", "content": "调用结束", "raw": None}


def _wait_chain_idle(sess, timeout: float = 15.0) -> bool:
    """等两跳链彻底收尾(busy 可能在两跳间瞬时翻转,轮询到持续空闲)。"""
    import time as _time

    deadline = _time.time() + timeout
    while _time.time() < deadline:
        if not sess.busy():
            # 再观察一小段:链式驱动可能正在解锁→下一跳窗口
            _time.sleep(0.15)
            if not sess.busy():
                return True
        _time.sleep(0.05)
    return not sess.busy()


def test_build_check_prompt_three_sections(tmp_path, fresh_session):
    """用例 1:build_check_prompt 三段——DESIGN.md 全文 + tier 头部行正例(TIER_LINE 常量字面)
    + 问题表头逐字 + 结论行文法(PASS 正例与 FIX)+ 目标文件名 + 干净的眼睛 + 明禁 + 红线。"""
    from backend.grammar import TIER_LINE_STRICT, TIER_LINE_LOOSE
    from backend.prompts import build_check_prompt

    docs = _enter_phase5(fresh_session, tmp_path)
    (docs / "DESIGN-check-1.md").write_text(
        _check_report(problems=[(1, "P1", "§2", "范围含糊", "写清")],
                      conclusion="> 核查结论:FIX(P1×1)"),
        encoding="utf-8",
    )

    prompt = build_check_prompt(tmp_path, 2, "严格")
    # DESIGN.md 全文片段
    assert "# 总设计文档" in prompt
    # tier 头部行正例(TIER_LINE 常量字面,逐字)
    assert TIER_LINE_STRICT in prompt
    assert TIER_LINE_LOOSE in prompt
    # 问题表头逐字
    assert "| 编号 | 级别 | 位置 | 问题 | 建议修法 |" in prompt
    # 结论行文法(PASS 正例与 FIX 反例均在)
    assert "> 核查结论:PASS" in prompt
    assert "> 核查结论:FIX(" in prompt
    # 目标文件名(n 参数注入)
    assert "docs/DESIGN-check-2.md" in prompt
    # 干净的眼睛角色句 + 绝不修改 DESIGN.md 明禁
    assert "干净的眼睛" in prompt
    assert "绝不修改 DESIGN.md" in prompt
    # 语言红线
    assert "简洁" in prompt and "大白话" in prompt


def test_build_check_prompt_injects_tier_line(tmp_path, fresh_session):
    """用例 1b:本轮档位头部行逐字注入任务段(真 CLI E2E 发现的缺陷回归)。

    缺陷形态:build_check_prompt 收 tier 参数但从未注入任务段——文法模板
    同时含两档正例且标注「档位由任务方给定」,AI 无从得知该写哪一行(真机
    观测:AI 写出 `自检档位:严格`,既缺 `> ` 前缀又选错档位,parse_tier_line
    返回 None)。修复 = 任务段落盘指令逐字注入本轮 tier_line。
    """
    from backend.grammar import TIER_LINE_LOOSE, TIER_LINE_STRICT
    from backend.prompts import build_check_prompt

    _enter_phase5(fresh_session, tmp_path)

    loose_prompt = build_check_prompt(tmp_path, 1, "宽松")
    # 任务段须含本轮档位行逐字(且明确「必须逐字写」)
    assert "必须逐字写:" + TIER_LINE_LOOSE in loose_prompt, (
        "宽松档 prompt 未逐字注入档位头部行(AI 无从得知该写哪一行)"
    )

    strict_prompt = build_check_prompt(tmp_path, 1, "严格")
    assert "必须逐字写:" + TIER_LINE_STRICT in strict_prompt, (
        "严格档 prompt 未逐字注入档位头部行"
    )


def test_build_check_prompt_multi_round_trend(tmp_path, fresh_session):
    """用例 2:多轮趋势照读——已有 check-1 时 prompt 资料段含 check-1 全文。"""
    from backend.prompts import build_check_prompt

    docs = _enter_phase5(fresh_session, tmp_path)
    report1 = _check_report(
        problems=[(1, "P1", "§2", "范围含糊", "写清")],
        conclusion="> 核查结论:FIX(P1×1)",
    )
    (docs / "DESIGN-check-1.md").write_text(report1, encoding="utf-8")

    prompt = build_check_prompt(tmp_path, 2, "严格")
    assert "范围含糊" in prompt, "既有 check-1 报告全文应进资料段(趋势照读)"
    assert "### 既有核查报告:docs/DESIGN-check-1.md(全文)" in prompt


def test_build_repair_prompt_contains(tmp_path, fresh_session):
    """用例 3:build_repair_prompt——最新报告全文 + 抛问协议 + tmp 落盘纪律 + DESIGN.md 全文。"""
    from backend.prompts import build_repair_prompt

    docs = _enter_phase5(fresh_session, tmp_path)
    report1 = _check_report(
        problems=[(1, "P1", "§2", "范围含糊", "写清")],
        conclusion="> 核查结论:FIX(P1×1)",
        pending_questions=[(1, "范围要不要收紧?")],
        verdict_lines=[(1, "修——按建议")],
    )
    (docs / "DESIGN-check-1.md").write_text(report1, encoding="utf-8")

    prompt = build_repair_prompt(tmp_path, 1, "严格")
    # DESIGN.md 全文
    assert "# 总设计文档" in prompt
    # 最新报告全文(含裁决行)
    assert "范围要不要收紧" in prompt
    assert "> 裁决:#1:修——按建议" in prompt
    # `> 待裁决:#K:` 抛问协议说明
    assert "> 待裁决:#K:" in prompt
    # tmp 落盘纪律
    assert "DESIGN.md.tmp" in prompt
    assert "绝不直接写 DESIGN.md" in prompt


def test_start_check_two_hop_chain(tmp_path, fresh_session):
    """用例 4(核心):严格档两跳自动驱动全链——check-1(P1)→ repair(1 次)
    → check-2(纯 P2)→ 停在残余裁决态;2 份报告、1 次修复。"""
    state = _enter_phase5(
        fresh_session, tmp_path,
        check_reports={}, tier="严格",
    )

    fake = DualRoleFake(
        check_specs=[
            _check_report(problems=[(1, "P1", "§2", "范围含糊", "写清")],
                          conclusion="> 核查结论:FIX(P1×1)"),
            _check_report(problems=[(2, "P2", "§5", "排版建议", "可选优化")],
                          conclusion="> 核查结论:FIX(P2×1)"),
        ],
        repair_specs=[RepairWritingFake()],
    )
    fresh_session._set_caller_for_tests(fake)

    assert fresh_session.start_check() is True
    assert _wait_chain_idle(fresh_session), "两跳链未在时限内收尾"

    docs = tmp_path / "docs"
    # 断言核心:修复调用计数 1 + check 报告最终编号 2
    assert len(fake.repair_calls) == 1, "应有恰好 1 次修复调用"
    assert len(fake.check_calls) == 2, "应有恰好 2 次核查调用(check-1、check-2)"
    assert (docs / "DESIGN-check-1.md").is_file()
    assert (docs / "DESIGN-check-2.md").is_file(), "check-2 应出现(check-2 计数 2)"
    assert not (tmp_path / "DESIGN.md.tmp").exists(), "tmp 应已被改名消费"

    # 纯 P2 报告后循环停在残余裁决态(无第三次核查/无第二次修复)
    snap = fresh_session.snapshot()
    assert snap["state"] == "phase5_checking"
    assert snap["current_check"] == 2


def test_start_check_pass_stops(tmp_path, fresh_session):
    """用例 5:PASS 报告——done 后无下一跳(修复零调用)、derive_state = mission_complete。"""
    _enter_phase5(fresh_session, tmp_path, check_reports={}, tier="严格")

    fake = DualRoleFake(
        check_specs=[_check_report(conclusion="> 核查结论:PASS")],
        repair_specs=[RepairWritingFake()],
    )
    fresh_session._set_caller_for_tests(fake)

    assert fresh_session.start_check() is True
    assert _wait_chain_idle(fresh_session)

    assert len(fake.check_calls) == 1
    assert len(fake.repair_calls) == 0, "PASS 报告不得触发修复"
    snap = fresh_session.snapshot()
    assert snap["state"] == "mission_complete"


def test_start_check_pending_question_intercepts(tmp_path, fresh_session):
    """用例 6:抛问截存——RepairFake say 事件含 `> 待裁决:#2:范围问题` → done 后报告尾部
    出现截存行、无下一跳 check(check 计数不增)。"""
    _enter_phase5(fresh_session, tmp_path, check_reports={}, tier="严格")

    fake = DualRoleFake(
        check_specs=[
            _check_report(problems=[(1, "P1", "§2", "范围含糊", "写清")],
                          conclusion="> 核查结论:FIX(P1×1)"),
        ],
        repair_specs=[
            RepairWritingFake(pending_lines=["> 待裁决:#2:范围问题"]),
        ],
    )
    fresh_session._set_caller_for_tests(fake)

    assert fresh_session.start_check() is True
    assert _wait_chain_idle(fresh_session)

    docs = tmp_path / "docs"
    report_text = (docs / "DESIGN-check-1.md").read_text(encoding="utf-8")
    assert "> 待裁决:#2:范围问题" in report_text, "抛问应被截存到报告尾部"
    # 无下一跳:check 调用计数 1,无 check-2
    assert len(fake.check_calls) == 1, "抛问后不得推进下一轮核查"
    assert not (docs / "DESIGN-check-2.md").exists()
    # 状态:phase5_checking(unpaired 非空 → 暂停态签名在盘)
    snap = fresh_session.snapshot()
    assert snap["state"] == "phase5_checking"
    import backend.grammar as grammar_mod

    assert grammar_mod.unpaired_verdicts(report_text) == [2]


def test_resume_after_verdict(tmp_path, fresh_session):
    """用例 7:续跑——verdict_append 落盘裁决 → start_repair 再跑 → 报告含裁决行的新 prompt。"""
    # resumed 态盘:问题表 #1 #2;#1 抛问且已裁决(配对)→ 判定式②命中;
    # #2 在问题表但未被抛问 → 残余未清零(不收口,®§6.4 判定式②的
    # 「配对问答行 + 无未配对 + 末行非 PASS」)
    report = _check_report(
        problems=[(1, "P1", "§2", "范围含糊", "写清"), (2, "P1", "§4", "措辞歧义", "直说")],
        conclusion="> 核查结论:FIX(P1×2)",
        pending_questions=[(1, "范围要不要收紧?")],
        verdict_lines=[(1, "修——按建议")],
    )
    _enter_phase5(fresh_session, tmp_path, check_reports={1: report}, tier="严格")

    # resumed 态直接验:「继续修复」唯一放行
    assert fresh_session.repair_available(tmp_path) is True

    repair_fake = RepairWritingFake()
    fresh_session._set_caller_for_tests(repair_fake)
    assert fresh_session.start_repair() is True
    assert _wait_chain_idle(fresh_session)

    # 续跑 prompt 资料段含问题与裁决行(以磁盘为准,§8.2 不引入其他通道)
    _, repair_prompt = repair_fake.repair_calls[0]
    assert "> 裁决:#1:修——按建议" in repair_prompt
    assert "范围要不要收紧" in repair_prompt
    # #2 在问题表未配对 → 无收口;同轮驱动链续跑下一轮核查(check 计数为 0 增:
    # 本 fake 只注入 repair caller 一次 —— 但驱动链会再起 check 调用同一 fake…)
    report_after = (tmp_path / "docs" / "DESIGN-check-1.md").read_text(encoding="utf-8")
    assert "> 核查结论:FIX(P1×2)" in report_after
    # 证据:#2 未被裁 → 残余不清零,报告不追加 PASS(收口判定零误触发)


def test_next_check_n_half_report_no_skip(tmp_path, fresh_session):
    """用例 8:半份重跑不跳号(D-P3-21)——半份盘(报告缺结论行)「继续自检」
    起跳 → Fake 写 docs/DESIGN-check-1.md 被覆盖(编号仍 1,不出现 check-2);
    完整盘起跳产 check-2。"""
    # 半份盘:check-1 报告无结论行
    half_report = (
        "# 核查报告\n\n> 自检档位:严格\n\n## 问题分级\n\n"
        "| 编号 | 级别 | 位置 | 问题 | 建议修法 |\n"
        "|---|---|---|---|---|\n"
        "| 1 | P1 | §2 | 范围含糊 | 写清 |\n"
    )  # 无 `> 核查结论:` 行 = 半份
    _enter_phase5(fresh_session, tmp_path, check_reports={1: half_report}, tier="严格")

    # _next_check_n 判定:半份 → 1(同轮覆盖)
    docs = tmp_path / "docs"
    assert fresh_session._next_check_n(tmp_path) == 1

    # 起跳(半份盘 phase5_checking,check_available True;CheckWritingFake
    # 脚本只给一跳 P1 报告——修复跳会因 caller 脚本耗尽而断链,这正是断言
    # 「不跳号」前需要的单跳形态;repair 跳不在本用例断言范围)
    fake = CheckWritingFake(specs=[
        _check_report(problems=[(1, "P1", "§2", "范围含糊", "写清")],
                      conclusion="> 核查结论:FIX(P1×1)"),
    ])

    class _Harness:
        """吞掉驱动链尾的修复跳(脚本到 check 为止):链断即停,不误报。"""

        def __init__(self, inner):
            self.inner = inner
            self.repair_calls: list[tuple[str, str]] = []

        def run(self, project_path, prompt: str):
            if "核查执行者" in prompt:
                yield from self.inner.run(project_path, prompt)
            else:
                # 修复跳被本用例吞停(不写 tmp、不发事件即 done)
                self.repair_calls.append((str(project_path), prompt))
                yield {"kind": "done", "content": "调用结束", "raw": None}

    harness = _Harness(fake)
    fresh_session._set_caller_for_tests(harness)
    assert fresh_session.start_check() is True
    assert _wait_chain_idle(fresh_session)

    # 编号仍 1,不出现 check-2(修复跳被吞停,链断在第一跳后)
    assert (docs / "DESIGN-check-1.md").is_file()
    assert not (docs / "DESIGN-check-2.md").exists(), "半份重跑不得跳号(D-P3-21)"

    # 对照:完整盘(有结论行)起跳 → 产 check-2
    assert fresh_session._next_check_n(tmp_path) == 2


def test_start_check_entry_rejects(tmp_path, fresh_session):
    """用例 9:入口拒绝——phase3/phase4 → False;busy 在飞 → False(HangingFake)。"""
    _enter_phase3_compliant(fresh_session, tmp_path)
    assert fresh_session.check_available(tmp_path) is False
    assert fresh_session.start_check() is False, "phase3 不应受理核查"
    assert fresh_session.start_repair() is False, "phase3 不应受理修复"

    _enter_phase4(fresh_session, tmp_path)
    assert fresh_session.start_check() is False, "phase4 不应受理核查"
    assert fresh_session.start_repair() is False, "phase4 不应受理修复"

    # busy:挂住在飞主调用 → start_check/start_repair 均 False
    _enter_phase5(fresh_session, tmp_path, check_reports={}, tier="严格")
    gate = threading.Event()
    release = threading.Event()

    class HangingFake(FakeAICaller):
        def run(self, project_path, prompt):
            self.run_calls.append((str(project_path), prompt))
            gate.set()
            release.wait(timeout=10)
            yield {"kind": "done", "content": "调用结束", "raw": None}

    hanging = HangingFake(events=[])
    fresh_session._set_caller_for_tests(hanging)
    threading.Thread(target=lambda: fresh_session.send_message("先聊"), daemon=True).start()
    assert gate.wait(timeout=5), "在飞调用未启动"

    assert fresh_session.start_check() is False, "在飞中不应受理核查"
    assert fresh_session.start_repair() is False, "在飞中不应受理修复"
    assert len(hanging.run_calls) == 1

    release.set()
    assert wait_idle(fresh_session), "调用未收尾"


def test_repair_available_three_states(tmp_path, fresh_session):
    """用例 10:repair_available 三态互斥(D-P3-20)——running False / 判定式② True / unpaired True→False / 纯 P2 False。"""
    # ① running 态:报告刚落盘未跑修复(无裁决行无待裁决行)→ False
    #    (与 check_available 同时 True 违反互斥——本盘形即防此盘)
    _enter_phase5(
        fresh_session, tmp_path,
        check_reports={1: _check_report(
            problems=[(1, "P1", "§2", "范围含糊", "写清")],
            conclusion="> 核查结论:FIX(P1×1)",
        )},
        tier="严格",
    )
    assert fresh_session.check_available(tmp_path) is True, "running 态继续自检可用(中断恢复)"
    assert fresh_session.repair_available(tmp_path) is False, \
        "running 态(报告刚落盘未跑修复)不得放行修复(D-P3-20 互斥)"

    # ② 判定式②:配对裁决 + 末行非 PASS → True(「继续修复」唯一放行)
    report = _check_report(
        problems=[(1, "P1", "§2", "范围含糊", "写清")],
        conclusion="> 核查结论:FIX(P1×1)",
        pending_questions=[(1, "范围要不要收紧?")],
        verdict_lines=[(1, "修——按建议")],
    )
    _enter_phase5(fresh_session, tmp_path, check_reports={1: report}, tier="严格")
    assert fresh_session.repair_available(tmp_path) is True, \
        "判定式②(配对裁决 + 末行非 PASS)应放行继续修复"
    assert fresh_session.check_available(tmp_path) is True  # check 是恢复通道,不互斥于此断言

    session._reset_for_tests()
    # unpaired 非空(paused 态)→ False
    report = _check_report(
        problems=[(1, "P1", "§2", "范围含糊", "写清")],
        conclusion="> 核查结论:FIX(P1×1)",
        pending_questions=[(1, "范围要不要收紧?")],
    )
    _enter_phase5(fresh_session, tmp_path, check_reports={1: report}, tier="严格")
    assert fresh_session.repair_available(tmp_path) is False, \
        "暂停态(未配对待裁决)不得放行修复"

    # 纯 P2 残余(p2 态)→ False
    report = _check_report(
        problems=[(2, "P2", "§5", "排版建议", "可选优化")],
        conclusion="> 核查结论:FIX(P2×1)",
    )
    _enter_phase5(fresh_session, tmp_path, check_reports={1: report}, tier="严格")
    assert fresh_session.repair_available(tmp_path) is False, \
        "纯 P2 残余走裁决卡通道,不放行修复"


def test_repair_no_tmp_stops_chain(tmp_path, fresh_session):
    """用例 11(G-idi03-1 RED):严格档修复跳未产出 tmp → 链必须断,不得无界自链。

    形态:check-1 产 P1 FIX 报告 → 自动链入修复 → 修复跳「不写 tmp、不发
    事件即 done」(AI 没写 tmp 的失败形态,D-P3-14 docstring 承诺该形态
    「error 事件『修复未产出 tmp,可重跑』,不驱动下一跳」)。
    修复前实测:守卫 `if tmp_path.is_file(): return` 在 tmp 缺失时不命中,
    执行直落 `_drive_next(project,"check")` → 无界自链
    (03-VERIFICATION.md G-idi03-1:20 秒内 10209 跳且仍在飞)。
    """
    _enter_phase5(fresh_session, tmp_path, check_reports={}, tier="严格")

    published: list[dict] = []
    orig_publish = fresh_session._publish_for_tests
    fresh_session._publish_for_tests = lambda ev: (published.append(dict(ev)), orig_publish(ev))[1]

    class _NoTmpHarness:
        """check 跳:固定产 P1 FIX 报告;repair 跳:不写 tmp、不发事件即 done。"""

        def __init__(self):
            self.check_calls = 0
            self.repair_calls = 0
            self.request_permission = None

        def run(self, project_path, prompt):
            if "核查执行者" in prompt:
                self.check_calls += 1
                n = _target_check_n(prompt) or self.check_calls
                docs = Path(project_path) / "docs"
                docs.mkdir(parents=True, exist_ok=True)
                (docs / f"DESIGN-check-{n}.md").write_text(
                    _check_report(problems=[(1, "P1", "§2", "范围含糊", "写清")],
                                  conclusion="> 核查结论:FIX(P1×1)"),
                    encoding="utf-8",
                )
                yield {"kind": "say", "content": f"核查第 {n} 轮完成。", "raw": None}
            else:
                self.repair_calls += 1
            yield {"kind": "done", "content": "调用结束", "raw": None}

    harness = _NoTmpHarness()
    fresh_session._set_caller_for_tests(harness)

    assert fresh_session.start_check() is True
    # 给链充分时间显影:修复前该窗口内会跑出数百跳(实测 510 跳/秒)
    time.sleep(1.5)

    assert harness.repair_calls == 1, \
        f"修复跳应恰好 1 次(未产出 tmp 不得再驱动),实际 {harness.repair_calls} 次"
    assert harness.check_calls == 1, \
        f"tmp 缺失不得驱动下一轮核查(无界自链),实际 {harness.check_calls} 次"
    assert not (tmp_path / "docs" / "DESIGN-check-2.md").exists(), \
        "tmp 缺失不得产生 check-2"
    assert any("修复未产出 tmp" in str(ev.get("content", "")) for ev in published), \
        "应发布「修复未产出 tmp,可重跑」error 事件"
    assert not fresh_session.busy(), "链应已停(不得仍在飞)"


def test_selfcheck_paused_questions_anchor_consistent(tmp_path, fresh_session):
    """用例 12(G-idi03-2 RED):待裁决行锚位与判定式一致——锚后抛问可见、
    锚前抛问按锁定文法不计(§6.4 配对空间限定在末一处结论行之后)。

    修复前:`_selfcheck_substate` 用 unpaired_verdicts(锚后限定)判 paused,
    却用 scan_pending_questions(无锚全文扫)取 questions——锚前抛问时判定式
    不命中而扫描命中,两扫描器分歧;锚后抛问时若报告头部另有一处同号行,
    questions 可能与判定式计数不一致。
    """
    import backend.grammar as grammar_mod

    # ① 锚前抛问:锁定文法不计(配对空间 = 末一处结论行之后)→ mode 不得为
    #    paused,questions 必须与判定式一致为空(不得呈现文法不认的问题)
    header_pending = (
        "# 核查报告\n\n> 自检档位:严格\n\n> 待裁决:#1:锚前抛问(正文行,不进配对空间)\n\n"
        "## 问题分级\n\n| 编号 | 级别 | 位置 | 问题 | 建议修法 |\n"
        "|---|---|---|---|---|\n| 1 | P1 | §2 | 范围含糊 | 写清 |\n\n"
        "> 核查结论:FIX(P1×1)\n"
    )
    _enter_phase5(fresh_session, tmp_path, check_reports={1: header_pending}, tier="严格")
    assert grammar_mod.unpaired_verdicts(header_pending) == [], "锚前抛问不进配对空间"
    snap = fresh_session.snapshot()
    assert snap["selfcheck"]["mode"] != "paused", \
        "锚前抛问不得判 paused(锁定文法不计)"
    assert snap["selfcheck"]["questions"] == [], \
        "questions 必须与判定式一致(不得呈现文法不认的问题)"

    # ①b 混合形态(分歧的正面显影):锚前一行 + 锚后一行 → 判定式只计锚后
    #     那一行,questions 不得把锚前那行也端出来(修复前 scan_pending_questions
    #     无锚全文扫 → questions 含两条,与 unpaired_verdicts 的计数分歧)
    session._reset_for_tests()
    mixed = (
        "# 核查报告\n\n> 自检档位:严格\n\n> 待裁决:#7:锚前抛问(不进配对空间)\n\n"
        "## 问题分级\n\n| 编号 | 级别 | 位置 | 问题 | 建议修法 |\n"
        "|---|---|---|---|---|\n| 1 | P1 | §2 | 范围含糊 | 写清 |\n\n"
        "> 核查结论:FIX(P1×1)\n\n> 待裁决:#1:范围要不要收紧?\n"
    )
    _enter_phase5(fresh_session, tmp_path, check_reports={1: mixed}, tier="严格")
    assert grammar_mod.unpaired_verdicts(mixed) == [1], "锁定文法只计锚后待裁决"
    snap = fresh_session.snapshot()
    assert snap["selfcheck"]["mode"] == "paused"
    assert snap["selfcheck"]["questions"] == [{"number": 1, "text": "范围要不要收紧?"}], \
        "questions 不得含锚前行(须与 unpaired_verdicts 同配对空间)"

    # ② 锚后抛问:锁定文法计入 → mode=paused,问题可见
    session._reset_for_tests()
    tail_pending = (
        "# 核查报告\n\n> 自检档位:严格\n\n## 问题分级\n\n"
        "| 编号 | 级别 | 位置 | 问题 | 建议修法 |\n|---|---|---|---|---|\n"
        "| 1 | P1 | §2 | 范围含糊 | 写清 |\n\n"
        "> 核查结论:FIX(P1×1)\n\n> 待裁决:#1:范围要不要收紧?\n"
    )
    _enter_phase5(fresh_session, tmp_path, check_reports={1: tail_pending}, tier="严格")
    assert grammar_mod.unpaired_verdicts(tail_pending) == [1]
    snap = fresh_session.snapshot()
    assert snap["selfcheck"]["mode"] == "paused"
    assert snap["selfcheck"]["questions"] == [{"number": 1, "text": "范围要不要收紧?"}]

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

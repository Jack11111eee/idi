# -*- coding: utf-8 -*-
"""/api/abort 路由层接线测试(Phase 1 验证 gap 修复,TDD RED 先行)。

既有 test_abort_leaves_no_dirty_ai_entry 直调 session.abort(),不经 HTTP 路由,
所以 Plan 03 会话层接管 caller 管理后的接线断裂没被拦住(VERIFICATION.md gap)。
本文件补经 FastAPI TestClient 的路由级行为:会话调用在飞时 POST /api/abort
必须真的杀 caller、释放 busy 锁、transcript 无脏 [ai]。
"""

import shutil
import sys
import threading
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from fastapi.testclient import TestClient  # noqa: E402

from backend import main, session  # noqa: E402
from backend.tests.test_session import FakeAICaller  # noqa: E402
from backend.transcript import parse_transcript  # noqa: E402


@pytest.fixture()
def route_env(tmp_path):
    """路由级测试环境:重置 session 状态 + 独立项目目录 + TestClient。"""
    session._reset_for_tests()
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "transcript.md").write_text("", encoding="utf-8")
    session.enter_project(tmp_path)
    client = TestClient(main.app)
    yield {"project": tmp_path, "client": client}
    session._reset_for_tests()


class HangingFake(FakeAICaller):
    """say 已产出但因长回答仍在生成的形态(在飞,等 abort 切断)。"""

    def __init__(self, events):
        super().__init__(events=events)
        self.mid_stream = threading.Event()
        self.release = threading.Event()

    def run(self, project_path, prompt):
        self.run_calls.append((str(project_path), prompt))
        for ev in list(self.events):
            yield dict(ev)
        self.mid_stream.set()  # say 全部产出,AI 仍在生成
        self.release.wait(timeout=10)  # 等 abort(或超时自续)
        if not self.aborted:
            yield {"kind": "done", "content": "调用结束", "raw": None}
        else:
            return  # 被杀:流被切断,不再产 done

    def abort(self) -> bool:
        self.aborted = True
        self.release.set()
        return True


def test_route_abort_kills_inflight_session_call(route_env):
    """会话调用在飞时 POST /api/abort:killed=true、caller.abort 被调、busy 释放、无脏 [ai]。"""
    client = route_env["client"]
    docs = route_env["project"] / "docs"

    fake = HangingFake(
        events=[{"kind": "say", "content": "开头说了几句,但还没说完。", "raw": None}]
    )
    session._set_caller_for_tests(fake)
    threading.Thread(target=lambda: session.send_message("长回答"), daemon=True).start()
    assert fake.mid_stream.wait(timeout=5), "未到达在飞时刻"
    assert session.busy(), "在飞调用应处于 busy"

    resp = client.post("/api/abort")
    assert resp.status_code == 200
    body = resp.json()
    assert body["killed"] is True, f"路由应真杀会话调用,实际返回:{body}"
    assert fake.aborted, "路由中止未触达 session caller 的 abort()"

    # busy 锁释放:后续 send 不再 409
    deadline = time.time() + 10
    while session.busy() and time.time() < deadline:
        time.sleep(0.05)
    assert not session.busy(), "abort 后 busy 锁未释放"

    # 中止语义(§5.5):未完成的 AI 回复不落盘 → transcript 只有 [user]
    messages = parse_transcript(docs / "transcript.md")
    roles = [m["role"] for m in messages]
    assert roles == ["user"], f"中止后应无脏 [ai] 条目,实际:{roles}"


def test_route_abort_idle_returns_killed_false(route_env):
    """无在飞调用时 POST /api/abort:killed=false(字段必须真实)。"""
    resp = route_env["client"].post("/api/abort")
    assert resp.status_code == 200
    assert resp.json()["killed"] is False

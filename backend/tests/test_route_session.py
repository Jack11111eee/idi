# -*- coding: utf-8 -*-
"""GET /api/session 路由测试(Phase 1 UAT gap G-idi01-7 修复,TDD RED 先行)。

背景:会话轮产出 draft.md 后,前端 refreshDraftAfterStream() 需要拉新门控
(g1_available / divergence_available / 状态徽标),否则「认可雏形」按钮要
手动重进目录才解禁。POST /api/enter 不适合流后刷新(会整页重渲染 transcript,
冲掉刚流式出的 AI 气泡,且首拍 [ai] 尚未落盘),故新增只读 GET /api/session,
返回与 /api/enter 同构的 session.snapshot() 全量字段。
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from fastapi.testclient import TestClient  # noqa: E402

from backend import main, session  # noqa: E402


@pytest.fixture()
def route_env(tmp_path):
    """路由级测试环境:重置 session 状态 + 独立项目目录 + TestClient。"""
    session._reset_for_tests()
    client = TestClient(main.app)
    yield {"project": tmp_path, "docs": tmp_path / "docs", "client": client}
    session._reset_for_tests()


def test_route_session_without_entered_project(route_env):
    """未进入项目:GET /api/session → 4xx + status=error(不 500)。"""
    resp = route_env["client"].get("/api/session")
    assert resp.status_code == 400
    body = resp.json()
    assert body["status"] == "error"
    assert "尚未进入" in body["message"]


def test_route_session_mirrors_enter_payload_and_tracks_disk(route_env):
    """进入后:GET /api/session 与 POST /api/enter 同构,门控随磁盘现状翻转。"""
    client = route_env["client"]
    docs = route_env["docs"]
    docs.mkdir()
    (docs / "transcript.md").write_text("", encoding="utf-8")

    # 进入后首拍:docs/ 存在 → 阶段 1-2,雏形未生 → 发散开、G1 关
    entered = client.post("/api/enter", json={"path": str(route_env["project"])})
    assert entered.status_code == 200

    resp = client.get("/api/session")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["state"] == "phase12_in_progress"
    assert body["transcript"] == []
    assert body["draft"] is None
    assert body["g1_available"] is False
    assert body["divergence_available"] is True

    # 会话轮产出 draft.md 后【不重进】再拉:门控必须随磁盘对齐
    (docs / "draft.md").write_text("# 雏形\n", encoding="utf-8")
    body2 = client.get("/api/session").json()
    assert body2["status"] == "ok"
    assert body2["draft"] == "# 雏形\n"
    assert body2["g1_available"] is True
    assert body2["divergence_available"] is False
    assert body2["state"] == "phase12_in_progress"

    # G1 定稿后(完整轮存在)再拉:phase3、当前轮 1、两门全关
    (docs / "discuss-round-1.md").write_text(
        "# 第 1 轮\n\n> 申请授权:否\n", encoding="utf-8"
    )
    body3 = client.get("/api/session").json()
    assert body3["status"] == "ok"
    assert body3["state"] == "phase3"
    assert body3["current_round"] == 1
    assert body3["g1_available"] is False
    assert body3["divergence_available"] is False

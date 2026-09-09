# -*- coding: utf-8 -*-
"""端到端冒烟(PLAN idi-01-03 Task 3):真实 claude CLI 依赖链路。

两个 @pytest.mark.slow 用例,IDI_E2E 未设时 skip(常规跑不依赖真 AI):
  1. test_full_conversation_roundtrip —— 真实会话一轮:
     enter_project + send_message → 轮询 transcript 出现 [ai] → [user, ai] 序列
  2. test_restart_recovery —— 重启恢复:
     重建 session 模块状态(模拟重启:文件即状态)→ 重进同目录 →
     transcript 恢复且 draft(若产生)可读
"""

import importlib
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend import session  # noqa: E402
from backend.transcript import parse_transcript  # noqa: E402

pytestmark = pytest.mark.slow

# 真实调用时长不受控:180s deadline(轮询循环内计)
_POLL_DEADLINE_SECONDS = 180
_POLL_INTERVAL = 1.0

# 用例提示词(明确不要求写 draft,隔离变量;draft 由用例 2 若产生则校验)
_INTRO_PROMPT = "请向我介绍你自己,一句话即可"


def _e2e_enabled() -> bool:
    import os

    return os.environ.get("IDI_E2E") == "1"


@pytest.fixture(scope="session")
def e2e_project(tmp_path_factory):
    """共享项目目录(两个用例先后用:用例 1 产出,用例 2 恢复;session 级同一目录)。"""
    return tmp_path_factory.mktemp("e2e_project")


def test_full_conversation_roundtrip(e2e_project):
    """E2E 1:真实会话一轮(真 claude CLI 调用)。"""
    if not _e2e_enabled():
        pytest.skip("IDI_E2E 未设(常规跑不依赖真 AI)")

    session._reset_for_tests()
    snapshot = session.enter_project(e2e_project)
    assert snapshot["state"] in ("phase1_new", "phase12_in_progress")

    accepted = session.send_message(_INTRO_PROMPT)
    assert accepted in (True, None), "send_message 未受理"

    transcript_path = e2e_project / "docs" / "transcript.md"
    waited = 0.0
    messages = []
    while waited < _POLL_DEADLINE_SECONDS:
        time.sleep(_POLL_INTERVAL)
        waited += _POLL_INTERVAL
        messages = parse_transcript(transcript_path)
        # [user] 在,[ai] 也落盘 = 调用完成
        if any(m["role"] == "ai" for m in messages):
            break
    assert any(m["role"] == "ai" for m in messages), (
        f"180s 内未出现 [ai] 条目(等待 {waited:.0f}s)"
    )
    roles = [m["role"] for m in messages]
    assert roles == ["user", "ai"], f"序列异常:{roles}"
    assert messages[1]["content"].strip() != "", "AI 回复为空"


def test_restart_recovery(e2e_project):
    """E2E 2:重启恢复——重建 session 模块状态后重进同目录,transcript/draft 从磁盘恢复。"""
    if not _e2e_enabled():
        pytest.skip("IDI_E2E 未设(常规跑不依赖真 AI)")

    # 模拟重启:重载模块(清空内存态;文件即状态,D-19)
    importlib.reload(session)

    snapshot = session.enter_project(e2e_project)
    # transcript 完整恢复(用例 1 的 [user][ai] 双条在)
    roles = [m["role"] for m in snapshot["transcript"]]
    assert roles == ["user", "ai"], f"重启后 transcript 未恢复:{roles}"
    assert snapshot["transcript"][0]["content"].strip() == _INTRO_PROMPT

    # draft:若上一用例产生了则可读(内容非空);未产生则是 None(不报错)
    if snapshot["draft"] is not None:
        assert snapshot["draft"].strip() != "", "draft 存在但为空"
    # 原文件仍在磁盘(文件即状态,恢复不依赖任何内存)
    assert (e2e_project / "docs" / "transcript.md").is_file()

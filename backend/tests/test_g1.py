# -*- coding: utf-8 -*-
"""G1 定稿纯函数测试(PLAN idi-01-04 Task 2,TDD RED 先行)。

五个 behavior 用例(FLOW-03 / §4.4 / §6.4):
  1. finalize_g1 后 discuss-round-1.md 存在,内容 = draft 全文 + 末行恰为 `> 申请授权:否`
  2. draft.md 保留、内容不变(定稿不改草稿)
  3. 幂等防护:discuss-round-1.md 已存在时抛 FileExistsError
  4. 标记行前有空行时 last_nonempty_line 语义不破坏(state.is_complete_round 复核)
  5. finalize 后 derive_state = phase3、current_round=1(三模块闭环)
全部纯文件系统构造,不起 AI、不起服务器。
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend import g1 as g1_mod  # noqa: E402
from backend.state import derive_state, is_complete_round  # noqa: E402


def _make_draft_project(tmp_path, content="# 雏形\n\n目标:做一个本地工具。\n", with_trailing_blank=True):
    """构造含 docs/draft.md 的临时项目;with_trailing_blank 在 draft 尾部加多余空白。"""
    docs = tmp_path / "docs"
    docs.mkdir(parents=True)
    draft = docs / "draft.md"
    text = content + ("\n\n\n" if with_trailing_blank else "")
    draft.write_text(text, encoding="utf-8")
    return docs / "draft.md"


def test_finalize_g1_marker_last_nonempty_line(tmp_path):
    """用例 1:定稿产物 = draft 全文 + 末行恰为 `> 申请授权:否`(strip 后全等)。"""
    _make_draft_project(tmp_path, content="# 雏形\n\n## 目标\n\n做 XYZ。\n\n## 边界\n\n不做什么。\n")
    result = g1_mod.finalize_g1(tmp_path)
    round1 = tmp_path / "docs" / "discuss-round-1.md"
    assert result == round1  # 返回新文件路径
    assert round1.is_file()
    text = round1.read_text(encoding="utf-8")
    # draft 全文在内
    assert "# 雏形" in text
    assert "做 XYZ。" in text
    assert "不做什么。" in text
    # 末行(strip 后全等;前缀不算)
    lines = text.splitlines()
    assert lines[-1].strip() == "> 申请授权:否"


def test_finalize_g1_draft_untouched(tmp_path):
    """用例 2:定稿不改草稿——draft.md 保留且内容不变。"""
    draft_path = _make_draft_project(tmp_path, content="# 草稿\n\n第一版。\n")
    before = draft_path.read_text(encoding="utf-8")
    g1_mod.finalize_g1(tmp_path)
    assert draft_path.is_file(), "draft.md 不应被删除"
    assert draft_path.read_text(encoding="utf-8") == before


def test_finalize_g1_idempotency_guard(tmp_path):
    """用例 3:discuss-round-1.md 已存在 → FileExistsError(G1 只走一次)。"""
    _make_draft_project(tmp_path)
    g1_mod.finalize_g1(tmp_path)
    with pytest.raises(FileExistsError):
        g1_mod.finalize_g1(tmp_path)
    # 已定稿的产物不被二次写坏(内容仍是第一次的定稿)
    round1 = tmp_path / "docs" / "discuss-round-1.md"
    assert round1.read_text(encoding="utf-8").splitlines()[-1].strip() == "> 申请授权:否"


def test_finalize_g1_no_draft_raises(tmp_path):
    """用例 3b(防护面):无 draft.md → FileNotFoundError(提示先有雏形)。"""
    (tmp_path / "docs").mkdir(parents=True)
    with pytest.raises(FileNotFoundError):
        g1_mod.finalize_g1(tmp_path)


def test_finalize_g1_complete_round_semantics(tmp_path):
    """用例 4:draft 尾部多余空白不破坏「最后一个非空行」语义——is_complete_round 判完整轮。"""
    _make_draft_project(tmp_path, content="# 雏形\n\n内容。\n", with_trailing_blank=True)
    g1_mod.finalize_g1(tmp_path)
    text = (tmp_path / "docs" / "discuss-round-1.md").read_text(encoding="utf-8")
    assert is_complete_round(text) is True, "定稿产物必须被完整轮判据确认"


def test_finalize_g1_derives_phase3(tmp_path):
    """用例 5:三模块闭环——finalize 后 derive_state = phase3、current_round=1。"""
    _make_draft_project(tmp_path, content="# 雏形\n\n已经谈妥。\n")
    g1_mod.finalize_g1(tmp_path)
    state = derive_state(tmp_path)
    assert state["state"] == "phase3"
    assert state["current_round"] == 1
    assert state["current_check"] is None

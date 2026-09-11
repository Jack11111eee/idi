# -*- coding: utf-8 -*-
"""G3 四查组合判定 + AUTHORIZATION.md 写入测试(PLAN idi-03-01 Task 1 / FLOW-05)。

用例(§4.4 四处机械校验 + §7.4 授权痕迹 / D-P3-1 / D-P3-2 / D-P3-4):
  1. 四查合规(维度全✓/清单清零/标记是/无 pending 批注)→ True
  2. ①污染:当前轮 annotations 含 pending comment → False(其余三条合规)
  3. ②污染:清单含一行「待决」→ False
  4. ③污染:维度表含一行 ◐ → False
  5. ④污染:末行 `> 申请授权:否` → False
  6. 非 phase3(无完整轮 / 已授权 phase4 / phase1_new)→ False
  7. authorize_write:写入项目根 AUTHORIZATION.md,内容含 ISO-8601 授权时间
     与「确认授权」确认词标记两要素;再次调用 → FileExistsError(幂等)
样本全部手造(tmp_path),不读本项目自身 docs/ 历史(D-P2-19 延续)。
全部纯文件系统构造,不起 AI、不起服务器。
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend import g3 as g3_mod  # noqa: E402
from backend.state import derive_state, is_complete_round  # noqa: E402

AUTH_YES = "> 申请授权:是"

_GREEN_TABLE = (
    "| 维度 | 状态 | 说明 |\n|------|------|------|\n"
    "| 目标与边界 | ✓ | 已明确 |\n| 用户与场景 | ✓ | 两类场景已定 |\n"
    "| 流程与状态 | ✓ | 五阶段三道门已定 |"
)
_CLEAR_LIST = (
    "| 编号 | 问题 | 状态 |\n|------|------|------|\n"
    "| Q1 | 部署形态? | 已决 |"
)


def _make_phase3_project(
    tmp_path,
    *,
    dimension_table: str = _GREEN_TABLE,
    pending_list: str = _CLEAR_LIST,
    marker: str = AUTH_YES,
    pending_annotation: bool = False,
) -> Path:
    """构造四查合规的 phase3 临时项目(手造最小五件套当前轮文档 + 空 annotations)。

    pending_annotation=True 时额外落一条 pending comment(①污染样本)。
    """
    docs = tmp_path / "docs"
    docs.mkdir(parents=True)
    doc = (
        "# 第 2 轮讨论\n\n"
        "## 1. 批注回应(处置)\n\n"
        "| 批注id | 原文摘录 | 回应 |\n|------|------|------|\n"
        "| a1-01 | 某段原文 | 已按意见补充 |\n\n"
        "## 2. 决策登记\n\n"
        "| 决策 | 内容 |\n|------|------|\n| D-01 | 示例 |\n\n"
        "## 3. 覆盖维度表\n\n"
        f"{dimension_table}\n\n"
        "## 4. 未决问题清单\n\n"
        f"{pending_list}\n\n"
        f"{marker}\n"
    )
    # 文档须为完整轮(末行合规授权标记),否则半成品轮被视为不存在
    assert is_complete_round(doc) is True, "测试样本必须是完整轮文档"
    (docs / "discuss-round-1.md").write_text(doc, encoding="utf-8")
    (docs / "discuss-round-2.md").write_text(doc, encoding="utf-8")

    items = []
    if pending_annotation:
        items.append(
            {
                "id": "a2-01",
                "quote": "某段原文",
                "before": "",
                "type": "comment",
                "note": "这里还差什么",
                "status": "pending",
                "answer": None,
                "created_at": "2026-09-10T00:00:00+00:00",
            }
        )
    annotations = {"round": 2, "items": items}
    (docs / "discuss-round-2.annotations.json").write_text(
        json.dumps(annotations, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return tmp_path


def test_g3_available_all_four_checks_pass(tmp_path):
    """用例 1:四查合规(维度全✓/清单清零/标记是/无 pending)→ True。"""
    project = _make_phase3_project(tmp_path)
    assert g3_mod.g3_available(project) is True
    state = derive_state(project)
    assert state["state"] == "phase3"
    assert state["current_round"] == 2


def test_g3_available_pending_annotation_pollution(tmp_path):
    """用例 2(①污染):当前轮 annotations 含 pending comment → False。"""
    project = _make_phase3_project(tmp_path, pending_annotation=True)
    assert g3_mod.g3_available(project) is False


def test_g3_available_pending_list_wait_pollution(tmp_path):
    """用例 3(②污染):清单含一行「待决」→ False(其余三条合规)。"""
    project = _make_phase3_project(
        tmp_path,
        pending_list=(
            "| 编号 | 问题 | 状态 |\n|------|------|------|\n"
            "| Q1 | 部署形态? | 已决 |\n| Q2 | 中期接手怎么算? | 待决 |"
        ),
    )
    assert g3_mod.g3_available(project) is False


def test_g3_available_dimension_half_pollution(tmp_path):
    """用例 4(③污染):维度表含一行 ◐ → False。"""
    project = _make_phase3_project(
        tmp_path,
        dimension_table=(
            "| 维度 | 状态 | 说明 |\n|------|------|------|\n"
            "| 目标与边界 | ✓ | 已明确 |\n| 流程与状态 | ◐ | 仍有草图 |"
        ),
    )
    assert g3_mod.g3_available(project) is False


def test_g3_available_auth_marker_no_pollution(tmp_path):
    """用例 5(④污染):末行 `> 申请授权:否` → False。"""
    project = _make_phase3_project(tmp_path, marker="> 申请授权:否")
    assert g3_mod.g3_available(project) is False


def test_g3_available_non_phase3_states(tmp_path):
    """用例 6:非 phase3 一律 False(无完整轮 / 已授权 phase4 / 无 docs/)。"""
    # 无 docs/ → phase1_new
    empty = tmp_path / "empty-proj"
    empty.mkdir()
    assert g3_mod.g3_available(empty) is False

    # 完整轮 + AUTHORIZATION.md → phase4(已授权,G3 不再开)
    project = _make_phase3_project(tmp_path)
    (project / "AUTHORIZATION.md").write_text("# 授权记录\n", encoding="utf-8")
    assert g3_mod.g3_available(project) is False

    # 只有半成品轮(末行无合规标记)→ 无完整轮 → phase12,G3 关闸
    partial = tmp_path / "partial-proj"
    docs2 = partial / "docs"
    docs2.mkdir(parents=True)
    (docs2 / "discuss-round-1.md").write_text(
        "# 半成品\n\n末行没有授权标记\n", encoding="utf-8"
    )
    assert g3_mod.g3_available(partial) is False


def test_g3_available_current_round_not_stale_round(tmp_path):
    """用例 6b(D-P3-2):四查只对最大完整轮判——round-2 标记为否但 round-1 合规,
    current_round=2,四查在 round-2 上判 → False(不回落旧轮)。"""
    project = _make_phase3_project(tmp_path, marker="> 申请授权:否")
    # round-1 保持合规样本(是),round-2 为否;若误读 round-1 会错误判 True
    assert g3_mod.g3_available(project) is False


def test_authorize_write_two_elements_and_idempotency(tmp_path):
    """用例 7:authorize_write 落盘两要素(ISO-8601 时间 + 「确认授权」标记);
    再次调用 → FileExistsError(G3 只走一次,幂等防护照 g1.py 先例)。"""
    project = _make_phase3_project(tmp_path)
    result = g3_mod.authorize_write(project)
    auth_path = project / "AUTHORIZATION.md"
    assert result == auth_path
    assert auth_path.is_file()
    assert (project / "docs" / "AUTHORIZATION.md").exists() is False, "落点在项目根,不在 docs/ 下"

    text = auth_path.read_text(encoding="utf-8")
    # 两要素之一:ISO-8601 授权时间(日期片段可 grep)
    assert "20" in text and "T" in text and ":" in text, "内容含 ISO-8601 授权时间"
    # 两要素之二:操作者确认词标记行含「确认授权」
    assert "确认授权" in text

    # 幂等防护:已存在 → FileExistsError(中文消息)
    with pytest.raises(FileExistsError, match="G3 只走一次"):
        g3_mod.authorize_write(project)
    # 首次产物不被二次调用写坏
    assert "确认授权" in auth_path.read_text(encoding="utf-8")

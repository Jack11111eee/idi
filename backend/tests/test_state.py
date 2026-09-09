# -*- coding: utf-8 -*-
"""derive_state 单元测试:DESIGN.md §7.4 八行推导表(自上而下首条命中)+ §6.4/§7.3 完整轮判据。

构造目录形态即断言依据(plan behavior 用例 1-10)。
"""
from pathlib import Path

from backend.state import (
    derive_state,
    is_complete_round,
    last_nonempty_line,
)


RESULT_KEYS = {"state", "current_round", "current_check"}

AUTH_YES = "> 申请授权:是"
AUTH_NO = "> 申请授权:否"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def assert_result(result, state, current_round=None, current_check=None):
    assert set(result.keys()) == RESULT_KEYS
    assert result["state"] == state
    assert result["current_round"] == current_round
    assert result["current_check"] == current_check


def valid_round_text(marker: str = AUTH_NO) -> str:
    return f"# 第 N 轮讨论\n\n正文……\n\n{marker}\n"


# ---------- 用例 1(行 1):空目录 ----------

def test_row1_empty_dir_is_phase1_new(tmp_path):
    assert_result(derive_state(tmp_path), "phase1_new")


# ---------- 用例 2(行 2):有 docs/、无完整轮、无 DESIGN.md、无 AUTHORIZATION.md ----------

def test_row2_docs_without_any_round_is_phase12(tmp_path):
    write(tmp_path / "docs" / "draft.md", "# 草稿\n")
    assert_result(derive_state(tmp_path), "phase12_in_progress")


def test_row2_g1_prelude_stale_round_residue(tmp_path):
    # "G1 定稿前旧轮残留":仅存在末行不合格的轮次文档——半成品轮视为不存在
    write(
        tmp_path / "docs" / "discuss-round-1.md",
        "# 半成品\n\n正文还没有授权标记\n",
    )
    assert_result(derive_state(tmp_path), "phase12_in_progress")


# ---------- 用例 3(行 3):有完整轮、无 DESIGN.md、无 AUTHORIZATION.md ----------

def test_row3_complete_rounds_current_round_is_max_complete(tmp_path):
    write(tmp_path / "docs" / "discuss-round-1.md", valid_round_text())
    write(tmp_path / "docs" / "discuss-round-2.md", valid_round_text())
    write(tmp_path / "docs" / "discuss-round-3.md", valid_round_text(AUTH_YES))
    # round-4 是半成品(末行不合格)——视为不存在
    write(
        tmp_path / "docs" / "discuss-round-4.md",
        "# 半成品第 4 轮\n\n末行没有合规授权标记\n",
    )
    assert_result(derive_state(tmp_path), "phase3", current_round=3)


def test_row3_round_auth_marker_is_a_request_not_a_credential(tmp_path):
    # 末轮申请标记为「是」仍按行 3 处理:授权凭证是 AUTHORIZATION.md,不是 AI 的申请
    write(tmp_path / "docs" / "discuss-round-1.md", valid_round_text(AUTH_YES))
    assert_result(derive_state(tmp_path), "phase3", current_round=1)


# ---------- 用例 4(行 4):有 AUTHORIZATION.md、无 DESIGN.md、无 DESIGN-check ----------
# 注:正常运行中 AUTHORIZATION.md 出现前 docs/ 早已存在(G1 定稿落轮次文档)
# ——行 1「目录内无 docs/」自上而下首条命中,故本行各用例均先建 docs/。

def test_row4_authorized_without_design_is_phase4(tmp_path):
    write(tmp_path / "docs" / "discuss-round-1.md", valid_round_text(AUTH_YES))
    write(tmp_path / "AUTHORIZATION.md", "2026-09-09 确认授权\n")
    assert_result(derive_state(tmp_path), "phase4")


def test_row4_tmp_residue_does_not_affect_judgement(tmp_path):
    # 撰写中断残留的 DESIGN.md.tmp 不影响判定
    write(tmp_path / "docs" / "discuss-round-1.md", valid_round_text(AUTH_YES))
    write(tmp_path / "AUTHORIZATION.md", "2026-09-09 确认授权\n")
    write(tmp_path / "DESIGN.md.tmp", "# 写了一半的设计文档\n")
    assert_result(derive_state(tmp_path), "phase4")


# ---------- 用例 5(行 5):有 DESIGN.md、无 DESIGN-check ----------

def test_row5_design_without_checks_awaits_tier(tmp_path):
    write(tmp_path / "docs" / "discuss-round-1.md", valid_round_text(AUTH_YES))
    write(tmp_path / "AUTHORIZATION.md", "2026-09-09 确认授权\n")
    write(tmp_path / "DESIGN.md", "# 总设计文档\n")
    assert_result(derive_state(tmp_path), "phase5_awaiting_tier")


# ---------- 用例 6(行 6):有 DESIGN.md 与 check 文件、最新报告末行非 PASS ----------

def test_row6_latest_check_without_pass_is_checking(tmp_path):
    write(tmp_path / "DESIGN.md", "# 总设计文档\n")
    write(
        tmp_path / "docs" / "DESIGN-check-1.md",
        "# 核查报告 1\n\n- 问题 A\n- 问题 B\n",
    )
    assert_result(derive_state(tmp_path), "phase5_checking", current_check=1)


def test_row6_report_on_disk_without_conclusion_line(tmp_path):
    # "报告已落盘但无结论行"形态:同样落行 6
    write(tmp_path / "DESIGN.md", "# 总设计文档\n")
    write(
        tmp_path / "docs" / "DESIGN-check-1.md",
        "# 核查报告 1(半成品)\n\n问题清单写到这里中断\n",
    )
    assert_result(derive_state(tmp_path), "phase5_checking", current_check=1)


# ---------- 用例 7(行 7):最新 DESIGN-check 末行以 PASS 开头 ----------

def test_row7_latest_check_pass_line_is_mission_complete(tmp_path):
    write(tmp_path / "DESIGN.md", "# 总设计文档\n")
    write(
        tmp_path / "docs" / "DESIGN-check-1.md",
        "# 核查报告 1\n\n> 核查结论:PASS(问题 3 项修复完毕)\n",
    )
    assert_result(derive_state(tmp_path), "mission_complete")


def test_row7_multiple_checks_take_max_number(tmp_path):
    # 边界(用例 10):多个 check 取最大编号为最新
    write(tmp_path / "DESIGN.md", "# 总设计文档\n")
    write(
        tmp_path / "docs" / "DESIGN-check-1.md",
        "# 核查报告 1\n\n> 核查结论:PASS\n",
    )
    write(
        tmp_path / "docs" / "DESIGN-check-2.md",
        "# 核查报告 2\n\n尚有问题未修\n",
    )
    assert_result(derive_state(tmp_path), "phase5_checking", current_check=2)


# ---------- 用例 8(边界):round 编号非连续时取实际存在的最大完整编号 ----------

def test_nonconsecutive_round_numbers_take_max_existing_complete(tmp_path):
    # 有 1、3 无 2:最大完整轮 = 3(实际存在者)
    write(tmp_path / "docs" / "discuss-round-1.md", valid_round_text())
    write(tmp_path / "docs" / "discuss-round-3.md", valid_round_text())
    assert_result(derive_state(tmp_path), "phase3", current_round=3)


# ---------- 用例 9(边界):末行授权标记后随空行/行尾空白 ----------

def test_last_nonempty_line_semantics(tmp_path):
    # 合规标记是"最后一个非空行"——标记后随空行仍合规
    write(
        tmp_path / "docs" / "discuss-round-1.md",
        f"# 第 1 轮\n\n{AUTH_NO}\n\n\n",
    )
    assert_result(derive_state(tmp_path), "phase3", current_round=1)


def test_marker_line_with_trailing_whitespace(tmp_path):
    # 行尾空白:strip 后恰等 → 合规
    write(
        tmp_path / "docs" / "discuss-round-1.md",
        f"# 第 1 轮\n\n{AUTH_NO}   \n",
    )
    assert_result(derive_state(tmp_path), "phase3", current_round=1)


# ---------- 判据辅助函数直测 ----------

def test_is_complete_round_exact_match_no_prefix_suffix_tolerance():
    # 前缀不算、后缀不算——exact match after strip
    assert is_complete_round(f"{AUTH_NO}\n") is True
    assert is_complete_round(f"{AUTH_YES}\n") is True
    assert is_complete_round(f"{AUTH_NO}   \n\n") is True  # 行尾空白 + 尾空行
    assert is_complete_round(f"> 申请授权:是的\n") is False  # 后缀不算
    assert is_complete_round(f"前缀 {AUTH_NO}\n") is False  # 前缀不算
    assert is_complete_round("") is False  # 空文档
    assert is_complete_round("# 只有标题\n") is False


def test_last_nonempty_line_basic():
    assert last_nonempty_line("a\nb\n\nc\n") == "c"
    assert last_nonempty_line("\n\n \n  x  \n") == "x"
    assert last_nonempty_line("") is None
    assert last_nonempty_line("\n \n") is None

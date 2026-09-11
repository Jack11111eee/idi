# -*- coding: utf-8 -*-
"""自检磁盘签名读写纯函数测试(PLAN idi-03-01 Task 3 / DATA-04 / §8.2 / §6.4 / D-P3-11/12/17/19)。

用例矩阵:
  tier:写读回(严格→宽松覆盖)/ 白名单外 ValueError / 不存在 None / 脏内容 None
  待裁决:追加 + 内容级幂等跳过(False)/ 同号新内容追加第二行 / 报告不存在 FileNotFoundError
  裁决:追加 + 同号 FileExistsError(一问一答)/ 报告不存在 FileNotFoundError
  PASS:追加后 is_pass_conclusion True(末行锚点机器证明)+ 幂等二跳不重复
  正文保全:三类追加前后正文逐字不变(T-idi03-03)
样本手造(tmp_path):报告含非 PASS 结论行(`> 核查结论:FIX(P1×1)`)+
P2 问题表,确保追加行落在结论行之后(进 §6.4 配对空间)。
D-P2-19 延续:不读本项目自身 docs/ 历史报告,全部手造。
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend import checks as checks_mod  # noqa: E402
from backend.grammar import is_pass_conclusion, parse_verdict_lines  # noqa: E402


def _make_report(tmp_path) -> Path:
    """手造最小 check 报告(头部档位行 + P2 问题表 + FIX 结论行)。"""
    report = tmp_path / "docs" / "DESIGN-check-1.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        "# DESIGN-check-1 核查报告\n\n"
        "> 自检档位:严格\n\n"
        "## 问题分级\n\n"
        "| 编号 | 级别 | 位置 | 问题 | 建议修法 |\n"
        "|------|------|------|------|----------|\n"
        "| 1 | P1 | §2.1 | 口径漂移 | 统一口径 |\n"
        "| 2 | P2 | §9 | 术语可更白话 | 改写术语 |\n"
        "\n> 核查结论:FIX(P1×1)\n",
        encoding="utf-8",
    )
    return report


# ---------- tier 签名三件(D-P3-11 / D-P3-12) ----------

def test_write_tier_and_read_back(tmp_path):
    """用例 1:write_tier 落盘 docs/DESIGN-check-tier.md,read_tier 读回;
    重选档覆盖(严格 → 宽松,覆盖式幂等)。"""
    result = checks_mod.write_tier(tmp_path, "严格")
    tier_path = tmp_path / "docs" / "DESIGN-check-tier.md"
    assert result == tier_path
    assert tier_path.is_file()
    text = tier_path.read_text(encoding="utf-8")
    assert text.strip() == "> 自检档位:严格"  # 头部行(单行文件,常量字面)
    assert checks_mod.read_tier(tmp_path) == "严格"

    # 覆盖式幂等:重选档覆盖
    checks_mod.write_tier(tmp_path, "宽松")
    assert checks_mod.read_tier(tmp_path) == "宽松"


def test_write_tier_whitelist_value_error(tmp_path):
    """用例 2:白名单外值(如「超严格」)→ ValueError(中文消息)。"""
    with pytest.raises(ValueError, match="严格|宽松"):
        checks_mod.write_tier(tmp_path, "超严格")
    assert (tmp_path / "docs" / "DESIGN-check-tier.md").exists() is False, "拒绝时不落盘"


def test_read_tier_missing_file_returns_none(tmp_path):
    """用例 3:文件不存在 → None(不抛)。"""
    assert checks_mod.read_tier(tmp_path) is None


def test_read_tier_dirty_content_returns_none(tmp_path):
    """用例 4:脏内容(头部行非法/被外部损坏)→ None + warning(不抛)。"""
    tier_path = tmp_path / "docs" / "DESIGN-check-tier.md"
    tier_path.parent.mkdir(parents=True, exist_ok=True)
    tier_path.write_text("> 自检档位:超严格\n", encoding="utf-8")
    assert checks_mod.read_tier(tmp_path) is None
    tier_path.write_text("完全无关的内容\n", encoding="utf-8")
    assert checks_mod.read_tier(tmp_path) is None


# ---------- 待裁决追加(D-P3-18 / §6.4 内容级幂等) ----------

def test_append_pending_question_and_content_idempotency(tmp_path):
    """用例 5:追加 `> 待裁决:#3:范围问题`;同内容重复调用 → False 不重复追加
    (内容级幂等);追加后进入 §6.4 配对空间(parse_verdict_lines 可见)。"""
    report = _make_report(tmp_path)
    before_lines = report.read_text(encoding="utf-8").splitlines()

    assert checks_mod.append_pending_question(report, 3, "范围问题") is True
    text = report.read_text(encoding="utf-8")
    assert text.splitlines()[-1].strip() == "> 待裁决:#3:范围问题"
    verdicts = parse_verdict_lines(text)
    assert {"kind": "待裁决", "number": 3} in verdicts

    # 内容级幂等:同号同内容再调 → False,文件一字不增(与首次追加后逐字相同)
    assert checks_mod.append_pending_question(report, 3, "范围问题") is False
    assert report.read_text(encoding="utf-8") == text, "同内容只追加一次"

    # 正文保全:追加前后正文(原内容)逐字不变(T-idi03-03)
    original = "\n".join(before_lines)
    assert original in report.read_text(encoding="utf-8")


def test_append_pending_question_same_number_new_text_appends(tmp_path):
    """用例 6:同号新内容 → 追加第二行(幂等为内容级非号级;判定式按
    同号配对不受影响——§6.4)。"""
    report = _make_report(tmp_path)
    checks_mod.append_pending_question(report, 3, "范围问题")
    assert checks_mod.append_pending_question(report, 3, "另一问") is True
    text = report.read_text(encoding="utf-8")
    assert text.count("> 待裁决:#3:") == 2
    # 两行同号:unpaired 配对语义照旧(1 号未答 → 出现一次)
    verdicts = parse_verdict_lines(text)
    assert [v for v in verdicts if v["kind"] == "待裁决"] == [
        {"kind": "待裁决", "number": 3},
        {"kind": "待裁决", "number": 3},
    ]


def test_append_pending_question_missing_report(tmp_path):
    """用例 7:报告不存在 → FileNotFoundError(报告必须先存在,调用方保证)。"""
    with pytest.raises(FileNotFoundError):
        checks_mod.append_pending_question(tmp_path / "docs" / "nope.md", 1, "问题")


# ---------- 裁决追加(D-P3-19 同号拒绝) ----------

def test_append_user_verdict_and_same_number_reject(tmp_path):
    """用例 8:追加 `> 裁决:#3:修`;同号裁决已存在 → FileExistsError
    (一问一答,不重复受理)。"""
    report = _make_report(tmp_path)
    checks_mod.append_pending_question(report, 3, "范围问题")

    result = checks_mod.append_user_verdict(report, 3, "修")
    assert result == report
    text = report.read_text(encoding="utf-8")
    assert text.splitlines()[-1].strip() == "> 裁决:#3:修"
    # 同号配对成立:unpaired 语义经锁定函数复核
    assert parse_verdict_lines(text) == [
        {"kind": "待裁决", "number": 3},
        {"kind": "裁决", "number": 3},
    ]

    # 同号拒绝:再次追加 #3 → FileExistsError
    with pytest.raises(FileExistsError, match="#3 已有裁决"):
        checks_mod.append_user_verdict(report, 3, "再答一次")


def test_append_user_verdict_missing_report(tmp_path):
    """用例 8b:报告不存在 → FileNotFoundError。"""
    with pytest.raises(FileNotFoundError):
        checks_mod.append_user_verdict(tmp_path / "docs" / "nope.md", 1, "修")


# ---------- PASS 收口(D-P3-17 收口半 / §6.4 末行锚点) ----------

def test_append_pass_conclusion_becomes_last_anchor(tmp_path):
    """用例 9:追加后 `> 核查结论:PASS(…)` 成为最后一个非空行——
    is_pass_conclusion 断言转 True(末行锚点的机器证明)。"""
    report = _make_report(tmp_path)
    assert is_pass_conclusion(report.read_text(encoding="utf-8")) is False  # 前置:FIX
    checks_mod.append_pass_conclusion(report, "残余裁决收口")
    text = report.read_text(encoding="utf-8")
    assert is_pass_conclusion(text) is True, "PASS 行必须成为末锚点"
    assert text.splitlines()[-1].strip() == "> 核查结论:PASS(残余裁决收口)"
    # 正文保全:FIX 结论行仍在(双结论行,锚点取末一处——§6.4)
    assert "> 核查结论:FIX(P1×1)" in text


def test_append_pass_conclusion_idempotent_no_duplicate(tmp_path):
    """用例 10:已 PASS 的报告再调 → 不重复追加(幂等二跳)。"""
    report = _make_report(tmp_path)
    checks_mod.append_pass_conclusion(report, "残余裁决收口")
    once = report.read_text(encoding="utf-8")
    checks_mod.append_pass_conclusion(report, "残余裁决收口")
    assert report.read_text(encoding="utf-8") == once, "已 PASS 不重复追加"
    assert once.count("> 核查结论:PASS") == 1

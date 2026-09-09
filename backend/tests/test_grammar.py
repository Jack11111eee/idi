# -*- coding: utf-8 -*-
"""§6.4 六条机器文法(D-P2-16~19 / FLOW-07 / ROADMAP 成功判据 6)单元测试:正反例矩阵。

样本 helper 手造最小合规轮次文档(五件套:批注回应表 + 决策登记标题 +
维度表 + 未决清单 + 末行授权标记);表头逐字用 §6.4/§6.3 字面:
  | 批注id | 原文摘录 | 回应 |
  | 维度 | 状态 | 说明 |
  | 编号 | 问题 | 状态 |
D-P2-19:不读本项目 docs/discuss-round-0~4 做输入,全部手造。

用例矩阵(D-P2-17 逐项):
  维度表:全绿 / 含◐ / 含✗ / 空表 / 状态列脏值(fail-closed)/ 无表
  未决清单:清零 / 有待决 / 脏值状态列
  授权标记:是 / 否 / 前缀 / 后缀 / 末行后空行 / 空文档
  回应表:正常提取 / 空 id 行跳过 / 空表 / 解析器只提取不配对
  PASS:仅FIX / PASS / 带括注 / 双结论行锚点取末一处
  裁决:同号配对 / 未配对 / 锚前行不收 / 形态不符
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.grammar import (  # noqa: E402
    is_dimension_table_green,
    is_pass_conclusion,
    is_pending_list_clear,
    parse_annotation_responses,
    parse_auth_marker,
    parse_dimension_table,
    parse_pending_list,
    parse_verdict_lines,
    unpaired_verdicts,
)
from backend.state import (  # noqa: E402
    AUTH_MARKER_NO,
    AUTH_MARKER_YES,
    PASS_PREFIX,
)

AUTH_YES = AUTH_MARKER_YES
AUTH_NO = AUTH_MARKER_NO


def make_round_doc(
    dimension_table: str = "| 维度 | 状态 | 说明 |\n|------|------|------|\n| 目标与边界 | ✓ | 已明确 |",
    pending_list: str = "| 编号 | 问题 | 状态 |\n|------|------|------|\n| Q1 | 部署形态? | 已决 |",
    response_table: str = "| 批注id | 原文摘录 | 回应 |\n|------|------|------|\n| a1-01 | 某段原文 | 已按意见补充 |",
    marker: str = AUTH_NO,
    trailing: str = "\n",
) -> str:
    """手造最小合规轮次文档(五件套,§6.3/§6.4 表头逐字)。"""
    return (
        "# 第 N 轮讨论\n\n"
        "## 1. 批注回应(处置)\n\n"
        f"{response_table}\n\n"
        "## 2. 决策登记\n\n"
        "| 决策 | 内容 |\n|------|------|\n| D-01 | 示例 |\n\n"
        "## 3. 覆盖维度表\n\n"
        f"{dimension_table}\n\n"
        "## 4. 未决问题清单\n\n"
        f"{pending_list}\n\n"
        f"{marker}{trailing}"
    )


# ---------- 维度表(D-P2-16 条 1) ----------

def test_dimension_table_all_green():
    # 用例 1(维度表全绿):状态列全部 ✓ → is_dimension_table_green True
    text = make_round_doc(
        dimension_table="| 维度 | 状态 | 说明 |\n|------|------|------|\n"
                       "| 目标与边界 | ✓ | 已明确 |\n| 用户与场景 | ✓ | 两类场景已定 |"
    )
    assert is_dimension_table_green(text) is True


def test_dimension_table_half_or_cross_not_green():
    # 用例 2(非全绿):含 ◐ 或 ✗ → False
    half = make_round_doc(
        dimension_table="| 维度 | 状态 | 说明 |\n|------|------|------|\n"
                       "| 流程与状态 | ◐ | 仍有草图 |"
    )
    assert is_dimension_table_green(half) is False
    cross = make_round_doc(
        dimension_table="| 维度 | 状态 | 说明 |\n|------|------|------|\n"
                        "| 目标与边界 | ✗ | 未覆盖 |"
    )
    assert is_dimension_table_green(cross) is False


def test_dimension_table_empty_is_green():
    # 用例 3(空表):无行动 = 绿(判定写进 DESIGN 假设:无 ◐ 无 ✗ 即绿)
    text = make_round_doc(
        dimension_table="| 维度 | 状态 | 说明 |\n|------|------|------|"
    )
    assert is_dimension_table_green(text) is True


def test_dimension_table_dirty_status_fail_closed():
    # 用例 4(脏值 fail-closed,刻意偏离 §6.4 字面):状态列值不在 {✓,◐,✗}
    # (如「待定」)→ 该行视为非绿(False)
    text = make_round_doc(
        dimension_table="| 维度 | 状态 | 说明 |\n|------|------|------|\n"
                        "| 数据与落盘 | ✓ | 已定 |\n| 异常与失败处理 | 待定 | 未讨论 |"
    )
    assert is_dimension_table_green(text) is False


def test_dimension_table_no_table_or_malformed():
    # 边界:无维度表(标题缺失)→ 空列表 + 不绿不抛(畸形输入给确定判定,T-idi02-01)
    no_table = "# 只有标题\n\n正文\n\n" + AUTH_NO
    assert parse_dimension_table(no_table) == []
    assert is_dimension_table_green(no_table) is True  # 空表语义 = 无行动 = 绿

    empty_text = ""
    assert parse_dimension_table(empty_text) == []
    assert is_dimension_table_green(empty_text) is True


def test_dimension_table_parse_rows():
    # 解析返回行结构({"dimension","status","note"};表头丢弃、列 strip)
    text = make_round_doc(
        dimension_table="| 维度 | 状态 | 说明 |\n|------|------|------|\n"
                       "| 目标与边界 | ✓ | round-0 基线 |"
    )
    rows = parse_dimension_table(text)
    assert rows == [{"dimension": "目标与边界", "status": "✓", "note": "round-0 基线"}]


# ---------- 未决清单(D-P2-16 条 2) ----------

def test_pending_list_clear_when_no_wait():
    # 用例 5(清单清零):无「待决」行 → True
    text = make_round_doc(
        pending_list="| 编号 | 问题 | 状态 |\n|------|------|------|\n"
                     "| Q1 | 部署形态? | 已决 |\n| Q2 | 多人协作? | 不适用 |"
    )
    assert is_pending_list_clear(text) is True


def test_pending_list_pending_open_not_clear():
    # 用例 6(有待决):存在待决行 → False
    text = make_round_doc(
        pending_list="| 编号 | 问题 | 状态 |\n|------|------|------|\n"
                     "| Q1 | 部署形态? | 已决 |\n| Q2 | 中期接手怎么算? | 待决 |"
    )
    assert is_pending_list_clear(text) is False


def test_pending_list_empty_is_clear():
    # 空清单(全部已决,无数据行)→ 清零
    text = make_round_doc(
        pending_list="| 编号 | 问题 | 状态 |\n|------|------|------|"
    )
    assert is_pending_list_clear(text) is True


def test_pending_list_status_dirty_value_counts_as_open():
    # 边界(与维度表不同):清单只判「无待决」,脏值行不算待决 → 清零。
    # 但解析器仍返回行数据(判定留给调用方;此用例锁定该语义)
    text = make_round_doc(
        pending_list="| 编号 | 问题 | 状态 |\n|------|------|------|\n"
                     "| Q1 | 部署形态? | 已解决 |"
    )
    rows = parse_pending_list(text)
    assert rows == [{"number": "Q1", "question": "部署形态?", "status": "已解决"}]
    assert is_pending_list_clear(text) is True  # 无「待决」字样即清零


def test_pending_list_no_heading_is_empty():
    # 无未决清单标题 → 空列表(畸形输入给确定判定)
    assert parse_pending_list("# 无清单\n\n正文\n" + AUTH_NO) == []


# ---------- 授权申请标记(D-P2-16 条 3,复用 state 常量) ----------

def test_auth_marker_yes_and_no_exact():
    # 用例 7(是/否):末非空行恰为两串之一 → "yes"/"no"
    assert parse_auth_marker(f"# 文档\n\n{AUTH_NO}\n") == "no"
    assert parse_auth_marker(f"# 文档\n\n{AUTH_YES}\n") == "yes"


def test_auth_marker_dirty_variants_return_none():
    # 用例 8(脏变体):前缀、后缀、末行后空白 → None(非两串之一)
    assert parse_auth_marker(f"# 文档\n\n前缀 {AUTH_NO}\n") is None
    assert parse_auth_marker(f"# 文档\n\n{AUTH_NO}的后缀\n") is None


def test_auth_marker_trailing_blank_lines_after_marker():
    # 末行后空行:标记仍是最后一个非空行 → 合规(照 last_nonempty_line 语义)
    assert parse_auth_marker(f"# 文档\n\n{AUTH_NO}\n\n\n") == "no"


def test_auth_marker_empty_text():
    # 空文档 / 无标记 → None
    assert parse_auth_marker("") is None
    assert parse_auth_marker("# 只有标题\n") is None


# ---------- 批注回应表(D-P2-16 条 4,供 writeback 配对) ----------

def test_annotation_responses_extract_rows():
    # 用例 9(正常提取):id/quote/response 三列可提取,表头丢弃、列 strip
    text = make_round_doc(
        response_table="| 批注id | 原文摘录 | 回应 |\n|------|------|------|\n"
                       "| a1-01 | 「范围太大」 | 已收窄到单机单人 |\n"
                       "| a1-02 | 「没有权限门」 | 权限规则已补 |"
    )
    rows = parse_annotation_responses(text)
    assert rows == [
        {"id": "a1-01", "quote": "「范围太大」", "response": "已收窄到单机单人"},
        {"id": "a1-02", "quote": "「没有权限门」", "response": "权限规则已补"},
    ]


def test_annotation_responses_empty_id_row_skipped():
    # 用例 10(id 空):id 列 strip 后为空的行 → 跳过,不抛
    text = make_round_doc(
        response_table="| 批注id | 原文摘录 | 回应 |\n|------|------|------|\n"
                       "|   | 空白 id 的行 | 不进结果 |\n"
                       "| a1-01 | 有 id 的行 | 进结果 |"
    )
    rows = parse_annotation_responses(text)
    assert rows == [{"id": "a1-01", "quote": "有 id 的行", "response": "进结果"}]


def test_annotation_responses_empty_table_and_missing_heading():
    # 空表 / 标题缺失 → 空列表(畸形输入给确定判定)
    empty = make_round_doc(response_table="| 批注id | 原文摘录 | 回应 |\n|------|------|------|")
    assert parse_annotation_responses(empty) == []
    assert parse_annotation_responses(f"# 无回应表\n\n{AUTH_NO}\n") == []


def test_annotation_responses_parser_does_not_match_ids():
    # 解析器只提取不配对:未出现的 id 不出现在结果里(配对是 writeback 的职责)
    rows = parse_annotation_responses(make_round_doc())
    assert all(row["id"] != "a9-99" for row in rows)


def test_annotation_responses_unrelated_heading_not_collected():
    # 标题不含关键词的二级标题下的表格不被误收(§6.4 标题定位)
    text = (
        "## 术语表\n\n"
        "| 术语 | 大白话 |\n|------|------|\n| 批注 | 划词写话 |\n\n"
        f"{AUTH_NO}\n"
    )
    assert parse_annotation_responses(text) == []


# ---------- PASS 结论行(D-P2-16 条 5,锚点取末一处) ----------

def test_pass_conclusion_pass_and_fix():
    # 用例 11(PASS / 仅 FIX):末锚点行前缀匹配 PASS_PREFIX → True;FIX → False
    assert is_pass_conclusion(f"# 报告\n\n{PASS_PREFIX}\n") is True
    assert is_pass_conclusion("# 报告\n\n> 核查结论:FIX(2 项)\n") is False


def test_pass_conclusion_with_annotation_suffix():
    # 用例 12(带括注):"> 核查结论:PASS(问题 N 项修复完毕)" → True(前缀匹配)
    assert is_pass_conclusion("# 报告\n\n> 核查结论:PASS(问题 3 项修复完毕)\n") is True


def test_pass_conclusion_double_conclusion_lines_takes_last():
    # 用例 13(双结论行,锚点取末一处):第一处 FIX、第二处 PASS → 取末锚点 → True
    text = (
        "# 报告\n\n"
        "> 核查结论:FIX(2 项)\n\n"
        "正文若干……\n\n"
        "> 核查结论:PASS(问题 2 项修复完毕)\n"
    )
    assert is_pass_conclusion(text) is True


def test_pass_conclusion_double_lines_last_is_fix():
    # 双结论行反向:第一处 PASS、第二处 FIX → 取末锚点(FIX)→ False
    text = (
        "# 报告\n\n"
        "> 核查结论:PASS\n\n"
        "后续又发现新问题……\n\n"
        "> 核查结论:FIX(1 项)\n"
    )
    assert is_pass_conclusion(text) is False


def test_pass_conclusion_no_conclusion_line():
    # 无结论行 / 空文档 → False(给确定判定,不抛)
    assert is_pass_conclusion("# 报告\n\n正文没有结论行\n") is False
    assert is_pass_conclusion("") is False


# ---------- 裁决追加行(D-P2-16 条 6,同号配对 / 锚点之后) ----------

def test_verdict_unpaired_pending_line():
    # 用例 14(未配对):结论行之后 "> 待裁决:#1:" 无同号裁决 → pending 含 1
    text = (
        "# 报告\n\n"
        "> 核查结论:FIX(1 项)\n\n"
        "> 待裁决:#1:这个范围问题属于用户职权吗?\n"
    )
    assert parse_verdict_lines(text) == [{"kind": "待裁决", "number": 1}]
    assert unpaired_verdicts(text) == [1]


def test_verdict_same_number_pairs_up():
    # 用例 15(同号配对):"> 裁决:#1:" 同号追加后 → 配对消失(不进 unpaired)
    text = (
        "# 报告\n\n"
        "> 核查结论:FIX(1 项)\n\n"
        "> 待裁决:#1:这个范围问题属于用户职权吗?\n\n"
        "> 裁决:#1:属于,按建议收窄处理。\n"
    )
    assert parse_verdict_lines(text) == [
        {"kind": "待裁决", "number": 1},
        {"kind": "裁决", "number": 1},
    ]
    assert unpaired_verdicts(text) == []


def test_verdict_multiple_numbers_partial_pairing():
    # 多组问答共存:K 递增;1 号配对、2 号未配对 → unpaired 只含 2
    text = (
        "# 报告\n\n"
        "> 核查结论:FIX(2 项)\n\n"
        "> 待裁决:#1:问题一?\n\n"
        "> 裁决:#1:回答一。\n\n"
        "> 待裁决:#2:问题二?\n"
    )
    assert unpaired_verdicts(text) == [2]


def test_verdict_lines_before_conclusion_not_counted():
    # 用例 16(锚前行不收):报告头部(结论行之前)的待裁决样式行 → 不进配对空间
    text = (
        "# 报告\n\n"
        "> 待裁决:#9:头部提到的问题(不应计入)\n\n"
        "> 核查结论:FIX(1 项)\n\n"
        "> 待裁决:#1:结论行之后的问题(应计入)\n"
    )
    assert parse_verdict_lines(text) == [{"kind": "待裁决", "number": 1}]
    assert unpaired_verdicts(text) == [1]


def test_verdict_malformed_shape_not_verdict_line():
    # 用例 17(形态不符):"> 待裁决 1:"(缺 #/冒号)不是裁决行
    text = (
        "# 报告\n\n"
        "> 核查结论:FIX(1 项)\n\n"
        "> 待裁决 1:形态不符的行\n"
    )
    assert parse_verdict_lines(text) == []
    assert unpaired_verdicts(text) == []


def test_verdict_no_conclusion_line_empty():
    # 无结论行 → 配对空间为空(锚点不存在,尾部不收)
    text = "# 报告\n\n> 待裁决:#1:没有锚点的行\n"
    assert parse_verdict_lines(text) == []
    assert unpaired_verdicts(text) == []


# ---------- 混合场景:五件套手造文档逐项判定 ----------

def test_full_sample_all_checks_pass():
    # 用例 18(五件套全绿):手造合规文档全判定通过(维度全绿/清单清零/标记 no)
    text = make_round_doc()
    assert is_dimension_table_green(text) is True
    assert is_pending_list_clear(text) is True
    assert parse_auth_marker(text) == "no"
    assert len(parse_annotation_responses(text)) == 1

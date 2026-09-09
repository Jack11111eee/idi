# -*- coding: utf-8 -*-
"""§6.4 六条机器文法解析器(DESIGN.md §6.4 / FLOW-07 / D-P2-16~19)。

解析(返回结构化数据)与判定(返回 bool)分离,照 state.py 的
list_complete_rounds / is_complete_round 分离风格;授权标记与 PASS 前缀
常量直接复用 backend.state(D-P2-16:同一语义不复制第二份,本模块源码
无第二处标记字符串字面量定义)。

六条覆盖(§6.4 表 + PASS/裁决段):
  1. 维度表:二级标题含「覆盖维度表」,列 = 维度/状态/说明,状态 ∈ {✓,◐,✗};
     全绿 ⇔ 无 ◐ 与 ✗(+ 状态列脏值 fail-closed,见 is_dimension_table_green)
  2. 未决清单:二级标题含「未决问题清单」,列 = 编号/问题/状态;清零 ⇔ 无待决
  3. 授权申请标记:文档最后一个非空行恰为两串之一(复用 state 常量与
     last_nonempty_line,exact match after strip——前缀不算,后缀不算)
  4. 批注回应表:二级标题含「批注回应」,列 = 批注id/原文摘录/回应;
     id 是回写配对的唯一依据(供 annotations.writeback 消费,D-P2-13)
  5. PASS 结论行:结论行锚点取最后一处 `> 核查结论:` 行,该行前缀匹配
     state.PASS_PREFIX
  6. 裁决追加行:`> (待裁决|裁决):#K:` 形态;仅统计结论行之后;同号配对

本模块只解析实施后新生成的轮次文档——不回溯解析本仓库历史轮文档
(D-P2-19);解析函数对任意畸形输入(空文档/无标题/空表格/脏表格行)
给确定判定不抛(T-idi02-01)。
零第三方依赖、纯标准库文本函数,无磁盘 IO。
"""
from __future__ import annotations

import re

from backend.state import (
    AUTH_MARKER_YES,
    AUTH_MARKER_NO,
    PASS_PREFIX,
    last_nonempty_line,
)

__all__ = [
    "parse_dimension_table",
    "is_dimension_table_green",
    "parse_pending_list",
    "is_pending_list_clear",
    "parse_auth_marker",
    "parse_annotation_responses",
    "is_pass_conclusion",
    "parse_verdict_lines",
    "unpaired_verdicts",
]

# §6.4 裁决追加行形态:"> (待裁决|裁决):#K:"(strip 后匹配;待裁决在前,
# 防止「裁决」前缀歧义——交替匹配按书写顺序取先者)
_VERDICT_RE = re.compile(r"^>\s*(待裁决|裁决):#(\d+):")

# §6.4 结论行锚点前缀(锚点取最后一处以它开头的行;PASS 判定前缀复用 state)
_CONCLUSION_LINE_PREFIX = "> 核查结论:"

# 维度表状态列合法值(§6.4:状态 ∈ {✓, ◐, ✗};全绿 ⇔ 无 ◐ 与 ✗)
_STATUS_GREEN = "✓"
_STATUS_HALF = "◐"
_STATUS_CROSS = "✗"
_KNOWN_DIM_STATUSES = {_STATUS_GREEN, _STATUS_HALF, _STATUS_CROSS}

# 未决清单状态列开放值(§6.4:清零 ⇔ 无状态为「待决」的行)
_PENDING_OPEN = "待决"

# 裁决行 kind(§6.4:待裁决 = 修复者抛出的第 K 问;裁决 = 用户对第 K 问的回答)
_VERDICT_PENDING = "待裁决"
_VERDICT_ANSWERED = "裁决"


def parse_dimension_table(md_text: str) -> list[dict]:
    """解析维度表为 [{"dimension", "status", "note"}](RED 骨架:未实现)。"""
    raise NotImplementedError("parse_dimension_table 尚未实现(Task 2 GREEN 阶段实现)")


def is_dimension_table_green(md_text: str) -> bool:
    """维度表全绿判定(RED 骨架:未实现)。"""
    raise NotImplementedError("is_dimension_table_green 尚未实现(Task 2 GREEN 阶段实现)")


def parse_pending_list(md_text: str) -> list[dict]:
    """解析未决清单为 [{"number", "question", "status"}](RED 骨架:未实现)。"""
    raise NotImplementedError("parse_pending_list 尚未实现(Task 2 GREEN 阶段实现)")


def is_pending_list_clear(md_text: str) -> bool:
    """未决清单清零判定(RED 骨架:未实现)。"""
    raise NotImplementedError("is_pending_list_clear 尚未实现(Task 2 GREEN 阶段实现)")


def parse_auth_marker(md_text: str) -> str | None:
    """授权申请标记三态解析:"yes"/"no"/None(RED 骨架:未实现)。"""
    raise NotImplementedError("parse_auth_marker 尚未实现(Task 2 GREEN 阶段实现)")


def parse_annotation_responses(md_text: str) -> list[dict]:
    """解析批注回应表为 [{"id", "quote", "response"}](RED 骨架:未实现)。"""
    raise NotImplementedError("parse_annotation_responses 尚未实现(Task 2 GREEN 阶段实现)")


def is_pass_conclusion(md_text: str) -> bool:
    """PASS 结论行判定(锚点取末一处,RED 骨架:未实现)。"""
    raise NotImplementedError("is_pass_conclusion 尚未实现(Task 2 GREEN 阶段实现)")


def parse_verdict_lines(md_text: str) -> list[dict]:
    """解析结论行之后的裁决追加行(RED 骨架:未实现)。"""
    raise NotImplementedError("parse_verdict_lines 尚未实现(Task 2 GREEN 阶段实现)")


def unpaired_verdicts(md_text: str) -> list[int]:
    """未配对的待裁决编号列表(RED 骨架:未实现)。"""
    raise NotImplementedError("unpaired_verdicts 尚未实现(Task 2 GREEN 阶段实现)")

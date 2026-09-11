# -*- coding: utf-8 -*-
"""自检磁盘签名读写纯函数(PLAN idi-03-01 Task 3 / DATA-04 / DESIGN.md §8.2 / §6.4 / D-P3-11 / D-P3-12 / D-P3-17 / D-P3-19)。

Phase 3 自检侧的纯函数层,两组六件:

档位签名三件(tier 签名文件,§8.2「档位记录于报告头部落盘」的选档落盘半):
  - write_tier(project, tier):落盘 docs/DESIGN-check-tier.md,头部一行
    `> 自检档位:严格|宽松`(覆盖式写入幂等,重选档可改);白名单外值 → ValueError
  - read_tier(project):文件不存在/脏内容 → None + warning(不抛)
  报告未出窗口期的中间态凭证;报告头部行格式与签名文件同字面(D-P3-12)。

报告尾部追加三件(裁决追加文法 §6.4,「结论行之后追加 + 不改写正文」):
  - append_pending_question(report_path, number, text):追加 `> 待裁决:#K:…`;
    内容级幂等(同内容已存在 → 跳过返回 False)
  - append_user_verdict(report_path, number, text):追加 `> 裁决:#K:…`;
    同号裁决已存在 → FileExistsError(同号拒绝,一问一答,D-P3-19)
  - append_pass_conclusion(report_path, note):追加 `> 核查结论:PASS(…)`;
    已 PASS → 直接返回不重复追加(幂等)

三类追加都只 append 到文件尾,不改写正文任何行(T-idi03-03:追加动作
不得改写报告正文破坏审计)。同号判定复用 grammar.parse_verdict_lines
(锁定函数只读消费,不重实现第二套)。

零第三方依赖、纯 pathlib,不碰 FastAPI/AI 层。
"""
from __future__ import annotations

import logging
from pathlib import Path

from backend.grammar import (
    TIER_LINE_LOOSE,
    TIER_LINE_STRICT,
    is_pass_conclusion,
    parse_verdict_lines,
)

logger = logging.getLogger(__name__)

# §6.1/§8.2:档位签名文件(docs/ 下,未编号;报告头部行格式与之同字面,D-P3-11/D-P3-12)
TIER_FILENAME = "DESIGN-check-tier.md"

# 档位合法值白名单(§8.2 两档)
TIER_VALUES = {"严格", "宽松"}

_TIER_LINE_BY_VALUE = {"严格": TIER_LINE_STRICT, "宽松": TIER_LINE_LOOSE}


def write_tier(project_path: Path, tier: str) -> Path:
    """落盘档位签名文件 docs/DESIGN-check-tier.md(覆盖式,幂等),返回路径。

    头部一行 = `> 自检档位:严格|宽松`(常量逐字,不手拼);tier 不在
    TIER_VALUES 白名单 → ValueError(中文消息)。覆盖写入:重选档覆盖旧值
    (D-P3-11:选档落盘可重选,幂等非一次性)。(RED 骨架:未实现)
    """
    raise NotImplementedError("write_tier 尚未实现(Task 3 GREEN 阶段实现)")


def read_tier(project_path: Path) -> str | None:
    """读档位签名:首非空行 strip 恰为两常量之一 → 对应值;否则 None。

    文件不存在 → None;脏内容 → None + warning 日志(不抛,照
    annotations.load 的「读不到给确定判定」模子,D-P3-12)。
    (RED 骨架:未实现)
    """
    raise NotImplementedError("read_tier 尚未实现(Task 3 GREEN 阶段实现)")


def append_pending_question(report_path: Path, number: int, text: str) -> bool:
    """向报告末尾追加 `> 待裁决:#K:…` 行;已存在同内容行 → 返回 False 不追加。

    内容级幂等(§6.4:仅当该问题尚无同内容待裁决行时追加);同号新内容
    → 追加第二行(幂等为内容级非号级,判定式按同号配对不受影响)。
    报告不存在 → FileNotFoundError(报告必须先存在,调用方保证)。
    (RED 骨架:未实现)
    """
    raise NotImplementedError("append_pending_question 尚未实现(Task 3 GREEN 阶段实现)")


def append_user_verdict(report_path: Path, number: int, text: str) -> Path:
    """向报告末尾追加 `> 裁决:#K:…` 行,返回报告路径。

    同号裁决行已存在(parse_verdict_lines 判定,锁定函数只读消费)→
    FileExistsError(中文:「#K 已有裁决,一问一答,不重复受理」——
    D-P3-19 择拒绝重复 POST 同号的纯函数层)。报告不存在 → FileNotFoundError。
    (RED 骨架:未实现)
    """
    raise NotImplementedError("append_user_verdict 尚未实现(Task 3 GREEN 阶段实现)")


def append_pass_conclusion(report_path: Path, note: str) -> Path:
    """向报告末尾追加 `> 核查结论:PASS(note)` 行,返回报告路径。

    追加后该行成为报告最后一个非空行(grammar.is_pass_conclusion → True
    是机器证明);报告已 PASS(is_pass_conclusion 现文 True)→ 直接返回
    不重复追加(幂等,D-P3-17 收口半)。(RED 骨架:未实现)
    """
    raise NotImplementedError("append_pass_conclusion 尚未实现(Task 3 GREEN 阶段实现)")

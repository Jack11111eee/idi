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
    (D-P3-11:选档落盘可重选,幂等非一次性)。
    """
    if tier not in TIER_VALUES:
        raise ValueError(f"档位必须是 {'/'.join(sorted(TIER_VALUES))},收到: {tier!r}")
    project = Path(project_path)
    tier_path = project / "docs" / TIER_FILENAME
    tier_path.parent.mkdir(parents=True, exist_ok=True)  # docs/ 理论上已存在,防御
    # 单行文件(头部行即全文):tier 参数选常量,不手拼字符串
    tier_path.write_text(f"{_TIER_LINE_BY_VALUE[tier]}\n", encoding="utf-8")
    logger.info("档位签名落盘:%s(%s)", tier_path, tier)
    return tier_path


def read_tier(project_path: Path) -> str | None:
    """读档位签名:首非空行 strip 恰为两常量之一 → 对应值;否则 None。

    文件不存在 → None;脏内容 → None + warning 日志(不抛,照
    annotations.load 的「读不到给确定判定」模子,D-P3-12)。
    """
    tier_path = Path(project_path) / "docs" / TIER_FILENAME
    if not tier_path.is_file():
        return None
    try:
        text = tier_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        logger.warning("读取 %s 失败,按无档位处理: %s", tier_path, exc)
        return None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        for value, line_literal in _TIER_LINE_BY_VALUE.items():
            if stripped == line_literal:
                return value
        logger.warning("%s 内容脏(头部行非合法档位行),按无档位处理", tier_path)
        return None  # 首非空行不合法即脏
    return None  # 全空文件视为脏


def _read_report(report_path: Path) -> str:
    """读报告现文;不存在 → FileNotFoundError(报告必须先存在,调用方保证)。"""
    path = Path(report_path)
    if not path.is_file():
        raise FileNotFoundError(f"报告不存在({path})——先由核查调用产出报告再追加")
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        logger.warning("读取 %s 失败: %s", path, exc)
        raise


def _append_line(report_path: Path, current: str, line: str) -> None:
    """在报告末尾追加一行(现文 rstrip + 空行 + 行;不改写正文任何行)。"""
    Path(report_path).write_text(
        f"{current.rstrip()}\n\n{line}\n", encoding="utf-8"
    )


def append_pending_question(report_path: Path, number: int, text: str) -> bool:
    """向报告末尾追加 `> 待裁决:#K:…` 行;已存在同内容行 → 返回 False 不追加。

    内容级幂等(§6.4:仅当该问题尚无同内容待裁决行时追加);同号新内容
    → 追加第二行(幂等为内容级非号级,判定式按同号配对不受影响)。
    报告不存在 → FileNotFoundError(报告必须先存在,调用方保证)。
    """
    path = Path(report_path)
    current = _read_report(path)
    line = f"> 待裁决:#{number}:{text}"
    if line in current.splitlines():
        return False  # 内容级幂等:同内容行已在,跳过
    _append_line(path, current, line)
    return True


def append_user_verdict(report_path: Path, number: int, text: str) -> Path:
    """向报告末尾追加 `> 裁决:#K:…` 行,返回报告路径。

    同号裁决行已存在(parse_verdict_lines 判定,锁定函数只读消费)→
    FileExistsError(中文:「#K 已有裁决,一问一答,不重复受理」——
    D-P3-19 择拒绝重复 POST 同号的纯函数层)。报告不存在 → FileNotFoundError。
    """
    path = Path(report_path)
    current = _read_report(path)
    for verdict in parse_verdict_lines(current):
        if verdict["kind"] == "裁决" and verdict["number"] == number:
            raise FileExistsError(
                f"#{number} 已有裁决,一问一答,不重复受理"
            )
    _append_line(path, current, f"> 裁决:#{number}:{text}")
    return path


def append_pass_conclusion(report_path: Path, note: str) -> Path:
    """向报告末尾追加 `> 核查结论:PASS(note)` 行,返回报告路径。

    追加后该行成为报告最后一个非空行(grammar.is_pass_conclusion → True
    是机器证明);报告已 PASS(is_pass_conclusion 现文 True)→ 直接返回
    不重复追加(幂等,D-P3-17 收口半)。
    """
    path = Path(report_path)
    current = _read_report(path)
    if is_pass_conclusion(current):
        return path  # 已 PASS,不重复追加
    _append_line(path, current, f"> 核查结论:PASS({note})")
    return path

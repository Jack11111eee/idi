# -*- coding: utf-8 -*-
"""derive_state(project_path) 纯函数——DESIGN.md v1.13 §7.4 八行推导表的完整实现。

「文件即状态」(D-19/D-P1-11):工具不维护独立流程状态,一切由磁盘现状推导。
推导表自上而下首条命中即取,行间条件已互斥化——严格照抄表条件,不自行改写组合。

完整轮判据(§7.3):最新轮次文档末行不是合规 `> 申请授权:是|否` 标记(§6.4)
即判半成品、视为不存在——当前轮取最大完整轮。

零第三方依赖、零全局状态:纯 pathlib + 标准库,不碰 FastAPI 层。
"""
from __future__ import annotations

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

# §7.4 状态常量(Phase 2/3 按钮逻辑消费)
STATE_PHASE1_NEW = "phase1_new"
STATE_PHASE12_IN_PROGRESS = "phase12_in_progress"
STATE_PHASE3 = "phase3"
STATE_PHASE4 = "phase4"
STATE_PHASE5_AWAITING_TIER = "phase5_awaiting_tier"
STATE_PHASE5_CHECKING = "phase5_checking"
STATE_MISSION_COMPLETE = "mission_complete"

# §6.4 授权申请标记:恰为这两个字符串之一(exact match after strip——前缀不算,后缀不算)
AUTH_MARKER_YES = "> 申请授权:是"
AUTH_MARKER_NO = "> 申请授权:否"
_AUTH_MARKERS = (AUTH_MARKER_YES, AUTH_MARKER_NO)

# §7.4 PASS 结论行:前缀匹配(其后可附括注,如 "> 核查结论:PASS(问题 N 项修复完毕)")
PASS_PREFIX = "> 核查结论:PASS"

# 文件名形态:编号有界([0-9]+),防畸形文件名注入
_ROUND_RE = re.compile(r"^discuss-round-(\d+)\.md$")
_CHECK_RE = re.compile(r"^DESIGN-check-(\d+)\.md$")

_ROUND_TEMPLATE = "discuss-round-{n}.md"
_CHECK_TEMPLATE = "DESIGN-check-{n}.md"


def last_nonempty_line(md_text: str) -> str | None:
    """返回文档最后一个非空行(行 strip 后取末一个非空);全空返回 None。"""
    last: str | None = None
    for line in md_text.splitlines():
        stripped = line.strip()
        if stripped:
            last = stripped
    return last


def is_complete_round(md_text: str) -> bool:
    """§7.3 完整轮判据 + §6.4 授权申请标记:最后一个非空行恰为合规标记(exact,strip 后全等)。"""
    last = last_nonempty_line(md_text)
    return last in _AUTH_MARKERS


def list_complete_rounds(docs_dir: Path) -> list[int]:
    """docs/ 下末行合规的 discuss-round-{N}.md 编号列表(升序);半成品轮视为不存在。"""
    if not docs_dir.is_dir():
        return []
    numbers: list[int] = []
    for entry in sorted(docs_dir.iterdir()):
        match = _ROUND_RE.match(entry.name)
        if not match or not entry.is_file():
            continue
        if is_complete_round(_read_text(entry)):
            numbers.append(int(match.group(1)))
    return sorted(numbers)


def max_check_number(docs_dir: Path) -> int | None:
    """docs/ 下 DESIGN-check-{N}.md 的最大编号;不存在返回 None。不校验报告内容完整性(半成品报告重跑覆盖)。"""
    if not docs_dir.is_dir():
        return None
    numbers: list[int] = []
    for entry in docs_dir.iterdir():
        match = _CHECK_RE.match(entry.name)
        if match and entry.is_file():
            numbers.append(int(match.group(1)))
    return max(numbers) if numbers else None


def latest_check_content(docs_dir: Path) -> str | None:
    """最新编号 DESIGN-check 报告的文本;不存在返回 None。"""
    latest = max_check_number(docs_dir)
    if latest is None:
        return None
    return _read_text(docs_dir / _CHECK_TEMPLATE.format(n=latest))


def derive_state(project_path: Path) -> dict:
    """按 §7.4 八行推导表(自上而下,首条命中即取)由磁盘现状推导流程状态。

    返回 {state: str, current_round: int|None, current_check: int|None};
    current_round 仅 phase3、current_check 仅 phase5_checking 下有值,其余为 None。
    """
    docs_dir = project_path / "docs"
    has_docs = docs_dir.is_dir()

    # 行 1:目录内无 docs/ → 新讨论(阶段 1)
    if not has_docs:
        return _result(STATE_PHASE1_NEW)

    has_design = (project_path / "DESIGN.md").is_file()  # .tmp 残留不算(行 4 注)
    has_authorization = (project_path / "AUTHORIZATION.md").is_file()
    complete_rounds = list_complete_rounds(docs_dir)

    # 行 2:有 docs/,无完整轮,无 DESIGN.md、无 AUTHORIZATION.md
    # → 视同行 2:阶段 1-2 进行中(含"G1 定稿前的旧轮残留"情形)
    if not complete_rounds and not has_design and not has_authorization:
        return _result(STATE_PHASE12_IN_PROGRESS)

    # 行 3:有 discuss-round-1..N(N 取最大完整轮),无 DESIGN.md,且无 AUTHORIZATION.md
    # → 阶段 3,当前轮 = 最大完整 N(末轮授权标记只是 AI 的申请,授权凭证是 AUTHORIZATION.md)
    if complete_rounds and not has_design and not has_authorization:
        return _result(STATE_PHASE3, current_round=max(complete_rounds))

    # 行 4:有 AUTHORIZATION.md,无 DESIGN-check-*.md,无 DESIGN.md
    # → 阶段 4(撰写半成品只残留 DESIGN.md.tmp,不影响本行——tmp 改名是原子操作)
    if has_authorization and not has_design:
        return _result(STATE_PHASE4)

    # 行 5:有 DESIGN.md,无 DESIGN-check-*.md → 阶段 5 待选档
    # (AUTHORIZATION.md 的有无不改变本行之后的推导:DESIGN.md 的存在已意味着授权链走到位)
    if has_design:
        max_check = max_check_number(docs_dir)
        if max_check is None:
            return _result(STATE_PHASE5_AWAITING_TIER)

        latest_text = _read_text(docs_dir / _CHECK_TEMPLATE.format(n=max_check))
        last_line = last_nonempty_line(latest_text)

        # 行 7:最新 DESIGN-check-*.md 末行以 `> 核查结论:PASS` 开头 → 使命完成
        if last_line is not None and last_line.startswith(PASS_PREFIX):
            return _result(STATE_MISSION_COMPLETE)

        # 行 6:有 DESIGN.md 与若干 DESIGN-check-*.md,最新一份末行非 PASS
        # → 自检进行中,当前核查轮 = check 最大编号(半成品报告同样落此行,重跑覆盖)
        return _result(STATE_PHASE5_CHECKING, current_check=max_check)

    # 防御兜底:上方行条件已互斥化覆盖全部正常形态;若磁盘形态超出
    # §7.4 表(如 docs/ 存在但为空目录)且不匹配任何行,回退阶段 1-2 进行中。
    return _result(STATE_PHASE12_IN_PROGRESS)


def _result(state: str, current_round: int | None = None, current_check: int | None = None) -> dict:
    return {
        "state": state,
        "current_round": current_round,
        "current_check": current_check,
    }


def _read_text(path: Path) -> str:
    """逐内容读文本;非 UTF-8 内容以 errors=replace 容错(T-idi02-01:不崩、给确定判定)。"""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:  # 读不到(权限/竞态)→按空文档处理,推导给确定判定
        logger.warning("读取 %s 失败,按空文档处理: %s", path, exc)
        return ""

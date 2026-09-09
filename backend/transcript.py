# -*- coding: utf-8 -*-
"""transcript.md 的 parse / append 读写函数——DESIGN.md §6.1 文法。

文法:每条消息 = 起始行 `[user]` 或 `[ai]`(独占一行)+ 任意多行消息体,
以下一条起始行或文件末尾为界,多行消息体不需转义。

per D-P1-10:追加式落盘动作由后端在用户发送 / AI 事件回落时调用本模块执行;
transcript.md 是会话恢复(FLOW-02)的唯一数据源,G1 后永久保留。
零第三方依赖、纯 pathlib 无状态。
"""
from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

STARTER_USER = "user"
STARTER_AI = "ai"
_VALID_ROLES = (STARTER_USER, STARTER_AI)
_STARTER_LINES = {f"[{role}]": role for role in _VALID_ROLES}

TRANSCRIPT_FILENAME = "transcript.md"


def parse_transcript(path: Path) -> list[dict]:
    """解析 transcript.md 为消息列表,每条 {role: "user"|"ai", content: str}。

    逐行扫描:遇到恰等于 [user] 或 [ai] 的整行(strip 后比较)即开新条目,
    其余行累积为当前条目体,直到下一起始行或文件末尾;条目体首尾 strip、内部空行保留。
    起始行之前的非空内容(脏头,正常不出现)丢弃并打 warning 日志。
    文件不存在或为空返回 []。
    """
    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:  # 读不到(权限/竞态)→ 按无转录处理
        logger.warning("读取 %s 失败,按空转录处理: %s", path, exc)
        return []

    messages: list[dict] = []
    dirty_lines: list[str] = []
    role: str | None = None       # None = 尚未见到起始行
    body_lines: list[str] | None = None

    for line in text.splitlines():
        starter_role = _STARTER_LINES.get(line.strip())
        if starter_role is not None:
            _flush(messages, role, body_lines)
            role = starter_role
            body_lines = []
        elif body_lines is not None:
            body_lines.append(line)
        elif line.strip():  # 脏头:起始行之前的非空内容
            dirty_lines.append(line)

    _flush(messages, role, body_lines)

    if dirty_lines:
        logger.warning(
            "transcript 起始行之前出现非空内容(脏头),已丢弃 %d 行: %s",
            len(dirty_lines),
            dirty_lines,
        )
    return messages


def append_message(path: Path, role: str, content: str) -> None:
    """向 transcript.md 追加一条消息(幂等可重入:每次调用只追加新条目)。

    以 a 模式打开(不存在则创建),写入起始行 `[role]` + 换行,再写消息体 + 尾换行。
    若文件已存在、非空且末字符非换行,先补一个换行再追加(无尾换行容错)。
    role 只接受 user/ai,其它抛 ValueError。
    """
    if role not in _VALID_ROLES:
        raise ValueError(
            f"role 必须是 {'/'.join(_VALID_ROLES)},收到: {role!r}"
        )

    # 父目录不存在则建(新讨论的第一条消息:docs/ 尚未建立)
    parent = path.parent
    if not parent.is_dir():
        parent.mkdir(parents=True, exist_ok=True)

    needs_leading_newline = _ends_without_newline(path)
    with path.open("a", encoding="utf-8") as f:
        if needs_leading_newline:
            f.write("\n")
        f.write(f"[{role}]\n")
        f.write(content)
        f.write("\n")


def transcript_exists(path: Path) -> bool:
    """transcript.md 是否存在(会话是否已开始)。"""
    return path.is_file()


def _ends_without_newline(path: Path) -> bool:
    """文件已存在、非空且末字符非换行 → True(需先补换行)。"""
    if not path.is_file():
        return False
    try:
        with path.open("rb") as f:
            f.seek(0, 2)  # EOF
            size = f.tell()
            if size == 0:
                return False
            f.seek(size - 1)
            return f.read(1) != b"\n"
    except OSError as exc:
        logger.warning("检查 %s 末字符失败,按需补换行处理: %s", path, exc)
        return True


def _flush(messages: list[dict], role: str | None, body_lines: list[str] | None) -> None:
    """把当前条目(role + 体)strip 首尾后收入消息列表;body_lines 为 None 时不动。"""
    if role is None or body_lines is None:
        return
    messages.append({"role": role, "content": "\n".join(body_lines).strip()})

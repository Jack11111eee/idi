# -*- coding: utf-8 -*-
"""transcript.md 文法(DESIGN.md §6.1)单元测试:parse 与 append。

文法:每条消息 = 起始行 [user] 或 [ai](独占一行)+ 任意多行消息体,
以下一条起始行或文件末尾为界——多行消息体不需转义。
"""
from pathlib import Path

import pytest

from backend.transcript import (
    append_message,
    parse_transcript,
    transcript_exists,
)


def test_parse_basic_three_messages(tmp_path):
    # 用例 1(基础解析):三段消息 [user]/[ai]/[user],各含单行体
    path = tmp_path / "docs" / "transcript.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        "[user]\n想法一\n"
        "[ai]\n回应一\n"
        "[user]\n想法二\n",
        encoding="utf-8",
    )
    messages = parse_transcript(path)
    assert messages == [
        {"role": "user", "content": "想法一"},
        {"role": "ai", "content": "回应一"},
        {"role": "user", "content": "想法二"},
    ]


def test_parse_multiline_body_preserved(tmp_path):
    # 用例 2(多行体):3 段落含空行,首尾 strip,内部空行不动
    path = tmp_path / "docs" / "transcript.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        "[ai]\n第一段。\n\n第二段(空行在上)。\n\n\n第三段。\n\n"
        "[user]\n  收到  \n",
        encoding="utf-8",
    )
    messages = parse_transcript(path)
    assert len(messages) == 2
    assert messages[0]["role"] == "ai"
    assert messages[0]["content"] == "第一段。\n\n第二段(空行在上)。\n\n\n第三段。"
    assert messages[1] == {"role": "user", "content": "收到"}


def test_append_after_existing_messages(tmp_path):
    # 用例 3(追加):既有 2 条,append 一条 role=ai 多行文 → 前 2 条不变,末条精确
    path = tmp_path / "docs" / "transcript.md"
    path.parent.mkdir(parents=True)
    path.write_text("[user]\n想法一\n[ai]\n回应一\n", encoding="utf-8")
    before = parse_transcript(path)

    append_message(path, "ai", "第一段。\n\n第二段。")

    after = parse_transcript(path)
    assert len(after) == 3
    assert after[:2] == before
    assert after[2] == {"role": "ai", "content": "第一段。\n\n第二段。"}


def test_parse_missing_and_empty_file(tmp_path):
    # 用例 4(空文件):不存在的文件与空文件都返回 []
    assert parse_transcript(tmp_path / "nope.md") == []
    empty = tmp_path / "docs" / "transcript.md"
    empty.parent.mkdir(parents=True)
    empty.write_text("", encoding="utf-8")
    assert parse_transcript(empty) == []


def test_append_creates_file(tmp_path):
    # 用例 5(追加建文件):对不存在的 transcript.md append → 文件被创建且以起始行开头
    path = tmp_path / "docs" / "transcript.md"
    assert not transcript_exists(path)
    append_message(path, "user", "第一条消息")
    assert transcript_exists(path)
    assert path.read_text(encoding="utf-8").startswith("[user]\n")
    assert parse_transcript(path) == [{"role": "user", "content": "第一条消息"}]


def test_append_missing_trailing_newline(tmp_path):
    # 用例 6(无尾换行容错):既有文件末行无换行符,先补换行再追加
    path = tmp_path / "docs" / "transcript.md"
    path.parent.mkdir(parents=True)
    path.write_text("[user]\n上一条没有尾换行", encoding="utf-8")

    append_message(path, "ai", "新消息")

    messages = parse_transcript(path)
    assert messages == [
        {"role": "user", "content": "上一条没有尾换行"},
        {"role": "ai", "content": "新消息"},
    ]


# ---------- 文法边界(§6.1 反例/容错) ----------

def test_append_rejects_unknown_role(tmp_path):
    path = tmp_path / "docs" / "transcript.md"
    with pytest.raises(ValueError):
        append_message(path, "system", "hi")


def test_parse_starter_line_requires_full_line_match(tmp_path):
    # 起始行是整行精确匹配(strip 后)——行内提及 [user] 不是起始行
    path = tmp_path / "docs" / "transcript.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        "[user]\n我说「[ai] 不是起始行」\n[ai]\n收到,那是消息体的一部分\n",
        encoding="utf-8",
    )
    messages = parse_transcript(path)
    assert messages == [
        {"role": "user", "content": "我说「[ai] 不是起始行」"},
        {"role": "ai", "content": "收到,那是消息体的一部分"},
    ]


def test_parse_starter_line_with_surrounding_whitespace(tmp_path):
    # strip 后恰等 [user]/[ai] 的整行仍是起始行
    path = tmp_path / "docs" / "transcript.md"
    path.parent.mkdir(parents=True)
    path.write_text("  [user]  \n带空白的起始行\n", encoding="utf-8")
    messages = parse_transcript(path)
    assert messages == [{"role": "user", "content": "带空白的起始行"}]


def test_parse_dirty_head_discarded(tmp_path):
    # 起始行之前的非空内容(脏头,正常不出现)丢弃
    path = tmp_path / "docs" / "transcript.md"
    path.parent.mkdir(parents=True)
    path.write_text("脏头残留\n[user]\n正文\n", encoding="utf-8")
    assert parse_transcript(path) == [{"role": "user", "content": "正文"}]


def test_parse_only_starters_no_body(tmp_path):
    # 连续起始行:消息体为空字符串
    path = tmp_path / "docs" / "transcript.md"
    path.parent.mkdir(parents=True)
    path.write_text("[user]\n[ai]\n", encoding="utf-8")
    assert parse_transcript(path) == [
        {"role": "user", "content": ""},
        {"role": "ai", "content": ""},
    ]

"""AICaller 纯函数级测试(Task 2):权限矩阵回归、工厂切线、事件归一化。

不真实起 claude 进程——归一化逻辑拆成独立纯函数(normalize_stream_line /
normalize_sdk_message)后直接喂人造输入。
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.ai_caller import (  # noqa: E402
    SdkAICaller,
    SubprocessAICaller,
    make_permission_decision,
    normalize_sdk_message,
    normalize_stream_line,
)
from backend.config import make_ai_caller, read_config  # noqa: E402


# ---------------------------------------------------------------------------
# 1. make_permission_decision 权限矩阵代表断言(回归,全表 9 例见 PLAN Task 1)
# ---------------------------------------------------------------------------


def test_permission_design_md_reject():
    """写项目根 DESIGN.md → reject(受保护终稿)。"""
    p = Path("/tmp/fakeproj")
    assert make_permission_decision(p, "write", p / "DESIGN.md") == "reject"


def test_permission_authorization_md_reject():
    """写项目根 AUTHORIZATION.md → reject(AI 无任何批准路径,§5.4 / D-P3-4)。

    Specific Ideas 红线:AUTHORIZATION.md 的写入者是后端且仅后端——
    权限矩阵对 AI 拒绝无任何绕过通道(PLAN idi-03-02 Task 2 断言在位)。
    """
    p = Path("/tmp/fakeproj")
    assert make_permission_decision(p, "write", p / "AUTHORIZATION.md") == "reject"


def test_permission_tmp_allow():
    """写项目根 DESIGN.md.tmp → allow(tmp 是 DESIGN.md 唯一合法落盘路径)。"""
    p = Path("/tmp/fakeproj")
    assert make_permission_decision(p, "write", p / "DESIGN.md.tmp") == "allow"


def test_permission_docs_allow():
    """写项目内 docs/ → allow(G1 定稿通道)。"""
    p = Path("/tmp/fakeproj")
    assert make_permission_decision(p, "write", p / "docs" / "x.md") == "allow"


def test_permission_command_confirm():
    """任何执行 → confirm(矩阵末行)。"""
    p = Path("/tmp/fakeproj")
    assert make_permission_decision(p, "command", "git status") == "confirm"


# ---------------------------------------------------------------------------
# 2. make_ai_caller 按 config 切换实现路线
# ---------------------------------------------------------------------------


def test_make_ai_caller_subprocess():
    """ai_caller=subprocess → SubprocessAICaller。"""
    caller = make_ai_caller({"ai_caller": "subprocess"})
    assert isinstance(caller, SubprocessAICaller)


def test_make_ai_caller_sdk():
    """ai_caller=sdk → SdkAICaller。"""
    caller = make_ai_caller({"ai_caller": "sdk"})
    assert isinstance(caller, SdkAICaller)


# ---------------------------------------------------------------------------
# 3. 子进程路线事件归一化(纯函数,喂人造 stream-json 行)
# ---------------------------------------------------------------------------


def test_normalize_assistant_text_line_is_say():
    """assistant 消息的文本块 → kind=say。"""
    line = (
        '{"type":"assistant","message":{"role":"assistant",'
        '"content":[{"type":"text","text":"我先看看目录。"}]}}'
    )
    event = normalize_stream_line(line)
    assert event["kind"] == "say"
    assert event["content"] == "我先看看目录。"


def test_normalize_tool_use_read_line_is_read():
    """assistant 消息内 tool_use 的 Read → kind=read,目标路径进 content。"""
    line = (
        '{"type":"assistant","message":{"role":"assistant","content":['
        '{"type":"tool_use","name":"Read","input":{"file_path":"/tmp/x/notes.md"}}]}}'
    )
    event = normalize_stream_line(line)
    assert event["kind"] == "read"
    assert event["content"] == "/tmp/x/notes.md"


def test_normalize_tool_result_line_is_result():
    """user 消息内 tool_result → kind=result。"""
    line = (
        '{"type":"user","message":{"role":"user","content":['
        '{"type":"tool_result","content":"文件内容如下…"}]}}'
    )
    event = normalize_stream_line(line)
    assert event["kind"] == "result"


def test_normalize_garbage_line_is_error():
    """解析失败行 → kind=error,不抛异常。"""
    event = normalize_stream_line("not-a-json-line")
    assert event["kind"] == "error"


# ---------------------------------------------------------------------------
# 4. SDK 路线事件归一化(派生自 claude_agent_sdk 真实类型,同构验证)
# ---------------------------------------------------------------------------


def test_normalize_sdk_assistant_text_is_say():
    """SDK AssistantMessage 文本块 → say(与子进程路线同构)。"""
    from claude_agent_sdk.types import AssistantMessage, TextBlock

    msg = AssistantMessage(content=[TextBlock(text="好的,我来读取文件。")], model="test")
    events = normalize_sdk_message(msg)
    assert events[0]["kind"] == "say"
    assert events[0]["content"] == "好的,我来读取文件。"


def test_normalize_sdk_tool_use_read_is_read():
    """SDK AssistantMessage ToolUseBlock(Read)→ read。"""
    from claude_agent_sdk.types import AssistantMessage, ToolUseBlock

    msg = AssistantMessage(
        content=[
            ToolUseBlock(
                id="tu_1", name="Read", input={"file_path": "/tmp/x/notes.md"}
            )
        ],
        model="test",
    )
    events = normalize_sdk_message(msg)
    assert events[0]["kind"] == "read"
    assert events[0]["content"] == "/tmp/x/notes.md"


def test_normalize_sdk_result_is_done():
    """SDK ResultMessage → done(或 error)。"""
    from claude_agent_sdk.types import ResultMessage

    msg = ResultMessage(subtype="success", duration_ms=1, duration_api_ms=1,
                        is_error=False, num_turns=1, session_id="s")
    events = normalize_sdk_message(msg)
    assert events[0]["kind"] == "done"


def test_normalize_sdk_result_error_is_error():
    """SDK ResultMessage(is_error=True)→ error。"""
    from claude_agent_sdk.types import ResultMessage

    msg = ResultMessage(subtype="error_max_turns", duration_ms=1, duration_api_ms=1,
                        is_error=True, num_turns=1, session_id="s", result="超限")
    events = normalize_sdk_message(msg)
    assert events[0]["kind"] == "error"


# ---------------------------------------------------------------------------
# 5. read_config 回落语义(工厂切线的地基)
# ---------------------------------------------------------------------------


def test_read_config_returns_valid_dict():
    """当前 config.json 有效时返回 dict 且 ai_caller 合法。"""
    cfg = read_config()
    assert cfg["ai_caller"] in ("sdk", "subprocess")


def test_make_ai_caller_reject_unknown_route():
    """未知路线 → ValueError(工厂不静默)。"""
    with pytest.raises(ValueError):
        make_ai_caller({"ai_caller": "nonsense"})

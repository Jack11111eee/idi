"""AICaller:AI 调用抽象接口 + 权限路由层(DESIGN.md §5.3/§5.4)。

双轨契约(D-P1-5/D-06):SDK 路线( Task 2 接入)与子进程路线实现同一接口,
事件归一化到统一 kind 枚举,前端与上层零改动切换。

统一事件字典(字段命名前端可见,本阶段内自洽):
  {
    "kind": "say" | "read" | "write" | "command" | "result" | "error" | "done",
    "content": str,               # 人类可读正文(事件内容摘要)
    "raw": object,                # 原始 JSON(SDK 消息对象或 CLI stream-json 行)
  }
"""

import json
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator

# ---------------------------------------------------------------------------
# 权限路由层(§5.4 矩阵,自上而下首条命中)——纯函数,Task 1 即完备
# ---------------------------------------------------------------------------

_READ = "read"
_WRITE = "write"


def make_permission_decision(project_path, action: str, target_path) -> str:
    """权限门核心(§5.4):返回 "allow" / "reject" / "confirm" 三态。

    规则序(首条命中即返回):
      1. 写且目标是项目根 DESIGN.md 或 AUTHORIZATION.md → reject
      2. 写且目标是项目根 DESIGN.md.tmp → allow
      3. 写且目标在项目内 docs/ 目录下 → allow
      4. 读且目标在项目内 → allow
      5. 其余(写项目内其他位置 / 读写项目外 / 任何执行)→ confirm

    action: "read" | "write" | "command"(command 时 target_path 为命令文本)
    """
    project = Path(project_path).resolve()

    # 矩阵末行:任何执行都需要确认,先于路径判断
    if action == "command":
        return "confirm"

    target_abs = Path(target_path)
    try:
        target_abs = target_abs.resolve()
    except (OSError, RuntimeError):  # 路径不可解析时按字面量对待
        pass
    in_project = target_abs == project or project in target_abs.parents

    if action == _WRITE:
        # 规则 1:项目根受保护文件直写 → 拒绝
        if target_abs.parent == project and target_abs.name in (
            "DESIGN.md",
            "AUTHORIZATION.md",
        ):
            return "reject"
        # 规则 2:项目根 DESIGN.md.tmp 是 DESIGN.md 明确允许的暂存名
        if target_abs.parent == project and target_abs.name == "DESIGN.md.tmp":
            return "allow"
        # 规则 3:项目内 docs/ 目录下的写放行(G1 定稿通道)
        if in_project and target_abs != project:
            try:
                rel = target_abs.relative_to(project)
                if rel.parts[:-1] and rel.parts[0] == "docs":
                    return "allow"
            except ValueError:
                pass
        # 规则 5a:写项目内其他位置
        if in_project:
            return "confirm"
        # 规则 5b:写项目外
        return "confirm"

    if action == _READ:
        # 规则 4:读项目内放行
        if in_project:
            return "allow"
        # 规则 5c:读项目外
        return "confirm"

    # 未知动作按最保守处理
    return "confirm"


def build_system_prompt() -> str:
    """SubprocessAICaller 交给 claude CLI 的 system prompt 段落。

    内容:权限约定要点 + §3.8 语言红线原文要义(简洁精准、术语先大白话定义)。
    硬执行拦截在后续任务扩展;本段先供 AI 遵守。
    """
    return (
        "你是本工具的 AI 讨论引擎。写作与回答遵守以下约定:\n"
        "1. 语言红线:简洁精准;每个术语先用大白话定义一次再使用;\n"
        "   不堆砌空话,面向单人开发者读者,讨论文档以中文为主。\n"
        "2. 文件权限约定:项目根 DESIGN.md 与 AUTHORIZATION.md 为只读终稿,"
        "不得直接改写;草稿请写入 DESIGN.md.tmp;\n"
        "   定稿产物写入 docs/ 目录下;读取项目内文件自由进行;\n"
        "   其他任何写入或命令执行前需要用户确认。\n"
    )


# ---------------------------------------------------------------------------
# CLI stream-json 单行 → 统一事件 的归一化(独立纯函数,便于单测)
# ---------------------------------------------------------------------------

# tool_use 名称 → 统一 kind 映射
_TOOL_KIND = {
    "Read": "read",
    "Write": "write",
    "Edit": "write",
    "Bash": "command",
}


def normalize_stream_line(line: str) -> dict | None:
    """把 claude CLI stream-json 的一行 JSON 解析为统一事件字典。

    - assistant 消息里的 message 文本 → kind=say
    - tool_use 的 Read/Write/Edit/Bash → 对应 kind,目标路径进 content
    - tool_result → kind=result
    - 其余已知类型(system 等)→ None(不产出事件,由调用方跳过)
    - 解析失败 → kind=error 的单条事件

    返回 None 表示该行无需产出事件。
    """
    text = line.strip()
    if not text:
        return None
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as exc:
        return {"kind": "error", "content": f"stream 行解析失败:{exc}", "raw": text}

    msg_type = obj.get("type")
    if msg_type == "assistant":
        message = obj.get("message") or {}
        blocks = message.get("content") or []
        events = None
        for block in blocks:
            if not isinstance(block, dict):
                continue
            block_type = block.get("type")
            if block_type == "text":
                events = {"kind": "say", "content": block.get("text", ""), "raw": obj}
            elif block_type == "tool_use":
                kind = _TOOL_KIND.get(block.get("name", ""), "command")
                tool_input = block.get("input") or {}
                target = (
                    tool_input.get("file_path")
                    or tool_input.get("notebook_path")
                    or tool_input.get("path")
                    or tool_input.get("command")
                    or tool_input.get("pattern")
                    or ""
                )
                events = {"kind": kind, "content": str(target), "raw": obj}
        return events  # 一行只上报一个代表事件(首个文本或首个工具)
    if msg_type == "user":
        # stream-json 的 tool_result 走 user 消息
        message = obj.get("message") or {}
        blocks = message.get("content") or []
        for block in blocks:
            if isinstance(block, dict) and block.get("type") == "tool_result":
                content = block.get("content")
                if isinstance(content, list):  # [{type:text,...}] 形态
                    content = " ".join(
                        b.get("text", "") for b in content if isinstance(b, dict)
                    )
                return {"kind": "result", "content": str(content or ""), "raw": obj}
        return None
    return None


# ---------------------------------------------------------------------------
# AICaller 抽象接口(D-P1-5/D-P1-6)
# ---------------------------------------------------------------------------


class AICaller(ABC):
    """AI 调用统一接口:两条实现路线(SDK / 子进程)的共同契约。"""

    @abstractmethod
    def run(self, project_path, prompt: str) -> Iterator[dict]:
        """在 project_path 目录上执行一次无头调用,逐条产出统一事件。"""

    def ask_lite(self, document_text: str, quoted_text: str, question: str) -> dict:
        """大白话轻量调用(§3.4,Phase 2 的 UI-02 实现)。

        只定义签名不实现逻辑(D-P1-6)——避免 Phase 2 改接口。
        """
        raise NotImplementedError("ask_lite 将在 Phase 2 实现(D-P1-6 接口预定义)")

    @abstractmethod
    def abort(self) -> None:
        """杀死当前调用(§5.5,D-P1-8:不留损坏状态,孤儿半成品由重跑覆盖)。"""


class SubprocessAICaller(AICaller):
    """子进程兜底路线:claude -p --output-format stream-json(§5.3)。"""

    def __init__(self):
        self._process: subprocess.Popen | None = None

    def run(self, project_path, prompt: str) -> Iterator[dict]:
        """起 claude CLI 子进程(stream-json),逐行归一化后 yield。

        工作目录 = project_path;system prompt 段落声明权限约定与语言红线。
        进程退出后按 returncode 产 done 或 error;stderr 逐行归 kind=error。
        """
        argv = [
            "claude",
            "-p",
            prompt,
            "--output-format",
            "stream-json",
            "--verbose",
            "--append-system-prompt",
            build_system_prompt(),
        ]
        self._process = subprocess.Popen(
            argv,
            cwd=str(project_path),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        proc = self._process
        # 逐行读 stdout;stderr 在退出后统一读(避免双流竞态)
        assert proc.stdout is not None
        for line in proc.stdout:
            event = normalize_stream_line(line)
            if event is not None:
                yield event
        proc.wait()
        stderr_text = proc.stderr.read() if proc.stderr else ""
        for err_line in [ln for ln in stderr_text.splitlines() if ln.strip()]:
            yield {"kind": "error", "content": err_line, "raw": {"stderr": True}}
        if proc.returncode == 0:
            yield {
                "kind": "done",
                "content": "调用结束",
                "raw": {"returncode": proc.returncode},
            }
        else:
            yield {
                "kind": "error",
                "content": f"claude CLI 退出码 {proc.returncode}",
                "raw": {"returncode": proc.returncode},
            }
        self._process = None

    def abort(self) -> bool:
        """终止当前子进程:先 terminate 再 kill(两段, §5.5)。"""
        proc = self._process
        if proc is None:
            return False
        try:
            proc.terminate()  # SIGTERM
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()  # SIGKILL
        except ProcessLookupError:
            pass  # 进程已先于我们退出
        self._process = None
        return True

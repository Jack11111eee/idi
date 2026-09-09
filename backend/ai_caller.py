"""AICaller:AI 调用抽象接口 + 权限路由层(DESIGN.md §5.3/§5.4)。

双轨契约(D-P1-5/D-06):SDK 路线与子进程路线实现同一接口,
事件归一化到统一 kind 枚举,前端与上层零改动切换。

统一事件字典(字段命名前端可见,本阶段内自洽):
  {
    "kind": "say" | "read" | "write" | "command" | "result" | "error" | "done",
    "content": str,               # 人类可读正文(事件内容摘要)
    "raw": object,                # 原始 JSON(SDK 消息对象或 CLI stream-json 行)
  }

权限确认回环(AI-04,依赖倒置):
  confirm 处置不降级为拒绝——经 set_request_permission(fn) 注入的回调征求用户:
    fn(tool_name, tool_input) -> bool  (True=放行,False=驳回)
  回调由上层(session)注入;ai_caller 不 import session。
"""

import asyncio
import json
import subprocess
import threading
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

    def __init__(self):
        # confirm 处置的用户征求回调(AI-04 依赖倒置:上层注入,不 import session)。
        # 为 None 时按 False 处理(最保守,不悄悄放行)。
        self._request_permission = None

    def set_request_permission(self, fn) -> None:
        """注入权限确认回调:fn(tool_name, tool_input) -> bool。

        confirm 处置的工具调用将通过它征求用户决定;True 放行 / False 驳回。
        """
        self._request_permission = fn

    def _ask_user_permission(self, tool_name: str, tool_input: dict) -> bool:
        """执行注入的权限回调;未注入时按 False(保守)。"""
        fn = self._request_permission
        if fn is None:
            return False
        return bool(fn(tool_name, tool_input))

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
    """子进程兜底路线:claude -p 双向 stream-json + 权限控制协议(§5.3)。

    CLI 按双向 stream-json 跑(与 SDK 同一进程协议):
      - stdin 送 {"type":"user"} 行后保持打开,应答 CLI 发来的 control_request
      - stdout 逐行读事件;control_request(can_use_tool)→ §5.4 判定:
          allow → control_response allow
          reject → control_response deny
          confirm → 注入的 request_permission 回调回环(阻塞等用户),按结果答
      - setting-sources 置空:用户全局 ~/.claude/settings.json 的 allow 规则
        (如 Write(*))会在权限回调前自动放行、绕过权限门,必须屏蔽
        (SDK 路线同因 setting_sources=[])。
    """

    def __init__(self, cli_path: str = "claude"):
        super().__init__()
        self._cli_path = cli_path
        self._process: subprocess.Popen | None = None
        self._reader_thread: threading.Thread | None = None

    def _classify_tool_action(self, tool_name: str, tool_input: dict):
        """工具名 + 参数 → §5.4 矩阵的 (action, target)。"""
        if tool_name in ("Bash",):
            return "command", tool_input.get("command", "")
        if tool_name in ("Write", "Edit", "NotebookEdit"):
            return "write", tool_input.get("file_path") or tool_input.get("notebook_path") or ""
        return "read", tool_input.get("file_path") or tool_input.get("path") or ""

    def _handle_control_request(self, obj: dict, project: Path, q) -> None:
        """应答 CLI 的 can_use_tool 控制请求(§5.4 矩阵 + 用户回环)。"""
        req = obj.get("request", {})
        if req.get("subtype") != "can_use_tool":
            return  # 其余控制请求(如 initialize)不在此处理
        request_id = obj.get("request_id")
        tool_name = req.get("tool_name", "")
        tool_input = req.get("input", {})
        action, target = self._classify_tool_action(tool_name, tool_input)
        decision = make_permission_decision(project, action, target)
        if decision == "allow":
            behavior = {"behavior": "allow", "updatedInput": tool_input}
        elif decision == "reject":
            behavior = {"behavior": "deny", "message": f"权限拒绝:目标 {target}"}
        else:  # confirm → 用户回环(AI-04;无降级)
            approved = self._ask_user_permission(tool_name, tool_input)
            behavior = (
                {"behavior": "allow", "updatedInput": tool_input}
                if approved
                else {"behavior": "deny", "message": f"用户驳回:{action} {target}"}
            )
            q.put(
                {
                    "kind": "command" if action == "command" else action,
                    "content": f"权限确认({action} {target}):{'同意' if approved else '驳回'}",
                    "raw": None,
                }
            )
        response = {
            "type": "control_response",
            "response": {
                "subtype": "success",
                "request_id": request_id,
                "response": behavior,
            },
        }
        proc = self._process
        try:
            if proc is not None and proc.stdin is not None:
                proc.stdin.write(json.dumps(response) + "\n")
                proc.stdin.flush()
        except (OSError, ValueError):  # 进程已收流/关闭
            pass

    def run(self, project_path, prompt: str) -> Iterator[dict]:
        """起 claude CLI 子进程(双向 stream-json),逐行归一化后 yield。

        工作目录 = project_path;system prompt 段落声明权限约定与语言红线。
        进程退出后按 returncode 产 done 或 error;stderr 逐行归 kind=error。
        """
        project = Path(project_path)
        argv = [
            self._cli_path,
            "-p",
            "--input-format", "stream-json",
            "--output-format", "stream-json",
            "--verbose",
            "--permission-prompt-tool", "stdio",
            "--setting-sources=",
            "--append-system-prompt",
            build_system_prompt(),
        ]
        self._process = subprocess.Popen(
            argv,
            cwd=str(project_path),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        proc = self._process

        # 送用户消息(双向 stream-json 输入格式)
        user_msg = {"type": "user", "message": {"role": "user", "content": prompt}}
        try:
            assert proc.stdin is not None
            proc.stdin.write(json.dumps(user_msg) + "\n")
            proc.stdin.flush()
        except (OSError, ValueError) as exc:
            yield {"kind": "error", "content": f"发送消息失败:{exc}", "raw": None}
            self._process = None
            return

        import queue as _queue

        out_q: _queue.Queue = _queue.Queue()

        def _read_stdout():
            """读 stdout:事件行入队;控制请求即时应答。"""
            assert proc.stdout is not None
            for line in proc.stdout:
                text = line.strip()
                if not text:
                    continue
                try:
                    obj = json.loads(text)
                except json.JSONDecodeError:
                    out_q.put({"kind": "error", "content": f"行解析失败:{text[:120]}", "raw": None})
                    continue
                if obj.get("type") == "control_request":
                    self._handle_control_request(obj, project, out_q)
                    continue
                event = normalize_stream_line(text)
                if event is not None:
                    out_q.put(event)

        self._reader_thread = threading.Thread(target=_read_stdout, daemon=True)
        self._reader_thread.start()

        FIN = object()
        watcher_killed = threading.Event()

        def _stderr_reader():
            """stderr 收集(退出后统一入队,避免双流竞态)。"""
            assert proc.stderr is not None
            text = proc.stderr.read()
            for err_line in [ln for ln in text.splitlines() if ln.strip()]:
                out_q.put({"kind": "error", "content": err_line, "raw": {"stderr": True}})

        stderr_thread = threading.Thread(target=_stderr_reader, daemon=True)
        stderr_thread.start()
        # stderr 线程会阻塞到 EOF;主 yield 循环从队列取,done 判据看 result 行。

        def _wait_exit():
            proc.wait()
            out_q.put(FIN)

        exit_thread = threading.Thread(target=_wait_exit, daemon=True)
        exit_thread.start()

        try:
            while True:
                item = out_q.get(timeout=600)
                if item is FIN:
                    break
                yield item
                if item.get("kind") == "done":
                    break
        except _queue.Empty:
            yield {"kind": "error", "content": "调用超时(600s 无事件)", "raw": None}
        finally:
            # 收流:杀进程 & 关 stdin(队列后续条目随之 EOF)
            self._process = None
            try:
                proc.terminate()
            except ProcessLookupError:
                pass

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


# ---------------------------------------------------------------------------
# SdkAICaller:Claude Agent SDK 路线(Task 2,§5.3 首选路线)
# ---------------------------------------------------------------------------

# SDK 消息里的 tool name → 统一 kind(与子进程路线共表)
_SDK_TOOL_KIND = _TOOL_KIND


def normalize_sdk_message(message) -> list[dict]:
    """把 SDK 消息对象归一化为统一事件字典列表(独立纯函数,便于单测)。

    - AssistantMessage:文本块 → say;ToolUseBlock → 按 _SDK_TOOL_KIND
      (一条消息可同时含文本与工具块,逐块产出,不丢事件)
    - ResultMessage → kind=done(或 error,当 is_error)
    - 其余(SystemMessage 等)→ 空列表
    """
    from claude_agent_sdk.types import AssistantMessage, ResultMessage

    if isinstance(message, AssistantMessage):
        events = []
        for block in message.content:
            block_type = type(block).__name__
            if block_type == "TextBlock" and block.text.strip():
                events.append(
                    {"kind": "say", "content": block.text, "raw": _raw_of(message)}
                )
            elif block_type == "ToolUseBlock":
                kind = _SDK_TOOL_KIND.get(block.name, "command")
                tool_input = block.input or {}
                target = (
                    tool_input.get("file_path")
                    or tool_input.get("notebook_path")
                    or tool_input.get("path")
                    or tool_input.get("command")
                    or tool_input.get("pattern")
                    or ""
                )
                events.append(
                    {"kind": kind, "content": str(target), "raw": _raw_of(message)}
                )
        return events
    if isinstance(message, ResultMessage):
        kind = "error" if message.is_error else "done"
        content = message.result or ("调用结束" if kind == "done" else "调用出错")
        return [{"kind": kind, "content": content, "raw": _raw_of(message)}]
    return []


def _raw_of(message) -> dict:
    """把 dataclass 消息转成可 JSON 序列化的 dict(raw 字段用)。"""
    import dataclasses

    if dataclasses.is_dataclass(message) and not isinstance(message, type):
        try:
            return dataclasses.asdict(message)
        except Exception:  # 不可序列化字段(枚举等)兜底
            return {"type": type(message).__name__}
    return {"type": type(message).__name__}


class SdkAICaller(AICaller):
    """SDK 首选路线:claude-agent-sdk 的 query() 查询式调用。

    事件枚举与 SubprocessAICaller 完全同构(§5.3 双轨契约);
    can_use_tool 回调接入 make_permission_decision:
    allow 放行 / reject 拒绝 / confirm 经注入的 request_permission 回调
    征求用户(AI-04 完整闭环;回调未注入时保守驳回,不降级为静默放行)。
    setting_sources=[]:屏蔽用户全局 settings.json 的 allow 规则——它们会在
    can_use_tool 之前自动放行工具调用、绕过权限门(与子进程路线同因)。
    """

    def __init__(self, cli_path: str | None = None, model: str | None = None):
        super().__init__()
        self._cli_path = cli_path
        self._model = model
        self._abort_flag = threading.Event()
        self._interrupt_event: asyncio.Event | None = None

    def _build_options(self, project_path):
        from claude_agent_sdk import ClaudeAgentOptions

        project = Path(project_path)

        async def _can_use_tool(
            tool_name: str, tool_input: dict, context
        ):
            # 动作分类:写类工具 → write,其余(read/查)→ read,Bash → command
            if tool_name == "Bash":
                action, target = "command", tool_input.get("command", "")
            elif tool_name in ("Write", "Edit"):
                action, target = "write", tool_input.get("file_path", "")
            else:
                action, target = "read", tool_input.get("file_path") or tool_input.get(
                    "path", ""
                )
            decision = make_permission_decision(project, action, target)
            from claude_agent_sdk.types import (
                PermissionResultAllow,
                PermissionResultDeny,
            )

            if decision == "allow":
                return PermissionResultAllow()
            if decision == "reject":
                return PermissionResultDeny(message=f"权限拒绝:目标 {target}")
            # confirm(AI-04):注入的回调回环征求用户(阻塞至用户决定);
            # 回调未注入时保守驳回——不悄悄放行。
            approved = self._ask_user_permission(tool_name, tool_input)
            if approved:
                return PermissionResultAllow()
            return PermissionResultDeny(
                message=f"用户驳回:{action} {target}"
            )

        options = ClaudeAgentOptions(
            cwd=str(project),
            system_prompt=build_system_prompt(),
            can_use_tool=_can_use_tool,
            setting_sources=[],
        )
        if self._cli_path:
            options.cli_path = self._cli_path
        if self._model:
            options.model = self._model
        return options

    async def _run_async(self, project_path, prompt: str):
        from claude_agent_sdk import ClaudeSDKClient
        from claude_agent_sdk.types import ResultMessage

        self._abort_flag.clear()
        self._interrupt_event = asyncio.Event()

        async def _watch_abort():
            # 在工作线程里等 threading.Event,置 asyncio Event 以中断迭代
            while not self._abort_flag.is_set():
                await asyncio.sleep(0.2)
            self._interrupt_event.set()

        options = self._build_options(project_path)
        client = ClaudeSDKClient(options=options)
        await client.connect()
        watcher = asyncio.create_task(_watch_abort())
        try:
            await client.query(prompt)
            async for message in client.receive_messages():
                if self._abort_flag.is_set():
                    break  # 中止:提前收流
                for event in normalize_sdk_message(message):
                    yield event
                if isinstance(message, ResultMessage):
                    return
        finally:
            watcher.cancel()
            try:
                await client.disconnect()
            except Exception:
                pass  # 中止路径下的断开异常不致命
            self._interrupt_event = None

    def run(self, project_path, prompt: str) -> Iterator[dict]:
        """驱动单个 asyncio 循环耗尽 _run_async,同步生成器逐条产出统一事件。

        注意:async 生成器必须绑定在同一个事件循环里迭代
        (asyncio.run 每次新建循环会导致 aclose 异常与事件丢失),
        因此把整个耗尽过程放进一个 loop,用队列把事件递给调用方。
        """
        import queue as _queue

        out_q: _queue.Queue = _queue.Queue()
        FIN = object()  # 流结束哨兵

        def _worker():
            async def _consume():
                agen = self._run_async(project_path, prompt)
                try:
                    async for event in agen:
                        out_q.put(event)
                finally:
                    out_q.put(FIN)

            try:
                asyncio.run(_consume())
            except Exception as exc:
                out_q.put({"kind": "error", "content": f"SDK 调用异常:{exc}", "raw": None})
                out_q.put(FIN)

        thread = threading.Thread(target=_worker, daemon=True)
        thread.start()
        saw_done = False
        while True:
            item = out_q.get()
            if item is FIN:
                break
            if item["kind"] in ("done", "error"):
                saw_done = True  # 流自带收尾事件(ResultMessage 异常转 error)
            yield item
        thread.join(timeout=5)
        if self._abort_flag.is_set():
            yield {"kind": "done", "content": "已中止", "raw": {"aborted": True}}
        elif not saw_done:
            # ResultMessage 未出现时(异常早退)补一条 done 收尾流
            yield {"kind": "done", "content": "调用结束", "raw": None}

    def abort(self) -> bool:
        """设置中止标志:迭代器侧提前 break;尽力断开底层 CLI 子进程。"""
        self._abort_flag.set()
        ev = self._interrupt_event
        if ev is not None:
            try:
                ev.set()
            except RuntimeError:  # 循环已关
                pass
        return True

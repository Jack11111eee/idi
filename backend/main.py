"""FastAPI 应用:会话路由 + 健康检查、SSE 事件流、中止、开发探针。

路由(Plan idi-01-03):
  GET  /api/health      健康检查
  GET  /api/events      SSE 流(text/event-stream)
  POST /api/abort       杀当前调用(§5.5)
  POST /api/dev/ping    开发探针(Plan 01 自证通道,保留)
  POST /api/enter       进入项目目录(FLOW-01):derive_state + transcript + draft
  POST /api/message     发消息(异步起,立即 202;在飞时 409)
  POST /api/permission  回答挂起权限确认(未知 id 404)
  GET  /api/draft       当前 draft.md 内容(前端流后拉新)
  GET  /api/session     当前会话只读快照(前端流后拉新门控;与 /api/enter 同构)
  GET  /api/transcript  全量消息列表(备用拉)
静态:frontend/ 目录挂在根路径。
"""

import threading

from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend import config as cfg
from backend import session
from backend.ai_caller import AICaller
from backend.cli_check import check_claude_cli
from backend.events import broker

app = FastAPI(title="interactive-discuss-iteration")

# ---------------------------------------------------------------------------
# 当前调用句柄(单机单用户,全局唯一调用,D-P1-8 中止语义)
# ---------------------------------------------------------------------------
_caller_lock = threading.Lock()
_current_caller: AICaller | None = None


def _ping_worker(project_path: str, prompt: str) -> None:
    """后台线程:跑一次 AICaller.run,把事件逐条 publish 到 broker。"""
    global _current_caller
    caller = cfg.make_ai_caller(cfg.read_config())
    with _caller_lock:
        _current_caller = caller
    try:
        for event in caller.run(project_path, prompt):
            broker.publish(event)
    except Exception as exc:  # 线程内兜底:任何异常转 error 事件,流不悬空
        broker.publish({"kind": "error", "content": f"调用线程异常:{exc}", "raw": None})
    finally:
        with _caller_lock:
            _current_caller = None
        broker.publish({"kind": "done", "content": "调用线程结束", "raw": None})


class PingBody(BaseModel):
    project_path: str
    prompt: str = "读取本目录下任意一个文件并向我说明它的内容"


class ConfigBody(BaseModel):
    ai_caller: str  # "sdk" | "subprocess"


class EnterBody(BaseModel):
    path: str


class MessageBody(BaseModel):
    text: str


class PermissionBody(BaseModel):
    id: str
    approved: bool


# ---------------------------------------------------------------------------
# 会话路由(FLOW-01 / FLOW-02 / AI-04)
# ---------------------------------------------------------------------------


@app.post("/api/enter")
def enter_project(body: EnterBody) -> JSONResponse:
    """进入项目:derive_state + transcript 历史 + draft/brainstorm 内容。"""
    try:
        snapshot = session.enter_project(body.path)
    except FileNotFoundError as exc:
        return JSONResponse(
            {"status": "error", "message": str(exc)}, status_code=400
        )
    return JSONResponse({"status": "ok", **snapshot})


@app.post("/api/message")
def send_message(body: MessageBody) -> JSONResponse:
    """发消息:全流水线后台跑;在飞调用中 → 409(T-idi03-04)。"""
    if session.busy():
        return JSONResponse(
            {"status": "error", "message": "当前有调用进行中,请等它结束或先中止"},
            status_code=409,
        )
    try:
        accepted = session.send_message(body.text)
    except RuntimeError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=400)
    if not accepted:
        return JSONResponse(
            {"status": "error", "message": "当前有调用进行中"}, status_code=409
        )
    return JSONResponse({"status": "accepted"}, status_code=202)


@app.post("/api/permission")
def resolve_permission(body: PermissionBody) -> JSONResponse:
    """回答挂起的权限确认;id 必须来自后端生成的挂起队列(未知一律 404)。"""
    decision = session.resolve_permission(body.id, body.approved)
    if decision is None:
        return JSONResponse(
            {"status": "error", "message": "未知或已处理的权限请求"}, status_code=404
        )
    return JSONResponse({"status": "ok", "approved": decision})


@app.get("/api/draft")
def get_draft() -> JSONResponse:
    """当前 draft.md 内容(供前端在会话流收尾后拉新);未进入项目 → null。"""
    try:
        snapshot = session.snapshot()
    except RuntimeError:
        return JSONResponse({"status": "ok", "draft": None})
    return JSONResponse({"status": "ok", "draft": snapshot["draft"]})


@app.get("/api/session")
def get_session() -> JSONResponse:
    """当前会话只读快照:与 POST /api/enter 同构(state/transcript/draft/门控)。

    供前端在会话流收尾(done)后拉新门控(g1_available / divergence_available /
    状态徽标)——不重进目录,会话流不必整页重渲染;已进入项目是前提(400)。
    """
    try:
        snapshot = session.snapshot()
    except RuntimeError as exc:
        return JSONResponse(
            {"status": "error", "message": str(exc)}, status_code=400
        )
    return JSONResponse({"status": "ok", **snapshot})


@app.post("/api/divergence")
def trigger_divergence() -> JSONResponse:
    """触发发散模式(FLOW-06):同一 AI 调用链,产物 brainstorm.md 由 AI 落盘。

    入口关闭(雏形已存在/已定稿,防绕过)→ 409;在飞调用 → 409(锁语义同发消息)。
    """
    try:
        accepted = session.trigger_divergence()
    except RuntimeError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=400)
    if not accepted:
        return JSONResponse(
            {
                "status": "error",
                "message": "发散入口已关闭(雏形已存在或已定稿)或当前有调用进行中",
            },
            status_code=409,
        )
    return JSONResponse({"status": "accepted"}, status_code=202)


@app.get("/api/brainstorm")
def get_brainstorm() -> JSONResponse:
    """当前 brainstorm.md 内容(前端渲染发散候选);未进入项目 → null。"""
    try:
        snapshot = session.snapshot()
    except RuntimeError:
        return JSONResponse({"status": "ok", "brainstorm": None})
    return JSONResponse({"status": "ok", "brainstorm": snapshot["brainstorm"]})


@app.post("/api/g1")
def finalize_g1() -> JSONResponse:
    """G1 认可雏形(FLOW-03 / §4.4):后端定稿 draft.md → docs/discuss-round-1.md。

    交互形态 = 前置决策门 direct-through(DESIGN.md §4.4 字面:点击即 G1 通过,零确认)。
    失败语义:无 draft.md → 400;已定稿(discuss-round-1.md 已存在)→ 409 幂等防护;
    AI 调用在飞 → 409。成功 → 新 derive_state 结果(前端据此切轮次视图)。
    """
    try:
        result = session.finalize_g1()
    except RuntimeError as exc:
        message = str(exc)
        if "在飞" in message or "进行中" in message:
            return JSONResponse(
                {"status": "error", "message": message}, status_code=409
            )
        return JSONResponse({"status": "error", "message": message}, status_code=400)
    except FileNotFoundError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=400)
    except FileExistsError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=409)
    return JSONResponse({"status": "ok", **result})


@app.get("/api/transcript")
def get_transcript() -> JSONResponse:
    """全量消息列表(备用拉;重启恢复也走 /api/enter 的同一组装)。"""
    try:
        snapshot = session.snapshot()
    except RuntimeError:
        return JSONResponse({"status": "ok", "transcript": []})
    return JSONResponse({"status": "ok", "transcript": snapshot["transcript"]})


# ---------------------------------------------------------------------------
# Plan 01 骨架路由(保留)
# ---------------------------------------------------------------------------


@app.post("/api/config")
def set_config(body: ConfigBody) -> JSONResponse:
    """运行时换线:写回 config.json 的 ai_caller 键(Task 3)。

    不重进程——下一次 /api/dev/ping 读最新配置重建 caller。
    """
    if body.ai_caller not in ("sdk", "subprocess"):
        return JSONResponse(
            {"status": "error", "message": f"非法 ai_caller:{body.ai_caller}"},
            status_code=400,
        )
    merged = cfg.write_config({"ai_caller": body.ai_caller})
    return JSONResponse({"status": "ok", "config": merged})


@app.get("/api/config")
def get_config() -> JSONResponse:
    return JSONResponse({"status": "ok", "config": cfg.read_config()})


@app.post("/api/dev/ping")
def dev_ping(body: PingBody) -> JSONResponse:
    """开发探针:在后台线程起一次真实调用,事件走 SSE 直播。"""
    threading.Thread(
        target=_ping_worker,
        args=(body.project_path, body.prompt),
        daemon=True,
    ).start()
    return JSONResponse({"status": "started"})


@app.post("/api/abort")
def abort() -> JSONResponse:
    """中止当前调用:杀进程,不留损坏状态(孤儿半成品由重跑覆盖)。

    两条在飞路径都要杀(D-P1-8 中止语义;Phase 1 验证 gap 修复):
      ① 会话流水线(send_message / trigger_divergence)—— session.abort():
        杀 caller + 强制释放挂起权限 + 解 busy 锁
      ② dev/ping 探针线程 —— main._current_caller.abort()
    killed 为真值:任一路径真的杀了在飞调用才为 true;两边都空闲时 false。
    """
    killed = False
    if session.busy():
        result = session.abort()
        killed = bool(result.get("killed"))
    with _caller_lock:
        caller = _current_caller
    if caller is not None and caller.abort():
        killed = True
    return JSONResponse({"status": "aborted", "killed": killed})


@app.get("/api/health")
def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})


@app.get("/api/cli-check")
def cli_check() -> JSONResponse:
    """claude CLI 自检(§7.1)。

    「只挡第一次」语义在前端:后端不缓存失败、不拒绝后续请求,
    用户点「重新检测」即再调本端点。
    """
    return JSONResponse(check_claude_cli())


@app.get("/api/events")
async def events() -> StreamingResponse:
    """SSE 流:订阅 broker,把事件按 SSE data 行逐条 yield(单向推送)。

    注意:queue.get 必须放线程池——直接在事件循环里阻塞 get 会把
    整个 loop 冻住(T-idi01-04,健康检查也会无响应)。
    """
    import asyncio

    q = broker.register()

    async def stream():
        try:
            while True:
                try:
                    # 阻塞 get 放 executor(超时 = 心跳窗口)
                    payload = await asyncio.to_thread(q.get, True, 15)
                    yield f"data: {payload}\n\n"
                except Exception:
                    # 队列空超时:发 SSE 注释行作心跳,保连接
                    yield ": keep-alive\n\n"
        finally:
            broker.unregister(q)

    return StreamingResponse(stream(), media_type="text/event-stream")


# 静态前端挂载(同源,无需 CORS;D-P1-2)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

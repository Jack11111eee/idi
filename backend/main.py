"""FastAPI 应用:健康检查、SSE 事件流、中止、开发探针(D-P1-1/D-P1-7)。

路由(本任务):
  GET  /api/health    健康检查
  GET  /api/events    SSE 流(text/event-stream)
  POST /api/abort     杀当前调用(§5.5)
  POST /api/dev/ping  开发探针:起一次真实 AI 调用并直播事件(Task 1 版)
静态:frontend/ 目录挂在根路径。
"""

import threading

from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend import config as cfg
from backend.ai_caller import AICaller
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
    """中止当前调用:杀进程,不留损坏状态(孤儿半成品由重跑覆盖)。"""
    with _caller_lock:
        caller = _current_caller
    killed = caller.abort() if caller is not None else False
    return JSONResponse({"status": "aborted", "killed": killed})


@app.get("/api/health")
def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})


@app.get("/api/events")
async def events() -> StreamingResponse:
    """SSE 流:订阅 broker,把事件按 SSE data 行逐条 yield(单向推送)。"""
    q = broker.register()

    async def stream():
        try:
            while True:
                try:
                    payload = q.get(timeout=15)  # 心跳窗口
                    yield f"data: {payload}\n\n"
                except Exception:
                    # 队列空超时:发 SSE 注释行作心跳,保连接(T-idi01-04)
                    yield ": keep-alive\n\n"
        finally:
            broker.unregister(q)

    return StreamingResponse(stream(), media_type="text/event-stream")


# 静态前端挂载(同源,无需 CORS;D-P1-2)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

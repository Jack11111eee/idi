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


class AnnotationBody(BaseModel):
    quote: str
    before: str = ""
    note: str


class PlainBody(BaseModel):
    quote: str
    before: str = ""
    question: str


class TierBody(BaseModel):
    tier: str


class VerdictBody(BaseModel):
    number: int
    decision: str
    note: str


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
# 轮次路由族(PLAN idi-02-02 Task 3,D-P2-22:FLOW-04/UI-02 的 HTTP 面)
# ---------------------------------------------------------------------------


@app.get("/api/rounds")
def get_rounds() -> JSONResponse:
    """轮次列表 + 当前轮号(完整轮列表来自 list_complete_rounds)。"""
    try:
        snapshot = session.snapshot()
    except RuntimeError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=400)
    return JSONResponse(
        {
            "status": "ok",
            "rounds": snapshot["rounds"],
            "current_round": snapshot["current_round"],
        }
    )


@app.get("/api/rounds/{round_n}")
def get_round(round_n: int) -> JSONResponse:
    """单轮视图:轮次文档全文 + annotations 合并(非完整轮 404)。"""
    try:
        snapshot = session.snapshot()
    except RuntimeError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=400)
    if round_n not in snapshot["rounds"]:
        return JSONResponse(
            {"status": "error", "message": "该轮不存在或不完整"}, status_code=404
        )
    from backend import annotations as annotations_mod

    project = session.current_project_path()
    doc_path = project / "docs" / f"discuss-round-{round_n}.md"
    try:
        document = doc_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        document = ""
    return JSONResponse(
        {
            "status": "ok",
            "round": round_n,
            "document": document,
            "annotations": annotations_mod.load(project, round_n),
        }
    )


@app.post("/api/rounds/{round_n}/annotations")
def post_annotation(round_n: int, body: AnnotationBody) -> JSONResponse:
    """建实质批注(type=comment,pending 落盘)。

    409 仅两条件(D-P2-22):非当前轮 / 非 phase3 —— 服务端强制(T-idi02-06,
    前端只是显示约束 D-P2-21);ValueError(quote 空等)→ 400。
    不做 busy 检查(写当前轮文件与 AI 回写上一轮不同对象,无竞态)。
    """
    if not body.quote.strip():
        return JSONResponse(
            {"status": "error", "message": "quote 不能为空(划选原文是必填项)"},
            status_code=400,
        )
    try:
        entry = session.add_annotation(round_n, body.quote, body.before, body.note)
    except RuntimeError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=409)
    except ValueError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=400)
    return JSONResponse({"status": "ok", "annotation": entry})


@app.post("/api/rounds/{round_n}/plain")
def post_plain(round_n: int, body: PlainBody) -> JSONResponse:
    """大白话即时答:同步 ask_lite + plain 条目落盘,返回 answer(§3.4/D-P2-10)。

    在飞 → 409;非当前轮/非 phase3 → 409;AI 调用失败 → 502;成功 200
    (answer 在条目的 answer 字段,前端可直读)。
    """
    if not body.quote.strip():
        return JSONResponse(
            {"status": "error", "message": "quote 不能为空(划选原文是必填项)"},
            status_code=400,
        )
    try:
        entry = session.answer_plain(
            round_n, body.quote, body.before, body.question
        )
    except RuntimeError as exc:
        message = str(exc)
        if message.startswith("大白话调用失败"):
            return JSONResponse(
                {"status": "error", "message": message}, status_code=502
            )
        if "在飞" in message or "进行中" in message:
            return JSONResponse(
                {"status": "error", "message": message}, status_code=409
            )
        return JSONResponse({"status": "error", "message": message}, status_code=409)
    except FileNotFoundError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=400)
    return JSONResponse({"status": "ok", "annotation": entry})


@app.post("/api/rounds/process")
def post_round_process() -> JSONResponse:
    """处理本轮批注(FLOW-04 / §4.4 G2):session.process_round,202 受理。

    非当前轮语义不适用(处理永远作用于当前轮);非 phase3 / 在飞 → 409。
    """
    try:
        accepted = session.process_round()
    except RuntimeError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=400)
    if not accepted:
        return JSONResponse(
            {
                "status": "error",
                "message": "轮次处理入口已关闭(非阶段 3 或当前有调用进行中)",
            },
            status_code=409,
        )
    return JSONResponse({"status": "accepted"}, status_code=202)


# ---------------------------------------------------------------------------
# 阶段 3/4/5 路由族(PLAN idi-03-02 + idi-03-03,D-P3-27:authorize/tier/verdict
# 三 POST + design/checks 两 GET + writing/start/repair 三条 202 受理路由)
# ---------------------------------------------------------------------------


@app.post("/api/authorize")
def authorize() -> JSONResponse:
    """G3 授权(FLOW-05 / §4.4 / §8.1):后端四查再查后写 AUTHORIZATION.md。

    无请求体——确认词在前端模态完成(D-P3-3),后端防线 = 四查再查 +
    authorize_write 动作本身。成功 → 200 新 derive_state(state=phase4);
    四查不过或已授权 → 409;未进项目 → 400。
    """
    try:
        accepted = session.authorize()
    except RuntimeError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=400)
    except FileExistsError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=409)
    if not accepted:
        return JSONResponse(
            {"status": "error", "message": "授权入口已关闭(四查未通过或已授权)"},
            status_code=409,
        )
    state = session.snapshot()
    return JSONResponse({"status": "ok", "state": state["state"]})


@app.post("/api/checks/tier")
def set_tier(body: TierBody) -> JSONResponse:
    """选档落盘(§8.2 / D-P3-11):写 docs/DESIGN-check-tier.md 签名文件。

    白名单外档位 → 400;非待选档阶段 → 409;成功 200。
    """
    try:
        session.set_tier(body.tier)
    except RuntimeError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=409)
    except ValueError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=400)
    return JSONResponse({"status": "ok"})


@app.post("/api/checks/verdict")
def post_verdict(body: VerdictBody) -> JSONResponse:
    """用户裁决追加落盘(§8.2 / §6.4 / D-P3-19):`> 裁决:#K:<decision>——<note>`。

    同号裁决已存在 → 409(一问一答);非自检阶段 → 409;在飞 → 409;
    未进项目 → 400;成功 200。残余全部配对时后端立即追加 PASS 收口
    (D-P3-17),响应附新 state 供前端感知 mission_complete。
    """
    try:
        accepted = session.verdict_append(body.number, body.decision, body.note)
    except RuntimeError as exc:
        message = str(exc)
        if message.startswith("尚未进入任何项目"):
            return JSONResponse({"status": "error", "message": message}, status_code=400)
        return JSONResponse({"status": "error", "message": message}, status_code=409)
    except FileExistsError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=409)
    if not accepted:
        return JSONResponse(
            {"status": "error", "message": "当前有调用进行中,请等它结束或先中止"},
            status_code=409,
        )
    state = session.snapshot()
    return JSONResponse({"status": "ok", "state": state["state"]})


@app.get("/api/design")
def get_design() -> JSONResponse:
    """DESIGN.md 全文(阶段 5/完成态前端渲染源,D-P3-27)。

    未进项目 → 400;文件不存在 → design: null(前端区分「尚未撰写」)。
    """
    try:
        project = session.current_project_path()
    except RuntimeError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=400)
    design_path = project / "DESIGN.md"
    if not design_path.is_file():
        return JSONResponse({"status": "ok", "design": None})
    try:
        content = design_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        content = None
    return JSONResponse({"status": "ok", "design": content})


@app.get("/api/checks")
def get_checks() -> JSONResponse:
    """check 报告列表 + 最新报告全文 + selfcheck 子状态(session snapshot 组合,
    D-P3-27;不重复判定——selfcheck 透传快照字段)。"""
    try:
        snapshot = session.snapshot()
    except RuntimeError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=400)
    project = session.current_project_path()
    docs_dir = project / "docs"
    from backend.state import latest_check_content, max_check_number

    max_check = max_check_number(docs_dir)
    checks_list = list(range(1, (max_check or 0) + 1))
    latest = latest_check_content(docs_dir)
    return JSONResponse(
        {
            "status": "ok",
            "checks": checks_list,
            "current_check": snapshot["current_check"],
            "latest": latest,
            "selfcheck": snapshot["selfcheck"],
        }
    )


@app.post("/api/writing")
def start_writing() -> JSONResponse:
    """撰写总设计文档(§7.3① / §7.4 行 4 / D-P3-6):session.start_writing,
    202 受理(分支照 /api/rounds/process 模子)。

    无请求体;非 phase4 / 在飞 → 409;未进项目 → 400。done 后 tmp 原子改名
    与事件流归 session 层(前端照 done-拉 /api/session 惯例,不新增收尾事件)。
    """
    try:
        accepted = session.start_writing()
    except RuntimeError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=400)
    if not accepted:
        return JSONResponse(
            {
                "status": "error",
                "message": "撰写入口已关闭(非阶段 4 或当前有调用进行中)",
            },
            status_code=409,
        )
    return JSONResponse({"status": "accepted"}, status_code=202)


@app.post("/api/checks/start")
def start_check() -> JSONResponse:
    """「继续自检」/首轮核查入口(§8.2 / D-P3-13 / D-P3-20):session.start_check,
    202 受理(check_n 与半份重跑判定全在 session 层,D-P3-21——路由零自算)。

    无请求体;未选档 / 非 phase5 / 在飞 → 409;未进项目 → 400。
    """
    try:
        accepted = session.start_check()
    except RuntimeError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=400)
    if not accepted:
        return JSONResponse(
            {
                "status": "error",
                "message": "自检入口已关闭(非自检阶段或当前有调用进行中)",
            },
            status_code=409,
        )
    return JSONResponse({"status": "accepted"}, status_code=202)


@app.post("/api/checks/repair")
def start_repair() -> JSONResponse:
    """「继续修复」入口(§8.2 / §6.4 判定式② / D-P3-14 / D-P3-20):
    session.start_repair,202 受理。

    无请求体;判定式②未命中(running / paused 待裁决 / 纯 P2 / 非
    phase5_checking)/ 在飞 → 409(unpaired 非空的服务端强制,T-idi03-13);
    未进项目 → 400。严格档自动链的 repair 跳走 session 内部驱动,不经本路由。
    """
    try:
        accepted = session.start_repair()
    except RuntimeError as exc:
        return JSONResponse({"status": "error", "message": str(exc)}, status_code=400)
    if not accepted:
        return JSONResponse(
            {
                "status": "error",
                "message": "修复入口已关闭(无待修问题或当前有调用进行中)",
            },
            status_code=409,
        )
    return JSONResponse({"status": "accepted"}, status_code=202)


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

# -*- coding: utf-8 -*-
"""GET /api/session 路由测试(Phase 1 UAT gap G-idi01-7 修复,TDD RED 先行)。

背景:会话轮产出 draft.md 后,前端 refreshDraftAfterStream() 需要拉新门控
(g1_available / divergence_available / 状态徽标),否则「认可雏形」按钮要
手动重进目录才解禁。POST /api/enter 不适合流后刷新(会整页重渲染 transcript,
冲掉刚流式出的 AI 气泡,且首拍 [ai] 尚未落盘),故新增只读 GET /api/session,
返回与 /api/enter 同构的 session.snapshot() 全量字段。
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from fastapi.testclient import TestClient  # noqa: E402

from backend import main, session  # noqa: E402


@pytest.fixture()
def route_env(tmp_path):
    """路由级测试环境:重置 session 状态 + 独立项目目录 + TestClient。"""
    session._reset_for_tests()
    client = TestClient(main.app)
    yield {"project": tmp_path, "docs": tmp_path / "docs", "client": client}
    session._reset_for_tests()


def test_route_session_without_entered_project(route_env):
    """未进入项目:GET /api/session → 4xx + status=error(不 500)。"""
    resp = route_env["client"].get("/api/session")
    assert resp.status_code == 400
    body = resp.json()
    assert body["status"] == "error"
    assert "尚未进入" in body["message"]


def test_route_session_mirrors_enter_payload_and_tracks_disk(route_env):
    """进入后:GET /api/session 与 POST /api/enter 同构,门控随磁盘现状翻转。"""
    client = route_env["client"]
    docs = route_env["docs"]
    docs.mkdir()
    (docs / "transcript.md").write_text("", encoding="utf-8")

    # 进入后首拍:docs/ 存在 → 阶段 1-2,雏形未生 → 发散开、G1 关
    entered = client.post("/api/enter", json={"path": str(route_env["project"])})
    assert entered.status_code == 200

    resp = client.get("/api/session")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["state"] == "phase12_in_progress"
    assert body["transcript"] == []
    assert body["draft"] is None
    assert body["g1_available"] is False
    assert body["divergence_available"] is True

    # 会话轮产出 draft.md 后【不重进】再拉:门控必须随磁盘对齐
    (docs / "draft.md").write_text("# 雏形\n", encoding="utf-8")
    body2 = client.get("/api/session").json()
    assert body2["status"] == "ok"
    assert body2["draft"] == "# 雏形\n"
    assert body2["g1_available"] is True
    assert body2["divergence_available"] is False
    assert body2["state"] == "phase12_in_progress"

    # G1 定稿后(完整轮存在)再拉:phase3、当前轮 1、两门全关
    (docs / "discuss-round-1.md").write_text(
        "# 第 1 轮\n\n> 申请授权:否\n", encoding="utf-8"
    )
    body3 = client.get("/api/session").json()
    assert body3["status"] == "ok"
    assert body3["state"] == "phase3"
    assert body3["current_round"] == 1
    assert body3["g1_available"] is False
    assert body3["divergence_available"] is False


# ---------------------------------------------------------------------------
# 轮次路由族 + 快照轮次字段(PLAN idi-02-02 Task 3,D-P2-15/D-P2-22)
# ---------------------------------------------------------------------------


def _enter_phase3_route(env, with_annotations=False):
    """直造 phase3:完整第 1 轮;可选补两条批注(1 pending comment + 1 plain)。"""
    from backend import annotations as annotations_mod

    docs = env["docs"]
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "discuss-round-1.md").write_text(
        "# 第 1 轮\n\n讲了目标与边界。\n\n> 申请授权:否\n", encoding="utf-8"
    )
    if with_annotations:
        annotations_mod.append_item(
            env["project"], 1,
            quote="目标与边界", before="", type="comment", note="这里没看懂",
        )
        annotations_mod.append_item(
            env["project"], 1,
            quote="讲了", before="",
            type="plain", note="随便问", answer="即时答一条",
        )
    entered = env["client"].post("/api/enter", json={"path": str(env["project"])})
    assert entered.status_code == 200
    return docs


def test_route_rounds_list_and_current(route_env):
    """用例 3:GET /api/rounds → {"rounds": [1], "current_round": 1}。"""
    _enter_phase3_route(route_env)
    resp = route_env["client"].get("/api/rounds")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["rounds"] == [1]
    assert body["current_round"] == 1


def test_route_round_single_and_404(route_env):
    """用例 4:GET /api/rounds/1 → 文档 + annotations;不存在的轮 5 → 404。"""
    _enter_phase3_route(route_env, with_annotations=True)
    client = route_env["client"]

    ok_resp = client.get("/api/rounds/1")
    assert ok_resp.status_code == 200
    body = ok_resp.json()
    assert body["status"] == "ok"
    assert body["round"] == 1
    assert "讲了目标与边界" in body["document"]
    assert "items" in body["annotations"]
    assert len(body["annotations"]["items"]) == 2

    not_found = client.get("/api/rounds/5")
    assert not_found.status_code == 404
    assert not_found.json()["status"] == "error"


def test_route_post_annotation_creates_and_409s(route_env):
    """用例 2:POST annotations 建条目(200 pending comment);非当前轮轮号 2 → 409。"""
    _enter_phase3_route(route_env)
    client = route_env["client"]

    ok_resp = client.post(
        "/api/rounds/1/annotations",
        json={"quote": "目标与边界", "before": "讲了", "note": "这里没看懂"},
    )
    assert ok_resp.status_code == 200
    body = ok_resp.json()
    assert body["status"] == "ok"
    entry = body["annotation"]
    assert entry["type"] == "comment"
    assert entry["status"] == "pending"

    # 非当前轮(轮号 2)→ 409(服务端强制,T-idi02-06)
    resp409 = client.post(
        "/api/rounds/2/annotations",
        json={"quote": "x", "before": "", "note": "y"},
    )
    assert resp409.status_code == 409

    # 空 quote → 400
    resp400 = client.post(
        "/api/rounds/1/annotations",
        json={"quote": " ", "before": "", "note": "y"},
    )
    assert resp400.status_code == 400


def test_route_post_plain_answers(route_env):
    """POST plain(路由级):同构 answer_plain —— Fake 打桩返回即时答落盘 200。"""
    _enter_phase3_route(route_env)

    class StubFake:
        def __init__(self):
            self.lite_calls = []

        def ask_lite(self, document_text, quoted_text, question):
            self.lite_calls.append((document_text, quoted_text, question))
            return {"answer": "即时答:字面意思。"}

    from backend import session as session_mod

    stub = StubFake()
    session_mod._set_caller_for_tests(stub)

    resp = route_env["client"].post(
        "/api/rounds/1/plain",
        json={"quote": "目标与边界", "before": "讲了", "question": "这段什么意思"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    entry = body["annotation"]
    assert entry["type"] == "plain"
    assert entry["status"] == "answered"
    assert entry["answer"] == "即时答:字面意思。"
    assert len(stub.lite_calls) == 1


def test_route_post_plain_502_on_ai_error(route_env):
    """用例 5 补:AI 调用失败(answer 空 + error)→ 502。"""
    _enter_phase3_route(route_env)

    class FailingFake:
        def ask_lite(self, document_text, quoted_text, question):
            return {"answer": "", "error": "大白话调用未返回结果"}

    from backend import session as session_mod

    session_mod._set_caller_for_tests(FailingFake())

    resp = route_env["client"].post(
        "/api/rounds/1/plain",
        json={"quote": "x", "before": "", "question": "y"},
    )
    assert resp.status_code == 502
    body = resp.json()
    assert body["status"] == "error"


def test_route_process_round_202_or_409(route_env):
    """用例 6:POST /api/rounds/process → 202 受理(不真跑完,更轻的入口级验证)。"""
    _enter_phase3_route(route_env)

    class NoRunFake:
        def run(self, project_path, prompt):
            self.run_calls = [(str(project_path), prompt)]
            yield {"kind": "done", "content": "调用结束", "raw": None}

    from backend import session as session_mod
    import threading

    no_run = NoRunFake()
    session_mod._set_caller_for_tests(no_run)

    resp = route_env["client"].post("/api/rounds/process")
    assert resp.status_code == 202
    assert resp.json()["status"] == "accepted"
    assert resp.json().get("accepted") or resp.json()["status"] == "accepted"

    # 等后台线程收流(避免状态泄漏下一个用例)
    deadline = threading.Event()
    import time as _time
    t0 = _time.time()
    while session_mod.busy() and _time.time() - t0 < 5:
        _time.sleep(0.05)
    deadline.set()


def test_route_process_round_409_non_phase3(route_env):
    """非 phase3(纯会话目录)→ 409。"""
    docs = route_env["docs"]
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "transcript.md").write_text("", encoding="utf-8")
    entered = route_env["client"].post("/api/enter", json={"path": str(route_env["project"])})
    assert entered.status_code == 200

    resp = route_env["client"].post("/api/rounds/process")
    assert resp.status_code == 409


def test_route_session_snapshot_rounds_fields(route_env):
    """用例 6(快照):GET /api/session 新增 rounds 与 pending_annotations;plain 不计。"""
    _enter_phase3_route(route_env, with_annotations=True)
    client = route_env["client"]

    resp = client.get("/api/session")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    # rounds 字段 = 完整轮列表
    assert body["rounds"] == [1]
    # pending_annotations = 1(1 条 pending comment;plain 不计,D-P2-15)
    assert body["pending_annotations"] == 1


# ---------------------------------------------------------------------------
# 阶段 3/4/5 快照扩展 + authorize/tier/verdict/design/checks 路由族
# (PLAN idi-03-02 Task 3 / D-P3-10 / D-P3-17 / D-P3-20 / D-P3-23 / D-P3-27)
# ---------------------------------------------------------------------------


def _compliant_round_doc_route(marker: str = "> 申请授权:是") -> str:
    """四查合规轮文档样本(与 test_session.py 同族,route 侧独立副本)。"""
    return (
        "# 第 1 轮讨论\n\n"
        "## 批注回应\n\n"
        "| 批注id | 原文摘录 | 回应 |\n|---|---|---|\n"
        "| a1-01 | 目标与边界 | 已补充说明。 |\n\n"
        "## 决策登记\n\n- D1:已对齐。\n\n"
        "## 覆盖维度表\n\n"
        "| 维度 | 状态 | 说明 |\n|---|---|---|\n"
        "| 目标与边界 | ✓ | 已对齐 |\n\n"
        "## 未决问题清单\n\n"
        "| 编号 | 问题 | 状态 |\n|---|---|---|\n"
        "| 1 | 用户画像 | 已决 |\n\n"
        f"{marker}\n"
    )


def _check_report_route(tier="严格", problems=None, conclusion="> 核查结论:FIX(P1×1)",
                        pending_questions=None, verdict_lines=None) -> str:
    """手造核查报告样本(route 侧,文法与 grammar 解析器一字不差)。"""
    lines = [f"# 核查报告\n\n> 自检档位:{tier}\n\n## 问题分级\n\n"]
    if problems:
        lines.append("| 编号 | 级别 | 位置 | 问题 | 建议修法 |\n|---|---|---|---|---|\n")
        for n, level, loc, issue, sug in problems:
            lines.append(f"| {n} | {level} | {loc} | {issue} | {sug} |\n")
    lines.append(f"\n{conclusion}\n")
    if pending_questions or verdict_lines:
        lines.append("\n")
        for n, text in pending_questions or []:
            lines.append(f"> 待裁决:#{n}:{text}\n")
        for n, text in verdict_lines or []:
            lines.append(f"> 裁决:#{n}:{text}\n")
    return "".join(lines)


def _enter_phase3_g3_route(env):
    """直造四查合规 phase3(完整合规第 1 轮)→ 进入项目。"""
    docs = env["docs"]
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "discuss-round-1.md").write_text(
        _compliant_round_doc_route(), encoding="utf-8"
    )
    entered = env["client"].post("/api/enter", json={"path": str(env["project"])})
    assert entered.status_code == 200
    return docs


def _enter_phase4_route(env, with_tmp=False):
    """直造 phase4(合规轮 + AUTHORIZATION.md)→ 进入项目。"""
    docs = _enter_phase3_g3_route(env)
    (env["project"] / "AUTHORIZATION.md").write_text(
        "# 授权记录\n\n- 操作者确认词:确认授权\n", encoding="utf-8"
    )
    if with_tmp:
        (env["project"] / "DESIGN.md.tmp").write_text("半份\n", encoding="utf-8")
    return docs


def _enter_phase5_route(env, design="# 总设计文档\n\n正文。\n",
                        check_reports=None, tier=None):
    """直造阶段 5(合规轮 + 授权 + DESIGN.md + 可选报告族)→ 进入项目。"""
    docs = _enter_phase4_route(env)
    (env["project"] / "DESIGN.md").write_text(design, encoding="utf-8")
    for n, text in (check_reports or {}).items():
        (docs / f"DESIGN-check-{n}.md").write_text(text, encoding="utf-8")
    if tier is not None:
        (docs / "DESIGN-check-tier.md").write_text(
            f"> 自检档位:{tier}\n", encoding="utf-8"
        )
    return docs




def _reenter_fresh_route(env, tag, maker):
    """重进一个全新子项目目录(同 client;旧盘文件不跨场景污染,
    tmp_path fixture 下残留是预期垃圾,pytest 自动清理)。"""
    new_dir = env["project"].parent / (env["project"].name + "-" + tag)
    new_dir.mkdir(parents=True, exist_ok=True)
    session._reset_for_tests()
    fresh_env = {"project": new_dir, "docs": new_dir / "docs", "client": env["client"]}
    maker(fresh_env)
    return fresh_env


def test_route_snapshot_g3_available(route_env):
    """用例 1:快照 g3_available——四查合规 phase3 → true;维度污染盘 → false。"""
    _enter_phase3_g3_route(route_env)
    body = route_env["client"].get("/api/session").json()
    assert body["state"] == "phase3"
    assert body["g3_available"] is True

    # 维度污染(◐)→ false
    (route_env["docs"] / "discuss-round-1.md").write_text(
        _compliant_round_doc_route().replace(
            "| 目标与边界 | ✓ | 已对齐 |", "| 目标与边界 | ◐ | 未对齐 |"
        ),
        encoding="utf-8",
    )
    body2 = route_env["client"].get("/api/session").json()
    assert body2["g3_available"] is False


def test_route_snapshot_writing_tmp_exists(route_env):
    """用例 2:快照 writing_tmp_exists——phase4 有/无 tmp 二态(D-P3-10);phase3 → false。"""
    _enter_phase4_route(route_env, with_tmp=True)
    body = route_env["client"].get("/api/session").json()
    assert body["state"] == "phase4"
    assert body["writing_tmp_exists"] is True

    # 删 tmp → false
    (route_env["project"] / "DESIGN.md.tmp").unlink()
    body2 = route_env["client"].get("/api/session").json()
    assert body2["writing_tmp_exists"] is False

    # phase3 盘(全新子目录,防旧盘残留)→ false
    fresh_env = _reenter_fresh_route(route_env, "p3", _enter_phase3_g3_route)
    body3 = fresh_env["client"].get("/api/session").json()
    assert body3["state"] == "phase3"
    assert body3["writing_tmp_exists"] is False


def test_route_snapshot_selfcheck_paused(route_env):
    """用例 3:快照 selfcheck——报告含未配对待裁决 → mode=paused、
    questions 为 {number, text} 抛问卡数据(D-P3-18/19)。"""
    _enter_phase5_route(
        route_env,
        check_reports={1: _check_report_route(
            problems=[(1, "P1", "§2", "范围含糊", "写清")],
            conclusion="> 核查结论:FIX(P1×1)",
            pending_questions=[(2, "范围问题")],
        )},
        tier="严格",
    )
    body = route_env["client"].get("/api/session").json()
    assert body["state"] == "phase5_checking"
    sc = body["selfcheck"]
    assert sc["mode"] == "paused"
    assert sc["tier"] == "严格"
    assert sc["questions"] == [{"number": 2, "text": "范围问题"}]


def test_route_snapshot_selfcheck_p2(route_env):
    """用例 4:快照 selfcheck——纯 P2 报告(无待裁决、末行非 PASS)→ mode=p2、
    questions 键集 = {number, location, issue, suggestion}(残余裁决卡,plan 04
    renderVerdictCard 消费面一字不差)。"""
    _enter_phase5_route(
        route_env,
        check_reports={1: _check_report_route(
            problems=[(2, "P2", "§5", "排版建议", "可选优化")],
            conclusion="> 核查结论:FIX(P2×1)",
        )},
        tier="严格",
    )
    body = route_env["client"].get("/api/session").json()
    sc = body["selfcheck"]
    assert sc["mode"] == "p2"
    assert sc["tier"] == "严格"
    assert len(sc["questions"]) == 1
    q = sc["questions"][0]
    assert set(q.keys()) == {"number", "location", "issue", "suggestion"}
    assert q["number"] == 2 and q["location"] == "§5"


def test_route_snapshot_selfcheck_half_p2_running(route_env):
    """用例 5:半份 P2 报告(P2 表已写、无结论行锚点)→ mode=running、questions=[]
    (is_pure_p2 半份 fail-closed;「继续自检」重跑恢复,不进 p2 死局态)。"""
    _enter_phase5_route(
        route_env,
        check_reports={1: (
            "# 核查报告\n\n> 自检档位:严格\n\n## 问题分级\n\n"
            "| 编号 | 级别 | 位置 | 问题 | 建议修法 |\n|---|---|---|---|---|\n"
            "| 1 | P2 | §5 | 排版建议 | 可选优化 |\n"
        )},  # 无 `> 核查结论:` 行 = 半份
        tier="严格",
    )
    body = route_env["client"].get("/api/session").json()
    sc = body["selfcheck"]
    assert sc["mode"] == "running"
    assert sc["questions"] == []


def test_route_snapshot_selfcheck_resumed_running_done(route_env):
    """用例 6:快照 selfcheck——resumed(配对裁决)/ running(无裁决签名,tier 恢复)/
    done(mission_complete)/ awaiting_tier(tier 文件值)。"""
    # resumed:配对裁决 + 末行非 PASS
    _enter_phase5_route(
        route_env,
        check_reports={1: _check_report_route(
            problems=[(1, "P1", "§2", "范围含糊", "写清"), (2, "P1", "§4", "歧义", "直说")],
            conclusion="> 核查结论:FIX(P1×2)",
            pending_questions=[(1, "范围?")],
            verdict_lines=[(1, "修——照办")],
        )},
        tier="严格",
    )
    body = route_env["client"].get("/api/session").json()
    assert body["selfcheck"]["mode"] == "resumed"

    # running:正常报告(无裁决行无待裁决行),tier 从报告头部行恢复
    fresh_env = _reenter_fresh_route(
        route_env, "running",
        lambda e: _enter_phase5_route(
            e,
            check_reports={1: _check_report_route(
                problems=[(1, "P1", "§2", "范围含糊", "写清")],
                conclusion="> 核查结论:FIX(P1×1)",
            )},
            tier=None,  # 无 tier 文件——tier 只能从报告头部恢复
        ),
    )
    body2 = fresh_env["client"].get("/api/session").json()
    assert body2["selfcheck"]["mode"] == "running"
    assert body2["selfcheck"]["tier"] == "严格", "tier 应从报告头部行恢复"

    # done:mission_complete(报告末行 PASS)
    fresh_env = _reenter_fresh_route(
        route_env, "done",
        lambda e: _enter_phase5_route(
            e,
            check_reports={1: _check_report_route(conclusion="> 核查结论:PASS")},
            tier="宽松",
        ),
    )
    body3 = fresh_env["client"].get("/api/session").json()
    assert body3["state"] == "mission_complete"
    assert body3["selfcheck"]["mode"] == "done"

    # awaiting_tier:tier 文件值或 None(重开恢复档位,无报告时 tier 文件为
    # 中间态凭证)
    fresh_env = _reenter_fresh_route(
        route_env, "await",
        lambda e: _enter_phase5_route(e, check_reports={}, tier=None),
    )
    body4 = fresh_env["client"].get("/api/session").json()
    assert body4["state"] == "phase5_awaiting_tier"
    assert body4["selfcheck"] == {"tier": None, "mode": "running", "questions": []}
    # 写 tier 文件 → 恢复档位值
    (fresh_env["docs"] / "DESIGN-check-tier.md").write_text(
        "> 自检档位:宽松\n", encoding="utf-8"
    )
    body5 = fresh_env["client"].get("/api/session").json()
    assert body5["selfcheck"]["tier"] == "宽松"


def test_route_design(route_env):
    """用例 7:GET /api/design——phase5+ → 200 全文;无 DESIGN.md → design: null。"""
    _enter_phase5_route(route_env)
    resp = route_env["client"].get("/api/design")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "# 总设计文档" in body["design"]

    # phase4(子造全新目录,无 DESIGN.md)→ null
    fresh_env = _reenter_fresh_route(route_env, "p4", _enter_phase4_route)
    body2 = fresh_env["client"].get("/api/design").json()
    assert body2["status"] == "ok"
    assert body2["design"] is None


def test_route_checks(route_env):
    """用例 8:GET /api/checks——phase5_checking → 200 checks 编号列表 +
    latest 报告全文 + selfcheck 对象(透传 snapshot 字段)。"""
    report1 = _check_report_route(
        problems=[(1, "P1", "§2", "范围含糊", "写清")],
        conclusion="> 核查结论:FIX(P1×1)",
    )
    report2 = _check_report_route(
        problems=[(2, "P2", "§5", "排版建议", "可选优化")],
        conclusion="> 核查结论:FIX(P2×1)",
    )
    _enter_phase5_route(
        route_env,
        check_reports={1: report1, 2: report2},
        tier="严格",
    )
    resp = route_env["client"].get("/api/checks")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["checks"] == [1, 2]
    assert body["current_check"] == 2
    assert "排版建议" in body["latest"], "latest = 最新报告全文"
    assert body["selfcheck"]["mode"] == "p2", "selfcheck 透传快照字段"


def test_route_verdict_all_branches(route_env):
    """用例 9:POST /api/checks/verdict——200 追加 / 同号 FileExistsError → 409 /
    非 phase5_checking → 409 / 未进项目 → 400。"""
    # 未进项目 → 400
    resp0 = route_env["client"].post(
        "/api/checks/verdict", json={"number": 1, "decision": "修", "note": "x"}
    )
    assert resp0.status_code == 400

    _enter_phase5_route(
        route_env,
        check_reports={1: _check_report_route(
            problems=[(1, "P1", "§2", "范围含糊", "写清")],
            conclusion="> 核查结论:FIX(P1×1)",
            pending_questions=[(1, "范围?"), (2, "另一问题?")],
        )},
        tier="严格",
    )
    client = route_env["client"]

    # 200 追加(#1 裁决;#2 仍待裁决 → 不收口)
    resp = client.post(
        "/api/checks/verdict", json={"number": 1, "decision": "修", "note": "按建议"}
    )
    assert resp.status_code == 200
    assert resp.json()["state"] == "phase5_checking"

    # 同号 FileExistsError → 409
    resp409 = client.post(
        "/api/checks/verdict", json={"number": 1, "decision": "再修", "note": "重复"}
    )
    assert resp409.status_code == 409

    # 非 phase5_checking(phase5_awaiting_tier,全新子目录)→ 409
    fresh_env = _reenter_fresh_route(
        route_env, "await",
        lambda e: _enter_phase5_route(e, check_reports={}, tier=None),
    )
    resp_state = fresh_env["client"].post(
        "/api/checks/verdict", json={"number": 1, "decision": "修", "note": "x"}
    )
    assert resp_state.status_code == 409
    assert "仅自检进行中可裁决" in resp_state.json()["message"]


def test_route_authorize_all_branches(route_env):
    """用例 10:POST /api/authorize——成功 200 返回新 state / 四查不过 409 /
    已授权(phase4 造盘直接 POST)→ 409 幂等。"""
    client = route_env["client"]

    # 四查合规 → 200 + state=phase4
    _enter_phase3_g3_route(route_env)
    resp = client.post("/api/authorize")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["state"] == "phase4"

    # 已授权(derive_state 已 phase4)→ 409 幂等
    resp409 = client.post("/api/authorize")
    assert resp409.status_code == 409

    # 四查不过(维度污染)→ 409
    session._reset_for_tests()
    docs = route_env["docs"]
    (docs / "discuss-round-1.md").write_text(
        _compliant_round_doc_route().replace(
            "| 目标与边界 | ✓ | 已对齐 |", "| 目标与边界 | ◐ | 未对齐 |"
        ),
        encoding="utf-8",
    )
    entered = client.post("/api/enter", json={"path": str(route_env["project"])})
    assert entered.status_code == 200
    resp_pollute = client.post("/api/authorize")
    assert resp_pollute.status_code == 409


def test_route_tier_all_branches(route_env):
    """用例 11:POST /api/checks/tier——成功 200 / phase5_awaiting_tier 白名单外 400 /
    非 phase5_awaiting_tier(phase3)→ 409。"""
    client = route_env["client"]

    # phase5_awaiting_tier:成功落盘 + 同值幂等
    _enter_phase5_route(route_env, check_reports={}, tier=None)
    resp = client.post("/api/checks/tier", json={"tier": "严格"})
    assert resp.status_code == 200
    resp_again = client.post("/api/checks/tier", json={"tier": "严格"})
    assert resp_again.status_code == 200, "同值重选覆盖幂等合法"

    # 白名单外 → 400
    resp400 = client.post("/api/checks/tier", json={"tier": "超严格"})
    assert resp400.status_code == 400

    # 非 phase5_awaiting_tier(phase3,全新子目录)→ 409
    fresh_env = _reenter_fresh_route(route_env, "p3t", _enter_phase3_g3_route)
    resp409 = fresh_env["client"].post("/api/checks/tier", json={"tier": "宽松"})
    assert resp409.status_code == 409
    assert "仅待选档阶段可选" in resp409.json()["message"]

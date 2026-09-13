# -*- coding: utf-8 -*-
"""端到端真 CLI 用例(PLAN idi-03-05 Task 1):G3 授权 → 撰写 → 选档 → 核查 → PASS 全链真验证。

两条 @pytest.mark.slow 用例,IDI_E2E 未设时 skip(常规跑不依赖真 AI):
  1. test_authorize_and_writing_real_cli —— 四查合规造盘 → authorize(真调用
     前半段纯后端)→ start_writing 真调用 → AI 写 DESIGN.md.tmp → 后端原子改名
     DESIGN.md → derive_state 前进 phase5_awaiting_tier
  2. test_selfcheck_real_cli_loose —— 接续选档(宽松)→ start_check 真调用 →
     docs/DESIGN-check-1.md 产出(头部档位行 + 问题分级表)→ 宽松一检一修 + PASS
     即止 → derive_state = mission_complete;若入纯 P2 残余分支则逐条 verdict
     收口(两条分支都合法,按真实报告断言并如实记录走向)

路线覆盖度(诚实记录):真 E2E 只跑 config.ai_caller 当前配置的路线——
另一条路线(未配置者)的写作/核查/修复链路从未被真调用,仅由 Wave 1-4 的
同形单测承担契约一致性(本文件不冒充双路线均已真验)。真调用未触发的分支
(严格档完整循环、修复者真抛问暂停)同样如实记录「由 Fake 级用例覆盖」。
"""

import json
import os
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend import session  # noqa: E402
from backend.grammar import (  # noqa: E402
    parse_problem_grades,
    parse_tier_line,
    parse_verdict_lines,
)
from backend.state import derive_state  # noqa: E402

pytestmark = pytest.mark.slow

# 真实调用时长门限(照 test_e2e_rounds.py 先例;T-idi03-19 超时即 fail 输出已等待时长)
_FIRST_EVENT_WINDOW_SECONDS = 120   # 存活窗口:首条事件(CLI 冷启动实测可 >60s)
_WRITING_DEADLINE_SECONDS = 420     # 撰写总限(首事件后;长文档撰写方差大)
_CHECK_DEADLINE_SECONDS = 600       # 核查+自动修复跳总限(含两跳)
_POLL_INTERVAL = 1.0


def _e2e_enabled() -> bool:
    return os.environ.get("IDI_E2E") == "1"


# 四查合规轮次文档(§4.4:维度表全绿 + 未决清单清零 + 末行授权标记「是」)
_ROUND1_READY_BODY = (
    "# 第 1 轮讨论文档\n\n"
    "本项目目标:把一次讨论收敛成一份可实施的总设计文档。\n\n"
    "## 批注回应\n\n"
    "| 批注id | 原文摘录 | 回应 |\n"
    "|---|---|---|\n"
    "| a1-01 | 首轮无批注 | 首轮建盘无上轮批注 |\n\n"
    "## 覆盖维度表\n\n"
    "| 维度 | 状态 | 说明 |\n"
    "|---|---|---|\n"
    "| 目标与边界 | ✓ | 目标已写入文档 |\n"
    "| 非目标 | ✓ | 非目标已明确 |\n"
    "| 验收标准 | ✓ | 验收标准已定 |\n\n"
    "## 未决问题清单\n\n"
    "| 编号 | 问题 | 状态 |\n"
    "|---|---|---|\n"
    "| 1 | 无待决问题 | 已决 |\n\n"
)


def _write_g3_ready_project(project: Path) -> None:
    """造盘一个 phase3 四查合规项目(docs/ 轮次文档 + 空 annotations + transcript)。"""
    docs = project / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "discuss-round-1.md").write_text(
        _ROUND1_READY_BODY + "\n> 申请授权:是\n", encoding="utf-8"
    )
    # 空 items 证明无 pending comment(四查①)
    (docs / "discuss-round-1.annotations.json").write_text(
        json.dumps({"round": 1, "items": []}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    # §6.4 transcript 格式:每条消息 = 起始行 [user]/[ai] 独占一行,其后消息体
    (docs / "transcript.md").write_text(
        "[user]\n\n开始讨论。\n\n[ai]\n\n好的,我们先对齐目标。\n",
        encoding="utf-8",
    )


def _wait_first_event(recorder, sess, window: float) -> bool:
    """存活窗口:window 秒内出现首条事件返回 True;调用已结束返回 False。"""
    deadline = time.monotonic() + window
    while not recorder.events and time.monotonic() < deadline:
        if not sess.busy():
            return False
        time.sleep(_POLL_INTERVAL)
    return bool(recorder.events)


def wait_idle(sess, timeout: float) -> tuple[bool, float]:
    """等在飞调用结束(照 test_e2e_rounds.py 形态;返回诚实耗时)。"""
    start = time.monotonic()
    deadline = start + timeout
    while sess.busy() and time.monotonic() < deadline:
        time.sleep(_POLL_INTERVAL)
    return (not sess.busy(), time.monotonic() - start)


class _EventRecorder:
    """记录 SSE 事件流(诊断 seam:包装 session._publish_for_tests)。"""

    def __init__(self, sess):
        self._sess = sess
        self._orig = sess._publish_for_tests
        self.events: list[dict] = []

    def __enter__(self):
        self._sess._publish_for_tests = self._record  # type: ignore[method-assign]
        return self

    def __exit__(self, *exc):
        self._sess._publish_for_tests = self._orig  # type: ignore[method-assign]
        return False

    def _record(self, event: dict) -> None:
        self.events.append(dict(event))
        self._orig(event)

    def summary(self) -> str:
        if not self.events:
            kinds = "(零事件)"
        else:
            kinds = ",".join(
                f"{k}x{n}"
                for k, n in sorted(
                    (k, sum(1 for e in self.events if e.get("kind") == k))
                    for k in {e.get("kind") for e in self.events}
                )
            )
        tail = "; ".join(
            f"{e.get('kind')}:{str(e.get('content', ''))[:60]}" for e in self.events[-3:]
        )
        with self._sess._lock:
            pending_n = len(self._sess._pending)
        return f"事件概要[{kinds}] 末3条[{tail}] 未决权限确认 {pending_n} 项"


def _start_unattended_denier(sess):
    """无人值守权限处理:后台线程序贯驳回全部挂起权限(§5.4 保守精神)。

    产品语义「confirm 无限等用户」对无人值守测试是死锁;写 docs/ 关键路径
    按规则 3 直接 allow 不经此循环(照 test_e2e_rounds.py 先例)。
    """
    import threading

    stop = threading.Event()
    denied: list[str] = []

    def _deny():
        while not stop.is_set():
            pid = sess._wait_for_pending_for_tests(timeout=1.0)
            if pid is not None:
                denied.append(str(pid))
                sess.resolve_permission(pid, False)

    thread = threading.Thread(target=_deny, daemon=True)
    thread.start()
    return stop, thread, denied


def test_authorize_and_writing_real_cli(tmp_path):
    """E2E 1:授权凭证 → 真撰写 → tmp 原子改名 → derive_state 前进 phase5。"""
    if not _e2e_enabled():
        pytest.skip("IDI_E2E 未设(常规跑不依赖真 AI)")

    project = tmp_path / "g3_writing_project"
    project.mkdir()
    _write_g3_ready_project(project)

    session._reset_for_tests()
    snapshot = session.enter_project(project)
    assert snapshot["state"] == "phase3", (
        f"造盘后应推导为 phase3,实际:{snapshot['state']}"
    )
    assert snapshot["g3_available"] is True, (
        "四查应全过(g3_available=True;造盘维度表/清单/标记不合规?)"
    )

    # 真调用前半段:authorize 是纯后端动作(零 AI),此处验证凭证落盘与推导前进
    accepted = session.authorize()
    assert accepted is True, "authorize 未受理(四查再查拒绝)"
    auth_path = project / "AUTHORIZATION.md"
    assert auth_path.is_file(), "AUTHORIZATION.md 未落盘(授权凭证缺失)"
    assert "确认授权" in auth_path.read_text(encoding="utf-8"), (
        "AUTHORIZATION.md 未含操作者确认词标记行"
    )
    state_after_auth = derive_state(project)
    assert state_after_auth["state"] == "phase4", (
        f"授权后应推导为 phase4,实际:{state_after_auth['state']}"
    )

    stop, denier, denied = _start_unattended_denier(session)
    recorder = _EventRecorder(session)
    try:
        with recorder:
            started = session.start_writing()
            assert started is True, (
                "start_writing 未受理(入口校验拒绝:非 phase4 或在飞?)"
            )
            if not _wait_first_event(recorder, session, _FIRST_EVENT_WINDOW_SECONDS):
                pytest.fail(
                    f"撰写调用 {_FIRST_EVENT_WINDOW_SECONDS}s 内零事件"
                    f"(CLI 子进程启动即挂死;已驳回权限 {len(denied)} 次;"
                    f"{recorder.summary()};T-idi03-19 真实发现)"
                )
            t0 = time.monotonic()
            idle, waited = wait_idle(session, _WRITING_DEADLINE_SECONDS)
            elapsed = time.monotonic() - t0
            if not idle:
                session.abort()
                time.sleep(2)
                pytest.fail(
                    f"撰写调用有事件流但 {_WRITING_DEADLINE_SECONDS}s 内未收流"
                    f"(已等待 {waited:.0f}s;已驳回权限 {len(denied)} 次;"
                    f"{recorder.summary()};T-idi03-19)"
                )
    finally:
        stop.set()
        denier.join(timeout=3)

    design_path = project / "DESIGN.md"
    tmp_path_ = project / "DESIGN.md.tmp"
    assert design_path.is_file(), (
        f"DESIGN.md 未落盘(docs/ 现有文件:{sorted(p.name for p in (project / 'docs').iterdir())};"
        f"AI 未按落盘指令写 DESIGN.md.tmp 或后端改名未发生;"
        f"已驳回权限 {len(denied)} 次;{recorder.summary()})"
    )
    assert not tmp_path_.is_file(), (
        "DESIGN.md.tmp 仍存在(tmp → DESIGN.md 原子改名未发生,D-P3-8)"
    )
    state_final = derive_state(project)
    assert state_final["state"] == "phase5_awaiting_tier", (
        f"撰写完成后应推导为 phase5_awaiting_tier(初稿无 check 报告),"
        f"实际:{state_final['state']}"
    )
    print(f"\n[撰写实测耗时] {elapsed:.1f}s")
    session._reset_for_tests()


def test_selfcheck_real_cli_loose(tmp_path):
    """E2E 2:选档(宽松)→ 真核查 → 报告文法合规 → PASS/残余收口 → mission_complete。"""
    if not _e2e_enabled():
        pytest.skip("IDI_E2E 未设(常规跑不依赖真 AI)")

    project = tmp_path / "g3_check_project"
    project.mkdir()
    _write_g3_ready_project(project)

    session._reset_for_tests()
    session.enter_project(project)
    assert session.authorize() is True, "authorize 未受理"
    # 直接落 DESIGN.md(隔离变量:本用例验核查链,不重复验撰写链——用例 1 已真验)
    (project / "DESIGN.md").write_text(
        "# 总设计文档\n\n## 目标\n\n把一次讨论收敛成可实施的设计。\n\n"
        "## 边界\n\n仅本工具职责范围。\n\n## 验收\n\n五条判据全绿。\n",
        encoding="utf-8",
    )
    state_awaiting = derive_state(project)
    assert state_awaiting["state"] == "phase5_awaiting_tier", (
        f"落 DESIGN.md 后应推导为 phase5_awaiting_tier,实际:{state_awaiting['state']}"
    )

    # 选档:宽松(一检一修即止,时长可控;严格档完整循环真调用耗时不可预算)
    assert session.set_tier("宽松") is True, "set_tier 未受理"
    tier_path = project / "docs" / "DESIGN-check-tier.md"
    assert tier_path.is_file(), "档位签名文件未落盘(D-P3-11)"
    assert "宽松" in tier_path.read_text(encoding="utf-8"), "档位签名内容不含「宽松」"

    stop, denier, denied = _start_unattended_denier(session)
    recorder = _EventRecorder(session)
    try:
        with recorder:
            started = session.start_check()
            assert started is True, "start_check 未受理(未选档/非 phase5/在飞?)"
            if not _wait_first_event(recorder, session, _FIRST_EVENT_WINDOW_SECONDS):
                pytest.fail(
                    f"核查调用 {_FIRST_EVENT_WINDOW_SECONDS}s 内零事件"
                    f"(已驳回权限 {len(denied)} 次;{recorder.summary()};T-idi03-19)"
                )
            t0 = time.monotonic()
            idle, waited = wait_idle(session, _CHECK_DEADLINE_SECONDS)
            elapsed = time.monotonic() - t0
            if not idle:
                session.abort()
                time.sleep(2)
                pytest.fail(
                    f"核查调用有事件流但 {_CHECK_DEADLINE_SECONDS}s 内未收流"
                    f"(已等待 {waited:.0f}s;已驳回权限 {len(denied)} 次;"
                    f"{recorder.summary()};T-idi03-19)"
                )
    finally:
        stop.set()
        denier.join(timeout=3)

    # 报告产出 + 头部档位行合规(§8.2 / D-P3-12)
    report_path = project / "docs" / "DESIGN-check-1.md"
    assert report_path.is_file(), (
        f"DESIGN-check-1.md 未产出(docs/ 现有文件:"
        f"{sorted(p.name for p in (project / 'docs').iterdir())};"
        f"已驳回权限 {len(denied)} 次;{recorder.summary()})"
    )
    report_text = report_path.read_text(encoding="utf-8", errors="replace")
    assert parse_tier_line(report_text) == "宽松", (
        f"报告头部档位行非「宽松」(实际:{parse_tier_line(report_text)!r};"
        "prompt 档位注入或 AI 文法遵守有偏差)"
    )
    # 问题分级表可解析(零问题报告亦合法:parse_problem_grades → [])
    grades = parse_problem_grades(report_text)
    print(f"\n[核查实测耗时] {elapsed:.1f}s;问题分级表 {len(grades)} 行")

    state_after_check = derive_state(project)
    if state_after_check["state"] == "mission_complete":
        # 理想分支:宽松一检一修 + PASS 即止(或零问题直 PASS)
        print("[分支] 宽松档一检一修即止 → mission_complete")
    else:
        # 残余分支:纯 P2 轮进入裁决态,逐条裁决(主张全修)→ 续跑修复 → 收口
        assert state_after_check["state"] == "phase5_checking", (
            f"核查后应为 mission_complete 或 phase5_checking,实际:{state_after_check['state']}"
        )
        snapshot = session.snapshot()
        mode = snapshot["selfcheck"]["mode"]
        questions = snapshot["selfcheck"]["questions"]
        print(f"[分支] 核查后 mode={mode},残余问题 {len(questions)} 条 → 逐条裁决收口")
        assert mode in ("p2", "paused", "resumed"), (
            f"残余分支 mode 应为 p2/paused/resumed,实际:{mode}"
        )
        # 逐条裁决落盘(一问一答;同号已裁的跳过——重启恢复语义)
        answered = {
            v["number"]
            for v in parse_verdict_lines(
                report_path.read_text(encoding="utf-8", errors="replace")
            )
            if v["kind"] == "裁决"
        }
        for q in questions:
            if q["number"] in answered:
                continue
            accepted = session.verdict_append(q["number"], "修", "E2E 主张全修")
            assert accepted is True, f"裁决 #{q['number']} 未受理"
        # 裁决落盘后两条合法走向(D-P3-17 / D-P3-19):
        #   a) 残余已清零 → 后端立即追加 PASS 收口(mission_complete);
        #   b) 仍有残余(如问题表含未抛问的 P2)→ resumed 态,「继续修复」放行
        mid = session.snapshot()
        if mid["state"] == "mission_complete":
            print("[分支] 裁决落盘即残余清零 → 后端自动 PASS 收口")
            state_final = derive_state(project)
            assert state_final["state"] == "mission_complete"
        else:
            assert mid["selfcheck"]["mode"] == "resumed", (
                f"裁决落盘后应为 resumed 态或已收口,实际:{mid['selfcheck']['mode']}"
            )
            assert session.repair_available(project) is True, (
                "裁决已配对且末行非 PASS 时「继续修复」应放行(D-P3-20 判定式②)"
            )
            # 续跑修复(真调用):宽松档修复者追加 PASS 收口(D-P3-14 特例)
            stop2, denier2, denied2 = _start_unattended_denier(session)
            recorder2 = _EventRecorder(session)
            try:
                with recorder2:
                    repaired = session.start_repair()
                    assert repaired is True, "start_repair 未受理(resumed 态应放行)"
                    if not _wait_first_event(recorder2, session, _FIRST_EVENT_WINDOW_SECONDS):
                        pytest.fail(
                            f"修复调用 {_FIRST_EVENT_WINDOW_SECONDS}s 内零事件"
                            f"(已驳回权限 {len(denied2)} 次;{recorder2.summary()};T-idi03-19)"
                        )
                    t1 = time.monotonic()
                    idle2, waited2 = wait_idle(session, _CHECK_DEADLINE_SECONDS)
                    elapsed += time.monotonic() - t1
                    if not idle2:
                        session.abort()
                        time.sleep(2)
                        pytest.fail(
                            f"修复调用有事件流但 {_CHECK_DEADLINE_SECONDS}s 内未收流"
                            f"(已等待 {waited2:.0f}s;已驳回权限 {len(denied2)} 次;"
                            f"{recorder2.summary()};T-idi03-19)"
                        )
            finally:
                stop2.set()
                denier2.join(timeout=3)
            # 宽松档:修复者在报告末追加 PASS 收口(D-P3-14)
            state_final = derive_state(project)
            assert state_final["state"] == "mission_complete", (
                f"宽松档修复续跑后应收口为 mission_complete,实际:{state_final['state']};"
                f"报告末行:{report_path.read_text(encoding='utf-8', errors='replace').strip().splitlines()[-1]!r}"
            )

    final = derive_state(project)
    assert final["state"] == "mission_complete", (
        f"最终态应为 mission_complete,实际:{final['state']}"
    )
    print(f"\n[核查链实测耗时] {elapsed:.1f}s(含自动修复跳)")
    session._reset_for_tests()
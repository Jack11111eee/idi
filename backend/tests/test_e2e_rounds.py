# -*- coding: utf-8 -*-
"""端到端真 CLI 用例(PLAN idi-02-04 Task 1):轮次收敛循环全链真验证。

两条 @pytest.mark.slow 用例,IDI_E2E 未设时 skip(常规跑不依赖真 AI):
  1. test_answer_plain_real_cli —— 大白话即时答真调用:
     mktemp 造盘 phase3 项目 → enter_project → answer_plain →
     断言返回 plain/answered/answer 非空、落盘条目字段齐全、耗时 < 60s
  2. test_process_round_real_cli —— 处理本轮批注真调用:
     同造盘模式 + 两条 pending comment 批注 → process_round → wait_idle
     (deadline 300s)→ 断言 discuss-round-2.md 完整轮(末行合规授权标记)、
     grammar.parse_annotation_responses 提取 id 含 a1-01、后端回写命中
     (a1-01 answered/answer 非空)、derive_state current_round == 2、
     上一轮 annotations items 只读保留。

路由覆盖度(诚实记录):真 E2E 只跑 config.ai_caller 当前配置的路线——
另一条路线(未配置者)的 ask_lite / process_run 从未被真调用,仅由
Wave 2 的同形单测承担契约一致性(本文件不冒充双路线均已真验)。
"""

import json
import os
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend import annotations as annotations_mod  # noqa: E402
from backend import session  # noqa: E402
from backend.grammar import parse_annotation_responses  # noqa: E402
from backend.state import derive_state, is_complete_round  # noqa: E402

pytestmark = pytest.mark.slow

# 真实调用时长门限:T-idi02-17(超时即 fail 并输出已等待时长)
_ANSWER_PLAIN_DEADLINE_SECONDS = 60  # §3.4「数秒内」的保守上限(实测值记 SUMMARY)
_FIRST_EVENT_WINDOW_SECONDS = 120  # 存活窗口(实测:本机重负载下 CLI 冷启动 >60s)
_ROUND_FINISH_DEADLINE_SECONDS = 420  # 首事件后总限(实测正常 127~310s,长尾余量)
_POLL_INTERVAL = 1.0

# 造盘:轮次文档正文里一句可引用的中文句子(划选对象)
_QUOTABLE_SENTENCE = "这一段是可以被划选的说明文字"
_ROUND1_BODY = (
    "# 第 1 轮讨论文档\n\n"
    "本项目的目标是把一次讨论变成一轮可核查的收敛。\n\n"
    f"{_QUOTABLE_SENTENCE}。它说明划词批注能绑定到精确原文。\n\n"
    "## 批注回应\n\n"
    "| 批注id | 原文摘录 | 回应 |\n"
    "|---|---|---|\n"
    "| a0-01 | 首轮无批注 | 首轮建盘无上轮批注 |\n\n"
    "## 覆盖维度表\n\n"
    "| 维度 | 状态 | 说明 |\n"
    "|---|---|---|\n"
    "| 目标对齐 | ✓ | 目标已写入文档 |\n"
    "| 边界 | ◐ | 边界仍有待决问题 |\n\n"
    "## 未决问题清单\n\n"
    "| 编号 | 问题 | 状态 |\n"
    "|---|---|---|\n"
    "| 1 | 目标是否足以指导实施 | 待决 |\n\n"
)


def _e2e_enabled() -> bool:
    return os.environ.get("IDI_E2E") == "1"


def _write_phase3_project(project: Path) -> None:
    """造盘一个 phase3 单轮项目:docs/discuss-round-1.md(末行合规授权标记)。"""
    docs = project / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "discuss-round-1.md").write_text(
        _ROUND1_BODY + "\n> 申请授权:否\n", encoding="utf-8"
    )


def _seed_pending_annotations(project: Path) -> None:
    """手写两条 pending comment 批注(§6.2 round schema,round=1)。

    id 按 aN-NN 方案(a1-01/a1-02);quote 取可引用句子的前半/全句;
    before 取空前缀(该句在该文档唯一,before 仅辅助)。
    """
    payload = {
        "round": 1,
        "items": [
            {
                "id": "a1-01",
                "quote": _QUOTABLE_SENTENCE,
                "before": "把一次讨论变成一轮可核查的收敛。",
                "type": "comment",
                "note": "这句话太抽象了,请解释它的实际含义。",
                "status": "pending",
                "answer": None,
                "created_at": "2026-09-09T00:00:00+00:00",
            },
            {
                "id": "a1-02",
                "quote": _QUOTABLE_SENTENCE[:8],
                "before": "收敛。",
                "type": "comment",
                "note": "「划选」和「批注」的关系再说明一下。",
                "status": "pending",
                "answer": None,
                "created_at": "2026-09-09T00:00:01+00:00",
            },
        ],
    }
    path = annotations_mod.annotations_path(project, 1)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def wait_idle(sess, timeout: float = 10.0) -> tuple[bool, float]:
    """等在飞调用结束(照 test_session.py 的 wait_idle 形态;返回诚实耗时)。

    返回 (是否空闲, 已等待秒数)——失败断言里输出真实等待时长,便于定位。
    """
    start = time.monotonic()
    deadline = start + timeout
    while sess.busy() and time.monotonic() < deadline:
        time.sleep(_POLL_INTERVAL)
    return (not sess.busy(), time.monotonic() - start)


class _EventRecorder:
    """记录 SSE 事件流(诊断 seam:包装 session._publish_for_tests)。

    E2E 失败时把事件 kind 概要带进断言消息——「写盘事件有没有出」
    「是否卡在权限确认」一眼可判,不盲猜挂死原因。
    """

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
        """事件流概要(kind 计数 + 最后 3 条 + 挂起权限数)。"""
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


def round2_path_probe(project: Path) -> bool:
    """挂死重试门卫:discuss-round-2.md 是否已在磁盘出现(纯只读探测)。"""
    return (project / "docs" / "discuss-round-2.md").is_file()


def test_answer_plain_real_cli(tmp_path):
    """E2E 1:大白话即时答真调用(秒级宽限 60s,落盘 plain 条目)。"""
    if not _e2e_enabled():
        pytest.skip("IDI_E2E 未设(常规跑不依赖真 AI)")

    project = tmp_path / "plain_project"
    project.mkdir()
    _write_phase3_project(project)

    session._reset_for_tests()
    snapshot = session.enter_project(project)
    assert snapshot["state"] == "phase3", (
        f"造盘后应推导为 phase3,实际:{snapshot['state']}"
    )
    assert snapshot["current_round"] == 1, (
        f"造盘后当前轮应为 1,实际:{snapshot['current_round']}"
    )

    t0 = time.monotonic()
    item = session.answer_plain(
        1,
        quote=_QUOTABLE_SENTENCE,
        before="把一次讨论变成一轮可核查的收敛。",
        question="这段讲什么?",
    )
    elapsed = time.monotonic() - t0

    # 秒级宽限:超时即失败(T-idi02-17;实测值记 SUMMARY)
    assert elapsed < _ANSWER_PLAIN_DEADLINE_SECONDS, (
        f"大白话即时答超时:耗时 {elapsed:.1f}s "
        f"(> {_ANSWER_PLAIN_DEADLINE_SECONDS}s 上限,§3.4 秒级要求未达)"
    )

    # 返回条目:type=plain、status=answered、answer 非空
    assert item["type"] == "plain", f"条目 type 应为 plain,实际:{item['type']}"
    assert item["status"] == "answered", (
        f"条目 status 应为 answered,实际:{item['status']}"
    )
    assert item["answer"] and item["answer"].strip(), (
        "大白话即时答为空(AI 调用失败或结果未返回)"
    )

    # 字段齐全:八字段(§6.2)
    for field in ("id", "quote", "before", "type", "note", "status", "answer", "created_at"):
        assert field in item, f"落盘条目缺字段 {field}(§6.2 八字段不全)"
    assert item["quote"] == _QUOTABLE_SENTENCE, (
        f"落盘 quote 与划选原文不一致:{item['quote']!r}"
    )

    # annotations.json 持久化:重新 load 后该条目在且形状一致
    persisted = annotations_mod.load(project, 1)
    ids = [it.get("id") for it in persisted["items"]]
    assert item["id"] in ids, (
        f"annotations.json 未持久化该 plain 条目(现有 id:{ids})"
    )
    stored = next(it for it in persisted["items"] if it["id"] == item["id"])
    assert stored["type"] == "plain", (
        f"持久化条目 type 应为 plain,实际:{stored['type']}"
    )
    assert stored["answer"] and stored["answer"].strip(), (
        "持久化条目的 answer 为空(落盘链路断裂)"
    )

    print(f"\n[answer_plain 实测耗时] {elapsed:.1f}s")
    session._reset_for_tests()


def test_process_round_real_cli(tmp_path):
    """E2E 2:处理本轮批注真调用——新轮产出 + 回应表回写 + 推导态前进。"""
    if not _e2e_enabled():
        pytest.skip("IDI_E2E 未设(常规跑不依赖真 AI)")

    # 挂死重试通过 importlib.reload(session) 重建模块(重启语义):
    # reload 重新绑定模块级名 session,声明为 global 使本函数读重绑后的值
    global session

    project = tmp_path / "rounds_project"
    project.mkdir()
    _write_phase3_project(project)
    _seed_pending_annotations(project)

    session._reset_for_tests()
    snapshot = session.enter_project(project)
    assert snapshot["state"] == "phase3", (
        f"造盘后应推导为 phase3,实际:{snapshot['state']}"
    )
    assert snapshot["current_round"] == 1, (
        f"造盘后当前轮应为 1,实际:{snapshot['current_round']}"
    )
    assert snapshot["pending_annotations"] == 2, (
        f"造盘后待处理批注应为 2 条,实际:{snapshot['pending_annotations']}"
    )

    # 真路线:不用 _set_caller_for_tests(配置工厂按 config.json 建 caller)
    # 无人值守权限处理:AI 若尝试项目外读取/命令(§5.4 → confirm),回环
    # 会无限等用户决定(产品语义正确——用户慢慢看),但无人值守 E2E 没有
    # 「用户」——用后台线程序贯 resolve_permission 全部驳回(保守拒绝,
    # §5.4 精神;写 docs/ 的关键路径按规则 3 直接 allow,不经此循环)。
    # AI 因此拿不到资料段之外的文件,只能按 prompt 内资料产出——这本身
    # 也是对「资料完备性」指令遵守度的真实检验。
    import threading

    stop_denier = threading.Event()
    denied: list[str] = []

    def _deny_permissions():
        while not stop_denier.is_set():
            pid = session._wait_for_pending_for_tests(timeout=1.0)
            if pid is not None:
                denied.append(str(pid))
                session.resolve_permission(pid, False)

    denier = threading.Thread(target=_deny_permissions, daemon=True)
    denier.start()

    recorder = _EventRecorder(session)
    try:
        # 首调 + 挂死重试一次(§7.3/D-P2-13 无状态重跑语义)。真机观测:
        # (a) CLI 子进程偶发启动即挂死(空闲窗口内零事件,连 say 都不出);
        # (b) 正常调用总耗时方差大(127s ~ 310s,模型端长尾)。
        # 挂死形态重试安全:挂死时新轮文档从未落盘,derive_state 仍指第
        # 1 轮,process_round 重调无副作用(与产品对用户的「重跑覆盖」
        # 承诺一致);重试门卫 = 零事件 + 磁盘无 round-2 + 推导态未前进。
        # 有事件流的慢调用不重试、不中断——按 420s 总限等它收流。
        _STALL_ATTEMPTS = 2
        t0 = time.monotonic()
        for attempt in range(1, _STALL_ATTEMPTS + 1):
            with recorder:
                accepted = session.process_round()
                assert accepted is True, (
                    "process_round 未受理(入口校验拒绝:非 phase3 或无完整轮)"
                )

                # 存活窗口:120s 内必须出首条事件(say/read/write/command
                # 任一)——否则判挂死。首条事件到达后转入 420s 总限收流等待。
                deadline = time.monotonic() + _FIRST_EVENT_WINDOW_SECONDS
                while not recorder.events and time.monotonic() < deadline:
                    if not session.busy():
                        break  # 调用已结束(异常路径):事件流概要会说明
                    time.sleep(_POLL_INTERVAL)

                if recorder.events:
                    idle, waited = wait_idle(
                        session, timeout=_ROUND_FINISH_DEADLINE_SECONDS
                    )
                    if idle:
                        break
                    session.abort()
                    time.sleep(2)
                    pytest.fail(
                        f"process_round 真调用第 {attempt} 次有事件流但 "
                        f"{_ROUND_FINISH_DEADLINE_SECONDS}s 内未收流"
                        f"(已等待 {waited:.0f}s;已驳回权限 {len(denied)} 次;"
                        f"{recorder.summary()};真机观测正常耗时 127~310s,"
                        f"超 420s 判 CLI 登录失效或挂死,T-idi02-17)"
                    )

                # 零事件:中止后按门卫判定是否可安全重试
                session.abort()
                time.sleep(2)
                state_mid = derive_state(project)
                disk_untouched = not round2_path_probe(project)
                retryable = (
                    disk_untouched
                    and state_mid["current_round"] == 1
                    and not session.busy()
                )
                if attempt < _STALL_ATTEMPTS and retryable:
                    # 退避:CLI 端在窗口枯竭期会连续拒连(真机观测:健康时段
                    # 4/4 全过,枯竭期连续零事件挂死)。等 90s 让配额窗口回填
                    # 再重试,比背靠背立刻再挂死更有效。
                    print(
                        f"\n[process_round 第 {attempt} 次调用零事件挂死"
                        f"(120s 无首个事件),退避 90s 后按 §7.3 无状态重跑语义重试]"
                    )
                    time.sleep(90)
                    # 重载模块 = 重启语义(照 test_e2e_smoke 的 restart-recovery
                    # 先例):清掉全部模块级状态(含 abort 后的 caller 与事件
                    # 链),再重进同一目录——文件即状态,D-19,重进零信息丢失。
                    import importlib

                    session = importlib.reload(session)
                    importlib.reload(annotations_mod)
                    session._reset_for_tests()
                    session.enter_project(project)
                    recorder = _EventRecorder(session)
                    continue
                pytest.fail(
                    f"process_round 第 {attempt} 次调用 "
                    f"{_FIRST_EVENT_WINDOW_SECONDS}s 内零事件(CLI 子进程启动即挂死;"
                    f"重试门卫:磁盘未触={disk_untouched},"
                    f"current_round={state_mid['current_round']},"
                    f"busy={session.busy()};已驳回权限 {len(denied)} 次;"
                    f"{recorder.summary()};T-idi02-17 真实发现)"
                )
        elapsed = time.monotonic() - t0
    finally:
        stop_denier.set()
        denier.join(timeout=3)

    # 断言 1:新轮文档存在且为完整轮(末行恰为合规授权标记)
    round2_path = project / "docs" / "discuss-round-2.md"
    new_doc_text = ""
    if round2_path.is_file():
        new_doc_text = round2_path.read_text(encoding="utf-8", errors="replace")
    if not new_doc_text.strip():
        # 诊断:列出 docs/ 实际文件(定位 AI 写到了哪里/是否漏写)
        docs_listing = sorted(
            p.name for p in (project / "docs").iterdir()
        )
        raise AssertionError(
            f"discuss-round-2.md 不存在或为空(docs/ 现有文件:{docs_listing};"
            f"AI 未按落盘指令写新轮文档)"
        )
    assert is_complete_round(new_doc_text), (
        "新轮文档末行不是合规授权标记(半成品轮:AI 产出不合规,真实发现)"
    )

    # 断言 2:文档含批注回应表文法,grammar 可解析且 id 含 a1-01
    responses = parse_annotation_responses(new_doc_text)
    response_ids = [r["id"] for r in responses]
    assert "a1-01" in response_ids, (
        f"新文档批注回应表未包含 a1-01(实际解析到的 id:{response_ids};"
        "AI 未逐条回应全部实质批注,prompt「逐条回应」指令未生效)"
    )

    # 断言 3:后端回写真实发生——a1-01 status=answered、answer 非空
    ann_after = annotations_mod.load(project, 1)
    items_after = {it["id"]: it for it in ann_after["items"]}
    assert "a1-01" in items_after, (
        "上一轮 annotations 条目丢失(items 只读保留被破坏,回写不应删条目)"
    )
    a101 = items_after["a1-01"]
    assert a101["status"] == "answered", (
        f"a1-01 未被回写为 answered(实际:{a101['status']};"
        "后端回写链路未命中——process_round 收流后未解析回应表回写)"
    )
    assert a101["answer"] and a101["answer"].strip(), (
        "a1-01 的 answer 为空(回写了 status 但答案为空,回写链路不完整)"
    )

    # 断言 4:a1-02 按回应表实际覆盖如实断言(不放宽)
    if "a1-02" in response_ids:
        assert items_after["a1-02"]["status"] == "answered", (
            "a1-02 在回应表中但未被回写为 answered(回写配对漏 id)"
        )
    else:
        # AI 若漏答 a1-02:按 PLAN 裁决记为真实发现,不放宽断言来隐藏
        raise AssertionError(
            f"AI 产物缺陷:回应表漏答实质批注 a1-02(解析到的 id:{response_ids};"
            "prompt 要求逐条回应全部实质批注——真实发现,按 failures 分支处理)"
        )

    # 断言 5:推导态前进 current_round == 2
    state = derive_state(project)
    assert state["state"] == "phase3", (
        f"处理后应仍为 phase3,实际:{state['state']}"
    )
    assert state["current_round"] == 2, (
        f"处理后 current_round 应前进到 2,实际:{state['current_round']}"
    )

    # 断言 6:上一轮 annotations items 只读保留(条目数不减少、id 不丢)
    ann_before_ids = {"a1-01", "a1-02"}
    assert ann_before_ids <= set(items_after), (
        f"上一轮批注条目丢失(现有:{sorted(items_after)};冻结语义:条目只读保留)"
    )

    print(f"\n[process_round 实测耗时] {elapsed:.1f}s")
    session._reset_for_tests()

# -*- coding: utf-8 -*-
"""annotations 存储(DESIGN.md §6.2 / D-18)单元测试:load / append_item / writeback / select_pending。

行为用例(全部手造磁盘形态,零 AI、零服务器):
  - 空形态:文件不存在与 JSON 脏文件都返回 {"round": N, "items": []}(D-P2-5)
  - 建条目:§6.2 八字段一字不差、id 递增 a1-01 → a1-02、跨轮 a3-01
  - plain 建条目即 answered(answer 即时写回)/ comment 落 pending
  - writeback:命中 id 回写 answer+status、未提及 id 保持 pending、返回命中数
  - select_pending:过滤 plain(仅 comment+pending)
测试样本全部手造(D-P2-19:不读本项目 docs/discuss-round-0~4)。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.annotations import (  # noqa: E402
    ANNOTATIONS_TEMPLATE,
    annotations_path,
    append_item,
    load,
    select_pending,
    writeback,
)

ITEM_KEYS = {"id", "quote", "before", "type", "note", "status", "answer", "created_at"}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


# ---------- 空形态(D-P2-5:文件不存在与文件损坏是两类不同输入,同一确定返回) ----------

def test_load_missing_file_returns_empty_shape(tmp_path):
    # 用例 1:不存在的 annotations 文件 → {"round": N, "items": []} 空形态(不抛)
    result = load(tmp_path, 3)
    assert result == {"round": 3, "items": []}


def test_load_corrupt_json_returns_empty_shape(tmp_path):
    # 用例 2:JSON 脏文件(手写坏 JSON)→ 同样空形态 + 不抛
    path = annotations_path(tmp_path, 2)
    write(path, "{这不是合法 JSON,,,")
    assert load(tmp_path, 2) == {"round": 2, "items": []}


def test_load_disk_round_value_does_not_override_param(tmp_path):
    # 边界:盘上 round 字段不可信时,返回的 round 以参数 N 为准
    path = annotations_path(tmp_path, 5)
    write(path, '{"round": 99, "items": [{"id": "a5-01"}]}')
    result = load(tmp_path, 5)
    assert result["round"] == 5
    assert len(result["items"]) == 1


def test_annotations_path_uses_template(tmp_path):
    # 文件名模板:project/docs/discuss-round-N.annotations.json(§6.1 字面)
    path = annotations_path(tmp_path, 3)
    assert path == tmp_path / "docs" / "discuss-round-3.annotations.json"
    assert path.name == ANNOTATIONS_TEMPLATE.format(n=3)


# ---------- 建条目(§6.2 八字段一字不差 + aN-NN id 方案) ----------

def test_append_item_first_entry_full_fields(tmp_path):
    # 用例 3:首条建条目 → id = "a1-01",落盘条目字段一字不差(八字段精确全等)
    entry = append_item(
        tmp_path, 1,
        quote="被划选的原文", before="前文第四十字符", type="comment",
        note="这里说得不清楚",
    )
    assert entry["id"] == "a1-01"
    assert set(entry.keys()) == ITEM_KEYS
    assert entry["status"] == "pending"
    assert entry["answer"] is None
    assert entry["quote"] == "被划选的原文"
    assert entry["before"] == "前文第四十字符"
    assert entry["type"] == "comment"
    assert entry["note"] == "这里说得不清楚"
    assert entry["created_at"]  # ISO-8601 非空

    # 落盘核对:顶层 round + items,条目字段集一致
    on_disk = load(tmp_path, 1)
    assert on_disk["round"] == 1
    assert len(on_disk["items"]) == 1
    assert set(on_disk["items"][0].keys()) == ITEM_KEYS


def test_append_item_ids_increment_same_round(tmp_path):
    # 用例 4:同轮第二条 → id = "a1-02"(aN-NN 递增)
    append_item(tmp_path, 1, quote="第一段", before="", type="comment", note="批注一")
    second = append_item(tmp_path, 1, quote="第二段", before="", type="comment", note="批注二")
    assert second["id"] == "a1-02"


def test_append_item_round_three_starts_a3_01(tmp_path):
    # 用例 5:round=3 首条 → id = "a3-01"(与 §6.2 示例同构)
    entry = append_item(tmp_path, 3, quote="某段原文", before="", type="comment", note="?")
    assert entry["id"] == "a3-01"


def test_append_item_plain_is_answered_immediately(tmp_path):
    # 用例 6:plain 建条目 → status 直接落 answered、answer 即时写回(D-P2-7)
    entry = append_item(
        tmp_path, 1,
        quote="看不懂的术语", before="", type="plain",
        note="用大白话讲讲", answer="这段是在说……",
    )
    assert entry["status"] == "answered"
    assert entry["answer"] == "这段是在说……"


def test_append_item_creates_docs_dir(tmp_path):
    # 父目录自举:docs/ 不存在时建条目也成功落盘
    assert not (tmp_path / "docs").exists()
    append_item(tmp_path, 2, quote="q", before="b", type="comment", note="n")
    assert annotations_path(tmp_path, 2).is_file()


def test_append_item_rejects_bad_type(tmp_path):
    # type 只接受 comment/plain,其它 ValueError(中文错误不校验文本,只校验抛)
    import pytest

    with pytest.raises(ValueError):
        append_item(tmp_path, 1, quote="q", before="b", type="urgent", note="n")


# ---------- 回写(D-P2-13:回写只认回应表中的 id) ----------

def test_writeback_hits_and_misses_mixed(tmp_path):
    # 用例 7:命中 a1-01 回写 answer+answered;未提及的 a1-02 保持 pending;返回命中数 1
    append_item(tmp_path, 1, quote="第一段", before="", type="comment", note="批注一")
    append_item(tmp_path, 1, quote="第二段", before="", type="comment", note="批注二")

    hits = writeback(tmp_path, 1, {"a1-01": "已按你的意见补充说明"})

    assert hits == 1
    after = load(tmp_path, 1)
    by_id = {item["id"]: item for item in after["items"]}
    assert by_id["a1-01"]["status"] == "answered"
    assert by_id["a1-01"]["answer"] == "已按你的意见补充说明"
    assert by_id["a1-02"]["status"] == "pending"  # 未提及的保持 pending
    assert by_id["a1-02"]["answer"] is None


def test_writeback_unknown_id_ignored(tmp_path):
    # 用例 8:传入不存在的 id → 忽略不抛,命中数不含它
    append_item(tmp_path, 1, quote="原文", before="", type="comment", note="n")
    hits = writeback(tmp_path, 1, {"a9-99": "不存在的 id"})
    assert hits == 0
    assert load(tmp_path, 1)["items"][0]["status"] == "pending"


def test_writeback_overwrite_answered_is_legal(tmp_path):
    # 覆盖语义:已 answered 的条目重写 answer 也合法
    append_item(tmp_path, 1, quote="原文", before="", type="comment", note="n")
    writeback(tmp_path, 1, {"a1-01": "第一次回应"})
    hits = writeback(tmp_path, 1, {"a1-01": "第二次回应(覆盖)"})
    assert hits == 1
    item = load(tmp_path, 1)["items"][0]
    assert item["answer"] == "第二次回应(覆盖)"
    assert item["status"] == "answered"


def test_writeback_empty_items_zero_hits(tmp_path):
    # 空 items:零命中、不写盘(读失败路径不走到写,T-idi02-02)
    hits = writeback(tmp_path, 1, {"a1-01": "没有条目"})
    assert hits == 0
    assert not annotations_path(tmp_path, 1).exists()


# ---------- select_pending(D-P2-15:plain 不计) ----------

def test_select_pending_filters_plain_and_answered(tmp_path):
    # 用例 9:comment+pending 被选出;plain(已 answered)与 answered comment 不选
    annotations = {
        "round": 1,
        "items": [
            {"id": "a1-01", "type": "comment", "status": "pending", "note": "n1"},
            {"id": "a1-02", "type": "plain", "status": "answered", "note": "n2"},
            {"id": "a1-03", "type": "comment", "status": "answered", "note": "n3"},
        ],
    }
    pending = select_pending(annotations)
    assert [item["id"] for item in pending] == ["a1-01"]


def test_select_pending_empty_shape():
    # 空形态入参 → 空列表(纯内存,无 IO)
    assert select_pending({"round": 1, "items": []}) == []

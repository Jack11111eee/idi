# -*- coding: utf-8 -*-
"""annotations.json 的读写纯函数——DESIGN.md §6.2 批注数据结构(D-18)。

存盘 JSON 字面即 §6.2 契约(不在本模块重定义字段模型——存盘是 DESIGN.md
字面契约,校验模型仅可用于 API 入口层,D-P2-5):顶层 {"round": N, "items": [...]},
条目八字段一字不差:id / quote / before / type / note / status / answer / created_at。

- id 方案 aN-NN:N = 轮次,NN = 该轮条目递增序号(与 §6.2 示例 "a3-01" 同构);
- 定位(locate_quote)靠精确文本匹配:quote + before 辅助,多匹配时优先
  "匹配点前文以 before 结尾"的那一处,仍不唯一取第一处;无匹配 None。
  轮次冻结(D-07/§3.5)保证被批注文本永不变化,无需模糊匹配(D-P2-6);
- 空形态兼容(D-P2-5):文件不存在 / JSON 脏文件都返回 {"round": N, "items": []}
  不抛不悬空——AI 写乱轮次文档时 annotations 不被连带污染;
- 字段写回职责(§6.2):建条目与回写全部走本模块(后端)。writeback 仅回写
  回应表中出现的 id(D-P2-13:回写只认表中 id,不依赖 AI 自觉),未在表中的
  id 保持 pending 不动。

零第三方依赖、纯 pathlib + json 无状态,不碰 Web 框架层与 AI 层。
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

logger = logging.getLogger(__name__)

# §6.1/§6.2 文件名字面:discuss-round-N.annotations.json(照 state.py 的 _ROUND_TEMPLATE 常量风格)
ANNOTATIONS_TEMPLATE = "discuss-round-{n}.annotations.json"

# 条目类型(§6.2):comment = 实质批注(进未决清单);plain = 大白话问答(即时答,不计清单 D-12)
TYPE_COMMENT = "comment"
TYPE_PLAIN = "plain"
_VALID_TYPES = (TYPE_COMMENT, TYPE_PLAIN)

# 条目状态(§6.2):comment 建条目落 pending;批量处理回写后 answered;plain 即时答直接 answered
STATUS_PENDING = "pending"
STATUS_ANSWERED = "answered"

# 落盘条目的字段全集(§6.2 八字段一字不差)
_ITEM_KEYS = {"id", "quote", "before", "type", "note", "status", "answer", "created_at"}


def annotations_path(project_path, round_n: int) -> Path:
    """返回第 round_n 轮 annotations 文件的完整路径:project/docs/discuss-round-N.annotations.json。"""
    return Path(project_path) / "docs" / ANNOTATIONS_TEMPLATE.format(n=round_n)


def load(project_path, round_n: int) -> dict:
    """读第 round_n 轮的 annotations;文件不存在或 JSON 损坏都返回空形态。

    空形态 = {"round": round_n, "items": []}(带轮号,§6.2 顶层结构)。
    JSONDecodeError / OSError 同样 warning + 空形态(照 transcript.py
    "读不到给确定判定"模式:两类失败同形态,不抛)。
    顶层 round 字段以参数 round_n 为准(盘上 round 不可信时也不覆写本判定)。
    """
    path = annotations_path(project_path, round_n)
    if not path.is_file():
        return {"round": round_n, "items": []}
    try:
        text = path.read_text(encoding="utf-8")
        obj = json.loads(text)
    except json.JSONDecodeError as exc:
        logger.warning("解析 %s 失败(JSON 脏文件),按空批注处理: %s", path, exc)
        return {"round": round_n, "items": []}
    except OSError as exc:  # 读不到(权限/竞态)→ 按空批注处理
        logger.warning("读取 %s 失败,按空批注处理: %s", path, exc)
        return {"round": round_n, "items": []}

    if not isinstance(obj, dict) or not isinstance(obj.get("items"), list):
        # 结构不符(如顶层不是对象 / items 不是数组)→ 同样给空形态,不抛
        logger.warning("%s 结构不符(顶层应为 {round, items}),按空批注处理", path)
        return {"round": round_n, "items": []}

    items = [item for item in obj["items"] if isinstance(item, dict)]
    return {"round": round_n, "items": items}


def append_item(
    project_path,
    round_n: int,
    *,
    quote: str,
    before: str,
    type: str,
    note: str,
    answer: str | None = None,
) -> dict:
    """向第 round_n 轮追加一条批注并落盘,返回新建条目 dict。

    - id = f"a{round_n}-{len(items)+1:02d}"(aN-NN 方案);
    - status:type=comment 落 "pending"(answer 为 None);type=plain 落
      "answered"(answer 由调用方传即时答文本,D-P2-7:plain 随建随写);
    - created_at = datetime.now(timezone.utc).isoformat();
    - 父目录自举:docs/ 不存在则 mkdir parents(照 transcript.py 先例);
    - json.dumps(obj, ensure_ascii=False, indent=2) 整体写盘(UTF-8)。
    type 仅接受 "comment"/"plain",其它抛 ValueError(中文错误消息)。
    """
    if type not in _VALID_TYPES:
        raise ValueError(f"type 必须是 {'/'.join(_VALID_TYPES)},收到: {type!r}")

    obj = load(project_path, round_n)
    items: list[dict] = obj["items"]
    new_id = f"a{round_n}-{len(items) + 1:02d}"
    entry = {
        "id": new_id,
        "quote": quote,
        "before": before,
        "type": type,
        "note": note,
        "status": STATUS_ANSWERED if type == TYPE_PLAIN else STATUS_PENDING,
        "answer": answer if type == TYPE_PLAIN else None,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    items.append(entry)

    path = annotations_path(project_path, round_n)
    # 父目录不存在则建(新轮第一条批注:防御性 mkdir,照 transcript.py 先例)
    parent = path.parent
    if not parent.is_dir():
        parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return entry


def writeback(project_path, round_n: int, answers: dict[str, str]) -> int:
    """按回应表批量回写条目(pending→answered 并填 answer),返回命中条数。

    回写以 id 配对为唯一依据(D-P2-13):仅回写 answers 中出现、且确实存在
    于 items 的条目(已 answered 的重写 answer 也合法,覆盖语义);未在
    answers 中出现的 id 一律不动(保持 pending)。answers 中不存在的 id
    忽略不抛(命中数不含)。空 items 时零命中;读失败路径(load 返回空形态)
    不会走到写,无覆盖损失面(T-idi02-02)。
    """
    obj = load(project_path, round_n)
    items: list[dict] = obj["items"]
    hits = 0
    for item in items:
        item_id = item.get("id")
        if item_id in answers:
            item["answer"] = answers[item_id]
            item["status"] = STATUS_ANSWERED
            hits += 1
    if hits:
        path = annotations_path(project_path, round_n)
        parent = path.parent
        if not parent.is_dir():
            parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return hits


def select_pending(annotations: dict) -> list[dict]:
    """纯内存过滤:type=comment 且 status=pending 的条目(无 IO)。

    session 层与前端计数共用此语义(D-P2-15):plain 不计(即时答不入清单 D-12)。
    """
    items = annotations.get("items") or []
    return [
        item
        for item in items
        if isinstance(item, dict)
        and item.get("type") == TYPE_COMMENT
        and item.get("status") == STATUS_PENDING
    ]


def locate_quote(full_text: str, quote: str, before: str) -> int | None:
    """在全文中定位 quote 的精确匹配起点(纯字符串函数,无 IO)。

    分支(D-P2-6 四分支 + 防呆):
    - quote 为空串 → None(空 quote 无语义);
    - 全文仅一处匹配 → 返回该匹配起点(首字符 index);
    - 多处匹配:优先取"匹配起点前文以 before 结尾"的那一处
      (起点前取 max(0, start-len(before)) 字切片比较);
    - 多处匹配且无一处前文以 before 结尾 → 取第一处;
    - 无匹配 → None(定位失败是合法返回,不是异常)。
    """
    if not quote:
        return None

    starts: list[int] = []
    pos = full_text.find(quote)
    while pos != -1:
        starts.append(pos)
        pos = full_text.find(quote, pos + 1)
    if not starts:
        return None
    if len(starts) == 1:
        return starts[0]

    # 多处匹配:before 辅助二次定位——找匹配点前文以 before 结尾的那一处
    if before:
        window = len(before)
        for start in starts:
            ctx_start = start - window
            if ctx_start < 0:
                ctx_start = 0
            if full_text[ctx_start:start] == before:
                return start
    return starts[0]

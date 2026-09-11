# -*- coding: utf-8 -*-
"""G3 授权纯函数(PLAN idi-03-01 Task 1 / FLOW-05 / DESIGN.md §4.4 / §7.4 / D-P3-1 / D-P3-4)。

G3 是「授权撰写总设计文档」门的纯函数层,两件事:
  1. g3_available(project_path):四处机械校验的组合判定——机械校验而非
     采信 AI 自评(D-17),四处任何一条不过即 False,不存在 AI 哄骗通道;
  2. authorize_write(project_path):确认词交互通过后,由后端(非 AI)在
     项目根写入 AUTHORIZATION.md(§5.4:AI 写入一律拒绝,无任何批准路径;
     它存在 = 用户确已授权——授权唯一凭证,§7.4 授权痕迹)。

g3_available 四查(§4.4 权威定义,四条在同一份当前轮文档快照上判定——
D-P3-1:读一次文档文本复用,不跨轮):
  ① 当前轮 annotations 无 status=pending 的 comment 条目(select_pending 空)
  ② 轮次文档未决清单清零(is_pending_list_clear)
  ③ 维度表全绿(is_dimension_table_green)
  ④ 授权申请标记为「是」(parse_auth_marker == "yes")
「当前轮」= derive_state 的 current_round(最大完整轮;半成品轮视为不
存在,D-P3-2/§7.3);derive_state 非 phase3 → 一律 False。

authorize_write 不重复四查(职责单一,组合判定在入口层):调用方
(Wave 2 路由)负责先 derive_state==phase3 + g3_available 后端再查
(D-P3-4 防绕过)后调用;AUTHORIZATION.md 已存在 → FileExistsError
(G3 只走一次,幂等防护照 g1.py 先例)。

零第三方依赖、纯 pathlib,不碰 FastAPI/AI 层。
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path

from backend import annotations as annotations_mod
from backend.grammar import (
    is_dimension_table_green,
    is_pending_list_clear,
    parse_auth_marker,
)
from backend.state import STATE_PHASE3, derive_state

logger = logging.getLogger(__name__)

# §7.4 行 3:授权痕迹文件名(项目根,不在 docs/ 下——§6.1 目录树)
AUTHORIZATION_FILENAME = "AUTHORIZATION.md"


def g3_available(project_path: Path) -> bool:
    """G3 四查组合判定:四处机械校验全部命中才 True(§4.4 权威定义)。

    机械校验而非采信 AI 自评(D-17):四处任何一条不过即 False;
    derive_state 非 phase3(或无完整轮)→ False。「当前轮」取 derive_state
    的 current_round(最大完整轮,半成品轮视为不存在,D-P3-2);四查在
    同一份当前轮文档快照上判定(D-P3-1:读一次文本复用,不跨轮):
      ① 当前轮 annotations 无 pending comment(select_pending 为空)
      ② 未决清单清零(is_pending_list_clear)
      ③ 维度表全绿(is_dimension_table_green)
      ④ 授权申请标记为「是」(parse_auth_marker == "yes")
    当前轮文档读不到(OSError/不存在)→ False(fail-closed:防御读失败
    即关闸,绝不因读不到而放行)。
    """
    project = Path(project_path)
    state = derive_state(project)
    if state["state"] != STATE_PHASE3 or state["current_round"] is None:
        return False

    round_n = state["current_round"]
    round_doc = project / "docs" / f"discuss-round-{round_n}.md"
    try:
        text = round_doc.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        # 文档在则轮完整(derive_state 已确认),读不到属防御性兜底:关闸
        logger.warning("读取当前轮文档 %s 失败,G3 判定 fail-closed: %s", round_doc, exc)
        return False

    # ①:当前轮 annotations 无 pending comment(四查复用既有解析器,
    # 不重新实现第二套——D-P3-1 铁律)
    if annotations_mod.select_pending(annotations_mod.load(project, round_n)):
        return False
    # ②:未决清单清零
    if not is_pending_list_clear(text):
        return False
    # ③:维度表全绿
    if not is_dimension_table_green(text):
        return False
    # ④:授权申请标记为「是」
    return parse_auth_marker(text) == "yes"


def authorize_write(project_path: Path) -> Path:
    """确认词通过后由后端写入项目根 AUTHORIZATION.md,返回文件路径(§7.4)。

    授权痕迹两要素(§7.4 授权痕迹段):授权时间(ISO-8601,UTC)+
    操作者确认词标记行(含「确认授权」)——后端生成明文 UTF-8,非 AI
    (§5.4:AI 写入一律拒绝)。AUTHORIZATION.md 已存在 → FileExistsError
    (G3 只走一次,幂等防护照 g1.py 先例;重开已授权项目按 §7.4 行 4
    显示「继续撰写」而非重新授权)。
    本函数不重复四查(职责单一):调用方(Wave 2 路由)负责先
    derive_state==phase3 + g3_available 再查后调用(D-P3-4 防绕过)。
    项目目录必已存在(enter 前置),不加 mkdir。
    """
    project = Path(project_path)
    auth_path = project / AUTHORIZATION_FILENAME
    if auth_path.is_file():
        raise FileExistsError(
            f"已授权({AUTHORIZATION_FILENAME} 已存在)——G3 只走一次,"
            "重开已授权项目按 §7.4 行 4 显示「继续撰写」"
        )

    authorized_at = datetime.now(timezone.utc).isoformat()
    content = (
        "# 授权记录\n\n"
        f"- 授权时间:{authorized_at}\n"
        "- 操作者确认词:确认授权\n"
        "- 说明:用户在 G3 门输入确认词「确认授权」,由后端写入本文件"
        "(AI 不可写,§5.4)。\n"
    )
    auth_path.write_text(content, encoding="utf-8")
    logger.info("G3 授权落盘:%s", auth_path)
    return auth_path

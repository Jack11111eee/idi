# -*- coding: utf-8 -*-
"""G1 定稿纯函数(PLAN idi-01-04 Task 2 / FLOW-03 / DESIGN.md §4.4 / D-P1-12)。

G1 是后端动作,不涉及 AI:把 docs/draft.md 定稿为 docs/discuss-round-1.md,
并在文档末尾追加合规的 `> 申请授权:否` 标记行(§6.4 文法:strip 后全等)。

规则:
  - draft.md 不存在 → FileNotFoundError(先有雏形才能定稿)
  - discuss-round-1.md 已存在 → FileExistsError(G1 只走一次,幂等防护;
    重开即 phase3,重入合法路径不存在)
  - draft 全文 rstrip 尾部空白后接换行 + 标记行 + 换行——保证「最后一个非空行」
    语义成立(draft 尾部多余空白不破坏标记)
  - draft.md 不删不改(§4.4:草稿保留)

零第三方依赖、纯 pathlib,不碰 FastAPI/AI 层。
"""
from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

DRAFT_FILENAME = "docs/draft.md"
ROUND_1_FILENAME = "docs/discuss-round-1.md"

# §6.4 授权申请标记(与 state.AUTH_MARKER_NO 同一字符串;独立常量防 import 环)
AUTH_MARKER_NO = "> 申请授权:否"


def finalize_g1(project_path: Path) -> Path:
    """将当前 draft.md 定稿为 discuss-round-1.md(后端追加授权标记行),返回新文件路径。"""
    project = Path(project_path)
    draft_path = project / DRAFT_FILENAME
    round_path = project / ROUND_1_FILENAME

    if not draft_path.is_file():
        raise FileNotFoundError(f"尚无雏形草稿({DRAFT_FILENAME})——先在阶段 1-2 讨论出雏形再认可")

    if round_path.is_file():
        raise FileExistsError(
            f"已定稿({ROUND_1_FILENAME} 已存在)——G1 只走一次,项目已在轮次阶段"
        )

    draft_text = draft_path.read_text(encoding="utf-8", errors="replace")
    # draft 全文(尾部空白 rstrip)换行接标记行换行:标记行是最后的非空行
    finalized = f"{draft_text.rstrip()}\n\n{AUTH_MARKER_NO}\n"

    round_path.parent.mkdir(parents=True, exist_ok=True)  # docs/ 理论上已存在(draft 在其中),防御
    round_path.write_text(finalized, encoding="utf-8")
    logger.info("G1 定稿完成:%s(draft.md 保留)", round_path)
    return round_path

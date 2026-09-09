# -*- coding: utf-8 -*-
"""阶段 1-2 系统提示词模板(DESIGN.md §5.1 无状态 + §3.8 语言红线)。

build_phase12_prompt(project_path, user_message) -> str:
拼装发给 AI 的完整调用载荷——每次调用 = 全新无头,启动自磁盘读 docs/ 全部文档(§5.1),
所有记忆都在文档里;本模块只负责"把磁盘现状读出来拼进提示词",自己不维护任何状态。

四段结构(PLAN idi-01-03 Task 1):
  一、系统段:角色(项目开工前的讨论搭档)+ §3.8 语言红线原文要义
  二、资料段:docs/ 下各文档(transcript.md 历史、draft.md 现状、brainstorm.md 若存在),
              以文件名标题 + 全文注入;docs/ 不存在或为空时说明「这是全新讨论」
  三、任务段:用户本次消息 + 阶段 1-2 会话指令(目标对齐需求与雏形,持续演进 docs/draft.md,
              草稿格式自由,有实质进展时应更新草稿文件)
"""

from __future__ import annotations

from pathlib import Path

# §3.8 语言红线原文要义(注入每个阶段的 prompt)
_LANGUAGE_RULES = (
    "语言红线:输出必须简洁、精准,不用晦涩词语。但解释必须清晰、完整——简洁不等于省略,"
    "不许因追求简短而含糊带过。未定义的术语不用;必须用术语时,先用一句大白话定义。"
    "一次讲一个小点,讲透。面向单人开发者读者,讨论文档以中文为主。"
)

# docs/ 下会注入 prompt 的固定文档(存在才注入;其余文件名不进载荷)
_KNOWN_DOCS = ("transcript.md", "draft.md", "brainstorm.md")

# 阶段 1-2 会话指令(任务段常量)
_PHASE12_INSTRUCTIONS = (
    "会话指令:当前处于阶段 1-2(需求与雏形对齐)。你的目标是和用户对齐需求、共同打磨雏形;"
    "讨论产出会持续演进 docs/draft.md 草稿——草稿格式自由,不必遵循任何模板,"
    "但每次有实质进展时应更新草稿文件(用 Write 工具写 docs/draft.md)。"
    "本阶段不讨论实现细节与代码,聚焦「要什么、为什么」。"
)


def build_phase12_prompt(project_path, user_message: str) -> str:
    """拼装阶段 1-2 的完整调用提示词(§5.1:磁盘现状 + 本次消息,四段结构)。"""
    project = Path(project_path)
    docs_dir = project / "docs"

    # ---- 资料段:docs/ 下已知文档逐个注入(文件名标题 + 全文) ----
    doc_sections: list[str] = []
    for name in _KNOWN_DOCS:
        path = docs_dir / name
        if path.is_file():
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                text = ""
            if not text.strip() and name != "transcript.md":
                # 空草稿也注入标题(状态可见),但空转录跳过
                doc_sections.append(f"### 文件:docs/{name}\n\n(文件为空)")
                continue
            body = f"### 文件:docs/{name}\n\n{text}" if text.strip() else None
            if body:
                doc_sections.append(body)
        else:
            if name in ("draft.md", "brainstorm.md"):
                # 不存在的草稿也登记状态(AI 知道还没写)
                doc_sections.append(f"### 文件:docs/{name}\n\n(尚不存在)")

    if doc_sections:
        # docs/ 有内容但讨论尚未有转录 → 仍是新讨论的延续形态;无任何转录时说明全新
        has_transcript = (docs_dir / "transcript.md").is_file() and any(
            "transcript.md" in s for s in doc_sections
        )
        material = "\n\n".join(doc_sections)
        material_note = (
            "以下是项目 docs/ 目录的当前文档(你的全部记忆来源):"
            if has_transcript
            else "这是全新讨论,尚无会话转录;以下为项目现有文档:"
        )
    else:
        material = "(docs/ 目录为空或不存在)"
        material_note = "这是全新讨论,尚无任何文档:"

    return (
        "## 一、你的角色\n\n"
        "你是本工具的 AI 讨论引擎,是用户在项目开工前的讨论搭档。"
        "和用户一起把想法打磨成需求与雏形,不是替用户决定。\n"
        f"{_LANGUAGE_RULES}\n\n"
        "## 二、项目资料\n\n"
        f"{material_note}\n\n"
        f"{material}\n\n"
        "## 三、本次任务\n\n"
        f"{_PHASE12_INSTRUCTIONS}\n\n"
        "## 四、用户消息\n\n"
        f"{user_message}\n"
    )

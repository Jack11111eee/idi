# -*- coding: utf-8 -*-
"""讨论流程各阶段的系统提示词模板(DESIGN.md §5.1 无状态 + §3.8 语言红线)。

build_phase12_prompt(project_path, user_message) -> str:
拼装发给 AI 的完整调用载荷——每次调用 = 全新无头,启动自磁盘读 docs/ 全部文档(§5.1),
所有记忆都在文档里;本模块只负责"把磁盘现状读出来拼进提示词",自己不维护任何状态。

build_plain_prompt(document_text, quoted_text, question) -> str(§3.4 D-05):
大白话轻量调用——仅携带当前文档 + 划选原文,不读全量 docs/(秒级响应,D-P2-8)。

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

# §3.7 发散模式固定视角清单(D-16 四条之「模板要点」①;清单写死在模板)
_DIVERGENCE_PERSPECTIVES = (
    "- 解决谁的什么痛点",
    "- 最省事的版本",
    "- 最贵的版本",
    "- 没人做但该有人做的",
)


def build_divergence_prompt(project_path) -> str:
    """拼装发散模式专用提示词(§3.7 D-16;跑在同一 AICaller 链路,本函数只组装)。

    四段结构:
      一、系统段:角色(发散引擎)+ §3.8 语言红线
      二、现况段:项目目录现状、既有 docs/brainstorm.md 全文(再次发散看得见上轮候选)
      三、任务段:三步走——① 多视角风暴(固定视角各出 2~3 个方向,鼓励离谱);
         ② 收敛——汇成 3~5 个候选方向,每个含一句话说明+一句为什么值得做;
         ③ 引导用户挑选或委托 AI 挑选
      四、落盘指令:风暴与候选全文写入 docs/brainstorm.md,整体覆盖旧文件
    """
    project = Path(project_path)
    docs_dir = project / "docs"

    # ---- 现况段:既有 brainstorm.md 全文注入(不存在则说明全新发散) ----
    brainstorm_path = docs_dir / "brainstorm.md"
    if brainstorm_path.is_file():
        try:
            existing = brainstorm_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            existing = ""
        current_section = (
            "以下是 docs/brainstorm.md 的当前内容(上一轮发散的候选,"
            "本次发散可以推翻、重组、深化它们):\n\n"
            f"{existing}"
            if existing.strip()
            else "docs/brainstorm.md 存在但为空——本次发散从空白开始。"
        )
    else:
        current_section = (
            "项目尚无任何发散记录(docs/brainstorm.md 不存在)——本次发散从空白开始。"
        )

    perspectives = "\n".join(_DIVERGENCE_PERSPECTIVES)

    return (
        "## 一、你的角色\n\n"
        "你是本工具的 AI 发散引擎。用户现在没有明确想法,你的任务是多视角头脑风暴,"
        "给出值得做的候选方向,让用户能挑一个往下走。\n"
        f"{_LANGUAGE_RULES}\n\n"
        "## 二、项目现况\n\n"
        f"{current_section}\n\n"
        "## 三、发散任务(三步走)\n\n"
        "**第一步:多视角风暴。**从下列固定视角出发,每个视角各出 2~3 个方向。"
        "鼓励离谱——风暴阶段不设可行性门槛,怪点子里常有真价值:\n\n"
        f"{perspectives}\n\n"
        "**第二步:收敛。**把风暴结果汇成 3~5 个候选方向。每个候选必须包含:"
        "一句话说明(它是什么)+ 一句为什么值得做(为什么有人需要它)。\n\n"
        "**第三步:引导挑选。**把候选方向清楚呈现在回复里,引导用户挑选一个方向,"
        "或者明确委托你来挑(用户说「你挑吧」即由你选定并说明理由)。\n\n"
        "## 四、落盘指令\n\n"
        "用 Write 工具把风暴过程与候选方向全文写入 `docs/brainstorm.md`,"
        "**整体覆盖**旧文件(它是不编号、不冻结的发散草稿,可反复覆盖)。"
        "不要创建其他编号变体文件。\n"
    )


# 大白话解释器角色指令(§3.4 D-05/D-P2-9:只解释,不改设计)
_PLAIN_ROLE = (
    "大白话解释是消歧不是新决定:你只负责把划选原文讲明白,"
    "不提出设计修改、不更新任何文档、不开新讨论线。"
)


def build_plain_prompt(document_text: str, quoted_text: str, question: str) -> str:
    """拼装大白话轻量调用的提示词(§3.4 D-05 / D-P2-8 / D-P2-9)。

    三段结构(轻量调用不走四段资源段——仅携带当前文档 + 划选原文,秒级响应):
      一、角色段:大白话解释器 + §3.8 语言红线 + 「只解释,不改设计」
      二、资料段:当前文档全文 + 划选原文两块
         (显式告知 AI 仅此两块资料,不读其他文件、不使用任何工具)
      三、任务段:用大白话解释用户关于划选原文的问题
    """
    return (
        "## 一、你的角色\n\n"
        "你是大白话解释器:用户在阅读讨论文档时对某段原文有疑问,"
        "你用平实的语言把它讲明白。\n"
        f"{_LANGUAGE_RULES}\n"
        f"{_PLAIN_ROLE}\n\n"
        "## 二、资料(仅此两块)\n\n"
        "### 当前文档全文\n\n"
        f"{document_text}\n\n"
        "### 划选原文\n\n"
        f"{quoted_text}\n\n"
        "以上是全部资料:不要读取其他文件,不要使用任何工具——"
        "这是一次纯问答,解释完即结束。\n\n"
        "## 三、本次问题\n\n"
        f"{question}\n"
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

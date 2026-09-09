# -*- coding: utf-8 -*-
"""讨论流程各阶段的系统提示词模板(DESIGN.md §5.1 无状态 + §3.8 语言红线)。

build_phase12_prompt(project_path, user_message) -> str:
拼装发给 AI 的完整调用载荷——每次调用 = 全新无头,启动自磁盘读 docs/ 全部文档(§5.1),
所有记忆都在文档里;本模块只负责"把磁盘现状读出来拼进提示词",自己不维护任何状态。

build_plain_prompt(document_text, quoted_text, question) -> str(§3.4 D-05):
大白话轻量调用——仅携带当前文档 + 划选原文,不读全量 docs/(秒级响应,D-P2-8)。

build_round_prompt(project_path, current_round) -> str(G2 / §4.4 / D-P2-11):
「处理本轮批注」的服务端提示词——资料段读全量 docs/(当前轮文档全文 +
当前轮 annotations 逐条 + transcript/draft),任务段注入 §3.3 四步 +
§6.3 五件套 + §6.4 文法模板逐字。

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


# §3.4 大白话解释器角色指令(D-05/D-P2-9:只解释,不改设计)
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


# ---------------------------------------------------------------------------
# 轮次收敛(G2「处理本轮批注」,PLAN idi-02-02 Task 2,D-P2-11/D-P2-18)
# ---------------------------------------------------------------------------

# 轮次文档文件名模板(§6.1;与 state._ROUND_TEMPLATE 同一字面)
_ROUND_TEMPLATE = "discuss-round-{n}.md"

# §6.3/§6.4 文法模板正例(逐字贴入 prompt——工具按此解析,改列名即解析失败)
_GRAMMAR_EXAMPLES = (
    "批注回应表(二级标题含「批注回应」,表格列头逐字如下):",
    "",
    "| 批注id | 原文摘录 | 回应 |",
    "|---|---|---|",
    "",
    "维度表(二级标题含「覆盖维度表」,表格列头逐字如下,状态仅 ✓ ◐ ✗):",
    "",
    "| 维度 | 状态 | 说明 |",
    "|---|---|---|",
    "",
    "未决清单(二级标题含「未决问题清单」,表格列头逐字如下,状态仅 待决/已决):",
    "",
    "| 编号 | 问题 | 状态 |",
    "|---|---|---|",
    "",
    "授权申请标记(文档最后一个非空行,恰为以下两串之一):",
    "",
    "> 申请授权:是",
    "> 申请授权:否",
    "",
    "切勿改列名、切勿改标记行格式——工具按此逐字解析,改动即解析失败。",
)

# 任务段常量(§3.3 四步 + §6.3 五件套 + §6.4 逐字模板 + 落盘指令;D-P2-11/D-P2-18)
_ROUND_INSTRUCTIONS = (
    "任务:处理本轮批注,产出下一轮轮次文档。四步走(§3.3 原文):\n"
    "1. 逐条回应上轮全部实质批注(批注逐条见下方资料段;大白话请求在产生时"
    "已即时回答,不进入本轮);\n"
    "2. 更新文档(本轮版次),已定决策标注「已对齐」;\n"
    "3. 追问新的更深层细节问题,进入清单;\n"
    "4. 文末公开当前未决清单。\n"
    "每轮文档必须全部包含五件套(§6.3):批注回应表、决策登记、覆盖维度表、"
    "未决问题清单、文末授权申请标记——缺一不可。\n"
    "收敛判据(满足才写「是」):上轮批注已全部被回应 + 未决清单清零 + "
    "覆盖维度表全绿;未满足写「否」并开启下一轮。\n"
    "批注回应表的批注id 必须与资料段中列出的上一轮批注 id 一一对应,"
    "每条实质批注都要有一行回应。\n"
    "资料完备性:下方「二、项目资料」已包含完成本任务所需的全部材料"
    "(当前轮文档全文 + 当前轮批注逐条 + 历史文档)——直接依据资料作答,"
    "不要读取资料段之外的任何文件,不要访问项目目录之外的任何路径。"
    "若认为资料不足,按现有资料尽力产出,并在文档中说明局限。\n"
    "结果落盘:用 Write 工具产出 {target_filename}(按 Markdown 全文整体写入,"
    "不要写其他文件)。批注记录(annotations 文件)由本工具后端管理,"
    "你不要写、不要改。\n"
    "写完后在回复里简述本轮改动。"
)


def build_round_prompt(project_path, current_round: int) -> str:
    """拼装 G2「处理本轮批注」的服务端提示词(D-P2-11/D-P2-18)。

    四段结构(照 build_phase12_prompt 骨架,资料段读全量 docs/,§5.1):
      一、系统段:角色(轮次收敛引擎)+ §3.8 语言红线
      二、资料段:当前轮文档全文(含半成品原文——重跑场景照读)+
                 当前轮全部 annotations 逐条(id/quote/note,无批注时显式说明
                 「当前轮暂无待处理批注」)+ transcript/draft/brainstorm 照
                 _KNOWN_DOCS 既有循环注入
      三、任务段:_ROUND_INSTRUCTIONS(§3.3 四步 + §6.3 五件套 +
                 §6.4 文法模板逐字 + 落盘指令)
      四、文法模板:_GRAMMAR_EXAMPLES 逐字贴入(表头行/标记行正例 +
                 切勿改列名硬指令)
    """
    project = Path(project_path)
    docs_dir = project / "docs"
    from backend import annotations as annotations_mod  # 延迟导入防环

    target_round = current_round + 1
    current_doc_name = _ROUND_TEMPLATE.format(n=current_round)
    target_filename = f"docs/{_ROUND_TEMPLATE.format(n=target_round)}"

    # ---- 资料段①:当前轮文档全文(半成品原文照读——重跑覆盖场景) ----
    current_doc_path = docs_dir / current_doc_name
    if current_doc_path.is_file():
        try:
            current_doc_text = current_doc_path.read_text(
                encoding="utf-8", errors="replace"
            )
        except OSError:
            current_doc_text = ""
        current_doc_section = (
            f"### 当前轮文档:docs/{current_doc_name}(全文)\n\n{current_doc_text}"
            if current_doc_text.strip()
            else f"### 当前轮文档:docs/{current_doc_name}\n\n(文件为空)"
        )
    else:
        current_doc_section = (
            f"### 当前轮文档:docs/{current_doc_name}\n\n(尚不存在)"
        )

    # ---- 资料段②:当前轮全部 annotations 逐条(id/quote/note) ----
    ann = annotations_mod.load(project, current_round)
    items = ann.get("items") or []
    if items:
        anno_lines = []
        for item in items:
            anno_lines.append(
                f"- id: {item.get('id', '')} | 原文摘录: {item.get('quote', '')} "
                f"| 用户批注: {item.get('note', '')} | 类型: {item.get('type', '')}"
            )
        annotations_section = (
            f"### 当前轮批注(discuss-round-{current_round}.annotations.json,"
            f"逐条;type=plain 的已即时回答,只需回应 type=comment 的实质批注)\n\n"
            + "\n".join(anno_lines)
        )
    else:
        annotations_section = "### 当前轮批注\n\n当前轮暂无待处理批注。"

    # ---- 资料段③:transcript / draft / brainstorm(_KNOWN_DOCS 既有形态) ----
    doc_sections: list[str] = []
    for name in _KNOWN_DOCS:
        path = docs_dir / name
        if path.is_file():
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                text = ""
            if text.strip():
                doc_sections.append(f"### 文件:docs/{name}\n\n{text}")
        else:
            if name in ("draft.md", "brainstorm.md"):
                doc_sections.append(f"### 文件:docs/{name}\n\n(尚不存在)")
    known_docs_section = (
        "\n\n".join(doc_sections) if doc_sections else "(无其他文档)"
    )

    grammar_examples = "\n".join(_GRAMMAR_EXAMPLES)
    instructions = _ROUND_INSTRUCTIONS.replace("{target_filename}", target_filename)

    return (
        "## 一、你的角色\n\n"
        "你是本工具的轮次收敛引擎。用户已对当前轮文档写好批注,"
        "你的任务是逐条回应这些批注并产出下一轮文档。\n"
        f"{_LANGUAGE_RULES}\n\n"
        "## 二、项目资料(docs/ 全量,§5.1)\n\n"
        f"{current_doc_section}\n\n"
        f"{annotations_section}\n\n"
        f"{known_docs_section}\n\n"
        "## 三、本次任务\n\n"
        f"{instructions}\n\n"
        "## 四、文法模板(逐字遵守,§6.4)\n\n"
        f"{grammar_examples}\n"
    )

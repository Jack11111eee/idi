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

build_writing_prompt(project_path) -> str(阶段 4 撰写 / §7.4 行 4 / D-P3-7):
「撰写总设计文档」的服务端提示词——资料段读全部完整轮文档 + 各轮批注
+ transcript/draft/brainstorm(绝不读 DESIGN.md.tmp / AUTHORIZATION.md,
D-P3-9),任务段注入七维度覆盖 + DESIGN.md.tmp 落盘指令与明禁。

build_check_prompt(project_path, check_n, tier) -> str(阶段 5 核查 / §8.2 /
D-P3-13 / D-P3-15):「干净的眼睛」核查提示词——资料段 = DESIGN.md 全文 +
全部轮次文档 + 全部批注 + 已有全部 DESIGN-check 报告;问题分级表头与
结论行文法逐字注入(解析器两端一字不差,D-P3-29),绝不修改 DESIGN.md。

build_repair_prompt(project_path, check_n, tier) -> str(阶段 5 修复 / §8.2 /
D-P3-14):修复者提示词——资料段 = DESIGN.md + 最新报告全文(含裁决行)
+ 其他报告;任务段 = 按裁决逐条修复、写 DESIGN.md.tmp、用户职权问题发
`> 待裁决:#K:` 停下、宽松档在报告末追加 PASS。

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


# ---------------------------------------------------------------------------
# 阶段 4 撰写(G3 授权后,PLAN idi-03-02 Task 1 / FLOW-05 / DATA-02 /
# §7.3① / §7.4 行 4 / D-P3-7 / D-P3-9)
# ---------------------------------------------------------------------------

# 撰写任务段落盘指令常量(照 _ROUND_INSTRUCTIONS 元组风格,D-P3-7)
_WRITING_INSTRUCTIONS = (
    "任务:产出一份无歧义的总设计文档。要求:\n"
    "1. 覆盖上一份轮次文档中覆盖维度表的全部七个维度内容;\n"
    "2. 吸收全部轮次的决策登记与已对齐结论(「已对齐」的决策照录为正式决策);\n"
    "3. 不含未决问题——授权已通过,未决清单应已清零;若你认为仍有歧义,"
    "选择最贴合已对齐结论的表述并继续,不把问题带进总设计文档。\n"
    "资料完备性:上方「二、项目资料」已包含完成本任务所需的全部材料"
    "(全部完整轮文档 + 全部批注 + 历史文档)——直接依据资料作答,"
    "不要读取资料段之外的任何文件,不要访问项目目录之外的任何路径。\n"
    "落盘指令:用 Write 工具把总设计文档全文写入 DESIGN.md.tmp"
    "(项目根,按 Markdown 全文整体覆盖式写入)后即结束,不要写其他文件。\n"
    "**绝不直接写 DESIGN.md 或 AUTHORIZATION.md——权限门将拒绝这两项写入。**"
    "DESIGN.md.tmp 是 DESIGN.md 唯一合法的落盘路径(暂存名):后端会在你"
    "完成后原子改名为 DESIGN.md。写完后在回复里简述文档结构。"
)


def build_writing_prompt(project_path) -> str:
    """拼装「撰写总设计文档」的服务端提示词(D-P3-7 / D-P3-9)。

    四段结构(照 build_round_prompt 同族):
      一、系统段:角色(总设计文档撰写引擎)+ §3.8 语言红线
      二、资料段:全部完整轮文档全文(list_complete_rounds 循环)+ 各轮
                 annotations 逐条(id/quote/note)+ transcript/draft/
                 brainstorm 照 _KNOWN_DOCS 既有循环注入
                 **绝不读 DESIGN.md.tmp 与 AUTHORIZATION.md**(D-P3-9:
                 半份 tmp 是被覆盖物,不入资料不参考;授权凭证与撰写无关)
      三、任务段:_WRITING_INSTRUCTIONS(七维度覆盖 + 吸收决策 + 不含
                 未决问题 + DESIGN.md.tmp 落盘指令与明禁)
    """
    project = Path(project_path)
    docs_dir = project / "docs"
    from backend import annotations as annotations_mod  # 延迟导入防环
    from backend.state import list_complete_rounds

    # ---- 资料段①:全部完整轮文档全文 ----
    round_numbers = list_complete_rounds(docs_dir)
    round_sections: list[str] = []
    if round_numbers:
        for n in round_numbers:
            round_path = docs_dir / f"discuss-round-{n}.md"
            try:
                text = round_path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                text = ""
            round_sections.append(
                f"### 轮次文档:docs/discuss-round-{n}.md(全文)\n\n{text}"
            )
        rounds_section = "\n\n".join(round_sections)
    else:
        rounds_section = "(无完整轮次文档)"

    # ---- 资料段②:各轮 annotations 逐条(id/quote/note) ----
    anno_lines: list[str] = []
    for n in round_numbers:
        ann = annotations_mod.load(project, n)
        for item in ann.get("items") or []:
            anno_lines.append(
                f"- 轮 {n} | id: {item.get('id', '')} | 原文摘录: "
                f"{item.get('quote', '')} | 用户批注: {item.get('note', '')}"
                f" | 类型: {item.get('type', '')}"
            )
    if anno_lines:
        annotations_section = (
            "### 各轮批注(discuss-round-*.annotations.json,逐条;"
            "type=plain 是大白话问答,type=comment 是实质批注——两类的"
            "用户原话都吸收进总设计文档)\n\n" + "\n".join(anno_lines)
        )
    else:
        annotations_section = "### 各轮批注\n\n全部轮次均无批注记录。"

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

    return (
        "## 一、你的角色\n\n"
        "你是本工具的总设计文档撰写引擎。用户已在 G3 门明确授权撰写总设计文档,"
        "你的任务是把整段讨论的收敛成果写成一份无歧义的总设计文档。\n"
        f"{_LANGUAGE_RULES}\n\n"
        "## 二、项目资料(docs/ 全量,§5.1)\n\n"
        f"{rounds_section}\n\n"
        f"{annotations_section}\n\n"
        f"{known_docs_section}\n\n"
        "## 三、本次任务\n\n"
        f"{_WRITING_INSTRUCTIONS}\n"
    )


# ---------------------------------------------------------------------------
# 阶段 5 自检两角色(PLAN idi-03-02 Task 2 / DATA-04 / §8.2 全节 /
# D-P3-13 / D-P3-14 / D-P3-15 / D-P3-29)
# ---------------------------------------------------------------------------

# 报告文法模板正例(逐字贴入 prompt——grammar.py 解析器按此逐字解析,
# 两端一字不差是 D-P3-29 硬要求;照 _GRAMMAR_EXAMPLES 元组形态)
_CHECK_GRAMMAR_EXAMPLES = (
    "报告文法(逐字遵守,工具按此解析):",
    "",
    "报告首行为档位头部行(恰为以下两串之一,「档位」由任务方给定):",
    "",
    "> 自检档位:严格",
    "> 自检档位:宽松",
    "",
    "问题分级表(二级标题含「问题分级」,表格列头逐字如下,级别仅 P0/P1/P2):",
    "",
    "| 编号 | 级别 | 位置 | 问题 | 建议修法 |",
    "|---|---|---|---|---|",
    "",
    "末行结论(报告最后一个非空行,恰为以下两形态之一;零问题时必须 PASS):",
    "",
    "> 核查结论:FIX(P1×2,P2×1 …)",
    "> 核查结论:PASS",
    "",
    "裁决追加形态(仅由后端追加,AI 正文任何行不得以这两前缀开头;"
    "引用样例须置于行内代码,如 `> 待裁决:#K:…`):",
    "",
    "> 待裁决:#K:…(修复者抛出的第 K 问)",
    "> 裁决:#K:…(用户对第 K 问的回答)",
    "",
    "切勿改列名、切勿改头部/结论行格式——工具按此逐字解析,改动即解析失败。",
)

# 核查任务段常量(D-P3-13)
_CHECK_INSTRUCTIONS = (
    "任务:以干净的眼睛核查总设计文档(DESIGN.md),按五维逐项检查:\n"
    "内部一致性 / 历史批注符合度 / 决策无歧义 / 可实施性 / 结论覆盖"
    "(全部决策无一遗漏)。\n"
    "发现问题即按问题分级表逐条列出(编号从 1 递增);零问题时问题分级表"
    "可整体省略。报告末行写结论行:零问题 → `> 核查结论:PASS`;有问题 →"
    " `> 核查结论:FIX(P1×2 …)` 附分级计数。\n"
    "资料完备性:上方「二、项目资料」已包含完成本任务所需的全部材料"
    "(DESIGN.md + 全部轮次文档与批注 + 已有全部核查报告)——直接依据"
    "资料作答,不要读取资料段之外的任何文件,不要访问项目目录之外的任何路径。\n"
    "**绝不修改 DESIGN.md——你只写自家的核查报告**(权限门会拒绝你对"
    " DESIGN.md 的写入)。\n"
    "落盘指令:用 Write 工具把报告全文写入 docs/DESIGN-check-{check_n}.md"
    "(编号由任务方给出,勿自定),报告首行写档位头部行(见四)。"
    "**本次档位已由任务方给定,报告首行必须逐字写:{tier_line}**"
    "(不得写另一档位、不得省略 `> ` 前缀)。"
    "写完后在回复里简述发现。"
)

# 修复任务段常量(D-P3-14)
_REPAIR_INSTRUCTIONS = (
    "任务:按最新核查报告的问题清单与用户裁决逐条修复总设计文档。\n"
    "规则:\n"
    "1. 报告中每个问题的处置以其后的 `> 裁决:#K:` 行为准(用户裁决:"
    "「修」= 按建议修法执行;「接受现状」= 不改动该项,仅记录);\n"
    "2. 报告问题若属用户职权(如范围与非目标类问题),**不得替用户决定**——"
    "在最终回复文本里单独一行输出 `> 待裁决:#K:<问题>` 后即结束"
    "(抛问协议:#K 从 1 递增,一次抛出全部待裁决问题;后端会截存并暂停"
    "等你获得裁决);\n"
    "3. 修订用 Write 工具把修改后的总设计文档**全文**写入 DESIGN.md.tmp"
    "(项目根,整体覆盖式写入)后即结束——绝不直接写 DESIGN.md"
    "(权限门将拒绝);{loose_pass_rule}\n"
    "资料完备性:上方「二、项目资料」已包含完成本任务所需的全部材料——"
    "直接依据资料作答,不要读取资料段之外的任何文件。"
)


def build_check_prompt(project_path, check_n: int, tier: str) -> str:
    """拼装「干净的眼睛」核查提示词(D-P3-13 / D-P3-15 / D-P3-29)。

    四段结构(照 build_round_prompt 同族):
      一、系统段:角色(独立核查引擎,无讨论立场,只依据磁盘文件)+ 明禁
                 绝不修改 DESIGN.md(只写自家报告)+ §3.8 语言红线
      二、资料段:DESIGN.md 全文 + 全部完整轮文档 + 各轮 annotations 逐条 +
                 已有全部 DESIGN-check 报告全文(max_check_number 循环,
                 严格档趋势照读,§8.2 以磁盘文件为唯一输入;报告缺给显式说明)
      三、任务段:_CHECK_INSTRUCTIONS(五维核查 + 结论行文法 + 落盘指令,
                 check_n 由后端算好注入防编错号 D-P3-21)
      四、文法模板:_CHECK_GRAMMAR_EXAMPLES 逐字(表头/头部行/结论行与
                 grammar.py 解析器两端一字不差)
    """
    project = Path(project_path)
    docs_dir = project / "docs"
    from backend import annotations as annotations_mod
    from backend.state import list_complete_rounds, max_check_number

    # ---- 资料段①:DESIGN.md 全文(§8.2 核查对象) ----
    design_path = project / "DESIGN.md"
    if design_path.is_file():
        try:
            design_text = design_path.read_text(
                encoding="utf-8", errors="replace"
            )
        except OSError:
            design_text = ""
        design_section = (
            f"### 总设计文档:DESIGN.md(全文——本轮核查对象)\n\n{design_text}"
            if design_text.strip()
            else "### 总设计文档:DESIGN.md\n\n(文件为空)"
        )
    else:
        design_section = "### 总设计文档:DESIGN.md\n\n(尚不存在)"

    # ---- 资料段②:全部完整轮文档 + 各轮 annotations 逐条 ----
    round_numbers = list_complete_rounds(docs_dir)
    round_sections: list[str] = []
    anno_lines: list[str] = []
    for n in round_numbers:
        round_path = docs_dir / f"discuss-round-{n}.md"
        try:
            text = round_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            text = ""
        round_sections.append(
            f"### 轮次文档:docs/discuss-round-{n}.md(全文)\n\n{text}"
        )
        ann = annotations_mod.load(project, n)
        for item in ann.get("items") or []:
            anno_lines.append(
                f"- 轮 {n} | id: {item.get('id', '')} | 原文摘录: "
                f"{item.get('quote', '')} | 用户批注: {item.get('note', '')}"
                f" | 类型: {item.get('type', '')}"
            )
    if round_sections:
        rounds_section = "\n\n".join(round_sections)
    else:
        rounds_section = "(无完整轮次文档)"
    if anno_lines:
        annotations_section = (
            "### 各轮批注(逐条;历史批注符合度是核查维度之一)\n\n"
            + "\n".join(anno_lines)
        )
    else:
        annotations_section = "### 各轮批注\n\n全部轮次均无批注记录。"

    # ---- 资料段③:已有全部 DESIGN-check 报告全文(严格档趋势照读) ----
    max_check = max_check_number(docs_dir)
    check_sections: list[str] = []
    if max_check is not None:
        for n in range(1, max_check + 1):
            check_path = docs_dir / f"DESIGN-check-{n}.md"
            if check_path.is_file():
                try:
                    text = check_path.read_text(
                        encoding="utf-8", errors="replace"
                    )
                except OSError:
                    text = ""
                check_sections.append(
                    f"### 既有核查报告:docs/DESIGN-check-{n}.md(全文)\n\n{text}"
                )
    if check_sections:
        checks_section = (
            "### 既有核查报告(全部," f"严格档趋势照读)\n\n" + "\n\n".join(check_sections)
        )
    else:
        checks_section = "### 既有核查报告\n\n(尚无任何核查报告——这是首轮核查。)"

    grammar_examples = "\n".join(_CHECK_GRAMMAR_EXAMPLES)
    # 档位头部行逐字注入(D-P3-12:报告首行必须与本轮档位一致;两常量字面
    # 取自 grammar,不手拼——缺此注入时 AI 无从得知该写哪一行)
    from backend.grammar import TIER_LINE_LOOSE, TIER_LINE_STRICT

    tier_line = TIER_LINE_LOOSE if tier == "宽松" else TIER_LINE_STRICT
    instructions = (
        _CHECK_INSTRUCTIONS.replace("{check_n}", str(check_n))
        .replace("{tier_line}", tier_line)
    )

    return (
        "## 一、你的角色\n\n"
        "你是本工具的核查执行者——干净的眼睛:独立核查引擎,无讨论立场,"
        "只依据磁盘文件判断。\n"
        f"{_LANGUAGE_RULES}\n"
        "**绝不修改 DESIGN.md——你只写自家的核查报告。**\n\n"
        f"## 二、项目资料(磁盘文件为唯一输入,§8.2)\n\n"
        f"{design_section}\n\n"
        f"{rounds_section}\n\n"
        f"{annotations_section}\n\n"
        f"{checks_section}\n\n"
        f"## 三、本次任务\n\n"
        f"{instructions}\n\n"
        "## 四、报告文法模板(逐字遵守,§6.4)\n\n"
        f"{grammar_examples}\n"
    )


def build_repair_prompt(project_path, check_n: int, tier: str) -> str:
    """拼装修复者提示词(D-P3-14 / D-P3-18 / D-P3-29)。

    四段结构:
      一、系统段:角色(修复引擎)+ §3.8 语言红线
      二、资料段:DESIGN.md 全文 + **最新报告全文**(含裁决行——磁盘即状态,
                 续跑天然满足 D-P3-19)+ 其他既有报告 + 轮次文档/批注
      三、任务段:_REPAIR_INSTRUCTIONS(按裁决逐条修复 + 抛问协议 +
                 tmp 落盘纪律 + 宽松档追加 PASS 特例)
      四、文法模板:_CHECK_GRAMMAR_EXAMPLES 逐字(问题分级表头与裁决
                 追加形态照读)
    """
    project = Path(project_path)
    docs_dir = project / "docs"
    from backend import annotations as annotations_mod
    from backend.state import list_complete_rounds

    # ---- 资料段①:DESIGN.md 全文 ----
    design_path = project / "DESIGN.md"
    if design_path.is_file():
        try:
            design_text = design_path.read_text(
                encoding="utf-8", errors="replace"
            )
        except OSError:
            design_text = ""
        design_section = (
            f"### 总设计文档:DESIGN.md(全文——本轮修复对象)\n\n{design_text}"
            if design_text.strip()
            else "### 总设计文档:DESIGN.md\n\n(文件为空)"
        )
    else:
        design_section = "### 总设计文档:DESIGN.md\n\n(尚不存在)"

    # ---- 资料段②:最新报告全文(含裁决行,磁盘即状态)+ 其他既有报告 ----
    latest_n = check_n
    check_sections: list[str] = []
    latest_path = docs_dir / f"DESIGN-check-{latest_n}.md"
    if latest_path.is_file():
        try:
            latest_text = latest_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            latest_text = ""
        check_sections.append(
            f"### 最新核查报告:docs/DESIGN-check-{latest_n}.md"
            "(全文——问题清单与用户裁决都在其中,修复以此为准)\n\n"
            f"{latest_text}"
        )
    else:
        check_sections.append(
            f"### 最新核查报告:docs/DESIGN-check-{latest_n}.md\n\n(尚不存在)"
        )
    for n in range(1, latest_n):
        other_path = docs_dir / f"DESIGN-check-{n}.md"
        if other_path.is_file():
            try:
                text = other_path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                text = ""
            check_sections.append(
                f"### 其他既有核查报告:docs/DESIGN-check-{n}.md(全文)\n\n{text}"
            )

    # ---- 资料段③:轮次文档 + 各轮批注 ----
    round_numbers = list_complete_rounds(docs_dir)
    round_sections: list[str] = []
    anno_lines: list[str] = []
    for n in round_numbers:
        round_path = docs_dir / f"discuss-round-{n}.md"
        try:
            text = round_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            text = ""
        round_sections.append(
            f"### 轮次文档:docs/discuss-round-{n}.md(全文)\n\n{text}"
        )
        ann = annotations_mod.load(project, n)
        for item in ann.get("items") or []:
            anno_lines.append(
                f"- 轮 {n} | id: {item.get('id', '')} | 原文摘录: "
                f"{item.get('quote', '')} | 用户批注: {item.get('note', '')}"
                f" | 类型: {item.get('type', '')}"
            )
    if round_sections:
        rounds_section = "\n\n".join(round_sections)
    else:
        rounds_section = "(无完整轮次文档)"
    if anno_lines:
        annotations_section = (
            "### 各轮批注(逐条)\n\n" + "\n".join(anno_lines)
        )
    else:
        annotations_section = "### 各轮批注\n\n全部轮次均无批注记录。"

    # 宽松档特例指令(D-P3-14:修复者在报告末追加 PASS)
    if tier == "宽松":
        loose_pass_rule = (
            "本档位为宽松档:这是唯一一轮修复——完成后用 Write 工具整体重写"
            " docs/DESIGN-check-{check_n}.md(含报告原内容)并在报告末行追加"
            " `> 核查结论:PASS` 结论行(或用 Edit 在末行追加——落盘物必须"
            " 末行前缀合规),随后即结束。"
        ).replace("{check_n}", str(check_n))
    else:
        loose_pass_rule = (
            "本档位为严格档:修复完成后即结束,后端会自动开启下一轮核查。"
        )

    grammar_examples = "\n".join(_CHECK_GRAMMAR_EXAMPLES)
    instructions = _REPAIR_INSTRUCTIONS.format(loose_pass_rule=loose_pass_rule)

    return (
        "## 一、你的角色\n\n"
        "你是本工具的修复引擎。最新核查报告已落盘,你的任务是把报告问题"
        "按用户裁决逐条修复到总设计文档。\n"
        f"{_LANGUAGE_RULES}\n\n"
        "## 二、项目资料(磁盘文件为唯一输入,§8.2)\n\n"
        f"{design_section}\n\n"
        + "\n\n".join(check_sections)
        + f"\n\n{rounds_section}\n\n"
        f"{annotations_section}\n\n"
        "## 三、本次任务\n\n"
        f"{instructions}\n\n"
        "## 四、报告文法模板(逐字遵守,§6.4)\n\n"
        f"{grammar_examples}\n"
    )

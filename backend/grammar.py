# -*- coding: utf-8 -*-
"""§6.4 六条机器文法解析器(DESIGN.md §6.4 / FLOW-07 / D-P2-16~19)。

解析(返回结构化数据)与判定(返回 bool)分离,照 state.py 的
list_complete_rounds / is_complete_round 分离风格;授权标记与 PASS 前缀
常量直接复用 backend.state(D-P2-16:同一语义不复制第二份,本模块源码
无第二处标记字符串字面量定义)。

六条覆盖(§6.4 表 + PASS/裁决段):
  1. 维度表:二级标题含「覆盖维度表」,列 = 维度/状态/说明,状态 ∈ {✓,◐,✗};
     全绿 ⇔ 无 ◐ 与 ✗(+ 状态列脏值 fail-closed,见 is_dimension_table_green)
  2. 未决清单:二级标题含「未决问题清单」,列 = 编号/问题/状态;清零 ⇔ 无待决
  3. 授权申请标记:文档最后一个非空行恰为两串之一(复用 state 常量与
     last_nonempty_line,exact match after strip——前缀不算,后缀不算)
  4. 批注回应表:二级标题含「批注回应」,列 = 批注id/原文摘录/回应;
     id 是回写配对的唯一依据(供 annotations.writeback 消费,D-P2-13)
  5. PASS 结论行:结论行锚点取最后一处 `> 核查结论:` 行,该行前缀匹配
     state.PASS_PREFIX
  6. 裁决追加行:`> (待裁决|裁决):#K:` 形态;仅统计结论行之后;同号配对

本模块只解析实施后新生成的轮次文档——不回溯解析本仓库历史轮文档
(D-P2-19);解析函数对任意畸形输入(空文档/无标题/空表格/脏表格行)
给确定判定不抛(T-idi02-01)。
零第三方依赖、纯标准库文本函数,无磁盘 IO。
"""
from __future__ import annotations

import logging
import re

from backend.state import (
    AUTH_MARKER_YES,
    AUTH_MARKER_NO,
    PASS_PREFIX,
    last_nonempty_line,
)

logger = logging.getLogger(__name__)

__all__ = [
    "TIER_LINE_STRICT",
    "TIER_LINE_LOOSE",
    "parse_dimension_table",
    "is_dimension_table_green",
    "parse_pending_list",
    "is_pending_list_clear",
    "parse_auth_marker",
    "parse_annotation_responses",
    "is_pass_conclusion",
    "parse_verdict_lines",
    "unpaired_verdicts",
    "parse_tier_line",
    "parse_problem_grades",
    "is_pure_p2",
    "scan_pending_questions",
]

# §6.4 裁决追加行形态:"> (待裁决|裁决):#K:"(strip 后匹配;待裁决在前,
# 防止「裁决」前缀歧义——交替匹配按书写顺序取先者)
_VERDICT_RE = re.compile(r"^>\s*(待裁决|裁决):#(\d+):")

# §6.4 结论行锚点前缀(锚点取最后一处以它开头的行;PASS 判定前缀复用 state)
_CONCLUSION_LINE_PREFIX = "> 核查结论:"

# 维度表状态列合法值(§6.4:状态 ∈ {✓, ◐, ✗};全绿 ⇔ 无 ◐ 与 ✗)
_STATUS_GREEN = "✓"
_STATUS_HALF = "◐"
_STATUS_CROSS = "✗"
_KNOWN_DIM_STATUSES = {_STATUS_GREEN, _STATUS_HALF, _STATUS_CROSS}

# 报告头部档位行字面(§8.2:档位记录于每份核查报告头部;checks.py 落盘与
# Wave 3 prompt 注入逐字引用同一常量,不复制第二份字面量——D-P3-12/D-P3-15)
TIER_LINE_STRICT = "> 自检档位:严格"
TIER_LINE_LOOSE = "> 自检档位:宽松"
_TIER_LINE_PREFIX = "> 自检档位:"

# 未决清单状态列开放值(§6.4:清零 ⇔ 无状态为「待决」的行)
_PENDING_OPEN = "待决"

# 裁决行 kind(§6.4:待裁决 = 修复者抛出的第 K 问;裁决 = 用户对第 K 问的回答)
_VERDICT_PENDING = "待裁决"
_VERDICT_ANSWERED = "裁决"

# 二级标题前缀(表格定位用)
_HEADING_PREFIX = "## "


def _extract_table(md_text: str, heading_keyword: str) -> list[list[str]]:
    """共通表格解析:定位首个标题含关键词的二级标题,取其下连续表格行。

    扫 splitlines:找到首个 line.startswith("## ") 且 heading_keyword in 标题文本
    的二级标题;其后逐行:表格首行尚未出现时空行跳过(markdown 标题与表间
    的空行惯例)、首个 | 行 = 表头丢弃、markdown 分隔行(|---|---|)不收;
    表格已开始后遇到任何非 | 行(空行/正文/新标题)即终止该表。同名标题
    多现取第一处(DESIGN.md 每轮一份的结构假设)。
    无标题 / 标题下无表格 → 返回 [](畸形输入给确定判定,T-idi02-01)。
    """
    lines = md_text.splitlines()
    rows: list[list[str]] = []
    in_target = False
    seen_row = False  # in_target 下是否已见到表格行(表头)
    for line in lines:
        if line.startswith(_HEADING_PREFIX):
            if in_target:
                break  # 目标表已定位(或已判定无表),同名标题再出现不重开
            in_target = heading_keyword in line
            continue
        if not in_target:
            continue
        body = line.strip()
        if not body.startswith("|"):
            if seen_row:
                break  # 表格已开始,遇到非表格行即终止该表
            if body:
                break  # 标题与表格之间出现非空的非表格正文 → 该标题下无表
            continue  # 表格开始前的空行跳过
        columns = [cell.strip() for cell in body.strip("|").split("|")]
        if not seen_row:
            seen_row = True  # 首个表格行 = 表头,丢弃
            continue
        if _is_separator_row(columns):
            continue  # markdown 分隔行(|---|---|)不是数据行
        rows.append(columns)
    return rows


def _is_separator_row(columns: list[str]) -> bool:
    """markdown 表格分隔行:非空 cell 全部只由 -/: 构成(如 ------)。"""
    non_empty = [cell for cell in columns if cell]
    return bool(non_empty) and all(set(cell) <= {"-", ":"} for cell in non_empty)


# ---------- 1. 维度表(§6.4:二级标题含「覆盖维度表」) ----------

def parse_dimension_table(md_text: str) -> list[dict]:
    """解析维度表为 [{"dimension", "status", "note"}] 行列表。

    列 = 维度/状态/说明(§6.4 字面);表头丢弃、各列 strip;无表返回 []。
    """
    rows = _extract_table(md_text, "覆盖维度表")
    result: list[dict] = []
    for columns in rows:
        dimension = columns[0] if len(columns) > 0 else ""
        status = columns[1] if len(columns) > 1 else ""
        note = columns[2] if len(columns) > 2 else ""
        result.append({"dimension": dimension, "status": status, "note": note})
    return result


def is_dimension_table_green(md_text: str) -> bool:
    """维度表全绿判定:状态列无 ◐ 与 ✗(§6.4 字面:全绿 ⇔ 无 ◐ 与 ✗)。

    空表 = 无行动 = 绿(表不存在或无数据行均返回 True——锁定 §6.4 判定式
    字面,按钮点亮条件由调用方另行组合)。
    deliberate deviation from §6.4 letter, fail-closed:状态列值不在
    {✓,◐,✗} 的脏值行(如「待定」)判非绿——比字面「无 ◐ 与 ✗」更保守,
    为后端防脏输入的显式设计选择。
    """
    for row in parse_dimension_table(md_text):
        status = row["status"]
        if status == _STATUS_HALF or status == _STATUS_CROSS:
            return False
        if status not in _KNOWN_DIM_STATUSES:
            return False  # 脏值 fail-closed(见 docstring)
    return True


# ---------- 2. 未决清单(§6.4:二级标题含「未决问题清单」) ----------

def parse_pending_list(md_text: str) -> list[dict]:
    """解析未决清单为 [{"number", "question", "status"}] 行列表。

    列 = 编号/问题/状态;表头丢弃、各列 strip;无表返回 []。
    """
    rows = _extract_table(md_text, "未决问题清单")
    result: list[dict] = []
    for columns in rows:
        number = columns[0] if len(columns) > 0 else ""
        question = columns[1] if len(columns) > 1 else ""
        status = columns[2] if len(columns) > 2 else ""
        result.append({"number": number, "question": question, "status": status})
    return result


def is_pending_list_clear(md_text: str) -> bool:
    """未决清单清零判定:无任何 status == 待决 的行(§6.4 字面)。

    脏值行(非「待决」)不算待决——清单判定照 §6.4 字面只找「待决」;
    与维度表的 fail-closed 刻意不同(清单脏值如实呈现给用户更合理,
    这里的「清零 ⇔ 无待决」是 DESIGN.md 判定式原文)。
    无表 = 清零 = True。
    """
    return all(row["status"] != _PENDING_OPEN for row in parse_pending_list(md_text))


# ---------- 3. 授权申请标记(§6.4:末非空行恰为两串之一) ----------

def parse_auth_marker(md_text: str) -> str | None:
    """授权申请标记三态解析:"yes" / "no" / None。

    state.is_complete_round 的三分化语义重组(合法两态 + None),底层复用
    state.last_nonempty_line 与 AUTH_MARKER_YES/NO;不复判 is_complete_round
    (后者继续留给 derive_state 用,两者共享底层常量,D-P2-16)。
    末非空行恰为 AUTH_MARKER_YES → "yes";恰为 AUTH_MARKER_NO → "no";
    其余(前缀/后缀/无标记/空文档)→ None。
    """
    last = last_nonempty_line(md_text)
    if last == AUTH_MARKER_YES:
        return "yes"
    if last == AUTH_MARKER_NO:
        return "no"
    return None


# ---------- 4. 批注回应表(§6.4:二级标题含「批注回应」) ----------

def parse_annotation_responses(md_text: str) -> list[dict]:
    """解析批注回应表为 [{"id", "quote", "response"}] 行列表。

    列 = 批注id/原文摘录/回应(§6.4/§6.3 字面);id 列 strip 后为空的行
    跳过(不抛);表头丢弃;无表返回 []。解析器只负责提取——命中/未命中
    的配对是 writeback 的职责(D-P2-13:回写以 id 配对为唯一依据)。
    """
    rows = _extract_table(md_text, "批注回应")
    result: list[dict] = []
    for columns in rows:
        item_id = columns[0] if len(columns) > 0 else ""
        if not item_id.strip():
            continue  # id 空 → 跳过该行
        quote = columns[1] if len(columns) > 1 else ""
        response = columns[2] if len(columns) > 2 else ""
        result.append(
            {"id": item_id.strip(), "quote": quote.strip(), "response": response.strip()}
        )
    return result


# ---------- 5. PASS 结论行(锚点取末一处) + 6. 裁决追加行 ----------

def _last_conclusion_index(md_text: str) -> int | None:
    """找最后一处以 "> 核查结论:" 开头(strip 后 startswith)的行号;无 → None。"""
    last_index: int | None = None
    for index, line in enumerate(md_text.splitlines()):
        if line.strip().startswith(_CONCLUSION_LINE_PREFIX):
            last_index = index
    return last_index


def is_pass_conclusion(md_text: str) -> bool:
    """PASS 结论行判定:末锚点行以 state.PASS_PREFIX 开头(前缀匹配)。

    锚点 = 最后一处 `> 核查结论:` 行(§6.4:宽松档含裁决轮的报告可有双
    结论行,锚点取末一处);无结论行 → False。
    等价于 state 的最新报告末行 PASS 判定,但按"末一处锚点"语义重新表述。
    """
    anchor = _last_conclusion_index(md_text)
    if anchor is None:
        return False
    lines = md_text.splitlines()
    return lines[anchor].strip().startswith(PASS_PREFIX)


def parse_verdict_lines(md_text: str) -> list[dict]:
    """解析结论行之后的裁决追加行为 [{"kind", "number"}] 列表。

    仅扫描末锚点行(`> 核查结论:` 取最后一处)之后的行;行 strip 后匹配
    _VERDICT_RE(r"^>\s*(待裁决|裁决):#(\d+):")的才收;报告头部(锚点之前)
    的同形态行一概不进配对空间(§6.4 扫描范围与排他);无锚点 → []。
    """
    anchor = _last_conclusion_index(md_text)
    if anchor is None:
        return []
    result: list[dict] = []
    for line in md_text.splitlines()[anchor + 1:]:
        match = _VERDICT_RE.match(line.strip())
        if match:
            result.append({"kind": match.group(1), "number": int(match.group(2))})
    return result


def unpaired_verdicts(md_text: str) -> list[int]:
    """未配对的待裁决编号列表:待裁决的 number 存在、同号裁决不存在。

    同号(待裁决 #K + 裁决 #K)即配对——配对的不出现;多组问答共存时各自
    配对;返回按出现顺序去重。供 §6.4 判定式①「存在未配对待裁决 → 暂停态」。
    """
    verdicts = parse_verdict_lines(md_text)
    pending_numbers = [
        v["number"] for v in verdicts if v["kind"] == _VERDICT_PENDING
    ]
    answered_numbers = {
        v["number"] for v in verdicts if v["kind"] == _VERDICT_ANSWERED
    }
    unpaired: list[int] = []
    for number in pending_numbers:
        if number not in answered_numbers and number not in unpaired:
            unpaired.append(number)
    return unpaired


# ---------- 7. 报告头部档位行 + 8. 问题分级表 + 9. 待裁决文本扫描 ----------
# (Phase 3 纯增量,PLAN idi-03-01 Task 2 / DATA-04 / D-P3-15 / D-P3-17 / D-P3-18;
#  既有六条(1-6)锁定语义零触碰——check-14 锁定版,本节只新增不修改)

# 形态来源 _VERDICT_RE 的待裁决分支(同前缀/分组风格派生,不复制第二份独立
# 形态来源;_VERDICT_RE 锚定「结论行之后」,本正则全文无锚点扫描——服务
# 修复者输出文本/事件流与暂停态问题呈现,D-P3-18)
_PENDING_QUESTION_RE = re.compile(r"^>\s*待裁决:#(\d+):(.*)$")


def parse_tier_line(md_text: str) -> str | None:
    """报告头部档位行三态解析:"严格"/"宽松"/None(§8.2 / D-P3-15)。

    扫首个以 `> 自检档位:` 开头(strip 后)的行——报告可能带 H1 标题,
    不假定首行;整行 strip 后恰为 TIER_LINE_STRICT / TIER_LINE_LOOSE 才
    返回对应值;脏变体(如「超严格」/行内尾注)与无该行 → None。
    """
    for line in md_text.splitlines():
        stripped = line.strip()
        if stripped.startswith(_TIER_LINE_PREFIX):
            if stripped == TIER_LINE_STRICT:
                return "严格"
            if stripped == TIER_LINE_LOOSE:
                return "宽松"
            return None  # 存在但脏(非两串之一)
    return None  # 无该前缀行


def parse_problem_grades(md_text: str) -> list[dict]:
    """解析问题分级表为 [{"number", "level", "location", "issue", "suggestion"}]。

    列 = 编号/级别/位置/问题/建议修法(D-P3-15 表头字面,与 prompt 注入
    逐字一致——两端同字面是 D-P3-29 硬要求);number 列转 int(脏值如「一」
    → 保留 0 + warning 不抛——与 scan_pending_questions/裁决行 #K 的整数
    K 同型,不做字符串/整数混型比较);表头与分隔行丢弃;无表 → []。
    """
    rows = _extract_table(md_text, "问题分级")
    result: list[dict] = []
    for columns in rows:
        raw_number = columns[0] if len(columns) > 0 else ""
        try:
            number = int(raw_number.strip())
        except ValueError:
            logger.warning("问题分级表编号脏值(%r),该行 number 落 0", raw_number)
            number = 0
        level = columns[1] if len(columns) > 1 else ""
        location = columns[2] if len(columns) > 2 else ""
        issue = columns[3] if len(columns) > 3 else ""
        suggestion = columns[4] if len(columns) > 4 else ""
        result.append(
            {
                "number": number,
                "level": level,
                "location": location,
                "issue": issue,
                "suggestion": suggestion,
            }
        )
    return result


def is_pure_p2(md_text: str) -> bool:
    """纯 P2 判定:问题表全部 level == P2 且报告有结论行锚点(D-P3-17 / D-22)。

    空表/无表 → False(零问题报告走 PASS 路径,不以纯 P2 处理,fail-closed);
    无 `> 核查结论:` 锚点行(半份 P2 报告:P2 表已写、结论行未写)→ False
    ——不得判纯 P2 进 p2 死局态,须回落 running 走「继续自检」恢复
    (复用既有 _last_conclusion_index 判 None);P0/P1 任一出现 → False。
    """
    rows = parse_problem_grades(md_text)
    if not rows:
        return False
    if _last_conclusion_index(md_text) is None:
        return False  # 半份报告 fail-closed
    return all(row["level"] == "P2" for row in rows)


def scan_pending_questions(text: str) -> list[dict]:
    """全文扫描 `> 待裁决:#K:` 形态行,返回 [{"number", "text"}](D-P3-18)。

    无锚点全文扫描(say 事件流与最终文本均可喂入)——与 parse_verdict_lines
    的「结论行之后」扫描空间不同,服务于修复者输出扫描与暂停态问题呈现;
    number 为 int(与 parse_verdict_lines 同型)。行内代码引用样例不误收:
    strip 后以反引号开头的行是 §6.4 写作纪律要求的行内代码引用样例
    (整行被包裹的文法讲解),不是真实抛问——跳过。
    """
    result: list[dict] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("`"):
            continue  # 行内代码引用样例(§6.4 写作纪律:引用样例须置于行内代码)
        match = _PENDING_QUESTION_RE.match(stripped)
        if match:
            result.append(
                {"number": int(match.group(1)), "text": match.group(2).strip()}
            )
    return result

# -*- coding: utf-8 -*-
"""阶段 1-2 系统提示词模板(DESIGN.md §5.1 无状态 + §3.8 语言红线)。

build_phase12_prompt(project_path, user_message) -> str:
拼装发给 AI 的完整调用载荷——每次调用 = 全新无头,启动自磁盘读 docs/ 全部文档(§5.1),
所有记忆都在文档里;本模块只负责"把磁盘现状读出来拼进提示词",自己不维护任何状态。
"""

from __future__ import annotations

from pathlib import Path


def build_phase12_prompt(project_path, user_message: str) -> str:
    """拼装阶段 1-2 的完整调用提示词(骨架:RED 占位,未实现)。"""
    raise NotImplementedError("build_phase12_prompt 尚未实现(Task 1 GREEN 阶段实现)")

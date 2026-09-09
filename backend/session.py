# -*- coding: utf-8 -*-
"""模块级会话管理(D-P1-10 / PLAN idi-01-03 Task 1):单机单人,一个当前项目。

职责:
  - enter_project(path) 校验目录存在 → 设当前项目 → 返回 derive_state 结果
  - send_message(user_text) 完整流水线:append [user] → 组装提示词 → 后台线程
    起 AICaller.run → 事件逐条 publish 到 broker → done 且非 abort 时追加 [ai]
  - 权限确认队列:pending {id: (Event, decision)} ;request_permission 挂起等待;
    resolve_permission(id, approved) 放行/驳回;abort 强制释放所有 pending 为 False

骨架:RED 占位,未实现(模块结构先立起来,GREEN 阶段填行为)。
"""

from __future__ import annotations

from pathlib import Path


def enter_project(path) -> dict:
    """校验目录存在后设当前项目,返回 derive_state 结果(RED 占位)。"""
    raise NotImplementedError("enter_project 尚未实现(Task 1 GREEN 阶段实现)")


def send_message(user_text: str) -> bool:
    """发消息流水线(RED 占位)。"""
    raise NotImplementedError("send_message 尚未实现(Task 1 GREEN 阶段实现)")


def resolve_permission(permission_id: str, approved: bool) -> bool:
    """回答一个挂起的权限确认(RED 占位)。"""
    raise NotImplementedError("resolve_permission 尚未实现(Task 1 GREEN 阶段实现)")

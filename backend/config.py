"""工具运行配置:仓库根 config.json 是唯一配置来源。

字段:
  ai_caller ∈ {"sdk", "subprocess"} —— AICaller 实现路线(DESIGN.md §5.3 双轨)
  ai_model  —— 后续阶段可扩展键(本阶段仅保存,不消费)
"""

import json
import logging
import os
from pathlib import Path

logger = logging.getLogger("backend.config")

# 仓库根 = 工具源代码仓(D-P1-4);config.json 属骨架新增文件
_REPO_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = _REPO_ROOT / "config.json"

# 合法的 ai_caller 取值
VALID_AI_CALLERS = ("sdk", "subprocess")

# 读取失败或字段缺失时回落到的默认配置
DEFAULT_CONFIG = {"ai_caller": "sdk", "ai_model": None}


def read_config() -> dict:
    """读仓库根 config.json;任何失败回落默认 {"ai_caller": "sdk"} 并在日志注明。"""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        if not isinstance(cfg, dict):
            raise ValueError("config.json 顶层必须是 JSON 对象")
        if cfg.get("ai_caller") not in VALID_AI_CALLERS:
            raise ValueError(f"ai_caller 非法:{cfg.get('ai_caller')!r}")
        # 归一化:未知键剔除,已知缺失键补默认
        merged = dict(DEFAULT_CONFIG)
        merged["ai_caller"] = cfg["ai_caller"]
        if "ai_model" in cfg:
            merged["ai_model"] = cfg["ai_model"]
        return merged
    except FileNotFoundError:
        logger.warning("config.json 不存在,回落默认 sdk 路线")
        return dict(DEFAULT_CONFIG)
    except (json.JSONDecodeError, ValueError) as exc:
        logger.warning("config.json 读取失败(%s),回落默认 sdk 路线", exc)
        return dict(DEFAULT_CONFIG)


def write_config(update: dict) -> dict:
    """把 update 深度合并进 config.json 并返回合并后的配置(Task 3 运行时换线用)。"""
    current = read_config()
    merged = dict(current)
    for key, value in update.items():
        if key in DEFAULT_CONFIG:  # 只接受已知键
            merged[key] = value
    if merged.get("ai_caller") not in VALID_AI_CALLERS:
        raise ValueError(f"ai_caller 非法:{merged.get('ai_caller')!r}")
    tmp = CONFIG_PATH.with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, CONFIG_PATH)  # 原子替换,避免半写状态
    return merged


def make_ai_caller(config: dict):
    """工厂:按 config 的 ai_caller 键选择 AICaller 实现路线(D-P1-5)。

    "sdk" → SdkAICaller(Claude Agent SDK 首选路线,Task 2 起可用)
    "subprocess" → SubprocessAICaller(claude CLI 子进程兜底)
    前端与上层零改动,两条路线事件契约一致。
    """
    route = config.get("ai_caller", "sdk")
    if route == "subprocess":
        from backend.ai_caller import SubprocessAICaller

        return SubprocessAICaller()
    if route == "sdk":
        from backend.ai_caller import SdkAICaller

        return SdkAICaller(model=config.get("ai_model"))
    raise ValueError(f"未知 ai_caller 路线:{route!r}")

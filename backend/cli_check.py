"""claude CLI 启动自检(§7.1,AI-05):已装 + 已登录。

「只挡第一次」的语义在前端实现——后端不缓存失败结果、不拒绝后续请求。
"""

import shutil
import subprocess

# 依赖 PyPI 包 fastapi/uvicorn,足够引导用户装 CLI
INSTALL_GUIDANCE = "安装 Claude Code CLI:npm install -g @anthropic-ai/claude-code"
LOGIN_GUIDANCE = "在终端运行 claude 完成登录后回到此页"


def check_claude_cli() -> dict:
    """自检 claude CLI。

    返回 dict(ok, installed, logged_in, guidance):
      ok          —— 两项全过才为 True
      installed   —— PATH 上能找到 claude 可执行文件
      logged_in   —— 一次真实查询式调用(claude -p "ping")退出码为 0
      guidance    —— 中文指引文案,按失败原因两分支
    """
    if shutil.which("claude") is None:
        return {
            "ok": False,
            "installed": False,
            "logged_in": False,
            "guidance": INSTALL_GUIDANCE,
        }
    # 已装,验可登录可调用:跑一次最小查询(倒计时 30s 防挂死)
    try:
        proc = subprocess.run(
            ["claude", "-p", "ping", "--output-format", "json"],
            capture_output=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "installed": True,
            "logged_in": False,
            "guidance": LOGIN_GUIDANCE,
        }
    logged_in = proc.returncode == 0
    if logged_in:
        guidance = ""  # 通过时无指引文案
    else:
        # 未登录或调用失败均指向登录指引(账号问题都从登录态排查)
        guidance = LOGIN_GUIDANCE
    return {
        "ok": logged_in,
        "installed": True,
        "logged_in": logged_in,
        "guidance": guidance,
    }

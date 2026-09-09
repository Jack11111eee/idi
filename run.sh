#!/usr/bin/env bash
# 一键启动脚本:自举 venv(不存在则创建并装依赖),然后启动 FastAPI 服务器。
set -euo pipefail
cd "$(dirname "$0")"

# 只在 .venv 缺失或依赖未装齐时重建/补装(幂等,可重复执行)
if [ ! -x .venv/bin/uvicorn ]; then
  echo "[run.sh] 初始化 Python 虚拟环境 .venv ..."
  python3 -m venv .venv
  .venv/bin/pip install -q -r requirements.txt
fi

echo "[run.sh] 启动服务器:http://127.0.0.1:8765"
exec .venv/bin/uvicorn backend.main:app --port 8765

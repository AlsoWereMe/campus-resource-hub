#!/bin/sh
# 服务启动：迁移到最新 → 基础种子 → 演示种子（可选）→ 启动 uvicorn。迁移与种子都幂等。
set -e
cd /app
alembic -c "services/${SERVICE}/alembic.ini" upgrade head
python -m "${SERVICE}_service.seeds" base
if [ "${SEED_DEMO:-false}" = "true" ]; then
  python -m "${SERVICE}_service.seeds" demo
fi
# shellcheck disable=SC2086
exec uvicorn --factory "${SERVICE}_service.main:create_app" --host 0.0.0.0 --port 8000 ${UVICORN_ARGS:-}

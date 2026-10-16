# 四个后端服务共用的镜像。构建：docker build -f deploy/service.Dockerfile --build-arg SERVICE=seat .
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.11 /uv /usr/local/bin/uv

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH=/opt/venv/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Shanghai

ARG SERVICE
ENV SERVICE=${SERVICE}
WORKDIR /app

# 先只装第三方依赖，源码变化时可复用这一层缓存
COPY pyproject.toml uv.lock ./
COPY libs/common/pyproject.toml libs/common/pyproject.toml
COPY services/platform/pyproject.toml services/platform/pyproject.toml
COPY services/seat/pyproject.toml services/seat/pyproject.toml
COPY services/room/pyproject.toml services/room/pyproject.toml
COPY services/repair/pyproject.toml services/repair/pyproject.toml
RUN uv sync --frozen --no-dev --no-install-workspace --package ${SERVICE}-service

COPY libs libs
COPY services services
COPY deploy/run-service.sh deploy/run-service.sh
RUN uv sync --frozen --no-dev --package ${SERVICE}-service

EXPOSE 8000
CMD ["/app/deploy/run-service.sh"]

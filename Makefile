# 常用本地命令。运行 make 或 make help 查看列表。Windows 组员请在 WSL2 中使用。
# 带 s= 的命令指定服务：platform | seat | room | repair

SHELL := /bin/bash
.DEFAULT_GOAL := help

-include .env
COMPOSE := docker compose --env-file .env -f deploy/compose.yml
S_UPPER = $(shell echo $(s) | tr a-z A-Z)
HOST_DB_URL = postgresql+psycopg://$(s)_svc:$($(S_UPPER)_DB_PASSWORD)@127.0.0.1:$(POSTGRES_PORT)/$(POSTGRES_DB)

.PHONY: help setup up down reset ps logs restart seed revision lint fmt typecheck test verify-db \
	contracts contracts-check check web web-check

help: ## 列出可用命令
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

.env:
	cp .env.example .env
	@echo "已从 .env.example 生成 .env；端口冲突时在 .env 中修改"

setup: .env ## 首次使用：生成 .env，安装 Python 与前端依赖
	uv sync --all-packages
	@if [ -f apps/web/package.json ]; then cd apps/web && pnpm install; fi

up: .env ## 构建并启动全部容器（中间件、四个服务、网关），等待健康
	$(COMPOSE) up -d --build --wait

down: ## 停止本地环境（保留数据）
	$(COMPOSE) down

reset: ## 停止并删除本地数据卷；下次 up 时从空库重新迁移并写入种子
	$(COMPOSE) down -v

ps: ## 查看容器状态
	$(COMPOSE) ps

logs: ## 跟随日志：make logs s=seat
	$(COMPOSE) logs -f $(s)

restart: ## 重启某个服务（会重新迁移）：make restart s=seat
	$(COMPOSE) restart $(s)

seed: ## 重新写入演示种子（幂等）：make seed s=platform
	$(COMPOSE) exec $(s) python -m $(s)_service.seeds demo

revision: ## 新建迁移（需先 make up）：make revision s=seat m="add booking"
	@test -n "$(s)" -a -n "$(m)" || (echo '用法：make revision s=seat m="说明"'; exit 1)
	DATABASE_URL="$(HOST_DB_URL)" uv run alembic -c services/$(s)/alembic.ini \
		revision --autogenerate -m "$(m)"

lint: ## 代码检查（不修改文件）
	uv run ruff check .
	uv run ruff format --check .

fmt: ## 自动格式化并修复可自动修复的问题
	uv run ruff format .
	uv run ruff check --fix .

typecheck: ## 类型检查（mypy strict）
	uv run mypy

test: ## 运行测试（需要 Docker）；只测一个服务：make test s=seat
	uv run pytest $(if $(s),services/$(s),)

contracts: ## 从代码导出接口与消息契约到 contracts/，并重新生成前端类型
	uv run python scripts/export_contracts.py
	@if [ -d apps/web/node_modules ]; then cd apps/web && pnpm gen:api; fi

contracts-check: ## 检查 contracts/ 与代码一致（提交前必跑）
	uv run python scripts/export_contracts.py --check

verify-db: .env ## 验证数据库按 schema 隔离（需先 make up）
	./scripts/verify-db-isolation.sh

check: lint typecheck contracts-check test web-check ## 提交前检查：后端 lint、类型、契约、测试 + 前端检查

web-check: ## 前端类型检查与单元测试
	@if [ -d apps/web/node_modules ]; then cd apps/web && pnpm typecheck && pnpm test; \
	else echo "未安装前端依赖，跳过（先运行 make setup）"; fi

web: ## 启动前端开发服务器，然后访问 http://127.0.0.1:8080
	cd apps/web && pnpm dev

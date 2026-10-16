# 常用本地命令。运行 make 或 make help 查看列表。Windows 组员请在 WSL2 中使用。

SHELL := /bin/bash
.DEFAULT_GOAL := help

COMPOSE := docker compose --env-file .env -f deploy/compose.yml
PY_SOURCES := $(shell find libs services -name '*.py' -not -path '*/.venv/*' 2>/dev/null)

.PHONY: help setup up down reset ps logs lint fmt typecheck test verify-db check

help: ## 列出可用命令
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

.env:
	cp .env.example .env
	@echo "已从 .env.example 生成 .env；端口冲突时在 .env 中修改"

setup: .env ## 首次使用：生成 .env 并安装 Python 依赖
	uv sync --all-packages

up: .env ## 启动本地中间件并等待全部健康
	$(COMPOSE) up -d --wait

down: ## 停止本地环境（保留数据）
	$(COMPOSE) down

reset: ## 停止并删除本地数据卷，下次 up 时从空库重新初始化
	$(COMPOSE) down -v

ps: ## 查看容器状态
	$(COMPOSE) ps

logs: ## 跟随日志；指定服务：make logs s=postgres
	$(COMPOSE) logs -f $(s)

lint: ## 代码检查（不修改文件）
	uv run ruff check .
	uv run ruff format --check .

fmt: ## 自动格式化并修复可自动修复的问题
	uv run ruff format .
	uv run ruff check --fix .

typecheck: ## 类型检查（mypy strict）
ifeq ($(strip $(PY_SOURCES)),)
	@echo "libs/ 与 services/ 中还没有 Python 代码，跳过类型检查"
else
	uv run mypy
endif

test: ## 运行测试（集成测试需要 Docker）
	@uv run pytest; status=$$?; \
	if [ $$status -eq 5 ]; then echo "没有收集到测试"; exit 0; fi; \
	exit $$status

verify-db: .env ## 验证数据库按 schema 隔离（需先 make up）
	./scripts/verify-db-isolation.sh

check: lint typecheck test ## 提交前检查：lint + typecheck + test

# campus-resource-hub

校园资源服务平台 · 软件过程管理与工程伦理课程实践项目（PJ）。

## 本地开发快速开始

**准备**：Docker（含 Compose v2）、[uv](https://docs.astral.sh/uv/)、make；前端另需 Node.js 24 与 pnpm。Windows 请在 WSL2 中操作。

```bash
make setup
```

```bash
make up
```

```bash
make verify-db
```

- `make setup`：从 `.env.example` 生成 `.env`，安装 Python 依赖；
- `make up`：启动 PostgreSQL、RabbitMQ、Redis、Mailpit，并等待全部健康；
- `make verify-db`：确认数据库已按服务账号与 schema 隔离；
- `make help`：查看全部命令。提交前运行 `make check`。

| 组件 | 地址 |
| --- | --- |
| PostgreSQL | `127.0.0.1:5432`，数据库 `campus` |
| RabbitMQ 管理界面 | http://127.0.0.1:15672 |
| Redis | `127.0.0.1:6379` |
| Mailpit（捕获的邮件） | http://127.0.0.1:8025 |

端口与本机其他服务冲突时，在 `.env` 中修改对应的 `*_PORT`。账号与口令见 `.env`，只用于本机。

## 目录

| 目录 | 内容 |
| --- | --- |
| [services/](services/README.md) | 后端服务：platform（公共层 D）、seat（M1）、room（M2）、repair（M3） |
| [libs/](libs/README.md) | 各服务共用的非业务公共库 |
| [apps/](apps/README.md) | 前端（Next.js） |
| [contracts/](contracts/README.md) | 接口与消息契约 |
| `deploy/` | Compose 与数据库初始化脚本 |
| `scripts/` | 辅助脚本 |
| `docs/` | 需求、架构与决策记录 |

## 文档

| 文档 | 说明 |
| --- | --- |
| [Pj-任务.pdf](Pj-任务.pdf) | 课程任务书 |
| [需求总览](docs/requirements/README.md) | 约定、角色总表、跨模块集成、非功能需求、决策记录；新成员从这里开始 |
| [公共层 D](docs/requirements/d-platform.md) | 身份与权限、空间与座位主数据、通知、审计 |
| [M1 自习座位预约](docs/requirements/m1-seat-reservation.md) | 任务书附件1 |
| [M2 整教室预约与审批](docs/requirements/m2-room-booking.md) | 权限门槛、申请、多级审批、超时撤销 |
| [M3 物业报修工单](docs/requirements/m3-repair.md) | 上报、派单、维修、超时升级、验收评价 |
| [系统架构设计](docs/architecture/architecture.md) | 抽象架构图、子模块职责、通信方式、部署与环境、分工 |

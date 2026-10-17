# services/

每个子目录是一个独立部署的后端服务（FastAPI），也是 uv 工作区中的一个包。一个模块 = 一个服务 = 一个目录 = 一组 schema = 一份契约（架构 §10.1）。

| 目录 | 服务 | 模块 | 数据库账号 | schema | API 前缀 |
| --- | --- | --- | --- | --- | --- |
| `platform/` | platform-service | 公共层 D | `platform_svc` | `iam`、`space`、`notify`、`audit` | `/api/{iam,space,notify,audit}/v1` |
| `seat/` | seat-service | M1 自习座位预约 | `seat_svc` | `m1` | `/api/m1/v1`、`/internal/m1/v1` |
| `room/` | room-service | M2 整教室预约与审批 | `room_svc` | `m2` | `/api/m2/v1` |
| `repair/` | repair-service | M3 物业报修工单 | `repair_svc` | `m3` | `/api/m3/v1` |

## 服务内的目录约定

```text
services/<name>/
├── pyproject.toml
├── src/<package>/
│   ├── api/              # 路由与请求 / 响应模型（每个任务一个文件，已写好接口桩）
│   ├── application/      # 用例：编排、事务、权限与数据范围校验
│   ├── domain/           # 实体、状态机、业务规则：不依赖框架，便于单元测试
│   ├── infrastructure/   # ORM 模型（models.py）、仓储、对外客户端
│   ├── seeds/            # 幂等种子：base（所有环境）与 demo（dev、test）
│   ├── jobs.py           # 定时任务登记
│   └── consumers.py      # 消息订阅登记
├── migrations/           # 本服务的 Alembic 迁移链（只新增，不修改已合入的迁移）
└── tests/                # 单元、集成、契约测试
```

## 规则

- 只改自己负责的服务目录；不得 import 其他服务的代码，共享代码只能放在 `libs/common`。
- 只访问本服务账号所属的 schema；跨模块数据通过对方的公开 / 内部 API 或消息获取。
- 对 M1 座位状态的影响只走 M1 占用块接口（`/internal/m1/v1/blocks`）。
- 本地数据库隔离可用 `make verify-db` 验证。

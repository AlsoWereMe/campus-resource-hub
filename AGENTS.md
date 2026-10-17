# AGENTS.md

在本仓库工作的智能代理（Claude Code、Codex、Qoder 等）与人类成员都遵守本文件。它是本项目流程规范的唯一来源。

## 1. 项目

- 课程实践项目「校园资源服务平台」：M1 自习座位预约、M2 整教室预约与审批、M3 物业报修工单，以及公共层 D（身份权限、空间主数据、通知、审计）。
- 考核重点是**有条理地使用智能代理开发可交付的系统**：先方案后实现，变更可追踪，AI 的产出经人验证。功能多少不是重点。
- 组长对需求、架构与决策有最终决定权。

## 2. 去哪里找

| 要找 | 位置 |
| --- | --- |
| 我该做什么 | [docs/tasks.md](docs/tasks.md) 任务卡；GitHub Issues |
| 需求、业务规则、验收标准 | [docs/requirements/](docs/requirements/README.md) |
| 接口契约 | 各服务 `api/*.py` 中的接口桩（签名即契约）；`contracts/` 为导出结果 |
| 架构、模块边界、技术栈 | [docs/architecture/architecture.md](docs/architecture/architecture.md) |
| 已做的决定 | [docs/adr.md](docs/adr.md)；需求总览 §7 |
| 过程记录 | [docs/log.md](docs/log.md) |
| 报缺陷、提变更或澄清 | 新建 Issue，选 `Bug report`（缺陷）或 `Change request`（变更请求）表单（`.github/ISSUE_TEMPLATE/`） |
| 写法参考 | 已实现的登录（`platform_service/iam/auth_api.py`）、空间查询（`space/read_api.py`）、前端账号页（`apps/web/src/app/(app)/account`） |

文档与代码不一致时以文档为准并告诉人；文档之间冲突时停下来问。

## 3. 做任务的流程

用 `do-task` skill（[.agents/skills/do-task](.agents/skills/do-task/SKILL.md)）执行，人只需说「做任务 M1-T04」。

1. **认领**：把 Issue 指派给自己；从最新 `main` 建分支 `<type>/<任务编号小写>-<英文短名>`，如 `feat/m1-t04-booking`。
2. **调研**：读任务卡、所列需求的正文与验收标准、接口桩、参考实现。
3. **方案**：写出目标（需求编号）、影响范围、按提交拆分的步骤、测试计划（每条验收标准对应哪个测试）、风险与待确认问题；有多种做法时列候选并给建议。**人确认后才写代码**；实现中发现方案不成立，停下来更新方案。
4. **实现**：按方案小步提交，每一步都能独立验证。
5. **验证**：见 §5。
6. **收尾**：更新追踪矩阵；开合并请求（`Closes #Issue`），按模板填写；请相关负责人评审。

需求有歧义、文档缺失或冲突、需要改别的模块或公共层、需要改契约：**停下来问人**，给出候选方案与建议。需要讨论的开 `Change request` Issue，讨论与组长的结论都留在 Issue 里，实现它的合并请求写 `Refs #N`。

## 4. 编码约定

### 4.1 后端分层（每个服务相同）

| 层 | 目录 | 写什么 |
| --- | --- | --- |
| 接口 | `api/` | 路由与请求 / 响应模型，只做参数转换、调用应用层 |
| 应用 | `application/` | 用例编排、权限与数据范围校验、调用 outbox |
| 领域 | `domain/` | 实体、状态机、业务规则；纯 Python，不依赖 FastAPI 与数据库 |
| 基础设施 | `infrastructure/` | ORM 模型（`models.py`）、仓储、对外客户端 |

### 4.2 必须使用的公共能力（`libs/common/src/campus_common`）

| 需要 | 用 | 禁止 |
| --- | --- | --- |
| 鉴权 | 每个接口声明其一：`require("权限点")`、`AUTHENTICATED`、`PUBLIC` | 只靠前端隐藏 |
| 数据范围 | `principal.scope(权限点).covers(building_id=…, department_id=…)` | |
| 当前时间 | `ClockDep` / `ctx.clock` 的 `now()`；业务日期用 `to_business()` | `datetime.now()` |
| 数据库事务 | `SessionDep`（请求结束自动提交，异常回滚） | 跨 schema 读写 |
| 错误 | `NotFound`、`Forbidden`、`Conflict`、`RuleViolation("BR-xx", …)` | 返回自定义错误格式 |
| 写回其他服务、通知、审计、发布事件 | `OutboxDep`：`call`、`notify`、`audit`、`publish` | 在业务代码中直接发 HTTP 或消息 |
| 读其他服务 | `ClientDep`（自动带服务令牌），按对方契约 | 访问对方数据库 |
| 定时任务 | 在 `jobs.py` 登记 `Job`，函数幂等 | |
| 订阅消息 | 在 `consumers.py` 中 `bus.subscribe(...)`，按 `message_id` 幂等 | |
| 业务参数 | 本服务参数表（`m1.*`、`m2.*`、`m3.*`） | 硬编码 |

### 4.3 模块边界与契约

- 只改自己席位的目录（见任务卡）；共享代码只能放 `libs/common`，且不放业务逻辑。
- 对 M1 座位状态的影响只走 M1 占用块接口。
- **契约先行**：接口桩的签名、请求 / 响应模型就是契约，实现时不改。确需修改时：先开 `Change request` Issue 并等组长结论 → 改模型与签名 → `make contracts` → 在合并请求中请所有消费方评审 → 再实现；不兼容的修改在提交说明中标 `BREAKING CHANGE`。
- 静态路径（如 `/bookings/history`）须在 `/{id}` 路由之前注册。

### 4.4 数据库

- 改表：改 `infrastructure/models.py` → `make revision s=<服务> m="<英文说明>"` → 检查生成的迁移 → `make restart s=<服务>`。
- 不修改已合入 main 的迁移，不手工改库；迁移先扩展、后收缩（先加列再删旧列，跨两个版本）。
- 每个服务只有一条迁移链：合并前若出现多个 head，把自己迁移的 `down_revision` 改为 main 上的最新版本。
- 种子写在 `seeds/`，必须幂等；`base` 用于所有环境，`demo` 只用于 dev / test，不得含真实个人信息。

### 4.5 Python 与前端

- Python 统一用异步库，不在事件循环里调阻塞 IO；类型标注齐全，通过 mypy strict。
- 前端只改自己的页面目录；只调本模块的 `api.<模块>` 客户端；不用 Route Handlers、Server Actions 写业务逻辑；不手写请求类型（`pnpm gen:api` 生成）。
- 文档、方案、提交说明用中文；代码标识符、API 字段、数据库对象用英文。

## 5. 测试与质量门槛

- 每条实现的验收标准都有测试，测试名含需求编号，如 `test_m1_rsv_02_ac5_concurrent_booking`。
- 测试必须验证行为：不断言常量、不靠空分支凑覆盖、不 mock 被测逻辑本身；集成测试用真实 PostgreSQL（Testcontainers，见各服务 `tests/conftest.py`）。
- 核心规则与状态机：**故意改错一处实现，确认测试失败**，再改回；在合并请求中写明做了哪次破坏。
- 时间相关逻辑用可注入时钟测试；联调时用 `PUT /internal/test/clock` 推进时间、`POST /internal/test/jobs/<name>` 立即触发任务（仅非生产环境）。
- 推送前在本地跑 `make check`（后端 lint、类型、契约一致、测试，前端类型与测试）。合并请求必须通过 CI 的 `backend`、`frontend` 两项检查（`.github/workflows/ci.yml`，另含前端生成类型一致与静态构建），不通过不能合并。CI 失败时在本地复现并修复，不要靠反复重跑碰运气。

## 6. 版本管理

- 提交历史是开发过程的主要证据：代码、规则文件、需求与决策、迁移、种子、契约、流水线配置都入库，随进展持续提交。
- 提交遵循 [commit-convention](.agents/skills/commit-convention/SKILL.md)：一个功能一个提交、Conventional Commits、`Refs` 需求编号、末尾 `Co-Authored-By` 如实标注模型、提交前向人发出提交申请。
- 合并请求：按模板填写；至少 1 人批准；改契约、`libs/common`、迁移或其他模块时，必须有相关负责人批准（CODEOWNERS 会自动请人）。
- **代码冲突由人处理**，代理不得自行解决合并冲突。不 force push，不改写已推送的历史，不用 `--no-verify`。
- 版本标记：每个里程碑合并完成后，组长在 main 上打附注标签 `vX.Y.Z`，并用 `gh release create vX.Y.Z --generate-notes` 生成发布说明。

## 7. AI 代码的常见隐患与对策

| 隐患 | 对策 |
| --- | --- |
| 测试看起来完整但什么都没测 | 验收标准逐条对应测试；故意破坏实现确认测试会失败 |
| 臆造不存在的 API、库或参数 | 只用锁文件中的依赖；以本仓库代码与契约为准；`make check` 通过才提交 |
| 越界修改别的模块、悄悄改契约 | 方案中列影响范围；`make contracts-check`；CODEOWNERS 评审 |
| 一次生成大批量、无法审查的改动 | 小步提交（单个提交尽量 ≤ 400 行）；人逐个审查后才提交 |
| 时间、时区与并发错误 | 可注入时钟；数据库约束兜底；并发与重启场景写测试 |
| 安全疏漏（越权、注入、泄露） | 每个接口声明权限并校验数据范围；ORM 参数化查询；日志不打印口令、令牌与完整个人信息 |
| 直接接受第一个方案 | 方案必须列候选与取舍，由人选定；重要取舍写入 docs/adr.md |

## 8. 需求追踪与决策

- 完成一条需求：在该需求文档追踪矩阵的「实现」填合并请求，「状态」改为已完成；不做的标「延期」并写原因，不得删除。
- 需求或决策要变：开 `Change request` Issue 问组长；同意后同步改需求正文、追踪矩阵、变更记录、需求总览 §7，并在 Issue 中附上链接。
- 新的架构取舍写入 docs/adr.md；关键过程（重要决定、事故与纠正）记入 docs/log.md。

## 9. 安全、隐私与工程伦理

- 不提交密钥、令牌、`.env`；配置经环境变量注入。
- 个人信息最小化展示（NFR-11）：其他学生看不到预约人；运营视图与导出默认脱敏；查看完整信息要留审计。
- 设计中涉及隐私、公平、可访问性等问题时，在方案中指出；每个合并请求在「伦理考量」一栏写一句（可写「无」），供个人课程论文取材。

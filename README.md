# campus-resource-hub

校园资源服务平台 · 软件过程管理与工程伦理课程实践项目（PJ）。

> **新成员只需读这一页。** 骨架已经能运行：登录、权限、空间数据、全部接口的契约都已就位，剩下的业务功能拆成了 36 张任务卡。

## 1. 第一次使用（约 10 分钟）

**准备**：Docker（含 Compose v2）、[uv](https://docs.astral.sh/uv/)、make、Node.js 24 与 pnpm。Windows 请在 WSL2 中操作。

```bash
make setup
```

```bash
make up
```

```bash
make web
```

然后打开 http://127.0.0.1:8080，用下表的演示账号登录（口令都是 `Passw0rd!`，只用于本机）。

| 账号 | 角色 | 账号 | 角色 |
| --- | --- | --- | --- |
| `student1` | 学生（计算机学院） | `roomadmin1` | 教室管理员（三教） |
| `student3` | 学生 + 学生组织负责人 | `resadmin1` | 资源管理员 |
| `staff1` | 教职工 | `ops1` | 运营管理员 |
| `approver1` | 院系审批人（计算机学院） | `dispatcher1` | 物业调度员 |
| `tech1` | 维修人员（三教） | `supervisor1` | 物业主管 |

系统管理员 `admin` 的口令为 `.env` 中的 `INITIAL_ADMIN_PASSWORD`。端口冲突时改 `.env` 中对应的 `*_PORT`。

## 2. 领任务、开发

1. 打开 [docs/tasks.md](docs/tasks.md)，选一个**席位**（A1、A2、B1、B2、C1、C2），在「席位认领」Issue 中留言；之后只做该席位的任务。
2. 在你的 AI 编程助手中打开本仓库，输入：

   ```text
   做任务 M1-T04
   ```

   助手会按 `do-task` 流程：认领 Issue、建分支、读需求与契约、**给出方案并等你确认**、实现与测试、按规范提交、开合并请求。
3. 你要做的三件事：**审方案**（不满意就让它改）、**审每次提交**（它会先问你）、**请同组成员评审合并请求**。
4. 合并后，Issue 自动关闭；进度在 GitHub 的 Issues 与里程碑中查看。
5. 发现缺陷，或要改接口、别的模块、需求：在 GitHub 新建 Issue，选「缺陷」或「变更请求」表单。

页面上标着「待实现 · 任务 X」的地方，就是该任务要写的页面；接口调用后返回 501 并给出任务编号的，就是该任务要实现的接口。

## 3. 规范

全部流程规范在 [AGENTS.md](AGENTS.md)（助手会自动读取），要点如下：

- 先方案后实现；一个功能一个提交；提交说明遵循 Conventional Commits，写明需求编号与参与的模型。
- 改接口、公共库、数据库迁移或其他模块，先问组长并请相关负责人评审；合并冲突由人处理。
- 每条验收标准都要有测试；核心规则要故意改错一次，确认测试会失败；合并前 `make check` 必须通过。
- 不提交密钥、`.env` 与真实个人信息；每个合并请求写一句伦理考量。

## 4. 常用命令

| 命令 | 作用 |
| --- | --- |
| `make up` / `make down` / `make reset` | 启动 / 停止 / 清空数据重来 |
| `make logs s=seat` | 看某个服务的日志（platform、seat、room、repair） |
| `make revision s=seat m="add booking"` | 改表后生成迁移 |
| `make test s=seat` | 跑某个服务的测试 |
| `make contracts` | 改了接口后导出契约并生成前端类型 |
| `make check` | 提交前检查（后端 + 前端） |
| `make help` | 全部命令 |

各服务的接口文档：platform http://127.0.0.1:8001/docs、seat :8002、room :8003、repair :8004；邮件在 Mailpit http://127.0.0.1:8025 查看。

## 5. 文档地图

| 文档 | 内容 |
| --- | --- |
| [docs/tasks.md](docs/tasks.md) | 席位、里程碑、36 张任务卡 |
| [docs/requirements/](docs/requirements/README.md) | 需求（134 条，含验收标准）与决策 Q1 ~ Q24 |
| [docs/architecture/architecture.md](docs/architecture/architecture.md) | 架构、模块边界、技术栈 |
| [docs/adr.md](docs/adr.md) | 架构决策记录（含公共层归属） |
| [docs/log.md](docs/log.md) | 过程日志 |
| [AGENTS.md](AGENTS.md) | 流程与编码规范 |
| [Pj-任务.pdf](Pj-任务.pdf) | 课程任务书 |

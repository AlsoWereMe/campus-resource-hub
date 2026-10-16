---
name: commit-convention
description: 本项目的 Git 提交规范：小步提交（一个功能一个提交）、Conventional Commits 格式、引用需求编号、末尾用 Co-Authored-By 标注参与的模型，提交前向用户发出提交申请并获确认。准备提交、拆分提交、编写提交说明，或用户说「提交」「commit」时使用。
---

# 提交规范

> 本文件与 `.claude/skills/commit-convention/SKILL.md` 内容保持一致，修改时两份同步。

任务书要求：提交历史是开发过程的主要证据；提交说明能对应任务或需求，讲清做了什么、为什么；AI 生成的变更须经人工验收后提交，避免无法审查的大批量变更。本规范把这些要求落到每一次提交。

## 1. 提交粒度：小步提交

- **一个提交只做一件事**：一个功能点（通常对应一条或少数几条需求）、一个缺陷修复、一次重构，或一次文档更新。
- 完成一个可验证的步骤就提交，不要把多个功能攒到最后一起提交。
- 不混合：功能与格式化、重构与行为变更、不同模块的无关改动，分开提交。
- 跨模块的一个功能按依赖顺序拆分：契约（`contracts/`）→ 提供方实现 → 消费方实现。
- 体量参考：单个提交的改动（不含生成文件、锁文件）尽量不超过约 400 行，超过时先考虑拆分。
- 每个提交都应能通过构建与相关测试，不提交已知会让 CI 失败的中间状态。
- 一个提交至多包含一个数据库迁移版本。

## 2. 提交申请：先确认，再提交

每次执行 `git commit` 之前，向用户发出提交申请，内容包括：

1. 将要提交的文件清单（`git status`、`git diff --stat`）；
2. 完整的提交说明；
3. 已运行的检查及结果（测试、静态检查）。

用户确认后才提交。用户在当前对话中已明确批准一组提交（含拆分方式）时，可按批准的拆分依次提交，不必逐个再问。

- 只 `git add` 本次提交涉及的文件，不用 `git add -A` 或 `git add .`。
- 不提交密钥、`.env`、本地配置、构建产物、IDE 文件。
- 提交作者是操作仓库的人（使用其 git 配置），智能代理只作为共同作者出现在说明末尾。

## 3. 提交说明格式（Conventional Commits 1.0.0）

```text
<type>(<scope>): <subject>

<body>

<footer>
```

### type

| type | 用途 |
| --- | --- |
| `feat` | 新功能 |
| `fix` | 缺陷修复 |
| `docs` | 只改文档 |
| `test` | 只增改测试 |
| `refactor` | 不改变行为的重构 |
| `perf` | 性能优化 |
| `build` | 构建系统、依赖 |
| `ci` | 流水线配置 |
| `chore` | 其他杂项（不改源码与测试） |
| `style` | 只改格式 |
| `revert` | 回退之前的提交 |

### scope

取改动所属的模块或区域，只写一个：

| scope | 范围 |
| --- | --- |
| `m1`、`m2`、`m3` | 业务模块服务 |
| `iam`、`space`、`notify`、`audit` | 公共层子模块 |
| `web` | 前端 |
| `contracts` | 接口与事件契约 |
| `gateway` | 接入层 |
| `deploy` | Compose、环境、初始化脚本 |
| `ci` | 流水线 |
| `requirements`、`architecture`、`adr` | 文档 |
| `agents` | AGENTS.md、CLAUDE.md、skill 等代理规范 |

一个提交需要写两个以上 scope 时，通常说明它应该拆分。

### subject

- 用中文动宾短语说明做了什么，如「创建预约时校验整点与时长上限」。
- 不超过 50 个汉字，末尾不加句号。
- 不兼容变更在 type 或 scope 后加 `!`，如 `feat(contracts)!: …`。

### body

- 讲清**做了什么、为什么**：关键取舍、未采用的方案、对其他模块的影响。
- 与 subject 之间空一行，适当换行。
- 纯机械改动（如改错别字）可省略 body。

### footer（按以下顺序）

| 行 | 何时必填 | 示例 |
| --- | --- | --- |
| `Refs:` | 有对应需求、业务规则或决策时 | `Refs: M1-RSV-02, BR-06` |
| `BREAKING CHANGE:` | 不兼容的接口或 schema 变更 | `BREAKING CHANGE: 占用块接口的 scope 字段改为必填` |
| `Co-Authored-By:` | 智能代理参与了本次变更时，**必须是最后一行** | `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` |

`Co-Authored-By` 如实填写本次实际参与的模型全名与其厂商约定的 noreply 邮箱；多个模型参与时各写一行。不得冒用其他模型或成员的名字。

## 4. 示例

```text
feat(m1): 创建预约时校验整点与单次时长上限

按 BR-01、BR-02 校验预约区间：起止必须为整点，时长为 1 至
m1.booking.max_hours 小时。校验放在领域层，不依赖框架，便于
单元测试与变异测试。

Refs: M1-RSV-02, BR-01, BR-02
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

```text
fix(m3): 验收不通过后保持维修下架

验收不通过时工单回到「维修中」，此前代码误调用了释放接口，导致
自习室提前恢复可约。改为不触发写回，并补充回归测试。

Refs: M3-ACC-01, BR-M3-07
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

```text
feat(contracts)!: 占用块写入接口要求显式传入作用范围

原先缺省视为整间，M3 的座位级下架容易误写成整间。改为必填，
M1 与 M2、M3 的客户端在后续提交中同步修改。

Refs: M1-INT-01, M3-WRK-02
BREAKING CHANGE: PUT /internal/m1/v1/blocks 的 scope 字段改为必填
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

## 5. 提交前检查清单

- [ ] 本次改动只包含一个功能、修复或文档主题
- [ ] 相关测试已在本地运行并通过；新行为有对应测试
- [ ] 需求文档追踪矩阵的「实现」「状态」已更新（如适用）
- [ ] 提交说明符合格式，`Refs` 与 `Co-Authored-By` 齐全
- [ ] 已向用户发出提交申请并获得确认

## 6. 禁止

- 不对已推送的提交执行 amend、rebase 或 force push。
- 不使用 `--no-verify` 跳过钩子。
- 不自行解决合并冲突：任务书规定代码冲突由人处理。
- 不在提交说明中写入密钥、令牌或个人信息。

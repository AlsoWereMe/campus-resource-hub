---
name: do-task
description: 按 docs/tasks.md 的任务卡完成一个开发任务：认领 Issue、建分支、读需求与契约、出方案并等人确认、实现与测试、更新追踪矩阵、提交并开合并请求。用户说「做任务 M1-T04」「领个任务」「继续做任务」时使用。
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(gh issue list:*), Bash(gh issue view:*), Bash(gh pr checks:*)
---

# 做任务

> 本文件与 `.agents/skills/do-task/SKILL.md` 内容保持一致，修改时两份同步。规则细节以 AGENTS.md 为准。

## 0. 确定任务

- 用户给了任务编号：直接使用。
- 没给：问用户的席位，列出该席位依赖已完成、未被认领的任务（`gh issue list --label "seat:<席位>" --state open`，结合 docs/tasks.md 的依赖），推荐第一个，让用户选。
- 已在做的任务（当前分支名含任务编号）：从上次停下的步骤继续。

## 1. 认领与建分支

```bash
gh issue list --state open --search "[<任务编号>] in:title"
gh issue edit <Issue 号> --add-assignee @me
git switch main && git pull --ff-only
git switch -c <type>/<任务编号小写>-<英文短名>
```

依赖的任务尚未完成时告诉用户：可以按契约先开发（写回经 outbox 自动重试，测试中用替身），或先换一个任务。

## 2. 读（不要跳过）

1. docs/tasks.md 中该任务卡（需求、后端文件、前端页面、要点）。
2. 卡中每个需求编号在 `docs/requirements/` 中的正文、业务规则（BR）、状态机、**验收标准**。
3. 卡中列出的接口桩文件：签名、请求 / 响应模型就是契约；以及 `contracts/` 中的对应部分。
4. 参考实现：`platform_service/iam/auth_api.py`、`platform_service/space/read_api.py`、`apps/web/src/app/(app)/account/page.tsx`；公共能力见 AGENTS.md §4.2。
5. 需要的话读同服务中已完成任务的代码，沿用其写法。

## 3. 出方案，等人确认

按下面的格式输出方案，然后**停下来等用户明确同意**。用户修改方案就按新方案执行。

```text
目标：要满足的需求编号与验收标准
影响范围：文件、表（迁移）、接口（是否改契约）、前端页面
步骤：按提交拆分，每步一句话，每步可独立验证
测试计划：验收标准 → 测试名 → 测试层级（单元 / 集成 / E2E）
候选与取舍：有多种做法时列出，并给建议
风险与待确认：需要用户决定的问题
```

方案需要改契约、其他席位的目录、`libs/common`、迁移或需求，或者需求有歧义时：先告诉用户，经同意后按 `Change request` 表单的结构开 Issue，把链接给用户，等组长在 Issue 中写出结论再继续：

```bash
gh issue create --label change --title "[change] <一句话>" --body-file <填好的正文>
# 正文各节：类型、发起席位、受影响的模块、相关需求编号与接口、问题与原因、候选方案与建议、是否兼容、结论（留空，组长填写）
```

## 4. 实现（每个步骤一个提交）

- 表：改 `infrastructure/models.py` → `make revision s=<服务> m="..."` → 检查迁移 → `make restart s=<服务>`。
- 规则写在 `domain/`（纯函数或类，便于单元测试）；用例写在 `application/`；接口桩所在文件只做参数转换并调用应用层。
- 写回、通知、审计、事件一律经 outbox；时间用 clock；参数读参数表；错误用 `RuleViolation("BR-xx", …)` 等公共错误。
- 前端：替换对应的 `page.tsx`，只调用本模块的 `api.<模块>`；参照账号页的写法处理错误。
- 每完成一步：`make test s=<服务>`（前端 `cd apps/web && pnpm test`），然后按 commit-convention 向用户发出提交申请，确认后提交。

## 5. 验证

- 每条验收标准都有通过的测试，测试名含需求编号。
- 核心规则与状态机：故意改错一处实现，确认测试失败，再改回；记下改了哪里，写进合并请求。
- 需要联调时：`make up`、`make web`，浏览器访问 http://127.0.0.1:8080，演示账号见 README；时间相关的用 `PUT /internal/test/clock`、`POST /internal/test/jobs/<name>`。
- `make check` 全部通过。

## 6. 收尾

1. 追踪矩阵：本任务涉及的需求行「实现」填合并请求链接（开 PR 后补），「状态」改为已完成；没做完的写明原因。
2. 改了接口：`make contracts`，在合并请求中说明并请消费方评审。
3. 推送并开合并请求，按 `.github/pull_request_template.md` 填写，正文含 `Closes #<Issue 号>`：

```bash
git push -u origin HEAD
gh pr create --base main --title "<type>(<scope>): <任务编号> <标题>" --body-file <填好的模板>
```

4. 等 CI 的 `backend`、`frontend` 两项检查通过（`gh pr checks --watch`）；失败就在本地复现、修复，按提交规范再提交推送。
5. 告诉用户：合并请求链接、CI 结果、需要谁评审、还有哪些未完成或待确认。

## 禁止

- 跳过第 3 步的确认直接写代码。
- 修改其他席位的目录、`libs/common`、迁移或契约而不先问。
- 需要组长决定的事只在对话里讨论，不开 `Change request` Issue。
- 自行解决合并冲突（交给人）；force push；`--no-verify`。

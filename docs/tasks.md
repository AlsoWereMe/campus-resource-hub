# 任务

> 进度看 GitHub Issues（每张任务卡一个 Issue，按席位、模块、优先级打标签）与里程碑。本文件是任务分解的基线，改动须走合并请求。
> 开工：在 agent 中输入「做任务 M1-T04」。agent 会按 `.agents/skills/do-task` 的流程认领、读文档、出方案、等你确认、实现、测试、开合并请求。

## 席位

| 席位 | 范围 | 任务 | 代码目录 |
| --- | --- | --- | --- |
| A1 | M1 预约域 | M1-T01 ~ T07 | `services/seat`、`apps/web/src/app/(app)/m1`、`…/admin/m1` |
| A2 | M1 履约域 | M1-T08 ~ T13 | 同上 |
| B1 | M2 整教室预约与审批 | M2-T01 ~ T07 | `services/room`、`…/m2`、`…/admin/m2` |
| B2 | 公共层：身份权限、审计；持续部署 | D-T01 ~ T04、X-T02 | `services/platform/…/iam`、`…/audit`、`…/admin/iam`、`…/admin/audit` |
| C1 | M3 物业报修工单 | M3-T01 ~ T06 | `services/repair`、`…/m3`、`…/admin/m3` |
| C2 | 公共层：空间、通知；会话代理 | D-T05 ~ T08、X-T01 | `services/platform/…/space`、`…/notify`、`…/admin/space`、`…/admin/notify` |

席位归属的依据与决定见 [docs/adr.md](adr.md) ADR-003。一个任务包含该功能的后端、前端与测试；别的席位的目录不要改，需要时先问。

## 里程碑与关键路径

| 里程碑 | 对应评审节点 | 任务 |
| --- | --- | --- |
| R1 | 第一次 Review：第一次迭代功能 | M1-T01 ~ T04、T08、T09；M2-T01 ~ T04；M3-T01 ~ T03；D-T01、T02、T05、T06 |
| R2 | 第二次 Review：主功能完成、集成链路打通 | M1-T05、T06、T10 ~ T13；M2-T05 ~ T07；M3-T04 ~ T06；D-T03、T04、T07、T08；X-T02 |
| R3 | 期末展示 | M1-T07、X-T01 |

**关键路径**：M1-T01（占用块）是 M2、M3 写回的落点；D-T01（按角色查用户）是 M2 审批、M3 派单的前提；D-T05（通知）让所有提醒真正发出。这三项各自席位优先做。依赖未完成时按契约先开发：写回经 outbox 会自动重试，对方实现后自然打通；测试中用假实现替身。

**已在骨架中实现**（可直接调用，也可作为写法参考）：登录 / 令牌 / 改口令 / 锁定（IAM-AUTH-01）、服务凭证与 JWKS（IAM-AUTH-03）、空间查询（`/api/space/v1/...`）、演示种子、前端登录页与账号页、CI（`.github/workflows/ci.yml`）。

---

## 任务卡

> 每张卡：席位 · 优先级 · 里程碑 · 依赖。需求编号在 `docs/requirements/` 中查正文与验收标准；接口桩在「后端」所列文件中，签名即契约。

### M1-T01 占用块与状态追溯
`A1` `P0` `R1` · 依赖：无
- 需求：M1-INT-01 ~ 04、M1-INT-06；BR-09；需求 §4.3
- 后端：`services/seat/src/seat_service/api/blocks.py`（5 个接口）
- 前端：`/admin/m1/trace`
- 要点：个人预约也写成占用块，同一座位的个人预约用 PostgreSQL 排他约束防重叠（`btree_gist` 已装在 m1）；写入、升级、释放都追加状态日志；ACTIVE 取消冲突预约并通知、不计违约。

### M1-T02 业务参数
`A1` `P0` `R1` · 依赖：无
- 需求：M1-CFG-01；参数清单见 M1 需求 §3
- 后端：`services/seat/src/seat_service/api/params.py`；参数表 + 基础种子写入默认值；提供给其他任务读取参数的函数
- 前端：`/admin/m1/settings`

### M1-T03 自习室浏览与座位检索
`A1` `P0` `R1` · 依赖：M1-T01
- 需求：M1-RSV-01、M1-SRH-01、M1-SRH-02、SPC-TAG-02（座位标记展示）；可约判定见 M1 需求 §4.2；BR-10
- 后端：`services/seat/src/seat_service/api/search.py`；房间与座位数据经服务令牌读 `/api/space/v1/...`
- 前端：`/m1/search`
- 要点：搜索 P95 < 1 秒（NFR-14），注意批量查询，避免逐个座位请求。

### M1-T04 创建、取消预约与我的预约
`A1` `P0` `R1` · 依赖：M1-T01、M1-T02
- 需求：M1-RSV-02、03、04，M1-INT-09（错误可供代理追问）；BR-01 ~ BR-11、BR-21
- 后端：`services/seat/src/seat_service/api/bookings.py`
- 前端：`/m1/search` 中的预约弹窗、`/m1/bookings`
- 要点：并发抢同一座位只有一人成功（数据库约束兜底）；Idempotency-Key；「预约成功」通知经 outbox；规则不满足用 `RuleViolation("BR-xx", …)`。

### M1-T05 历史与再次预约
`A1` `P0` `R2` · 依赖：M1-T04
- 需求：M1-HIS-01、M1-HIS-02
- 后端：`services/seat/src/seat_service/api/history.py`
- 前端：`/m1/history`
- 要点：预约中快照座位编号与自习室名称，座位注销后历史仍可显示。

### M1-T06 主数据变更处理
`A1` `P0` `R2` · 依赖：M1-T04、D-T06
- 需求：M1-INT-05；BR-19
- 后端：`services/seat/src/seat_service/consumers.py` 订阅 `space.room.updated`、`space.seats.updated`
- 要点：消息处理幂等；受影响预约系统取消并通知、不计违约。

### M1-T07 拓展功能
`A1` `P2` `R3` · 依赖：M1-T04
- 需求：M1-RSV-06、M1-SRH-03、M1-SRH-04、M1-HIS-03、M1-INT-07、M1-INT-08
- 后端：`services/seat/src/seat_service/api/extensions.py`
- 前端：签退按钮、座位图、收藏、一键报修跳转

### M1-T08 签到码与屏幕端
`A2` `P0` `R1` · 依赖：无
- 需求：M1-CHK-01、M1-CHK-02；BR-16
- 后端：`services/seat/src/seat_service/api/screen.py`
- 前端：`/screen`（全屏，无需登录，设备令牌）、`/admin/m1/screens`
- 要点：签到码用 `secrets` 生成；设备令牌只存哈希。

### M1-T09 签到（输码与扫码）
`A2` `P0` `R1` · 依赖：M1-T04、M1-T08
- 需求：M1-CHK-03、M1-CHK-04；BR-13、BR-16、BR-17
- 后端：`services/seat/src/seat_service/api/checkin.py`
- 前端：`/m1/bookings` 中的签到入口、`/checkin`（扫码落地页）

### M1-T10 提醒、超时取消与自动完成
`A2` `P0` `R2` · 依赖：M1-T04、M1-T09
- 需求：M1-REM-01 ~ 03、M1-VIO-01、M1-RSV-05；BR-12 ~ 15、BR-20
- 后端：`services/seat/src/seat_service/jobs.py`（定时任务，无接口）
- 要点：用测试端点推进时间验证（`PUT /internal/test/clock`、`POST /internal/test/jobs/<name>`）；幂等键 = 预约号 + 事件类型；重启与多实例下恰好一次。

### M1-T11 违约查询、处罚与撤销
`A2` `P0` `R2` · 依赖：M1-T10
- 需求：M1-VIO-02 ~ 04；BR-18
- 后端：`services/seat/src/seat_service/api/violations.py`
- 前端：`/m1/violations`、`/admin/m1/violations`

### M1-T12 管理员处置与补签
`A2` `P1` `R2` · 依赖：M1-T04
- 需求：M1-RSV-07、M1-CHK-05
- 后端：`services/seat/src/seat_service/api/admin_bookings.py`
- 前端：`/admin/m1/bookings` 中的操作按钮
- 要点：校验数据范围（`principal.scope(...).covers(building_id=…)`）；写审计。

### M1-T13 运营看板、统计与导出
`A2` `P0` `R2` · 依赖：M1-T04、M1-T10
- 需求：M1-OPS-01 ~ 05；指标口径见 M1-OPS-03
- 后端：`services/seat/src/seat_service/api/ops.py`
- 前端：`/admin/m1/dashboard`、`/admin/m1/bookings`
- 要点：指标用固定种子数据集 + 手算期望值写测试；学生信息默认脱敏（NFR-11）。

### M2-T01 房间检索与冲突预检
`B1` `P0` `R1` · 依赖：M1-T01（冲突预检）
- 需求：M2-ROOM-01、M2-ROOM-02、M2-INT-02
- 后端：`services/room/src/room_service/api/rooms.py`
- 前端：`/m2/rooms` 的检索部分

### M2-T02 准入校验
`B1` `P0` `R1` · 依赖：无
- 需求：M2-ELG-01 ~ 05；BR-M2-01 ~ 07、17、18
- 后端：`services/room/src/room_service/api/eligibility.py`；校验逻辑写在 domain，供 M2-T04 复用
- 要点：每项不满足都返回具体规则编号，供前端与会话代理说明。

### M2-T03 审批链与参数
`B1` `P0` `R1` · 依赖：无
- 需求：M2-FLOW-01、M2-FLOW-02、M2-APP-02；预置审批链见 M2 需求 §4.2
- 后端：`services/room/src/room_service/api/flows.py`；基础种子写入 4 条预置规则与参数默认值
- 前端：`/admin/m2/flows`

### M2-T04 提交、撤回、取消与写回
`B1` `P0` `R1` · 依赖：M2-T02、M2-T03（写回需 M1-T01，可先开发）
- 需求：M2-APP-01、03、04、05，M2-QRY-01，M2-INT-01、03；BR-M2-04、05、13 ~ 16
- 后端：`services/room/src/room_service/api/applications.py`
- 前端：`/m2/rooms` 的提交部分、`/m2/applications`
- 要点：写回一律 `outbox.call(service="seat", …, aggregate="application:<id>")`，申请详情显示 `writeback_status`。

### M2-T05 多级审批
`B1` `P0` `R2` · 依赖：M2-T04、D-T01
- 需求：M2-APV-01 ~ 06；BR-M2-08、10
- 后端：`services/room/src/room_service/api/approvals.py`
- 前端：`/m2/approvals`
- 要点：审批人按「级别角色 + 数据范围」经 D-T01 接口解析；同级并发只生效一次（行锁或条件更新）。

### M2-T06 超时撤销与提醒
`B1` `P0` `R2` · 依赖：M2-T04、M2-T05
- 需求：M2-TMO-01 ~ 03；BR-M2-11、12
- 后端：`services/room/src/room_service/jobs.py`

### M2-T07 管理、统计与外部事件
`B1` `P1` `R2` · 依赖：M2-T04
- 需求：M2-APP-06、M2-QRY-02、M2-QRY-03、M2-INT-04 ~ 06
- 后端：`services/room/src/room_service/api/admin.py`、`services/room/src/room_service/consumers.py`（`m3.workorder.repairing`、`space.room.updated`）
- 前端：`/admin/m2/applications`

### M3-T01 故障上报、取消与我的报修
`C1` `P0` `R1` · 依赖：无
- 需求：M3-RPT-01、03、04，M3-QRY-01；BR-M3-01 ~ 03、09、13
- 后端：`services/repair/src/repair_service/api/reports.py`；基础种子写入故障类别
- 前端：`/m3/report`（位置级联用已实现的 `/api/space/v1/...`）、`/m3/mine`

### M3-T02 派单、改派、退回与关闭
`C1` `P0` `R1` · 依赖：M3-T01、D-T01
- 需求：M3-DSP-01 ~ 05；BR-M3-15
- 后端：`services/repair/src/repair_service/api/dispatch.py`
- 前端：`/m3/workbench` 中的派单操作

### M3-T03 维修过程与下架写回
`C1` `P0` `R1` · 依赖：M3-T02（写回需 M1-T01，可先开发）
- 需求：M3-WRK-01 ~ 04、M3-INT-01 ~ 03；BR-M3-06 ~ 08
- 后端：`services/repair/src/repair_service/api/repair.py`
- 前端：`/m3/workbench` 中的维修操作
- 要点：写回经 `outbox.call(service="seat", …, aggregate="workorder:<id>")`；两张维修中工单的场景要有测试。

### M3-T04 验收与评价
`C1` `P0` `R2` · 依赖：M3-T03
- 需求：M3-ACC-01 ~ 04；BR-M3-10 ~ 12
- 后端：`services/repair/src/repair_service/api/acceptance.py`、`services/repair/src/repair_service/jobs.py`（自动验收）
- 前端：`/m3/mine` 中的验收评价

### M3-T05 时限与超时升级
`C1` `P0` `R2` · 依赖：M3-T01
- 需求：M3-ESC-01 ~ 04；BR-M3-04、05、16
- 后端：`services/repair/src/repair_service/api/sla.py`、`services/repair/src/repair_service/jobs.py`（升级扫描）
- 前端：`/admin/m3/settings`

### M3-T06 工作台、统计、附件与事件
`C1` `P1` `R2` · 依赖：M3-T02
- 需求：M3-QRY-02 ~ 04、M3-RPT-02、M3-RPT-05、M3-INT-04 ~ 06
- 后端：`services/repair/src/repair_service/api/workbench.py`、`services/repair/src/repair_service/consumers.py`；附件存挂载卷（决策 Q24）
- 前端：`/m3/workbench`、`/admin/m3/stats`

### D-T01 按角色与范围查询用户
`B2` `P0` `R1` · 依赖：无
- 需求：IAM-USER-02
- 后端：`services/platform/src/platform_service/iam/query_api.py`
- 要点：M2 审批、M3 派单都依赖它，优先完成。

### D-T02 用户、院系与账号管理
`B2` `P0` `R1` · 依赖：无
- 需求：IAM-AUTH-02、IAM-USER-01
- 后端：`services/platform/src/platform_service/iam/users_api.py`
- 前端：`/admin/iam/users`
- 要点：CSV 导入全部校验通过才写入；停用账号立即吊销刷新令牌。

### D-T03 角色、权限点与授权
`B2` `P0` `R2` · 依赖：D-T02
- 需求：IAM-ROLE-01 ~ 04
- 后端：`services/platform/src/platform_service/iam/roles_api.py`；权限点清单来自 `campus_common/contracts/permissions.py`
- 前端：`/admin/iam/roles`

### D-T04 操作审计
`B2` `P0` `R2` · 依赖：无
- 需求：AUD-01、AUD-02
- 后端：`services/platform/src/platform_service/audit/api.py`、`services/platform/src/platform_service/consumers.py`（订阅 `audit.record`）、`audit` schema 中的表
- 前端：`/admin/audit`

### D-T05 通知服务
`C2` `P0` `R1` · 依赖：无
- 需求：NTF-01 ~ 04；各模块事件清单见 D 需求 §4
- 后端：`services/platform/src/platform_service/notify/api.py`、`services/platform/src/platform_service/consumers.py`（订阅 `notify.send`）、`services/platform/src/platform_service/jobs.py`（重试）
- 前端：`/inbox`、`/admin/notify`
- 要点：按幂等键只投递一次；dev / test 的邮件可在 Mailpit（http://127.0.0.1:8025）中查看。

### D-T06 房间与自习开放管理
`C2` `P0` `R1` · 依赖：无
- 需求：SPC-ROOM-01、02、04、05、06，SPC-EVT-01（房间事件）
- 后端：`services/platform/src/platform_service/space/rooms_admin.py`；变更后经 outbox 发布 `space.room.updated`
- 前端：`/admin/space/rooms`
- 要点：关闭、停用前用 M1 可用性接口给出影响预览。

### D-T07 开放时间与闭馆日
`C2` `P0` `R2` · 依赖：D-T06
- 需求：SPC-ROOM-03；BR-22
- 后端：`services/platform/src/platform_service/space/hours_admin.py`
- 前端：`/admin/space/rooms` 中的开放时间设置

### D-T08 座位与标记管理
`C2` `P0` `R2` · 依赖：D-T06
- 需求：SPC-SEAT-01 ~ 03、SPC-TAG-01、SPC-EVT-01（座位事件）
- 后端：`services/platform/src/platform_service/space/seats_admin.py`
- 前端：`/admin/space/seats`

### X-T01 会话代理插件（附加项）
`C2` `P2` `R3` · 依赖：各模块 P0 接口
- 需求：需求总览 §5；任务书第五节
- 代码：`agent-plugin/`（新建）；只调公开接口，用 `contracts/` 生成客户端
- 要点：意图不明确时按接口返回的 `FIELD_REQUIRED`、`RULE_VIOLATION` 追问；安装与配置纳入流水线。

### X-T02 持续部署：镜像、test 部署、发布与回滚
`B2` `P0` `R2` · 依赖：无
- 需求：NFR-02 ~ 06、NFR-13；任务书「交付流水线」；架构 §8；ADR-014
- 代码：`.github/workflows/`（新增部署工作流；`ci.yml` 已由组长完成，其两项必过检查不改名）、`deploy/`
- 要点：
  - 镜像：合并 main 后构建四个服务（`deploy/service.Dockerfile`）与前端（Nginx 托管静态文件）的镜像，tag = 提交 SHA，推送 GHCR；`/version` 与前端页脚显示版本号、SHA、构建时间。
  - test：CI 通过后部署，顺序为迁移 → D → M1 → M2 / M3 → 前端，每步健康检查通过才继续；用并发组做部署锁，部署后跑 E2E（`apps/web/e2e`），跑完才释放。
  - prod：推送版本标签触发，经 GitHub Environments 人工审批，晋升同一镜像；另建「部署指定标签」工作流用于回滚。
  - 部署目标：服务器到位前，部署到 Actions runner 上的临时环境（Compose 起全栈，跑完即销毁），完整演示上述流程；服务器到位后只换部署目标（SSH + Secrets），工作流结构不变。

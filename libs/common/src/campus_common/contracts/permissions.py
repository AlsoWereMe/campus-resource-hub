"""权限点与预置角色（IAM-ROLE-01、02；各模块需求文档附录 A）。

- 权限点由代码定义，管理员只能把它们组合成角色；
- 预置角色由 IAM 的基础种子写入数据库；default_scope 是授予该角色时的默认数据范围；
- 服务凭证的权限见 SERVICE_CLIENTS。
"""

from dataclasses import dataclass
from typing import Literal

PERMISSIONS: dict[str, str] = {
    # 公共层 D
    "iam:user:manage": "用户、批量导入、停用",
    "iam:role:manage": "角色、权限、授权与数据范围",
    "iam:user:query": "按角色与范围查询用户（服务）",
    "space:read": "查看校区、楼宇、房间、座位",
    "space:room:manage": "维护房间、自习开放、开放时间、整间预约属性",
    "space:seat:manage": "维护座位、停用与恢复",
    "space:tag:manage": "维护标记字典、为座位打标记",
    "notify:template:manage": "维护通知模板",
    "notify:delivery:view": "查看通知投递记录",
    "audit:log:view": "查询审计记录",
    # M1 自习座位预约
    "m1:seat:search": "浏览自习室、搜索座位、查看时间轴",
    "m1:booking:create": "创建预约",
    "m1:booking:cancel-own": "取消本人预约",
    "m1:booking:view-own": "查看本人预约与历史",
    "m1:checkin:do": "签到、签退",
    "m1:violation:view-own": "查看本人违约",
    "m1:booking:view-all": "查看范围内预约明细",
    "m1:booking:cancel-any": "处置范围内预约",
    "m1:checkin:manual": "管理员补签",
    "m1:violation:view-all": "查看范围内违约",
    "m1:violation:revoke": "撤销违约",
    "m1:stats:view": "运营看板与统计",
    "m1:stats:export": "导出明细与统计",
    "m1:screen:manage": "生成、吊销屏幕设备令牌",
    "m1:trace:view": "座位状态来源追溯",
    "m1:setting:manage": "修改 M1 业务参数",
    "m1:block:write": "写入、释放占用块（服务）",
    "m1:violation:summary": "查询学生违约摘要（服务）",
    # M2 整教室预约与审批
    "m2:room:search": "检索可申请房间、查看占用日历",
    "m2:application:create": "提交整间申请",
    "m2:application:manage-own": "查看、撤回、取消本人申请",
    "m2:approval:act": "审批（受级别角色与数据范围约束）",
    "m2:application:view-all": "查看范围内全部申请",
    "m2:application:revoke": "撤销已通过的申请",
    "m2:flow:manage": "维护审批链与 M2 参数",
    "m2:writeback:retry": "手动重试写回",
    "m2:stats:view": "M2 统计",
    # M3 物业报修工单
    "m3:workorder:create": "上报故障",
    "m3:workorder:manage-own": "查看、取消、验收、评价本人工单",
    "m3:dispatch:act": "派单、改派、关闭、代验收、调整影响范围",
    "m3:repair:act": "开始维修、进度备注、完工、退回、调整影响范围",
    "m3:workorder:view-all": "查看范围内全部工单",
    "m3:escalation:handle": "处理升级工单",
    "m3:stats:view": "M3 统计",
    "m3:config:manage": "维护故障类别与处理时限",
    "m3:writeback:retry": "手动重试写回",
}

SERVICE_ONLY = {"iam:user:query", "m1:block:write", "m1:violation:summary"}

ScopeType = Literal["ALL", "BUILDING", "DEPARTMENT", "SELF"]


@dataclass(frozen=True)
class RoleSpec:
    code: str
    name: str
    description: str
    permissions: tuple[str, ...]
    default_scope: ScopeType


_STUDENT_M1 = (
    "m1:seat:search",
    "m1:booking:create",
    "m1:booking:cancel-own",
    "m1:booking:view-own",
    "m1:checkin:do",
    "m1:violation:view-own",
)
_REPORTER = ("m3:workorder:create", "m3:workorder:manage-own")
_APPLICANT = ("m2:room:search", "m2:application:create", "m2:application:manage-own")

PRESET_ROLES: tuple[RoleSpec, ...] = (
    RoleSpec(
        "student", "学生", "预约座位、签到、报修", ("space:read", *_STUDENT_M1, *_REPORTER), "SELF"
    ),
    RoleSpec("staff", "教职工", "整间申请、报修", ("space:read", *_APPLICANT, *_REPORTER), "SELF"),
    RoleSpec(
        "student_leader",
        "学生组织负责人",
        "由系统管理员授予学生，可提交整间申请",
        _APPLICANT,
        "SELF",
    ),
    RoleSpec(
        "dept_approver",
        "院系审批人",
        "审批与本院系相关的整间申请级别",
        ("space:read", "m2:room:search", "m2:approval:act"),
        "DEPARTMENT",
    ),
    RoleSpec(
        "room_admin",
        "教室管理员",
        "管理范围内的自习室与座位，处理异常预约，审批范围内房间的整间申请",
        (
            "space:read",
            "space:room:manage",
            "space:seat:manage",
            "space:tag:manage",
            "m1:seat:search",
            "m1:booking:view-all",
            "m1:booking:cancel-any",
            "m1:checkin:manual",
            "m1:violation:view-all",
            "m1:violation:revoke",
            "m1:stats:view",
            "m1:screen:manage",
            "m1:trace:view",
            "m2:room:search",
            "m2:approval:act",
            "m2:application:view-all",
            "notify:delivery:view",
        ),
        "BUILDING",
    ),
    RoleSpec(
        "resource_admin",
        "资源管理员",
        "整间申请校级终审，可撤销已通过的申请",
        (
            "space:read",
            "m2:room:search",
            "m2:approval:act",
            "m2:application:view-all",
            "m2:application:revoke",
            "m2:stats:view",
        ),
        "ALL",
    ),
    RoleSpec(
        "ops_admin",
        "运营管理员",
        "只读查看预约情况与统计",
        (
            "space:read",
            "m1:seat:search",
            "m1:booking:view-all",
            "m1:violation:view-all",
            "m1:stats:view",
            "m1:stats:export",
            "m1:trace:view",
            "notify:delivery:view",
        ),
        "ALL",
    ),
    RoleSpec(
        "dispatcher",
        "物业调度员",
        "受理派单、改派、关闭、代验收",
        ("space:read", *_REPORTER, "m3:dispatch:act", "m3:workorder:view-all"),
        "BUILDING",
    ),
    RoleSpec(
        "technician",
        "维修人员",
        "处理派给自己的工单",
        ("space:read", *_REPORTER, "m3:repair:act"),
        "BUILDING",
    ),
    RoleSpec(
        "property_supervisor",
        "物业主管",
        "升级工单的接收人，查看全部工单与统计",
        (
            "space:read",
            *_REPORTER,
            "m3:dispatch:act",
            "m3:workorder:view-all",
            "m3:escalation:handle",
            "m3:stats:view",
        ),
        "ALL",
    ),
    RoleSpec(
        "sys_admin",
        "系统管理员",
        "管理全部配置、角色、权限、用户；不可删除",
        tuple(p for p in PERMISSIONS if p not in SERVICE_ONLY),
        "ALL",
    ),
)

# 服务凭证可用的权限点（IAM-AUTH-03）
SERVICE_CLIENTS: dict[str, tuple[str, ...]] = {
    "platform": ("space:read",),
    "seat": ("space:read", "iam:user:query"),
    "room": ("space:read", "iam:user:query", "m1:block:write", "m1:violation:summary"),
    "repair": ("space:read", "iam:user:query", "m1:block:write"),
}

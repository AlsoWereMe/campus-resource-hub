"""M2 多个任务共用的接口模型。修改即修改契约（AGENTS.md「契约先行」）。"""

import datetime as dt
from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import Field

from campus_common.models import ApiModel

API = "/api/m2/v1"

WritebackStatus = Literal["NONE", "SYNCING", "SYNCED", "FAILED"]


class ApplicationStatus(StrEnum):
    PENDING = "PENDING"  # 审批中（第 k 级）
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    EXPIRED = "EXPIRED"  # 超时撤销
    CANCELLED = "CANCELLED"
    REVOKED = "REVOKED"  # 资源管理员撤销
    COMPLETED = "COMPLETED"


class ScopeFrom(StrEnum):
    """审批人数据范围的取法。"""

    APPLICANT_DEPARTMENT = "APPLICANT_DEPARTMENT"  # 申请人所在院系
    ROOM_SCOPE = "ROOM_SCOPE"  # 房间所在楼宇或归属院系
    ALL = "ALL"


class ApprovalLevel(ApiModel):
    level: int = Field(ge=1)
    role: str = Field(description="审批角色，如 dept_approver、room_admin、resource_admin")
    scope_from: ScopeFrom


class ApprovalRecord(ApiModel):
    level: int
    approver_id: int
    approver_name: str
    action: Literal["APPROVE", "REJECT", "TRANSFER"]
    comment: str | None
    at: datetime


class ApplicationCreate(ApiModel):
    room_id: int
    date: dt.date
    start_hour: int = Field(ge=0, le=23, description="整点（BR-M2-01）")
    hours: int = Field(ge=1, le=24, description="实际上限取参数 m2.max_duration_hours")
    title: str = Field(min_length=1, max_length=50, description="活动名称")
    purpose: str = Field(min_length=1, max_length=500)
    attendees: int = Field(ge=1, description="预计人数，不得超过房间容量（BR-M2-06）")
    contact_name: str | None = Field(None, max_length=50, description="默认本人")
    contact_phone: str | None = Field(None, max_length=32)
    remark: str | None = Field(None, max_length=500)


class ApplicationOut(ApiModel):
    id: int
    room_id: int
    room_code: str
    room_name: str
    building_name: str
    starts_at: datetime
    ends_at: datetime
    title: str
    purpose: str
    attendees: int
    contact_name: str
    contact_phone: str | None
    remark: str | None
    applicant_id: int
    applicant_name: str
    status: ApplicationStatus
    current_level: int | None = Field(description="审批中时的当前级别")
    deadline: datetime | None = Field(description="当前级别的审批截止时刻（BR-M2-11）")
    chain: list[ApprovalLevel] = Field(description="提交时固化的审批链快照（M2-APP-02）")
    records: list[ApprovalRecord]
    writeback: WritebackStatus = Field(description="在 M1 中的占用同步状态（M2-INT-03）")
    created_at: datetime

"""M3 多个任务共用的接口模型。修改即修改契约（AGENTS.md「契约先行」）。"""

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import Field

from campus_common.models import ApiModel

API = "/api/m3/v1"

WritebackStatus = Literal["NONE", "SYNCING", "SYNCED", "FAILED"]


class WorkOrderStatus(StrEnum):
    SUBMITTED = "SUBMITTED"  # 待受理
    ASSIGNED = "ASSIGNED"  # 已派单
    IN_REPAIR = "IN_REPAIR"  # 维修中（写回 M1 下架）
    PENDING_ACCEPTANCE = "PENDING_ACCEPTANCE"  # 待验收（保持下架）
    COMPLETED = "COMPLETED"  # 已完成（释放）
    CANCELLED = "CANCELLED"
    CLOSED = "CLOSED"  # 调度员关闭


class Urgency(StrEnum):
    NORMAL = "NORMAL"
    URGENT = "URGENT"


class ImpactScope(StrEnum):
    ROOM = "ROOM"
    SEATS = "SEATS"


class Stage(StrEnum):
    ACCEPT = "ACCEPT"  # 受理：提交 → 派单
    RESPOND = "RESPOND"  # 响应：派单 → 开始维修
    REPAIR = "REPAIR"  # 修复：开始维修 → 完工


class AttachmentOut(ApiModel):
    id: int
    file_name: str
    url: str
    uploaded_at: datetime


class TimelineEntry(ApiModel):
    at: datetime
    actor_id: str
    actor_name: str
    action: str = Field(description="如 SUBMIT、ASSIGN、START、NOTE、COMPLETE、ESCALATE、ACCEPT")
    detail: str | None = None


class WorkOrderOut(ApiModel):
    id: int
    building_id: int
    building_name: str
    room_id: int | None
    room_name: str | None
    seat_id: int | None
    seat_code: str | None
    category_code: str
    category_name: str
    urgency: Urgency
    description: str
    contact_phone: str | None
    reporter_id: int
    reporter_name: str
    assignee_id: int | None
    assignee_name: str | None
    status: WorkOrderStatus
    stage: Stage | None
    stage_deadline: datetime | None = Field(description="当前处理阶段的截止时刻（BR-M3-04）")
    escalation_level: int = Field(description="0 未升级；1 已通知调度员；2 已通知物业主管")
    impact_scope: ImpactScope | None
    impact_seat_ids: list[int]
    resolution: str | None
    rating: int | None
    comment: str | None
    attachments: list[AttachmentOut]
    timeline: list[TimelineEntry]
    writeback: WritebackStatus = Field(description="在 M1 中的下架同步状态（M3-INT-03）")
    created_at: datetime


class WorkOrderBrief(ApiModel):
    id: int
    room_name: str | None
    category_name: str
    status: WorkOrderStatus
    created_at: datetime


class ReasonIn(ApiModel):
    reason: str = Field(min_length=1, max_length=200)

"""消息契约（路由键 → 消息体），经 RabbitMQ 交换机 domain.events 传递。

发布方经 Outbox 发布；订阅方用对应模型校验消息体，并按 message_id 幂等处理。
"""

from datetime import datetime
from typing import Any, Literal

from pydantic import Field

from campus_common.contracts.space import RoomInfo, SeatInfo
from campus_common.models import ApiModel

Channel = Literal["email", "inbox"]


def _all_channels() -> list[Channel]:
    return ["email", "inbox"]


class NotifySend(ApiModel):
    """notify.send：请通知服务给某个用户发通知（NTF-01）。"""

    idempotency_key: str = Field(description="同一键只投递一次，如 m1:booking:123:remind-before")
    recipient_user_id: int
    event: str = Field(description="事件类型，决定模板，如 m1.booking.reminder")
    summary: str = Field(description="无模板时直接使用的通知正文")
    variables: dict[str, Any] = Field(default_factory=dict, description="模板变量")
    channels: list[Channel] = Field(default_factory=_all_channels)


class AuditRecord(ApiModel):
    """audit.record：一条操作审计（AUD-01）。"""

    actor_type: Literal["user", "service", "system"]
    actor_id: str
    actor_name: str | None = None
    action: str = Field(description="如 m1.setting.update、m2.application.approve")
    target_type: str
    target_id: str
    before: dict[str, Any] | None = None
    after: dict[str, Any] | None = None
    result: Literal["success", "failure"] = "success"
    occurred_at: datetime
    trace_id: str | None = None


class SpaceRoomUpdated(ApiModel):
    """space.room.updated：房间任何属性变化后发布完整快照（SPC-EVT-01）。"""

    room: RoomInfo
    changed_fields: list[str]


class SpaceSeatsUpdated(ApiModel):
    """space.seats.updated：座位状态、标记等变化后发布受影响座位的快照（SPC-EVT-01）。"""

    room_id: int
    seats: list[SeatInfo]
    changed_fields: list[str]


class WorkOrderEvent(ApiModel):
    """m3.workorder.repairing / completed / closed（M3-INT-04）。"""

    work_order_id: int
    status: str
    building_id: int
    room_id: int | None
    impact_scope: Literal["ROOM", "SEATS"] | None
    seat_ids: list[int] = Field(default_factory=list)
    occurred_at: datetime


EVENTS: dict[str, type[ApiModel]] = {
    "notify.send": NotifySend,
    "audit.record": AuditRecord,
    "space.room.updated": SpaceRoomUpdated,
    "space.seats.updated": SpaceSeatsUpdated,
    "m3.workorder.repairing": WorkOrderEvent,
    "m3.workorder.completed": WorkOrderEvent,
    "m3.workorder.closed": WorkOrderEvent,
}

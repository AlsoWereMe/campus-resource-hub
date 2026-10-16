"""M1 对外提供的内部接口模型：占用块与可用性查询（M1-INT-01 ~ 04、07；M2、M3 消费）。"""

from datetime import datetime
from enum import StrEnum

from pydantic import Field

from campus_common.models import ApiModel


class BlockSource(StrEnum):
    M1_BOOKING = "M1_BOOKING"
    M2_ROOM_BOOKING = "M2_ROOM_BOOKING"
    M3_REPAIR = "M3_REPAIR"
    ADMIN = "ADMIN"


class BlockKind(StrEnum):
    HOLD = "HOLD"  # 预占：阻止新预约，不影响已有预约
    ACTIVE = "ACTIVE"  # 生效：阻止新预约，并取消冲突的已有预约


class BlockScope(StrEnum):
    ROOM = "ROOM"
    SEATS = "SEATS"


class BlockUpsert(ApiModel):
    """PUT /internal/m1/v1/blocks/{source}/{sourceRef}：以「来源 + 来源单号」幂等。"""

    scope: BlockScope
    room_id: int
    seat_ids: list[int] = Field(default_factory=list, description="scope=SEATS 时必填")
    starts_at: datetime
    ends_at: datetime | None = Field(None, description="为空表示直到释放，仅 M3_REPAIR、ADMIN 允许")
    kind: BlockKind = BlockKind.ACTIVE
    reason: str = Field(max_length=200)


class BlockResult(ApiModel):
    block_id: int
    source: BlockSource
    source_ref: str
    kind: BlockKind
    cancelled_booking_ids: list[int] = Field(
        default_factory=list, description="因本次写入被系统取消的个人预约（不含学生身份）"
    )


class BlockBrief(ApiModel):
    source: BlockSource
    source_ref: str
    kind: BlockKind
    scope: BlockScope
    starts_at: datetime
    ends_at: datetime | None


class RoomAvailability(ApiModel):
    """GET /internal/m1/v1/rooms/{roomId}/availability（M1-INT-04）。"""

    room_id: int
    starts_at: datetime
    ends_at: datetime
    blocks: list[BlockBrief]
    conflicting_booking_count: int


class ViolationSummary(ApiModel):
    """GET /internal/m1/v1/users/{userId}/violation-summary（M1-INT-07）。"""

    user_id: int
    window_days: int
    count: int
    suspended_until: datetime | None

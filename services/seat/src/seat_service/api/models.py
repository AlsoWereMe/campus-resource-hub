"""M1 多个任务共用的接口模型。修改即修改契约（AGENTS.md「契约先行」）。"""

import datetime as dt
from datetime import datetime
from enum import StrEnum

from pydantic import Field

from campus_common.contracts.m1 import BlockSource
from campus_common.models import ApiModel

API = "/api/m1/v1"
INTERNAL = "/internal/m1/v1"


class BookingStatus(StrEnum):
    PENDING = "PENDING"  # 待签到
    CHECKED_IN = "CHECKED_IN"  # 已签到
    COMPLETED = "COMPLETED"  # 已完成
    CANCELLED = "CANCELLED"  # 本人取消
    NO_SHOW = "NO_SHOW"  # 违约取消
    REVOKED = "REVOKED"  # 系统取消（维修下架 / 整间占用 / 管理员）


class CheckinMethod(StrEnum):
    CODE = "CODE"
    SCAN = "SCAN"
    MANUAL = "MANUAL"


class SlotState(StrEnum):
    """座位在某时段对当前学生的状态，按 §4.2 的优先级取第一个命中项。"""

    CLOSED = "CLOSED"  # 不开放
    DISABLED = "DISABLED"  # 停用
    REPAIR = "REPAIR"  # 维修下架
    ROOM_OCCUPIED = "ROOM_OCCUPIED"  # 整间占用
    BOOKED = "BOOKED"  # 已被预约（不暴露预约人）
    AVAILABLE = "AVAILABLE"


class SlotQuery(ApiModel):
    date: dt.date | None = Field(None, description="默认今天（业务时区）")
    start_hour: int | None = Field(None, ge=0, le=23, description="默认最近可约整点")
    hours: int = Field(1, ge=1, le=12)


class BookingOut(ApiModel):
    id: int
    seat_id: int
    seat_code: str
    room_id: int
    room_name: str
    building_name: str
    starts_at: datetime
    ends_at: datetime
    status: BookingStatus
    created_at: datetime
    checkin_opens_at: datetime = Field(description="签到窗口开启时刻（BR-13）")
    checkin_deadline: datetime = Field(description="签到截止时刻 T0 + 15 分钟（BR-12、13）")
    checked_in_at: datetime | None = None
    checkin_method: CheckinMethod | None = None
    cancelled_at: datetime | None = None
    cancel_reason: str | None = None
    cancel_source: BlockSource | None = Field(None, description="系统取消时的写入来源")
    cancel_source_ref: str | None = None


class SeatResult(ApiModel):
    seat_id: int
    code: str
    tags: list[str]
    state: SlotState

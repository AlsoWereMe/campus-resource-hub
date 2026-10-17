"""任务 M2-T01：可申请房间检索、占用日历与冲突预检（M2-ROOM-01、02，M2-INT-02）。"""

import datetime as dt
from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Query
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.contracts.m1 import BlockBrief
from campus_common.contracts.space import RoomType
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel, Page, PageQuery
from room_service.api.models import API

TASK = "M2-T01"

router = APIRouter(prefix=API, tags=["M2 · 房间"])


class SlotQuery(ApiModel):
    date: dt.date
    start_hour: int = Field(ge=0, le=23)
    hours: int = Field(ge=1, le=24)


class RoomSearchQuery(PageQuery):
    date: dt.date | None = None
    start_hour: int | None = Field(None, ge=0, le=23)
    hours: int | None = Field(None, ge=1, le=24)
    building_id: int | None = None
    room_type: RoomType | None = None
    min_capacity: int | None = Field(None, ge=1, description="预计人数")


class ApplicableRoom(ApiModel):
    room_id: int
    code: str
    name: str
    building_name: str
    room_type: RoomType
    capacity: int
    facilities: list[str]
    opening_hours: str
    applicable: bool = Field(description="所选时段是否可申请")
    reason: str | None = Field(
        None, description="不可申请的原因：已有申请 / 维修下架 / 不在开放时间"
    )


class CalendarItem(ApiModel):
    starts_at: datetime
    ends_at: datetime | None
    kind: Literal["APPLICATION", "REPAIR", "PERSONAL_BOOKINGS"]
    status: str | None = Field(None, description="整间申请的状态；不显示申请人")
    count: int | None = Field(None, description="个人预约数量")


class CalendarQuery(ApiModel):
    date_from: dt.date
    date_to: dt.date


class ConflictPreview(ApiModel):
    personal_booking_count: int = Field(description="审批通过后将被取消的个人预约数")
    blocks: list[BlockBrief]
    can_submit: bool
    reason: str | None = None


@router.get(
    "/rooms",
    summary="可申请房间检索（M2-ROOM-01）",
    description="只返回申请人有资格申请的可整间预约房间（BR-M2-17），并说明不可申请的原因。",
)
async def search_rooms(
    q: Annotated[RoomSearchQuery, Query()], _: Principal = require("m2:room:search")
) -> Page[ApplicableRoom]:
    raise NotImplementedYet(TASK)


@router.get("/rooms/{room_id}/calendar", summary="房间占用日历（M2-ROOM-02，P1）")
async def room_calendar(
    room_id: int, q: Annotated[CalendarQuery, Query()], _: Principal = require("m2:room:search")
) -> list[CalendarItem]:
    raise NotImplementedYet(TASK)


@router.get(
    "/rooms/{room_id}/conflicts",
    summary="冲突预检（M2-INT-02）",
    description="调用 M1 可用性查询。提交前查询失败则不可提交；审批页查询失败只提示。",
)
async def room_conflicts(
    room_id: int, q: Annotated[SlotQuery, Query()], _: Principal = require("m2:room:search")
) -> ConflictPreview:
    raise NotImplementedYet(TASK)

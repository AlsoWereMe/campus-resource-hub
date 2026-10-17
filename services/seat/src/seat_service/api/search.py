"""任务 M1-T03：自习室浏览与座位检索（M1-RSV-01、M1-SRH-01、02；可约判定见需求 §4.2）。"""

import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Query
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.contracts.space import RoomType
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel, Page, PageQuery
from seat_service.api.models import API, SeatResult, SlotQuery, SlotState

TASK = "M1-T03"

router = APIRouter(prefix=API, tags=["M1 · 检索"])


class RoomBrowseQuery(SlotQuery):
    campus_id: int | None = None
    building_id: int | None = None
    room_type: RoomType | None = None


class RoomBrowseItem(ApiModel):
    room_id: int
    code: str
    name: str
    building_name: str
    room_type: RoomType
    department_id: int | None
    opening_hours: str = Field(description="当日开放时间，如 08:00-22:00；不开放为空串")
    total_seats: int
    available_seats: int = Field(description="所选时段内按 §4.2 可约的座位数")
    tag_counts: dict[str, int] = Field(description="各标记的座位数")


class SeatSearchQuery(SlotQuery, PageQuery):
    campus_id: int | None = None
    building_id: int | None = None
    room_id: int | None = None
    room_type: RoomType | None = None
    tags: list[str] | None = Field(None, description="多选须全部满足")
    any_outlet: bool = Field(False, description="快捷条件：有插座（任一类型）")
    only_available: bool = True
    keyword: str | None = Field(None, max_length=50, description="自习室名称或座位编号")


class RoomSeats(ApiModel):
    room_id: int
    room_code: str
    room_name: str
    building_name: str
    available_count: int
    seats: list[SeatResult]


class TimelineSlot(ApiModel):
    hour: int
    state: SlotState


class SeatTimeline(ApiModel):
    seat_id: int
    seat_code: str
    date: dt.date
    slots: list[TimelineSlot]


class TimelineQuery(ApiModel):
    date: dt.date | None = None


@router.get(
    "/rooms",
    summary="浏览可用自习室（M1-RSV-01）",
    description="只返回学生可见（院系专属仅本院系，BR-10）、已开放的自习室。",
)
async def browse_rooms(
    q: Annotated[RoomBrowseQuery, Query()], _: Principal = require("m1:seat:search")
) -> list[RoomBrowseItem]:
    raise NotImplementedYet(TASK)


@router.get(
    "/seats/search",
    summary="条件搜索座位（M1-SRH-01）",
    description="结果按自习室分组；标记多选须全部满足；P95 < 1 秒（NFR-14）。",
)
async def search_seats(
    q: Annotated[SeatSearchQuery, Query()], _: Principal = require("m1:seat:search")
) -> Page[RoomSeats]:
    raise NotImplementedYet(TASK)


@router.get(
    "/seats/{seat_id}/timeline",
    summary="座位当日各整点时段状态（M1-SRH-02）",
    description="不显示他人身份，只给状态类别。",
)
async def seat_timeline(
    seat_id: int,
    q: Annotated[TimelineQuery, Query()],
    _: Principal = require("m1:seat:search"),
) -> SeatTimeline:
    raise NotImplementedYet(TASK)

"""任务 M1-T05：历史与再次预约（M1-HIS-01、02）。"""

import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Query
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel, Page, PageQuery
from seat_service.api.models import API, BookingOut, BookingStatus

TASK = "M1-T05"

router = APIRouter(prefix=API, tags=["M1 · 历史"])


class HistoryQuery(PageQuery):
    status: list[BookingStatus] | None = None
    date_from: dt.date | None = None
    date_to: dt.date | None = None


class RebookHint(ApiModel):
    booking_id: int
    seat_id: int
    seat_code: str
    room_name: str
    seat_usable: bool = Field(description="座位仍存在、启用且本人有权预约")
    reason: str | None = Field(None, description="不可用的原因，如「座位已注销」")


@router.get(
    "/bookings/history",
    summary="历史预约（M1-HIS-01）",
    description="按时间倒序分页；已注销座位仍显示当时的编号与自习室名称。",
)
async def booking_history(
    q: Annotated[HistoryQuery, Query()], _: Principal = require("m1:booking:view-own")
) -> Page[BookingOut]:
    raise NotImplementedYet(TASK)


@router.get(
    "/bookings/{booking_id}/rebook",
    summary="再次预约该座位前的检查（M1-HIS-02）",
    description="前端据此预填座位；座位不可用时给出原因并引导回搜索。",
)
async def rebook_hint(booking_id: int, _: Principal = require("m1:booking:view-own")) -> RebookHint:
    raise NotImplementedYet(TASK)

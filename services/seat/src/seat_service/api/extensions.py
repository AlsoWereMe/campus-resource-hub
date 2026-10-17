"""任务 M1-T07：拓展功能（P2）。

签退、座位图、替代推荐、收藏、违约摘要（M1-RSV-06、SRH-03、04、HIS-03、INT-07）。
"""

from typing import Annotated

from fastapi import APIRouter, Query, Response

from campus_common.auth import Principal, require
from campus_common.contracts.m1 import ViolationSummary
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel
from seat_service.api.models import API, INTERNAL, BookingOut, SeatResult, SlotQuery

TASK = "M1-T07"

router = APIRouter(prefix=API, tags=["M1 · 拓展（P2）"])
internal = APIRouter(prefix=INTERNAL, tags=["M1 · 内部接口"])


class SeatMapCell(ApiModel):
    row: int
    col: int
    seat: SeatResult


class SeatMap(ApiModel):
    room_id: int
    rows: int
    cols: int
    cells: list[SeatMapCell]


class FavoriteSeat(ApiModel):
    seat_id: int
    seat_code: str
    room_id: int
    room_name: str


class SummaryQuery(ApiModel):
    days: int = 30


@router.post(
    "/bookings/{booking_id}/checkout",
    summary="提前签退（M1-RSV-06）",
    description="自下一个整点起释放剩余时段，状态为已完成（提前签退）。",
)
async def checkout(booking_id: int, _: Principal = require("m1:checkin:do")) -> BookingOut:
    raise NotImplementedYet(TASK)


@router.get("/rooms/{room_id}/seat-map", summary="座位图（M1-SRH-03）")
async def seat_map(
    room_id: int, q: Annotated[SlotQuery, Query()], _: Principal = require("m1:seat:search")
) -> SeatMap:
    raise NotImplementedYet(TASK)


@router.get("/seats/{seat_id}/alternatives", summary="替代推荐：同室同标记的可约座位（M1-SRH-04）")
async def alternatives(
    seat_id: int, q: Annotated[SlotQuery, Query()], _: Principal = require("m1:seat:search")
) -> list[SeatResult]:
    raise NotImplementedYet(TASK)


@router.get("/favorites", summary="我的常用座位（M1-HIS-03）")
async def favorites(_: Principal = require("m1:booking:view-own")) -> list[FavoriteSeat]:
    raise NotImplementedYet(TASK)


@router.put("/favorites/{seat_id}", status_code=204, summary="收藏座位（M1-HIS-03）")
async def add_favorite(seat_id: int, _: Principal = require("m1:booking:view-own")) -> Response:
    raise NotImplementedYet(TASK)


@router.delete("/favorites/{seat_id}", status_code=204, summary="取消收藏（M1-HIS-03）")
async def remove_favorite(seat_id: int, _: Principal = require("m1:booking:view-own")) -> Response:
    raise NotImplementedYet(TASK)


@internal.get(
    "/users/{user_id}/violation-summary",
    summary="学生近期违约摘要（M1-INT-07，供 M2 准入门槛）",
)
async def violation_summary(
    user_id: int,
    q: Annotated[SummaryQuery, Query()],
    _: Principal = require("m1:violation:summary"),
) -> ViolationSummary:
    raise NotImplementedYet(TASK)

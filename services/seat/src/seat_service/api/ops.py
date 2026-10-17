"""任务 M1-T13：运营看板、预约明细、统计与导出（M1-OPS-01 ~ 05；指标口径见需求 M1-OPS-03）。"""

import datetime as dt
from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Query, Response
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel, Page, PageQuery
from seat_service.api.models import API, BookingOut, BookingStatus

TASK = "M1-T13"

router = APIRouter(prefix=f"{API}/admin", tags=["M1 · 运营"])


class RoomLive(ApiModel):
    room_id: int
    room_name: str
    building_name: str
    total: int
    unavailable: int
    booked_not_checked_in: int
    checked_in: int
    free: int


class Dashboard(ApiModel):
    at: datetime
    rooms: list[RoomLive]


class DashboardQuery(ApiModel):
    building_id: int | None = None


class AdminBooking(BookingOut):
    user_id: int
    student_no_masked: str = Field(description="运营管理员默认看到脱敏学号（NFR-11）")
    student_name: str | None = Field(None, description="无查看完整信息的权限时为空")


class AdminBookingQuery(PageQuery):
    date_from: dt.date
    date_to: dt.date
    building_id: int | None = None
    room_id: int | None = None
    status: list[BookingStatus] | None = None


class StatsQuery(ApiModel):
    date_from: dt.date
    date_to: dt.date
    building_id: int | None = None
    room_id: int | None = None


class Stats(ApiModel):
    open_seat_hours: float
    booking_rate: float
    usage_rate: float
    checkin_rate: float
    no_show_rate: float
    daily_turnover: float
    heatmap: list[list[float]] = Field(description="7 × 24：星期 × 整点 的预约率")


class RoomFlag(ApiModel):
    room_id: int
    room_name: str
    kind: Literal["LOW_USAGE", "TIGHT"]
    value: float


@router.get("/dashboard", summary="实时看板（M1-OPS-01）", description="数据延迟 ≤ 1 分钟。")
async def dashboard(
    q: Annotated[DashboardQuery, Query()], _: Principal = require("m1:stats:view")
) -> Dashboard:
    raise NotImplementedYet(TASK)


@router.get("/bookings", summary="预约明细（M1-OPS-02）")
async def admin_bookings(
    q: Annotated[AdminBookingQuery, Query()], _: Principal = require("m1:booking:view-all")
) -> Page[AdminBooking]:
    raise NotImplementedYet(TASK)


@router.get("/stats", summary="统计指标（M1-OPS-03）")
async def stats(
    q: Annotated[StatsQuery, Query()], _: Principal = require("m1:stats:view")
) -> Stats:
    raise NotImplementedYet(TASK)


@router.get("/stats/flags", summary="低利用率与紧张自习室（M1-OPS-04）")
async def stats_flags(
    q: Annotated[StatsQuery, Query()], _: Principal = require("m1:stats:view")
) -> list[RoomFlag]:
    raise NotImplementedYet(TASK)


@router.get(
    "/export/bookings.csv",
    summary="导出预约明细 CSV（M1-OPS-05）",
    response_class=Response,
    responses={200: {"content": {"text/csv": {}}}},
)
async def export_bookings(
    q: Annotated[AdminBookingQuery, Query()], _: Principal = require("m1:stats:export")
) -> Response:
    raise NotImplementedYet(TASK)


@router.get(
    "/export/stats.csv",
    summary="导出统计 CSV（M1-OPS-05）",
    response_class=Response,
    responses={200: {"content": {"text/csv": {}}}},
)
async def export_stats(
    q: Annotated[StatsQuery, Query()], _: Principal = require("m1:stats:export")
) -> Response:
    raise NotImplementedYet(TASK)

"""任务 M1-T04：创建、取消预约与我的预约（M1-RSV-02、03、04；BR-01 ~ BR-11、BR-21）。"""

import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Header
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel
from seat_service.api.models import API, BookingOut

TASK = "M1-T04"

router = APIRouter(prefix=API, tags=["M1 · 预约"])


class BookingCreate(ApiModel):
    seat_id: int
    date: dt.date
    start_hour: int = Field(ge=0, le=23, description="整点（BR-01）")
    hours: int = Field(ge=1, le=12, description="实际上限取参数 m1.booking.max_hours（BR-02）")


@router.post(
    "/bookings",
    status_code=201,
    summary="创建预约（M1-RSV-02）",
    description="按 BR-01 ~ BR-10 与暂停状态校验；规则不满足返回 RULE_VIOLATION 并给出规则编号；"
    "同一 Idempotency-Key 只产生一条预约；并发抢同一座位只有一人成功。",
)
async def create_booking(
    body: BookingCreate,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
    _: Principal = require("m1:booking:create"),
) -> BookingOut:
    raise NotImplementedYet(TASK)


@router.get("/bookings/current", summary="我的当前与即将开始的预约（M1-RSV-04）")
async def current_bookings(_: Principal = require("m1:booking:view-own")) -> list[BookingOut]:
    raise NotImplementedYet(TASK)


@router.get("/bookings/{booking_id}", summary="预约详情（本人）")
async def get_booking(booking_id: int, _: Principal = require("m1:booking:view-own")) -> BookingOut:
    raise NotImplementedYet(TASK)


@router.post(
    "/bookings/{booking_id}/cancel",
    summary="取消预约（M1-RSV-03）",
    description="签到截止前可取消「待签到」预约，不计违约，座位立即释放（BR-11）。",
)
async def cancel_booking(
    booking_id: int, _: Principal = require("m1:booking:cancel-own")
) -> BookingOut:
    raise NotImplementedYet(TASK)

"""任务 M1-T09：签到——输码与扫码（M1-CHK-03、04；BR-13、16、17）。"""

from typing import Annotated

from fastapi import APIRouter, Query
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel
from seat_service.api.models import API, BookingOut, CheckinMethod

TASK = "M1-T09"

router = APIRouter(prefix=API, tags=["M1 · 签到"])


class CheckinIn(ApiModel):
    code: str = Field(min_length=6, max_length=6)
    method: CheckinMethod = Field(CheckinMethod.CODE, description="CODE 输码 / SCAN 扫码")


class CandidateQuery(ApiModel):
    room_id: int


@router.get(
    "/checkin/candidate",
    summary="扫码后找到本人在该室处于签到窗口内的预约（M1-CHK-04）",
    description="没有时返回 null，前端提示原因并给出「去预约」入口。",
)
async def checkin_candidate(
    q: Annotated[CandidateQuery, Query()], _: Principal = require("m1:checkin:do")
) -> BookingOut | None:
    raise NotImplementedYet(TASK)


@router.post(
    "/bookings/{booking_id}/checkin",
    summary="签到（M1-CHK-03、04）",
    description="校验：本人、待签到、在窗口内（BR-13）、码属于该室且有效（BR-16）、"
    "10 分钟内输错不超过 5 次（BR-17）。",
)
async def checkin(
    booking_id: int, body: CheckinIn, _: Principal = require("m1:checkin:do")
) -> BookingOut:
    raise NotImplementedYet(TASK)

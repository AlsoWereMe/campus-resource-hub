"""任务 M1-T12：管理员处置预约与补签（M1-RSV-07、M1-CHK-05；BR-19）。"""

from fastapi import APIRouter
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel
from seat_service.api.models import API, BookingOut

TASK = "M1-T12"

router = APIRouter(prefix=f"{API}/admin", tags=["M1 · 管理员处置"])


class ReasonIn(ApiModel):
    reason: str = Field(min_length=1, max_length=200)


@router.post(
    "/bookings/{booking_id}/cancel",
    summary="管理员取消预约（M1-RSV-07）",
    description="限数据范围内；通知学生、不计违约、写入审计。",
)
async def admin_cancel(
    booking_id: int, body: ReasonIn, _: Principal = require("m1:booking:cancel-any")
) -> BookingOut:
    raise NotImplementedYet(TASK)


@router.post("/bookings/{booking_id}/checkin", summary="管理员补签（M1-CHK-05，P2）")
async def admin_checkin(
    booking_id: int, body: ReasonIn, _: Principal = require("m1:checkin:manual")
) -> BookingOut:
    raise NotImplementedYet(TASK)

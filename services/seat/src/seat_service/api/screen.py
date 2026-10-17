"""任务 M1-T08：签到码与屏幕端（M1-CHK-01、02；BR-16）。"""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Header, Query
from pydantic import Field

from campus_common.auth import PUBLIC, Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel
from seat_service.api.models import API

TASK = "M1-T08"

router = APIRouter(prefix=API, tags=["M1 · 签到码与屏幕端"])


class ScreenCode(ApiModel):
    room_id: int
    room_name: str
    code: str = Field(description="6 位，去除易混字符，安全随机生成")
    qr_url: str = Field(description="扫码签到网址，含房间与签到码参数")
    valid_until: datetime
    refresh_seconds: int = Field(description="屏幕轮询间隔，换码后 30 秒内可见")


class ScreenDevice(ApiModel):
    id: int
    room_id: int
    name: str
    created_at: datetime
    revoked_at: datetime | None


class ScreenDeviceCreated(ScreenDevice):
    token: str = Field(description="设备令牌，只在创建时返回一次")


class ScreenDeviceCreate(ApiModel):
    room_id: int
    name: str = Field(max_length=50)


class ScreenQuery(ApiModel):
    room_id: int | None = None


@router.get(
    "/screen/code",
    dependencies=[PUBLIC],
    summary="屏幕端获取当前签到码（M1-CHK-02）",
    description="用请求头 X-Device-Token 鉴权；设备令牌只能取绑定自习室的码，吊销后被拒绝。",
)
async def screen_code(
    device_token: Annotated[str, Header(alias="X-Device-Token")],
) -> ScreenCode:
    raise NotImplementedYet(TASK)


@router.get("/admin/screens", summary="屏幕终端列表")
async def list_screens(
    q: Annotated[ScreenQuery, Query()], _: Principal = require("m1:screen:manage")
) -> list[ScreenDevice]:
    raise NotImplementedYet(TASK)


@router.post("/admin/screens", status_code=201, summary="为自习室生成屏幕设备令牌")
async def create_screen(
    body: ScreenDeviceCreate, _: Principal = require("m1:screen:manage")
) -> ScreenDeviceCreated:
    raise NotImplementedYet(TASK)


@router.post("/admin/screens/{device_id}/revoke", summary="吊销屏幕设备令牌")
async def revoke_screen(device_id: int, _: Principal = require("m1:screen:manage")) -> ScreenDevice:
    raise NotImplementedYet(TASK)

"""任务 M2-T07：申请管理、撤销与统计（M2-APP-06，M2-QRY-02、03）。"""

import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Query
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel, Page, PageQuery
from room_service.api.models import API, ApplicationOut, ApplicationStatus

TASK = "M2-T07"

router = APIRouter(prefix=f"{API}/admin", tags=["M2 · 管理"])


class AdminApplicationQuery(PageQuery):
    status: list[ApplicationStatus] | None = None
    room_id: int | None = None
    applicant_id: int | None = None
    date_from: dt.date | None = None
    date_to: dt.date | None = None


class RevokeIn(ApiModel):
    reason: str = Field(min_length=1, max_length=200)


class StatsQuery(ApiModel):
    date_from: dt.date
    date_to: dt.date


class RoomStats(ApiModel):
    room_id: int
    room_name: str
    month: str
    submitted: int
    approval_rate: float
    avg_approval_hours: float
    expired_rate: float


@router.get("/applications", summary="范围内全部申请（M2-QRY-02）")
async def list_applications(
    q: Annotated[AdminApplicationQuery, Query()],
    _: Principal = require("m2:application:view-all"),
) -> Page[ApplicationOut]:
    raise NotImplementedYet(TASK)


@router.post(
    "/applications/{application_id}/revoke",
    summary="撤销已通过的申请（M2-APP-06）",
    description="理由必填、写入审计；释放占用并通知申请人。",
)
async def revoke_application(
    application_id: int, body: RevokeIn, _: Principal = require("m2:application:revoke")
) -> ApplicationOut:
    raise NotImplementedYet(TASK)


@router.get("/stats", summary="申请统计（M2-QRY-03，P2）")
async def stats(
    q: Annotated[StatsQuery, Query()], _: Principal = require("m2:stats:view")
) -> list[RoomStats]:
    raise NotImplementedYet(TASK)

"""任务 M1-T11：违约查询、处罚与撤销（M1-VIO-02 ~ 04；BR-18）。"""

import datetime as dt
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Query
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel, Page, PageQuery
from seat_service.api.models import API

TASK = "M1-T11"

router = APIRouter(prefix=API, tags=["M1 · 违约"])


class ViolationOut(ApiModel):
    id: int
    booking_id: int
    user_id: int
    student_no_masked: str = Field(description="脱敏学号，如 2621****32（NFR-11）")
    room_name: str
    seat_code: str
    starts_at: datetime
    ends_at: datetime
    occurred_at: datetime
    reason: str
    revoked_at: datetime | None = None
    revoke_reason: str | None = None


class Suspension(ApiModel):
    active: bool
    until: datetime | None
    recent_count: int
    threshold: int
    window_days: int


class MyViolations(ApiModel):
    records: list[ViolationOut]
    suspension: Suspension


class ViolationQuery(PageQuery):
    user_id: int | None = None
    room_id: int | None = None
    date_from: dt.date | None = None
    date_to: dt.date | None = None


class RevokeIn(ApiModel):
    reason: str = Field(min_length=1, max_length=200)


@router.get("/violations/mine", summary="我的违约与处罚状态（M1-VIO-02）")
async def my_violations(_: Principal = require("m1:violation:view-own")) -> MyViolations:
    raise NotImplementedYet(TASK)


@router.get("/admin/violations", summary="范围内违约查询（M1-VIO-02）")
async def list_violations(
    q: Annotated[ViolationQuery, Query()], _: Principal = require("m1:violation:view-all")
) -> Page[ViolationOut]:
    raise NotImplementedYet(TASK)


@router.post(
    "/admin/violations/{violation_id}/revoke",
    summary="撤销违约（M1-VIO-04）",
    description="原因必填、写入审计；撤销后重新计算处罚状态。",
)
async def revoke_violation(
    violation_id: int, body: RevokeIn, _: Principal = require("m1:violation:revoke")
) -> ViolationOut:
    raise NotImplementedYet(TASK)

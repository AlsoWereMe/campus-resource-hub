"""任务 M2-T04：提交、撤回、取消与写回 M1（M2-APP-01、03、04、05，M2-QRY-01，M2-INT-01、03）。

写回映射（BR-M2-14）：提交 → HOLD；终审通过 → ACTIVE；驳回、撤回、超时撤销、取消、撤销 → 释放。
一律经 outbox 调用 M1 /internal/m1/v1/blocks（见 docs/requirements/README.md §4.3）。
"""

from typing import Annotated

from fastapi import APIRouter, Header, Query

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import Page, PageQuery
from room_service.api.models import API, ApplicationCreate, ApplicationOut, ApplicationStatus

TASK = "M2-T04"

router = APIRouter(prefix=API, tags=["M2 · 申请"])


class MyApplicationsQuery(PageQuery):
    status: list[ApplicationStatus] | None = None


@router.post(
    "/applications",
    status_code=201,
    summary="提交整间申请（M2-APP-01）",
    description="准入校验（M2-T02）→ 冲突校验（BR-M2-04、05）→ 匹配并固化审批链 → 写回 HOLD → "
    "通知第 1 级审批人。同一 Idempotency-Key 只产生一条申请。",
)
async def submit_application(
    body: ApplicationCreate,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
    _: Principal = require("m2:application:create"),
) -> ApplicationOut:
    raise NotImplementedYet(TASK)


@router.get("/applications/mine", summary="我的申请（M2-QRY-01）")
async def my_applications(
    q: Annotated[MyApplicationsQuery, Query()],
    _: Principal = require("m2:application:manage-own"),
) -> Page[ApplicationOut]:
    raise NotImplementedYet(TASK)


@router.get(
    "/applications/{application_id}",
    summary="申请详情：审批时间线、截止时刻、写回状态（M2-APV-04）",
)
async def get_application(
    application_id: int, _: Principal = require("m2:application:manage-own")
) -> ApplicationOut:
    raise NotImplementedYet(TASK)


@router.post("/applications/{application_id}/withdraw", summary="撤回审批中的申请（M2-APP-03）")
async def withdraw_application(
    application_id: int, _: Principal = require("m2:application:manage-own")
) -> ApplicationOut:
    raise NotImplementedYet(TASK)


@router.post(
    "/applications/{application_id}/cancel",
    summary="取消已通过、未开始的申请（M2-APP-04）",
    description="释放占用；被 M1 取消的个人预约不恢复。开始后不能取消（BR-M2-13）。",
)
async def cancel_application(
    application_id: int, _: Principal = require("m2:application:manage-own")
) -> ApplicationOut:
    raise NotImplementedYet(TASK)


@router.post(
    "/admin/applications/{application_id}/writeback/retry",
    summary="手动重试失败的写回（M2-INT-03）",
)
async def retry_writeback(
    application_id: int, _: Principal = require("m2:writeback:retry")
) -> ApplicationOut:
    raise NotImplementedYet(TASK)

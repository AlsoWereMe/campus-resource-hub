"""任务 M2-T05：多级审批（M2-APV-01 ~ 06；BR-M2-08、10）。

审批人按「级别角色 + 数据范围」确定，不只看权限点；同一级并发操作只生效一次。
"""

from typing import Annotated

from fastapi import APIRouter, Query
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel, Page, PageQuery
from room_service.api.models import API, ApplicationOut

TASK = "M2-T05"

router = APIRouter(prefix=API, tags=["M2 · 审批"])


class ApproveIn(ApiModel):
    comment: str | None = Field(None, max_length=200)


class RejectIn(ApiModel):
    reason: str = Field(min_length=1, max_length=200, description="驳回理由必填（BR-M2-10）")


class TransferIn(ApiModel):
    to_user_id: int


@router.get(
    "/approvals/pending",
    summary="待我审批（M2-APV-01）",
    description="按截止时刻升序；不含本人提交的申请与本人已审批过的申请（M2-APV-05）。",
)
async def pending_approvals(
    q: Annotated[PageQuery, Query()], _: Principal = require("m2:approval:act")
) -> Page[ApplicationOut]:
    raise NotImplementedYet(TASK)


@router.get("/approvals/done", summary="我已审批")
async def done_approvals(
    q: Annotated[PageQuery, Query()], _: Principal = require("m2:approval:act")
) -> Page[ApplicationOut]:
    raise NotImplementedYet(TASK)


@router.post(
    "/applications/{application_id}/approve",
    summary="通过当前级别（M2-APV-02）",
    description="有下一级则进入下一级并通知；末级通过则写回 ACTIVE 并通知申请人。",
)
async def approve(
    application_id: int, body: ApproveIn, _: Principal = require("m2:approval:act")
) -> ApplicationOut:
    raise NotImplementedYet(TASK)


@router.post("/applications/{application_id}/reject", summary="驳回（M2-APV-03）")
async def reject(
    application_id: int, body: RejectIn, _: Principal = require("m2:approval:act")
) -> ApplicationOut:
    raise NotImplementedYet(TASK)


@router.post("/applications/{application_id}/transfer", summary="转交同级审批人（M2-APV-06，P2）")
async def transfer(
    application_id: int, body: TransferIn, _: Principal = require("m2:approval:act")
) -> ApplicationOut:
    raise NotImplementedYet(TASK)

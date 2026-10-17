"""任务 M3-T04：验收与评价（M3-ACC-01 ~ 04；BR-M3-10 ~ 12）。"""

from fastapi import APIRouter
from pydantic import Field, model_validator

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel
from repair_service.api.models import API, ReasonIn, WorkOrderOut

TASK = "M3-T04"

router = APIRouter(prefix=API, tags=["M3 · 验收"])


class AcceptIn(ApiModel):
    passed: bool
    reason: str | None = Field(None, max_length=200, description="不通过时必填（BR-M3-10）")
    rating: int | None = Field(None, ge=1, le=5, description="通过时可评 1 ~ 5 星（BR-M3-12）")
    comment: str | None = Field(None, max_length=500)

    @model_validator(mode="after")
    def reason_required_when_rejected(self) -> "AcceptIn":
        if not self.passed and not self.reason:
            raise ValueError("验收不通过须填写原因")
        return self


@router.post(
    "/workorders/{work_order_id}/accept",
    summary="验收与评价（M3-ACC-01、02）",
    description="通过：已完成并释放下架；不通过：回到维修中，修复时限重新计算。评价只能提交一次。",
)
async def accept(
    work_order_id: int, body: AcceptIn, _: Principal = require("m3:workorder:manage-own")
) -> WorkOrderOut:
    raise NotImplementedYet(TASK)


@router.post(
    "/workorders/{work_order_id}/accept-on-behalf", summary="调度员代验收（M3-ACC-04，P1）"
)
async def accept_on_behalf(
    work_order_id: int, body: ReasonIn, _: Principal = require("m3:dispatch:act")
) -> WorkOrderOut:
    raise NotImplementedYet(TASK)

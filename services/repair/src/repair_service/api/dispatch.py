"""任务 M3-T02：受理派单、改派、退回、关闭（M3-DSP-01 ~ 05；BR-M3-15）。"""

from typing import Annotated

from fastapi import APIRouter, Query
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel
from repair_service.api.models import API, ReasonIn, Urgency, WorkOrderOut

TASK = "M3-T02"

router = APIRouter(prefix=API, tags=["M3 · 派单"])


class TechnicianLoad(ApiModel):
    user_id: int
    name: str
    open_count: int = Field(description="在办工单数")


class TechnicianQuery(ApiModel):
    building_id: int


class AssignIn(ApiModel):
    technician_id: int
    category_code: str | None = None
    urgency: Urgency | None = None


class ReassignIn(ApiModel):
    technician_id: int
    reason: str = Field(min_length=1, max_length=200)


class WorkOrderPatch(ApiModel):
    category_code: str | None = None
    urgency: Urgency | None = None


@router.get(
    "/technicians",
    summary="范围覆盖该楼宇的维修人员及在办数（M3-DSP-01）",
    description="人员来自 IAM-USER-02（按角色与范围查询用户）。",
)
async def technicians(
    q: Annotated[TechnicianQuery, Query()], _: Principal = require("m3:dispatch:act")
) -> list[TechnicianLoad]:
    raise NotImplementedYet(TASK)


@router.post("/workorders/{work_order_id}/assign", summary="受理并派单（M3-DSP-01）")
async def assign(
    work_order_id: int, body: AssignIn, _: Principal = require("m3:dispatch:act")
) -> WorkOrderOut:
    raise NotImplementedYet(TASK)


@router.post(
    "/workorders/{work_order_id}/reassign",
    summary="改派（M3-DSP-02）",
    description="已派单、维修中可改派；不影响下架状态与当前阶段截止时刻。",
)
async def reassign(
    work_order_id: int, body: ReassignIn, _: Principal = require("m3:dispatch:act")
) -> WorkOrderOut:
    raise NotImplementedYet(TASK)


@router.post("/workorders/{work_order_id}/return", summary="维修人员退回工单（M3-DSP-03，P1）")
async def return_work_order(
    work_order_id: int, body: ReasonIn, _: Principal = require("m3:repair:act")
) -> WorkOrderOut:
    raise NotImplementedYet(TASK)


@router.post(
    "/workorders/{work_order_id}/close",
    summary="关闭无效、重复或无需维修的工单（M3-DSP-05）",
    description="若在维修中则同时释放 M1 下架。",
)
async def close(
    work_order_id: int, body: ReasonIn, _: Principal = require("m3:dispatch:act")
) -> WorkOrderOut:
    raise NotImplementedYet(TASK)


@router.patch(
    "/workorders/{work_order_id}",
    summary="调整类别或紧急程度（M3-DSP-01、M3-ESC-03）",
)
async def patch_work_order(
    work_order_id: int, body: WorkOrderPatch, _: Principal = require("m3:dispatch:act")
) -> WorkOrderOut:
    raise NotImplementedYet(TASK)

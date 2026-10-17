"""任务 M3-T01：故障上报、取消与我的报修（M3-RPT-01、03、04，M3-QRY-01；BR-M3-01 ~ 03、09、13）。"""

from typing import Annotated

from fastapi import APIRouter, Header, Query
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel, Page, PageQuery
from repair_service.api.models import (
    API,
    Urgency,
    WorkOrderBrief,
    WorkOrderOut,
    WorkOrderStatus,
)

TASK = "M3-T01"

router = APIRouter(prefix=API, tags=["M3 · 上报"])


class Category(ApiModel):
    code: str
    name: str


class WorkOrderCreate(ApiModel):
    building_id: int
    room_id: int | None = Field(None, description="可选，含公共区域")
    seat_id: int | None = Field(None, description="可选，须属于所选房间（BR-M3-01）")
    category_code: str
    urgency: Urgency = Urgency.NORMAL
    description: str = Field(min_length=10, max_length=500)
    contact_phone: str | None = Field(None, max_length=32)


class MyWorkOrdersQuery(PageQuery):
    status: list[WorkOrderStatus] | None = None


class DuplicateQuery(ApiModel):
    room_id: int
    category_code: str


@router.get("/categories", summary="故障类别字典（BR-M3-02）")
async def categories(_: Principal = require("m3:workorder:create")) -> list[Category]:
    raise NotImplementedYet(TASK)


@router.get(
    "/workorders/duplicates",
    summary="同房间同类别的未关闭工单，上报前提示可能重复（M3-RPT-03，P1）",
)
async def duplicates(
    q: Annotated[DuplicateQuery, Query()], _: Principal = require("m3:workorder:create")
) -> list[WorkOrderBrief]:
    raise NotImplementedYet(TASK)


@router.post(
    "/workorders",
    status_code=201,
    summary="故障上报（M3-RPT-01）",
    description="状态为待受理，计算受理截止，通知范围内调度员。同一 Idempotency-Key 只产生一张工单。",
)
async def report(
    body: WorkOrderCreate,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
    _: Principal = require("m3:workorder:create"),
) -> WorkOrderOut:
    raise NotImplementedYet(TASK)


@router.get("/workorders/mine", summary="我的报修（M3-QRY-01）")
async def my_work_orders(
    q: Annotated[MyWorkOrdersQuery, Query()], _: Principal = require("m3:workorder:manage-own")
) -> Page[WorkOrderOut]:
    raise NotImplementedYet(TASK)


@router.get("/workorders/{work_order_id}", summary="工单详情与时间线（M3-QRY-01）")
async def get_work_order(
    work_order_id: int, _: Principal = require("m3:workorder:manage-own")
) -> WorkOrderOut:
    raise NotImplementedYet(TASK)


@router.post(
    "/workorders/{work_order_id}/cancel",
    summary="取消工单（M3-RPT-04）",
    description="只能在待受理、已派单时取消；维修中只能由调度员关闭（BR-M3-09）。",
)
async def cancel(
    work_order_id: int, _: Principal = require("m3:workorder:manage-own")
) -> WorkOrderOut:
    raise NotImplementedYet(TASK)

"""任务 M3-T06：工单工作台、统计、按位置查历史、图片附件（M3-QRY-02 ~ 04，M3-RPT-02）。"""

import datetime as dt
from typing import Annotated, Literal

from fastapi import APIRouter, Query, Response, UploadFile

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel, Page, PageQuery
from repair_service.api.models import (
    API,
    AttachmentOut,
    Urgency,
    WorkOrderBrief,
    WorkOrderOut,
    WorkOrderStatus,
)

TASK = "M3-T06"

router = APIRouter(prefix=API, tags=["M3 · 工作台与统计"])


class WorkbenchQuery(PageQuery):
    status: list[WorkOrderStatus] | None = None
    category_code: str | None = None
    building_id: int | None = None
    urgency: Urgency | None = None
    escalated: bool | None = None
    assigned_to_me: bool = False


class StatsQuery(ApiModel):
    date_from: dt.date
    date_to: dt.date
    group_by: Literal["building", "category", "technician"] = "building"


class StatsRow(ApiModel):
    key: str
    total: int
    avg_accept_minutes: float
    avg_respond_minutes: float
    avg_repair_minutes: float
    sla_rate: float
    avg_rating: float | None


@router.get(
    "/workorders",
    summary="工单工作台（M3-QRY-02）",
    description="调度员看范围内、维修人员看 assignedToMe、物业主管看全部；已升级的置顶。",
)
async def workbench(
    q: Annotated[WorkbenchQuery, Query()], _: Principal = require("m3:workorder:create")
) -> Page[WorkOrderOut]:
    raise NotImplementedYet(TASK)


@router.get("/admin/stats", summary="工单统计（M3-QRY-03，P1）")
async def stats(
    q: Annotated[StatsQuery, Query()], _: Principal = require("m3:stats:view")
) -> list[StatsRow]:
    raise NotImplementedYet(TASK)


@router.get("/admin/rooms/{room_id}/workorders", summary="按房间查历史工单（M3-QRY-04，P1）")
async def room_history(
    room_id: int, _: Principal = require("m3:workorder:view-all")
) -> list[WorkOrderBrief]:
    raise NotImplementedYet(TASK)


@router.post(
    "/workorders/{work_order_id}/attachments",
    status_code=201,
    summary="上传图片附件（M3-RPT-02，P1）",
    description="每张工单至多 3 张，每张 ≤ 5 MB，仅 jpg / png（BR-M3-14）；文件存挂载卷（决策 Q24）。",
)
async def upload_attachment(
    work_order_id: int, file: UploadFile, _: Principal = require("m3:workorder:create")
) -> AttachmentOut:
    raise NotImplementedYet(TASK)


@router.get(
    "/attachments/{attachment_id}",
    summary="下载图片附件（M3-RPT-02）",
    response_class=Response,
    responses={200: {"content": {"image/jpeg": {}, "image/png": {}}}},
)
async def download_attachment(
    attachment_id: int, _: Principal = require("m3:workorder:create")
) -> Response:
    raise NotImplementedYet(TASK)

"""任务 M3-T03：维修过程与下架写回（M3-WRK-01 ~ 04，M3-INT-01 ~ 03；BR-M3-06 ~ 08）。

进入维修中 → 经 outbox 调用 M1 PUT /internal/m1/v1/blocks/M3_REPAIR/{工单号}（ACTIVE，无结束时间）；
验收通过或维修中关闭 → DELETE 同一占用块。
"""

from fastapi import APIRouter
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel
from repair_service.api.models import API, ImpactScope, WorkOrderOut

TASK = "M3-T03"

router = APIRouter(prefix=API, tags=["M3 · 维修"])


class ImpactIn(ApiModel):
    impact_scope: ImpactScope = ImpactScope.ROOM
    seat_ids: list[int] = Field(default_factory=list, description="impact_scope=SEATS 时必填")


class NoteIn(ApiModel):
    content: str = Field(min_length=1, max_length=500)


class CompleteIn(ApiModel):
    resolution: str = Field(min_length=1, max_length=500, description="处理说明必填")
    attachment_ids: list[int] = Field(default_factory=list)


@router.post(
    "/workorders/{work_order_id}/start",
    summary="开始维修，写回下架（M3-WRK-01、M3-INT-01）",
    description="影响范围默认整间（决策 Q7）；只有定位到房间的工单才写回。",
)
async def start(
    work_order_id: int, body: ImpactIn, _: Principal = require("m3:repair:act")
) -> WorkOrderOut:
    raise NotImplementedYet(TASK)


@router.put("/workorders/{work_order_id}/impact", summary="调整影响范围（M3-WRK-02，P1）")
async def change_impact(
    work_order_id: int, body: ImpactIn, _: Principal = require("m3:repair:act")
) -> WorkOrderOut:
    raise NotImplementedYet(TASK)


@router.post("/workorders/{work_order_id}/notes", summary="追加进度备注（M3-WRK-03，P1）")
async def add_note(
    work_order_id: int, body: NoteIn, _: Principal = require("m3:repair:act")
) -> WorkOrderOut:
    raise NotImplementedYet(TASK)


@router.post(
    "/workorders/{work_order_id}/complete",
    summary="完工提交（M3-WRK-04）",
    description="进入待验收；下架保持到验收通过（BR-M3-07）。",
)
async def complete(
    work_order_id: int, body: CompleteIn, _: Principal = require("m3:repair:act")
) -> WorkOrderOut:
    raise NotImplementedYet(TASK)


@router.post(
    "/admin/workorders/{work_order_id}/writeback/retry",
    summary="手动重试失败的写回（M3-INT-03）",
)
async def retry_writeback(
    work_order_id: int, _: Principal = require("m3:writeback:retry")
) -> WorkOrderOut:
    raise NotImplementedYet(TASK)

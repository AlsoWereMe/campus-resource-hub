"""任务 D-T07：开放时间与闭馆日（SPC-ROOM-03；BR-22）。变更后发布 space.room.updated。"""

import datetime as dt

from fastapi import APIRouter, Response
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.contracts.space import OpeningRule
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel
from platform_service.space.rooms_admin import ImpactPreview

TASK = "D-T07"

router = APIRouter(prefix="/api/space/v1", tags=["空间 · 开放时间"])


class OpeningHoursIn(ApiModel):
    rules: list[OpeningRule] = Field(description="起止必须为整点，同一天的区间不得重叠")
    confirm: bool = Field(False, description="缩短导致冲突时先预览，确认后执行")


class ClosureIn(ApiModel):
    date: dt.date
    reason: str = Field(max_length=200)


class ClosureOut(ClosureIn):
    id: int


@router.put(
    "/rooms/{room_id}/opening-hours",
    summary="设置按星期的开放时间（SPC-ROOM-03）",
    description="非整点被拒绝（BR-22）；缩短开放时间时按 SPC-ROOM-02 的确认流程处理受影响预约。",
)
async def set_opening_hours(
    room_id: int, body: OpeningHoursIn, _: Principal = require("space:room:manage")
) -> ImpactPreview:
    raise NotImplementedYet(TASK)


@router.get("/rooms/{room_id}/closures", summary="闭馆日列表（P1）")
async def list_closures(room_id: int, _: Principal = require("space:read")) -> list[ClosureOut]:
    raise NotImplementedYet(TASK)


@router.post("/rooms/{room_id}/closures", status_code=201, summary="新增闭馆日（P1）")
async def add_closure(
    room_id: int, body: ClosureIn, _: Principal = require("space:room:manage")
) -> ClosureOut:
    raise NotImplementedYet(TASK)


@router.delete(
    "/rooms/{room_id}/closures/{closure_id}", status_code=204, summary="删除闭馆日（P1）"
)
async def delete_closure(
    room_id: int, closure_id: int, _: Principal = require("space:room:manage")
) -> Response:
    raise NotImplementedYet(TASK)

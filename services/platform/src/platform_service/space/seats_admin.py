"""任务 D-T08：座位与标记管理（SPC-SEAT-01 ~ 03，SPC-TAG-01，SPC-EVT-01）。

座位状态、标记变更后经 outbox 发布 space.seats.updated；停用、注销前先返回影响预览。
"""

from fastapi import APIRouter, UploadFile
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.contracts.space import SeatInfo, Status
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel
from platform_service.space.read_api import TagOut
from platform_service.space.rooms_admin import ImpactPreview

TASK = "D-T08"

router = APIRouter(prefix="/api/space/v1", tags=["空间 · 座位与标记"])


class SeatIn(ApiModel):
    room_id: int
    code: str = Field(max_length=48, description="全局唯一，建议「房间编号-序号」")
    row: int | None = None
    col: int | None = None
    tags: list[str] = Field(default_factory=list)


class SeatPatch(ApiModel):
    row: int | None = None
    col: int | None = None


class SeatBatchIn(ApiModel):
    count: int = Field(ge=1, le=500, description="按序号自动编号，与已有座位不冲突（P1）")
    per_row: int = Field(8, ge=1, le=50)


class SeatStatusIn(ApiModel):
    seat_ids: list[int] = Field(min_length=1)
    status: Status
    reason: str = Field(min_length=1, max_length=200, description="停用原因必填（SPC-SEAT-02）")
    confirm: bool = False


class SeatTagsIn(ApiModel):
    seat_ids: list[int] = Field(min_length=1)
    add: list[str] = Field(default_factory=list)
    remove: list[str] = Field(default_factory=list)


class TagIn(ApiModel):
    code: str = Field(pattern=r"^[A-Z_]{2,32}$")
    name: str = Field(max_length=50)


@router.post("/seats", status_code=201, summary="登记座位（SPC-SEAT-01）")
async def create_seat(body: SeatIn, _: Principal = require("space:seat:manage")) -> SeatInfo:
    raise NotImplementedYet(TASK)


@router.post(
    "/rooms/{room_id}/seats/batch", status_code=201, summary="批量生成座位（SPC-SEAT-01，P1）"
)
async def create_seats_batch(
    room_id: int, body: SeatBatchIn, _: Principal = require("space:seat:manage")
) -> list[SeatInfo]:
    raise NotImplementedYet(TASK)


@router.post("/rooms/{room_id}/seats/import", summary="CSV 导入座位（SPC-SEAT-01，P2）")
async def import_seats(
    room_id: int, file: UploadFile, _: Principal = require("space:seat:manage")
) -> list[SeatInfo]:
    raise NotImplementedYet(TASK)


@router.patch("/seats/{seat_id}", summary="修改座位平面位置（SPC-SEAT-03，P2）")
async def update_seat(
    seat_id: int, body: SeatPatch, _: Principal = require("space:seat:manage")
) -> SeatInfo:
    raise NotImplementedYet(TASK)


@router.post(
    "/seats/status",
    summary="停用、恢复、注销座位（SPC-SEAT-01、02）",
    description="停用在 M1 中表现为写入来源 ADMIN 的占用块；受影响预约按 BR-19 处理。",
)
async def set_seats_status(
    body: SeatStatusIn, _: Principal = require("space:seat:manage")
) -> ImpactPreview:
    raise NotImplementedYet(TASK)


@router.post("/seats/tags", summary="批量添加、移除座位标记（SPC-TAG-01）")
async def set_seat_tags(
    body: SeatTagsIn, _: Principal = require("space:tag:manage")
) -> list[SeatInfo]:
    raise NotImplementedYet(TASK)


@router.post("/tags", status_code=201, summary="扩展标记字典（SPC-TAG-01，P2）")
async def create_tag(body: TagIn, _: Principal = require("space:tag:manage")) -> TagOut:
    raise NotImplementedYet(TASK)

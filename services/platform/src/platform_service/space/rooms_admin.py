"""任务 D-T06：校区、楼宇、房间与自习开放管理（SPC-ROOM-01、02、04、05、06，SPC-EVT-01）。

任何房间属性变更后经 outbox 发布 space.room.updated（完整快照，见 campus_common.contracts.events）。
关闭自习、停用、注销前先返回影响预览（调用 M1 可用性查询），confirm=true 时才执行。
"""

from fastapi import APIRouter
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.contracts.space import (
    ApplicantType,
    Building,
    Campus,
    OwnerType,
    RoomInfo,
    RoomType,
    Status,
)
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel

TASK = "D-T06"

router = APIRouter(prefix="/api/space/v1", tags=["空间 · 房间管理"])


class CampusIn(ApiModel):
    code: str = Field(max_length=32)
    name: str = Field(max_length=100)


class BuildingIn(ApiModel):
    campus_id: int
    code: str = Field(max_length=32)
    name: str = Field(max_length=100)


class RoomIn(ApiModel):
    building_id: int
    code: str = Field(max_length=32, description="全局唯一（SPC-ROOM-01）")
    name: str = Field(max_length=100)
    floor: int | None = None
    room_type: RoomType
    capacity: int = Field(ge=0)
    owner_type: OwnerType = OwnerType.SCHOOL
    department_id: int | None = Field(None, description="owner_type=DEPARTMENT 时必填")


class RoomPatch(ApiModel):
    name: str | None = Field(None, max_length=100)
    floor: int | None = None
    room_type: RoomType | None = None
    capacity: int | None = Field(None, ge=0)
    owner_type: OwnerType | None = None
    department_id: int | None = None


class ImpactPreview(ApiModel):
    affected_booking_count: int = Field(description="将被系统取消的未结束预约数（BR-19）")
    executed: bool = Field(description="confirm=false 时只预览，不执行")
    room: RoomInfo | None = None


class StudyOpenIn(ApiModel):
    study_open: bool
    confirm: bool = False


class StatusIn(ApiModel):
    status: Status
    confirm: bool = False


class BookingPolicyIn(ApiModel):
    whole_room_bookable: bool
    allowed_applicant_types: list[ApplicantType] = Field(default_factory=list)


class FacilitiesIn(ApiModel):
    facilities: list[str] = Field(
        description="如 PROJECTOR、SPEAKER、MICROPHONE（SPC-ROOM-06，P2）"
    )


@router.post("/campuses", status_code=201, summary="新增校区")
async def create_campus(body: CampusIn, _: Principal = require("space:room:manage")) -> Campus:
    raise NotImplementedYet(TASK)


@router.post("/buildings", status_code=201, summary="新增楼宇")
async def create_building(
    body: BuildingIn, _: Principal = require("space:room:manage")
) -> Building:
    raise NotImplementedYet(TASK)


@router.post("/rooms", status_code=201, summary="新增房间（SPC-ROOM-01）")
async def create_room(body: RoomIn, _: Principal = require("space:room:manage")) -> RoomInfo:
    raise NotImplementedYet(TASK)


@router.patch("/rooms/{room_id}", summary="修改房间属性（SPC-ROOM-01、04）")
async def update_room(
    room_id: int, body: RoomPatch, _: Principal = require("space:room:manage")
) -> RoomInfo:
    raise NotImplementedYet(TASK)


@router.post(
    "/rooms/{room_id}/study",
    summary="开放为自习室或关闭自习（SPC-ROOM-02）",
    description="关闭时若有未结束预约，先返回影响预览；确认后执行，受影响学生收到通知且不计违约。",
)
async def set_study_open(
    room_id: int, body: StudyOpenIn, _: Principal = require("space:room:manage")
) -> ImpactPreview:
    raise NotImplementedYet(TASK)


@router.post("/rooms/{room_id}/status", summary="启用、停用、注销房间（SPC-ROOM-01、02）")
async def set_room_status(
    room_id: int, body: StatusIn, _: Principal = require("space:room:manage")
) -> ImpactPreview:
    raise NotImplementedYet(TASK)


@router.put("/rooms/{room_id}/booking-policy", summary="整间预约属性（SPC-ROOM-05）")
async def set_booking_policy(
    room_id: int, body: BookingPolicyIn, _: Principal = require("space:room:manage")
) -> RoomInfo:
    raise NotImplementedYet(TASK)


@router.put("/rooms/{room_id}/facilities", summary="房间设施（SPC-ROOM-06，P2）")
async def set_facilities(
    room_id: int, body: FacilitiesIn, _: Principal = require("space:room:manage")
) -> RoomInfo:
    raise NotImplementedYet(TASK)

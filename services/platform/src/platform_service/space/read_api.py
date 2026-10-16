"""空间与座位主数据查询（SPC-LOC-01 等的只读部分）。骨架已实现。

前端与其他服务（持服务令牌，经服务地址直连）共用这些接口。
"""

from typing import Annotated

from fastapi import APIRouter, Query
from pydantic import Field
from sqlalchemy import func, select

from campus_common.auth import Principal, require
from campus_common.contracts.space import Building as BuildingOut
from campus_common.contracts.space import Campus as CampusOut
from campus_common.contracts.space import RoomInfo, RoomType, SeatInfo
from campus_common.db import SessionDep
from campus_common.errors import NotFound
from campus_common.models import ApiModel, Page, PageQuery
from platform_service.space.models import Building, Campus, Room, Seat, SeatTag, Tag

router = APIRouter(prefix="/api/space/v1", tags=["空间 · 查询"])

READ = "space:read"


class TagOut(ApiModel):
    code: str
    name: str


class RoomQuery(PageQuery):
    campus_id: int | None = None
    building_id: int | None = None
    room_type: RoomType | None = None
    study_open: bool | None = Field(None, description="只看已开放为自习室的房间")
    whole_room_bookable: bool | None = Field(None, description="只看允许整间预约的房间")
    department_id: int | None = None
    keyword: str | None = Field(None, max_length=50, description="匹配房间编号或名称")
    ids: list[int] | None = Field(None, description="按 ID 批量查询")
    include_deleted: bool = Field(False, description="包含已注销的房间（用于历史展示）")


class SeatQuery(ApiModel):
    tag: list[str] | None = Field(None, description="须带全部所列标记")
    include_disabled: bool = True


@router.get("/campuses", summary="校区列表")
async def campuses(session: SessionDep, _: Principal = require(READ)) -> list[CampusOut]:
    rows = await session.scalars(select(Campus).order_by(Campus.code))
    return [CampusOut.model_validate(c) for c in rows]


@router.get("/buildings", summary="楼宇列表")
async def buildings(
    session: SessionDep,
    campus_id: Annotated[int | None, Query(alias="campusId")] = None,
    _: Principal = require(READ),
) -> list[BuildingOut]:
    query = select(Building).order_by(Building.code)
    if campus_id is not None:
        query = query.where(Building.campus_id == campus_id)
    return [BuildingOut.model_validate(b) for b in await session.scalars(query)]


@router.get("/rooms", summary="房间列表（含公共区域，可按条件筛选）")
async def rooms(
    session: SessionDep,
    q: Annotated[RoomQuery, Query()],
    _: Principal = require(READ),
) -> Page[RoomInfo]:
    query = select(Room).join(Building, Building.id == Room.building_id)
    if not q.include_deleted:
        query = query.where(Room.status != "DELETED")
    if q.campus_id is not None:
        query = query.where(Building.campus_id == q.campus_id)
    if q.building_id is not None:
        query = query.where(Room.building_id == q.building_id)
    if q.room_type is not None:
        query = query.where(Room.room_type == q.room_type.value)
    if q.study_open is not None:
        query = query.where(Room.study_open.is_(q.study_open))
    if q.whole_room_bookable is not None:
        query = query.where(Room.whole_room_bookable.is_(q.whole_room_bookable))
    if q.department_id is not None:
        query = query.where(Room.department_id == q.department_id)
    if q.keyword:
        like = f"%{q.keyword}%"
        query = query.where(Room.code.ilike(like) | Room.name.ilike(like))
    if q.ids:
        query = query.where(Room.id.in_(q.ids))
    total = await session.scalar(select(func.count()).select_from(query.subquery())) or 0
    rows = await session.scalars(query.order_by(Room.code).offset(q.offset).limit(q.size))
    return Page(items=[r.to_info() for r in rows], total=total, page=q.page, size=q.size)


@router.get("/rooms/{room_id}", summary="房间详情（含开放时间、整间预约属性）")
async def room(room_id: int, session: SessionDep, _: Principal = require(READ)) -> RoomInfo:
    found = await session.get(Room, room_id)
    if found is None:
        raise NotFound("房间不存在")
    return found.to_info()


@router.get("/rooms/{room_id}/seats", summary="房间内的座位")
async def room_seats(
    room_id: int,
    session: SessionDep,
    q: Annotated[SeatQuery, Query()],
    _: Principal = require(READ),
) -> list[SeatInfo]:
    query = select(Seat).where(Seat.room_id == room_id, Seat.status != "DELETED")
    if not q.include_disabled:
        query = query.where(Seat.status == "ENABLED")
    for code in q.tag or []:
        query = query.where(
            select(SeatTag.seat_id)
            .where(SeatTag.seat_id == Seat.id, SeatTag.tag_code == code)
            .exists()
        )
    return [s.to_info() for s in await session.scalars(query.order_by(Seat.code))]


@router.get("/seats/{seat_id}", summary="座位详情")
async def seat(seat_id: int, session: SessionDep, _: Principal = require(READ)) -> SeatInfo:
    found = await session.get(Seat, seat_id)
    if found is None:
        raise NotFound("座位不存在")
    return found.to_info()


@router.get("/tags", summary="座位标记字典")
async def tags(session: SessionDep, _: Principal = require(READ)) -> list[TagOut]:
    return [TagOut.model_validate(t) for t in await session.scalars(select(Tag).order_by(Tag.code))]

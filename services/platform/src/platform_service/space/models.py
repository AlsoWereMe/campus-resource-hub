from datetime import date, datetime

from sqlalchemy import (
    ARRAY,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from campus_common.contracts.space import (
    ApplicantType,
    OwnerType,
    RoomInfo,
    RoomType,
    SeatInfo,
    Status,
)
from campus_common.contracts.space import OpeningRule as OpeningRuleOut
from platform_service.db import SpaceBase


class Campus(SpaceBase):
    __tablename__ = "campus"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True)
    name: Mapped[str] = mapped_column(String(100))


class Building(SpaceBase):
    __tablename__ = "building"

    id: Mapped[int] = mapped_column(primary_key=True)
    campus_id: Mapped[int] = mapped_column(ForeignKey("space.campus.id"))
    code: Mapped[str] = mapped_column(String(32), unique=True)
    name: Mapped[str] = mapped_column(String(100))


class Room(SpaceBase):
    __tablename__ = "room"

    id: Mapped[int] = mapped_column(primary_key=True)
    building_id: Mapped[int] = mapped_column(ForeignKey("space.building.id"))
    code: Mapped[str] = mapped_column(String(32), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    floor: Mapped[int | None] = mapped_column(Integer)
    room_type: Mapped[str] = mapped_column(String(32))
    capacity: Mapped[int] = mapped_column(Integer, default=0)
    owner_type: Mapped[str] = mapped_column(String(16), default="SCHOOL")
    department_id: Mapped[int | None] = mapped_column(
        Integer, comment="iam.department.id，不建外键"
    )
    status: Mapped[str] = mapped_column(String(16), default="ENABLED")
    study_open: Mapped[bool] = mapped_column(Boolean, default=False)
    whole_room_bookable: Mapped[bool] = mapped_column(Boolean, default=False)
    allowed_applicant_types: Mapped[list[str]] = mapped_column(ARRAY(String(32)), default=list)
    facilities: Mapped[list[str]] = mapped_column(ARRAY(String(32)), default=list)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    building: Mapped[Building] = relationship(lazy="selectin")
    opening_rules: Mapped[list["OpeningRule"]] = relationship(
        lazy="selectin", order_by="OpeningRule.weekday", cascade="all, delete-orphan"
    )
    closures: Mapped[list["Closure"]] = relationship(lazy="selectin", cascade="all, delete-orphan")

    def to_info(self) -> RoomInfo:
        return RoomInfo(
            id=self.id,
            code=self.code,
            name=self.name,
            campus_id=self.building.campus_id,
            building_id=self.building_id,
            building_name=self.building.name,
            floor=self.floor,
            room_type=RoomType(self.room_type),
            capacity=self.capacity,
            owner_type=OwnerType(self.owner_type),
            department_id=self.department_id,
            status=Status(self.status),
            study_open=self.study_open,
            whole_room_bookable=self.whole_room_bookable,
            allowed_applicant_types=[ApplicantType(t) for t in self.allowed_applicant_types],
            facilities=self.facilities,
            opening_rules=[
                OpeningRuleOut(weekday=r.weekday, start_hour=r.start_hour, end_hour=r.end_hour)
                for r in self.opening_rules
            ],
            closures=sorted(c.day for c in self.closures),
        )


class OpeningRule(SpaceBase):
    """开放时间：按星期配置整点区间（SPC-ROOM-03）。"""

    __tablename__ = "room_opening_rule"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("space.room.id", ondelete="CASCADE"))
    weekday: Mapped[int] = mapped_column(Integer, comment="1=周一 … 7=周日")
    start_hour: Mapped[int] = mapped_column(Integer)
    end_hour: Mapped[int] = mapped_column(Integer)


class Closure(SpaceBase):
    """特定日期闭馆（SPC-ROOM-03，P1）。"""

    __tablename__ = "room_closure"
    __table_args__ = (UniqueConstraint("room_id", "day"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("space.room.id", ondelete="CASCADE"))
    day: Mapped[date] = mapped_column(Date)
    reason: Mapped[str] = mapped_column(String(200), default="")


class Tag(SpaceBase):
    """座位标记字典（SPC-TAG-01）。"""

    __tablename__ = "tag"

    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class SeatTag(SpaceBase):
    __tablename__ = "seat_tag"

    seat_id: Mapped[int] = mapped_column(
        ForeignKey("space.seat.id", ondelete="CASCADE"), primary_key=True
    )
    tag_code: Mapped[str] = mapped_column(ForeignKey("space.tag.code"), primary_key=True)


class Seat(SpaceBase):
    __tablename__ = "seat"

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("space.room.id"))
    code: Mapped[str] = mapped_column(String(48), unique=True)
    status: Mapped[str] = mapped_column(String(16), default="ENABLED")
    row: Mapped[int | None] = mapped_column(Integer)
    col: Mapped[int | None] = mapped_column(Integer)

    tag_links: Mapped[list[SeatTag]] = relationship(lazy="selectin", cascade="all, delete-orphan")

    def to_info(self) -> SeatInfo:
        return SeatInfo(
            id=self.id,
            room_id=self.room_id,
            code=self.code,
            status=Status(self.status),
            tags=sorted(link.tag_code for link in self.tag_links),
            row=self.row,
            col=self.col,
        )

"""空间与座位主数据的读模型（D-SPC 提供；M1、M2、M3 消费）。"""

from datetime import date
from enum import StrEnum

from pydantic import Field

from campus_common.models import ApiModel


class RoomType(StrEnum):
    CLASSROOM = "CLASSROOM"  # 普通教室
    LIBRARY_STUDY = "LIBRARY_STUDY"  # 图书馆专用自习室
    OTHER_STUDY = "OTHER_STUDY"  # 其他自习场地
    MEETING = "MEETING"  # 会议室
    PUBLIC_AREA = "PUBLIC_AREA"  # 公共区域（走廊、卫生间等，仅用于报修定位）


class OwnerType(StrEnum):
    SCHOOL = "SCHOOL"
    DEPARTMENT = "DEPARTMENT"


class Status(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    DELETED = "DELETED"  # 逻辑注销


class ApplicantType(StrEnum):
    STAFF = "STAFF"
    STUDENT_LEADER = "STUDENT_LEADER"


class SeatTag(StrEnum):
    """预置标记；标记字典可扩展，未知标记按字符串处理。"""

    FIXED_OUTLET = "FIXED_OUTLET"  # 固定插座
    RAIL_OUTLET = "RAIL_OUTLET"  # 移动导轨插座


class OpeningRule(ApiModel):
    weekday: int = Field(ge=1, le=7, description="1=周一 … 7=周日")
    start_hour: int = Field(ge=0, le=23)
    end_hour: int = Field(ge=1, le=24, description="不含；起止均为整点（BR-22）")


class Campus(ApiModel):
    id: int
    code: str
    name: str


class Building(ApiModel):
    id: int
    campus_id: int
    code: str
    name: str


class RoomInfo(ApiModel):
    id: int
    code: str
    name: str
    campus_id: int
    building_id: int
    building_name: str
    floor: int | None = None
    room_type: RoomType
    capacity: int
    owner_type: OwnerType
    department_id: int | None = Field(None, description="归属院系；校级房间为空")
    status: Status
    study_open: bool = Field(description="是否开放为自习室（SPC-ROOM-02）")
    whole_room_bookable: bool = Field(description="是否允许整间预约（SPC-ROOM-05）")
    allowed_applicant_types: list[ApplicantType] = Field(default_factory=list)
    facilities: list[str] = Field(default_factory=list)
    opening_rules: list[OpeningRule] = Field(default_factory=list)
    closures: list[date] = Field(default_factory=list, description="闭馆日期（P1）")


class SeatInfo(ApiModel):
    id: int
    room_id: int
    code: str
    status: Status
    tags: list[str] = Field(default_factory=list)
    row: int | None = None
    col: int | None = None

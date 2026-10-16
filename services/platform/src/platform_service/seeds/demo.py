"""演示数据：只用于 dev / test。所有姓名、邮箱均为虚构，不含真实个人信息。

演示账号统一口令见配置 demo_password（默认 Passw0rd!）；账号与角色见 README「演示账号」。
"""

from dataclasses import dataclass, field

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from platform_service.config import Settings
from platform_service.iam.models import Department, Role, User, UserRole
from platform_service.iam.security import hash_password
from platform_service.space.models import (
    Building,
    Campus,
    OpeningRule,
    Room,
    Seat,
    SeatTag,
)

DEPARTMENTS = {"CS": "计算机学院", "MATH": "数学科学学院"}


@dataclass(frozen=True)
class DemoUser:
    username: str
    name: str
    user_type: str
    department: str | None
    # (角色, 范围)：范围为 "ALL"、"SELF"、("BUILDING", [楼宇编号]) 或 ("DEPARTMENT", [院系编号])
    roles: list[tuple[str, object]] = field(default_factory=list)


DEMO_USERS = [
    DemoUser("student1", "学生甲", "student", "CS", [("student", "SELF")]),
    DemoUser("student2", "学生乙", "student", "MATH", [("student", "SELF")]),
    DemoUser(
        "student3", "学生丙", "student", "CS", [("student", "SELF"), ("student_leader", "SELF")]
    ),
    DemoUser("staff1", "教师甲", "staff", "CS", [("staff", "SELF")]),
    DemoUser("staff2", "教师乙", "staff", "MATH", [("staff", "SELF")]),
    DemoUser(
        "approver1",
        "院系审批人甲",
        "staff",
        "CS",
        [("staff", "SELF"), ("dept_approver", ("DEPARTMENT", ["CS"]))],
    ),
    DemoUser(
        "approver2",
        "院系审批人乙",
        "staff",
        "MATH",
        [("staff", "SELF"), ("dept_approver", ("DEPARTMENT", ["MATH"]))],
    ),
    DemoUser("roomadmin1", "教室管理员甲", "staff", None, [("room_admin", ("BUILDING", ["H3"]))]),
    DemoUser("roomadmin2", "教室管理员乙", "staff", None, [("room_admin", ("BUILDING", ["LIB"]))]),
    DemoUser("resadmin1", "资源管理员", "staff", None, [("resource_admin", "ALL")]),
    DemoUser("ops1", "运营管理员", "staff", None, [("ops_admin", "ALL")]),
    DemoUser(
        "dispatcher1", "物业调度员", "staff", None, [("dispatcher", ("BUILDING", ["H3", "LIB"]))]
    ),
    DemoUser("tech1", "维修人员甲", "staff", None, [("technician", ("BUILDING", ["H3"]))]),
    DemoUser("tech2", "维修人员乙", "staff", None, [("technician", ("BUILDING", ["LIB"]))]),
    DemoUser("supervisor1", "物业主管", "staff", None, [("property_supervisor", "ALL")]),
]

BUILDINGS = {"H3": "第三教学楼", "LIB": "图书馆"}

WEEKDAYS_8_22 = [(d, 8, 22) for d in range(1, 6)] + [(d, 9, 21) for d in (6, 7)]
DAILY_8_23 = [(d, 8, 23) for d in range(1, 8)]


@dataclass(frozen=True)
class DemoRoom:
    code: str
    name: str
    building: str
    floor: int
    room_type: str
    capacity: int
    department: str | None = None
    study_open: bool = False
    whole_room_bookable: bool = False
    applicants: tuple[str, ...] = ()
    facilities: tuple[str, ...] = ()
    opening: list[tuple[int, int, int]] = field(default_factory=lambda: WEEKDAYS_8_22)


DEMO_ROOMS = [
    DemoRoom(
        "H3-101",
        "三教 101",
        "H3",
        1,
        "CLASSROOM",
        40,
        None,
        True,
        True,
        ("STAFF", "STUDENT_LEADER"),
        ("PROJECTOR",),
    ),
    DemoRoom("H3-102", "三教 102", "H3", 1, "CLASSROOM", 40, None, True, True, ("STAFF",)),
    DemoRoom(
        "H3-201",
        "三教 201（计算机学院）",
        "H3",
        2,
        "CLASSROOM",
        32,
        "CS",
        True,
        True,
        ("STAFF", "STUDENT_LEADER"),
    ),
    DemoRoom(
        "H3-301",
        "三教 301 报告厅",
        "H3",
        3,
        "MEETING",
        120,
        None,
        False,
        True,
        ("STAFF", "STUDENT_LEADER"),
        ("PROJECTOR", "SPEAKER", "MICROPHONE"),
    ),
    DemoRoom("H3-1F", "三教一楼公共区域", "H3", 1, "PUBLIC_AREA", 0),
    DemoRoom(
        "LIB-201", "图书馆二楼自习区", "LIB", 2, "LIBRARY_STUDY", 64, None, True, opening=DAILY_8_23
    ),
    DemoRoom(
        "LIB-301",
        "图书馆三楼自习区（数学科学学院）",
        "LIB",
        3,
        "LIBRARY_STUDY",
        48,
        "MATH",
        True,
        opening=DAILY_8_23,
    ),
]


def seat_tags(seq: int) -> list[str]:
    tags = []
    if seq % 4 == 1:
        tags.append("FIXED_OUTLET")
    if seq % 10 == 0:
        tags.append("RAIL_OUTLET")
    return tags


async def seed_iam(session: AsyncSession, settings: Settings) -> None:
    departments: dict[str, Department] = {}
    for code, name in DEPARTMENTS.items():
        dept = await session.scalar(select(Department).where(Department.code == code))
        if dept is None:
            dept = Department(code=code, name=name)
            session.add(dept)
            await session.flush()
        departments[code] = dept
    roles = {r.code: r for r in await session.scalars(select(Role))}
    buildings = {b.code: b.id for b in await session.scalars(select(Building))}
    password_hash = hash_password(settings.demo_password)
    for spec in DEMO_USERS:
        if await session.scalar(select(User).where(User.username == spec.username)) is not None:
            continue
        user = User(
            username=spec.username,
            password_hash=password_hash,
            name=spec.name,
            user_type=spec.user_type,
            department_id=departments[spec.department].id if spec.department else None,
            email=f"{spec.username}@example.edu",
        )
        session.add(user)
        await session.flush()
        for role_code, scope in spec.roles:
            grant = UserRole(user_id=user.id, role_id=roles[role_code].id)
            if scope == "ALL":
                grant.scope_all = True
            elif isinstance(scope, tuple) and scope[0] == "BUILDING":
                grant.scope_buildings = [buildings[c] for c in scope[1]]
            elif isinstance(scope, tuple) and scope[0] == "DEPARTMENT":
                grant.scope_departments = [departments[c].id for c in scope[1]]
            session.add(grant)


async def seed_space(session: AsyncSession) -> None:
    campus = await session.scalar(select(Campus).where(Campus.code == "MAIN"))
    if campus is None:
        campus = Campus(code="MAIN", name="主校区")
        session.add(campus)
        await session.flush()
    buildings: dict[str, Building] = {}
    for code, name in BUILDINGS.items():
        building = await session.scalar(select(Building).where(Building.code == code))
        if building is None:
            building = Building(campus_id=campus.id, code=code, name=name)
            session.add(building)
            await session.flush()
        buildings[code] = building
    departments = {d.code: d.id for d in await session.scalars(select(Department))}
    for spec in DEMO_ROOMS:
        if await session.scalar(select(Room).where(Room.code == spec.code)) is not None:
            continue
        room = Room(
            building_id=buildings[spec.building].id,
            code=spec.code,
            name=spec.name,
            floor=spec.floor,
            room_type=spec.room_type,
            capacity=spec.capacity,
            owner_type="DEPARTMENT" if spec.department else "SCHOOL",
            department_id=departments.get(spec.department) if spec.department else None,
            study_open=spec.study_open,
            whole_room_bookable=spec.whole_room_bookable,
            allowed_applicant_types=list(spec.applicants),
            facilities=list(spec.facilities),
            opening_rules=[
                OpeningRule(weekday=d, start_hour=s, end_hour=e) for d, s, e in spec.opening
            ],
        )
        session.add(room)
        await session.flush()
        if spec.study_open:
            for seq in range(1, spec.capacity + 1):
                seat = Seat(
                    room_id=room.id,
                    code=f"{spec.code}-{seq:03d}",
                    row=(seq - 1) // 8 + 1,
                    col=(seq - 1) % 8 + 1,
                    tag_links=[SeatTag(tag_code=t) for t in seat_tags(seq)],
                )
                session.add(seat)


async def seed_demo(session: AsyncSession, settings: Settings) -> None:
    # 先建空间（院系 ID 在建房间时需要，故先建院系）
    for code, name in DEPARTMENTS.items():
        if await session.scalar(select(Department).where(Department.code == code)) is None:
            session.add(Department(code=code, name=name))
    await session.flush()
    await seed_space(session)
    await session.flush()
    await seed_iam(session, settings)

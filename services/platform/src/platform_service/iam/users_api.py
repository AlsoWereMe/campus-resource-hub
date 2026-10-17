"""任务 D-T02：用户、院系与账号管理（IAM-AUTH-02、IAM-USER-01）。"""

from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Query, UploadFile
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel, Page, PageQuery

TASK = "D-T02"

router = APIRouter(prefix="/api/iam/v1", tags=["IAM · 用户与院系"])

UserType = Literal["student", "staff"]
UserStatus = Literal["ACTIVE", "DISABLED"]


class UserOut(ApiModel):
    id: int
    username: str = Field(description="学号或工号")
    name: str
    user_type: UserType
    department_id: int | None
    department_name: str | None
    email: str | None
    phone: str | None
    status: UserStatus
    roles: list[str]
    created_at: datetime


class UserCreate(ApiModel):
    username: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=100)
    user_type: UserType
    department_id: int | None = None
    email: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, max_length=32)
    initial_password: str = Field(min_length=8, max_length=128)


class UserUpdate(ApiModel):
    name: str | None = Field(None, max_length=100)
    department_id: int | None = None
    email: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, max_length=32)


class UserQuery(PageQuery):
    keyword: str | None = Field(None, max_length=50, description="学号、工号或姓名")
    department_id: int | None = None
    role: str | None = None
    status: UserStatus | None = None


class ImportIssue(ApiModel):
    line: int
    message: str


class ImportResult(ApiModel):
    imported: int
    errors: list[ImportIssue] = Field(description="有任何错误则整批不导入（IAM-AUTH-02）")


class DepartmentOut(ApiModel):
    id: int
    code: str
    name: str


class DepartmentIn(ApiModel):
    code: str = Field(min_length=1, max_length=32)
    name: str = Field(min_length=1, max_length=100)


@router.get("/users", summary="用户列表")
async def list_users(
    q: Annotated[UserQuery, Query()], _: Principal = require("iam:user:manage")
) -> Page[UserOut]:
    raise NotImplementedYet(TASK)


@router.post("/users", status_code=201, summary="新建用户（默认授予学生或教职工角色）")
async def create_user(body: UserCreate, _: Principal = require("iam:user:manage")) -> UserOut:
    raise NotImplementedYet(TASK)


@router.post(
    "/users/import",
    summary="CSV 批量导入用户（IAM-AUTH-02）",
    description="列：学号、姓名、院系编码、邮箱、初始角色。全部校验通过才导入，否则按行号列出全部错误。",
)
async def import_users(file: UploadFile, _: Principal = require("iam:user:manage")) -> ImportResult:
    raise NotImplementedYet(TASK)


@router.get("/users/{user_id}", summary="用户详情")
async def get_user(user_id: int, _: Principal = require("iam:user:manage")) -> UserOut:
    raise NotImplementedYet(TASK)


@router.patch(
    "/users/{user_id}",
    summary="修改用户（IAM-USER-01）",
    description="院系变更后可见的院系专属自习室随之变化，已有预约不受影响。",
)
async def update_user(
    user_id: int, body: UserUpdate, _: Principal = require("iam:user:manage")
) -> UserOut:
    raise NotImplementedYet(TASK)


@router.post(
    "/users/{user_id}/disable",
    summary="停用账号（IAM-AUTH-02）",
    description="立即不能登录，刷新令牌全部失效；已签发访问令牌在有效期（≤ 15 分钟）后失效。",
)
async def disable_user(user_id: int, _: Principal = require("iam:user:manage")) -> UserOut:
    raise NotImplementedYet(TASK)


@router.post("/users/{user_id}/enable", summary="启用账号")
async def enable_user(user_id: int, _: Principal = require("iam:user:manage")) -> UserOut:
    raise NotImplementedYet(TASK)


@router.get("/departments", summary="院系列表（IAM-USER-01）")
async def list_departments(_: Principal = require("iam:user:manage")) -> list[DepartmentOut]:
    raise NotImplementedYet(TASK)


@router.post("/departments", status_code=201, summary="新增院系")
async def create_department(
    body: DepartmentIn, _: Principal = require("iam:user:manage")
) -> DepartmentOut:
    raise NotImplementedYet(TASK)


@router.patch("/departments/{department_id}", summary="修改院系")
async def update_department(
    department_id: int, body: DepartmentIn, _: Principal = require("iam:user:manage")
) -> DepartmentOut:
    raise NotImplementedYet(TASK)

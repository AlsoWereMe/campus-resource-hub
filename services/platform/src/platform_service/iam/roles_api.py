"""任务 D-T03：角色、权限点与授权（IAM-ROLE-01 ~ 04）。权限点清单见 contracts/permissions.yaml。"""

from fastapi import APIRouter, Response
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel

TASK = "D-T03"

router = APIRouter(prefix="/api/iam/v1", tags=["IAM · 角色与授权"])


class PermissionOut(ApiModel):
    code: str
    description: str


class RoleOut(ApiModel):
    id: int
    code: str
    name: str
    description: str
    builtin: bool
    enabled: bool
    permissions: list[str]
    user_count: int


class RoleIn(ApiModel):
    code: str = Field(pattern=r"^[a-z_]{2,64}$")
    name: str = Field(max_length=100)
    description: str = Field("", max_length=500)
    permissions: list[str]
    enabled: bool = True


class RolePatch(ApiModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=500)
    permissions: list[str] | None = None
    enabled: bool | None = None


class RoleGrant(ApiModel):
    role_id: int
    scope_all: bool = False
    building_ids: list[int] = Field(default_factory=list)
    department_ids: list[int] = Field(default_factory=list)


@router.get("/permissions", summary="权限点清单（IAM-ROLE-01，只读）")
async def permissions(_: Principal = require("iam:role:manage")) -> list[PermissionOut]:
    raise NotImplementedYet(TASK)


@router.get("/roles", summary="角色列表")
async def list_roles(_: Principal = require("iam:role:manage")) -> list[RoleOut]:
    raise NotImplementedYet(TASK)


@router.post("/roles", status_code=201, summary="新建角色（IAM-ROLE-02）")
async def create_role(body: RoleIn, _: Principal = require("iam:role:manage")) -> RoleOut:
    raise NotImplementedYet(TASK)


@router.get("/roles/{role_id}", summary="角色详情")
async def get_role(role_id: int, _: Principal = require("iam:role:manage")) -> RoleOut:
    raise NotImplementedYet(TASK)


@router.patch(
    "/roles/{role_id}",
    summary="修改角色（IAM-ROLE-02）",
    description="系统管理员角色不可减少权限；权限点必须来自清单；写入审计。",
)
async def update_role(
    role_id: int, body: RolePatch, _: Principal = require("iam:role:manage")
) -> RoleOut:
    raise NotImplementedYet(TASK)


@router.delete(
    "/roles/{role_id}",
    status_code=204,
    summary="删除角色（IAM-ROLE-02）",
    description="仍有用户绑定时拒绝并提示人数；系统管理员角色不可删除。",
)
async def delete_role(role_id: int, _: Principal = require("iam:role:manage")) -> Response:
    raise NotImplementedYet(TASK)


@router.get("/users/{user_id}/roles", summary="用户的角色与数据范围（IAM-ROLE-03）")
async def user_roles(user_id: int, _: Principal = require("iam:role:manage")) -> list[RoleGrant]:
    raise NotImplementedYet(TASK)


@router.put(
    "/users/{user_id}/roles",
    summary="设置用户的角色与数据范围（IAM-ROLE-03、04）",
    description="整体替换；一人可多角色，权限取并集；写入审计。",
)
async def set_user_roles(
    user_id: int, body: list[RoleGrant], _: Principal = require("iam:role:manage")
) -> list[RoleGrant]:
    raise NotImplementedYet(TASK)

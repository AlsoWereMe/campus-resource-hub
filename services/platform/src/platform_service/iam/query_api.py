"""任务 D-T01：按角色与范围查询用户（IAM-USER-02）。M2 解析审批人、M3 列出维修人员都依赖它。"""

from typing import Annotated

from fastapi import APIRouter, Query
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.contracts.iam import UserBrief
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel

TASK = "D-T01"

router = APIRouter(prefix="/internal/iam/v1", tags=["IAM · 内部"])


class UsersByRoleQuery(ApiModel):
    role: str = Field(description="角色编码，如 technician")
    department_id: int | None = Field(None, description="数据范围须覆盖该院系")
    building_id: int | None = Field(None, description="数据范围须覆盖该楼宇")


class UserIdsQuery(ApiModel):
    ids: list[int]


@router.get(
    "/users",
    summary="按角色与数据范围查询有效用户（IAM-USER-02）",
    description="返回拥有该角色、且该授权的数据范围覆盖给定院系或楼宇的启用用户；全校范围总是覆盖。",
)
async def users_by_role(
    q: Annotated[UsersByRoleQuery, Query()], _: Principal = require("iam:user:query")
) -> list[UserBrief]:
    raise NotImplementedYet(TASK)


@router.get("/users/batch", summary="按 ID 批量查询用户摘要（展示姓名、发送通知）")
async def users_by_ids(
    q: Annotated[UserIdsQuery, Query()], _: Principal = require("iam:user:query")
) -> list[UserBrief]:
    raise NotImplementedYet(TASK)

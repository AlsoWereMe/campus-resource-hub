"""任务 M2-T02：准入校验——权限门槛（M2-ELG-01 ~ 05；BR-M2-01 ~ 07、17、18）。

提交接口（M2-T04）在写入前调用同一套校验；本接口供前端与会话代理在提交前预检。
"""

from fastapi import APIRouter
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel
from room_service.api.models import API, ApplicationCreate

TASK = "M2-T02"

router = APIRouter(prefix=API, tags=["M2 · 准入校验"])


class Violation(ApiModel):
    rule: str = Field(description="规则编号，如 BR-M2-03")
    message: str


class EligibilityResult(ApiModel):
    eligible: bool
    violations: list[Violation]


@router.post("/applications/check", summary="提交前预检准入门槛（M2-ELG-01 ~ 05）")
async def check_eligibility(
    body: ApplicationCreate, _: Principal = require("m2:application:create")
) -> EligibilityResult:
    raise NotImplementedYet(TASK)

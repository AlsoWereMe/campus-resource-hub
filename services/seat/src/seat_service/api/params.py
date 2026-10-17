"""任务 M1-T02：业务参数（M1-CFG-01；参数清单见需求 §3）。"""

from fastapi import APIRouter
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel
from seat_service.api.models import API

TASK = "M1-T02"

router = APIRouter(prefix=f"{API}/admin", tags=["M1 · 业务参数"])


class Setting(ApiModel):
    key: str = Field(description="如 m1.booking.max_hours")
    value: int | bool
    default: int | bool
    min: int | None = None
    max: int | None = None
    description: str


class SettingsUpdate(ApiModel):
    values: dict[str, int | bool] = Field(description="要修改的参数键与新值")


@router.get("/settings", summary="查看 M1 业务参数")
async def list_settings(_: Principal = require("m1:setting:manage")) -> list[Setting]:
    raise NotImplementedYet(TASK)


@router.put(
    "/settings",
    summary="修改 M1 业务参数（M1-CFG-01）",
    description="校验取值范围；写入审计；只作用于此后新建的预约（BR-21）。",
)
async def update_settings(
    body: SettingsUpdate, _: Principal = require("m1:setting:manage")
) -> list[Setting]:
    raise NotImplementedYet(TASK)

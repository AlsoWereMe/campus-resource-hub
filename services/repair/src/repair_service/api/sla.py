"""任务 M3-T05：处理时限、超时升级的配置与故障类别维护（M3-ESC-04；BR-M3-02、04、16）。

升级扫描本身是定时任务，见 jobs.py。
"""

from fastapi import APIRouter
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel
from repair_service.api.models import API

TASK = "M3-T05"

router = APIRouter(prefix=f"{API}/admin", tags=["M3 · 时限与类别"])


class Setting(ApiModel):
    key: str = Field(description="如 m3.sla.accept.normal_minutes")
    value: int
    default: int
    min: int | None = None
    max: int | None = None
    description: str


class SettingsUpdate(ApiModel):
    values: dict[str, int]


class CategoryIn(ApiModel):
    code: str = Field(pattern=r"^[A-Z_]{2,32}$")
    name: str = Field(max_length=20)
    enabled: bool = True


@router.get("/settings", summary="查看处理时限等 M3 参数")
async def list_settings(_: Principal = require("m3:config:manage")) -> list[Setting]:
    raise NotImplementedYet(TASK)


@router.put(
    "/settings",
    summary="修改处理时限（M3-ESC-04）",
    description="只影响此后进入新阶段的工单（BR-M3-16）；写入审计。",
)
async def update_settings(
    body: SettingsUpdate, _: Principal = require("m3:config:manage")
) -> list[Setting]:
    raise NotImplementedYet(TASK)


@router.put("/categories", summary="维护故障类别字典（BR-M3-02）")
async def upsert_categories(
    body: list[CategoryIn], _: Principal = require("m3:config:manage")
) -> list[CategoryIn]:
    raise NotImplementedYet(TASK)

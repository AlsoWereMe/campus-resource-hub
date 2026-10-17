"""任务 M2-T03：审批链配置与 M2 参数（M2-FLOW-01、02，M2-APP-02；预置审批链见需求 §4.2）。"""

from fastapi import APIRouter, Response
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.contracts.space import ApplicantType, OwnerType, RoomType
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel
from room_service.api.models import API, ApprovalLevel

TASK = "M2-T03"

router = APIRouter(prefix=f"{API}/admin", tags=["M2 · 审批链与参数"])


class FlowCondition(ApiModel):
    applicant_types: list[ApplicantType] = Field(default_factory=list, description="空表示不限")
    min_attendees: int | None = Field(None, description="预计人数大于该值时命中")
    min_hours: int | None = Field(None, description="时长大于该值时命中")
    room_types: list[RoomType] = Field(default_factory=list)
    room_owner: OwnerType | None = None


class FlowRuleIn(ApiModel):
    name: str = Field(max_length=50)
    priority: int = Field(ge=1, description="数字越小越优先，取第一条命中的规则（BR-M2-09）")
    condition: FlowCondition
    levels: list[ApprovalLevel] = Field(min_length=1)
    enabled: bool = True


class FlowRule(FlowRuleIn):
    id: int


class Setting(ApiModel):
    key: str = Field(description="如 m2.level_timeout_hours")
    value: int
    default: int
    min: int | None = None
    max: int | None = None
    description: str


class SettingsUpdate(ApiModel):
    values: dict[str, int]


@router.get("/flows", summary="审批链规则列表（M2-FLOW-01）")
async def list_flows(_: Principal = require("m2:flow:manage")) -> list[FlowRule]:
    raise NotImplementedYet(TASK)


@router.post(
    "/flows",
    status_code=201,
    summary="新增审批链规则（M2-FLOW-02）",
    description="只影响此后提交的申请（M2-APP-02）；写入审计。",
)
async def create_flow(body: FlowRuleIn, _: Principal = require("m2:flow:manage")) -> FlowRule:
    raise NotImplementedYet(TASK)


@router.put("/flows/{flow_id}", summary="修改审批链规则（M2-FLOW-02）")
async def update_flow(
    flow_id: int, body: FlowRuleIn, _: Principal = require("m2:flow:manage")
) -> FlowRule:
    raise NotImplementedYet(TASK)


@router.delete("/flows/{flow_id}", status_code=204, summary="删除审批链规则（M2-FLOW-02）")
async def delete_flow(flow_id: int, _: Principal = require("m2:flow:manage")) -> Response:
    raise NotImplementedYet(TASK)


@router.get("/settings", summary="查看 M2 参数")
async def list_settings(_: Principal = require("m2:flow:manage")) -> list[Setting]:
    raise NotImplementedYet(TASK)


@router.put("/settings", summary="修改 M2 参数（BR-M2-19：只作用于新申请）")
async def update_settings(
    body: SettingsUpdate, _: Principal = require("m2:flow:manage")
) -> list[Setting]:
    raise NotImplementedYet(TASK)

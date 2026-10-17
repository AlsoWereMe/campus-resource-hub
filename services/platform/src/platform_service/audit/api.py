"""任务 D-T04：操作审计（AUD-01、02）。

AUD-01：消费 audit.record 消息并只增不改地存储（消息处理写在 platform_service/consumers.py）。
AUD-02：查询接口。
"""

import datetime as dt
from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Query

from campus_common.auth import Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel, Page, PageQuery

TASK = "D-T04"

router = APIRouter(prefix="/api/audit/v1", tags=["审计"])


class AuditLogOut(ApiModel):
    id: int
    actor_type: str
    actor_id: str
    actor_name: str | None
    action: str
    target_type: str
    target_id: str
    before: dict[str, Any] | None
    after: dict[str, Any] | None
    result: str
    occurred_at: datetime
    trace_id: str | None


class AuditQuery(PageQuery):
    actor_id: str | None = None
    action: str | None = None
    target_type: str | None = None
    target_id: str | None = None
    date_from: dt.date | None = None
    date_to: dt.date | None = None


@router.get(
    "/logs",
    summary="审计查询（AUD-02）",
    description="审计记录只增不改，任何角色都不能修改或删除。",
)
async def logs(
    q: Annotated[AuditQuery, Query()], _: Principal = require("audit:log:view")
) -> Page[AuditLogOut]:
    raise NotImplementedYet(TASK)

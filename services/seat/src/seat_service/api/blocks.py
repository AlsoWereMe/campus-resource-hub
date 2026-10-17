"""任务 M1-T01：占用块与状态追溯（M1-INT-01 ~ 04、06）。

座位「不可预约」只用占用块表达：个人预约、整间占用、维修下架、管理员停用（需求 §4.3）。
M2、M3 只通过本文件中的内部接口写回 M1。
"""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Query, Response
from pydantic import Field

from campus_common.auth import Principal, require
from campus_common.contracts.m1 import (
    BlockKind,
    BlockResult,
    BlockSource,
    BlockUpsert,
    RoomAvailability,
)
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel
from seat_service.api.models import API, INTERNAL, SlotState

TASK = "M1-T01"

internal = APIRouter(prefix=INTERNAL, tags=["M1 · 内部接口"])
admin = APIRouter(prefix=f"{API}/admin", tags=["M1 · 状态追溯"])


class AvailabilityQuery(ApiModel):
    starts_at: datetime
    ends_at: datetime


class SeatTrace(ApiModel):
    seat_id: int
    at: datetime
    state: SlotState
    source: BlockSource | None
    source_ref: str | None
    kind: BlockKind | None
    written_at: datetime | None
    written_by: str | None


class SeatStateLog(ApiModel):
    id: int
    seat_id: int
    action: str  # WRITE / UPGRADE / RELEASE
    source: BlockSource
    source_ref: str
    kind: BlockKind
    starts_at: datetime
    ends_at: datetime | None
    written_by: str
    at: datetime


class TraceQuery(ApiModel):
    seat_id: int
    at: datetime


class TraceHistoryQuery(ApiModel):
    seat_id: int
    from_: datetime | None = Field(None, alias="from")
    to: datetime | None = None


@internal.put(
    "/blocks/{source}/{source_ref}",
    summary="写入或更新占用块（M1-INT-01、03）",
    description="以「写入来源 + 来源单号」幂等。ACTIVE 取消冲突的个人预约并通知"
    "（不计违约，BR-19），HOLD 只阻止新预约。仅 M3_REPAIR、ADMIN 可不填结束时间。",
)
async def upsert_block(
    source: BlockSource,
    source_ref: str,
    body: BlockUpsert,
    _: Principal = require("m1:block:write"),
) -> BlockResult:
    raise NotImplementedYet(TASK)


@internal.delete(
    "/blocks/{source}/{source_ref}",
    status_code=204,
    summary="释放占用块（M1-INT-02）",
    description="幂等：释放不存在或已释放的块也返回 204。被取消的个人预约不自动恢复。",
)
async def release_block(
    source: BlockSource,
    source_ref: str,
    _: Principal = require("m1:block:write"),
) -> Response:
    raise NotImplementedYet(TASK)


@internal.get(
    "/rooms/{room_id}/availability",
    summary="自习室在区间内的占用与冲突预约数（M1-INT-04）",
    description="供 M2 提交、审批前展示冲突；不含学生身份。",
)
async def room_availability(
    room_id: int,
    q: Annotated[AvailabilityQuery, Query()],
    _: Principal = require("m1:block:write"),
) -> RoomAvailability:
    raise NotImplementedYet(TASK)


@admin.get("/trace", summary="座位在某时刻的状态与来源（M1-INT-06）")
async def seat_trace(
    q: Annotated[TraceQuery, Query()], _: Principal = require("m1:trace:view")
) -> SeatTrace:
    raise NotImplementedYet(TASK)


@admin.get("/trace/history", summary="座位状态变更历史（M1-INT-06）")
async def seat_trace_history(
    q: Annotated[TraceHistoryQuery, Query()], _: Principal = require("m1:trace:view")
) -> list[SeatStateLog]:
    raise NotImplementedYet(TASK)

"""任务 D-T05：通知服务（NTF-01 ~ 04）。

NTF-01：消费 notify.send 消息，按幂等键只投递一次，经 SMTP（dev / test 为 Mailpit）发邮件并写站内信，
失败按退避重试（消息处理写在 platform_service/consumers.py）。本文件是站内信、模板、投递记录接口。
"""

import datetime as dt
from datetime import datetime
from typing import Annotated, Literal

from fastapi import APIRouter, Query, Response
from pydantic import Field

from campus_common.auth import AUTHENTICATED, Principal, require
from campus_common.errors import NotImplementedYet
from campus_common.models import ApiModel, Page, PageQuery

TASK = "D-T05"

router = APIRouter(prefix="/api/notify/v1", tags=["通知"])


class InboxMessage(ApiModel):
    id: int
    event: str
    title: str
    body: str
    read: bool
    created_at: datetime


class InboxQuery(PageQuery):
    unread_only: bool = False


class UnreadCount(ApiModel):
    count: int


class Template(ApiModel):
    event: str = Field(description="事件类型，如 m1.booking.reminder")
    title: str
    body: str = Field(description="支持 ${变量} 占位，如 ${roomName}")


class TemplateIn(ApiModel):
    title: str = Field(max_length=100)
    body: str = Field(max_length=2000)


class Delivery(ApiModel):
    id: int
    idempotency_key: str
    recipient_user_id: int
    event: str
    channel: Literal["email", "inbox"]
    status: Literal["PENDING", "SENT", "FAILED"]
    attempts: int
    last_error: str | None
    created_at: datetime
    sent_at: datetime | None


class DeliveryQuery(PageQuery):
    recipient_user_id: int | None = None
    event: str | None = None
    status: Literal["PENDING", "SENT", "FAILED"] | None = None
    date_from: dt.date | None = None
    date_to: dt.date | None = None


@router.get("/inbox", summary="我的站内消息（NTF-03）")
async def inbox(
    q: Annotated[InboxQuery, Query()], _: Principal = AUTHENTICATED
) -> Page[InboxMessage]:
    raise NotImplementedYet(TASK)


@router.get("/inbox/unread-count", summary="未读数（NTF-03）")
async def unread_count(_: Principal = AUTHENTICATED) -> UnreadCount:
    raise NotImplementedYet(TASK)


@router.post("/inbox/{message_id}/read", status_code=204, summary="标记已读（NTF-03）")
async def mark_read(message_id: int, _: Principal = AUTHENTICATED) -> Response:
    raise NotImplementedYet(TASK)


@router.post("/inbox/read-all", status_code=204, summary="全部标记已读（NTF-03）")
async def mark_all_read(_: Principal = AUTHENTICATED) -> Response:
    raise NotImplementedYet(TASK)


@router.get("/templates", summary="通知模板列表（NTF-02）")
async def templates(_: Principal = require("notify:template:manage")) -> list[Template]:
    raise NotImplementedYet(TASK)


@router.put("/templates/{event}", summary="修改某类事件的模板（NTF-02）")
async def update_template(
    event: str, body: TemplateIn, _: Principal = require("notify:template:manage")
) -> Template:
    raise NotImplementedYet(TASK)


@router.get("/deliveries", summary="投递记录（NTF-04）")
async def deliveries(
    q: Annotated[DeliveryQuery, Query()], _: Principal = require("notify:delivery:view")
) -> Page[Delivery]:
    raise NotImplementedYet(TASK)

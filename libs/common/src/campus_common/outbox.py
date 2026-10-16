"""Outbox：业务状态变更与「待发送的跨服务调用 / 消息」在同一事务中写入（架构 §5）。

后台投递器异步发送。

用法（在业务事务中）：
    outbox = request.app.state.outbox
    await outbox.call(session, service="seat", method="PUT", path="/internal/m1/v1/blocks/...",
                      body={...}, dedup_key="M2:123:HOLD", aggregate="application:123")
    await outbox.publish(session, "m3.workorder.repairing", event_model)
    await outbox.notify(session, NotifySend(...))
    await outbox.audit(session, AuditRecord(...))
    status = await outbox.writeback_status(session, "application:123")   # 写回状态（M2-INT-03）

投递规则：同一 aggregate 的消息严格按写入顺序发送；5xx 与网络错误按退避重试，
达到上限或遇到 4xx 时置为 failed，可用 retry_failed() 人工重放。
"""

import asyncio
from datetime import timedelta
from typing import Any, Literal, Protocol

import httpx
from pydantic import BaseModel
from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Identity,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    func,
    select,
    update,
)
from sqlalchemy.dialects.postgresql import JSONB, insert
from sqlalchemy.engine import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from campus_common.config import ServiceName
from campus_common.contracts.events import AuditRecord, NotifySend
from campus_common.db import Database
from campus_common.logging import get_logger
from campus_common.tracing import current_trace_id, trace_context

PENDING, SENT, FAILED = "pending", "sent", "failed"
WritebackStatus = Literal["NONE", "SYNCING", "SYNCED", "FAILED"]

log = get_logger(__name__)


def outbox_table(metadata: MetaData) -> Table:
    """在本服务的 metadata 中定义 outbox 表（随本服务的迁移创建）。"""
    return Table(
        "outbox",
        metadata,
        Column("id", BigInteger, Identity(), primary_key=True),
        Column("kind", String(16), nullable=False, comment="http | event"),
        Column(
            "target", String(300), nullable=False, comment="http：服务 方法 路径；event：路由键"
        ),
        Column("payload", JSONB, nullable=True),
        Column("dedup_key", String(200), nullable=True, unique=True),
        Column("aggregate", String(100), nullable=True, index=True),
        Column("status", String(16), nullable=False, server_default=PENDING, index=True),
        Column("attempts", Integer, nullable=False, server_default="0"),
        Column(
            "next_attempt_at", DateTime(timezone=True), nullable=False, server_default=func.now()
        ),
        Column("last_error", Text, nullable=True),
        Column("trace_id", String(32), nullable=True),
        Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
        Column("sent_at", DateTime(timezone=True), nullable=True),
    )


def _dump(payload: BaseModel | dict[str, Any] | None) -> Any:
    if isinstance(payload, BaseModel):
        return payload.model_dump(mode="json", by_alias=True)
    return payload


class Outbox:
    def __init__(self, table: Table) -> None:
        self.table = table

    async def _insert(
        self,
        session: AsyncSession,
        *,
        kind: str,
        target: str,
        payload: Any,
        dedup_key: str | None,
        aggregate: str | None,
    ) -> None:
        stmt = insert(self.table).values(
            kind=kind,
            target=target,
            payload=payload,
            dedup_key=dedup_key,
            aggregate=aggregate,
            trace_id=current_trace_id(),
        )
        if dedup_key is not None:
            stmt = stmt.on_conflict_do_nothing(index_elements=["dedup_key"])
        await session.execute(stmt)

    async def call(
        self,
        session: AsyncSession,
        *,
        service: ServiceName,
        method: str,
        path: str,
        body: BaseModel | dict[str, Any] | None = None,
        dedup_key: str,
        aggregate: str | None = None,
    ) -> None:
        """登记一次对其他服务的 HTTP 调用（如 M2、M3 写回 M1 占用块）。"""
        await self._insert(
            session,
            kind="http",
            target=f"{service} {method.upper()} {path}",
            payload=_dump(body),
            dedup_key=dedup_key,
            aggregate=aggregate,
        )

    async def publish(
        self,
        session: AsyncSession,
        routing_key: str,
        payload: BaseModel | dict[str, Any],
        *,
        dedup_key: str | None = None,
        aggregate: str | None = None,
    ) -> None:
        """登记一条领域事件或命令消息。"""
        await self._insert(
            session,
            kind="event",
            target=routing_key,
            payload=_dump(payload),
            dedup_key=dedup_key,
            aggregate=aggregate,
        )

    async def notify(self, session: AsyncSession, message: NotifySend) -> None:
        await self.publish(
            session, "notify.send", message, dedup_key=f"notify:{message.idempotency_key}"
        )

    async def audit(self, session: AsyncSession, record: AuditRecord) -> None:
        await self.publish(session, "audit.record", record)

    async def writeback_status(self, session: AsyncSession, aggregate: str) -> WritebackStatus:
        t = self.table
        statuses = (
            await session.scalars(
                select(t.c.status).where(t.c.aggregate == aggregate, t.c.kind == "http")
            )
        ).all()
        if not statuses:
            return "NONE"
        if FAILED in statuses:
            return "FAILED"
        return "SYNCING" if PENDING in statuses else "SYNCED"

    async def retry_failed(self, session: AsyncSession, aggregate: str) -> int:
        t = self.table
        result = await session.execute(
            update(t)
            .where(t.c.aggregate == aggregate, t.c.status == FAILED)
            .values(status=PENDING, attempts=0, next_attempt_at=func.now(), last_error=None)
        )
        return int(result.rowcount or 0)  # type: ignore[attr-defined]


class HttpCaller(Protocol):
    async def request(
        self, service: ServiceName, method: str, path: str, **kwargs: Any
    ) -> httpx.Response: ...


class EventPublisher(Protocol):
    async def publish(
        self, routing_key: str, payload: dict[str, Any], *, message_id: str
    ) -> None: ...


class PermanentFailure(Exception):
    """对方明确拒绝（4xx），重试没有意义。"""


class OutboxRelay:
    """后台投递器：按顺序发送 outbox 中的消息。"""

    def __init__(
        self,
        db: Database,
        table: Table,
        *,
        service: str,
        client: HttpCaller,
        bus: EventPublisher | None,
        max_attempts: int,
        batch: int = 50,
    ) -> None:
        self.db = db
        self.table = table
        self.service = service
        self.client = client
        self.bus = bus
        self.max_attempts = max_attempts
        self.batch = batch

    async def run_once(self) -> int:
        t = self.table
        earlier = t.alias("earlier")
        blocked = (
            select(earlier.c.id)
            .where(
                earlier.c.aggregate == t.c.aggregate,
                earlier.c.id < t.c.id,
                earlier.c.status != SENT,
            )
            .exists()
        )
        stmt = (
            select(t)
            .where(t.c.status == PENDING, t.c.next_attempt_at <= func.now(), ~blocked)
            .order_by(t.c.id)
            .limit(self.batch)
            .with_for_update(skip_locked=True, of=t)
        )
        async with self.db.sessionmaker() as session, session.begin():
            rows = (await session.execute(stmt)).mappings().all()
            for row in rows:
                await self._deliver(session, row)
        return len(rows)

    async def _deliver(self, session: AsyncSession, row: RowMapping) -> None:
        t = self.table
        try:
            with trace_context(row["trace_id"]):
                await self._dispatch(row)
        except Exception as exc:
            attempts = row["attempts"] + 1
            permanent = isinstance(exc, PermanentFailure) or attempts >= self.max_attempts
            backoff = timedelta(seconds=min(2**attempts, 300))
            await session.execute(
                update(t)
                .where(t.c.id == row["id"])
                .values(
                    attempts=attempts,
                    status=FAILED if permanent else PENDING,
                    next_attempt_at=func.now() + backoff,
                    last_error=f"{type(exc).__name__}: {exc}"[:2000],
                )
            )
            log.warning(
                "outbox_delivery_failed", id=row["id"], target=row["target"], permanent=permanent
            )
        else:
            await session.execute(
                update(t).where(t.c.id == row["id"]).values(status=SENT, sent_at=func.now())
            )

    async def _dispatch(self, row: RowMapping) -> None:
        if row["kind"] == "http":
            service, method, path = row["target"].split(" ", 2)
            response = await self.client.request(
                service,
                method,
                path,
                json=row["payload"],
                idempotency_key=row["dedup_key"],
            )
            if 400 <= response.status_code < 500:
                raise PermanentFailure(f"{response.status_code} {response.text[:500]}")
            return
        if self.bus is None:
            raise RuntimeError("未连接消息总线")
        await self.bus.publish(
            row["target"], row["payload"] or {}, message_id=f"{self.service}:{row['id']}"
        )

    async def run_forever(self, interval: float = 1.0) -> None:
        while True:
            try:
                processed = await self.run_once()
            except Exception:
                log.exception("outbox_relay_error")
                processed = 0
            await asyncio.sleep(0 if processed >= self.batch else interval)

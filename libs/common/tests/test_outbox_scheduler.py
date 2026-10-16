"""Outbox 投递与定时任务互斥（NFR-08），使用真实 PostgreSQL。"""

import asyncio
from collections.abc import AsyncIterator
from typing import Any

import httpx
import pytest
from sqlalchemy import MetaData, select, text, update

from campus_common.clock import SystemClock
from campus_common.config import ServiceName
from campus_common.db import Database
from campus_common.outbox import Outbox, OutboxRelay, outbox_table
from campus_common.scheduler import Job, JobContext, Scheduler

pytestmark = pytest.mark.integration

metadata = MetaData(schema="t_outbox")
table = outbox_table(metadata)


class FakeClient:
    """记录调用；按预设返回状态码或抛出连接错误。"""

    def __init__(self) -> None:
        self.calls: list[tuple[ServiceName, str, str, Any]] = []
        self.responses: list[int | Exception] = []

    async def request(
        self, service: ServiceName, method: str, path: str, **kwargs: Any
    ) -> httpx.Response:
        self.calls.append((service, method, path, kwargs.get("json")))
        outcome = self.responses.pop(0) if self.responses else 200
        if isinstance(outcome, Exception):
            raise outcome
        return httpx.Response(outcome)


class FakeBus:
    def __init__(self) -> None:
        self.published: list[tuple[str, dict[str, Any]]] = []

    async def publish(self, routing_key: str, payload: dict[str, Any], *, message_id: str) -> None:
        self.published.append((routing_key, payload))


@pytest.fixture
async def db(pg_url: str) -> AsyncIterator[Database]:
    database = Database(pg_url)
    async with database.engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA IF EXISTS t_outbox CASCADE"))
        await conn.execute(text("CREATE SCHEMA t_outbox"))
        await conn.run_sync(metadata.create_all)
    yield database
    await database.dispose()


def relay_for(db: Database, client: FakeClient, bus: FakeBus) -> OutboxRelay:
    return OutboxRelay(db, table, service="test", client=client, bus=bus, max_attempts=3)


async def make_due(db: Database) -> None:
    """模拟退避时间已过。"""
    async with db.engine.begin() as conn:
        await conn.execute(update(table).values(next_attempt_at=text("now()")))


async def test_messages_are_written_only_when_business_transaction_commits(db: Database) -> None:
    outbox = Outbox(table)

    async def failing_business_transaction() -> None:
        async with db.sessionmaker() as session, session.begin():
            await outbox.publish(session, "audit.record", {"x": 1})
            raise RuntimeError("业务失败，回滚")

    with pytest.raises(RuntimeError):
        await failing_business_transaction()
    async with db.sessionmaker() as session:
        assert (await session.scalars(select(table.c.id))).all() == []


async def test_same_dedup_key_is_stored_once(db: Database) -> None:
    outbox = Outbox(table)
    async with db.sessionmaker() as session, session.begin():
        for _ in range(3):
            await outbox.call(
                session, service="seat", method="PUT", path="/b/1", body={}, dedup_key="k1"
            )
    async with db.sessionmaker() as session:
        assert len((await session.scalars(select(table.c.id))).all()) == 1


async def test_later_message_of_same_aggregate_waits_for_earlier_one(db: Database) -> None:
    outbox, client, bus = Outbox(table), FakeClient(), FakeBus()
    async with db.sessionmaker() as session, session.begin():
        await outbox.call(
            session, service="seat", method="PUT", path="/hold", dedup_key="a", aggregate="app:1"
        )
        await outbox.call(
            session, service="seat", method="PUT", path="/active", dedup_key="b", aggregate="app:1"
        )
    client.responses = [httpx.ConnectError("down")]
    relay = relay_for(db, client, bus)

    await relay.run_once()
    assert [c[2] for c in client.calls] == ["/hold"]
    async with db.sessionmaker() as session:
        assert await outbox.writeback_status(session, "app:1") == "SYNCING"

    await make_due(db)
    await relay.run_once()
    await relay.run_once()
    assert [c[2] for c in client.calls] == ["/hold", "/hold", "/active"]
    async with db.sessionmaker() as session:
        assert await outbox.writeback_status(session, "app:1") == "SYNCED"


async def test_client_error_fails_permanently_and_can_be_retried(db: Database) -> None:
    outbox, client, bus = Outbox(table), FakeClient(), FakeBus()
    async with db.sessionmaker() as session, session.begin():
        await outbox.call(
            session, service="seat", method="PUT", path="/x", dedup_key="c", aggregate="wo:9"
        )
    client.responses = [409]
    relay = relay_for(db, client, bus)
    await relay.run_once()
    async with db.sessionmaker() as session, session.begin():
        assert await outbox.writeback_status(session, "wo:9") == "FAILED"
        assert await outbox.retry_failed(session, "wo:9") == 1
    await relay.run_once()
    async with db.sessionmaker() as session:
        assert await outbox.writeback_status(session, "wo:9") == "SYNCED"


async def test_events_are_published_to_bus(db: Database) -> None:
    outbox, client, bus = Outbox(table), FakeClient(), FakeBus()
    async with db.sessionmaker() as session, session.begin():
        await outbox.publish(session, "m3.workorder.repairing", {"workOrderId": 5})
    await relay_for(db, client, bus).run_once()
    assert bus.published == [("m3.workorder.repairing", {"workOrderId": 5})]


async def test_same_job_never_runs_concurrently(db: Database) -> None:
    running = 0
    peak = 0

    async def slow(_: JobContext) -> None:
        nonlocal running, peak
        running += 1
        peak = max(peak, running)
        await asyncio.sleep(0.3)
        running -= 1

    scheduler = Scheduler(db, SystemClock(), state=None)
    scheduler.register([Job("demo.slow", 60, slow)])
    results = await asyncio.gather(scheduler.run("demo.slow"), scheduler.run("demo.slow"))
    assert sorted(results) == [False, True]
    assert peak == 1

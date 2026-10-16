"""定时任务：进程内 APScheduler（NFR-08）。

多实例部署时用 PostgreSQL advisory lock 保证同一任务同一时刻只执行一次。

定义任务（任务函数必须幂等，按「扫描到期项并处理」编写）：
    async def expire_unchecked(ctx: JobContext) -> None:
        now = ctx.clock.now()
        ...
    JOBS = [Job("m1.expire_unchecked", 60, expire_unchecked)]
非生产环境可经测试端点立即触发：POST /internal/<api>/v1/test/jobs/<name>
"""

from collections.abc import Awaitable, Callable, Iterable
from dataclasses import dataclass
from typing import Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from campus_common.clock import Clock
from campus_common.db import Database
from campus_common.logging import get_logger
from campus_common.tracing import trace_context

log = get_logger(__name__)


@dataclass
class JobContext:
    session: AsyncSession
    clock: Clock
    state: Any  # FastAPI app.state：可取 outbox、http、settings 等


@dataclass(frozen=True)
class Job:
    name: str
    seconds: int
    func: Callable[[JobContext], Awaitable[None]]


class Scheduler:
    def __init__(self, db: Database, clock: Clock, state: Any) -> None:
        self.db = db
        self.clock = clock
        self.state = state
        self.jobs: dict[str, Job] = {}
        self._scheduler: AsyncIOScheduler | None = None

    def register(self, jobs: Iterable[Job]) -> None:
        for job in jobs:
            self.jobs[job.name] = job

    async def run(self, name: str) -> bool:
        """执行一次任务；若另一实例正在执行同名任务则跳过并返回 False。"""
        job = self.jobs[name]
        async with self.db.sessionmaker() as session, session.begin():
            locked = await session.scalar(
                select(func.pg_try_advisory_xact_lock(func.hashtext(name)))
            )
            if not locked:
                return False
            with trace_context():
                await job.func(JobContext(session=session, clock=self.clock, state=self.state))
        return True

    async def _safe_run(self, name: str) -> None:
        try:
            await self.run(name)
        except Exception:
            log.exception("job_failed", job=name)

    def start(self) -> None:
        scheduler = AsyncIOScheduler(timezone="UTC")
        for job in self.jobs.values():
            scheduler.add_job(
                self._safe_run,
                "interval",
                seconds=job.seconds,
                args=[job.name],
                id=job.name,
                max_instances=1,
                coalesce=True,
            )
        scheduler.start()
        self._scheduler = scheduler

    def shutdown(self) -> None:
        if self._scheduler is not None and self._scheduler.running:
            self._scheduler.shutdown(wait=False)

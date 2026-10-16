"""服务应用工厂与接口通用模型。各服务的 main.py 只需描述自己的路由、任务与消息订阅。"""

import asyncio
from collections.abc import AsyncIterator, Awaitable, Callable, Sequence
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import Field
from sqlalchemy import Table, text

from campus_common.auth import PUBLIC, TokenVerifier
from campus_common.clock import AdjustableClock, Clock, SystemClock
from campus_common.config import ServiceSettings
from campus_common.db import Database
from campus_common.errors import AppError, NotFound, install_error_handlers
from campus_common.http import InternalClient
from campus_common.logging import configure_logging
from campus_common.models import ApiModel, Page, PageQuery
from campus_common.mq import MessageBus
from campus_common.outbox import Outbox, OutboxRelay
from campus_common.scheduler import Job, Scheduler
from campus_common.tracing import TraceMiddleware

__all__ = ["ApiModel", "Page", "PageQuery", "ServiceSpec", "create_service_app"]


def get_outbox(request: Request) -> Outbox:
    outbox: Outbox | None = request.app.state.outbox
    if outbox is None:
        raise RuntimeError("本服务未配置 outbox")
    return outbox


def get_internal_client(request: Request) -> InternalClient:
    client: InternalClient = request.app.state.http
    return client


def get_app_clock(request: Request) -> Clock:
    clock: Clock = request.app.state.clock
    return clock


OutboxDep = Annotated[Outbox, Depends(get_outbox)]
ClientDep = Annotated[InternalClient, Depends(get_internal_client)]
ClockDep = Annotated[Clock, Depends(get_app_clock)]

ConsumerSetup = Callable[[MessageBus, FastAPI], Awaitable[None]]


@dataclass
class ServiceSpec:
    settings: ServiceSettings
    title: str
    description: str
    routers: Sequence[APIRouter]
    outbox_table: Table | None = None
    jobs: Sequence[Job] = ()
    consumers: ConsumerSetup | None = None
    openapi_tags: list[dict[str, Any]] = field(default_factory=list)


class ClockUpdate(ApiModel):
    now: datetime | None = Field(None, description="把时钟设为指定时刻（带时区）")
    advance_seconds: int | None = Field(None, description="把时钟向前推进若干秒")
    reset: bool = Field(False, description="恢复为真实时间")


def _ops_router() -> APIRouter:
    router = APIRouter(include_in_schema=False, dependencies=[PUBLIC])

    @router.get("/health/live")
    async def live() -> dict[str, str]:
        return {"status": "ok"}

    @router.get("/health/ready")
    async def ready(request: Request) -> JSONResponse:
        try:
            async with request.app.state.db.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception:
            return JSONResponse({"status": "unavailable"}, status_code=503)
        return JSONResponse({"status": "ok"})

    @router.get("/version")
    async def version(request: Request) -> dict[str, str]:
        s: ServiceSettings = request.app.state.settings
        return {
            "service": s.service_name,
            "version": s.app_version,
            "gitSha": s.git_sha,
            "buildTime": s.build_time,
        }

    return router


def _test_router() -> APIRouter:
    """时间推进与立即触发任务，只在非生产环境挂载，网关不对外暴露（NFR-09）。"""
    router = APIRouter(prefix="/internal/test", include_in_schema=False, dependencies=[PUBLIC])

    def adjustable(request: Request) -> AdjustableClock:
        clock = request.app.state.clock
        if not isinstance(clock, AdjustableClock):
            raise AppError("当前环境不支持调整时间", code="CLOCK_FIXED")
        return clock

    @router.get("/clock")
    async def get_clock(request: Request) -> dict[str, Any]:
        clock = adjustable(request)
        return {"now": clock.now().isoformat(), "offsetSeconds": clock.offset.total_seconds()}

    @router.put("/clock")
    async def set_clock(request: Request, body: ClockUpdate) -> dict[str, Any]:
        clock = adjustable(request)
        if body.reset:
            clock.reset()
        if body.now is not None:
            clock.set(body.now)
        if body.advance_seconds is not None:
            clock.advance(timedelta(seconds=body.advance_seconds))
        return {"now": clock.now().isoformat(), "offsetSeconds": clock.offset.total_seconds()}

    @router.get("/jobs")
    async def list_jobs(request: Request) -> list[str]:
        return sorted(request.app.state.scheduler.jobs)

    @router.post("/jobs/{name}")
    async def run_job(request: Request, name: str) -> dict[str, bool]:
        scheduler: Scheduler = request.app.state.scheduler
        if name not in scheduler.jobs:
            raise NotFound(f"没有名为 {name} 的任务")
        return {"ran": await scheduler.run(name)}

    return router


def create_service_app(spec: ServiceSpec) -> FastAPI:
    settings = spec.settings
    configure_logging(settings.service_name, json=settings.env != "dev")

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        tasks: list[asyncio.Task[None]] = []
        if settings.background_tasks:
            await app.state.bus.connect()
            if spec.consumers is not None:
                await spec.consumers(app.state.bus, app)
            if app.state.relay is not None:
                tasks.append(asyncio.create_task(app.state.relay.run_forever()))
            app.state.scheduler.start()
        try:
            yield
        finally:
            for task in tasks:
                task.cancel()
            app.state.scheduler.shutdown()
            if settings.background_tasks:
                await app.state.bus.close()
            await app.state.http.aclose()
            await app.state.db.dispose()

    app = FastAPI(
        title=spec.title,
        description=spec.description,
        version=settings.app_version,
        lifespan=lifespan,
        openapi_tags=spec.openapi_tags or None,
    )
    state = app.state
    state.settings = settings
    state.db = Database(settings.database_url)
    state.clock = AdjustableClock() if settings.test_endpoints_enabled else SystemClock()
    state.verifier = TokenVerifier(
        jwks_url=None if settings.jwt_public_key else settings.jwks_url,
        public_key_pem=settings.jwt_public_key,
    )
    state.http = InternalClient(settings)
    state.bus = MessageBus(settings.rabbitmq_url, settings.service_name)
    state.outbox = Outbox(spec.outbox_table) if spec.outbox_table is not None else None
    state.relay = (
        OutboxRelay(
            state.db,
            spec.outbox_table,
            service=settings.service_name,
            client=state.http,
            bus=state.bus,
            max_attempts=settings.outbox_max_attempts,
        )
        if spec.outbox_table is not None
        else None
    )
    state.scheduler = Scheduler(state.db, state.clock, state)
    state.scheduler.register(spec.jobs)

    app.add_middleware(TraceMiddleware)
    install_error_handlers(app)
    app.include_router(_ops_router())
    for router in spec.routers:
        app.include_router(router)
    if settings.test_endpoints_enabled:
        app.include_router(_test_router())
    return app

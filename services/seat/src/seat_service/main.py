"""seat-service 入口：uvicorn --factory seat_service.main:create_app"""

from fastapi import FastAPI

from campus_common.api import ServiceSpec, create_service_app
from seat_service import consumers
from seat_service.api import (
    admin_bookings,
    blocks,
    bookings,
    checkin,
    extensions,
    history,
    ops,
    params,
    screen,
    search,
    violations,
)
from seat_service.config import Settings
from seat_service.db import OUTBOX
from seat_service.jobs import JOBS


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    return create_service_app(
        ServiceSpec(
            settings=settings,
            title="seat-service · M1 自习座位预约",
            description="需求：docs/requirements/m1-seat-reservation.md",
            # 静态路径（如 /bookings/history）须在 /bookings/{booking_id} 之前注册
            routers=[
                search.router,
                history.router,
                bookings.router,
                checkin.router,
                screen.router,
                violations.router,
                extensions.router,
                params.router,
                admin_bookings.router,
                ops.router,
                blocks.admin,
                blocks.internal,
                extensions.internal,
            ],
            outbox_table=OUTBOX,
            jobs=JOBS,
            consumers=consumers.setup,
        )
    )

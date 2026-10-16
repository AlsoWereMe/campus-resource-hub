"""seat-service 入口：uvicorn --factory seat_service.main:create_app"""

from fastapi import FastAPI

from campus_common.api import ServiceSpec, create_service_app
from seat_service import consumers
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
            routers=[],
            outbox_table=OUTBOX,
            jobs=JOBS,
            consumers=consumers.setup,
        )
    )

"""room-service 入口：uvicorn --factory room_service.main:create_app"""

from fastapi import FastAPI

from campus_common.api import ServiceSpec, create_service_app
from room_service import consumers
from room_service.api import admin, applications, approvals, eligibility, flows, rooms
from room_service.config import Settings
from room_service.db import OUTBOX
from room_service.jobs import JOBS


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    return create_service_app(
        ServiceSpec(
            settings=settings,
            title="room-service · M2 整教室预约与审批",
            description="需求：docs/requirements/m2-room-booking.md",
            routers=[
                rooms.router,
                eligibility.router,
                applications.router,
                approvals.router,
                flows.router,
                admin.router,
            ],
            outbox_table=OUTBOX,
            jobs=JOBS,
            consumers=consumers.setup,
        )
    )

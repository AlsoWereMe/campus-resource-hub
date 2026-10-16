"""platform-service 入口：uvicorn --factory platform_service.main:create_app"""

from fastapi import FastAPI

from campus_common.api import ServiceSpec, create_service_app
from platform_service.config import Settings
from platform_service.db import OUTBOX

TAGS: list[dict[str, str]] = []


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    app = create_service_app(
        ServiceSpec(
            settings=settings,
            title="platform-service · 公共层 D",
            description="身份与权限、空间与座位主数据、通知、审计。需求：docs/requirements/d-platform.md",
            routers=[],
            outbox_table=OUTBOX,
            openapi_tags=TAGS,
        )
    )
    return app

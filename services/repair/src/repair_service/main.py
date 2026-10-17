"""repair-service 入口：uvicorn --factory repair_service.main:create_app"""

from fastapi import FastAPI

from campus_common.api import ServiceSpec, create_service_app
from repair_service import consumers
from repair_service.api import acceptance, dispatch, repair, reports, sla, workbench
from repair_service.config import Settings
from repair_service.db import OUTBOX
from repair_service.jobs import JOBS


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    return create_service_app(
        ServiceSpec(
            settings=settings,
            title="repair-service · M3 物业报修工单",
            description="需求：docs/requirements/m3-repair.md",
            # 静态路径（如 /workorders/mine）须在 /workorders/{work_order_id} 之前注册
            routers=[
                reports.router,
                workbench.router,
                dispatch.router,
                repair.router,
                acceptance.router,
                sla.router,
            ],
            outbox_table=OUTBOX,
            jobs=JOBS,
            consumers=consumers.setup,
        )
    )

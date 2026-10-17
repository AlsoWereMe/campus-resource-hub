"""platform-service 入口：uvicorn --factory platform_service.main:create_app"""

from fastapi import FastAPI

from campus_common.api import ServiceSpec, create_service_app
from platform_service import consumers
from platform_service.audit import api as audit_api
from platform_service.config import Settings
from platform_service.db import OUTBOX
from platform_service.iam import auth_api, internal_api, query_api, roles_api, users_api
from platform_service.iam.security import PlatformVerifier
from platform_service.jobs import JOBS
from platform_service.notify import api as notify_api
from platform_service.space import hours_admin, read_api, rooms_admin, seats_admin

TAGS = [
    {"name": "IAM · 登录", "description": "登录、令牌、当前用户（已实现）"},
    {"name": "IAM · 内部", "description": "JWKS、服务凭证（已实现）；按角色查询用户（D-T01）"},
    {"name": "IAM · 用户与院系", "description": "任务 D-T02"},
    {"name": "IAM · 角色与授权", "description": "任务 D-T03"},
    {"name": "空间 · 查询", "description": "校区、楼宇、房间、座位（已实现）"},
    {"name": "空间 · 房间管理", "description": "任务 D-T06"},
    {"name": "空间 · 开放时间", "description": "任务 D-T07"},
    {"name": "空间 · 座位与标记", "description": "任务 D-T08"},
    {"name": "通知", "description": "任务 D-T05"},
    {"name": "审计", "description": "任务 D-T04"},
]


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    app = create_service_app(
        ServiceSpec(
            settings=settings,
            title="platform-service · 公共层 D",
            description="身份与权限、空间与座位主数据、通知、审计。需求：docs/requirements/d-platform.md",
            routers=[
                auth_api.router,
                internal_api.router,
                query_api.router,
                users_api.router,
                roles_api.router,
                read_api.router,
                rooms_admin.router,
                hours_admin.router,
                seats_admin.router,
                notify_api.router,
                audit_api.router,
            ],
            outbox_table=OUTBOX,
            jobs=JOBS,
            consumers=consumers.setup,
            openapi_tags=TAGS,
        )
    )
    app.state.verifier = PlatformVerifier(app.state.db, settings.jwt_public_key)
    return app

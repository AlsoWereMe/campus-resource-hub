"""platform-service 入口：uvicorn --factory platform_service.main:create_app"""

from fastapi import FastAPI

from campus_common.api import ServiceSpec, create_service_app
from platform_service.config import Settings
from platform_service.db import OUTBOX
from platform_service.iam import auth_api, internal_api
from platform_service.iam.security import PlatformVerifier
from platform_service.space import read_api

TAGS = [
    {"name": "IAM · 登录", "description": "登录、令牌、当前用户（已实现）"},
    {"name": "IAM · 内部", "description": "JWKS、服务凭证（已实现）；网关不对外暴露"},
    {"name": "空间 · 查询", "description": "校区、楼宇、房间、座位（已实现）"},
]


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    app = create_service_app(
        ServiceSpec(
            settings=settings,
            title="platform-service · 公共层 D",
            description="身份与权限、空间与座位主数据、通知、审计。需求：docs/requirements/d-platform.md",
            routers=[auth_api.router, internal_api.router, read_api.router],
            outbox_table=OUTBOX,
            openapi_tags=TAGS,
        )
    )
    app.state.verifier = PlatformVerifier(app.state.db, settings.jwt_public_key)
    return app

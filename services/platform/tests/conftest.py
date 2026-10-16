from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import httpx
import pytest
from fastapi import FastAPI

from campus_common.testing import (
    api_client,
    postgres_container,
    prepare_schemas,
    run_alembic,
    settings_for_tests,
)
from platform_service.config import Settings
from platform_service.db import SCHEMAS
from platform_service.main import create_app
from platform_service.seeds.base import seed_base

SERVICE_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def database_url() -> Iterator[str]:
    """真实 PostgreSQL，从空库执行全部迁移（同时验证迁移可从空库重放）。"""
    with postgres_container() as url:
        prepare_schemas(url, SCHEMAS)
        run_alembic(SERVICE_ROOT / "alembic.ini", url)
        yield url


@pytest.fixture(scope="session")
def settings(database_url: str) -> Settings:
    return settings_for_tests(
        "platform",
        database_url,
        Settings,
        initial_admin_password="admin-pass",
        service_client_secrets="seat:seat-secret,room:room-secret",
    )


@pytest.fixture
async def app(settings: Settings) -> AsyncIterator[FastAPI]:
    application = create_app(settings)
    async with application.state.db.sessionmaker() as session, session.begin():
        await seed_base(session, settings)
    yield application
    await application.state.db.dispose()


@pytest.fixture
async def client(app: FastAPI) -> AsyncIterator[httpx.AsyncClient]:
    async with api_client(app) as c:
        yield c

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
from seat_service.config import Settings
from seat_service.main import create_app

SERVICE_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def database_url() -> Iterator[str]:
    """真实 PostgreSQL，从空库执行全部迁移。"""
    with postgres_container() as url:
        prepare_schemas(url, ["m1"], {"btree_gist": "m1"})
        run_alembic(SERVICE_ROOT / "alembic.ini", url)
        yield url


@pytest.fixture(scope="session")
def settings(database_url: str) -> Settings:
    return settings_for_tests("seat", database_url, Settings)


@pytest.fixture
async def app(settings: Settings) -> AsyncIterator[FastAPI]:
    application = create_app(settings)
    yield application
    await application.state.db.dispose()


@pytest.fixture
async def client(app: FastAPI) -> AsyncIterator[httpx.AsyncClient]:
    async with api_client(app) as c:
        yield c

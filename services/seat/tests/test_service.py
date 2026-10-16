"""服务骨架：健康检查、版本、每个接口都声明了访问要求（IAM-ROLE-01）。"""

import httpx
import pytest
from fastapi import FastAPI

from campus_common.auth import undeclared_routes

pytestmark = pytest.mark.integration


async def test_ready_checks_database(client: httpx.AsyncClient) -> None:
    response = await client.get("/health/ready")
    assert response.json() == {"status": "ok"}


async def test_version_reports_service(client: httpx.AsyncClient) -> None:
    assert (await client.get("/version")).json()["service"] == "seat"


def test_every_route_declares_access(app: FastAPI) -> None:
    assert undeclared_routes(app) == []

"""服务骨架：健康检查、版本、每个接口都声明了访问要求（IAM-ROLE-01）。"""

import httpx
import pytest
from fastapi import FastAPI

from campus_common.auth import undeclared_routes
from campus_common.testing import auth_headers

pytestmark = pytest.mark.integration


async def test_ready_checks_database(client: httpx.AsyncClient) -> None:
    response = await client.get("/health/ready")
    assert response.json() == {"status": "ok"}


async def test_version_reports_service(client: httpx.AsyncClient) -> None:
    assert (await client.get("/version")).json()["service"] == "seat"


def test_every_route_declares_access(app: FastAPI) -> None:
    assert undeclared_routes(app) == []


async def test_static_paths_are_not_shadowed_by_id_routes(client: httpx.AsyncClient) -> None:
    """静态路径须先于 /{id} 注册，否则会被当成 ID 解析而返回 422。"""
    headers = auth_headers(perms=["m1:booking:view-own"])
    for path in [
        "/api/m1/v1/bookings/history",
        "/api/m1/v1/bookings/current",
    ]:
        response = await client.get(path, headers=headers)
        assert response.status_code not in (404, 422), (path, response.json())

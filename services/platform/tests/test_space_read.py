"""空间主数据查询与演示种子。"""

import httpx
import pytest
from fastapi import FastAPI
from sqlalchemy import func, select

from campus_common.testing import auth_headers
from platform_service.config import Settings
from platform_service.iam.models import User
from platform_service.seeds.base import seed_base
from platform_service.seeds.demo import seed_demo
from platform_service.space.models import Room, Seat

pytestmark = pytest.mark.integration

READER = auth_headers(perms=["space:read"])


async def test_rooms_can_be_filtered_by_study_open(client: httpx.AsyncClient) -> None:
    response = await client.get(
        "/api/space/v1/rooms", params={"studyOpen": "true", "size": 50}, headers=READER
    )
    codes = {r["code"] for r in response.json()["items"]}
    assert {"H3-101", "LIB-201"} <= codes
    assert "H3-301" not in codes  # 报告厅未开放自习


async def test_seats_filtered_by_tag_all_carry_it(client: httpx.AsyncClient) -> None:
    rooms = await client.get("/api/space/v1/rooms", params={"keyword": "H3-101"}, headers=READER)
    room_id = rooms.json()["items"][0]["id"]
    seats = await client.get(
        f"/api/space/v1/rooms/{room_id}/seats", params={"tag": "FIXED_OUTLET"}, headers=READER
    )
    assert seats.json()
    assert all("FIXED_OUTLET" in s["tags"] for s in seats.json())


async def test_reading_space_requires_permission(client: httpx.AsyncClient) -> None:
    response = await client.get("/api/space/v1/campuses", headers=auth_headers(perms=[]))
    assert response.status_code == 403


async def test_seeds_are_idempotent(app: FastAPI, settings: Settings) -> None:
    async def counts() -> tuple[int, int, int]:
        async with app.state.db.sessionmaker() as session:
            rooms = await session.scalar(select(func.count()).select_from(Room))
            seats = await session.scalar(select(func.count()).select_from(Seat))
            users = await session.scalar(select(func.count()).select_from(User))
        return rooms or 0, seats or 0, users or 0

    before = await counts()
    async with app.state.db.sessionmaker() as session, session.begin():
        await seed_base(session, settings)
        await seed_demo(session, settings)
    assert await counts() == before

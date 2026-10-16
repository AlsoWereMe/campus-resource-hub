"""统一错误结构与 traceId（NFR-12、NFR-13）。"""

from fastapi import APIRouter, FastAPI

from campus_common.api import ServiceSpec, create_service_app
from campus_common.auth import PUBLIC
from campus_common.config import ServiceSettings
from campus_common.errors import NotImplementedYet, RuleViolation
from campus_common.models import ApiModel
from campus_common.testing import api_client

TRACE = "0af7651916cd43dd8448eb211c80319c"


class BookingIn(ApiModel):
    seat_id: int
    hours: int


def make_app() -> FastAPI:
    router = APIRouter(dependencies=[PUBLIC])

    @router.post("/bookings")
    async def create(body: BookingIn) -> BookingIn:
        if body.hours > 4:
            raise RuleViolation("BR-02", "单次预约最长 4 小时", maxHours=4)
        return body

    @router.get("/stub")
    async def stub() -> None:
        raise NotImplementedYet("M1-T03")

    @router.get("/boom")
    async def boom() -> None:
        raise RuntimeError("unexpected")

    settings = ServiceSettings(service_name="seat", env="test", background_tasks=False)
    return create_service_app(
        ServiceSpec(settings=settings, title="t", description="", routers=[router])
    )


async def test_missing_fields_are_listed_by_camel_case_name() -> None:
    async with api_client(make_app()) as client:
        response = await client.post("/bookings", json={"hours": 2})
    body = response.json()
    assert response.status_code == 422
    assert body["code"] == "FIELD_REQUIRED"
    assert body["details"]["fields"] == ["seatId"]


async def test_invalid_field_type_reports_field_invalid() -> None:
    async with api_client(make_app()) as client:
        response = await client.post("/bookings", json={"seatId": "abc", "hours": 2})
    assert response.json()["code"] == "FIELD_INVALID"
    assert response.json()["details"]["fields"] == ["seatId"]


async def test_rule_violation_carries_rule_id() -> None:
    async with api_client(make_app()) as client:
        response = await client.post("/bookings", json={"seatId": 1, "hours": 5})
    body = response.json()
    assert response.status_code == 422
    assert body["code"] == "RULE_VIOLATION"
    assert body["details"] == {"rule": "BR-02", "maxHours": 4}


async def test_stub_points_to_task() -> None:
    async with api_client(make_app()) as client:
        response = await client.get("/stub")
    assert response.status_code == 501
    assert response.json()["details"]["task"] == "M1-T03"


async def test_trace_id_from_traceparent_is_echoed_in_header_and_error_body() -> None:
    headers = {"traceparent": f"00-{TRACE}-b7ad6b7169203331-01"}
    async with api_client(make_app()) as client:
        response = await client.get("/stub", headers=headers)
    assert response.headers["x-trace-id"] == TRACE
    assert response.json()["traceId"] == TRACE


async def test_unexpected_error_returns_500_with_same_trace_id() -> None:
    async with api_client(make_app()) as client:
        response = await client.get("/boom")
    assert response.status_code == 500
    assert response.json()["code"] == "INTERNAL_ERROR"
    assert response.json()["traceId"] == response.headers["x-trace-id"]

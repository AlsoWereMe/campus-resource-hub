"""IAM-AUTH-01 账号登录、IAM-AUTH-03 服务间身份的验收标准。"""

import secrets

import httpx
import pytest
from fastapi import FastAPI
from sqlalchemy import select

from campus_common.auth import TokenVerifier, undeclared_routes
from platform_service.iam.models import Role, User, UserRole
from platform_service.iam.security import hash_password

pytestmark = pytest.mark.integration

LOGIN = "/api/iam/v1/auth/login"


async def new_user(app: FastAPI, *, password: str = "Secret#123", status: str = "ACTIVE") -> str:
    """每个测试使用独立账号，互不影响锁定计数。"""
    username = f"u{secrets.token_hex(4)}"
    async with app.state.db.sessionmaker() as session, session.begin():
        user = User(
            username=username,
            password_hash=hash_password(password),
            name="测试账号",
            user_type="student",
            status=status,
        )
        session.add(user)
        await session.flush()
        role = await session.scalar(select(Role).where(Role.code == "student"))
        assert role is not None
        session.add(UserRole(user_id=user.id, role_id=role.id))
    return username


async def login(client: httpx.AsyncClient, username: str, password: str) -> httpx.Response:
    return await client.post(LOGIN, json={"username": username, "password": password})


async def test_ac1_login_returns_tokens_and_me_shows_roles(
    app: FastAPI, client: httpx.AsyncClient
) -> None:
    username = await new_user(app)
    response = await login(client, username, "Secret#123")
    assert response.status_code == 200
    tokens = response.json()
    me = await client.get(
        "/api/iam/v1/me", headers={"Authorization": f"Bearer {tokens['accessToken']}"}
    )
    assert me.json()["roles"] == ["student"]
    assert "m1:booking:create" in me.json()["permissions"]


async def test_ac2_unknown_user_and_wrong_password_look_the_same(
    app: FastAPI, client: httpx.AsyncClient
) -> None:
    username = await new_user(app)
    wrong = await login(client, username, "nope")
    unknown = await login(client, "no-such-user", "nope")
    assert wrong.status_code == unknown.status_code == 401
    assert wrong.json()["code"] == unknown.json()["code"] == "INVALID_CREDENTIALS"
    assert wrong.json()["message"] == unknown.json()["message"]


async def test_ac3_five_failures_lock_the_account_for_fifteen_minutes(
    app: FastAPI, client: httpx.AsyncClient
) -> None:
    username = await new_user(app)
    for _ in range(5):
        await login(client, username, "nope")
    locked = await login(client, username, "Secret#123")
    assert locked.json()["code"] == "ACCOUNT_LOCKED"

    await client.put("/internal/test/clock", json={"advanceSeconds": 15 * 60 + 1})
    try:
        assert (await login(client, username, "Secret#123")).status_code == 200
    finally:
        await client.put("/internal/test/clock", json={"reset": True})


async def test_ac4_refresh_rotates_and_logout_revokes(
    app: FastAPI, client: httpx.AsyncClient
) -> None:
    username = await new_user(app)
    first = (await login(client, username, "Secret#123")).json()
    refreshed = await client.post(
        "/api/iam/v1/auth/refresh", json={"refreshToken": first["refreshToken"]}
    )
    assert refreshed.status_code == 200
    reused = await client.post(
        "/api/iam/v1/auth/refresh", json={"refreshToken": first["refreshToken"]}
    )
    assert reused.json()["code"] == "INVALID_REFRESH_TOKEN"

    second = refreshed.json()["refreshToken"]
    await client.post("/api/iam/v1/auth/logout", json={"refreshToken": second})
    after_logout = await client.post("/api/iam/v1/auth/refresh", json={"refreshToken": second})
    assert after_logout.status_code == 401


async def test_password_change_invalidates_old_password(
    app: FastAPI, client: httpx.AsyncClient
) -> None:
    username = await new_user(app)
    token = (await login(client, username, "Secret#123")).json()["accessToken"]
    headers = {"Authorization": f"Bearer {token}"}
    wrong_old = await client.post(
        "/api/iam/v1/auth/password",
        json={"oldPassword": "nope", "newPassword": "Another#456"},
        headers=headers,
    )
    assert wrong_old.status_code == 401
    changed = await client.post(
        "/api/iam/v1/auth/password",
        json={"oldPassword": "Secret#123", "newPassword": "Another#456"},
        headers=headers,
    )
    assert changed.status_code == 204
    assert (await login(client, username, "Secret#123")).status_code == 401
    assert (await login(client, username, "Another#456")).status_code == 200


async def test_disabled_account_cannot_login(app: FastAPI, client: httpx.AsyncClient) -> None:
    username = await new_user(app, status="DISABLED")
    assert (await login(client, username, "Secret#123")).json()["code"] == "ACCOUNT_DISABLED"


async def test_login_token_verifies_through_jwks(app: FastAPI, client: httpx.AsyncClient) -> None:
    username = await new_user(app)
    token = (await login(client, username, "Secret#123")).json()["accessToken"]
    verifier = TokenVerifier(jwks_url="http://test/internal/iam/v1/jwks", http=client)
    assert (await verifier.verify(token)).subject.isdigit()


async def test_service_token_carries_service_permissions(client: httpx.AsyncClient) -> None:
    ok = await client.post(
        "/internal/iam/v1/service-token", json={"clientId": "room", "clientSecret": "room-secret"}
    )
    bad = await client.post(
        "/internal/iam/v1/service-token", json={"clientId": "room", "clientSecret": "guess"}
    )
    assert ok.status_code == 200
    assert bad.json()["code"] == "INVALID_CLIENT"
    verifier = TokenVerifier(jwks_url="http://test/internal/iam/v1/jwks", http=client)
    principal = await verifier.verify(ok.json()["accessToken"])
    assert principal.kind == "service"
    assert principal.has("m1:block:write")


def test_every_route_declares_access(app: FastAPI) -> None:
    assert undeclared_routes(app) == []

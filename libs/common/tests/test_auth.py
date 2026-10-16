"""令牌、权限点与数据范围（IAM-ROLE-01、03，IAM-AUTH-03）。"""

from datetime import timedelta

import httpx
import pytest
from fastapi import APIRouter, FastAPI

from campus_common.api import ServiceSpec, create_service_app
from campus_common.auth import (
    AUTHENTICATED,
    Grant,
    Principal,
    Scope,
    TokenSigner,
    TokenVerifier,
    require,
    undeclared_routes,
)
from campus_common.config import ServiceSettings
from campus_common.errors import Unauthorized
from campus_common.testing import api_client, auth_headers, signer_for_tests


def principal(**overrides: object) -> Principal:
    data: dict[str, object] = {
        "subject": "7",
        "kind": "user",
        "name": "张三",
        "roles": ["room_admin"],
        "grants": [
            Grant(perms=["m1:booking:view-all"], buildings=[1]),
            Grant(perms=["m1:booking:view-all", "m1:stats:view"], departments=[9]),
        ],
        "user_type": "staff",
        "department_id": 9,
    }
    data.update(overrides)
    return Principal.model_validate(data)


def test_scope_is_union_of_grants_holding_the_permission() -> None:
    p = principal()
    assert p.scope("m1:booking:view-all") == Scope(
        buildings=frozenset({1}), departments=frozenset({9})
    )
    assert p.scope("m1:stats:view").covers(department_id=9)
    assert not p.scope("m1:stats:view").covers(building_id=1)
    assert p.scope("m1:setting:manage").empty


def test_all_scope_covers_everything() -> None:
    assert Scope(all=True).covers(building_id=42)
    assert not Scope().covers(building_id=42, department_id=1)


async def test_signed_token_round_trips_through_static_key() -> None:
    signer = signer_for_tests()
    verifier = TokenVerifier(public_key_pem=signer.public_key_pem())
    original = principal()
    restored = await verifier.verify(signer.sign(original, timedelta(minutes=5)))
    assert restored == original
    assert restored.user_id == 7


async def test_expired_token_is_rejected_with_specific_code() -> None:
    signer = signer_for_tests()
    verifier = TokenVerifier(public_key_pem=signer.public_key_pem())
    token = signer.sign(principal(), timedelta(seconds=-1))
    with pytest.raises(Unauthorized) as info:
        await verifier.verify(token)
    assert info.value.code == "TOKEN_EXPIRED"


async def test_token_from_another_key_is_rejected() -> None:
    other = TokenSigner(TokenSigner.generate_private_key_pem(), kid="other")
    verifier = TokenVerifier(public_key_pem=signer_for_tests().public_key_pem())
    with pytest.raises(Unauthorized):
        await verifier.verify(other.sign(principal(), timedelta(minutes=5)))


async def test_jwks_keys_are_fetched_and_unknown_kid_rejected() -> None:
    signer = signer_for_tests()
    jwks = {"keys": [signer.public_jwk()]}
    transport = httpx.MockTransport(lambda _: httpx.Response(200, json=jwks))
    async with httpx.AsyncClient(transport=transport) as http:
        verifier = TokenVerifier(jwks_url="http://iam/jwks", http=http)
        assert (
            await verifier.verify(signer.sign(principal(), timedelta(minutes=5)))
        ).name == "张三"
        stranger = TokenSigner(TokenSigner.generate_private_key_pem(), kid="stranger")
        with pytest.raises(Unauthorized):
            await verifier.verify(stranger.sign(principal(), timedelta(minutes=5)))


def make_app(*, declare: bool = True) -> FastAPI:
    router = APIRouter()

    @router.get("/stats")
    async def stats(p: Principal = require("m1:stats:view")) -> dict[str, str]:
        return {"who": p.name}

    @router.get("/me")
    async def me(p: Principal = AUTHENTICATED) -> dict[str, str]:
        return {"who": p.subject}

    if not declare:

        @router.get("/forgotten")
        async def forgotten() -> None:
            return None

    settings = ServiceSettings(
        service_name="seat",
        env="test",
        background_tasks=False,
        jwt_public_key=signer_for_tests().public_key_pem(),
    )
    return create_service_app(
        ServiceSpec(settings=settings, title="t", description="", routers=[router])
    )


async def test_require_rejects_missing_token_and_missing_permission() -> None:
    async with api_client(make_app()) as client:
        anonymous = await client.get("/stats")
        without = await client.get("/stats", headers=auth_headers(perms=["m1:seat:search"]))
        allowed = await client.get("/stats", headers=auth_headers(perms=["m1:stats:view"]))
    assert anonymous.status_code == 401
    assert without.status_code == 403
    assert without.json()["details"]["permission"] == "m1:stats:view"
    assert allowed.status_code == 200


def test_routes_without_access_declaration_are_detected() -> None:
    assert undeclared_routes(make_app()) == []
    assert undeclared_routes(make_app(declare=False)) == ["['GET'] /forgotten"]

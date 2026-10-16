"""JWKS 与服务凭证（IAM-AUTH-03）。骨架已实现。网关不对外暴露 /internal/**。"""

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Request
from sqlalchemy import select

from campus_common.auth import PUBLIC, Grant, Principal, TokenSigner
from campus_common.contracts.iam import ServiceTokenRequest, TokenResponse
from campus_common.db import SessionDep
from campus_common.errors import Unauthorized
from campus_common.models import ApiModel
from platform_service.iam.models import ServiceClient, SigningKey
from platform_service.iam.security import get_signer, verify_password

router = APIRouter(prefix="/internal/iam/v1", tags=["IAM · 内部"])

SERVICE_TOKEN_MINUTES = 15


class Jwks(ApiModel):
    keys: list[dict[str, Any]]


@router.get("/jwks", dependencies=[PUBLIC], summary="令牌验签公钥（JWKS）")
async def jwks(request: Request, session: SessionDep) -> Jwks:
    await get_signer(request.app.state, session)  # 确保至少有一把密钥
    keys = (await session.scalars(select(SigningKey).where(SigningKey.active.is_(True)))).all()
    return Jwks(keys=[TokenSigner(k.private_pem, k.kid).public_jwk() for k in keys])


@router.post("/service-token", dependencies=[PUBLIC], summary="用服务凭证换取服务令牌")
async def service_token(
    body: ServiceTokenRequest, request: Request, session: SessionDep
) -> TokenResponse:
    client = await session.get(ServiceClient, body.client_id)
    if client is None or not verify_password(client.secret_hash, body.client_secret):
        raise Unauthorized("服务凭证无效", code="INVALID_CLIENT")
    principal = Principal(
        subject=f"svc:{client.client_id}",
        kind="service",
        name=client.client_id,
        grants=[Grant(perms=sorted(client.permissions), all=True)],
    )
    signer = await get_signer(request.app.state, session)
    return TokenResponse(
        access_token=signer.sign(principal, timedelta(minutes=SERVICE_TOKEN_MINUTES)),
        expires_in=SERVICE_TOKEN_MINUTES * 60,
    )

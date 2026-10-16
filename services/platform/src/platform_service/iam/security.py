"""口令哈希、签名密钥、由用户角色构造令牌主体。"""

import hashlib
import secrets
from typing import Any

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError
from cryptography.hazmat.primitives import serialization
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from campus_common.auth import Grant, Principal, TokenSigner, TokenVerifier
from campus_common.db import Database
from campus_common.errors import Unauthorized
from platform_service.iam.models import Role, RolePermission, SigningKey, User, UserRole

_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    try:
        return _hasher.verify(password_hash, password)
    except (VerifyMismatchError, InvalidHashError):
        return False


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def new_refresh_token() -> str:
    return secrets.token_urlsafe(32)


async def get_signer(state: Any, session: AsyncSession) -> TokenSigner:
    """当前签名密钥；首次调用时生成并存库（多实例下用 advisory lock 防止重复生成）。"""
    cached: TokenSigner | None = getattr(state, "signer", None)
    if cached is not None:
        return cached
    query = (
        select(SigningKey).where(SigningKey.active.is_(True)).order_by(SigningKey.created_at.desc())
    )
    key = await session.scalar(query)
    if key is None:
        await session.execute(select(func.pg_advisory_xact_lock(func.hashtext("iam.signing_key"))))
        key = await session.scalar(query)
    if key is None:
        key = SigningKey(
            kid=secrets.token_hex(8), private_pem=TokenSigner.generate_private_key_pem()
        )
        session.add(key)
        await session.flush()
    signer = TokenSigner(key.private_pem, key.kid)
    state.signer = signer
    return signer


async def principal_for(session: AsyncSession, user: User) -> Principal:
    rows = await session.execute(
        select(UserRole, Role)
        .join(Role, Role.id == UserRole.role_id)
        .where(UserRole.user_id == user.id, Role.enabled.is_(True))
        .order_by(Role.code)
    )
    roles: list[str] = []
    grants: list[Grant] = []
    for user_role, role in rows:
        perms = (
            await session.scalars(
                select(RolePermission.permission).where(RolePermission.role_id == role.id)
            )
        ).all()
        roles.append(role.code)
        grants.append(
            Grant(
                perms=sorted(perms),
                all=user_role.scope_all,
                buildings=list(user_role.scope_buildings),
                departments=list(user_role.scope_departments),
            )
        )
    return Principal(
        subject=str(user.id),
        kind="user",
        name=user.name,
        roles=roles,
        grants=grants,
        user_type="staff" if user.user_type == "staff" else "student",
        department_id=user.department_id,
    )


class PlatformVerifier(TokenVerifier):
    """platform 自己校验令牌时直接读库中的公钥，不经 HTTP 调自己的 JWKS。

    测试环境额外接受测试密钥（kid=test）签发的令牌。
    """

    def __init__(self, db: Database, test_public_key: str | None) -> None:
        super().__init__()
        self._db = db
        self._test_key = (
            serialization.load_pem_public_key(test_public_key.encode()) if test_public_key else None
        )

    async def _key_for(self, kid: str | None) -> Any:
        if kid == "test" and self._test_key is not None:
            return self._test_key
        if kid not in self._keys:
            async with self._db.sessionmaker() as session:
                keys = (await session.scalars(select(SigningKey))).all()
            self._keys = {
                k.kid: serialization.load_pem_public_key(
                    TokenSigner(k.private_pem, k.kid).public_key_pem().encode()
                )
                for k in keys
            }
        if kid not in self._keys:
            raise Unauthorized("令牌签名密钥未知")
        return self._keys[kid]

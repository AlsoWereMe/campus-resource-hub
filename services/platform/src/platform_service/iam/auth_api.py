"""登录、令牌刷新、登出、修改口令、当前用户（IAM-AUTH-01）。骨架已实现。"""

from datetime import timedelta

from fastapi import APIRouter, Request
from pydantic import Field
from sqlalchemy import select, update

from campus_common.api import ClockDep
from campus_common.auth import AUTHENTICATED, PUBLIC, Principal
from campus_common.clock import to_business
from campus_common.contracts.iam import TokenResponse
from campus_common.db import Database, SessionDep
from campus_common.errors import Unauthorized
from campus_common.models import ApiModel
from platform_service.config import Settings
from platform_service.iam.models import Department, RefreshToken, User
from platform_service.iam.security import (
    get_signer,
    hash_password,
    hash_token,
    new_refresh_token,
    principal_for,
    verify_password,
)

router = APIRouter(prefix="/api/iam/v1", tags=["IAM · 登录"])

INVALID = "用户名或密码错误"


class LoginIn(ApiModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=128)


class RefreshIn(ApiModel):
    refresh_token: str


class PasswordChangeIn(ApiModel):
    old_password: str
    new_password: str = Field(min_length=8, max_length=128)


class MeOut(ApiModel):
    id: int
    username: str
    name: str
    user_type: str
    department_id: int | None
    department_name: str | None
    email: str | None
    roles: list[str]
    permissions: list[str]


async def _issue(request: Request, session: SessionDep, user: User) -> TokenResponse:
    settings: Settings = request.app.state.settings
    clock = request.app.state.clock
    signer = await get_signer(request.app.state, session)
    principal = await principal_for(session, user)
    refresh = new_refresh_token()
    session.add(
        RefreshToken(
            user_id=user.id,
            token_hash=hash_token(refresh),
            expires_at=clock.now() + timedelta(days=settings.refresh_token_days),
        )
    )
    return TokenResponse(
        access_token=signer.sign(principal, timedelta(minutes=settings.access_token_minutes)),
        expires_in=settings.access_token_minutes * 60,
        refresh_token=refresh,
    )


@router.post("/auth/login", dependencies=[PUBLIC], summary="账号登录（IAM-AUTH-01）")
async def login(body: LoginIn, request: Request, clock: ClockDep) -> TokenResponse:
    """连续失败达到上限后锁定一段时间；用户不存在与口令错误返回同一种错误。"""
    settings: Settings = request.app.state.settings
    db: Database = request.app.state.db
    now = clock.now()
    error: Unauthorized | None = None
    async with db.sessionmaker() as session, session.begin():
        user = await session.scalar(
            select(User).where(User.username == body.username).with_for_update()
        )
        if user is None:
            error = Unauthorized(INVALID, code="INVALID_CREDENTIALS")
        elif user.locked_until is not None and user.locked_until > now:
            until = to_business(user.locked_until)
            error = Unauthorized(
                f"连续登录失败次数过多，账号已锁定，请于 {until:%H:%M} 后再试",
                code="ACCOUNT_LOCKED",
                details={"lockedUntil": until.isoformat()},
            )
        elif not verify_password(user.password_hash, body.password):
            user.failed_logins += 1
            if user.failed_logins > settings.max_failed_logins:
                user.failed_logins = 0
                user.locked_until = now + timedelta(minutes=settings.lock_minutes)
            error = Unauthorized(INVALID, code="INVALID_CREDENTIALS")
        elif user.status != "ACTIVE":
            error = Unauthorized("账号已停用，请联系管理员", code="ACCOUNT_DISABLED")
        else:
            user.failed_logins = 0
            user.locked_until = None
            return await _issue(request, session, user)
    raise error or Unauthorized(INVALID, code="INVALID_CREDENTIALS")


@router.post("/auth/refresh", dependencies=[PUBLIC], summary="用刷新令牌换取新令牌（IAM-AUTH-01）")
async def refresh(body: RefreshIn, request: Request, session: SessionDep) -> TokenResponse:
    """刷新令牌一次性使用：换取新令牌后旧刷新令牌立即失效。"""
    clock = request.app.state.clock
    token = await session.scalar(
        select(RefreshToken).where(RefreshToken.token_hash == hash_token(body.refresh_token))
    )
    if token is None or token.revoked_at is not None or token.expires_at <= clock.now():
        raise Unauthorized("刷新令牌无效或已过期，请重新登录", code="INVALID_REFRESH_TOKEN")
    user = await session.get(User, token.user_id)
    if user is None or user.status != "ACTIVE":
        raise Unauthorized("账号已停用，请联系管理员", code="ACCOUNT_DISABLED")
    token.revoked_at = clock.now()
    return await _issue(request, session, user)


@router.post("/auth/logout", status_code=204, dependencies=[PUBLIC], summary="登出（IAM-AUTH-01）")
async def logout(body: RefreshIn, request: Request, session: SessionDep) -> None:
    await session.execute(
        update(RefreshToken)
        .where(
            RefreshToken.token_hash == hash_token(body.refresh_token),
            RefreshToken.revoked_at.is_(None),
        )
        .values(revoked_at=request.app.state.clock.now())
    )


@router.post("/auth/password", status_code=204, summary="修改口令（IAM-AUTH-01）")
async def change_password(
    body: PasswordChangeIn,
    request: Request,
    session: SessionDep,
    principal: Principal = AUTHENTICATED,
) -> None:
    """修改成功后，该用户所有刷新令牌失效。"""
    user = await session.get(User, principal.user_id)
    if user is None or not verify_password(user.password_hash, body.old_password):
        raise Unauthorized("原口令不正确", code="INVALID_CREDENTIALS")
    user.password_hash = hash_password(body.new_password)
    await session.execute(
        update(RefreshToken)
        .where(RefreshToken.user_id == user.id, RefreshToken.revoked_at.is_(None))
        .values(revoked_at=request.app.state.clock.now())
    )


@router.get("/me", summary="当前用户、角色与权限点")
async def me(session: SessionDep, principal: Principal = AUTHENTICATED) -> MeOut:
    user = await session.get(User, principal.user_id)
    if user is None:
        raise Unauthorized("用户不存在")
    department = await session.get(Department, user.department_id) if user.department_id else None
    return MeOut(
        id=user.id,
        username=user.username,
        name=user.name,
        user_type=user.user_type,
        department_id=user.department_id,
        department_name=department.name if department else None,
        email=user.email,
        roles=principal.roles,
        permissions=sorted(principal.perms),
    )

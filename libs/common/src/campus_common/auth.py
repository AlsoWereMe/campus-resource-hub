"""鉴权：JWT 验签、调用者身份（Principal）、权限点与数据范围校验（IAM-ROLE-01、03，NFR-10）。

在路由上声明访问要求，三选一（测试会检查每个接口都声明了）：
    principal: Principal = require("m1:booking:create")   # 需要权限点
    principal: Principal = AUTHENTICATED                    # 任何已登录用户
    @router.get(..., dependencies=[PUBLIC])                 # 无需登录
数据范围：principal.scope("m1:booking:view-all").covers(building_id=...)
"""

import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any, Literal

import httpx
import jwt
import structlog
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import Depends, FastAPI, Request
from fastapi.routing import APIRoute, iter_route_contexts
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from campus_common.errors import Forbidden, Unauthorized

ISSUER = "campus-iam"


@dataclass(frozen=True)
class Scope:
    """数据范围：全校，或若干楼宇 / 院系。"""

    all: bool = False
    buildings: frozenset[int] = frozenset()
    departments: frozenset[int] = frozenset()

    def covers(self, *, building_id: int | None = None, department_id: int | None = None) -> bool:
        if self.all:
            return True
        if building_id is not None and building_id in self.buildings:
            return True
        return department_id is not None and department_id in self.departments

    def union(self, other: "Scope") -> "Scope":
        return Scope(
            all=self.all or other.all,
            buildings=self.buildings | other.buildings,
            departments=self.departments | other.departments,
        )

    @property
    def empty(self) -> bool:
        return not (self.all or self.buildings or self.departments)


class Grant(BaseModel):
    """一个角色授予的权限点及其数据范围。"""

    perms: list[str]
    all: bool = False
    buildings: list[int] = Field(default_factory=list)
    departments: list[int] = Field(default_factory=list)


class Principal(BaseModel):
    """调用者：用户或服务。"""

    subject: str = Field(description="用户为数字 ID 的字符串，服务为 svc:<服务名>")
    kind: Literal["user", "service"]
    name: str
    roles: list[str] = Field(default_factory=list)
    grants: list[Grant] = Field(default_factory=list)
    user_type: Literal["student", "staff"] | None = None
    department_id: int | None = None

    @property
    def user_id(self) -> int:
        if self.kind != "user":
            raise Forbidden("该操作只允许用户调用")
        return int(self.subject)

    @property
    def perms(self) -> set[str]:
        return {p for g in self.grants for p in g.perms}

    def has(self, permission: str) -> bool:
        return permission in self.perms

    def scope(self, permission: str) -> Scope:
        result = Scope()
        for g in self.grants:
            if permission in g.perms:
                result = result.union(
                    Scope(g.all, frozenset(g.buildings), frozenset(g.departments))
                )
        return result

    def to_claims(self) -> dict[str, Any]:
        return {
            "sub": self.subject,
            "typ": self.kind,
            "name": self.name,
            "roles": self.roles,
            "grants": [g.model_dump() for g in self.grants],
            "utype": self.user_type,
            "dept": self.department_id,
        }

    @classmethod
    def from_claims(cls, claims: dict[str, Any]) -> "Principal":
        return cls(
            subject=claims["sub"],
            kind=claims.get("typ", "user"),
            name=claims.get("name", ""),
            roles=claims.get("roles", []),
            grants=[Grant.model_validate(g) for g in claims.get("grants", [])],
            user_type=claims.get("utype"),
            department_id=claims.get("dept"),
        )


class TokenSigner:
    """签发 RS256 令牌。只有 IAM 与测试使用。令牌时间一律用真实时间，不受业务时钟影响。"""

    def __init__(self, private_key_pem: str, kid: str) -> None:
        key = serialization.load_pem_private_key(private_key_pem.encode(), password=None)
        if not isinstance(key, rsa.RSAPrivateKey):
            raise TypeError("需要 RSA 私钥")
        self._key = key
        self.kid = kid

    @staticmethod
    def generate_private_key_pem() -> str:
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        return key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        ).decode()

    def public_key_pem(self) -> str:
        return (
            self._key.public_key()
            .public_bytes(
                serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo
            )
            .decode()
        )

    def public_jwk(self) -> dict[str, Any]:
        jwk: dict[str, Any] = jwt.algorithms.RSAAlgorithm.to_jwk(
            self._key.public_key(), as_dict=True
        )
        return {**jwk, "kid": self.kid, "use": "sig", "alg": "RS256"}

    def sign(self, principal: Principal, ttl: timedelta) -> str:
        now = datetime.now(UTC)
        claims = {
            **principal.to_claims(),
            "iss": ISSUER,
            "iat": now,
            "exp": now + ttl,
            "jti": secrets.token_hex(8),
        }
        return jwt.encode(claims, self._key, algorithm="RS256", headers={"kid": self.kid})


class TokenVerifier:
    """校验令牌。生产中经 JWKS 获取 IAM 公钥并缓存；测试中可直接给公钥。"""

    def __init__(
        self,
        *,
        jwks_url: str | None = None,
        public_key_pem: str | None = None,
        http: httpx.AsyncClient | None = None,
        cache_seconds: int = 300,
    ) -> None:
        self._jwks_url = jwks_url
        self._static_key = (
            serialization.load_pem_public_key(public_key_pem.encode()) if public_key_pem else None
        )
        self._http = http
        self._cache_seconds = cache_seconds
        self._keys: dict[str, Any] = {}
        self._fetched_at: datetime | None = None

    async def verify(self, token: str) -> Principal:
        try:
            header = jwt.get_unverified_header(token)
        except jwt.PyJWTError as exc:
            raise Unauthorized("令牌格式无效") from exc
        key = await self._key_for(header.get("kid"))
        try:
            claims = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                issuer=ISSUER,
                options={"require": ["exp", "iat", "sub"]},
            )
        except jwt.ExpiredSignatureError as exc:
            raise Unauthorized("登录已过期，请刷新令牌或重新登录", code="TOKEN_EXPIRED") from exc
        except jwt.PyJWTError as exc:
            raise Unauthorized("令牌无效") from exc
        return Principal.from_claims(claims)

    async def _key_for(self, kid: str | None) -> Any:
        if self._static_key is not None:
            return self._static_key
        stale = self._fetched_at is None or (
            datetime.now(UTC) - self._fetched_at > timedelta(seconds=self._cache_seconds)
        )
        if kid not in self._keys or stale:
            await self._refresh()
        if kid not in self._keys:
            raise Unauthorized("令牌签名密钥未知")
        return self._keys[kid]

    async def _refresh(self) -> None:
        if not self._jwks_url:
            raise Unauthorized("未配置 JWKS 地址")
        client = self._http or httpx.AsyncClient(timeout=5)
        try:
            response = await client.get(self._jwks_url)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise Unauthorized("暂时无法校验令牌（IAM 不可用）", code="IAM_UNAVAILABLE") from exc
        finally:
            if self._http is None:
                await client.aclose()
        self._keys = {k["kid"]: jwt.PyJWK(k).key for k in response.json().get("keys", [])}
        self._fetched_at = datetime.now(UTC)


_bearer = HTTPBearer(auto_error=False, description="IAM 签发的访问令牌")


async def current_principal(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> Principal:
    if credentials is None:
        raise Unauthorized("请先登录")
    verifier: TokenVerifier = request.app.state.verifier
    principal = await verifier.verify(credentials.credentials)
    request.state.principal = principal
    structlog.contextvars.bind_contextvars(actor=principal.subject)
    return principal


class Require:
    """路由依赖：调用者必须持有指定权限点。"""

    def __init__(self, permission: str) -> None:
        self.permission = permission

    async def __call__(self, principal: Principal = Depends(current_principal)) -> Principal:
        if not principal.has(self.permission):
            raise Forbidden(
                f"缺少权限点 {self.permission}", details={"permission": self.permission}
            )
        return principal


class Authenticated:
    """路由依赖：任何已登录的调用者。"""

    async def __call__(self, principal: Principal = Depends(current_principal)) -> Principal:
        return principal


class Public:
    """路由依赖标记：无需登录（登录、JWKS、健康检查、屏幕端等）。"""

    async def __call__(self) -> None:
        return None


def require(permission: str) -> Any:
    return Depends(Require(permission))


AUTHENTICATED: Any = Depends(Authenticated())
PUBLIC: Any = Depends(Public())


def declared_access(route: Any) -> str | None:
    """返回路由声明的访问要求：权限点、authenticated、public；未声明返回 None。"""
    dependant = getattr(route, "dependant", None)
    stack = list(dependant.dependencies) if dependant is not None else []
    while stack:
        dep = stack.pop()
        if isinstance(dep.call, Require):
            return dep.call.permission
        if isinstance(dep.call, Authenticated):
            return "authenticated"
        if isinstance(dep.call, Public):
            return "public"
        stack.extend(dep.dependencies)
    return None


def api_routes(app: FastAPI) -> list[Any]:
    """展开应用中的全部接口（含 include_router 进来的），每项有 path、methods、dependant。"""
    return [
        ctx for ctx in iter_route_contexts(app.routes) if isinstance(ctx.original_route, APIRoute)
    ]


def undeclared_routes(app: FastAPI) -> list[str]:
    """列出没有声明访问要求的接口（IAM-ROLE-01 验收标准）。"""
    return [
        f"{sorted(r.methods or [])} {r.path}" for r in api_routes(app) if declared_access(r) is None
    ]

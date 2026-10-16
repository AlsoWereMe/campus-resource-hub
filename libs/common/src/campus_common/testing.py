"""测试工具：测试令牌、真实 PostgreSQL（Testcontainers）、迁移、测试客户端。

典型用法（服务的 tests/conftest.py）：
    prepare_schemas(database_url, ["m1"], {"btree_gist": "m1"})
    run_alembic(SERVICE_ROOT / "alembic.ini", database_url)
    app = create_app(settings_for_tests("seat", database_url))
    async with api_client(app) as client:
        await client.get("/api/m1/v1/...", headers=auth_headers(perms=["m1:seat:search"]))
"""

from collections.abc import AsyncIterator, Iterable, Iterator
from contextlib import asynccontextmanager, contextmanager
from datetime import timedelta
from functools import lru_cache
from pathlib import Path
from typing import Any

import httpx
from fastapi import FastAPI

from campus_common.auth import Grant, Principal, TokenSigner
from campus_common.config import ServiceName, ServiceSettings


@lru_cache(maxsize=1)
def signer_for_tests() -> TokenSigner:
    return TokenSigner(TokenSigner.generate_private_key_pem(), kid="test")


def token_for(
    *,
    perms: Iterable[str] = (),
    user_id: int = 1,
    name: str = "测试用户",
    roles: Iterable[str] = (),
    user_type: str = "student",
    department_id: int | None = 1,
    all_scope: bool = True,
    buildings: Iterable[int] = (),
    departments: Iterable[int] = (),
) -> str:
    """签发测试用的用户令牌。默认数据范围为全校。"""
    principal = Principal(
        subject=str(user_id),
        kind="user",
        name=name,
        roles=list(roles),
        grants=[
            Grant(
                perms=list(perms),
                all=all_scope,
                buildings=list(buildings),
                departments=list(departments),
            )
        ],
        user_type=user_type,
        department_id=department_id,
    )
    return signer_for_tests().sign(principal, timedelta(minutes=15))


def service_token_for(service: str, perms: Iterable[str]) -> str:
    principal = Principal(
        subject=f"svc:{service}",
        kind="service",
        name=service,
        grants=[Grant(perms=list(perms), all=True)],
    )
    return signer_for_tests().sign(principal, timedelta(minutes=15))


def auth_headers(**kwargs: Any) -> dict[str, str]:
    return {"Authorization": f"Bearer {token_for(**kwargs)}"}


def settings_for_tests(
    service: ServiceName, database_url: str, **overrides: Any
) -> ServiceSettings:
    return ServiceSettings(
        service_name=service,
        env="test",
        database_url=database_url,
        jwt_public_key=signer_for_tests().public_key_pem(),
        background_tasks=False,
        **overrides,
    )


@contextmanager
def postgres_container() -> Iterator[str]:
    """启动一个临时 PostgreSQL 16，返回超级用户连接串（postgresql+psycopg://…）。"""
    from testcontainers.community.postgres import PostgresContainer

    with PostgresContainer("postgres:16", driver="psycopg") as pg:
        yield pg.get_connection_url()


def prepare_schemas(
    database_url: str, schemas: Iterable[str], extensions: dict[str, str] | None = None
) -> None:
    """在测试库中创建 schema 与扩展（生产中由 deploy/postgres/init 完成）。"""
    import psycopg

    dsn = database_url.replace("postgresql+psycopg://", "postgresql://")
    with psycopg.connect(dsn, autocommit=True) as conn:
        for schema in schemas:
            conn.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')
        for ext, schema in (extensions or {}).items():
            conn.execute(f'CREATE EXTENSION IF NOT EXISTS "{ext}" SCHEMA "{schema}"')


def run_alembic(alembic_ini: Path, database_url: str) -> None:
    """把服务的迁移升级到最新（同步执行，须在事件循环之外调用）。"""
    from alembic import command
    from alembic.config import Config

    config = Config(str(alembic_ini))
    config.set_main_option("sqlalchemy.url", database_url)
    command.upgrade(config, "head")


@asynccontextmanager
async def api_client(app: FastAPI) -> AsyncIterator[httpx.AsyncClient]:
    transport = httpx.ASGITransport(app=app, raise_app_exceptions=False)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

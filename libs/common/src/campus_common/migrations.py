"""Alembic 环境的公共实现。各服务的 migrations/env.py 只需一行：

    run_migrations([Base.metadata], schemas=["m1"])

数据库地址取 alembic 配置中的 sqlalchemy.url，未设置时取环境变量 DATABASE_URL。
迁移不创建 schema（schema 与账号由 deploy/postgres/init 创建），版本表放在第一个 schema 中。
"""

import asyncio
import os
from typing import Any

from sqlalchemy import MetaData, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine


def run_migrations(metadatas: list[MetaData], *, schemas: list[str]) -> None:
    from alembic import context

    config = context.config
    url = config.get_main_option("sqlalchemy.url") or os.environ["DATABASE_URL"]
    version_schema = schemas[0]

    def include_name(name: str | None, type_: str, _: Any) -> bool:
        return type_ != "schema" or name in schemas

    options: dict[str, Any] = {
        "target_metadata": metadatas,
        "version_table_schema": version_schema,
        "include_schemas": True,
        "include_name": include_name,
        "compare_type": True,
    }

    if context.is_offline_mode():
        context.configure(url=url, literal_binds=True, **options)
        with context.begin_transaction():
            context.run_migrations()
        return

    def do_run(connection: Connection) -> None:
        context.configure(connection=connection, **options)
        with context.begin_transaction():
            context.run_migrations()

    async def run_async() -> None:
        engine = create_async_engine(url, poolclass=pool.NullPool)
        async with engine.connect() as connection:
            await connection.run_sync(do_run)
        await engine.dispose()

    asyncio.run(run_async())

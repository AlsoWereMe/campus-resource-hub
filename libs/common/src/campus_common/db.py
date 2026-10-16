"""数据库：异步引擎、每请求一个事务、按 schema 隔离的 ORM 基类。

用法：
    class Base(DeclarativeBase):              # 本服务 schema 中的所有表都继承它
        metadata = schema_metadata("m1")
    async def handler(session: SessionDep):  # 请求结束时自动提交，抛异常时回滚
"""

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


def schema_metadata(schema: str) -> MetaData:
    """返回绑定到指定 schema 的 MetaData。每个 schema 一个，不得跨 schema 建外键。"""
    return MetaData(schema=schema, naming_convention=NAMING_CONVENTION)


class Database:
    def __init__(self, url: str) -> None:
        self.engine: AsyncEngine = create_async_engine(url, pool_pre_ping=True)
        self.sessionmaker = async_sessionmaker(self.engine, expire_on_commit=False)

    async def dispose(self) -> None:
        await self.engine.dispose()


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    db: Database = request.app.state.db
    async with db.sessionmaker() as session, session.begin():
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]

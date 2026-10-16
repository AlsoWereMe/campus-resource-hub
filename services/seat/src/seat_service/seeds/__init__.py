"""种子数据（NFR-07）：脚本化、幂等、与迁移分离。base 用于所有环境，demo 只用于 dev / test。

运行：python -m seat_service.seeds base|demo（容器启动时自动执行）
"""

from sqlalchemy.ext.asyncio import AsyncSession

from seat_service.config import Settings


async def seed_base(session: AsyncSession, settings: Settings) -> None:
    """所有环境都需要的基础数据。"""


async def seed_demo(session: AsyncSession, settings: Settings) -> None:
    """只用于 dev / test 的演示数据。"""

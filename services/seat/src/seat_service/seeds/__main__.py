import asyncio
import sys

from campus_common.db import Database
from seat_service.config import Settings
from seat_service.seeds import seed_base, seed_demo


async def main(kind: str) -> None:
    settings = Settings()
    db = Database(settings.database_url)
    try:
        async with db.sessionmaker() as session, session.begin():
            if kind == "base":
                await seed_base(session, settings)
            elif kind == "demo":
                await seed_demo(session, settings)
            else:
                raise SystemExit("用法：python -m seat_service.seeds base|demo")
    finally:
        await db.dispose()
    print(f"seat 种子数据（{kind}）已就绪")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else ""))

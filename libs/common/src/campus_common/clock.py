"""可注入的时钟（AGENTS.md：时间相关逻辑使用可注入的时钟）。

- 业务代码只通过 Clock.now() 取当前时间，永远是带时区的 UTC 时间；
- 按业务时区（Asia/Shanghai）解释日期与整点时，用 to_business()；
- 非生产环境使用 AdjustableClock，可通过测试端点推进时间，用于演示提醒、超时等。
"""

from datetime import UTC, date, datetime, time, timedelta
from typing import Protocol
from zoneinfo import ZoneInfo

from fastapi import Request

BUSINESS_TZ = ZoneInfo("Asia/Shanghai")


class Clock(Protocol):
    def now(self) -> datetime: ...


class SystemClock:
    def now(self) -> datetime:
        return datetime.now(UTC)


class AdjustableClock:
    """系统时间加偏移量。只在非生产环境使用。"""

    def __init__(self) -> None:
        self.offset = timedelta()

    def now(self) -> datetime:
        return datetime.now(UTC) + self.offset

    def advance(self, delta: timedelta) -> None:
        self.offset += delta

    def set(self, moment: datetime) -> None:
        self.offset = moment - datetime.now(UTC)

    def reset(self) -> None:
        self.offset = timedelta()


class FixedClock:
    """单元测试用：时间固定，可手动推进。"""

    def __init__(self, moment: datetime) -> None:
        if moment.tzinfo is None:
            raise ValueError("FixedClock 需要带时区的时间")
        self.moment = moment

    def now(self) -> datetime:
        return self.moment

    def advance(self, delta: timedelta) -> None:
        self.moment += delta


def to_business(moment: datetime) -> datetime:
    """转换为业务时区（Asia/Shanghai）时间。"""
    return moment.astimezone(BUSINESS_TZ)


def business_datetime(day: date, hour: int, minute: int = 0) -> datetime:
    """业务时区中某天某时刻，返回带时区的时间。"""
    return datetime.combine(day, time(hour, minute), tzinfo=BUSINESS_TZ)


def get_clock(request: Request) -> Clock:
    clock: Clock = request.app.state.clock
    return clock

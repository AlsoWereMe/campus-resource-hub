from datetime import UTC, date, datetime, timedelta

import pytest

from campus_common.clock import AdjustableClock, FixedClock, business_datetime, to_business


def test_adjustable_clock_moves_forward_and_resets() -> None:
    clock = AdjustableClock()
    before = clock.now()
    clock.advance(timedelta(hours=2))
    assert clock.now() - before >= timedelta(hours=2)
    clock.reset()
    assert clock.now() - before < timedelta(minutes=1)


def test_fixed_clock_requires_timezone() -> None:
    with pytest.raises(ValueError, match="时区"):
        FixedClock(datetime(2026, 10, 20, 14, 0))  # noqa: DTZ001


def test_business_time_is_shanghai() -> None:
    moment = business_datetime(date(2026, 10, 20), 14)
    assert moment.astimezone(UTC) == datetime(2026, 10, 20, 6, 0, tzinfo=UTC)
    assert to_business(datetime(2026, 10, 20, 6, 0, tzinfo=UTC)).hour == 14

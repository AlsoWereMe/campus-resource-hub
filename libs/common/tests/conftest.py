from collections.abc import Iterator

import pytest

from campus_common.testing import postgres_container


@pytest.fixture(scope="session")
def pg_url() -> Iterator[str]:
    """整个测试会话共用一个临时 PostgreSQL（需要 Docker）。"""
    with postgres_container() as url:
        yield url

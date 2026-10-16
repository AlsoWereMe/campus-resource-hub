"""结构化 JSON 日志，自动带上服务名与 traceId（NFR-13）。不得记录密码、令牌与完整个人信息。"""

import logging
import sys
from collections.abc import MutableMapping
from typing import Any

import structlog


def configure_logging(service: str, *, json: bool = True, level: str = "INFO") -> None:
    def add_service(_: Any, __: str, event: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
        event.setdefault("service", service)
        return event

    renderer: Any = structlog.processors.JSONRenderer() if json else structlog.dev.ConsoleRenderer()
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            add_service,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.dict_tracebacks,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelNamesMapping()[level]),
        logger_factory=structlog.PrintLoggerFactory(sys.stdout),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> Any:
    return structlog.get_logger(name)

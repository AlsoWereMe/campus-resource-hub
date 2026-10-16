"""traceId 贯穿网关 → 服务 → 被调服务 → 消息（NFR-13）。使用 W3C traceparent 头。"""

import json
import re
import secrets
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar

import structlog
from starlette.types import ASGIApp, Message, Receive, Scope, Send

TRACEPARENT = "traceparent"
TRACE_ID_HEADER = "x-trace-id"

_TRACEPARENT_RE = re.compile(r"^00-([0-9a-f]{32})-[0-9a-f]{16}-[0-9a-f]{2}$")
_trace_id: ContextVar[str | None] = ContextVar("trace_id", default=None)


def new_trace_id() -> str:
    return secrets.token_hex(16)


def current_trace_id() -> str:
    """当前上下文的 traceId；不在任何请求或消息上下文中时生成一个新的。"""
    value = _trace_id.get()
    return value if value is not None else new_trace_id()


def parse_traceparent(value: str | None) -> str | None:
    if not value:
        return None
    match = _TRACEPARENT_RE.match(value.strip().lower())
    return match.group(1) if match else None


def outgoing_headers() -> dict[str, str]:
    """调用其他服务或发布消息时附带的追踪头。"""
    return {TRACEPARENT: f"00-{current_trace_id()}-{secrets.token_hex(8)}-01"}


@contextmanager
def trace_context(trace_id: str | None = None) -> Iterator[str]:
    """在消息消费、定时任务中建立追踪上下文。"""
    value = trace_id or new_trace_id()
    token = _trace_id.set(value)
    structlog.contextvars.bind_contextvars(trace_id=value)
    try:
        yield value
    finally:
        structlog.contextvars.unbind_contextvars("trace_id")
        _trace_id.reset(token)


class TraceMiddleware:
    """从 traceparent 读取或生成 traceId，并在响应头 X-Trace-Id 中返回。

    未捕获的异常也在这里转成 500 响应，保证响应体中的 traceId 与日志一致。
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        headers = {k.decode().lower(): v.decode() for k, v in scope.get("headers", [])}
        trace_id = parse_traceparent(headers.get(TRACEPARENT)) or new_trace_id()
        started = False

        async def send_with_trace(message: Message) -> None:
            nonlocal started
            if message["type"] == "http.response.start":
                started = True
                message.setdefault("headers", [])
                message["headers"].append((TRACE_ID_HEADER.encode(), trace_id.encode()))
            await send(message)

        with trace_context(trace_id):
            try:
                await self.app(scope, receive, send_with_trace)
            except Exception:
                structlog.get_logger(__name__).exception("unhandled_error")
                if started:
                    raise
                body = json.dumps(
                    {
                        "code": "INTERNAL_ERROR",
                        "message": "服务器内部错误，请凭 traceId 联系维护人员",
                        "details": {},
                        "traceId": trace_id,
                    },
                    ensure_ascii=False,
                ).encode()
                await send_with_trace(
                    {
                        "type": "http.response.start",
                        "status": 500,
                        "headers": [(b"content-type", b"application/json")],
                    }
                )
                await send({"type": "http.response.body", "body": body})

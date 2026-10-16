"""消息总线：RabbitMQ topic 交换机 domain.events（架构 §4.5）。

- 发布：一律经 Outbox（outbox.py），不要在业务代码中直接 publish，否则事务回滚后消息仍会发出；
- 消费：bus.subscribe("seat.space-events", ["space.#"], handler)；处理失败的消息进入死信队列；
- 处理函数必须幂等：同一消息可能被投递多次，用 envelope.message_id 去重。
"""

import json
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

import aio_pika
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustConnection

from campus_common.logging import get_logger
from campus_common.tracing import outgoing_headers, parse_traceparent, trace_context

EXCHANGE = "domain.events"
DEAD_LETTER_EXCHANGE = "domain.events.dlx"

log = get_logger(__name__)


@dataclass
class Envelope:
    message_id: str
    routing_key: str
    trace_id: str | None
    headers: dict[str, Any] = field(default_factory=dict)


Handler = Callable[[dict[str, Any], Envelope], Awaitable[None]]


class MessageBus:
    def __init__(self, url: str, service_name: str) -> None:
        self._url = url
        self._service = service_name
        self._connection: AbstractRobustConnection | None = None
        self._channel: aio_pika.abc.AbstractRobustChannel | None = None
        self._exchange: aio_pika.abc.AbstractExchange | None = None

    async def connect(self) -> None:
        self._connection = await aio_pika.connect_robust(self._url)
        self._channel = await self._connection.channel()
        await self._channel.set_qos(prefetch_count=20)
        self._exchange = await self._channel.declare_exchange(
            EXCHANGE, aio_pika.ExchangeType.TOPIC, durable=True
        )
        await self._channel.declare_exchange(
            DEAD_LETTER_EXCHANGE, aio_pika.ExchangeType.TOPIC, durable=True
        )

    async def publish(self, routing_key: str, payload: dict[str, Any], *, message_id: str) -> None:
        if self._exchange is None:
            raise RuntimeError("MessageBus 尚未连接")
        message = aio_pika.Message(
            body=json.dumps(payload, ensure_ascii=False, default=str).encode(),
            content_type="application/json",
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            message_id=message_id,
            app_id=self._service,
            headers=dict(outgoing_headers()),
        )
        await self._exchange.publish(message, routing_key=routing_key)

    async def subscribe(self, queue_name: str, binding_keys: list[str], handler: Handler) -> None:
        if self._channel is None or self._exchange is None:
            raise RuntimeError("MessageBus 尚未连接")
        dlq = await self._channel.declare_queue(f"{queue_name}.dlq", durable=True)
        await dlq.bind(DEAD_LETTER_EXCHANGE, routing_key=queue_name)
        queue = await self._channel.declare_queue(
            queue_name,
            durable=True,
            arguments={
                "x-dead-letter-exchange": DEAD_LETTER_EXCHANGE,
                "x-dead-letter-routing-key": queue_name,
            },
        )
        for key in binding_keys:
            await queue.bind(self._exchange, routing_key=key)

        async def on_message(message: AbstractIncomingMessage) -> None:
            headers = dict(message.headers or {})
            trace_id = parse_traceparent(str(headers.get("traceparent", "")))
            envelope = Envelope(
                message_id=message.message_id or "",
                routing_key=message.routing_key or "",
                trace_id=trace_id,
                headers=headers,
            )
            with trace_context(trace_id):
                try:
                    await handler(json.loads(message.body), envelope)
                except Exception:
                    log.exception("message_failed", queue=queue_name, key=envelope.routing_key)
                    await message.reject(requeue=False)
                else:
                    await message.ack()

        await queue.consume(on_message)

    async def close(self) -> None:
        if self._connection is not None:
            await self._connection.close()

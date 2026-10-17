"""platform 订阅的消息。在 setup 中调用 bus.subscribe(队列名, [路由键], 处理函数)。

待实现：
- 任务 D-T05（NTF-01）：订阅 notify.send，按幂等键只投递一次，发邮件并写站内信；
- 任务 D-T04（AUD-01）：订阅 audit.record，只增不改地存储。
    await bus.subscribe("platform.notify", ["notify.send"], handle_notify)
    await bus.subscribe("platform.audit", ["audit.record"], handle_audit)
"""

from fastapi import FastAPI

from campus_common.mq import MessageBus


async def setup(bus: MessageBus, app: FastAPI) -> None:
    return None

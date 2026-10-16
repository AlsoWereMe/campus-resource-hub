"""本服务订阅的消息。在 setup 中调用 bus.subscribe(队列名, [路由键], 处理函数)。"""

from fastapi import FastAPI

from campus_common.mq import MessageBus


async def setup(bus: MessageBus, app: FastAPI) -> None:
    return None

"""本服务订阅的消息。在 setup 中调用 bus.subscribe(队列名, [路由键], 处理函数)。

待实现（任务 M3-T06，P2）：订阅 space.room.updated，房间注销时标记该房间未关闭的工单并通知调度员（M3-INT-06）。
"""

from fastapi import FastAPI

from campus_common.mq import MessageBus


async def setup(bus: MessageBus, app: FastAPI) -> None:
    return None

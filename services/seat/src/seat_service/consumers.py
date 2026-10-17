"""本服务订阅的消息。在 setup 中调用 bus.subscribe(队列名, [路由键], 处理函数)。

待实现（任务 M1-T06，M1-INT-05）：订阅 space.room.updated、space.seats.updated，
房间关闭或停用、座位停用或注销、开放时间缩短时，按 BR-19 处理受影响预约。
    await bus.subscribe("seat.space-events", ["space.#"], handle_space_event)
"""

from fastapi import FastAPI

from campus_common.mq import MessageBus


async def setup(bus: MessageBus, app: FastAPI) -> None:
    return None

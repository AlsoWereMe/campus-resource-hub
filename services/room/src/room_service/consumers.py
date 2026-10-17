"""本服务订阅的消息。在 setup 中调用 bus.subscribe(队列名, [路由键], 处理函数)。

待实现（任务 M2-T07）：
- m3.workorder.repairing：房间进入维修时，通知受影响申请的申请人与资源管理员（M2-INT-04）；
- space.room.updated：房间停用、注销或取消整间预约时处理在途申请（M2-INT-06）。
"""

from fastapi import FastAPI

from campus_common.mq import MessageBus


async def setup(bus: MessageBus, app: FastAPI) -> None:
    return None

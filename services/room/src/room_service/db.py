"""本服务的 ORM 基类：所有表都在 schema m2 中，模型写在各子包的 models.py。"""

from sqlalchemy.orm import DeclarativeBase

from campus_common.db import schema_metadata
from campus_common.outbox import outbox_table


class Base(DeclarativeBase):
    metadata = schema_metadata("m2")


# 跨服务调用与消息一律经 outbox 发送（campus_common/outbox.py）
OUTBOX = outbox_table(Base.metadata)

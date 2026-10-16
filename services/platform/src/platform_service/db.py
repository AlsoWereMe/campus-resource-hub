"""platform 的四个 schema 各有一个 ORM 基类；不得跨 schema 建外键（院系 ID 等只存数值）。"""

from sqlalchemy.orm import DeclarativeBase

from campus_common.db import schema_metadata
from campus_common.outbox import outbox_table


class IamBase(DeclarativeBase):
    metadata = schema_metadata("iam")


class SpaceBase(DeclarativeBase):
    metadata = schema_metadata("space")


class NotifyBase(DeclarativeBase):
    metadata = schema_metadata("notify")


class AuditBase(DeclarativeBase):
    metadata = schema_metadata("audit")


# platform 发出的事件（space.*）与审计、通知统一经此 outbox 发送
OUTBOX = outbox_table(IamBase.metadata)

SCHEMAS = ["iam", "space", "notify", "audit"]
METADATAS = [IamBase.metadata, SpaceBase.metadata, NotifyBase.metadata, AuditBase.metadata]

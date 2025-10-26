__all__ = (
    "NotificationCreate",
    "NotificationRead",
)

from datetime import (
    datetime,
)
from typing import Annotated

from annotated_types import (
    Gt,
    MaxLen,
)
from pydantic import BaseModel, ConfigDict

from bot.enums import NotificationTypeEnum


class NotificationBase(BaseModel):
    telegram_id: Annotated[int, Gt(0)]
    message: Annotated[str, MaxLen(1000)]
    notif_time: datetime
    is_active: bool = True
    notification_type: NotificationTypeEnum = NotificationTypeEnum.DAILY


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdatePartial(BaseModel):
    telegram_id: Annotated[int, Gt(0)] | None = None
    message: Annotated[str, MaxLen(1000)] | None = None
    notif_time: datetime | None = None
    is_active: bool | None = None
    notification_type: NotificationTypeEnum | None = None


class NotificationRead(NotificationBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    created_at: datetime

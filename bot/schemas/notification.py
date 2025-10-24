__all__ = (
    "NotificationCreate",
    "NotificationRead",
)

from datetime import (
    datetime,
    time,
)
from typing import Annotated

from annotated_types import (
    Gt,
    MaxLen,
)
from pydantic import BaseModel, ConfigDict


class NotificationBase(BaseModel):
    message: Annotated[str, MaxLen(1000)]
    notification_time: time
    user_id: Annotated[int, Gt(0)]
    is_active: bool | None = True
    job_id: int | None = None


class NotificationCreate(NotificationBase):
    pass


class NotificationRead(NotificationBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    created_at: datetime

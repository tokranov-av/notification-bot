__all__ = (
    "UserCreate",
    "UserRead",
)

from datetime import datetime
from typing import Annotated

from annotated_types import (
    MaxLen,
    MinLen,
)
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    telegram_id: int
    first_name: Annotated[str, MinLen(3), MaxLen(255)] | None
    last_name: Annotated[str, MinLen(3), MaxLen(255)] | None


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    created_at: datetime

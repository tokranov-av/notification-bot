from datetime import time
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    Time,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Notification(Base):
    """Модель уведомлений."""

    message: Mapped[str] = mapped_column(String(1000))
    notification_time: Mapped[time] = mapped_column(Time)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    job_id: Mapped[str | None] = mapped_column(String(255), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(
        "User",
        back_populates="notifications",
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(id={self.user_id}, username={self.notification_time!r})"

    def __repr__(self) -> str:
        return str(self)

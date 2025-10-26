from datetime import (
    datetime,
    time,
)

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Enum,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from bot.enums import NotificationTypeEnum

from .base import Base


class Notification(Base):
    """Модель уведомлений."""

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    message: Mapped[str] = mapped_column(String(1000))
    notif_time: Mapped[datetime] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    notification_type: Mapped[NotificationTypeEnum] = mapped_column(
        Enum(NotificationTypeEnum),
        default=NotificationTypeEnum.DAILY,
    )

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(telegram_id={self.telegram_id}, time={self.notification_time!r})"

    def __repr__(self) -> str:
        return str(self)

    @property
    def notification_time(self) -> time | datetime:
        if self.notification_type == NotificationTypeEnum.DAILY:
            return self.notif_time.time()

        return self.notif_time

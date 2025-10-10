from datetime import time

from sqlalchemy import (
    BigInteger,
    Boolean,
    String,
    Time,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import Base


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    message: Mapped[str] = mapped_column(String(1000))
    notification_time: Mapped[time] = mapped_column(Time)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    job_id: Mapped[str | None] = mapped_column(String(255), unique=True)

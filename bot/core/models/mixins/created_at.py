from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from bot.core.config import TIME_ZONE


def get_current_dt() -> datetime:
    dt = datetime.now(tz=TIME_ZONE)
    return dt.replace(microsecond=0, tzinfo=None)


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        default=get_current_dt,
        server_default=func.now(),
    )

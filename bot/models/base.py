from datetime import datetime

from sqlalchemy import MetaData, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

from bot.config import (
    TIME_ZONE,
    settings,
)


def get_current_dt() -> datetime:
    dt = datetime.now(tz=TIME_ZONE)
    return dt.replace(microsecond=0, tzinfo=None)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.postgres.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: N805
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        default=get_current_dt,
        server_default=func.now(),
    )

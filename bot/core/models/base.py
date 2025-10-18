from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
)

from bot.core import settings


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.postgres.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: N805
        return f"{cls.__name__.lower()}s"

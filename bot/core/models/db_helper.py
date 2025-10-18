import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from bot.core.config import settings

log = logging.getLogger(__name__)


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,  # noqa: FBT001, FBT002
        echo_pool: bool = False,  # noqa: FBT001, FBT002
        pool_size: int = 5,
        max_overflow: int = 10,
    ) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()
        log.info("Database engine disposed")

    async def session_getter(self) -> AsyncGenerator[AsyncSession]:
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    url=str(settings.postgres.url),
    echo=settings.postgres.echo,
    echo_pool=settings.postgres.echo_pool,
    pool_size=settings.postgres.pool_size,
    max_overflow=settings.postgres.max_overflow,
)

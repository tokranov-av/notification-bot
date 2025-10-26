import asyncio
import logging

from aiogram import (
    Dispatcher,
)

from bot.config import settings
from bot.core import bot
from bot.handlers import router
from bot.scheduler import scheduler_loop

logging.basicConfig(
    level=settings.logging.log_level,
    format=settings.logging.log_format,
    datefmt=settings.logging.date_format,
)

dp = Dispatcher()
dp.include_router(router)


async def main() -> None:
    asyncio.create_task(scheduler_loop())  # noqa: RUF006
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

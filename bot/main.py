import asyncio
import logging

from aiogram import (
    Bot,
    Dispatcher,
)

from bot.config import settings
from bot.handlers import router

logging.basicConfig(
    level=settings.logging.log_level,
    format=settings.logging.log_format,
    datefmt=settings.logging.date_format,
)


bot = Bot(token=settings.bot.token)
dp = Dispatcher()
dp.include_router(router)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import logging

from aiogram import (
    Bot,
    Dispatcher,
    types,
)
from aiogram.filters import Command

from bot.core import settings

logging.basicConfig(
    level=settings.logging.log_level,
    format=settings.logging.log_format,
    datefmt=settings.logging.date_format,
)


bot = Bot(token=settings.bot.token)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    await message.answer("Hello!")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

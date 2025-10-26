__all__ = ("bot",)

from aiogram import Bot

from bot.config import settings

bot = Bot(token=settings.bot.token)

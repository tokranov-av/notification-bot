__all__ = ("send_message",)

import logging

from bot.core import bot

logger = logging.getLogger(__name__)


async def send_message(user_id: int, message: str) -> None:
    try:
        await bot.send_message(chat_id=user_id, text=message)
    except Exception:
        logger.exception("Ошибка при отправке уведомления: %s", user_id)

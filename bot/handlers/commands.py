__all__ = ("router",)

import logging
from datetime import datetime

from aiogram import Router, types
from aiogram.filters import Command, CommandStart

from bot.core.models import db_helper
from bot.core.schemas import NotificationCreate
from bot.crud import (
    create_notification,
    get_notification,
)
from bot.enums import NotificationTypeEnum

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    await message.answer(
        "👋 Привет! Используйте команду /time чтобы задать время ежедневного напоминая.",
    )


@router.message(Command("time"))
async def cmd_time(message: types.Message) -> None:
    await message.answer(
        "🕓 Введите время для уведомления в формате `ЧЧ:ММ` (например: `09:30`)",
        parse_mode="Markdown",
    )


@router.message(lambda message: not message.text.startswith("/"))
async def handle_text(message: types.Message) -> None:
    if message.text is None:
        await message.answer(
            "Пожалуйста, введите время для уведомления в формате `ЧЧ:ММ` (например: `09:30`)",
        )
    else:
        try:
            hours, minutes = map(int, message.text.split(":"))
            now = datetime.now()
            notification_time = datetime(
                now.year,
                now.month,
                now.day,
                hours,
                minutes,
            )
        except ValueError:
            await message.answer("Неверный формат времени")
        else:
            async with db_helper.session_factory() as session:
                if message.from_user is not None:
                    notification = await get_notification(
                        session=session,
                        telegram_id=message.from_user.id,
                        notification_time=notification_time,
                    )
                    if not notification:
                        new_notification = NotificationCreate(
                            telegram_id=message.from_user.id,
                            message="Привет",
                            notif_time=notification_time,
                            notification_type=NotificationTypeEnum.DAILY,
                        )
                        await create_notification(
                            session=session,
                            notification_create=new_notification,
                        )

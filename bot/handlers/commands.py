__all__ = ("router",)

import logging
from datetime import time

from aiogram import Router, types
from aiogram.filters import Command, CommandStart

from bot.crud import (
    create_notification,
    create_user,
    get_notification,
    get_user,
)
from bot.database.db_helper import db_helper
from bot.schemas import NotificationCreate, UserCreate

logger = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    await message.answer(
        "👋 Привет! Используйте команду /time чтобы задать время напоминая.",
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
            notification_time = time(hours, minutes)
        except ValueError:
            await message.answer("Неверный формат времени")
        else:
            async with db_helper.session_factory() as session:
                if message.from_user is not None:
                    user = await get_user(
                        session=session,
                        telegram_id=message.from_user.id,
                    )
                    if not user:
                        user_create = UserCreate(
                            username=message.from_user.username,
                            telegram_id=message.from_user.id,
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                        )
                        user = await create_user(
                            session=session,
                            user_create=user_create,
                        )
                    notification = await get_notification(
                        session=session,
                        user_id=user.id,
                        notification_time=notification_time,
                    )
                    if not notification:
                        new_notification = NotificationCreate(
                            message="Привет",
                            notification_time=notification_time,
                            user_id=user.id,
                        )
                        await create_notification(
                            session=session,
                            notification_create=new_notification,
                        )

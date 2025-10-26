import asyncio
from datetime import datetime

from bot.core.models.db_helper import db_helper
from bot.crud import get_active_notifications
from bot.enums import DaysOfTheWeek
from bot.utils.send_message import send_message


async def scheduler_loop() -> None:
    while True:
        now = datetime.now()
        if now.weekday() > DaysOfTheWeek.SATURDAY.value:
            async with db_helper.session_factory() as session:
                notifications = await get_active_notifications(session)
                for notif in notifications:
                    if (
                        notif.notif_time.hour == now.hour
                        and notif.notif_time.minute == now.minute
                    ):
                        await send_message(notif.telegram_id, notif.message)

        await asyncio.sleep(60)

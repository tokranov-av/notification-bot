from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.core.models import Notification
from bot.core.schemas import NotificationCreate, NotificationUpdatePartial


async def get_notification(
    session: AsyncSession,
    telegram_id: int,
    notification_time: datetime,
) -> Notification | None:
    stmt = (
        select(Notification)
        .where(Notification.telegram_id == telegram_id)
        .where(Notification.notif_time == notification_time)
        .order_by(Notification.id)
    )
    result = await session.scalars(stmt)

    return result.one_or_none()


async def create_notification(
    session: AsyncSession,
    notification_create: NotificationCreate,
) -> Notification:
    notification = Notification(**notification_create.model_dump())
    session.add(notification)
    await session.commit()
    # await session.refresh(user)
    return notification


async def update_notification_partial(
    session: AsyncSession,
    notification: Notification,
    notification_update: NotificationUpdatePartial,
) -> Notification | None:
    for field_name, value in notification_update.model_dump(exclude_unset=True).items():
        setattr(notification, field_name, value)
    await session.commit()

    return notification


async def get_active_notifications(
    session: AsyncSession,
) -> Sequence[Notification]:
    result = await session.execute(
        select(Notification).where(Notification.is_active),
    )

    return result.scalars().all()

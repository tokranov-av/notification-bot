from datetime import time

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import Notification
from bot.schemas import NotificationCreate


async def get_notification(
    session: AsyncSession,
    user_id: int,
    notification_time: time,
) -> Notification | None:
    stmt = (
        select(Notification)
        .where(Notification.user_id == user_id)
        .where(Notification.notification_time == notification_time)
        .where(Notification.is_active)
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


async def update_job_id(
    session: AsyncSession,
    notification_id: int,
    job_id: str,
) -> Notification:
    """Обновление job_id уведомления"""
    stmt = (
        update(Notification)
        .where(Notification.id == notification_id)
        .values(job_id=job_id)
        .returning(Notification)
    )
    result = await session.execute(stmt)
    await session.commit()

    return result.scalar_one()

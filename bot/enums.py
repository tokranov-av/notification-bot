__all__ = (
    "DaysOfTheWeek",
    "NotificationTypeEnum",
)

import enum


class NotificationTypeEnum(enum.Enum):
    """Тип уведомления."""

    ONE_TIME = "Один раз"
    DAILY = "Ежедневно"


class DaysOfTheWeek(enum.Enum):
    """Дни недели."""

    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

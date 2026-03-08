from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from ..db.declarative_base import Base
from .enums import TaskStatus


class TaskBaseModel(Base):
    """
    Базовая модель Celery задач.
    """
    __abstract__ = True

    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        default=TaskStatus.PENDING,
        nullable=False
    )

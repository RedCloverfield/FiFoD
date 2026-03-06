from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ...db.declarative_base import Base
from ..enums import TaskStatus


class AttachmentCreationTask(Base):
    attachment_id: Mapped[int] = mapped_column(
        ForeignKey('attachment.id', ondelete='CASCADE')
    )
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        default=TaskStatus.PENDING,
        nullable=False
    )

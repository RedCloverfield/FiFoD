from sqlalchemy import String, Text, Index, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from ..db.declarative_base import Base
from ..celery_tasks.enums import TaskStatus


class Attachment(Base):
    deviceId: Mapped[str] = mapped_column(String, nullable=False)
    fileNames: Mapped[list[str]] = mapped_column(
        ARRAY(String), default=list, nullable=False
    )
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    tags: Mapped[list[str]] = mapped_column(
        ARRAY(String), default=list, nullable=True
    )

    __table_args__ = (
        Index(
            'idx_attachments_tags',
            tags,
            postgresql_using='gin'
        ),
        UniqueConstraint(
            deviceId,
            fileNames,
            name='unique_attachment_constraint'
        )
    )

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..models import TaskBaseModel


class AttachmentCreationTask(TaskBaseModel):
    '''
    Модель Celery задач, запущенных при операциях с привязками.
    '''
    attachment_id: Mapped[int] = mapped_column(
        ForeignKey('attachment.id', ondelete='CASCADE')
    )

'''Импорты класса Base и всех моделей проекта для Alembic.'''
from .declarative_base import Base  # noqa
from ..users.models import User  # noqa
from ..attachments.models import Attachment  # noqa
from ..celery_tasks.attachments.models import AttachmentCreationTask  # noqa

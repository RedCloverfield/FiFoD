from ..dependencies import get_celery_tasks_service
from .models import AttachmentCreationTask
from ..repository import CeleryTasksRepository


def get_celery_tasks_repository() -> CeleryTasksRepository:
    return CeleryTasksRepository(model=AttachmentCreationTask)


get_attachments_tasks_service = get_celery_tasks_service(
    repository_construct=get_celery_tasks_repository
)

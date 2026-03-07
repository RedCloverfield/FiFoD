from ..dependencies import get_celery_tasks_service
from .models import AttachmentCreationTask
from ..repository import CeleryTasksRepository


def get_celery_tasks_repository() -> CeleryTasksRepository:
    '''
    Создает экземпляр репозитория `CeleryTasksRepository` для осуществления
    операций с Celery задачами созданными при операциях с привязками.

    Returns:
        CeleryTasksRepository: Экземпляр репозитория `CeleryTasksRepository`
        для работы с моделью `AttachmentCreationTask`.
    '''
    return CeleryTasksRepository(model=AttachmentCreationTask)


get_attachments_tasks_service = get_celery_tasks_service(
    repository_construct=get_celery_tasks_repository
)

import asyncio
from worker.celery_app import celery

from ...db.session import session_factory
from .dependencies import get_celery_tasks_repository
from ..enums import TaskStatus

celery_tasks_repository = get_celery_tasks_repository()


@celery.task(bind=True)
def process_attachment_task(self, task_id: int):
    '''
    Функция-адаптер. Синхронная точка входа для запуска Celery задач.

    Args:
        task_id (int): Идентификатор Celery задачи.
    '''
    asyncio.run(start_attachment_task(task_id=task_id))


async def start_attachment_task(task_id: int):
    '''
    Симуляция задачи, запускаемой при создании привязки файлов к устройству.
    В зависимости от результата выполнения задачи записывает соотвествующий
    статус в базу данных.

    Args:
        task_id (int): Идентификатор задачи.
    '''
    async with session_factory() as session:
        await celery_tasks_repository.update_task_status(
            session=session,
            task_id=task_id,
            new_status=TaskStatus.IN_PROGRESS
        )
        try:
            # Симулируем логику фоновой задачи
            await asyncio.sleep(10)
            await celery_tasks_repository.update_task_status(
                session=session,
                task_id=task_id,
                new_status=TaskStatus.DONE
            )
        # Поскольку логика фоновой задачи не определена четко,
        # перехватываем любое исключение
        except Exception:
            await celery_tasks_repository.update_task_status(
                session=session,
                task_id=task_id,
                new_status=TaskStatus.FAILED
            )

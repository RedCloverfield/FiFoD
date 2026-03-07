from enum import StrEnum


class TaskStatus(StrEnum):
    '''
    Статусы выполнения Celery задачи.
    '''
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    FAILED = 'failed'

from celery import Celery
from api.config import settings

celery = Celery(
    'fifod_worker',
    broker=settings.redis_broker_url,
    backend=settings.redis_result_url
)

celery.autodiscover_tasks(['api.celery_tasks.attachments'])

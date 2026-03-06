from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from ..celery_tasks.attachments.tasks import process_attachment_task
from ..celery_tasks.attachments.models import AttachmentCreationTask
from .models import Attachment
from .repository import AttachmentRepository
from .validation import AttachmentValidator
from .schemas import CreateAttachmentDTO


class AttachmentService:

    def __init__(
        self,
        session_factory: Callable[[], AsyncSession],
        repository: AttachmentRepository
    ):
        self._session_factory = session_factory
        self._repository = repository

    @property
    def attachment_repository(self):
        return self._repository

    @property
    def session_factory(self):
        return self._session_factory

    async def create_attachment(
        self,
        new_attachment: CreateAttachmentDTO
    ) -> Attachment:
        async with self.session_factory() as session:
            validator = AttachmentValidator(
                repository=self.attachment_repository
            )
            await validator.validate_attachment_creation(
                session=session,
                device_id=new_attachment.device_id,
                filenames=new_attachment.filenames
            )
            attachment = Attachment(
                deviceId=new_attachment.device_id,
                fileNames=new_attachment.filenames,
                comment=new_attachment.comment,
                tags=new_attachment.tags
            )
            await self.attachment_repository.create(
                session=session,
                obj=attachment
            )
            task = AttachmentCreationTask(  # Celery
                attachment_id=attachment.id
            )
            await self.attachment_repository.create(  # Celery
                session=session,
                obj=task
            )
            await session.commit()
            process_attachment_task.delay(task.id)  # Celery
            return attachment

    async def get_attachments(
        self, filter_by
    ) -> list[Attachment]:
        async with self.session_factory() as session:
            attachments = await self.attachment_repository.get_attachments(
                session=session,
                filter_by=filter_by
            )
        return attachments

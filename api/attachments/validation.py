from sqlalchemy.ext.asyncio import AsyncSession

from ..core.constants import FILES_STORAGE_PATH
from ..core.exceptions import ObjectNotFound, ObjectAlreadyExists
from ..infrastructure.external_api_client import ExternalAPIClient
from ..files.utils import scan_directory
from .repository import AttachmentRepository


class AttachmentValidator:

    def __init__(self, repository: AttachmentRepository):
        self._repository = repository

    @property
    def repository(self):
        return self._repository

    async def _ensure_device_exists(self, device_id: str):
        client = ExternalAPIClient()
        devices = await client.get_devices()
        if device_id not in [device.serial for device in devices]:
            raise ObjectNotFound(
                f'Устройство с серийным номером {device_id} не найдено'
            )

    async def _ensure_files_exist(self, filenames: list[str]):
        files = await scan_directory(FILES_STORAGE_PATH)
        uncorrect_filenames = set(filenames).difference(
            set(file.name for file in files)
        )
        if uncorrect_filenames:
            raise ObjectNotFound(
                'Невозможно осуществить привязку. '
                f'Отсутствуют файлы с названиями: {', '.join(uncorrect_filenames)}'
            )

    async def _ensure_attachment_not_exists(
        self,
        session: AsyncSession,
        device_id: str,
        filenames: list[str]
    ):
        if await self.repository.get_by(
            session=session,
            deviceId=device_id,
            fileNames=filenames
        ):
            raise ObjectAlreadyExists('Такая привязка уже существует')

    async def validate_attachment_creation(
        self,
        session: AsyncSession,
        device_id: str,
        filenames: list[str]
    ):
        await self._ensure_device_exists(device_id=device_id)
        await self._ensure_files_exist(filenames=filenames)
        await self._ensure_attachment_not_exists(
            session=session,
            device_id=device_id,
            filenames=filenames
        )

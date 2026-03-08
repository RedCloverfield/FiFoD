from datetime import datetime, timezone

import aiofiles
from fastapi import UploadFile

from ..core.constants import APPROPRIATE_FILE_EXT, FILES_STORAGE_PATH
from ..core.schemas import SuccessResponse
from .validation import FileValidator
from .utils import scan_directory, get_file_meta
from .schemas import FileInfoDTO


class FileService:
    '''
    Сервисный слой, для осуществления операций с файлами.
    '''

    async def upload_file(
        self, uploaded_file: UploadFile
    ) -> SuccessResponse:
        """
        Загружает файл на сервер по чанкам. Валидрует существование директории
        для хранения файлов.

        Args:
            uploaded_file (UploadFile): Загружаемый файл.

        Returns:
            SuccessResponse: Сообщение об успешной загрузке файлов.
        """
        validator = FileValidator()
        await validator.validate_directory_existance(
            directory=FILES_STORAGE_PATH
        )
        filename = uploaded_file.filename
        async with aiofiles.open(FILES_STORAGE_PATH / filename, 'wb') as f:
            while chunk := await uploaded_file.read(1024 * 1024):
                await f.write(chunk)
        return SuccessResponse(
            message='Файл успешно загружен'
        )

    async def get_image_files(self) -> list[FileInfoDTO]:
        """
        Возвращает метаданные файлов-изображений.

        Returns:
            list[FileInfoDTO]: Метаданные файлов.
        """
        validator = FileValidator()
        await validator.validate_directory_existance(
            directory=FILES_STORAGE_PATH
        )
        files = await scan_directory(FILES_STORAGE_PATH)
        files_info: list[FileInfoDTO] = []
        for file in files:
            if not file.is_file():
                continue
            metadata = await get_file_meta(file)
            if file.suffix in APPROPRIATE_FILE_EXT:
                files_info.append(
                    FileInfoDTO(
                        name=file.name,
                        size=metadata.st_size,
                        extention=file.suffix,
                        updated_at=datetime.fromtimestamp(
                            metadata.st_mtime,
                            tz=timezone.utc,
                        ),
                    )
                )
        return files_info

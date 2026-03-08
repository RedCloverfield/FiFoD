from pathlib import Path

from ..core.exceptions import FilesDirectoryUnavailable


class FileValidator:
    '''
    Валидатор операций с файлами.
    '''

    async def validate_directory_existance(self, directory: Path) -> None:
        if not directory.exists():
            raise FilesDirectoryUnavailable()

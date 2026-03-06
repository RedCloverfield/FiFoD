from .service import FileService


def get_file_service() -> FileService:
    return FileService()

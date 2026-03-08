from .service import FileService


def get_file_service() -> FileService:
    '''
    Создает экземпляр класса :class:`FileService`.
    '''
    return FileService()

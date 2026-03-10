from fastapi import status

from .schemas import ErrorDetail, ErrorResponse


class BaseAPIException(Exception):
    '''
    Базовая ошибка приложения.
    '''
    status_code: int
    code: str
    message: str
    details: dict | None = None

    def __init__(self, message: str | None = None):
        if message:
            self.message = message

    def to_dict(self) -> dict:
        '''
        Преобразует поля ошибки в Pydantic модель, а затем в словарь.

        Returns:
            dict: Словарь, содержащий данные ошибки.
        '''
        return ErrorResponse(
            error=ErrorDetail(
                message=self.message,
                code=self.code,
                details=self.details
            )
        ).model_dump(exclude_none=True)


class AuthenticationError(BaseAPIException):
    '''
    Ошибка аутентифкации пользователя.
    '''
    status_code = status.HTTP_401_UNAUTHORIZED
    code = 'authentication_error'
    message = 'Ошибка аутентификации'


class AuthorizationError(BaseAPIException):
    '''
    Ошибка авторизации пользователя.
    '''
    status_code = status.HTTP_401_UNAUTHORIZED
    code = 'authorization_error'
    message = 'Ошибка авторизации'


class ObjectAlreadyExists(BaseAPIException):
    '''
    Ошибка, возникающая при попытке создать уже существующую
    сущность в базе данных.
    '''
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    code = 'obj_already_exists'


class ObjectNotFound(BaseAPIException):
    '''
    Ошибка, возникающая при попытке обращения к несуществующей
    сущности в базе данных.
    '''
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    code = 'obj_not_found'


class FilesDirectoryUnavailable(BaseAPIException):
    '''
    Ошибка отсутствия директории для хранения загружаемых файлов на сервере.
    '''
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = 'files_directory_unavailable'
    message = 'Директория для хранения файлов не найдена'

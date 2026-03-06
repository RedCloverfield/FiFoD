from fastapi import status

from .schemas import ErrorDetail, ErrorResponse


class BaseAPIException(Exception):
    status_code: int
    code: str
    message: str
    details: dict | None = None

    def __init__(self, message: str | None = None):
        if message:
            self.message = message

    def to_dict(self):
        return ErrorResponse(
            error=ErrorDetail(
                message=self.message,
                code=self.code,
                details=self.details
            )
        ).model_dump(exclude_none=True)


class AuthenticationError(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = 'auth_error'
    message = 'Ошибка аутентификации'


class ObjectAlreadyExists(BaseAPIException):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    code = 'obj_already_exists'


class ObjectNotFound(BaseAPIException):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    code = 'obj_not_found'


class FilesDirectoryUnavailable(BaseAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = 'files_directory_unavailable'
    message = 'Директория для хранения файлов не найдена'

from datetime import datetime, timedelta, timezone

from jose import jwt

from ..core.config import settings


def create_access_token(data: dict) -> str:
    '''
    Создает и возвращает JWT Access токен с переданными данными.

    Args:
        data (dict): Данные для передачи в токен.

    Returns:
        str: JWT Access токен
    '''
    to_encode = data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({'exp': expire_time})
    return jwt.encode(
        claims=to_encode,
        key=settings.secret_key,
        algorithm=settings.algorithm
    )


def decode_token(token: str) -> dict:
    '''
    Декодирует токен и возвращает его данные.

    Args:
        token (str): Токен.

    Returns:
        dict: Данные токена.
    '''
    return jwt.decode(
        token=token,
        key=settings.secret_key,
        algorithms=[settings.algorithm]
    )

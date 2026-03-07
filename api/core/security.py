from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    '''
    Хеширует переданный пароль и возвращает его.

    Args:
        password (str): Пароль для хеширования.

    Returns:
        str: Хешированный пароль.
    '''
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    '''
    Сравнивает пароль с хэшем пароля.

    Args:
        password (str): Пароль.
        hashed_password (str): Хешированный пароль.

    Returns:
        bool: Результат верификации пароля. `True`, если пароли совпадают,
         иначе `False`.
    '''
    return pwd_context.verify(
        secret=password, hash=hashed_password
    )

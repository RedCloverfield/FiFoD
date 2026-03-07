from enum import StrEnum


class TokenType(StrEnum):
    '''
    Типы JWT токенов.
    '''
    BEARER = 'Bearer'

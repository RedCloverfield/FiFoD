from enum import StrEnum


class TokenType(StrEnum):
    '''
    Типы JWT токенов.
    '''
    ACCESS_TOKEN = 'access_token'
    REFRESH_TOKEN = 'refresh_token'

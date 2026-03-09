from pydantic import BaseModel


class AccessTokenDTO(BaseModel):
    '''
    Модель ответа, содержащего JWT Access токен.
    '''
    access_token: str


class TokensDTO(BaseModel):
    '''
    Модель, содержащая JWT Access и Refresh токены.
    '''
    access_token: str
    refresh_token: str

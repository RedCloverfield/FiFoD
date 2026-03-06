from pydantic import BaseModel, ConfigDict, SecretStr


class UserCreateDTO(BaseModel):
    username: str
    password: SecretStr


class UserDTO(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)

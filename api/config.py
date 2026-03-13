from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int
    api_url: str = 'http://localhost:8000'
    project_title: str = 'FiFoD'
    postgres_hostname: str = 'localhost'
    postgres_port: int = 5432
    postgres_db: str
    postgres_user: str
    postgres_password: str
    superuser_name: str
    superuser_password: str
    redis_db_broker: int = 0
    redis_db_result: int = 1
    redis_port: int = 6379
    redis_hostname: str = 'localhost'
    redis_user: str
    redis_password: str
    external_api_url: str
    external_api_token: str
    files_storage_dir: str

    @property
    def postgres_url(self) -> str:
        return (
            f'postgresql+asyncpg://{self.postgres_user}:'
            f'{self.postgres_password}@{self.postgres_hostname}:'
            f'{self.postgres_port}/{self.postgres_db}'
        )

    @property
    def redis_broker_url(self) -> str:
        return (
            f'redis://:{self.redis_password}@{self.redis_hostname}:'
            f'{self.redis_port}/{self.redis_db_broker}'
        )

    @property
    def redis_result_url(self) -> str:
        return (
            f'redis://:{self.redis_password}@{self.redis_hostname}:'
            f'{self.redis_port}/{self.redis_db_result}'
        )

    class Config:
        env_file = '../.env'


settings = Settings()

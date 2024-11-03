from pathlib import Path

from fastapi.templating import Jinja2Templates
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_title: str = 'Chat'
    description: str = 'Chat'
    postgres_user: str = 'chatuser'
    postgres_password: str = 'chat_pass'
    postgres_host: str = 'localhost'
    postgres_port: int = 5432
    postgres_db: str = 'chatdb'
    # database_url: str = (
    #     f'postgresql+asyncpg://{postgres_user}:{postgres_password}@'
    #     f'{postgres_host}:{postgres_port}/{postgres_db}'
    # )
    secret: str = 'SECRET'
    algorithm: str = ''

    min_password_length: int = 3
    max_length_string: int = 100
    min_length_string: int = 1
    base_dir: Path = Path(__file__).parent.parent.parent

    host: str = 'localhost'
    port: int = 8000
    celery_port: int = 6379
    model_config = SettingsConfigDict(env_file='infra/.env', extra="ignore")


class BotSettings(BaseSettings):
    bot_token: SecretStr
    model_config = SettingsConfigDict(env_file='infra/.env', extra="ignore")


settings = Settings()
bot_settings = BotSettings()


def get_auth_data():
    return {
        'secret_key': settings.secret,
        'algorithm': settings.algorithm
    }


DATABASE_URL = (
        f'postgresql+asyncpg://{settings.postgres_user}:'
        f'{settings.postgres_password}@'
        f'{settings.postgres_host}:{settings.postgres_port}/'
        f'{settings.postgres_db}'
    )

templates = Jinja2Templates(directory="templates")

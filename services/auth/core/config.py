import os
from logging import config as logging_config

from dotenv import load_dotenv

from core.logger import LOGGING

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

QUERY_DESC = "Поисковая строка"
QUERY_ALIAS = "query"

SORT_ORDER_DESC = "Сортировка. asc - по возрастанию, desc - по убыванию"
SORT_ORDER_ALIAS = "sort_order"

SORT_FIELD_DESC = "Поле для сортировки"
SORT_FIELD_ALIAS = "sort_field"

PAGE_DESC = "Номер страницы"
PAGE_ALIAS = "page"

SIZE_DESC = "Количество элементов на странице"
SIZE_ALIAS = "size"

GENRE_DESC = "Фильтр по жанру фильма"
GENRE_ALIAS = "genre_id"

MAX_PAGE_SIZE = 100

MAX_GENRES_SIZE = 50

logging_config.dictConfig(LOGGING)

load_dotenv(f'{BASE_DIR}/env/.env')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    project_name: str = ...
    redis_host: str = Field('redis', alias='REDIS_HOST')
    redis_port: int = Field(6379, alias='REDIS_PORT')
    echo_var: bool = ...
    debug: bool = ...
    secret_key_session: str = ...


settings = Settings()


class OAuthYandexSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    client_id: str = Field(alias='YANDEX_CLIENT_ID')
    client_secret: str = Field(alias='YANDEX_CLIENT_SECRET')
    scope: str = 'login:email'
    api_base_url: str = 'https://login.yandex.ru/'
    authorize_url: str = 'https://oauth.yandex.ru/authorize'
    access_token_url: str = 'https://oauth.yandex.ru/token'
    redirect_uri: str


oauth_yandex = OAuthYandexSettings()


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='postgres_',
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )
    db: str = ...
    user: str = ...
    password: str = ...
    host: str = ...
    port: int = ...


pg = PostgresSettings()

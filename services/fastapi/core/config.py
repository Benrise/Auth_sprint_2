import os
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings

from core.logger import LOGGING

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


class Settings(BaseSettings):
    project_name: str = Field(..., alias='API_PROJECT_NAME')
    service_port: int = Field(8000, alias='API_SERVICE_PORT')
    redis_host: str = Field('redis', alias='API_REDIS_HOST')
    redis_port: int = Field(6379, alias='API_REDIS_PORT')
    elastic_protocol: str = Field('http', alias='API_ELASTIC_PROTOCOL')
    elastic_host: str = Field('elasticsearch', alias='API_ELASTIC_HOST')
    elastic_port: int = Field(9200, alias='API_ELASTIC_PORT')
    debug: bool = Field(True, alias='API_DEBUG')


settings = Settings()

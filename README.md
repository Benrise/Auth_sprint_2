# Проектная работа 5 спринта

### [Auth_sprint_2](https://github.com/Benrise/Auth_sprint_2) - улучшение сервиса авторизации

Команда: [Артём](https://github.com/Benrise)

[Приглашение](https://github.com/Benrise/Auth_sprint_2/invitations)

[Репозиторий](https://github.com/Benrise/Auth_sprint_2)

## Запуск в среде Docker:

1. Сконфигурировать .env файл на примере .env.example

    Для локальной разработки необходимо пробросить порты наружу для нужной бд. В качестве хоста бд установить localhost.

2. Запуск сборки
    ```bash
   docker-compose up -d --build
   ```

3. Далее для сервиса авторизации необходимо локально выполнить следующие команды:

-  Применить последние миграции
    ```bash
    alembic upgrade head
    ```
- Создать стартовый набор ролей
    ```bash
    python create_roles.py
    ```

- Создать суперпользователя
    ```bash
    python create_superuser.py <login> <password>
    ```

    ### Сервис авторизации
    [http://localhost/auth](http://localhost/auth)
    ### Сервис выдачи контента
    [http://localhost/movies](http://localhost/movies)
    ### Сервис администрирования
    [http://localhost/admin](http://localhost/admin)


## OAuth 2.0

1. Поддерживаемые провайдеры: Яндекс

```bash
  http://localhost/auth/api/v1/users/signin/yandex
```

После успешной авторизации вернется ответ в виде 2 токенов.

Реализовано с помощью [Authlib](https://authlib.org/pypi)

## Партицирование
- Реализовано в миграции под версией 593fc7775d55_add_partition
- Для автоматизации и облегчения партиционирования используется pg_partman
- Для корректного применения миграции необходимы права суперпользователя бд

## Ограничие запросов
- Реализовано с помощью библиотеки [fastapi_limiter](https://pypi.org/project/fastapi-limiter/)

## Трассировка
- Работа на основе заголовка x-request-id
- Отправка и отслеживание трассировок в [Jaeger](https://www.jaegertracing.io/)

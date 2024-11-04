# Мини чат на FastApi, websockets

## Используемые технологии
- Fastapi
- PostgreSQL
- SQLAlchemy
- Alembic
- Redis
- Celery
- aiogram

## Описание работы приложения
При старте приложения пользователь попадает на страницу регистрации/авторизации. После успешной авторизации ползователь перенаправляется на страницу чата. На странице выводятся id юзеров, которым можно написать сообщение. Для отправки сообщения в поле Message пишется текст сообщения, в поле Recipient указывается id юзера из списка. Если recipient не в сети, ему придет уведомление в через телеграм бот.


## Запуск приложения
- клонировать репозиторий
```
git clone git@github.com:D-Abramoc/mini_chat_2.git
```
- в папке infra/ создать файл .env и заполнить по примеру env.sample
- поднять контейнеры
```
sudo docker compose -f infra/docker-compose.yml up -d --build
```
- применить миграции
```
sudo docker compose -f infra/docker-compose.yml exec -T backend alembic upgrade head
```

### Приложение доступно по адресу
```
http://127.0.0.1/
```

### Документация
```
http://127.0.0.1/docs
```
### Celery dashboard
```
http://127.0.0.1:5555
```
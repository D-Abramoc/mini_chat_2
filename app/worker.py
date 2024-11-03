import asyncio

from celery import Celery

from app.bot.main import bot
from app.core.config import settings


celery_app = Celery(
    'tasks',
    broker=f'redis://redis:{settings.celery_port}/0',
    backend=f'redis://redis:{settings.celery_port}/0',
)


@celery_app.task
def send_notification(client_id: int, message: str):
    """
    Отправляет уведомление юзеру в тг бот.
    """
    asyncio.get_event_loop().run_until_complete(
        bot.send_message(client_id, message)
    )
    return 'ok'

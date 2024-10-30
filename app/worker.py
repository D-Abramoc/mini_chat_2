import asyncio
from contextlib import asynccontextmanager
from asyncio import current_task

from celery import Celery, shared_task

from app.bot.main import bot
from app.core.config import settings
from app.core.db import AsyncSessionLocal
from app.crud.messages import message_crud
from app.models import Message

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_scoped_session


# sync_engine = create_engine('postgresql://chatuser:chat_pass@db:5432/chatdb)', echo=True)
# SyncSessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=sync_engine,
# )

loop = asyncio.get_event_loop()


@asynccontextmanager
async def scoped_session():
    scoped_factory = async_scoped_session(
        AsyncSessionLocal,
        scopefunc=current_task,
    )
    try:
        async with scoped_factory() as s:
            yield s
    finally:
        await scoped_factory.remove()


async def add_massage(
    sender_id: int, recipient_id: int, content
):
    async with scoped_session() as session:
        await message_crud.add(
            session=session,
            sender_id=sender_id,
            recipient_id=recipient_id,
            content=content
        )


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


@celery_app.task
def create_message_into_db(
    sender_id: int, recipient_id: int, content
):
    """Сохранение сообщения в базу."""
    loop.run_until_complete(add_massage(sender_id, recipient_id, content))
    return 'ok'

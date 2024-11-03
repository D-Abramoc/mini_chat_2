from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.messages import MessageRead
from app.models import User
from app.dependencies import get_current_user
from app.core.db import get_async_session
from app.crud.messages import message_crud


router = APIRouter(prefix='/chat', tags=['Chat'])

templates = Jinja2Templates(directory='app/templates')


@router.get('/', response_class=HTMLResponse)
async def chat_page(
    request: Request,
    user_data: Annotated[User, Depends(get_current_user)]
):
    """Возвращает страницу чата."""
    return templates.TemplateResponse(
        'chat.html',
        {'request': request,
         'user': user_data}
    )


@router.get('/messages/{user_id}', response_model=list[MessageRead])
@cache(expire=120)
async def get_messages_between_users(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Возвращает историю сообщений между пользователями."""
    return await message_crud.get_messages_between_users(
        user_id_1=user_id,
        user_id_2=current_user.id,
        session=session
    ) or []

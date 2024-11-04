from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.users import user_crud
from app.schemas.users import SUserRead

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/', response_model=list[SUserRead])
@cache(expire=120)
async def get_users(
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    """Возвращает список пользователей."""
    return await user_crud.find_all(session=session)

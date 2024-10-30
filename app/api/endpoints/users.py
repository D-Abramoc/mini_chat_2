from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.users import SUserRead
from app.core.db import get_async_session
from app.crud.users import user_crud


router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/', response_model=list[SUserRead])
async def get_users(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return await user_crud.find_all(session=session)

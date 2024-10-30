from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_auth_data
from app.exceptions import (
    TokenExpiredException, NoJwtException, NoUserIdException,
    TokenNoFoundException,
)
from app.crud.users import user_crud
from app.core.db import get_async_session
from app.models import User


def get_token(request: Request):
    """Извлечение токена из куки."""
    token = request.cookies.get('users_access_token')
    if not token:
        raise TokenNoFoundException
    return token


async def get_current_user(token: str = Depends(get_token),
                           session: AsyncSession = Depends(get_async_session)) -> User:
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(
            token, auth_data['secret_key'], algorithms=auth_data['algorithm']
        )
    except JWTError:
        raise NoJwtException

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id: str = payload.get('sub')
    if not user_id:
        raise NoUserIdException

    user = await user_crud.find_one_or_none_by_id(
        int(user_id), session=session
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found'
        )
    return user

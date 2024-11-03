from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.users import SUserAuth, SUserRegister
from app.core.db import get_async_session
from app.crud.users import user_crud
from app.exceptions import (
    UserAlreadyExistsException, PasswordMismatchException,
    IncorrectEmailOrPasswordException,
)
from app.api.utils.auth import (
    get_password_hash, authenticate_user, create_access_token
)


router = APIRouter(prefix='/auth', tags=['Auth'])

templates = Jinja2Templates(directory='app/templates')


@router.get('/', response_class=HTMLResponse)
async def get_auth_page(request: Request):
    """Возвращает страницу регистрации/авторизации."""
    return templates.TemplateResponse(
        'auth.html',
        {'request': request}
    )


@router.post('/register')
async def register_user(
    user_data: SUserRegister,
    session: AsyncSession = Depends(get_async_session)
) -> dict[str, str]:
    """Регистрация пользователя."""
    user = await user_crud.find_one_or_none(session, email=user_data.email)
    if user:
        raise UserAlreadyExistsException
    if user_data.password != user_data.password_check:
        raise PasswordMismatchException('Пароли не совпадают')
    hashed_password = get_password_hash(user_data.password)
    await user_crud.add(
        session,
        name=user_data.name,
        email=user_data.email,
        password=hashed_password
    )

    return {'message': 'Вы успешно зарегистрированы!'}


@router.post('/login/')
async def auth_user(
    response: Response, user_data: SUserAuth,
    session: AsyncSession = Depends(get_async_session)
):
    """Аутентификация пользователя и установка куки."""
    check = await authenticate_user(
        email=user_data.email, password=user_data.password, session=session
    )
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({'sub': str(check.id)})
    response.set_cookie(
        key='users_access_token', value=access_token, httponly=True
    )
    return {
        'ok': True,
        'access_token': access_token,
        'refresh_token': None,
        'message': 'Авторизация успешна!'
    }


@router.post("/logout/")
async def logout_user(response: Response):
    """Выход пользователя."""
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}

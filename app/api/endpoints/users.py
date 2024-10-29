from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix='/auth', tags=['Auth'])

templates = Jinja2Templates(directory='app/templates')


@router.get('/', response_class=HTMLResponse)
async def get_auth_page(request: Request):
    return templates.TemplateResponse(
        'auth.html',
        {'request': request}
    )

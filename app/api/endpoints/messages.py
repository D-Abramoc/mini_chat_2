from typing import Annotated

from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils.messages import manager
from app.schemas.messages import MessageRead
from app.models import User
from app.dependencies import get_current_user
from app.core.db import get_async_session
from app.crud.messages import message_crud


router = APIRouter(prefix='/chat', tags=['Chat'])

templates = Jinja2Templates(directory='app/templates')


@router.get('/', response_class=HTMLResponse)
async def chat_page(request: Request, user_data: Annotated[User, Depends(get_current_user)]):
    return templates.TemplateResponse(
        'chat.html',
        {'request': request,
         'user': user_data}
    )


@router.get('/messages/{user_id}', response_model=list[MessageRead])
async def get_messages_between_users(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    return await message_crud.get_messages_between_users(
        user_id_1=user_id,
        user_id_2=current_user.id,
        session=session
    ) or []


# @router.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.send_personal_message(f"You wrote: {data}", websocket)
#             await manager.broadcast(f"Client #{client_id} says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client #{client_id} left the chat")

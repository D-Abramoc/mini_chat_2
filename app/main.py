from typing import Annotated

from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.messages import router as messages_router
from app.api.endpoints.users import router as users_router
from app.api.utils.messages import manager
from app.crud.messages import message_crud
from app.dependencies import get_async_session
from app.redis_app import redis as r

app = FastAPI()
app.mount('/static', StaticFiles(directory='app/static'), name='static')


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth_router)
app.include_router(messages_router)
app.include_router(users_router)


@app.on_event("startup")
async def startup_event():
    FastAPICache.init(RedisBackend(redis=r), prefix='fastapi-cache')


@app.get("/")
async def redirect_to_auth():
    return RedirectResponse(url="/auth")


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket, client_id: int,
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    await manager.connect(client_id, websocket)
    try:
        while True:
            try:
                data = await websocket.receive_text()
            except WebSocketDisconnect:
                manager.disconnect(client_id)
            try:
                to_recipient, message = data.split(maxsplit=1)
            except ValueError:
                to_recipient = data.strip()
                message = 'Отправлено пустое сообщение.'
            except UnboundLocalError:
                break
            try:
                await message_crud.add(
                    session=session,
                    sender_id=client_id,
                    recipient_id=int(to_recipient),
                    content=message
                )
            except IntegrityError:
                to_recipient = to_recipient
                message = 'Такого пользователя не существует.'
            await manager.send_personal_message(
                    f"Сообщение пользователю {to_recipient}: {message}",
                    websocket
                )
            await manager.send_message_to_user(
                    f"Сообщение от пользователя {client_id}: {message}",
                    int(to_recipient)
                )
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast(f"Client #{client_id} left the chat")
    except Exception:
        pass

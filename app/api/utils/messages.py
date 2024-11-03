from fastapi import WebSocket

from app.core.db import AsyncSessionLocal
from app.crud.users import user_crud
from app.worker import send_notification


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        try:
            del self.active_connections[user_id]
        except TypeError:
            pass

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: str):
        for _, connection in self.active_connections.items():
            await connection.send_json(message)

    async def send_message_to_user(self, message: str, user_id: str,):
        if user_id not in self.active_connections:
            async with AsyncSessionLocal() as session:
                user = await user_crud.find_one_or_none(
                    session, id=int(user_id)
                )
            if user is None:
                pass
            else:
                send_notification.delay(user.tg_id, 'You have a message')
        else:
            connection = self.active_connections[user_id]
            await connection.send_text(message)


manager = ConnectionManager()

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.utils.messages import manager


router = APIRouter(prefix='/chat', tags=['Chat'])

templates = Jinja2Templates(directory='app/templates')


@router.get('/', response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse(
        'chat.html',
        {'request': request}
    )


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

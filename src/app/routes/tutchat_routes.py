from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import List, Dict
from config import TEMPLATES_PATH
from auth import get_current_user
from utils.templates import verstkaprofile
from services.chat_service import getchatsbytutorid, addmessage, getstudentchatinfo, getchatmessages
from services.stats_tut_service import gettutorinfo, gettutinfobyid
import asyncio
import json

router = APIRouter()


active_connections: Dict[str, List[WebSocket]] = {}



@router.get("/tutchat/{room_name}")
def tutchat(request: Request, room_name: str):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        tutorinfo = gettutorinfo(name)
        tutor_id = tutorinfo[2]
        tutfirst_name = tutorinfo[0]
        tutlast_name = tutorinfo[1]

        contact_template = ""

        with open(f"{TEMPLATES_PATH}cards/tutcontact.html", 'r', encoding="utf-8") as f:
            contact_card = f.read()

        chats = getchatsbytutorid(tutor_id)

        for chat in chats:
            contact_template += contact_card

            chat_id = chat[0]
            student_first_name = chat[2]
            student_last_name = chat[3]
            last = chat[5]

            contact_template = contact_template.replace("{{ chat_id }}", str(chat_id))
            contact_template = contact_template.replace("{{ contact_avatar }}", str(student_first_name)[0] + str(student_last_name)[0])
            contact_template = contact_template.replace("{{ contact_first_name }}", str(student_first_name))
            contact_template = contact_template.replace("{{ contact_last_name }}", str(student_last_name))
            contact_template = contact_template.replace("{{ last_message }}", str(last))

        studinfo = getstudentchatinfo(chat_id)
        student_id = studinfo[0]
        studfirst_name = studinfo[1]
        studlast_name = studinfo[2]


        messages_history = getchatmessages(room_name)
    
        messages_template= ""
        for message in messages_history:
            message_id = message[0]
            sender_id = message[1]
            sender_type = message[2]
            message_text = message[3]
            created_at = message[4]

            if sender_type == 'tutor' and sender_id == tutor_id:
                message_class = "my-message"
                sender_name = str(tutfirst_name) + str(tutlast_name)

            elif sender_type == 'system':
                message_class = "system-message"
                sender_name = "system"
            else:
                message_class = "other-message"
                sender_name = str(studfirst_name) + str(studlast_name)

            message_card = f"""
            <div class="message {message_class}">
                <strong>{sender_name}</strong> [{created_at}]<br>
                {message_text}
            </div>
            """
            messages_template += message_card

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url='/login', status_code=303)

    with open (f"{TEMPLATES_PATH}chat/tutchat.html", 'r', encoding='utf-8') as f:
        content = verstkaprofile(f.read(), name, tutfirst_name, tutlast_name)
    content = content.replace("{{ contacts_template }}", str(contact_template))
    content = content.replace("{{ room_name }}", str(room_name))
    content = content.replace("{{ dialog_first_name }}", str(studfirst_name))
    content = content.replace("{{ dialog_last_name }}", str(studlast_name))
    content = content.replace("{{ tutfirst_name }}", str(tutfirst_name))
    content = content.replace("{{ tutlast_name }}", str(tutlast_name))
    content = content.replace("{{ tutor_id }}", str(tutor_id))
    content = content.replace("{{ messages_template }}", str(messages_template))
    return HTMLResponse(content=content)



@router.post("/savetutmessage")
async def save_message(request: Request):
    data = await request.json()
    
    room_id = data.get("room_id")
    sender_id = data.get("sender_id")
    sender_type = data.get("sender_type")
    text = data.get("text")
    
    if not all([room_id, sender_id, sender_type, text]):
        return {"error": "Missing required fields"}
    
    addmessage(room_id, sender_id, sender_type, text)
    print(f"Сохранил в комнате - {room_id}")
    
    return {"status": "ok"}

@router.post("/savestudentmessage")
async def save_message(request: Request):
    data = await request.json()
    
    room_id = data.get("room_id")
    sender_id = data.get("sender_id")
    sender_type = data.get("sender_type")
    text = data.get("text")
    
    if not all([room_id, sender_id, sender_type, text]):
        return {"error": "Missing required fields"}
    
    addmessage(room_id, sender_id, sender_type, text)
    
    return {"status": "ok"}


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, username: str = "Аноним"):
    try:
        await websocket.accept()
        print(f"✅ WebSocket принят: {room_id} {username}")
    except Exception as e:
        print(f"❌ Ошибка при accept: {e}")
        return

    try:
        # Добавляем в комнату
        if room_id not in active_connections:
            active_connections[room_id] = []
        active_connections[room_id].append(websocket)

        # Уведомляем всех в комнате о новом пользователе
        await broadcast_to_room(room_id, {
            "type": "system",
            "text": f"{username} присоединился к чату"
        }, exclude=websocket)

        # Отправляем новому пользователю список всех в комнате
        await websocket.send_json({
            "type": "users",
            "users": [f"Пользователь {i+1}" for i in range(len(active_connections[room_id]))]
        })

        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            if message_data["type"] == "message":
                await broadcast_to_room(room_id, {
                    "type": "message",
                    "sender": username,
                    "text": message_data["text"]
                })
    except WebSocketDisconnect:
        if room_id in active_connections:
            active_connections[room_id].remove(websocket)
            if not active_connections[room_id]:
                del active_connections[room_id]
        await broadcast_to_room(room_id, {
            "type": "system",
            "text": f"{username} покинул чат"
        })
    except Exception as e:
        import traceback
        traceback.print_exc()


async def broadcast_to_room(room_id: str, message: dict, exclude: WebSocket = None):
    """Отправить сообщение всем в комнате"""
    if room_id in active_connections:
        for connection in active_connections[room_id]:
            if connection != exclude:
                try:
                    await connection.send_json(message)
                except:
                    pass
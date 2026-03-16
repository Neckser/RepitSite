from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
import json
import asyncio
from typing import Dict, List, Any
from datetime import datetime
import uuid
from config import TEMPLATES_PATH
from auth import get_current_user
from utils.templates import verstkaprofile
from services.stats_tut_service import gettutorinfo
from services.stats_stud_service import getstudinfo

router = APIRouter()

# Хранилище комнат: token -> {connections: [], drawings: [], images: []}
rooms: Dict[str, Dict[str, Any]] = {}

@router.get("/tutboard/{board_id}")
async def tutboard(request: Request, board_id: str):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        tutorinfo = gettutorinfo(name)
        tutfirst_name = tutorinfo[0]
        tutlast_name = tutorinfo[1]
        tutor_id = tutorinfo[2]
        
        with open(f"{TEMPLATES_PATH}boards/tutboard.html", 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, tutfirst_name, tutlast_name)
        
        content = content.replace("{{ board_id }}", str(board_id))
        return HTMLResponse(content=content)
        
    except Exception as e:
        print(f"Ошибка в tutboard: {e}")
        return RedirectResponse(url="/login", status_code=303)


@router.websocket("/ws/board/{room_token}")
async def websocket_endpoint(websocket: WebSocket, room_token: str):
    await websocket.accept()
    
    print(f"Новое подключение к комнате: {room_token}")
    
    # Создаем комнату если её ещё нет
    if room_token not in rooms:
        rooms[room_token] = {
            "connections": [],
            "drawings": [],  # Сохраненные линии
            "images": []     # Сохраненные картинки (base64 + координаты)
        }
        print(f"Создана новая комната: {room_token}")
    
    # Добавляем соединение в комнату
    rooms[room_token]["connections"].append(websocket)
    print(f"В комнате {room_token} сейчас {len(rooms[room_token]['connections'])} пользователей")
    
    # Отправляем новому пользователю текущее состояние комнаты
    await websocket.send_json({
        "type": "init",
        "data": {
            "drawings": rooms[room_token]["drawings"],
            "images": rooms[room_token]["images"]
        }
    })
    
    try:
        while True:
            # Получаем сообщение от клиента
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Добавляем отправителя в сообщение
            message["sender"] = id(websocket)
            
            # Обрабатываем разные типы сообщений
            if message["type"] == "draw_line":
                # Сохраняем линию в историю комнаты
                rooms[room_token]["drawings"].append(message["data"])
                # Ограничиваем историю (последние 1000 линий)
                if len(rooms[room_token]["drawings"]) > 1000:
                    rooms[room_token]["drawings"] = rooms[room_token]["drawings"][-1000:]
                
            elif message["type"] == "add_image":
                # Сохраняем картинку в историю комнаты
                rooms[room_token]["images"].append(message["data"])
                
            elif message["type"] == "move_image":
                # Обновляем позицию картинки
                for i, img in enumerate(rooms[room_token]["images"]):
                    if img["id"] == message["data"]["id"]:
                        rooms[room_token]["images"][i]["x"] = message["data"]["x"]
                        rooms[room_token]["images"][i]["y"] = message["data"]["y"]
                        break
                        
            elif message["type"] == "resize_image":
                # Обновляем размер картинки
                for i, img in enumerate(rooms[room_token]["images"]):
                    if img["id"] == message["data"]["id"]:
                        rooms[room_token]["images"][i]["width"] = message["data"]["width"]
                        rooms[room_token]["images"][i]["height"] = message["data"]["height"]
                        rooms[room_token]["images"][i]["x"] = message["data"]["x"]
                        rooms[room_token]["images"][i]["y"] = message["data"]["y"]
                        break
                        
            elif message["type"] == "delete_image":
                # Удаляем картинку
                rooms[room_token]["images"] = [
                    img for img in rooms[room_token]["images"] 
                    if img["id"] != message["data"]["id"]
                ]
                
            elif message["type"] == "clear_board":
                # Очищаем всю доску
                rooms[room_token]["drawings"] = []
                rooms[room_token]["images"] = []
            
            # Рассылаем сообщение всем в комнате (кроме отправителя)
            for connection in rooms[room_token]["connections"]:
                if connection != websocket:
                    try:
                        await connection.send_json(message)
                    except:
                        pass
    
    except WebSocketDisconnect:
        # Удаляем соединение из комнаты
        rooms[room_token]["connections"].remove(websocket)
        print(f"Пользователь отключился. В комнате {room_token} осталось {len(rooms[room_token]['connections'])} пользователей")
        
        # Если комната пустая, можно её удалить (опционально)
        if len(rooms[room_token]["connections"]) == 0:
            del rooms[room_token]
            print(f"Комната {room_token} удалена (пуста)")


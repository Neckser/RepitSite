from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
import json
from typing import Dict, Any
from config import TEMPLATES_PATH
from auth import get_current_user
from utils.templates import verstkaprofile
from services.stats_tut_service import gettutorinfo

router = APIRouter()

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
    
    if room_token not in rooms:
        rooms[room_token] = {
            "connections": [],
            "drawings": [],
            "images": []
        }
        print(f"Создана новая комната: {room_token}")
    
    rooms[room_token]["connections"].append(websocket)
    print(f"В комнате {room_token} сейчас {len(rooms[room_token]['connections'])} пользователей")
    
    await websocket.send_json({
        "type": "init",
        "data": {
            "drawings": rooms[room_token]["drawings"],
            "images": rooms[room_token]["images"]
        }
    })
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            message["sender"] = id(websocket)
            if message["type"] == "draw_line":
                rooms[room_token]["drawings"].append(message["data"])
                if len(rooms[room_token]["drawings"]) > 1000:
                    rooms[room_token]["drawings"] = rooms[room_token]["drawings"][-1000:]
                
            elif message["type"] == "add_image":
                rooms[room_token]["images"].append(message["data"])
                
            elif message["type"] == "move_image":
                for i, img in enumerate(rooms[room_token]["images"]):
                    if img["id"] == message["data"]["id"]:
                        rooms[room_token]["images"][i]["x"] = message["data"]["x"]
                        rooms[room_token]["images"][i]["y"] = message["data"]["y"]
                        break
                        
            elif message["type"] == "resize_image":
                for i, img in enumerate(rooms[room_token]["images"]):
                    if img["id"] == message["data"]["id"]:
                        rooms[room_token]["images"][i]["width"] = message["data"]["width"]
                        rooms[room_token]["images"][i]["height"] = message["data"]["height"]
                        rooms[room_token]["images"][i]["x"] = message["data"]["x"]
                        rooms[room_token]["images"][i]["y"] = message["data"]["y"]
                        break
                        
            elif message["type"] == "delete_image":
                rooms[room_token]["images"] = [
                    img for img in rooms[room_token]["images"] 
                    if img["id"] != message["data"]["id"]
                ]
                
            elif message["type"] == "clear_board":
                rooms[room_token]["drawings"] = []
                rooms[room_token]["images"] = []
            
            for connection in rooms[room_token]["connections"]:
                if connection != websocket:
                    try:
                        await connection.send_json(message)
                    except:
                        pass
    
    except WebSocketDisconnect:
        rooms[room_token]["connections"].remove(websocket)
        print(f"Пользователь отключился. В комнате {room_token} осталось {len(rooms[room_token]['connections'])} пользователей")
        if len(rooms[room_token]["connections"]) == 0:
            del rooms[room_token]
            print(f"Комната {room_token} удалена (пуста)")


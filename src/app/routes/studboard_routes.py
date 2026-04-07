from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
import json
import asyncio
import html
from typing import Dict, List, Any
from datetime import datetime
import uuid
from config import TEMPLATES_PATH
from auth import get_current_user
from utils.templates import verstkaprofile
from services.stats_tut_service import gettutorinfo
from services.stats_stud_service import getstudinfo

router = APIRouter()

@router.get("/studboard/{board_id}")
async def studboard(request: Request, board_id: str):
    try:
        name, user_type = get_current_user(request)
        if user_type != "student":
            return RedirectResponse(url="/login", status_code=303)
    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        studinfo = getstudinfo(name)
        studfirst_name = studinfo[0]
        studlast_name = studinfo[1]
        student_id = studinfo[2]
        
        with open(f"{TEMPLATES_PATH}boards/studboard.html", 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, studfirst_name, studlast_name)
        content = content.replace("{{ board_id }}", html.escape(str(board_id)))
        return HTMLResponse(content=content)
        
    except Exception as e:
        print(f"Ошибка в studboard: {e}")
        return RedirectResponse(url="/login", status_code=303)
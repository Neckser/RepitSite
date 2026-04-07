from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import List, Dict
from config import TEMPLATES_PATH
from auth import get_current_user
from utils.templates import verstkaprofile
from services.chat_service import  getchatmessages, gettutorchatinfo, checkchatexists
from services.stats_tut_service import gettutorinfo, gettutinfobyid
from services.stats_stud_service import getstudinfo
import asyncio
import json
import html

router = APIRouter()

@router.get("/studchat/{room_name}")
def studchat(request: Request, room_name: str):
    try:
        name, user_type = get_current_user(request)
        if user_type != "student":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)
    
    if checkchatexists(room_name) == False:
        with open(f'{TEMPLATES_PATH}errors/error.html', 'r', encoding='utf-8') as f:
            content = f.read()
        return HTMLResponse(content=content, status_code=404)
    
    studinfo = getstudinfo(name)
    studfirst_name = studinfo[0]
    studlast_name = studinfo[1]
    student_id = studinfo[2]


    tutinfo = gettutorchatinfo(room_name)
    tutfirst_name = tutinfo[1]
    tutlast_name = tutinfo[2]


    messages_history = getchatmessages(room_name)
    
    messages_template= ""
    for message in messages_history:
        message_id = message[0]
        sender_id = message[1]
        sender_type = message[2]
        message_text = message[3]
        created_at = message[4]

        if sender_type == 'student' and sender_id == student_id:
            message_class = "my-message"
            sender_name = studfirst_name + studlast_name
        elif sender_type == 'system':
            message_class = "system-message"
            sender_name = "system"
        else:
            message_class = "other-message"
            sender_name = str(tutfirst_name) + str(tutlast_name)

        message_card = f"""
        <div class="message {message_class}">
            <strong>{sender_name}</strong> [{created_at}]<br>
            {html.escape(message_text)}
        </div>
        """
        messages_template += message_card

    
    with open(f"{TEMPLATES_PATH}chat/studchat.html", 'r', encoding='utf-8') as f:
        content = verstkaprofile(f.read(), name, studfirst_name, studlast_name)
    content = content.replace("{{ messages_template }}", str(messages_template))
    content = content.replace("{{ dialog_first_name }}", html.escape(str(tutfirst_name)))
    content = content.replace("{{ dialog_last_name }}", html.escape(str(tutlast_name)))
    content = content.replace("{{ room_name }}", html.escape(str(room_name)))
    content = content.replace("{{ student_id }}", html.escape(str(student_id)))
    content = content.replace("{{ studfirst_name }}", html.escape(str(studfirst_name)))
    content = content.replace("{{ studlast_name }}", html.escape(str(studlast_name)))

    return HTMLResponse(content=content)
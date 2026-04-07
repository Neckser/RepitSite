from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from config import TEMPLATES_PATH
from auth import get_current_user
from utils.templates import verstkaprofile
from services.stats_stud_service import getstudinfo, getstudhw
from services.stats_tut_service import getstudcolvo, gettuthwcolvo, getstudents, gettutorinfo, gettodaylessonscolvo
from services.hw_service import updatehwstatus
from services.chat_service import getchatid
import html

router = APIRouter()

@router.get("/home")
def home(request: Request):
    try:
        name, user_type = get_current_user(request)
        if user_type != "student":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:

        updatehwstatus()

        hwtemplate = ""

        with open(f'{TEMPLATES_PATH}cards/hwcard.html', 'r', encoding='utf-8') as f:
            a = f.read()

        studinfo = getstudinfo(name)
        first_name = studinfo[0]
        last_name = studinfo[1]
        student_id = studinfo[2]

        homeworks = getstudhw(student_id)

        if homeworks:
            for hw in homeworks:
                hwtemplate += a
                if hw[3] == "Активно":
                    hwtemplate = hwtemplate.replace("{{ status_line }}", "<span class='status active'>Активно</span>")
                elif hw[3] == "Завершено":
                    hwtemplate = hwtemplate.replace("{{ status_line }}", "<span class='status completed'>Завершено</span>")
                # hwtemplate = hwtemplate.replace("{{ status }}", str(hw[3]))
                hwtemplate = hwtemplate.replace("{{ title }}", html.escape(str(hw[0])))
                hwtemplate = hwtemplate.replace("{{ data }}", html.escape(str(hw[2])))
                hwtemplate = hwtemplate.replace("{{ description }}", html.escape(str(hw[1])))
                hwtemplate = hwtemplate.replace("{{ tutor_first_name }}", html.escape(str(hw[4])))
                hwtemplate = hwtemplate.replace("{{ tutor_last_name }}", html.escape(str(hw[5])))
                hwtemplate = hwtemplate.replace("{{ subject }}", html.escape(str(hw[6])))
                
        
        else:
            with open(f'{TEMPLATES_PATH}cards/nohw.html', 'r', encoding="utf-8") as f:
                hwtemplate = f.read() 
        with open(f"{TEMPLATES_PATH}mainpages/mainpage.html", "r", encoding = "utf-8") as f:
            content = verstkaprofile(f.read(), name, first_name, last_name)
        content = content.replace("{{ hwtemplate }}", hwtemplate)
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    

@router.get("/hometut")
def hometut(request: Request):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        studtemplate = ""

        with open(f'{TEMPLATES_PATH}cards/studcard.html', 'r', encoding='utf-8') as f:
            a = f.read()

        tutinfo = gettutorinfo(name)
        tutfirst_name = tutinfo[0]
        tutlast_name = tutinfo[1]
        tutor_id = tutinfo[2]
        
        student_colvo = getstudcolvo(name)

        tuthomework_colvo = gettuthwcolvo(name)

        lessons_today_colvo = gettodaylessonscolvo()

        students = getstudents(name)

        for student in students:
            studtemplate += a
            student_id = student[0]
            studfirst_name = student[1]
            studlast_name = student[2]
            chat_id = getchatid(student_id, tutor_id)

            studtemplate = studtemplate.replace("{{ first_name }}", html.escape(str(studfirst_name)))
            studtemplate = studtemplate.replace("{{ last_name }}", html.escape(str(studlast_name)))
            studtemplate = studtemplate.replace("{{ grade }}", html.escape(str(student[5])))
            studtemplate = studtemplate.replace("{{ avatarstud }}", html.escape(str(studfirst_name[0] + studlast_name[0])))
            studtemplate = studtemplate.replace("{{ chat_id }}", html.escape(str(chat_id)))

        with open(f'{TEMPLATES_PATH}mainpages/hometut.html', 'r', encoding='utf-8') as file:
            content = verstkaprofile(file.read(), name, tutfirst_name, tutlast_name)
        content = content.replace("{{ student_colvo }}", html.escape(str(student_colvo)))
        content = content.replace("{{ homework_colvo }}", html.escape(str(tuthomework_colvo)))
        content = content.replace("{{ studtemplate }}", str(studtemplate))
        content = content.replace("{{ lessons_today }}", html.escape(str(lessons_today_colvo)))
        return HTMLResponse(content=content)
    
    except Exception as e: 
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
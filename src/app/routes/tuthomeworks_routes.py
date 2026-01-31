from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from config import TEMPLATES_PATH
from auth import get_current_user
from utils.templates import verstkaprofile
from services.stats_tut_service import gettutorinfo, getstudents, gettuthw
from services.hw_service import updatehwstatus, addhw, delhw

router = APIRouter()

@router.get("/homeworkstut")
def homeworkstut(request: Request):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:

        updatehwstatus()

        optionTemaplate = '''<select class="assignment-form__select" id="student_id" name="student_id" required>
        <option value="">Выберите ученика</option>'''

        hwtemplate = ""

        with open(f'{TEMPLATES_PATH}cards/hwtutcard.html', 'r', encoding='utf-8') as f:
            a = f.read()

        tutinfo = gettutorinfo(name)
        tutfirst_name = tutinfo[0]
        tutlast_name = tutinfo[1]
        tutor_id = tutinfo[2]
        
        students = getstudents(name)

        if students:
            for student in students:
                optionTemaplate += f'   <option value="{student[0]}">{student[1]} {student[2]} ({student[5]} класс)</option>'
        optionTemaplate += "</select>"


        homeworks = gettuthw(tutor_id)

        if homeworks:
            for hw in homeworks:
                hwtemplate += a
                hwtemplate = hwtemplate.replace("{{ status }}", str(hw[3]))
                hwtemplate = hwtemplate.replace("{{ title }}", str(hw[0]))
                hwtemplate = hwtemplate.replace("{{ data }}", str(hw[2]))
                hwtemplate = hwtemplate.replace("{{ description }}", str(hw[1]))
                hwtemplate = hwtemplate.replace("{{ subject }}", str(hw[4]))
                hwtemplate = hwtemplate.replace("{{ homework_id }}", str(hw[5]))
        
        with open(f'{TEMPLATES_PATH}homeworks/homeworkstut.html', 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, tutfirst_name, tutlast_name)
        content = content.replace("{{ selectForm }}", optionTemaplate)
        content = content.replace("{{ hwtemplate }}", hwtemplate)
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)


@router.post("/createhw")
def createhw(request: Request, student_id: str = Form(...), subject: str = Form(...), title: str = Form(...), deadline: str = Form(...), description: str = Form(...)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        tutinfo = gettutorinfo(name)
        tutor_id = tutinfo[2]

        addhw(student_id, tutor_id, title, description, subject, deadline)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    
    return RedirectResponse(url=f"/homeworkstut", status_code=303)


@router.post("/deletehw")
def deletehw(request: Request, homework_id: str = Form(...)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:

        delhw(homework_id)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

    return RedirectResponse(url=f"/homeworkstut", status_code=303)
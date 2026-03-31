from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from config import TEMPLATES_PATH
from auth import get_current_user
from utils.templates import verstkaprofile
from utils.validation import checkrequiredfields
from services.stats_stud_service import getstudinfo, gettutlist
from services.stats_tut_service import getstudcolvo, gettutsubject
from services.findtut_service import addtutor
from services.auth_tut_service import checktutexistsbyid
from services.chat_service import generatecontacttotutor, getchatid

router = APIRouter()

@router.get("/tutlist")
def tutlist(request: Request):
    
    try:
        name, user_type = get_current_user(request)
        if user_type != "student":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        tuttemplate = ""

        with open(f'{TEMPLATES_PATH}cards/tutcards.html', 'r', encoding='utf-8') as f:
            a = f.read()

        studinfo = getstudinfo(name)
        studfirst_name = studinfo[0]
        studlast_name = studinfo[1]
        student_id = studinfo[2]

        tutorlist = gettutlist(name)

        for tutor in tutorlist:
            tutor_id = tutor[0]
            tutfirst_name = tutor[1]
            tutlast_name = tutor[2]
            tutlogin = tutor[4]
            student_colvo = getstudcolvo(tutlogin)
            tutsubjects = gettutsubject(tutlogin)

            chat_id = getchatid(student_id, tutor_id)

            subjecttemplate = ""

            tuttemplate += a

            for tutsubject in tutsubjects:
                subjecttemplate += f'''<span class="subject-badge {tutsubject}">{tutsubject}</span>'''

            tuttemplate = tuttemplate.replace("{{ first_name }}", tutfirst_name)
            tuttemplate = tuttemplate.replace("{{ last_name }}", tutlast_name)
            tuttemplate = tuttemplate.replace("{{ avatar }}", tutfirst_name[0] + tutlast_name[0])
            tuttemplate = tuttemplate.replace("{{ student_colvo }}", str(student_colvo))
            tuttemplate = tuttemplate.replace("{{ subjecttemplate }}", subjecttemplate)
            tuttemplate = tuttemplate.replace("{{ lesson_count }}", '🚧')
            tuttemplate = tuttemplate.replace("{{ rating }}", '🚧')
            tuttemplate = tuttemplate.replace("{{ chat_id }}", str(chat_id))

        with open(f'{TEMPLATES_PATH}findtut/tutlist.html', 'r', encoding="utf-8") as f:
            content = verstkaprofile(f.read(), name, studfirst_name, studlast_name)

        content = content.replace("{{ tuttemplate }}", tuttemplate)

        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

@router.get("/findtut")
def findtut(request: Request):
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

        with open(f"{TEMPLATES_PATH}findtut/findtut.html", "r", encoding = "utf-8") as f:
            content = verstkaprofile(f.read(), name, studfirst_name, studlast_name)
            return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Ловит ошибку - { e }")
        return RedirectResponse(url="/login", status_code=303)
    


@router.post("/addtut")
def addtut(request: Request, tutor_code: str = Form(None)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "student":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        form_data = {"tutor_code": tutor_code}
        error_validation = checkrequiredfields(form_data, ["tutor_code"],f"{TEMPLATES_PATH}findtut/findtut.html")
        if error_validation:
            return RedirectResponse(url=f"/tutlist", status_code=303)

        studinfo = getstudinfo(name)
        student_id = studinfo[2]
        studfirst_name = studinfo[0]
        studlast_name = studinfo[1]

        if checktutexistsbyid(tutor_code):

            addtutor(student_id, tutor_code)

            generatecontacttotutor(student_id, tutor_code)


        else:
            with open(f"{TEMPLATES_PATH}findtut/findtutidfailed.html", "r", encoding='utf-8') as file:
                content = verstkaprofile(file.read(), name, studfirst_name, studlast_name)
            return HTMLResponse(content=content)

        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)   
    
    return RedirectResponse(url=f"/tutlist", status_code=303)


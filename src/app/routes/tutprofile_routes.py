from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from config import TEMPLATES_PATH
from auth import get_current_user
from utils.templates import verstkaprofile
from services.stats_tut_service import gettutorinfo, getstudcolvo, gettutsubject
from services.profile_service import editutbasic, edittutbio, edittutsubjects

router = APIRouter()

@router.get("/profiletut")
def profiletut(request: Request):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        tutinfo = gettutorinfo(name)
        tutfirst_name = tutinfo[0]
        tutlast_name = tutinfo[1]
        tutor_id = tutinfo[2]
        experience = tutinfo[3]
        bio = tutinfo[4]
        
        student_colvo = getstudcolvo(name)

        tutsubjects = gettutsubject(name)

        profiletutsubjecttemplate = ""

        if bio is None or bio == "":
            bio = "Всем привет - я использую RepitHub"

        for tutsubject in tutsubjects:
                profiletutsubjecttemplate += f'''<span class="subject-badge {tutsubject}">{tutsubject}</span>'''

        with open(f'{TEMPLATES_PATH}profiles/profiletut.html', 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, tutfirst_name, tutlast_name)
        content = content.replace("{{ experience }}", str(experience))
        content = content.replace("{{ student_colvo }}", str(student_colvo))
        content = content.replace("{{ repcode }}", str(tutor_id))
        content = content.replace("{{ profiletutsubjecttemplate }}", profiletutsubjecttemplate)
        content = content.replace("{{ bio }}", str(bio))
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)


@router.get("/edittutprofile")
def edittutprofile(request: Request):
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

        with open(f'{TEMPLATES_PATH}profiles/edittutprofile.html', 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, tutfirst_name, tutlast_name)
        return HTMLResponse(content=content)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    

@router.post("/updatetutbasic")
def updatetutbasic(request: Request, first_name: str = Form(...), last_name: str = Form(...), experience: int = Form(...)):
    try:
        name, user_type = get_current_user(request)

        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:

        editutbasic(first_name, last_name, experience, name)

        return RedirectResponse(url="/profiletut", status_code=303)
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

    
@router.post("/updatetutsubjects")
async def updatetutsubjects(request: Request):
    try:
        name, user_type = get_current_user(request)

        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        form_data = await request.form()
        selected_subjects = form_data.getlist("subjects")

        edittutsubjects(selected_subjects, name)

        return RedirectResponse(url="/profiletut", status_code=303)
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

@router.post("/updatetutbio")
def updatetutbio(request: Request, bio: str = Form("")):
    try:
        name, user_type = get_current_user(request)

        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:

        edittutbio(bio, name)

        return RedirectResponse(url="/profiletut", status_code=303)
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from config import TEMPLATES_PATH
from auth import get_current_user
from utils.templates import verstkaprofile
from services.stats_stud_service import getstudinfo, getstudcompletedhwcolvo, getstudhwcolvo, gettutorcount, getavggrade
from services.profile_service import editstudbasic, editstudbio

router = APIRouter()

@router.get("/profile")
def studprofile(request: Request):
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
        grade = studinfo[3]
        bio = studinfo[4]
            
        homework_colvo = getstudhwcolvo(name)

        completed_homeworks = getstudcompletedhwcolvo(name)
        
        tutor_count = gettutorcount(name)

        avggrade = getavggrade(name)

        if bio is None or bio == "":
            bio = "Всем привет - я использую RepitHub"

        with open(f"{TEMPLATES_PATH}profiles/studprofile.html", "r", encoding = "utf-8") as f:
            content = verstkaprofile(f.read(), name, studfirst_name, studlast_name)
            content = content.replace("{{ grade }}", str(grade))
            content = content.replace("{{ tutors_count }}", str(tutor_count))
            content = content.replace("{{ homework_colvo }}", str(homework_colvo))
            content = content.replace("{{ completed_homeworks }}", str(completed_homeworks))
            content = content.replace("{{ avg_grade }}", str(avggrade))
            content = content.replace("{{ bio }}", bio)

        return HTMLResponse(content=content)

    except Exception as e:
        print(f"Ловит ошибку - { e }")
        return RedirectResponse(url="/login", status_code=303)
    

@router.get("/editstudprofile")
def edittutprofile(request: Request):
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

        with open(f'{TEMPLATES_PATH}profiles/editstudprofile.html', 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, studfirst_name, studlast_name)
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    

@router.post("/updatestudbasic")
def updatestudbasic(request: Request, first_name: str = Form(...), last_name: str = Form(...), grade: int = Form(...)):
    try:
        name, user_type = get_current_user(request)

        if user_type != "student":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:

        editstudbasic(first_name, last_name, grade, name)

        return RedirectResponse(url="/profile", status_code=303)
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

@router.post("/updatestudbio")
def updatetutbio(request: Request, bio: str = Form("")):
    try:
        name, user_type = get_current_user(request)

        if user_type != "student":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:

        editstudbio(bio, name)

        return RedirectResponse(url="/profile", status_code=303)
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie(key="access_token")
    return response
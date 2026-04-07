from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from config import TEMPLATES_PATH
from typing import Optional
from auth import create_access_token
from services.auth_stud_service import checkstudreg, studregister, checkstudloginexists
from services.auth_tut_service import checktutreg, tutregister, checktutloginexists
from utils.validation import checkrequiredfields

router = APIRouter()

@router.get("/login")
def get_login():
    with open(f"{TEMPLATES_PATH}auth/login.html", "r", encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)

@router.post("/login")
def login(login: str = Form(None), password: str = Form(None)):
    try:
        form_data = {"login": login,"password": password}
        error_validation = checkrequiredfields(form_data, ["login", "password"],f"{TEMPLATES_PATH}auth/login.html")
        if error_validation:
            return error_validation

        if checkstudreg(login, password):
            access_token = create_access_token(login, "student")
            response = RedirectResponse(url="/home", status_code=303)
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                max_age=60 * 60,
                path="/",
                secure=True,
                samesite="lax", 
            )
            return response
        else:
            with open(f"{TEMPLATES_PATH}auth/loginstudfailed.html", "r", encoding='utf-8') as file:
                content = file.read()
            return HTMLResponse(content=content)
    except Exception as e:
        print(f"Ошибка login: {e}")
        with open(f"{TEMPLATES_PATH}auth/loginstudfailed.html", "r", encoding='utf-8') as file:
            content = file.read()
        return HTMLResponse(content=content)

@router.post("/logintut")
def logintut(login: str = Form(None), password: str = Form(None)):
    try:
        form_data = {"login": login,"password": password}
        error_validation = checkrequiredfields(form_data, ["login", "password"],f"{TEMPLATES_PATH}auth/login.html")
        if error_validation:
            return error_validation

        if checktutreg(login, password):
            access_token = create_access_token(login, "tutor")
            response = RedirectResponse(url=f"/hometut", status_code=303)
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                max_age=60 * 60,
                path="/",
                secure=True,
                samesite="lax", 
            )
            return response
        else:
            with open(f"{TEMPLATES_PATH}auth/loginrepfailed.html", "r", encoding='utf-8') as file:
                content = file.read()
            return HTMLResponse(content=content)
    except Exception as e:
        print(f"Ошибка logintut: {e}")
        with open(f"{TEMPLATES_PATH}auth/loginrepfailed.html", "r", encoding='utf-8') as file:
            content = file.read()
        return HTMLResponse(content=content)

@router.get("/register")
def get_registration():
    with open(f'{TEMPLATES_PATH}register/regstud.html', 'r', encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)

@router.post("/register")
def post_registration(first_name: str = Form(None), last_name: str = Form(None), grade: str = Form(None), login: str = Form(None), password: str = Form(None)):
    try:
        form_data = {"first_name": first_name,"last_name": last_name,"grade": grade,"login": login,"password": password}
        error_validation = checkrequiredfields(form_data, ["first_name", "last_name", "grade", "login", "password"],f"{TEMPLATES_PATH}register/regstud.html")
        if error_validation:
            return error_validation

        if checkstudloginexists(login):
            with open(f'{TEMPLATES_PATH}regstudloginalreadyexists/regstudloginalreadyexists.html', 'r', encoding='utf-8') as file:
                content = file.read()
            return HTMLResponse(content=content)

        else:
            studregister(first_name, last_name, grade, login, password)

            access_token = create_access_token(login, "student")
            response = RedirectResponse(url="/home", status_code=303)
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                max_age=60 * 60,
                path="/",
                secure=True,
                samesite="lax",
            )
        
            return response

    except Exception as e:
        print(f"Ошибка post_registration: {e}")
        return RedirectResponse(url="/login", status_code=303)

@router.get("/registertut")
def get_registertut():
    with open(f'{TEMPLATES_PATH}register/regtut.html', 'r', encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)

@router.post("/registertut")
def post_registertut(
    first_name: str = Form(None), 
    last_name: str = Form(None), 
    education: str = Form(None), 
    experience: int = Form(None), 
    login: str = Form(None), 
    password: str = Form(None),
    subject_math: Optional[str] = Form(None),
    subject_physics: Optional[str] = Form(None),
    subject_chemistry: Optional[str] = Form(None),
    subject_computer: Optional[str] = Form(None),
    subject_russian: Optional[str] = Form(None),
    subject_english: Optional[str] = Form(None),
    subject_german: Optional[str] = Form(None),
    subject_french: Optional[str] = Form(None),
    subject_history: Optional[str] = Form(None),
    subject_social: Optional[str] = Form(None),
    subject_literature: Optional[str] = Form(None),
    subject_biology: Optional[str] = Form(None),
    subject_geography: Optional[str] = Form(None),
    subject_economics: Optional[str] = Form(None),
    subject_art: Optional[str] = Form(None),
    subject_music: Optional[str] = Form(None)
):
    try:
        form_data = {
            "first_name": first_name,
            "last_name": last_name,
            "education": education,
            "experience": experience,
            "login": login,
            "password": password
        }
        
        error_validation = checkrequiredfields(form_data, ["first_name", "last_name", "education", "experience", "login", "password"],f"{TEMPLATES_PATH}register/regtut.html")
        if error_validation:
            return error_validation
        
        if checktutloginexists(login):
            with open(f'{TEMPLATES_PATH}regtutloginalreadyexists/regtutloginalreadyexists.html', 'r', encoding='utf-8') as file:
                content = file.read()
            return HTMLResponse(content=content)
        
        tutregister(
            first_name, last_name, 
            subject_math, subject_physics, subject_chemistry, 
            subject_computer, subject_russian, subject_english, 
            subject_german, subject_french, subject_history, 
            subject_social, subject_literature, subject_biology, 
            subject_geography, subject_economics, subject_art, 
            subject_music, experience, login, password
        )
        access_token = create_access_token(login, "tutor")
        response = RedirectResponse(url="/hometut", status_code=303)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=60 * 60,
            path="/",
            secure=True,
            samesite="lax",
        )
    
        return response

        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from config import TEMPLATES_PATH
from typing import Optional
from auth import create_access_token
from services.auth_stud_service import checkstudreg, studregister
from services.auth_tut_service import checktutreg, tutregister

router = APIRouter()

@router.get("/login")
def get_login():
    with open(f"{TEMPLATES_PATH}auth/login.html", "r", encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)

@router.post("/login")
def login(login: str = Form(...), password: str = Form(...)):
    try:
        if checkstudreg(login, password):
            access_token = create_access_token(login, "student")
            response = RedirectResponse(url="/home", status_code=303)
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                max_age=60 * 60,
                path="/",
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
def logintut(login: str = Form(...), password: str = Form(...)):
    try:
        if checktutreg(login, password):
            access_token = create_access_token(login, "tutor")
            response = RedirectResponse(url=f"/hometut", status_code=303)
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                max_age=60 * 60,
                path="/",
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
def post_registration(first_name: str = Form(), last_name: str = Form(), grade: str = Form(),
                      login: str = Form(...), password: str = Form(...)):
    try:
        studregister(first_name, last_name, grade, login, password)
    except Exception as e:
        print(f"Ошибка post_registration: {e}")
        return RedirectResponse(url="/login", status_code=303)
    return RedirectResponse(url="/login", status_code=303)

@router.get("/registertut")
def get_registertut():
    with open(f'{TEMPLATES_PATH}register/regtut.html', 'r', encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)

@router.post("/registertut")
def post_registertut(first_name: str = Form(...), last_name: str = Form(...), education: str = Form(...), experience: int = Form(...), login: str = Form(...), password: str = Form(...),
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
    subject_music: Optional[str] = Form(None)):

    #Доделать обработку файлов

    try:

        tutregister(first_name, last_name, subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music, experience, login, password)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

    return RedirectResponse(url="/login", status_code=303)

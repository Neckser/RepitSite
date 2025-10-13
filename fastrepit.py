from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from database import init_database
from typing import Optional, List
import sqlite3
import random

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_database()

def create_id():
    return random.randint(1000000, 100000000000000)

def verstka(file, name):
    formatted_content = file.replace("{{ name }}", name)
    return formatted_content

@app.get("/")
def startlog():
    with open("login.html", "r", encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.get("/login")
def get_login():
    with open("login.html", "r", encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.post("/login")
def login(login: str = Form(...), password: str = Form(...)):
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM students WHERE login = ? AND password = ?", (login, password))
        res = cursor.fetchall()
        if res:
            return RedirectResponse(url=f"/home?name={login}", status_code=303)
        else:
            with open("loginstudfailed.html", "r", encoding='utf-8') as file:
                content = file.read()
            return HTMLResponse(content=content)
    finally:
        connection.close()

@app.post("/logintut")
def logintut(login: str = Form(...), password: str = Form(...)):
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM tutors WHERE login = ? AND password = ?", (login, password))
        res = cursor.fetchall()
        if res:
            return RedirectResponse(url=f"/hometut", status_code=303)
        else:
            with open("loginrepfailed.html", "r", encoding='utf-8') as file:
                content = file.read()
            return HTMLResponse(content=content)
    finally:
        connection.close()


@app.get("/register")
def get_registration():
    with open('regstud.html', 'r', encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.post("/register")
def post_registration(first_name: str = Form(), last_name: str = Form(), grade: str = Form(), login: str = Form(...), password: str = Form(...)):
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO students (student_id, first_name, last_name, login, password) VALUES (?, ?, ?, ?, ?)", (create_id(), first_name, last_name, login, password))
        connection.commit()
    except sqlite3.IntegrityError:
        #Доделать страницу когда Логин уже занят
        return "Ошибка: такой логин уже занят"
    finally:
        connection.close()
    return RedirectResponse(url="/login", status_code=303)

@app.get("/registertut")
def get_registertut():
    with open('regtut.html', 'r', encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.post("/registertut")
def post_registertut(first_name: str = Form(...), last_name: str = Form(...), education: str = Form(...), experience: int = Form(...), login: str = Form(...), password: str = Form(...),photo: UploadFile = File(...), resume: Optional[UploadFile] = File(None),
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

    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO tutors (tutor_id, first_name, last_name, subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music, experience, login, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (create_id(), first_name, last_name, subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music, experience, login, password))
        connection.commit()
    except sqlite3.IntegrityError:
        #Доделать страницу когда Логин уже занят
        return "Ошибка: такой логин уже занят"
    finally:
        connection.close()
    return RedirectResponse(url="/login", status_code=303)

@app.get("/home")
def home(name: str = None):
    with open("mainpage.html", "r", encoding = "utf-8") as f:
        content = verstka(f.read(), name)
        return HTMLResponse(content=content)
    

@app.get("/hometut")
def get_registertut():
    with open('hometut.html', 'r', encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)
    
@app.get("/tutlist")
def tutlist(name: str = None):
    with open("tutlist.html",'r', encoding='utf-8') as f:
        content = verstka(f.read(), name)
        return HTMLResponse(content=content)
    
@app.get("/findtut")
def findtut(name: str = None):
    with open("findtut.html", "r", encoding = "utf-8") as f:
        content = verstka(f.read(), name)
        return HTMLResponse(content=content)
    
@app.post("/addtut")
def addtut(tutor_code: str = Form(...), name: str = Form(...)):
    #сделать обработку бд добавления репетитора челиксу
    return RedirectResponse(url=f"/tutlist?name={name}", status_code=303)




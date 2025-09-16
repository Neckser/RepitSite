from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional, List
import sqlite3
import random

app = FastAPI()

def create_id():
    return random.randint(1000000, 100000000000000)

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
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER UNIQUE PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        login TEXT UNIQUE NOT NULL,
        password TEXT UNIQUE,
        registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
    );''')
    connection.commit()
    cursor.execute("SELECT * FROM students WHERE login = ? AND password = ?", (login, password))
    res = cursor.fetchall()
    connection.close()
    if res:
        return RedirectResponse(url=f"/home?name={login}", status_code=303)
    else:
        with open("loginstudfailed.html", "r", encoding='utf-8') as file:
            content = file.read()
        return HTMLResponse(content=content)


@app.post("/logintut")
def login(login: str = Form(...), password: str = Form(...)):
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tutors (
        tutor_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        login TEXT UNIQUE NOT NULL,
        password TEXT UNIQUE NOT NULL,
        specialization TEXT,
        experience INTEGER,
        registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
    );''')
    connection.commit()
    cursor.execute("SELECT * FROM tutors WHERE login = ? AND password = ?", (login, password))
    res = cursor.fetchall()
    connection.close()
    if res:
        return RedirectResponse(url=f"/home?name={login}", status_code=303)
    else:
        with open("loginrepfailed.html", "r", encoding='utf-8') as file:
            content = file.read()
        return HTMLResponse(content=content)

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
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER UNIQUE PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
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
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tutors (
            tutor_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            subject_math TEXT,
            subject_physics TEXT,
            subject_chemistry TEXT,
            subject_computer TEXT,
            subject_russian TEXT,
            subject_english TEXT,
            subject_german TEXT,
            subject_french TEXT,
            subject_history TEXT,
            subject_social TEXT,
            subject_literature TEXT,
            subject_biology TEXT,
            subject_geography TEXT,
            subject_economics TEXT,
            subject_art TEXT,
            subject_music TEXT,
            experience INTEGER,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
        );''')
        cursor.execute("INSERT INTO tutors (tutor_id, first_name, last_name, subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music, experience, login, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       (create_id(), first_name, last_name, subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music, experience, login, password))
        connection.commit()
    except sqlite3.IntegrityError:
        #Доделать страницу когда Логин уже занят
        return "Ошибка: такой логин уже занят"
    finally:
        connection.close()
    return RedirectResponse(url="/login", status_code=303)

@app.get("/home")
def home():
    with open("mainpage.html", "r", encoding = "utf-8") as f:
        content = f.read()
        return HTMLResponse(content=content)


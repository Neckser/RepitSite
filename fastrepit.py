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

def verstkatut(file, name, tutor_cout, tutor_data):
    verstkatemplatetut = ""
    verstkatemplatetut += file
    for i in range(tutor_cout):
        verstkatemplatetut += """
        <div class="tutor-card">
        <div class="tutor-header">
            <div class="tutor-avatar">{{avatar_initials}}</div>
            <div class="tutor-info">
                <h3>{{first_name}} {{last_name}}</h3>
                <span class="tutor-subject">{{specialization}}</span>
            </div>
        </div>
        
        <div class="tutor-stats">
            <div class="stat-item">
                <div class="stat-value"><!-- {{homeworks_count}} --> 1</div>
                <div class="stat-label">заданий</div>
            </div>
            <div class="stat-item">
                <div class="stat-value"><!-- {{rating}} --> 5.0</div>
                <div class="stat-label">рейтинг</div>
            </div>
            <div class="stat-item">
                <div class="stat-value"><!-- {{lessons_count}} --> 1</div>
                <div class="stat-label">уроков</div>
            </div>
        </div>
        
        <div class="tutor-actions">
            <!-- <a href="/tutor/{{tutor_id}}/assignments" class="action-btn assignments-btn">Задания</a> -->
            <a href="/messages/tutor/{{tutor_id}}" class="action-btn message-btn">Написать</a>
        </div>
    </div>
"""
        formatted_content = verstkatemplatetut.replace("{{name}}", name)
        formatted_content = formatted_content.replace("{{tutor_id}}", str(tutor_data[i]['tutor_id']))
        formatted_content = formatted_content.replace("{{first_name}}", tutor_data[i]['first_name'])
        formatted_content = formatted_content.replace("{{last_name}}", tutor_data[i]['last_name'])
        formatted_content = formatted_content.replace("{{experience}}", str(tutor_data[i]['experience']))
        formatted_content = formatted_content.replace("{{specialization}}", tutor_data[i]['specialization'])
        formatted_content = formatted_content.replace("{{avatar_initials}}", tutor_data[i]['first_name'][0] + tutor_data[i]['last_name'][0])
    
    return formatted_content


def verstkaprofile(file, name, first_name, last_name):
    formatted_content = file.replace("{{ name }}", name)
    formatted_content = formatted_content.replace("{{ first_name }}", first_name)
    formatted_content = formatted_content.replace("{{ last_name }}", last_name)
    formatted_content = formatted_content.replace("{{ avatar }}", first_name[0] + last_name[0])
    
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
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT first_name, last_name FROM students WHERE login = ?", (name,))
        res = cursor.fetchone()
        if res:
            first_name = res[0]
            last_name = res[1]
            with open("mainpage.html", "r", encoding = "utf-8") as f:
                content = verstkaprofile(f.read(), name, first_name, last_name)
            return HTMLResponse(content=content)
        else:
            pass
            #Прописать когда нету такого логина
    except Exception as e:
        print(f"Ловит ошибку - { e }")
    

@app.get("/hometut")
def get_registertut():
    with open('hometut.html', 'r', encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)
    
@app.get("/tutlist")
def tutlist(name: str = None):
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    cursor.execute("""
        SELECT 
            tutors.tutor_id, tutors.first_name, tutors.last_name, tutors.experience,
            tutors.subject_math, tutors.subject_physics, tutors.subject_chemistry, tutors.subject_computer,
            tutors.subject_russian, tutors.subject_english, tutors.subject_german, tutors.subject_french,
            tutors.subject_history, tutors.subject_social, tutors.subject_literature, tutors.subject_biology,
            tutors.subject_geography, tutors.subject_economics, tutors.subject_art, tutors.subject_music
        FROM tutors
        INNER JOIN student_tutors ON tutors.tutor_id = student_tutors.tutor_id
        INNER JOIN students ON student_tutors.student_id = students.student_id
        WHERE students.login = ?
    """, (name, ))

    all_tutors = cursor.fetchall()
    tutor_count = len(all_tutors)

    tutors_data = []
    for tutor in all_tutors:
        tutor_id, first_name, last_name, experience = tutor[0:4]
        subjects = tutor[4:]

        subject_names = ["Математика", "Физика", "Химия", "Информатика", "Русский язык", 
                        "Английский язык", "Немецкий язык", "Французский язык", "История",
                        "Обществознание", "Литература", "Биология", "География", "Экономика",
                        "Искусство", "Музыка"]

        first_subject = "Не указано"
        for i, subject in enumerate(subjects):
            if subject is not None:
                first_subject = subject_names[i]
                break
            
        tutors_data.append({
            'tutor_id': tutor_id,
            'first_name': first_name,
            'last_name': last_name,
            'experience': experience,
            'specialization': first_subject
        })

    connection.close()
    with open("tutlistbegin.html", 'r', encoding='utf-8') as f:
        content = verstkatut(f.read(), name, tutor_count, tutors_data)
    with open("tutlistend.html", 'r', encoding='utf-8') as f:
        content += f.read()
        content = content.replace("{{ name }}", name)
    return HTMLResponse(content=content)

@app.get("/findtut")
def findtut(name: str = None):
    with open("findtut.html", "r", encoding = "utf-8") as f:
        content = verstka(f.read(), name)
        return HTMLResponse(content=content)
    
@app.post("/addtut")
def addtut(tutor_code: str = Form(...), name: str = Form(...)):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()
        cursor.execute("SELECT student_id FROM students WHERE login = ?", (name,))
        res = cursor.fetchone()
        if res:
            stud_id = res[0]
            cursor.execute("SELECT tutor_id FROM tutors WHERE tutor_id = ?", (tutor_code,))
            tutor_exists = cursor.fetchone()
            if tutor_exists:
                cursor.execute("INSERT INTO student_tutors (student_id, tutor_id) VALUES (?, ?)", (stud_id, tutor_code))
                connection.commit()
            else:
                with open("findtutidfailed.html", "r", encoding='utf-8') as file:
                    content = verstka(file.read(), name)
                return HTMLResponse(content=content) 
        else:
            with open("findtutstudidfailed.html", "r", encoding='utf-8') as file:
                content = verstka(file.read(), name)
            return HTMLResponse(content=content) 
            
    except Exception as e:
        # Общая ошибка
        with open("findtutidfailed.html", "r", encoding='utf-8') as file:
            content = verstka(file.read(), name)
        return HTMLResponse(content=content) 
            
    finally:
        connection.close()
    
    return RedirectResponse(url=f"/home?name={name}", status_code=303)
    # return RedirectResponse(url=f"/tutlist?name={name}", status_code=303)


@app.get("/profile")
def studprofile(name: str = None):
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT first_name, last_name FROM students WHERE login = ?", (name,))
        res = cursor.fetchone()
        if res:
            first_name = res[0]
            last_name = res[1]
            with open("studprofile.html", "r", encoding = "utf-8") as f:
                content = verstkaprofile(f.read(), name, first_name, last_name)
            return HTMLResponse(content=content)
        else:
            return RedirectResponse(url="/login", status_code=303)
    except Exception as e:
        print(f"Ловит ошибку - { e }")

@app.get("/check_links")
def check_links():
    """Проверить все связи в БД"""
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM student_tutors")
    links = cursor.fetchall()
    
    connection.close()
    
    html = "<h1>Все связи в student_tutors:</h1><ul>"
    for link in links:
        html += f"<li>ID: {link[0]}, student_id: {link[1]}, tutor_id: {link[2]}</li>"
    html += "</ul>"
    
    return HTMLResponse(content=html)




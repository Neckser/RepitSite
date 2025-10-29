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
            return RedirectResponse(url=f"/hometut?name={login}", status_code=303)
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
        cursor.execute("INSERT INTO students (student_id, first_name, last_name, grade, login, password) VALUES (?, ?, ?, ?, ?, ?)", (create_id(), first_name, last_name, grade, login, password))
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
    hwtemplate = ""
    a = '''<div class="assignment-card">
    <div class="assignment-header">
        <!-- <span class="subject-badge math">Математика</span> -->
        <span class="due-date">До {{ data }}</span>
        <span class="status active">{{ status }}</span>
    </div>
    <h3 class="assignment-title">{{ title }}</h3>
    <p class="assignment-description">{{ description }}</p>
    <div class="assignment-footer">
        <span class="tutor-info">{{ tutor_first_name }} {{ tutor_last_name }}</span>
        <!-- <button class="assignment-btn">Перейти к заданию</button> -->                
    </div>
</div>'''




    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT first_name, last_name, student_id FROM students WHERE login = ?", (name,))
        res = cursor.fetchone()
        if res:
            first_name = res[0]
            last_name = res[1]
            student_id = res[2]

        cursor.execute(''' SELECT h.title, h.description, h.deadline, h.status, t.first_name, t.last_name FROM homeworks h JOIN tutors t ON h.tutor_id = t.tutor_id WHERE h.student_id = ? ORDER BY h.deadline ASC''', (student_id,))
        homeworks = cursor.fetchall()
        for hw in homeworks:
            hwtemplate += a
            if hw[3] == "assigned":
                hwtemplate = hwtemplate.replace("{{ status }}", "активно")
            hwtemplate = hwtemplate.replace("{{ status }}", str(hw[3]))
            hwtemplate = hwtemplate.replace("{{ title }}", str(hw[0]))
            hwtemplate = hwtemplate.replace("{{ data }}", str(hw[2]))
            hwtemplate = hwtemplate.replace("{{ description }}", str(hw[1]))
            hwtemplate = hwtemplate.replace("{{ tutor_first_name }}", str(hw[4]))
            hwtemplate = hwtemplate.replace("{{ tutor_last_name }}", str(hw[5]))
            

        with open("mainpage.html", "r", encoding = "utf-8") as f:
            content = verstkaprofile(f.read(), name, first_name, last_name)
        connection.close()
        content = content.replace("{{ hwtemplate }}", hwtemplate)
        return HTMLResponse(content=content)
    except Exception as e:
        print(f"Ловит ошибку - { e }")
    

@app.get("/hometut")
def get_registertut(name: str = None):
    studtemplate = ""
    a = '''<div class="student-card">
                    <div class="student-header">
                        <div class="student-avatar">{{ avatarstud }}</div>
                        <div class="student-info">
                            <h3>{{ first_name }} {{ last_name }}</h3>
                            <span class="student-grade">{{ grade }} класс</span>
                        </div>
                    </div>
                    <div class="student-stats">
                        <div class="student-stat">
                            <div class="student-stat-value">5</div>
                            <div class="student-stat-label">заданий</div>
                        </div>
                        <div class="student-stat">
                            <div class="student-stat-value">12</div>
                            <div class="student-stat-label">уроков</div>
                        </div>
                        <div class="student-stat">
                            <div class="student-stat-value">4.8</div>
                            <div class="student-stat-label">успеваемость</div>
                        </div>
                    </div>
                    <div class="student-actions">
                        <a href="#" class="student-btn assignments-btn">Задания</a>
                        <a href="#" class="student-btn message-btn">Написать</a>
                    </div>
                </div>'''



    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT first_name, last_name FROM tutors WHERE login = ?", (name,))
        res = cursor.fetchone()
        if res:
            first_name = res[0]
            last_name = res[1]
        else:
            return RedirectResponse(url="/login", status_code=303)
        
        cursor.execute('''SELECT COUNT(*) FROM student_tutors st JOIN tutors t ON st.tutor_id = t.tutor_id WHERE t.login = ?''', (name,))
        res = cursor.fetchone()
        if res:
            student_colvo = res[0]

        cursor.execute('''SELECT COUNT(*) FROM homeworks st JOIN tutors t ON st.tutor_id = t.tutor_id WHERE t.login = ?''', (name,))
        res = cursor.fetchone()
        if res:
            homework_colvo = res[0]

        cursor.execute('''SELECT s.student_id, s.first_name,  s.last_name,  s.login, s.registration_date, s.grade FROM students s INNER JOIN student_tutors st ON s.student_id = st.student_id INNER JOIN tutors t ON st.tutor_id = t.tutor_id WHERE t.login = ?''', (name,))
        students = cursor.fetchall()
        for student in students:
            studtemplate += a;
            studtemplate = studtemplate.replace("{{ first_name }}", str(student[1]))
            studtemplate = studtemplate.replace("{{ last_name }}", str(student[2]))
            studtemplate = studtemplate.replace("{{ grade }}", str(student[5]))
            studtemplate = studtemplate.replace("{{ avatarstud }}", str(student[1][0] + student[2][0]))

        with open('hometut.html', 'r', encoding='utf-8') as file:
            content = verstkaprofile(file.read(), name, first_name, last_name)
        content = content.replace("{{ student_colvo }}", str(student_colvo))
        content = content.replace("{{ homework_colvo }}", str(homework_colvo))
        content = content.replace("{{ studtemplate }}", str(studtemplate))
        connection.close()
        return HTMLResponse(content=content)
    except Exception as e: 
        print(f"Случилась ошибка - {e}")
        connection.close()
    
@app.get("/tutlist")
def tutlist(name: str = None):
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()

    tuttemplate = ""

    a = '''<div class="tutor-card">
                <div class="tutor-header">
                    <div class="tutor-avatar">{{ avatar }}</div>
                    <div class="tutor-info">
                        <h3>{{ first_name }} {{ last_name }}</h3>
                        <span class="tutor-subject">Математика</span>
                    </div>
                </div>
                
                <div class="tutor-stats">
                    <div class="stat-item">
                        <div class="stat-value">7</div>
                        <div class="stat-label">уроков</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">5.0</div>
                        <div class="stat-label">рейтинг</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">3</div>
                        <div class="stat-label">ученика</div>
                    </div>
                </div>
                
                <div class="tutor-actions">
                    <a href="#" class="action-btn assignments-btn">
                        Задания
                    </a>
                    <a href="#" class="action-btn message-btn">
                        Сообщения
                    </a>
                </div>
            </div>'''

    cursor.execute("SELECT first_name, last_name FROM students WHERE login = ?", (name,))
    res = cursor.fetchone()
    if res:
        first_name = res[0]
        last_name = res[1]
    else:
        return RedirectResponse(url="/login", status_code=303)
    cursor.execute('''SELECT t.tutor_id, t.first_name, t.last_name, t.experience FROM tutors t INNER JOIN student_tutors st ON t.tutor_id = st.tutor_id INNER JOIN students s ON st.student_id = s.student_id WHERE s.login = ?''', (name,))
    tutors = cursor.fetchall()
    for tutor in tutors:
        tuttemplate += a
        tuttemplate = tuttemplate.replace("{{ first_name }}", tutor[1])
        tuttemplate = tuttemplate.replace("{{ last_name }}", tutor[2])
        tuttemplate = tuttemplate.replace("{{ avatar }}", tutor[1][0] + tutor[2][0])
    with open('tutlist.html', 'r', encoding="utf-8") as f:
        content = verstkaprofile(f.read(), name, first_name, last_name)
    connection.close()
    content = content.replace("{{ tuttemplate }}", tuttemplate)
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
            connection.close()
            return HTMLResponse(content=content) 
            
    except Exception as e:
        # Общая ошибка
        connection.close()
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
        cursor.execute("SELECT first_name, last_name, grade FROM students WHERE login = ?", (name,))
        res = cursor.fetchone()
        if res:
            first_name = res[0]
            last_name = res[1]
            grade = res[2]
        else:
            return RedirectResponse(url="/login", status_code=303)
            
        cursor.execute('''SELECT COUNT(*) FROM homeworks h JOIN students s ON h.student_id = s.student_id WHERE s.login = ?''', (name,))
        res = cursor.fetchone()
        if res:
            homework_colvo = res[0]
        else:
            return RedirectResponse(url="/login", status_code=303)
        cursor.execute('''SELECT COUNT(*) FROM homeworks h JOIN students s ON h.student_id = s.student_id WHERE s.login = ? AND h.status = "completed"''', (name,))
        res = cursor.fetchone()
        if res:
            completed_homeworks = res[0]
        else:
            return RedirectResponse(url="/login", status_code=303)
        cursor.execute('''SELECT COUNT(*) FROM student_tutors st JOIN students s ON st.student_id = s.student_id WHERE s.login = ?''', (name,))
        res = cursor.fetchone()
        if res:
            tutor_count = res[0]
        else:
            return RedirectResponse(url="/login", status_code=303)
        connection.close()
        with open("studprofile.html", "r", encoding = "utf-8") as f:
            content = verstkaprofile(f.read(), name, first_name, last_name)
            content = content.replace("{{ grade }}", str(grade))
            content = content.replace("{{ tutors_count }}", str(tutor_count))
            content = content.replace("{{ homework_colvo }}", str(homework_colvo))
            content = content.replace("{{ completed_homeworks }}", str(completed_homeworks))
        connection.close()
        return HTMLResponse(content=content)

    except Exception as e:
        print(f"Ловит ошибку - { e }")
        connection.close()


@app.get("/studtime")
def studtime(name: str = None):
    with open('studtime.html', 'r', encoding="utf-8") as f:
        content = verstka(f.read(), name)
    return HTMLResponse(content=content)





@app.get("/profiletut")
def profiletut(name : str =  None):
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT first_name, last_name, experience, tutor_id FROM tutors WHERE login = ?", (name,))
        res = cursor.fetchone()
        if res:
            first_name = res[0]
            last_name = res[1]
            experience = res[2]
            tutor_id = res[3]
        else:
            return RedirectResponse(url="/login", status_code=303)
        
        cursor.execute('''SELECT COUNT(*) FROM student_tutors st JOIN tutors t ON st.tutor_id = t.tutor_id WHERE t.login = ?''', (name,))
        res = cursor.fetchone()
        if res:
            student_colvo = res[0]
        with open('profiletut.html', 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, first_name, last_name)
        content = content.replace("{{ experience }}", str(experience))
        content = content.replace("{{ student_colvo }}", str(student_colvo))
        content = content.replace("{{ repcode }}", str(tutor_id))
        connection.close()
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"произошла - {e}")
        connection.close()

@app.get("/homeworkstut")
def homeworkstut(name : str =  None):
    optionTemaplate = '''<select class="form-select" id="student_id" name="student_id" required>
    <option value="">Выберите ученика</option>'''

    hwtemplate = ""
    a = '''<div class="assignment-item">
    <div class="assignment-header">
        <div class="assignment-info">
            <h3>{{ title }}</h3>
            <div class="assignment-meta">
                <span class="assignment-date">Срок: {{ data }}</span>
            </div>
        </div>
        <div class="assignment-status status-active">{{ status }}</div>
    </div>
<div class="assignment-content">
    {{ description }}
</div>
</div>'''
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT first_name, last_name FROM tutors WHERE login = ?", (name,))
        res = cursor.fetchone()
        if res:
            first_name = res[0]
            last_name = res[1]
        else:
            return RedirectResponse(url="/login", status_code=303)
        cursor.execute('''SELECT s.student_id,s.first_name, s.last_name, s.login, s.grade FROM students s JOIN student_tutors st ON s.student_id = st.student_id JOIN tutors t ON st.tutor_id = t.tutor_id WHERE t.login = ? ORDER BY s.first_name, s.last_name''', (name,))
        students = cursor.fetchall()
        for student in students:
            optionTemaplate += f'   <option value="{student[0]}">{student[1]} {student[2]} ({student[4]} класс)</option>'
        optionTemaplate += "</select>"


        cursor.execute("SELECT tutor_id FROM tutors WHERE login = ?", (name,))
        res = cursor.fetchone()
        if res:
            tutor_id = res[0]

        cursor.execute('''SELECT h.title, h.description, h.deadline, h.status FROM homeworks h JOIN tutors t ON h.tutor_id = t.tutor_id WHERE h.tutor_id = ? ORDER BY h.deadline ASC''', (tutor_id,))
        homeworks = cursor.fetchall()
        for hw in homeworks:
            hwtemplate += a
            if hw[3] == "assigned":
                hwtemplate = hwtemplate.replace("{{ status }}", "активно")
            hwtemplate = hwtemplate.replace("{{ status }}", str(hw[3]))
            hwtemplate = hwtemplate.replace("{{ title }}", str(hw[0]))
            hwtemplate = hwtemplate.replace("{{ data }}", str(hw[2]))
            hwtemplate = hwtemplate.replace("{{ description }}", str(hw[1]))
        
        with open('homeworkstut.html', 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, first_name, last_name)
        content = content.replace("{{ selectForm }}", optionTemaplate)
        content = content.replace("{{ hwtemplate }}", hwtemplate)
        return HTMLResponse(content=content)
    except Exception as e:
        print(f"Произошла ошибка - {e}")



@app.post("/createhw")
def createhw(name: str = Form(...), student_id: str = Form(...), subject: str = Form(...), title: str = Form(...), deadline: str = Form(...), description: str = Form(...)):
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT tutor_id FROM tutors WHERE login = ?", (name,))
        res = cursor.fetchone()
        if res:
            tutor_id = res[0]
        cursor.execute('''
            INSERT INTO homeworks (student_id, tutor_id, title, description, deadline, status) VALUES (?, ?, ?, ?, ?, 'assigned')''', (student_id, tutor_id, title, description, deadline))
        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Произошла ошибка - {e}")

    
    return RedirectResponse(url=f"/homeworkstut?name={name}", status_code=303)


@app.post("/deletehw")
def deletehw(name: str = Form(...), title: str = Form(...)):
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()
    try:
        cursor.execute('''DELETE FROM homeworks WHERE title = ?''', (title,))
        connection.commit()
    except Exception as e:
        print(f"Произошла ошибка - {e}")

    print(f"Удалена домашка:  {name} - {title}")
    connection.close()
    return RedirectResponse(url=f"/homeworkstut?name={name}", status_code=303)








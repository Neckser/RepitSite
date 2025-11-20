from fastapi import FastAPI, Form, File, UploadFile, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from database import init_database
from typing import Optional, List
from datetime import datetime
import sqlite3
import random
from auth import get_current_user, create_access_token


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

def gethwstatus(deadline):
    try:
        deadline = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
        now = datetime.now()
        if now > deadline:
            return "Завершено"
        else:
            return "Активно"
            
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return "Активно"
    
def updatehwstatus():
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()
        
        cursor.execute('''UPDATE homeworks SET status = 'Завершено' WHERE deadline < datetime('now') AND status != 'Завершено' ''')
        connection.commit()
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def studregister(studfirst_name, studlast_name, grade, studlogin, password):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO students (student_id, first_name, last_name, grade, login, password) VALUES (?, ?, ?, ?, ?, ?)", (create_id(), studfirst_name, studlast_name, grade, studlogin, password))
        connection.commit()

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def tutregister(tutfirst_name, tutlast_name, subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music, experience, tutlogin, password):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO tutors (tutor_id, first_name, last_name, subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music, experience, login, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (create_id(), tutfirst_name, tutlast_name, subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music, experience, tutlogin, password))
        connection.commit()

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def checkstudreg(login, password):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM students WHERE login = ? AND password = ?", (login, password))
        res = cursor.fetchall()
        if res:
            return True
        else:
            return False
    
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e
    
    finally:
        connection.close()

def checktutreg(login, password):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM tutors WHERE login = ? AND password = ?", (login, password))
        res = cursor.fetchall()
        if res:
            return True
        else:
            return False
    
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e
    
    finally:
        connection.close()


def gettutsubject(tutlogin):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()
    
        cursor.execute('''SELECT subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music FROM tutors WHERE login = ?''', (tutlogin,))
        subjects_row = cursor.fetchone()
    
        if subjects_row:
            subject_names = ["Математика", "Физика", "Химия", "Информатика", "Русский язык", "Английский язык", "Немецкий язык", "Французский язык", "История","Обществознание", "Литература", "Биология", "География", "Экономика","ИЗО", "Музыка"]

            return [subject_names[i] for i, subject in enumerate(subjects_row) if subject is not None]

        return None
    
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e
    
    finally:
        connection.close()

def gettutorinfo(tutlogin):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()

        cursor.execute("SELECT first_name, last_name, tutor_id, experience FROM tutors WHERE login = ?", (tutlogin,))
        res = cursor.fetchone()
        if res:
            first_name = res[0]
            last_name = res[1]
            tutor_id = res[2]
            experience = res[3]
            return [first_name, last_name, tutor_id, experience]
        else:
            return None
        
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e
    
    finally:
        connection.close()

def gettutinfobyid(tutor_id):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()

        cursor.execute("SELECT first_name, last_name, login, experience FROM tutors WHERE tutor_id = ?", (tutor_id,))
        res = cursor.fetchone()
        if res:
            tutfirst_name = res[0]
            tutlast_name = res[1]
            tutlogin = res[2]
            experience = res[3]
            return [tutfirst_name, tutlast_name, tutlogin, experience]
        else:
            return None

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def checktutexistsbyid(tutor_id):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()

        cursor.execute("SELECT tutor_id FROM tutors WHERE tutor_id = ?", (tutor_id,))
        tutor_exists = cursor.fetchone()
        if tutor_exists:
            return True
        else:
            return False

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()
    
def getstudinfo(studlogin):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()

        cursor.execute("SELECT first_name, last_name, student_id, grade FROM students WHERE login = ?", (studlogin,))
        res = cursor.fetchone()
        if res:
            studfirst_name = res[0]
            studlast_name = res[1]
            student_id = res[2]
            grade = res[3]
            return [studfirst_name, studlast_name, student_id, grade]
        else:
            return None
        
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e
    
    finally:
        connection.close()

def getstudinfobyid(student_id):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()

        cursor.execute("SELECT first_name, last_name, login, grade FROM students WHERE student_id = ?", (student_id,))
        res = cursor.fetchone()
        if res:
            studfirst_name = res[0]
            studlast_name = res[1]
            studlogin = res[2]
            grade = res[3]
            return [studfirst_name, studlast_name, studlogin, grade]
        else:
            return None

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

    finally:
        connection.close()

def getstudhwcolvo(studlogin):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()
        cursor.execute('''SELECT COUNT(*) FROM homeworks h JOIN students s ON h.student_id = s.student_id WHERE s.login = ?''', (studlogin,))
        res = cursor.fetchone()
        homework_colvo = res[0]
        return homework_colvo
            
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e

    finally:
        connection.close()

def gettutorcount(studlogin):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()

        cursor.execute('''SELECT COUNT(*) FROM student_tutors st JOIN students s ON st.student_id = s.student_id WHERE s.login = ?''', (studlogin,))
        res = cursor.fetchone()
        tutor_count = res[0]
        return tutor_count
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def getstudhw(student_id):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()

        cursor.execute(''' SELECT h.title, h.description, h.deadline, h.status, t.first_name, t.last_name, h.subject FROM homeworks h JOIN tutors t ON h.tutor_id = t.tutor_id WHERE h.student_id = ? ORDER BY h.deadline ASC''', (student_id,))
        homeworks = cursor.fetchall()
        if homeworks:
            return homeworks
        else:
            return None

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def gettuthw(tutor_id):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()

        cursor.execute('''SELECT h.title, h.description, h.deadline, h.status, h.subject FROM homeworks h JOIN tutors t ON h.tutor_id = t.tutor_id WHERE h.tutor_id = ? ORDER BY h.deadline ASC''', (tutor_id,))
        homeworks = cursor.fetchall()
        return homeworks

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def getstudcompletedhwcolvo(studlogin):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()
        cursor.execute('''SELECT COUNT(*) FROM homeworks h JOIN students s ON h.student_id = s.student_id WHERE s.login = ? AND h.status = "Завершено"''', (studlogin,))
        res = cursor.fetchone()
        completed_homeworks = res[0]
        return completed_homeworks
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()


def gettutlist(studlogin):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()
        cursor.execute('''SELECT t.tutor_id, t.first_name, t.last_name, t.experience, t.login FROM tutors t INNER JOIN student_tutors st ON t.tutor_id = st.tutor_id INNER JOIN students s ON st.student_id = s.student_id WHERE s.login = ?''', (studlogin,))
        tutlist = cursor.fetchall()
        return tutlist
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def addtutor(student_id, tutor_id):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()

        cursor.execute('''SELECT 1 FROM student_tutors WHERE student_id = ? AND tutor_id = ?''', (student_id, tutor_id))
        if cursor.fetchone():
            #Доделать верстку когда такой репетитор уже есть
            pass
        else:
            cursor.execute("INSERT INTO student_tutors (student_id, tutor_id) VALUES (?, ?)", (student_id, tutor_id))
            connection.commit()

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

    finally:
        connection.close()


def getstudcolvo(tutlogin):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()

        cursor.execute('''SELECT COUNT(*) FROM student_tutors st JOIN tutors t ON st.tutor_id = t.tutor_id WHERE t.login = ?''', (tutlogin,))
        res = cursor.fetchone()
        student_colvo = res[0]
        return student_colvo

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()
    
def gettuthwcolvo(tutlogin):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()

        cursor.execute('''SELECT COUNT(*) FROM homeworks st JOIN tutors t ON st.tutor_id = t.tutor_id WHERE t.login = ?''', (tutlogin,))
        res = cursor.fetchone()
        if res:
            tuthomework_colvo = res[0]
            return tuthomework_colvo

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def getstudents(tutlogin):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()
        
        cursor.execute('''SELECT s.student_id, s.first_name,  s.last_name,  s.login, s.registration_date, s.grade FROM students s INNER JOIN student_tutors st ON s.student_id = st.student_id INNER JOIN tutors t ON st.tutor_id = t.tutor_id WHERE t.login = ?''', (tutlogin,))
        students = cursor.fetchall()
        return students

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def addhw(student_id, tutor_id, title, description, subject, deadline):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()

        status = gethwstatus(deadline)
        
        cursor.execute('''INSERT INTO homeworks (student_id, tutor_id, title, description, subject, deadline, status) VALUES (?, ?, ?, ?, ?, ?, ?)''', (student_id, tutor_id, title, description, subject, deadline, status))
        connection.commit()

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def delhw(title):
    try:
        connection = sqlite3.connect('basa.db')
        cursor = connection.cursor()
        
        cursor.execute('''DELETE FROM homeworks WHERE title = ?''', (title,))
        connection.commit()

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

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
    try:
        if checkstudreg(login, password):
            access_token = create_access_token(login, "student")
            response = RedirectResponse(url="/home", status_code=303)
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                max_age=60,
                path="/",
            )
            return response
        else:
            with open("loginstudfailed.html", "r", encoding='utf-8') as file:
                content = file.read()
            return HTMLResponse(content=content)
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        with open("loginstudfailed.html", "r", encoding='utf-8') as file:
            content = file.read()
        return HTMLResponse(content=content)



@app.post("/logintut")
def logintut(login: str = Form(...), password: str = Form(...)):
    try:
        if checktutreg(login, password):
            access_token = create_access_token(login, "tutor")
            response = RedirectResponse(url=f"/hometut", status_code=303)
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                max_age=60,
                path="/",
            )
            return response
        else:
            with open("loginrepfailed.html", "r", encoding='utf-8') as file:
                content = file.read()
            return HTMLResponse(content=content)
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
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
    try:

        studregister(first_name, last_name, grade, login, password)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    
    return RedirectResponse(url="/login", status_code=303)

@app.get("/registertut")
def get_registertut():
    with open('regtut.html', 'r', encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.post("/registertut")
def post_registertut(first_name: str = Form(...), last_name: str = Form(...), education: str = Form(...), experience: int = Form(...), login: str = Form(...), password: str = Form(...),
    photo: UploadFile = File(...), 
    resume: Optional[UploadFile] = File(None),
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

@app.get("/home")
def home(request: Request):
    try:
        name, user_type = get_current_user(request)
        if user_type != "student":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:

        updatehwstatus()

        hwtemplate = ""

        with open('hwcard.html', 'r', encoding='utf-8') as f:
            a = f.read()

        studinfo = getstudinfo(name)
        first_name = studinfo[0]
        last_name = studinfo[1]
        student_id = studinfo[2]

        homeworks = getstudhw(student_id)

        if homeworks:
            for hw in homeworks:
                hwtemplate += a
                if hw[3] == "Активно":
                    hwtemplate = hwtemplate.replace("{{ status_line }}", "<span class='status active'>Активно</span>")
                elif hw[3] == "Завершено":
                    hwtemplate = hwtemplate.replace("{{ status_line }}", "<span class='status completed'>Завершено</span>")
                # hwtemplate = hwtemplate.replace("{{ status }}", str(hw[3]))
                hwtemplate = hwtemplate.replace("{{ title }}", str(hw[0]))
                hwtemplate = hwtemplate.replace("{{ data }}", str(hw[2]))
                hwtemplate = hwtemplate.replace("{{ description }}", str(hw[1]))
                hwtemplate = hwtemplate.replace("{{ tutor_first_name }}", str(hw[4]))
                hwtemplate = hwtemplate.replace("{{ tutor_last_name }}", str(hw[5]))
                hwtemplate = hwtemplate.replace("{{ subject }}", str(hw[6]))
                
        
        else:
            with open('nohw.html', 'r', encoding="utf-8") as f:
                hwtemplate = f.read() 
        with open("mainpage.html", "r", encoding = "utf-8") as f:
            content = verstkaprofile(f.read(), name, first_name, last_name)
        content = content.replace("{{ hwtemplate }}", hwtemplate)
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    

@app.get("/hometut")
def get_registertut(request: Request):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        studtemplate = ""

        with open('studcard.html', 'r', encoding='utf-8') as f:
            a = f.read()

        tutinfo = gettutorinfo(name)
        tutfirst_name = tutinfo[0]
        tutlast_name = tutinfo[1]
        
        student_colvo = getstudcolvo(name)

        tuthomework_colvo = gettuthwcolvo(name)

        students = getstudents(name)

        for student in students:
            studtemplate += a
            studtemplate = studtemplate.replace("{{ first_name }}", str(student[1]))
            studtemplate = studtemplate.replace("{{ last_name }}", str(student[2]))
            studtemplate = studtemplate.replace("{{ grade }}", str(student[5]))
            studtemplate = studtemplate.replace("{{ avatarstud }}", str(student[1][0] + student[2][0]))

        with open('hometut.html', 'r', encoding='utf-8') as file:
            content = verstkaprofile(file.read(), name, tutfirst_name, tutlast_name)
        content = content.replace("{{ student_colvo }}", str(student_colvo))
        content = content.replace("{{ homework_colvo }}", str(tuthomework_colvo))
        content = content.replace("{{ studtemplate }}", str(studtemplate))
        return HTMLResponse(content=content)
    
    except Exception as e: 
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    
@app.get("/tutlist")
def tutlist(request: Request):
    
    try:
        name, user_type = get_current_user(request)
        if user_type != "student":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        tuttemplate = ""

        with open('tutcards.html', 'r', encoding='utf-8') as f:
            a = f.read()

        studinfo = getstudinfo(name)
        studfirst_name = studinfo[0]
        studlast_name = studinfo[1]

        tutorlist = gettutlist(name)

        for tutor in tutorlist:

            tutfirst_name = tutor[1]
            tutlast_name = tutor[2]
            tutlogin = tutor[4]
            student_colvo = getstudcolvo(tutlogin)
            tutsubjects = gettutsubject(tutlogin)

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

        with open('tutlist.html', 'r', encoding="utf-8") as f:
            content = verstkaprofile(f.read(), name, studfirst_name, studlast_name)

        content = content.replace("{{ tuttemplate }}", tuttemplate)

        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

@app.get("/findtut")
def findtut(request: Request):
    try:
        name, user_type = get_current_user(request)
        if user_type != "student":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    with open("findtut.html", "r", encoding = "utf-8") as f:
        content = verstka(f.read(), name)
        return HTMLResponse(content=content)
    
@app.post("/addtut")
def addtut(request: Request, tutor_code: str = Form(...)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "student":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        studinfo = getstudinfo(name)

        if studinfo:
            student_id = studinfo[2]
        else:
            with open("findtutstudidfailed.html", "r", encoding='utf-8') as file:
                content = verstka(file.read(), name)
            return HTMLResponse(content=content) 
        
        if not(checktutexistsbyid(tutor_code)):
            with open("findtutidfailed.html", "r", encoding='utf-8') as file:
                content = verstka(file.read(), name)
            return HTMLResponse(content=content) 

        if checktutexistsbyid(tutor_code):
            addtutor(student_id, tutor_code)
        else:
            with open("findtutidfailed.html", "r", encoding='utf-8') as file:
                content = verstka(file.read(), name)
            return HTMLResponse(content=content)
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)   
    
    return RedirectResponse(url=f"/tutlist", status_code=303)


@app.get("/profile")
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
            
        homework_colvo = getstudhwcolvo(name)

        completed_homeworks = getstudcompletedhwcolvo(name)
        
        tutor_count = gettutorcount(name)

        with open("studprofile.html", "r", encoding = "utf-8") as f:
            content = verstkaprofile(f.read(), name, studfirst_name, studlast_name)
            content = content.replace("{{ grade }}", str(grade))
            content = content.replace("{{ tutors_count }}", str(tutor_count))
            content = content.replace("{{ homework_colvo }}", str(homework_colvo))
            content = content.replace("{{ completed_homeworks }}", str(completed_homeworks))
            content = content.replace("{{ avg_grade }}", '🚧')
            content = content.replace("{{ subject }}", '🚧')
            content = content.replace("{{ subject_percentile }}", '🚧')

        return HTMLResponse(content=content)

    except Exception as e:
        print(f"Ловит ошибку - { e }")
        return RedirectResponse(url="/login", status_code=303)

@app.get("/profiletut")
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
        
        student_colvo = getstudcolvo(name)

        tutsubjects = gettutsubject(name)

        profiletutsubjecttemplate = ""

        for tutsubject in tutsubjects:
                profiletutsubjecttemplate += f'''<span class="subject-badge {tutsubject}">{tutsubject}</span>'''

        with open('profiletut.html', 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, tutfirst_name, tutlast_name)
        content = content.replace("{{ experience }}", str(experience))
        content = content.replace("{{ student_colvo }}", str(student_colvo))
        content = content.replace("{{ repcode }}", str(tutor_id))
        content = content.replace("{{ profiletutsubjecttemplate }}", profiletutsubjecttemplate)
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

@app.get("/homeworkstut")
def homeworkstut(request: Request):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:

        updatehwstatus()

        optionTemaplate = '''<select class="form-select" id="student_id" name="student_id" required>
        <option value="">Выберите ученика</option>'''

        hwtemplate = ""

        with open('hwtutcard.html', 'r', encoding='utf-8') as f:
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
        
        with open('homeworkstut.html', 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, tutfirst_name, tutlast_name)
        content = content.replace("{{ selectForm }}", optionTemaplate)
        content = content.replace("{{ hwtemplate }}", hwtemplate)
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)


@app.post("/createhw")
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


@app.post("/deletehw")
def deletehw(request: Request, title: str = Form(...)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:

        delhw(title)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

    return RedirectResponse(url=f"/homeworkstut", status_code=303)


# @app.get("/studtime")
# def studtime(name: str = None):
#     with open('studtime.html', 'r', encoding="utf-8") as f:
#         content = verstka(f.read(), name)
#     return HTMLResponse(content=content)

# @app.get("/tuttime")
# def studtime(name: str = None):
#     with open('tuttime.html', 'r', encoding="utf-8") as f:
#         content = verstka(f.read(), name)
#     return HTMLResponse(content=content)



@app.exception_handler(404)
def error404(request: Request, exc):
    with open('error.html', 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content, status_code=404)

@app.exception_handler(500)
def error500(request: Request, exc):
    with open('error.html', 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content, status_code=500)


@app.get("/favicon.ico")
def favicon():
    return FileResponse("favicon.ico")

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie(key="access_token")

    return response



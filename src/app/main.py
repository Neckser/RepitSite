from fastapi import FastAPI, Form, File, UploadFile, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from database import init_database
from typing import Optional, List
from datetime import datetime
from auth import get_current_user, create_access_token
from logic import *


app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_database()

@app.get("/")
def startlog():
    with open("templates/auth/login.html", "r", encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.get("/login")
def get_login():
    with open("templates/auth/login.html", "r", encoding='utf-8') as file:
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
                max_age=60 * 5,
                path="/",
            )
            return response
        else:
            with open("templates/auth/loginstudfailed.html", "r", encoding='utf-8') as file:
                content = file.read()
            return HTMLResponse(content=content)
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        with open("templates/auth/loginstudfailed.html", "r", encoding='utf-8') as file:
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
                max_age=60 * 5,
                path="/",
            )
            return response
        else:
            with open("templates/auth/loginrepfailed.html", "r", encoding='utf-8') as file:
                content = file.read()
            return HTMLResponse(content=content)
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        with open("templates/auth/loginrepfailed.html", "r", encoding='utf-8') as file:
            content = file.read()
        return HTMLResponse(content=content)



@app.get("/register")
def get_registration():
    with open('templates/register/regstud.html', 'r', encoding='utf-8') as file:
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
    with open('templates/register/regtut.html', 'r', encoding='utf-8') as file:
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

        with open('templates/cards/hwcard.html', 'r', encoding='utf-8') as f:
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
            with open('templates/cards/nohw.html', 'r', encoding="utf-8") as f:
                hwtemplate = f.read() 
        with open("templates/mainpages/mainpage.html", "r", encoding = "utf-8") as f:
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

        with open('templates/cards/studcard.html', 'r', encoding='utf-8') as f:
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

        with open('templates/mainpages/hometut.html', 'r', encoding='utf-8') as file:
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

        with open('templates/cards/tutcards.html', 'r', encoding='utf-8') as f:
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

        with open('templates/findtut/tutlist.html', 'r', encoding="utf-8") as f:
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
    try:
        studinfo = getstudinfo(name)
        studfirst_name = studinfo[0]
        studlast_name = studinfo[1]

        with open("templates/findtut/findtut.html", "r", encoding = "utf-8") as f:
            content = verstkaprofile(f.read(), name, studfirst_name, studlast_name)
            return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Ловит ошибку - { e }")
        return RedirectResponse(url="/login", status_code=303)

    
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
            with open("templates/findtut/findtutstudidfailed.html", "r", encoding='utf-8') as file:
                content = verstka(file.read(), name)
            return HTMLResponse(content=content) 
        
        if not(checktutexistsbyid(tutor_code)):
            with open("templates/findtut/findtutidfailed.html", "r", encoding='utf-8') as file:
                content = verstka(file.read(), name)
            return HTMLResponse(content=content) 

        if checktutexistsbyid(tutor_code):
            addtutor(student_id, tutor_code)
        else:
            with open("templates/findtut/findtutidfailed.html", "r", encoding='utf-8') as file:
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
        bio = studinfo[4]
            
        homework_colvo = getstudhwcolvo(name)

        completed_homeworks = getstudcompletedhwcolvo(name)
        
        tutor_count = gettutorcount(name)

        if bio is None or bio == "":
            bio = "Всем привет - я использую RepitHub"

        with open("templates/profiles/studprofile.html", "r", encoding = "utf-8") as f:
            content = verstkaprofile(f.read(), name, studfirst_name, studlast_name)
            content = content.replace("{{ grade }}", str(grade))
            content = content.replace("{{ tutors_count }}", str(tutor_count))
            content = content.replace("{{ homework_colvo }}", str(homework_colvo))
            content = content.replace("{{ completed_homeworks }}", str(completed_homeworks))
            content = content.replace("{{ avg_grade }}", '🚧')
            content = content.replace("{{ subject }}", '🚧')
            content = content.replace("{{ subject_percentile }}", '🚧')
            content = content.replace("{{ bio }}", bio)

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
        bio = tutinfo[4]
        
        student_colvo = getstudcolvo(name)

        tutsubjects = gettutsubject(name)

        profiletutsubjecttemplate = ""

        if bio is None or bio == "":
            bio = "Всем привет - я использую RepitHub"

        for tutsubject in tutsubjects:
                profiletutsubjecttemplate += f'''<span class="subject-badge {tutsubject}">{tutsubject}</span>'''

        with open('templates/profiles/profiletut.html', 'r', encoding='utf-8') as f:
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

        with open('templates/cards/hwtutcard.html', 'r', encoding='utf-8') as f:
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
        
        with open('templates/homeworks/homeworkstut.html', 'r', encoding='utf-8') as f:
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
#     with open('templates/studtime.html', 'r', encoding="utf-8") as f:
#         content = verstka(f.read(), name)
#     return HTMLResponse(content=content)

# @app.get("/tuttime")
# def studtime(name: str = None):
#     with open('templates/tuttime.html', 'r', encoding="utf-8") as f:
#         content = verstka(f.read(), name)
#     return HTMLResponse(content=content)

@app.get("/studgrades")
def studgrades(request: Request):
    try:
        name, user_type = get_current_user(request)
        if user_type != "student":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        avg_grade = getavggrade(name)
        colvo_grades = getcolvogrades(name)
        colvo_fives = getcolvofives(name)
        
        grades = getstrgrades(name)

        studinfo = getstudinfo(name)
        studfirst_name = studinfo[0]
        studlast_name = studinfo[1]

        grade_template = ""

        with open('templates/cards/gradestr.html', 'r', encoding='utf-8') as f:
            a = f.read()

        if grades:
            for grade in grades:
                grade_template += a
                grade_template = grade_template.replace("{{ subject }}", str(grade[3]))
                grade_template = grade_template.replace("{{ grade }}", str(grade[4]))
                grade_template = grade_template.replace("{{ date }}", str(grade[5]))
                grade_template = grade_template.replace("{{ description }}", str(grade[6]))
                grade_template = grade_template.replace("{{ comment }}", str(grade[7]))

        with open('templates/grades/studgrades.html', 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, studfirst_name, studlast_name)
        content = content.replace("{{ grade_template }}", grade_template)
        content = content.replace("{{ average_grade }}", str(avg_grade))
        content = content.replace("{{ colvo_grades }}", str(colvo_grades))
        content = content.replace("{{ colvo_fives }}", str(colvo_fives))

        return HTMLResponse(content=content)
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    

@app.get("/tutgrades")
def tutgrades(request: Request):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    optionTemplate = '''<select class="form-select" id="student_id" name="student_id" required>
    <option value="">Выберите ученика</option>'''

    students = getstudents(name)

    if students:
        for student in students:
            optionTemplate += f'   <option value="{student[0]}">{student[1]} {student[2]} ({student[5]} класс)</option>'
    optionTemplate += "</select>"

    try:
        tutorgrades = gettutorgrades(name)

        a = ""
        gradestemplate = ""

        with open ('templates/cards/gradestemplate.html', 'r', encoding='utf-8') as f:
            a = f.read()

        tutinfo = gettutorinfo(name)
        tutfirst_name = tutinfo[0]
        tutlast_name = tutinfo[1]
        

        if tutorgrades:
            for grade in tutorgrades:
                gradestemplate += a
                studinfo = getstudinfobyid(grade[1])
                gradestemplate = gradestemplate.replace("{{ first_name }}", studinfo[0])
                gradestemplate = gradestemplate.replace("{{ last_name }}", studinfo[1])
                gradestemplate = gradestemplate.replace("{{ grade_id }}", str(grade[0]))
                gradestemplate = gradestemplate.replace("{{ grade }}", str(grade[3]))
                gradestemplate = gradestemplate.replace("{{ description }}", grade[5])
                gradestemplate = gradestemplate.replace("{{ date }}", grade[4])
                gradestemplate = gradestemplate.replace("{{ comment }}", grade[6])
                gradestemplate = gradestemplate.replace("{{ subject }}", grade[2])

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url='/login', status_code=303)
        

    with open('templates/grades/tutgrades.html', 'r', encoding='utf-8') as f:
        content = verstkaprofile(f.read(), name, tutfirst_name, tutlast_name)
    content = content.replace("{{ selectForm }}", optionTemplate)
    content = content.replace("{{ gradestemplate }}", gradestemplate)
    return HTMLResponse(content=content)

@app.post('/creategrade')
def creategrade(request: Request, student_id: str = Form(...), subject: str = Form(...), grade: str = Form(...), reason: str = Form(...), comment: str = Form(...)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        tutinfo = gettutorinfo(name)
        tutor_id = tutinfo[2]

        addgrade(student_id, tutor_id, subject, grade, reason, comment)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    
    return RedirectResponse(url=f"/tutgrades", status_code=303)


@app.post("/deletegrade")
def deletehw(request: Request, grade_id: str = Form(...)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:

        delgrade(grade_id)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

    return RedirectResponse(url=f"/tutgrades", status_code=303)

@app.get("/edittutprofile")
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

        with open('templates/profiles/edittutprofile.html', 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, tutfirst_name, tutlast_name)
        return HTMLResponse(content=content)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)


@app.get("/editstudprofile")
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

        with open('templates/profiles/editstudprofile.html', 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, studfirst_name, studlast_name)
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)



@app.exception_handler(404)
def error404(request: Request, exc):
    with open('templates/errors/error.html', 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content, status_code=404)

@app.exception_handler(500)
def error500(request: Request, exc):
    with open('templates/error.html', 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content, status_code=500)


@app.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie(key="access_token")
    return response


@app.post("/updatetutbasic")
def updatetutbasic(request: Request, first_name: str = Form(...), last_name: str = Form(...), experience: int = Form(...)):
    try:
        name, user_type = get_current_user(request)

        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:

        edittutbasic(first_name, last_name, experience, name)

        return RedirectResponse(url="/profiletut", status_code=303)
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

    
@app.post("/updatetutsubjects")
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

        eduttutsubjects(selected_subjects, name)

        return RedirectResponse(url="/profiletut", status_code=303)
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

@app.post("/updatetutbio")
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


@app.post("/updatestudbasic")
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

@app.post("/updatestudbio")
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
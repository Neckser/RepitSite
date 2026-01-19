from fastapi import FastAPI, Form, Query, File, UploadFile, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from database import init_database
from typing import Optional, List
from datetime import datetime
from auth import get_current_user, create_access_token
from logic import *

TEMPLATES_PATH = "../../build/"

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_database()

@app.get("/")
def start():
    with open(f"{TEMPLATES_PATH}landing/mainlanding.html", "r", encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.get("/policy")
def policy():
    with open(f"{TEMPLATES_PATH}landing/policy.html", 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/cookies")
def policy():
    with open(f"{TEMPLATES_PATH}landing/cookies.html", 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/terms")
def terms():
    with open(f"{TEMPLATES_PATH}landing/terms.html", 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/contact")
def terms():
    with open(f"{TEMPLATES_PATH}landing/contact.html", 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/faq")
def terms():
    with open(f"{TEMPLATES_PATH}landing/faq.html", 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/login")
def get_login():
    with open(f"{TEMPLATES_PATH}auth/login.html", "r", encoding='utf-8') as file:
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
                max_age=60 * 60,
                path="/",
            )
            return response
        else:
            with open(f"{TEMPLATES_PATH}auth/loginstudfailed.html", "r", encoding='utf-8') as file:
                content = file.read()
            return HTMLResponse(content=content)
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        with open(f"{TEMPLATES_PATH}auth/loginstudfailed.html", "r", encoding='utf-8') as file:
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
                max_age=60 * 60,
                path="/",
            )
            return response
        else:
            with open(f"{TEMPLATES_PATH}auth/loginrepfailed.html", "r", encoding='utf-8') as file:
                content = file.read()
            return HTMLResponse(content=content)
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        with open(f"{TEMPLATES_PATH}auth/loginrepfailed.html", "r", encoding='utf-8') as file:
            content = file.read()
        return HTMLResponse(content=content)



@app.get("/register")
def get_registration():
    with open(f'{TEMPLATES_PATH}register/regstud.html', 'r', encoding='utf-8') as file:
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
    with open(f'{TEMPLATES_PATH}register/regtut.html', 'r', encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.post("/registertut")
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

        with open(f'{TEMPLATES_PATH}cards/hwcard.html', 'r', encoding='utf-8') as f:
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
            with open(f'{TEMPLATES_PATH}cards/nohw.html', 'r', encoding="utf-8") as f:
                hwtemplate = f.read() 
        with open(f"{TEMPLATES_PATH}mainpages/mainpage.html", "r", encoding = "utf-8") as f:
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

        with open(f'{TEMPLATES_PATH}cards/studcard.html', 'r', encoding='utf-8') as f:
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

        with open(f'{TEMPLATES_PATH}mainpages/hometut.html', 'r', encoding='utf-8') as file:
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

        with open(f'{TEMPLATES_PATH}cards/tutcards.html', 'r', encoding='utf-8') as f:
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

        with open(f'{TEMPLATES_PATH}findtut/tutlist.html', 'r', encoding="utf-8") as f:
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

        with open(f"{TEMPLATES_PATH}findtut/findtut.html", "r", encoding = "utf-8") as f:
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
        student_id = studinfo[2]
        studfirst_name = studinfo[0]
        studlast_name = studinfo[1]

        if checktutexistsbyid(tutor_code):

            addtutor(student_id, tutor_code)

        else:
            with open(f"{TEMPLATES_PATH}findtut/findtutidfailed.html", "r", encoding='utf-8') as file:
                content = verstkaprofile(file.read(), name, studfirst_name, studlast_name)
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

        optionTemaplate = '''<select class="assignment-form__select" id="student_id" name="student_id" required>
        <option value="">Выберите ученика</option>'''

        hwtemplate = ""

        with open(f'{TEMPLATES_PATH}cards/hwtutcard.html', 'r', encoding='utf-8') as f:
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
                hwtemplate = hwtemplate.replace("{{ homework_id }}", str(hw[5]))
        
        with open(f'{TEMPLATES_PATH}homeworks/homeworkstut.html', 'r', encoding='utf-8') as f:
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
def deletehw(request: Request, homework_id: str = Form(...)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:

        delhw(homework_id)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

    return RedirectResponse(url=f"/homeworkstut", status_code=303)


@app.get("/studtime")
def studtime(request: Request, week_offset: int = Query(0)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "student":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        base_monday = get_base_monday()
        target_monday = base_monday + timedelta(days=week_offset * 7)
        week = getstudentweektimetable(name, target_monday)


        studinfo = getstudinfo(name)
        studfirst_name = studinfo[0]
        studlast_name = studinfo[1]

        weekdates = getweekdates(target_monday)
        mon = weekdates[0]
        tue = weekdates[1]
        wed = weekdates[2]
        thu = weekdates[3]
        fri = weekdates[4]
        sat = weekdates[5]
        sun = weekdates[6]

        monday_date = list(week.keys())[0]
        monday_lessons = week[monday_date]["lessons"]
        if monday_lessons == "Нет занятий":
            with open(f'{TEMPLATES_PATH}cards/nolessons.html', 'r', encoding='utf-8') as f:
                monday_template = f.read()
        else:
            with open(f'{TEMPLATES_PATH}cards/lesson.html', 'r', encoding='utf-8') as f:
                a = f.read()
            monday_template = ""
            for lesson in monday_lessons:
                start_time = datetime.strptime(lesson["time"], "%H:%M")
                duration_minutes = lesson.get("duration", 60)
                duration = timedelta(minutes=duration_minutes)
                start_time_str = start_time.strftime("%H:%M")
                end_time_str = (start_time + duration).strftime("%H:%M")
                monday_template += a
                tutinfo = gettutinfobyid(lesson["tutor_id"])
                tutfirst_name = tutinfo[0]
                tutlast_name = tutinfo[1]
                monday_template = monday_template.replace('{{ subject }}', lesson["subject"])
                monday_template = monday_template.replace('{{ tutfirst_name }}', tutfirst_name)
                monday_template = monday_template.replace('{{ tutlast_name }}', tutlast_name)
                monday_template = monday_template.replace('{{ starttime }}', str(start_time_str))
                monday_template = monday_template.replace('{{ endtime }}', str(end_time_str))


        tuesday_date = list(week.keys())[1]
        tuesday_lessons = week[tuesday_date]["lessons"]
        if tuesday_lessons == "Нет занятий":
            with open(f'{TEMPLATES_PATH}cards/nolessons.html', 'r', encoding='utf-8') as f:
                tuesday_template = f.read()
        else:
            with open(f'{TEMPLATES_PATH}cards/lesson.html', 'r', encoding='utf-8') as f:
                a = f.read()
            tuesday_template = ""
            for lesson in tuesday_lessons:
                start_time = datetime.strptime(lesson["time"], "%H:%M")
                duration_minutes = lesson.get("duration", 60)
                duration = timedelta(minutes=duration_minutes)
                start_time_str = start_time.strftime("%H:%M")
                end_time_str = (start_time + duration).strftime("%H:%M")
                tuesday_template += a
                tutinfo = gettutinfobyid(lesson["tutor_id"])
                tutfirst_name = tutinfo[0]
                tutlast_name = tutinfo[1]
                tuesday_template = tuesday_template.replace('{{ subject }}', lesson["subject"])
                # tuesday_template = tuesday_template.replace('{{ status }}', lesson["status"])
                tuesday_template = tuesday_template.replace('{{ tutfirst_name }}', tutfirst_name)
                tuesday_template = tuesday_template.replace('{{ tutlast_name }}', tutlast_name)
                tuesday_template = tuesday_template.replace('{{ starttime }}', str(start_time_str))
                tuesday_template = tuesday_template.replace('{{ endtime }}', str(end_time_str))

        wednesday_date = list(week.keys())[2]
        wednesday_lessons = week[wednesday_date]["lessons"]
        if wednesday_lessons == "Нет занятий":
            with open(f'{TEMPLATES_PATH}cards/nolessons.html', 'r', encoding='utf-8') as f:
                wednesday_template = f.read()
        else:
            with open(f'{TEMPLATES_PATH}cards/lesson.html', 'r', encoding='utf-8') as f:
                a = f.read()
            wednesday_template = ""
            for lesson in wednesday_lessons:
                start_time = datetime.strptime(lesson["time"], "%H:%M")
                duration_minutes = lesson.get("duration", 60)
                duration = timedelta(minutes=duration_minutes)
                start_time_str = start_time.strftime("%H:%M")
                end_time_str = (start_time + duration).strftime("%H:%M")
                wednesday_template += a
                tutinfo = gettutinfobyid(lesson["tutor_id"])
                tutfirst_name = tutinfo[0]
                tutlast_name = tutinfo[1]
                wednesday_template = wednesday_template.replace('{{ tutfirst_name }}', tutfirst_name)
                wednesday_template = wednesday_template.replace('{{ tutlast_name }}', tutlast_name)
                wednesday_template = wednesday_template.replace('{{ subject }}', lesson["subject"])
                # wednesday_template = wednesday_template.replace('{{ status }}', lesson["status"])
                wednesday_template = wednesday_template.replace('{{ starttime }}', str(start_time_str))
                wednesday_template = wednesday_template.replace('{{ endtime }}', str(end_time_str))

        thursday_date = list(week.keys())[3]
        thursday_lessons = week[thursday_date]["lessons"]
        if thursday_lessons == "Нет занятий":
            with open(f'{TEMPLATES_PATH}cards/nolessons.html', 'r', encoding='utf-8') as f:
                thursday_template = f.read()
        else:
            with open(f'{TEMPLATES_PATH}cards/lesson.html', 'r', encoding='utf-8') as f:
                a = f.read()
            thursday_template = ""
            for lesson in thursday_lessons:
                start_time = datetime.strptime(lesson["time"], "%H:%M")
                duration_minutes = lesson.get("duration", 60)
                duration = timedelta(minutes=duration_minutes)
                start_time_str = start_time.strftime("%H:%M")
                end_time_str = (start_time + duration).strftime("%H:%M")
                thursday_template += a
                tutinfo = gettutinfobyid(lesson["tutor_id"])
                tutfirst_name = tutinfo[0]
                tutlast_name = tutinfo[1]
                thursday_template = thursday_template.replace('{{ tutfirst_name }}', tutfirst_name)
                thursday_template = thursday_template.replace('{{ tutlast_name }}', tutlast_name)
                thursday_template = thursday_template.replace('{{ subject }}', lesson["subject"])
                # thursday_template = thursday_template.replace('{{ status }}', lesson["status"])
                thursday_template = thursday_template.replace('{{ starttime }}', str(start_time_str))
                thursday_template = thursday_template.replace('{{ endtime }}', str(end_time_str))
                

        friday_date = list(week.keys())[4]
        friday_lessons = week[friday_date]["lessons"]
        if friday_lessons == "Нет занятий":
            with open(f'{TEMPLATES_PATH}cards/nolessons.html', 'r', encoding='utf-8') as f:
                friday_template = f.read()
        else:
            with open(f'{TEMPLATES_PATH}cards/lesson.html', 'r', encoding='utf-8') as f:
                a = f.read()
            friday_template = ""
            for lesson in friday_lessons:
                start_time = datetime.strptime(lesson["time"], "%H:%M")
                duration_minutes = lesson.get("duration", 60)
                duration = timedelta(minutes=duration_minutes)
                start_time_str = start_time.strftime("%H:%M")
                end_time_str = (start_time + duration).strftime("%H:%M")
                friday_template += a
                tutinfo = gettutinfobyid(lesson["tutor_id"])
                tutfirst_name = tutinfo[0]
                tutlast_name = tutinfo[1]
                friday_template = friday_template.replace('{{ tutfirst_name }}', tutfirst_name)
                friday_template = friday_template.replace('{{ tutlast_name }}', tutlast_name)
                friday_template = friday_template.replace('{{ subject }}', lesson["subject"])
                # friday_template = friday_template.replace('{{ status }}', lesson["status"])
                friday_template = friday_template.replace('{{ starttime }}', str(start_time_str))
                friday_template = friday_template.replace('{{ endtime }}', str(end_time_str))

        saturday_date = list(week.keys())[5]
        saturday_lessons = week[saturday_date]["lessons"]
        if saturday_lessons == "Нет занятий":
            with open(f'{TEMPLATES_PATH}cards/nolessons.html', 'r', encoding='utf-8') as f:
                saturday_template = f.read()
        else:
            with open(f'{TEMPLATES_PATH}cards/lesson.html', 'r', encoding='utf-8') as f:
                a = f.read()
            saturday_template = ""
            for lesson in saturday_lessons:
                start_time = datetime.strptime(lesson["time"], "%H:%M")
                duration_minutes = lesson.get("duration", 60)
                duration = timedelta(minutes=duration_minutes)
                start_time_str = start_time.strftime("%H:%M")
                end_time_str = (start_time + duration).strftime("%H:%M")
                saturday_template += a
                tutinfo = gettutinfobyid(lesson["tutor_id"])
                tutfirst_name = tutinfo[0]
                tutlast_name = tutinfo[1]
                saturday_template = saturday_template.replace('{{ tutfirst_name }}', tutfirst_name)
                saturday_template = saturday_template.replace('{{ tutlast_name }}', tutlast_name)
                saturday_template = saturday_template.replace('{{ subject }}', lesson["subject"])
                # saturday_template = saturday_template.replace('{{ status }}', lesson["status"])
                saturday_template = saturday_template.replace('{{ starttime }}', str(start_time_str))
                saturday_template = saturday_template.replace('{{ endtime }}', str(end_time_str))

        sunday_date = list(week.keys())[6]
        sunday_lessons = week[sunday_date]["lessons"]
        if sunday_lessons == "Нет занятий":
            with open(f'{TEMPLATES_PATH}cards/nolessons.html', 'r', encoding='utf-8') as f:
                sunday_template = f.read()
        else:
            with open(f'{TEMPLATES_PATH}cards/lesson.html', 'r', encoding='utf-8') as f:
                a = f.read()
            sunday_template = ""
            for lesson in sunday_lessons:
                start_time = datetime.strptime(lesson["time"], "%H:%M")
                duration_minutes = lesson.get("duration", 60)
                duration = timedelta(minutes=duration_minutes)
                start_time_str = start_time.strftime("%H:%M")
                end_time_str = (start_time + duration).strftime("%H:%M")
                sunday_template += a
                tutinfo = gettutinfobyid(lesson["tutor_id"])
                tutfirst_name = tutinfo[0]
                tutlast_name = tutinfo[1]
                sunday_template = sunday_template.replace('{{ tutfirst_name }}', tutfirst_name)
                sunday_template = sunday_template.replace('{{ tutlast_name }}', tutlast_name)
                sunday_template = sunday_template.replace('{{ subject }}', lesson["subject"])
                # sunday_template = sunday_template.replace('{{ status }}', lesson["status"])
                sunday_template = sunday_template.replace('{{ starttime }}', str(start_time_str))
                sunday_template = sunday_template.replace('{{ endtime }}', str(end_time_str))

        with open(f'{TEMPLATES_PATH}timetable/studtime.html', 'r', encoding="utf-8") as f:
            content = verstkaprofile(f.read(), name, studfirst_name, studlast_name)
        content = content.replace("{{ mon }}", str(mon))
        content = content.replace("{{ tue }}", str(tue))
        content = content.replace("{{ wed }}", str(wed))
        content = content.replace("{{ thu }}", str(thu))
        content = content.replace("{{ fri }}", str(fri))
        content = content.replace("{{ sat }}", str(sat))
        content = content.replace("{{ sun }}", str(sun))
        content = content.replace("{{ monday_lessons }}", monday_template)
        content = content.replace("{{ tuesday_lessons }}", tuesday_template)
        content = content.replace("{{ wednesday_lessons }}", wednesday_template)
        content = content.replace("{{ thursday_lessons }}", thursday_template)
        content = content.replace("{{ friday_lessons }}", friday_template)
        content = content.replace("{{ saturday_lessons }}", saturday_template)
        content = content.replace("{{ sunday_lessons }}", sunday_template)
        content = content.replace("{{ week_offset }}", str(week_offset))
        content = content.replace("{{ week_offset - 1 }}", str(week_offset - 1))
        content = content.replace("{{ week_offset + 1 }}", str(week_offset + 1))
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

@app.get("/tuttime")
def tuttime(request: Request, week_offset: int = Query(0)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        base_monday = get_base_monday()
        target_monday = base_monday + timedelta(days=week_offset * 7)
        week = gettutorweektimetable(name, target_monday)

        optionTemplate = ""

        students = getstudents(name)

        if students:
            for student in students:
                optionTemplate += f'   <option value="{student[0]}">{student[1]} {student[2]} ({student[5]} класс)</option>'
        optionTemplate += "</select>"


        tutorinfo = gettutorinfo(name)
        tutfirst_name = tutorinfo[0]
        tutlast_name = tutorinfo[1]

        weekdates = getweekdates(target_monday)
        mon = weekdates[0]
        tue = weekdates[1]
        wed = weekdates[2]
        thu = weekdates[3]
        fri = weekdates[4]
        sat = weekdates[5]
        sun = weekdates[6]

        monday_date = list(week.keys())[0]
        monday_lessons = week[monday_date]["lessons"]
        if monday_lessons == "Нет занятий":
            with open(f'{TEMPLATES_PATH}cards/nolessons.html', 'r', encoding='utf-8') as f:
                monday_template = f.read()
        else:
            with open(f'{TEMPLATES_PATH}cards/tutlesson.html', 'r', encoding='utf-8') as f:
                a = f.read()
            monday_template = ""
            for lesson in monday_lessons:
                start_time = datetime.strptime(lesson["time"], "%H:%M")
                duration_minutes = lesson.get("duration", 60)
                duration = timedelta(minutes=duration_minutes)
                start_time_str = start_time.strftime("%H:%M")
                end_time_str = (start_time + duration).strftime("%H:%M")
                monday_template += a
                studinfo = getstudinfobyid(lesson["student_id"])
                studfirst_name = studinfo[0]
                studlast_name = studinfo[1]
                monday_template = monday_template.replace('{{ subject }}', lesson["subject"])
                monday_template = monday_template.replace('{{ schedule_id }}', str(lesson["schedule_id"]))
                monday_template = monday_template.replace('{{ studfirst_name }}', studfirst_name)
                monday_template = monday_template.replace('{{ studlast_name }}', studlast_name)
                monday_template = monday_template.replace('{{ starttime }}', str(start_time_str))
                monday_template = monday_template.replace('{{ endtime }}', str(end_time_str))


        tuesday_date = list(week.keys())[1]
        tuesday_lessons = week[tuesday_date]["lessons"]
        if tuesday_lessons == "Нет занятий":
            with open(f'{TEMPLATES_PATH}cards/nolessons.html', 'r', encoding='utf-8') as f:
                tuesday_template = f.read()
        else:
            with open(f'{TEMPLATES_PATH}cards/tutlesson.html', 'r', encoding='utf-8') as f:
                a = f.read()
            tuesday_template = ""
            for lesson in tuesday_lessons:
                start_time = datetime.strptime(lesson["time"], "%H:%M")
                duration_minutes = lesson.get("duration", 60)
                duration = timedelta(minutes=duration_minutes)
                start_time_str = start_time.strftime("%H:%M")
                end_time_str = (start_time + duration).strftime("%H:%M")
                tuesday_template += a
                studinfo = getstudinfobyid(lesson["student_id"])
                studfirst_name = studinfo[0]
                studlast_name = studinfo[1]
                tuesday_template = tuesday_template.replace('{{ subject }}', lesson["subject"])
                tuesday_template = tuesday_template.replace('{{ schedule_id }}', str(lesson["schedule_id"]))
                # tuesday_template = tuesday_template.replace('{{ status }}', lesson["status"])
                tuesday_template = tuesday_template.replace('{{ studfirst_name }}', studfirst_name)
                tuesday_template = tuesday_template.replace('{{ studlast_name }}', studlast_name)
                tuesday_template = tuesday_template.replace('{{ starttime }}', str(start_time_str))
                tuesday_template = tuesday_template.replace('{{ endtime }}', str(end_time_str))

        wednesday_date = list(week.keys())[2]
        wednesday_lessons = week[wednesday_date]["lessons"]
        if wednesday_lessons == "Нет занятий":
            with open(f'{TEMPLATES_PATH}cards/nolessons.html', 'r', encoding='utf-8') as f:
                wednesday_template = f.read()
        else:
            with open(f'{TEMPLATES_PATH}cards/tutlesson.html', 'r', encoding='utf-8') as f:
                a = f.read()
            wednesday_template = ""
            for lesson in wednesday_lessons:
                start_time = datetime.strptime(lesson["time"], "%H:%M")
                duration_minutes = lesson.get("duration", 60)
                duration = timedelta(minutes=duration_minutes)
                start_time_str = start_time.strftime("%H:%M")
                end_time_str = (start_time + duration).strftime("%H:%M")
                wednesday_template += a
                studinfo = getstudinfobyid(lesson["student_id"])
                studfirst_name = studinfo[0]
                studlast_name = studinfo[1]
                wednesday_template = wednesday_template.replace('{{ studfirst_name }}', studfirst_name)
                wednesday_template = wednesday_template.replace('{{ studlast_name }}', studlast_name)
                wednesday_template = wednesday_template.replace('{{ subject }}', lesson["subject"])
                wednesday_template = wednesday_template.replace('{{ schedule_id }}', str(lesson["schedule_id"]))
                # wednesday_template = wednesday_template.replace('{{ status }}', lesson["status"])
                wednesday_template = wednesday_template.replace('{{ starttime }}', str(start_time_str))
                wednesday_template = wednesday_template.replace('{{ endtime }}', str(end_time_str))

        thursday_date = list(week.keys())[3]
        thursday_lessons = week[thursday_date]["lessons"]
        if thursday_lessons == "Нет занятий":
            with open(f'{TEMPLATES_PATH}cards/nolessons.html', 'r', encoding='utf-8') as f:
                thursday_template = f.read()
        else:
            with open(f'{TEMPLATES_PATH}cards/tutlesson.html', 'r', encoding='utf-8') as f:
                a = f.read()
            thursday_template = ""
            for lesson in thursday_lessons:
                start_time = datetime.strptime(lesson["time"], "%H:%M")
                duration_minutes = lesson.get("duration", 60)
                duration = timedelta(minutes=duration_minutes)
                start_time_str = start_time.strftime("%H:%M")
                end_time_str = (start_time + duration).strftime("%H:%M")
                thursday_template += a
                studinfo = getstudinfobyid(lesson["student_id"])
                studfirst_name = studinfo[0]
                studlast_name = studinfo[1]
                thursday_template = thursday_template.replace('{{ studfirst_name }}', studfirst_name)
                thursday_template = thursday_template.replace('{{ studlast_name }}', studlast_name)
                thursday_template = thursday_template.replace('{{ subject }}', lesson["subject"])
                thursday_template = thursday_template.replace('{{ schedule_id }}', str(lesson["schedule_id"]))
                # thursday_template = thursday_template.replace('{{ status }}', lesson["status"])
                thursday_template = thursday_template.replace('{{ starttime }}', str(start_time_str))
                thursday_template = thursday_template.replace('{{ endtime }}', str(end_time_str))
                

        friday_date = list(week.keys())[4]
        friday_lessons = week[friday_date]["lessons"]
        if friday_lessons == "Нет занятий":
            with open(f'{TEMPLATES_PATH}cards/nolessons.html', 'r', encoding='utf-8') as f:
                friday_template = f.read()
        else:
            with open(f'{TEMPLATES_PATH}cards/tutlesson.html', 'r', encoding='utf-8') as f:
                a = f.read()
            friday_template = ""
            for lesson in friday_lessons:
                start_time = datetime.strptime(lesson["time"], "%H:%M")
                duration_minutes = lesson.get("duration", 60)
                duration = timedelta(minutes=duration_minutes)
                start_time_str = start_time.strftime("%H:%M")
                end_time_str = (start_time + duration).strftime("%H:%M")
                friday_template += a
                studinfo = getstudinfobyid(lesson["student_id"])
                studfirst_name = studinfo[0]
                studlast_name = studinfo[1]
                friday_template = friday_template.replace('{{ studfirst_name }}', studfirst_name)
                friday_template = friday_template.replace('{{ studlast_name }}', studlast_name)
                friday_template = friday_template.replace('{{ subject }}', lesson["subject"])
                friday_template = friday_template.replace('{{ schedule_id }}', str(lesson["schedule_id"]))
                # friday_template = friday_template.replace('{{ status }}', lesson["status"])
                friday_template = friday_template.replace('{{ starttime }}', str(start_time_str))
                friday_template = friday_template.replace('{{ endtime }}', str(end_time_str))

        saturday_date = list(week.keys())[5]
        saturday_lessons = week[saturday_date]["lessons"]
        if saturday_lessons == "Нет занятий":
            with open(f'{TEMPLATES_PATH}cards/nolessons.html', 'r', encoding='utf-8') as f:
                saturday_template = f.read()
        else:
            with open(f'{TEMPLATES_PATH}cards/tutlesson.html', 'r', encoding='utf-8') as f:
                a = f.read()
            saturday_template = ""
            for lesson in saturday_lessons:
                start_time = datetime.strptime(lesson["time"], "%H:%M")
                duration_minutes = lesson.get("duration", 60)
                duration = timedelta(minutes=duration_minutes)
                start_time_str = start_time.strftime("%H:%M")
                end_time_str = (start_time + duration).strftime("%H:%M")
                saturday_template += a
                studinfo = getstudinfobyid(lesson["student_id"])
                studfirst_name = studinfo[0]
                studlast_name = studinfo[1]
                saturday_template = saturday_template.replace('{{ studfirst_name }}', studfirst_name)
                saturday_template = saturday_template.replace('{{ studlast_name }}', studlast_name)
                saturday_template = saturday_template.replace('{{ subject }}', lesson["subject"])
                saturday_template = saturday_template.replace('{{ schedule_id }}', str(lesson["schedule_id"]))
                # saturday_template = saturday_template.replace('{{ status }}', lesson["status"])
                saturday_template = saturday_template.replace('{{ starttime }}', str(start_time_str))
                saturday_template = saturday_template.replace('{{ endtime }}', str(end_time_str))

        sunday_date = list(week.keys())[6]
        sunday_lessons = week[sunday_date]["lessons"]
        if sunday_lessons == "Нет занятий":
            with open(f'{TEMPLATES_PATH}cards/nolessons.html', 'r', encoding='utf-8') as f:
                sunday_template = f.read()
        else:
            with open(f'{TEMPLATES_PATH}cards/tutlesson.html', 'r', encoding='utf-8') as f:
                a = f.read()
            sunday_template = ""
            for lesson in sunday_lessons:
                start_time = datetime.strptime(lesson["time"], "%H:%M")
                duration_minutes = lesson.get("duration", 60)
                duration = timedelta(minutes=duration_minutes)
                start_time_str = start_time.strftime("%H:%M")
                end_time_str = (start_time + duration).strftime("%H:%M")
                sunday_template += a
                studinfo = getstudinfobyid(lesson["student_id"])
                studfirst_name = studinfo[0]
                studlast_name = studinfo[1]
                sunday_template = sunday_template.replace('{{ studfirst_name }}', studfirst_name)
                sunday_template = sunday_template.replace('{{ studlast_name }}', studlast_name)
                sunday_template = sunday_template.replace('{{ subject }}', lesson["subject"])
                sunday_template = sunday_template.replace('{{ schedule_id }}', str(lesson["schedule_id"]))
                # sunday_template = sunday_template.replace('{{ status }}', lesson["status"])
                sunday_template = sunday_template.replace('{{ starttime }}', str(start_time_str))
                sunday_template = sunday_template.replace('{{ endtime }}', str(end_time_str))

        with open(f'{TEMPLATES_PATH}timetable/tuttime.html', 'r', encoding="utf-8") as f:
            content = verstkaprofile(f.read(), name, tutfirst_name, tutlast_name)
        content = content.replace("{{ mon }}", str(mon))
        content = content.replace("{{ tue }}", str(tue))
        content = content.replace("{{ wed }}", str(wed))
        content = content.replace("{{ thu }}", str(thu))
        content = content.replace("{{ fri }}", str(fri))
        content = content.replace("{{ sat }}", str(sat))
        content = content.replace("{{ sun }}", str(sun))
        content = content.replace("{{ selectForm }}", optionTemplate)
        content = content.replace("{{ monday_lessons }}", monday_template)
        content = content.replace("{{ tuesday_lessons }}", tuesday_template)
        content = content.replace("{{ wednesday_lessons }}", wednesday_template)
        content = content.replace("{{ thursday_lessons }}", thursday_template)
        content = content.replace("{{ friday_lessons }}", friday_template)
        content = content.replace("{{ saturday_lessons }}", saturday_template)
        content = content.replace("{{ sunday_lessons }}", sunday_template)
        content = content.replace("{{ week_offset }}", str(week_offset))
        content = content.replace("{{ week_offset - 1 }}", str(week_offset - 1))
        content = content.replace("{{ week_offset + 1 }}", str(week_offset + 1))
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    
@app.post("/createlesson")
def createlesson(request: Request, student_id: str = Form(...), subject: str = Form(...), lesson_date: str = Form(...), lesson_time: str = Form(...), duration: str = Form(...)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        tutinfo = gettutorinfo(name)
        tutor_id = tutinfo[2]

        addlesson(student_id, tutor_id, subject, lesson_date, lesson_time, duration)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    
    return RedirectResponse(url=f"/tuttime", status_code=303)

@app.post("/deletelesson")
def deletelesson(request: Request, lesson_id: str = Form(...)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:

        dellesson(lesson_id)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

    return RedirectResponse(url=f"/tuttime", status_code=303)


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

        with open(f'{TEMPLATES_PATH}cards/gradestr.html', 'r', encoding='utf-8') as f:
            a = f.read()

        if grades:
            for grade in grades:
                grade_template += a
                grade_template = grade_template.replace("{{ subject }}", str(grade[3]))
                grade_template = grade_template.replace("{{ grade }}", str(grade[4]))
                grade_template = grade_template.replace("{{ date }}", str(grade[5]))
                grade_template = grade_template.replace("{{ description }}", str(grade[6]))
                grade_template = grade_template.replace("{{ comment }}", str(grade[7]))

        with open(f'{TEMPLATES_PATH}grades/studgrades.html', 'r', encoding='utf-8') as f:
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

    optionTemplate = '''<select class="grade-form__select" id="student_id" name="student_id" required>
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

        with open (f'{TEMPLATES_PATH}cards/gradestemplate.html', 'r', encoding='utf-8') as f:
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
        

    with open(f'{TEMPLATES_PATH}grades/tutgrades.html', 'r', encoding='utf-8') as f:
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

        with open(f'{TEMPLATES_PATH}profiles/edittutprofile.html', 'r', encoding='utf-8') as f:
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

        with open(f'{TEMPLATES_PATH}profiles/editstudprofile.html', 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, studfirst_name, studlast_name)
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)



@app.exception_handler(404)
def error404(request: Request, exc):
    with open(f'{TEMPLATES_PATH}errors/error.html', 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content, status_code=404)

@app.exception_handler(500)
def error500(request: Request, exc):
    with open(f'{TEMPLATES_PATH}errors/error.html', 'r', encoding='utf-8') as f:
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
    
@app.get("/tuttests")
def tuttests(request: Request):
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
        tutor_id = tutorinfo[2]

        with open(f'{TEMPLATES_PATH}cards/tuttest.html', 'r', encoding='utf-8') as f:
            a = f.read()

        tests_template = ""
        tuttests = gettuttests(tutor_id)

        if tuttests is not None:
            for tuttest in tuttests:
                tests_template += a
                studinfo = getstudinfobyid(tuttest[2])
                studfirst_name = studinfo[0]
                studlast_name = studinfo[1]
                tests_template = tests_template.replace("{{ test_id }}", str(tuttest[0]))
                tests_template = tests_template.replace("{{ title }}", str(tuttest[3]))
                tests_template = tests_template.replace("{{ subject }}", str(tuttest[4]))
                tests_template = tests_template.replace("{{ studfirst_name }}", studfirst_name)
                tests_template = tests_template.replace("{{ studlast_name }}", studlast_name)
                tests_template = tests_template.replace("{{ question_colvo }}", str(getquestioncolvobyid(tuttest[0])))
                tests_template = tests_template.replace("{{ data }}", str(tuttest[7]))
                tests_template = tests_template.replace("{{ date_start }}", str(tuttest[5]))
                tests_template = tests_template.replace("{{ date_end }}", str(tuttest[6]))

        with open(f'{TEMPLATES_PATH}ctests/tuttests.html', 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, tutfirst_name, tutlast_name)
        content = content.replace("{{ tests_template }}", tests_template)
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

    
@app.get("/tutctest")
def tutctest(request: Request):
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

        select_form = ""
        students = getstudents(name)
        for student in students:
            select_form += f'<option value="{student[0]}">{student[1]} {student[2]} ({student[5]} класс)</option>'

        with open(f'{TEMPLATES_PATH}ctests/tutctest.html', 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, tutfirst_name, tutlast_name)
        content = content.replace("{{ select_form }}", select_form)
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)


@app.post("/createtest")
async def create_test(request: Request):
    try:
        name, user_type = get_current_user(request)

        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        tutorinfo = gettutorinfo(name)
        tutor_id = tutorinfo[2]

        form = await request.form()

        createtest(tutor_id, form)

        return RedirectResponse(url="/tuttests", status_code=303)
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    
@app.post("/deletetest")
def deletetest(request: Request, test_id: str = Form(...)):
    try:
        name, user_type = get_current_user(request)

        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        tutorinfo = gettutorinfo(name)
        tutor_id = tutorinfo[2]

        deltest(tutor_id,test_id)

        return RedirectResponse(url="/tuttests", status_code=303)

    except Exception as e:
        print(f"Произола ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    
@app.get("/testutres/{test_id}")
def testutres(request: Request, test_id: int):
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

        testinfo = gettestbyid(test_id)
        title = testinfo[2]
        subject = testinfo[3]
        date_start = testinfo[4]
        date_end = testinfo[5]
        created_at = testinfo[6]
        duration = testinfo[7]

        questions_colvo = getquestioncolvobyid(test_id)

        testresinfo = gettestres(test_id)
        students_done = testresinfo[0]
        avg_score = testresinfo[1]
        avg_time_sec = testresinfo[2]

        studtest_template = ""

        with open(f"{TEMPLATES_PATH}ctests/testutres.html", 'r', encoding="utf-8") as f:
            content = verstkaprofile(f.read(), name, tutfirst_name, tutlast_name)
        content = content.replace("{{ test_id }}", str(test_id))
        content = content.replace("{{ title }}", title)
        content = content.replace("{{ subject }}", subject)
        content = content.replace("{{ date_start }}", str(date_start))
        content = content.replace("{{ date_end }}", str(date_end))
        content = content.replace("{{ duration }}", str(duration))
        content = content.replace("{{ questions_colvo }}", str(questions_colvo))
        content = content.replace("{{ students_done }}", str(students_done))
        content = content.replace("{{ avg_score }}", str(avg_score))
        content = content.replace("{{ avg_time }}", str(avg_time_sec))
        content = content.replace("{{ studtest_template }}", studtest_template)
        return HTMLResponse(content=content)

    except Exception as e:
        print(f"Произола ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    

@app.get("/test/t/{test_id}")
def viewtest(request: Request, test_id: int):
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

        testinfo = gettestbyid(test_id)
        title = testinfo[2]
        subject = testinfo[3]
        duration = testinfo[7]

        questions_template = ""

        with open(f"{TEMPLATES_PATH}cards/textquestion.html", 'r', encoding="utf-8") as f:
            textquestion = f.read()

        with open(f"{TEMPLATES_PATH}cards/singlequestion.html", 'r', encoding="utf-8") as f:
            singlequestion = f.read()

        with open(f"{TEMPLATES_PATH}cards/multiquestion.html", 'r', encoding="utf-8") as f:
            multiquestion = f.read()

        questions = gettestquestionsbyid(test_id)

        index = 1
        for question in questions:
            question_id = question[0]
            type = question[1]
            title = question[2]
            data_str = question[3]
            data = json.loads(data_str)
            if type == "text":
                questions_template += textquestion
                questions_template = questions_template.replace("{{ question_id }}", str(question_id))
                questions_template = questions_template.replace("{{ question_number }}", str(index))
                questions_template = questions_template.replace("{{ title_question }}", title)
            elif type == "single_choice":
                questions_template += singlequestion
                options = data.get("options", ["", "", "", ""])
                questions_template = questions_template.replace("{{ question_id }}", str(question_id))
                questions_template = questions_template.replace("{{ question_number }}", str(index))
                questions_template = questions_template.replace("{{ title_question }}", title)
                questions_template = questions_template.replace("{{ first_var }}", options[0])
                questions_template = questions_template.replace("{{ second_var }}", options[1])
                questions_template = questions_template.replace("{{ third_var }}", options[2])
                questions_template = questions_template.replace("{{ fourth_var }}", options[3])
            elif type == "multi_choice":
                questions_template += multiquestion
                options = data.get("options", ["", "", "", ""])
                questions_template = questions_template.replace("{{ question_id }}", str(question_id))
                questions_template = questions_template.replace("{{ question_number }}", str(index))
                questions_template = questions_template.replace("{{ title_question }}", title)
                questions_template = questions_template.replace("{{ first_var }}", options[0])
                questions_template = questions_template.replace("{{ second_var }}", options[1])
                questions_template = questions_template.replace("{{ third_var }}", options[2])
                questions_template = questions_template.replace("{{ fourth_var }}", options[3])
            index += 1

    
        with open(f"{TEMPLATES_PATH}ctests/viewtest.html", "r", encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, tutfirst_name, tutlast_name)
        content = content.replace("{{ questions_template }}", questions_template)
        content = content.replace("{{ title }}", title)
        content = content.replace("{{ subject }}", subject)
        content = content.replace("{{ test_id }}", str(test_id))
        content = content.replace("{{ duration }}", str(duration))
        return HTMLResponse(content=content)
    

    except Exception as e:
        print(f"Произола ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    

    
@app.get("/restest")
def restest(request: Request):
    try:
        name, user_type = get_current_user(request)

        if user_type != "tutor" and user_type != "student":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)
    
    try:

        with open(f'{TEMPLATES_PATH}ctests/restest.html', 'r', encoding='utf-8') as f:
            content = f.read()
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url='/login', status_code=303)
    
@app.post("/tutanswertest")
async def tutanswertest(request: Request, test_id: int = Form(...)):
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
        tutor_id = tutorinfo[2]

        form = await request.form()

        testinfo = gettestbyid(test_id)
        title = testinfo[2]
        subject = testinfo[3]

        answersandtime = gettestanswersandtime(form)
        answers = answersandtime[0]
        time = answersandtime[1]
        score = checktestanswers(answers, test_id)
        questions_colvo = getquestioncolvobyid(test_id)
        percent_score = round((score / questions_colvo) * 100, 2)


        with open(f"{TEMPLATES_PATH}ctests/restest.html", 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace("'{{ score }}'", str(score))
        content = content.replace("'{{ questions_colvo }}'", str(questions_colvo))
        content = content.replace("'{{ percent_score }}'", str(percent_score))
        content = content.replace("{{ time }}", str(time))
        content = content.replace("{{ title }}", str(title))
        content = content.replace("{{ subject }}", subject)
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    

@app.get("/studtests")
def studtests(request: Request):
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

        with open(f"{TEMPLATES_PATH}ctests/studtests.html", 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name , studfirst_name, studlast_name)
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
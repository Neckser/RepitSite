from fastapi import APIRouter, Form, Query, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from config import TEMPLATES_PATH
from datetime import datetime, timedelta
from auth import get_current_user
from utils.dates import get_base_monday, getweekdates
from utils.templates import verstkaprofile
from services.stats_tut_service import getstudents, gettutorinfo, gettutorweektimetable
from services.stats_stud_service import getstudinfobyid
from services.timetable_service import addlesson, dellesson

router = APIRouter()


@router.get("/tuttime")
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
    


@router.post("/createlesson")
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

@router.post("/deletelesson")
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
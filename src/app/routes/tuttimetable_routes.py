from fastapi import APIRouter, Form, Query, HTTPException, Request, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional
from config import TEMPLATES_PATH, UPLOAD_DIR
import os
import asyncio
import html
from utils.id import generate_uuid
from datetime import datetime, timedelta
from auth import get_current_user
from utils.dates import get_base_monday, getweekdates
from utils.templates import verstkaprofile
from services.stats_tut_service import getstudents, gettutorinfo, gettutorweektimetable
from services.stats_stud_service import getstudinfobyid
from services.timetable_service import addlesson, dellesson, addtexttask, getlessontasks, addvideolink, getvideolink, getdesklink, adddesklink, addimagetask

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

        with open(f'{TEMPLATES_PATH}cards/nolessons.html', 'r', encoding='utf-8') as f:
            day_no_lessons_template = f.read()

        with open(f'{TEMPLATES_PATH}cards/tutlesson.html', 'r', encoding='utf-8') as f:
            day_lesson_template = f.read()

        with open(f'{TEMPLATES_PATH}cards/lessontask.html', 'r', encoding='utf-8') as f:
            task_template = f.read()

        with open(f'{TEMPLATES_PATH}cards/lessontaskimage.html', 'r', encoding='utf-8') as f:
            imagetask_template = f.read()

        for i in range(0,7):

            day_template = ""
            day = list(week.keys())[i]
            day_lessons = week[day]["lessons"]

            if day_lessons == "Нет занятий":
                day_template = day_no_lessons_template
            else:
                for lesson in day_lessons:

                    lesson_id = lesson["schedule_id"]
                    lesson_tasks = getlessontasks(lesson_id)
                    lesson_tasks_template =""
                    task_number = 1
                    for task in lesson_tasks:
                        task_type = task[2]
                        content = task[3]
                        if task_type == "text":
                            lesson_tasks_template += task_template
                            lesson_tasks_template = lesson_tasks_template.replace("{{ number }}", html.escape(str(task_number)))
                            lesson_tasks_template = lesson_tasks_template.replace("{{ content }}", html.escape(str(content)))
                            task_number += 1
                        elif task_type == "image":
                            lesson_tasks_template += imagetask_template
                            lesson_tasks_template = lesson_tasks_template.replace("{{ number }}", html.escape(str(task_number)))
                            lesson_tasks_template = lesson_tasks_template.replace("{{ content }}", html.escape(str(content)))
                            task_number += 1


                    start_time = datetime.combine(datetime.today(), lesson["time"])
                    duration_minutes = lesson.get("duration", 60)
                    duration = timedelta(minutes=duration_minutes)
                    start_time_str = start_time.strftime("%H:%M")
                    end_time_str = (start_time + duration).strftime("%H:%M")


                    day_template += day_lesson_template
                    studinfo = getstudinfobyid(lesson["student_id"])
                    studfirst_name = studinfo[0]
                    studlast_name = studinfo[1]

                    video_link = getvideolink(lesson_id)
                    desk_link = getdesklink(lesson_id)

                    day_template = day_template.replace('{{ subject }}', html.escape(lesson["subject"]))
                    day_template = day_template.replace('{{ schedule_id }}', html.escape(str(lesson["schedule_id"])))
                    day_template = day_template.replace('{{ studfirst_name }}', html.escape(studfirst_name))
                    day_template = day_template.replace('{{ studlast_name }}', html.escape(studlast_name))
                    day_template = day_template.replace('{{ starttime }}', html.escape(str(start_time_str)))
                    day_template = day_template.replace('{{ endtime }}', html.escape(str(end_time_str)))
                    day_template = day_template.replace('{{ video_link }}', html.escape(str(video_link)))
                    day_template = day_template.replace('{{ desk_link }}', html.escape(str(desk_link)))
                    day_template = day_template.replace('{{ tasks_template }}', str(lesson_tasks_template))
                    
                
            if i == 0:
                monday_template = day_template
            elif i == 1:
                tuesday_template = day_template
            elif i == 2:
                wednesday_template = day_template
            elif i == 3:
                thursday_template = day_template
            elif i == 4:
                friday_template = day_template
            elif i == 5:
                saturday_template = day_template
            elif i == 6:
                sunday_template = day_template

        with open(f'{TEMPLATES_PATH}timetable/tuttime.html', 'r', encoding="utf-8") as f:
            content = verstkaprofile(f.read(), name, tutfirst_name, tutlast_name)
        content = content.replace("{{ mon }}", html.escape(str(mon)))
        content = content.replace("{{ tue }}", html.escape(str(tue)))
        content = content.replace("{{ wed }}", html.escape(str(wed)))
        content = content.replace("{{ thu }}", html.escape(str(thu)))
        content = content.replace("{{ fri }}", html.escape(str(fri)))
        content = content.replace("{{ sat }}", html.escape(str(sat)))
        content = content.replace("{{ sun }}", html.escape(str(sun)))
        content = content.replace("{{ selectForm }}", optionTemplate)
        content = content.replace("{{ monday_lessons }}", monday_template)
        content = content.replace("{{ tuesday_lessons }}", tuesday_template)
        content = content.replace("{{ wednesday_lessons }}", wednesday_template)
        content = content.replace("{{ thursday_lessons }}", thursday_template)
        content = content.replace("{{ friday_lessons }}", friday_template)
        content = content.replace("{{ saturday_lessons }}", saturday_template)
        content = content.replace("{{ sunday_lessons }}", sunday_template)
        content = content.replace("{{ week_offset }}", html.escape(str(week_offset)))
        content = content.replace("{{ week_offset - 1 }}", html.escape(str(week_offset - 1)))
        content = content.replace("{{ week_offset + 1 }}", html.escape(str(week_offset + 1)))
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

@router.post("/add_lesson_task/{lesson_id}")
async def addtask(request: Request, lesson_id: int, task_type: str = Form(...), task_text: str = Form(None), task_file: UploadFile = File(None)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)
    
    try:

        if task_type == "text":
            addtexttask(lesson_id, task_type, task_text)

        elif task_type == "image":
            upload_dir = os.path.join(UPLOAD_DIR, "tasks")
            os.makedirs(upload_dir, exist_ok=True)
            file_extension = os.path.splitext(task_file.filename)[1].lower()

            new_uuid = str(generate_uuid())
            unique_filename = f"{new_uuid}{file_extension}"
            save_path = os.path.join(upload_dir, unique_filename)
            content = await task_file.read()
            with open(save_path, "wb") as f:
                f.write(content)
            
            addimagetask(lesson_id, "image",unique_filename)
                

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

    return RedirectResponse(url=f"/tuttime", status_code=303)

@router.post("/savevideolink/{lesson_id}")
def savevideolink(request: Request, lesson_id: int, video_link: Optional[str] = Form(None)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        if video_link is not None:
            link_to_save = video_link
        else:
            link_to_save = ""
        addvideolink(lesson_id, link_to_save)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    
    return RedirectResponse(url=f"/tuttime", status_code=303)

@router.post("/savedesklink/{lesson_id}")
def savevideolink(request: Request, lesson_id: int, desk_link: Optional[str] = Form(None)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        if desk_link is not None:
            link_to_save = desk_link
        else:
            link_to_save = ""
        adddesklink(lesson_id, link_to_save)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    
    return RedirectResponse(url=f"/tuttime", status_code=303)
from fastapi import APIRouter, HTTPException, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime, timedelta
from config import TEMPLATES_PATH
from auth import get_current_user
from utils.dates import get_base_monday, getweekdates
from utils.templates import verstkaprofile
from services.stats_stud_service import getstudinfo, getstudentweektimetable
from services.stats_tut_service import gettutinfobyid
from services.timetable_service import getlessontasks, getvideolink, getdesklink, adddesklink

router = APIRouter()


@router.get("/studtime")
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

        with open(f'{TEMPLATES_PATH}cards/nolessons.html', 'r', encoding='utf-8') as f:
            day_no_lessons_template = f.read()

        with open(f'{TEMPLATES_PATH}cards/lesson.html', 'r', encoding='utf-8') as f:
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
                            lesson_tasks_template = lesson_tasks_template.replace("{{ number }}", str(task_number))
                            lesson_tasks_template = lesson_tasks_template.replace("{{ content }}", str(content))
                            task_number += 1
                        elif task_type == "image":
                            lesson_tasks_template += imagetask_template
                            lesson_tasks_template = lesson_tasks_template.replace("{{ number }}", str(task_number))
                            lesson_tasks_template = lesson_tasks_template.replace("{{ content }}", str(content))
                            task_number += 1

                    start_time = datetime.combine(datetime.today(), lesson["time"])
                    duration_minutes = lesson.get("duration", 60)
                    duration = timedelta(minutes=duration_minutes)
                    start_time_str = start_time.strftime("%H:%M")
                    end_time_str = (start_time + duration).strftime("%H:%M")

                    day_template += day_lesson_template

                    tutinfo = gettutinfobyid(lesson["tutor_id"])
                    tutfirst_name = tutinfo[0]
                    tutlast_name = tutinfo[1]
                    
                    video_link = getvideolink(lesson_id)
                    desk_link = getdesklink(lesson_id)

                    day_template = day_template.replace('{{ subject }}', lesson["subject"])
                    day_template = day_template.replace('{{ tutfirst_name }}', tutfirst_name)
                    day_template = day_template.replace('{{ tutlast_name }}', tutlast_name)
                    day_template = day_template.replace('{{ starttime }}', str(start_time_str))
                    day_template = day_template.replace('{{ endtime }}', str(end_time_str))
                    day_template = day_template.replace('{{ tasks_template }}', str(lesson_tasks_template))
                    day_template = day_template.replace('{{ video_link }}', str(video_link))
                    day_template = day_template.replace('{{ desk_link }}', str(desk_link))
                    day_template = day_template.replace('{{ schedule_id }}', str(lesson_id))

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
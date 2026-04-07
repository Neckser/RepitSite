from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from config import TEMPLATES_PATH
from auth import get_current_user
from auth import get_current_user
from utils.templates import verstkaprofile
from services.stats_stud_service import getstudinfo
from services.stats_stud_service import getavggrade, getcolvogrades, getcolvofives, getstrgrades
import html

router = APIRouter()


@router.get("/studgrades")
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
                grade_template = grade_template.replace("{{ subject }}", html.escape(str(grade[3])))
                grade_template = grade_template.replace("{{ grade }}", html.escape(str(grade[4])))
                grade_template = grade_template.replace("{{ date }}", html.escape(str(grade[5])))
                grade_template = grade_template.replace("{{ description }}", html.escape(str(grade[6])))
                grade_template = grade_template.replace("{{ comment }}", html.escape(str(grade[7])))

        with open(f'{TEMPLATES_PATH}grades/studgrades.html', 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, studfirst_name, studlast_name)
        content = content.replace("{{ grade_template }}", grade_template)
        content = content.replace("{{ average_grade }}", html.escape(str(avg_grade)))
        content = content.replace("{{ colvo_grades }}", html.escape(str(colvo_grades)))
        content = content.replace("{{ colvo_fives }}", html.escape(str(colvo_fives)))

        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
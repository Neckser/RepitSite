from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from config import TEMPLATES_PATH
from auth import get_current_user
from utils.templates import verstkaprofile
from utils.validation import checkrequiredfields
from services.stats_tut_service import gettutorinfo, gettutorgrades, getstudents
from services.stats_stud_service import getstudinfobyid
from services.grade_service import addgrade, delgrade

router = APIRouter()


@router.get("/tutgrades")
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
                gradestemplate = gradestemplate.replace("{{ date }}", str(grade[4]))
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

@router.post('/creategrade')
def creategrade(request: Request, student_id: str = Form(None), subject: str = Form(None), grade: str = Form(None), reason: str = Form(None), comment: str = Form(None)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        form_data = {"student_id": student_id,"subject": subject,"grade": grade,"reason": reason,"comment": comment}
        error_validation = checkrequiredfields(form_data, ["student_id", "subject", "grade", "reason", "comment"],f'{TEMPLATES_PATH}grades/tutgrades.html')
        if error_validation:
            return RedirectResponse(url=f"/tutgrades", status_code=303)
        
        tutinfo = gettutorinfo(name)
        tutor_id = tutinfo[2]

        addgrade(student_id, tutor_id, subject, grade, reason, comment)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    
    return RedirectResponse(url=f"/tutgrades", status_code=303)


@router.post("/deletegrade")
def deletehw(request: Request, grade_id: str = Form(None)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        form_data = {"grade_id": grade_id}
        error_validation = checkrequiredfields(form_data, ["grade_id"],f'{TEMPLATES_PATH}grades/tutgrades.html')
        if error_validation:
            return RedirectResponse(url=f"/tutgrades", status_code=303)
        
        delgrade(grade_id)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

    return RedirectResponse(url=f"/tutgrades", status_code=303)
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from config import TEMPLATES_PATH
from auth import get_current_user
from utils.templates import verstkaprofile
from utils.validation import checkrequiredfields
from services.stats_tut_service import gettutorinfo, getstudents, gettuthw
from services.stats_stud_service import gethwtasks
from services.hw_service import updatehwstatus, addhw, delhw
import html

router = APIRouter()

@router.get("/homeworkstut")
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
        
        with open(f"{TEMPLATES_PATH}cards/hwtuttexttask.html", 'r', encoding='utf-8') as f:
            texttask_template = f.read()

        with open(f"{TEMPLATES_PATH}cards/hwimagetuttask.html", 'r', encoding='utf-8') as f:
            imagetask_template = f.read()

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
                task_title = hw[0]
                task_description = hw[1]
                task_deadline = hw[2]
                task_status = hw[3]
                task_subject = hw[4]
                homework_id = hw[5]

                full_task_template = ""
                task_number = 0

                hwtemplate += a

                tasks = gethwtasks(homework_id)

                if tasks:
                    for task in tasks:
                        task_id = task[0]
                        task_homework_id = task[1]
                        type_of_task = task[2]
                        content_of_task = task[3]
                        status_of_task = task[4]
                        task_number += 1
                        
                        if type_of_task == "text":

                            full_task_template += texttask_template
                            full_task_template = full_task_template.replace("{{ task_number }}", str(task_number))
                            full_task_template = full_task_template.replace("{{ task_content }}", html.escape(str(content_of_task)))
                            # full_task_template = full_task_template.replace("{{ task_id }}", str(task_id))
                            # full_task_template = full_task_template.replace("{{ homework_id }}", str(task_homework_id))

                        elif type_of_task == "image":
                            full_task_template += imagetask_template
                            full_task_template = full_task_template.replace("{{ task_number }}", str(task_number))
                            full_task_template = full_task_template.replace("{{ task_content }}", html.escape(str(content_of_task)))



                hwtemplate = hwtemplate.replace("{{ status }}", html.escape(str(task_status)))
                hwtemplate = hwtemplate.replace("{{ title }}", html.escape(str(task_title)))
                hwtemplate = hwtemplate.replace("{{ data }}", html.escape(str(task_deadline)))
                hwtemplate = hwtemplate.replace("{{ description }}", html.escape(str(task_description)))
                hwtemplate = hwtemplate.replace("{{ subject }}", html.escape(str(task_subject)))
                hwtemplate = hwtemplate.replace("{{ homework_id }}", html.escape(str(homework_id)))
                hwtemplate = hwtemplate.replace("{{ tasks_template }}", str(full_task_template))
        
        with open(f'{TEMPLATES_PATH}homeworks/homeworkstut.html', 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, tutfirst_name, tutlast_name)
        content = content.replace("{{ selectForm }}", optionTemaplate)
        content = content.replace("{{ hwtemplate }}", hwtemplate)
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)


@router.post("/createhw")
def createhw(request: Request, student_id: str = Form(None), subject: str = Form(None), title: str = Form(None), deadline: str = Form(None), description: str = Form(None)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)

    try:
        form_data = {"student_id": student_id,"subject": subject,"title": title,"deadline": deadline,"description": description}
        error_validation = checkrequiredfields(form_data, ["student_id", "subject", "title", "deadline", "description"],f'{TEMPLATES_PATH}homeworks/homeworkstut.html')
        if error_validation:
            return RedirectResponse(url=f"/homeworkstut", status_code=303)

        tutinfo = gettutorinfo(name)
        tutor_id = tutinfo[2]

        addhw(student_id, tutor_id, title, description, subject, deadline)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    
    return RedirectResponse(url=f"/homeworkstut", status_code=303)


@router.post("/deletehw")
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
from fastapi import APIRouter, HTTPException, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from config import TEMPLATES_PATH, UPLOAD_DIR
from auth import get_current_user
from utils.id import generate_uuid
from utils.templates import verstkaprofile
from services.stats_stud_service import getstudinfo, getstudhw, gethwtasks
from services.stats_tut_service import getstudcolvo, gettuthwcolvo, getstudents, gettutorinfo, gettodaylessonscolvo
from services.hw_service import updatehwstatus, marktask, addhwtexttask, addhwimagetask
from services.chat_service import getchatid
import html
import os


router = APIRouter()

@router.get("/home")
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

        with open(f"{TEMPLATES_PATH}cards/hwtextstudtask.html", 'r', encoding='utf-8') as f:
            texttask_template = f.read()

        with open(f"{TEMPLATES_PATH}cards/hwimagestudtask.html", 'r', encoding='utf-8') as f:
            imagetask_template = f.read()

        studinfo = getstudinfo(name)
        first_name = studinfo[0]
        last_name = studinfo[1]
        student_id = studinfo[2]

        homeworks = getstudhw(student_id)

        if homeworks:
            for hw in homeworks:
                full_task_template = ""
                task_number = 0
                homework_id = hw[7]
                hwtemplate += a

                tasks = gethwtasks(homework_id)

                if tasks:
                    for task in tasks:
                        task_id = task[0]
                        homework_id = task[1]
                        type_of_task = task[2]
                        content_of_task = task[3]
                        status_of_task = task[4]
                        task_number += 1
                        
                        if type_of_task == "text":

                            full_task_template += texttask_template
                            if status_of_task == "pending":
                                full_task_template = full_task_template.replace("{{ task_mark_button }}", "Сделано")
                                full_task_template = full_task_template.replace("{{ task_status_text }}", "Не выполнено")
                                full_task_template = full_task_template.replace("{{ task_status_class }}", "pending")
                                full_task_template = full_task_template.replace("{{ button_class }}", "complete-task-btn")
                                full_task_template = full_task_template.replace("{{ button_icon }}", "✓")

                            else:
                                full_task_template = full_task_template.replace("{{ task_mark_button }}", "Отменить")
                                full_task_template = full_task_template.replace("{{ task_status_text }}", "Выполнено")
                                full_task_template = full_task_template.replace("{{ task_status_class }}", "completed")
                                full_task_template = full_task_template.replace("{{ button_class }}", "undo-task-btn")
                                full_task_template = full_task_template.replace("{{ button_icon }}", "↩")


                            full_task_template = full_task_template.replace("{{ task_number }}", str(task_number))
                            full_task_template = full_task_template.replace("{{ task_content }}", html.escape(str(content_of_task)))
                            full_task_template = full_task_template.replace("{{ task_id }}", str(task_id))
                            full_task_template = full_task_template.replace("{{ homework_id }}", str(homework_id))

                        elif type_of_task == "image":
                            full_task_template += imagetask_template

                            if status_of_task == "pending":
                                full_task_template = full_task_template.replace("{{ task_mark_button }}", "Сделано")
                                full_task_template = full_task_template.replace("{{ task_status_text }}", "Не выполнено")
                                full_task_template = full_task_template.replace("{{ task_status_class }}", "pending")
                                full_task_template = full_task_template.replace("{{ button_class }}", "complete-task-btn")
                                full_task_template = full_task_template.replace("{{ button_icon }}", "✓")
                            else:
                                full_task_template = full_task_template.replace("{{ task_mark_button }}", "Отменить")
                                full_task_template = full_task_template.replace("{{ task_status_text }}", "Выполнено")
                                full_task_template = full_task_template.replace("{{ task_status_class }}", "completed")
                                full_task_template = full_task_template.replace("{{ button_class }}", "undo-task-btn")
                                full_task_template = full_task_template.replace("{{ button_icon }}", "↩")

                            full_task_template = full_task_template.replace("{{ task_number }}", str(task_number))
                            full_task_template = full_task_template.replace("{{ task_content }}", str(content_of_task))
                            full_task_template = full_task_template.replace("{{ task_id }}", str(task_id))
                            full_task_template = full_task_template.replace("{{ homework_id }}", str(homework_id))
                            
                if hw[3] == "Активно":
                    hwtemplate = hwtemplate.replace("{{ status_class }}", "active")
                    hwtemplate = hwtemplate.replace("{{ status_text }}", "Активно")
                elif hw[3] == "Завершено":
                    hwtemplate = hwtemplate.replace("{{ status_class }}", "completed")
                    hwtemplate = hwtemplate.replace("{{ status_text }}", "Завершено")
                hwtemplate = hwtemplate.replace("{{ title }}", html.escape(str(hw[0])))
                hwtemplate = hwtemplate.replace("{{ data }}", html.escape(str(hw[2])))
                hwtemplate = hwtemplate.replace("{{ description }}", html.escape(str(hw[1])))
                hwtemplate = hwtemplate.replace("{{ tutor_first_name }}", html.escape(str(hw[4])))
                hwtemplate = hwtemplate.replace("{{ tutor_last_name }}", html.escape(str(hw[5])))
                hwtemplate = hwtemplate.replace("{{ subject }}", html.escape(str(hw[6])))
                hwtemplate = hwtemplate.replace("{{ task_template }}", str(full_task_template))
                
        
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
    

@router.get("/hometut")
def hometut(request: Request):
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
        tutor_id = tutinfo[2]
        
        student_colvo = getstudcolvo(name)

        tuthomework_colvo = gettuthwcolvo(name)

        lessons_today_colvo = gettodaylessonscolvo()

        students = getstudents(name)

        for student in students:
            studtemplate += a
            student_id = student[0]
            studfirst_name = student[1]
            studlast_name = student[2]
            chat_id = getchatid(student_id, tutor_id)

            studtemplate = studtemplate.replace("{{ first_name }}", html.escape(str(studfirst_name)))
            studtemplate = studtemplate.replace("{{ last_name }}", html.escape(str(studlast_name)))
            studtemplate = studtemplate.replace("{{ grade }}", html.escape(str(student[5])))
            studtemplate = studtemplate.replace("{{ avatarstud }}", html.escape(str(studfirst_name[0] + studlast_name[0])))
            studtemplate = studtemplate.replace("{{ chat_id }}", html.escape(str(chat_id)))

        with open(f'{TEMPLATES_PATH}mainpages/hometut.html', 'r', encoding='utf-8') as file:
            content = verstkaprofile(file.read(), name, tutfirst_name, tutlast_name)
        content = content.replace("{{ student_colvo }}", html.escape(str(student_colvo)))
        content = content.replace("{{ homework_colvo }}", html.escape(str(tuthomework_colvo)))
        content = content.replace("{{ studtemplate }}", str(studtemplate))
        content = content.replace("{{ lessons_today }}", html.escape(str(lessons_today_colvo)))
        return HTMLResponse(content=content)
    
    except Exception as e: 
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    

@router.post("/marklessontask")
def marklessontask(request: Request, task_id: str = Form(None), homework_id: str = Form(None)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "student":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)
    
    try:

        marktask(task_id, homework_id)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

    return RedirectResponse(url=f"/home", status_code=303)


@router.post("/add_homework_task/{homework_id}")
async def addhwtask(request: Request, homework_id: int, task_type: str = Form(...), task_text: str = Form(None), task_file: UploadFile = File(None)):
    try:
        name, user_type = get_current_user(request)
        if user_type != "tutor":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)
    
    try:

        if task_type == "text":
            addhwtexttask(homework_id, task_type, task_text)

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
            
            addhwimagetask(homework_id, "image",unique_filename)
                

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)

    return RedirectResponse(url=f"/homeworkstut", status_code=303)
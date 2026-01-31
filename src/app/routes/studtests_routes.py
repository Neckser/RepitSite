import json
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from config import TEMPLATES_PATH
from auth import get_current_user
from utils.templates import verstkaprofile
from services.stats_stud_service import getstudinfo, getstudtests
from services.stats_tut_service import gettutinfobyid
from services.tests_service import gettestquestionsbyid, getquestioncolvobyid, gettestbyid, savestudattempt, gettestanswersandtime, checktestanswers

router = APIRouter()


@router.get("/studtests")
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
        student_id = studinfo[2]

        tests_template = ""

        tests = getstudtests(student_id)

        with open(f"{TEMPLATES_PATH}cards/studtest.html", 'r', encoding='utf-8') as f:
            a = f.read()

        if tests is not None:
            for test in tests:
                tests_template += a
                tutorinfo = gettutinfobyid(test[1])
                tutfirst_name = tutorinfo[0]
                tutlast_name = tutorinfo[1]
                tests_template = tests_template.replace("{{ test_id }}", str(test[0]))
                tests_template = tests_template.replace("{{ title }}", str(test[3]))
                tests_template = tests_template.replace("{{ subject }}", str(test[4]))
                tests_template = tests_template.replace("{{ tutfirst_name }}", tutfirst_name)
                tests_template = tests_template.replace("{{ tutlast_name }}", tutlast_name)
                tests_template = tests_template.replace("{{ question_colvo }}", str(getquestioncolvobyid(test[0])))
                tests_template = tests_template.replace("{{ data }}", str(test[7]))
                tests_template = tests_template.replace("{{ date_start }}", str(test[5]))
                tests_template = tests_template.replace("{{ date_end }}", str(test[6]))
                tests_template = tests_template.replace("{{ duration }}", str(test[8]))
        else:
            with open(f"{TEMPLATES_PATH}ctests/notests/html", 'r', encoding="utf-8") as f:
                tests_template = f.read()



        with open(f"{TEMPLATES_PATH}ctests/studtests.html", 'r', encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name , studfirst_name, studlast_name)
        content = content.replace("{{ tests_template }}", tests_template)
        return HTMLResponse(content=content)
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)


@router.get("/test/s/{test_id}")
def viewtest(request: Request, test_id: int):
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

    
        with open(f"{TEMPLATES_PATH}ctests/studviewtest.html", "r", encoding='utf-8') as f:
            content = verstkaprofile(f.read(), name, studfirst_name, studlast_name)
        content = content.replace("{{ questions_template }}", questions_template)
        content = content.replace("{{ title }}", title)
        content = content.replace("{{ subject }}", subject)
        content = content.replace("{{ test_id }}", str(test_id))
        content = content.replace("{{ duration }}", str(duration))
        return HTMLResponse(content=content)
    

    except Exception as e:
        print(f"Произола ошибка - {e}")
        return RedirectResponse(url="/login", status_code=303)
    

@router.post("/studanswertest")
async def tutanswertest(request: Request, test_id: int = Form(...)):
    try:
        name, user_type = get_current_user(request)

        if user_type != "student":
            return RedirectResponse(url="/login", status_code=303)

    except HTTPException:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        studinfo = getstudinfo(name)
        student_id = studinfo[2]

        form = await request.form()

        testinfo = gettestbyid(test_id)
        title = testinfo[2]
        subject = testinfo[3]
        duration = testinfo[7]

        answersandtime = gettestanswersandtime(form)
        answers = answersandtime[0]
        time = answersandtime[1]
        score = checktestanswers(answers, test_id)
        questions_colvo = getquestioncolvobyid(test_id)
        percent_score = round((score / questions_colvo) * 100, 2)

        savestudattempt(test_id, student_id, time, percent_score)

        with open(f"{TEMPLATES_PATH}ctests/studrestest.html", 'r', encoding='utf-8') as f:
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
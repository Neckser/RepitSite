import json
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from config import TEMPLATES_PATH
from auth import get_current_user
from utils.templates import verstkaprofile
from services.stats_tut_service import gettutorinfo, gettuttests, getstudents
from services.stats_stud_service import getstudinfobyid
from services.tests_service import getquestioncolvobyid, gettestanswersandtime, gettestquestionsbyid, gettestres, getteststudstr, gettestbyid, checktestanswers, createtest, deltest

router = APIRouter()


@router.get("/tuttests")
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

    
@router.get("/tutctest")
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


@router.post("/createtest")
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
    
@router.post("/deletetest")
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
    
@router.get("/testutres/{test_id}")
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

        studstrs = getteststudstr(test_id)

        with open(f"{TEMPLATES_PATH}cards/studtest_res.html", 'r', encoding="utf-8") as f:
            a = f.read()

        for studstr in studstrs:
            studtest_template += a
            student_id = studstr[2]
            studinfo = getstudinfobyid(student_id)
            studfirst_name = studinfo[0]
            studlast_name = studinfo[1]
            data = studstr[4]
            duration = studstr[5]
            score_percent = studstr[6]
            score = (score_percent * questions_colvo) / 100
            studtest_template = studtest_template.replace("{{ studfirst_name }}", studfirst_name)
            studtest_template = studtest_template.replace("{{ studlast_name }}", studlast_name)
            studtest_template = studtest_template.replace("{{ data }}", str(data))
            studtest_template = studtest_template.replace("{{ duration }}", str(duration) + " сек")
            studtest_template = studtest_template.replace("{{ score }}", str(score) + f"/{questions_colvo}")
            studtest_template = studtest_template.replace("{{ score_percent }}", str(score_percent))

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
    

@router.get("/test/t/{test_id}")
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
    

    
@router.get("/restest")
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
    
@router.post("/tutanswertest")
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
    
    
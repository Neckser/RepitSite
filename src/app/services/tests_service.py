import sqlite3
import json
from datetime import datetime, timedelta
from config import DB_PATH


def createtest(tutor_id, form):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""INSERT INTO tests (tutor_id, student_id, title, subject, date_start, date_end, duration) VALUES (?, ?, ?, ?, ?, ?, ?)""", ( tutor_id, form['student_id'], form['test_title'], form['subject'], form['date_start'], form['date_end'], form['test_duration']))
    test_id = cursor.lastrowid

    questions = form.getlist('question[]')
    answers = form.getlist('answer[]')

    for q_text, answer in zip(questions, answers):
        options = {"correct_answer": answer}

        cursor.execute("""INSERT INTO test_questions (test_id, question_type, question_text, options) VALUES (?, 'text', ?, ?)""", (test_id, q_text, json.dumps(options, ensure_ascii=False)))

    mcq_questions = form.getlist('mcq_question[]')

    for index, q_text in enumerate(mcq_questions, start=1):
        options_list = form.getlist(f'mcq_option_{index}[]')
        correct = form.get(f'mcq_correct_{index}')

        if not correct:
            continue

        options = {
            "options": options_list,
            "correct": int(correct) - 1
        }

        cursor.execute("""INSERT INTO test_questions (test_id, question_type, question_text, options) VALUES (?, 'single_choice', ?, ?)""", (test_id, q_text, json.dumps(options, ensure_ascii=False)))

    multi_questions = form.getlist('multi_question[]')

    for index, q_text in enumerate(multi_questions, start=1):
        options_list = form.getlist(f'multi_option_{index}[]')
        correct_list = form.getlist(f'multi_correct_{index}[]')

        correct_indexes = [int(i) - 1 for i in correct_list]

        options = {
            "options": options_list,
            "correct": correct_indexes
        }

        cursor.execute("""INSERT INTO test_questions (test_id, question_type, question_text, options) VALUES (?, 'multi_choice', ?, ?)""", (test_id, q_text, json.dumps(options, ensure_ascii=False)))
    connection.commit()
    connection.close()

    return test_id

def deltest(tutor_id, test_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("DELETE FROM test_questions WHERE test_id = ?",(test_id,))

        cursor.execute("DELETE FROM tests WHERE test_id = ? AND tutor_id = ?",(test_id, tutor_id))
        connection.commit()
    
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e
    
    finally:
        connection.close()

def getquestioncolvobyid(test_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute('''SELECT COUNT(*) FROM test_questions WHERE test_id = ? ORDER BY question_id; ''', (test_id,))
        question_colvo = cursor.fetchone()[0]

        return question_colvo
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()
    
def gettestquestionsbyid(test_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""SELECT question_id, question_type, question_text, options FROM test_questions WHERE test_id = ? ORDER BY question_id""", (test_id,))
        questions = cursor.fetchall()

        return questions
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def gettestbyid(test_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT tutor_id, student_id, title, subject, date_start, date_end, created_at, duration FROM tests WHERE test_id = ?", (test_id,))
        questioninfo = cursor.fetchone()

        return questioninfo
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def gettestanswersandtime(form):
    test_id = int(form.get("test_id"))
    time_spent = int(form.get("time_spent", 0))

    question_ids = [int(q) for q in form.getlist("question_id[]")]
    text_answers = form.getlist("answer_text[]")

    answers = []

    text_index = 0

    for qid in question_ids:
        single = form.get(f"answer_single_{qid}")
        multi = form.getlist(f"answer_multi_{qid}[]")

        if single:
            answers.append({
                "question_id": qid,
                "type": "single",
                "answer": single
            })

        elif multi:
            answers.append({
                "question_id": qid,
                "type": "multi",
                "answer": multi
            })

        else:
            if text_index < len(text_answers):
                text_answer = text_answers[text_index].strip()
                text_index += 1

                if text_answer:
                    answers.append({
                        "question_id": qid,
                        "type": "text",
                        "answer": text_answer
                    })

    return [answers, time_spent]

    
def check_answer(question_type, user_answer, options_json):
    options = json.loads(options_json)

    if question_type == "text":
        correct = options["correct_answer"].strip().lower()
        return user_answer.strip().lower() == correct

    if question_type == "single_choice":
        correct_index = options["correct"]
        correct_value = options["options"][correct_index]
        return user_answer == correct_value

    if question_type == "multi_choice":
        correct_indexes = options["correct"]
        correct_values = {options["options"][i] for i in correct_indexes}
        return set(user_answer) == correct_values

    return False


def checktestanswers(answers, test_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        correct_count = 0

        for a in answers:
            cursor.execute("""SELECT question_type, options FROM test_questions WHERE question_id = ?""", (a["question_id"],))

            q_type, options_json = cursor.fetchone()

            is_correct = check_answer(q_type, a["answer"], options_json)

            if is_correct:
                correct_count += 1

            cursor.execute("""INSERT INTO test_answers (test_id, question_id, answer, is_correct) VALUES (?, ?, ?, ?)""", (test_id, a["question_id"], json.dumps(a["answer"], ensure_ascii=False), int(is_correct)))
            connection.commit()

        return correct_count

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()


def gettestres(test_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""SELECT COUNT(DISTINCT student_id) AS students_passed, ROUND(AVG(score), 2) AS avg_score_percent, ROUND(AVG(duration_seconds), 2) AS avg_duration_seconds, ROUND(AVG(duration_seconds)/60.0, 2) AS avg_duration_minutes FROM test_attempts WHERE test_id = ?""", (test_id,))
        row = cursor.fetchone()

        students_passed, avg_score_percent, avg_duration_seconds, avg_duration_minutes = row

        avg_score_percent = avg_score_percent or 0.0
        avg_duration_seconds = avg_duration_seconds or 0.0
        avg_duration_minutes = avg_duration_minutes or 0.0

        return students_passed, avg_score_percent, avg_duration_seconds, avg_duration_minutes
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()



def savestudattempt(test_id: int, student_id: int, duration: int, score: int):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        end_time = datetime.utcnow()
        start_time = end_time - timedelta(seconds=duration)

        cursor.execute("""INSERT INTO test_attempts (test_id, student_id, start_time, end_time, duration_seconds, score) VALUES (?, ?, ?, ?, ?, ?)""", (test_id, student_id, start_time, end_time, duration, score))
        connection.commit()

        return cursor.lastrowid

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def getteststudstr(test_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM test_attempts WHERE test_id=?", (test_id,))
        studstr = cursor.fetchall()

        return studstr
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()
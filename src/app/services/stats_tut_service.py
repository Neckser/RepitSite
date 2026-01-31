import sqlite3
from utils.dates import build_week_for_tutors
from config import DB_PATH

def gettutsubject(tutlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
    
        cursor.execute('''SELECT subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music FROM tutors WHERE login = ?''', (tutlogin,))
        subjects_row = cursor.fetchone()
    
        if subjects_row:
            subject_names = ["Математика", "Физика", "Химия", "Информатика", "Русский язык", "Английский язык", "Немецкий язык", "Французский язык", "История","Обществознание", "Литература", "Биология", "География", "Экономика","ИЗО", "Музыка"]

            return [subject_names[i] for i, subject in enumerate(subjects_row) if subject is not None]

        return None
    
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e
    
    finally:
        connection.close()

def gettutorinfo(tutlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT first_name, last_name, tutor_id, experience, bio FROM tutors WHERE login = ?", (tutlogin,))
        res = cursor.fetchone()
        if res:
            first_name = res[0]
            last_name = res[1]
            tutor_id = res[2]
            experience = res[3]
            bio = res[4]
            return [first_name, last_name, tutor_id, experience, bio]
        else:
            return None
        
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e
    
    finally:
        connection.close()

def gettutinfobyid(tutor_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT first_name, last_name, login, experience FROM tutors WHERE tutor_id = ?", (tutor_id,))
        res = cursor.fetchone()
        if res:
            tutfirst_name = res[0]
            tutlast_name = res[1]
            tutlogin = res[2]
            experience = res[3]
            return [tutfirst_name, tutlast_name, tutlogin, experience]
        else:
            return None

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()


def gettuthw(tutor_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute('''SELECT h.title, h.description, h.deadline, h.status, h.subject, h.homework_id FROM homeworks h JOIN tutors t ON h.tutor_id = t.tutor_id WHERE h.tutor_id = ? ORDER BY h.deadline ASC''', (tutor_id,))
        homeworks = cursor.fetchall()
        return homeworks

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def getstudcolvo(tutlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute('''SELECT COUNT(*) FROM student_tutors st JOIN tutors t ON st.tutor_id = t.tutor_id WHERE t.login = ?''', (tutlogin,))
        res = cursor.fetchone()
        student_colvo = res[0]
        return student_colvo

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()


def gettuthwcolvo(tutlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute('''SELECT COUNT(*) FROM homeworks st JOIN tutors t ON st.tutor_id = t.tutor_id WHERE t.login = ?''', (tutlogin,))
        res = cursor.fetchone()
        if res:
            tuthomework_colvo = res[0]
            return tuthomework_colvo

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def getstudents(tutlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute('''SELECT s.student_id, s.first_name,  s.last_name,  s.login, s.registration_date, s.grade FROM students s INNER JOIN student_tutors st ON s.student_id = st.student_id INNER JOIN tutors t ON st.tutor_id = t.tutor_id WHERE t.login = ?''', (tutlogin,))
        students = cursor.fetchall()
        return students

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def gettutorgrades(tutlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT g.grade_id, g.student_id, g.subject, g.grade, g.date, g.description, g.tutor_comment FROM grades g JOIN tutors t ON g.tutor_id = t.tutor_id WHERE t.login = ?", (tutlogin,))
        res = cursor.fetchall()
        return res

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def gettutorweektimetable(tutlogin, monday):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                t.schedule_id,
                t.lesson_date,
                t.lesson_time,
                t.subject,
                t.student_id,
                t.status,
                t.notes,
                t.duration
            FROM timetable t
            JOIN tutors tu ON t.tutor_id = tu.tutor_id
            WHERE tu.login = ?
              AND t.lesson_date BETWEEN DATE(?) AND DATE(?, '+6 days')
            ORDER BY t.lesson_date, t.lesson_time
        """, (
            tutlogin,
            monday.strftime("%Y-%m-%d"),
            monday.strftime("%Y-%m-%d")
        ))

        rows = cursor.fetchall()
        return build_week_for_tutors(monday, rows)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

    finally:
        connection.close()


def gettuttests(tutor_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM tests WHERE tutor_id = ? ORDER BY created_at DESC", (tutor_id,))
        tests = cursor.fetchall()

        return tests
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()
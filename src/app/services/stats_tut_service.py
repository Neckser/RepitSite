from db_wrapper import query_one, query_all
from utils.dates import build_week_for_tutors
from datetime import date

def gettutsubject(tutlogin):
    try:
        subjects_row = query_one("""SELECT subject_math, subject_physics, subject_chemistry, subject_computer, 
                                           subject_russian, subject_english, subject_german, subject_french, 
                                           subject_history, subject_social, subject_literature, subject_biology, 
                                           subject_geography, subject_economics, subject_art, subject_music 
                                    FROM tutors WHERE login = ?""", (tutlogin,))
        
        if subjects_row:
            subject_names = ["Математика", "Физика", "Химия", "Информатика", "Русский язык", "Английский язык", 
                           "Немецкий язык", "Французский язык", "История", "Обществознание", "Литература", 
                           "Биология", "География", "Экономика", "ИЗО", "Музыка"]
            return [subject_names[i] for i, subject in enumerate(subjects_row) if subject is not None]
        return None
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e

def gettutorinfo(tutlogin):
    try:
        result = query_one("SELECT first_name, last_name, tutor_id, experience, bio FROM tutors WHERE login = ?", (tutlogin,))
        if result:
            return [result[0], result[1], result[2], result[3], result[4]]
        return None
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e

def gettutinfobyid(tutor_id):
    try:
        result = query_one("SELECT first_name, last_name, login, experience FROM tutors WHERE tutor_id = ?", (tutor_id,))
        if result:
            return [result[0], result[1], result[2], result[3]]
        return None
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def gettuthw(tutor_id):
    try:
        homeworks = query_all("""SELECT h.title, h.description, h.deadline, h.status, h.subject, h.homework_id 
                                 FROM homeworks h JOIN tutors t ON h.tutor_id = t.tutor_id 
                                 WHERE h.tutor_id = ? ORDER BY h.deadline ASC""", (tutor_id,))
        return homeworks if homeworks else []
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def getstudcolvo(tutlogin):
    try:
        result = query_one("SELECT COUNT(*) FROM student_tutors st JOIN tutors t ON st.tutor_id = t.tutor_id WHERE t.login = ?", (tutlogin,))
        return result[0] if result else 0
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def gettuthwcolvo(tutlogin):
    try:
        result = query_one("SELECT COUNT(*) FROM homeworks st JOIN tutors t ON st.tutor_id = t.tutor_id WHERE t.login = ?", (tutlogin,))
        return result[0] if result else 0
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def getstudents(tutlogin):
    try:
        students = query_all("""SELECT s.student_id, s.first_name, s.last_name, s.login, s.registration_date, s.grade 
                                FROM students s INNER JOIN student_tutors st ON s.student_id = st.student_id 
                                INNER JOIN tutors t ON st.tutor_id = t.tutor_id WHERE t.login = ?""", (tutlogin,))
        return students if students else []
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def gettutorgrades(tutlogin):
    try:
        grades = query_all("""SELECT g.grade_id, g.student_id, g.subject, g.grade, g.date, g.description, g.tutor_comment 
                              FROM grades g JOIN tutors t ON g.tutor_id = t.tutor_id WHERE t.login = ?""", (tutlogin,))
        return grades if grades else []
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def gettutorweektimetable(tutlogin, monday):
    try:
        rows = query_all("""
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
              AND t.lesson_date BETWEEN ?::date AND ?::date + INTERVAL '6 days'
            ORDER BY t.lesson_date, t.lesson_time
        """, (
            tutlogin,
            monday.strftime("%Y-%m-%d"),
            monday.strftime("%Y-%m-%d")
        ))
        return build_week_for_tutors(monday, rows if rows else [])
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
def gettuttests(tutor_id):
    try:
        tests = query_all("SELECT * FROM tests WHERE tutor_id = ? ORDER BY created_at DESC", (tutor_id,))
        return tests if tests else []
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def gettodaylessonscolvo():
    try:
        today = date.today()
        result = query_one("SELECT COUNT(*) FROM timetable WHERE lesson_date = ?", (today,))
        return result[0] if result else 0
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
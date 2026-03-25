from db_wrapper import execute, query_one, query_all
from utils.dates import build_week_for_students

def getstudinfo(studlogin):
    try:
        result = query_one("SELECT first_name, last_name, student_id, grade, bio FROM students WHERE login = ?", (studlogin,))
        if result:
            return [result[0], result[1], result[2], result[3], result[4]]
        return None
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e

def getstudinfobyid(student_id):
    try:
        result = query_one("SELECT first_name, last_name, login, grade FROM students WHERE student_id = ?", (student_id,))
        if result:
            return [result[0], result[1], result[2], result[3]]
        return None
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def getstudhwcolvo(studlogin):
    try:
        result = query_one("SELECT COUNT(*) FROM homeworks h JOIN students s ON h.student_id = s.student_id WHERE s.login = ?", (studlogin,))
        return result[0] if result else 0
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e

def gettutorcount(studlogin):
    try:
        result = query_one("SELECT COUNT(*) FROM student_tutors st JOIN students s ON st.student_id = s.student_id WHERE s.login = ?", (studlogin,))
        return result[0] if result else 0
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def getstudhw(student_id):
    try:
        homeworks = query_all("""SELECT h.title, h.description, h.deadline, h.status, t.first_name, t.last_name, h.subject 
                                 FROM homeworks h JOIN tutors t ON h.tutor_id = t.tutor_id 
                                 WHERE h.student_id = ? ORDER BY h.deadline ASC""", (student_id,))
        return homeworks if homeworks else None
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def getstudcompletedhwcolvo(studlogin):
    try:
        result = query_one("""SELECT COUNT(*) FROM homeworks h JOIN students s ON h.student_id = s.student_id 
                              WHERE s.login = ? AND h.status = 'Завершено'""", (studlogin,))
        return result[0] if result else 0
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def gettutlist(studlogin):
    try:
        tutlist = query_all("""SELECT t.tutor_id, t.first_name, t.last_name, t.experience, t.login 
                               FROM tutors t INNER JOIN student_tutors st ON t.tutor_id = st.tutor_id 
                               INNER JOIN students s ON st.student_id = s.student_id WHERE s.login = ?""", (studlogin,))
        return tutlist if tutlist else []
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def getavggrade(studlogin):
    try:
        result = query_one("SELECT AVG(grades.grade) FROM grades JOIN students ON grades.student_id = students.student_id WHERE students.login = ?", (studlogin,))
        avggrade = result[0] if result and result[0] is not None else 0
        return avggrade
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def getcolvofives(studlogin):
    try:
        result = query_one("SELECT COUNT(*) FROM grades JOIN students ON grades.student_id = students.student_id WHERE students.login = ? AND grades.grade = 5", (studlogin,))
        return result[0] if result else 0
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def getcolvogrades(studlogin):
    try:
        result = query_one("SELECT COUNT(*) FROM grades JOIN students ON grades.student_id = students.student_id WHERE students.login = ?", (studlogin,))
        return result[0] if result else 0
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def getstrgrades(studlogin):
    try:
        allgrades = query_all("SELECT grades.* FROM grades JOIN students ON grades.student_id = students.student_id WHERE students.login = ?", (studlogin,))
        return allgrades if allgrades else []
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def getstudentweektimetable(studlogin, monday):
    try:
        rows = query_all("""
            SELECT
                t.schedule_id,
                t.lesson_date,
                t.lesson_time,
                t.subject,
                t.tutor_id,
                t.status,
                t.notes,
                t.duration
            FROM timetable t
            JOIN students s ON t.student_id = s.student_id
            WHERE s.login = ?
              AND t.lesson_date BETWEEN ?::date AND ?::date + INTERVAL '6 days'
            ORDER BY t.lesson_date, t.lesson_time
        """, (
            studlogin,
            monday.strftime("%Y-%m-%d"),
            monday.strftime("%Y-%m-%d")
        ))
        return build_week_for_students(monday, rows if rows else [])
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def getstudtests(student_id):
    try:
        tests = query_all("SELECT * FROM tests WHERE student_id = ? AND date_start <= CURRENT_TIMESTAMP AND date_end >= CURRENT_TIMESTAMP ORDER BY created_at DESC", (student_id,))
        return tests if tests else []
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
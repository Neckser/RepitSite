import sqlite3
from utils.dates import build_week_for_students
from config import DB_PATH

def getstudinfo(studlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT first_name, last_name, student_id, grade, bio FROM students WHERE login = ?", (studlogin,))
        res = cursor.fetchone()
        if res:
            studfirst_name = res[0]
            studlast_name = res[1]
            student_id = res[2]
            grade = res[3]
            bio = res[4]
            return [studfirst_name, studlast_name, student_id, grade, bio]
        else:
            return None
        
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e
    
    finally:
        connection.close()

def getstudinfobyid(student_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT first_name, last_name, login, grade FROM students WHERE student_id = ?", (student_id,))
        res = cursor.fetchone()
        if res:
            studfirst_name = res[0]
            studlast_name = res[1]
            studlogin = res[2]
            grade = res[3]
            return [studfirst_name, studlast_name, studlogin, grade]
        else:
            return None

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

    finally:
        connection.close()

def getstudhwcolvo(studlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute('''SELECT COUNT(*) FROM homeworks h JOIN students s ON h.student_id = s.student_id WHERE s.login = ?''', (studlogin,))
        res = cursor.fetchone()
        homework_colvo = res[0]
        return homework_colvo
            
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e

    finally:
        connection.close()

def gettutorcount(studlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute('''SELECT COUNT(*) FROM student_tutors st JOIN students s ON st.student_id = s.student_id WHERE s.login = ?''', (studlogin,))
        res = cursor.fetchone()
        tutor_count = res[0]
        return tutor_count
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def getstudhw(student_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute(''' SELECT h.title, h.description, h.deadline, h.status, t.first_name, t.last_name, h.subject FROM homeworks h JOIN tutors t ON h.tutor_id = t.tutor_id WHERE h.student_id = ? ORDER BY h.deadline ASC''', (student_id,))
        homeworks = cursor.fetchall()
        if homeworks:
            return homeworks
        else:
            return None

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()


def getstudcompletedhwcolvo(studlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute('''SELECT COUNT(*) FROM homeworks h JOIN students s ON h.student_id = s.student_id WHERE s.login = ? AND h.status = "Завершено"''', (studlogin,))
        res = cursor.fetchone()
        completed_homeworks = res[0]
        return completed_homeworks
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()


def gettutlist(studlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute('''SELECT t.tutor_id, t.first_name, t.last_name, t.experience, t.login FROM tutors t INNER JOIN student_tutors st ON t.tutor_id = st.tutor_id INNER JOIN students s ON st.student_id = s.student_id WHERE s.login = ?''', (studlogin,))
        tutlist = cursor.fetchall()
        return tutlist
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()


def getavggrade(studlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""SELECT AVG(grades.grade) FROM grades JOIN students ON grades.student_id = students.student_id WHERE students.login = ?""", (studlogin,))
        avggrade = cursor.fetchone()[0]
        if avggrade is None:
            avggrade = 0

        return avggrade
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def getcolvofives(studlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute("""SELECT COUNT(*) FROM grades JOIN students ON grades.student_id = students.student_id WHERE students.login = ? AND grades.grade = 5""", (studlogin,))
        colvo_fives = cursor.fetchone()[0]

        return colvo_fives
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def getcolvogrades(studlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute("""SELECT COUNT(*) FROM grades JOIN students ON grades.student_id = students.student_id WHERE students.login = ?""", (studlogin,))
        colvo_grades = cursor.fetchone()[0]

        return colvo_grades
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def getstrgrades(studlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""SELECT grades.* FROM grades JOIN students ON grades.student_id = students.student_id WHERE students.login = ?""", (studlogin,))
        allgrades = cursor.fetchall()
        
        return allgrades

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def getstudentweektimetable(studlogin, monday):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
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
              AND t.lesson_date BETWEEN DATE(?) AND DATE(?, '+6 days')
            ORDER BY t.lesson_date, t.lesson_time
        """, (
            studlogin,
            monday.strftime("%Y-%m-%d"),
            monday.strftime("%Y-%m-%d")
        ))

        rows = cursor.fetchall()
        return build_week_for_students(monday, rows)

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

    finally:
        connection.close()


def getstudtests(student_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""SELECT * FROM tests WHERE student_id = ? AND date_start <= CURRENT_TIMESTAMP AND date_end >= CURRENT_TIMESTAMP ORDER BY created_at DESC""", (student_id,))
        tests = cursor.fetchall()

        return tests

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

    finally:
        connection.close()        
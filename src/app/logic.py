import sqlite3
import random
import locale 
import json
from datetime import datetime, timedelta

DB_PATH = '../../data/basa.db'

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

def create_id():
    return random.randint(1000000, 100000000000000)

def verstka(file, name):
    formatted_content = file.replace("{{ name }}", name)
    return formatted_content

def verstkaprofile(file, name, first_name, last_name):
    formatted_content = file.replace("{{ name }}", name)
    formatted_content = formatted_content.replace("{{ first_name }}", first_name)
    formatted_content = formatted_content.replace("{{ last_name }}", last_name)
    formatted_content = formatted_content.replace("{{ avatar }}", first_name[0] + last_name[0])
    
    return formatted_content

def gethwstatus(deadline):
    try:
        deadline = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
        now = datetime.now()
        if now > deadline:
            return "Завершено"
        else:
            return "Активно"
            
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return "Активно"
    
def updatehwstatus():
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute('''UPDATE homeworks SET status = 'Завершено' WHERE deadline < datetime('now') AND status != 'Завершено' ''')
        connection.commit()
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def studregister(studfirst_name, studlast_name, grade, studlogin, password):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO students (student_id, first_name, last_name, grade, login, password) VALUES (?, ?, ?, ?, ?, ?)", (create_id(), studfirst_name, studlast_name, grade, studlogin, password))
        connection.commit()

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def tutregister(tutfirst_name, tutlast_name, subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music, experience, tutlogin, password):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("INSERT INTO tutors (tutor_id, first_name, last_name, subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music, experience, login, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (create_id(), tutfirst_name, tutlast_name, subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music, experience, tutlogin, password))
        connection.commit()

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def checkstudreg(login, password):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM students WHERE login = ? AND password = ?", (login, password))
        res = cursor.fetchall()
        if res:
            return True
        else:
            return False
    
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e
    
    finally:
        connection.close()

def checktutreg(login, password):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM tutors WHERE login = ? AND password = ?", (login, password))
        res = cursor.fetchall()
        if res:
            return True
        else:
            return False
    
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e
    
    finally:
        connection.close()


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

def checktutexistsbyid(tutor_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT tutor_id FROM tutors WHERE tutor_id = ?", (tutor_id,))
        tutor_exists = cursor.fetchone()
        if tutor_exists:
            return True
        else:
            return False

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()
    
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

def addtutor(student_id, tutor_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute('''SELECT 1 FROM student_tutors WHERE student_id = ? AND tutor_id = ?''', (student_id, tutor_id))
        if cursor.fetchone():
            #Доделать верстку когда такой репетитор уже есть
            pass
        else:
            cursor.execute("INSERT INTO student_tutors (student_id, tutor_id) VALUES (?, ?)", (student_id, tutor_id))
            connection.commit()

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

def addhw(student_id, tutor_id, title, description, subject, deadline):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        status = gethwstatus(deadline)
        
        cursor.execute('''INSERT INTO homeworks (student_id, tutor_id, title, description, subject, deadline, status) VALUES (?, ?, ?, ?, ?, ?, ?)''', (student_id, tutor_id, title, description, subject, deadline, status))
        connection.commit()

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def delhw(homework_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute('''DELETE FROM homeworks WHERE homework_id = ?''', (homework_id,))
        connection.commit()

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def edittutbasic(studfirst_name, studlast_name, experience, tutlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute("UPDATE tutors SET first_name = ?, last_name = ?, experience = ? WHERE login = ?", (studfirst_name, studlast_name, experience, tutlogin))

        connection.commit()
        connection.close()
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

    finally:
        connection.close()

def eduttutsubjects(subjects, tutlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute('''UPDATE tutors SET subject_math = NULL, subject_physics = NULL, subject_chemistry = NULL, subject_computer = NULL, subject_russian = NULL, subject_english = NULL, subject_german = NULL, subject_french = NULL, subject_history = NULL, subject_social = NULL, subject_literature = NULL, subject_biology = NULL, subject_geography = NULL, subject_economics = NULL, subject_art = NULL, subject_music = NULL WHERE login = ?''', (tutlogin,))

        subject_mapping = {"Математика": "subject_math", "Физика": "subject_physics", "Химия": "subject_chemistry", "Информатика": "subject_computer", "Русский": "subject_russian", "Английский": "subject_english", "Немецкий": "subject_german", "Французский": "subject_french", "История": "subject_history", "Обществознание": "subject_social", "Литература": "subject_literature", "Биология": "subject_biology", "География": "subject_geography", "Экономика": "subject_economics", "ИЗО": "subject_art", "Музыка": "subject_music"}

        for subject in subjects:
            if subject in subject_mapping:
                column_name = subject_mapping[subject]
                cursor.execute(f"UPDATE tutors SET {column_name} = ? WHERE login = ?", (subject, tutlogin))

        connection.commit()

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

    finally:
        connection.close()

def edittutbio(bio, tutlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute("UPDATE tutors SET bio = ? WHERE login = ?", (bio, tutlogin))

        connection.commit()

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

    finally:
        connection.close()

def editstudbasic(tutfirst_name, tutlast_name, grade, studlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute("UPDATE students SET first_name = ?, last_name = ?, grade = ? WHERE login = ?", (tutfirst_name, tutlast_name, grade, studlogin))

        connection.commit()
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

    finally:
        connection.close()


def editstudbio(bio, studlogin):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute("UPDATE students SET bio = ? WHERE login = ?", (bio, studlogin))

        connection.commit()

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

def addgrade(student_id, tutor_id, subject, grade, reason, comment):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""INSERT INTO grades (student_id, tutor_id, subject, grade, description, tutor_comment) VALUES (?, ?, ?, ?, ?, ?) """, (student_id, tutor_id, subject, grade, reason, comment))
        connection.commit()

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()


def delgrade(grade_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute('''DELETE FROM grades WHERE grade_id = ?''', (grade_id,))
        connection.commit()

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

# def getmonday(date):
#     date = datetime.strptime(date, "%Y-%m-%d")
#     monday = date - timedelta(days=date.weekday())
#     return monday

def get_base_monday():
    today = datetime.today()
    return today - timedelta(days=today.weekday())


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



def build_week_for_students(monday_date, rows):
    today = datetime.today().strftime("%Y-%m-%d")
    week = {}

    for i in range(7):
        day = monday_date + timedelta(days=i)
        date_str = day.strftime("%Y-%m-%d")
        week[date_str] = {
            "is_today": date_str == today,
            "lessons": []
        }
    for row in rows:
        lesson_date, lesson_time, subject, tutor_id, status, notes, duration = row
        week[lesson_date]["lessons"].append({
            "time": lesson_time,
            "subject": subject,
            "tutor_id": tutor_id,
            "status": status,
            "notes": notes,
            "duration": duration
        })

    for day in week:
        if not week[day]["lessons"]:
            week[day]["lessons"] = "Нет занятий"

    return week

def getweekdates(monday):
    return [f"{(monday + timedelta(days=i)).day} {(monday + timedelta(days=i)).strftime('%B')}" for i in range(7)]


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

def build_week_for_tutors(monday_date, rows):
    today = datetime.today().strftime("%Y-%m-%d")
    week = {}

    for i in range(7):
        day = monday_date + timedelta(days=i)
        date_str = day.strftime("%Y-%m-%d")
        week[date_str] = {
            "is_today": date_str == today,
            "lessons": []
        }
    
    for row in rows:
        schedule_id, lesson_date, lesson_time, subject, student_id, status, notes, duration = row
        week[lesson_date]["lessons"].append({
            "schedule_id": schedule_id,
            "time": lesson_time,
            "subject": subject,
            "student_id": student_id,
            "status": status,
            "notes": notes,
            "duration": duration
        })

    for day in week:
        if not week[day]["lessons"]:
            week[day]["lessons"] = "Нет занятий"

    return week

def addlesson(student_id, tutor_id, subject, lesson_date, lesson_time, duration):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""INSERT INTO timetable (student_id, tutor_id, subject, lesson_date, lesson_time, duration) VALUES (?, ?, ?, ?, ?, ?) """, (student_id, tutor_id, subject, lesson_date, lesson_time, duration))
        connection.commit()

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()


def dellesson(schedule_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute('''DELETE FROM timetable WHERE schedule_id = ?''', (schedule_id,))
        connection.commit()

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

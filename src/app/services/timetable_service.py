from db_wrapper import execute, query_one, query_all

def addlesson(student_id, tutor_id, subject, lesson_date, lesson_time, duration):
    try:
        execute("INSERT INTO timetable (student_id, tutor_id, subject, lesson_date, lesson_time, duration) VALUES (?, ?, ?, ?, ?, ?)", 
                (student_id, tutor_id, subject, lesson_date, lesson_time, duration))
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def dellesson(schedule_id):
    try:
        execute("DELETE FROM timetable WHERE schedule_id = ?", (schedule_id,))
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def addtexttask(lesson_id, task_type, task):
    try:
        execute("INSERT INTO lesson_tasks (schedule_id, type, content) VALUES (?, ?, ?)", 
                (lesson_id, task_type, task))
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
def addimagetask(lesson_id, task_type, filename):
    """Добавляет задание с изображением"""
    try:
        execute("""INSERT INTO lesson_tasks (schedule_id, type, content) VALUES (%s, %s, %s)""", (lesson_id, task_type, filename))
    except Exception as e:
        print(f"Ошибка при добавлении изображения: {e}")
        raise e
    

def getlessontasks(lesson_id):
    try:
        res = query_all("SELECT * FROM lesson_tasks WHERE schedule_id = ?", (lesson_id,))
        return res if res else []
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def addvideolink(lesson_id, link):
    try:
        execute("DELETE FROM lesson_links WHERE schedule_id = ?", (lesson_id,))
        execute("INSERT INTO lesson_links (schedule_id, link) VALUES (?, ?)", (lesson_id, link))
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def getvideolink(lesson_id):
    try:
        res = query_one("SELECT * FROM lesson_links WHERE schedule_id = ?", (lesson_id,))
        return res[2] if res else ""
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def adddesklink(lesson_id, desk):
    try:
        execute("DELETE FROM lesson_desks WHERE schedule_id = ?", (lesson_id,))
        execute("INSERT INTO lesson_desks (schedule_id, desk) VALUES (?, ?)", (lesson_id, desk))
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def getdesklink(lesson_id):
    try:
        res = query_one("SELECT * FROM lesson_desks WHERE schedule_id = ?", (lesson_id,))
        return res[2] if res else ""
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
import sqlite3
from config import DB_PATH

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

def addtexttask(lesson_id, task_type, task):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute('''INSERT INTO lesson_tasks (schedule_id, type, content) VALUES (?, ?, ?) ''', (lesson_id, task_type, task))
        connection.commit()

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def getlessontasks(lesson_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute('''SELECT * FROM lesson_tasks WHERE schedule_id = ?''', (lesson_id,))
        res = cursor.fetchall()

        return res


    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def addvideolink(lesson_id, link):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute('''DELETE FROM lesson_links WHERE schedule_id = ?''', (lesson_id,))
        cursor.execute('''INSERT INTO lesson_links (schedule_id, link) VALUES (?, ?) ''', (lesson_id, link))
        connection.commit()

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def getvideolink(lesson_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute('''SELECT * FROM lesson_links WHERE schedule_id = ?''', (lesson_id,))
        res = cursor.fetchone()

        if res is None:
            return ""
            
        return res[2]



    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()
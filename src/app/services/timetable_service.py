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
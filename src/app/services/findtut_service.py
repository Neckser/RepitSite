import sqlite3
from config import DB_PATH

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
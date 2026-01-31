import sqlite3
from config import DB_PATH

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
import datetime
import sqlite3
from config import DB_PATH

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
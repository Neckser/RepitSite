import datetime
from db_wrapper import execute, query_one, query_all

def gethwstatus(deadline):
    try:
        deadline = datetime.datetime.fromisoformat(deadline.replace('Z', '+00:00'))
        now = datetime.datetime.now()
        if now > deadline:
            return "Завершено"
        else:
            return "Активно"
            
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        return "Активно"
    
def updatehwstatus():
    try:
        execute("UPDATE homeworks SET status = 'Завершено' WHERE deadline < CURRENT_TIMESTAMP AND status != 'Завершено'")
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def addhw(student_id, tutor_id, title, description, subject, deadline):
    try:
        status = gethwstatus(deadline)
        
        execute("INSERT INTO homeworks (student_id, tutor_id, title, description, subject, deadline, status) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                (student_id, tutor_id, title, description, subject, deadline, status))
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def delhw(homework_id):
    try:
        execute("DELETE FROM homeworks WHERE homework_id = ?", (homework_id,))
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
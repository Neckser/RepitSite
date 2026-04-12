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
        active_homeworks = query_all("""SELECT homework_id FROM homeworks WHERE status = 'Активно'""")
        
        if active_homeworks:
            for (homework_id,) in active_homeworks:
                result = query_one("""SELECT COUNT(*) as total, SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed FROM homework_tasks WHERE homework_id = ?""", (homework_id,))
                
                total_tasks = result[0] if result else 0
                completed_tasks = result[1] if result and result[1] else 0
                
                if total_tasks > 0 and completed_tasks == total_tasks:
                    execute("""UPDATE homeworks SET status = 'Завершено' WHERE homework_id = ?""", (homework_id,))
        
        execute("""UPDATE homeworks SET status = 'Завершено' WHERE deadline < CURRENT_TIMESTAMP AND status = 'Активно'""")
        
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
    
def marktask(task_id, homework_id):
    try:
        
        execute("""UPDATE homework_tasks SET status = CASE WHEN status = 'pending' THEN 'completed' WHEN status = 'completed' THEN 'pending' ELSE status END WHERE task_id = %s AND homework_id = %s""", (task_id, homework_id))

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e


def addhwtexttask(homework_id, task_type, task):
    try:
        execute("INSERT INTO homework_tasks (homework_id, type, content, status) VALUES (?, ?, ?, ?)", 
                (homework_id, task_type, task, "pending"))
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    

def addhwimagetask(homework_id, task_type, filename):
    """Добавляет задание с изображением"""
    try:
        execute("""INSERT INTO homework_tasks (homework_id, type, content, status) VALUES (%s, %s, %s, %s)""", (homework_id, task_type, filename, "pending"))
    except Exception as e:
        print(f"Ошибка при добавлении изображения: {e}")
        raise e
    
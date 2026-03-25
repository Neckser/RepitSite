from db_wrapper import execute, query_one

def addtutor(student_id, tutor_id):
    try:
        # Проверяем, существует ли уже такая связь
        existing = query_one("SELECT 1 FROM student_tutors WHERE student_id = ? AND tutor_id = ?", (student_id, tutor_id))
        
        if existing:
            # Доделать верстку когда такой репетитор уже есть
            pass
        else:
            execute("INSERT INTO student_tutors (student_id, tutor_id) VALUES (?, ?)", (student_id, tutor_id))
            
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
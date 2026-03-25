from db_wrapper import execute

def addgrade(student_id, tutor_id, subject, grade, reason, comment):
    try:
        execute("INSERT INTO grades (student_id, tutor_id, subject, grade, description, tutor_comment) VALUES (?, ?, ?, ?, ?, ?)", 
                (student_id, tutor_id, subject, grade, reason, comment))
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def delgrade(grade_id):
    try:
        execute("DELETE FROM grades WHERE grade_id = ?", (grade_id,))
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
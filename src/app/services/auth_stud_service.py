from db_wrapper import execute, query_one, query_all
from utils.id import generate_uuid
from utils.hash import hashpassword
import bcrypt

def studregister(studfirst_name, studlast_name, grade, studlogin, password):
    """Регистрация нового студента"""
    try:
        new_uuid = str(generate_uuid())
        hashed_password = hashpassword(password)
        execute("""INSERT INTO students (student_id, first_name, last_name, grade, login, password) VALUES (%s, %s, %s, %s, %s, %s)""", (new_uuid, studfirst_name, studlast_name, grade, studlogin, hashed_password))
        return True
        
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e


def checkstudreg(login, password):
    """Проверка существования студента"""
    try:
        student = query_one("SELECT * FROM students WHERE login = %s",(login,))
        
        if not student:
            return False
        
        stored_hash = student[6]
        
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
        
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e


def get_student_by_login(login):
    """Получение студента по логину"""
    try:
        return query_one("SELECT * FROM students WHERE login = %s",(login,))
    
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e
    
def checkstudloginexists(login):
    """Проверка существования логина в базе"""
    try:
        student = query_one("SELECT login FROM students WHERE login = %s", (login,))
        return student is not None
        
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e


def get_student_by_id(student_id):
    """Получение студента по ID"""
    try:
        return query_one("SELECT * FROM students WHERE student_id = %s",(student_id,))
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e


def update_student_bio(student_id, bio):
    """Обновление биографии студента"""
    try:
        execute("UPDATE students SET bio = %s WHERE student_id = %s",(bio, student_id))
        return True
    
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e


def get_all_students():
    """Получение всех студентов"""
    try:
        return query_all("SELECT * FROM students ORDER BY registration_date DESC")
    
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e
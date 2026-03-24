import sqlite3
from config import DB_PATH
from utils.id import create_id
from utils.id import generate_uuid

def studregister(studfirst_name, studlast_name, grade, studlogin, password):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        new_uuid = str(generate_uuid())

        cursor.execute("INSERT INTO students (student_id, first_name, last_name, grade, login, password) VALUES (?, ?, ?, ?, ?, ?)", (new_uuid, studfirst_name, studlast_name, grade, studlogin, password))
        connection.commit()

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()


def checkstudreg(login, password):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM students WHERE login = ? AND password = ?", (login, password))
        res = cursor.fetchall()
        if res:
            return True
        else:
            return False
    
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e
    
    finally:
        connection.close()
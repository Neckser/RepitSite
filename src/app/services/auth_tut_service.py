import sqlite3
from config import DB_PATH
from utils.id import create_id
from utils.id import generate_uuid

def tutregister(tutfirst_name, tutlast_name, subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music, experience, tutlogin, password):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        new_uuid = str(generate_uuid())

        cursor.execute("INSERT INTO tutors (tutor_id, first_name, last_name, subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music, experience, login, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (new_uuid, tutfirst_name, tutlast_name, subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music, experience, tutlogin, password))
        connection.commit()

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()

def checktutreg(login, password):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM tutors WHERE login = ? AND password = ?", (login, password))
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

def checktutexistsbyid(tutor_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("SELECT tutor_id FROM tutors WHERE tutor_id = ?", (tutor_id,))
        tutor_exists = cursor.fetchone()
        if tutor_exists:
            return True
        else:
            return False

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()
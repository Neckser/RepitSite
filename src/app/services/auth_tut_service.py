from db_wrapper import execute, query_one, query_all
from utils.id import generate_uuid

def tutregister(tutfirst_name, tutlast_name, subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music, experience, tutlogin, password):
    try:
        new_uuid = str(generate_uuid())
        execute("INSERT INTO tutors (tutor_id, first_name, last_name, subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music, experience, login, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (new_uuid, tutfirst_name, tutlast_name, subject_math, subject_physics, subject_chemistry, subject_computer, subject_russian, subject_english, subject_german, subject_french, subject_history, subject_social, subject_literature, subject_biology, subject_geography, subject_economics, subject_art, subject_music, experience, tutlogin, password))
        return True
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def checktutreg(login, password):
    try:
        tutor = query_one("SELECT * FROM tutors WHERE login = ? AND password = ?", (login, password))
        return tutor is not None
    
    except Exception as e:
        print(f'Произошла ошибка - {e}')
        raise e

def checktutexistsbyid(tutor_id):
    try:
        tutor = query_one("SELECT tutor_id FROM tutors WHERE tutor_id = ?", (tutor_id,))
        return tutor is not None
    
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
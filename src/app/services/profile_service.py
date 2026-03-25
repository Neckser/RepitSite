from db_wrapper import execute

def editutbasic(studfirst_name, studlast_name, experience, tutlogin):
    try:
        execute("UPDATE tutors SET first_name = ?, last_name = ?, experience = ? WHERE login = ?", 
                (studfirst_name, studlast_name, experience, tutlogin))
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def edittutsubjects(subjects, tutlogin):
    try:
        execute("""UPDATE tutors SET 
            subject_math = NULL, subject_physics = NULL, subject_chemistry = NULL, 
            subject_computer = NULL, subject_russian = NULL, subject_english = NULL, 
            subject_german = NULL, subject_french = NULL, subject_history = NULL, 
            subject_social = NULL, subject_literature = NULL, subject_biology = NULL, 
            subject_geography = NULL, subject_economics = NULL, subject_art = NULL, 
            subject_music = NULL WHERE login = ?""", (tutlogin,))

        subject_mapping = {
            "Математика": "subject_math", 
            "Физика": "subject_physics", 
            "Химия": "subject_chemistry", 
            "Информатика": "subject_computer", 
            "Русский": "subject_russian", 
            "Английский": "subject_english", 
            "Немецкий": "subject_german", 
            "Французский": "subject_french", 
            "История": "subject_history", 
            "Обществознание": "subject_social", 
            "Литература": "subject_literature", 
            "Биология": "subject_biology", 
            "География": "subject_geography", 
            "Экономика": "subject_economics", 
            "ИЗО": "subject_art", 
            "Музыка": "subject_music"
        }

        for subject in subjects:
            if subject in subject_mapping:
                column_name = subject_mapping[subject]
                # Используем f-string для имени колонки, но параметры через ?
                execute(f"UPDATE tutors SET {column_name} = ? WHERE login = ?", (subject, tutlogin))

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def edittutbio(bio, tutlogin):
    try:
        execute("UPDATE tutors SET bio = ? WHERE login = ?", (bio, tutlogin))
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def editstudbasic(tutfirst_name, tutlast_name, grade, studlogin):
    try:
        execute("UPDATE students SET first_name = ?, last_name = ?, grade = ? WHERE login = ?", 
                (tutfirst_name, tutlast_name, grade, studlogin))
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def editstudbio(bio, studlogin):
    try:
        execute("UPDATE students SET bio = ? WHERE login = ?", (bio, studlogin))
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
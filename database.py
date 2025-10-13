# database.py
import sqlite3

def init_database():
    connection = sqlite3.connect('basa.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER UNIQUE PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tutors (
            tutor_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            subject_math TEXT,
            subject_physics TEXT,
            subject_chemistry TEXT,
            subject_computer TEXT,
            subject_russian TEXT,
            subject_english TEXT,
            subject_german TEXT,
            subject_french TEXT,
            subject_history TEXT,
            subject_social TEXT,
            subject_literature TEXT,
            subject_biology TEXT,
            subject_geography TEXT,
            subject_economics TEXT,
            subject_art TEXT,
            subject_music TEXT,
            experience INTEGER,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_tutors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            tutor_id INTEGER NOT NULL,
            start_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY (tutor_id) REFERENCES tutors(tutor_id) ON DELETE CASCADE,
            UNIQUE(student_id, tutor_id)
        )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS homeworks (
            homework_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            tutor_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            deadline DATETIME,
            status TEXT DEFAULT 'assigned',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY (tutor_id) REFERENCES tutors(tutor_id) ON DELETE CASCADE
        )''')

    connection.commit()
    connection.close()
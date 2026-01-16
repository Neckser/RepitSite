import sqlite3

DB_PATH = '../../data/basa.db'

def init_database():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER UNIQUE PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            grade INTEGER NOT NULL,
            bio TEXT,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tutors (
            tutor_id INTEGER UNIQUE PRIMARY KEY,
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
            bio TEXT,
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
            subject TEXT NOT NULL,
            deadline DATETIME,
            status TEXT DEFAULT 'Активно',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY (tutor_id) REFERENCES tutors(tutor_id) ON DELETE CASCADE
        )''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timetable (
            schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            tutor_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            lesson_date DATE NOT NULL,
            lesson_time TIME NOT NULL,
            duration INTEGER,
            status TEXT DEFAULT 'scheduled' CHECK(status IN ('scheduled', 'completed', 'cancelled')),
            notes TEXT,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY (tutor_id) REFERENCES tutors(tutor_id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            tutor_id INTEGER NOT NULL,
            subject TEXT NOT NULL,
            grade INTEGER NOT NULL CHECK(grade BETWEEN 2 AND 5),
            date DATETIME DEFAULT CURRENT_TIMESTAMP,
            description TEXT,
            tutor_comment TEXT,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY (tutor_id) REFERENCES tutors(tutor_id) ON DELETE CASCADE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tests (
            test_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tutor_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            date_start DATETIME NOT NULL,
            date_end DATETIME NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            duration INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_questions (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL,
            question_type TEXT NOT NULL CHECK(question_type IN ('text', 'single_choice', 'multi_choice')),
            question_text TEXT NOT NULL,
            options TEXT
        )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS test_attempts (
        attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        end_time DATETIME,
        duration_seconds INTEGER,
        score INTEGER DEFAULT 0,
        max_score INTEGER,
        FOREIGN KEY (test_id) REFERENCES tests(test_id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
    );
    ''')

    connection.commit()
    connection.close()
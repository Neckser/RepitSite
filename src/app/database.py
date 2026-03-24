import sqlite3

DB_PATH = '../../data/basa.db'

def init_database():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT UNIQUE PRIMARY KEY,
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
            tutor_id TEXT UNIQUE PRIMARY KEY,
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
            student_id TEXT NOT NULL,
            tutor_id TEXT NOT NULL,
            start_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY (tutor_id) REFERENCES tutors(tutor_id) ON DELETE CASCADE,
            UNIQUE(student_id, tutor_id)
        )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS homeworks (
            homework_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            tutor_id TEXT NOT NULL,
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
            student_id TEXT NOT NULL,
            tutor_id TEXT NOT NULL,
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
            student_id TEXT NOT NULL,
            tutor_id TEXT NOT NULL,
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
            tutor_id TEXT NOT NULL,
            student_id TEXT NOT NULL,
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
            options TEXT,
            FOREIGN KEY (test_id) REFERENCES tests(test_id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS test_answers (
        answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_id INTEGER,
        question_id INTEGER,
        answer TEXT,
        is_correct INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (test_id) REFERENCES tests(test_id) ON DELETE CASCADE,
        FOREIGN KEY (question_id) REFERENCES test_questions(question_id) ON DELETE CASCADE
    );
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS test_attempts (
        attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_id INTEGER NOT NULL,
        student_id TEXT NOT NULL,
        start_time DATETIME,
        end_time DATETIME,
        duration_seconds INTEGER,
        score INTEGER DEFAULT 0,
        FOREIGN KEY (test_id) REFERENCES tests(test_id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lesson_tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        schedule_id INTEGER,
        type TEXT,
        content TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (schedule_id) REFERENCES timetable(schedule_id) ON DELETE CASCADE
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lesson_links (
        link_id INTEGER PRIMARY KEY AUTOINCREMENT,
        schedule_id INTEGER,
        link TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (schedule_id) REFERENCES timetable(schedule_id) ON DELETE CASCADE
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lesson_desks (
        desk_id INTEGER PRIMARY KEY AUTOINCREMENT,
        schedule_id INTEGER,
        desk TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (schedule_id) REFERENCES timetable(schedule_id) ON DELETE CASCADE
    );
    ''')

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            chat_id TEXT UNIQUE PRIMARY KEY,
            student_id TEXT NOT NULL,
            tutor_id TEXT NOT NULL,
            last_message_text TEXT,
            last_message_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(student_id, tutor_id)  -- чтобы не было дубликатов чатов между теми же людьми
        )
    ''')

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT NOT NULL,
            sender_id TEXT NOT NULL,
            sender_type TEXT NOT NULL CHECK(sender_type IN ('student', 'tutor')),
            message_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chat_id) REFERENCES chats(chat_id) ON DELETE CASCADE
        )
    ''')

    
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_chat_last_message 
        AFTER INSERT ON messages
        BEGIN
            UPDATE chats 
            SET last_message_text = NEW.message_text,
                last_message_at = NEW.created_at 
            WHERE chat_id = NEW.chat_id;
        END;
    ''')

    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_messages_chat_time 
        ON messages(chat_id, created_at DESC)
    ''')

    connection.commit()
    connection.close()
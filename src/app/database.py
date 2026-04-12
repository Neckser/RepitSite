import psycopg2
from psycopg2 import pool
import os
from contextlib import contextmanager

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'postgres'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'tutoring_db'),
    'user': os.getenv('DB_USER', 'tutoring_user'),
    'password': os.getenv('DB_PASSWORD')
}

connection_pool = None

def init_connection_pool():
    """Создает пул соединений с PostgreSQL"""
    global connection_pool
    connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, **DB_CONFIG)

def get_connection():
    """Получить соединение из пула"""
    global connection_pool
    if connection_pool is None:
        init_connection_pool()
    return connection_pool.getconn()

def return_connection(conn):
    """Вернуть соединение в пул"""
    if connection_pool:
        connection_pool.putconn(conn)

@contextmanager
def get_db_cursor():
    """Контекстный менеджер для работы с БД"""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        return_connection(conn)

def init_database():
    """Инициализация базы данных - создание всех таблиц"""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    student_id TEXT UNIQUE PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    grade INTEGER NOT NULL,
                    bio TEXT,
                    login TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cur.execute('''
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
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cur.execute('''
                CREATE TABLE IF NOT EXISTS student_tutors (
                    id SERIAL PRIMARY KEY,
                    student_id TEXT NOT NULL,
                    tutor_id TEXT NOT NULL,
                    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                    FOREIGN KEY (tutor_id) REFERENCES tutors(tutor_id) ON DELETE CASCADE,
                    UNIQUE(student_id, tutor_id)
                )
            ''')
            
            cur.execute('''
                CREATE TABLE IF NOT EXISTS homeworks (
                    homework_id SERIAL PRIMARY KEY,
                    student_id TEXT NOT NULL,
                    tutor_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    subject TEXT NOT NULL,
                    deadline TIMESTAMP,
                    status TEXT DEFAULT 'Активно',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                    FOREIGN KEY (tutor_id) REFERENCES tutors(tutor_id) ON DELETE CASCADE
                )
            ''')

            cur.execute('''
                CREATE TABLE IF NOT EXISTS homework_tasks (
                    task_id SERIAL PRIMARY KEY,
                    homework_id INTEGER NOT NULL,
                    type TEXT,
                    content TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (homework_id) REFERENCES homeworks(homework_id) ON DELETE CASCADE
                )
            ''')
            
            cur.execute('''
                CREATE TABLE IF NOT EXISTS timetable (
                    schedule_id SERIAL PRIMARY KEY,
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
            
            cur.execute('''
                CREATE TABLE IF NOT EXISTS grades (
                    grade_id SERIAL PRIMARY KEY,
                    student_id TEXT NOT NULL,
                    tutor_id TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    grade INTEGER NOT NULL CHECK(grade BETWEEN 2 AND 5),
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    description TEXT,
                    tutor_comment TEXT,
                    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                    FOREIGN KEY (tutor_id) REFERENCES tutors(tutor_id) ON DELETE CASCADE
                )
            ''')
            
            cur.execute('''
                CREATE TABLE IF NOT EXISTS tests (
                    test_id SERIAL PRIMARY KEY,
                    tutor_id TEXT NOT NULL,
                    student_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    date_start TIMESTAMP NOT NULL,
                    date_end TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    duration INTEGER NOT NULL
                )
            ''')
            
            cur.execute('''
                CREATE TABLE IF NOT EXISTS test_questions (
                    question_id SERIAL PRIMARY KEY,
                    test_id INTEGER NOT NULL,
                    question_type TEXT NOT NULL CHECK(question_type IN ('text', 'single_choice', 'multi_choice')),
                    question_text TEXT NOT NULL,
                    options TEXT,
                    FOREIGN KEY (test_id) REFERENCES tests(test_id) ON DELETE CASCADE
                )
            ''')
            
            cur.execute('''
                CREATE TABLE IF NOT EXISTS test_answers (
                    answer_id SERIAL PRIMARY KEY,
                    test_id INTEGER,
                    question_id INTEGER,
                    answer TEXT,
                    is_correct INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (test_id) REFERENCES tests(test_id) ON DELETE CASCADE,
                    FOREIGN KEY (question_id) REFERENCES test_questions(question_id) ON DELETE CASCADE
                )
            ''')
            
            cur.execute('''
                CREATE TABLE IF NOT EXISTS test_attempts (
                    attempt_id SERIAL PRIMARY KEY,
                    test_id INTEGER NOT NULL,
                    student_id TEXT NOT NULL,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    duration_seconds INTEGER,
                    score INTEGER DEFAULT 0,
                    FOREIGN KEY (test_id) REFERENCES tests(test_id) ON DELETE CASCADE,
                    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
                )
            ''')
            
            cur.execute('''
                CREATE TABLE IF NOT EXISTS lesson_tasks (
                    task_id SERIAL PRIMARY KEY,
                    schedule_id INTEGER,
                    type TEXT,
                    content TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (schedule_id) REFERENCES timetable(schedule_id) ON DELETE CASCADE
                )
            ''')
            
            cur.execute('''
                CREATE TABLE IF NOT EXISTS lesson_links (
                    link_id SERIAL PRIMARY KEY,
                    schedule_id INTEGER,
                    link TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (schedule_id) REFERENCES timetable(schedule_id) ON DELETE CASCADE
                )
            ''')
            
            cur.execute('''
                CREATE TABLE IF NOT EXISTS lesson_desks (
                    desk_id SERIAL PRIMARY KEY,
                    schedule_id INTEGER,
                    desk TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (schedule_id) REFERENCES timetable(schedule_id) ON DELETE CASCADE
                )
            ''')
            
            cur.execute('''
                CREATE TABLE IF NOT EXISTS chats (
                    chat_id TEXT UNIQUE PRIMARY KEY,
                    student_id TEXT NOT NULL,
                    tutor_id TEXT NOT NULL,
                    last_message_text TEXT,
                    last_message_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(student_id, tutor_id)
                )
            ''')
            
            cur.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    message_id SERIAL PRIMARY KEY,
                    chat_id TEXT NOT NULL,
                    sender_id TEXT NOT NULL,
                    sender_type TEXT NOT NULL CHECK(sender_type IN ('student', 'tutor')),
                    message_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (chat_id) REFERENCES chats(chat_id) ON DELETE CASCADE
                )
            ''')
            
            cur.execute('''
                CREATE OR REPLACE FUNCTION update_chat_last_message()
                RETURNS TRIGGER AS $$
                BEGIN
                    UPDATE chats 
                    SET last_message_text = NEW.message_text,
                        last_message_at = NEW.created_at 
                    WHERE chat_id = NEW.chat_id;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            ''')
            
            cur.execute('''
                DROP TRIGGER IF EXISTS update_chat_last_message_trigger ON messages;
                CREATE TRIGGER update_chat_last_message_trigger
                AFTER INSERT ON messages
                FOR EACH ROW
                EXECUTE FUNCTION update_chat_last_message();
            ''')
            
            cur.execute('''
                CREATE INDEX IF NOT EXISTS idx_messages_chat_time 
                ON messages(chat_id, created_at DESC)
            ''')
            
            conn.commit()
            
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        return_connection(conn)
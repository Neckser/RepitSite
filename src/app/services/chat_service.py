import sqlite3
from config import DB_PATH
from utils.id import generate_uuid


def getchatmessages(chat_id: str, limit: int = 100):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute('''SELECT message_id, sender_id, sender_type, message_text, created_at FROM messages WHERE chat_id = ? ORDER BY created_at ASC LIMIT ? ''', (chat_id, limit))
        messages = cursor.fetchall()

        return messages

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()


def getchatsbytutorid(tutor_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute('''SELECT c.chat_id, c.student_id, s.first_name, s.last_name, s.login, c.last_message_text, c.last_message_at FROM chats c JOIN students s ON c.student_id = s.student_id WHERE c.tutor_id = ? ORDER BY c.last_message_at DESC''', (tutor_id,))
        chats = cursor.fetchall()
        
        return chats

    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e
    
    finally:
        connection.close()


def addmessage(chat_id, sender_id, sender_type, message_text):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute('''INSERT INTO messages (chat_id, sender_id, sender_type, message_text) VALUES (?, ?, ?, ?)''', (chat_id, sender_id, sender_type, message_text))
        connection.commit()
        
    except Exception as e:
        print(f"Ошибка базы данных: {e}")
        raise e
    
    finally:
        connection.close()


def getstudentchatinfo(chat_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute("SELECT s.student_id, s.first_name, s.last_name FROM students s JOIN chats c ON s.student_id = c.student_id WHERE c.chat_id = ?;", (chat_id,))
        chatstudentinfo = cursor.fetchone()
        
        return chatstudentinfo
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        raise e
    
    finally:
        connection.close()


def gettutorchatinfo(chat_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        cursor.execute("""SELECT t.tutor_id, t.first_name, t.last_name, t.login FROM tutors t JOIN chats c ON t.tutor_id = c.tutor_id WHERE c.chat_id = ?;""", (chat_id,))
        chattutorinfo = cursor.fetchone()

        return chattutorinfo
        
    except Exception as e:
        print(f"Ошибка при получении информации о репетиторе: {e}")
        raise e
    
    finally:
        connection.close()

def generatecontacttotutor(student_id, tutor_id):
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        
        newuuid = str(generate_uuid())
        
        cursor.execute('''INSERT INTO chats (chat_id, student_id, tutor_id) VALUES (?, ?, ?)''', (newuuid, student_id, tutor_id))
        connection.commit()
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        raise e
    
    finally:
        connection.close()
from db_wrapper import execute, query_one, query_all
from utils.id import generate_uuid

def getchatmessages(chat_id: str, limit: int = 100):
    try:
        messages = query_all("""SELECT message_id, sender_id, sender_type, message_text, created_at 
                                FROM messages WHERE chat_id = ? ORDER BY created_at ASC LIMIT ?""", 
                             (chat_id, limit))
        return messages if messages else []
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def getchatsbytutorid(tutor_id):
    try:
        chats = query_all("""SELECT c.chat_id, c.student_id, s.first_name, s.last_name, s.login, 
                                    c.last_message_text, c.last_message_at 
                             FROM chats c JOIN students s ON c.student_id = s.student_id 
                             WHERE c.tutor_id = ? ORDER BY c.last_message_at DESC""", (tutor_id,))
        return chats if chats else []
    except Exception as e:
        print(f"Произошла ошибка - {e}")
        raise e

def addmessage(chat_id, sender_id, sender_type, message_text):
    try:
        execute("INSERT INTO messages (chat_id, sender_id, sender_type, message_text) VALUES (?, ?, ?, ?)", 
                (chat_id, sender_id, sender_type, message_text))
    except Exception as e:
        print(f"Ошибка базы данных: {e}")
        raise e

def getstudentchatinfo(chat_id):
    try:
        result = query_one("""SELECT s.student_id, s.first_name, s.last_name 
                              FROM students s JOIN chats c ON s.student_id = c.student_id 
                              WHERE c.chat_id = ?""", (chat_id,))
        return result if result else None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        raise e

def gettutorchatinfo(chat_id):
    try:
        result = query_one("""SELECT t.tutor_id, t.first_name, t.last_name, t.login 
                              FROM tutors t JOIN chats c ON t.tutor_id = c.tutor_id 
                              WHERE c.chat_id = ?""", (chat_id,))
        return result if result else None
    except Exception as e:
        print(f"Ошибка при получении информации о репетиторе: {e}")
        raise e

def generatecontacttotutor(student_id, tutor_id):
    """Создает чат между студентом и репетитором, если его еще нет"""
    try:
        existing_chat = query_one("SELECT chat_id FROM chats WHERE student_id = %s AND tutor_id = %s",(student_id, tutor_id))
        
        if existing_chat:
            pass

        else:
            newuuid = str(generate_uuid())
            execute("INSERT INTO chats (chat_id, student_id, tutor_id) VALUES (%s, %s, %s)", (newuuid, student_id, tutor_id))
        
    except Exception as e:
        print(f"Произошла ошибка в generatecontacttotutor: {e}")
        raise e

def checkchatexists(chat_id):
    try:
        result = query_one("SELECT EXISTS(SELECT 1 FROM chats WHERE chat_id = ?)", (chat_id,))
        return bool(result[0]) if result else False
    except Exception as e:
        print(f"Ошибка при проверке чата: {e}")
        return False

def getchatid(student_id, tutor_id):
    try:
        result = query_one("SELECT chat_id FROM chats WHERE student_id = ? AND tutor_id = ?", 
                          (student_id, tutor_id))
        return result[0] if result else ""
    except Exception as e:
        print(f"Ошибка при получении chat_id: {e}")
        return False
from fastapi.responses import HTMLResponse
import re

def checkrequiredfields(data: dict, required_fields: list, error_template: str):
    """
    Проверяет наличие обязательных полей
    
    Args:
        data: словарь с данными формы
        required_fields: список обязательных полей
        error_template: путь к HTML шаблону ошибки
    
    Returns:
        HTMLResponse если есть ошибка, иначе None
    """
    missing = []
    for field in required_fields:
        value = data.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(field)
    
    if missing:
        with open(error_template, 'r', encoding='utf-8') as file:
            content = file.read()
        return HTMLResponse(content=content, status_code=400)
    
    return None


def is_strong_password(password: str) -> tuple[bool, str]:
    """
    Проверяет, что пароль:
    - Не менее 8 символов
    - Содержит хотя бы одну цифру
    - Содержит хотя бы одну заглавную букву
    - Содержит хотя бы одну строчную букву
    Возвращает (True, "") если пароль надежный, иначе (False, "причина")
    """
    if len(password) < 8:
        return False, "Пароль должен содержать не менее 8 символов"
    if not re.search(r"\d", password):
        return False, "Пароль должен содержать хотя бы одну цифру"
    if not re.search(r"[A-Z]", password):
        return False, "Пароль должен содержать хотя бы одну заглавную букву"
    if not re.search(r"[a-z]", password):
        return False, "Пароль должен содержать хотя бы одну строчную букву"
    return True, ""

def is_valid_login(login: str) -> tuple[bool, str]:
    """
    Проверяет, что логин:
    - Не менее 6 символов
    - Содержит только буквы и цифры
    """
    if len(login) < 6:
        return False, "Логин должен содержать не менее 6 символов"
    if not re.match(r"^[A-Za-z0-9]+$", login):
        return False, "Логин должен содержать только латинские буквы и цифры"
    return True, ""
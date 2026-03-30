from fastapi.responses import HTMLResponse

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
from fastapi import Request
from fastapi.responses import HTMLResponse
from config import TEMPLATES_PATH

async def error404(request: Request, exc):
    with open(f'{TEMPLATES_PATH}errors/error.html', 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content, status_code=404)

async def error500(request: Request, exc):
    with open(f'{TEMPLATES_PATH}errors/error.html', 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content, status_code=500)
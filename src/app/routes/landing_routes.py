from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from config import TEMPLATES_PATH

router = APIRouter()

@router.get("/")
def start():
    with open(f"{TEMPLATES_PATH}landing/mainlanding.html", "r", encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)

@router.get("/policy")
def policy():
    with open(f"{TEMPLATES_PATH}landing/policy.html", 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content)

@router.get("/cookies")
def cookies():
    with open(f"{TEMPLATES_PATH}landing/cookies.html", 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content)

@router.get("/terms")
def terms():
    with open(f"{TEMPLATES_PATH}landing/terms.html", 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content)

@router.get("/contact")
def contact():
    with open(f"{TEMPLATES_PATH}landing/contact.html", 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content)

@router.get("/faq")
def faq():
    with open(f"{TEMPLATES_PATH}landing/faq.html", 'r', encoding='utf-8') as f:
        content = f.read()
    return HTMLResponse(content=content)

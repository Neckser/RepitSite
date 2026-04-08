from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from config import TEMPLATES_PATH
from auth import get_current_user

router = APIRouter()

@router.get("/admin")
def adminpanel(request: Request):
    with open (f"{TEMPLATES_PATH}/admin/adminpanel.html", 'r', encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content = content)
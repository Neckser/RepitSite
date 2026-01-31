from fastapi import APIRouter
from fastapi.responses import FileResponse
from config import TEMPLATES_PATH

router = APIRouter()

@router.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")

@router.get("/yandexlogo.svg")
def yandexlogo():
    return FileResponse("static/yandexlogo.svg")
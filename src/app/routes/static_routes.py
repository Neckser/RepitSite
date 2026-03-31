from fastapi import APIRouter
from fastapi.responses import FileResponse
from config import TEMPLATES_PATH
import os
from fastapi import HTTPException

router = APIRouter()

@router.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")

@router.get("/yandexlogo.svg")
def yandexlogo():
    return FileResponse("static/yandexlogo.svg")


UPLOAD_DIR = os.getenv('UPLOAD_DIR', '/app/uploads')

@router.get("/viewimage/{filename}")
async def view_image(filename: str):
    """Отдает картинку по имени файла"""
    file_path = os.path.join(UPLOAD_DIR, "tasks", filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(file_path)
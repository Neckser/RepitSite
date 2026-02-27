import os
import uuid
import shutil
from pathlib import Path
from fastapi import UploadFile

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/app/uploads"))

def save_upload_file(upload_file: UploadFile) -> str:

    extension = Path(upload_file.filename).suffix.lower()
    
    new_filename = f"{uuid.uuid4().hex}{extension}"
    
    dest_path = UPLOAD_DIR / new_filename
    
    try:
        with dest_path.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
    finally:
        upload_file.close()
        
    return new_filename

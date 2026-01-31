import time
import jwt
from fastapi import HTTPException, Request
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE

def create_access_token(username: str, user_type: str):
    payload = {
        "sub": username,
        "type": user_type,
        "exp": time.time() + ACCESS_TOKEN_EXPIRE
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401)
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"], payload["type"]

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401)

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401)

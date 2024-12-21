import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Callable
from uuid import UUID

from dotenv import load_dotenv
from fastapi import Depends, Header, HTTPException, Request
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import get_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


class TokenData(BaseModel):
    user_id: str

def create_token(user_id: str):
    print(f"SECRET KEY: {SECRET_KEY}")
    expiration = datetime.now() + timedelta(hours=1)
    payload = {"user_id": user_id, "exp": expiration}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(**payload)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


''''''''''''''''''

def authorize_user(func):
    @wraps(func)
    async def wrapper(request: Request, authorization: str = Header(None), session: Session = Depends(get_db), *args, **kwargs):
        if authorization is None or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        
        token = authorization.split(" ")[1]
        user_uuid_str = decode_token(token)
        user_uuid =  UUID(user_uuid_str)
        
        return await func(request, user_uuid=user_uuid, session=session, *args, **kwargs)
    
    return wrapper
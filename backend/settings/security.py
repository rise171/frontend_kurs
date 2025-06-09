from fastapi import Depends
from jose import JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from typing import Optional

from models.user import User
from settings.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from settings.database import get_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.PyJWTError:
        return None

async def get_current_user(credentials: HTTPBearer = Depends(security), session: AsyncSession = Depends(get_session)) -> User:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
            
        # Получаем пользователя из базы
        result = await session.get(User, user_id)
        if result is None:
            raise HTTPException(status_code=401, detail="User not found")
            
        return result
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return current_user
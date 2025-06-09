from pydantic import BaseModel, EmailStr
from typing import Optional
from schemas.feedback import UserRole

class UserCreate(BaseModel):
    username: str
    login: str
    password: str
    role: UserRole = UserRole.USER  # По умолчанию обычный пользователь

class UserDelete(BaseModel):
    id: int

class UserUpdate(BaseModel):
    id: int
    username: Optional[str] = None
    role: Optional[UserRole] = None
    
class UserGetting(BaseModel):
    id: int
    username: str
    login: str
    role: UserRole

    class Config:
        orm_mode = True

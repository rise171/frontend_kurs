from typing import List, Dict

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from schemas.user import UserCreate, UserGetting
from services.auth import AuthService
from services.user import UserService
from settings.database import get_session
from settings.security import get_current_user
from models.user import User, UserRole

router = APIRouter(prefix="/user", tags=["Auth"])

class LoginRequest(BaseModel):
    login: str
    password: str

async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Проверяет, является ли текущий пользователь администратором"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Only administrators can access this resource"
        )
    return current_user

@router.post("/login", response_model=dict)
async def login_user(data: LoginRequest, session: AsyncSession = Depends(get_session)):
    return await AuthService.login_user(data.login, data.password, session)

@router.post("/register", response_model=UserGetting)
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    user_id = await AuthService.register_user(user_data, session)
    if not user_id:
        raise HTTPException(status_code=400, detail="User already exists")

    user = await AuthService.get_user_profile(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    return user


@router.get("/profile/{user_id}", response_model=UserGetting)
async def get_user_profile(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await AuthService.get_user_profile(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    return user

@router.get("/get_users", response_model=List[UserGetting])
async def get_users(
    limit: int = Query(100, description="Maximum number of users to return", ge=1, le=500),
    offset: int = Query(0, description="Offset for pagination", ge=0),
    session: AsyncSession = Depends(get_session)
):
    return await UserService.get_all_users(session=session, limit=limit, offset=offset)

@router.delete("/{user_id}", response_model=Dict[str, str])
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_admin_user),
    session: AsyncSession = Depends(get_session)
):
    """Delete user by ID (admin only)."""
    # Проверяем, чтобы админ не удалил сам себя
    if user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete your own admin account"
        )
    
    success, message = await UserService.delete_user(user_id, session)
    return {"message": message}



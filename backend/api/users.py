from fastapi import APIRouter, Depends, HTTPException
from typing import List
from schemas.user import UserCreate, UserGetting, UserUpdate
from services.user import UserService
from api.auth import get_admin_user
from models.user import User
from settings.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserGetting])
async def get_all_users(
    limit: int = 100,
    offset: int = 0,
    current_user: User = Depends(get_admin_user),
    session: AsyncSession = Depends(get_session)
):
    """Get all users (admin only)."""
    return await UserService.get_all_users(session=session, limit=limit, offset=offset)

@router.get("/{user_id}", response_model=UserGetting)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_admin_user),
    session: AsyncSession = Depends(get_session)
):
    """Get user by ID (admin only)."""
    user = await UserService.get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user 
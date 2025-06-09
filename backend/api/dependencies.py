from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from settings.database import get_session
from services.auth import AuthService
from models.user import UserRole
from repository.auth_repos import AuthRepos

async def get_current_user(
    session: AsyncSession = Depends(get_session),
    request: Request = None
):
    # Получаем текущего пользователя через репозиторий
    user = await AuthRepos.get_current_user(session, request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_admin_user(current_user=Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user 
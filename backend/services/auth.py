from sqlalchemy.ext.asyncio import AsyncSession
from repository.auth_repos import AuthRepos
from schemas.user import UserCreate
from sqlalchemy.future import select
from fastapi import Depends
from settings.database import get_session
from fastapi import HTTPException
from models.user import User

class AuthService:
    @staticmethod
    async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)) -> int:
        user_id = await AuthRepos.register_user(
            login=user_data.login,
            username=user_data.username,
            password=user_data.password,
            role=user_data.role,
            session=session
        )
        if not user_id:
            return None
        user = await AuthService.get_user_profile(user_id, session)
        if not user:
            raise HTTPException(status_code=404)
        return user.id

    @staticmethod
    async def get_user_profile(user_id: int, session: AsyncSession = Depends(get_session)):
        result = await session.execute(select(User).filter(User.id == user_id))
        user = result.scalar()
        return user

    @staticmethod
    async def login_user(login: str, password: str, session: AsyncSession = Depends(get_session)):
        # Логика аутентификации
        token_data = await AuthRepos.login_user(login, password, session)
        if not token_data:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {
            "access_token": token_data["access_token"],
            "token_type": "bearer",
            "user_id": token_data["user_id"],
            "role": token_data["role"]
        }
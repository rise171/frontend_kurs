from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User, UserRole
from settings.database import get_session
from settings.security import hash_password, verify_password, decode_jwt_token
from sqlalchemy.future import select
from fastapi import Depends, Request
from settings.security import create_jwt_token as create_access_token


class AuthRepos:
    @staticmethod
    async def register_user(
        login: str,
        username: str,
        password: str,
        role: UserRole = UserRole.USER,
        session: AsyncSession = Depends(get_session)
    ):
        existing_user = await session.execute(select(User).filter(User.login == login))
        if existing_user.scalar():
            return None

        hashed_password = hash_password(password)

        # Автоматически назначаем роль администратора для admin@gmail.com
        if login == "admin@gmail.com":
            role = UserRole.ADMIN

        new_user = User(
            username=username,
            login=login,
            hashed_password=hashed_password,
            role=role
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user.id

    @staticmethod
    async def authenticate_user(login: str, password: str, session: AsyncSession):
        result = await session.execute(select(User).filter(User.login == login))
        user = result.scalar_one_or_none()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    async def login_user(login: str, password: str, session: AsyncSession):
        user = await AuthRepos.authenticate_user(login, password, session)
        if not user:
            return None

        access_token = create_access_token(data={"sub": str(user.id)})
        return {
            "access_token": access_token,
            "user_id": user.id,
            "role": user.role
        }

    @staticmethod
    async def get_current_user(session: AsyncSession, request: Request = None):
        if not request:
            return None
            
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            return None
            
        token = authorization.split(" ")[1]
        try:
            payload = decode_jwt_token(token)
            user_id = int(payload.get("sub"))
            result = await session.execute(select(User).filter(User.id == user_id))
            return result.scalar_one_or_none()
        except:
            return None
from typing import Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from repository.user import UserRepository
from schemas.user import UserGetting, UserCreate, UserUpdate
from settings.security import hash_password
from fastapi import HTTPException

class UserService:
    @staticmethod
    async def create_user(
        user_data: UserCreate,
        session: AsyncSession
    ) -> UserGetting:
        repo = UserRepository(session)
        user_data.password = hash_password(user_data.password)
        user = await repo.create(user_data)
        return UserGetting.from_orm(user)

    @staticmethod
    async def get_user_by_id(
        user_id: int,
        session: AsyncSession
    ) -> Optional[UserGetting]:
        repo = UserRepository(session)
        user = await repo.get_by_id(user_id)
        return UserGetting.from_orm(user) if user else None

    @staticmethod
    async def update_user(
        user_id: int,
        user_data: UserUpdate,
        session: AsyncSession
    ) -> Optional[UserGetting]:
        repo = UserRepository(session)
        user = await repo.update(user_id, user_data)
        return UserGetting.from_orm(user) if user else None

    @staticmethod
    async def get_all_users(
        session: AsyncSession,
        limit: int = 100,
        offset: int = 0
    ) -> List[UserGetting]:
        repo = UserRepository(session)
        users = await repo.get_all(limit=limit, offset=offset)
        return [UserGetting.from_orm(user) for user in users]

    @staticmethod
    async def delete_user(
        user_id: int,
        session: AsyncSession
    ) -> Tuple[bool, str]:
        repo = UserRepository(session)
        success, message = await repo.delete(user_id)
        if not success:
            raise HTTPException(status_code=400, detail=message)
        return success, message
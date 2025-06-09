from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from models.user import User, UserRole
from schemas.user import UserCreate, UserUpdate
from typing import Optional, List, Tuple
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

class UserRepository:
    def __init__(self, session: AsyncSession):
        if session is None:
            raise HTTPException(status_code=500, detail="Database session is not initialized")
        self.session = session

    async def create(self, user_data: UserCreate) -> User:
        user = User(
            username=user_data.username,
            login=user_data.login,
            hashed_password=user_data.password,
            role=UserRole.USER
        )
        self.session.add(user)
        try:
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="User with this username or login already exists")

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_by_login(self, login: str) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.login == login))
        return result.scalars().first()

    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        try:
            await self.session.execute(
                update(User)
                .where(User.id == user_id)
                .values(**user_data.model_dump(exclude_unset=True))
            )
            await self.session.commit()
            return await self.get_by_id(user_id)
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail="User with this username or login already exists")

    async def delete(self, user_id: int) -> Tuple[bool, str]:
        user = await self.get_by_id(user_id)
        if not user:
            return False, "User not found"
            
        if user.role == UserRole.ADMIN:
            admin_count = await self.count_admins()
            if admin_count <= 1:
                return False, "Cannot delete the last admin user"

        try:
            # Удаляем связанные записи (каскадное удаление)
            await self.session.delete(user)
            await self.session.commit()
            return True, "User deleted successfully"
        except Exception as e:
            await self.session.rollback()
            return False, f"Failed to delete user: {str(e)}"

    async def get_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        result = await self.session.execute(
            select(User)
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def count_admins(self) -> int:
        result = await self.session.execute(
            select(User).where(User.role == UserRole.ADMIN)
        )
        return len(result.scalars().all())
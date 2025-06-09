from datetime import date
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from repository.mood import MoodRepository
from schemas.mood import MoodGetting, MoodCreate, MoodUpdate
from fastapi import HTTPException

class MoodService:
    @staticmethod
    async def create_mood(
        mood_data: MoodCreate,
        user_id: int,
        session: AsyncSession
    ) -> MoodGetting:
        repo = MoodRepository(session)
        mood = await repo.create(mood_data, user_id)
        return MoodGetting.from_orm(mood)

    @staticmethod
    async def get_moods(
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        session: AsyncSession = None
    ) -> List[MoodGetting]:
        repo = MoodRepository(session)
        moods = await repo.get_all_for_user(user_id, start_date, end_date)
        return [MoodGetting.from_orm(m) for m in moods]

    @staticmethod
    async def update_mood(
        mood_id: int,
        mood_update: MoodUpdate,
        user_id: int,
        session: AsyncSession
    ) -> Optional[MoodGetting]:
        repo = MoodRepository(session)
        mood = await repo.update(mood_id, mood_update, user_id)
        return MoodGetting.from_orm(mood) if mood else None

    @staticmethod
    async def delete_mood(
        mood_id: int,
        user_id: int,
        session: AsyncSession
    ) -> bool:
        repo = MoodRepository(session)
        # Проверяем, принадлежит ли запись пользователю
        mood = await repo.get_by_id(mood_id)
        if not mood:
            raise HTTPException(status_code=404, detail="Mood entry not found")
        if mood.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this mood entry")
            
        return await repo.delete(mood_id)

    @staticmethod
    async def get_statistics(
        user_id: int,
        month: Optional[int] = None,
        year: Optional[int] = None,
        session: AsyncSession = None
    ) -> dict:
        repo = MoodRepository(session)
        return await repo.get_statistics(user_id, month, year)

    @staticmethod
    async def get_mood_by_date(
        user_id: int,
        target_date: date,
        session: AsyncSession
    ) -> List[MoodGetting]:
        """Get all mood entries for a specific date."""
        repo = MoodRepository(session)
        moods = await repo.get_by_date(user_id, target_date)
        return [MoodGetting.from_orm(m) for m in moods]
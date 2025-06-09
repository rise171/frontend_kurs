from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.mood import MoodCalendar
from schemas.mood import MoodCreate, MoodUpdate
from datetime import datetime, date
from typing import Optional, List
from fastapi import HTTPException

class MoodRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, mood_data: MoodCreate, user_id: int) -> MoodCalendar:
        mood = MoodCalendar(
            user_id=user_id,
            mood=mood_data.mood,
            date=mood_data.date or datetime.utcnow()
        )
        self.session.add(mood)
        await self.session.commit()
        await self.session.refresh(mood)
        return mood

    async def get_by_id(self, mood_id: int) -> Optional[MoodCalendar]:
        result = await self.session.execute(
            select(MoodCalendar).where(MoodCalendar.id == mood_id)
        )
        return result.scalars().first()

    async def get_all_for_user(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[MoodCalendar]:
        query = select(MoodCalendar).where(MoodCalendar.user_id == user_id)
        
        if start_date:
            query = query.where(func.date(MoodCalendar.date) >= start_date)
        if end_date:
            query = query.where(func.date(MoodCalendar.date) <= end_date)
            
        query = query.order_by(MoodCalendar.date.desc())
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, mood_id: int, mood_update: MoodUpdate, user_id: int) -> Optional[MoodCalendar]:
        mood = await self.get_by_id(mood_id)
        if not mood:
            raise HTTPException(status_code=404, detail="Mood entry not found")
        
        if mood.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this mood entry")
        
        update_data = mood_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key != 'id':  # Игнорируем попытку изменить ID
                setattr(mood, key, value)
        
        await self.session.commit()
        await self.session.refresh(mood)
        return mood

    async def delete(self, mood_id: int) -> bool:
        mood = await self.get_by_id(mood_id)
        if mood:
            await self.session.delete(mood)
            await self.session.commit()
            return True
        return False

    async def get_statistics(self, user_id: int, month: Optional[int] = None, year: Optional[int] = None) -> dict:
        query = select(MoodCalendar.mood, func.count(MoodCalendar.id))\
            .where(MoodCalendar.user_id == user_id)
            
        if month and year:
            query = query.where(
                func.extract('month', MoodCalendar.date) == month,
                func.extract('year', MoodCalendar.date) == year
            )
        elif year:
            query = query.where(func.extract('year', MoodCalendar.date) == year)
            
        query = query.group_by(MoodCalendar.mood)
        result = await self.session.execute(query)
        
        return {mood: count for mood, count in result.all()}

    async def get_by_date(
        self,
        user_id: int,
        target_date: date
    ) -> List[MoodCalendar]:
        """Get all mood entries for a specific date."""
        query = select(MoodCalendar).where(
            MoodCalendar.user_id == user_id,
            func.date(MoodCalendar.date) == target_date
        ).order_by(MoodCalendar.date.desc())
        
        result = await self.session.execute(query)
        return result.scalars().all()